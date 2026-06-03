---
title: "Threads e seu ciclo de vida"
created: 2026-06-03
updated: 2026-06-03
type: concept
progress: backlog
status: seedling
publish: true
fase: iniciado
tags:
  - java
  - concorrencia
  - iniciado
  - threads
  - lifecycle
aliases:
  - Thread
  - Ciclo de vida de thread
---

# Threads e seu ciclo de vida

> [!abstract] TL;DR
> Uma **thread** é a unidade mínima de execução da JVM — um fluxo independente de instruções que o agendador do sistema operacional pode intercalar com outros. Em Java, toda thread tem um **ciclo de vida** com seis estados definidos em `Thread.State` (NEW → RUNNABLE → BLOCKED / WAITING / TIMED_WAITING → TERMINATED), acessíveis via `thread.getState()`. Criar uma thread diretamente (`new Thread(...)`) é a fundação do modelo, mas em código moderno a criação é delegada a `ExecutorService` ou Virtual Threads — entender o ciclo de vida, a política de interrupção e a diferença entre threads daemon e user é pré-requisito para qualquer dessas abstrações.

## O que é

Uma **thread** (linha de execução) é o menor elemento de processamento gerenciado pela JVM e pelo sistema operacional. Em um processo Java, todas as threads compartilham o mesmo heap, mas cada uma possui sua própria **pilha de chamadas** (call stack), contador de programa e registradores de CPU.

Em Java, threads são representadas pela classe `java.lang.Thread`. A JVM mantém pelo menos duas threads ao iniciar: a _main thread_ (que executa `main()`) e threads internas de sistema (ex.: GC, JIT). O desenvolvedor pode criar threads adicionais para executar trabalho concorrentemente.

Três formas de definir o trabalho de uma thread:

| Abordagem | Como | Nota |
|---|---|---|
| Subclasse de `Thread` | sobrescreve `run()` | Acopla tarefa e mecanismo; evitar |
| `Runnable` passado ao construtor | `new Thread(runnable)` | Desacopla tarefa; forma clássica |
| Lambda / method reference | `new Thread(() -> ...)` | Açúcar sintático para `Runnable` |

## Por que importa

Entender o ciclo de vida e os controles básicos de thread é pré-requisito para compreender qualquer camada de abstração sobre concorrência em Java:

- **`ExecutorService` e thread pools** gerenciam threads internamente; erros de interrupção engolidos nessa camada causam comportamentos imprevisíveis no pool.
- **Virtual Threads** (Java 21+) seguem o mesmo modelo de estados e herdam o protocolo de interrupção; o código que trata `InterruptedException` corretamente funciona em ambos.
- **Debugging via thread dump** (`jstack`, `jcmd Thread.print`) expõe exatamente os estados do `Thread.State` — interpretar um dump sem conhecer os estados é impossível.
- **Entrevistas senior** frequentemente testam os estados, a política de interrupção e a armadilha do `run()` direto.

## Como funciona

### `Thread` vs `Runnable`

O contrato fundamental: `start()` agenda a execução em uma **nova** thread; `run()` executa o corpo na thread **atual**.

```java
Runnable tarefa = () -> System.out.println("Thread: " + Thread.currentThread().getName());

// CORRETO — cria e agenda nova thread
Thread t = new Thread(tarefa, "worker-1");
t.start();  // retorna imediatamente; tarefa roda concorrentemente

// ERRADO — executa na thread que chamou (sem nova thread)
t.run();    // roda na thread atual, como chamada de método normal
```

`start()` só pode ser chamado **uma vez** por instância. Chamar novamente lança `IllegalThreadStateException`. Se precisar reutilizar a tarefa, crie uma nova instância de `Thread`.

---

### Estados de uma thread

Cada thread está em exatamente um dos seis estados definidos em `Thread.State` (JDK 21, `java.lang.Thread.State`):

```text
                    ┌─────────────────────────────────────────────────┐
                    │                                                 │
  new Thread()      │   t.start()                                     │
  ──────────►  NEW ──────────► RUNNABLE ◄───────────────────────────┐ │
                               │      │                             │ │
         Object.wait()         │      │  monitor lock               │ │
         Thread.join()         │      │  não disponível             │ │
         LockSupport.park()    │      ▼                             │ │
                               │   BLOCKED ──► lock adquirido ─────┘ │
                               │                                      │
         Thread.sleep(t)       │      ▼                               │
         Object.wait(t)        │   WAITING ──► notify/join/unpark ───┘│
         Thread.join(t)        │                                       │
         LockSupport.parkNanos │      ▼                                │
                               │   TIMED_WAITING ──► tempo esgotado/  │
                               │                     sinal ───────────┘
                               │
                               ▼
                           TERMINATED
                        (run() concluiu
                         ou exceção)
```

| Estado | Quando ocorre |
|---|---|
| `NEW` | Objeto criado, `start()` não chamado |
| `RUNNABLE` | Em execução na JVM ou aguardando CPU (inclui operações de I/O em andamento) |
| `BLOCKED` | Aguardando adquirir um **monitor lock** (`synchronized`) |
| `WAITING` | Aguardando indefinidamente: `Object.wait()`, `Thread.join()`, `LockSupport.park()` |
| `TIMED_WAITING` | Aguardando com timeout: `Thread.sleep(t)`, `Object.wait(t)`, `Thread.join(t)` |
| `TERMINATED` | `run()` completou (normalmente ou por exceção não tratada) |

Esses são **estados da JVM**, não do sistema operacional. Uma thread `RUNNABLE` pode estar aguardando CPU no kernel — a JVM não distingue.

---

### Controle: `join` / `interrupt` / `sleep` / `yield`

**`join()`** — a thread chamante bloqueia até que a thread-alvo chegue a `TERMINATED`:

```java
Thread t = new Thread(() -> processarLote());
t.start();
t.join();   // bloqueia até t terminar
// A partir daqui, t.getState() == TERMINATED
System.out.println("Lote concluído");
```

Versão com timeout: `t.join(5000)` espera no máximo 5 segundos; retorna mesmo que `t` ainda esteja viva. Ambas lançam `InterruptedException`.

**`interrupt()`** — seta o **flag de interrupção** da thread. Não força a thread a parar:

```java
t.interrupt();  // seta o flag; t deve checar e reagir
```

Se `t` estiver bloqueada em `sleep`, `wait` ou `join`, a operação lança `InterruptedException` e **limpa** o flag. Se `t` estiver `RUNNABLE`, apenas o flag é setado — a thread deve checar `Thread.currentThread().isInterrupted()` no seu próprio loop.

**`sleep(long millis)`** — pausa a thread atual pelo tempo especificado (não libera locks). Lança `InterruptedException` se interrompida durante o sono, limpando o flag:

```java
try {
    Thread.sleep(1000);   // pausa 1 segundo
} catch (InterruptedException e) {
    Thread.currentThread().interrupt(); // restaurar o flag!
    return; // ou propagar
}
```

**`yield()`** — dica ao agendador de que a thread atual está disposta a ceder o processador. O agendador é livre para ignorar. Raramente necessário fora de benchmarks ou loops de spin:

```java
Thread.yield(); // apenas uma sugestão; sem garantia
```

---

### Daemon vs user threads

Threads se dividem em dois tipos:

| Tipo | Comportamento ao finalizar |
|---|---|
| **User thread** (padrão) | JVM **aguarda** todas as user threads antes de sair |
| **Daemon thread** | JVM **não aguarda**; são encerradas abruptamente quando só sobram daemons |

```java
Thread daemon = new Thread(() -> {
    while (true) {
        limpezaPeriodicaDeCache(); // tarefa de background
    }
});
daemon.setDaemon(true);  // DEVE ser chamado antes de start()
daemon.start();
// Quando a main thread terminar, a JVM encerrará daemon abruptamente
```

`setDaemon(true)` deve ser chamado antes de `start()` — depois lança `IllegalThreadStateException`. Virtual Threads são sempre daemon (`setDaemon(false)` lança `IllegalArgumentException` nelas).

Exemplos de daemon threads da própria JVM: Garbage Collector, JIT compiler, finalizadores.

---

### Ler um thread dump (intro)

Thread dumps são a primeira ferramenta em incidentes de concorrência. Cada entrada mostra nome, estado e stack:

```bash
# Gerar thread dump (escolha um):
jstack <pid>              # imprime no terminal
jcmd <pid> Thread.print   # equivalente via jcmd
kill -3 <pid>             # SIGQUIT → imprime no stderr do processo
```

Trecho típico de um dump:

```text
"worker-1" #12 prio=5 os_prio=0 tid=0x... nid=0x... waiting for monitor entry
   java.lang.Thread.State: BLOCKED (on object monitor)
    at com.exemplo.Servico.processar(Servico.java:42)
    - waiting to lock <0x...> (a java.lang.Object)
```

O que observar:

- Várias threads em `BLOCKED` no mesmo objeto → contenção de lock
- Threads em `WAITING` em filas → pool sub-dimensionado
- `DEADLOCK` marcado explicitamente pelo `jstack`

## Na prática

**Criando e iniciando uma thread com lambda:**

```java
// Tarefa simples
Thread t = new Thread(() -> {
    System.out.println("Executando em: " + Thread.currentThread().getName());
}, "minha-thread");

t.setDaemon(false);  // user thread (padrão)
t.start();
t.join();            // espera concluir
```

**Interrupção cooperativa — o padrão correto:**

```java
// hipotético: worker que processa tarefas até ser interrompido
Thread worker = new Thread(() -> {
    while (!Thread.currentThread().isInterrupted()) {
        try {
            Tarefa t = fila.take();  // WAITING — pode lançar InterruptedException
            processar(t);
        } catch (InterruptedException e) {
            // take() limpou o flag — restaurar para que o loop possa detectar
            Thread.currentThread().interrupt();
            // loop verifica isInterrupted() e termina na próxima iteração
        }
    }
    System.out.println("Worker encerrado normalmente");
});

worker.start();

// Em outro ponto do código:
worker.interrupt(); // sinaliza ao worker para parar
worker.join();
```

A chave do padrão: ao capturar `InterruptedException`, **restaurar o flag** com `Thread.currentThread().interrupt()`. Isso permite que o chamador (ou o laço de verificação) saiba que uma interrupção ocorreu.

## Armadilhas

### (1) Chamar `run()` diretamente em vez de `start()`

**O problema:** `run()` é um método comum — chamá-lo executa o corpo da thread na thread que fez a chamada, sem criar nenhuma nova thread. Nenhum erro é lançado; o código "funciona", mas não concorrentemente.

```java
Thread t = new Thread(() -> {
    System.out.println("Em: " + Thread.currentThread().getName());
});

t.run();    // BUG: imprime "Em: main" — roda na main thread
t.start();  // CORRETO: imprime "Em: Thread-0" (ou nome configurado)
```

**Fix:** sempre usar `start()` para iniciar concorrência. A confusão ocorre especialmente ao tentar "testar" a tarefa diretamente.

---

### (2) Engolir `InterruptedException` — perder o sinal de interrupção

**O problema:** capturar `InterruptedException` e não fazer nada silencia o pedido de interrupção. O chamador (ex.: `ExecutorService` ao fazer `shutdownNow()`) nunca saberá que a thread deveria ter parado. Em thread pools, isso pode fazer com que o pool nunca encerre limpo.

```java
// BUG — InterruptedException engolida
void processarComSleep() {
    try {
        Thread.sleep(5000);
    } catch (InterruptedException e) {
        // nada — o flag foi limpo, o sinal foi perdido para sempre
    }
}
```

**Fix — opção 1: restaurar o flag e retornar:**

```java
void processarComSleep() {
    try {
        Thread.sleep(5000);
    } catch (InterruptedException e) {
        Thread.currentThread().interrupt(); // restaura o flag
        return;                             // ou break, dependendo do contexto
    }
}
```

**Fix — opção 2: propagar a exceção (melhor quando possível):**

```java
void processarComSleep() throws InterruptedException {
    Thread.sleep(5000);  // propaga; o chamador decide o que fazer
}
```

---

### (3) Usar `Thread.stop()` para encerrar uma thread — deprecated e inseguro

**O problema:** `Thread.stop()` foi depreciado desde Java 1.2 e lança `UnsupportedOperationException` desde versões mais recentes. Mesmo quando "funcionava", era perigoso: forçava o lançamento de `ThreadDeath` na thread-alvo em ponto arbitrário, podendo corromper objetos em estados intermediários (ex.: dentro de um bloco `synchronized` mantendo invariantes).

```java
Thread t = new Thread(tarefaLonga);
t.start();
t.stop();  // NÃO FAZER — UnsupportedOperationException em JDK moderno
```

**Fix:** implementar interrupção cooperativa — a thread verifica `isInterrupted()` (ou um flag `volatile boolean`) em pontos seguros e encerra por vontade própria:

```java
// hipotético: flag de parada para tarefa que não usa operações bloqueantes
volatile boolean parar = false;

Thread t = new Thread(() -> {
    while (!parar && !Thread.currentThread().isInterrupted()) {
        processarProximoItem();
    }
});

t.start();
// Para parar:
parar = true;
t.interrupt(); // desperta se estiver em sleep/wait
t.join();
```

## Em entrevista

### Frase pronta (inglês)

> "The key trade-off when working with threads directly versus using an executor is control versus complexity. A `Thread` object goes through six well-defined states — NEW, RUNNABLE, BLOCKED, WAITING, TIMED_WAITING, and TERMINATED — and understanding those states is essential for reading thread dumps and diagnosing concurrency issues in production. The critical design decision around interruption is that Java uses a *cooperative* model: calling `interrupt()` merely sets a flag; the thread itself must check `isInterrupted()` or handle `InterruptedException` and decide to stop. The most common caveat is swallowing `InterruptedException` without restoring the flag — this silently kills the interrupt signal and can prevent executor shutdown from working correctly. In modern Java, you rarely create `Thread` directly; you use `ExecutorService` or, since Java 21, virtual threads — but the interrupt protocol and lifecycle states apply equally to both."

### Vocabulário

| Termo PT | Termo EN |
|---|---|
| thread | thread |
| ciclo de vida de thread | thread lifecycle |
| estado da thread | thread state |
| interrupção cooperativa | cooperative interruption |
| flag de interrupção | interrupt flag / interrupt status |
| thread daemon | daemon thread |
| thread usuário / não-daemon | user thread / non-daemon thread |
| pilha de chamadas | call stack |
| agendador | scheduler |
| despejo de threads | thread dump |
| contenção de lock | lock contention |
| thread carrier (Virtual Threads) | carrier thread |

## Veja também

- [[01 - Concorrência e paralelismo - o modelo]]
- [[03 - Exclusão mútua com synchronized]]
- [[08 - Executors e thread pools]]
- [[03-Dominios/Java/Concorrência e paralelismo/index|MOC do galho]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[Java Concurrency]]
- [[03-Dominios/Java/Dicionário de Java#Thread pool|thread pool]]

## Referências

- [Class Thread — Java SE 21 API (docs.oracle.com)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/Thread.html)
- [Enum Thread.State — Java SE 21 API (docs.oracle.com)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/Thread.State.html)
- [Lesson: Concurrency — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/essential/concurrency/)
- [JEP 444: Virtual Threads — openjdk.org](https://openjdk.org/jeps/444)
