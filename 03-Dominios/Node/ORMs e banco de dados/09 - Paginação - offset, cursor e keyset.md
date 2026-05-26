---
title: "Paginação - offset, cursor e keyset"
created: 2026-05-12
updated: 2026-05-12
type: concept
status: growing
publish: true
tags:
  - node
  - orm
  - paginação
  - banco-de-dados
aliases:
  - Paginação Node
  - Paginação com ORM
---

# Paginação - offset, cursor e keyset

> [!abstract] TL;DR
> Offset pagination é simples mas degrada em tabelas grandes: `OFFSET N` força o banco a varrer N linhas antes de retornar qualquer resultado (O(N)). Cursor pagination usa um ponteiro opaco para a última linha vista, mantendo O(1) independentemente da posição na tabela. Keyset pagination filtra diretamente em colunas indexadas (`WHERE id > last_id`), sendo a estratégia mais rápida para tabelas com inserções frequentes. Cada ORM tem suporte nativo: Prisma via `cursor` + `skip: 1`, Sequelize via `limit`/`offset` e `Op.gt`, TypeORM via `findAndCount` e QueryBuilder, Drizzle via `.where(gt(...))`. Decisão: offset para admin UIs com acesso aleatório a páginas, cursor/keyset para infinite scroll e feeds.

## Como funciona

### Conceitos fundamentais

**Offset pagination**

A estratégia mais comum e mais simples. O banco descarta os primeiros N resultados e retorna os próximos K.

```sql
SELECT * FROM users ORDER BY id LIMIT 10 OFFSET 990;
```

O problema fundamental: o banco precisa identificar e varrer as 990 linhas antes de retornar as 10 desejadas. Em PostgreSQL, isso significa leitura de índice ou heap sequencial até a linha 1000 — o custo cresce linearmente com o offset.

- Use case: admin UIs, tabelas pequenas (menos de 100k linhas), situações onde o usuário precisa acessar uma página arbitrária diretamente.

**Cursor pagination**

Usa um token opaco que codifica a posição da última linha vista. Internamente, o banco filtra a partir desse ponto em vez de contar e descartar.

```sql
SELECT * FROM posts WHERE id > 42 ORDER BY id LIMIT 10;
```

Estável: inserções e deleções entre requisições não deslocam os resultados porque a âncora é posicional, não numérica. Limitação: não é possível pular para uma página arbitrária — a navegação é estritamente linear (próximo / anterior).

**Keyset pagination**

Filtra diretamente nas colunas indexadas, suportando chaves compostas para desempate quando a coluna de ordenação não é única.

```sql
SELECT * FROM events
WHERE (created_at, id) < ($last_created_at, $last_id)
ORDER BY created_at DESC, id DESC
LIMIT 10;
```

Quando o índice composto existe, o banco usa uma única operação de seek — O(1) independentemente do tamanho da tabela. É a estratégia mais performática para tabelas append-only com IDs sequenciais ou timestamps.

**Comparação**

| Estratégia | Performance em tabelas grandes | Acesso aleatório | Estável com inserts |
|---|---|---|---|
| Offset | ❌ O(N) | ✅ sim | ❌ não |
| Cursor | ✅ O(1) | ❌ não | ✅ sim |
| Keyset | ✅ O(1) | ❌ não | ✅ sim |

### Paginação em Prisma

**Offset com contagem total:**

```typescript
async function listarUsuariosOffset(pagina: number, porPagina: number) {
  const [usuarios, total] = await prisma.$transaction([
    prisma.user.findMany({
      skip: (pagina - 1) * porPagina,
      take: porPagina,
      orderBy: { createdAt: 'desc' },
    }),
    prisma.user.count(),
  ]);
  return { usuarios, total, paginas: Math.ceil(total / porPagina) };
}
```

**Cursor (Prisma nativo):**

```typescript
async function listarPostsCursor(cursor?: string, limite = 10) {
  const posts = await prisma.post.findMany({
    take: limite + 1, // busca 1 a mais para detectar hasNextPage
    ...(cursor && {
      cursor: { id: cursor },
      skip: 1, // pula o próprio cursor
    }),
    orderBy: { id: 'asc' },
    select: { id: true, title: true, createdAt: true },
  });

  const hasNextPage = posts.length > limite;
  if (hasNextPage) posts.pop();

  return {
    posts,
    nextCursor: hasNextPage ? posts[posts.length - 1].id : null,
  };
}
```

> [!tip] Cursor no Prisma é o valor bruto
> O Prisma cursor usa o campo como opaque pointer — passe o valor bruto (string/int), não um token base64 codificado. O encoding fica na camada de API se necessário.

### Paginação em TypeORM

**Offset com `findAndCount`:**

```typescript
async function listarProdutosOffset(pagina: number, porPagina: number) {
  const [produtos, total] = await productRepository.findAndCount({
    skip: (pagina - 1) * porPagina,
    take: porPagina,
    order: { createdAt: 'DESC' },
  });
  return { produtos, total, paginas: Math.ceil(total / porPagina) };
}
```

**Keyset com QueryBuilder:**

```typescript
async function listarProdutosKeyset(lastId?: number, limite = 10) {
  const qb = productRepository
    .createQueryBuilder('p')
    .orderBy('p.id', 'ASC')
    .take(limite + 1);

  if (lastId !== undefined) {
    qb.where('p.id > :lastId', { lastId });
  }

  const produtos = await qb.getMany();
  const hasNextPage = produtos.length > limite;
  if (hasNextPage) produtos.pop();

  return {
    produtos,
    nextId: hasNextPage ? produtos[produtos.length - 1].id : null,
  };
}
```

### Paginação em Sequelize

**Offset com `findAndCountAll`:**

```typescript
async function listarOrdensOffset(pagina: number, porPagina: number) {
  const { rows: ordens, count: total } = await Order.findAndCountAll({
    limit: porPagina,
    offset: (pagina - 1) * porPagina,
    order: [['createdAt', 'DESC']],
  });
  return { ordens, total, paginas: Math.ceil(total / porPagina) };
}
```

**Keyset com `Op.gt`:**

```typescript
import { Op } from 'sequelize';

async function listarOrdensKeyset(lastId?: number, limite = 10) {
  const ordens = await Order.findAll({
    limit: limite + 1,
    where: lastId !== undefined ? { id: { [Op.gt]: lastId } } : {},
    order: [['id', 'ASC']],
  });

  const hasNextPage = ordens.length > limite;
  if (hasNextPage) ordens.pop();

  return {
    ordens,
    nextId: hasNextPage ? ordens[ordens.length - 1].id : null,
  };
}
```

### Paginação em Drizzle

**Offset:**

```typescript
import { desc, count } from 'drizzle-orm';

async function listarEventosOffset(pagina: number, porPagina: number) {
  const [eventos, [{ total }]] = await Promise.all([
    db
      .select()
      .from(events)
      .orderBy(desc(events.createdAt))
      .limit(porPagina)
      .offset((pagina - 1) * porPagina),
    db.select({ total: count() }).from(events),
  ]);
  return { eventos, total, paginas: Math.ceil(total / porPagina) };
}
```

**Keyset:**

```typescript
import { gt } from 'drizzle-orm';

async function listarEventosKeyset(lastId?: number, limite = 10) {
  const eventos = await db
    .select()
    .from(events)
    .where(lastId !== undefined ? gt(events.id, lastId) : undefined)
    .orderBy(asc(events.id))
    .limit(limite + 1);

  const hasNextPage = eventos.length > limite;
  if (hasNextPage) eventos.pop();

  return {
    eventos,
    nextId: hasNextPage ? eventos[eventos.length - 1].id : null,
  };
}
```

> [!tip] `undefined` em `.where()` no Drizzle (≥ 0.29)
> No Drizzle ORM ≥ 0.29, passe `undefined` para `.where()` para omitir o filtro — o ORM ignora cláusulas `undefined` automaticamente, eliminando condicionais de string.

## Quando usar

| Caso de uso | Estratégia recomendada | Motivo |
|---|---|---|
| Admin UI com acesso a página arbitrária | Offset | Random access necessário |
| Feed de posts / timeline | Cursor ou Keyset | Estável, O(1) |
| Tabela < 100k linhas | Offset | Diferença de performance negligível |
| Export em lote (ETL, relatório) | Keyset | Predictable memory, sem drift |
| API pública com `page=` | Offset | Expectativa de devs externos |
| Infinite scroll mobile | Cursor | Token opaco, simples de implementar |
| Tabela append-only com ID sequencial | Keyset | Mais simples que cursor, mesma performance |

## Armadilhas comuns

> [!danger] COUNT(*) em cursor pagination anula o ganho de performance
> `COUNT(*)` realiza um full table scan e anula completamente o benefício de O(1) do cursor. Cursor pagination não tem total de páginas por design — use estimativas via `EXPLAIN`, estatísticas da tabela, ou simplesmente omita o total da resposta.

> [!danger] Ordenação sem índice transforma keyset/cursor em O(N)
> Keyset e cursor pagination sobre uma coluna sem índice forçam o banco a fazer um full table scan para encontrar o ponto de corte. Sempre crie o índice antes de adotar essas estratégias: `CREATE INDEX ON tabela (coluna_sort)` ou `CREATE INDEX ON tabela (coluna_sort, id)` para chave composta.

> [!danger] OFFSET em tabelas grandes é lento por design
> `OFFSET 50000 LIMIT 10` instrui o banco a ler 50.010 linhas e descartar 50.000. Em PostgreSQL com 1 milhão de linhas e sem índice cobrindo a ordenação, isso pode levar mais de 1 segundo — e o custo cresce linearmente com o offset.

> [!danger] Cursor instável com colunas não únicas quebra a paginação
> Um cursor baseado apenas em `created_at` quebra silenciosamente quando múltiplas linhas têm o mesmo timestamp: algumas linhas serão puladas ou repetidas entre páginas. Sempre use um tiebreaker — defina o keyset como `(created_at, id)` para garantir ordenação determinística e estável.

> [!danger] Esquecer `take: limite + 1` força um COUNT extra
> Sem buscar N+1 itens, a única forma de saber se existe uma próxima página é executar um `COUNT(*)` separado — que é caro e inconsistente com reads concorrentes. O padrão canônico é: busque `limite + 1`, verifique `length > limite`, remova o último item com `.pop()`, e use o ID do último item retornado como `nextCursor`.

## Em entrevista

**Q: "Why does OFFSET pagination degrade at scale, and what would you use instead?"**

OFFSET pagination forces the database to perform a full table scan up to the offset position — fetching `OFFSET 50000 LIMIT 10` reads 50,010 rows and discards 50,000 of them, making it O(N) relative to the offset value. On large tables this translates to multi-second query times even with indexes on the sort column, because the database must traverse the index to count rows rather than seek directly to a position. For high-traffic or large-dataset scenarios I would switch to cursor-based or keyset pagination, both of which are O(1) regardless of how deep into the dataset the client is. Keyset pagination in particular — filtering on an indexed column with `WHERE id > last_id` — leverages a single index seek and is ideal for append-heavy tables with sequential IDs. The trade-off is losing random page access, which is acceptable for feeds and infinite scroll but not for admin UIs requiring arbitrary page jumps.

**Q: "How does cursor pagination work, and what are its trade-offs?"**

Cursor pagination encodes the position of the last-seen row into an opaque token — the raw primary key or composite key value, optionally base64-encoded at the API layer for opacity — which the client sends back on the next request to anchor the query at that exact position. Because the query filters from a known row forward rather than counting and skipping, it delivers stable results even when rows are inserted or deleted between requests, and the query cost stays constant regardless of how many pages have already been consumed. The primary trade-off is that there is no random access: the client cannot jump to page 5 without having traversed pages 1 through 4, and there is no meaningful concept of a total page count. Implementing `hasNextPage` correctly requires the N+1 fetch pattern — requesting one extra item, checking if it exists, and popping it before returning the response — to avoid an expensive COUNT query. This model is well-suited for infinite scroll and social feeds but a poor fit for UIs where users expect to navigate directly to a specific page number.

## Vocabulário

| Termo | Definição |
|---|---|
| **offset pagination** | Estratégia de paginação que usa `LIMIT` e `OFFSET` SQL; simples mas O(N) em datasets grandes |
| **cursor pagination** | Paginação baseada em um token opaco que aponta para a última linha vista; O(1) e estável |
| **keyset pagination** | Filtragem direta em colunas indexadas (`WHERE col > last_val`); também chamado de seek method |
| **opaque cursor** | Token enviado ao cliente que codifica a posição no dataset sem expor detalhes internos (ex.: ID, timestamp) |
| **hasNextPage** | Flag booleana que indica se existe uma próxima página; detectada via N+1 fetch pattern |
| **tiebreaker** | Coluna secundária (geralmente `id`) usada para desambiguar linhas com o mesmo valor na coluna de ordenação primária |
| **full table scan** | Leitura de todas as linhas de uma tabela; o que acontece quando OFFSET é alto ou falta índice na ordenação |
| **N+1 fetch pattern** | Buscar `limite + 1` itens para detectar `hasNextPage` sem executar um COUNT separado |
| **índice composto** | Índice em múltiplas colunas (ex.: `(created_at, id)`); essencial para keyset pagination com tiebreaker |
| **stable pagination** | Propriedade de cursor/keyset: inserts e deletes entre páginas não causam linhas duplicadas ou puladas |
| **infinite scroll** | Padrão de UX que carrega mais conteúdo conforme o usuário rola; caso de uso canônico para cursor pagination |
| **seek method** | Outro nome para keyset pagination; referência ao seek de índice que o banco executa internamente |
| **findAndCount / findAndCountAll** | Métodos de ORM (TypeORM / Sequelize) que executam SELECT e COUNT em uma única chamada |
| **drift de paginação** | Fenômeno em offset pagination onde inserts/deletes causam repetição ou omissão de linhas entre páginas |

## Veja também

- `[[ORMs e banco de dados]]` — MOC do galho
- `[[06 - N+1 queries - detecção e DataLoader]]` — N+1 em associações, mesmo padrão de N+1 fetch
- `[[08 - Transações - gerenciamento manual vs automático]]` — transações e locking em contexto de leitura
- `[[10 - Cheatsheet e decision tree de ORMs]]` — próxima nota
