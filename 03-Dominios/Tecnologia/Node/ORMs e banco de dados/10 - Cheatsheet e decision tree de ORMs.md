---
title: "Cheatsheet e decision tree de ORMs"
created: 2026-05-12
updated: 2026-06-28
type: concept
status: growing
fase: Magus
publish: true
tags:
  - node
  - orm
  - banco-de-dados
  - cheatsheet
aliases:
  - ORM Decision Tree
  - Cheatsheet ORMs Node
---

# Cheatsheet e decision tree de ORMs

> [!abstract] TL;DR
> Escolha de ORM em Node.js em 2026: Prisma para projetos TypeScript greenfield com necessidade de type safety máxima; TypeORM para equipes vindas de Java/Spring que preferem decorators; Sequelize para manutenção de codebases legados; Drizzle para contextos serverless/edge ou quando tamanho de bundle é crítico. Os padrões transversais que mais impactam produção são N+1 queries (use eager loading ou DataLoader), migrations (nunca edite arquivos já aplicados), transações (prefira gerenciadas; libere QueryRunner no `finally` no TypeORM) e paginação (evite OFFSET em tabelas grandes; use cursor ou keyset).

## Visão geral do ecossistema

```mermaid
flowchart LR
    APP["Aplicação Node.js\n(TypeScript)"]

    APP --> SEQ["Sequelize v7\nActive Record\n~3 MB"]
    APP --> PRI["Prisma v6\nSchema-first\n~2 MB + engine"]
    APP --> TOR["TypeORM v0.3\nData Mapper\n~2 MB"]
    APP --> DRI["Drizzle ≥0.30\nQuery Builder\n< 1 MB"]

    SEQ -->|"Caso de uso"| SEQ_USE["Legado / brownfield\nequipes Sequelize existentes"]
    PRI -->|"Caso de uso"| PRI_USE["Greenfield TypeScript\ntype safety máxima"]
    TOR -->|"Caso de uso"| TOR_USE["Times Java/Spring\ndecorators JPA-style"]
    DRI -->|"Caso de uso"| DRI_USE["Serverless / Edge\nCloudflare Workers / Vercel Edge"]

    SEQ_USE --> DB[("PostgreSQL\nMySQL\nSQLite")]
    PRI_USE --> DB
    TOR_USE --> DB
    DRI_USE --> DB

    style APP fill:#4A90D9,color:#fff
    style SEQ fill:#F5A623,color:#fff
    style PRI fill:#4A90D9,color:#fff
    style TOR fill:#4A90D9,color:#fff
    style DRI fill:#4A90D9,color:#fff
    style DB fill:#4A90D9,color:#fff
```

## Decision tree

- Projeto greenfield com TypeScript?
  - Sim → **Prisma**
    - Precisa de relações complexas, múltiplos schemas ou RLS no banco?
      - Sim → considere TypeORM ou raw SQL
      - Não → Prisma é suficiente
  - Não →
    - Equipe vem de Java/Spring (familiaridade com JPA/Hibernate)?
      - Sim → **TypeORM**
    - Codebase existente já usa Sequelize?
      - Sim → **Sequelize** (manter consistência supera custo de migração)
    - Deploy em ambiente serverless, edge (Cloudflare Workers) ou bundle crítico?
      - Sim → **Drizzle**
    - Nenhuma das anteriores?
      - → **Prisma** ou **Drizzle** (avalie tamanho de bundle e preferências de DX)

## Comparação rápida

| Critério | Sequelize | Prisma | TypeORM | Drizzle |
|---|---|---|---|---|
| Paradigma | Active Record | Schema-first + Data Mapper | Data Mapper (decorators) | Query builder tipado |
| Type safety | Parcial (v7 melhora) | Excelente (gerado) | Parcial (decorators) | Excelente (inferido) |
| Migrations | Próprio CLI | `prisma migrate` | `typeorm migration:*` | `drizzle-kit` |
| Suporte a raw SQL | `sequelize.query()` | `prisma.$queryRaw` | `queryRunner.query()` | `db.execute(sql\`\`)` |
| Bundle size | ~3 MB | ~2 MB (+ engine) | ~2 MB | < 1 MB |
| Curva de aprendizado | Média | Baixa | Alta | Baixa |
| Maturidade | Alta (desde 2010) | Média (desde 2019) | Alta (desde 2016) | Baixa (desde 2022) |
| Serverless / Edge | Parcial | Parcial (Accelerate) | Não recomendado | Excelente |
| Comunidade | Grande | Muito grande | Grande | Crescente |
| Caso de uso primário | Legado, brownfield | Greenfield TypeScript | Times Java/Spring | Serverless, edge |

## Padrões críticos

### N+1 queries

> [!danger] Lazy loading silencioso gera N+1
> ORMs que resolvem associações sob demanda executam uma query por item da lista pai — 100 posts geram 100 queries de autor separadas. O problema é silencioso em desenvolvimento e destrutivo em produção.

**Solução: eager loading ou DataLoader**

Prisma — `include`:
```typescript
const posts = await prisma.post.findMany({
  include: { author: true },
});
```

TypeORM — `relations`:
```typescript
const posts = await postRepository.find({
  relations: ['author'],
});
```

Sequelize — `include`:
```typescript
const posts = await Post.findAll({
  include: [{ model: User, as: 'author' }],
});
```

Drizzle — join explícito (sem lazy loading por design):
```typescript
const posts = await db
  .select()
  .from(postsTable)
  .leftJoin(usersTable, eq(postsTable.authorId, usersTable.id));
```

DataLoader (qualquer ORM — útil em GraphQL resolvers):
```typescript
import { In } from 'typeorm';

const userLoader = new DataLoader(async (ids: readonly number[]) => {
  const users = await userRepository.find({ where: { id: In([...ids]) } });
  return ids.map(id => users.find(u => u.id === id) ?? null);
});
```

### Migrations

**Regra fundamental:** nunca edite um arquivo de migration já aplicado em qualquer ambiente. Crie sempre uma nova migration para corrigir.

| ORM | Criar migration | Aplicar | Reverter |
|---|---|---|---|
| Sequelize | `npx sequelize-cli migration:generate --name <name>` | `npx sequelize-cli db:migrate` | `npx sequelize-cli db:migrate:undo` |
| Prisma | `npx prisma migrate dev --name <name>` | automático no `dev` / `npx prisma migrate deploy` (prod) | não tem rollback automático — crie migration de reverso |
| TypeORM | `npx typeorm migration:generate src/migrations/<Name> -d src/data-source.ts` | `npx typeorm migration:run -d src/data-source.ts` | `npx typeorm migration:revert -d src/data-source.ts` |
| Drizzle | `npx drizzle-kit generate` | `npx drizzle-kit push` (dev) / `npx drizzle-kit migrate` (prod) | manual — edite ou crie migration de reverso |

> [!warning] Prisma não tem rollback automático
> `prisma migrate dev` aplica e não oferece `down` nativo. Em produção, planeje migrations reversíveis escrevendo a operação inversa como nova migration antes de deployar.

### Transações

> [!warning] Prefira transações gerenciadas
> Transações gerenciadas fazem rollback automático em exceção e simplificam o fluxo de erro. Use transações manuais apenas quando precisar de controle de isolamento explícito ou lógica condicional de rollback.

Prisma — `$transaction` (gerenciada):
```typescript
const [pedido, estoque] = await prisma.$transaction([
  prisma.order.create({ data: orderData }),
  prisma.product.update({
    where: { id: productId },
    data: { stock: { decrement: 1 } },
  }),
]);
```

TypeORM — `QueryRunner` (manual):
```typescript
const queryRunner = dataSource.createQueryRunner();
await queryRunner.connect();
await queryRunner.startTransaction();
try {
  await queryRunner.manager.save(Order, order);
  await queryRunner.manager.save(Stock, stock);
  await queryRunner.commitTransaction();
} catch (err) {
  await queryRunner.rollbackTransaction();
  throw err;
} finally {
  await queryRunner.release(); // obrigatório — evita ConnectionTimeoutError
}
```

Sequelize — `transaction` com callback (gerenciada):
```typescript
await sequelize.transaction(async (t) => {
  await Order.create(orderData, { transaction: t });
  await Product.update({ stock: sequelize.literal('stock - 1') }, {
    where: { id: productId },
    transaction: t,
  });
});
```

Drizzle — `db.transaction` (gerenciada):
```typescript
await db.transaction(async (tx) => {
  await tx.insert(orders).values(orderData);
  await tx.update(products)
    .set({ stock: sql`${products.stock} - 1` })
    .where(eq(products.id, productId));
});
```

### Paginação

| Caso de uso | Estratégia | Motivo |
|---|---|---|
| Admin UI com acesso a página arbitrária | Offset | Random access necessário |
| Feed / timeline / infinite scroll | Cursor ou Keyset | O(1), estável com inserts |
| Tabela < 100k linhas | Offset | Diferença negligível |
| Export em lote / ETL | Keyset | Memory previsível, sem drift |

Prisma — cursor nativo:
```typescript
const posts = await prisma.post.findMany({
  take: limite + 1,
  ...(cursor && { cursor: { id: cursor }, skip: 1 }),
  orderBy: { id: 'asc' },
});
const hasNextPage = posts.length > limite;
if (hasNextPage) posts.pop();
return { posts, nextCursor: hasNextPage ? posts[posts.length - 1].id : null };
```

Drizzle — keyset com `gt`:
```typescript
import { gt, asc } from 'drizzle-orm';
const rows = await db.select().from(events)
  .where(lastId !== undefined ? gt(events.id, lastId) : undefined)
  .orderBy(asc(events.id))
  .limit(limite + 1);
```

### Connection pooling

O pool de conexões é o recurso mais frequentemente mal configurado em aplicações Node.js com ORM. Cada conexão abre um socket TCP, aloca memória no banco e conta contra o limite `max_connections` do PostgreSQL (padrão: 100). Sem pool adequado, a aplicação exaure conexões sob carga.

**Prisma — `connection_limit` na connection string**

```typescript
// prisma/schema.prisma
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL") // ?connection_limit=10&pool_timeout=20
}

// .env
DATABASE_URL="postgresql://user:pass@localhost:5432/mydb?connection_limit=10&pool_timeout=20"
```

Prisma usa seu próprio connection pool embutido no Query Engine (processo Rust separado). `connection_limit` define o máximo de conexões simultâneas; `pool_timeout` em segundos define quanto tempo esperar por uma conexão livre antes de lançar erro. Em serverless (Vercel, AWS Lambda), use [Prisma Accelerate](https://www.prisma.io/accelerate) que mantém o pool fora da função.

**TypeORM — `poolSize` no DataSource**

```typescript
const AppDataSource = new DataSource({
  type: 'postgres',
  url: process.env.DATABASE_URL,
  poolSize: 10,              // máximo de conexões no pool
  connectTimeoutMS: 5000,    // timeout para abrir conexão
  extra: {
    // opções diretas do driver pg (node-postgres)
    idleTimeoutMillis: 30000,  // conexão ociosa por 30s é fechada
    connectionTimeoutMillis: 5000,
    max: 10,                   // redundante com poolSize, mas explícito
    min: 2,                    // mantém 2 conexões abertas sempre
  },
});
```

TypeORM delega o pool para o driver subjacente (`pg` no caso do PostgreSQL). O `extra` passa opções diretamente para `pg.Pool`. Importante: `poolSize` no TypeORM define o `max` do pool; para controlar `min` e `idleTimeout`, use `extra`.

**Sequelize — `pool` no construtor**

```typescript
const sequelize = new Sequelize(process.env.DATABASE_URL, {
  dialect: 'postgres',
  pool: {
    max: 10,          // conexões simultâneas máximas
    min: 2,           // conexões mínimas mantidas abertas
    acquire: 30000,   // ms para aguardar conexão antes de lançar erro
    idle: 10000,      // ms ociosa antes de fechar
    evict: 1000,      // intervalo de verificação de conexões ociosas
  },
  logging: false,     // desabilita log de queries (ver seção abaixo)
});
```

**Drizzle — pool externo com `pg.Pool`**

Drizzle não tem pool embutido — você configura o pool via driver e passa para o Drizzle:

```typescript
import { Pool } from 'pg';
import { drizzle } from 'drizzle-orm/node-postgres';

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 10,                      // conexões simultâneas máximas
  min: 2,                       // conexões mínimas sempre abertas
  idleTimeoutMillis: 30000,     // fechar conexão ociosa após 30s
  connectionTimeoutMillis: 5000, // timeout para abrir conexão
});

export const db = drizzle(pool, { schema });
```

> [!tip] Regra prática de pool size
> O número ótimo de conexões não é "mais = melhor". Cada conexão consome ~5-10 MB no PostgreSQL. A fórmula empírica do pgBouncer: `max_pool = (núcleos_cpu * 2) + disco_efetivo`. Para uma instância de 4 núcleos sem SSD dedicado, o ideal é `max: 10`. Em serverless, use PgBouncer ou Prisma Accelerate — funções stateless não sustentam pool eficientemente.

### Tracing de queries

Logar queries lentas em produção é essencial para identificar N+1, missing indexes e queries problemáticas antes que impactem usuários.

**Prisma — `log` no client**

```typescript
import { PrismaClient } from '@prisma/client';

export const prisma = new PrismaClient({
  log: [
    { emit: 'event', level: 'query' },
    { emit: 'stdout', level: 'error' },
    { emit: 'stdout', level: 'warn' },
  ],
});

// Log de queries lentas (> 100ms)
prisma.$on('query', (e) => {
  if (e.duration > 100) {
    console.warn(`[SLOW QUERY] ${e.duration}ms | ${e.query} | params: ${e.params}`);
  }
});
```

O `emit: 'event'` expõe o evento `query` programaticamente em vez de logar tudo no stdout — permite filtrar por duração e integrar com APM (Datadog, New Relic).

**TypeORM — `logging` no DataSource**

```typescript
const AppDataSource = new DataSource({
  type: 'postgres',
  url: process.env.DATABASE_URL,
  logging: ['query', 'error', 'warn', 'slow'],  // ou 'all'
  maxQueryExecutionTime: 100, // loga automaticamente queries > 100ms
  logger: 'advanced-console', // 'advanced-console' | 'simple-console' | 'file'
});
```

`maxQueryExecutionTime` é o mecanismo de slow query log nativo do TypeORM: qualquer query que exceder o valor em ms é logada como `[SLOW QUERY]` automaticamente, sem código adicional.

**Sequelize — `logging` no construtor**

```typescript
const sequelize = new Sequelize(process.env.DATABASE_URL, {
  dialect: 'postgres',
  logging: (sql, timing) => {
    if (timing && timing > 100) {
      console.warn(`[SLOW QUERY] ${timing}ms | ${sql}`);
    }
  },
  benchmark: true, // habilita o parâmetro timing no callback de logging
});
```

O `benchmark: true` injeta o tempo de execução como segundo argumento no callback de `logging` — sem ele, `timing` é `undefined`.

**Drizzle — `logger` na inicialização**

```typescript
import { drizzle } from 'drizzle-orm/node-postgres';
import { Pool } from 'pg';

const pool = new Pool({ connectionString: process.env.DATABASE_URL });

export const db = drizzle(pool, {
  schema,
  logger: {
    logQuery(query: string, params: unknown[]) {
      // Drizzle não expõe timing nativamente; use pg hooks para medir
      console.log(`[QUERY] ${query}`, params);
    },
  },
});

// Para timing real, intercepte no nível do pool pg:
pool.on('query', (e) => console.log('[PG QUERY]', e.text));
```

Drizzle não tem slow query log nativo — para medir duração, instrumentalize o pool `pg` diretamente ou use middleware de OTel (OpenTelemetry) com `@opentelemetry/instrumentation-pg`.

> [!warning] Nunca logue queries com dados sensíveis em produção
> Parâmetros de query como senhas, tokens e dados PII aparecem nos logs de Prisma (`e.params`) e Sequelize. Use redaction ou filtre os parâmetros antes de logar. TypeORM e Drizzle não expõem parâmetros por padrão nos seus loggers nativos, mas o nível `pg` os expõe — cuidado ao habilitar logging de pool em produção.

## Em entrevista

**Q: "How do you choose an ORM for a new Node.js project?"**

The decision comes down to four axes: type safety requirements, team background, deployment environment, and whether the codebase is greenfield or brownfield. For TypeScript greenfield projects where developer experience and type safety matter most, Prisma is the default choice — its schema-first approach generates fully typed clients and the migration tooling is straightforward. If the team comes from a Java or Spring background, TypeORM's decorator syntax maps closely to JPA and reduces the mental model shift. For brownfield projects already using Sequelize, the cost of migrating rarely justifies switching unless there are specific performance or type safety pain points. For serverless or edge deployments where bundle size is critical, Drizzle is the clear winner — it has no runtime magic and the smallest footprint of the four. The wrong answer is choosing an ORM because it's familiar without considering the deployment context or team background.

**Q: "What is an N+1 query problem and how do you fix it?"**

The N+1 problem occurs when fetching a list of N parent records triggers N additional queries — one per parent — to resolve an association. This happens when ORMs resolve associations lazily under the hood, and it's especially dangerous because it's invisible in development with small datasets but catastrophic at scale. The standard fix is eager loading: use `include` in Prisma or Sequelize, `relations` in TypeORM, or explicit joins in Drizzle to fetch parent and child records in a single query. In GraphQL resolvers where each field resolver runs independently, eager loading alone is insufficient because resolvers compose dynamically — DataLoader is the right tool there, batching and deduplicating IDs across multiple resolver invocations into a single database query per tick of the event loop.

**Q: "When would you use cursor pagination over offset pagination?"**

Offset pagination is straightforward but has a fundamental performance problem: `OFFSET N` forces the database to scan and discard N rows before returning results, making it O(N) relative to the offset value. At 50,000+ rows this becomes a multi-second query even with indexes. Cursor pagination replaces the offset with a pointer to the last-seen row — the query filters from that position forward rather than counting rows from the beginning, so the cost stays O(1) regardless of depth. I'd use cursor pagination for any high-traffic feed, timeline, or infinite scroll feature where users routinely reach deep pages. The trade-off is that cursor pagination doesn't support random page access — you can't jump directly to page 50 — which makes it unsuitable for admin UIs where users expect numbered pagination. Keyset pagination is a specialization of cursor pagination that filters directly on an indexed column (`WHERE id > last_id`), making it the fastest option for append-heavy tables with sequential IDs.

**Q: "What's the difference between managed and manual transactions in TypeORM?"**

TypeORM offers two transaction approaches. The managed approach uses the `dataSource.transaction()` callback — TypeORM automatically commits when the callback returns and rolls back on any thrown error, so error handling is clean and there's no risk of forgetting to commit or release. The manual approach uses a `QueryRunner`: you call `connect`, `startTransaction`, `commitTransaction` or `rollbackTransaction`, and critically `release` in a `finally` block. The release call is mandatory — skipping it leaks the connection back to the pool and eventually causes `ConnectionTimeoutError` as the pool exhausts available connections. I use managed transactions by default and reach for `QueryRunner` only when I need to set a specific isolation level or implement conditional rollback logic that the callback model doesn't express cleanly.

## Casos práticos

### Cenário A — Escolhendo o ORM certo para um SaaS multi-tenant em TypeScript

Uma startup está construindo um SaaS B2B com PostgreSQL, row-level security (RLS) e necessidade de multi-schema por tenant. O time cogita Prisma, mas descobre que Prisma não suporta RLS nativo e tem suporte limitado a múltiplos schemas. A decisão final:

```typescript
// Contexto: TypeORM com QueryRunner para SET app.tenant_id antes de cada query

import { DataSource, QueryRunner } from 'typeorm';

const AppDataSource = new DataSource({
  type: 'postgres',
  url: process.env.DATABASE_URL,
  entities: [__dirname + '/entities/**/*.entity{.ts,.js}'],
  migrations: [__dirname + '/migrations/**/*{.ts,.js}'],
  synchronize: false, // NUNCA true em produção
});

// Middleware NestJS que seta o tenant_id via SET LOCAL (RLS trigger)
async function withTenantContext<T>(
  dataSource: DataSource,
  tenantId: string,
  callback: (qr: QueryRunner) => Promise<T>,
): Promise<T> {
  const qr = dataSource.createQueryRunner();
  await qr.connect();
  await qr.startTransaction();
  try {
    // Seta variável de sessão que o RLS policy do Postgres lê
    await qr.query(`SET LOCAL app.tenant_id = '${tenantId}'`);
    const result = await callback(qr);
    await qr.commitTransaction();
    return result;
  } catch (err) {
    await qr.rollbackTransaction();
    throw err;
  } finally {
    await qr.release(); // SEMPRE liberar no finally
  }
}

// Uso no service
async createOrder(tenantId: string, data: CreateOrderDto) {
  return withTenantContext(AppDataSource, tenantId, async (qr) => {
    const order = qr.manager.create(Order, data);
    return qr.manager.save(order);
  });
}
```

O TypeORM foi escolhido aqui porque o `QueryRunner` permite executar `SET LOCAL` dentro da transação — algo que APIs de alto nível como `prisma.$transaction` não expõem diretamente. O `SET LOCAL` garante que a variável de sessão é revertida junto com a transação se algo der errado.

### Cenário B — Migração zero-downtime com expand-and-contract em qualquer ORM

Uma coluna `name` precisa ser dividida em `first_name` e `last_name` sem downtime. O padrão expand-and-contract funciona com qualquer ORM e requer 3 migrations coordenadas com deploys:

```typescript
// Migration 1 — EXPAND: adiciona as novas colunas (nullable, sem remover name)
// TypeORM
export class AddFirstLastName1701000001 implements MigrationInterface {
  async up(qr: QueryRunner): Promise<void> {
    await qr.query(`
      ALTER TABLE users
        ADD COLUMN first_name VARCHAR(100),
        ADD COLUMN last_name  VARCHAR(100)
    `);
    // Backfill inicial dos dados existentes
    await qr.query(`
      UPDATE users
        SET first_name = split_part(name, ' ', 1),
            last_name  = nullif(substring(name FROM position(' ' IN name) + 1), '')
        WHERE first_name IS NULL
    `);
  }
  async down(qr: QueryRunner): Promise<void> {
    await qr.query(`ALTER TABLE users DROP COLUMN first_name, DROP COLUMN last_name`);
  }
}

// Deploy v2 — código escreve em AMBAS as colunas (name + first_name + last_name)
// Isso garante retrocompatibilidade durante o rollout gradual

// Migration 2 — BACKFILL: garante consistência total (roda após todos os pods estarem em v2)
export class BackfillNames1701000002 implements MigrationInterface {
  async up(qr: QueryRunner): Promise<void> {
    await qr.query(`
      UPDATE users
        SET first_name = split_part(name, ' ', 1),
            last_name  = nullif(substring(name FROM position(' ' IN name) + 1), '')
        WHERE first_name IS NULL OR last_name IS NULL
    `);
    // Adiciona NOT NULL agora que todos os dados estão preenchidos
    await qr.query(`ALTER TABLE users ALTER COLUMN first_name SET NOT NULL`);
    await qr.query(`ALTER TABLE users ALTER COLUMN last_name  SET NOT NULL`);
  }
  async down(qr: QueryRunner): Promise<void> {
    await qr.query(`ALTER TABLE users ALTER COLUMN first_name DROP NOT NULL`);
    await qr.query(`ALTER TABLE users ALTER COLUMN last_name  DROP NOT NULL`);
  }
}

// Deploy v3 — código lê apenas first_name/last_name, não escreve mais em name

// Migration 3 — CONTRACT: remove coluna antiga
export class DropNameColumn1701000003 implements MigrationInterface {
  async up(qr: QueryRunner): Promise<void> {
    await qr.query(`ALTER TABLE users DROP COLUMN name`);
  }
  async down(qr: QueryRunner): Promise<void> {
    await qr.query(`ALTER TABLE users ADD COLUMN name VARCHAR(200)`);
    await qr.query(`UPDATE users SET name = concat(first_name, ' ', last_name)`);
  }
}
```

O mesmo padrão funciona com Prisma (`prisma.$queryRaw`), Sequelize (`queryInterface.addColumn`) ou Drizzle (`db.execute(sql\`...\``)`). A disciplina é sempre a mesma: expand → deploy → backfill → deploy → contract.

## O que vem a seguir

Este cheatsheet encerra o galho **ORMs e banco de dados**. Você tem agora um mapa completo do ecossistema de acesso a dados em Node.js: da escolha de ORM ao ciclo de migrations, do diagnóstico de N+1 ao gerenciamento de transações e paginação.

Para aprofundar cada tópico individualmente: **[[03-Dominios/Tecnologia/Node/ORMs e banco de dados/06 - N+1 queries - detecção e DataLoader|06 - N+1]]**, **[[03-Dominios/Tecnologia/Node/ORMs e banco de dados/07 - Migrations e versionamento de schema|07 - Migrations]]**, **[[03-Dominios/Tecnologia/Node/ORMs e banco de dados/08 - Transações - gerenciamento manual vs automático|08 - Transações]]** e **[[03-Dominios/Tecnologia/Node/ORMs e banco de dados/09 - Paginação - offset, cursor e keyset|09 - Paginação]]**.

O próximo domínio natural é **performance e observabilidade** — como medir o que você acabou de construir. As notas sobre profiling, tracing e logging estão em `[[03-Dominios/Tecnologia/Node/ORMs e banco de dados/index|índice do galho]]`.

## Vocabulário consolidado

| Termo | Definição |
|---|---|
| **ORM** | Object-Relational Mapper — biblioteca que abstrai SQL mapeando tabelas para objetos ou classes |
| **Active Record** | Padrão onde a classe de modelo contém tanto os dados quanto a lógica de acesso ao banco (ex.: Sequelize) |
| **Data Mapper** | Padrão que separa a classe de domínio da lógica de persistência em um repositório (ex.: TypeORM, Prisma) |
| **Schema-first** | Abordagem onde o schema do banco é definido em um arquivo dedicado (`.prisma`) e o cliente é gerado a partir dele |
| **Eager loading** | Estratégia que carrega associações junto com a query principal, evitando N+1 |
| **Lazy loading** | Associações resolvidas sob demanda em queries separadas — causa N+1 quando usada em loops |
| **N+1 problem** | Anti-pattern onde N registros pai geram N queries adicionais para resolver associações |
| **DataLoader** | Biblioteca de batching que agrupa IDs de múltiplos resolvers em uma única query por tick do event loop |
| **Migration** | Arquivo versionado que descreve uma alteração incremental no schema do banco; nunca editar após aplicado |
| **Rollback** | Reverter uma transação ao estado anterior ao `BEGIN`; desfaz todas as operações da transação |
| **ACID** | Atomicity, Consistency, Isolation, Durability — propriedades que garantem integridade em transações |
| **Isolation level** | Grau de visibilidade de alterações não commitadas entre transações concorrentes (Read Committed, Repeatable Read, Serializable) |
| **Managed transaction** | Transação onde o ORM faz commit/rollback automaticamente via callback; menos propensa a vazamentos |
| **Manual transaction** | Transação gerenciada explicitamente pelo dev via `QueryRunner` ou similar; exige `release()` no `finally` |
| **Offset pagination** | Paginação via `LIMIT/OFFSET` SQL; simples mas O(N) em datasets grandes |
| **Cursor pagination** | Paginação via token opaco que aponta para a última linha vista; O(1) e estável com inserts |
| **Keyset pagination** | Filtragem direta em coluna indexada (`WHERE col > last_val`); também chamado de seek method |
| **Opaque cursor** | Token enviado ao cliente que codifica posição no dataset sem expor detalhes internos (ID, timestamp) |
| **Connection pool** | Conjunto de conexões de banco reutilizáveis; `QueryRunner.release()` devolve a conexão ao pool |

## Fontes

- [Prisma docs — Getting Started](https://www.prisma.io/docs/getting-started) — guia oficial schema-first
- [TypeORM docs — Data Source](https://typeorm.io/data-source) — DataSource, QueryRunner, migrations
- [Sequelize v7 docs](https://sequelize.org/docs/v7/) — API atualizada com melhor suporte a TypeScript
- [Drizzle ORM docs](https://orm.drizzle.team/docs/overview) — schema, queries, drizzle-kit
- [Prisma vs TypeORM vs Sequelize vs Drizzle — comparação 2024](https://www.prisma.io/dataguide/postgresql/reading-and-querying-data/comparing-orms) — benchmarks e trade-offs
- [Martin Fowler — DataMapper](https://martinfowler.com/eaaCatalog/dataMapper.html) — padrão original
- [Expand-and-Contract pattern](https://www.infoq.com/videos/expand-contract-pattern/) — zero-downtime migrations

## Veja também

- `[[ORMs e banco de dados]]` — MOC do galho
- `[[01 - Panorama de ORMs]]` — comparação inicial dos 4 ORMs
- `[[02 - Sequelize - queries e associações]]` — API Sequelize em detalhe
- `[[03 - Prisma - schema-first e type safety]]` — schema Prisma, `$transaction`, cursor nativo
- `[[04 - TypeORM - decorators ao estilo JPA]]` — decorators, QueryRunner, DataSource
- `[[05 - Drizzle - ORM lightweight e type-safe]]` — sintaxe Drizzle, joins, transactions
- `[[06 - N+1 queries - detecção e DataLoader]]` — diagnóstico e DataLoader em profundidade
- `[[07 - Migrations e versionamento de schema]]` — ciclo de vida de migrations nos 4 ORMs
- `[[08 - Transações - gerenciamento manual vs automático]]` — ACID, isolation levels, padrões por ORM
- `[[09 - Paginação - offset, cursor e keyset]]` — offset, cursor, keyset em profundidade
