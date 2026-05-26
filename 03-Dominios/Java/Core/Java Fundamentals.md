---
title: "Java Fundamentals"
created: 2026-04-01
updated: 2026-04-10
type: concept
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

### Tipos primitivos

| Tipo      | Tamanho | Range      | Wrapper     | Default  |
| --------- | ------- | ---------- | ----------- | -------- |
| `byte`    | 8 bits  | -128 a 127 | `Byte`      | 0        |
| `short`   | 16 bits | -32K a 32K | `Short`     | 0        |
| `int`     | 32 bits | -2B a 2B   | `Integer`   | 0        |
| `long`    | 64 bits | ±9.2×10¹⁸  | `Long`      | 0L       |
| `float`   | 32 bits | ±3.4×10³⁸  | `Float`     | 0.0f     |
| `double`  | 64 bits | ±1.7×10³⁰⁸ | `Double`    | 0.0      |
| `char`    | 16 bits | Unicode    | `Character` | '\u0000' |
| `boolean` | 1 bit   | true/false | `Boolean`   | false    |

**Autoboxing:** conversão automática entre primitivo e wrapper. Cuidado em loops (cria objetos).

### Igualdade

- **`==`** compara referência (mesmo objeto na memória)
- **`.equals()`** compara conteúdo (valor)
- **String pool:** `"hello" == "hello"` → `true` (interned), mas `new String("hello") == "hello"` → `false`
- **Contrato hashCode/equals:** se `a.equals(b)`, então `a.hashCode() == b.hashCode()`. Quebrar isso quebra HashMap.

### Casting e promoção

```java
// Promoção automática (widening): sem perda
int x = 10;
long y = x;        // int → long OK
double z = y;      // long → double OK

// Casting explícito (narrowing): pode perder dados
double d = 9.99;
int i = (int) d;   // 9 (trunca, não arredonda)
```

### Variáveis e escopo

- **Local:** dentro de método, sem valor default, deve ser inicializada
- **Instance (campo):** dentro da classe, tem valor default (0, null, false)
- **Static (classe):** compartilhada entre instâncias, acessada via `Class.field`
- **`var` (Java 10+):** inferência de tipo local. `var list = new ArrayList<String>();`
- **`final`:** valor não pode ser reatribuído (mas objetos mutáveis ainda podem ser alterados internamente)

---

## Estruturas de controle

### Condicionais

```java
// if-else
if (age >= 18) {
    status = "adult";
} else if (age >= 13) {
    status = "teen";
} else {
    status = "child";
}

// Ternário
String status = age >= 18 ? "adult" : "minor";

// Switch expression (Java 14+)
String result = switch (day) {
    case MONDAY, FRIDAY    -> "Work hard";
    case SATURDAY, SUNDAY  -> "Rest";
    default                -> "Normal day";
};
```

### Loops

```java
// for clássico
for (int i = 0; i < 10; i++) { ... }

// for-each (enhanced for)
for (String name : names) { ... }

// while
while (condition) { ... }

// do-while (executa ao menos uma vez)
do { ... } while (condition);

// break e continue
for (int i = 0; i < 100; i++) {
    if (i == 50) break;       // sai do loop
    if (i % 2 == 0) continue; // pula para próxima iteração
}
```

---

## Strings

Strings são **imutáveis** em Java. Toda operação retorna uma nova String.

```java
String s = "Hello";
s.length();                    // 5
s.charAt(0);                   // 'H'
s.substring(0, 3);             // "Hel"
s.toLowerCase();               // "hello"
s.contains("ell");             // true
s.indexOf("lo");               // 3
s.replace("Hello", "Hi");     // "Hi"
s.split(",");                  // String[]
s.strip();                     // remove espaços (Java 11+)
s.isBlank();                   // true se vazio ou só espaços (Java 11+)
```

**StringBuilder** — para concatenação em loops (mutável, mais eficiente):

```java
var sb = new StringBuilder();
for (int i = 0; i < 1000; i++) {
    sb.append(i).append(", ");
}
String result = sb.toString();
// NÃO fazer: result += i; em loop (cria 1000 Strings)
```

**Formatted strings (Java 15+):**

```java
String msg = "Patient %s, age %d".formatted(name, age);
// ou
String msg = STR."Patient \{name}, age \{age}"; // String templates (preview Java 21+)
```

---

## Arrays

Coleções de tamanho fixo. Tipo definido em compile-time.

```java
// Declaração e inicialização
int[] numbers = new int[5];          // [0, 0, 0, 0, 0]
int[] primes = {2, 3, 5, 7, 11};    // literal
String[] names = new String[3];      // [null, null, null]

// Acesso
primes[0];        // 2
primes.length;    // 5 (propriedade, não método)

// Multidimensional
int[][] matrix = {
    {1, 2, 3},
    {4, 5, 6}
};
matrix[1][2];     // 6

// Iterar
for (int n : primes) { System.out.println(n); }

// Utilitários
Arrays.sort(numbers);
Arrays.fill(numbers, 0);
Arrays.copyOf(primes, 10);          // copia e expande
Arrays.asList(primes);              // converte para List (tamanho fixo)
List.of(1, 2, 3);                   // List imutável (Java 9+)
```

---

## OOP em Java

### Classes e objetos

```java
public class Patient {
    // Campos (instance variables)
    private String name;
    private final LocalDate birthDate;
    private static int count = 0;   // compartilhado entre instâncias

    // Construtor
    public Patient(String name, LocalDate birthDate) {
        this.name = name;
        this.birthDate = birthDate;
        count++;
    }

    // Construtor sobrecarregado (overloaded)
    public Patient(String name) {
        this(name, LocalDate.now());  // chama outro construtor
    }

    // Métodos
    public String getName() { return name; }
    public int getAge() {
        return Period.between(birthDate, LocalDate.now()).getYears();
    }

    // Método estático
    public static int getCount() { return count; }
}
```

### Modificadores de acesso

| Modificador | Classe | Package | Subclass | Mundo |
| ----------- | ------ | ------- | -------- | ----- |
| `public`    | ✅      | ✅       | ✅        | ✅     |
| `protected` | ✅      | ✅       | ✅        | ❌     |
| (default)   | ✅      | ✅       | ❌        | ❌     |
| `private`   | ✅      | ❌       | ❌        | ❌     |

### Herança

```java
public class Doctor extends Patient {
    private String specialty;

    public Doctor(String name, LocalDate birthDate, String specialty) {
        super(name, birthDate);   // chama construtor do pai
        this.specialty = specialty;
    }

    @Override
    public String toString() {    // sobrescreve método do pai
        return "Dr. " + getName() + " (" + specialty + ")";
    }
}
```

**Regras de herança:**

- Java suporta herança simples (uma superclass). Múltipla apenas via interfaces.
- `final class` não pode ser estendida. `final method` não pode ser sobrescrito.
- Construtores não são herdados — subclass deve chamar `super()`.

### Overriding vs Overloading

| Aspecto     | Overriding (sobrescrita)               | Overloading (sobrecarga)                   |
| ----------- | -------------------------------------- | ------------------------------------------ |
| Onde        | Subclass redefine método da superclass | Mesma classe, métodos com mesmo nome       |
| Assinatura  | Mesma assinatura                       | Parâmetros diferentes (tipo ou quantidade) |
| Retorno     | Mesmo tipo ou covariante (subtipo)     | Pode ser diferente                         |
| Acesso      | Igual ou mais permissivo               | Qualquer                                   |
| `@Override` | Obrigatório (por convenção)            | Não se aplica                              |
| Binding     | Runtime (dynamic dispatch)             | Compile-time (static)                      |
| `static`    | Não pode ser sobrescrito (hidden)      | Pode ser sobrecarregado                    |

```java
// Overloading — mesmo nome, parâmetros diferentes
public double calculate(double price) { return price * 1.1; }
public double calculate(double price, double discount) { return price * (1 - discount); }

// Overriding — subclass redefine comportamento
@Override
public String toString() { return "Custom: " + name; }
```

### Classes abstratas vs Interfaces

```java
// Classe abstrata — pode ter estado e implementação
public abstract class Notification {
    protected String recipient;

    public Notification(String recipient) {
        this.recipient = recipient;
    }

    public abstract void send(String message); // subclass implementa

    public void log(String message) {          // implementação compartilhada
        System.out.println("Sent to " + recipient + ": " + message);
    }
}

// Interface — contrato puro (Java 8+: pode ter default methods)
public interface Sendable {
    void send(String message);                  // abstrato

    default void retry(String message, int times) {  // default method
        for (int i = 0; i < times; i++) {
            try { send(message); return; }
            catch (Exception e) { /* retry */ }
        }
    }

    static Sendable noOp() {                   // static method
        return message -> {};
    }
}
```

**Quando usar:**

- **Interface:** definir contrato. Uma classe pode implementar N interfaces.
- **Classe abstrata:** compartilhar estado e implementação entre subclasses. Herança simples.

### Enums

```java
public enum OrderStatus {
    PENDING("Pendente"),
    CONFIRMED("Confirmado"),
    SHIPPED("Enviado"),
    DELIVERED("Entregue"),
    CANCELLED("Cancelado");

    private final String label;

    OrderStatus(String label) { this.label = label; }

    public String getLabel() { return label; }

    // Enum pode ter métodos
    public boolean isFinal() {
        return this == DELIVERED || this == CANCELLED;
    }
}

// Uso
OrderStatus status = OrderStatus.PENDING;
OrderStatus.valueOf("PENDING");    // parse de String
OrderStatus.values();              // todos os valores
```

---

## Records (Java 16+)

Classes imutáveis para dados — elimina boilerplate de equals/hashCode/toString/getters. **Feature essencial do Java moderno.**

### Declaração

```java
// Um record define componentes imutáveis em uma linha
public record Patient(Long id, String name, LocalDate birthDate, String email) {}

// O compilador gera automaticamente:
// - Construtor canônico: public Patient(Long id, String name, LocalDate birthDate, String email)
// - Accessors: id(), name(), birthDate(), email() (sem "get" prefix!)
// - equals() e hashCode() baseados em todos os componentes
// - toString(): "Patient[id=42, name=Maria, birthDate=1985-03-15, email=...]"
```

### Validação no construtor compacto

```java
public record Patient(Long id, String name, LocalDate birthDate, String email) {
    // Compact constructor — valida ou normaliza antes do assignment automático
    public Patient {
        Objects.requireNonNull(id, "id is required");
        if (name == null || name.isBlank()) {
            throw new IllegalArgumentException("name is required");
        }
        if (birthDate != null && birthDate.isAfter(LocalDate.now())) {
            throw new IllegalArgumentException("birthDate cannot be in the future");
        }
        // Normalização — reassign é permitido no compact constructor
        name = name.strip();
        email = email != null ? email.toLowerCase() : null;
    }
}
```

### Métodos adicionais

```java
public record Money(BigDecimal amount, Currency currency) {
    // Construtor secundário
    public Money(double amount, String currencyCode) {
        this(BigDecimal.valueOf(amount), Currency.getInstance(currencyCode));
    }

    // Métodos de negócio
    public Money add(Money other) {
        if (!this.currency.equals(other.currency)) {
            throw new IllegalArgumentException("currency mismatch");
        }
        return new Money(this.amount.add(other.amount), this.currency);
    }

    public boolean isZero() {
        return amount.compareTo(BigDecimal.ZERO) == 0;
    }

    // Static factory
    public static Money zero(Currency currency) {
        return new Money(BigDecimal.ZERO, currency);
    }
}
```

### Records implementam interfaces

```java
public interface Identifiable {
    Long id();
}

public record Patient(Long id, String name) implements Identifiable {}
// Record já implementa id() pelo accessor automático
```

### Record patterns (Java 21+)

```java
// Pattern matching desestruturando o record
record Point(int x, int y) {}
record Circle(Point center, double radius) {}

Object shape = new Circle(new Point(0, 0), 5);

// Desestruturação aninhada
if (shape instanceof Circle(Point(int x, int y), double r)) {
    System.out.println("Circle at (" + x + "," + y + ") radius " + r);
}

// Em switch
String describe(Object obj) {
    return switch (obj) {
        case Circle(Point(int x, int y), double r)
            when r > 10 -> "Big circle at " + x + "," + y;
        case Circle(Point p, double r) -> "Small circle";
        case Point(int x, int y) -> "Point at " + x + "," + y;
        case null -> "nothing";
        default -> "unknown";
    };
}
```

### Quando usar records

**Ideais para:**

- **DTOs** — request/response em APIs REST (elimina classes anêmicas)
- **Value Objects (DDD)** — `Money`, `Email`, `CPF`, `Coordinates`
- **Tuplas** — retornos multi-valor sem criar classe
- **Projections** — em Spring Data JPA (`SELECT new Record(...)`)
- **Dados imutáveis** em geral

**NÃO são ideais quando:**

- Você precisa de herança (records são `final`)
- A classe tem lógica mutável
- Você precisa de JavaBean convention (`getName()` em vez de `name()`) — alguns frameworks antigos assumem isso

### Records em Spring Boot

```java
// DTO de request
public record CreatePatientRequest(
    @NotBlank String name,
    @Email @NotBlank String email,
    @Past @NotNull LocalDate birthDate
) {}

// DTO de response
public record PatientResponse(Long id, String name, String email, int age) {
    public static PatientResponse from(Patient patient) {
        return new PatientResponse(
            patient.getId(),
            patient.getName(),
            patient.getEmail(),
            Period.between(patient.getBirthDate(), LocalDate.now()).getYears()
        );
    }
}

// Controller
@PostMapping("/patients")
public PatientResponse create(@Valid @RequestBody CreatePatientRequest req) {
    Patient saved = service.create(req);
    return PatientResponse.from(saved);
}
```

---

## Sealed Classes (Java 17+)

Controla **quem pode estender** uma classe/interface. Permite o compilador saber o conjunto **exaustivo** de subtipos.

```java
public sealed interface Shape permits Circle, Rectangle, Triangle {}

public record Circle(double radius) implements Shape {}
public record Rectangle(double width, double height) implements Shape {}
public record Triangle(double base, double height) implements Shape {}

// Exhaustive pattern matching — compilador exige tratar todos os casos
double area(Shape shape) {
    return switch (shape) {
        case Circle c     -> Math.PI * c.radius() * c.radius();
        case Rectangle r  -> r.width() * r.height();
        case Triangle t   -> 0.5 * t.base() * t.height();
        // Sem default! Compilador garante exaustividade
    };
}
```

**Modificadores dos subtipos:**

- `final` — não pode ser estendido
- `sealed` — só pode ser estendido pelo `permits` declarado
- `non-sealed` — volta a ser aberto (qualquer um pode estender)

**Uso prático:**

- Algebraic Data Types (ADTs) no Java — hierarquias fechadas (`Result<T> = Success<T> | Failure`)
- Domain modeling — "um pedido é um de {Draft, Confirmed, Shipped, Delivered, Cancelled}"
- API design — garantir que subtipos sejam controlados

```java
// Result type usando sealed + records
public sealed interface Result<T> permits Success, Failure {
    record Success<T>(T value) implements Result<T> {}
    record Failure<T>(String error) implements Result<T> {}

    static <T> Result<T> ok(T value) { return new Success<>(value); }
    static <T> Result<T> fail(String error) { return new Failure<>(error); }
}

// Uso com pattern matching
Result<User> result = fetchUser(id);
String message = switch (result) {
    case Success<User>(User u) -> "Got " + u.name();
    case Failure<User>(String err) -> "Error: " + err;
};
```

---

## Pattern Matching

Evoluiu em várias versões. Hoje (Java 21+) é um dos pontos fortes do Java moderno.

### instanceof pattern (Java 16)

```java
// Antes
if (obj instanceof String) {
    String s = (String) obj;
    System.out.println(s.length());
}

// Com pattern
if (obj instanceof String s) {
    System.out.println(s.length());
}

// Em condição
if (obj instanceof String s && !s.isBlank()) {
    process(s);
}
```

### Switch patterns (Java 21)

```java
String describe(Object obj) {
    return switch (obj) {
        case null            -> "null";
        case Integer i when i < 0  -> "negative int: " + i;
        case Integer i       -> "int: " + i;
        case String s        -> "string of length " + s.length();
        case int[] arr       -> "int array of length " + arr.length;
        case List<?> list    -> "list with " + list.size() + " elements";
        default              -> "something else";
    };
}
```

### Record patterns (Java 21)

Ver seção [Records](#records-java-16) acima.

### Primitive patterns (Java 23+)

```java
// Preview
Object o = 42;
switch (o) {
    case int i  -> System.out.println("int: " + i);
    case long l -> System.out.println("long: " + l);
    // ...
}
```

---

## Annotations

Metadata no código. Processadas em compile-time ou runtime.

```java
// Built-in
@Override          // verifica que está sobrescrevendo
@Deprecated        // marca como obsoleto
@SuppressWarnings  // silencia warnings
@FunctionalInterface // garante que interface tem 1 método abstrato

// Custom annotation
@Target(ElementType.FIELD)
@Retention(RetentionPolicy.RUNTIME)
public @interface NotEmpty {
    String message() default "Field cannot be empty";
}
```

**Em Spring:** `@Service`, `@Repository`, `@RestController`, `@Autowired`, `@Transactional` — annotations são o mecanismo principal de configuração.

> **Fonte:** [O que são anotações no Java? (vídeo)](https://www.youtube.com/watch?v=d7oJwcGJWUk)

---

## Collections Framework

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

Hierarquia: `Throwable` → `Error` (sistema, não tratar) e `Exception` (aplicação).

```text
Throwable
  ├── Error (OutOfMemoryError, StackOverflowError, VirtualMachineError)
  │   → não capturar — sistema está em estado inconsistente
  └── Exception
       ├── IOException, SQLException, InterruptedException, ...
       │   → CHECKED — compilador obriga a tratar
       └── RuntimeException
            ├── NullPointerException
            ├── IllegalArgumentException
            ├── IllegalStateException
            ├── IndexOutOfBoundsException
            ├── ClassCastException
            ├── ArithmeticException
            └── ... → UNCHECKED — não precisa declarar
```

### Checked vs Unchecked: o debate eterno

**Checked exceptions** foram uma inovação do Java que hoje é vista como erro de design por muitos (incluindo Rod Johnson, criador do Spring). Problemas:

- **Poluição de assinatura** — `throws IOException, SQLException, ...` em toda a chain
- **Vazam implementação** — interface de alto nível herda detalhes do DAO
- **Difíceis em lambdas e streams** — `Consumer<T>` não declara checked exceptions
- **Frequentemente ignoradas** — `catch (Exception e) {}` vazio para silenciar o compilador

**Tendência moderna:** maioria das bibliotecas modernas (Spring, JPA, Reactor) usam **unchecked**. O próprio Java evoluiu — `java.io` em NIO.2 lança `UncheckedIOException` onde faz sentido.

**Regra prática:**

- **Checked** — apenas se o caller pode e deve recuperar da falha (raro)
- **Unchecked** — default para tudo o mais

### Try-catch-finally e try-with-resources

```java
// Try-with-resources — fecha automaticamente recursos que implementam AutoCloseable
try (var reader = Files.newBufferedReader(Path.of("data.txt"));
     var writer = Files.newBufferedWriter(Path.of("out.txt"))) {
    String line;
    while ((line = reader.readLine()) != null) {
        writer.write(process(line));
        writer.newLine();
    }
} catch (IOException e) {
    log.error("Failed to process file", e);
    throw new ProcessingException("File processing failed", e);  // preserva cause
}
// Recursos fechados automaticamente, mesmo em exceção
```

**Suppressed exceptions:** se o `close()` do recurso lançar durante cleanup após outra exceção, a segunda é **suprimida** (não substitui a original). Acessível via `throwable.getSuppressed()`.

### Custom exceptions: boas práticas

```java
// Exceção de domínio com contexto rico
public class PatientNotFoundException extends RuntimeException {
    private final Long patientId;

    public PatientNotFoundException(Long id) {
        super("Patient not found: id=" + id);
        this.patientId = id;
    }

    public Long getPatientId() { return patientId; }
}

// Exception chaining — preserve a causa original
public class ServiceException extends RuntimeException {
    public ServiceException(String message, Throwable cause) {
        super(message, cause);
    }
}

try {
    repository.save(patient);
} catch (DataAccessException e) {
    throw new ServiceException("Failed to save patient " + patient.getId(), e);
}
```

**Regras:**

- **Herdar de `RuntimeException`** para unchecked
- **Mensagens úteis** — incluam o dado relevante (`id=42`, não apenas "not found")
- **Preservar a cause** — nunca `throw new X("...")` descartando a original
- **Exceções de domínio** no package do domínio, não em `util.exceptions`

### Anti-patterns

```java
// RUIM — silenciar exceção
try {
    doSomething();
} catch (Exception e) { }  // Swallow — bug escondido

// RUIM — logar e throw
try {
    doSomething();
} catch (Exception e) {
    log.error("Error", e);
    throw e;  // Loga 2x (aqui e em cima na stack)
}
// → Escolha: logar OU throw, não ambos. Se tratar, log. Se propagar, não log.

// RUIM — catch genérico
try {
    doSomething();
} catch (Throwable t) { ... }  // Captura Error também, muito amplo

// RUIM — perder a cause
try {
    doSomething();
} catch (IOException e) {
    throw new RuntimeException("Failed");  // Cause perdida!
}
// BOM
throw new RuntimeException("Failed", e);

// RUIM — exception para controle de fluxo
try {
    Integer.parseInt(str);
    return true;
} catch (NumberFormatException e) {
    return false;
}
// MELHOR
return str.chars().allMatch(Character::isDigit);  // ou regex
// (exceções são caras — o JIT não otimiza bem around them)
```

### Exceções em lambdas

```java
// RUIM — lambda com checked exception não compila
list.forEach(f -> Files.readString(f));  // IOException não tratada

// Workaround 1 — wrap em unchecked
list.forEach(f -> {
    try { return Files.readString(f); }
    catch (IOException e) { throw new UncheckedIOException(e); }
});

// Workaround 2 — helper
static <T, R> Function<T, R> unchecked(ThrowingFunction<T, R> fn) {
    return t -> {
        try { return fn.apply(t); }
        catch (Exception e) { throw new RuntimeException(e); }
    };
}
list.stream().map(unchecked(Files::readString)).toList();
```

### Em APIs REST

Traduzir exceções de domínio para HTTP status codes via `@RestControllerAdvice`. Detalhes em [[API Design]] (RFC 9457 Problem Details) e [[Spring Boot]].

> **Fontes:**
>
> - [Java Exceptions — Baeldung](https://www.baeldung.com/java-exceptions)
> - [Checked vs Unchecked — Baeldung](https://www.baeldung.com/java-checked-unchecked-exceptions)
> - [Try-with-resources — Baeldung](https://www.baeldung.com/java-try-with-resources)
> - [Sneaky throws — Baeldung](https://www.baeldung.com/java-sneaky-throws)
> - [Chained exceptions — Baeldung](https://www.baeldung.com/java-chained-exceptions)
> - [Exceptions performance — Baeldung](https://www.baeldung.com/java-exceptions-performance)
> - [Pensando nas Exceptions do Java](https://insights.itexto.com.br/pensando-nas-exceptions-do-java-ou-por-que-elas-sao-assim/)

---

## Optional

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

Tipos parametrizados. Segurança de tipos em compile-time.

```java
// Classe genérica
public class Result<T> {
    private final T data;
    private final String error;

    public static <T> Result<T> ok(T data) { return new Result<>(data, null); }
    public static <T> Result<T> fail(String error) { return new Result<>(null, error); }
}

// Bounded types
public <T extends Comparable<T>> T max(T a, T b) {
    return a.compareTo(b) >= 0 ? a : b;
}

// Wildcards
List<? extends Number> numbers;  // leitura (producer) — pode ser List<Integer>, List<Double>
List<? super Integer> sink;      // escrita (consumer) — pode ser List<Integer>, List<Number>
```

**PECS:** Producer Extends, Consumer Super.

**Type erasure:** generics são removidos em runtime. `List<String>` e `List<Integer>` são o mesmo `List` em bytecode.

---

## Concorrência (visão geral)

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

### Java 8 (2014) — A revolução

- **Lambdas e interfaces funcionais** — `(x) -> x * 2`
- **Streams API** — processamento funcional de coleções
- **Optional** — alternativa a null
- **Date/Time API** — `LocalDate`, `Instant`, `Duration`
- **Default methods em interfaces** — evolução sem quebrar
- **Method references** — `String::toUpperCase`

### Java 9-10 (2017-2018)

- **Modules (JPMS)** — modularização da JVM
- **`List.of()`, `Set.of()`, `Map.of()`** — coleções imutáveis
- **`var` (Java 10)** — inferência de tipo local
- **`Optional.ifPresentOrElse()`, `Optional.or()`**
- **`Stream.ofNullable()`, `Stream.takeWhile()`, `Stream.dropWhile()`**

### Java 11-16 (2018-2021)

- **`String.isBlank()`, `.strip()`, `.lines()`, `.repeat()`** (Java 11)
- **`Files.readString()`, `Files.writeString()`** (Java 11)
- **Switch expressions** (Java 14) — `switch` retorna valor
- **Text blocks** (Java 15) — `"""multiline"""`
- **Records** (Java 16) — `record Point(int x, int y) {}`
- **Pattern matching for instanceof** (Java 16) — `if (obj instanceof String s)`
- **`Stream.toList()`** (Java 16) — substitui `collect(Collectors.toList())`

### Java 17 (2021, LTS)

- **Sealed classes** — `sealed class Shape permits Circle, Rectangle`
- **Pattern matching em switch** (preview)
- **Remoção do Applet API e Security Manager**

### Java 21 (2023, LTS)

- **Virtual Threads** — threads leves para I/O-bound
- **Record patterns** — `if (obj instanceof Point(int x, int y))`
- **Pattern matching em switch** (final)
- **Sequenced Collections** — `SequencedCollection`, `SequencedMap` com `getFirst()`, `getLast()`
- **String templates** (preview) — `STR."Hello \{name}"`

### Java 22 (2024)

- **Unnamed variables and patterns** — `_` para variáveis/patterns não usados
- **Statements before super()** — validar argumentos antes de chamar construtor pai
- **Stream Gatherers** (preview) — operações intermediárias customizadas no Stream
- **String templates** (preview revisto) — `STR."Hello \{name}"`
- **Structured Concurrency** (preview) — grupo de tarefas como unidade atômica
- **Scoped Values** (preview) — alternativa thread-safe a ThreadLocal
- **Class-File API** (preview) — ler/escrever bytecode via API Java

### Java 23 (Setembro 2024)

- **Primitive types in patterns** (preview) — `case int i` em switch
- **Module import declarations** (preview) — `import module java.base`
- **Markdown em Javadoc** — blocos de código em Markdown nativamente
- **Implicitly declared classes e main methods** (preview) — scripts Java sem `public class Main { ... }`
- **Flexible Constructor Bodies** — evolução de "statements before super()"

### Java 24 (Março 2025)

- **Stream Gatherers** (final)
- **Scoped Values** (final) — substitui ThreadLocal em Virtual Threads
- **Ahead-of-Time Class Loading & Linking** (preview) — startup mais rápido
- **Compact Object Headers** (experimental) — menos memória por objeto
- **Generational Shenandoah GC** (experimental)

### Java 25 (Setembro 2025, LTS)

- **Structured Concurrency** (final)
- **Primitive Patterns** (final)
- **Module import declarations** (final)
- **Compact Source Files and Instance Main Methods** (final) — Java para scripting
- **PEM Encodings of Cryptographic Objects** — API moderna para keys/certs
- **Stable Values** (preview) — imutabilidade deferred
- Consolida vários previews acumulados desde Java 21

> **Fontes:**
>
> - [Java features desde JDK 8 ao 21](https://advancedweb.hu/a-categorized-list-of-all-java-and-jvm-features-since-jdk-8-to-21/)
> - [Java Language Updates](https://docs.oracle.com/en/java/javase/21/language/index.html)
> - [Java Evolved](https://javaevolved.github.io/)

---

## Armadilhas comuns

- **NullPointerException:** usar `Optional` para retornos, `Objects.requireNonNull()` para validação
- **Mutabilidade acidental:** `List.of()` é imutável, `Collections.unmodifiableList()` é view (original mutável!)
- **ConcurrentModificationException:** modificar coleção durante iteração. Usar `Iterator.remove()` ou Streams.
- **Autoboxing em loops:** `Integer` em vez de `int` em loops grandes = milhões de objetos
- **String concatenação em loop:** usar `StringBuilder`, não `+=`
- **`==` para comparar Strings:** usar `.equals()`. `==` funciona com literais por causa do pool, mas falha com `new String()`
- **Parallel streams sem pensar:** ForkJoinPool compartilhado, poucos elementos = overhead > ganho

## Na prática (da minha experiência)

> Com 20+ anos em Java, a linguagem evoluiu enormemente. No MedEspecialista, uso Java 21 com Records para DTOs (elimina boilerplate), Streams para transformações de dados, e CompletableFuture para chamadas paralelas a serviços externos. A migração para Virtual Threads reduziu a necessidade de tuning de thread pools em endpoints I/O-bound. No dia a dia, Collections e Streams são 80% do que uso — o outro 20% é concorrência e I/O.

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
