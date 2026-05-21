---
title: "Clean Architecture em Node"
created: 2026-05-08
updated: 2026-05-08
type: concept
status: seedling
publish: true
tags:
  - node
  - frameworks
  - clean-architecture
  - hexagonal
  - architecture
aliases:
  - Clean Architecture
  - Hexagonal
  - Ports and adapters
---

# Clean Architecture em Node

> [!abstract] TL;DR
> Clean Architecture organiza código em camadas: entities, use cases, interface adapters e frameworks/drivers. A dependency rule diz que dependências apontam para dentro. Em Node, isso aparece como domínio sem Express/ORM, use cases dependentes de ports e adapters externos. Use quando domínio justifica.

## O que é

Clean Architecture, popularizada por Robert C. Martin, separa políticas de negócio de mecanismos externos. Hexagonal/Ports and Adapters é uma formulação próxima: domínio e aplicação definem portas; infraestrutura implementa adapters.

## Por que importa

Se use case importa `Request` do Express ou entity importa decorator do ORM, framework virou parte do núcleo. Isso dificulta teste, troca de adapter e manutenção. Em domínio rico, separar camadas reduz acoplamento. Em CRUD simples, pode ser over-engineering.

## Como funciona

```text
Entities
└── Use Cases
    └── Interface Adapters
        └── Frameworks and Drivers
```

```text
src/
├── domain/
│   └── User.ts
├── application/
│   ├── CreateUserUseCase.ts
│   └── UserRepository.ts
├── infrastructure/
│   ├── db/UserRepositoryPg.ts
│   └── http/UserController.ts
└── presentation/
    └── server.ts
```

```typescript
export class User {
  constructor(
    public readonly id: string,
    public name: string,
    public readonly email: string,
  ) {}

  changeName(name: string) {
    if (name.length < 1) throw new Error("Name required");
    this.name = name;
  }
}
```

```typescript
export interface UserRepository {
  save(user: User): Promise<void>;
  findById(id: string): Promise<User | null>;
}

export class CreateUserUseCase {
  constructor(private readonly repo: UserRepository) {}

  async execute(input: { name: string; email: string }) {
    const user = new User(crypto.randomUUID(), input.name, input.email);
    await this.repo.save(user);
    return user;
  }
}
```

```typescript
export class UserRepositoryPg implements UserRepository {
  constructor(private readonly db: PgPool) {}

  async save(user: User): Promise<void> {
    await this.db.query("insert into users(id, name, email) values($1, $2, $3)", [
      user.id,
      user.name,
      user.email,
    ]);
  }

  async findById(id: string): Promise<User | null> {
    const result = await this.db.query("select * from users where id = $1", [id]);
    return result.rowCount ? new User(result.rows[0].id, result.rows[0].name, result.rows[0].email) : null;
  }
}
```

```typescript
const repo = new UserRepositoryPg(pgPool);
const useCase = new CreateUserUseCase(repo);
const controller = new UserController(useCase);

app.post("/users", (req, res) => controller.create(req, res));
```

## Na prática

Use Clean quando há regra de negócio rica, múltiplos adapters, testes de use case valiosos e vida longa do produto. Em Express/Fastify, composition root manual faz o wiring. Em NestJS, módulos e providers ajudam, mas não garantem Clean: ainda é possível violar camadas.

### Regra de dependência em imports

A forma mais simples de auditar Clean em Node é olhar imports.

```typescript
// Bom: aplicação depende de domínio.
import { User } from "../domain/User";
import type { UserRepository } from "./UserRepository";
```

```typescript
// Ruim: domínio depende de framework/infra.
import { Entity, Column } from "typeorm";
import type { Request } from "express";
```

Se `domain/` importa ORM, HTTP, logger externo ou framework, a camada interna conhece detalhe externo.

### Controller como adapter

Controller adapta HTTP para use case. Ele não deve conter regra de negócio rica.

```typescript
export class UserController {
  constructor(private readonly createUser: CreateUserUseCase) {}

  async create(req: Request, res: Response) {
    const input = CreateUserSchema.parse(req.body);
    const user = await this.createUser.execute(input);
    res.status(201).json(UserPresenter.toHttp(user));
  }
}
```

Validation e presenter pertencem à borda. Use case não sabe que existe Express.

### Use case como política de aplicação

Use case orquestra regra. Ele conhece ports, não adapters.

```typescript
export class CreateInvoiceUseCase {
  constructor(
    private readonly invoices: InvoiceRepository,
    private readonly payments: PaymentGateway,
    private readonly clock: Clock,
  ) {}

  async execute(input: CreateInvoiceInput) {
    const invoice = Invoice.create(input, this.clock.now());
    await this.payments.authorize(invoice.total);
    await this.invoices.save(invoice);
    return invoice;
  }
}
```

`PaymentGateway` é uma porta. Stripe, Pagar.me ou mock são adapters.

### NestJS com Clean

NestJS pode ser usado como composition layer, mas cuidado para decorators não contaminarem domínio.

```typescript
@Module({
  providers: [
    CreateInvoiceUseCase,
    { provide: INVOICE_REPOSITORY, useClass: PrismaInvoiceRepository },
    { provide: PAYMENT_GATEWAY, useClass: StripePaymentGateway },
  ],
  controllers: [InvoicesController],
})
export class InvoicesModule {}
```

O módulo monta dependências. O use case continua sendo TypeScript puro.

### Quando não aplicar

Clean não é ritual. Para CRUD administrativo simples, uma separação leve pode ser melhor:

```text
users/
├── users.router.ts
├── users.service.ts
├── users.repository.ts
└── users.schema.ts
```

Se não há regra de domínio, criar `entities/`, `use-cases/`, `ports/`, `adapters/` pode só espalhar código.

## Checklist de code review

- `domain/` importa apenas linguagem e tipos internos?
- Use cases dependem de interfaces/ports?
- Controllers são adapters finos?
- Repositories implementam ports, não vazam ORM para use case?
- Mappers/presenters isolam formato HTTP/DB?
- Composition root está claro?
- Testes de use case rodam sem framework HTTP?
- A complexidade do domínio justifica as camadas?

## Exercício de maturidade

Violação comum:

```typescript
export class CreateUserUseCase {
  constructor(private readonly prisma: PrismaClient) {}

  async execute(input: Input) {
    return this.prisma.user.create({ data: input });
  }
}
```

O use case conhece Prisma. Trocar ORM, banco ou teste fake fica mais caro.

Versão com port:

```typescript
export class CreateUserUseCase {
  constructor(private readonly users: UserRepository) {}

  async execute(input: Input) {
    const user = User.create(input);
    await this.users.save(user);
    return user;
  }
}
```

```typescript
export class PrismaUserRepository implements UserRepository {
  constructor(private readonly prisma: PrismaClient) {}
}
```

Agora Prisma fica no adapter. O use case fala a linguagem da aplicação.

### Teste como prova arquitetural

Se o teste de use case precisa subir NestJS, Express ou Postgres, a camada talvez esteja acoplada demais.

```typescript
test("creates user", async () => {
  const repo = new InMemoryUserRepository();
  const useCase = new CreateUserUseCase(repo);
  const user = await useCase.execute({ name: "Ada", email: "ada@example.com" });
  expect(await repo.findById(user.id)).toEqual(user);
});
```

Teste simples é sinal de boundary saudável.

## Armadilhas

1. Entity importando ORM/decorator: framework entrou no domínio.
2. Use case recebendo `Request`/`Response`: framework entrou na aplicação.
3. Aplicar Clean em CRUD trivial: complexidade sem retorno.
4. Adapter virando god class: separar por bounded context/feature.
5. Sem composition root claro: dependências ficam espalhadas.
6. Chamar qualquer pasta de `domain` sem regra de negócio real.
7. Colocar validação HTTP dentro da entity.
8. Testar use case subindo Nest/Express inteiro.
9. Mapper ausente: formato de banco vira formato de API por acidente.

## Perguntas de entrevista

**Qual é a dependency rule?**
Dependências de código apontam para dentro. Camadas internas não conhecem frameworks, banco ou UI.

**Como Clean aparece em Node?**
Domínio puro, use cases dependentes de ports, adapters para HTTP/DB e composition root no startup/framework.

**Quando Clean é exagero?**
Quando o app é CRUD simples, sem regra de domínio rica e sem múltiplos adapters relevantes.

**NestJS garante Clean Architecture?**
Não. Ele ajuda com DI e módulos, mas você ainda pode acoplar use case a framework ou ORM.

## Em entrevista

"Clean Architecture separates business policies from external mechanisms. The dependency rule is the key: source dependencies point inward, so the domain does not know about Express, databases, or framework details. In Node, that means use cases depend on ports, and infrastructure implements adapters. It is valuable for complex domains, but over-engineering for simple CRUD."

Vocabulário-chave:

- layer -> camada
- dependency rule -> regra de dependência
- port -> porta
- adapter -> adaptador
- dependency inversion -> inversão de dependência

## Fontes

- [The Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)

## Veja também

- [[03 - NestJS - fundamentos]]
- [[08 - Error handling estruturado]]
- [[09 - Validation com schema]]
- [[11 - DI - manual vs container]]
- [[Node.js]]
- [[Arquitetura de Software]]
