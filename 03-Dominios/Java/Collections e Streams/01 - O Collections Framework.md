---
title: "O Collections Framework"
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
  - framework
aliases:
  - Collections Framework
  - Coleções em Java
---

# O Collections Framework

> [!abstract] TL;DR
> O Collections Framework é uma arquitetura unificada para representar e manipular grupos de objetos. Ele define interfaces (`List`, `Set`, `Queue`, `Map`) separadas de suas implementações (`ArrayList`, `HashSet`, `HashMap`…). `Map` **não é** `Collection` — modela pares chave-valor, não elementos avulsos. A decisão de nível sênior está em escolher a **interface** certa antes de escolher a implementação.

## O que é

O Collections Framework foi introduzido no Java 2 (JDK 1.2) e fornece:

- **Interfaces** — tipos abstratos que descrevem os contratos (`Collection`, `List`, `Set`, `Queue`, `Map`).
- **Implementações** — classes concretas que cumprem esses contratos (`ArrayList`, `LinkedList`, `HashSet`, `TreeSet`, `HashMap`, `TreeMap`…).
- **Algoritmos** — métodos utilitários na classe `Collections` (ordenação, embaralhamento, busca binária etc.).

### A hierarquia raiz: `Iterable` → `Collection`

```text
java.lang.Iterable
  └── java.util.Collection
        ├── List    → ArrayList, LinkedList, Vector
        ├── Set     → HashSet, LinkedHashSet, TreeSet
        └── Queue   → PriorityQueue, ArrayDeque, LinkedList
```

`Iterable` é a interface raiz: define apenas `iterator()`, permitindo que qualquer objeto seja percorrido pelo `for-each`. `Collection` estende `Iterable` e acrescenta os contratos de adição, remoção, tamanho e conversão para stream.

### Por que `Map` **não é** `Collection`

A hierarquia consiste em duas árvores distintas: a de `Collection` e a de `Map`. Segundo a documentação oficial dos The Java Tutorials:

> "Note also that the hierarchy consists of two distinct trees — a Map is not a true Collection."

`Map` modela associações chave→valor — o acesso é por chave, não por iteração de elementos avulsos. Por isso `Map` **não estende** `Collection`: a semântica é fundamentalmente diferente. `Map` tem sua própria hierarquia:

```text
java.util.Map
  └── HashMap, LinkedHashMap, TreeMap, ConcurrentHashMap, Hashtable
```

Dica de memória: se a estrutura armazena *pares*, é `Map`; se armazena *elementos*, é `Collection`.

## Por que importa

Escolher a estrutura de dados certa é uma das decisões mais visíveis de um desenvolvedor sênior. Os impactos práticos:

- **Performance**: `ArrayList` com acesso por índice é O(1); `LinkedList` é O(n). `HashSet.contains` é O(1); `TreeSet.contains` é O(log n).
- **Semântica**: `Set` garante unicidade; `List` garante ordem de inserção; `Queue` garante ordem de processamento.
- **Contratos de API**: um método que recebe `Collection<Order>` aceita qualquer implementação, tornando o código mais flexível. Um método que exige `ArrayList<Order>` cria acoplamento desnecessário.

Em entrevistas para posições sênior, a hierarquia do Collections Framework é perguntada quase certamente — especialmente a distinção entre `List`/`Set`/`Queue` e o papel à parte do `Map`.

## Como funciona

### A hierarquia (`Iterable` / `Collection` / `List` / `Set` / `Queue` / `Map`)

```text
java.lang.Iterable
│   iterator()
│
└── java.util.Collection
    │   add(E)  remove(Object)  contains(Object)  size()  isEmpty()
    │   iterator()  stream()  parallelStream()
    │   addAll()  removeAll()  retainAll()  clear()
    │
    ├── java.util.List           (ordenada por índice, permite duplicatas)
    │     get(int)  set(int, E)  indexOf(Object)  subList(int, int)
    │     Impls: ArrayList, LinkedList
    │
    ├── java.util.Set            (sem duplicatas)
    │   ├── SortedSet / NavigableSet  (ordenada por Comparator/natural)
    │   Impls: HashSet, LinkedHashSet, TreeSet
    │
    └── java.util.Queue          (FIFO / prioridade)
          offer(E)  poll()  peek()
          └── Deque (double-ended)
          Impls: PriorityQueue, ArrayDeque, LinkedList

java.util.Map   ← raiz separada, NÃO extends Collection
  put(K, V)  get(Object)  containsKey(Object)  keySet()  values()  entrySet()
  Impls: HashMap, LinkedHashMap, TreeMap
```

### A API comum de `Collection` (`add` / `remove` / `contains` / `size` / `iterator` / `stream`)

Todos os subtipos de `Collection` herdam estes métodos:

| Método | Descrição |
|--------|-----------|
| `boolean add(E e)` | Adiciona o elemento; retorna `true` se a coleção foi modificada |
| `boolean remove(Object o)` | Remove uma instância do elemento; retorna `true` se modificada |
| `boolean contains(Object o)` | Retorna `true` se o elemento está presente |
| `int size()` | Número de elementos |
| `boolean isEmpty()` | Atalho para `size() == 0` |
| `Iterator<E> iterator()` | Retorna um `Iterator` para percorrer a coleção |
| `Stream<E> stream()` | Retorna um stream sequencial (Java 8+) |
| `Stream<E> parallelStream()` | Retorna um stream paralelo (Java 8+) |
| `void clear()` | Remove todos os elementos |

> O `add` é definido de forma geral o suficiente para fazer sentido em coleções que permitem duplicatas e nas que não permitem. Ele garante que a coleção conterá o elemento especificado após a chamada e retorna `true` se a coleção foi modificada. — The Java Tutorials (Oracle)

### Coleções imutáveis (`List.of` / `Set.of` / `Map.of`, Java 9) vs views (`Collections.unmodifiableList`)

A partir do **Java 9**, foram introduzidos métodos de fábrica estáticos que criam coleções **verdadeiramente imutáveis**:

```java
List<String> imutavel   = List.of("a", "b", "c");
Set<String>  conjunto   = Set.of("x", "y", "z");
Map<String, Integer> mapa = Map.of("chave", 1, "outra", 2);
```

Características garantidas pela Javadoc oficial (Java 21):

- **Imutável de verdade**: qualquer chamada a método mutador (`add`, `remove`, `set`, `put`) lança `UnsupportedOperationException`.
- **Null proibido**: tentar criar com elemento `null` lança `NullPointerException`.
- **Serializável**: se todos os elementos forem serializáveis.
- **Sem ordem garantida** para `Set.of` e `Map.of` (a ordem pode variar entre JVMs).

Isso é diferente de `Collections.unmodifiableList(lista)`, que cria apenas uma **view** — uma camada de proteção sobre a lista original:

```java
List<String> original = new ArrayList<>(List.of("a", "b", "c"));
List<String> view     = Collections.unmodifiableList(original);

// view.add("d");    // lança UnsupportedOperationException
original.add("d");   // OK — a lista original é mutável
System.out.println(view); // [a, b, c, d]  ← a view reflete a mutação!
```

| Característica | `List.of(...)` | `Collections.unmodifiableList(x)` |
|----------------|---------------|-----------------------------------|
| Imutável de verdade | Sim | Não (é view) |
| Reflete mutações na fonte | N/A | Sim |
| Null aceito | Não | Depende da lista original |
| Disponível desde | Java 9 | Java 1.2 |

### Coleções thread-safe existem — dono é o Galho 4

O Collections Framework inclui wrappers thread-safe (`Collections.synchronizedList`) e implementações concorrentes (`ConcurrentHashMap`, `CopyOnWriteArrayList`). Este é um tópico do [[03-Dominios/Java/Concorrência e paralelismo/07 - Concurrent collections|Galho 4 — Concurrent collections]]. Aqui apenas se registra que a necessidade existe; o design correto para ambientes multi-thread vai para esse galho.

## Na prática

O exemplo abaixo mostra os padrões mais comuns com `List`, `Set` e `Map`, usando um domínio neutro de pedidos (`Order`, `Customer`):

```java
import java.util.*;

public class ColecoesDemonstration {

    record Order(int id, String customer, double total) {}

    public static void main(String[] args) {

        // --- List: coleção ordenada, permite duplicatas ---
        List<Order> orders = new ArrayList<>();
        orders.add(new Order(1, "Alice", 250.00));
        orders.add(new Order(2, "Bob",   180.50));
        orders.add(new Order(3, "Alice", 99.90));

        System.out.println("Tamanho: " + orders.size());          // 3
        System.out.println("Contém id=1? " + orders.contains(new Order(1, "Alice", 250.00)));

        // Iteração com for-each (Iterable)
        for (Order o : orders) {
            System.out.println(o.id() + " - " + o.customer());
        }

        // Iteração com stream (Collection)
        orders.stream()
              .filter(o -> o.total() > 100)
              .forEach(o -> System.out.println("Alto valor: " + o.id()));

        // --- Set: sem duplicatas ---
        Set<String> customers = new HashSet<>();
        customers.add("Alice");
        customers.add("Bob");
        customers.add("Alice");  // ignorado — já existe
        System.out.println("Clientes únicos: " + customers.size()); // 2

        // --- Map: pares chave-valor (NÃO é Collection) ---
        Map<String, Double> totalPorCliente = new HashMap<>();
        for (Order o : orders) {
            totalPorCliente.merge(o.customer(), o.total(), Double::sum);
        }
        totalPorCliente.forEach((cliente, total) ->
            System.out.printf("%s → R$ %.2f%n", cliente, total));

        // --- Coleção imutável (Java 9+) ---
        List<String> categorias = List.of("Eletrônicos", "Vestuário", "Alimentos");
        System.out.println(categorias.contains("Vestuário")); // true
        // categorias.add("Livros"); // UnsupportedOperationException!
    }
}
```

```text
Tamanho: 3
Contém id=1? true
1 - Alice
2 - Bob
3 - Alice
Alto valor: 1
Alto valor: 2
Clientes únicos: 2
Alice → R$ 349,90
Bob   → R$ 180,50
true
```

## Armadilhas

### (1) `List.of(...)` é imutável — `add` lança `UnsupportedOperationException`

**O problema:** criar uma lista com `List.of(...)` e tentar modificá-la depois é um erro comum, especialmente ao migrar código que usava `Arrays.asList(...)`.

```java
List<String> lista = List.of("a", "b", "c");
lista.add("d");  // UnsupportedOperationException em runtime!
```

**Fix:** Se a lista precisar ser mutável, copie-a para uma implementação mutável:

```java
List<String> mutavel = new ArrayList<>(List.of("a", "b", "c"));
mutavel.add("d");  // OK
```

---

### (2) `Collections.unmodifiableList(x)` é uma *view* — mutar a lista original afeta a view

**O problema:** `unmodifiableList` protege contra modificações *via* a view, mas não protege contra modificações feitas na lista original. Isso cria um falso senso de imutabilidade.

```java
List<String> original = new ArrayList<>(Arrays.asList("a", "b"));
List<String> view     = Collections.unmodifiableList(original);

// view.add("c");   // UnsupportedOperationException — parece seguro
original.add("c");  // Funciona — e a view reflete a mudança
System.out.println(view); // [a, b, c]  ← vazamento!
```

**Fix:** Para imutabilidade real, use `List.of(...)` (Java 9+) ou copie antes de criar a view:

```java
List<String> segura = Collections.unmodifiableList(new ArrayList<>(original));
```

---

### (3) `Arrays.asList(...)` tem tamanho fixo — `add`/`remove` lançam `UnsupportedOperationException`

**O problema:** `Arrays.asList("a", "b", "c")` retorna uma `List` de tamanho **fixo** — permite `set()`, mas não `add()` ou `remove()`. Desenvolvedores assumem que é uma lista comum.

```java
List<String> lista = Arrays.asList("a", "b", "c");
lista.set(0, "x"); // OK — substituição permitida
lista.add("d");    // UnsupportedOperationException!
```

**Fix:** Use `new ArrayList<>(Arrays.asList(...))` para uma lista verdadeiramente mutável, ou prefira `List.of(...)` (Java 9+) se mutabilidade não for necessária.

## Em entrevista

### Frase pronta (inglês)

> "The Java Collections Framework provides a unified architecture of interfaces and implementations for working with groups of objects. The core hierarchy starts at `Iterable`, which enables `for-each` loops, and extends to `Collection` — the root for `List`, `Set`, and `Queue`. `Map` is **not** a `Collection` because it models key-value associations rather than individual elements, so it has its own separate hierarchy. The trade-off when choosing a type is always about semantics and performance: `List` preserves insertion order and allows duplicates in O(1) amortized for `ArrayList`; `Set` enforces uniqueness with O(1) lookups in `HashSet`; `Map` gives O(1) key lookup in `HashMap`. A senior decision point is to program to the **interface** — accept `Collection<T>` or `List<T>` in method signatures, not `ArrayList<T>` — to keep the code flexible. The caveat is immutability: `List.of()` (Java 9+) gives a truly immutable list and throws `UnsupportedOperationException` on any mutator call, while `Collections.unmodifiableList()` only wraps the original and still reflects mutations to the backing list."

### Vocabulário

| Termo PT | Termo EN |
|----------|----------|
| coleção / framework de coleções | collection / Collections Framework |
| lista | list |
| conjunto | set |
| fila | queue |
| mapa | map |
| implementação | implementation |
| coleção imutável | unmodifiable / immutable collection |
| view imutável | unmodifiable view |
| fábrica estática | static factory method |
| operação de mutação | mutator operation |
| exceção de operação não suportada | `UnsupportedOperationException` |
| iterador | iterator |
| percorrer / iterar | iterate / traverse |

## Veja também

- [[02 - Listas, conjuntos e filas]]
- [[03 - Mapas]]
- [[06 - Comparable e Comparator]]
- [[03-Dominios/Java/Collections e Streams/index|Collections e Streams (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Linguagem e sintaxe moderna/12 - Generics em profundidade|Generics]]
- [[03-Dominios/Java/Concorrência e paralelismo/07 - Concurrent collections|Concurrent collections]]
- [[03-Dominios/Java/Dicionário de Java#Collections Framework|Collections Framework]]

## Referências

- [Introduction to the Collections Framework — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/collections/intro/index.html)
- [The Collection Interface — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/collections/interfaces/collection.html)
- [Collections Framework Overview — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/collections/interfaces/index.html)
- [Collections Framework — dev.java](https://dev.java/learn/api/collections-framework/)
- [Javadoc: `java.util.Collection` (Java 21) — Oracle](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/Collection.html)
- [Javadoc: `java.util.List.of()` (Java 21) — Oracle](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/List.html#of(E...))
- [Javadoc: `java.util.Collections.unmodifiableList()` (Java 21) — Oracle](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/Collections.html#unmodifiableList(java.util.List))
