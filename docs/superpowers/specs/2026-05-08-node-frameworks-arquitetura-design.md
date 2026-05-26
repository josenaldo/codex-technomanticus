---
title: "Spec — Sub-trilha Frameworks e arquitetura (Galho 4)"
date: 2026-05-08
author: Josenaldo
status: draft
type: spec
publish: false
---

# Spec — Sub-trilha "Frameworks e arquitetura" (Galho 4)

## 1. Contexto e motivação

Esta é a **quarta sub-trilha** (galho 4) do roadmap descrito em `2026-05-07-node-roadmap-design.md`. Pressupõe leitura desse roadmap — a metáfora tronco/galhos, os padrões editoriais comuns, e a política de poda do `Node.js.md` monolítico não são repetidos aqui.

Em 2026, escolher framework Node não é mais "Express ou NestJS?" — há **4 frameworks principais** com use cases distintos:

- **Express** — middleware-based, ubíquo (~70% dos projetos Node), v5 trouxe async support nativo
- **NestJS** — opinativo, DI + decorators (estilo Spring Boot), default em apps enterprise
- **Fastify** — performance-first, schema-driven, 2-3× mais rápido que Express em benchmarks típicos
- **Hono** — ultralight, edge-first (Cloudflare Workers, Deno Deploy, Bun, Node), Fetch API native

E não é só sobre framework — é sobre os **patterns transversais** que os frameworks abstraem: middleware pipeline, error handling estruturado (Problem Details RFC 7807), schema-driven validation. O senior decide framework justificando trade-offs e sabe **escrever código idiomático em cada um**.

Há também a camada de **arquitetura**: Clean Architecture / Hexagonal em Node, DI manual vs framework-driven. Em apps grandes, a escolha do framework é menos importante que a disciplina arquitetural — mas saber quando NestJS é o caminho certo (DI built-in justifica) e quando é overkill (app pequeno, manual DI basta) é decisão de senior.

A sub-trilha existe para dar ao leitor:

1. **Visão comparativa** dos 4 frameworks principais com decision tree pragmática
2. **Domínio idiomático** de cada um (Express+NestJS em depth; Fastify+Hono em breadth)
3. **Patterns transversais** (middleware, error handling, validation) que sobrevivem a qualquer framework
4. **Disciplina arquitetural** (Clean Architecture, DI) aplicada a Node
5. **Vocabulário em inglês** para entrevista internacional

## 2. Objetivo

Produzir **12 notas atômicas + 1 MOC** (13 arquivos) em `03-Dominios/Node/Frameworks e arquitetura/`, todas `publish: true`, em PT-BR, cobrindo os 4 frameworks principais, patterns transversais, Clean Architecture, e DI.

A trilha precisa ser:

- **Atômica** — cada nota linkável e citável separadamente
- **Híbrida em camadas** — TL;DR + corpo técnico, no padrão do roadmap
- **Sem dogma framework-religioso** — apresenta cada framework com seus trade-offs; decision tree pragmática, sem campeão pré-definido
- **Idiomática 2026** — Node 22 LTS / 24, Express 5, NestJS 10+, Fastify 5, Hono 4+
- **Orientada a entrevistas internacionais** — cada nota tem "Em entrevista" com frase pronta em inglês + vocabulário; rota alternativa "entrevista" no MOC

## 3. Escopo

### Em escopo

- 13 arquivos markdown em `03-Dominios/Node/Frameworks e arquitetura/`
- Todos com `publish: true`
- Idioma: PT-BR; termos técnicos em inglês mantidos (middleware, decorator, dependency injection, etc.)
- Wikilinks densos para `[[Node.js]]` (tronco), `[[Runtime e Event Loop]]` (galho 1), `[[Streams]]` (galho 3 — frameworks abstraem multipart/streaming)
- Pesquisa baseada em fontes primárias (docs oficiais dos 4 frameworks, RFC 7807, zod docs)
- Tasks de poda do tronco executadas ao fechar o galho

### Fora de escopo

- **Frameworks legacy não-cobertos** — Koa (relevante mas pequena fatia em 2026), Hapi (decadência), Sails (declínio). Express/NestJS/Fastify/Hono cobrem >90% do uso atual
- **Frontend frameworks** — React, Next.js, etc. (irrelevante; outros galhos)
- **GraphQL frameworks** (Apollo, Yoga, Mercurius) — caso específico, fora do escopo do galho
- **gRPC frameworks** (`@grpc/grpc-js`, NestJS gRPC microservices) — caso específico
- **Observability dos frameworks** (logging, métricas) — galho 5 (Observability) cobre isso
- **Segurança específica de framework** (Helmet, CORS, CSRF) — galho 6 (Segurança)
- **Comparação Node vs Bun/Deno na camada de framework** — menções pontuais; comparação detalhada é fora
- **Migração entre frameworks** — caso real mas projeto separado se virar foco

## 4. Audiência e barra de qualidade

**Audiência primária:** dev senior em prep para entrevista internacional. Já trabalhou com Express e provavelmente NestJS, mas não consegue **comparar fluentemente** os 4 frameworks ou justificar escolha de Clean Architecture vs abordagem mais leve.

**Audiência secundária:** o mesmo dev decidindo arquitetura/framework para projeto novo, ou avaliando migração.

**Barra de qualidade:** ao terminar a sub-trilha, o leitor deve **compreender ao nível exigido de um senior** — decidir, justificar, reconhecer patterns e armadilhas em code review. Concretamente:

1. Decidir, em <30 segundos, qual framework usar pra um projeto concreto descrito (microsserviço I/O-bound, app enterprise, edge worker, etc.)
2. Explicar em inglês os trade-offs entre Express, NestJS, Fastify, Hono — não como ranking, mas como matching problema → ferramenta
3. Reconhecer middleware pipeline em qualquer um dos 4 frameworks e identificar onde colocar uma cross-cutting concern
4. Implementar mentalmente error handling estruturado seguindo Problem Details (RFC 7807) em pelo menos 2 frameworks
5. Identificar validation com schema (zod, Fastify schema, NestJS pipes) e justificar por que schema-first ganha de validação manual ad-hoc
6. Diferenciar guard, interceptor, pipe e filter em NestJS, e saber quando usar cada um
7. Argumentar quando NestJS é overkill (app pequeno, time pequeno) e quando é o caminho certo (enterprise, time grande, DI complexa)
8. Reconhecer Clean Architecture / Hexagonal em codebase Node e identificar layer violations
9. Citar pelo menos 5 armadilhas operacionais ao revisar código (Express async sem wrapper, mutating `req` em middleware, NestJS provider scope wrong, etc.)
10. Avaliar performance trade-offs entre frameworks usando ordens de magnitude (não números absolutos que envelhecem)

## 5. Estrutura da sub-trilha (13 arquivos)

### MOC

| # | Arquivo | Propósito |
|---|---|---|
| — | `Frameworks e arquitetura.md` | MOC do galho. Trilha sequencial 01→12 + 5 rotas alternativas. Dataview. Linka pro MOC central, tronco, galhos 1 e 3. |

### Bloco A — Visão geral (1 nota)

| # | Arquivo | Propósito | Conteúdo-chave |
|---|---|---|---|
| 01 | `01 - Os 4 frameworks - Express, NestJS, Fastify, Hono.md` | Visão comparativa + when each | Tabela rica: framework · estilo · use case · maturidade · trade-offs. Express (middleware-based, ubíquo, v5 com async nativo). NestJS (opinativo, DI + decorators, comparison com Spring Boot). Fastify (performance, schema-first, plugins). Hono (edge-first, ultralight, Fetch API native). Decision tree preliminar. Apontador pras notas detalhadas (02-06). |

### Bloco B — Frameworks principais (4 notas)

| # | Arquivo | Propósito | Conteúdo-chave |
|---|---|---|---|
| 02 | `02 - Express idiomático.md` | Express moderno, comum em entrevistas | Middleware pipeline + ordem (`app.use`, `app.METHOD`). Async wrapper — Express 4 não captura `Promise.reject` em handler async; Express 5 (estável em 2024+) captura. Wrapper pattern (`asyncHandler`) ainda comum. Error middleware com signature `(err, req, res, next)` — diferente de regular middleware. req/res/next semantics. Mounting routes (`app.use('/api/v1', router)`). Typing com `@types/express` + extensions. Quando Express é a escolha certa. |
| 03 | `03 - NestJS - fundamentos.md` | DI, módulos, controllers, providers | `@Injectable()`, `@Module()`, `@Controller()` decorators. Provider scope (singleton — default; `Scope.REQUEST`; `Scope.TRANSIENT`). Module imports/exports. DI container que resolve dependências automaticamente via constructor injection. Comparação com Spring Boot pra leitor com background Java. Decoradores customizados. Quando NestJS é a escolha certa (apps enterprise, time grande, DI complexa). |
| 04 | `04 - NestJS - guards, interceptors, pipes, filters.md` | Patterns avançados de NestJS | Request lifecycle: middleware → guard → interceptor (before) → pipe → handler → interceptor (after) → exception filter. **Guards** (`@UseGuards`, `CanActivate`) — autenticação/autorização. **Pipes** (`@UsePipes`, `ValidationPipe`, `ParseIntPipe`) — validação e transformação. **Interceptors** (`@UseInterceptors`, `NestInterceptor`) — cross-cutting (logging, timeout, transform de response, cache). **Exception filters** (`@UseFilters`) — captura erros e formata response (Problem Details). Como compõem em controllers e globalmente. |
| 05 | `05 - Fastify - schema-first, plugins, performance.md` | Performance e validation declarativa | Schema JSON em route (request/response validation + serialization automática via fast-json-stringify). Plugin system (`fastify-plugin`, encapsulation por default). Reply object diferente de Express (`reply.send()` vs `res.send()`). Async handlers nativos. Performance ~2-3× Express em benchmarks típicos (ordem de magnitude, não número absoluto). Quando Fastify é a escolha certa (APIs com schema bem definido, throughput alto). |

### Bloco C — Edge runtimes (1 nota)

| # | Arquivo | Propósito | Conteúdo-chave |
|---|---|---|---|
| 06 | `06 - Hono e edge runtimes.md` | Frameworks pra edge | Hono (ultralight, multi-runtime: Cloudflare Workers, Deno Deploy, Bun, Node, AWS Lambda). API minimalista (Fetch API native — `Request`/`Response` ao invés de `req`/`res`). Constraints de edge: sem `fs`, sem TCP custom, limites de tempo (~50ms-30s) e memória (~128MB-1GB). Tipos de deploy: edge (CF Workers), serverless (Lambda), regional (Deno Deploy). Comparação com Express/Fastify quando deploy é edge-first. Quando Hono ainda **não** é a escolha (app stateful, integração com `fs`/`net`/`http2` específicas). |

### Bloco D — Patterns transversais (3 notas)

| # | Arquivo | Propósito | Conteúdo-chave |
|---|---|---|---|
| 07 | `07 - Middleware pipeline.md` | Como os 4 frameworks lidam | Express (signature `(req, res, next)`, ordem matters, mutate-friendly). Fastify (hooks tipados: `onRequest`, `preHandler`, `preValidation`, `onResponse`, `onError`). NestJS (interceptors com `Observable<T>`-style + middleware function tradicional). Hono (Koa-like onion model com `await next()`). Trade-offs e quando cada modelo cabe. Common patterns: logging, auth, rate limiting, CORS — em cada framework. |
| 08 | `08 - Error handling estruturado.md` | Problem Details (RFC 7807) | `application/problem+json` (type, title, status, detail, instance). Por que padronizar errors (cliente parse uniforme, observability uniforme). Implementação em Express (error middleware), NestJS (exception filter — `HttpException` + custom filter), Fastify (custom errorHandler + schema). Async wrapper em Express (Express 5 nativo, Express 4 manual). Error taxonomy: 4xx (cliente errou) vs 5xx (servidor errou); programmer error vs operational. Stack trace exposure: nunca em prod. |
| 09 | `09 - Validation com schema.md` | zod, joi, Fastify schema, NestJS pipes | **zod** como padrão moderno em 2026 — schema TypeScript-first → tipo + runtime validation; `z.infer<typeof schema>` para tipo. **joi** (mais antigo, ainda comum em código legacy). **Fastify schema** (JSON Schema, integrado ao runtime + serialization). **NestJS** (`ValidationPipe` + `class-validator` + `class-transformer`; também aceita zod via wrapper). Convergência: schema-first em todo o ecossistema. Type inference de schemas. Versionamento de schemas (path-based vs header-based). |

### Bloco E — Arquitetura (2 notas)

| # | Arquivo | Propósito | Conteúdo-chave |
|---|---|---|---|
| 10 | `10 - Clean Architecture em Node.md` | Camadas e ports/adapters | Camadas (entities, use cases, controllers, frameworks/drivers). Hexagonal/ports-adapters mapping para Node. Como aplica em Express+TypeScript (manual, com pastas por camada) vs NestJS (módulos por feature, providers como camadas). Inversão de dependência. Layer violations comuns (entity importando ORM; use case importando framework). Trade-off: pureza arquitetural vs custo de manutenção em time pequeno. Pragmatismo: aplicar Clean quando a complexidade do domínio justifica. |
| 11 | `11 - DI - manual vs container.md` | Quando vale framework de DI | DI manual: constructor injection puro (passar dependências no `new MyService(repo, logger)`), factory functions (`createService(deps)`), composition root no startup. Containers: NestJS (built-in, decorator-based), tsyringe (decorator-based), awilix (proxy-based, sem decorators), InversifyJS (decorator-based, mais antigo). Quando container vale: app grande, time grande, lifecycle complexo (request-scoped providers), módulos lazy-loaded. Quando overkill: app pequeno, time pequeno, dependências rasas. Trade-off: complexidade ramp-up vs escalabilidade. |

### Bloco F — Fechamento (1 nota)

| # | Arquivo | Propósito | Conteúdo-chave |
|---|---|---|---|
| 12 | `12 - Decision tree + cheatsheet.md` | Síntese | Decision tree "qual framework pra qual contexto" (microsserviço I/O-bound; app enterprise grande; edge/serverless; CLI tool com web admin; API com schema bem definido). Tabela 4 frameworks × atributos (DI, validation, performance, ecosystem, maturity, learning curve). Top 10 armadilhas (Express async sem wrapper; mutating req em middleware; NestJS provider scope wrong; Fastify schema sem `additionalProperties: false`; Hono assumindo Node APIs em edge; etc.). Vocabulário PT→EN consolidado. Apontador pros próximos galhos (5 observability — métricas; 6 segurança — Helmet, rate limiting, etc.). |

## 6. Padrão estrutural por nota

Toda nota segue o padrão herdado do roadmap:

```markdown
---
title: "<título sem prefixo numérico>"
created: 2026-05-08
updated: 2026-05-08
type: concept
status: seedling
publish: true
tags:
  - node
  - frameworks
  - <conceito-tag específica: express, nestjs, fastify, hono, middleware, error-handling, validation, clean-architecture, di>
aliases:
  - <opcional>
---

# <Título>

> [!abstract] TL;DR
> <2-4 linhas em PT-BR. Conceito + regra prática + por que importa.>

## O que é

## Por que importa

## Como funciona

## Na prática

## Armadilhas

## Em entrevista

## Veja também
```

**Variações permitidas:**

- **Nota 12 (Decision tree + cheatsheet):** estrutura tópica — fluxograma + tabela + lista de armadilhas. Não tem narrativa "Como funciona".
- **MOC (`Frameworks e arquitetura.md`):** estrutura própria — abertura + Comece por aqui + 5 rotas alternativas + dataview. `type: moc`.

**Tamanho típico:** 200-500 linhas. Notas conceituais densas (04 NestJS advanced, 09 Validation) podem ir até 600 quando o tema pedir.

## 7. Rotas alternativas no MOC

### Rota completa
Sequencial 01 → 12. Recomendada na primeira leitura.

### Rota entrevista internacional
01 → 02 → 03 → 04 → 07 → 08 → 12. Foco em "explicar trade-offs entre frameworks pra entrevistador".

### Rota produção (escolhendo framework pra projeto novo)
01 → 05 → 09 → 10 → 12. Foco em "como decido qual usar agora".

### Rota NestJS-first
03 → 04 → 09 → 11. Pra quem vai usar NestJS em projeto enterprise.

### Rota patterns sobre framework
07 → 08 → 09 → 10. Pra quem quer entender padrões transversais aos frameworks.

### Rota edge
01 → 06 → 12. Pra quem está olhando Cloudflare Workers / Deno Deploy / Bun.

## 8. Fontes principais

### Referências canônicas

- [Express docs](https://expressjs.com/)
- [Express 5 release notes](https://expressjs.com/2024/10/15/v5-release.html) (ou equivalente)
- [NestJS docs](https://docs.nestjs.com/)
- [Fastify docs](https://fastify.dev/)
- [Hono docs](https://hono.dev/)
- [Problem Details RFC 7807](https://datatracker.ietf.org/doc/html/rfc7807)
- [zod](https://zod.dev/)
- [joi](https://joi.dev/api/)

### Referências de arquitetura

- [Clean Architecture by Robert Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) — referência canônica
- [tsyringe](https://github.com/microsoft/tsyringe), [awilix](https://github.com/jeffijoe/awilix), [InversifyJS](https://github.com/inversify/InversifyJS) — DI containers

### A buscar conforme necessidade

- TechEmpower benchmarks atuais (ordem de magnitude, não números absolutos)
- Discussões 2026 sobre Hono em produção
- NestJS roadmap (versão atual, breaking changes)
- Posts comparando frameworks em casos reais

## 9. Decisões editoriais

- **Idioma:** PT-BR exclusivo nesta fase
- **Tom:** técnico mas acessível; TL;DR sempre presente
- **Versões assumidas:** Node 22 LTS / 24; Express 5; NestJS 10+; Fastify 5; Hono 4+. Quando uma feature é específica de uma versão, mencionar
- **Frontmatter:** `publish: true`, `status: seedling`, tags `[node, frameworks, <conceito>]`
- **Wikilinks:** densidade alta para `[[Node.js]]` (tronco), `[[Runtime e Event Loop]]` (galho 1), `[[Streams]]` (galho 3 — frameworks abstraem upload streaming, multipart), e entre as 12 notas
- **Code samples:** TypeScript preferencialmente (todos os 4 frameworks têm bom TS support); JS quando exemplo conceitual curto; comentários em PT-BR onde didáticos
- **Inglês:** apenas em "Em entrevista" (frases prontas + vocabulário) e em termos técnicos do ecossistema (middleware, decorator, dependency injection, etc.)
- **Sem dogma framework-religioso:** cada framework apresentado com seus trade-offs explícitos; decision tree pragmática

## 10. Tasks de poda do tronco

Ao fechar o galho, executar no `03-Dominios/JavaScript/Backend/Node.js.md`:

1. Substituir seção **`### Frameworks`** por callout `[!nota]` apontando pra:
   - `[[Frameworks e arquitetura]]` (MOC)
   - `[[01 - Os 4 frameworks - Express, NestJS, Fastify, Hono]]` (visão geral)
   - `[[02 - Express idiomático]]`
   - `[[03 - NestJS - fundamentos]]`
   - `[[05 - Fastify - schema-first, plugins, performance]]`
   - `[[06 - Hono e edge runtimes]]`
2. Substituir seção **`### Error Handling`** por callout apontando pra `[[08 - Error handling estruturado]]`
3. Adicionar `[[Frameworks e arquitetura]]` no `## Veja também` do tronco como **quarto bullet** (após `[[Runtime e Event Loop]]`, `[[Paralelismo]]`, `[[Streams]]`)
4. Atualizar `updated:` no frontmatter do tronco
5. Atualizar `03-Dominios/Node/index.md` (MOC central) adicionando `[[Frameworks e arquitetura]]` na seção "Galhos da trilha Node Senior"

Confirmar nomes exatos das seções no Task 0 do plano (podem ter variações pós-podas anteriores).

## 11. Riscos e mitigações

| Risco | Mitigação |
|---|---|
| Frameworks evoluem rápido (versões, breaking changes) | Versões assumidas declaradas no frontmatter; foco em **modelos** (middleware-based, DI, schema-first, edge-first) que sobrevivem versões |
| NestJS = 2 notas (03 fundamentos + 04 advanced) — risco de redundância | 03 cobre o que NestJS é (DI, módulos, controllers); 04 cobre **lifecycle hooks** (guards, interceptors, pipes, filters). Linha clara |
| Bias entre frameworks (religious wars) | Padrão "sem dogma" estabelecido em galhos anteriores: cada framework com trade-offs explícitos, sem campeão pré-definido. Decision tree é **matching**, não ranking |
| Performance benchmarks envelhecem | Mencionar ordens de magnitude ("Fastify ~2-3× Express em benchmarks típicos"), não números absolutos. Apontar TechEmpower como referência viva |
| Hono pode não ser canônico em 2 anos | Nota 06 declara "estado de 2026" e foca no **modelo** (edge runtimes, Fetch API native, constraints) que é mais durável que o framework específico |
| Clean Architecture virar evangelismo arquitetural | Nota 10 inclui callout explícito: "aplicar Clean quando a complexidade do domínio justifica". Trade-off pragmático declarado |
| Overlap entre middleware (07) e NestJS interceptors (04) | 04 cobre apenas dentro de NestJS; 07 cobre comparação cross-framework. Linha clara |

## 12. Critérios de aceitação

A sub-trilha está completa quando:

1. Todos os 13 arquivos existem em `03-Dominios/Node/Frameworks e arquitetura/`
2. Todos têm frontmatter completo com `publish: true`
3. MOC `Frameworks e arquitetura.md` tem 12 notas linkadas + 5 rotas alternativas + dataview
4. Cada nota satisfaz a rubrica padrão:
   - TL;DR em callout `[!abstract]`
   - 2+ wikilinks pra outras notas do galho + 1+ wikilink pra `[[Node.js]]` (tronco) ou galho anterior
   - 3+ code samples em TS ou JS (notas 01, 12 podem ter menos se forem síntese)
   - Seção "Em entrevista" com 1+ frase pronta em inglês + vocabulário-chave
   - Seção "Armadilhas" com 2+ armadilhas concretas
   - Frontmatter completo (`publish: true`, `status: seedling`, tags `[node, frameworks, <conceito>]`)
   - PT-BR natural; termos técnicos em inglês mantidos
   - **Zero atribuição de experiência pessoal ao autor**
5. Tasks de poda do tronco (seção 10) executadas
6. MOC central `03-Dominios/Node/index.md` atualizado (4 galhos listados)
7. Quartz publica corretamente
8. Pelo menos 4 notas têm code sample testável em script standalone (ex: Express handler com error wrapper, Fastify schema route, NestJS module + controller, zod schema com infer)

## 13. Plano de execução

O plano detalhado vai em `docs/superpowers/plans/2026-05-08-node-frameworks-arquitetura-execution.md` (gerado pela skill `superpowers:writing-plans` após aprovação deste spec).

A ordem de execução recomendada:

1. MOC (esqueleto) + 01 (visão geral)
2. 02 + 03 + 04 + 05 (frameworks principais)
3. 06 (Hono / edge)
4. 07 + 08 + 09 (patterns transversais)
5. 10 + 11 (arquitetura)
6. 12 (fechamento, agrega)
7. Pass final no MOC
8. Tasks de poda do tronco (1 task atômica final)
9. Atualização do MOC central

## 14. Documentos relacionados

- `2026-05-07-node-roadmap-design.md` — roadmap macro dos 6 galhos (este spec é sub-trilha #4)
- `2026-05-07-node-runtime-event-loop-design.md` — galho 1
- `2026-05-07-node-paralelismo-design.md` — galho 2
- `2026-05-08-node-streams-design.md` — galho 3
- Plano de execução do galho 4 (criado depois): `2026-05-08-node-frameworks-arquitetura-execution.md`
- Tronco a ser podado: `03-Dominios/JavaScript/Backend/Node.js.md`
- MOC central: `03-Dominios/Node/index.md`
- Galhos anteriores fechados: `03-Dominios/Node/Runtime e Event Loop/`, `03-Dominios/Node/Paralelismo/`, `03-Dominios/Node/Streams/`
