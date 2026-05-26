---
title: "Drizzle - ORM lightweight e type-safe"
created: 2026-05-10
updated: 2026-05-12
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
aliases:
  - Drizzle ORM
  - Drizzle
---

# Drizzle - ORM lightweight e type-safe

> [!abstract] TL;DR
> O Drizzle ORM v0.30+ é o queridinho de 2024–2026 no ecossistema [[Node.js]]: SQL-first, zero runtime overhead e type safety construído sobre o próprio sistema de tipos do TypeScript — não há geração de código nem binários externos. Você define schemas em TypeScript usando `pgTable()`, e o tipo de cada query é inferido diretamente no moment de compilação, sem etapa extra de `generate`.
> A filosofia SQL-first separa o Drizzle de ORMs como Prisma e TypeORM: a API espelha SQL real (`.select().from().where()`) em vez de abstrair com `.find({ where: ... })`; isso significa que um dev que conhece SQL consegue ler queries Drizzle sem aprender um DSL proprietário, e o SQL gerado é sempre previsível.
> A killer feature para arquiteturas modernas é compatibilidade nativa com edge runtimes (Cloudflare Workers, Vercel Edge, Deno Deploy): Drizzle usa drivers HTTP (`@neondatabase/serverless`, `@libsql/client`) que não dependem do módulo `net` do Node.js, impossível em contextos edge.
> O `drizzle-kit` gerencia migrations com dois fluxos: `generate` + `migrate` para produção (rastreável, reversível) e `push` para prototipagem rápida em desenvolvimento — nunca em produção. Veja também [[03-Dominios/Node/ORMs e banco de dados/index]] e [[01 - Panorama de ORMs]] para contexto comparativo.

## O que é

O Drizzle ORM é um **query builder e ORM SQL-first para TypeScript e JavaScript**, projetado com três princípios centrais: zero runtime overhead, type safety nativo sem geração de código e API que espelha a sintaxe SQL.

### Filosofia SQL-first

A distinção fundamental do Drizzle frente a Prisma, TypeORM e Sequelize é filosófica antes de técnica: enquanto esses ORMs adotam uma abordagem **ORM-first** (você pensa em objetos e o ORM traduz para SQL), o Drizzle adota **SQL-first** (você pensa em SQL e o Drizzle fornece type safety em cima disso).

Na prática, isso significa que a API é intencionalmente próxima ao SQL:

| ORM-first (Prisma)              | SQL-first (Drizzle)                                 |
| ------------------------------- | --------------------------------------------------- |
| `db.user.findMany({ where: {} })`| `db.select().from(users).where(eq(users.active, true))` |
| `db.user.create({ data: {} })`  | `db.insert(users).values({}).returning()`           |
| `db.user.update({ where: {} })` | `db.update(users).set({}).where(eq(users.id, id))`  |
| Schema em arquivo `.prisma`     | Schema em arquivos `.ts` normais                    |

Um dev que sabe SQL consegue ler e escrever queries Drizzle sem estudar um DSL novo — o mapeamento mental é direto.

### Zero runtime overhead

O Drizzle não tem query engine externo, binário sidecar nem processo separado. O type safety é construído **sobre o sistema de tipos do TypeScript em tempo de compilação**: os tipos das colunas definidos no schema são propagados diretamente para os tipos de retorno das queries via inferência genérica.

Compare com Prisma v5 (antes do WASM engine do v6): o Prisma dependia de um binário compilado por plataforma que rodava como processo separado, adicionando overhead de IPC. Com Drizzle, tudo fica no processo Node.js, sem etapas adicionais.

### Posição em 2026

Em [[01 - Panorama de ORMs]], o Drizzle aparece como a escolha preferida para:

- **Edge runtimes** — único ORM com suporte nativo a drivers HTTP
- **Equipes com domínio de SQL** — API previsível, sem abstração opaca
- **Performance crítica** — zero overhead de engine, SQL gerado é o SQL executado
- **Projetos greenfield TypeScript** — type safety completo sem geração de código

---

## Como funciona

### Schema definition

O schema é definido em arquivos TypeScript comuns usando funções do `drizzle-orm/pg-core`. Cada tabela é uma constante exportada, e os tipos das colunas são inferidos automaticamente.

```typescript
// src/schema.ts
import {
  pgTable,
  text,
  integer,
  boolean,
  timestamp,
  uuid,
  jsonb,
} from 'drizzle-orm/pg-core';

export const users = pgTable('users', {
  id: uuid('id').primaryKey().defaultRandom(),
  email: text('email').notNull().unique(),
  name: text('name').notNull(),
  active: boolean('active').notNull().default(true),
  createdAt: timestamp('created_at').notNull().defaultNow(),
});

export const posts = pgTable('posts', {
  id: uuid('id').primaryKey().defaultRandom(),
  title: text('title').notNull(),
  body: text('body'),
  authorId: uuid('author_id').notNull().references(() => users.id),
  publishedAt: timestamp('published_at'),
  metadata: jsonb('metadata'),
});
```

O tipo `typeof users.$inferSelect` retorna automaticamente o tipo de uma linha selecionada; `typeof users.$inferInsert` retorna o tipo para inserção (campos com `default` tornam-se opcionais).

```typescript
// Inferindo tipos do schema — sem escrever interfaces manuais
type User = typeof users.$inferSelect;
// { id: string; email: string; name: string; active: boolean; createdAt: Date }

type NewUser = typeof users.$inferInsert;
// { id?: string; email: string; name: string; active?: boolean; createdAt?: Date }
```

**Referências entre tabelas** usam closures para evitar dependências circulares:

```typescript
// Correto: reference via closure
authorId: uuid('author_id').notNull().references(() => users.id),

// Incorreto: referência direta causa erro de inicialização circular
// authorId: uuid('author_id').notNull().references(users.id),
```

### Queries — select

O cliente é inicializado uma vez e reutilizado em todo o projeto:

```typescript
// src/db.ts
import postgres from 'postgres';
import { drizzle } from 'drizzle-orm/postgres-js';
import * as schema from './schema';

const client = postgres(process.env.DATABASE_URL!);
export const db = drizzle(client, { schema });
```

Com o cliente configurado, as queries seguem a sintaxe SQL-first:

```typescript
import { db } from './db';
import { users, posts } from './schema';
import { eq, and, gt, ilike, isNull, inArray } from 'drizzle-orm';

// Select completo (SELECT * FROM users)
const allUsers = await db.select().from(users);

// Com filtro (WHERE active = true)
const activeUsers = await db
  .select()
  .from(users)
  .where(eq(users.active, true));

// Projeção — seleciona colunas específicas
const emailsOnly = await db
  .select({ id: users.id, email: users.email })
  .from(users);
// Tipo inferido: { id: string; email: string }[]

// Join com múltiplos filtros
const postsWithAuthors = await db
  .select({
    postId: posts.id,
    title: posts.title,
    authorName: users.name,
  })
  .from(posts)
  .leftJoin(users, eq(posts.authorId, users.id))
  .where(
    and(
      ilike(posts.title, '%typescript%'),
      gt(posts.publishedAt, new Date('2026-01-01')),
    ),
  )
  .orderBy(posts.publishedAt)
  .limit(20);

// isNull e inArray
const drafts = await db
  .select()
  .from(posts)
  .where(isNull(posts.publishedAt));

const byIds = await db
  .select()
  .from(users)
  .where(inArray(users.id, ['id-1', 'id-2', 'id-3']));
```

> [!tip] Operadores disponíveis
> O Drizzle exporta operadores SQL diretamente: `eq`, `ne`, `gt`, `gte`, `lt`, `lte`, `and`, `or`, `not`, `isNull`, `isNotNull`, `inArray`, `notInArray`, `between`, `ilike`, `like`, `exists`. Todos são type-safe e correspondem diretamente a operadores SQL.

### Queries — mutations

Insert, update e delete seguem o mesmo padrão SQL-first:

```typescript
// INSERT com RETURNING
const [newUser] = await db
  .insert(users)
  .values({
    email: 'alice@example.com',
    name: 'Alice',
  })
  .returning();
// newUser: User (tipo completo inferido)

// INSERT múltiplos registros
const newPosts = await db
  .insert(posts)
  .values([
    { title: 'Post 1', authorId: newUser.id },
    { title: 'Post 2', authorId: newUser.id },
  ])
  .returning({ id: posts.id, title: posts.title });

// UPSERT — INSERT ... ON CONFLICT DO UPDATE
await db
  .insert(users)
  .values({ email: 'alice@example.com', name: 'Alice' })
  .onConflictDoUpdate({
    target: users.email,         // coluna(s) da constraint
    set: { name: 'Alice Updated' }, // campos a atualizar no conflito
  });

// UPDATE com WHERE
const [updated] = await db
  .update(users)
  .set({ active: false, name: 'Alice (inactive)' })
  .where(eq(users.id, newUser.id))
  .returning();

// DELETE com WHERE
await db
  .delete(posts)
  .where(eq(posts.authorId, newUser.id));
```

> [!warning] `.returning()` é PostgreSQL e SQLite only
> O método `.returning()` é suportado nativamente no **PostgreSQL** e no **SQLite**. No **MySQL, não há suporte** — não existe simulação automática nem queries extras emitidas pelo Drizzle. Para recuperar o ID gerado em inserts com autoincrement no MySQL, use `.$returningId()`. Para outros campos, execute um `SELECT` separado após o insert.

### Relations API

A Relations API é uma camada separada do query builder SQL — ela define o grafo de relacionamentos e permite carregar dados associados com uma sintaxe declarativa, sem escrever JOINs manuais.

```typescript
// src/schema.ts — adicionando relações
import { relations } from 'drizzle-orm';

export const usersRelations = relations(users, ({ many }) => ({
  posts: many(posts),
}));

export const postsRelations = relations(posts, ({ one }) => ({
  author: one(users, {
    fields: [posts.authorId],   // FK na tabela posts
    references: [users.id],      // PK na tabela users
  }),
}));
```

Com as relações definidas, o `db.query.*` (Relational Query API) permite carregar dados aninhados:

```typescript
import { asc, isNull } from 'drizzle-orm';

// Users com posts associados — gera SQL otimizado (sem N+1)
const usersWithPosts = await db.query.users.findMany({
  with: {
    posts: {
      where: isNull(posts.publishedAt), // só rascunhos
      orderBy: [asc(posts.publishedAt)],
      limit: 5,
    },
  },
});
// Tipo inferido: (User & { posts: Post[] })[]

// Post com autor
const post = await db.query.posts.findFirst({
  where: eq(posts.id, postId),
  with: {
    author: true,
  },
});
// Tipo: (Post & { author: User }) | undefined
```

> [!important] SQL joins vs Relations API — não misture
> O query builder SQL (`.select().from().leftJoin()`) sem projeção retorna **objetos agrupados por tabela** (`{ posts: Post; users: User | null }[]`), não relações aninhadas. Com projeção customizada, retorna exatamente a forma que você definiu. A Relations API (`.query.*`) retorna **objetos aninhados estruturados** automaticamente com tipos inferidos. Misturar os dois em uma mesma query não é possível e confunde os tipos gerados pelo TypeScript.

### Drizzle Kit — migrations

O `drizzle-kit` é a ferramenta CLI de migrações, instalada como dev dependency (`drizzle-kit`). A configuração fica em `drizzle.config.ts` na raiz do projeto:

```typescript
// drizzle.config.ts
import { defineConfig } from 'drizzle-kit';

export default defineConfig({
  schema: './src/schema.ts',   // caminho do schema TypeScript
  out: './drizzle',             // diretório para arquivos de migration
  dialect: 'postgresql',
  dbCredentials: {
    url: process.env.DATABASE_URL!,
  },
});
```

**Fluxo de migrations — produção:**

```bash
# 1. Gera arquivo SQL de migration baseado no diff do schema
npx drizzle-kit generate
# Cria: drizzle/0001_add_users_table.sql (arquivo commitável)

# 2. Aplica as migrations pendentes ao banco
npx drizzle-kit migrate
# Executa os .sql em ordem, rastreando no __drizzle_migrations
```

**Fluxo de desenvolvimento rápido (APENAS dev):**

```bash
# Push aplica o schema diretamente ao banco SEM gerar arquivos de migration
npx drizzle-kit push
# ⚠️ Sem histórico, sem rollback, sem auditoria — nunca em produção

# Abre o Drizzle Studio (GUI web para inspecionar o banco)
npx drizzle-kit studio
```

> [!danger] `drizzle-kit push` nunca em produção
> O `push` aplica mudanças diretamente no banco de dados sem criar arquivos de migration. Isso significa: sem histórico de mudanças, sem possibilidade de rollback, sem rastreabilidade de "quem mudou o quê quando". Use apenas em banco de desenvolvimento local ou ambientes descartáveis. O fluxo `generate` + `migrate` é obrigatório para produção.

### Edge runtimes

A compatibilidade com edge runtimes é uma diferença técnica real, não marketing. Edge runtimes (Cloudflare Workers, Vercel Edge Functions, Deno Deploy) **não permitem conexões TCP brutas** — o módulo `net` do Node.js simplesmente não existe nesse ambiente.

ORMs tradicionais que dependem de `pg` (node-postgres) ou `mysql2` usam sockets TCP e falham em edge. O Drizzle resolve isso suportando **drivers HTTP**:

```typescript
// Cloudflare Workers + Neon (PostgreSQL serverless via HTTP)
import { neon } from '@neondatabase/serverless';
import { drizzle } from 'drizzle-orm/neon-http';
import { eq } from 'drizzle-orm';
import { users } from './schema';

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const sql = neon(env.DATABASE_URL);
    const db = drizzle({ client: sql });

    const result = await db
      .select({ id: users.id, name: users.name })
      .from(users)
      .where(eq(users.active, true));

    return Response.json(result);
  },
};
```

```typescript
// Vercel Edge + Turso (SQLite distribuído via HTTP)
import { createClient } from '@libsql/client/http';
import { drizzle } from 'drizzle-orm/libsql';

const client = createClient({
  url: process.env.TURSO_URL!,
  authToken: process.env.TURSO_AUTH_TOKEN!,
});
export const db = drizzle(client);
```

**Por que funciona em edge:**
- `@neondatabase/serverless` e `@libsql/client` comunicam via HTTP/HTTPS, não TCP
- Nenhum módulo exclusivo do Node.js (`net`, `tls`, `dns`) é usado
- O bundle do Drizzle é pequeno (sem query engine binário) — adequado aos limites de tamanho de bundle dos edge runtimes (geralmente 1–4 MB)

> [!tip] Connection pooling em serverless
> Em arquiteturas serverless (Lambda, Vercel Functions), cada invocação pode criar uma nova conexão com o banco. Com drivers TCP tradicionais, isso esgota o pool rapidamente. Com `@neondatabase/serverless`, cada query é um request HTTP — sem estado de conexão persistente. Para node-postgres em serverless, use PgBouncer, Neon connection pooling ou Supabase Pooler como pooler externo.

---

## Quando usar

**Use Drizzle quando:**

- O projeto roda em **edge runtimes** (Cloudflare Workers, Vercel Edge, Deno Deploy) — é a escolha natural
- A equipe tem **domínio de SQL** e prefere queries previsíveis sem abstração opaca
- **Performance é crítica** e você precisa de SQL gerado previsível e otimizável
- O projeto é **greenfield TypeScript** e você quer type safety sem etapa de geração de código
- Você precisa de **controle fino sobre JOINs e subqueries** que ORMs com abstração alta escondem

**Prefira outras opções quando:**

- A equipe tem **baixo domínio de SQL** e prefere uma API mais declarativa orientada a objetos (Prisma tem melhor DX nesse caso)
- O projeto usa **NestJS com arquitetura enterprise** e decorators são um requisito (TypeORM tem integração mais profunda)
- Há requisito de **suporte a múltiplos bancos** com abstração total — Drizzle suporta PostgreSQL, MySQL, SQLite, mas a API não é 100% portável entre dialects
- **Equipe migrando de Java/Spring** — TypeORM com decorators é mais familiar

---

## Armadilhas comuns

### 1. Confundir SQL joins com a Relations API

A armadilha mais comum ao aprender Drizzle é misturar os dois sistemas de query.

**Problema:** usar `leftJoin` no query builder e esperar objetos aninhados como na Relations API:

```typescript
// ❌ leftJoin sem projeção retorna objetos agrupados por tabela — não relações aninhadas
const result = await db
  .select()
  .from(posts)
  .leftJoin(users, eq(posts.authorId, users.id));

// result é: { posts: Post; users: User | null }[]
// NÃO é: (Post & { author: User })[]
// Tentar acessar result[0].author retorna undefined — não existe essa chave
```

**Fix:** use a Relations API quando precisar de objetos aninhados, ou shape o resultado manualmente no query builder:

```typescript
// ✅ Relations API — retorna objetos aninhados tipados
const postsWithAuthor = await db.query.posts.findMany({
  with: { author: true },
});
// postsWithAuthor: (Post & { author: User })[]

// ✅ Query builder com shape manual explícito
const result = await db
  .select({
    post: posts,
    authorName: users.name,
  })
  .from(posts)
  .leftJoin(users, eq(posts.authorId, users.id));
// result: { post: Post; authorName: string | null }[]
```

### 2. `drizzle-kit push` em ambiente de produção

O `push` é conveniente para desenvolvimento, mas catastrófico em produção.

**Problema:** usar `push` em produção (ou em um banco com dados reais) sem perceber que não há rollback:

```bash
# ❌ Nunca em produção — aplica schema sem migration file
npx drizzle-kit push

# Se der errado (coluna renomeada = DROP + CREATE, dados perdidos),
# não há histórico de migration para reverter
```

**Fix:** sempre usar `generate` + `migrate` em produção; `push` apenas em banco local descartável:

```bash
# ✅ Fluxo de produção — rastreável e reversível
npx drizzle-kit generate   # Gera ./drizzle/XXXX_migration.sql
git add drizzle/            # Commita os arquivos de migration
npx drizzle-kit migrate     # Aplica ao banco (rastreado em __drizzle_migrations)

# ✅ push apenas para dev local
npx drizzle-kit push        # OK para banco local descartável
```

### 3. Missing connection pooling em serverless com driver TCP

Em Lambda/Vercel Functions com driver `postgres` (node-postgres), cada invocação abre uma nova conexão TCP. Com tráfego moderado, você esgota o pool do PostgreSQL rapidamente.

**Problema:**

```typescript
// ❌ Nova conexão por invocação em serverless — sem pooling
// src/db.ts
import postgres from 'postgres';
import { drizzle } from 'drizzle-orm/postgres-js';

// Esta conexão é criada a cada cold start, sem reuso entre invocações
const client = postgres(process.env.DATABASE_URL!);
export const db = drizzle(client);
```

**Fix:** use um pooler externo ou driver HTTP:

```typescript
// ✅ Opção 1: Neon serverless via HTTP (sem estado de conexão)
import { neon } from '@neondatabase/serverless';
import { drizzle } from 'drizzle-orm/neon-http';

const sql = neon(process.env.DATABASE_URL!);
export const db = drizzle({ client: sql });

// ✅ Opção 2: postgres.js com max de conexões limitado
// e DATABASE_URL apontando para PgBouncer/Supabase Pooler
const client = postgres(process.env.DATABASE_URL!, {
  max: 1,            // limita conexões por instância serverless
  idle_timeout: 20,  // fecha conexões ociosas rapidamente
});
export const db = drizzle(client);
```

### 4. Esquecer que `.returning()` retorna array

O `.returning()` sempre retorna um array — mesmo que apenas um registro seja inserido/atualizado.

**Problema:**

```typescript
// ❌ Tentativa de acessar diretamente como objeto único
const user = await db
  .insert(users)
  .values({ email: 'x@y.com', name: 'X' })
  .returning();

console.log(user.email); // undefined — user é um array!
```

**Fix:** desestruture o primeiro elemento:

```typescript
// ✅ Desestruturação para pegar o primeiro elemento
const [user] = await db
  .insert(users)
  .values({ email: 'x@y.com', name: 'X' })
  .returning();

console.log(user.email); // 'x@y.com' ✓

// ✅ Ou use índice explícito
const result = await db.insert(users).values({ ... }).returning();
const user = result[0];
```

---

## Em entrevista

**Pergunta comum: "Por que usar Drizzle em vez de Prisma?"**

Drizzle and Prisma solve the same core problem — type-safe database access in TypeScript — but from fundamentally different angles: Drizzle is SQL-first, meaning its query API mirrors SQL syntax directly (`.select().from().where()`), while Prisma is ORM-first with a declarative object model that abstracts the underlying SQL. This distinction matters in practice because Drizzle produces predictable, auditable SQL that senior engineers can reason about without learning a proprietary DSL, whereas Prisma's abstraction can hide performance issues like missing indexes or implicit N+1 patterns behind a clean-looking API. A critical architectural advantage of Drizzle is edge runtime compatibility: since it uses HTTP-based drivers instead of Node.js TCP sockets, it runs natively on Cloudflare Workers and Vercel Edge Functions where `pg` (node-postgres) simply cannot work. For greenfield TypeScript projects targeting serverless or edge deployments, Drizzle is often the stronger choice; for teams that prioritize developer experience, rapid iteration, and a lower SQL fluency requirement, Prisma's schema-first approach and auto-generated types offer a more accessible path.

**Pergunta: "Como o Drizzle garante type safety sem geração de código?"**

Unlike Prisma, which requires a `prisma generate` step to produce a typed client from the `.prisma` schema file, Drizzle builds its type safety directly on TypeScript's structural type system: when you define a column as `text('email').notNull()`, that declaration is a TypeScript value whose generic parameters encode the column's type and nullability, so the query builder can infer return types at compile time without any code generation step. The practical implication is that Drizzle's types are always in sync with the schema — there's no risk of running queries with a stale generated client because the schema definition and the type system are the same artifact. This also means Drizzle adds zero runtime overhead: no query engine process, no IPC, just your TypeScript compiled to SQL strings executed by a thin driver.

---

## Vocabulário PT→EN

| Português                         | Inglês (técnico)                         |
| --------------------------------- | ---------------------------------------- |
| Esquema de banco de dados         | Database schema                          |
| Tabela                            | Table                                    |
| Chave primária                    | Primary key (PK)                         |
| Chave estrangeira                 | Foreign key (FK)                         |
| Migração de banco de dados        | Database migration                       |
| Inferência de tipo                | Type inference                           |
| Sem overhead em tempo de execução | Zero runtime overhead                    |
| Construtor de queries             | Query builder                            |
| Junção (SQL)                      | Join (LEFT JOIN, INNER JOIN, etc.)       |
| Projeção (selecionar colunas)     | Projection / column selection            |
| Upsert (insert or update)         | Upsert / INSERT ON CONFLICT DO UPDATE    |
| Runtime de borda / computação distribuída | Edge runtime                     |
| Driver baseado em HTTP            | HTTP-based driver / serverless driver    |
| Pool de conexões                  | Connection pool / connection pooling     |
| Rollback de migração              | Migration rollback                       |
| Relações (entre tabelas)          | Relations / associations                 |

---

## Fontes

- [Drizzle ORM — Documentação oficial](https://orm.drizzle.team/docs/overview)
- [Drizzle Kit — Migrações e CLI](https://orm.drizzle.team/docs/kit-overview)
- [Drizzle — Relational Queries (Relations API)](https://orm.drizzle.team/docs/rqb)
- [Drizzle — Edge & Serverless](https://orm.drizzle.team/docs/connect-neon)
- [Neon Serverless Driver](https://neon.tech/docs/serverless/serverless-driver)
- [drizzle-orm no npm](https://www.npmjs.com/package/drizzle-orm)
- [drizzle-kit no npm](https://www.npmjs.com/package/drizzle-kit)
