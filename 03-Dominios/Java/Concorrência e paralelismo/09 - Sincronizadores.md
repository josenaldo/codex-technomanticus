---
title: "Sincronizadores"
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
  - sincronizadores
  - semaphore
aliases:
  - CountDownLatch
  - Semaphore
  - CyclicBarrier
---

# Sincronizadores

> [!abstract] TL;DR
> **Sincronizadores** são primitivas de coordenação de `java.util.concurrent` que permitem que threads aguardem umas às outras ou controlem acesso a recursos — sem precisar de `wait/notify` manual. `CountDownLatch` é **one-shot**: uma ou mais threads esperam que N eventos aconteçam e não pode ser reiniciado. `CyclicBarrier` é **reutilizável**: N threads se esperam mutuamente num ponto de encontro e o ciclo recomeça automaticamente. `Semaphore` limita quantas threads acessam um recurso simultaneamente com um contador de _permits_. `Phaser` generaliza os dois anteriores com registro dinâmico de participantes e múltiplas fases. `Exchanger` faz handoff síncrono de objetos entre exatamente duas threads. Escolher o sincronizador certo elimina a necessidade de lógica frágil de `wait/notify` e torna a intenção de coordenação explícita no código.

## O que é

**Sincronizadores** são classes do pacote `java.util.concurrent` que orquestram a coordenação entre threads além do que locks e variáveis atômicas oferecem. Enquanto `synchronized` e `ReentrantLock` protegem seções críticas e `AtomicInteger` garante operações atômicas, sincronizadores endereçam um problema diferente: **fazer threads esperarem umas às outras atingirem determinados estados antes de prosseguir**.

Os cinco principais sincronizadores da JDK são:

| Classe | Quem espera quem | Reutilizável? |
|---|---|---|
| `CountDownLatch` | 1 (ou N) thread(s) esperam N eventos | Não (one-shot) |
| `CyclicBarrier` | N threads esperam umas às outras | Sim (automático) |
| `Semaphore` | Thread espera um _permit_ disponível | Sim (permits são devolvidos) |
| `Phaser` | Registro dinâmico de partes, múltiplas fases | Sim |
| `Exchanger` | 2 threads trocam um objeto entre si | Sim |

Todos estão disponíveis desde Java 5 (`Phaser` desde Java 7).

## Por que importa

Coordenar threads com `Object.wait()` e `notifyAll()` é trabalhoso, propenso a erros e dificulta a leitura: é necessário gerenciar o monitor manualmente, lembrar de colocar o `wait()` dentro de um loop (spurious wakeups), e garantir que `notify` ocorra depois do `wait`. Sincronizadores encapsulam esses padrões em APIs com semântica clara:

- `countDown()` é muito mais legível do que "decrementar uma variável compartilhada e notificar"
- `semaphore.acquire()` comunica intenção melhor do que um `synchronized` com contador manual
- `barrier.await()` torna explícito que a thread espera as demais chegarem ao mesmo ponto

Em entrevistas, dominar a distinção entre one-shot vs reutilizável e saber quando cada primitiva se aplica é o que diferencia quem conhece `java.util.concurrent` de quem apenas sabe que ele existe.

## Como funciona

### `CountDownLatch` (one-shot, espera N eventos)

`CountDownLatch` é inicializado com um contador inteiro `count`. Threads chamam `countDown()` para decrementar o contador; outras threads chamam `await()` para bloquear até que o contador chegue a zero. Quando zero é atingido, **todas as threads em `await()` são liberadas imediatamente** e qualquer chamada subsequente a `await()` retorna sem bloquear.

**O contador não pode ser reiniciado.** Uma vez zerado, o latch está esgotado — essa é a característica one-shot. Para um comportamento reutilizável, use `CyclicBarrier`.

```java
// Esperar 3 serviços inicializarem antes de aceitar tráfego
CountDownLatch startGate = new CountDownLatch(3);

executor.submit(() -> { initDatabase();  startGate.countDown(); });
executor.submit(() -> { initCache();     startGate.countDown(); });
executor.submit(() -> { initMessaging(); startGate.countDown(); });

// Thread principal bloqueia até os 3 finalizarem
boolean ok = startGate.await(30, TimeUnit.SECONDS);
if (!ok) throw new TimeoutException("Serviços não inicializaram em 30s");
// a partir daqui, os 3 serviços estão prontos
```

Métodos principais:
- `CountDownLatch(int count)` — construtor; lança `IllegalArgumentException` se `count < 0`
- `void countDown()` — decrementa; se já era zero, não faz nada
- `void await()` — bloqueia até `count == 0`; lança `InterruptedException`
- `boolean await(long timeout, TimeUnit unit)` — retorna `true` se zero atingido, `false` se timeout

---

### `CyclicBarrier` (reutilizável, N threads se esperam + barrier action)

`CyclicBarrier` coordena N threads que devem se encontrar num ponto comum antes de prosseguir. Cada thread chama `await()`; a última a chegar libera todas. Diferentemente do latch, **a barreira se reinicia automaticamente** após cada ciclo — daí o adjetivo "cyclic".

O construtor aceita um `Runnable` opcional (barrier action) que é executado pela **última thread a chegar**, antes de qualquer thread ser liberada. É útil para consolidar resultados parciais.

```java
// Simulação de processamento em fases: 3 workers sincronizam entre cada fase
CyclicBarrier barrier = new CyclicBarrier(3, () ->
    System.out.println("Fase concluída — combinando resultados"));

for (int i = 0; i < 3; i++) {
    executor.submit(() -> {
        calcularFase1();
        barrier.await();   // espera todas as 3 threads
        calcularFase2();
        barrier.await();   // reutiliza a barreira no 2º ciclo
        calcularFase3();
        barrier.await();   // 3º ciclo
    });
}
```

O `await()` retorna o índice de chegada (`0` para a última thread a chegar, `parties-1` para a primeira). Se uma thread for interrompida ou expirar antes de todas chegarem, a barreira entra em **estado quebrado** (_broken_) e todas as threads aguardando (e futuras) recebem `BrokenBarrierException`.

Métodos principais:
- `CyclicBarrier(int parties)` e `CyclicBarrier(int parties, Runnable barrierAction)`
- `int await()` — lança `InterruptedException`, `BrokenBarrierException`
- `int await(long timeout, TimeUnit unit)` — lança também `TimeoutException`
- `void reset()` — reinicia forçadamente; threads aguardando recebem `BrokenBarrierException`
- `boolean isBroken()` — verifica se a barreira está em estado quebrado

---

### `Semaphore` (N permits, recurso limitado)

`Semaphore` mantém um contador de _permits_ (permissões). Uma thread chama `acquire()` para obter um permit — bloqueando se nenhum estiver disponível — e `release()` para devolvê-lo, potencialmente liberando outra thread. Não há noção de "dono" do permit: qualquer thread pode chamar `release()`, inclusive sem ter chamado `acquire()` antes.

```java
// Limitar a 5 chamadas simultâneas a um serviço externo
Semaphore semaphore = new Semaphore(5);

public Response chamarServico(Request req) throws InterruptedException {
    semaphore.acquire();
    try {
        return servicoExterno.enviar(req);
    } finally {
        semaphore.release();  // SEMPRE no finally — ver Armadilhas
    }
}
```

O modo `fair` (segundo argumento booleano no construtor) garante ordem FIFO entre as threads aguardando — previne starvation ao custo de menor throughput.

Métodos principais:
- `Semaphore(int permits)` e `Semaphore(int permits, boolean fair)`
- `void acquire()` — bloqueia se `permits == 0`; lança `InterruptedException`
- `void acquireUninterruptibly()` — idêntico mas ignora interrupção
- `boolean tryAcquire()` — retorna `false` imediatamente se sem permits (não bloqueia)
- `boolean tryAcquire(long timeout, TimeUnit unit)`
- `void release()` — devolve 1 permit
- `void release(int permits)` — devolve N permits

---

### `Phaser` (fases dinâmicas)

`Phaser` combina `CountDownLatch` e `CyclicBarrier`, adicionando duas características que os outros não têm: **número de participantes configurável dinamicamente** (threads podem entrar e sair) e **controle de terminação via hook `onAdvance()`**. O número de fase (`getPhase()`) avança automaticamente a cada ciclo.

```java
Phaser phaser = new Phaser(3);  // 3 participantes iniciais

for (int i = 0; i < 3; i++) {
    executor.submit(() -> {
        processarFase1();
        phaser.arriveAndAwaitAdvance();  // sincroniza; fase avança para 1
        processarFase2();
        phaser.arriveAndAwaitAdvance();  // fase avança para 2
        phaser.arriveAndDeregister();    // saindo do grupo
    });
}
```

Para controlar quantas iterações ocorrem, sobrescreva `onAdvance()`:

```java
Phaser phaser = new Phaser(workers) {
    @Override
    protected boolean onAdvance(int phase, int registeredParties) {
        return phase >= 2 || registeredParties == 0;  // termina após fase 2
    }
};
```

O `Phaser` também suporta hierarquia de phasers para reduzir contenção com muitos participantes. Limite documentado: 65.535 participantes por instância.

Métodos principais:
- `int arriveAndAwaitAdvance()` — chega e aguarda os demais; retorna o número da nova fase
- `int arriveAndDeregister()` — chega e remove-se do grupo
- `int arrive()` — registra chegada sem bloquear
- `int register()` / `int bulkRegister(int parties)` — adiciona participantes
- `boolean isTerminated()` / `void forceTermination()`

---

### `Exchanger` (troca entre 2 threads)

`Exchanger<V>` é um ponto de rendez-vous onde exatamente duas threads trocam objetos. A primeira thread a chamar `exchange(obj)` bloqueia até que uma segunda thread também chame `exchange(outrObj)`, momento em que ambas recebem o objeto da outra. Pode ser visto como um `SynchronousQueue` bidirecional.

```java
Exchanger<byte[]> exchanger = new Exchanger<>();

// Thread produtora — preenche buffer e o troca por um vazio
executor.submit(() -> {
    byte[] buffer = new byte[1024];
    while (true) {
        preencher(buffer);
        buffer = exchanger.exchange(buffer);  // entrega cheio, recebe vazio
    }
});

// Thread consumidora — processa buffer e o troca por um vazio
executor.submit(() -> {
    byte[] buffer = new byte[1024];
    while (true) {
        buffer = exchanger.exchange(buffer);  // entrega vazio, recebe cheio
        consumir(buffer);
    }
});
```

Se apenas uma thread chamar `exchange()`, ela bloqueia indefinidamente até que a segunda chegue (ou seja interrompida). A versão com timeout — `exchange(obj, timeout, TimeUnit)` — lança `TimeoutException` se a parceira não aparecer a tempo.

---

### Tabela: latch vs barrier vs semaphore — quando usar

| Critério | `CountDownLatch` | `CyclicBarrier` | `Semaphore` |
|---|---|---|---|
| **Quantas threads esperam?** | 1 (ou N) esperam N eventos | N threads esperam umas às outras | Qualquer número, até N simultâneas |
| **Reutilizável?** | Não (one-shot) | Sim (automático) | Sim (acquire/release) |
| **Quem decrementa/sinaliza?** | Qualquer thread (countDown) | As próprias N threads (await) | Thread que libera (release) |
| **Caso de uso clássico** | Aguardar inicialização / fim de batch | Sincronizar fases de um algoritmo | Rate limiting, pool de recursos |
| **Barrier action (callback)?** | Não | Sim | Não |
| **Quando N não é fixo?** | Reiniciar: não dá; use Phaser | Reiniciar: use reset(); N fixo | N fixo nos permits; tryAcquire para não-bloqueante |

## Na prática

### Startup gate com `CountDownLatch`

Um padrão comum em aplicações com múltiplos componentes: o servidor não abre conexões até que todos os subsistemas estejam prontos. O latch garante que a thread principal não prossegue antes de todos os inits terminarem.

```java
public class Aplicacao {
    private final CountDownLatch prontoGate = new CountDownLatch(3);

    public void inicializar(ExecutorService executor) {
        executor.submit(() -> { bancoConexao.start();   prontoGate.countDown(); });
        executor.submit(() -> { cacheCliente.connect(); prontoGate.countDown(); });
        executor.submit(() -> { filaConsumer.start();   prontoGate.countDown(); });
    }

    public void aguardarPronto() throws InterruptedException, TimeoutException {
        boolean ok = prontoGate.await(60, TimeUnit.SECONDS);
        if (!ok) throw new TimeoutException("Inicialização ultrapassou 60s");
    }
}
```

Após `prontoGate.await()` retornar `true`, qualquer chamada futura a `await()` retorna imediatamente — o latch age como uma trava permanentemente aberta.

---

### Rate limiting com `Semaphore`

Semaphore é a forma idiomática de limitar chamadas simultâneas a recursos externos (APIs de terceiros, conexões de banco legadas sem pool, leituras de arquivo):

```java
public class ClienteApiExterno {
    // No máximo 10 chamadas simultâneas
    private final Semaphore rateLimiter = new Semaphore(10);

    public Resposta consultar(String recurso) throws InterruptedException {
        rateLimiter.acquire();
        try {
            return httpClient.get(baseUrl + recurso);
        } finally {
            rateLimiter.release();  // libera mesmo se houver exceção
        }
    }

    // Versão não-bloqueante — útil em sistemas com backpressure explícito
    public Optional<Resposta> tentarConsultar(String recurso) {
        if (!rateLimiter.tryAcquire()) {
            return Optional.empty();  // sistema sobrecarregado, rejeitamos
        }
        try {
            return Optional.of(httpClient.get(baseUrl + recurso));
        } catch (Exception e) {
            return Optional.empty();
        } finally {
            rateLimiter.release();
        }
    }
}
```

`tryAcquire()` ignora a configuração de fairness e retorna `false` imediatamente se não há permit disponível — ideal para circuito de backpressure sem esperar na fila.

## Armadilhas

### (1) Tentar reusar `CountDownLatch` — é one-shot, o contador não reinicia

**O problema:** após o contador atingir zero, `countDown()` se torna no-op e `await()` retorna imediatamente. Criar um novo latch no lugar do antigo só funciona se todas as referências forem atualizadas atomicamente — o que raramente é o caso em código multithread.

```java
// RUIM — tentativa de "resetar" o latch substituindo o objeto
private CountDownLatch latch = new CountDownLatch(3);

public void reiniciarCiclo() {
    latch = new CountDownLatch(3);  // race: outra thread pode ainda ter a referência antiga
}
```

```java
// FIX — use CyclicBarrier quando precisar de repetição
private final CyclicBarrier barrier = new CyclicBarrier(3);

// barrier.await() em cada thread; quando todas chegam, o ciclo reinicia automaticamente
// Para reset forçado: barrier.reset() (threads aguardando recebem BrokenBarrierException)
```

---

### (2) `BrokenBarrierException` quando uma thread morre ou atinge timeout na barrier

**O problema:** `CyclicBarrier` adota um modelo "tudo ou nada". Se qualquer thread for interrompida, lançar uma exceção não capturada ou expirar com timeout antes de todas chegarem, a barreira entra em estado **broken** (`isBroken() == true`). A partir daí, toda chamada a `await()` — incluindo threads que ainda não chegaram — lança `BrokenBarrierException` imediatamente.

```java
// RUIM — sem tratamento de BrokenBarrierException
barrier.await();  // pode lançar BrokenBarrierException se outra thread falhou
processarFase2(); // nunca executado se barrier estiver quebrada
```

```java
// FIX — tratar ambas as exceções e decidir política de retry/abort
try {
    barrier.await(30, TimeUnit.SECONDS);
} catch (BrokenBarrierException e) {
    // Outra thread falhou ou o barrier foi resetado
    log.error("Barrier quebrada — abortando ciclo", e);
    throw new ProcessamentoException("Sincronização falhou", e);
} catch (TimeoutException e) {
    // Esta thread expirou — o barrier agora também está broken para os demais
    log.error("Timeout aguardando barrier", e);
    barrier.reset();  // opcional: reinicia o ciclo para próxima tentativa
    throw new ProcessamentoException("Timeout na barrier", e);
} catch (InterruptedException e) {
    Thread.currentThread().interrupt();
    throw new ProcessamentoException("Interrompida", e);
}
```

---

### (3) `Semaphore` sem `release()` no `finally` — permits vazam

**O problema:** se a thread que adquiriu o permit lançar uma exceção antes de chamar `release()`, o permit nunca é devolvido. Com tempo, todos os permits se esgotam e a aplicação trava com todas as threads bloqueadas em `acquire()`.

```java
// RUIM — permit vaza se chamaExterna() lançar exceção
public void processar() throws InterruptedException {
    semaphore.acquire();
    chamaExterna();  // pode lançar RuntimeException
    semaphore.release();  // nunca executado se chamaExterna() falhar
}
```

```java
// FIX — release() sempre no finally
public void processar() throws InterruptedException {
    semaphore.acquire();
    try {
        chamaExterna();
    } finally {
        semaphore.release();  // executa mesmo com exceção
    }
}
```

Esse padrão é análogo ao `lock.unlock()` sempre em `finally` com `ReentrantLock`. Qualquer saída do bloco — normal ou excepcional — deve devolver o permit.

## Em entrevista

### Frase pronta (inglês)

> "The key distinction between `CountDownLatch` and `CyclicBarrier` is reusability and directionality: a latch is one-shot — you count down N events and any waiting thread is released when the counter hits zero, but the counter can never be reset. A cyclic barrier, on the other hand, is for N threads that need to rendezvous with each other at a common point; once all parties arrive, the barrier resets automatically for the next cycle, and you can optionally run a barrier action — a Runnable executed by the last arriving thread before anyone is released." "Semaphore models access to a limited resource through permits: `acquire()` blocks until a permit is available and `release()` returns one. Unlike locks, semaphore has no notion of ownership — any thread can release, which makes it suitable for rate limiting and resource pools, but also means you need to be disciplined about releasing in a `finally` block to avoid permit leaks." "Phaser is the most flexible of the synchronizers: it generalizes both latch and barrier with dynamic party registration, explicit phase numbers, and a termination hook via `onAdvance()`. I reach for it when the number of participating threads is not known at construction time or when I need to run a multi-phase algorithm with different sets of threads in each phase."

### Vocabulário

| Termo PT | Termo EN |
|---|---|
| sincronizador | synchronizer |
| trava única (não reutilizável) | one-shot latch |
| barreira cíclica | cyclic barrier |
| semáforo / permit | semaphore / permit |
| ação de barreira | barrier action |
| barreira quebrada | broken barrier |
| vazamento de permit | permit leak |
| ponto de encontro | rendezvous point |
| registro dinâmico | dynamic party registration |
| handoff síncrono | synchronous handoff |
| fase | phase |
| partes registradas | registered parties |

## Veja também

- [[07 - Concurrent collections]]
- [[08 - Executors e thread pools]]
- [[03-Dominios/Java/Concorrência e paralelismo/index|MOC do galho]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[Java Concurrency]]
- [[03-Dominios/Java/Dicionário de Java#Latch (CountDownLatch)|latch]]
- [[03-Dominios/Java/Dicionário de Java#Barrier (CyclicBarrier)|barrier]]
- [[03-Dominios/Java/Dicionário de Java#Semaphore (semáforo)|semaphore]]

## Referências

- [CountDownLatch — Java 21 API (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/CountDownLatch.html)
- [CyclicBarrier — Java 21 API (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/CyclicBarrier.html)
- [Semaphore — Java 21 API (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/Semaphore.html)
- [Phaser — Java 21 API (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/Phaser.html)
- [Exchanger — Java 21 API (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/Exchanger.html)
- [java.util.concurrent — Package Summary, Java 21 (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/package-summary.html)
