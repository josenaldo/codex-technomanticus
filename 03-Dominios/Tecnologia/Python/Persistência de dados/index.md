---
title: "Python — Persistência de dados"
created: 2026-07-11
type: moc
status: growing
publish: true
tags:
  - python
  - moc
aliases:
  - "Galho 9 - Persistência de dados"
---

# Persistência de dados

> [!abstract] TL;DR
> Galho 9 da trilha Python: como Python fala com o banco relacional em produção — `SQLAlchemy` Core (SQL como expressão Python) e ORM (`Session`, mapeamento de classes, relationships), migrations versionadas com `Alembic`, o Django ORM como o outro grande caminho (QuerySets lazy, managers), o problema clássico de N+1 e como resolvê-lo (`joinedload`/`selectinload` vs. `select_related`/`prefetch_related`), transações e isolamento (ACID na prática, isolation levels, deadlocks de aplicação), e connection pooling em produção. Fase Adepto→Magus; 8 notas. Primeiro galho do bloco "Backend e arquitetura" (9-13) — abre a trilha pra construção de sistemas de verdade, depois do núcleo da linguagem (1-6) e concorrência (7-8).

## Sobre este galho

Até aqui a trilha ensinou a linguagem e como ela executa. Este galho vira a página pra onde a maioria dos sistemas backend guarda estado de verdade: o banco relacional. Dois caminhos dominam o ecossistema Python — `SQLAlchemy` (explícito, duas camadas Core/ORM, usado com FastAPI/Flask e frameworks agnósticos) e o `Django ORM` (integrado, opinativo, parte do framework). Este galho ensina os dois, mas o foco maior vai pros problemas que aparecem em QUALQUER ORM assim que o sistema cresce: N+1, transações mal isoladas, pool de conexões saturado.

**Audiência:** quem já escreve Python de produção (núcleo da linguagem fechado) e precisa persistir dados de verdade — não é um tutorial de SQL, assume que você já sabe o básico de banco relacional.

## Adepto

1. [[01 - SQLAlchemy Core — Engine, Connection e expressão SQL|01 — SQLAlchemy Core: `Engine`, `Connection` e expressão SQL]]
2. [[02 - SQLAlchemy ORM — Session, mapped classes e relationships|02 — SQLAlchemy ORM: `Session`, mapped classes e relationships]]
3. [[03 - Migrations com Alembic — versionamento de schema|03 — Migrations com Alembic: versionamento de schema]]

## Adepto→Magus

4. [[04 - Django ORM — QuerySets, managers e migrations nativas|04 — Django ORM: `QuerySet`s, managers e migrations nativas]]

## Magus

5. [[05 - N+1 e eager loading — joinedload-selectinload vs select_related-prefetch_related|05 — N+1 e eager loading: `joinedload`/`selectinload` vs. `select_related`/`prefetch_related`]]
6. [[06 - Transações e isolamento — ACID na prática, isolation levels, deadlocks de aplicação|06 — Transações e isolamento: ACID na prática, isolation levels, deadlocks de aplicação]]
7. [[07 - Connection pooling e performance em produção|07 — Connection pooling e performance em produção]]
8. [[08 - Capstone — projetando a camada de persistência de um serviço real|08 — Capstone: projetando a camada de persistência de um serviço real]] — recapitula o galho.

## Veja também

- [[03-Dominios/Tecnologia/Python/index|Trilha Python]] (MOC central)
- [[03-Dominios/Tecnologia/Python/Concorrência e paralelismo/index|Concorrência e paralelismo]] — Galho 7 (async ORM/drivers tocam concorrência; aqui o foco é o modelo relacional em si)
- [[03-Dominios/Tecnologia/Python/Web e APIs REST/index|Web e APIs REST]] — Galho 10 (próximo; consome a camada de persistência via endpoints)
- [[03-Dominios/Tecnologia/Python/Arquitetura e Design Patterns/index|Arquitetura e Design Patterns]] — Galho 13 (Repository/Unit of Work formalizam os padrões de acesso a dados vistos aqui)
