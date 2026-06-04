---
title: "Introdução à Stream API"
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
  - streams
aliases:
  - Stream API
  - Stream
  - Pipeline
---

# Introdução à Stream API

> [!abstract] TL;DR
> Um **Stream** é uma sequência de elementos que transporta valores de uma fonte através de um pipeline de operações — **não é uma estrutura de dados e não armazena nada**. O pipeline tem três partes: uma fonte (coleção, array, gerador), zero ou mais **operações intermediárias** (lazy — não executam até que haja uma terminal) e exatamente uma **operação terminal** (eager — dispara toda a execução). Uma vez consumido, o stream não pode ser reutilizado. O estilo é declarativo: você descreve *o quê* quer, não *como* iterar.

## O que é

A Stream API foi introduzida no Java 8 (pacote `java.util.stream`) e fornece um modelo de processamento funcional de sequências de dados. Na definição formal do Javadoc:

> "A stream is not a data structure that stores elements; instead, it conveys elements from a source such as a data structure, an array, a generator function, or an I/O channel, through a pipeline of computational operations."

Quatro propriedades essenciais, direto da especificação:

| Propriedade | O que significa |
|-------------|-----------------|
| **Sem armazenamento** | Um stream não guarda dados; ele conduz elementos da fonte para o resultado |
| **Funcional** | As operações não modificam a coleção original |
| **Lazy-seeking** | Operações intermediárias são adiadas até a terminal ser chamada |
| **Consumível uma vez** | Após a terminal, o stream está encerrado — não pode ser reusado |

A distinção mais importante para entrevistas: **Collection armazena, Stream processa**.

## Por que importa

O estilo imperativo de processar dados via `for`/`while` mistura *o que fazer* com *como iterar*. A Stream API separa essas preocupações e permite escrever pipelines declarativos que são mais legíveis e compossíveis.

Exemplos da diferença de estilo:

```java
// Imperativo — iterar explicitamente, acumular manualmente
List<String> nomes = new ArrayList<>();
for (Order order : orders) {
    if (order.isActive()) {
        nomes.add(order.getCustomerName());
    }
}

// Declarativo com Stream — descreve a intenção
List<String> nomes = orders.stream()
    .filter(Order::isActive)
    .map(Order::getCustomerName)
    .toList();
```

Por que cai em entrevista: recrutadores de posições sênior cobram a diferença entre **lazy e eager**, a razão pela qual uma stream intermediária não executa sozinha, e quando preferir loop sobre stream. Entender o modelo de execução — não apenas a sintaxe — é o que diferencia as respostas.

## Como funciona

### Anatomia: source → intermediárias (lazy) → terminal (eager)

Todo pipeline tem exatamente três partes:

```text
Source                     Intermediárias (lazy)          Terminal (eager)
───────────────────        ──────────────────────────     ─────────────────
orders.stream()     →     .filter(Order::isActive)   →   .toList()
List, Array, File         .map(Order::getTotal)
Generator, I/O            .sorted(...)
                          .limit(10)
                          (nenhuma executa ainda)          ← execução começa aqui
```

- **Source (fonte):** qualquer `Collection`, array, `Stream.of(...)`, `Stream.generate(...)`, `Files.lines(...)`, entre outros.
- **Operações intermediárias:** `filter`, `map`, `flatMap`, `distinct`, `sorted`, `limit`, `skip`, `peek`, `takeWhile`, `dropWhile`. Retornam um novo `Stream` — por isso podem ser encadeadas. São sempre **lazy**.
- **Operação terminal:** `toList()`, `collect(...)`, `forEach`, `count`, `reduce`, `findFirst`, `anyMatch`, `min`, `max`. Produz um resultado ou efeito — sempre **eager** (com raras exceções como `iterator()` e `spliterator()`).

### Avaliação preguiçosa e curto-circuito (nada roda até a terminal)

O Javadoc é preciso:

> "Intermediate operations are always lazy; executing an intermediate operation such as `filter()` does not actually perform any filtering, but instead creates a new stream that, when traversed, contains the elements of the initial stream that match the given predicate."

Isso tem consequências importantes:

```java
// Nenhuma das linhas abaixo executa filter ou map ainda
Stream<String> pipeline = orders.stream()
    .filter(o -> {
        System.out.println("filtrando: " + o.getId()); // não imprime nada
        return o.isActive();
    })
    .map(Order::getCustomerName);

// Somente aqui o pipeline é percorrido
List<String> resultado = pipeline.toList(); // agora as mensagens aparecem
```

**Curto-circuito (short-circuit):** certas operações terminais — `findFirst()`, `findAny()`, `anyMatch()`, `noneMatch()`, `allMatch()` — podem encerrar o pipeline antes de processar todos os elementos. Da mesma forma, a intermediária `limit(n)` é short-circuit: para de pedir elementos à fonte após `n`. Isso é indispensável para trabalhar com streams potencialmente infinitos (`Stream.generate(...)`, `Stream.iterate(...)`).

```java
// Para na primeira ordem acima de R$ 1000 — não percorre a lista inteira
Optional<Order> cara = orders.stream()
    .filter(o -> o.getTotal() > 1000.0)
    .findFirst();
```

### Stream vs Collection (processamento vs armazenamento)

| Aspecto | Collection | Stream |
|---------|-----------|--------|
| Armazena dados | Sim, na memória | Não — conduz da fonte |
| Modificação da fonte | Operações alteram a coleção | Operações não alteram a fonte |
| Avaliação | Eager (add, remove imediatos) | Intermediárias lazy, terminal eager |
| Reutilização | Ilimitada | Consumível uma vez |
| Tamanho | Sempre finito | Pode ser infinito (`Stream.generate`) |
| Iteração | Interna ou externa | Sempre interna (declarativa) |

### Stream vs loop (quando cada um)

Prefira **Stream** quando:
- A lógica é uma sequência de filter/map/collect sem estado acumulado complexo.
- Legibilidade e composição importam mais que performance de microbenchmark.
- Você quer usar referências de método e programação funcional.

Prefira **loop** quando:
- O processamento tem múltiplas saídas (break em condição externa, múltiplas listas acumuladas).
- Há estado mutável local complexo entre iterações.
- Performance de baixíssima latência é crítica (tight loop com muitos elementos primitivos — use streams primitivos nesse caso, ver [[09 - Streams primitivos]]).

### Stream é consumível uma vez

Após a operação terminal, o stream está encerrado. Tentar usá-lo novamente lança `IllegalStateException`. Da especificação:

> "The elements of a stream are only visited once during the life of a stream. Like an Iterator, a new stream must be generated to revisit the same elements of the source."

```java
Stream<Order> stream = orders.stream().filter(Order::isActive);
long count = stream.count();         // terminal — stream encerrado
List<Order> lista = stream.toList(); // IllegalStateException!

// Solução: obter um novo stream a partir da fonte
List<Order> lista = orders.stream().filter(Order::isActive).toList();
```

> [!note] Paralelismo
> A Stream API suporta processamento paralelo via `parallelStream()` ou `.parallel()`. Internamente, isso usa o `ForkJoinPool.commonPool()`. A decisão de quando paralelizar, o impacto no common pool compartilhado e as armadilhas de estado mutável em paralelo são cobertos em profundidade em [[03-Dominios/Java/Concorrência e paralelismo/15 - Parallel streams e fork-join|Parallel streams e fork/join]] — este galho não repete esse conteúdo.

## Na prática

Um pipeline típico em código de produção:

```java
// orders: List<Order>
// Objetivo: nomes dos clientes de pedidos ativos acima de R$ 500, ordenados

List<String> resultado = orders.stream()           // source
    .filter(Order::isActive)                       // intermediária — lazy
    .filter(o -> o.getTotal() > 500.0)             // intermediária — lazy
    .map(Order::getCustomerName)                   // intermediária — lazy
    .sorted()                                      // intermediária — lazy (stateful)
    .toList();                                     // terminal — eager, dispara tudo
```

Observe que sem a chamada `.toList()` no final, nenhum `filter` ou `map` executa. Isso também significa que pipelines intermediários podem ser construídos e passados como valores antes de serem materializados:

```java
// Compondo pipelines reutilizáveis (a partir de uma nova stream a cada uso)
// Não reutilize o objeto Stream — construa a cadeia a partir da coleção
Stream<Order> ativos = orders.stream().filter(Order::isActive);
// ativos ainda não executou nada

long total = ativos.count(); // agora executa
// ativos está consumido — para reutilizar, crie outro: orders.stream().filter(...)
```

Outro padrão comum — agrupamento com `Collectors`:

```java
// Agrupa pedidos ativos por cliente
Map<String, List<Order>> porCliente = orders.stream()
    .filter(Order::isActive)
    .collect(Collectors.groupingBy(Order::getCustomerName));
```

Veja [[08 - Collectors e agrupamento]] para o universo completo de `Collectors`.

## Armadilhas

### (1) Reusar stream já consumido (`IllegalStateException`)

**O problema:** armazenar um `Stream` em variável e chamar uma segunda operação terminal nele.

```java
// ERRADO
Stream<Order> stream = orders.stream()
    .filter(o -> o.getTotal() > 100.0);

long quantidade = stream.count();   // primeira terminal — OK
List<Order> lista = stream.toList(); // IllegalStateException: stream has already been operated upon or closed
```

**Fix:** nunca reutilize a mesma instância de `Stream`. Sempre obtenha um novo stream a partir da coleção (que é reutilizável) quando precisar executar duas operações:

```java
// CORRETO — dois streams separados a partir da mesma fonte
long quantidade = orders.stream().filter(o -> o.getTotal() > 100.0).count();
List<Order> lista = orders.stream().filter(o -> o.getTotal() > 100.0).toList();
```

Se a filtragem for cara, considere materializar para uma lista intermediária antes:

```java
List<Order> filtrados = orders.stream()
    .filter(o -> o.getTotal() > 100.0)
    .toList(); // materializa uma vez

long quantidade = filtrados.size();
String primeiro = filtrados.get(0).getCustomerName();
```

---

### (2) Achar que operações intermediárias executam sozinhas

**O problema:** chamar `.filter(...)` ou `.map(...)` e esperar que o efeito já tenha ocorrido — não há terminal no pipeline.

```java
// ERRADO — nada acontece; nenhuma linha de log é impressa
orders.stream()
    .filter(Order::isActive)
    .map(o -> {
        System.out.println("Processando: " + o.getId()); // nunca executa
        return o.getCustomerName();
    });
// Resultado esperado pelo dev: logs apareceram. Resultado real: silêncio.
```

**Fix:** sempre encerre o pipeline com uma operação terminal:

```java
// CORRETO — terminal presente, pipeline executa
List<String> nomes = orders.stream()
    .filter(Order::isActive)
    .map(o -> {
        System.out.println("Processando: " + o.getId()); // executa agora
        return o.getCustomerName();
    })
    .toList();
```

> [!tip] Regra prática
> Se você escreve `stream.filter(...).map(...)` e não vê um `.toList()`, `.collect(...)`, `.forEach(...)` ou outra terminal no final, é quase certo que há um bug de pipeline incompleto.

---

### (3) Efeito colateral em `map` ou `peek`

**O problema:** usar `map` ou `peek` para modificar estado externo (acumular em lista, incrementar contador, persistir em banco). Além de violar o princípio de não-interferência da especificação, isso torna o código frágil ao paralelismo e dificulta raciocinar sobre a ordem de execução.

```java
// ERRADO — acumulando em lista externa via map (efeito colateral)
List<String> nomes = new ArrayList<>();
orders.stream()
    .filter(Order::isActive)
    .map(o -> {
        nomes.add(o.getCustomerName()); // efeito colateral — quebra em paralelo
        return o.getCustomerName();
    })
    .count();

// ERRADO — peek para "fazer coisas" além de debug
orders.stream()
    .filter(Order::isActive)
    .peek(o -> salvarNoBanco(o)) // peek é para debug/inspeção; não para side effects de negócio
    .toList();
```

**Fix:** use operações terminais adequadas para efeitos e produza resultados via `collect` ou `reduce`:

```java
// CORRETO — collect para acumular
List<String> nomes = orders.stream()
    .filter(Order::isActive)
    .map(Order::getCustomerName)
    .collect(Collectors.toList());

// CORRETO — forEach para efeitos colaterais explícitos (em stream sequencial)
orders.stream()
    .filter(Order::isActive)
    .forEach(o -> salvarNoBanco(o));
```

> [!warning] `peek` em produção
> `peek` é uma operação intermediária que só deve ser usada para **inspeção/debug** (imprimir valores intermediários). Não faça persistência, notificações ou mutação de estado dentro de `peek` — o comportamento pode mudar com otimizações do compilador JIT ou com paralelismo.

## Em entrevista

### Frase pronta (inglês)

> "A Stream in Java is a sequence of elements that carries values from a source through a pipeline of computational operations — it is explicitly not a data structure and does not store elements. The pipeline is composed of a source, zero or more intermediate operations which are lazy by definition, and exactly one terminal operation which is eager and triggers the actual execution of the entire pipeline."
>
> "The lazy nature of intermediate operations means that calling `filter()` or `map()` on a stream doesn't process anything — it just describes the pipeline. Nothing runs until a terminal operation like `toList()`, `collect()`, or `forEach()` is invoked. This enables optimizations like short-circuiting: `findFirst()` can stop after the first match without traversing the whole source."
>
> "Streams are single-use: once a terminal operation is called, the stream is consumed and cannot be reused — attempting to do so throws `IllegalStateException`. The source collection, on the other hand, is not affected and a new stream can always be obtained from it. For parallel execution, `parallelStream()` or `.parallel()` distribute the work across the `ForkJoinPool.commonPool()`, but this introduces its own trade-offs around shared state, I/O blocking and overhead on small datasets."

### Vocabulário

| Termo PT | Termo EN |
|----------|----------|
| sequência de elementos | sequence of elements |
| pipeline de operações | operation pipeline |
| operação intermediária | intermediate operation |
| operação terminal | terminal operation |
| avaliação preguiçosa | lazy evaluation |
| curto-circuito | short-circuit |
| consumível uma vez | single-use / consumed once |
| não interfere na fonte | non-interference |
| fonte do stream | stream source |
| coletor | collector |
| stream primitivo | primitive stream (`IntStream`, `LongStream`, `DoubleStream`) |
| stream paralelo | parallel stream |

## Veja também

- [[04 - Lambdas e interfaces funcionais]]
- [[07 - Operações de Stream — intermediárias e terminais]]
- [[08 - Collectors e agrupamento]]
- [[09 - Streams primitivos]]
- [[03-Dominios/Java/Collections e Streams/index|Collections e Streams (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Concorrência e paralelismo/15 - Parallel streams e fork-join|Parallel streams]]
- [[03-Dominios/Java/Dicionário de Java#Stream|Stream]]
- [[03-Dominios/Java/Dicionário de Java#operação intermediária / terminal|operação intermediária / terminal]]
- [[03-Dominios/Java/Dicionário de Java#stream lazy (avaliação preguiçosa)|stream lazy]]

## Referências

- [Aggregate Operations — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/collections/streams/index.html)
- [java.util.stream — Package Summary, Java SE 21 API Docs (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/stream/package-summary.html)
