---
title: "Por que paralelismo em Node"
created: 2026-05-07
updated: 2026-05-07
type: concept
status: seedling
publish: true
tags:
  - node
  - paralelismo
  - mental-model
  - cpu-bound
aliases:
  - CPU-bound vs I/O-bound
  - Quando paralelizar
---

# Por que paralelismo em Node

> [!abstract] TL;DR
> Node é single-thread e isso geralmente está certo — o event loop resolve a imensa maioria dos workloads I/O-bound com eficiência notável. Mas há casos onde paralelismo é a única saída: trabalho CPU-bound persistente, event loop lag que não cede com otimização, throughput cronicamente limitado. Antes de paralelizar, considere streaming, paginação, refatoração do algoritmo ou filas de background. Quando essas alternativas falham, há 3 ferramentas: Worker Threads, Cluster, e `child_process` — a escolha depende do problema, não do que parece mais familiar.

---

## O que é

Paralelismo no contexto Node significa executar trabalho **simultaneamente** em outras threads ou processos, fora do event loop principal.

Essa definição importa porque é diferente de **concorrência** — que é o que `async/await` e o event loop fazem. Concorrência significa *alternar* entre tarefas: o event loop processa um callback, suspende enquanto I/O aguarda, retoma outro callback. Em nenhum momento duas linhas de JavaScript executam ao mesmo tempo na thread principal.

Paralelismo quebra essa restrição ao mover trabalho para fora da thread JS:

| Mecanismo | O que é | Fronteira |
|---|---|---|
| **Worker Threads** | Threads JS separadas no mesmo processo | Memória compartilhável via `SharedArrayBuffer`; comunicação via `postMessage` |
| **Cluster** | Múltiplos processos Node compartilhando a mesma porta TCP | Processos independentes; o SO distribui as conexões |
| **`child_process`** | Processo externo independente | Totalmente isolado; comunica via stdin/stdout/IPC |

As três ferramentas são cobertas em detalhe nas notas seguintes do galho. Esta nota responde a pergunta anterior: *por que você precisaria de qualquer uma delas*.

---

## Por que importa

Node.js tem um design deliberado: single-threaded. A aposta é que a maioria dos servidores web passa mais tempo esperando I/O (banco de dados, rede, disco) do que executando JavaScript. Essa aposta está correta para a maioria dos casos — e é por isso que Node escala bem com `async/await` sem precisar de threads.

O problema surge quando um serviço tem trabalho genuinamente **CPU-bound**: o event loop não pode "esperar" por um cálculo da mesma forma que espera por um banco de dados. Enquanto o cálculo roda, a thread JS está ocupada. Nenhum outro callback executa.

Sem o entendimento de paralelismo, o padrão de debugging vai na direção errada:

- Tentar resolver bloqueio de CPU com `async/await` — não funciona. Como demonstrado em [[09 - async-await - o que é, o que não é]], `async` não cria uma thread separada. Código síncrono dentro de um handler `async` ainda bloqueia o event loop.
- Aumentar réplicas no orquestrador sem entender a causa raiz — pode funcionar, mas é caro e mascara o problema estrutural.
- Mover para uma linguagem "mais rápida" sem evidência de que o gargalo é o runtime — decisão irreversível baseada em hipótese.

Saber reconhecer CPU-bound vs I/O-bound, e conhecer as 3 ferramentas de paralelismo, é o que diferencia uma análise de causa raiz de um debugging por tentativa e erro.

---

## Como funciona

### CPU-bound vs I/O-bound: a distinção central

A distinção mais importante para decidir quando paralelizar:

**I/O-bound:** o trabalho é esperar. O programa envia um request ao banco de dados, ao sistema de arquivos, a uma API externa — e aguarda a resposta. A thread JS fica livre durante a espera. O event loop + `async/await` resolvem isso perfeitamente. Paralelismo via Worker Threads geralmente não ajuda aqui e pode piorar (mais context switches, mais overhead de coordenação).

**CPU-bound:** o trabalho é computação. Hashing de senha, processamento de imagem, compressão, inferência de modelos de ML, parsing de CSV de 500 mil linhas em memória. A thread JS fica ocupada executando JavaScript. O event loop não consegue "liberar" a thread para I/O porque não há I/O aguardando — só cálculo.

O sinal diagnóstico é o event loop lag — coberto em detalhes em [[10 - Bloqueio do event loop - sintomas e causas]]. Em condições normais: lag de 0-5ms. Com CPU-bound persistente: lag de centenas de milissegundos ou segundos. A latência sobe em **todos** os endpoints simultaneamente — não apenas no endpoint responsável pelo cálculo.

### O exemplo concreto: bcrypt sob carga

Imagine um servidor de autenticação que usa `bcrypt.hashSync` para criar hashes de senha:

```javascript
// ❌ Problema — bcrypt síncrono bloqueia o event loop
app.post('/register', (req, res) => {
  const { password } = req.body;

  // hashSync executa em JavaScript puro na thread principal
  // Dependendo do cost factor, pode levar 200-400ms
  const hash = bcrypt.hashSync(password, 12);

  await db.users.create({ password: hash });
  res.json({ ok: true });
});
```

Com 10 requisições de registro concorrentes, o event loop fica efetivamente bloqueado de forma contínua. Todos os outros endpoints — incluindo `GET /health` — passam a responder com latência de segundos, independente de quão simples sejam.

**Antes de ir direto para Worker Thread**, há opções de menor complexidade para testar:

```javascript
// Opção 1 — usar a API async do bcrypt (usa o thread pool de libuv)
app.post('/register', async (req, res) => {
  const { password } = req.body;

  // bcrypt.hash usa callbacks internamente — a operação vai para o thread pool
  const hash = await bcrypt.hash(password, 12);

  await db.users.create({ password: hash });
  res.json({ ok: true });
});
```

A API async do bcrypt (e do `crypto.pbkdf2`, `crypto.randomBytes`, etc.) usa o **thread pool de libuv** — as 4 threads nativas que Node mantém por padrão. Isso remove o trabalho da thread JS. Se ainda saturar (muitas requisições concorrentes de registro), o próximo passo é aumentar o pool:

```bash
# Aumentar o thread pool de 4 para 16 threads
UV_THREADPOOL_SIZE=16 node server.js
```

Se mesmo com pool ampliado o CPU usage de cada thread do pool for persistentemente alto, aí sim Worker Thread dedicado é a solução estrutural — porque o problema não é o número de threads, mas o tempo de CPU por operação.

```javascript
// Opção 2 — Worker Thread dedicado (quando o pool ainda satura)
// worker-bcrypt.js
const { workerData, parentPort } = require('worker_threads');
const bcrypt = require('bcrypt');

async function run() {
  const hash = await bcrypt.hash(workerData.password, workerData.rounds);
  parentPort.postMessage({ hash });
}

run().catch((err) => parentPort.postMessage({ error: err.message }));

// handler principal
import { Worker } from 'worker_threads';

function hashNoWorker(password, rounds) {
  return new Promise((resolve, reject) => {
    const worker = new Worker('./worker-bcrypt.js', {
      workerData: { password, rounds },
    });
    worker.once('message', ({ hash, error }) => {
      if (error) reject(new Error(error));
      else resolve(hash);
    });
    worker.once('error', reject);
  });
}

app.post('/register', async (req, res) => {
  const hash = await hashNoWorker(req.body.password, 12);
  await db.users.create({ password: hash });
  res.json({ ok: true });
  // Thread principal livre durante todo o hashing
});
```

O padrão acima cria um Worker por request — funcional, mas não ideal para alta carga (overhead de criação de thread por request). A próxima evolução é um **pool de workers** reutilizáveis, coberto em [[06 - Pool de workers - pattern de produção]].

---

## Na prática

O padrão de raciocínio recomendado antes de qualquer decisão de paralelismo:

### Passo 1 — Medir antes de qualquer coisa

"Tá lento" sem medição é hipótese, não diagnóstico. Metrificar:

- **Event loop lag** (`perf_hooks.monitorEventLoopDelay`, Clinic.js) — o sinal mais direto de bloqueio de thread
- **Percentis de latência por endpoint** (p50, p95, p99) — latência conjunta aponta para event loop; latência isolada aponta para lógica local
- **CPU usage** por thread — distingue thread pool saturado de loop JS bloqueado

Sem esses números, qualquer solução é um palpite. Mais contexto de diagnóstico em [[10 - Bloqueio do event loop - sintomas e causas]].

### Passo 2 — Tentar alternativas antes de paralelizar

Paralelismo adiciona complexidade real: coordenação entre threads/processos, serialização de dados, tratamento de erros cruzados, debugging mais difícil. Há alternativas que resolvem muitos casos com menos custo:

| Alternativa | Quando usar |
|---|---|
| **Streaming** | Dados grandes que podem ser processados em chunks — evita `JSON.parse` de payload inteiro |
| **Paginação** | Listas grandes que podem ser retornadas em partes |
| **Refatoração do algoritmo** | Complexidade O(n²) que pode virar O(n log n); evita a causa raiz |
| **API async em vez de sync** | Trocar `crypto.pbkdf2Sync` por `crypto.pbkdf2`; `fs.readFileSync` por `fs.promises.readFile` |
| **Aumentar `UV_THREADPOOL_SIZE`** | Quando o gargalo é o pool de libuv saturado, não o loop JS |
| **Fila de background** (BullMQ, etc.) | Trabalho que não precisa de resposta imediata; desacopla o request do processamento |

Essas alternativas não são "workarounds inferiores" — frequentemente são a solução correta. Paralelismo é para quando elas falham.

### Passo 3 — Escolher a ferramenta certa

Quando paralelismo é inevitável, a ferramenta certa depende do problema:

- **Worker Threads** — CPU-bound dentro do processo Node; acesso à memória compartilhada possível; mesma codebase
- **Cluster** — escalar um servidor HTTP para usar todos os cores da máquina; o SO distribui as conexões TCP
- **`child_process`** — rodar ferramenta externa (ImageMagick, ffmpeg, script Python) ou spawnar processo Node isolado

A decision tree completa está em [[11 - Decision tree - qual ferramenta para qual problema]].

---

## Armadilhas

### 1. Paralelizar sem medir

O erro mais comum: adotar Worker Threads como primeira resposta a "a API está lenta". Worker Threads adicionam complexidade mensurável — thread management, serialização de mensagens via `postMessage`, tratamento de erros em contextos separados, debugging mais difícil. Se o bottleneck for I/O (query lenta, dependência externa, paginação ausente), Worker Thread não ajuda em nada e pode piorar a latência por overhead de coordenação.

A sequência correta é sempre: medir → identificar o tipo de bottleneck → selecionar a solução mínima que resolve.

### 2. Confundir CPU-bound com I/O-bound

Um handler que faz `await db.query()` e depois processa os resultados em memória pode ter ambos os componentes: I/O-bound na query (resolvido por `async/await`) e CPU-bound no processamento dos resultados (não resolvido por `async/await`).

O erro é assumir que porque o handler usa `await` e o banco está "lento", a solução é otimizar a query. Se o event loop lag dispara *depois* que a query retorna, o problema é o processamento em memória — CPU-bound — e a query está bem.

Paralelizar I/O via Worker Threads é tipicamente pior que `async/await` puro: há overhead de serialização dos dados entre threads, e a operação de I/O em si vai para o kernel/thread pool de qualquer forma.

### 3. Achar que `UV_THREADPOOL_SIZE` resolve qualquer CPU-bound

`UV_THREADPOOL_SIZE` aumenta o número de threads nativas no pool de libuv. Isso ajuda apenas para operações que **usam esse pool** — `crypto.pbkdf2`, `bcrypt.hash` (via API async), `fs.promises.*`, `dns.lookup`, compressão com `zlib` async.

Trabalho síncrono próprio em JavaScript — um loop de processamento, um parser customizado, um algoritmo de cálculo — não usa o pool de libuv. Ele roda na thread JS. `UV_THREADPOOL_SIZE=100` não faz nenhuma diferença para esse tipo de trabalho. A solução para código JS síncrono pesado é Worker Thread — que cria uma thread JS separada onde esse código pode rodar sem bloquear o event loop principal.

---

## Em entrevista

### Frase pronta (em inglês)

> "Node is single-threaded by design, and that's the right choice for most I/O-bound workloads. But when you have genuine CPU-bound work — image processing, hashing, ML inference, compression — single-thread becomes the bottleneck. The signal is event loop lag that persists across optimization attempts. The structural fix is parallelism, but Node has three different parallelism tools — Worker Threads for shared-memory threads within the same process, Cluster for sharing an HTTP port across multiple Node processes so the OS distributes connections, and `child_process` for spawning external commands or isolated Node processes. Choosing the right one matters more than knowing they exist. And before reaching for any of them, I'd validate that streaming, pagination, algorithm refactoring, or background queues don't solve the problem with less complexity."

### Vocabulário técnico

| PT-BR | EN |
|---|---|
| paralelismo | parallelism |
| concorrência | concurrency |
| trabalho de CPU / limitado por CPU | CPU-bound work |
| limitado por I/O | I/O-bound |
| atraso do event loop | event loop lag |
| pool de threads | thread pool |
| processo | process |
| thread | thread |
| thread principal | main thread |
| serialização | serialization |
| overhead de coordenação | coordination overhead |

### Perguntas frequentes em entrevista

**"Por que Node não cria uma thread por request como Java/Go?"**
Por design deliberado: threads têm custo fixo de memória e o context switching tem overhead. Para workloads I/O-bound (a maioria dos servidores web), um único event loop com I/O assíncrono escala com menos recursos. O custo é que workloads CPU-bound precisam de tratamento explícito — o que exige mais conhecimento do runtime mas resulta em sistemas mais previsíveis.

**"Quando você escolheria Worker Threads vs Cluster?"**
Worker Threads para CPU-bound dentro de um processo: processamento de imagem, hashing, computação pesada que precisa de resultado para devolver ao handler. Cluster para escalar um servidor HTTP para usar múltiplos cores: réplicas do processo inteiro, cada uma com seu event loop, o SO distribuindo conexões TCP entre elas. São soluções para problemas diferentes.

**"Async/await não resolve CPU-bound?"**
Não. `async/await` é açúcar sintático sobre Promises — gerencia quando a thread JS espera por I/O. Código síncrono dentro de um handler `async` ainda roda na thread JS e ainda bloqueia o event loop. A distinção completa está em [[09 - async-await - o que é, o que não é]].

---

## Veja também

- [[02 - As 3 ferramentas - Worker Threads, Cluster, child_process]] — visão panorâmica das 3 ferramentas com comparação de trade-offs
- [[03 - Worker Threads - fundamentos]] — como criar, comunicar e destruir Worker Threads
- [[11 - Decision tree - qual ferramenta para qual problema]] — fluxograma de decisão com critérios objetivos
- [[03-Dominios/Node/Runtime e Event Loop/index]] — galho 1: o modelo mental de base que esta nota pressupõe
- [[09 - async-await - o que é, o que não é]] — galho 1: por que `async` não resolve CPU-bound
- [[10 - Bloqueio do event loop - sintomas e causas]] — galho 1: como diagnosticar e confirmar bloqueio
- [[Node.js]] — tronco da trilha Node Senior
