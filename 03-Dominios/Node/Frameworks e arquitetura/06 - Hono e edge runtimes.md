---
title: "Hono e edge runtimes"
created: 2026-05-08
updated: 2026-05-08
type: concept
status: seedling
publish: true
tags:
  - node
  - frameworks
  - hono
  - edge
  - cloudflare-workers
  - serverless
aliases:
  - Hono
  - edge runtime
  - Cloudflare Workers
  - Deno Deploy
---

# Hono e edge runtimes

> [!abstract] TL;DR
> Hono é um framework ultralight baseado em Web Standards e Fetch API. Roda em Cloudflare Workers, Deno, Bun, AWS Lambda e Node. É boa escolha quando o deploy é edge/serverless multi-runtime; é ruim quando o app depende de APIs Node-only.

## O que é

Hono é um framework HTTP minimalista e multi-runtime. Em vez de `req`/`res` estilo Node, ele trabalha perto de `Request`/`Response` da Fetch API e expõe um contexto `c`.

## Por que importa

Edge runtimes mudam o contrato. Cloudflare Workers e similares não são "Node completo em outro lugar": `fs`, TCP custom, processos longos e várias libs nativas podem não existir. Hono dá uma API uniforme para escrever Web APIs nesse ambiente.

## Como funciona

```typescript
import { Hono } from "hono";

const app = new Hono();
app.get("/hello", (c) => c.json({ greeting: "hello" }));

export default app;
```

```typescript
// Mesmo app.fetch pode ser adaptado por runtime.
// Cloudflare Workers: export default app;
// Node: serve({ fetch: app.fetch })
// Deno: Deno.serve(app.fetch)
// Bun: export default { fetch: app.fetch }
```

```typescript
app.use("*", async (c, next) => {
  const start = Date.now();
  await next();
  const ms = Date.now() - start;
  console.log(`${c.req.method} ${c.req.url} ${ms}ms`);
});
```

```typescript
import { zValidator } from "@hono/zod-validator";
import { z } from "zod";

const CreateUser = z.object({
  name: z.string().min(1),
  email: z.string().email(),
});

app.post("/users", zValidator("json", CreateUser), (c) => {
  const data = c.req.valid("json");
  return c.json({ id: crypto.randomUUID(), ...data }, 201);
});
```

```typescript
import { HTTPException } from "hono/http-exception";

app.onError((err, c) => {
  const status = err instanceof HTTPException ? err.status : 500;
  return c.json(
    { type: "about:blank", title: "Error", status, detail: err.message },
    status,
    { "Content-Type": "application/problem+json" },
  );
});
```

## Na prática

Use Hono quando o deploy é Cloudflare Workers, Vercel Edge, Deno Deploy, Lambda@Edge ou quando a portabilidade multi-runtime é requisito. Prefira Express/Fastify/NestJS quando o app é Node-only, precisa de libs Node-specific ou tem integração profunda com filesystem, sockets, streams Node ou infraestrutura tradicional.

### Fetch API como contrato

Hono funciona bem porque fica perto do contrato universal da plataforma web: `Request`, `Response`, headers, URL e body streams. O contexto `c` é ergonomia em cima disso.

```typescript
app.get("/search", (c) => {
  const url = new URL(c.req.url);
  const q = url.searchParams.get("q") ?? "";
  return c.json({ query: q });
});
```

```typescript
app.get("/raw", () => {
  return new Response(JSON.stringify({ ok: true }), {
    status: 200,
    headers: { "content-type": "application/json" },
  });
});
```

Essa proximidade com Web Standards reduz lock-in de Node, mas também remove confortos do ecossistema Node tradicional.

### Bindings e ambiente

Em edge runtimes, dependências externas frequentemente aparecem como bindings, não como clients globais criados no startup.

```typescript
type Env = {
  Bindings: {
    KV: KVNamespace;
    DB: D1Database;
  };
};

const app = new Hono<Env>();

app.get("/flags/:userId", async (c) => {
  const flags = await c.env.KV.get(`flags:${c.req.param("userId")}`, "json");
  return c.json(flags ?? {});
});
```

Isso muda o desenho da aplicação: composition root tradicional dá lugar a adapters por runtime.

### Middleware onion na prática

O modelo onion permite before/after em um único middleware.

```typescript
app.use("*", async (c, next) => {
  const requestId = crypto.randomUUID();
  c.set("requestId", requestId);

  await next();

  c.res.headers.set("x-request-id", requestId);
});
```

Se `await next()` for esquecido, nada depois roda. Se `next()` for chamado duas vezes, a pipeline fica inválida.

### Limites de edge

Não fixe números absolutos como se fossem universais; cada provedor muda limites. O modelo mental é:

- CPU time menor que server tradicional.
- Memória limitada.
- Startup rápido importa.
- Conexões longas e sockets custom podem não existir.
- `fs`, `net`, `tls` e libs nativas podem falhar.
- Storage costuma ser remoto: KV, D1, Durable Objects, S3-like APIs.

```typescript
// Ruim para edge: depende de filesystem local.
const template = await fs.promises.readFile("email.html", "utf8");
```

```typescript
// Melhor: asset/binding/config entregue pelo runtime.
const template = await c.env.ASSETS.fetch(new URL("/email.html", c.req.url));
```

## Checklist de code review

- O código usa Web APIs ou APIs Node-only?
- Dependências externas existem no runtime alvo?
- Middleware chama `await next()` exatamente uma vez?
- Estado global é cache seguro ou estado de negócio indevido?
- Handlers evitam CPU-heavy work?
- Storage é compatível com edge/serverless?
- Observability considera cold start e request ID?
- Testes cobrem adapter Node e runtime alvo quando houver portabilidade real?

## Exercício de maturidade

Uma rota Hono que parece portátil pode esconder dependência de Node:

```typescript
import { readFile } from "node:fs/promises";

app.get("/template", async (c) => {
  return c.html(await readFile("template.html", "utf8"));
});
```

Em Node funciona; em Cloudflare Workers falha. A versão edge-aware usa asset/binding ou bundling:

```typescript
app.get("/template", async (c) => {
  const asset = await c.env.ASSETS.fetch(new URL("/template.html", c.req.url));
  return new Response(asset.body, {
    headers: { "content-type": "text/html; charset=utf-8" },
  });
});
```

O ponto de maturidade é auditar dependências por runtime, não só compilar TypeScript.

### Estado e cache

Estado global em edge deve ser tratado como cache oportunista, não fonte de verdade.

```typescript
let cachedConfig: Config | undefined;

app.get("/config", async (c) => {
  cachedConfig ??= await loadConfig(c.env.KV);
  return c.json(cachedConfig);
});
```

Isso pode reduzir latência, mas não deve ser usado para carrinho, saldo, sessão crítica ou qualquer dado que exige consistência forte.

### Observability em edge

Logs e tracing podem ser diferentes do Node tradicional. Inclua request ID na resposta e no log, porque debugar execução distribuída sem correlação é caro.

```typescript
app.use("*", async (c, next) => {
  const requestId = crypto.randomUUID();
  await next();
  c.res.headers.set("x-request-id", requestId);
  console.log(JSON.stringify({ requestId, path: c.req.path, status: c.res.status }));
});
```

### Regra prática final

Hono é uma escolha de runtime antes de ser uma escolha de estilo. Se o app precisa ser Web Standards-first, edge-friendly e pequeno, ele encaixa. Se o app é um backend Node tradicional com várias integrações Node-only, Hono pode até funcionar, mas deixa de ser a escolha óbvia.

### Sinal de resposta madura

Em entrevista, não venda Hono como "mais rápido" ou "mais novo". Venda como compatibilidade de plataforma:

```text
I would choose Hono when the platform is edge or multi-runtime.
The implementation consequence is auditing dependencies for Web API compatibility
and isolating provider-specific bindings from domain logic.
```

Essa resposta conecta framework, runtime e arquitetura.

## Armadilhas

1. Assumir `fs`/`net` em edge runtime: falha fora de Node.
2. Fazer CPU-heavy handler em edge: limites de tempo e CPU são menores.
3. Guardar estado mutável global: edge pode escalar/isolar instâncias de forma diferente.
4. Esquecer `await next()` no middleware onion: o handler posterior não roda.
5. Usar biblioteca de auth/storage que depende de Node internals.
6. Tratar KV como banco transacional: consistência e latência podem ser diferentes.
7. Criar client pesado por request sem necessidade.
8. Achar que multi-runtime é grátis: cada runtime tem bindings e deploy próprios.

## Perguntas de entrevista

**O que diferencia Hono de Express?**
Hono é baseado em Fetch API e Web Standards, pensado para múltiplos runtimes. Express é centrado no modelo HTTP de Node.

**Quando Hono não é boa escolha?**
Quando o app depende profundamente de APIs Node-only, sockets, filesystem local, libs nativas ou processos longos.

**O que é onion middleware?**
Um middleware executa lógica antes de `await next()` e depois que os próximos handlers terminam.

**Qual é a decisão principal antes de usar Hono?**
Confirmar deploy target. Se o runtime é edge/serverless multi-runtime, Hono faz sentido; se é Node container tradicional, compare com Express/Fastify.

## Em entrevista

"Hono is an ultralight, multi-runtime framework built on Web Standards. It uses the Fetch API model instead of Node's `req` and `res`, and it runs on Cloudflare Workers, Deno, Bun, AWS Lambda, and Node. The decision is deploy-driven: choose it for edge or serverless multi-runtime apps; avoid it when the application depends deeply on Node-only APIs."

Vocabulário-chave:

- edge runtime -> runtime de borda
- Fetch API native -> nativo da Fetch API
- multi-runtime -> múltiplos runtimes
- ultralight -> ultraleve
- onion middleware -> middleware em cebola

## Fontes

- [Hono docs](https://hono.dev/docs)

## Veja também

- [[01 - Os 4 frameworks - Express, NestJS, Fastify, Hono]]
- [[07 - Middleware pipeline]]
- [[09 - Validation com schema]]
- [[12 - Decision tree + cheatsheet]]
- [[Node.js]]
