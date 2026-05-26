---
title: "Algoritmos"
created: 2026-04-01
updated: 2026-04-09
type: concept
status: evergreen
tags:
  - fundamentos
  - entrevista
publish: false
---

# Algoritmos

Sequências de passos bem definidas para resolver problemas computacionais. Em entrevistas, o que separa um senior é menos "saber implementar quicksort de cor" e mais **reconhecer padrões**, **analisar trade-offs** e **comunicar raciocínio** enquanto resolve.

## O que é

Um algoritmo é uma solução passo-a-passo para um problema computacional. Tem três propriedades fundamentais:

1. **Correção** — produz o resultado certo para todas as entradas válidas, incluindo edge cases
2. **Complexidade** — quanto consome de tempo e espaço em função do tamanho da entrada
3. **Generalidade** — funciona para uma classe de problemas, não só para um caso

Em uma entrevista de algoritmos, você é avaliado em quatro dimensões: **resolução do problema**, **qualidade do código**, **comunicação** e **identificação de edge cases**. Um candidato que resolve perfeitamente sem falar perde para quem narra o raciocínio mesmo cometendo pequenos erros.

---

## Análise de complexidade (Big O)

Big O descreve o **comportamento assintótico** — como o tempo ou espaço crescem conforme a entrada cresce, ignorando constantes e termos menores. Não é "quanto tempo leva", é "como escala".

### Hierarquia de complexidades

| Complexidade | Nome | Exemplo | Para n=10⁶ |
| --- | --- | --- | --- |
| O(1) | Constante | Acesso a array, `HashMap.get()` | instantâneo |
| O(log n) | Logarítmica | Binary search, BST balanceada | ~20 ops |
| O(n) | Linear | Percorrer array, busca linear | 10⁶ ops |
| O(n log n) | Linearítmica | Merge sort, TimSort, heap sort | ~2×10⁷ ops |
| O(n²) | Quadrática | Bubble sort, dois loops aninhados | 10¹² ops (lento) |
| O(n³) | Cúbica | Floyd-Warshall, matriz multiplicação ingênua | 10¹⁸ ops (inviável) |
| O(2ⁿ) | Exponencial | Subsets, recursão Fibonacci sem memo | inviável > n=30 |
| O(n!) | Fatorial | Permutações, brute force TSP | inviável > n=12 |

### Regras práticas

1. **Ignore constantes:** O(2n + 100) = O(n)
2. **Domine o termo maior:** O(n² + n log n + n) = O(n²)
3. **Loops aninhados independentes multiplicam:** dois loops de n × m = O(n × m)
4. **Loops sequenciais somam:** O(n) + O(m) = O(n + m), simplifica para O(max(n, m))
5. **Recursão = profundidade × trabalho por nível:** Fibonacci ingênuo é O(2ⁿ) porque árvore tem 2ⁿ nós
6. **Caso médio vs pior caso:** quicksort é O(n log n) médio, O(n²) pior caso. Mencione ambos.
7. **Espaço importa tanto quanto tempo:** memoization gasta O(n) de espaço para ganhar tempo

### Best, average, worst case

- **Best case (Ω):** entrada mais favorável. Pouco usado em discussões — quase sempre irrelevante.
- **Average case (Θ):** entrada típica. É o mais útil para sistemas reais.
- **Worst case (O):** pior entrada possível. Crítico para sistemas com SLA ou tempo real.

> Exemplo: HashMap é O(1) médio, mas O(n) pior caso (todas as chaves colidem). Por isso bancos não usam HashMap em índices — usam B-Tree, que garante O(log n) **sempre**.

### Análise amortizada

Quando uma operação **ocasionalmente** é cara, mas o **custo médio** ao longo de muitas operações é baixo. Exemplo clássico: `ArrayList.add()` é O(1) amortizado — a maioria dos `add` é instantânea, mas quando o array interno enche, ele dobra de tamanho (O(n)). Distribuído ao longo de n inserções, dá O(1) por operação.

---

## Sorting

Raramente você implementa um sort do zero em produção, mas em entrevistas é fundamental conhecer as características de cada um.

### Comparativo

| Algoritmo | Tempo médio | Tempo pior | Espaço | Estável | In-place | Notas |
| --- | --- | --- | --- | --- | --- | --- |
| Bubble Sort | O(n²) | O(n²) | O(1) | sim | sim | didático apenas |
| Insertion Sort | O(n²) | O(n²) | O(1) | sim | sim | rápido para n pequeno |
| Selection Sort | O(n²) | O(n²) | O(1) | não | sim | sempre n² |
| Merge Sort | O(n log n) | O(n log n) | O(n) | sim | não | divide & conquer |
| Quick Sort | O(n log n) | O(n²) | O(log n) | não | sim | rápido na prática |
| Heap Sort | O(n log n) | O(n log n) | O(1) | não | sim | sem pior caso ruim |
| TimSort | O(n log n) | O(n log n) | O(n) | sim | não | usado em Java/Python |
| Counting Sort | O(n + k) | O(n + k) | O(k) | sim | não | inteiros em range limitado |
| Radix Sort | O(d·n) | O(d·n) | O(n + k) | sim | não | inteiros, strings |

**Estável** = elementos com chave igual mantêm a ordem relativa. Importante para sorts encadeados (sort por nome, depois por idade, sem perder ordem por nome).

### Na prática (linguagens reais)

```java
// Java: TimSort para objetos, Dual-Pivot Quicksort para primitivos
int[] nums = {3, 1, 4, 1, 5};
Arrays.sort(nums); // O(n log n)

List<String> nomes = new ArrayList<>(List.of("Carla", "Ana", "Bruno"));
Collections.sort(nomes);                              // ordem natural
nomes.sort(Comparator.reverseOrder());                // descendente
nomes.sort(Comparator.comparing(String::length));     // por tamanho
nomes.sort(Comparator.comparing(String::length)
                     .thenComparing(Comparator.naturalOrder())); // tiebreaker
```

```typescript
// JS/TS: TimSort na V8 (estável desde ES2019)
const nums = [3, 1, 4, 1, 5];
nums.sort((a, b) => a - b); // CUIDADO: sem comparator, ordena lexicograficamente!

const pessoas = [{ idade: 30 }, { idade: 25 }];
pessoas.sort((a, b) => a.idade - b.idade);
```

> **Pegadinha JS:** `[10, 2, 1].sort()` retorna `[1, 10, 2]` — sem comparator, converte para string. Sempre passe `(a, b) => a - b`.

### Quando pensar em sorting

- Output precisa estar ordenado
- Pré-processamento para binary search
- Detecção de duplicatas (vizinhos iguais após sort) — alternativa ao HashSet
- Two pointers funciona melhor em arrays ordenados
- Ordenar por critério customizado é trabalho de comparator, não de algoritmo

---

## Searching

### Linear search

O(n). Não interessante isoladamente, mas é o baseline.

### Binary search

O(log n) em **dados ordenados**. Template fundamental — saiba escrever sem hesitar:

```java
int binarySearch(int[] arr, int target) {
    int left = 0, right = arr.length - 1;
    while (left <= right) {
        int mid = left + (right - left) / 2; // evita overflow
        if (arr[mid] == target) return mid;
        if (arr[mid] < target) left = mid + 1;
        else right = mid - 1;
    }
    return -1;
}
```

**Variações importantes:**

- **Lower bound** — primeira posição onde `arr[i] >= target` (insertion point)
- **Upper bound** — primeira posição onde `arr[i] > target`
- **Binary search no espaço de respostas** — quando o array é "implícito": "qual o menor X que satisfaz uma propriedade monotônica?"

> **Sinal de "use binary search":** o problema fala em ordenado, ou você consegue formular como "encontre o menor/maior X tal que P(X) é verdadeiro" onde P é monotônica.

### Two Pointers

Dois ponteiros percorrem o array (geralmente ordenado), aproximando-se ou movendo-se juntos. Resolve problemas O(n²) ingênuos em O(n).

```java
// Soma de dois números em array ordenado
int[] twoSum(int[] arr, int target) {
    int left = 0, right = arr.length - 1;
    while (left < right) {
        int sum = arr[left] + arr[right];
        if (sum == target) return new int[]{left, right};
        if (sum < target) left++;
        else right--;
    }
    return new int[]{-1, -1};
}
```

**Variações:**

- Slow/fast pointer — detecção de ciclo em linked list (Floyd's tortoise and hare)
- Remoção in-place de duplicatas
- Palíndromos
- Container with most water

### Sliding Window

Janela contígua que desliza sobre array/string. O(n) em vez de O(n × k).

```java
// Maior soma de subarray contíguo de tamanho k
int maxSum(int[] arr, int k) {
    int sum = 0;
    for (int i = 0; i < k; i++) sum += arr[i];
    int max = sum;
    for (int i = k; i < arr.length; i++) {
        sum += arr[i] - arr[i - k];   // adiciona o novo, remove o que saiu
        max = Math.max(max, sum);
    }
    return max;
}
```

**Variações:**

- Janela de tamanho fixo (acima)
- Janela de tamanho variável — "menor substring que contém X"
- Combinada com HashMap/HashSet para "substring sem caracteres repetidos"

---

## Recursão

Função que se chama a si mesma. Toda recursão precisa de:

1. **Base case** — condição de parada que não recorre
2. **Recursive case** — chamada que se aproxima do base case
3. **Garantia de progresso** — cada chamada reduz o problema

```java
int factorial(int n) {
    if (n <= 1) return 1;          // base case
    return n * factorial(n - 1);   // recursive case
}
```

### Recursão vs iteração

- **Recursão** é mais natural para árvores, grafos, divide & conquer, backtracking
- **Iteração** evita stack overflow e é geralmente mais rápida (sem overhead de chamadas)
- **Tail recursion** — quando a chamada recursiva é a última operação. Java **não** otimiza tail calls; Scala e algumas JVMs sim. Em Java, prefira converter para loop quando profundidade é alta.

### Stack overflow

Cada chamada empilha um stack frame. Profundidade típica antes de estourar: ~10⁴ a 10⁵. Para problemas com profundidade maior (DFS em grafo enorme), converta para iterativo com pilha explícita.

---

## Divide and Conquer

Estratégia: dividir o problema em subproblemas independentes do mesmo tipo, resolver recursivamente, combinar resultados.

**Exemplos canônicos:**

- **Merge sort** — divide o array em duas metades, ordena cada uma, faz merge
- **Quick sort** — escolhe pivô, particiona, recursão em cada lado
- **Binary search** — descarta metade a cada passo
- **Closest pair of points** — divide o plano em metades

**Master theorem** (regra para recorrências do tipo T(n) = a·T(n/b) + f(n)):

- Merge sort: T(n) = 2·T(n/2) + O(n) → O(n log n)
- Binary search: T(n) = T(n/2) + O(1) → O(log n)

---

## Dynamic Programming (DP)

DP é recursão com memória. Aplica-se quando o problema tem:

1. **Subestrutura ótima** — solução ótima do problema contém soluções ótimas de subproblemas
2. **Subproblemas sobrepostos** — os mesmos subproblemas são resolvidos múltiplas vezes

Sem memoization, Fibonacci recursivo é O(2ⁿ). Com memoization, vira O(n).

### Top-down (memoization)

Recursão natural + cache. Mais intuitivo, parte do problema original.

```java
Map<Integer, Long> memo = new HashMap<>();
long fib(int n) {
    if (n < 2) return n;
    if (memo.containsKey(n)) return memo.get(n);
    long result = fib(n - 1) + fib(n - 2);
    memo.put(n, result);
    return result;
}
```

### Bottom-up (tabulation)

Preenche tabela iterativamente, do menor subproblema ao maior. Sem overhead de recursão, geralmente mais eficiente.

```java
long fib(int n) {
    if (n < 2) return n;
    long[] dp = new long[n + 1];
    dp[0] = 0; dp[1] = 1;
    for (int i = 2; i <= n; i++) {
        dp[i] = dp[i - 1] + dp[i - 2];
    }
    return dp[n];
}

// Otimização de espaço: só os dois últimos importam
long fib(int n) {
    if (n < 2) return n;
    long prev = 0, curr = 1;
    for (int i = 2; i <= n; i++) {
        long next = prev + curr;
        prev = curr;
        curr = next;
    }
    return curr;
}
```

### Como abordar um problema de DP

1. **Defina o estado:** o que `dp[i]` (ou `dp[i][j]`) representa? Seja preciso.
2. **Defina a transição:** como `dp[i]` se calcula a partir de estados anteriores?
3. **Defina o caso base:** valores iniciais
4. **Defina a resposta final:** qual célula da tabela é a resposta?
5. **Otimize espaço se possível:** muitas vezes só precisa de O(1) ou O(n) em vez de O(n²)

### Problemas clássicos de DP

- **Fibonacci** — introdução à DP
- **Climbing stairs** — variação de Fibonacci
- **Coin change** — número mínimo de moedas para um valor
- **Knapsack 0/1** — maximizar valor sob restrição de peso
- **Longest Common Subsequence (LCS)** — clássico de DP 2D
- **Longest Increasing Subsequence (LIS)** — O(n²) ou O(n log n)
- **Edit distance (Levenshtein)** — usado em correção ortográfica
- **Matrix chain multiplication** — minimizar operações

> **Sinal de "use DP":** problema pede otimização (máximo, mínimo, contagem) E você consegue identificar subproblemas que se repetem. Se precisa retornar **uma** solução qualquer, recursão pode bastar; se pede a **melhor**, DP.

---

## Greedy

Estratégia: a cada passo, fazer a escolha **localmente ótima**, esperando que isso leve à solução globalmente ótima.

**Quando funciona:** quando o problema tem a propriedade da escolha gulosa — provar isso é difícil, e errar significa solução errada.

**Exemplos onde greedy funciona:**

- **Interval scheduling** — selecionar máximo de intervalos não sobrepostos (escolha sempre o que termina antes)
- **Huffman coding** — compressão
- **Dijkstra** — sempre expande o vértice mais próximo
- **Kruskal/Prim** — minimum spanning tree
- **Coin change com sistema canônico** (R$1, R$0,50, R$0,25, R$0,10...) — guloso funciona
- **Coin change com sistema arbitrário** (1, 3, 4 e alvo 6) — guloso **falha** (escolhe 4+1+1 quando 3+3 é melhor)

> **Cuidado em entrevistas:** se você "sente" que greedy funciona, prove com argumento de troca (exchange argument) ou prepare-se para mostrar contra-exemplo se não funciona. DP é o fallback seguro.

---

## Backtracking

Recursão que **explora todas as possibilidades** e desfaz escolhas que não levam a uma solução. Tipicamente O(exponencial), mas com poda eficiente é viável para n moderado.

Estrutura geral:

```java
void backtrack(State state, List<Solution> solutions) {
    if (isGoal(state)) {
        solutions.add(state.copy());
        return;
    }
    for (Choice choice : possibleChoices(state)) {
        if (!isValid(state, choice)) continue;  // poda
        state.apply(choice);
        backtrack(state, solutions);
        state.undo(choice);                      // backtrack
    }
}
```

**Problemas clássicos:**

- N-queens
- Sudoku solver
- Permutações e combinações
- Subset sum
- Word search em matriz
- Generate parentheses

---

## Algoritmos em Grafos

### BFS — Breadth-First Search

Explora em camadas, do mais próximo ao mais distante. Usa **fila**. Encontra caminho mais curto em grafos **não-ponderados**.

```java
void bfs(Map<Integer, List<Integer>> grafo, int origem) {
    Set<Integer> visitado = new HashSet<>();
    Queue<Integer> fila = new ArrayDeque<>();
    fila.offer(origem);
    visitado.add(origem);
    while (!fila.isEmpty()) {
        int v = fila.poll();
        for (int vizinho : grafo.getOrDefault(v, List.of())) {
            if (visitado.add(vizinho)) {
                fila.offer(vizinho);
            }
        }
    }
}
```

### DFS — Depth-First Search

Mergulha o mais fundo possível antes de voltar. Usa **pilha** (ou recursão). Detecção de ciclos, topological sort, componentes conexos.

```java
void dfs(int v, Map<Integer, List<Integer>> grafo, Set<Integer> visitado) {
    if (!visitado.add(v)) return;
    for (int vizinho : grafo.getOrDefault(v, List.of())) {
        dfs(vizinho, grafo, visitado);
    }
}
```

### Dijkstra

Caminho mais curto em grafo ponderado **com pesos não-negativos**. Usa priority queue. O((V + E) log V).

Ideia: a cada passo, expanda o vértice ainda não visitado de menor distância acumulada. Atualize as distâncias dos vizinhos.

### Bellman-Ford

Como Dijkstra, mas aceita pesos negativos. Detecta ciclos negativos. O(V·E) — mais lento que Dijkstra.

### Topological Sort

Ordenação linear de vértices em DAG respeitando dependências. Duas abordagens:

1. **Kahn's algorithm** (BFS) — repetidamente remove vértices sem dependências
2. **DFS com post-order** — empilha após visitar todos os descendentes

**Uso real:** build systems (Gradle, Maven), task schedulers, currículo de cursos com pré-requisitos, dependency injection.

### A* (A-star)

Dijkstra + heurística que estima distância até o destino. Usado em pathfinding de jogos e navegação GPS.

### Floyd-Warshall

Caminho mais curto entre **todos os pares** de vértices. O(V³). Vale quando o grafo é pequeno e você precisa de todas as distâncias.

---

## Patterns: como reconhecer o algoritmo certo

| Sinal no enunciado | Abordagem |
| --- | --- |
| "ordenado" | binary search, two pointers |
| "todas as combinações / permutações" | backtracking |
| "subarray contíguo" | sliding window, prefix sum |
| "soma / par / triplet com soma X" | hash map, two pointers |
| "k-ésimo maior/menor" | heap, quickselect |
| "shortest path" não-ponderado | BFS |
| "shortest path" com pesos | Dijkstra |
| "ordem de execução com dependências" | topological sort |
| "número de caminhos / formas" | DP (contagem) |
| "máximo/mínimo de algo com restrições" | DP ou greedy |
| "intervalos sobrepostos" | sort + sweep line |
| "string matching / busca de padrão" | KMP, Rabin-Karp, sliding window |
| "encontrar ciclo" | Floyd's tortoise and hare, DFS, Union-Find |
| "componentes conexos" | DFS/BFS ou Union-Find |
| "mediana em stream" | dois heaps |
| "soma de range em array (com updates)" | prefix sum, segment tree, Fenwick tree |
| "matriz / grid 2D" | DFS/BFS ou DP 2D |

---

## Framework para resolver em entrevista

Quase tudo se reduz a este protocolo de 6 passos. Pratique-o.

1. **Clarify** — confirme inputs, outputs, range, edge cases. Faça perguntas: "podem ser negativos?", "quantos elementos no máximo?", "há duplicatas?", "se vazio, retorno o quê?".
2. **Explore com exemplos** — escreva 1-2 exemplos pequenos manualmente. Inclua um edge case.
3. **Brute force primeiro** — declare a solução ingênua e sua complexidade. Mostra que você entendeu o problema.
4. **Otimize** — identifique o gargalo (geralmente trabalho repetido) e proponha uma estrutura/técnica para eliminá-lo. Compare complexidades.
5. **Code** — escreva código limpo, nomeie bem variáveis, narre o que está fazendo.
6. **Test** — passe pelo código com o exemplo, depois com edge cases. Identifique bugs antes do entrevistador.

### Edge cases que esquecem com frequência

- Array/string vazio
- Um único elemento
- Todos os elementos iguais
- Já ordenado / em ordem reversa
- Negativos, zeros
- Overflow (use `long` ou `BigInteger` em Java)
- Caracteres não-ASCII em strings
- Grafo desconectado
- Ciclos
- Recursão profunda (stack overflow)

---

## Armadilhas comuns

- **Otimizar antes de resolver:** brute force primeiro, sempre. Optimização prematura = código errado e lento de produzir.
- **Esquecer edge cases:** array vazio, um elemento, todos iguais, overflow, negativos, ciclos.
- **Não comunicar:** entrevistador não vê dentro da sua cabeça. Narre.
- **Confundir BFS com DFS:** BFS = fila = caminho mais curto não-ponderado; DFS = pilha = exploração completa.
- **DP sem definir o estado:** "uso DP" não é um plano. `dp[i] = ?` é um plano.
- **Greedy sem prova:** se não consegue argumentar por que funciona, use DP.
- **Off-by-one em binary search:** `<= right` vs `< right`, `mid + 1` vs `mid`. Tenha um template confiável.
- **`mid = (left + right) / 2` overflow:** use `mid = left + (right - left) / 2`.
- **Modificar coleção enquanto itera:** `ConcurrentModificationException` em Java. Use `Iterator.remove()` ou copie.
- **Recursão profunda em Java:** sem TCO, profundidade > ~10⁴ estoura. Converta para iterativo.
- **Não considerar complexidade de espaço:** "minha solução é O(n)... mas usa O(n²) de memória." Mencione ambos.

---

## Na prática (da minha experiência)

> No dia a dia de backend Java/Spring, raramente implemento algoritmos clássicos do zero — Collections, Streams e o banco fazem o trabalho pesado. Mas **entender complexidade** muda decisões arquiteturais o tempo todo.
>
> No MedEspecialista, um endpoint de busca de profissionais começou com um JOIN ingênuo que rodava em ~3s para alguns filtros. A solução não foi "otimizar o algoritmo" — foi mover a contagem de avaliações para uma coluna desnormalizada e adicionar índice composto, transformando uma query O(n × m) em O(log n). O conhecimento de Big O guiou a decisão de modelagem.
>
> Em outro caso (Digidados), processamos lotes de leituras de sensores. A primeira versão usava `list.contains()` dentro de um loop — O(n²) que travava com 10k registros. Trocando por `HashSet.contains()`, virou O(n) e o processamento caiu de minutos para segundos. **A diferença não estava em "saber binary search" — estava em reconhecer o pattern.**
>
> Em coding interviews, o que mais me ajudou foi praticar os patterns (NeetCode 150) até reconhecer rápido o tipo de problema. Decorar soluções não funciona; reconhecer padrões funciona.

---

## How to explain in English

> "When I approach an algorithm problem in an interview, my first goal isn't to write code — it's to make sure I understand the problem. I clarify inputs, outputs, constraints, and edge cases. Then I work through a small example by hand to confirm I understand the expected behavior.
>
> Next, I state the brute force solution and its complexity, even if I already see a better approach. This shows the interviewer I understand the baseline. Then I look for the bottleneck — usually repeated work — and identify a data structure or technique that eliminates it. For two-sum, that means going from O(n²) nested loops to O(n) with a hash map storing complements.
>
> While I code, I narrate. I explain what each variable represents and why I'm structuring the loop a certain way. After the code is written, I trace through it with the example I built, and then with edge cases — empty input, single element, duplicates, overflow.
>
> In my day-to-day work, I rarely implement sorting or graph algorithms from scratch — the standard library handles that. But knowing complexity is what lets me make good architectural decisions: when to add a database index, when to denormalize, when a hash-based cache will save a database round-trip. The algorithms knowledge isn't decoration; it's the vocabulary I use to reason about performance."

### Frases úteis em entrevista

- "Let me start with the brute force and then optimize."
- "The bottleneck here is the nested loop — let's see if we can eliminate it."
- "I'll trade some space for time by using a hash map."
- "Let me trace through this with a small example to make sure it's correct."
- "What's the constraint on the input size? That'll affect which approach makes sense."
- "There's an edge case I want to handle — what if the array is empty?"
- "I'm going to use binary search because the array is sorted, so we can do this in O(log n) instead of O(n)."

### Key vocabulary

- complexidade de tempo / espaço → time / space complexity
- caso médio / pior caso → average case / worst case
- amortizado → amortized
- assintótico → asymptotic
- força bruta → brute force
- busca binária → binary search
- ponteiros duplos → two pointers
- janela deslizante → sliding window
- programação dinâmica → dynamic programming (DP)
- memoização → memoization
- tabulação → tabulation
- subestrutura ótima → optimal substructure
- subproblemas sobrepostos → overlapping subproblems
- algoritmo guloso → greedy algorithm
- backtracking → backtracking
- recursão → recursion
- caso base → base case
- divisão e conquista → divide and conquer
- ordenação → sorting
- estável → stable (sort)
- in-place → in-place
- caminho mais curto → shortest path
- ordenação topológica → topological sort
- componentes conexos → connected components
- ciclo → cycle
- grafo direcionado acíclico → DAG (directed acyclic graph)
- transbordamento → overflow

---

## Recursos

### Cursos

- [Algorithms, Part I](https://www.coursera.org/learn/algorithms-part1) — Princeton (Sedgewick)
- [Algorithms, Part II](https://www.coursera.org/learn/algorithms-part2) — Princeton (Sedgewick)
- [MIT 6.006 — Introduction to Algorithms](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/) — OCW

### Livros

- *Algorithms, 4th Edition* — Sedgewick & Wayne
- *Introduction to Algorithms (CLRS)* — Cormen, Leiserson, Rivest, Stein — referência canônica
- *Cracking the Coding Interview* — Gayle Laakmann McDowell — foco em entrevistas
- *Elements of Programming Interviews* — Aziz, Lee, Prakash — coleção excelente de problemas

### Prática

- [NeetCode 150](https://neetcode.io/) — roadmap por pattern, recomendado para preparação focada
- [LeetCode](https://leetcode.com/) — biblioteca enorme de problemas
- [Codeforces](https://codeforces.com/) — competitive programming (mais difícil, opcional)

## Veja também

- [[Estruturas de Dados]]
- [[Coding Challenges Strategy]]
- [[System Design]]
- [[Banco de dados]] — índices e sua relação com complexidade de query
