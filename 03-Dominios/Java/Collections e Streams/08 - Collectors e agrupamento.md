---
title: "Collectors e agrupamento"
created: 2026-06-04
updated: 2026-06-04
type: concept
progress: backlog
status: seedling
publish: true
fase: adepto
tags:
  - java
  - collections
  - adepto
  - streams
  - collectors
aliases:
  - Collectors
  - groupingBy
  - toMap
---

# Collectors e agrupamento

> [!abstract] TL;DR
> Um **`Collector`** é uma *receita de redução mutável*: ele descreve como acumular os elementos de um stream dentro de um contêiner mutável (uma lista, um mapa, um `StringBuilder`) e como produzir o resultado final. Quem executa essa receita é a operação terminal `collect`. A classe utilitária `java.util.stream.Collectors` é uma fábrica de coletores prontos: `toList`, `toSet`, `toMap`, `joining`, `groupingBy`, `partitioningBy`, `counting`, `summingInt`, `mapping`, `collectingAndThen`, `reducing` e `teeing` (Java 12). O ponto que mais cai em entrevista é o **`groupingBy` com downstream collector** — agrupar e, ao mesmo tempo, contar/somar/mapear cada grupo — e a diferença conceitual entre `collect` (redução **mutável**) e `reduce` (redução **imutável**).

## O que é

Um **`Collector<T, A, R>`** é uma estratégia de **redução mutável**: a partir de elementos de tipo `T`, acumula-os em um contêiner intermediário mutável de tipo `A` (o *accumulator*) e produz um resultado final de tipo `R`. Ele é apenas a *especificação* da operação — não percorre nada por conta própria. Quem dispara a travessia do stream e aplica a receita é a operação terminal `collect(Collector)`.

A classe `java.util.stream.Collectors` é uma **fábrica de coletores comuns**, todos métodos estáticos. Em vez de implementar a interface `Collector` à mão (assunto avançado, coberto em [[15 - Collectors customizados e Gatherers]]), você combina os coletores prontos.

```java
// Collector é a receita; collect é quem executa
List<Order> ativos = orders.stream()
    .filter(Order::isActive)
    .collect(Collectors.toList()); // toList() devolve um Collector; collect o aplica
```

A documentação resume bem o papel da classe:

> "The `Collectors` class contains many useful reduction operations, such as accumulating elements into collections and summarizing elements according to various criteria."

A grande sacada dos coletores é que eles **compõem**: o resultado de um agrupamento pode ser, por sua vez, reduzido por outro coletor (o *downstream*). É isso que transforma `groupingBy` em uma ferramenta de sumarização declarativa, não apenas de particionamento.

## Por que importa

Sem coletores, agrupar e sumarizar dados volta a ser código imperativo verboso: criar um `Map` vazio, iterar, fazer `computeIfAbsent`, acumular manualmente. Com `Collectors`, a mesma intenção vira uma única expressão declarativa que diz *o quê* você quer — "agrupe por status e conte cada grupo" — sem o *como*.

```java
// Imperativo — boilerplate de agrupamento manual
Map<Status, Long> contagem = new HashMap<>();
for (Order o : orders) {
    contagem.merge(o.status(), 1L, Long::sum);
}

// Declarativo — a mesma intenção em uma linha
Map<Status, Long> contagem = orders.stream()
    .collect(Collectors.groupingBy(Order::status, Collectors.counting()));
```

Em entrevistas técnicas, **`Collectors` é o tópico de stream que mais aparece logo depois das operações intermediárias e terminais básicas** (cobertas em [[07 - Operações de Stream — intermediárias e terminais]]). Recrutadores cobram especialmente: o `groupingBy` com downstream, o que acontece com chaves duplicadas no `toMap`, e por que `collect` é "mutável" e `reduce` é "imutável". Saber recitar `toList()` não basta — o diferencial sênior é combinar coletores e prever os tipos de retorno.

## Como funciona

### Coletar em coleção (`toList`/`toUnmodifiableList`/`toSet`/`toCollection`)

Os coletores mais básicos materializam o stream em uma coleção.

```java
// toList() — List, sem garantia de tipo/mutabilidade/serialização
List<Order> lista = orders.stream()
    .filter(Order::isActive)
    .collect(Collectors.toList());

// toUnmodifiableList() — List IMUTÁVEL, em ordem de encontro (Java 10+)
// rejeita nulls: lança NullPointerException se algum elemento for null
List<Order> imutavel = orders.stream()
    .collect(Collectors.toUnmodifiableList());

// toSet() — Set, coletor "unordered", sem garantia de tipo
Set<Customer> clientes = orders.stream()
    .map(Order::customer)
    .collect(Collectors.toSet());

// toCollection(Supplier) — você escolhe a implementação concreta
TreeSet<String> ordenado = orders.stream()
    .map(Order::id)
    .collect(Collectors.toCollection(TreeSet::new));
LinkedList<Order> fila = orders.stream()
    .collect(Collectors.toCollection(LinkedList::new));
```

> [!note] `Stream.toList()` vs `Collectors.toList()`
> Desde o Java 16 existe `Stream.toList()` (sem `collect`), que devolve uma lista **imutável** em ordem de encontro. Não confunda com `Collectors.toList()`, que **não** garante mutabilidade nem imutabilidade — apenas "uma `List`". Se precisa de imutabilidade explícita via coletor, use `toUnmodifiableList()`.

Assinaturas:

```java
static <T>            Collector<T,?,List<T>> toList()
static <T>            Collector<T,?,List<T>> toUnmodifiableList()   // Java 10+
static <T>            Collector<T,?,Set<T>>  toSet()
static <T,C extends Collection<T>> Collector<T,?,C> toCollection(Supplier<C> factory)
```

### `toMap` e o **merge function** (chave duplicada)

`toMap` constrói um `Map` aplicando uma função de chave e uma de valor a cada elemento. O detalhe crítico: a versão de dois argumentos **lança `IllegalStateException`** se duas entradas produzirem a mesma chave.

```java
// Indexar pedidos por id (ids são únicos → seguro)
Map<String, Order> porId = orders.stream()
    .collect(Collectors.toMap(Order::id, Function.identity()));
```

Quando há risco de colisão de chave, use a sobrecarga com **merge function** — um `BinaryOperator<U>` que decide qual valor manter quando a chave já existe:

```java
// Total gasto por cliente — vários pedidos por cliente → chaves repetem
Map<Customer, Double> gastoPorCliente = orders.stream()
    .collect(Collectors.toMap(
        Order::customer,
        Order::total,
        Double::sum));        // merge: soma os totais em colisão

// "Fique com o último" — sobrescreve o valor anterior
Map<Customer, Order> ultimoPedido = orders.stream()
    .collect(Collectors.toMap(
        Order::customer,
        Function.identity(),
        (anterior, novo) -> novo));

// Quarta sobrecarga: escolher a implementação do Map (ex.: LinkedHashMap, TreeMap)
Map<Customer, Double> ordenado = orders.stream()
    .collect(Collectors.toMap(
        Order::customer,
        Order::total,
        Double::sum,
        LinkedHashMap::new));
```

Assinaturas:

```java
static <T,K,U> Collector<T,?,Map<K,U>> toMap(Function keyMapper, Function valueMapper)
static <T,K,U> Collector<T,?,Map<K,U>> toMap(Function keyMapper, Function valueMapper,
                                             BinaryOperator<U> mergeFunction)
static <T,K,U,M extends Map<K,U>> Collector<T,?,M> toMap(Function keyMapper, Function valueMapper,
                                             BinaryOperator<U> mergeFunction, Supplier<M> mapFactory)
```

### `joining` (concatenar strings)

Concatena os elementos (`CharSequence`) em uma única `String`, em ordem de encontro. Tem três sobrecargas: sem argumento, só delimitador, ou delimitador + prefixo + sufixo.

```java
// Sem delimitador
String ids = orders.stream().map(Order::id).collect(Collectors.joining());
// "A1B2C3"

// Com delimitador
String csv = orders.stream().map(Order::id).collect(Collectors.joining(", "));
// "A1, B2, C3"

// Delimitador + prefixo + sufixo
String json = orders.stream().map(Order::id)
    .collect(Collectors.joining(", ", "[", "]"));
// "[A1, B2, C3]"
```

> [!tip] `joining` usa `StringBuilder` por baixo
> O coletor `joining` acumula em um `StringBuilder` (contêiner mutável), o que é muito mais eficiente do que `reduce((a, b) -> a + b)` com `String` — este último cria uma nova `String` a cada passo. É o exemplo canônico de por que `collect` (mutável) vence `reduce` (imutável) para concatenação.

### **`groupingBy`** e downstream collectors (`counting`/`summingInt`/`averagingDouble`/`mapping`/`toList`)

O `groupingBy` é o coletor estrela. Na forma de **um argumento**, aplica uma função classificadora e devolve `Map<K, List<T>>` — cada chave aponta para a lista dos elementos daquele grupo.

```java
// Map<Status, List<Order>>
Map<Status, List<Order>> porStatus = orders.stream()
    .collect(Collectors.groupingBy(Order::status));
```

A forma de **dois argumentos** recebe um **downstream collector**: em vez de coletar cada grupo em uma lista, aplica outra redução a cada grupo. É a fonte de quase todo o poder da classe.

```java
// Contar quantos pedidos por status → Map<Status, Long>
Map<Status, Long> contagem = orders.stream()
    .collect(Collectors.groupingBy(Order::status, Collectors.counting()));

// Somar o total de cada status → Map<Status, Integer>
// (summingInt devolve Integer; aqui o total em centavos)
Map<Status, Integer> totalCentavos = orders.stream()
    .collect(Collectors.groupingBy(Order::status,
             Collectors.summingInt(Order::totalCents)));

// Média de itens por status → Map<Status, Double>
Map<Status, Double> mediaItens = orders.stream()
    .collect(Collectors.groupingBy(Order::status,
             Collectors.averagingDouble(Order::itemCount)));

// mapping: transformar antes de coletar o grupo
// agrupa por cliente, mas coleta apenas os IDS dos pedidos
Map<Customer, List<String>> idsPorCliente = orders.stream()
    .collect(Collectors.groupingBy(Order::customer,
             Collectors.mapping(Order::id, Collectors.toList())));
```

Há ainda a forma de **três argumentos**, que aceita um *map supplier* para escolher a implementação do mapa (por exemplo, `TreeMap` para chaves ordenadas):

```java
// Map ORDENADO por status (TreeMap)
Map<Status, Long> ordenado = orders.stream()
    .collect(Collectors.groupingBy(Order::status, TreeMap::new, Collectors.counting()));
```

Assinaturas:

```java
static <T,K>     Collector<T,?,Map<K,List<T>>> groupingBy(Function classifier)
static <T,K,A,D> Collector<T,?,Map<K,D>>       groupingBy(Function classifier,
                                                          Collector<? super T,A,D> downstream)
static <T,K,D,A,M extends Map<K,D>> Collector<T,?,M> groupingBy(Function classifier,
                                                          Supplier<M> mapFactory,
                                                          Collector<? super T,A,D> downstream)
```

> [!note] Downstream collectors são "Lego"
> `counting()`, `summingInt(...)`, `averagingDouble(...)`, `mapping(...)`, `toList()`, `toSet()`, `joining(...)`, `reducing(...)` e até outro `groupingBy(...)` aninhado podem todos entrar na posição de downstream. Agrupamento de dois níveis (`groupingBy` dentro de `groupingBy`) produz um `Map<K1, Map<K2, ...>>` — comum em relatórios.

### `partitioningBy` (predicado → 2 grupos)

`partitioningBy` é um caso especial de agrupamento por um **`Predicate`**: sempre produz um `Map<Boolean, ...>` com **exatamente duas chaves**, `true` e `false` — ambas presentes mesmo que um dos lados esteja vazio.

```java
// Map<Boolean, List<Order>> — { true=[ativos], false=[inativos] }
Map<Boolean, List<Order>> particao = orders.stream()
    .collect(Collectors.partitioningBy(Order::isActive));

List<Order> ativos   = particao.get(true);
List<Order> inativos = particao.get(false);

// Também aceita downstream — contar cada partição
Map<Boolean, Long> contagem = orders.stream()
    .collect(Collectors.partitioningBy(Order::isActive, Collectors.counting()));
```

> [!tip] `partitioningBy` vs `groupingBy(predicado)`
> Você poderia usar `groupingBy(o -> o.isActive())` e obter `Map<Boolean, ...>` também — mas `partitioningBy` é mais eficiente (usa uma estrutura otimizada para dois buckets) e **garante** as duas chaves. Com `groupingBy`, se nenhum elemento cair no `false`, a chave `false` simplesmente não existe no mapa.

### `collectingAndThen`/`reducing`/`teeing`

**`collectingAndThen`** envolve um coletor com uma transformação final (*finisher*). O uso clássico é tornar o resultado imutável ou aplicar `Optional`:

```java
// Coleta em List e a torna imutável em uma só expressão
List<Order> imutavel = orders.stream()
    .collect(Collectors.collectingAndThen(
        Collectors.toList(),
        Collections::unmodifiableList));
```

**`reducing`** é o coletor de redução geral (o análogo a `Stream.reduce`, mas usável como downstream de `groupingBy`). Tem três sobrecargas — só operador (devolve `Optional<T>`), identidade + operador, e identidade + mapper + operador.

```java
// Pedido de maior total dentro de cada status (reducing como downstream)
Map<Status, Optional<Order>> maiorPorStatus = orders.stream()
    .collect(Collectors.groupingBy(Order::status,
             Collectors.reducing(BinaryOperator.maxBy(
                 Comparator.comparingInt(Order::totalCents)))));
```

**`teeing`** (Java 12) bifurca os elementos para **dois** coletores e combina os dois resultados com um `BiFunction`. Útil para calcular duas agregações em uma única passada.

```java
// Média de total em UMA passada: soma e contagem juntas via teeing (Java 12+)
double media = orders.stream()
    .collect(Collectors.teeing(
        Collectors.summingDouble(Order::total),  // R1: soma
        Collectors.counting(),                    // R2: contagem
        (soma, n) -> n == 0 ? 0.0 : soma / n));   // merge
```

### `collect` (mutável) vs `reduce` (imutável)

Esta é a distinção conceitual que sustenta toda a classe `Collectors`. A documentação coloca de forma direta:

> "The `reduce` operation always returns a new value. (...) Unlike the `reduce` method, which always creates a new value when it processes an element, the `collect` method modifies, or mutates, an existing value."

- **`reduce`** é uma redução **imutável**: o acumulador é um valor (`int`, `String`, um objeto imutável) e cada passo produz um **novo** valor. Ideal para somar, multiplicar, achar o máximo — operações sobre valores.
- **`collect`** é uma redução **mutável**: existe um contêiner mutável único (`ArrayList`, `HashMap`, `StringBuilder`) que é **modificado in-place** a cada elemento. Ideal quando o resultado é uma coleção ou um agregado complexo, porque evita criar uma estrutura nova por elemento.

```java
// reduce — imutável: somar idades, cada passo gera um novo Integer
int totalCents = orders.stream()
    .map(Order::totalCents)
    .reduce(0, Integer::sum);

// collect — mutável: acumular em uma única List (sem recriar a lista a cada passo)
List<String> ids = orders.stream()
    .map(Order::id)
    .collect(Collectors.toList());
```

> [!warning] Não use `reduce` para construir coleções
> Fazer `reduce(new ArrayList<>(), (lista, e) -> { lista.add(e); return lista; }, ...)` é o anti-padrão clássico: em paralelo, o contêiner compartilhado corrompe; em sequencial, ainda viola o contrato de não-mutação do `reduce`. Para acumular em coleção, **sempre** `collect`.

## Na prática

```java
// 1) Contar pedidos por status
Map<Status, Long> contagemPorStatus = orders.stream()
    .collect(Collectors.groupingBy(Order::status, Collectors.counting()));

// 2) IDs dos pedidos agrupados por cliente (groupingBy + mapping + toList)
Map<Customer, List<String>> idsPorCliente = orders.stream()
    .collect(Collectors.groupingBy(
        Order::customer,
        Collectors.mapping(Order::id, Collectors.toList())));
```

Um relatório típico — **top 5 clientes por valor gasto**, combinando agrupamento, `entrySet().stream()`, ordenação e um `toMap` ordenado:

```java
// Total gasto por cliente, depois top 5 em ordem decrescente
Map<Customer, Double> top5 = orders.stream()
    .collect(Collectors.groupingBy(
        Order::customer,
        Collectors.summingDouble(Order::total)))   // Map<Customer, Double>
    .entrySet().stream()                            // Stream<Map.Entry<Customer, Double>>
    .sorted(Map.Entry.<Customer, Double>comparingByValue().reversed())
    .limit(5)
    .collect(Collectors.toMap(
        Map.Entry::getKey,
        Map.Entry::getValue,
        (a, b) -> a,            // merge irrelevante (chaves já únicas), mas obrigatório
        LinkedHashMap::new));   // LinkedHashMap preserva a ordem do top 5
```

Note o padrão "agrupa → re-streama o `entrySet` → ordena → `limit` → recoleta". Ele aparece em praticamente todo relatório de ranking, e o `LinkedHashMap::new` no `toMap` final é o que preserva a ordem da ordenação (um `HashMap` a perderia).

## Armadilhas

### (1) `toMap` com chave duplicada lança `IllegalStateException`

**O problema:** a versão de dois argumentos de `toMap` não tolera chaves repetidas — ao encontrar a segunda entrada com a mesma chave, lança `IllegalStateException: Duplicate key`.

```java
// ERRADO — vários pedidos têm o mesmo cliente → chave duplica
Map<Customer, Double> gasto = orders.stream()
    .collect(Collectors.toMap(Order::customer, Order::total));
// IllegalStateException: Duplicate key Customer[...] (attempted merging values ...)
```

**Fix:** forneça uma **merge function** que decida como combinar valores em colisão:

```java
// CORRETO — soma os totais quando a chave (cliente) repete
Map<Customer, Double> gasto = orders.stream()
    .collect(Collectors.toMap(Order::customer, Order::total, Double::sum));

// Ou "fique com o primeiro": (a, b) -> a   |   "fique com o último": (a, b) -> b
```

---

### (2) Assumir que o mapa de `groupingBy` (ou suas listas) é imutável

**O problema:** o `Map` devolvido por `groupingBy` e as `List` de cada grupo são **mutáveis** (não há garantia de imutabilidade). Código que confia em imutabilidade pode ser corrompido por mutação acidental rio abaixo.

```java
// ERRADO — assumir que não dá pra mexer
Map<Status, List<Order>> grupos = orders.stream()
    .collect(Collectors.groupingBy(Order::status));
grupos.get(Status.OPEN).clear();  // compila e executa — esvazia o grupo!
grupos.put(Status.CLOSED, null);  // também permitido
```

**Fix:** se precisa de listas imutáveis por grupo, use `toUnmodifiableList()` como downstream (e, se quiser, `collectingAndThen` para blindar o mapa externo):

```java
// CORRETO — cada grupo é uma List imutável
Map<Status, List<Order>> grupos = orders.stream()
    .collect(Collectors.groupingBy(
        Order::status,
        Collectors.toUnmodifiableList()));
grupos.get(Status.OPEN).clear();  // UnsupportedOperationException
```

---

### (3) Downstream errado: `counting()` devolve `Long`, não `Integer`

**O problema:** o tipo de retorno do downstream determina o tipo de valor do mapa. `counting()` devolve **`Long`**, não `Integer`; `summingInt(...)` devolve `Integer`; `summingDouble(...)`/`averagingInt(...)`/`averagingDouble(...)` devolvem `Double`. Declarar o tipo errado quebra a compilação.

```java
// ERRADO — counting() é Long, não Integer
Map<Status, Integer> contagem = orders.stream()
    .collect(Collectors.groupingBy(Order::status, Collectors.counting()));
// erro de compilação: incompatible types — Map<Status,Long> não cabe em Map<Status,Integer>
```

**Fix:** declare o tipo que o downstream realmente produz (ou use `var`):

```java
// CORRETO — Long, casando com counting()
Map<Status, Long> contagem = orders.stream()
    .collect(Collectors.groupingBy(Order::status, Collectors.counting()));

// Tabela rápida de tipos de retorno dos downstreams numéricos:
//   counting()          -> Long
//   summingInt          -> Integer      summingLong -> Long      summingDouble -> Double
//   averagingInt/Long/Double -> Double  (sempre Double)
```

> [!tip] Use `var` quando o tipo do coletor for verboso
> Em agrupamentos aninhados (`groupingBy` dentro de `groupingBy`), o tipo declarado fica gigantesco. `var resultado = ...` deixa o compilador inferir e evita erros como o do `Long`/`Integer` acima.

## Em entrevista

### Frase pronta (inglês)

> "A `Collector` is a recipe for a *mutable reduction*: it specifies how to accumulate stream elements into a mutable container — a list, a map, a `StringBuilder` — and how to produce the final result. The terminal operation `collect` is what actually runs that recipe. The `Collectors` class is a factory of ready-made collectors: `toList`, `toSet`, `toMap`, `joining`, `groupingBy`, `partitioningBy`, and reduction helpers like `counting` and `summingInt`."
>
> "The most powerful one is `groupingBy` with a downstream collector. The single-argument form returns a `Map<K, List<T>>`, but the two-argument form lets you reduce each group on the fly — for example, `groupingBy(Order::status, counting())` returns a `Map<Status, Long>` of counts per status. `partitioningBy` is a special case that splits elements by a predicate into a `Map<Boolean, ...>` that always contains both the true and false keys."
>
> "Two gotchas I always mention: `toMap` with duplicate keys throws `IllegalStateException` unless you supply a merge function, and the map returned by `groupingBy` is mutable — if I need immutability per group I use `toUnmodifiableList` as the downstream. Conceptually, `collect` is a mutable reduction that modifies one container in place, whereas `reduce` is an immutable reduction that produces a brand-new value at every step — so I never build collections with `reduce`."

### Vocabulário

| Termo PT | Termo EN |
|----------|----------|
| coletor | collector |
| redução mutável | mutable reduction |
| redução imutável | immutable reduction |
| agrupar por | group by |
| função classificadora | classifier function |
| coletor downstream | downstream collector |
| função de mesclagem | merge function |
| chave duplicada | duplicate key |
| particionar por predicado | partition by predicate |
| transformação final | finishing transformation (finisher) |
| concatenar | join / concatenate |
| sumarizar | summarize |

## Veja também

- [[05 - Introdução à Stream API]]
- [[07 - Operações de Stream — intermediárias e terminais]]
- [[09 - Streams primitivos]]
- [[15 - Collectors customizados e Gatherers]]
- [[03-Dominios/Java/Collections e Streams/index|Collections e Streams (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Dicionário de Java#Collector (coletor)|Collector]]
- [[03-Dominios/Java/Dicionário de Java#groupingBy|groupingBy]]

## Referências

- [Collectors — Java SE 21 API Docs (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/stream/Collectors.html)
- [Reduction — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/collections/streams/reduction.html)
