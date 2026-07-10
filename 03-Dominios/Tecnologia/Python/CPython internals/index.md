---
title: "Python — CPython internals"
created: 2026-07-10
type: moc
status: growing
publish: true
tags:
  - python
  - moc
aliases:
  - "Galho 6 - CPython internals"
---

# CPython internals

> [!abstract] TL;DR
> Galho 6 da trilha Python: o "como por dentro" do interpretador de referência (CPython) — o loop de execução, `PyObject`/refcounting, o Garbage Collector geracional, o GIL (o que ele é de verdade e o que muda com free-threading na PEP 703), gerenciamento de memória via `pymalloc` e as ferramentas de profiling que revelam tudo isso na prática. Fase Magus; 9 notas. Equivalente ao galho [[03-Dominios/Tecnologia/Java/JVM/index|JVM]] do Java. Assume os Galhos [[03-Dominios/Tecnologia/Python/Core/index|1 (Core)]] e [[03-Dominios/Tecnologia/Python/Funcional e idiomas avançados/index|4 (Funcional e idiomas avançados)]] como pré-requisito.

## Sobre este galho

Até aqui a trilha tratou Python como uma linguagem — sintaxe, OO, generators, tipos. Este galho vira a página e olha pro **interpretador**: a peça de software C (CPython é a implementação de referência, a que 95%+ do ecossistema roda) que de fato executa o bytecode gerado a partir do seu código. Entender isso muda como você debuga performance (por que um loop é lento?), memória (por que meu processo Python não devolve RAM?) e concorrência (por que `threading` não acelera CPU-bound, mas `asyncio` e `multiprocessing` sim?) — perguntas que só fazem sentido quando você sabe o que tem por baixo do `.py`.

**Audiência:** quem já é produtivo em Python (Core + OO + Funcional) e está pronto pro salto de "uso a linguagem" pra "entendo a máquina que a executa" — o mesmo salto que o galho JVM representa pra quem vem de Java.

## Magus

1. [[01 - O interpretador por dentro — ceval loop e frame objects|01 — O interpretador por dentro: ceval loop e frame objects]]
2. [[02 - Objetos em CPython — PyObject, refcounting e tipos internos|02 — Objetos em CPython: `PyObject`, refcounting e tipos internos]]
3. [[03 - Reference counting e o Garbage Collector geracional|03 — Reference counting e o Garbage Collector geracional]]
4. [[04 - O GIL — o que é de verdade e por que existe|04 — O GIL: o que é de verdade e por que existe]]
5. [[05 - GIL e concorrência na prática — threading vs multiprocessing|05 — GIL e concorrência na prática: threading vs multiprocessing]]
6. [[06 - Free-threading — o GIL opcional (PEP 703)|06 — Free-threading: o GIL opcional (PEP 703)]]
7. [[07 - Memory management — allocators, pymalloc e arenas|07 — Memory management: allocators, pymalloc e arenas]]
8. [[08 - Profiling — cProfile, py-spy, tracemalloc|08 — Profiling: `cProfile`, `py-spy`, `tracemalloc`]]
9. [[09 - Capstone — CPython internals|09 — Capstone: CPython internals]] — recapitula o galho.

## Todas as notas

```dataview
TABLE fase, status FROM "03-Dominios/Tecnologia/Python/CPython internals" WHERE type = "concept" SORT file.name ASC
```

## Veja também

- [[03-Dominios/Tecnologia/Python/index|Trilha Python]] (MOC central)
- [[03-Dominios/Tecnologia/Java/JVM/index|JVM (Java)]] — galho equivalente na trilha irmã, boa referência de contraste (GC determinístico vs. tracing, GIL vs. threads nativas)
- [[03-Dominios/Tecnologia/Python/Funcional e idiomas avançados/index|Funcional e idiomas avançados]] — Galho 4 (generators/decorators cujo custo real este galho explica)
- [[03-Dominios/Tecnologia/Python/Concorrência e paralelismo/index|Concorrência e paralelismo]] — Galho 7 (próximo; aprofunda threading/multiprocessing/asyncio à luz do GIL)
