---
title: "Java Fundamentals"
created: 2026-04-01
updated: 2026-06-04
type: concept
progress: backlog
status: evergreen
tags:
  - java
  - entrevista
publish: false
---

# Java Fundamentals

Guia comprehensive da linguagem Java — do básico ao moderno (Java 8 → 25). Para um senior em entrevista internacional, o que importa não é decorar sintaxe — é **entender a JVM**, **dominar Collections e Streams**, **saber quando usar cada feature** e **reconhecer as armadilhas clássicas**. Para deep dive em concorrência (Memory Model, locks, Virtual Threads), veja [[Java Concurrency]].

## O que é

Java é uma linguagem **orientada a objetos**, **fortemente e estaticamente tipada**, **compilada para bytecode**, **garbage-collected**, e projetada em torno do princípio **"write once, run anywhere"** via JVM. Criada em 1995 por James Gosling na Sun Microsystems (hoje Oracle), é a espinha dorsal de sistemas enterprise, microserviços backend, Android (até recentemente), big data (Hadoop, Spark, Kafka), e de toda a stack Spring.

Em entrevistas, o que diferencia um senior em Java:

1. **Entender a JVM** — memória, GC, JIT, classloader — não apenas usar como caixa preta
2. **Dominar Collections** — saber escolher `ArrayList` vs `LinkedList` vs `ArrayDeque` com argumentos
3. **Streams com parcimônia** — saber quando Stream adiciona clareza e quando for-loop é melhor
4. **Concorrência** — Memory Model, happens-before, quando usar `synchronized` vs `Lock` vs atômicos
5. **Modern Java** — Records, pattern matching, sealed classes, Virtual Threads
6. **Pitfalls** — autoboxing em loops, `==` em Strings, mutação acidental, exceptions mal tratadas

---

## JVM (Java Virtual Machine)

> [!info] Migra em galho futuro
> Este tópico será expandido em galho próprio (Galho 3 (JVM por dentro)). Por ora permanece aqui.

A JVM é o ambiente de execução que faz Java portátil. Entender como ela funciona é o que diferencia um senior de um junior.

### Pipeline de compilação e execução

```
Código fonte              Bytecode              Código nativo
(.java)          javac    (.class)              (arquitetura específica)
   │    ─────────────►       │      JIT (runtime)       │
   │                         │    ─────────────────►    │
   │                         │                          │
  texto                 instruções JVM              instruções da CPU
                        (stack-based)                  (x86, ARM)
```

1. **`javac`** compila `.java` → `.class` (bytecode JVM). O bytecode é independente de plataforma.
2. **Classloader** carrega as classes sob demanda na JVM.
3. **Bytecode verifier** valida que o bytecode é seguro (sem violar tipagem, sem corromper stack).
4. **Interpreter** executa o bytecode inicialmente, instrução por instrução.
5. **JIT (Just-In-Time) Compiler** monitora código quente (hot paths) e compila para código nativo otimizado.
6. **Garbage Collector** gerencia memória automaticamente.

### Bytecode — uma olhada

```java
public int sum(int a, int b) { return a + b; }
```

Compila para:

```
public int sum(int, int);
  Code:
     0: iload_1      // push a
     1: iload_2      // push b
     2: iadd         // pop 2, add, push result
     3: ireturn      // return
```

A JVM é **stack-based** (não register-based como x86). Operações trabalham sobre uma pilha de operandos. Isso simplifica o bytecode e torna-o portátil. Você pode inspecionar bytecode com `javap -c ClassName`.

### Memory areas

A JVM divide memória em regiões com propósitos distintos:

```
┌───────────────────────────────────────────────────────┐
│ JVM Memory                                            │
│                                                       │
│  ┌─────────────────────────────────────────┐          │
│  │ Heap (compartilhada entre threads)      │          │
│  │  ┌────────────┐  ┌──────────────────┐   │          │
│  │  │ Young Gen  │  │ Old Gen (Tenured)│   │          │
│  │  │ ┌────┐     │  │                  │   │          │
│  │  │ │Eden│ S0 S1  │                  │   │          │
│  │  │ └────┘     │  │                  │   │          │
│  │  └────────────┘  └──────────────────┘   │          │
│  └─────────────────────────────────────────┘          │
│                                                       │
│  ┌─────────────────────────────────────────┐          │
│  │ Metaspace (metadata de classes)         │          │
│  │ (fora do heap, em memória nativa)       │          │
│  └─────────────────────────────────────────┘          │
│                                                       │
│  Por thread:                                          │
│  ┌──────────┐  ┌──────────┐  ┌────────────────┐      │
│  │ Stack    │  │ PC Reg   │  │ Native Method  │      │
│  │ (frames) │  │          │  │ Stack          │      │
│  └──────────┘  └──────────┘  └────────────────┘      │
└───────────────────────────────────────────────────────┘
```

**Heap** — onde objetos e arrays vivem. Compartilhada entre threads. Gerenciada pelo GC.

- **Young Generation** — objetos novos. Subdividida em **Eden** (alocação inicial) e 2 **Survivor spaces** (S0, S1). A maioria dos objetos morre jovem (weak generational hypothesis).
- **Old Generation (Tenured)** — objetos que sobreviveram múltiplos ciclos de GC no Young. Coletados menos frequentemente.
- **Humongous objects** (G1) — objetos > 50% do tamanho de uma region vão direto para o Old.

**Metaspace** (Java 8+) — metadata de classes carregadas (substituiu **PermGen**, que tinha tamanho fixo e gerava `OutOfMemoryError: PermGen space`). Metaspace cresce dinamicamente em memória nativa.

**Stack** — uma por thread. Contém stack frames (um por chamada de método), com variáveis locais, operandos e referências. `StackOverflowError` acontece quando a stack enche (recursão infinita).

**PC Register** — program counter, por thread. Aponta para a próxima instrução bytecode.

**Native Method Stack** — stack para código nativo (JNI).

**Code Cache** — área onde o JIT armazena código nativo compilado.

### Garbage Collection

O GC libera memória de objetos não mais referenciáveis. Java tem vários algoritmos disponíveis:

| GC                   | Introduzido       | Pausas                      | Throughput | Uso ideal                          |
| -------------------- | ----------------- | --------------------------- | ---------- | ---------------------------------- |
| **Serial**           | sempre            | Altas (stop-the-world)      | Baixo      | Single-thread, apps pequenos       |
| **Parallel**         | Java 5            | Altas                       | Alto       | Batch processing, throughput-first |
| **CMS** (deprecated) | Java 5            | Médias                      | Médio      | Latência — substituído por G1      |
| **G1** (default)     | Java 9            | Previsíveis (configuráveis) | Bom        | **Default moderno, uso geral**     |
| **ZGC**              | Java 15           | **< 1ms**                   | Bom        | Low-latency, heaps grandes (TB)    |
| **Shenandoah**       | Java 12 (Red Hat) | < 10ms                      | Bom        | Low-latency, alternativa a ZGC     |
| **Epsilon**          | Java 11           | N/A (não coleta)            | Máximo     | Testing, short-lived apps          |

**G1 GC (default):**

- Divide o heap em **regions** (1-32 MB)
- Coleta incrementalmente as regions "mais lucrativas" (mais lixo por tempo gasto)
- Tenta atingir um **pause time target** configurável (`-XX:MaxGCPauseMillis=200`)
- Mistura Young e Old collections (mixed GC)

**ZGC (Java 15+):**

- **Concurrent** — faz quase tudo em paralelo com a aplicação
- Pausas consistentemente **< 1ms** mesmo em heaps de TB
- Custo: mais overhead de CPU e memória que G1
- Uso: sistemas de baixa latência (trading, real-time)

### Como escolher GC

**Regras práticas:**

- **Default:** G1 — cobre a maioria dos casos
- **Latência crítica (p99.9 < 10ms):** ZGC ou Shenandoah
- **Batch / throughput:** Parallel GC
- **Heap pequeno (< 512 MB):** Serial pode ser suficiente

**Flags úteis:**

```bash
# G1 com pause target de 200ms
java -XX:+UseG1GC -XX:MaxGCPauseMillis=200 -jar app.jar

# ZGC
java -XX:+UseZGC -jar app.jar

# Heap size
java -Xms512m -Xmx4g -jar app.jar

# Log de GC (diagnóstico)
java -Xlog:gc*:file=gc.log:time,level,tags -jar app.jar

# Heap dump em OOM
java -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/tmp/ -jar app.jar
```

### JIT Compiler

A JVM HotSpot combina interpretação com compilação JIT:

- **C1 (Client compiler)** — compila rápido, otimizações leves. Usado para startup rápido.
- **C2 (Server compiler)** — compila mais devagar, otimizações agressivas. Usado após identificar código quente.
- **Tiered compilation** (default) — começa interpretando, promove para C1, depois C2 quando o código aquece.

**Otimizações comuns do C2:**

- **Inlining** — substitui chamada de método pelo corpo (se pequeno e chamado frequentemente)
- **Escape analysis** — se um objeto não "escapa" do método, pode ser alocado na stack (não no heap)
- **Dead code elimination**
- **Loop unrolling**
- **Lock elision** — remove `synchronized` desnecessário
- **Branch prediction** — otimiza para o caminho mais frequente

**Implicação prática:** benchmarks ingênuos mentem. Sempre use **JMH** (Java Microbenchmark Harness) para medir código Java — ele lida com warmup, dead code elimination, e outros artefatos do JIT.

### Classloader

Carrega `.class` files na JVM sob demanda. Hierarquia padrão:

```
Bootstrap ClassLoader  → carrega rt.jar (java.lang, java.util, etc.)
    ↑
Platform ClassLoader   → carrega APIs da plataforma
    ↑
Application ClassLoader → carrega classpath da aplicação
    ↑
Custom ClassLoaders    → WARs em Tomcat, plugins, etc.
```

**Parent delegation:** quando um classloader recebe um pedido para carregar uma classe, delega primeiro ao parent. Isso evita que código de usuário sobrescreva classes core (ex.: definir seu próprio `java.lang.String`).

**Custom classloaders** são usados por:

- Servers de aplicação (isolar WARs)
- Frameworks de plugins (carregar módulos dinamicamente)
- Hot reload (recarregar classes alteradas)

### Project Loom e Virtual Threads

→ Detalhes em [[Java Concurrency]]. Em resumo: Virtual Threads (Java 21) são threads leves gerenciadas pela JVM, não pelo OS. Permitem milhões de threads concorrentes, ideais para I/O-bound.

---

## Sintaxe básica e tipos

> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Java/Linguagem e sintaxe moderna/index|Linguagem e sintaxe moderna]]. Veja [[02 - Tipos, variáveis e operadores]].

---

## Estruturas de controle

> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Java/Linguagem e sintaxe moderna/index|Linguagem e sintaxe moderna]]. Veja [[03 - Estruturas de controle e fluxo]].

---

## Strings

> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Java/Linguagem e sintaxe moderna/index|Linguagem e sintaxe moderna]]. Veja [[04 - Strings e text blocks]].

---

## Arrays

> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Java/Linguagem e sintaxe moderna/index|Linguagem e sintaxe moderna]]. Veja [[05 - Arrays e varargs]].

---

## OOP em Java

> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Java/Linguagem e sintaxe moderna/index|Linguagem e sintaxe moderna]]. Veja [[06 - Classes, objetos e encapsulamento]], [[07 - Herança e polimorfismo]], [[08 - Interfaces e classes abstratas]].

---

## Records (Java 16+)

> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Java/Linguagem e sintaxe moderna/index|Linguagem e sintaxe moderna]]. Veja [[13 - Records e record patterns]].

---

## Sealed Classes (Java 17+)

> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Java/Linguagem e sintaxe moderna/index|Linguagem e sintaxe moderna]]. Veja [[14 - Sealed classes e pattern matching]].

---

## Pattern Matching

> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Java/Linguagem e sintaxe moderna/index|Linguagem e sintaxe moderna]]. Veja [[14 - Sealed classes e pattern matching]].

---

## Annotations

> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Java/Linguagem e sintaxe moderna/index|Linguagem e sintaxe moderna]]. Veja [[11 - Annotations]].

---

## Collections Framework

> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Java/Collections e Streams/index|Collections, Streams e Programação Funcional]]. Veja [[01 - O Collections Framework]], [[02 - Listas, conjuntos e filas]], [[03 - Mapas]], [[06 - Comparable e Comparator]].

---

## Lambdas e Interfaces Funcionais

> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Java/Collections e Streams/index|Collections, Streams e Programação Funcional]]. Veja [[04 - Lambdas e interfaces funcionais]], [[13 - Composição funcional e funções de alta ordem]].

---

## Streams API

> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Java/Collections e Streams/index|Collections, Streams e Programação Funcional]]. Veja [[05 - Introdução à Stream API]], [[07 - Operações de Stream — intermediárias e terminais]], [[08 - Collectors e agrupamento]], [[09 - Streams primitivos]].

---

## Date/Time API (Java 8+)

> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Java/Collections e Streams/index|Collections, Streams e Programação Funcional]]. Veja [[11 - java.time — Date e Time API]].

---

## I/O (Arquivos)

> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Java/Collections e Streams/index|Collections, Streams e Programação Funcional]]. Veja [[12 - I-O moderno com java.nio.file]].

---

## Exceções

> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Java/Linguagem e sintaxe moderna/index|Linguagem e sintaxe moderna]]. Veja [[10 - Exceções e tratamento de erros]].

---

## Optional

> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Java/Collections e Streams/index|Collections, Streams e Programação Funcional]]. Veja [[10 - Optional]].

---

## Generics

> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Java/Linguagem e sintaxe moderna/index|Linguagem e sintaxe moderna]]. Veja [[12 - Generics em profundidade]].

---

## Concorrência (visão geral)

> [!info] Migra em galho futuro
> Este tópico será expandido em galho próprio (Galho 4 (Concorrência e paralelismo)). Por ora permanece aqui.

> **Deep dive:** [[Java Concurrency]] — Memory Model, happens-before, locks avançados, java.util.concurrent, Virtual Threads, Structured Concurrency, patterns e pitfalls.

### Primitivas essenciais

```java
// Thread básica (raramente criada diretamente em código moderno)
Thread thread = new Thread(() -> System.out.println("Running"));
thread.start();

// ExecutorService — pool gerenciado (preferido para código tradicional)
try (ExecutorService executor = Executors.newFixedThreadPool(4)) {
    Future<String> future = executor.submit(() -> fetchData());
    String result = future.get();  // bloqueia até completar
}  // executor fechado automaticamente (Java 19+)

// CompletableFuture — composição assíncrona declarativa
CompletableFuture.supplyAsync(() -> fetchUser(id))
    .thenApply(user -> enrichWithOrders(user))
    .thenAccept(user -> sendNotification(user))
    .exceptionally(ex -> { log.error("Failed", ex); return null; });

// Paralelismo com múltiplos CompletableFutures
var userFuture = CompletableFuture.supplyAsync(() -> fetchUser(id));
var ordersFuture = CompletableFuture.supplyAsync(() -> fetchOrders(id));
CompletableFuture.allOf(userFuture, ordersFuture).join();
User user = userFuture.join();
List<Order> orders = ordersFuture.join();
```

### Sincronização

- **`synchronized`** — implícito, mais simples, monitor intrínseco do objeto. Default para a maioria dos casos.
- **`ReentrantLock`** — explícito, `tryLock` com timeout, interruptível, fair mode. Para cenários avançados.
- **`volatile`** — garante **visibilidade** entre threads, mas não atomicidade. Para flags e publicação segura.
- **`java.util.concurrent.atomic`** — `AtomicInteger`, `AtomicReference`, `LongAdder` para operações atômicas lock-free.

### Virtual Threads (Java 21)

Threads leves gerenciadas pela JVM (não pelo OS). Ideais para **I/O-bound**.

```java
// Virtual threads — milhões de threads sem overhead
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    IntStream.range(0, 100_000).forEach(i ->
        executor.submit(() -> {
            var data = httpClient.send(request, bodyHandler);  // bloqueia, mas barato
            return process(data);
        })
    );
}
```

**Quando usar:**

- I/O-bound (HTTP, DB, fila) — ganho enorme
- CPU-bound — **não** ajuda (use platform threads)
- Código que já depende de ThreadLocal — pode não performar bem (use Scoped Values)

→ Para detalhes e patterns, ver [[Java Concurrency]]

---

## Features modernas por versão

> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Java/Linguagem e sintaxe moderna/index|Linguagem e sintaxe moderna]]. Veja [[15 - A evolução do Java (8 a 25)]].

---

## Armadilhas comuns

- **NullPointerException:** usar `Optional` para retornos, `Objects.requireNonNull()` para validação
- **Mutabilidade acidental:** `List.of()` é imutável, `Collections.unmodifiableList()` é view (original mutável!)
- **ConcurrentModificationException:** modificar coleção durante iteração. Usar `Iterator.remove()` ou Streams.
- **Autoboxing em loops:** `Integer` em vez de `int` em loops grandes = milhões de objetos
- **String concatenação em loop:** usar `StringBuilder`, não `+=`
- **`==` para comparar Strings:** usar `.equals()`. `==` funciona com literais por causa do pool, mas falha com `new String()`
- **Parallel streams sem pensar:** ForkJoinPool compartilhado, poucos elementos = overhead > ganho

## Na prática

Em projetos enterprise com Java 21, Records são o padrão para DTOs — eliminam boilerplate de equals/hashCode/toString mantendo imutabilidade. Streams e lambdas cobrem a maior parte das transformações de dados; CompletableFuture é o padrão para orquestrar chamadas paralelas a serviços externos. A adoção de Virtual Threads (Java 21) elimina a necessidade de tuning fino de thread pools em endpoints I/O-bound, simplificando a operação de microserviços com alto volume de chamadas blocking. Collections e Streams representam a maior fatia do uso cotidiano; concorrência e I/O completam o quadro em integrações e processamento assíncrono.

## Como explicar em inglês

> [!nota] Vocabulário de entrevista migrou para os galhos
> Cada nota dos galhos tem uma seção "Em entrevista" com frase pronta em inglês (3+ sentenças) e vocabulário PT→EN. Para Collections/Streams/funcional, ver [[03-Dominios/Java/Collections e Streams/index|Collections, Streams e Programação Funcional]]; para linguagem, [[03-Dominios/Java/Linguagem e sintaxe moderna/index|Linguagem e sintaxe moderna]]; para concorrência, [[03-Dominios/Java/Concorrência e paralelismo/index|Concorrência e paralelismo]].

## Recursos

- [Java Language Updates](https://docs.oracle.com/en/java/javase/21/language/index.html) — features por versão
- [JDK 22 Documentation](https://docs.oracle.com/en/java/javase/22/)
- [Java features desde JDK 8 ao 21](https://advancedweb.hu/a-categorized-list-of-all-java-and-jvm-features-since-jdk-8-to-21/)
- [Java Evolved](https://javaevolved.github.io/) — evolução da linguagem
- [O que são anotações no Java? (vídeo)](https://www.youtube.com/watch?v=d7oJwcGJWUk)
- [[Senda Java]] — trilha de aprendizado completa
- [[What should you do to stand out as a Java-Spring Boot Developer]]

## Veja também

- [[Spring Boot]]
- [[Testes em Java]]
- [[Orientação a Objetos]]
- [[Design Patterns]]
- [[03-Dominios/Java/Backend/Kafka/Kafka]]
- [[JavaFX]]
- [[03-Dominios/Java/Linguagem e sintaxe moderna/index|Linguagem e sintaxe moderna (galho)]]
