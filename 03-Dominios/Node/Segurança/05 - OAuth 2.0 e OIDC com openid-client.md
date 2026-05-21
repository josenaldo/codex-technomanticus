---
title: "OAuth 2.0 e OIDC com openid-client"
created: 2026-05-13
updated: 2026-05-13
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
---

# OAuth 2.0 e OIDC com openid-client

> [!abstract] TL;DR
> OAuth 2.0 é um framework de **autorização delegada** — ele permite que um usuário conceda a uma aplicação acesso limitado a seus recursos em outro serviço, mas por si só **não autentica** ninguém: o access token não diz quem o usuário é, apenas o que ele pode fazer. OpenID Connect (OIDC) resolve isso adicionando uma camada de identidade sobre OAuth 2.0: introduz o **ID Token** (um JWT assinado que contém claims sobre o usuário) e o endpoint **UserInfo**, transformando OAuth 2.0 em um protocolo de autenticação completo. No ecossistema Node.js, `openid-client` v5 é a biblioteca de referência para implementar fluxos OIDC no lado servidor — suporta discovery automático de metadados, Authorization Code com PKCE, validação de ID Token e integração com Express ou Fastify com poucas linhas de código.

## O que é

### OAuth 2.0 — framework de autorização

**OAuth 2.0** é um framework de autorização definido na [RFC 6749](https://datatracker.ietf.org/doc/html/rfc6749). Ele resolve um problema específico: permitir que um usuário autorize uma aplicação de terceiros a agir em seu nome em outro serviço — sem compartilhar sua senha.

O exemplo clássico é "Login com Google": o usuário não entrega a senha do Google para a sua app. Em vez disso, o Google emite um **access token** que representa a permissão concedida pelo usuário, com escopo limitado e tempo de vida definido.

**OAuth 2.0 define 4 papéis:**

| Papel | Descrição |
|-------|-----------|
| **Resource Owner** | O usuário que possui os dados |
| **Client** | A aplicação que quer acessar os dados |
| **Authorization Server** | Emite tokens (ex: Google, GitHub, Auth0) |
| **Resource Server** | Hospeda os recursos protegidos (ex: Google Drive API) |

**O que OAuth 2.0 NÃO faz:** O access token não contém identidade do usuário — é apenas um "bilhete de permissão". Usar o access token para autenticar usuários é uma vulnerabilidade clássica, porque qualquer aplicação que receber esse token pode ser enganada a pensar que o usuário está autenticado.

### OIDC — camada de identidade sobre OAuth 2.0

**OpenID Connect (OIDC)** é uma extensão do OAuth 2.0 que adiciona identidade ao protocolo. Ele resolve exatamente a lacuna deixada pelo OAuth 2.0:

- Adiciona o **ID Token**: um JWT assinado com claims sobre o usuário (`sub`, `email`, `name`, `iss`, `aud`, `exp`)
- Adiciona o endpoint **UserInfo**: rota padronizada para buscar claims adicionais usando o access token
- Adiciona o **Discovery endpoint** (`/.well-known/openid-configuration`): metadados do servidor, endpoints, chaves públicas — permite configuração automática via `Issuer.discover()`
- Adiciona parâmetros obrigatórios: `nonce` para prevenir replay attacks, `scope: 'openid'` para ativar o protocolo

**Resumo da distinção:**

| Protocolo | Finalidade | Token principal | Garante identidade? |
|-----------|-----------|-----------------|----------------------|
| OAuth 2.0 | Autorização delegada | Access Token | Não |
| OIDC | Autenticação + autorização | ID Token + Access Token | Sim |

### Por que a distinção importa

Em uma entrevista ou code review, confundir OAuth 2.0 com autenticação é um sinal de alerta imediato. Um access token pode ser emitido para um serviço de máquina (Client Credentials flow) — sem nenhum usuário humano envolvido. Validar "quem o usuário é" com base no access token é inseguro porque:

1. O token pode ter sido emitido para outro client
2. O token não contém `aud` restrito ao seu servidor
3. Um atacante pode reutilizar um token legítimo em um contexto diferente

A distinção correta: **use OAuth 2.0 para autorização** (o usuário pode fazer X?), **use OIDC para autenticação** (quem é o usuário?).

## Como funciona

### Flows OAuth 2.0

OAuth 2.0 define múltiplos **grant types** (fluxos) para cenários distintos:

#### Authorization Code (com PKCE)

O fluxo padrão para aplicações web com servidor backend. Com PKCE (Proof Key for Code Exchange), também é seguro para SPAs e apps mobile.

**Quando usar:** aplicação web que autentica usuários humanos via provedor externo (Google, GitHub, Auth0, Okta).

**Sequência:**

```
1. Client gera code_verifier (random) e code_challenge = SHA256(code_verifier)
2. Client redireciona usuário para /authorize?response_type=code&code_challenge=...
3. Authorization Server autentica o usuário e emite authorization code
4. Client troca code + code_verifier por access_token + id_token no /token endpoint
5. Authorization Server valida code_verifier contra code_challenge armazenado
```

**Por que PKCE:** sem PKCE, um atacante que intercepta o authorization code (em logs, referrer header, ou redirecionar malicioso) pode trocar esse code por tokens. PKCE vincula o code ao client que o gerou via criptografia — mesmo que o code seja capturado, o atacante não tem o `code_verifier` para completar a troca.

#### Client Credentials

Fluxo machine-to-machine: sem usuário humano, a aplicação autentica com suas próprias credenciais.

**Quando usar:** microsserviço que consome outra API interna, cronjob que acessa recursos protegidos, daemon de background.

```javascript
import { Issuer } from 'openid-client';

const issuer = await Issuer.discover('https://auth.example.com');
const client = new issuer.Client({
  client_id: process.env.CLIENT_ID,
  client_secret: process.env.CLIENT_SECRET,
});

// v5: client.grant() não processa nem valida a resposta como um TokenSet completo
// Troca credenciais por access token — sem redirect, sem usuário
const tokenSet = await client.grant({
  grant_type: 'client_credentials',
  scope: 'api:read api:write',
});

console.log(tokenSet.access_token);
```

#### Device Code

Para dispositivos sem browser (smart TVs, CLIs, IoT). O dispositivo exibe um código que o usuário digita em outro dispositivo (celular, computador).

**Quando usar:** CLI que precisa de autenticação do usuário, dispositivo embedded sem teclado, TV apps.

### openid-client v5

`openid-client` v5 usa named exports e API baseada em `Issuer` (discovery) e `Client` (operações).

#### Discovery e criação do client

```javascript
import { Issuer, generators } from 'openid-client';

// Discovery automático: busca /.well-known/openid-configuration
// e cria o Issuer com todos os endpoints e chaves públicas
const issuer = await Issuer.discover('https://accounts.google.com');

console.log('Issuer:', issuer.issuer);
console.log('Authorization endpoint:', issuer.authorization_endpoint);
console.log('Token endpoint:', issuer.token_endpoint);
console.log('JWKS URI:', issuer.jwks_uri);

// Cria o client com as credenciais da aplicação
const client = new issuer.Client({
  client_id: process.env.GOOGLE_CLIENT_ID,
  client_secret: process.env.GOOGLE_CLIENT_SECRET,
  redirect_uris: ['https://app.example.com/auth/callback'],
  response_types: ['code'],
});
```

#### Gerando a URL de autorização

```javascript
import { generators } from 'openid-client';

// PKCE: code_verifier é o segredo, code_challenge vai para o AS
const code_verifier = generators.codeVerifier();  // 43-128 chars random
const code_challenge = generators.codeChallenge(code_verifier); // SHA256(verifier) base64url

// state previne CSRF: valor aleatório que deve ser retornado pelo AS
const state = generators.state();

// nonce previne replay de ID Token (obrigatório em OIDC)
const nonce = generators.nonce();

const authUrl = client.authorizationUrl({
  scope: 'openid email profile',
  code_challenge,
  code_challenge_method: 'S256',
  state,
  nonce,
});

// Armazene code_verifier, state e nonce na sessão — necessários no callback
// session.code_verifier = code_verifier
// session.state = state
// session.nonce = nonce

console.log('Redirect to:', authUrl);
```

#### Callback: trocando o code por tokens

```javascript
import { Issuer, generators } from 'openid-client';

async function handleCallback(req, client) {
  // Parâmetros retornados pelo Authorization Server
  const params = client.callbackParams(req);

  // client.callback() faz a troca do code por tokens E valida o ID Token
  // - Verifica assinatura com chaves JWKS do issuer
  // - Verifica iss, aud, exp, iat, nonce
  // - Verifica state contra o valor da sessão
  const tokenSet = await client.callback(
    'https://app.example.com/auth/callback', // redirect_uri registrada
    params,
    {
      code_verifier: req.session.code_verifier, // valida PKCE
      state: req.session.state,                 // valida CSRF
      nonce: req.session.nonce,                 // valida replay
    }
  );

  console.log('ID Token claims:', tokenSet.claims());
  // { sub: 'user123', email: 'user@example.com', iss: '...', aud: '...', exp: ... }

  console.log('Access Token:', tokenSet.access_token);
  console.log('ID Token:', tokenSet.id_token);

  return tokenSet;
}
```

#### Buscando informações adicionais com UserInfo

```javascript
async function getUserInfo(client, tokenSet) {
  // UserInfo endpoint retorna claims adicionais sobre o usuário
  // Requer o access_token (não o id_token)
  const userinfo = await client.userinfo(tokenSet.access_token);

  // userinfo contém claims como: sub, email, email_verified, name, picture
  // O 'sub' deve bater com tokenSet.claims().sub — valide isso!
  if (userinfo.sub !== tokenSet.claims().sub) {
    throw new Error('UserInfo sub mismatch — possible token substitution attack');
  }

  return {
    id: userinfo.sub,
    email: userinfo.email,
    name: userinfo.name,
    picture: userinfo.picture,
    emailVerified: userinfo.email_verified,
  };
}
```

### Integração com Express

Exemplo completo com rotas de login, callback, sessão e proteção CSRF:

```javascript
import express from 'express';
import session from 'express-session';
import { Issuer, generators } from 'openid-client';

const app = express();

// Sessão necessária para armazenar state, nonce e code_verifier entre requests
app.use(session({
  secret: process.env.SESSION_SECRET,
  resave: false,
  saveUninitialized: false,
  cookie: {
    httpOnly: true,   // JavaScript não acessa o cookie
    secure: true,     // HTTPS obrigatório em produção
    sameSite: 'lax',  // Proteção básica contra CSRF
    maxAge: 10 * 60 * 1000, // 10 minutos — apenas para o fluxo de auth
  },
}));

// Discovery e criação do client (faça uma vez no startup)
let client;
async function initOIDC() {
  const issuer = await Issuer.discover(process.env.OIDC_ISSUER_URL);
  client = new issuer.Client({
    client_id: process.env.OIDC_CLIENT_ID,
    client_secret: process.env.OIDC_CLIENT_SECRET,
    redirect_uris: [process.env.OIDC_REDIRECT_URI],
    response_types: ['code'],
  });
}

// Rota de login: gera parâmetros de segurança e redireciona
app.get('/auth/login', (req, res) => {
  const code_verifier = generators.codeVerifier();
  const code_challenge = generators.codeChallenge(code_verifier);
  const state = generators.state();
  const nonce = generators.nonce();

  // Persiste na sessão para validar no callback
  req.session.oidc = { code_verifier, state, nonce };

  const authUrl = client.authorizationUrl({
    scope: 'openid email profile',
    code_challenge,
    code_challenge_method: 'S256',
    state,
    nonce,
  });

  res.redirect(authUrl);
});

// Rota de callback: valida, troca code por tokens, cria sessão de usuário
app.get('/auth/callback', async (req, res) => {
  try {
    const { code_verifier, state, nonce } = req.session.oidc ?? {};

    if (!code_verifier || !state || !nonce) {
      return res.status(400).send('Session expired or invalid');
    }

    const params = client.callbackParams(req);

    const tokenSet = await client.callback(
      process.env.OIDC_REDIRECT_URI,
      params,
      { code_verifier, state, nonce }
    );

    const userinfo = await client.userinfo(tokenSet.access_token);

    // Substitui a sessão de auth pela sessão de usuário autenticado
    delete req.session.oidc;
    req.session.user = {
      id: userinfo.sub,
      email: userinfo.email,
      name: userinfo.name,
    };

    res.redirect('/dashboard');
  } catch (err) {
    console.error('OIDC callback error:', err);
    res.status(500).send('Authentication failed');
  }
});

// Middleware de autenticação
function requireAuth(req, res, next) {
  if (!req.session.user) return res.redirect('/auth/login');
  next();
}

app.get('/dashboard', requireAuth, (req, res) => {
  res.json({ user: req.session.user });
});

initOIDC().then(() => app.listen(3000));
```

## OIDC: ID Token vs Access Token

### ID Token

O **ID Token** é um JWT assinado emitido pelo Authorization Server que contém **claims sobre o usuário**. Ele é destinado ao **client** (sua aplicação) para confirmar a identidade do usuário.

**Claims padrão do ID Token:**

| Claim | Tipo | Descrição |
|-------|------|-----------|
| `sub` | string | Subject: identificador único e estável do usuário no issuer |
| `iss` | string | Issuer: URL do Authorization Server que emitiu o token |
| `aud` | string/array | Audience: deve conter o `client_id` da sua aplicação |
| `exp` | number | Expiration: timestamp Unix de expiração (obrigatório validar) |
| `iat` | number | Issued At: timestamp de emissão |
| `nonce` | string | Valor enviado no request — previne replay attacks |
| `email` | string | Email do usuário (se scope `email` solicitado) |
| `name` | string | Nome completo (se scope `profile` solicitado) |
| `email_verified` | boolean | Se o email foi verificado pelo issuer |

**Validações obrigatórias do ID Token** (a `openid-client` faz automaticamente via `client.callback()`):

1. Verificar assinatura com as chaves JWKS do issuer
2. `iss` deve bater com o issuer descoberto
3. `aud` deve conter o `client_id` da aplicação
4. `exp` deve ser no futuro
5. `iat` deve ser no passado razoável (skew de ± 5 minutos)
6. `nonce` deve bater com o valor enviado na requisição

### Access Token

O **Access Token** é uma credencial que autoriza chamadas ao **Resource Server**. Ele é destinado às APIs que o usuário autorizou — não à sua aplicação.

**Diferenças críticas:**

| | ID Token | Access Token |
|--|----------|--------------|
| Destinatário | Client (sua app) | Resource Server (API) |
| Formato | JWT (sempre) | Opaco ou JWT |
| Contém identidade? | Sim (`sub`, `email`) | Às vezes, mas não garantido |
| Use para autenticar? | Sim | **Nunca** |
| Valide `aud`? | Sim — deve ser seu client_id | Depende da API |

### UserInfo Endpoint

O endpoint `/userinfo` retorna claims adicionais sobre o usuário autenticado. É acessado com o **access token** (não o ID Token):

```javascript
// GET /userinfo com Authorization: Bearer <access_token>
const userinfo = await client.userinfo(tokenSet.access_token);

// IMPORTANTE: valide que sub bate com o ID Token
// Previne token substitution attack
const idTokenClaims = tokenSet.claims();
if (userinfo.sub !== idTokenClaims.sub) {
  throw new Error('sub mismatch between UserInfo and ID Token');
}
```

## passport.js — alternativa simplificada

### passport-oauth2

O `passport-oauth2` oferece uma abstração mais simples para fluxos OAuth 2.0 básicos. É útil quando você não precisa do protocolo OIDC completo e quer integração direta com o middleware de autenticação do Express.

```javascript
import passport from 'passport';
import { Strategy as OAuth2Strategy } from 'passport-oauth2';

passport.use(new OAuth2Strategy(
  {
    authorizationURL: 'https://provider.example.com/oauth/authorize',
    tokenURL: 'https://provider.example.com/oauth/token',
    clientID: process.env.OAUTH_CLIENT_ID,
    clientSecret: process.env.OAUTH_CLIENT_SECRET,
    callbackURL: 'https://app.example.com/auth/callback',
    scope: ['read:user', 'user:email'],
    state: true,  // habilita CSRF protection automática
  },
  // verify callback: access_token já foi obtido
  async (accessToken, refreshToken, profile, done) => {
    try {
      // Busca ou cria usuário no banco
      const user = await User.findOrCreate({ oauthId: profile.id });
      return done(null, user);
    } catch (err) {
      return done(err);
    }
  }
));

// Serialize/deserialize para sessão
passport.serializeUser((user, done) => done(null, user.id));
passport.deserializeUser(async (id, done) => {
  const user = await User.findById(id);
  done(null, user);
});

// Rotas
app.get('/auth/github', passport.authenticate('oauth2'));
app.get('/auth/callback',
  passport.authenticate('oauth2', { failureRedirect: '/login' }),
  (req, res) => res.redirect('/dashboard')
);
```

### Passport vs openid-client: quando usar cada um

| Critério | passport-oauth2 | openid-client |
|----------|-----------------|---------------|
| Simplicidade | Alto — abstrações prontas | Médio — API mais explícita |
| Suporte OIDC completo | Limitado | Total |
| Validação de ID Token | Manual | Automática |
| PKCE | Sim (v1.5+, `pkce: true`) | Nativo |
| Discovery automático | Não | Sim |
| Flexibilidade | Menor | Maior |
| Ideal para | OAuth 2.0 simples, muitos providers via plugins | OIDC completo, ambientes corporativos, segurança rigorosa |

**Regra prática:** use `openid-client` quando estiver implementando OIDC em produção com requisitos de segurança (PKCE obrigatório, validação de nonce, múltiplos providers empresariais como Okta, Azure AD, Keycloak). Use `passport-oauth2` para prototipagem ou quando precisar de plugins prontos para providers populares (GitHub, Google, Facebook) com configuração mínima.

## Armadilhas

> [!danger] Não validar `state` abre CSRF no fluxo OAuth
> **Ataque:** o atacante cria uma URL de callback com seu próprio authorization code e engana a vítima a clicar nela. O servidor processa o code do atacante, autentica o atacante na conta da vítima — o atacante assume a sessão.
> **Por que funciona:** sem validar `state`, o servidor aceita qualquer callback sem verificar se o fluxo foi iniciado pelo usuário legítimo.
> **Fix:** gere `state` criptograficamente aleatório, armazene na sessão antes do redirect, e verifique `params.state === session.state` no callback. `openid-client` faz isso automaticamente quando você passa `state` para `client.callback()`.
>
> A mesma lógica vale para `aud` e `iss` no ID Token: não validar `aud` permite que um token emitido para outra aplicação seja aceito na sua; não validar `iss` permite tokens de issuers maliciosos. `openid-client` valida ambos automaticamente — mas se você decodificar o JWT manualmente com `jwt.decode()`, **você perde toda a validação**.

> [!danger] Open redirect no callback — valide `redirect_uri` estritamente
> **Ataque:** o atacante manipula o parâmetro `redirect_uri` para apontar para um domínio que controla. O Authorization Server emite o code para o domínio do atacante, que então o usa para obter tokens válidos.
> **Por que funciona:** Authorization Servers que fazem matching parcial da redirect_uri (ex: permite qualquer URL que comece com `https://app.example.com`) são vulneráveis a payloads como `https://app.example.com.evil.com/callback`.
> **Fix no AS:** registre URIs exatas (não prefixos) — o RFC 6749 exige matching exato. **Fix no client:** nunca aceite `redirect_uri` dinamicamente de parâmetros do request; use sempre a URI registrada hard-coded ou via variável de ambiente validada no startup. No Express, nunca faça `redirect_uri: req.query.redirect` — isso é um open redirect instantâneo.

> [!danger] Usar access token como ID Token — confusão de audiência
> **Problema:** o access token não tem `aud` garantido como o `client_id` da sua aplicação. Um access token pode ser obtido por outra aplicação e apresentado à sua — você não pode distinguir se foi emitido para você.
> **Regra:** nunca use `access_token` para determinar a identidade do usuário na sua aplicação. Use **sempre** o `id_token` (validado via `tokenSet.claims()`) ou o resultado do endpoint `/userinfo`, verificando que `sub` bate com o `sub` do ID Token.

## PKCE — geração de code_verifier e code_challenge

```javascript
import { generators } from 'openid-client';
import crypto from 'crypto';

// openid-client v5 — forma recomendada
const code_verifier = generators.codeVerifier();
// Resultado: string aleatória de 43-128 caracteres (base64url sem padding)
// Exemplo: "dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk"

const code_challenge = generators.codeChallenge(code_verifier);
// Resultado: BASE64URL(SHA256(ASCII(code_verifier)))
// Exemplo: "E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM"

// Equivalente manual (para entender o que acontece por baixo):
function manualCodeChallenge(verifier) {
  return crypto
    .createHash('sha256')
    .update(verifier)
    .digest('base64url'); // base64url, não base64 — sem padding, safe para URL
}

// No authorization request:
const authUrl = client.authorizationUrl({
  scope: 'openid email',
  code_challenge,
  code_challenge_method: 'S256', // sempre S256 — 'plain' é inseguro
  state: generators.state(),
  nonce: generators.nonce(),
});

// No token request (callback):
const tokenSet = await client.callback(redirectUri, params, {
  code_verifier, // AS recalcula SHA256 e compara com code_challenge
  state,
  nonce,
});
```

## Em entrevista

**Q: What is the difference between OAuth 2.0 and OIDC, and why does it matter?**

A: OAuth 2.0 is an authorization framework — it allows a user to delegate limited access to their resources to a third-party application without sharing credentials. The access token it produces is a capability token: it says what the holder can do, not who they are. OpenID Connect is an authentication protocol built on top of OAuth 2.0 — it adds the ID Token, a signed JWT that contains verified identity claims (sub, email, aud, iss, exp), and standardizes the UserInfo endpoint for fetching additional attributes. The distinction matters in security because using an access token to authenticate users is a well-known vulnerability: access tokens may be opaque, may not have a restricted audience, and can be issued in machine-to-machine flows with no user involved at all. If you use OAuth 2.0 alone for login, you have no cryptographic guarantee of who the user is — you need OIDC for that.

---

**Q: What is PKCE and why is it required for public clients?**

A: PKCE (Proof Key for Code Exchange, RFC 7636) is a mechanism that cryptographically binds an authorization code to the client that initiated the request. The client generates a random `code_verifier`, computes `code_challenge = BASE64URL(SHA256(code_verifier))`, and sends the challenge in the authorization request. When exchanging the code for tokens, the client sends the original `code_verifier` — the Authorization Server validates it by recomputing the hash. This prevents authorization code interception attacks: even if an attacker captures the authorization code (via browser history, referrer headers, or a malicious redirect), they cannot exchange it for tokens without the `code_verifier`. PKCE is required for public clients — SPAs and mobile apps — because they cannot securely store a `client_secret`. With a backend confidential client you still use PKCE as defense-in-depth; it is now recommended for all flows by OAuth 2.1.

---

**Q: What claims should you validate in an ID Token and why?**

A: The minimum required validations for an ID Token are: (1) **signature** — verify against the issuer's JWKS public keys to ensure the token was not tampered with; (2) **`iss`** — must match the exact issuer URL you discovered or configured, preventing tokens from a different Authorization Server being accepted; (3) **`aud`** — must contain your `client_id`, preventing tokens issued for another application from being used against yours (audience confusion attack); (4) **`exp`** — must be in the future, enforcing the token's time-limited validity; (5) **`nonce`** — must match the value you sent in the authorization request, preventing replay attacks where a captured ID Token is reused. Additionally, validate `iat` with a small clock skew tolerance (typically ±5 minutes). The `openid-client` library performs all these validations automatically in `client.callback()` — but if you decode the JWT manually with something like `jwt.decode()` without verifying, you lose all security guarantees entirely.

## Vocabulário

| Termo | Definição |
|-------|-----------|
| **OAuth 2.0** | Framework de autorização delegada (RFC 6749): permite que uma aplicação aja em nome de um usuário em outro serviço, com escopo e tempo de vida limitados |
| **OIDC (OpenID Connect)** | Protocolo de autenticação construído sobre OAuth 2.0: adiciona ID Token, UserInfo endpoint e Discovery para confirmar identidade do usuário |
| **Authorization Code** | Grant type OAuth 2.0 para apps com servidor backend: o AS emite um código temporário que é trocado por tokens em canal seguro |
| **PKCE** | Proof Key for Code Exchange (RFC 7636): mecanismo criptográfico que vincula um authorization code ao cliente, prevenindo interceptação em clients públicos |
| **ID Token** | JWT assinado emitido pelo Authorization Server contendo claims de identidade do usuário (`sub`, `iss`, `aud`, `exp`, `nonce`); destinado ao client |
| **Claims** | Afirmações sobre uma entidade (usuário, aplicação) transportadas em um token JWT; podem ser registradas (RFC padrão), públicas ou privadas |
| **State** | Parâmetro aleatório gerado pelo client e retornado pelo AS no callback; previne CSRF no fluxo OAuth 2.0 |
| **Nonce** | Valor aleatório incluído no ID Token pelo AS; o client verifica que bate com o valor enviado na requisição, prevenindo replay attacks |
| **Access Token** | Credencial que autoriza acesso ao Resource Server; não garante identidade do usuário e não deve ser usado para autenticação |
| **UserInfo endpoint** | Endpoint padronizado pelo OIDC que retorna claims adicionais do usuário autenticado; acessado com o access token |
| **Discovery** | Mecanismo OIDC para descoberta automática de metadados do issuer via `/.well-known/openid-configuration`; implementado via `Issuer.discover()` |
| **Client Credentials** | Grant type OAuth 2.0 para comunicação machine-to-machine; não envolve usuário humano |

## Veja também

- [[03-Dominios/Node/Segurança/index|Segurança]] — índice do galho, trilha completa de segurança Node
- [[JavaScript/Backend/Node.js|Node.js]] — tronco da trilha Node Senior
- [[03-Dominios/Node/Segurança/04 - JWT e autenticação com jsonwebtoken|JWT e autenticação com jsonwebtoken]] — nota anterior: tokens JWT, sign/verify, access + refresh
- [[03-Dominios/Node/Segurança/06 - RBAC e ABAC com casl e casbin|RBAC e ABAC com casl e casbin]] — nota seguinte: autorização granular
- [openid-client no npm](https://www.npmjs.com/package/openid-client) — documentação oficial da biblioteca
- [RFC 6749 — OAuth 2.0](https://datatracker.ietf.org/doc/html/rfc6749) — especificação original
- [RFC 7636 — PKCE](https://datatracker.ietf.org/doc/html/rfc7636) — Proof Key for Code Exchange
- [OpenID Connect Core 1.0](https://openid.net/specs/openid-connect-core-1_0.html) — especificação OIDC
