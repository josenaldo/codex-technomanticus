---
title: "Estruturas de Dados"
created: 2026-06-17
updated: 2026-06-17
type: moc
status: seedling
publish: true
tags:
  - fundamentos
  - estruturas-de-dados
  - entrevista
  - moc
aliases:
  - Estruturas de Dados
  - Estruturas de dados
  - Galho - Estruturas de Dados
  - Data Structures
---

# Estruturas de Dados

> [!abstract] TL;DR
> Galho de Fundamentos sobre as formas de organizar e armazenar dados — e os trade-offs de
> tempo, espaço e ordem que cada uma impõe. Interview-critical. Cada estrutura traz uma
> comparação profunda de implementação em **Java, TypeScript, Python e Go**, mostrando como
> as particularidades de cada linguagem moldam a estrutura.

## Sobre este galho

Cobre as estruturas de dados de ponta a ponta: dos blocos fundamentais (arrays, listas, pilhas,
filas, tabelas hash) às hierárquicas e relacionais (árvores, heaps, tries, árvores B, grafos) e às
especializadas (LRU, Bloom filter, skip list, union-find). O eixo é sempre **trade-off**: qual
estrutura para qual padrão de acesso, e por quê.

Cada nota traz uma seção **"Implementações comparadas: Java · TypeScript · Python · Go"** — não só
o código, mas *como cada stack pensa* a estrutura e como as particularidades da linguagem (a JVM e o
Collections Framework; a V8 e o array-como-objeto; o CPython e o `dict` compacto; os slices e a
semântica de valor do Go) influenciam a implementação e o desempenho.

**Audiência:** dev senior em preparação para entrevista internacional. Cada nota tem seção
"Em entrevista" com frases prontas em inglês e vocabulário técnico.

**Não cobre:** a teoria de análise de complexidade (Big-O, recorrências, classes de complexidade) —
isso vive no galho **Algoritmos**. Aqui a complexidade aparece pontualmente, por estrutura.

## Iniciado — estruturas fundamentais

1. [[01 - O que é uma estrutura de dados]] — contrato de operações, dimensões (tempo/espaço/ordem), framework de decisão.
2. [[02 - Arrays e listas dinâmicas]] — array, array dinâmico, localidade de cache, custo amortizado.
3. [[03 - Listas encadeadas]] — singly/doubly, o trade-off contra o array.
4. [[04 - Pilhas, filas e deques]] — LIFO/FIFO, deque.
5. [[05 - Tabelas hash]] — hashing, colisões, load factor, o contrato hashCode/equals.

## Adepto — hierárquicas e relacionais

6. [[06 - Árvores e árvores de busca]] — BST, balanceadas (AVL/Red-Black), TreeMap.
7. [[07 - Heaps e filas de prioridade]] — heap binário, top-K.
8. [[08 - Tries]] — busca por prefixo, autocomplete.
9. [[09 - Árvores B e índices]] — B-Tree/B+Tree e os índices de banco.
10. [[10 - Grafos - representação e tipos]] — adjacência (lista/matriz), direcionado/ponderado/DAG.
11. [[11 - Grafos - travessia e algoritmos]] — BFS, DFS, Dijkstra, topological sort, union-find.

## Magus — especializadas e aplicação

12. [[12 - Estruturas especializadas]] — LRU cache, Bloom filter, skip list, disjoint set.
13. [[13 - Escolhendo a estrutura certa]] — tabela comparativa, patterns de entrevista, armadilhas, prep bilíngue.

## Rotas alternativas

### Entrevista internacional
01 → 02 → 05 → 07 → 10 → 11 → 13. Trade-offs, hash, heap (top-K), grafos e o capstone de decisão.

### Comparação entre linguagens
01 → 02 → 05 → 06 → 10. As estruturas com maior divergência de implementação entre Java/TS/Python/Go.

### Base para banco de dados
05 → 06 → 09. Hash, árvores de busca e B-Trees — o que sustenta os índices.

## Todas as notas

```dataview
TABLE fase, status, updated
FROM "03-Dominios/Fundamentos/Estruturas de Dados"
WHERE type = "concept"
SORT file.name ASC
```

## Veja também

- [[03-Dominios/Fundamentos/index|Fundamentos (MOC do domínio)]]
- [[Algoritmos]] — a análise de complexidade e os algoritmos que operam sobre estas estruturas
- [[Banco de dados]] — B-Trees nos índices
- [[Dicionário de Fundamentos]]
