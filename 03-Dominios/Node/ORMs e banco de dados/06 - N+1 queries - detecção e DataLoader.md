---
title: "N+1 queries - detecção e DataLoader"
created: 2026-05-12
updated: 2026-05-12
type: concept
status: seedling
progresso: andamento
tags:
  - node
  - orm
  - performance
  - n+1
  - dataloader
  - banco-de-dados
publish: false
aliases:
  - N+1
  - DataLoader
---

# N+1 queries — detecção e DataLoader

> [!abstract] TL;DR
> O problema **N+1** ocorre quando o código emite 1 query para buscar uma lista de N registros e depois dispara mais N queries individuais para carregar uma associação de cada registro — totalizando N+1 queries no banco. É silencioso: nenhum erro é lançado, apenas latência crescente proporcional ao tamanho do resultado, inviabilizando performance em produção. A forma mais rápida de detectar é habilitar o log de queries em cada ORM e verificar se o número de queries emitidas cresce com o tamanho do resultado. A solução primária para APIs REST é **eager loading** (JOINs), disponível em todos os ORMs via `include` (Sequelize/Prisma), `relations` (TypeORM) ou `with` (Drizzle). Para contextos GraphQL — onde resolvers são chamados individualmente por campo — o **DataLoader** resolve o problema via batching automático no mesmo tick de evento e cache por requisição. Veja também [[01 - Panorama de ORMs]] para o comparativo geral entre ORMs e o contexto de quando cada solução se aplica.

## O que é

### O problema N+1

O problema **N+1** é um anti-padrão de acesso a banco de dados que surge quando o código busca uma coleção de registros e, para cada registro, realiza uma query adicional para carregar uma associação. Se a lista tem N itens, o total de queries é **1 + N**: 1 para buscar a lista, N para buscar as associações.

O que torna o N+1 traiçoeiro é que ele é **invisível no código-fonte**: o ORM faz lazy loading por padrão, ou seja, as queries adicionais só disparam quando o código acessa o campo relacionado. Nenhum erro é lançado — a aplicação simplesmente fica mais lenta à medida que o volume de dados cresce.

**O padrão quebrado clássico:**

```typescript
// ❌ N+1 com Prisma — parece inocente, é catastrófico em escala
const posts = await prisma.post.findMany(); // 1 query

for (const post of posts) {
  // ⚠️ cada acesso dispara 1 query separada para buscar o author
  const author = await prisma.user.findUnique({
    where: { id: post.authorId },
  });
  console.log(`${post.title} — ${author?.name}`);
}
```

**O que o log de queries mostra com 50 posts:**

```sql
-- Query 1: busca a lista
SELECT * FROM "Post";

-- Queries 2 a 51: uma por post
SELECT * FROM "User" WHERE "id" = 1;
SELECT * FROM "User" WHERE "id" = 3;
SELECT * FROM "User" WHERE "id" = 1;  -- ← mesmo id repetido!
SELECT * FROM "User" WHERE "id" = 7;
-- ... 46 queries a mais
```

Com 50 posts, o banco recebe **51 queries**. Com 500 posts, **501 queries**. A latência acumula round-trips de rede ao banco, e o banco sofre com connection pool esgotado sob carga.

## Como funciona

Para ancorar todos os exemplos, considere o seguinte schema:

```typescript
// Schema: User e Post
// Tabela "User": id (Int, PK), name (String), email (String)
// Tabela "Post": id (Int, PK), title (String), content (String),
//                authorId (Int, FK → User.id), published (Boolean)
```

---

### Detectando N+1

O primeiro passo para resolver um N+1 é provar que ele existe. Cada ORM expõe logs de queries de forma diferente.

**Sequelize — habilitar log por instância:**

```typescript
import { Sequelize } from "sequelize";

const sequelize = new Sequelize("postgres://user:pass@localhost/db", {
  logging: console.log, // imprime cada SQL no stdout
  // ou: logging: (sql, timing) => logger.debug({ sql, timing })
});

// Para desabilitar em produção:
// logging: process.env.NODE_ENV === "development" ? console.log : false
```

**Prisma — evento de query:**

```typescript
import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient({
  log: [{ emit: "event", level: "query" }],
});

prisma.$on("query", (e) => {
  console.log(`Query: ${e.query}`);
  console.log(`Params: ${e.params}`);
  console.log(`Duration: ${e.duration}ms`);
});
```

**TypeORM — flag na DataSource:**

```typescript
import { DataSource } from "typeorm";

const AppDataSource = new DataSource({
  type: "postgres",
  host: "localhost",
  port: 5432,
  username: "user",
  password: "pass",
  database: "db",
  logging: true, // imprime cada SQL; use ["query", "error"] para filtrar
  entities: [User, Post],
});
```

**Drizzle — sem log embutido; usar middleware de banco ou PG nativo:**

```typescript
import { drizzle } from "drizzle-orm/node-postgres";
import { Pool } from "pg";

const pool = new Pool({
  connectionString: "postgres://user:pass@localhost/db",
});

// Drizzle não tem log embutido — intercepte no driver pg:
// No postgresql.conf: log_min_duration_statement = 0
// Ou wrape a pool com um proxy de log manual

const db = drizzle(pool, { schema });
```

> [!tip] Smell test de N+1
> Ative o log de queries e execute o endpoint sob teste. Se o número de queries no log for igual ao tamanho do resultado + 1 (ex.: 51 queries para 50 posts), você tem um N+1. Repita com 100 registros — se virar 101 queries, confirmado.

---

### Solução 1 — Eager loading (JOINs)

Eager loading instrui o ORM a buscar a associação **na mesma query** (ou em uma segunda query otimizada com `IN`), eliminando as N queries individuais.

**Prisma — `include`:**

```typescript
// ✅ 1 query com JOIN — busca posts e seus autores de uma vez
const posts = await prisma.post.findMany({
  include: {
    author: true, // LEFT JOIN em "User"
  },
  // Limite de campos: use select dentro de include para não trazer tudo
  // include: { author: { select: { id: true, name: true } } }
});

// Agora post.author já está disponível sem queries adicionais
for (const post of posts) {
  console.log(`${post.title} — ${post.author.name}`);
}
```

**TypeORM — `relations` no find ou `leftJoinAndSelect` no QueryBuilder:**

```typescript
import { AppDataSource } from "./data-source";
import { Post } from "./entity/Post";

// Opção A: find com relations (gera 2 queries otimizadas com IN)
const posts = await AppDataSource.getRepository(Post).find({
  relations: ["author"],
});

// Opção B: QueryBuilder com LEFT JOIN explícito (1 query com JOIN)
const postsWithAuthor = await AppDataSource.getRepository(Post)
  .createQueryBuilder("post")
  .leftJoinAndSelect("post.author", "author")
  .getMany();

// Em ambos os casos: post.author já populado
```

**Sequelize — `include`:**

```typescript
import { Post } from "./models/post";
import { User } from "./models/user";

const posts = await Post.findAll({
  include: [{ model: User, as: "author", attributes: ["id", "name"] }],
});
```

**Drizzle — `with` na Relations API ou `leftJoin` explícito:**

```typescript
import { db } from "./db";
import { posts, users } from "./schema";
import { eq } from "drizzle-orm";

// Relations API (requer definição de relations no schema)
const result = await db.query.posts.findMany({
  with: { author: true },
});

// Alternativa: leftJoin explícito
const result = await db
  .select()
  .from(posts)
  .leftJoin(users, eq(posts.authorId, users.id));
```

> [!success] Resultado
> Com eager loading, o banco recebe **1 query** (ou 2 com `IN` no TypeORM) independentemente do tamanho do resultado. 50 posts = 1 query. 500 posts = 1 query.

---

### Solução 2 — DataLoader (batch + cache)

**Quando JOINs não resolvem:** em APIs GraphQL, cada campo de um tipo é resolvido por um resolver independente. Um resolver `author` é chamado N vezes — uma para cada post — sem contexto das outras chamadas. Eager loading não é aplicável porque o ORM não sabe com antecedência quais posts serão carregados.

O **DataLoader** resolve isso com duas técnicas:

1. **Batching:** coleta todas as chamadas `.load(id)` que ocorrem no mesmo tick do event loop e dispara uma única query com todos os IDs via `IN`.
2. **Cache por instância:** dentro de uma mesma instância de DataLoader, cada ID é carregado apenas uma vez.

**Implementação completa de um UserLoader:**

```typescript
import DataLoader from "dataloader";
import { prisma } from "./prisma-client";

// Tipo do User retornado pelo banco
interface User {
  id: number;
  name: string;
  email: string;
}

// A batch function recebe um array de keys e DEVE retornar
// um array de resultados na MESMA ORDEM que as keys
async function batchLoadUsers(ids: readonly number[]): Promise<(User | Error)[]> {
  // 1 query com WHERE id IN (...)
  const users = await prisma.user.findMany({
    where: { id: { in: [...ids] } },
    select: { id: true, name: true, email: true },
  });

  // Indexar por id para lookup O(1)
  const userMap = new Map<number, User>(users.map((u) => [u.id, u]));

  // ⚠️ CONTRATO CRÍTICO: retornar na mesma ordem que `ids`
  // Se um id não existir, retornar Error (não undefined)
  return ids.map((id) => userMap.get(id) ?? new Error(`User ${id} not found`));
}

// Fábrica — sempre criar nova instância por requisição
export function createUserLoader(): DataLoader<number, User> {
  return new DataLoader<number, User>(batchLoadUsers, {
    // cache: true é o padrão — desative com cache: false se não quiser cache
    maxBatchSize: 100, // limite de IDs por batch
  });
}
```

**Uso em resolver GraphQL:**

```typescript
import { createUserLoader } from "./loaders/user-loader";

// Tipo do contexto GraphQL — o loader vive no context da requisição
interface GraphQLContext {
  userLoader: DataLoader<number, User>;
}

const resolvers = {
  Post: {
    // Chamado 1x por post — DataLoader batcheia tudo no mesmo tick
    author: (post: Post, _args: unknown, ctx: GraphQLContext) => {
      return ctx.userLoader.load(post.authorId);
    },
  },
};
```

**Setup por requisição (Express):**

```typescript
import express from "express";
import { ApolloServer } from "@apollo/server";
import { expressMiddleware } from "@apollo/server/express4";
import { createUserLoader } from "./loaders/user-loader";

const app = express();
const server = new ApolloServer({ typeDefs, resolvers });
await server.start();

app.use(
  "/graphql",
  expressMiddleware(server, {
    // ✅ Nova instância por requisição — NUNCA use singleton global
    context: async () => ({
      userLoader: createUserLoader(),
      // Adicione outros loaders aqui conforme necessário
    }),
  })
);
```

**Carregando múltiplos IDs com `loadMany`:**

```typescript
// Em um resolver que precisa de vários autores ao mesmo tempo
const Post = {
  coAuthors: async (post: Post, _args: unknown, ctx: GraphQLContext) => {
    // loadMany retorna Promise<(User | Error)[]>
    const results = await ctx.userLoader.loadMany(post.coAuthorIds);

    // Filtrar erros e retornar apenas Users válidos
    return results.filter((r): r is User => !(r instanceof Error));
  },
};
```

---

### DataLoader internals

Entender o mecanismo interno ajuda a evitar bugs sutis e explicar em entrevista.

**Batching baseado em ticks do event loop:**

1. O resolver do `Post.author` chama `userLoader.load(1)`.
2. O GraphQL processa o próximo post e chama `userLoader.load(3)`.
3. O GraphQL processa mais um post e chama `userLoader.load(1)` novamente.
4. **Fim do tick atual** — DataLoader dispara a batch function com `[1, 3]` (deduplicado, sem o segundo `1`).
5. A batch function emite `SELECT * FROM "User" WHERE id IN (1, 3)` — **1 query** para os 50 posts.

**Cache por instância:**

- O cache é interno à instância do DataLoader (um `Map<key, Promise<value>>`).
- Se `load(1)` for chamado duas vezes, a segunda chamada retorna o mesmo `Promise` — sem segunda query.
- Por isso a instância deve ser **por requisição**: um cache global carregaria dados de um usuário para outro.
- Para invalidar manualmente: `loader.clear(id)` ou `loader.clearAll()`.

**O contrato de ordenação (obrigatório):**

A batch function DEVE retornar um array de resultados onde `results[i]` corresponde a `keys[i]`. O DataLoader usa o índice para resolver cada `Promise` individual. Se a ordem estiver errada, resolvers receberão dados do usuário errado — um bug silencioso e grave.

```typescript
// ✅ Correto — map sobre keys garante a ordem
return ids.map((id) => userMap.get(id) ?? new Error(`User ${id} not found`));

// ❌ Errado — retornar o array do banco diretamente sem ordenar
return users; // a ordem do banco pode não corresponder à ordem de ids
```

## Quando usar

| Cenário | Solução recomendada |
|---|---|
| API REST com associações conhecidas em build time | Eager loading (include / relations / with) |
| Relatório com muitas associações fixas | Eager loading com campos limitados (select / attributes) |
| GraphQL — resolver de campo de associação | DataLoader |
| Associações que variam por usuário/requisição | DataLoader |
| N desconhecido em query time (lista dinâmica) | DataLoader |
| Cross-service calls (microserviços, HTTP externo) | DataLoader (batcheia chamadas HTTP também) |

> [!tip] Regra de ouro
> Se você sabe **no momento da query** quais associações vai precisar, use eager loading. Se a necessidade surge durante a resolução de campos individuais (GraphQL, templates dinâmicos), use DataLoader.

## Armadilhas comuns

> [!danger] Armadilha 1 — DataLoader singleton global
> **Nunca** instancie o DataLoader fora do escopo de requisição. Um singleton global compartilha cache entre requisições — o usuário A pode receber dados do usuário B que estavam em cache. Sempre crie uma nova instância no middleware de contexto, uma por requisição.

> [!warning] Armadilha 2 — Violação do contrato de ordenação
> A batch function deve retornar resultados na **mesma ordem** que o array de `keys` recebido. Retornar o array do banco diretamente sem alinhar com `keys` causa resolvers recebendo entidades trocadas. Sempre use `.map()` sobre `keys` indexando em um `Map` construído a partir do resultado.

> [!warning] Armadilha 3 — Over-including com eager loading
> `include: { author: true }` no Prisma e `include: [User]` no Sequelize carregam **todas** as colunas da tabela associada. Em tabelas com colunas grandes (blobs, JSON extenso, senhas hasheadas), isso aumenta o tráfego de rede desnecessariamente. Use sempre `select` (Prisma) ou `attributes` (Sequelize) para limitar os campos retornados.

```typescript
// ❌ Carrega todas as colunas de User, incluindo password_hash e dados sensíveis
const posts = await prisma.post.findMany({
  include: { author: true },
});

// ✅ Carrega apenas o necessário
const posts = await prisma.post.findMany({
  include: {
    author: {
      select: { id: true, name: true },
    },
  },
});
```

## Em entrevista

**"What is the N+1 problem and how do you detect it in production?"**

The N+1 problem is a database performance anti-pattern where code fetches a list of N records with one query and then fires N additional individual queries to load an association for each record — totaling N+1 database round-trips. It's dangerous because it's completely silent: the ORM performs lazy loading without errors, and the only symptom is increasing latency proportional to result size. To detect it in development, you enable query logging in your ORM and watch whether the query count matches the result size plus one. In production, you look for it through slow query monitors, APM tools like Datadog or New Relic, or by tracking total query count per request. A reliable signal is a p95 latency that grows linearly with the number of rows in a collection endpoint — that's almost always an N+1. The fix is usually eager loading via JOINs or, in GraphQL contexts, DataLoader.

**"Explain how DataLoader solves the N+1 problem in GraphQL"**

In GraphQL, each field on a type has its own resolver function, so a list of 50 posts will call the `author` resolver 50 times individually. There's no natural place to do a single JOIN because each resolver runs independently without knowing about the others. DataLoader solves this with two mechanisms: batching and caching. For batching, DataLoader collects all `.load(id)` calls that happen within the same JavaScript event loop tick and defers execution to the next tick, at which point it fires a single batch function with all the collected IDs — emitting one `WHERE id IN (...)` query instead of 50 individual ones. For caching, within a single DataLoader instance, each ID is only loaded once; subsequent `.load()` calls for the same ID return the cached Promise. The critical implementation rule is that DataLoader must be instantiated once per HTTP request, never as a global singleton, because the cache must not leak between requests. The batch function also has a strict contract: it must return results in exactly the same order as the input keys array, or resolvers will receive mismatched data.

## Vocabulário PT → EN

| Português | English |
|---|---|
| Problema N+1 | N+1 problem |
| Carregamento ansioso | Eager loading |
| Carregamento preguiçoso | Lazy loading |
| Consulta em lote | Batch query / query batching |
| Função de lote | Batch function |
| Cache por requisição | Per-request cache |
| Junção | JOIN |
| Associação | Association / relation |
| Tick do event loop | Event loop tick |
| Deduplicação | Deduplication |
| Contrato de ordenação | Ordering contract |
| Round-trip de rede | Network round-trip |

## Fontes

- [DataLoader — GitHub oficial (graphql/dataloader)](https://github.com/graphql/dataloader)
- [Prisma — Solving the N+1 problem](https://www.prisma.io/docs/guides/performance-and-optimization/query-optimization-performance)
- [Sequelize — Eager loading](https://sequelize.org/docs/v6/advanced-association-concepts/eager-loading/)
- [TypeORM — Relations documentation](https://typeorm.io/relations)
