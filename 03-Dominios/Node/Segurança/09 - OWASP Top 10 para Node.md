---
title: "OWASP Top 10 para Node"
created: 2026-05-12
updated: 2026-05-12
type: concept
status: growing
publish: true
tags:
  - node
  - segurança
  - owasp
aliases:
  - OWASP Node.js
  - OWASP Top 10 Node
---

> [!abstract] TL;DR
> O OWASP Top 10 é a lista das 10 classes de vulnerabilidade mais críticas em aplicações web, publicada pela Open Web Application Security Project com base em dados reais de exploração.
> Em Node.js, as categorias mais frequentes incluem BOLA/IDOR (A01), injeção NoSQL e SSTI (A03), misconfiguration de Express em produção (A05), e SSRF via `fetch` com URL de usuário (A10).
> A defesa efetiva combina validação de input com Zod, ownership checks em toda rota de dados, `npm ci` no CI/CD, `bcrypt` para senhas, tokens criptograficamente seguros, e error handlers que ocultam stack traces em produção.
> Conhecer todos os 10 itens com exemplos Node.js é requisito de entrevistas sênior de segurança.

## O que é

**OWASP Top 10** é um documento de conscientização publicado pela [Open Web Application Security Project](https://owasp.org/www-project-top-ten/) listando as dez vulnerabilidades mais críticas em aplicações web. A lista é atualizada periodicamente com base em dados reais de exploração coletados de centenas de organizações.

Cada categoria agrupa uma classe de falha de segurança com código `A0X:YYYY` — por exemplo, `A01:2021 Broken Access Control`. Não é uma checklist exaustiva, mas um mapa das falhas com maior impacto real e maior prevalência em produção.

Para equipes Node.js, o OWASP Top 10 é um roteiro mínimo: cada categoria tem padrões de ataque específicos ao ecossistema (MongoDB `$where`, pacotes npm maliciosos, stack traces do Express, JWT sem algoritmo fixo) que a equipe precisa conhecer e mitigar ativamente.

## Como funciona

### A01 — Broken Access Control

**O problema**: a aplicação não verifica se o usuário autenticado tem permissão de acessar o recurso específico que solicita. Em REST APIs, o padrão mais comum é BOLA (Broken Object Level Authorization), também chamado de IDOR (Insecure Direct Object Reference): o endpoint `/api/orders/:id` retorna o pedido sem verificar se pertence ao usuário logado — qualquer usuário autenticado pode trocar o ID na URL e ler pedidos alheios.

> [!danger] BOLA em REST API Node.js
> Sem ownership check, qualquer usuário autenticado pode enumerar IDs e ler dados de outros usuários.
> Fix: sempre busque o objeto e verifique `object.userId === req.user.id` antes de retornar. Middleware de autenticação não é suficiente — ele não tem o objeto em mãos.

```typescript
import express from 'express'

const router = express.Router()

// VULNERÁVEL: qualquer usuário autenticado pode acessar qualquer pedido pelo ID
router.get('/orders/:id', async (req, res) => {
  const order = await db.order.findUnique({ where: { id: req.params.id } })
  if (!order) return res.status(404).json({ error: 'Order not found' })
  return res.json(order) // retorna o pedido sem verificar se pertence ao usuário
})

// CORRETO: verifica ownership antes de retornar
router.get('/orders/:id', async (req, res) => {
  const order = await db.order.findUnique({ where: { id: req.params.id } })
  if (!order) return res.status(404).json({ error: 'Order not found' })
  if (order.userId !== req.user.id) return res.status(403).json({ error: 'Forbidden' })
  return res.json(order)
})
```

Mitigações adicionais: RBAC/ABAC para controle de função (admin vs. user), testes automatizados que verificam rejeição de acesso entre usuários, e revisão de código centrada em cada endpoint que expõe IDs de recursos.

### A02 — Cryptographic Failures

**O problema**: dados sensíveis são protegidos com algoritmos fracos ou sem proteção nenhuma. Em Node.js, os erros mais comuns são senhas armazenadas com MD5 ou SHA-1 (sem salt, rápidos de computar — trivialmente revertidos com rainbow tables), segredos hardcoded no código-fonte (`const apiKey = 'abc123'`), e dados sensíveis transmitidos sem TLS.

```typescript
import crypto from 'node:crypto'
import bcrypt from 'bcrypt'

// ERRADO: MD5 não tem salt, é rápido e trivialmente revertível com rainbow tables
function hashPasswordWrong(password: string): string {
  return crypto.createHash('md5').update(password).digest('hex')
}

// CORRETO: bcrypt inclui salt automático, é lento por design e resistente a rainbow tables
async function hashPassword(password: string): Promise<string> {
  const saltRounds = 12 // custo computacional: 2^12 iterações
  return bcrypt.hash(password, saltRounds)
}

async function verifyPassword(password: string, hash: string): Promise<boolean> {
  return bcrypt.compare(password, hash)
}
```

Mitigações: `bcrypt` ou `argon2` para senhas; variáveis de ambiente via `dotenv` + gerenciador de segredos (Vault, AWS Secrets Manager) para credenciais; HTTPS em todos os endpoints; nunca logar senhas, tokens ou dados de cartão.

### A03 — Injection

**O problema**: dados de usuário chegam a um interpretador (SQL, NoSQL, template engine, shell) sem validação ou sanitização, alterando a lógica da query ou executando código arbitrário. Em Node.js, os vetores mais comuns são:

- **NoSQL injection**: MongoDB `$where` executa JavaScript no servidor — input não validado dentro de `$where` permite expressões arbitrárias
- **SQL injection**: concatenação de strings em queries SQL brutas (`"SELECT * FROM users WHERE id = " + req.params.id`)
- **SSTI (Server-Side Template Injection)**: input de usuário renderizado diretamente em engines como Handlebars ou EJS sem escape

> [!danger] NoSQL Injection no MongoDB
> `$where` executa JavaScript no servidor MongoDB. Input não sanitizado pode retornar todos os documentos ou causar DoS.
> Fix: nunca use `$where`. Use operadores seguros do MongoDB e valide todo input com Zod antes da query.

```typescript
import { z } from 'zod'

// VULNERÁVEL: user input direto em $where → execução de JS arbitrário no servidor MongoDB
async function findUserVulnerable(username: string) {
  return User.findOne({ $where: `this.username === '${username}'` })
  // Atacante envia: ' ; return true; // → retorna todos os documentos
}

// CORRETO: validar e sanitizar input com Zod antes de qualquer query
const UsernameSchema = z.string().min(3).max(50).regex(/^[a-zA-Z0-9_]+$/)

async function findUserSafe(rawUsername: unknown) {
  const username = UsernameSchema.parse(rawUsername) // lança ZodError se inválido
  // Nunca use $where — use operadores seguros do MongoDB
  return User.findOne({ username }) // campo direto, sem operadores de JS
}
```

Mitigações: Zod ou Joi para validar todo input externo antes de qualquer operador; ORM/ODM com queries parametrizadas (Prisma, Mongoose sem `$where`); `Content-Type: application/json` com parsing estrito; desabilitar `$where` globalmente no MongoDB.

### A04 — Insecure Design

**O problema**: falhas de segurança arquitetural que nenhuma implementação correta pode corrigir porque o design em si é inseguro. Em Node.js, exemplos comuns incluem: endpoints de autenticação sem rate limiting (brute force irrestrito), flows de reset de senha com tokens sem expiração, ausência de MFA em operações críticas, e ausência de separação entre tokens de curta e longa duração.

```typescript
import crypto from 'node:crypto'
import rateLimit from 'express-rate-limit'
import express from 'express'

const app = express()

// DESIGN CORRETO: rate limiting no endpoint de login evita brute force
const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutos
  limit: 10, // máximo 10 tentativas por IP por janela
  message: { error: 'Too many login attempts, please try again later' },
  standardHeaders: true, // retorna RateLimit-* headers (RFC 6585)
  legacyHeaders: false,
})

app.post('/auth/login', loginLimiter, async (req, res) => {
  // lógica de autenticação
})

// Tokens de reset de senha com TTL curto
function generatePasswordResetToken(): { token: string; expiresAt: Date } {
  const token = crypto.randomBytes(32).toString('hex')
  const expiresAt = new Date(Date.now() + 15 * 60 * 1000) // 15 minutos
  return { token, expiresAt }
}
```

Mitigações: `express-rate-limit` em todas as rotas de autenticação; tokens de reset com expiração de 15 minutos; invalidar tokens após o primeiro uso; threat modeling durante o design, não após a implementação.

### A05 — Security Misconfiguration

**O problema**: o servidor opera com configurações inseguras de fábrica ou deixadas por descuido. Em Express/Node.js: rodar em modo `development` em produção (stack traces expostos nos erros), usar o error handler padrão do Express (expõe detalhes de implementação), deixar rotas de admin acessíveis sem autenticação, e manter `DEBUG=*` no ambiente de produção.

```typescript
import express, { Request, Response, NextFunction } from 'express'

const app = express()

// ERRADO: Express em dev expõe stack traces nos erros por padrão
// Nunca use app.set('env', 'development') em produção
// Nunca deixe NODE_ENV=development no servidor de produção

// CORRETO: error handler customizado que oculta detalhes em produção
app.use((err: Error, _req: Request, res: Response, _next: NextFunction) => {
  // Loga o erro completo internamente (para observability)
  console.error({ message: err.message, stack: err.stack })

  // Retorna mensagem genérica para o cliente — nunca exponha stack trace
  const isProd = process.env.NODE_ENV === 'production'
  res.status(500).json({
    error: isProd ? 'Internal Server Error' : err.message,
  })
})
```

Mitigações: `NODE_ENV=production` obrigatório em produção; error handler customizado que não vaza stack traces; `helmet()` para headers HTTP seguros por padrão; checklist de configuração no pipeline de deploy; remover rotas de debug antes do deploy.

### A06 — Vulnerable and Outdated Components

**O problema**: dependências npm com CVEs conhecidas instaladas em produção. Com o ecossistema npm tendo mais de 2 milhões de pacotes, a chance de uma dependência transitória ter vulnerabilidade é alta. Pacotes abandonados (sem manutenção há anos) acumulam CVEs sem patch.

```bash
# Auditar vulnerabilidades nas dependências instaladas
npm audit

# Corrigir automaticamente vulnerabilidades de baixo risco (atualizações semver-compatíveis)
npm audit fix

# Ver apenas vulnerabilidades de nível high e critical
npm audit --audit-level=high

# Formato JSON para integração com CI/CD pipelines
npm audit --json | jq '.vulnerabilities | to_entries[] | select(.value.severity == "critical")'
```

Mitigações: `npm audit` no pipeline de CI como gate obrigatório (falha o build se high/critical); Dependabot ou Renovate Bot para pull requests automáticos de atualização; lockfile (`package-lock.json`) versionado no repositório; política de não usar pacotes com mais de 2 anos sem commit.

### A07 — Identification and Authentication Failures

**O problema**: falhas no processo de identificação e autenticação. Em Node.js: tokens de sessão gerados com `Math.random()` (previsíveis — não são criptograficamente seguros), JWTs sem especificação do algoritmo esperado (algorithm confusion attack), ausência de invalidação de sessão no logout, e não revogar tokens após mudança de senha.

```typescript
import crypto from 'node:crypto'
import jwt from 'jsonwebtoken'

// ERRADO: Math.random() é previsível — não use para tokens de segurança
function generateTokenWrong(): string {
  return Math.random().toString(36).substring(2)
}

// CORRETO: crypto.randomBytes gera entropia criptograficamente segura
function generateSessionToken(): string {
  return crypto.randomBytes(32).toString('hex') // 256 bits de entropia
}

// JWT: sempre especifique o algoritmo esperado para evitar algorithm confusion
function verifyToken(token: string): object {
  // ERRADO: jwt.verify(token, secret) — vulnerável a algorithm confusion
  // Atacante pode forjar token com alg: "none" ou trocar RS256 por HS256

  // CORRETO: sempre passe { algorithms: ['HS256'] }
  return jwt.verify(token, process.env.JWT_SECRET!, { algorithms: ['HS256'] }) as object
}
```

Mitigações: `crypto.randomBytes(32)` para qualquer token de sessão ou reset; `{ algorithms: ['HS256'] }` explícito no `jwt.verify`; lista negra de tokens invalidados (Redis) para logout e rotação após mudança de senha; expiração curta para access tokens (`exp: 15m`) com refresh tokens rotativos.

### A08 — Software and Data Integrity Failures

**O problema**: o processo de build e deploy não verifica a integridade das dependências e artefatos. Em Node.js: `npm install` sem lockfile pode instalar versões diferentes das testadas; pacotes npm comprometidos podem executar código via scripts de ciclo de vida (`postinstall`, `prepare`); CI/CD que baixa scripts externos sem verificação de hash.

```bash
# ERRADO: npm install pode instalar versões diferentes das testadas
# (sem lockfile, ou se package.json tem ranges como ^1.0.0)
npm install

# CORRETO: npm ci usa o lockfile exatamente e falha se package.json diverge
# Ideal para CI/CD — garante reprodutibilidade
npm ci

# Auditar vulnerabilidades antes de instalar em produção
npm audit --audit-level=high

# Instalar sem executar scripts de ciclo de vida (postinstall, prepare)
# Mitiga pacotes maliciosos que executam código na instalação
npm ci --ignore-scripts
```

Mitigações: `npm ci` (não `npm install`) em todos os ambientes de CI/CD e produção; `--ignore-scripts` para builds de produção; revisar `postinstall` de novos pacotes antes de instalar; habilitar 2FA na conta npm de publicação; usar Sigstore/npm provenance para verificar origem de pacotes publicados.

### A09 — Security Logging and Monitoring Failures

**O problema**: a aplicação não loga eventos de segurança relevantes, loga dados sensíveis em plaintext, ou não tem alertas para comportamentos anômalos. Sem logs adequados, incidentes de segurança passam despercebidos por meses. Em Node.js: usar `console.log` sem estrutura, logar objetos de requisição inteiros (que podem conter senhas ou tokens), e não monitorar falhas de autenticação.

```typescript
import pino from 'pino'

// Logger estruturado com redação automática de campos sensíveis
const logger = pino({
  level: process.env.LOG_LEVEL ?? 'info',
  redact: {
    // Pino automaticamente substitui esses campos por [Redacted] nos logs
    paths: ['req.headers.authorization', 'body.password', 'body.token', 'body.creditCard'],
    censor: '[Redacted]',
  },
})

// Logar eventos de autenticação com nível WARN para fácil filtragem
async function loginHandler(req: express.Request, res: express.Response) {
  const { username, password } = req.body

  const user = await findUser(username)
  if (!user || !(await verifyPassword(password, user.passwordHash))) {
    // Log de falha de autenticação — nunca logue a senha tentada
    logger.warn({ username, ip: req.ip, event: 'auth.failed' }, 'Authentication failed')
    return res.status(401).json({ error: 'Invalid credentials' })
  }

  logger.info({ userId: user.id, ip: req.ip, event: 'auth.success' }, 'User authenticated')
  // ... gerar token e retornar
}
```

Mitigações: `pino` ou `winston` com redação de campos sensíveis; logar todos os eventos de autenticação (sucesso e falha) com IP e timestamp; alertas automáticos para N falhas de login de um mesmo IP em janela de tempo; nunca logar passwords, tokens, CVVs ou PII diretamente; centralizar logs em serviço externo (Datadog, CloudWatch) para auditoria.

### A10 — Server-Side Request Forgery (SSRF)

**O problema**: o servidor faz uma requisição HTTP para uma URL fornecida pelo usuário, sem validar o destino. O atacante pode fornecer `http://169.254.169.254/latest/meta-data/` (endpoint de metadados da AWS, acessível apenas de dentro da instância) e obter as credenciais IAM da aplicação. Ou pode usar a aplicação para fazer port scan na rede interna.

> [!danger] SSRF via fetch com URL de usuário
> Qualquer `fetch(req.body.url)` sem validação é um vetor de SSRF. Em AWS, a URL `http://169.254.169.254/latest/meta-data/iam/security-credentials/` retorna as credenciais IAM da instância EC2.
> Fix: allowlist de hosts aprovados + enforcement de HTTPS + bloqueio de ranges IP privados antes do fetch.

```typescript
import { URL } from 'node:url'

const ALLOWED_HOSTS = new Set(['api.example.com', 'cdn.example.com'])

// Lista de ranges IP privados — bloquear acesso a metadata endpoints e rede interna
const PRIVATE_IP_REGEX = /^(10\.|172\.(1[6-9]|2\d|3[01])\.|192\.168\.|127\.|169\.254\.)/

async function safeFetch(rawUrl: string): Promise<Response> {
  let parsed: URL
  try {
    parsed = new URL(rawUrl)
  } catch {
    throw new Error('Invalid URL')
  }

  // Permite apenas HTTPS
  if (parsed.protocol !== 'https:') {
    throw new Error('Only HTTPS URLs are allowed')
  }

  // Verifica se o host está na allowlist
  if (!ALLOWED_HOSTS.has(parsed.hostname)) {
    throw new Error(`Host ${parsed.hostname} is not allowed`)
  }

  // Bloqueia IPs privados (mitiga DNS rebinding e acesso a metadados de cloud)
  if (PRIVATE_IP_REGEX.test(parsed.hostname)) {
    throw new Error('Access to private IP ranges is not allowed')
  }

  return fetch(rawUrl)
}
```

Mitigações: allowlist de hosts por hostname antes do fetch; enforcement de HTTPS-only; bloqueio de ranges IP privados (RFC 1918 + link-local `169.254.x.x`); resolver o hostname para IP antes do fetch para detectar DNS rebinding; não expor erros de rede ao cliente (evita enumeração de serviços internos).

## Em entrevista

**Q: What is Broken Object Level Authorization (BOLA) and how do you prevent it in a Node.js REST API?**

A: BOLA, also called IDOR (Insecure Direct Object Reference), is when an API endpoint exposes objects by ID without verifying the requester owns or has permission to access that object. For example, `GET /orders/123` returns the order regardless of who calls it — any authenticated user can enumerate IDs and read other users' data. Prevention requires an ownership check at the data access layer: after fetching the object, verify that `object.userId === req.user.id` before returning. This check must happen for every endpoint that exposes user-specific data — middleware-level guards alone are insufficient because they don't have access to the fetched object's ownership fields.

**Q: How does NoSQL injection work in MongoDB and how do you prevent it in Node.js?**

A: MongoDB's `$where` operator executes a JavaScript expression on the server. If an attacker sends input that ends up in a `$where` query — for example, `{ $where: "this.username === '" + userInput + "'" }` — they can inject `'; return true; //` and match all documents, or craft expressions that extract data or cause denial of service. Prevention has two layers: first, never use `$where` — use MongoDB's standard query operators instead, which do not execute JavaScript. Second, validate and type-check input with a schema validator like Zod before constructing any query. Zod's `parse` throws on invalid input before your query code runs, so injected operators like `$where`, `$gt`, or `$regex` in a JSON body are rejected at the boundary.

**Q: What is SSRF and what is the correct defense in a Node.js service that fetches user-supplied URLs?**

A: SSRF (Server-Side Request Forgery) occurs when an attacker supplies a URL that the server fetches on their behalf — allowing access to internal services or cloud metadata endpoints not reachable from the internet. The most famous example is AWS's metadata endpoint at `169.254.169.254`, which returns instance credentials. The correct defense is not a blocklist of bad IPs (DNS rebinding can bypass it) but an allowlist of approved hostnames: resolve the URL, verify the hostname is in your approved set, reject anything else. Additionally, enforce HTTPS-only to prevent protocol-level attacks, and consider resolving hostnames to IPs before fetching to detect DNS rebinding — though allowlisting by hostname is the practical first line of defense for most applications.

**Q: What is the difference between `npm install` and `npm ci` and why does it matter for security?**

A: `npm install` resolves dependencies according to `package.json` version ranges (e.g., `^1.0.0` matches any 1.x.x) and may install versions different from what was tested — either due to a newer patch release or a modified lockfile. `npm ci` installs exactly the versions in `package-lock.json`, fails if `package.json` and the lockfile are out of sync, and never modifies the lockfile. For production and CI/CD environments, `npm ci` is essential because it guarantees that the deployed code uses the exact same dependency tree that passed tests. Pairing it with `--ignore-scripts` prevents malicious packages from executing code during installation via `postinstall` scripts — a common supply chain attack vector.

**Q: How does algorithm confusion work in JWT verification and how do you prevent it?**

A: Algorithm confusion (also called algorithm substitution) exploits the fact that the JWT header specifies the algorithm used to sign the token. If the server calls `jwt.verify(token, secret)` without restricting which algorithms are accepted, an attacker can forge a token by setting the `alg` header to `none` (bypassing signature verification entirely) or by switching from an asymmetric algorithm like RS256 to the symmetric HS256 and signing with the server's public key — which is often freely available. The fix is always explicit: pass `{ algorithms: ['HS256'] }` as the third argument to `jwt.verify()`. This makes the server reject any token whose header specifies a different algorithm, regardless of whether the signature would otherwise verify.

## Vocabulário

- **OWASP (Open Web Application Security Project)**: organização sem fins lucrativos que publica o Top 10 — lista das 10 vulnerabilidades mais críticas em aplicações web, atualizada periodicamente com base em dados reais de exploração.

- **BOLA/IDOR (Broken Object Level Authorization / Insecure Direct Object Reference)**: vulnerabilidade onde uma API retorna ou modifica objetos sem verificar se o solicitante tem permissão de acesso àquele objeto específico; o atacante enumera IDs para acessar dados de outros usuários.

- **NoSQL Injection**: injeção de operadores de query (como `$where`, `$regex`, `$gt`) em campos que não foram validados; permite modificar a lógica de busca ou executar código no servidor MongoDB.

- **SSRF (Server-Side Request Forgery)**: ataque onde o servidor faz requisições HTTP para URLs fornecidas pelo atacante, permitindo acesso a serviços internos ou endpoints de metadados de cloud (ex: `169.254.169.254` na AWS retorna credenciais IAM da instância).

- **Supply chain attack**: compromisso de uma dependência upstream (pacote npm, script de build) para distribuir código malicioso a todos os projetos que a usam; `npm ci` e revisão de scripts `postinstall` são defesas primárias.

- **Security Misconfiguration**: classe de vulnerabilidade onde o servidor opera com configurações inseguras — stack traces expostos, modo de desenvolvimento em produção, admin interfaces públicas, `DEBUG` habilitado com variável de ambiente visível.

- **Algorithm confusion (JWT)**: ataque onde o atacante força o servidor a verificar um JWT com um algoritmo diferente do esperado (ex: trocar RS256 por HS256 e assinar com a chave pública); prevenido passando `{ algorithms: ['HS256'] }` explicitamente ao `jwt.verify()`.

- **DNS rebinding**: técnica que contorna allowlists de IP associando um hostname aprovado a um IP privado após a resolução DNS inicial, permitindo SSRF mesmo com verificação de IP no momento da requisição; mitigado resolvendo o hostname para IP antes do fetch e revalidando.

- **Rainbow table**: tabela pré-computada de pares `(hash → plaintext)` usada para reverter hashes rápidos sem salt (MD5, SHA1); bcrypt e argon2 são imunes porque incluem salt aleatório em cada hash.

- **Lockfile (package-lock.json)**: arquivo gerado automaticamente pelo npm que registra a árvore exata de dependências instaladas, incluindo versões transitivas; `npm ci` usa o lockfile como fonte de verdade e falha se divergir de `package.json`.

## Veja também

- [[03-Dominios/Node/Segurança/index|Segurança]] — MOC do galho 8
- [[03-Dominios/Node/Segurança/03 - Validação de entrada com Zod e Joi|Validação de entrada com Zod e Joi]] — defesa primária contra A03 Injection
- [[03-Dominios/Node/Segurança/04 - JWT e autenticação com jsonwebtoken|JWT e jsonwebtoken]] — defesa contra A07 Authentication Failures
- [[03-Dominios/Node/Segurança/06 - RBAC e ABAC com casl e casbin|RBAC e ABAC]] — defesa contra A01 Broken Access Control
- [[03-Dominios/Node/Segurança/07 - Rate limiting com express-rate-limit|Rate limiting]] — defesa contra A04 Insecure Design (brute force)
- [[03-Dominios/Node/Segurança/08 - Helmet.js e hardening HTTP|Helmet.js e hardening HTTP]] — defesa contra A05 Security Misconfiguration
- [[03-Dominios/Node/Segurança/01 - Supply chain attacks e npm audit|Supply chain attacks e npm audit]] — defesa contra A08 Software Integrity
- [OWASP Top 10](https://owasp.org/www-project-top-ten/) — lista oficial com descrições completas de cada categoria
