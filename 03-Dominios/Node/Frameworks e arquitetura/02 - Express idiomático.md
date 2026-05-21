---
title: "Express idiomático"
created: 2026-05-08
updated: 2026-05-08
type: concept
status: seedling
publish: true
tags:
  - node
  - frameworks
  - express
  - middleware
aliases:
  - Express
  - asyncHandler
  - error middleware
---

# Express idiomático

> [!abstract] TL;DR
> Express é middleware-based: uma pipeline ordenada de funções `(req, res, next)`. Express 5 encaminha rejeições de Promises para `next(err)` automaticamente; Express 4 ainda exige wrapper em muito código legacy. Error middleware tem quatro argumentos: `(err, req, res, next)`.

## O que é

Express é o framework HTTP minimalista mais conhecido do ecossistema Node. Ele oferece routing, middleware e integração direta com `http`, mas deixa validação, DI, OpenAPI, auth e organização arquitetural por conta da aplicação.

## Por que importa

Express continua aparecendo em entrevistas e projetos reais porque é simples, estável e bem conhecido. Código Express idiomático em 2026 é diferente de código Express 4 escrito sem TypeScript, sem schema e sem erro global consistente.

## Como funciona

```typescript
import express from "express";

const app = express();
app.use(express.json({ limit: "1mb" }));

app.get("/hello", (_req, res) => {
  res.json({ greeting: "hello" });
});

app.listen(3000);
```

```typescript
// Express 5: reject/throw em async handler chega ao error middleware.
app.get("/users/:id", async (req, res) => {
  const user = await db.users.findById(req.params.id);
  if (!user) throw new NotFoundError("User not found");
  res.json(user);
});
```

```typescript
// Express 4 ou compat: wrapper ainda aparece em codebases legacy.
const asyncHandler =
  <T extends express.RequestHandler>(fn: T): express.RequestHandler =>
  (req, res, next) => {
    Promise.resolve(fn(req, res, next)).catch(next);
  };

app.get(
  "/users/:id",
  asyncHandler(async (req, res) => {
    const user = await db.users.findById(req.params.id);
    res.json(user);
  }),
);
```

```typescript
import type { NextFunction, Request, Response } from "express";

app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  if (res.headersSent) return next(err);

  const status = err instanceof HttpError ? err.status : 500;
  res.status(status).type("application/problem+json").json({
    type: "about:blank",
    title: err.name,
    status,
    detail: status >= 500 ? "Unexpected error" : err.message,
    instance: req.originalUrl,
  });
});
```

```typescript
const userRouter = express.Router();
userRouter.get("/", listUsers);
userRouter.get("/:id", getUser);
userRouter.post("/", createUser);

app.use("/api/v1/users", userRouter);
```

## Na prática

Padrão típico em projetos TypeScript novos: Express 5 + `zod` + error middleware global + middlewares explícitos (`helmet`, `cors`, logger, rate limit) + routers por feature. `express.json({ limit })` deve ter limite explícito; body sem limite é porta para abuso de memória.

### Pipeline de uma request real

Uma request Express madura normalmente atravessa camadas em ordem. A ordem é o contrato:

```typescript
app.set("trust proxy", 1);

app.use(requestId());
app.use(logger());
app.use(helmet());
app.use(cors(corsOptions));
app.use(express.json({ limit: "1mb" }));

app.use("/api/v1/users", userRouter);
app.use(notFoundHandler);
app.use(problemDetailsHandler);
```

Se `problemDetailsHandler` vier antes dos routers, ele não verá erros das rotas. Se `express.json()` vier depois do router, `req.body` não existirá. Express dá liberdade; a dívida é documentar ordem.

### TypeScript sem mutação invisível

Mutar `req` é comum, mas precisa ser explícito. Para dados transversais, prefira `res.locals` quando o dado só será usado na resposta, ou declaration merging quando o dado realmente vira parte do contrato da request.

```typescript
declare global {
  namespace Express {
    interface Request {
      user?: { id: string; role: "admin" | "member" };
    }
  }
}

function authenticate(req: Request, _res: Response, next: NextFunction) {
  req.user = parseJwt(req.headers.authorization);
  next();
}
```

```typescript
function requireUser(req: Request, _res: Response, next: NextFunction) {
  if (!req.user) return next(new UnauthorizedError());
  next();
}
```

O ponto de code review: se uma rota assume `req.user`, o router precisa montar `authenticate` e `requireUser` antes da rota.

### Validation idiomática com zod

Express não tem validation nativa. Em 2026, um padrão simples é transformar schema em middleware.

```typescript
const validateBody =
  <T extends z.ZodTypeAny>(schema: T): express.RequestHandler =>
  (req, _res, next) => {
    const result = schema.safeParse(req.body);
    if (!result.success) return next(new ValidationError(result.error));
    req.body = result.data;
    next();
  };

userRouter.post("/", validateBody(CreateUserSchema), async (req, res) => {
  const user = await users.create(req.body);
  res.status(201).json(user);
});
```

Isso mantém controller fino e aproxima Express do modelo schema-first sem trocar de framework.

### Streaming e headers sent

Error handling em Express fica mais sutil quando a resposta já começou. A documentação oficial recomenda delegar ao handler default quando `res.headersSent`.

```typescript
app.get("/export", async (req, res, next) => {
  try {
    res.type("text/csv");
    await pipeline(exportUsersCsv(), res);
  } catch (err) {
    next(err);
  }
});
```

Se `pipeline` falhar depois de bytes enviados, não dá para trocar para JSON Problem Details. O máximo seguro é fechar conexão e logar com correlation ID. Essa fronteira conecta Express a [[03-Dominios/Node/Streams/index]].

### Organização por feature

Evite um `routes.ts` gigante. Uma estrutura comum:

```text
src/
├── app.ts
├── features/
│   └── users/
│       ├── users.router.ts
│       ├── users.controller.ts
│       ├── create-user.schema.ts
│       └── users.service.ts
└── shared/
    ├── errors/problem-details.ts
    └── middleware/request-id.ts
```

Express não impõe estrutura, então a estrutura precisa aparecer no repositório.

## Checklist de code review

- Error middleware é o último `app.use()`?
- Async handlers em Express 4 usam wrapper ou o app já está em Express 5?
- `express.json()` tem `limit` explícito?
- Routers são montados por feature, não todos no arquivo principal?
- Validation cobre body, params e query?
- Mutação de `req` tem tipo declarado?
- `res.headersSent` é tratado no error middleware?
- Health check não passa por auth pesada?
- Logs incluem request ID/correlation ID?

## Exercício de maturidade

Pegue uma rota Express escrita assim:

```typescript
app.post("/users", async (req, res) => {
  const user = await db.user.create({ data: req.body });
  res.json(user);
});
```

O refactor senior separa quatro concerns:

```typescript
userRouter.post(
  "/",
  validateBody(CreateUserSchema),
  asyncHandler(async (req, res) => {
    const user = await createUser.execute(req.body);
    res.status(201).json(UserPresenter.toHttp(user));
  }),
);
```

O que mudou:

- schema valida boundary;
- use case não conhece Express;
- presenter controla contrato de saída;
- erro sobe para middleware global;
- status code ficou explícito.

Esse é o tipo de evolução que transforma Express de "arquivo de rotas" em aplicação sustentável.

## Armadilhas

1. Express 4 com handler async sem wrapper: rejeição não chega ao error middleware.
2. Error middleware com 3 argumentos: Express não o reconhece como handler de erro.
3. Mutar `req` em middleware sem tipo/documentação: a ordem vira contrato invisível.
4. Chamar `res.send()` e depois `next(err)`: risco de `Cannot set headers after they are sent`.
5. Registrar error middleware antes das rotas: ele não captura o que vem depois.
6. Usar `app.use(auth)` global e quebrar `/health`, `/metrics` ou callback público.
7. Validar em controller depois de chamar service: dado inválido já atravessou boundary.
8. Capturar erro e responder direto em cada rota: perde consistência de [[08 - Error handling estruturado]].
9. Ignorar `trust proxy` atrás de load balancer: IP, HTTPS e secure cookies ficam errados.

## Perguntas de entrevista

**O que mudou no Express 5 para async handlers?**
Handlers e middlewares que retornam Promise chamam `next(value)` automaticamente quando rejeitam ou lançam erro. Em Express 4, wrapper ou `.catch(next)` ainda é necessário.

**Por que error middleware tem quatro argumentos?**
É como Express distingue middleware normal de error handler: `(err, req, res, next)`.

**Como você estruturaria Express em app médio?**
Routers por feature, schemas por boundary, services/use cases fora da camada HTTP, error middleware global e composition root explícito.

**Quando você não escolheria Express?**
Quando o time precisa de convenção forte, DI/lifecycle built-in ou contrato schema-first nativo. Nesses casos, NestJS ou Fastify podem reduzir decisões repetidas.

## Em entrevista

"Express is a minimal middleware-based framework. In Express 5, promise rejections from async route handlers automatically call `next(err)`, while Express 4 codebases commonly need an `asyncHandler` wrapper. Error middleware is different from regular middleware: it has four arguments, with `err` first, and it should be registered after routes."

Vocabulário-chave:

- middleware pipeline -> pipeline de middleware
- error middleware -> middleware de erro
- async wrapper -> wrapper assíncrono
- router mounting -> montagem de routers
- body limit -> limite de payload

## Fontes

- [Express](https://expressjs.com/)
- [Express error handling](https://expressjs.com/en/guide/error-handling.html)

## Veja também

- [[01 - Os 4 frameworks - Express, NestJS, Fastify, Hono]]
- [[07 - Middleware pipeline]]
- [[08 - Error handling estruturado]]
- [[09 - Validation com schema]]
- [[Node.js]]
