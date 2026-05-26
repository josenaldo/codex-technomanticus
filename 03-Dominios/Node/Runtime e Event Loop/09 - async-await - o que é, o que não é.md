---
title: "async/await: o que é, o que não é"
created: 2026-05-07
updated: 2026-05-07
type: concept
status: seedling
publish: true
tags:
  - node
  - event-loop
  - async-await
  - promise
  - performance
aliases:
  - async function
  - await
  - Promise.all
---

# async/await: o que é, o que não é

> [!abstract] TL;DR
> `async/await` é açúcar sintático sobre Promises — **não cria threads, não paraleliza, não evita bloqueio**. Uma função `async` sempre retorna uma Promise. `await` pausa a execução da função até a promise liquidar, mas a thread JS fica livre para processar outros eventos durante essa pausa. Para executar operações assíncronas em paralelo, use `Promise.all`. Para descarregar trabalho CPU-bound, use Worker Threads.

---

## O que é

### `async`: a função que sempre retorna Promise

A palavra-chave `async` transforma qualquer função em uma **função assíncrona**. O efeito é simples e preciso: a função sempre retorna uma Promise, independente do que esteja dentro dela.

```javascript
async function saudacao() {
  return 'olá';
}

saudacao(); // Promise { 'olá' } — não a string diretamente
```

As equivalências exatas:

| Dentro da função async | O que a promise faz |
|---|---|
| `return value` | `Promise.resolve(value)` |
| `throw error` | `Promise.reject(error)` |
| Função retorna sem `return` | `Promise.resolve(undefined)` |

Se você retornar uma Promise de dentro de uma função `async`, o motor não encapsula promise dentro de promise — ele adota a promise interna:

```javascript
async function f() {
  return Promise.resolve(42); // mesma coisa que: return 42
}

f().then(console.log); // 42 — não Promise { 42 }
```

### `await`: pausa sem bloquear

`await` só pode ser usado dentro de uma função `async` (ou no nível de módulo com ES Modules). Ele pausa a execução da função até que a promise à direita se **liquide** (settle) — seja fulfillada ou rejeitada.

```javascript
async function buscarDados() {
  console.log('antes do await');
  const dados = await fetch('/api/dados'); // pausa aqui
  console.log('depois do await');         // continua quando fetch resolver
  return dados.json();
}
```

Durante a pausa, a thread JS não fica bloqueada esperando. O controle retorna ao event loop, que pode processar outras callbacks, timers, eventos de I/O — qualquer trabalho pendente. Quando a promise liquidar, a continuação da função é enfileirada como **microtask** e retoma assim que o frame atual terminar.

### `await` em valor não-Promise

`await` funciona com qualquer valor, não apenas promises. Se o valor não for uma promise (ou thenable), ele é automaticamente envolvido em `Promise.resolve(value)`:

```javascript
async function exemplo() {
  const x = await 42;     // mesmo que: await Promise.resolve(42)
  const y = await 'texto'; // mesmo que: await Promise.resolve('texto')
  console.log(x, y); // 42 'texto'
}
```

O comportamento é correto, mas desnecessário para valores síncronos — é açúcar que não adiciona valor nesses casos.

### Top-level await (ES Modules)

Em módulos ES (`.mjs` ou `"type": "module"` no `package.json`), `await` pode ser usado no nível do módulo, fora de qualquer função `async`:

```javascript
// arquivo.mjs
const config = await import('./config.json', { assert: { type: 'json' } });
console.log(config); // aguarda o import antes de continuar
```

Em CommonJS (`.cjs` ou padrão do Node), isso não funciona — é necessário embrulhar em uma IIFE async.

---

## O mito central: `async` não é performance

> [!warning] O mito mais comum em entrevistas de Node.js
> "Usei `async/await`, então minha rota é performática."
>
> **Errado.** `async` é uma declaração sobre o *tipo de retorno* da função — não sobre o que acontece *dentro* dela.

### O exemplo do gatilho desta trilha

```javascript
// Parece correto. Tem async. Mas bloqueia o event loop.
app.get('/users', async (req, res) => {
  const result = heavyProcessing(data);  // CPU-bound síncrono
  res.json(result);
});
```

`heavyProcessing` é código síncrono. Não importa que o handler seja `async` — enquanto `heavyProcessing` roda, a thread JS está 100% ocupada. Nenhuma outra request pode ser processada. O event loop inteiro espera.

A `async` aqui serve apenas para permitir o uso de `await` dentro do handler. Ela não cria uma thread separada, não enfileira o trabalho em background, não "torna async" o que é síncrono.

### O que `async` faz vs o que não faz

| Afirmação | Verdadeiro? |
|---|---|
| Função `async` sempre retorna Promise | Sim |
| `await` pausa a função sem bloquear a thread | Sim |
| `async` cria uma nova thread para a função | **Não** |
| `async` evita bloqueio de código CPU-bound | **Não** |
| `async` paraleliza operações dentro da função | **Não** |
| `await` em série paraleliza as operações | **Não** |

O modelo mental correto: `async/await` é uma forma de escrever código que *espera por I/O* de forma legível. Para I/O (rede, disco, banco de dados), funciona perfeitamente — a thread fica livre enquanto o sistema operacional ou libuv faz o trabalho pesado. Para CPU, não ajuda em nada.

---

## Como funciona

### Sequencial vs paralelo: o padrão mais importante

O erro mais comum com `async/await` em código de produção:

```javascript
// RUIM — sequencial sem necessidade
// Tempo total: tempo(A) + tempo(B) + tempo(C)
async function buscarDados() {
  const usuario = await fetch('/api/usuario');
  const pedidos = await fetch('/api/pedidos');
  const config  = await fetch('/api/config');
  return { usuario, pedidos, config };
}
```

Cada `await` aguarda o anterior terminar antes de disparar o próximo. As três requisições acontecem uma após a outra, mesmo sem nenhuma dependência entre elas.

```javascript
// BOM — paralelo com Promise.all
// Tempo total: max(tempo(A), tempo(B), tempo(C))
async function buscarDados() {
  const [usuario, pedidos, config] = await Promise.all([
    fetch('/api/usuario'),
    fetch('/api/pedidos'),
    fetch('/api/config'),
  ]);
  return { usuario, pedidos, config };
}
```

`Promise.all` dispara as três promises ao mesmo tempo. O `await` aguarda que todas liquidem. O tempo total é o da mais lenta — não a soma de todas.

> [!tip] Regra prática
> Se duas ou mais operações assíncronas não dependem uma da outra, use `Promise.all`. `await` em série é correto apenas quando cada operação depende do resultado da anterior.

### Os quatro combinadores de Promise

```javascript
// Promise.all — falha rápido, retorna array de valores
const [a, b, c] = await Promise.all([opA(), opB(), opC()]);
// Se qualquer uma rejeitar, Promise.all rejeita imediatamente

// Promise.allSettled — aguarda todas, retorna status de cada uma
const resultados = await Promise.allSettled([opA(), opB(), opC()]);
// resultados[0] = { status: 'fulfilled', value: ... }
//              ou { status: 'rejected', reason: ... }

// Promise.race — retorna quando a primeira liquidar (fulfilled ou rejected)
const primeiro = await Promise.race([opA(), opB(), opC()]);

// Promise.any — retorna quando a primeira fulfillada (ignora rejects)
const primeiroSucesso = await Promise.any([opA(), opB(), opC()]);
// Se todas rejeitarem, lança AggregateError
```

Tabela comparativa:

| Combinador | Falha rápida? | Aguarda todas? | Retorna | Quando usar |
|---|---|---|---|---|
| `Promise.all` | Sim (1ª rejeição) | Não | Array de valores | Todas precisam ter sucesso |
| `Promise.allSettled` | Não | Sim | Array de `{status, value\|reason}` | Tolerante a falhas parciais |
| `Promise.race` | — | Não | 1ª promise settled | Timeout, primeira resposta |
| `Promise.any` | Não | Não | 1º valor fulfillado | Fallback, redundância |

### Async iterators: `for await...of`

Quando cada item de uma coleção retorna uma promise (ou quando a coleção em si é assíncrona, como um stream), use `for await...of`:

```javascript
// Processar chunks de um stream do Node.js
async function processarStream(stream) {
  for await (const chunk of stream) {
    await processarChunk(chunk);
  }
}

// Consumir um gerador assíncrono
async function* gerarItens() {
  for (const id of ids) {
    yield await buscarItem(id); // cada next() retorna Promise
  }
}

for await (const item of gerarItens()) {
  console.log(item);
}
```

A semântica é: a cada iteração, espera o `next()` do iterador resolver antes de avançar. Combina bem com streams do Node (que implementam `Symbol.asyncIterator` desde o Node 10).

---

## Na prática

### APIs com múltiplos fetches independentes

O padrão mais observado em handlers Express/Fastify que fazem N chamadas a serviços internos:

```javascript
// Handler de página de perfil — 3 fontes independentes
app.get('/perfil/:id', async (req, res) => {
  const { id } = req.params;

  const [usuario, conquistas, atividade] = await Promise.all([
    db.usuarios.findById(id),
    db.conquistas.findByUsuario(id),
    db.atividade.findRecente(id),
  ]);

  res.json({ usuario, conquistas, atividade });
});
```

Tempo de resposta dominado pela query mais lenta, não pela soma das três.

### APIs tolerantes a falha parcial

Quando parte dos dados é opcional e a API deve responder mesmo que algumas fontes falhem:

```javascript
app.get('/dashboard', async (req, res) => {
  const resultados = await Promise.allSettled([
    buscarMetricasPrincipais(),   // crítico
    buscarAlertas(),               // opcional
    buscarNotificacoes(),          // opcional
  ]);

  const [metricas, alertas, notificacoes] = resultados;

  res.json({
    metricas: metricas.status === 'fulfilled'
      ? metricas.value
      : null,
    alertas: alertas.status === 'fulfilled'
      ? alertas.value
      : [],
    notificacoes: notificacoes.status === 'fulfilled'
      ? notificacoes.value
      : [],
  });
});
```

### Timeout de operação

Padrão clássico com `Promise.race` (ainda encontrado em codebases legados):

```javascript
// Padrão antigo — ainda válido, mas verboso
function comTimeout(promise, ms) {
  const timeout = new Promise((_, reject) =>
    setTimeout(() => reject(new Error(`Timeout após ${ms}ms`)), ms)
  );
  return Promise.race([promise, timeout]);
}

const resultado = await comTimeout(fetchExterno(), 3000);
```

Em 2026, prefira `AbortSignal.timeout()` — mais integrado com a plataforma, cancela a operação em vez de apenas rejeitar:

```javascript
// Padrão moderno — cancela o fetch quando expira
const resposta = await fetch('/api/dados', {
  signal: AbortSignal.timeout(3000),
});
```

---

## Armadilhas

### 1. `await` em loop sequencial

```javascript
// ARMADILHA — O(n) serial. Lento para listas grandes.
async function processarTodos(itens) {
  const resultados = [];
  for (const item of itens) {
    resultados.push(await processarItem(item)); // aguarda cada um
  }
  return resultados;
}

// CORRETO — paralelo
async function processarTodos(itens) {
  return Promise.all(itens.map(processarItem));
}
```

O loop com `await` não é sempre errado — é correto quando cada item depende do resultado do anterior, ou quando você precisa limitar concorrência. Mas é um problema grave quando as operações são independentes.

### 2. `Promise.all` sem controle de concorrência

```javascript
// ARMADILHA — 10.000 conexões simultâneas
const resultados = await Promise.all(
  listaComDezMilItens.map(item => fetch(`/api/${item}`))
);
// Pode derrubar o servidor de destino ou esgotar o pool de conexões
```

Para listas grandes, use batches ou uma biblioteca como `p-limit`:

```javascript
import pLimit from 'p-limit';

const limit = pLimit(10); // máximo 10 concorrentes

const resultados = await Promise.all(
  listaComDezMilItens.map(item =>
    limit(() => fetch(`/api/${item}`))
  )
);
```

Ou processe em batches manuais com `for await...of`:

```javascript
async function* emBatches(itens, tamanho) {
  for (let i = 0; i < itens.length; i += tamanho) {
    yield itens.slice(i, i + tamanho);
  }
}

for await (const batch of emBatches(itens, 50)) {
  await Promise.all(batch.map(processarItem));
}
```

### 3. `async` em handler Express não captura erros automaticamente

```javascript
// ARMADILHA — erro não chega ao middleware de erro do Express
app.get('/rota', async (req, res) => {
  const dados = await operacaoQuePodeFalhar(); // se rejeitar...
  res.json(dados);
  // ...o Express não sabe. O processo pode ficar em estado inconsistente.
});

// CORRETO — wrapper que captura e passa pro next()
const asyncHandler = (fn) => (req, res, next) =>
  Promise.resolve(fn(req, res, next)).catch(next);

app.get('/rota', asyncHandler(async (req, res) => {
  const dados = await operacaoQuePodeFalhar();
  res.json(dados);
}));
```

**Fastify** e **NestJS** lidam com isso nativamente — handlers `async` que rejeitam são automaticamente roteados para o handler de erro. No Express 5 (lançado em 2024), handlers async também são capturados automaticamente. No Express 4 (ainda amplamente usado), o wrapper manual ou uma biblioteca como `express-async-errors` é necessária.

### 4. `async` não cria thread — o exemplo do gatilho, revisitado

```javascript
// ARMADILHA — parece async, bloqueia o event loop
app.post('/relatorio', async (req, res) => {
  // parse de CSV com 500k linhas, todo em memória, síncrono
  const linhas = req.body.csv
    .split('\n')
    .map(linha => linha.split(','));

  const agregado = calcularAgregados(linhas); // CPU pesado, síncrono

  res.json(agregado);
});
```

Enquanto `calcularAgregados` roda (digamos, 800ms), zero outras requests são processadas. A `async` não muda isso. Solução: mover o trabalho CPU-bound para um Worker Thread (coberto no galho 2 da trilha — Paralelismo em Node.js).

```javascript
// Esboço da solução correta para CPU-bound
import { Worker } from 'worker_threads';

app.post('/relatorio', async (req, res) => {
  const resultado = await rodarEmWorker('./workers/relatorio.js', {
    csv: req.body.csv,
  });
  res.json(resultado);
  // A thread principal ficou livre durante o processamento
});
```

### 5. Ausência de try/catch em código `async`

Rejeições de promises dentro de funções `async` viram erros não capturados se não houver `try/catch` ou `.catch()` no ponto de chamada:

```javascript
// ARMADILHA — rejeição silenciosa
async function inicializar() {
  const config = await carregarConfig(); // pode rejeitar
  await conectarBanco(config);           // pode rejeitar
}

inicializar(); // Promise não capturada — no Node 15+, termina o processo

// CORRETO
inicializar().catch((err) => {
  console.error('Falha na inicialização:', err);
  process.exit(1);
});

// Ou com top-level await em ESM:
try {
  await inicializar();
} catch (err) {
  console.error('Falha na inicialização:', err);
  process.exit(1);
}
```

---

## Em entrevista

### Frase pronta (em inglês)

> "`async/await` is syntactic sugar over Promises. An `async` function always returns a Promise; `await` pauses the function until the awaited Promise settles, but the JS thread is free during that pause to handle other work. The most common misconception in Node interviews is that `async` makes code 'performant' or 'parallel' — it doesn't. If your async handler does CPU-bound synchronous work, the entire event loop blocks for that duration and every other request has to wait. To actually parallelize asynchronous work, use `Promise.all` or `Promise.allSettled`. To offload CPU work, use Worker Threads."

### Perguntas frequentes e respostas diretas

**"Qual a diferença entre `async/await` e Promises?"**
Nenhuma diferença de comportamento — `async/await` é açúcar sintático. Por baixo, o motor converte para encadeamento de Promises. A diferença é legibilidade: `async/await` elimina `.then()` encadeados e torna o fluxo linear.

**"Por que usar `Promise.all` em vez de vários `await`s em série?"**
Operações em série tomam `soma(tempos)`. Operações em paralelo com `Promise.all` tomam `max(tempos)`. Para operações independentes, o paralelo é sempre mais rápido.

**"O que acontece se uma promise em `Promise.all` rejeitar?"**
`Promise.all` rejeita imediatamente com o motivo da primeira rejeição. As outras promises continuam rodando, mas seus resultados são ignorados. Se você precisa do resultado de todas — incluindo as falhas — use `Promise.allSettled`.

**"Pode usar `await` fora de uma função `async`?"**
Sim, em ES Modules (top-level await). Não em CommonJS. Em CommonJS é necessário embrulhar em `(async () => { ... })()`.

**"Como lidar com erros em `async/await`?"**
`try/catch` dentro da função async captura rejeições de qualquer `await` dentro do bloco. No ponto de chamada, `.catch()` ou `try/catch` em volta do `await` da chamada. Em handlers de frameworks, verificar se o framework captura automaticamente (Fastify/NestJS/Express 5 sim; Express 4 não).

### Vocabulário técnico

| PT-BR | EN |
|---|---|
| açúcar sintático | syntactic sugar |
| liquidar / liquidada | settle / settled |
| pausar a função | pause the function |
| paralelizar | parallelize |
| trabalho de CPU / trabalho CPU-bound | CPU-bound work |
| iterador assíncrono | async iterator |
| falha rápida | fail-fast |
| concorrência | concurrency |
| thread principal | main thread / event loop thread |

---

## Veja também

- [[08 - Promises por dentro]] — estados, microtask queue, encadeamento: o substrato que `async/await` abstrai
- [[10 - Bloqueio do event loop - sintomas e causas]] — o que acontece quando código síncrono pesado domina a thread
- [[Node.js]] — tronco da trilha Node Senior

Para descarregar trabalho CPU-bound da thread principal, o caminho é **Worker Threads** — coberto no galho 2 da trilha (Paralelismo em Node.js), que ainda não existe neste vault. Quando disponível, será acessível a partir do MOC central do Node.js. A nota [[10 - Bloqueio do event loop - sintomas e causas]] já toca no diagnóstico de quando isso é necessário.
