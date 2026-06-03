---
title: "As armadilhas: race, deadlock e companhia"
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
  - deadlock
  - race-condition
aliases:
  - Race condition
  - Deadlock
---

# As armadilhas: race, deadlock e companhia

> [!abstract] TL;DR
> Programas concorrentes falham de formas que código sequencial nunca apresentaria. As armadilhas clássicas são: **race condition** (resultado depende da ordem de execução), **deadlock** (threads bloqueadas esperando umas pelas outras para sempre), **livelock** (threads ativas mas sem progresso) e **starvation** (thread que nunca consegue acesso). Cada uma tem causas, sinais e prevenções distintas — identificá-las rapidamente em código ou em entrevista é marca de programador sênior.

## O que é

Concorrência expõe o estado compartilhado a múltiplas threads simultaneamente. Quando esse acesso não é devidamente coordenado, surgem classes de bugs que não são reproduzíveis deterministicamente: dependem de timing, carga e arquitetura do processador.

As categorias clássicas de problemas são:

- **Race condition** — o resultado do programa depende da ordem ou do entrelaçamento de operações de múltiplas threads. O bug pode nunca aparecer em testes de baixa carga e manifestar-se apenas em produção.
- **Deadlock** — duas ou mais threads ficam bloqueadas indefinidamente, cada uma aguardando um recurso que outra detém.
- **Livelock** — threads não estão bloqueadas, mas também não progridem: ficam reagindo continuamente umas às outras sem avançar.
- **Starvation** — uma thread nunca consegue acesso ao recurso de que precisa porque outras threads passam consistentemente na frente.
- **Visibility e publication bugs** — uma thread não enxerga escritas realizadas por outra por falta de sincronização de memória (ver aprofundamento em [[11 - Java Memory Model em profundidade]]).

## Por que importa

Esses bugs são especialmente traiçoeiros porque:

1. **Não são determinísticos.** Um race condition pode existir no código por meses sem se manifestar — e explodir sob carga em produção com dados reais. A expressão "funciona aqui, quebra lá" reflete exatamente esse comportamento: o bug é real e latente, mas só aparece quando o timing é desfavorável.
2. **São difíceis de reproduzir.** Adicionar logs ou um breakpoint frequentemente muda o timing e faz o bug desaparecer.
3. **Deadlocks travam o sistema.** Partes inteiras de uma aplicação deixam de responder sem lançar exceção, o que dificulta o diagnóstico.
4. **Starvation e livelock se parecem com lentidão.** Podem ser confundidos com gargalos de desempenho comuns.

Reconhecer esses padrões em revisão de código ou em sistemas com comportamento anômalo é uma competência central para quem trabalha com sistemas concorrentes em Java.

## Como funciona

### Race condition

Uma race condition ocorre quando o comportamento correto do programa depende de que certas operações aconteçam em uma ordem específica entre threads — e essa ordem não é garantida.

Há dois padrões recorrentes:

**Check-then-act:** a thread verifica uma condição e então age com base nela, mas entre a verificação e a ação outra thread pode ter alterado o estado.

```java
// BUG — check-then-act sem sincronização
if (!cache.containsKey(key)) {   // Thread A e Thread B chegam aqui ao mesmo tempo
    cache.put(key, compute(key)); // Ambas inserem — uma sobrescreve a outra
}

// FIX — operação atômica
cache.computeIfAbsent(key, k -> compute(k));
```

**Read-modify-write:** a thread lê um valor, modifica-o e escreve de volta. Se outra thread fizer o mesmo entre a leitura e a escrita, uma das modificações é perdida.

```java
// BUG — read-modify-write sem sincronização
// Supondo: counter começa em 5
// Thread A lê 5, Thread B lê 5
// Thread A escreve 6, Thread B escreve 6 — uma incrementação foi perdida
counter++; // não atômico: é read + increment + write

// FIX — usar AtomicInteger
AtomicInteger counter = new AtomicInteger(0);
counter.incrementAndGet(); // atômico por CAS (Compare-And-Swap)
```

> [!warning] Não-determinismo
> O resultado de um race condition **não é previsível**. Em duas execuções consecutivas do mesmo código, o comportamento pode ser diferente. Nunca assuma que "sempre funciona" significa "está correto".

---

### Deadlock

Um deadlock ocorre quando duas ou mais threads formam um ciclo de espera: cada uma detém um recurso e aguarda um recurso detido por outra.

A literatura clássica de sistemas operacionais descreve **quatro condições necessárias para um deadlock** (conhecidas como condições de Coffman, 1971):

1. **Exclusão mútua** — o recurso só pode ser usado por uma thread de cada vez.
2. **Posse e espera** — uma thread detém ao menos um recurso enquanto aguarda outro.
3. **Sem preempção** — recursos não podem ser tomados à força; só são liberados voluntariamente.
4. **Espera circular** — existe um ciclo: A espera por B, B espera por C, C espera por A.

Para eliminar o deadlock, basta quebrar qualquer uma dessas condições. Na prática, a mais fácil de controlar é a **espera circular**, impondo uma **ordem global de aquisição de locks**.

```java
// BUG — ordem inconsistente de locks → deadlock
// Thread A: adquire lockX, depois tenta lockY
// Thread B: adquire lockY, depois tenta lockX
// Resultado: ciclo de espera permanente

// FIX — sempre adquirir locks na mesma ordem global
// Define: lockX sempre antes de lockY (por convenção ou por ID)
synchronized (lockX) {
    synchronized (lockY) {
        // operação segura
    }
}
```

Outra estratégia é usar `tryLock` com timeout do `ReentrantLock`, que permite desistir se o lock não for obtido em tempo:

```java
ReentrantLock lockA = new ReentrantLock();
ReentrantLock lockB = new ReentrantLock();

boolean acquired = false;
try {
    acquired = lockA.tryLock(100, TimeUnit.MILLISECONDS);
    if (acquired) {
        if (lockB.tryLock(100, TimeUnit.MILLISECONDS)) {
            try {
                // operação
            } finally {
                lockB.unlock();
            }
        }
    }
} catch (InterruptedException e) {
    Thread.currentThread().interrupt();
} finally {
    if (acquired) lockA.unlock();
}
```

**Detecção em produção:** `jstack <pid>` imprime thread dumps e marca deadlocks explicitamente. Via JMX: `ManagementFactory.getThreadMXBean().findDeadlockedThreads()`.

---

### Livelock

No livelock, as threads não estão bloqueadas — estão ativas e respondendo. O problema é que elas ficam reagindo umas às outras em um ciclo sem progressão real.

Analogia canônica da documentação Oracle: dois pedestres num corredor estreito. Cada um desvia para o mesmo lado que o outro, repetidamente, e nenhum consegue passar.

```text
Thread A detecta conflito → recua → Thread B detecta conflito → recua →
Thread A tenta avançar → detecta conflito novamente → recua...
(nenhuma progride)
```

**Prevenção:** introduzir aleatoriedade no tempo de espera antes de tentar novamente (*exponential backoff with jitter*), ou usar lógica assimétrica (ex.: thread com ID menor sempre cede primeiro).

---

### Starvation e fairness

Starvation ocorre quando uma thread nunca consegue acesso ao recurso de que precisa — não porque haja deadlock, mas porque outras threads sempre chegam antes.

Causas comuns:
- Threads de alta prioridade monopolizando a CPU.
- Locks não-fair (`synchronized` padrão e `ReentrantLock` sem argumento) que não garantem ordem FIFO de aquisição.
- Um método `synchronized` que demora muito: quem o chama com frequência pode sempre "vencer" threads que tentam acessar o mesmo objeto com menos frequência.

**Prevenção:**

```java
// ReentrantLock em modo fair — respeita ordem FIFO de chegada
ReentrantLock fairLock = new ReentrantLock(true);

// Semaphore em modo fair
Semaphore fairSemaphore = new Semaphore(1, true);
```

> [!warning] Custo do fair mode
> Locks em modo fair têm throughput menor que locks não-fair. Use quando starvation for um risco real — não por padrão.

---

### Visibility e publication bugs (teaser)

Uma thread pode não enxergar valores escritos por outra thread se não houver sincronização adequada. O compilador e o processador podem reordenar instruções e manter valores em cache de CPU. Esses comportamentos são governados pelo **Java Memory Model**, que define quando uma escrita é garantidamente visível para uma leitura.

Aprofundamento completo em [[11 - Java Memory Model em profundidade]].

## Na prática

### Deadlock clássico: transferência entre contas

Um cenário recorrente em entrevistas é o deadlock em transferência bancária. Duas operações simultâneas transferem valores entre as mesmas contas em sentidos opostos, cada uma adquirindo os locks em ordem diferente.

```java
// Classe Account simples (exemplo neutro)
class Account {
    private final int id;
    private int balance;

    Account(int id, int balance) {
        this.id = id;
        this.balance = balance;
    }

    int getId() { return id; }

    synchronized void debit(int amount)  { balance -= amount; }
    synchronized void credit(int amount) { balance += amount; }
}
```

```java
// BUG — deadlock potencial
void transfer(Account from, Account to, int amount) {
    synchronized (from) {               // Thread A bloqueia conta1
        synchronized (to) {             // Thread A tenta bloquear conta2
            from.debit(amount);         // Thread B já bloqueou conta2
            to.credit(amount);          // e tenta bloquear conta1 → DEADLOCK
        }
    }
}
```

Se duas threads executarem `transfer(conta1, conta2, 100)` e `transfer(conta2, conta1, 50)` simultaneamente, o deadlock é possível.

**Fix: ordenar locks pelo ID da conta**

```java
// FIX — lock ordering pelo ID garante ordem global consistente
void transfer(Account from, Account to, int amount) {
    Account first  = from.getId() < to.getId() ? from : to;
    Account second = from.getId() < to.getId() ? to   : from;

    synchronized (first) {
        synchronized (second) {
            from.debit(amount);
            to.credit(amount);
        }
    }
}
```

Com lock ordering, qualquer par de threads que tente transferir entre as mesmas duas contas sempre adquirirá os locks na mesma sequência — o ciclo de espera nunca se forma.

## Armadilhas

### (1) Adquirir locks em ordem inconsistente

**O problema:** código em diferentes partes do sistema adquire os mesmos locks em ordens diferentes. Cada parte funciona isoladamente; o deadlock só aparece quando ambas executam ao mesmo tempo, com timing desfavorável.

```java
// Módulo X
synchronized (lockAlpha) {
    synchronized (lockBeta) { /* ... */ }
}

// Módulo Y (em outro arquivo, escrito por outro desenvolvedor)
synchronized (lockBeta) {
    synchronized (lockAlpha) { /* ... */ }  // ordem invertida!
}
```

**Fix:** definir e documentar uma ordem global de aquisição de locks. Uma estratégia prática é usar o `System.identityHashCode()` ou um ID imutável do objeto para determinar a ordem quando os locks são dinâmicos.

```java
// Ordem determinada por identityHashCode
void lockInOrder(Object a, Object b, Runnable action) {
    Object first  = System.identityHashCode(a) <= System.identityHashCode(b) ? a : b;
    Object second = first == a ? b : a;
    synchronized (first) {
        synchronized (second) {
            action.run();
        }
    }
}
```

---

### (2) "Funciona aqui, quebra lá" — race latente que só aparece sob carga

**O problema:** races com janela de tempo muito pequena raramente se manifestam em ambientes de desenvolvimento (pouca carga, poucas threads). O código passa por testes, vai para produção e quebra sob tráfego real — quando múltiplas threads competem com frequência suficiente para cair na janela crítica.

```java
// Parece inofensivo em testes com 1-2 threads
if (session.isValid()) {          // Thread A: válida → entra
    session.process(request);     // Thread B: invalida a sessão aqui
    // Thread A: processa sessão inválida → comportamento indefinido
}
```

**Fix:** identificar e eliminar sequências check-then-act não atômicas. Usar operações atômicas, `synchronized`, ou estruturas de dados concorrentes (`ConcurrentHashMap.computeIfAbsent`, `AtomicReference.compareAndSet`). Testes de carga com concorrência alta (`CountDownLatch`, `CyclicBarrier` em testes) ajudam a expor a janela.

```java
// FIX — a validação e o processamento devem ser atômicos
synchronized (session) {
    if (session.isValid()) {
        session.process(request);
    }
}
```

---

### (3) Starvation por thread de baixa prioridade

**O problema:** threads de baixa prioridade são constantemente preteridas por threads de alta prioridade ou por threads que seguram locks por períodos longos. A thread de baixa prioridade fica viva mas não avança — o sistema como um todo aparenta lentidão nessa parte.

```java
// Cenário: thread de relatório (baixa prioridade) compete com
// threads de requisição HTTP (alta prioridade) pelo mesmo lock
// O relatório pode demorar horas para completar — ou nunca completar

Thread relatorio = new Thread(this::gerarRelatorio);
relatorio.setPriority(Thread.MIN_PRIORITY); // quase nunca recebe CPU
relatorio.start();
```

**Fix:** usar `ReentrantLock(true)` (fair mode) para garantir FIFO, ou separar completamente os recursos usados pela thread de baixa prioridade para que ela não compita diretamente. Alternativamente, usar filas de trabalho dedicadas (`BlockingQueue`) em vez de locks compartilhados.

```java
// FIX — lock fair garante que a thread de relatório não seja preterida indefinidamente
ReentrantLock fairLock = new ReentrantLock(true);

// ou: separar recursos — relatório usa snapshot imutável, não compete com o live path
List<Record> snapshot = new ArrayList<>(liveData); // cópia defensiva
gerarRelatorio(snapshot);                           // sem lock compartilhado
```

## Em entrevista

### Frase pronta (inglês)

> "Race conditions, deadlocks, livelocks, and starvation are the four classic failure modes in concurrent programming. A race condition occurs when correctness depends on unguaranteed thread scheduling — check-then-act and read-modify-write sequences are the most common patterns. Deadlock requires four conditions to hold simultaneously — mutual exclusion, hold-and-wait, no preemption, and circular wait — and the most practical prevention strategy is enforcing a global lock-ordering discipline so that circular wait can never form. Livelock is subtler: threads are not blocked but are stuck responding to each other, and the usual fix is adding randomized backoff; starvation, on the other hand, is solved by fair locks or by redesigning resource access to avoid long-held monopolies."

### Vocabulário

| Termo PT                              | Termo EN                                              |
|---------------------------------------|-------------------------------------------------------|
| condição de corrida                   | race condition                                        |
| impasse / deadlock                    | deadlock                                              |
| impasse ativo / pseudoimpasse         | livelock                                              |
| inanição                              | starvation                                            |
| condições de Coffman                  | Coffman conditions                                    |
| exclusão mútua                        | mutual exclusion                                      |
| posse e espera                        | hold-and-wait                                         |
| espera circular                       | circular wait                                         |
| ordem de aquisição de locks           | lock ordering / lock acquisition order                |
| lock justo / modo FIFO                | fair lock / fair mode                                 |
| backoff com aleatoriedade             | randomized backoff / exponential backoff with jitter  |
| visibilidade de memória               | memory visibility                                     |

## Veja também

- [[03 - Exclusão mútua com synchronized]]
- [[05 - Locks explícitos]]
- [[11 - Java Memory Model em profundidade]]
- [[16 - Padrões e diagnóstico de concorrência]]
- [[03-Dominios/Java/Concorrência e paralelismo/index|MOC do galho]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[Java Concurrency]]
- [[03-Dominios/Java/Dicionário de Java#Condição de corrida (race condition)|race condition]]
- [[03-Dominios/Java/Dicionário de Java#Deadlock|deadlock]]
- [[03-Dominios/Java/Dicionário de Java#Livelock|livelock]]
- [[03-Dominios/Java/Dicionário de Java#Starvation|starvation]]

## Referências

- [Deadlock — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/essential/concurrency/deadlock.html)
- [Starvation and Livelock — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/essential/concurrency/starvelive.html)
- Goetz, Brian et al. *Java Concurrency in Practice*. Addison-Wesley, 2006. Cap. 10 (Avoiding Liveness Hazards).
