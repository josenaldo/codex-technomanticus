---
title: "DI: manual vs container"
created: 2026-05-08
updated: 2026-05-08
type: concept
status: seedling
publish: true
tags:
  - node
  - frameworks
  - dependency-injection
  - di
  - architecture
aliases:
  - DI manual
  - DI container
  - tsyringe
  - awilix
---

# DI: manual vs container

> [!abstract] TL;DR
> DI manual é constructor injection + composition root. Containers (NestJS, awilix, tsyringe, InversifyJS) automatizam wiring e lifecycle scopes. Manual é simples e explícito em apps pequenos; container vale quando o grafo de dependências e escopos fica complexo.

## O que é

Dependency Injection é passar dependências de fora para dentro, em vez de instanciá-las dentro da classe/função. Container de DI é uma ferramenta que resolve esse grafo automaticamente.

## Por que importa

Sem DI, use cases criam DB clients, loggers e gateways diretamente. Isso acopla, dificulta teste e viola [[10 - Clean Architecture em Node]]. Com DI, dependências ficam explícitas. Com container, o wiring pode ser centralizado e escalável.

## Como funciona

```typescript
// composition-root.ts
const logger = new Logger();
const db = new PgPool(config.database);
const userRepo = new UserRepositoryPg(db);
const createUser = new CreateUserUseCase(userRepo, logger);
const userController = new UserController(createUser);

export { userController };
```

```typescript
export function makeUserController(deps: { db: PgPool; logger: Logger }) {
  const repo = new UserRepositoryPg(deps.db);
  const createUser = new CreateUserUseCase(repo, deps.logger);
  return new UserController(createUser);
}
```

```typescript
@Injectable()
export class CreateUserUseCase {
  constructor(
    private readonly repo: UserRepository,
    private readonly logger: Logger,
  ) {}
}
```

```typescript
import { asClass, asValue, createContainer, InjectionMode } from "awilix";

const container = createContainer({ injectionMode: InjectionMode.PROXY });
container.register({
  db: asValue(pgPool),
  logger: asClass(Logger).singleton(),
  userRepo: asClass(UserRepositoryPg).singleton(),
  createUser: asClass(CreateUserUseCase).singleton(),
});

const createUser = container.resolve<CreateUserUseCase>("createUser");
```

```typescript
import "reflect-metadata";
import { container, inject, injectable } from "tsyringe";

@injectable()
class CreateUserUseCase {
  constructor(
    @inject("UserRepository") private readonly repo: UserRepository,
    @inject("Logger") private readonly logger: Logger,
  ) {}
}

container.register("UserRepository", { useClass: UserRepositoryPg });
const useCase = container.resolve(CreateUserUseCase);
```

| Approach | Ramp-up | Scopes | Quando usar |
| --- | --- | --- | --- |
| Manual | Baixo | Manual | App pequeno, dependências rasas |
| NestJS DI | Médio | Singleton/request/transient | Apps NestJS |
| awilix | Médio | Singleton/scoped/transient | Express/Fastify com grafo médio |
| tsyringe | Médio | Decorator-based | Times confortáveis com decorators |
| InversifyJS | Alto | Completo | Apps grandes, legado com container |

## Na prática

Até cerca de poucas dezenas de services, composition root manual costuma ser suficiente. Quando há módulos, request-scoped providers, lazy loading ou muitos adapters, container paga o custo. O ponto não é "container moderno"; é custo de wiring versus clareza.

### Composition root explícito

Composition root é o lugar onde o grafo de objetos nasce. Em app pequeno, isso é legível e poderoso.

```typescript
export function buildApp(config: Config) {
  const logger = new Logger(config.log);
  const db = new PgPool(config.database);
  const users = new UserRepositoryPg(db);
  const createUser = new CreateUserUseCase(users, logger);
  const app = express();

  app.use("/users", makeUsersRouter({ createUser }));
  return { app, close: () => db.end() };
}
```

Teste pode montar outro grafo sem container.

```typescript
const createUser = new CreateUserUseCase(new InMemoryUserRepository(), fakeLogger);
```

### Factory por feature

Quando o app cresce, factories mantêm wiring local sem container global.

```typescript
export function makeUsersFeature(deps: { db: PgPool; logger: Logger }) {
  const repo = new UserRepositoryPg(deps.db);
  const createUser = new CreateUserUseCase(repo, deps.logger);
  const router = makeUsersRouter({ createUser });

  return { router };
}
```

Esse padrão funciona bem com Express/Fastify e continua claro para code review.

### Container com lifecycle

Container começa a valer quando lifecycle importa.

```typescript
container.register({
  requestContext: asClass(RequestContext).scoped(),
  auditLogger: asClass(AuditLogger).singleton(),
  createOrder: asClass(CreateOrderUseCase).scoped(),
});
```

`scoped()` pode criar uma instância por request, útil para correlation ID, tenant, auth context. Manualmente, isso exigiria passar contexto por várias camadas.

### Service locator: anti-pattern comum

DI injeta dependências no constructor. Service locator busca dependências de dentro da classe.

```typescript
// Ruim: classe esconde dependência global.
class CreateUserUseCase {
  async execute(input: Input) {
    const repo = container.resolve<UserRepository>("userRepo");
    return repo.save(input);
  }
}
```

```typescript
// Bom: dependência explícita.
class CreateUserUseCase {
  constructor(private readonly repo: UserRepository) {}
}
```

Service locator dificulta teste e torna dependências invisíveis.

### Tokens e runtime

Como em [[03 - NestJS - fundamentos]], interface TypeScript não existe em runtime. Containers precisam de tokens.

```typescript
const TOKENS = {
  userRepository: Symbol("userRepository"),
  logger: Symbol("logger"),
} as const;
```

Padronize tokens cedo se for usar container, senão o projeto vira mistura de strings mágicas.

## Checklist de code review

- Dependências aparecem no constructor/factory?
- Não há `container.resolve()` dentro de regra de negócio?
- Composition root é único ou claramente dividido por feature?
- Lifecycle scope foi escolhido por necessidade, não por conveniência?
- Tokens são constantes, não strings espalhadas?
- Testes conseguem substituir adapters sem framework inteiro?
- Manual DI ainda está legível ou virou wiring repetitivo demais?
- Container não foi introduzido antes de existir problema real?

## Exercício de maturidade

Dependência escondida:

```typescript
export class SendWelcomeEmail {
  async execute(user: User) {
    const mailer = globalContainer.resolve<Mailer>("mailer");
    await mailer.send(user.email, "welcome");
  }
}
```

Teste precisa configurar container global. A dependência não aparece na assinatura.

Dependência explícita:

```typescript
export class SendWelcomeEmail {
  constructor(private readonly mailer: Mailer) {}

  async execute(user: User) {
    await this.mailer.send(user.email, "welcome");
  }
}
```

Agora teste passa fake direto.

```typescript
const sent: string[] = [];
const useCase = new SendWelcomeEmail({ send: async (email) => sent.push(email) });
```

### Quando migrar de manual para container

Sinais razoáveis:

- factories começaram a repetir wiring complexo;
- há múltiplos scopes por request/tenant;
- módulos são carregados condicionalmente;
- features independentes precisam registrar providers;
- testes de integração precisam trocar adapters em massa.

Sem esses sinais, manual DI continua sendo escolha forte.

## Armadilhas

1. Container em app pequeno por antecipação: complexidade antes da necessidade.
2. Misturar DI manual e container sem fronteira: ninguém sabe quem instancia quem.
3. `tsyringe` sem `reflect-metadata`: falhas em runtime.
4. Request scope viral em NestJS: dependências podem virar request-scoped.
5. Composition root espalhado: wiring perde rastreabilidade.
6. Service locator escondendo dependências dentro de use case.
7. Token string duplicado com typo.
8. Container global em teste gerando estado compartilhado entre casos.
9. Escopo singleton para objeto que carrega dados de request.

## Perguntas de entrevista

**DI precisa de container?**
Não. DI é passar dependências explicitamente. Container é ferramenta para automatizar wiring.

**O que é composition root?**
O ponto de startup onde objetos concretos são instanciados e conectados.

**Por que service locator é problemático?**
Porque dependências ficam escondidas. A classe parece simples, mas busca coisas em estado global.

**Quando container vale a pena?**
Quando o grafo é grande, há lifecycle scopes, módulos independentes ou muita substituição de adapters.

## Em entrevista

"Dependency injection without a container is constructor injection plus a composition root. You instantiate dependencies explicitly at startup and pass them in. Containers like NestJS DI, awilix, and tsyringe automate wiring and lifecycle scopes. Manual DI is better for small apps; containers earn their complexity in large apps, complex domains, or request-scoped lifecycles."

Vocabulário-chave:

- composition root -> raiz de composição
- constructor injection -> injeção por construtor
- container -> contêiner de DI
- lifecycle scope -> escopo de ciclo de vida
- request-scoped -> escopado por request

## Fontes

- [awilix](https://github.com/jeffijoe/awilix)
- [tsyringe](https://github.com/microsoft/tsyringe)
- [NestJS docs](https://docs.nestjs.com/)

## Veja também

- [[03 - NestJS - fundamentos]]
- [[10 - Clean Architecture em Node]]
- [[12 - Decision tree + cheatsheet]]
- [[Node.js]]
