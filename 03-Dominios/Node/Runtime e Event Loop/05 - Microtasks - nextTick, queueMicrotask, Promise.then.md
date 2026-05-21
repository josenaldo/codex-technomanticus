---
title: "Microtasks: nextTick, queueMicrotask, Promise.then"
created: 2026-05-07
updated: 2026-05-07
type: concept
status: seedling
publish: true
tags:
  - node
  - event-loop
  - microtask
  - nexttick
  - promise
aliases:
  - Microtasks
  - process.nextTick
  - queueMicrotask
---

# Microtasks: nextTick, queueMicrotask, Promise.then

> [!abstract] TL;DR
> Microtasks rodam **entre fases** do event loop, antes que a próxima fase comece. A hierarquia de prioridade é estrita: `process.nextTick` drena sua fila inteira primeiro, depois `queueMicrotask` e `Promise.then` são processados na fila padrão de microtasks. Recursão em `nextTick` **bloqueia o loop indefinidamente** — o fenômeno chamado de queue starvation. `nextTick` é uma API Node-specific; `queueMicrotask` é a API padrão da web, portável entre runtimes.

## O que é

Uma **microtask** é uma unidade de trabalho que o runtime executa assim que o código síncrono atual termina, mas **antes** de avançar para a próxima fase do event loop (antes de processar timers, I/O, setImmediate, etc.). O conceito existe tanto no browser quanto no Node.js, mas o Node adiciona uma camada extra: a fila do `process.nextTick`.

No Node.js, existem três APIs principais que agendam trabalho nesse espaço "entre fases":

### `process.nextTick(callback[, ...args])`

A API mais antiga e de maior prioridade. Callbacks registrados com `nextTick` são colocados em uma **fila separada** — a `nextTickQueue` — que é drenada **completamente** antes que qualquer microtask convencional seja processada, e antes que o event loop avance de fase. É uma API **Node-specific**: não existe nos browsers nem no Deno com a mesma semântica.

```javascript
process.nextTick(() => {
  console.log('nextTick callback');
});
```

O segundo argumento em diante é repassado como argumento ao callback — útil para evitar closures desnecessárias:

```javascript
process.nextTick((usuario, acao) => {
  console.log(`${usuario} fez ${acao}`);
}, 'alice', 'login');
```

### `queueMicrotask(callback)`

Introduzida no Node.js 11 (globalizada no Node 12), `queueMicrotask` agenda uma função na **fila padrão de microtasks** — a mesma fila usada pelos callbacks de `Promise`. É a API **portável**: existe no browser, no Node.js, no Deno e no Bun com comportamento idêntico. Não aceita argumentos extras (use uma arrow function se precisar de closure).

```javascript
queueMicrotask(() => {
  console.log('microtask via queueMicrotask');
});
```

### `Promise.resolve().then(callback)`

O mecanismo mais familiar. Callbacks de `.then()`, `.catch()` e `.finally()` também são enfileirados na fila padrão de microtasks, na mesma posição que `queueMicrotask`. A diferença principal está no tratamento de erros: erros em callbacks de Promise viram `unhandledRejection`; erros em `queueMicrotask` viram `uncaughtException`.

```javascript
Promise.resolve().then(() => {
  console.log('microtask via Promise.then');
});
```

### Hierarquia dentro de uma iteração

Em cada ponto de drenagem (ao final de cada fase do event loop, e ao final de cada callback de macrotask):

1. **`nextTickQueue`** — drenada completamente (todos os `nextTick` pendentes, incluindo os novos que forem adicionados durante a drenagem)
2. **Microtask queue** — drenada completamente (`queueMicrotask` + `Promise.then`, intercalados na ordem em que foram enfileirados)
3. **Próxima fase do event loop** começa

## Por que importa

Controlar a ordem de execução em nível fino é essencial em dois contextos principais:

**Correção de APIs assíncronas**: uma função que às vezes retorna sincronamente e às vezes assincronamente cria bugs difíceis de rastrear. Deferir o callback com `nextTick` garante que o caller sempre recebe o resultado de forma assíncrona, mesmo quando o trabalho é síncrono — permitindo que o caller registre listeners ou configure estado *antes* que o callback rode.

**Debugging de ordem de execução**: microtasks são a causa mais comum de "por que esse callback rodou antes do que eu esperava?". Entender a hierarquia — nextTick > microtasks > macrotasks (timers, I/O, setImmediate) — é requisito para diagnosticar corridas e comportamentos inesperados em código assíncrono.

## Como funciona

### Exemplo 1 — Ordem de execução com timer, Promise e nextTick

```javascript
setTimeout(() => console.log('1: timer'), 0);

Promise.resolve().then(() => console.log('2: promise'));

process.nextTick(() => console.log('3: nextTick'));

console.log('4: síncrono');

// Saída:
// 4: síncrono      (código síncrono roda primeiro, esvaziando a call stack)
// 3: nextTick      (nextTickQueue drenada antes das microtasks)
// 2: promise       (microtask queue drenada antes de avançar de fase)
// 1: timer         (macrotask — fase timers do event loop)
```

A call stack deve estar vazia antes de qualquer microtask rodar. Código síncrono tem prioridade absoluta. Em seguida vem a `nextTickQueue`, depois as microtasks convencionais, e só então o event loop avança para a próxima fase (onde timers, I/O e setImmediate vivem).

### Exemplo 2 — Recursão em nextTick bloqueia o event loop (starvation)

```javascript
function loop() {
  process.nextTick(loop);
}

loop();

// O programa nunca avança.
// Nenhum timer, I/O, ou setImmediate jamais executa.
// A nextTickQueue é drenada antes de qualquer avanço de fase,
// mas cada drenagem adiciona mais um item — loop infinito na fila.
```

O mesmo problema ocorre com `queueMicrotask` recursivo: a microtask queue também é completamente drenada antes de avançar de fase, então recursão na microtask queue também trava o event loop.

### Exemplo 3 — queueMicrotask vs Promise.resolve().then

```javascript
queueMicrotask(() => console.log('A: queueMicrotask'));
Promise.resolve().then(() => console.log('B: Promise.then'));
queueMicrotask(() => console.log('C: queueMicrotask 2'));

// Saída:
// A: queueMicrotask
// B: Promise.then
// C: queueMicrotask 2

// Ambas as APIs alimentam a mesma fila de microtasks.
// A ordem é a ordem de enfileiramento — FIFO.
```

A diferença não é de prioridade, mas de comportamento em caso de erro:

```javascript
// Erro em queueMicrotask → uncaughtException
queueMicrotask(() => {
  throw new Error('erro síncrono na microtask');
});

// Erro em Promise.then → unhandledRejection
Promise.resolve().then(() => {
  throw new Error('erro vira rejeição de Promise');
});
```

### Tabela comparativa

| API | Fila | Prioridade | Padrão | Aceita args extras | Erro não capturado |
|-----|------|-----------|--------|--------------------|--------------------|
| `process.nextTick` | `nextTickQueue` | Mais alta | Node-specific | Sim | `uncaughtException` |
| `queueMicrotask` | Microtask queue | Padrão | Web/Node/Deno/Bun | Não | `uncaughtException` |
| `Promise.then` | Microtask queue | Padrão | Web/Node/Deno/Bun | Não | `unhandledRejection` |

## Na prática

### Pattern: EventEmitter no constructor

O uso canônico do `process.nextTick` em bibliotecas é garantir que o evento emitido no construtor possa ser observado por listeners registrados *depois* da instanciação:

```javascript
const { EventEmitter } = require('node:events');

class MyEmitter extends EventEmitter {
  constructor() {
    super();
    // SEM nextTick: o emit roda antes do caller registrar .on('event', ...)
    // COM nextTick: o emit é diferido, caller tem chance de registrar o listener
    process.nextTick(() => {
      this.emit('ready');
    });
  }
}

const emitter = new MyEmitter();

// Este listener é registrado antes do nextTick rodar
emitter.on('ready', () => {
  console.log('emitter pronto'); // funciona corretamente
});
```

Sem o `nextTick`, o `emit('ready')` rodaria durante a execução do construtor, antes que a linha `emitter.on('ready', ...)` fosse alcançada — e o listener nunca seria disparado.

### Pattern: validação assíncrona consistente

```javascript
function processarDados(dados, callback) {
  if (!Array.isArray(dados)) {
    // Retornar erro sincronamente quebraria o contrato assíncrono da API
    return process.nextTick(callback, new TypeError('dados deve ser array'));
  }

  // Caminho assíncrono real
  setImmediate(() => {
    callback(null, dados.map(d => d * 2));
  });
}

// O caller sempre recebe o callback de forma assíncrona — comportamento previsível
processarDados('erro', (err) => {
  console.error(err.message); // 'dados deve ser array'
});
```

### Quando preferir queueMicrotask

Use `queueMicrotask` quando:
- O código precisa rodar em múltiplos runtimes (browser + Node.js)
- Não há necessidade de prioridade sobre Promises
- A semântica padrão de microtask é suficiente

Use `process.nextTick` quando:
- É necessária execução *antes* de qualquer Promise pendente
- O código é Node.js-only e precisa do padrão de callback assíncrono consistente
- Está construindo uma API de baixo nível que emite eventos

## Armadilhas

### 1. nextTick recursivo trava o event loop

```javascript
// NUNCA faça isso em produção
function processarFila(items) {
  if (items.length === 0) return;
  const item = items.shift();
  console.log(item);
  process.nextTick(() => processarFila(items)); // starvation!
}
```

Esse padrão impede que qualquer timer ou I/O execute enquanto a fila não estiver vazia. Em um servidor HTTP, isso causa timeouts em todas as requests concorrentes. Use `setImmediate` em vez de `nextTick` para processar filas longas — `setImmediate` roda na fase check, **após** I/O, sem bloquear o loop.

### 2. queueMicrotask recursivo também trava

```javascript
function processar() {
  queueMicrotask(processar); // mesma armadilha, diferente API
}
processar();
```

A microtask queue é drenada completamente antes de avançar de fase, assim como a `nextTickQueue`. Qualquer recursão sem condição de parada nas duas filas produz starvation.

### 3. Erros não capturados têm comportamento diferente por API

```javascript
// Erro em nextTick → uncaughtException (pode derrubrar o processo)
process.nextTick(() => {
  throw new Error('falha em nextTick');
});

// Erro em queueMicrotask → uncaughtException (similar ao nextTick)
queueMicrotask(() => {
  throw new Error('falha em queueMicrotask');
});

// Erro em Promise.then → unhandledRejection (pode ser capturado com .catch)
Promise.resolve()
  .then(() => { throw new Error('falha em then'); })
  .catch(err => console.error('capturado:', err.message)); // funciona
```

Rejeições de Promise sem `.catch()` geram `unhandledRejection` — evento diferente de `uncaughtException`. Em Node.js 15+, `unhandledRejection` derruba o processo por padrão. Mas erros em `nextTick` e `queueMicrotask` vão direto para `uncaughtException` — não existe mecanismo de "catch" para eles além do handler global.

### 4. setImmediate não é "imediato" no sentido de microtask

```javascript
setImmediate(() => console.log('A: setImmediate'));
Promise.resolve().then(() => console.log('B: Promise'));
process.nextTick(() => console.log('C: nextTick'));

// Saída:
// C: nextTick
// B: Promise
// A: setImmediate  ← roda por último, na fase check do próximo tick
```

`setImmediate` é uma **macrotask** que roda na fase `check` do event loop — depois de toda a drenagem de microtasks. Desenvolvedores que esperam `setImmediate` ser "mais imediato" que `Promise.then` se surpreendem com essa ordem.

### 5. nextTick dentro de callback de Promise herda o contexto correto

```javascript
Promise.resolve().then(() => {
  process.nextTick(() => console.log('nextTick dentro de then'));
  console.log('dentro do then');
});

// Saída:
// dentro do then
// nextTick dentro de then  ← nextTick registrado dentro de then roda ANTES
//                             das próximas microtasks na fila
```

Um `nextTick` registrado dentro de uma microtask em execução é processado **antes** das demais microtasks já enfileiradas. A `nextTickQueue` é verificada após cada microtask individual, não apenas ao final de toda a fila.

## Em entrevista

> [!tip] Frase pronta (inglês)
> "Node has three microtask APIs with a strict priority order: `process.nextTick` runs first — it has its own queue that's drained before any other microtask. Then `queueMicrotask` and `Promise.then` are interleaved in the standard microtask queue. Microtasks run between every event loop phase, so they're higher priority than any timer or I/O callback. The danger of `process.nextTick` is recursion — a callback that schedules another `nextTick` will starve the event loop, since the queue is drained completely before phases advance."

### Vocabulário técnico

| Português | Inglês |
|-----------|--------|
| Fila de microtarefas | Microtask queue |
| Prioridade | Priority |
| Inanição da fila | Queue starvation |
| API específica de Node | Node-specific API |
| Drenagem da fila | Queue draining |
| Iteração do event loop | Event loop tick / iteration |
| Avanço de fase | Phase transition |

### Perguntas frequentes em entrevista

**"Qual a diferença entre `process.nextTick` e `setImmediate`?"**
`nextTick` roda antes de qualquer fase do event loop avançar — é uma microtask com prioridade máxima. `setImmediate` roda na fase `check`, que é uma macrotask executada depois de I/O. Em termos de ordem: nextTick → microtasks → I/O → setImmediate → timers (próxima iteração).

**"Quando devo usar `queueMicrotask` em vez de `Promise.resolve().then()`?"**
Quando não há uma Promise natural no contexto e você quer agendar uma microtask sem criar um wrapper de Promise desnecessário. `queueMicrotask` é mais explícito na intenção e tem overhead ligeiramente menor. Semanticamente são equivalentes em termos de prioridade e ordem.

**"O que acontece se eu lançar um erro dentro de `process.nextTick`?"**
O erro propaga como `uncaughtException` — não existe `.catch()` para nextTick. O processo pode ser derrubado se não houver um handler `process.on('uncaughtException', ...)`. Diferente de Promise, onde o erro vira `unhandledRejection` e pode ser capturado com `.catch()`.

## Veja também

- `[[04 - As fases do event loop]]` — onde as microtasks se encaixam no ciclo completo
- `[[06 - Macrotasks e timers - setTimeout, setInterval, setImmediate]]` — a camada de macrotasks que vem depois das microtasks
- `[[08 - Promises por dentro]]` — como o mecanismo de Promise alimenta a microtask queue
- `[[Node.js]]` — tronco da trilha de runtime Node.js
