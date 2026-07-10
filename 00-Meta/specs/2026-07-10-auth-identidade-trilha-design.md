---
title: "Design Spec — Trilha Auth e Identidade"
created: 2026-07-10
type: meta
publish: false
tags:
  - meta
  - spec
  - auth-identidade
---

# Design Spec — Trilha Auth e Identidade

> Cobertura ausente (🚫) do [[00-Meta/Roadmap]] — "Auth & Identidade (OAuth2/OIDC/JWT/sessões): espalhado em Segurança; merece foco". Quarta trilha da família Engenharia pós-System Design: **System Design** (desenha) → **Operação** (opera) → **Comunicação** (contrata) → **Auth e Identidade** (quem pode o quê).

## Ponto de vista (pedido do usuário 2026-07-10)

Trilha **conceito → protocolo → decisão → implementação guiada**. Diferente da Comunicação (que proibiu tutorial por stack), aqui o usuário pediu **explicitamente** implementação nos stacks: Python (Django e FastAPI), Java (Spring Boot), Node (Express e NestJS), Go (Gin — framework dominante, ~48% de uso) e **Keycloak** como IdP self-hosted. A exceção à regra "sem tutorial" é deliberada e vale só para o sub-galho 4/5.

Regra de honestidade das notas de stack: onde a trilha da linguagem já cobre o assunto profundamente (Java/Segurança = 18 notas de Spring Security; Node/Segurança = JWT/OIDC/casl), a nota daqui é **ponte + o que falta lá** (Keycloak, passkeys, Authorization Server), nunca re-tutorial.

## Pesquisa web (2026-07-10) — estado do tema

- **OAuth 2.1**: draft-15 (mar/2026), tecnicamente estável e amplamente adotado. Consolida RFC 6749 + PKCE (7636) + Security BCP (RFC 9700). **PKCE obrigatório para todo authorization code flow** (não só public clients); implicit flow e password grant **removidos**; refresh token rotation/sender-constraining para public clients. "Se você escreve OAuth novo em 2026, escreve OAuth 2.1."
- **Passkeys/WebAuthn**: 2026 é o ano em que passkeys viram default para apps novas — plataforma estável, tooling maduro, 75% de awareness (FIDO World Passkey Day Report). Estratégia prática: rodar ao lado de senhas, não substituir de uma vez.
- **Keycloak**: linha 26.x — estável 26.6.4 (jun/2026), 26.7.0 lançado jul/2026. Passkeys oficiais desde 26.4 (conditional/modal UI, discoverable credentials); **Organizations** (multi-tenancy B2B dentro de um realm) maduro, admin roles por organização no 26.7; SCIM API (preview) e multi-cluster HA sem cache externo (preview) no 26.7.
- **Go**: Gin é o framework dominante (~48%; Gorilla 17%, Echo 16%, Fiber 11%) — nota Go usa **Gin** + `coreos/go-oidc` + `golang-jwt`.
- **Node**: Passport ainda é o middleware mais usado (500+ strategies) mas é low-level; **better-auth** (que hoje mantém o Auth.js) é a aposta moderna. Express = sessões/Passport/better-auth; NestJS = guards + @nestjs/passport + @nestjs/jwt.
- **Python**: Django = contrib.auth/sessions + django-allauth (agora com provider OIDC) + DRF/SimpleJWT; FastAPI = fastapi.security (OAuth2PasswordBearer) + PyJWT/Authlib + passlib (argon2/bcrypt), revogação via denylist Redis ou short-lived + rotation.
- **Autorização fine-grained**: consenso 2026 = híbrido **RBAC (coarse) + ReBAC (resource-level)** em B2B SaaS. Zanzibar (Google) como paper seminal; implementações: OpenFGA (CNCF incubating), SpiceDB, Permify, Ory Keto; policy-as-code: OPA/Rego, Cedar (AWS).
- **Spring Security**: 6.x com suporte nativo a passkeys/WebAuthn e one-time tokens (6.4+); Spring Authorization Server já incorpora as recomendações OAuth 2.1; docs de Token Exchange (RFC 8693) em 2026.

## Contexto: o que já existe (fronteiras!)

- `Engenharia/Segurança/` 12 (Autenticação) e 13 (Autorização) — **conceito neutro**; ganham callout apontando pra cá. Cripto (hash 06, assinaturas 10, PKI 11) mora lá — linkar, não reexplicar.
- `Tecnologia/Java/Segurança/` — **18 notas de Spring Security** (filter chain, UserDetailsService, BCrypt/Argon2, JWT 08, resource server 09, OAuth2/OIDC client + grants 12, refresh/revogação 13, RBAC vs ABAC 14, capstone). A nota Spring daqui é ponte + lacunas (Spring Authorization Server, passkeys/OTT 6.4+, integração Keycloak).
- `Tecnologia/Node/Segurança/` — JWT com jsonwebtoken (04), OAuth/OIDC com openid-client (05), RBAC/ABAC com casl/casbin (06). A nota Express daqui aproveita e completa (sessões production-grade, better-auth, integração Keycloak); NestJS não tem cobertura em lugar nenhum → nota completa.
- `Tecnologia/Python/` — trilha em construção (galho 5 em andamento, outra sessão); auth não estará coberta lá tão cedo → notas Django/FastAPI completas aqui. Sinalizar no roadmap da trilha Python que auth mora aqui.
- `Tecnologia/Go/` — stub; nota Gin completa aqui, mesma sinalização.
- `Comunicação entre Sistemas/` SG2-03 — panorama de auth de API (decisão); linka pra cá como deep-dive.
- **API keys/mTLS/rate limiting**: mTLS conceitual em Segurança 11/14; rate limiting em System Design/Comunicação — mencionar, não aprofundar.

## Onde mora

`03-Dominios/Engenharia/Auth e Identidade/` — domínio novo em Engenharia, irmão de Comunicação entre Sistemas. Protocolo/decisão é disciplina neutra; os sub-galhos de stack são a instrumentação (exceção deliberada, como Testes JS instrumenta Engenharia/Testes — mas aqui dentro do mesmo galho, por pedido do usuário).

## Estrutura de pastas

```
Engenharia/Auth e Identidade/
├── index.md                        (MOC do galho-pai, novo)
├── roadmap.md                      (roadmap recursivo, novo)
├── 1 - Fundamentos de identidade/   (Iniciado)
├── 2 - OAuth 2.1 e OpenID Connect/  (Adepto)
├── 3 - Autorização e multi-tenancy/ (Adepto→Magus)
├── 4 - Auth nos stacks/             (Magus)
└── 5 - Keycloak/                    (Magus)
+ capstone no galho-pai (Magus)
```

## Roster de notas

### Sub-galho 1 — Fundamentos de identidade (Iniciado, 5 notas)

> O vocabulário e os blocos: o que é identidade digital, como se prova, onde vive.

| # | Nota | Escopo | Fronteira / cross-link |
|---|------|--------|------------------------|
| 01 | Identidade, autenticação e autorização — o mapa | IAM como disciplina; AuthN vs AuthZ vs accounting; fatores (something you know/have/are); identidade como produto (CIAM vs workforce). | instrumenta Segurança 12/13 |
| 02 | Sessões e cookies — auth stateful | Session ID server-side, cookie flags (HttpOnly/Secure/SameSite), CSRF e por que SameSite não basta, session fixation, stores (Redis), quando sessão ainda é a resposta certa (spoiler: quase sempre em web tradicional). | linka Plataforma Web/Storage; Segurança 12 |
| 03 | JWT e a família de tokens | Anatomia (header/payload/signature), JWS vs JWE, algoritmos (HS256/RS256/ES256/EdDSA), claims registradas, JWKS e rotação de chave, armadilhas clássicas (alg=none, kid injection, storage no browser), stateless vs revogável. | linka Segurança 10 (assinaturas); Java/Seg 08; Node/Seg 04 |
| 04 | Senhas e MFA — o legado que não morre | Hashing moderno (argon2id > bcrypt; nunca MD5/SHA puro), políticas NIST 800-63B (comprimento > complexidade, sem rotação forçada), credential stuffing/breach detection, TOTP, por que SMS é fraco, account recovery como elo fraco. | linka Segurança 06 (hashing) |
| 05 | Passkeys e WebAuthn — o presente sem senha | FIDO2/CTAP2+WebAuthn, cerimônias de registro/autenticação, discoverable credentials, synced (iCloud/Google/1Password) vs device-bound, phishing-resistance, estratégia de rollout gradual 2026. | fecha SG1; prepara Keycloak passkeys |

### Sub-galho 2 — OAuth 2.1 e OpenID Connect (Adepto, 6 notas)

> Os protocolos que o mercado fala. Baseline OAuth 2.1 (draft-15) — ensinar direto o mundo pós-implicit.

| # | Nota | Escopo | Fronteira / cross-link |
|---|------|--------|------------------------|
| 01 | OAuth — o problema da delegação | Por que existe (a era da senha compartilhada), papéis (resource owner/client/AS/RS), scopes, história 1.0→2.0→2.1, **"OAuth não é autenticação"** (o erro clássico). | enquadra o SG |
| 02 | Authorization Code + PKCE — o fluxo canônico | O fluxo passo a passo (com Mermaid sequence), PKCE (code_verifier/challenge) e por que virou obrigatório pra todos, exact redirect URI matching, state/nonce, a morte do implicit e do password grant. | núcleo do SG |
| 03 | OpenID Connect — identidade sobre OAuth | ID token vs access token, claims e scopes padrão (profile/email), discovery (/.well-known), userinfo, logout (RP-initiated, back-channel), OIDC vs SAML (quando cada um). | linka SG2-06 |
| 04 | Grants de máquina e fluxos especiais | Client credentials (M2M), device authorization flow (TVs/CLIs), token exchange (RFC 8693, delegação entre serviços), sender-constrained tokens (mTLS, DPoP). | linka Java/Seg 12 |
| 05 | Tokens em produção | Access curto + refresh rotation, detecção de reuse, revogação (denylist vs introspection RFC 7662), opaque vs JWT no RS, **onde guardar token no browser** (memória vs cookie; localStorage não) e o **padrão BFF** como resposta 2026 pra SPAs. | linka Java/Seg 13; Node/Seg 04 |
| 06 | SSO corporativo — SAML, federação e SCIM | Por que SAML não morreu (enterprise B2B), assertions/IdP-initiated vs SP-initiated, federação de identidade, provisioning com SCIM 2.0, "enterprise readiness" (SSO tax). | fecha SG2; prepara Keycloak Organizations |

### Sub-galho 3 — Autorização e multi-tenancy (Adepto→Magus, 4 notas)

> Autenticado ≠ autorizado. Os modelos de "quem pode o quê" e o corte B2B.

| # | Nota | Escopo | Fronteira / cross-link |
|---|------|--------|------------------------|
| 01 | RBAC, ABAC e ReBAC — os três modelos | Roles agregam, atributos avaliam, relacionamentos caminham grafo; limites do RBAC (role explosion), quando cada um; consenso 2026: híbrido RBAC coarse + ReBAC fine em B2B SaaS. | aprofunda Segurança 13; linka Java/Seg 14, Node/Seg 06 |
| 02 | Fine-grained authorization — Zanzibar e policy-as-code | O paper Zanzibar (tuplas objeto-relação-usuário), OpenFGA/SpiceDB/Ory Keto, policy-as-code com OPA/Rego e Cedar, decisão centralizada vs embutida, latência do check. | Magus; linka Operação (sidecar/gateway) |
| 03 | Multi-tenancy e organizações | Tenant como fronteira de identidade: orgs, convites, membership, roles por organização, isolamento (realm/org/schema), o modelo B2B SaaS (usuário em N orgs). | prepara Keycloak Organizations |
| 04 | Autorização de API na prática | Scopes vs permissions vs roles no token (claims design), enforcement no gateway vs no serviço, propagação de identidade entre microserviços (token exchange/headers assinados), audit trail. | fecha SG3; linka Comunicação SG2-03 |

### Sub-galho 4 — Auth nos stacks (Magus, 6 notas)

> A exceção deliberada: implementação guiada, uma nota por stack. Formato comum: mapa das opções do ecossistema → fluxo recomendado 2026 (sessão web + API com OIDC) → código essencial (não boilerplate) → integração com IdP externo (ponte pro SG5) → armadilhas do stack.

| # | Nota | Escopo | Fronteira / cross-link |
|---|------|--------|------------------------|
| 01 | Java — Spring Security e Spring Authorization Server | **Nota-ponte**: mapa das 18 notas de Java/Segurança (não reexplicar) + o que falta lá: Spring Authorization Server (ser o IdP), passkeys/WebAuthn e one-time tokens (6.4+), token exchange, integração Keycloak como resource server/client. | **ponte** → Java/Segurança 01-18 |
| 02 | Python — Django | contrib.auth e o modelo de sessão, django-allauth (social + MFA + provider OIDC), DRF com SimpleJWT, custom User model (a decisão irreversível), async e auth. | trilha Python não cobre auth; sinalizar lá |
| 03 | Python — FastAPI | fastapi.security e DI de auth (Depends), OAuth2PasswordBearer, PyJWT/Authlib, passlib (argon2), validação de token OIDC de IdP externo, revogação (Redis denylist vs short-lived+rotation), scopes por endpoint. | idem |
| 04 | Node — Express | Sessões production-grade (express-session + Redis, SameSite), Passport (quando ainda faz sentido) vs **better-auth**/Auth.js, openid-client pra OIDC — **completa** Node/Seg 04/05 sem repetir. | **ponte parcial** → Node/Segurança 04/05/06 |
| 05 | Node — NestJS | Guards e o request lifecycle, @nestjs/passport + strategies, @nestjs/jwt, decorators (@Roles + RolesGuard), auth em GraphQL/WebSocket, testing de guards. | cobertura inédita no vault |
| 06 | Go — Gin | Middleware chain do Gin, golang-jwt/jwt v5, coreos/go-oidc pra validar tokens de IdP, sessões (gorilla/sessions ou scs), goth pra social login, o idioma Go de auth (explícito, sem magia de framework). | trilha Go não existe; sinalizar no Roadmap |

### Sub-galho 5 — Keycloak (Magus, 3 notas)

> O IdP self-hosted de referência (pedido explícito). Baseline Keycloak 26.x.

| # | Nota | Escopo | Fronteira / cross-link |
|---|------|--------|------------------------|
| 01 | Keycloak — realms, clients e flows | Por que um IdP pronto (build vs buy), arquitetura (realm/client/user/role/group), authentication flows customizáveis, admin console e Admin API, temas. | usa SG2 inteiro |
| 02 | Keycloak em produção | Organizations (multi-tenancy B2B, 26.x), passkeys (26.4+), SCIM provisioning (26.7 preview), HA/clustering (Infinispan; multi-cluster preview 26.7), atrás de reverse proxy, upgrade strategy, SPI/extensões, quando Keycloak é overkill (Auth0/Cognito/Zitadel). | linka Operação (rodar em prod) |
| 03 | Integrando os stacks com Keycloak | Um fluxo de referência (SPA+BFF+API) com Keycloak como AS: Spring resource server, FastAPI validando via JWKS, NestJS/Express como client OIDC, Gin com go-oidc — fecha o loop SG4↔SG5 com tabela comparativa. | costura SG4; quase-capstone |

### Capstone (Magus, galho-pai)

**"Desenhando a identidade de um SaaS B2B do zero"** — walkthrough decisório: build vs buy (Keycloak vs Auth0/Cognito vs better-auth embutido), sessão vs token vs BFF, social + passkeys + senha (estratégia de rollout), SSO/SAML/SCIM pro cliente enterprise, RBAC+ReBAC por organização, MFA. Costura os 5 sub-galhos. Nunca fabricar experiência do usuário ([[feedback_no_fabrication]]).

**Total planejado:** 5+6+4+6+3 = 24 notas + 1 capstone = **25 notas**.

## Fronteiras anti-duplicação

| Tópico | Papel aqui | Mora em | Regra |
|--------|-----------|---------|-------|
| Autenticação/autorização conceitual | deep-dive de protocolo | Segurança 12/13 | lá ganha callout pra cá |
| Hashing, assinaturas, PKI, mTLS | uso, não teoria | Segurança 06/10/11/14 | linkar, não reexplicar |
| Spring Security (filter chain, JWT, resource server, grants) | ponte + lacunas | Java/Segurança 01-18 | SG4-01 é mapa, não re-tutorial |
| JWT/OIDC/casl em Node | completar, não repetir | Node/Segurança 04/05/06 | SG4-04 é ponte parcial |
| Auth de API como decisão de contrato | deep-dive | Comunicação SG2-03 (panorama) | lá linka pra cá |
| Rate limiting, gateway | menção | System Design / Comunicação | linkar |
| Segurança de sessão web (XSS/CSRF geral) | só o que toca auth | Plataforma Web, OWASP nas trilhas | linkar |
| Rodar Keycloak em K8s/observabilidade | menção | Operação | linkar |

## Padrão de escrita (herdado de System Design/Operação/Comunicação)

Nota = capítulo de livro ([[feedback_padrao_capitulo_livro]]): TL;DR `[!abstract]`, abertura problema-first, divulgação progressiva, exemplo trabalhado. Densidade ~440-540 linhas ([[feedback_notas_profundas_diagramas]]). `fase:` no frontmatter. ≥1 Mermaid (paleta azul `#4A90D9` / âmbar `#F5A623` / vermelho `#D0021B` — fluxos OAuth pedem sequenceDiagram). Callouts `[!question]-`/`[!warning]`. "Em entrevista" + "How to explain in English" (tabela PT↔EN). "O que vem a seguir". `## Fontes` datadas. **SG4/SG5: código essencial permitido (exceção deliberada), mas mínimo que ensina o fluxo — não boilerplate de projeto.** `[!info]` de caducidade nas notas com versão cravada (Keycloak 26.x, better-auth, Spring Security 6.4+, OAuth 2.1 draft-15).

## Fontes canônicas da trilha

- **Specs/RFCs:** OAuth 2.1 draft-ietf-oauth-v2-1-15, RFC 9700 (Security BCP), RFC 7636 (PKCE), RFC 8693 (Token Exchange), RFC 7662 (Introspection), OpenID Connect Core 1.0, WebAuthn Level 3 (W3C), SCIM (RFC 7643/7644), NIST 800-63B.
- **Livros:** *OAuth 2 in Action* (Richer/Sanso); *API Security in Action* (Neil Madden); *Solving Identity Management in Modern Applications* (Wilson/Hingnikar).
- **Docs:** oauth.net/2.1, Keycloak docs (26.x), Spring Security reference, django-allauth, FastAPI security tutorial, better-auth, Passport, NestJS security recipes, coreos/go-oidc, OpenFGA docs, webauthn.guide.

## Plano de execução (ritmo B, igual às trilhas irmãs)

1. Criar domínio: `index.md` (MOC) + `roadmap.md` do galho-pai.
2. Semear sub-galho a sub-galho, ordem 1→2→3→4→5. Cada subpasta: `index.md` + `roadmap.md` + notas via subagente-por-nota (≤3/onda, Sonnet, EXEMPLAR = nota 01 do System Design até a 01 daqui virar exemplar próprio; WebSearch inline; barra de densidade explícita).
3. Ao fechar cada sub-galho: roadmap-folha + roadmap-pai + commit (paths explícitos, sem Co-Authored-By, push manual).
4. Fechamento: capstone; callouts em Segurança 12/13 e Comunicação SG2-03; atualizar [[00-Meta/Roadmap]] (🚫→🟢, seção Engenharia + coberturas ausentes); atualizar memória.

## Pontos em aberto

- **Ritmo por sessão**: 25 notas ≈ 4-5 sessões (1-2 sub-galhos/sessão), colidindo com a trilha Python em andamento (1 galho/sessão) — intercalar ou serializar fica a critério do usuário.
- **better-auth vs Passport na nota Express**: pesquisa aponta better-auth como aposta moderna; validar profundidade na escrita (ecossistema Node muda rápido — caducidade explícita).
- **SG3-02 (OpenFGA/Zanzibar)**: se crescer demais, candidato a broto (`fase: Magus`) em vez de nota core.
