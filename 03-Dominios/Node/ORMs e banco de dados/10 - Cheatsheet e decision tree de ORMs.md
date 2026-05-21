---
title: "Cheatsheet e decision tree de ORMs"
created: 2026-05-12
updated: 2026-05-12
type: concept
status: growing
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

## Em entrevista

**Q: "How do you choose an ORM for a new Node.js project?"**

The decision comes down to four axes: type safety requirements, team background, deployment environment, and whether the codebase is greenfield or brownfield. For TypeScript greenfield projects where developer experience and type safety matter most, Prisma is the default choice — its schema-first approach generates fully typed clients and the migration tooling is straightforward. If the team comes from a Java or Spring background, TypeORM's decorator syntax maps closely to JPA and reduces the mental model shift. For brownfield projects already using Sequelize, the cost of migrating rarely justifies switching unless there are specific performance or type safety pain points. For serverless or edge deployments where bundle size is critical, Drizzle is the clear winner — it has no runtime magic and the smallest footprint of the four. The wrong answer is choosing an ORM because it's familiar without considering the deployment context or team background.

**Q: "What is an N+1 query problem and how do you fix it?"**

The N+1 problem occurs when fetching a list of N parent records triggers N additional queries — one per parent — to resolve an association. This happens when ORMs resolve associations lazily under the hood, and it's especially dangerous because it's invisible in development with small datasets but catastrophic at scale. The standard fix is eager loading: use `include` in Prisma or Sequelize, `relations` in TypeORM, or explicit joins in Drizzle to fetch parent and child records in a single query. In GraphQL resolvers where each field resolver runs independently, eager loading alone is insufficient because resolvers compose dynamically — DataLoader is the right tool there, batching and deduplicating IDs across multiple resolver invocations into a single database query per tick of the event loop.

**Q: "When would you use cursor pagination over offset pagination?"**

Offset pagination is straightforward but has a fundamental performance problem: `OFFSET N` forces the database to scan and discard N rows before returning results, making it O(N) relative to the offset value. At 50,000+ rows this becomes a multi-second query even with indexes. Cursor pagination replaces the offset with a pointer to the last-seen row — the query filters from that position forward rather than counting rows from the beginning, so the cost stays O(1) regardless of depth. I'd use cursor pagination for any high-traffic feed, timeline, or infinite scroll feature where users routinely reach deep pages. The trade-off is that cursor pagination doesn't support random page access — you can't jump directly to page 50 — which makes it unsuitable for admin UIs where users expect numbered pagination. Keyset pagination is a specialization of cursor pagination that filters directly on an indexed column (`WHERE id > last_id`), making it the fastest option for append-heavy tables with sequential IDs.

**Q: "What's the difference between managed and manual transactions in TypeORM?"**

TypeORM offers two transaction approaches. The managed approach uses the `dataSource.transaction()` callback — TypeORM automatically commits when the callback returns and rolls back on any thrown error, so error handling is clean and there's no risk of forgetting to commit or release. The manual approach uses a `QueryRunner`: you call `connect`, `startTransaction`, `commitTransaction` or `rollbackTransaction`, and critically `release` in a `finally` block. The release call is mandatory — skipping it leaks the connection back to the pool and eventually causes `ConnectionTimeoutError` as the pool exhausts available connections. I use managed transactions by default and reach for `QueryRunner` only when I need to set a specific isolation level or implement conditional rollback logic that the callback model doesn't express cleanly.

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
