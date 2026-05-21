---
title: "Middleware pipeline"
created: 2026-05-08
updated: 2026-05-08
type: concept
status: seedling
publish: true
tags:
  - node
  - frameworks
  - middleware
  - pipeline
aliases:
  - Middleware
  - Hooks
  - Onion model
---

# Middleware pipeline

> [!abstract] TL;DR
> Middleware é a pipeline de funções que processa request/response ao redor do handler. Express usa `(req, res, next)`, Fastify usa hooks nomeados, NestJS usa middleware + interceptors/guards/pipes/filters, Hono usa onion model com `await next()`.

## O que é

Pipeline é onde entram concerns transversais: logging, auth, CORS, rate limit, parsing, tracing e error handling. O conceito é comum; o modelo de cada framework muda.

## Por que importa

Quem entende só Express tende a procurar `next()` em todo lugar. Em Fastify, o ponto certo pode ser `preHandler`; em NestJS, auth pode ser Guard; em Hono, after logic vem depois de `await next()`. Saber mapear o concern para o hook certo é skill de senior.

## Como funciona

```typescript
// Express: sequencial e mutável.
app.use((req, _res, next) => {
  req.startTime = Date.now();
  next();
});
```

```typescript
// Fastify: hooks nomeados por fase.
app.addHook("onRequest", async (req) => {
  req.startTime = Date.now();
});

app.addHook("onResponse", async (req) => {
  app.log.info({ ms: Date.now() - req.startTime });
});
```

```typescript
// NestJS: interceptor com before/after.
@Injectable()
class TimingInterceptor implements NestInterceptor {
  intercept(_ctx: ExecutionContext, next: CallHandler) {
    const start = Date.now();
    return next.handle().pipe(tap(() => log(Date.now() - start)));
  }
}
```

```typescript
// Hono: onion model.
app.use("*", async (_c, next) => {
  const start = Date.now();
  await next();
  console.log(`took ${Date.now() - start}ms`);
});
```

| Framework | Modelo | Mutação | Async | Before/after |
| --- | --- | --- | --- | --- |
| Express | `next()` callback | Comum | v5 nativo | Sequencial |
| Fastify | Hooks tipados | Parcial | Sim | Fase nomeada |
| NestJS | Interceptors + hooks | Sim | Sim | Lifecycle explícito |
| Hono | Onion com `await next()` | Sim | Sim | Mesmo middleware antes/depois |

## Na prática

- Logging: Express middleware, Fastify `onResponse`, NestJS interceptor, Hono onion.
- Auth: Express middleware, Fastify `preHandler`, NestJS Guard, Hono middleware com `c.set()`.
- CORS: `cors`, `@fastify/cors`, `app.enableCors()`, middleware Hono.
- Rate limit: lib específica por framework.

### Logging comparado

O mesmo concern muda de forma em cada framework.

```typescript
// Express
app.use((req, res, next) => {
  const start = Date.now();
  res.on("finish", () => logger.info({ path: req.path, ms: Date.now() - start }));
  next();
});
```

```typescript
// Fastify
app.addHook("onResponse", async (req, reply) => {
  req.log.info({ statusCode: reply.statusCode }, "request completed");
});
```

```typescript
// NestJS
return next.handle().pipe(
  tap(() => this.logger.log({ handler: ctx.getHandler().name })),
);
```

```typescript
// Hono
app.use("*", async (c, next) => {
  const start = Date.now();
  await next();
  console.log(c.req.path, Date.now() - start);
});
```

Express usa evento da response; Fastify já integra logger por request; NestJS envolve handler; Hono usa before/after no mesmo middleware.

### Auth comparado

Auth precisa escolher ponto do lifecycle conforme dado disponível.

```typescript
// Express: middleware antes do router protegido.
app.use("/api/private", authenticate, privateRouter);
```

```typescript
// Fastify: preHandler depois de parsing/validation.
app.addHook("preHandler", async (req) => {
  req.user = await authenticate(req.headers.authorization);
});
```

```typescript
// NestJS: Guard.
@UseGuards(AuthGuard, RolesGuard)
@Get("admin/report")
report() {}
```

```typescript
// Hono: contexto tipado.
app.use("/private/*", async (c, next) => {
  c.set("user", await authenticate(c.req.header("authorization")));
  await next();
});
```

### Antes/depois nem sempre existe

Express middleware clássico não tem after natural. Você precisa ouvir `finish`/`close` na response. Hono onion e NestJS interceptor têm after explícito. Fastify tem hooks de response.

```typescript
app.use((req, res, next) => {
  res.on("finish", () => audit(req, res.statusCode));
  res.on("close", () => auditAborted(req));
  next();
});
```

Esse detalhe importa para métricas: `finish` indica resposta enviada; `close` pode indicar conexão abortada.

### Ordem vs fase nomeada

Express e Hono dependem fortemente da ordem de registro. Fastify e NestJS dão nomes/fases, mas ainda há ordem dentro do mesmo escopo.

```typescript
app.use(authenticate);
app.use(authorize);
app.use(router);
```

```typescript
app.addHook("preHandler", authenticate);
app.addHook("preHandler", authorize);
```

O modelo muda, mas o princípio permanece: pipeline é contrato.

## Checklist de code review

- O concern está no hook certo ou foi enfiado no controller?
- Há diferença clara entre authn e authz?
- Métricas capturam sucesso, erro e conexão abortada?
- Middleware CPU-heavy foi evitado?
- A ordem de middlewares está documentada?
- Dados adicionados ao contexto/request têm tipo?
- Error handling conversa com [[08 - Error handling estruturado]]?
- CORS/rate limit/body parser estão antes das rotas certas?

## Exercício de maturidade

Uma API imatura repete concerns em cada handler:

```typescript
app.get("/orders", async (req, res) => {
  const start = Date.now();
  if (!req.headers.authorization) return res.sendStatus(401);
  try {
    res.json(await orders.list());
  } finally {
    console.log(Date.now() - start);
  }
});
```

A versão madura move concerns para pipeline:

```typescript
app.use(requestId);
app.use(timing);
app.use(authenticate);
app.get("/orders", listOrders);
app.use(problemDetailsHandler);
```

O handler volta a expressar o caso de uso. A pipeline expressa policies transversais.

### Ordem recomendada por categoria

```text
request id / tracing
security headers
CORS
body parser com limite
rate limit barato
authn
authz
validation
handler
not found
error handler
```

Nem todo framework usa exatamente essa sequência, mas o raciocínio ajuda: coloque proteções baratas antes de operações caras.

### Quando não usar middleware

Nem toda lógica compartilhada é middleware. Regra de domínio compartilhada deve ir para service/use case/policy, não para pipeline HTTP.

```typescript
// Ruim: middleware decide regra de desconto.
app.use(applyBlackFridayDiscount);

// Melhor: policy de domínio chamada pelo use case.
const price = discountPolicy.apply(order, campaign);
```

## Armadilhas

1. Express: ordem de `app.use()` decide comportamento.
2. Fastify: `onRequest` roda antes de parsing/validation; nem todo dado está disponível.
3. NestJS: middleware tradicional é mais cru; interceptor/guard tem melhor integração com DI.
4. Hono: sem `await next()`, o handler posterior não executa.
5. Middleware que faz CPU-heavy work bloqueia [[03-Dominios/Node/Runtime e Event Loop/index]].
6. Logging só no caminho feliz: erros e aborts ficam invisíveis.
7. Auth global bloqueando `/health` e `/metrics`.
8. Rate limit depois de operação cara: ataque ainda consome CPU/DB.
9. Contexto mutável sem tipagem: bug aparece longe da origem.

## Perguntas de entrevista

**Onde colocar logging?**
Na pipeline, não no controller. O mecanismo muda por framework: Express response events, Fastify `onResponse`, NestJS interceptor, Hono onion.

**Qual a diferença entre middleware e interceptor em NestJS?**
Middleware é mais próximo do Express e roda cedo; interceptor é DI-aware e envolve o handler.

**Por que Fastify tem hooks nomeados?**
Para dar pontos precisos do lifecycle, como `onRequest`, `preValidation`, `preHandler`, `onResponse`.

**Qual bug comum em Hono/Koa-like?**
Esquecer `await next()`, impedindo a continuação da pipeline.

## Em entrevista

"Middleware is the cross-cutting pipeline around handlers, but each framework models it differently. Express is sequential and mutation-friendly with `(req, res, next)`. Fastify has lifecycle hooks like `onRequest`, `preHandler`, and `onResponse`. NestJS uses both traditional middleware and DI-aware hooks such as guards and interceptors. Hono uses the Koa-like onion model with `await next()`."

Vocabulário-chave:

- middleware -> middleware
- hook -> gancho
- interceptor -> interceptor
- onion model -> modelo cebola
- request lifecycle -> ciclo de vida da request

## Veja também

- [[02 - Express idiomático]]
- [[04 - NestJS - guards, interceptors, pipes, filters]]
- [[05 - Fastify - schema-first, plugins, performance]]
- [[06 - Hono e edge runtimes]]
- [[Node.js]]
