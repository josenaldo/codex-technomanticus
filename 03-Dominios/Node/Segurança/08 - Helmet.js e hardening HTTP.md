---
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
---

# Helmet.js e hardening HTTP

> [!abstract] TL;DR
> Helmet.js v7 é um middleware para Express/Node.js que aplica em uma única chamada o conjunto canônico de security headers HTTP — `Content-Security-Policy`, `Strict-Transport-Security`, `X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy` e outros — seguindo a filosofia *secure by default*: tudo ativo por padrão, com opt-out seletivo para casos específicos. CSP com nonces é o controle central contra XSS: gere um valor aleatório por requisição (`crypto.randomBytes(16).toString('base64')`), adicione ao header como `'nonce-<valor>'` e ao atributo `nonce` dos scripts legítimos — scripts injetados não conhecem o nonce e são bloqueados pelo browser. HSTS instrui o browser a usar apenas HTTPS pelo período de `maxAge`; habilitá-lo antes de HTTPS estar totalmente operacional trava o acesso ao site pelo tempo todo de `maxAge`. CORS não é responsabilidade do Helmet, mas `cors` (o pacote) deve ser configurado junto: usar `Access-Control-Allow-Origin: *` com `credentials: true` é inválido — sempre use uma allowlist de origens exatas. Middleware order matters: `app.use(helmet())` deve vir antes de qualquer rota.

## O que é

**Helmet.js** é uma coleção de middlewares pequenos que configuram headers HTTP relacionados à segurança em aplicações Express e Node.js. A versão 7 — atual — é puramente ESM-first, compatível com CommonJS via interop padrão, e ativa por padrão todos os headers recomendados.

A filosofia do Helmet é *secure by default*: ao chamar `helmet()` sem argumentos, você recebe a configuração mais segura para a grande maioria dos casos. Quando um header específico conflita com um requisito da aplicação (ex: precisar embutir a app em um iframe de terceiro), você desativa seletivamente com `{ xFrameOptions: false }` — em vez de partir de zero e lembrar de ligar cada proteção manualmente.

Helmet não é uma solução de segurança completa. Ele não substitui validação de input, autenticação adequada, rate limiting ou gestão de segredos. É uma camada de hardening que fecha as brechas mais comuns de configuração de HTTP que navegadores modernos exploram ativamente — ou que atacantes exploram porque a maioria dos servidores não configura.

## Como funciona

### Headers que Helmet configura por padrão

Helmet v7 ativa os seguintes headers automaticamente quando chamado sem argumentos:

| Header | Valor padrão | Proteção |
|--------|-------------|----------|
| `Content-Security-Policy` | Política restritiva com `default-src 'self'` | XSS, data injection |
| `Cross-Origin-Opener-Policy` | `same-origin` | Isolamento de processo cross-origin |
| `Cross-Origin-Resource-Policy` | `same-origin` | Impede leitura cross-origin de recursos |
| `Origin-Agent-Cluster` | `?1` | Isola o contexto de execução do origin |
| `Referrer-Policy` | `no-referrer` | Não vaza URL de origem em requisições cross-origin |
| `Strict-Transport-Security` | `max-age=15552000; includeSubDomains` | Força HTTPS por 180 dias |
| `X-Content-Type-Options` | `nosniff` | Impede MIME sniffing |
| `X-DNS-Prefetch-Control` | `off` | Previne vazamento via DNS prefetching |
| `X-Download-Options` | `noopen` | Previne download automático no IE (legacy) |
| `X-Frame-Options` | `SAMEORIGIN` | Bloqueia clickjacking em frames cross-origin |
| `X-Permitted-Cross-Domain-Policies` | `none` | Bloqueia acesso cross-domain a documentos Flash/PDF |

**O que foi removido no Helmet v7:** `X-XSS-Protection` foi descontinuado porque browsers modernos o ignoram ou — pior — eram explorados por ele. CSP (`Content-Security-Policy`) é a substituição correta e superior para mitigar XSS.

### Content Security Policy (CSP)

CSP é o header mais poderoso e o mais complexo. Ele instrui o browser sobre quais fontes são permitidas para carregar scripts, estilos, imagens, fontes, frames e conexões. Uma violação CSP bloqueia o recurso e pode reportar o incidente ao servidor.

**Diretivas principais:**

| Diretiva | Controla |
|----------|---------|
| `default-src` | Fallback para todas as diretivas não especificadas |
| `script-src` | Fontes de JavaScript |
| `style-src` | Fontes de CSS |
| `img-src` | Fontes de imagens |
| `connect-src` | Targets de `fetch`, `XHR`, `WebSocket` |
| `font-src` | Fontes de web fonts |
| `frame-src` | Fontes de `<iframe>` |
| `object-src` | Plugins como Flash — deve ser `'none'` |
| `base-uri` | Restricts `<base>` tag |
| `form-action` | Restricts `action` em formulários |

**Nonces — como permitir inline scripts sem `'unsafe-inline'`:**

Um nonce é um valor aleatório gerado a cada requisição. Você adiciona esse valor à diretiva `script-src` como `'nonce-<valor>'` e ao atributo `nonce` de cada script legítimo no HTML. O browser aceita o inline script porque o nonce bate; um script injetado pelo atacante não conhece o nonce e é bloqueado.

**`report-uri` / `report-to`:** permite enviar violações CSP a um endpoint de coleta. Útil para detectar ataques e erros de configuração sem bloquear imediatamente — use `Content-Security-Policy-Report-Only` para modo de auditoria antes de ativar em modo de bloqueio.

### HTTP Strict Transport Security (HSTS)

HSTS instrui o browser a usar apenas HTTPS para o domínio pelo período de `maxAge` segundos. Após a primeira visita com o header, o browser recusa conexões HTTP — mesmo se o usuário digitar `http://` na barra de endereço.

**Parâmetros críticos:**

- `maxAge`: duração em segundos. Mínimo recomendado para produção: `31536000` (1 ano). Comece com um valor menor (ex: `86400` = 1 dia) para validar antes de aumentar.
- `includeSubDomains`: estende a política a todos os subdomínios do domínio. Requer que todos os subdomínios também estejam em HTTPS.
- `preload`: opt-in para submissão à [lista HSTS preload](https://hstspreload.org/) dos browsers. Browsers que consultam a lista nunca tentam HTTP — mesmo na primeira visita, antes de receber o header. Requisitos: `maxAge ≥ 31536000`, `includeSubDomains` e `preload` todos presentes.

> [!danger] Nunca habilite HSTS antes de HTTPS estar totalmente operacional
> HSTS é cacheado pelo browser pelo tempo todo de `maxAge`. Se você habilitar HSTS com `maxAge=31536000` enquanto o site ainda serve tráfego HTTP — ou antes de o certificado TLS estar correto — os usuários que já visitaram o site ficarão bloqueados por até 1 ano. O browser recusará conexões HTTP e não há reset fácil do lado do cliente (exceto limpar manualmente o cache HSTS do browser).
>
> **Solução correta**: valide HTTPS completamente primeiro (certificado válido, redirect HTTP→HTTPS funcionando, sem mixed content). Então habilite HSTS com `maxAge` pequeno (86400 = 1 dia). Monitore por erros. Aumente gradualmente até `31536000`. Só então adicione `preload` se necessário.

### CORS correto

CORS (Cross-Origin Resource Sharing) não é configurado pelo Helmet — é responsabilidade do pacote `cors`. Mas eles trabalham juntos: Helmet configura os headers de segurança passivos; `cors` configura os headers de controle de acesso ativos (`Access-Control-Allow-Origin`, `Access-Control-Allow-Credentials`, etc.).

**Regras críticas de CORS:**

- `Access-Control-Allow-Origin: *` permite qualquer origem. É adequado apenas para APIs públicas sem autenticação.
- `Access-Control-Allow-Credentials: true` permite que requisições incluam cookies e headers de autenticação.
- **`*` + `credentials: true` é inválido** — a spec CORS proíbe explicitamente essa combinação. Browsers rejeitam a resposta. Sempre use uma allowlist de origens exatas quando `credentials: true` for necessário.

A forma correta de implementar allowlist dinâmica: receba o header `Origin` da requisição, verifique se está em um `Set` de origens aprovadas, e reflita o valor exato no `Access-Control-Allow-Origin` da resposta — ou rejeite com erro se não estiver na lista.

### Configuração avançada

**Desabilitando um middleware específico:**

```typescript
app.use(helmet({ xFrameOptions: false }))
```

**Passando opções para um middleware específico:**

```typescript
app.use(helmet({
  contentSecurityPolicy: {
    directives: { defaultSrc: ["'self'"], scriptSrc: ["'self'"] }
  }
}))
```

**Ordem dos middlewares:** Helmet deve ser registrado antes das rotas. Como middlewares Express são executados na ordem de registro, registrar Helmet depois de uma rota faz com que as respostas dessa rota não recebam os headers de segurança.

## Armadilhas

> [!danger] CSP com `'unsafe-inline'` anula a proteção contra XSS
> `'unsafe-inline'` na diretiva `script-src` permite que qualquer script inline seja executado — incluindo scripts injetados por um atacante via XSS. Se você precisar de inline scripts, a solução não é `'unsafe-inline'`; é **nonces**: gere um valor aleatório por requisição com `crypto.randomBytes(16).toString('base64')`, adicione `'nonce-<valor>'` à diretiva `script-src` e o atributo `nonce="<valor>"` em cada `<script>` legítimo. Scripts injetados não conhecem o nonce e são bloqueados pelo browser.
>
> **Solução**: remova `'unsafe-inline'` e implemente nonces como mostrado no Snippet 2. Se você usa um template engine (Pug, EJS, Handlebars), passe `res.locals.cspNonce` para o template e adicione `nonce="{{ cspNonce }}"` a cada `<script>` no HTML.

> [!danger] HSTS sem HTTPS ativo trava os usuários
> Se o site ainda serve tráfego HTTP — ou se o certificado TLS não está correto — e você define `Strict-Transport-Security: max-age=31536000`, o browser cacheia essa instrução e recusará conexões HTTP pelo período inteiro. Não há como reverter isso do lado do servidor: o browser ignora um `max-age=0` enviado via HTTP porque já sabe que deve usar apenas HTTPS. O usuário fica bloqueado até expirar o cache manualmente ou o `maxAge` vencer.
>
> **Solução**: habilite HSTS apenas depois de HTTPS estar totalmente operacional. Comece com `maxAge` pequeno, monitore, aumente gradualmente.

> [!danger] CORS `*` + `credentials: true` é rejeitado pelos browsers
> A spec CORS proíbe `Access-Control-Allow-Origin: *` combinado com `Access-Control-Allow-Credentials: true`. Qualquer origem significa que qualquer site pode fazer requisições autenticadas — o que é uma falha de segurança grave. Browsers implementam essa proteção e rejeitam a resposta com erro de CORS.
>
> **Solução**: use uma allowlist de origens exatas. No pacote `cors`, implemente o callback `origin`:
>
> ```typescript
> cors({
>   origin: (origin, callback) => {
>     if (!origin || ALLOWED_ORIGINS.has(origin)) callback(null, true)
>     else callback(new Error(`Origin ${origin} not allowed`))
>   },
>   credentials: true,
> })
> ```

## Snippets

### Snippet 1 — Setup básico com Express

```typescript
import express from 'express'
import helmet from 'helmet'

const app = express()

// Helmet deve vir antes das rotas — configura headers em cada resposta
app.use(helmet())

app.get('/health', (_req, res) => res.json({ status: 'ok' }))

app.listen(3000)
```

### Snippet 2 — CSP customizado com nonces

```typescript
import express, { Request, Response, NextFunction } from 'express'
import helmet from 'helmet'
import crypto from 'node:crypto'

const app = express()

// Middleware 1: gera um nonce fresco por requisição — NUNCA reutilize nonces
app.use((_req: Request, res: Response, next: NextFunction) => {
  res.locals.cspNonce = crypto.randomBytes(16).toString('base64')
  next()
})

// Middleware 2: aplica Helmet com CSP usando o nonce da requisição
app.use((_req: Request, res: Response, next: NextFunction) => {
  helmet({
    contentSecurityPolicy: {
      directives: {
        defaultSrc: ["'self'"],
        // Função recebe (req, res) e retorna a diretiva com o nonce da requisição atual
        scriptSrc: ["'self'", (_req, res) => `'nonce-${(res as Response).locals.cspNonce}'`],
        styleSrc: ["'self'", "'unsafe-inline'"], // aceitável para estilos sem conteúdo controlado pelo usuário
        imgSrc: ["'self'", 'data:', 'https:'],
        connectSrc: ["'self'"],
        fontSrc: ["'self'"],
        objectSrc: ["'none'"],    // bloqueia plugins como Flash
        baseUri: ["'self'"],      // impede hijack via <base>
        formAction: ["'self'"],   // restringe targets de formulários
      },
    },
  })(_req, res, next)
})

app.get('/', (_req, res) => {
  // Passa o nonce para o template engine — aqui demonstrado inline
  res.send(`<script nonce="${res.locals.cspNonce}">console.log('safe inline script')</script>`)
})

app.listen(3000)
```

### Snippet 3 — HSTS e desabilitando middlewares específicos

```typescript
import express from 'express'
import helmet from 'helmet'

const app = express()

app.use(
  helmet({
    // HSTS: apenas habilite quando HTTPS estiver totalmente operacional
    strictTransportSecurity: {
      maxAge: 31536000,      // 1 ano em segundos — padrão recomendado para produção
      includeSubDomains: true,
      preload: true,         // opt-in para lista HSTS preload dos browsers
    },

    // X-Frame-Options: DENY bloqueia todos os frames — previne clickjacking
    xFrameOptions: { action: 'deny' },

    // Referrer-Policy: no-referrer para APIs privacy-sensitive
    referrerPolicy: { policy: 'no-referrer' },

    // X-Content-Type-Options: nosniff já está ativo por padrão — deixe assim
    // contentTypeOptions: {},  // equivalente a não especificar (comportamento padrão)

    // Para desabilitar um middleware completamente (ex: embedding legítimo em iframe):
    // xFrameOptions: false,
  })
)

app.get('/api/data', (_req, res) => res.json({ data: 'secured' }))

app.listen(3000)
```

### Snippet 4 — CORS com allowlist dinâmica (par com Helmet)

```typescript
import express from 'express'
import helmet from 'helmet'
import cors from 'cors'

const ALLOWED_ORIGINS = new Set([
  'https://app.example.com',
  'https://staging.example.com',
])

const app = express()

// Helmet primeiro — headers de segurança passivos
app.use(helmet())

// CORS depois — headers de controle de acesso ativos
app.use(
  cors({
    origin: (origin, callback) => {
      // Permite server-to-server (sem header Origin) ou origens aprovadas
      if (!origin || ALLOWED_ORIGINS.has(origin)) {
        callback(null, true)
      } else {
        callback(new Error(`Origin ${origin} not allowed by CORS policy`))
      }
    },
    credentials: true,   // requer origem exata — nunca use com '*'
    methods: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH'],
    allowedHeaders: ['Content-Type', 'Authorization'],
  })
)

app.get('/api/profile', (_req, res) => res.json({ user: 'Alice' }))

app.listen(3000)
```

### Snippet 5 — Verificando headers em testes com supertest

```typescript
import request from 'supertest'
import express from 'express'
import helmet from 'helmet'

const app = express()
app.use(helmet())
app.get('/ping', (_req, res) => res.json({ ok: true }))

describe('security headers', () => {
  it('sets Content-Security-Policy', async () => {
    const res = await request(app).get('/ping')
    expect(res.headers['content-security-policy']).toBeDefined()
  })

  it('sets X-Content-Type-Options: nosniff', async () => {
    const res = await request(app).get('/ping')
    expect(res.headers['x-content-type-options']).toBe('nosniff')
  })

  it('sets Strict-Transport-Security', async () => {
    const res = await request(app).get('/ping')
    expect(res.headers['strict-transport-security']).toContain('max-age=')
  })

  it('sets X-Frame-Options', async () => {
    const res = await request(app).get('/ping')
    expect(res.headers['x-frame-options']).toBeDefined()
  })

  it('does not set X-XSS-Protection (removed in Helmet v7)', async () => {
    const res = await request(app).get('/ping')
    // X-XSS-Protection foi removido no Helmet v7 — browsers modernos ignoram ou exploram esse header
    expect(res.headers['x-xss-protection']).toBeUndefined()
  })
})
```

### Snippet 6 — Report-Only CSP para auditoria antes de bloqueio

```typescript
import express, { Request, Response, NextFunction } from 'express'
import helmet from 'helmet'
import crypto from 'node:crypto'

const app = express()

// Gera nonce por requisição
app.use((_req: Request, res: Response, next: NextFunction) => {
  res.locals.cspNonce = crypto.randomBytes(16).toString('base64')
  next()
})

// Fase 1: modo report-only — coleta violações sem bloquear
// Útil para auditar uma app existente antes de ativar CSP em modo de bloqueio
app.use((_req: Request, res: Response, next: NextFunction) => {
  const nonce = (res as Response).locals.cspNonce as string

  // Helmet aplica Content-Security-Policy; sobrescreva com Report-Only manualmente
  helmet({
    contentSecurityPolicy: {
      directives: {
        defaultSrc: ["'self'"],
        scriptSrc: ["'self'", `'nonce-${nonce}'`],
        reportUri: '/csp-report', // envia violações para o endpoint de coleta
      },
      // reportOnly: true — disponível como opção direta no helmet v7
      reportOnly: true,
    },
  })(_req, res, next)
})

// Endpoint que recebe relatórios de violação CSP do browser
app.post('/csp-report', express.json({ type: 'application/csp-report' }), (req, res) => {
  const report = req.body['csp-report'] as Record<string, string>
  console.warn('CSP violation:', JSON.stringify({
    blockedUri: report['blocked-uri'],
    violatedDirective: report['violated-directive'],
    documentUri: report['document-uri'],
  }))
  res.status(204).end()
})

app.listen(3000)
```

## Em entrevista

**Q: What does Helmet.js do and why should you always include it in Express applications?**

A: Helmet is a collection of small middleware functions that set security-related HTTP response headers. It protects against common web vulnerabilities: Content-Security-Policy mitigates XSS by controlling which sources the browser may execute scripts from, X-Frame-Options prevents clickjacking by blocking the app from being embedded in cross-origin iframes, Strict-Transport-Security enforces HTTPS so browsers never fall back to HTTP, and X-Content-Type-Options prevents MIME sniffing where browsers ignore the declared `Content-Type` and execute content based on guessing its type. Including it is a baseline security requirement — without it, browsers operate in a permissive mode that enables entire classes of attacks a single middleware call would prevent. Helmet v7 follows a secure-by-default philosophy: `app.use(helmet())` gives you the correct configuration immediately, and you opt out of specific headers only when your application genuinely requires it.

**Q: What is Content Security Policy and how do you add inline script support without using 'unsafe-inline'?**

A: CSP is an HTTP header that tells the browser which sources are allowed to load scripts, styles, images, and other resources. Without CSP, if an attacker injects a `<script>` tag via XSS, the browser executes it. With a strict CSP like `script-src 'self'`, the browser only executes scripts from the same origin — injected scripts are blocked. Using `'unsafe-inline'` defeats CSP's main value entirely — it allows any inline script, including injected ones. The correct approach is nonces: for each request, generate a cryptographically random value with `crypto.randomBytes(16).toString('base64')`, add it to the `script-src` directive as `'nonce-<value>'`, and include the same value as the `nonce` attribute on legitimate inline `<script>` tags. The attacker cannot know the nonce because it changes every request, so injected scripts without the correct nonce attribute are blocked by the browser.

**Q: Why is enabling HSTS dangerous if your site is not fully on HTTPS?**

A: HSTS tells browsers to always use HTTPS for the domain for `maxAge` seconds — and browsers cache this directive persistently. If you enable HSTS while your site still serves traffic over HTTP, or before your TLS certificate is correctly configured, every user who has visited the site will be unable to reach it over HTTP for the entire HSTS duration — potentially a year. The browser ignores any attempt to reset this via HTTP because it already knows the site must use HTTPS. There is no easy server-side reset; the user must manually clear their browser's HSTS cache. The correct order is: get HTTPS working and validate it thoroughly — correct certificate, HTTP redirects to HTTPS working, no mixed content warnings — then enable HSTS with a short `maxAge` like 86400 seconds (one day), monitor for issues, and gradually increase to the production value of 31536000 (one year). Only add `preload` after the full `maxAge` is stable.

**Q: Why does CORS `Access-Control-Allow-Origin: *` fail when credentials are enabled?**

A: The CORS spec explicitly forbids combining `Access-Control-Allow-Origin: *` with `Access-Control-Allow-Credentials: true`. The wildcard means "any origin may read this response," but sharing cookies or authorization tokens with any arbitrary origin is a fundamental security hole — any malicious site could make authenticated requests to your API on behalf of logged-in users. Browsers enforce this rule at the spec level and reject the response with a CORS error regardless of what the server sends. The fix is to echo back the specific allowed origin from an approved allowlist, making the `Access-Control-Allow-Origin` header an exact origin string — for example, `https://app.example.com` — instead of `*`. In the `cors` package, this is done via the `origin` callback: check `Set.has(origin)`, then `callback(null, true)` or `callback(new Error(...))`.

## Vocabulário

| Termo | Definição |
|-------|-----------|
| **CSP (Content Security Policy)** | Header HTTP que define quais fontes de recursos o browser pode carregar; mitiga XSS impedindo execução de scripts não autorizados — a configuração correta usa nonces em vez de `'unsafe-inline'` |
| **HSTS (HTTP Strict Transport Security)** | Header que instrui o browser a usar apenas HTTPS para o domínio pelo período de `maxAge` em segundos; evita downgrade attacks e é cacheado persistentemente pelo browser |
| **Nonce** | Valor aleatório de uso único gerado por requisição (`crypto.randomBytes(16).toString('base64')`), adicionado ao header CSP e ao atributo `nonce` de scripts legítimos; permite inline scripts sem `'unsafe-inline'` porque o atacante não conhece o valor |
| **Clickjacking** | Ataque que carrega o site-alvo em um `<iframe>` invisível sobre outro site e engana o usuário a clicar em elementos da página-alvo; mitigado por `X-Frame-Options: DENY` ou pela diretiva CSP `frame-ancestors 'none'` |
| **MIME sniffing** | Comportamento de browsers que tentam inferir o tipo de conteúdo ignorando o `Content-Type` declarado pelo servidor; bloqueado pelo header `X-Content-Type-Options: nosniff`, que força o browser a usar o tipo declarado |
| **CORS (Cross-Origin Resource Sharing)** | Mecanismo de browser que controla quais origens externas podem fazer requisições para a API; mal configurado — uso de `*` com `credentials: true` — é inválido e vira vetor de ataque |
| **Referrer-Policy** | Header que controla quanta informação sobre a URL de origem é enviada no header `Referer` em requisições cross-origin; `no-referrer` omite completamente, útil para APIs privacy-sensitive |
| **Security header** | Header HTTP que instrui o browser a aplicar políticas de segurança; Helmet.js automatiza a configuração correta de múltiplos security headers em uma única chamada de middleware |
| **HSTS preload** | Lista mantida pelos browsers (Chrome, Firefox, Safari) com domínios que devem usar apenas HTTPS mesmo antes da primeira visita; opt-in via diretiva `preload` no header HSTS mais submissão em hstspreload.org |
| **CSP report-only** | Modo de operação do CSP via header `Content-Security-Policy-Report-Only` que coleta violações sem bloquear recursos; útil para auditar antes de ativar CSP em modo de bloqueio |

## Veja também

- [[03-Dominios/Node/Segurança/index|Segurança]] — MOC do galho 8
- [[03-Dominios/Node/Segurança/05 - OAuth 2.0 e OIDC com openid-client|OAuth 2.0 e OIDC]] — autenticação complementar ao hardening HTTP
- [[03-Dominios/Node/Segurança/04 - JWT e autenticação com jsonwebtoken|JWT e jsonwebtoken]] — autenticação complementar ao hardening HTTP
- [[03-Dominios/Node/Segurança/07 - Rate limiting com express-rate-limit|Rate limiting]] — proteção contra abuso de API, par natural do Helmet
- [[03-Dominios/Node/Segurança/09 - OWASP Top 10 para Node|OWASP Top 10 para Node]] — contexto de ameaças que estes headers mitigam
- [Helmet.js docs](https://helmetjs.github.io/) — documentação oficial com lista completa de headers e opções de configuração
- [MDN: Content-Security-Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy) — referência completa de diretivas CSP com exemplos e compatibilidade de browsers
- [hstspreload.org](https://hstspreload.org/) — submissão e verificação de status na lista HSTS preload dos browsers
