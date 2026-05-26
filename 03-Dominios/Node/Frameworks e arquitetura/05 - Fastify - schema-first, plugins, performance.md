---
title: "Fastify: schema-first, plugins, performance"
created: 2026-05-08
updated: 2026-05-08
type: concept
status: seedling
publish: true
tags:
  - node
  - frameworks
  - fastify
  - schema
  - performance
aliases:
  - Fastify
  - JSON schema
  - fastify-plugin
---

# Fastify: schema-first, plugins, performance

> [!abstract] TL;DR
> Fastify é performance-focused e schema-first. Route schemas validam input e serializam output com Ajv/fast-json-stringify. Plugins são encapsulados por default. É boa escolha para APIs com contrato claro e throughput relevante.

## O que é

Fastify é um framework HTTP de baixo overhead para Node. Seus pilares são performance, developer experience, hooks, plugins/decorators e uso recomendado de JSON Schema para validation/serialization.

## Por que importa

Quando API tem contrato claro, schema-first reduz validação ad-hoc e aproxima runtime, tipos e OpenAPI. Performance não deve ser a única métrica, mas em endpoints I/O-bound com alto volume a diferença de overhead pode importar.

## Como funciona

```typescript
import Fastify from "fastify";

const app = Fastify({ logger: true });
app.get("/hello", async () => ({ greeting: "hello" }));
await app.listen({ port: 3000 });
```

```typescript
app.post(
  "/users",
  {
    schema: {
      body: {
        type: "object",
        required: ["name", "email"],
        additionalProperties: false,
        properties: {
          name: { type: "string", minLength: 1 },
          email: { type: "string", format: "email" },
        },
      },
      response: {
        201: {
          type: "object",
          required: ["id", "name", "email"],
          properties: {
            id: { type: "string" },
            name: { type: "string" },
            email: { type: "string" },
          },
        },
      },
    },
  },
  async (req, reply) => {
    const user = await db.users.create(req.body);
    return reply.code(201).send(user);
  },
);
```

```typescript
import fp from "fastify-plugin";

async function dbPlugin(fastify: FastifyInstance) {
  const db = await connectDb();
  fastify.decorate("db", db);
  fastify.addHook("onClose", async () => db.close());
}

export default fp(dbPlugin);
```

```typescript
app.addHook("onRequest", async (req) => {
  req.startTime = Date.now();
});

app.addHook("onResponse", async (req) => {
  app.log.info({ url: req.url, ms: Date.now() - req.startTime });
});
```

```typescript
import { TypeBoxTypeProvider } from "@fastify/type-provider-typebox";
import { Type } from "@sinclair/typebox";

const typed = Fastify().withTypeProvider<TypeBoxTypeProvider>();
const UserSchema = Type.Object({ name: Type.String(), email: Type.String() });

typed.post("/users", { schema: { body: UserSchema } }, async (req) => {
  return { acceptedName: req.body.name };
});
```

## Na prática

Padrão forte: schema em toda rota, plugins por feature, encapsulation como isolamento e `@fastify/swagger` para derivar OpenAPI. Use `fastify-plugin` quando um plugin precisa expor decorators ao escopo pai.

### Lifecycle de hooks

Fastify não usa uma pipeline genérica estilo Express. Ele tem fases nomeadas. Isso melhora precisão, mas exige escolher o hook certo.

```text
onRequest
  -> preParsing
  -> preValidation
  -> preHandler
  -> handler
  -> preSerialization
  -> onSend
  -> onResponse
```

```typescript
app.addHook("preValidation", async (req) => {
  // Body já foi parseado; validation ainda vai acontecer.
  req.log.debug({ body: req.body }, "validating request");
});

app.addHook("preHandler", async (req) => {
  // Bom ponto para auth que precisa de params/body validados.
  await authorize(req);
});
```

`onRequest` é cedo demais para depender de body. `preHandler` é tarde demais para alterar parsing. Essa precisão é força e armadilha.

### Encapsulation como boundary

Encapsulation significa que plugins criam escopos. Rotas e decorators registrados dentro de um plugin ficam disponíveis para filhos, não necessariamente para irmãos ou pai.

```typescript
app.register(async function usersPlugin(users) {
  users.decorate("usersRepo", new UsersRepository());

  users.get("/users/:id", async function (req) {
    return this.usersRepo.findById(req.params.id);
  });
});
```

```typescript
app.register(async function ordersPlugin(orders) {
  // orders.usersRepo NÃO existe aqui.
  orders.get("/orders/:id", async () => ({ id: "ord_1" }));
});
```

Isso evita vazamento acidental. Quando o objetivo é plugin global, use `fastify-plugin`.

### Schema como contrato e performance

Schema em Fastify tem duas funções: valida entrada e permite serialização otimizada de saída.

```typescript
const UserResponse = {
  type: "object",
  required: ["id", "name", "email"],
  additionalProperties: false,
  properties: {
    id: { type: "string" },
    name: { type: "string" },
    email: { type: "string" },
  },
} as const;

app.get("/users/:id", {
  schema: {
    params: {
      type: "object",
      required: ["id"],
      properties: { id: { type: "string" } },
    },
    response: { 200: UserResponse },
  },
}, async (req) => users.findById(req.params.id));
```

Sem `response` schema, você perde parte do valor do framework: contrato de saída e serialização previsível.

### Testes com inject

Fastify tem `app.inject()`, útil para testar sem abrir porta.

```typescript
test("POST /users validates body", async () => {
  const app = buildApp();
  await app.ready();

  const res = await app.inject({
    method: "POST",
    url: "/users",
    payload: { name: "", email: "invalid" },
  });

  expect(res.statusCode).toBe(400);
  await app.close();
});
```

Esse padrão deixa teste rápido e evita flakiness de porta TCP.

## Checklist de code review

- Toda rota pública tem schema de body/query/params quando aplicável?
- Response schema existe para endpoints críticos?
- `additionalProperties: false` aparece onde contrato precisa ser estrito?
- Hooks estão na fase correta (`onRequest` vs `preHandler`)?
- Plugin encapsulation é intencional?
- `fastify-plugin` foi usado só quando precisa expor decorators?
- Testes usam `app.inject()` e fecham o app?
- Logs usam `req.log`, não logger global solto?

## Exercício de maturidade

Compare uma rota Fastify sem aproveitar o framework:

```typescript
app.post("/users", async (req, reply) => {
  if (!req.body.email) return reply.code(400).send({ error: "email required" });
  return db.users.create(req.body);
});
```

Com uma rota alinhada ao modelo Fastify:

```typescript
app.post("/users", {
  schema: {
    body: CreateUserBody,
    response: {
      201: UserResponse,
      400: ProblemDetailsResponse,
    },
  },
}, async (req, reply) => {
  const user = await createUser.execute(req.body);
  return reply.code(201).send(user);
});
```

A segunda versão torna validation, response contract e documentação derivável parte da rota. Se o projeto não quer isso, talvez Fastify não esteja sendo usado pelo motivo certo.

### Performance com responsabilidade

Fastify reduz overhead, mas não compensa:

- query N+1 no banco;
- payload gigante sem paginação;
- CPU-heavy JSON transform;
- chamada serial a serviços externos;
- logging síncrono excessivo.

O framework ajuda quando o gargalo é camada HTTP/serialization. Meça antes de vender performance como argumento principal.

## Armadilhas

1. Schema sem `additionalProperties: false`: payloads extras passam.
2. Decorator registrado em plugin encapsulado e esperado no app pai: não vaza por design.
3. Validation async batendo em banco: pode virar DoS; use hook depois da validation.
4. Teste sem `await app.ready()` ou `await app.close()`: lifecycle incompleto.
5. Usar `onRequest` esperando `req.body`: body ainda não foi parseado.
6. Não declarar response schema e perder serialização/contrato.
7. Misturar plugin global e feature plugin sem regra: escopo fica imprevisível.
8. Tratar Fastify como Express com `reply` diferente: o modelo é schema/hooks/plugins.

## Perguntas de entrevista

**Por que Fastify é chamado schema-first?**
Porque schemas ficam na definição da rota e participam de validation, serialization e documentação.

**O que é plugin encapsulation?**
É o isolamento de decorators, hooks e rotas por escopo de plugin. O que um plugin registra não vaza automaticamente para o pai ou irmãos.

**Quando escolher Fastify sobre Express?**
Quando contrato HTTP, validation, serialization e throughput importam mais do que o ecossistema máximo e a simplicidade absoluta.

**Qual hook você usaria para auth?**
Depende. Se precisa só de header, `onRequest` pode bastar. Se precisa de params/body validados, `preHandler` é mais seguro.

## Em entrevista

"Fastify is schema-first and performance-focused. You declare JSON Schemas for request and response; Fastify uses Ajv for validation and fast-json-stringify for serialization. Its plugin system is encapsulated by default, which keeps feature modules isolated. It is a strong fit when your API contract is explicit and throughput matters."

Vocabulário-chave:

- schema-first -> orientado por schema
- JSON Schema -> schema JSON
- type provider -> provedor de tipos
- plugin encapsulation -> encapsulamento de plugin
- throughput -> vazão

## Fontes

- [Fastify](https://fastify.dev/)
- [Fastify validation and serialization](https://fastify.dev/docs/latest/Reference/Validation-and-Serialization/)

## Veja também

- [[01 - Os 4 frameworks - Express, NestJS, Fastify, Hono]]
- [[07 - Middleware pipeline]]
- [[09 - Validation com schema]]
- [[12 - Decision tree + cheatsheet]]
- [[Node.js]]
