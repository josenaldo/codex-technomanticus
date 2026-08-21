---
title: "Python — Funcional e idiomas avançados"
created: 2026-07-10
type: moc
status: growing
publish: true
tags:
  - python
  - moc
aliases:
  - "Galho 4 - Funcional e idiomas avançados"
---

# Funcional e idiomas avançados

> [!abstract] TL;DR
> Galho 4 da trilha Python: o "como por dentro" de generators e iterators, closures de verdade, decorators (fundamentos e com argumentos) e o kit `functools`, fechando com context managers via generator. Fases Adepto→Magus; 9 notas. Assume os Galhos [[03-Dominios/Tecnologia/Python/Core/index|1 (Core)]], [[03-Dominios/Tecnologia/Python/Collections e Comprehensions/index|2 (Collections)]] e [[03-Dominios/Tecnologia/Python/OO e Data Model/index|3 (OO e Data Model)]] como pré-requisito.

## Sobre este galho

Este galho pega três ferramentas que o resto da linguagem usa por baixo dos panos — iteração, funções de primeira classe e closures — e mostra como elas realmente funcionam. O Galho 2 já usou generator expressions e o Galho 3 já tocou no protocolo iterator via Data Model; aqui é o aprofundamento: como escrever seus próprios generators, como `yield from` delega pra subgenerators, como closures capturam variáveis (e a armadilha clássica do late binding em loops), e como decorators — que parecem mágica — são só açúcar sintático pra `func = decorador(func)`. Fecha com `functools` (o kit de ferramentas funcionais da stdlib) e uma segunda forma de escrever context managers, via generator.

**Audiência:** quem já é confortável com Python básico e OO (Core + Collections + OO e Data Model) e quer entender os idiomas que tornam o código Python "pythônico" — os mesmos padrões usados por bibliotecas populares (Flask, pytest, Click) internamente.

## Adepto

1. [[01 - Iterators e o protocolo __iter__ __next__|01 — Iterators e o protocolo `__iter__`/`__next__`]]
2. [[02 - Generators — yield e generator functions|02 — Generators: `yield` e generator functions]]
3. [[03 - yield from e delegação de generators|03 — `yield from` e delegação de generators]]
4. [[04 - Closures de verdade|04 — Closures de verdade]]
5. [[05 - Decorators — fundamentos|05 — Decorators: fundamentos]]

## Magus

6. [[06 - Decorators com argumentos e functools.wraps|06 — Decorators com argumentos e `functools.wraps`]]
7. [[07 - functools — ferramentas funcionais|07 — `functools`: ferramentas funcionais]]
8. [[08 - Context managers via generator|08 — Context managers via generator]]
9. [[09 - Capstone — funcional e idiomas avançados|09 — Capstone: funcional e idiomas avançados]] — recapitula o galho.

## Veja também

- [[03-Dominios/Tecnologia/Python/index|Trilha Python]] (MOC central)
- [[03-Dominios/Tecnologia/Python/Core/index|Core]] — Galho 1
- [[03-Dominios/Tecnologia/Python/Collections e Comprehensions/index|Collections e Comprehensions]] — Galho 2
- [[03-Dominios/Tecnologia/Python/OO e Data Model/index|OO e Data Model]] — Galho 3 (context managers manuais, ponte pra generator-based aqui)
