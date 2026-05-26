---
title: "Padrões práticos"
created: 2026-05-08
updated: 2026-05-08
type: concept
status: seedling
publish: true
tags:
  - node
  - streams
  - patterns
  - line-parser
  - csv
aliases:
  - Stream patterns
  - line parser
  - CSV streaming
  - fetch streaming
---

# Padrões práticos

> [!abstract] TL;DR
> Recipes do dia a dia: line parser, CSV → JSONL, multipart upload, fetch streaming e stream tee. Cada um em sua sub-seção; foco em "este é o pattern, copie e adapte". Quando a lógica for simples, implemente na mão. Quando o formato for complexo (multipart, CSV com quoting, logs estruturados), use uma lib madura como `csv-parser` ou `busboy`.

---

## O que é

Esta nota é um catálogo de **padrões recorrentes de streams em produção**. Não é referência de API — é receita. Cada padrão tem um code sample completo e uma nota de armadilha.

Padrões cobertos:

| # | Padrão | Caso de uso típico |
|---|---|---|
| 1 | **Line parser** | Processar arquivos de log ou NDJSON linha a linha |
| 2 | **CSV → JSONL** | Converter dump de banco em formato consumível por outras ferramentas |
| 3 | **Multipart upload streaming** | Receber upload de arquivo grande sem explodir a RAM |
| 4 | **Fetch streaming** | Consumir LLM SSE, downloads grandes, ou APIs de streaming |
| 5 | **Stream tee** | Enviar os mesmos bytes para dois destinos simultâneos |
| 6 | **Multiplexing N streams** | Concatenar várias fontes em um único stream de saída |

---

## Padrão 1: Line parser

Um `Transform` que acumula chunks num buffer interno e emite uma linha completa a cada `\n`. O detalhe crítico é o método `_flush`: ele garante que a última linha — que pode chegar sem `\n` final — não seja descartada.

```js
// line-parser.js
import { Transform } from 'node:stream';

class LineParser extends Transform {
  constructor(options = {}) {
    super({ ...options, objectMode: true });
    this._buffer = '';
  }

  _transform(chunk, _encoding, callback) {
    this._buffer += chunk.toString();
    const lines = this._buffer.split('\n');
    // A última parte pode ser incompleta — guarda pro próximo chunk
    this._buffer = lines.pop();
    for (const line of lines) {
      if (line.trim()) this.push(line);
    }
    callback();
  }

  _flush(callback) {
    // Emite o que sobrou no buffer (última linha sem \n)
    if (this._buffer.trim()) this.push(this._buffer);
    this._buffer = '';
    callback();
  }
}

export { LineParser };
```

Uso:

```js
import { createReadStream } from 'node:fs';
import { pipeline } from 'node:stream/promises';
import { LineParser } from './line-parser.js';
import { Writable } from 'node:stream';

await pipeline(
  createReadStream('access.log'),
  new LineParser(),
  new Writable({
    objectMode: true,
    write(line, _enc, cb) {
      console.log('linha:', line);
      cb();
    },
  })
);
```

> [!warning] Armadilha
> Sem `_flush`, a última linha do arquivo — se não terminar com `\n` — fica presa no `_buffer` e nunca é emitida. Sempre implemente `_flush`.

---

## Padrão 2: CSV → JSONL

Compose de Transforms em pipeline: `LineParser` → separação por vírgula → `JSON.stringify` → arquivo JSONL. A ideia é que cada Transform faça uma única coisa.

```js
// csv-to-jsonl.js
import { createReadStream, createWriteStream } from 'node:fs';
import { Transform } from 'node:stream';
import { pipeline } from 'node:stream/promises';
import { LineParser } from './line-parser.js';

// Transform: string de linha CSV → objeto JS
class CsvRowToObject extends Transform {
  constructor() {
    super({ objectMode: true, readableObjectMode: true, writableObjectMode: true });
    this._headers = null;
  }

  _transform(line, _enc, callback) {
    const cols = line.split(',').map((c) => c.trim());
    if (!this._headers) {
      this._headers = cols; // primeira linha = cabeçalho
    } else {
      const obj = Object.fromEntries(this._headers.map((h, i) => [h, cols[i]]));
      this.push(obj);
    }
    callback();
  }
}

// Transform: objeto JS → string JSON + newline
const toJsonl = new Transform({
  writableObjectMode: true,
  transform(obj, _enc, callback) {
    callback(null, JSON.stringify(obj) + '\n');
  },
});

await pipeline(
  createReadStream('dados.csv'),
  new LineParser(),
  new CsvRowToObject(),
  toJsonl,
  createWriteStream('saida.jsonl')
);

console.log('Conversão concluída.');
```

> [!tip] Quando usar lib
> `CsvRowToObject` acima não trata aspas, escapes ou valores multilinhas. Para CSV real (Excel exports, dumps de banco), use `csv-parser` — um Transform stream que faz isso a ~90 000 linhas/s e passa no csv-spectrum test suite:
> ```js
> import csv from 'csv-parser';
> import { createReadStream } from 'node:fs';
> createReadStream('dados.csv').pipe(csv()).on('data', (row) => console.log(row));
> ```

---

## Padrão 3: Multipart upload streaming

Imagine um endpoint que recebe upload de vídeos grandes. Bufferizar o `req` inteiro antes de processar explode a RAM e não escala. A solução é usar `busboy`: um Writable que parseia `multipart/form-data` chunk a chunk, emitindo cada arquivo como um Readable stream.

```js
// upload-route.js  (Express)
import busboy from 'busboy';
import { createWriteStream } from 'node:fs';
import { pipeline } from 'node:stream/promises';

app.post('/upload', (req, res) => {
  const bb = busboy({ headers: req.headers });

  bb.on('file', async (fieldname, fileStream, info) => {
    const { filename } = info;
    console.log(`Recebendo: ${filename}`);

    try {
      // O fileStream é um Readable — pipe direto pro disco (ou S3, ou GCS)
      await pipeline(fileStream, createWriteStream(`/tmp/${filename}`));
      console.log(`Salvo: ${filename}`);
    } catch (err) {
      console.error('Erro ao salvar arquivo:', err);
      fileStream.resume(); // drena o stream mesmo em erro
    }
  });

  bb.on('field', (name, value) => {
    console.log(`Campo: ${name} = ${value}`);
  });

  bb.on('close', () => res.json({ status: 'ok' }));
  bb.on('error', (err) => res.status(500).json({ error: err.message }));

  req.pipe(bb);
});
```

> [!warning] Armadilha
> Se o `fileStream` não for consumido (nem por pipeline, nem por `.resume()`), o busboy trava e nunca emite o evento `close`. A requisição fica pendurada para sempre.

---

## Padrão 4: Fetch streaming

`fetch()` retorna `response.body` como um `ReadableStream` da Web Streams API. Bom para consumir respostas grandes (downloads, LLM streaming, SSE) sem bufferizar tudo em memória.

```js
// fetch-streaming.js
const url = 'https://example.com/large-file.ndjson';
const response = await fetch(url);

if (!response.ok) throw new Error(`HTTP ${response.status}`);

// response.body é um ReadableStream (Web Streams) — iterável com for-await
let lineBuffer = '';
const decoder = new TextDecoder();

for await (const chunk of response.body) {
  lineBuffer += decoder.decode(chunk, { stream: true });
  const lines = lineBuffer.split('\n');
  lineBuffer = lines.pop(); // última parte pode estar incompleta

  for (const line of lines) {
    if (line.trim()) {
      const obj = JSON.parse(line);
      console.log(obj);
    }
  }
}

// Último fragmento (se houver)
if (lineBuffer.trim()) console.log(JSON.parse(lineBuffer));
```

Para integrar com Node Streams (ex: passar por um `pipeline`), converta com `Readable.fromWeb()`:

```js
import { Readable } from 'node:stream';
import { pipeline } from 'node:stream/promises';

const response = await fetch(url);
const nodeReadable = Readable.fromWeb(response.body);

await pipeline(
  nodeReadable,
  new LineParser(),
  // ... demais estágios
);
```

> [!tip] Caso de uso: LLM streaming
> APIs como a da Anthropic ou OpenAI retornam SSE via `response.body`. O loop `for await` processa cada token à medida que chega, sem esperar a resposta completa — essencial para UI responsiva.

---

## Padrão 5: Stream tee

`tee` = bifurcar um stream para dois consumidores. Útil para "salvar no disco E enviar para S3 ao mesmo tempo", ou "processar E logar simultaneamente".

A forma mais pragmática em Node Streams é um `PassThrough`:

```js
// stream-tee.js
import { createReadStream, createWriteStream } from 'node:fs';
import { PassThrough } from 'node:stream';
import { pipeline } from 'node:stream/promises';

async function teeToTwoSinks(sourcePath, sink1Path, sink2Path) {
  const source = createReadStream(sourcePath);
  const passthrough = new PassThrough();

  // Inicia os dois pipelines a partir do PassThrough
  const p1 = pipeline(passthrough, createWriteStream(sink1Path));
  const p2 = pipeline(passthrough, createWriteStream(sink2Path));

  // Alimenta o PassThrough com a fonte
  source.pipe(passthrough);

  // Aguarda ambos os destinos terminarem
  await Promise.all([p1, p2]);
}

await teeToTwoSinks('video-original.mp4', '/tmp/copia-local.mp4', '/tmp/copia-backup.mp4');
```

Para Web Streams, a API tem `.tee()` nativo:

```js
const [branch1, branch2] = response.body.tee();
// branch1 e branch2 são ReadableStreams independentes
```

> [!warning] Armadilha
> Se os dois consumidores têm velocidades muito diferentes, o mais lento aplica backpressure sobre o `PassThrough`, que por sua vez freia a fonte. O stream mais rápido fica bloqueado esperando o mais lento. Se isso for um problema, use um buffer explícito no consumidor lento, ou aceite que o rápido vai esperar.

---

## Padrão 6 (bônus): Multiplexing N streams em 1

Concatenar múltiplas fontes em um único stream de saída — útil para "servir vários arquivos como um único body de resposta", ou "concatenar logs de múltiplos serviços".

```js
// merge-streams.js
import { Readable, PassThrough } from 'node:stream';
import { pipeline } from 'node:stream/promises';
import { createReadStream } from 'node:fs';

/**
 * Concatena N Readable streams em sequência num único stream de saída.
 * Cada fonte é drenada por completo antes de iniciar a próxima.
 */
async function mergeSequential(sources, destination) {
  for (const source of sources) {
    await pipeline(source, destination, { end: false }); // não fecha o destino entre fontes
  }
  destination.end(); // fecha só no final
}

const files = ['parte1.log', 'parte2.log', 'parte3.log'].map(createReadStream);
const output = createWriteStream('merged.log');

await mergeSequential(files, output);
console.log('Arquivos concatenados.');
```

Para merge **concorrente** (intercalar chunks de N fontes sem ordem garantida), use `stream.addListener('data')` em cada fonte e empurre tudo para um `PassThrough` compartilhado — mas atenção ao gerenciamento de `end`: só feche o destino quando **todas** as fontes encerrarem.

---

## Na prática

**Quando implementar na mão:**

- A lógica é simples (line parser, JSON stringify, contador de bytes).
- O formato é trivial (NDJSON, texto, binary blob sem framing).
- Zero dependências é um requisito.

**Quando usar uma lib:**

| Necessidade | Lib |
|---|---|
| CSV com quoting, escapes, BOM | `csv-parser` |
| Multipart / form-data | `busboy` |
| Logging estruturado de alta performance | `pino` |
| Gzip/brotli | `node:zlib` (built-in) |
| Criptografia | `node:crypto` (built-in) |

A regra prática: se o formato tem uma spec (RFC, MIME type, W3C), existe uma lib madura para ele. Não reimplemente multipart na mão.

---

## Armadilhas

> [!bug] Armadilha 1: Line parser sem `_flush` → última linha perdida
> O `_buffer` interno guarda o fragmento incompleto entre chunks. Se `_flush` não for implementado, esse fragmento nunca é emitido. Arquivos sem `\n` final — comum em logs — perdem a última entrada silenciosamente.

> [!bug] Armadilha 2: Multipart sem stream → buffer everything no body
> Usar `express.json()` ou `body-parser` em rotas de upload bufferiza o corpo inteiro antes de passar para o handler. Um upload de 2 GB usa 2 GB de RAM por requisição. Use `busboy` (ou `multer`, que usa busboy internamente) para processar chunk a chunk.

> [!bug] Armadilha 3: Tee com consumidores de velocidades muito diferentes
> O `PassThrough` aplica backpressure de ambos os consumers. O consumer lento segura o rápido. Se um dos destinos for uma rede lenta (S3 via conexão ruim) e o outro for disco local rápido, o disco vai esperar a rede. Avalie se processamento sequencial (primeiro disco, depois S3) seria mais simples e aceitável.

> [!bug] Armadilha 4: `fileStream` não consumido no busboy
> Se o handler do evento `file` não consumir o `fileStream` (nem pipe, nem `.resume()`), o busboy para de parsear o body e o evento `close` nunca dispara. A requisição trava.

> [!bug] Armadilha 5: `TextDecoder` sem `{ stream: true }` em fetch streaming
> Sem a opção `stream: true`, o decoder trata cada chunk como um texto completo. Caracteres multibyte (UTF-8 de 2–4 bytes) que chegam partidos entre dois chunks são decodificados errado. Sempre passe `{ stream: true }` no loop e `{ stream: false }` (ou nenhum flag) na chamada final.

---

## Em entrevista

**Frase pronta:**

> "Common stream patterns in production: a line parser is a Transform with an internal buffer that splits chunks on newlines, with `_flush` to emit any partial last line. CSV-to-JSONL is just a pipeline of Transforms — line parser, CSV split, `JSON.stringify`, write to file with newlines. For multipart uploads, libraries like `busboy` give you Transforms that parse the body chunk by chunk without buffering. For `fetch()` streaming, the response body is a Web Stream that you can iterate with `for await of`. For sending the same data to multiple sinks, `tee()` or `PassThrough` clones the stream."

**Vocabulário:**

| PT-BR | EN |
|---|---|
| analisador de linhas | line parser |
| buffer interno | internal buffer |
| upload multipart | multipart upload |
| streaming de fetch | fetch streaming |
| bifurcação de stream | stream tee |
| multiplexação | multiplexing |
| modo objeto | object mode |
| descarte / drenagem | drain / resume |

**Perguntas que podem vir:**

- *"Como você processaria um CSV de 10 GB sem estourar a memória?"*
  → Pipeline: `createReadStream` → `csv-parser` (Transform) → Transform de processamento → `createWriteStream`. Nunca `fs.readFileSync`.

- *"Como você implementaria upload de arquivo grande no Express?"*
  → `busboy` pipeado do `req`, com o `fileStream` de cada arquivo pipeado para o destino final (S3 via SDK, disco via `fs`).

- *"Como você consumiria streaming de um LLM?"*
  → `fetch()` → `for await (const chunk of response.body)` → decodificar com `TextDecoder({ stream: true })` → exibir token a token.

---

## Veja também

- `[[03 - Readable streams]]`
- `[[04 - Writable streams]]`
- `[[05 - Duplex e Transform]]`
- `[[07 - pipeline vs pipe - error handling]]`
- `[[08 - Async iteration de streams]]`
- `[[09 - Web Streams - interop com padrão universal]]`
- `[[Node.js]]` (tronco)
