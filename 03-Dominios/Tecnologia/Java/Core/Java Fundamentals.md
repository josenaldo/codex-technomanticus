---
title: "Java Fundamentals"
created: 2026-04-01
updated: 2026-06-05
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

> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Tecnologia/Java/JVM/index|JVM por dentro]]. Veja [[01 - A JVM — o que é e o pipeline de execução]], [[02 - Áreas de memória de runtime]], [[03 - Garbage Collection — o conceito]], [[06 - Os coletores do HotSpot]], [[07 - JIT — C1, C2 e tiered compilation]].

---

## Sintaxe básica e tipos

> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/index|Linguagem e sintaxe moderna]]. Veja [[02 - Tipos, variáveis e operadores]].

---

## Estruturas de controle

> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/index|Linguagem e sintaxe moderna]]. Veja [[03 - Estruturas de controle e fluxo]].

---

## Strings

> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/index|Linguagem e sintaxe moderna]]. Veja [[04 - Strings e text blocks]].

---

## Arrays

> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/index|Linguagem e sintaxe moderna]]. Veja [[05 - Arrays e varargs]].

---

## OOP em Java

> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/index|Linguagem e sintaxe moderna]]. Veja [[06 - Classes, objetos e encapsulamento]], [[07 - Herança e polimorfismo]], [[08 - Interfaces e classes abstratas]].

---

## Records (Java 16+)

> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/index|Linguagem e sintaxe moderna]]. Veja [[13 - Records e record patterns]].

---

## Sealed Classes (Java 17+)

> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/index|Linguagem e sintaxe moderna]]. Veja [[14 - Sealed classes e pattern matching]].

---

## Pattern Matching

> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/index|Linguagem e sintaxe moderna]]. Veja [[14 - Sealed classes e pattern matching]].

---

## Annotations

> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/index|Linguagem e sintaxe moderna]]. Veja [[11 - Annotations]].

---

## Collections Framework

> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Tecnologia/Java/Collections e Streams/index|Collections, Streams e Programação Funcional]]. Veja [[01 - O Collections Framework]], [[02 - Listas, conjuntos e filas]], [[03 - Mapas]], [[06 - Comparable e Comparator]].

---

## Lambdas e Interfaces Funcionais

> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Tecnologia/Java/Collections e Streams/index|Collections, Streams e Programação Funcional]]. Veja [[04 - Lambdas e interfaces funcionais]], [[13 - Composição funcional e funções de alta ordem]].

---

## Streams API

> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Tecnologia/Java/Collections e Streams/index|Collections, Streams e Programação Funcional]]. Veja [[05 - Introdução à Stream API]], [[07 - Operações de Stream — intermediárias e terminais]], [[08 - Collectors e agrupamento]], [[09 - Streams primitivos]].

---

## Date/Time API (Java 8+)

> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Tecnologia/Java/Collections e Streams/index|Collections, Streams e Programação Funcional]]. Veja [[11 - java.time — Date e Time API]].

---

## I/O (Arquivos)

> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Tecnologia/Java/Collections e Streams/index|Collections, Streams e Programação Funcional]]. Veja [[12 - I-O moderno com java.nio.file]].

---

## Exceções

> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/index|Linguagem e sintaxe moderna]]. Veja [[10 - Exceções e tratamento de erros]].

---

## Optional

> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Tecnologia/Java/Collections e Streams/index|Collections, Streams e Programação Funcional]]. Veja [[10 - Optional]].

---

## Generics

> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/index|Linguagem e sintaxe moderna]]. Veja [[12 - Generics em profundidade]].

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
> Expandido no galho [[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/index|Linguagem e sintaxe moderna]]. Veja [[15 - A evolução do Java (8 a 25)]].

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
> Cada nota dos galhos tem uma seção "Em entrevista" com frase pronta em inglês (3+ sentenças) e vocabulário PT→EN. Para Collections/Streams/funcional, ver [[03-Dominios/Tecnologia/Java/Collections e Streams/index|Collections, Streams e Programação Funcional]]; para linguagem, [[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/index|Linguagem e sintaxe moderna]]; para concorrência, [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Concorrência e paralelismo]].

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
- [[03-Dominios/Tecnologia/Java/Backend/Kafka/Kafka]]
- [[JavaFX]]
- [[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/index|Linguagem e sintaxe moderna (galho)]]
- [[03-Dominios/Tecnologia/Java/JVM/index|JVM por dentro (galho)]]
