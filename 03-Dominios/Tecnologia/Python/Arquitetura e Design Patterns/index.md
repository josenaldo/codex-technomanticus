---
title: "Python — Arquitetura e Design Patterns"
created: 2026-07-12
type: moc
status: growing
publish: true
tags:
  - python
  - moc
aliases:
  - "Galho 13 - Arquitetura e Design Patterns"
---

# Arquitetura e Design Patterns

> [!abstract] TL;DR
> Galho 13 da trilha Python: por que os padrões GoF clássicos pesam menos em Python (first-class functions, duck typing, decorators já resolvem boa parte do que Java resolve com classe+interface), domain modeling separado do framework, Repository e Unit of Work formalizando o que já apareceu organicamente nos Galhos 9-12 (a `Session` do SQLAlchemy JÁ É uma Unit of Work), injeção de dependência sem framework pesado, Service Layer orquestrando casos de uso, arquitetura hexagonal/Ports and Adapters aplicada em FastAPI. Fecha com capstone refatorando a API de Tarefas pra essa arquitetura. Fase Magus; 8 notas. Último galho do bloco "Backend e arquitetura" (9-13) — fecha esse bloco antes da trilha entrar em plataforma distribuída/produção (14-18).

## Sobre este galho

Este galho tem uma fonte primária declarada desde o spec: **Architecture Patterns with Python**, de Harry Percival e Bob Gregory (O'Reilly) — o livro que a trilha usa como referência de rigor pra este tema (já citado no Galho 12, nota 08, sobre TDD outside-in). O galho pega os padrões que o livro desenvolve — Repository, Unit of Work, Service Layer, arquitetura hexagonal — e os aplica sobre o código real construído nos Galhos 9 (persistência), 10 (API REST), 11 (segurança) e 12 (testes) desta trilha, em vez de reensinar num domínio de exemplo genérico.

**Fronteiras anti-duplicação:** os padrões GoF clássicos em si (Strategy, Observer, Factory, Adapter etc.) já estão documentados de forma agnóstica de linguagem em [[03-Dominios/Engenharia/Design de Software/Design Patterns|Engenharia/Design de Software]] — este galho não os reensina, referencia e discute por que MENOS deles aparecem explicitamente em código Python idiomático. SOLID já está coberto em [[03-Dominios/Engenharia/Design de Software/SOLID/index|Engenharia/Design de Software/SOLID]] — referenciado, não repetido. Arquitetura hexagonal/Ports and Adapters como CONCEITO já aparece em [[03-Dominios/Engenharia/Arquitetura/index|Engenharia/Arquitetura]] — este galho é a aplicação Python concreta, não a teoria do estilo arquitetural. `Session` como Unit of Work já foi mencionado sem ser formalizado no Galho 9 (nota 02) — este galho nomeia e generaliza o padrão. `Depends()` do FastAPI já ensinou injeção de dependência mecânica no Galho 10 (nota 04) — este galho discute DI como PRINCÍPIO arquitetural, não a sintaxe do framework.

**Audiência:** quem já construiu, blindou e testou a API dos Galhos 9-12 e quer entender por que o código atual (handler HTTP falando direto com `Session`) tem um acoplamento que preocupa em sistemas maiores — e como formalizar as camadas que resolvem isso.

## Magus

1. [[01 - Por que GoF clássico é menos necessário em Python|01 — Por que GoF clássico é menos necessário em Python]]
2. [[02 - Domain modeling — separando a lógica de negócio do framework|02 — Domain modeling: separando a lógica de negócio do framework]]
3. [[03 - Repository pattern — abstraindo a persistência|03 — Repository pattern: abstraindo a persistência]]
4. [[04 - Unit of Work — formalizando o padrão que já existia|04 — Unit of Work: formalizando o padrão que já existia]]
5. [[05 - Injeção de dependência como princípio — sem framework pesado|05 — Injeção de dependência como princípio: sem framework pesado]]
6. [[06 - Service Layer — orquestrando casos de uso|06 — Service Layer: orquestrando casos de uso]]
7. [[07 - Arquitetura hexagonal e Ports and Adapters em Python|07 — Arquitetura hexagonal e Ports and Adapters em Python]]
8. [[08 - Capstone — refatorando a API de Tarefas pra arquitetura hexagonal|08 — Capstone: refatorando a API de Tarefas pra arquitetura hexagonal]] — recapitula o galho e fecha o bloco "Backend e arquitetura".

## Todas as notas

```dataview
TABLE fase, status FROM "03-Dominios/Tecnologia/Python/Arquitetura e Design Patterns" WHERE type = "concept" SORT file.name ASC
```

## Veja também

- [[03-Dominios/Tecnologia/Python/index|Trilha Python]] (MOC central)
- [[03-Dominios/Engenharia/Design de Software/Design Patterns|Design Patterns (GoF)]] — padrões clássicos genéricos, referenciados sem repetição
- [[03-Dominios/Engenharia/Design de Software/SOLID/index|SOLID]] — princípios de design, referenciados sem repetição
- [[03-Dominios/Engenharia/Arquitetura/index|Arquitetura (Engenharia)]] — estilo hexagonal/clean architecture como teoria agnóstica
- [[03-Dominios/Tecnologia/Python/Persistência de dados/index|Persistência de dados]] — Galho 9 (Session/Engine que este galho formaliza como Repository/UoW)
- [[03-Dominios/Tecnologia/Python/Web e APIs REST/index|Web e APIs REST]] — Galho 10 (handler HTTP que este galho desacopla via Service Layer)
- [[03-Dominios/Tecnologia/Python/Testes/index|Testes]] — Galho 12 (a capstone já apontou os padrões aparecendo informalmente na suíte)
