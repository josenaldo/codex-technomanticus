---
title: "ORMs e banco de dados"
created: 2026-05-10
updated: 2026-05-10
type: moc
status: growing
publish: true
tags:
  - node
  - orm
  - banco-de-dados
  - moc
aliases:
  - ORMs Node
  - Galho 6 - ORMs
---

# ORMs e banco de dados

> [!abstract] TL;DR
> Galho 6 da trilha Node Senior. Um ORM (Object-Relational Mapper) abstrai SQL e mapeia tabelas para objetos/classes, eliminando boilerplate mas introduzindo trade-offs de performance e transparência. O ecossistema Node tem 4 players principais em 2026: **Sequelize** (maduro, API fluente, legado sólido), **Prisma** (schema-first, type safety excepcional, geração de código), **TypeORM** (decorators estilo JPA, favorito de devs Java/C# migrando), **Drizzle** (lightweight, sem runtime mágico, SQL explícito com tipos). Padrões críticos cobertos: detecção e resolução de **N+1 queries** com DataLoader, **migrations** e versionamento de schema, **transações** (manual vs automático), e **paginação** (offset, cursor, keyset). Decision tree no final para escolher o ORM certo para cada contexto.

## Sobre este galho

Este galho cobre **ORMs e banco de dados em Node.js**: os 4 principais ORMs do ecossistema (Sequelize, Prisma, TypeORM, Drizzle), seus posicionamentos em 2026 e os padrões críticos que aparecem em qualquer API de produção. O foco não é dominar todos os ORMs, mas entender os trade-offs de cada um e saber defender a escolha em entrevista ou code review.

Os padrões transversais são tão importantes quanto os ORMs em si. N+1 queries destroem performance silenciosamente. Migrations mal gerenciadas quebram deploys. Transações mal colocadas geram inconsistência de dados. Paginação ingênua com `OFFSET` trava em tabelas grandes. Cada um desses tópicos tem uma nota dedicada com diagnóstico, solução e vocabulário para entrevista.

**Pré-requisito:** [[03-Dominios/Node/Frameworks e arquitetura/index]] (galho 4) — pressupõe entender como uma API Node está estruturada antes de conectar banco. [[Node.js]] (tronco) — especialmente async/await e event loop para entender o comportamento de queries assíncronas.

**Audiência primária:** dev senior em prep para entrevista internacional. Cada nota tem seção "Em entrevista" com resposta em inglês + vocabulário técnico para impressionar entrevistadores de empresas globais.

**Audiência secundária:** dev integrando banco de dados em API Node existente que precisa escolher ORM, estruturar migrations ou diagnosticar problema de performance.

## Comece por aqui — trilha completa (10 notas)

### Bloco A — Visão geral

1. [[01 - Panorama de ORMs]]

### Bloco B — Os 4 ORMs

2. [[02 - Sequelize - queries e associações]]
3. [[03 - Prisma - schema-first e type safety]]
4. [[04 - TypeORM - decorators ao estilo JPA]]
5. [[05 - Drizzle - ORM lightweight e type-safe]]

### Bloco C — Padrões críticos

6. [[06 - N+1 queries - detecção e DataLoader]]
7. [[07 - Migrations e versionamento de schema]]
8. [[08 - Transações - gerenciamento manual vs automático]]
9. [[09 - Paginação - offset, cursor e keyset]]

### Bloco D — Fechamento

10. [[10 - Cheatsheet e decision tree de ORMs]]

## Rotas alternativas

### Rota entrevista

01 → 03 → 06 → 10. Foco nos 4 ORMs (via panorama comparativo), N+1 e decision tree. Cobre 90% das perguntas de entrevista sobre banco de dados em Node em tempo mínimo.

### Rota migrations

07 → 08 → 10. Para quem já escolheu ORM e precisa estruturar o ciclo de vida do schema: versionamento, estratégias de rollback e checklist de deploy.

### Rota performance / N+1

06 → 09 → 10. Para quem está investigando lentidão em API existente. N+1 e paginação são as duas causas mais comuns de degradação silenciosa em APIs com ORM.

### Rota onboarding Prisma

03 → 07 → 08 → 09. Trilha prática para quem vai adotar Prisma em projeto novo: schema-first, migrations via `prisma migrate`, transações com `$transaction` e paginação com cursor nativo do Prisma.

## Todas as notas

```dataview
TABLE status, updated
FROM "03-Dominios/Node/ORMs e banco de dados"
WHERE type = "concept"
SORT file.name ASC
```

## Veja também

- [[03-Dominios/Node/index|Node.js (MOC central)]]
- [[Node.js]] — tronco
- [[03-Dominios/Node/Runtime e Event Loop/index]] — galho 1
- [[03-Dominios/Node/Paralelismo/index]] — galho 2
- [[03-Dominios/Node/Streams/index]] — galho 3
- [[03-Dominios/Node/Frameworks e arquitetura/index]] — galho 4
- [[03-Dominios/Node/Observability e produção/index]] — galho 5
