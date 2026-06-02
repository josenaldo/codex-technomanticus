---
title: "Java Fundamentals"
created: 2026-04-01
updated: 2026-06-02
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

> [!info] Migra em galho futuro
> Este tópico será expandido em galho próprio (Galho 2). Por ora permanece aqui.

### Hierarquia

```text
Iterable
  └── Collection
       ├── List     → ArrayList, LinkedList, Vector
       ├── Set      → HashSet, LinkedHashSet, TreeSet
       └── Queue    → PriorityQueue, ArrayDeque, LinkedList

Map (não é Collection)
  └── HashMap, LinkedHashMap, TreeMap, ConcurrentHashMap, Hashtable
```

### Comparativo detalhado

| Interface | Impl              | Estrutura interna               | Ordenado           | Duplicatas  | Null       | Thread-safe | Quando usar                |
| --------- | ----------------- | ------------------------------- | ------------------ | ----------- | ---------- | ----------- | -------------------------- |
| List      | ArrayList         | Array dinâmico                  | Inserção           | Sim         | Sim        | Não         | Default para listas        |
| List      | LinkedList        | Lista duplamente ligada         | Inserção           | Sim         | Sim        | Não         | Inserção/remoção no início |
| Set       | HashSet           | HashMap interno                 | Não                | Não         | 1 null     | Não         | Deduplicação               |
| Set       | LinkedHashSet     | HashMap + lista ligada          | Inserção           | Não         | 1 null     | Não         | Dedup mantendo ordem       |
| Set       | TreeSet           | Red-Black tree                  | Natural/Comparator | Não         | Não        | Não         | Conjunto ordenado          |
| Map       | HashMap           | Array de buckets + lista/árvore | Não                | Keys únicas | 1 null key | Não         | Default para mapas         |
| Map       | LinkedHashMap     | HashMap + lista ligada          | Inserção ou acesso | Keys únicas | 1 null key | Não         | Cache LRU                  |
| Map       | TreeMap           | Red-Black tree                  | Natural/Comparator | Keys únicas | Não        | Não         | Mapa ordenado              |
| Map       | ConcurrentHashMap | Segments com locks              | Não                | Keys únicas | Não        | Sim         | Concorrência               |
| Queue     | PriorityQueue     | Binary heap                     | Por prioridade     | Sim         | Não        | Não         | Top-K, scheduling          |
| Queue     | ArrayDeque        | Array circular                  | FIFO/LIFO          | Sim         | Não        | Não         | Stack ou Queue             |

### Operações comuns

```java
// List
List<String> names = new ArrayList<>(List.of("Ana", "Bruno", "Carlos"));
names.add("Diana");
names.get(0);              // "Ana"
names.remove("Bruno");
names.contains("Ana");     // true
names.indexOf("Carlos");   // 1
names.sort(Comparator.naturalOrder());
names.subList(0, 2);       // view (não cópia!)

// Set
Set<String> unique = new HashSet<>(names);
unique.add("Ana");         // false (já existe)

// Map
Map<String, Integer> scores = new HashMap<>();
scores.put("Ana", 95);
scores.getOrDefault("Bob", 0);         // 0
scores.putIfAbsent("Ana", 100);        // não sobrescreve
scores.merge("Ana", 5, Integer::sum);  // 95 + 5 = 100
scores.computeIfAbsent("Bob", k -> 0); // cria se não existe
scores.forEach((k, v) -> System.out.println(k + ": " + v));

// Coleções imutáveis (Java 9+)
List<String> immutable = List.of("a", "b", "c");
Map<String, Integer> immutableMap = Map.of("key", 1);
Set<String> immutableSet = Set.of("x", "y");
// .add(), .put() lançam UnsupportedOperationException

// Collections utilitários
Collections.unmodifiableList(list);   // view imutável (list original ainda é mutável!)
Collections.synchronizedList(list);   // wrapper thread-safe
Collections.singletonList("only");    // lista com 1 elemento
Collections.emptyList();              // lista vazia imutável
```

### Comparable vs Comparator

```java
// Comparable — ordem natural, implementado NA classe
public class Patient implements Comparable<Patient> {
    @Override
    public int compareTo(Patient other) {
        return this.name.compareTo(other.name);
    }
}

// Comparator — ordem customizada, FORA da classe
patients.sort(Comparator.comparing(Patient::getName));
patients.sort(Comparator.comparing(Patient::getAge).reversed());
patients.sort(Comparator.comparing(Patient::getSpecialty)
                        .thenComparing(Patient::getName));
```

### Iteração

```java
// for-each (mais comum)
for (Patient p : patients) { ... }

// Iterator (permite remover durante iteração)
Iterator<Patient> it = patients.iterator();
while (it.hasNext()) {
    Patient p = it.next();
    if (p.isInactive()) it.remove();
}

// forEach com lambda
patients.forEach(p -> System.out.println(p.getName()));

// Stream (processamento funcional)
patients.stream().filter(Patient::isActive).toList();
```

---

## Lambdas e Interfaces Funcionais

> [!info] Migra em galho futuro
> Este tópico será expandido em galho próprio (Galho 2). Por ora permanece aqui.

Introduzidas no Java 8. Lambdas são funções anônimas que implementam interfaces funcionais.

### Sintaxe

```java
// Sem lambda (classe anônima)
Comparator<String> comp = new Comparator<String>() {
    @Override
    public int compare(String a, String b) {
        return a.length() - b.length();
    }
};

// Com lambda
Comparator<String> comp = (a, b) -> a.length() - b.length();

// Method reference
Comparator<String> comp = Comparator.comparingInt(String::length);
```

### Interfaces funcionais do `java.util.function`

| Interface           | Assinatura               | Uso                         |
| ------------------- | ------------------------ | --------------------------- |
| `Function<T,R>`     | `R apply(T t)`           | Transformar T em R          |
| `Predicate<T>`      | `boolean test(T t)`      | Filtrar/testar condição     |
| `Consumer<T>`       | `void accept(T t)`       | Ação sem retorno (forEach)  |
| `Supplier<T>`       | `T get()`                | Factory, lazy evaluation    |
| `UnaryOperator<T>`  | `T apply(T t)`           | Transformar mantendo tipo   |
| `BiFunction<T,U,R>` | `R apply(T t, U u)`      | Transformar dois argumentos |
| `BiPredicate<T,U>`  | `boolean test(T t, U u)` | Testar com dois argumentos  |

### Method references

```java
// Static method
Function<String, Integer> parse = Integer::parseInt;

// Instance method de um tipo
Function<String, String> upper = String::toUpperCase;

// Instance method de um objeto
Consumer<String> printer = System.out::println;

// Constructor
Supplier<ArrayList<String>> factory = ArrayList::new;
```

### Composição de funções

```java
Function<String, String> trim = String::strip;
Function<String, String> lower = String::toLowerCase;
Function<String, String> process = trim.andThen(lower);

Predicate<Patient> active = Patient::isActive;
Predicate<Patient> senior = p -> p.getAge() > 60;
Predicate<Patient> activeSenior = active.and(senior);
```

---

## Streams API

> [!info] Migra em galho futuro
> Este tópico será expandido em galho próprio (Galho 2). Por ora permanece aqui.

Pipeline funcional para processar coleções. Introduzida no Java 8.

### Anatomia de um Stream

```text
Source (List, Array, File, Generator)
  → Operações intermediárias (lazy, retornam Stream)
  → Operação terminal (eager, produz resultado)
```

### Operações intermediárias

```java
stream.filter(p -> p.isActive())         // filtrar
      .map(Patient::getName)              // transformar
      .flatMap(name -> name.chars().boxed()) // 1→N (achatar)
      .distinct()                         // remover duplicatas
      .sorted()                           // ordenar (natural)
      .sorted(Comparator.comparing(Patient::getAge)) // ordenar custom
      .peek(System.out::println)          // debug (não usar em prod)
      .limit(10)                          // primeiros N
      .skip(5)                            // pular N
      .takeWhile(p -> p.getAge() < 60)    // até condição falhar (Java 9+)
      .dropWhile(p -> p.getAge() < 18)    // descartar até condição falhar
```

### Operações terminais

```java
// Coletar
.toList()                                 // Java 16+ (imutável)
.collect(Collectors.toList())             // mutável
.collect(Collectors.toSet())
.collect(Collectors.toMap(Patient::getId, Function.identity()))
.collect(Collectors.joining(", "))        // "Ana, Bruno, Carlos"

// Agrupar
.collect(Collectors.groupingBy(Patient::getSpecialty))  // Map<String, List<Patient>>
.collect(Collectors.groupingBy(Patient::getSpecialty, Collectors.counting())) // Map<String, Long>
.collect(Collectors.partitioningBy(Patient::isActive))  // Map<Boolean, List<Patient>>

// Reduzir
.count()
.min(Comparator.comparing(Patient::getAge))  // Optional<Patient>
.max(Comparator.comparing(Patient::getAge))
.reduce(0, (sum, p) -> sum + p.getAge(), Integer::sum)

// Buscar
.findFirst()     // Optional<T> — primeiro elemento
.findAny()       // Optional<T> — qualquer (útil em parallel)
.anyMatch(p -> p.getAge() > 60)   // boolean
.allMatch(Patient::isActive)
.noneMatch(p -> p.getName().isBlank())

// Iterar
.forEach(System.out::println)     // ação sem retorno
.forEachOrdered(...)              // garante ordem em parallel
```

### Streams primitivos

Evitam boxing/unboxing. Ganho significativo de performance em grandes volumes.

```java
IntStream.range(0, 100)           // 0 a 99
IntStream.rangeClosed(1, 100)     // 1 a 100
IntStream.of(1, 2, 3)

patients.stream()
    .mapToInt(Patient::getAge)    // IntStream
    .average()                    // OptionalDouble
    .orElse(0.0);

// Converter de volta
IntStream.range(0, 10).boxed()    // Stream<Integer>
```

### Exemplo completo

```java
// Relatório: top 5 especialidades com mais pacientes ativos
Map<String, Long> topSpecialties = patients.stream()
    .filter(Patient::isActive)
    .collect(Collectors.groupingBy(
        Patient::getSpecialty,
        Collectors.counting()
    ))
    .entrySet().stream()
    .sorted(Map.Entry.<String, Long>comparingByValue().reversed())
    .limit(5)
    .collect(Collectors.toMap(
        Map.Entry::getKey,
        Map.Entry::getValue,
        (a, b) -> a,
        LinkedHashMap::new  // mantém ordem
    ));
```

### Checklist de performance

1. `collect()` guarda tudo na memória? Pode reduzir em passo único (`sum`, `count`, `max`)?
2. Usar Streams primitivos (`IntStream`, `LongStream`) para evitar boxing
3. `sorted()` ou `distinct()` em dados grandes carrega tudo em memória
4. Filtros mais seletivos no início da pipeline
5. Operações de curto-circuito (`findFirst`, `limit`, `anyMatch`) quando possível
6. `parallelStream()` — só quando o overhead de threading compensa (dados grandes, operação CPU-intensive)
7. `flatMap` pode expandir demais o volume — monitorar

> **Fontes:**
>
> - [Java Streams — exemplo prático](https://computaria.gitlab.io/blog/2025/04/27/java-streams-exemplo)
> - [Java moderno com Peano](https://computaria.gitlab.io/blog/2025/03/10/peano-java-moderno)

---

## Date/Time API (Java 8+)

> [!info] Migra em galho futuro
> Este tópico será expandido em galho próprio (Galho 2). Por ora permanece aqui.

Substituiu o problemático `Date`/`Calendar`. Imutável, thread-safe.

```java
// Data
LocalDate today = LocalDate.now();
LocalDate birth = LocalDate.of(1985, 3, 15);
LocalDate parsed = LocalDate.parse("2026-04-01");

// Hora
LocalTime now = LocalTime.now();
LocalTime appointment = LocalTime.of(14, 30);

// Data + Hora
LocalDateTime dateTime = LocalDateTime.of(today, appointment);

// Com timezone
ZonedDateTime zonedNow = ZonedDateTime.now(ZoneId.of("America/Sao_Paulo"));
Instant instant = Instant.now();  // timestamp UTC (para persistência)

// Duração e período
Duration duration = Duration.between(start, end);   // horas, minutos, segundos
Period period = Period.between(birth, today);         // anos, meses, dias
int age = period.getYears();

// Formatação
DateTimeFormatter fmt = DateTimeFormatter.ofPattern("dd/MM/yyyy HH:mm");
String formatted = dateTime.format(fmt);
LocalDateTime parsed2 = LocalDateTime.parse("01/04/2026 14:30", fmt);

// Manipulação (imutável — retorna nova instância)
LocalDate nextWeek = today.plusWeeks(1);
LocalDate lastMonth = today.minusMonths(1);
LocalDate firstDayOfMonth = today.withDayOfMonth(1);
```

**Regra prática:**

- `LocalDate` / `LocalTime` / `LocalDateTime` — quando timezone não importa
- `ZonedDateTime` — quando precisa de timezone (agendamentos internacionais)
- `Instant` — para persistência e cálculos de duração (sempre UTC)

---

## I/O (Arquivos)

> [!info] Migra em galho futuro
> Este tópico será expandido em galho próprio (Galho 2). Por ora permanece aqui.

### java.nio.file (moderno — preferir)

```java
// Ler arquivo inteiro
String content = Files.readString(Path.of("data.txt"));
List<String> lines = Files.readAllLines(Path.of("data.txt"));

// Ler arquivo grande (streaming — não carrega tudo na memória)
try (Stream<String> stream = Files.lines(Path.of("large.csv"))) {
    long count = stream.filter(line -> line.contains("ERROR")).count();
}

// Escrever
Files.writeString(Path.of("output.txt"), "Hello");
Files.write(Path.of("output.txt"), lines);

// Operações de diretório
Files.exists(path);
Files.createDirectories(Path.of("a/b/c"));
Files.list(Path.of("."))             // Stream<Path> (nível 1)
     .filter(Files::isRegularFile)
     .forEach(System.out::println);
Files.walk(Path.of("."))             // Stream<Path> (recursivo)
     .filter(p -> p.toString().endsWith(".java"))
     .forEach(System.out::println);

// Copiar e mover
Files.copy(source, target, StandardCopyOption.REPLACE_EXISTING);
Files.move(source, target);
Files.delete(path);
```

### Try-with-resources

```java
try (var reader = new BufferedReader(new FileReader("data.csv"));
     var writer = new BufferedWriter(new FileWriter("output.csv"))) {
    String line;
    while ((line = reader.readLine()) != null) {
        writer.write(processLine(line));
        writer.newLine();
    }
} // ambos fechados automaticamente
```

---

## Exceções

> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Java/Linguagem e sintaxe moderna/index|Linguagem e sintaxe moderna]]. Veja [[10 - Exceções e tratamento de erros]].

---

## Optional

> [!info] Migra em galho futuro
> Este tópico será expandido em galho próprio (Galho 2). Por ora permanece aqui.

Wrapper para valores que podem ou não existir. Substitui `null`.

```java
Optional<Patient> patient = repository.findById(id);

String name = patient.map(Patient::getName).orElse("Desconhecido");
Patient p = patient.orElseThrow(() -> new PatientNotFoundException(id));
patient.ifPresent(pat -> sendWelcomeEmail(pat));
```

**Regras:**

- Usar como retorno de métodos que podem não ter resultado
- **Nunca** como parâmetro de método ou campo de classe
- **Nunca** usar `Optional.get()` sem verificar
- `Optional.empty()` em vez de retornar `null`

> **Fonte:** [Java Optional](https://computaria.gitlab.io/blog/2025/04/25/java-optional)

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

## How to explain in English

"Java has been my primary language for over 20 years, and I've seen it evolve significantly. Modern Java — 17 and beyond — is much more concise than the Java of 10 years ago. Records eliminate boilerplate for data classes, pattern matching simplifies type checking, and text blocks make working with multi-line strings natural.

The Collections Framework is something I use constantly. For most cases, ArrayList and HashMap cover 90% of needs. I reach for ConcurrentHashMap in multi-threaded scenarios and TreeMap when I need sorted iteration. Understanding the performance characteristics helps me make the right choice.

Streams and lambdas transformed how I write Java. Instead of imperative loops with mutable accumulators, I use declarative pipelines that are easier to read and parallelize. The key is knowing when Streams add clarity versus when a simple for-loop is better.

For concurrency, Virtual Threads in Java 21 are a game-changer. In traditional Java, each thread maps to an OS thread, limiting you to tens of thousands of concurrent connections. Virtual Threads are managed by the JVM and are much cheaper — you can have millions. This simplifies I/O-bound microservices enormously."

### Key vocabulary

- máquina virtual → JVM (Java Virtual Machine)
- coleta de lixo → garbage collection (GC)
- tipo genérico → generic type
- thread virtual → virtual thread (Project Loom)
- registro → record: classe imutável para dados
- fluxo → stream: pipeline de processamento funcional
- classe selada → sealed class
- inferência de tipo → type inference (`var`)
- sobrescrita → overriding: redefinir método na subclass
- sobrecarga → overloading: mesmo nome, parâmetros diferentes
- interface funcional → functional interface: interface com 1 método abstrato
- referência a método → method reference: `Class::method`

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
