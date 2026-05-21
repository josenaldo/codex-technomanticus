---
title: "Plano — Execução da Sub-trilha Paralelismo (Galho 2)"
date: 2026-05-07
status: ready
type: plan
publish: false
---

# Sub-trilha Paralelismo — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produzir 12 notas atômicas + 1 MOC em `03-Dominios/Node/Paralelismo/`, em PT-BR, todas `publish: true`, cobrindo Worker Threads (fundamentos, comunicação, SharedArrayBuffer/Atomics, pool), Cluster, child_process (exec/spawn, fork), contexto de produção (PM2/K8s) e decision tree — para um dev senior em prep para entrevista internacional. Ao final, podar a seção correspondente do tronco `JavaScript/Backend/Node.js.md` e atualizar o MOC central de `03-Dominios/Node/index.md`.

**Architecture:** Sub-trilha sequencial em 5 blocos (Mental model + fundamentos → Worker Threads → Multi-processo → Produção → Fechamento) + 1 MOC com 5 rotas alternativas. Pressupõe galho 1 (Runtime e Event Loop) como pré-requisito; em particular as notas 09 (async/await desmistificado) e 10 (Bloqueio do event loop) são wikilinks frequentes. Cada nota é atômica, segue estrutura híbrida (TL;DR + corpo técnico), com code samples em JS ou TS (Node 22 LTS / 24, `worker_threads` estável, `cluster` estável), e seção "Em entrevista" para preparação internacional.

**Tech Stack:** Markdown + Obsidian Flavored Markdown (wikilinks, callouts, dataview), Quartz para publicação no site público (josenaldo.github.io). Sem código a executar como sistema — code samples didáticos validáveis via `node script.js` ou `node --experimental-strip-types script.ts` quando útil. Bibliografia âncora: Node docs (`worker_threads`, `cluster`, `child_process`), MDN (`Atomics`, `SharedArrayBuffer`), `piscina` repo (worker pool de referência), PM2 docs.

---

## ⚠️ Restrição absoluta — fabricação

A memória [Nunca inventar dados sobre o usuário](/home/josenaldo/.claude/projects/-home-josenaldo-repos-personal-codex-technomanticus/memory/feedback_no_fabrication.md) é regra inegociável. **Nenhuma nota pode atribuir ao autor experiências profissionais, projetos, clientes, métricas ou casos não-vividos.**

A seção "Na prática" de cada nota usa:

- "Padrão observado em libs do ecossistema (piscina, PM2, Express, NestJS)"
- "Caso típico em microserviços com CPU-bound (image processing, ML inference, hashing)"
- "Armadilha comum reportada na comunidade"
- Citações com fonte verificável (docs oficiais, talks identificadas, repos públicos)
- Hipotéticos explícitos ("Imagine um endpoint que recebe uploads e calcula bcrypt...")

Quando faltar contexto factual, **PERGUNTAR antes de escrever** — nunca preencher com plausibilidade.

---

## File Structure

13 arquivos novos em `03-Dominios/Node/Paralelismo/`:

```
03-Dominios/Node/Paralelismo/
├── Paralelismo.md                                                        # MOC (Task 1)
├── 01 - Por que paralelismo em Node.md                                   # Task 2
├── 02 - As 3 ferramentas - Worker Threads, Cluster, child_process.md     # Task 3
├── 03 - Worker Threads - fundamentos.md                                  # Task 4
├── 04 - Comunicação entre workers - postMessage e MessageChannel.md      # Task 5
├── 05 - Memória compartilhada - SharedArrayBuffer e Atomics.md           # Task 6
├── 06 - Pool de workers - pattern de produção.md                         # Task 7
├── 07 - Cluster - escalando HTTP por CPU.md                              # Task 8
├── 08 - child_process com exec e spawn.md                                # Task 9
├── 09 - child_process com fork - Node child com IPC.md                   # Task 10
├── 10 - Cluster vs PM2 vs Kubernetes - quem orquestra.md                 # Task 11
├── 11 - Decision tree - qual ferramenta para qual problema.md            # Task 12
└── 12 - Armadilhas, regras práticas, cheatsheet.md                       # Task 13
```

**Final integration (Task 14, 15, 16):**
- Pass final no MOC inserindo todos os wikilinks + dataview
- Poda do tronco `03-Dominios/JavaScript/Backend/Node.js.md` (uma seção)
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
  - paralelismo
  - <tag específica: worker-threads, cluster, child-process, atomics, pool, etc>
aliases:
  - <opcional: alternativas naturais de busca>
---

# <Título>

> [!abstract] TL;DR
> <2-4 linhas em PT-BR direto. Define o conceito-chave + a regra prática + por que importa.>

## O que é

<1-3 parágrafos definindo o conceito da nota. Pressupõe leitura de [[Runtime e Event Loop]] (galho 1) ou consulta paralela.>

## Por que importa

<O problema que isso resolve no dia a dia. Onde o desenvolvedor "trava" sem esse conhecimento.>

## Como funciona

<Aprofundamento técnico com code samples em JS ou TS. Mostrar o pattern, depois variações. Edge cases.>

## Na prática

<Exemplo realista. Sem fabricar experiência do autor — usar "padrão observado em X", "lib Y faz isso", hipotéticos explícitos.>

## Armadilhas

<Gotchas específicos. O que erra normalmente. Mínimo 2 itens.>

## Em entrevista

<Frase pronta em inglês para explicar o conceito. Vocabulário-chave (PT → EN). Pergunta típica + resposta defensiva.>

## Veja também

- [[Outra nota da trilha]] — relação
- [[Runtime e Event Loop]] — galho 1 (pré-requisito)
- [[Node.js]] — tronco
```

### Variações permitidas

- **Nota 12 (Armadilhas, cheatsheet):** estrutura tópica — lista numerada de armadilhas + tabelas + decision tree compactada. Não tem narrativa "Como funciona".
- **MOC (`Paralelismo.md`):** estrutura própria — abertura + Comece por aqui + 5 rotas alternativas + dataview. `type: moc`.

### Critérios de qualidade (rubrica aplicada por nota)

- [ ] TL;DR em callout `[!abstract]`, 2-4 linhas, compreensível em <30s
- [ ] 2+ wikilinks pra outras notas do galho + 1+ wikilink pra `[[Node.js]]` (tronco) ou `[[Runtime e Event Loop]]` (galho 1)
- [ ] 3+ code samples em JS ou TS (notas conceituais 01, 02 podem ter menos se forem síntese)
- [ ] Seção "Em entrevista" com pelo menos 1 frase pronta em inglês + vocabulário-chave (mínimo 4 termos PT→EN)
- [ ] Seção "Armadilhas" com pelo menos 2 armadilhas concretas
- [ ] Frontmatter completo (`publish: true`, `status: seedling`, tags `[node, paralelismo, <específica>]`)
- [ ] Versões assumidas declaradas se relevante (Node 22 LTS / 24)
- [ ] PT-BR natural; termos técnicos em inglês mantidos (Worker, postMessage, transferList, fork, spawn, etc.)
- [ ] **Zero atribuição de experiência pessoal ao autor** (regra absoluta)
- [ ] Nenhuma alegação técnica não-trivial sem fonte ou code sample que comprove

---

## Bibliografia centralizada (consulta rápida durante a escrita)

### Referências canônicas

- **Node.js docs — `worker_threads`:** `https://nodejs.org/api/worker_threads.html`
- **Node.js docs — `cluster`:** `https://nodejs.org/api/cluster.html`
- **Node.js docs — `child_process`:** `https://nodejs.org/api/child_process.html`
- **MDN — `Atomics`:** `https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Atomics`
- **MDN — `SharedArrayBuffer`:** `https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/SharedArrayBuffer`
- **Structured clone algorithm:** `https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API/Structured_clone_algorithm`

### Referências de produção e libs

- **piscina** (worker pool de referência, Matteo Collina): `https://github.com/piscinajs/piscina`
- **PM2 docs:** `https://pm2.keymetrics.io/`
- **@socket.io/sticky:** `https://github.com/socketio/socketio-sticky-session`

### Notas no vault (referências paralelas)

- `03-Dominios/JavaScript/Backend/Node.js.md` — tronco a ser podado (uma seção)
- `03-Dominios/Node/index.md` — MOC central a ser atualizado
- `03-Dominios/Node/Runtime e Event Loop/` — galho 1, pré-requisito; em particular notas 09 (async/await) e 10 (Bloqueio)
- `03-Dominios/JavaScript/Core/JavaScript Fundamentals.md` (caminho confirmado em galho 1 Task 0)
- `03-Dominios/JavaScript/Core/TypeScript.md` (caminho confirmado)

### A buscar conforme necessidade

- Discussões recentes sobre `cluster` em 2026 (deprecation? mudanças de API?)
- Talks/posts de Anna Henningsen (addaleax) sobre `worker_threads` internals
- Material sobre Permission Model do Node 20+ tocando `child_process` indiretamente
- Comparações Worker Threads vs `fork` em casos reais (issues do `nodejs/node`)

---

## Task 0: Pré-flight

**Files:**
- Create: `03-Dominios/Node/Paralelismo/` (diretório)

- [ ] **Step 1: Criar o diretório**

```bash
mkdir -p "03-Dominios/Node/Paralelismo"
```

Verificar com:

```bash
ls -la "03-Dominios/Node/Paralelismo"
```

Esperado: diretório vazio.

- [ ] **Step 2: Confirmar memória de no-fabrication carregada**

```bash
cat /home/josenaldo/.claude/projects/-home-josenaldo-repos-personal-codex-technomanticus/memory/MEMORY.md | grep -i "fabrica\|invent"
```

Esperado: ao menos uma linha referenciando `feedback_no_fabrication.md`. Se não estiver, abortar e pedir reload.

- [ ] **Step 3: Confirmar memória de tronco/galhos pattern carregada**

```bash
cat /home/josenaldo/.claude/projects/-home-josenaldo-repos-personal-codex-technomanticus/memory/MEMORY.md | grep -i "tronco\|galho"
```

Esperado: linha referenciando `project_tronco_galhos_pattern.md`. Se não estiver, registrar e prosseguir (não é bloqueante mas deve ser consultada para coesão com galho 1).

- [ ] **Step 4: Sanity check do tronco — confirmar a seção a podar**

Ler `03-Dominios/JavaScript/Backend/Node.js.md` e confirmar que existe a seção:

- `### Worker Threads, cluster, child_process — as 3 formas de paralelismo`

Anotar o número da linha exato onde a seção começa e onde termina (próxima `###` ou `##`). Se o nome estiver diferente, anotar exatamente como aparece.

```bash
grep -n "Worker Threads.*paralelismo\|Worker Threads.*cluster" "03-Dominios/JavaScript/Backend/Node.js.md"
```

- [ ] **Step 5: Confirmar wikilinks do galho 1 funcionando**

O galho 2 vai linkar pro galho 1 frequentemente. Confirmar que os arquivos existem:

```bash
ls "03-Dominios/Node/Runtime e Event Loop/" | grep -E "(09|10|MOC|Runtime)"
```

Esperado: ver `09 - async-await - o que é, o que não é.md`, `10 - Bloqueio do event loop - sintomas e causas.md`, `Runtime e Event Loop.md` (MOC).

- [ ] **Step 6: Sanity check das fontes-âncora**

Disparar WebFetch em paralelo para as 4 fontes mais críticas:

```
WebFetch: https://nodejs.org/api/worker_threads.html
WebFetch: https://nodejs.org/api/cluster.html
WebFetch: https://nodejs.org/api/child_process.html
WebFetch: https://github.com/piscinajs/piscina
```

Confirmar acesso. Se alguma falhar, registrar e usar fontes alternativas (MDN, talks).

- [ ] **Step 7: Commit pré-flight**

```bash
git add -A
git commit -m "feat(node-paralelismo): create directory for Paralelismo sub-trail"
```

(Sem `Co-Authored-By` Claude — regra do usuário.)

---

## Task 1: MOC esqueleto

**Files:**
- Create: `03-Dominios/Node/Paralelismo/Paralelismo.md`

- [ ] **Step 1: Criar o MOC esqueleto**

Criar `03-Dominios/Node/Paralelismo/Paralelismo.md` com este conteúdo (a seção "Sobre este galho" tem placeholder a preencher na Task 14):

```markdown
---
title: "Paralelismo"
created: 2026-05-07
updated: 2026-05-07
type: moc
status: seedling
publish: true
tags:
  - node
  - paralelismo
  - moc
aliases:
  - Worker Threads
  - Galho 2 - Paralelismo
---

# Paralelismo

> [!abstract] TL;DR
> Galho 2 da trilha Node Senior. Cobre as 3 ferramentas para fugir do single-thread: Worker Threads (CPU-bound em mesmo processo), Cluster (escalar HTTP por CPU), child_process (rodar comando externo ou spawn de Node). Inclui SharedArrayBuffer/Atomics, pool de workers, contexto de produção (PM2 vs K8s), e decision tree. Pré-requisito: galho 1 (Runtime e Event Loop).

## Sobre este galho

(introdução curta — preencher na Task 14)

## Comece por aqui — trilha completa (12 notas)

### Bloco A — Mental model e fundamentos

1. [[01 - Por que paralelismo em Node]]
2. [[02 - As 3 ferramentas - Worker Threads, Cluster, child_process]]

### Bloco B — Worker Threads

3. [[03 - Worker Threads - fundamentos]]
4. [[04 - Comunicação entre workers - postMessage e MessageChannel]]
5. [[05 - Memória compartilhada - SharedArrayBuffer e Atomics]]
6. [[06 - Pool de workers - pattern de produção]]

### Bloco C — Multi-processo

7. [[07 - Cluster - escalando HTTP por CPU]]
8. [[08 - child_process com exec e spawn]]
9. [[09 - child_process com fork - Node child com IPC]]

### Bloco D — Produção

10. [[10 - Cluster vs PM2 vs Kubernetes - quem orquestra]]
11. [[11 - Decision tree - qual ferramenta para qual problema]]

### Bloco E — Fechamento

12. [[12 - Armadilhas, regras práticas, cheatsheet]]

## Rotas alternativas

### Rota entrevista internacional

01 → 02 → 03 → 05 → 07 → 11. Foco em "explicar os 3 modelos pra entrevistador".

### Rota produção

01 → 06 → 07 → 10 → 12. Foco em "pôr em produção".

### Rota CPU-bound

01 → 03 → 04 → 06. Foco em "escapar do bloqueio com Worker Threads".

### Rota integração com OS

01 → 02 → 08 → 09. Foco em "rodar comandos externos e spawn de Node".

## Todas as notas

\`\`\`dataview
TABLE status, updated
FROM "03-Dominios/Node/Paralelismo"
WHERE type = "concept"
SORT file.name ASC
\`\`\`

## Veja também

- [[03-Dominios/Node/index|Node.js (MOC central)]]
- [[Node.js]] — tronco (deep dive panorâmico)
- [[Runtime e Event Loop]] — galho 1 (pré-requisito)
```

**IMPORTANT:** No conteúdo do arquivo, substitua os `\`\`\`` (com backslashes) por triple backticks reais. Os backslashes acima são apenas para escape neste plano. O dataview deve ficar como bloco de código com triple backticks reais e o language tag `dataview`.

- [ ] **Step 2: Verificar frontmatter e estrutura**

Confirmar:
- `type: moc`
- `publish: true`
- 12 notas listadas em ordem em 5 blocos (A, B, C, D, E)
- 4 rotas alternativas presentes (entrevista, produção, CPU-bound, integração com OS) — a "rota completa" implícita é o sequencial 01→12 sob "Comece por aqui"
- Dataview com `SORT file.name ASC`
- Wikilinks pro MOC central, tronco, e galho 1

- [ ] **Step 3: Commit**

```bash
git add "03-Dominios/Node/Paralelismo/Paralelismo.md"
git commit -m "feat(node-paralelismo): add MOC skeleton for Paralelismo branch"
```

---

## Task 2: Nota 01 — Por que paralelismo em Node

**Files:**
- Create: `03-Dominios/Node/Paralelismo/01 - Por que paralelismo em Node.md`

**Conteúdo-chave do spec (Bloco A):**

> CPU-bound vs I/O-bound (revisão do galho 1). Sintomas que pedem paralelismo verdadeiro: event loop lag persistente mesmo após otimizações, latência conjunta acima do tolerável, throughput limitado pela CPU. Alternativas a considerar **antes** de paralelizar: streaming (preview galho 3), paginação, refator do algoritmo, mover trabalho pra background queue. Quando paralelismo é a resposta certa. Conexão direta com galho 1 nota 09.

- [ ] **Step 1: Pesquisa-âncora**

Sem WebFetch nessa nota — é síntese do galho 1 + framing do galho 2. Reler:

- `03-Dominios/Node/Runtime e Event Loop/09 - async-await - o que é, o que não é.md` (mito da performance)
- `03-Dominios/Node/Runtime e Event Loop/10 - Bloqueio do event loop - sintomas e causas.md` (sintomas)

para garantir vocabulário e pontes coesos.

- [ ] **Step 2: Criar arquivo + frontmatter**

```yaml
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
```

- [ ] **Step 3: Escrever a nota completa (250-400 linhas)**

Cobrir, em PT-BR, em ordem:

- **TL;DR (callout `[!abstract]`):** Node é single-thread e isso geralmente está certo. Mas há casos onde paralelismo é a única saída: CPU-bound persistente, event loop lag que não cede com otimização, throughput limitado. Antes de paralelizar, considere streaming, paginação, refator. Quando essas falham, há 3 ferramentas (Worker Threads, Cluster, child_process) — escolha depende do problema.
- **## O que é:** definição prática. Paralelismo no contexto Node = executar trabalho **simultaneamente** em outras threads ou processos, fora do event loop principal. Distinto de concorrência (event loop alterna entre tarefas). Cobre: Worker Thread (mesma processo, threads JS separadas), Cluster (múltiplos processos compartilhando porta), child_process (processo independente).
- **## Por que importa:** sem o conhecimento, o dev tenta resolver CPU-bound com `async/await` (não funciona — galho 1 nota 09 mostra), ou aumenta réplicas no orquestrador sem entender por que (caro). Saber as ferramentas + decision tree separa um sênior em decision-making.
- **## Como funciona:** revisão CPU-bound vs I/O-bound:
  - I/O-bound (DB, HTTP, file): event loop + `async/await` resolvem; paralelismo aqui geralmente não ajuda e pode piorar (mais context switches).
  - CPU-bound (hash, image processing, compress, ML inference): single-thread bloqueia. Aqui paralelismo é a única solução estrutural.
  - Code sample minimal: handler com `bcrypt.hashSync` que trava o servidor sob load. Antes de Worker Thread, tentar: rodar bcrypt async (callback API usa thread pool), aumentar `UV_THREADPOOL_SIZE` (galho 1 nota 07). Se ainda saturar, Worker Thread.
- **## Na prática:** padrão de raciocínio:
  1. Medir primeiro (galho 1 nota 11): event loop lag, percentis de latência, CPU usage. "Tá lento" sem medição é hipótese.
  2. Tentar **antes** de paralelizar: streaming (galho 3) para dados grandes; paginação para listas; refator do algoritmo; mover pra background queue (BullMQ, etc.); usar API async em vez de sync.
  3. Se paralelismo for inevitável, escolher a ferramenta certa (decision tree em nota 11).
- **## Armadilhas (3+):**
  1. Pular pra Worker Thread sem medir — adiciona complexidade sem ganho mensurável
  2. Confundir CPU-bound com I/O-bound — paralelizar I/O via Worker Threads é tipicamente pior que `async/await`
  3. Achar que "subir UV_THREADPOOL_SIZE" resolve qualquer CPU-bound — funciona apenas para APIs que usam o pool (bcrypt async, crypto.pbkdf2). Trabalho síncrono próprio precisa de Worker Thread.
- **## Em entrevista:**
  - Frase pronta: "Node is single-threaded by design, and that's the right choice for most I/O-bound workloads. But when you have genuine CPU-bound work — image processing, hashing, ML inference, compression — single-thread becomes the bottleneck. The signal is event loop lag that persists across optimization attempts. The structural fix is parallelism, but Node has three different parallelism tools — Worker Threads for shared-memory threads, Cluster for sharing an HTTP port across processes, and `child_process` for spawning external commands or isolated Node processes. Choosing the right one matters more than knowing they exist."
  - Vocabulário (5+): paralelismo (parallelism), concorrência (concurrency), trabalho de CPU (CPU-bound work), atraso do event loop (event loop lag), pool de threads (thread pool), processo (process), thread (thread).
- **## Veja também:**
  - `[[02 - As 3 ferramentas - Worker Threads, Cluster, child_process]]`
  - `[[03 - Worker Threads - fundamentos]]`
  - `[[11 - Decision tree - qual ferramenta para qual problema]]`
  - `[[Runtime e Event Loop]]` (galho 1)
  - `[[09 - async-await - o que é, o que não é]]` (galho 1 — mito da performance)
  - `[[10 - Bloqueio do event loop - sintomas e causas]]` (galho 1 — sintomas)
  - `[[Node.js]]` (tronco)

- [ ] **Step 4: Verificar rubrica**

```
[ ] TL;DR no callout [!abstract]
[ ] 6+ wikilinks (5+ da trilha + tronco + galho 1)
[ ] 1+ code sample (handler bcrypt bloqueante)
[ ] Em entrevista: 1 frase em inglês + 5+ termos
[ ] Armadilhas: 3 itens
[ ] Frontmatter completo
[ ] PT-BR natural; termos técnicos em inglês
[ ] Sem fabricação
[ ] Tamanho 250-400 linhas
```

- [ ] **Step 5: Commit**

```bash
git add "03-Dominios/Node/Paralelismo/01 - Por que paralelismo em Node.md"
git commit -m "feat(node-paralelismo): add note 01 — Por que paralelismo em Node"
```

---

## Task 3: Nota 02 — As 3 ferramentas (visão geral)

**Files:**
- Create: `03-Dominios/Node/Paralelismo/02 - As 3 ferramentas - Worker Threads, Cluster, child_process.md`

**Conteúdo-chave do spec:**

> Tabela rica: ferramenta · modelo · isolamento · custo de criação · IPC · uso típico. Worker Threads = shared-memory model. Cluster = shared-port model. child_process = separate-process model. Apontador pras notas detalhadas (3-9). Decisão preliminar; decisão completa em nota 11.

- [ ] **Step 1: Pesquisa-âncora**

WebFetch panorâmico (overviews, não deep dive — esses ficam pras notas dedicadas):

```
https://nodejs.org/api/worker_threads.html
https://nodejs.org/api/cluster.html
https://nodejs.org/api/child_process.html
```

Capturar: descrição em uma frase de cada API + diferenças de modelo de paralelismo.

- [ ] **Step 2: Frontmatter**

```yaml
---
title: "As 3 ferramentas: Worker Threads, Cluster, child_process"
created: 2026-05-07
updated: 2026-05-07
type: concept
status: seedling
publish: true
tags:
  - node
  - paralelismo
  - mental-model
  - worker-threads
  - cluster
  - child-process
aliases:
  - 3 modelos de paralelismo
  - Visão geral paralelismo Node
---
```

- [ ] **Step 3: Escrever a nota (300-450 linhas)**

- **TL;DR:** Node tem 3 ferramentas para paralelizar: Worker Threads (threads JS no mesmo processo, mensagens ou memória compartilhada), Cluster (múltiplos processos compartilhando porta HTTP), child_process (processo externo independente, IPC opcional via fork). Cada uma resolve um problema diferente — escolher a errada é fonte clássica de complexidade desnecessária.
- **## O que é:** os 3 **modelos** de paralelismo:
  1. **Shared-memory model** (Worker Threads): múltiplas threads JS no mesmo processo, podem trocar mensagens (clone) ou compartilhar memória (`SharedArrayBuffer`)
  2. **Shared-port model** (Cluster): primary fork() processos workers; todos compartilham mesma porta HTTP via round-robin do kernel
  3. **Separate-process model** (`child_process`): spawn de processo externo (qualquer comando) ou Node child com IPC. Sem compartilhamento de estado.
- **## Por que importa:** confundir os modelos leva a soluções erradas. "Tenho CPU-bound, vou usar Cluster" → cada worker faz a mesma CPU-bound, não paraleliza dentro de uma request. "Quero spawn um Python script, vou usar Worker Thread" → Worker só roda JS.
- **## Como funciona:** **tabela canônica** (esta é a estrela da nota):

  | Ferramenta | Modelo | Isolamento | Custo criação | IPC | Uso típico |
  |---|---|---|---|---|---|
  | Worker Thread | shared-memory | thread (mesma heap em SAB) | ~ms | postMessage / SAB | CPU-bound em handler |
  | Cluster | shared-port | processo | ~100ms | IPC built-in | Escalar HTTP por CPU |
  | child_process spawn | separate-process | processo | ~100ms | stdio | Rodar comando externo |
  | child_process fork | separate-process | processo | ~100ms | IPC built-in | Node child isolado |

  - Code sample minimal de cada um (10 linhas cada): Worker Thread via `new Worker`, Cluster via `cluster.fork()`, spawn via `spawn('ls')`, fork via `fork('./worker.js')`.
- **## Na prática:** a regra mental:
  - "Eu tenho CPU-bound e quero paralelizar dentro do mesmo processo" → Worker Thread
  - "Eu quero rodar 4 cópias do meu HTTP server em uma máquina" → Cluster (ou orquestrador)
  - "Eu quero rodar `ffmpeg` ou outro comando" → spawn
  - "Eu quero spawn um processo Node isolado" → fork
- **## Armadilhas (3+):**
  1. Usar Cluster pra CPU-bound em handler — não ajuda; cada worker tem o mesmo problema
  2. Tentar usar Worker Thread pra rodar comando externo — Worker só executa JS
  3. Achar que `fork` do `child_process` e `cluster.fork` são a mesma coisa — `cluster.fork` é especialização que compartilha porta
  4. Tomar decisão sem entender o problema (CPU-bound vs HTTP-scaling vs OS-integration)
- **## Em entrevista:**
  - Frase pronta: "Node has three parallelism tools, each solving a different problem. Worker Threads give you multiple JS threads in the same process — shared-memory model with message passing or `SharedArrayBuffer`. Cluster forks multiple processes that share an HTTP port via kernel round-robin — useful for scaling a web server across CPUs on a single host. `child_process` spawns external processes — `spawn` and `exec` for arbitrary commands, `fork` for Node children with IPC. The decision rule: CPU-bound → Worker Thread; HTTP scaling → Cluster or orchestrator; external command → spawn; isolated Node child → fork."
  - Vocabulário (6+): thread (thread), processo (process), modelo de memória compartilhada (shared-memory model), porta compartilhada (shared port), processo separado (separate process), comunicação interprocess (inter-process communication / IPC), bifurcar (fork), spawnar (spawn).
- **## Veja também:**
  - `[[01 - Por que paralelismo em Node]]`
  - `[[03 - Worker Threads - fundamentos]]`
  - `[[07 - Cluster - escalando HTTP por CPU]]`
  - `[[08 - child_process com exec e spawn]]`
  - `[[09 - child_process com fork - Node child com IPC]]`
  - `[[11 - Decision tree - qual ferramenta para qual problema]]`
  - `[[Node.js]]` (tronco)

- [ ] **Step 4: Verificar rubrica** (standard)

- [ ] **Step 5: Commit**

```bash
git add "03-Dominios/Node/Paralelismo/02 - As 3 ferramentas - Worker Threads, Cluster, child_process.md"
git commit -m "feat(node-paralelismo): add note 02 — As 3 ferramentas"
```

---

## Task 4: Nota 03 — Worker Threads (fundamentos)

**Files:**
- Create: `03-Dominios/Node/Paralelismo/03 - Worker Threads - fundamentos.md`

**Conteúdo-chave do spec:**

> API básica: `new Worker(file, { workerData })`, `parentPort`, `worker.on('message'/'error'/'exit'/'online')`, `worker.terminate()`. Custo de criação (~ms vs novo processo ~100ms). `isMainThread` flag. Modos: arquivo separado vs inline. Quando o Worker termina por conta própria, quando precisa de `terminate` explícito.

- [ ] **Step 1: Pesquisa-âncora**

```
WebFetch: https://nodejs.org/api/worker_threads.html
```

Capturar: API completa, eventos, lifecycle, propriedades estáticas (`isMainThread`, `workerData`, `parentPort`, `threadId`).

- [ ] **Step 2: Frontmatter**

```yaml
---
title: "Worker Threads: fundamentos"
created: 2026-05-07
updated: 2026-05-07
type: concept
status: seedling
publish: true
tags:
  - node
  - paralelismo
  - worker-threads
aliases:
  - Worker
  - parentPort
  - workerData
---
```

- [ ] **Step 3: Escrever a nota (350-500 linhas)**

- **TL;DR:** Worker Thread é uma thread JS adicional no mesmo processo Node. Criada via `new Worker(file, { workerData })`, comunica com main via `parentPort`. Custo de criação ~ms (vs ~100ms de processo). Eventos: `online`, `message`, `error`, `exit`. Terminate explícito ou natural quando termina o trabalho.
- **## O que é:** uma thread JS isolada (heap separada) que compartilha o mesmo processo Node. Tem seu próprio event loop, seu próprio V8 isolate. Útil pra trabalho CPU-bound porque não bloqueia a thread main.
- **## Por que importa:** alternativa às soluções "à força bruta" (subir réplicas no orquestrador). Worker Threads dão paralelismo real dentro de um processo, mantendo o footprint pequeno.
- **## Como funciona:** code samples:
  1. **Modo arquivo separado** (`main.js` + `worker.js`):
     ```javascript
     // main.js
     import { Worker } from 'node:worker_threads';
     const w = new Worker('./worker.js', { workerData: { input: 42 } });
     w.on('message', (msg) => console.log('result:', msg));
     w.on('error', console.error);
     w.on('exit', (code) => console.log('worker exited', code));
     
     // worker.js
     import { parentPort, workerData } from 'node:worker_threads';
     const result = workerData.input * 2;
     parentPort.postMessage(result);
     ```
  2. **Modo inline** (mesmo arquivo via `isMainThread`):
     ```javascript
     import { Worker, isMainThread, parentPort, workerData } from 'node:worker_threads';
     if (isMainThread) {
       const w = new Worker(__filename, { workerData: { input: 42 } });
       w.on('message', console.log);
     } else {
       parentPort.postMessage(workerData.input * 2);
     }
     ```
  3. **Lifecycle completo** com todos os eventos:
     ```javascript
     w.on('online', () => console.log('worker started'));
     w.on('message', (m) => /* handle */);
     w.on('messageerror', (err) => /* clone failure */);
     w.on('error', (err) => /* uncaught in worker */);
     w.on('exit', (code) => /* 0 = clean, !0 = error */);
     ```
  4. **Terminate explícito**: `await w.terminate()` retorna exit code.
  5. **threadId**: `worker_threads.threadId` (0 no main, sequencial nos workers).
- **## Na prática:** padrão observado:
  - Modo arquivo separado é mais comum (separação clara, fácil testar)
  - Modo inline economiza arquivos mas dificulta tooling (linter, types)
  - `worker.terminate()` é forçado — usa SIGKILL semanticamente; preferir cooperação via mensagem `'shutdown'`
  - `unref()` permite o processo main sair sem esperar o worker (útil pra workers que fazem trabalho de fundo não-crítico)
- **## Armadilhas (3+):**
  1. Esquecer de tratar evento `'error'` — error handler default vai pra `unhandledException` (e fatal em Node 22+)
  2. `terminate()` pode deixar trabalho não-finalizado (escrita parcial em arquivo, mensagem perdida); preferir cooperative shutdown
  3. `workerData` passa por structured clone — funções, classes, refs DOM falham (preview da nota 04)
  4. Confundir Worker Thread com Web Worker do browser — APIs parecidas mas não idênticas (`importScripts` não existe, etc.)
- **## Em entrevista:**
  - Frase pronta: "A Worker Thread is an additional JS thread in the same Node process — separate V8 isolate, separate event loop, separate heap. You create one with `new Worker(filePath, { workerData })`. The worker communicates with the main thread via `parentPort.postMessage`, and the main thread listens with `worker.on('message')`. Lifecycle events are `online`, `message`, `error`, `exit`. Workers cost about a millisecond to create, versus around 100 milliseconds for a process — so they're cheap enough for per-request use, though pooling is the production pattern."
  - Vocabulário (5+): thread de trabalho (Worker Thread), thread principal (main thread), porta-pai (parentPort), dados do worker (workerData), terminar (terminate), isolado V8 (V8 isolate), thread leve (lightweight thread).
- **## Veja também:**
  - `[[01 - Por que paralelismo em Node]]`
  - `[[02 - As 3 ferramentas - Worker Threads, Cluster, child_process]]`
  - `[[04 - Comunicação entre workers - postMessage e MessageChannel]]`
  - `[[05 - Memória compartilhada - SharedArrayBuffer e Atomics]]`
  - `[[06 - Pool de workers - pattern de produção]]`
  - `[[Node.js]]` (tronco)

- [ ] **Step 4: Verificar rubrica** (standard, code samples mínimo 4 dado o tema operacional)

- [ ] **Step 5: Commit**

```bash
git add "03-Dominios/Node/Paralelismo/03 - Worker Threads - fundamentos.md"
git commit -m "feat(node-paralelismo): add note 03 — Worker Threads fundamentos"
```

---

## Task 5: Nota 04 — Comunicação entre workers

**Files:**
- Create: `03-Dominios/Node/Paralelismo/04 - Comunicação entre workers - postMessage e MessageChannel.md`

**Conteúdo-chave do spec:**

> Algoritmo de clone estruturado. `transferList` para passar `ArrayBuffer`/`MessagePort` sem cópia. `MessageChannel` para canais bidirecionais isolados do `parentPort`. Tipos do `worker_threads`.

- [ ] **Step 1: Pesquisa-âncora**

```
WebFetch: https://nodejs.org/api/worker_threads.html#workerpostmessagevalue-transferlist
WebFetch: https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API/Structured_clone_algorithm
```

- [ ] **Step 2: Frontmatter**

```yaml
---
title: "Comunicação entre workers: postMessage e MessageChannel"
created: 2026-05-07
updated: 2026-05-07
type: concept
status: seedling
publish: true
tags:
  - node
  - paralelismo
  - worker-threads
  - postmessage
  - messagechannel
aliases:
  - postMessage
  - transferList
  - MessageChannel
---
```

- [ ] **Step 3: Escrever a nota (350-500 linhas)**

- **TL;DR:** Workers comunicam via `postMessage`, que clona o payload (algoritmo de clone estruturado). Para evitar cópia de buffers grandes, use `transferList` — o `ArrayBuffer` é movido (referência transferida; original fica detached). `MessageChannel` cria canais bidirecionais separados do `parentPort`.
- **## O que é:** o protocolo de mensagens entre Worker e main, e entre Workers entre si.
- **## Por que importa:** copiar 100MB via clone estruturado a cada mensagem é caro. `transferList` é o mecanismo zero-copy. `MessageChannel` é como você arquiteta múltiplos workers se comunicando entre si.
- **## Como funciona:**
  1. **Algoritmo de clone estruturado** — tipos suportados:
     - Primitivos, `Date`, `RegExp`, `Map`, `Set`, `Array`, `Object`, `Buffer`, `ArrayBuffer`, `TypedArray`, `Error`
     - Não suportados: funções, símbolos (parcial), DOM nodes, classes (perdem prototype), getters/setters
  2. Code sample: o que é clonado, o que falha:
     ```javascript
     // OK
     w.postMessage({ name: 'Ada', born: new Date('1815'), tags: new Set(['math']) });
     
     // FALHA
     w.postMessage({ greet: () => 'hi' }); // Throws: function not cloneable
     class Foo {}
     w.postMessage(new Foo()); // Clona dados, mas perde prototype
     ```
  3. **`transferList` para zero-copy:**
     ```javascript
     const buf = new ArrayBuffer(100_000_000);
     w.postMessage(buf, [buf]);
     // buf no main agora está detached: buf.byteLength === 0
     ```
  4. **`MessageChannel` para canais bidirecionais:**
     ```javascript
     import { Worker, MessageChannel } from 'node:worker_threads';
     const { port1, port2 } = new MessageChannel();
     const w = new Worker('./worker.js');
     w.postMessage({ port: port2 }, [port2]);  // transfer port2 to worker
     port1.on('message', (m) => console.log('from worker:', m));
     port1.postMessage('hello worker via dedicated channel');
     ```
  5. Tabela: o que é clonado vs movido vs falha.
- **## Na prática:** padrões:
  - `transferList` essencial pra processamento de imagem, audio, ML inference (buffers grandes)
  - `MessageChannel` permite N workers comunicando entre si sem passar pelo main (broker pattern)
  - JSON.stringify + JSON.parse é frequentemente mais rápido que structured clone pra payloads pequenos com tipos simples (arrays de números, strings)
- **## Armadilhas (3+):**
  1. Esquecer `transferList` em buffers grandes — cópia de 100MB acontece silenciosamente
  2. Tentar enviar funções ou classes — clone falha em runtime, descobre só sob load
  3. Usar `MessageChannel` sem fechar `port` — vaza file descriptor; sempre `port.close()` no shutdown
  4. Achar que `MessagePort` é serializável em log/JSON — não é, é um handle de comunicação
- **## Em entrevista:**
  - Frase pronta: "Communication between Worker Threads goes through `postMessage`, which uses the structured clone algorithm to deep-copy the payload. That means most JS values work — primitives, plain objects, Maps, Sets, Buffers — but functions and class instances don't survive. For zero-copy of large buffers, the second argument is `transferList`: the `ArrayBuffer` is moved instead of copied, leaving the original detached on the sender side. For multi-worker architectures, `MessageChannel` creates a dedicated bidirectional channel that you can transfer to a worker, letting workers talk to each other without going through main."
  - Vocabulário (5+): clone estruturado (structured clone), zero-cópia (zero-copy), transferir referência (transfer ownership), buffer destacado (detached buffer), canal de mensagem (message channel), postar mensagem (post message).
- **## Veja também:**
  - `[[03 - Worker Threads - fundamentos]]`
  - `[[05 - Memória compartilhada - SharedArrayBuffer e Atomics]]`
  - `[[06 - Pool de workers - pattern de produção]]`
  - `[[Node.js]]` (tronco)

- [ ] **Step 4: Verificar rubrica** (standard)

- [ ] **Step 5: Commit**

```bash
git add "03-Dominios/Node/Paralelismo/04 - Comunicação entre workers - postMessage e MessageChannel.md"
git commit -m "feat(node-paralelismo): add note 04 — Comunicação entre workers"
```

---

## Task 6: Nota 05 — SharedArrayBuffer e Atomics

**Files:**
- Create: `03-Dominios/Node/Paralelismo/05 - Memória compartilhada - SharedArrayBuffer e Atomics.md`

**Conteúdo-chave do spec:** Concorrência real em JS. `SharedArrayBuffer` (visível em múltiplos workers, sem clone). `Atomics` para operações atômicas: `Atomics.load/store/add/sub/compareExchange`. `Atomics.wait` / `Atomics.notify` para sincronização. Race conditions canônicas. Casos legítimos. Restrições de segurança.

> **Nota especial:** o spec do galho diz que essa nota não tem limite artificial de tamanho. Concorrência com memória compartilhada é tema profundo e merece a profundidade que pedir. O alvo é cobrir o panorama completo (estados, todas as ops do `Atomics`, wait/notify, race conditions canônicas, quando preferir mensagens) — não comprimir.

- [ ] **Step 1: Pesquisa-âncora**

```
WebFetch: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/SharedArrayBuffer
WebFetch: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Atomics
WebFetch: https://nodejs.org/api/worker_threads.html
```

- [ ] **Step 2: Frontmatter**

```yaml
---
title: "Memória compartilhada: SharedArrayBuffer e Atomics"
created: 2026-05-07
updated: 2026-05-07
type: concept
status: seedling
publish: true
tags:
  - node
  - paralelismo
  - worker-threads
  - sharedarraybuffer
  - atomics
  - concurrency
aliases:
  - SharedArrayBuffer
  - SAB
  - Atomics
  - Race conditions em JS
---
```

- [ ] **Step 3: Escrever a nota completa (sem limite — alvo 500-700 linhas se o tema pedir)**

Cobrir, em PT-BR:

- **TL;DR:** `SharedArrayBuffer` (SAB) é um buffer visível simultaneamente em múltiplos Workers — diferente de `ArrayBuffer` (clonado ou transferido). Acesso direto cria race conditions; use `Atomics` para operações atômicas e `Atomics.wait`/`notify` para sincronização. Casos legítimos: matrizes grandes em ML/imagens, contadores compartilhados, semáforos. Quando possível, preferir mensagens.
- **## O que é:** SAB e Atomics. SAB = `ArrayBuffer` que vive em memória compartilhada entre workers. `Atomics` = objeto global com operações atômicas sobre `TypedArray` que apontam pra SAB.
- **## Por que importa:** alternativa zero-copy + multi-worker pra trabalho pesado em buffers (matrizes, áudio, video frames). Bem usado, é a solução mais eficiente; mal usado, produz race conditions difíceis de reproduzir.
- **## Como funciona:**
  1. **Criando e compartilhando SAB:**
     ```javascript
     // main
     const sab = new SharedArrayBuffer(1024);  // 1KB compartilhado
     const view = new Int32Array(sab);
     w.postMessage({ sab });  // SAB não precisa estar no transferList — não é movido
     ```
  2. **Race condition canônica** (incremento não-atômico):
     ```javascript
     // worker
     view[0]++;  // RUIM — read + increment + write não atômicos
     // 2 workers fazendo isso → resultado incorreto
     ```
  3. **`Atomics` para operações atômicas:**
     - `Atomics.load(view, idx)` — leitura atômica
     - `Atomics.store(view, idx, val)` — escrita atômica
     - `Atomics.add(view, idx, val)` — incremento atômico, retorna valor antigo
     - `Atomics.sub`, `Atomics.and`, `Atomics.or`, `Atomics.xor` — análogos
     - `Atomics.exchange(view, idx, val)` — swap atômico
     - `Atomics.compareExchange(view, idx, expected, newVal)` — CAS clássico
  4. **Sincronização com `wait`/`notify`:**
     - `Atomics.wait(view, idx, expectedVal, timeout?)` — bloqueia worker até `view[idx]` mudar (ou timeout); retorna `'ok'`/`'not-equal'`/`'timed-out'`
     - `Atomics.notify(view, idx, count)` — acorda até `count` workers em `wait` naquele índice
     - Atenção: `Atomics.wait` SÓ funciona em workers, NÃO no main thread (lança em main thread)
  5. **Padrões canônicos:**
     - Contador atômico (counter compartilhado)
     - Spinlock primitivo (não recomendado em prod — preferir mensagens)
     - Producer-consumer com SAB + `wait`/`notify`
- **## Na prática:** quando SAB+Atomics é justificado:
  - Matrizes grandes em ML inference paralelizada (imagem dividida em tiles)
  - Streams de áudio/vídeo onde frames são compartilhados entre threads de processamento
  - Contadores de progresso visíveis em tempo real do main
  - Quando preferir mensagens: na maioria dos casos. SAB+Atomics é "concorrência baixo nível em JS" — fácil errar.
- **## Armadilhas:** (4+ armadilhas concretas):
  1. Acessar SAB sem `Atomics` — race conditions silenciosas
  2. `Atomics.wait` no main thread → throws (só funciona em workers)
  3. Esquecer que `Int32Array` index é em índices, não bytes (`view[1]` é byte 4-7)
  4. SAB cresce até `byteLength` fixo — não dá pra resize. Provisionar com folga
  5. Confundir `Atomics.add` (retorna ANTIGO) com convenção pré/pós-incremento
  6. Race condition em sequência de duas operações atômicas — atomicidade individual não compõe
- **## Em entrevista:**
  - Frase pronta: "`SharedArrayBuffer` is a buffer that's visible simultaneously across multiple Worker Threads — unlike a regular `ArrayBuffer`, which is cloned or transferred. Once you have shared memory, you have race conditions, so reads and writes need `Atomics` — `Atomics.load`, `store`, `add`, `compareExchange`, and so on. For coordination, `Atomics.wait` and `Atomics.notify` give you a primitive condition variable, but `wait` only works inside Workers, not the main thread. The legitimate use cases are tight: large matrices in ML or image processing, shared counters, semaphores. For most application code, message passing is simpler and the right default."
  - Vocabulário (6+): memória compartilhada (shared memory), operação atômica (atomic operation), condição de corrida (race condition), comparar-e-trocar (compare-and-swap), aguardar e notificar (wait and notify), variável de condição (condition variable), spinlock.
- **## Veja também:**
  - `[[03 - Worker Threads - fundamentos]]`
  - `[[04 - Comunicação entre workers - postMessage e MessageChannel]]`
  - `[[06 - Pool de workers - pattern de produção]]`
  - `[[Node.js]]` (tronco)

- [ ] **Step 4: Verificar rubrica** (standard, code samples mínimo 5 — tema é operacional e race conditions só ficam claras com código)

- [ ] **Step 5: Commit**

```bash
git add "03-Dominios/Node/Paralelismo/05 - Memória compartilhada - SharedArrayBuffer e Atomics.md"
git commit -m "feat(node-paralelismo): add note 05 — SharedArrayBuffer e Atomics"
```

---

## Task 7: Nota 06 — Pool de workers

**Files:**
- Create: `03-Dominios/Node/Paralelismo/06 - Pool de workers - pattern de produção.md`

**Conteúdo-chave do spec:** Reusar workers, queue, bounded concurrency, `piscina` como referência, lifecycle, graceful shutdown.

- [ ] **Step 1: Pesquisa-âncora**

```
WebFetch: https://github.com/piscinajs/piscina
WebFetch: https://nodejs.org/api/worker_threads.html
```

- [ ] **Step 2: Frontmatter**

```yaml
---
title: "Pool de workers: pattern de produção"
created: 2026-05-07
updated: 2026-05-07
type: concept
status: seedling
publish: true
tags:
  - node
  - paralelismo
  - worker-threads
  - pool
  - piscina
aliases:
  - Worker pool
  - piscina
  - bounded concurrency
---
```

- [ ] **Step 3: Escrever a nota (350-500 linhas)**

- **TL;DR:** Em produção, criar um Worker por task é caro (custo de criação amortizado, GC pressure). O pattern canônico é **pool**: N workers reutilizáveis + queue de tasks pendentes. `piscina` é a lib de referência. Implementação manual: queue + worker pool + handoff via `MessagePort`. Sempre incluir graceful shutdown.
- **## O que é:** worker pool = abstração que mantém N workers vivos e despacha tasks pra eles via queue. Evita custo de spawn por task.
- **## Por que importa:** sem pool, app sob carga cria/destroi workers num loop hot — o custo de ~ms por criação vira gargalo, e o GC tem que limpar workers terminados constantemente.
- **## Como funciona:**
  1. **Implementação manual mínima** (~30 linhas) — pool de 4 workers + queue:
     ```javascript
     class WorkerPool {
       constructor(file, size) {
         this.workers = Array.from({ length: size }, () => new Worker(file));
         this.idle = [...this.workers];
         this.queue = [];
       }
       run(data) {
         return new Promise((resolve, reject) => {
           const task = { data, resolve, reject };
           if (this.idle.length) this.dispatch(task);
           else this.queue.push(task);
         });
       }
       dispatch(task) {
         const w = this.idle.pop();
         w.once('message', (result) => {
           task.resolve(result);
           if (this.queue.length) this.dispatch(this.queue.shift());
           else this.idle.push(w);
         });
         w.postMessage(task.data);
       }
       async shutdown() {
         await Promise.all(this.workers.map(w => w.terminate()));
       }
     }
     ```
     (Versão didática; tem bugs de error handling — `piscina` resolve.)
  2. **Usando `piscina`:**
     ```javascript
     import Piscina from 'piscina';
     const pool = new Piscina({
       filename: new URL('./worker.js', import.meta.url).href,
       maxThreads: 8,
       minThreads: 2,
     });
     const result = await pool.run({ input: 42 });
     // ou: pool.run({ input: 42 }, { name: 'specificFn' })
     ```
  3. **Graceful shutdown:**
     ```javascript
     process.on('SIGTERM', async () => {
       await pool.destroy();  // espera tasks em andamento
       process.exit(0);
     });
     ```
  4. **Concurrency tuning:** `maxThreads = numberOfCpus()` é default sensato. `idleTimeout` mata workers parados pra economizar memória.
- **## Na prática:** padrão observado:
  - `piscina` é o default em produção; implementação manual só pra entender o pattern
  - `maxQueue` (limite de fila) evita memory blow-up sob load extremo
  - Tasks devem ser idempotentes — se um worker crashar mid-task, o pool re-spawn mas a task pode ter side effects
  - Métricas relevantes: `pool.queueSize`, `pool.threads.length`, `pool.completed`
- **## Armadilhas (3+):**
  1. Pool sem `maxQueue` — backpressure se acumula até OOM
  2. Esquecer `pool.destroy()` em SIGTERM — graceful shutdown não acontece, tasks em andamento perdidas
  3. Tasks com side effects (escrita em DB) sem idempotência — crash + retry corrompem
  4. `maxThreads` muito alto em apps com pouca CPU dedicada — context switching mata throughput
- **## Em entrevista:**
  - Frase pronta: "In production, you don't create a Worker per task — the spawn cost adds up and the garbage collector has to clean up dead workers constantly. The canonical pattern is a worker pool: a fixed number of workers kept alive, with a queue of pending tasks. The reference implementation is `piscina`, by Matteo Collina — it handles thread management, queueing, idle timeout, and graceful shutdown. The interesting tuning knob is `maxThreads`, typically set to the number of CPU cores. Always wire `pool.destroy()` to your SIGTERM handler so in-flight tasks complete before shutdown."
  - Vocabulário (5+): pool de workers (worker pool), fila de tarefas (task queue), concorrência limitada (bounded concurrency), encerramento gracioso (graceful shutdown), tempo limite de inatividade (idle timeout).
- **## Veja também:**
  - `[[03 - Worker Threads - fundamentos]]`
  - `[[04 - Comunicação entre workers - postMessage e MessageChannel]]`
  - `[[10 - Cluster vs PM2 vs Kubernetes - quem orquestra]]`
  - `[[12 - Armadilhas, regras práticas, cheatsheet]]`
  - `[[Node.js]]` (tronco)

- [ ] **Step 4: Verificar rubrica** (standard)

- [ ] **Step 5: Commit**

```bash
git add "03-Dominios/Node/Paralelismo/06 - Pool de workers - pattern de produção.md"
git commit -m "feat(node-paralelismo): add note 06 — Pool de workers"
```

---

## Task 8: Nota 07 — Cluster

**Files:**
- Create: `03-Dominios/Node/Paralelismo/07 - Cluster - escalando HTTP por CPU.md`

**Conteúdo-chave do spec:** API: `cluster.isPrimary`, `cluster.fork()`, eventos. Restart automático. Port sharing. Sticky sessions. Graceful shutdown.

- [ ] **Step 1: Pesquisa-âncora**

```
WebFetch: https://nodejs.org/api/cluster.html
```

- [ ] **Step 2: Frontmatter**

```yaml
---
title: "Cluster: escalando HTTP por CPU"
created: 2026-05-07
updated: 2026-05-07
type: concept
status: seedling
publish: true
tags:
  - node
  - paralelismo
  - cluster
  - http
  - scaling
aliases:
  - cluster
  - cluster.fork
  - port sharing
---
```

- [ ] **Step 3: Escrever a nota (350-500 linhas)**

Estrutura padrão. Cobrir:

- **TL;DR:** Cluster é o módulo nativo que fork-a múltiplos processos Node compartilhando a mesma porta HTTP. Primary controla; workers atendem requests. Round-robin no Linux. Útil em deploys single-VM; em prod com orquestrador (K8s, ECS), o orquestrador já faz isso.
- **## O que é**, **## Por que importa**, **## Como funciona** com:
  1. Code sample minimal: primary forks N workers, cada worker ouve port 3000:
     ```javascript
     import cluster from 'node:cluster';
     import { availableParallelism } from 'node:os';
     import http from 'node:http';
     
     if (cluster.isPrimary) {
       const numCPUs = availableParallelism();
       for (let i = 0; i < numCPUs; i++) cluster.fork();
       cluster.on('exit', (worker) => {
         console.log(`worker ${worker.process.pid} died, restarting`);
         cluster.fork();
       });
     } else {
       http.createServer((req, res) => res.end(`pid ${process.pid}`)).listen(3000);
     }
     ```
  2. **Port sharing**: como funciona (kernel SO_REUSEPORT no Linux + round-robin do Node)
  3. **Sticky sessions**: por que precisa (WebSocket); como implementar com `@socket.io/sticky` ou nginx upstream `ip_hash`
  4. **Graceful shutdown**: SIGTERM no primary → primary manda `disconnect` nos workers → workers param de aceitar novas conexões → drain → exit
- **## Na prática**: cluster sozinho é raramente usado em prod nova; quando ainda usado é em VMs single-host (small SaaS, internal tooling, scripts/CLIs que precisam paralelizar HTTP)
- **## Armadilhas (3+):**
  1. State em memória local de worker (cache, sessões) — comportamento inconsistente entre workers
  2. Esquecer `cluster.on('exit', ...)` — worker morre e ninguém substitui
  3. Sticky sessions sem reverse proxy ciente — round-robin do kernel mata WebSocket
  4. Usar cluster + orquestrador (1 pod com cluster de 4 + 4 réplicas K8s) = 16 processos sem necessidade
- **## Em entrevista**: frase pronta + vocabulário (cluster, primary/worker, port sharing, sticky session, graceful shutdown)
- **## Veja também**: 02, 06, 09, 10, 11, Node.js (tronco)

- [ ] **Step 4: Verificar rubrica** (standard)

- [ ] **Step 5: Commit**

```bash
git add "03-Dominios/Node/Paralelismo/07 - Cluster - escalando HTTP por CPU.md"
git commit -m "feat(node-paralelismo): add note 07 — Cluster"
```

---

## Task 9: Nota 08 — child_process com exec e spawn

**Files:**
- Create: `03-Dominios/Node/Paralelismo/08 - child_process com exec e spawn.md`

- [ ] **Step 1: Pesquisa-âncora**

```
WebFetch: https://nodejs.org/api/child_process.html
WebFetch: https://nodejs.org/api/child_process.html#child_processexeccommand-options-callback
WebFetch: https://nodejs.org/api/child_process.html#child_processexecfilefile-args-options-callback
WebFetch: https://nodejs.org/api/child_process.html#child_processspawncommand-args-options
```

- [ ] **Step 2: Frontmatter**

```yaml
---
title: "child_process com exec e spawn"
created: 2026-05-07
updated: 2026-05-07
type: concept
status: seedling
publish: true
tags:
  - node
  - paralelismo
  - child-process
  - exec
  - spawn
  - security
aliases:
  - exec
  - spawn
  - execFile
  - shell injection
---
```

- [ ] **Step 3: Escrever a nota (350-500 linhas)**

Estrutura padrão. Cobrir:

- **TL;DR:** `exec` (bufferizado, conveniente, **vulnerável a shell injection**), `execFile` (sem shell, mais seguro), `spawn` (streaming, sem buffer limit, ideal pra output longo). Regra: nunca passar input do usuário pro shell; preferir `execFile`/`spawn` com array de args.
- **## O que é**, **## Por que importa**, **## Como funciona** com code samples:
  1. `exec` (com promisify):
     ```javascript
     import { promisify } from 'node:util';
     import { exec } from 'node:child_process';
     const execP = promisify(exec);
     const { stdout } = await execP('git log --oneline -5');
     ```
  2. `execFile` (sem shell):
     ```javascript
     import { execFile } from 'node:child_process';
     execFile('git', ['log', '--oneline', '-5'], (err, stdout) => { /* ... */ });
     ```
  3. `spawn` (streaming):
     ```javascript
     import { spawn } from 'node:child_process';
     const proc = spawn('ffmpeg', ['-i', 'input.mp4', 'output.webm']);
     proc.stdout.on('data', (chunk) => process.stdout.write(chunk));
     proc.on('close', (code) => console.log(`exited ${code}`));
     ```
  4. **Shell injection — o exemplo definitivo:**
     ```javascript
     // VULNERÁVEL
     exec(`grep ${userInput} file.txt`);  // userInput = "; rm -rf /" detona
     // SEGURO
     execFile('grep', [userInput, 'file.txt']);
     ```
  5. `stdio` config (`'inherit'` vs `'pipe'`), encoding, signal handling
- **## Na prática**: regra de ouro — sempre `execFile`/`spawn` com array de args. `exec` só pra comandos hardcoded sem input externo
- **## Armadilhas (3+):**
  1. Shell injection via `exec` — vulnerabilidade clássica
  2. `exec` com output longo (>~1MB) — `maxBuffer` exceded, processo morre
  3. Esquecer signal handling — child fica zumbi se parent crashar
  4. `spawn` sem ler stdout/stderr — buffer cheio bloqueia child
- **## Em entrevista**: frase pronta + vocabulário (executar comando, injeção de shell, shell injection, fluxo de dados, streaming)
- **## Veja também**: 02, 09, 12, Node.js (tronco)

- [ ] **Step 4: Verificar rubrica** (standard)

- [ ] **Step 5: Commit**

```bash
git add "03-Dominios/Node/Paralelismo/08 - child_process com exec e spawn.md"
git commit -m "feat(node-paralelismo): add note 08 — child_process exec e spawn"
```

---

## Task 10: Nota 09 — child_process com fork

**Files:**
- Create: `03-Dominios/Node/Paralelismo/09 - child_process com fork - Node child com IPC.md`

- [ ] **Step 1: Pesquisa-âncora**

```
WebFetch: https://nodejs.org/api/child_process.html#child_processforkmodulepath-args-options
```

- [ ] **Step 2: Frontmatter**

```yaml
---
title: "child_process com fork: Node child com IPC"
created: 2026-05-07
updated: 2026-05-07
type: concept
status: seedling
publish: true
tags:
  - node
  - paralelismo
  - child-process
  - fork
  - ipc
aliases:
  - fork
  - Node child
  - process IPC
---
```

- [ ] **Step 3: Escrever a nota (300-450 linhas)**

Estrutura padrão. Cobrir:

- **TL;DR:** `fork('./worker.js')` cria child Node com canal IPC built-in (`child.send()` / `process.on('message')`). Diferente de Worker Thread: isolamento total de memória, separate event loop, separate V8 isolate, custo de criação maior (~100ms). Quando preferir fork sobre Worker: isolamento total, native modules incompatíveis com Worker, supervisor tree, processo descartável.
- **## O que é**, **## Por que importa**, **## Como funciona**:
  1. Code sample: parent fork-a child, troca mensagens
     ```javascript
     // parent.js
     import { fork } from 'node:child_process';
     const child = fork('./worker.js');
     child.send({ type: 'work', payload: 42 });
     child.on('message', (msg) => console.log('from child:', msg));
     child.on('exit', (code) => console.log('child exited', code));
     
     // worker.js
     process.on('message', (msg) => {
       const result = msg.payload * 2;
       process.send({ type: 'result', result });
     });
     ```
  2. Tabela comparativa **fork vs Worker Thread**: isolamento, custo, APIs disponíveis (Worker tem postMessage; fork tem child.send), uso típico
- **## Na prática**: 4 casos onde fork ainda ganha:
  1. Isolamento total de memória (security boundary, multi-tenancy)
  2. Native modules incompatíveis com Worker Threads (alguns N-API addons antigos)
  3. Supervisor tree (Erlang-style) — child morre + parent respawn é design intencional
  4. Processo descartável que pode crashar sem afetar parent (sandboxed code execution)
- **## Armadilhas (3+):**
  1. Esquecer cleanup de child em parent crash — zombies
  2. `child.send` com objeto não-serializable — silent fail
  3. Confundir `fork` do `child_process` com `cluster.fork` — overlapping nomes, semântica diferente
  4. Custo de criação alto sem reuso — usar pool ou spawn-on-demand explicitamente
- **## Em entrevista**: frase pronta + vocabulário (bifurcar processo, fork, IPC, comunicação inter-processo, isolamento de memória)
- **## Veja também**: 03, 07, 08, 11, Node.js (tronco)

- [ ] **Step 4: Verificar rubrica** (standard)

- [ ] **Step 5: Commit**

```bash
git add "03-Dominios/Node/Paralelismo/09 - child_process com fork - Node child com IPC.md"
git commit -m "feat(node-paralelismo): add note 09 — child_process fork"
```

---

## Task 11: Nota 10 — Cluster vs PM2 vs Kubernetes

**Files:**
- Create: `03-Dominios/Node/Paralelismo/10 - Cluster vs PM2 vs Kubernetes - quem orquestra.md`

**Conteúdo-chave do spec:** Histórico (cluster brilhou ~2014-2018, PM2 fez cluster + watchdog ~2018-2020, hoje K8s/ECS são default). Quando cluster ainda faz sentido em 2026.

- [ ] **Step 1: Pesquisa-âncora**

```
WebFetch: https://pm2.keymetrics.io/
WebFetch: https://nodejs.org/api/cluster.html
```

Buscar também: discussões recentes sobre cluster nativo em 2026 (pode ser via `WebSearch` se WebFetch não bastar).

- [ ] **Step 2: Frontmatter**

```yaml
---
title: "Cluster vs PM2 vs Kubernetes: quem orquestra"
created: 2026-05-07
updated: 2026-05-07
type: concept
status: seedling
publish: true
tags:
  - node
  - paralelismo
  - cluster
  - pm2
  - kubernetes
  - production
aliases:
  - PM2
  - K8s Node
  - Cluster vs orquestrador
---
```

- [ ] **Step 3: Escrever a nota (350-500 linhas)**

- **TL;DR:** Cluster nativo brilhou em ~2014-2018 quando deploys eram em VMs single-host. PM2 ofereceu cluster + watchdog + logs (default ~2018-2020). Hoje (2026), Kubernetes/ECS/Nomad fazem fork em escala diferente: 1 pod por core, autoscaling horizontal, rolling updates declarativos. Cluster nativo virou raro em prod nova — use orquestrador. Cluster nativo só faz sentido em single-VM deploys ou em scripts/CLIs.
- **## O que é**: contraste histórico das 3 abordagens.
- **## Por que importa**: muitas equipes ainda usam cluster + K8s sem perceber a redundância (1 pod com cluster de 4 + 4 réplicas K8s = 16 processos). Saber o histórico ajuda a fazer escolhas que envelhecem bem.
- **## Como funciona**:
  - **Cluster nativo**: API stdlib, primary/worker, port sharing kernel
  - **PM2**: wrapper sobre cluster + features (watchdog, logs, zero-downtime reload, monitoring dashboard)
  - **Kubernetes**: pod = 1 processo (geralmente Node sem cluster), N pods replica horizontal, kube-proxy/ingress balanceia
- **## Na prática**:
  - **Em 2026**: K8s/ECS/Nomad é o default em qualquer empresa de médio porte
  - PM2 ainda usado em VPS pequenos / single-VM (Hetzner, Linode, Digital Ocean droplets)
  - Cluster nativo: dev local (testar comportamento multi-worker), single-VM deploys de SaaS pequeno, scripts CLI que precisam paralelizar HTTP, ou em pods K8s de tamanho grande quando faz sentido aproveitar a CPU disponível por pod
- **## Armadilhas (3+):**
  1. Cluster + K8s sem pensar — overhead inútil
  2. State em worker (sessões, cache local) — funciona em dev, quebra em prod
  3. Confiar em PM2 graceful reload sem testar — alguns apps quebram em SIGUSR2
  4. Migrar pra K8s sem reescrever stateful logic — sessões em memória local viram bug em escala
- **## Em entrevista**: frase pronta + vocabulário (orquestrador, autoscaling, rolling update, réplica, balanceamento de carga, processo stateless)
- **## Veja também**: 07, 11, 12, Node.js (tronco)

- [ ] **Step 4: Verificar rubrica** (standard)

- [ ] **Step 5: Commit**

```bash
git add "03-Dominios/Node/Paralelismo/10 - Cluster vs PM2 vs Kubernetes - quem orquestra.md"
git commit -m "feat(node-paralelismo): add note 10 — Cluster vs PM2 vs K8s"
```

---

## Task 12: Nota 11 — Decision tree

**Files:**
- Create: `03-Dominios/Node/Paralelismo/11 - Decision tree - qual ferramenta para qual problema.md`

**Conteúdo-chave do spec:** Síntese com fluxograma. Decision tree em ASCII. Tabela problema → ferramenta → razão.

- [ ] **Step 1: Síntese (sem WebFetch)**

Reler todas as 10 notas anteriores e o spec do galho. Esta nota é puramente síntese.

- [ ] **Step 2: Frontmatter**

```yaml
---
title: "Decision tree: qual ferramenta para qual problema"
created: 2026-05-07
updated: 2026-05-07
type: concept
status: seedling
publish: true
tags:
  - node
  - paralelismo
  - decision-tree
  - referencia
aliases:
  - Decision tree paralelismo
  - Qual ferramenta usar
---
```

- [ ] **Step 3: Escrever a nota (300-450 linhas)**

Estrutura tópica (não narrativa pura — combina prosa com fluxograma e tabela):

- **TL;DR:** Pergunta-chave: qual o problema? CPU-bound em handler → Worker Thread (com pool em prod). Escalar HTTP além de single-thread → orquestrador (K8s); Cluster apenas se single-VM. Rodar comando externo → spawn / execFile (nunca exec com input do user). Spawn de Node isolado → fork.
- **## O que é**: decision tree como artefato — separa problema (CPU? HTTP? OS?) da ferramenta (Worker / Cluster / spawn / fork).
- **## Por que importa**: a maioria dos erros não é técnico — é escolher a ferramenta errada pro problema.
- **## Como funciona — fluxograma ASCII completo:**

  ```
  Qual o problema?
  
  ├─ CPU-bound em handler/job?
  │   └─ → Worker Thread
  │       ├─ Tarefa frequente? → pool (piscina)
  │       └─ Tarefa rara? → Worker per task OK
  │
  ├─ Preciso escalar HTTP além de 1 thread?
  │   ├─ Tem orquestrador (K8s/ECS)? → deixa o orquestrador (1 pod por core)
  │   ├─ Single-VM deploy / VPS? → Cluster (ou PM2)
  │   └─ Dev local pra testar comportamento multi-worker? → Cluster
  │
  ├─ Preciso rodar comando externo (ffmpeg, git, ls)?
  │   ├─ Output curto, sem input do usuário? → execFile (com array de args)
  │   ├─ Output streaming? → spawn
  │   └─ Comando hardcoded sem input? → exec OK
  │       (com input do usuário → NUNCA exec — shell injection)
  │
  └─ Preciso spawn de processo Node isolado?
      ├─ Isolamento total (memória, native modules, security)? → fork
      ├─ CPU-bound só → Worker Thread (mais leve)
      └─ Supervisor tree / processo descartável → fork
  ```

- **## Tabela problema → ferramenta → razão:**

  | Problema | Ferramenta | Por quê |
  |---|---|---|
  | Hash bcrypt em handler | Worker Thread + pool | CPU-bound, mesmo processo, pool reusável |
  | Image processing 100MB/req | Worker Thread + transferList | Zero-copy de buffers grandes |
  | Matrix ops em ML inference | Worker Thread + SharedArrayBuffer | Memória compartilhada zero-copy |
  | Servir HTTP com 4 cores | K8s 4 réplicas / Cluster (single VM) | Round-robin de conexões |
  | Rodar `ffmpeg` | spawn | Streaming output |
  | Rodar `git log` curto | execFile | Buffered + sem shell |
  | Sandbox de código user | fork (ou vm/isolated-vm) | Isolamento total |
  | Worker tree (queue managers) | fork + supervisor pattern | Crash + respawn é OK |

- **## Na prática**: aplicar a decision tree:
  - Caso 1: endpoint que recebe upload de imagem e gera thumbnail → Worker Thread + pool (CPU-bound, freq alta)
  - Caso 2: API que executa `aws s3 ls` para o user → execFile com array de args (nunca exec)
  - Caso 3: build server que orquestra child processes → fork + supervisor
  - Caso 4: WebSocket server escalando em K8s → 4 pods, sem cluster nativo, sticky session via ingress
- **## Armadilhas (3+):**
  1. Confundir CPU-bound com problemas de DB lento — DB lento ≠ CPU-bound
  2. Usar Cluster + K8s sem pensar — overhead duplicado
  3. Achar que "vou usar Worker Thread" resolve qualquer problema — só CPU-bound
  4. exec com input do user — sempre vulnerabilidade
- **## Em entrevista**: frase pronta integrada + vocabulário consolidado
- **## Veja também**: 12, todos os outros do galho, MOC, Node.js, Runtime e Event Loop

- [ ] **Step 4: Verificar rubrica** (standard, fluxograma é o code sample principal)

- [ ] **Step 5: Commit**

```bash
git add "03-Dominios/Node/Paralelismo/11 - Decision tree - qual ferramenta para qual problema.md"
git commit -m "feat(node-paralelismo): add note 11 — Decision tree"
```

---

## Task 13: Nota 12 — Armadilhas e cheatsheet

**Files:**
- Create: `03-Dominios/Node/Paralelismo/12 - Armadilhas, regras práticas, cheatsheet.md`

**Conteúdo-chave do spec:** Top 10 armadilhas, cheatsheet visual (3 ferramentas × 5 atributos), decision tree compactada, vocabulário PT→EN consolidado, apontador pros próximos galhos.

- [ ] **Step 1: Síntese das 11 notas anteriores**

Reler todas as 11 notas e extrair as armadilhas mais críticas. Sintetizar.

- [ ] **Step 2: Frontmatter**

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
  - paralelismo
  - cheatsheet
  - armadilhas
  - referencia
aliases:
  - Cheatsheet paralelismo
  - Armadilhas Node paralelismo
---
```

- [ ] **Step 3: Escrever a nota (300-450 linhas, estrutura tópica)**

- **TL;DR**: cheatsheet de fechamento. Top 10 armadilhas, tabela ferramenta×atributo, decision tree compactada, vocabulário PT→EN, próximos galhos (3 streams, 5 observability, 6 security).
- **## Top 10 armadilhas** — lista numerada com (a) descrição 1 linha, (b) exemplo curto, (c) fix 1 linha:
  1. Worker sem `terminate` em shutdown → leak. Fix: `await pool.destroy()` ou `await worker.terminate()` em SIGTERM
  2. IPC leak (mensagens acumulando em fila do parent quando child não lê) → memory growth. Fix: backpressure ou fechar canal
  3. Race em `SharedArrayBuffer` sem `Atomics` → corrupção de estado. Fix: sempre `Atomics.load/store/add`
  4. `exec` com input do user → shell injection. Fix: `execFile`/`spawn` com array de args
  5. Cluster com state em memória (cache local) → comportamento inconsistente entre workers. Fix: state externo (Redis, DB)
  6. Fork sem cleanup de child em parent crash → zombies. Fix: child.kill() em SIGTERM do parent
  7. `transferList` esquecido em buffer grande → cópia silenciosa. Fix: `postMessage(buf, [buf])`
  8. Worker preso em loop síncrono → mensagens não processadas, terminate é única opção. Fix: dividir trabalho em chunks com yield (`setImmediate`)
  9. Cluster + sticky sessions sem reverse proxy ciente → WebSocket quebra. Fix: nginx `ip_hash` ou `@socket.io/sticky`
  10. spawn com `shell: true` → injection. Fix: nunca usar `shell: true` com input user
- **## Cheatsheet — 3 ferramentas × 5 atributos:**

  | Atributo | Worker Thread | Cluster | child_process |
  |---|---|---|---|
  | Modelo | shared-memory (mesma processo) | shared-port (multi-processo) | separate-process |
  | Custo criação | ~1ms | ~100ms | ~100ms |
  | IPC | postMessage / SAB | IPC built-in | stdio (spawn/exec) ou IPC (fork) |
  | Use case | CPU-bound em handler | Escalar HTTP em single-VM | Comando externo / Node child |
  | Lib de prod | piscina | PM2 (legacy) / orquestrador | — |

- **## Decision tree compactada** (versão 1-tela do que está em nota 11)
- **## Vocabulário PT→EN consolidado** (mínimo 18 termos do galho): paralelismo (parallelism), concorrência (concurrency), thread de trabalho (Worker Thread), porta-pai (parentPort), bifurcar (fork), spawnar (spawn), pool de workers (worker pool), memória compartilhada (shared memory), operação atômica (atomic operation), condição de corrida (race condition), comparar-e-trocar (compare-and-swap), aguardar-notificar (wait-notify), porta compartilhada (shared port), comunicação interprocess (IPC), injeção de shell (shell injection), zumbi (zombie), encerramento gracioso (graceful shutdown), orquestrador (orchestrator), réplica (replica).
- **## Próximos galhos:**
  - Pra **dados grandes sem bloquear**: galho 3 (Streams) — Readable, Writable, Transform, backpressure
  - Pra **observar workers/cluster em produção**: galho 5 (Observability) — métricas de pool, profiling de Worker Threads, alertas
  - Pra **isolamento e sandbox**: galho 6 (Segurança) — `vm` module, `isolated-vm`, Permission Model
- **## Veja também**: MOC, todas as 11 notas, Node.js (tronco), Runtime e Event Loop (galho 1)

- [ ] **Step 4: Verificar rubrica adaptada** (estrutura tópica):

```
[ ] TL;DR no callout [!abstract]
[ ] Top 10 armadilhas com 1 exemplo + 1 fix cada
[ ] Cheatsheet 3 ferramentas × 5 atributos
[ ] Decision tree compactada
[ ] Vocabulário PT→EN com 18+ termos
[ ] Wikilinks: 12+ (todas as notas + MOC + tronco + galho 1)
[ ] Frontmatter completo (tags inclui cheatsheet)
[ ] Sem fabricação
```

- [ ] **Step 5: Commit**

```bash
git add "03-Dominios/Node/Paralelismo/12 - Armadilhas, regras práticas, cheatsheet.md"
git commit -m "feat(node-paralelismo): add note 12 — Armadilhas, cheatsheet"
```

---

## Task 14: Pass final no MOC

**Files:**
- Modify: `03-Dominios/Node/Paralelismo/Paralelismo.md`

- [ ] **Step 1: Confirmar 12 notas existem**

```bash
ls "03-Dominios/Node/Paralelismo/" | wc -l
# Esperado: 13 (12 notas + MOC)
```

- [ ] **Step 2: Substituir o placeholder de intro**

Em `03-Dominios/Node/Paralelismo/Paralelismo.md`, encontrar:

```markdown
## Sobre este galho

(introdução curta — preencher na Task 14)
```

Substituir SOMENTE a linha `(introdução curta — preencher na Task 14)` por:

```markdown
Este galho cobre **as 3 ferramentas de paralelismo em Node**: Worker Threads (threads JS no mesmo processo), Cluster (múltiplos processos compartilhando porta HTTP), child_process (processo externo via spawn/exec ou Node child via fork). Inclui SharedArrayBuffer/Atomics (concorrência com memória compartilhada), pool de workers (pattern de produção, `piscina`), contexto de produção em 2026 (Cluster vs PM2 vs Kubernetes) e uma decision tree completa de "qual ferramenta para qual problema".

Pré-requisito: galho 1 ([[Runtime e Event Loop]]). Em particular as notas [[09 - async-await - o que é, o que não é]] (mito da performance) e [[10 - Bloqueio do event loop - sintomas e causas]] (sintomas que pedem paralelismo).

**Audiência primária:** dev senior em prep para entrevista internacional. Cada nota tem seção "Em entrevista" com frase pronta em inglês + vocabulário.

**Audiência secundária:** o mesmo dev decidindo arquitetura ou debugando problemas de CPU em produção.
```

Manter o header `## Sobre este galho`.

- [ ] **Step 3: Verificar todos os wikilinks resolvem**

Confirmar que cada `[[01 - ...]]` até `[[12 - ...]]` corresponde a um arquivo existente:

```bash
for i in 01 02 03 04 05 06 07 08 09 10 11 12; do
  ls "03-Dominios/Node/Paralelismo/" | grep "^$i" || echo "MISSING: nota $i"
done
```

Esperado: 12 linhas mostrando arquivos existentes; nenhum "MISSING".

- [ ] **Step 4: Verificar dataview**

Garantir que o bloco dataview tem o caminho `"03-Dominios/Node/Paralelismo"` (não `"Runtime e Event Loop"` por copy-paste do galho 1).

- [ ] **Step 5: Commit**

```bash
git add "03-Dominios/Node/Paralelismo/Paralelismo.md"
git commit -m "feat(node-paralelismo): finalize MOC with all wikilinks and intro"
```

---

## Task 15: Poda do tronco

**Files:**
- Modify: `03-Dominios/JavaScript/Backend/Node.js.md`

Esta é uma poda **mais simples** que a do galho 1 (uma seção só vs cinco).

- [ ] **Step 1: Localizar a seção a podar**

```bash
grep -n "^### Worker Threads.*paralelismo\|^### Worker Threads.*cluster" "03-Dominios/JavaScript/Backend/Node.js.md"
```

Esperado: 1 match. Anotar o número da linha. Depois encontrar onde termina (próxima `###` ou `##`).

- [ ] **Step 2: Substituir a seção `### Worker Threads, cluster, child_process — as 3 formas de paralelismo`**

Substituir TODO o conteúdo entre o `### Worker Threads...` e a próxima seção (mantendo o header) por:

```markdown
### Worker Threads, cluster, child_process — as 3 formas de paralelismo

> [!nota] Migrado para galho próprio
> As 3 ferramentas de paralelismo foram expandidas em [[Paralelismo]] (galho 2). Veja em particular [[02 - As 3 ferramentas - Worker Threads, Cluster, child_process]] (visão geral comparativa), [[03 - Worker Threads - fundamentos]] (Worker Threads), [[07 - Cluster - escalando HTTP por CPU]] (Cluster), [[08 - child_process com exec e spawn]] (rodar comandos externos) e [[09 - child_process com fork - Node child com IPC]] (Node child isolado). Decision tree completa em [[11 - Decision tree - qual ferramenta para qual problema]].
```

**IMPORTANTE:** Preservar o nível EXATO do header (`###` três hashes). Cuidado para não deletar a seção seguinte.

- [ ] **Step 3: Adicionar wikilink no `## Veja também` do tronco**

No tronco, encontrar `## Veja também` (perto do final). Adicionar como **segundo bullet** (depois de `[[Runtime e Event Loop]]` que foi adicionado no galho 1):

```markdown
- [[Paralelismo]] — galho 2 da trilha Node Senior; as 3 ferramentas de paralelismo (Worker Threads, Cluster, child_process), SharedArrayBuffer/Atomics, pool de workers, decision tree
```

- [ ] **Step 4: Atualizar `updated` no frontmatter do tronco**

Mudar `updated: 2026-05-07` (já estava nesse valor desde o galho 1) — confirmar que está em `2026-05-07`. Se estiver em data anterior, atualizar.

- [ ] **Step 5: Commit**

```bash
git add "03-Dominios/JavaScript/Backend/Node.js.md"
git commit -m "refactor(node): prune trunk Node.js.md, link to Paralelismo branch"
```

---

## Task 16: MOC central + verificação final

**Files:**
- Modify: `03-Dominios/Node/index.md`

- [ ] **Step 1: Atualizar MOC central**

Em `03-Dominios/Node/index.md`, encontrar a seção:

```markdown
### Galhos da trilha Node Senior

- [[Runtime e Event Loop]] — galho 1: o motor do Node (single-thread, libuv, fases, microtasks, async/await, bloqueio, diagnóstico)
```

Adicionar logo abaixo:

```markdown
- [[Paralelismo]] — galho 2: as 3 ferramentas de paralelismo (Worker Threads, Cluster, child_process), SharedArrayBuffer/Atomics, pool de workers, contexto de produção, decision tree
```

Atualizar `updated: 2026-05-07` no frontmatter (se ainda não estiver).

- [ ] **Step 2: Commit MOC central**

```bash
git add "03-Dominios/Node/index.md"
git commit -m "feat(node-paralelismo): wire branch into central Node MOC"
```

- [ ] **Step 3: Verificação final — critérios de aceitação**

```bash
# 1. 13 arquivos no diretório
ls "03-Dominios/Node/Paralelismo/" | wc -l
# Esperado: 13

# 2. Todos com publish: true
grep -l "publish: true" "03-Dominios/Node/Paralelismo/"*.md | wc -l
# Esperado: 13

# 3. Total de linhas do galho
wc -l "03-Dominios/Node/Paralelismo/"*.md | tail -1

# 4. Tronco tem agora 5 callouts (4 do galho 1 + 1 do galho 2)
grep -c "Migrado para galho próprio" "03-Dominios/JavaScript/Backend/Node.js.md"
# Esperado: 5

# 5. MOC central linka pros 2 galhos
grep -E "Runtime e Event Loop|Paralelismo" "03-Dominios/Node/index.md" | grep -v "^#" | wc -l
# Esperado: pelo menos 2 matches (1 por galho)
```

Reportar o resultado de cada check.

- [ ] **Step 4: Closing commit**

```bash
git commit --allow-empty -m "chore(node-paralelismo): close branch Galho 2 — Paralelismo

12 atomic notes + MOC published in 03-Dominios/Node/Paralelismo/.
Trunk Node.js.md pruned (single section). Central Node MOC updated.
All acceptance criteria from 2026-05-07-node-paralelismo-design.md met."
```

**Sem `Co-Authored-By`.**

- [ ] **Step 5: Quartz check (passivo)**

O Quartz tem deploy via CI (`.github/workflows/trigger-site-deploy.yaml`); commits em main disparam o build automaticamente. Não é necessário rodar localmente. Mencionar no relatório.

---

## Pós-execução

1. **Atualizar memória se algum aprendizado novo apareceu** — galho 2 tem peculiaridades (poda mais simples; novo padrão de wikilinks pro galho anterior; SharedArrayBuffer sem limite de tamanho)
2. **Revisar `2026-05-07-node-roadmap-design.md`** com aprendizados — afinar a "Política de poda do tronco" se necessário
3. **Decidir destino final do tronco** — se já passou do galho 1 + galho 2, o tronco está com 5 callouts; mais um galho e a estrutura começa a se inverter (mais callouts que conteúdo). Ponto de avaliar se vira MOC.
4. **Próximo galho** — escolher entre Galho 3 (Streams), Galho 5 (Observability), Galho 4 (Frameworks), ou Galho 6 (Segurança), conforme prioridade do momento

---

## Self-review do plano

- **Spec coverage:**
  - 12 nomes de nota do spec seção 5 cobertos por Tasks 2-13 ✓
  - MOC criado em Task 1, finalizado em Task 14 ✓
  - 5 rotas alternativas presentes no MOC esqueleto (Task 1) — incluindo "completa" implícita ✓
  - Tasks de poda (spec seção 10): cobertas em Task 15 ✓
  - Atualização do MOC central: Task 16 ✓
  - Critérios de aceitação (spec seção 12): checklist em Task 16 step 3 ✓
  - Bibliografia (spec seção 8): centralizada no topo + WebFetch específico em cada Task ✓
  - Restrição de fabricação: bloco no topo + na rubrica de cada nota ✓
  - Nota 05 (SharedArrayBuffer) sem limite artificial — consistente com spec refinement aprovado pelo usuário ✓

- **Placeholder scan:** O único `(introdução curta — preencher na Task 14)` é placeholder INTENCIONAL com instrução explícita de substituição — não é placeholder de plano ✓

- **Type consistency:** títulos de notas batem entre Task de criação, MOC esqueleto (Task 1), pass final (Task 14), e poda do tronco (Task 15). Wikilinks usam mesmo título nominal em todas as ocorrências ✓

- **Coesão com galho 1:** wikilinks pra `[[Runtime e Event Loop]]`, `[[09 - async-await - o que é, o que não é]]`, `[[10 - Bloqueio do event loop - sintomas e causas]]` aparecem nas notas certas (especialmente nota 01) ✓
