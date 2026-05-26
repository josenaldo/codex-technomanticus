---
title: "Java Concurrency"
created: 2026-04-10
updated: 2026-04-10
type: concept
status: evergreen
tags:
  - java
  - concorrencia
  - entrevista
publish: false
---

# Java Concurrency

Deep dive em concorrência e paralelismo na JVM — do **Java Memory Model** e happens-before até **Virtual Threads** e **Structured Concurrency**. Uma das áreas mais cobradas em entrevistas senior de Java, e uma das mais mal compreendidas. Para fundamentos gerais de Java, ver [[Java Fundamentals]].

## O que é

Concorrência em Java é a arte de escrever código que múltiplas threads podem executar simultaneamente sem produzir resultados incorretos ou inesperados. Envolve três conceitos centrais:

1. **Visibilidade** — uma thread ver escritas feitas por outras
2. **Ordenação** — garantir que operações aconteçam na ordem esperada
3. **Atomicidade** — operações compostas tratadas como unidade indivisível

Em entrevistas, o que diferencia um senior em concorrência:

1. **Entender o Java Memory Model (JMM)** — volatile, happens-before, e por que `synchronized` funciona
2. **Saber quando usar `synchronized` vs `Lock` vs atômicos vs `Concurrent*` collections**
3. **Conhecer `CompletableFuture`** — composição de operações assíncronas
4. **Dominar `java.util.concurrent`** — ExecutorService, BlockingQueue, Semaphore, CountDownLatch, CyclicBarrier
5. **Virtual Threads** — quando usar (I/O-bound) e quando não (CPU-bound)
6. **Reconhecer bugs clássicos** — deadlock, race condition, livelock, starvation, visibility, reordering

---

## Threads na JVM

### Platform Threads (tradicional)

Thread Java mapeia 1:1 para thread do OS. Cada thread custa ~1 MB de stack + estruturas no kernel. Limite prático: ~5.000-10.000 threads por JVM.

```java
Thread t = new Thread(() -> {
    System.out.println("Running in " + Thread.currentThread().getName());
});
t.setName("worker-1");
t.setDaemon(true);  // thread daemon não impede JVM de sair
t.start();

// Esperar thread completar
t.join();

// Interromper
t.interrupt();  // seta flag; thread deve checar
```

**Raramente criamos `Thread` diretamente em código moderno.** Use `ExecutorService` ou Virtual Threads.

### Estados de uma Thread

```
NEW ──► RUNNABLE ──► BLOCKED (esperando monitor lock)
              │
              ├──► WAITING (Object.wait, Thread.join, LockSupport.park)
              │
              ├──► TIMED_WAITING (sleep, wait(timeout), join(timeout))
              │
              └──► TERMINATED
```

Acessíveis via `thread.getState()` — útil em debugging e thread dumps.

### Thread dump

Em incidentes, thread dump é a primeira ferramenta:

```bash
# Pegar PID
jps

# Thread dump
jstack <pid>

# Ou diretamente na JVM
kill -3 <pid>  # SIGQUIT → stderr

# Ferramentas: jvisualvm, jmc, IntelliJ profiler
```

Analise por:

- **Deadlocks** — `jstack` marca explicitamente
- **Muitas threads em BLOCKED** no mesmo monitor → contention
- **Threads em WAITING** em I/O → pool mal dimensionado
- **Threads em RUNNABLE** com stacks CPU-intensivas → CPU saturada

---

## Java Memory Model (JMM)

O JMM define **o que uma thread pode ver quando lê uma variável modificada por outra thread**. É o fundamento invisível de toda concorrência correta em Java.

### O problema: reordering e visibility

Compiladores, JIT e CPUs reordenam instruções para performance. Em single-threaded isso é invisível, mas em multi-thread pode quebrar código aparentemente correto:

```java
// Thread 1
x = 1;      // (a)
flag = true;  // (b)

// Thread 2
if (flag) {        // (c)
    System.out.println(x);  // (d) — pode imprimir 0!
}
```

Sem sincronização:

- CPU pode reordenar (b) antes de (a)
- Cache de CPU pode manter (a) em cache local sem flush
- Thread 2 pode ver `flag=true` e `x=0`

### Happens-Before: a relação fundamental

**Happens-before** é uma relação entre operações. Se A happens-before B, então o efeito de A é **visível** para B, e A ocorreu **antes** de B na ordem de sincronização.

**Relações happens-before definidas pelo JMM:**

1. **Program order** — dentro de uma thread, cada operação happens-before a próxima
2. **Monitor lock** — unlock de um monitor happens-before qualquer lock subsequente do mesmo monitor
3. **Volatile** — write em volatile happens-before qualquer read subsequente da mesma variável
4. **Thread start** — `Thread.start()` happens-before qualquer ação na thread iniciada
5. **Thread termination** — qualquer ação em uma thread happens-before detecção de término via `join()`
6. **Interruption** — interrupt happens-before detecção via `isInterrupted()` ou `InterruptedException`
7. **Final fields** — término do construtor happens-before publicação do objeto (se publicado corretamente)
8. **Transitivity** — se A hb B e B hb C, então A hb C

### Volatile

`volatile` garante **visibilidade** e **ordenação** para uma variável, mas **não atomicidade**.

```java
public class StopFlag {
    private volatile boolean stop = false;

    public void stop() {
        stop = true;  // visible para outras threads imediatamente
    }

    public void run() {
        while (!stop) {  // sempre lê o valor mais recente
            // work
        }
    }
}
```

Sem `volatile`, o JIT pode otimizar o loop assumindo que `stop` nunca muda → loop infinito.

**Volatile NÃO substitui synchronized:**

```java
// RUIM — volatile não garante atomicidade
private volatile int counter = 0;
public void increment() { counter++; }  // read-modify-write, não atômico!

// BOM
private final AtomicInteger counter = new AtomicInteger();
public void increment() { counter.incrementAndGet(); }

// OU
private int counter = 0;
public synchronized void increment() { counter++; }
```

### Double-Checked Locking (clássico)

Padrão para singleton lazy init, que **só funciona com volatile** desde Java 5:

```java
public class Singleton {
    private static volatile Singleton instance;  // volatile é crítico!

    public static Singleton getInstance() {
        Singleton local = instance;           // leitura em variável local (otimização)
        if (local == null) {
            synchronized (Singleton.class) {
                local = instance;
                if (local == null) {
                    local = new Singleton();
                    instance = local;
                }
            }
        }
        return local;
    }
}
```

Sem `volatile`, outra thread pode ver `instance != null` mas com campos ainda não inicializados (reordering do construtor).

**Solução moderna (mais simples):**

```java
public class Singleton {
    private static class Holder {
        static final Singleton INSTANCE = new Singleton();
    }

    public static Singleton getInstance() {
        return Holder.INSTANCE;  // Classloader garante initialization-on-demand thread-safe
    }
}
```

### Final fields

Campos `final` têm garantia especial: se o objeto é publicado de forma segura (não vazando `this` durante construção), outras threads sempre veem `final` fields corretamente inicializados. É o que permite `String` e `Integer` serem thread-safe sem sincronização.

---

## Synchronized

Mecanismo built-in de locking baseado em **monitores intrínsecos**.

### Synchronized methods

```java
public class Counter {
    private int count = 0;

    // Sinônimo de synchronized(this)
    public synchronized void increment() {
        count++;
    }

    public synchronized int get() {
        return count;
    }
}
```

### Synchronized blocks

```java
public class AccountService {
    private final Object lock = new Object();
    private BigDecimal balance = BigDecimal.ZERO;

    public void deposit(BigDecimal amount) {
        synchronized (lock) {
            balance = balance.add(amount);
        }
    }
}
```

**Por que usar objeto explícito em vez de `synchronized(this)`:**

- Não expõe o lock publicamente (evita interferência externa)
- Pode ter múltiplos locks para operações diferentes
- Protege contra `synchronized(instance)` feito por código cliente

### Synchronized em static methods

```java
public class Config {
    private static int value;

    // Equivalente a synchronized(Config.class)
    public static synchronized void set(int v) {
        value = v;
    }
}
```

### Reentrância

Monitores Java são **reentrantes** — a mesma thread pode adquirir o mesmo lock múltiplas vezes sem deadlock.

```java
public synchronized void a() {
    b();  // OK, mesma thread já detém o lock
}

public synchronized void b() { ... }
```

### Anti-patterns

```java
// RUIM — synchronized em String literal
synchronized ("lock") { ... }  // Strings são interned, outra parte do código pode compartilhar!

// RUIM — synchronized em Integer/Long
private Long counter = 0L;
synchronized (counter) { ... }  // Autoboxing cria novos objetos, lock muda!

// BOM — objeto final dedicado
private final Object lock = new Object();
synchronized (lock) { ... }
```

### wait / notify / notifyAll

Comunicação entre threads via monitor. API antiga, raramente usada em código moderno (prefira `BlockingQueue`, `CountDownLatch`, `Condition`).

```java
synchronized (lock) {
    while (!condition) {
        lock.wait();  // libera lock, espera notify
    }
    // usa recurso
}

// Em outra thread
synchronized (lock) {
    condition = true;
    lock.notifyAll();  // acorda threads esperando
}
```

**Regras:**

- `wait()`, `notify()`, `notifyAll()` só podem ser chamados **segurando o monitor**
- Sempre `wait()` dentro de loop verificando a condição (spurious wakeups)
- Prefira `notifyAll()` — `notify()` acorda uma thread arbitrária

---

## java.util.concurrent.locks

API moderna de locks, mais flexível que `synchronized`.

### ReentrantLock

```java
private final ReentrantLock lock = new ReentrantLock();

public void process() {
    lock.lock();
    try {
        // critical section
    } finally {
        lock.unlock();  // SEMPRE em finally
    }
}
```

**Vantagens sobre `synchronized`:**

```java
// tryLock — não bloqueia
if (lock.tryLock(5, TimeUnit.SECONDS)) {
    try { ... } finally { lock.unlock(); }
} else {
    // não conseguiu obter lock — fallback
}

// Interruptible
lock.lockInterruptibly();

// Fair mode — FIFO (mais lento, mas sem starvation)
Lock fairLock = new ReentrantLock(true);

// Condition variables (wait/notify modernos)
Condition notFull = lock.newCondition();
Condition notEmpty = lock.newCondition();
```

### ReadWriteLock

Múltiplas threads podem ler simultaneamente; escrita é exclusiva.

```java
private final ReadWriteLock rwLock = new ReentrantReadWriteLock();
private final Map<String, String> cache = new HashMap<>();

public String get(String key) {
    rwLock.readLock().lock();
    try {
        return cache.get(key);
    } finally {
        rwLock.readLock().unlock();
    }
}

public void put(String key, String value) {
    rwLock.writeLock().lock();
    try {
        cache.put(key, value);
    } finally {
        rwLock.writeLock().unlock();
    }
}
```

**Quando usar:** read-heavy workloads onde leituras são frequentes e escritas raras.

**Alternativa moderna:** `ConcurrentHashMap` ou `StampedLock` (abaixo) são frequentemente melhores.

### StampedLock (Java 8+)

Mais performático que `ReadWriteLock`, com modo **optimistic read** que não bloqueia.

```java
private final StampedLock lock = new StampedLock();
private int x, y;

public double distanceFromOrigin() {
    long stamp = lock.tryOptimisticRead();  // sem bloquear
    int currentX = x;
    int currentY = y;
    if (!lock.validate(stamp)) {  // alguém escreveu durante a leitura?
        stamp = lock.readLock();  // fallback para read lock tradicional
        try {
            currentX = x;
            currentY = y;
        } finally {
            lock.unlockRead(stamp);
        }
    }
    return Math.sqrt(currentX * currentX + currentY * currentY);
}

public void move(int deltaX, int deltaY) {
    long stamp = lock.writeLock();
    try {
        x += deltaX;
        y += deltaY;
    } finally {
        lock.unlockWrite(stamp);
    }
}
```

**Cuidado:** StampedLock **não é reentrante**. Adquirir 2x na mesma thread = deadlock.

---

## Atomic classes

`java.util.concurrent.atomic` oferece operações atômicas lock-free baseadas em **CAS (Compare-And-Swap)** — primitiva de CPU.

### AtomicInteger, AtomicLong, AtomicReference

```java
AtomicInteger counter = new AtomicInteger(0);

counter.incrementAndGet();   // ++counter atômico
counter.getAndIncrement();   // counter++ atômico
counter.addAndGet(5);        // += 5 atômico

counter.compareAndSet(10, 20);  // if (counter == 10) counter = 20; retorna true/false

counter.updateAndGet(x -> x * 2);  // operação customizada atômica
counter.accumulateAndGet(10, Integer::sum);

AtomicReference<User> ref = new AtomicReference<>(user);
ref.compareAndSet(oldUser, newUser);
```

### LongAdder, DoubleAdder (Java 8+)

Otimizado para alta contenção — mantém múltiplos contadores internos, soma sob demanda.

```java
LongAdder counter = new LongAdder();
counter.increment();
long total = counter.sum();  // combina todos os contadores internos
```

**Use `LongAdder` em vez de `AtomicLong` quando muitas threads incrementam e leituras são ocasionais.** Escala muito melhor sob contenção.

### AtomicStampedReference

Resolve o **ABA problem** — CAS vê `A`, mas o valor foi `A → B → A` no meio.

```java
AtomicStampedReference<Node> ref = new AtomicStampedReference<>(node, 0);
int[] stamp = new int[1];
Node current = ref.get(stamp);
ref.compareAndSet(current, newNode, stamp[0], stamp[0] + 1);
```

---

## Concurrent Collections

Coleções thread-safe otimizadas para concorrência. Muito melhores que `Collections.synchronizedList(...)`.

### ConcurrentHashMap

Map thread-safe com alta concorrência. Não bloqueia reads, bloqueia escrita só em buckets individuais.

```java
ConcurrentHashMap<String, Integer> map = new ConcurrentHashMap<>();

map.put("a", 1);
map.putIfAbsent("a", 2);  // só adiciona se ausente

// Operações atômicas compostas
map.computeIfAbsent("key", k -> expensiveComputation(k));
map.compute("count", (k, v) -> v == null ? 1 : v + 1);
map.merge("count", 1, Integer::sum);

// Iteração é weakly consistent — pode ver ou não modificações concorrentes, mas não lança ConcurrentModificationException
map.forEach((k, v) -> System.out.println(k + "=" + v));

// Paralelismo built-in
map.forEach(10_000, (k, v) -> process(k, v));  // usa ForkJoinPool se > threshold
map.reduce(10_000, (k, v) -> v, Integer::sum);
map.search(10_000, (k, v) -> v > 100 ? k : null);
```

### CopyOnWriteArrayList / CopyOnWriteArraySet

Escrita cria uma cópia inteira do array. Reads são lock-free e consistentes.

**Uso ideal:** estruturas lidas constantemente e raramente modificadas (ex.: listeners, handlers registrados).

```java
CopyOnWriteArrayList<Listener> listeners = new CopyOnWriteArrayList<>();
listeners.add(listener1);  // cria cópia do array
listeners.forEach(Listener::onEvent);  // lock-free, iterator snapshot
```

**Não use para listas que mudam frequentemente** — cada write é O(n).

### BlockingQueue

Queue thread-safe com operações que bloqueiam. Base de thread pools e produtor-consumidor.

```java
BlockingQueue<Task> queue = new LinkedBlockingQueue<>(1000);  // capacidade limitada

// Producer
queue.put(task);       // bloqueia se cheia
queue.offer(task, 5, TimeUnit.SECONDS);  // timeout
queue.offer(task);     // retorna false se cheia (não bloqueia)

// Consumer
Task t = queue.take();     // bloqueia se vazia
Task t = queue.poll(5, TimeUnit.SECONDS);  // timeout
Task t = queue.poll();     // retorna null se vazia
```

**Implementações:**

- **`ArrayBlockingQueue`** — capacidade fixa, array circular, fair mode opcional
- **`LinkedBlockingQueue`** — opcional unbounded, dois locks (put e take), mais throughput
- **`PriorityBlockingQueue`** — prioridade, unbounded, baseado em heap
- **`DelayQueue`** — elementos liberados após delay
- **`SynchronousQueue`** — capacidade zero, handoff direto produtor↔consumidor
- **`LinkedTransferQueue`** — handoff com fallback para queue

### ConcurrentLinkedQueue / ConcurrentLinkedDeque

Non-blocking, lock-free (CAS). Unbounded.

```java
ConcurrentLinkedQueue<Event> events = new ConcurrentLinkedQueue<>();
events.offer(event);       // nunca bloqueia
Event e = events.poll();   // retorna null se vazio
```

**Use quando:** você não quer bloquear mas precisa de fila thread-safe.

### ConcurrentSkipListMap / ConcurrentSkipListSet

Alternativa concorrente a `TreeMap` / `TreeSet`. Mantém ordenação.

---

## ExecutorService e Thread Pools

Abstração para gerenciar threads. **Sempre** prefira em vez de criar threads diretamente.

### Factory methods

```java
// Fixed pool — N threads persistentes
ExecutorService fixed = Executors.newFixedThreadPool(10);

// Single thread — garante ordem sequencial
ExecutorService single = Executors.newSingleThreadExecutor();

// Cached — cria threads sob demanda, reusa ociosas, sem limite (!)
ExecutorService cached = Executors.newCachedThreadPool();

// Scheduled — para tarefas agendadas/recorrentes
ScheduledExecutorService scheduled = Executors.newScheduledThreadPool(4);
scheduled.scheduleAtFixedRate(task, 0, 1, TimeUnit.MINUTES);

// Virtual threads (Java 21+) — 1 virtual thread por task
ExecutorService virtual = Executors.newVirtualThreadPerTaskExecutor();
```

**⚠️ Evite `newCachedThreadPool()` em produção** — pode criar threads sem limite sob carga, causando OOM.

### ThreadPoolExecutor (controle fino)

Para controle completo, use `ThreadPoolExecutor` diretamente:

```java
ThreadPoolExecutor executor = new ThreadPoolExecutor(
    10,                                // corePoolSize
    50,                                // maximumPoolSize
    60, TimeUnit.SECONDS,              // keepAliveTime para threads acima do core
    new LinkedBlockingQueue<>(1000),   // workQueue com capacidade
    new ThreadFactoryBuilder()         // nome das threads para debugging
        .setNameFormat("worker-%d")
        .setDaemon(false)
        .build(),
    new ThreadPoolExecutor.CallerRunsPolicy()  // rejection policy
);
```

**Rejection policies:**

- `AbortPolicy` — lança `RejectedExecutionException` (default)
- `CallerRunsPolicy` — executa na thread que submeteu (backpressure natural)
- `DiscardPolicy` — descarta silenciosamente
- `DiscardOldestPolicy` — descarta o mais antigo da fila

### Submit e Future

```java
ExecutorService executor = Executors.newFixedThreadPool(4);

// Runnable — sem retorno
executor.submit(() -> System.out.println("Task done"));

// Callable — com retorno
Future<String> future = executor.submit(() -> fetchData());
String result = future.get();           // bloqueia
String result = future.get(5, TimeUnit.SECONDS);  // com timeout

// Cancelamento
future.cancel(true);  // mayInterruptIfRunning

// invokeAll — submit múltiplos, espera todos
List<Callable<String>> tasks = List.of(...);
List<Future<String>> futures = executor.invokeAll(tasks);

// invokeAny — retorna o primeiro resultado
String first = executor.invokeAny(tasks);
```

### Shutdown

**Sempre** encerre o executor — senão a JVM não termina.

```java
executor.shutdown();  // não aceita novas, termina as em andamento
if (!executor.awaitTermination(30, TimeUnit.SECONDS)) {
    executor.shutdownNow();  // força interrupção
}
```

**Java 19+:** `ExecutorService` implementa `AutoCloseable`, permitindo try-with-resources:

```java
try (var executor = Executors.newFixedThreadPool(4)) {
    executor.submit(task);
}  // shutdown() + awaitTermination() automaticamente
```

---

## CompletableFuture

API moderna para composição assíncrona. Sucessor de `Future`, muito mais expressivo.

### Criação

```java
// Valor já conhecido
CompletableFuture<String> done = CompletableFuture.completedFuture("value");

// Executar assíncrono
CompletableFuture<User> future = CompletableFuture.supplyAsync(() -> fetchUser(id));

// Com executor customizado
CompletableFuture<User> future = CompletableFuture.supplyAsync(
    () -> fetchUser(id),
    customExecutor
);

// Runnable (sem retorno)
CompletableFuture<Void> task = CompletableFuture.runAsync(() -> sendEmail(id));
```

### Transformação e composição

```java
// thenApply — transforma resultado (sync)
future.thenApply(User::getName)
      .thenApply(String::toUpperCase);

// thenApplyAsync — transforma resultado em thread separada
future.thenApplyAsync(User::enrichData);

// thenCompose — flatMap (chain operações que retornam CompletableFuture)
future
    .thenCompose(user -> fetchOrders(user.getId()))  // evita nested Future<Future<...>>
    .thenCompose(orders -> calculateTotal(orders));

// thenAccept — consome sem retornar (sideeffect)
future.thenAccept(user -> log.info("Got {}", user));

// thenRun — runnable após completar
future.thenRun(() -> System.out.println("Done"));
```

### Combinando futures

```java
// thenCombine — combina dois futures
CompletableFuture<User> userF = fetchUser(id);
CompletableFuture<Address> addressF = fetchAddress(id);

CompletableFuture<UserWithAddress> combined =
    userF.thenCombine(addressF, UserWithAddress::new);

// allOf — espera todos
CompletableFuture<Void> allDone = CompletableFuture.allOf(f1, f2, f3);
allDone.thenRun(() -> System.out.println("All done"));

// Coletar resultados de allOf
List<CompletableFuture<User>> futures = ids.stream()
    .map(id -> CompletableFuture.supplyAsync(() -> fetchUser(id)))
    .toList();

CompletableFuture<List<User>> allUsers = CompletableFuture
    .allOf(futures.toArray(new CompletableFuture[0]))
    .thenApply(v -> futures.stream().map(CompletableFuture::join).toList());

// anyOf — primeiro que completar
CompletableFuture<Object> first = CompletableFuture.anyOf(f1, f2, f3);
```

### Error handling

```java
future
    .thenApply(User::enrich)
    .exceptionally(ex -> {
        log.error("Failed", ex);
        return User.empty();
    });

// handle — trata resultado E exceção
future.handle((result, ex) -> {
    if (ex != null) return "Error: " + ex.getMessage();
    return "OK: " + result;
});

// whenComplete — side effect em ambos os casos (sem transformar)
future.whenComplete((result, ex) -> {
    if (ex != null) log.error("Failed", ex);
    else log.info("Got {}", result);
});

// exceptionallyCompose — flatMap no caso de erro
future.exceptionallyCompose(ex -> fallbackFuture());
```

### Timeout (Java 9+)

```java
future.orTimeout(5, TimeUnit.SECONDS);  // completa excepcionalmente em timeout
future.completeOnTimeout(defaultValue, 5, TimeUnit.SECONDS);  // valor default em timeout
```

### Async vs sync variants

Cada método tem 3 versões:

- `thenApply(fn)` — executa na mesma thread (ou na thread que completou o future)
- `thenApplyAsync(fn)` — executa no ForkJoinPool.commonPool()
- `thenApplyAsync(fn, executor)` — executa em executor customizado

**Regra:** use `Async` + executor customizado em produção para controlar onde o código roda.

---

## Sincronizadores

`java.util.concurrent` oferece várias primitivas de coordenação além de locks.

### CountDownLatch

Uma thread (ou várias) espera até que um contador chegue a zero.

```java
CountDownLatch latch = new CountDownLatch(3);

// Workers
for (int i = 0; i < 3; i++) {
    executor.submit(() -> {
        try { doWork(); }
        finally { latch.countDown(); }
    });
}

// Main thread espera
latch.await();  // bloqueia até contador == 0
// ou
if (latch.await(30, TimeUnit.SECONDS)) {
    // todos completaram
}
```

**Uso:** esperar inicialização de N componentes, coordenar fim de batch, etc.

**Limitação:** é one-shot. Depois de zerar, não reinicia.

### CyclicBarrier

N threads esperam umas às outras em um barrier. Quando todas chegam, elas continuam juntas.

```java
CyclicBarrier barrier = new CyclicBarrier(3, () -> {
    System.out.println("All arrived, proceeding");
});

for (int i = 0; i < 3; i++) {
    executor.submit(() -> {
        phase1();
        barrier.await();  // espera até 3 threads chegarem
        phase2();
    });
}
```

**Diferença do CountDownLatch:**

- CyclicBarrier pode ser **reutilizado** após `reset()`
- CountDownLatch: uma thread espera N eventos; CyclicBarrier: N threads esperam umas às outras

### Semaphore

Controla quantas threads podem acessar um recurso simultaneamente.

```java
Semaphore semaphore = new Semaphore(5);  // 5 permits

public void callExternalAPI() {
    semaphore.acquire();  // bloqueia se sem permits
    try {
        externalApi.call();
    } finally {
        semaphore.release();
    }
}
```

**Uso:** rate limiting, pool de recursos limitados, backpressure.

### Phaser

Mais flexível que `CountDownLatch` e `CyclicBarrier`. Suporta múltiplas fases.

```java
Phaser phaser = new Phaser(3);

for (int i = 0; i < 3; i++) {
    executor.submit(() -> {
        phase1();
        phaser.arriveAndAwaitAdvance();  // espera outras
        phase2();
        phaser.arriveAndAwaitAdvance();
        phase3();
        phaser.arriveAndDeregister();  // sai do grupo
    });
}
```

### Exchanger

Handoff síncrono entre duas threads.

```java
Exchanger<Buffer> exchanger = new Exchanger<>();

// Thread A
Buffer current = new Buffer();
while (true) {
    fillBuffer(current);
    current = exchanger.exchange(current);  // troca com Thread B
}

// Thread B
Buffer current = new Buffer();
while (true) {
    consumeBuffer(current);
    current = exchanger.exchange(current);
}
```

---

## ForkJoinPool

Thread pool otimizado para **divide-and-conquer**. Base das parallel streams e do common pool.

```java
// Common pool — usado por parallelStream()
ForkJoinPool common = ForkJoinPool.commonPool();

// Pool customizado
ForkJoinPool pool = new ForkJoinPool(Runtime.getRuntime().availableProcessors());

// RecursiveTask — retorna valor
class SumTask extends RecursiveTask<Long> {
    private final long[] array;
    private final int start, end;

    @Override
    protected Long compute() {
        if (end - start <= 1000) {
            long sum = 0;
            for (int i = start; i < end; i++) sum += array[i];
            return sum;
        }
        int mid = (start + end) / 2;
        SumTask left = new SumTask(array, start, mid);
        SumTask right = new SumTask(array, mid, end);
        left.fork();                  // executa async
        long rightResult = right.compute();  // executa sync
        long leftResult = left.join();
        return leftResult + rightResult;
    }
}

Long total = pool.invoke(new SumTask(array, 0, array.length));
```

**Work stealing:** cada worker tem uma deque própria. Quando fica sem trabalho, "rouba" tarefas de outras deques. Balanceia carga automaticamente.

---

## Parallel Streams

Stream que executa operações em paralelo usando ForkJoinPool.commonPool().

```java
long sum = list.parallelStream()
    .mapToLong(Item::getValue)
    .sum();
```

**Quando usar:**

- **Dados grandes** (milhares+ elementos)
- **Operação CPU-intensive** por elemento
- **Operação associativa e sem side effects**
- **Fonte particionável** (ArrayList ✅, LinkedList ❌)

**Quando NÃO usar:**

- Poucos elementos (overhead > ganho)
- I/O-bound (common pool fica bloqueado — use `CompletableFuture`)
- Operações com ordem sequencial importante
- Dentro de servidor web compartilhando o common pool

**Cuidados críticos:**

```java
// RUIM — side effect não thread-safe
List<String> result = new ArrayList<>();
stream.parallel().forEach(result::add);  // ConcurrentModificationException ou perda de dados

// BOM — collect é thread-safe
List<String> result = stream.parallel().collect(Collectors.toList());

// RUIM — common pool saturado com I/O
list.parallelStream().map(id -> httpClient.fetch(id)).toList();
// → bloqueia threads do common pool, afeta tudo
```

---

## Virtual Threads (Java 21+)

O maior avanço em concorrência Java em décadas. **Project Loom**.

### O problema que resolve

Platform threads são caras (~1 MB stack, kernel overhead). Em sistemas I/O-bound, você fica limitado por número de threads bloqueadas em I/O, não por CPU.

**Abordagens tradicionais para contornar:**

- **Thread pools** — reutiliza threads, mas pool cheio = requests esperando
- **Async/Reactive** — callback hell ou código "colorido" (CompletableFuture/Reactor)

Virtual threads oferecem a **simplicidade do modelo síncrono** com **escalabilidade do modelo async**.

### Como funciona

Virtual threads são gerenciadas pela JVM, não pelo OS. Quando uma virtual thread bloqueia em I/O, ela é **desmontada** da platform thread carrier e outra virtual thread usa o carrier. Milhões de virtual threads rodam em ~CPU-count platform threads.

```
Platform threads (carriers):  [ T1 ] [ T2 ] [ T3 ] [ T4 ]
                                 │      │      │      │
                                 │      │      │      │
Virtual threads:           [ VT-1 ] [ VT-2 ] ... [ VT-1000000 ]
                             ↑                         ↑
                        monta quando                quando I/O,
                        CPU-bound                   desmonta e libera carrier
```

### Uso

```java
// Criar virtual thread
Thread vt = Thread.ofVirtual().start(() -> {
    System.out.println("In virtual thread");
});

// Executor de virtual threads
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    IntStream.range(0, 10_000_000).forEach(i ->
        executor.submit(() -> {
            var response = httpClient.send(request, BodyHandlers.ofString());
            return process(response);
        })
    );
}
// 10 milhões de tasks, poucas platform threads
```

### Quando usar

**✅ Use virtual threads para:**

- **I/O-bound** — HTTP clients, database, file I/O, sockets
- **Alto fan-out** — agregar dados de muitos serviços
- **Substituir pools grandes** — antes, `newFixedThreadPool(500)` era comum para Tomcat

**❌ NÃO use para:**

- **CPU-bound** — não traz benefício, overhead de scheduling
- **Código com muito `synchronized`** — causa **pinning** (virtual thread pinned no carrier)
- **ThreadLocal heavy** — cada virtual thread tem seus próprios ThreadLocals, consumindo memória

### Pinning (armadilha)

Quando uma virtual thread fica **pinned** no carrier, ela bloqueia a platform thread — perdendo o benefício:

- **Dentro de `synchronized`** (até Java 23 — Java 24+ resolve)
- **Dentro de código nativo JNI**
- **Algumas operações de classe de compatibilidade**

**Diagnóstico:**

```bash
java -Djdk.tracePinnedThreads=full -jar app.jar
```

**Solução:** substitua `synchronized` por `ReentrantLock` em seções críticas que bloqueiam.

### Virtual threads vs Reactive

Reactive (Reactor, RxJava) foi a resposta para escala de I/O na era pré-Loom. **Virtual threads tornam Reactive menos necessário em muitos casos:**

| Aspecto                  | Virtual Threads           | Reactive              |
| ------------------------ | ------------------------- | --------------------- |
| Modelo                   | Síncrono (imperativo)     | Async (declarativo)   |
| Código                   | Simples, igual a blocking | Complexo, operadores  |
| Debugging                | Stack trace normal        | Difícil               |
| Backpressure             | Não nativo                | Nativo                |
| Compat com libs blocking | Sim                       | Não (precisa adapter) |
| Performance I/O          | Equivalente               | Equivalente ou melhor |
| Performance CPU          | Piora                     | Piora                 |

**Quando ainda usar Reactive:**

- Backpressure explícito é requisito
- Streaming com operadores complexos (window, buffer, merge)
- Stack já é Reactive (Spring WebFlux, Project Reactor em bibliotecas)

---

## Structured Concurrency (Java 21 preview, 25 final)

Tratar grupos de tarefas concorrentes como unidade estruturada — começam juntas, terminam juntas, erros propagam para o escopo pai.

### Problema que resolve

Concorrência tradicional é **não estruturada** — tasks começam sem relação pai/filho clara:

```java
// Tradicional — task órfãs, difícil de gerenciar
Future<User> user = executor.submit(() -> fetchUser(id));
Future<List<Order>> orders = executor.submit(() -> fetchOrders(id));
// E se user falhar? orders continua rodando inutilmente
```

### Com structured concurrency

```java
try (var scope = StructuredTaskScope.<Object>open()) {
    var userTask = scope.fork(() -> fetchUser(id));
    var ordersTask = scope.fork(() -> fetchOrders(id));

    scope.join();                 // espera ambos
    scope.throwIfFailed();         // propaga qualquer exceção

    User user = userTask.get();
    List<Order> orders = ordersTask.get();

    return new UserDetails(user, orders);
}
// Qualquer exceção cancela outras tasks e propaga para cima
```

**Vantagens:**

- **Cancelamento automático** — se uma task falha, as outras são canceladas
- **Visibilidade de relações** — scope deixa explícito o grupo de tasks
- **Error handling unificado** — exceções propagam para o escopo
- **Evita leaks** — todas as tasks têm lifetime atrelado ao scope

### Policies

- **`ShutdownOnFailure`** — cancela as outras se qualquer falha
- **`ShutdownOnSuccess`** — cancela as outras quando qualquer uma completa (race)

```java
try (var scope = StructuredTaskScope.open(Joiner.anySuccessfulResultOrThrow())) {
    scope.fork(() -> tryMirror1());
    scope.fork(() -> tryMirror2());
    scope.fork(() -> tryMirror3());
    var result = scope.join();  // primeiro sucesso
}
```

---

## Scoped Values (Java 25 final)

Alternativa thread-safe e eficiente a `ThreadLocal`, especialmente com Virtual Threads.

**Problema com ThreadLocal + Virtual Threads:** cada virtual thread tem seus próprios ThreadLocals. Milhões de virtual threads = milhões de ThreadLocal copies.

```java
// ThreadLocal tradicional
private static final ThreadLocal<User> CURRENT_USER = new ThreadLocal<>();

CURRENT_USER.set(user);
try {
    doSomething();  // lê CURRENT_USER
} finally {
    CURRENT_USER.remove();  // fácil esquecer → leak
}

// Scoped Value (moderno)
private static final ScopedValue<User> CURRENT_USER = ScopedValue.newInstance();

ScopedValue.where(CURRENT_USER, user).run(() -> {
    doSomething();  // lê CURRENT_USER.get()
});
// Automaticamente limpo ao sair do scope
```

**Vantagens:**

- Imutável dentro do escopo (mais seguro)
- Sem leaks (lifecycle claro)
- Eficiente com virtual threads (sem copies)

---

## Deadlock, Race Condition e companhia

Os clássicos bugs de concorrência.

### Race Condition

Resultado depende da ordem de execução de threads. O bug mais comum.

```java
// BUG — check-then-act
if (!map.containsKey(key)) {  // ✓ thread B pode entrar aqui também
    map.put(key, value);       // ✓ ambos escrevem
}

// FIX
map.putIfAbsent(key, value);  // atômico
// ou
map.computeIfAbsent(key, k -> computeValue(k));
```

### Deadlock

Duas threads esperam uma pela outra, para sempre.

```java
// Thread A
synchronized (lockA) {
    synchronized (lockB) { ... }  // espera lockB
}

// Thread B
synchronized (lockB) {
    synchronized (lockA) { ... }  // espera lockA
}
// → DEADLOCK
```

**Prevenção:**

- **Ordem consistente de locks** — sempre adquirir na mesma ordem global
- **`tryLock` com timeout** — fallback e retry
- **Menos locks** — combinar recursos sob um único lock
- **Lock-free structures** quando possível

**Detecção:** `jstack` marca explicitamente deadlocks. JMX tem `findDeadlockedThreads()`.

### Livelock

Threads estão ativas mas não progridem — ficam reagindo uma à outra.

```java
// Duas pessoas no corredor estreito, cada uma desvia para o mesmo lado
```

**Prevenção:** introduzir aleatoriedade (backoff com jitter), ou lógica assimétrica.

### Starvation

Uma thread nunca obtém o recurso que precisa, porque outras sempre passam na frente.

**Causa comum:** prioridades de thread mal usadas, ou lock não-fair sempre favorecendo a mesma thread.

**Prevenção:** `ReentrantLock(true)` (fair mode), `Semaphore(permits, true)`, evitar prioridades.

### Visibility bugs

Thread não vê escritas de outra thread por falta de sincronização.

```java
// BUG
private boolean stop = false;
public void stop() { stop = true; }
public void run() { while (!stop) { work(); } }  // pode ser loop infinito

// FIX
private volatile boolean stop = false;
```

### Publication bugs (unsafe publication)

Publicar objeto parcialmente construído.

```java
// BUG
class Holder {
    private Holder holder;
    public void initialize() { this.holder = new Holder(data); }
    public Holder get() { return holder; }  // outra thread pode ver Holder com fields default
}

// FIX
// - usar volatile
// - usar final fields (safe publication garantida)
// - sincronizar publicação
```

---

## Patterns de design concorrente

### Thread-safe por imutabilidade

A maneira mais simples de ser thread-safe: **não mudar**.

```java
// Imutável — safe sem sincronização
public record Point(int x, int y) {}

// String, Integer, LocalDate, BigDecimal — todos imutáveis
```

**Regras para imutabilidade:**

1. Todos os campos `final`
2. Sem setters
3. Classe `final` (ou construtor privado + factory)
4. Defensive copy de inputs e outputs mutáveis
5. `this` não escape durante construção

### Producer-Consumer

```java
BlockingQueue<Task> queue = new ArrayBlockingQueue<>(1000);

// Producer
executor.submit(() -> {
    while (!done) {
        Task task = generateTask();
        queue.put(task);  // bloqueia se cheia (backpressure)
    }
});

// Consumers
for (int i = 0; i < 10; i++) {
    executor.submit(() -> {
        while (!Thread.currentThread().isInterrupted()) {
            Task task = queue.take();
            process(task);
        }
    });
}
```

### Thread-local state

Isola estado por thread — cada thread tem sua própria cópia.

```java
// Tradicional
private static final ThreadLocal<DateFormat> FORMAT =
    ThreadLocal.withInitial(() -> new SimpleDateFormat("yyyy-MM-dd"));

String formatted = FORMAT.get().format(date);

// Moderno (Java 25): Scoped Values quando possível
```

**Cuidados:**

- **Leaks** — remover com `ThreadLocal.remove()` em pools de thread
- **Virtual threads** — evite, prefira Scoped Values

### Double-Checked Locking

Lazy initialization thread-safe. Ver seção volatile acima.

### Copy-on-write

Leituras são frequentes, escritas raras. Na escrita, cria cópia inteira.

```java
private volatile List<Listener> listeners = List.of();

public synchronized void addListener(Listener l) {
    listeners = Stream.concat(listeners.stream(), Stream.of(l)).toList();
}

public void fire(Event e) {
    listeners.forEach(l -> l.onEvent(e));  // sem sincronização no read
}
```

Ou use `CopyOnWriteArrayList` direto.

---

## Debugging e profiling

### Thread dump

```bash
jstack <pid> > dump.txt

# Analise:
# - Deadlocks (marcados explicitamente)
# - Threads em BLOCKED (contention)
# - Threads em WAITING (pools mal dimensionados)
# - Threads iguais em runnable (loop?)
```

### JFR (Java Flight Recorder)

Built-in desde Java 11. Gera profile de baixo overhead.

```bash
java -XX:StartFlightRecording=duration=60s,filename=profile.jfr -jar app.jar

# Abrir no JDK Mission Control (jmc)
```

**Eventos relevantes para concorrência:**

- Thread state changes
- Lock contention
- Monitor wait
- Thread park

### async-profiler

Profiler low-overhead externo, excelente para flame graphs.

```bash
./profiler.sh -d 60 -f profile.html <pid>
```

### jcmd

```bash
jcmd <pid> Thread.print       # thread dump
jcmd <pid> GC.heap_dump file  # heap dump
jcmd <pid> JFR.start duration=60s filename=profile.jfr
```

---

## Armadilhas comuns

- **`volatile` para atomicidade** — não protege operações compostas (`counter++`)
- **`synchronized` em wrapper** — `Long`, `Integer` mudam de identidade com autoboxing
- **Double-checked locking sem `volatile`** — quebra com reordering
- **`catch (InterruptedException e) {}`** — engole o interrupt. Sempre `Thread.currentThread().interrupt();` ou propague
- **`ThreadLocal` sem `remove()`** — leak em pools de thread
- **`Executors.newCachedThreadPool()` em produção** — sem limite, OOM sob carga
- **Compartilhar `SimpleDateFormat` sem sync** — não é thread-safe
- **`HashMap` em concorrência** — race condition, pode virar loop infinito
- **`parallelStream()` em I/O** — bloqueia common pool, afeta todo o sistema
- **`parallelStream()` com side effects** — ConcurrentModificationException ou perda de dados
- **Deadlock por ordem inconsistente de locks** — sempre adquirir na mesma ordem
- **`synchronized(this)` com lock exposto** — código externo pode sincronizar no mesmo objeto
- **`wait()` sem loop** — spurious wakeups causam bugs
- **Virtual threads com muito `synchronized`** — pinning, perde o benefício
- **`CompletableFuture.get()` sem timeout** — pode travar para sempre
- **`shutdown()` sem `awaitTermination()`** — tasks perdidas
- **Não nomear threads de pool** — thread dumps ilegíveis (`pool-1-thread-1`)
- **Confiar em `Thread.sleep()` para coordenação** — frágil, sempre é race condition
- **Incremento não atômico em contadores** — use `AtomicLong` ou `LongAdder`
- **Assumir ordem entre threads sem happens-before** — reordering pode morder
- **ThreadPoolExecutor com unbounded queue** — efetivo até `maximumPoolSize` nunca ser atingido
- **Chamar API bloqueante de dentro de `CompletableFuture` sync** — bloqueia o common pool

---

## Na prática (da minha experiência)

> **MedEspecialista — migração para Virtual Threads:**
> Java 21 trouxe Virtual Threads, e foi uma das migrações mais impactantes que fiz. O backend Spring Boot estava usando `newFixedThreadPool(200)` para processar requests que fazem múltiplas chamadas a serviços externos (integrações com clínicas, pagamento, notificação). Sob carga, threads ficavam bloqueadas esperando I/O, e o pool enchia.
>
> **Migração:** `spring.threads.virtual.enabled=true` em Spring Boot 3.2+. A partir daí, cada request do Tomcat roda em virtual thread. Resultado: eliminei tuning de pool, a aplicação passou a aguentar 10x mais concorrência no mesmo hardware, e o código continuou sendo **imperativo síncrono** — muito mais simples que migrar para WebFlux.
>
> **Armadilha:** uma biblioteca interna usava `synchronized` pesado em um método chamado milhões de vezes. Isso causou pinning das virtual threads, anulando o ganho. Migrei o `synchronized` para `ReentrantLock` e o problema desapareceu. `-Djdk.tracePinnedThreads=full` foi essencial para diagnosticar.
>
> **Cuidado com ThreadLocal:** o sistema tinha `ThreadLocal<UserContext>` para carregar o user autenticado através da chain de chamadas. Com virtual threads, cada request tem uma thread diferente, e ThreadLocal funcionava, mas vi consumo de memória aumentando. Migrei para Scoped Values (quando for final em Java 25) e reduziu o footprint significativamente.
>
> **CompletableFuture para chamadas paralelas:**
> Em endpoint que precisa agregar dados de 5 serviços diferentes, usei `CompletableFuture` para paralelizar. Antes era sequencial (~2s), depois ~400ms.
>
> ```java
> var user = CompletableFuture.supplyAsync(() -> userService.find(id), executor);
> var orders = CompletableFuture.supplyAsync(() -> orderService.list(id), executor);
> var prefs = CompletableFuture.supplyAsync(() -> prefService.get(id), executor);
>
> return CompletableFuture.allOf(user, orders, prefs)
>     .thenApply(v -> new UserDetails(user.join(), orders.join(), prefs.join()))
>     .orTimeout(3, TimeUnit.SECONDS)
>     .join();
> ```
>
> Executor customizado foi importante — não usar o `ForkJoinPool.commonPool()` porque o compartilho com parallel streams no resto da aplicação.
>
> **Incidente clássico de concorrência:**
> Um dia debuguei um bug onde um cache em `HashMap` estava entrando em loop infinito em produção, consumindo 100% de uma CPU. Causa: `HashMap` não é thread-safe, e sob resize concorrente, a estrutura interna pode virar um cyclic linked list. Solução: `ConcurrentHashMap`. Lesson learned: nunca use `HashMap` mutável em código compartilhado.
>
> **Lock contention em produção:**
> Descobri via JFR profiling que um método `synchronized` estava gargalando a aplicação. Contenção alta em `java.util.Collections.synchronizedMap`. Migrei para `ConcurrentHashMap` e p99 caiu de 200ms para 15ms.
>
> **A lição principal:** concorrência correta é difícil, mas as ferramentas modernas (Virtual Threads, CompletableFuture, java.util.concurrent) tornaram muito mais fácil do que era em 2010. Aprenda o Memory Model uma vez, domine 2-3 padrões (immutability, producer-consumer, CompletableFuture chain), e você resolve 90% dos casos. Para os outros 10%, use thread dumps, JFR, e não tente ser esperto sem medir.

---

## How to explain in English

> "Java concurrency is an area where understanding the Java Memory Model is the foundation. The JMM defines happens-before relationships that determine when writes by one thread are visible to another. Without understanding this, even simple code can have subtle bugs — like a loop that doesn't terminate because the compiler optimized assuming no other thread modifies the flag.
>
> For synchronization, my default is choosing the weakest tool that works. Immutability first — if the object can't change, it's automatically thread-safe. Then atomic classes for counters and references. Then ConcurrentHashMap for maps. Only when I need compound operations do I reach for explicit locks. I use `synchronized` for simple cases and `ReentrantLock` when I need tryLock, timeouts, or fair mode.
>
> For asynchronous composition, I use CompletableFuture. It's much more expressive than the old Future interface — thenCompose, thenCombine, allOf, exceptionally, and orTimeout cover most use cases. I always pass an explicit executor to the async variants so I know which thread pool is running what, especially in production where the common ForkJoinPool shouldn't be overloaded.
>
> Virtual Threads, introduced in Java 21, have been transformative. For I/O-bound workloads, which is most of what a typical backend does, they eliminate the need to tune thread pools. At MedEspecialista, I enabled them in Spring Boot 3.2+ with a single property, and the application could handle 10x more concurrent requests with the same hardware. The code stays synchronous and imperative, which is simpler than moving to WebFlux. The main pitfall is pinning — if code uses synchronized heavily, virtual threads get pinned to their carrier thread and you lose the benefit. I use `-Djdk.tracePinnedThreads=full` to diagnose and migrate hot synchronized paths to ReentrantLock.
>
> For common bugs, I watch for the usual suspects: race conditions in check-then-act, deadlocks from inconsistent lock ordering, visibility bugs from missing volatile, and the classic HashMap-in-concurrent-code trap. When things go wrong in production, jstack and JFR are my first tools."

### Frases úteis em entrevista

- "The Java Memory Model defines happens-before relationships that determine cross-thread visibility."
- "I prefer immutability first, then atomic classes, then concurrent collections, then explicit locks."
- "Volatile gives you visibility and ordering, but not atomicity."
- "My default is `synchronized` for simplicity; I use `ReentrantLock` when I need tryLock or fair mode."
- "CompletableFuture is my go-to for async composition — chain with thenCompose, combine with allOf."
- "Virtual Threads in Java 21 let me keep imperative code while scaling I/O-bound workloads to millions of concurrent operations."
- "The main virtual thread pitfall is pinning — `synchronized` causes it until Java 24."
- "For CPU-bound work, I use platform threads with a pool sized to CPU count. Virtual threads don't help there."
- "Never use plain HashMap in shared state — use ConcurrentHashMap or the copy-on-write pattern."
- "Rate limiting with Semaphore, coordinating phases with CountDownLatch or CyclicBarrier, handoff with SynchronousQueue."
- "Always pass an explicit executor to CompletableFuture async methods — don't rely on the common pool."

### Key vocabulary

- concorrência → concurrency
- paralelismo → parallelism
- thread virtual → virtual thread
- thread plataforma → platform thread (carrier)
- modelo de memória Java → Java Memory Model (JMM)
- acontece antes → happens-before
- visibilidade → visibility
- atomicidade → atomicity
- reordenação → reordering
- condição de corrida → race condition
- impasse → deadlock
- inanição → starvation
- contenção de lock → lock contention
- comparação e troca → compare-and-swap (CAS)
- lock reentrante → reentrant lock
- bloqueante → blocking
- sem bloqueio → non-blocking
- trava / lock → lock
- barreira → barrier
- semáforo → semaphore
- fila bloqueante → blocking queue
- pool de threads → thread pool
- executor → executor service
- future composável → composable future (CompletableFuture)
- concorrência estruturada → structured concurrency
- valor com escopo → scoped value
- fixação → pinning (virtual thread pinned to carrier)
- publicação segura → safe publication

---

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

- [[Java Fundamentals]] — fundamentos gerais (sintaxe, collections, streams, OOP)
- [[Spring Boot]] — concorrência em Spring (async, thread pools, virtual threads)
- [[System Design]] — patterns de concorrência em larga escala
- [[Redes e Protocolos]] — I/O-bound, connection pooling, timeouts
- [[Banco de dados]] — transações, isolation levels, connection pool
- [[03-Dominios/Java/Backend/Kafka/Kafka]] — consumer concurrency, paralelismo por partição
