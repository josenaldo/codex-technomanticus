---
title: "Duplex e Transform"
created: 2026-05-08
updated: 2026-05-08
type: concept
status: seedling
publish: true
tags:
  - node
  - streams
  - duplex
  - transform
aliases:
  - Duplex
  - Transform
  - _transform
  - _flush
---

# Duplex e Transform

> [!abstract] TL;DR
> `Duplex` implementa leitura e escrita **independentes** — dois buffers separados, dois canais lógicos sem conexão entre si. O exemplo canônico é o socket TCP: você lê dados que chegam do peer e escreve dados que vão para o peer, cada lado na sua própria velocidade. `Transform` é um `Duplex` onde a escrita **alimenta** a leitura após uma transformação — o que você escreve sai transformado do outro lado. Implementação custom: subclasse `Transform` + `_transform(chunk, enc, cb)` + opcional `_flush(cb)` para emitir o estado final quando o stream encerra.

---

## O que é

Node.js expõe quatro tipos de stream. `Duplex` e `Transform` são os dois que combinam leitura e escrita na mesma instância — mas de formas fundamentalmente diferentes.

### Duplex

`stream.Duplex` é uma stream que implementa **simultaneamente** as interfaces `Readable` e `Writable`. Internamente mantém **dois buffers separados**: um para o lado leitor, outro para o lado escritor. Esses buffers são independentes — cada um tem seu próprio `highWaterMark`, sua própria lógica de backpressure e seu próprio estado de fluxo.

A palavra-chave é **independência**: o que você escreve em um Duplex não tem relação automática com o que você lê dele. São dois canais lógicos que coexistem na mesma instância por conveniência de API.

> [!example] Analogia física
> Pense em um cano bidirecional onde água pode correr nos dois sentidos ao mesmo tempo, mas os fluxos não se misturam — cada direção é um canal distinto dentro da mesma estrutura.

O exemplo canônico da documentação oficial é `net.Socket`:

- **Lado Readable**: dados que chegam do peer remoto (você lê).
- **Lado Writable**: dados que você envia para o peer (você escreve).

Esses lados operam em velocidades diferentes, com buffers diferentes, sem nenhuma transformação de um para o outro.

### Transform

`stream.Transform` **estende** `stream.Duplex`. A diferença crítica: o lado Writable está **conectado** ao lado Readable através de uma transformação. O que você escreve passa pela função `_transform()` e o resultado fica disponível para leitura.

O fluxo é unidirecional:

```
escrita (write) → _transform() → leitura (read)
```

Exemplos da biblioteca padrão: `zlib.createGzip()` comprime o que você escreve e disponibiliza os bytes comprimidos para leitura; `zlib.createGunzip()` faz o caminho inverso; `crypto.createCipheriv()` criptografa; parsers de protocolo convertem bytes em objetos.

---

## Por que importa

A confusão entre `Duplex` e `Transform` é uma das armadilhas mais comuns ao implementar streams customizadas.

Se você precisa de um canal bidirecional **onde os dois lados são independentes** (ex.: protocolo de comunicação, proxy, WebSocket), use `Duplex`.

Se você precisa de uma **transformação de dados** onde a entrada vira saída processada (ex.: compressão, cifragem, parsing, serialização), use `Transform`.

Usar `Duplex` quando você quer um `Transform` significa que você precisará manualmente pegar o que foi escrito e empurrar para o lado leitor — reinventando exatamente o que `Transform` já faz. O resultado é código mais complexo, mais frágil e sem backpressure correto.

> [!danger] Dois buffers ≠ fluxo conectado
> Em um `Duplex` puro, `this.push()` no lado leitor e os dados recebidos no lado escritor não têm relação automática. Em um `Transform`, `_transform()` é a ponte obrigatória — é ali que você chama `this.push()` para conectar os dois lados.

Outro motivo prático: `pipeline()` e `pipe()` tratam `Transform` de forma especial. Um `Transform` pode ser encadeado no meio de um pipeline como filtro ou conversor:

```
source → transform1 → transform2 → sink
```

Um `Duplex` puro no meio de um pipeline exigiria lógica manual para conectar os lados.

---

## Como funciona

### 1. Duplex com canais independentes — socket TCP

O exemplo mais direto de `Duplex` puro é um servidor TCP usando `net.createServer`. O socket retornado é um `Duplex`:

```javascript
import net from 'node:net';

const server = net.createServer((socket) => {
  // socket é um Duplex:
  // - socket (Readable): dados que chegam do cliente
  // - socket (Writable): dados que vão para o cliente

  console.log('Cliente conectado');

  // Leitura: consumindo o que o cliente enviou
  socket.on('data', (chunk) => {
    console.log('Recebido:', chunk.toString());
  });

  // Escrita: enviando uma resposta ao cliente
  // (os dois lados são completamente independentes)
  socket.write('Olá, cliente!\n');

  socket.on('end', () => {
    console.log('Cliente desconectou');
  });

  socket.on('error', (err) => {
    console.error('Erro no socket:', err.message);
  });
});

server.listen(3000, () => {
  console.log('Servidor ouvindo na porta 3000');
});
```

O que o servidor escreve no socket (`socket.write`) e o que ele lê do socket (`socket.on('data')`) são fluxos completamente diferentes. Não há transformação de um para o outro — são dois canais físicos distintos na mesma instância.

---

### 2. Transform básico — ToUpperCase

O caso mais simples de `Transform` customizado: converter texto para maiúsculas.

```javascript
import { Transform } from 'node:stream';

class ToUpperCase extends Transform {
  _transform(chunk, encoding, callback) {
    // chunk é um Buffer por padrão
    // toString() converte para string usando a encoding informada
    const upper = chunk.toString().toUpperCase();

    // push() envia o dado transformado para o lado Readable
    this.push(upper);

    // callback() sinaliza que este chunk foi processado
    // _transform() NÃO será chamado novamente até callback() ser invocado
    callback();
  }
}

// Uso direto
const upper = new ToUpperCase();

upper.on('data', (chunk) => {
  process.stdout.write(chunk);
});

upper.write('hello world\n'); // → "HELLO WORLD\n"
upper.write('streams são poderosas\n'); // → "STREAMS SÃO PODEROSAS\n"
upper.end();
```

A assinatura completa de `callback` permite propagar erros:

```javascript
_transform(chunk, encoding, callback) {
  try {
    const result = processarChunk(chunk);
    this.push(result);
    callback(); // sucesso
  } catch (err) {
    callback(err); // propaga o erro → emite evento 'error' no stream
  }
}
```

> [!warning] Esquecer `callback()` trava o stream
> Se `callback()` nunca for chamado, `_transform()` não será chamado para o próximo chunk. O stream fica suspenso sem erro visível — um dos bugs mais difíceis de diagnosticar.

---

### 3. `_flush` — emitindo o estado final

Parsers frequentemente acumulam estado interno entre chunks. Quando o stream encerra, pode restar dado no buffer interno que precisa ser emitido. É para isso que existe `_flush(callback)`.

`_flush` é chamado automaticamente pelo runtime quando o lado Writable recebe `.end()`, antes de o stream emitir `'finish'` e `'end'`.

```javascript
import { Transform } from 'node:stream';

class LineParser extends Transform {
  // Campo de instância: buffer para o fragmento da linha atual
  #buffer = '';

  _transform(chunk, encoding, callback) {
    // Acumula o novo chunk no buffer
    this.#buffer += chunk.toString();

    // Divide nas quebras de linha encontradas
    const lines = this.#buffer.split('\n');

    // O último elemento pode ser um fragmento incompleto —
    // guardamos para o próximo chunk (ou para _flush)
    this.#buffer = lines.pop() ?? '';

    // Emite todas as linhas completas
    for (const line of lines) {
      this.push(line + '\n');
    }

    callback();
  }

  _flush(callback) {
    // Ao final do stream, o que restou no buffer é a última linha
    // (que não terminou com '\n')
    if (this.#buffer) {
      this.push(this.#buffer);
    }
    callback();
  }
}

// Uso em pipeline
import { pipeline } from 'node:stream/promises';
import { createReadStream, createWriteStream } from 'node:fs';

await pipeline(
  createReadStream('./access.log'),
  new LineParser(),
  createWriteStream('./lines.txt')
);
```

> [!info] Por que `lines.pop()`?
> Após `split('\n')`, se o chunk termina com `\n`, o último elemento é uma string vazia `''`. Se não termina, é um fragmento de linha. Em ambos os casos, `pop()` remove esse elemento do array de linhas completas e o guarda no buffer — a lógica é a mesma.

---

### 4. Object mode em Transform — CSV para objetos

`Transform` em object mode permite trabalhar com objetos JavaScript em vez de `Buffer`/`string`. É o idioma canônico para processamento estruturado.

```javascript
import { Transform } from 'node:stream';

class CsvToJson extends Transform {
  #headers = null;
  #lineBuffer = '';

  constructor() {
    super({
      // readableObjectMode: a saída é um objeto JS
      // writableObjectMode: false (entrada ainda é texto)
      readableObjectMode: true,
    });
  }

  _transform(chunk, encoding, callback) {
    this.#lineBuffer += chunk.toString();
    const lines = this.#lineBuffer.split('\n');
    this.#lineBuffer = lines.pop() ?? '';

    for (const line of lines) {
      const trimmed = line.trim();
      if (!trimmed) continue;

      const values = trimmed.split(',');

      if (!this.#headers) {
        // Primeira linha: cabeçalho
        this.#headers = values;
      } else {
        // Linhas subsequentes: dados
        const obj = Object.fromEntries(
          this.#headers.map((key, i) => [key, values[i] ?? ''])
        );
        this.push(obj); // empurra um objeto, não um Buffer
      }
    }

    callback();
  }

  _flush(callback) {
    if (this.#lineBuffer.trim() && this.#headers) {
      const values = this.#lineBuffer.split(',');
      const obj = Object.fromEntries(
        this.#headers.map((key, i) => [key, values[i] ?? ''])
      );
      this.push(obj);
    }
    callback();
  }
}

// Uso: parsear CSV e processar cada objeto
import { createReadStream } from 'node:fs';
import { pipeline } from 'node:stream/promises';
import { Writable } from 'node:stream';

const printer = new Writable({
  objectMode: true,
  write(obj, enc, cb) {
    console.log(obj);
    cb();
  },
});

await pipeline(
  createReadStream('./dados.csv'),
  new CsvToJson(),
  printer
);
```

> [!tip] `readableObjectMode` vs `objectMode`
> `objectMode: true` ativa object mode nos dois lados (Readable e Writable). `readableObjectMode: true` só ativa no lado de saída — útil para parsers que recebem bytes e emitem objetos, como o `CsvToJson` acima.

---

## Na prática

### Transforms compostos em pipeline

O idioma mais comum em código de produção é encadear vários `Transform` em `pipeline()`:

```javascript
import { pipeline } from 'node:stream/promises';
import { createReadStream, createWriteStream } from 'node:fs';
import { createGzip } from 'node:zlib';

await pipeline(
  createReadStream('./grande-arquivo.csv'),   // Readable
  new LineParser(),                           // Transform: bytes → linhas
  new CsvToJson(),                            // Transform: linhas → objetos
  new FiltroDeRegistros(),                    // Transform: filtra por critério
  new JsonStringify(),                        // Transform: objetos → JSON strings
  createGzip(),                               // Transform: comprime
  createWriteStream('./saida.json.gz')        // Writable
);
```

Cada `Transform` no pipeline recebe o output do anterior, processa e emite para o próximo. O backpressure é propagado automaticamente pelo `pipeline()` — se o Writable final está cheio, a pressão sobe até o Readable de origem pausar.

### `_flush` é obrigatório em parsers

Qualquer `Transform` que acumule estado interno entre chunks precisa de `_flush`. A regra prática:

- Tem `#buffer` ou variável de acumulação? Precisa de `_flush`.
- Emite dados em grupos maiores que chunks individuais (ex.: linhas, objetos JSON completos)? Precisa de `_flush`.
- É puramente stateless (transforma chunk por chunk sem acumular)? `_flush` é opcional.

### Object mode + Transform = processamento estruturado

O par `Transform` em object mode + `pipeline()` é o idioma Node.js para processar dados estruturados de forma eficiente em memória. Em vez de carregar o arquivo inteiro em RAM e processar com `JSON.parse` ou `csv-parse` de forma síncrona, você processa chunk a chunk, mantendo uso de memória constante independentemente do tamanho do input.

---

## Armadilhas

### 1. Esquecer `_flush` em parsers — último chunk perdido

```javascript
// ERRADO: sem _flush, a última linha pode nunca ser emitida
class LineParser extends Transform {
  #buffer = '';

  _transform(chunk, enc, cb) {
    this.#buffer += chunk.toString();
    const lines = this.#buffer.split('\n');
    this.#buffer = lines.pop() ?? '';
    for (const line of lines) this.push(line + '\n');
    cb();
  }
  // _flush ausente → this.#buffer com conteúdo residual é descartado
}
```

Resultado: o arquivo tem 1000 linhas, o parser emite 999. O bug só aparece se a última linha não terminar com `\n` — comum em arquivos gerados por ferramentas que não adicionam newline final.

### 2. `callback(error)` esquecido — erros silenciosos

```javascript
// ERRADO: erro capturado mas não propagado
_transform(chunk, enc, cb) {
  try {
    this.push(transformar(chunk));
    cb();
  } catch (err) {
    console.error(err); // logou, mas não propagou
    cb(); // stream continua como se nada tivesse acontecido
    // CORRETO: cb(err) → emite 'error' → pipeline() rejeita a Promise
  }
}
```

### 3. Chamar `cb()` antes de `this.push()` — comportamento inesperado

```javascript
// PROBLEMÁTICO: cb() sinaliza que o próximo chunk pode vir
// antes de push() ter sido chamado
_transform(chunk, enc, cb) {
  cb(); // libera o próximo chunk imediatamente
  this.push(transformar(chunk)); // push depois do cb — pode gerar race condition
}

// CORRETO: sempre push() antes de cb()
_transform(chunk, enc, cb) {
  this.push(transformar(chunk));
  cb();
}
```

Em alguns cenários com streams de alta velocidade, chamar `cb()` antes de `this.push()` pode fazer o runtime solicitar o próximo chunk antes do atual ter sido completamente processado, gerando resultados fora de ordem.

### 4. Confundir Duplex com Transform na implementação

```javascript
// ERRADO: implementando lógica de Transform em um Duplex puro
class MeuProcessador extends Duplex {
  _write(chunk, enc, cb) {
    // Tentando "conectar" manualmente os dois lados — frágil e incorreto
    const resultado = processar(chunk);
    this.push(resultado);
    cb();
  }
  _read() {}
}

// CORRETO: se a saída é derivada da entrada via transformação, use Transform
class MeuProcessador extends Transform {
  _transform(chunk, enc, cb) {
    const resultado = processar(chunk);
    this.push(resultado);
    cb();
  }
}
```

`Transform` já implementa `_write` internamente de forma que chama `_transform` no momento certo. Reimplementar essa lógica em `Duplex` é reinventar a roda — e geralmente errado.

### 5. `highWaterMark` em object mode — a unidade muda

Em byte mode, `highWaterMark` é em bytes (padrão: 16 KB). Em object mode, é em número de objetos (padrão: 16). Um `Transform` em object mode com `highWaterMark: 1` processa um objeto por vez — útil para operações lentas (ex.: I/O assíncrono por registro), mas pode ser gargalo em operações rápidas.

---

## Em entrevista

> [!quote] Frase pronta
> "Duplex and Transform both implement read and write, but they're conceptually different. Duplex has **two independent channels** — the canonical example is a TCP socket where you read from the peer and write to the peer through separate logical buffers. Transform is a Duplex where what you write feeds the read side after a transformation — `zlib.createGzip()` is the classic example. To implement a custom Transform, you subclass and define `_transform(chunk, encoding, callback)`, optionally `_flush(callback)` to emit any remaining state at end."

### Perguntas frequentes

**"Quando você usaria Duplex vs Transform?"**

Duplex quando os dois sentidos são **logicamente independentes** — comunicação bidirecional, proxies, WebSockets. Transform quando a saída é **derivada** da entrada por alguma operação — compressão, cifragem, parsing, serialização.

**"O que acontece se você não chamar `callback()` em `_transform`?"**

O stream fica suspenso. O runtime não chamará `_transform` para o próximo chunk até o callback do chunk atual ser invocado. Sem erro, sem deadlock aparente — simplesmente para de processar.

**"Por que `_flush` existe?"**

Porque `_transform` é chamado por chunk, mas muitos processamentos acumulam estado entre chunks (ex.: um parser de linha que espera `\n`). Quando o stream encerra, pode restar dado no buffer interno. `_flush` é a oportunidade de emitir esse dado residual antes de o stream fechar.

**"Como object mode muda o comportamento de Transform?"**

Em byte mode, chunks são `Buffer`. Em object mode, chunks podem ser qualquer valor JavaScript. O `highWaterMark` muda de bytes para número de objetos. Isso permite encadear parsers que emitem objetos diretamente, sem serializar e deserializar entre stages do pipeline.

### Vocabulário para entrevistas em inglês

| PT-BR | EN |
|-------|-----|
| canal duplo | duplex channel |
| fluxo encadeado | chained flow / piped stream |
| transformação | transformation |
| descarga final | flush |
| modo objeto | object mode |
| fragmento residual | trailing chunk / leftover buffer |
| backpressure em pipeline | pipeline backpressure |
| estado acumulado | accumulated state |

---

## Veja também

- `[[02 - Os 4 tipos - Readable, Writable, Duplex, Transform]]` — visão geral comparativa dos quatro tipos
- `[[03 - Readable streams]]` — como funciona o lado leitor
- `[[04 - Writable streams]]` — como funciona o lado escritor
- `[[06 - Backpressure]]` — o mecanismo de controle de fluxo que Transform propaga automaticamente
- `[[10 - Padrões práticos]]` — pipelines compostos com múltiplos Transforms
- `[[Node.js]]` — tronco do domínio Node.js

---

## Fontes

- [Node.js Docs — Class: stream.Duplex](https://nodejs.org/api/stream.html#class-streamduplex)
- [Node.js Docs — Class: stream.Transform](https://nodejs.org/api/stream.html#class-streamtransform)
