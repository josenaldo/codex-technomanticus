---
title: "Cheatsheet e decision tree de segurança"
created: 2026-05-12
updated: 2026-05-12
type: concept
status: growing
publish: true
tags:
  - node
  - segurança
  - cheatsheet
aliases:
  - Security Decision Tree Node
  - Cheatsheet Segurança Node
---

# Cheatsheet e decision tree de segurança

> [!abstract] TL;DR
> Referência consolidada de decisões de segurança para Node.js senior. O galho 8 cobre 9 áreas críticas: supply chain (npm audit + socket.dev), segredos (vault, env validation com Zod), validação de entrada (Zod vs Joi), JWT (jsonwebtoken, refresh token rotation, Redis blacklist), OAuth 2.0/OIDC (openid-client, PKCE), autorização (casl ABAC vs casbin policies), rate limiting (express-rate-limit + Redis), HTTP headers (Helmet.js) e OWASP Top 10 (A01–A10 com exemplos Node). Use este cheatsheet como ponto de entrada rápido e decision tree para escolher a ferramenta certa para cada categoria de segurança.

## O que é

Este cheatsheet consolida os padrões, ferramentas e decisões de segurança das 9 notas do galho 8 da trilha Node Senior. Não é um resumo superficial — é um mapa de decisão para situações reais: qual biblioteca escolher, qual padrão aplicar, o que checar em um PR de segurança.

**Quando usar este cheatsheet:**
- Início de projeto: escolher o stack de segurança correto
- Code review: validar que as decisões de segurança estão corretas
- Entrevista: responder perguntas transversais sobre segurança Node.js senior
- Incidente: identificar rapidamente qual área pode ter falhado

## Como funciona

### Decision tree — escolha a ferramenta certa

```mermaid
flowchart TD
    A[Precisa de segurança em Node.js] --> B{Qual área?}

    B --> C[Validação de entrada]
    B --> D[Autenticação]
    B --> E[Autorização]
    B --> F[Proteção de API]
    B --> G[Supply chain]
    B --> H[Segredos]
    B --> I[HTTP Headers]

    C --> C1{TypeScript?}
    C1 -->|Sim| C2[Zod v3\nsafeParse + infer]
    C1 -->|Legado JS| C3[Joi v17\nschema object-based]

    D --> D1{OAuth/OIDC externo?}
    D1 -->|Sim| D2[openid-client v5\nIssuer.discover + PKCE]
    D1 -->|JWT próprio| D3[jsonwebtoken v9\nHS256 ou RS256]
    D3 --> D4[Access + Refresh tokens\nBlacklist no Redis]

    E --> E1{Regras baseadas em atributos?}
    E1 -->|Sim, TypeScript| E2[casl v6\ndefineAbility + can/cannot]
    E1 -->|Políticas externas| E3[casbin\npolicy files + enforce]
    E1 -->|RBAC simples| E4[Claims no JWT\ncheckRole middleware]

    F --> F1[express-rate-limit v7\n+ rate-limit-redis\nstore Redis para múltiplas instâncias]

    G --> G1[npm audit\n+ npm ci no CI\n+ socket.dev ou snyk]

    H --> H1{Produção?}
    H1 -->|Sim| H2[AWS Secrets Manager\nHashiCorp Vault\nDoppler]
    H1 -->|Dev| H3[.env local\nnode --env-file=.env\nValidar com Zod na inicialização]

    I --> I1[Helmet v7\napp.use(helmet())\nCSP com nonce para scripts inline]
```

### Tabela comparativa por categoria

| Categoria | Biblioteca principal | Quando usar | Alternativa |
|---|---|---|---|
| Validação de entrada | Zod v3 | TypeScript, schema-first, infer de tipos | Joi v17 (legado JS) |
| Autenticação JWT | jsonwebtoken v9 | JWT próprio, stateless, microservices | `@fastify/jwt` para Fastify |
| OAuth 2.0 / OIDC | openid-client v5 | Login social, SSO enterprise, Authorization Code + PKCE | passport-oauth2 (flows simples) |
| Autorização | casl v6 | ABAC TypeScript, permissões condicionais, NestJS | casbin (policies em arquivo) |
| HTTP Headers | Helmet v7 | Qualquer app Express — padrão obrigatório | `@fastify/helmet` para Fastify |
| Rate Limiting | express-rate-limit v7 | Auth endpoints, APIs públicas | `@fastify/rate-limit` para Fastify |
| Supply chain | npm audit + socket.dev | CI/CD pipeline, pre-merge check | Snyk, Dependabot (GitHub) |
| Segredos em prod | AWS Secrets Manager / Vault | Rotação automática, auditoria de acesso | GCP Secret Manager, Doppler |

### Checklist de segurança para PR review

Use este checklist em code reviews que tocam lógica de negócio ou infra:

```
## Security Review

### Validação e sanitização
- [ ] Input externo validado com Zod/Joi na borda do sistema (controller/route handler)
- [ ] Nenhum `req.body` ou `req.query` passado diretamente para query de banco ou sistema de arquivos
- [ ] Tamanho máximo de strings e arrays definido no schema (previne ReDoS e DoS)

### Segredos
- [ ] Nenhum segredo hardcoded no código (API keys, passwords, tokens)
- [ ] Nenhum `.env` de produção no repositório
- [ ] Env vars validadas com Zod na inicialização — app falha rápido se variável estiver ausente

### Autenticação e sessão
- [ ] `jwt.verify()` chamado com `{ algorithms: ['HS256'] }` explícito (previne algorithm confusion)
- [ ] Refresh tokens com rotação (revoga o anterior ao emitir o novo)
- [ ] Mensagens de erro de auth genéricas (não vazar se email existe ou não)

### Autorização
- [ ] Verificação de ownership feita server-side, não apenas no frontend
- [ ] Usuário pode acessar apenas seus próprios recursos (BOLA/IDOR check)
- [ ] Logs de decisões de autorização negadas registrados (auditoria)

### HTTP e headers
- [ ] `helmet()` aplicado globalmente antes das rotas
- [ ] CSP configurada — sem `'unsafe-inline'` nos scripts (exceto se usando nonces)
- [ ] CORS allowlist explícita, não `*` com `credentials: true`

### Rate limiting
- [ ] Rate limiting aplicado em endpoints de autenticação (login, reset de senha)
- [ ] Store Redis configurado (não memória) em ambientes com múltiplas instâncias

### Supply chain
- [ ] `npm audit` sem vulnerabilidades high/critical
- [ ] `package-lock.json` ou `pnpm-lock.yaml` commitado e usado com `npm ci` no CI

### Logging
- [ ] Dados sensíveis redactados nos logs (senha, token, CPF, cartão)
- [ ] Stack traces não expostos em respostas de API em produção
- [ ] Eventos de autenticação (login, logout, falhas) logados com user_id e IP
```

### Padrões de resposta de erro segura

Erros mal formatados são um vetor de information disclosure. O padrão correto é genérico para o cliente e detalhado internamente.

```typescript
import express, { Request, Response, NextFunction } from 'express'

interface AppError extends Error {
  statusCode?: number
  code?: string
  isOperational?: boolean
}

// Formato de erro público — sem detalhes internos
interface ErrorResponse {
  error: {
    code: string
    message: string
  }
}

function errorHandler(
  err: AppError,
  req: Request,
  res: Response,
  _next: NextFunction,
): void {
  // Log completo interno (stack trace, contexto)
  console.error({
    message: err.message,
    stack: err.stack,
    path: req.path,
    method: req.method,
    ip: req.ip,
  })

  // Resposta pública: sem stack trace, mensagem genérica para erros não operacionais
  const statusCode = err.statusCode ?? 500
  const isOperational = err.isOperational ?? false

  const response: ErrorResponse = {
    error: {
      code: err.code ?? 'INTERNAL_ERROR',
      // Erros não operacionais (bugs) → mensagem genérica
      // Erros operacionais (validação, negócio) → mensagem da aplicação
      message: isOperational ? err.message : 'An unexpected error occurred',
    },
  }

  res.status(statusCode).json(response)
}

// Erros de autenticação: sempre genérico — não vazar se email existe
function authErrorResponse(res: Response): void {
  // 401 correto para auth failure (não 400 — isso vaza informação de que o email existe)
  res.status(401).json({
    error: {
      code: 'AUTH_FAILED',
      message: 'Invalid credentials',
    },
  })
}

// 401 vs 403: regra clara
// 401 Unauthorized → não autenticado (sem token ou token inválido)
// 403 Forbidden     → autenticado mas sem permissão para o recurso
function authorizationErrorResponse(res: Response, isAuthenticated: boolean): void {
  if (!isAuthenticated) {
    res.status(401).json({ error: { code: 'UNAUTHENTICATED', message: 'Authentication required' } })
  } else {
    res.status(403).json({ error: { code: 'FORBIDDEN', message: 'You do not have permission to access this resource' } })
  }
}

export { errorHandler, authErrorResponse, authorizationErrorResponse }
```

### Bootstrap seguro da aplicação

Configuração mínima de segurança para uma aplicação Express em produção:

```typescript
import express from 'express'
import helmet from 'helmet'
import rateLimit from 'express-rate-limit'
import { z } from 'zod'
import crypto from 'node:crypto'

// 1. Validar env vars na inicialização — falha rápido se algo estiver ausente
const EnvSchema = z.object({
  NODE_ENV: z.enum(['development', 'test', 'production']),
  JWT_SECRET: z.string().min(32, 'JWT_SECRET must be at least 32 characters'),
  DATABASE_URL: z.string().url(),
  REDIS_URL: z.string().url(),
  PORT: z.coerce.number().default(3000),
  ALLOWED_ORIGINS: z.string().transform((val) => val.split(',')),
})

const env = EnvSchema.parse(process.env)

const app = express()

// 2. Helmet — headers de segurança HTTP (antes de qualquer rota)
app.use(
  helmet({
    contentSecurityPolicy: {
      directives: {
        defaultSrc: ["'self'"],
        scriptSrc: ["'self'", (_req, res) => `'nonce-${(res as any).locals.nonce}'`],
        styleSrc: ["'self'", "'unsafe-inline'"],
        imgSrc: ["'self'", 'data:', 'https:'],
      },
    },
  }),
)

// Gerar nonce por request (para CSP com scripts inline)
app.use((_req, res, next) => {
  res.locals.nonce = crypto.randomBytes(16).toString('base64')
  next()
})

// 3. CORS com allowlist explícita
app.use((_req, res, next) => {
  const origin = _req.headers.origin
  if (origin && env.ALLOWED_ORIGINS.includes(origin)) {
    res.setHeader('Access-Control-Allow-Origin', origin)
    res.setHeader('Access-Control-Allow-Credentials', 'true')
    res.setHeader('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  }
  if (_req.method === 'OPTIONS') {
    res.sendStatus(204)
    return
  }
  next()
})

// 4. Rate limiting global
const globalLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  limit: 100,
  standardHeaders: 'draft-7',
  legacyHeaders: false,
})
app.use(globalLimiter)

// 5. Rate limiting restrito para auth endpoints
const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  limit: 10,
  message: { error: { code: 'RATE_LIMIT_EXCEEDED', message: 'Too many authentication attempts' } },
  standardHeaders: 'draft-7',
  legacyHeaders: false,
})
app.use('/auth', authLimiter)

// 6. Body parsing com limite de tamanho
app.use(express.json({ limit: '10kb' }))

export { app, env }
```

### JWT verify com proteção contra algorithm confusion

```typescript
import jwt from 'jsonwebtoken'
import { z } from 'zod'

const JwtPayloadSchema = z.object({
  sub: z.string(),
  email: z.string().email(),
  role: z.enum(['admin', 'user', 'moderator']),
  iat: z.number(),
  exp: z.number(),
})

type JwtPayload = z.infer<typeof JwtPayloadSchema>

function verifyAccessToken(token: string, secret: string): JwtPayload {
  // Sempre passar algorithms explicitamente — previne algorithm confusion attack
  // Se omitir, um atacante pode forjar token com alg: "none" ou trocar HS256 por RS256
  const raw = jwt.verify(token, secret, { algorithms: ['HS256'] })

  // Validar estrutura do payload com Zod — jwt.verify não valida claims customizados
  const result = JwtPayloadSchema.safeParse(raw)
  if (!result.success) {
    throw new Error('Invalid token payload structure')
  }

  return result.data
}

export { verifyAccessToken, JwtPayload }
```

## Armadilhas

> [!danger] Erros de auth com mensagem específica vazam informação
> Retornar `"User not found"` vs `"Wrong password"` permite a um atacante confirmar quais emails estão cadastrados (user enumeration attack). A mitigação é sempre retornar a mesma mensagem genérica: `"Invalid credentials"` — e tomar o mesmo tempo para processar ambos os casos (comparação de hash mesmo quando o usuário não existe, usando `bcrypt.compare` com um hash fake para evitar timing attack).

> [!danger] jwt.verify sem algorithms abre brecha de algorithm confusion
> `jwt.verify(token, secret)` sem `{ algorithms: ['HS256'] }` aceita qualquer algoritmo declarado no header do token, incluindo `"none"`. Um atacante pode criar um token sem assinatura com `alg: "none"` e bypassar a verificação. Sempre passe o array de algoritmos aceitos explicitamente.

> [!danger] Rate limiting em memória não funciona em múltiplas instâncias
> O store padrão do `express-rate-limit` é em memória (por processo). Em um cluster com 4 workers ou 3 pods Kubernetes, cada instância tem seu próprio contador — o limite efetivo é multiplicado pelo número de instâncias. Use `rate-limit-redis` com um store Redis compartilhado para garantir que o limite seja global.

## Em entrevista

**Q: How would you secure a Node.js REST API end-to-end?**

A: I'd think of security in layers. At the network layer, HTTPS everywhere and a reverse proxy handling TLS termination. At the HTTP layer, Helmet.js for security headers — CSP, HSTS, X-Frame-Options — and rate limiting on all endpoints, stricter on authentication. At the application boundary, all external input validated with Zod before touching any business logic. For authentication, JWTs with short expiry signed with HS256 or RS256 (never `alg: none`), plus a refresh token rotation pattern with a Redis blacklist. Authorization is checked server-side on every request — ownership verification for resource access to prevent BOLA/IDOR. Secrets never in code, only from environment variables validated at startup, pulled from AWS Secrets Manager or Vault in production. And supply chain: `npm ci` in CI, `npm audit` as a pipeline gate, socket.dev for real-time package threat analysis.

**Q: What's the difference between authentication and authorization, and how do you implement both in Node.js?**

A: Authentication answers "who are you?" — verifying identity. Authorization answers "what are you allowed to do?" — verifying permissions. They must always happen in that order, and on the server side. In Node.js, authentication typically means validating a JWT with `jsonwebtoken`'s `verify()` using an explicit algorithms array, or running an OIDC flow with `openid-client`. Authorization for simple role-based rules can live in JWT claims with a `checkRole` middleware, but for anything conditional — like "users can only edit their own posts" — I use `casl`, which lets me express `can('update', 'Post', { authorId: user.id })` and check it against the actual resource. The key mistake is checking authorization only in the frontend, or forgetting to verify ownership when the user provides a resource ID in the URL.

**Q: How do you prevent OWASP A01 Broken Access Control in a Node.js API?**

A: A01 is consistently the top OWASP risk because it's easy to miss. The main patterns I protect against are BOLA (Broken Object Level Authorization) — where a user accesses another user's resource by changing an ID in the URL — and privilege escalation. For BOLA, the rule is: never trust IDs from the request alone. Always verify ownership server-side: `WHERE id = ? AND owner_id = ?`. For privilege escalation, I never let users set their own role via API, and I check the role from the JWT, not from the database row the user controls. In code reviews I specifically look for routes that accept a resource ID without verifying it belongs to the authenticated user — that pattern appears constantly in CRUD APIs.

**Q: How do you handle secrets in a Node.js production environment?**

A: The principles are: secrets never in source code, never in environment variables baked into Docker images, and rotatable without downtime. In production I pull secrets from AWS Secrets Manager or HashiCorp Vault at startup, using the SDK — the app crashes fast if a required secret is missing, which is better than running with a wrong configuration. I validate all environment variables with a Zod schema at boot: `EnvSchema.parse(process.env)`. For rotation, the pattern is to support two valid versions of a secret simultaneously during the rotation window — issue new JWTs signed with the new key, keep accepting old ones until they expire. No manual secret rotation that requires a deployment.

## Vocabulário

- **Supply chain attack**: ataque que compromete uma dependência (pacote npm, build tool, CI pipeline) em vez de atacar diretamente a aplicação
- **BOLA (Broken Object Level Authorization)**: vulnerabilidade onde um usuário acessa recursos de outro usuário alterando um ID na requisição; sinônimo de IDOR (Insecure Direct Object Reference)
- **Algorithm confusion**: ataque JWT onde o atacante altera o campo `alg` do header para `none` ou troca RS256 por HS256, bypassando verificação de assinatura quando `algorithms` não é passado explicitamente ao `verify()`
- **SSRF (Server-Side Request Forgery)**: vulnerabilidade onde o servidor realiza requisições HTTP a destinos controlados pelo atacante — pode expor metadados de cloud (169.254.169.254) ou serviços internos
- **CSP (Content Security Policy)**: header HTTP que instrui o browser sobre quais origens de scripts, estilos e recursos são permitidas — principal defesa contra XSS
- **HSTS (HTTP Strict Transport Security)**: header que instrui o browser a sempre usar HTTPS para o domínio pelo período definido em `maxAge`, impedindo downgrade para HTTP
- **Rate limiting**: mecanismo que limita o número de requisições de uma origem em uma janela de tempo — protege contra brute force, DoS e abuso de API
- **Input validation**: verificação que dados externos (req.body, req.query, req.params) obedecem o schema esperado antes de qualquer processamento — primeira linha de defesa contra injection
- **Least privilege**: princípio de segurança onde um usuário, serviço ou processo recebe apenas as permissões mínimas necessárias para sua função
- **Secret rotation**: processo de substituição periódica de segredos (API keys, JWT secrets, DB passwords) sem downtime — requer suporte a múltiplas versões válidas durante a transição
- **CVE (Common Vulnerabilities and Exposures)**: identificador único para vulnerabilidades de segurança conhecidas; reportado por `npm audit`
- **Timing attack**: ataque que mede diferenças de tempo de resposta para inferir informação — e.g., comparar strings com `===` em vez de `crypto.timingSafeEqual` vaza se o hash começou a divergir

## Veja também

- [[03-Dominios/Node/Segurança/index|Segurança]] — MOC do galho 8
- [[03-Dominios/Node/Segurança/01 - Supply chain attacks e npm audit]] — npm audit, socket.dev, lockfile integrity
- [[03-Dominios/Node/Segurança/02 - Segredos e variáveis de ambiente]] — vault, env validation, rotação de segredos
- [[03-Dominios/Node/Segurança/03 - Validação de entrada com Zod e Joi]] — Zod v3, Joi v17, middleware de validação
- [[03-Dominios/Node/Segurança/04 - JWT e autenticação com jsonwebtoken]] — sign/verify, access+refresh, blacklist Redis
- [[03-Dominios/Node/Segurança/05 - OAuth 2.0 e OIDC com openid-client]] — Authorization Code + PKCE, ID Token, openid-client v5
- [[03-Dominios/Node/Segurança/06 - RBAC e ABAC com casl e casbin]] — defineAbility, can/cannot, casbin policies
- [[03-Dominios/Node/Segurança/07 - Rate limiting com express-rate-limit]] — express-rate-limit v7, Redis store, algoritmos
- [[03-Dominios/Node/Segurança/08 - Helmet.js e hardening HTTP]] — CSP com nonce, HSTS, CORS allowlist
- [[03-Dominios/Node/Segurança/09 - OWASP Top 10 para Node]] — A01–A10 com exemplos Node e mitigações
- [[03-Dominios/Node/index|Node.js (MOC central)]] — visão geral de todos os galhos da trilha
- [[JavaScript/Backend/Node.js|Node.js]] — tronco da trilha Node Senior
