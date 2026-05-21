---
title: "Segurança"
created: 2026-05-12
updated: 2026-05-12
type: moc
status: growing
publish: true
progresso: andamento
tags:
  - node
  - segurança
  - moc
aliases:
  - Segurança Node
  - Node Security
---

# Segurança

> [!abstract] TL;DR
> Galho 8 da trilha Node Senior. Segurança em Node.js vai muito além de "usar HTTPS": começa na supply chain — npm audit, lockfiles e ferramentas como socket.dev detectam typosquatting e dependency confusion antes que o pacote malicioso chegue à produção. Segredos jamais vivem em código; o padrão moderno é validar variáveis de ambiente com Zod e injetar valores via AWS Secrets Manager, Vault ou Doppler. Inputs externos são validados com Zod ou Joi para eliminar injection e ReDoS; autenticação é feita com JWT (HS256/RS256, access + refresh + blacklist Redis) ou OAuth 2.0 / OIDC com PKCE via openid-client v5. Autorização granular usa RBAC com casl v6 ou ABAC com casbin seguindo o princípio de least privilege. Rate limiting com express-rate-limit e Redis store protege contra brute force usando fixed/sliding window e token bucket com headers RFC 6585. Helmet.js aplica de uma vez CSP, HSTS, CORS, X-Frame-Options e Referrer-Policy. O galho fecha com o OWASP Top 10 mapeado para Node (BOLA, SSRF, IDOR, misconfiguration) e um decision tree consolidado para uso em code review e entrevista.

## Sobre este galho

Este galho cobre a **camada de segurança** de aplicações Node.js modernas — da supply chain ao hardening HTTP, passando por autenticação, autorização e validação de entrada. O objetivo não é listar CVEs, mas construir o **modelo mental de defesa em profundidade**: como as ameaças se encadeiam, quais controles bloqueiam cada vetor de ataque, e como comunicar essas decisões em inglês técnico durante uma entrevista senior.

O escopo inclui: supply chain security (npm audit, lockfiles, socket.dev), gerenciamento de segredos (process.env, Vault, Doppler), validação de entrada com Zod e Joi, autenticação com JWT e OAuth 2.0/OIDC, autorização com RBAC/ABAC, rate limiting com Redis, hardening HTTP com Helmet.js e OWASP Top 10 aplicado a Node.js.

**Audiência primária:** dev senior em preparação para entrevista internacional. Cada nota inclui seção "Em entrevista" com frase pronta em inglês e vocabulário PT→EN para discussão técnica fluente.

**Audiência secundária:** dev implementando ou auditando segurança em APIs Node.js em produção — que precisa de um mapa coerente do que proteger e com quais ferramentas.

**Pré-requisitos:**
- [[JavaScript/Backend/Node.js|Node.js]] — tronco da trilha, conceitos fundamentais de Node
- [[03-Dominios/Node/Runtime e Event Loop/index|Runtime e Event Loop]] — galho 1, modelo mental de event loop e async
- [[03-Dominios/Node/Frameworks e arquitetura/index|Frameworks e arquitetura]] — galho 4, Express e Fastify como base para middleware de segurança

## Comece por aqui — trilha completa (10 notas)

### Bloco A — Supply chain e segredos

| # | Nota | O que você aprende |
|---|------|--------------------|
| 1 | [[01 - Supply chain attacks e npm audit]] | npm audit, typosquatting, dependency confusion, lockfile, socket.dev |
| 2 | [[02 - Segredos e variáveis de ambiente]] | process.env, .env, AWS Secrets Manager, Vault, Doppler, validação com Zod |

### Bloco B — Validação e autenticação

| # | Nota | O que você aprende |
|---|------|--------------------|
| 3 | [[03 - Validação de entrada com Zod e Joi]] | Schema validation, parse/safeParse, middleware Express/Fastify, ReDoS |
| 4 | [[04 - JWT e autenticação com jsonwebtoken]] | sign/verify, HS256/RS256, access + refresh token, blacklist Redis |
| 5 | [[05 - OAuth 2.0 e OIDC com openid-client]] | Authorization Code + PKCE, OIDC, ID Token, openid-client v5 |

### Bloco C — Autorização e controle de acesso

| # | Nota | O que você aprende |
|---|------|--------------------|
| 6 | [[06 - RBAC e ABAC com casl e casbin]] | RBAC, ABAC, casl v6, casbin, least privilege |

### Bloco D — Hardening e proteção HTTP

| # | Nota | O que você aprende |
|---|------|--------------------|
| 7 | [[07 - Rate limiting com express-rate-limit]] | Fixed/sliding window, token bucket, Redis store, RFC 6585 headers |
| 8 | [[08 - Helmet.js e hardening HTTP]] | CSP, HSTS, CORS, X-Frame-Options, Referrer-Policy |

### Bloco E — OWASP e fechamento

| # | Nota | O que você aprende |
|---|------|--------------------|
| 9 | [[09 - OWASP Top 10 para Node]] | A01-A10, BOLA, injection, SSRF, IDOR, misconfiguration |
| 10 | [[10 - Cheatsheet e decision tree de segurança]] | Decision tree consolidado, tabela comparativa, checklist de PR |

## Rotas alternativas

> [!tip] Rota entrevista (01 → 04 → 05 → 09 → 10)
> Foco nas perguntas mais cobradas em entrevistas senior: supply chain, JWT vs OAuth, OWASP Top 10 e o decision tree de segurança. Cobre os vetores de ataque mais discutidos em ~5 notas.

> [!tip] Rota hardening de API (02 → 03 → 07 → 08 → 10)
> Para quem precisa blindar uma API existente: segredos bem gerenciados, validação de input, rate limiting e headers HTTP corretos — cinco notas que eliminam a maioria das vulnerabilidades de configuração.

> [!tip] Rota auth completa (04 → 05 → 06)
> Para quem implementa autenticação e autorização do zero: JWT com rotação de tokens, OAuth 2.0 / OIDC com PKCE e controle de acesso RBAC/ABAC em sequência lógica.

> [!tip] Rota OWASP Top 10 (09 → 01 → 03 → 08)
> Para quem precisa mapear vulnerabilidades para controles concretos: começa pelo framework OWASP e depois associa cada categoria (injection, supply chain, misconfiguration) à nota específica que a trata.

## Todas as notas

```dataview
TABLE status, updated
FROM "03-Dominios/Node/Segurança"
WHERE type = "concept"
SORT file.name ASC
```

## Veja também

- [[JavaScript/Backend/Node.js|Node.js]] — tronco da trilha Node Senior
- [[03-Dominios/Node/index|Node.js (MOC central)]] — visão geral de todos os galhos
- [[03-Dominios/Node/Frameworks e arquitetura/index|Frameworks e arquitetura]] — galho 4, base para middlewares de segurança
- [[03-Dominios/Node/Tooling e ecossistema moderno/index|Tooling e ecossistema moderno]] — galho 7, supply chain e package managers
