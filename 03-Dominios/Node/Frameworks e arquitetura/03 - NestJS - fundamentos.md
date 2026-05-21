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

# NestJS: fundamentos

> [!abstract] TL;DR
> NestJS é um framework TypeScript opinativo, decorator-based e com DI built-in. A unidade organizacional é o módulo: ele declara controllers, providers, imports e exports. O container resolve dependências por constructor injection. É forte para apps enterprise; é overhead em apps pequenos.

## O que é

NestJS é um framework para aplicações server-side Node que organiza código em módulos, controllers e providers. Por padrão usa Express por baixo, mas pode usar Fastify como adapter. A filosofia lembra Spring Boot/Angular: metadata via decorators, DI container e arquitetura explícita.

## Por que importa

Em apps grandes, wiring manual, lifecycle e padrões transversais viram custo. NestJS compra estrutura: módulos por feature, providers testáveis, guards/pipes/interceptors/filters e DI consistente. Em apps pequenos, a mesma estrutura pode ser mais cerimônia que benefício.

## Como funciona

```typescript
import { Module } from "@nestjs/common";
import { UsersController } from "./users.controller";
import { UsersService } from "./users.service";

@Module({
  controllers: [UsersController],
  providers: [UsersService],
  exports: [UsersService],
})
export class UsersModule {}
```

```typescript
import { Injectable } from "@nestjs/common";

@Injectable()
export class UsersService {
  constructor(private readonly db: DatabaseClient) {}

  async findById(id: string) {
    return this.db.users.findById(id);
  }
}
```

```typescript
import { Controller, Get, Param } from "@nestjs/common";

@Controller("users")
export class UsersController {
  constructor(private readonly users: UsersService) {}

  @Get(":id")
  async getUser(@Param("id") id: string) {
    return this.users.findById(id);
  }
}
```

```typescript
import { Injectable, Scope } from "@nestjs/common";

@Injectable({ scope: Scope.REQUEST })
export class RequestContextService {}

@Injectable({ scope: Scope.TRANSIENT })
export class NewPerInjectionService {}

// Default: singleton no módulo/app.
```

```typescript
@Module({
  imports: [DatabaseModule, UsersModule],
  controllers: [OrdersController],
  providers: [OrdersService],
  exports: [OrdersService],
})
export class OrdersModule {}
```

## Na prática

Padrão observado no ecossistema: um módulo por feature (`UsersModule`, `OrdersModule`), shared modules para concerns transversais (`DatabaseModule`, `LoggerModule`), singleton como default, request scope apenas quando precisa de contexto da request. `exports` é o contrato entre módulos.

### O módulo como boundary de feature

Um módulo NestJS saudável não é só uma pasta. Ele declara o que a feature possui e o que exporta para outras features.

```typescript
@Module({
  imports: [DatabaseModule],
  controllers: [UsersController],
  providers: [
    UsersService,
    CreateUserUseCase,
    { provide: USER_REPOSITORY, useClass: PostgresUserRepository },
  ],
  exports: [UsersService],
})
export class UsersModule {}
```

Se outro módulo precisa criar usuário, ele importa `UsersModule` e injeta o contrato exportado. Ele não deve importar arquivos internos da pasta `users` por caminho relativo atravessando boundary.

### Tokens e interfaces

Interfaces TypeScript somem em runtime. Para injetar uma abstração, use token explícito.

```typescript
export const USER_REPOSITORY = Symbol("USER_REPOSITORY");

export interface UserRepository {
  findById(id: string): Promise<User | null>;
  save(user: User): Promise<void>;
}

@Injectable()
export class CreateUserUseCase {
  constructor(
    @Inject(USER_REPOSITORY)
    private readonly repo: UserRepository,
  ) {}
}
```

Esse detalhe é comum em entrevista porque mostra que o candidato entende TypeScript runtime, não só syntax de NestJS.

### Provider scope sem surpresa

Singleton é o default e geralmente é certo. Request scope deve ser exceção. Ele cria uma instância por request e pode propagar o custo para dependências que pareciam singleton.

```typescript
@Injectable()
export class PriceCalculator {
  // Stateless: singleton ideal.
}

@Injectable({ scope: Scope.REQUEST })
export class RequestContext {
  constructor(@Inject(REQUEST) private readonly req: Request) {}
}
```

Se o objetivo é só carregar `userId` ou `correlationId`, muitas vezes um interceptor/guard que popula contexto explícito resolve melhor do que transformar vários providers em request-scoped.

### Dynamic modules

Dynamic modules aparecem quando um módulo precisa de configuração.

```typescript
@Module({})
export class DatabaseModule {
  static forRoot(options: DatabaseOptions): DynamicModule {
    return {
      module: DatabaseModule,
      providers: [
        { provide: DATABASE_OPTIONS, useValue: options },
        DatabaseClient,
      ],
      exports: [DatabaseClient],
    };
  }
}
```

Use quando há variação real de configuração. Não crie dynamic module para esconder wiring simples.

### Testabilidade

NestJS facilita substituir providers em teste.

```typescript
const moduleRef = await Test.createTestingModule({
  providers: [CreateUserUseCase, UsersService],
})
  .overrideProvider(USER_REPOSITORY)
  .useValue(fakeUserRepository)
  .compile();

const useCase = moduleRef.get(CreateUserUseCase);
```

Esse é um benefício concreto do container: trocar adapter sem mexer no código de aplicação.

## Checklist de code review

- Módulos exportam só o necessário?
- Há imports cruzados entre features por caminho interno?
- Providers stateless ficaram singleton?
- Request scope tem justificativa explícita?
- Tokens são usados quando a dependência é interface/abstração?
- Circular dependency foi resolvida com design ou só mascarada com `forwardRef()`?
- Controller chama use case/service, não repository direto?
- DTOs e validation estão na camada HTTP, não no domínio?

## Exercício de maturidade

Um controller NestJS imaturo costuma acumular tudo:

```typescript
@Post()
async create(@Body() body: any) {
  if (!body.email) throw new BadRequestException();
  const existing = await this.prisma.user.findUnique({ where: { email: body.email } });
  if (existing) throw new ConflictException();
  return this.prisma.user.create({ data: body });
}
```

Uma versão mais madura separa boundary, use case e adapter:

```typescript
@Post()
async create(@Body() dto: CreateUserDto) {
  const user = await this.createUser.execute(dto);
  return UserPresenter.toHttp(user);
}
```

```typescript
@Injectable()
export class CreateUserUseCase {
  constructor(
    @Inject(USER_REPOSITORY) private readonly users: UserRepository,
  ) {}
}
```

O NestJS continua sendo o framework, mas a regra de negócio não fica presa ao controller nem ao Prisma.

### Sinal de arquitetura saudável

Você consegue testar `CreateUserUseCase` sem `TestingModule`, sem HTTP e sem banco real. Use `TestingModule` para integração NestJS; use teste puro para regra de aplicação.

### Regra prática final

Use NestJS para padronizar a aplicação, não para esconder design. Se módulos, providers e decorators tornam boundaries mais claros, o framework está ajudando. Se todo problema vira decorator novo, módulo global ou `forwardRef()`, o framework virou maquiagem sobre acoplamento.

## Armadilhas

1. `Scope.REQUEST` usado sem necessidade: escopo request propaga para dependências e pode custar performance.
2. Circular imports entre módulos: `forwardRef()` existe, mas frequentemente sinaliza design ruim.
3. Esquecer `exports`: outro módulo importa mas não consegue injetar o provider.
4. Colocar lógica pesada no constructor: prefira lifecycle hooks como `OnModuleInit`.
5. Injetar interface sem token: TypeScript não existe em runtime.
6. Transformar `SharedModule` em gaveta global: tudo depende de tudo.
7. Controller importando adapter de infraestrutura diretamente.
8. Usar decorators de ORM na entity de domínio e achar que isso ainda é Clean Architecture.

## Perguntas de entrevista

**Qual é a unidade fundamental de organização em NestJS?**
O módulo. Ele agrupa controllers, providers, imports e exports. É boundary de composição.

**Por que interfaces precisam de tokens?**
Porque interfaces TypeScript são apagadas em runtime. O container precisa de um token concreto: string, symbol ou classe.

**Quando usar request scope?**
Quando a instância realmente precisa ser diferente por request, como contexto específico da request. Não use para resolver conveniência de passar `userId`.

**Como NestJS se relaciona com Clean Architecture?**
Ele ajuda com módulos e DI, mas não garante arquitetura limpa. A dependency rule ainda precisa ser respeitada.

## Em entrevista

"NestJS is opinionated and decorator-based, with a built-in dependency injection container. Its fundamental unit is the module: a module declares controllers, providers, imports, and exports. Providers default to singleton scope; request and transient scopes exist but should be used deliberately. It is a good fit for enterprise apps with complex domains and teams that benefit from structure."

Vocabulário-chave:

- dependency injection -> injeção de dependência
- provider -> componente injetável
- module -> módulo
- controller -> controlador HTTP
- scope -> escopo

## Fontes

- [NestJS docs](https://docs.nestjs.com/)

## Veja também

- [[01 - Os 4 frameworks - Express, NestJS, Fastify, Hono]]
- [[04 - NestJS - guards, interceptors, pipes, filters]]
- [[09 - Validation com schema]]
- [[11 - DI - manual vs container]]
- [[Node.js]]
