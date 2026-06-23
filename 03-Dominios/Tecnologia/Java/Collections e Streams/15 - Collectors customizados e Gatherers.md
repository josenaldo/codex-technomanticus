---
title: "Collectors customizados e Gatherers"
created: 2026-06-04
updated: 2026-06-04
type: concept
progress: backlog
status: seedling
publish: true
fase: magus
tags:
  - java
  - collections
  - magus
  - streams
  - gatherers
  - collectors
aliases:
  - Stream Gatherers
  - Collector.of
  - JEP 485
---

# Collectors customizados e Gatherers

> [!abstract] TL;DR
> Há **duas formas de estender a pipeline de stream** além dos coletores prontos de `Collectors`. (1) `Collector.of(supplier, accumulator, combiner, finisher, characteristics...)` constrói uma **operação terminal sob medida** — você descreve como criar o contêiner mutável, como acumular cada elemento, como mesclar dois contêineres em paralelo e como produzir o resultado final. (2) **Stream Gatherers** (`Stream.gather(Gatherer)`, finalizado no **Java 24** pela **JEP 485**) trazem o que faltava: **operações intermediárias customizadas**. Antes deles, janela deslizante, *scan* (prefix sum), *fold* ordenado e mapeamento concorrente eram impossíveis sem sair do stream. Um `Gatherer<T, A, R>` é especificado por quatro funções — *initializer*, *integrator*, *combiner* e *finisher* — e a classe `Gatherers` já entrega fábricas prontas: `windowFixed`, `windowSliding`, `fold`, `scan` e `mapConcurrent`. A regra de ouro em ambos os casos: o **combiner** define se a operação é paralelizável — combiner errado corrompe em paralelo, silenciosamente.

## O que é

Os coletores prontos de [[08 - Collectors e agrupamento|Collectors]] cobrem o grosso do dia a dia, mas eventualmente você precisa de uma redução ou de uma transformação que a biblioteca não oferece. Existem **duas portas de extensão**, em dois pontos diferentes da pipeline:

1. **`Collector.of(...)`** — fabrica um **coletor terminal sob medida**. Um `Collector<T, A, R>` continua sendo aquilo descrito em [[08 - Collectors e agrupamento|Collectors e agrupamento]]: uma receita de redução mutável (acumula elementos `T` em um contêiner mutável `A` e produz `R`). A diferença é que aqui *você* fornece as quatro funções da receita em vez de combinar coletores prontos. É a operação **terminal** — roda no `collect`.

2. **Stream Gatherers** (`Stream.gather(Gatherer)`) — adicionam **operações intermediárias customizadas**. Um `Gatherer<T, A, R>` é, nas palavras da própria API, "*an intermediate operation that transforms a stream of input elements into a stream of output elements, optionally applying a final action when the end of the upstream is reached*". Diferente de um `Collector`, que encerra o stream, um `Gatherer` continua a pipeline — sua saída ainda é um `Stream<R>` em que você pode encadear `map`, `filter`, `collect`. Finalizado no **Java 24** pela **JEP 485**.

```java
// Collector.of: operação TERMINAL sob medida — encerra o stream em um R
R resultado = stream.collect(meuCollector);

// Stream.gather: operação INTERMEDIÁRIA sob medida — o stream continua
Stream<R> aindaStream = stream.gather(meuGatherer).filter(...);
```

A simetria conceitual é elegante: `Collector` é à operação terminal `collect` o que `Gatherer` é à (nova) operação intermediária `gather`. Ambos são *especificações* — quatro funções cada — e ambos delegam a execução à própria Stream API.

## Por que importa

`Collectors` resolve **reduções**, mas sempre no fim da pipeline. O buraco histórico da Stream API estava nas **operações intermediárias com estado e dependentes de ordem**: a biblioteca oferecia `map`, `filter`, `distinct`, `sorted`, `limit` — e parava aí. Não havia como expressar, *dentro* do stream:

- **Janela deslizante** — agrupar cada 3 elementos consecutivos sobrepostos (médias móveis, detecção de padrões em séries).
- **Scan / prefix sum** — emitir o acumulado parcial a cada passo (saldo corrente, soma acumulada).
- **Fold ordenado** — uma redução que depende estritamente da ordem e não tem combiner possível.
- **Map concorrente com ordem preservada** — disparar N chamadas a um serviço em paralelo, mantendo a ordem de saída.

Antes dos Gatherers, a única saída era **abandonar o stream**: coletar numa lista, escrever um laço imperativo com índices, e talvez voltar para um stream depois. Isso quebra a fluência e reintroduz o boilerplate que a Stream API existia para eliminar. Gatherers fecham essa lacuna — são para as **intermediárias** o que `Collectors` é para as **terminais**.

Em entrevista, este é o tópico de stream que mais soa **"Java moderno"**. Demonstra que você acompanhou a evolução da linguagem (preview no Java 22/23, final no 24), entende a anatomia de um `Collector` por dentro (não só decora `toList()`), e sabe quando *não* reinventar o que já existe. É um diferencial sênior claro.

## Como funciona

### `Collector.of` (supplier/accumulator/combiner/finisher/characteristics)

Quando os coletores de `Collectors` não combinam para o que você precisa, `Collector.of(...)` constrói um do zero a partir de quatro funções (mais características opcionais):

- **`supplier`** (`Supplier<A>`) — cria um novo contêiner mutável `A` vazio. Chamado uma vez por partição.
- **`accumulator`** (`BiConsumer<A, T>`) — incorpora um elemento `T` ao contêiner `A`, **mutando-o in-place**.
- **`combiner`** (`BinaryOperator<A>`) — funde dois contêineres parciais em um. **Só é chamado em execução paralela**, para juntar os resultados das partições.
- **`finisher`** (`Function<A, R>`) — transforma o contêiner final `A` no resultado `R`. Quando `A` e `R` são o mesmo tipo, existe a sobrecarga de três argumentos (sem finisher) — internamente um finisher identidade.
- **`characteristics`** (`Collector.Characteristics...`) — dicas opcionais: `UNORDERED` (a ordem de encontro não importa), `CONCURRENT` (o accumulator pode ser chamado concorrentemente no mesmo contêiner) e `IDENTITY_FINISH` (o finisher é a identidade, pode ser pulado).

```java
// Coletor manual equivalente a um joining(", ", "[", "]") — para ilustrar a anatomia
Collector<String, StringJoiner, String> meuJoining = Collector.of(
    () -> new StringJoiner(", ", "[", "]"),  // supplier: contêiner mutável
    StringJoiner::add,                        // accumulator: muta in-place
    StringJoiner::merge,                      // combiner: funde dois (paralelo)
    StringJoiner::toString);                  // finisher: A (StringJoiner) -> R (String)
```

Assinaturas:

```java
static <T,R> Collector<T,R,R> of(Supplier<R> supplier,
                                 BiConsumer<R,T> accumulator,
                                 BinaryOperator<R> combiner,
                                 Characteristics... characteristics)

static <T,A,R> Collector<T,A,R> of(Supplier<A> supplier,
                                   BiConsumer<A,T> accumulator,
                                   BinaryOperator<A> combiner,
                                   Function<A,R> finisher,
                                   Characteristics... characteristics)
```

> [!note] O `combiner` é o coração do paralelismo
> Em stream **sequencial**, o `combiner` nunca é invocado — há um só contêiner. Ele só entra em ação quando o stream é **paralelo** e cada partição produziu seu contêiner parcial. Por isso um combiner errado passa despercebido em testes sequenciais e só explode (ou produz lixo) em paralelo. Veja as Armadilhas.

### Quando escrever um collector próprio vs combinar os de `Collectors`

A regra prática: **comece sempre tentando compor coletores prontos**. `groupingBy` + downstream (`mapping`, `collectingAndThen`, `teeing`, `reducing`) resolve a esmagadora maioria dos casos sem uma linha de `Collector.of`.

Escreva um coletor próprio só quando:

- O **contêiner de acumulação** é incomum (um `StringJoiner`, um `BitSet`, um *builder* de domínio, uma estrutura de terceiros).
- Você precisa de **características específicas** (`CONCURRENT`/`UNORDERED`) para performance, que os coletores compostos não dão.
- A lógica de acumulação **não se expressa** como combinação dos coletores existentes.

Na dúvida, o `collectingAndThen(coletorComposto, finisher)` costuma cobrir o que parecia exigir um coletor manual. Reservar `Collector.of` para o que realmente não compõe mantém o código legível.

### **Stream Gatherers** (`Gatherer`, `Stream.gather`) — o que são e por que existem

Um **`Gatherer<T, A, R>`** é uma operação **intermediária** definida por você. Onde um `Collector` reduz `T → R` no fim da pipeline, um `Gatherer` transforma um fluxo de `T` em um fluxo de `R` **no meio** da pipeline, podendo manter estado e bufferizar elementos antes de emitir. A operação que o consome é `Stream.gather(Gatherer)`, e o resultado é de novo um `Stream` — a pipeline continua.

Um `Gatherer` é especificado por **quatro funções** (paralelas, mas não idênticas, às do `Collector`):

- **`initializer`** — "*a function that produces an instance of the intermediate state used for this gathering operation*". O estado privado `A` do gatherer (ex.: a janela atual, o acumulado do scan). Stateless gatherers podem dispensá-lo.
- **`integrator`** — "*a function which integrates provided elements, potentially using the provided intermediate state, optionally producing output to the provided `Gatherer.Downstream`*". É o núcleo: recebe `(estado, elemento, downstream)`, decide o que emitir via `downstream.push(...)` e retorna um `boolean` indicando se quer continuar recebendo elementos (permite **short-circuit**, como um `limit` faria).
- **`combiner`** — "*a function which accepts two intermediate states and combines them into one*". Como no `Collector`, habilita **paralelismo**. Se você não fornecer um combiner, o gatherer roda **sequencialmente** mesmo num stream paralelo.
- **`finisher`** — "*a function which accepts the final intermediate state and a `Gatherer.Downstream` object, allowing to perform a final action at the end of input elements*". Emite o que sobrou no buffer quando o upstream acaba (ex.: a última janela parcial).

O fluxo operacional, segundo a própria documentação:

```java
A state = gatherer.initializer().get();
for (T t : data) {
    gatherer.integrator().integrate(state, t, downstream);
}
gatherer.finisher().accept(state, downstream);
```

Para construir um do zero há `Gatherer.of(...)` e `Gatherer.ofSequential(...)` (este último para gatherers ordenados sem combiner). O integrator costuma vir de `Gatherer.Integrator.of(...)` ou `Gatherer.Integrator.ofGreedy(...)` (quando o integrator nunca faz short-circuit, o que abre otimizações).

```java
// Esqueleto de gatherer customizado (estado mutável + integrator)
Gatherer<T, A, R> custom = Gatherer.ofSequential(
    () -> new A(),                          // initializer
    Gatherer.Integrator.of((state, element, downstream) -> {
        // ... muta state, eventualmente downstream.push(resultado) ...
        return true;                        // true = continuar; false = parar (short-circuit)
    }),
    (state, downstream) -> { /* finisher: drena o buffer final */ });
```

### As fábricas de `Gatherers` (`windowFixed`/`windowSliding`/`fold`/`scan`/`mapConcurrent`)

Assim como `Collectors` é a fábrica de coletores prontos, a classe **`java.util.stream.Gatherers`** entrega gatherers prontos para os casos mais comuns. **Confira os nomes** — são exatamente estes cinco:

| Fábrica | O que faz (descrição da API) |
|---------|------------------------------|
| `windowFixed(int n)` | "*gathers elements into windows — encounter-ordered groups of elements — of a fixed size*". Janelas **não sobrepostas** de tamanho `n` (a última pode vir incompleta). |
| `windowSliding(int n)` | "*windows (...) of a given size, where each subsequent window includes all elements of the previous window except for the least recent, and adds the next element*". Janela **deslizante**: a cada passo descarta o mais antigo e inclui o próximo. |
| `fold(Supplier initial, BiFunction folder)` | "*an ordered, reduction-like, transformation for scenarios where no combiner-function can be implemented, or for reductions which are intrinsically order-dependent*". Reduz a um **único** resultado, respeitando a ordem. |
| `scan(Supplier initial, BiFunction scanner)` | "*a Prefix Scan — an incremental accumulation*". Emite o **acumulado parcial a cada elemento** (saldo corrente, soma acumulada). |
| `mapConcurrent(int maxConcurrency, Function mapper)` | "*executes a function concurrently with a configured level of max concurrency, using virtual threads*", preservando a ordem de saída. |

```java
import java.util.stream.Gatherers;

// windowFixed: lotes de 2, sem sobreposição -> [[a,b],[c,d],[e]]
Stream.of("a","b","c","d","e")
    .gather(Gatherers.windowFixed(2))
    .forEach(System.out::println);

// scan: soma acumulada -> 1, 3, 6, 10
Stream.of(1, 2, 3, 4)
    .gather(Gatherers.scan(() -> 0, Integer::sum))
    .forEach(System.out::println);
```

`mapConcurrent` é o caso especial: ele aplica o `mapper` em **virtual threads**, com no máximo `maxConcurrency` chamadas simultâneas, e **preserva a ordem de encontro** na saída. É o jeito idiomático de paralelizar chamadas I/O-bound (HTTP, banco) dentro de um stream sem mexer no common pool. Ele se relaciona com — mas **não substitui** — o paralelismo de divisão-e-conquista de parallel streams; para o modelo fork/join e quando preferir cada um, veja [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/15 - Parallel streams e fork-join|Parallel streams]].

### **Status de versão** (final no Java 24 via JEP 485 — declarar; hedge se preview na release alvo)

Linha do tempo confirmada da feature **Stream Gatherers**:

| Release | JEP | Status |
|---------|-----|--------|
| Java 22 | JEP 461 | Preview (1ª rodada) |
| Java 23 | JEP 473 | Preview (2ª rodada, sem mudanças) |
| **Java 24** | **JEP 485** | **Final / permanente** (sem mudanças) |

A partir do **Java 24**, `Stream.gather`, `Gatherer` e `Gatherers` são **API padrão e estável** — não exigem `--enable-preview`. Em **Java 22 ou 23**, a feature existe mas é **preview**: o código só compila e roda com a flag `--enable-preview` (e o `--release` correspondente). Em **Java 21 ou anterior**, a API **não existe** — `Stream` nem tem o método `gather`.

> [!warning] Declare a versão alvo antes de usar Gatherers
> Se o projeto está em Java 21 (LTS), Gatherers **não estão disponíveis** em forma alguma. Se está em 22/23, são preview e exigem `--enable-preview` (não recomendado em produção). Só em **24+** são estáveis. Confirme a `--release` do build antes de escrever `.gather(...)`.

## Na prática

```java
// === 1) Collector.of: um coletor terminal sob medida ===
// Acumula os IDs de pedidos num StringJoiner formatado, em uma passada.
// Requer: Java 8+ (Collector.of existe desde o Java 8).
Collector<Order, StringJoiner, String> idsFormatados = Collector.of(
    () -> new StringJoiner(", ", "pedidos[", "]"),  // supplier
    (sj, order) -> sj.add(order.id()),               // accumulator
    StringJoiner::merge,                             // combiner (paralelo)
    StringJoiner::toString);                         // finisher

String resumo = orders.stream().collect(idsFormatados);
// "pedidos[A1, B2, C3]"

// === 2) Gatherers.windowSliding: média móvel de 3 sobre uma sequência de Order ===
// Requer: Java 24+ (Stream Gatherers final via JEP 485).
//         Em Java 22/23 seria preview e exigiria --enable-preview.
List<Double> mediaMovel = orders.stream()
    .map(Order::total)                               // Stream<Double> de totais
    .gather(Gatherers.windowSliding(3))              // Stream<List<Double>> de janelas de 3
    .map(janela -> janela.stream()
        .mapToDouble(Double::doubleValue)
        .average().orElse(0.0))                      // média de cada janela
    .toList();

// orders com totais [100, 200, 300, 400] -> janelas [100,200,300] e [200,300,400]
// -> médias móveis [200.0, 300.0]
```

O `windowSliding(3)` é exatamente o tipo de operação intermediária que **não existia** antes da JEP 485: ela carrega estado (a janela corrente), depende da ordem e emite uma lista por elemento a partir do terceiro. Tente expressar isso só com `map`/`filter` e você acaba num laço com índices, fora do stream.

## Armadilhas

### (1) `combiner` incorreto num `Collector` quebra silenciosamente em paralelo

**O problema:** o `combiner` só é exercitado em execução **paralela**. Um combiner errado (ou que assume associatividade que não existe) passa em todos os testes sequenciais e só corrompe o resultado — sem exceção — quando alguém chama `.parallel()` na fonte.

```java
// ERRADO — "combiner" que só devolve o primeiro contêiner, ignorando o segundo
Collector<Order, List<String>, List<String>> ruim = Collector.of(
    ArrayList::new,
    (lista, o) -> lista.add(o.id()),
    (a, b) -> a);          // BUG: descarta 'b' inteiro

orders.stream().collect(ruim);            // sequencial: parece correto
orders.parallelStream().collect(ruim);    // PARALELO: perde metade dos IDs, sem erro
```

**Fix:** o combiner deve **realmente fundir** os dois contêineres; se a operação não é paralelizável, marque-a como tal em vez de fingir um combiner. Para coletores, isso significa testar de fato em paralelo. Para gatherers que não têm combiner válido, use `Gatherer.ofSequential(...)` (sem combiner) — assim a operação roda sequencialmente mesmo num stream paralelo, em vez de produzir lixo.

```java
// CORRETO — combiner funde os dois
Collector<Order, List<String>, List<String>> bom = Collector.of(
    ArrayList::new,
    (lista, o) -> lista.add(o.id()),
    (a, b) -> { a.addAll(b); return a; });   // funde de verdade
```

---

### (2) Reinventar um `Gatherer` que já existe em `Gatherers`

**O problema:** escrever um `Gatherer.ofSequential(...)` manual de janela deslizante, soma acumulada ou batching — quando a classe `Gatherers` já entrega `windowSliding`, `scan`, `fold` e `windowFixed` prontos, testados e otimizados.

```java
// ERRADO — reimplementar janela deslizante de 3 na mão
Gatherer<T, ArrayDeque<T>, List<T>> janelaCaseira = Gatherer.ofSequential(
    ArrayDeque::new,
    Gatherer.Integrator.of((deque, e, down) -> {
        deque.addLast(e);
        if (deque.size() > 3) deque.removeFirst();
        if (deque.size() == 3) down.push(List.copyOf(deque));
        return true;
    }));
```

**Fix:** use a fábrica pronta — menos código, sem bugs de borda (a última janela parcial, *off-by-one*, etc.):

```java
// CORRETO — a biblioteca já faz, e melhor
stream.gather(Gatherers.windowSliding(3));
```

Escreva um gatherer próprio só quando o comportamento **não** for um dos cinco prontos.

---

### (3) Usar Gatherers numa versão que não os tem (não compila)

**O problema:** `Stream.gather`, `Gatherer` e `Gatherers` **não existem** antes do Java 22, e são **preview** no 22/23. Código com `.gather(...)` compilado contra Java 21 falha com "*cannot find symbol*"; contra Java 22/23 sem a flag, falha com erro de preview.

```text
// Java 21:  error: cannot find symbol — method gather(...)
// Java 22/23 sem --enable-preview:
//   error: Stream.gather is a preview API and is disabled by default
```

**Fix:** confira a **release alvo** do build antes de usar a API. Em **Java 24+**, é estável — nada a fazer. Em **22/23**, habilite preview explicitamente (`--release 23 --enable-preview` no `javac` e `--enable-preview` na JVM), ciente de que preview não é para produção. Em **21 ou anterior**, a feature simplesmente não está disponível — sem flag que a destrave.

## Em entrevista

### Frase pronta (inglês)

> "There are two ways to extend a stream pipeline beyond the built-in collectors. First, `Collector.of` builds a custom **terminal** reduction from four functions — a supplier for the mutable container, an accumulator that mutates it in place, a combiner that merges two partial containers in parallel, and a finisher that produces the final result. The combiner is the key detail: it's only invoked in parallel execution, so a broken combiner passes every sequential test and silently corrupts results once someone calls `.parallel()`."
>
> "Second, **Stream Gatherers** — `Stream.gather(Gatherer)`, finalized in Java 24 by JEP 485 after two preview rounds in 22 and 23 — add custom **intermediate** operations, which the API historically lacked. A `Gatherer` is specified by an initializer, an integrator, an optional combiner, and a finisher, and unlike a collector it keeps the pipeline open. The `Gatherers` factory ships ready-made ones: `windowFixed`, `windowSliding`, `fold`, `scan`, and `mapConcurrent` — the last running the mapper on virtual threads with bounded concurrency while preserving encounter order."
>
> "So the symmetry is: `Gatherer` is to the new intermediate `gather` operation what `Collector` is to the terminal `collect` operation. In practice I always try to compose existing collectors and gatherers first, and only write `Collector.of` or `Gatherer.of` when the behavior genuinely can't be expressed by the built-ins — sliding windows and prefix scans, for instance, are already provided, so reinventing them is a smell."

### Vocabulário

| Termo PT | Termo EN |
|----------|----------|
| coletor customizado | custom collector |
| operação intermediária | intermediate operation |
| operação terminal | terminal operation |
| contêiner mutável | mutable container |
| função de mesclagem (combiner) | combiner function |
| estado intermediário | intermediate state |
| janela deslizante | sliding window |
| janela fixa | fixed window |
| varredura de prefixo (scan) | prefix scan |
| dobra / redução ordenada (fold) | fold / ordered reduction |
| característica do coletor | collector characteristic |
| feature de pré-visualização | preview feature |
| curto-circuito (short-circuit) | short-circuit |
| mapeamento concorrente | concurrent mapping |

## Veja também

- [[07 - Operações de Stream — intermediárias e terminais]]
- [[08 - Collectors e agrupamento]]
- [[09 - Streams primitivos]]
- [[03-Dominios/Tecnologia/Java/Collections e Streams/index|Collections e Streams (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/15 - Parallel streams e fork-join|Parallel streams]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#Gatherer (Stream Gatherers)|Gatherer]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#Collector (coletor)|Collector]]

## Referências

- [JEP 485: Stream Gatherers (OpenJDK)](https://openjdk.org/jeps/485) — finalização da feature no Java 24.
- [Gatherers — Java SE 24 API Docs (Oracle)](https://docs.oracle.com/en/java/javase/24/docs/api/java.base/java/util/stream/Gatherers.html) — fábricas `windowFixed`/`windowSliding`/`fold`/`scan`/`mapConcurrent`.
- [Gatherer — Java SE 24 API Docs (Oracle)](https://docs.oracle.com/en/java/javase/24/docs/api/java.base/java/util/stream/Gatherer.html) — initializer/integrator/combiner/finisher.
- [Collector — Java SE 21 API Docs (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/stream/Collector.html) — `Collector.of` e characteristics.
