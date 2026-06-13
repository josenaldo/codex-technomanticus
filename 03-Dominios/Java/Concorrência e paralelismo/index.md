---
title: "Concorrência e paralelismo"
created: 2026-06-03
updated: 2026-06-10
type: moc
status: growing
publish: true
tags:
  - java
  - concorrencia
  - moc
aliases:
  - Concorrência Java
  - Galho 4 - Concorrência
---

# Concorrência e paralelismo

> [!abstract] TL;DR
> Galho 4 da trilha Java Senior; concorrência do Java moderno, das threads e do Java Memory Model até executors, CompletableFuture, virtual threads/Loom e structured concurrency. Tema de altíssimo valor de entrevista.

## Sobre este galho

Este galho cobre a **concorrência** Java de ponta a ponta: threads e seu ciclo de vida, exclusão mútua com `synchronized`, Java Memory Model, locks explícitos (`ReentrantLock`, `StampedLock`), atômicos e operações lock-free, concurrent collections, executors e thread pools, sincronizadores clássicos (`CountDownLatch`, `Semaphore`, `Phaser`), composição assíncrona com `CompletableFuture`, virtual threads do Project Loom (GA no Java 21), structured concurrency, scoped values, parallel streams com fork/join e, por fim, padrões e diagnóstico de problemas em produção. Não cobre Streams funcionais, Collections genéricas nem I/O assíncrono — esses tópicos têm galhos próprios.

**Audiência primária:** dev senior em preparação para entrevista internacional. Cada nota tem seção "Em entrevista" com frases prontas em inglês e vocabulário técnico. **Audiência secundária:** o mesmo dev em contexto de decisões de design e troubleshooting de produção — cada nota expõe o "porquê" por trás das escolhas de concorrência e as armadilhas mais cobradas.

## Iniciado

1. [[01 - Concorrência e paralelismo - o modelo]] — concorrência vs paralelismo, memória compartilhada, os 3 problemas, landscape platform vs virtual.
2. [[02 - Threads e seu ciclo de vida]] — Thread/Runnable, estados, join/interrupt, daemon, thread dump.
3. [[03 - Exclusão mútua com synchronized]] — race condition, monitor/intrinsic lock, synchronized, reentrância, wait/notify.
4. [[04 - As armadilhas - race, deadlock e companhia]] — race, deadlock (Coffman), livelock, starvation, fairness.

## Adepto

5. [[05 - Locks explícitos]] — ReentrantLock, ReadWriteLock, StampedLock, Condition; synchronized vs Lock.
6. [[06 - Atômicos e operações lock-free]] — Atomic*, CAS, LongAdder, problema ABA.
7. [[07 - Concurrent collections]] — ConcurrentHashMap, CopyOnWrite, BlockingQueue, SkipList.
8. [[08 - Executors e thread pools]] — ExecutorService, ThreadPoolExecutor, Future, shutdown, sizing.
9. [[09 - Sincronizadores]] — CountDownLatch, CyclicBarrier, Semaphore, Phaser, Exchanger.
10. [[10 - CompletableFuture e composição assíncrona]] — supplyAsync, thenCompose/thenCombine, allOf, exceptionally, timeout.

## Magus

11. [[11 - Java Memory Model em profundidade]] — happens-before, volatile, final fields, double-checked locking, safe publication.
12. [[12 - Virtual Threads e Project Loom]] — platform vs virtual, carrier threads, pinning, thread-per-request, GA Java 21.
13. [[13 - Structured concurrency]] — StructuredTaskScope, joiners, propagação de erro/cancelamento (preview no Java 25).
14. [[14 - Scoped values]] — ScopedValue vs ThreadLocal, where().run(), rebinding (final no Java 25).
15. [[15 - Parallel streams e fork-join]] — ForkJoinPool, work-stealing, common pool, quando paralelizar.
16. [[16 - Padrões e diagnóstico de concorrência]] — patterns + thread dump, JFR, jcmd, cheatsheet de fechamento.

## Rotas alternativas

### Completa

01 → 02 → 03 → 04 → 05 → 06 → 07 → 08 → 09 → 10 → 11 → 12 → 13 → 14 → 15 → 16. Percurso linear do básico ao avançado.

### Entrevista internacional

01 → 03 → 11 → 08 → 12 → 13. Race/JMM, executors, virtual threads, structured concurrency — o que mais cai.

### Java moderno / Loom

01 → 02 → 08 → 12 → 13 → 14. Virtual threads + structured concurrency + scoped values.

### Troubleshooting de produção

04 → 11 → 16 → 08. Deadlock/contention, visibility, diagnóstico, pool sizing.

### Lock-free / performance

06 → 11 → 05 → 15. Atomics, JMM, locks finos, paralelismo.

## Todas as notas

```dataview
TABLE fase, status, updated
FROM "03-Dominios/Java/Concorrência e paralelismo"
WHERE type = "concept"
SORT file.name ASC
```

## Veja também

- [[03-Dominios/Java/index|Java (MOC central)]]
- [[Java Concurrency]]
- [[03-Dominios/Java/Linguagem e sintaxe moderna/index|Linguagem e sintaxe moderna (Galho 1)]]
- [[03-Dominios/Java/Dicionário de Java|Dicionário de Java]]
- [[03-Dominios/Java/JVM/index|JVM por dentro (Galho 3)]] — memória de runtime, GC, JIT e diagnóstico
- [[03-Dominios/Java/Programação Reativa/index|Programação Reativa (Galho 11)]] — o modelo reativo e o confronto honesto com Virtual Threads.
