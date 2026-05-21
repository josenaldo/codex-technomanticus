---
title: "Por que streams"
created: 2026-05-08
updated: 2026-05-08
type: concept
status: seedling
publish: true
tags:
  - node
  - streams
  - mental-model
aliases:
  - Quando usar streams
  - Streams motivação
---

# Por que streams

> [!abstract] TL;DR
> Streams são a abstração do Node para processar dados em chunks sem carregar tudo em memória. Use quando o payload é grande (>100 MB), o throughput é sustentado, ou backpressure precisa ser respeitado. Alternativas mais simples (buffer everything, paginação) ganham em casos pequenos; streams ganham em casos grandes ou de longa duração.

---

## O que é

Um stream é uma sequência de chunks que pode ser produzida ou consumida incrementalmente — sem materializar o conjunto completo de dados de uma só vez.

A metáfora útil: ler um livro página a página em vez de memorizá-lo inteiro antes de começar. O conteúdo existe em ordem, mas apenas uma parte precisa estar "em mãos" a qualquer momento.

Node.js expõe quatro tipos de stream nativos (detalhados na nota 02):

| Tipo | Papel | Exemplo |
|---|---|---|
| **Readable** | Fonte de dados — produz chunks | `fs.createReadStream`, `req` HTTP |
| **Writable** | Destino de dados — consome chunks | `fs.createWriteStream`, `res` HTTP |
| **Duplex** | Lê e escreve de forma independente | `net.Socket`, conexão TCP |
| **Transform** | Lê, transforma, e escreve | `zlib.createGzip`, `crypto.createCipheriv` |

A diferença fundamental em relação a um array completo:

| Dimensão | Array / Buffer completo | Stream |
|---|---|---|
| Uso de memória | O(N) — cresce com os dados | O(chunkSize) — constante |
| Primeiro output | Após carregar tudo | Após receber o primeiro chunk |
| Composição | Encadeia operações sobre coleções | Encadeia transformações sobre o fluxo |
| Backpressure | Inexistente | Nativo — produtor pode ser pausado |

---

## Por que importa

O problema concreto surge em três cenários frequentes em servidores de produção.

**Upload ou download de arquivos grandes.** Um endpoint que recebe um arquivo de 5 GB e faz `const data = await readFile(path)` antes de processar precisa de pelo menos 5 GB de heap disponível — por requisição. Com 3 requisições simultâneas, são 15 GB. A heap do processo Node tem limite configurável, mas nenhum servidor sobrevive a esse padrão sob carga.

**Pipelines de transformação de dados.** Um job que processa um CSV de 2 milhões de linhas: se a lógica carrega todas as linhas antes de começar a processar, a latência do primeiro output é proporcional ao tamanho total do arquivo. Com streaming, o primeiro registro pode ser escrito na saída antes que 1% do arquivo seja lido.

**Streaming de respostas longas.** Respostas SSE (Server-Sent Events) e respostas de LLMs chegam em partes ao longo de segundos. Se o servidor faz buffer da resposta completa antes de repassar ao cliente, o usuário espera sem ver progresso — a UX quebra. Com streaming, cada chunk é encaminhado assim que chega.

O event loop é o elo de ligação aqui. Como visto em [[10 - Bloqueio do event loop - sintomas e causas]], carregar um payload gigante com `JSON.parse` ou `readFileSync` é uma das causas canônicas de bloqueio da thread JavaScript. Streams evitam esse bloqueio ao não forçar a materialização completa dos dados na thread principal.

O ponto sutil: o problema não é apenas memória — é a **combinação de memória e thread**. Um `readFile` de 500 MB bloqueia porque:
1. Reserva 500 MB de heap de uma vez
2. A desserialização subsequente (`JSON.parse` de payload grande) bloqueia a thread JS por centenas de milissegundos

Com stream, cada chunk chega de forma assíncrona, é processado, e é descartado. A thread JS nunca segura mais do que um chunk de cada vez.

---

## Como funciona

### Buffer everything vs. stream — comparação direta

**Abordagem buffer everything:**

```javascript
import { readFile, writeFile } from 'node:fs/promises';
import { parse } from 'csv-parse/sync';

// ❌ Carrega o arquivo inteiro antes de processar qualquer linha
const raw = await readFile('registros.csv');          // O(N) memória
const rows = parse(raw, { columns: true });           // O(N) memória adicional
const result = rows.map(transformarRegistro);         // O(N) memória adicional
await writeFile('saida.json', JSON.stringify(result));// O(N) memória adicional

// Pico de memória: aproximadamente 4× o tamanho do CSV
```

**Abordagem stream:**

```javascript
import { createReadStream, createWriteStream } from 'node:fs';
import { pipeline } from 'node:stream/promises';
import { parse } from 'csv-parse';
import { stringify } from 'ndjson';

// ✅ Processa chunk a chunk — memória constante independente do tamanho
await pipeline(
  createReadStream('registros.csv'),
  parse({ columns: true }),
  new Transform({
    objectMode: true,
    transform(row, _enc, cb) { cb(null, transformarRegistro(row)); },
  }),
  stringify(),
  createWriteStream('saida.ndjson'),
);

// Pico de memória: O(chunkSize) — independente do tamanho total do arquivo
```

O crescimento de memória com buffer everything é linear no tamanho dos dados. Com stream, o buffer interno tem tamanho fixo (controlado por `highWaterMark`). A função `pipeline` da `node:stream/promises` também cuida de propagação de erros e cleanup automático — mais sobre isso na nota 07.

### Diagrama mental do fluxo

```
Buffer everything:
  Fonte ──────────────────────────────────► Memória (N bytes) ──► Consumidor
         espera carregar tudo antes de prosseguir

Stream:
  Fonte ──► [chunk 1] ──► Transform ──► [chunk 1'] ──► Consumidor
         ──► [chunk 2] ──► Transform ──► [chunk 2'] ──► Consumidor
         ──► [chunk 3] ──► Transform ──► [chunk 3'] ──► Consumidor
         Pipeline fluindo continuamente — memória = O(buffer interno)
```

### Backpressure — o mecanismo que controla o fluxo

Backpressure é o mecanismo pelo qual um consumidor lento sinaliza ao produtor para reduzir a velocidade. Sem backpressure, um produtor rápido (leitura de disco em NVMe) conectado a um consumidor lento (escrita em rede com latência alta) encheria o buffer interno até o heap explodir.

```javascript
// Sem backpressure — produtor ignora a pressão do consumidor
const readable = createReadStream('grande.bin');
const writable = createWriteStream('/dev/null');

readable.on('data', (chunk) => {
  // ❌ Se writable.write() retornar false (buffer cheio), ignoramos
  writable.write(chunk);
});

// Com backpressure respeitado — via pipeline (forma correta)
await pipeline(
  createReadStream('grande.bin'),
  createWriteStream('/dev/null'),
);
// pipeline pausa o readable automaticamente quando o writable está cheio
```

A conexão com o galho 2 (Paralelismo) surge aqui: quando dados precisam ser transferidos entre Worker Threads via `postMessage`, a alternativa é usar `transferList` com `ArrayBuffer` para zero-copy. Quando os dados fluem entre processos ou entre rede e disco, streams são o mecanismo correto — cada um evita cópias desnecessárias em seu contexto. Ver [[04 - Comunicação entre workers - postMessage e MessageChannel]].

### highWaterMark — controlando o buffer interno

Cada stream tem um buffer interno cujo tamanho máximo é controlado por `highWaterMark`. Para streams em modo bytes (padrão), o valor é em bytes (padrão: 16 KB). Para streams em modo objeto (`objectMode: true`), o valor é em número de objetos (padrão: 16).

```javascript
import { createReadStream } from 'node:fs';

// highWaterMark de 64 KB — chunks maiores, menos chamadas de sistema
const readable = createReadStream('grande.csv', { highWaterMark: 64 * 1024 });

// Para streams de objetos (ex.: parsing de CSV linha a linha)
const { Transform } = require('node:stream');
const parser = new Transform({
  objectMode: true,
  highWaterMark: 100, // máximo de 100 objetos no buffer interno
  transform(chunk, _enc, cb) { /* ... */ cb(null, parsed); },
});
```

`highWaterMark` não é um limite rígido — é o threshold após o qual `write()` retorna `false` (sinalizando ao produtor para pausar). Aumentar `highWaterMark` melhora o throughput mas aumenta o uso de memória; diminuir reduz a memória mas pode aumentar a latência por pausas mais frequentes. Para a maioria dos casos, o valor padrão (16 KB) é adequado.

---

## Na prática

### Quando usar streams

- Arquivos ou payloads maiores que ~100 MB
- Throughput sustentado em servidor sob carga (uploads, downloads, transformações contínuas)
- Respostas cujo primeiro chunk precisa ser entregue ao cliente antes do final (SSE, LLM, progress)
- Composição de múltiplas transformações sequenciais (parse → filter → transform → serialize)
- Qualquer situação onde o tamanho total dos dados é desconhecido em tempo de execução

### Quando NÃO usar streams

| Situação | Alternativa adequada | Motivo |
|---|---|---|
| Payload < 10 MB | `readFile` + processamento síncrono | Overhead de stream > benefício; mais simples |
| Operação que precisa ver todos os dados de uma vez | Buffer completo | Sort global, dedup global, join de datasets |
| Latência ponta-a-ponta importa mais que throughput | Buffer + paginação | Stream tem latência de primeira resposta similar ao buffer |
| Uma única transformação simples sobre dados pequenos | Buffer + array methods | `.map`, `.filter`, `.reduce` são mais legíveis e suficientes |
| Dados JSON estruturados sem volume extremo | `JSON.parse` direta | O custo de parsing é desprezível abaixo de ~5 MB |

A decisão não é "streams são sempre melhores". É "streams trocam complexidade por eficiência de memória e throughput". Para datasets pequenos, a complexidade não se paga.

### Exemplo completo: upload de arquivo grande

```javascript
import { createServer } from 'node:http';
import { createWriteStream } from 'node:fs';
import { pipeline } from 'node:stream/promises';
import { createGunzip } from 'node:zlib';

// ✅ Recebe upload, descomprime, salva — sem carregar tudo em memória
createServer(async (req, res) => {
  if (req.method !== 'POST') return res.end();

  try {
    await pipeline(
      req,              // Readable: stream do body HTTP
      createGunzip(),   // Transform: descomprime gzip on-the-fly
      createWriteStream('/tmp/upload.dat'), // Writable: salva no disco
    );
    res.writeHead(200);
    res.end(JSON.stringify({ ok: true }));
  } catch (err) {
    // pipeline propaga erros e faz cleanup de todos os estágios
    res.writeHead(500);
    res.end(JSON.stringify({ error: err.message }));
  }
}).listen(3000);
```

Neste padrão, um upload de 5 GB usa apenas ~16 KB de heap por chunk — independente do tamanho total. O mesmo servidor pode lidar com múltiplos uploads simultâneos sem explodir a memória.

---

## Armadilhas

**1. Usar stream em payload pequeno — overhead sem benefício.**

Stream adiciona indireção: criação de objetos, eventos, tratamento de backpressure, propagação de erros. Para arquivos de 50 KB ou payloads de API típicos, esse overhead é mensurável e não compensa. A heurística: abaixo de 10 MB e sem requisito de latência de primeiro chunk, buffer é mais simples e igualmente eficiente.

**2. Confundir "streaming HTTP" com "Node Streams".**

Quando uma resposta HTTP chega em chunks via Transfer-Encoding chunked ou SSE, isso é streaming no protocolo. Node Streams são a abstração do runtime para processar esses (e outros) dados. Os dois se relacionam — `req` e `res` são Node Streams — mas não são a mesma coisa. É possível consumir uma resposta HTTP em streaming sem usar a API `stream` explicitamente (usando `fetch` com `response.body`), e é possível usar Node Streams sem envolver HTTP (arquivos, stdin/stdout).

**3. Achar que stream resolve memória, mas ignorar backpressure.**

O argumento de "memória constante" assume que o produtor e o consumidor operam em velocidades compatíveis ou que backpressure está sendo respeitado. Se um Readable drena disco em NVMe mas o Writable é uma conexão de rede lenta, e backpressure é ignorado, o buffer interno do Writable cresce indefinidamente — a memória explode mesmo com stream. A conclusão errada seria "streams não ajudam com memória". A conclusão correta: streams ajudam, mas apenas quando backpressure está implementado. `pipeline` implementa backpressure automaticamente; `pipe` faz o mesmo mas tem semântica de erro fraca; conectar manualmente com eventos `data` exige cuidado explícito.

**4. Usar `stream.pipe()` em código novo.**

`pipe` não propaga erros corretamente entre estágios e não destrói streams upstream quando um downstream falha — o que leva a leaks de file descriptors. `pipeline` (da `node:stream/promises`) substitui `pipe` em todos os casos de produção. Mais detalhes na nota 07.

---

## Em entrevista

> [!tip] Frase pronta (EN)
> "Node Streams are the canonical way to process data in chunks without loading everything into memory. The motivation is concrete: large file processing, sustained throughput on a server, and respecting backpressure between fast producers and slow consumers. They're not always the right answer — for small payloads, the overhead exceeds the benefit, and for operations that need a global view of the data, you need the full buffer anyway. The signal that you should reach for streams is when memory or latency under load is the bottleneck."

### Vocabulário técnico

| PT-BR | EN |
|---|---|
| chunk | chunk |
| throughput | throughput |
| backpressure | backpressure |
| produtor / consumidor | producer / consumer |
| latência | latency |
| buffer interno | internal buffer |
| alto nível d'água | high-water mark |
| fluxo de dados | data flow |
| pipeline de transformação | transformation pipeline |

### Perguntas frequentes em entrevista

**"Qual a diferença entre stream e buffer em Node?"**
Buffer carrega todos os dados em memória antes de qualquer processamento — uso de memória O(N). Stream entrega dados em chunks incrementais — uso de memória O(chunkSize). A diferença é relevante para payloads grandes; para dados pequenos, ambos têm desempenho equivalente.

**"Quando streams não são a resposta certa?"**
Quando o payload é pequeno (overhead de stream não se paga), quando a operação exige visão global dos dados (sort, dedup, join), ou quando a latência de entrega do primeiro chunk não é um requisito — nesse caso, buffer com paginação pode ter latência total menor com menor complexidade.

**"O que é backpressure e por que importa?"**
Backpressure é o mecanismo pelo qual um consumidor lento sinaliza ao produtor para pausar. Sem ele, um produtor rápido enche o buffer interno do consumidor até o heap estourar. `pipeline` gerencia backpressure automaticamente; `pipe` faz o mesmo; conectar streams manualmente via eventos `data` exige implementar backpressure explicitamente via `readable.pause()` / `readable.resume()`.

---

## Veja também

- [[02 - Os 4 tipos - Readable, Writable, Duplex, Transform]]
- [[06 - Backpressure]]
- [[07 - pipeline vs pipe - error handling]]
- [[03-Dominios/Node/Runtime e Event Loop/index]] — galho 1
- [[10 - Bloqueio do event loop - sintomas e causas]] — galho 1: buffer de payload gigante como causa de bloqueio
- [[03-Dominios/Node/Paralelismo/index]] — galho 2
- [[04 - Comunicação entre workers - postMessage e MessageChannel]] — galho 2: transferList como alternativa a streams para Worker Threads
- [[Node.js]] — tronco
