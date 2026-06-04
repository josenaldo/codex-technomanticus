---
title: "Spec — Galho 2 da trilha Java Senior (Collections, Streams e Programação Funcional)"
date: 2026-06-04
author: Josenaldo
status: draft
type: spec
publish: false
---

# Spec — Galho 2 da trilha Java Senior (Collections, Streams e Programação Funcional)

## 1. Contexto e motivação

Este é o **segundo galho** da trilha Java Senior (roadmap em `docs/superpowers/specs/2026-06-02-java-senior-roadmap-design.md`). Pressupõe leitura do roadmap, que estabelece topologia flat, esquema de 3 fases, padrões editoriais e política de poda. Os Galhos 1 (Linguagem, 15 notas), 4 (Concorrência, 16 notas) e 5 (Swing, 12 notas) já fecharam e mergearam em `main` — seus artefatos são o **template de padrão e qualidade** deste galho.

**Diferença estrutural decisiva em relação ao Galho 5: este é um galho de REFATOR DE TRONCO, não de pesquisa.** O Galho 5 nasceu de docs oficiais porque não tinha tronco. O Galho 2 tem tronco a podar: `Core/Java Fundamentals.md` alimenta os galhos 1-4, e seis de suas seções estão hoje marcadas com o callout `[!info] Migra em galho futuro (Galho 2)`, esperando este galho. Consequências:

- **Há pré-flight de leitura de tronco** (§6), já executado nesta fase de brainstorming: headings reais confirmados, poda do Galho 1 verificada (parcial), seções do Galho 2 mapeadas.
- **Há task de poda parcial** (§3.5): as seis seções do Galho 2 viram callouts com wikilinks; a seção `## JVM` fica pro Galho 3 e a `## Concorrência (visão geral)` é dívida do Galho 4 — **nenhuma das duas é tocada aqui**.
- **Há higienização de fabricação** (§3.5): o tronco tem conteúdo em primeira pessoa fabricado (a cauda `## How to explain in English` abre com *"Java has been my primary language for over 20 years, and I've seen it evolve"*) e exemplos com sabor de cliente real (`Patient`/`getSpecialty`/`getAge`, eco do MedEspecialista). O Galho 4 já encontrou referências reais nessas seções — **atenção redobrada** (regra inegociável [[feedback_no_fabrication]]). As notas novas usam exemplos neutros (`Order`/`Customer`/`Product`); a poda higieniza o que ficar.
- **Há quitação de dívida de linkback** (§3.6): o Galho 4 hoje linka `[[Java Fundamentals]]` nas notas 07 (Concurrent collections) e 15 (Parallel streams) porque o Galho 2 não existia. Quando as notas deste galho existirem, esses links passam a apontar pras notas reais.

Galho 2 é o **dono dos conceitos de coleções, streams e programação funcional** da trilha. Depende do Galho 1 (genéricos, interfaces, records). É denso por natureza — cobre Collections Framework + Stream API + programação funcional + Optional + Date/Time + I/O moderno — e por isso tem **16 notas**, na mesma faixa de densidade dos Galhos 1 (15) e 4 (16).

## 2. Objetivo

Produzir, em uma sessão de execução dedicada **direto na `main`** (sem branch dedicada — ver [[feedback_galhos_direto_main]]), **16 notas atômicas + 1 MOC do galho + expansão do Dicionário de Java + ativação do MOC central + poda parcial do tronco + quitação da dívida de linkback do Galho 4**, em `03-Dominios/Java/Collections e Streams/` e `03-Dominios/Java/`, todas `publish: true`, em PT-BR, distribuídas em 3 fases (5 Iniciado + 7 Adepto + 4 Magus).

Ao terminar o galho, o leitor deve conseguir:

- **Explicar em inglês** a hierarquia do Collections Framework, o contrato `hashCode`/`equals`, a anatomia lazy/eager de uma pipeline de Stream e o papel das interfaces funcionais.
- **Escolher e justificar** a estrutura de dados certa (`ArrayList` vs `LinkedList`, `HashMap` vs `TreeMap`, `ArrayDeque` vs `PriorityQueue`) e o estilo (stream vs loop, funcional vs imperativo) para um cenário dado, com as características de performance (Big-O) na ponta da língua.
- **Reconhecer e diagnosticar** em code review as armadilhas clássicas (`hashCode`/`equals` quebrados, `ConcurrentModificationException`, abuso de `peek`, `Optional` como campo/parâmetro, `Collectors.toMap` com chave duplicada, boxing em loop, `==` em datas).
- **Decidir e defender** quando o estilo funcional/declarativo agrega clareza e quando um loop imperativo é melhor — sem dogma.

A barra é "decidir, justificar, reconhecer patterns e armadilhas em code review" — não "implementar um framework de coleções from scratch".

## 3. Saídas concretas

### 3.1. Notas (`03-Dominios/Java/Collections e Streams/`)

Pasta **nova**, flat. 16 notas + 1 MOC. Numeração global por galho (não reinicia por fase). Pasta precisa de `index.md` (Quartz folder-link). Tag de galho: `collections`.

#### Iniciado (5 notas — vocabulário + modelo mental)

| # | Nota | Escopo nuclear |
|---|------|----------------|
| 01 | O Collections Framework | O que é o framework; hierarquia `Iterable`→`Collection`→`List`/`Set`/`Queue` e `Map` (que **não** é `Collection`); o papel de cada família; `Collection` API comum (`add`/`remove`/`contains`/`size`/`iterator`); coleções imutáveis (`List.of`/`Set.of`/`Map.of`, Java 9+) vs views (`unmodifiableList`). Porta de entrada do galho. **Linka Galho 1** (genéricos) e **Galho 4** (concurrent collections — dono lá). |
| 02 | Listas, conjuntos e filas | `ArrayList` (array dinâmico, acesso O(1)) vs `LinkedList` (lista ligada); `HashSet`/`LinkedHashSet`/`TreeSet` (dedup, ordem, Red-Black tree); `Queue`/`Deque` com `ArrayDeque` (FIFO/LIFO, substitui `Stack`) e `PriorityQueue` (heap, top-K). Estrutura interna + Big-O + quando usar cada um. |
| 03 | Mapas | `HashMap` por dentro (buckets, função de hash, **contrato `hashCode`/`equals`**, treeification de bucket em Java 8+); `LinkedHashMap` (ordem de inserção/acesso, base de cache LRU); `TreeMap` (ordenado, `NavigableMap`); a **API rica** (`getOrDefault`/`putIfAbsent`/`merge`/`compute`/`computeIfAbsent`/`forEach`). `ConcurrentHashMap` é **citado** mas é dono do Galho 4. |
| 04 | Lambdas e interfaces funcionais | Sintaxe lambda; `@FunctionalInterface` (SAM); as quatro centrais `Function<T,R>`/`Predicate<T>`/`Consumer<T>`/`Supplier<T>` + variantes (`BiFunction`, `UnaryOperator`, `BiPredicate`, especializações primitivas `IntFunction`/`ToIntFunction`); **method references** (estático, de instância de tipo, de objeto, construtor). **Linka Galho 1** (08 Interfaces) pra mecânica de interfaces — **não re-explica**. |
| 05 | Introdução à Stream API | O que é um stream (sequência + pipeline, **não** estrutura de dados); anatomia da pipeline (source → intermediárias **lazy** → terminal **eager**); avaliação preguiçosa e curto-circuito; stream vs collection; stream vs loop; stream é consumível uma vez. Menciona `parallelStream` mas **linka Galho 4** (15) pro paralelismo. |

#### Adepto (7 notas — domínio operacional; 1 densa → opus)

| # | Nota | Escopo nuclear |
|---|------|----------------|
| 06 | Comparable e Comparator | Ordem natural com `Comparable<T>` (`compareTo`, contrato de consistência com `equals`); ordem externa com `Comparator` (`comparing`/`comparingInt`/`thenComparing`/`reversed`/`nullsFirst`/`nullsLast`); `sort` em `List` e em streams. Exemplos com record (link Galho 1). |
| 07 | Operações de Stream — intermediárias e terminais | Intermediárias: `map`/`filter`/`flatMap`/`mapMulti`/`distinct`/`sorted`/`peek`/`limit`/`skip`/`takeWhile`/`dropWhile`. Terminais: `forEach`/`forEachOrdered`/`toList`/`collect`/`reduce`/`count`/`min`/`max`/`findFirst`/`findAny`/`anyMatch`/`allMatch`/`noneMatch`. Quando usar curto-circuito; `peek` só pra debug. |
| 08 | Collectors e agrupamento *(opus)* | `Collectors.toList`/`toUnmodifiableList`/`toSet`/`toMap` (e o merge function pra chave duplicada); `joining`; **`groupingBy`** + downstream collectors (`counting`/`summingInt`/`mapping`/`averagingDouble`/`toList`); `partitioningBy`; `collectingAndThen`; `reducing`. O `collect` mutável vs `reduce` imutável. |
| 09 | Streams primitivos | `IntStream`/`LongStream`/`DoubleStream`; `range`/`rangeClosed`/`iterate`/`of`; `mapToInt`/`mapToObj`/`boxed`; `sum`/`average`/`max`/`summaryStatistics` (`IntSummaryStatistics`); **custo de boxing/unboxing** e quando o ganho compensa. |
| 10 | Optional | `Optional<T>` como tipo de retorno pra ausência; criação (`of`/`ofNullable`/`empty`); transformação (`map`/`flatMap`/`filter`); consumo (`orElse`/`orElseGet`/`orElseThrow`/`ifPresent`/`ifPresentOrElse`); `Optional` em streams (`stream()`, `flatMap`). **Anti-patterns**: campo de classe, parâmetro de método, `get()` cru, `isPresent()`+`get()`. |
| 11 | java.time — Date/Time API | `LocalDate`/`LocalTime`/`LocalDateTime` (sem timezone), `ZonedDateTime`/`OffsetDateTime` (com), `Instant` (UTC, persistência); `Duration` vs `Period`; `DateTimeFormatter` (parse/format); imutabilidade e thread-safety; regra prática de qual tipo usar. Armadilhas do legado `Date`/`Calendar`/`SimpleDateFormat`. |
| 12 | I/O moderno com java.nio.file | `Path` e `Files`; ler (`readString`/`readAllLines`/`lines`) e escrever (`writeString`/`write`); operações de diretório (`exists`/`createDirectories`/`list`/`walk`); **try-with-resources** e `AutoCloseable` (link Galho 1, 10 Exceções); streaming de arquivos grandes com `Files.lines` (e por que fechar o stream). |

#### Magus (4 notas — maestria + decisão de arquitetura; 3 → opus)

| # | Nota | Escopo nuclear |
|---|------|----------------|
| 13 | Composição funcional e funções de alta ordem *(opus)* | `Function.compose`/`andThen`; `Predicate.and`/`or`/`negate`; `Consumer.andThen`; funções de alta ordem (receber/retornar funções); captura de variáveis e `effectively final`; closures em Java; quando o estilo funcional **ajuda** (transformação declarativa, reuso) vs **atrapalha** (debugging, stack traces, estado). **Linka Galho 1** (lambdas básicas na 04 deste galho). |
| 14 | SequencedCollection e SequencedMap (Java 21) | As interfaces `SequencedCollection`/`SequencedSet`/`SequencedMap` (JEP 431); `getFirst`/`getLast`/`addFirst`/`addLast`/`removeFirst`/`removeLast`/`reversed`; por que foram adicionadas (unificar acesso às pontas, antes inconsistente entre `List`/`Deque`/`LinkedHashSet`); o que passou a implementá-las. **WebFetch obrigatório** (confirmar API e versão). |
| 15 | Collectors customizados e Gatherers (Java 24) *(opus)* | `Collector.of` (supplier/accumulator/combiner/finisher/characteristics) pra coletor sob medida; **Stream Gatherers** (`Stream.gather`, `Gatherer`, fábricas de `Gatherers`: `windowFixed`/`windowSliding`/`fold`/`scan`/`mapConcurrent`) como extensão de intermediárias customizadas. **WebFetch obrigatório** — confirmar status final (JEP 485, Java 24) e a API; declarar version-specificity. |
| 16 | Escolha de coleção e estilo funcional — síntese *(capstone, opus)* | Decision tree: qual coleção pra qual problema (tabela Big-O consolidada); stream vs loop (quando cada um); funcional vs imperativo (trade-offs de legibilidade/debug/performance); cheatsheet de fechamento (qual nota pra qual problema); enquadramento de entrevista. Liga o galho inteiro. |

**Decisões de fronteira (escopo NÃO coberto aqui ou de outro dono):**

- **Paralelismo (parallel streams, fork/join, spliterators)** → **Galho 4 é dono** (nota 15). O Galho 2 é dono do *pipeline* da Stream API (notas 05, 07, 08); menciona `parallelStream`/`parallel()` como existência e **linka** `[[03-Dominios/Java/Concorrência e paralelismo/15 - Parallel streams e fork-join|Parallel streams e fork-join]]` — **não re-explica** fork/join nem decompõe o `ForkJoinPool`. (`mapConcurrent` na nota 15 é a exceção controlada: é um Gatherer da Stream API base, não paralelismo de fork/join — citar como concorrência estruturada leve, com link pro Galho 4.)
- **Concurrent collections (`ConcurrentHashMap`, `CopyOnWriteArrayList`, etc.)** → **Galho 4 é dono** (nota 07). O Galho 2 é dono do Collections Framework base (notas 01-03); **cita** as variantes thread-safe e **linka** pra lá, sem re-explicar concorrência.
- **Interfaces, OOP, genéricos, records, exceções** → **Galho 1 é dono**. A nota 04 (lambdas) linka `[[03-Dominios/Java/Linguagem e sintaxe moderna/08 - Interfaces e classes abstratas|Interfaces e classes abstratas]]`; notas com generics linkam `[[03-Dominios/Java/Linguagem e sintaxe moderna/12 - Generics em profundidade|Generics]]`; exemplos com record linkam `[[03-Dominios/Java/Linguagem e sintaxe moderna/13 - Records e record patterns|Records]]`; try-with-resources linka `[[03-Dominios/Java/Linguagem e sintaxe moderna/10 - Exceções e tratamento de erros|Exceções]]`. **Sem re-explicar.**
- **JVM (memory model, GC)** → **Galho 3** (próximo). Quando uma nota tocar em custo de memória (boxing, treeification, heap), citar como texto "ver Galho 3 (JVM), planejado" — **sem wikilink quebrado**.
- **`JTable` model / Swing** → Galho 5; sem sobreposição (Swing models usam Collections mas o Galho 5 já é dono dos seus models).

### 3.2. MOC do galho

`03-Dominios/Java/Collections e Streams/index.md`:
- `type: moc`, `status: growing`
- Frontmatter padrão (`title: "Collections, Streams e Programação Funcional"`, tags `java`/`collections`/`moc`, aliases `["Collections e Streams", "Galho 2 - Collections, Streams e Programação Funcional"]`)
- TL;DR callout (galho cobre Collections Framework, Stream API, programação funcional/lambdas, Optional, Date/Time e I/O moderno)
- "Sobre este galho" + audiência primária/secundária + nota de que é galho de refator do tronco `Java Fundamentals` (poda parcial)
- Conteúdo agrupado em 3 H2 (`## Iniciado` / `## Adepto` / `## Magus`) com wikilinks pras 16 notas (uma linha descritiva cada, no padrão dos MOCs dos Galhos 1/4/5)
- **Rotas alternativas (5):**
  - **Completa** — 01 → 16 em ordem
  - **Entrevista internacional** — 01 → 03 → 04 → 05 → 07 → 08 → 10 → 16 (framework, mapas, funcional, streams, operações, collectors, Optional, síntese — o que mais cai)
  - **Domine Streams** — 05 → 07 → 08 → 09 → 15 (pipeline → operações → collectors → primitivos → Gatherers) — liga ao Galho 4 pro paralelismo
  - **Escolha de estrutura de dados** — 01 → 02 → 03 → 06 → 16 (hierarquia, impls, mapas, ordenação, decisão)
  - **Programação funcional** — 04 → 13 → 10 → 07 (lambdas, composição, Optional, operações de stream)
- "Veja também": MOC central `[[03-Dominios/Java/index|Trilha Java]]`, Galho 1 (Linguagem), Galho 4 (Concorrência), Galho 3 (JVM, **planejado** — texto sem wikilink), Dicionário de Java, tronco `[[Java Fundamentals]]` (em transição)
- Dataview "Todas as notas do galho"

### 3.3. Dicionário de Java (EXPANSÃO — não recriar)

`03-Dominios/Java/Dicionário de Java.md` já existe (criado no Galho 1, expandido nos Galhos 4 e 5, `type: glossary`, seções alfabéticas A–Y). Este galho **expande** o arquivo inserindo os verbetes de Collections/Streams/funcional **em ordem alfabética case-insensitive (sem acento)** nas seções apropriadas, criando seções novas se necessário. **Nunca recriar o arquivo nem reordenar verbetes existentes.** Atualizar `updated: 2026-06-04`.

Verbetes a inserir (~24-28, lista de referência — ajustar na execução conforme as âncoras reais das notas):

`boxing / unboxing`, `Collector (coletor)`, `Collections Framework`, `Comparable`, `Comparator`, `Deque`, `Duration / Period`, `effectively final`, `Function / Predicate / Consumer / Supplier`, `Gatherer (Stream Gatherers)`, `groupingBy`, `hashCode / equals (contrato)`, `interface funcional`, `Instant`, `java.nio.file (Path / Files)`, `lambda`, `LocalDate / LocalDateTime`, `method reference`, `Optional`, `operação intermediária / terminal`, `PriorityQueue`, `SequencedCollection / SequencedMap`, `Stream`, `stream lazy (avaliação preguiçosa)`, `stream primitivo (IntStream)`, `treeification`, `try-with-resources`.

Cada verbete: definição curta (1-3 linhas) em PT-BR + `Veja também:` apontando pra(s) nota(s) canônica(s). **Conferir 1:1** que os headings dos verbetes batem EXATAMENTE com as âncoras usadas nas notas (extrair as âncoras de Dicionário das notas e conferir, como nos Galhos 4 e 5). Alguns termos já podem existir no Dicionário (ex: `Atomic` é do Galho 4; conferir antes de inserir pra não duplicar).

### 3.4. MOC central (ativação do Galho 2)

`03-Dominios/Java/index.md` já existe e lista os 18 galhos. Task **mínima**: trocar a **linha 26** (atualmente `2. Collections, Streams e Programação Funcional *(planejado)* — Collections Framework, Stream API, lambdas, Optional, Date/Time, I/O`) por um wikilink ativo no padrão das linhas 25/28/32:

```markdown
2. [[03-Dominios/Java/Collections e Streams/index|Collections, Streams e Programação Funcional]] — Collections Framework, Stream API, lambdas e interfaces funcionais, Optional, Date/Time (java.time), I/O moderno (java.nio.file)
```

Atualizar `updated: 2026-06-04`. Não mexer no resto do MOC central.

### 3.5. Poda parcial do tronco + higienização

`Core/Java Fundamentals.md` (862 linhas). O pré-flight (§6) confirmou que **seis seções** estão marcadas com `[!info] Migra em galho futuro (Galho 2)` e são exatamente o escopo deste galho. Cada uma vira um callout no padrão de poda do roadmap (§9):

| Seção do tronco (linhas atuais) | Substituir por callout apontando pra |
|---|---|
| `## Collections Framework` (~291-401) | Notas 01, 02, 03, 06 |
| `## Lambdas e Interfaces Funcionais` (~404-468) | Notas 04, 13 |
| `## Streams API` (~471-588) | Notas 05, 07, 08, 09 |
| `## Date/Time API (Java 8+)` (~591-636) | Nota 11 |
| `## I/O (Arquivos)` (~639-688) | Nota 12 |
| `## Optional` (~698-721) | Nota 10 |

Modelo de callout (padrão §9 do roadmap):

```markdown
## Collections Framework

> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Java/Collections e Streams/index|Collections, Streams e Programação Funcional]]. Veja [[01 - O Collections Framework]], [[02 - Listas, conjuntos e filas]], [[03 - Mapas]], [[06 - Comparable e Comparator]].
```

**NÃO podar:**
- `## JVM (Java Virtual Machine)` (~33-227) → é do **Galho 3** (próximo). Deixar como está.
- `## Concorrência (visão geral)` (~731-796) → dívida de poda do **Galho 4** (ainda marcada `[!info] Migra em galho futuro (Galho 4)`). **Não é escopo deste galho.** Deixar como está.
- As demais seções `[!nota] Migrado` do Galho 1 (Sintaxe, OOP, Records, etc.) — já podadas.

**Higienização de fabricação (regra inegociável [[feedback_no_fabrication]]):**
1. As seis seções podadas perdem todo o corpo (viram callout) — incluindo os exemplos com `Patient`/`getSpecialty`/`getAge` (sabor MedEspecialista). Resolvido pela própria poda.
2. A **cauda compartilhada** do tronco tem fabricação em primeira pessoa que precisa ser higienizada agora:
   - `## How to explain in English` (~819-827): abre com *"Java has been my primary language for over 20 years, and I've seen it evolve significantly... The Collections Framework is something I use constantly. I reach for ConcurrentHashMap..."* — **primeira pessoa fabricada**. Reescrever em terceira pessoa neutra (sobre o ecossistema/a linguagem) **ou** remover, já que o conteúdo de inglês agora mora nas seções "Em entrevista" dos galhos. **Decisão de execução:** reescrever como parágrafo neutro curto + ponteiro pros galhos (preserva utilidade sem atribuir experiência ao autor).
   - `## Na prática` (~815-817): framing "Em projetos enterprise com Java 21..." é aceitável (neutro/genérico), mas conferir que não há atribuição pessoal; manter ou enxugar.
   - `## Armadilhas comuns` (~805-813): neutro, manter (ou linkar pras notas; não é obrigatório migrar).
3. **Atualizar** o "Veja também" e `updated:` do tronco; não apagar histórico Git.

> Esta higienização é restrita à cauda compartilhada e às seções podadas. **Não** reescrever as seções de JVM/Concorrência (donas de outros galhos).

### 3.6. Quitação da dívida de linkback do Galho 4

O Galho 4 fechou antes do Galho 2 existir, então linka o tronco `[[Java Fundamentals]]` onde deveria linkar notas do Galho 2. Pré-flight (§6) localizou as ocorrências. Atualizar (com a `verificar-wikilinks` rodando depois):

| Arquivo | Linha | Hoje | Passa a apontar pra |
|---|---|---|---|
| `Concorrência e paralelismo/07 - Concurrent collections.md` | ~31 (corpo) | "O framework [[Java Fundamentals]] define as interfaces `Map`, `List`, `Queue` e `Set`" | `[[03-Dominios/Java/Collections e Streams/01 - O Collections Framework\|Collections Framework]]` |
| `Concorrência e paralelismo/07 - Concurrent collections.md` | ~399 (Veja também) | `[[Java Fundamentals]]` | `[[03-Dominios/Java/Collections e Streams/01 - O Collections Framework\|Collections Framework]]` (e/ou 03 Mapas) |
| `Concorrência e paralelismo/15 - Parallel streams e fork-join.md` | ~49 (corpo) | "o pipeline... pertence ao Galho 2 (Stream API); consulte [[Java Fundamentals]] para essa base" | `[[03-Dominios/Java/Collections e Streams/05 - Introdução à Stream API\|Stream API]]` (e/ou 07 Operações) |
| `Concorrência e paralelismo/15 - Parallel streams e fork-join.md` | ~450 (Veja também) | `[[Java Fundamentals]]` | `[[03-Dominios/Java/Collections e Streams/07 - Operações de Stream — intermediárias e terminais\|Operações de Stream]]` |

As ocorrências em `11 - Java Memory Model` (~518) e `12 - Virtual Threads` (~394) linkam `[[Java Fundamentals]]` em "Veja também" como **referência geral ao tronco** (não Collections/Streams) — **não são dívida**; deixar como estão. (O tronco segue existindo "em transição".) As linhas exatas serão reconfirmadas na execução (podem ter mudado).

### 3.7. Reciprocidade de links Galho 2 → Galho 4

As notas do Galho 2 que tocam fronteira **linkam de volta** pro Galho 4 (mão dupla):
- Nota 01 (framework) e 03 (mapas) → `[[03-Dominios/Java/Concorrência e paralelismo/07 - Concurrent collections|Concurrent collections]]`.
- Nota 05 (intro stream) e 07 (operações) → `[[03-Dominios/Java/Concorrência e paralelismo/15 - Parallel streams e fork-join|Parallel streams]]`.

## 4. Convenções por nota

Herda §7 do roadmap e §4 dos specs dos Galhos 1/4/5. Reforços específicos:

### 4.1. Frontmatter

```yaml
---
title: "<título>"
created: 2026-06-04
updated: 2026-06-04
type: concept
status: seedling
publish: true
fase: iniciado | adepto | magus
tags:
  - java
  - collections
  - <fase>
  - <tags específicas: streams, funcional, lambda, optional, comparator, collectors, datetime, io, sequenced, gatherers>
aliases:
  - <aliases opcionais>
---
```

### 4.2. Estrutura H2 obrigatória

- `> [!abstract] TL;DR` (callout, NÃO H2)
- `## O que é` / `## Por que importa` / `## Como funciona` (≥3 subseções em notas Adepto/Magus)
- `## Na prática` — exemplos compiláveis; framing neutro ("padrão observado no JDK/no ecossistema", "caso típico em serviço enterprise"); NUNCA "no meu projeto"
- `## Armadilhas` — **≥2** (Iniciado) / **≥3** (Adepto/Magus), cada uma com descrição + exemplo curto de código demonstrando o problema + fix em 1 linha
- `## Em entrevista` — subheading `### Frase pronta (inglês)` com frase de **3+ sentenças** (trade-off + decisão + caveat) + vocabulário **6+ termos PT→EN**
- `## Veja também` — wikilinks **SEM backticks**; sempre inclui notas relacionadas do galho + `[[03-Dominios/Java/Collections e Streams/index|MOC do galho]]` + `[[03-Dominios/Java/index|Trilha Java]]` + (quando o conceito conectar) Galho 1 / Galho 4 + verbetes do Dicionário. **Evitar âncoras same-file `[[#Heading]]`** (falso-positivo no checker).
- `## Referências` — docs oficiais (`dev.java`, `docs.oracle.com`/Javadoc, The Java Tutorials), JEPs quando relevantes.

### 4.3. Restrições absolutas

1. **Sem fabricação** de experiência pessoal. Exemplos neutros (`Order`, `Customer`, `Product`, `Employee`) ou hipotéticos explícitos (`// hipotético: ...`). **NUNCA** `Patient`/`getSpecialty` (sabor MedEspecialista do tronco), `josenaldo`, nem casos vividos.
2. **Conteúdo herdado do tronco é matéria-prima, não cópia** — o tronco tem o esqueleto correto, mas as notas **expandem e modernizam** (não copiam tabelas e snippets como estão). Toda alegação version-specific (`SequencedCollection` Java 21, Gatherers Java 24, `takeWhile`/`dropWhile` Java 9, `toList()` Java 16) é **verificada via WebFetch** antes de afirmar — nada de API "de memória".
3. **Code samples compiláveis** — Java moderno (var, records, switch expressions onde idiomático); 3-5 por nota conceitual. Code fences corretos: ` ```java `, ` ```text ` (output). Sempre fechadas.
4. **Comparações justas** — ao comparar (`ArrayList` vs `LinkedList`, `HashMap` vs `TreeMap`, stream vs loop, funcional vs imperativo, `collect` vs `reduce`), incluir "quando X" E "quando Y". A capstone (16) é o ápice dessa exigência.
5. **Wikilinks sem backticks** em "Veja também"; MOC do galho + MOC central obrigatórios. **Não linkar notas do Galho 3 (JVM, inexistente)** — usar texto "planejado".
6. **`fase:` no frontmatter + na tag** — obrigatório.
7. **Higiene de commits** — sem `Co-Authored-By: Claude` ([[feedback_commits]]), sem `--no-verify`, `git add <path>` nominal, **1 commit por nota**. **Trabalho direto na `main`** ([[feedback_galhos_direto_main]]); **push é manual do usuário** — não pushar.
8. **Tom pedagógico graduado** — Iniciado assume pouco; Magus assume domínio dos anteriores e do Galho 1.

## 5. Conteúdo por nota (síntese)

Esboço do recorte. As notas **expandem** o material do tronco (não copiam) e verificam features version-specific via WebFetch. Fontes-base: Javadoc de `java.util`/`java.util.stream`/`java.util.function`/`java.time`/`java.nio.file`, The Java Tutorials (Collections, Lambda Expressions, Aggregate Operations), `dev.java`, JEPs (431 Sequenced Collections, 485 Stream Gatherers).

- **01 — O Collections Framework.** Hierarquia, papel de `List`/`Set`/`Queue`/`Map`, `Collection` API comum, imutáveis vs views. Armadilhas: `List.of` é imutável (`UnsupportedOperationException`); `unmodifiableList` é view (original ainda muta); `Arrays.asList` tamanho fixo. Linka Galho 1 (generics), Galho 4 (concurrent). Fonte: Tutorial "Collections", Javadoc `java.util`.
- **02 — Listas, conjuntos e filas.** `ArrayList`/`LinkedList`, `HashSet`/`LinkedHashSet`/`TreeSet`, `ArrayDeque`/`PriorityQueue`; Big-O; quando cada um. Armadilhas: `LinkedList` por reflexo (quase sempre `ArrayList` ganha); `contains` em `ArrayList` é O(n); `TreeSet` exige `Comparable`/`Comparator`. Fonte: Javadoc das impls.
- **03 — Mapas.** `HashMap` por dentro (buckets, hash, **contrato `hashCode`/`equals`**, treeification), `LinkedHashMap`, `TreeMap`/`NavigableMap`, API rica. Armadilhas: `hashCode`/`equals` inconsistentes (chave some do mapa); mutar chave depois de inserir; `HashMap` em acesso concorrente → cita Galho 4. Fonte: Javadoc `HashMap`/`Map`.
- **04 — Lambdas e interfaces funcionais.** Sintaxe, `@FunctionalInterface`, as quatro centrais + variantes + especializações primitivas, method references. Linka Galho 1 (08). Armadilhas: lambda capturando variável não-`effectively final`; method reference ambíguo; criar interface funcional onde já existe uma no JDK. Fonte: Tutorial "Lambda Expressions", Javadoc `java.util.function`.
- **05 — Introdução à Stream API.** Stream não é estrutura de dados; pipeline lazy/eager; curto-circuito; stream consumível uma vez; stream vs loop. Menciona `parallelStream` → linka Galho 4. Armadilhas: reusar um stream já consumido (`IllegalStateException`); achar que intermediárias executam sozinhas (são lazy); efeito colateral em `map`. Fonte: Tutorial "Aggregate Operations", Javadoc `java.util.stream`.
- **06 — Comparable e Comparator.** Ordem natural vs externa; combinadores; consistência com `equals`. Armadilhas: `compareTo` inconsistente com `equals` (`TreeSet` "perde" elementos); subtração de int com overflow (`a-b`) → usar `Integer.compare`; esquecer `nullsFirst`. Fonte: Javadoc `Comparator`/`Comparable`.
- **07 — Operações de Stream.** Intermediárias e terminais (catálogo + semântica). Armadilhas: `peek` pra lógica (não garantido); `sorted` sem `Comparator` em tipo não-`Comparable`; `forEach` mutando estado externo. Fonte: Javadoc `Stream`.
- **08 — Collectors e agrupamento (opus).** `toList`/`toMap` (+ merge function), `joining`, `groupingBy` + downstream, `partitioningBy`, `collectingAndThen`. Armadilhas: `toMap` com chave duplicada (`IllegalStateException`) → merge function; `groupingBy` mutável vs `toUnmodifiableList`; downstream collector errado. Fonte: Javadoc `Collectors`.
- **09 — Streams primitivos.** `IntStream`/`LongStream`/`DoubleStream`, criação, `mapToInt`/`boxed`, summary statistics, custo de boxing. Armadilhas: `Stream<Integer>` onde `IntStream` serve (boxing); `mapToObj` esquecido; `average()` retorna `OptionalDouble`. Fonte: Javadoc `IntStream`.
- **10 — Optional.** Retorno pra ausência; criação/transformação/consumo; `Optional` em streams. Armadilhas: `Optional` como campo/parâmetro; `get()` cru; `isPresent()`+`get()` (use `map`/`orElse`); `Optional.of(null)` (NPE). Fonte: Javadoc `Optional`.
- **11 — java.time.** `Local*`/`Zoned*`/`Instant`, `Duration`/`Period`, `DateTimeFormatter`, imutabilidade. Armadilhas: `Date`/`Calendar`/`SimpleDateFormat` (legado, mutável, não thread-safe); confundir `Duration` (tempo) com `Period` (datas); timezone implícito. Fonte: Tutorial "Date Time", Javadoc `java.time`.
- **12 — I/O moderno com java.nio.file.** `Path`/`Files`, ler/escrever, diretórios, try-with-resources, `Files.lines` streaming. Linka Galho 1 (10 Exceções) pra try-with-resources. Armadilhas: não fechar `Files.lines`/`Files.walk` (vaza file handle) → try-with-resources; `readAllLines` em arquivo gigante (OOM); paths hard-coded com separador. Fonte: Tutorial "File I/O (NIO.2)", Javadoc `Files`.
- **13 — Composição funcional e funções de alta ordem (opus).** `compose`/`andThen`, `Predicate.and`/`or`/`negate`, higher-order, captura/`effectively final`, closures, quando funcional ajuda vs atrapalha. Armadilhas: ordem de `compose` vs `andThen` invertida; pipeline funcional ilegível (extrair métodos nomeados); stack trace inútil em lambda profunda. Fonte: Javadoc `Function`/`Predicate`.
- **14 — SequencedCollection e SequencedMap (Java 21).** As interfaces (JEP 431), métodos de ponta + `reversed`, motivação, o que passou a implementá-las. **WebFetch obrigatório.** Armadilhas: `reversed()` é view (muta o original); assumir disponibilidade em Java < 21; `getFirst` em coleção vazia (`NoSuchElementException`). Fonte: JEP 431, Javadoc `SequencedCollection`.
- **15 — Collectors customizados e Gatherers (Java 24) (opus).** `Collector.of`; Stream Gatherers (`gather`, `Gatherer`, fábricas). **WebFetch obrigatório** — confirmar JEP 485/status final no Java 24 e a API exata; declarar version-specificity (hedge se preview em alguma release). Armadilhas: reinventar um Gatherer que já existe; combiner incorreto em collector (quebra em parallel); usar Gatherers numa versão que não os tem. Fonte: JEP 485, Javadoc `Gatherer`/`Gatherers`/`Collector`.
- **16 — Escolha de coleção e estilo funcional — síntese (capstone, opus).** Decision tree de coleção (Big-O consolidado); stream vs loop; funcional vs imperativo; cheatsheet; entrevista. Armadilhas (de raciocínio): escolher coleção por hábito; "tudo vira stream" (loop às vezes é mais claro/rápido); otimização prematura de estrutura. Liga o galho. Fonte: síntese das anteriores + Javadoc.

## 6. Pré-flight (executado nesta fase de brainstorming)

Como é galho de refator, o pré-flight foi **ler o tronco e confirmar o terreno** antes de escrever:

1. **Headings reais de `Core/Java Fundamentals.md` confirmados** (862 linhas). As seis seções do Galho 2 (`## Collections Framework`, `## Lambdas e Interfaces Funcionais`, `## Streams API`, `## Date/Time API`, `## I/O (Arquivos)`, `## Optional`) estão marcadas `[!info] Migra em galho futuro (Galho 2)` e mantêm corpo completo (matéria-prima da poda).
2. **Poda do Galho 1 confirmada (parcial):** as seções de linguagem (`## Sintaxe básica`, `## OOP em Java`, `## Records`, `## Sealed`, `## Pattern Matching`, `## Annotations`, `## Exceções`, `## Generics`, `## Features modernas por versão`) já são callouts `[!nota] Migrado`.
3. **`## JVM` e `## Concorrência (visão geral)` NÃO são deste galho** — JVM é Galho 3; Concorrência é dívida do Galho 4. Não tocar.
4. **Fabricação localizada:** exemplos `Patient`/`getSpecialty`/`getAge` nas seções a podar (resolvido pela poda); `## How to explain in English` em primeira pessoa fabricada (a higienizar, §3.5).
5. **Dívida de linkback do Galho 4 localizada:** notas 07 (linhas ~31, ~399) e 15 (linhas ~49, ~450) linkam `[[Java Fundamentals]]` pra base de Collections/Streams (§3.6).
6. **Verificações version-specific a fazer na execução (WebFetch):** `SequencedCollection`/`SequencedMap` (JEP 431, Java 21 — nota 14); Stream Gatherers (JEP 485, Java 24 — nota 15); `Collector.of` characteristics; `takeWhile`/`dropWhile` (Java 9); `Stream.toList()` (Java 16); `mapMulti` (Java 16); `Stream.iterate` 3-arg (Java 9).

Quando faltar fato verificável, **PERGUNTAR** antes de escrever.

## 7. Critérios de aceitação do galho

Além dos critérios gerais (§10 do roadmap):

1. 16 notas em `03-Dominios/Java/Collections e Streams/`, frontmatter completo com `fase:`, `publish: true`, distribuídas 5/7/4.
2. MOC do galho com 3 subseções de fase + 5 rotas alternativas + dataview + folder-link resolve (`index.md` presente).
3. Dicionário de Java **expandido** (não recriado) com ~24-28 verbetes em ordem alfabética; verbetes dos Galhos 1/4/5 intactos; `updated` atualizado; headings dos verbetes conferidos 1:1 com as âncoras usadas nas notas; sem duplicar verbetes pré-existentes.
4. MOC central `Java/index.md` com Galho 2 ativado (linha 26 vira wikilink); resto intacto.
5. **Poda parcial executada:** as 6 seções do Galho 2 no tronco viram callouts com wikilinks; `## JVM` e `## Concorrência` intactos; cauda `## How to explain in English` higienizada (sem primeira pessoa fabricada); `updated` do tronco atualizado.
6. **Dívida de linkback do Galho 4 quitada:** notas 07 e 15 apontam pras notas reais do Galho 2 (não mais `[[Java Fundamentals]]` pra base de Collections/Streams).
7. Cada nota: TL;DR; 3-5 code samples; "Em entrevista" com `### Frase pronta (inglês)` 3+ sentenças + 6+ termos PT→EN; "Armadilhas" com exemplo+fix (≥2 Iniciado, ≥3 Adepto/Magus); wikilinks (galho + MOC central + Galhos 1/4 quando conectar + Dicionário); "Referências" com docs oficiais.
8. Zero fabricação de experiência pessoal; exemplos neutros (`Order`/`Customer`); features version-specific verificadas via WebFetch (nada de API "de memória").
9. 1 commit por nota; sem `Co-Authored-By: Claude`; sem `--no-verify`; stage nominal; **direto na `main`, sem push**.
10. `verificar-wikilinks` roda limpo na pasta do galho e nas notas 07/15 do Galho 4 editadas (cuidado: falso-positivo em self-anchors `[[#Heading]]` — preferir não usar âncoras same-file); Quartz publica sem erros.

## 8. Riscos e mitigações

| Risco | Mitigação |
|---|---|
| Copiar tabelas/snippets do tronco como estão (incluindo `Patient`) | Notas **expandem e modernizam**, não copiam; exemplos refeitos neutros (`Order`/`Customer`); critério de aceitação exige zero fabricação. |
| Fabricação em primeira pessoa vazar do tronco (`How to explain in English`) | Higienização explícita na poda (§3.5); reescrita neutra ou remoção; critério 5/8. |
| Sobreposição com Galho 4 (parallel streams, concurrent collections) | Galho 4 é dono; Galho 2 cita e linka, não re-explica fork/join nem concurrent collections (§3.1 fronteiras); reciprocidade de links (§3.7). |
| Podar seção de outro galho por engano (JVM/Concorrência) | Pré-flight fixou que só as 6 seções marcadas "(Galho 2)" são podadas; `## JVM` (Galho 3) e `## Concorrência` (dívida Galho 4) explicitamente intocados. |
| Features version-specific erradas (Sequenced Java 21, Gatherers Java 24) | WebFetch obrigatório nas notas 14/15 (e nas afirmações de versão das demais); declarar version-specificity; hedge quando preview. |
| Gatherers (nota 15) ainda preview ou API mudou | WebFetch confirma status final (JEP 485) na release atual; se preview em alguma versão suportada, declarar com `--enable-preview` e hedge; não afirmar como estável sem fonte. |
| Galho denso (16 notas) inflar notas individuais | `JTable`-style: tópicos pesados distribuídos (Streams em 05/07/08/09/15; Collections em 01/02/03/06; funcional em 04/13); nenhuma nota vira monstro; se inflar, dividir nota, não galho. |
| Dívida de linkback do Galho 4 com linhas deslocadas | Reconfirmar as ocorrências por `grep "Java Fundamentals"` na execução (linhas podem ter mudado); editar por conteúdo, não por número de linha. |
| Duplicar verbete já existente no Dicionário | Conferir cada verbete contra o arquivo antes de inserir; nunca reordenar/recriar. |
| Quebrar wikilinks existentes pro tronco ao podar | Tronco **continua existindo** (poda = callout, não deleção); `verificar-wikilinks` roda ao fim. |

## 9. Próximos passos

1. **Aprovação deste spec**
2. **Plano de execução** via skill `superpowers:writing-plans` → `docs/superpowers/plans/2026-06-04-java-galho-02-collections-streams-execution.md`
3. **Execução** via `superpowers:subagent-driven-development` **direto na `main`** (1 subagente por nota; sonnet, opus pras notas 08/13/15/16; review **por fase** + fix loop)
4. **Poda parcial** do tronco + **quitação da dívida de linkback** do Galho 4
5. **Verificação** de wikilinks + build Quartz
6. **Revisão do roadmap** com aprendizados antes do próximo galho (Galho 3 — JVM)

## 10. Documentos relacionados

- `2026-06-02-java-senior-roadmap-design.md` — roadmap macro (18 galhos)
- `2026-06-02-java-galho-01-linguagem-design.md` / `...-execution.md` — Galho 1 (dono de interfaces/generics/records que o Galho 2 linka)
- `2026-06-03-java-galho-04-concorrencia-design.md` / `...-execution.md` — Galho 4 (dono de paralelismo/concurrent collections; alvo da quitação de linkback)
- `2026-06-03-java-galho-05-swing-design.md` / `...-execution.md` — Galho 5 (template mais recente de spec/plano)
- Tronco a podar: `03-Dominios/Java/Core/Java Fundamentals.md` (poda parcial — 6 seções)
- Artefatos a atualizar: `03-Dominios/Java/Dicionário de Java.md`, `03-Dominios/Java/index.md`, `Concorrência e paralelismo/07 - Concurrent collections.md`, `Concorrência e paralelismo/15 - Parallel streams e fork-join.md`
- Fontes-base do galho: Javadoc `java.util`/`java.util.stream`/`java.util.function`/`java.time`/`java.nio.file`, The Java Tutorials (Collections, Lambdas, Aggregate Operations, Date-Time, File I/O), `dev.java`, JEP 431 (Sequenced Collections), JEP 485 (Stream Gatherers)
- Memórias: [[project_trilha_java]], [[project_trilhas_fases_aprendizado]], [[project_tronco_galhos_pattern]], [[feedback_no_fabrication]], [[feedback_quartz_index]], [[feedback_commits]], [[feedback_galhos_direto_main]]
