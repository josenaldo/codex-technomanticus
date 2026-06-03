---
title: "Padrões e diagnóstico de concorrência"
created: 2026-06-03
updated: 2026-06-03
type: concept
progress: backlog
status: seedling
publish: true
fase: magus
tags:
  - java
  - concorrencia
  - magus
  - patterns
  - diagnostico
aliases:
  - Padrões de concorrência
  - Diagnóstico de concorrência
  - Thread dump
---

# Padrões e diagnóstico de concorrência

> [!abstract] TL;DR
> Concorrência correta em Java combina **padrões de design** que evitam problemas na raiz com **ferramentas de diagnóstico** que identificam problemas em produção. Os padrões canônicos são: imutabilidade/confinement, producer-consumer com `BlockingQueue`, thread-local state, copy-on-write e guarded suspension. O diagnóstico começa com um **thread dump** (`jcmd <pid> Thread.print` ou `jstack <pid>`): estados RUNNABLE/BLOCKED/WAITING mapeiam diretamente a contention, deadlock e pool subdimensionado. A JVM detecta deadlocks automaticamente e os sinaliza no dump. Para análise temporal, **JFR + JDK Mission Control** revelam lock contention ao longo do tempo sem overhead significativo; o **async-profiler** gera flame graphs de lock. O cheatsheet de fechamento do galho mapeia cada primitiva (`synchronized`, `Lock`, atômicos, concurrent collections, `CompletableFuture`, virtual threads, structured concurrency) ao tipo de problema que resolve.

## O que é

Padrões de design concorrente são soluções comprovadas para problemas recorrentes de coordenação entre threads — formas de estruturar o código para que a ausência de bugs de concorrência seja uma propriedade do design, não de disciplina manual. Diagnóstico de concorrência é o conjunto de ferramentas e técnicas para identificar o que está errado quando o código já está em produção.

A distinção é importante: o design correto minimiza a necessidade de diagnóstico, mas sistemas reais herdam código legado, têm interações inesperadas e falham de formas que só aparecem sob carga. Um engenheiro senior precisa dos dois: prevenir pelo design e saber investigar quando necessário.

Este galho cobriu as primitivas individualmente (notas 03 a 15). Esta nota fecha o galho juntando os padrões de uso e as ferramentas de diagnóstico, e oferece o cheatsheet de "qual primitiva para qual problema".

## Por que importa

Bugs de concorrência têm três propriedades que os tornam especialmente perigosos:

1. **Não são reproduzíveis deterministicamente** — dependem de timing entre threads, que varia com carga, JIT warming, GC pauses e hardware. O bug que apareceu em produção às 3h da manhã pode não aparecer no ambiente de desenvolvimento.
2. **Falham silenciosamente** — race conditions não lançam exceção; simplesmente produzem dados corrompidos ou estados inconsistentes. Deadlocks aparecem como lentidão ou timeout, não como `NullPointerException`.
3. **Ferramentas erradas tornam o diagnóstico ineficaz** — tentar debugar contention sem thread dump, ou usar `System.out.println` para diagnosticar race condition, é contraproducente. As ferramentas certas revelam o problema em segundos; sem elas, horas de especulação não chegam a lugar algum.

Para entrevistas senior, a expectativa é que o candidato: (1) saiba escolher o padrão certo antes de escrever código, e (2) descreva como diagnosticaria um problema de concorrência em produção passo a passo, usando as ferramentas concretas da JVM.

## Como funciona

### Thread-safety por imutabilidade e confinement

O padrão mais simples de ser thread-safe é **não ter estado mutável compartilhado**. Há duas formas:

**Imutabilidade**: o objeto não pode mudar após a construção. Threads compartilham referências sem sincronização.

```java
// Record é imutável por padrão — campos são final implicitamente
public record PriceQuote(String symbol, BigDecimal price, Instant timestamp) {}

// Regras para imutabilidade manual:
// 1. Todos os campos final   2. Sem setters
// 3. Classe final            4. Defensive copy de coleções mutáveis
// 5. 'this' não escapa durante construção
public final class ImmutableConfig {
    private final List<String> hosts;
    public ImmutableConfig(List<String> hosts) {
        this.hosts = List.copyOf(hosts);  // defensive copy — imutável
    }
    public List<String> hosts() { return hosts; }
}
```

**Thread confinement**: o estado mutável existe, mas pertence a uma única thread. Variáveis locais são stack-confined automaticamente. `ThreadLocal` serve para estado que precisa persistir através de chamadas dentro da mesma thread.

### Producer-consumer com `BlockingQueue`

O padrão de producer-consumer desacopla produção de consumo via fila com backpressure natural. O `BlockingQueue` é a implementação idiomática em Java.

```java
BlockingQueue<WorkItem> queue = new ArrayBlockingQueue<>(500);  // bounded — backpressure

Runnable producer = () -> {
    try {
        while (!Thread.currentThread().isInterrupted()) {
            queue.put(generateNextItem());  // bloqueia se cheia — backpressure natural
        }
    } catch (InterruptedException e) { Thread.currentThread().interrupt(); }
};

Runnable consumer = () -> {
    try {
        while (!Thread.currentThread().isInterrupted()) {
            process(queue.take());  // bloqueia se vazia
        }
    } catch (InterruptedException e) { Thread.currentThread().interrupt(); }
};
```

Escolha da implementação:
- `ArrayBlockingQueue` — capacidade fixa, array circular; padrão quando o limite é conhecido
- `LinkedBlockingQueue` — dois locks separados para put/take (maior throughput); opcionalmente unbounded
- `SynchronousQueue` — capacidade zero; handoff direto produtor↔consumidor sem buffer

### Thread-local state

Quando o estado precisa ser mantido por thread mas não faz sentido como campo compartilhado, `ThreadLocal` isola uma cópia por thread.

```java
// Caso clássico: DateTimeFormatter não é thread-safe
private static final ThreadLocal<DateTimeFormatter> FORMATTER =
    ThreadLocal.withInitial(() -> DateTimeFormatter.ofPattern("yyyy-MM-dd"));

public String formatDate(LocalDate date) {
    try {
        return FORMATTER.get().format(date);
    } finally {
        FORMATTER.remove();  // obrigatório em thread pools para evitar leak
    }
}
```

> [!tip] Virtual Threads: prefira Scoped Values
> Com virtual threads (Java 21+), `ThreadLocal` cria uma cópia por virtual thread — com milhões delas, o footprint cresce. Para contexto propagado (user autenticado, trace ID), use `ScopedValue` (GA Java 25): imutável dentro do scope e sem risco de leak.

### Copy-on-write

Quando leituras são muito mais frequentes que escritas, o padrão copy-on-write elimina a sincronização no caminho de leitura: na escrita, cria-se uma nova cópia do dado; leitores veem o snapshot anterior (consistente) até a referência ser trocada.

```java
// Implementação pronta — CopyOnWriteArrayList
CopyOnWriteArrayList<EventListener> listeners = new CopyOnWriteArrayList<>();
listeners.add(listener);          // cópia O(n) — adequado para listas estáveis
listeners.forEach(l -> l.onEvent(e));  // lock-free, itera sobre snapshot imutável

// Implementação manual com volatile + synchronized no write
private volatile List<EventListener> listeners = List.of();

public synchronized void register(EventListener l) {
    List<EventListener> updated = new ArrayList<>(listeners);
    updated.add(l);
    listeners = List.copyOf(updated);  // troca atômica da referência
}

public void publish(Event event) {
    listeners.forEach(l -> l.onEvent(event));  // sem lock — lê snapshot imutável
}
```

> [!warning] Writes frequentes = O(n) por escrita
> `CopyOnWriteArrayList` copia o array inteiro a cada mutação. Ideal para listas de listeners/handlers que raramente mudam. Inadequado para estruturas com inserções frequentes.

### Guarded suspension

Quando uma thread precisa aguardar que uma condição se torne verdadeira antes de continuar, o padrão guarded suspension encapsula a espera com verificação da condição em loop.

```java
// Estrutura canônica com ReentrantLock + Condition
private final ReentrantLock lock = new ReentrantLock();
private final Condition ready = lock.newCondition();

public void waitUntilReady() throws InterruptedException {
    lock.lock();
    try {
        while (!conditionMet()) {  // SEMPRE loop — não if — por spurious wakeups
            ready.await();
        }
        // condição garantida aqui
    } finally {
        lock.unlock();
    }
}

public void setReady() {
    lock.lock();
    try {
        markConditionMet();
        ready.signalAll();
    } finally {
        lock.unlock();
    }
}
```

> [!note] Por que `while` e não `if`?
> Spurious wakeups: a JVM pode acordar uma thread em `await()` sem `signal()` — comportamento permitido pela especificação. O loop revalida a condição antes de prosseguir. Usar `if` introduz race condition sutil. `BlockingQueue` já implementa guarded suspension internamente — prefira-o ao implementar producer-consumer manualmente.

## Na prática

### Anatomia de um thread dump

Um thread dump é um snapshot de todas as threads JVM em um instante — seus estados, stack traces e locks. É a primeira ferramenta para diagnosticar qualquer problema de concorrência em produção.

**Como obter:**

```bash
# Recomendado (jcmd) — disponível desde Java 7
jcmd <pid> Thread.print

# Com informação estendida de locks java.util.concurrent
jcmd <pid> Thread.print -l

# Alternativa clássica
jstack <pid>

# Descobrir o PID
jps -l
```

**Estrutura de uma entrada de thread:**

```text
"http-nio-8080-exec-5" #42 daemon prio=5 os_prio=0 cpu=15.23ms elapsed=120.01s
   tid=0x00007f3e4c0c5000 nid=0x3e2a waiting for monitor entry [0x00007f3e3c0bb000]
   java.lang.Thread.State: BLOCKED (on object monitor)

        at com.example.service.ReportService.generate(ReportService.java:87)
        - waiting to lock <0x000000071b4c2d80> (a com.example.service.ReportService)
        at com.example.controller.ReportController.get(ReportController.java:44)
        ...
```

**Estados e o que significam:**

| Estado | Significado | Sintoma associado |
|--------|-------------|-------------------|
| `RUNNABLE` | Executando ou pronto para executar | CPU alta: verifique loops; stack trace indica o quê |
| `BLOCKED` | Aguardando adquirir um monitor lock (`synchronized`) | Lock contention — outro thread detém o lock |
| `WAITING` | Aguardando indefinidamente (`Object.wait`, `LockSupport.park`, `Thread.join`) | Pool subdimensionado, produtor lento, signal nunca chega |
| `TIMED_WAITING` | Aguardando com timeout (`Thread.sleep`, `Object.wait(timeout)`) | Normal em muitos casos; verifique se timeout é adequado |
| `TERMINATED` | Thread finalizada | — |

**Deadlock detectado automaticamente pela JVM:**

```text
Found one Java-level deadlock:
=============================
"worker-thread-2":
  waiting to lock monitor 0x000000071b4c2e80 (object 0x000000071b4c2e80, a java.lang.Object),
  which is held by "worker-thread-1"

"worker-thread-1":
  waiting to lock monitor 0x000000071b4c2d80 (object 0x000000071b4c2d80, a java.lang.Object),
  which is held by "worker-thread-2"

Java stack information for the threads listed above:
===================================================
"worker-thread-2":
        at com.example.TransferService.transferTo(TransferService.java:52)
        - waiting to lock <0x000000071b4c2e80> (a com.example.Account)
        - locked <0x000000071b4c2d80> (a com.example.Account)
        at com.example.TransferService.execute(TransferService.java:31)
"worker-thread-1":
        at com.example.TransferService.transferTo(TransferService.java:52)
        - waiting to lock <0x000000071b4c2d80> (a com.example.Account)
        - locked <0x000000071b4c2e80> (a com.example.Account)
        at com.example.TransferService.execute(TransferService.java:31)

Found 1 deadlock.
```

O dump mostra exatamente quem está esperando quem, qual lock está sendo esperado, e qual thread o detém. A seção `Found 1 deadlock.` é gerada automaticamente — para deadlocks via `java.util.concurrent.locks`, use `jstack -l` ou `jcmd Thread.print -l`.

### JFR + Mission Control

Java Flight Recorder é um profiler de baixo overhead integrado à JVM, disponível sem licença adicional desde Java 11. Captura eventos ao longo do tempo — ao contrário do thread dump, que é um snapshot.

```bash
# Iniciar gravação de 60 segundos
jcmd <pid> JFR.start duration=60s filename=/tmp/app-recording.jfr

# Verificar gravações ativas
jcmd <pid> JFR.check

# Fazer dump imediato (mesmo com gravação contínua)
jcmd <pid> JFR.dump filename=/tmp/app-now.jfr

# Parar gravação
jcmd <pid> JFR.stop

# Ou iniciar junto com a aplicação (útil para startup analysis)
java -XX:StartFlightRecording=duration=120s,filename=/tmp/startup.jfr -jar app.jar
```

No JDK Mission Control (`jmc`), a aba **Threads** mostra atividade de cada thread ao longo do tempo. A aba **Lock Instances** detalha quais locks causaram bloqueio, por quanto tempo, e quais threads estavam envolvidas. Eventos relevantes para concorrência:

- `jdk.ThreadBlocked` — thread entrou em BLOCKED; `jdk.JavaMonitorWait` — entrou em `Object.wait()`
- `jdk.JavaMonitorEnter` — tentou adquirir monitor lock; `jdk.ThreadPark` — fez `LockSupport.park()`

### `jcmd <pid> Thread.print`

Comando recomendado pela Oracle — mais seguro que `kill -3` (vai para stderr e pode ser perdido) e mais completo que `jstack`.

```bash
# Dump básico
jcmd <pid> Thread.print

# Com informação de locks java.util.concurrent (ReentrantLock, Semaphore, etc.)
jcmd <pid> Thread.print -l

# Com informação estendida (locks + heap stats por thread — mais lento)
jcmd <pid> Thread.print -l -e
```

Para deadlocks com `ReentrantLock` e outros locks `AbstractQueuedSynchronizer`-based, o `-l` é essencial — sem ele, apenas monitores intrínsecos (`synchronized`) aparecem.

### async-profiler para lock contention

O async-profiler é um profiler externo de baixo overhead que usa APIs de profiling da JVM para gerar flame graphs. Especialmente útil para contention de lock em produção, onde o overhead do profiler importa.

```bash
# Instalar e rodar (exemplo Linux)
./asprof -d 60 -e lock -f /tmp/lock-contention.html <pid>

# Flame graph de lock: identifica visualmente qual método
# concentra mais tempo em contenção de lock
```

O modo `-e lock` foca em eventos de lock — mostra quais métodos passam mais tempo aguardando monitores. Útil quando `jstack` revela muitas threads em BLOCKED mas não é óbvio qual parte do código é o gargalo.

### Sintomas → causa provável

| Sintoma no thread dump | Causa mais provável | Investigação |
|------------------------|--------------------|--------------| 
| Muitas threads `BLOCKED` no mesmo monitor | Lock contention — `synchronized` num método popular | Qual objeto é o monitor? Refatorar para lock mais granular ou estrutura lock-free |
| Muitas threads `WAITING` em `take()` | Fila vazia — produtor lento ou pool de workers grande demais para a vazão | Balancear produção/consumo; reduzir consumers |
| Muitas threads `WAITING` em `park()` | Pool de threads ocioso aguardando tasks | Normal se carga baixa; anormal se requests estão atrasados |
| Seção `Found N deadlock(s)` | Deadlock — ciclo de dependência entre locks | Corrigir ordem de aquisição; usar `tryLock` com timeout |
| Poucas threads `RUNNABLE` com CPU alta | Loop tight ou trabalho CPU-intensivo concentrado | Stack trace diz exatamente onde; avaliar parallelismo |
| Threads `RUNNABLE` em I/O nativo | Threads de plataforma aguardando I/O (normal com virtual threads: carrier liberado) | Com platform threads: verificar pool sizing |

## Armadilhas

### (1) `synchronized(this)` — expor o monitor ao código externo

**O problema:** quando um método usa `synchronized(this)`, o lock é o objeto `this` — que é acessível a qualquer código que tenha referência ao objeto. Código externo pode (acidentalmente ou não) sincronizar no mesmo monitor, criando deadlocks ou serialização inesperada.

```java
// PROBLEMA — qualquer código com referência ao Counter pode sincronizar nele
public class Counter {
    public synchronized void increment() { /* ... */ }
}

// Código externo — talvez em outra lib ou test framework
Counter counter = getCounter();
synchronized (counter) {  // bloqueia o mesmo monitor que increment() usa!
    // operação longa aqui — serializa todas as chamadas a increment()
    processInBatch(counter);
}
```

**Fix:** use um objeto de lock privado, final e dedicado. Código externo não tem acesso a ele.

```java
public class Counter {
    private final Object lock = new Object();  // privado, inacessível externamente
    private int count = 0;

    public void increment() {
        synchronized (lock) {
            count++;
        }
    }

    public int get() {
        synchronized (lock) {
            return count;
        }
    }
}
```

Mesma lógica vale para `synchronized` em método static: o lock é `Classe.class`, acessível via `Counter.class`. Prefira um `static final Object LOCK = new Object()` privado.

---

### (2) Diagnosticar contention sem thread dump — "chutar" a causa

**O problema:** tentar diagnosticar lentidão ou travamento em produção sem obter um thread dump primeiro. Equipes gastam horas revisando código, mudando parâmetros de pool e fazendo deploy sem entender o estado real da aplicação.

```text
Sintoma: aplicação ficou lenta repentinamente às 14h37.
Abordagem errada:
  - "Acho que é o banco, vou aumentar o connection pool"
  - "Deve ser o GC, vou mudar as flags"
  - Deploy de hotfix sem diagnóstico → problema volta ou piora

Abordagem correta:
  1. jcmd <pid> Thread.print -l > dump_14h37.txt
  2. Verificar: há seção "Found N deadlock(s)"?
  3. Muitas threads em BLOCKED? Em qual monitor?
  4. Muitas threads em WAITING? Esperando o quê?
  5. Diagnóstico em minutos — não horas de especulação
```

**Fix:** torne thread dumps reflexo pavloviano ante qualquer incidente de concorrência. São baratos (microssegundos de overhead), não requerem restart, e revelam o estado exato da aplicação no momento do problema. Salve com timestamp para análise post-mortem. Se o problema é intermitente, capture múltiplos dumps com 10-30 segundos de intervalo — padrões que aparecem em todos indicam o gargalo real.

---

### (3) Thread pool subdimensionado escondendo deadlock por exaustão

**O problema:** um deadlock lógico (dependência cíclica entre tasks) pode não aparecer como "deadlock detectado" no thread dump quando ocorre por exaustão de pool — todas as threads do pool estão ocupadas esperando resultados de tasks que nunca serão executadas porque o pool está cheio.

```java
// PROBLEMA — deadlock por exaustão de pool
ExecutorService pool = Executors.newFixedThreadPool(5);

// Task A submete Task B e aguarda seu resultado
// Se todas as 5 threads estiverem executando Task A,
// Task B nunca consegue uma thread para executar
// → todas as 5 threads ficam em WAITING indefinidamente
pool.submit(() -> {
    Future<String> inner = pool.submit(() -> fetchData());  // ← Task B
    return inner.get();  // ← Task A aguarda Task B, mas pool está saturado
});
```

O thread dump mostrará as threads em `WAITING` em `Future.get()`, mas *não* haverá seção de deadlock — a JVM não detecta esse padrão porque não é deadlock de monitor.

**Fix:** nunca submeta tasks que aguardam resultados de outras tasks para o mesmo pool limitado. Use pools separados para tasks com dependência hierárquica, ou use `CompletableFuture` com encadeamento (não blocking get), ou use virtual threads (onde o bloqueio libera o carrier, sem esgotar o pool).

## Em entrevista

### Frase pronta (inglês)

> "When diagnosing a concurrency issue in production, my first step is always a thread dump — either `jcmd <pid> Thread.print -l` or `jstack <pid>`. The thread states tell the story immediately: a cluster of threads in BLOCKED on the same monitor means lock contention; threads in WAITING on `take()` mean the producer is slower than the consumers; and the JVM will call out deadlocks explicitly in the dump with a 'Found N deadlock(s)' section. For time-series analysis — identifying which lock causes the most contention over time — I use Java Flight Recorder via `jcmd JFR.start` and analyze in JDK Mission Control. On the design side, my default hierarchy is: immutability first, then thread confinement, then lock-free structures like `ConcurrentHashMap` and atomics, then explicit synchronization only when compound operations require it. I reach for `BlockingQueue`-based producer-consumer when I need to decouple production from consumption with natural backpressure, and `CompletableFuture` for fan-out over multiple async calls with timeout."

### Vocabulário

| Termo PT | Termo EN |
|----------|----------|
| despejo de threads | thread dump |
| contenção de lock | lock contention |
| impasse | deadlock |
| exaustão de pool | thread pool exhaustion |
| padrão produtor-consumidor | producer-consumer pattern |
| confinamento de thread | thread confinement |
| suspensão guardada | guarded suspension |
| estado BLOQUEADO | BLOCKED state |
| estado EM ESPERA | WAITING state |
| gravação de voo Java | Java Flight Recorder (JFR) |
| profiler de chama | flame graph / async-profiler |
| monitor intrínseco | intrinsic monitor |

### Cheatsheet

Fechamento do galho: qual primitiva escolher para qual problema.

| Problema | Solução preferida | Por que |
|----------|-------------------|---------|
| Objeto compartilhado que não muda | Imutabilidade (`record`, campos `final`) | Zero overhead, trivialmente thread-safe |
| Contador de alta contenção (muitas threads incrementando) | `LongAdder` / `AtomicLong` | Lock-free via CAS; `LongAdder` escala melhor sob contenção |
| Referência atômica com CAS | `AtomicReference` | Troca atômica sem lock |
| Map compartilhado | `ConcurrentHashMap` | Lock granular por bucket; reads lock-free |
| Lista lida constantemente, raramente modificada | `CopyOnWriteArrayList` | Reads lock-free; writes criam cópia (só para listas pequenas e estáveis) |
| Seção crítica simples (compound read-modify-write) | `synchronized` (bloco com lock privado) | Simples, reentrante, adequado para baixa contenção |
| Seção crítica com timeout ou interrupção | `ReentrantLock` | `tryLock`, `lockInterruptibly`, fair mode |
| Cache read-heavy com writes raros | `ReadWriteLock` / `StampedLock` | Múltiplos readers simultâneos; `StampedLock` tem optimistic read |
| Desacoplar produção de consumo com backpressure | `BlockingQueue` + producer-consumer | `put` bloqueia se cheia; `take` bloqueia se vazia — backpressure automático |
| Composição de operações assíncronas | `CompletableFuture` | Pipeline declarativo; `allOf` para fan-in; `orTimeout` para SLA |
| I/O-bound em alta concorrência | Virtual Threads (`Executors.newVirtualThreadPerTaskExecutor()`) | Milhões de threads leves; código síncrono simples |
| Grupo de tasks com ciclo de vida compartilhado | Structured Concurrency (`StructuredTaskScope`) | Cancelamento automático; error propagation; sem task orphans (GA Java 25) |
| Contexto imutável por scope de execução | `ScopedValue` | Imutável, sem leak, eficiente com virtual threads (GA Java 25) |

## Veja também

- [[03 - Exclusão mútua com synchronized]]
- [[04 - As armadilhas - race, deadlock e companhia]]
- [[08 - Executors e thread pools]]
- [[11 - Java Memory Model em profundidade]]
- [[03-Dominios/Java/Concorrência e paralelismo/index|MOC do galho]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[Java Concurrency]]
- [[03-Dominios/Java/Dicionário de Java#Contention|contention]]
- [[03-Dominios/Java/Dicionário de Java#Deadlock|deadlock]]

## Referências

- [Troubleshooting Guide — Oracle JDK 21](https://docs.oracle.com/en/java/javase/21/troubleshoot/diagnostic-tools.html) — jcmd Thread.print, jstack, thread dump analysis
- [Java Flight Recorder — jcmd JFR commands](https://docs.oracle.com/en/java/javase/21/troubleshoot/diagnostic-tools.html#GUID-0C6F4CD4-C9D7-4C5B-88D0-FB7DDC9EBD4E) — JFR via linha de comando
- [JDK Mission Control](https://adoptopenjdk.net/jmc.html) — análise de gravações JFR
- *Java Concurrency in Practice* — Brian Goetz et al. (cap. 10: Avoiding Liveness Hazards; cap. 11: Performance and Scalability)
- [async-profiler](https://github.com/async-profiler/async-profiler) — flame graphs de lock contention, CPU e alocação
- [java.util.concurrent — Java 21 API](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/package-summary.html) — referência completa das primitivas
