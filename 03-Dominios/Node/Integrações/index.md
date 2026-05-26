---
title: "Integrações"
type: moc
publish: true
created: 2026-05-12
updated: 2026-05-12
status: growing
progresso: andamento
tags:
  - node
  - integrações
  - moc
  - backend
aliases:
  - Node Integrações
  - Integrações Node
---

# Integrações

> [!abstract] TL;DR
> Galho 9 da trilha Node Senior. Cobre as 10 integrações essenciais que qualquer API Node de produção precisa dominar: **PostgreSQL** via node-postgres (queries, pool, transações), **Redis** via ioredis (cache, pub/sub, TTL), **BullMQ** (filas de tarefas com Redis), **Kafka** via kafkajs (streaming de eventos, consumer groups, partições), **gRPC** via grpc-js (RPC tipado com Protocol Buffers), **GraphQL** via Apollo Server e Mercurius (schema-first, resolvers, N+1), **WebSockets** via ws e Socket.io (tempo real, rooms, namespaces), **Clientes HTTP** (fetch nativo, axios, got, undici — trade-offs e quando usar cada um), **Padrões de resiliência** (retry com backoff exponencial, circuit breaker, bulkhead), e **Cheatsheet e decision tree** para escolher a tecnologia certa para cada contexto de integração.

## Sobre este galho

Este galho cobre **integrações externas em Node.js**: como conectar APIs com bancos de dados SQL, caches, filas, brokers de mensagens, serviços gRPC, GraphQL e clientes em tempo real. O foco é a camada de integração — onde a lógica de negócio encontra o mundo externo — e os padrões que tornam essas conexões resilientes, observáveis e testáveis em produção.

Integração mal feita é a principal fonte de falhas em microsserviços: connections leak, retries sem backoff, circuit breakers ausentes e pools subutilizados. Cada nota endereça um problema real com código de produção, diagnóstico de problemas comuns e vocabulário para entrevista senior.

**Pré-requisito:** [[03-Dominios/Node/Runtime e Event Loop/index]] (galho 1) — event loop e async/await são fundamentais para entender como I/O externo é gerenciado. [[03-Dominios/Node/Frameworks e arquitetura/index]] (galho 4) — pressupõe uma API estruturada onde as integrações serão plugadas.

**Audiência primária:** dev senior em prep para entrevista internacional. Cada nota tem seção "Em entrevista" com resposta em inglês e vocabulário técnico.

**Audiência secundária:** dev que precisa integrar um serviço externo específico em API Node existente e quer o padrão correto sem reinventar a roda.

## Conteúdo

### Bloco A — Persistência e cache

1. [[03-Dominios/Node/Integrações/01 - PostgreSQL com node-postgres]] — Conexão com PostgreSQL via `pg`: pool de conexões, queries parametrizadas, transações e prepared statements
2. [[03-Dominios/Node/Integrações/02 - Redis e ioredis]] — Cache, pub/sub, TTL e estruturas de dados com ioredis v5; padrões de invalidação e uso correto de pipelines

### Bloco B — Filas e mensageria

3. [[03-Dominios/Node/Integrações/03 - BullMQ - filas de tarefas]] — Filas de tarefas com BullMQ sobre Redis: workers, retries, dead-letter queue, jobs recorrentes e monitoramento
4. [[03-Dominios/Node/Integrações/04 - Kafka com kafkajs]] — Streaming de eventos com kafkajs: producers, consumers, consumer groups, partições, offsets e rebalance

### Bloco C — Protocolos de comunicação

5. [[03-Dominios/Node/Integrações/05 - gRPC com grpc-js]] — RPC tipado com Protocol Buffers: definição de serviços `.proto`, streaming bidirecional, interceptors e reflexão
6. [[03-Dominios/Node/Integrações/06 - GraphQL com Apollo Server e Mercurius]] — APIs GraphQL em Node: schema-first com SDL, resolvers, DataLoader para N+1, subscriptions e comparativo Apollo vs Mercurius
7. [[03-Dominios/Node/Integrações/07 - WebSockets com ws e Socket.io]] — Comunicação em tempo real: WebSocket nativo com `ws`, rooms e namespaces com Socket.io v4, autenticação e scaling horizontal

### Bloco D — Clientes HTTP e resiliência

8. [[03-Dominios/Node/Integrações/08 - Clientes HTTP - fetch, axios, got e undici]] — Clientes HTTP em Node.js: fetch nativo (Node 18+), axios, got e undici — performance, interceptors, retry e quando usar cada um
9. [[03-Dominios/Node/Integrações/09 - Padrões de resiliência - retry, circuit breaker e bulkhead]] — Resiliência em integrações: retry com backoff exponencial, circuit breaker com `opossum`, bulkhead e timeout — protegendo a API de falhas em cascata

### Bloco E — Fechamento

10. [[03-Dominios/Node/Integrações/10 - Cheatsheet e decision tree de integrações]] — Decision tree para escolher a tecnologia certa: SQL vs Redis vs Kafka vs gRPC vs REST; cheatsheet de configurações essenciais por biblioteca

## Rotas alternativas

### Rota entrevista rápida

01 → 04 → 09 → 10. PostgreSQL (base), Kafka (mensageria — favorita em entrevista sênior), resiliência e decision tree. Cobre 80% das perguntas de system design sobre integrações em tempo mínimo.

### Rota tempo real

07 → 03 → 09. WebSockets com Socket.io, BullMQ para background jobs desacoplados do websocket e padrões de resiliência para o sistema como um todo.

### Rota microsserviços

05 → 04 → 09 → 10. gRPC para comunicação síncrona entre serviços, Kafka para comunicação assíncrona, resiliência e decision tree para tomar decisões arquiteturais defensáveis.

### Rota performance de API

01 → 02 → 08 → 09. PostgreSQL com pool otimizado, Redis como cache na frente, cliente HTTP correto para chamadas externas e resiliência. Endereça os gargalos mais comuns em APIs Node.

## Stack técnica

| Tecnologia | Biblioteca | Versão |
|---|---|---|
| PostgreSQL | `pg` (node-postgres) | v8 |
| Redis | `ioredis` | v5 |
| Filas | `bullmq` | v5 |
| Kafka | `kafkajs` | v2 |
| gRPC | `@grpc/grpc-js` | v1.10+ |
| GraphQL (framework) | `@apollo/server` | v4 |
| GraphQL (Fastify) | `mercurius` | latest |
| WebSocket nativo | `ws` | v8 |
| WebSocket full-featured | `socket.io` | v4 |
| Circuit breaker | `opossum` | latest |
| Resiliência geral | `cockatiel` | latest |
| HTTP client | `fetch` (Node 18+), `axios`, `got`, `undici` | — |

## Todas as notas

```dataview
TABLE status, updated
FROM "03-Dominios/Node/Integrações"
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
- [[03-Dominios/Node/ORMs e banco de dados/index]] — galho 6
