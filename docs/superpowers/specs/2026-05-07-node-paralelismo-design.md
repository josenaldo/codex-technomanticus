---
title: "Spec — Sub-trilha Paralelismo (Galho 2)"
date: 2026-05-07
author: Josenaldo
status: draft
type: spec
publish: false
---

# Spec — Sub-trilha "Paralelismo" (Galho 2)

## 1. Contexto e motivação

Esta é a **segunda sub-trilha** (galho 2) do roadmap descrito em `2026-05-07-node-roadmap-design.md`. Pressupõe leitura desse roadmap — a metáfora tronco/galhos, os padrões editoriais comuns, e a política de poda do `Node.js.md` monolítico não são repetidos aqui.

O gatilho específico desta sub-trilha vem direto do galho 1. A nota `09 - async-await - o que é, o que não é` desfaz o mito "async = performance" e termina com a moral: pra **fugir do single-thread quando há trabalho CPU-bound**, é preciso paralelismo verdadeiro. As notas 10 e 11 (Bloqueio + Diagnóstico) fecham o ciclo "saber identificar o problema". Faltam as ferramentas para **resolver estruturalmente**.

Em Node 22+/24, há três ferramentas idiomáticas para fugir do single-thread:

- **Worker Threads** — múltiplas threads JS no mesmo processo, comunicando por mensagens ou memória compartilhada (`SharedArrayBuffer` + `Atomics`)
- **Cluster** — múltiplos processos Node compartilhando porta HTTP, em geral um por CPU
- **`child_process`** — spawn de processo externo (`exec`, `spawn`, `execFile`) ou child Node.js (`fork` com IPC)

Cada uma resolve um problema diferente, e a **decision tree** de "qual usar quando" é onde a maior parte das equipes erra. Cluster, em particular, é frequentemente usado em 2026 quando um orquestrador (Kubernetes, ECS) já está fazendo o trabalho de paralelismo de processos — virou ferramenta legada para a maioria dos cenários, mas continua relevante em deploys single-VM.

A sub-trilha existe pra dar ao leitor:

1. **Mental model** de quando paralelismo é a solução certa (e quando não é)
2. **Domínio operacional** das 3 ferramentas, com profundidade suficiente para entrevistas e produção
3. **Decision tree** clara, ancorada em contexto de produção 2026 (orquestradores)
4. **Patterns idiomáticos** — pool de workers, `transferList`, fork com IPC, exec seguro contra injection
5. **Vocabulário em inglês** para entrevista internacional

## 2. Objetivo

Produzir **12 notas atômicas + 1 MOC** (13 arquivos) em `03-Dominios/Node/Paralelismo/`, todas `publish: true`, em PT-BR, cobrindo do mental model de "quando paralelizar" ao domínio operacional das 3 ferramentas e à decisão de qual usar.

A trilha precisa ser:

- **Atômica** — cada nota linkável e citável separadamente
- **Híbrida em camadas** — TL;DR + corpo técnico, no padrão do roadmap
- **Complementar ao galho 1** — pressupõe leitor entende event loop, single-thread, async/await desmistificado
- **Idiomática 2026** — Node 22 LTS / 24, Worker Threads maduros, contexto de orquestradores como K8s/ECS
- **Orientada a entrevistas internacionais** — cada nota tem "Em entrevista" com frase pronta em inglês + vocabulário; rota alternativa "entrevista" no MOC

## 3. Escopo

### Em escopo

- 13 arquivos markdown em `03-Dominios/Node/Paralelismo/`
- Todos com `publish: true`
- Idioma: PT-BR; termos técnicos em inglês mantidos
- Wikilinks densos para `[[Node.js]]` (tronco), `[[Runtime e Event Loop]]` (galho 1, em particular nota 09 e 10), `[[JavaScript Fundamentals]]` quando relevante
- Pesquisa baseada em fontes primárias (Node docs, MDN para Atomics, piscina como referência canônica de worker pool)
- Tasks de poda do tronco executadas ao fechar o galho

### Fora de escopo

- **Streams** — galho 3. Worker Threads e streams se cruzam (workers podem produzir/consumir streams), mas o foco aqui é paralelismo de execução, não throughput de dados.
- **Frameworks** — galho 4. Examples usam Node "puro" ou Express minimal; não cobre integração com NestJS/Fastify.
- **Profiling avançado de Worker Threads** — galho 5 (Observability). A nota 06 (Pool) menciona que monitorar workers é crítico, mas não detalha ferramental.
- **Segurança em depth de child_process** — galho 6. A nota 08 cobre injeção via shell como armadilha (porque é frequente), mas sandboxing avançado, Permission Model, `vm` module ficam fora.
- **Modelo de memória completo do JS** — a nota 05 cobre o operacional de `SharedArrayBuffer`/`Atomics`, race conditions, wait/notify. Modelo de memória formal (memory_order da spec ECMA) fica fora; nota aponta pra spec.
- **Native addons (N-API, node-gyp)** — alternativa pra CPU-bound em alguns casos, mas é tema próprio e fora do escopo do galho.
- **Comparação Node vs Bun/Deno em paralelismo** — menções pontuais; comparação aprofundada é fora.

## 4. Audiência e barra de qualidade

**Audiência primária:** dev senior em prep para entrevista internacional. Já entendeu (galho 1) que Node é single-thread e que `async/await` não paraleliza nada; agora precisa **dominar fluentemente** as 3 ferramentas e saber explicar quando cada uma é a escolha certa.

**Audiência secundária:** o mesmo dev em produção, decidindo arquitetura de uma feature CPU-bound nova ou debugando um deploy que está saturando CPU.

**Barra de qualidade:** ao terminar a sub-trilha, o leitor deve **compreender ao nível exigido de um sênior** — explicar trade-offs, justificar escolhas, reconhecer patterns e armadilhas. Não é "saber implementar from scratch"; é "entender o suficiente pra decidir bem e ler/revisar código com olhar crítico".

Concretamente, ao terminar a sub-trilha o leitor deve conseguir:

1. Decidir, em <30 segundos, qual ferramenta (Worker Thread, Cluster, child_process) usar para um problema concreto
2. Explicar em inglês a diferença entre os 3 modelos de paralelismo (shared memory, shared port, separate process)
3. Reconhecer o pattern de worker pool, justificar por que ele bate worker-per-task, e citar `piscina` como referência canônica
4. Entender o protocolo de mensagens (`postMessage`, structured clone, `transferList`) e identificar quando uma cópia desnecessária está acontecendo num PR alheio
5. Identificar quando `SharedArrayBuffer` + `Atomics` é justificado vs preferir mensagens, e reconhecer race conditions canônicas ao revisar código
6. Explicar o padrão Cluster (primary/worker, port sharing, restart) e — mais importante — argumentar quando **não** usar Cluster (orquestrador já paraleliza)
7. Diferenciar `exec` / `execFile` / `spawn`, em particular as implicações de segurança (shell injection) que separam um sênior de um pleno em code review
8. Diferenciar `fork` de `spawn` e justificar quando `fork` ainda ganha de Worker Thread (isolamento total de memória, native modules incompatíveis, supervisor tree)
9. Reconhecer pelo menos 5 armadilhas operacionais ao ler código (Worker sem terminate, IPC leak, race em SharedArrayBuffer, exec com input do usuário, cluster com state em memória)

## 5. Estrutura da sub-trilha (13 arquivos)

### MOC

| # | Arquivo | Propósito |
|---|---|---|
| — | `Paralelismo.md` | MOC do galho. Trilha sequencial 01→12 + 5 rotas alternativas. Dataview de "Todas as notas do galho". Linka pro MOC central `Node/index.md`, pro tronco `[[Node.js]]`, e pro galho anterior `[[Runtime e Event Loop]]`. |

### Bloco A — Mental model e fundamentos (2 notas)

| # | Arquivo | Propósito | Conteúdo-chave |
|---|---|---|---|
| 01 | `01 - Por que paralelismo em Node.md` | Quando o single-thread aperta | CPU-bound vs I/O-bound (revisão do galho 1). Sintomas que pedem paralelismo verdadeiro: event loop lag persistente mesmo após otimizações, latência conjunta acima do tolerável, throughput limitado pela CPU. Alternativas a considerar **antes** de paralelizar: streaming (preview galho 3), paginação, refator do algoritmo, mover trabalho pra background queue. Quando paralelismo é a resposta certa. Conexão direta com galho 1 nota 09. |
| 02 | `02 - As 3 ferramentas - Worker Threads, Cluster, child_process.md` | Visão geral comparativa | Tabela rica: ferramenta · modelo · isolamento · custo de criação · IPC · uso típico. Worker Threads = shared-memory model (mesmo processo, threads). Cluster = shared-port model (múltiplos processos compartilhando porta HTTP). child_process = separate-process model (processos independentes). Apontador pras notas detalhadas (3-9). Decisão preliminar; decisão completa fica em nota 11. |

### Bloco B — Worker Threads (4 notas)

| # | Arquivo | Propósito | Conteúdo-chave |
|---|---|---|---|
| 03 | `03 - Worker Threads - fundamentos.md` | Criação, lifecycle, terminate | API básica: `new Worker(file, { workerData })`, `parentPort`, `worker.on('message'/'error'/'exit'/'online')`, `worker.terminate()`. Custo de criação (~ms para Worker; ~100ms para processo). `isMainThread` flag. Modos: arquivo separado vs inline (`new Worker(__filename, ...)`). Quando o Worker termina por conta própria (sem mais trabalho), quando precisa de `terminate` explícito. |
| 04 | `04 - Comunicação entre workers - postMessage e MessageChannel.md` | Mensagens estruturadas + zero-copy | Algoritmo de clone estruturado: tipos suportados (objects, arrays, Map, Set, Date, RegExp, Buffer); não suportados (functions, classes, DOM nodes). `transferList` para passar `ArrayBuffer`/`MessagePort` sem cópia (movido, não copiado). `MessageChannel` para canais bidirecionais isolados do `parentPort` (útil em arquiteturas de multiple workers). Tipos do `worker_threads` (`MessagePort`, `Worker`). |
| 05 | `05 - Memória compartilhada - SharedArrayBuffer e Atomics.md` | Concorrência real em JS | `SharedArrayBuffer` (visível simultaneamente em múltiplos workers, sem clone). `Atomics` para operações atômicas: `Atomics.load/store/add/sub/compareExchange`. `Atomics.wait` / `Atomics.notify` para sincronização. Race conditions canônicas (incremento não-atômico). Casos legítimos: matrizes grandes em ML/imagens, contadores compartilhados, semáforos. Preferir mensagens quando possível. Restrições de segurança (cross-origin isolation requirements em browser; em Node basta usar). |
| 06 | `06 - Pool de workers - pattern de produção.md` | Reusar workers, queue, bounded concurrency | Por que pool > worker-per-task: custo de criação amortizado, limite de concorrência previsível, GC pressure menor. Implementação canônica do zero: queue + N workers + handoff via `MessagePort`. `piscina` como referência (Matteo Collina). Lifecycle: lazy creation, max idle timeout, graceful shutdown propagando ao pool. Comparação com lazy creation (worker-per-task). |

### Bloco C — Multi-processo (3 notas)

| # | Arquivo | Propósito | Conteúdo-chave |
|---|---|---|---|
| 07 | `07 - Cluster - escalando HTTP por CPU.md` | Primary/worker, fork, port sharing | API: `cluster.isPrimary`, `cluster.fork()`, eventos `online`/`exit`/`disconnect`. Restart automático no `exit`. Como o port sharing funciona: round-robin no Linux (default), kernel-balanced no Windows. Sticky sessions com `@socket.io/sticky` ou similar (necessário para WebSocket). Graceful shutdown: drain via `disconnect`, fechar handles, exit. Comportamento em Node 22+. |
| 08 | `08 - child_process com exec e spawn.md` | Executar comandos externos | `exec`: bufferizado, conveniente, **vulnerável a shell injection** se input do user não sanitizado. `execFile`: sem shell, mais seguro. `spawn`: streaming, sem buffer limit, ideal para output longo (ffmpeg, build scripts). Configuração de `stdio`, `encoding`, signal handling (SIGTERM, SIGKILL). **Segurança canônica**: nunca passar input do user pro shell; preferir `execFile`/`spawn` com array de args. |
| 09 | `09 - child_process com fork - Node child com IPC.md` | Spawn de child Node.js específico | `fork('./worker.js')` cria child Node com canal IPC built-in (`child.send()` / `process.on('message')`). Quando preferir fork sobre Worker Thread: isolamento total de memória, separate event loop, native modules incompatíveis com Worker Threads, processo precisa morrer/respawn por design (workflow tipo "actor" ou "supervisor tree"). Custo de criação maior (~100ms vs ~ms do Worker). |

### Bloco D — Produção (2 notas)

| # | Arquivo | Propósito | Conteúdo-chave |
|---|---|---|---|
| 10 | `10 - Cluster vs PM2 vs Kubernetes - quem orquestra.md` | Contexto de produção 2026 | História: cluster nativo brilhou em ~2014-2018 quando deploys eram em VMs single-host. PM2 fez cluster + watchdog + logs + zero-downtime reload (era a escolha default ~2018-2020). Hoje (2026): K8s/ECS/Nomad fazem fork em escala diferente — 1 pod por core, autoscaling horizontal, rolling updates declarativos. Cluster nativo virou raro em prod nova; PM2 ainda usado em VPS/single-VM. Quando cluster ainda faz sentido: dev local, single-VM deploys (small SaaS, internal tooling), worker pools de fork orquestrados pela própria app. |
| 11 | `11 - Decision tree - qual ferramenta para qual problema.md` | Síntese com fluxograma | Fluxograma ASCII completo: pergunta → ramificação. CPU-bound em handler? → Worker Thread (e considerar pool). Escalar HTTP além do single-thread? → orquestrador (K8s, PM2); cluster nativo só se single-VM. Rodar comando externo? → `spawn` (ou `execFile` se output curto). Spawn de child Node com isolamento? → `fork`. Tabela complementar: problema → ferramenta → razão. Apontador pras notas relevantes. |

### Bloco E — Fechamento (1 nota)

| # | Arquivo | Propósito | Conteúdo-chave |
|---|---|---|---|
| 12 | `12 - Armadilhas, regras práticas, cheatsheet.md` | Síntese e referência | Top 10 armadilhas: (1) Worker sem `terminate` → leak; (2) IPC leak (mensagens acumulando em fila); (3) race em `SharedArrayBuffer` sem `Atomics`; (4) `exec` com input do user → shell injection; (5) cluster com state em memória (cache local) → comportamento inconsistente entre workers; (6) fork sem cleanup de child em parent crash → zombies; (7) `transferList` esquecido → cópia em vez de move; (8) Worker preso em loop síncrono → `terminate` é a única opção; (9) Cluster + sticky sessions sem reverse proxy ciente; (10) Node child via `spawn` com `shell: true` → injection. Cheatsheet visual: 3 ferramentas × 5 atributos. Decision tree compactada. Vocabulário PT→EN consolidado. Apontador pros próximos galhos. |

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
  - paralelismo
  - <conceito-tag específica: worker-threads, cluster, child-process, atomics, etc>
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

- **Nota 12 (cheatsheet):** estrutura tópica — lista de armadilhas + tabelas + decision tree. Não tem narrativa "Como funciona".
- **MOC (`Paralelismo.md`):** estrutura própria — abertura + Comece por aqui + Rotas alternativas + dataview. `type: moc`.

**Tamanho típico:** 200-500 linhas por nota. Notas conceituais densas (05 SharedArrayBuffer, 06 Pool, 11 Decision tree) podem ir até 600.

## 7. Rotas alternativas no MOC

### Rota completa
Sequencial 01 → 12. Recomendada na primeira leitura.

### Rota entrevista internacional
01 → 02 → 03 → 05 → 07 → 11. Foco em "explicar os 3 modelos pra entrevistador". Cobre: motivação, visão geral, Worker fundamentos, memória compartilhada, cluster, decision tree.

### Rota produção
01 → 06 → 07 → 10 → 12. Foco em "pôr em produção". Cobre: motivação, pool, cluster, contexto orquestradores, armadilhas.

### Rota CPU-bound
01 → 03 → 04 → 06. Foco em "escapar do bloqueio com Worker Threads". Cobre: motivação, Worker fundamentos, comunicação, pool.

### Rota integração com OS
01 → 02 → 08 → 09. Foco em "rodar comandos externos e spawn de Node". Cobre: motivação, visão geral, exec/spawn, fork.

## 8. Fontes principais

### Referências canônicas

- [Node.js docs — `worker_threads`](https://nodejs.org/api/worker_threads.html)
- [Node.js docs — `cluster`](https://nodejs.org/api/cluster.html)
- [Node.js docs — `child_process`](https://nodejs.org/api/child_process.html)
- [MDN — `Atomics`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Atomics)
- [MDN — `SharedArrayBuffer`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/SharedArrayBuffer)
- [Structured clone algorithm](https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API/Structured_clone_algorithm)

### Referências de produção e libs

- [piscina](https://github.com/piscinajs/piscina) — worker pool lib de referência (Matteo Collina); design e API são modelo
- [PM2 docs](https://pm2.keymetrics.io/) — comparação histórica
- [@socket.io/sticky](https://github.com/socketio/socketio-sticky-session) — sticky sessions com cluster

### Talks e artigos

- Anna Henningsen (addaleax) — talks/posts sobre `worker_threads` internals
- Matteo Collina — "Node.js Worker Threads in production" (buscar a mais recente)

### A buscar conforme necessidade

- Discussões recentes sobre `cluster` em 2026 (deprecation? mudanças?)
- Material sobre Permission Model do Node 20+ tocando child_process indiretamente
- Issues do `nodejs/node` documentando mudanças de `worker_threads` entre 22 e 24

## 9. Decisões editoriais

- **Idioma:** PT-BR exclusivo nesta fase
- **Tom:** técnico mas acessível; TL;DR sempre presente
- **Versões assumidas:** Node 22 LTS e Node 24; `worker_threads` estável; `cluster` estável
- **Frontmatter:** `publish: true`, `status: seedling`, tags `[node, paralelismo, <conceito>]`
- **Wikilinks:** densidade alta para `[[Node.js]]` (tronco), `[[Runtime e Event Loop]]` (galho 1, especialmente notas 09 e 10), e entre as 12 notas
- **Code samples:** mistura — JavaScript pra exemplos pedagógicos curtos, TypeScript pra exemplos realistas de produção
- **Inglês:** apenas em "Em entrevista" e em termos técnicos (Worker, message, transferList, fork, spawn, SharedArrayBuffer, Atomics, etc.)

## 10. Tasks de poda do tronco

Ao fechar o galho, executar no `03-Dominios/JavaScript/Backend/Node.js.md`:

1. Substituir seção **`### Worker Threads, cluster, child_process — as 3 formas de paralelismo`** por callout `[!nota]` com wikilinks pra:
   - `[[Paralelismo]]` (MOC do galho)
   - `[[02 - As 3 ferramentas - Worker Threads, Cluster, child_process]]` (visão geral)
   - `[[03 - Worker Threads - fundamentos]]`
   - `[[07 - Cluster - escalando HTTP por CPU]]`
   - `[[08 - child_process com exec e spawn]]`
   - `[[09 - child_process com fork - Node child com IPC]]`
2. Adicionar `[[Paralelismo]]` no `## Veja também` do tronco como segundo bullet (após `[[Runtime e Event Loop]]` que foi adicionado no galho 1)
3. Atualizar `updated: 2026-05-07` no frontmatter do tronco (se não estiver já)
4. Atualizar `03-Dominios/Node/index.md` (MOC central) adicionando `[[Paralelismo]]` na seção "Galhos da trilha Node Senior"

## 11. Riscos e mitigações

| Risco | Mitigação |
|---|---|
| Sobreposição entre nota 03 (Worker fundamentos) e 04 (comunicação) | 03 cobre lifecycle/terminate/eventos; 04 cobre exclusivamente payload e protocolo. Linhas claras de divisão. |
| Nota 05 (SharedArrayBuffer + Atomics) ficar densa | Sem limite artificial de tamanho — concorrência com memória compartilhada é tema profundo e merece a profundidade que pedir, mesmo que estoure 600+ linhas. O leitor sênior precisa do panorama completo: estados de memória, todas as ops do `Atomics` (load/store/add/sub/and/or/xor/exchange/compareExchange), `wait`/`notify`, race conditions canônicas, e quando preferir mensagens. Apontar pra spec ECMAScript pra quem quiser o modelo formal. |
| Nota 09 (fork) ficar redundante com Worker Threads em 2026 | Nota explicita os 4 casos onde fork ainda ganha (isolamento total, native modules incompatíveis, supervisor tree, processo descartável). Sem isso, é tentador omitir. |
| Cluster ficar desatualizado rapidamente | Nota 10 declara contexto 2026 explicitamente; usa "PM2 e K8s" como exemplos sem se aprofundar em features específicas que evoluem. |
| Notas operacionais ficarem genéricas demais | Toda nota tem code sample concreto + seção "Em entrevista" com frase pronta + "Armadilhas" com 2+ casos específicos. Restrição de fabricação no plano. |
| Confusão entre "shared memory" (Worker Threads via SharedArrayBuffer) e "shared port" (Cluster) | Nota 02 introduz os 3 modelos com nomenclatura explícita; nota 11 reforça na decision tree. |
| Nota 11 (decision tree) duplicar nota 02 (visão geral) | 02 é INTRO ("aqui estão suas 3 ferramentas"); 11 é OUTRO ("dado um problema X, escolha Y"). Diferença é o ângulo: catalogar vs decidir. |

## 12. Critérios de aceitação

A sub-trilha está completa quando:

1. Todas as 13 arquivos existem em `03-Dominios/Node/Paralelismo/`
2. Todos têm frontmatter completo com `publish: true`
3. MOC `Paralelismo.md` tem seção "Comece por aqui" com 12 notas linkadas em ordem + 5 rotas alternativas + dataview de "Todas as notas do galho"
4. Cada nota satisfaz a rubrica padrão:
   - TL;DR em callout `[!abstract]`
   - 2+ wikilinks pra outras notas do galho + 1+ wikilink pra `[[Node.js]]` (tronco) ou `[[Runtime e Event Loop]]` (galho 1)
   - 3+ code samples em JS ou TS
   - Seção "Em entrevista" presente, com pelo menos 1 frase pronta em inglês + vocabulário-chave
   - Seção "Armadilhas" presente, com pelo menos 2 armadilhas concretas
   - Frontmatter completo (`publish: true`, `status: seedling`, tags `[node, paralelismo, <conceito>]`)
   - Versões assumidas declaradas se relevante
   - PT-BR natural; termos técnicos em inglês mantidos
   - **Zero atribuição de experiência pessoal ao autor**
5. Tasks de poda do tronco (seção 10) executadas
6. MOC central `03-Dominios/Node/index.md` atualizado (galho 2 listado)
7. Quartz publica corretamente
8. Pelo menos 4 notas têm code sample testável em script standalone (ex: pool de workers minimal, exec vs execFile, cluster com `cluster.isPrimary`)

## 13. Plano de execução

O plano detalhado de execução vai em `docs/superpowers/plans/2026-05-07-node-paralelismo-execution.md` (gerado pela skill `superpowers:writing-plans` após aprovação deste spec).

A ordem de execução recomendada:

1. MOC (esqueleto sem links ainda) + 01 + 02 (mental model + visão geral)
2. 03 (Worker fundamentos — base do bloco B)
3. 04 + 05 + 06 sequencialmente (Worker Threads deep dive)
4. 07 + 08 + 09 (multi-processo)
5. 10 + 11 (produção)
6. 12 (fechamento, agrega)
7. Pass final no MOC (todos os wikilinks finais + dataview)
8. Tasks de poda do tronco (1 task atômica final)
9. Atualização do MOC central `Node/index.md`

## 14. Documentos relacionados

- `2026-05-07-node-roadmap-design.md` — roadmap macro dos 6 galhos (este spec é sub-trilha #2)
- `2026-05-07-node-runtime-event-loop-design.md` — spec do galho 1 (Runtime e Event Loop), referência de formato
- `2026-05-07-node-runtime-event-loop-execution.md` — plano do galho 1, referência de estrutura de tasks
- Plano de execução do galho 2 (criado depois): `2026-05-07-node-paralelismo-execution.md`
- Tronco a ser podado: `03-Dominios/JavaScript/Backend/Node.js.md`
- MOC central: `03-Dominios/Node/index.md`
- Galho anterior fechado (referência): `03-Dominios/Node/Runtime e Event Loop/`
