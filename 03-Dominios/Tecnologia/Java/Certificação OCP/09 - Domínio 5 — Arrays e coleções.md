---
title: "Domínio 5 — Arrays e coleções"
created: 2026-06-13
updated: 2026-06-13
type: concept
status: seedling
publish: true
fase: dominios
tags:
  - java
  - certificacao-ocp
  - dominios
aliases:
  - "Domínio 5 OCP"
  - "Arrays e coleções na OCP"
---

# Domínio 5 — Arrays e coleções

> [!abstract] TL;DR
> Este é o domínio das estruturas de dados na OCP. A Oracle quer que você conheça arrays (declaração, multi-dimensão, `Arrays.toString/sort/binarySearch`) e o Collections Framework inteiro: `List`/`Set`/`Map`/`Queue`, suas implementações, ordenação com `Comparable`/`Comparator`, imutabilidade (**view vs cópia**) e as novidades sequenced do Java 21. As pegadinhas aqui são quase todas sobre _o que a coleção faz quando você tenta mexer nela_ — tamanho fixo, view que reflete a original, `ConcurrentModificationException`.

> [!info] Títulos oficiais
> - **1Z0-830 (Java 21):** _Working with Arrays and Collections_
> - **1Z0-831 (Java 25):** _Using Arrays and Collections to Store and Retrieve Data_

## O que a Oracle cobra

- **Arrays** — declaração, inicialização, arrays multi-dimensionais (e "jagged"), `Arrays.toString`, `Arrays.sort`, `Arrays.binarySearch` (exige array já ordenado, senão resultado é indefinido).
- **List, Set, Map, Queue** — as quatro interfaces-base e suas implementações; características de cada uma (ordenação, duplicatas, nulos).
- **ArrayList vs LinkedList** — trade-offs de acesso aleatório (`ArrayList` O(1)) vs inserção/remoção nas pontas (`LinkedList`).
- **HashMap, TreeMap, LinkedHashMap** — sem ordem garantida vs ordem natural/`Comparator` vs ordem de inserção.
- **HashSet, TreeSet, LinkedHashSet** — os mesmos contratos de ordenação aplicados a `Set`.
- **Deque, Stack, Queue** — operações e em qual ponta elas atuam: `push`/`pop`/`peek` (pilha, topo), `offer`/`poll` (fila, sem exceção em fila vazia — devolvem `false`/`null`).
- **Iterator e Iterable** — percorrer coleções; comportamento **fail-fast** (iteradores de `ArrayList`, `HashMap`) vs **fail-safe** (coleções concorrentes, ex. `CopyOnWriteArrayList`).
- **Comparable e Comparator** — `compareTo` (ordem natural, dentro da classe) vs `Comparator` (ordem externa); `Comparator.comparing`, `thenComparing` (desempate), `reversed`.
- **Collections.sort** e imutabilidade — `List.of`, `Collections.unmodifiableList` e a distinção crítica entre **view vs cópia**.
- **ConcurrentModificationException** — o que dispara e como evitar.
- **SequencedCollection / SequencedSet / SequencedMap** (Java 21) — `getFirst()` / `getLast()` / `addFirst` / `addLast` / `reversed()`.

## Mapa de revisão

A trilha de Collections (Galho 2) já cobre tudo isto em profundidade — aqui vão os pontos exatos de revisão:

- [[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/05 - Arrays e varargs|Arrays e varargs (G1)]]
- [[03-Dominios/Tecnologia/Java/Collections e Streams/01 - O Collections Framework|O Collections Framework (G2)]]
- [[03-Dominios/Tecnologia/Java/Collections e Streams/02 - Listas, conjuntos e filas|Listas, conjuntos e filas (G2)]]
- [[03-Dominios/Tecnologia/Java/Collections e Streams/03 - Mapas|Mapas (G2)]]
- [[03-Dominios/Tecnologia/Java/Collections e Streams/06 - Comparable e Comparator|Comparable e Comparator (G2)]]
- [[03-Dominios/Tecnologia/Java/Collections e Streams/14 - SequencedCollection e SequencedMap|SequencedCollection e SequencedMap (G2)]]

## Pegadinhas deste domínio

Este domínio é uma mina de armadilhas. A prova adora um snippet curto que _parece_ inocente e estoura em runtime. As cinco mais cobradas:

**1. `Arrays.asList(arr)` retorna lista de TAMANHO FIXO.** Não é uma `ArrayList` "de verdade". Você pode `set()` em índice existente, mas `.add()` ou `.remove()` lançam `UnsupportedOperationException`.

```java
List<Integer> lista = Arrays.asList(1, 2, 3);
lista.set(0, 99); // OK — tamanho não muda
lista.add(4);     // 💥 UnsupportedOperationException
```

**2. View vs cópia.** `Collections.unmodifiableList(original)` é uma **VIEW**: você não pode escrever _por ela_, mas se a lista original mudar, a view reflete a mudança. Já `List.copyOf(original)` e `List.of(...)` produzem **cópias** independentes e imutáveis.

```java
List<String> orig = new ArrayList<>(List.of("a"));
List<String> view = Collections.unmodifiableList(orig);
List<String> copia = List.copyOf(orig);
orig.add("b");
view.size();  // 2 — a view enxerga a mudança
copia.size(); // 1 — a cópia ficou congelada
```

**3. Valores default de arrays.** Ao alocar um array, os elementos recebem o default do tipo — não ficam "vazios":

```java
int[]     a = new int[3];     // [0, 0, 0]
Integer[] b = new Integer[3]; // [null, null, null]  ← wrapper, não primitivo
boolean[] c = new boolean[3]; // [false, false, false]
```

**4. `ConcurrentModificationException` no for-each.** Modificar a coleção (add/remove) enquanto a percorre com for-each (que usa o `Iterator` fail-fast por baixo) dispara a exceção. Use `Iterator.remove()` ou `removeIf()`.

```java
for (String s : lista) {
    if (s.equals("x")) lista.remove(s); // 💥 ConcurrentModificationException
}
lista.removeIf(s -> s.equals("x"));     // ✅ forma segura
```

**5. `equals`/`hashCode` quebrados.** Se você usa um objeto como chave de `HashMap` ou elemento de `HashSet` sem sobrescrever `hashCode()` (ou sobrescrever `equals` mas não `hashCode`), a coleção "perde" o objeto: você guarda e depois não consegue mais recuperá-lo, porque a busca cai em outro bucket.

> [!tip] Catálogo completo
> Essas e mais armadilhas estão consolidadas no [[03-Dominios/Tecnologia/Java/Certificação OCP/15 - O catálogo de pegadinhas clássicas|catálogo de pegadinhas]] do galho.

## Em entrevista

Falar com clareza sobre imutabilidade pega bem em qualquer entrevista — sem precisar reivindicar a certificação:

> "An `unmodifiableList` is a read-only **view** over the backing list — changes to the original still show through it. `List.copyOf` gives you a true defensive copy. And remember that `ArrayList`'s iterator is **fail-fast**: it throws if the collection is structurally modified mid-iteration."

Vocabulário PT | EN:

- coleção imutável → **immutable collection**
- visão → **view**
- tamanho fixo → **fixed-size**
- ordem de inserção → **insertion order**
- desempate (no `thenComparing`) → **tie-breaker**

## Veja também

- [[03-Dominios/Tecnologia/Java/Certificação OCP/04 - O mapa objetivo → galho — revisar a trilha pra prova|O mapa objetivo → galho]]
- [[03-Dominios/Tecnologia/Java/Certificação OCP/10 - Domínio 6 — Streams e lambdas|Domínio 6 — Streams e lambdas]]
- [[03-Dominios/Tecnologia/Java/Certificação OCP/index|Certificação OCP (MOC do galho)]]

## Referências

- [Enthuware — OCP Java 21 Exam Syllabus](https://enthuware.com/oca-ocp-java-certification-resources/290-ocp-java-21-exam-syllabus)
