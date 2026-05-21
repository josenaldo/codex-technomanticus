---
title: "NestJS: guards, interceptors, pipes, filters"
created: 2026-05-08
updated: 2026-05-08
type: concept
status: seedling
publish: true
tags:
  - node
  - frameworks
  - nestjs
  - guards
  - interceptors
  - pipes
  - filters
aliases:
  - NestJS lifecycle
  - "@UseGuards"
  - "@UseInterceptors"
  - ValidationPipe
---

# NestJS: guards, interceptors, pipes, filters

> [!abstract] TL;DR
> NestJS separa concerns no lifecycle da request: Guards decidem se a request passa; Pipes validam/transformam input; Interceptors envolvem o handler antes/depois; Exception Filters formatam erros. Cada hook pode ser aplicado por rota, controller ou globalmente.

## O que é

Esses quatro hooks são o motivo de NestJS não ser apenas routing com decorators. Eles transformam auth, validation, logging, cache, timeout e error handling em componentes reutilizáveis.

Fluxo mental:

```text
Middleware -> Guard -> Interceptor(before) -> Pipe -> Handler
                    -> Interceptor(after) -> Exception Filter(se erro)
```

## Por que importa

Sem lifecycle hooks, controllers acumulam boilerplate: checar auth, validar body, medir tempo, transformar resposta e formatar erro em cada método. Em NestJS idiomático, controller coordena caso de uso; concerns transversais ficam nos hooks certos.

## Como funciona

```typescript
@Injectable()
export class AuthGuard implements CanActivate {
  canActivate(ctx: ExecutionContext): boolean {
    const req = ctx.switchToHttp().getRequest<Request>();
    return Boolean(req.headers.authorization);
  }
}

@UseGuards(AuthGuard)
@Get("profile")
getProfile() {
  return this.users.current();
}
```

```typescript
@UsePipes(new ValidationPipe({ whitelist: true, forbidNonWhitelisted: true }))
@Post("users")
createUser(@Body() dto: CreateUserDto) {
  return this.users.create(dto);
}
```

```typescript
@Injectable()
export class TimingInterceptor implements NestInterceptor {
  intercept(_ctx: ExecutionContext, next: CallHandler) {
    const start = Date.now();
    return next.handle().pipe(
      tap(() => console.log(`request took ${Date.now() - start}ms`)),
    );
  }
}
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
      detail: exception instanceof Error ? exception.message : "Unexpected error",
      instance: req.url,
    });
  }
}
```

```typescript
// main.ts
app.useGlobalGuards(new AuthGuard());
app.useGlobalPipes(new ValidationPipe({ whitelist: true }));
app.useGlobalInterceptors(new TimingInterceptor());
app.useGlobalFilters(new ProblemDetailsFilter());
```

## Na prática

- Auth/autorização: Guard global ou por feature.
- Validation: `ValidationPipe` global com `whitelist` e `forbidNonWhitelisted`.
- Logging/timing/cache: Interceptor.
- Problem Details: Exception Filter global.
- Controller: fino, chamando use case/service.

### Escopo: global, controller ou rota

O mesmo hook pode ter escopos diferentes. A regra prática: global para política padrão, controller para feature, rota para exceção.

```typescript
// Global: toda request passa por validation.
app.useGlobalPipes(new ValidationPipe({ whitelist: true }));
```

```typescript
// Controller: todas as rotas de admin exigem auth.
@UseGuards(AdminGuard)
@Controller("admin/users")
export class AdminUsersController {}
```

```typescript
// Rota: cache só nesta operação.
@UseInterceptors(CacheInterceptor)
@Get("catalog")
findCatalog() {}
```

O erro comum é aplicar tudo globalmente e depois criar exceções em cascata. Global deve representar política quase universal.

### Guard: autenticação vs autorização

Autenticação responde "quem é?". Autorização responde "pode fazer isso?". Em apps reais, separar ajuda teste e composição.

```typescript
@Injectable()
export class JwtAuthGuard implements CanActivate {
  canActivate(ctx: ExecutionContext) {
    const req = ctx.switchToHttp().getRequest<Request>();
    req.user = verifyJwt(req.headers.authorization);
    return true;
  }
}

@Injectable()
export class RolesGuard implements CanActivate {
  canActivate(ctx: ExecutionContext) {
    const req = ctx.switchToHttp().getRequest<Request>();
    const required = this.reflector.get<Role[]>("roles", ctx.getHandler()) ?? [];
    return required.every((role) => req.user?.roles.includes(role));
  }
}
```

### Pipe: boundary de input

Pipe é boundary. Ele roda antes do handler e deve transformar input externo em shape confiável.

```typescript
@Get(":id")
findOne(@Param("id", ParseUUIDPipe) id: string) {
  return this.users.findOne(id);
}
```

```typescript
@Post()
create(@Body(new ZodPipe(CreateUserSchema)) input: CreateUserInput) {
  return this.createUser.execute(input);
}
```

Se a validação aparece dentro do service, o boundary HTTP já vazou.

### Interceptor: before/after e response mapping

Interceptor é ideal para medir tempo, mapear resposta, aplicar cache e timeout. Ele não deve virar lugar de regra de negócio.

```typescript
@Injectable()
export class EnvelopeInterceptor implements NestInterceptor {
  intercept(_ctx: ExecutionContext, next: CallHandler) {
    return next.handle().pipe(
      map((data) => ({ data, meta: { servedAt: new Date().toISOString() } })),
    );
  }
}
```

Se o interceptor precisa conhecer detalhes de domínio, provavelmente a regra pertence ao use case.

### Filter: taxonomy e Problem Details

Exception filter global deve converter tipos conhecidos em respostas previsíveis.

```typescript
@Catch(DomainError)
export class DomainErrorFilter implements ExceptionFilter {
  catch(error: DomainError, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const res = ctx.getResponse<Response>();

    res.status(error.status).type("application/problem+json").json({
      type: error.type,
      title: error.title,
      status: error.status,
      detail: error.message,
    });
  }
}
```

Não transforme todo erro em 500 genérico antes de classificar erros operacionais.

## Checklist de code review

- Guard faz autorização/autenticação, não valida DTO?
- Pipe cobre params/query/body?
- Interceptor não contém regra de domínio?
- Filter não expõe stack trace em produção?
- Hooks globais têm exceções explícitas para health/metrics?
- Ordem mental do lifecycle está documentada em features críticas?
- `ValidationPipe` tem `whitelist` e, quando apropriado, `forbidNonWhitelisted`?
- Uso de Observable/RxJS no interceptor é simples e não faz CPU-heavy work?

## Exercício de maturidade

Ao revisar um controller cheio de decorators, pergunte se cada decorator representa uma policy estável:

```typescript
@UseGuards(JwtAuthGuard, RolesGuard)
@UseInterceptors(AuditInterceptor)
@UsePipes(new ValidationPipe({ whitelist: true }))
@Post("invoices")
createInvoice(@Body() dto: CreateInvoiceDto) {}
```

Isso é aceitável se:

- auth é realmente política da rota;
- audit é concern transversal;
- validation pertence à boundary;
- controller continua fino.

Se decorators aparecem para corrigir comportamento específico de regra de negócio, provavelmente o use case está pobre e o controller virou orquestrador.

### Debug de lifecycle

Quando comportamento parece "fora de ordem", registre o lifecycle:

```typescript
logger.debug("guard");
logger.debug("interceptor before");
logger.debug("pipe");
logger.debug("handler");
logger.debug("interceptor after");
```

Esse tracing simples resolve boa parte das confusões entre Guard, Pipe e Interceptor.

## Armadilhas

1. Confundir Guard com Pipe: Guard autoriza; Pipe transforma/valida input.
2. Interceptor com trabalho CPU-heavy dentro de `tap`: bloqueia event loop.
3. Filter `@Catch()` genérico demais sem taxonomy: todos os erros viram iguais.
4. DTO sem decorators de validação: `ValidationPipe` não tem o que validar.
5. Aplicar hook global sem pensar em rotas públicas: auth pode bloquear health check.
6. Colocar regra de negócio no Guard porque ele "já roda antes".
7. Usar Interceptor para alterar input: isso é trabalho de Pipe.
8. Exception Filter que captura tudo e apaga status original.
9. Pipe que bate em banco para validação pesada em toda request.

## Perguntas de entrevista

**Qual a diferença entre Guard e Pipe?**
Guard decide se a request continua. Pipe valida/transforma dados de entrada.

**Por que Interceptor é útil para logging?**
Porque envolve o handler: consegue medir antes/depois e observar sucesso/erro sem poluir controller.

**Onde você implementaria Problem Details em NestJS?**
Em Exception Filter global, com mapping explícito de erros conhecidos para `application/problem+json`.

**Quando aplicar hook globalmente?**
Quando a política vale para quase toda aplicação: validation, logging, error formatting. Auth global exige cuidado com rotas públicas.

## Em entrevista

"NestJS request lifecycle has specialized hooks. Guards decide whether a request is allowed to proceed. Pipes validate and transform input, with `ValidationPipe` being the canonical example. Interceptors wrap the handler with before-and-after behavior, useful for logging, caching, and response transformation. Exception filters format errors, often as Problem Details. Each can be route-scoped, controller-scoped, or global."

Vocabulário-chave:

- guard -> guarda de autorização
- pipe -> validação/transformação
- interceptor -> wrapper de execução
- exception filter -> filtro de exceção
- lifecycle hook -> gancho do ciclo de vida

## Fontes

- [NestJS docs](https://docs.nestjs.com/)

## Veja também

- [[03 - NestJS - fundamentos]]
- [[07 - Middleware pipeline]]
- [[08 - Error handling estruturado]]
- [[09 - Validation com schema]]
- [[Node.js]]
