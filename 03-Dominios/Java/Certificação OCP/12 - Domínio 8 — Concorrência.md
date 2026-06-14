---
title: "Domínio 8 — Concorrência"
created: 2026-06-13
updated: 2026-06-13
type: concept
status: seedling
publish: true
fase: dominios
tags:
  - java
  - certificacao-ocp
  - dominios
aliases:
  - "Domínio 8 OCP"
  - "Concorrência na OCP"
---

# Domínio 8 — Concorrência

> [!abstract] TL;DR
> Este é o domínio que mais separa quem "sabe Java" de quem "passa na OCP". A Oracle cobra a mecânica fina: a diferença entre `start()` e `run()`, os seis estados de uma thread, o contrato de `synchronized`/`volatile`/`wait`-`notify`, e toda a camada moderna de `ExecutorService`, `CompletableFuture`, atômicos e coleções concorrentes. Na versão Java 21 (1Z0-830) entram os **Virtual Threads** e o `newVirtualThreadPerTaskExecutor` — o tema novo mais provável de aparecer. As pegadinhas aqui quase nunca são sobre lógica: são sobre comportamento de runtime (thread nova ou não? exceção ou silêncio? visibilidade ou atomicidade?). Decore os comportamentos, não só as APIs.

> [!info] Títulos oficiais
> - **1Z0-830 (Java 21)**: *Managing Concurrent Code Execution*
> - **1Z0-831 (Java 25)**: *Implementing Multithreading for Concurrent Code Execution*
>
> O título de 2025 troca "managing" por "implementing multithreading", sinalizando ênfase ainda maior em escrever código concorrente (e não só descrever APIs). O miolo permanece o mesmo; Virtual Threads consolidam de vez como tópico de primeira classe.

## O que a Oracle cobra

- **Criação de thread** — `extends Thread` vs `implements Runnable`; a distinção crucial entre `start()` (cria uma nova linha de execução) e `run()` (executa no caller, sem concorrência). `Runnable` é preferível por não acoplar à herança.
- **Estados da thread** — os seis valores do enum `Thread.State`: `NEW`, `RUNNABLE`, `BLOCKED`, `WAITING`, `TIMED_WAITING`, `TERMINATED`. Saiba que transição leva a cada um (ex.: `wait()` → `WAITING`; `sleep(ms)` → `TIMED_WAITING`; bloqueio em monitor → `BLOCKED`).
- **Lifecycle** — `sleep` (não solta o monitor), `join` (espera outra thread terminar), `interrupt` (sinaliza, não mata).
- **`synchronized`** — em métodos (de instância → lock no `this`; estático → lock no objeto `Class`) e em blocos (`synchronized(obj)`); o conceito de **monitor** (lock reentrante embutido em todo objeto).
- **`volatile`** — garante **visibilidade** entre threads (leituras enxergam a última escrita), mas **não** garante atomicidade de operações compostas.
- **`wait`/`notify`/`notifyAll`** — só podem ser chamados dentro de bloco sincronizado sobre o mesmo objeto; `wait()` solta o monitor, `notify()`/`notifyAll()` acordam threads em espera.
- **`ExecutorService`** — fábricas de `Executors`: `newFixedThreadPool`, `newSingleThreadExecutor`, `newCachedThreadPool`, `newScheduledThreadPool` e — novidade do Java 21 — **`newVirtualThreadPerTaskExecutor`**.
- **`Callable`/`Future`** — `submit` (aceita `Runnable` ou `Callable`), `Future.get` (bloqueia até o resultado), `cancel`.
- **`CompletableFuture`** — `supplyAsync`, `thenApply` (transforma o valor), `thenCompose` (encadeia outro futuro — evita futuro-de-futuro), `thenCombine` (junta dois), `allOf`, `anyOf`, `exceptionally` (recuperação de erro).
- **Atômicos** — `AtomicInteger`, `AtomicReference`, `compareAndSet` (CAS — operação lock-free).
- **Coleções concorrentes** — `ConcurrentHashMap` (leituras sem lock, escrita por segmento) e `CopyOnWriteArrayList` (cópia integral a cada escrita; ideal para leitura predominante).
- **Virtual Threads (Java 21)** — criação (`Thread.ofVirtual()`, `Thread.startVirtualThread()`), e a diferença para platform threads: virtual threads são baratas, montadas sobre poucas threads do SO, ideais para tarefas I/O-bound.
- **Locks** — `ReentrantLock` (lock explícito, mais flexível que `synchronized`) e `ReadWriteLock` (leitores concorrentes, escritor exclusivo) — em nível básico.

## Mapa de revisão

Este domínio mapeia inteiro sobre o Galho 4 (Concorrência e paralelismo). Para a prova, revise nesta ordem:

- [[03-Dominios/Java/Concorrência e paralelismo/02 - Threads e seu ciclo de vida|Threads e seu ciclo de vida (G4)]]
- [[03-Dominios/Java/Concorrência e paralelismo/03 - Exclusão mútua com synchronized|Exclusão mútua com synchronized (G4)]]
- [[03-Dominios/Java/Concorrência e paralelismo/06 - Atômicos e operações lock-free|Atômicos e operações lock-free (G4)]]
- [[03-Dominios/Java/Concorrência e paralelismo/07 - Concurrent collections|Concurrent collections (G4)]]
- [[03-Dominios/Java/Concorrência e paralelismo/08 - Executors e thread pools|Executors e thread pools (G4)]]
- [[03-Dominios/Java/Concorrência e paralelismo/10 - CompletableFuture e composição assíncrona|CompletableFuture (G4)]]
- [[03-Dominios/Java/Concorrência e paralelismo/11 - Java Memory Model em profundidade|Java Memory Model (G4)]]
- [[03-Dominios/Java/Concorrência e paralelismo/12 - Virtual Threads e Project Loom|Virtual Threads e Project Loom (G4)]]
- [[03-Dominios/Java/Concorrência e paralelismo/15 - Parallel streams e fork-join|Parallel streams e fork-join (G4)]]

## Pegadinhas deste domínio

A banca adora cobrar comportamento de runtime, não lógica. Guarde estes cinco reflexos:

**1. `run()` não cria thread.**

```java
Thread t = new Thread(() -> System.out.println(Thread.currentThread().getName()));
t.run();   // roda na thread CHAMADORA — imprime "main"
t.start(); // cria thread nova — imprime "Thread-0"
```

Se a questão chama `run()`, não há concorrência: a tarefa executa síncrona no caller.

**2. `start()` duas vezes lança exceção.**

```java
Thread t = new Thread(task);
t.start();
t.start(); // IllegalThreadStateException em runtime
```

Uma thread só pode ser iniciada uma vez. Reiniciar uma thread terminada também não é permitido.

**3. `volatile` dá visibilidade, não atomicidade.**

```java
volatile int i = 0;
i++; // NÃO é atômico: é read-modify-write — sujeito a perda de atualização
```

Para incremento thread-safe use `AtomicInteger.incrementAndGet()` ou `synchronized`.

**4. `ExecutorService` não fechado segura a JVM.**

Pools (exceto os de virtual threads/daemon) mantêm threads non-daemon vivas; sem `shutdown()` a JVM não encerra. Em Java 21, `ExecutorService` é `AutoCloseable` — prefira try-with-resources:

```java
try (var exec = Executors.newFixedThreadPool(4)) {
    exec.submit(task);
} // close() faz shutdown + aguarda término
```

**5. Virtual thread não se "pooleia".**

Virtual threads são descartáveis e baratas — uma por tarefa. Pooleá-las anula o ganho. Use `Executors.newVirtualThreadPerTaskExecutor()`, nunca `newFixedThreadPool` com virtual threads dentro.

Veja o apanhado geral em [[03-Dominios/Java/Certificação OCP/15 - O catálogo de pegadinhas clássicas|catálogo de pegadinhas]].

## Em entrevista

> "Calling `run()` directly executes the task on the current thread — no new thread is created. You need `start()` to spawn a separate thread of execution."

Outra fala forte para sinalizar atualidade:

> "With virtual threads, I can model each request as its own thread instead of pooling, because they're cheap and scheduled on top of a small carrier pool."

Não reivindique a credencial até ter o certificado em mãos — fale do conhecimento, não do papel.

Vocabulário PT|EN:
- linha de execução → thread
- visibilidade → visibility
- monitor → monitor

## Veja também

- [[03-Dominios/Java/Certificação OCP/04 - O mapa objetivo → galho — revisar a trilha pra prova|O mapa objetivo → galho]]
- [[03-Dominios/Java/Certificação OCP/13 - Domínio 9 — I-O|Domínio 9 — I/O]]
- [[03-Dominios/Java/Certificação OCP/index|Certificação OCP (MOC do galho)]]

## Referências

- https://enthuware.com/oca-ocp-java-certification-resources/290-ocp-java-21-exam-syllabus
