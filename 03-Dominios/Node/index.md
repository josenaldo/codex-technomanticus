---
title: "Node.js"
type: moc
publish: true
created: 2026-05-04
updated: 2026-05-13
status: growing
progresso: andamento
tags:
  - node
  - moc
  - backend
aliases:
  - NodeJS
  - Node
---
# Node.js

> [!abstract] TL;DR
> Trilha Node Senior em 9 galhos: Runtime e Event Loop, Paralelismo, Streams, Frameworks e arquitetura, Observability e produção, ORMs e banco de dados, Tooling e ecossistema moderno, Segurança, Integrações. Cada galho cobre os 4–5 players principais de cada área, padrões críticos de produção, vocabulário técnico e respostas de entrevista em inglês.

Estante de Node.js da trilha senior em prep para entrevistas internacionais. Cobre desde os fundamentos do runtime (event loop, libuv, single-thread) até segurança (supply chain, JWT, OAuth 2.0, RBAC, Helmet.js, OWASP Top 10) e integrações de produção (PostgreSQL, Redis, Kafka, gRPC, GraphQL, WebSockets, HTTP clients e padrões de resiliência). A trilha está organizada em 9 galhos temáticos progressivos — cada galho é um conjunto de notas atômicas com seção de entrevista em inglês, vocabulário técnico e decision trees práticos.

## Conteúdo

### Galhos da trilha Node Senior

- [[03-Dominios/Node/Runtime e Event Loop/index]] — galho 1: o motor do Node (single-thread, libuv, fases, microtasks, async/await, bloqueio, diagnóstico)
- [[03-Dominios/Node/Paralelismo/index]] — galho 2: as 3 ferramentas de paralelismo (Worker Threads, Cluster, child_process), SharedArrayBuffer/Atomics, pool de workers, contexto de produção, decision tree
- [[03-Dominios/Node/Streams/index]] — galho 3: abstração fundamental para processar dados em chunks (4 tipos, backpressure, pipeline, async iter, Web Streams, padrões práticos, performance)
- [[03-Dominios/Node/Frameworks e arquitetura/index]] — galho 4: os 4 frameworks principais (Express, NestJS, Fastify, Hono), patterns transversais (middleware, error handling, validation), Clean Architecture e DI
- [[03-Dominios/Node/Observability e produção/index]] — galho 5: logs, métricas, traces, profiling avançado, SLOs, dashboards Grafana, alertas multi-janela e checklists de produção
- [[03-Dominios/Node/ORMs e banco de dados/index]] — galho 6: os 4 ORMs principais (Sequelize, Prisma, TypeORM, Drizzle), padrões críticos de N+1, migrations, transações e paginação, decision tree para escolha de ORM
- [[03-Dominios/Node/Tooling e ecossistema moderno/index]] — galho 7: package managers (npm, pnpm, yarn, Bun), semver, ESM vs CJS, TypeScript nativo, test runner nativo (`node:test`), DX flags e SEA
- [[03-Dominios/Node/Segurança/index]] — galho 8: supply chain, segredos, validação de entrada (Zod/Joi), JWT, OAuth 2.0 e OIDC, RBAC, rate limiting, Helmet.js e OWASP Top 10
- [[03-Dominios/Node/Integrações/index]] — galho 9: PostgreSQL (node-postgres), Redis (ioredis), BullMQ, Kafka (kafkajs), gRPC, GraphQL, WebSockets, HTTP clients e padrões de resiliência

## Veja também

- [[03-Dominios/JavaScript/index|JavaScript]]
- [[03-Dominios/TypeScript/index|TypeScript]]
- [[Ferramentas|Ferramentas]]
