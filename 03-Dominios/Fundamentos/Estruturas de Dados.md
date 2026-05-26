---
title: "Estruturas de Dados"
created: 2026-04-01
updated: 2026-04-09
type: concept
status: evergreen
tags:
  - fundamentos
  - entrevista
publish: false
---

# Estruturas de Dados

Formas de organizar e armazenar dados que determinam a eficiência das operações sobre eles. A escolha correta impacta diretamente performance, consumo de memória, legibilidade e — em entrevistas — demonstra maturidade técnica.

## O que é

Uma estrutura de dados é uma coleção organizada com um **contrato de operações** (inserir, remover, buscar, iterar) e **complexidades conhecidas** para cada uma. Em entrevistas, a pergunta raramente é "o que é um hashmap" — é "qual estrutura você usaria para X e por quê". O foco é sempre em **trade-offs**.

Três dimensões para comparar estruturas:

1. **Tempo** — complexidade das operações (Big O)
2. **Espaço** — memória consumida e overhead por elemento
3. **Ordem** — mantém ordem de inserção? ordenação natural? nenhuma ordem?

## Como escolher (framework de decisão)

Antes de codar, responda:

1. **Qual é o padrão de acesso dominante?** (lookup, iteração, top-K, range query?)
2. **Há chave natural?** (se sim → hash ou tree; se não → array/list)
3. **Preciso de ordem?** (inserção → LinkedHashMap; natural → TreeMap; nenhuma → HashMap)
4. **O tamanho é conhecido?** (fixo → array; dinâmico → ArrayList/Map)
5. **Há concorrência?** (sim → `ConcurrentHashMap`, `CopyOnWriteArrayList`)
6. **Preciso de duplicatas?** (sim → List; não → Set)

---

## Arrays

Bloco fundamental: região contígua de memória com tamanho fixo e acesso O(1) por índice.

### Características

- **Acesso aleatório O(1)** — calcula-se `endereço_base + índice * tamanho_elemento`.
- **Localidade de cache excelente** — elementos vizinhos estão próximos em memória, o CPU faz pré-fetch eficiente.
- **Tamanho fixo** — em Java, um `int[10]` não cresce. Para crescer, aloca-se novo array e copia.
- **Inserção/remoção no meio é O(n)** — todos os elementos à direita precisam deslocar.

### Em Java

```java
int[] numeros = new int[10];
numeros[0] = 42;
int len = numeros.length; // 10

// Inicialização literal
String[] nomes = {"Ana", "Bruno", "Carla"};

// Cópia e redimensionamento
int[] maior = Arrays.copyOf(numeros, 20);

// Ordenação
Arrays.sort(nomes);

// Stream
int soma = Arrays.stream(numeros).sum();
```

### ArrayList (array dinâmico)

`ArrayList` encapsula um array interno e redimensiona automaticamente (geralmente dobrando a capacidade). Operações:

- `add(e)` — O(1) amortizado (às vezes paga O(n) de cópia ao redimensionar)
- `get(i)` — O(1)
- `add(i, e)` / `remove(i)` no meio — O(n)
- `contains(e)` — O(n) (busca linear)

```java
List<String> lista = new ArrayList<>();
lista.add("Ana");
lista.add("Bruno");
lista.get(0);          // "Ana"
lista.remove(0);       // desloca todos à esquerda
lista.size();
```

### Em TypeScript

```typescript
const numeros: number[] = [1, 2, 3];
numeros.push(4);          // O(1) amortizado
numeros.pop();            // O(1)
numeros.unshift(0);       // O(n) — desloca tudo
const primeiro = numeros[0]; // O(1)

// Operações funcionais (todas O(n))
const dobrados = numeros.map(n => n * 2);
const pares    = numeros.filter(n => n % 2 === 0);
const soma     = numeros.reduce((acc, n) => acc + n, 0);
```

> **Nota:** arrays em JS/TS são na verdade objetos indexados, com otimizações V8 quando mantidos densos e homogêneos. Arrays esparsos (`arr[1000] = 1` sem preencher intermediários) perdem essas otimizações.

### Quando usar

- Acesso por índice é dominante
- Iteração sequencial frequente (cache-friendly)
- Tamanho previsível ou crescimento pelo final
- Padrão de "two pointers", "sliding window", "prefix sum" em coding challenges

---

## Listas Encadeadas (Linked Lists)

Nós independentes conectados por ponteiros. Cada nó armazena o dado e uma (ou duas) referências para os vizinhos.

### Singly vs Doubly

- **Singly linked:** cada nó aponta apenas para o próximo. Menor overhead, mas só permite percorrer em uma direção.
- **Doubly linked:** cada nó aponta para o anterior e o próximo. Permite percorrer em ambas direções e remoção O(1) dado o nó — `java.util.LinkedList` é doubly linked.

### Operações

| Operação                  | Array/ArrayList | LinkedList                   |
| ------------------------- | --------------- | ---------------------------- |
| Acesso por índice         | O(1)            | O(n)                         |
| Inserção no início        | O(n)            | O(1)                         |
| Inserção no final         | O(1)*           | O(1)**                       |
| Remoção no meio (com ref) | O(n)            | O(1)                         |
| Busca por valor           | O(n)            | O(n)                         |
| Memória por elemento      | baixo           | alto (overhead de ponteiros) |

\* Amortizado. \*\* Se tiver ponteiro para o tail.

### Em Java

```java
LinkedList<String> fila = new LinkedList<>();
fila.addFirst("A");
fila.addLast("B");
fila.removeFirst();   // O(1)
fila.get(5);          // O(n) — percorre do início
```

### Trade-off prático

> Na maioria dos casos em backend Java, **ArrayList vence LinkedList** mesmo em cenários "teoricamente" favoráveis à lista encadeada. Razão: localidade de cache. Percorrer 10.000 inteiros em array é ordens de magnitude mais rápido que em linked list por causa de cache misses. LinkedList só brilha quando você precisa de inserção/remoção frequente **com referência direta ao nó** (não por índice).

### Quando usar

- Implementação de filas, pilhas e deques
- LRU cache (combinado com HashMap para lookup)
- Quando o custo de `System.arraycopy` dos arrays dinâmicos se torna gargalo comprovado por profiling

---

## Hash Tables

A estrutura mais importante para entrevistas de backend. Oferece inserção, remoção e busca em O(1) amortizado via função de hash.

### Como funciona

1. A chave passa por uma **função de hash** que produz um inteiro.
2. O inteiro é mapeado para um **bucket** (`hash % capacity`).
3. O par chave-valor é armazenado nesse bucket.
4. **Colisões** (duas chaves no mesmo bucket) são resolvidas por:
   - **Chaining** — cada bucket é uma lista encadeada (ou árvore a partir de um threshold, como em Java 8+).
   - **Open addressing** — probing: tenta o próximo slot livre (linear, quadrático, double hashing).

### Load factor e rehashing

Quando `tamanho / capacidade > load_factor` (default 0.75 em Java), a tabela **rehashia**: aloca nova tabela com o dobro de buckets e reinsere tudo. Isso é O(n) e paga-se ocasionalmente — por isso dizemos "O(1) amortizado".

### hashCode + equals contract (Java)

Regra crítica ao usar objetos como chave:

1. Se `a.equals(b)` então `a.hashCode() == b.hashCode()`.
2. Se sobrescreve `equals`, **sempre** sobrescreva `hashCode`.
3. Hash deve ser estável ao longo da vida da chave (não dependa de campos mutáveis).

```java
public class Cpf {
    private final String numero;

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Cpf other)) return false;
        return numero.equals(other.numero);
    }

    @Override
    public int hashCode() {
        return numero.hashCode();
    }
}
```

### HashMap, HashSet, LinkedHashMap, TreeMap

| Estrutura       | Ordem                | Complexidade | Uso típico                              |
| --------------- | -------------------- | ------------ | --------------------------------------- |
| `HashMap`       | nenhuma              | O(1)         | lookup geral, cache, contagem           |
| `LinkedHashMap` | inserção (ou acesso) | O(1)         | LRU cache, preservar ordem de chegada   |
| `TreeMap`       | natural (Comparable) | O(log n)     | range queries, ordenado                 |
| `HashSet`       | nenhuma              | O(1)         | deduplicação, verificação de existência |
| `TreeSet`       | natural              | O(log n)     | conjunto ordenado                       |

```java
Map<String, Integer> freq = new HashMap<>();
for (String palavra : texto.split(" ")) {
    freq.merge(palavra, 1, Integer::sum);
}

// LRU cache simples
Map<String, String> lru = new LinkedHashMap<>(16, 0.75f, true) {
    protected boolean removeEldestEntry(Map.Entry<String, String> eldest) {
        return size() > 100;
    }
};
```

### Em JS/TS

```typescript
// Map (recomendado): aceita qualquer chave, preserva ordem de inserção
const cache = new Map<string, User>();
cache.set("u1", user);
cache.get("u1");
cache.has("u1");
cache.delete("u1");
cache.size;

// Set: deduplicação
const unicos = new Set([1, 2, 2, 3]); // {1, 2, 3}

// Object: cuidado — chaves são sempre strings (ou Symbol)
const obj: Record<string, number> = {};
obj["foo"] = 1;
```

> **`Map` vs `Object` em JS:** prefira `Map` quando as chaves são dinâmicas, quando precisa iterar em ordem de inserção, ou quando quer suporte a chaves não-string. `Object` ainda vence para shapes fixos conhecidos (melhor JIT).

### Quando usar

- Lookup por chave única — cache, índice secundário
- Contagem de frequência
- Deduplicação (Set)
- Memoization
- Verificação rápida de existência

### Armadilhas

- Usar objeto mutável como chave e depois mutá-lo — o hash muda e a entrada fica "perdida"
- Esquecer de sobrescrever `hashCode` ao sobrescrever `equals`
- Assumir ordem de iteração em `HashMap` (use `LinkedHashMap` se precisar)
- Usar `HashMap` em cenário concorrente — use `ConcurrentHashMap`

---

## Árvores (Trees)

Estrutura hierárquica onde cada nó tem zero ou mais filhos. O nó sem pai é a **raiz**; nós sem filhos são **folhas**.

### Binary Search Tree (BST)

Cada nó tem até dois filhos. Invariante: `esquerda < nó < direita`. Busca, inserção e remoção são O(log n) **no caso médio**, O(n) no pior (árvore degenerada em lista).

### Árvores balanceadas

**AVL** e **Red-Black Trees** mantêm a altura em O(log n) através de rotações. Java usa Red-Black em `TreeMap` e `TreeSet`.

```java
TreeMap<Integer, String> ordenado = new TreeMap<>();
ordenado.put(3, "três");
ordenado.put(1, "um");
ordenado.put(2, "dois");

ordenado.firstKey();              // 1
ordenado.lastKey();               // 3
ordenado.floorKey(2);             // 2 (maior chave <= 2)
ordenado.ceilingKey(2);           // 2 (menor chave >= 2)
ordenado.subMap(1, 3);            // range query
```

### Heap (Priority Queue)

Árvore binária **completa** onde o pai é sempre ≥ (max-heap) ou ≤ (min-heap) que os filhos. Implementada tipicamente como array.

- **Inserção e remoção do topo:** O(log n)
- **Leitura do topo (peek):** O(1)
- **Não é ordenada globalmente** — só garante a relação pai/filho.

```java
// Min-heap (padrão)
PriorityQueue<Integer> minHeap = new PriorityQueue<>();
minHeap.offer(5);
minHeap.offer(1);
minHeap.offer(3);
minHeap.peek();  // 1
minHeap.poll();  // 1 (remove)

// Max-heap
PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Comparator.reverseOrder());

// Top-K problema clássico: K maiores elementos
PriorityQueue<Integer> topK = new PriorityQueue<>();
for (int n : numeros) {
    topK.offer(n);
    if (topK.size() > k) topK.poll();
}
```

### Trie (árvore de prefixos)

Árvore onde cada nó representa um caractere. Caminho da raiz até um nó forma um prefixo. Operações em O(L) onde L é o tamanho da string.

**Uso típico:** autocomplete, verificação de dicionário, filtros de palavras.

```
      (root)
      /  |  \
     c   d   p
     |   |   |
     a   o   i
     |   |   |
     t   g   e
```

### B-Tree e B+Tree

Árvores multi-way (cada nó tem muitas chaves e muitos filhos) otimizadas para armazenamento em disco. **É o que indexa seu banco de dados**: PostgreSQL, MySQL, Oracle — todos usam B-Tree ou B+Tree para índices. Altura baixa minimiza I/O de disco.

### Quando usar árvores

- **TreeMap/TreeSet:** quando você precisa de ordenação E busca eficiente E range queries
- **PriorityQueue:** top-K, merge de listas ordenadas, Dijkstra, scheduling
- **Trie:** buscas por prefixo, autocomplete
- **BST balanceada:** fundamento para entender índices de banco

---

## Grafos (Graphs)

Conjunto de **vértices** (nós) conectados por **arestas**. Modelam redes sociais, rotas, dependências, fluxos.

### Representações

| Representação        | Espaço   | Verificar aresta | Iterar vizinhos |
| -------------------- | -------- | ---------------- | --------------- |
| Matriz de adjacência | O(V²)    | O(1)             | O(V)            |
| Lista de adjacência  | O(V + E) | O(grau)          | O(grau)         |

**Regra prática:** use lista de adjacência (99% dos casos). Matriz só vale para grafos densos ou quando verificar a existência de uma aresta específica é a operação dominante.

```java
// Lista de adjacência com HashMap
Map<Integer, List<Integer>> grafo = new HashMap<>();
grafo.computeIfAbsent(1, k -> new ArrayList<>()).add(2);
grafo.computeIfAbsent(1, k -> new ArrayList<>()).add(3);
```

### Tipos

- **Direcionado vs não-direcionado** — arestas têm sentido ou não
- **Ponderado** — arestas têm peso (distância, custo, latência)
- **Cíclico vs acíclico** — DAG (Directed Acyclic Graph) é base para topological sort
- **Conectado** — existe caminho entre qualquer par de vértices

### Algoritmos essenciais

- **BFS** (Breadth-First Search) — fila. Caminho mais curto em grafos **não ponderados**. Explora em camadas.
- **DFS** (Depth-First Search) — pilha (ou recursão). Detecção de ciclos, topological sort, componentes conexos.
- **Dijkstra** — caminho mais curto em grafos **ponderados com pesos não-negativos**. Usa priority queue. O((V + E) log V).
- **Bellman-Ford** — como Dijkstra, mas aceita pesos negativos. O(V × E).
- **Topological Sort** — ordena vértices de um DAG respeitando dependências. Base para build systems, task schedulers.
- **Union-Find (Disjoint Set)** — detecta componentes conexos e ciclos em tempo quase O(1) amortizado.

### Onde aparecem em sistemas reais

- **Redes sociais** — amigos, sugestões (BFS de 2 níveis)
- **Maps/rotas** — Dijkstra, A*
- **Build systems** — topological sort de dependências (Gradle, Maven)
- **Dependency injection** — grafo de beans no Spring
- **Git** — commits formam um DAG

---

## Stacks e Queues

### Stack (Pilha) — LIFO

Última a entrar, primeira a sair. Operações O(1): `push`, `pop`, `peek`.

**Usos clássicos:**

- Call stack da JVM / navegador
- Parsing de expressões (balanceamento de parênteses)
- Undo/redo
- DFS iterativo
- Backtracking

```java
Deque<Integer> pilha = new ArrayDeque<>(); // preferir sobre Stack (legacy)
pilha.push(1);
pilha.push(2);
pilha.peek();  // 2
pilha.pop();   // 2
```

> **Por que `ArrayDeque` e não `Stack`?** A classe `java.util.Stack` é legacy (estende `Vector`, sincronizado desnecessariamente). `ArrayDeque` é mais rápido e recomendado como stack e queue.

### Queue (Fila) — FIFO

Primeira a entrar, primeira a sair. Operações O(1): `offer`, `poll`, `peek`.

**Usos clássicos:**

- BFS
- Message queues (Kafka, RabbitMQ)
- Task scheduling
- Buffers (producer-consumer)

```java
Queue<Integer> fila = new ArrayDeque<>();
fila.offer(1);
fila.offer(2);
fila.peek();  // 1
fila.poll();  // 1
```

### Deque (Double-Ended Queue)

Permite inserção e remoção em **ambas as pontas**. Generaliza stack e queue.

```java
Deque<Integer> deque = new ArrayDeque<>();
deque.addFirst(1);
deque.addLast(2);
```

### Priority Queue

Ver seção [Heap](#heap-priority-queue). O elemento de maior prioridade sai primeiro, independentemente da ordem de inserção.

---

## Estruturas especializadas (para demonstrar senioridade)

Raramente cobradas em coding challenges, mas mencioná-las em system design impressiona.

### LRU Cache

Cache de tamanho fixo que remove o elemento **menos recentemente usado** quando atinge capacidade. Implementação: `HashMap` + doubly linked list (ou `LinkedHashMap` com access order).

```java
// Implementação concisa via LinkedHashMap
class LRUCache<K, V> extends LinkedHashMap<K, V> {
    private final int capacity;
    public LRUCache(int capacity) {
        super(capacity, 0.75f, true); // accessOrder = true
        this.capacity = capacity;
    }
    protected boolean removeEldestEntry(Map.Entry<K, V> eldest) {
        return size() > capacity;
    }
}
```

### Bloom Filter

Estrutura probabilística que responde "este elemento **pode estar** no conjunto" ou "**definitivamente não está**". Usa múltiplas funções de hash e um bit array. **Falsos positivos sim, falsos negativos não.**

**Uso típico:** evitar queries caras a banco/disco ("esse ID existe?"), caches distribuídos, web crawlers.

### Skip List

Listas encadeadas com múltiplas camadas de "atalhos" que permitem busca em O(log n). Alternativa probabilística a árvores balanceadas, mais simples de implementar. Usada no Redis para sorted sets.

### Disjoint Set (Union-Find)

Mantém partições de um conjunto. Operações `union` e `find` em quase O(1) com path compression e union by rank. Essencial em algoritmos de grafos (Kruskal MST, detecção de ciclos).

---

## Complexidade comparativa

| Estrutura             | Acesso | Busca    | Inserção    | Remoção  | Espaço   | Ordem           |
| --------------------- | ------ | -------- | ----------- | -------- | -------- | --------------- |
| Array                 | O(1)   | O(n)     | O(n)        | O(n)     | O(n)     | inserção        |
| ArrayList             | O(1)   | O(n)     | O(1) amort. | O(n)     | O(n)     | inserção        |
| LinkedList            | O(n)   | O(n)     | O(1)*       | O(1)*    | O(n)     | inserção        |
| Stack / Queue / Deque | O(n)   | O(n)     | O(1)        | O(1)     | O(n)     | inserção        |
| HashMap / HashSet     | —      | O(1)     | O(1)        | O(1)     | O(n)     | nenhuma         |
| LinkedHashMap         | —      | O(1)     | O(1)        | O(1)     | O(n)     | inserção/acesso |
| TreeMap / TreeSet     | —      | O(log n) | O(log n)    | O(log n) | O(n)     | natural         |
| Heap (PriorityQueue)  | —      | O(n)     | O(log n)    | O(log n) | O(n)     | parcial         |
| Trie                  | —      | O(L)     | O(L)        | O(L)     | O(A·N·L) | lexicográfica   |
| BST desbalanceada     | —      | O(n)     | O(n)        | O(n)     | O(n)     | natural         |

\* Com referência ao nó. L = comprimento da string; A = alfabeto; N = número de strings.

---

## Patterns comuns em coding interviews

Reconhecer o pattern é metade do problema:

| Sinal no enunciado                          | Estrutura / técnica           |
| ------------------------------------------- | ----------------------------- |
| "qual é o par com soma X"                   | HashMap (complemento)         |
| "primeira ocorrência repetida"              | HashSet                       |
| "k maiores / menores elementos"             | Heap de tamanho k             |
| "intervalo / janela de tamanho fixo"        | Sliding window                |
| "subarray contíguo com soma X"              | Prefix sum + HashMap          |
| "parênteses balanceados" / parsing          | Stack                         |
| "caminho mais curto" em grafo não-ponderado | BFS                           |
| "caminho mais curto" com pesos              | Dijkstra                      |
| "ordem de execução com dependências"        | Topological sort (DFS)        |
| "autocomplete / busca por prefixo"          | Trie                          |
| "LRU / cache com expiração"                 | LinkedHashMap / HashMap + DLL |
| "mediana em stream"                         | Dois heaps (min + max)        |
| "intervalo ordenado / range query"          | TreeMap                       |
| "detectar ciclo"                            | DFS com estados ou Union-Find |

---

## Armadilhas comuns

- **Confundir ArrayList com LinkedList:** em Java, ArrayList vence em quase todos os cenários. LinkedList só em cenários muito específicos de inserção/remoção por referência.
- **Usar `Stack` em vez de `ArrayDeque`:** `Stack` é legacy e sincronizado.
- **Esquecer `hashCode()`/`equals()`** ao usar objetos custom como chave em HashMap.
- **Mutar chaves de HashMap** — o hash muda e a entrada fica inacessível.
- **Assumir ordem em HashMap** — use `LinkedHashMap` ou `TreeMap` se a ordem importa.
- **HashMap em cenário concorrente** — use `ConcurrentHashMap`. Estruturas comuns não são thread-safe.
- **Ignorar fator de carga** — HashMap degradado com muitas colisões vira O(n).
- **Usar matriz de adjacência para grafos esparsos** — desperdício de memória. Use lista de adjacência.
- **Recursão profunda em DFS** sem considerar stack overflow — para grafos grandes, converta para iterativo com stack explícito.
- **Escolher TreeMap quando HashMap basta** — O(log n) desnecessário se a ordem não importa.
- **`PriorityQueue` sem `Comparator`** quando os elementos não implementam `Comparable` — erro em runtime.

---

## Na prática (da minha experiência)

> No MedEspecialista, usei intensamente `HashMap` como cache em memória de configurações carregadas no boot e consultadas em hot paths — evitando round-trips ao banco para dados quase-estáticos. Para um endpoint que precisava retornar os **10 médicos mais bem avaliados**, usei um `PriorityQueue` de tamanho fixo 10 como min-heap, mantendo apenas os top-10 enquanto iterava o resultado do banco — O(n log k) em vez de O(n log n) de um sort completo.
>
> Em outro projeto (Digidados), precisei ordenar e fazer range queries sobre leituras de sensores por timestamp: `TreeMap<Long, Reading>` entregou `subMap(inicio, fim)` elegante sem precisar de query extra ao banco.
>
> Um caso onde LinkedList fez sentido: uma fila de replay de eventos onde eu adicionava no final e removia do começo em alta frequência, sem jamais acessar por índice — `ArrayDeque` seria ainda melhor, e foi a escolha final depois do profiling mostrar cache misses.

---

## How to explain in English

When discussing data structures in an interview, the goal isn't reciting definitions — it's showing you reason about **trade-offs**.

> "The data structure I choose depends on the access pattern. If I need constant-time lookups by a unique key, I reach for a hash map — `HashMap` in Java, `Map` in TypeScript. If I also need the keys to be sorted, or I need range queries, I use a `TreeMap`, which trades O(1) for O(log n) to give me ordering and operations like `floorKey` and `subMap`.
>
> For top-K problems — say, the ten most-recent events or the five highest scores — I use a priority queue of fixed size K. That turns what would be an O(n log n) sort into an O(n log k) pass, which matters when n is large.
>
> For modeling relationships — users and their friends, services and their dependencies — I think in graphs. Adjacency lists by default; adjacency matrices only when the graph is dense and edge-existence checks dominate.
>
> One thing I've learned is that in most backend code, ninety percent of the work is done by arrays, hash maps, and queues. Knowing when to reach for something more specialized — a trie for autocomplete, a bloom filter to avoid expensive lookups, an LRU cache to bound memory — is what separates a senior from a junior. But reaching for them unnecessarily is its own mistake: complexity has a cost."

### Frases úteis para pivotar trade-offs

- "I'd trade a bit of memory for faster lookups here."
- "The naive approach is O(n²), but with a hash map we can bring it down to O(n)."
- "It depends on whether reads or writes dominate."
- "This is O(log n) amortized — worst case is O(n) during rehashing, but that happens rarely."
- "I'd profile before optimizing, but my first instinct is..."

### Key vocabulary

- lista encadeada → linked list
- lista duplamente encadeada → doubly linked list
- árvore binária de busca → binary search tree (BST)
- árvore balanceada → balanced tree / self-balancing tree
- tabela hash → hash table / hash map
- colisão → collision
- fator de carga → load factor
- rehashing → rehashing
- pilha → stack
- fila → queue
- fila de prioridade → priority queue
- heap de mínimo / máximo → min-heap / max-heap
- grafo direcionado acíclico → directed acyclic graph (DAG)
- busca em largura → breadth-first search (BFS)
- busca em profundidade → depth-first search (DFS)
- ordenação topológica → topological sort
- caminho mais curto → shortest path
- complexidade de tempo / espaço → time / space complexity
- amortizado → amortized
- pior caso / caso médio → worst case / average case
- localidade de cache → cache locality
- contíguo em memória → contiguous in memory

---

## Recursos

- [Visualgo](https://visualgo.net/) — visualização interativa de estruturas e algoritmos
- [Big-O Cheat Sheet](https://bigocheatsheet.com/) — referência rápida de complexidades
- [Algorithms, Part I](https://www.coursera.org/learn/algorithms-part1) e [Part II](https://www.coursera.org/learn/algorithms-part2) — Princeton (Sedgewick), Coursera
- [NeetCode 150](https://neetcode.io/) — trilha de problemas categorizada por padrão
- [Java Collections Framework docs](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/package-summary.html)

## Veja também

- [[Algoritmos]]
- [[Orientação a Objetos]]
- [[Java Fundamentals]] — Collections Framework e Streams
- [[Banco de dados]] — B-Trees em índices
- [[System Design]] — uso de estruturas em arquitetura
- [[Coding Challenges Strategy]] — patterns e reconhecimento
