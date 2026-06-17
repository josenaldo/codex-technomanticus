---
title: "Algoritmos"
created: 2026-06-17
updated: 2026-06-17
type: moc
status: growing
publish: true
tags:
  - fundamentos
  - algoritmos
  - entrevista
  - moc
aliases:
  - Algoritmos
  - algoritmos
  - Galho - Algoritmos
  - Algorithms
---

# Algoritmos

> [!abstract] TL;DR
> Galho de Fundamentos sobre as sequências de passos que resolvem problemas computacionais — e,
> sobretudo, como **raciocinar** sobre elas: análise de complexidade, recorrências, e as grandes
> famílias de técnicas (ordenação, busca, dois ponteiros, divisão e conquista, programação dinâmica,
> greedy, backtracking). Interview-critical. O que separa um senior não é decorar quicksort, é
> **reconhecer padrões**, **analisar trade-offs** e **comunicar raciocínio**.

## Sobre este galho

Este galho é o **dono canônico da teoria de complexidade** no vault: Big-O, notação Θ/Ω,
análise de melhor/médio/pior caso, custo amortizado, recorrências e o Teorema Mestre. O galho
[[03-Dominios/Fundamentos/Estruturas de Dados/index|Estruturas de Dados]] delega para cá toda a
fundamentação de complexidade e apenas a aplica pontualmente por estrutura.

Sobre essa base assentam as grandes famílias de algoritmos clássicos — ordenação, busca, dois
ponteiros e janela deslizante, divisão e conquista, programação dinâmica, greedy e backtracking —
e fecha com a leitura de **intratabilidade** (quando não há algoritmo eficiente) e um capstone de
reconhecimento de padrões para entrevista.

**Audiência:** dev senior em preparação para entrevista internacional. Cada nota tem seção
"Em entrevista" com frases prontas em inglês e vocabulário técnico.

**Fronteiras:** os algoritmos de **grafo** (BFS, DFS, Dijkstra, Bellman-Ford, topological sort,
A*, Floyd-Warshall) vivem em [[11 - Grafos - travessia e algoritmos]], no galho de Estruturas de
Dados — aqui apenas linkamos. A teoria formal de **classes P/NP** (redução, NP-completude) pertence
ao galho *Teoria da Computação*; aqui fica só a face prática da intratabilidade (nota 13).

## Iniciado — análise e fundamentos

1. [[01 - O que é um algoritmo]] — correção, terminação, generalidade; as dimensões avaliadas em entrevista.
2. [[02 - Análise de complexidade - Big-O]] — comportamento assintótico, hierarquia, notação O/Θ/Ω, melhor/médio/pior caso.
3. [[03 - Análise amortizada]] — custo amortizado; métodos agregado, contábil e potencial; o array dinâmico.
4. [[04 - Recursão]] — base/recursive case, call stack, recursão vs. iteração, tail call, stack overflow.

## Adepto — algoritmos clássicos

5. [[05 - Recorrências e o Teorema Mestre]] — T(n)=a·T(n/b)+f(n), os três casos, árvore de recursão.
6. [[06 - Divisão e conquista]] — merge sort, quicksort, closest pair, Karatsuba.
7. [[07 - Ordenação]] — comparativo, estabilidade, in-place, limite Ω(n log n); o sort de cada linguagem.
8. [[08 - Busca]] — busca linear, binária e variações, busca no espaço de respostas, quickselect.
9. [[09 - Two pointers e sliding window]] — ponteiros convergentes, janela fixa/variável, fast/slow.
10. [[10 - Programação dinâmica]] — subestrutura ótima, memoização vs. tabulação, problemas clássicos.
11. [[11 - Greedy]] — escolha localmente ótima, exchange argument, quando funciona e quando falha.
12. [[12 - Backtracking]] — explorar e desfazer, poda, N-queens, permutações, subsets.

## Magus — síntese e limites

13. [[13 - Intratabilidade]] — tratável vs. intratável, NP-difícil como sinal prático, aproximação e heurística.
14. [[14 - Reconhecendo o algoritmo certo]] — tabela de padrões, framework de entrevista, armadilhas, prep bilíngue.

## Rotas alternativas

### Entrevista internacional
01 → 02 → 07 → 08 → 09 → 10 → 14. Complexidade, os dois sorts/buscas que sempre caem, os padrões mais cobrados e o capstone.

### Fundamentos de análise
02 → 03 → 05. Big-O, amortização e recorrências — o ferramental para medir qualquer algoritmo.

### Famílias de técnicas
04 → 06 → 10 → 11 → 12. Recursão como base, divisão e conquista, DP, greedy e backtracking.

## Todas as notas

```dataview
TABLE fase, status, updated
FROM "03-Dominios/Fundamentos/Algoritmos"
WHERE type = "concept"
SORT file.name ASC
```

## Veja também

- [[03-Dominios/Fundamentos/index|Fundamentos (MOC do domínio)]]
- [[03-Dominios/Fundamentos/Estruturas de Dados/index|Estruturas de Dados]] — as estruturas sobre as quais os algoritmos operam
- [[Banco de dados]] — índices e a complexidade das queries
- [[Dicionário de Fundamentos]]
