---
title: "Python — Collections e Comprehensions"
created: 2026-07-09
type: moc
status: growing
publish: true
tags:
  - python
  - moc
aliases:
  - "Galho 2 - Collections e Comprehensions"
---

# Collections e Comprehensions

> [!abstract] TL;DR
> Galho 2 da trilha Python: as estruturas de dados nativas (listas, tuplas, dicionários, sets), a sintaxe de comprehension, o módulo `itertools` e o módulo `collections` (Counter/defaultdict/deque/namedtuple). Fases Iniciado→Adepto; 8 notas. Assume o [[03-Dominios/Tecnologia/Python/Core/index|Galho 1 (Core)]] como pré-requisito.

## Sobre este galho

Depois de dominar sintaxe e controle de fluxo, este galho cobre o que move dados de verdade em Python: as 4 collections nativas e suas armadilhas específicas, a sintaxe de comprehension que substitui boa parte dos loops explícitos, os módulos padrão `itertools` (iteração combinatória/lazy) e `collections` (estruturas especializadas). Fecha com um capstone comparativo de complexidade — a pergunta "por que essa estrutura e não outra" que separa código correto de código eficiente.

**Audiência:** mesma do Galho 1 — quem está aprendendo Python do zero ou vindo de outra linguagem. Comparações com List/Map/Set do Java e Array/Object/Map/Set do JS aparecem quando esclarecem.

Iteradores/geradores de verdade (o "como" por trás de comprehensions e generator expressions) são o [[03-Dominios/Tecnologia/Python/Funcional e idiomas avançados/index|Galho 4]] — aqui é o uso prático.

## Iniciado

1. [[01 - Listas — criação, métodos e slicing avançado|01 — Listas: criação, métodos e slicing avançado]]
2. [[02 - Tuplas e desempacotamento|02 — Tuplas e desempacotamento]]
3. [[03 - Dicionários|03 — Dicionários]]
4. [[04 - Sets|04 — Sets]]

## Adepto

5. [[05 - Comprehensions — list, dict, set e generator expressions|05 — Comprehensions (list, dict, set, generator)]]
6. [[06 - itertools — os essenciais|06 — itertools: os essenciais]]
7. [[07 - O módulo collections — Counter, defaultdict, deque, namedtuple|07 — O módulo collections]]
8. [[08 - Escolhendo a estrutura certa|08 — Escolhendo a estrutura certa]] — capstone do galho.

## Todas as notas

```dataview
TABLE fase, status FROM "03-Dominios/Tecnologia/Python/Collections e Comprehensions" WHERE type = "concept" SORT file.name ASC
```

## Veja também

- [[03-Dominios/Tecnologia/Python/index|Trilha Python]] (MOC central)
- [[03-Dominios/Tecnologia/Python/Core/index|Core]] — Galho 1 (pré-requisito)
- [[03-Dominios/Tecnologia/Python/OO e Data Model/index|OO e Data Model]] — Galho 3 (próximo)
- [[03-Dominios/Tecnologia/Python/Funcional e idiomas avançados/index|Funcional e idiomas avançados]] — Galho 4 (iteradores/geradores de verdade)
