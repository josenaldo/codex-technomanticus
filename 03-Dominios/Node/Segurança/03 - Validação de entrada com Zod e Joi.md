---
title: "Validação de entrada com Zod e Joi"
created: 2026-05-12
updated: 2026-05-13
type: concept
status: growing
publish: true
tags:
  - node
  - segurança
  - validação
  - zod
  - joi
aliases:
  - Validação de entrada Node
  - Zod Node
  - Joi Node
---

# Validação de entrada com Zod e Joi

> [!abstract] TL;DR
> Nunca confiar em input externo é o axioma central de segurança de APIs: qualquer dado que cruza a fronteira da sua aplicação — body de requisição, query string, parâmetros de rota, cabeçalhos HTTP, mensagens de fila — deve ser validado e sanitizado antes de ser processado. Input não validado é o vetor que alimenta injection attacks (SQL, NoSQL, command), prototype pollution via `__proto__` em JSON, XSS em campos de texto e ReDoS via strings longas em expressões regulares. Zod v3 é a escolha padrão em projetos TypeScript modernos porque infere tipos estaticamente a partir do schema, eliminando a duplicação entre runtime e compile-time; Joi v17 domina codebases Node.js legados com API encadeada e madura. A validação deve acontecer na borda do sistema — no middleware de rota, antes de qualquer lógica de negócio ou acesso ao banco — e erros de validação devem retornar HTTP 422 Unprocessable Entity com mensagens estruturadas, não 500 genérico.

## O que é

**Validação de entrada** é o processo de verificar que dados externos — vindos de requisições HTTP, mensagens de fila, arquivos carregados, argumentos de CLI — estão no formato esperado, dentro dos limites aceitáveis e livres de conteúdo malicioso antes de serem processados pela aplicação.

**Schema validation** é a abordagem declarativa dominante: define-se um schema (contrato estrutural) que descreve o formato esperado dos dados, e uma biblioteca de validação verifica conformidade e extrai os valores tipados. É diferente de validação imperativa (uma série de `if` statements) — o schema é reutilizável, autodocumentado e composável.

As duas bibliotecas dominantes no ecossistema Node.js são:

- **Zod v3** — schema-first, TypeScript-native, inferência de tipos automática, zero dependências. Padrão em projetos modernos com TypeScript.
- **Joi v17** — API orientada a objetos encadeada, amplamente usada em codebases Node.js legados e JavaScript puro, referência no ecossistema hapi/Fastify histórico.

## Por que validação de entrada é segurança

Validação não é apenas "qualidade de dados" — é a primeira linha de defesa contra vetores de ataque que exploram a ausência de checagem na borda da aplicação.

### Injection attacks

**NoSQL injection** ocorre quando input do usuário é inserido diretamente em uma query MongoDB sem sanitização:

```javascript
// ❌ Sem validação — vulnerável a NoSQL injection
app.post('/login', async (req, res) => {
  const { username, password } = req.body;
  // Atacante envia: { "username": "admin", "password": { "$ne": null } }
  // A query encontra o usuário admin sem verificar a senha real
  const user = await User.findOne({ username, password });
  if (user) return res.json({ token: generateToken(user) });
  res.status(401).json({ error: 'Invalid credentials' });
});
```

Com validação de schema que rejeita qualquer campo que não seja string simples, o vetor é eliminado: `{ "$ne": null }` falha na validação porque não é string.

**SQL injection** e **command injection** seguem o mesmo padrão — input não validado que carrega metacaracteres (`'`, `;`, `|`, `` ` ``) atinge o parser do banco ou do shell com consequências arbitrárias.

### Prototype pollution

JSON bodies podem conter campos como `__proto__` ou `constructor` que, ao serem atribuídos a objetos JavaScript, corrompem o prototype chain de todos os objetos da aplicação:

```javascript
// ❌ Merge ingênuo — vulnerável a prototype pollution
app.post('/merge-config', (req, res) => {
  const config = {};
  Object.assign(config, req.body);
  // Atacante envia: { "__proto__": { "isAdmin": true } }
  // Agora ({}).isAdmin === true em qualquer objeto novo
});
```

Validação de schema com Zod ou Joi rejeita chaves desconhecidas como `__proto__` por padrão (modo `strict`) ou via `.strip()` — o campo é descartado antes de chegar à aplicação.

### XSS via campos de texto

Campos de texto sem restrição de formato que chegam a templates HTML ou são armazenados e exibidos posteriormente são vetores de XSS (Cross-Site Scripting). Validação define limites de comprimento e formato; sanitização remove ou escapa HTML. Ambos são necessários para campos de rich text.

### ReDoS (Regular Expression Denial of Service)

Expressões regulares com backtracking catastrófico podem consumir CPU exponencialmente quando alimentadas com strings longas cuidadosamente construídas. Um campo de email sem `.max(254)` aceita strings de megabytes que travam o event loop Node.js (single-threaded) por segundos:

```javascript
// ❌ Regex vulnerável a ReDoS sem limite de comprimento
const emailRegex = /^([a-zA-Z0-9])(([a-zA-Z0-9])*([._-])?([a-zA-Z0-9]))*@([a-zA-Z0-9]+)(([\.\-]?[a-zA-Z0-9]+)*)\.([a-zA-Z]{2,})$/;
// Input: "a".repeat(50) + "@" + "b".repeat(50) → trava o event loop
```

Com `.max(254)` no schema, strings longas são rejeitadas antes de chegar à regex.

## Zod v3

Zod é uma biblioteca TypeScript-first de schema declaration e validation. O diferencial fundamental é a **inferência de tipos**: o tipo TypeScript é derivado automaticamente do schema em runtime, eliminando a necessidade de declarar o tipo manualmente e manter schema e tipo em sincronia.

```typescript
import { z } from 'zod';

const UserSchema = z.object({ name: z.string() });
type User = z.infer<typeof UserSchema>; // { name: string }
// Tipo derivado do schema — nunca desincronizam
```

### Primitivos e estruturas básicas

```typescript
import { z } from 'zod';

// Tipos primitivos
const StringSchema = z.string();
const NumberSchema = z.number();
const BooleanSchema = z.boolean();
const DateSchema = z.date();

// Strings com restrições
const EmailSchema = z.string().email().max(254).toLowerCase();
const PasswordSchema = z.string().min(8).max(72).regex(
  /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])/,
  { message: 'Password must contain uppercase, lowercase, number and special char' }
);
const SlugSchema = z.string().min(1).max(100).regex(/^[a-z0-9-]+$/);

// Números com restrições
const AgeSchema = z.number().int().min(0).max(150);
const PriceSchema = z.number().positive().finite().multipleOf(0.01);
const PageSchema = z.number().int().min(1).default(1);

// Enums e unions
const RoleSchema = z.enum(['admin', 'editor', 'viewer']);
const StatusSchema = z.union([z.literal('active'), z.literal('inactive'), z.literal('pending')]);

// Arrays
const TagsSchema = z.array(z.string().min(1).max(50)).min(1).max(10);

// Opcionais e defaults
const OptionalBioSchema = z.string().max(500).optional();  // string | undefined
const NullableField = z.string().nullable();               // string | null
const WithDefault = z.number().default(0);                 // number, default 0 se ausente

// Objetos
const AddressSchema = z.object({
  street: z.string().min(1).max(200),
  city: z.string().min(1).max(100),
  country: z.string().length(2),  // ISO 3166-1 alpha-2
  zip: z.string().regex(/^\d{5}(-\d{4})?$/).optional(),
});
```

### parse vs safeParse

A diferença entre os dois métodos é o modelo de erro — `parse` lança exceção, `safeParse` retorna um resultado discriminado:

```typescript
import { z } from 'zod';

const Schema = z.object({
  name: z.string().min(1),
  age: z.number().int().min(0),
});

// parse — lança ZodError se inválido
// Use quando falha é exceção não recuperável (ex: validação de env vars na startup)
try {
  const data = Schema.parse({ name: 'Alice', age: 30 });
  // data é tipado como { name: string; age: number }
  console.log(data.name); // TypeScript sabe o tipo
} catch (err) {
  if (err instanceof z.ZodError) {
    console.error(err.errors); // ZodIssue[]
  }
}

// safeParse — nunca lança, retorna discriminated union
// Use em middleware de API — você controla o response de erro
const result = Schema.safeParse({ name: '', age: -1 });

if (!result.success) {
  // result.error é ZodError
  const errors = result.error.errors.map(e => ({
    path: e.path.join('.'),
    message: e.message,
  }));
  // [{ path: 'name', message: 'String must contain at least 1 character(s)' },
  //  { path: 'age', message: 'Number must be greater than or equal to 0' }]
} else {
  // result.data é tipado corretamente
  console.log(result.data.name);
}
```

**Regra prática:**
- `parse` → validação de env vars na startup (fail-fast desejado), testes unitários
- `safeParse` → middleware de API (você quer retornar 422, não deixar o erro borbulhar como 500)

### Transformações

`.transform()` converte o valor após validação bem-sucedida. `.preprocess()` converte *antes* da validação — útil para coerção de tipos de query strings (que chegam como string):

```typescript
import { z } from 'zod';

// preprocess — converte antes de validar (query params chegam como string)
const PageSchema = z.preprocess(
  (val) => (typeof val === 'string' ? parseInt(val, 10) : val),
  z.number().int().min(1).max(1000).default(1)
);

PageSchema.parse('5');   // 5 (number)
PageSchema.parse('abc'); // ZodError: Expected number, received nan

// transform — transforma após validação
const EmailSchema = z.string().email().transform(val => val.toLowerCase().trim());
EmailSchema.parse(' ALICE@Example.COM '); // 'alice@example.com'

// Transformação complexa — converter data string em Date object
const DateStringSchema = z.string()
  .regex(/^\d{4}-\d{2}-\d{2}$/, 'Use YYYY-MM-DD format')
  .transform(val => new Date(val));
// z.infer<typeof DateStringSchema> é Date, não string

// pipe — encadeia schemas (alternativa moderna ao preprocess)
const CoercedPage = z.string().pipe(z.coerce.number().int().min(1));
```

### Refinamentos

`.refine()` adiciona validação customizada com acesso ao valor completo. `.superRefine()` dá controle total sobre os erros gerados, incluindo path e código:

```typescript
import { z } from 'zod';

// refine — validação customizada simples
const PasswordConfirmSchema = z.object({
  password: z.string().min(8),
  confirmPassword: z.string(),
}).refine(
  (data) => data.password === data.confirmPassword,
  {
    message: 'Passwords do not match',
    path: ['confirmPassword'],  // erro aparece no campo confirmPassword
  }
);

// superRefine — controle total, múltiplos erros customizados
const CreditCardSchema = z.object({
  number: z.string(),
  expiry: z.string(),
  cvv: z.string(),
}).superRefine((data, ctx) => {
  if (!luhnCheck(data.number)) {
    ctx.addIssue({
      code: z.ZodIssueCode.custom,
      path: ['number'],
      message: 'Invalid card number (Luhn check failed)',
    });
  }
  if (!isValidExpiry(data.expiry)) {
    ctx.addIssue({
      code: z.ZodIssueCode.custom,
      path: ['expiry'],
      message: 'Card is expired or expiry format is invalid (MM/YY)',
    });
  }
});
```

### Mensagens de erro customizadas

Zod aceita mensagens customizadas inline em cada validação, ou via objeto `{ message }`:

```typescript
import { z } from 'zod';

const ProductSchema = z.object({
  name: z.string({
    required_error: 'Product name is required',
    invalid_type_error: 'Product name must be a string',
  }).min(1, 'Name cannot be empty').max(200, 'Name is too long (max 200 chars)'),

  price: z.number({
    required_error: 'Price is required',
    invalid_type_error: 'Price must be a number',
  }).positive('Price must be positive').finite('Price must be a finite number'),

  category: z.enum(['electronics', 'clothing', 'food'], {
    errorMap: (issue, ctx) => ({
      message: `Category must be one of: electronics, clothing, food. Got: ${ctx.data}`,
    }),
  }),

  sku: z.string().regex(/^[A-Z]{2}-\d{6}$/, {
    message: 'SKU must follow format: XX-000000 (2 uppercase letters, hyphen, 6 digits)',
  }),
});
```

### Schema completo para request body de API REST

```typescript
import { z } from 'zod';

// Schema de criação de usuário — exemplo completo de produção
export const CreateUserSchema = z.object({
  // Campos obrigatórios
  email: z.string({
    required_error: 'Email is required',
  })
    .email('Invalid email address')
    .max(254, 'Email too long')
    .toLowerCase()
    .trim(),

  password: z.string({
    required_error: 'Password is required',
  })
    .min(8, 'Password must be at least 8 characters')
    .max(72, 'Password too long (bcrypt limit)')
    .regex(
      /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]/,
      'Password must contain uppercase, lowercase, number and special character'
    ),

  name: z.string()
    .min(1, 'Name is required')
    .max(100, 'Name too long')
    .trim(),

  // Campos opcionais com defaults
  role: z.enum(['admin', 'editor', 'viewer']).default('viewer'),

  birthDate: z.string()
    .regex(/^\d{4}-\d{2}-\d{2}$/, 'Use YYYY-MM-DD format')
    .transform(val => new Date(val))
    .optional(),

  preferences: z.object({
    language: z.enum(['en', 'pt', 'es']).default('en'),
    notifications: z.boolean().default(true),
    timezone: z.string().max(50).optional(),
  }).optional().default({}),

  // Array com limites — previne payloads absurdamente grandes
  tags: z.array(
    z.string().min(1).max(50).regex(/^[a-z0-9-]+$/)
  ).max(10).optional().default([]),
})
// .strict() rejeita chaves desconhecidas — previne prototype pollution
// Use .strip() (default) para silenciosamente remover, .strict() para rejeitar
.strict();

// Tipo inferido — use em toda a camada de serviço
export type CreateUserInput = z.infer<typeof CreateUserSchema>;

// Schema de query params para listagem
export const ListUsersQuerySchema = z.object({
  page: z.preprocess(
    (val) => (typeof val === 'string' ? parseInt(val, 10) : val),
    z.number().int().min(1).default(1)
  ),
  limit: z.preprocess(
    (val) => (typeof val === 'string' ? parseInt(val, 10) : val),
    z.number().int().min(1).max(100).default(20)
  ),
  role: z.enum(['admin', 'editor', 'viewer']).optional(),
  search: z.string().max(100).optional().transform(val => val?.trim()),
  sortBy: z.enum(['name', 'email', 'createdAt']).default('createdAt'),
  order: z.enum(['asc', 'desc']).default('desc'),
});

export type ListUsersQuery = z.infer<typeof ListUsersQuerySchema>;
```

## Integração Zod com Express

O padrão mais robusto é uma **factory function** que recebe um schema e retorna um middleware Express reutilizável. Isso mantém as rotas limpas e centraliza o tratamento de erros de validação.

```typescript
import { Request, Response, NextFunction } from 'express';
import { z, ZodSchema, ZodError } from 'zod';

// Tipos auxiliares para rotas tipadas
type RequestWithBody<T> = Request & { body: T };
type RequestWithQuery<T> = Request & { query: T };

// Factory function — valida req.body
export function validateBody<T>(schema: ZodSchema<T>) {
  return (req: Request, res: Response, next: NextFunction): void => {
    const result = schema.safeParse(req.body);

    if (!result.success) {
      res.status(422).json({
        error: 'Validation failed',
        details: result.error.errors.map(err => ({
          field: err.path.join('.'),
          message: err.message,
          code: err.code,
        })),
      });
      return;
    }

    // Substitui req.body pelos dados validados e transformados
    req.body = result.data;
    next();
  };
}

// Factory function — valida req.query
export function validateQuery<T>(schema: ZodSchema<T>) {
  return (req: Request, res: Response, next: NextFunction): void => {
    const result = schema.safeParse(req.query);

    if (!result.success) {
      res.status(422).json({
        error: 'Invalid query parameters',
        details: result.error.errors.map(err => ({
          param: err.path.join('.'),
          message: err.message,
        })),
      });
      return;
    }

    // @ts-expect-error — sobrescreve query com valores tipados e transformados
    req.query = result.data;
    next();
  };
}

// Factory function — valida req.params
export function validateParams<T>(schema: ZodSchema<T>) {
  return (req: Request, res: Response, next: NextFunction): void => {
    const result = schema.safeParse(req.params);

    if (!result.success) {
      res.status(422).json({
        error: 'Invalid path parameters',
        details: result.error.errors.map(err => ({
          param: err.path.join('.'),
          message: err.message,
        })),
      });
      return;
    }

    req.params = result.data as Record<string, string>;
    next();
  };
}
```

Uso nas rotas — as rotas ficam limpas, toda validação é declarativa:

```typescript
import express from 'express';
import { validateBody, validateQuery, validateParams } from './middleware/validate';
import { CreateUserSchema, ListUsersQuerySchema } from './schemas/user';
import { z } from 'zod';

const router = express.Router();

const UserIdSchema = z.object({
  id: z.string().uuid('Invalid user ID format'),
});

// POST /users — valida body
router.post(
  '/',
  validateBody(CreateUserSchema),
  async (req, res) => {
    // req.body é tipado como CreateUserInput aqui
    const user = await userService.create(req.body);
    res.status(201).json(user);
  }
);

// GET /users — valida query params
router.get(
  '/',
  validateQuery(ListUsersQuerySchema),
  async (req, res) => {
    const users = await userService.list(req.query as any);
    res.json(users);
  }
);

// GET /users/:id — valida params de rota
router.get(
  '/:id',
  validateParams(UserIdSchema),
  async (req, res) => {
    const user = await userService.findById(req.params.id);
    if (!user) return res.status(404).json({ error: 'User not found' });
    res.json(user);
  }
);

export default router;
```

Registro do error handler global para `ZodError` não capturado (última linha de defesa):

```typescript
import express, { Request, Response, NextFunction } from 'express';
import { ZodError } from 'zod';

const app = express();
app.use(express.json());

// ... rotas

// Error handler global — captura ZodError que escapou de alguma rota
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  if (err instanceof ZodError) {
    return res.status(422).json({
      error: 'Validation error',
      details: err.errors,
    });
  }
  // Outros erros — não vazar stack trace em produção
  const statusCode = (err as any).statusCode ?? 500;
  res.status(statusCode).json({
    error: process.env.NODE_ENV === 'production' ? 'Internal Server Error' : err.message,
  });
});
```

## Integração Zod com Fastify

Fastify tem suporte nativo a JSON Schema para validação, mas também aceita Zod via plugin `@fastify/type-provider-zod` ou via hook `preHandler` manual.

```typescript
import Fastify from 'fastify';
import {
  serializerCompiler,
  validatorCompiler,
  ZodTypeProvider,
} from '@fastify/type-provider-zod';
import { z } from 'zod';

const app = Fastify({ logger: true });

// Configura Fastify para usar Zod como engine de validação e serialização
app.setValidatorCompiler(validatorCompiler);
app.setSerializerCompiler(serializerCompiler);

// Rota com schema tipado via ZodTypeProvider
app.withTypeProvider<ZodTypeProvider>().post(
  '/users',
  {
    schema: {
      body: z.object({
        email: z.string().email().max(254),
        name: z.string().min(1).max(100),
        role: z.enum(['admin', 'editor', 'viewer']).default('viewer'),
      }),
      response: {
        201: z.object({
          id: z.string().uuid(),
          email: z.string(),
          name: z.string(),
          role: z.string(),
          createdAt: z.string().datetime(),
        }),
      },
    },
  },
  async (request, reply) => {
    // request.body é totalmente tipado pelo Zod schema
    const { email, name, role } = request.body;
    const user = await userService.create({ email, name, role });
    reply.status(201).send(user);
  }
);

// Alternativa: validação manual no hook preHandler (sem plugin)
app.post('/products', {
  preHandler: async (request, reply) => {
    const ProductSchema = z.object({
      name: z.string().min(1).max(200),
      price: z.number().positive(),
    });

    const result = ProductSchema.safeParse(request.body);
    if (!result.success) {
      reply.code(422).send({
        error: 'Validation failed',
        details: result.error.errors,
      });
    } else {
      request.body = result.data; // substitui com dados validados
    }
  },
}, async (request, reply) => {
  reply.send({ ok: true });
});
```

### Integração com NestJS

NestJS não tem suporte nativo a Zod, mas integra via `PipeTransform` — a interface do framework para transformação e validação de valores antes de chegarem ao handler. A abordagem manual cria um `ValidationPipe` reutilizável que recebe qualquer `ZodSchema` no construtor:

```typescript
import { z, ZodTypeAny } from 'zod'
import { PipeTransform, Injectable, BadRequestException } from '@nestjs/common'

@Injectable()
export class ZodValidationPipe implements PipeTransform {
  constructor(private schema: ZodTypeAny) {}

  transform(value: unknown) {
    const result = this.schema.safeParse(value)
    if (!result.success) {
      throw new BadRequestException(result.error.format())
    }
    return result.data
  }
}
```

Uso no controller via `@UsePipes`, passando uma instância com o schema específico da rota:

```typescript
import { Body, Controller, Post, UsePipes } from '@nestjs/common'
import { z } from 'zod'
import { ZodValidationPipe } from './zod-validation.pipe'

const CreateUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(2).max(100),
})

type CreateUserDto = z.infer<typeof CreateUserSchema>

@Controller('users')
export class UsersController {
  @Post()
  @UsePipes(new ZodValidationPipe(CreateUserSchema))
  create(@Body() body: CreateUserDto) {
    return { message: 'User created', data: body }
  }
}
```

O pacote `nestjs-zod` é uma alternativa que adiciona decoradores (`@ZodBody()`, `@ZodParam()`) e auto-wiring do pipe globalmente, eliminando o `@UsePipes` por rota.

## Joi v17

Joi é a biblioteca de validação histórica do ecossistema Node.js, criada pelo time do framework hapi. Amplamente usada em codebases legados e projetos JavaScript puro onde inferência TypeScript não é prioridade.

```javascript
import Joi from 'joi';

// Definição de schema — API encadeada orientada a objetos
const CreateUserSchema = Joi.object({
  email: Joi.string().email({ tlds: { allow: false } }).max(254).required(),
  password: Joi.string().min(8).max(72).required(),
  name: Joi.string().min(1).max(100).trim().required(),
  role: Joi.string().valid('admin', 'editor', 'viewer').default('viewer'),
  tags: Joi.array().items(Joi.string().alphanum().max(50)).max(10).default([]),
}).options({ stripUnknown: true }); // remove campos desconhecidos

// Validação — retorna { error, value }
const { error, value } = CreateUserSchema.validate(req.body, {
  abortEarly: false,   // coleta TODOS os erros, não só o primeiro
  stripUnknown: true,  // remove campos não definidos no schema
  convert: true,       // converte tipos (string → number) quando possível
});

if (error) {
  return res.status(422).json({
    error: 'Validation failed',
    details: error.details.map(d => ({
      field: d.path.join('.'),
      message: d.message,
    })),
  });
}

// value contém os dados validados, transformados e com defaults aplicados
await userService.create(value);
```

### Joi vs Zod — quando usar cada

| Critério | Zod | Joi |
|---|---|---|
| TypeScript inference | Automática via `z.infer<>` | Manual (tipos separados do schema) |
| Bundle size | ~13 KB minzipped | ~25 KB minzipped |
| API style | Schema-first, funcional | Encadeada, OO |
| Codebase legado JS | Funciona, mas perde vantagem | Histórico mais amplo |
| Ecossistema moderno | tRPC, Fastify, React Hook Form | Hapi, projetos > 5 anos |
| Coerção de tipos | Explícita (`z.coerce`, `preprocess`) | Implícita (opção `convert: true`) |

**Regra de decisão:** Novo projeto TypeScript → Zod. Projeto existente com Joi → não migre sem necessidade clara; os dois têm parity de features.

## Sanitização vs Validação

Validação e sanitização são controles complementares, não intercambiáveis:

**Validação** — verifica se o input está no formato esperado e **rejeita** o que não está. É um portão: passa ou não passa. Não altera o dado.

**Sanitização** — **transforma** o input para uma forma segura para processamento ou exibição. Não rejeita — converte.

```typescript
import { z } from 'zod';
import xss from 'xss';
import DOMPurify from 'isomorphic-dompurify';

// Validação pura — rejeita se não for email válido
const EmailSchema = z.string().email().max(254);

// Sanitização — transforma HTML potencialmente perigoso em HTML seguro
// Necessário para campos de rich text (WYSIWYG editors)
function sanitizeHtml(input: string): string {
  return DOMPurify.sanitize(input, {
    ALLOWED_TAGS: ['p', 'br', 'strong', 'em', 'ul', 'ol', 'li', 'a'],
    ALLOWED_ATTR: ['href', 'title'],
    FORBID_SCRIPTS: true,
  });
}

// Para campos de texto simples (sem HTML) — xss é mais direto
function sanitizeText(input: string): string {
  return xss(input, { whiteList: {} }); // remove TODA tag HTML
}

// Em uma rota de criação de post com rich text
app.post('/posts', async (req, res) => {
  // Etapa 1: validar estrutura e tipos
  const ValidPostSchema = z.object({
    title: z.string().min(1).max(200),
    body: z.string().min(1).max(50_000), // rich text — comprimento, não formato HTML
    excerpt: z.string().max(500).optional(),
  });

  const result = ValidPostSchema.safeParse(req.body);
  if (!result.success) return res.status(422).json({ error: result.error.errors });

  // Etapa 2: sanitizar o campo de rich text antes de armazenar
  const sanitizedPost = {
    ...result.data,
    body: sanitizeHtml(result.data.body),       // DOMPurify para rich text
    excerpt: result.data.excerpt
      ? sanitizeText(result.data.excerpt)        // xss para texto simples
      : undefined,
  };

  await postService.create(sanitizedPost);
  res.status(201).json({ ok: true });
});
```

**Quando sanitizar server-side:**
- Campos que aceitam HTML de editores WYSIWYG (Quill, TipTap, CKEditor) armazenado no banco
- Campos que serão renderizados como HTML em emails transacionais
- Campos de comentário/bio que podem conter markdown interpretado

**Não confunda:** Escapar output (ex: `{{ variable | escape }}` em templates) é uma terceira técnica — proteção na camada de apresentação, não na entrada.

## Validação de env vars com Zod

A mesma abordagem schema-first se aplica à configuração da aplicação. Zod valida `process.env` na startup e tipifica todo o módulo de config — eliminando erros de configuração silenciosos e providenciando tipos corretos em todo o código.

```typescript
import { z } from 'zod';

// Schema de configuração — todas as env vars da aplicação
const EnvSchema = z.object({
  // Servidor
  NODE_ENV: z.enum(['development', 'test', 'production']).default('development'),
  PORT: z.preprocess(
    (val) => (typeof val === 'string' ? parseInt(val, 10) : val),
    z.number().int().min(1).max(65535).default(3000)
  ),
  HOST: z.string().default('0.0.0.0'),

  // Banco de dados
  DATABASE_URL: z.string().url('DATABASE_URL must be a valid URL'),

  // Autenticação
  JWT_SECRET: z.string().min(32, 'JWT_SECRET must be at least 32 characters'),
  JWT_EXPIRES_IN: z.string().regex(/^\d+[smhd]$/, 'Use format: 30s, 15m, 1h, 7d').default('15m'),
  REFRESH_TOKEN_SECRET: z.string().min(32),
  REFRESH_TOKEN_EXPIRES_IN: z.string().default('7d'),

  // Redis (opcional em desenvolvimento)
  REDIS_URL: z.string().url().optional(),

  // Externos
  SMTP_HOST: z.string().optional(),
  SMTP_PORT: z.preprocess(
    (val) => val !== undefined ? parseInt(String(val), 10) : val,
    z.number().int().min(1).max(65535).optional()
  ),
  STRIPE_SECRET_KEY: z.string().startsWith('sk_').optional(),
  SENTRY_DSN: z.string().url().optional(),
});

// parse lança ZodError se inválido — fail-fast na startup
// A aplicação não sobe com configuração incompleta
let env: z.infer<typeof EnvSchema>;
try {
  env = EnvSchema.parse(process.env);
} catch (err) {
  if (err instanceof z.ZodError) {
    console.error('❌ Invalid environment configuration:');
    err.errors.forEach(e => {
      console.error(`  ${e.path.join('.')}: ${e.message}`);
    });
    process.exit(1);
  }
  throw err;
}

export { env };

// Uso em qualquer módulo — totalmente tipado
import { env } from './config/env';
// env.PORT é number, env.NODE_ENV é 'development' | 'test' | 'production'
// env.REDIS_URL é string | undefined
```

## Armadilhas

> [!danger] Validar tipo sem limitar tamanho — vetor de ReDoS e DoS
> **Problema:** `z.string()` sem `.max()` aceita strings de qualquer tamanho. Um campo de email com regex de validação complexa e entrada de 10 MB pode travar o event loop Node.js por segundos — Denial of Service efetivo em produção. Além disso, strings ilimitadas chegam ao banco sem controle de tamanho de coluna.
> **Solução:** Sempre adicionar `.max()` em todo campo string. Use os limites do domínio: email → `.max(254)` (RFC 5321), nome → `.max(100)`, texto livre → `.max(5000)`, password → `.max(72)` (limite do bcrypt). Para arrays, `.max(N)` também é obrigatório para prevenir payloads absurdamente grandes.

> [!danger] Confiar em validação do cliente — frontend validation is not security
> **Problema:** Validação no frontend (React, Angular, formulários HTML) é UX, não segurança. Qualquer pessoa com `curl` ou Postman pode bypassar toda validação do browser e enviar payloads arbitrários diretamente para a API. APIs que validam apenas no cliente aceitam SQL injection, NoSQL injection e prototype pollution via ferramentas como Burp Suite ou scripts simples.
> **Solução:** Toda validação de segurança acontece obrigatoriamente no servidor, na borda da API (middleware). Validação do cliente é duplicada deliberada para melhorar UX — não substitui a validação server-side em hipótese alguma.

> [!danger] Usar parse sem try/catch em rotas Express
> **Problema:** `Schema.parse(req.body)` lança `ZodError` se inválido. Sem `try/catch`, o erro borbulha até o error handler padrão do Express — que retorna HTTP 500 com stack trace vazio. O cliente recebe um erro genérico sem informação sobre o que estava errado, e o log do servidor registra um erro 500 que na verdade é um problema de input do cliente (4xx).
> **Solução:** Em rotas e middlewares de API, sempre use `safeParse` — que nunca lança e retorna um resultado discriminado `{ success: true, data } | { success: false, error }`. Use `parse` apenas em contextos onde a exceção é intencionalmente fatal (startup, testes).

## Em entrevista

**Q: How do you prevent injection attacks in a Node.js API?**
A: The primary defense is input validation at the system boundary — every external input goes through a schema validator like Zod before reaching any business logic or database layer. Zod with `.strict()` rejects unknown keys, preventing prototype pollution via `__proto__` in JSON bodies. For NoSQL injection specifically, if MongoDB receives `{ password: { "$ne": null } }` as a query operator, it bypasses password checks — schema validation rejects that because the field is defined as `z.string()`, not an object. For SQL, parameterized queries via `pg` or an ORM handle escaping, but schema validation ensures only expected fields reach the query builder. Defense in depth: validate at the API layer, use parameterized queries at the DB layer, apply principle of least privilege at the auth layer.

**Q: What's the difference between validation and sanitization?**
A: Validation is a gate — it checks whether input conforms to the expected schema and rejects non-conforming data with an error. It doesn't modify the data. Sanitization is a transformation — it takes potentially dangerous input and converts it to a safe form. Both are necessary for different scenarios. For structured data like API request bodies — user IDs, email addresses, enums — validation via Zod is sufficient and correct: invalid input should be rejected, not silently transformed. For rich text fields from WYSIWYG editors, sanitization with DOMPurify is necessary: the input is legitimately HTML, but you need to strip `<script>` tags, `javascript:` href values, and event handlers before storing or rendering. The common mistake is applying sanitization where rejection is correct — it can silently swallow legitimate errors and leave the system in an unexpected state.

**Q: Why is Zod preferred over Joi in new TypeScript projects?**
A: The decisive advantage is static type inference. With Zod, you define the schema once and derive the TypeScript type via `z.infer<typeof Schema>` — the runtime validation and the compile-time type are guaranteed to be in sync because they come from the same source of truth. With Joi, you define the schema and separately declare a TypeScript interface — they can drift apart silently. If you add a required field to the Joi schema but forget to update the interface, TypeScript won't catch it, but at runtime the validated object has the field. Additionally, Zod has zero dependencies, a smaller bundle (~13 KB vs ~25 KB), and integrates natively with the modern TypeScript ecosystem — tRPC, React Hook Form, and Fastify's type provider all have first-class Zod support. Joi remains the right choice for large existing Node.js codebases where Zod's TypeScript advantages don't justify a migration.

**Q: How do you handle validation errors consistently across an Express API?**
A: The pattern I use is a `validateBody(schema)` factory function that returns a middleware. The middleware calls `schema.safeParse(req.body)` — which never throws — and if validation fails, immediately returns HTTP 422 Unprocessable Entity with a structured error body listing each field and its error message. HTTP 422 is semantically correct: the request was well-formed (200 is JSON), but the server cannot process the instructions — distinct from 400 (malformed syntax) and 500 (server fault). I also register a global error handler as a safety net that catches any `ZodError` that escaped a route and maps it to 422 — preventing a validation error from appearing as a 500 in metrics and alerting dashboards.

## Vocabulário

- **schema validation** — técnica de validar dados contra um contrato estrutural declarativo (schema) que define tipos, formatos e restrições; a conformidade é verificada em runtime
- **sanitization** — transformação de input potencialmente perigoso em uma forma segura para processamento ou renderização; distinto de validação, que rejeita — sanitização transforma
- **parse** — método Zod que valida e transforma um valor, lançando `ZodError` se inválido; use onde falha fatal é desejada (startup, testes)
- **safeParse** — método Zod que retorna `{ success: true, data }` ou `{ success: false, error }` sem lançar exceção; use em middleware de API para controlar o response de erro
- **type coercion** — conversão automática ou explícita de um valor de um tipo para outro (ex: string `"5"` → number `5`); Zod expõe coerção via `z.coerce.*` e `z.preprocess()`, mantendo-a explícita e auditável
- **ReDoS** (Regular Expression Denial of Service) — ataque que explora backtracking catastrófico em expressões regulares com strings longas cuidadosamente construídas, travando o event loop single-threaded do Node.js; mitigado com `.max()` nos campos string antes da validação por regex
- **prototype pollution** — vetor de ataque em que propriedades como `__proto__` ou `constructor` em JSON body corrompem o prototype chain de objetos JavaScript, afetando toda a aplicação; bloqueado por schema validation com `.strict()` ou descarte de chaves desconhecidas
- **fail-fast** — princípio de interromper imediatamente a execução ao detectar condição inválida, em vez de continuar com estado inconsistente; aplicado na validação de env vars com `parse()` na startup: a aplicação recusa subir se a configuração estiver incompleta
- **HTTP 422 Unprocessable Entity** — código de status HTTP correto para erros de validação de negócio: a sintaxe da requisição está correta (não é 400), mas o servidor não pode processar as instruções contidas no payload
- **discriminated union** — tipo TypeScript (e padrão de retorno do `safeParse`) onde um campo discriminador (`success: true/false`) determina o shape do objeto; permite narrowing de tipo seguro sem type assertions

## Veja também

- [[03-Dominios/Node/Segurança/index|Segurança]] — MOC do galho 8, visão geral de todos os tópicos de segurança Node
- [[JavaScript/Backend/Node.js|Node.js]] — tronco da trilha Node Senior
- [[03-Dominios/Node/Segurança/02 - Segredos e variáveis de ambiente|Segredos e variáveis de ambiente]] — validação de env vars com Zod na startup
- [[03-Dominios/Node/Segurança/04 - JWT e autenticação com jsonwebtoken|JWT e autenticação]] — próxima nota do galho
- [Zod — documentação oficial](https://zod.dev) — referência completa da API Zod v3
- [Joi — documentação oficial](https://joi.dev) — referência da API Joi v17
- [OWASP Input Validation Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html) — guia OWASP sobre validação de entrada
