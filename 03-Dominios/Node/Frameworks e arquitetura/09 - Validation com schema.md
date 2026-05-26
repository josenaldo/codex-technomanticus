---
title: "Validation com schema"
created: 2026-05-08
updated: 2026-05-08
type: concept
status: seedling
publish: true
tags:
  - node
  - frameworks
  - validation
  - zod
  - schema
aliases:
  - zod
  - JSON Schema
  - ValidationPipe
  - class-validator
---

# Validation com schema

> [!abstract] TL;DR
> Schema-first é o padrão pragmático para validation em Node moderno. `zod` une schema, runtime validation e type inference; Fastify usa JSON Schema nativo; NestJS usa `ValidationPipe` com `class-validator` ou wrappers zod. O objetivo é evitar validação manual espalhada.

## O que é

Validation com schema define o contrato de input em um objeto reutilizável. Esse contrato valida dados em runtime e, dependendo da ferramenta, também gera tipos TypeScript e documentação.

## Por que importa

Toda entrada externa é `unknown`: body, query, params, headers, webhooks, mensagens de fila. Sem schema, validação vira if espalhado em controller. Com schema, validação fica centralizada, testável e reaproveitável.

## Como funciona

```typescript
import { z } from "zod";

const CreateUserSchema = z.object({
  name: z.string().min(1).max(100),
  email: z.string().email(),
  age: z.number().int().min(0).optional(),
}).strict();

type CreateUser = z.infer<typeof CreateUserSchema>;

app.post("/users", (req, res) => {
  const data: CreateUser = CreateUserSchema.parse(req.body);
  res.status(201).json(data);
});
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
          name: { type: "string", minLength: 1, maxLength: 100 },
          email: { type: "string", format: "email" },
          age: { type: "integer", minimum: 0 },
        },
      },
    },
  },
  async (req) => req.body,
);
```

```typescript
import { IsEmail, IsInt, IsOptional, IsString, MaxLength, Min, MinLength } from "class-validator";

export class CreateUserDto {
  @IsString()
  @MinLength(1)
  @MaxLength(100)
  name!: string;

  @IsEmail()
  email!: string;

  @IsOptional()
  @IsInt()
  @Min(0)
  age?: number;
}
```

```typescript
app.useGlobalPipes(
  new ValidationPipe({
    whitelist: true,
    forbidNonWhitelisted: true,
    transform: true,
  }),
);
```

```typescript
import { zValidator } from "@hono/zod-validator";

app.post("/users", zValidator("json", CreateUserSchema), (c) => {
  const data = c.req.valid("json");
  return c.json(data, 201);
});
```

## Na prática

`zod` é forte em projetos TypeScript por type inference e ergonomia. Fastify brilha quando JSON Schema já é o contrato da API e OpenAPI importa. NestJS clássico usa DTO class + decorators; projetos novos também podem padronizar zod com wrapper. `joi` ainda aparece em legacy, mas não é a escolha natural para TS-first.

### Boundary-first validation

Valide em todas as fronteiras externas, não apenas em controllers HTTP.

```typescript
const GithubWebhookSchema = z.object({
  action: z.string(),
  repository: z.object({ full_name: z.string() }),
  sender: z.object({ login: z.string() }),
}).strict();

export async function handleGithubWebhook(raw: unknown) {
  const event = GithubWebhookSchema.parse(raw);
  return processGithubEvent(event);
}
```

Esse mesmo padrão vale para Kafka, SQS, cron input, env vars e arquivos importados.

### Params, query e headers

Body é só uma parte da entrada.

```typescript
const Params = z.object({ id: z.string().uuid() });
const Query = z.object({
  page: z.coerce.number().int().min(1).default(1),
  pageSize: z.coerce.number().int().min(1).max(100).default(25),
});

app.get("/users/:id", (req, res) => {
  const params = Params.parse(req.params);
  const query = Query.parse(req.query);
  return users.findOne(params.id, query);
});
```

`z.coerce` é útil para query string, mas deve ser usado deliberadamente. Coerção ampla demais pode esconder input ruim.

### Input schema vs domain type

Nem todo schema de input é tipo de domínio. Input aceita strings, formatos externos e campos opcionais. Domínio pode exigir invariantes mais fortes.

```typescript
const CreateUserInput = z.object({
  name: z.string().min(1),
  email: z.string().email(),
});

class Email {
  private constructor(readonly value: string) {}

  static parse(value: string) {
    const email = z.string().email().parse(value);
    return new Email(email.toLowerCase());
  }
}
```

Schema de boundary protege a aplicação; value objects protegem o domínio.

### Versionamento de schema

APIs evoluem. Não altere schema de forma incompatível sem versionar contrato.

```typescript
const CreateUserV1 = z.object({
  name: z.string(),
  email: z.string().email(),
});

const CreateUserV2 = CreateUserV1.extend({
  locale: z.enum(["pt-BR", "en-US"]).default("en-US"),
});
```

Escolha uma estratégia: path (`/v1`, `/v2`), header, media type ou compatibilidade aditiva. O pior cenário é mudar silenciosamente.

### Erros de validação como Problem Details

Validation deve conversar com [[08 - Error handling estruturado]].

```typescript
function toProblem(error: z.ZodError, instance: string) {
  return {
    type: "https://api.example.com/errors/validation",
    title: "Validation Failed",
    status: 400,
    detail: "Request payload is invalid",
    instance,
    invalidParams: error.issues.map((issue) => ({
      name: issue.path.join("."),
      reason: issue.message,
    })),
  };
}
```

Cliente precisa de erro parseável; dev precisa de log completo.

## Checklist de code review

- Body, params, query e headers relevantes são validados?
- Schema é strict quando contrato exige?
- Coerção (`z.coerce`, transform) é intencional?
- Schema de input não foi confundido com entity de domínio?
- Erros de validation viram Problem Details estável?
- Schemas têm estratégia de versionamento?
- Mensagens de erro não vazam detalhes internos?
- Testes cobrem payload válido, inválido e campos extras?

## Exercício de maturidade

Validação manual típica:

```typescript
if (!body.email || !body.email.includes("@")) {
  throw new BadRequestError("invalid email");
}
```

Problemas:

- regra incompleta;
- mensagem inconsistente;
- tipo TypeScript não melhora;
- teste precisa cobrir cada if manual;
- controller cresce.

Schema-first:

```typescript
const Email = z.string().email().transform((value) => value.toLowerCase());

const CreateUser = z.object({
  name: z.string().trim().min(1).max(100),
  email: Email,
}).strict();
```

Agora o contrato é declarativo, reusável e testável.

### Testes de schema

Schemas merecem teste quando são contrato público.

```typescript
test("rejects unknown fields", () => {
  expect(() => CreateUser.parse({
    name: "Ada",
    email: "ada@example.com",
    admin: true,
  })).toThrow();
});
```

Esse teste protege contra regressão de `.strict()` removido por acidente.

## Armadilhas

1. Schema permissivo sem `.strict()` ou `additionalProperties: false`.
2. Validar só body e esquecer query/params/headers.
3. Misturar zod e `class-validator` sem convenção clara.
4. Mensagens de erro cruas demais para cliente final.
5. Validar depois do use case: domínio já recebeu dado inválido.
6. Transformar tudo em string com coerção e aceitar input ambíguo.
7. Usar schema de DTO como entity de domínio.
8. Alterar schema público sem versionamento.
9. Validar webhook depois de executar efeito colateral.

## Perguntas de entrevista

**Por que schema-first é melhor que validação manual?**
Porque centraliza contrato, reduz duplicação, permite type inference e torna erro/teste mais previsível.

**Onde validar query string?**
Na boundary HTTP, antes do use case. Query chega como string e precisa de parsing/coerção explícita.

**Qual a diferença entre DTO e entidade?**
DTO representa formato de entrada/saída. Entidade representa regra de domínio e invariantes internas.

**Como devolver erro de validação para cliente?**
Com formato estruturado, idealmente Problem Details com lista de campos inválidos.

## Em entrevista

"Schema-first validation is the modern Node pattern. With zod, you define a schema once and get both runtime validation and TypeScript inference through `z.infer`. Fastify uses JSON Schema natively for validation and serialization. NestJS traditionally uses DTO classes with `class-validator` through a global `ValidationPipe`, though zod wrappers are common. The senior pattern is validating every external boundary, not only request bodies."

Vocabulário-chave:

- schema-first -> orientado por schema
- type inference -> inferência de tipo
- JSON Schema -> schema JSON
- ValidationPipe -> pipe de validação
- external boundary -> fronteira externa

## Fontes

- [Zod](https://zod.dev/)
- [Fastify validation and serialization](https://fastify.dev/docs/latest/Reference/Validation-and-Serialization/)
- [NestJS docs](https://docs.nestjs.com/)

## Veja também

- [[04 - NestJS - guards, interceptors, pipes, filters]]
- [[05 - Fastify - schema-first, plugins, performance]]
- [[06 - Hono e edge runtimes]]
- [[08 - Error handling estruturado]]
- [[Node.js]]
