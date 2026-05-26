---
title: "Prisma - schema-first e type safety"
created: 2026-05-10
updated: 2026-05-10
type: concept
status: seedling
progresso: andamento
aliases:
  - Prisma Node
  - Prisma schema-first
publish: false
tags:
  - node
  - orm
  - prisma
  - type-safety
  - banco-de-dados
---

# Prisma - schema-first e type safety

> [!abstract] TL;DR
> O Prisma v6 em 2026 é o ORM com melhor DX do ecossistema [[Node.js]] — você define o banco de dados inteiro em um único arquivo `schema.prisma` (declarativo, fácil de ler), e o Prisma Client gerado automaticamente carrega types TypeScript precisos para cada operação, eliminando a necessidade de escrever tipos manualmente.
> O Prisma Migrate versiona o schema em arquivos SQL gerados automaticamente (`prisma/migrations/`), garantindo rastreabilidade completa das mudanças; o Prisma Studio oferece inspeção visual do banco via browser sem instalar nada.
> A grande virada do v6 foi a migração do query engine para **WASM rodando in-process** — ao contrário das versões anteriores que dependiam de um binário sidecar separado, o WASM engine embutido permite que o Prisma Client funcione nativamente em edge runtimes (Cloudflare Workers, Vercel Edge, Deno Deploy) sem configuração extra.
> Prisma Accelerate GA adiciona connection pooling global e cache de queries em CDN, tornando o Prisma a escolha natural para arquiteturas serverless e edge onde conexões de banco são caras e latência é crítica.
> Para devs TypeScript migrando de outros ecossistemas, a curva de aprendizado é menor do que TypeORM (sem decorators) e o type safety é mais completo do que Sequelize v7 sem configuração adicional.

## O que é

O Prisma é descrito pela própria equipe como um **toolkit de banco de dados** — não apenas um ORM. Essa distinção importa: enquanto um ORM clássico foca em mapear objetos para tabelas, o Prisma cobre o ciclo completo de trabalho com banco de dados em três camadas complementares.

### As três camadas do Prisma

**Prisma Client** é o cliente gerado automaticamente a partir do `schema.prisma`. Após rodar `prisma generate`, você tem um módulo TypeScript com classes e métodos completamente tipados para cada model, relação e operação definida no schema. O tipo de retorno de cada query é inferido com precisão — se você fizer um `findMany` com `select` apenas para `id` e `name`, o tipo de retorno reflete exatamente esses dois campos.

**Prisma Migrate** é o sistema de migrations baseado em schema declarativo. Você edita o `schema.prisma`, roda `prisma migrate dev`, e o Prisma detecta o diff entre o estado atual e o desejado, gera um arquivo `.sql` com as alterações e aplica ao banco de desenvolvimento. Os arquivos de migration ficam em `prisma/migrations/` e devem ser commitados — são a fonte de verdade do histórico do schema.

**Prisma Studio** é um GUI web gerado localmente com `prisma studio`. Abre um browser com visualização de todas as tabelas, permite criar, editar e deletar registros sem escrever SQL — útil para inspeção rápida durante desenvolvimento e debugging de dados.

### Breve histórico e posição em 2026

O Prisma surgiu como "Prisma 1" em 2018 com uma arquitetura radicalmente diferente (servidor GraphQL intermediário). A partir de 2019 o time refez tudo do zero — o "Prisma 2" (hoje simplesmente Prisma) lançou GA em 2021 com a arquitetura atual de schema-first e client gerado. O v5 trouxe melhorias de performance e o v6 (2024) substituiu o query engine binário por WASM in-process, resolvendo de vez a incompatibilidade com edge runtimes.

Em 2026, o Prisma ocupa a posição de **melhor DX entre os ORMs Node.js** — type safety automático, migrations gerenciadas, documentação excelente. A desvantagem histórica de performance (overhead do engine externo) desapareceu com o WASM in-process do v6, tornando a adoção mais defensável em stacks de alta performance.

---

## Como funciona

### Schema Prisma

Toda configuração do Prisma vive em um único arquivo: `prisma/schema.prisma`. O arquivo é dividido em blocos com funções distintas.

**Bloco `datasource`** — configura a conexão com o banco:

```prisma
// prisma/schema.prisma
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}
```

`provider` aceita `postgresql`, `mysql`, `sqlite`, `sqlserver`, `mongodb` e `cockroachdb`. A URL é sempre lida de variável de ambiente — nunca hardcoded.

**Bloco `generator`** — configura o que será gerado:

```prisma
generator client {
  provider = "prisma-client-js"
}
```

Em 2026, `prisma-client-js` é o padrão. Existem geradores da comunidade para outros targets (Dart, Go, etc.), mas o oficial é esse.

**Blocos `model`** — definem as entidades. Cada model vira uma tabela no banco e uma interface TypeScript no client gerado:

```prisma
// prisma/schema.prisma — exemplo completo com 3 models relacionados

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

generator client {
  provider = "prisma-client-js"
}

model User {
  id        Int      @id @default(autoincrement())
  email     String   @unique
  name      String?
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  posts     Post[]
  profile   Profile?
}

model Profile {
  id     Int     @id @default(autoincrement())
  bio    String?
  userId Int     @unique

  user   User    @relation(fields: [userId], references: [id])
}

model Post {
  id          Int       @id @default(autoincrement())
  title       String
  content     String?
  published   Boolean   @default(false)
  createdAt   DateTime  @default(now())
  authorId    Int

  author      User      @relation(fields: [authorId], references: [id])
  tags        Tag[]
}

model Tag {
  id    Int    @id @default(autoincrement())
  name  String @unique

  posts Post[]
}
```

**Tipos de campo disponíveis:**

| Tipo Prisma | Tipo TypeScript gerado | Exemplo no banco (PostgreSQL) |
|-------------|------------------------|-------------------------------|
| `String`    | `string`               | `TEXT` / `VARCHAR`            |
| `Int`       | `number`               | `INTEGER`                     |
| `BigInt`    | `bigint`               | `BIGINT`                      |
| `Float`     | `number`               | `DOUBLE PRECISION`            |
| `Decimal`   | `Decimal`              | `DECIMAL`                     |
| `Boolean`   | `boolean`              | `BOOLEAN`                     |
| `DateTime`  | `Date`                 | `TIMESTAMP`                   |
| `Json`      | `JsonValue`            | `JSONB` (PostgreSQL)          |
| `Bytes`     | `Buffer`               | `BYTEA`                       |

**Modificadores de campo:**

- `?` — campo opcional (`String?` → `string | null` no TypeScript)
- `[]` — array de relação (só para campos de relação, não para tipos escalares no PostgreSQL padrão)

**Atributos de campo importantes:**

- `@id` — chave primária
- `@unique` — constraint de unicidade
- `@default(value)` — valor padrão (`autoincrement()`, `now()`, `uuid()`, `cuid()`, literal)
- `@updatedAt` — atualizado automaticamente pelo Prisma a cada update
- `@relation(fields: [...], references: [...])` — define a FK e a referência

**Atributos de model (nível de bloco):**

```prisma
model Post {
  id       Int    @id
  title    String
  authorId Int

  @@index([authorId])
  @@unique([title, authorId])
}
```

**Enums:**

```prisma
enum Role {
  USER
  ADMIN
  MODERATOR
}

model User {
  id   Int    @id @default(autoincrement())
  role Role   @default(USER)
}
```

---

### Prisma Client — CRUD

Após rodar `prisma generate`, o Prisma Client fica disponível em `@prisma/client`. A prática padrão é criar uma instância singleton:

```typescript
// lib/prisma.ts
import { PrismaClient } from '@prisma/client'

const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined
}

export const prisma =
  globalForPrisma.prisma ??
  new PrismaClient({
    log: process.env.NODE_ENV === 'development' ? ['query', 'error', 'warn'] : ['error'],
  })

if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = prisma
```

O padrão singleton com `globalThis` evita criar múltiplas instâncias durante hot-reload em desenvolvimento (Next.js, Vite, etc.).

**Operações de leitura:**

```typescript
import { prisma } from './lib/prisma'

// findMany — retorna array, nunca null
const users = await prisma.user.findMany()

// findFirst — retorna o primeiro match ou null
const user = await prisma.user.findFirst({
  where: { email: { contains: '@example.com' } },
})

// findUnique — requer campo @id ou @unique; retorna null se não encontrar
const user = await prisma.user.findUnique({
  where: { email: 'alice@example.com' },
})

// findUniqueOrThrow — igual ao findUnique mas lança PrismaClientKnownRequestError se não encontrar
// Útil para rotas onde a ausência é um erro de negócio
const user = await prisma.user.findUniqueOrThrow({
  where: { id: 1 },
})
```

**Filtros compostos com `where`:**

```typescript
// AND implícito — objeto com múltiplos campos
const posts = await prisma.post.findMany({
  where: {
    published: true,
    authorId: 1,
  },
})

// OR explícito
const posts = await prisma.post.findMany({
  where: {
    OR: [
      { title: { contains: 'Node' } },
      { title: { contains: 'TypeScript' } },
    ],
  },
})

// NOT
const users = await prisma.user.findMany({
  where: {
    NOT: { email: { endsWith: '@spam.com' } },
  },
})

// Filtros escalares disponíveis: equals, not, in, notIn, lt, lte, gt, gte,
// contains, startsWith, endsWith, mode (case insensitive)
```

**Paginação com `take`, `skip` e `cursor`:**

```typescript
// Offset pagination — simples mas O(n) no banco para pages grandes
const page2 = await prisma.post.findMany({
  orderBy: { createdAt: 'desc' },
  take: 10,
  skip: 10, // pula os 10 primeiros
})

// Cursor pagination — eficiente, baseado em posição real
const nextPage = await prisma.post.findMany({
  take: 10,
  cursor: { id: lastSeenId },
  skip: 1, // skip o próprio cursor
  orderBy: { id: 'asc' },
})
```

**Operações de escrita:**

```typescript
// create — cria um registro
const newUser = await prisma.user.create({
  data: {
    email: 'bob@example.com',
    name: 'Bob',
  },
})

// createMany — cria múltiplos (sem retornar os criados por padrão)
const result = await prisma.user.createMany({
  data: [
    { email: 'alice@example.com', name: 'Alice' },
    { email: 'carol@example.com', name: 'Carol' },
  ],
  skipDuplicates: true, // ignora registros que violam @unique
})
// result = { count: 2 }

// update — atualiza por @id ou @unique, erro se não encontrar
const updated = await prisma.user.update({
  where: { id: 1 },
  data: { name: 'Alice Updated' },
})

// updateMany — atualiza múltiplos, retorna count
const { count } = await prisma.post.updateMany({
  where: { published: false },
  data: { published: true },
})

// upsert — cria se não existir, atualiza se existir
const user = await prisma.user.upsert({
  where: { email: 'alice@example.com' },
  create: { email: 'alice@example.com', name: 'Alice' },
  update: { name: 'Alice Updated' },
})

// delete — deleta por @id ou @unique
await prisma.user.delete({ where: { id: 1 } })

// deleteMany — deleta múltiplos, retorna count
const { count } = await prisma.post.deleteMany({
  where: { published: false },
})
```

**`select` vs `include` — diferença fundamental:**

`select` é **projeção**: escolhe quais campos do model retornar. O tipo de retorno reflete exatamente os campos selecionados — se você selecionar só `id` e `name`, o TypeScript não deixará acessar `email` no resultado.

`include` é **eager loading**: carrega models relacionados inteiros junto com o model principal.

```typescript
// select — retorna { id: number; name: string | null }[]
// TypeScript não permite acessar .email no resultado
const users = await prisma.user.findMany({
  select: {
    id: true,
    name: true,
    // email: false — omitir é o padrão
  },
})

// include — retorna User com posts: Post[] carregados
const users = await prisma.user.findMany({
  include: {
    posts: true,
  },
})

// select + include podem coexistir via select com campos de relação
// Isso é a forma de fazer projection granular + eager loading juntos
const users = await prisma.user.findMany({
  select: {
    id: true,
    name: true,
    posts: {
      select: {
        id: true,
        title: true,
      },
    },
  },
})
```

---

### Relações e includes

**Relações aninhadas com `include`:**

```typescript
// Carrega user com posts e, para cada post, carrega as tags
const userWithPostsAndTags = await prisma.user.findUnique({
  where: { id: 1 },
  include: {
    posts: {
      where: { published: true },
      orderBy: { createdAt: 'desc' },
      take: 5,
      include: {
        tags: true,
      },
    },
    profile: true,
  },
})
```

**`_count` para contar sem carregar:**

Usar `include: { posts: true }` para só contar quantos posts um usuário tem é desperdício — carrega todos os dados de posts para usar apenas `.length`. A forma correta:

```typescript
// _count — retorna { id, name, _count: { posts: number } }
const usersWithPostCount = await prisma.user.findMany({
  select: {
    id: true,
    name: true,
    _count: {
      select: { posts: true },
    },
  },
})

// Acessar: usersWithPostCount[0]._count.posts
```

**Gerenciando relações no `create` e `update` com `connect`/`disconnect`/`set`:**

```typescript
// create com relação — connect associa a um registro existente
const post = await prisma.post.create({
  data: {
    title: 'Prisma v6',
    author: {
      connect: { id: 1 }, // associa ao User com id=1
    },
    tags: {
      connect: [{ id: 1 }, { id: 2 }], // associa tags existentes
    },
  },
})

// update com disconnect — remove associação sem deletar o registro
await prisma.post.update({
  where: { id: 1 },
  data: {
    tags: {
      disconnect: [{ id: 2 }], // remove tag 2 do post
    },
  },
})

// set — substitui todas as relações de uma vez (operação destrutiva)
await prisma.post.update({
  where: { id: 1 },
  data: {
    tags: {
      set: [{ id: 3 }, { id: 4 }], // remove todas as tags anteriores e define [3, 4]
    },
  },
})

// create dentro de relação — cria e associa em uma transação implícita
const user = await prisma.user.create({
  data: {
    email: 'new@example.com',
    profile: {
      create: { bio: 'Desenvolvedor Node.js' },
    },
  },
})
```

---

### Prisma Migrate

O Prisma Migrate é o sistema de controle de versão do schema. Entender o fluxo correto dev vs prod é crítico.

**Fluxo de desenvolvimento:**

```bash
# 1. Editar prisma/schema.prisma
# 2. Gerar e aplicar a migration ao banco de dev
npx prisma migrate dev --name add_user_role

# O comando acima:
# - Detecta diff entre schema atual e banco
# - Gera prisma/migrations/20260510120000_add_user_role/migration.sql
# - Aplica o SQL ao banco de desenvolvimento
# - Roda prisma generate automaticamente (atualiza o client)
```

O arquivo gerado em `prisma/migrations/` é SQL puro — você pode e deve revisá-lo antes de commitar. Em casos de dados sensíveis (ex: renomear coluna), pode ser necessário editar o SQL da migration para preservar dados.

**`prisma db push` — apenas para prototipagem rápida:**

```bash
# Sincroniza o schema direto no banco SEM criar migration files
# Usar apenas em desenvolvimento/prototipagem — nunca em produção
npx prisma db push
```

`prisma db push` é útil quando você está explorando um modelo de dados e não quer se preocupar com migration files ainda. Quando o design estiver consolidado, descarta o banco de dev e usa `prisma migrate dev` para criar o histórico limpo.

**Fluxo de produção:**

```bash
# Em produção (CI/CD), aplica as migrations pendentes
# NÃO gera novas migrations, NÃO roda prisma generate
npx prisma migrate deploy
```

`prisma migrate deploy` lê os arquivos em `prisma/migrations/`, verifica quais já foram aplicados (tabela `_prisma_migrations` no banco), e aplica apenas os pendentes em ordem. É idempotente e seguro para pipelines CI/CD.

**Regra de ouro:**
- `prisma migrate dev` → só em desenvolvimento local
- `prisma db push` → só em prototipagem/dev, nunca em produção
- `prisma migrate deploy` → produção, staging, qualquer ambiente além do local

**Introspecting banco existente:**

```bash
# Gera schema.prisma a partir de um banco existente
npx prisma db pull
```

Útil para migrar um projeto legado para Prisma sem reescrever o banco do zero.

---

### Raw queries e escape de type safety

Prisma Client cobre a maioria dos casos de uso, mas há situações onde SQL bruto é necessário: window functions, CTEs recursivas, queries com sintaxe específica do banco que o Prisma não suporta.

**`$queryRaw` — SELECT com resultado tipado:**

```typescript
import { Prisma } from '@prisma/client'
import { prisma } from './lib/prisma'

// CORRETO — usa Prisma.sql para parametrização segura
const userId = 1
const result = await prisma.$queryRaw<{ id: number; name: string }[]>(
  Prisma.sql`SELECT id, name FROM "User" WHERE id = ${userId}`
)
// userId é automaticamente parametrizado — sem risco de SQL injection

// ERRADO — interpolação de string direta (SQL injection!)
// NUNCA faça isso:
const result = await prisma.$queryRaw(`SELECT * FROM "User" WHERE id = ${userId}`)
```

O `Prisma.sql` é um tagged template literal que automaticamente converte os valores interpolados em parâmetros (`$1`, `$2`, etc.) para o banco — o valor nunca é inserido diretamente na string SQL.

**`$executeRaw` — DML sem retorno de dados:**

```typescript
// Para INSERT, UPDATE, DELETE em raw SQL
// Retorna o número de linhas afetadas
const affectedRows = await prisma.$executeRaw(
  Prisma.sql`UPDATE "Post" SET published = true WHERE "createdAt" < ${thirtyDaysAgo}`
)
```

**Quando usar raw queries:**

- Window functions: `ROW_NUMBER() OVER (PARTITION BY ...)`, `LAG()`, `LEAD()`
- CTEs: `WITH recursive ...`
- Full-text search avançado no PostgreSQL (`tsquery`, `tsvector`)
- Bulk operations com sintaxe específica do banco
- Funções de banco de dados customizadas

**Atenção ao tipo de retorno de `$queryRaw`:** o TypeScript aceita o generic, mas o Prisma não valida o tipo em runtime — é responsabilidade do dev garantir que o tipo declarado bate com as colunas retornadas. Para dados críticos, valide com Zod.

```typescript
import { z } from 'zod'

const UserRow = z.object({ id: z.number(), name: z.string() })
const rawResult = await prisma.$queryRaw<unknown[]>(
  Prisma.sql`SELECT id, name FROM "User" LIMIT 10`
)
const users = z.array(UserRow).parse(rawResult)
```

---

### Prisma Accelerate (v6)

O Prisma Accelerate é um serviço gerenciado da Prisma Data Platform (opt-in, pago além do free tier) que resolve dois problemas centrais de arquiteturas serverless e edge.

**Connection pooling global:**

Bancos de dados relacionais têm um limite de conexões simultâneas. Em ambientes serverless (Lambda, Vercel Functions, Cloudflare Workers), cada invocação pode abrir uma nova conexão — com tráfego médio, é fácil exaurir o pool do banco. O Prisma Accelerate atua como proxy inteligente, mantendo um pool estável de conexões entre o Accelerate e o banco, e recebendo conexões HTTP dos clientes edge.

**Cache de queries em CDN:**

`cacheStrategy` requer o pacote `@prisma/extension-accelerate` instalado como dependência. O cliente padrão (`PrismaClient`) não expõe essa opção.

```typescript
import { withAccelerate } from '@prisma/extension-accelerate'

// Cliente deve ser extendido com Accelerate para cacheStrategy funcionar
const prisma = new PrismaClient().$extends(withAccelerate())

// Ativar cache por query com TTL e stale-while-revalidate
const users = await prisma.user.findMany({
  cacheStrategy: {
    ttl: 60,         // dados frescos por 60 segundos
    swr: 300,        // serve stale por até 300s enquanto revalida em background
  },
})
```

A URL de conexão para Accelerate é fornecida pelo dashboard da Prisma Data Platform e substitui a `DATABASE_URL` normal. O cliente é gerado com o mesmo `prisma generate` — a API de queries não muda.

**Quando faz sentido usar Accelerate:**

- Deploy em edge (Cloudflare Workers, Vercel Edge, Deno Deploy) onde o banco está geograficamente distante
- Arquitetura serverless com muitas funções abrindo conexões concorrentes
- Queries read-heavy com dados que toleram eventual consistency (listas de produtos, dados de dashboard, etc.)

**Quando NÃO usar:**

- Aplicações com servidor persistente (Node.js tradicional com pool próprio via `PrismaClient`)
- Dados que exigem consistência estrita e não toleram cache
- Orçamento limitado sem justificativa de escala

---

## Quando usar

O Prisma é a escolha mais defensável para projetos que:

- **Iniciam do zero com TypeScript** — o schema-first com client gerado elimina a necessidade de manter tipos manualmente sincronizados com o banco.
- **Precisam de migrations confiáveis** — o histórico de migrations versionadas no repositório facilita code review, rollback e auditoria de mudanças de schema.
- **Vão rodar em edge ou serverless** — o WASM engine do v6 funciona nativamente sem configuração extra, e o Prisma Accelerate resolve o problema de connection pooling.
- **Têm equipe com perfil TypeScript forte** — a curva de aprendizado é mais suave do que TypeORM (sem decorators) e mais completa em type safety do que Sequelize v7.

**Comparação com TypeORM:** TypeORM usa decorators em classes (`@Entity`, `@Column`, `@ManyToOne`) e é o favorito de projetos NestJS enterprise, especialmente para equipes vindas de Java/Spring. A integração com NestJS é mais nativa. O Prisma oferece melhor type safety automático, migrations mais confiáveis e DX superior — mas TypeORM é melhor para projetos onde o modelo de domínio em classes é central.

**Comparação com Drizzle:** Drizzle é o queridinho de 2024–2025 — SQL-first, zero runtime overhead, type-safe e excelente para edge. Para equipes com domínio sólido de SQL que querem controle total das queries, Drizzle é competitivo. O Prisma vence em DX para operações comuns (CRUD, relações aninhadas) e no Prisma Studio. Drizzle vence em performance raw e transparência de SQL gerado.

---

## Armadilhas comuns

### 1. `findMany` sem paginação em tabelas grandes

**Problema:** buscar todos os registros de uma tabela grande sem limitar retorna todos os dados para memória da aplicação — OOM em produção com tabelas de milhões de registros.

```typescript
// PROBLEMA — sem limite, retorna TODOS os usuários
const allUsers = await prisma.user.findMany()
// Em produção com 5 milhões de usuários: OOM ou timeout
```

```typescript
// FIX — sempre paginar findMany em contextos de listagem
const users = await prisma.user.findMany({
  take: 50,
  skip: page * 50,
  orderBy: { createdAt: 'desc' },
})

// Ou cursor pagination para grandes volumes:
const users = await prisma.user.findMany({
  take: 50,
  cursor: lastCursor ? { id: lastCursor } : undefined,
  skip: lastCursor ? 1 : 0,
  orderBy: { id: 'asc' },
})
```

### 2. N+1 queries — chamar Prisma dentro de um loop

**Problema:** o N+1 clássico em Prisma com PostgreSQL não vem do `include` (que usa JOINs ou no máximo 2 queries com `relation.mode='join'`, o padrão para PostgreSQL). O N+1 real acontece quando relações são buscadas individualmente dentro de um loop — 1 query para a lista pai + N queries para cada item filho.

```typescript
// PROBLEMA: N+1 — 1 query para posts + N queries para o author de cada post
const posts = await prisma.post.findMany()
const result = await Promise.all(
  posts.map(post => prisma.user.findUnique({ where: { id: post.authorId } }))
)
```

```typescript
// FIX — include carrega tudo em 2 queries (posts + JOIN com users)
const posts = await prisma.post.findMany({
  include: { author: true }
})
```

Ativar `log: ['query']` no `PrismaClient` durante desenvolvimento para inspecionar o SQL gerado e identificar N+1 real.

### 3. `$queryRaw` com interpolação de string — SQL injection

**Problema:** usar template literal comum (sem `Prisma.sql`) ou concatenação de string diretamente no `$queryRaw` expõe a aplicação a SQL injection.

```typescript
// PROBLEMA — interpolação de string direta é SQL injection
const search = req.query.search as string // pode ser "'; DROP TABLE User; --"
const results = await prisma.$queryRaw(
  `SELECT * FROM "User" WHERE name LIKE '%${search}%'` // VULNERÁVEL
)
```

```typescript
// FIX — sempre usar Prisma.sql como tagged template literal
import { Prisma } from '@prisma/client'

const search = req.query.search as string
const results = await prisma.$queryRaw<{ id: number; name: string }[]>(
  Prisma.sql`SELECT id, name FROM "User" WHERE name ILIKE ${'%' + search + '%'}`
  // O valor é parametrizado automaticamente — nunca interpolado no SQL
)
```

`Prisma.sql` converte cada expressão interpolada em um parâmetro (`$1`, `$2`, etc.) que é enviado separadamente ao banco — o valor nunca compõe a string SQL.

### 4. `prisma migrate deploy` sem testar em ambiente de staging

**Problema:** aplicar migrations diretamente em produção sem testar em um ambiente com dados reais pode resultar em breaking changes silenciosas — especialmente operações como renomear coluna (que geram DROP + ADD Column, não RENAME), adicionar constraint NOT NULL em coluna com dados nulos existentes, ou operações de reescrita de tabela que bloqueiam por minutos.

```bash
# PROBLEMA — pipeline que vai direto para produção sem staging
# CI/CD script errado:
npx prisma migrate deploy  # diretamente em prod sem validação
```

```bash
# FIX — pipeline correto com staging intermediário
# 1. Em staging (dados próximos de produção):
DATABASE_URL=$STAGING_DATABASE_URL npx prisma migrate deploy

# 2. Validar comportamento e rollback plan
# 3. Só então aplicar em produção:
DATABASE_URL=$PROD_DATABASE_URL npx prisma migrate deploy

# Para migrations de alto risco (renomear coluna, adicionar NOT NULL),
# dividir em 3 migrations separadas:
# M1: adicionar nova coluna (nullable)
# M2: backfill de dados (script separado)
# M3: tornar NOT NULL e remover coluna antiga
```

---

## Em entrevista

When asked about Prisma in a technical interview, the key differentiator to communicate is the schema-first approach: instead of writing type definitions separately from your database schema, Prisma generates a fully-typed TypeScript client directly from `schema.prisma`, so the types are always in sync with what's actually in the database — you can't have a TypeScript model that references a column that doesn't exist. This is fundamentally different from TypeORM, where you write the entity class with decorators and the schema is derived from it, or Sequelize, where you define the model programmatically and types require extra effort to stay accurate.

A strong point to make is the distinction between Prisma v5 and v6: the v6 query engine runs as WebAssembly in-process rather than as a separate binary sidecar spawned by the Node process. This architectural change is what makes Prisma v6 natively compatible with edge runtimes like Cloudflare Workers and Vercel Edge Functions — the previous binary engine couldn't run in those environments because they don't support spawning child processes. Being able to explain this shows you understand not just the API surface but the runtime constraints of modern deployment targets.

When comparing Prisma to Drizzle in an interview context, frame it as a trade-off between developer experience and control: Prisma optimizes for productivity and type safety with less SQL knowledge required, while Drizzle is SQL-first and gives you full visibility into every query generated, with near-zero runtime overhead. Neither is objectively better; the right choice depends on team SQL proficiency, performance requirements, and whether you're targeting edge runtimes where Drizzle's smaller bundle size can matter. For teams that need to move fast with a TypeScript-first stack, Prisma's `findMany` with nested `select` and automatic pagination types is hard to beat; for teams that want to reason about SQL directly, Drizzle's schema definition as TypeScript objects and query builder are more transparent.

On the migrations side, the critical point for interviews is the dev vs prod workflow separation: `prisma migrate dev` is for local development and generates migration files, `prisma db push` is for rapid prototyping without migration history, and `prisma migrate deploy` is the only safe command for production pipelines — it reads existing migration files and applies only pending ones without generating new ones, making it safe and idempotent in CI/CD.

---

## Vocabulário PT→EN

| PT | EN |
|----|----|
| esquema declarativo | declarative schema |
| cliente gerado | generated client |
| type safety gerada | auto-generated type safety |
| migração versionada | versioned migration |
| banco de dados de borda | edge database |
| carregamento antecipado | eager loading |
| projeção (de campos) | projection / field selection |
| pooling de conexões | connection pooling |
| motor de consulta | query engine |
| relação aninhada | nested relation |
| paginação por cursor | cursor-based pagination |
| parâmetro de consulta | query parameter |

---

## Veja também

- [[Node.js]]
- [[03-Dominios/Node/ORMs e banco de dados/index]]
- [[01 - Panorama de ORMs]]
- [[06 - N+1 queries - detecção e DataLoader]]
- [[07 - Migrations e versionamento de schema]]

---

## Fontes

- [Prisma Documentation — Getting Started](https://www.prisma.io/docs/getting-started)
- [Prisma v6 Migration Guide](https://www.prisma.io/docs/orm/more/upgrade-guides/upgrading-versions/upgrading-to-prisma-6)
- [Prisma Schema Reference](https://www.prisma.io/docs/orm/reference/prisma-schema-reference)
- [Prisma Client API Reference](https://www.prisma.io/docs/orm/reference/prisma-client-reference)
- [Prisma Accelerate Documentation](https://www.prisma.io/docs/accelerate)
- [Prisma Migrate — Conceptual Overview](https://www.prisma.io/docs/orm/prisma-migrate/understanding-prisma-migrate/overview)
