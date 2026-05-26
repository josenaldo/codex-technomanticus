---
title: "Panorama de ORMs"
created: 2026-05-10
updated: 2026-05-11
type: concept
status: seedling
progresso: andamento
aliases:
  - Panorama ORMs Node
  - ORMs Node comparativo
publish: false
tags:
  - node
  - orm
  - sequelize
  - prisma
  - typeorm
  - drizzle
---

# Panorama de ORMs

> [!abstract] TL;DR
> Em 2026, o ecossistema Node.js tem 4 ORMs com posicionamentos bem distintos: **Sequelize** é battle-tested, surgiu na era callback e ainda domina em projetos legacy com v7 trazendo melhor suporte TypeScript; **Prisma v6** é schema-first com DX excepcional, type safety gerado automaticamente e suporte a edge runtimes com Prisma Accelerate GA; **TypeORM** usa decorators estilo JPA/Hibernate e é o favorito de devs vindos do Java/C#, com integração nativa ao NestJS; **Drizzle** é o queridinho de 2024–2025 — SQL-first, zero runtime overhead, type-safe e excelente para edge runtimes (Cloudflare Workers, Vercel Edge).
> A escolha não é sobre "melhor ORM", é sobre fit: Prisma para DX e projetos novos, Drizzle para edge ou equipes com domínio de SQL, TypeORM para NestJS enterprise, Sequelize para manutenção de código legado.
> O risco maior é escolher por popularidade e não por requisito: cada ORM tem trade-offs reais de performance, transparência de queries e compatibilidade com runtime.
> Armadilha clássica de entrevista: `synchronize: true` no TypeORM em produção pode dropar colunas com dados; raw queries no Prisma não têm type safety automático — sempre valide o retorno.

## O que é

### ORM — Object-Relational Mapper

Um **ORM** (Object-Relational Mapper) é uma camada de abstração que mapeia tabelas de banco de dados relacional para objetos/classes na linguagem de programação. Em vez de escrever SQL puro, o desenvolvedor manipula objetos que representam registros, e o ORM traduz essas operações para queries SQL adequadas ao banco alvo.

O propósito central de um ORM em [[Node.js]] é eliminar o boilerplate repetitivo de construção manual de queries, reduzir erros de concatenação de strings SQL e fornecer um modelo mental orientado a objetos para interagir com o banco. Em um projeto de médio porte sem ORM, é comum ter centenas de queries SQL repetidas com pequenas variações — um ORM consolida essas variações em chamadas de método tipadas.

**O que um ORM oferece na prática:**
- Mapeamento de tabelas para classes/interfaces TypeScript
- Construção programática de queries (filtros, joins, ordenação)
- Migrations automáticas ou semi-automáticas do schema
- Pool de conexões gerenciado
- Type safety nas queries (em graus variados por ORM)
- Suporte a relacionamentos (has many, belongs to, many-to-many)
- Tratamento de transações

### ORM vs Query Builder vs SQL Puro

Entender essa gradação é fundamental para defender escolhas técnicas:

| Camada | Abstração | Controle | Tipo safety | Exemplo |
|--------|-----------|----------|-------------|---------|
| SQL Puro | Mínima | Total | Manual | `pg`, `mysql2` |
| Query Builder | Média | Alto | Parcial | `knex`, `kysely` |
| ORM leve (SQL-first) | Média-alta | Bom | Excelente | Drizzle |
| ORM completo | Alta | Limitado | Variável | Prisma, TypeORM, Sequelize |

**SQL Puro** (com drivers como `pg` ou `mysql2`) dá controle absoluto mas exige escrever e manter todo SQL manualmente. Ideal para queries extremamente otimizadas ou features que nenhum ORM suporta bem (window functions complexas, CTEs recursivos).

**Query Builders** como `knex` ou `kysely` constroem SQL programaticamente sem mapear entidades. São ótimos para projetos que precisam de flexibilidade máxima sem o overhead de um ORM completo. O `kysely` em particular é o favorito para type safety em 2026 quando você não quer um ORM, mas quer TypeScript rigoroso.

**ORMs leves (SQL-first)** como Drizzle ficam no meio-termo: você define schema em TypeScript, as queries parecem SQL mas são type-safe, e não há mágica de runtime transformando objetos.

**ORMs completos** como Prisma, TypeORM e Sequelize abstraem mais: você trabalha com entidades, repositórios, relacionamentos declarativos — o ORM cuida de gerar o SQL correto. A desvantagem é menor controle sobre a query gerada e possível overhead de performance.

### Por que escolher um ORM em Node.js

O argumento principal não é performance — SQL puro sempre ganha. O argumento é **produtividade, segurança e manutenibilidade**:

- **Menos bugs de SQL injection**: ORMs parametrizam queries por padrão.
- **Migrations rastreáveis**: alterações de schema ficam em arquivos versionados no git.
- **Type safety nas queries**: com Prisma ou Drizzle, o TypeScript pega erros de coluna inexistente em tempo de compilação.
- **Onboarding mais rápido**: um dev novo no projeto entende o schema via código, não precisando mapear SQL solto por todo o codebase.
- **Portabilidade de banco**: trocar de PostgreSQL para MySQL é mais simples (com caveats).

A contrapartida é real: ORMs adicionam uma camada de indireção que pode gerar queries sub-ótimas, especialmente com relacionamentos complexos. Saber ler o SQL gerado e identificar N+1 queries é parte do arsenal de qualquer dev sênior usando ORM — veja [[06 - N+1 queries - detecção e DataLoader]].

---

## Como funciona

### Eixos de comparação

A tabela abaixo compara os 4 principais ORMs do ecossistema Node.js em 2026 nos eixos mais relevantes para tomada de decisão:

| Eixo | Sequelize v7 | Prisma v6 | TypeORM v0.3 | Drizzle v0.30+ |
|------|-------------|-----------|--------------|----------------|
| **Paradigma** | Code-first | Schema-first | Code-first (decorators) | SQL-first |
| **Type safety** | Manual/parcial | Gerada automaticamente | Manual via decorators | Nativa (inferida) |
| **Migration strategy** | Sequelize CLI / manual | `prisma migrate` (automático) | `typeorm migration:generate` | `drizzle-kit generate` + `migrate` (`push` = dev-only) |
| **Performance overhead** | Médio | Médio-alto (query engine) | Médio | Mínimo (zero proxies) |
| **Edge runtime** | Não | Sim (v6+, Prisma Accelerate) | Não | Sim (nativo) |
| **Maturidade** | Alta (2011+) | Alta (2019+, v6 2025) | Alta (2016+) | Crescente (2022+) |
| **Popularidade 2026** | Estável (legacy) | Muito alta (novos projetos) | Alta (NestJS) | Em ascensão |
| **Ideal para** | Manutenção legacy | Projetos novos, DX | NestJS enterprise | Edge, SQL-focused, performance |
| **Stars GitHub (aprox.)** | ~29k | ~38k | ~34k | ~25k |
| **Suporte a PostgreSQL** | Sim | Sim | Sim | Sim |
| **Suporte a SQLite** | Sim | Sim | Sim | Sim |
| **Suporte a MySQL** | Sim | Sim | Sim | Sim |

> [!note] Prisma v6 e serverless
> O Prisma v6 usa um query engine baseado em WASM que roda in-process
> (sem sidecar binário separado). Em ambientes serverless, o gargalo é a
> inicialização do WASM + setup do connection pool a cada cold start.
> O Prisma Accelerate mitiga isso com connection pooling externo e cache
> de queries, mas é um serviço pago.

---

### Sequelize

Sequelize é o ORM mais antigo do ecossistema Node.js, lançado em 2011 quando callbacks eram o padrão. Passou pela transição para Promises e depois para async/await, acumulando API legada ao longo do caminho. Em 2025, o Sequelize v7 chegou com melhor suporte a TypeScript nativo, remoção de métodos deprecated e alinhamento com padrões modernos — mas o peso histórico da API ainda é visível.

**Características principais:**
- API baseada em modelos estendidos de `Model` (class-based)
- Tipo safety manual: você declara atributos no modelo e o TypeScript acredita em você
- Dialetos para PostgreSQL, MySQL, MariaDB, SQLite, MSSQL
- Associações declarativas (`hasMany`, `belongsTo`, `belongsToMany`)
- Hooks (lifecycle callbacks: beforeCreate, afterUpdate, etc.)
- Scopes para reutilizar condições de query

**Quando ainda faz sentido usar Sequelize:**
- Projeto legado já usando Sequelize v6 — migração para outro ORM tem custo alto sem benefício claro
- Equipe familiar com a API e sem tempo para onboarding em novo ORM
- Requisito de suporte a MSSQL (Drizzle e Prisma têm suporte mais limitado)

**v7 — principais mudanças (2025):**
- TypeScript nativo sem dependência de `@types/sequelize`
- `DataTypes` com melhor inferência
- Remoção de `sequelize.sync()` em produção por padrão
- Suporte a ES modules nativo

```typescript
// Sequelize v7 — Model definition com TypeScript
import { DataTypes, Model, InferAttributes, InferCreationAttributes, CreationOptional } from 'sequelize';
import { sequelize } from './database';

class User extends Model<InferAttributes<User>, InferCreationAttributes<User>> {
  declare id: CreationOptional<number>;
  declare name: string;
  declare email: string;
  declare createdAt: CreationOptional<Date>;
}

User.init(
  {
    id: {
      type: DataTypes.INTEGER.UNSIGNED,
      autoIncrement: true,
      primaryKey: true,
    },
    name: {
      type: DataTypes.STRING(128),
      allowNull: false,
    },
    email: {
      type: DataTypes.STRING(256),
      allowNull: false,
      unique: true,
    },
    createdAt: DataTypes.DATE,
  },
  {
    tableName: 'users',
    sequelize,
  }
);

// Query com include (eager loading de associação)
const usersWithPosts = await User.findAll({
  where: { name: { [Op.like]: '%João%' } },
  include: [{ model: Post, as: 'posts', required: false }],
  limit: 10,
  order: [['createdAt', 'DESC']],
});
```

---

### Prisma

Prisma é o ORM mais adotado em novos projetos Node.js/TypeScript em 2026. Seu diferencial central é o **schema-first declarativo**: você define o schema em `schema.prisma`, executa a geração, e o Prisma Client tipado é gerado automaticamente — sem decorators, sem configuração manual de tipos, sem discrepância entre schema e código.

**O ecossistema Prisma tem 3 componentes principais:**
- **Prisma Client**: cliente de query gerado, 100% tipado com base no schema
- **Prisma Migrate**: sistema de migrations declarativas com histórico em arquivos SQL
- **Prisma Studio**: UI visual para explorar e editar dados (similar ao TablePlus, mas integrado)

**Prisma v6 — destaques (2025):**
- **Edge runtime support**: o Prisma Client agora roda em Cloudflare Workers, Vercel Edge e Deno nativo
- **Prisma Accelerate GA**: proxy de connection pooling + cache de query, resolve o problema de cold start serverless
- **Prisma Pulse**: CDC (Change Data Capture) em tempo real com subscriptions TypeScript
- **Melhorias de performance**: query engine refatorado com menor overhead em queries simples
- **TypedSQL**: queries SQL raw com type safety completa via `$queryRaw` tipado

**O ponto de atenção:** `$queryRaw` e `$executeRaw` para queries customizadas **não são type-safe por padrão**. O TypedSQL (feature de v6) mitiga isso, mas exige anotações extras. Assumir que "tudo no Prisma é type-safe" é uma armadilha real.

```prisma
// schema.prisma — definição declarativa
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id        Int      @id @default(autoincrement())
  name      String
  email     String   @unique
  posts     Post[]
  profile   Profile?
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}

model Post {
  id        Int      @id @default(autoincrement())
  title     String
  content   String?
  published Boolean  @default(false)
  author    User     @relation(fields: [authorId], references: [id])
  authorId  Int
  createdAt DateTime @default(now())
}
```

```typescript
// Prisma Client v6 — queries tipadas
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

// findMany com filtro e include
const publishedPosts = await prisma.post.findMany({
  where: { published: true },
  include: {
    author: {
      select: { name: true, email: true },
    },
  },
  orderBy: { createdAt: 'desc' },
  take: 20,
});

// Transação com $transaction
const [user, post] = await prisma.$transaction([
  prisma.user.create({
    data: { name: 'Alice', email: 'alice@example.com' },
  }),
  prisma.post.create({
    data: { title: 'Hello World', authorId: 1 },
  }),
]);

// Upsert (create or update)
const upsertedUser = await prisma.user.upsert({
  where: { email: 'bob@example.com' },
  update: { name: 'Bob Updated' },
  create: { name: 'Bob', email: 'bob@example.com' },
});
```

---

### TypeORM

TypeORM adota o padrão **Active Record / Data Mapper** com decorators TypeScript estilo JPA (Java Persistence API) / Hibernate. É a escolha natural para devs vindos de Java ou C# (Entity Framework) porque o modelo mental é praticamente idêntico — entidades são classes decoradas, repositórios são injetáveis, relacionamentos são declarados via decorators.

**Integração com NestJS** é o principal driver de adoção em 2026. O pacote `@nestjs/typeorm` integra o TypeORM ao container de DI do NestJS de forma transparente, tornando a combinação NestJS + TypeORM o stack mais popular para APIs enterprise no ecossistema Node.

**v0.3+ — evolução:**
- Melhorias significativas de type safety em queries
- Suporte a ESM
- `DataSource` substituindo `createConnection` (v0.3 quebrou APIs de v0.2)
- QueryBuilder mais robusto
- Melhor suporte a migrations com `typeorm migration:generate`

**Ponto crítico de produção:** `synchronize: true` sincroniza o schema automaticamente na inicialização da aplicação — conveniente em dev, **catastrófico em produção**. TypeORM pode dropar colunas sem aviso se achar que o schema mudou. Nunca use `synchronize: true` fora de desenvolvimento.

```typescript
// TypeORM v0.3 — Entity com decorators
import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  CreateDateColumn,
  UpdateDateColumn,
  OneToMany,
  ManyToOne,
  JoinColumn,
} from 'typeorm';

@Entity('users')
export class User {
  @PrimaryGeneratedColumn()
  id: number;

  @Column({ length: 128 })
  name: string;

  @Column({ unique: true, length: 256 })
  email: string;

  @OneToMany(() => Post, (post) => post.author)
  posts: Post[];

  @CreateDateColumn()
  createdAt: Date;

  @UpdateDateColumn()
  updatedAt: Date;
}

@Entity('posts')
export class Post {
  @PrimaryGeneratedColumn()
  id: number;

  @Column()
  title: string;

  @Column({ default: false })
  published: boolean;

  @ManyToOne(() => User, (user) => user.posts)
  @JoinColumn({ name: 'authorId' })
  author: User;

  @Column()
  authorId: number;
}
```

```typescript
// TypeORM v0.3 — Repository pattern com DataSource
import { DataSource } from 'typeorm';
import { User } from './entities/User';
import { Post } from './entities/Post';

const AppDataSource = new DataSource({
  type: 'postgres',
  host: process.env.DB_HOST,
  port: Number(process.env.DB_PORT),
  username: process.env.DB_USER,
  password: process.env.DB_PASS,
  database: process.env.DB_NAME,
  entities: [User, Post],
  migrations: ['src/migrations/*.ts'],
  synchronize: false, // NUNCA true em produção
});

await AppDataSource.initialize();

const userRepository = AppDataSource.getRepository(User);

// findOne com relação carregada
const user = await userRepository.findOne({
  where: { email: 'alice@example.com' },
  relations: { posts: true },
});

// QueryBuilder para queries complexas
const postsWithAuthors = await AppDataSource
  .getRepository(Post)
  .createQueryBuilder('post')
  .leftJoinAndSelect('post.author', 'author')
  .where('post.published = :published', { published: true })
  .orderBy('post.createdAt', 'DESC')
  .take(10)
  .getMany();
```

---

### Drizzle ORM

Drizzle é o ORM que ganhou mais adoção entre 2024 e 2026, particularmente em projetos que precisam de edge runtimes ou equipes que querem controle SQL sem abrir mão de type safety. O slogan não oficial é "SQL que você conhece, tipos que você merece" — as queries em Drizzle parecem SQL, mas são TypeScript com inferência total.

**Filosofia central — sem mágica de runtime:**
- Sem proxies JavaScript para interceptar acesso a propriedades
- Sem lazy loading implícito (você sempre sabe o que vai ao banco)
- Sem query engine externo (ao contrário do Prisma)
- O código Drizzle compila para SQL puro — o que você escreve é exatamente o que executa

**Drizzle Kit** é o CLI de tooling: `drizzle-kit generate` gera migrations SQL a partir de mudanças no schema, `drizzle-kit push` aplica schema diretamente (útil em dev), `drizzle-kit studio` abre uma UI visual similar ao Prisma Studio.

**Por que Drizzle é favorito para edge runtimes:**
- Não tem dependência de binário externo (ao contrário do Prisma pre-v6)
- Bundle size mínimo — fundamental para Cloudflare Workers com limite de 1MB
- Compatível nativamente com D1 (SQLite da Cloudflare), Neon, PlanetScale, Turso
- Funciona com HTTP-based database clients (sem TCP connections persistentes)

**v0.30+ — destaques:**
- Drizzle Studio estável
- Suporte a `$with` (CTEs) e window functions
- Relational queries API (`db.query.*`) com type safety para joins
- Melhor suporte a migrations incrementais

```typescript
// Drizzle v0.30+ — Schema definition
import { pgTable, serial, varchar, text, boolean, timestamp, integer } from 'drizzle-orm/pg-core';
import { relations } from 'drizzle-orm';

export const users = pgTable('users', {
  id: serial('id').primaryKey(),
  name: varchar('name', { length: 128 }).notNull(),
  email: varchar('email', { length: 256 }).notNull().unique(),
  createdAt: timestamp('created_at').defaultNow().notNull(),
});

export const posts = pgTable('posts', {
  id: serial('id').primaryKey(),
  title: varchar('title', { length: 256 }).notNull(),
  content: text('content'),
  published: boolean('published').default(false).notNull(),
  authorId: integer('author_id')
    .notNull()
    .references(() => users.id),
  createdAt: timestamp('created_at').defaultNow().notNull(),
});

// Declaração de relações (para relational queries API)
export const usersRelations = relations(users, ({ many }) => ({
  posts: many(posts),
}));

export const postsRelations = relations(posts, ({ one }) => ({
  author: one(users, { fields: [posts.authorId], references: [users.id] }),
}));
```

```typescript
// Drizzle v0.30+ — Queries com SQL-first syntax
import { drizzle } from 'drizzle-orm/node-postgres';
import { eq, desc, and, like } from 'drizzle-orm';
import { Pool } from 'pg';
import { users, posts } from './schema';

const pool = new Pool({ connectionString: process.env.DATABASE_URL });
const db = drizzle(pool, { schema: { users, posts } });

// Select com join explícito (SQL-first)
const publishedPostsWithAuthors = await db
  .select({
    postId: posts.id,
    title: posts.title,
    authorName: users.name,
  })
  .from(posts)
  .innerJoin(users, eq(posts.authorId, users.id))
  .where(eq(posts.published, true))
  .orderBy(desc(posts.createdAt))
  .limit(20);

// Relational query API (mais ergonômico para includes)
const usersWithPosts = await db.query.users.findMany({
  where: (user, { like }) => like(user.name, '%Alice%'),
  with: {
    posts: {
      where: (post, { eq }) => eq(post.published, true),
      orderBy: (post, { desc }) => desc(post.createdAt),
    },
  },
  limit: 10,
});

// Insert com returning
const [newUser] = await db
  .insert(users)
  .values({ name: 'Carol', email: 'carol@example.com' })
  .returning({ id: users.id, name: users.name });
```

---

## Quando usar

A decisão de ORM raramente é binária — é contextual. Use este decision tree como ponto de partida, não como dogma.

### Decision Tree

```
Você está em um projeto existente com Sequelize?
├── Sim → Upgrade para Sequelize v7. Migração para outro ORM tem custo
│          alto sem benefício técnico claro. Invista em testes e migrations.
└── Não → Continue abaixo.

Você vai rodar em edge runtime? (Cloudflare Workers, Vercel Edge, Deno Deploy)
├── Sim → Drizzle é a escolha natural.
│         Prisma v6 com Accelerate também funciona (mas com custo).
└── Não → Continue abaixo.

Você está em um projeto NestJS enterprise?
├── Sim → TypeORM (integração nativa @nestjs/typeorm) ou Prisma
│         (equipes que preferem DX sobre convenção NestJS).
└── Não → Continue abaixo.

Sua equipe tem domínio forte de SQL e prefere controle explícito?
├── Sim → Drizzle. Você vai se sentir em casa.
└── Não → Continue abaixo.

Você quer a melhor DX e type safety out-of-the-box?
├── Sim → Prisma v6. Schema-first, geração automática de tipos,
│         migrations declarativas, Studio incluído.
└── Não → Drizzle (se performance for prioritária) ou Prisma (se DX importar).
```

### Resumo por cenário

| Cenário | ORM recomendado | Motivo |
|---------|-----------------|--------|
| Novo projeto Node.js + PostgreSQL | **Prisma v6** | DX, type safety, migrations, Studio |
| Edge runtime (CF Workers, Vercel Edge) | **Drizzle** | Zero overhead, bundle mínimo, nativo |
| NestJS enterprise com DI | **TypeORM** | Integração @nestjs/typeorm, DI nativo |
| NestJS com foco em DX | **Prisma** | Schema-first, melhor type safety |
| Manutenção de projeto legado | **Sequelize v7** | Sem rewrite, upgrade incremental |
| Equipe com background Java/C# | **TypeORM** | Mental model familiar (JPA/EF) |
| Equipe forte em SQL | **Drizzle** | SQL-first sem surpresas |
| Serverless/Lambda em escala | **Drizzle** ou **Prisma Accelerate** | Cold start mínimo |
| Prototipagem rápida | **Prisma** | Schema → types → queries em minutos |

---

## Armadilhas comuns

### 1. Escolher ORM por popularidade, não por fit

O erro mais comum é olhar para o número de estrelas no GitHub ou o número de tutoriais e escolher o ORM "mais popular". Em 2026, Prisma lidera em novos projetos — mas Prisma é uma péssima escolha para um Cloudflare Worker que precisa ser serverless e ter bundle abaixo de 1MB. TypeORM com NestJS é uma combinação consolidada, mas adotar TypeORM em um projeto standalone sem NestJS é carregar overhead sem benefício.

**Como evitar:** mapeie os requisitos primeiro. Precisa de edge runtime? Serverless com cold start crítico? ORM existente no projeto? Equipe familiarizada com algum estilo (code-first, schema-first, SQL-first)? A tabela de eixos de comparação acima deve ser o guia.

### 2. Assumir que Prisma é sempre type-safe

Prisma gera tipos excepcionais para o Prisma Client gerado — mas há escape hatches que quebram essa garantia. Queries com `$queryRaw` retornam `unknown` por padrão, e `$executeRaw` não tem nenhuma validação de tipo no resultado. Devs que confiam cegamente nos tipos do Prisma e fazem uma query raw podem ter um bug de runtime que o TypeScript não pegou.

```typescript
// ⚠️ $queryRaw sem TypedSQL — resultado é 'unknown'
const result = await prisma.$queryRaw`
  SELECT id, name FROM users WHERE email = ${email}
`;
// result é 'unknown' — você precisa fazer cast manual ou usar TypedSQL

// ✅ Com TypedSQL (Prisma v6) — você define o tipo esperado
import { Prisma } from '@prisma/client';
const users = await prisma.$queryRaw<Array<{ id: number; name: string }>>`
  SELECT id, name FROM users WHERE email = ${email}
`;
```

**Como evitar:** prefira o Prisma Client gerado sempre que possível. Use `$queryRaw` apenas quando o Prisma Client não consegue expressar a query. Se usar raw, sempre defina o tipo retornado ou valide com Zod/Valibot.

### 3. TypeORM `synchronize: true` em produção

O TypeORM tem uma flag conveniente: `synchronize: true` na `DataSource` faz o ORM comparar as entidades com o schema do banco a cada inicialização e aplicar as diferenças automaticamente. Em desenvolvimento, é prático. Em produção, é uma bomba relógio.

O TypeORM pode interpretar que uma coluna renomeada é uma coluna dropada + coluna nova criada — e dropar a coluna com dados sem aviso. Não há rollback automático, não há histórico de migrations gerado, não há como auditoria depois.

```typescript
// ❌ NUNCA em produção
const AppDataSource = new DataSource({
  // ...
  synchronize: true, // PERIGO: pode dropar colunas com dados
});

// ✅ Correto em produção
const AppDataSource = new DataSource({
  // ...
  synchronize: false,
  migrations: ['dist/migrations/*.js'],
  migrationsRun: true, // roda migrations pendentes na inicialização
});
```

**Como evitar:** use `synchronize: false` sempre. Gere migrations com `typeorm migration:generate` para cada mudança de schema e revise o SQL gerado antes de aplicar. Ver [[07 - Migrations e versionamento de schema]] para o processo completo.

### 4. Ignorar o N+1 implícito de eager loading

Todos os ORMs desta lista podem gerar N+1 queries quando você carrega relacionamentos de forma ingênua. O Sequelize com `include` não otimizado, o TypeORM com relações carregadas por lazy loading implícito, e até o Prisma com `include` aninhado em listas podem disparar uma query por registro da lista.

```typescript
// ⚠️ Potencial N+1 — Sequelize sem eager loading correto
const users = await User.findAll(); // 1 query
for (const user of users) {
  const posts = await user.getPosts(); // N queries (1 por usuário)!
}

// ✅ Eager loading correto com include
const users = await User.findAll({
  include: [{ model: Post, as: 'posts' }], // 2 queries: users + posts
});
```

Veja [[06 - N+1 queries - detecção e DataLoader]] para diagnóstico e soluções detalhadas.

---

## Em entrevista

When choosing an ORM for a Node.js project, the decision should be driven by runtime constraints, team familiarity, and long-term maintainability — not by popularity or personal preference. In 2026, Prisma v6 is the go-to choice for most new projects because of its schema-first approach, automatically generated TypeScript types, and excellent developer experience with integrated migrations and Prisma Studio. However, if the project runs on edge runtimes like Cloudflare Workers or Vercel Edge, Drizzle becomes the clear winner due to its zero runtime overhead, minimal bundle size, and native compatibility with HTTP-based database clients that edge environments require. For enterprise NestJS applications, TypeORM integrates natively through the `@nestjs/typeorm` package and follows a decorator-based approach familiar to developers coming from Java or C# backgrounds, making onboarding faster in those contexts. When maintaining legacy codebases, upgrading Sequelize to v7 is usually preferable to a full ORM migration, as the risk-to-benefit ratio rarely justifies the rewrite cost. A senior engineer should be able to articulate these trade-offs clearly and defend a choice based on concrete requirements rather than defaulting to whichever ORM they used last.

### Vocabulário PT → EN

| Português | Inglês | Uso em contexto |
|-----------|--------|-----------------|
| Mapeamento objeto-relacional | Object-Relational Mapping (ORM) | "We use an ORM to map database tables to TypeScript classes" |
| Esquema / schema | Schema | "The schema is defined declaratively in `schema.prisma`" |
| Migração | Migration | "We run migrations before each deployment" |
| Carregamento antecipado | Eager loading | "Use eager loading to avoid N+1 queries" |
| Carregamento tardio | Lazy loading | "Lazy loading can hide N+1 issues in production" |
| Construtor de queries | Query builder | "Drizzle is closer to a query builder than a full ORM" |
| Segurança de tipos | Type safety | "Prisma's generated client gives you full type safety on queries" |
| Código primeiro | Code-first | "TypeORM uses a code-first approach with decorators" |
| Esquema primeiro | Schema-first | "Prisma is schema-first: you define the schema, it generates the client" |
| SQL primeiro | SQL-first | "Drizzle is SQL-first: the query API mirrors SQL syntax" |
| Entidade | Entity | "In TypeORM, each database table is represented by an Entity class" |
| Repositório | Repository | "The Repository pattern separates data access logic from business logic" |
| Pool de conexões | Connection pool | "Always configure a connection pool to limit database connections" |
| Transação | Transaction | "Wrap multi-step operations in a transaction to ensure atomicity" |
| Rollback | Rollback | "If any step fails, the transaction rollback reverts all changes" |

---

## Fontes

- [Sequelize v7 — Documentação oficial](https://sequelize.org/)
- [Sequelize — Getting Started com TypeScript](https://sequelize.org/docs/v7/other-topics/typescript/)
- [Prisma v6 — Documentação oficial](https://www.prisma.io/docs)
- [Prisma — What's new in Prisma 6](https://www.prisma.io/blog/prisma-6)
- [Prisma Accelerate](https://www.prisma.io/data-platform/accelerate)
- [TypeORM v0.3 — Documentação oficial](https://typeorm.io/)
- [TypeORM — Data Source options](https://typeorm.io/data-source-options)
- [NestJS — Database (TypeORM integration)](https://docs.nestjs.com/techniques/database)
- [Drizzle ORM — Documentação oficial](https://orm.drizzle.team/)
- [Drizzle — Getting Started com PostgreSQL](https://orm.drizzle.team/docs/get-started-postgresql)
- [Drizzle Kit — Migrations](https://orm.drizzle.team/kit-docs/overview)
- [Kysely — Type-safe SQL query builder (alternativa)](https://kysely.dev/)
- [State of JS 2024 — Databases & ORMs](https://stateofjs.com/)

---

## Veja também

- [[03-Dominios/Node/ORMs e banco de dados/index]] — MOC do galho 6
- [[Node.js]] — tronco da trilha Node Senior
- [[02 - Sequelize - queries e associações]] — deep dive Sequelize
- [[03 - Prisma - schema-first e type safety]] — deep dive Prisma
- [[04 - TypeORM - decorators ao estilo JPA]] — deep dive TypeORM
- [[05 - Drizzle - ORM lightweight e type-safe]] — deep dive Drizzle
- [[06 - N+1 queries - detecção e DataLoader]] — problema transversal crítico
- [[07 - Migrations e versionamento de schema]] — gerenciamento de schema
- [[10 - Cheatsheet e decision tree de ORMs]] — referência rápida e comparativo final
