# Galho 2 — Collections, Streams e Programação Funcional (Java Senior) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Criar o Galho 2 da trilha Java Senior — 16 notas atômicas (Collections Framework, Stream API, programação funcional, Optional, Date/Time, I/O moderno) em 3 fases + MOC do galho + expansão do Dicionário + ativação do MOC central + **poda parcial do tronco** `Java Fundamentals` + **quitação da dívida de linkback do Galho 4**.

**Architecture:** Padrão galhos + 3 fases (Iniciado/Adepto/Magus). Pasta flat `03-Dominios/Tecnologia/Java/Collections e Streams/`, notas atômicas `publish: true` em PT-BR, numeração global 01-16 (5 Iniciado / 7 Adepto / 4 Magus). **Galho de refator de tronco:** o monolito `Core/Java Fundamentals.md` tem 6 seções marcadas `[!info] Migra em galho futuro (Galho 2)` que são a matéria-prima — as notas **expandem e modernizam** (não copiam) e verificam features version-specific via WebFetch. Galho dono de Collections/Streams/funcional; **linka** pro Galho 4 (paralelismo, concurrent collections) e Galho 1 (interfaces, generics, records) sem re-explicar. A seção JVM fica pro Galho 3; a seção Concorrência é dívida do Galho 4 — **nenhuma das duas é tocada**. **Trabalho direto na `main`** (sem branch dedicada — ver [[feedback_galhos_direto_main]]); push é manual do usuário.

**Tech Stack:** Obsidian Flavored Markdown, frontmatter YAML, wikilinks, callouts, Dataview, Quartz v4. Verificação de fonte via WebFetch (docs.oracle.com/Javadoc, dev.java, JEPs).

---

## Convenções aplicadas a TODAS as notas (ler antes de qualquer task)

**Frontmatter** (ajustar `title`/`fase`/`tags`/`aliases` por nota; `created`/`updated: 2026-06-04`):

```yaml
---
title: "<título sem prefixo numérico>"
created: 2026-06-04
updated: 2026-06-04
type: concept
progress: backlog
status: seedling
publish: true
fase: iniciado | adepto | magus
tags:
  - java
  - collections
  - <fase>
  - <1-3 tags de conceito>
aliases:
  - <aliases>
---
```

**Estrutura H2 obrigatória** (nesta ordem):

1. `> [!abstract] TL;DR` — 2-4 linhas (conceito central + regra prática + por que importa). Callout, NÃO H2.
2. `## O que é` — definição.
3. `## Por que importa` — relevância pra senior/entrevista. (Pode fundir com "O que é" em notas Iniciado curtas.)
4. `## Como funciona` — H3s; mínimo 3 subseções em notas Adepto/Magus.
5. `## Na prática` — exemplos compiláveis, framing neutro ("padrão observado no JDK / no ecossistema", "caso típico em serviço enterprise", hipotético explícito `// hipotético:`). **NUNCA** "no meu projeto"; **NUNCA** `Patient`/`getSpecialty` (sabor MedEspecialista do tronco). Domínios neutros: `Order`, `Customer`, `Product`, `Employee`.
6. `## Armadilhas` — ≥2 (Iniciado) / ≥3 (Adepto/Magus). Cada armadilha: `### (N) Título` + descrição + exemplo curto de código demonstrando o problema + fix em 1 linha.
7. `## Em entrevista` — subheading `### Frase pronta (inglês)` com frase de **3+ sentenças** (trade-off + decisão + caveat) + sub-bloco "Vocabulário" com **6+ termos PT→EN** traduzidos.
8. `## Veja também` — wikilinks SEM backticks. Sempre inclui: notas relacionadas do galho + `[[03-Dominios/Tecnologia/Java/Collections e Streams/index|Collections e Streams (MOC do galho)]]` + `[[03-Dominios/Tecnologia/Java/index|Trilha Java]]` + (quando o conceito conectar) `[[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Concorrência]]` / `[[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/index|Linguagem]]` + verbetes do Dicionário relevantes.
9. `## Referências` — docs oficiais (Javadoc, The Java Tutorials, dev.java) + (quando pertinente) JEPs.

**Tamanho:** 200-500 linhas (notas Magus densas até 700).

**Restrições absolutas** (qualquer violação reprova a nota):
- **Conteúdo herdado do tronco é matéria-prima, não cópia.** O tronco tem o esqueleto certo, mas a nota **expande e moderniza**. **Toda afirmação version-specific é verificada via WebFetch antes de afirmar** — nada de API "de memória". Toda nota tem "Referências".
- Sem fabricação de experiência pessoal. Exemplos: `Order`, `Customer`, `Product`, ou `// hipotético: ...`. NUNCA `josenaldo`/caminhos pessoais/casos vividos/`Patient`.
- Comparações justas ("quando X vence" E "quando Y vence") — `ArrayList` vs `LinkedList`, `HashMap` vs `TreeMap`, stream vs loop, funcional vs imperativo, `collect` vs `reduce`.
- **Não re-explicar o que é de outro galho.** Paralelismo/concurrent collections → Galho 4 (linkar). Interfaces/generics/records/exceções → Galho 1 (linkar). JVM/GC → Galho 3 (texto "planejado", **sem wikilink** — não existe ainda).
- Code fences: ` ```java ` pra código, ` ```text ` pra output. Sempre fechadas.
- Commits: sem `Co-Authored-By: Claude`; sem `--no-verify`; `git add <path>` nominal (nunca `git add -A`); 1 commit por nota; **direto na `main`**; **sem push**.

**Material de origem:** tronco `03-Dominios/Tecnologia/Java/Core/Java Fundamentals.md` (seções "(Galho 2)") como matéria-prima. Spec de referência: `docs/superpowers/specs/2026-06-04-java-galho-02-collections-streams-design.md` §5. Template de qualidade: notas dos Galhos 1/4/5 em `03-Dominios/Tecnologia/Java/`.

**Modelo por nota:** sonnet por padrão; **opus** nas notas **08** (Collectors), **13** (Composição funcional), **15** (Gatherers) e **16** (capstone) — as mais densas/sensíveis.

**Fontes oficiais (base por área):** Tutorial Collections `https://docs.oracle.com/javase/tutorial/collections/`; Lambdas `https://docs.oracle.com/javase/tutorial/java/javaOO/lambdaexpressions.html`; Streams `https://docs.oracle.com/javase/tutorial/collections/streams/`; Date-Time `https://docs.oracle.com/javase/tutorial/datetime/`; File I/O `https://docs.oracle.com/javase/tutorial/essential/io/fileio.html`; `https://dev.java/`; Javadoc Java 21 `https://docs.oracle.com/en/java/javase/21/docs/api/`. JEPs: 431 (`https://openjdk.org/jeps/431`), 485 (`https://openjdk.org/jeps/485`).

---

## Task 0: Pré-flight — pasta e confirmação do terreno (tronco já lido na brainstorming)

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Collections e Streams/` (pasta)

- [ ] **Step 1: Confirmar que está na `main`**

```bash
git branch --show-current
```
Expected: `main`. (Galho 2 é executado direto na main — ver [[feedback_galhos_direto_main]]. NÃO criar branch.)

- [ ] **Step 2: Criar a pasta do galho**

```bash
mkdir -p "03-Dominios/Tecnologia/Java/Collections e Streams"
```

- [ ] **Step 3: Reconfirmar as seções do tronco a podar (matéria-prima)**

```bash
grep -nE '^## (Collections Framework|Lambdas e Interfaces Funcionais|Streams API|Date/Time API|I/O \(Arquivos\)|Optional)' "03-Dominios/Tecnologia/Java/Core/Java Fundamentals.md"
grep -n "Migra em galho futuro (Galho 2)" "03-Dominios/Tecnologia/Java/Core/Java Fundamentals.md"
```
Expected: as 6 seções existem e estão marcadas `[!info] Migra em galho futuro (Galho 2)`. (Já confirmado na brainstorming; reconfirmar pois linhas podem ter mudado.) **NÃO** tocar `## JVM` (Galho 3) nem `## Concorrência (visão geral)` (dívida Galho 4).

- [ ] **Step 4: Reconfirmar as ocorrências da dívida de linkback do Galho 4**

```bash
grep -rn "Java Fundamentals" "03-Dominios/Tecnologia/Java/Concorrência e paralelismo/"
```
Expected: ver as linhas em `07 - Concurrent collections.md` e `15 - Parallel streams e fork-join.md` (base de Collections/Streams) — alvos da Task 21. As ocorrências em `11 - Java Memory Model` e `12 - Virtual Threads` são referência geral ao tronco (NÃO mexer).

- [ ] **Step 5: Fixar versões assumidas**

Baseline: **Java 21 LTS** / **Java 25 LTS**. Features a verificar version-specificity na execução: `SequencedCollection` (Java 21), Stream Gatherers (Java 24), `takeWhile`/`dropWhile`/`Stream.iterate` 3-arg (Java 9), `Stream.toList()`/`mapMulti`/`Collectors.teeing` (Java 16/12), `List.of`/`Map.of` (Java 9).

- [ ] **Step 6: Sem commit** (task de preparação).

---

## Fase INICIADO (notas 01-05)

### Task 1: Nota 01 — O Collections Framework

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Collections e Streams/01 - O Collections Framework.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch `https://docs.oracle.com/javase/tutorial/collections/intro/index.html` (Introduction to Collections) e `https://dev.java/learn/api/collections-framework/` (overview). Confirmar a hierarquia `Iterable`→`Collection`→`List`/`Set`/`Queue` e `Map` fora dela; conferir `List.of`/`Set.of`/`Map.of` (Java 9) no Javadoc.

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: iniciado`, tags `[java, collections, iniciado, framework]`, aliases `["Collections Framework", "Coleções em Java"]`.

Conteúdo:
- TL;DR: o Collections Framework = conjunto de interfaces (`List`/`Set`/`Queue`/`Map`) + implementações reutilizáveis; escolher a interface certa antes da implementação.
- `## O que é` — o que é o framework; `Iterable`→`Collection`; por que `Map` **não** é `Collection`.
- `## Por que importa` — escolher a estrutura certa é decisão de senior; entrevista cobra a hierarquia e os trade-offs.
- `## Como funciona` — H3s: "A hierarquia (`Iterable`/`Collection`/`List`/`Set`/`Queue`/`Map`)", "A API comum de `Collection` (`add`/`remove`/`contains`/`size`/`iterator`/`stream`)", "Coleções imutáveis (`List.of`/`Set.of`/`Map.of`, Java 9) vs views (`Collections.unmodifiableList`)", "Coleções thread-safe existem (`ConcurrentHashMap` etc.) — **dono é o Galho 4**".
- `## Na prática` — criar `List`/`Set`/`Map` de `Order`; iterar; uma coleção imutável.
- `## Armadilhas` — ≥2: (1) `List.of(...)` é imutável → `add` lança `UnsupportedOperationException`; (2) `Collections.unmodifiableList(x)` é **view** (mutar `x` ainda afeta) → copiar antes se precisar isolar; (3) `Arrays.asList(...)` tem tamanho fixo. Exemplo + fix.
- `## Em entrevista` (`### Frase pronta (inglês)`) + `## Veja também` (02, 03, 06, MOC galho, MOC central, `[[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/12 - Generics em profundidade|Generics]]`, `[[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/07 - Concurrent collections|Concurrent collections]]`, verbetes `Collections Framework`) + `## Referências`.

Tamanho: 220-340 linhas (abertura).

- [ ] **Step 3: Verificar**

```bash
grep -cE "^## (O que é|Como funciona|Armadilhas|Em entrevista|Veja também|Referências)" "03-Dominios/Tecnologia/Java/Collections e Streams/01 - O Collections Framework.md"
grep -E "Iterable|Collection|List.of|unmodifiable" "03-Dominios/Tecnologia/Java/Collections e Streams/01 - O Collections Framework.md" | head
```
Expected: grep de seções ≥6; cobre hierarquia + imutáveis.

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/Collections e Streams/01 - O Collections Framework.md"
git commit -m "feat(java): galho 2 nota 01 — o Collections Framework"
```

---

### Task 2: Nota 02 — Listas, conjuntos e filas

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Collections e Streams/02 - Listas, conjuntos e filas.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch `https://docs.oracle.com/javase/tutorial/collections/implementations/index.html` (Implementations) + Javadoc de `ArrayList`, `LinkedList`, `HashSet`, `TreeSet`, `ArrayDeque`, `PriorityQueue` (Java 21). Confirmar estrutura interna e complexidade (Big-O) de cada.

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: iniciado`, tags `[java, collections, iniciado, list, set, queue]`, aliases `["ArrayList", "HashSet", "ArrayDeque"]`.

Conteúdo:
- `## O que é` — as três famílias de `Collection`: `List` (ordenada, índice), `Set` (sem duplicatas), `Queue`/`Deque` (pontas).
- `## Como funciona` — H3s: "`ArrayList` (array dinâmico, acesso O(1), inserção amortizada) vs `LinkedList` (lista duplamente ligada)", "`HashSet`/`LinkedHashSet`/`TreeSet` (dedup, ordem de inserção, Red-Black tree)", "`Queue`/`Deque`: `ArrayDeque` (FIFO/LIFO, substitui `Stack`/`Vector`) e `PriorityQueue` (binary heap, top-K)", "Complexidade comparada (tabela Big-O)".
- `## Na prática` — escolher `ArrayList` pra acesso por índice; `ArrayDeque` como pilha; `PriorityQueue` pra top-K de `Order` por valor.
- `## Armadilhas` — ≥2: (1) usar `LinkedList` por reflexo (quase sempre `ArrayList` ganha — cache locality) → medir antes; (2) `contains` em `ArrayList` é O(n) → `HashSet` se busca é frequente; (3) `TreeSet` exige `Comparable` ou `Comparator` (senão `ClassCastException`). Exemplo + fix.
- `## Em entrevista` + `## Veja também` (01, 03, 06, MOC, central, `[[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/07 - Concurrent collections|Concurrent collections]]`, verbetes `Deque`/`PriorityQueue`) + `## Referências`.

Tamanho: 280-420 linhas.

- [ ] **Step 3: Verificar**

```bash
grep -E "ArrayList|LinkedList|HashSet|TreeSet|ArrayDeque|PriorityQueue|O\(1\)|O\(n\)" "03-Dominios/Tecnologia/Java/Collections e Streams/02 - Listas, conjuntos e filas.md" | head
```

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/Collections e Streams/02 - Listas, conjuntos e filas.md"
git commit -m "feat(java): galho 2 nota 02 — listas, conjuntos e filas"
```

---

### Task 3: Nota 03 — Mapas

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Collections e Streams/03 - Mapas.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch Javadoc `HashMap`, `LinkedHashMap`, `TreeMap`, `NavigableMap`, `Map` (Java 21) e `https://dev.java/learn/api/collections-framework/maps/`. Confirmar o contrato `hashCode`/`equals`, a treeification de bucket (Java 8+) e a API (`merge`/`compute`/`getOrDefault`).

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: iniciado`, tags `[java, collections, iniciado, map]`, aliases `["HashMap", "TreeMap", "Mapas"]`.

Conteúdo:
- `## O que é` — `Map<K,V>`: associação chave→valor; chaves únicas.
- `## Como funciona` — H3s: "`HashMap` por dentro (buckets, função de hash, **contrato `hashCode`/`equals`**, treeification de bucket em colisão alta — Java 8+)", "`LinkedHashMap` (ordem de inserção/acesso; base de cache LRU)", "`TreeMap`/`NavigableMap` (ordenado, `floorKey`/`ceilingKey`)", "A API rica (`getOrDefault`/`putIfAbsent`/`merge`/`compute`/`computeIfAbsent`/`forEach`)".
- `## Na prática` — contar ocorrências com `merge`; agrupar manualmente com `computeIfAbsent`; `TreeMap` pra ranges.
- `## Armadilhas` — ≥2: (1) `hashCode`/`equals` inconsistentes (ou mutar a chave após inserir) → chave "some" do mapa; usar chave imutável (record); (2) `HashMap` em acesso concorrente (corrompe/loop) → `ConcurrentHashMap` (Galho 4); (3) `get` retorna `null` ambíguo (ausente vs valor null) → `getOrDefault`/`containsKey`. Exemplo + fix.
- `## Em entrevista` + `## Veja também` (01, 02, 06, MOC, central, `[[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/13 - Records e record patterns|Records]]` (chave imutável), `[[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/07 - Concurrent collections|Concurrent collections]]`, verbetes `hashCode / equals (contrato)`/`treeification`) + `## Referências`.

Tamanho: 300-440 linhas.

- [ ] **Step 3: Verificar**

```bash
grep -E "HashMap|hashCode|equals|TreeMap|LinkedHashMap|merge|computeIfAbsent|treeif" "03-Dominios/Tecnologia/Java/Collections e Streams/03 - Mapas.md" | head
```

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/Collections e Streams/03 - Mapas.md"
git commit -m "feat(java): galho 2 nota 03 — mapas"
```

---

### Task 4: Nota 04 — Lambdas e interfaces funcionais

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Collections e Streams/04 - Lambdas e interfaces funcionais.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch `https://docs.oracle.com/javase/tutorial/java/javaOO/lambdaexpressions.html` (Lambda Expressions) + Javadoc `java.util.function` (Java 21) + `https://docs.oracle.com/javase/tutorial/java/javaOO/methodreferences.html` (Method References). Confirmar a noção SAM e as 4 interfaces centrais + variantes.

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: iniciado`, tags `[java, collections, iniciado, funcional, lambda]`, aliases `["Lambda", "Interface funcional", "Function Predicate Consumer Supplier"]`.

Conteúdo:
- `## O que é` — lambda = implementação anônima e concisa de uma interface funcional (SAM — single abstract method).
- `## Por que importa` — base de Streams, Optional, callbacks; entrevista cobra as interfaces do `java.util.function`.
- `## Como funciona` — H3s: "Sintaxe lambda (vs classe anônima)", "`@FunctionalInterface` e o conceito SAM", "As quatro centrais: `Function<T,R>`/`Predicate<T>`/`Consumer<T>`/`Supplier<T>`", "Variantes (`BiFunction`, `UnaryOperator`, `BiPredicate`) e especializações primitivas (`IntFunction`, `ToIntFunction`, `IntPredicate`)", "Method references (estático `Integer::parseInt`, de instância de tipo `String::toUpperCase`, de objeto `System.out::println`, construtor `ArrayList::new`)". **Linka Galho 1 (08 Interfaces)** pra mecânica — não re-explica.
- `## Na prática` — `Predicate<Order>` de filtro; `Function<Order,String>` de extração; method reference em `forEach`.
- `## Armadilhas` — ≥2: (1) lambda capturando variável **não** `effectively final` (não compila) → tornar final/copiar; (2) criar interface funcional própria onde já existe uma no JDK → reusar `Function`/`Predicate`; (3) method reference ambíguo (instância vs estático) → desambiguar com lambda. Exemplo + fix.
- `## Em entrevista` + `## Veja também` (05, 07, 13, 10, MOC, central, `[[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/08 - Interfaces e classes abstratas|Interfaces e classes abstratas]]`, verbetes `lambda`/`interface funcional`/`Function / Predicate / Consumer / Supplier`/`method reference`) + `## Referências`.

Tamanho: 300-440 linhas.

- [ ] **Step 3: Verificar**

```bash
grep -E "FunctionalInterface|Function|Predicate|Consumer|Supplier|::|effectively final" "03-Dominios/Tecnologia/Java/Collections e Streams/04 - Lambdas e interfaces funcionais.md" | head
```

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/Collections e Streams/04 - Lambdas e interfaces funcionais.md"
git commit -m "feat(java): galho 2 nota 04 — lambdas e interfaces funcionais"
```

---

### Task 5: Nota 05 — Introdução à Stream API

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Collections e Streams/05 - Introdução à Stream API.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch `https://docs.oracle.com/javase/tutorial/collections/streams/index.html` (Aggregate Operations) + Javadoc `java.util.stream` (package summary — descreve lazy/terminal/short-circuit). Confirmar que stream não é estrutura de dados, é consumível uma vez, e a separação lazy/eager.

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: iniciado`, tags `[java, collections, iniciado, streams]`, aliases `["Stream API", "Stream", "Pipeline"]`.

Conteúdo:
- `## O que é` — stream = sequência de elementos + pipeline de operações; **não** é estrutura de dados (não armazena).
- `## Por que importa` — estilo declarativo de processar coleções; substitui loops imperativos; entrevista cobra lazy vs eager.
- `## Como funciona` — H3s: "Anatomia: source → intermediárias (**lazy**) → terminal (**eager**)", "Avaliação preguiçosa e curto-circuito (nada roda até a terminal)", "Stream vs Collection (processamento vs armazenamento)", "Stream vs loop (quando cada um)", "Stream é consumível uma vez". Menciona `parallelStream`/`.parallel()` como existência → **linka Galho 4 (15)** pro paralelismo, **não** explica fork/join.
- `## Na prática` — `orders.stream().filter(...).map(...).toList()` simples; mostrar que sem terminal nada executa.
- `## Armadilhas` — ≥2: (1) reusar um stream já consumido (`IllegalStateException: stream has already been operated upon`) → criar novo; (2) achar que intermediárias executam sozinhas (são lazy) → precisa de terminal; (3) efeito colateral em `map`/`peek` (não confiável). Exemplo + fix.
- `## Em entrevista` + `## Veja também` (04, 07, 08, 09, MOC, central, `[[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/15 - Parallel streams e fork-join|Parallel streams]]`, verbetes `Stream`/`operação intermediária / terminal`/`stream lazy (avaliação preguiçosa)`) + `## Referências`.

Tamanho: 280-400 linhas.

- [ ] **Step 3: Verificar**

```bash
grep -E "lazy|eager|terminal|intermediári|curto-circuito|parallelStream|consumível" "03-Dominios/Tecnologia/Java/Collections e Streams/05 - Introdução à Stream API.md" | head
```

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/Collections e Streams/05 - Introdução à Stream API.md"
git commit -m "feat(java): galho 2 nota 05 — introdução à Stream API"
```

---

## Fase ADEPTO (notas 06-12)

### Task 6: Nota 06 — Comparable e Comparator

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Collections e Streams/06 - Comparable e Comparator.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch Javadoc `Comparable` e `Comparator` (Java 21) + `https://dev.java/learn/api/collections-framework/sorting/`. Confirmar os combinadores (`comparing`/`thenComparing`/`reversed`/`nullsFirst`/`nullsLast`) e o contrato de consistência com `equals`.

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: adepto`, tags `[java, collections, adepto, comparator, ordenacao]`, aliases `["Comparable", "Comparator", "Ordenação"]`.

Conteúdo:
- `## O que é` — `Comparable` (ordem natural, dentro da classe) vs `Comparator` (ordem externa, plugável).
- `## Como funciona` — H3s: "`Comparable<T>.compareTo` (contrato: -/0/+; consistência com `equals`)", "`Comparator` e os combinadores (`comparing`/`comparingInt`/`thenComparing`/`reversed`)", "Nulos (`nullsFirst`/`nullsLast`)", "Ordenar `List` (`sort`) e streams (`sorted`)".
- `## Na prática` — ordenar `List<Order>` por valor e depois por data com `thenComparing`; `Comparator.comparing(Order::customer).reversed()`.
- `## Armadilhas` — ≥3: (1) `compareTo`/`Comparator` inconsistente com `equals` → `TreeSet`/`TreeMap` "perde" elementos iguais segundo o comparador; (2) `a - b` pra comparar int (overflow) → `Integer.compare(a,b)`; (3) esquecer `nullsFirst` com campos nuláveis (`NullPointerException`). Exemplo + fix.
- `## Em entrevista` + `## Veja também` (01, 02, 07, MOC, central, `[[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/13 - Records e record patterns|Records]]`, verbetes `Comparable`/`Comparator`) + `## Referências`.

Tamanho: 260-400 linhas.

- [ ] **Step 3: Verificar**

```bash
grep -E "Comparable|Comparator|compareTo|thenComparing|reversed|nullsFirst|Integer.compare" "03-Dominios/Tecnologia/Java/Collections e Streams/06 - Comparable e Comparator.md" | head
```

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/Collections e Streams/06 - Comparable e Comparator.md"
git commit -m "feat(java): galho 2 nota 06 — Comparable e Comparator"
```

---

### Task 7: Nota 07 — Operações de Stream: intermediárias e terminais

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Collections e Streams/07 - Operações de Stream — intermediárias e terminais.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch Javadoc `java.util.stream.Stream` (Java 21) — lista de métodos. Confirmar `takeWhile`/`dropWhile` (Java 9), `mapMulti` (Java 16), `toList()` (Java 16) e a semântica de cada operação.

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: adepto`, tags `[java, collections, adepto, streams]`, aliases `["Operações de stream", "map filter reduce", "flatMap"]`.

Conteúdo:
- `## O que é` — o catálogo de operações: intermediárias (transformam o stream, lazy) e terminais (produzem resultado/efeito, eager).
- `## Como funciona` — H3s: "Intermediárias de transformação (`map`/`mapToObj`/`flatMap`/`mapMulti`)", "Intermediárias de filtragem/fatiamento (`filter`/`distinct`/`sorted`/`limit`/`skip`/`takeWhile`/`dropWhile`/`peek`)", "Terminais de coleta/redução (`toList`/`collect`/`reduce`/`count`/`min`/`max`)", "Terminais de busca/match (curto-circuito: `findFirst`/`findAny`/`anyMatch`/`allMatch`/`noneMatch`)", "Terminais de iteração (`forEach`/`forEachOrdered`)".
- `## Na prática` — pipeline `orders.stream().filter(...).map(...).sorted(...).limit(5).toList()`; `flatMap` achatando `List<Order>` → itens.
- `## Armadilhas` — ≥3: (1) `peek` pra lógica (não garantido executar — só debug) → mover pra `map`/`forEach`; (2) `sorted()` sem `Comparator` em tipo não-`Comparable` (`ClassCastException`) → passar `Comparator`; (3) `forEach` mutando coleção externa (quebra em paralelo) → `collect`. Exemplo + fix.
- `## Em entrevista` + `## Veja também` (05, 08, 09, MOC, central, `[[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/15 - Parallel streams e fork-join|Parallel streams]]`, verbetes `operação intermediária / terminal`) + `## Referências`.

Tamanho: 320-460 linhas.

- [ ] **Step 3: Verificar**

```bash
grep -E "map|filter|flatMap|takeWhile|dropWhile|reduce|findFirst|anyMatch|peek" "03-Dominios/Tecnologia/Java/Collections e Streams/07 - Operações de Stream — intermediárias e terminais.md" | head
```

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/Collections e Streams/07 - Operações de Stream — intermediárias e terminais.md"
git commit -m "feat(java): galho 2 nota 07 — operações de stream (intermediárias e terminais)"
```

---

### Task 8: Nota 08 — Collectors e agrupamento  ⟦opus⟧

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Collections e Streams/08 - Collectors e agrupamento.md`

- [ ] **Step 1: Pesquisar fonte (usar modelo opus)**

WebFetch Javadoc `java.util.stream.Collectors` (Java 21) + `https://docs.oracle.com/javase/tutorial/collections/streams/reduction.html` (Reduction). Confirmar `groupingBy` (com downstream), `partitioningBy`, `toMap` (merge function), `collectingAndThen`, `teeing` (Java 12), e a diferença `collect` (mutável) vs `reduce` (imutável).

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: adepto`, tags `[java, collections, adepto, streams, collectors]`, aliases `["Collectors", "groupingBy", "toMap"]`.

Conteúdo:
- `## O que é` — `Collector`: receita de redução mutável que a terminal `collect` executa; a "caixa de ferramentas" de `Collectors`.
- `## Por que importa` — agrupamento/sumarização declarativos; o tópico de stream que mais cai em entrevista depois das operações básicas.
- `## Como funciona` — H3s: "Coletar em coleção (`toList`/`toUnmodifiableList`/`toSet`/`toCollection`)", "`toMap` e o **merge function** (chave duplicada)", "`joining` (concatenar strings)", "**`groupingBy`** e os downstream collectors (`counting`/`summingInt`/`averagingDouble`/`mapping`/`toList`)", "`partitioningBy` (predicado → 2 grupos)", "`collectingAndThen`/`reducing`", "`collect` (mutável) vs `reduce` (imutável)".
- `## Na prática` — `groupingBy(Order::status, counting())`; `groupingBy(Order::customer, mapping(Order::id, toList()))`; relatório top-5 com `entrySet().stream()`.
- `## Armadilhas` — ≥3: (1) `toMap` com chave duplicada (`IllegalStateException`) → passar merge function `(a,b)->a`; (2) assumir que o mapa de `groupingBy` é imutável (é mutável) → `toUnmodifiableList` no downstream se precisa; (3) downstream collector errado (ex: `counting` retorna `Long`, não `Integer`). Exemplo + fix.
- `## Em entrevista` + `## Veja também` (05, 07, 09, 15, MOC, central, verbetes `Collector (coletor)`/`groupingBy`) + `## Referências`.

Tamanho: 340-500 linhas (densa; opus).

- [ ] **Step 3: Verificar**

```bash
grep -E "Collectors|groupingBy|partitioningBy|toMap|collectingAndThen|downstream|merge" "03-Dominios/Tecnologia/Java/Collections e Streams/08 - Collectors e agrupamento.md" | head
```

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/Collections e Streams/08 - Collectors e agrupamento.md"
git commit -m "feat(java): galho 2 nota 08 — collectors e agrupamento"
```

---

### Task 9: Nota 09 — Streams primitivos

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Collections e Streams/09 - Streams primitivos.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch Javadoc `IntStream`, `LongStream`, `DoubleStream`, `IntSummaryStatistics` (Java 21). Confirmar `range`/`rangeClosed`, `mapToInt`/`mapToObj`/`boxed`, `summaryStatistics`.

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: adepto`, tags `[java, collections, adepto, streams, primitivos]`, aliases `["IntStream", "Streams primitivos", "Summary statistics"]`.

Conteúdo:
- `## O que é` — `IntStream`/`LongStream`/`DoubleStream`: streams especializados que evitam boxing.
- `## Como funciona` — H3s: "Criação (`range`/`rangeClosed`/`of`/`iterate`/`Arrays.stream`)", "Conversões (`mapToInt`/`mapToObj`/`boxed`/`asLongStream`)", "Operações numéricas (`sum`/`average`/`min`/`max` → `OptionalInt`/`OptionalDouble`)", "`summaryStatistics()` (`IntSummaryStatistics`: count/sum/min/max/average de uma vez)", "Custo de boxing/unboxing e quando o ganho compensa".
- `## Na prática` — média de idade com `mapToInt(Order::quantity).average()`; `IntStream.rangeClosed(1,100).sum()`; `summaryStatistics`.
- `## Armadilhas` — ≥3: (1) `Stream<Integer>` onde `IntStream` serve (boxing em volume) → `mapToInt`; (2) esquecer `boxed()` ao precisar de `Stream<Integer>` pra um collector; (3) `average()` retorna `OptionalDouble` (não `double`) → `.orElse(0.0)`. Exemplo + fix.
- `## Em entrevista` + `## Veja também` (05, 07, 08, MOC, central, verbetes `stream primitivo (IntStream)`/`boxing / unboxing`) + `## Referências`.

Tamanho: 260-380 linhas.

- [ ] **Step 3: Verificar**

```bash
grep -E "IntStream|LongStream|mapToInt|boxed|summaryStatistics|OptionalDouble|boxing" "03-Dominios/Tecnologia/Java/Collections e Streams/09 - Streams primitivos.md" | head
```

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/Collections e Streams/09 - Streams primitivos.md"
git commit -m "feat(java): galho 2 nota 09 — streams primitivos"
```

---

### Task 10: Nota 10 — Optional

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Collections e Streams/10 - Optional.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch Javadoc `java.util.Optional` (Java 21) + `https://dev.java/learn/api/optional/` (ou The Java Tutorials sobre Optional). Confirmar `of`/`ofNullable`/`empty`, `map`/`flatMap`/`filter`, `orElse`/`orElseGet`/`orElseThrow`, `ifPresentOrElse` (Java 9), `stream()` (Java 9).

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: adepto`, tags `[java, collections, adepto, optional, funcional]`, aliases `["Optional", "Optional Java"]`.

Conteúdo:
- `## O que é` — `Optional<T>`: container que pode conter ou não um valor; comunica ausência no tipo de retorno (alternativa a `null`).
- `## Por que importa` — reduz NPE; documenta ausência possível; entrevista cobra o uso correto vs anti-patterns.
- `## Como funciona` — H3s: "Criação (`of`/`ofNullable`/`empty`)", "Transformação (`map`/`flatMap`/`filter`)", "Consumo (`orElse`/`orElseGet`/`orElseThrow`/`ifPresent`/`ifPresentOrElse`)", "`Optional` em streams (`stream()`, `flatMap`)", "`orElse` vs `orElseGet` (eager vs lazy)".
- `## Na prática` — `findById(id).map(Order::total).orElse(0)`; `orElseThrow(() -> new OrderNotFoundException(id))`.
- `## Armadilhas` — ≥3: (1) `Optional` como **campo de classe ou parâmetro de método** (anti-pattern — só retorno); (2) `get()` cru ou `isPresent()`+`get()` (derrota o propósito) → `map`/`orElse`; (3) `orElse(expensive())` sempre avalia o argumento → `orElseGet(() -> expensive())`; (4) `Optional.of(null)` → NPE; usar `ofNullable`. Exemplo + fix.
- `## Em entrevista` + `## Veja também` (04, 07, 13, MOC, central, verbetes `Optional`) + `## Referências`.

Tamanho: 280-400 linhas.

- [ ] **Step 3: Verificar**

```bash
grep -E "Optional|ofNullable|orElseGet|orElseThrow|ifPresentOrElse|flatMap" "03-Dominios/Tecnologia/Java/Collections e Streams/10 - Optional.md" | head
```

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/Collections e Streams/10 - Optional.md"
git commit -m "feat(java): galho 2 nota 10 — Optional"
```

---

### Task 11: Nota 11 — java.time (Date/Time API)

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Collections e Streams/11 - java.time — Date e Time API.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch `https://docs.oracle.com/javase/tutorial/datetime/index.html` (Date Time trail) + Javadoc `java.time` (`LocalDate`/`LocalDateTime`/`ZonedDateTime`/`Instant`/`Duration`/`Period`/`DateTimeFormatter`). Confirmar imutabilidade e a regra de qual tipo usar.

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: adepto`, tags `[java, collections, adepto, datetime, java-time]`, aliases `["java.time", "LocalDate", "Date Time API"]`.

Conteúdo:
- `## O que é` — `java.time` (JSR-310, Java 8): API moderna de data/hora, **imutável e thread-safe**, que substitui `Date`/`Calendar`.
- `## Por que importa` — manipulação de datas é onipresente; o legado `Date`/`SimpleDateFormat` é fonte clássica de bug; entrevista cobra `Instant` vs `LocalDateTime`.
- `## Como funciona` — H3s: "Tipos sem timezone (`LocalDate`/`LocalTime`/`LocalDateTime`)", "Tipos com timezone (`ZonedDateTime`/`OffsetDateTime`) e `Instant` (UTC, para persistência)", "`Duration` (baseado em tempo) vs `Period` (baseado em datas)", "Formatação/parsing (`DateTimeFormatter`)", "Imutabilidade (operações retornam nova instância)".
- `## Na prática` — `LocalDate.now().plusWeeks(1)`; `Duration.between(start, end)`; formatar com `DateTimeFormatter.ofPattern`.
- `## Armadilhas` — ≥3: (1) usar `Date`/`Calendar`/`SimpleDateFormat` (legado, mutável, `SimpleDateFormat` não é thread-safe) → `java.time`; (2) confundir `Duration` (horas/segundos) com `Period` (anos/meses/dias); (3) `LocalDateTime` para timestamp persistido (perde timezone) → `Instant`. Exemplo + fix.
- `## Em entrevista` + `## Veja também` (MOC, central, verbetes `LocalDate / LocalDateTime`/`Instant`/`Duration / Period`) + `## Referências`.

Tamanho: 280-420 linhas.

- [ ] **Step 3: Verificar**

```bash
grep -E "LocalDate|LocalDateTime|ZonedDateTime|Instant|Duration|Period|DateTimeFormatter|imutáv" "03-Dominios/Tecnologia/Java/Collections e Streams/11 - java.time — Date e Time API.md" | head
```

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/Collections e Streams/11 - java.time — Date e Time API.md"
git commit -m "feat(java): galho 2 nota 11 — java.time (Date/Time API)"
```

---

### Task 12: Nota 12 — I/O moderno com java.nio.file

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Collections e Streams/12 - I-O moderno com java.nio.file.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch `https://docs.oracle.com/javase/tutorial/essential/io/fileio.html` (File I/O NIO.2) + Javadoc `java.nio.file.Files`/`Path`. Confirmar `readString`/`lines`/`writeString`/`walk` e o contrato de fechamento dos streams de `Files.lines`/`Files.walk`.

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: adepto`, tags `[java, collections, adepto, io, nio]`, aliases `["java.nio.file", "Files", "Path", "I/O moderno"]`.

Conteúdo:
- `## O que é` — `java.nio.file` (NIO.2, Java 7): API moderna de arquivos (`Path` + `Files`), preferida ao legado `java.io.File`.
- `## Como funciona` — H3s: "`Path` e `Files` (a dupla central)", "Ler (`readString`/`readAllLines`/`lines`) e escrever (`writeString`/`write`)", "Operações de diretório (`exists`/`createDirectories`/`list`/`walk`)", "**Try-with-resources** e `AutoCloseable` (link Galho 1, 10 Exceções)", "Streaming de arquivos grandes (`Files.lines` retorna `Stream<String>` — fechar!)".
- `## Na prática` — ler um arquivo inteiro (`readString`); processar um CSV grande linha-a-linha com `Files.lines` dentro de try-with-resources.
- `## Armadilhas` — ≥3: (1) não fechar o `Stream` de `Files.lines`/`Files.walk` (vaza file handle) → try-with-resources; (2) `readAllLines`/`readString` em arquivo gigante (OOM) → `Files.lines` streaming; (3) montar path com separador hard-coded (`"a/b"`) → `Path.of("a","b")`. Exemplo + fix.
- `## Em entrevista` + `## Veja também` (05, 07, MOC, central, `[[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/10 - Exceções e tratamento de erros|Exceções]]` (try-with-resources), verbetes `java.nio.file (Path / Files)`/`try-with-resources`) + `## Referências`.

Tamanho: 280-400 linhas.

- [ ] **Step 3: Verificar**

```bash
grep -E "java.nio.file|Files|Path|readString|Files.lines|try-with-resources|AutoCloseable|walk" "03-Dominios/Tecnologia/Java/Collections e Streams/12 - I-O moderno com java.nio.file.md" | head
```

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/Collections e Streams/12 - I-O moderno com java.nio.file.md"
git commit -m "feat(java): galho 2 nota 12 — I/O moderno com java.nio.file"
```

---

## Fase MAGUS (notas 13-16)

### Task 13: Nota 13 — Composição funcional e funções de alta ordem  ⟦opus⟧

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Collections e Streams/13 - Composição funcional e funções de alta ordem.md`

- [ ] **Step 1: Pesquisar fonte (usar modelo opus)**

WebFetch Javadoc `Function` (`compose`/`andThen`/`identity`), `Predicate` (`and`/`or`/`negate`/`isEqual`), `Consumer` (`andThen`) (Java 21). Confirmar a ordem de execução de `compose` vs `andThen`.

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: magus`, tags `[java, collections, magus, funcional, composicao]`, aliases `["Composição de funções", "Funções de alta ordem", "compose andThen"]`.

Conteúdo:
- `## O que é` — compor funções pequenas em pipelines; funções de alta ordem (recebem/retornam funções).
- `## Por que importa` — reuso e legibilidade declarativa; mas tem custo (debug, stack traces) — decisão de senior saber quando aplicar.
- `## Como funciona` — H3s: "`Function.compose` vs `andThen` (ordem importa)", "`Predicate.and`/`or`/`negate`/`isEqual`", "`Consumer.andThen`", "Funções de alta ordem (retornar uma `Function`; receber `Function` como parâmetro)", "Captura e `effectively final`; closures em Java", "Quando o estilo funcional **ajuda** (transformação declarativa, reuso) vs **atrapalha** (debugging, stack traces opacos, estado mutável)".
- `## Na prática` — montar um `Function<Order,Order>` pipeline com `andThen`; um `Predicate<Order>` composto com `and`/`or`; uma fábrica `Function<Config, Function<Order,Order>>`.
- `## Armadilhas` — ≥3: (1) inverter `compose` (g.compose(f) roda f primeiro) vs `andThen` (f.andThen(g) roda f primeiro) → escolher pela ordem desejada; (2) pipeline funcional ilegível (composição profunda inline) → extrair funções nomeadas; (3) stack trace inútil em lambda aninhada → nomear/quebrar. Exemplo + fix.
- `## Em entrevista` + `## Veja também` (04, 07, 10, MOC, central, `[[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/08 - Interfaces e classes abstratas|Interfaces]]`, verbetes `effectively final`/`Function / Predicate / Consumer / Supplier`) + `## Referências`.

Tamanho: 300-460 linhas (densa; opus).

- [ ] **Step 3: Verificar**

```bash
grep -E "compose|andThen|negate|effectively final|alta ordem|closure" "03-Dominios/Tecnologia/Java/Collections e Streams/13 - Composição funcional e funções de alta ordem.md" | head
```

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/Collections e Streams/13 - Composição funcional e funções de alta ordem.md"
git commit -m "feat(java): galho 2 nota 13 — composição funcional e funções de alta ordem"
```

---

### Task 14: Nota 14 — SequencedCollection e SequencedMap (Java 21)

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Collections e Streams/14 - SequencedCollection e SequencedMap.md`

- [ ] **Step 1: Pesquisar fonte — VERIFICAÇÃO OBRIGATÓRIA**

WebFetch `https://openjdk.org/jeps/431` (JEP 431 — Sequenced Collections) + Javadoc `SequencedCollection`/`SequencedSet`/`SequencedMap` (Java 21). Confirmar a versão (Java 21 final), os métodos (`getFirst`/`getLast`/`addFirst`/`addLast`/`removeFirst`/`removeLast`/`reversed`) e quais coleções passaram a implementá-las.

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: magus`, tags `[java, collections, magus, sequenced, java-21]`, aliases `["SequencedCollection", "SequencedMap", "JEP 431"]`.

Conteúdo:
- `## O que é` — as interfaces `SequencedCollection`/`SequencedSet`/`SequencedMap` (Java 21, JEP 431) que unificam o acesso às **pontas** de uma coleção ordenada.
- `## Por que importa` — antes do Java 21, acessar o primeiro/último elemento era inconsistente entre `List` (`get(0)`/`get(size-1)`), `Deque` (`getFirst`/`getLast`) e `LinkedHashSet` (sem acesso direto ao último). Diferencial de "Java moderno" em entrevista.
- `## Como funciona` — H3s: "O problema que resolve (inconsistência histórica)", "`SequencedCollection` (`getFirst`/`getLast`/`addFirst`/`addLast`/`removeFirst`/`removeLast`/`reversed`)", "`SequencedSet` e `SequencedMap` (`firstEntry`/`lastEntry`/`putFirst`/`putLast`)", "O que passou a implementá-las (`List`, `Deque`, `LinkedHashSet`/`LinkedHashMap`, `SortedSet`/`SortedMap`)". **Declarar: Java 21+.**
- `## Na prática` — `list.getFirst()`/`list.getLast()` em vez de índices; `linkedHashSet.reversed()`; iterar de trás pra frente.
- `## Armadilhas` — ≥3: (1) `reversed()` retorna **view** (muta o original) → copiar se precisa isolar; (2) assumir disponibilidade em Java < 21 (não compila) → declarar baseline; (3) `getFirst()` em coleção vazia (`NoSuchElementException`) → checar `isEmpty`. Exemplo + fix.
- `## Em entrevista` + `## Veja também` (01, 02, MOC, central, verbetes `SequencedCollection / SequencedMap`) + `## Referências` (JEP 431, Javadoc).

Tamanho: 240-360 linhas.

- [ ] **Step 3: Verificar**

```bash
grep -E "Sequenced|getFirst|getLast|addFirst|reversed|JEP 431|Java 21" "03-Dominios/Tecnologia/Java/Collections e Streams/14 - SequencedCollection e SequencedMap.md" | head
```

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/Collections e Streams/14 - SequencedCollection e SequencedMap.md"
git commit -m "feat(java): galho 2 nota 14 — SequencedCollection e SequencedMap (Java 21)"
```

---

### Task 15: Nota 15 — Collectors customizados e Gatherers (Java 24)  ⟦opus⟧

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Collections e Streams/15 - Collectors customizados e Gatherers.md`

- [ ] **Step 1: Pesquisar fonte — VERIFICAÇÃO OBRIGATÓRIA**

WebFetch `https://openjdk.org/jeps/485` (JEP 485 — Stream Gatherers) + Javadoc `java.util.stream.Gatherer`/`Gatherers` e `java.util.stream.Collector` (`Collector.of`). **Confirmar o status final**: JEP 485 entregou Gatherers como feature final no **Java 24** (após preview em 22/23). Confirmar a versão exata, a assinatura de `Stream.gather` e as fábricas (`windowFixed`/`windowSliding`/`fold`/`scan`/`mapConcurrent`). Se em alguma versão suportada ainda for preview, **declarar com hedge** e `--enable-preview`. **Não afirmar como estável sem a fonte.**

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: magus`, tags `[java, collections, magus, streams, gatherers, collectors]`, aliases `["Stream Gatherers", "Collector.of", "JEP 485"]`.

Conteúdo:
- `## O que é` — duas formas de estender a pipeline: `Collector.of` (terminal sob medida) e **Stream Gatherers** (`Stream.gather` — intermediárias customizadas, Java 24).
- `## Por que importa` — antes dos Gatherers, intermediárias customizadas (janela deslizante, scan, fold) eram impossíveis sem sair do stream; é o tópico de stream mais "Java moderno" pra entrevista.
- `## Como funciona` — H3s: "`Collector.of` (supplier/accumulator/combiner/finisher/characteristics)", "Quando escrever um collector próprio vs combinar os de `Collectors`", "**Stream Gatherers** (`Gatherer`, `Stream.gather`) — o que são e por que existem", "As fábricas de `Gatherers` (`windowFixed`/`windowSliding`/`fold`/`scan`/`mapConcurrent`)", "**Status de versão** (final no Java 24 via JEP 485 — declarar; hedge se preview na release alvo)".
- `## Na prática` — um `Collector.of` simples; um `Gatherers.windowSliding(3)` numa sequência de `Order`. **Declarar a versão exigida** em comentário.
- `## Armadilhas` — ≥3: (1) `combiner` incorreto num `Collector` (quebra silenciosamente em paralelo) → testar paralelo ou marcar não-concorrente; (2) reinventar um Gatherer que já existe em `Gatherers`; (3) usar Gatherers numa versão que não os tem (não compila) → conferir a release/`--enable-preview`. Exemplo + fix.
- `## Em entrevista` + `## Veja também` (07, 08, 09, MOC, central, `[[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/15 - Parallel streams e fork-join|Parallel streams]]` (mencionar `mapConcurrent` linka aqui, sem re-explicar paralelismo), verbetes `Gatherer (Stream Gatherers)`/`Collector (coletor)`) + `## Referências` (JEP 485, Javadoc).

Tamanho: 300-460 linhas (densa + version-sensitive; opus).

- [ ] **Step 3: Verificar**

```bash
grep -E "Gatherer|gather|Collector.of|windowSliding|JEP 485|Java 24|preview" "03-Dominios/Tecnologia/Java/Collections e Streams/15 - Collectors customizados e Gatherers.md" | head
```
Expected: cobre `Collector.of` + Gatherers; versão declarada com fonte (JEP 485).

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/Collections e Streams/15 - Collectors customizados e Gatherers.md"
git commit -m "feat(java): galho 2 nota 15 — collectors customizados e Gatherers (Java 24)"
```

---

### Task 16: Nota 16 — Escolha de coleção e estilo funcional: síntese  ⟦opus⟧ (capstone)

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Collections e Streams/16 - Escolha de coleção e estilo funcional — síntese.md`

- [ ] **Step 1: Pesquisar fonte (usar modelo opus)**

Reler as notas 01-15 do galho (esta é síntese, não pesquisa nova). Conferir os números de Big-O afirmados contra o Javadoc das implementações (reusar as fontes das notas 02/03). Sem inventar benchmark.

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: magus`, tags `[java, collections, magus, sintese, decisao]`, aliases `["Escolha de coleção", "Stream vs loop", "Funcional vs imperativo"]`.

Conteúdo (capstone — decisão de arquitetura, liga o galho):
- TL;DR: não existe "melhor" coleção/estilo no abstrato — existe o certo pro acesso, volume e contexto. A nota dá os critérios.
- `## O que é` — síntese: como escolher estrutura de dados e estilo de processamento.
- `## Como funciona` — H3s:
  - "Decision tree de coleção" — tabela consolidada (acesso por índice? → `ArrayList`; dedup? → `HashSet`; ordenado? → `TreeMap`/`TreeSet`; pontas/fila? → `ArrayDeque`; prioridade? → `PriorityQueue`; concorrente? → Galho 4) com Big-O.
  - "Stream vs loop" — quando o stream agrega clareza (transformação/agregação declarativa) vs quando o loop é melhor (lógica imperativa complexa, performance crítica, early-return).
  - "Funcional vs imperativo" — trade-offs de legibilidade, debug e performance; sem dogma.
  - "Quando paralelizar" — gancho curto pro Galho 4 (parallel streams) sem re-explicar.
- `## Na prática` — 2-3 cenários (hipotéticos explícitos) escolhendo coleção + estilo e justificando.
- `## Armadilhas` (de raciocínio) — ≥3: (1) escolher coleção por hábito (`ArrayList`/`HashMap` sempre) sem pensar no acesso; (2) "tudo vira stream" (um loop simples às vezes é mais claro/rápido); (3) otimização prematura de estrutura sem medir. Cada uma com o raciocínio correto.
- `## Em entrevista` — frase 3+ sentenças enquadrando escolha de estrutura como decisão de design; vocabulário 6+ termos.
- `### Cheatsheet do galho` — tabela "qual nota pra qual problema" (hierarquia→01, impls→02/03, ordenação→06, streams→05/07/08/09, funcional→04/13, Optional→10, datas→11, I/O→12, moderno→14/15).
- `## Veja também` (01, 02, 03, 05, 07, 08, MOC, central, `[[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/15 - Parallel streams e fork-join|Parallel streams]]`) + `## Referências`.

Tamanho: 300-480 linhas (fechamento; opus).

- [ ] **Step 3: Verificar**

```bash
grep -iE "decision|Big-O|stream vs loop|funcional vs imperativo|Cheatsheet" "03-Dominios/Tecnologia/Java/Collections e Streams/16 - Escolha de coleção e estilo funcional — síntese.md" | head
grep -riE "minha experiência|no meu projeto|josenaldo|Patient" "03-Dominios/Tecnologia/Java/Collections e Streams/16 - Escolha de coleção e estilo funcional — síntese.md"
```
Expected: cobre as três decisões + cheatsheet; **segundo grep VAZIO** (zero fabricação).

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/Collections e Streams/16 - Escolha de coleção e estilo funcional — síntese.md"
git commit -m "feat(java): galho 2 nota 16 — escolha de coleção e estilo funcional (capstone)"
```

---

## Task 17: MOC do galho

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Collections e Streams/index.md`

- [ ] **Step 1: Escrever o MOC**

Frontmatter: `type: moc`, `status: growing`, `publish: true`, `title: "Collections, Streams e Programação Funcional"`, tags `[java, collections, moc]`, aliases `["Collections e Streams", "Galho 2 - Collections, Streams e Programação Funcional"]`, `created`/`updated: 2026-06-04`.

Conteúdo (modelar pelo `03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index.md`):
- `> [!abstract] TL;DR` — Galho 2 da trilha Java Senior; Collections Framework, Stream API, programação funcional (lambdas/composição), Optional, Date/Time (java.time) e I/O moderno (java.nio.file).
- `## Sobre este galho` — escopo + audiência primária (senior em prep de entrevista) + secundária (decisão de design no dia a dia) + nota de que é galho de **refator do tronco** `Java Fundamentals` (poda parcial).
- `## Iniciado` — wikilinks 01-05 (uma linha descritiva cada).
- `## Adepto` — wikilinks 06-12.
- `## Magus` — wikilinks 13-16.
- `## Rotas alternativas` — 5 rotas:
  - **Completa** — 01 → 16.
  - **Entrevista internacional** — 01 → 03 → 04 → 05 → 07 → 08 → 10 → 16.
  - **Domine Streams** — 05 → 07 → 08 → 09 → 15.
  - **Escolha de estrutura de dados** — 01 → 02 → 03 → 06 → 16.
  - **Programação funcional** — 04 → 13 → 10 → 07.
- `## Todas as notas` — bloco Dataview:

````markdown
```dataview
TABLE fase, status, updated
FROM "03-Dominios/Tecnologia/Java/Collections e Streams"
WHERE type = "concept"
SORT file.name ASC
```
````

- `## Veja também` — `[[03-Dominios/Tecnologia/Java/index|Java (MOC central)]]`, `[[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/index|Linguagem e sintaxe moderna (Galho 1)]]`, `[[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Concorrência e paralelismo (Galho 4)]]`, `[[03-Dominios/Tecnologia/Java/Dicionário de Java|Dicionário de Java]]`, `[[Java Fundamentals]]` (tronco em transição). Galho 3 (JVM) como texto "(planejado)", SEM wikilink.

- [ ] **Step 2: Verificar**

```bash
grep -cE "^## (Iniciado|Adepto|Magus|Rotas alternativas)" "03-Dominios/Tecnologia/Java/Collections e Streams/index.md"
grep -c "\[\[" "03-Dominios/Tecnologia/Java/Collections e Streams/index.md"
grep -iE "JVM" "03-Dominios/Tecnologia/Java/Collections e Streams/index.md"
```
Expected: 4 headings de seção; ≥16 wikilinks; "JVM" só como texto "(planejado)" SEM `[[`.

- [ ] **Step 3: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/Collections e Streams/index.md"
git commit -m "feat(java): galho 2 MOC — Collections, Streams e Programação Funcional"
```

---

## Task 18: Expandir o Dicionário de Java (NÃO recriar)

**Files:**
- Modify: `03-Dominios/Tecnologia/Java/Dicionário de Java.md`

- [ ] **Step 1: Reler o Dicionário existente**

Ler `03-Dominios/Tecnologia/Java/Dicionário de Java.md` inteiro. Mapear as seções alfabéticas (A–Y) e os verbetes já presentes (Galhos 1/4/5). **NÃO recriar; NÃO reordenar.** Confirmar o formato (`### Termo` + 1-3 linhas + `Veja também: [[nota]].`). **Conferir duplicatas** — termos como `Atomic` (Galho 4) já existem; não reinserir.

- [ ] **Step 2: Extrair as âncoras de Dicionário usadas nas notas 01-16**

```bash
grep -rhoE "Dicionário de Java#[^]|]+" "03-Dominios/Tecnologia/Java/Collections e Streams/"
```
Anotar cada âncora. **Cada verbete inserido deve ter heading que bate EXATAMENTE (case/acento) com a âncora usada nas notas** (regra dos Galhos 4/5).

- [ ] **Step 3: Inserir os verbetes em ordem alfabética**

Inserir os verbetes abaixo na seção alfabética correta (case-insensitive, sem acento; criar seção se não existir). Cada um: definição 1-3 linhas em PT-BR + `Veja também:` pra nota canônica. **Conferir antes de inserir que o termo não existe** (ajustar a lista às âncoras reais do Step 2).

| Verbete | Seção | Nota canônica |
|---|---|---|
| boxing / unboxing | B | →09 |
| Collector (coletor) | C | →08 |
| Collections Framework | C | →01 |
| Comparable | C | →06 |
| Comparator | C | →06 |
| Deque | D | →02 |
| Duration / Period | D | →11 |
| effectively final | E | →13 |
| Function / Predicate / Consumer / Supplier | F | →04 |
| Gatherer (Stream Gatherers) | G | →15 |
| groupingBy | G | →08 |
| hashCode / equals (contrato) | H | →03 |
| Instant | I | →11 |
| interface funcional | I | →04 |
| java.nio.file (Path / Files) | J | →12 |
| lambda | L | →04 |
| LocalDate / LocalDateTime | L | →11 |
| method reference | M | →04 |
| operação intermediária / terminal | O | →05 |
| Optional | O | →10 |
| PriorityQueue | P | →02 |
| SequencedCollection / SequencedMap | S | →14 |
| Stream | S | →05 |
| stream lazy (avaliação preguiçosa) | S | →05 |
| stream primitivo (IntStream) | S | →09 |
| treeification | T | →03 |
| try-with-resources | T | →12 |

Atualizar frontmatter `updated: 2026-06-04`.

- [ ] **Step 4: Verificar**

```bash
grep -E "^### (Collections Framework|Optional|Stream|Gatherer|groupingBy|lambda|java.nio.file)" "03-Dominios/Tecnologia/Java/Dicionário de Java.md"
grep -cE "^### " "03-Dominios/Tecnologia/Java/Dicionário de Java.md"
```
Expected: verbetes do Galho 2 presentes; contagem total subiu ~24-27 vs baseline; verbetes anteriores intactos.

- [ ] **Step 5: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/Dicionário de Java.md"
git commit -m "feat(java): expande Dicionário de Java com verbetes do galho 2 (Collections/Streams)"
```

---

## Task 19: Ativar o Galho 2 no MOC central `Java/index.md`

**Files:**
- Modify: `03-Dominios/Tecnologia/Java/index.md`

- [ ] **Step 1: Trocar a linha do Galho 2 por wikilink ativo**

Substituir a linha 26 (atualmente `2. Collections, Streams e Programação Funcional *(planejado)* — Collections Framework, Stream API, lambdas, Optional, Date/Time, I/O`) por:

```markdown
2. [[03-Dominios/Tecnologia/Java/Collections e Streams/index|Collections, Streams e Programação Funcional]] — Collections Framework, Stream API, lambdas e interfaces funcionais, Optional, Date/Time (java.time), I/O moderno (java.nio.file)
```

Atualizar `updated: 2026-06-04`. **Não mexer no resto** (galho 3 e 6-18 seguem texto "(planejado)").

- [ ] **Step 2: Verificar**

```bash
grep -E "Collections e Streams/index" "03-Dominios/Tecnologia/Java/index.md"
grep -E "updated: 2026-06-04" "03-Dominios/Tecnologia/Java/index.md"
```
Expected: wikilink ativo do Galho 2; `updated` atualizado.

- [ ] **Step 3: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/index.md"
git commit -m "feat(java): ativa Galho 2 (Collections, Streams) no MOC central"
```

---

## Task 20: Poda parcial do tronco + higienização de fabricação

**Files:**
- Modify: `03-Dominios/Tecnologia/Java/Core/Java Fundamentals.md`

- [ ] **Step 1: Reler as 6 seções a podar (confirmar limites)**

Reler `Core/Java Fundamentals.md` nas 6 seções marcadas `(Galho 2)`: `## Collections Framework`, `## Lambdas e Interfaces Funcionais`, `## Streams API`, `## Date/Time API (Java 8+)`, `## I/O (Arquivos)`, `## Optional`. Confirmar onde cada uma começa e termina (até a próxima `## ` ou o `---`). **NÃO** tocar `## JVM` (Galho 3) nem `## Concorrência (visão geral)` (dívida Galho 4).

- [ ] **Step 2: Substituir cada seção pelo callout de poda**

Substituir o **corpo** de cada uma das 6 seções por um callout no padrão §9 do roadmap (mantém o heading `## `, troca o conteúdo):

```markdown
## Collections Framework

> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Tecnologia/Java/Collections e Streams/index|Collections, Streams e Programação Funcional]]. Veja [[01 - O Collections Framework]], [[02 - Listas, conjuntos e filas]], [[03 - Mapas]], [[06 - Comparable e Comparator]].
```

```markdown
## Lambdas e Interfaces Funcionais

> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Tecnologia/Java/Collections e Streams/index|Collections, Streams e Programação Funcional]]. Veja [[04 - Lambdas e interfaces funcionais]], [[13 - Composição funcional e funções de alta ordem]].
```

```markdown
## Streams API

> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Tecnologia/Java/Collections e Streams/index|Collections, Streams e Programação Funcional]]. Veja [[05 - Introdução à Stream API]], [[07 - Operações de Stream — intermediárias e terminais]], [[08 - Collectors e agrupamento]], [[09 - Streams primitivos]].
```

```markdown
## Date/Time API (Java 8+)

> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Tecnologia/Java/Collections e Streams/index|Collections, Streams e Programação Funcional]]. Veja [[11 - java.time — Date e Time API]].
```

```markdown
## I/O (Arquivos)

> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Tecnologia/Java/Collections e Streams/index|Collections, Streams e Programação Funcional]]. Veja [[12 - I-O moderno com java.nio.file]].
```

```markdown
## Optional

> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Tecnologia/Java/Collections e Streams/index|Collections, Streams e Programação Funcional]]. Veja [[10 - Optional]].
```

(Os wikilinks usam o título de arquivo sem o path completo — Obsidian resolve pelo nome; o callout do Galho 1 no mesmo tronco já usa esse formato. Conferir na Task 22 que resolvem.)

- [ ] **Step 3: Higienizar a cauda fabricada em primeira pessoa**

Na seção `## How to explain in English` (~819-827), o texto está em primeira pessoa fabricada (*"Java has been my primary language for over 20 years, and I've seen it evolve... I use constantly... I reach for..."*). **Reescrever em terceira pessoa neutra**, sobre a linguagem/ecossistema (não sobre o autor), enxugando para um parágrafo curto + ponteiro pros galhos. Modelo de substituição:

```markdown
## Como explicar em inglês

> [!nota] Vocabulário de entrevista migrou para os galhos
> Cada nota dos galhos tem uma seção "Em entrevista" com frase pronta em inglês (3+ sentenças) e vocabulário PT→EN. Para Collections/Streams/funcional, ver [[03-Dominios/Tecnologia/Java/Collections e Streams/index|Collections, Streams e Programação Funcional]]; para linguagem, [[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/index|Linguagem e sintaxe moderna]]; para concorrência, [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Concorrência e paralelismo]].
```

Conferir também `## Na prática` (~815-817): se houver atribuição pessoal, neutralizar (o framing "Em projetos enterprise..." é genérico e pode ficar; remover qualquer "eu"/"meu"). **NÃO** reescrever seções de JVM/Concorrência.

- [ ] **Step 4: Atualizar `updated` do tronco**

Atualizar o frontmatter `updated:` de `Core/Java Fundamentals.md` para `2026-06-04`.

- [ ] **Step 5: Verificar**

```bash
grep -A2 "^## Collections Framework" "03-Dominios/Tecnologia/Java/Core/Java Fundamentals.md" | head -4
grep -c "Migrado para galho próprio" "03-Dominios/Tecnologia/Java/Core/Java Fundamentals.md"
grep -iE "my primary language|I use constantly|I reach for|I've seen" "03-Dominios/Tecnologia/Java/Core/Java Fundamentals.md"
grep -nE "^## (JVM|Concorrência)" "03-Dominios/Tecnologia/Java/Core/Java Fundamentals.md"
```
Expected: as 6 seções do Galho 2 agora são callouts "Migrado" (contador de "Migrado para galho próprio" subiu 6 vs baseline do Galho 1); terceiro grep (fabricação em 1ª pessoa) **VAZIO**; `## JVM` e `## Concorrência` ainda presentes (intactos).

- [ ] **Step 6: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/Core/Java Fundamentals.md"
git commit -m "refactor(java): poda parcial do tronco Java Fundamentals (galho 2) + higieniza cauda em 1ª pessoa"
```

---

## Task 21: Quitar a dívida de linkback do Galho 4

**Files:**
- Modify: `03-Dominios/Tecnologia/Java/Concorrência e paralelismo/07 - Concurrent collections.md`
- Modify: `03-Dominios/Tecnologia/Java/Concorrência e paralelismo/15 - Parallel streams e fork-join.md`

- [ ] **Step 1: Relocalizar as ocorrências (por conteúdo, não por linha)**

```bash
grep -n "Java Fundamentals" "03-Dominios/Tecnologia/Java/Concorrência e paralelismo/07 - Concurrent collections.md" "03-Dominios/Tecnologia/Java/Concorrência e paralelismo/15 - Parallel streams e fork-join.md"
```
São 4 ocorrências relevantes (2 por arquivo: 1 no corpo + 1 em "Veja também"). As ocorrências em `11 - Java Memory Model` e `12 - Virtual Threads` **NÃO** entram (referência geral ao tronco).

- [ ] **Step 2: Atualizar a nota 07 (Concurrent collections)**

No corpo (frase "O framework [[Java Fundamentals]] define as interfaces `Map`, `List`, `Queue` e `Set`..."), trocar `[[Java Fundamentals]]` por `[[03-Dominios/Tecnologia/Java/Collections e Streams/01 - O Collections Framework|Collections Framework]]`.

No "Veja também", trocar a linha `- [[Java Fundamentals]]` por:
```markdown
- [[03-Dominios/Tecnologia/Java/Collections e Streams/01 - O Collections Framework|Collections Framework]]
- [[03-Dominios/Tecnologia/Java/Collections e Streams/03 - Mapas|Mapas]]
```

- [ ] **Step 3: Atualizar a nota 15 (Parallel streams)**

No corpo (frase "o pipeline de operações de stream em si... pertence ao Galho 2 (Stream API); consulte [[Java Fundamentals]] para essa base"), trocar `[[Java Fundamentals]]` por `[[03-Dominios/Tecnologia/Java/Collections e Streams/05 - Introdução à Stream API|Stream API]]` (e, se fluir, citar também `[[03-Dominios/Tecnologia/Java/Collections e Streams/07 - Operações de Stream — intermediárias e terminais|Operações de Stream]]`). Ajustar o texto para não dizer mais "Galho 2 (Stream API)" como futuro — o galho agora existe.

No "Veja também", trocar `- [[Java Fundamentals]]` por:
```markdown
- [[03-Dominios/Tecnologia/Java/Collections e Streams/07 - Operações de Stream — intermediárias e terminais|Operações de Stream]]
```

- [ ] **Step 4: Verificar**

```bash
grep -n "Java Fundamentals" "03-Dominios/Tecnologia/Java/Concorrência e paralelismo/07 - Concurrent collections.md" "03-Dominios/Tecnologia/Java/Concorrência e paralelismo/15 - Parallel streams e fork-join.md"
grep -n "Collections e Streams" "03-Dominios/Tecnologia/Java/Concorrência e paralelismo/07 - Concurrent collections.md" "03-Dominios/Tecnologia/Java/Concorrência e paralelismo/15 - Parallel streams e fork-join.md"
```
Expected: nas notas 07/15, as 4 ocorrências da **base de Collections/Streams** agora apontam pro Galho 2 (não mais `[[Java Fundamentals]]` nesses pontos); links pro Galho 2 presentes.

- [ ] **Step 5: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/Concorrência e paralelismo/07 - Concurrent collections.md" "03-Dominios/Tecnologia/Java/Concorrência e paralelismo/15 - Parallel streams e fork-join.md"
git commit -m "refactor(java): quita dívida de linkback do galho 4 (07/15 apontam pro galho 2)"
```

---

## Task 22: Verificação final do galho

**Files:** (somente leitura/verificação)

- [ ] **Step 1: Conferir as 16 notas + MOC presentes**

```bash
ls "03-Dominios/Tecnologia/Java/Collections e Streams/" | sort
```
Expected: 01..16 + index.md (17 arquivos .md).

- [ ] **Step 2: Conferir frontmatter `fase` e distribuição**

```bash
for f in "03-Dominios/Tecnologia/Java/Collections e Streams/"[0-9]*.md; do grep -H "^fase:" "$f"; done
```
Expected: toda nota 01-16 tem `fase:`; distribuição 5 iniciado / 7 adepto / 4 magus.

- [ ] **Step 3: Conferir seções obrigatórias em todas as notas**

```bash
for f in "03-Dominios/Tecnologia/Java/Collections e Streams/"[0-9]*.md; do
  echo "$f: $(grep -cE '^## (Em entrevista|Armadilhas|Veja também)' "$f")"
done
```
Expected: cada nota retorna 3.

- [ ] **Step 4: Conferir ausência de fabricação e de wikilinks pro Galho 3 (JVM)**

```bash
grep -riE "minha experiência|no meu projeto|josenaldo|Patient|getSpecialty" "03-Dominios/Tecnologia/Java/Collections e Streams/"
grep -rE "\[\[[^]]*JVM" "03-Dominios/Tecnologia/Java/Collections e Streams/"
```
Expected: ambos VAZIOS (zero fabricação; JVM nunca como wikilink — só texto "(planejado)").

- [ ] **Step 5: Conferir a "Frase pronta (inglês)" em todas as notas**

```bash
for f in "03-Dominios/Tecnologia/Java/Collections e Streams/"[0-9]*.md; do
  echo "$f: $(grep -c '### Frase pronta (inglês)' "$f")"
done
```
Expected: cada nota retorna 1.

- [ ] **Step 6: Rodar a skill de wikilinks**

Invocar a skill `verificar-wikilinks` na pasta `03-Dominios/Tecnologia/Java/Collections e Streams/` + `03-Dominios/Tecnologia/Java/index.md` + `03-Dominios/Tecnologia/Java/Dicionário de Java.md` + `03-Dominios/Tecnologia/Java/Core/Java Fundamentals.md` + as duas notas editadas do Galho 4 (07, 15). Corrigir quebrados (folder-links exigem index.md — regra Quartz). **Lembrar:** falso-positivo em self-anchors `[[#Heading]]` — as notas evitam âncoras same-file; ignorar esse falso-positivo. **Conferir que as âncoras `Dicionário de Java#...` usadas nas notas resolvem 1:1 com os headings dos verbetes inseridos (Task 18 Step 2).** Conferir também que os wikilinks curtos do tronco podado (`[[01 - O Collections Framework]]` etc.) resolvem. Se houver correções, commitar à parte.

- [ ] **Step 7: Build Quartz (se disponível)**

Confirmar publicação sem erro conforme o pipeline do projeto (deploy cross-repo é manual do usuário — NÃO fazer push/deploy). Se o build não rodar localmente, registrar como verificação manual pendente.

- [ ] **Step 8: Resumo de fechamento (sem commit)**

Reportar ao usuário: 16 notas criadas, distribuição de fases, verbetes adicionados, poda parcial executada (6 seções + higienização da cauda), dívida de linkback do Galho 4 quitada, estado da verificação de wikilinks (e qualquer falso-positivo ignorado). Trabalho está na `main` (commits locais) — **push é manual do usuário** (não foi feito).

---

## Self-Review (preenchido na escrita do plano)

**Spec coverage:** as 16 notas (Tasks 1-16) cobrem o §3.1 do spec; MOC (Task 17) → §3.2; Dicionário expandido (Task 18) → §3.3; MOC central (Task 19) → §3.4; poda parcial + higienização (Task 20) → §3.5; dívida de linkback do Galho 4 (Task 21) → §3.6; pré-flight (Task 0) → §6; verificação final (Task 22) → §7. Reciprocidade de links Galho 2→Galho 4 (§3.7) honrada nas notas 01/03 (→07 Concurrent collections) e 05/07 (→15 Parallel streams). Fronteiras (§3.1) respeitadas: paralelismo/concurrent collections linkam Galho 4, não re-explicam; interfaces/generics/records/exceções linkam Galho 1; JVM como texto "(planejado)" sem wikilink.

**Placeholder scan:** sem TBD/TODO. Cada nota tem Step 1 com URLs de fonte oficial nomeadas, frontmatter concreto, outline de seções (H3s), armadilhas mínimas (≥2 Iniciado / ≥3 Adepto-Magus) e tamanho-alvo. Notas version-sensitive (14 SequencedCollection, 15 Gatherers) com verificação obrigatória explícita. Capstone (16) com grep anti-fabricação.

**Type/naming consistency:** numeração 01-16 consistente entre tasks, MOC (rotas/seções), Dicionário (notas canônicas), poda (callouts) e verificação. Distribuição 5/7/4 consistente no header, nas fases das tasks e na Task 22 Step 2. Notas opus (08/13/15/16) marcadas ⟦opus⟧. Nomes de arquivo sem `:` nem `/` problemático (usado `—` em "07/16", `I-O` em "12" pra evitar `/` no filesystem). Pasta `Collections e Streams` (decidida na brainstorming) consistente em todos os paths. Âncoras do Dicionário conferidas 1:1 (Task 18 Step 2 + Task 22 Step 6). Linkback (Task 21) edita por conteúdo, não por número de linha (resiliente a deslocamento).
