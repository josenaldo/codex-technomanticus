---
title: "Python — OO e Data Model"
created: 2026-07-09
type: moc
status: growing
publish: true
tags:
  - python
  - moc
aliases:
  - "Galho 3 - OO e Data Model"
---

# OO e Data Model

> [!abstract] TL;DR
> Galho 3 da trilha Python: classes, herança e MRO, o **Data Model** (dunder methods — o coração do livro *Python Fluente*), properties, dataclasses, ABC/Protocol (tipagem estrutural) e uma introdução honesta a metaclasses. Fases Adepto→Magus; 9 notas. Assume os Galhos [[03-Dominios/Tecnologia/Python/Core/index|1 (Core)]] e [[03-Dominios/Tecnologia/Python/Collections e Comprehensions/index|2 (Collections)]] como pré-requisito.

## Sobre este galho

Este é o galho mais "pythônico" da trilha — onde a linguagem revela sua filosofia central: **o Data Model**. Python não tem interfaces especiais pra "objeto iterável" ou "objeto comparável" — qualquer classe que implemente os métodos certos (`__iter__`, `__eq__`, `__len__`...) simplesmente *é* iterável/comparável/o-que-for. Esse galho ensina classes do básico (atributos, métodos, herança) até o data model completo, passando por properties, dataclasses, tipagem estrutural com Protocol, e uma introdução sóbria a metaclasses (ferramenta poderosa, raramente necessária).

**Audiência:** quem já é confortável com Python básico (Core + Collections) e quer entender OO "de verdade" em Python — não a tradução mecânica de Java/C#, mas o modelo mental próprio da linguagem.

Iteradores/geradores de verdade (o "como" por trás do `__iter__`/`__next__`) são aprofundados no [[03-Dominios/Tecnologia/Python/Funcional e idiomas avançados/index|Galho 4]] — aqui é a introdução via Data Model.

## Adepto

1. [[01 - Classes — definição, atributos e métodos|01 — Classes: definição, atributos e métodos]]
2. [[02 - Herança e MRO|02 — Herança e MRO]]
3. [[03 - O Data Model — dunder methods essenciais|03 — O Data Model: dunder methods essenciais]]
4. [[04 - Properties e encapsulamento|04 — Properties e encapsulamento]]
5. [[05 - Dataclasses|05 — Dataclasses]]
6. [[06 - ABC e Protocol — tipagem estrutural|06 — ABC e Protocol: tipagem estrutural]]

## Magus

7. [[07 - Operator overloading e protocolos avançados|07 — Operator overloading e protocolos avançados]]
8. [[08 - Metaclasses — introdução|08 — Metaclasses: introdução]]
9. [[09 - Composição vs herança|09 — Composição vs herança]] — capstone do galho.

## Todas as notas

```dataview
TABLE fase, status FROM "03-Dominios/Tecnologia/Python/OO e Data Model" WHERE type = "concept" SORT file.name ASC
```

## Veja também

- [[03-Dominios/Tecnologia/Python/index|Trilha Python]] (MOC central)
- [[03-Dominios/Tecnologia/Python/Core/index|Core]] — Galho 1
- [[03-Dominios/Tecnologia/Python/Collections e Comprehensions/index|Collections e Comprehensions]] — Galho 2 (namedtuple é ponte pra dataclasses aqui)
- [[03-Dominios/Tecnologia/Python/Funcional e idiomas avançados/index|Funcional e idiomas avançados]] — Galho 4 (próximo)
