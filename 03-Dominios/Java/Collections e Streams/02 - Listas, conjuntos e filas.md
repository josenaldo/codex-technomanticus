---
title: "Listas, conjuntos e filas"
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
  - list
  - set
  - queue
aliases:
  - ArrayList
  - HashSet
  - ArrayDeque
---

# Listas, conjuntos e filas

> [!abstract] TL;DR
> `Collection` em Java divide-se em três famílias: **`List`** (sequência indexada, permite duplicatas), **`Set`** (sem duplicatas, semanticas de conjunto) e **`Queue`/`Deque`** (acesso pelas pontas). Para listas, `ArrayList` é a escolha padrão — array dinâmico com acesso O(1). Para sets, `HashSet` oferece O(1) médio; `TreeSet` mantém ordem a custo de O(log n). Para filas e pilhas, `ArrayDeque` substitui tanto `Stack` quanto `LinkedList` em praticamente todos os cenários. `PriorityQueue` é um binary min-heap: ideal para problemas de top-K. Conhecer a estrutura interna e o Big-O de cada implementação é pré-requisito para escolher a coleção certa e para entrevistas técnicas.

## O que é

A hierarquia `Collection` organiza todas as estruturas de dados do Java Collections Framework em três interfaces fundamentais:

| Família | Interface-raiz | Contrato central |
|---|---|---|
| **Lista** | `java.util.List` | Sequência **ordenada por índice**; permite duplicatas e null |
| **Conjunto** | `java.util.Set` | **Sem duplicatas**; modela o conceito matemático de conjunto |
| **Fila/Deque** | `java.util.Queue` / `java.util.Deque` | Acesso pelas **pontas** (FIFO, LIFO ou por prioridade) |

Essas interfaces descendem de `java.util.Collection`, que por sua vez estende `java.lang.Iterable`. Todas as implementações da biblioteca padrão são **não sincronizadas** por padrão — para acesso concorrente, ver [[03-Dominios/Java/Concorrência e paralelismo/07 - Concurrent collections|Concurrent collections]].

O princípio de design do framework: **programe sempre contra a interface**, não contra a implementação:

```java
List<String>  nomes  = new ArrayList<>();   // não: ArrayList<String>
Set<String>   vistos = new HashSet<>();
Deque<String> fila   = new ArrayDeque<>();
```

Isso permite trocar a implementação em um único lugar sem alterar o restante do código.

## Por que importa

- **Corretude:** escolher `Set` quando duplicatas são proibidas elimina verificações manuais; escolher `Queue` comunica intenção de acesso FIFO.
- **Performance:** `contains` em `ArrayList` é O(n); o mesmo método em `HashSet` é O(1). Em 1 milhão de elementos a diferença é de segundos vs microssegundos.
- **Legibilidade:** `Deque<T> pilha = new ArrayDeque<>()` expressa "pilha" sem ambiguidade; `Stack<T>` é legado e não deve ser usado em código moderno.
- **Entrevistas:** perguntas sobre Big-O de Collections são frequentes em processos técnicos.

## Como funciona

### `ArrayList` (array dinâmico, acesso O(1)) vs `LinkedList` (lista ligada)

**`ArrayList`** armazena elementos em um array interno que cresce automaticamente (capacidade inicial 10; fator de crescimento ~50% por redimensionamento). O acesso por índice é O(1) pois o array é contíguo na memória.

```java
List<String> produtos = new ArrayList<>();
produtos.add("Notebook");        // O(1) amortizado — append ao final
produtos.add(0, "Monitor");      // O(n) — desloca todos os elementos
String item = produtos.get(1);   // O(1) — acesso direto ao array
produtos.remove("Notebook");     // O(n) — busca linear + deslocamento
```

**`LinkedList`** é uma lista duplamente encadeada (doubly-linked list): cada nó guarda referência ao anterior e ao próximo. Operações nas pontas são O(1), mas acesso por índice exige travessia e é O(n). O problema prático mais grave é a **localidade de cache**: os nós ficam espalhados pela memória heap, causando cache misses frequentes, o que torna `LinkedList` mais lento que `ArrayList` em iterações mesmo quando a complexidade teórica seria equivalente.

```java
// LinkedList na memória — nós espalhados:
// [nó 0, addr:0x1A] → [nó 1, addr:0x9F] → [nó 2, addr:0x3C]
//
// ArrayList na memória — contíguo (cache-friendly):
// [0][1][2][3][4]
```

A única vantagem real de `LinkedList` é inserção/remoção O(1) na primeira posição — e para esse caso `ArrayDeque` costuma ser mais adequado.

---

### `HashSet` / `LinkedHashSet` / `TreeSet` (dedup, ordem, Red-Black tree)

**`HashSet`** é implementado sobre um `HashMap` interno. Operações `add`, `remove` e `contains` são O(1) médio (dependem da qualidade da função hash). Não garante ordem de iteração. Permite um elemento `null`.

```java
Set<String> categorias = new HashSet<>();
categorias.add("Backend");
categorias.add("Frontend");
categorias.add("Backend");   // ignorado — já existe
System.out.println(categorias.size()); // 2
```

**`LinkedHashSet`** estende `HashSet` acrescentando uma lista duplamente encadeada que mantém a **ordem de inserção**. Mesmas complexidades de `HashSet`; iteração ligeiramente mais lenta que `HashSet` mas mais previsível.

**`TreeSet`** é baseado em `TreeMap`, que usa uma **Red-Black tree** (árvore rubro-negra balanceada). Mantém os elementos em **ordem natural** (via `Comparable`) ou por `Comparator` passado ao construtor. Operações de modificação e busca são O(log n). Não permite `null` com ordenação natural.

```java
TreeSet<String> ordenado = new TreeSet<>();
ordenado.add("Zebra");
ordenado.add("Abelha");
ordenado.add("Mango");
System.out.println(ordenado.first()); // "Abelha"
System.out.println(ordenado.last());  // "Zebra"

// range-views (backed by original — não cópias)
SortedSet<String> sub = ordenado.headSet("M"); // {"Abelha"}
```

`TreeSet` também implementa `NavigableSet`, expondo métodos como `ceiling(e)`, `floor(e)`, `higher(e)`, `lower(e)` para consultas de vizinhança em O(log n).

---

### `Queue`/`Deque`: `ArrayDeque` (FIFO/LIFO, substitui `Stack`/`Vector`) e `PriorityQueue` (binary heap, top-K)

**`ArrayDeque`** usa um **array circular redimensionável** (capacidade inicial 16). Todas as operações nas pontas são O(1) amortizado. É a implementação recomendada tanto para filas (FIFO) quanto para pilhas (LIFO) — substitui `Stack` (legado, sincronizado desnecessariamente) e `LinkedList` (cache locality ruim). Não permite `null`.

```java
// Como fila (FIFO)
Deque<String> fila = new ArrayDeque<>();
fila.offer("primeiro");   // addLast — O(1)
fila.offer("segundo");
String head = fila.poll(); // removeFirst — O(1) → "primeiro"

// Como pilha (LIFO)
Deque<String> pilha = new ArrayDeque<>();
pilha.push("base");       // addFirst — O(1)
pilha.push("topo");
String top = pilha.pop(); // removeFirst — O(1) → "topo"
```

**`PriorityQueue`** é um **binary min-heap** armazenado em array. O elemento de menor prioridade (segundo `Comparable` ou `Comparator`) fica sempre na raiz e é retornado por `peek()` em O(1). Inserção (`offer`) e remoção do topo (`poll`) são O(log n). Busca arbitrária (`contains`, `remove(Object)`) é O(n). Não permite `null`. A iteração **não garante ordem** — para extrair em ordem, use `poll()` em loop.

```java
// Min-heap padrão (menor elemento na frente)
PriorityQueue<Integer> pq = new PriorityQueue<>();
pq.offer(30);
pq.offer(10);
pq.offer(20);
System.out.println(pq.peek());  // 10 — O(1)
System.out.println(pq.poll());  // 10 — O(log n)
System.out.println(pq.poll());  // 20

// Max-heap (maior elemento na frente)
PriorityQueue<Integer> maxPq = new PriorityQueue<>(Comparator.reverseOrder());
```

---

### Complexidade comparada (tabela Big-O)

| Estrutura | `add` (fim) | `get(i)` | `remove(i)` | `contains` | Iteração |
|---|---|---|---|---|---|
| `ArrayList` | O(1)* | O(1) | O(n) | O(n) | O(n) |
| `LinkedList` | O(1) | O(n) | O(n)† | O(n) | O(n)‡ |
| `HashSet` | O(1)* | — | O(1)* | O(1)* | O(n+m) |
| `LinkedHashSet` | O(1)* | — | O(1)* | O(1)* | O(n) |
| `TreeSet` | O(log n) | — | O(log n) | O(log n) | O(n) |
| `ArrayDeque` | O(1)* | — | O(n) | O(n) | O(n) |
| `PriorityQueue` | O(log n) | — | O(n) | O(n) | O(n)§ |

\* amortizado  
† O(1) se referência ao nó for conhecida; O(n) para `remove(index)`  
‡ O(n) teórico, mas na prática mais lento que `ArrayList` por cache misses  
§ iteração não garante ordem de prioridade; use `poll()` para extrair em ordem

## Na prática

**`ArrayList` para acesso por índice:**

```java
// Relatório de produtos em ordem de inserção
List<String> relatorio = new ArrayList<>();
relatorio.add("Produto A");
relatorio.add("Produto B");
relatorio.add("Produto C");

// Acesso por posição — O(1)
String primeiro = relatorio.get(0);

// Iteração eficiente — O(n), cache-friendly
for (String p : relatorio) {
    System.out.println(p);
}
```

**`ArrayDeque` como pilha (desfazer operações):**

```java
// Histórico de ações — pilha LIFO
Deque<String> historico = new ArrayDeque<>();
historico.push("criar pedido #100");
historico.push("adicionar item A");
historico.push("alterar quantidade");

// Desfazer última ação
String ultimaAcao = historico.pop(); // "alterar quantidade"
System.out.println("Desfeito: " + ultimaAcao);
```

**`PriorityQueue` para top-K de `Order` por valor:**

```java
record Order(String id, double value) {}

// Top-3 pedidos de menor valor (min-heap de tamanho K)
int K = 3;
PriorityQueue<Order> topK = new PriorityQueue<>(
    Comparator.comparingDouble(Order::value).reversed()
    // max-heap: remove o maior quando ultrapassa K
);

List<Order> pedidos = List.of(
    new Order("A", 500.0),
    new Order("B", 120.0),
    new Order("C", 350.0),
    new Order("D", 80.0),
    new Order("E", 200.0)
);

for (Order o : pedidos) {
    topK.offer(o);
    if (topK.size() > K) {
        topK.poll(); // descarta o maior, mantém os K menores
    }
}

// topK contém os 3 pedidos de menor valor
while (!topK.isEmpty()) {
    System.out.println(topK.poll().id()); // ordem pode variar
}
```

## Armadilhas

### (1) Usar `LinkedList` por reflexo esperando ganho de performance

**O problema:** é tentador escolher `LinkedList` quando se esperam inserções e remoções frequentes — afinal, a teoria diz O(1) para adicionar ao início. Na prática, `LinkedList` quase sempre perde para `ArrayList` porque cada nó é um objeto alocado separadamente no heap, causando **cache misses** em série durante a travessia. Processadores modernos dependem fortemente do cache L1/L2; dados não contíguos resultam em latências 10-100x maiores por acesso.

```java
// Tentação: "vou inserir no início com frequência — LinkedList é O(1)!"
List<String> itens = new LinkedList<>();
for (int i = 0; i < 1_000_000; i++) {
    itens.add(0, "item-" + i); // O(1) para o link, mas cache miss em cada nó
}

// Na prática: ArrayList é mais rápido mesmo para inserção no início
// em listas de tamanho moderado, pois o deslocamento em memória contígua
// é barato para o processador comparado com pointer chasing.
```

**Fix:** meça antes de otimizar. Use `ArrayList` como padrão. Se precisar de inserção/remoção eficiente nas pontas, use `ArrayDeque`. Só use `LinkedList` se benchmarks concretos justificarem.

---

### (2) Usar `contains` em `ArrayList` para busca frequente

**O problema:** `ArrayList.contains(Object)` percorre o array elemento por elemento — O(n). Em um loop de verificação com milhares de chamadas, isso degrada para O(n²) na prática.

```java
List<String> permissoes = new ArrayList<>(
    List.of("READ", "WRITE", "DELETE", "ADMIN")
);

// BUG de performance: O(n) por chamada
List<String> acoes = obterAcoes(); // pode ter milhares
for (String acao : acoes) {
    if (permissoes.contains(acao)) { // O(n) aqui dentro do loop
        executar(acao);
    }
}
```

**Fix:** quando `contains` é chamado com frequência, use `HashSet` — que oferece O(1) médio:

```java
Set<String> permissoes = new HashSet<>(
    List.of("READ", "WRITE", "DELETE", "ADMIN")
);

for (String acao : acoes) {
    if (permissoes.contains(acao)) { // O(1) médio
        executar(acao);
    }
}
```

Se a ordem de inserção precisar ser preservada, use `LinkedHashSet`.

---

### (3) Inserir objetos sem `Comparable`/`Comparator` em `TreeSet`

**O problema:** `TreeSet` precisa comparar elementos para mantê-los ordenados. Se o elemento não implementa `Comparable` e nenhum `Comparator` foi fornecido ao construtor, a operação `add` lança `ClassCastException` em tempo de execução — não em compilação.

```java
class Category {
    String name;
    Category(String name) { this.name = name; }
    // SEM implements Comparable<Category>
}

TreeSet<Category> cats = new TreeSet<>();
cats.add(new Category("Backend"));  // OK, primeiro elemento
cats.add(new Category("Frontend")); // ClassCastException!
// java.lang.ClassCastException: Category cannot be cast to java.lang.Comparable
```

O erro é silencioso até o segundo `add` porque o heap compara o novo elemento com os existentes — e só há comparação quando há mais de um elemento.

**Fix:** implemente `Comparable<T>` na classe ou passe um `Comparator` ao construtor:

```java
// Opção 1: Comparable na classe
class Category implements Comparable<Category> {
    String name;
    @Override
    public int compareTo(Category other) {
        return this.name.compareTo(other.name);
    }
}

// Opção 2: Comparator externo (não altera a classe)
TreeSet<Category> cats = new TreeSet<>(
    Comparator.comparing(c -> c.name)
);
```

Lembre-se também que `TreeSet` **não aceita `null`** com ordenação natural — `null` não é `Comparable` e lançará `NullPointerException`.

## Em entrevista

### Frase pronta (inglês)

> "The three main families under `Collection` are `List`, `Set`, and `Queue`/`Deque`, each with distinct contracts. For lists, `ArrayList` is the go-to choice: it's backed by a dynamic array, giving O(1) random access and amortized O(1) appends. `LinkedList` is almost never the right pick in practice despite its theoretical O(1) head insertions, because poor cache locality means pointer-chasing overhead outweighs the algorithmic benefit in real workloads — I'd measure before choosing it. For sets, `HashSet` gives O(1) average for add, remove, and contains; `TreeSet` uses a Red-Black tree and keeps elements in sorted order at O(log n) cost, but requires elements to be `Comparable` or a `Comparator` to be supplied — otherwise you get a `ClassCastException` at runtime. For queues and stacks, `ArrayDeque` is the modern replacement for both the legacy `Stack` class and `LinkedList`: it uses a resizable circular array, delivers O(1) amortized operations at both ends, and has better cache performance. `PriorityQueue` is a binary min-heap — peek is O(1), offer and poll are O(log n) — and it's the natural fit for top-K problems."

### Vocabulário

| Termo PT | Termo EN |
|---|---|
| lista | list |
| conjunto | set |
| fila | queue |
| pilha | stack |
| fila de dois extremos | deque (double-ended queue) |
| fila de prioridade | priority queue |
| heap binário / heap mínimo | binary heap / min-heap |
| árvore rubro-negra | Red-Black tree |
| localidade de cache | cache locality |
| falha de cache | cache miss |
| acesso aleatório | random access |
| complexidade amortizada | amortized complexity |

## Veja também

- [[01 - O Collections Framework]]
- [[03 - Mapas]]
- [[06 - Comparable e Comparator]]
- [[03-Dominios/Java/Collections e Streams/index|Collections e Streams (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Concorrência e paralelismo/07 - Concurrent collections|Concurrent collections]]
- [[03-Dominios/Java/Dicionário de Java#Deque|Deque]]
- [[03-Dominios/Java/Dicionário de Java#PriorityQueue|PriorityQueue]]

## Referências

- [Collections Implementations — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/collections/implementations/index.html)
- [Class ArrayList — Java SE 21 API (docs.oracle.com)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/ArrayList.html)
- [Class LinkedList — Java SE 21 API (docs.oracle.com)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/LinkedList.html)
- [Class HashSet — Java SE 21 API (docs.oracle.com)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/HashSet.html)
- [Class TreeSet — Java SE 21 API (docs.oracle.com)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/TreeSet.html)
- [Class ArrayDeque — Java SE 21 API (docs.oracle.com)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/ArrayDeque.html)
- [Class PriorityQueue — Java SE 21 API (docs.oracle.com)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/PriorityQueue.html)
