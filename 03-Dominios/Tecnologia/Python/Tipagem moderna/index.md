---
title: "Python — Tipagem moderna"
created: 2026-07-10
type: moc
status: growing
publish: true
tags:
  - python
  - moc
aliases:
  - "Galho 5 - Tipagem moderna"
---

# Tipagem moderna

> [!abstract] TL;DR
> Galho 5 da trilha Python: type hints do básico ao avançado — `Union`/`Optional`, generics (`TypeVar`/`Generic`/sintaxe PEP 695), checagem estática com `mypy`/`pyright`, tipos estruturados (`TypedDict`/`Literal`/`NewType`) e validação em runtime com Pydantic. Fase Adepto→Magus; 8 notas. Assume os Galhos [[03-Dominios/Tecnologia/Python/Core/index|1 (Core)]], [[03-Dominios/Tecnologia/Python/OO e Data Model/index|3 (OO e Data Model)]] — especialmente a nota de [[03-Dominios/Tecnologia/Python/OO e Data Model/06 - ABC e Protocol — tipagem estrutural|Protocol/ABC]] — e [[03-Dominios/Tecnologia/Python/Funcional e idiomas avançados/index|4 (Funcional e idiomas avançados)]] como pré-requisito.

## Sobre este galho

Python é dinamicamente tipado por natureza, mas desde a PEP 484 (2014) ganhou um sistema de type hints opcional e cada vez mais usado em produção — não pra mudar o runtime, mas pra dar a ferramentas estáticas (mypy, pyright) e bibliotecas de validação (Pydantic) informação suficiente pra pegar bugs antes de rodar o código. Este galho cobre esse sistema do zero: anotações básicas, generics, as duas famílias de ferramentas que fazem algo com essas anotações (checagem estática vs. validação em runtime), e os tipos estruturados que preenchem lacunas específicas (`TypedDict` pra dicts com schema, `Literal` pra valores fechados, `NewType` pra distinguir tipos "primos"). `typing.Protocol` e `abc.ABC` — as duas formas de tipagem nominal/estrutural aplicadas a classes — já foram cobertas no Galho 3 e não são repetidas aqui.

**Audiência:** quem já escreve Python funcional/OO confortavelmente e quer o nível de rigor de tipos esperado em times sêniores — sobretudo quem vem de linguagens estaticamente tipadas (Java, TypeScript) e estranha a ausência de erro em tempo de execução quando um tipo "errado" é passado.

## Adepto

1. [[01 - Type hints — fundamentos e gradual typing|01 — Type hints: fundamentos e gradual typing]]
2. [[02 - Union, Optional e o operador |02 — Union, Optional e o operador `|`]]
3. [[03 - Generics — TypeVar, Generic e sintaxe moderna|03 — Generics: `TypeVar`, `Generic` e sintaxe moderna]]
4. [[04 - mypy e pyright — checagem estática na prática|04 — `mypy` e `pyright`: checagem estática na prática]]
5. [[05 - TypedDict, Literal, NewType e Final|05 — `TypedDict`, `Literal`, `NewType` e `Final`]]
6. [[06 - Pydantic — validação em runtime|06 — Pydantic: validação em runtime]]

## Magus

7. [[07 - Typing avançado — overload, Self, ParamSpec|07 — Typing avançado: `overload`, `Self`, `ParamSpec`]]
8. [[08 - Capstone — tipagem moderna|08 — Capstone: tipagem moderna]] — recapitula o galho.

## Todas as notas

```dataview
TABLE fase, status FROM "03-Dominios/Tecnologia/Python/Tipagem moderna" WHERE type = "concept" SORT file.name ASC
```

## Veja também

- [[03-Dominios/Tecnologia/Python/index|Trilha Python]] (MOC central)
- [[03-Dominios/Tecnologia/Python/OO e Data Model/index|OO e Data Model]] — Galho 3 (Protocol/ABC, pré-requisito não repetido aqui)
- [[03-Dominios/Tecnologia/Python/Funcional e idiomas avançados/index|Funcional e idiomas avançados]] — Galho 4 (decorators genéricos tipados com `ParamSpec` retomam esse galho)
- [[03-Dominios/Tecnologia/Python/CPython internals/index|CPython internals]] — Galho 6 (próximo)
