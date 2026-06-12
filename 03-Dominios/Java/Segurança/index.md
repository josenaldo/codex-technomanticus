---
title: "Segurança"
created: 2026-06-10
updated: 2026-06-11
type: moc
status: growing
publish: true
tags:
  - java
  - seguranca
  - moc
aliases:
  - "Segurança"
  - "Spring Security"
  - "Segurança em Java"
  - "Galho 12 - Segurança"
---

# Segurança

> [!abstract] TL;DR
> O **Galho 12** é a camada que protege a borda web do Galho 9 usando o mecanismo do Galho 8: o **filter chain**, autenticação e password encoding, autorização **URL-based** e **method-level**, **JWT**, **OAuth2/OIDC**, **CSRF/CORS**, session management e security headers, e o **OWASP Top 10** mapeado pras defesas do Spring Security. São **18 notas** em 3 fases (Iniciado, Adepto, Magus).

## Sobre este galho

Segurança no stack Spring é a camada que **autentica** (quem é você) e **autoriza** (o que você pode) cada request antes que ela toque a regra de negócio. Este galho parte do filter chain e do `SecurityContext`, percorre a autenticação (`UserDetailsService`, password encoding) e a autorização (URL-based e method-level com SpEL), sobe pro mundo stateless (JWT, OAuth2 Resource Server, OIDC Client, refresh tokens), cobre as defesas de borda (CSRF, CORS, headers, sessão) e fecha mapeando o **OWASP Top 10** pras ferramentas do Spring Security, com um capstone de API production-grade.

**Audiência primária:** dev pleno/sênior que vai encarar **entrevista internacional de backend Java/Spring** e precisa explicar autenticação, autorização e o filter chain com critério. **Secundária:** quem desenha ou audita a segurança de uma API Spring e precisa decidir entre stateful e stateless, URL-based e method-level, RBAC e ABAC.

É um **galho híbrido**: combina a **poda integral do tronco** `Spring Security.md` (a nota monolítica antiga, agora dissolvida em notas atômicas) com **pesquisa version-specific** na doc oficial do Spring Security 6.x. E tem **dupla fronteira**: usa o **mecanismo AOP do Galho 8** ([[03-Dominios/Java/Spring Core e Boot/index|Spring Core e Boot]] — os proxies que fazem `@PreAuthorize` funcionar), protege a **borda web do Galho 9** ([[03-Dominios/Java/Web e APIs REST/index|Web e APIs REST]] — os endpoints que o filter chain envolve) e toca de leve a **Servlet API do Galho 7** ([[03-Dominios/Java/Jakarta EE/index|Jakarta EE]] — os `Filter`s por baixo do `SecurityFilterChain`). As notas linkam de volta a essas fronteiras sem re-explicá-las.

O foco é **servlet/MVC**: a segurança reativa (WebFlux Security) é fronteira pra frente. Testes de segurança são o galho [[03-Dominios/Java/Testes/13 - Testando a segurança|Testes]]; segurança em microservices é o galho [[03-Dominios/Java/Microservices e sistemas distribuídos/17 - Segurança entre serviços|Microservices e sistemas distribuídos]]; segredos/cloud security não têm cobertura aqui (o Galho 17 trata só de ConfigMap/Secret básico em produção, não de secret-management).

## Iniciado

O modelo mental — authn, authz e o usuário atual.

- [[03-Dominios/Java/Segurança/01 - O que é Spring Security — authn, authz e o filter chain|01 — O que é Spring Security]] — autenticação vs autorização e o filter chain como espinha dorsal.
- [[03-Dominios/Java/Segurança/02 - SecurityContext, Authentication e Principal — o usuário atual|02 — SecurityContext, Authentication e Principal]] — onde mora o usuário atual e como o request o carrega.
- [[03-Dominios/Java/Segurança/03 - Autenticação — UserDetailsService, AuthenticationManager, Form e Basic|03 — Autenticação]] — `UserDetailsService`, `AuthenticationManager` e os fluxos Form e Basic.
- [[03-Dominios/Java/Segurança/04 - Password encoding — BCrypt, Argon2 e o DelegatingPasswordEncoder|04 — Password encoding]] — por que nunca guardar senha em claro: BCrypt, Argon2 e o `DelegatingPasswordEncoder`.
- [[03-Dominios/Java/Segurança/05 - Autorização baseada em URL — authorizeHttpRequests, roles vs authorities|05 — Autorização baseada em URL]] — `authorizeHttpRequests` e a diferença entre roles e authorities.

## Adepto

O filter chain a fundo, method security, JWT e as defesas de borda.

- [[03-Dominios/Java/Segurança/06 - A arquitetura do filter chain em profundidade|06 — A arquitetura do filter chain]] — a ordem dos filtros, o `SecurityFilterChain` e como o request atravessa.
- [[03-Dominios/Java/Segurança/07 - Method security — @PreAuthorize, @PostAuthorize e SpEL|07 — Method security]] — autorização no método com `@PreAuthorize`/`@PostAuthorize` e o poder do SpEL.
- [[03-Dominios/Java/Segurança/08 - JWT — estrutura, assinatura e validação|08 — JWT]] — header, payload e signature: a estrutura, a assinatura e a validação de um token.
- [[03-Dominios/Java/Segurança/09 - OAuth2 Resource Server — validando JWT na API|09 — OAuth2 Resource Server]] — a API como Resource Server validando o JWT a cada request.
- [[03-Dominios/Java/Segurança/10 - CSRF — por que ligado por default e quando desligar|10 — CSRF]] — o ataque, por que o Spring liga CSRF por default e quando é seguro desligar.
- [[03-Dominios/Java/Segurança/11 - CORS — a borda, o preflight e a config de segurança|11 — CORS]] — a same-origin policy, o preflight `OPTIONS` e onde a config de CORS entra na segurança.

## Magus

OAuth2/OIDC client, autorização avançada, o panorama OWASP e o capstone.

- [[03-Dominios/Java/Segurança/12 - OAuth2 e OIDC Client e os grant types|12 — OAuth2 e OIDC Client]] — o lado client do OAuth2/OIDC e os grant types (authorization code, client credentials).
- [[03-Dominios/Java/Segurança/13 - Refresh tokens e revogação de token|13 — Refresh tokens e revogação]] — o ciclo de vida do token: refresh, expiração e o problema de revogar o irrevogável.
- [[03-Dominios/Java/Segurança/14 - Autorização avançada — AuthorizationManager, RBAC vs ABAC|14 — Autorização avançada]] — o `AuthorizationManager` e o confronto RBAC vs ABAC.
- [[03-Dominios/Java/Segurança/15 - Session management e security headers|15 — Session management e security headers]] — fixation, concorrência de sessão e os headers que o Spring injeta por default.
- [[03-Dominios/Java/Segurança/16 - OWASP Top 10 no contexto Java|16 — OWASP Top 10 no contexto Java]] — as 10 categorias mapeadas pras defesas do Spring Security e do ecossistema Java.
- [[03-Dominios/Java/Segurança/17 - Uma request autenticada do token à autorização no método|17 — Uma request autenticada de ponta a ponta]] — o trajeto completo: do token no filtro à autorização no método.
- [[03-Dominios/Java/Segurança/18 - Capstone — projetando a segurança de uma API Spring production-grade|18 — Capstone]] — projetando a segurança de uma API Spring production-grade de ponta a ponta.

## Rotas alternativas

- **Completa** — 01 → 18 em ordem (do filter chain ao capstone).
- **Entrevista internacional** — 01 → 03 → 06 → 07 → 08 → 09 → 17 (Spring Security, autenticação, filter chain, method security, JWT, Resource Server, request de ponta a ponta — o que mais cai).
- **API stateless com JWT** — 01 → 08 → 09 → 10 → 13 → 17 (o modelo, JWT, Resource Server, CSRF no contexto stateless, refresh, request de ponta a ponta).
- **Autorização do grosso ao fino** — 05 → 07 → 14 → 16 (URL-based, method-level, `AuthorizationManager`/RBAC-vs-ABAC, OWASP).
- **Protegendo a borda web** — 01 → 06 → 10 → 11 → 15 + Galho 9 (`DispatcherServlet`, `Interceptor`s vs `Filter`s — onde a segurança encontra o MVC).

## Todas as notas

```dataview
TABLE fase, status
FROM "03-Dominios/Java/Segurança"
WHERE type = "concept"
SORT file.name ASC
```

## Veja também

- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Spring Core e Boot/index|Spring Core e Boot]] — o mecanismo AOP que faz method security funcionar (Galho 8)
- [[03-Dominios/Java/Web e APIs REST/index|Web e APIs REST]] — a borda que a segurança protege (Galho 9)
- [[03-Dominios/Java/Jakarta EE/index|Jakarta EE]] — a Servlet API por baixo do filter chain (Galho 7)
- [[03-Dominios/Java/Dicionário de Java]] — glossário de termos da trilha

> Galhos 13 (Testes), 16 (Microservices) e 17 (Cloud) — planejados.
