---
title: "Collections, Streams e Programação Funcional"
created: 2026-06-04
updated: 2026-06-04
type: moc
status: growing
publish: true
tags:
  - java
  - collections
  - moc
aliases:
  - Collections e Streams
  - Galho 2 - Collections, Streams e Programação Funcional
---

# Collections, Streams e Programação Funcional

> [!abstract] TL;DR
> Galho 2 da trilha Java Senior; cobre Collections Framework, Stream API, programação funcional (lambdas/composição), Optional, Date/Time (java.time) e I/O moderno (java.nio.file).

## Sobre este galho

Este galho cobre o **ecossistema de dados e processamento funcional** do Java: a hierarquia do Collections Framework com suas implementações e trade-offs, a Stream API com seu modelo lazy/eager, programação funcional com lambdas e interfaces funcionais, composição de funções de alta ordem, Optional como alternativa idiomática ao null, a API moderna de datas com `java.time`, e I/O de arquivos com `java.nio.file`. Não cobre concorrência, threads nem parallel streams — esses tópicos ficam no Galho 4.

Este galho é um **refator do tronco** `[[Java Fundamentals]]`: as seções de Collections e Streams foram extraídas do monolito original, aprofundadas e reorganizadas em notas atômicas por fase de aprendizado.

**Audiência primária:** dev senior em preparação para entrevista internacional. Cada nota expõe o "porquê" das escolhas de estrutura e as perguntas mais cobradas, com frases prontas em inglês. **Audiência secundária:** o mesmo dev em decisões de design do dia a dia — qual coleção escolher, quando usar stream vs loop, como modelar ausência com Optional.

## Iniciado

1. [[01 - O Collections Framework]] — hierarquia Iterable/Collection/List/Set/Queue/Map, imutáveis vs views.
2. [[02 - Listas, conjuntos e filas]] — ArrayList/LinkedList, HashSet/TreeSet, ArrayDeque/PriorityQueue, Big-O.
3. [[03 - Mapas]] — HashMap por dentro, contrato hashCode/equals, TreeMap, API rica.
4. [[04 - Lambdas e interfaces funcionais]] — SAM, Function/Predicate/Consumer/Supplier, method references.
5. [[05 - Introdução à Stream API]] — pipeline lazy/eager, stream vs collection, consumível uma vez.

## Adepto

6. [[06 - Comparable e Comparator]] — ordem natural vs externa, combinadores.
7. [[07 - Operações de Stream — intermediárias e terminais]] — map/filter/flatMap/reduce/find/match.
8. [[08 - Collectors e agrupamento]] — toMap/groupingBy/partitioningBy, downstream collectors.
9. [[09 - Streams primitivos]] — IntStream/LongStream, summary statistics, boxing.
10. [[10 - Optional]] — ausência no tipo, map/orElse, anti-patterns.
11. [[11 - java.time — Date e Time API]] — LocalDate/Instant, Duration/Period, imutabilidade.
12. [[12 - I-O moderno com java.nio.file]] — Path/Files, try-with-resources, streaming.

## Magus

13. [[13 - Composição funcional e funções de alta ordem]] — compose/andThen, HOFs, quando funcional ajuda.
14. [[14 - SequencedCollection e SequencedMap]] — Java 21, acesso uniforme às pontas, reversed.
15. [[15 - Collectors customizados e Gatherers]] — Collector.of, Stream Gatherers (Java 24).
16. [[16 - Escolha de coleção e estilo funcional — síntese]] — capstone: decision tree, stream vs loop.

## Rotas alternativas

### Completa

01 → 02 → 03 → 04 → 05 → 06 → 07 → 08 → 09 → 10 → 11 → 12 → 13 → 14 → 15 → 16. Percurso linear do básico ao avançado.

### Entrevista internacional

01 → 03 → 04 → 05 → 07 → 08 → 10 → 16. Collections fundamentais, lambdas, streams com collectors, Optional e síntese — o que mais cai.

### Domine Streams

05 → 07 → 08 → 09 → 15. Pipeline básico, operações, agrupamento, primitivos e collectors avançados.

### Escolha de estrutura de dados

01 → 02 → 03 → 06 → 16. Hierarquia, implementações principais, ordenação e decision tree final.

### Programação funcional

04 → 13 → 10 → 07. Lambdas, composição de funções, Optional e operações de stream.

## Todas as notas

```dataview
TABLE fase, status, updated
FROM "03-Dominios/Java/Collections e Streams"
WHERE type = "concept"
SORT file.name ASC
```

## Veja também

- [[03-Dominios/Java/index|Java (MOC central)]]
- [[03-Dominios/Java/Linguagem e sintaxe moderna/index|Linguagem e sintaxe moderna (Galho 1)]]
- [[03-Dominios/Java/Concorrência e paralelismo/index|Concorrência e paralelismo (Galho 4)]]
- [[03-Dominios/Java/Dicionário de Java|Dicionário de Java]]
- [[Java Fundamentals]] (tronco em transição)
- JVM por dentro (Galho 3) — planejado.
