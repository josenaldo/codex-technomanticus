# Galho 6 — ORMs e banco de dados: Plano de Execução

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Criar 10 notas atômicas + 1 MOC em `03-Dominios/Node/ORMs e banco de dados/` cobrindo os principais ORMs do ecossistema Node.js (Sequelize, Prisma, TypeORM, Drizzle), padrões de banco de dados (N+1, migrations, transações, paginação), e podar as seções correspondentes do tronco `Node.js.md`. Contexto: maio de 2026 — Prisma v6+, Drizzle ORM consolidado, Node 22 LTS, TypeScript nativo.

**Architecture:** Cada nota é um arquivo Markdown independente em `03-Dominios/Node/ORMs e banco de dados/`. O MOC serve como ponto de entrada com rotas alternativas. O tronco é podado ao final com callouts de migração.

**Tech Stack:** Obsidian Flavored Markdown, frontmatter YAML, wikilinks `[[]]`, callouts `[!abstract]`, dataview query no MOC. ORMs cobertos: Sequelize v7, Prisma v6, TypeORM v0.3, Drizzle ORM v0.30+. Runtime: Node 22 LTS + TypeScript nativo. Bancos: PostgreSQL (primário), MySQL/SQLite (menção).

---

## REGRAS CRÍTICAS PARA O AGENTE EXECUTOR

> ⚠️ **ONE commit per note, NOT bundled.** Cada task = 1 nota = 1 commit dedicado. Commitar múltiplas notas em 1 commit é violação do workflow.
>
> ⚠️ **Nenhuma nota abaixo do mínimo de linhas declarado.** Abaixo do mínimo a nota perde profundidade para o nível senior exigido. O mínimo é piso, não teto.
>
> ⚠️ **"Em entrevista" obrigatoriamente 3+ sentenças em inglês interligadas.** Proibido one-liner.
>
> ⚠️ **Sem Co-Authored-By em commits.** Mensagens seguem o formato: `feat(node/g6): add <número> - <título>`.
>
> ⚠️ **Self-check antes de cada commit** — ver checklist na seção Self-Check abaixo.
>
> ⚠️ **Informações atualizadas para maio de 2026:** Prisma v6 (não v5), Drizzle v0.30+, Node 22 LTS, TypeScript 5.5+. Nunca referenciar APIs deprecadas como default atual.

## Self-Check (executar antes de cada commit de nota)

```
[ ] Frontmatter completo: title, created, updated, type, status, progresso, publish, tags, aliases (quando aplicável)
[ ] TL;DR callout [!abstract] presente com conteúdo denso (> 3 linhas)
[ ] Contagem de linhas >= mínimo declarado para esta nota
[ ] "Em entrevista" tem 3+ sentenças em inglês (não one-liner)
[ ] "Vocabulário PT→EN" tem >= 6 termos com tradução
[ ] Cada armadilha tem: (a) descrição + (b) código-problema + (c) fix
[ ] "Como funciona" tem >= 3 subsecções (headings ###)
[ ] Número de exemplos de código >= mínimo declarado para esta nota
[ ] Wikilinks para [[Node.js]] e [[ORMs e banco de dados]] (MOC) presentes
[ ] "Fontes" com pelo menos 1 link oficial da ferramenta principal
```

---

## Estrutura de arquivos

**Criar:**

```
03-Dominios/Node/ORMs e banco de dados/
├── ORMs e banco de dados.md              (MOC — Task 1)
├── 01 - Panorama de ORMs.md              (Task 2)
├── 02 - Sequelize - queries e associações.md   (Task 3)
├── 03 - Prisma - schema-first e type safety.md (Task 4)
├── 04 - TypeORM - decorators ao estilo JPA.md  (Task 5)
├── 05 - Drizzle - ORM lightweight e type-safe.md (Task 6)
├── 06 - N+1 queries - detecção e DataLoader.md (Task 7)
├── 07 - Migrations e versionamento de schema.md (Task 8)
├── 08 - Transações - gerenciamento manual vs automático.md (Task 9)
├── 09 - Paginação - offset, cursor e keyset.md (Task 10)
└── 10 - Cheatsheet e decision tree de ORMs.md  (Task 11)
```

**Modificar:**

```
03-Dominios/JavaScript/Backend/Node.js.md     (poda: 2 seções → callouts — Task 12)
03-Dominios/Node/index.md                     (adicionar galho 6 — Task 12)
```

---

## Task 1: MOC — ORMs e banco de dados

**Files:**
- Create: `03-Dominios/Node/ORMs e banco de dados/ORMs e banco de dados.md`

**Commit:** `feat(node/g6): add MOC - ORMs e banco de dados`

- [ ] **Step 1: Criar o arquivo MOC**

Criar `03-Dominios/Node/ORMs e banco de dados/ORMs e banco de dados.md` com:

```markdown
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
```

Conteúdo do MOC deve incluir:

1. **Callout `[!abstract] TL;DR`** cobrindo o galho (4+ linhas): o que é um ORM, os 4 principais do ecossistema Node (Sequelize, Prisma, TypeORM, Drizzle) e seus posicionamentos em 2026, e os padrões críticos (N+1, migrations, transações, paginação).

2. **Seção `## Sobre este galho`** com:
   - Descrição clara do escopo (2-3 parágrafos)
   - Pré-requisitos: `[[Frameworks e arquitetura]]` (galho 4), `[[Node.js]]` (tronco)
   - Audiência primária: dev senior prep entrevista internacional
   - Audiência secundária: dev integrando banco em API Node existente

3. **Seção `## Comece por aqui — trilha completa (10 notas)`** organizada em blocos:
   - **Bloco A — Visão geral**: `[[01 - Panorama de ORMs]]`
   - **Bloco B — Os 4 ORMs**: notas 02-05
   - **Bloco C — Padrões críticos**: notas 06-09
   - **Bloco D — Fechamento**: `[[10 - Cheatsheet e decision tree de ORMs]]`

4. **Seção `## Rotas alternativas`** com pelo menos 3 rotas:
   - Rota entrevista (foco nos 4 ORMs + N+1 + decision tree)
   - Rota migrations (07 → 08 → 10)
   - Rota performance/N+1 (06 → 09 → 10)
   - Rota onboarding Prisma (03 → 07 → 08 → 09)

5. **Seção `## Todas as notas`** com query dataview:
   ```dataview
   TABLE status, updated
   FROM "03-Dominios/Node/ORMs e banco de dados"
   WHERE type = "concept"
   SORT file.name ASC
   ```

6. **Seção `## Veja também`** com wikilinks para: `[[Node.js]]`, `[[Frameworks e arquitetura]]`, galhos anteriores, `[[03-Dominios/Node/index|Node.js (MOC central)]]`.

**Mínimo de linhas:** 80

---

## Task 2: Nota 01 — Panorama de ORMs

**Files:**
- Create: `03-Dominios/Node/ORMs e banco de dados/01 - Panorama de ORMs.md`

**Commit:** `feat(node/g6): add 01 - Panorama de ORMs`

**Frontmatter:**
```yaml
title: "Panorama de ORMs"
created: 2026-05-10
updated: 2026-05-10
type: concept
status: seedling
progresso: andamento
tags:
  - node
  - orm
  - sequelize
  - prisma
  - typeorm
  - drizzle
publish: false
```

**Conteúdo mínimo (340+ linhas):**

1. **Callout `[!abstract] TL;DR`** (4+ linhas): Os 4 ORMs e seus posicionamentos em 2026 — Sequelize (battle-tested, callback-era), Prisma (schema-first, DX excelente, v6 estável), TypeORM (decorators, similar ao JPA, popular em NestJS), Drizzle (lightweight, SQL-first, type-safe, favorito de 2024-2025).

2. **Seção `## O que é`** explicando:
   - O que é um ORM e para que serve
   - A diferença entre ORM, query builder e SQL puro
   - Por que escolher um ORM em Node.js

3. **Seção `## Como funciona`** com subsecções:

   ### Eixos de comparação
   Tabela Markdown comparando os 4 ORMs nos eixos:
   - Paradigma (schema-first, code-first, SQL-first)
   - Type safety (gerada, manual, nativa)
   - Migration strategy
   - Performance overhead
   - Suporte a edge runtimes (Cloudflare Workers, Vercel Edge)
   - Maturidade/popularidade em 2026
   - Ideal para (projetos novos, legacy, NestJS, edge)

   ### Sequelize
   Parágrafo + snippets:
   - Surgiu na era do callback, amadureceu com Promises
   - v7 (2025): melhor suporte a TypeScript, removed deprecated methods
   - Ainda popular em projetos legacy e empresas que não migraram
   - Exemplo de model + query básica

   ### Prisma
   Parágrafo + snippets:
   - v6 (2025): suporte a edge runtimes, Prisma Accelerate GA, melhor performance
   - Schema declarativo em `schema.prisma` → gera types TypeScript automaticamente
   - Prisma Client, Prisma Migrate, Prisma Studio
   - Exemplo de schema.prisma + query

   ### TypeORM
   Parágrafo + snippets:
   - Decorators style à la JPA/Hibernate
   - Integração nativa com NestJS (`@nestjs/typeorm`)
   - v0.3+ com melhorias de type safety
   - Exemplo de Entity + Repository

   ### Drizzle ORM
   Parágrafo + snippets:
   - SQL-first: você escreve TypeScript que parece SQL
   - Zero-runtime overhead: sem proxies, sem magic
   - Excelente para edge runtimes
   - Drizzle Studio (similar ao Prisma Studio)
   - Exemplo de schema + query

4. **Seção `## Quando usar`** com decision tree textual:
   - NestJS enterprise → TypeORM ou Prisma
   - Edge runtime (Cloudflare Workers) → Drizzle
   - Projeto legacy com Sequelize → upgrade v7, não migrar
   - Novo projeto Node.js → Prisma v6 (DX) ou Drizzle (performance/edge)
   - Equipe familiarizada com SQL → Drizzle
   - Equipe vinda do Java/Spring → TypeORM

5. **Seção `## Armadilhas comuns`** (3+ armadilhas):
   - Escolher ORM por popularidade e não por fit (edge vs server)
   - Assumir que Prisma gerado é always type-safe (raw queries não são)
   - TypeORM `synchronize: true` em produção

6. **Seção `## Em entrevista`** com:
   - Parágrafo em inglês (4+ sentenças) sobre como escolher entre os 4 ORMs
   - Vocabulário PT→EN (8+ termos): schema, migration, eager loading, lazy loading, query builder, type safety, code-first, schema-first, etc.

7. **Seção `## Fontes`** com links para docs oficiais de todos os 4 ORMs.

8. **Seção `## Veja também`** com wikilinks para as 4 notas individuais + MOC.

**Mínimo de código:** 6 snippets TypeScript (ao menos 1 por ORM + tabela comparativa)

---

## Task 3: Nota 02 — Sequelize — queries e associações

**Files:**
- Create: `03-Dominios/Node/ORMs e banco de dados/02 - Sequelize - queries e associações.md`

**Commit:** `feat(node/g6): add 02 - Sequelize - queries e associações`

**Frontmatter:**
```yaml
title: "Sequelize - queries e associações"
created: 2026-05-10
updated: 2026-05-10
type: concept
status: seedling
progresso: andamento
tags:
  - node
  - orm
  - sequelize
  - postgres
  - banco-de-dados
publish: false
```

**Conteúdo mínimo (340+ linhas):**

1. **Callout `[!abstract] TL;DR`** (4+ linhas): Sequelize v7, ORM battle-tested, suporte TypeScript melhorado, modelo baseado em `define`/decorators, associations (HasMany, BelongsTo, BelongsToMany), eager loading com `include` para evitar N+1. Em 2026 ainda relevante para projetos existentes mas Prisma/Drizzle são preferidos para novos projetos.

2. **Seção `## O que é`**: Sequelize como ORM Node.js mais antigo (2011), suporte a PostgreSQL, MySQL, MariaDB, SQLite, SQL Server.

3. **Seção `## Como funciona`** com subsecções:

   ### Definição de models
   - Model com `sequelize-typescript` (decorators)
   - Tipos de colunas: `DataTypes.STRING`, `DataTypes.INTEGER`, `DataTypes.JSONB`, `DataTypes.DATE`, etc.
   - Validações inline (`@Column({ validate: { isEmail: true } })`)

   ### Associations (relacionamentos)
   - `@HasMany`, `@BelongsTo`, `@HasOne`, `@BelongsToMany`
   - Como configurar foreign keys
   - Associações polimórficas (quando evitar)

   ### Queries CRUD
   - `findAll`, `findOne`, `findByPk`, `findOrCreate`
   - `create`, `update`, `destroy`, `upsert`
   - Operadores (`Op.eq`, `Op.gte`, `Op.like`, `Op.in`, `Op.or`)
   - Ordenação, limit, offset

   ### Eager loading e include
   - `include: [Model]` básico
   - `include` com `where`, `attributes`, `required` (INNER vs LEFT JOIN)
   - `include` aninhado (3 níveis max antes de problema de performance)
   - Evitar N+1 com eager loading (ponte para Task 7)

   ### Transações
   - `sequelize.transaction(async (t) => { ... })`
   - Managed vs unmanaged transactions
   - Ponteiro para Task 9

   ### Hooks e lifecycle
   - `beforeCreate`, `afterCreate`, `beforeUpdate`, `beforeDestroy`
   - Caso de uso: hash de senha, audit log

4. **Seção `## Quando usar`**: projetos legacy, equipes que já conhecem, quando não compensa migrar.

5. **Seção `## Armadilhas comuns`** (4+ armadilhas com código):
   - Lazy loading acidental (N+1 — com código antes/depois)
   - `include` sem `required: false` gerando INNER JOIN silencioso
   - `destroy()` sem `where` deletando tudo
   - `Op.like` em produção com pattern `%texto%` (full scan)
   - `timestamps: false` + `paranoid: true` conflito

6. **Seção `## Em entrevista`**: 4+ sentenças em inglês sobre quando usar Sequelize vs alternativas, eager loading para evitar N+1, estratégia de migrations.

7. **Seção `## Vocabulário PT→EN`** (8+ termos): associação, carregamento antecipado, carregamento preguiçoso, gancho de ciclo de vida, transação gerenciada, etc.

8. **Seção `## Fontes`**: links para docs oficiais Sequelize v7 + sequelize-typescript.

**Mínimo de código:** 8 snippets TypeScript

---

## Task 4: Nota 03 — Prisma — schema-first e type safety

**Files:**
- Create: `03-Dominios/Node/ORMs e banco de dados/03 - Prisma - schema-first e type safety.md`

**Commit:** `feat(node/g6): add 03 - Prisma - schema-first e type safety`

**Frontmatter:**
```yaml
title: "Prisma - schema-first e type safety"
created: 2026-05-10
updated: 2026-05-10
type: concept
status: seedling
progresso: andamento
tags:
  - node
  - orm
  - prisma
  - type-safety
  - banco-de-dados
publish: false
```

**Conteúdo mínimo (380+ linhas):**

1. **Callout `[!abstract] TL;DR`** (4+ linhas): Prisma v6 em 2026 — schema declarativo em `schema.prisma`, Prisma Client gerado automaticamente com types TypeScript precisos, Prisma Migrate para versionamento, Prisma Studio para inspeção visual. Suporte a edge runtimes com Prisma Accelerate. Melhor DX entre os ORMs Node, curva de aprendizado menor para devs TypeScript.

2. **Seção `## O que é`**: Prisma como toolkit de banco de dados (não só ORM) — três camadas: Prisma Client, Prisma Migrate, Prisma Studio.

3. **Seção `## Como funciona`** com subsecções:

   ### Schema Prisma
   - Sintaxe de `schema.prisma`: `datasource`, `generator`, `model`, `enum`
   - Tipos de campo: `String`, `Int`, `Boolean`, `DateTime`, `Json`, `Bytes`
   - Modificadores: `?` (opcional), `[]` (array)
   - Relações: `@relation`, campos de relação explícitos
   - Exemplo completo com 2-3 models relacionados

   ### Prisma Client — CRUD
   - `findMany`, `findFirst`, `findUnique`, `findUniqueOrThrow`
   - `create`, `createMany`, `update`, `updateMany`, `upsert`, `delete`, `deleteMany`
   - `select` vs `include` — diferença importante
   - `where` com filtros compostos (`AND`, `OR`, `NOT`)
   - `orderBy`, `take`, `skip`, `cursor`

   ### Relações e includes
   - `include` com relações aninhadas
   - `select` para projection granular (evitar over-fetching)
   - `_count` para contar registros relacionados sem carregar
   - `connect`/`disconnect`/`set` para gerenciar relações no `create`/`update`

   ### Prisma Migrate
   - `prisma migrate dev` vs `prisma migrate deploy`
   - Migration files gerados automaticamente
   - Squash de migrations antigas
   - `prisma db push` para prototipagem (sem migration files)
   - Diferença entre `dev` e `prod` workflow

   ### Raw queries e escape de type safety
   - `$queryRaw` e `$executeRaw` para SQL literal
   - `Prisma.sql` template tag para evitar SQL injection
   - Quando usar raw: queries complexas, window functions, CTEs

   ### Prisma Accelerate (v6)
   - Connection pooling global para edge
   - Cache em CDN para queries lentas
   - Quando faz sentido ativar

4. **Seção `## Quando usar`**: novo projeto com TypeScript, edge runtime, equipe que valoriza DX, migrations versionadas automáticas.

5. **Seção `## Armadilhas comuns`** (4+ armadilhas com código):
   - `findMany` sem paginação em tabelas grandes (OOM)
   - `include` aninhado profundo causando N+1 (explicar o caso)
   - `$queryRaw` com interpolação string (SQL injection)
   - `prisma migrate deploy` em dev (nunca em prod sem teste)
   - Não versionar `schema.prisma` no git (sempre versionar)

6. **Seção `## Em entrevista`**: 4+ sentenças em inglês sobre Prisma, schema-first, type safety gerada, vs TypeORM/Drizzle.

7. **Seção `## Vocabulário PT→EN`** (8+ termos).

8. **Seção `## Fontes`**: links para docs Prisma v6 + changelog de breaking changes v5→v6.

**Mínimo de código:** 10 snippets (prisma schema + TypeScript)

---

## Task 5: Nota 04 — TypeORM — decorators ao estilo JPA

**Files:**
- Create: `03-Dominios/Node/ORMs e banco de dados/04 - TypeORM - decorators ao estilo JPA.md`

**Commit:** `feat(node/g6): add 04 - TypeORM - decorators ao estilo JPA`

**Frontmatter:**
```yaml
title: "TypeORM - decorators ao estilo JPA"
created: 2026-05-10
updated: 2026-05-10
type: concept
status: seedling
progresso: andamento
tags:
  - node
  - orm
  - typeorm
  - nestjs
  - banco-de-dados
publish: false
```

**Conteúdo mínimo (320+ linhas):**

1. **Callout `[!abstract] TL;DR`** (4+ linhas): TypeORM com decorators (`@Entity`, `@Column`, `@OneToMany`), estilo similar ao JPA/Hibernate — familiar para devs Java. Integração nativa com NestJS via `@nestjs/typeorm`. Repository pattern built-in. Em 2026, escolha válida para projetos NestJS enterprise mas Prisma v6 compete no mesmo espaço com melhor DX.

2. **Seção `## O que é`**: TypeORM origem, motivação (trazer JPA para Node.js), posição em 2026.

3. **Seção `## Como funciona`** com subsecções:

   ### Entities e decorators
   - `@Entity`, `@Column`, `@PrimaryGeneratedColumn`, `@CreateDateColumn`, `@UpdateDateColumn`
   - `@Index`, `@Unique`
   - Tipos de coluna TypeORM e mapeamento para DB
   - Exemplo de entity completa com PostgreSQL

   ### Relacionamentos
   - `@OneToOne`, `@OneToMany`, `@ManyToOne`, `@ManyToMany`
   - `@JoinColumn`, `@JoinTable`
   - Diferença entre owning side e inverse side
   - Lazy vs eager loading (`{ eager: true }` vs relations no find)

   ### Repository pattern
   - `getRepository(Entity)` vs `DataSource.manager`
   - Custom repositories: `extend Repository<Entity>`
   - `find`, `findOne`, `findOneBy`, `save`, `remove`, `delete`
   - Query options: `where`, `order`, `take`, `skip`, `relations`

   ### QueryBuilder
   - Quando usar QueryBuilder vs find methods
   - `createQueryBuilder('alias').leftJoinAndSelect(...).where(...).getMany()`
   - Subqueries, CTEs (quando fugir para QueryBuilder)
   - Contagem com `getCount`

   ### Integração com NestJS
   - `TypeOrmModule.forRoot(config)` e `TypeOrmModule.forFeature([Entity])`
   - `@InjectRepository(Entity)` nos services
   - DataSource vs EntityManager

   ### Migrations com TypeORM
   - `typeorm migration:generate` e `typeorm migration:run`
   - Diferença de `synchronize: true` (dev) vs migrations (prod)

4. **Seção `## Quando usar`**: NestJS enterprise, equipe vindo de Java, projetos que precisam do Repository pattern explícito.

5. **Seção `## Armadilhas comuns`** (4+ armadilhas com código):
   - `synchronize: true` em produção (NUNCA)
   - N+1 silencioso com lazy loading
   - `save()` fazendo SELECT antes de INSERT (use `insert()` para bulk)
   - Circular dependency entre entities

6. **Seção `## Em entrevista`**: 4+ sentenças em inglês comparando TypeORM com JPA, quando preferir sobre Prisma, pattern com NestJS.

7. **Seção `## Vocabulário PT→EN`** (8+ termos).

8. **Seção `## Fontes`**: links TypeORM v0.3 docs + NestJS TypeORM guide.

**Mínimo de código:** 8 snippets TypeScript

---

## Task 6: Nota 05 — Drizzle — ORM lightweight e type-safe

**Files:**
- Create: `03-Dominios/Node/ORMs e banco de dados/05 - Drizzle - ORM lightweight e type-safe.md`

**Commit:** `feat(node/g6): add 05 - Drizzle - ORM lightweight e type-safe`

**Frontmatter:**
```yaml
title: "Drizzle - ORM lightweight e type-safe"
created: 2026-05-10
updated: 2026-05-10
type: concept
status: seedling
progresso: andamento
tags:
  - node
  - orm
  - drizzle
  - type-safety
  - edge
  - banco-de-dados
publish: false
```

**Conteúdo mínimo (320+ linhas):**

1. **Callout `[!abstract] TL;DR`** (4+ linhas): Drizzle ORM v0.30+ — SQL-first, zero overhead de runtime, TypeScript-native, excelente para edge runtimes (Cloudflare Workers, Vercel Edge). Cresceu muito em adoção em 2024-2025. Drizzle Kit para migrations. Drizzle Studio para inspeção. Preferido quando performance e edge são prioridades.

2. **Seção `## O que é`**: Drizzle como "SQL com superpowers TypeScript" — filosofia SQL-first vs ORM-first.

3. **Seção `## Como funciona`** com subsecções:

   ### Schema definition
   - `pgTable`, `text`, `integer`, `boolean`, `timestamp`, `jsonb`, `uuid`
   - `primaryKey`, `notNull`, `default`, `references` para FK
   - Exemplo de schema completo para PostgreSQL com 2-3 tables

   ### Queries — select
   - `db.select().from(table).where(eq(table.col, val)).limit(n)`
   - `leftJoin`, `innerJoin` explícitos (diferença de outros ORMs)
   - Operadores: `eq`, `ne`, `gt`, `lt`, `gte`, `lte`, `and`, `or`, `inArray`, `like`, `ilike`, `isNull`
   - `orderBy`, `groupBy`, `having`

   ### Queries — mutations
   - `db.insert(table).values({ ... })` e `onConflictDoUpdate`
   - `db.update(table).set({ ... }).where(...)`
   - `db.delete(table).where(...)`
   - Retornando valores com `.returning()`

   ### Relations (Drizzle ORM relations API)
   - `relations()` para definir relações sem FK explícita
   - `db.query.table.findMany({ with: { related: true } })` — eager loading
   - Diferença entre SQL join e relations API

   ### Drizzle Kit — migrations
   - `drizzle-kit generate` → gera SQL migrations
   - `drizzle-kit migrate` → aplica
   - `drizzle-kit studio` → Drizzle Studio

   ### Edge runtimes
   - Por que Drizzle funciona em edge (sem `net` module)
   - `neon-serverless`, `@libsql/client` para Turso, `postgres.js`
   - Exemplo com Cloudflare Workers + Neon

4. **Seção `## Quando usar`**: edge runtimes, performance crítica, equipe que gosta de SQL, projetos novos com TypeScript.

5. **Seção `## Armadilhas comuns`** (3+ armadilhas com código):
   - Confundir SQL joins com relations API (diferentes trade-offs)
   - `.all()` vs `.get()` — diferença sutil
   - Usar Drizzle sem connection pooling em serverless (usar pool externo)

6. **Seção `## Em entrevista`**: 4+ sentenças em inglês sobre Drizzle vs Prisma, SQL-first philosophy, edge runtime advantage.

7. **Seção `## Vocabulário PT→EN`** (8+ termos).

8. **Seção `## Fontes`**: links para Drizzle docs + Drizzle Kit docs.

**Mínimo de código:** 8 snippets TypeScript

---

## Task 7: Nota 06 — N+1 queries — detecção e DataLoader

**Files:**
- Create: `03-Dominios/Node/ORMs e banco de dados/06 - N+1 queries - detecção e DataLoader.md`

**Commit:** `feat(node/g6): add 06 - N+1 queries - detecção e DataLoader`

**Frontmatter:**
```yaml
title: "N+1 queries - detecção e DataLoader"
created: 2026-05-10
updated: 2026-05-10
type: concept
status: seedling
progresso: andamento
tags:
  - node
  - orm
  - performance
  - n-mais-um
  - dataloader
  - graphql
  - banco-de-dados
publish: false
```

**Conteúdo mínimo (340+ linhas):**

1. **Callout `[!abstract] TL;DR`** (4+ linhas): N+1 é o problema de performance mais comum com ORMs. Ocorre quando buscamos N entidades e fazemos 1 query adicional por entidade para buscar relacionamentos. Solução: eager loading (`include`/`join`) para REST, DataLoader para GraphQL (batching + deduplication). Todos os ORMs sofrem; a solução varia.

2. **Seção `## O que é`**: definição precisa de N+1, por que é silencioso, como identificar nos logs de query.

3. **Seção `## Como funciona`** com subsecções:

   ### O problema — exemplo em cada ORM
   - Sequelize N+1 com lazy loading
   - Prisma N+1 (mais difícil de ocorrer, mas possível com relações aninhadas em loops)
   - TypeORM N+1 com lazy relations
   - Drizzle: por ser SQL-first, N+1 é mais explícito

   ### Solução com eager loading
   - Sequelize: `include: [{ model: Related }]` (gera JOIN)
   - Prisma: `include: { related: true }` vs `select: { related: { select: {...} } }`
   - TypeORM: `relations: ['related']` no find, ou QueryBuilder com `leftJoinAndSelect`
   - Drizzle: `leftJoin` explícito no SQL

   ### DataLoader pattern
   - O que é DataLoader (Facebook/Meta) — batch + deduplicate
   - Como instanciar: `new DataLoader(async (ids) => { ... })`
   - Regra dos 3: o batch function deve retornar array na mesma ordem e tamanho dos IDs
   - Exemplo completo: GraphQL resolver com DataLoader
   - DataLoader por request (instanciar no contexto, não como singleton)
   - DataLoader com Prisma e com TypeORM

   ### Detecção em produção
   - Ativar query logging nos ORMs
   - Sequelize: `logging: console.log`
   - Prisma: `log: ['query']`
   - TypeORM: `logging: 'all'`
   - Drizzle: `logger: true`
   - OpenTelemetry traces para detectar queries repetidas (ponte para galho 5)

4. **Seção `## Quando usar`** (contexto de escolha de estratégia):
   - REST: sempre eager loading
   - GraphQL: DataLoader é obrigatório em resolvers de relações
   - Batch jobs: eager loading com chunks (10k registros de cada vez)

5. **Seção `## Armadilhas comuns`** (4+ armadilhas com código):
   - DataLoader como singleton global (vazamento entre requests)
   - Eager loading em tabela com milhões de registros (OOM)
   - `include` circular causando stack overflow
   - DataLoader batch function retornando na ordem errada (bug silencioso)

6. **Seção `## Em entrevista`**: 4+ sentenças em inglês sobre N+1, como detectar, DataLoader pattern, eager loading trade-offs.

7. **Seção `## Vocabulário PT→EN`** (8+ termos).

8. **Seção `## Fontes`**: link para docs do DataLoader (npm/GitHub) + artigos sobre N+1 em cada ORM.

**Mínimo de código:** 8 snippets TypeScript (incluindo DataLoader completo)

---

## Task 8: Nota 07 — Migrations e versionamento de schema

**Files:**
- Create: `03-Dominios/Node/ORMs e banco de dados/07 - Migrations e versionamento de schema.md`

**Commit:** `feat(node/g6): add 07 - Migrations e versionamento de schema`

**Frontmatter:**
```yaml
title: "Migrations e versionamento de schema"
created: 2026-05-10
updated: 2026-05-10
type: concept
status: seedling
progresso: andamento
tags:
  - node
  - orm
  - migrations
  - schema
  - banco-de-dados
publish: false
```

**Conteúdo mínimo (320+ linhas):**

1. **Callout `[!abstract] TL;DR`** (4+ linhas): Migrations são o controle de versão do schema do banco. Cada ORM tem sua abordagem: Sequelize CLI, Prisma Migrate, TypeORM CLI, Drizzle Kit. Regra fundamental: nunca usar `synchronize: true` em produção. Em 2026, Prisma Migrate é considerado o mais ergonômico; para multi-ORM, Flyway/Liquibase são alternativas portáveis.

2. **Seção `## O que é`**: o problema que migrations resolve, analogia com `git` para código.

3. **Seção `## Como funciona`** com subsecções:

   ### Migrations com Sequelize
   - `sequelize-cli`: `npx sequelize migration:generate`, `migrate`, `undo`
   - Estrutura de um arquivo de migration (up/down)
   - Tabela `SequelizeMeta` como controle
   - Seeder vs migration

   ### Migrations com Prisma Migrate
   - `prisma migrate dev` (dev + shadow database)
   - `prisma migrate deploy` (prod, sem shadow)
   - `prisma migrate reset` (dev only — NUNCA em prod)
   - Estrutura da pasta `prisma/migrations/`
   - Baseline de schema existente (`prisma migrate baseline`)

   ### Migrations com TypeORM
   - `typeorm migration:generate -n NomeMigration`
   - `typeorm migration:run` e `migration:revert`
   - `MigrationInterface` com `up()` e `down()`
   - Tabela `migrations` no banco

   ### Migrations com Drizzle Kit
   - `drizzle-kit generate:pg` (ou mysql/sqlite)
   - `drizzle-kit migrate`
   - Pasta `drizzle/` com SQL files gerados
   - Sem shadow database — gera SQL puro

   ### Workflow de CI/CD
   - Migrations em pipeline: rodar antes do deploy (não no startup)
   - Rollback de migration em produção (quando é seguro)
   - Zero-downtime migrations: additive-only (add column nullable, backfill, add NOT NULL)
   - Estratégia expand-contract para colunas renomeadas

4. **Seção `## Quando usar`** (comparativo de abordagens):
   - Novo projeto TypeScript: Prisma Migrate
   - NestJS + TypeORM: TypeORM CLI integrado
   - Legacy Sequelize: continuar com Sequelize CLI
   - Edge + Drizzle: Drizzle Kit
   - Multi-banco/multi-linguagem: Flyway

5. **Seção `## Armadilhas comuns`** (4+ armadilhas com código):
   - `synchronize: true` em produção (NUNCA — listar consequências)
   - Migration que adiciona coluna NOT NULL sem default em tabela com dados
   - Não versionar migration files no git
   - Rodar migrations no startup da aplicação (race condition em multi-instance)
   - Squash de migrations em produção (sem coordenação prévia)

6. **Seção `## Em entrevista`**: 4+ sentenças em inglês sobre migration strategy, zero-downtime, expand-contract pattern.

7. **Seção `## Vocabulário PT→EN`** (8+ termos).

8. **Seção `## Fontes`**: links para docs de migrations de cada ORM + artigo sobre zero-downtime migrations.

**Mínimo de código:** 6 snippets (migration files + comandos CLI)

---

## Task 9: Nota 08 — Transações — gerenciamento manual vs automático

**Files:**
- Create: `03-Dominios/Node/ORMs e banco de dados/08 - Transações - gerenciamento manual vs automático.md`

**Commit:** `feat(node/g6): add 08 - Transações - gerenciamento manual vs automático`

**Frontmatter:**
```yaml
title: "Transações - gerenciamento manual vs automático"
created: 2026-05-10
updated: 2026-05-10
type: concept
status: seedling
progresso: andamento
tags:
  - node
  - orm
  - transacoes
  - acid
  - banco-de-dados
publish: false
```

**Conteúdo mínimo (320+ linhas):**

1. **Callout `[!abstract] TL;DR`** (4+ linhas): Transações garantem ACID — Atomicity, Consistency, Isolation, Durability. Em ORMs Node: Sequelize usa callbacks ou `sequelize.transaction()`, Prisma usa `prisma.$transaction()` (interativa ou batch), TypeORM usa `queryRunner.startTransaction()`, Drizzle usa `db.transaction()`. O erro mais perigoso: fazer operações parciais fora de transação em processos que devem ser atômicos.

2. **Seção `## O que é`**: ACID, quando transações são necessárias, custo de locks.

3. **Seção `## Como funciona`** com subsecções:

   ### Níveis de isolamento
   - Read Uncommitted, Read Committed, Repeatable Read, Serializable
   - PostgreSQL default: Read Committed
   - Quando subir o nível (e o custo)
   - Fenômenos: dirty read, non-repeatable read, phantom read

   ### Transações com Sequelize
   - Managed transactions (callback): `sequelize.transaction(async (t) => { ... })`
   - Unmanaged transactions: `const t = await sequelize.transaction(); try { ... await t.commit() } catch { await t.rollback() }`
   - Passar `{ transaction: t }` em todas as queries dentro da transação
   - Savepoints

   ### Transações com Prisma
   - Interactive transactions: `prisma.$transaction(async (tx) => { ... })` — tx é um Prisma Client isolado
   - Sequential transactions (batch): `prisma.$transaction([query1, query2])` — mais rápido, sem dependências
   - Timeout de transação: `{ timeout: 5000 }`
   - `maxWait` para espera de connection
   - Prisma v6: melhorias no retry de transações

   ### Transações com TypeORM
   - `queryRunner`: `await queryRunner.startTransaction()`, `commitTransaction()`, `rollbackTransaction()`
   - `@Transaction()` decorator (deprecated em v0.3+)
   - DataSource transaction callback

   ### Transações com Drizzle
   - `db.transaction(async (tx) => { ... })`
   - Nested transactions (savepoints)
   - Rollback explícito com `tx.rollback()`

   ### Padrões transacionais
   - Outbox pattern: persistir evento + estado na mesma transação
   - Saga pattern: transações distribuídas (quando transação única não é possível)
   - Pessimistic vs optimistic locking

4. **Seção `## Quando usar`**: operações que devem ser atômicas (debitar + creditar, criar pedido + baixar estoque).

5. **Seção `## Armadilhas comuns`** (4+ armadilhas com código):
   - Esquecer de passar `{ transaction: t }` em Sequelize (operação fora da transação)
   - Prisma interactive transaction com timeout muito curto
   - Deadlock silencioso (detectar e resolver)
   - Transação aberta muito longa bloqueando outras operações
   - Fazer HTTP calls dentro de uma transação (lock mantido durante I/O)

6. **Seção `## Em entrevista`**: 4+ sentenças em inglês sobre ACID, quando usar transações, optimistic vs pessimistic locking.

7. **Seção `## Vocabulário PT→EN`** (8+ termos).

8. **Seção `## Fontes`**: links para docs de transação de cada ORM + PostgreSQL isolation levels docs.

**Mínimo de código:** 8 snippets TypeScript

---

## Task 10: Nota 09 — Paginação — offset, cursor e keyset

**Files:**
- Create: `03-Dominios/Node/ORMs e banco de dados/09 - Paginação - offset, cursor e keyset.md`

**Commit:** `feat(node/g6): add 09 - Paginação - offset, cursor e keyset`

**Frontmatter:**
```yaml
title: "Paginação - offset, cursor e keyset"
created: 2026-05-10
updated: 2026-05-10
type: concept
status: seedling
progresso: andamento
tags:
  - node
  - orm
  - paginacao
  - performance
  - banco-de-dados
publish: false
```

**Conteúdo mínimo (320+ linhas):**

1. **Callout `[!abstract] TL;DR`** (4+ linhas): Três estratégias de paginação com trade-offs distintos. Offset/limit: simples, mas degradação com OFFSET alto. Cursor-based: eficiente, sem duplicatas em paginação, mas sem saltar páginas. Keyset: mais eficiente ainda, usa índice, adequado para feeds infinitos. Para APIs REST modernas: cursor ou keyset. Offset só para casos de uso com "ir para página X".

2. **Seção `## O que é`**: o problema de paginação, por que importa para performance e UX.

3. **Seção `## Como funciona`** com subsecções:

   ### Offset/Limit
   - `LIMIT 20 OFFSET 200` — como funciona internamente no banco
   - Por que degrada: banco faz full scan + descarta as primeiras N linhas
   - Problema de duplicatas/skips com dados mutáveis
   - Quando ainda é aceitável (tabelas pequenas, admin panels, relatórios)
   - Implementação em Sequelize, Prisma, TypeORM, Drizzle

   ### Cursor-based pagination
   - Opaque cursor (base64 encoded) vs transparent cursor (ID)
   - `WHERE id > :cursor ORDER BY id LIMIT n`
   - Implementação com Prisma (`cursor: { id: lastId }, skip: 1, take: 20`)
   - Como retornar `nextCursor` e `hasNextPage` na resposta
   - Limitação: não permite pular para "página 10"
   - Exemplo de response envelope: `{ data: [...], nextCursor: "...", hasNextPage: true }`

   ### Keyset pagination
   - `WHERE (created_at, id) < (:ts, :id) ORDER BY created_at DESC, id DESC LIMIT n`
   - Por que é mais eficiente que cursor (usa índice composto)
   - Índice necessário no banco
   - Implementação com Drizzle (mais natural) e Prisma (raw query)
   - Caso de uso: feeds infinitos, timelines, logs

   ### Paginação bidirecional
   - `hasPreviousPage`, `startCursor`, `endCursor` (GraphQL Relay spec)
   - Implementação com Prisma (`before`/`after`)

   ### Total count e performance
   - `COUNT(*)` é caro em tabelas grandes
   - Estratégia: retornar `hasMore` em vez de `totalCount`
   - Quando o total é necessário: usar `pg_estimate_count` (estimativa) ou cache

4. **Seção `## Quando usar`**: tabela de comparação offset vs cursor vs keyset por caso de uso.

5. **Seção `## Armadilhas comuns`** (4+ armadilhas com código):
   - `OFFSET` alto em tabela de 10M rows (timeouts em produção)
   - Cursor sem índice no campo de ordenação (full scan)
   - Paginação bidirecional com keyset sem índice composto
   - Retornar `totalCount` com `COUNT(*)` em toda requisição sem cache

6. **Seção `## Em entrevista`**: 4+ sentenças em inglês sobre paginação strategies, quando usar cada uma, como implementar cursor-based.

7. **Seção `## Vocabulário PT→EN`** (8+ termos).

8. **Seção `## Fontes`**: links para Prisma pagination docs + artigos sobre keyset pagination.

**Mínimo de código:** 8 snippets (SQL + implementações nos ORMs)

---

## Task 11: Nota 10 — Cheatsheet e decision tree de ORMs

**Files:**
- Create: `03-Dominios/Node/ORMs e banco de dados/10 - Cheatsheet e decision tree de ORMs.md`

**Commit:** `feat(node/g6): add 10 - Cheatsheet e decision tree de ORMs`

**Frontmatter:**
```yaml
title: "Cheatsheet e decision tree de ORMs"
created: 2026-05-10
updated: 2026-05-10
type: concept
status: seedling
progresso: andamento
tags:
  - node
  - orm
  - cheatsheet
  - banco-de-dados
publish: false
aliases:
  - Decision tree ORMs
  - ORM cheatsheet
```

**Conteúdo mínimo (300+ linhas):**

Esta nota é uma referência consolidada — priorizando densidade e escaneabilidade (tabelas, listas, snippets curtos).

1. **Callout `[!abstract] TL;DR`** (3+ linhas): Referência rápida para entrevistas e implementação. Inclui comparativo de APIs entre os 4 ORMs, decision tree, snippets prontos para os casos mais frequentes, e checklist de produção.

2. **Seção `## Decision tree`** com lógica em cascata:
   ```
   Edge runtime? → Drizzle
   NestJS enterprise? → TypeORM ou Prisma
   Projeto novo TypeScript? → Prisma v6
   Legacy Sequelize? → manter Sequelize (upgrade v7)
   SQL-first preference? → Drizzle
   Equipe Java/JPA background? → TypeORM
   Default → Prisma v6
   ```

3. **Seção `## Comparativo de APIs`** — tabela de operações equivalentes nos 4 ORMs:
   | Operação | Sequelize | Prisma | TypeORM | Drizzle |
   - findAll / findMany / find / select
   - findOne / findFirst / findOne / select().limit(1)
   - create / create / save / insert
   - update / update / save / update
   - delete / delete / remove / delete
   - eager loading (include/relations)
   - transaction

4. **Seção `## Snippets rápidos por ORM`** com os padrões mais usados em cada ORM (copiar/colar).

5. **Seção `## Checklist de produção`**:
   - [ ] `synchronize: false` em TypeORM produção
   - [ ] Migrations versionadas no git
   - [ ] Connection pool configurado (máx de conexões)
   - [ ] Query logging ativo em dev, desativado em prod
   - [ ] N+1 verificado com eager loading ou DataLoader
   - [ ] Paginação com cursor (não offset) em tabelas grandes
   - [ ] Transações em operações atômicas
   - [ ] Índices nas colunas de WHERE e ORDER BY mais usadas
   - [ ] Timeout de query configurado

6. **Seção `## Vocabulário completo PT→EN`** com 15+ termos consolidados do galho.

7. **Seção `## Em entrevista — frases prontas`**:
   Paragráfos curtos em inglês para os cenários mais perguntados:
   - "How do you choose an ORM?"
   - "How do you handle N+1 queries?"
   - "What's your migration strategy?"
   - "How do you handle transactions?"
   - "How do you paginate large datasets?"

8. **Seção `## Veja também`** com wikilinks para todas as notas do galho.

**Mínimo de código:** 4 snippets comparativos

---

## Task 12: Poda do tronco + atualização do índice

**Files:**
- Modify: `03-Dominios/JavaScript/Backend/Node.js.md`
- Modify: `03-Dominios/Node/index.md`

**Commit:** `chore(node/g6): prune trunk - 2 sections migrated to orms galho`

**Step 1: Podar seção `### ORMs` do tronco**

Localizar a seção `### ORMs` dentro de `## How to explain in English` (linhas 218-249 aproximadamente) e substituir o conteúdo completo pelo callout:

```markdown
### ORMs

> [!nota] Migrado para galho próprio
> Os 4 ORMs principais (Sequelize, Prisma, TypeORM, Drizzle) foram expandidos em [[ORMs e banco de dados]] (galho 6). Veja em particular [[01 - Panorama de ORMs]] (comparativo), [[03 - Prisma - schema-first e type safety]] (Prisma v6), [[05 - Drizzle - ORM lightweight e type-safe]] (edge-first) e [[10 - Cheatsheet e decision tree de ORMs]] (referência rápida).
```

**Step 2: Podar seção `### N+1 queries` do tronco**

Localizar a seção `### N+1 queries` dentro de `## Troubleshooting em produção` (linhas 259-289 aproximadamente) e substituir o conteúdo completo pelo callout:

```markdown
### N+1 queries

> [!nota] Migrado para galho próprio
> Detecção, estratégias de resolução (eager loading, DataLoader) e exemplos em todos os ORMs foram expandidos em [[ORMs e banco de dados]] (galho 6): [[06 - N+1 queries - detecção e DataLoader]].
```

**Step 3: Adicionar galho 6 no `## Veja também` do tronco**

Adicionar a linha após `[[Observability e produção]]`:

```markdown
- [[ORMs e banco de dados]] — galho 6 da trilha Node Senior; os 4 ORMs (Sequelize, Prisma, TypeORM, Drizzle), N+1, migrations, transações, paginação e decision tree
```

**Step 4: Adicionar galho 6 em `03-Dominios/Node/index.md`**

Na seção `### Galhos da trilha Node Senior`, adicionar após a linha do galho 5:

```markdown
- [[ORMs e banco de dados]] — galho 6: os 4 ORMs (Sequelize, Prisma, TypeORM, Drizzle), padrões críticos (N+1, migrations, transações, paginação) e decision tree
```

---

## Checklist final

- [ ] Task 1: MOC criado e commitado
- [ ] Task 2: Nota 01 Panorama criada e commitada
- [ ] Task 3: Nota 02 Sequelize criada e commitada
- [ ] Task 4: Nota 03 Prisma criada e commitada
- [ ] Task 5: Nota 04 TypeORM criada e commitada
- [ ] Task 6: Nota 05 Drizzle criada e commitada
- [ ] Task 7: Nota 06 N+1 criada e commitada
- [ ] Task 8: Nota 07 Migrations criada e commitada
- [ ] Task 9: Nota 08 Transações criada e commitada
- [ ] Task 10: Nota 09 Paginação criada e commitada
- [ ] Task 11: Nota 10 Cheatsheet criada e commitada
- [ ] Task 12: Tronco podado + index atualizado e commitados
