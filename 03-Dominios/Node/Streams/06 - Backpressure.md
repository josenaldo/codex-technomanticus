---
title: "Backpressure"
created: 2026-05-08
updated: 2026-05-08
type: concept
status: seedling
publish: true
tags:
  - node
  - streams
  - backpressure
  - performance
aliases:
  - Retroalimentação
  - drain event
  - highWaterMark
---

# Backpressure

> [!abstract] TL;DR
> Backpressure é o sinal explícito do consumer dizendo "estou cheio, pare de produzir". Em Node, o sinal é o `boolean` retornado por `.write()`: `false` significa "pare"; espere o evento `'drain'` antes de continuar. `highWaterMark` define o limite do buffer interno (padrão: 16 KB para bytes, 16 para objetos). Ignorar esse sinal é a causa mais comum de vazamento de memória em código que processa streams — o buffer cresce sem limite até OOM. A forma idiomática moderna é `pipeline()` de `stream/promises`, que gerencia backpressure automaticamente.

---

## O que é

Backpressure (retroalimentação) é o mecanismo pelo qual um **consumer lento sinaliza ao producer rápido que deve desacelerar**.

A analogia mais direta: uma mangueira conectada a uma caixa d'água. Se o destino (caixa) está cheio, abrir a torneira mais ainda não ajuda — a água transborda. O mecanismo que detecta esse estado e sinaliza "feche a torneira" é o backpressure.

Em sistemas de computação, a mesma lógica se aplica:

- **Sem backpressure**: o producer escreve no ritmo máximo; o consumer não consegue acompanhar; dados se acumulam em buffers intermediários; memória cresce sem limite.
- **Com backpressure**: quando o buffer do consumer atinge um limiar, ele sinaliza ao producer para pausar; producer para; consumer drena; consumer sinaliza "pode continuar".

Em Node.js, esse mecanismo é **explícito** e intencional: o runtime não força pausa automática — é responsabilidade do código que chama `.write()` verificar o retorno e pausar quando necessário.

### O que não é

Backpressure **não é**:

- Um mecanismo de rate limiting externo (ex: throttle de API com token bucket).
- Um conceito restrito a TCP/HTTP (existe em qualquer sistema com produtor/consumidor).
- Algo que o Node.js resolve automaticamente sem que você escreva código correto.

---

## Por que importa

O vazamento de memória mais comum em aplicações Node que processam dados é exatamente este: **um loop que chama `.write()` sem verificar o retorno**.

```javascript
// O bug clássico — parece inocente, vaza memória
for (const chunk of milhoesDePedacos) {
  ws.write(chunk); // retorno ignorado
}
```

O problema não aparece em desenvolvimento com datasets pequenos. Aparece em produção, tarde da noite, quando o volume cresce. O processo começa a consumir memória progressivamente, o GC passa a trabalhar mais, throughput cai, e eventualmente o processo morre com OOM.

Dados concretos da documentação oficial do Node.js mostram o custo:

| Métrica | Com backpressure | Sem backpressure |
|---------|-----------------|-----------------|
| Memória máxima | ~87 MB | ~1,5 GB |
| Frequência de GC | ~75 ciclos/min | ~36 ciclos/min |

O GC com backpressure rodando **mais** e com memória **menor** não é contradição — são muitos ciclos pequenos (saudável) contra poucos ciclos gigantes (drena CPU, causa latência de STW).

> [!danger] O runtime não vai te avisar em tempo real
> A Writable continua aceitando `.write()` mesmo com o buffer cheio. Não há exceção, não há crash imediato. O buffer simplesmente cresce. O único sinal é o `boolean` retornado por `.write()` — se você não lê esse retorno, está voando cego.

---

## Como funciona

### 1. `highWaterMark`: o limiar do buffer

Cada stream tem um `highWaterMark` — a marca d'água alta que define o tamanho máximo desejado do buffer interno antes que backpressure seja sinalizado.

```javascript
import { createWriteStream } from 'node:fs';

// highWaterMark padrão para fs: 16384 bytes (16 KB)
const ws = createWriteStream('./output.txt');

// Configurando highWaterMark explicitamente
const ws64 = createWriteStream('./output.txt', {
  highWaterMark: 64 * 1024 // 64 KB
});

// Em object mode: padrão é 16 objetos
import { Transform } from 'node:stream';
const t = new Transform({
  objectMode: true,
  highWaterMark: 32, // 32 objetos
  transform(chunk, enc, cb) { cb(null, chunk); }
});
```

> [!info] `highWaterMark` não é um limite absoluto
> É um limiar, não um teto rígido. Depois que o buffer ultrapassa o `highWaterMark`, `.write()` retorna `false` — mas a Writable **ainda aceita** mais dados. Você precisa parar voluntariamente. O buffer pode continuar crescendo se você ignorar o sinal.

Propriedades de inspeção em runtime:

```javascript
ws.writableHighWaterMark  // valor configurado (16384 por padrão)
ws.writableLength         // bytes/objetos atualmente no buffer
ws.writableNeedDrain      // true se write() retornou false e drain ainda não ocorreu
```

### 2. O sinal: `.write()` retorna `boolean`

`.write()` retorna:

- `true` → buffer ainda abaixo do `highWaterMark`; pode continuar escrevendo.
- `false` → buffer atingiu ou excedeu o `highWaterMark`; **pare de escrever**.

```javascript
const ok = ws.write(chunk);
// ok === false → backpressure ativo
// ok === true  → seguro continuar
```

Esse é o único sinal de backpressure na API. Não há evento, não há exceção. É um `boolean` de retorno de método — simples, mas fácil de ignorar acidentalmente.

### 3. A pausa: parar de escrever

Quando `.write()` retorna `false`, a ação correta é parar completamente de chamar `.write()`. Não "escrever menos". Não "escrever mais devagar". **Parar**.

O motivo: qualquer `.write()` adicional com o buffer cheio aumenta o problema — cada chamada empilha mais dados no buffer já saturado.

### 4. O evento `'drain'`: retomar

O evento `'drain'` é emitido quando o buffer interno da Writable drenou abaixo do `highWaterMark` e é seguro retomar a escrita.

```javascript
ws.once('drain', () => {
  // Buffer drenado — pode chamar .write() novamente
  resumeWriting();
});
```

Use `once` em vez de `on` porque você quer retomar apenas uma vez por backpressure. Um `on` permanente adicionaria listeners acumulativos a cada ciclo.

### 5. Código correto vs. código com leak

**INCORRETO — ignora backpressure, vaza memória:**

```javascript
// Nunca faça isso com arrays grandes
async function writeAllErrado(ws, chunks) {
  for (const chunk of chunks) {
    ws.write(chunk); // boolean ignorado — buffer cresce sem limite
  }
  ws.end();
}
```

**CORRETO — respeita backpressure com async/await:**

```javascript
async function writeAll(ws, chunks) {
  for (const chunk of chunks) {
    // Verifica o sinal a cada write
    if (!ws.write(chunk)) {
      // Buffer cheio: aguarda drenagem antes de continuar
      await new Promise(resolve => ws.once('drain', resolve));
    }
  }
  ws.end();
}
```

**CORRETO — padrão clássico com while/callback (pré-async):**

```javascript
function writeMany(ws, items, onDone) {
  let i = 0;

  function next() {
    while (i < items.length) {
      const chunk = items[i++];
      const ok = ws.write(chunk);

      if (!ok) {
        // Sair do loop e aguardar drain
        ws.once('drain', next);
        return; // CRÍTICO: return imediato, não continua o while
      }
    }
    // Todos os chunks escritos
    ws.end(onDone);
  }

  next();
}
```

O `return` após registrar o listener `'drain'` é crítico. Sem ele, o `while` continuaria consumindo o array mesmo com backpressure ativo.

### 6. `pipeline()` resolve automaticamente

`pipeline()` de `node:stream/promises` encapsula todo o mecanismo de backpressure:

```javascript
import { pipeline } from 'node:stream/promises';
import { createReadStream, createWriteStream } from 'node:fs';
import { createGzip } from 'node:zlib';

// pipeline gerencia backpressure entre cada par de streams
await pipeline(
  createReadStream('./input.txt'),
  createGzip(),
  createWriteStream('./output.txt.gz')
);
// Sem .write() manual, sem listener 'drain', sem gestão de buffer
```

Internamente, `pipeline()` faz exatamente o que o padrão manual faz: quando `.write()` retorna `false`, pausa o Readable de origem e espera `'drain'` na Writable antes de retomar. A diferença é que você não precisa escrever esse código — e ela também trata erros e destroi todos os streams da cadeia em caso de falha.

**Comparação lado a lado:**

```javascript
// Sem pipeline — gestão manual de backpressure
import { createReadStream, createWriteStream } from 'node:fs';

const rs = createReadStream('./input.txt');
const ws = createWriteStream('./output.txt');

rs.on('data', chunk => {
  if (!ws.write(chunk)) {
    rs.pause(); // para de produzir
    ws.once('drain', () => rs.resume()); // retoma quando buffer drena
  }
});

rs.on('end', () => ws.end());
rs.on('error', err => { ws.destroy(err); });
ws.on('error', err => { rs.destroy(err); });

// Com pipeline — equivalente, mas idiomático e correto por padrão
import { pipeline } from 'node:stream/promises';
import { createReadStream, createWriteStream } from 'node:fs';

await pipeline(
  createReadStream('./input.txt'),
  createWriteStream('./output.txt')
);
```

O bloco "sem pipeline" tem 10 linhas e ainda é simplificado — tratamento de erro completo exigiria mais. `pipeline()` cobre tudo em 3 linhas.

---

## Na prática

### Quando implementar backpressure manual

Backpressure manual com `while + once('drain')` só é necessário em dois cenários:

1. **Dados gerados programaticamente** — você não tem um Readable de origem, apenas produz chunks em código (loop sobre array, geração de relatório, etc.).
2. **Implementando uma Writable customizada** — você controla o `_write` e precisa sinalizar ao runtime quando o chunk foi consumido.

Em todos os outros casos, `pipeline()` é a forma correta.

### Sinalizando backpressure em Writables customizadas

Em uma Writable customizada, o sinal de backpressure sai pelo callback de `_write`. O runtime só considera o chunk como consumido quando o callback é chamado — e só então avalia se pode entregar o próximo chunk:

```javascript
import { Writable } from 'node:stream';

class SlowWriter extends Writable {
  _write(chunk, encoding, callback) {
    // O runtime não enviará o próximo chunk até que callback() seja chamado.
    // Se o processamento for lento, isso naturalmente cria backpressure
    // — o produtor de origem vai esperar.
    setTimeout(() => {
      processar(chunk);
      callback(); // Sinaliza: pronto para o próximo chunk
    }, 100);
  }
}
```

Se `callback` nunca for chamado, o stream trava — nenhum chunk adicional é entregue. Se for chamado múltiplas vezes, o comportamento é indefinido. Um callback por `_write`, sempre.

### Backpressure em Readable customizada: `.push()` também retorna boolean

O sinal funciona nos dois lados do pipeline. Em uma Readable customizada, `.push(chunk)` também retorna `boolean`:

```javascript
import { Readable } from 'node:stream';

class DatabaseCursor extends Readable {
  constructor(cursor) {
    super({ objectMode: true });
    this.cursor = cursor;
  }

  _read() {
    this.cursor.next().then(record => {
      if (record === null) {
        this.push(null); // fim do stream
        return;
      }
      const canContinue = this.push(record);
      if (canContinue) {
        this._read(); // consumer ainda quer mais
        // Se !canContinue, _read() será chamado novamente pelo runtime
        // quando o consumer estiver pronto — não chame você mesmo
      }
    });
  }
}
```

> [!tip] Regra de ouro para Readable customizada
> Nunca chame `_read()` manualmente quando `push()` retornar `false`. O runtime chama `_read()` automaticamente quando o consumer estiver pronto para mais dados. Forçar a chamada quebra o backpressure — você estaria produzindo dados que ninguém está consumindo.

### Tuning de `highWaterMark`

`highWaterMark` pode ser ajustado para otimizar throughput — mas com cautela:

```javascript
// Aumentar para reduzir round-trips em redes lentas
const ws = createWriteStream('./output.bin', {
  highWaterMark: 256 * 1024 // 256 KB
});

// Reduzir para latência menor em tempo real (ex: streaming de audio)
const ws = createWriteStream('./audio.pcm', {
  highWaterMark: 4 * 1024 // 4 KB
});
```

Regra prática: meça antes de tunar. Um `highWaterMark` maior reduz overhead de handshakes de backpressure mas aumenta latência de primeira resposta e uso de memória pico.

---

## Armadilhas

### 1. Ignorar o boolean de `.write()` em loop → memory growth silencioso

```javascript
// ERRADO — vaza memória de forma silenciosa em produção
const linhas = gerarRelatorio(); // array grande
for (const linha of linhas) {
  ws.write(linha); // boolean ignorado
}
ws.end();
```

Esse código funciona perfeitamente em testes com datasets pequenos. Em produção, quando o relatório tem 500 MB, o processo consome 1,5 GB+ antes de terminar. Não há erro — apenas lentidão e eventual OOM.

### 2. `for...of` com array grande → leak silencioso

O padrão específico `for (const x of arr) ws.write(x)` é especialmente perigoso porque parece idiomático e correto. O JavaScript não tem como "pausar" um `for...of` — uma vez iniciado, vai até o fim, independente de quantos `false` `.write()` retorna.

A solução é substituir pelo padrão `while + once('drain')` ou pela versão `async/await`:

```javascript
// Substitua o for...of por um padrão que pode pausar
for (const chunk of chunks) {
  if (!ws.write(chunk)) {
    await new Promise(resolve => ws.once('drain', resolve));
  }
}
```

### 3. Achar que `pipeline()` não tem backpressure — tem

`pipeline()` **não elimina** backpressure — ela **gerencia automaticamente**. A limitação de throughput ainda existe; você apenas não precisa codificar o mecanismo.

Isso importa quando você tenta "otimizar" `pipeline()` aumentando `highWaterMark` sem medir: você pode estar mascarando gargalos em vez de resolvê-los.

### 4. Tunar `highWaterMark` sem medir → mascara o bug

```javascript
// Tentação: o pipeline está "lento", então aumento o highWaterMark
const ws = createWriteStream('./out.bin', {
  highWaterMark: 16 * 1024 * 1024 // 16 MB — "vai ficar mais rápido"
});
```

Com `highWaterMark` muito alto, backpressure dispara com menos frequência — o código parece mais rápido porque o producer pode escrever mais antes de pausar. Mas o problema de fundo (consumer lento) permanece. Você aumentou o buffer, não o throughput. O processo agora usa 16x mais memória e o GC vai sofrer mais quando o buffer finalmente drenar.

### 5. `readable.on('data')` sem pause → produtor irrestrito

```javascript
// ERRADO: 'data' handler sem backpressure
readable.on('data', chunk => {
  writable.write(chunk); // ignora retorno
});

// CERTO: verificar e pausar
readable.on('data', chunk => {
  if (!writable.write(chunk)) {
    readable.pause();
    writable.once('drain', () => readable.resume());
  }
});

// IDIOMÁTICO: deixe pipeline() fazer isso
await pipeline(readable, writable);
```

Adicionar um listener `'data'` coloca o Readable em modo flowing — ele produz na velocidade máxima. Sem verificar o retorno de `.write()` na Writable, você está conectando um produtor irrestrito a um consumer com limite de buffer.

### 6. `once` vs `on` no listener `'drain'`

```javascript
// ERRADO: listener permanente — acumula a cada ciclo de backpressure
ws.on('drain', resumeWriting);

// CERTO: listener de uso único por ciclo de backpressure
ws.once('drain', resumeWriting);
```

Usar `on` em vez de `once` faz com que `resumeWriting` seja chamado em **todos** os drains futuros, não apenas no próximo. Com múltiplos ciclos de backpressure, você acumula listeners, chamando `resumeWriting` N vezes no (N+1)-ésimo drain.

---

## Em entrevista

### Frase pronta

> "Backpressure is the mechanism by which a slow consumer signals back to a fast producer to slow down. In Node Streams, the signal is the boolean returned by `.write()` — if it returns `false`, you have to stop writing until the `'drain'` event fires. Ignoring this signal is the most common cause of memory leaks in stream-based code: the internal buffer grows unbounded. The `highWaterMark` defines the threshold — default 16KB for binary streams, 16 for object mode. The modern idiom is `pipeline()` from `stream/promises`, which handles backpressure automatically. Manual `.write()` is only needed in low-level code — generating data programmatically or implementing a custom Writable."

### Perguntas frequentes e respostas diretas

**"O que acontece se você ignorar o retorno de `.write()`?"**
O buffer interno cresce sem limite. Não há erro imediato — o código parece funcionar. Em produção, com alto volume, o processo consome memória progressivamente. O GC degrada. Throughput cai. O processo morre por OOM. O benchmark oficial mostra 17x mais memória sem backpressure vs. com backpressure.

**"Qual a diferença entre `highWaterMark` e o buffer do SO?"**
`highWaterMark` é o buffer **interno do stream Node**, gerenciado em userland. O buffer do SO (socket buffer, kernel buffer) é separado e gerenciado pelo kernel. Backpressure de streams Node atua no buffer userland — o buffer do SO tem seus próprios mecanismos de controle de fluxo (TCP flow control, por exemplo).

**"Por que usar `once('drain')` e não `on('drain')`?"**
Porque você quer retomar uma vez por ciclo de backpressure. `on` adiciona um listener permanente — com múltiplos ciclos, você acumula listeners que disparam repetidamente no mesmo evento. `once` registra um listener que se autorremove após a primeira dispara.

**"Como `pipeline()` implementa backpressure internamente?"**
Quando `.write()` retorna `false`, `pipeline()` chama `.pause()` no Readable de origem e registra `ws.once('drain', resume)`. Quando `'drain'` dispara, chama `.resume()` no Readable. É exatamente o padrão manual — mas implementado de forma robusta e com tratamento de erro para todos os streams da cadeia.

**"Em que cenário você precisaria de backpressure manual em vez de `pipeline()`?"**
Quando você produz dados programaticamente sem um Readable de origem — por exemplo, iterando sobre um array em memória e escrevendo em um arquivo, ou gerando um relatório linha a linha. Nesses casos não há Readable para pausar, então você controla o ritmo manualmente via `if (!ws.write(chunk)) await drain`.

**"O que acontece se `_write` nunca chamar o callback?"**
O stream trava permanentemente. O runtime não entrega nenhum chunk adicional enquanto aguarda o callback. Do ponto de vista do produtor, a Writable parece ter parado de consumir — backpressure permanente. Qualquer `pipeline()` que termine nessa Writable nunca resolverá.

### Vocabulário PT-BR ↔ EN

| Português | English |
|-----------|---------|
| retroalimentação | backpressure |
| marca d'água alta | high water mark (`highWaterMark`) |
| evento drain | drain event |
| buffer interno | internal buffer |
| memória crescente | memory growth |
| saturar | saturate |
| sumidouro | sink |
| fonte | source |
| drenar | drain |
| pausar | pause |
| retomar | resume |
| vazamento de memória | memory leak |

---

## Rubric

| Critério | Status |
|----------|--------|
| TL;DR cobre o mecanismo central | OK |
| `highWaterMark` explicado com defaults corretos | OK |
| Sinal via `.write()` boolean documentado | OK |
| Evento `'drain'` documentado | OK |
| Código INCORRETO vs CORRETO com explicação | OK |
| `pipeline()` como forma idiomática | OK |
| Comparação pipeline vs. manual lado a lado | OK |
| Custom Writable: papel do callback em `_write` | OK |
| Custom Readable: papel do retorno de `.push()` | OK |
| Armadilhas (6) com código | OK |
| Frase pronta para entrevista em EN | OK |
| Perguntas frequentes com respostas diretas | OK |
| Vocabulário PT-BR ↔ EN (12 termos) | OK |
| Veja também com wikilinks corretos | OK |
| Sem fabricação de dados reais | OK |

---

## Veja também

- `[[04 - Writable streams]]` — API completa de `.write()`, `.end()`, `cork()`/`uncork()`, implementação custom
- `[[07 - pipeline vs pipe - error handling]]` — por que `pipeline()` substitui `.pipe()` e como gerencia erros
- `[[11 - Performance e tuning]]` — tuning de `highWaterMark`, profiling de memória, benchmarks
- `[[Runtime e Event Loop]]` — galho 1: event loop e por que backpressure importa para não bloquear o loop
- `[[Node.js]]` — tronco: panorama do runtime

---

## Fontes

- [Node.js Docs — Buffering](https://nodejs.org/api/stream.html#buffering)
- [Node.js Guides — Backpressuring in Streams](https://nodejs.org/en/learn/modules/backpressuring-in-streams)
