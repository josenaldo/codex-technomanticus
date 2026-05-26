---
title: "Decision tree + cheatsheet"
created: 2026-05-08
updated: 2026-05-08
type: concept
status: seedling
publish: true
tags:
  - node
  - frameworks
  - cheatsheet
  - decision-tree
  - referencia
aliases:
  - Cheatsheet frameworks
  - Decision tree frameworks
---

# Decision tree + cheatsheet

> [!abstract] TL;DR
> Fechamento do galho: decision tree para escolher framework, tabela comparativa, top armadilhas e vocabulário PT->EN. Use como revisão rápida antes de entrevista ou decisão de arquitetura.

## Decision tree - qual framework para qual contexto

```text
Qual o contexto?

├─ Microsserviço I/O-bound simples, time pequeno
│  ├─ Performance/contrato importam muito? -> Fastify
│  └─ Time conhece Express e quer simplicidade? -> Express
│
├─ App enterprise, domínio complexo, time grande
│  ├─ DI, módulos e convenção corporativa importam? -> NestJS
│  └─ Time quer controle manual? -> Express/Fastify + Clean Architecture
│
├─ API com schema bem definido + throughput alto
│  └─ -> Fastify
│
├─ Edge worker / serverless multi-runtime
│  └─ -> Hono
│
└─ Migração de legacy
   ├─ Express legacy saudável -> modernizar Express
   └─ Framework abandonado -> avaliar Fastify ou NestJS
```

## Tabela comparativa

| Atributo | Express | NestJS | Fastify | Hono |
| --- | --- | --- | --- | --- |
| Modelo | Middleware-based | Opinionated, DI | Schema-first | Edge-first |
| DI built-in | Não | Sim | Não | Não |
| Validation | Manual/zod/joi | `ValidationPipe` ou zod | JSON Schema nativo | zod via lib |
| Performance | Baseline | Adapter-dependent | Baixo overhead | Edge-optimized |
| Maturidade | Alta | Alta | Alta | Crescente |
| Ecossistema | Maior | Médio/Nest-specific | Médio | Menor, crescendo |
| Learning curve | Baixa | Alta | Média | Baixa |
| Use case | Glue, protótipo, microsserviço | Enterprise | APIs throughput-focused | Edge/serverless |

## Top armadilhas

1. Express 4 sem `asyncHandler`: erro async não capturado.
2. Express error middleware com 3 args: precisa de `(err, req, res, next)`.
3. Mutar `req` sem contrato: ordem de middleware vira bug invisível.
4. NestJS `Scope.REQUEST` sem necessidade: custo propaga.
5. NestJS circular import resolvido com `forwardRef()` sem refatorar design.
6. Fastify schema sem `additionalProperties: false`.
7. Fastify plugin encapsulado quando deveria expor decorator ao pai.
8. Hono assumindo APIs Node em edge runtime.
9. Hono middleware sem `await next()`.
10. Stack trace em produção.
11. DI container em app pequeno sem necessidade.
12. Clean Architecture em CRUD simples.
13. Schema só para body, ignorando query/params/headers.
14. Misturar zod e `class-validator` sem convenção.

## Playbooks rápidos

### Projeto novo: API interna simples

Escolha padrão: Express ou Fastify.

- Use Express se o time já domina e o contrato é simples.
- Use Fastify se schemas e OpenAPI serão parte do fluxo desde o início.
- Evite NestJS se a justificativa for só "pode crescer".
- Defina desde o dia 1: error handler, validation, request ID e estrutura por feature.

```text
Express/Fastify + zod + Problem Details + composition root simples
```

### Projeto novo: domínio enterprise

Escolha padrão: NestJS ou Clean Architecture manual.

- Use NestJS se convenção, DI e módulos reduzem atrito do time.
- Use Express/Fastify + Clean se o time prefere controle explícito.
- Evite controller gordo.
- Separe ports/adapters antes de integrar banco e provedores externos.

```text
Controller -> Use Case -> Port -> Adapter
```

### Edge/serverless multi-runtime

Escolha padrão: Hono.

- Confirme runtime alvo antes de escolher libs.
- Evite APIs Node-only.
- Pense em bindings e storage do provedor.
- Teste cold start, limites de CPU e observability.

```text
Hono + Web APIs + bindings do runtime + schema validation
```

### Legacy Express

Não migre por reflexo.

- Primeiro atualize error handling.
- Depois centralize validation.
- Em seguida organize routers por feature.
- Só então avalie Fastify/NestJS se ainda houver dor real.

```text
modernizar antes de migrar
```

## Checklist de revisão de arquitetura

- O framework foi escolhido por deploy, domínio, contrato e time?
- Há error handling global com Problem Details?
- Inputs externos são validados com schema?
- Cross-cutting concerns estão na pipeline, não nos controllers?
- O app tem composition root ou DI container claro?
- Clean Architecture foi aplicada onde há domínio, não por ritual?
- Edge apps não dependem de APIs Node-only?
- Performance claims têm benchmark do caso real?
- Rotas públicas, health e metrics foram consideradas na auth?
- Observability mínima existe: request ID, logs, status, latência?

## Flashcards mentais para entrevista

**Express:** liberdade máxima, responsabilidade máxima.
**NestJS:** convenção e DI para complexidade organizacional.
**Fastify:** contrato e performance via schema.
**Hono:** deploy edge/multi-runtime via Web Standards.
**Middleware:** pipeline de cross-cutting concerns.
**Problem Details:** erro como contrato.
**Validation:** toda entrada externa é `unknown`.
**Clean:** dependências apontam para dentro.
**DI:** explícito primeiro; container quando wiring/lifecycle justificam.

## Perguntas que diferenciam senior

1. Qual é o deploy target e quais APIs ele suporta?
2. Qual parte do sistema tem regra de domínio de verdade?
3. O gargalo provável é framework overhead, banco, rede ou CPU?
4. O time precisa mais de liberdade local ou convenção compartilhada?
5. O contrato HTTP precisa gerar documentação e clients?
6. Como erros serão parseados por clientes e logs?
7. Como auth, validation e logging entram sem poluir controller?
8. O framework ajuda ou esconde a arquitetura?
9. O código pode ser testado sem subir servidor real?
10. O que aconteceria se trocássemos banco/provedor/framework?

## Vocabulário PT->EN

| PT | EN |
| --- | --- |
| middleware | middleware |
| middleware de erro | error middleware |
| decorador | decorator |
| injeção de dependência | dependency injection |
| provedor | provider |
| módulo | module |
| controlador | controller |
| escopo | scope |
| guarda | guard |
| interceptor | interceptor |
| pipe | pipe |
| filtro | filter |
| ciclo de vida | lifecycle |
| orientado por schema | schema-first |
| inferência de tipo | type inference |
| encapsulamento de plugin | plugin encapsulation |
| runtime de borda | edge runtime |
| nativo da Fetch API | Fetch API native |
| modelo cebola | onion model |
| taxonomia de erros | error taxonomy |
| raiz de composição | composition root |
| portas e adaptadores | ports and adapters |
| arquitetura hexagonal | hexagonal architecture |
| inversão de dependência | dependency inversion |

## Próximos galhos

- Observability: logging estruturado, métricas, tracing, profiling e diagnóstico de frameworks em produção.
- Segurança: Helmet, CORS, rate limiting, CSRF, input sanitization e hardening por framework.
- Base técnica: [[03-Dominios/Node/Runtime e Event Loop/index]], [[03-Dominios/Node/Paralelismo/index]] e [[03-Dominios/Node/Streams/index]].

## Revisão em 60 segundos

Se o entrevistador perguntar "qual framework Node você escolheria?", não comece pelo nome do framework. Comece pelo contexto:

```text
I would start from the problem shape:
deploy target, domain complexity, team size, API contract,
and operational constraints. Then I would map that to the framework.
```

Depois aplique:

- **Deploy edge?** Hono.
- **Contrato/schema/throughput?** Fastify.
- **Enterprise/DI/time grande?** NestJS.
- **Simplicidade/ecossistema/glue?** Express.
- **Domínio rico?** Clean Architecture independente do framework.
- **App pequeno?** DI manual antes de container.

## Simulações de entrevista

### "We need a high-throughput public REST API with strict contracts"

Resposta forte:

```text
I would consider Fastify first because the API contract is central.
Its route-level JSON Schemas give validation and response serialization,
and they can feed OpenAPI. I would still benchmark the real workload,
because database and network calls may dominate framework overhead.
```

### "We have a large team building a modular enterprise backend"

Resposta forte:

```text
NestJS is a reasonable default because modules, providers, guards,
pipes, interceptors, and DI give the team a shared architecture.
I would still keep domain logic outside controllers and avoid leaking
ORM decorators into domain entities.
```

### "We want to run the same API on Cloudflare Workers and Node"

Resposta forte:

```text
I would look at Hono because it is based on Web Standards and the Fetch API.
The main review item would be runtime compatibility: no hidden fs/net usage,
provider-specific bindings isolated, and observability tested in the edge runtime.
```

### "We already have Express legacy"

Resposta forte:

```text
I would not migrate by reflex. First I would modernize error handling,
validation, route organization, TypeScript types, and tests. If the remaining
pain is structure or schema-first contract, then I would evaluate NestJS or Fastify.
```

## Rubrica pessoal de decisão

| Pergunta | Puxa para |
| --- | --- |
| Deploy edge/multi-runtime? | Hono |
| Contrato HTTP rigoroso? | Fastify |
| Time grande e domínio modular? | NestJS |
| Glue code e simplicidade? | Express |
| Domínio rico e longa vida? | Clean Architecture |
| Dependências rasas? | DI manual |
| Lifecycle complexo? | Container |

Essa tabela não substitui julgamento; ela evita começar pelo gosto pessoal.

## Em entrevista

"I choose a Node framework by matching the problem shape. Express is simple and ubiquitous, Fastify is schema-first and low-overhead, NestJS is the structured enterprise choice with dependency injection, and Hono is the edge-first multi-runtime option. I would not rank them globally; I would choose based on deploy target, API contract, team size, and domain complexity."

Vocabulário-chave:

- decision tree -> árvore de decisão
- trade-off -> troca/custo-benefício
- problem shape -> formato do problema
- deploy target -> alvo de deploy
- framework fit -> encaixe do framework

## Veja também

- [[03-Dominios/Node/Frameworks e arquitetura/index]]
- [[01 - Os 4 frameworks - Express, NestJS, Fastify, Hono]]
- [[02 - Express idiomático]]
- [[03 - NestJS - fundamentos]]
- [[04 - NestJS - guards, interceptors, pipes, filters]]
- [[05 - Fastify - schema-first, plugins, performance]]
- [[06 - Hono e edge runtimes]]
- [[07 - Middleware pipeline]]
- [[08 - Error handling estruturado]]
- [[09 - Validation com schema]]
- [[10 - Clean Architecture em Node]]
- [[11 - DI - manual vs container]]
- [[Node.js]]
- [[03-Dominios/Node/Runtime e Event Loop/index]]
- [[03-Dominios/Node/Paralelismo/index]]
- [[03-Dominios/Node/Streams/index]]
