---
title: "Escolha de coleção e estilo funcional — síntese"
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
  - sintese
  - decisao
aliases:
  - Escolha de coleção
  - Stream vs loop
  - Funcional vs imperativo
---

# Escolha de coleção e estilo funcional — síntese

> [!abstract] TL;DR
> Não existe "melhor" coleção nem "melhor" estilo de processamento no abstrato — existe o **certo para o padrão de acesso, o volume de dados e o contexto** em que o código vai rodar. `ArrayList` e `HashMap` são bons padrões, mas padrão não é resposta automática: a pergunta certa é sempre *como esses dados serão acessados?* (por índice? por chave? em ordem? pelas pontas?). O mesmo vale para `stream` vs loop: o stream agrega clareza quando o fluxo é um pipeline de transformações; o loop vence quando a lógica é imperativa, precisa de *early-return* ou está em caminho crítico de performance. Esta nota não introduz conteúdo novo — ela **liga o galho inteiro**, transformando as decisões espalhadas pelas notas 01–15 em critérios reutilizáveis. A tese é simples: escolher estrutura de dados e estilo é uma **decisão de design**, não um reflexo.

## O que é

Esta é a nota de fechamento do galho **Collections e Streams**. Em vez de cobrir um tópico novo, ela responde a duas perguntas práticas que atravessam todas as outras notas:

1. **Como escolher a estrutura de dados** certa para um problema, entre as implementações de `Collection` e `Map` que o galho cobriu.
2. **Como escolher o estilo de processamento** — `stream` funcional ou loop imperativo — para iterar e transformar esses dados.

A síntese organiza essas escolhas em árvores de decisão e trade-offs explícitos. A ideia central: cada implementação da biblioteca padrão tem um perfil de custo (Big-O por operação) e um perfil de uso (o que ela comunica e garante). Casar o perfil da estrutura com o padrão de acesso do problema é o que separa código correto-e-rápido de código que "funciona" mas degrada sob volume.

O mesmo raciocínio se aplica ao estilo: `stream` e loop não são rivais ideológicos, são ferramentas com pontos ótimos diferentes.

## Por que importa

- **A escolha errada é silenciosa até escalar.** Um `ArrayList.contains` em loop funciona perfeitamente com 50 elementos e derruba o serviço com 500 mil — o bug só aparece em produção, sob volume. Decidir a estrutura *pelo padrão de acesso* previne essa classe inteira de problema.
- **Estrutura e estilo comunicam intenção.** `Set<String>` diz "sem duplicatas" sem um comentário; um pipeline de `stream` diz "transformação sem efeito colateral". Código que comunica intenção é mais fácil de revisar e manter.
- **É uma decisão de design, e design é o que se cobra de um senior.** Em entrevista e em revisão de código, a pergunta não é "você sabe a sintaxe do `groupingBy`?", e sim "por que essa coleção, e não outra?". Saber justificar a escolha é o diferencial de senioridade.
- **Centraliza o galho.** Quem leu as 15 notas anteriores tem as peças; esta nota dá o mapa para encontrá-las e combiná-las sob pressão.

## Como funciona

### Decision tree de coleção

A escolha começa com **uma pergunta sobre o padrão de acesso**, não sobre a implementação. A árvore abaixo consolida as decisões das notas [[01 - O Collections Framework]], [[02 - Listas, conjuntos e filas]] e [[03 - Mapas]].

| Pergunta-guia | Escolha | Por quê | Custo dominante |
|---|---|---|---|
| Preciso de **acesso por índice** / sequência ordenada por posição? | `ArrayList` | Array contíguo, cache-friendly | `get(i)` O(1), `add` fim O(1)* |
| Preciso de **deduplicação** / teste de pertinência rápido? | `HashSet` | Tabela hash, sem ordem | `add`/`contains`/`remove` O(1)* |
| Preciso de **dedup com ordem de inserção** preservada? | `LinkedHashSet` | Hash + lista encadeada | O(1)* com iteração previsível |
| Preciso dos elementos **sempre ordenados**? | `TreeSet` | Red-Black tree | `add`/`contains` O(log n) |
| Preciso de **chave → valor**, acesso rápido? | `HashMap` | Tabela hash | `get`/`put` O(1)* |
| Preciso de **mapa ordenado por chave** / range queries? | `TreeMap` | Red-Black tree | `get`/`put` O(log n) |
| Preciso de mapa com **ordem de inserção** (ou LRU)? | `LinkedHashMap` | Hash + lista encadeada | O(1)* com ordem |
| Preciso de **acesso pelas pontas** (FIFO ou LIFO)? | `ArrayDeque` | Array circular | `offer`/`poll`/`push`/`pop` O(1)* |
| Preciso do **menor/maior elemento** repetidamente (top-K)? | `PriorityQueue` | Binary min-heap | `peek` O(1), `offer`/`poll` O(log n) |
| Preciso de acesso **concorrente** seguro? | (Galho 4) | `ConcurrentHashMap`, `CopyOnWriteArrayList`… | ver [[03-Dominios/Java/Concorrência e paralelismo/15 - Parallel streams e fork-join|Galho 4]] |

\* amortizado / médio (depende da qualidade da função hash em estruturas hash-based)

**Big-O consolidado** das implementações principais (fonte: nota [[02 - Listas, conjuntos e filas]], conferido contra o Javadoc):

| Estrutura | `add`/`put` | acesso (`get`) | `remove` | `contains`/busca | Ordem de iteração |
|---|---|---|---|---|---|
| `ArrayList` | O(1)* fim | O(1) índice | O(n) | O(n) | inserção |
| `LinkedList` | O(1) pontas | O(n) índice | O(n) índice | O(n) | inserção |
| `HashSet` | O(1)* | — | O(1)* | O(1)* | nenhuma |
| `LinkedHashSet` | O(1)* | — | O(1)* | O(1)* | inserção |
| `TreeSet` | O(log n) | — | O(log n) | O(log n) | ordenada |
| `HashMap` | O(1)* | O(1)* | O(1)* | O(1)* (chave) | nenhuma |
| `LinkedHashMap` | O(1)* | O(1)* | O(1)* | O(1)* (chave) | inserção/acesso |
| `TreeMap` | O(log n) | O(log n) | O(log n) | O(log n) (chave) | ordenada por chave |
| `ArrayDeque` | O(1)* pontas | — | O(n) meio | O(n) | inserção (FIFO/LIFO) |
| `PriorityQueue` | O(log n) | `peek` O(1) | O(log n) topo | O(n) arbitrário | **não ordenada** na iteração |

\* amortizado ou médio. Nota sobre memória: estruturas baseadas em nós (`LinkedList`, `TreeMap`/`TreeSet`) gastam mais memória por elemento (ponteiros + objetos `Node` espalhados no heap) do que arrays contíguos — o impacto disso no GC e na localidade de cache se conecta a [[03-Dominios/Java/JVM/02 - Áreas de memória de runtime|Áreas de memória de runtime]] (Galho 3).

A regra de ouro da árvore: **se você não consegue nomear o padrão de acesso, ainda não escolheu a coleção — só chutou o padrão.**

### Stream vs loop

`stream` e `for`/`for-each` produzem o mesmo resultado; a diferença é **qual deles comunica melhor a intenção e a que custo**. O material está nas notas [[05 - Introdução à Stream API]], [[07 - Operações de Stream — intermediárias e terminais]] e [[08 - Collectors e agrupamento]].

**O stream agrega clareza quando** o processamento é um **pipeline declarativo**: uma sequência de transformações sem estado mutável compartilhado.

```java
// Pipeline: filtrar → mapear → agrupar. O stream lê como a descrição do problema.
Map<String, List<String>> porCategoria = orders.stream()
    .filter(o -> o.value() > 100)
    .collect(Collectors.groupingBy(
        Order::category,
        Collectors.mapping(Order::id, Collectors.toList())));
```

**O loop é a escolha melhor quando:**

- **A lógica é imperativa e complexa** — múltiplas variáveis de estado, condições aninhadas que não cabem num `filter`/`map` legível.
- **Você precisa de *early-return* / `break`** — um loop sai no primeiro match com `break` ou `return`; no stream o equivalente é `findFirst()`/`anyMatch()`, que cobrem casos simples mas não controle de fluxo arbitrário no meio de uma transformação.
- **Performance é crítica em caminho quente** — para iterações triviais e muito frequentes, o loop evita a alocação dos objetos intermediários do pipeline e o overhead de lambdas/`Spliterator`. (Em microbenchmarks isso costuma ser pequeno; *meça* antes de afirmar — não suponha.)
- **Há efeito colateral inevitável** — `stream.forEach` com mutação de estado externo é um anti-padrão; se você precisa mutar algo a cada iteração, um loop é mais honesto.

```java
// Early-return: o loop expressa "pare assim que achar" diretamente.
for (Order o : orders) {
    if (o.id().equals(target)) {
        return o;          // sai na hora
    }
}
return null;
```

### Funcional vs imperativo

Acima da escolha pontual stream-vs-loop está o trade-off de **estilo**, coberto por [[04 - Lambdas e interfaces funcionais]] e pela nota de funcional moderno do galho. Sem dogma — cada eixo tem um custo real:

| Eixo | Estilo funcional (stream/lambda) | Estilo imperativo (loop) |
|---|---|---|
| **Legibilidade** | Vence em pipelines de transformação; o código descreve *o quê*, não *como* | Vence em lógica de fluxo complexa, com estado e ramificações |
| **Debug** | Mais difícil: stack traces de lambdas são opacos, não dá pra colocar breakpoint "no meio do pipeline" trivialmente | Mais fácil: passo a passo, breakpoint em qualquer linha, inspeção de variáveis |
| **Estado** | Favorece imutabilidade; sem variáveis mutáveis compartilhadas | Tende a usar mutação local — barato, mas exige cuidado |
| **Performance** | Overhead de alocação/boxing em hot paths; ganha quando habilita paralelismo trivial | Sem overhead de pipeline; previsível |
| **Composição** | Alta: operações encadeáveis e reutilizáveis | Baixa: lógica acoplada ao loop |

O ponto de equilíbrio: use **funcional para descrever transformações de dados** e **imperativo para controlar fluxo**. Misturar os dois de forma deliberada (um pipeline declarativo dentro de um método, um loop com `break` em outro) é maturidade, não inconsistência.

### Quando paralelizar

Quando o volume é grande e o trabalho por elemento é independente e CPU-bound, um `stream` pode virar `parallelStream()` para distribuir o processamento entre núcleos via fork-join. Mas paralelizar tem custo de coordenação, exige operações *stateless* e *associativas*, e frequentemente perde para o stream sequencial em volumes pequenos. Os critérios completos — quando vale, quando atrapalha, como medir — estão no Galho 4: ver [[03-Dominios/Java/Concorrência e paralelismo/15 - Parallel streams e fork-join|Parallel streams]]. Aqui fica só o gancho: **paralelismo é uma otimização condicional, não um upgrade gratuito do pipeline.**

### Recursos modernos a favor da decisão

A árvore de coleção e o eixo stream-vs-loop são a base; mas Java 21–24 trouxe três recursos que **ampliam o espaço de decisão** sem mudar os princípios. Saber que eles existem evita escolhas piores por desconhecimento da plataforma.

- **Acesso uniforme às pontas — [[14 - SequencedCollection e SequencedMap]] (Java 21).** Antes, "preciso do primeiro/último elemento" influenciava a escolha da coleção (uma `Deque` por causa do `peekFirst`/`peekLast`, por exemplo) ou forçava `get(size()-1)` propenso a *off-by-one*. Com `SequencedCollection`/`SequencedMap`, `getFirst()`/`getLast()`/`reversed()` viraram contrato comum a `List`, `Deque`, `LinkedHashSet`, `TreeMap` etc. Efeito na decisão: o acesso pelas pontas **deixa de ser um critério de desempate** entre estruturas — qualquer coleção ordenada o oferece de forma uniforme, e `reversed()` é uma *view* ao vivo (sem cópia). A escolha volta a ser pelo padrão de acesso dominante (índice, pertinência, ordem), não pela ergonomia de pegar a ponta.

- **Customizar o pipeline quando o padrão não basta — [[15 - Collectors customizados e Gatherers]] (Gatherers GA no Java 24).** A decisão stream-vs-loop muitas vezes pendia para o loop justamente porque a operação desejada — janela deslizante, *scan* (soma/saldo acumulado), *fold* ordenado — não existia como operação intermediária de stream. Os **Gatherers** (`Stream.gather`, com fábricas `windowFixed`, `windowSliding`, `fold`, `scan`, `mapConcurrent`) fecham essa lacuna: passa a ser possível manter o estilo declarativo onde antes só o loop resolvia. Efeito na decisão: o argumento "tem que ser loop porque o stream não tem essa operação" enfraquece — mas só se o baseline do projeto for Java 24+. Sem isso, o critério antigo continua valendo.

- **Compor a transformação em vez de aninhá-la — [[13 - Composição funcional e funções de alta ordem]].** Quando a escolha é o estilo funcional, a composição (`Function.andThen`/`compose`, `Predicate.and`/`or`) permite **nomear** etapas (`precificar = aplicarImposto.andThen(arredondar)`) e reusá-las entre pipelines, em vez de empilhar lambdas anônimas. Efeito na decisão: melhora o lado "legibilidade" do estilo funcional — desde que a composição não vire uma cadeia inline profunda, que reintroduz o problema de *debug* e stack traces opacos. Compor é a favor; aninhar sem nomear é contra.

A leitura conjunta: esses recursos **não criam regras novas**, deslocam os pesos da decisão existente. Acesso às pontas some como critério de escolha de coleção; Gatherers reduzem os casos em que o loop vence o stream; composição reforça o estilo funcional quando aplicada com nome e parcimônia.

## Na prática

**Cenário 1 — deduplicar e ordenar tags de pedidos.** Imagine um serviço que recebe `Order`s, cada um com uma lista de *tags*, e precisa devolver o conjunto de tags **únicas em ordem alfabética** para um filtro de UI.

- *Coleção:* `TreeSet<String>` — dedup (é `Set`) + ordenação natural (Red-Black tree) em uma estrutura só, sem etapa extra de `sort`.
- *Estilo:* funcional, porque é um pipeline puro de coleta.

```java
Set<String> tagsOrdenadas = orders.stream()
    .flatMap(o -> o.tags().stream())
    .collect(Collectors.toCollection(TreeSet::new));
// dedup + ordenação garantidos pela estrutura, não por código manual
```

**Cenário 2 — os 10 clientes de maior gasto.** Imagine um serviço que processa milhões de `Order`s em streaming e precisa manter, a qualquer momento, o **top-10 de `Customer` por gasto acumulado**, sem carregar tudo na memória ordenado.

- *Coleção:* `PriorityQueue` de tamanho fixo 10 (min-heap) — mantém só os 10 maiores, descartando o menor quando estoura. Evita ordenar a coleção inteira (O(n log n)) para pegar 10 itens.
- *Estilo:* imperativo, porque há **estado mutável** (a heap) atualizado a cada elemento — um loop é mais honesto que um `forEach` com efeito colateral.

```java
int K = 10;
PriorityQueue<Customer> top = new PriorityQueue<>(
    Comparator.comparingDouble(Customer::totalSpent)); // min-heap
for (Customer c : customers) {           // streaming, milhões de itens
    top.offer(c);
    if (top.size() > K) top.poll();      // descarta o menor — mantém top-K
}
// top contém os 10 maiores; custo O(n log K), não O(n log n)
```

**Cenário 3 — índice produto → estoque para lookups frequentes.** Imagine um serviço de checkout que, para cada item do carrinho, consulta o estoque de um `Product` milhares de vezes por segundo.

- *Coleção:* `HashMap<String, Integer>` (id do produto → quantidade) — `get` O(1) médio. Usar uma `List` e buscar com `contains`/loop seria O(n) por consulta e derrubaria a latência sob carga.
- *Estilo:* o build do índice é funcional (pipeline de coleta); a consulta quente é um simples `map.get` — sem pipeline, sem overhead.

```java
Map<String, Integer> estoque = products.stream()
    .collect(Collectors.toMap(Product::id, Product::stock));   // build: funcional

// caminho quente, milhares de chamadas/s — lookup O(1), sem stream
int disponivel = estoque.getOrDefault(itemId, 0);
```

**Cenário 4 — histórico de saldo e o N mais recente.** Imagine um serviço que registra os lançamentos de um `Customer` em ordem cronológica e precisa de duas coisas: (a) o **saldo acumulado a cada lançamento** (para um gráfico) e (b) acesso rápido ao **lançamento mais recente** e aos *N* últimos, em ordem inversa.

- *Coleção:* `LinkedHashMap`/`List` preservando ordem de inserção — é a ordem cronológica. Como é uma coleção sequenciada (Java 21), o "mais recente" é `getLast()` e os últimos em ordem inversa saem de `reversed()` como *view*, sem cópia nem `sort`. Aqui o acesso pelas pontas **não decide** a estrutura (ver [[14 - SequencedCollection e SequencedMap]]): a ordem de inserção já era o requisito; as pontas vêm de graça.
- *Estilo:* funcional para o saldo acumulado, **se** o baseline for Java 24+: o *scan* dos [[15 - Collectors customizados e Gatherers]] emite o parcial a cada elemento sem laço manual com variável de estado. Em baseline anterior, esse mesmo cálculo cai para um loop com acumulador — exatamente o caso em que "o stream não tem a operação" empurra para o imperativo.

```java
// (a) saldo acumulado por lançamento — Java 24+: scan mantém o estilo declarativo
List<Long> saldoCorrente = lancamentos.stream()
    .map(Lancamento::valor)
    .gather(Gatherers.scan(() -> 0L, Long::sum))   // emite o acumulado a cada passo
    .toList();

// (b) lançamento mais recente e os 3 últimos em ordem inversa — sem cópia (view)
Lancamento maisRecente = lancamentos.getLast();    // Java 21
List<Lancamento> ultimos3 = lancamentos.reversed().stream()
    .limit(3)
    .toList();
```

A decisão combinada: a estrutura veio do requisito de ordem (não da ergonomia de ponta), e o estilo dependeu de uma feature de plataforma estar disponível — ilustrando que "qual baseline de Java?" é parte legítima da decisão de design, não um detalhe.

## Armadilhas

### (1) Escolher a coleção por hábito (`ArrayList`/`HashMap` sempre)

**O raciocínio errado:** "`ArrayList` é a lista, `HashMap` é o mapa, é o que eu sempre uso." O hábito ignora a pergunta que deveria vir primeiro — *como esses dados serão acessados?*. `ArrayList` é péssimo para teste de pertinência frequente (`contains` O(n)); `HashMap` é inútil quando você precisa de ordem.

**O raciocínio correto:** deixe o **padrão de acesso ditar a estrutura**. Pertinência frequente → `HashSet`. Precisa de ordem → `TreeSet`/`TreeMap` ou variante `Linked`. Acesso pelas pontas → `ArrayDeque`. `ArrayList`/`HashMap` são *defaults sensatos*, não respostas automáticas — defaults são onde você começa quando o padrão de acesso é "genérico", não onde você para de pensar.

### (2) "Tudo vira stream"

**O raciocínio errado:** "stream é moderno, loop é antigo — então converto todo `for` em pipeline." O resultado são pipelines tortuosos para lógica que é naturalmente imperativa: `forEach` com mutação de estado externo, `reduce` ilegível onde um acumulador num loop seria óbvio, ou um `findFirst` improvisado onde um `break` diria a mesma coisa com menos cerimônia.

**O raciocínio correto:** o stream é para **transformação declarativa de dados**; o loop é para **controle de fluxo**. Um loop com `break` para early-return, um acumulador mutável local, ou lógica condicional aninhada complexa muitas vezes são **mais claros e mais rápidos** como loop. Escolha pela clareza do caso concreto, não pela modernidade percebida da sintaxe.

### (3) Otimização prematura de estrutura sem medir

**O raciocínio errado:** "`LinkedList` é O(1) para inserir no início, então vou usar para ganhar performance" — ou trocar `ArrayList` por estruturas exóticas baseado em intuição de Big-O. Big-O ignora constantes e localidade de cache: na prática `LinkedList` quase sempre perde para `ArrayList` por *pointer chasing* e cache misses, mesmo onde a complexidade teórica favoreceria a lista ligada.

**O raciocínio correto:** **meça antes de otimizar.** Comece com o default sensato (`ArrayList`/`HashMap`), defina a métrica que importa (latência? throughput? memória?) e só troque a estrutura com um benchmark concreto justificando. Otimização guiada por intuição de complexidade, sem medição, troca um problema real (legibilidade) por um ganho imaginário.

### (4) Ignorar o custo de alocação do pipeline (e o de imutabilidade)

**O raciocínio errado:** tratar o eixo stream-vs-loop como puramente estético ("qual fica mais bonito") e o eixo imutável-vs-mutável como dogma ("imutável é sempre melhor"), sem ver o custo de memória por trás de cada escolha.

**O raciocínio correto:** os dois eixos têm um custo de **alocação** concreto que pesa em caminho quente.

- *Stream vs loop — alocação intermediária.* Um pipeline de stream aloca objetos que o loop não aloca: o `Stream`/`Spliterator`, as instâncias de lambda (em geral reusadas, mas presentes), e — o mais caro — o *boxing* de primitivos quando se usa `Stream<Integer>` em vez de `IntStream`. Para uma transformação trivial executada milhões de vezes por segundo, essa pressão extra no *young gen* pode dominar o tempo. O loop, sem pipeline, não paga isso. **Em volume pequeno ou frequência baixa a diferença é irrelevante** e a clareza do stream vence; o trade-off só morde no *hot path*. Daí a regra recorrente desta nota: *meça antes de afirmar* — e, se for processar primitivos, prefira `IntStream`/`LongStream` (ver [[09 - Streams primitivos]]) para eliminar o boxing antes de pensar em abandonar o stream.

- *Imutável vs mutável — cópia vs partilha.* Coleções imutáveis (`List.of`, `Map.of`, `Collectors.toUnmodifiableList`) comunicam intenção, são *thread-safe* por construção e seguras para compartilhar como retorno de método sem defensive copy. O custo: **toda "modificação" é uma nova alocação** — construir uma `List.of` derivada a cada passo, num laço quente, multiplica o lixo. Coleções mutáveis (um `ArrayList` que cresce *in place*) evitam essa alocação repetida, ao preço de exigir disciplina contra vazamento de referência mutável. A decisão: **imutável por padrão na fronteira** (o que sai de um método, o que vira chave de mapa), **mutável no acúmulo local quente** (o contêiner que você preenche dentro do método e só então expõe — eventualmente "congelando" com `Collections.unmodifiableList` ou `List.copyOf` na saída). Não é "imutável sempre"; é imutável onde a segurança paga o custo, mutável onde o custo não se justifica.

O fio comum com as armadilhas anteriores: **alocação é um recurso, e escolher coleção e estilo é também escolher quanto lixo gerar.** O default continua sendo clareza; o ajuste por alocação é guiado por medição, não por intuição.

## Em entrevista

### Frase pronta (inglês)

> "I treat the choice of data structure as a design decision, not a default. The first question I ask is about the access pattern — am I indexing by position, testing membership, keeping things sorted, or accessing from the ends? That answer points straight at the right implementation: `ArrayList` for indexed access, `HashSet`/`HashMap` for O(1) membership and lookup, `TreeSet`/`TreeMap` when I need sorted order at O(log n), `ArrayDeque` for stacks and queues, and a fixed-size `PriorityQueue` for top-K problems. I apply the same judgment to streams versus loops: streams shine for declarative data transformations — filter, map, collect — while a plain loop wins when the logic is imperative, needs an early break, or sits on a hot path where allocation overhead matters. And I never optimize a structure on intuition alone — Big-O hides cache effects, so `LinkedList` usually loses to `ArrayList` in practice. I measure before I switch."

### Vocabulário

| Termo PT | Termo EN |
|---|---|
| padrão de acesso | access pattern |
| estrutura de dados | data structure |
| teste de pertinência | membership test |
| caminho quente / crítico | hot path / critical path |
| retorno antecipado | early return |
| efeito colateral | side effect |
| imutabilidade | immutability |
| decisão de design | design decision |
| otimização prematura | premature optimization |
| sobrecarga (de alocação) | (allocation) overhead |

### Cheatsheet do galho

Qual nota consultar para qual problema:

| Preciso de… | Nota |
|---|---|
| Entender a hierarquia `Collection`/`Map` | [[01 - O Collections Framework]] |
| Escolher implementação de lista/set/fila (Big-O) | [[02 - Listas, conjuntos e filas]] |
| Escolher implementação de mapa | [[03 - Mapas]] |
| Ordenar elementos (`Comparable`/`Comparator`) | [[06 - Comparable e Comparator]] |
| Introdução a streams | [[05 - Introdução à Stream API]] |
| Operações intermediárias e terminais | [[07 - Operações de Stream — intermediárias e terminais]] |
| Agrupar e coletar resultados | [[08 - Collectors e agrupamento]] |
| Streams de primitivos (`IntStream` etc.) | [[09 - Streams primitivos]] |
| Lambdas e interfaces funcionais | [[04 - Lambdas e interfaces funcionais]] |
| Evitar `null` com `Optional` | [[10 - Optional]] |
| Datas e horas (`java.time`) | [[11 - java.time — Date e Time API]] |
| I/O de arquivos (`java.nio.file`) | [[12 - I-O moderno com java.nio.file|I/O moderno com java.nio.file]] |
| Compor funções / funções de alta ordem | [[13 - Composição funcional e funções de alta ordem]] |
| Acesso pelas pontas (`getFirst`/`getLast`/`reversed`, Java 21) | [[14 - SequencedCollection e SequencedMap]] |
| Coletor ou Gatherer customizado (Java 24) | [[15 - Collectors customizados e Gatherers]] |

## Veja também

- [[01 - O Collections Framework]]
- [[02 - Listas, conjuntos e filas]]
- [[03 - Mapas]]
- [[05 - Introdução à Stream API]]
- [[07 - Operações de Stream — intermediárias e terminais]]
- [[08 - Collectors e agrupamento]]
- [[13 - Composição funcional e funções de alta ordem]]
- [[14 - SequencedCollection e SequencedMap]]
- [[15 - Collectors customizados e Gatherers]]
- [[03-Dominios/Java/Collections e Streams/index|Collections e Streams (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Concorrência e paralelismo/15 - Parallel streams e fork-join|Parallel streams]]

## Referências

- [Collections Framework Overview — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/collections/intro/index.html)
- [Collections Implementations — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/collections/implementations/index.html)
- [Class ArrayList — Java SE 21 API (docs.oracle.com)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/ArrayList.html)
- [Class HashMap — Java SE 21 API (docs.oracle.com)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/HashMap.html)
- [Class TreeMap — Java SE 21 API (docs.oracle.com)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/TreeMap.html)
- [Class ArrayDeque — Java SE 21 API (docs.oracle.com)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/ArrayDeque.html)
- [Class PriorityQueue — Java SE 21 API (docs.oracle.com)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/PriorityQueue.html)
- [Package java.util.stream — Java SE 21 API (docs.oracle.com)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/stream/package-summary.html)
- [Aggregate Operations (Streams) — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/collections/streams/index.html)
