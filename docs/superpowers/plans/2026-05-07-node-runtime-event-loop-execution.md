---
title: "Plano — Execução da Sub-trilha Runtime e Event Loop (Galho 1)"
date: 2026-05-07
status: ready
type: plan
publish: false
---

# Sub-trilha Runtime e Event Loop — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produzir 12 notas atômicas + 1 MOC em `03-Dominios/Node/Runtime e Event Loop/`, em PT-BR, todas `publish: true`, cobrindo do mental model do runtime de Node ao diagnóstico de event loop bloqueado — para um dev senior em prep para entrevista internacional. Ao final, podar as seções correspondentes do tronco `JavaScript/Backend/Node.js.md` e atualizar o MOC central de `03-Dominios/Node/index.md`.

**Architecture:** Sub-trilha sequencial em 4 blocos (Mental model → Event loop deep dive → async/await em profundidade → Bloqueio e diagnóstico) + 1 nota de fechamento + 1 MOC com 4 rotas alternativas. Cada nota é atômica e linkável, segue estrutura híbrida (TL;DR + corpo técnico), com code samples em JS ou TS (Node 22 LTS / 24, V8 12.x/13.x, libuv 1.x), wikilinks densos para `[[Node.js]]` (tronco), `[[JavaScript Fundamentals]]`, e seção "Em entrevista" para preparação internacional. Ao fim, tronco é podado e MOC central atualizado.

**Tech Stack:** Markdown + Obsidian Flavored Markdown (wikilinks, callouts, dataview), Quartz para publicação no site público (josenaldo.github.io). Sem código a executar como sistema — code samples didáticos que podem ser validados em script standalone via `node script.js` ou `node --experimental-strip-types script.ts` quando útil.

---

## ⚠️ Restrição absoluta — fabricação

A memória [Nunca inventar dados sobre o usuário](/home/josenaldo/.claude/projects/-home-josenaldo-repos-personal-codex-technomanticus/memory/feedback_no_fabrication.md) é regra inegociável. **Nenhuma nota pode atribuir ao autor experiências profissionais, projetos, clientes, métricas ou casos não-vividos.**

A seção "Na prática" de cada nota usa:

- "Padrão observado em libs do ecossistema (Express, Fastify, NestJS)"
- "Caso típico em microserviços I/O-bound"
- "Armadilha comum reportada na comunidade"
- Citações com fonte verificável (docs oficiais, talks identificadas, repos públicos)
- Hipotéticos explícitos ("Imagine um servidor que processa uploads de imagens...")

Quando faltar contexto factual, **PERGUNTAR antes de escrever** — nunca preencher com plausibilidade.

---

## File Structure

13 arquivos novos em `03-Dominios/Node/Runtime e Event Loop/`:

```
03-Dominios/Node/Runtime e Event Loop/
├── Runtime e Event Loop.md                                          # MOC (Task 1)
├── 01 - Single-thread e non-blocking I-O.md                         # Task 2
├── 02 - V8, libuv e thread pool.md                                  # Task 3
├── 03 - Call stack, heap e queues.md                                # Task 4
├── 04 - As fases do event loop.md                                   # Task 5
├── 05 - Microtasks - nextTick, queueMicrotask, Promise.then.md      # Task 6
├── 06 - Macrotasks e timers - setTimeout, setInterval, setImmediate.md  # Task 7
├── 07 - I-O assíncrono - kernel vs thread pool.md                   # Task 8
├── 08 - Promises por dentro.md                                      # Task 9
├── 09 - async-await - o que é, o que não é.md                       # Task 10
├── 10 - Bloqueio do event loop - sintomas e causas.md               # Task 11
├── 11 - Diagnóstico do event loop.md                                # Task 12
└── 12 - Armadilhas, regras práticas, cheatsheet.md                  # Task 13
```

**Final integration (Task 14, 15, 16):**
- Pass final no MOC inserindo todos os wikilinks + dataview
- Poda do tronco `03-Dominios/JavaScript/Backend/Node.js.md`
- Atualização do MOC central `03-Dominios/Node/index.md` + verificação de build do Quartz

---

## Template padrão (definido uma vez, aplicado a todas as 12 notas)

```markdown
---
title: "<título sem prefixo numérico>"
created: 2026-05-07
updated: 2026-05-07
type: concept
status: seedling
publish: true
tags:
  - node
  - event-loop
  - <tag específica: microtask, timer, promise, blocking, etc>
aliases:
  - <opcional: alternativas naturais de busca>
---

# <Título>

> [!abstract] TL;DR
> <2-4 linhas em PT-BR direto. Define o conceito-chave + a regra prática + por que importa.>

## O que é

<1-3 parágrafos definindo o conceito da nota. Pressupõe leitura de [[Node.js]] (tronco) ou consulta paralela.>

## Por que importa

<O problema que isso resolve no dia a dia. Onde o desenvolvedor "trava" sem esse conhecimento. Casos de uso reais.>

## Como funciona

<Aprofundamento técnico com code samples em JS ou TS. Mostrar o pattern, depois variações. Edge cases.>

## Na prática

<Exemplo realista. Sem fabricar experiência do autor — usar "padrão observado em X", "lib Y faz isso", hipotéticos explícitos.>

## Armadilhas

<Gotchas específicos. O que erra normalmente, mensagens de erro confusas, anti-patterns comuns. Mínimo 2 itens.>

## Em entrevista

<Frase pronta em inglês para explicar o conceito. Vocabulário-chave (PT → EN). Pergunta típica + resposta defensiva.>

## Veja também

- [[Outra nota da trilha]] — relação
- [[Node.js]] — tronco
- [[JavaScript Fundamentals]] — quando aplicável
```

### Variações permitidas

- **Nota 12 (Armadilhas, cheatsheet):** estrutura tópica (lista numerada de armadilhas + tabelas + decision tree), não narrativa "Como funciona"
- **MOC (`Runtime e Event Loop.md`):** estrutura própria (abertura + Comece por aqui + Rotas alternativas + dataview), `type: moc`

### Critérios de qualidade (rubrica aplicada por nota)

- [ ] TL;DR em callout `[!abstract]`, 2-4 linhas, compreensível em <30s
- [ ] 2+ wikilinks pra outras notas do galho + 1+ wikilink pra `[[Node.js]]` (tronco) ou `[[JavaScript Fundamentals]]`
- [ ] 3+ code samples em JS ou TS (notas 01, 03 podem ter menos se forem puramente conceituais)
- [ ] Seção "Em entrevista" com pelo menos 1 frase pronta em inglês + vocabulário-chave (mínimo 3 termos PT→EN)
- [ ] Seção "Armadilhas" com pelo menos 2 armadilhas concretas
- [ ] Frontmatter completo (`publish: true`, `status: seedling`, tags `[node, event-loop, <específica>]`)
- [ ] Versões assumidas declaradas se relevante (Node 22 LTS / 24)
- [ ] PT-BR natural; termos técnicos em inglês mantidos (event loop, microtask, etc.)
- [ ] **Zero atribuição de experiência pessoal ao autor** (regra absoluta)
- [ ] Nenhuma alegação técnica não-trivial sem fonte ou code sample que comprove

---

## Bibliografia centralizada (consulta rápida durante a escrita)

### Referências canônicas

- **Node.js docs — Event Loop:** `https://nodejs.org/en/learn/asynchronous-work/event-loop-timers-and-nexttick`
- **Node.js docs — Don't Block the Event Loop:** `https://nodejs.org/en/learn/asynchronous-work/dont-block-the-event-loop`
- **libuv design:** `https://docs.libuv.org/en/v1.x/design.html`
- **V8 Blog:** `https://v8.dev/blog`

### Talks e artigos clássicos

- **Bert Belder — Event Loop:** `https://www.youtube.com/watch?v=PNa9OMajw9w`
- **Daniel Khan — Node.js Event Loop:** `https://medium.com/@danielkhan/the-node-js-event-loop-72ed5e3f5e0a`
- **Bytearcher — Parallel vs Async:** `https://bytearcher.com/articles/parallel-vs-asynchronous-in-node.js/`
- **Matteo Collina (busca dirigida):** `https://www.youtube.com/results?search_query=matteo+collina+event+loop`

### Diagnóstico

- **perf_hooks docs:** `https://nodejs.org/api/perf_hooks.html#perf_hooksmonitoreventloopdelayoptions`
- **clinic.js Doctor:** `https://clinicjs.org/doctor/`
- **clinic.js Bubbleprof:** `https://clinicjs.org/bubbleprof/`
- **autocannon:** `https://github.com/mcollina/autocannon`

### Notas no vault (referências paralelas)

- `03-Dominios/JavaScript/Backend/Node.js.md` — tronco a ser podado
- `03-Dominios/Node/index.md` — MOC central a ser atualizado
- `03-Dominios/JavaScript/Core/JavaScript Fundamentals.md` (verificar caminho exato) — event loop básico do JS, pré-requisito
- `03-Dominios/JavaScript/Core/TypeScript.md` (verificar caminho exato) — quando code sample usar TS

### A buscar conforme necessidade

- Posts atuais sobre `process.nextTick` vs `queueMicrotask` em Node 24
- Material sobre Permission Model do Node 20+ tocando event loop indiretamente
- Anna Henningsen (addaleax) posts/talks sobre internals
- Issues do repo `nodejs/node` documentando mudanças entre versões

---

## Task 0: Pré-flight

**Files:**
- Create: `03-Dominios/Node/Runtime e Event Loop/` (diretório)

- [ ] **Step 1: Criar o diretório**

```bash
mkdir -p "03-Dominios/Node/Runtime e Event Loop"
```

Verificar com:

```bash
ls -la "03-Dominios/Node/Runtime e Event Loop"
```

Esperado: diretório vazio.

- [ ] **Step 2: Confirmar memória de no-fabrication carregada**

Ler:

```bash
cat /home/josenaldo/.claude/projects/-home-josenaldo-repos-personal-codex-technomanticus/memory/MEMORY.md | grep -i "fabrica\|invent"
```

Esperado: ao menos uma linha referenciando `feedback_no_fabrication.md`. Se não estiver, abortar e pedir reload.

- [ ] **Step 3: Sanity check do tronco**

Ler `03-Dominios/JavaScript/Backend/Node.js.md` e confirmar que existem as seções a podar:

- "Arquitetura"
- "Single-threaded com non-blocking I/O"
- "Event loop phases — detalhado"
- "Event loop blocking" (em Troubleshooting)
- "Armadilhas comuns"

Se alguma estiver com nome diferente, anotar o nome exato pra usar na Task 15.

- [ ] **Step 4: Verificar caminhos exatos das notas-mãe**

Buscar:

```bash
find /home/josenaldo/repos/personal/codex-technomanticus -name "JavaScript Fundamentals*" -type f
find /home/josenaldo/repos/personal/codex-technomanticus -name "TypeScript*" -type f -path "*JavaScript*"
```

Anotar caminhos exatos pra usar nos wikilinks `[[...]]`.

- [ ] **Step 5: Sanity check das fontes-âncora**

Disparar WebFetch em paralelo para as 3 fontes mais críticas:

```
WebFetch: https://nodejs.org/en/learn/asynchronous-work/event-loop-timers-and-nexttick
WebFetch: https://nodejs.org/en/learn/asynchronous-work/dont-block-the-event-loop
WebFetch: https://docs.libuv.org/en/v1.x/design.html
```

Confirmar que estão acessíveis e capturar o conteúdo essencial. Se alguma estiver fora do ar, registrar e usar fontes alternativas (V8 blog, talks).

- [ ] **Step 6: Commit pré-flight**

```bash
git add -A
git commit -m "feat(node-event-loop): create directory for Runtime e Event Loop sub-trail"
```

(Sem Co-Authored-By Claude — regra do usuário.)

---

## Task 1: MOC esqueleto

**Files:**
- Create: `03-Dominios/Node/Runtime e Event Loop/Runtime e Event Loop.md`

- [ ] **Step 1: Criar o MOC esqueleto**

Criar `03-Dominios/Node/Runtime e Event Loop/Runtime e Event Loop.md`:

```markdown
---
title: "Runtime e Event Loop"
created: 2026-05-07
updated: 2026-05-07
type: moc
status: seedling
publish: true
tags:
  - node
  - event-loop
  - moc
aliases:
  - Event Loop
  - Node Runtime
  - Galho 1 - Runtime
---

# Runtime e Event Loop

> [!abstract] TL;DR
> Galho 1 da trilha Node Senior. Cobre o "motor" do Node — single-thread, V8, libuv, fases do event loop, microtasks/macrotasks, promises por dentro, async/await desmistificado, bloqueio do loop e diagnóstico. Pré-requisito de todos os outros galhos (paralelismo, streams, frameworks, observability, segurança).

## Sobre este galho

(introdução curta — preencher na Task 14)

## Comece por aqui — trilha completa (12 notas)

### Bloco A — Mental model

1. [[01 - Single-thread e non-blocking I-O]]
2. [[02 - V8, libuv e thread pool]]
3. [[03 - Call stack, heap e queues]]

### Bloco B — Event loop deep dive

4. [[04 - As fases do event loop]]
5. [[05 - Microtasks - nextTick, queueMicrotask, Promise.then]]
6. [[06 - Macrotasks e timers - setTimeout, setInterval, setImmediate]]
7. [[07 - I-O assíncrono - kernel vs thread pool]]

### Bloco C — async/await em profundidade

8. [[08 - Promises por dentro]]
9. [[09 - async-await - o que é, o que não é]]

### Bloco D — Bloqueio e diagnóstico

10. [[10 - Bloqueio do event loop - sintomas e causas]]
11. [[11 - Diagnóstico do event loop]]

### Bloco E — Fechamento

12. [[12 - Armadilhas, regras práticas, cheatsheet]]

## Rotas alternativas

### Rota entrevista internacional

01 → 03 → 04 → 05 → 06 → 09 → 10. Foco em "explicar o motor pra entrevistador".

### Rota debugging em produção

01 → 04 → 07 → 10 → 11. Foco em "minha app tá lenta, por quê?".

### Rota async/await

03 → 05 → 08 → 09. Foco em entender o "porquê" das promises.

## Todas as notas

```dataview
TABLE status, updated
FROM "03-Dominios/Node/Runtime e Event Loop"
WHERE type = "concept"
SORT file.name ASC
```

## Veja também

- [[03-Dominios/Node/index|Node.js (MOC central)]]
- [[Node.js]] — tronco (deep dive panorâmico)
- [[JavaScript Fundamentals]] — event loop básico do JS
```

- [ ] **Step 2: Verificar frontmatter e estrutura**

Confirmar:
- `type: moc`
- `publish: true`
- Todas as 12 notas listadas em ordem
- 4 rotas alternativas presentes
- Dataview com SORT
- Wikilinks pro MOC central e tronco

- [ ] **Step 3: Commit**

```bash
git add "03-Dominios/Node/Runtime e Event Loop/Runtime e Event Loop.md"
git commit -m "feat(node-event-loop): add MOC skeleton for Runtime e Event Loop branch"
```

---

## Task 2: Nota 01 — Single-thread e non-blocking I/O

**Files:**
- Create: `03-Dominios/Node/Runtime e Event Loop/01 - Single-thread e non-blocking I-O.md`

**Conteúdo-chave do spec (seção 5, Bloco A):**

> Por que Node é single-threaded mas atende milhares de conexões. A intuição: I/O é delegado, código JS roda em uma thread só. Comparação com modelo thread-per-request (Apache, Tomcat tradicional). Onde isso ganha (I/O-bound) e onde perde (CPU-bound).

- [ ] **Step 1: Pesquisa-âncora**

WebFetch em paralelo:

```
WebFetch: https://nodejs.org/en/learn/asynchronous-work/event-loop-timers-and-nexttick
WebFetch: https://bytearcher.com/articles/parallel-vs-asynchronous-in-node.js/
```

Capturar: definição oficial de "single-threaded with non-blocking I/O", comparação com modelos blocking, casos de uso onde Node ganha/perde.

- [ ] **Step 2: Criar o arquivo com frontmatter + esqueleto**

Criar `03-Dominios/Node/Runtime e Event Loop/01 - Single-thread e non-blocking I-O.md` com:

```yaml
---
title: "Single-thread e non-blocking I/O"
created: 2026-05-07
updated: 2026-05-07
type: concept
status: seedling
publish: true
tags:
  - node
  - event-loop
  - mental-model
  - non-blocking
aliases:
  - Single-threaded
  - Non-blocking I/O
---
```

- [ ] **Step 3: Escrever a nota completa**

Cobrir:

- **TL;DR:** Node é single-thread mas atende milhares de conexões porque I/O é delegado ao OS. A thread JS só executa código JS — o I/O acontece em paralelo.
- **O que é:** definição precisa de single-threaded (uma thread executa JS), non-blocking I/O (chamadas de I/O retornam imediatamente, callback é enfileirado quando completam).
- **Por que importa:** desfaz a confusão "como Node aguenta requisições?". Esclarece o trade-off central de Node (I/O-bound favorece, CPU-bound prejudica).
- **Como funciona:** code sample com `fs.readFile` mostrando que o `console.log` posterior imprime antes do callback. Diagrama em ASCII: thread JS → bindings → libuv → OS → callback de volta.
- **Na prática:** comparação com modelo thread-per-request (Apache prefork, Tomcat default) — quando cada modelo ganha. Limite prático (cada thread em Java consome ~512KB de stack; uma conexão em Node consome bytes).
- **Armadilhas:** (1) achar que `async` cria thread (preview da nota 09), (2) assumir que TODO I/O é não-bloqueante (sync APIs como `readFileSync` existem e travam tudo).
- **Em entrevista:** frase pronta: "Node.js uses a single-threaded event loop with non-blocking I/O. The JS thread never blocks on I/O — it delegates to the OS via libuv and registers a callback. This is what allows a single process to handle thousands of concurrent connections without thread-per-request overhead." Vocabulário: thread única (single thread), I/O não-bloqueante (non-blocking I/O), modelo orientado a eventos (event-driven model), conexões concorrentes (concurrent connections).
- **Veja também:** `[[02 - V8, libuv e thread pool]]`, `[[09 - async-await - o que é, o que não é]]`, `[[10 - Bloqueio do event loop - sintomas e causas]]`, `[[Node.js]]` (tronco), `[[JavaScript Fundamentals]]`.

Tamanho-alvo: 200-400 linhas.

- [ ] **Step 4: Verificar rubrica**

Checklist:

```
[ ] TL;DR no callout [!abstract]
[ ] 4+ wikilinks (3 da trilha + tronco + fundamentals)
[ ] 2+ code samples (fs.readFile non-blocking + comparação com sync)
[ ] Em entrevista: 1 frase em inglês + 4 termos de vocabulário
[ ] Armadilhas: 2 itens
[ ] Frontmatter completo
[ ] PT-BR natural, termos técnicos em inglês
[ ] Sem fabricação de experiência do autor
```

- [ ] **Step 5: Commit**

```bash
git add "03-Dominios/Node/Runtime e Event Loop/01 - Single-thread e non-blocking I-O.md"
git commit -m "feat(node-event-loop): add note 01 — Single-thread e non-blocking I/O"
```

---

## Task 3: Nota 02 — V8, libuv e thread pool

**Files:**
- Create: `03-Dominios/Node/Runtime e Event Loop/02 - V8, libuv e thread pool.md`

**Conteúdo-chave do spec:**

> Os 3 componentes: V8 (engine JS, JIT), libuv (event loop + thread pool C), Node bindings (C++ glue). Tamanho default do thread pool (4 threads) e `UV_THREADPOOL_SIZE`. O que usa o pool: filesystem (parte), DNS (`dns.lookup`), crypto, compression. O que não usa: net/http (vai direto pro epoll/kqueue).

- [ ] **Step 1: Pesquisa-âncora**

WebFetch em paralelo:

```
WebFetch: https://docs.libuv.org/en/v1.x/design.html
WebFetch: https://nodejs.org/api/cli.html#uv_threadpool_sizesize
```

Capturar: arquitetura libuv (event loop + thread pool), default size, quem usa o pool.

- [ ] **Step 2: Criar arquivo + frontmatter**

```yaml
---
title: "V8, libuv e thread pool"
created: 2026-05-07
updated: 2026-05-07
type: concept
status: seedling
publish: true
tags:
  - node
  - event-loop
  - mental-model
  - libuv
  - v8
aliases:
  - libuv
  - Thread pool
---
```

- [ ] **Step 3: Escrever a nota completa**

Cobrir:

- **TL;DR:** Node é a soma de V8 (motor JS) + libuv (lib C com event loop e thread pool) + bindings (C++). O thread pool tem 4 threads por default — só algumas APIs (file I/O, DNS lookup, crypto, compression) o usam; net/http vai direto pro kernel.
- **O que é:** 3 componentes detalhados. V8 = JIT compiler do Chrome. libuv = abstração cross-platform de event loop, file I/O, networking, threads. Bindings = ponte C++ entre JS e libuv/V8.
- **Por que importa:** entender que existem **dois lugares onde paralelismo acontece** — kernel (epoll/kqueue/IOCP, infinito) e thread pool (limitado, default 4). Confusão clássica leva a tunings errados.
- **Como funciona:** diagrama ASCII das camadas. Code sample: `UV_THREADPOOL_SIZE=8 node app.js`. Tabela: API → usa pool? → por quê.
- **Na prática:** caso típico — app que faz muito `crypto.pbkdf2` em paralelo satura pool default; subir `UV_THREADPOOL_SIZE` resolve. Hipotético explícito.
- **Armadilhas:** (1) `UV_THREADPOOL_SIZE` precisa ser setada **antes** de qualquer require que use o pool (ex: antes de `require('crypto')`), senão é ignorada nessa primeira chamada; (2) achar que aumentar o pool sempre ajuda (mais threads = mais context switching, ponto de retorno decrescente).
- **Em entrevista:** "Node is composed of V8 for JavaScript execution, libuv for async I/O and event loop, and a small set of C++ bindings to glue them. libuv has a thread pool — default size 4, configurable via UV_THREADPOOL_SIZE — used for file system, DNS lookup, crypto, and compression. Network I/O does not use the pool; it goes directly to the OS via epoll, kqueue, or IOCP." Vocabulário: motor (engine), pool de threads (thread pool), camada de ligação (binding layer), cross-platform.
- **Veja também:** `[[01 - Single-thread e non-blocking I-O]]`, `[[03 - Call stack, heap e queues]]`, `[[07 - I-O assíncrono - kernel vs thread pool]]`, `[[Node.js]]` (tronco).

Tamanho-alvo: 250-450 linhas.

- [ ] **Step 4: Verificar rubrica**

Checklist (como na Task 2).

- [ ] **Step 5: Commit**

```bash
git add "03-Dominios/Node/Runtime e Event Loop/02 - V8, libuv e thread pool.md"
git commit -m "feat(node-event-loop): add note 02 — V8, libuv e thread pool"
```

---

## Task 4: Nota 03 — Call stack, heap e queues

**Files:**
- Create: `03-Dominios/Node/Runtime e Event Loop/03 - Call stack, heap e queues.md`

**Conteúdo-chave do spec:**

> Call stack (frames de execução, V8 stack size, `RangeError: Maximum call stack`), heap (objetos, GC, gerações), microtask queue, macrotask queue (callback queue). Como uma operação async navega entre eles. Por que a stack precisa esvaziar antes do event loop avançar.

- [ ] **Step 1: Pesquisa-âncora**

WebFetch:

```
WebFetch: https://v8.dev/blog/trash-talk
```

Capturar: gerações do GC do V8, conceito de call stack do V8.

- [ ] **Step 2: Criar arquivo + frontmatter**

```yaml
---
title: "Call stack, heap e queues"
created: 2026-05-07
updated: 2026-05-07
type: concept
status: seedling
publish: true
tags:
  - node
  - event-loop
  - mental-model
  - call-stack
  - heap
aliases:
  - Call stack
  - Heap
  - Microtask queue
  - Macrotask queue
---
```

- [ ] **Step 3: Escrever a nota completa**

Cobrir:

- **TL;DR:** A thread JS tem 4 estruturas em runtime: call stack (frames de função), heap (objetos), microtask queue (Promises, nextTick) e macrotask queue (timers, I/O callbacks). O event loop só avança quando a stack esvazia.
- **O que é:** definir cada estrutura. Call stack: frames LIFO de chamadas de função. Heap: pool de objetos JS (GC gerenciado). Microtask queue: fila de microtasks pendentes. Macrotask queue: fila de callbacks de I/O e timers (também chamada "callback queue" ou "task queue").
- **Por que importa:** sem entender que **a stack precisa esvaziar antes do loop avançar**, é impossível entender por que `process.nextTick` em recursão trava o programa. Também é a base pra entender RangeError.
- **Como funciona:** code sample mostrando call stack overflow (`function f() { f(); } f();`). Code sample mostrando ordem de execução: sync code → microtasks → macrotasks. Diagrama ASCII das 4 estruturas.
- **Na prática:** investigar um stack trace típico em Node. Como `console.trace()` mostra a stack atual. Como o tamanho default da stack do V8 (`--stack-size`) afeta apps com recursão profunda.
- **Armadilhas:** (1) recursão sem case-base → RangeError; (2) achar que microtasks "rodam em background" — não, rodam na mesma thread, só em momento diferente; (3) confundir heap (objetos) com stack (frames).
- **Em entrevista:** "The JS thread has four runtime structures: the call stack of execution frames, the heap of objects managed by V8's garbage collector, the microtask queue for Promises and process.nextTick, and the macrotask queue for timer and I/O callbacks. The event loop can only pick up work from the queues when the call stack is empty — that's why a synchronous infinite loop blocks everything, including microtasks." Vocabulário: pilha de chamadas (call stack), monte (heap), coletor de lixo (garbage collector), fila de microtarefas (microtask queue).
- **Veja também:** `[[02 - V8, libuv e thread pool]]`, `[[04 - As fases do event loop]]`, `[[05 - Microtasks - nextTick, queueMicrotask, Promise.then]]`, `[[Node.js]]`, `[[JavaScript Fundamentals]]`.

Tamanho-alvo: 250-450 linhas.

- [ ] **Step 4: Verificar rubrica**

- [ ] **Step 5: Commit**

```bash
git add "03-Dominios/Node/Runtime e Event Loop/03 - Call stack, heap e queues.md"
git commit -m "feat(node-event-loop): add note 03 — Call stack, heap e queues"
```

---

## Task 5: Nota 04 — As fases do event loop

**Files:**
- Create: `03-Dominios/Node/Runtime e Event Loop/04 - As fases do event loop.md`

**Conteúdo-chave do spec:**

> As 6 fases: timers, pending callbacks, idle/prepare (interno), poll, check, close callbacks. O que cada uma faz e em que ordem. Diagrama. Onde microtasks rodam (entre cada fase). Por que `poll` é especial (pode bloquear).

- [ ] **Step 1: Pesquisa-âncora**

WebFetch:

```
WebFetch: https://nodejs.org/en/learn/asynchronous-work/event-loop-timers-and-nexttick
WebFetch: https://docs.libuv.org/en/v1.x/design.html
```

Capturar: descrição oficial de cada fase, ordem, comportamento de poll.

- [ ] **Step 2: Criar arquivo + frontmatter**

```yaml
---
title: "As fases do event loop"
created: 2026-05-07
updated: 2026-05-07
type: concept
status: seedling
publish: true
tags:
  - node
  - event-loop
  - libuv
  - phases
aliases:
  - Event loop phases
  - Fases do event loop
---
```

- [ ] **Step 3: Escrever a nota completa**

Cobrir:

- **TL;DR:** O event loop tem 6 fases (timers, pending callbacks, idle/prepare, poll, check, close callbacks), executadas em ordem fixa. Entre cada fase, microtasks são drenadas. A fase `poll` pode bloquear esperando I/O.
- **O que é:** cada fase, em ordem, com 1-2 frases:
  - **timers** — executa callbacks de `setTimeout`/`setInterval` que estão expirados
  - **pending callbacks** — callbacks de I/O que foram diferidos (ex: erros de TCP)
  - **idle, prepare** — interno, libuv usa
  - **poll** — pega novos eventos de I/O (epoll/kqueue/IOCP). Pode bloquear até timer mais próximo expirar
  - **check** — executa callbacks de `setImmediate`
  - **close callbacks** — `socket.on('close', ...)`, etc.
- **Por que importa:** sem saber as fases, comportamentos como "`setImmediate` roda antes de `setTimeout(fn, 0)` quando estamos em I/O" parecem mágica. Também explica por que `process.nextTick` é diferente (microtask, não fase).
- **Como funciona:** diagrama ASCII completo (cópia do tronco original já tem um bom). Code sample: ordem de execução em I/O context (`fs.readFile` callback → `setTimeout(fn, 0)` vs `setImmediate(fn)`).
- **Na prática:** comportamento do `poll` quando não há I/O agendado nem timer pendente: o loop **encerra**. Por isso `setInterval` mantém o programa vivo. Caso típico: server HTTP — `poll` fica esperando conexões, loop nunca termina.
- **Armadilhas:** (1) achar que microtasks rodam **entre tasks da mesma fase** — não, rodam **entre fases**; (2) confundir "task queue" (callback queue da fase poll) com macrotask queue genérica; (3) `setImmediate` em fora-de-I/O não é determinístico vs `setTimeout(fn, 0)`.
- **Em entrevista:** "The Node.js event loop runs in six phases per iteration: timers, pending callbacks, idle/prepare, poll, check, and close callbacks. The poll phase is the most interesting — it picks up new I/O events from the OS, and it can block waiting for I/O until the nearest timer is due. Between every phase, microtasks are drained — that's why `process.nextTick` and Promise callbacks are higher priority than any timer or I/O callback." Vocabulário: fase (phase), iteração (iteration), drenar microtasks (drain microtasks), bloquear esperando I/O (block waiting for I/O).
- **Veja também:** `[[03 - Call stack, heap e queues]]`, `[[05 - Microtasks - nextTick, queueMicrotask, Promise.then]]`, `[[06 - Macrotasks e timers - setTimeout, setInterval, setImmediate]]`, `[[07 - I-O assíncrono - kernel vs thread pool]]`, `[[Node.js]]`.

Tamanho-alvo: 400-600 linhas (nota central, justifica densidade).

- [ ] **Step 4: Verificar rubrica**

- [ ] **Step 5: Commit**

```bash
git add "03-Dominios/Node/Runtime e Event Loop/04 - As fases do event loop.md"
git commit -m "feat(node-event-loop): add note 04 — As fases do event loop"
```

---

## Task 6: Nota 05 — Microtasks (nextTick, queueMicrotask, Promise.then)

**Files:**
- Create: `03-Dominios/Node/Runtime e Event Loop/05 - Microtasks - nextTick, queueMicrotask, Promise.then.md`

**Conteúdo-chave do spec:**

> A hierarquia: `process.nextTick` (prioridade máxima, antes do próximo iteration) > `queueMicrotask` ≈ `Promise.then` (entre fases). Tabela comparativa. Por que recursão em `nextTick` bloqueia o loop ("nextTick starvation"). Quando usar cada um. `process.nextTick` é Node-específico; `queueMicrotask` é padrão.

- [ ] **Step 1: Pesquisa-âncora**

WebFetch:

```
WebFetch: https://nodejs.org/en/learn/asynchronous-work/event-loop-timers-and-nexttick
WebFetch: https://nodejs.org/api/process.html#processnexttickcallback-args
```

- [ ] **Step 2: Criar arquivo + frontmatter**

```yaml
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
```

- [ ] **Step 3: Escrever a nota completa**

Cobrir:

- **TL;DR:** Microtasks rodam entre fases do event loop, antes da próxima fase. Hierarquia: `process.nextTick` > `queueMicrotask` ≈ `Promise.then`. Recursão em `nextTick` bloqueia o loop ("starvation"). `nextTick` é Node-específico; `queueMicrotask` é padrão da web.
- **O que é:** definir microtask. Listar as 3 APIs: `process.nextTick(cb)`, `queueMicrotask(cb)`, `Promise.resolve().then(cb)`. Explicar que `nextTick` tem prioridade absoluta dentro de microtasks (drena toda a `nextTick` queue antes de qualquer outra microtask).
- **Por que importa:** controla **ordem de execução fina** — quando você precisa que algo aconteça "depois desta tick mas antes de qualquer I/O", microtasks são a ferramenta. Também é fonte clássica de bugs ("por que meu callback rodou antes do esperado?").
- **Como funciona:** code samples curtos e claros:
  1. `setTimeout(() => log('timer'), 0); Promise.resolve().then(() => log('promise')); process.nextTick(() => log('nextTick'));` — ordem: nextTick → promise → timer
  2. Recursão de `nextTick` que bloqueia: `function loop() { process.nextTick(loop); } loop();` — programa nunca avança
  3. `queueMicrotask` vs `Promise.resolve().then` — equivalentes em ordem; diferenças sutis em error handling
- Tabela comparativa: API | onde roda | prioridade | padrão (Node ou web)
- **Na prática:** uso legítimo de `nextTick`: deferir um callback síncrono pra que os listeners que serão registrados nas próximas linhas sejam considerados (pattern em libs que emitem eventos no constructor). Caso comum reportado na comunidade.
- **Armadilhas:** (1) `nextTick` recursivo trava o loop e provoca timeouts em outras requests; (2) `queueMicrotask` em recursão também trava; (3) microtask que lança erro não capturado vira `unhandledRejection` (se Promise) ou `uncaughtException` (se sync); (4) achar que `setImmediate` é "imediato" — não é, ele é macrotask na fase check, sempre depois das microtasks.
- **Em entrevista:** "Node has three microtask APIs with a strict priority order: `process.nextTick` runs first — it has its own queue that's drained before any other microtask. Then `queueMicrotask` and `Promise.then` are interleaved in the standard microtask queue. Microtasks run between every event loop phase, so they're higher priority than any timer or I/O callback. The danger of `process.nextTick` is recursion — a callback that schedules another `nextTick` will starve the event loop, since the queue is drained completely before phases advance." Vocabulário: fila de microtarefas (microtask queue), prioridade (priority), inanição da fila (queue starvation), API específica de Node (Node-specific API).
- **Veja também:** `[[04 - As fases do event loop]]`, `[[06 - Macrotasks e timers - setTimeout, setInterval, setImmediate]]`, `[[08 - Promises por dentro]]`, `[[Node.js]]`.

Tamanho-alvo: 300-500 linhas.

- [ ] **Step 4: Verificar rubrica**

- [ ] **Step 5: Commit**

```bash
git add "03-Dominios/Node/Runtime e Event Loop/05 - Microtasks - nextTick, queueMicrotask, Promise.then.md"
git commit -m "feat(node-event-loop): add note 05 — Microtasks"
```

---

## Task 7: Nota 06 — Macrotasks e timers

**Files:**
- Create: `03-Dominios/Node/Runtime e Event Loop/06 - Macrotasks e timers - setTimeout, setInterval, setImmediate.md`

**Conteúdo-chave do spec:**

> `setTimeout(fn, 0)` mínimo de 1ms. `setImmediate` na fase `check`. `setImmediate` vs `setTimeout(fn, 0)` — em I/O é determinístico (`setImmediate` ganha), fora não. Caveat de `setInterval` com handler que demora. `timers/promises` para sleep idiomático.

- [ ] **Step 1: Pesquisa-âncora**

WebFetch:

```
WebFetch: https://nodejs.org/api/timers.html
WebFetch: https://nodejs.org/api/timers.html#timerspromisessettimeoutdelay-value-options
```

- [ ] **Step 2: Criar arquivo + frontmatter**

```yaml
---
title: "Macrotasks e timers: setTimeout, setInterval, setImmediate"
created: 2026-05-07
updated: 2026-05-07
type: concept
status: seedling
publish: true
tags:
  - node
  - event-loop
  - timer
  - macrotask
  - setimmediate
aliases:
  - Timers
  - setImmediate
  - setTimeout
---
```

- [ ] **Step 3: Escrever a nota completa**

Cobrir:

- **TL;DR:** `setTimeout`/`setInterval` rodam na fase `timers`. `setImmediate` roda na fase `check`. Em contexto de I/O, `setImmediate` é determinístico (ganha de `setTimeout(fn, 0)`); fora, ordem é imprevisível. Use `timers/promises` para sleep idiomático.
- **O que é:** as 3 APIs detalhadas. `setTimeout(fn, ms)` — agenda na fila de timers. `setInterval(fn, ms)` — repete. `setImmediate(fn)` — agenda na fase check do próximo iteration. `timers/promises` — versões Promise-based.
- **Por que importa:** entender ordem de execução é crítico em código que mistura timers e I/O. `setImmediate` ser determinístico em I/O é o que permite escrever "execute na próxima tick após este callback" de forma confiável.
- **Como funciona:** code samples:
  1. `setTimeout(fn, 0)` mínimo na prática — V8 força >=1ms (alguns runtimes mais)
  2. Em contexto I/O: `fs.readFile(...., () => { setTimeout(fn, 0); setImmediate(fn); })` — `setImmediate` sempre primeiro
  3. Fora de I/O: `setTimeout(fn, 0); setImmediate(fn)` — ordem depende de timing do registro
  4. `setInterval` com handler que demora 200ms e `interval` de 100ms — não há "catch up", próximo callback agendado normalmente; podem se acumular e travar o loop
  5. `import { setTimeout } from 'node:timers/promises'; await setTimeout(1000);` — sleep idiomático
- Tabela: API | fase | repete? | retorno
- **Na prática:** preferência por `setImmediate(fn)` sobre `setTimeout(fn, 0)` quando a intenção é "depois desta tick" — explicito e determinístico. `setInterval` é raramente correto em produção; preferir loop com `setTimeout` recursivo + cálculo de drift. Padrão observado em libs.
- **Armadilhas:** (1) `setInterval` reentrante (handler demora > intervalo); (2) acreditar que `setTimeout(fn, 0)` é instantâneo; (3) usar `setTimeout` para sleep em código async (use `timers/promises`); (4) timer com closure pesado vaza memória se nunca limpo (`clearTimeout`/`clearInterval`).
- **Em entrevista:** "`setTimeout` and `setInterval` run in the timers phase; `setImmediate` runs in the check phase. The interesting trivia: in an I/O callback, `setImmediate` always runs before `setTimeout(fn, 0)` — it's deterministic, because the loop is in the poll phase and the next phase is check. Outside I/O, the order is non-deterministic. For modern code, prefer `setImmediate` when you want 'next tick after this callback', and use `node:timers/promises` for awaitable sleeps." Vocabulário: temporizador (timer), fase de timers (timers phase), fase check (check phase), reentrância (reentrancy), drift do timer.
- **Veja também:** `[[04 - As fases do event loop]]`, `[[05 - Microtasks - nextTick, queueMicrotask, Promise.then]]`, `[[09 - async-await - o que é, o que não é]]`, `[[Node.js]]`.

Tamanho-alvo: 300-500 linhas.

- [ ] **Step 4: Verificar rubrica**

- [ ] **Step 5: Commit**

```bash
git add "03-Dominios/Node/Runtime e Event Loop/06 - Macrotasks e timers - setTimeout, setInterval, setImmediate.md"
git commit -m "feat(node-event-loop): add note 06 — Macrotasks e timers"
```

---

## Task 8: Nota 07 — I/O assíncrono (kernel vs thread pool)

**Files:**
- Create: `03-Dominios/Node/Runtime e Event Loop/07 - I-O assíncrono - kernel vs thread pool.md`

**Conteúdo-chave do spec:**

> Network I/O (`net`, `http`, `https`) usa **epoll/kqueue/IOCP do OS** — não consome thread do pool. File I/O (`fs`) usa o pool. DNS (`dns.lookup`) usa o pool, mas `dns.resolve` não. Implicação prática: pool exausto em apps file-heavy ou crypto-heavy.

- [ ] **Step 1: Pesquisa-âncora**

WebFetch:

```
WebFetch: https://docs.libuv.org/en/v1.x/threadpool.html
WebFetch: https://nodejs.org/api/dns.html#dnslookuphostname-options-callback
WebFetch: https://bytearcher.com/articles/parallel-vs-asynchronous-in-node.js/
```

- [ ] **Step 2: Criar arquivo + frontmatter**

```yaml
---
title: "I/O assíncrono: kernel vs thread pool"
created: 2026-05-07
updated: 2026-05-07
type: concept
status: seedling
publish: true
tags:
  - node
  - event-loop
  - io
  - libuv
  - thread-pool
aliases:
  - epoll
  - kqueue
  - dns.lookup
---
```

- [ ] **Step 3: Escrever a nota completa**

Cobrir:

- **TL;DR:** Nem todo I/O passa pelo thread pool. Network I/O (TCP, HTTP) usa **kernel async** (epoll/kqueue/IOCP) — não consome thread. File I/O (`fs`), DNS lookup (`dns.lookup`), crypto e zlib usam o **thread pool de 4** — podem saturar.
- **O que é:** explicar epoll (Linux), kqueue (macOS/BSD), IOCP (Windows) como mecanismos do OS para I/O async escalável. Contrastar com file I/O do POSIX que historicamente não tem API async kernel-level.
- **Por que importa:** sem entender essa divisão, sintomas de "thread pool exausto" parecem mágica. App que faz milhões de queries TCP em paralelo está bem; app que abre 100 arquivos em paralelo já travou o pool.
- **Como funciona:** tabela: API | onde | thread pool? | escala
  - `net.Socket`, `http.request` → kernel → não → milhões
  - `fs.readFile` → thread pool → sim → ~4 paralelas
  - `dns.lookup` → thread pool (via getaddrinfo do glibc) → sim → ~4 paralelas
  - `dns.resolve` (e `dns.resolve4`, etc) → kernel via socket UDP → não → milhões
  - `crypto.pbkdf2`, `crypto.scrypt` → thread pool → sim
  - zlib (compress, decompress) → thread pool → sim
- Code sample: experimento controlado que satura pool default. Subir `UV_THREADPOOL_SIZE=64` e re-medir.
- **Na prática:** caso típico — app que processa uploads e calcula bcrypt em paralelo. bcrypt usa thread pool; com 4 threads, 5 uploads concorrentes começam a esperar. Solução comum: subir `UV_THREADPOOL_SIZE` ou mover bcrypt pra Worker Thread (galho 2).
- **Armadilhas:** (1) `dns.lookup` é a função que `http.request` usa internamente — endpoints com DNS lento podem saturar pool sem aparente file I/O; (2) `crypto.randomBytes` em modo callback usa pool, em modo sync não; (3) `UV_THREADPOOL_SIZE` precisa ser setada antes de qualquer module que registre handle no pool.
- **Em entrevista:** "Node's async I/O comes in two flavors. Network I/O — TCP, HTTP — uses the OS's kernel-level async primitives: epoll on Linux, kqueue on macOS, IOCP on Windows. These are extremely scalable; you can have millions of open sockets. File I/O is different — POSIX doesn't have a real async file API, so libuv uses a thread pool, default size 4. DNS, crypto, and zlib also use the pool. The implication: an app heavy on file ops or crypto can saturate the pool with just 5 concurrent operations, while the same app doing TCP scales effortlessly." Vocabulário: I/O do kernel (kernel-level I/O), saturação do pool (pool saturation), busca DNS (DNS lookup), primitivas async do OS (OS async primitives).
- **Veja também:** `[[02 - V8, libuv e thread pool]]`, `[[04 - As fases do event loop]]`, `[[10 - Bloqueio do event loop - sintomas e causas]]`, `[[Node.js]]`.

Tamanho-alvo: 350-500 linhas.

- [ ] **Step 4: Verificar rubrica**

- [ ] **Step 5: Commit**

```bash
git add "03-Dominios/Node/Runtime e Event Loop/07 - I-O assíncrono - kernel vs thread pool.md"
git commit -m "feat(node-event-loop): add note 07 — I/O assíncrono kernel vs thread pool"
```

---

## Task 9: Nota 08 — Promises por dentro

**Files:**
- Create: `03-Dominios/Node/Runtime e Event Loop/08 - Promises por dentro.md`

**Conteúdo-chave do spec:**

> Estados (pending, fulfilled, rejected). Microtask queue como "memória" das `.then`. Encadeamento (`then` retornando promise). `Promise.resolve(value)` vs `new Promise((res) => res(value))`. Erros não capturados (`unhandledRejection`, `rejectionHandled`). Anti-patterns: Promise constructor anti-pattern, deferred.

- [ ] **Step 1: Pesquisa-âncora**

WebFetch:

```
WebFetch: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise
WebFetch: https://nodejs.org/api/process.html#event-unhandledrejection
```

- [ ] **Step 2: Criar arquivo + frontmatter**

```yaml
---
title: "Promises por dentro"
created: 2026-05-07
updated: 2026-05-07
type: concept
status: seedling
publish: true
tags:
  - node
  - event-loop
  - promise
  - microtask
aliases:
  - Promise mechanics
  - Promise internals
---
```

- [ ] **Step 3: Escrever a nota completa**

Cobrir:

- **TL;DR:** Uma Promise tem 3 estados (pending, fulfilled, rejected). `.then(cb)` enfileira `cb` na microtask queue quando a promise resolve. Encadeamento devolve promise nova; erros propagam até o primeiro `.catch`. `Promise.resolve(x)` é açúcar — cria promise já resolvida.
- **O que é:** revisar estados, contrato (uma vez resolvida, não muda). Mecânica do `.then` — não roda imediatamente, enfileira microtask. Encadeamento (cada `.then` retorna **nova** promise).
- **Por que importa:** a base de async/await. Sem entender que `.then` não é síncrono mesmo quando a promise já resolveu, você cria bugs sutis de ordem.
- **Como funciona:** code samples:
  1. Estados — `const p = new Promise((res) => res(42)); p.then(v => log(v));` — log do `v` é microtask, ainda assim
  2. Encadeamento: `p.then(v => v + 1).then(v => v * 2)` — cada then é uma nova promise
  3. Erros propagam: `p.then(() => { throw new Error(); }).catch(e => log(e))` 
  4. `Promise.resolve(x)` vs `new Promise((res) => res(x))` — equivalentes; o primeiro é mais limpo
  5. Anti-pattern do Promise constructor: `new Promise((res, rej) => fetch(url).then(res).catch(rej))` — duplica o que `fetch(url)` já é
  6. Deferred anti-pattern: extrair `resolve`/`reject` pra fora — válido em casos específicos (ex: build manual), evitar como padrão
- `unhandledRejection` event: code sample registrando handler global; comportamento de Node 22+ (default: terminate).
- **Na prática:** padrões observados:
  - Libs usam `Promise.resolve(value)` para normalizar APIs que aceitam value-or-promise
  - `unhandledRejection` handler em produção sempre presente, exporta pra logger
  - Padrão "fire and forget": `void doAsync()` quando rejeição é genuinamente irrelevante (raro)
- **Armadilhas:** (1) esquecer `return` dentro de `.then` — promise interna não é encadeada; (2) `await` em `Promise.resolve(syncFn())` — `syncFn()` ainda roda síncrono; (3) `Promise.all([])` resolve com `[]` (não erro); (4) `unhandledRejection` que você "trata" mas não logga vira bug fantasma.
- **Em entrevista:** "A Promise has three states: pending, fulfilled, and rejected — once settled, it's immutable. `.then` doesn't run synchronously; it queues the callback in the microtask queue, even if the promise is already resolved. Chained `.then` calls return new promises, so errors propagate down the chain until the first `.catch`. The unhandled rejection handler in Node logs the error and, by default in modern versions, terminates the process — which is the right behavior for unrecoverable bugs." Vocabulário: estados (states), liquidada/resolvida (settled), encadear (chain), promessa rejeitada não tratada (unhandled rejection).
- **Veja também:** `[[03 - Call stack, heap e queues]]`, `[[05 - Microtasks - nextTick, queueMicrotask, Promise.then]]`, `[[09 - async-await - o que é, o que não é]]`, `[[Node.js]]`.

Tamanho-alvo: 350-500 linhas.

- [ ] **Step 4: Verificar rubrica**

- [ ] **Step 5: Commit**

```bash
git add "03-Dominios/Node/Runtime e Event Loop/08 - Promises por dentro.md"
git commit -m "feat(node-event-loop): add note 08 — Promises por dentro"
```

---

## Task 10: Nota 09 — async/await desmistificado

**Files:**
- Create: `03-Dominios/Node/Runtime e Event Loop/09 - async-await - o que é, o que não é.md`

**Conteúdo-chave do spec:**

> `async/await` é **açúcar sintático sobre Promises** — não cria threads, não paraleliza. O exemplo da motivação (`heavyProcessing` em handler async ainda bloqueia). Sequenciamento desnecessário (`await a; await b;` quando `Promise.all([a, b])` cabe). Padrões: `Promise.all`, `Promise.allSettled`, `Promise.race`, `Promise.any`. async iterators (`for await of`).

- [ ] **Step 1: Pesquisa-âncora**

WebFetch:

```
WebFetch: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/async_function
WebFetch: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/all
```

- [ ] **Step 2: Criar arquivo + frontmatter**

```yaml
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
```

- [ ] **Step 3: Escrever a nota completa**

Cobrir:

- **TL;DR:** `async/await` é açúcar sobre Promises — **não cria threads, não paraleliza, não evita bloqueio**. Função async retorna Promise. `await` pausa a função até a promise resolver, mas a thread JS continua livre. Pra paralelizar de verdade, use `Promise.all`.
- **O que é:** definir `async` (função sempre retorna Promise; `return value` vira `Promise.resolve(value)`; throw vira reject). Definir `await` (pausa a function até promise settled, sem bloquear thread). Lembrar que await só funciona dentro de async (ou top-level com ESM).
- **Por que importa:** **mito central** — "ah usei async, então é performático". O exemplo da motivação:
  
  ```javascript
  app.get('/users', async (req, res) => {
      const result = heavyProcessing(data);  // CPU-bound síncrono
      res.json(result);
  });
  ```
  
  Mesmo com `async`, `heavyProcessing` bloqueia a thread JS — todas as outras requests esperam. `async` só diz "esta função retorna Promise"; não muda o que está dentro.
- **Como funciona:** code samples didáticos:
  1. `async function f() { return 42; }` — retorna Promise<42>
  2. `await` em valor não-Promise — funciona, comportamento de `await Promise.resolve(value)`
  3. Sequenciamento desnecessário:
     ```javascript
     // RUIM — sequencial sem necessidade
     const a = await fetch('/a');
     const b = await fetch('/b');
     // BOM — paralelo
     const [a, b] = await Promise.all([fetch('/a'), fetch('/b')]);
     ```
  4. `Promise.all` — falha rápido (rejeita no primeiro reject); `Promise.allSettled` — espera todas, retorna array de `{status, value|reason}`; `Promise.race` — primeira a settled (incluindo reject); `Promise.any` — primeira a fulfill (ignora rejects).
  5. async iterators: `for await (const chunk of stream) { ... }` — itera enquanto cada `next()` retorna promise.
- Tabela: combinator | falha rápida? | retorna | quando usar
- **Na prática:** padrão observado:
  - APIs que fazem 3 fetches independentes usam `Promise.all`
  - APIs que toleram falha parcial usam `Promise.allSettled`
  - Timeout de operação com `Promise.race([op, timeout])` — antes de `AbortSignal` virar mainstream; em 2026, preferir `AbortSignal.timeout(ms)`
- **Armadilhas:** (1) `await` em loop sequencial vira lentidão escondida (`for (item of list) { await processItem(item) }` quando `Promise.all(list.map(processItem))` cabia); (2) `Promise.all` sem limite de concorrência detona quando a list tem 10k items (use `p-limit` ou `for await of` com batches); (3) achar que `async` em handler do framework faz o framework "esperar" — Express precisa de wrapper pra capturar erros (`next(err)`); Fastify e NestJS lidam nativamente; (4) **o exemplo da motivação** — `async` não cria thread, não evita bloqueio se há código sync pesado.
- **Em entrevista:** "`async/await` is syntactic sugar over Promises. An `async` function always returns a Promise; `await` pauses the function until the awaited Promise settles, but the JS thread is free during that pause to handle other work. This is the most common misconception in Node interviews — that `async` makes code 'performant' or 'parallel'. It doesn't. If your async handler does CPU-bound synchronous work, the entire event loop blocks for that duration, and every other request has to wait. To actually parallelize asynchronous work, use `Promise.all` or `Promise.allSettled`. To offload CPU work, use Worker Threads." Vocabulário: açúcar sintático (syntactic sugar), liquidar (settle), pausar a função (pause the function), paralelizar (parallelize), trabalho de CPU (CPU-bound work).
- **Veja também:** `[[08 - Promises por dentro]]`, `[[10 - Bloqueio do event loop - sintomas e causas]]`, `[[Node.js]]`. Apontar pro galho 2 (Paralelismo) quando ele existir.

Tamanho-alvo: 400-600 linhas (nota crítica, justifica densidade).

- [ ] **Step 4: Verificar rubrica**

- [ ] **Step 5: Commit**

```bash
git add "03-Dominios/Node/Runtime e Event Loop/09 - async-await - o que é, o que não é.md"
git commit -m "feat(node-event-loop): add note 09 — async/await desmistificado"
```

---

## Task 11: Nota 10 — Bloqueio do event loop

**Files:**
- Create: `03-Dominios/Node/Runtime e Event Loop/10 - Bloqueio do event loop - sintomas e causas.md`

**Conteúdo-chave do spec:**

> Sintomas: latência geral subindo, todas as requests travam ao mesmo tempo, healthcheck timeout, conexões caindo. Causas canônicas: CPU-bound em handler (loops pesados, regex catastróficas, `JSON.parse` de payload grande), sync APIs (`fs.readFileSync`, `crypto.pbkdf2Sync`), thread pool exausto (file I/O concorrente além de 4). Como reproduzir num script controlado.

- [ ] **Step 1: Pesquisa-âncora**

WebFetch:

```
WebFetch: https://nodejs.org/en/learn/asynchronous-work/dont-block-the-event-loop
WebFetch: https://snyk.io/blog/redos-and-catastrophic-backtracking/
```

- [ ] **Step 2: Criar arquivo + frontmatter**

```yaml
---
title: "Bloqueio do event loop: sintomas e causas"
created: 2026-05-07
updated: 2026-05-07
type: concept
status: seedling
publish: true
tags:
  - node
  - event-loop
  - blocking
  - troubleshooting
  - performance
aliases:
  - Event loop blocking
  - Bloqueio do loop
  - CPU-bound
---
```

- [ ] **Step 3: Escrever a nota completa**

Cobrir:

- **TL;DR:** Sintomas de event loop bloqueado: latência geral subindo, requests travadas em conjunto, healthcheck timeoutando. Causas canônicas: CPU-bound síncrono em handler, sync APIs, regex catastróficas, JSON.parse de payload gigante, thread pool saturado.
- **O que é:** "event loop bloqueado" = a thread JS está executando código síncrono e o loop não consegue avançar. Todas as outras requests, timers, e I/O callbacks ficam esperando.
- **Por que importa:** "comportamentos estranhos no backend" — requests aparentemente desconexas todas lentas ao mesmo tempo, padrão de latência em "ondas". Sem esse modelo mental, é tentador buscar bug no código que tá lento, quando o culpado é outro handler bloqueando.
- **Como funciona:** sintomas detalhados:
  - Latência **conjunta** sobe (não isolada por endpoint)
  - Healthcheck (`GET /health`) começa a falhar
  - Conexões TCP idle são encerradas pelo OS
  - Métricas de event loop lag disparam
- Causas canônicas com code sample minimal:
  1. **CPU-bound em handler:**
     ```javascript
     app.get('/slow', (req, res) => {
       let sum = 0;
       for (let i = 0; i < 1e9; i++) sum += i;  // bloqueia
       res.json({ sum });
     });
     ```
  2. **Sync API:** `fs.readFileSync('big.txt')` ou `crypto.pbkdf2Sync(...)`
  3. **Regex catastrófica (ReDoS):** `^(a+)+$` contra string longa de `a` seguida de `b`
  4. **`JSON.parse` de payload gigante** — síncrono, parser bloqueia
  5. **Thread pool exausto:** 5+ `fs.readFile` paralelos com pool default 4 — não bloqueia event loop diretamente, mas cria fila no pool e produz timeouts
- Como reproduzir: script standalone com `autocannon` apontando pra dois endpoints (um normal, um bloqueante), observar latência do normal disparar.
- **Na prática:** caso típico — endpoint que processa CSV grande síncrono via `JSON.parse`. Solução estrutural: streaming (galho 3), Worker Thread (galho 2), ou paginação no client.
- **Armadilhas:** (1) regex em entrada de usuário sem timeout — ReDoS clássico; (2) middleware que loga o body inteiro (`JSON.stringify` de payload de 50MB); (3) `fs.readFileSync` no startup OK; em handler, fatal; (4) crypto sync (`pbkdf2Sync`) "porque é mais simples" — mata o servidor sob load.
- **Em entrevista:** "Symptoms of a blocked event loop are surprisingly consistent: latency rises across all endpoints simultaneously, healthchecks start timing out, and TCP connections start dropping. Common causes: CPU-bound work in a handler — loops, catastrophic regex, JSON.parse on huge payloads — and synchronous I/O APIs like `fs.readFileSync` or `crypto.pbkdf2Sync`. Thread pool saturation is the subtler cousin: file I/O or crypto in callback mode that exceeds the default 4 threads creates a queue, so requests appear blocked even though the event loop itself is fine. The structural fix is to move heavy work to Worker Threads or to stream the data." Vocabulário: bloqueio do loop (event loop blocking), regex catastrófica (catastrophic regex / ReDoS), saturação do pool (pool saturation), latência conjunta (correlated latency).
- **Veja também:** `[[04 - As fases do event loop]]`, `[[07 - I-O assíncrono - kernel vs thread pool]]`, `[[09 - async-await - o que é, o que não é]]`, `[[11 - Diagnóstico do event loop]]`, `[[Node.js]]`.

Tamanho-alvo: 400-550 linhas.

- [ ] **Step 4: Verificar rubrica**

- [ ] **Step 5: Commit**

```bash
git add "03-Dominios/Node/Runtime e Event Loop/10 - Bloqueio do event loop - sintomas e causas.md"
git commit -m "feat(node-event-loop): add note 10 — Bloqueio do event loop"
```

---

## Task 12: Nota 11 — Diagnóstico do event loop

**Files:**
- Create: `03-Dominios/Node/Runtime e Event Loop/11 - Diagnóstico do event loop.md`

**Conteúdo-chave do spec:**

> `perf_hooks.monitorEventLoopDelay` para métrica contínua. `process.hrtime.bigint()` pra medir handlers individuais. `--inspect` + Chrome DevTools (CPU profile, flame chart). `clinic.js doctor` (visão geral) e `clinic.js bubbleprof` (mapa de async). `autocannon` pra load test.

- [ ] **Step 1: Pesquisa-âncora**

WebFetch:

```
WebFetch: https://nodejs.org/api/perf_hooks.html#perf_hooksmonitoreventloopdelayoptions
WebFetch: https://clinicjs.org/doctor/
WebFetch: https://github.com/mcollina/autocannon
```

- [ ] **Step 2: Criar arquivo + frontmatter**

```yaml
---
title: "Diagnóstico do event loop"
created: 2026-05-07
updated: 2026-05-07
type: concept
status: seedling
publish: true
tags:
  - node
  - event-loop
  - diagnostics
  - profiling
  - perf-hooks
aliases:
  - perf_hooks
  - clinic.js
  - autocannon
  - event loop lag
---
```

- [ ] **Step 3: Escrever a nota completa**

Cobrir:

- **TL;DR:** Pra diagnosticar event loop, use 4 ferramentas em camadas: `perf_hooks.monitorEventLoopDelay` (métrica contínua → Prometheus), `process.hrtime.bigint()` (medir handler específico), `--inspect` + Chrome DevTools (CPU profile pontual), `clinic.js` (análise estruturada). `autocannon` pra reproduzir load.
- **O que é:** "event loop lag" = tempo entre quando uma tick deveria começar e quando começa de fato. Subindo significa thread JS sobrecarregada. Resolução típica: 50ms ou menos.
- **Por que importa:** sem métrica, "tá lento" é hipótese; com métrica, é diagnóstico. Event loop lag em produção é o sinal mais direto de bloqueio.
- **Como funciona:** code samples para cada ferramenta:
  1. **`monitorEventLoopDelay`:**
     ```typescript
     import { monitorEventLoopDelay } from 'node:perf_hooks';
     const h = monitorEventLoopDelay({ resolution: 50 });
     h.enable();
     setInterval(() => {
       console.log(`p99=${h.percentile(99) / 1e6}ms p50=${h.percentile(50) / 1e6}ms`);
       h.reset();
     }, 10000);
     ```
  2. **`process.hrtime.bigint()` para medir handler:**
     ```typescript
     app.use((req, res, next) => {
       const start = process.hrtime.bigint();
       res.on('finish', () => {
         const ns = Number(process.hrtime.bigint() - start);
         logger.info({ url: req.url, ms: ns / 1e6 });
       });
       next();
     });
     ```
  3. **`--inspect` + DevTools:** rodar `node --inspect app.js`, abrir `chrome://inspect`, attach, gravar CPU profile durante load. Analisar flame chart — função no topo é o bloqueio.
  4. **`clinic.js`:**
     ```bash
     npx clinic doctor -- node app.js
     # ataca com autocannon
     npx autocannon http://localhost:3000
     # Ctrl+C, clinic gera relatório HTML
     ```
     `doctor` dá um diagnóstico em prosa (CPU? Event loop? GC? I/O?). `bubbleprof` mapeia operações async.
  5. **autocannon:**
     ```bash
     npx autocannon -c 100 -d 30 http://localhost:3000/endpoint
     ```
     100 conexões, 30s de duração; reporta latency p50/p99, RPS.
- Tabela: ferramenta | nivel | uso | quando
- **Na prática:** em produção:
  - `monitorEventLoopDelay` exportado pra Prometheus (gauge `nodejs_event_loop_lag_seconds`)
  - Alerta quando p99 passa de 100ms
  - Quando alerta dispara, `clinic doctor` em pré-prod com load similar
  - `--inspect` em prod só com cuidado (custo, segurança)
- **Armadilhas:** (1) `monitorEventLoopDelay` sem `enable()` não faz nada; (2) esquecer `reset()` faz percentis virarem média histórica eterna; (3) `clinic.js` exige load real — sem load, output é inútil; (4) `autocannon` num serviço sem proteção pode derrubá-lo (rate limit do framework); (5) `--inspect` em prod expõe debugger se a porta vazar — usar `--inspect=127.0.0.1` e SSH tunnel.
- **Em entrevista:** "Diagnostics for event loop issues come in layers. For continuous metrics, `perf_hooks.monitorEventLoopDelay` exposes a histogram of event loop lag — typically exported to Prometheus with an alert when p99 crosses 100 milliseconds. For per-request timing, `process.hrtime.bigint()` in middleware. For deep dives, `node --inspect` plus Chrome DevTools gives a CPU profile and flame chart. For structured analysis, `clinic.js doctor` runs your app under load and produces a prose diagnosis — CPU, event loop, GC, or I/O. And to actually generate the load, `autocannon`." Vocabulário: atraso do event loop (event loop lag), perfil de CPU (CPU profile), gráfico de chamas (flame chart), teste de carga (load test).
- **Veja também:** `[[10 - Bloqueio do event loop - sintomas e causas]]`, `[[12 - Armadilhas, regras práticas, cheatsheet]]`, `[[Node.js]]`. Apontador pro galho 5 (Observability) quando ele existir.

Tamanho-alvo: 400-550 linhas.

- [ ] **Step 4: Verificar rubrica**

- [ ] **Step 5: Commit**

```bash
git add "03-Dominios/Node/Runtime e Event Loop/11 - Diagnóstico do event loop.md"
git commit -m "feat(node-event-loop): add note 11 — Diagnóstico do event loop"
```

---

## Task 13: Nota 12 — Armadilhas, regras práticas, cheatsheet

**Files:**
- Create: `03-Dominios/Node/Runtime e Event Loop/12 - Armadilhas, regras práticas, cheatsheet.md`

**Conteúdo-chave do spec:**

> Top 10 armadilhas. Tabela cheatsheet (timer → fase → quando usar). Decision tree "minha request está lenta — por onde começar?". Cheatsheet de vocabulário em inglês. Links pros galhos seguintes.

- [ ] **Step 1: Compilar de todas as notas**

Reler todas as 11 notas anteriores e extrair as armadilhas mais críticas. Compor a Top 10. Não precisa de WebFetch novo — síntese.

- [ ] **Step 2: Criar arquivo + frontmatter**

```yaml
---
title: "Armadilhas, regras práticas, cheatsheet"
created: 2026-05-07
updated: 2026-05-07
type: concept
status: seedling
publish: true
tags:
  - node
  - event-loop
  - cheatsheet
  - armadilhas
  - referencia
aliases:
  - Cheatsheet event loop
  - Armadilhas Node runtime
---
```

- [ ] **Step 3: Escrever a nota completa**

Estrutura tópica (não narrativa):

- **TL;DR:** Cheatsheet de fechamento da sub-trilha. Top 10 armadilhas, tabela timer/fase, decision tree de "minha request está lenta", vocabulário PT→EN, e quando seguir pros galhos 2 (paralelismo), 3 (streams), 5 (observability).
- **Top 10 armadilhas:** lista numerada, cada com: descrição (1 linha), exemplo curto, fix:
  1. Recursão em `process.nextTick` → starvation do loop. Fix: usar `setImmediate`.
  2. CPU-bound síncrono em handler async → bloqueia tudo. Fix: Worker Thread (galho 2) ou streaming.
  3. `Promise.all` em lista grande sem limite de concorrência → satura recursos. Fix: `p-limit` ou batches.
  4. `await` em loop sequencial onde paralelo cabe → lentidão escondida. Fix: `Promise.all(list.map(...))`.
  5. `setInterval` reentrante (handler > intervalo) → callbacks empilhados. Fix: `setTimeout` recursivo com cálculo de drift.
  6. `unhandledRejection` não tratado → processo termina silenciosamente em Node 22+. Fix: handler global que loga.
  7. Sync APIs em handler (`fs.readFileSync`, `crypto.pbkdf2Sync`, `JSON.parse` de payload grande) → bloqueio. Fix: versão async + streaming.
  8. Thread pool exausto por file I/O ou crypto concorrentes → timeouts em endpoints sem causa óbvia. Fix: `UV_THREADPOOL_SIZE` ou Worker Thread.
  9. Regex catastrófica em input do usuário → ReDoS. Fix: validar com lib (zod/joi), limitar tamanho do input, regex sem backtracking.
  10. Timer com closure pesado nunca limpo → memory leak. Fix: `clearTimeout`/`clearInterval` no cleanup.
- **Cheatsheet — timer e fase:**

| API | Tipo | Fase | Quando usar |
|---|---|---|---|
| `process.nextTick` | microtask | entre fases | deferir mínimo, prioridade máxima |
| `queueMicrotask` | microtask | entre fases | padrão web, após código síncrono |
| `Promise.then` | microtask | entre fases | após uma promise resolver |
| `setTimeout(fn, ms)` | macrotask | timers | delay com tempo |
| `setInterval(fn, ms)` | macrotask | timers | repetição (preferir setTimeout recursivo) |
| `setImmediate(fn)` | macrotask | check | após I/O atual, antes do próximo timer |

- **Decision tree — "minha request está lenta":**
  ```
  P50 alto?
  ├─ Sim → CPU-bound? regex? JSON.parse big?
  │         └─ Sim → Worker Thread / streaming / paginação
  │         └─ Não → DB? rede? → fora deste galho
  └─ Não, mas P99 alto e correlacionado entre endpoints?
            └─ Sim → event loop lag (ver nota 11). Causas: pool saturado, GC, sync API
            └─ Não → endpoint específico tem bug
  ```
- **Vocabulário PT→EN (compilado):** event loop, single-thread, non-blocking I/O, microtask, macrotask, queue starvation, thread pool, kernel async, epoll/kqueue/IOCP, await, Promise settled, async iterator, event loop lag, flame chart, ReDoS, catastrophic backtracking, CPU-bound, I/O-bound.
- **Próximos galhos:**
  - Pra **fugir do bloqueio estruturalmente**: `[[Galho 2 — Paralelismo]]` (Worker Threads, cluster, child_process)
  - Pra **processar dados grandes sem bloquear**: `[[Galho 3 — Streams]]`
  - Pra **observar em produção**: `[[Galho 5 — Observability]]` (profiling, logging, métricas)
- **Veja também:** `[[Runtime e Event Loop]]` (MOC do galho), `[[Node.js]]` (tronco), todos os outros 11 itens da trilha.

Tamanho-alvo: 350-500 linhas (denso por natureza tópica).

- [ ] **Step 4: Verificar rubrica**

Rubrica adaptada (nota tópica):

```
[ ] TL;DR no callout [!abstract]
[ ] Top 10 armadilhas com 1 exemplo + 1 fix cada
[ ] Cheatsheet de timer/fase em tabela
[ ] Decision tree presente
[ ] Vocabulário PT→EN (15+ termos)
[ ] Wikilinks: 12+ (todas as notas + tronco + galhos futuros)
[ ] Frontmatter completo
[ ] Sem fabricação
```

- [ ] **Step 5: Commit**

```bash
git add "03-Dominios/Node/Runtime e Event Loop/12 - Armadilhas, regras práticas, cheatsheet.md"
git commit -m "feat(node-event-loop): add note 12 — Armadilhas, regras práticas, cheatsheet"
```

---

## Task 14: Pass final no MOC

**Files:**
- Modify: `03-Dominios/Node/Runtime e Event Loop/Runtime e Event Loop.md`

- [ ] **Step 1: Reler todas as 12 notas**

Carregar mentalmente os títulos finais (que podem ter divergido do esqueleto se algum título foi ajustado).

- [ ] **Step 2: Atualizar a seção "Sobre este galho" do MOC**

Substituir o placeholder `(introdução curta — preencher na Task 14)` por:

```markdown
## Sobre este galho

Este galho cobre o **motor** do Node.js — como uma única thread JS atende milhares de conexões. Inclui o mental model (single-thread, V8/libuv, queues), o ciclo do event loop em profundidade (fases, microtasks, macrotasks, I/O), `async/await` desmistificado (não é paralelismo!), e ferramentas para diagnosticar bloqueio em produção.

É a **base de todos os outros galhos**: paralelismo, streams, frameworks, observability e segurança pressupõem esse modelo mental.

**Audiência primária:** dev senior em prep para entrevista internacional. Cada nota tem seção "Em entrevista" com frase pronta em inglês + vocabulário.

**Audiência secundária:** o mesmo dev em produção, debugando "comportamentos estranhos" (latência subindo, requests travando). Use a rota "debugging em produção".
```

- [ ] **Step 3: Verificar todos os wikilinks**

Confirmar que cada `[[01 - ...]]` até `[[12 - ...]]` resolve pra arquivo existente. Em particular, o título do arquivo deve bater **exatamente** com o conteúdo do wikilink.

```bash
ls "03-Dominios/Node/Runtime e Event Loop/"
```

Comparar com os wikilinks do MOC. Se algum estiver quebrado, corrigir.

- [ ] **Step 4: Atualizar dataview se necessário**

Se algum item não aparecer na dataview, debugar — pode ser que `type` de alguma nota esteja errado.

- [ ] **Step 5: Commit**

```bash
git add "03-Dominios/Node/Runtime e Event Loop/Runtime e Event Loop.md"
git commit -m "feat(node-event-loop): finalize MOC with all wikilinks and intro"
```

---

## Task 15: Poda do tronco

**Files:**
- Modify: `03-Dominios/JavaScript/Backend/Node.js.md`

- [ ] **Step 1: Reler o tronco e identificar seções a podar**

Ler `03-Dominios/JavaScript/Backend/Node.js.md` integralmente. Identificar (com nomes exatos confirmados na Task 0):

- Seção "Arquitetura" (~linha 47-70)
- Seção "Single-threaded com non-blocking I/O" (~linha 71-83)
- Seção "Event loop phases — detalhado" (~linha 84-135)
- Em "Armadilhas comuns": item "Blocking the event loop"
- Em "Troubleshooting em produção": seção "Event loop blocking"

- [ ] **Step 2: Substituir "Arquitetura"**

Substituir o conteúdo (preservando o título da seção) por:

```markdown
### Arquitetura

> [!nota] Migrado para galho próprio
> A anatomia interna do runtime — V8, libuv, thread pool — foi expandida em [[Runtime e Event Loop]]. Veja em particular [[02 - V8, libuv e thread pool]] (componentes), [[01 - Single-thread e non-blocking I-O]] (modelo), e [[07 - I-O assíncrono - kernel vs thread pool]] (onde o paralelismo verdadeiro mora).
```

- [ ] **Step 3: Substituir "Single-threaded com non-blocking I/O"**

```markdown
### Single-threaded com non-blocking I/O

> [!nota] Migrado para galho próprio
> O modelo single-thread + non-blocking I/O foi expandido em [[01 - Single-thread e non-blocking I-O]] dentro do galho [[Runtime e Event Loop]].
```

- [ ] **Step 4: Substituir "Event loop phases — detalhado"**

```markdown
### Event loop phases — detalhado

> [!nota] Migrado para galho próprio
> As fases do event loop foram expandidas em [[Runtime e Event Loop]]. Veja em particular [[04 - As fases do event loop]] (ciclo libuv), [[05 - Microtasks - nextTick, queueMicrotask, Promise.then]] (microtasks), e [[06 - Macrotasks e timers - setTimeout, setInterval, setImmediate]] (timers).
```

- [ ] **Step 5: Atualizar "Armadilhas comuns"**

Localizar item "Blocking the event loop" e substituir por:

```markdown
- **Blocking the event loop:** Sintomas, causas e diagnóstico em [[10 - Bloqueio do event loop - sintomas e causas]] e [[11 - Diagnóstico do event loop]] (galho [[Runtime e Event Loop]]).
```

- [ ] **Step 6: Atualizar "Troubleshooting em produção" (Event loop blocking)**

Substituir conteúdo de "Event loop blocking" por:

```markdown
### Event loop blocking

> [!nota] Migrado para galho próprio
> Sintomas, causas e ferramentas de diagnóstico foram expandidos em [[Runtime e Event Loop]]: [[10 - Bloqueio do event loop - sintomas e causas]] e [[11 - Diagnóstico do event loop]].
```

- [ ] **Step 7: Atualizar "Veja também" do tronco**

Adicionar à lista de "Veja também" do final do arquivo:

```markdown
- [[Runtime e Event Loop]] — galho 1 da trilha Node Senior; deep dive do motor (single-thread, libuv, fases, microtasks, async/await, bloqueio, diagnóstico)
```

- [ ] **Step 8: Atualizar `updated` no frontmatter do tronco**

Mudar `updated: 2026-04-11` (ou o que estiver) para `updated: 2026-05-07`.

- [ ] **Step 9: Commit**

```bash
git add "03-Dominios/JavaScript/Backend/Node.js.md"
git commit -m "refactor(node): prune trunk Node.js.md, link to Runtime e Event Loop branch"
```

---

## Task 16: Atualizar MOC central + verificar Quartz

**Files:**
- Modify: `03-Dominios/Node/index.md`

- [ ] **Step 1: Atualizar o MOC central**

Substituir a seção "Conteúdo" do `03-Dominios/Node/index.md`:

```markdown
## Conteúdo

### Galhos da trilha Node Senior

- [[Runtime e Event Loop]] — galho 1: o motor do Node (single-thread, libuv, fases, microtasks, async/await, bloqueio, diagnóstico)

### Outras notas

- [[Ferramentas Node]] — panorama de ferramentas do ecossistema (em construção)
```

E atualizar `updated` pra `2026-05-07`.

- [ ] **Step 2: Verificar build do Quartz**

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus
# ou onde quer que o Quartz esteja configurado pra ler este vault
# adaptar comando conforme setup local
```

Se o setup do Quartz exigir build local, rodar e verificar:

- Sem erros de build
- As 13 novas notas aparecem na pasta `Node/Runtime e Event Loop/`
- Wikilinks resolvem
- MOC central linka pro galho

Se Quartz é build em CI (push to main), o teste é o build CI passar.

- [ ] **Step 3: Commit**

```bash
git add "03-Dominios/Node/index.md"
git commit -m "feat(node-event-loop): wire branch into central Node MOC"
```

- [ ] **Step 4: Verificação final — critérios de aceitação**

Checklist do spec seção 12:

```
[ ] 13 arquivos existem em "03-Dominios/Node/Runtime e Event Loop/"
[ ] Todos com publish: true
[ ] MOC com 4 rotas + dataview + 12 notas linkadas
[ ] Cada nota satisfaz a rubrica padrão
[ ] Tasks de poda (seção 10 do spec) executadas
[ ] MOC central atualizado
[ ] Quartz publica corretamente
[ ] 4+ notas com code samples testáveis em script standalone
```

Se algum item falhar, voltar e corrigir antes de declarar galho fechado.

- [ ] **Step 5: Commit final de "galho fechado"**

```bash
git commit --allow-empty -m "chore(node-event-loop): close branch Galho 1 — Runtime e Event Loop

12 atomic notes + MOC published in 03-Dominios/Node/Runtime e Event Loop/.
Trunk Node.js.md pruned. Central Node MOC updated. All acceptance
criteria from 2026-05-07-node-runtime-event-loop-design.md met."
```

---

## Pós-execução

1. **Atualizar memória** se algum aprendizado novo apareceu (ex: padrão de poda do tronco que vale registrar pros próximos galhos)
2. **Revisar `2026-05-07-node-roadmap-design.md`** com aprendizados — se a poda foi mais simples/complexa que esperado, ajustar a "Política de poda do tronco"
3. **Decidir destino final do tronco** (vira MOC enxuto? continua como visão panorâmica?) — decisão informada pela primeira poda
4. **Próximo galho** — escolher entre Galho 2 (Paralelismo) ou Galho 3 (Streams) com base em prioridade do momento, brainstormar e escrever spec

---

## Self-review do plano

- **Spec coverage:**
  - Os 12 nomes de nota do spec seção 5 estão cobertos por Tasks 2-13 ✓
  - MOC criado em Task 1, finalizado em Task 14 ✓
  - 4 rotas alternativas presentes no MOC esqueleto (Task 1) ✓
  - Tasks de poda (spec seção 10): cobertas em Task 15 ✓
  - Atualização do MOC central (spec seção 10, item 6): Task 16 ✓
  - Critérios de aceitação (spec seção 12): checklist em Task 16 step 4 ✓
  - Bibliografia (spec seção 8): centralizada no topo + WebFetch específico em cada Task ✓
  - Restrição de fabricação: bloco no topo + na rubrica de cada nota ✓

- **Placeholder scan:** sem TBD/TODO. O único `(introdução curta — preencher na Task 14)` é parte do MOC esqueleto e tem instrução explícita pra ser substituído na Task 14 step 2 ✓

- **Type consistency:** títulos das notas batem entre Task de criação, MOC esqueleto (Task 1), pass final do MOC (Task 14), poda do tronco (Task 15). Wikilinks usam o mesmo título nominal em todas as ocorrências ✓
