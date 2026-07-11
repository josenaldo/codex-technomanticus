---
title: "Roadmap — Auth nos stacks"
created: 2026-07-11
type: meta
publish: false
tags:
  - meta
  - roadmap
  - auth-identidade
---

# Roadmap — Auth nos stacks (sub-galho 4)

Roadmap-folha do sub-galho `Auth e Identidade/4 - Auth nos stacks`. Fase **Magus** (densidade ~6-7k palavras/nota). **Exceção deliberada à regra "sem tutorial"**: código essencial permitido, mínimo que ensina o fluxo — não boilerplate. Spec: [[00-Meta/specs/2026-07-10-auth-identidade-trilha-design]].

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 6 |
| ⬜ pendente | 0 |
| ✅ feita | 6 |
| 🔄 em andamento | 0 |
| % concluído | 100% ✅ |

---

## Notas

#### 01 - Java — Spring Security e Spring Authorization Server   [substantivo]
- **Estado:** ✅ feita (2026-07-11) · fase: Magus · **NOTA-PONTE**
- **Escopo:** mapa tabular das 18 notas de Java/Segurança (só wikilinks, não reexplica) + o que falta lá: Spring Authorization Server (ser o IdP — RegisteredClient/SecurityFilterChain), passkeys/WebAuthn `webAuthn()` DSL (6.4+), one-time tokens (6.4+), token exchange (RFC 8693), Keycloak nos 2 papéis (resource server + client). Exemplo com 2 cenários (validar token Keycloak vs virar AS próprio).
- **Resultado:** 371 linhas / ~4.850 palavras; 3 Mermaid, 15 fontes, `[!info]` caducidade. Versões: Spring Authorization Server 1.5.x, Spring Security 6.4/6.5, Keycloak 26.x. **Débito leve:** palavras abaixo do alvo (nota-ponte é mais enxuta por design — parte do valor é a curadoria do mapa).

#### 02 - Python — Django   [substantivo]
- **Estado:** ✅ feita (2026-07-11) · fase: Magus
- **Escopo:** contrib.auth + modelo de sessão (default battle-tested); custom User model como decisão do dia 1 (AbstractUser vs AbstractBaseUser, AUTH_USER_MODEL quase irreversível); DRF em 3 vias (SessionAuth, SimpleJWT, mozilla-django-oidc); django-allauth (social/MFA/OIDC provider/headless); Group/Permission como RBAC nativo; async e auth. Exemplo: painel interno via sessão + app mobile via Keycloak/OIDC.
- **Resultado:** 403 linhas / ~5.000 palavras; 3 Mermaid, 15 fontes (formato lista). Versões: Django 5.x/6.0 docs, allauth 65.18.0. Código essencial (custom User, settings allauth/SimpleJWT, permission class).

#### 03 - Python — FastAPI   [substantivo]
- **Estado:** ✅ feita (2026-07-11) · fase: Magus
- **Escopo:** DI como mecanismo de auth (Depends aninhado, get_current_user); OAuth2PasswordBearer; PyJWT como validador puro vs Authlib (cliente OAuth completo, depende de SessionMiddleware); pwdlib substituindo passlib (doc oficial migrou); validação JWKS contra Keycloak (PyJWKClient); scopes via Security(...); revogação (denylist Redis vs short-lived+rotation). Contraste com Django (baterias vs monte-você-mesmo).
- **Resultado:** 411 linhas / ~4.871 palavras; 4 Mermaid, ~15 fontes. **Achado:** python-jose sem release e com CVEs abertos → reforça PyJWT. Código essencial (OAuth2PasswordBearer, hash pwdlib, dependency, JWKS).

#### 04 - Node — Express   [substantivo]
- **Estado:** ✅ feita (2026-07-11) · fase: Magus · **NOTA-PONTE PARCIAL**
- **Escopo:** mapa curto do que está em Node/Seg 04/05/06 (wikilinks) + o núcleo novo: express-session + connect-redis production-grade (SameSite/rolling/regenerate contra fixation); panorama de libs 2026 (Passport low-level vs better-auth moderno — que hoje mantém o Auth.js desde set/2025); Express como OIDC client do Keycloak (reusa openid-client; keycloak-connect deprecado).
- **Resultado:** 412 linhas / ~4.400 palavras; 3 Mermaid, 15 fontes, `[!info]` caducidade (Node volátil). Versões: better-auth 1.6.x. **Débito leve:** palavras enxutas por design (ponte parcial — evita duplicar Node/Seg).

#### 05 - Node — NestJS   [substantivo]
- **Estado:** ✅ feita (2026-07-11) · fase: Magus
- **Escopo:** request lifecycle (middleware→guards→interceptors→pipes) e onde auth entra; Guards/CanActivate; @nestjs/passport + strategies; @nestjs/jwt (emissão); @Roles + RolesGuard + Reflector; @CurrentUser; @Public()/APP_GUARD; Keycloak via jwt strategy/JWKS; GraphQL (GqlExecutionContext) e WebSocket (limitação de handshake); testing de guards (valor da DI). Contraste com Express (estrutura opinada + testável).
- **Resultado:** 502 linhas / ~5.560 palavras; 2 Mermaid, 15 fontes. Versões: NestJS 11.x. Código essencial (JwtStrategy, RolesGuard, decorator, guard em resolver).

#### 06 - Go — Gin   [substantivo]
- **Estado:** ✅ feita (2026-07-11) · fase: Magus · **FECHA o sub-galho**
- **Escopo:** middleware chain do Gin (c.Next/Abort/Set/Get); golang-jwt/jwt v5 com a armadilha do `alg` (algorithm confusion, CVE 2026); coreos/go-oidc (discovery/JWKS/Keycloak); sessões (gorilla arquivado→reativado vs alexedwards/scs); goth pra social login; o idioma Go de auth (explícito, erros como valores, sem DI mágico). Sinaliza que auth-em-Go mora aqui (trilha Go não existe).
- **Resultado:** 425 linhas / ~5.730 palavras; 3 Mermaid, 15 fontes, `[!info]` caducidade. Versões: golang-jwt v5, go-oidc v3, Gin ~48% mercado. Código essencial (middleware auth, parse golang-jwt com verificação de método, verifier go-oidc).
