---
title: "Certificação Java OCP"
created: 2026-04-10
updated: 2026-04-10
type: concept
status: evergreen
tags:
  - java
  - certificacao
  - entrevista
publish: false
---

# Certificação Java OCP

Guia completo para a certificação **Oracle Certified Professional (OCP) Java SE** — tópicos, formato da prova, armadilhas clássicas, estratégia de estudo e preparação. Para fundamentos da linguagem, ver [[Java Fundamentals]]. Para concorrência, ver [[Java Concurrency]].

## O que é e por que fazer

A **OCP (Oracle Certified Professional) Java SE** é a certificação oficial da Oracle que valida conhecimento profundo da linguagem Java e de suas APIs principais. É reconhecida internacionalmente e frequentemente requisitada em vagas senior na Europa, EUA e Ásia.

**Vantagens de ter OCP:**

- **Credencial internacional** — valioso para aplicar a vagas fora do Brasil
- **Força você a dominar detalhes** da linguagem que você não usa no dia a dia
- **Elimina gaps** — revela áreas que você "acha que sabe" mas não sabe
- **Disciplina de aprendizado** — estrutura para revisar Java profundamente
- **Salary bump** em muitas empresas que dão bônus por certificações

**Desvantagens / críticas:**

- **Conhecimento acadêmico** — muito focado em pegadinhas de bytecode e corner cases raros
- **Não substitui experiência** — saber que `int i = 0b10;` é válido não faz você bom em arquitetura
- **Caro** — USD 245 por prova
- **Validade** — certificação não expira, mas a versão sim (Java 8 certificado hoje é menos valorizado)

**Regra prática:** faça a certificação se (1) você quer estruturar seu estudo, (2) você quer credencial para vagas internacionais, ou (3) seu empregador reembolsa. Não faça apenas por currículo — experiência vale mais.

---

## Versões disponíveis

A Oracle atualiza a certificação a cada nova versão LTS. Em 2026, as opções relevantes são:

| Certificação | Prova | Versão | Status | Quando fazer |
| --- | --- | --- | --- | --- |
| **OCP Java SE 21** | 1Z0-830 | LTS 21 | **Atual** | **Recomendado** |
| OCP Java SE 17 | 1Z0-829 | LTS 17 | Ainda válida | Se estudou para ela |
| OCP Java SE 11 | 1Z0-819 | LTS 11 | Válida, mas antiga | Evite |
| OCP Java SE 8 | 1Z0-809 | LTS 8 | Legada | Não faça mais |

**Recomendação:** vá direto para **OCP Java SE 21** — é a mais atual, valoriza features modernas (Records, Sealed Classes, Pattern Matching, Virtual Threads) e tem mais peso no mercado.

### OCA ainda existe?

**Não.** Antes de 2020, havia OCA (Associate) + OCP (Professional) como duas provas. Desde Java 11, a Oracle consolidou em **uma única prova OCP** (1Z0-819, 1Z0-829, 1Z0-830). Se você vê material falando de "OCA", é antigo.

---

## Formato da prova (OCP Java SE 21 — 1Z0-830)

| Item | Detalhes |
| --- | --- |
| **Nome oficial** | Java SE 21 Developer Professional |
| **Código** | 1Z0-830 |
| **Duração** | 90 minutos |
| **Número de questões** | ~50 questões |
| **Nota de corte** | ~68% (muda a cada release) |
| **Formato** | Multiple choice (single ou multiple answer) |
| **Idioma** | Inglês (oficial) |
| **Preço** | USD 245 |
| **Onde fazer** | Pearson VUE (centro físico) ou Online Proctored (em casa) |
| **Tentativas** | 1 voucher por tentativa. 14 dias de espera entre tentativas falhadas |
| **Validade** | Não expira, mas a versão fica datada |

### Características da prova

- **Multiple choice** — algumas questões pedem 1 resposta, outras pedem 2-3 respostas corretas. Leia o enunciado com atenção ("Select two.").
- **Código Java real** — você vê código e tem que dizer o que imprime, se compila, qual exceção lança
- **Perguntas traiçoeiras** — respostas "corretas" em 95% dos casos mas erradas naquele cenário específico
- **Sem parcial** — em questões multi-answer, você precisa acertar TODAS as respostas corretas, sem extras
- **Marcador para revisão** — você pode marcar questões e voltar depois (use!)
- **Proibido** — calculadora, scratch paper digital, ajuda externa

### Online Proctored vs Centro físico

**Online Proctored** (em casa):
- ✅ Mais barato (só o voucher, sem deslocamento)
- ✅ Sem deslocamento
- ⚠️ Requer webcam, mic, ambiente limpo, sem ninguém por perto
- ⚠️ Proctor observa via webcam, bate papo sobre ambiente no início
- ⚠️ Você **não pode** falar sozinho, olhar para os lados, levantar. Comportamento suspeito = prova invalidada

**Centro físico** (Pearson VUE):
- ✅ Ambiente controlado, sem estresse de proctor online
- ⚠️ Deslocamento
- ⚠️ Disponibilidade de horários depende da sua cidade

**Recomendação:** se você tem um ambiente calmo e webcam boa, online proctored. Se não, centro físico.

---

## Tópicos cobertos na prova (OCP Java SE 21)

A Oracle publica o **objetivos oficiais** em [education.oracle.com](https://education.oracle.com/java-se-21-developer-professional/pexam_1Z0-830). Aqui vai o mapa completo com comentários práticos.

### 1. Handling date, time, text, numeric and boolean values

- **Dados primitivos e wrappers** — autoboxing, unboxing, range de cada tipo
- **Literais numéricos** — `100_000`, `0b1010`, `0xFF`, `42L`, `3.14f`
- **Operadores** — precedência, associatividade, short-circuit (`&&` vs `&`)
- **Strings** — imutabilidade, pool, `equals` vs `==`, `compareTo`, `format`, text blocks
- **StringBuilder** — quando usar
- **Date/Time API** — `LocalDate`, `LocalTime`, `LocalDateTime`, `ZonedDateTime`, `Instant`, `Duration`, `Period`
- **DateTimeFormatter** — ISO vs custom patterns
- **BigDecimal** — evitar float/double para dinheiro, `setScale`, `RoundingMode`

**Armadilha clássica:** `Integer i = 127; Integer j = 127; i == j` → `true` (Integer cache). Mas `i = 128; j = 128; i == j` → **`false`**. Cache vai só de -128 a 127.

### 2. Controlling program flow

- **if/else** — blocos, nesting
- **switch statement e switch expression** (Java 14+)
- **Pattern matching em switch** (Java 21)
- **Loops** — `for`, `enhanced for`, `while`, `do-while`
- **Labels** — `break label;`, `continue label;`
- **Return, break, continue**

**Armadilha:** switch expression sem `default` quando o tipo não é enum ou sealed → erro de compilação. Com sealed types e record patterns, o compilador infere exaustividade.

### 3. Utilizing Java object-oriented approach

- **Classes e objetos** — instanciação, garbage collection, `this`, `super`
- **Construtores** — default, chaining (`this()`, `super()`), ordem de inicialização
- **Inicialização** — instance initializer, static initializer, final fields
- **Métodos** — parâmetros, varargs, return types, covariant returns
- **Encapsulamento** — modificadores de acesso
- **Herança** — `extends`, `@Override`, polimorfismo, dynamic dispatch
- **Casting** — upcast, downcast, `instanceof`, pattern matching
- **Classes abstratas vs interfaces**
- **Default methods em interfaces** — diamond problem, `super.method()`
- **Static e final** — semântica exata
- **Inner classes** — static nested, inner, local, anonymous
- **Enums** — com métodos, constructors, `values()`, `valueOf()`
- **Records** — componentes, compact constructor, métodos, `equals`/`hashCode`/`toString` gerados
- **Sealed classes** — `sealed`, `permits`, `non-sealed`, `final`
- **Pattern matching** — `instanceof`, switch, record patterns

**Armadilhas:**
- Ordem de inicialização: `static` → `instance` → `constructor`
- Sobrescrita de `static` não existe (é **hiding**)
- `final` em parâmetro de método não afeta o caller
- Enum com construtor é chamado uma vez por constante, na primeira vez que a enum é usada
- Record component é **final** — você não pode reassignar no corpo do método

### 4. Handling exceptions

- **Hierarquia** — Throwable, Error, Exception, RuntimeException
- **Checked vs unchecked**
- **try/catch/finally** — execution order, multi-catch (`|`), exception chaining
- **try-with-resources** — AutoCloseable, suppressed exceptions, ordem de close
- **throws** — propagação, overriding (não pode adicionar checked)
- **Custom exceptions**
- **Assertions** (raro, mas cai)

**Armadilhas clássicas:**
- `try-with-resources` fecha recursos na **ordem reversa** da declaração
- `return` dentro de `try` e `finally` com `return` — o do `finally` sobrescreve!
- Multi-catch com exceções relacionadas — erro de compilação (`catch (IOException | FileNotFoundException e)` não compila, FileNotFoundException é subclasse)
- Sobrescrita de método não pode **adicionar** checked exception, mas pode remover ou usar subclass

```java
// Pegadinha clássica
public int foo() {
    try {
        return 1;
    } finally {
        return 2;  // retorna 2, não 1
    }
}
```

### 5. Working with arrays and collections

- **Arrays** — declaração, inicialização, multi-dim, `Arrays.toString`, `Arrays.sort`, `Arrays.binarySearch`
- **List, Set, Map, Queue** — implementações e características
- **ArrayList vs LinkedList** — trade-offs
- **HashMap, TreeMap, LinkedHashMap** — ordenação e performance
- **HashSet, TreeSet, LinkedHashSet**
- **Deque, Stack, Queue** — operations (`push`, `pop`, `peek`, `offer`, `poll`)
- **Iterator e Iterable** — `fail-fast` vs `fail-safe`
- **Comparable e Comparator** — `compareTo`, `Comparator.comparing`, `thenComparing`, `reversed`
- **Collections.sort**, imutáveis (`List.of`, `Collections.unmodifiableList` — **view vs cópia**)
- **ConcurrentModificationException** — modificar coleção durante iteration

**Armadilha:** `Arrays.asList(array)` retorna lista de tamanho fixo, não uma `ArrayList`. `.add()` lança `UnsupportedOperationException`.

### 6. Working with Streams and Lambda expressions

- **Lambda syntax** — parâmetros, corpo, variáveis capturadas (effectively final)
- **Method references** — `Class::method`, `instance::method`, `Class::new`
- **Interfaces funcionais** — `Function`, `Predicate`, `Consumer`, `Supplier`, `BiFunction`, `UnaryOperator`, primitive versions (`IntFunction`, etc.)
- **Stream creation** — `stream()`, `Stream.of`, `Stream.generate`, `Stream.iterate`, `IntStream.range`
- **Intermediate operations** — `filter`, `map`, `flatMap`, `distinct`, `sorted`, `peek`, `limit`, `skip`, `takeWhile`, `dropWhile`
- **Terminal operations** — `forEach`, `toList`, `collect`, `reduce`, `count`, `min`, `max`, `findFirst`, `findAny`, `anyMatch`, `allMatch`, `noneMatch`
- **Collectors** — `toList`, `toSet`, `toMap`, `joining`, `groupingBy`, `partitioningBy`, `counting`, `summingInt`, `averagingDouble`, `mapping`, `reducing`
- **Optional** — `of`, `empty`, `ofNullable`, `isPresent`, `ifPresent`, `orElse`, `orElseGet`, `orElseThrow`, `map`, `flatMap`, `filter`
- **Parallel streams** — quando usar, pitfalls
- **Stream Gatherers** (Java 22+) — preview mas pode cair

**Armadilhas:**
- Stream é **one-shot** — chamar terminal operation 2x dá erro
- `peek` pode não executar se operações subsequentes não precisarem (lazy)
- `Optional.orElse(expensiveCall())` **sempre** executa. Use `orElseGet(() -> ...)` para lazy
- `Optional` como parâmetro de método é anti-pattern (não cai na prova diretamente, mas ajuda entender)
- `Collectors.toMap` lança se tiver chaves duplicadas — passe mergeFunction ou use `groupingBy`

### 7. Implementing localization

Menos peso na prova, mas cai:

- **Locale** — criação, `Locale.getDefault`, localização de mensagens
- **ResourceBundle** — properties files, fallback
- **NumberFormat** — currency, percent, locale-specific
- **DateTimeFormatter** — FormatStyle.SHORT/MEDIUM/LONG/FULL

### 8. Managing concurrent code execution

- **Thread creation** — extends Thread vs implements Runnable, Thread.start vs run
- **Thread states** — NEW, RUNNABLE, BLOCKED, WAITING, TIMED_WAITING, TERMINATED
- **Thread lifecycle methods** — sleep, join, interrupt
- **synchronized** — methods, blocks, monitor
- **volatile** — visibility
- **wait/notify/notifyAll** — monitor contract
- **ExecutorService** — newFixedThreadPool, newSingleThreadExecutor, newCachedThreadPool, newScheduledThreadPool, **newVirtualThreadPerTaskExecutor** (Java 21)
- **Callable, Future** — submit, get, cancel
- **CompletableFuture** — supplyAsync, thenApply, thenCompose, thenCombine, allOf, anyOf, exceptionally
- **java.util.concurrent.atomic** — AtomicInteger, AtomicReference, compareAndSet
- **Concurrent collections** — ConcurrentHashMap, CopyOnWriteArrayList
- **Virtual Threads** — criação, diferença para platform threads
- **Locks** — ReentrantLock, ReadWriteLock (básico)

→ Deep dive em [[Java Concurrency]]

**Armadilha:** `Thread t = new Thread(...); t.run();` **não cria thread nova** — executa no caller. Você tem que chamar `t.start()`.

### 9. Using Java I/O API

- **java.io** — InputStream/OutputStream (bytes), Reader/Writer (chars)
- **BufferedReader, BufferedWriter** — wrap para performance
- **FileInputStream, FileOutputStream, FileReader, FileWriter**
- **try-with-resources** — fecha automaticamente
- **java.nio.file** — Path, Paths, Files, Files.lines, Files.walk
- **Serialization** — Serializable, transient, serialVersionUID, `ObjectInputStream`/`ObjectOutputStream`
- **Console I/O** — Console class

**Cuidado:** serialization é coberto superficialmente; geralmente 1-2 questões.

### 10. Accessing databases using JDBC

JDBC básico está no escopo:

- **Connection, Statement, PreparedStatement, CallableStatement**
- **ResultSet** — navigating, getters
- **Transações** — commit, rollback, setAutoCommit, savepoints
- **try-with-resources** com Connection
- **SQLException**
- **DriverManager.getConnection**

**Armadilha:** ordem de fechamento importa. Close ResultSet → Statement → Connection, mas try-with-resources faz automaticamente.

### 11. Implementing modular applications (JPMS)

Módulos Java — Java Platform Module System (JPMS), introduzido no Java 9:

- **module-info.java** — `requires`, `exports`, `opens`, `uses`, `provides`
- **Tipos de módulos** — named, unnamed, automatic
- **Service Loader** — `ServiceLoader.load()`
- **jlink** — criar runtime customizado
- **Migração** — de classpath para modulepath

**Na prática:** JPMS é pouco usado em produção real (Spring, Jakarta EE não usam agressivamente), mas **cai bastante** na prova. Estude mesmo que não use.

### 12. Packaging and deploying

- **jar** — command line, META-INF/MANIFEST.MF
- **jlink** — runtime customizado
- **jpackage** — native installer (Java 14+)
- **javac, java** — compilação e execução, classpath, modulepath
- **JShell** (Java 9+)
- **Implicit classes e instance main methods** (preview/final em Java 21+) — scripts Java

---

## Novidades específicas do Java 21 (peso alto na prova OCP 21)

### Records e Record Patterns

Record com compact constructor, métodos, interfaces. Record patterns em switch e if.

```java
record Point(int x, int y) {}
record Line(Point start, Point end) {}

// Desestruturação aninhada
if (shape instanceof Line(Point(var x1, var y1), Point(var x2, var y2))) {
    // ...
}
```

### Sealed classes

```java
sealed interface Shape permits Circle, Square, Triangle {}
// ...

double area(Shape s) {
    return switch (s) {
        case Circle c -> Math.PI * c.radius() * c.radius();
        case Square sq -> sq.side() * sq.side();
        case Triangle t -> 0.5 * t.base() * t.height();
        // Sem default — compilador garante exaustividade
    };
}
```

### Pattern matching em switch

```java
String describe(Object o) {
    return switch (o) {
        case null          -> "null";
        case Integer i when i < 0 -> "negative int";
        case Integer i     -> "int: " + i;
        case String s      -> "string: " + s;
        case int[] arr     -> "int array length " + arr.length;
        default            -> "unknown";
    };
}
```

### Virtual Threads

```java
// Criar virtual thread
Thread.ofVirtual().start(() -> doWork());

// ExecutorService de virtual threads
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    executor.submit(() -> doWork());
}
```

### Sequenced Collections

Interface `SequencedCollection`, `SequencedSet`, `SequencedMap` com `getFirst()`, `getLast()`, `addFirst`, `addLast`, `reversed()`.

```java
List<String> list = List.of("a", "b", "c");
list.getFirst();  // "a"
list.getLast();   // "c"
list.reversed();  // view invertida
```

### Text blocks (já em versões anteriores, mas cai)

```java
String json = """
    {
      "name": "Maria",
      "age": 30
    }
    """;
```

### Switch expressions

```java
int daysInMonth = switch (month) {
    case JAN, MAR, MAY, JUL, AUG, OCT, DEC -> 31;
    case APR, JUN, SEP, NOV                -> 30;
    case FEB                                -> isLeapYear ? 29 : 28;
};
```

**Cuidado:** `yield` em bloco.

```java
int result = switch (x) {
    case 1 -> 10;
    case 2 -> {
        int temp = calculate();
        yield temp * 2;  // yield, não return
    }
    default -> 0;
};
```

---

## Armadilhas clássicas da prova OCP

Esta seção vale ouro — são pegadinhas recorrentes que a prova adora.

### Integer cache

```java
Integer a = 127;
Integer b = 127;
System.out.println(a == b);  // true (cache -128..127)

Integer c = 128;
Integer d = 128;
System.out.println(c == d);  // false (fora do cache)

// SEMPRE compare com equals
System.out.println(c.equals(d));  // true
```

### String pool vs new String

```java
String s1 = "hello";
String s2 = "hello";
String s3 = new String("hello");

System.out.println(s1 == s2);        // true (ambos do pool)
System.out.println(s1 == s3);        // false (s3 é novo objeto)
System.out.println(s1.equals(s3));   // true
System.out.println(s1 == s3.intern()); // true
```

### `var` com tipos ambíguos

```java
var list = new ArrayList<>();  // ArrayList<Object>
list.add("hello");
list.add(42);
// list é List<Object>, não List<String>

// var NÃO pode:
// var x;                    // sem inicializador
// var y = null;             // null sem tipo
// var z = () -> 1;          // lambda sem target type
// var arr[] = new int[10];  // array declaration
// var method() { }          // return type
```

### Autoboxing com null

```java
Integer i = null;
int j = i;  // NullPointerException!
```

### Final com objeto mutável

```java
final List<String> list = new ArrayList<>();
list.add("hello");  // OK — só a referência é final
// list = new ArrayList<>();  // ERRO — reassign não permitido
```

### Override vs Overload com autoboxing

```java
class A {
    void foo(int x) { System.out.println("int"); }
    void foo(Integer x) { System.out.println("Integer"); }
    void foo(Object x) { System.out.println("Object"); }
}

new A().foo(1);      // "int" (exact match ganha)
new A().foo((Integer) 1);  // "Integer"
new A().foo("str");  // "Object"
```

**Regras de resolução (em ordem):** exact match → widening → autoboxing → varargs

### Static method hiding (não é override)

```java
class Parent {
    static void foo() { System.out.println("Parent"); }
}

class Child extends Parent {
    static void foo() { System.out.println("Child"); }
}

Parent p = new Child();
p.foo();  // "Parent" — static é resolvido em compile-time pelo TIPO declarado
```

### Try-finally com return

```java
int method() {
    try {
        return 1;
    } finally {
        return 2;  // sobrescreve o return do try
    }
}
// retorna 2
```

### Try-with-resources order

```java
try (A a = new A();
     B b = new B();
     C c = new C()) {
    // use
}
// Ordem de close: c → b → a (reversa da declaração)
```

### Equals e hashCode contrato

```java
// Se você sobrescreve equals, DEVE sobrescrever hashCode
// Senão, HashMap/HashSet quebram:

class Person {
    String name;
    public boolean equals(Object o) { /* compara name */ }
    // FALTA hashCode — BUG
}

Set<Person> set = new HashSet<>();
set.add(new Person("Maria"));
set.contains(new Person("Maria"));  // false! hashCode default é baseado em identidade
```

### Collections imutáveis: view vs cópia

```java
List<String> list = new ArrayList<>(List.of("a", "b"));
List<String> unmod = Collections.unmodifiableList(list);
List<String> copy = List.copyOf(list);  // cópia

list.add("c");

System.out.println(unmod.size());  // 3 — view! reflete mudanças na original
System.out.println(copy.size());   // 2 — cópia
```

### Switch fall-through

```java
int x = 2;
switch (x) {
    case 1:
        System.out.println("1");
    case 2:
        System.out.println("2");
    case 3:
        System.out.println("3");
    default:
        System.out.println("default");
}
// Imprime: 2, 3, default (fall-through sem break)
```

Switch expression (arrow) **não** tem fall-through:

```java
switch (x) {
    case 1 -> System.out.println("1");
    case 2 -> System.out.println("2");
    case 3 -> System.out.println("3");
    default -> System.out.println("default");
}
// Imprime apenas: 2
```

### Stream consumido 2x

```java
Stream<String> stream = Stream.of("a", "b", "c");
stream.forEach(System.out::println);  // ok
stream.forEach(System.out::println);  // IllegalStateException
```

### Effectively final em lambdas

```java
int x = 10;
Runnable r = () -> System.out.println(x);  // OK, x é effectively final
// x = 20;  // ERRO — se reassignar, não é mais effectively final
```

### Inicialização de arrays

```java
int[] a = new int[5];          // todos 0
Integer[] b = new Integer[5];  // todos null
boolean[] c = new boolean[5];  // todos false
String[] d = new String[5];    // todos null
```

### Enum constructor

```java
enum Status {
    ACTIVE("active"),
    INACTIVE("inactive");

    private final String label;

    Status(String label) {  // sempre private (implícito)
        this.label = label;
    }
}
```

Enum constructor **não pode** ser `public` ou `protected`. Sempre implicitamente `private`.

### Generics e type erasure

```java
List<String> stringList = new ArrayList<>();
List<Integer> intList = new ArrayList<>();

System.out.println(stringList.getClass() == intList.getClass());  // true!
// Em runtime, ambos são apenas List — type erasure
```

---

## Estratégia de estudo

### Plano de estudo (3-4 meses)

**Mês 1 — Fundamentos:**
- Revisar todos os tópicos de [[Java Fundamentals]]
- Ler capítulos do livro (Scott Selikoff + Jeanne Boyarsky) de 1 a 8
- Fazer exercícios de cada capítulo
- Escrever código experimental no JShell

**Mês 2 — Tópicos avançados:**
- Concorrência ([[Java Concurrency]])
- Streams + Collectors (deep)
- NIO.2 (Files, Paths)
- JDBC básico
- Módulos (JPMS) — mesmo que não use
- Localization

**Mês 3 — Features modernas e prática:**
- Records, Sealed Classes, Pattern Matching
- Virtual Threads
- Text blocks, switch expressions
- **Mock exams** — Enthuware ou MyExamCloud
- Revisar erros, estudar tópicos fracos

**Mês 4 — Reta final:**
- Mock exams adicionais (meta: >80% de acerto consistente)
- Revisar armadilhas clássicas
- Flashcards de APIs decoradas (Collectors, Optional, Stream methods)
- Simular condições da prova (90min, sem consulta)
- **Marcar a prova** quando atingir >80% em 3 mocks consecutivos

### Recursos essenciais

**Livro (essencial):**
- **OCP Oracle Certified Professional Java SE 21 Developer Study Guide** — Scott Selikoff & Jeanne Boyarsky (Sybex). **É o livro.** Cobre todos os tópicos, tem exercícios e mock exams.

**Mock exams (essenciais):**
- **Enthuware** — USD 10-15. Mock exams com qualidade similar à prova real. **Melhor custo-benefício do mercado.**
- **MyExamCloud** — alternativa, também bom
- **Whizlabs** — OK, mas qualidade de questões inferior a Enthuware

**Cursos (opcionais):**
- **Udemy — Master Java OCP Certification** (vários instrutores)
- **Pluralsight** — cursos por tópico

**Videos em português:**
- [Certificação Java OCP 17 — José Programador](https://www.youtube.com/playlist?list=PLUP6iVXwQmPFFI0U6PveU46ORw0QsZ4VC) — gratuito, excelente
- Maratona Java Virado no Jiraya — fundamentos

**Prática (essencial):**
- **JShell** — teste expressões e ideias rapidamente
- **Mini projetos** — NIO.2, Concurrency, Streams — escrever código experimental, quebrar e consertar
- **Leitura de bytecode** — `javap -c Classe.class` para ver o que o compilador gerou em casos ambíguos

### Como usar mock exams corretamente

1. **Primeiro mock** — teste diagnóstico. Não se preocupe com nota. Descubra fraquezas.
2. **Revise TODAS as questões** — certas e erradas. Entenda POR QUE a resposta é aquela.
3. **Mantenha um caderno de erros** — anote toda armadilha nova que aprender.
4. **Repita tópicos fracos** com questões focadas
5. **Mocks completos semanais** — simule condições reais (90 min, sem interrupção)
6. **Não cole, não repita mock sem intervalo** — você decora respostas, não aprende

**Regra de ouro:** não marque a prova real antes de fazer **3+ mock exams consecutivos acima de 80%**.

---

## Tips para o dia da prova

**Antes:**
- Durma bem (8h mínimo — cansaço mata raciocínio)
- Evite estudar no dia (revisão leve apenas, flash cards)
- Chegue 30 min antes (presencial) ou teste setup 1h antes (online)
- Documento com foto obrigatório (passaporte ou RG para brasileiros fora do Brasil)
- Banheiro antes

**Durante:**
- **Leia o enunciado 2x** — questões trapaceiras escondem detalhes
- **Não passe muito tempo em uma questão** — marque para revisão e siga adiante
- **Elimine respostas obviamente erradas** primeiro
- **Cuidado com "Select two" / "Select three"** — fácil esquecer
- **Code review mental** — leia cada linha do código antes de responder
- **Trust but verify** — respostas óbvias podem estar certas, mas verifique
- **Revise marcadas no final** — se sobrar tempo
- **Não deixe em branco** — não há penalidade por erro (verifique regra atual)

**Gerenciamento de tempo:**
- 90 minutos / 50 questões = ~1.8 min por questão
- Passe rápido nas fáceis (< 1 min) para ganhar tempo nas difíceis
- **Nunca gaste mais de 3 min** em uma questão na primeira passada
- **Pelo menos 10 min** de revisão no final

**Mentalidade:**
- Esteja pronto para questões que parecem impossíveis — elas são desenhadas para confundir
- Confie no seu preparo se estudou
- Ansiedade é normal — respire fundo, leia o enunciado devagar

---

## Depois da prova

### Se passou

- Parabéns! 🎉
- Baixe o certificado digital na Oracle (CertView)
- Adicione ao LinkedIn (`Licenses & certifications`)
- Adicione ao currículo
- Guarde a **digital badge** (Credly) para compartilhar

### Se não passou

- **Não é o fim do mundo.** A Oracle dá um relatório com as áreas fracas
- Esperar **14 dias** mínimo antes de tentar de novo
- Revisar áreas onde errou
- Fazer mais mocks
- **Segunda tentativa geralmente passa** se primeira foi perto (> 60%)

---

## Na prática (da minha experiência)

> **Planejamento e motivação:**
> Certificações são investimento de tempo significativo. Fazê-la só faz sentido se houver objetivo claro — vaga internacional, mudança de emprego, ou marco pessoal. O valor real não é o papel em si, mas a **disciplina de estudo estruturado** que força você a fechar gaps.
>
> **O que mais me ajudou:**
>
> **1. Livro Sybex (Selikoff & Boyarsky) como base.** Cobre absolutamente tudo, com ordem didática bem pensada. Ler sequencialmente, fazer os exercícios no final de cada capítulo, **não pular**.
>
> **2. Enthuware mock exams.** Qualidade de questão próxima à prova real. Fiz ~15 mocks, revisei cada erro. Meu caderno de erros virou 30 páginas de armadilhas aprendidas.
>
> **3. JShell para experimentação.** Questões sobre output de código exigem saber exatamente o que a JVM faz. JShell permitia testar hipóteses em 10 segundos. "Se `Integer i = 128; Integer j = 128; i == j` dá `false`, e se `Integer i = 127; Integer j = 127`? Vamos testar."
>
> **4. Revisão ativa dos erros.** Para cada mock, passei ~2 horas revisando as 10-15 questões erradas. Escrevia explicação da resposta correta no meu caderno de erros. Depois de algumas semanas, comecei a reconhecer padrões.
>
> **5. Foco nas armadilhas clássicas.** A prova adora: Integer cache, String pool, static vs instance, try/finally com return, autoboxing e NPE, generics type erasure, ordem de inicialização. **Decore essas.**
>
> **6. Tópicos "maçantes" merecem atenção.** JPMS (módulos), NIO.2, Localization — você não usa no dia a dia, mas a prova cobra. Invista tempo neles, mesmo achando sem graça.
>
> **O que menos valeu:**
>
> - **Cursos em vídeo longos** — lentos, repetitivos. Livro + mocks é mais eficiente.
> - **Decorar APIs inteiras** — você não precisa saber cada método de Stream. Saber os patterns comuns basta.
> - **Estudar tópicos que sei de cor do dia a dia.** Foquei em tópicos fracos, não em reforçar pontos fortes.
>
> **Sobre a prova em si:**
>
> Primeira passada, tempo não foi problema (terminei em ~60 min). Mas algumas questões eram **armadilhas realmente traiçoeiras** — precisa ler 3-4 vezes para entender a pegadinha. Marquei ~8 questões para revisão, resolvi 5 delas no final.
>
> **Lição principal:** certificação Java é um exercício de **atenção aos detalhes** e **disciplina de estudo**. Dominar a linguagem profundamente é o subproduto mais valioso. Mesmo que você nunca precise do certificado, o processo de estudo faz você um Java dev melhor. Mas não confunda ter OCP com ser um bom engenheiro — são eixos diferentes.

---

## How to explain in English

> "I pursued the OCP Java SE 21 certification as part of my preparation for international senior roles. It's the Oracle Certified Professional exam that validates deep knowledge of the Java language and its standard APIs. The certification matters in Europe and Asian markets, where it's explicitly listed in many job requirements.
>
> My study strategy was disciplined: three months with the Sybex book by Selikoff and Boyarsky, reading sequentially and doing every exercise. Then I moved to Enthuware mock exams — they closely match the real exam difficulty and format. I kept an error log, writing down every gotcha I learned: things like the Integer cache behavior, the distinction between String pool and `new String`, the try-finally return semantics, and static method hiding that's not polymorphism.
>
> The exam itself is tricky. It's 50 questions in 90 minutes, multiple choice with single and multi-answer questions. Many questions show code and ask what it prints — the traps are usually subtle details like autoboxing with null, type erasure, or the exact order of initialization. You need to read each question at least twice to spot the catch.
>
> What surprised me is how much the certification covers areas I rarely use in production — Java Platform Module System (JPMS), localization, serialization. You have to study them even if they're not in your day-to-day work, because the exam will test them.
>
> The real value wasn't the certificate itself, it was the forcing function. Studying for OCP made me review parts of Java I'd taken for granted after years of use. I found gaps in my understanding of concurrent collections, Optional semantics, and pattern matching. That knowledge makes me a better engineer even in contexts where I never mention the certification."

### Frases úteis em entrevista

- "I have the OCP Java SE 21 certification, which validates deep knowledge of Java language internals and APIs."
- "Studying for OCP reinforced my understanding of concurrent collections, pattern matching, and functional interfaces."
- "The certification covers classical traps — Integer cache, String pool, type erasure — that I regularly watch for in code reviews."
- "I used the Sybex book and Enthuware mock exams for preparation."
- "What the certification doesn't test is architecture, testing strategy, or production experience — those come from practice."

### Key vocabulary

- certificação → certification
- exame → exam / test
- questão de múltipla escolha → multiple choice question
- nota de corte → passing score
- mock exam → mock exam / practice test
- armadilha → gotcha / trap / pitfall
- tópico → topic
- objetivos oficiais → official objectives
- retomar → retake
- comprovante → proof / certificate

---

## Recursos

### Site oficial Oracle

- [Oracle Java Certification](https://education.oracle.com/java-certification)
- [Java SE 21 Developer Professional (1Z0-830)](https://education.oracle.com/java-se-21-developer-professional/pexam_1Z0-830)
- [CertView — seus certificados](https://certview.oracle.com)
- [Oracle Certification LinkedIn Program](https://www.credly.com/organizations/oracle-corporation/badges)

### Livros

- **OCP Oracle Certified Professional Java SE 21 Developer Study Guide** — Scott Selikoff & Jeanne Boyarsky (Sybex) — **o livro**
- **OCP Oracle Certified Professional Java SE 17 Developer Complete Study Guide** — Selikoff & Boyarsky — se for fazer OCP 17
- **Effective Java** — Joshua Bloch — não é para certificação, mas aprofunda conceitos cobertos

### Mock exams

- **[Enthuware](https://enthuware.com/)** — USD 10-15, melhor custo-benefício
- **[MyExamCloud](https://www.myexamcloud.com/)** — alternativa
- **[Whizlabs](https://www.whizlabs.com/)** — mais questões, qualidade variável

### Cursos online

- [Udemy — Master Java OCP 21](https://www.udemy.com/courses/search/?q=OCP+java+21)
- [Pluralsight Java paths](https://www.pluralsight.com/paths/java)

### Vídeos em português

> [!info] Certificação Java OCP 17 — José Programador
> [https://www.youtube.com/playlist?list=PLUP6iVXwQmPFFI0U6PveU46ORw0QsZ4VC](https://www.youtube.com/playlist?list=PLUP6iVXwQmPFFI0U6PveU46ORw0QsZ4VC)

> [!info] Maratona Java Virado no Jiraya
> [https://www.youtube.com/playlist?list=PL62G310vn6nFIsOCC0H-C2infYgwm8SWW](https://www.youtube.com/playlist?list=PL62G310vn6nFIsOCC0H-C2infYgwm8SWW)

### Comunidades

- [CodeRanch — Java certification forum](https://coderanch.com/f/24/java-certification)
- [Reddit r/javaCertification](https://www.reddit.com/r/javacertification/)
- [Oracle Certification Community](https://community.oracle.com/certification)
- [Discord Brasil Java Community](https://discord.com/invite/oDS8Wt3) (verificar canal ativo)

### Ferramentas de prática

- [JShell](https://docs.oracle.com/en/java/javase/21/jshell/) — REPL oficial
- [javap](https://docs.oracle.com/en/java/javase/21/docs/specs/man/javap.html) — disassembler
- [Compiler Explorer](https://godbolt.org/) — veja como JVM compila (Java + bytecode)

---

## Veja também

- [[Java Fundamentals]] — base da linguagem coberta na prova
- [[Java Concurrency]] — tópico de alto peso na prova
- [[Testes em Java]] — não é coberto na prova, mas complementa
- [[Spring Boot]] — não é coberto, mas é o próximo passo lógico
- [[Senda Java]] — plano de aprendizado geral
- [[What should you do to stand out as a Java-Spring Boot Developer]]
