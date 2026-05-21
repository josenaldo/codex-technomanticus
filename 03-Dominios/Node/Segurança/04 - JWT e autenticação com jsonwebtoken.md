---
title: "JWT e autenticação com jsonwebtoken"
created: 2026-05-13
updated: 2026-05-13
type: concept
status: growing
publish: true
tags:
  - node
  - segurança
  - jwt
  - autenticação
aliases:
  - JWT Node
  - jsonwebtoken
  - JSON Web Token Node
---

# JWT e autenticação com jsonwebtoken

> [!abstract] TL;DR
> JWT (JSON Web Token) é um formato compacto de token autocontido e assinado digitalmente que permite transmitir claims entre partes sem consultar um banco de dados a cada requisição — a autenticidade é verificada localmente pela assinatura criptográfica, tornando o sistema stateless por natureza. A biblioteca `jsonwebtoken` v9 é a implementação de referência no ecossistema Node.js, expondo `jwt.sign()` para emitir tokens e `jwt.verify()` para validar assinatura, expiração e claims adicionais em uma única chamada. O padrão de access token (vida curta, 15min) combinado com refresh token (vida longa, 7d) resolve o dilema entre segurança e usabilidade: o access token expira rápido limitando a janela de abuso, enquanto o refresh token — armazenado de forma segura e rotacionado a cada uso — permite renovar a sessão sem nova autenticação do usuário.

## O que é

**JWT (JSON Web Token)** é um padrão aberto definido na [RFC 7519](https://datatracker.ietf.org/doc/html/rfc7519) para representar claims entre duas partes de forma compacta, URL-safe e opcionalmente verificável ou criptografada. Na prática, é uma string com três partes separadas por ponto (`.`), cada uma codificada em **base64url** — não base64 padrão, pois base64url é seguro para uso em URLs e cabeçalhos HTTP sem escape adicional.

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyXzEyMyIsImlhdCI6MTcxNTYwMDAwMCwiZXhwIjoxNzE1NjA5MDAwfQ.abc123signature
```

### Header

O header é um objeto JSON com dois campos obrigatórios codificado em base64url:

```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

- **`alg`**: algoritmo de assinatura — `HS256`, `RS256`, `ES256`, entre outros
- **`typ`**: tipo do token — sempre `"JWT"` para JWTs padrão

### Payload (claims)

O payload contém os **claims** — afirmações sobre o sujeito do token. Há três categorias:

**Claims registrados (RFC 7519):**

| Claim | Nome               | Descrição                                         |
|-------|--------------------|---------------------------------------------------|
| `sub` | Subject            | Identificador único do sujeito (ex: user ID)      |
| `iat` | Issued At          | Timestamp de emissão (segundos desde epoch)       |
| `exp` | Expiration Time    | Timestamp de expiração — verificado automaticamente |
| `iss` | Issuer             | Quem emitiu o token (ex: `"api.example.com"`)    |
| `aud` | Audience           | Destinatário(s) do token (ex: `"web-client"`)    |
| `jti` | JWT ID             | Identificador único do token — essencial para revogação |
| `nbf` | Not Before         | Token não é válido antes deste timestamp          |

**Claims públicos** são registrados no IANA JWT Registry para interoperabilidade.

**Claims privados** são campos customizados acordados entre emissor e receptor — `role`, `plan`, `orgId`, etc.

> [!warning] Payload não é criptografado
> O payload é apenas codificado em base64url — **qualquer pessoa com o token pode decodificá-lo**. Nunca coloque dados sensíveis no payload: senhas, números de cartão, PII completa. A assinatura garante **integridade** (o payload não foi alterado), não **confidencialidade**.

### Signature

A assinatura é calculada sobre `base64url(header) + "." + base64url(payload)` usando o algoritmo e a chave definidos no header:

```
HMACSHA256(
  base64url(header) + "." + base64url(payload),
  secret
)
```

Para algoritmos assimétricos (RS256, ES256), a chave privada assina e a chave pública verifica. O receptor valida a assinatura sem nunca ter acesso à chave de assinatura.

## Como funciona

### jwt.sign()

`jwt.sign(payload, secretOrPrivateKey, options)` cria e retorna um JWT assinado.

```javascript
import jwt from 'jsonwebtoken'

// Geração de access token — HS256 (simétrico)
const accessToken = jwt.sign(
  {
    sub: user.id,
    role: user.role,
    iss: 'api.example.com',
    aud: 'web-client',
  },
  process.env.JWT_SECRET,
  {
    algorithm: 'HS256',
    expiresIn: '15m',
    jwtid: crypto.randomUUID(), // popula o claim jti
  }
)

// Geração de token — RS256 (assimétrico)
const tokenRS256 = jwt.sign(
  { sub: user.id },
  process.env.RSA_PRIVATE_KEY, // chave privada PEM
  {
    algorithm: 'RS256',
    expiresIn: '15m',
  }
)
```

**HS256 vs RS256 vs ES256:**

| Algoritmo | Tipo        | Chave de assinatura | Chave de verificação | Quando usar                                      |
|-----------|-------------|---------------------|----------------------|--------------------------------------------------|
| HS256     | Simétrico   | `secret` (string)   | Mesmo `secret`       | Serviço único ou microserviços com secret compartilhado |
| RS256     | Assimétrico | Chave privada RSA   | Chave pública RSA    | Múltiplos serviços verificadores sem expor a chave de assinatura |
| ES256     | Assimétrico | Chave privada EC    | Chave pública EC     | Mesmos casos do RS256 com chaves menores e performance melhor |

Use **HS256** quando todos os serviços que assinam e verificam estão sob seu controle e podem compartilhar o secret com segurança. Use **RS256/ES256** em sistemas com múltiplos consumidores: os verificadores recebem apenas a chave pública (sem risco de forjar tokens) e você pode publicar a chave pública via JWKS endpoint (`/.well-known/jwks.json`).

### jwt.verify()

`jwt.verify(token, secretOrPublicKey, options)` valida assinatura, expiração e outros claims. Lança exceção em caso de falha — sempre use try/catch.

```javascript
import jwt from 'jsonwebtoken'

function verifyAccessToken(token) {
  try {
    const payload = jwt.verify(token, process.env.JWT_SECRET, {
      algorithms: ['HS256'],      // OBRIGATÓRIO: previne algorithm confusion attack
      issuer: 'api.example.com',  // valida claim iss
      audience: 'web-client',     // valida claim aud
    })
    return { valid: true, payload }
  } catch (err) {
    if (err instanceof jwt.TokenExpiredError) {
      // Token expirou — exp está no passado
      // err.expiredAt contém o timestamp de expiração
      return { valid: false, reason: 'expired', expiredAt: err.expiredAt }
    }

    if (err instanceof jwt.NotBeforeError) {
      // Token ainda não é válido — nbf está no futuro
      // err.date contém o timestamp nbf
      return { valid: false, reason: 'not_yet_valid', date: err.date }
    }

    if (err instanceof jwt.JsonWebTokenError) {
      // Assinatura inválida, token malformado, algorithm none, etc.
      return { valid: false, reason: 'invalid', message: err.message }
    }

    // Erro inesperado — não vaze detalhes internos
    return { valid: false, reason: 'unknown' }
  }
}
```

**Tipos de erro lançados por `jwt.verify()`:**

| Erro                  | Causa                                                         |
|-----------------------|---------------------------------------------------------------|
| `TokenExpiredError`   | `exp` está no passado — token expirou                        |
| `NotBeforeError`      | `nbf` está no futuro — token ainda não é válido              |
| `JsonWebTokenError`   | Assinatura inválida, formato malformado, algorithm `none`    |

### Access token + refresh token

O padrão de dual-token resolve a tensão entre segurança (tokens curtos expiram rápido) e usabilidade (usuário não precisa relogar a cada 15 minutos).

**Fluxo:**

1. Login bem-sucedido → servidor emite `accessToken` (15min) + `refreshToken` (7d)
2. Client usa `accessToken` em cada requisição (`Authorization: Bearer <token>`)
3. Quando `accessToken` expira (recebe 401), client envia `refreshToken` ao endpoint de renovação
4. Servidor valida `refreshToken`, invalida o token atual (rotação), emite novo par de tokens
5. Client armazena o novo par e continua operando

```javascript
import jwt from 'jsonwebtoken'
import { randomUUID } from 'node:crypto'

const ACCESS_TOKEN_SECRET = process.env.ACCESS_TOKEN_SECRET
const REFRESH_TOKEN_SECRET = process.env.REFRESH_TOKEN_SECRET

function generateTokenPair(userId, role) {
  const jti = randomUUID()

  const accessToken = jwt.sign(
    { sub: userId, role, jti: `access_${jti}` },
    ACCESS_TOKEN_SECRET,
    { algorithm: 'HS256', expiresIn: '15m', issuer: 'api.example.com' }
  )

  const refreshToken = jwt.sign(
    { sub: userId, jti: `refresh_${jti}` },
    REFRESH_TOKEN_SECRET,
    { algorithm: 'HS256', expiresIn: '7d', issuer: 'api.example.com' }
  )

  return { accessToken, refreshToken }
}

// Endpoint de renovação com rotação de refresh token
async function refreshTokenEndpoint(req, res) {
  const { refreshToken } = req.cookies // httpOnly cookie

  if (!refreshToken) {
    return res.status(401).json({ error: 'No refresh token' })
  }

  try {
    const payload = jwt.verify(refreshToken, REFRESH_TOKEN_SECRET, {
      algorithms: ['HS256'],
      issuer: 'api.example.com',
    })

    // Verifica se o refresh token foi revogado (blacklist Redis)
    const isBlacklisted = await redis.get(`jwt:blacklist:${payload.jti}`)
    if (isBlacklisted) {
      return res.status(401).json({ error: 'Token revoked' })
    }

    // Rotação: invalida o refresh token atual
    const ttl = payload.exp - Math.floor(Date.now() / 1000)
    await redis.setex(`jwt:blacklist:${payload.jti}`, ttl, '1')

    // Emite novo par de tokens
    const user = await User.findById(payload.sub)
    const tokens = generateTokenPair(user.id, user.role)

    // Envia refresh token via httpOnly cookie
    res.cookie('refreshToken', tokens.refreshToken, {
      httpOnly: true,
      secure: true,
      sameSite: 'strict',
      maxAge: 7 * 24 * 60 * 60 * 1000, // 7 dias em ms
    })

    return res.json({ accessToken: tokens.accessToken })
  } catch (err) {
    if (err instanceof jwt.TokenExpiredError) {
      return res.status(401).json({ error: 'Refresh token expired' })
    }
    return res.status(401).json({ error: 'Invalid refresh token' })
  }
}
```

## Middleware de autenticação

O middleware extrai o token do cabeçalho `Authorization: Bearer <token>`, valida e injeta o payload na requisição para uso nas rotas subsequentes.

```javascript
import jwt from 'jsonwebtoken'

function authenticate(req, res, next) {
  const authHeader = req.headers['authorization']

  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'Missing or malformed Authorization header' })
  }

  const token = authHeader.slice(7) // remove "Bearer "

  try {
    const payload = jwt.verify(token, process.env.ACCESS_TOKEN_SECRET, {
      algorithms: ['HS256'],
      issuer: 'api.example.com',
    })

    req.user = payload // { sub, role, jti, iat, exp, iss }
    next()
  } catch (err) {
    if (err instanceof jwt.TokenExpiredError) {
      return res.status(401).json({ error: 'Token expired' })
    }
    return res.status(401).json({ error: 'Invalid token' })
  }
}

// Uso em rotas Express
app.get('/api/profile', authenticate, (req, res) => {
  res.json({ userId: req.user.sub, role: req.user.role })
})
```

## Armazenamento seguro no cliente

A escolha de onde armazenar tokens no browser tem implicações diretas de segurança:

| Local             | Vulnerabilidade principal | Mitigação                            |
|-------------------|--------------------------|--------------------------------------|
| `localStorage`    | XSS — qualquer script na página pode ler | Content Security Policy, mas não elimina o risco |
| `sessionStorage`  | XSS — mesmo problema do localStorage     | Expira ao fechar a aba, mas ainda vulnerável |
| Cookie `httpOnly` | CSRF — requisição forjada por outro site | `SameSite=Strict` ou `SameSite=Lax` + CSRF token |

**Recomendação:**

- **Access token** em memória JavaScript (variável de módulo ou estado React/Vue) — desaparece no reload, mas não é acessível via XSS de outros scripts e não persiste em disco
- **Refresh token** em cookie `httpOnly; Secure; SameSite=Strict` — inacessível via JavaScript, enviado automaticamente pelo browser, protegido contra CSRF pelo `SameSite`

Esse padrão híbrido é o que frameworks de auth modernos (NextAuth, Auth.js) implementam por padrão.

> [!tip] SPA com servidor BFF
> Em arquiteturas com Backend-for-Frontend, o BFF gerencia os tokens inteiramente no servidor — o browser nunca vê tokens, apenas session cookies httpOnly. Isso elimina a superfície de ataque XSS no cliente completamente.

## Revogação de tokens

JWT é stateless por natureza — uma vez emitido, o servidor não pode "invalidar" o token antes da expiração sem alguma forma de estado compartilhado. As estratégias principais são:

### Redis blacklist com jti

Armazena o `jti` (JWT ID) de tokens revogados no Redis com TTL igual ao tempo restante de vida do token. A cada requisição, verifica se o `jti` está na blacklist antes de processar.

```javascript
import { Redis } from 'ioredis'

const redis = new Redis(process.env.REDIS_URL)

// Revogar um token (ex: logout, troca de senha)
async function revokeToken(payload) {
  const now = Math.floor(Date.now() / 1000)
  const ttl = payload.exp - now

  if (ttl > 0) {
    // Mantém na blacklist até o token naturalmente expirar
    await redis.setex(`jwt:blacklist:${payload.jti}`, ttl, '1')
  }
}

// Verificar na blacklist — use no middleware authenticate
async function isTokenRevoked(jti) {
  const result = await redis.get(`jwt:blacklist:${jti}`)
  return result !== null
}

// Middleware com verificação de blacklist
async function authenticateWithBlacklist(req, res, next) {
  const authHeader = req.headers['authorization']
  if (!authHeader?.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'Missing Authorization header' })
  }

  const token = authHeader.slice(7)

  try {
    const payload = jwt.verify(token, process.env.ACCESS_TOKEN_SECRET, {
      algorithms: ['HS256'],
    })

    const revoked = await isTokenRevoked(payload.jti)
    if (revoked) {
      return res.status(401).json({ error: 'Token has been revoked' })
    }

    req.user = payload
    next()
  } catch (err) {
    return res.status(401).json({ error: 'Invalid token' })
  }
}
```

### Token version no banco (tokenVersion)

Alternativa ao Redis: cada usuário tem um campo `tokenVersion` no banco. O claim `version` é incluído no token. Se o `tokenVersion` do usuário for incrementado (logout, troca de senha, comprometimento), todos os tokens anteriores falham na verificação mesmo sem uma blacklist.

```javascript
// Ao emitir token — inclui a versão atual do usuário
const token = jwt.sign(
  { sub: user.id, version: user.tokenVersion },
  process.env.JWT_SECRET,
  { algorithm: 'HS256', expiresIn: '15m' }
)

// No middleware — verifica versão
async function authenticateWithVersion(req, res, next) {
  // ... verificação padrão do jwt.verify() ...
  const user = await User.findById(payload.sub).select('tokenVersion')
  if (user.tokenVersion !== payload.version) {
    return res.status(401).json({ error: 'Token invalidated' })
  }
  req.user = payload
  next()
}

// Para invalidar todos os tokens do usuário (ex: logout global)
async function invalidateAllTokens(userId) {
  await User.findByIdAndUpdate(userId, { $inc: { tokenVersion: 1 } })
}
```

**Comparação de estratégias de revogação:**

| Estratégia        | Latência por request | Dependência extra | Granularidade     |
|-------------------|---------------------|-------------------|-------------------|
| Redis blacklist   | ~1ms (Redis local)  | Redis             | Token individual  |
| Token version     | ~5-10ms (DB query)  | Banco existente   | Todos os tokens do usuário |
| Expiração curta   | Zero                | Nenhuma           | Nenhuma (espera expirar) |

## Armadilhas

> [!danger] Algorithm none attack
> A especificação JWT original permitia `"alg": "none"`, indicando que o token não possui assinatura. Algumas implementações antigas aceitavam essa opção — um atacante poderia criar um token com qualquer payload e definir `alg: none` para que o servidor aceitasse sem verificar assinatura. **Solução**: sempre passe a opção `algorithms` explicitamente em `jwt.verify()`:
> ```javascript
> // ❌ Vulnerável — aceita qualquer algoritmo incluindo none
> jwt.verify(token, secret)
>
> // ✅ Seguro — restringe ao algoritmo esperado
> jwt.verify(token, secret, { algorithms: ['HS256'] })
> ```
> A biblioteca `jsonwebtoken` v9 já rejeita `alg: none` por padrão — é necessário passar explicitamente `algorithms: ['none']` para aceitar tokens não assinados. A opção explícita continua sendo defesa em profundidade e documenta a intenção.

> [!danger] Secrets fracos e previsíveis
> Um secret HS256 de baixa entropia pode ser quebrado por força bruta offline — o atacante captura um token válido e tenta secrets até a assinatura bater. A RFC 7518 recomenda mínimo de 256 bits (32 bytes) de entropia para HS256. Nunca use strings curtas, palavras do dicionário ou valores hardcoded no código. Use `node:crypto` para gerar secrets seguros:
> ```javascript
> import { randomBytes } from 'node:crypto'
>
> // Gera 32 bytes (256 bits) de entropia — adequado para HS256
> const secret = randomBytes(32).toString('hex') // 64 chars hex
>
> // Execute uma vez e armazene no gerenciador de secrets (Vault, AWS Secrets Manager, etc.)
> console.log(secret)
> ```

> [!danger] Dados sensíveis no payload
> O payload JWT é **apenas codificado em base64url**, não criptografado. Qualquer pessoa que interceptar ou receber o token pode decodificá-lo em milissegundos com `atob()` no browser ou `Buffer.from(token.split('.')[1], 'base64').toString()` no Node. Nunca coloque no payload: senhas (mesmo hash), números de cartão de crédito, tokens de API de terceiros, informações médicas, ou qualquer dado que não possa ser exposto publicamente. Se precisar de payload criptografado, use **JWE (JSON Web Encryption)** — RFC 7516.

## Em entrevista

**Q: What is the difference between HS256 and RS256, and when would you use each?**

A: HS256 is a symmetric algorithm — the same secret key is used to both sign and verify tokens. This means every service that needs to verify tokens must have access to the secret, which creates a security risk in distributed systems: if any verifier is compromised, the attacker can forge tokens. RS256 is asymmetric — a private key signs the token and a public key verifies it. Only the issuing service holds the private key, while verifiers only need the public key, which can be safely distributed or published via a JWKS endpoint. I use HS256 for single-service applications or tightly controlled microservices where secret distribution is manageable. I switch to RS256 or ES256 when there are multiple independent services consuming tokens, third-party integrations, or when I need to publish a JWKS endpoint for public key discovery. ES256 is generally preferable to RS256 when choosing asymmetric algorithms because it produces smaller keys and signatures with equivalent security.

---

**Q: How do you handle JWT revocation in a stateless system?**

A: Pure stateless JWT revocation is a contradiction in terms — true revocation requires state. The practical approaches are: First, Redis blacklisting using the `jti` claim: when a token is revoked (logout, password change, compromise), store its `jti` in Redis with a TTL equal to the token's remaining lifetime. Every request checks the blacklist before processing. This adds one Redis round-trip per request but is fast and precise at the individual token level. Second, token versioning: store a `tokenVersion` field per user in the database, embed it as a claim, and verify it matches on every request. Incrementing the version instantly invalidates all existing tokens for that user, which is useful for "logout everywhere" scenarios. Third, keeping access token lifetimes very short (5-15 minutes) and accepting that revocation only applies to refresh tokens, which are rotated on every use and explicitly tracked. In practice I combine short-lived access tokens with Redis blacklisting for logout and refresh token rotation with a database or Redis store for session management.

---

**Q: What is the algorithm none vulnerability and how do you prevent it?**

A: The algorithm none vulnerability exploits an optional feature in the original JWT specification that allowed tokens with no signature — the header would contain `"alg": "none"` and the signature segment would be empty. Some early libraries, when receiving such a token, would skip signature verification entirely, trusting the payload unconditionally. An attacker could take any valid token, decode the payload, modify the claims (e.g., change `role` to `admin`), re-encode with `alg: none` and an empty signature, and the vulnerable server would accept it. Prevention has two layers: first, always pass an explicit `algorithms` array to `jwt.verify()` — for example `{ algorithms: ['HS256'] }` — so the library rejects tokens using any other algorithm. Second, use an up-to-date version of `jsonwebtoken` (v9+), which rejects `alg: none` by default when a secret is provided, but the explicit option is defense-in-depth. This is also an example of why you should never trust the `alg` header from the token itself to determine which key or algorithm to use during verification.

---

**Q: Explain the access token + refresh token pattern and why it's used.**

A: The pattern solves a fundamental tension in stateless authentication: short token lifetimes improve security but hurt usability, while long lifetimes improve usability but increase the window of exposure if a token is stolen. The solution is two tokens with different lifetimes and purposes. The access token is short-lived — typically 5 to 15 minutes — and is sent with every API request in the Authorization header. When it expires, the client uses the refresh token to get a new access token without prompting the user to log in again. The refresh token is long-lived — 7 to 30 days — but it is only sent to one specific endpoint (the token refresh endpoint), reducing its exposure surface. Critically, refresh tokens should be rotated: every time a refresh token is used, it is invalidated and a new one is issued. This enables refresh token theft detection — if an attacker uses a stolen refresh token, the legitimate user's next refresh attempt will fail because the token was already used, signaling a compromise. Refresh tokens should be stored in httpOnly cookies to prevent JavaScript access, while access tokens can be kept in memory. This pattern is the foundation of how OAuth 2.0 and most modern authentication systems work.

## Vocabulário

| Termo                       | Definição                                                                                                                                                                    |
|-----------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **JWT (JSON Web Token)**    | Padrão aberto (RFC 7519) para representar claims entre partes como uma string compacta, URL-safe, composta por header, payload e signature separados por ponto               |
| **Claim**                   | Afirmação sobre o sujeito do token ou sobre o próprio token; pode ser registrado (definido na RFC), público (registrado no IANA) ou privado (acordado entre as partes)       |
| **Signature**               | Terceira parte do JWT, gerada aplicando o algoritmo definido no header sobre `base64url(header).base64url(payload)` usando a chave secreta ou privada; garante integridade    |
| **Access token**            | Token de vida curta (5-15 min) enviado a cada requisição para autenticar o usuário; projetado para expirar rapidamente, limitando o impacto de um vazamento                  |
| **Refresh token**           | Token de vida longa (dias a semanas) usado exclusivamente para obter novos access tokens sem nova autenticação do usuário; deve ser rotacionado e armazenado com segurança    |
| **Revogação**               | Processo de invalidar um token antes do seu vencimento natural; requer estado externo (Redis, banco de dados) já que o JWT em si é stateless                                 |
| **jti (JWT ID)**            | Claim opcional mas recomendado que contém um identificador único para o token (UUID); essencial para implementar blacklists de revogação precisas no nível do token individual |
| **Algorithm confusion attack** | Ataque que explora implementações que aceitam múltiplos algoritmos sem restrição explícita; exemplo clássico é o ataque `alg: none` que bypassa verificação de assinatura   |

## Veja também

- [[03-Dominios/Node/Segurança/index|Segurança]]
- [[JavaScript/Backend/Node.js|Node.js]]
- [[03-Dominios/Node/Segurança/02 - Segredos e variáveis de ambiente|Segredos e variáveis de ambiente]]
- [[03-Dominios/Node/Segurança/01 - Supply chain attacks e npm audit|Supply chain attacks e npm audit]]
- [jsonwebtoken — npm](https://www.npmjs.com/package/jsonwebtoken)
- [RFC 7519 — JSON Web Token](https://datatracker.ietf.org/doc/html/rfc7519)
- [RFC 7518 — JSON Web Algorithms](https://datatracker.ietf.org/doc/html/rfc7518)
