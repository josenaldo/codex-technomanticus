---
title: "Frameworks e arquitetura"
created: 2026-05-08
updated: 2026-05-08
type: moc
status: seedling
publish: true
tags:
  - node
  - frameworks
  - moc
aliases:
  - Frameworks Node
  - Galho 4 - Frameworks
---

# Frameworks e arquitetura

> [!abstract] TL;DR
> Galho 4 da trilha Node Senior. Cobre os 4 frameworks principais (Express, NestJS, Fastify, Hono) com trade-offs explícitos, patterns transversais (middleware, error handling Problem Details, schema validation), Clean Architecture em Node e DI manual vs container. Pré-requisito: galho 1 (Runtime e Event Loop). Sem dogma framework-religioso: decision tree é matching, não ranking.

## Sobre este galho

Este galho cobre **frameworks Node**: os 4 principais (Express, NestJS, Fastify, Hono) com trade-offs explícitos, patterns transversais (middleware, error handling Problem Details, schema validation), Clean Architecture em Node e DI manual vs container. Sem dogma framework-religioso: decision tree é matching, não ranking.

Pré-requisito: galho 1 ([[03-Dominios/Node/Runtime e Event Loop/index]]) - pressupõe entender event loop. Galho 3 ([[03-Dominios/Node/Streams/index]]) é referência cruzada, porque frameworks abstraem multipart e streaming via libs como busboy.

**Audiência primária:** dev senior em prep para entrevista internacional. Cada nota tem seção "Em entrevista" com frase pronta em inglês + vocabulário.

**Audiência secundária:** o mesmo dev decidindo framework/arquitetura para projeto novo, ou avaliando migração entre frameworks.

## Comece por aqui - trilha completa (12 notas)

### Bloco A - Visão geral

1. [[01 - Os 4 frameworks - Express, NestJS, Fastify, Hono]]

### Bloco B - Frameworks principais

2. [[02 - Express idiomático]]
3. [[03 - NestJS - fundamentos]]
4. [[04 - NestJS - guards, interceptors, pipes, filters]]
5. [[05 - Fastify - schema-first, plugins, performance]]

### Bloco C - Edge runtimes

6. [[06 - Hono e edge runtimes]]

### Bloco D - Patterns transversais

7. [[07 - Middleware pipeline]]
8. [[08 - Error handling estruturado]]
9. [[09 - Validation com schema]]

### Bloco E - Arquitetura

10. [[10 - Clean Architecture em Node]]
11. [[11 - DI - manual vs container]]

### Bloco F - Fechamento

12. [[12 - Decision tree + cheatsheet]]

## Rotas alternativas

### Rota entrevista internacional

01 -> 02 -> 03 -> 04 -> 07 -> 08 -> 12. Foco em explicar trade-offs entre frameworks para entrevistador.

### Rota produção

01 -> 05 -> 09 -> 10 -> 12. Foco em decidir qual framework usar em projeto novo.

### Rota NestJS-first

03 -> 04 -> 09 -> 11. Para quem vai usar NestJS em projeto enterprise.

### Rota patterns sobre framework

07 -> 08 -> 09 -> 10. Para entender padrões transversais aos frameworks.

### Rota edge

01 -> 06 -> 12. Para quem está olhando Cloudflare Workers, Deno Deploy, Bun ou serverless multi-runtime.

## Todas as notas

```dataview
TABLE status, updated
FROM "03-Dominios/Node/Frameworks e arquitetura"
WHERE type = "concept"
SORT file.name ASC
```

## Veja também

- [[03-Dominios/Node/index|Node.js (MOC central)]]
- [[Node.js]] - tronco
- [[03-Dominios/Node/Runtime e Event Loop/index]] - galho 1
- [[03-Dominios/Node/Paralelismo/index]] - galho 2
- [[03-Dominios/Node/Streams/index]] - galho 3

