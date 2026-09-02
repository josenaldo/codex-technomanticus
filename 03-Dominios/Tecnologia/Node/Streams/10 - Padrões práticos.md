---
title: "Padrões práticos"
created: 2026-05-08
updated: 2026-06-28
type: concept
fase: magus
status: growing
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

## Fundamento teórico

Streams em Node.js são implementações do padrão **produtor-consumidor**: uma fonte gera dados em um ritmo arbitrário; um destino os consome em outro ritmo. Quando a fonte é mais rápida que o destino, o mecanismo de backpressure freia a produção — protegendo a memória. Quando o destino está livre, a produção retoma.

Cada padrão desta nota resolve uma variação do mesmo problema: **processar dados em fluxo contínuo sem acumular tudo na memória**. A arquitetura é sempre a mesma:

```mermaid
flowchart LR
    classDef neutro fill:#1B2029,stroke:#4E5666,color:#C6CCD8
    A["Fonte\n(createReadStream, fetch, DB cursor)"]
    B["Transform 1\n(parse, filter, enrich)"]
    C["Transform 2\n(serialize, compress)"]
    D["Destino\n(createWriteStream, S3, HTTP response)"]

    A -->|"chunks\nbinários"| B
    B -->|"objetos JS\nou linhas"| C
    C -->|"bytes\nserializados"| D

    class A neutro
    class B neutro
    class C neutro
    class D neutro
```

Cada Transform faz **uma única coisa** — o princípio de separação de responsabilidades aplicado a pipelines de dados. `pipeline()` conecta os estágios e garante limpeza automática de recursos em caso de erro.

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

## Armadilhas comuns

> [!warning] Line parser sem `_flush` — última linha perdida
> **O que acontece:** a última linha de um arquivo sem `\n` final nunca é emitida — o dado desaparece silenciosamente. **Por quê:** o `_buffer` interno guarda o fragmento incompleto entre chunks. Sem `_flush`, esse fragmento nunca é liberado quando o stream encerra. **Como evitar:** implementar sempre `_flush(cb)` em qualquer Transform que mantém buffer interno. Chamar `callback()` ao final.

> [!warning] Multipart sem stream — buffer everything no body
> **O que acontece:** uploads de 2 GB usam 2 GB de RAM por requisição; sob carga, o processo fica sem memória. **Por quê:** `express.json()` e `body-parser` bufferizam o corpo HTTP inteiro antes de passar para o handler. Não foram projetados para uploads de arquivo. **Como evitar:** usar `busboy` (ou `multer`, que usa busboy internamente) diretamente no `req` — parseia o corpo chunk a chunk sem materializar na memória.

> [!warning] Tee com consumers de velocidades muito diferentes
> **O que acontece:** o consumer rápido fica bloqueado esperando o lento; a fonte fica parada; latência total sobe para o pior caso. **Por quê:** `PassThrough` aplica backpressure de ambos os consumers. O consumer lento (ex: upload para S3 via conexão lenta) segura o rápido (ex: gravação em disco local). **Como evitar:** avaliar se processamento sequencial é aceitável; ou bufferizar explicitamente no consumer lento com queue interna; ou aceitar que o rápido espera o lento.

> [!warning] `fileStream` não consumido no busboy — requisição trava
> **O que acontece:** o evento `close` do busboy nunca dispara; a requisição HTTP fica pendurada até o cliente desistir. **Por quê:** se o handler do evento `file` não consumir o `fileStream` (nem `pipeline`, nem `.resume()`), o busboy para de parsear o body — o parser fica bloqueado esperando o consumer drenar. **Como evitar:**
> ```javascript
> bb.on('file', async (fieldname, fileStream, info) => {
>   try {
>     await pipeline(fileStream, createWriteStream(`/tmp/${info.filename}`));
>   } catch (err) {
>     fileStream.resume(); // drena mesmo em erro — impede o travamento
>   }
> });
> ```

> [!warning] `TextDecoder` sem `{ stream: true }` — caracteres multibyte corrompidos
> **O que acontece:** caracteres UTF-8 de 2–4 bytes que chegam partidos entre dois chunks são decodificados errado — exibem `?` ou `â€` no lugar do caractere original. **Por quê:** sem `stream: true`, cada chamada a `decode()` trata o chunk como texto completo e descarta o estado de decodificação entre chunks. **Como evitar:** sempre passar `{ stream: true }` no loop e omitir o flag (ou passar `{ stream: false }`) na chamada final após o loop.

---

## Casos práticos

### Cenário 1 — Pipeline de ingestão de logs multiservidor em NDJSON

Em sistemas distribuídos, é comum agregar logs de múltiplos serviços em um único arquivo de análise. Cada arquivo de log tem milhares de linhas; processar tudo em memória não é viável.

```javascript
// ingest-logs.js
import { createReadStream, createWriteStream } from 'node:fs';
import { Transform } from 'node:stream';
import { pipeline } from 'node:stream/promises';
import { LineParser } from './line-parser.js';

// Enriquece cada linha de log com metadados do serviço
class LogEnricher extends Transform {
  constructor(serviceName) {
    super({ objectMode: true, readableObjectMode: true, writableObjectMode: true });
    this._service = serviceName;
  }

  _transform(line, _enc, callback) {
    try {
      const entry = JSON.parse(line);
      this.push({
        ...entry,
        service: this._service,
        ingestedAt: new Date().toISOString(),
      });
    } catch {
      // Linha malformada: descarta silenciosamente em logs de produção
      // Em debug, emitir evento 'warning' aqui
    }
    callback();
  }
}

// Serializa objetos JS de volta para NDJSON
const toNdjson = new Transform({
  writableObjectMode: true,
  transform(obj, _enc, callback) {
    callback(null, JSON.stringify(obj) + '\n');
  },
});

// Processa logs de 3 serviços, cada um como pipeline separado
const services = ['auth', 'api', 'worker'];

for (const service of services) {
  await pipeline(
    createReadStream(`./logs/${service}.log`),
    new LineParser(),
    new LogEnricher(service),
    toNdjson,
    createWriteStream('./logs/aggregated.ndjson', { flags: 'a' }), // append
  );
  console.log(`Ingestão concluída: ${service}`);
}
```

O pipeline garante que cada serviço seja processado sequencialmente e que erros em um serviço não corrompam o output — `pipeline()` fecha todos os streams envolvidos em caso de falha.

### Cenário 2 — Streaming de resposta de LLM para cliente HTTP

APIs de LLM (Anthropic, OpenAI) retornam tokens via SSE. O servidor deve repassar cada token para o cliente assim que chega — sem bufferizar a resposta completa.

```javascript
// llm-proxy.js (Express)
import { Readable } from 'node:stream';
import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic();

app.post('/chat', async (req, res) => {
  const { message } = req.body;

  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');

  try {
    // stream() retorna AsyncIterable de eventos SSE
    const stream = await client.messages.stream({
      model: 'claude-opus-4-5',
      max_tokens: 1024,
      messages: [{ role: 'user', content: message }],
    });

    // Itera token a token e escreve para o cliente
    for await (const event of stream) {
      if (event.type === 'content_block_delta') {
        const text = event.delta?.text ?? '';
        // Formato SSE: "data: <payload>\n\n"
        res.write(`data: ${JSON.stringify({ text })}\n\n`);
      }
    }

    res.write('data: [DONE]\n\n');
    res.end();
  } catch (err) {
    console.error('Erro no streaming LLM:', err);
    res.status(500).end();
  }
});
```

O padrão `for await...of` processa cada evento à medida que chega — sem esperar a resposta completa. Se o cliente desconectar, o loop termina naturalmente na próxima iteração quando `res.write()` falhar.

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

- *"Como você processaria um CSV de 10 GB sem estourar a memória?"* → Pipeline: `createReadStream` → `csv-parser` (Transform) → Transform de processamento → `createWriteStream`. Nunca `fs.readFileSync`.

- *"Como você implementaria upload de arquivo grande no Express?"* → `busboy` pipeado do `req`, com o `fileStream` de cada arquivo pipeado para o destino final (S3 via SDK, disco via `fs`).

- *"Como você consumiria streaming de um LLM?"* → `fetch()` → `for await (const chunk of response.body)` → decodificar com `TextDecoder({ stream: true })` → exibir token a token.

---

## O que vem a seguir

Com os padrões práticos dominados, o próximo passo é entender quando streams realmente valem o overhead — e como diagnosticar gargalos quando a pipeline é lenta:

- `[[11 - Performance e tuning]]` — quando streams perdem para buffer everything, como ajustar `highWaterMark`, sync vs async transforms
- `[[12 - Armadilhas, regras práticas, cheatsheet]]` — consolidação final: top 10+ armadilhas, decision tree e vocabulário completo

---

## Fontes

- [Node.js — stream module](https://nodejs.org/api/stream.html) — documentação oficial de `Transform`, `pipeline`, `PassThrough` e todas as APIs usadas nos padrões desta nota
- [busboy — streaming multipart parser](https://github.com/mscdex/busboy) — parser de `multipart/form-data` sem bufferização; base para `multer`
- [csv-parser](https://github.com/mafintosh/csv-parser) — Transform stream para CSV com suporte a quoting, BOM e escape; passa no csv-spectrum test suite

---

## Veja também

- `[[03 - Readable streams]]`
- `[[04 - Writable streams]]`
- `[[05 - Duplex e Transform]]`
- `[[07 - pipeline vs pipe - error handling]]`
- `[[08 - Async iteration de streams]]`
- `[[09 - Web Streams - interop com padrão universal]]`
- `[[Node.js]]` (tronco)
