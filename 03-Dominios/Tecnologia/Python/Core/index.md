---
title: "Python — Core"
created: 2026-07-09
type: moc
status: growing
publish: true
tags:
  - python
  - moc
aliases:
  - "Python Core"
  - "Galho 1 - Core"
---

# Core

> [!abstract] TL;DR
> Galho 1 da trilha Python: os fundamentos absolutos da linguagem — como ela executa, tipos e variáveis, controle de fluxo, funções, strings, exceções e o sistema de módulos. Fase única **Iniciado**; 9 notas. Ponto de partida antes de qualquer outro galho.

## Sobre este galho

Este é o alicerce de toda a trilha Python — sem ele, nenhum outro galho faz sentido. Cobre o que qualquer código Python precisa: como o interpretador executa um arquivo `.py`, os tipos primitivos e sua mutabilidade, as estruturas de controle (incluindo o `match`/`case` moderno), como escrever e chamar funções, manipular strings, tratar erros, e organizar código em módulos e pacotes.

**Audiência primária:** quem está aprendendo Python pela primeira vez ou vem de outra linguagem e quer o modelo mental certo desde o início — cada nota expõe não só "como fazer" mas "por que Python decidiu fazer assim" (comparações com Java/JS quando ajudam quem já programa). **Audiência secundária:** quem já usa Python no dia a dia mas nunca formalizou os fundamentos e quer preencher lacunas antes de avançar pros galhos de OO/funcional/concorrência.

Collections/comprehensions avançadas são o [[03-Dominios/Tecnologia/Python/Collections e Comprehensions/index|Galho 2]]; classes e o data model são o [[03-Dominios/Tecnologia/Python/OO e Data Model/index|Galho 3]]; closures/decorators/generators de verdade são o [[03-Dominios/Tecnologia/Python/Funcional e idiomas avançados/index|Galho 4]] — este galho fica só no essencial pra começar a escrever Python com segurança.

## Iniciado

1. [[01 - O que é Python e como ele executa|01 — O que é Python e como ele executa]] — o interpretador, bytecode, REPL, CPython vs outras implementações.
2. [[02 - Tipos e variáveis|02 — Tipos e variáveis]] — dynamic + strong typing, mutabilidade, `None`, tipos primitivos, `is` vs `==`.
3. [[03 - Operadores e expressões|03 — Operadores e expressões]] — aritméticos, comparação, lógicos, bitwise, walrus operator.
4. [[04 - Controle de fluxo — if-elif-else e match-case|04 — Controle de fluxo (if/elif/else e match/case)]] — condicionais, truthiness, structural pattern matching.
5. [[05 - Loops — for, while, range, enumerate, zip|05 — Loops (for, while, range, enumerate, zip)]] — laços, `break`/`continue`, a cláusula `else` de loop.
6. [[06 - Funções — definição, argumentos e escopo básico|06 — Funções: definição, argumentos e escopo básico]] — `def`, `*args`/`**kwargs`, escopo LEGB.
7. [[07 - Strings e formatação|07 — Strings e formatação]] — f-strings, métodos, `str` vs `bytes`.
8. [[08 - Erros e exceções|08 — Erros e exceções]] — `try`/`except`/`else`/`finally`, hierarquia, EAFP vs LBYL.
9. [[09 - Módulos e imports|09 — Módulos e imports]] — sistema de import, pacotes, `__name__ == "__main__"`. Capstone do galho.

## Rotas alternativas

### Completa

01 → 02 → 03 → 04 → 05 → 06 → 07 → 08 → 09. Percurso linear recomendado para quem está começando do zero.

### Já programo, só quero o idioma Python

01 → 02 (skim) → 04 (match/case é novo mesmo pra quem já programa) → 06 (`*args`/`**kwargs` é a maior pegadinha de quem vem de Java/C#) → 08 (EAFP é uma inversão cultural real) → 09.

## Veja também

- [[03-Dominios/Tecnologia/Python/index|Trilha Python]] (MOC central)
- [[03-Dominios/Tecnologia/Python/Collections e Comprehensions/index|Collections e Comprehensions]] — Galho 2
- [[03-Dominios/Tecnologia/Python/OO e Data Model/index|OO e Data Model]] — Galho 3
- [[03-Dominios/Tecnologia/Java/index|Java]] — trilha irmã, mesmo padrão estrutural
