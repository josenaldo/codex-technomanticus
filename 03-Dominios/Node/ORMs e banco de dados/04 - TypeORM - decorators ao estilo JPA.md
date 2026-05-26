---
title: "TypeORM - decorators ao estilo JPA"
created: 2026-05-10
updated: 2026-05-10
type: concept
status: seedling
progresso: andamento
aliases:
  - TypeORM Node
  - TypeORM decorators
publish: false
tags:
  - node
  - orm
  - typeorm
  - nestjs
  - banco-de-dados
---

# TypeORM - decorators ao estilo JPA

> [!abstract] TL;DR
> O TypeORM em 2026 é o ORM clássico do ecossistema [[Node.js]] — usa decorators TypeScript (`@Entity`, `@Column`, `@OneToMany`) em estilo deliberadamente similar ao JPA/Hibernate do Java, tornando a transição natural para devs que vêm de Java ou C#.
> A integração com [[03-Dominios/Node/Frameworks e arquitetura/index|NestJS]] é nativa via `@nestjs/typeorm`: o módulo `TypeOrmModule` conecta ao banco, registra entidades por feature e fornece injeção de `Repository<Entity>` nos serviços com `@InjectRepository`.
> O Repository pattern é built-in — cada entidade tem um `Repository<T>` tipado que encapsula as operações de banco, e custom repositories em v0.3 são criados com o método `.extend()` ao invés do decorator `@EntityRepository` que foi depreciado.
> Em 2026, TypeORM v0.3 é uma escolha válida para projetos NestJS enterprise, especialmente em times que vêm de Java/C# — mas o Prisma v6 compete no mesmo espaço com melhor DX e type safety mais rigoroso; a escolha entre eles depende principalmente do contexto do time e das necessidades do projeto.

## O que é

O TypeORM foi criado em 2016 com uma proposta clara: trazer os padrões enterprise do Java para o ecossistema Node.js. O projeto se inspira diretamente no JPA (Java Persistence API) e no Hibernate — tanto na terminologia (entidades, repositórios, eager/lazy loading) quanto na mecânica de decorators que mapeiam classes TypeScript para tabelas de banco de dados.

A motivação era legítima: os ORMs disponíveis em Node.js à época (principalmente Sequelize) usavam um estilo funcional/encadeado que não se traduzia bem para TypeScript e não oferecia a riqueza semântica dos padrões Java. O TypeORM trouxe o modelo de objetos de domínio (classes com decorators descritivos) que desenvolvedores empresariais já conheciam.

Em 2026, o TypeORM está na versão estável v0.3.x. A versão 0.3 introduziu uma mudança arquitetural importante: a `DataSource` substituiu a função global `createConnection()` como ponto central de configuração e acesso ao banco. Isso tornou o ciclo de vida mais explícito e previsível — você instancia uma `DataSource`, chama `initialize()`, e a partir daí obtém repositories e executa queries por meio dessa instância.

O ecossistema NestJS abraçou o TypeORM como ORM padrão desde cedo, e o pacote `@nestjs/typeorm` faz a ponte entre o sistema de módulos e injeção de dependência do NestJS e o ciclo de vida da `DataSource`. Essa integração consolidou o TypeORM como a escolha de referência em projetos NestJS enterprise, posição que mantém em 2026 ainda que o Prisma v6 venha conquistando espaço com uma proposta de melhor DX.

## Como funciona

### Entities e decorators

Uma entidade TypeORM é uma classe TypeScript decorada com `@Entity()`. Cada propriedade da classe mapeia para uma coluna do banco via decorators específicos. O TypeORM lê esses metadados em tempo de execução para construir o schema e gerar SQL.

```typescript
import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  Index,
  Unique,
  CreateDateColumn,
  UpdateDateColumn,
} from 'typeorm';

@Entity('users')
@Unique(['email'])
export class User {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Index()
  @Column({ type: 'varchar', length: 255, nullable: false })
  email: string;

  @Column({ type: 'varchar', length: 100, nullable: false })
  name: string;

  @Column({ type: 'boolean', default: true })
  active: boolean;

  @Column({ type: 'jsonb', nullable: true })
  metadata: Record<string, unknown> | null;

  @CreateDateColumn({ type: 'timestamp with time zone' })
  createdAt: Date;

  @UpdateDateColumn({ type: 'timestamp with time zone' })
  updatedAt: Date;
}
```

Os tipos de coluna disponíveis variam por banco de dados. Para PostgreSQL, os mais comuns são: `'varchar'` para strings com tamanho máximo, `'text'` para strings sem limite, `'int'` e `'bigint'` para inteiros, `'boolean'`, `'jsonb'` para JSON indexável, `'timestamp'` e `'timestamp with time zone'` para datas, e `'numeric'`/`'decimal'` para valores monetários.

`@PrimaryGeneratedColumn()` sem argumento gera um inteiro autoincrement. `@PrimaryGeneratedColumn('uuid')` gera UUIDs automáticos via `gen_random_uuid()` no PostgreSQL. `@CreateDateColumn` e `@UpdateDateColumn` são gerenciados pelo TypeORM automaticamente — você nunca precisa preencher esses campos manualmente.

`@Index()` cria um índice simples na coluna. `@Unique(['campo'])` na entidade (não na propriedade) cria uma constraint de unicidade, que também cria um índice único implícito.

### Relacionamentos

O TypeORM suporta os quatro tipos de relacionamento relacionais com decorators dedicados:

```typescript
import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  OneToMany,
  ManyToOne,
  ManyToMany,
  OneToOne,
  JoinColumn,
  JoinTable,
  CreateDateColumn,
} from 'typeorm';
import { User } from './user.entity';
import { Tag } from './tag.entity';

@Entity('posts')
export class Post {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column({ type: 'varchar', length: 255 })
  title: string;

  // ManyToOne: Post tem uma FK para User (owning side)
  @ManyToOne(() => User, (user) => user.posts, { nullable: false })
  @JoinColumn({ name: 'author_id' })
  author: User;

  // ManyToMany: a tabela de junção fica no owning side (quem tem @JoinTable)
  @ManyToMany(() => Tag, (tag) => tag.posts)
  @JoinTable({
    name: 'post_tags',
    joinColumn: { name: 'post_id' },
    inverseJoinColumn: { name: 'tag_id' },
  })
  tags: Tag[];

  @CreateDateColumn()
  createdAt: Date;
}
```

```typescript
// user.entity.ts — inverse side do relacionamento
@Entity('users')
export class User {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column({ type: 'varchar', length: 255 })
  email: string;

  // OneToMany: User não tem FK — Post tem a FK
  @OneToMany(() => Post, (post) => post.author)
  posts: Post[];
}
```

O conceito de **owning side** é central: é o lado que contém a foreign key no banco. Em `ManyToOne`/`OneToOne`, o owning side é o que tem `@JoinColumn`. Em `ManyToMany`, é o que tem `@JoinTable`. O inverse side apenas declara a relação para navegação mas não influencia o schema.

Eager loading: o TypeORM oferece duas formas. A primeira é `{ eager: true }` no decorator — mas isso é global e vai carregar a relação em **toda** query que use aquela entidade, causando over-fetching. A forma recomendada é usar a opção `relations` explicitamente no `find()`, carregando apenas quando necessário.

### Repository pattern

No TypeORM v0.3, o acesso às operações de banco passa pela `DataSource`. O `Repository<Entity>` é o objeto central que encapsula os métodos de query:

```typescript
import { DataSource, Repository } from 'typeorm';
import { User } from './user.entity';

// Obtendo o repository a partir da DataSource (padrão v0.3)
const userRepository: Repository<User> = dataSource.getRepository(User);

// find com FindOptions
const users = await userRepository.find({
  where: { active: true },
  order: { createdAt: 'DESC' },
  take: 20,        // LIMIT
  skip: 40,        // OFFSET
  relations: { posts: true },   // JOINs explícitos
  select: { id: true, email: true, name: true },  // SELECT parcial
});

// findOne — retorna null se não encontrar
const user = await userRepository.findOne({
  where: { id: userId },
  relations: { posts: true },
});

// findOneBy — atalho para where simples
const userByEmail = await userRepository.findOneBy({ email });

// findAndCount — útil para paginação
const [items, total] = await userRepository.findAndCount({
  where: { active: true },
  take: 10,
  skip: 0,
});

// save — INSERT se não tem id, UPDATE se tem
const savedUser = await userRepository.save(newUser);

// delete — por condição, não carrega a entidade
await userRepository.delete({ id: userId });

// remove — recebe entidade carregada, dispara hooks
await userRepository.remove(user);

// update — UPDATE parcial por condição
await userRepository.update({ id: userId }, { name: 'Novo Nome' });
```

Custom repositories em v0.3 usam o método `.extend()` — o decorator `@EntityRepository` foi depreciado e removido:

```typescript
// custom-user.repository.ts
import { DataSource } from 'typeorm';
import { User } from './user.entity';

export const createUserRepository = (dataSource: DataSource) =>
  dataSource.getRepository(User).extend({
    async findActiveWithPosts(): Promise<User[]> {
      return this.find({
        where: { active: true },
        relations: { posts: true },
        order: { createdAt: 'DESC' },
      });
    },

    async countByEmail(email: string): Promise<number> {
      return this.countBy({ email });
    },
  });

export type UserRepository = ReturnType<typeof createUserRepository>;
```

No NestJS, a injeção do custom repository pode ser feita via factory provider ou simplesmente adicionando os métodos extras em um service que já recebe o `Repository<User>` via `@InjectRepository`.

### QueryBuilder

O `QueryBuilder` é a camada de escape para quando os métodos `find` não são suficientes — JOINs complexos, subqueries, `GROUP BY`, window functions, `HAVING`, ou quando você precisa de controle fino sobre o SQL gerado:

```typescript
import { DataSource } from 'typeorm';
import { Post } from './post.entity';

// Buscar posts com contagem de comentários usando QueryBuilder
const posts = await dataSource
  .createQueryBuilder(Post, 'post')
  .leftJoinAndSelect('post.author', 'author')
  .leftJoin('post.comments', 'comment') // leftJoin sem Select — não queremos dados de comment
  .addSelect('COUNT(comment.id)', 'commentCount')
  .where('post.createdAt > :since', { since: new Date('2026-01-01') })
  .andWhere('author.active = :active', { active: true })
  .groupBy('post.id')
  .addGroupBy('author.id')
  .orderBy('commentCount', 'DESC')
  .take(10)
  .getMany();
// ATENÇÃO: não combine leftJoinAndSelect em ManyToMany com GROUP BY.
// leftJoinAndSelect injeta colunas de tag no SELECT; o PostgreSQL exige que apareçam no
// GROUP BY ou em um agregador. Ao adicionar tag.id ao GROUP BY, o agrupamento vira
// (post, tag) em vez de post — COUNT e SUM passam a calcular por par, não por post.
// Use leftJoin (sem Select) para relações ManyToMany em queries com GROUP BY.

// getCount() — COUNT sem carregar entidades
const total = await dataSource
  .createQueryBuilder(Post, 'post')
  .where('post.authorId = :authorId', { authorId })
  .getCount();
```

A regra sobre parâmetros é absoluta: **nunca interpolar strings diretamente no QueryBuilder**. Use sempre a sintaxe `:paramName` com o objeto de parâmetros como segundo argumento. Interpolar diretamente abre brecha para SQL injection.

```typescript
// ERRADO — SQL injection
.where(`post.title LIKE '%${searchTerm}%'`)

// CORRETO — parameterizado
.where('post.title ILIKE :search', { search: `%${searchTerm}%` })
```

### Integração com NestJS

A integração TypeORM + NestJS é feita pelo pacote `@nestjs/typeorm`. A configuração acontece em dois níveis: o módulo raiz configura a `DataSource`, e cada feature module registra suas entidades:

```typescript
// app.module.ts
import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { User } from './users/user.entity';
import { Post } from './posts/post.entity';

@Module({
  imports: [
    TypeOrmModule.forRoot({
      type: 'postgres',
      host: process.env.DB_HOST,
      port: parseInt(process.env.DB_PORT ?? '5432'),
      username: process.env.DB_USER,
      password: process.env.DB_PASS,
      database: process.env.DB_NAME,
      entities: [User, Post],
      synchronize: false,   // NUNCA true em produção
      migrations: ['dist/migrations/*.js'],
      migrationsRun: true,  // roda migrations no boot
    }),
  ],
})
export class AppModule {}
```

```typescript
// users.module.ts
import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { User } from './user.entity';
import { UsersService } from './users.service';
import { UsersController } from './users.controller';

@Module({
  imports: [TypeOrmModule.forFeature([User])],
  providers: [UsersService],
  controllers: [UsersController],
  exports: [TypeOrmModule],
})
export class UsersModule {}
```

```typescript
// users.service.ts
import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { DataSource, Repository } from 'typeorm';
import { User } from './user.entity';

@Injectable()
export class UsersService {
  constructor(
    @InjectRepository(User)
    private readonly usersRepository: Repository<User>,
    // DataSource injetável diretamente para queries raw ou transações
    private readonly dataSource: DataSource,
  ) {}

  async findAll(): Promise<User[]> {
    return this.usersRepository.find({ where: { active: true } });
  }

  async findWithPosts(userId: string): Promise<User | null> {
    return this.usersRepository.findOne({
      where: { id: userId },
      relations: { posts: true },
    });
  }

  async createWithTransaction(userData: Partial<User>): Promise<User> {
    return this.dataSource.transaction(async (manager) => {
      const user = manager.create(User, userData);
      return manager.save(user);
    });
  }
}
```

### Migrations com TypeORM

O TypeORM CLI gera migrations por diff de schema — compara as entidades registradas com o estado atual do banco e gera o SQL de diferença:

```bash
# Gerar migration com nome descritivo
npx typeorm migration:generate src/migrations/AddUserActiveColumn -d src/data-source.ts

# Aplicar migrations pendentes
npx typeorm migration:run -d src/data-source.ts

# Reverter a última migration aplicada
npx typeorm migration:revert -d src/data-source.ts

# Listar migrations com status (aplicada / pendente)
npx typeorm migration:show -d src/data-source.ts
```

O arquivo `data-source.ts` exporta uma instância de `DataSource` que o CLI usa:

```typescript
// src/data-source.ts
import { DataSource } from 'typeorm';

export const AppDataSource = new DataSource({
  type: 'postgres',
  host: process.env.DB_HOST ?? 'localhost',
  port: parseInt(process.env.DB_PORT ?? '5432'),
  username: process.env.DB_USER ?? 'postgres',
  password: process.env.DB_PASS ?? 'postgres',
  database: process.env.DB_NAME ?? 'app_dev',
  entities: ['src/**/*.entity.ts'],
  migrations: ['src/migrations/*.ts'],
  synchronize: false,
});
```

`synchronize: true` sincroniza automaticamente o schema das entidades com o banco no boot — útil em desenvolvimento local para não ter que rodar migrations a cada mudança de entidade. Em produção, **nunca use `synchronize: true`**: o TypeORM pode dropar colunas e dados silenciosamente para alinhar o banco com as entidades atuais.

## Quando usar

TypeORM é a escolha natural nos seguintes cenários:

**Time vindo de Java ou C#**: devs familiarizados com JPA, Hibernate ou Entity Framework encontram no TypeORM os mesmos padrões — entidades como classes decoradas, repositories tipados, lifecycle hooks (`@BeforeInsert`, `@AfterLoad`), e um modelo mental de "objeto de domínio com persistência". A curva de aprendizado é muito menor do que aprender o modelo schema-first do Prisma.

**Projeto NestJS enterprise com histórico TypeORM**: se o projeto já usa TypeORM e há um volume razoável de código (migrations, repositories, entidades), a migração para Prisma tem custo alto sem benefício imediato. TypeORM v0.3 é maduro e estável; manter e evoluir faz mais sentido.

**Necessidade de Repository pattern explícito**: equipes que preferem abstrair o acesso ao banco em classes de repositório com métodos de domínio (ao invés de usar o Prisma Client diretamente nos serviços) se beneficiam da estrutura nativa que o TypeORM oferece.

**QueryBuilder para queries complexas**: projetos com muitas queries analíticas (JOINs com múltiplas tabelas, subqueries correlacionadas, window functions) aproveitam bem o QueryBuilder, que oferece mais controle granular do que o Prisma para esses casos.

Para novos projetos sem restrições de time ou legado, o Prisma v6 em 2026 oferece melhor DX, type safety mais rigoroso e suporte nativo a edge runtimes. A decisão entre TypeORM e Prisma é principalmente sobre contexto — não existe uma resposta universal.

## Armadilhas comuns

### `synchronize: true` em produção

O `synchronize: true` instrui o TypeORM a ajustar automaticamente o schema do banco para corresponder às entidades no boot. Em desenvolvimento, isso economiza tempo. Em produção, é um vetor de destruição: se você renomear uma entidade ou remover um campo, o TypeORM pode dropar a coluna (e os dados) silenciosamente, sem aviso e sem possibilidade de rollback.

```typescript
// PROBLEMA — synchronize: true em produção remove colunas e dados sem aviso
TypeOrmModule.forRoot({
  type: 'postgres',
  synchronize: true, // NUNCA em produção
  entities: [User],
})
```

```typescript
// CORRETO — migrations explícitas em produção
TypeOrmModule.forRoot({
  type: 'postgres',
  synchronize: false,
  migrations: ['dist/migrations/*.js'],
  migrationsRun: true,  // roda migrations pendentes no boot
  entities: [User],
})
```

### N+1 silencioso com lazy loading

O TypeORM suporta lazy loading quando as relações são tipadas como `Promise<T>` — o tipo `Promise` é suficiente para ativar o comportamento lazy, sem necessidade de `lazy: true` no decorator. O problema: cada acesso a uma relação lazy dispara uma query separada. Se você busca 50 posts e acessa `post.author` em cada iteração, dispara 51 queries (1 para posts + 50 para autores).

```typescript
// Entidade com lazy loading — Promise<User> no tipo é o que ativa o comportamento
@Entity('posts')
export class PostLazy {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  // Promise<User> como tipo ativa o lazy loading — não é necessário lazy: true no decorator
  @ManyToOne(() => User, (user) => user.posts)
  author: Promise<User>;
}
```

```typescript
// PROBLEMA — lazy loading dispara queries N+1
const posts = await postRepository.find(); // 1 query
for (const post of posts) {
  const author = await post.author; // N queries — uma para cada post
  console.log(author.name);
}
```

```typescript
// CORRETO — carregue relations explicitamente com uma única query com JOIN
const posts = await postRepository.find({
  relations: { author: true }, // LEFT JOIN na mesma query
});
for (const post of posts) {
  console.log(post.author.name); // sem queries adicionais
}
```

### `save()` em bulk operations faz SELECT antes de INSERT

O método `save()` do TypeORM é inteligente: verifica se a entidade já existe (via `id`) para decidir entre INSERT e UPDATE. Essa checagem envolve um SELECT adicional por entidade. Para bulk inserts de centenas ou milhares de registros, isso se torna uma enxurrada de SELECTs desnecessários antes dos INSERTs.

```typescript
// PROBLEMA — save() em loop faz SELECT + INSERT por entidade
const users = generateUsers(500);
for (const user of users) {
  await userRepository.save(user); // 1 SELECT + 1 INSERT por iteração = 1000 queries
}
```

```typescript
// CORRETO — insert() faz INSERT direto sem SELECT prévio
const users = generateUsers(500);
await userRepository.insert(users); // 1 query de INSERT em batch

// Ou com QueryBuilder para controle total
await dataSource
  .createQueryBuilder()
  .insert()
  .into(User)
  .values(users)
  .execute();
```

### `{ eager: true }` global causa over-fetching

O decorator `{ eager: true }` em uma relação faz o TypeORM carregar aquela relação em **todas** as queries que envolvam aquela entidade — não importa se você precisa ou não da relação naquele contexto. Em entidades com múltiplas relações eager, uma simples listagem de IDs pode resultar em dezenas de JOINs desnecessários.

```typescript
// PROBLEMA — eager global carrega a relação em TODA query
@Entity()
export class Post {
  @ManyToOne(() => User, { eager: true })  // sempre carregado, sem exceção
  author: User;

  @ManyToMany(() => Tag, { eager: true })  // idem
  @JoinTable()
  tags: Tag[];
}

// Esta query simples vai fazer JOINs para author e tags mesmo sem precisar
const posts = await postRepository.findBy({ active: true });
```

```typescript
// CORRETO — sem eager: true no decorator, use relations explícito quando necessário
@Entity()
export class Post {
  @ManyToOne(() => User)  // sem eager
  author: User;

  @ManyToMany(() => Tag)
  @JoinTable()
  tags: Tag[];
}

// Carregue somente o que a operação atual realmente precisa
const posts = await postRepository.find({
  where: { active: true },
  relations: { author: true }, // explícito e controlado
});

// Quando não precisa de relações, a query é limpa
const postIds = await postRepository.findBy({ active: true }); // sem JOINs
```

## Em entrevista

TypeORM and JPA/Hibernate share the same conceptual model — entities as annotated classes, a repository abstraction for data access operations, and explicit relationship mapping with owning side semantics. The key difference is that JPA is a specification with multiple implementations (Hibernate being the dominant one), while TypeORM is both the specification and the implementation. In JPA, lazy loading is the default and triggers a `LazyInitializationException` if accessed outside a session; TypeORM's lazy loading requires explicit configuration and returns `Promise<T>`, which is more predictable but still creates N+1 risks if not handled carefully.

When choosing TypeORM over Prisma in 2026, the strongest arguments are team familiarity and existing codebase. If your team comes from a Java or C# background and already knows the Repository and Entity patterns, TypeORM reduces cognitive overhead. If you have a significant existing TypeORM codebase with custom repositories and migrations, the cost of migrating to Prisma rarely justifies the DX improvement. For genuinely new projects without these constraints, Prisma v6's schema-first approach, stricter type safety, and native edge runtime support make it the more compelling choice.

The Repository pattern in NestJS with TypeORM follows the module boundary principle. Each feature module calls `TypeOrmModule.forFeature([Entity])`, which makes the `Repository<Entity>` available for injection within that module's providers. Services receive the repository via `@InjectRepository(Entity)` in the constructor, which means the repository is scoped to the module and the dependency graph is explicit. For cross-module data access, you export `TypeOrmModule` from the feature module and import the feature module — not the repository directly.

For transactions in NestJS + TypeORM, the recommended approach is injecting the `DataSource` directly into the service and using `dataSource.transaction(async (manager) => { ... })`. The transaction manager receives an `EntityManager` that scopes all operations to the same transaction. Avoid the `@Transaction()` decorator (deprecated in v0.3) and the pattern of passing managers between methods, which makes the code harder to test and reason about.

## Vocabulário PT→EN

| PT | EN |
|---|---|
| entidade | entity |
| decorador | decorator |
| repositório | repository |
| carregamento antecipado | eager loading |
| carregamento preguiçoso | lazy loading |
| lado possuidor | owning side |
| migração | migration |
| construtor de queries | query builder |
| chave estrangeira | foreign key |
| tabela de junção | join table |
| sincronização de schema | schema synchronization |
| gestor de entidades | entity manager |

## Veja também

- [[Node.js]]
- [[03-Dominios/Node/ORMs e banco de dados/index]]
- [[01 - Panorama de ORMs]]
- [[03-Dominios/Node/Frameworks e arquitetura/index]]

## Fontes

- [TypeORM v0.3 — Documentação oficial](https://typeorm.io)
- [NestJS — TypeORM integration guide](https://docs.nestjs.com/techniques/database)
- [TypeORM — Relations documentation](https://typeorm.io/relations)
- [TypeORM — Migrations](https://typeorm.io/migrations)
