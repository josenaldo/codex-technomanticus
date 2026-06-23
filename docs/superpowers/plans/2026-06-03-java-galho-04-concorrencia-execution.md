# Galho 4 — Concorrência e paralelismo (Java Senior) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Criar o Galho 4 da trilha Java Senior — 16 notas atômicas de concorrência em 3 fases + MOC do galho + expansão do Dicionário de Java + ativação do MOC central + poda integral do tronco `Java Concurrency`.

**Architecture:** Padrão tronco/galhos + 3 fases (Iniciado/Adepto/Magus). Pasta flat `03-Dominios/Tecnologia/Java/Concorrência e paralelismo/`, notas atômicas `publish: true` em PT-BR, numeração global 01-16 (4 Iniciado / 6 Adepto / 6 Magus). Cada nota refatora/expande material do tronco `Core/Java Concurrency.md` (matéria-prima, não cópia 1:1); features version-specific (virtual threads, structured concurrency, scoped values) verificadas via JEP/doc oficial. Ao fim, o tronco é podado **integralmente** (todo conteúdo migra → redirect enxuto) e a fabricação higienizada. Branch dedicada `java-galho-04-concorrencia` (NÃO em `main`).

**Tech Stack:** Obsidian Flavored Markdown, frontmatter YAML, wikilinks, callouts, Dataview, Quartz v4 (publicação). Verificação de fonte via WebFetch (dev.java, docs.oracle.com, openjdk.org/jeps).

---

## Convenções aplicadas a TODAS as notas (ler antes de qualquer task)

**Frontmatter** (ajustar `title`/`fase`/`tags`/`aliases` por nota; `created`/`updated: 2026-06-03`):

```yaml
---
title: "<título sem prefixo numérico>"
created: 2026-06-03
updated: 2026-06-03
type: concept
progress: backlog
status: seedling
publish: true
fase: iniciado | adepto | magus
tags:
  - java
  - concorrencia
  - <fase>
  - <1-3 tags de conceito>
aliases:
  - <aliases>
---
```

**Estrutura H2 obrigatória** (nesta ordem):

1. `> [!abstract] TL;DR` — 2-4 linhas (conceito central + regra prática + por que importa). Callout, NÃO H2.
2. `## O que é` — definição.
3. `## Por que importa` — relevância pra senior/entrevista. (Pode fundir com "O que é" em notas Iniciado curtas.)
4. `## Como funciona` — H3s; mínimo 3 subseções em notas Adepto/Magus.
5. `## Na prática` — exemplos compiláveis, framing neutro ("padrão observado no JDK/Spring", hipotético explícito `// hipotético:`). NUNCA "no meu projeto". Concorrência: ao demonstrar race/visibility bug, declarar que o output é **não-determinístico**.
6. `## Armadilhas` — ≥2 (Iniciado) / ≥3 (Adepto/Magus). Cada armadilha: `### (N) Título` + descrição + exemplo curto de código demonstrando o problema + fix em 1 linha.
7. `## Em entrevista` — frase pronta em inglês com **3+ sentenças** (trade-off + decisão + caveat) + sub-bloco "Vocabulário" com **6+ termos PT→EN** traduzidos.
8. `## Veja também` — wikilinks SEM backticks. Sempre inclui: notas relacionadas do galho + `[[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|MOC do galho]]` + `[[03-Dominios/Tecnologia/Java/index|Trilha Java]]` + `[[Java Concurrency]]` (tronco) + verbetes do Dicionário relevantes.
9. `## Referências` — docs oficiais + JEPs + *Java Concurrency in Practice* (Goetz) quando pertinente.

**Tamanho:** 200-500 linhas (notas Magus densas até 700; notas 11 JMM e 12 Loom podem ir mais alto — contingência de divisão na própria task).

**Restrições absolutas** (qualquer violação reprova a nota):
- Sem fabricação de experiência pessoal. Exemplos: `Order`, `Customer`, `account`, ou `// hipotético: ...`. NUNCA `josenaldo`/caminhos pessoais/casos vividos.
- Sem invenção de API/feature/versão. Feature version-specific → WebFetch da fonte oficial/JEP no Step de pesquisa. Status GA/preview hedged.
- Comparações justas ("quando X vence" E "quando Y vence") — em especial "virtual threads não substituem tudo".
- Versões hedged (ex: "virtual threads são GA no Java 21 (JEP 444); structured concurrency e scoped values tornaram-se final no Java 25 — verifique sua versão").
- Não linkar notas de galhos inexistentes (2 Streams, 3 JVM, 11 Reativa). Quando o conceito conectar, linkar o **tronco** `[[Java Fundamentals]]` ou `[[Java Concurrency]]`.
- Code fences: ` ```java ` pra código, ` ```text ` pra output/thread dump/erro. Sempre fechadas.
- Commits: sem `Co-Authored-By: Claude`; sem `--no-verify`; `git add <path>` nominal (nunca `git add -A`); 1 commit por nota.

**Material de origem:** `03-Dominios/Tecnologia/Java/Core/Java Concurrency.md` (ler a seção indicada em cada task como matéria-prima; expandir, não copiar). Spec de referência: `docs/superpowers/specs/2026-06-03-java-galho-04-concorrencia-design.md` §5. Template de qualidade: notas do Galho 1 em `03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/`.

**Modelo por nota:** sonnet por padrão; **opus** nas notas 11 (JMM) e 12 (Virtual Threads/Loom) — as mais densas.

---

## Task 0: Pré-flight — branch, pasta, versões e leitura do tronco

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Concorrência e paralelismo/` (pasta)
- Read: `03-Dominios/Tecnologia/Java/Core/Java Concurrency.md`

- [ ] **Step 1: Criar a branch dedicada**

```bash
git checkout -b java-galho-04-concorrencia
git branch --show-current
```
Expected: `java-galho-04-concorrencia` (NÃO trabalhar em `main`).

- [ ] **Step 2: Criar a pasta do galho**

```bash
mkdir -p "03-Dominios/Tecnologia/Java/Concorrência e paralelismo"
```

- [ ] **Step 3: Ler o tronco e confirmar headings reais**

Ler `03-Dominios/Tecnologia/Java/Core/Java Concurrency.md` inteiro. Anotar os números de linha REAIS das seções (mapa de poda no §6 do spec): "Threads na JVM", "Java Memory Model (JMM)", "Synchronized", "java.util.concurrent.locks", "Atomic classes", "Concurrent Collections", "ExecutorService e Thread Pools", "CompletableFuture", "Sincronizadores", "ForkJoinPool", "Parallel Streams", "Virtual Threads", "Structured Concurrency", "Scoped Values", "Deadlock, Race Condition e companhia", "Patterns de design concorrente", "Debugging e profiling", "Armadilhas comuns", e a seção de fabricação `## Na prática (da minha experiência)` (≈ linha 1441).

- [ ] **Step 4: Fixar versões assumidas do galho**

Baseline: **Java 21 LTS** (virtual threads GA) e **Java 25 LTS** (structured concurrency + scoped values final). WebFetch `https://openjdk.org/jeps/444` (Virtual Threads) e `https://dev.java/evolution/` pra confirmar: status GA dos virtual threads (21), e o release exato em que structured concurrency e scoped values saíram de preview pra final. Registrar — será usado nas notas 12/13/14.

- [ ] **Step 5: Sem commit** (task de preparação; nada a versionar ainda).

---

## Fase INICIADO (notas 01-04)

### Task 1: Nota 01 — Concorrência e paralelismo: o modelo

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Concorrência e paralelismo/01 - Concorrência e paralelismo - o modelo.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch `https://dev.java/learn/` (seção concurrency) e `https://docs.oracle.com/javase/tutorial/essential/concurrency/` pra confirmar a distinção concorrência vs paralelismo e o modelo de threads da JVM.

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: iniciado`, tags `[java, concorrencia, iniciado, threads, fundamentos]`, aliases `["Concorrência", "Paralelismo"]`.

Conteúdo (matéria-prima: tronco "## O que é" + intro de "Threads na JVM"):
- TL;DR: concorrência = lidar com muitas tarefas; paralelismo = executá-las ao mesmo tempo; Java usa memória compartilhada → daí a dificuldade.
- `## O que é` — concorrência vs paralelismo (definições + analogia), processos vs threads (memória compartilhada vs isolada).
- `## Por que importa` — pra senior: a maioria dos bugs difíceis de produção é concorrência; entrevista cobra o modelo mental.
- `## Como funciona` — H3s: "Processos vs threads", "Modelo de memória compartilhada" (vs message-passing), "Os três problemas: atomicidade, visibilidade, ordenação" (teaser, deep no 11), "O landscape moderno: platform vs virtual threads" (marco, deep no 12).
- `## Armadilhas` — ≥2: (1) confundir concorrência com paralelismo; (2) "mais threads = mais rápido" (contention, context switch). Exemplo + fix.
- `## Em entrevista` — frase 3+ sentenças sobre concorrência vs paralelismo e o trade-off de shared memory; vocabulário 6+ termos.
- `## Veja também` — 02, 03, 04, 11, 12, MOC galho, MOC central, tronco, verbetes `mutual exclusion (exclusão mútua)`/`contention`.
- `## Referências` — dev.java, docs Oracle, *Java Concurrency in Practice*.

Tamanho: 200-320 linhas (abertura, mais conceitual).

- [ ] **Step 3: Verificar a nota**

```bash
head -20 "03-Dominios/Tecnologia/Java/Concorrência e paralelismo/01 - Concorrência e paralelismo - o modelo.md"
grep -cE "^## (O que é|Como funciona|Armadilhas|Em entrevista|Veja também|Referências)" "03-Dominios/Tecnologia/Java/Concorrência e paralelismo/01 - Concorrência e paralelismo - o modelo.md"
```
Expected: frontmatter com `fase: iniciado`; grep retorna ≥6.

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/Concorrência e paralelismo/01 - Concorrência e paralelismo - o modelo.md"
git commit -m "feat(java): galho 4 nota 01 — concorrência e paralelismo: o modelo"
```

---

### Task 2: Nota 02 — Threads e seu ciclo de vida

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Concorrência e paralelismo/02 - Threads e seu ciclo de vida.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch doc de `Thread` (`https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/Thread.html`) e `Thread.State`. Confirmar estados e a política de interrupção (`InterruptedException`).

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: iniciado`, tags `[java, concorrencia, iniciado, threads, lifecycle]`, aliases `["Thread", "Ciclo de vida de thread"]`.

Conteúdo (matéria-prima: tronco "## Threads na JVM" — Platform Threads, Estados, Thread dump):
- `## Como funciona` — H3s: "`Thread` vs `Runnable`" (`start` vs `run`), "Estados de uma thread" (NEW→RUNNABLE→BLOCKED/WAITING/TIMED_WAITING→TERMINATED + diagrama), "Controle: `join`/`interrupt`/`sleep`/`yield`", "Daemon vs user threads", "Ler um thread dump (intro)".
- `## Na prática` — criar/iniciar thread com lambda; interrupção cooperativa.
- `## Armadilhas` — ≥2: (1) chamar `run()` direto (roda na thread atual, não cria nova); (2) engolir `InterruptedException` (perder o sinal — restaurar com `Thread.currentThread().interrupt()`); (3) `Thread.stop()` deprecado/inseguro. Exemplo + fix.
- `## Em entrevista` + `## Veja também` (01, 03, 08, MOC, tronco, verbete `thread pool`) + `## Referências`.

Tamanho: 250-380 linhas.

- [ ] **Step 3: Verificar**

```bash
grep -E "^fase: iniciado" "03-Dominios/Tecnologia/Java/Concorrência e paralelismo/02 - Threads e seu ciclo de vida.md"
grep -E "RUNNABLE|BLOCKED|WAITING|InterruptedException" "03-Dominios/Tecnologia/Java/Concorrência e paralelismo/02 - Threads e seu ciclo de vida.md" | head
```
Expected: `fase: iniciado`; cobre estados + interrupção.

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/Concorrência e paralelismo/02 - Threads e seu ciclo de vida.md"
git commit -m "feat(java): galho 4 nota 02 — threads e seu ciclo de vida"
```

---

### Task 3: Nota 03 — Exclusão mútua com synchronized

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Concorrência e paralelismo/03 - Exclusão mútua com synchronized.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch `https://docs.oracle.com/javase/tutorial/essential/concurrency/sync.html` (intrinsic locks, synchronized) e a seção de `wait`/`notify` (guarded blocks).

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: iniciado`, tags `[java, concorrencia, iniciado, synchronized, locks]`, aliases `["synchronized", "Exclusão mútua"]`.

Conteúdo (matéria-prima: tronco "## Synchronized" — todas as subseções, incl. wait/notify, anti-patterns):
- `## O que é` — race condition concreta (contador `i++` perdendo updates) → necessidade de mutual exclusion.
- `## Como funciona` — H3s: "Intrinsic lock / monitor", "`synchronized` em methods, blocks e static", "Reentrância", "`wait`/`notify`/`notifyAll` e o loop de guarda (`while`, não `if`)".
- `## Na prática` — contador thread-safe; producer-consumer mínimo com wait/notify.
- `## Armadilhas` — ≥2: (1) lock em `String`/`Integer` cacheado ou objeto que muda (lock instável); (2) `if` em vez de `while` no wait (spurious wakeup); (3) escopo `synchronized` amplo demais (contention). Exemplo + fix.
- `## Em entrevista` + `## Veja também` (02, 04, 05, 11, MOC, tronco, verbetes `synchronized`/`monitor (intrinsic lock)`/`mutual exclusion (exclusão mútua)`) + `## Referências`.

Tamanho: 280-420 linhas.

- [ ] **Step 3: Verificar**

```bash
grep -E "synchronized|monitor|wait|notify|reentr" "03-Dominios/Tecnologia/Java/Concorrência e paralelismo/03 - Exclusão mútua com synchronized.md" | head
```

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/Concorrência e paralelismo/03 - Exclusão mútua com synchronized.md"
git commit -m "feat(java): galho 4 nota 03 — exclusão mútua com synchronized"
```

---

### Task 4: Nota 04 — As armadilhas: race, deadlock e companhia

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Concorrência e paralelismo/04 - As armadilhas - race, deadlock e companhia.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch `https://docs.oracle.com/javase/tutorial/essential/concurrency/deadlock.html` (deadlock, livelock, starvation). Confirmar as 4 condições de Coffman.

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: iniciado`, tags `[java, concorrencia, iniciado, deadlock, race-condition]`, aliases `["Race condition", "Deadlock"]`.

Conteúdo (matéria-prima: tronco "## Deadlock, Race Condition e companhia"):
- `## Como funciona` — H3s: "Race condition" (check-then-act, read-modify-write), "Deadlock" (4 condições de Coffman + prevenção via lock ordering / tryLock com timeout), "Livelock", "Starvation e fairness", "Visibility e publication bugs (teaser)" — apontar deep pro 11.
- `## Na prática` — deadlock clássico (duas contas, transferência cruzada) + fix por ordenação de locks.
- `## Armadilhas` — ≥2: (1) adquirir locks em ordem inconsistente (deadlock); (2) "funciona na minha máquina" (race latente que só aparece sob carga); (3) starvation por thread de baixa prioridade. Exemplo + fix.
- `## Em entrevista` + `## Veja também` (03, 05, 11, 16, MOC, tronco, verbetes `condição de corrida (race condition)`/`deadlock`/`livelock`/`starvation`) + `## Referências`.

Tamanho: 260-400 linhas.

- [ ] **Step 3: Verificar**

```bash
grep -E "deadlock|race|livelock|starvation|Coffman" "03-Dominios/Tecnologia/Java/Concorrência e paralelismo/04 - As armadilhas - race, deadlock e companhia.md" | head
```

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/Concorrência e paralelismo/04 - As armadilhas - race, deadlock e companhia.md"
git commit -m "feat(java): galho 4 nota 04 — armadilhas: race, deadlock e companhia"
```

---

## Fase ADEPTO (notas 05-10)

### Task 5: Nota 05 — Locks explícitos (java.util.concurrent.locks)

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Concorrência e paralelismo/05 - Locks explícitos.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch docs de `ReentrantLock`, `ReadWriteLock`, `StampedLock` (`https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/locks/package-summary.html`). Confirmar que `StampedLock` NÃO é reentrante e o padrão optimistic read.

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: adepto`, tags `[java, concorrencia, adepto, locks, reentrantlock]`, aliases `["ReentrantLock", "Locks explícitos", "StampedLock"]`.

Conteúdo (matéria-prima: tronco "## java.util.concurrent.locks"):
- `## Como funciona` — H3s: "`Lock` e `ReentrantLock`" (padrão `lock()`/`try`/`finally unlock()`, `tryLock`, timeout, fairness, `lockInterruptibly`), "`ReadWriteLock`" (muitos leitores/poucos escritores), "`StampedLock`" (optimistic read, não-reentrante), "`Condition`" (vs wait/notify).
- `## Na prática` — cache com ReadWriteLock; optimistic read com StampedLock.
- `## Por que importa` / comparação justa: "`synchronized` vs `Lock`" (quando cada um vence — synchronized é mais simples e legível; Lock dá tryLock/timeout/fairness/interruptibilidade).
- `## Armadilhas` — ≥3: (1) esquecer `unlock()` fora do `finally` (lock vazado em exceção); (2) tratar `StampedLock` como reentrante (deadlock consigo mesmo); (3) fairness matando throughput. Exemplo + fix.
- `## Em entrevista` + `## Veja também` (03, 06, 04, MOC, tronco, verbete `synchronized`) + `## Referências`.

Tamanho: 300-440 linhas.

- [ ] **Step 3: Verificar**

```bash
grep -E "ReentrantLock|ReadWriteLock|StampedLock|tryLock|Condition" "03-Dominios/Tecnologia/Java/Concorrência e paralelismo/05 - Locks explícitos.md" | head
```

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/Concorrência e paralelismo/05 - Locks explícitos.md"
git commit -m "feat(java): galho 4 nota 05 — locks explícitos (j.u.c.locks)"
```

---

### Task 6: Nota 06 — Atômicos e operações lock-free

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Concorrência e paralelismo/06 - Atômicos e operações lock-free.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch docs de `java.util.concurrent.atomic` (package-summary) e `LongAdder`. Confirmar semântica de CAS e o problema ABA com `AtomicStampedReference`.

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: adepto`, tags `[java, concorrencia, adepto, atomics, lock-free]`, aliases `["Atomic", "CAS", "lock-free"]`.

Conteúdo (matéria-prima: tronco "## Atomic classes"):
- `## Como funciona` — H3s: "`AtomicInteger`/`AtomicLong`/`AtomicReference`", "CAS (compare-and-swap) e `compareAndSet`" (instrução de hardware, base do lock-free), "`getAndUpdate`/`updateAndGet`/`accumulateAndGet`", "`LongAdder`/`DoubleAdder` (striping sob alta contention)", "`AtomicStampedReference` e o problema ABA".
- `## Na prática` — contador lock-free com `AtomicLong`; sequence generator com CAS loop; métrica de alto volume com `LongAdder`.
- `## Armadilhas` — ≥3: (1) loop CAS sem limite virando quase-livelock sob contention extrema; (2) problema ABA com `AtomicReference` simples; (3) assumir que `LongAdder.sum()` é instantâneo-consistente (é aproximado durante updates). Exemplo + fix.
- `## Em entrevista` + `## Veja também` (05, 07, 11, MOC, tronco, verbetes `atomic (variável atômica)`/`CAS (compare-and-swap)`/`ABA problem`/`lock-free`) + `## Referências`.

Tamanho: 300-440 linhas.

- [ ] **Step 3: Verificar**

```bash
grep -E "AtomicInteger|compareAndSet|CAS|LongAdder|ABA" "03-Dominios/Tecnologia/Java/Concorrência e paralelismo/06 - Atômicos e operações lock-free.md" | head
```

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/Concorrência e paralelismo/06 - Atômicos e operações lock-free.md"
git commit -m "feat(java): galho 4 nota 06 — atômicos e operações lock-free"
```

---

### Task 7: Nota 07 — Concurrent collections

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Concorrência e paralelismo/07 - Concurrent collections.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch docs de `ConcurrentHashMap`, `CopyOnWriteArrayList`, `BlockingQueue`. Confirmar atomicidade de `computeIfAbsent`/`merge` e a semântica aproximada de `size()`.

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: adepto`, tags `[java, concorrencia, adepto, collections, concurrent-collections]`, aliases `["ConcurrentHashMap", "BlockingQueue", "Concurrent collections"]`.

Conteúdo (matéria-prima: tronco "## Concurrent Collections"):
- `## Como funciona` — H3s: "`ConcurrentHashMap`" (operações atômicas `computeIfAbsent`/`merge`, `size()` aproximado, sem null), "`CopyOnWriteArrayList`/`Set`" (read-heavy), "`BlockingQueue`" (`ArrayBlockingQueue` bounded vs `LinkedBlockingQueue`, `put`/`take`, producer-consumer), "`ConcurrentLinkedQueue`" (não-bloqueante), "`ConcurrentSkipListMap`/`Set`" (ordenado).
- `## Na prática` — cache concorrente com `computeIfAbsent`; pipeline producer-consumer com `BlockingQueue`. Árvore de decisão (qual escolher). Liga ao Galho 2 (Collections base) via tronco `[[Java Fundamentals]]`.
- `## Armadilhas` — ≥3: (1) `Collections.synchronizedMap` + iteração não-atômica (precisa lock externo); (2) compound op não-atômica em ConcurrentHashMap (`get` depois `put` — usar `compute`); (3) `CopyOnWriteArrayList` em workload write-heavy (cópia a cada escrita). Exemplo + fix.
- `## Em entrevista` + `## Veja também` (06, 08, 09, MOC, tronco, verbetes `ConcurrentHashMap`/`BlockingQueue`) + `## Referências`.

Tamanho: 300-440 linhas.

- [ ] **Step 3: Verificar**

```bash
grep -E "ConcurrentHashMap|CopyOnWrite|BlockingQueue|computeIfAbsent" "03-Dominios/Tecnologia/Java/Concorrência e paralelismo/07 - Concurrent collections.md" | head
```

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/Concorrência e paralelismo/07 - Concurrent collections.md"
git commit -m "feat(java): galho 4 nota 07 — concurrent collections"
```

---

### Task 8: Nota 08 — Executors e thread pools

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Concorrência e paralelismo/08 - Executors e thread pools.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch docs de `ExecutorService`, `ThreadPoolExecutor`, `Executors`. Confirmar os perigos dos factory methods (queue/pool unbounded) e os parâmetros do `ThreadPoolExecutor`.

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: adepto`, tags `[java, concorrencia, adepto, executors, thread-pools]`, aliases `["ExecutorService", "Thread pool", "ThreadPoolExecutor"]`.

Conteúdo (matéria-prima: tronco "## ExecutorService e Thread Pools" + intro de "## ForkJoinPool"):
- `## Como funciona` — H3s: "`Executor`/`ExecutorService`/`ScheduledExecutorService`", "Factory methods e seus perigos" (`newCachedThreadPool` ilimitado vs `newFixedThreadPool` com queue ilimitada), "`ThreadPoolExecutor` (controle fino: core/max/keep-alive/workQueue/rejection policy)", "`Future`, `submit`/`invokeAll`/`invokeAny`", "Shutdown gracioso (`shutdown` vs `shutdownNow` + `awaitTermination`)", "Dimensionar o pool (CPU-bound ≈ N+1; IO-bound maior; lei de Little)".
- `## Na prática` — pool configurado à mão com rejection policy; shutdown ordenado.
- `## Armadilhas` — ≥3: (1) não fazer shutdown (threads non-daemon impedem JVM de encerrar / leak); (2) pool/queue ilimitado (OOM sob carga); (3) exceção engolida em task submetida via `execute` (sem Future pra propagar). Exemplo + fix.
- `## Em entrevista` + `## Veja também` (02, 10, 15, MOC, tronco, verbetes `Executor / ExecutorService`/`thread pool`/`Future`) + `## Referências`.

Tamanho: 320-460 linhas.

- [ ] **Step 3: Verificar**

```bash
grep -E "ExecutorService|ThreadPoolExecutor|shutdown|rejection|Future" "03-Dominios/Tecnologia/Java/Concorrência e paralelismo/08 - Executors e thread pools.md" | head
```

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/Concorrência e paralelismo/08 - Executors e thread pools.md"
git commit -m "feat(java): galho 4 nota 08 — executors e thread pools"
```

---

### Task 9: Nota 09 — Sincronizadores

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Concorrência e paralelismo/09 - Sincronizadores.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch docs de `CountDownLatch`, `CyclicBarrier`, `Semaphore`, `Phaser`, `Exchanger`. Confirmar one-shot (latch) vs reutilizável (barrier).

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: adepto`, tags `[java, concorrencia, adepto, sincronizadores, semaphore]`, aliases `["CountDownLatch", "Semaphore", "CyclicBarrier"]`.

Conteúdo (matéria-prima: tronco "## Sincronizadores"):
- `## Como funciona` — H3s: "`CountDownLatch` (one-shot, espera N eventos)", "`CyclicBarrier` (reutilizável, N threads se esperam + barrier action)", "`Semaphore` (N permits, recurso limitado)", "`Phaser` (fases dinâmicas)", "`Exchanger` (troca entre 2 threads)". Tabela "latch vs barrier vs semaphore — quando usar".
- `## Na prática` — startup gate com latch; rate limiting com semaphore.
- `## Armadilhas` — ≥3: (1) tentar reusar `CountDownLatch` (não dá — é one-shot; usar `CyclicBarrier`); (2) `BrokenBarrierException` quando uma thread morre/timeouta na barrier; (3) `Semaphore` sem `release()` no `finally` (permits vazam). Exemplo + fix.
- `## Em entrevista` + `## Veja também` (07, 08, MOC, tronco, verbetes `latch (CountDownLatch)`/`barrier (CyclicBarrier)`/`semaphore (semáforo)`) + `## Referências`.

Tamanho: 280-420 linhas.

- [ ] **Step 3: Verificar**

```bash
grep -E "CountDownLatch|CyclicBarrier|Semaphore|Phaser|Exchanger" "03-Dominios/Tecnologia/Java/Concorrência e paralelismo/09 - Sincronizadores.md" | head
```

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/Concorrência e paralelismo/09 - Sincronizadores.md"
git commit -m "feat(java): galho 4 nota 09 — sincronizadores"
```

---

### Task 10: Nota 10 — CompletableFuture e composição assíncrona

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Concorrência e paralelismo/10 - CompletableFuture e composição assíncrona.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch doc de `CompletableFuture` (`https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/CompletableFuture.html`). Confirmar `thenCompose` vs `thenApply`, `orTimeout`/`completeOnTimeout` (Java 9+) e o executor default (common pool).

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: adepto`, tags `[java, concorrencia, adepto, completablefuture, async]`, aliases `["CompletableFuture", "Composição assíncrona"]`.

Conteúdo (matéria-prima: tronco "## CompletableFuture"):
- `## Como funciona` — H3s: "Criação (`supplyAsync`/`runAsync`)", "Transformação (`thenApply`/`thenAccept`/`thenRun`)", "Encadeamento: `thenCompose` (flatMap) vs `thenApply` (map)", "Combinação (`thenCombine`/`allOf`/`anyOf`)", "Error handling (`exceptionally`/`handle`/`whenComplete`)", "Timeout (`orTimeout`/`completeOnTimeout`, Java 9+)", "Async vs sync variants e qual executor (common pool default)".
- `## Na prática` — orquestrar 2 chamadas paralelas e combinar; fan-out/fan-in com `allOf`.
- `## Armadilhas` — ≥3: (1) bloquear IO no common pool (satura o pool compartilhado — passar executor próprio); (2) `get()` sem timeout (trava indefinidamente); (3) perder exceção sem `handle`/`exceptionally` (falha silenciosa). Exemplo + fix.
- `## Em entrevista` + `## Veja também` (08, 12, 15, MOC, tronco, verbetes `CompletableFuture`/`Future`) + `## Referências`.

Tamanho: 320-460 linhas.

- [ ] **Step 3: Verificar**

```bash
grep -E "supplyAsync|thenCompose|thenCombine|exceptionally|orTimeout" "03-Dominios/Tecnologia/Java/Concorrência e paralelismo/10 - CompletableFuture e composição assíncrona.md" | head
```

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/Concorrência e paralelismo/10 - CompletableFuture e composição assíncrona.md"
git commit -m "feat(java): galho 4 nota 10 — CompletableFuture e composição assíncrona"
```

---

## Fase MAGUS (notas 11-16)

### Task 11: Nota 11 — Java Memory Model em profundidade  ⟦opus⟧

> **Contingência:** se passar de ~700 linhas, dividir em `11 - Java Memory Model` + uma nota dedicada de "Safe publication", renumerando as Magus seguintes (galho viraria 17 notas). Decidir na execução; atualizar MOC e tasks 12+.

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Concorrência e paralelismo/11 - Java Memory Model em profundidade.md`

- [ ] **Step 1: Pesquisar fonte (usar modelo opus)**

WebFetch a especificação do JMM: `https://docs.oracle.com/javase/specs/jls/se21/html/jls-17.html` (JLS §17.4, happens-before) e material de referência sobre `volatile`/final fields. Confirmar as regras de happens-before e a semântica de publicação de final fields.

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: magus`, tags `[java, concorrencia, magus, jmm, volatile]`, aliases `["Java Memory Model", "JMM", "happens-before", "volatile"]`.

Conteúdo (matéria-prima: tronco "## Java Memory Model (JMM)" + "### Final fields" + "### Visibility bugs" + "### Publication bugs"):
- `## O que é` — por que existe um modelo de memória (CPUs/compiladores reordenam; caches não são coerentes por padrão).
- `## Como funciona` — H3s: "Reordering (compilador, CPU, cache store buffers)", "Visibility (sem garantia entre threads sem sincronização)", "Atomicidade (long/double podem ser não-atômicos sem volatile)", "**Happens-before** (a relação fundamental + regras: program order, monitor lock, volatile, thread start/join, final fields)", "**`volatile`** (visibility + ordering; NÃO dá atomicidade composta) — dono do conceito", "Final field semantics (publicação segura de imutáveis)", "Double-checked locking correto (com `volatile`)", "**Safe vs unsafe publication**".
- `## Na prática` — flag de parada com `volatile`; DCL correto de singleton; imutável publicado com segurança via final.
- `## Armadilhas` — ≥3: (1) DCL sem `volatile` (lê objeto parcialmente construído); (2) achar que `volatile` torna `i++` atômico (não — é read-modify-write); (3) publicar `this` no construtor (escape) / ler campo não-final sem sincronização. Cada uma com exemplo (declarar output não-determinístico) + fix.
- `## Em entrevista` — frase 3+ sentenças sobre happens-before/visibility (alto valor); vocabulário 6+ termos.
- `## Veja também` (03, 04, 05, 06, 12, MOC, tronco `[[Java Concurrency]]`, tronco `[[Java Fundamentals]]` (JVM memory — Galho 3 futuro), verbetes `happens-before`/`volatile`/`safe publication (publicação segura)`/`mutual exclusion (exclusão mútua)`) + `## Referências` (JLS §17, *Java Concurrency in Practice* cap. 16).

Tamanho: 400-700 linhas (nota mais teórica do galho; usar opus).

- [ ] **Step 3: Verificar**

```bash
grep -E "happens-before|volatile|reorder|publicação|double-checked" "03-Dominios/Tecnologia/Java/Concorrência e paralelismo/11 - Java Memory Model em profundidade.md" | head
wc -l "03-Dominios/Tecnologia/Java/Concorrência e paralelismo/11 - Java Memory Model em profundidade.md"
```
Expected: cobre happens-before+volatile+safe publication; se `wc -l` > 700, aplicar contingência.

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/Concorrência e paralelismo/11 - Java Memory Model em profundidade.md"
git commit -m "feat(java): galho 4 nota 11 — Java Memory Model em profundidade"
```

---

### Task 12: Nota 12 — Virtual Threads e Project Loom  ⟦opus⟧

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Concorrência e paralelismo/12 - Virtual Threads e Project Loom.md`

- [ ] **Step 1: Pesquisar fonte (usar modelo opus)**

WebFetch JEP 444 (Virtual Threads, GA Java 21) `https://openjdk.org/jeps/444` e `https://docs.oracle.com/en/java/javase/21/core/virtual-threads.html`. Confirmar status GA (21), pinning (synchronized/native), e a recomendação de NÃO fazer pool de virtual threads.

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: magus`, tags `[java, concorrencia, magus, virtual-threads, loom]`, aliases `["Virtual Threads", "Project Loom", "Virtual thread"]`.

Conteúdo (matéria-prima: tronco "## Virtual Threads (Java 21+)"):
- `## O que é` — virtual thread = thread leve gerenciada pela JVM (não 1:1 com OS thread); ressurreição do estilo thread-per-request.
- `## Como funciona` — H3s: "Platform threads (= OS thread) vs virtual threads", "Carrier threads (ForkJoinPool) e mount/unmount em operação bloqueante", "**Pinning** (synchronized block / native call prendem o carrier — armadilha)", "Criação (`Thread.ofVirtual().start()`, `Executors.newVirtualThreadPerTaskExecutor()`)".
- `## Por que importa` / comparação justa — "Quando usar (IO-bound, alta concorrência, thread-per-request) vs quando NÃO (CPU-bound — não acelera; pooling de virtual threads é anti-pattern)"; "Virtual threads vs reactive" (gancho Galho 11 — linkar tronco, não nota inexistente).
- `## Na prática` — servidor thread-per-request com `newVirtualThreadPerTaskExecutor`; substituir `synchronized` por `ReentrantLock` em hot path pra evitar pinning.
- `## Armadilhas` — ≥3: (1) fazer pool/limitar virtual threads (anti-pattern — crie uma por tarefa); (2) `synchronized` em seção que bloqueia (pinning → usar `ReentrantLock`); (3) `ThreadLocal` pesado com milhões de VTs (custo de memória — gancho pro 14 scoped values). Exemplo + fix.
- `## Em entrevista` — frase 3+ sentenças sobre o trade-off virtual vs platform (alto valor); vocabulário 6+ termos.
- `## Veja também` (02, 08, 10, 13, 14, MOC, tronco, `[[Java Fundamentals]]`, verbetes `virtual thread`/`carrier thread`/`pinning`/`thread pool`) + `## Referências` (JEP 444/425).

Tamanho: 400-650 linhas (densa; usar opus).

- [ ] **Step 3: Verificar**

```bash
grep -E "virtual thread|carrier|pinning|ofVirtual|newVirtualThread" "03-Dominios/Tecnologia/Java/Concorrência e paralelismo/12 - Virtual Threads e Project Loom.md" | head
```

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/Concorrência e paralelismo/12 - Virtual Threads e Project Loom.md"
git commit -m "feat(java): galho 4 nota 12 — Virtual Threads e Project Loom"
```

---

### Task 13: Nota 13 — Structured concurrency

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Concorrência e paralelismo/13 - Structured concurrency.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch o JEP de Structured Concurrency (verificar o número do release atual: 453/462/480/499/505) via `https://openjdk.org/jeps/` e `https://dev.java/evolution/`. **Confirmar o release exato em que virou final (Java 25)** vs os preview anteriores. Confirmar a API de `StructuredTaskScope` (pode ter mudado entre previews — usar a forma do release final).

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: magus`, tags `[java, concorrencia, magus, structured-concurrency, loom]`, aliases `["Structured concurrency", "StructuredTaskScope"]`.

Conteúdo (matéria-prima: tronco "## Structured Concurrency"):
- `## O que é` — problema: tasks órfãs, leaks e cancelamento manual com `ExecutorService`; a ideia de que subtarefas formam uma unidade com escopo.
- `## Como funciona` — H3s: "`StructuredTaskScope` e `fork`/`join`", "Policies (`ShutdownOnFailure` = todas ou falha rápida; `ShutdownOnSuccess` = primeira que vence)", "Propagação de erro e cancelamento automático", "Escopo como unidade de trabalho (vs ExecutorService solto)".
- `## Na prática` — buscar user+order em paralelo e falhar rápido se um falhar (ShutdownOnFailure). **Declarar versão/status** (final no Java 25; era preview antes — `--enable-preview`).
- `## Armadilhas` — ≥3: (1) vazar tasks/usar resultado fora do scope (`join` antes de ler); (2) ignorar cancelamento (não checar interrupção em loops longos); (3) misturar com `ExecutorService` manual (perde a estrutura). Exemplo + fix.
- `## Em entrevista` + `## Veja também` (12, 14, 08, MOC, tronco, verbete `structured concurrency`) + `## Referências` (JEP).

Tamanho: 300-460 linhas.

- [ ] **Step 3: Verificar**

```bash
grep -E "StructuredTaskScope|ShutdownOnFailure|fork|join|preview|final" "03-Dominios/Tecnologia/Java/Concorrência e paralelismo/13 - Structured concurrency.md" | head
```

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/Concorrência e paralelismo/13 - Structured concurrency.md"
git commit -m "feat(java): galho 4 nota 13 — structured concurrency"
```

---

### Task 14: Nota 14 — Scoped values

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Concorrência e paralelismo/14 - Scoped values.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch o JEP de Scoped Values (verificar número do release; final no Java 25) via `https://openjdk.org/jeps/` e `https://dev.java/evolution/`. Confirmar a API `ScopedValue.where(...).run(...)` e o status final.

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: magus`, tags `[java, concorrencia, magus, scoped-values, threadlocal]`, aliases `["Scoped values", "ScopedValue"]`.

Conteúdo (matéria-prima: tronco "## Scoped Values (Java 25 final)"):
- `## O que é` — alternativa imutável e com escopo delimitado ao `ThreadLocal`, motivada pela escala de virtual threads.
- `## Como funciona` — H3s: "Problemas do `ThreadLocal`" (lifetime ilimitado, mutável, inheritance caro com milhões de VTs), "`ScopedValue` e `where().run()`" (imutável, escopo dinâmico), "Rebinding", "Herança em forks de structured concurrency".
- `## Na prática` — propagar um request-id por um escopo sem `ThreadLocal`. Tabela "**`ThreadLocal` vs `ScopedValue`**" (mutabilidade, lifetime, custo, herança). **Declarar status** (final Java 25).
- `## Armadilhas` — ≥2: (1) tentar mutar um scoped value (é imutável — use rebinding); (2) ler fora do escopo `run()` (lança exceção); (3) assumir herança automática sem structured concurrency. Exemplo + fix.
- `## Em entrevista` + `## Veja também` (12, 13, MOC, tronco, verbete `scoped value`) + `## Referências` (JEP).

Tamanho: 200-340 linhas (nota mais enxuta do galho — API focada).

- [ ] **Step 3: Verificar**

```bash
grep -E "ScopedValue|ThreadLocal|where|run|rebinding" "03-Dominios/Tecnologia/Java/Concorrência e paralelismo/14 - Scoped values.md" | head
```

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/Concorrência e paralelismo/14 - Scoped values.md"
git commit -m "feat(java): galho 4 nota 14 — scoped values"
```

---

### Task 15: Nota 15 — Parallel streams e fork/join

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Concorrência e paralelismo/15 - Parallel streams e fork-join.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch docs de `ForkJoinPool` e do parallel stream (`https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/ForkJoinPool.html` + tutorial de parallelism). Confirmar work-stealing e o compartilhamento do common pool.

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: magus`, tags `[java, concorrencia, magus, parallel-streams, fork-join]`, aliases `["Parallel streams", "ForkJoinPool", "fork/join"]`.

Conteúdo (matéria-prima: tronco "## ForkJoinPool" + "## Parallel Streams"):
- `## Como funciona` — H3s: "`ForkJoinPool` e work-stealing", "Common pool (compartilhado com parallel streams e CompletableFuture)", "`RecursiveTask`/`RecursiveAction` (fork/join/compute)", "Parallel streams (`.parallel()`) e o spliterator".
- `## Por que importa` / comparação justa — "Quando o paralelismo ganha (CPU-bound, dataset grande, spliterator balanceado, sem ordering) vs quando perde (IO, source mal-particionável como `LinkedList`, lambdas com estado, autoboxing, dataset pequeno)". Liga ao Galho 2 (Stream API base) via tronco — **não re-explica o pipeline**.
- `## Na prática` — soma paralela com `RecursiveTask`; medir parallel vs sequential num caso CPU-bound.
- `## Armadilhas` — ≥3: (1) estado mutável compartilhado em lambda de parallel stream (resultado corrompido); (2) bloquear IO no common pool (satura o pool global); (3) `.parallel()` em dataset pequeno (overhead > ganho). Exemplo + fix.
- `## Em entrevista` + `## Veja também` (08, 10, 16, MOC, tronco, `[[Java Fundamentals]]` (Streams — Galho 2 futuro), verbetes `fork/join`/`work-stealing`) + `## Referências`.

Tamanho: 320-460 linhas.

- [ ] **Step 3: Verificar**

```bash
grep -E "ForkJoinPool|work-stealing|RecursiveTask|parallel|common pool" "03-Dominios/Tecnologia/Java/Concorrência e paralelismo/15 - Parallel streams e fork-join.md" | head
```

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/Concorrência e paralelismo/15 - Parallel streams e fork-join.md"
git commit -m "feat(java): galho 4 nota 15 — parallel streams e fork/join"
```

---

### Task 16: Nota 16 — Padrões e diagnóstico de concorrência

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Concorrência e paralelismo/16 - Padrões e diagnóstico de concorrência.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch sobre análise de thread dump (`https://docs.oracle.com/en/java/javase/21/troubleshoot/`) e JFR/`jcmd`. Confirmar como deadlock aparece num thread dump e os estados BLOCKED/WAITING.

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: magus`, tags `[java, concorrencia, magus, patterns, diagnostico]`, aliases `["Padrões de concorrência", "Diagnóstico de concorrência", "Thread dump"]`.

Conteúdo (matéria-prima: tronco "## Patterns de design concorrente" + "## Debugging e profiling" + "## Armadilhas comuns"):
- `## Como funciona` — H3s: "Patterns: thread-safety por imutabilidade/confinement", "Producer-consumer com `BlockingQueue`", "Thread-local state", "Copy-on-write", "Guarded suspension".
- `## Na prática` (diagnóstico) — "Anatomia de um thread dump" (RUNNABLE/BLOCKED/WAITING; deadlock detectado pela JVM), "JFR + Mission Control", "`jcmd <pid> Thread.print`", "async-profiler para lock contention", "sintomas → causa" (contention, pool subdimensionado, deadlock).
- `## Armadilhas` — ≥3: (1) confiar em `synchronized(this)` exposto (cliente pode lockar o mesmo monitor); (2) diagnosticar contention sem thread dump (chutar); (3) thread pool subdimensionado escondendo deadlock por exaustão. Exemplo + fix.
- `### Cheatsheet` — tabela "qual primitiva para qual problema" (fechamento do galho: synchronized/Lock/atomic/concurrent collection/CompletableFuture/virtual thread).
- `## Em entrevista` + `## Veja também` (03, 04, 08, 11, MOC, tronco, verbetes `contention`/`deadlock`) + `## Referências`.

Tamanho: 320-480 linhas (nota de fechamento).

- [ ] **Step 3: Verificar**

```bash
grep -E "thread dump|BLOCKED|WAITING|JFR|jcmd|Cheatsheet|contention" "03-Dominios/Tecnologia/Java/Concorrência e paralelismo/16 - Padrões e diagnóstico de concorrência.md" | head
```

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/Concorrência e paralelismo/16 - Padrões e diagnóstico de concorrência.md"
git commit -m "feat(java): galho 4 nota 16 — padrões e diagnóstico de concorrência"
```

---

## Task 17: MOC do galho

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index.md`

- [ ] **Step 1: Escrever o MOC**

Frontmatter: `type: moc`, `status: growing`, `publish: true`, `title: "Concorrência e paralelismo"`, tags `[java, concorrencia, moc]`, aliases `["Concorrência Java", "Galho 4 - Concorrência"]`, `created`/`updated: 2026-06-03`.

Conteúdo (modelar pelo `03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/index.md`):
- `> [!abstract] TL;DR` — Galho 4 da trilha Java Senior; concorrência do Java moderno, das threads e JMM aos executors, CompletableFuture, virtual threads/Loom e structured concurrency.
- `## Sobre este galho` — escopo + audiência primária (senior em prep de entrevista) + secundária (decisões de design + troubleshooting de produção).
- `## Iniciado` — wikilinks 01-04 (uma linha descritiva cada).
- `## Adepto` — wikilinks 05-10.
- `## Magus` — wikilinks 11-16.
- `## Rotas alternativas` — 5 rotas:
  - **Completa** — 01 → 16.
  - **Entrevista internacional** — 01 → 03 → 11 → 08 → 12 → 13.
  - **Java moderno / Loom** — 01 → 02 → 08 → 12 → 13 → 14.
  - **Troubleshooting de produção** — 04 → 11 → 16 → 08.
  - **Lock-free / performance** — 06 → 11 → 05 → 15.
- `## Todas as notas` — bloco Dataview:

````markdown
```dataview
TABLE fase, status, updated
FROM "03-Dominios/Tecnologia/Java/Concorrência e paralelismo"
WHERE type = "concept"
SORT file.name ASC
```
````

- `## Veja também` — `[[03-Dominios/Tecnologia/Java/index|Java (MOC central)]]`, `[[Java Concurrency]]` (tronco), `[[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/index|Linguagem e sintaxe moderna (Galho 1)]]`, `[[03-Dominios/Tecnologia/Java/Dicionário de Java|Dicionário de Java]]`. Galhos 3 (JVM) e 11 (Reativa) como texto "(planejado)", SEM wikilink.

- [ ] **Step 2: Verificar**

```bash
grep -cE "^## (Iniciado|Adepto|Magus|Rotas alternativas)" "03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index.md"
grep -c "\[\[" "03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index.md"
```
Expected: 4 headings de seção; ≥16 wikilinks (uma por nota + Veja também).

- [ ] **Step 3: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index.md"
git commit -m "feat(java): galho 4 MOC — concorrência e paralelismo"
```

---

## Task 18: Expandir o Dicionário de Java (NÃO recriar)

**Files:**
- Modify: `03-Dominios/Tecnologia/Java/Dicionário de Java.md`

- [ ] **Step 1: Reler o Dicionário existente**

Ler `03-Dominios/Tecnologia/Java/Dicionário de Java.md` inteiro. Mapear as seções alfabéticas existentes (`## A`..`## Y`) e os verbetes já presentes (do Galho 1). **NÃO recriar o arquivo; NÃO reordenar verbetes existentes.** Confirmar o formato de verbete (`### Termo` + definição 1-3 linhas + `Veja também: [[nota]].`).

- [ ] **Step 2: Inserir os verbetes de concorrência em ordem alfabética**

Inserir os ~28-32 verbetes abaixo na seção alfabética correta (criar seções novas `## H`, `## M`, `## N`, `## Q` etc. se não existirem; ordenação case-insensitive, sem acento). Cada verbete: definição curta + `Veja também:` pra nota canônica do galho.

| Verbete | Seção | Nota canônica |
|---|---|---|
| ABA problem | A | →06 |
| atomic (variável atômica) | A | →06 |
| barrier (CyclicBarrier) | B | →09 |
| BlockingQueue | B | →07 |
| carrier thread | C | →12 |
| CAS (compare-and-swap) | C | →06 |
| CompletableFuture | C | →10 |
| ConcurrentHashMap | C | →07 |
| condição de corrida (race condition) | C | →04 |
| contention | C | →04/16 |
| deadlock | D | →04 |
| Executor / ExecutorService | E | →08 |
| fork/join | F | →15 |
| Future | F | →08 |
| happens-before | H | →11 |
| latch (CountDownLatch) | L | →09 |
| livelock | L | →04 |
| lock-free | L | →06 |
| monitor (intrinsic lock) | M | →03 |
| mutual exclusion (exclusão mútua) | M | →03 |
| pinning | P | →12 |
| safe publication (publicação segura) | S | →11 |
| scoped value | S | →14 |
| semaphore (semáforo) | S | →09 |
| starvation | S | →04 |
| structured concurrency | S | →13 |
| synchronized | S | →03 |
| thread pool | T | →08 |
| virtual thread | V | →12 |
| volatile | V | →11 |
| work-stealing | W | →15 |

Atualizar frontmatter `updated: 2026-06-03`.

- [ ] **Step 3: Verificar**

```bash
grep -E "^### (happens-before|virtual thread|volatile|deadlock|CAS|pinning)" "03-Dominios/Tecnologia/Java/Dicionário de Java.md"
grep -cE "^### " "03-Dominios/Tecnologia/Java/Dicionário de Java.md"
```
Expected: verbetes de concorrência presentes; contagem total de `###` subiu ~28-32 vs o baseline do Galho 1 (~30 → ~58-62). Verbetes do Galho 1 intactos.

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/Dicionário de Java.md"
git commit -m "feat(java): expande Dicionário de Java com verbetes de concorrência (galho 4)"
```

---

## Task 19: Ativar o Galho 4 no MOC central `Java/index.md`

**Files:**
- Modify: `03-Dominios/Tecnologia/Java/index.md`

- [ ] **Step 1: Trocar a linha do Galho 4 por wikilink ativo**

Substituir a linha 28 (atualmente `4. Concorrência e paralelismo *(planejado)* — Memory Model, locks, executors, CompletableFuture, Virtual Threads/Loom, structured concurrency`) por:

```markdown
4. [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Concorrência e paralelismo]] — Memory Model, locks, atomics, executors, CompletableFuture, Virtual Threads/Loom, structured concurrency
```

Atualizar `updated: 2026-06-03`. **Não mexer no resto do MOC** (galhos 2/3 e 5-18 permanecem como texto "(planejado)").

- [ ] **Step 2: Verificar**

```bash
grep -E "Concorrência e paralelismo/index" "03-Dominios/Tecnologia/Java/index.md"
grep -E "updated: 2026-06-03" "03-Dominios/Tecnologia/Java/index.md"
```
Expected: wikilink ativo do Galho 4; `updated` atualizado.

- [ ] **Step 3: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/index.md"
git commit -m "feat(java): ativa Galho 4 (Concorrência) no MOC central"
```

---

## Task 20: Poda integral do tronco `Java Concurrency.md`

**Files:**
- Modify: `03-Dominios/Tecnologia/Java/Core/Java Concurrency.md`

- [ ] **Step 1: Reler o tronco e confirmar headings (usar notas do Task 0)**

Confirmar os ranges reais de cada seção a podar.

- [ ] **Step 2: Podar TODAS as seções conceituais (substituir corpo por callout)**

Como o galho é **dono integral**, substituir o corpo de cada seção conceitual por callout (manter o heading H2), apontando pra(s) nota(s) destino segundo o mapa do §6 do spec:

```markdown
> [!nota] Migrado para galho próprio
> Este tópico foi expandido no galho [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Concorrência e paralelismo]]. Veja [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/<nota canônica>|<título>]].
```

Mapa de poda (seção do tronco → nota destino):
- "Threads na JVM" → 01, 02
- "Java Memory Model (JMM)" + "Final fields" → 11
- "Synchronized" → 03
- "java.util.concurrent.locks" → 05
- "Atomic classes" → 06
- "Concurrent Collections" → 07
- "ExecutorService e Thread Pools" → 08
- "CompletableFuture" → 10
- "Sincronizadores" → 09
- "ForkJoinPool" + "Parallel Streams" → 15
- "Virtual Threads" → 12
- "Structured Concurrency" → 13
- "Scoped Values" → 14
- "Deadlock, Race Condition e companhia" → 04, 11
- "Patterns de design concorrente" + "Debugging e profiling" + "Armadilhas comuns" → 16

- [ ] **Step 3: Migrar e podar as seções de inglês**

A seção `## How to explain in English` + `### Key vocabulary` tem conteúdo útil — o material já foi incorporado nas seções "Em entrevista" das notas (Tasks 1-16). Substituir por callout apontando pro MOC do galho (as notas têm o vocabulário). Não duplicar.

- [ ] **Step 4: Higienizar a fabricação**

Localizar `## Na prática (da minha experiência)` (≈ linha 1441) e reescrever como padrão neutro OU remover a atribuição pessoal (**regra inegociável** [[feedback_no_fabrication]]). Varrer o resto do tronco por 1ª pessoa ("eu", "meu", "na minha", "já vi", "no meu") e neutralizar.

- [ ] **Step 5: Reduzir o tronco a redirect enxuto + atualizar frontmatter**

Manter header + TL;DR (apontando pro galho) + os callouts por seção + "Veja também" com `[[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Concorrência e paralelismo (galho)]]`. Atualizar `updated: 2026-06-03`. Manter `publish: false`. NÃO apagar o arquivo (histórico + wikilinks).

- [ ] **Step 6: Verificar**

```bash
grep -c "Migrado para galho próprio" "03-Dominios/Tecnologia/Java/Core/Java Concurrency.md"
grep -iE "da minha experiência|na minha experiência|no meu projeto" "03-Dominios/Tecnologia/Java/Core/Java Concurrency.md"
```
Expected: ≥12 callouts de migração; ZERO ocorrências de "minha experiência"/"meu projeto".

- [ ] **Step 7: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/Core/Java Concurrency.md"
git commit -m "refactor(java): poda integral de Java Concurrency (migra p/ galho 4) + higieniza fabricação"
```

---

## Task 21: Verificação final do galho

**Files:** (somente leitura/verificação)

- [ ] **Step 1: Conferir as 16 notas + MOC presentes**

```bash
ls "03-Dominios/Tecnologia/Java/Concorrência e paralelismo/" | sort
```
Expected: 01..16 + index.md (17 arquivos .md).

- [ ] **Step 2: Conferir frontmatter `fase` e distribuição**

```bash
for f in "03-Dominios/Tecnologia/Java/Concorrência e paralelismo/"[0-9]*.md; do grep -H "^fase:" "$f"; done
```
Expected: toda nota 01-16 tem `fase:`; distribuição 4 iniciado / 6 adepto / 6 magus.

- [ ] **Step 3: Conferir seções obrigatórias em todas as notas**

```bash
for f in "03-Dominios/Tecnologia/Java/Concorrência e paralelismo/"[0-9]*.md; do
  echo "$f: $(grep -cE '^## (Em entrevista|Armadilhas|Veja também)' "$f")"
done
```
Expected: cada nota retorna 3 (tem "Em entrevista", "Armadilhas", "Veja também").

- [ ] **Step 4: Rodar a skill de wikilinks**

Invocar a skill `verificar-wikilinks` na pasta `03-Dominios/Tecnologia/Java/Concorrência e paralelismo/` + `03-Dominios/Tecnologia/Java/index.md` + `03-Dominios/Tecnologia/Java/Dicionário de Java.md`. Corrigir quebrados (folder-links exigem index.md — regra Quartz). **Lembrar:** o checker dá falso-positivo em self-anchors `[[#Heading]]` — as notas evitam âncoras same-file; ignorar esse falso-positivo. Se houver correções, commitar à parte.

- [ ] **Step 5: Build Quartz (se disponível)**

Confirmar publicação sem erro conforme o pipeline do projeto (deploy cross-repo é manual do usuário — NÃO fazer push/deploy). Se o build não rodar localmente, registrar como verificação manual pendente.

- [ ] **Step 6: Resumo de fechamento (sem commit)**

Reportar ao usuário: notas criadas, distribuição de fases, verbetes adicionados, estado da poda, e qualquer falso-positivo de wikilink ignorado. Branch `java-galho-04-concorrencia` pronta para review/merge manual (sem push).

---

## Self-Review (preenchido na escrita do plano)

**Spec coverage:** as 16 notas (Tasks 1-16) cobrem o §3.1 do spec; MOC (17) cobre §3.2; Dicionário expandido (18) cobre §3.3; MOC central (19) cobre §3.4; poda integral (20) cobre §3.5/§6; verificação (21) cobre §7. Todas as seções do spec mapeadas. Fronteiras (§3.1 "decisões de fronteira") respeitadas: links pra galhos inexistentes (2/3/11) vão pro tronco; virtual threads é dono na nota 12; volatile na 11.

**Placeholder scan:** sem TBD/TODO. Conteúdo por nota especificado com seções concretas, fontes WebFetch nomeadas (JEPs com URL), armadilhas mínimas e tamanho-alvo.

**Type/naming consistency:** numeração 01-16 consistente entre tasks, MOC (rotas alternativas), Dicionário (notas canônicas) e poda (mapa §6). Distribuição 4/6/6 consistente no header, nas fases das tasks e na verificação (Task 21 Step 2). Notas opus (11, 12) marcadas ⟦opus⟧ e com Step 1 indicando o modelo. Contingência de divisão da nota 11 documentada com efeito na renumeração. Nomes de arquivo sem `:` (usado `-` em "01 - Concorrência e paralelismo - o modelo") pra evitar problema de filesystem.
