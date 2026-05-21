# Galho 8 — Segurança: Plano de Execução

## Goal

Criar o galho 8 da trilha Node Senior no vault `codex-technomanticus`. O galho cobre segurança em Node.js: supply chain attacks, gerenciamento de segredos e variáveis de ambiente, validação de entrada com Zod e Joi, autenticação com JWT e jsonwebtoken, OAuth 2.0 e OIDC com openid-client, autorização com RBAC/ABAC usando casl e casbin, rate limiting com express-rate-limit, hardening HTTP com Helmet.js, OWASP Top 10 para Node.js e cheatsheet de decisão.

## Architecture

Pasta destino: `03-Dominios/Node/Segurança/`

Cada nota é atômica — cobre um tópico com profundidade suficiente para responder perguntas de entrevista senior. As notas seguem o padrão canônico do vault: frontmatter completo, TL;DR, seções de conteúdo, "Em entrevista" em inglês, vocabulário técnico e "Veja também".

## Tech Stack

- Zod v3 (validação schema-first e TypeScript-first)
- Joi v17 (validação orientada a objetos, legado)
- jsonwebtoken v9 (geração e verificação de JWTs)
- helmet v7 (headers de segurança HTTP)
- express-rate-limit v7 (rate limiting)
- passport.js v0.7 (middleware de autenticação plugável)
- openid-client v5 (OAuth 2.0 e OIDC)
- casl v6 (ABAC/RBAC declarativo)
- casbin (enforcer de políticas Rego/CSV)
- node:crypto (módulo nativo para operações criptográficas)

---

## REGRAS CRÍTICAS

1. **Nunca adicionar Co-Authored-By ao commit** — a mensagem de commit termina após a descrição, sem nenhuma linha de assinatura.
2. **Mínimo de linhas é limite inferior** — entregar mais é correto; entregar menos é falha.
3. **Código real, não pseudocódigo** — todos os snippets devem ser executáveis com os pacotes declarados em Tech Stack. Nenhum snippet placeholder.
4. **"Em entrevista" em inglês** — mínimo 3 perguntas com respostas em inglês fluente de nível senior. Nenhuma resposta de entrevista em português.
5. **Vocabulário mínimo** — toda nota de conteúdo deve ter seção `## Vocabulário` com no mínimo 6 termos definidos.

---

## Self-Check (executar antes de cada commit)

```
[ ] 1. Frontmatter completo: title, created, updated, type: concept, status: growing, publish: true, tags (node + tema), aliases
[ ] 2. TL;DR presente e com ≥ 3 linhas de conteúdo real (não placeholder)
[ ] 3. Contagem de linhas ≥ mínimo definido na task
[ ] 4. Seção "Em entrevista" com ≥ 3 perguntas e respostas em inglês de nível senior (não em português)
[ ] 5. Seção "Vocabulário" com ≥ 6 termos definidos
[ ] 6. Seção de armadilhas com pelo menos 1 callout [!danger] com problema + solução concreta
[ ] 7. Seção "Como funciona" com ≥ 3 subseções ou subsections nomeadas
[ ] 8. Snippets de código: ≥ mínimo definido na task, todos executáveis com o tech stack declarado
[ ] 9. Wikilinks para [[Node.js]] e [[Segurança]] (MOC do galho) presentes no corpo ou "Veja também"
[ ] 10. Seção "Veja também" com link para a nota oficial ou documentação da biblioteca principal (fonte externa real)
```

---

## Estrutura de arquivos

```
03-Dominios/Node/Segurança/
├── index.md
├── 01 - Supply chain attacks e npm audit.md
├── 02 - Segredos e variáveis de ambiente.md
├── 03 - Validação de entrada com Zod e Joi.md
├── 04 - JWT e autenticação com jsonwebtoken.md
├── 05 - OAuth 2.0 e OIDC com openid-client.md
├── 06 - RBAC e ABAC com casl e casbin.md
├── 07 - Rate limiting com express-rate-limit.md
├── 08 - Helmet.js e hardening HTTP.md
├── 09 - OWASP Top 10 para Node.md
└── 10 - Cheatsheet e decision tree de segurança.md
```

---

## Tasks

### Task 1 — index.md (MOC do galho)

**Files:** `03-Dominios/Node/Segurança/index.md` (criar)

**Commit:** `feat(node/g8): add index - Segurança MOC`

**Frontmatter:**
```yaml
title: "Segurança"
type: moc
publish: true
created: 2026-05-12
updated: 2026-05-12
status: growing
progresso: andamento
tags:
  - node
  - segurança
  - moc
aliases:
  - Segurança Node
  - Node Security
```

**Conteúdo mínimo:**
- TL;DR resumindo os 10 tópicos do galho
- Parágrafo de introdução contextualizando segurança em Node.js senior
- Lista de links para todas as 10 notas do galho com descrição de 1 linha cada
- Seção "Veja também" com links para `[[Node.js]]` e `[[03-Dominios/Node/index]]`

**Mínimo de linhas:** 80

**Mínimo de snippets:** 0

---

### Task 2 — 01 - Supply chain attacks e npm audit

**Files:** `03-Dominios/Node/Segurança/01 - Supply chain attacks e npm audit.md` (criar)

**Commit:** `feat(node/g8): add 01 - Supply chain attacks e npm audit`

**Frontmatter:**
```yaml
title: "Supply chain attacks e npm audit"
created: 2026-05-12
updated: 2026-05-12
type: concept
status: growing
publish: true
tags:
  - node
  - segurança
  - supply-chain
  - npm
aliases:
  - Supply Chain Node
  - npm audit
```

**Conteúdo mínimo:**
- TL;DR: o que são supply chain attacks, por que npm é vetor de ataque, ferramentas de mitigação
- Como funcionam supply chain attacks: typosquatting, dependency confusion, malicious maintainer takeover
- `npm audit` e `npm audit fix` — output, CVEs, severidade
- Ferramentas complementares: `socket.dev`, `snyk`, `osv-scanner`, GitHub Dependabot
- Estratégias de mitigação: lockfile commit, `npm ci`, allowlist de pacotes, `--ignore-scripts`
- Verificação de integridade: `npm pack --dry-run`, `npx is-my-node-vulnerable`
- Armadilhas: `npm audit fix --force` que introduz breaking changes; scripts pós-instalação maliciosos
- Em entrevista: 3+ perguntas sobre supply chain em inglês
- Vocabulário: ≥ 6 termos (supply chain attack, typosquatting, dependency confusion, lockfile, CVE, SCA)

**Mínimo de linhas:** 280

**Mínimo de snippets:** 5

---

### Task 3 — 02 - Segredos e variáveis de ambiente

**Files:** `03-Dominios/Node/Segurança/02 - Segredos e variáveis de ambiente.md` (criar)

**Commit:** `feat(node/g8): add 02 - Segredos e variáveis de ambiente`

**Frontmatter:**
```yaml
title: "Segredos e variáveis de ambiente"
created: 2026-05-12
updated: 2026-05-12
type: concept
status: growing
publish: true
tags:
  - node
  - segurança
  - env-vars
  - secrets
aliases:
  - Segredos Node
  - Env Vars Segurança
```

**Conteúdo mínimo:**
- TL;DR: nunca hardcode segredos, usar process.env, vault ou secrets manager
- Antipadrões: hardcode no código, .env commitado, console.log de segredos
- `node --env-file=.env` (Node 20.6+) como substituto de dotenv
- `.env` local vs `.env.example` no git — convenção de equipe
- Gestão de segredos em produção: AWS Secrets Manager, HashiCorp Vault, Doppler, GCP Secret Manager
- Validação de env vars na inicialização com Zod (`z.object({...}).parse(process.env)`)
- Rotação de segredos sem downtime: graceful reload, env vars dinâmicas
- Armadilhas: vazar segredos em stack traces, env vars expostas via `process.env` em logs, `.env.production` no repositório
- Em entrevista: 3+ perguntas sobre gestão de segredos em inglês
- Vocabulário: ≥ 6 termos (secret, env var, vault, rotation, least privilege, secret sprawl)

**Mínimo de linhas:** 280

**Mínimo de snippets:** 5

---

### Task 4 — 03 - Validação de entrada com Zod e Joi

**Files:** `03-Dominios/Node/Segurança/03 - Validação de entrada com Zod e Joi.md` (criar)

**Commit:** `feat(node/g8): add 03 - Validação de entrada com Zod e Joi`

**Frontmatter:**
```yaml
title: "Validação de entrada com Zod e Joi"
created: 2026-05-12
updated: 2026-05-12
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
```

**Conteúdo mínimo:**
- TL;DR: nunca confiar em input externo; validar e sanitizar na borda do sistema
- Por que validação de entrada é segurança: injection attacks, prototype pollution, XSS via JSON
- Zod v3: definição de schema, `parse` vs `safeParse`, `z.object`, `z.string`, `z.enum`, `z.union`, transformações
- Integração do Zod com Express/Fastify/NestJS (middleware de validação)
- Joi v17: alternativa orientada a objetos, uso em codebases legados
- Sanitização vs Validação — diferença conceitual; quando usar `xss`, `DOMPurify` server-side
- Validação de env vars com Zod na inicialização da aplicação
- Armadilhas: validar apenas o tipo sem checar tamanho/formato (ReDoS, buffer overflows), confiar em validação do cliente
- Em entrevista: 3+ perguntas em inglês sobre validação de entrada
- Vocabulário: ≥ 6 termos (schema validation, sanitization, parse, safeParse, type coercion, ReDoS)

**Mínimo de linhas:** 320

**Mínimo de snippets:** 7

---

### Task 5 — 04 - JWT e autenticação com jsonwebtoken

**Files:** `03-Dominios/Node/Segurança/04 - JWT e autenticação com jsonwebtoken.md` (criar)

**Commit:** `feat(node/g8): add 04 - JWT e autenticação com jsonwebtoken`

**Frontmatter:**
```yaml
title: "JWT e autenticação com jsonwebtoken"
created: 2026-05-12
updated: 2026-05-12
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
```

**Conteúdo mínimo:**
- TL;DR: JWT como token stateless assinado; jsonwebtoken para sign/verify; access + refresh token pattern
- Anatomia do JWT: header, payload, signature — o que cada parte contém
- `jwt.sign()` com expiração (`expiresIn`), algoritmos (HS256 vs RS256 vs ES256) e quando usar cada
- `jwt.verify()` e tratamento de erros (`TokenExpiredError`, `JsonWebTokenError`, `NotBeforeError`)
- Access token + refresh token pattern: duração, rotação, blacklist com Redis
- Armazenamento seguro no cliente: cookie httpOnly vs localStorage — trade-offs
- Revogação de tokens: Redis blacklist, versão no banco, jti claim
- Armadilhas: algoritmo `none`, segredos fracos, claims não validados, payload sensível sem criptografia
- Em entrevista: 3+ perguntas em inglês sobre JWT
- Vocabulário: ≥ 6 termos (JWT, claim, signature, access token, refresh token, revocation)

**Mínimo de linhas:** 320

**Mínimo de snippets:** 7

---

### Task 6 — 05 - OAuth 2.0 e OIDC com openid-client

**Files:** `03-Dominios/Node/Segurança/05 - OAuth 2.0 e OIDC com openid-client.md` (criar)

**Commit:** `feat(node/g8): add 05 - OAuth 2.0 e OIDC com openid-client`

**Frontmatter:**
```yaml
title: "OAuth 2.0 e OIDC com openid-client"
created: 2026-05-12
updated: 2026-05-12
type: concept
status: growing
publish: true
tags:
  - node
  - segurança
  - oauth
  - oidc
  - autenticação
aliases:
  - OAuth Node
  - OIDC Node
  - openid-client
```

**Conteúdo mínimo:**
- TL;DR: OAuth 2.0 para autorização delegada; OIDC como camada de identidade; openid-client para integração server-side
- OAuth 2.0 flows: Authorization Code (com PKCE), Client Credentials, Device Code — quando usar cada
- OIDC: ID Token vs Access Token, claims padrão (`sub`, `email`, `aud`, `iss`), UserInfo endpoint
- openid-client v5: `Issuer.discover()`, `new Client()`, `authorizationUrl()`, `callback()`, `userinfo()`
- Integração com Express: callback route, session management, CSRF protection com `state` e `nonce`
- passport.js com `passport-oauth2` para flows simples
- Armadilhas: não validar `state`, aceitar `aud` inválido, não verificar `iss`, open redirect no callback
- Em entrevista: 3+ perguntas em inglês sobre OAuth 2.0 e OIDC
- Vocabulário: ≥ 6 termos (OAuth 2.0, OIDC, authorization code, PKCE, ID token, claims)

**Mínimo de linhas:** 320

**Mínimo de snippets:** 6

---

### Task 7 — 06 - RBAC e ABAC com casl e casbin

**Files:** `03-Dominios/Node/Segurança/06 - RBAC e ABAC com casl e casbin.md` (criar)

**Commit:** `feat(node/g8): add 06 - RBAC e ABAC com casl e casbin`

**Frontmatter:**
```yaml
title: "RBAC e ABAC com casl e casbin"
created: 2026-05-12
updated: 2026-05-12
type: concept
status: growing
publish: true
tags:
  - node
  - segurança
  - autorização
  - rbac
  - abac
aliases:
  - RBAC Node
  - ABAC Node
  - casl
  - casbin
```

**Conteúdo mínimo:**
- TL;DR: RBAC mapeia papel→permissão; ABAC avalia atributos de sujeito/objeto/contexto; casl para ABAC TypeScript, casbin para políticas externas
- RBAC vs ABAC — diferenças, quando usar cada modelo
- casl v6: `defineAbility`, `can`, `cannot`, `subject`, middleware Express/NestJS
- Permissões condicionais em casl: `can('read', 'Post', { authorId: user.id })`
- casbin: modelo de política (`p = sub, obj, act`), adapter para banco, `enforce()` síncrono e assíncrono
- Integração com JWT: claims de papéis/permissões no token
- Princípio do menor privilégio e separação de responsabilidades
- Armadilhas: checar autorização apenas no frontend, papéis hardcoded no código, falta de audit log de decisões de autorização
- Em entrevista: 3+ perguntas em inglês sobre autorização
- Vocabulário: ≥ 6 termos (RBAC, ABAC, permission, policy, principal, least privilege)

**Mínimo de linhas:** 300

**Mínimo de snippets:** 6

---

### Task 8 — 07 - Rate limiting com express-rate-limit

**Files:** `03-Dominios/Node/Segurança/07 - Rate limiting com express-rate-limit.md` (criar)

**Commit:** `feat(node/g8): add 07 - Rate limiting com express-rate-limit`

**Frontmatter:**
```yaml
title: "Rate limiting com express-rate-limit"
created: 2026-05-12
updated: 2026-05-12
type: concept
status: growing
publish: true
tags:
  - node
  - segurança
  - rate-limiting
  - express
aliases:
  - Rate Limiting Node
  - express-rate-limit
```

**Conteúdo mínimo:**
- TL;DR: rate limiting protege APIs de DoS, brute force e abuso; express-rate-limit com store Redis para ambientes distribuídos
- Algoritmos de rate limiting: fixed window, sliding window, token bucket, leaky bucket — trade-offs
- `express-rate-limit` v7: configuração básica, `windowMs`, `max`, `message`, `standardHeaders`, `legacyHeaders`
- Store distribuído com `rate-limit-redis` (ioredis) para múltiplas instâncias
- Rate limiting por rota vs global: login (5 req/min) vs API pública (100 req/min)
- Headers de rate limit: `RateLimit-Limit`, `RateLimit-Remaining`, `RateLimit-Reset` (RFC 6585)
- Rate limiting em Fastify: `@fastify/rate-limit` com Redis
- Armadilhas: store em memória não funciona em cluster, rate limit por IP atrás de proxy reverso (X-Forwarded-For), não retornar headers de rate limit
- Em entrevista: 3+ perguntas em inglês sobre rate limiting
- Vocabulário: ≥ 6 termos (rate limiting, fixed window, sliding window, token bucket, throttling, DoS)

**Mínimo de linhas:** 280

**Mínimo de snippets:** 6

---

### Task 9 — 08 - Helmet.js e hardening HTTP

**Files:** `03-Dominios/Node/Segurança/08 - Helmet.js e hardening HTTP.md` (criar)

**Commit:** `feat(node/g8): add 08 - Helmet.js e hardening HTTP`

**Frontmatter:**
```yaml
title: "Helmet.js e hardening HTTP"
created: 2026-05-12
updated: 2026-05-12
type: concept
status: growing
publish: true
tags:
  - node
  - segurança
  - helmet
  - http-headers
aliases:
  - Helmet.js
  - Hardening HTTP Node
  - Security Headers Node
```

**Conteúdo mínimo:**
- TL;DR: Helmet.js configura headers de segurança HTTP em uma linha; defaults cobrem os principais vetores de ataque
- O que Helmet configura por padrão: `Content-Security-Policy`, `X-DNS-Prefetch-Control`, `X-Frame-Options`, `HSTS`, `X-Content-Type-Options`, `Referrer-Policy`, `X-XSS-Protection` (removido no v7)
- Content Security Policy (CSP): `default-src`, `script-src`, `style-src`, nonces, report-uri
- HTTP Strict Transport Security (HSTS): `maxAge`, `includeSubDomains`, `preload`
- CORS correto: `Access-Control-Allow-Origin`, `credentials`, allowlist dinâmica vs `*`
- Configuração avançada: desabilitar middleware específico, `helmet.contentSecurityPolicy({ directives: {...} })`
- Armadilhas: CSP `'unsafe-inline'` anula proteção XSS, HSTS sem HTTPS configurado, CORS `*` com `credentials: true` (inválido)
- Em entrevista: 3+ perguntas em inglês sobre security headers
- Vocabulário: ≥ 6 termos (CSP, HSTS, CORS, XSS, clickjacking, security header)

**Mínimo de linhas:** 280

**Mínimo de snippets:** 5

---

### Task 10 — 09 - OWASP Top 10 para Node

**Files:** `03-Dominios/Node/Segurança/09 - OWASP Top 10 para Node.md` (criar)

**Commit:** `feat(node/g8): add 09 - OWASP Top 10 para Node`

**Frontmatter:**
```yaml
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
```

**Conteúdo mínimo:**
- TL;DR: as 10 categorias de vulnerabilidade mais críticas para aplicações web segundo OWASP, com exemplos Node.js concretos e mitigações
- A01 Broken Access Control: exemplos Node (BOLA/IDOR em APIs REST, falta de verificação de ownership)
- A02 Cryptographic Failures: uso de MD5/SHA1 para senhas, transmissão sem TLS, segredos em código
- A03 Injection: NoSQL injection (MongoDB `$where`), SQL injection com query strings, SSTI
- A04 Insecure Design: ausência de rate limiting, autenticação sem MFA em flows críticos
- A05 Security Misconfiguration: Express em modo development em prod, stack traces expostos, admin UIs públicas
- A06 Vulnerable Components: npm audit, versões desatualizadas, pacotes abandonados
- A07 Authentication Failures: senhas fracas, tokens de sessão previsíveis, falta de invalidação
- A08 Software Integrity: supply chain, `npm ci` vs `npm install`, lockfile integrity
- A09 Logging Failures: ausência de logs de autenticação, dados sensíveis em logs
- A10 SSRF: fetch de URLs fornecidas pelo usuário sem allowlist, cloud metadata endpoint
- Em entrevista: 3+ perguntas em inglês sobre OWASP
- Vocabulário: ≥ 6 termos (OWASP, BOLA, injection, SSRF, IDOR, security misconfiguration)

**Mínimo de linhas:** 350

**Mínimo de snippets:** 7

---

### Task 11 — 10 - Cheatsheet e decision tree de segurança

**Files:** `03-Dominios/Node/Segurança/10 - Cheatsheet e decision tree de segurança.md` (criar)

**Commit:** `feat(node/g8): add 10 - Cheatsheet e decision tree de segurança`

**Frontmatter:**
```yaml
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
```

**Conteúdo mínimo:**
- TL;DR: decisões e padrões de segurança consolidados para Node.js senior
- Decision tree: precisa validar entrada? → Zod (TypeScript) ou Joi (JS legado); precisa autenticar usuários com OAuth? → openid-client; precisa autorização granular? → casl (ABAC) ou RBAC simples; precisa proteger API de abuso? → express-rate-limit + Redis
- Tabela comparativa: ferramentas de segurança por categoria (validação, auth, autorização, headers, rate limiting, supply chain)
- Checklist de security review para PRs: validação de entrada, sanitização, autenticação, autorização, segredos, logging, rate limiting, dependency audit
- Padrões de resposta de erro segura: não vazar stack traces, mensagens genéricas para erros de autenticação, códigos HTTP corretos
- Vocabulário consolidado: ≥ 8 termos das notas anteriores do galho
- Em entrevista: 3+ perguntas transversais sobre segurança em Node.js senior em inglês
- Seção "Veja também" apontando para todas as notas do galho

**Mínimo de linhas:** 300

**Mínimo de snippets:** 4

---

### Task 12 — Atualizar index.md do Node e Node.js.md

**Files:**
- `03-Dominios/Node/index.md` (editar)
- `03-Dominios/JavaScript/Backend/Node.js.md` (editar)

**Commit:** `feat(node/g8): register galho 8 in Node MOC and trunk`

**Passos:**

1. Em `03-Dominios/Node/index.md`, adicionar na lista de galhos (após a linha do galho 7, se existir, ou no final da lista existente):
   ```
   - [[03-Dominios/Node/Segurança/index]] — galho 8: supply chain, segredos, validação de entrada (Zod/Joi), JWT, OAuth 2.0 e OIDC, RBAC, rate limiting, Helmet.js e OWASP Top 10
   ```

2. Em `03-Dominios/JavaScript/Backend/Node.js.md`, adicionar na seção `## Veja também` (após linha do galho 7, se existir, ou antes das demais entradas de galho):
   ```
   - [[03-Dominios/Node/Segurança/index|Segurança]] — galho 8 da trilha Node Senior; supply chain, segredos, validação, JWT, OAuth 2.0, RBAC, rate limiting, Helmet.js e OWASP Top 10
   ```

3. Atualizar campo `updated:` em ambos os arquivos para `2026-05-12`.
