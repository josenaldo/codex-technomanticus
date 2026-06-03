---
title: "Locks explícitos"
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
  - locks
  - reentrantlock
aliases:
  - ReentrantLock
  - Locks explícitos
  - StampedLock
---

# Locks explícitos

> [!abstract] TL;DR
> **Locks explícitos** (`java.util.concurrent.locks`) são a alternativa programática ao `synchronized` — mais verbosos, porém significativamente mais flexíveis. `ReentrantLock` oferece `tryLock` com timeout, interruptibilidade e modo justo (FIFO). `ReadWriteLock` / `ReentrantReadWriteLock` permite múltiplos leitores simultâneos com escrita exclusiva — ideal para caches read-heavy. `StampedLock` (Java 8+) vai além com **optimistic read**: tenta ler sem adquirir nenhum lock e valida depois; é mais rápido sob pouca contenção de escrita, mas **não é reentrante** — reentrar na mesma thread causa deadlock imediato. `Condition` substitui `wait`/`notify` com precisão cirúrgica: múltiplas filas de espera por objeto, sem depender do monitor intrínseco. A escolha entre `synchronized` e `Lock` depende de necessidade real: se `tryLock`, timeout, fairness ou interruptibilidade não são necessários, `synchronized` vence pela simplicidade.

## O que é

`java.util.concurrent.locks` é o pacote do Java que oferece implementações de lock **programáticas** — adquiridas e liberadas explicitamente no código, ao contrário do `synchronized`, que opera via sintaxe da linguagem e blocos delimitados por chaves.

A interface central é `Lock`:

```java
public interface Lock {
    void lock();
    void lockInterruptibly() throws InterruptedException;
    boolean tryLock();
    boolean tryLock(long time, TimeUnit unit) throws InterruptedException;
    void unlock();
    Condition newCondition();
}
```

Toda implementação dessa hierarquia é construída sobre o **AbstractQueuedSynchronizer (AQS)** — uma fila interna de threads bloqueadas gerenciada com operações CAS. É a espinha dorsal de `ReentrantLock`, `ReadWriteLock`, `Semaphore` e `CountDownLatch`.

## Por que importa

### `synchronized` vs `Lock` — comparação justa

`synchronized` continua sendo a escolha certa para a maioria dos casos. Mas há situações em que `Lock` é indispensável:

| Capacidade | `synchronized` | `ReentrantLock` |
|---|---|---|
| Sintaxe | Bloco delimitado, automático | `lock()` / `unlock()` manual |
| Reentrância | Sim | Sim |
| `tryLock` (sem bloquear) | Não | Sim |
| Timeout no lock | Não | Sim (`tryLock(n, unit)`) |
| Interruptível | Não | Sim (`lockInterruptibly()`) |
| Modo justo (FIFO) | Não | Sim (`new ReentrantLock(true)`) |
| Múltiplas conditions | Não (só um wait-set) | Sim (`newCondition()`) |
| Leitores simultâneos | Não | Via `ReadWriteLock` |
| Legibilidade | Alta | Média (mais verboso) |
| Risco de lock vazado | Zero (compilador garante) | Alto (requer `finally`) |

**Quando `synchronized` vence:** o caso é simples, sem necessidade de timeout ou interrupção, e a legibilidade importa. `synchronized` é intrínseco à JVM, mais fácil de revisar e não apresenta o risco de esquecer o `unlock`.

**Quando `Lock` vence:** você precisa de `tryLock` para evitar deadlock; quer timeout para implementar circuit breaker; precisa que a thread seja interrompível enquanto aguarda; ou quer fairness para evitar starvation de threads esperando há muito tempo.

> [!tip] Regra prática
> Comece com `synchronized`. Migre para `ReentrantLock` quando uma dessas capacidades for concretamente necessária — não por antecipação.

## Como funciona

### `Lock` e `ReentrantLock`

`ReentrantLock` é a implementação padrão de `Lock`. Reentrante: a mesma thread pode adquirir o lock múltiplas vezes sem deadlock (precisa liberar o mesmo número de vezes).

**Padrão canônico — sempre `unlock()` no `finally`:**

```java
private final ReentrantLock lock = new ReentrantLock();

public void processar() {
    lock.lock();
    try {
        // seção crítica
        executarLogica();
    } finally {
        lock.unlock();  // garante liberação mesmo com exceção
    }
}
```

**`tryLock` — não bloqueia:**

```java
// Retorna true imediatamente se disponível, false se ocupado
if (lock.tryLock()) {
    try {
        atualizarRecurso();
    } finally {
        lock.unlock();
    }
} else {
    // fallback: recurso ocupado, tente depois
    registrarTentativaFalha();
}
```

**`tryLock` com timeout:**

```java
// Espera até 500ms; útil para evitar deadlock com retry
if (lock.tryLock(500, TimeUnit.MILLISECONDS)) {
    try {
        processar();
    } finally {
        lock.unlock();
    }
} else {
    throw new TimeoutException("Lock não obtido em 500ms");
}
```

**`lockInterruptibly` — interrompível; modo justo (fairness):**

```java
// Se interrompida enquanto espera, lança InterruptedException
lock.lockInterruptibly();  // útil para cancelamento cooperativo
// sempre restaurar: Thread.currentThread().interrupt() no catch

// Threads atendidas em ordem FIFO — elimina starvation, reduz throughput
Lock lockJusto = new ReentrantLock(true);  // (ver Armadilhas sobre custo)
```

---

### `ReadWriteLock`

`ReadWriteLock` separa os acessos em dois locks: **múltiplos leitores** podem atuar simultaneamente; **um único escritor** exige exclusividade total. A implementação padrão é `ReentrantReadWriteLock` (reentrante em ambos os modos).

```java
private final ReentrantReadWriteLock rwl = new ReentrantReadWriteLock();
// rwl.readLock()  — adquirido por leitores (concorrente)
// rwl.writeLock() — adquirido por escritores (exclusivo)
```

**Quando vale a pena:** proporção leitura/escrita muito alta — ex.: catálogo de configuração lido a cada request, atualizado de hora em hora. Se escritas são frequentes, o overhead do segundo lock anula o ganho.

> [!warning] Downgrade de lock
> `ReentrantReadWriteLock` suporta **downgrade** (write → read): adquirir readLock enquanto ainda segura writeLock, depois liberar o write. O sentido inverso (upgrade de read → write) não é suportado e causa deadlock.

---

### `StampedLock`

Introduzido no Java 8, `StampedLock` oferece três modos de operação e usa um **stamp** (long) como token de acesso. É mais performático que `ReadWriteLock` em cenários de leitura intensiva, graças ao **optimistic read**.

**Diferença crítica:** `StampedLock` **não é reentrante**. Tentar readquirir o lock da mesma thread (mesmo modo) causa deadlock imediato.

**Os três modos:**

| Modo | Método de aquisição | Bloqueante? | Exclusivo? |
|---|---|---|---|
| Write | `writeLock()` | Sim | Sim |
| Read | `readLock()` | Sim (se escritor ativo) | Não |
| Optimistic read | `tryOptimisticRead()` | Nunca | Não — apenas observa |

**Optimistic read — o diferencial:**

`tryOptimisticRead()` retorna um stamp **sem adquirir nenhum lock**. Você lê os dados e chama `validate(stamp)` para verificar se nenhum escritor modificou os dados durante a leitura. Se a validação falhar, faz fallback para um read lock real.

```java
// hipotético: ponto em espaço 2D compartilhado entre threads
private final StampedLock sl = new StampedLock();
private double x, y;

public double distanciaOrigem() {
    long stamp = sl.tryOptimisticRead();  // sem bloquear
    double cx = x;
    double cy = y;
    if (!sl.validate(stamp)) {           // alguém escreveu no intervalo?
        stamp = sl.readLock();           // fallback: adquire read lock real
        try {
            cx = x;
            cy = y;
        } finally {
            sl.unlockRead(stamp);
        }
    }
    return Math.hypot(cx, cy);
}

public void mover(double dx, double dy) {
    long stamp = sl.writeLock();
    try {
        x += dx;
        y += dy;
    } finally {
        sl.unlockWrite(stamp);
    }
}
```

---

### `Condition`

`Condition` é o substituto moderno de `Object.wait()` / `notify()` / `notifyAll()`. Obtida via `lock.newCondition()`, permite **múltiplas filas de espera** (wait-sets) associadas a um mesmo lock — enquanto `synchronized` tem apenas uma fila por monitor. Outros ganhos: timeout em nanosegundos (`awaitNanos`), versão não interruptível (`awaitUninterruptibly`), e `signal()` que acorda exclusivamente a fila desejada.

**Exemplo — buffer bounded (produtor/consumidor):**

```java
// hipotético: buffer circular com duas filas de espera distintas
private final ReentrantLock lock    = new ReentrantLock();
private final Condition naoCheia   = lock.newCondition();  // produtores aguardam aqui
private final Condition naoVazia   = lock.newCondition();  // consumidores aguardam aqui
private final Object[] itens = new Object[10];
private int count, putIdx, takeIdx;

public void produzir(Object item) throws InterruptedException {
    lock.lock();
    try {
        while (count == itens.length) naoCheia.await();  // await em while (spurious wakeups)
        itens[putIdx] = item;
        putIdx = (putIdx + 1) % itens.length;
        count++;
        naoVazia.signal();   // acorda UM consumidor — não todos
    } finally { lock.unlock(); }
}

public Object consumir() throws InterruptedException {
    lock.lock();
    try {
        while (count == 0) naoVazia.await();
        Object item = itens[takeIdx];
        takeIdx = (takeIdx + 1) % itens.length;
        count--;
        naoCheia.signal();   // acorda UM produtor
        return item;
    } finally { lock.unlock(); }
}
```

Com `notifyAll` em monitor único, todos os produtores e consumidores acordariam juntos — contenção desnecessária. `Condition` notifica a fila exata.

> [!warning] `await` sempre em loop
> Assim como `Object.wait()`, `Condition.await()` está sujeito a **spurious wakeups**. Sempre verifique a condição em um `while`, nunca em um `if`.

## Na prática

### Cache com `ReadWriteLock`

```java
// hipotético: cache de configurações — muitas leituras, atualização periódica
private final ReadWriteLock rwl   = new ReentrantReadWriteLock();
private final Lock leitura        = rwl.readLock();
private final Lock escrita        = rwl.writeLock();
private Map<String, String> dados = new HashMap<>();

public String obter(String chave) {
    leitura.lock();
    try { return dados.get(chave); }
    finally { leitura.unlock(); }
}

public void recarregar(Map<String, String> novosDados) {
    escrita.lock();
    try { dados = new HashMap<>(novosDados); }
    finally { escrita.unlock(); }
}
```

Funciona bem com proporção leitura/escrita alta — centenas de leituras por segundo, recarregamento periódico.

---

### Optimistic read com `StampedLock`

O padrão `tryOptimisticRead → leitura → validate → fallback readLock` (mostrado em "Como funciona") aplica-se diretamente a qualquer estrutura lida com alta frequência e atualizada raramente: contadores de telemetria, snapshots de configuração, coordenadas geométricas. O caminho quente não adquire nenhum lock — apenas valida um contador de versão interno. A degradação para read lock real só ocorre quando um escritor atualiza durante a leitura.

## Armadilhas

### (1) Esquecer `unlock()` fora do `finally` — lock vazado em exceção

**O problema:** diferente de `synchronized`, `ReentrantLock` não é liberado automaticamente quando uma exceção é lançada. Se `unlock()` não estiver em um bloco `finally`, qualquer exceção no caminho crítico deixa o lock adquirido para sempre — a thread termina, o lock nunca é liberado, e todas as threads que tentarem adquiri-lo ficam bloqueadas indefinidamente.

```java
// RUIM — lock vazado se processarDados() lançar exceção
public void processar() {
    lock.lock();
    processarDados();   // lança RuntimeException
    lock.unlock();      // nunca executado!
}
```

```java
// FIX — unlock sempre no finally
public void processar() {
    lock.lock();
    try {
        processarDados();
    } finally {
        lock.unlock();  // executado mesmo com exceção
    }
}
```

> [!danger] Esta é a armadilha mais comum com locks explícitos. Em code review, qualquer `lock.lock()` sem `try/finally` imediato é um red flag.

---

### (2) Tratar `StampedLock` como reentrante — deadlock imediato

**O problema:** `StampedLock` **não é reentrante**. Se a mesma thread tenta readquirir o lock (em qualquer modo) enquanto já o detém, ela se bloqueia esperando por ela mesma — deadlock.

```java
// RUIM — deadlock: mesma thread tenta adquirir readLock duas vezes
private final StampedLock sl = new StampedLock();

public void operacaoExterna() {
    long stamp = sl.readLock();
    try {
        operacaoInterna();   // chama método que também adquire readLock
    } finally {
        sl.unlockRead(stamp);
    }
}

private void operacaoInterna() {
    long stamp = sl.readLock();  // DEADLOCK — thread já segura readLock
    try {
        // ...
    } finally {
        sl.unlockRead(stamp);
    }
}
```

```java
// FIX — opção 1: passar o stamp para métodos internos
private void operacaoInterna(long stamp) {
    // usa dados já protegidos pelo stamp externo
}

// FIX — opção 2: usar ReentrantReadWriteLock se reentrância é necessária
private final ReadWriteLock rwl = new ReentrantReadWriteLock();
```

> [!warning] A Oracle documenta explicitamente: "They are not reentrant, so locked bodies should not call other unknown methods that may try to re-acquire locks."

---

### (3) Fairness matando throughput

**O problema:** `new ReentrantLock(true)` garante ordem FIFO, eliminando starvation. Porém, fairness tem um custo real: threads não podem "pular a fila" mesmo que o lock esteja disponível, o que reduz throughput significativamente em cenários de alta contenção.

```java
// RUIM em cenários de alta contenção — throughput pode cair 5-10x
private final Lock lock = new ReentrantLock(true);  // fairness sem necessidade real

// Múltiplas threads em loop:
lock.lock();
try {
    contagem++;
} finally {
    lock.unlock();
}
```

```java
// FIX — usar fairness só quando starvation é um problema real e verificado
// Na maioria dos casos, o lock non-fair (padrão) distribui de forma suficientemente justa

Lock lock = new ReentrantLock();         // non-fair: maior throughput
Lock lockJusto = new ReentrantLock(true); // fair: use apenas quando starvation é documentado
```

Fairness resolve starvation, mas em sistemas onde o throughput é crítico e starvation não ocorre na prática, é um custo desnecessário. Meça antes de ativar.

## Em entrevista

### Frase pronta (inglês)

> "The main trade-off between `synchronized` and explicit locks like `ReentrantLock` is capability versus simplicity: `synchronized` is less error-prone because the compiler guarantees the lock is always released, but it offers no way to attempt a lock without blocking, set a timeout, or respond to interruption." "I reach for `ReentrantLock` when I specifically need `tryLock` to avoid deadlock in lock-ordering scenarios, or `lockInterruptibly` for threads that need cooperative cancellation, or fair mode when starvation of long-waiting threads is a measured problem — not by default." "The important caveat with `StampedLock` is that it is not reentrant: if a method holding a `StampedLock` calls another method that tries to reacquire the same lock on the same thread, you get an immediate deadlock, which is a much harder bug to track down than a simple race condition."

### Vocabulário

| Termo PT | Termo EN |
|---|---|
| lock explícito | explicit lock |
| lock reentrante | reentrant lock |
| modo justo / fairness | fair mode / fairness |
| leitura otimista | optimistic read |
| validação de stamp | stamp validation |
| fila de espera | wait-set / condition queue |
| lock de leitura | read lock |
| lock de escrita | write lock |
| contenção de lock | lock contention |
| lock vazado | leaked lock / lock not released |
| inanição de thread | thread starvation |
| downgrade de lock | lock downgrade |

## Veja também

- [[03 - Exclusão mútua com synchronized]]
- [[06 - Atômicos e operações lock-free]]
- [[04 - As armadilhas - race, deadlock e companhia]]
- [[03-Dominios/Java/Concorrência e paralelismo/index|MOC do galho]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[Java Concurrency]]
- [[03-Dominios/Java/Dicionário de Java#Synchronized|synchronized]]

## Referências

- [StampedLock — Java 21 API (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/locks/StampedLock.html)
- [ReentrantLock — Java 21 API (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/locks/ReentrantLock.html)
- [ReentrantReadWriteLock — Java 21 API (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/locks/ReentrantReadWriteLock.html)
- [Condition — Java 21 API (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/locks/Condition.html)
- [java.util.concurrent.locks — package summary (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/locks/package-summary.html)
- GOETZ, Brian et al. *Java Concurrency in Practice*. Addison-Wesley, 2006. Cap. 13 (Explicit Locks).
