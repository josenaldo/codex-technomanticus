---
title: "Executors e thread pools"
created: 2026-06-03
updated: 2026-06-03
type: concept
progress: backlog
status: seedling
publish: true
fase: adepto
tags:
  - java
  - concorrencia
  - adepto
  - executors
  - thread-pools
aliases:
  - ExecutorService
  - Thread pool
  - ThreadPoolExecutor
---

# Executors e thread pools

> [!abstract] TL;DR
> **Nunca crie `Thread` diretamente em código moderno:** use um **`ExecutorService`** para separar a lógica de tarefa da política de uso de threads. A hierarquia é `Executor` → `ExecutorService` → `ScheduledExecutorService`. A classe utilitária `Executors` oferece factory methods rápidos, mas todos têm perigos silenciosos — `newCachedThreadPool()` cria threads sem limite, e `newFixedThreadPool(n)` usa uma fila `LinkedBlockingQueue` sem capacidade definida, que pode crescer até consumir toda a memória. Para produção, construa um `ThreadPoolExecutor` diretamente e defina core/max pool, tamanho de fila e rejection policy explicitamente. Sempre encerre o executor com o padrão `shutdown` → `awaitTermination` → `shutdownNow`, ou use o `try-with-resources` disponível desde Java 19+.

## O que é

Um **thread pool** é um conjunto pré-alocado de threads que aceita tarefas de uma fila e as executa sem criar uma nova thread para cada trabalho. A ideia central é reutilizar threads — criá-las tem custo de SO — e limitar o número em execução para evitar contenção de CPU e memória.

O framework `java.util.concurrent` (Java 5+) abstrai esse mecanismo pela hierarquia `Executor` / `ExecutorService`. O desenvolvedor submete tarefas (`Runnable` ou `Callable<T>`) e o pool decide quando e em qual thread executá-las.

```java
new Thread(() -> processarPedido(pedido)).start();  // antipadrão: thread nova por task
executor.submit(() -> processarPedido(pedido));     // pool gerencia as threads
```

## Por que importa

- **Throughput e latência:** criar uma thread plataforma custa tempo (alocação de stack, syscall) e ≈ 512 KB de memória. Um pool amortiza esse custo reutilizando threads ociosas.
- **Controle de recursos:** sem limite, uma rafada de requisições pode esgotar memória e file descriptors. O pool é o ponto central de backpressure.
- **Observabilidade:** um pool nomeado aparece em thread dumps como `worker-0` — legível. `Thread-23` não diz nada.
- **Entrevistas:** "Como você dimensiona um pool?" e "Qual a diferença entre `shutdown` e `shutdownNow`?" são recorrentes em nível pleno/sênior.

## Como funciona

### `Executor` / `ExecutorService` / `ScheduledExecutorService`

A hierarquia tem três níveis:

```
Executor
  └── ExecutorService           (adiciona submit, invokeAll, invokeAny, lifecycle)
        └── ScheduledExecutorService   (adiciona schedule, scheduleAtFixedRate, scheduleWithFixedDelay)
```

- **`Executor`** — interface mínima com um único método: `void execute(Runnable command)`. Não retorna nada, não oferece controle de ciclo de vida.
- **`ExecutorService`** — estende `Executor` e adiciona: submissão com `Future<T>`, execução em lote (`invokeAll`, `invokeAny`) e gerenciamento de ciclo de vida (`shutdown`, `shutdownNow`, `isTerminated`). Desde Java 19+ também estende `AutoCloseable`.
- **`ScheduledExecutorService`** — adiciona suporte a delays e execução periódica. Útil para jobs recorrentes sem precisar de um scheduler externo.

A interface principal do dia a dia é `ExecutorService`. As implementações concretas mais usadas são `ThreadPoolExecutor` (para tarefas de plataforma) e `ForkJoinPool` (para divide-and-conquer com work-stealing).

---

### Factory methods e seus perigos

A classe `Executors` oferece atalhos convenientes:

```java
// Fixed: N threads persistentes, fila LinkedBlockingQueue SEM limite
ExecutorService fixed = Executors.newFixedThreadPool(4);

// Single: 1 thread, garante execução sequencial, fila também sem limite
ExecutorService single = Executors.newSingleThreadExecutor();

// Cached: SEM limite de threads, cria sob demanda, idle 60s → termina
ExecutorService cached = Executors.newCachedThreadPool();

// Scheduled: N threads core, fila de delay sem limite
ScheduledExecutorService scheduled = Executors.newScheduledThreadPool(4);
scheduled.scheduleAtFixedRate(task, 0, 1, TimeUnit.MINUTES);
scheduled.schedule(task, 5, TimeUnit.SECONDS);        // delay único

// Virtual threads (Java 21+): 1 virtual thread por tarefa
ExecutorService virtual = Executors.newVirtualThreadPerTaskExecutor();
```

**Perigos dos factory methods:**

| Factory method | Risco |
|---|---|
| `newFixedThreadPool(n)` | Fila `LinkedBlockingQueue` sem capacidade → crescimento ilimitado → OOM sob carga sustentada |
| `newCachedThreadPool()` | Usa `SynchronousQueue` (sem buffer) e `maximumPoolSize = Integer.MAX_VALUE` → cria threads sem limite → OOM ou thrashing |
| `newSingleThreadExecutor()` | Mesma fila ilimitada do `newFixedThreadPool` |
| `newScheduledThreadPool(n)` | Fila de delay sem limite; sob carga pode acumular tarefas indefinidamente |
| `newVirtualThreadPerTaskExecutor()` | Threads virtuais são leves, mas tarefas ilimitadas ainda alocam memória de heap e podem esgotar outros recursos |

> [!warning] Regra de produção
> Nenhum dos factory methods acima oferece backpressure real. Para sistemas sob carga variável, prefira `ThreadPoolExecutor` com fila e rejection policy explícitas.

---

### `ThreadPoolExecutor` (controle fino: core/max/keep-alive/workQueue/rejection policy)

O construtor completo:

```java
ThreadPoolExecutor executor = new ThreadPoolExecutor(
    4,                                     // corePoolSize: threads mantidas vivas mesmo ociosas
    16,                                    // maximumPoolSize: teto de threads simultâneas
    60, TimeUnit.SECONDS,                  // keepAliveTime: tempo de vida de threads acima do core
    new ArrayBlockingQueue<>(500),         // workQueue: fila LIMITADA (backpressure real)
    new ThreadFactory() {                  // threadFactory: nomeia threads para thread dumps
        private final AtomicInteger n = new AtomicInteger();
        public Thread newThread(Runnable r) {
            Thread t = new Thread(r, "worker-" + n.getAndIncrement());
            t.setDaemon(false);
            return t;
        }
    },
    new ThreadPoolExecutor.CallerRunsPolicy() // rejection policy
);
```

**Como o pool decide o que fazer com uma tarefa nova:**

```
Task chegou
  ├── threads ativas < corePoolSize  → cria nova thread (mesmo com fila vazia)
  ├── threads ativas >= corePoolSize → tenta enfileirar
  │     ├── fila com espaço          → enfileira
  │     └── fila cheia
  │           ├── threads < maximumPoolSize → cria nova thread
  │           └── threads >= maximumPoolSize → rejection policy
```

> [!info] Armadilha sutil: fila ilimitada anula o maximumPoolSize
> Com `LinkedBlockingQueue` sem capacidade, a fila nunca fica cheia — o pool nunca ultrapassa o `corePoolSize`. O `maximumPoolSize` torna-se letra morta. Para ter threads extras sob pressão, a fila precisa ser bounded (`ArrayBlockingQueue` ou `LinkedBlockingQueue(n)`).

**Parâmetros em detalhe:**

| Parâmetro | Função |
|---|---|
| `corePoolSize` | Threads mantidas vivas mesmo sem trabalho (não terminam pelo keep-alive por padrão) |
| `maximumPoolSize` | Teto absoluto de threads simultâneas no pool |
| `keepAliveTime` | Tempo que threads *acima do core* ficam ociosas antes de terminar |
| `workQueue` | `ArrayBlockingQueue(n)` para fila bounded; `LinkedBlockingQueue()` sem arg é unbounded |
| `threadFactory` | Customiza nome, daemon flag, prioridade das threads |
| `handler` | O que fazer quando fila cheia e pool no teto |

**Rejection policies:**

| Política | Comportamento |
|---|---|
| `AbortPolicy` (padrão) | Lança `RejectedExecutionException` — o caller descobre imediatamente |
| `CallerRunsPolicy` | Executa a tarefa na thread que submeteu — backpressure natural, desacelera o produtor |
| `DiscardPolicy` | Descarta silenciosamente — use só quando perda de tarefa é aceitável |
| `DiscardOldestPolicy` | Descarta a tarefa mais antiga da fila — raramente a escolha certa |

---

### `Future`, `submit` / `invokeAll` / `invokeAny`

```java
Future<String> f = executor.submit(() -> buscarDados(id));  // Callable → Future tipado
String resultado = f.get(5, TimeUnit.SECONDS);              // bloqueia com timeout
f.cancel(true);                                             // interrompe se possível

// invokeAll — bloqueia até TODAS terminarem (com timeout opcional)
List<Future<String>> futures = executor.invokeAll(tarefas, 10, TimeUnit.SECONDS);

// invokeAny — retorna o PRIMEIRO resultado bem-sucedido; cancela as demais
String primeiro = executor.invokeAny(tarefas, 5, TimeUnit.SECONDS);
```

> [!tip] `execute` vs `submit`
> `execute(Runnable)` vem de `Executor` — fire-and-forget, sem retorno. Exceções não capturadas são enviadas ao `UncaughtExceptionHandler` da thread, não propagadas ao caller. `submit(Runnable)` retorna `Future<?>` — exceções ficam armazenadas no `Future` e só são levantadas quando `future.get()` é chamado. Se o `Future` nunca for consultado, a exceção desaparece.

---

### Shutdown gracioso (`shutdown` vs `shutdownNow` + `awaitTermination`)

O padrão canônico de encerramento (presente na própria Javadoc do `ExecutorService`):

```java
executor.shutdown();  // para de aceitar novas tarefas; as em andamento e na fila continuam
try {
    if (!executor.awaitTermination(30, TimeUnit.SECONDS)) {
        executor.shutdownNow();  // envia interrupt para threads ativas; retorna lista de tasks pendentes
        if (!executor.awaitTermination(10, TimeUnit.SECONDS)) {
            log.error("Pool não terminou após shutdownNow");
        }
    }
} catch (InterruptedException e) {
    executor.shutdownNow();
    Thread.currentThread().interrupt();  // restaura o flag de interrupt
}
```

- **`shutdown()`:** para de aceitar tarefas novas; as em fila e em execução continuam.
- **`shutdownNow()`:** envia `interrupt()` para threads ativas; retorna `List<Runnable>` pendentes na fila.
- **`awaitTermination(timeout, unit)`:** bloqueia até TERMINATED ou timeout expirar.

**Java 19+ — `try-with-resources`:** `close()` faz `shutdown()` + `awaitTermination` automaticamente.

```java
try (ExecutorService executor = Executors.newFixedThreadPool(4)) {
    executor.submit(tarefa);
}  // bloqueia até todas as tarefas terminarem
```

---

### Dimensionar o pool (CPU-bound ≈ N+1; IO-bound maior; lei de Little)

**CPU-bound (cálculo puro, sem I/O):**
```
threads = Runtime.getRuntime().availableProcessors() + 1
```
O `+1` compensa pausas breves (GC, page faults). Mais threads do que CPUs só adiciona troca de contexto sem ganho de throughput.

**IO-bound (banco, HTTP, disco):**
```
threads = N × (1 + tempo_espera / tempo_cpu)
```
Se uma tarefa passa 90% do tempo esperando I/O e 10% em CPU, uma CPU suporta até 10 threads com 100% de utilização. Na prática, use profiling e ajuste empírico — os valores teóricos são ponto de partida.

**Lei de Little (queueing theory):** `L = λ × W` — se chegam 100 req/s (`λ`) e cada task leva 0,2s (`W`), o sistema precisa de 20 slots em steady state. Dimensione fila + pool para 2–3× esse valor para absorver picos.

**Com Virtual Threads (Java 21+):** para IO-bound, `newVirtualThreadPerTaskExecutor()` elimina o dimensionamento — o gargalo passa a ser o recurso externo, não o pool.

## Na prática

### Pool configurado manualmente com rejection policy e shutdown ordenado

```java
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

public class PedidoProcessor {

    private final ExecutorService executor;

    public PedidoProcessor() {
        AtomicInteger threadCount = new AtomicInteger();
        this.executor = new ThreadPoolExecutor(
            4,                              // core: sempre vivas
            8,                              // max: até 8 sob pressão
            60, TimeUnit.SECONDS,           // keep-alive das extras
            new ArrayBlockingQueue<>(200),  // fila bounded — backpressure real
            r -> {
                Thread t = new Thread(r, "pedido-worker-" + threadCount.getAndIncrement());
                t.setDaemon(false);
                return t;
            },
            new ThreadPoolExecutor.CallerRunsPolicy()  // desacelera o produtor em vez de descartar
        );
    }

    public Future<ResultadoPedido> processar(Pedido pedido) {
        return executor.submit(() -> {
            // lógica de processamento — pode lançar exceção
            return realizarProcessamento(pedido);
        });
    }

    public void encerrar() {
        executor.shutdown();
        try {
            if (!executor.awaitTermination(30, TimeUnit.SECONDS)) {
                List<Runnable> pendentes = executor.shutdownNow();
                log.warn("Pool forçado; {} tarefas descartadas", pendentes.size());
                if (!executor.awaitTermination(10, TimeUnit.SECONDS)) {
                    log.error("Pool não terminou após shutdownNow");
                }
            }
        } catch (InterruptedException e) {
            executor.shutdownNow();
            Thread.currentThread().interrupt();
        }
    }
}
```

### Recuperar resultado com tratamento de exceção via `Future`

```java
Future<ResultadoPedido> futuro = processor.processar(pedido);

try {
    ResultadoPedido resultado = futuro.get(10, TimeUnit.SECONDS);
    registrar(resultado);
} catch (ExecutionException e) {
    // exceção lançada dentro da task — acessível via getCause()
    log.error("Falha ao processar pedido id={}", pedido.getId(), e.getCause());
} catch (TimeoutException e) {
    futuro.cancel(true);
    log.warn("Timeout ao processar pedido id={}", pedido.getId());
} catch (InterruptedException e) {
    Thread.currentThread().interrupt();
    futuro.cancel(true);
}
```


## Armadilhas

### (1) Não fazer shutdown — threads non-daemon impedem a JVM de encerrar

**O problema:** threads de pool criadas com `setDaemon(false)` (o padrão) são threads de usuário. A JVM só encerra quando todas as threads de usuário terminam. Se o `ExecutorService` nunca for encerrado, as threads ficam vivas indefinidamente, impedindo o shutdown da aplicação — ou causando leak de recursos em aplicações de longa duração que reconfiguram pools dinamicamente.

```java
// RUIM — executor nunca é encerrado
public class Servico {
    private final ExecutorService exec = Executors.newFixedThreadPool(4);

    public void processar(Pedido p) {
        exec.submit(() -> realizarProcessamento(p));
        // exec.shutdown() nunca é chamado → threads vivem para sempre
    }
}
```

```java
// FIX 1 — shutdown no ciclo de vida do componente (Spring @PreDestroy, Hook etc.)
@PreDestroy
public void encerrar() {
    executor.shutdown();
    try {
        if (!executor.awaitTermination(30, TimeUnit.SECONDS))
            executor.shutdownNow();
    } catch (InterruptedException e) {
        executor.shutdownNow();
        Thread.currentThread().interrupt();
    }
}

// FIX 2 — try-with-resources (Java 19+) para operações bem-delimitadas
try (ExecutorService exec = Executors.newFixedThreadPool(4)) {
    exec.submit(tarefa);
}  // close() chama shutdown() + awaitTermination automaticamente
```

---

### (2) Pool ou fila ilimitados — OOM sob carga

**O problema:** os factory methods da classe `Executors` usam filas sem capacidade ou pools sem limite de threads. Sob carga sustentada, a fila cresce sem parar (consumindo heap) ou o número de threads explode (consumindo memória de stack e file descriptors), resultando em `OutOfMemoryError`.

```java
// RUIM — fila LinkedBlockingQueue sem capacidade definida
ExecutorService exec = Executors.newFixedThreadPool(8);
// Sob 10.000 req/s e processamento lento: fila acumula, heap se esgota

// RUIM — threads sem limite
ExecutorService exec = Executors.newCachedThreadPool();
// Sob pico: pode criar 10.000 threads, cada uma com ~512KB de stack
```

```java
// FIX — ThreadPoolExecutor com fila bounded e rejection policy explícita
ExecutorService exec = new ThreadPoolExecutor(
    8, 16, 60, TimeUnit.SECONDS,
    new ArrayBlockingQueue<>(1000),              // backpressure: rejeita ao encher
    Executors.defaultThreadFactory(),
    new ThreadPoolExecutor.CallerRunsPolicy()    // desacelera o produtor
);
```

Dimensionar corretamente requer conhecer: taxa de chegada (req/s), tempo médio de serviço, e margem de pico. Lei de Little fornece a estimativa de base; ajuste empírico (load test) valida.

---

### (3) Exceção engolida em task submetida via `execute` — sem Future para propagar

**O problema:** quando uma tarefa lançada via `execute(Runnable)` lança uma exceção não capturada, ela vai para o `UncaughtExceptionHandler` da thread (que, por padrão, apenas imprime no stderr) e a thread termina. Nenhuma exceção é propagada ao caller, nenhum `Future` armazena o erro. O trabalho falha silenciosamente.

O mesmo acontece com `submit(Runnable)` se o `Future` retornado nunca for consultado via `get()`: a exceção fica armazenada no `Future`, mas ninguém a lê.

```java
// RUIM — exception some; o sistema continua como se nada tivesse acontecido
executor.execute(() -> {
    processar(pedido);  // lança RuntimeException → vai para UncaughtExceptionHandler
});

// TAMBÉM RUIM — Future retornado mas ignorado
executor.submit(() -> processar(pedido));  // Future descartado, exceção nunca vista
```

```java
// FIX 1 — capturar dentro da task e registrar
executor.execute(() -> {
    try {
        processar(pedido);
    } catch (Exception e) {
        log.error("Falha ao processar pedido id={}", pedido.getId(), e);
        // decida: re-enfileirar? marcar como falha? notificar?
    }
});

// FIX 2 — usar submit e consultar o Future
Future<?> f = executor.submit(() -> processar(pedido));
try {
    f.get(10, TimeUnit.SECONDS);  // propaga ExecutionException se a task falhou
} catch (ExecutionException e) {
    log.error("Falha na task", e.getCause());
}

// FIX 3 — UncaughtExceptionHandler na ThreadFactory (rede de segurança)
ThreadFactory factory = r -> {
    Thread t = new Thread(r, "worker");
    t.setUncaughtExceptionHandler((thread, ex) ->
        log.error("Exceção não tratada na thread {}", thread.getName(), ex));
    return t;
};
```

## Em entrevista

### Frase pronta (inglês)

> "The standard practice in Java is to never create `Thread` objects directly in application code — instead, you submit tasks to an `ExecutorService` and let the pool manage thread lifecycle, reuse, and error handling." "The `Executors` factory methods are convenient but carry hidden risks: `newFixedThreadPool` uses an unbounded `LinkedBlockingQueue`, so under sustained load the queue grows without bound until you hit an `OutOfMemoryError`; `newCachedThreadPool` has no thread limit at all and can spawn thousands of threads in seconds." "For production systems I always construct a `ThreadPoolExecutor` directly, with a bounded `ArrayBlockingQueue` and an explicit rejection policy — usually `CallerRunsPolicy`, which naturally slows down the producer thread when the pool is saturated rather than silently dropping work; and I always shut it down explicitly with the `shutdown` → `awaitTermination` → `shutdownNow` pattern, because non-daemon pool threads will prevent the JVM from exiting otherwise."

### Vocabulário

| Termo PT | Termo EN |
|---|---|
| pool de threads | thread pool |
| fila de trabalho | work queue / task queue |
| política de rejeição | rejection policy |
| pressão de retorno | backpressure |
| tamanho do pool (núcleo / máximo) | core pool size / maximum pool size |
| tempo de keep-alive | keep-alive time |
| tarefa pendente | pending task |
| encerramento gracioso | graceful shutdown |
| fábrica de threads | thread factory |
| lei de Little | Little's Law |
| execução em lote | bulk execution / batch submission |
| tarefa agendada | scheduled task |

## Veja também

- [[02 - Threads e seu ciclo de vida]]
- [[10 - CompletableFuture e composição assíncrona]]
- [[15 - Parallel streams e fork-join]]
- [[12 - Virtual Threads e Project Loom]]
- [[03-Dominios/Java/Concorrência e paralelismo/index|MOC do galho]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[Java Concurrency]]
- [[03-Dominios/Java/Dicionário de Java#Executor / ExecutorService|Executor]]
- [[03-Dominios/Java/Dicionário de Java#Thread pool|thread pool]]
- [[03-Dominios/Java/Dicionário de Java#Future|Future]]

## Referências

- [ExecutorService — Java 21 API (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/ExecutorService.html)
- [ThreadPoolExecutor — Java 21 API (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/ThreadPoolExecutor.html)
- [Executors — Java 21 API (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/Executors.html)
- [Lesson: Concurrency — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/essential/concurrency/)
- Goetz, Brian et al. *Java Concurrency in Practice*. Addison-Wesley, 2006. Cap. 6–8 (Task Execution, Applying Thread Pools).
