---
title: "Spec — Galho 4 da trilha Java Senior (Concorrência e paralelismo)"
date: 2026-06-03
author: Josenaldo
status: draft
type: spec
publish: false
---

# Spec — Galho 4 da trilha Java Senior (Concorrência e paralelismo)

## 1. Contexto e motivação

Este é o **quarto galho** da trilha Java Senior (roadmap em `docs/superpowers/specs/2026-06-02-java-senior-roadmap-design.md`). Pressupõe leitura do roadmap, que estabelece topologia flat, esquema de 3 fases, padrões editoriais e política de poda. O Galho 1 (`2026-06-02-java-galho-01-linguagem-design.md`) já fechou e mergeou em `main` — seus artefatos (15 notas + MOC + Dicionário) são o **template de padrão e qualidade** deste galho.

O galho refatora o tronco `03-Dominios/Tecnologia/Java/Core/Java Concurrency.md` (1579 linhas, `publish: false`, `status: evergreen`). Diferença estrutural em relação ao Galho 1: enquanto `Java Fundamentals` alimenta quatro galhos (1, 2, 3, 4) e sofreu poda **parcial**, o tronco `Java Concurrency` é **integralmente** do Galho 4 — todo o seu conteúdo migra. A poda aqui é **total**: cada seção do tronco vira callout apontando pra nota do galho (ver §6).

Concorrência é um dos temas de **mais alto valor de entrevista internacional** e um dos mais densos da plataforma: Java Memory Model, virtual threads (Project Loom) e structured concurrency são tópicos quentes em 2024-2026. Por isso o galho adota **16 notas com Magus pesado** (distribuição 4/6/6), explicitamente autorizado pelo roadmap (§7.2: "Magus pode crescer em galhos complexos como Concorrência, JVM, Reativa").

**Atenção à fabricação:** o tronco tem uma seção `## Na prática (da minha experiência)` (linha 1441). Nenhuma nota nova pode herdar atribuição de experiência pessoal — exemplos são neutros (`Order`, `Customer`) ou hipotéticos explícitos. A poda do tronco (§6) higieniza essa seção (regra inegociável [[feedback_no_fabrication]]).

**Atenção a versões:** virtual threads (GA Java 21), structured concurrency e scoped values (preview por vários releases, final em Java 25) são version-specific e exigem **verificação via JEP/doc oficial (WebFetch obrigatório)** antes de afirmar status GA/preview — nunca inventar.

## 2. Objetivo

Produzir, em uma sessão de execução dedicada, **16 notas atômicas + 1 MOC do galho + expansão do Dicionário de Java + poda do tronco + ativação do MOC central**, em `03-Dominios/Tecnologia/Java/Concorrência e paralelismo/` e `03-Dominios/Tecnologia/Java/`, todas `publish: true`, em PT-BR, distribuídas em 3 fases (4 Iniciado + 6 Adepto + 6 Magus).

Ao terminar o galho, o leitor deve conseguir:

- **Explicar em inglês** o modelo de memória do Java, a diferença entre platform e virtual threads, e o trade-off de cada primitiva de sincronização.
- **Escolher e justificar** a primitiva certa (synchronized vs Lock vs atomic vs concurrent collection vs CompletableFuture vs virtual thread) para um cenário dado.
- **Reconhecer e diagnosticar** race conditions, deadlocks, visibility bugs e contention em code review e em produção (thread dump, JFR).
- **Decidir** quando usar paralelismo (parallel streams / fork-join) e quando ele perde para sequencial.

A barra é "decidir, justificar, reconhecer patterns e armadilhas em code review e diagnosticar produção" — não "implementar um scheduler from scratch".

## 3. Saídas concretas

### 3.1. Notas (`03-Dominios/Tecnologia/Java/Concorrência e paralelismo/`)

Pasta nova, flat. 16 notas + 1 MOC. Numeração global por galho (não reinicia por fase).

#### Iniciado (4 notas — vocabulário + modelo mental)

| # | Nota | Escopo nuclear |
|---|------|----------------|
| 01 | Concorrência e paralelismo: o modelo | Concorrência vs paralelismo, threads vs processos, modelo de memória compartilhada, por que concorrência é difícil (teaser atomicidade/visibilidade/ordenação), landscape moderno (platform vs virtual threads como marco). Porta de entrada da trilha de concorrência. |
| 02 | Threads e seu ciclo de vida | `Thread`/`Runnable`, estados (NEW→RUNNABLE→BLOCKED/WAITING/TIMED_WAITING→TERMINATED), `start`/`join`/`interrupt`/`sleep`/`yield`, daemon threads, prioridades, ler um thread dump (intro). |
| 03 | Exclusão mútua com `synchronized` | Race condition na prática, mutual exclusion, intrinsic lock/monitor, `synchronized` em methods/blocks/static, reentrância, `wait`/`notify`/`notifyAll` e o loop de guarda, anti-patterns básicos (lock em `String`/`Integer`, escopo amplo demais). |
| 04 | As armadilhas: race, deadlock e companhia | Panorama: race condition (check-then-act, read-modify-write), deadlock (4 condições de Coffman) e como evitar (ordenação de locks), livelock, starvation, fairness. Teaser de visibility/publication bugs apontando pro JMM (nota 11). |

#### Adepto (6 notas — domínio operacional)

| # | Nota | Escopo nuclear |
|---|------|----------------|
| 05 | Locks explícitos (`java.util.concurrent.locks`) | `ReentrantLock` (tryLock, fairness, lockInterruptibly), `ReadWriteLock`, `StampedLock` (optimistic read), `Condition` (vs wait/notify). `synchronized` vs `Lock`: quando cada um vence. |
| 06 | Atômicos e operações lock-free | `AtomicInteger`/`Long`/`Reference`, CAS e `compareAndSet`, `getAndUpdate`/`accumulateAndGet`, `LongAdder`/`DoubleAdder` (alta contention), `AtomicStampedReference` (problema ABA). Liga ao JMM (11). |
| 07 | Concurrent collections | `ConcurrentHashMap` (operações atômicas, `computeIfAbsent`), `CopyOnWriteArrayList`/`Set`, `BlockingQueue` (Array/Linked, produtor-consumidor), `ConcurrentLinkedQueue`, `ConcurrentSkipListMap`/`Set`; árvore de decisão. Liga ao Galho 2 (Collections) — não re-explica o framework base. |
| 08 | Executors e thread pools | `Executor`/`ExecutorService`, factory methods e seus perigos (`newFixedThreadPool` vs `newCachedThreadPool`), `ThreadPoolExecutor` (core/max/keep-alive/queue/rejection policy), `Future`, `submit`/`invokeAll`/`invokeAny`, shutdown gracioso, dimensionar pool (CPU- vs IO-bound). |
| 09 | Sincronizadores | `CountDownLatch` (one-shot), `CyclicBarrier` (reutilizável + barrier action), `Semaphore` (permits, bounded), `Phaser` (dinâmico), `Exchanger`. Tabela de quando usar cada um; latch vs barrier. |
| 10 | `CompletableFuture` e composição assíncrona | Criação (`supplyAsync`/`runAsync`), transformação (`thenApply`/`thenAccept`/`thenCompose`), combinação (`thenCombine`/`allOf`/`anyOf`), error handling (`exceptionally`/`handle`/`whenComplete`), timeout (`orTimeout`/`completeOnTimeout`, Java 9+), async vs sync variants e qual executor. |

#### Magus (6 notas — maestria + decisões de arquitetura)

| # | Nota | Escopo nuclear |
|---|------|----------------|
| 11 | Java Memory Model em profundidade *(opus)* | Reordering (compiler/CPU), visibility, atomicidade; **happens-before** (a relação fundamental); `volatile` (semântica completa — **dono do conceito**); final field semantics; double-checked locking (a forma correta); **safe publication** (unsafe publication bugs). |
| 12 | Virtual Threads e Project Loom *(opus)* | Platform vs virtual threads, carrier threads, mounting/unmounting, **pinning** (synchronized/native — armadilha), quando usar (IO-bound) vs quando não (CPU-bound/pooling), revival do thread-per-request, `Thread.ofVirtual`/`Executors.newVirtualThreadPerTaskExecutor`, migração. **Dono do conceito** (Galho 1 nota 15 e futuro Galho 11 linkam). Status GA Java 21 verificado via JEP 444. |
| 13 | Structured concurrency | `StructuredTaskScope`, joiners/policies (ShutdownOnFailure/ShutdownOnSuccess), propagação de erro e cancelamento, hierarquia de tasks vs `ExecutorService`. Status (preview por vários releases → final Java 25) **verificado via JEP** (453/462/.../505 conforme release). |
| 14 | Scoped values | `ScopedValue.where().run()`, rebinding, herança em forks de structured concurrency, imutabilidade; **ThreadLocal vs ScopedValue** (lifetime ilimitado, mutabilidade, custo de inheritance com milhões de virtual threads). Status final Java 25 **verificado via JEP**. |
| 15 | Parallel streams e fork/join | `ForkJoinPool`, work-stealing, common pool e seu compartilhamento, `RecursiveTask`/`RecursiveAction`, parallel streams (quando ganha: CPU-bound + dados grandes + spliterator eficiente; quando perde: IO, ordering, boxing, source mal-particionável), armadilhas (estado compartilhado, common pool saturado). Liga ao Galho 2 — não re-explica a Stream API. |
| 16 | Padrões e diagnóstico de concorrência | Design patterns (thread-safety por imutabilidade, producer-consumer, thread-local state, copy-on-write, confinement) + diagnóstico (anatomia de um thread dump: BLOCKED/WAITING/deadlock; JFR; `jcmd`; async-profiler; sintomas de contention). Nota de fechamento/cheatsheet. |

**Decisões de fronteira (escopo NÃO coberto aqui ou de outro dono):**
- **JVM memory (heap/stack/metaspace, GC, JIT)** → Galho 3 (ainda não construído). A nota 11 (JMM) trata do *modelo de memória de concorrência* (happens-before/visibility), não da *organização física de memória da JVM*; linka pro **tronco `Java Fundamentals` (seção JVM)** em vez de notas inexistentes do Galho 3, pra não gerar wikilink quebrado.
- **Virtual Threads** → Galho 4 é **dono** (nota 12). Galho 1 (nota 15) cita como marco; futuro Galho 11 (Reativa) compara com reactive. Eles linkam pra cá.
- **Parallel streams / Stream API** → o pipeline de streams é do Galho 2 (ainda não construído). A nota 15 cobre *o paralelismo* (fork/join, quando paralelizar), linkando pro tronco `Java Fundamentals` (seção Streams) em vez de notas inexistentes do Galho 2.
- **`volatile`** vive na nota 11 (só faz sentido com visibility/ordering). Notas Iniciado/Adepto citam e apontam pra lá.
- **Reactive (Reactor/WebFlux)** → Galho 11. A nota 12 faz só a comparação virtual threads vs reactive, sem ensinar reativo.

### 3.2. MOC do galho

`03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index.md`:
- `type: moc`, `status: growing`
- Frontmatter padrão (`title: "Concorrência e paralelismo"`, tags `java`/`concorrencia`/`moc`, aliases `["Concorrência Java", "Galho 4 - Concorrência"]`)
- TL;DR callout (galho cobre concorrência do Java moderno, das threads ao JMM, executors, CompletableFuture, virtual threads/Loom e structured concurrency)
- "Sobre este galho" + audiência primária/secundária
- Conteúdo agrupado em 3 H2 (`## Iniciado` / `## Adepto` / `## Magus`) com wikilinks pras 16 notas (uma linha descritiva cada, no padrão do MOC do Galho 1)
- **Rotas alternativas (5):**
  - **Completa** — 01 → 16 em ordem
  - **Entrevista internacional** — 01 → 03 → 11 → 08 → 12 → 13 (race/JMM, executors, virtual threads, structured concurrency — o que mais cai)
  - **Java moderno / Loom** — 01 → 02 → 08 → 12 → 13 → 14 (virtual threads + structured concurrency + scoped values)
  - **Troubleshooting de produção** — 04 → 11 → 16 → 08 (deadlock/contention, visibility, diagnóstico, pool sizing)
  - **Lock-free / performance** — 06 → 11 → 05 → 15 (atomics, JMM, locks finos, paralelismo)
- "Veja também": tronco `[[Java Concurrency]]`, MOC central, Galho 1 (Linguagem), Galho 3 (JVM, planejado), Galho 11 (Reativa, planejado), Dicionário de Java
- Dataview "Todas as notas do galho"

### 3.3. Dicionário de Java (EXPANSÃO — não recriar)

`03-Dominios/Tecnologia/Java/Dicionário de Java.md` já existe (criado no Galho 1, `type: glossary`, 223 linhas, seções alfabéticas `## A`..`## Y`). Este galho **expande** o arquivo existente inserindo os verbetes de concorrência **em ordem alfabética case-insensitive (sem acento)** nas seções apropriadas, criando seções novas (`## H`, `## M`, `## N`, `## Q`, etc.) quando necessário. **Nunca recriar o arquivo nem reordenar verbetes existentes.** Atualizar `updated: 2026-06-03` no frontmatter.

Verbetes a inserir (~28-32):

`ABA problem`, `atomic (variável atômica)`, `backpressure` (menção breve, dono é Galho 11), `barrier (CyclicBarrier)`, `BlockingQueue`, `carrier thread`, `CAS (compare-and-swap)`, `CompletableFuture`, `ConcurrentHashMap`, `condição de corrida (race condition)`, `contention`, `deadlock`, `Executor / ExecutorService`, `fork/join`, `Future`, `happens-before`, `latch (CountDownLatch)`, `livelock`, `lock-free`, `mutual exclusion (exclusão mútua)`, `monitor (intrinsic lock)`, `pinning`, `safe publication (publicação segura)`, `scoped value`, `semaphore (semáforo)`, `starvation`, `structured concurrency`, `synchronized`, `thread pool`, `virtual thread`, `volatile`, `work-stealing`.

Cada verbete: definição curta (1-3 linhas) em PT-BR + `Veja também:` apontando pra(s) nota(s) canônica(s) do galho.

### 3.4. MOC central (ativação do Galho 4)

`03-Dominios/Tecnologia/Java/index.md` já existe e lista os 18 galhos. Task **mínima**: trocar a linha 28 (atualmente `4. Concorrência e paralelismo *(planejado)* — ...`) por um wikilink ativo no padrão da linha 25 do Galho 1:

```markdown
4. [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Concorrência e paralelismo]] — Memory Model, locks, atomics, executors, CompletableFuture, Virtual Threads/Loom, structured concurrency
```

Atualizar `updated: 2026-06-03`. Não mexer no resto do MOC central.

### 3.5. Poda do tronco

`03-Dominios/Tecnologia/Java/Core/Java Concurrency.md` — poda **integral** (todo o conteúdo migra). Ver §6.

## 4. Convenções por nota

Herda §7 do roadmap e §4 do spec do Galho 1. Reforços específicos:

### 4.1. Frontmatter

```yaml
---
title: "<título>"
created: 2026-06-03
updated: 2026-06-03
type: concept
status: seedling
publish: true
fase: iniciado | adepto | magus
tags:
  - java
  - concorrencia
  - <fase>
  - <tags específicas: threads, locks, jmm, executors, virtual-threads, structured-concurrency, atomics, deadlock>
aliases:
  - <aliases opcionais>
---
```

### 4.2. Estrutura H2 obrigatória

- `> [!abstract] TL;DR` (callout, NÃO H2)
- `## O que é` / `## Por que importa` / `## Como funciona` (≥3 subseções em notas Adepto/Magus)
- `## Na prática` — exemplos compiláveis, framing neutro ("padrão observado no JDK/Spring", "caso típico em serviço enterprise"); NUNCA "no meu projeto"
- `## Armadilhas` — **≥2** (Iniciado) / **≥3** (Adepto/Magus), cada uma com descrição + exemplo curto de código demonstrando o problema + fix em 1 linha
- `## Em entrevista` — frase pronta em inglês com **3+ sentenças** (trade-off + decisão + caveat) + vocabulário **6+ termos PT→EN**
- `## Veja também` — wikilinks SEM backticks; sempre inclui notas relacionadas do galho + `[[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|MOC do galho]]` + `[[03-Dominios/Tecnologia/Java/index|Trilha Java]]` + tronco `[[Java Concurrency]]` + verbetes do Dicionário
- `## Referências` — docs oficiais (dev.java, docs.oracle.com), JEPs relevantes, *Java Concurrency in Practice* (Goetz), talks identificadas

### 4.3. Restrições absolutas

1. **Sem fabricação** de experiência pessoal. Exemplos neutros (`Order`, `Customer`, `account`) ou hipotéticos explícitos (`// hipotético: ...`). NUNCA `josenaldo` nem casos vividos.
2. **Sem invenção** de APIs/features/versões. Features version-specific (virtual threads GA 21, structured concurrency, scoped values, StampedLock, LongAdder) verificadas via doc oficial/JEP — **WebFetch obrigatório no Step 1 das notas 11-14** e de qualquer feature recente.
3. **Code samples compiláveis** — Java válido; preferir snippets testáveis em jshell/JBang quando possível. Concorrência é difícil de demonstrar deterministicamente: ao mostrar um bug de visibilidade/race, deixar explícito que o output é não-determinístico.
4. **Comparações justas** — ao comparar (synchronized vs Lock, virtual vs platform threads, parallel vs sequential stream, ThreadLocal vs ScopedValue, atomic vs lock), incluir "quando X vence" E "quando Y vence". Sem dogma (especialmente "virtual threads não substituem tudo").
5. **Versões hedged** — "virtual threads são GA no Java 21 (JEP 444); structured concurrency e scoped values eram preview e tornaram-se final no Java 25 — verifique sua versão" em vez de afirmar GA precipitada.
6. **Wikilinks sem backticks** em "Veja também"; tronco + MOC do galho + MOC central obrigatórios. Não linkar notas de galhos inexistentes (3, 2, 11) — linkar o tronco correspondente.
7. **Code fences corretos:** ` ```java ` pra código, ` ```text ` pra output/thread dump/erros. Sempre fechadas.
8. **`fase:` no frontmatter + na tag** — obrigatório.
9. **Higiene de commits** — sem `Co-Authored-By: Claude`, sem `--no-verify`, `git add <path>` nominal, 1 commit por nota.
10. **Tom pedagógico graduado** — Iniciado assume pouco; Magus assume domínio dos anteriores e dos Galhos 1.

## 5. Conteúdo por nota (síntese)

Esboço do recorte. O tronco `Java Concurrency` é matéria-prima (refatorar/expandir, não copiar 1:1); features recentes exigem verificação via doc oficial/JEP. Mapeamento tronco→nota indicado.

- **01 — Concorrência e paralelismo: o modelo.** Concorrência (lidar com muitas coisas) vs paralelismo (fazer muitas ao mesmo tempo), processos vs threads, modelo de memória compartilhada vs message-passing, os 3 problemas (atomicidade, visibilidade, ordenação) como teaser, landscape (platform threads desde sempre, virtual threads como salto). Armadilhas: confundir concorrência com paralelismo; achar que "mais threads = mais rápido". Tronco: "O que é" + intro de "Threads na JVM".
- **02 — Threads e ciclo de vida.** `Thread` vs `Runnable`, `start` vs `run`, estados e transições, `join`/`interrupt`/`sleep`/`yield`, daemon vs user threads, `InterruptedException` e a política de interrupção, ler thread dump. Armadilhas: chamar `run()` direto; engolir `InterruptedException`; `Thread.stop()` (deprecado). Tronco: "Threads na JVM" (Platform Threads, Estados, Thread dump).
- **03 — Exclusão mútua com synchronized.** Race condition concreta (contador), mutual exclusion, monitor/intrinsic lock, synchronized methods/blocks/static, reentrância, wait/notify/notifyAll + loop de guarda (`while`, não `if`). Armadilhas: lock em objeto mutável/`String`/`Integer` cacheado; `if` em vez de `while` no wait; synchronized amplo demais (contention). Tronco: "Synchronized" (todas as subseções, incl. wait/notify, anti-patterns).
- **04 — Armadilhas: race, deadlock e companhia.** Race (check-then-act, read-modify-write), deadlock + 4 condições de Coffman + prevenção (lock ordering, tryLock com timeout), livelock, starvation, fairness. Visibility/publication bugs introduzidos como fenômeno, deep no 11. Armadilhas: ordem de aquisição de locks inconsistente; deadlock com locks aninhados; "funciona na minha máquina" (race latente). Tronco: "Deadlock, Race Condition e companhia".
- **05 — Locks explícitos.** `Lock`/`ReentrantLock` (tryLock, timeout, fairness, lockInterruptibly), padrão `lock()`/`try`/`finally unlock()`, `ReadWriteLock` (muitos leitores/poucos escritores), `StampedLock` (optimistic read, não-reentrante), `Condition`. synchronized vs Lock. Armadilhas: esquecer `unlock()` no finally; StampedLock reentrante (não é); fairness matando throughput. Tronco: "java.util.concurrent.locks".
- **06 — Atômicos e lock-free.** `Atomic*`, CAS (hardware), `compareAndSet`, `getAndIncrement`/`updateAndGet`/`accumulateAndGet`, `LongAdder`/`DoubleAdder` (striping sob contention), `AtomicStampedReference`/`AtomicMarkableReference` (ABA). Armadilhas: loop CAS sem limite (livelock sob contention); ABA com `AtomicReference`; `LongAdder.sum()` não é instantâneo-consistente. Tronco: "Atomic classes".
- **07 — Concurrent collections.** `ConcurrentHashMap` (lock striping, `computeIfAbsent`/`merge` atômicos, `size()` aproximado), `CopyOnWriteArrayList`/`Set` (read-heavy), `BlockingQueue` (`ArrayBlockingQueue`/`LinkedBlockingQueue`, put/take, producer-consumer), `ConcurrentLinkedQueue` (não-bloqueante), `ConcurrentSkipListMap`/`Set` (ordenado). Árvore de decisão. Armadilhas: `Collections.synchronizedMap` + iteração não-atômica; compound ops em ConcurrentHashMap; CopyOnWrite em write-heavy. Tronco: "Concurrent Collections". Liga ao Galho 2.
- **08 — Executors e thread pools.** `Executor`/`ExecutorService`/`ScheduledExecutorService`, factory methods e armadilhas (`newCachedThreadPool` unbounded, `newFixedThreadPool` queue unbounded), `ThreadPoolExecutor` (core/max/keepAlive/workQueue/handler), `Future`, `submit`/`invokeAll`/`invokeAny`, `shutdown` vs `shutdownNow` + `awaitTermination`, dimensionamento (CPU-bound ≈ N+1, IO-bound maior; fórmula de Little). Armadilhas: não fazer shutdown (leak); pool ilimitado (OOM); engolir exceção de task em `execute`. Tronco: "ExecutorService e Thread Pools", "ForkJoinPool" (intro; deep no 15).
- **09 — Sincronizadores.** `CountDownLatch` (one-shot, espera N eventos), `CyclicBarrier` (reutilizável, N threads se esperam, barrier action), `Semaphore` (N permits, bounded resource), `Phaser` (fases dinâmicas), `Exchanger` (troca entre 2). Latch vs barrier (one-shot vs cíclico). Armadilhas: reusar CountDownLatch (não dá); barrier com thread que morre (BrokenBarrierException); semaphore sem release no finally. Tronco: "Sincronizadores".
- **10 — CompletableFuture.** `supplyAsync`/`runAsync`, `thenApply`/`thenAccept`/`thenRun`, `thenCompose` (flatMap) vs `thenApply` (map), `thenCombine`/`allOf`/`anyOf`, `exceptionally`/`handle`/`whenComplete`, `orTimeout`/`completeOnTimeout` (Java 9+), async variants e o executor default (common pool). Armadilhas: bloquear no common pool; `get()` sem timeout; perder exceção sem `handle`/`exceptionally`. Tronco: "CompletableFuture".
- **11 — Java Memory Model (opus).** Reordering (compilador/CPU/cache), visibility (sem garantia entre threads), atomicidade (long/double sem volatile), **happens-before** e suas regras (program order, monitor, volatile, thread start/join, final), `volatile` (visibility + ordering, não atomicidade composta), final field semantics (publicação segura de imutáveis), double-checked locking correto (volatile), **safe vs unsafe publication**. Armadilhas: DCL sem volatile; achar que volatile dá atomicidade de `i++`; publicar `this` no construtor; campo não-final lido sem sincronização. Tronco: "Java Memory Model (JMM)", "Final fields", "Visibility bugs", "Publication bugs". **WebFetch JEP/JLS.**
- **12 — Virtual Threads / Loom (opus).** Platform thread (= OS thread) vs virtual thread (gerenciado pela JVM), carrier threads (ForkJoinPool), mount/unmount em operação bloqueante, **pinning** (synchronized block, native call → carrier preso), quando usar (IO-bound, alta concorrência, thread-per-request) vs não (CPU-bound, não dá pra "pool" virtual threads), `Thread.ofVirtual().start()`, `Executors.newVirtualThreadPerTaskExecutor()`, cautela com ThreadLocal e pooling de recursos caros, virtual vs reactive (gancho Galho 11). Armadilhas: pool de virtual threads (anti-pattern); synchronized em hot path (pinning) → usar ReentrantLock; ThreadLocal pesado com milhões de VTs. Tronco: "Virtual Threads (Java 21+)". **WebFetch JEP 444/425.**
- **13 — Structured concurrency.** Problema (tasks órfãs, leaks, cancelamento manual com ExecutorService), `StructuredTaskScope` + `fork`/`join`, policies (`ShutdownOnFailure` = todas ou falha; `ShutdownOnSuccess` = primeira que vence), propagação de erro e cancelamento automático, escopo como unidade de trabalho. Status preview→final (verificar release exato). Armadilhas: vazar tasks fora do scope; ignorar cancelamento; misturar com ExecutorService manual. Tronco: "Structured Concurrency". **WebFetch JEP (453/462/480/499/505 conforme release).**
- **14 — Scoped values.** Problemas do ThreadLocal (lifetime ilimitado, mutável, inheritance caro com muitas VTs), `ScopedValue` (imutável, escopo dinâmico delimitado por `where().run()`), rebinding, herança em forks de structured concurrency, ThreadLocal vs ScopedValue (tabela). Status final Java 25 (verificar). Armadilhas: tentar mutar; usar fora do escopo; assumir herança automática sem structured concurrency. Tronco: "Scoped Values (Java 25 final)". **WebFetch JEP.**
- **15 — Parallel streams e fork/join.** `ForkJoinPool`, work-stealing, common pool (compartilhado com parallel streams e CompletableFuture), `RecursiveTask`/`RecursiveAction` + fork/join/compute, `.parallel()` em streams, quando ganha (CPU-bound, dataset grande, spliterator balanceado, sem ordering) vs perde (IO, source `LinkedList`/`Iterator`, lambdas com estado, autoboxing). Armadilhas: estado mutável compartilhado em lambda; bloquear IO no common pool; `parallel()` em dataset pequeno (overhead > ganho). Tronco: "Parallel Streams", "ForkJoinPool" (deep). Liga ao Galho 2.
- **16 — Padrões e diagnóstico.** Patterns (imutabilidade/thread-confinement, producer-consumer com BlockingQueue, thread-local state, copy-on-write, guarded suspension) + diagnóstico (anatomia de thread dump: RUNNABLE/BLOCKED/WAITING, deadlock detectado, contention; JFR + Mission Control; `jcmd Thread.print`; async-profiler para lock contention; sintomas → causa). Cheatsheet de fechamento (qual primitiva para qual problema). Tronco: "Patterns de design concorrente", "Debugging e profiling", "Armadilhas comuns".

## 6. Poda do tronco (`Java Concurrency.md`)

Poda **integral** — todo o tronco migra pro Galho 4 (diferente da poda parcial do Galho 1). Procedimento:

1. **Ler o tronco** pra confirmar headings reais (linhas indicadas no §1 podem ter mudado; já mapeados em pré-flight).
2. **Substituir** o corpo de cada seção conceitual por callout apontando pra(s) nota(s) do galho:

```markdown
> [!nota] Migrado para galho próprio
> Este tópico foi expandido no galho [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Concorrência e paralelismo]]. Veja em particular [[11 - Java Memory Model em profundidade]] e [[03 - Exclusão mútua com synchronized]].
```

Mapeamento de poda (seção do tronco → nota destino):

| Seção do tronco | Nota(s) destino |
|---|---|
| O que é + Threads na JVM | 01, 02 |
| Java Memory Model (JMM) + Final fields | 11 |
| Synchronized (incl. wait/notify, anti-patterns) | 03 |
| java.util.concurrent.locks | 05 |
| Atomic classes | 06 |
| Concurrent Collections | 07 |
| ExecutorService e Thread Pools | 08 |
| CompletableFuture | 10 |
| Sincronizadores | 09 |
| ForkJoinPool + Parallel Streams | 15 |
| Virtual Threads | 12 |
| Structured Concurrency | 13 |
| Scoped Values | 14 |
| Deadlock, Race Condition e companhia | 04, 11 |
| Patterns de design concorrente + Debugging e profiling + Armadilhas comuns | 16 |

3. **Higienizar** a seção `## Na prática (da minha experiência)` (linha ~1441): reescrever como padrão neutro/hipotético ou remover atribuição pessoal (regra inegociável de fabricação). As seções `## How to explain in English` e `### Key vocabulary` do tronco têm conteúdo bom — migrar o útil pras seções "Em entrevista" das notas e podar do tronco.
4. **Atualizar** "Veja também" do tronco linkando o MOC do galho + `updated: 2026-06-03`. Manter `publish: false` no tronco.
5. **Reduzir o tronco** a um redirect enxuto: header + TL;DR apontando pro galho + os callouts por seção + Veja também. Como o galho é dono integral, o tronco vira essencialmente um índice histórico/redirect (candidato a deprecação formal quando o MOC central amadurecer — **não** decidir agora).
6. **Não apagar** histórico — commit reversível.

## 7. Critérios de aceitação do galho

Além dos critérios gerais (§10 do roadmap):

1. 16 notas em `03-Dominios/Tecnologia/Java/Concorrência e paralelismo/`, frontmatter completo com `fase:`, `publish: true`, distribuídas 4/6/6.
2. MOC do galho com 3 subseções de fase + 5 rotas alternativas + dataview + folder-link resolve (index.md presente).
3. Dicionário de Java **expandido** (não recriado) com ~28-32 verbetes de concorrência em ordem alfabética; verbetes do Galho 1 intactos; `updated` atualizado.
4. MOC central `Java/index.md` com Galho 4 ativado (linha 28 vira wikilink); resto intacto.
5. Tronco `Java Concurrency` podado integralmente (callouts + redirect) + fabricação higienizada; `publish: false` mantido; histórico preservado.
6. Cada nota: TL;DR; 3-5 code samples (notas conceituais); "Em entrevista" com frase 3+ sentenças EN + 6+ termos PT→EN; "Armadilhas" com exemplo+fix (≥2 Iniciado, ≥3 Adepto/Magus); wikilinks (galho + tronco + MOC + Dicionário); "Referências" com docs/JEPs.
7. Zero fabricação de experiência pessoal.
8. Features version-specific (virtual threads GA 21, structured concurrency, scoped values, StampedLock, LongAdder) verificadas via doc oficial/JEP; status GA/preview correto e hedged.
9. 1 commit por nota; sem `Co-Authored-By: Claude`; sem `--no-verify`; stage nominal.
10. `verificar-wikilinks` roda limpo na pasta do galho (cuidado: falso-positivo em self-anchors `[[#Heading]]` — preferir não usar âncoras same-file); Quartz publica sem erros.

## 8. Riscos e mitigações

| Risco | Mitigação |
|---|---|
| Nota 11 (JMM) ou 12 (Loom) inflarem (>700 linhas) | Notas densas são esperadas aqui; teto de ~700 é guia, não trava. Se passar muito, considerar dividir (ex: 11 → JMM + safe publication), decidir na execução. Usar modelo **opus** nessas. |
| Sobreposição virtual threads entre Galho 1 (15), Galho 4 (12) e futuro Galho 11 | Dono é o Galho 4 (nota 12). Galho 1 já está fechado citando-as como marco — não re-editar. Galho 11 (futuro) linkará pra cá. |
| Wikilinks pra galhos inexistentes (2 Streams, 3 JVM, 11 Reativa) quebrarem | Linkar o **tronco** `Java Fundamentals` (JVM/Streams) e o MOC central, nunca notas inexistentes. MOC marca galhos 3/11 como "planejado" (texto, sem wikilink). |
| Code samples de concorrência não serem deterministas (race/visibility) | Declarar explicitamente que o output é não-determinístico; usar exemplos que *demonstram* o bug sem prometer reprodução garantida. |
| Status preview/final de structured concurrency e scoped values envelhecer/estar errado | WebFetch JEP obrigatório nas notas 13/14; versões hedged; declarar release exato verificado. |
| Poda integral deixar o tronco órfão/confuso | Tronco vira redirect enxuto (não monstro meio-podado); decisão de deprecação formal adiada pro amadurecimento do MOC central. |
| Fabricação herdada do tronco ("da minha experiência", linha 1441) vazar | Poda higieniza obrigatoriamente; rubrica exige zero atribuição pessoal; notas novas usam framing neutro. |
| Magus pesado (6 notas) inflar o galho | Autorizado pelo roadmap pra galhos complexos; distribuição 4/6/6 fixada; se inflar, dividir nota (não galho). |

## 9. Próximos passos

1. **Aprovação deste spec**
2. **Plano de execução** via skill `superpowers:writing-plans` → `docs/superpowers/plans/2026-06-03-java-galho-04-concorrencia-execution.md`
3. **Execução** via `superpowers:subagent-driven-development` em branch dedicada `java-galho-04-concorrencia` (1 subagente por nota; sonnet, opus pras notas 11/12; review por fase + fix loop)
4. **Verificação** de wikilinks + build Quartz
5. **Revisão do roadmap** com aprendizados antes do próximo galho

## 10. Documentos relacionados

- `2026-06-02-java-senior-roadmap-design.md` — roadmap macro (18 galhos)
- `2026-06-02-java-galho-01-linguagem-design.md` — spec do Galho 1 (template de qualidade)
- `2026-06-02-java-galho-01-linguagem-execution.md` — plano do Galho 1 (template de plano)
- Tronco a podar: `03-Dominios/Tecnologia/Java/Core/Java Concurrency.md`
- Artefatos a atualizar: `03-Dominios/Tecnologia/Java/Dicionário de Java.md`, `03-Dominios/Tecnologia/Java/index.md`
- Memórias: [[project_trilha_java]], [[project_tronco_galhos_pattern]], [[project_trilhas_fases_aprendizado]], [[feedback_no_fabrication]], [[feedback_quartz_index]], [[feedback_commits]]
