---
title: "Error handling estruturado"
created: 2026-05-08
updated: 2026-05-08
type: concept
status: seedling
publish: true
tags:
  - node
  - frameworks
  - error-handling
  - problem-details
  - rfc-7807
aliases:
  - Problem Details
  - RFC 7807
  - error middleware
---

# Error handling estruturado

> [!abstract] TL;DR
> Problem Details (RFC 7807) padroniza erros HTTP com `application/problem+json` e campos como `type`, `title`, `status`, `detail`, `instance`. Express implementa com error middleware; NestJS com exception filter; Fastify com `setErrorHandler`; Hono com `app.onError`.

## O que é

Error handling estruturado é tratar erro como contrato de API. Em vez de cada endpoint retornar JSON diferente, a API usa um envelope previsível que clientes e logs conseguem entender.

## Por que importa

Sem padrão, cliente faz parsing ad-hoc, observability perde contexto e bugs 4xx/5xx se misturam. Com Problem Details, cada erro tem status, título, detalhe e instância da request.

## Como funciona

```json
{
  "type": "https://api.example.com/errors/validation",
  "title": "Validation Failed",
  "status": 400,
  "detail": "Field 'email' must be a valid email",
  "instance": "/api/v1/users"
}
```

```typescript
class HttpError extends Error {
  constructor(
    public readonly status: number,
    public readonly type: string,
    message: string,
  ) {
    super(message);
  }
}

app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  if (res.headersSent) return next(err);
  const status = err instanceof HttpError ? err.status : 500;
  res.status(status).type("application/problem+json").json({
    type: err instanceof HttpError ? err.type : "about:blank",
    title: err.name,
    status,
    detail: status >= 500 ? "Unexpected error" : err.message,
    instance: req.originalUrl,
  });
});
```

```typescript
@Catch()
export class ProblemDetailsFilter implements ExceptionFilter {
  catch(exception: unknown, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const res = ctx.getResponse<Response>();
    const req = ctx.getRequest<Request>();
    const status = exception instanceof HttpException ? exception.getStatus() : 500;

    res.status(status).type("application/problem+json").json({
      type: "about:blank",
      title: "Error",
      status,
      detail: status >= 500 ? "Unexpected error" : String(exception),
      instance: req.url,
    });
  }
}
```

```typescript
app.setErrorHandler((err, req, reply) => {
  const status = err.statusCode ?? 500;
  reply.code(status).type("application/problem+json").send({
    type: "about:blank",
    title: err.name,
    status,
    detail: status >= 500 ? "Unexpected error" : err.message,
    instance: req.url,
  });
});
```

```typescript
app.onError((err, c) => {
  const status = err instanceof HTTPException ? err.status : 500;
  return c.json(
    { type: "about:blank", title: "Error", status, detail: err.message, instance: c.req.url },
    status,
    { "Content-Type": "application/problem+json" },
  );
});
```

Taxonomy prática:

- 4xx: cliente errou (validation, auth, not found).
- 5xx: servidor errou (bug, dependência indisponível, timeout interno).
- Programmer error: bug; logar e responder 500 genérico.
- Operational error: esperado; responder status específico.

## Na prática

Use handler global. Não exponha stack trace em produção. Inclua correlation ID via header/campo extra quando existir. Faça classes/tipos de erro pequenos: `ValidationError`, `NotFoundError`, `UnauthorizedError`, `ConflictError`.

### Taxonomy operacional

Uma API madura diferencia erro por origem e por ação esperada.

| Tipo | Exemplo | Status | Ação |
| --- | --- | --- | --- |
| Validation | body inválido | 400/422 | cliente corrige payload |
| Authn | token ausente/inválido | 401 | cliente autentica |
| Authz | sem permissão | 403 | cliente não deve repetir igual |
| Not found | recurso inexistente | 404 | cliente ajusta referência |
| Conflict | versão/estado conflita | 409 | cliente refaz fluxo |
| Rate limit | limite excedido | 429 | cliente aguarda |
| Dependency | DB/serviço fora | 503 | retry/backoff |
| Programmer | bug/type error | 500 | log + alerta |

Essa tabela deve virar código, não só documentação.

```typescript
abstract class AppError extends Error {
  abstract readonly status: number;
  abstract readonly type: string;
  abstract readonly title: string;
}

class ConflictError extends AppError {
  readonly status = 409;
  readonly type = "https://api.example.com/errors/conflict";
  readonly title = "Conflict";
}
```

### Problem Details com extensão

RFC 7807 permite membros extras. Use com parcimônia para campos úteis ao cliente.

```json
{
  "type": "https://api.example.com/errors/validation",
  "title": "Validation Failed",
  "status": 400,
  "detail": "Request body is invalid",
  "instance": "/api/v1/users",
  "invalidParams": [
    { "name": "email", "reason": "must be a valid email" }
  ]
}
```

O contrato deve ser estável. Não inclua stack, SQL, nome de tabela ou mensagem crua de dependência.

### Logs e resposta não são a mesma coisa

Resposta ao cliente deve ser sanitizada. Log interno deve ser rico.

```typescript
logger.error({
  err,
  requestId: req.id,
  path: req.originalUrl,
  userId: req.user?.id,
}, "request failed");

res.status(500).type("application/problem+json").json({
  type: "about:blank",
  title: "Internal Server Error",
  status: 500,
  detail: "Unexpected error",
  instance: req.originalUrl,
});
```

Essa separação reduz vazamento sem perder debuggability.

### Streaming e erro tardio

Depois que headers/body começaram, não há como responder Problem Details. Em Express, se `res.headersSent`, delegue ou encerre. Em streams, use [[03-Dominios/Node/Streams/index]] e `pipeline` para cleanup.

```typescript
if (res.headersSent) {
  req.log?.error({ err }, "streaming response failed after headers");
  return next(err);
}
```

## Checklist de code review

- Erros conhecidos têm classes/tipos explícitos?
- 4xx e 5xx não estão misturados?
- Stack trace nunca sai em produção?
- Logs internos têm request/correlation ID?
- Problem Details tem `type`, `title`, `status`, `detail`, `instance`?
- Validation errors têm formato parseável?
- Streaming trata `headersSent`?
- Retryable errors usam status adequado, como 503/429?

## Exercício de maturidade

Um handler imaturo responde erro localmente:

```typescript
app.post("/users", async (req, res) => {
  try {
    const user = await users.create(req.body);
    res.json(user);
  } catch (err) {
    res.status(500).json({ error: String(err) });
  }
});
```

Uma versão madura deixa a taxonomy centralizada:

```typescript
app.post("/users", asyncHandler(async (req, res) => {
  const user = await users.create(req.body);
  res.status(201).json(user);
}));

app.use(problemDetailsHandler);
```

```typescript
function problemDetailsHandler(err: unknown, req: Request, res: Response, next: NextFunction) {
  const problem = classifyError(err, req.originalUrl);
  req.log.error({ err, problem }, "request failed");
  res.status(problem.status).type("application/problem+json").json(problem);
}
```

O ponto de maturidade é ter um único lugar para policy de erro, com logs ricos e resposta estável.

### Erro de dependência externa

Dependência fora não é validation error. Use status e mensagem que ajudem cliente e operação.

```typescript
class PaymentProviderUnavailable extends AppError {
  readonly status = 503;
  readonly type = "https://api.example.com/errors/payment-provider-unavailable";
  readonly title = "Payment Provider Unavailable";
}
```

Inclua `Retry-After` quando fizer sentido. Não diga ao cliente "ECONNRESET from provider X" se isso não faz parte do contrato público.

## Armadilhas

1. Stack trace em produção: vazamento de informação.
2. Express error middleware com 3 args: não captura erro.
3. Responder 500 para validação ou 400 para DB down: taxonomy quebrada.
4. Handler async sem wrapper em Express 4: rejeição não chega ao handler global.
5. `detail` com mensagem interna de banco: pode vazar schema ou credenciais.
6. Responder erro diferente em cada endpoint.
7. Logar só `err.message` e perder stack/cause no log interno.
8. Converter todo erro desconhecido em 200 com `{ success: false }`.
9. Não diferenciar erro retryable de erro permanente.

## Perguntas de entrevista

**O que é Problem Details?**
Um formato padrão para erros HTTP estruturados com media type `application/problem+json` e campos como `type`, `title`, `status`, `detail`, `instance`.

**Por que não expor stack trace?**
Porque stack revela detalhes internos, paths, dependências e às vezes dados sensíveis. Stack pertence ao log, não à resposta.

**Como tratar erro de validação?**
Como erro 4xx com detalhes parseáveis por campo, sem transformar em 500.

**Como lidar com erro depois de iniciar streaming?**
Não tente trocar para JSON. Faça cleanup, logue, encerre/delegue conforme o framework.

## Em entrevista

"Problem Details, from RFC 7807, gives HTTP APIs a standard error envelope: `type`, `title`, `status`, `detail`, and `instance`, usually with `application/problem+json`. Express uses error middleware, NestJS uses exception filters, Fastify uses `setErrorHandler`, and Hono uses `app.onError`. The senior part is taxonomy: operational errors get specific 4xx/5xx responses, programmer errors get logged and sanitized."

Vocabulário-chave:

- Problem Details -> detalhes de problema
- error middleware -> middleware de erro
- exception filter -> filtro de exceção
- error taxonomy -> taxonomia de erros
- correlation ID -> identificador de correlação

## Fontes

- [RFC 7807](https://datatracker.ietf.org/doc/html/rfc7807)
- [Express error handling](https://expressjs.com/en/guide/error-handling.html)

## Veja também

- [[02 - Express idiomático]]
- [[04 - NestJS - guards, interceptors, pipes, filters]]
- [[05 - Fastify - schema-first, plugins, performance]]
- [[09 - Validation com schema]]
- [[Node.js]]
