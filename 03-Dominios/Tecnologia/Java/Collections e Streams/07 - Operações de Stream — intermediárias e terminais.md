---
title: "Operações de Stream — intermediárias e terminais"
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
aliases:
  - "Operações de stream"
  - "map filter reduce"
  - "flatMap"
---

# Operações de Stream — intermediárias e terminais

> [!abstract] TL;DR
> **Operações intermediárias** transformam um `Stream` em outro `Stream` e são **lazy** — não executam nada até que uma operação terminal seja invocada. **Operações terminais** encerram o pipeline, produzem um resultado concreto (lista, valor, booleano) ou realizam um efeito colateral, e são **eager** — disparam toda a execução acumulada. Conhecer o catálogo completo — com as adições do Java 9 (`takeWhile`/`dropWhile`) e do Java 16 (`mapMulti`, `toList()`) — e entender quando cada operação é stateful, short-circuit ou stateless é exatamente o que diferencia respostas medianas de respostas sênior em entrevistas.

## O que é

Um pipeline de Stream é uma cadeia inerte até o momento em que a operação terminal é acionada. Isso não é apenas um detalhe de implementação — é uma característica arquitetural que permite otimizações como **fusão de loops** (loop fusion) e **curto-circuito** que não seriam possíveis em avaliação eager.

A especificação do Java classifica as operações em dois eixos independentes:

| Eixo | Categorias |
|------|-----------|
| **Quando executa** | *lazy* (intermediária) vs. *eager* (terminal) |
| **Dependência de estado** | *stateless* (cada elemento independente) vs. *stateful* (precisa ver múltiplos elementos) |
| **Completude** | *short-circuit* (pode parar antes do fim da fonte) vs. *full* (precisa processar tudo) |

Entender esses eixos importa porque operações **stateful** (`sorted`, `distinct`, `limit`) consomem memória proporcional ao que já processaram, enquanto operações **stateless** (`filter`, `map`) processam cada elemento e descartam na hora. E operações **short-circuit** (`limit`, `findFirst`, `anyMatch`) tornam viável trabalhar com streams infinitos (`Stream.generate`, `Stream.iterate`).

## Por que importa

Dominantes sênior não "sabem que `filter` existe" — eles entendem por que o compilador pode reordenar internamente operações stateless, por que `sorted()` quebra o processamento elemento-a-elemento e carrega tudo na memória antes de emitir o primeiro resultado, e por que `peek` não é confiável como mecanismo de efeito em pipelines com otimização.

Esses detalhes aparecem constantemente em entrevistas de sistema distribuído, quando a conversa passa de "o que você usaria" para "por que isso funciona assim em paralelo" — e é onde a nota [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/15 - Parallel streams e fork-join|Parallel streams]] aprofunda o modelo de execução concorrente.

## Como funciona

### Intermediárias de transformação (`map`/`mapToObj`/`flatMap`/`mapMulti`)

Todas **stateless** — aplicam uma função a cada elemento individualmente, sem olhar para o contexto dos demais.

**`map(Function<T, R>)`** — transforma cada elemento de `T` para `R`. Um-para-um.

```java
// List<Order> → List<String> com os IDs
List<String> ids = orders.stream()
    .map(Order::getId)
    .toList();
```

**`mapToInt`/`mapToLong`/`mapToDouble`** — variantes que produzem streams primitivos (`IntStream`, `LongStream`, `DoubleStream`), eliminando boxing. Ver [[09 - Streams primitivos]] para o universo completo de streams primitivos.

**`mapToObj(IntFunction<R>)`** — caminho inverso: `IntStream` → `Stream<R>`.

**`flatMap(Function<T, Stream<R>>)`** — substitui cada elemento por um `Stream` de zero ou mais elementos e "achata" (flatten) tudo num único stream. Um-para-muitos.

```java
// List<Order> onde cada Order tem List<String> itens
// Queremos Stream<String> de todos os itens de todos os pedidos
List<String> todosItens = orders.stream()
    .flatMap(order -> order.getItems().stream())
    .toList();
```

A diferença entre `map` e `flatMap`: `map` produziria `Stream<List<String>>` (lista de listas), `flatMap` produz `Stream<String>` (lista plana).

**`mapMulti(BiConsumer<T, Consumer<R>>)`** *(Java 16)* — alternativa imperativa ao `flatMap` que evita a criação de um `Stream` intermediário por elemento. Mais eficiente quando o número de elementos resultantes por entrada é pequeno.

```java
// Mesmo efeito que flatMap, mas sem criar Stream por Order
List<String> todosItens = orders.<String>mapMulti((order, consumer) -> {
    for (String item : order.getItems()) {
        consumer.accept(item);
    }
}).toList();
```

Quando prefer `mapMulti` sobre `flatMap`: quando a lambda produziria zero ou um elemento na maioria dos casos (o overhead de criar um `Stream` vazio ou singleton é evitado) ou quando a lógica de geração é naturalmente imperativa com condições complexas.

---

### Intermediárias de filtragem/fatiamento (`filter`/`distinct`/`sorted`/`limit`/`skip`/`takeWhile`/`dropWhile`/`peek`)

**`filter(Predicate<T>)`** — **stateless, short-circuit não** (precisa testar cada elemento). Emite apenas os elementos que satisfazem o predicado.

```java
List<Order> ativos = orders.stream()
    .filter(Order::isActive)
    .toList();
```

**`distinct()`** — **stateful**. Mantém um conjunto interno dos elementos já vistos e descarta duplicatas. Usa `equals`/`hashCode` do elemento. Atenção: em streams não-ordenados a escolha de qual duplicata manter não é garantida.

**`sorted()`** / **`sorted(Comparator<T>)`** — **stateful, potencialmente caro**. Precisa acumular todos os elementos na memória antes de emitir o primeiro resultado ordenado. Em streams grandes, essa é a operação que mais impacta memória.

- `sorted()` sem argumento usa a ordem natural — o tipo `T` precisa implementar `Comparable<T>`, caso contrário lança `ClassCastException` em tempo de execução (ver Armadilhas).
- `sorted(Comparator.comparing(...))` define ordem explícita sem depender de `Comparable`.

**`limit(long n)`** — **stateful, short-circuit**. Trunca o stream após `n` elementos. Essencial para streams infinitos.

**`skip(long n)`** — **stateful**. Descarta os primeiros `n` elementos e emite o restante.

**`takeWhile(Predicate<T>)`** *(Java 9)* — emite elementos enquanto o predicado for `true` e para imediatamente quando falhar. Pré-condição: faz mais sentido com fontes ordenadas.

```java
// Assumindo stream de valores crescentes: 1, 2, 3, 10, 4, 5
// Para no 10 (predicado falha), NÃO retoma em 4 e 5
List<Integer> prefixo = Stream.of(1, 2, 3, 10, 4, 5)
    .takeWhile(n -> n < 10)
    .toList(); // [1, 2, 3]
```

**`dropWhile(Predicate<T>)`** *(Java 9)* — descarta elementos enquanto o predicado for `true` e emite todos os restantes a partir do primeiro elemento que falhe.

```java
List<Integer> sufixo = Stream.of(1, 2, 3, 10, 4, 5)
    .dropWhile(n -> n < 10)
    .toList(); // [10, 4, 5]
```

`takeWhile`/`dropWhile` são complementares a `limit`/`skip`: enquanto `limit`/`skip` trabalham com contagem, `takeWhile`/`dropWhile` trabalham com condição.

**`peek(Consumer<T>)`** — **stateless**. Executa uma ação em cada elemento *sem modificar o stream*. Projetado para **debug e inspeção apenas** — não para efeitos colaterais de negócio (ver Armadilhas).

---

### Terminais de coleta/redução (`toList`/`collect`/`reduce`/`count`/`min`/`max`)

Essas operações consomem o stream e produzem um valor concreto ou estrutura de dados.

**`toList()`** *(Java 16)* — retorna uma `List<T>` **imutável** com os elementos na ordem de encontro. Semelhante a `collect(Collectors.toUnmodifiableList())`, mas mais conciso e com uma diferença importante: `toList()` **aceita elementos `null`**, enquanto `toUnmodifiableList()` os rejeita com `NullPointerException`. Tentar adicionar/remover elementos depois lança `UnsupportedOperationException`.

```java
List<String> nomes = orders.stream()
    .map(Order::getCustomerName)
    .toList(); // imutável — não chamar .add() depois
```

**`collect(Collector<T, A, R>)`** — redução mutável genérica. O `Collector` encapsula três funções: supplier (cria o contêiner), accumulator (adiciona elemento) e combiner (mescla dois contêineres em paralelo). Veja [[08 - Collectors e agrupamento]] para o catálogo completo de `Collectors`.

```java
// Versão mutável (pode ser modificada depois)
List<String> mutavel = orders.stream()
    .map(Order::getCustomerName)
    .collect(Collectors.toList());

// Agrupamento
Map<String, List<Order>> porCliente = orders.stream()
    .collect(Collectors.groupingBy(Order::getCustomerName));
```

**`reduce(T identity, BinaryOperator<T>)`** — redução por acumulação usando um valor identidade. Retorna `T` diretamente (nunca `Optional`, pois a identidade garante resultado mesmo com stream vazio).

```java
// Soma dos totais de pedido
double totalGeral = orders.stream()
    .mapToDouble(Order::getTotal)
    .reduce(0.0, Double::sum);
```

A variante `reduce(BinaryOperator<T>)` sem identidade retorna `Optional<T>` — correto quando o stream pode estar vazio.

**`count()`** — retorna o número de elementos como `long`. Pode ser otimizado pela JVM para fontes com tamanho conhecido (ex.: `ArrayList`) sem traversal completo.

**`min(Comparator<T>)`** / **`max(Comparator<T>)`** — retornam `Optional<T>`. Retornam `Optional.empty()` se o stream estiver vazio.

```java
Optional<Order> maiorPedido = orders.stream()
    .max(Comparator.comparingDouble(Order::getTotal));

maiorPedido.ifPresent(o ->
    System.out.println("Maior: " + o.getId() + " = " + o.getTotal()));
```

---

### Terminais de busca/match — curto-circuito (`findFirst`/`findAny`/`anyMatch`/`allMatch`/`noneMatch`)

Estas operações podem retornar antes de processar todo o stream — elas **param assim que a resposta é determinada**. São as operações que tornam streams potencialmente infinitos utilizáveis.

**`findFirst()`** — retorna `Optional<T>` com o primeiro elemento na ordem de encontro (encounter order). Em streams não-ordenados, retorna qualquer elemento com garantia de ser consistente entre execuções sequenciais.

**`findAny()`** — retorna `Optional<T>` com qualquer elemento, sem garantia de qual. Em streams sequenciais, tende a retornar o primeiro, mas a especificação não garante isso. Em streams paralelos, pode retornar qualquer elemento de qualquer partição — mais eficiente que `findFirst` em paralelo porque não precisa sincronizar para manter a ordem.

```java
// Primeiro pedido ativo acima de R$ 500 — para na primeira ocorrência
Optional<Order> candidato = orders.stream()
    .filter(o -> o.isActive() && o.getTotal() > 500.0)
    .findFirst();
```

**`anyMatch(Predicate<T>)`** — retorna `true` assim que encontra o primeiro elemento que satisfaz o predicado; retorna `false` se nenhum satisfizer.

**`allMatch(Predicate<T>)`** — retorna `false` assim que encontra o primeiro elemento que **não** satisfaz o predicado; retorna `true` se todos satisfizerem (incluindo stream vazio, por vacuidade).

**`noneMatch(Predicate<T>)`** — retorna `false` assim que encontra o primeiro elemento que satisfaz o predicado; retorna `true` se nenhum satisfizer (incluindo stream vazio).

```java
boolean todosAtivos   = orders.stream().allMatch(Order::isActive);
boolean algumAtrasado = orders.stream().anyMatch(Order::isLate);
boolean semCancelados = orders.stream().noneMatch(Order::isCancelled);
```

A tabela de comportamento com stream vazio é importante para entrevistas:

| Operação | Stream vazio retorna |
|----------|---------------------|
| `anyMatch(p)` | `false` |
| `allMatch(p)` | `true` (vacuamente verdadeiro) |
| `noneMatch(p)` | `true` |
| `findFirst()` | `Optional.empty()` |
| `findAny()` | `Optional.empty()` |

---

### Terminais de iteração (`forEach`/`forEachOrdered`)

**`forEach(Consumer<T>)`** — executa uma ação para cada elemento. A **ordem de processamento não é garantida** em streams não-ordenados ou paralelos. Para streams sequenciais com fonte ordenada (ex.: `List`), na prática processa em ordem, mas a especificação não garante.

**`forEachOrdered(Consumer<T>)`** — garante que a ação é executada na **ordem de encontro (encounter order)**, mesmo em streams paralelos. Em paralelo, isso implica sincronização adicional — use apenas quando a ordem é realmente necessária.

```java
// forEach — aceitável para efeitos de saída em stream sequencial
orders.stream()
    .filter(Order::isActive)
    .forEach(o -> System.out.println(o.getId()));

// forEachOrdered — quando a ordem importa (ex.: logging ordenado em paralelo)
orders.parallelStream()
    .filter(Order::isActive)
    .forEachOrdered(o -> System.out.println(o.getId())); // mais lento, mas ordenado
```

Diferença chave: prefira `collect` sobre `forEach` quando o objetivo é acumular elementos (ver Armadilhas).

## Na prática

Pipeline completo típico em código de produção — filtragem, transformação, ordenação, paginação e materialização:

```java
// orders: List<Order>
// Objetivo: top 5 pedidos mais valiosos ativos, retornar apenas o ID e total

record OrderSummary(String id, double total) {}

List<OrderSummary> top5 = orders.stream()
    .filter(Order::isActive)                                        // filtra inativos
    .sorted(Comparator.comparingDouble(Order::getTotal).reversed()) // ordena desc
    .limit(5)                                                       // pega os 5 primeiros
    .map(o -> new OrderSummary(o.getId(), o.getTotal()))            // projeta
    .toList();                                                      // materializa imutável
```

Observe a ordem das operações: `filter` antes de `sorted` reduz o custo do sort (menos elementos para ordenar). `limit` antes de `map` reduz o custo da projeção. Essa ordenação deliberada é um critério de qualidade em code review.

`flatMap` achatando `List<Order>` para seus itens individuais:

```java
// orders: List<Order>, cada Order tem List<String> items
// Objetivo: lista de todos os itens distintos, ordenados alfabeticamente

List<String> catalogoItens = orders.stream()
    .filter(Order::isActive)
    .flatMap(order -> order.getItems().stream())  // achata List<List<String>> → List<String>
    .distinct()                                   // remove duplicatas
    .sorted()                                     // ordena alfabeticamente
    .toList();
```

Comparação `flatMap` vs `mapMulti` para o mesmo resultado:

```java
// flatMap — idiomático, cria Stream por elemento
List<String> itensA = orders.stream()
    .flatMap(o -> o.getItems().stream())
    .toList();

// mapMulti (Java 16) — evita Stream intermediário, bom quando há filtragem inline
List<String> itensB = orders.<String>mapMulti((order, consumer) -> {
    if (order.isActive()) {
        order.getItems().forEach(consumer);
    }
}).toList();
```

## Armadilhas

### (1) Usar `peek` como mecanismo de efeito de negócio

**O problema:** `peek` é uma operação intermediária projetada para inspeção/debug. A especificação diz explicitamente que o comportamento de `peek` pode ser suprimido pelo runtime quando a otimização detectar que não é necessário visitar todos os elementos (ex.: com `limit` ou `findFirst` antes). Em paralelo, a ordem e o número de invocações não são garantidos.

```java
// ERRADO — usar peek para salvar pedidos no banco
orders.stream()
    .filter(Order::isActive)
    .peek(orderService::save)  // pode não executar para todos; não garantido em otimizações
    .map(Order::getId)
    .findFirst();

// CORRETO — lógica de negócio vai em map (se há transformação) ou forEach (terminal)
orders.stream()
    .filter(Order::isActive)
    .map(o -> { orderService.save(o); return o.getId(); }) // map com efeito explícito
    .findFirst();

// Melhor ainda: separar efeito da transformação
orders.stream()
    .filter(Order::isActive)
    .forEach(orderService::save);   // terminal dedicado a efeitos
```

`peek` deve ser reservado exclusivamente para `System.out.println` / logging em debug de pipelines.

---

### (2) `sorted()` sem `Comparator` em tipo não-`Comparable`

**O problema:** `sorted()` sem argumento invoca a ordem natural, que exige que `T` implemente `Comparable<T>`. Se o tipo não implementar, a exceção só aparece **em tempo de execução** ao executar o terminal — não há erro de compilação.

```java
// Order NÃO implementa Comparable<Order>

// ERRADO — compila, mas lança ClassCastException em runtime
List<Order> ordenados = orders.stream()
    .sorted()    // tenta Order.compareTo() — Order não tem, ClassCastException!
    .toList();
// java.lang.ClassCastException: class Order cannot be cast to class java.lang.Comparable

// CORRETO — Comparator explícito
List<Order> ordenados = orders.stream()
    .sorted(Comparator.comparing(Order::getCreatedAt))
    .toList();

// CORRETO — Comparator composto para desempate
List<Order> ordenados = orders.stream()
    .sorted(Comparator.comparing(Order::getCustomerName)
                      .thenComparingDouble(Order::getTotal))
    .toList();
```

Regra prática: use `sorted(Comparator)` sempre que o tipo não for `String`, `Integer`, `Long` ou outro primitivo boxeado — todos esses já implementam `Comparable`.

---

### (3) `forEach` mutando coleção externa (quebra em paralelo → usar `collect`)

**O problema:** acumular resultados de stream em uma coleção mutable via `forEach` parece funcionar em streams sequenciais, mas é uma violação da especificação de não-interferência. Em streams paralelos, múltiplas threads chamam `add()` simultaneamente em uma `ArrayList` (não-thread-safe), causando perda de dados, duplicatas ou `ArrayIndexOutOfBoundsException` — sem erro de compilação.

```java
// ERRADO — ArrayList não é thread-safe; em paralelo, resultados são corrompidos
List<String> resultado = new ArrayList<>();
orders.parallelStream()
    .filter(Order::isActive)
    .map(Order::getCustomerName)
    .forEach(resultado::add);  // race condition — List corrompida
// Mesmo em stream sequencial: viola a especificação de non-interference

// CORRETO — collect() gerencia a thread-safety internamente
List<String> resultado = orders.parallelStream()
    .filter(Order::isActive)
    .map(Order::getCustomerName)
    .collect(Collectors.toList());

// CORRETO — toList() (Java 16+) também é seguro
List<String> resultado = orders.stream()
    .filter(Order::isActive)
    .map(Order::getCustomerName)
    .toList();
```

A regra é simples: se o objetivo é produzir uma coleção, use `collect` ou `toList()`. `forEach` existe para efeitos finais (imprimir, persistir, notificar) — não para acumulação.

## Em entrevista

### Frase pronta (inglês)

> "Stream operations fall into two categories: intermediate operations, which are lazy and return a new stream without executing anything, and terminal operations, which are eager and trigger the actual traversal of the pipeline. This lazy evaluation is what enables optimizations like loop fusion — where `filter` and `map` are fused into a single pass over the data — and short-circuit evaluation, where operations like `findFirst` or `anyMatch` stop processing as soon as the answer is determined."
>
> "Within intermediate operations there's a further distinction between stateless operations, like `filter` and `map`, which process each element independently and are highly parallelizable, versus stateful operations like `sorted`, `distinct`, and `limit`, which need to buffer or track state across multiple elements. `sorted` in particular must buffer the entire stream before emitting the first element, which is why it's the most expensive intermediate operation in terms of memory."
>
> "Java 9 added `takeWhile` and `dropWhile` for prefix-based slicing based on a predicate rather than a count, and Java 16 added `mapMulti` as a more efficient alternative to `flatMap` for cases where you're generating zero or one element per input, and `toList()` as a concise way to get an unmodifiable list — which is preferable to `collect(Collectors.toList())` for read-only results because it makes the immutability intent explicit."

### Vocabulário

| Termo PT | Termo EN |
|----------|----------|
| operação intermediária | intermediate operation |
| operação terminal | terminal operation |
| avaliação preguiçosa | lazy evaluation |
| avaliação ansiosa | eager evaluation |
| curto-circuito | short-circuit |
| operação com estado | stateful operation |
| operação sem estado | stateless operation |
| achatar / nivelar | flatten |
| redução | reduction |
| redução mutável | mutable reduction |
| ordem de encontro | encounter order |
| não-interferência | non-interference |

## Veja também

- [[05 - Introdução à Stream API]]
- [[08 - Collectors e agrupamento]]
- [[09 - Streams primitivos]]
- [[03-Dominios/Tecnologia/Java/Collections e Streams/index|Collections e Streams (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/15 - Parallel streams e fork-join|Parallel streams]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#operação intermediária / terminal|operação intermediária / terminal]]

## Referências

- [Stream — Java SE 21 API Docs (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/stream/Stream.html)
- [java.util.stream — Package Summary, Java SE 21 API Docs (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/stream/package-summary.html)
- [Aggregate Operations — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/collections/streams/index.html)
- [Parallelism — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/collections/streams/parallelism.html)
