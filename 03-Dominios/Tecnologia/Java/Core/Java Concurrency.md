---
title: "Java Concurrency"
created: 2026-04-10
updated: 2026-06-03
type: concept
progress: backlog
status: evergreen
tags:
  - java
  - concorrencia
  - entrevista
publish: false
---

# Java Concurrency

> [!info] Tronco em transição
> Este tronco foi **integralmente migrado** para o galho [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Concorrência e paralelismo]] (16 notas em 3 fases). O conteúdo abaixo é um índice de redirecionamento; cada seção aponta para a nota canônica. Mantido por histórico e compatibilidade de wikilinks.

Deep dive em concorrência e paralelismo na JVM — do **Java Memory Model** e happens-before até **Virtual Threads** e **Structured Concurrency**. Uma das áreas mais cobradas em entrevistas senior de Java, e uma das mais mal compreendidas. Para fundamentos gerais de Java, ver [[Java Fundamentals]].

## O que é

> [!nota] Migrado para galho próprio
> Este tópico foi expandido no galho [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Concorrência e paralelismo]]. Veja em particular [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/01 - Concorrência e paralelismo - o modelo|01 - Concorrência e paralelismo: o modelo]] e [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/02 - Threads e seu ciclo de vida|02 - Threads e seu ciclo de vida]].

## Threads na JVM

> [!nota] Migrado para galho próprio
> Este tópico foi expandido no galho [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Concorrência e paralelismo]]. Veja em particular [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/01 - Concorrência e paralelismo - o modelo|01 - Concorrência e paralelismo: o modelo]] e [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/02 - Threads e seu ciclo de vida|02 - Threads e seu ciclo de vida]].

## Java Memory Model (JMM)

> [!nota] Migrado para galho próprio
> Este tópico foi expandido no galho [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Concorrência e paralelismo]]. Veja em particular [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/11 - Java Memory Model em profundidade|11 - Java Memory Model em profundidade]].

## Synchronized

> [!nota] Migrado para galho próprio
> Este tópico foi expandido no galho [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Concorrência e paralelismo]]. Veja em particular [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/03 - Exclusão mútua com synchronized|03 - Exclusão mútua com synchronized]] e [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/11 - Java Memory Model em profundidade|11 - Java Memory Model em profundidade]].

## java.util.concurrent.locks

> [!nota] Migrado para galho próprio
> Este tópico foi expandido no galho [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Concorrência e paralelismo]]. Veja em particular [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/05 - Locks explícitos|05 - Locks explícitos]].

## Atomic classes

> [!nota] Migrado para galho próprio
> Este tópico foi expandido no galho [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Concorrência e paralelismo]]. Veja em particular [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/06 - Atômicos e operações lock-free|06 - Atômicos e operações lock-free]].

## Concurrent Collections

> [!nota] Migrado para galho próprio
> Este tópico foi expandido no galho [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Concorrência e paralelismo]]. Veja em particular [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/07 - Concurrent collections|07 - Concurrent collections]].

## ExecutorService e Thread Pools

> [!nota] Migrado para galho próprio
> Este tópico foi expandido no galho [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Concorrência e paralelismo]]. Veja em particular [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/08 - Executors e thread pools|08 - Executors e thread pools]].

## CompletableFuture

> [!nota] Migrado para galho próprio
> Este tópico foi expandido no galho [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Concorrência e paralelismo]]. Veja em particular [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/10 - CompletableFuture e composição assíncrona|10 - CompletableFuture e composição assíncrona]].

## Sincronizadores

> [!nota] Migrado para galho próprio
> Este tópico foi expandido no galho [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Concorrência e paralelismo]]. Veja em particular [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/09 - Sincronizadores|09 - Sincronizadores]].

## ForkJoinPool

> [!nota] Migrado para galho próprio
> Este tópico foi expandido no galho [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Concorrência e paralelismo]]. Veja em particular [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/15 - Parallel streams e fork-join|15 - Parallel streams e fork/join]].

## Parallel Streams

> [!nota] Migrado para galho próprio
> Este tópico foi expandido no galho [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Concorrência e paralelismo]]. Veja em particular [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/15 - Parallel streams e fork-join|15 - Parallel streams e fork/join]].

## Virtual Threads (Java 21+)

> [!nota] Migrado para galho próprio
> Este tópico foi expandido no galho [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Concorrência e paralelismo]]. Veja em particular [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/12 - Virtual Threads e Project Loom|12 - Virtual Threads e Project Loom]].

## Structured Concurrency (Java 21 preview, 25 final)

> [!nota] Migrado para galho próprio
> Este tópico foi expandido no galho [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Concorrência e paralelismo]]. Veja em particular [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/13 - Structured concurrency|13 - Structured concurrency]].

## Scoped Values (Java 25 final)

> [!nota] Migrado para galho próprio
> Este tópico foi expandido no galho [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Concorrência e paralelismo]]. Veja em particular [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/14 - Scoped values|14 - Scoped values]].

## Deadlock, Race Condition e companhia

> [!nota] Migrado para galho próprio
> Este tópico foi expandido no galho [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Concorrência e paralelismo]]. Veja em particular [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/04 - As armadilhas - race, deadlock e companhia|04 - As armadilhas: race, deadlock e companhia]] e [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/11 - Java Memory Model em profundidade|11 - Java Memory Model em profundidade]].

## Patterns de design concorrente

> [!nota] Migrado para galho próprio
> Este tópico foi expandido no galho [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Concorrência e paralelismo]]. Veja em particular [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/16 - Padrões e diagnóstico de concorrência|16 - Padrões e diagnóstico de concorrência]].

## Debugging e profiling

> [!nota] Migrado para galho próprio
> Este tópico foi expandido no galho [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Concorrência e paralelismo]]. Veja em particular [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/16 - Padrões e diagnóstico de concorrência|16 - Padrões e diagnóstico de concorrência]].

## Armadilhas comuns

> [!nota] Migrado para galho próprio
> Este tópico foi expandido no galho [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Concorrência e paralelismo]]. Veja em particular [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/16 - Padrões e diagnóstico de concorrência|16 - Padrões e diagnóstico de concorrência]].

## Na prática

> [!nota] Migrado para galho próprio
> Padrões práticos e armadilhas de produção foram reescritos de forma neutra em [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/16 - Padrões e diagnóstico de concorrência|16 - Padrões e diagnóstico de concorrência]].

## How to explain in English

> [!nota] Migrado para galho próprio
> Vocabulário de entrevista e frases em inglês agora vivem na seção "Em entrevista" de cada nota do galho [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Concorrência e paralelismo]].

## Recursos

### Livros essenciais

- **Java Concurrency in Practice** — Brian Goetz et al. (2006, mas ainda é A referência)
- **Modern Java in Action** — Raoul-Gabriel Urma, Mario Fusco, Alan Mycroft
- **The Well-Grounded Java Developer** — Benjamin Evans, Jason Clark (capítulos sobre concorrência e JMM)

### Documentação oficial

- [Java Concurrency Tutorial](https://docs.oracle.com/javase/tutorial/essential/concurrency/)
- [Java Memory Model (JSR 133)](https://www.cs.umd.edu/~pugh/java/memoryModel/)
- [java.util.concurrent API](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/package-summary.html)
- [Virtual Threads (JEP 444)](https://openjdk.org/jeps/444)
- [Structured Concurrency (JEP 505)](https://openjdk.org/jeps/505)
- [Scoped Values (JEP 506)](https://openjdk.org/jeps/506)

### Artigos

- [Brian Goetz — Going inside Java's Project Loom](https://www.youtube.com/watch?v=fOEPEXTpbJA)
- [Virtual Threads: Dude, Where's My Lock?](https://www.morling.dev/blog/loom-virtual-thread-pinning/) — pinning explicado
- [Doug Lea's The java.util.concurrent Synchronizer Framework](https://gee.cs.oswego.edu/dl/papers/aqs.pdf) — o paper por trás do AQS
- [Baeldung — java.util.concurrent overview](https://www.baeldung.com/java-util-concurrent)
- [CompletableFuture guide — Baeldung](https://www.baeldung.com/java-completablefuture)

### Ferramentas

- [JMH (Java Microbenchmark Harness)](https://openjdk.org/projects/code-tools/jmh/) — benchmarking correto
- [async-profiler](https://github.com/async-profiler/async-profiler) — CPU, alloc, lock profiling
- [JDK Mission Control](https://adoptopenjdk.net/jmc.html) — análise de JFR
- [VisualVM](https://visualvm.github.io/) — thread dumps, heap dumps, monitoring
- [jstack, jcmd, jps](https://docs.oracle.com/en/java/javase/21/docs/specs/man/) — built-in tools

---

## Veja também

- [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Concorrência e paralelismo (galho)]] — o galho canônico (16 notas em 3 fases)
- [[03-Dominios/Tecnologia/Java/index|Java (MOC central)]]
- [[Java Fundamentals]] — fundamentos gerais (sintaxe, collections, streams, OOP)
- [[Spring Boot]] — concorrência em Spring (async, thread pools, virtual threads)
- [[System Design]] — patterns de concorrência em larga escala
- [[Redes e Protocolos]] — I/O-bound, connection pooling, timeouts
- [[Banco de dados]] — transações, isolation levels, connection pool
- [[03-Dominios/Tecnologia/Java/Backend/Kafka/Kafka]] — consumer concurrency, paralelismo por partição
