---
title: "SequencedCollection e SequencedMap"
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
  - sequenced
  - java-21
aliases:
  - SequencedCollection
  - SequencedMap
  - JEP 431
---

# SequencedCollection e SequencedMap

> [!abstract] TL;DR
> **Java 21 (JEP 431)** introduziu três novas interfaces — `SequencedCollection`, `SequencedSet` e `SequencedMap` — para unificar o acesso às **pontas** de qualquer coleção ordenada. Antes disso, obter o primeiro ou último elemento de uma `List`, de uma `Deque` ou de um `LinkedHashSet` exigia APIs completamente diferentes e inconsistentes. A partir do Java 21, todas essas estruturas expõem `getFirst()`/`getLast()`, `addFirst()`/`addLast()`, `removeFirst()`/`removeLast()` e `reversed()` por meio de uma interface comum. `reversed()` devolve uma **view reversa ao vivo** — mutações nela refletem na coleção original. O ponto de armadilha mais frequente em entrevista: confundir `reversed()` com uma cópia e assumir isolamento que não existe.

## O que é

Antes do Java 21, o Collections Framework não possuía uma abstração comum para coleções que têm uma **ordem de encontro** (*encounter order*) bem definida — ou seja, onde existe um primeiro e um último elemento. Cada família de coleção expunha o acesso às pontas de modo diferente, sem interface unificada.

O **JEP 431**, entregue como **feature GA no Java 21** (setembro de 2023 — LTS), corrigiu isso introduzindo três novas interfaces em `java.util`:

| Interface | Estende | Propósito |
|---|---|---|
| `SequencedCollection<E>` | `Collection<E>` | Qualquer coleção com ordem de encontro definida |
| `SequencedSet<E>` | `SequencedCollection<E>`, `Set<E>` | `SequencedCollection` sem duplicatas |
| `SequencedMap<K,V>` | `Map<K,V>` | Mapa com ordem de encontro definida nas entradas |

Essas interfaces **não quebram nenhuma API existente**: as implementações já presentes na biblioteca padrão (como `ArrayList`, `LinkedHashSet`, `TreeMap`) passaram simplesmente a declarar os novos tipos, e os novos métodos foram adicionados como `default methods`, portanto código existente continua compilando sem alteração.

## Por que importa

### A inconsistência histórica

Antes do Java 21, obter o primeiro ou último elemento de uma coleção dependia da família usada — não havia um contrato único:

| Coleção | Pegar o primeiro | Pegar o último |
|---|---|---|
| `List<E>` | `list.get(0)` | `list.get(list.size() - 1)` |
| `Deque<E>` | `deque.peekFirst()` | `deque.peekLast()` |
| `LinkedHashSet<E>` | `set.iterator().next()` | sem suporte direto |
| `SortedSet<E>` | `set.first()` | `set.last()` |

Três interfaces, quatro formas diferentes, nenhuma delas portátil. Escrever código genérico que acesse as pontas de "qualquer coleção ordenada" era impossível sem downcasting.

### O diferencial em entrevista

Conhecer o JEP 431 e conseguir explicar *o que mudou* e *por quê* é exatamente o tipo de conhecimento que diferencia um candidato sênior de um que parou no Java 8 ou 11. A pergunta clássica é: "Como você pega o último elemento de uma `List`?" — o candidato que responde `list.getLast()` e em seguida menciona Java 21 e `SequencedCollection` demonstra acompanhamento ativo da plataforma.

## Como funciona

### O problema que resolve (inconsistência histórica)

O Java Collections Framework foi projetado com três hierarquias paralelas (`Collection`, `Set`, `Map`), mas sem uma abstração para o conceito ortogonal de *ter uma ordem de encontro*. O resultado foi a proliferação de APIs idiossincráticas para acessar pontas: índices em `List`, métodos `first()`/`last()` em `SortedSet`, métodos `peekFirst()`/`peekLast()` em `Deque`. O JEP 431 inseriu `SequencedCollection` diretamente na hierarquia existente, sem quebrar compatibilidade binária.

### `SequencedCollection` — métodos de ponta e `reversed()`

A interface `SequencedCollection<E>` define sete métodos — e no Java 21 **todos são `default`**, inclusive `reversed()`. `reversed()` é o **método-chave que cada implementação concreta fornece/sobrescreve** para devolver a view reversa adequada à sua estrutura; os demais métodos de mutação têm implementação `default` que lança `UnsupportedOperationException` (portanto implementações imutáveis funcionam sem override extra):

```java
// Métodos default (implementação base via interface)
default E    getFirst()          // retorna o primeiro elemento
default E    getLast()           // retorna o último elemento
default void addFirst(E e)       // insere e como novo primeiro elemento
default void addLast(E e)        // insere e como novo último elemento
default E    removeFirst()       // remove e retorna o primeiro elemento
default E    removeLast()        // remove e retorna o último elemento

// Método-chave (cada implementação concreta fornece/sobrescreve)
SequencedCollection<E> reversed() // retorna view reversa ao vivo
```

Uso prático com uma `ArrayList` (Java 21+):

```java
List<String> frutas = new ArrayList<>(List.of("maçã", "banana", "caju"));

String primeira = frutas.getFirst();  // "maçã"    — antes: frutas.get(0)
String ultima   = frutas.getLast();   // "caju"     — antes: frutas.get(frutas.size() - 1)

frutas.addFirst("abacaxi");           // ["abacaxi","maçã","banana","caju"]
frutas.removeLast();                  // remove "caju" → ["abacaxi","maçã","banana"]

// Iteração reversa sem inverter a lista
for (String f : frutas.reversed()) {
    System.out.println(f);           // banana → maçã → abacaxi
}
```

### `SequencedSet` e `SequencedMap`

**`SequencedSet<E>`** estende `SequencedCollection<E>` e `Set<E>`. A única diferença em relação a `SequencedCollection` é o tipo de retorno de `reversed()` — o método-chave que cada implementação concreta sobrescreve —, que aqui é `SequencedSet<E>` (covariância):

```java
SequencedSet<E> reversed()   // retorna view reversa como SequencedSet
```

`LinkedHashSet` passa a implementar `SequencedSet` no Java 21:

```java
SequencedSet<String> siglas = new LinkedHashSet<>(List.of("JVM", "JDK", "JRE"));
System.out.println(siglas.getFirst()); // "JVM"
System.out.println(siglas.getLast());  // "JRE"

// Iterar em ordem inversa de inserção
siglas.reversed().forEach(System.out::println); // JRE → JDK → JVM
```

**`SequencedMap<K,V>`** é análogo, mas na hierarquia de mapas. Aqui também todos os métodos são `default` no Java 21; `reversed()` é o método-chave que cada implementação concreta fornece/sobrescreve:

```java
// Acesso às pontas
default Map.Entry<K,V> firstEntry()           // primeira entrada (sem remover)
default Map.Entry<K,V> lastEntry()            // última entrada (sem remover)
default Map.Entry<K,V> pollFirstEntry()       // remove e retorna a primeira entrada
default Map.Entry<K,V> pollLastEntry()        // remove e retorna a última entrada

// Inserção posicionada
default V putFirst(K k, V v)                  // insere/move entrada para o início
default V putLast(K k, V v)                   // insere/move entrada para o fim

// Views sequenciadas
default SequencedSet<K>              sequencedKeySet()
default SequencedCollection<V>       sequencedValues()
default SequencedSet<Map.Entry<K,V>> sequencedEntrySet()

// Método-chave (cada implementação concreta fornece/sobrescreve)
SequencedMap<K,V> reversed()
```

Uso com `LinkedHashMap` (Java 21+):

```java
SequencedMap<String, Integer> notas = new LinkedHashMap<>();
notas.put("Alice", 90);
notas.put("Bruno", 85);
notas.put("Carla", 92);

Map.Entry<String, Integer> primeira = notas.firstEntry(); // Alice=90
Map.Entry<String, Integer> ultima   = notas.lastEntry();  // Carla=92

notas.putFirst("Ana", 88); // Ana=88 passa a ser o primeiro par
notas.sequencedKeySet().reversed().forEach(System.out::println); // Carla → Bruno → Alice → Ana
```

### O que passou a implementar essas interfaces (Java 21)

| Interface | Implementações principais |
|---|---|
| `SequencedCollection` | `List`, `Deque`, `BlockingDeque` (e todas as implementações concretas: `ArrayList`, `LinkedList`, `ArrayDeque`, `CopyOnWriteArrayList`, etc.) |
| `SequencedSet` | `LinkedHashSet`, `TreeSet`, `ConcurrentSkipListSet` (via `NavigableSet` / `SortedSet`) |
| `SequencedMap` | `LinkedHashMap`, `TreeMap`, `ConcurrentSkipListMap` (via `NavigableMap` / `SortedMap`) |

> [!important] Requer Java 21+
> `SequencedCollection`, `SequencedSet` e `SequencedMap` são **GA desde o Java 21** (JEP 431). Código que usa `getFirst()`, `getLast()`, `reversed()` etc. **não compila em Java 8, 11 ou 17**. Declara o baseline do projeto antes de adotar.

## Na prática

### Antes e depois — List

```java
// Java 8–20: acesso por índice, propenso a off-by-one
String primeiro = lista.get(0);
String ultimo   = lista.get(lista.size() - 1);

// Java 21+: explícito e seguro
String primeiro = lista.getFirst();
String ultimo   = lista.getLast();
```

### Iteração reversa sem copiar

```java
List<Integer> numeros = new ArrayList<>(List.of(1, 2, 3, 4, 5));

// Antes: era necessário Collections.reverse() (muta in-place) ou subList com índices
// Agora: view reversa ao vivo — sem alocação extra de lista
numeros.reversed().forEach(n -> System.out.print(n + " ")); // 5 4 3 2 1

// Ou via Stream:
numeros.reversed().stream()
       .filter(n -> n % 2 == 0)
       .forEach(System.out::println); // 4 → 2
```

### LinkedHashSet com acesso posicionado

```java
SequencedSet<String> linguagens = new LinkedHashSet<>(
    List.of("Java", "Kotlin", "Scala")
);

linguagens.addFirst("Groovy"); // Groovy agora é o primeiro
linguagens.addLast("Clojure"); // Clojure agora é o último

System.out.println(linguagens.getFirst()); // Groovy
System.out.println(linguagens.getLast());  // Clojure
```

### View reversa de mapa preservando tipo sequenciado

```java
SequencedMap<String, Integer> ranking = new LinkedHashMap<>();
ranking.put("ouro",   1);
ranking.put("prata",  2);
ranking.put("bronze", 3);

// Iterar do último para o primeiro sem criar novo mapa
ranking.reversed().forEach((medal, pos) ->
    System.out.println(pos + ". " + medal)
); // 3. bronze → 2. prata → 1. ouro
```

## Armadilhas

> [!warning] `reversed()` é uma view ao vivo, não uma cópia
> Modificar a view reversa **muta a coleção original**, e vice-versa. Se você precisa de isolamento, copie explicitamente:
> ```java
> List<String> original = new ArrayList<>(List.of("a", "b", "c"));
> List<String> reversa  = original.reversed();
>
> reversa.addFirst("z"); // muta original → ["a", "b", "c", "z"]  ← surpresa!
>
> // Correto quando isolar:
> List<String> copia = new ArrayList<>(original.reversed());
> ```

> [!warning] `getFirst()` / `getLast()` em coleção vazia lança `NoSuchElementException`
> Diferente de `Optional`, os métodos de acesso às pontas não retornam um valor sentinela — eles lançam exceção se a coleção estiver vazia. Sempre cheque antes de acessar:
> ```java
> if (!lista.isEmpty()) {
>     String ultimo = lista.getLast();
> }
> // ou use Optional manualmente se preferir fluxo funcional
> Optional<String> opt = lista.isEmpty()
>     ? Optional.empty()
>     : Optional.of(lista.getLast());
> ```

> [!warning] Não use em código com baseline anterior ao Java 21
> `getFirst()`, `getLast()`, `reversed()` e os demais métodos de `SequencedCollection` **não existem antes do Java 21**. Compilar com `--source 17` ou executar em JVM 17 resultará em erro. Verifique o `sourceCompatibility` / `--release` da build antes de adotar. Em ambientes corporativos presos no Java 11 ou 17, a API ainda não está disponível.

> [!tip] `putFirst`/`putLast` em `LinkedHashMap` move entradas existentes
> Se a chave já existe no mapa, `putFirst(k, v)` ou `putLast(k, v)` **não criam uma entrada duplicada** — elas reposicionam a entrada existente para a ponta solicitada, como um "move to front/back". Esse comportamento difere de um `put` comum e é útil para implementar caches LRU simples.

## Em entrevista

### Frase pronta (inglês)

"Prior to Java 21, there was no unified way to access the first or last element of an ordered collection — you had `get(0)` on `List`, `peekFirst()` on `Deque`, and `first()` on `SortedSet`, all incompatible. JEP 431, delivered as a GA feature in Java 21, introduced the `SequencedCollection`, `SequencedSet`, and `SequencedMap` interfaces to fix exactly that inconsistency, adding `getFirst()`, `getLast()`, `addFirst()`, `addLast()`, `removeFirst()`, `removeLast()`, and `reversed()` to all ordered collection types. The key subtlety is that `reversed()` returns a live, bidirectional view of the original — mutations on the view propagate back to the source — so you should copy it explicitly if you need an isolated snapshot."

### Vocabulário (inglês)

| Termo | Definição |
|---|---|
| **sequenced collection** | any collection with a well-defined *encounter order* exposing `getFirst`/`getLast` |
| **encounter order** | the order in which elements are encountered during iteration |
| **live view** | a view object whose state reflects mutations in the backing collection in real time |
| **JEP 431** | the Java Enhancement Proposal that introduced the three sequenced interfaces in Java 21 |
| **covariant return type** | `SequencedSet.reversed()` returns `SequencedSet`, narrowing the return type of the parent |
| **`pollFirstEntry` / `pollLastEntry`** | remove-and-return operations on `SequencedMap`, analogous to `poll` on `Deque` |

## Veja também

- [[01 - O Collections Framework]]
- [[02 - Listas, conjuntos e filas]]
- [[03-Dominios/Java/Collections e Streams/index|Collections e Streams (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Dicionário de Java#SequencedCollection / SequencedMap|SequencedCollection / SequencedMap]]

## Referências

- OpenJDK — **JEP 431: Sequenced Collections** (Java 21, GA): https://openjdk.org/jeps/431
- Oracle Javadoc 21 — `SequencedCollection`: https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/SequencedCollection.html
- Oracle Javadoc 21 — `SequencedSet`: https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/SequencedSet.html
- Oracle Javadoc 21 — `SequencedMap`: https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/SequencedMap.html
