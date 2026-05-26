---
title: "Coding Challenges Strategy"
created: 2026-04-01
updated: 2026-04-01
type: concept
status: seedling
tags:
  - entrevista
  - prática
publish: false
---

# Coding Challenges Strategy

Estratégia para coding interviews — não é sobre memorizar soluções, é sobre reconhecer padrões.

## Abordagem para coding interviews

### Framework de resolução (durante a entrevista)

**1. Entender o problema (2-3 min)**

- Repetir o problema com suas palavras
- Clarificar inputs, outputs, constraints
- Perguntar sobre edge cases: vazio? negativo? duplicatas? overflow?
- Confirmar: "So I need to return X given Y, correct?"

**2. Pensar em exemplos (2 min)**

- Trabalhar com exemplos concretos (small input)
- Identificar o padrão antes de codar

**3. Propor abordagem (3-5 min)**

- Começar com brute force: "The naive approach would be O(n²)..."
- Otimizar: "But we can do better using a hash map for O(n)..."
- Comunicar a complexidade de tempo E espaço

**4. Codar (15-20 min)**

- Narrar enquanto escreve
- Usar nomes de variáveis claros
- Modularizar: extrair funções helper

**5. Testar (5 min)**

- Dry-run com exemplo simples
- Testar edge cases: vazio, um elemento, todos iguais
- Verificar off-by-one errors

### Os 15 padrões mais comuns

| # | Padrão | Quando usar | Complexidade típica |
| --- | --- | --- | --- |
| 1 | Two Pointers | Array ordenado, pares | O(n) |
| 2 | Sliding Window | Subarray/substring contígua | O(n) |
| 3 | Fast & Slow Pointers | Ciclo em lista, meio da lista | O(n) |
| 4 | Merge Intervals | Intervalos sobrepostos | O(n log n) |
| 5 | Binary Search | Array ordenado, busca | O(log n) |
| 6 | BFS | Nível de árvore/grafo, caminho mais curto | O(V+E) |
| 7 | DFS | Exploração completa, backtracking | O(V+E) |
| 8 | HashMap/Set | Lookup O(1), contagem, dedup | O(n) |
| 9 | Stack | Parsing, matching, monotonic | O(n) |
| 10 | Heap/Priority Queue | Top-K, merge sorted | O(n log k) |
| 11 | Dynamic Programming | Otimização com subproblemas | Varia |
| 12 | Backtracking | Combinações, permutações | O(2ⁿ) ou O(n!) |
| 13 | Greedy | Escolha local ótima | O(n log n) |
| 14 | Trie | Prefixos, autocomplete | O(m) por operação |
| 15 | Union-Find | Componentes conectados | O(α(n)) |

### Plano de estudo progressivo

**Semana 1-2: Fundamentos**

- [ ] Two Pointers (5 problemas)
- [ ] Sliding Window (5 problemas)
- [ ] HashMap/Set (5 problemas)
- [ ] Binary Search (5 problemas)

**Semana 3-4: Árvores e Grafos**

- [ ] BFS (5 problemas)
- [ ] DFS (5 problemas)
- [ ] Heap/Priority Queue (5 problemas)
- [ ] Stack (5 problemas)

**Semana 5-6: Avançado**

- [ ] Dynamic Programming (10 problemas — Fibonacci, Knapsack, LCS, etc.)
- [ ] Backtracking (5 problemas)
- [ ] Greedy (5 problemas)
- [ ] Merge Intervals (3 problemas)

**Semana 7-8: Revisão e simulação**

- [ ] Revisar padrões fracos
- [ ] Mock interviews (timed, 45 min)
- [ ] Problemas mistos sem saber o padrão

## Dicas específicas por linguagem

### Java

```java
// HashMap para contagem
Map<Character, Integer> freq = new HashMap<>();
for (char c : s.toCharArray()) {
    freq.merge(c, 1, Integer::sum);
}

// PriorityQueue (min-heap)
PriorityQueue<Integer> pq = new PriorityQueue<>();

// Sort com comparator
Arrays.sort(intervals, Comparator.comparingInt(a -> a[0]));

// StringBuilder (não concatenar strings em loop)
StringBuilder sb = new StringBuilder();
```

### TypeScript/JavaScript

```typescript
// Map para contagem
const freq = new Map<string, number>();
for (const c of s) {
  freq.set(c, (freq.get(c) ?? 0) + 1);
}

// Sort (cuidado: default é lexicográfico!)
nums.sort((a, b) => a - b);

// Set para dedup
const unique = [...new Set(arr)];

// Two pointers
let left = 0, right = arr.length - 1;
while (left < right) { ... }
```

## Armadilhas comuns

- **Pular direto pro código:** sem entender o problema e propor abordagem. O processo vale mais que a solução.
- **Silêncio:** não falar enquanto pensa/coda. O entrevistador precisa ver seu raciocínio.
- **Otimizar prematuramente:** comece com brute force, depois otimize. Mostra progressão de pensamento.
- **Não testar:** após codar, sempre dry-run com um exemplo e checar edge cases.
- **Memorizar soluções:** entrevistadores mudam detalhes. Entender o padrão é mais valioso.

## Recursos

- [NeetCode Roadmap](https://neetcode.io/roadmap) — problemas organizados por padrão
- [LeetCode](https://leetcode.com/) — plataforma principal
- [Blind 75](https://leetcode.com/discuss/general-discussion/460599/blind-75-leetcode-questions) — lista curada de 75 problemas essenciais
- [Grind 75](https://www.techinterviewhandbook.org/grind75) — versão atualizada com scheduler

## Veja também

- [[Algoritmos]]
- [[Estruturas de Dados]]
