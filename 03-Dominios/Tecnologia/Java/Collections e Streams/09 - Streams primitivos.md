---
title: "Streams primitivos"
created: 2026-06-04
updated: 2026-06-04
type: concept
progress: backlog
status: seedling
publish: true
fase: Adepto
tags:
  - java
  - collections
  - adepto
  - streams
  - primitivos
aliases:
  - IntStream
  - Streams primitivos
  - Summary statistics
---

# Streams primitivos

> [!abstract] TL;DR
> `IntStream`, `LongStream` e `DoubleStream` são especializações da Stream API para tipos primitivos. Elas eliminam o boxing/unboxing de `Stream<Integer>`, `Stream<Long>` e `Stream<Double>`, oferecendo operações numéricas diretas — `sum()`, `average()`, `min()`, `max()` e `summaryStatistics()` — sem custo de alocação de objetos wrapper. Use `mapToInt`/`mapToLong`/`mapToDouble` para entrar nesse mundo a partir de um `Stream<T>`, e `boxed()` ou `mapToObj()` para sair.

## O que é

`IntStream`, `LongStream` e `DoubleStream` são as especializações primitivas da Stream API, introduzidas no Java 8 no pacote `java.util.stream`. Em vez de empacotar cada valor em um objeto wrapper (`Integer`, `Long`, `Double`) como faria `Stream<Integer>`, elas operam diretamente sobre os tipos primitivos `int`, `long` e `double`.

Da especificação do Javadoc:

> "`IntStream` is a sequence of primitive `int`-valued elements supporting sequential and parallel aggregate operations. This is the `int` primitive specialization of `Stream`."

As três interfaces seguem o mesmo contrato, diferindo apenas no tipo base:

| Interface | Tipo primitivo | Wrapper evitado | Optional de retorno |
|-----------|---------------|-----------------|---------------------|
| `IntStream` | `int` | `Integer` | `OptionalInt` / `OptionalDouble` |
| `LongStream` | `long` | `Long` | `OptionalLong` / `OptionalDouble` |
| `DoubleStream` | `double` | `Double` | `OptionalDouble` |

A classe `IntSummaryStatistics` (pacote `java.util`) agrega count, sum, min, max e average em uma única passagem — obtida via `summaryStatistics()` em qualquer das três interfaces.

## Por que importa

Quando um `Stream<Integer>` processa um milhão de inteiros, cada valor requer um objeto `Integer` no heap: alocação, pressão no GC e acesso indireto à memória. Com `IntStream`, os valores ficam em arrays de `int` na stack ou em regiões compactas de memória — sem overhead de objeto.

Além da performance, as streams primitivas oferecem terminais numéricas que não existem em `Stream<T>`:

- `sum()` — soma direta, sem `reduce` manual
- `average()` — média aritmética (retorna `OptionalDouble`)
- `min()` / `max()` — mínimo e máximo (retornam `OptionalInt`/`OptionalLong`/`OptionalDouble`)
- `summaryStatistics()` — todas as cinco métricas em uma única travessia

Em entrevista, dominar streams primitivos demonstra consciência de performance — algo cobrado para posições sênior.

## Como funciona

### Criação (`range`/`rangeClosed`/`of`/`iterate`/`Arrays.stream`)

```java
// range: início inclusivo, fim exclusivo — [0, 100)
IntStream.range(0, 100);           // 0, 1, 2, ..., 99

// rangeClosed: ambos inclusivos — [1, 100]
IntStream.rangeClosed(1, 100);     // 1, 2, ..., 100

// of: valores literais
IntStream.of(10, 20, 30);

// iterate (infinito com limit, ou finito com predicado)
IntStream.iterate(0, n -> n + 2).limit(5);      // 0, 2, 4, 6, 8
IntStream.iterate(1, n -> n <= 1000, n -> n * 2); // 1, 2, 4, ..., 512

// Arrays.stream — a partir de int[]
int[] valores = {3, 1, 4, 1, 5};
Arrays.stream(valores);            // IntStream dos elementos

// LongStream e DoubleStream: mesma lógica
LongStream.rangeClosed(1L, 1_000_000L);
DoubleStream.of(1.1, 2.2, 3.3);
```

`range` e `rangeClosed` existem em `IntStream` e `LongStream`, mas **não** em `DoubleStream` (intervalos de ponto flutuante não têm cardinalidade natural definida).

### Conversões (`mapToInt`/`mapToObj`/`boxed`/`asLongStream`)

```java
// Stream<T> → IntStream
orders.stream()
    .mapToInt(Order::quantity);        // extrai int de cada elemento

// IntStream → Stream<U>
IntStream.range(1, 6)
    .mapToObj(i -> "item-" + i);       // Stream<String>

// IntStream → Stream<Integer>
IntStream.range(1, 6)
    .boxed();                          // equivale a mapToObj(Integer::valueOf)

// IntStream → LongStream (widening sem perda)
IntStream.range(1, 6)
    .asLongStream();

// IntStream → DoubleStream (widening sem perda)
IntStream.range(1, 6)
    .asDoubleStream();

// LongStream → DoubleStream
LongStream.range(1, 6)
    .asDoubleStream();

// DoubleStream → IntStream (com função de mapeamento)
DoubleStream.of(1.9, 2.5)
    .mapToInt(d -> (int) d);           // trunca — cuidado com dados reais
```

Resumo dos caminhos de conversão:

```
Stream<T> ──mapToInt──▶ IntStream ──asLongStream──▶ LongStream
                              │                          │
                              └──asDoubleStream──▶ DoubleStream
                              │                          │
                         mapToObj / boxed            mapToObj / boxed
                              │                          │
                         Stream<U>                  Stream<U>
```

### Operações numéricas (`sum`/`average`/`min`/`max` → `OptionalInt`/`OptionalDouble`)

```java
IntStream numeros = IntStream.of(3, 1, 4, 1, 5, 9, 2, 6);

int soma       = numeros.sum();                // int — 31
// atenção: numeros está consumida após sum(); criar novo IntStream para as próximas

OptionalDouble media = IntStream.of(3, 1, 4).average();  // OptionalDouble
media.orElse(0.0);                                        // 2.6666...

OptionalInt minimo = IntStream.of(3, 1, 4).min();        // OptionalInt
minimo.getAsInt();                                        // 1

OptionalInt maximo = IntStream.of(3, 1, 4).max();        // OptionalInt
maximo.getAsInt();                                        // 4

// Stream vazia — Optional.empty
OptionalInt vazio = IntStream.empty().min();              // OptionalInt.empty
vazio.isPresent();                                        // false
```

`sum()` retorna 0 para stream vazia (identidade da soma). `average()`, `min()` e `max()` retornam `Optional` vazio para stream vazia, pois não há resposta definida.

### `summaryStatistics()` (`IntSummaryStatistics`: count/sum/min/max/average de uma vez)

Quando você precisa de mais de uma métrica sobre o mesmo conjunto, `summaryStatistics()` percorre a stream **uma única vez** e agrega tudo:

```java
IntSummaryStatistics stats = IntStream.rangeClosed(1, 10)
    .summaryStatistics();

stats.getCount();    // long  — 10
stats.getSum();      // long  — 55
stats.getMin();      // int   — 1
stats.getMax();      // int   — 10
stats.getAverage();  // double — 5.5
```

Isso é superior a calcular `sum()`, `count()`, `min()` e `max()` separadamente (quatro travessias vs. uma). `IntSummaryStatistics` está em `java.util`; há `LongSummaryStatistics` e `DoubleSummaryStatistics` para as outras especializações.

Em stream vazia, `getMin()` retorna `Integer.MAX_VALUE` e `getMax()` retorna `Integer.MIN_VALUE` (valores sentinela do construtor vazio — verifique `getCount() > 0` antes de usar esses resultados).

### Custo de boxing/unboxing e quando o ganho compensa

O boxing converte um `int` primitivo em um objeto `Integer` no heap. Em um `Stream<Integer>` com N elementos:

- N objetos `Integer` alocados
- N referências de 4-8 bytes no array de objetos
- Acesso indireto (ponteiro → objeto → valor)
- Pressão extra no garbage collector

Com `IntStream`, os valores ficam compactados como `int[]` — acesso direto, localidade de cache maximizada.

**Quando o ganho compensa:**

| Cenário | Recomendação |
|---------|--------------|
| Coleção com milhares de inteiros ou mais | Use `IntStream` via `mapToInt` |
| Cálculo de soma, média, min, max | Use `IntStream` diretamente |
| Loop de intervalo (`for i = 0; i < n`) | `IntStream.range(0, n)` ou loop convencional (diferença pequena) |
| Poucos elementos (dezenas) | Indiferente — legibilidade prevalece |
| Resultado precisa de `Stream<Integer>` para collector | `boxed()` no final |

## Na prática

```java
// Média de quantidades de uma lista de pedidos
OptionalDouble mediaQuantidade = orders.stream()
    .mapToInt(Order::quantity)
    .average();
double resultado = mediaQuantidade.orElse(0.0);

// Soma de 1 a 100 com rangeClosed
int soma = IntStream.rangeClosed(1, 100).sum(); // 5050

// summaryStatistics para relatório de preços (em centavos)
IntSummaryStatistics statsPrecos = catalog.stream()
    .mapToInt(Product::priceInCents)
    .summaryStatistics();

System.out.printf(
    "Total: %d produtos | Soma: R$ %.2f | Min: R$ %.2f | Max: R$ %.2f | Média: R$ %.2f%n",
    statsPrecos.getCount(),
    statsPrecos.getSum()     / 100.0,
    statsPrecos.getMin()     / 100.0,
    statsPrecos.getMax()     / 100.0,
    statsPrecos.getAverage() / 100.0
);

// Verificar se há itens antes de usar min/max
if (statsPrecos.getCount() > 0) {
    int menorPreco = statsPrecos.getMin();
}

// Construir array de índices e mapear para objetos
String[] letras = IntStream.range(0, alphabet.length)
    .mapToObj(i -> alphabet[i] + ":" + i)
    .toArray(String[]::new);
```

## Armadilhas

### (1) Usar `Stream<Integer>` onde `IntStream` serve — boxing em volume

```java
// ERRADO — cria N objetos Integer desnecessariamente
long total = orders.stream()
    .map(Order::quantity)          // Stream<Integer> — boxing
    .reduce(0, Integer::sum);

// CORRETO — operação nativa sem boxing
long total = orders.stream()
    .mapToInt(Order::quantity)     // IntStream
    .sum();
```

O sinal de alerta: `Stream<Integer>` com `.reduce(0, Integer::sum)` ou `.mapToInt(Integer::intValue)` logo depois são indícios de que se deveria ter usado `mapToInt` desde o início.

### (2) Esquecer `boxed()` ao precisar de `Stream<Integer>` para um collector

```java
// ERRADO — IntStream não tem Collectors.toList() diretamente
List<Integer> lista = IntStream.range(1, 6)
    .collect(Collectors.toList()); // erro de compilação: incompatible types

// CORRETO — boxed() converte IntStream → Stream<Integer>
List<Integer> lista = IntStream.range(1, 6)
    .boxed()
    .collect(Collectors.toList());

// Alternativa — toArray direto se lista não for necessária
int[] array = IntStream.range(1, 6).toArray();
```

### (3) `average()` retorna `OptionalDouble`, não `double` — tratar stream vazia

```java
// ERRADO — lança NoSuchElementException se a stream estiver vazia
double media = orders.stream()
    .mapToInt(Order::quantity)
    .average()
    .getAsDouble();   // explode em stream vazia

// CORRETO — fornecer valor padrão
double media = orders.stream()
    .mapToInt(Order::quantity)
    .average()
    .orElse(0.0);

// Alternativa — verificar antes
OptionalDouble opt = orders.stream()
    .mapToInt(Order::quantity)
    .average();
if (opt.isPresent()) {
    process(opt.getAsDouble());
}
```

O mesmo vale para `min()` e `max()` que retornam `OptionalInt` / `OptionalLong` / `OptionalDouble` — nunca chamar `getAsInt()` sem verificar `isPresent()` ou usar `orElse`.

## Em entrevista

### Frase pronta (inglês)

> "Java provides three primitive stream specializations — `IntStream`, `LongStream`, and `DoubleStream` — that avoid the boxing and unboxing overhead of `Stream<Integer>`, `Stream<Long>`, and `Stream<Double>`. When you have a large collection of numeric values and need to compute aggregates, using `mapToInt()` to switch to an `IntStream` and then calling `sum()`, `average()`, `min()`, or `max()` is significantly more efficient than wrapping every value in a heap-allocated wrapper object."
>
> "These specialized streams expose terminal operations that do not exist on a generic `Stream<T>`: `sum()` returns a plain `int`/`long`/`double`, while `average()`, `min()`, and `max()` return the corresponding `Optional` types — `OptionalDouble`, `OptionalInt`, or `OptionalLong` — to safely handle the empty-stream case."
>
> "When you need multiple statistics in one pass, `summaryStatistics()` returns an `IntSummaryStatistics` object that combines count, sum, min, max, and average without traversing the stream multiple times. To go back to a boxed `Stream<Integer>`, you call `boxed()` on the `IntStream`, which is necessary when you need to pass the result to a collector or an API that expects object types."

### Vocabulário

| Termo PT | Termo EN |
|----------|----------|
| stream primitivo | primitive stream |
| boxing / unboxing | boxing / unboxing |
| tipo primitivo | primitive type |
| tipo wrapper / envoltório | wrapper type |
| operação numérica | numeric terminal operation |
| estatísticas resumidas | summary statistics |
| stream vazia | empty stream |
| valor sentinela | sentinel value |
| travessia única | single-pass traversal |
| converter para boxed | box the stream / call `boxed()` |
| intervalo fechado | closed range (`rangeClosed`) |
| pressão no GC | GC pressure |

## Veja também

- [[05 - Introdução à Stream API]]
- [[07 - Operações de Stream — intermediárias e terminais]]
- [[08 - Collectors e agrupamento]]
- [[03-Dominios/Tecnologia/Java/Collections e Streams/index|Collections e Streams (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#stream primitivo (IntStream)|stream primitivo]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#boxing / unboxing|boxing / unboxing]]

## Referências

- [IntStream — Java SE 21 API Docs (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/stream/IntStream.html)
- [LongStream — Java SE 21 API Docs (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/stream/LongStream.html)
- [DoubleStream — Java SE 21 API Docs (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/stream/DoubleStream.html)
- [IntSummaryStatistics — Java SE 21 API Docs (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/IntSummaryStatistics.html)
