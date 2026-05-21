---
title: "Spec — Sub-trilha Runtime e Event Loop (Galho 1)"
date: 2026-05-07
author: Josenaldo
status: draft
type: spec
publish: false
---

# Spec — Sub-trilha "Runtime e Event Loop" (Galho 1)

## 1. Contexto e motivação

Esta é a **primeira sub-trilha** (galho 1) do roadmap descrito em `2026-05-07-node-roadmap-design.md`. Pressupõe leitura desse roadmap — a metáfora tronco/galhos, os padrões editoriais comuns, e a política de poda do `Node.js.md` monolítico não são repetidos aqui.

O gatilho específico desta sub-trilha é uma observação recorrente: **muita gente usa Node.js todo dia mas só começa a entender a stack quando aprende como o event loop funciona**. Node é single-threaded e mesmo assim atende milhares de requisições — esse paradoxo confunde, e a confusão produz código que parece performático mas não é.

O exemplo canônico:

```javascript
app.get('/users', async (req, res) => {
    const result = heavyProcessing(data);  // CPU-bound, síncrono
    res.json(result);
});
```

Mesmo com `async`, se `heavyProcessing` consumir CPU, **outras requisições travam esperando**. `async/await` é açúcar sintático sobre Promises — não cria threads, não paraleliza, não muda a natureza single-thread do runtime.

Entender de verdade exige descer ao motor:

- **Call stack** — onde o JS roda
- **Event loop** — como o ciclo agenda trabalho
- **Microtasks** — `process.nextTick`, `queueMicrotask`, `Promise.then`
- **Macrotasks** — `setTimeout`, `setInterval`, `setImmediate`
- **Promises** — mecânica interna, microtask queue
- **Timers** — quando cada um roda
- **I/O** — kernel async vs thread pool do libuv

E entender quando o motor **trava** ("comportamentos estranhos no backend"): latência geral subindo, requests aparentemente desconexas todas lentas, healthcheck timeoutando.

Esta sub-trilha existe pra dar ao leitor o **modelo mental completo do runtime** + **as ferramentas de diagnóstico** quando o modelo é violado.

## 2. Objetivo

Produzir **12 notas atômicas + 1 MOC** (13 arquivos) em `03-Dominios/Node/Runtime e Event Loop/`, todas `publish: true`, em PT-BR, cobrindo do mental model do runtime ao diagnóstico de event loop bloqueado.

A trilha precisa ser:

- **Atômica** — cada nota linkável e citável separadamente
- **Híbrida em camadas** — TL;DR + corpo técnico, no padrão do roadmap
- **Complementar ao tronco** — pressupõe que o leitor pode consultar `[[Node.js]]` mas a sub-trilha aprofunda além do que o tronco cobre, e a poda do tronco substitui as seções correspondentes por wikilinks aqui
- **Idiomática 2026** — Node 22 LTS / 24, V8 12.x/13.x, libuv 1.x, TypeScript 5.x quando relevante
- **Orientada a entrevistas internacionais** — cada nota tem "Em entrevista" com frase em inglês + vocabulário; rota alternativa "entrevista" no MOC

## 3. Escopo

### Em escopo

- 13 arquivos markdown em `03-Dominios/Node/Runtime e Event Loop/`
- Todos com `publish: true`
- Idioma: PT-BR; termos técnicos em inglês mantidos
- Wikilinks densos para `[[Node.js]]` (tronco), `[[JavaScript Fundamentals]]` (event loop básico do JS), `[[TypeScript]]` quando code samples em TS
- Pesquisa baseada em fontes primárias declaradas na bibliografia
- Tasks de poda do tronco executadas ao fechar o galho

### Fora de escopo

- **Worker Threads, cluster, child_process** — galho 2 (Paralelismo). Esta sub-trilha menciona "fugir do bloqueio = galho 2", sem entrar em detalhes
- **Streams** — galho 3. Backpressure é mencionado en passant na nota de I/O quando relevante
- **Frameworks** — galho 4. Exemplos de código usam Express ou plain Node, mas o galho não aprofunda framework
- **Profiling avançado / clinic.js / OpenTelemetry** — galho 5 (Observability). Esta sub-trilha cobre `perf_hooks.monitorEventLoopDelay` e `--inspect` no nível "diagnóstico imediato"; profiling estruturado é galho 5
- **Segurança** — galho 6
- **Comparação Node vs Bun vs Deno em runtime** — menções pontuais quando relevante; comparação aprofundada é fora de escopo
- **JS engine internals (V8 hidden classes, inline caches, TurboFan)** — V8 aparece como caixa-preta nominal; deep dive de V8 é projeto separado se virar foco

## 4. Audiência e barra de qualidade

**Audiência primária:** dev senior em prep para entrevista internacional. Já usa Node há anos, sabe que existe event loop e single-thread, mas não consegue **explicar com vocabulário preciso** em inglês as fases do loop, a diferença entre microtask e macrotask, ou por que `process.nextTick` é mais perigoso que `setImmediate`.

**Audiência secundária:** o mesmo dev em produção, debugando latência inexplicada e lentidão geral. Para esse público, a rota alternativa "debugging em produção" no MOC é otimizada.

**Barra de qualidade:** ao terminar de ler a sub-trilha, o leitor deve conseguir:

1. Explicar em inglês, em <2 minutos, como Node é single-threaded e ainda assim atende milhares de conexões
2. Listar as 6 fases do event loop em ordem e descrever o que cada uma faz
3. Diferenciar microtask de macrotask, citar 3 funções de cada categoria, e explicar a ordem de execução
4. Reconhecer e explicar que `async/await` não paraleliza nada — só açúcar sobre Promise
5. Identificar pelo menos 5 causas canônicas de event loop bloqueado em código alheio
6. Usar `perf_hooks.monitorEventLoopDelay` para medir lag do loop em produção
7. Explicar a diferença entre I/O do kernel (epoll/kqueue) e I/O do thread pool do libuv
8. Reconhecer quando recursão em `process.nextTick` está bloqueando o loop
9. Saber quando preferir `Promise.all` sobre `await` sequencial (e quando o sequencial é correto)
10. Citar e usar pelo menos 3 ferramentas de diagnóstico (`--inspect`, `perf_hooks`, `clinic.js`) com vocabulário em inglês

## 5. Estrutura da sub-trilha (13 arquivos)

### MOC

| # | Arquivo | Propósito |
|---|---|---|
| — | `Runtime e Event Loop.md` | MOC do galho. Trilha sequencial 01→12 + 4 rotas alternativas. Dataview de "Todas as notas do galho". Linka pro MOC central `Node/index.md` e pro tronco `[[Node.js]]`. |

### Bloco A — Mental model (3 notas)

| # | Arquivo | Propósito | Conteúdo-chave |
|---|---|---|---|
| 01 | `01 - Single-thread e non-blocking I-O.md` | O modelo, em uma frase | Por que Node é single-threaded mas atende milhares de conexões. A intuição: I/O é delegado, código JS roda em uma thread só. Comparação com modelo thread-per-request (Apache, Tomcat tradicional). Onde isso ganha (I/O-bound) e onde perde (CPU-bound). |
| 02 | `02 - V8, libuv e thread pool.md` | Anatomia interna do runtime | Os 3 componentes: V8 (engine JS, JIT), libuv (event loop + thread pool C), Node bindings (C++ glue). Tamanho default do thread pool (4 threads) e `UV_THREADPOOL_SIZE`. O que usa o pool: filesystem (parte), DNS (`dns.lookup`), crypto, compression. O que não usa: net/http (vai direto pro epoll/kqueue). |
| 03 | `03 - Call stack, heap e queues.md` | Estado da thread JS em runtime | Call stack (frames de execução, V8 stack size, `RangeError: Maximum call stack`), heap (objetos, GC, gerações), microtask queue, macrotask queue (callback queue). Como uma operação async navega entre eles. Por que a stack precisa esvaziar antes do event loop avançar. |

### Bloco B — Event loop deep dive (4 notas)

| # | Arquivo | Propósito | Conteúdo-chave |
|---|---|---|---|
| 04 | `04 - As fases do event loop.md` | O ciclo libuv | As 6 fases: timers, pending callbacks, idle/prepare (interno), poll, check, close callbacks. O que cada uma faz e em que ordem. Diagrama. Onde microtasks rodam (entre cada fase). Por que `poll` é especial (pode bloquear). |
| 05 | `05 - Microtasks - nextTick, queueMicrotask, Promise.then.md` | Prioridade e quando rodam | A hierarquia: `process.nextTick` (prioridade máxima, antes do próximo iteration) > `queueMicrotask` ≈ `Promise.then` (entre fases). Tabela comparativa. Por que recursão em `nextTick` bloqueia o loop ("nextTick starvation"). Quando usar cada um. Note: `process.nextTick` é Node-específico; `queueMicrotask` é padrão. |
| 06 | `06 - Macrotasks e timers - setTimeout, setInterval, setImmediate.md` | Os timers e o que rodam onde | `setTimeout(fn, 0)` mínimo de 1ms (nos motores modernos, mas atenção). `setImmediate` na fase `check`. `setImmediate` vs `setTimeout(fn, 0)` — em I/O é determinístico (`setImmediate` ganha), fora não. Caveat de `setInterval` com handler que demora. `timers/promises` para sleep idiomático. |
| 07 | `07 - I-O assíncrono - kernel vs thread pool.md` | Onde mora o paralelismo "verdadeiro" | Confusão clássica: nem todo I/O passa pelo thread pool. Network I/O (`net`, `http`, `https`) usa **epoll/kqueue/IOCP do OS** — não consome thread do pool. File I/O (`fs`) usa o pool (porque file I/O do POSIX não é realmente async). DNS (`dns.lookup`) usa o pool, mas `dns.resolve` não. Implicação prática: pool exausto em apps file-heavy ou crypto-heavy. |

### Bloco C — async/await em profundidade (2 notas)

| # | Arquivo | Propósito | Conteúdo-chave |
|---|---|---|---|
| 08 | `08 - Promises por dentro.md` | Mecânica da Promise | Estados (pending, fulfilled, rejected). Microtask queue como "memória" das `.then`. Encadeamento (`then` retornando promise). `Promise.resolve(value)` vs `new Promise((res) => res(value))`. Erros não capturados (`unhandledRejection`, `rejectionHandled`). Anti-patterns: Promise constructor anti-pattern, deferred. |
| 09 | `09 - async-await - o que é, o que não é.md` | O mito "async = performance" | `async/await` é **açúcar sintático sobre Promises** — não cria threads, não paraleliza. O exemplo da motivação (`heavyProcessing` em handler async ainda bloqueia). Sequenciamento desnecessário (`await a; await b;` quando `Promise.all([a, b])` cabe). Padrões: `Promise.all`, `Promise.allSettled`, `Promise.race`, `Promise.any`. async iterators (`for await of`). |

### Bloco D — Bloqueio e diagnóstico (2 notas)

| # | Arquivo | Propósito | Conteúdo-chave |
|---|---|---|---|
| 10 | `10 - Bloqueio do event loop - sintomas e causas.md` | "Comportamentos estranhos" | Sintomas: latência geral subindo, todas as requests travam ao mesmo tempo, healthcheck timeout, conexões caindo. Causas canônicas: CPU-bound em handler (loops pesados, regex catastróficas, `JSON.parse` de payload grande), sync APIs (`fs.readFileSync`, `crypto.pbkdf2Sync`), thread pool exausto (file I/O concorrente além de 4). Como reproduzir num script controlado. Conexão com galho 2 (Paralelismo) como solução estrutural. |
| 11 | `11 - Diagnóstico do event loop.md` | Ferramentas e patterns | `perf_hooks.monitorEventLoopDelay` para métrica contínua (resolução, percentis, reset). `process.hrtime.bigint()` pra medir handlers individuais. `--inspect` + Chrome DevTools (CPU profile, flame chart). `clinic.js doctor` (visão geral) e `clinic.js bubbleprof` (mapa de async). `autocannon` pra load test. Quando cada ferramenta. Como exportar event loop lag pra Prometheus. Apontador pro galho 5 (Observability) pra profiling avançado. |

### Bloco E — Fechamento (1 nota)

| # | Arquivo | Propósito | Conteúdo-chave |
|---|---|---|---|
| 12 | `12 - Armadilhas, regras práticas, cheatsheet.md` | O que checar antes de fechar PR | Top 10 armadilhas (recursão em `nextTick`, sync I/O em handler, thread pool exausto, `Promise.all` sem limite, `setInterval` reentrante, esquecer await, retornar Promise dentro de Promise sem await, etc.). Tabela cheatsheet (timer → fase → quando usar). Decision tree "minha request está lenta — por onde começar?". Cheatsheet de vocabulário em inglês. Links pros galhos seguintes (paralelismo, observability). |

## 6. Padrão estrutural por nota

Toda nota segue o padrão herdado do roadmap:

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
  - <conceito-tag específica>
aliases:
  - <opcional>
---

# <Título>

> [!abstract] TL;DR
> <2-4 linhas em PT-BR. Conceito + regra prática + por que importa.>

## O que é

## Por que importa

## Como funciona

## Na prática

## Armadilhas

## Em entrevista

## Veja também
```

**Variações permitidas:**

- **Nota 12 (Armadilhas, cheatsheet):** estrutura tópica — lista de armadilhas + tabelas + decision tree. Não tem narrativa "Como funciona".
- **MOC (`Runtime e Event Loop.md`):** estrutura própria — abertura + Comece por aqui + Rotas alternativas + dataview de Todas as notas. `type: moc`.

**Tamanho típico:** 200-500 linhas por nota. Notas conceituais densas (04, 05, 11) podem ir até 600.

## 7. Rotas alternativas no MOC

### Rota completa
Sequencial 01 → 12. Recomendada na primeira leitura.

### Rota entrevista internacional
01 → 03 → 04 → 05 → 06 → 09 → 10. Foco em "explicar o motor pra entrevistador". Cobre: modelo, anatomia, fases, micro/macrotasks, mito do async, sintomas de problema.

### Rota debugging em produção
01 → 04 → 07 → 10 → 11. Foco em "minha app tá lenta, por quê?". Cobre: modelo, fases, I/O kernel vs pool, bloqueio, ferramentas.

### Rota async/await
03 → 05 → 08 → 09. Foco em entender o "porquê" das promises. Cobre: queues, microtasks, mecânica de Promise, async/await desmistificado.

## 8. Fontes principais

### Referências canônicas

- [Node.js docs — Event Loop, Timers, and `process.nextTick()`](https://nodejs.org/en/learn/asynchronous-work/event-loop-timers-and-nexttick) — referência canônica oficial
- [Node.js docs — Don't Block the Event Loop](https://nodejs.org/en/learn/asynchronous-work/dont-block-the-event-loop) — antipatterns oficiais
- [libuv docs — Design overview](https://docs.libuv.org/en/v1.x/design.html) — design da lib que faz o event loop
- [V8 Blog](https://v8.dev/blog) — para fundamentos de motor (uso pontual)

### Talks e artigos clássicos

- [Bert Belder — "Everything You Need to Know About Node.js Event Loop"](https://www.youtube.com/watch?v=PNa9OMajw9w) — Node.js Interactive 2016, ainda referência
- [Daniel Khan — "The Node.js Event Loop"](https://medium.com/@danielkhan/the-node-js-event-loop-72ed5e3f5e0a)
- [Bytearcher — "Parallel vs Async in Node.js"](https://bytearcher.com/articles/parallel-vs-asynchronous-in-node.js/) — esclarece thread pool vs kernel async
- [Matteo Collina — Streams + Event Loop talks (YouTube)](https://www.youtube.com/results?search_query=matteo+collina+event+loop) — buscar a mais recente

### Referências de diagnóstico

- [perf_hooks docs — `monitorEventLoopDelay`](https://nodejs.org/api/perf_hooks.html#perf_hooksmonitoreventloopdelayoptions)
- [clinic.js — Doctor](https://clinicjs.org/doctor/) e [Bubbleprof](https://clinicjs.org/bubbleprof/)
- [autocannon](https://github.com/mcollina/autocannon) — load testing

### A buscar conforme necessidade

- Posts recentes sobre `process.nextTick` vs `queueMicrotask` em Node 24
- Material atualizado sobre thread pool exausto em apps reais (case studies)
- Referências sobre Permission Model do Node 20+ tocando event loop indiretamente
- Anna Henningsen (addaleax) posts sobre internals
- Issues do repo `nodejs/node` que documentaram mudanças de comportamento entre versões

## 9. Decisões editoriais

- **Idioma:** PT-BR exclusivo nesta fase
- **Tom:** técnico mas acessível; TL;DR sempre presente
- **Versões assumidas:** Node 22 LTS e Node 24; V8 12.x/13.x; libuv 1.x. Quando uma feature é específica de uma versão, mencionar explicitamente
- **Frontmatter:** `publish: true`, `status: seedling`, tags `[node, event-loop, <conceito>]`
- **Wikilinks:** densidade alta para `[[Node.js]]` (tronco), `[[JavaScript Fundamentals]]`, e entre as 12 notas
- **Code samples:** mistura — JavaScript pra exemplos pedagógicos curtos (mostrar mecânica do runtime), TypeScript pra exemplos realistas de produção
- **Inglês:** apenas em "Em entrevista" (frases prontas + vocabulário) e em termos técnicos do ecossistema (event loop, microtask, etc.)

## 10. Tasks de poda do tronco

Ao fechar o galho, executar no `03-Dominios/JavaScript/Backend/Node.js.md`:

1. Substituir seção **"Arquitetura"** por callout `[!nota]` + wikilink pra `[[02 - V8, libuv e thread pool]]`
2. Substituir **"Single-threaded com non-blocking I/O"** por callout + wikilink pra `[[01 - Single-thread e non-blocking I-O]]`
3. Substituir **"Event loop phases — detalhado"** por callout + wikilinks pra `[[04 - As fases do event loop]]` + `[[05 - Microtasks - nextTick, queueMicrotask, Promise.then]]` + `[[06 - Macrotasks e timers - setTimeout, setInterval, setImmediate]]`
4. Substituir parte CPU-bound de **"Armadilhas comuns"** e **"Event loop blocking"** (de Troubleshooting) por wikilinks pras notas `[[10 - Bloqueio do event loop - sintomas e causas]]` + `[[11 - Diagnóstico do event loop]]`
5. Atualizar "Veja também" do tronco linkando o MOC `[[Runtime e Event Loop]]`
6. Atualizar `03-Dominios/Node/index.md` (MOC central) linkando `[[Runtime e Event Loop]]` na seção "Conteúdo"

A poda é **uma única task atômica** no plano de execução, ao final, quando todas as 12 notas estiverem prontas. Não podar antes — o tronco é referência ativa enquanto a sub-trilha está sendo escrita.

## 11. Riscos e mitigações

| Risco | Mitigação |
|---|---|
| Sobreposição com `[[JavaScript Fundamentals]]` na seção de event loop básico | Cada nota linka pra `[[JavaScript Fundamentals]]` quando o conceito é "JS puro"; o galho assume que o leitor já leu (ou pode consultar) e foca em **especificidades de Node** (libuv, fases, thread pool) |
| Notas 04 e 05 ficarem muito densas | Aceitar 500-600 linhas nessas; partir só se passar disso e a divisão fizer sentido (ex: nota 04 separa em "Fases do loop" + "O que é poll") |
| Mito "thread pool é onde tudo async acontece" persistir | Nota 07 é dedicada exclusivamente a desfazer essa confusão; outras notas linkam pra ela quando o tema aparecer |
| Code samples envelhecerem com mudanças de Node | Versões assumidas declaradas no frontmatter de cada nota afetada; revisão de `updated` quando uma nova LTS sair |
| `clinic.js` mudar de mantenedor / sair do ar | Apresentar 2-3 alternativas em diagnóstico (clinic, --inspect nativo, perf_hooks); não depender de uma única ferramenta de terceiros |
| Notas ficarem genéricas ("tutorial qualquer de event loop") | Toda nota tem seção "Em entrevista" com frase pronta concreta; "Armadilhas" com 2+ casos específicos; restrição absoluta de fabricação no plano |
| Confusão entre "macrotask" (termo informal) e "callback queue" / "task queue" (termo HTML spec) | Nota 06 dedica parágrafo a vocabulário: "Node usa 'callback queue' nos docs; comunidade usa 'macrotask' por contraste com 'microtask'; ambos OK em entrevista" |

## 12. Critérios de aceitação

A sub-trilha está completa quando:

1. Todas as 13 arquivos existem em `03-Dominios/Node/Runtime e Event Loop/`
2. Todos têm frontmatter completo com `publish: true`
3. MOC `Runtime e Event Loop.md` tem seção "Comece por aqui" com 12 notas linkadas em ordem + 4 rotas alternativas + dataview de "Todas as notas do galho"
4. Cada nota satisfaz a rubrica padrão:
   - TL;DR em callout `[!abstract]`
   - 2+ wikilinks pra outras notas do galho + 1+ wikilink pra `[[Node.js]]` (tronco) ou `[[JavaScript Fundamentals]]`
   - 3+ code samples em JS ou TS (notas conceituais puras 01, 03 podem ter menos)
   - Seção "Em entrevista" presente, com pelo menos 1 frase pronta em inglês + vocabulário-chave
   - Seção "Armadilhas" presente, com pelo menos 2 armadilhas concretas
   - Frontmatter completo (`publish: true`, `status: seedling`, tags `[node, event-loop, <conceito>]`)
   - Versões assumidas declaradas se relevante
   - PT-BR natural; termos técnicos em inglês mantidos
   - **Zero atribuição de experiência pessoal ao autor**
5. Tasks de poda do tronco (seção 10) executadas
6. MOC central `03-Dominios/Node/index.md` atualizado
7. Quartz publica corretamente em josenaldo.github.io
8. Pelo menos 4 notas têm exemplo de código testado em script standalone (rodável com `node arquivo.js` ou `node --experimental-strip-types arquivo.ts`)

## 13. Plano de execução

O plano detalhado de execução vai em `docs/superpowers/plans/2026-05-07-node-runtime-event-loop-execution.md` (gerado pela skill `superpowers:writing-plans` após aprovação deste spec).

A ordem de execução recomendada:

1. MOC (esqueleto sem links ainda) + 01 + 02 + 03 (mental model fundamental)
2. 04 (fases — central, ancora 05 e 06)
3. 05 + 06 + 07 sequencialmente (event loop deep dive)
4. 08 + 09 (async/await — depende de 03 e 05 estarem prontos)
5. 10 + 11 (bloqueio e diagnóstico)
6. 12 (fechamento, agrega)
7. Pass final no MOC (todos os wikilinks finais + dataview)
8. Tasks de poda do tronco (1 task atômica final)
9. Atualização do MOC central `Node/index.md`

## 14. Documentos relacionados

- `2026-05-07-node-roadmap-design.md` — roadmap macro dos 6 galhos (este spec é sub-trilha #1)
- Plano de execução (criado depois): `2026-05-07-node-runtime-event-loop-execution.md`
- Tronco a ser podado: `03-Dominios/JavaScript/Backend/Node.js.md`
- MOC central: `03-Dominios/Node/index.md`
- Spec de referência (formato análogo): `2026-04-26-typescript-react-design.md`
