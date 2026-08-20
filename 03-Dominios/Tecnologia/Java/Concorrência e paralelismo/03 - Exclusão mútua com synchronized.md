---
title: "Exclusão mútua com synchronized"
created: 2026-06-03
updated: 2026-06-03
type: concept
progress: backlog
status: seedling
publish: true
fase: Iniciado
tags:
  - java
  - concorrencia
  - iniciado
  - synchronized
  - locks
aliases:
  - synchronized
  - Exclusão mútua
---

# Exclusão mútua com synchronized

> [!abstract] TL;DR
> Toda vez que duas ou mais threads leem e escrevem um dado compartilhado sem coordenação, o resultado é imprevisível — isso é uma **race condition**. Java resolve isso com `synchronized`, que associa um **intrinsic lock** (monitor) a cada objeto: só a thread que detém o lock executa a seção crítica; todas as outras bloqueiam. `synchronized` pode decorar métodos de instância (`this` como lock), blocos com objeto explícito, e métodos estáticos (`Class` como lock). O mecanismo é **reentrante**: a mesma thread pode adquirir o mesmo lock várias vezes sem travar. Para coordenação entre threads, `wait`/`notify`/`notifyAll` operam sobre o monitor — `wait` **deve** ficar dentro de um `while`, nunca de um `if`, para sobreviver a spurious wakeups.

## O que é

Considere o contador mais simples possível:

```java
// hipotético: contador compartilhado por duas threads
public class Contador {
    private int valor = 0;

    public void incrementar() {
        valor++; // parece atômica — não é
    }

    public int get() {
        return valor;
    }
}
```

A expressão `valor++` compila em três operações JVM: ler, somar 1, gravar. Com duas threads executando simultaneamente:

```text
Thread A lê valor = 5
Thread B lê valor = 5        ← B lê antes de A gravar
Thread A soma → 6, grava: valor = 6
Thread B soma → 6, grava: valor = 6  ← sobrescrita silenciosa!
```

O resultado esperado era `7`; obtemos `6`. O output **não é determinístico** — depende do escalonamento do SO. Esse é o problema de **interferência entre threads** (thread interference), uma subclasse das race conditions.

Além da interferência, há o problema de **consistência de memória**: sem sincronização, a JVM pode manter valores em caches por razões de performance; uma thread lê um valor desatualizado. `synchronized` resolve os dois problemas: (1) **exclusão mútua** — só uma thread executa a seção crítica por vez; (2) **visibilidade** — ao liberar o lock, as escritas tornam-se visíveis pela relação _happens-before_ do JMM.

## Por que importa

- **Corretude primeiro**: código não sincronizado com estado compartilhado produz resultados errados silenciosos — o tipo de bug mais difícil de reproduzir.
- **Fundamento para ferramentas modernas**: `ReentrantLock`, `AtomicInteger`, `ConcurrentHashMap` e Virtual Threads (pinning) só fazem sentido com `synchronized` como base de referência.
- **Recorrente em entrevistas**: race condition, deadlock, `volatile` vs `synchronized`, e `wait`/`notify` aparecem em toda entrevista sênior de Java.
- **Base do JMM**: a relação _happens-before_ gerada pelo `synchronized` é a garantia formal de visibilidade de memória entre threads.

## Como funciona

### Intrinsic lock / monitor

Todo objeto Java possui internamente um **intrinsic lock** (também chamado de _monitor lock_ ou simplesmente _monitor_). Esse lock é gerenciado automaticamente pela JVM.

Quando uma thread entra em um bloco ou método `synchronized`:

1. Ela tenta **adquirir** o intrinsic lock do objeto alvo.
2. Se o lock estiver livre, ela o adquire e prossegue.
3. Se outra thread já detém o lock, ela **bloqueia** (estado `BLOCKED`) até o lock ser liberado.
4. Ao sair do bloco/método — normalmente ou por exceção — ela **libera** o lock.

A liberação do lock estabelece uma relação _happens-before_ com qualquer aquisição subsequente do mesmo lock. Isso significa que tudo que a thread escreveu antes de liberar o lock será visível para a próxima thread que adquiri-lo.

### `synchronized` em methods, blocks e static

**Método de instância:** o lock é o objeto receptor (`this`).

```java
public class ContadorSeguro {
    private int valor = 0;

    // equivalente a synchronized(this)
    public synchronized void incrementar() {
        valor++;
    }

    public synchronized int get() {
        return valor;
    }
}
```

```java
// Exemplo de uso
ContadorSeguro c = new ContadorSeguro();

Thread t1 = new Thread(() -> {
    for (int i = 0; i < 10_000; i++) c.incrementar();
});
Thread t2 = new Thread(() -> {
    for (int i = 0; i < 10_000; i++) c.incrementar();
});
t1.start(); t2.start();
t1.join();  t2.join();
System.out.println(c.get()); // sempre 20000
```

**Bloco sincronizado com objeto explícito:** permite controle mais fino — apenas a seção crítica é protegida, e o lock pode ser um objeto privado em vez de `this`.

```java
public class Conta {
    private final Object lock = new Object();
    private long saldo = 0;

    public void depositar(long valor) {
        synchronized (lock) {       // seção crítica mínima
            saldo += valor;
        }
        // código não crítico pode ficar fora do bloco
    }

    public long getSaldo() {
        synchronized (lock) {
            return saldo;
        }
    }
}
```

Usar um objeto privado como lock em vez de `synchronized(this)` tem uma vantagem: código externo não consegue sincronizar no mesmo lock, evitando interferências indesejadas.

**Método estático:** o lock é o objeto `Class` da classe (por exemplo, `Conta.class`), que é distinto dos locks de instância.

```java
public class Configuracao {
    private static int versao = 0;

    // equivalente a synchronized(Configuracao.class)
    public static synchronized void atualizarVersao(int v) {
        versao = v;
    }

    public static synchronized int getVersao() {
        return versao;
    }
}
```

> [!note] Locks estáticos e de instância são independentes — se o mesmo campo pode ser acessado por métodos estáticos e de instância, um único lock deve proteger todos os caminhos.

### Reentrância

O mecanismo de `synchronized` em Java é **reentrante**: uma thread que já detém um lock pode adquiri-lo novamente sem bloquear. Internamente, o monitor mantém um contador de reentrância e só libera o lock quando o contador chega a zero.

```java
public class Base {
    public synchronized void metodoA() {
        System.out.println("Base.metodoA");
        metodoB(); // a mesma thread já detém o lock de 'this' → sem deadlock
    }

    public synchronized void metodoB() {
        System.out.println("Base.metodoB");
    }
}
```

Sem reentrância, `metodoA` chamando `metodoB` no mesmo objeto causaria um deadlock imediato. Subclasses também se beneficiam: `super.metodoA()` funciona mesmo que o lock já seja mantido.

### `wait` / `notify` / `notifyAll` e o loop de guarda (`while`, não `if`)

`synchronized` garante exclusão mútua, mas por si só não coordena **quando** uma thread deve agir. Para isso existem `wait`, `notify` e `notifyAll` — métodos de `Object` que só podem ser chamados por uma thread que detém o monitor do objeto.

| Método         | Efeito                                                                                      |
|----------------|---------------------------------------------------------------------------------------------|
| `wait()`       | Libera o lock e suspende a thread até que outra chame `notify`/`notifyAll` no mesmo objeto  |
| `notify()`     | Acorda uma thread arbitrária que está em `wait` no mesmo monitor                            |
| `notifyAll()`  | Acorda todas as threads em `wait` no mesmo monitor                                          |

**O loop de guarda é obrigatório.** A JVM permite **spurious wakeups** (despertar espúrio): uma thread pode ser acordada de `wait()` sem que nenhuma outra tenha chamado `notify`. Por isso, a condição deve ser re-testada após acordar:

```java
// CORRETO — while testa a condição após cada acordar
synchronized (lock) {
    while (!condicaoSatisfeita) {
        lock.wait();
    }
    // usa o recurso
}

// ERRADO — if não protege contra spurious wakeup
synchronized (lock) {
    if (!condicaoSatisfeita) {   // acorda, condição ainda é falsa → bug
        lock.wait();
    }
    // usa o recurso prematuramente
}
```

Prefira `notifyAll()` a `notify()`: `notify()` acorda uma thread arbitrária — se a thread acordada não for a que precisa agir, o sistema pode travar. `notifyAll()` acorda todas, deixando cada uma re-verificar a condição.

## Na prática

### Contador thread-safe

`ContadorSeguro` (definido acima, em "Como funciona") com duas threads concorrentes:

```java
// Teste: duas threads incrementando 10.000 vezes cada
ContadorSeguro contador = new ContadorSeguro();
Thread t1 = new Thread(() -> {
    for (int i = 0; i < 10_000; i++) contador.incrementar();
});
Thread t2 = new Thread(() -> {
    for (int i = 0; i < 10_000; i++) contador.incrementar();
});
t1.start(); t2.start();
t1.join();  t2.join();
// Resultado sempre determinístico: 20000
System.out.println(contador.get());
```

> [!note] Para contadores simples em código moderno
> `AtomicInteger` (lock-free, baseado em CAS) costuma ser mais eficiente que `synchronized` para contadores isolados. `synchronized` brilha quando a seção crítica envolve múltiplas variáveis que precisam ser atualizadas atomicamente juntas.

### Producer-consumer mínimo com wait/notify

O padrão clássico: um produtor gera itens; um consumidor os retira. A estrutura compartilhada (`Caixa`) coordena via `wait`/`notifyAll`.

```java
public class Caixa {
    private String mensagem;
    private boolean vazia = true;

    /** Consumidor chama: bloqueia enquanto não há mensagem. */
    public synchronized String retirar() {
        while (vazia) {
            try {
                wait(); // libera lock e dorme
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
        vazia = true;
        notifyAll(); // avisa produtor que pode depositar
        return mensagem;
    }

    /** Produtor chama: bloqueia enquanto caixa está cheia. */
    public synchronized void depositar(String msg) {
        while (!vazia) {
            try {
                wait(); // libera lock e dorme
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
        vazia = false;
        this.mensagem = msg;
        notifyAll(); // avisa consumidor que há mensagem
    }
}
```

```java
Caixa caixa = new Caixa();

Thread produtor = new Thread(() -> {
    String[] itens = {"alfa", "beta", "gama", "DONE"};
    for (String item : itens) {
        caixa.depositar(item);
    }
});

Thread consumidor = new Thread(() -> {
    String item;
    while (!(item = caixa.retirar()).equals("DONE")) {
        System.out.println("Recebido: " + item);
    }
});

produtor.start();
consumidor.start();
```

> [!note] Em código de produção
> Prefira `java.util.concurrent.BlockingQueue` (ex.: `LinkedBlockingQueue`) — ela encapsula exatamente esse padrão de forma mais robusta e sem risco de esquecer o `while`.

## Armadilhas

### (1) Lock instável — `String`, `Integer` ou objeto que muda

**O problema:** sincronizar em um objeto que pode ser substituído por outro (ou que é compartilhado globalmente sem você saber) faz com que o lock mude de identidade entre chamadas. Threads diferentes acabam adquirindo locks diferentes, anulando a proteção.

```java
// RUIM — String literals são internadas (interned): outra parte do
// código pode sincronizar no mesmo objeto literalmente
private String lock = "meuLock";
public void operacao() {
    synchronized (lock) { /* ... */ }
}

// RUIM — autoboxing cria novos objetos Long para valores fora de [-128, 127]
private Long contador = 0L;
public void incrementar() {
    synchronized (contador) {  // contador++ cria novo Long → lock muda!
        contador++;
    }
}
```

```java
// BOM — objeto final dedicado: identidade fixa, privado, sem compartilhamento externo
private final Object lock = new Object();
public void operacao() {
    synchronized (lock) { /* ... */ }
}
```

A regra: o objeto usado como lock **deve** ser `final` e **não deve** ser um tipo que sofre autoboxing nem uma String literal.

---

### (2) `if` em vez de `while` no `wait` — spurious wakeup

**O problema:** a JVM especifica que `wait()` pode retornar sem que nenhuma thread tenha chamado `notify`. Se a condição for testada com `if`, a thread prosseguirá mesmo que a condição ainda seja falsa.

```java
// RUIM — if não reprotege contra spurious wakeup
synchronized (lock) {
    if (fila.isEmpty()) {
        lock.wait(); // acorda espontaneamente → fila ainda está vazia
    }
    processar(fila.poll()); // NPE ou processamento incorreto!
}
```

```java
// BOM — while garante re-verificação após cada acordar
synchronized (lock) {
    while (fila.isEmpty()) {
        lock.wait();
    }
    processar(fila.poll()); // seguro: fila tem item
}
```

O `while` é obrigatório mesmo que você confie em `notifyAll()`: entre o momento em que a thread acorda e o momento em que ela re-adquire o lock, outra thread pode ter consumido o item.

---

### (3) Escopo de `synchronized` amplo demais — contenção excessiva

**O problema:** sincronizar um método inteiro quando apenas uma pequena parte acessa estado compartilhado força threads a esperar por operações desnecessárias, reduzindo o paralelismo.

```java
// RUIM — lock mantido durante operação longa que não precisa de exclusão
public synchronized void processarArquivo(Path arquivo) {
    List<String> linhas = lerArquivo(arquivo); // I/O: pode demorar segundos!
    dados.addAll(linhas);                       // única parte crítica
    enviarParaLog(linhas);                      // não precisa do lock
}
```

```java
// BOM — lock apenas na seção realmente crítica
public void processarArquivo(Path arquivo) {
    List<String> linhas = lerArquivo(arquivo); // fora do lock: sem contenção
    synchronized (this) {
        dados.addAll(linhas);                   // seção crítica mínima
    }
    enviarParaLog(linhas);                      // fora do lock
}
```

Segure o lock pelo menor tempo possível. Operações de I/O, chamadas de rede e cálculos pesados raramente precisam estar dentro de um bloco sincronizado.

## Em entrevista

### Frase pronta (inglês)

> "The `synchronized` keyword in Java provides mutual exclusion by associating an intrinsic lock — also called a monitor — with every object. When a thread enters a synchronized method or block, it acquires that lock; any other thread attempting to enter a synchronized section guarded by the same lock will block until the first thread releases it. This acquisition and release of the lock also establishes a happens-before relationship, meaning all writes performed by the releasing thread are guaranteed to be visible to the next thread that acquires the same lock — which is the memory-visibility guarantee on top of the mutual-exclusion guarantee. For `wait`/`notify` coordination, the pattern always uses a `while` loop — not `if` — to test the condition after waking up, because the JVM allows spurious wakeups: a thread can return from `wait` without any call to `notify`, so you must re-verify the condition before proceeding."

Use essa resposta para perguntas como *"How does `synchronized` work in Java?"*, *"What is an intrinsic lock?"*, *"Why do we use `while` instead of `if` with `wait`?"*.

### Vocabulário

| Termo PT                          | Termo EN                                          |
|-----------------------------------|---------------------------------------------------|
| exclusão mútua                    | mutual exclusion                                  |
| lock intrínseco / monitor         | intrinsic lock / monitor lock                     |
| seção crítica                     | critical section                                  |
| condição de corrida               | race condition                                    |
| despertar espúrio                 | spurious wakeup                                   |
| reentrância                       | reentrancy / reentrant synchronization            |
| contenção de lock                 | lock contention                                   |
| visibilidade de memória           | memory visibility                                 |
| acontece antes                    | happens-before                                    |
| bloqueio (thread)                 | blocking / blocked state                          |
| bloco sincronizado                | synchronized block / synchronized statement       |
| método sincronizado               | synchronized method                               |

## Veja também

- [[02 - Threads e seu ciclo de vida]]
- [[04 - As armadilhas - race, deadlock e companhia]]
- [[05 - Locks explícitos]]
- [[11 - Java Memory Model em profundidade]]
- [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|MOC do galho]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[Java Concurrency]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#Synchronized|synchronized]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#Monitor (intrinsic lock)|monitor]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#Mutual exclusion (exclusão mútua)|mutual exclusion]]

## Referências

- [Synchronization — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/essential/concurrency/sync.html)
- [Synchronized Methods — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/essential/concurrency/syncmeth.html)
- [Intrinsic Locks and Synchronization — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/essential/concurrency/locksync.html)
- [Guarded Blocks — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/essential/concurrency/guardmeth.html)
- Goetz, Brian et al. *Java Concurrency in Practice*. Addison-Wesley, 2006. Caps. 2 (Thread Safety), 3 (Sharing Objects).
