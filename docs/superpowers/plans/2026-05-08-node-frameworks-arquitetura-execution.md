---
title: "Plano — Execução da Sub-trilha Frameworks e arquitetura (Galho 4)"
date: 2026-05-08
status: ready
type: plan
publish: false
---

# Sub-trilha Frameworks e arquitetura — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produzir 12 notas atômicas + 1 MOC em `03-Dominios/Node/Frameworks e arquitetura/`, em PT-BR, todas `publish: true`, cobrindo os 4 frameworks principais (Express, NestJS, Fastify, Hono), patterns transversais (middleware, error handling Problem Details, schema validation), Clean Architecture em Node, e DI manual vs container — para um dev senior em prep para entrevista internacional. Ao final, podar 2 seções do tronco `JavaScript/Backend/Node.js.md` e atualizar o MOC central.

**Architecture:** Sub-trilha sequencial em 6 blocos (Visão geral → Frameworks principais → Edge runtimes → Patterns transversais → Arquitetura → Fechamento) + 1 MOC com 5 rotas alternativas. Pressupõe galho 1 (Runtime e Event Loop) como base. Cada nota é atômica, segue estrutura híbrida (TL;DR + corpo técnico), com code samples em TypeScript moderno (Node 22 LTS / 24, Express 5, NestJS 10+, Fastify 5, Hono 4+), seção "Em entrevista" pra preparação internacional. Padrão "sem dogma" — cada framework apresentado com trade-offs explícitos.

**Tech Stack:** Markdown + Obsidian Flavored Markdown (wikilinks, callouts, dataview), Quartz para publicação no site público (josenaldo.github.io). Sem código a executar como sistema — code samples didáticos validáveis quando útil. Bibliografia âncora: docs oficiais dos 4 frameworks, RFC 7807, zod docs.

---

## ⚠️ Restrição absoluta — fabricação

A memória [Nunca inventar dados sobre o usuário](/home/josenaldo/.claude/projects/-home-josenaldo-repos-personal-codex-technomanticus/memory/feedback_no_fabrication.md) é regra inegociável. **Nenhuma nota pode atribuir ao autor experiências profissionais, projetos, clientes, métricas ou casos não-vividos.**

A seção "Na prática" de cada nota usa:

- "Padrão observado em libs do ecossistema (Express middleware comuns, NestJS apps enterprise)"
- "Caso típico em microsserviços I/O-bound"
- "Armadilha comum reportada na comunidade"
- Citações com fonte verificável (docs oficiais, talks identificadas, repos públicos)
- Hipotéticos explícitos ("Imagine uma API que recebe webhooks...")

Quando faltar contexto factual, **PERGUNTAR antes de escrever** — nunca preencher com plausibilidade.

---

## File Structure

13 arquivos novos em `03-Dominios/Node/Frameworks e arquitetura/`:

```
03-Dominios/Node/Frameworks e arquitetura/
├── Frameworks e arquitetura.md                                       # MOC (Task 1)
├── 01 - Os 4 frameworks - Express, NestJS, Fastify, Hono.md          # Task 2
├── 02 - Express idiomático.md                                        # Task 3
├── 03 - NestJS - fundamentos.md                                      # Task 4
├── 04 - NestJS - guards, interceptors, pipes, filters.md             # Task 5
├── 05 - Fastify - schema-first, plugins, performance.md              # Task 6
├── 06 - Hono e edge runtimes.md                                      # Task 7
├── 07 - Middleware pipeline.md                                       # Task 8
├── 08 - Error handling estruturado.md                                # Task 9
├── 09 - Validation com schema.md                                     # Task 10
├── 10 - Clean Architecture em Node.md                                # Task 11
├── 11 - DI - manual vs container.md                                  # Task 12
└── 12 - Decision tree + cheatsheet.md                                # Task 13
```

**Final integration (Task 14, 15, 16):**
- Pass final no MOC inserindo intro + verificações
- Poda do tronco `03-Dominios/JavaScript/Backend/Node.js.md` (2 seções)
- Atualização do MOC central + verificação Quartz

---

## Template padrão

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
  - <tag específica: express, nestjs, fastify, hono, middleware, error-handling, validation, clean-architecture, di>
aliases:
  - <opcional>
---

# <Título>

> [!abstract] TL;DR
> <2-4 linhas em PT-BR direto.>

## O que é

## Por que importa

## Como funciona

## Na prática

## Armadilhas

## Em entrevista

## Veja também
```

### Variações permitidas

- **Nota 12 (Decision tree + cheatsheet):** estrutura tópica — fluxograma + tabela + lista de armadilhas.
- **MOC (`Frameworks e arquitetura.md`):** estrutura própria + 5 rotas alternativas + dataview. `type: moc`.

### Critérios de qualidade (rubrica por nota)

- [ ] TL;DR em callout `[!abstract]`, 2-4 linhas
- [ ] 2+ wikilinks pra outras notas do galho + 1+ wikilink pra `[[Node.js]]` (tronco) ou galho anterior
- [ ] 3+ code samples em TS ou JS (notas conceituais 01, 12 podem ter menos)
- [ ] Seção "Em entrevista" com 1+ frase pronta em inglês + vocabulário-chave (mínimo 4 termos PT→EN)
- [ ] Seção "Armadilhas" com 2+ armadilhas concretas
- [ ] Frontmatter completo (`publish: true`, `status: seedling`, tags `[node, frameworks, <específica>]`)
- [ ] Versões assumidas declaradas (Express 5, NestJS 10+, Fastify 5, Hono 4+)
- [ ] PT-BR natural; termos técnicos em inglês mantidos
- [ ] **Zero atribuição de experiência pessoal ao autor**
- [ ] Nenhuma alegação técnica não-trivial sem fonte ou code sample

---

## Bibliografia centralizada

### Referências canônicas

- **Express:** `https://expressjs.com/`
- **NestJS:** `https://docs.nestjs.com/`
- **Fastify:** `https://fastify.dev/`
- **Hono:** `https://hono.dev/`
- **Problem Details RFC 7807:** `https://datatracker.ietf.org/doc/html/rfc7807`
- **zod:** `https://zod.dev/`
- **joi:** `https://joi.dev/api/`

### Referências de arquitetura

- **Clean Architecture (Robert Martin):** `https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html`
- **tsyringe:** `https://github.com/microsoft/tsyringe`
- **awilix:** `https://github.com/jeffijoe/awilix`
- **InversifyJS:** `https://github.com/inversify/InversifyJS`

### Notas no vault

- `03-Dominios/JavaScript/Backend/Node.js.md` — tronco (2 seções a podar)
- `03-Dominios/Node/index.md` — MOC central
- `03-Dominios/Node/Runtime e Event Loop/` — galho 1 (pré-requisito)
- `03-Dominios/Node/Streams/` — galho 3 (frameworks abstraem multipart/streaming)

### A buscar conforme necessidade

- TechEmpower benchmarks atuais (ordem de magnitude, não números absolutos)
- Discussões 2026 sobre Hono em produção
- Versão atual do NestJS roadmap

---

## Task 0: Pré-flight

**Files:**
- Create: `03-Dominios/Node/Frameworks e arquitetura/` (diretório)

- [ ] **Step 1: Criar o diretório**

```bash
mkdir -p "03-Dominios/Node/Frameworks e arquitetura"
ls -la "03-Dominios/Node/Frameworks e arquitetura"
```

Esperado: diretório vazio.

- [ ] **Step 2: Confirmar memórias críticas**

```bash
cat /home/josenaldo/.claude/projects/-home-josenaldo-repos-personal-codex-technomanticus/memory/MEMORY.md | grep -iE "fabrica|invent|tronco|galho"
```

Esperado: linhas referenciando `feedback_no_fabrication.md` e `project_tronco_galhos_pattern.md`. Se faltar `no_fabrication`, BLOCKED.

- [ ] **Step 3: Sanity check do tronco — 2 seções a podar**

```bash
grep -nE "^### Frameworks|^### Error Handling" "03-Dominios/JavaScript/Backend/Node.js.md"
```

Esperado: 2 matches. Anotar números de linha exatos. Confirmar que cada seção termina antes da próxima `###` ou `##`. Se nomes divergirem, anotar exatamente.

- [ ] **Step 4: Confirmar wikilinks dos galhos anteriores resolvem**

```bash
ls "03-Dominios/Node/Runtime e Event Loop/" | wc -l   # esperado 13
ls "03-Dominios/Node/Paralelismo/" | wc -l            # esperado 13
ls "03-Dominios/Node/Streams/" | wc -l                # esperado 13
ls "03-Dominios/Node/index.md"
ls "03-Dominios/JavaScript/Backend/Node.js.md"
```

- [ ] **Step 5: Sanity check das fontes-âncora**

WebFetch em paralelo:

```
https://expressjs.com/
https://docs.nestjs.com/
https://fastify.dev/
https://hono.dev/
```

Confirmar acesso. Se alguma falhar, registrar e usar fontes alternativas (GitHub repos).

- [ ] **Step 6: Commit**

```bash
git add -A
git commit -m "feat(node-frameworks): create directory for Frameworks e arquitetura sub-trail"
```

(Sem `Co-Authored-By` — regra do usuário.)

---

## Task 1: MOC esqueleto

**Files:**
- Create: `03-Dominios/Node/Frameworks e arquitetura/Frameworks e arquitetura.md`

- [ ] **Step 1: Criar MOC**

Criar com este conteúdo (substituir `\`\`\`` por triple backticks reais — escapes apenas neste plano):

```markdown
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
> Galho 4 da trilha Node Senior. Cobre os 4 frameworks principais (Express, NestJS, Fastify, Hono) com trade-offs explícitos, patterns transversais (middleware, error handling Problem Details, schema validation), Clean Architecture em Node e DI manual vs container. Pré-requisito: galho 1 (Runtime e Event Loop). Sem dogma framework-religioso — decision tree é matching, não ranking.

## Sobre este galho

(introdução curta — preencher na Task 14)

## Comece por aqui — trilha completa (12 notas)

### Bloco A — Visão geral

1. [[01 - Os 4 frameworks - Express, NestJS, Fastify, Hono]]

### Bloco B — Frameworks principais

2. [[02 - Express idiomático]]
3. [[03 - NestJS - fundamentos]]
4. [[04 - NestJS - guards, interceptors, pipes, filters]]
5. [[05 - Fastify - schema-first, plugins, performance]]

### Bloco C — Edge runtimes

6. [[06 - Hono e edge runtimes]]

### Bloco D — Patterns transversais

7. [[07 - Middleware pipeline]]
8. [[08 - Error handling estruturado]]
9. [[09 - Validation com schema]]

### Bloco E — Arquitetura

10. [[10 - Clean Architecture em Node]]
11. [[11 - DI - manual vs container]]

### Bloco F — Fechamento

12. [[12 - Decision tree + cheatsheet]]

## Rotas alternativas

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

## Todas as notas

\`\`\`dataview
TABLE status, updated
FROM "03-Dominios/Node/Frameworks e arquitetura"
WHERE type = "concept"
SORT file.name ASC
\`\`\`

## Veja também

- [[03-Dominios/Node/index|Node.js (MOC central)]]
- [[Node.js]] — tronco (deep dive panorâmico)
- [[Runtime e Event Loop]] — galho 1 (pré-requisito)
- [[Paralelismo]] — galho 2
- [[Streams]] — galho 3
```

- [ ] **Step 2: Cleanup `.gitkeep`** (se foi criado em Task 0)

```bash
ls "03-Dominios/Node/Frameworks e arquitetura/.gitkeep" 2>/dev/null && git rm "03-Dominios/Node/Frameworks e arquitetura/.gitkeep" || echo "no .gitkeep"
```

- [ ] **Step 3: Verificar**

- `type: moc`, `publish: true`
- 12 notas em 6 blocos (A-F)
- 5 rotas alternativas (entrevista, produção, NestJS-first, patterns, edge)
- Dataview path: `"03-Dominios/Node/Frameworks e arquitetura"`
- Wikilinks pro MOC central, tronco, galhos 1+2+3

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Node/Frameworks e arquitetura/Frameworks e arquitetura.md"
git commit -m "feat(node-frameworks): add MOC skeleton for Frameworks e arquitetura branch"
```

---

## Task 2: Nota 01 — Os 4 frameworks

**Files:**
- Create: `03-Dominios/Node/Frameworks e arquitetura/01 - Os 4 frameworks - Express, NestJS, Fastify, Hono.md`

- [ ] **Step 1: Pesquisa-âncora**

WebFetch em paralelo:

```
https://expressjs.com/
https://docs.nestjs.com/
https://fastify.dev/
https://hono.dev/
```

Capturar: descrição em uma frase de cada, modelo de programação, target use case.

- [ ] **Step 2: Frontmatter**

```yaml
---
title: "Os 4 frameworks: Express, NestJS, Fastify, Hono"
created: 2026-05-08
updated: 2026-05-08
type: concept
status: seedling
publish: true
tags:
  - node
  - frameworks
  - mental-model
  - express
  - nestjs
  - fastify
  - hono
aliases:
  - Visão geral frameworks Node
  - 4 frameworks Node
---
```

- [ ] **Step 3: Escrever (300-450 linhas, PT-BR)**

- **TL;DR**: Em 2026, há 4 frameworks principais em Node — Express (middleware-based, ubíquo), NestJS (opinativo, DI + decorators), Fastify (performance, schema-first), Hono (edge-first, ultralight). Não há "melhor" — há **matching problema → ferramenta**. Decision tree pragmática mais importante que ranking.

- **## O que é**: cada framework definido em 1-2 frases:
  - **Express** — minimalista, baseado em middleware, ubíquo (~70% dos projetos Node), v5 estável com async support nativo
  - **NestJS** — opinativo, decorator-based, DI built-in, estilo Spring Boot, ~10+ versão atual
  - **Fastify** — schema-first, performance-focused, plugin system encapsulated, ~5+ versão atual
  - **Hono** — ultralight, Fetch API native, edge-first (Cloudflare Workers, Deno Deploy, Bun, Node), ~4+ versão atual

- **## Por que importa**: confundir os modelos leva a escolhas erradas. "Vou usar NestJS por estar na moda" em projeto de microsserviço I/O-bound simples = overhead de DI sem benefício. "Vou usar Express porque é o que conheço" em app enterprise grande = sem estrutura, vira espagueti.

- **## Como funciona** — **tabela canônica** (estrela da nota):

  | Framework | Modelo | Use case típico | Maturidade | Trade-offs |
  |---|---|---|---|---|
  | Express | Middleware-based, minimalista | Microsserviços simples, prototipagem, glue code | Maduro (2010+), v5 desde 2024 | Pouca estrutura; precisa montar tudo manual |
  | NestJS | Opinativo, DI, decorators (Spring-like) | Apps enterprise, time grande, domínio complexo | Maduro (2017+), v10+ | Curva de aprendizado; overhead em apps simples |
  | Fastify | Schema-first, performance-focused | APIs com schema bem definido, throughput alto | Maduro (2017+), v5 | Plugin system encapsulated (curva); ecosystem menor que Express |
  | Hono | Ultralight, edge-first, Fetch API | Edge workers, serverless, multi-runtime | Recente (2022+), v4+ | Ecosystem menor; constraints de edge limitam |

  Code sample minimal de cada (8-10 linhas) — handler `GET /hello` retornando JSON.

- **## Na prática**: decision tree preliminar:
  - "Microsserviço I/O-bound simples, time pequeno" → Express ou Fastify
  - "App enterprise, time grande, DI complexa" → NestJS
  - "API com schema bem definido, throughput alto" → Fastify
  - "Edge worker, serverless, multi-runtime" → Hono
  - Decision tree completa em nota 12

- **## Armadilhas (3+)**:
  1. Escolher framework por hype, não por fit — "todo mundo usa NestJS" não justifica em projeto pequeno
  2. Migrar de framework no meio do projeto — custo alto, raramente justificado
  3. Comparar performance em benchmarks sintéticos sem medir caso real
  4. Achar que NestJS = "Express com decorators" — modelo conceitualmente diferente

- **## Em entrevista**:
  - Frase pronta: "Node has four main frameworks in 2026, each solving different problems. Express is middleware-based and ubiquitous — minimalist, you assemble everything manually. NestJS is opinionated, with built-in dependency injection and decorators, comparable to Spring Boot — the right choice for enterprise apps with complex domains. Fastify is schema-first and performance-focused — about two to three times faster than Express in typical benchmarks. Hono is ultralight and edge-first — designed for Cloudflare Workers, Deno Deploy, Bun, and Node, using the Fetch API natively. The decision is matching, not ranking — pick based on problem shape and team."
  - Vocabulário (5+): middleware-based, opinativo (opinionated), schema-first, edge-first, decision matching.

- **## Veja também**:
  - `[[02 - Express idiomático]]`
  - `[[03 - NestJS - fundamentos]]`
  - `[[05 - Fastify - schema-first, plugins, performance]]`
  - `[[06 - Hono e edge runtimes]]`
  - `[[12 - Decision tree + cheatsheet]]`
  - `[[Node.js]]` (tronco)

- [ ] **Step 4: Verificar rubrica** (standard)

- [ ] **Step 5: Commit**

```bash
git add "03-Dominios/Node/Frameworks e arquitetura/01 - Os 4 frameworks - Express, NestJS, Fastify, Hono.md"
git commit -m "feat(node-frameworks): add note 01 — Os 4 frameworks"
```

---

## Task 3: Nota 02 — Express idiomático

**Files:**
- Create: `03-Dominios/Node/Frameworks e arquitetura/02 - Express idiomático.md`

- [ ] **Step 1: Pesquisa-âncora**

```
WebFetch: https://expressjs.com/en/4x/api.html
WebFetch: https://expressjs.com/en/guide/error-handling.html
```

Capturar: API moderna, async support em v5, error middleware signature.

- [ ] **Step 2: Frontmatter**

```yaml
---
title: "Express idiomático"
created: 2026-05-08
updated: 2026-05-08
type: concept
status: seedling
publish: true
tags:
  - node
  - frameworks
  - express
  - middleware
aliases:
  - Express
  - asyncHandler
  - error middleware
---
```

- [ ] **Step 3: Escrever (350-500 linhas, PT-BR)**

- **TL;DR**: Express é middleware-based, com pipeline ordenado de funções `(req, res, next)`. Express 5 (estável em 2024+) captura `Promise.reject` em handlers async; Express 4 não — wrapper pattern (`asyncHandler`) ainda comum em código legacy. Error middleware tem signature `(err, req, res, next)` — diferente de regular middleware.

- **## O que é**: minimalist HTTP framework, middleware-based, ubíquo.

- **## Por que importa**: ainda dominante em projetos Node; conhecer Express idiomático moderno separa código legacy mantido de código novo bem escrito.

- **## Como funciona** — code samples:
  1. **Setup minimal Express 5:**
     ```typescript
     import express from 'express';
     const app = express();
     app.use(express.json());
     app.get('/hello', (req, res) => res.json({ greeting: 'hello' }));
     app.listen(3000);
     ```
  2. **Async handler (Express 5 nativo):**
     ```typescript
     app.get('/users/:id', async (req, res) => {
       const user = await db.users.findById(req.params.id);
       if (!user) throw new NotFoundError();
       res.json(user);
     });
     ```
  3. **asyncHandler wrapper (Express 4 ou compat):**
     ```typescript
     const asyncHandler = (fn: any) => (req: any, res: any, next: any) =>
       Promise.resolve(fn(req, res, next)).catch(next);
     
     app.get('/users/:id', asyncHandler(async (req, res) => {
       const user = await db.users.findById(req.params.id);
       res.json(user);
     }));
     ```
  4. **Error middleware:**
     ```typescript
     app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
       const status = err instanceof HttpError ? err.status : 500;
       res.status(status).json({
         type: 'about:blank',
         title: err.name,
         status,
         detail: err.message,
       });
     });
     ```
  5. **Routers e mounting:**
     ```typescript
     const userRouter = express.Router();
     userRouter.get('/', listUsers);
     userRouter.get('/:id', getUser);
     app.use('/api/v1/users', userRouter);
     ```

- **## Na prática**: padrões observados:
  - Express + TypeScript + zod = stack comum em 2026
  - `helmet`, `cors`, `compression`, `morgan` — middlewares quase obrigatórios
  - Error middleware **sempre** no final da pipeline
  - `app.use(express.json({ limit: '10mb' }))` — limit explícito (preview de DoS na nota 06 do galho 6)

- **## Armadilhas (3+)**:
  1. Express 4: handler async sem wrapper → erro não capturado
  2. Mutating `req`/`res` em middleware sem documentar — ordem matters
  3. Error middleware com 3 args (`(req, res, next)`) ao invés de 4 (`(err, req, res, next)`) — Express não trata como error handler
  4. `next(err)` esquecido em catch — error não chega ao error middleware
  5. `res.send()` chamado duas vezes (ex: depois de erro) — `Cannot set headers after they are sent`

- **## Em entrevista**:
  - Frase pronta: "Express 5, stable since 2024, brings native async support — promise rejections in async handlers automatically reach the error middleware. In Express 4 you need an `asyncHandler` wrapper that catches and calls `next(err)`. The error middleware has a different signature than regular middleware — four arguments, with `err` first. Mounting routers with `app.use('/api/v1', router)` is the canonical way to organize routes. Helmet, cors, and a body limit are middleware essentials in production."
  - Vocabulário (5+): middleware pipeline, error middleware, async wrapper, router mounting, body limit.

- **## Veja também**:
  - `[[01 - Os 4 frameworks - Express, NestJS, Fastify, Hono]]`
  - `[[07 - Middleware pipeline]]`
  - `[[08 - Error handling estruturado]]`
  - `[[09 - Validation com schema]]`
  - `[[Node.js]]` (tronco)

- [ ] **Step 4: Rubric** (standard)

- [ ] **Step 5: Commit**

```bash
git add "03-Dominios/Node/Frameworks e arquitetura/02 - Express idiomático.md"
git commit -m "feat(node-frameworks): add note 02 — Express idiomático"
```

---

## Task 4: Nota 03 — NestJS fundamentos

**Files:**
- Create: `03-Dominios/Node/Frameworks e arquitetura/03 - NestJS - fundamentos.md`

- [ ] **Step 1: Pesquisa-âncora**

```
WebFetch: https://docs.nestjs.com/first-steps
WebFetch: https://docs.nestjs.com/modules
WebFetch: https://docs.nestjs.com/providers
```

- [ ] **Step 2: Frontmatter**

```yaml
---
title: "NestJS: fundamentos"
created: 2026-05-08
updated: 2026-05-08
type: concept
status: seedling
publish: true
tags:
  - node
  - frameworks
  - nestjs
  - dependency-injection
  - modules
aliases:
  - NestJS DI
  - NestJS modules
  - "@Injectable"
---
```

- [ ] **Step 3: Escrever (400-500 linhas, PT-BR)**

- **TL;DR**: NestJS é framework opinativo com DI built-in, decorator-based, estilo Spring Boot. Estrutura organizada em **módulos** que declaram providers, controllers e exports. DI container resolve dependências automaticamente via constructor injection. Right choice pra apps enterprise com domínio complexo e time grande.

- **## O que é**: framework opinativo construído sobre Express (ou Fastify, opcional). Decorator-based pra metadata. DI container que ecoa Angular (frontend) e Spring (Java).

- **## Por que importa**: em apps grandes, DI built-in + módulos + lifecycle hooks economizam tempo de scaffolding. Em apps pequenos, é overhead. Saber a fronteira é decisão de senior.

- **## Como funciona** — code samples:
  1. **Module básico:**
     ```typescript
     import { Module } from '@nestjs/common';
     import { UsersController } from './users.controller';
     import { UsersService } from './users.service';
     
     @Module({
       controllers: [UsersController],
       providers: [UsersService],
       exports: [UsersService],
     })
     export class UsersModule {}
     ```
  2. **Provider com `@Injectable`:**
     ```typescript
     import { Injectable } from '@nestjs/common';
     
     @Injectable()
     export class UsersService {
       constructor(private readonly db: DatabaseClient) {}
       async findById(id: string) { return this.db.users.findById(id); }
     }
     ```
  3. **Controller injetando service:**
     ```typescript
     import { Controller, Get, Param } from '@nestjs/common';
     
     @Controller('users')
     export class UsersController {
       constructor(private readonly users: UsersService) {}
       @Get(':id')
       async getUser(@Param('id') id: string) {
         return this.users.findById(id);
       }
     }
     ```
  4. **Provider scope:**
     ```typescript
     @Injectable({ scope: Scope.REQUEST })  // novo a cada request
     export class RequestScopedService {}
     
     @Injectable({ scope: Scope.TRANSIENT })  // novo a cada injection
     export class TransientService {}
     // default = SINGLETON (instância única no app inteiro)
     ```
  5. **Module imports/exports:**
     ```typescript
     @Module({
       imports: [DatabaseModule, UsersModule],  // outros módulos
       controllers: [...],
       providers: [...],
       exports: [...],  // o que outros módulos podem injetar
     })
     export class AppModule {}
     ```

- **## Na prática**: padrão observado:
  - 1 módulo por feature (UsersModule, OrdersModule)
  - Shared modules para coisa transversal (DatabaseModule, LoggerModule)
  - SINGLETON é o default e geralmente certo
  - REQUEST scope quando provider precisa de contexto da request (auth user, tracing ID)

- **## Armadilhas (3+)**:
  1. REQUEST scope vira TRANSIENT-style sem entender — toda dep de REQUEST vira REQUEST (escala mal)
  2. Circular imports entre módulos — usar `forwardRef()` (mas é code smell)
  3. Esquecer `exports` no módulo — outro módulo não consegue injetar
  4. Constructor com lógica → roda no startup; preferir `OnModuleInit` lifecycle hook

- **## Em entrevista**:
  - Frase pronta: "NestJS is opinionated and decorator-based, with a built-in dependency injection container similar to Angular's, comparable to Spring Boot for backend developers coming from Java. The fundamental units are modules — each declares its controllers, providers, and what it exports for other modules to consume. Providers default to singleton scope, with `Scope.REQUEST` for per-request instances and `Scope.TRANSIENT` for new-per-injection. The DI container resolves the dependency graph at startup, validating that everything is wired correctly. The right choice for enterprise apps with complex domains; overkill for simple I/O microservices."
  - Vocabulário (5+): dependency injection (DI), provider, módulo (module), controller, decorador (decorator), escopo (scope).

- **## Veja também**:
  - `[[01 - Os 4 frameworks - Express, NestJS, Fastify, Hono]]`
  - `[[04 - NestJS - guards, interceptors, pipes, filters]]`
  - `[[09 - Validation com schema]]`
  - `[[11 - DI - manual vs container]]`
  - `[[Node.js]]` (tronco)

- [ ] **Step 4: Rubric** (standard, code samples mínimo 5)

- [ ] **Step 5: Commit**

```bash
git add "03-Dominios/Node/Frameworks e arquitetura/03 - NestJS - fundamentos.md"
git commit -m "feat(node-frameworks): add note 03 — NestJS fundamentos"
```

---

## Task 5: Nota 04 — NestJS guards, interceptors, pipes, filters

**Files:**
- Create: `03-Dominios/Node/Frameworks e arquitetura/04 - NestJS - guards, interceptors, pipes, filters.md`

- [ ] **Step 1: Pesquisa-âncora**

```
WebFetch: https://docs.nestjs.com/guards
WebFetch: https://docs.nestjs.com/interceptors
WebFetch: https://docs.nestjs.com/pipes
WebFetch: https://docs.nestjs.com/exception-filters
```

- [ ] **Step 2: Frontmatter**

```yaml
---
title: "NestJS: guards, interceptors, pipes, filters"
created: 2026-05-08
updated: 2026-05-08
type: concept
status: seedling
publish: true
tags:
  - node
  - frameworks
  - nestjs
  - guards
  - interceptors
  - pipes
  - filters
aliases:
  - NestJS lifecycle
  - "@UseGuards"
  - "@UseInterceptors"
  - ValidationPipe
---
```

- [ ] **Step 3: Escrever (450-550 linhas, PT-BR — nota densa)**

- **TL;DR**: NestJS tem 4 lifecycle hooks compostos numa request: **Guards** (autenticação/autorização), **Pipes** (validação/transformação), **Interceptors** (cross-cutting, antes e depois do handler), **Exception Filters** (formatação de erros). Cada um tem decorator (`@UseGuards`, `@UsePipes`, `@UseInterceptors`, `@UseFilters`) e pode ser aplicado por route, controller, ou globalmente.

- **## O que é**: cada hook + posição na request lifecycle.

- **## Por que importa**: separar concerns. Sem guards/pipes/interceptors/filters, controllers viram massa de boilerplate (auth + validation + logging + error handling em todo método).

- **## Como funciona** — request lifecycle + code samples:

  Request lifecycle order:
  
  ```
  Middleware → Guard → Interceptor (before) → Pipe → Handler →
                       Interceptor (after) → Exception Filter (se erro)
  ```

  1. **Guard:**
     ```typescript
     @Injectable()
     export class AuthGuard implements CanActivate {
       canActivate(ctx: ExecutionContext): boolean {
         const req = ctx.switchToHttp().getRequest();
         return Boolean(req.headers.authorization);
       }
     }
     
     @UseGuards(AuthGuard)
     @Get('/profile')
     getProfile() { /* ... */ }
     ```
  2. **Pipe:**
     ```typescript
     @UsePipes(new ValidationPipe({ whitelist: true, forbidNonWhitelisted: true }))
     @Post('/users')
     createUser(@Body() dto: CreateUserDto) { /* dto já validado */ }
     ```
  3. **Interceptor:**
     ```typescript
     @Injectable()
     export class TimingInterceptor implements NestInterceptor {
       intercept(ctx: ExecutionContext, next: CallHandler) {
         const start = Date.now();
         return next.handle().pipe(
           tap(() => console.log(`took ${Date.now() - start}ms`))
         );
       }
     }
     ```
  4. **Exception Filter:**
     ```typescript
     @Catch()
     export class AllExceptionsFilter implements ExceptionFilter {
       catch(exception: unknown, host: ArgumentsHost) {
         const ctx = host.switchToHttp();
         const res = ctx.getResponse<Response>();
         const status = exception instanceof HttpException ? exception.getStatus() : 500;
         res.status(status).json({
           type: 'about:blank',
           title: 'Error',
           status,
           detail: String(exception),
         });
       }
     }
     ```
  5. **Aplicação global:**
     ```typescript
     // main.ts
     app.useGlobalGuards(new AuthGuard(...));
     app.useGlobalPipes(new ValidationPipe({ whitelist: true }));
     app.useGlobalInterceptors(new TimingInterceptor());
     app.useGlobalFilters(new AllExceptionsFilter());
     ```

- **## Na prática**: padrões observados:
  - Auth: Guard global ou por feature
  - Validation: `ValidationPipe` global com `whitelist` + `forbidNonWhitelisted`
  - Logging/timing: Interceptor global
  - Problem Details: Exception Filter global (formato uniforme para todos os erros)

- **## Armadilhas (3+)**:
  1. Confundir Guard com Pipe — Guard decide se passa; Pipe transforma input
  2. Interceptor `tap()` síncrono que demora — bloqueia event loop
  3. Filter sem `@Catch()` específico → captura tudo, perde tipagem
  4. Pipe global + DTO sem decorators (`@IsString`, etc.) — validation passa silenciosa
  5. Esquecer `ValidationPipe` global → DTOs aceitam qualquer payload

- **## Em entrevista**:
  - Frase pronta: "NestJS has four lifecycle hooks composed per request. Guards run first — they decide whether the request proceeds, typically for authentication and authorization. Pipes transform and validate input — `ValidationPipe` with `class-validator` is the canonical pattern. Interceptors wrap the handler with before-and-after logic — useful for logging, timing, response transformation, and caching. Exception Filters format errors — wiring Problem Details RFC 7807 globally is the production idiom. Each hook has a decorator (`@UseGuards`, `@UsePipes`, `@UseInterceptors`, `@UseFilters`) and can be applied per-route, per-controller, or globally via `app.useGlobal*` in `main.ts`."
  - Vocabulário (6+): guard, interceptor, pipe, filter, decorator, lifecycle hook, request lifecycle.

- **## Veja também**:
  - `[[03 - NestJS - fundamentos]]`
  - `[[07 - Middleware pipeline]]`
  - `[[08 - Error handling estruturado]]`
  - `[[09 - Validation com schema]]`
  - `[[Node.js]]` (tronco)

- [ ] **Step 4: Rubric** (standard, code samples mínimo 5)

- [ ] **Step 5: Commit**

```bash
git add "03-Dominios/Node/Frameworks e arquitetura/04 - NestJS - guards, interceptors, pipes, filters.md"
git commit -m "feat(node-frameworks): add note 04 — NestJS lifecycle hooks"
```

---

## Task 6: Nota 05 — Fastify

**Files:**
- Create: `03-Dominios/Node/Frameworks e arquitetura/05 - Fastify - schema-first, plugins, performance.md`

- [ ] **Step 1: Pesquisa-âncora**

```
WebFetch: https://fastify.dev/docs/latest/Reference/Validation-and-Serialization/
WebFetch: https://fastify.dev/docs/latest/Reference/Plugins/
WebFetch: https://fastify.dev/docs/latest/Reference/Hooks/
```

- [ ] **Step 2: Frontmatter**

```yaml
---
title: "Fastify: schema-first, plugins, performance"
created: 2026-05-08
updated: 2026-05-08
type: concept
status: seedling
publish: true
tags:
  - node
  - frameworks
  - fastify
  - schema
  - performance
aliases:
  - Fastify
  - JSON schema
  - fastify-plugin
---
```

- [ ] **Step 3: Escrever (350-500 linhas, PT-BR)**

- **TL;DR**: Fastify é performance-focused, com **schema JSON declarativo** em route (validation + serialization automática via `fast-json-stringify`). Plugin system com encapsulation por default (o que um plugin faz não vaza). Throughput ~2-3× Express em benchmarks típicos. Right choice pra APIs com schema bem definido e throughput como prioridade.

- **## O que é**: framework HTTP performance-focused, schema-driven.

- **## Por que importa**: em APIs com contrato bem definido (REST com OpenAPI, GraphQL, RPC), schema-first ganha validação manual ad-hoc. Performance edge é cereja.

- **## Como funciona** — code samples:
  1. **Setup minimal:**
     ```typescript
     import Fastify from 'fastify';
     const app = Fastify({ logger: true });
     app.get('/hello', async () => ({ greeting: 'hello' }));
     await app.listen({ port: 3000 });
     ```
  2. **Schema em route (validation + serialization):**
     ```typescript
     app.post('/users', {
       schema: {
         body: {
           type: 'object',
           required: ['name', 'email'],
           properties: {
             name: { type: 'string', minLength: 1 },
             email: { type: 'string', format: 'email' },
           },
         },
         response: {
           201: {
             type: 'object',
             properties: {
               id: { type: 'string' },
               name: { type: 'string' },
               email: { type: 'string' },
             },
           },
         },
       },
     }, async (req, reply) => {
       const user = await db.users.create(req.body);
       reply.code(201).send(user);
     });
     ```
  3. **Plugin com encapsulation:**
     ```typescript
     import fp from 'fastify-plugin';
     
     async function dbPlugin(fastify) {
       const db = await connectDb();
       fastify.decorate('db', db);
       fastify.addHook('onClose', async () => db.close());
     }
     
     export default fp(dbPlugin); // fp() opta-out de encapsulation (acessível em scopes pais)
     ```
  4. **Hooks:**
     ```typescript
     app.addHook('onRequest', async (req, reply) => {
       req.startTime = Date.now();
     });
     app.addHook('onResponse', async (req, reply) => {
       const ms = Date.now() - req.startTime;
       app.log.info({ url: req.url, ms });
     });
     ```
  5. **Type provider (TypeScript-first):**
     ```typescript
     import { TypeBoxTypeProvider } from '@fastify/type-provider-typebox';
     import { Type } from '@sinclair/typebox';
     
     const app = Fastify().withTypeProvider<TypeBoxTypeProvider>();
     const UserSchema = Type.Object({ name: Type.String(), email: Type.String() });
     app.post('/users', { schema: { body: UserSchema } }, async (req) => {
       // req.body é tipado automaticamente
     });
     ```

- **## Na prática**: padrão observado:
  - Schema em **toda** route (mesmo simples) — validation + serialization free
  - Plugins per feature, encapsulated
  - TypeBox ou JSON Schema direto, dependendo de preferência
  - `@fastify/swagger` gera OpenAPI dos schemas

- **## Armadilhas (3+)**:
  1. Schema sem `additionalProperties: false` → propriedades extras passam
  2. Esquecer `await app.listen(...)` ou `await app.ready()` em testes
  3. Plugin que registra rota sem encapsulation → polui app pai
  4. `app.decorate('foo', ...)` dentro de plugin encapsulated → não vaza pra fora (é o ponto)

- **## Em entrevista**:
  - Frase pronta: "Fastify is schema-first and performance-focused. You declare a JSON schema or TypeBox schema in every route — that gives you input validation and response serialization automatically, with `fast-json-stringify` doing serialization about ten times faster than `JSON.stringify`. Throughput is typically two to three times Express in standard benchmarks. The plugin system is encapsulated by default — what a plugin registers doesn't leak to its parent unless you wrap it with `fastify-plugin`. Right choice when your API contract is well-defined and throughput matters."
  - Vocabulário (5+): schema-first, JSON schema, type provider, plugin encapsulation, throughput.

- **## Veja também**:
  - `[[01 - Os 4 frameworks - Express, NestJS, Fastify, Hono]]`
  - `[[07 - Middleware pipeline]]`
  - `[[09 - Validation com schema]]`
  - `[[Node.js]]` (tronco)

- [ ] **Step 4: Rubric** (standard)

- [ ] **Step 5: Commit**

```bash
git add "03-Dominios/Node/Frameworks e arquitetura/05 - Fastify - schema-first, plugins, performance.md"
git commit -m "feat(node-frameworks): add note 05 — Fastify"
```

---

## Task 7: Nota 06 — Hono e edge runtimes

**Files:**
- Create: `03-Dominios/Node/Frameworks e arquitetura/06 - Hono e edge runtimes.md`

- [ ] **Step 1: Pesquisa-âncora**

```
WebFetch: https://hono.dev/docs/
WebFetch: https://hono.dev/docs/concepts/middleware
```

- [ ] **Step 2: Frontmatter**

```yaml
---
title: "Hono e edge runtimes"
created: 2026-05-08
updated: 2026-05-08
type: concept
status: seedling
publish: true
tags:
  - node
  - frameworks
  - hono
  - edge
  - cloudflare-workers
  - serverless
aliases:
  - Hono
  - edge runtime
  - Cloudflare Workers
  - Deno Deploy
---
```

- [ ] **Step 3: Escrever (350-450 linhas, PT-BR)**

- **TL;DR**: Hono é framework ultralight com Fetch API native (`Request`/`Response` ao invés de `req`/`res`), multi-runtime: Cloudflare Workers, Deno Deploy, Bun, Node, AWS Lambda. Constraints de edge: sem `fs`, sem TCP custom, limites de tempo (~50ms-30s) e memória (~128MB-1GB). Right choice quando deploy é edge-first.

- **## O que é**: framework HTTP minimalista, multi-runtime, edge-first.

- **## Por que importa**: edge runtimes (Cloudflare Workers, Deno Deploy, Vercel Edge Functions) crescem em 2026. Frameworks Node-specific (Express, NestJS) não funcionam diretamente — Hono dá uma API uniforme.

- **## Como funciona** — code samples:
  1. **Setup minimal:**
     ```typescript
     import { Hono } from 'hono';
     const app = new Hono();
     app.get('/hello', (c) => c.json({ greeting: 'hello' }));
     export default app;
     ```
  2. **Multi-runtime export:**
     ```typescript
     // Mesmo código roda em Node, Cloudflare Workers, Deno, Bun
     // Cloudflare Workers: export default app;
     // Node: import { serve } from '@hono/node-server'; serve({ fetch: app.fetch })
     // Deno: Deno.serve(app.fetch)
     // Bun: export default { fetch: app.fetch }
     ```
  3. **Middleware (Koa-like onion):**
     ```typescript
     app.use('*', async (c, next) => {
       const start = Date.now();
       await next();
       const ms = Date.now() - start;
       console.log(`${c.req.method} ${c.req.url} ${ms}ms`);
     });
     ```
  4. **Validation com zod (oficial):**
     ```typescript
     import { zValidator } from '@hono/zod-validator';
     import { z } from 'zod';
     
     const schema = z.object({ name: z.string(), email: z.string().email() });
     app.post('/users', zValidator('json', schema), async (c) => {
       const data = c.req.valid('json'); // tipado
       return c.json({ id: 'new', ...data }, 201);
     });
     ```
  5. **Error handling:**
     ```typescript
     app.onError((err, c) => {
       const status = err instanceof HTTPException ? err.status : 500;
       return c.json({ type: 'about:blank', title: 'Error', status, detail: err.message }, status);
     });
     ```

- **## Na prática**: decisão pragmática:
  - **Use Hono quando:** deploy é edge (Cloudflare Workers, Vercel Edge), serverless multi-runtime, ou preview de portabilidade futura
  - **Use Express/Fastify/NestJS quando:** Node-only, integração com `fs`/`net`/`http2` específica, ecossistema maduro de libs Node-only
  - Constraints de edge: tempo limitado, memória limitada, sem APIs Node-specific. Hono respeita.

- **## Armadilhas (3+)**:
  1. Assumir APIs Node-specific (`fs`, `net`) em edge runtime — falha em CF Workers
  2. CPU time limit em edge (~10-50ms grátis) — handlers pesados quebram
  3. State em variável de módulo — em edge cada request pode ser worker isolado, sem state shared
  4. Esquecer que `c.req.json()` é async — `await` é obrigatório

- **## Em entrevista**:
  - Frase pronta: "Hono is an ultralight framework that runs natively on multiple JavaScript runtimes — Cloudflare Workers, Deno Deploy, Bun, Node, AWS Lambda. The API is built on the Fetch API standard — `Request` and `Response` objects, instead of `req` and `res`. Middleware uses the Koa-like onion model with `await next()`. The decision to use Hono is pragmatic: pick it when your deploy target is edge or serverless multi-runtime. For Node-only apps with deep integration into `fs` or `net`, Express, Fastify, or NestJS still win because of the mature ecosystem."
  - Vocabulário (5+): edge runtime, Fetch API native, multi-runtime, ultralight, onion middleware.

- **## Veja também**:
  - `[[01 - Os 4 frameworks - Express, NestJS, Fastify, Hono]]`
  - `[[07 - Middleware pipeline]]`
  - `[[12 - Decision tree + cheatsheet]]`
  - `[[Node.js]]` (tronco)

- [ ] **Step 4: Rubric** (standard)

- [ ] **Step 5: Commit**

```bash
git add "03-Dominios/Node/Frameworks e arquitetura/06 - Hono e edge runtimes.md"
git commit -m "feat(node-frameworks): add note 06 — Hono e edge runtimes"
```

---

## Task 8: Nota 07 — Middleware pipeline

**Files:**
- Create: `03-Dominios/Node/Frameworks e arquitetura/07 - Middleware pipeline.md`

- [ ] **Step 1: Pesquisa-âncora**

Sem WebFetch específica — síntese das 4 docs.

- [ ] **Step 2: Frontmatter**

```yaml
---
title: "Middleware pipeline"
created: 2026-05-08
updated: 2026-05-08
type: concept
status: seedling
publish: true
tags:
  - node
  - frameworks
  - middleware
  - pipeline
aliases:
  - Middleware
  - Hooks
  - Onion model
---
```

- [ ] **Step 3: Escrever (350-450 linhas, PT-BR)**

- **TL;DR**: Os 4 frameworks lidam com middleware/pipeline diferente: Express (`(req, res, next)`, ordem matters, mutate-friendly), Fastify (hooks tipados: `onRequest`, `preHandler`, `onResponse`, `onError`), NestJS (interceptors com `Observable`-style + middleware function tradicional), Hono (Koa-like onion com `await next()`). Trade-offs e quando cada modelo cabe.

- **## O que é**: pipeline de funções que processam request antes/depois do handler.

- **## Por que importa**: cross-cutting concerns (auth, logging, rate limit, CORS) vivem na pipeline. Modelo certo facilita; errado vira boilerplate ou bugs.

- **## Como funciona** — code samples comparativos:
  1. **Express:**
     ```typescript
     app.use((req, res, next) => {
       req.startTime = Date.now();
       next(); // ordem matters, mutate req é comum
     });
     ```
  2. **Fastify (hooks):**
     ```typescript
     app.addHook('onRequest', async (req, reply) => { req.startTime = Date.now(); });
     app.addHook('onResponse', async (req, reply) => {
       app.log.info({ ms: Date.now() - req.startTime });
     });
     ```
  3. **NestJS (Interceptor):**
     ```typescript
     @Injectable()
     class TimingInterceptor implements NestInterceptor {
       intercept(ctx: ExecutionContext, next: CallHandler) {
         const start = Date.now();
         return next.handle().pipe(tap(() => log(`took ${Date.now() - start}`)));
       }
     }
     ```
  4. **Hono (Koa-like onion):**
     ```typescript
     app.use('*', async (c, next) => {
       const start = Date.now();
       await next(); // ⬅ aguarda handler + middlewares posteriores
       console.log(`took ${Date.now() - start}`);
     });
     ```

- **Tabela comparativa:**

  | Framework | Modelo | Mutação OK? | Async nativo? | Posição (before/after) |
  |---|---|---|---|---|
  | Express | next() callback | sim | v5 sim, v4 manual | sequencial |
  | Fastify | hooks tipados | parcial | sim | hook nomeado |
  | NestJS | Observable + middleware | sim | sim | decorator + lifecycle |
  | Hono | onion (await next) | sim | sim | onion (before + after no mesmo) |

- **## Na prática**: patterns comuns implementados em cada framework:
  - **Logging**: Express middleware, Fastify hook, NestJS interceptor, Hono onion
  - **Auth**: Express middleware com `next(err)`, Fastify preHandler, NestJS Guard, Hono middleware com `c.set()`
  - **CORS**: Express `cors`, Fastify `@fastify/cors`, NestJS `app.enableCors()`, Hono built-in
  - **Rate limit**: Express `express-rate-limit`, Fastify `@fastify/rate-limit`, NestJS `@nestjs/throttler`, Hono `hono-rate-limiter`

- **## Armadilhas (3+)**:
  1. Express: ordem do `app.use()` matters — middleware depois da rota não pega
  2. Fastify: hook `onRequest` vs `preHandler` — onRequest roda mais cedo (antes de validation/parsing)
  3. NestJS: middleware vs interceptor — middleware é mais cru (pre-DI), interceptor tem acesso ao DI container
  4. Hono: esquecer `await next()` → handler nunca roda
  5. Async middleware sem error handling → silencioso

- **## Em entrevista**:
  - Frase pronta: "Each of the four main Node frameworks models middleware differently. Express is the classic — `(req, res, next)`, sequential, mutation-friendly. Fastify uses typed hooks — `onRequest`, `preHandler`, `onResponse`, `onError` — which gives you precise control over when in the lifecycle you run. NestJS has both traditional middleware functions and Interceptors, which use an Observable-based model and have access to the DI container. Hono uses the Koa-like onion model — you call `await next()` and the same function gets a before-and-after view of the request."
  - Vocabulário (5+): middleware, hook, interceptor, onion model, request lifecycle.

- **## Veja também**:
  - `[[02 - Express idiomático]]`
  - `[[03 - NestJS - fundamentos]]`
  - `[[04 - NestJS - guards, interceptors, pipes, filters]]`
  - `[[05 - Fastify - schema-first, plugins, performance]]`
  - `[[06 - Hono e edge runtimes]]`
  - `[[Node.js]]` (tronco)

- [ ] **Step 4: Rubric** (standard)

- [ ] **Step 5: Commit**

```bash
git add "03-Dominios/Node/Frameworks e arquitetura/07 - Middleware pipeline.md"
git commit -m "feat(node-frameworks): add note 07 — Middleware pipeline"
```

---

## Task 9: Nota 08 — Error handling estruturado

**Files:**
- Create: `03-Dominios/Node/Frameworks e arquitetura/08 - Error handling estruturado.md`

- [ ] **Step 1: Pesquisa-âncora**

```
WebFetch: https://datatracker.ietf.org/doc/html/rfc7807
```

- [ ] **Step 2: Frontmatter**

```yaml
---
title: "Error handling estruturado"
created: 2026-05-08
updated: 2026-05-08
type: concept
status: seedling
publish: true
tags:
  - node
  - frameworks
  - error-handling
  - problem-details
  - rfc-7807
aliases:
  - Problem Details
  - RFC 7807
  - error middleware
---
```

- [ ] **Step 3: Escrever (350-500 linhas, PT-BR)**

- **TL;DR**: Problem Details (RFC 7807) é o padrão pra erros HTTP estruturados — `application/problem+json` com `type`, `title`, `status`, `detail`, `instance`. Implementação varia por framework: Express (error middleware com 4 args), NestJS (exception filter), Fastify (custom errorHandler + schema). Padronizar errors deixa cliente parsear uniforme e observability uniforme.

- **## O que é**: RFC 7807 + implementação em cada framework.

- **## Por que importa**: cada framework tem seu jeito; sem padrão, cliente trata cada API diferente, observability vira ad-hoc, debugging é difícil.

- **## Como funciona**:

  Estrutura Problem Details:
  ```json
  {
    "type": "https://api.example.com/errors/validation",
    "title": "Validation Failed",
    "status": 400,
    "detail": "Field 'email' must be a valid email",
    "instance": "/api/v1/users"
  }
  ```

  1. **Express:**
     ```typescript
     class HttpError extends Error {
       constructor(public status: number, public type: string, message: string) { super(message); }
     }
     
     app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
       if (err instanceof HttpError) {
         res.status(err.status).type('application/problem+json').json({
           type: err.type,
           title: err.constructor.name,
           status: err.status,
           detail: err.message,
           instance: req.originalUrl,
         });
       } else {
         res.status(500).type('application/problem+json').json({
           type: 'about:blank',
           title: 'Internal Server Error',
           status: 500,
           detail: 'Unexpected error',
           instance: req.originalUrl,
         });
       }
     });
     ```
  2. **NestJS (exception filter):**
     ```typescript
     @Catch()
     export class ProblemDetailsFilter implements ExceptionFilter {
       catch(exception: unknown, host: ArgumentsHost) {
         const ctx = host.switchToHttp();
         const res = ctx.getResponse<Response>();
         const req = ctx.getRequest<Request>();
         const status = exception instanceof HttpException ? exception.getStatus() : 500;
         const detail = exception instanceof Error ? exception.message : String(exception);
         res.status(status).type('application/problem+json').json({
           type: 'about:blank', title: 'Error', status, detail, instance: req.url,
         });
       }
     }
     // main.ts: app.useGlobalFilters(new ProblemDetailsFilter())
     ```
  3. **Fastify:**
     ```typescript
     app.setErrorHandler((err, req, reply) => {
       const status = err.statusCode ?? 500;
       reply.code(status).type('application/problem+json').send({
         type: 'about:blank', title: err.name, status, detail: err.message, instance: req.url,
       });
     });
     ```
  4. **Hono:**
     ```typescript
     app.onError((err, c) => {
       const status = err instanceof HTTPException ? err.status : 500;
       return c.json({
         type: 'about:blank', title: 'Error', status, detail: err.message, instance: c.req.url,
       }, status, { 'Content-Type': 'application/problem+json' });
     });
     ```

  **Error taxonomy:**
  - 4xx: client error (validation fail, not found, unauthorized)
  - 5xx: server error (DB down, unexpected exception)
  - **Programmer error** (bug): assertion fail, type error → log + 500
  - **Operational error** (esperado): validation fail, not found → log + status apropriado

- **## Na prática**: padrões observados:
  - Filter/middleware **global** (não per-route)
  - Stack trace **só em dev** — vazar em prod é vulnerabilidade
  - Correlation ID no `instance` ou em campo extra (preview de galho 5)
  - Tipos de erro como hierarquia (`HttpError` → `NotFoundError`, `ValidationError`, etc.)

- **## Armadilhas (3+)**:
  1. Stack trace exposto em prod → leak de info sensível
  2. Error middleware com 3 args ao invés de 4 → Express não trata como error handler
  3. Mistura de status codes (400 pra DB error, 500 pra validation) → cliente confuso
  4. Async handler sem try/catch e sem wrapper → erro vira `unhandledRejection`
  5. Esquecer `next(err)` em catch — error não chega ao handler global

- **## Em entrevista**:
  - Frase pronta: "Problem Details, defined in RFC 7807, is the standard for structured HTTP errors — `application/problem+json` with `type`, `title`, `status`, `detail`, and `instance` fields. Each framework implements it differently. Express uses error middleware with a four-argument signature — `(err, req, res, next)` — registered globally. NestJS uses an exception filter applied with `useGlobalFilters`. Fastify uses `setErrorHandler`. Hono uses `app.onError`. The senior detail is taxonomy — distinguishing programmer errors from operational errors, never exposing stack traces in production, and correlating with logs via instance or correlation ID."
  - Vocabulário (5+): Problem Details, error middleware, exception filter, error taxonomy, correlation ID.

- **## Veja também**:
  - `[[02 - Express idiomático]]`
  - `[[04 - NestJS - guards, interceptors, pipes, filters]]`
  - `[[05 - Fastify - schema-first, plugins, performance]]`
  - `[[06 - Hono e edge runtimes]]`
  - `[[09 - Validation com schema]]`
  - `[[Node.js]]` (tronco)

- [ ] **Step 4: Rubric** (standard, code samples mínimo 4)

- [ ] **Step 5: Commit**

```bash
git add "03-Dominios/Node/Frameworks e arquitetura/08 - Error handling estruturado.md"
git commit -m "feat(node-frameworks): add note 08 — Error handling"
```

---

## Task 10: Nota 09 — Validation com schema

**Files:**
- Create: `03-Dominios/Node/Frameworks e arquitetura/09 - Validation com schema.md`

- [ ] **Step 1: Pesquisa-âncora**

```
WebFetch: https://zod.dev/
WebFetch: https://docs.nestjs.com/techniques/validation
```

- [ ] **Step 2: Frontmatter**

```yaml
---
title: "Validation com schema"
created: 2026-05-08
updated: 2026-05-08
type: concept
status: seedling
publish: true
tags:
  - node
  - frameworks
  - validation
  - zod
  - schema
aliases:
  - zod
  - JSON Schema
  - ValidationPipe
  - class-validator
---
```

- [ ] **Step 3: Escrever (400-500 linhas, PT-BR)**

- **TL;DR**: Em 2026, schema-first é o padrão pra validation em Node. **zod** lidera (TypeScript-first, schema → tipo + runtime validation). **Fastify schema** (JSON Schema integrado), **NestJS ValidationPipe + class-validator**, **joi** (legacy mas ainda comum). Convergência: schema-first elimina validação manual ad-hoc; type inference dá DX moderna.

- **## O que é**: schemas como contrato de input + tipo TypeScript + validation runtime.

- **## Por que importa**: validação manual ad-hoc espalhada em controllers vira bug factory. Schema centraliza, é testável, e gera tipo automaticamente.

- **## Como funciona** — code samples por lib/framework:
  1. **zod (cross-framework):**
     ```typescript
     import { z } from 'zod';
     
     const CreateUserSchema = z.object({
       name: z.string().min(1).max(100),
       email: z.string().email(),
       age: z.number().int().min(0).optional(),
     });
     
     type CreateUser = z.infer<typeof CreateUserSchema>; // tipo derivado
     
     // Express
     app.post('/users', (req, res) => {
       const data = CreateUserSchema.parse(req.body); // throws on fail
       // data é tipado como CreateUser
     });
     
     // Hono (oficial)
     import { zValidator } from '@hono/zod-validator';
     app.post('/users', zValidator('json', CreateUserSchema), (c) => {
       const data = c.req.valid('json');
     });
     ```
  2. **Fastify (JSON Schema):**
     ```typescript
     app.post('/users', {
       schema: {
         body: {
           type: 'object',
           required: ['name', 'email'],
           additionalProperties: false,
           properties: {
             name: { type: 'string', minLength: 1, maxLength: 100 },
             email: { type: 'string', format: 'email' },
             age: { type: 'integer', minimum: 0 },
           },
         },
       },
     }, async (req) => {
       // req.body é validado e tipado (com type provider)
     });
     ```
  3. **NestJS (class-validator + class-transformer):**
     ```typescript
     import { IsString, IsEmail, IsInt, Min, IsOptional, MinLength, MaxLength } from 'class-validator';
     
     export class CreateUserDto {
       @IsString() @MinLength(1) @MaxLength(100)
       name!: string;
     
       @IsEmail()
       email!: string;
     
       @IsOptional() @IsInt() @Min(0)
       age?: number;
     }
     
     @Controller('users')
     export class UsersController {
       @Post()
       create(@Body() dto: CreateUserDto) {
         // dto validado pela ValidationPipe global
       }
     }
     ```
  4. **NestJS + zod (alternativa moderna):**
     ```typescript
     import { ZodValidationPipe } from 'nestjs-zod';
     
     @Post()
     @UsePipes(new ZodValidationPipe(CreateUserSchema))
     create(@Body() dto: CreateUser) { /* ... */ }
     ```
  5. **Versionamento via path-based:**
     ```typescript
     // /api/v1 → schema v1; /api/v2 → schema v2 (campo extra, etc.)
     // Schemas separados por versão em arquivos diferentes
     ```

- **## Na prática**: padrão observado:
  - **zod** é o default em projetos novos com TypeScript em 2026
  - **JSON Schema (Fastify)** quando integração com OpenAPI matters
  - **class-validator** ainda dominante em NestJS legacy; novos projetos NestJS migrando pra zod via wrappers
  - **joi** raramente em código novo
  - Schema único definido uma vez, reusado em validation + tipo + OpenAPI gen

- **## Armadilhas (3+)**:
  1. Schema sem `.strict()` (zod) ou `additionalProperties: false` (JSON Schema) → propriedades extras passam silenciosamente
  2. Validar só request body, esquecer query/params — data inválida entra
  3. Mensagens de erro padrão (zod) genéricas — customizar `.refine()` ou `errorMap`
  4. `class-validator` sem `whitelist: true` na ValidationPipe — DTO com campos extras aceito
  5. Mistura de zod + class-validator no mesmo projeto — confusão

- **## Em entrevista**:
  - Frase pronta: "Schema-first validation has converged in the Node ecosystem in 2026. zod is the modern default for TypeScript projects — you write a schema once, get a TypeScript type via `z.infer`, and runtime validation via `.parse()`. Fastify uses JSON Schema natively, integrating with OpenAPI generation. NestJS traditionally uses `class-validator` with decorators on DTO classes, validated by a global `ValidationPipe` — newer NestJS projects often wrap zod instead. The senior pattern: define the schema once, reuse for input validation, type inference, and API contract documentation."
  - Vocabulário (5+): schema-first, type inference, JSON Schema, ValidationPipe, schema wrapper.

- **## Veja também**:
  - `[[04 - NestJS - guards, interceptors, pipes, filters]]`
  - `[[05 - Fastify - schema-first, plugins, performance]]`
  - `[[06 - Hono e edge runtimes]]`
  - `[[08 - Error handling estruturado]]`
  - `[[Node.js]]` (tronco)

- [ ] **Step 4: Rubric** (standard, code samples mínimo 4)

- [ ] **Step 5: Commit**

```bash
git add "03-Dominios/Node/Frameworks e arquitetura/09 - Validation com schema.md"
git commit -m "feat(node-frameworks): add note 09 — Validation com schema"
```

---

## Task 11: Nota 10 — Clean Architecture em Node

**Files:**
- Create: `03-Dominios/Node/Frameworks e arquitetura/10 - Clean Architecture em Node.md`

- [ ] **Step 1: Pesquisa-âncora**

```
WebFetch: https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html
```

- [ ] **Step 2: Frontmatter**

```yaml
---
title: "Clean Architecture em Node"
created: 2026-05-08
updated: 2026-05-08
type: concept
status: seedling
publish: true
tags:
  - node
  - frameworks
  - clean-architecture
  - hexagonal
  - architecture
aliases:
  - Clean Architecture
  - Hexagonal
  - Ports and adapters
---
```

- [ ] **Step 3: Escrever (400-500 linhas, PT-BR)**

- **TL;DR**: Clean Architecture (Robert Martin) organiza código em camadas concêntricas: entities (regras de domínio), use cases (regras de aplicação), interface adapters (controllers, presenters), frameworks/drivers (Express, DB drivers). Dependency rule: dependências apontam **pra dentro**. Em Node, aplica em Express+TS (manual, pastas) ou NestJS (módulos por feature). Pragmatismo: aplicar quando complexidade do domínio justifica.

- **## O que é**: arquitetura concêntrica, dependency rule.

- **## Por que importa**: separar regras de negócio de framework permite trocar Express por Fastify, MySQL por Postgres, sem mexer em domínio. Em apps de domínio rico, evita acoplamento que mata manutenção.

- **## Como funciona**:

  Camadas:
  ```
  Entities (núcleo)
  └─ Use Cases
     └─ Interface Adapters (controllers, presenters, repositories)
        └─ Frameworks & Drivers (Express, DB, libs externas)
  ```

  **Dependency rule:** camadas externas dependem de internas; internas não dependem de externas (inversão).

  1. **Estrutura de pastas (Express + TypeScript):**
     ```
     src/
     ├─ domain/          # entities (puro JS, sem deps externas)
     │  └─ User.ts
     ├─ application/     # use cases
     │  └─ CreateUserUseCase.ts
     ├─ infrastructure/  # adapters: DB, HTTP, libs
     │  ├─ db/UserRepositoryPg.ts
     │  └─ http/UserController.ts
     └─ presentation/    # framework wiring (Express setup)
        └─ server.ts
     ```
  2. **Entity (puro):**
     ```typescript
     export class User {
       constructor(public readonly id: string, public name: string, public email: string) {}
       changeName(name: string) {
         if (name.length < 1) throw new Error('Name required');
         this.name = name;
       }
     }
     ```
  3. **Use case (depende de port, não de adapter):**
     ```typescript
     export interface UserRepository {
       save(user: User): Promise<void>;
       findById(id: string): Promise<User | null>;
     }
     
     export class CreateUserUseCase {
       constructor(private readonly repo: UserRepository) {}
       async execute(input: { name: string; email: string }): Promise<User> {
         const user = new User(generateId(), input.name, input.email);
         await this.repo.save(user);
         return user;
       }
     }
     ```
  4. **Adapter (implementa port):**
     ```typescript
     import { UserRepository } from '../../application/UserRepository';
     
     export class UserRepositoryPg implements UserRepository {
       constructor(private readonly db: PgPool) {}
       async save(user: User): Promise<void> {
         await this.db.query('INSERT ...', [user.id, user.name, user.email]);
       }
       async findById(id: string): Promise<User | null> { /* ... */ }
     }
     ```
  5. **Wiring (presentation):**
     ```typescript
     const repo = new UserRepositoryPg(pgPool);
     const useCase = new CreateUserUseCase(repo);
     const controller = new UserController(useCase);
     app.post('/users', (req, res) => controller.create(req, res));
     ```

- **## Na prática**:
  - **Em apps com domínio rico** (regras de negócio complexas, múltiplas integrações): Clean ganha — testabilidade, separação clara
  - **Em apps simples** (CRUD direto, sem regras complexas): Clean é overhead — pasta `domain` quase vazia, complexidade inflada
  - **NestJS módulos por feature** se aproxima naturalmente — providers funcionam como adapters
  - **Hexagonal/Ports-and-Adapters** é nomenclatura alternativa pra mesma ideia

- **## Armadilhas (3+)**:
  1. Aplicar Clean em CRUD simples — overhead sem benefício
  2. Entity importando ORM (`@Entity()` decorator) → vaza framework pra dentro
  3. Use case importando Express request — acopla camada interna a framework
  4. Adapter virando god class — quebrar por contexto
  5. DI manual sem composition root claro — fica difícil mudar wire

- **## Em entrevista**:
  - Frase pronta: "Clean Architecture, defined by Robert Martin, organizes code in concentric layers — entities at the core, then use cases, then interface adapters like controllers and repositories, with frameworks and drivers at the outermost layer. The dependency rule is the load-bearing idea: dependencies point inward, never outward, which means you can swap Express for Fastify or PostgreSQL for another database without touching the domain layer. The pragmatic version: apply Clean when domain complexity justifies the structural overhead. For simple CRUD apps, it's over-engineering. NestJS's feature-module structure naturally approximates this when used disciplined."
  - Vocabulário (5+): camada (layer), regra de dependência (dependency rule), porta (port), adaptador (adapter), inversão de dependência (dependency inversion).

- **## Veja também**:
  - `[[03 - NestJS - fundamentos]]`
  - `[[11 - DI - manual vs container]]`
  - `[[Node.js]]` (tronco)
  - `[[Arquitetura de Software]]` (se existir)

- [ ] **Step 4: Rubric** (standard, code samples mínimo 4)

- [ ] **Step 5: Commit**

```bash
git add "03-Dominios/Node/Frameworks e arquitetura/10 - Clean Architecture em Node.md"
git commit -m "feat(node-frameworks): add note 10 — Clean Architecture"
```

---

## Task 12: Nota 11 — DI manual vs container

**Files:**
- Create: `03-Dominios/Node/Frameworks e arquitetura/11 - DI - manual vs container.md`

- [ ] **Step 1: Pesquisa-âncora**

```
WebFetch: https://github.com/jeffijoe/awilix
WebFetch: https://github.com/microsoft/tsyringe
```

- [ ] **Step 2: Frontmatter**

```yaml
---
title: "DI: manual vs container"
created: 2026-05-08
updated: 2026-05-08
type: concept
status: seedling
publish: true
tags:
  - node
  - frameworks
  - dependency-injection
  - di
  - architecture
aliases:
  - DI manual
  - DI container
  - tsyringe
  - awilix
---
```

- [ ] **Step 3: Escrever (350-450 linhas, PT-BR)**

- **TL;DR**: DI sem container é constructor injection puro — passar dependências no `new MyService(repo, logger)`, com **composition root** no startup. Containers (NestJS built-in, tsyringe, awilix, InversifyJS) automatizam wiring + lifecycle scopes. Use container quando app é grande, time é grande, ou lifecycle é complexo (request-scoped). Overkill em apps pequenos.

- **## O que é**: DI manual vs framework de DI.

- **## Por que importa**: container resolve "quem instancia quem" automaticamente em apps grandes, mas adiciona complexidade conceitual em apps pequenos.

- **## Como funciona**:
  1. **DI manual com composition root:**
     ```typescript
     // composition-root.ts (rodado uma vez no startup)
     const logger = new Logger();
     const db = new PgPool({ /* config */ });
     const userRepo = new UserRepositoryPg(db);
     const createUser = new CreateUserUseCase(userRepo, logger);
     const userController = new UserController(createUser);
     
     export { userController };
     ```
  2. **Factory functions (alternativa funcional):**
     ```typescript
     export function makeUserController(deps: { db: PgPool; logger: Logger }) {
       const repo = new UserRepositoryPg(deps.db);
       const createUser = new CreateUserUseCase(repo, deps.logger);
       return new UserController(createUser);
     }
     ```
  3. **NestJS container (built-in):**
     ```typescript
     @Injectable()
     class CreateUserUseCase {
       constructor(private readonly repo: UserRepository, private readonly logger: Logger) {}
     }
     // NestJS resolve automaticamente
     ```
  4. **awilix (proxy-based, sem decorators):**
     ```typescript
     import { createContainer, asClass, asValue, InjectionMode } from 'awilix';
     
     const container = createContainer({ injectionMode: InjectionMode.PROXY });
     container.register({
       db: asValue(pgPool),
       logger: asClass(Logger).singleton(),
       userRepo: asClass(UserRepositoryPg).singleton(),
       createUser: asClass(CreateUserUseCase).singleton(),
     });
     
     const createUser = container.resolve('createUser');
     ```
  5. **tsyringe (decorator-based):**
     ```typescript
     import { container, injectable, inject } from 'tsyringe';
     
     @injectable()
     class CreateUserUseCase {
       constructor(
         @inject('UserRepository') private repo: UserRepository,
         @inject('Logger') private logger: Logger,
       ) {}
     }
     
     container.register('UserRepository', { useClass: UserRepositoryPg });
     const useCase = container.resolve(CreateUserUseCase);
     ```

  **Tabela comparativa:**

  | Approach | Complexidade ramp-up | Lifecycle scopes | Boilerplate | Quando usar |
  |---|---|---|---|---|
  | Manual (composition root) | Mínima | Manual | Baixo em pequeno; alto em grande | App pequeno, time pequeno |
  | NestJS DI | Médio (aprender DI) | Built-in (singleton, request, transient) | Mínimo (decorators) | Apps NestJS (default) |
  | awilix | Médio | `singleton`, `scoped`, `transient` | Médio | Express/Fastify quando container ajuda |
  | tsyringe | Médio | `singleton`, `transient` | Médio (decorators + tokens) | Express/Fastify quando decorators ok |
  | InversifyJS | Alto | Completo | Alto | Apps grandes JS clássico |

- **## Na prática**:
  - **App pequeno (≤10 services)**: DI manual com composition root. Simples, direto.
  - **App médio (10-50 services)**: factory functions ou container leve (awilix).
  - **App grande (50+ services)**: container completo (NestJS, InversifyJS).
  - **Request-scoped providers** (dados da request, tracing): container facilita; manual fica chato.

- **## Armadilhas (3+)**:
  1. Container em app pequeno — "estamos prontos pra escalar" geralmente vira complexidade que não escala
  2. Mistura de DI manual + container no mesmo projeto — confuso
  3. tsyringe sem `reflect-metadata` import → erros silenciosos em runtime
  4. NestJS request-scoped provider que injeta singleton → singleton vira request-scoped (pegadinha)
  5. Composition root espalhado em vários arquivos — perde rastreabilidade

- **## Em entrevista**:
  - Frase pronta: "DI without a container is constructor injection plus a composition root — you instantiate everything once in startup, passing dependencies explicitly. Containers like NestJS built-in, tsyringe, and awilix automate the wiring and add lifecycle scopes — singleton, request-scoped, transient. The decision is matching: small app with shallow dependencies, manual DI is simpler. Large app, complex domain, or request-scoped providers — container earns its complexity. The senior anti-pattern: introducing a container in a small app 'because we'll need it later' — usually that complexity doesn't scale, it just makes the simple case harder."
  - Vocabulário (5+): composition root, constructor injection, container, lifecycle scope, request-scoped.

- **## Veja também**:
  - `[[03 - NestJS - fundamentos]]`
  - `[[10 - Clean Architecture em Node]]`
  - `[[Node.js]]` (tronco)

- [ ] **Step 4: Rubric** (standard, code samples mínimo 4)

- [ ] **Step 5: Commit**

```bash
git add "03-Dominios/Node/Frameworks e arquitetura/11 - DI - manual vs container.md"
git commit -m "feat(node-frameworks): add note 11 — DI manual vs container"
```

---

## Task 13: Nota 12 — Decision tree + cheatsheet

**Files:**
- Create: `03-Dominios/Node/Frameworks e arquitetura/12 - Decision tree + cheatsheet.md`

- [ ] **Step 1: Síntese das 11 notas anteriores**

Reler todas e extrair armadilhas + decision points. Síntese sem WebFetch.

- [ ] **Step 2: Frontmatter**

```yaml
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
```

- [ ] **Step 3: Escrever (300-450 linhas, PT-BR — estrutura tópica)**

- **TL;DR**: Cheatsheet de fechamento. Decision tree "qual framework pra qual contexto", tabela 4 frameworks × atributos, top 10+ armadilhas, vocabulário PT→EN, próximos galhos.

- **## Decision tree — qual framework pra qual contexto:**

  ```
  Qual o contexto?
  
  ├─ Microsserviço I/O-bound simples, time pequeno
  │   ├─ Performance importa? → Fastify
  │   └─ Conhecimento da equipe é Express? → Express
  │
  ├─ App enterprise, domínio complexo, time grande (10+ devs)
  │   ├─ Padrões corporativos (DI, módulos)? → NestJS
  │   └─ Time prefere arquitetura manual? → Express + Clean Architecture
  │
  ├─ API com schema bem definido + throughput alto
  │   └─ → Fastify (schema-first nativo)
  │
  ├─ Edge worker / serverless / multi-runtime
  │   └─ → Hono
  │
  └─ Migração de legacy
      ├─ Express legacy → manter Express, modernizar com TypeScript
      └─ Hapi/Sails → considerar Fastify ou NestJS
  ```

- **## Tabela 4 frameworks × atributos:**

  | Atributo | Express | NestJS | Fastify | Hono |
  |---|---|---|---|---|
  | Modelo | Middleware-based | Opinionated, DI | Schema-first | Edge-first |
  | DI built-in | Não | Sim | Não (plugins) | Não |
  | Validation | Manual ou zod/joi | class-validator ou zod | JSON Schema nativo | zod via lib |
  | Performance | Baseline | Similar Express | ~2-3× Express | Edge-optimized |
  | Maturidade | Madura (2010+) | Madura (2017+) | Madura (2017+) | Recente (2022+) |
  | Ecosystem | Maior | Médio (Nest-specific) | Médio | Pequeno (crescendo) |
  | Learning curve | Baixa | Alta (DI conceitos) | Média (schema) | Baixa |
  | Use case | Glue, prototype, microsservice | Enterprise, time grande | API throughput-focused | Edge, serverless |

- **## Top 10+ armadilhas:**

  1. Express 4 sem `asyncHandler` → erro async não capturado. Fix: Express 5 ou wrapper
  2. Express error middleware com 3 args → não é treated as error handler. Fix: 4 args `(err, req, res, next)`
  3. Mutating `req` em middleware sem documentar → ordem matters. Fix: docs claros + ordering convention
  4. NestJS provider scope wrong → request-scoped vira viral. Fix: SINGLETON default
  5. NestJS circular import → `forwardRef()`. Fix: refactor estrutura, evitar
  6. Fastify schema sem `additionalProperties: false` → propriedades extras passam. Fix: explicit
  7. Fastify plugin sem `fastify-plugin` quando deveria → encapsulation indesejada. Fix: `fp()` quando precisa expor
  8. Hono assumindo Node APIs em edge runtime → falha em CF Workers. Fix: usar APIs Web Standard (Fetch, etc.)
  9. Hono esquecer `await next()` → handler nunca roda. Fix: sempre await
  10. Stack trace exposto em prod → leak de info. Fix: sanitize em error handler global
  11. Container DI em app pequeno → complexidade sem benefício. Fix: manual DI até app crescer
  12. Clean Architecture em CRUD simples → over-engineering. Fix: pragmatismo
  13. Schema só em body, esquecer query/params → dados inválidos passam. Fix: validar todos inputs
  14. Misturar zod + class-validator no mesmo projeto → confuso. Fix: padronizar 1

- **## Vocabulário PT→EN consolidado** (mínimo 18 termos): middleware, error middleware, decorator, dependency injection (DI), provider, módulo (module), controller, escopo (scope), guard, interceptor, pipe, filter, lifecycle hook, schema-first, JSON Schema, type provider, plugin encapsulation, edge runtime, Fetch API native, onion middleware, Problem Details, RFC 7807, error taxonomy, composition root, ports and adapters, hexagonal architecture, dependency inversion.

- **## Próximos galhos:**
  - Pra **observar frameworks em produção**: galho 5 (Observability) — métricas de framework, profiling, logging estruturado
  - Pra **endurecer frameworks** contra ataques: galho 6 (Segurança) — Helmet, CORS, rate limiting, CSRF, input sanitization
  - Galhos 1, 2, 3 (Runtime, Paralelismo, Streams) — base já fechada

- **## Veja também** (12+ wikilinks): MOC, todas as 11 notas, Node.js (tronco), Runtime e Event Loop (galho 1), Paralelismo (galho 2), Streams (galho 3)

- [ ] **Step 4: Rubric adaptada** (estrutura tópica)

- [ ] **Step 5: Commit**

```bash
git add "03-Dominios/Node/Frameworks e arquitetura/12 - Decision tree + cheatsheet.md"
git commit -m "feat(node-frameworks): add note 12 — Decision tree + cheatsheet"
```

---

## Task 14: Pass final no MOC

**Files:**
- Modify: `03-Dominios/Node/Frameworks e arquitetura/Frameworks e arquitetura.md`

- [ ] **Step 1: Confirmar 12 notas existem**

```bash
ls "03-Dominios/Node/Frameworks e arquitetura/" | wc -l
# Esperado: 13
```

- [ ] **Step 2: Substituir placeholder de intro**

Substituir `(introdução curta — preencher na Task 14)` por:

```markdown
Este galho cobre **frameworks Node** — os 4 principais (Express, NestJS, Fastify, Hono) com trade-offs explícitos, patterns transversais (middleware, error handling Problem Details, schema validation), Clean Architecture em Node e DI manual vs container. Sem dogma framework-religioso — decision tree é matching, não ranking.

Pré-requisito: galho 1 ([[Runtime e Event Loop]]) — pressupõe entender event loop. Galho 3 ([[Streams]]) é referência cruzada (frameworks abstraem multipart/streaming via libs como busboy).

**Audiência primária:** dev senior em prep para entrevista internacional. Cada nota tem seção "Em entrevista" com frase pronta em inglês + vocabulário.

**Audiência secundária:** o mesmo dev decidindo framework/arquitetura para projeto novo, ou avaliando migração entre frameworks.
```

- [ ] **Step 3: Verificar 12 wikilinks**

```bash
ls "03-Dominios/Node/Frameworks e arquitetura/"
```

Confirmar 13 arquivos. Se algum nome diverge, BLOCKED.

- [ ] **Step 4: Verificar dataview path**

Confirmar `"03-Dominios/Node/Frameworks e arquitetura"`.

- [ ] **Step 5: Commit**

```bash
git add "03-Dominios/Node/Frameworks e arquitetura/Frameworks e arquitetura.md"
git commit -m "feat(node-frameworks): finalize MOC with all wikilinks and intro"
```

---

## Task 15: Poda do tronco (2 seções)

**Files:**
- Modify: `03-Dominios/JavaScript/Backend/Node.js.md`

- [ ] **Step 1: Localizar seções**

```bash
grep -nE "^### Frameworks|^### Error Handling" "03-Dominios/JavaScript/Backend/Node.js.md"
```

Esperado: 2 matches. Anotar números de linha. Identificar próxima seção após cada para definir boundary.

- [ ] **Step 2: Substituir `### Frameworks`**

```markdown
### Frameworks

> [!nota] Migrado para galho próprio
> Os 4 frameworks principais foram expandidos em [[Frameworks e arquitetura]] (galho 4). Veja em particular [[01 - Os 4 frameworks - Express, NestJS, Fastify, Hono]] (visão geral comparativa), [[02 - Express idiomático]] (Express moderno), [[03 - NestJS - fundamentos]] (DI + módulos), [[05 - Fastify - schema-first, plugins, performance]] (Fastify) e [[06 - Hono e edge runtimes]] (edge-first).
```

- [ ] **Step 3: Substituir `### Error Handling`**

```markdown
### Error Handling

> [!nota] Migrado para galho próprio
> Error handling estruturado (Problem Details RFC 7807) foi expandido em [[08 - Error handling estruturado]] no galho [[Frameworks e arquitetura]], com implementação em todos os 4 frameworks principais.
```

- [ ] **Step 4: Adicionar `[[Frameworks e arquitetura]]` no Veja também**

Como **quarto bullet** (após `[[Runtime e Event Loop]]`, `[[Paralelismo]]`, `[[Streams]]`):

```markdown
- [[Frameworks e arquitetura]] — galho 4 da trilha Node Senior; os 4 frameworks principais (Express, NestJS, Fastify, Hono), patterns transversais e arquitetura
```

- [ ] **Step 5: Atualizar `updated:`**

Mudar pra `updated: 2026-05-08`.

- [ ] **Step 6: Commit**

```bash
git add "03-Dominios/JavaScript/Backend/Node.js.md"
git commit -m "refactor(node): prune trunk Node.js.md, link to Frameworks e arquitetura branch"
```

---

## Task 16: MOC central + verificação final

**Files:**
- Modify: `03-Dominios/Node/index.md`

- [ ] **Step 1: Atualizar MOC central**

Adicionar como **quarto bullet** em "Galhos da trilha Node Senior":

```markdown
- [[Frameworks e arquitetura]] — galho 4: os 4 frameworks principais (Express, NestJS, Fastify, Hono), patterns transversais (middleware, error handling, validation), Clean Architecture e DI
```

Atualizar `updated: 2026-05-08`.

- [ ] **Step 2: Commit**

```bash
git add "03-Dominios/Node/index.md"
git commit -m "feat(node-frameworks): wire branch into central Node MOC"
```

- [ ] **Step 3: Verificação final**

```bash
# 1. 13 arquivos
ls "03-Dominios/Node/Frameworks e arquitetura/" | wc -l   # Esperado: 13

# 2. Todos publish: true
grep -l "publish: true" "03-Dominios/Node/Frameworks e arquitetura/"*.md | wc -l   # Esperado: 13

# 3. Total de linhas
wc -l "03-Dominios/Node/Frameworks e arquitetura/"*.md | tail -1

# 4. Tronco tem 11 callouts (5 G1 + 1 G2 + 4 G3 + 2 G4 = 12... wait, actually 4 + 1 + 4 + 2 = 11)
grep -c "Migrado para galho próprio" "03-Dominios/JavaScript/Backend/Node.js.md"
# Esperado: 11 (4 do galho 1 + 1 do galho 2 + 4 do galho 3 + 2 do galho 4)

# 5. MOC central com 4 galhos
grep -E "Runtime e Event Loop|Paralelismo|Streams|Frameworks e arquitetura" "03-Dominios/Node/index.md" | grep -v "^#" | wc -l
# Esperado: pelo menos 4
```

- [ ] **Step 4: Closing commit**

```bash
git commit --allow-empty -m "chore(node-frameworks): close branch Galho 4 — Frameworks e arquitetura

12 atomic notes + MOC published in 03-Dominios/Node/Frameworks e arquitetura/.
Trunk Node.js.md pruned (2 sections — Frameworks + Error Handling).
Central Node MOC updated. All acceptance criteria from
2026-05-08-node-frameworks-arquitetura-design.md met."
```

**Sem `Co-Authored-By`.**

- [ ] **Step 5: Quartz status**

CI workflow `.github/workflows/trigger-site-deploy.yaml`. Confirmar arquivo existe.

```bash
ls /home/josenaldo/repos/personal/codex-technomanticus/.github/workflows/
```

---

## Pós-execução

1. **Atualizar memória** se aprendizado novo apareceu (galho 4 tem peculiaridades — primeiro galho com 6 blocos, primeiro com NestJS dedicado, primeiro com versionamento de framework como concern)
2. **Revisar `2026-05-07-node-roadmap-design.md`** — após 4 galhos, política de poda está consolidada. Tronco está em ~474 linhas; pode ser hora de avaliar destino final
3. **Próximo galho** — escolher entre Galho 5 (Observability) ou Galho 6 (Segurança)

---

## Self-review do plano

- **Spec coverage:** 12 notas do spec seção 5 cobertas por Tasks 2-13 ✓; MOC criado em Task 1, finalizado em Task 14 ✓; 5 rotas alternativas ✓; 2 seções de poda em Task 15 ✓; MOC central em Task 16 ✓; critérios em Task 16 step 3 ✓; bibliografia centralizada ✓; restrição de fabricação ✓.

- **Placeholder scan:** apenas `(introdução curta — preencher na Task 14)` que é placeholder INTENCIONAL com instrução explícita ✓.

- **Type consistency:** títulos batem entre Tasks 1, 2-13, 14, 15. Wikilinks consistentes ✓.

- **Coesão com galhos anteriores:** wikilinks pra `[[Runtime e Event Loop]]`, `[[Paralelismo]]`, `[[Streams]]`, `[[Node.js]]` aparecem nas notas certas ✓.
