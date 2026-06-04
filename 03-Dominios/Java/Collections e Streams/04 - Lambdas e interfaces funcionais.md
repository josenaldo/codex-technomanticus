---
title: "Lambdas e interfaces funcionais"
created: 2026-06-04
updated: 2026-06-04
type: concept
progress: backlog
status: seedling
publish: true
fase: iniciado
tags:
  - java
  - collections
  - iniciado
  - funcional
  - lambda
aliases:
  - Lambda
  - Interface funcional
  - Function Predicate Consumer Supplier
---

# Lambdas e interfaces funcionais

> [!abstract] TL;DR
> Um **lambda** é a implementação anônima e concisa de uma **interface funcional** — qualquer interface com exatamente um método abstrato (SAM, *Single Abstract Method*). Em vez de uma classe anônima verbosa, você escreve `(params) -> corpo`. O pacote `java.util.function` fornece as quatro interfaces centrais prontas para uso: `Function<T,R>` (transforma), `Predicate<T>` (testa), `Consumer<T>` (age sem retornar), `Supplier<T>` (fornece sem receber). **Method references** (`Classe::método`) são atalhos de lambda para métodos já existentes. Lambdas e interfaces funcionais são a base de Streams, Optional e toda a API funcional do Java 8+.

## O que é

Um **lambda** é uma função anônima que implementa, de forma concisa, a única operação abstrata de uma **interface funcional**.

**Interface funcional** (*functional interface*) é qualquer interface que possua exatamente **um método abstrato** — esse método único é chamado de **SAM** (*Single Abstract Method*). `default` methods e `static` methods não contam para o requisito SAM: uma interface pode ter vários deles e ainda ser funcional, desde que só um seja abstrato.

A anotação `@FunctionalInterface` instrui o compilador a verificar essa restrição em tempo de compilação. Se a interface tiver zero ou dois ou mais métodos abstratos, o compilador recusa com erro imediato.

```java
@FunctionalInterface
interface Transformador<T, R> {
    R transformar(T entrada);           // único método abstrato → SAM

    default Transformador<T, T> identidade() {  // não conta para SAM
        return t -> (T) t;
    }
}
```

> Para a mecânica completa de interfaces — `default` methods, `static` methods, herança múltipla de tipo e o problema do diamante — veja [[03-Dominios/Java/Linguagem e sintaxe moderna/08 - Interfaces e classes abstratas|Interfaces e classes abstratas]]. Esta nota foca no uso de interfaces funcionais com lambdas.

## Por que importa

Lambdas e interfaces funcionais são o alicerce de toda a API funcional do Java moderno:

- **Streams** — cada operação (`filter`, `map`, `forEach`, `reduce`) aceita uma interface funcional: `Predicate`, `Function`, `Consumer`, `BinaryOperator`.
- **Optional** — `map`, `flatMap`, `filter`, `ifPresent` recebem lambdas.
- **Callbacks e eventos** — qualquer `Runnable`, `Callable`, `Comparator` pode ser escrito como lambda.
- **Entrevistas técnicas** — é muito comum que entrevistadores peçam para explicar as quatro interfaces centrais do `java.util.function`, a diferença entre elas, e como `@FunctionalInterface` funciona.

Sem entender lambdas e interfaces funcionais, o código com Streams vira uma caixa preta. Com esse entendimento, cada passo do pipeline fica legível e controlado.

## Como funciona

### Sintaxe lambda (vs classe anônima)

Um lambda substitui a cerimônia de uma classe anônima quando a interface tem um único método abstrato. As formas sintáticas são:

```java
// Parâmetro único sem tipo → parênteses opcionais
Predicate<String> naoVazio = s -> !s.isBlank();

// Múltiplos parâmetros → parênteses obrigatórios; tipos inferidos
Comparator<String> porTamanho = (a, b) -> a.length() - b.length();

// Corpo com múltiplas linhas → bloco com return explícito
Function<String, String> normalizar = s -> {
    String trimmed = s.strip();
    return trimmed.toLowerCase();
};
```

Equivalente em classe anônima (mais verboso, mesmo efeito):

```java
// Sem lambda
Comparator<String> porTamanho = new Comparator<String>() {
    @Override
    public int compare(String a, String b) {
        return a.length() - b.length();
    }
};

// Com lambda — idêntico em runtime, muito mais conciso
Comparator<String> porTamanho = (a, b) -> a.length() - b.length();
```

Regras do compilador:
- **Tipos dos parâmetros**: sempre podem ser omitidos (inferência de tipo). Quando explicitados, todos devem ser explicitados juntos.
- **Parênteses**: obrigatórios com zero ou dois+ parâmetros; opcionais com exatamente um.
- **`return`**: implícito quando o corpo é uma expressão simples; obrigatório dentro de bloco `{ }`.
- **Escopo**: o lambda não cria novo escopo de variável — não pode declarar parâmetro com o mesmo nome de variável local do método envolvente.

### `@FunctionalInterface` e o conceito SAM

`@FunctionalInterface` é uma anotação de verificação, não de comportamento. Qualquer interface com um único método abstrato já é funcional — a anotação apenas aciona um erro de compilação preventivo caso alguém adicione um segundo método abstrato acidentalmente.

```java
@FunctionalInterface
interface Filtro<T> {
    boolean aceita(T valor);    // único método abstrato

    // Adicionar outro método abstrato aqui causaria erro de compilação:
    // "Unexpected @FunctionalInterface annotation"
}
```

Interfaces do JDK como `Runnable`, `Callable<V>` e `Comparator<T>` são funcionais e por isso também aceitam lambdas — `Runnable` tem exatamente um método abstrato (`run()`), `Comparator` tem `compare()`.

Métodos abstratos herdados de `java.lang.Object` (`equals`, `hashCode`, `toString`) **não contam** para o requisito SAM — o compilador os ignora nessa contagem.

### As quatro centrais: `Function<T,R>` / `Predicate<T>` / `Consumer<T>` / `Supplier<T>`

O pacote `java.util.function` define **quatro formas funcionais básicas**. Tudo mais no pacote é variante ou especialização dessas quatro.

| Interface | Método abstrato | Propósito |
|---|---|---|
| `Function<T, R>` | `R apply(T t)` | Transforma T em R (mapeamento) |
| `Predicate<T>` | `boolean test(T t)` | Testa condição booleana sobre T |
| `Consumer<T>` | `void accept(T t)` | Executa ação sobre T, sem retorno |
| `Supplier<T>` | `T get()` | Fornece T sem receber nenhum argumento |

Exemplos diretos:

```java
// Function<T,R> — transforma String em Integer
Function<String, Integer> comprimento = s -> s.length();
Integer n = comprimento.apply("Java");   // 4

// Predicate<T> — testa se string não está em branco
Predicate<String> naoVazio = s -> !s.isBlank();
boolean ok = naoVazio.test("ola");       // true

// Consumer<T> — imprime sem retornar nada
Consumer<String> imprimir = s -> System.out.println(s);
imprimir.accept("hello");               // imprime "hello"

// Supplier<T> — fornece valor sem receber argumento
Supplier<String> saudacao = () -> "Olá, mundo!";
String msg = saudacao.get();            // "Olá, mundo!"
```

Cada uma tem métodos de **composição** declarados como `default`:
- `Function`: `andThen(after)` (encadeia), `compose(before)` (pré-processa).
- `Predicate`: `and(other)`, `or(other)`, `negate()`.
- `Consumer`: `andThen(after)` (executa os dois em sequência).

```java
// Composição de Function
Function<String, String> trim  = String::strip;
Function<String, String> lower = String::toLowerCase;
Function<String, String> normalizar = trim.andThen(lower);
// normalizar.apply("  JAVA  ") → "java"

// Composição de Predicate
Predicate<String> naoVazio  = s -> !s.isBlank();
Predicate<String> curto     = s -> s.length() < 20;
Predicate<String> valido    = naoVazio.and(curto);
// valido.test("Java") → true
```

### Variantes (`BiFunction`, `UnaryOperator`, `BiPredicate`) e especializações primitivas

**Variantes por aridade e tipo:**

| Interface | Método abstrato | Notas |
|---|---|---|
| `BiFunction<T,U,R>` | `R apply(T t, U u)` | Transforma dois argumentos em R |
| `UnaryOperator<T>` | `T apply(T t)` | `Function<T,T>` — entrada e saída do mesmo tipo |
| `BinaryOperator<T>` | `T apply(T t1, T t2)` | `BiFunction<T,T,T>` — redução do mesmo tipo |
| `BiConsumer<T,U>` | `void accept(T t, U u)` | Ação sobre dois argumentos |
| `BiPredicate<T,U>` | `boolean test(T t, U u)` | Teste com dois argumentos |

```java
// UnaryOperator — transforma String em String
UnaryOperator<String> maiusculo = String::toUpperCase;
// maiusculo.apply("java") → "JAVA"

// BinaryOperator — soma dois inteiros (boxed)
BinaryOperator<Integer> soma = (a, b) -> a + b;
// soma.apply(3, 7) → 10

// BiFunction — combina nome e sobrenome
BiFunction<String, String, String> nomeCompleto =
    (nome, sobrenome) -> nome + " " + sobrenome;
```

**Especializações primitivas** — evitam boxing/unboxing quando o tipo é `int`, `long` ou `double`:

| Grupo | Exemplos | Benefício |
|---|---|---|
| Entrada primitiva | `IntFunction<R>`, `LongFunction<R>`, `DoubleFunction<R>` | Recebe primitivo, retorna objeto |
| Saída primitiva | `ToIntFunction<T>`, `ToLongFunction<T>`, `ToDoubleFunction<T>` | Recebe objeto, retorna primitivo |
| Tudo primitivo | `IntUnaryOperator`, `IntBinaryOperator`, `IntPredicate`, `IntConsumer`, `IntSupplier` | Sem boxing, máxima performance |
| Conversão | `IntToDoubleFunction`, `LongToIntFunction` | Converte entre primitivos |

```java
// ToIntFunction<T> — extrai int sem boxing
ToIntFunction<String> tamanho = String::length;
int n = tamanho.applyAsInt("Java");   // 4, sem Integer

// IntPredicate — testa int sem boxing
IntPredicate positivo = n2 -> n2 > 0;
positivo.test(5);   // true
```

### Method references (estático / de instância de tipo / de objeto / construtor)

**Method reference** é um atalho de lambda para um método já existente. O compilador resolve qual sobrecarga encaixa no SAM esperado.

**Forma 1 — Referência a método estático** (`Classe::métodoEstático`):

```java
// Lambda equivalente: s -> Integer.parseInt(s)
Function<String, Integer> parse = Integer::parseInt;
parse.apply("42");   // 42
```

**Forma 2 — Referência a método de instância de um objeto específico** (`objeto::método`):

```java
// Lambda equivalente: s -> System.out.println(s)
Consumer<String> imprimir = System.out::println;
imprimir.accept("ola");   // imprime "ola"

// O objeto 'System.out' é capturado no momento da criação da referência
```

**Forma 3 — Referência a método de instância de um tipo arbitrário** (`Tipo::método`):

```java
// Lambda equivalente: s -> s.toUpperCase()
// O primeiro parâmetro do lambda torna-se o receptor do método
Function<String, String> maiusculo = String::toUpperCase;
maiusculo.apply("java");   // "JAVA"

// Com dois parâmetros: (s1, s2) -> s1.compareToIgnoreCase(s2)
Comparator<String> comp = String::compareToIgnoreCase;
```

**Forma 4 — Referência a construtor** (`Classe::new`):

```java
// Lambda equivalente: () -> new ArrayList<>()
Supplier<ArrayList<String>> fabricar = ArrayList::new;
ArrayList<String> lista = fabricar.get();

// Com argumento: n -> new ArrayList<>(n)
IntFunction<ArrayList<String>> comCapacidade = ArrayList::new;
```

Resumo das quatro formas:

| Forma | Sintaxe | Lambda equivalente |
|---|---|---|
| Estático | `Integer::parseInt` | `s -> Integer.parseInt(s)` |
| Objeto específico | `System.out::println` | `s -> System.out.println(s)` |
| Instância de tipo | `String::toUpperCase` | `s -> s.toUpperCase()` |
| Construtor | `ArrayList::new` | `() -> new ArrayList<>()` |

## Na prática

Cenário: um sistema de pedidos onde `Order` tem `getStatus()`, `getCustomerName()` e `getTotal()`. Queremos filtrar pedidos pendentes, extrair nomes de clientes e imprimir.

```java
import java.util.List;
import java.util.function.*;

record Order(String customerName, String status, double total) {}

public class OrderReport {

    // Aceita qualquer Predicate<Order> — reutilizável
    public static List<Order> filter(List<Order> orders, Predicate<Order> condition) {
        return orders.stream()
            .filter(condition)
            .toList();
    }

    // Aceita qualquer Function<Order, String> — reutilizável
    public static List<String> extract(List<Order> orders, Function<Order, String> extractor) {
        return orders.stream()
            .map(extractor)
            .toList();
    }

    public static void main(String[] args) {
        List<Order> orders = List.of(
            new Order("Alice", "PENDING", 150.0),
            new Order("Bob",   "PAID",    320.0),
            new Order("Carol", "PENDING",  89.5)
        );

        // Predicate<Order> — filtra pedidos pendentes
        Predicate<Order> isPending = o -> "PENDING".equals(o.status());

        // Function<Order, String> — extrai nome do cliente
        Function<Order, String> getName = Order::customerName;

        // Pipeline: filtrar → extrair → imprimir via method reference
        filter(orders, isPending)
            .stream()
            .map(getName)
            .forEach(System.out::println);
        // Saída: Alice, Carol
    }
}
```

Pontos do exemplo:
- `Predicate<Order>` e `Function<Order, String>` são passados como parâmetros — os métodos ficam agnósticos à regra de negócio.
- `Order::customerName` é uma referência a método de instância de tipo (Forma 3).
- `System.out::println` é uma referência a método de objeto específico (Forma 2).
- A composição `filter → map → forEach` fica legível sem variáveis intermediárias.

## Armadilhas

### (1) Lambda capturando variável não `effectively final`

**O problema:** lambdas podem capturar variáveis locais do escopo envolvente, mas somente se forem `final` ou *effectively final* — ou seja, nunca reatribuídas após a inicialização. Tentar capturar uma variável que é modificada depois causa erro de compilação.

```java
public void processOrders(List<Order> orders) {
    String prefix = "PEDIDO";

    // ERRO DE COMPILAÇÃO: 'prefix' deixa de ser effectively final após reatribuição
    prefix = "ORDER";   // ← reatribuição invalida a captura

    orders.forEach(o -> System.out.println(prefix + ": " + o.customerName()));
    //                                     ^^^^^^
    // "Variable used in lambda expression should be final or effectively final"
}
```

**Fix:** não reatribua a variável. Se precisar de um valor alternativo, crie uma nova variável final/effectively final:

```java
public void processOrders(List<Order> orders, boolean usePortuguese) {
    String prefix = usePortuguese ? "PEDIDO" : "ORDER";   // atribuído uma vez → effectively final

    orders.forEach(o -> System.out.println(prefix + ": " + o.customerName()));
    // Compila corretamente
}
```

---

### (2) Criar interface funcional própria onde já existe equivalente no JDK

**O problema:** é tentador criar interfaces funcionais específicas para cada contexto, quando o JDK já fornece a interface correta. Isso polui o código com tipos redundantes e impede interoperabilidade com a API de Streams e coleções.

```java
// DESNECESSÁRIO — duplica o que já existe
@FunctionalInterface
interface OrderFilter {
    boolean check(Order order);   // idêntico a Predicate<Order>
}

@FunctionalInterface
interface OrderMapper {
    String extract(Order order);  // idêntico a Function<Order, String>
}
```

**Fix:** use diretamente `Predicate<Order>` e `Function<Order, String>`. Além de eliminar código redundante, os métodos que aceitam essas interfaces ficam automaticamente compatíveis com `.filter()`, `.map()` e demais operações de Stream.

```java
// Correto — reutiliza tipos do JDK; interopera com Stream API
Predicate<Order> isPending   = o -> "PENDING".equals(o.status());
Function<Order, String> name = Order::customerName;

orders.stream()
    .filter(isPending)
    .map(name)
    .forEach(System.out::println);
```

A exceção legítima: criar sua própria interface funcional quando ela precisa lançar checked exceptions (o JDK não fornece variantes que declaram `throws`), ou quando um nome de domínio específico melhora muito a legibilidade para a equipe.

---

### (3) Method reference ambíguo — quando o compilador não consegue resolver

**O problema:** quando existem sobrecargas do método referenciado, o compilador pode não conseguir determinar qual sobrecarga encaixa no SAM alvo, gerando erro de ambiguidade.

```java
// println tem sobrecargas: println(String), println(int), println(Object)...
Consumer<String>  ok  = System.out::println;   // compila — infere println(String)
Consumer<Integer> ok2 = System.out::println;   // compila — infere println(int) via unboxing

// Contexto ambíguo — o compilador não consegue escolher
var ambiguo = System.out::println;  // ERRO: não há tipo alvo para inferência
```

**Fix:** desambigue com lambda explícita (especifica os tipos) ou com cast para o tipo funcional desejado:

```java
// Opção 1: lambda com tipo explícito
Consumer<Object> imprimirObj = obj -> System.out.println(obj);

// Opção 2: forçar inferência via cast para o tipo funcional alvo
Consumer<String> imprimirStr = (Consumer<String>) System.out::println;

// Opção 3: declarar a variável com tipo explícito (mais limpo)
Consumer<String> imprimirStr2 = System.out::println;   // funciona — tipo alvo é conhecido
```

Em geral: method references ambíguos em contexto `var` são o caso mais comum — a solução é sempre tipar a variável explicitamente.

## Em entrevista

### Frase pronta (inglês)

> "A lambda is a concise, anonymous implementation of a functional interface — any interface with exactly one abstract method, which we call a SAM, or Single Abstract Method. The `@FunctionalInterface` annotation is a compile-time guard: the compiler rejects the interface if it has zero or more than one abstract method, but the annotation itself doesn't change runtime behavior."
>
> "The four core shapes in `java.util.function` are `Function<T,R>` for transformation, `Predicate<T>` for boolean testing, `Consumer<T>` for side effects without a return value, and `Supplier<T>` for lazy provision of a value without arguments. Everything else in the package — `BiFunction`, `UnaryOperator`, `IntPredicate` — is a variant or primitive specialization of those four."
>
> "Method references are syntactic sugar for lambdas that do nothing but delegate to an existing method. There are four forms: static method reference like `Integer::parseInt`, instance method of a specific object like `System.out::println`, instance method of an arbitrary object of a type like `String::toUpperCase`, and constructor reference like `ArrayList::new`. The key constraint on lambda capture is that any local variable from the enclosing scope must be effectively final — assigning to it after the lambda captures it is a compile-time error."

### Vocabulário

| Termo PT | Termo EN |
|---|---|
| interface funcional | functional interface |
| método abstrato único | SAM — Single Abstract Method |
| lambda / expressão lambda | lambda / lambda expression |
| captura de variável | variable capture |
| efetivamente final | effectively final |
| referência de método | method reference |
| referência de construtor | constructor reference |
| especialização primitiva | primitive specialization |
| composição de funções | function composition |
| inferência de tipo | type inference |

## Veja também

- [[05 - Introdução à Stream API]]
- [[07 - Operações de Stream — intermediárias e terminais]]
- [[10 - Optional]]
- [[13 - Composição funcional e funções de alta ordem]]
- [[03-Dominios/Java/Collections e Streams/index|Collections e Streams (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Linguagem e sintaxe moderna/08 - Interfaces e classes abstratas|Interfaces e classes abstratas]]
- [[03-Dominios/Java/Dicionário de Java#lambda|lambda]]
- [[03-Dominios/Java/Dicionário de Java#interface funcional|interface funcional]]
- [[03-Dominios/Java/Dicionário de Java#method reference|method reference]]

## Referências

- [Lambda Expressions — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/java/javaOO/lambdaexpressions.html)
- [Method References — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/java/javaOO/methodreferences.html)
- [java.util.function — Javadoc Java 21 (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/function/package-summary.html)
