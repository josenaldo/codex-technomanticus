---
title: "Spec — Galho 12 da trilha Java Senior (Segurança)"
date: 2026-06-10
author: Josenaldo
status: draft
type: spec
publish: false
---

# Spec — Galho 12 da trilha Java Senior (Segurança)

## 1. Contexto e motivação

Este é o **décimo segundo galho** da trilha Java Senior (roadmap em `docs/superpowers/specs/2026-06-02-java-senior-roadmap-design.md`, §5, bloco "Fundamentos enterprise e Spring", linha 153). Pressupõe leitura do roadmap, que estabelece topologia flat, esquema de 3 fases, padrões editoriais e política de poda. Os Galhos 1 (Linguagem), 2 (Collections/Streams), 3 (JVM), 4 (Concorrência), 5 (Swing), 6 (JavaFX), 7 (Jakarta EE), 8 (Spring Core e Boot), 9 (Web e APIs REST), 10 (Persistência) e **11 (Programação Reativa)** já fecharam em `main` — seus artefatos são o **template de padrão e qualidade** deste galho. As dependências diretas são os **Galhos 8 e 9** (linha 155 do roadmap): o Galho 8 é dono do **mecanismo** (o container, o proxy AOP que faz `@PreAuthorize`/`@EnableMethodSecurity` funcionar; o `SecurityFilterChain` é um bean); o Galho 9 é dono da **camada web** que a segurança protege (o `DispatcherServlet`, o `Filter` genérico, o CORS como config MVC).

**Galho HÍBRIDO: REFATOR (poda INTEGRAL de tronco monolítico) + PESQUISA.** Como o Galho 10, tem dupla natureza, mas poda **um único** tronco — de forma integral (padrão JavaFX/Galho 6):

- **Parte REFATOR (poda integral):** `Backend/Spring Security.md` (1116 linhas, `publish: false`, `status: evergreen`) é o **tronco dedicado deste galho**. Cobre **todo** o escopo (filter chain, authn/authz, JWT, OAuth2/OIDC, method security, CSRF, CORS, password encoding, session management, security headers, OWASP) de forma densa e monolítica. **Poda INTEGRAL** (padrão JavaFX/Galho 6): o tronco encolhe a um hub de ~20 linhas — frontmatter (`publish: false`), H1, 1-2 frases de intro e um único callout `[!nota] Migrado para galho próprio` com wikilinks pro MOC do galho + notas representativas. **Toda a fabricação evapora** com a poda (o tronco tem `Patient`/`Doctor`/`Appointment`/`MedEspecialista`, a seção `## Na prática (da minha experiência)` ~963 com incidentes fabricados — "pentest", "incidente memorável com `alg: none`", "NPE em SecurityContext sob carga" —, e `## How to explain in English` em 1ª pessoa ~1003 — **contraexemplo, jamais copiar pras notas**).

- **Parte PESQUISA:** mesmo o tronco dedicado sendo rico, várias afirmações são **version-specific** e exigem confirmação via WebFetch. A seção `## Evolução da configuração` do tronco mistura Spring Security 5.x (legado) e 6.x, e pode ter config stale a re-fundar na doc oficial. Pontos minados (ZERO memória): **`WebSecurityConfigurerAdapter` removido na 6.0** (usa-se `SecurityFilterChain` bean + lambda DSL); **`authorizeHttpRequests` substituiu `authorizeRequests`**; **`@EnableMethodSecurity` substituiu `@EnableGlobalMethodSecurity`**; `DelegatingPasswordEncoder`/BCrypt/Argon2; OAuth2 Resource Server (JWT) vs Client; **CSRF habilitado por default** (e quando desabilitar pra API stateless). Fonte: `docs.spring.io/spring-security/reference/`. **OWASP no contexto Java sem inventar estatística.**

**A fronteira-assinatura é DUPLA.** Os Galhos 8 e 9 plantaram ganchos esperando exatamente as notas deste galho. Este galho **linka de volta aos dois**, sem re-explicar nenhum (e toca **levemente** o Galho 7 num único ponto — a Servlet API por baixo do filter chain):

- **Galho 8 (o mecanismo):** o **proxy AOP** que intercepta `@PreAuthorize` → [[03-Dominios/Tecnologia/Java/Spring Core e Boot/09 - AOP e proxies no Spring|AOP e proxies]]; os **limites do proxy** (`@PreAuthorize` em método `private`/`final` não funciona, self-invocation) → [[03-Dominios/Tecnologia/Java/Spring Core e Boot/10 - Self-invocation e os limites do proxy|Self-invocation e os limites do proxy]]; o `SecurityFilterChain` é um **bean** no container → [[03-Dominios/Tecnologia/Java/Spring Core e Boot/06 - ApplicationContext — o container e seu ciclo|ApplicationContext]]. Este galho cobre **method security** e a config; **não o mecanismo** (que é o AOP do Galho 8).
- **Galho 9 (a camada web que a segurança protege):** o filter chain senta na frente do **DispatcherServlet** → [[03-Dominios/Tecnologia/Java/Web e APIs REST/06 - O pipeline do DispatcherServlet|O pipeline do DispatcherServlet]]; o **`Filter` genérico vs o `SecurityFilterChain`** → [[03-Dominios/Tecnologia/Java/Web e APIs REST/11 - Interceptors vs Filters|Interceptors vs Filters]] (que *espera* esse link — `:357`); **CORS** foi tratado como config MVC no Galho 9 — aqui é a **borda de segurança**. Este galho cobre a **camada de filtros do Spring Security**; **não re-explica o pipeline MVC**.
- **Galho 7 (toque leve — a Servlet API por baixo):** o filter chain do Spring Security é, no fundo, um único `Filter` da plataforma Servlet → [[03-Dominios/Tecnologia/Java/Jakarta EE/03 - Servlet API — o alicerce HTTP|Servlet API]] (link só na nota 06, sem re-explicar a spec).

Os Galhos 8 e 9 deixaram **ganchos "Galho 12 (planejado)"** em texto esperando exatamente esses wikilinks (dívida reversa — §3.6). Este galho **quita** essa dívida.

Segurança é a **camada que protege a borda web do Galho 9 usando o mecanismo do Galho 8**: como o filter chain intercepta cada request antes do `DispatcherServlet`, como se autentica (quem é — `UserDetailsService`, `AuthenticationManager`, password encoding) e se autoriza (o que pode — `authorizeHttpRequests`, method security via proxy AOP, RBAC), como JWT torna a API stateless, como OAuth2/OIDC delega identidade (Resource Server validando vs Client logando), como CSRF/CORS protegem a borda, e como o OWASP Top 10 se mapeia pras defesas do Spring Security. Depende dos Galhos 8 (mecanismo) e 9 (camada web).

## 2. Objetivo

Produzir, em uma sessão de execução dedicada, **18 notas atômicas + 1 MOC do galho + expansão do Dicionário de Java + ativação do MOC central + poda INTEGRAL do tronco `Spring Security.md` + quitação da dívida reversa**, em `03-Dominios/Tecnologia/Java/Segurança/` e `03-Dominios/Tecnologia/Java/`, todas `publish: true`, em PT-BR, distribuídas em 3 fases (**5 Iniciado + 6 Adepto + 7 Magus**).

Ao terminar o galho, o leitor deve conseguir:

- **Explicar em inglês** a arquitetura central do Spring Security (o filter chain na frente do `DispatcherServlet`), a diferença authentication vs authorization, o fluxo de uma request autenticada (token → filtro → `SecurityContext` → autorização), e por que CSRF é ligado por default mas se desabilita numa API stateless com JWT.
- **Reconhecer o que este galho deve ao mecanismo do Galho 8**: method security (`@PreAuthorize`/`@EnableMethodSecurity`) roda sobre o **proxy AOP**, e os limites do proxy (método `private`/`final`, self-invocation) explicam por que `@PreAuthorize` às vezes "não funciona"; o `SecurityFilterChain` é um **bean** no container.
- **Reconhecer o que este galho protege da camada web do Galho 9**: o filter chain senta na frente do `DispatcherServlet`, o `SecurityFilterChain` contrasta com o `Filter` genérico, e CORS aqui é a **borda de segurança** (não a config MVC).
- **Projetar uma camada de segurança production-grade**: `SecurityFilterChain` bean + lambda DSL (6.x), autenticação stateless via OAuth2 Resource Server (JWT validado por JWKS, `iss`/`aud`/`exp`, nunca confiar no `alg`), autorização method-level com SpEL, password encoding com `DelegatingPasswordEncoder`/BCrypt, CSRF off em API stateless / on em web app com sessão, CORS com origens explícitas, e os security headers certos.
- **Diagnosticar armadilhas clássicas**: `antMatchers`/`authorizeRequests` legados (6.x usa `requestMatchers`/`authorizeHttpRequests`), CSRF desabilitado em web app com sessão, JWT com `alg: none` aceito, JWT sem validar `aud`/`iss`, `@PreAuthorize` em método `private` (proxy AOP), esquecer `@EnableMethodSecurity` (anotação ignorada silenciosamente), `allowedOrigins("*")` + `allowCredentials(true)`, confundir CORS com segurança do servidor (`curl` bypassa), `SecurityContextHolder` vazando auth entre requests em thread pool.

A barra é "explicar o filter chain, reconhecer o mecanismo (Galho 8) e a borda (Galho 9) por baixo, e projetar a camada de segurança com critério" — não "escrever um `AuthenticationProvider` customizado pra SAML do zero".

## 3. Saídas concretas

### 3.1. Notas (`03-Dominios/Tecnologia/Java/Segurança/`)

Pasta **nova**, flat. 18 notas + 1 MOC (`index.md`, obrigatório pro folder-link do Quartz). Numeração global por galho (não reinicia por fase).

#### Iniciado (5 notas — vocabulário + modelo mental)

| # | Nota | Escopo nuclear |
|---|------|----------------|
| 01 | O que é Spring Security — authn, authz e o filter chain *(opus)* | Authentication (quem você é) vs authorization (o que pode); o **filter chain** como modelo mental (request → `FilterChainProxy` → `SecurityFilterChain` → `DispatcherServlet`); config moderna 6.x (`SecurityFilterChain` bean + **lambda DSL**; `@EnableWebSecurity`; **`WebSecurityConfigurerAdapter` removido na 6.0** — WebFetch). **A nota-assinatura da DUPLA fronteira:** o chain senta na frente do `DispatcherServlet` (Galho 9), method security roda sobre AOP (Galho 8). Linka **G9 nota 11** (Filter genérico vs SecurityFilterChain), **G8** (bean no container). |
| 02 | SecurityContext, Authentication e Principal — o usuário atual | `SecurityContextHolder` (`ThreadLocal` por default; nota de fronteira pra scoped values em Java 21+ sem aprofundar); `Authentication` (extends `Principal`) / `Principal` / `GrantedAuthority`; onde o principal vive durante o request; `@AuthenticationPrincipal` no controller. |
| 03 | Autenticação — UserDetailsService, AuthenticationManager, Form e Basic *(opus)* | Os tipos de auth (Basic, Form, JWT, OAuth2 — tabela "quando usar"); `UserDetailsService.loadUserByUsername` carregando do banco (auto-detectado como bean); `AuthenticationManager` → `AuthenticationProvider` → `UserDetailsService`; HTTP Basic (sempre HTTPS) vs Form login (sessão). |
| 04 | Password encoding — BCrypt, Argon2 e o DelegatingPasswordEncoder | Nunca plain text; `PasswordEncoder` (`encode`/`matches`); BCrypt (default, work factor, slow-by-design) vs Argon2 vs Pbkdf2/Scrypt; **`DelegatingPasswordEncoder`** e o prefixo `{bcrypt}$2a$...`; migração gradual entre algoritmos. WebFetch. |
| 05 | Autorização baseada em URL — authorizeHttpRequests, roles vs authorities | **`authorizeHttpRequests`** (substituiu `authorizeRequests` — WebFetch) + `requestMatchers` (substituiu `antMatchers`); `permitAll`/`authenticated`/`hasRole`/`hasAuthority`/`denyAll`; **`hasRole("ADMIN")` busca `ROLE_ADMIN`** (prefixo convenção); RBAC básico; matcher por `HttpMethod`. **Quita a dívida do Actuator (G8 nota 17)**: proteger `/actuator/**` com `requestMatchers`. |

#### Adepto (6 notas — domínio operacional)

| # | Nota | Escopo nuclear |
|---|------|----------------|
| 06 | A arquitetura do filter chain em profundidade *(opus)* | `FilterChainProxy` (o `Filter` único que delega), a **ordem dos filtros** (`SecurityContextHolderFilter` → headers → CORS → CSRF → auth filters → `ExceptionTranslationFilter` → `AuthorizationFilter`), **múltiplos `SecurityFilterChain`** (por `securityMatcher`), `ExceptionTranslationFilter` (401 não-autenticado vs 403 não-autorizado), onde adicionar filtro custom (`addFilterBefore`/`After`). **O contraste explícito: `Filter` genérico (G9 nota 11) vs `SecurityFilterChain`.** Linka **G9 nota 11**, **G7 nota 03** (Servlet API por baixo). |
| 07 | Method security — @PreAuthorize, @PostAuthorize e SpEL *(opus)* | **`@EnableMethodSecurity`** (substituiu `@EnableGlobalMethodSecurity`; `prePostEnabled` default true — WebFetch); `@PreAuthorize`/`@PostAuthorize`/`@PreFilter`/`@PostFilter`; SpEL (`hasRole`, `#param`, `authentication.principal`, `@bean.method`); URL-based (grossa) vs method-level (granular). **O mecanismo é o proxy AOP do G8** → linka **G8 nota 09** (AOP) + **nota 10** (`@PreAuthorize` em `private`/self-invocation não funciona — o limite do proxy). |
| 08 | JWT — estrutura, assinatura e validação *(opus)* | Header/payload/signature (base64, **não criptografia**); claims (`iss`/`sub`/`aud`/`exp`/`nbf`/`iat`/`jti`); **assimétrico RS256/ES256 vs simétrico HS256**; **`alg: none` e a whitelist de algoritmos**; stateless; prós (portável, self-contained) e contras (revogação difícil — forward-link pra **nota 13**). |
| 09 | OAuth2 Resource Server — validando JWT na API *(opus)* | `spring-boot-starter-oauth2-resource-server`; `oauth2ResourceServer().jwt()`; `issuer-uri`/**JWKS** (`jwk-set-uri`, rotação sem downtime); `JwtAuthenticationConverter` (claim `roles`/`scope` → `GrantedAuthority`, prefixo `SCOPE_`/`ROLE_`); `@AuthenticationPrincipal Jwt`; `SessionCreationPolicy.STATELESS` + CSRF off (forward-link notas 10/15). WebFetch. |
| 10 | CSRF — por que ligado por default e quando desligar | O ataque (request autenticada forjada via cookie); **CSRF ativo por default** no Spring Security (WebFetch); web app com sessão cookie **mantém** (token sincronizado em form); API stateless com JWT em `Authorization` header **desliga** (browser não envia o header automaticamente); SPA + cookie session (`CookieCsrfTokenRepository.withHttpOnlyFalse`, `X-XSRF-TOKEN`). |
| 11 | CORS — a borda, o preflight e a config de segurança | Mecanismo do **browser** (não do servidor — `curl` bypassa, **não é segurança server-side**); `CorsConfigurationSource` (`allowedOrigins`/`Methods`/`Headers`, `allowCredentials`, `maxAge`); **preflight OPTIONS** (requests "complexos"); `allowedOrigins("*")` + `allowCredentials(true)` rejeitado; `.cors()` no filter chain. **vs a config CORS como MVC do Galho 9** — aqui é a borda de segurança no filter chain. Linka **G9**. |

#### Magus (7 notas — maestria + arquitetura)

| # | Nota | Escopo nuclear |
|---|------|----------------|
| 12 | OAuth2/OIDC Client e os grant types *(opus)* | Login social (`spring-boot-starter-oauth2-client`, `oauth2Login`, `@AuthenticationPrincipal OidcUser`); **OAuth2 (delegação de acesso) vs OIDC (camada de identidade, `id_token`)**; os grant types: **authorization code + PKCE** (web/mobile), **client credentials** (server-to-server, sem user); implicit/password **deprecated**; Resource Server (nota 09) vs Client (aqui). OAuth2 num gateway/microservices → Galho 16 (texto "(planejado)"). |
| 13 | Refresh tokens e revogação de token | O trade-off **stateless vs revogação** (JWT válido até expirar); par **access token curto (15min) + refresh token server-side (UUID, não JWT)**; rotação a cada uso; tabela `refresh_tokens` (`token_hash`, `user_id`, `expires_at`, `revoked`); revogação imediata (logout/troca de senha); blacklist quebra o stateless (trade-off honesto); armazenamento (HttpOnly Secure SameSite cookie vs localStorage — XSS). |
| 14 | Autorização avançada — AuthorizationManager, RBAC vs ABAC | `AuthorizationManager<RequestAuthorizationContext>` + `.access(...)` pra lógica custom (acesso a `tenant`/recurso); **RBAC** (roles→permissões, cobre a maioria) vs **ABAC** (atributos, via SpEL) vs **ReBAC** (Zanzibar — OpenFGA/SpiceDB, menção); role hierarchy (`RoleHierarchy`); exemplo neutro "`owner` só vê o próprio recurso" (`#resource.ownerId == authentication.principal.id`). |
| 15 | Session management e security headers | **STATELESS** (JWT) vs stateful (`HttpSession`/`JSESSIONID`); **session fixation** (`migrateSession` — default); concurrent sessions (`maximumSessions`); Spring Session/Redis (multi-instância, menção); **security headers** (HSTS, **CSP** anti-XSS, `X-Frame-Options` anti-clickjacking, `X-Content-Type-Options: nosniff`, `Referrer-Policy`) que o Spring adiciona por default e como customizar. |
| 16 | OWASP Top 10 no contexto Java *(— a síntese)* | O Top 10 mapeado pras defesas que o galho já cobriu: **Broken Access Control** → method security (07)/authz (05,14); **Cryptographic Failures** → BCrypt (04)/HTTPS/JWT assinado (08); **Injection** → JPA params (Galho 10)/`PreparedStatement`; **Insecure Design**/**Security Misconfiguration** → CSRF/CORS/headers (10,11,15); **Identification/Auth Failures** → password encoding, session (15), refresh tokens (13); **SSRF** etc. **Sem estatística inventada** (mapeamento conceitual, não "X% das brechas"). Cita defesa-em-profundidade sem fabricar incidente. |
| 17 | Uma request autenticada do token à autorização no método *(opus, capstone — trace)* | **Trace:** `Authorization: Bearer <jwt>` → `BearerTokenAuthenticationFilter` → decode + validação (assinatura/JWKS, `iss`/`aud`/`exp`) → `JwtAuthenticationConverter` monta `Authentication` → `SecurityContextHolder` → `AuthorizationFilter` (regras de URL) → `DispatcherServlet` → controller → `@PreAuthorize` (proxy AOP — G8) → service. O caminho do 401 (não-autenticado) e do 403 (não-autorizado) via `ExceptionTranslationFilter`. |
| 18 | Capstone — projetando a segurança de uma API Spring production-grade *(opus, checklist + síntese)* | **Checklist production-grade:** `SecurityFilterChain` bean + lambda DSL; stateless + OAuth2 Resource Server (JWKS, valida `iss`/`aud`/`exp`, whitelist de `alg`); CSRF off (stateless) / on (sessão); CORS com origens explícitas; method security com SpEL; `DelegatingPasswordEncoder`/BCrypt; security headers; refresh tokens server-side. **Tabela "Galho 12 → mecanismo (Galho 8) / borda (Galho 9)"** (`@PreAuthorize`↔proxy AOP, `SecurityFilterChain`↔bean+Filter, CORS↔borda vs config MVC). **Menção de teste de segurança** (`@WithMockUser`/`with(jwt())`) como fronteira → Galho 13. Cheatsheet nota→problema. Munição de entrevista. |

**Notas opus (9):** 01 (assinatura/dupla fronteira), 03 (autenticação), 06 (filter chain — a mais densa), 07 (method security + AOP), 08 (JWT), 09 (Resource Server), 12 (OAuth2/OIDC Client), 17 (capstone-trace), 18 (capstone-checklist). As demais (02, 04, 05, 10, 11, 13, 14, 15, 16) → sonnet. Notas com afirmação version-specific (01, 04, 05, 07, 09, 10) fazem WebFetch no Step 1 independentemente do modelo.

**Decisões de fronteira (escopo de outro dono — texto "(planejado)", sem wikilink):**
- **Container / IoC / AOP / o proxy que faz `@PreAuthorize` / self-invocation / bean** → Galho 8 (COMPLETO). **Linkar de volta, nunca re-explicar o mecanismo** (method security ≠ AOP). Primeira face da fronteira-assinatura.
- **DispatcherServlet / `Filter` genérico vs `SecurityFilterChain` / CORS como config MVC / pipeline web** → Galho 9 (COMPLETO). **Linkar de volta, nunca re-explicar o pipeline.** Segunda face.
- **Servlet API / o `Filter` da plataforma por baixo do chain** → Galho 7 (COMPLETO). Toque leve (só nota 06).
- **Segurança reativa / WebFlux Security / `ReactiveSecurityContextHolder` / `Mono<Authentication>`** → menção "(planejado)". O foco é **servlet/MVC**; a segurança reativa fica fora (o Galho 11 Reativa deixou o gancho `index:35` "segurança reativa (Galho 12)" — **permanece "(planejado)"**, é fronteira pra frente).
- **OAuth2 num API gateway / SSO entre microservices / Spring Cloud Gateway security** → Galho 16 (planejado). A nota 12 **cita** que num gateway o OAuth2 vive na borda do sistema, sem aprofundar.
- **Testes de segurança (`@WithMockUser`, `with(jwt())`, Testcontainers + Keycloak)** → Galho 13 (planejado). As notas **citam** que se testa com mock user / JWT de teste, sem ensinar a stack de teste; a capstone (18) **menciona** como fronteira.
- **Observabilidade do Actuator (métricas, tracing)** → Galho 17 (planejado). A **proteção** dos endpoints do Actuator (autenticação/autorização) é **quitada aqui** (nota 05); a observabilidade em si fica no 17.
- **Segurança a nível de dados (row-level security, criptografia de campo, auditoria com `AuditorAware`/`SecurityContext`)** → tocada **de leve**; profundidade fica fora. A auditoria JPA (`@CreatedDate`) é do Galho 10; o `AuditorAware` que puxa o `SecurityContext` é a ponte (mencionada, não aprofundada).
- **TLS/HTTPS/certificados (teoria de rede)** → nota existente [[Redes e Protocolos]] (linkar quando JWT/Basic exigirem HTTPS). **SQL injection (mecânica de query)** → Galho 10 (linkar na nota 16 OWASP). **Annotations (mecânica)** → Galho 1 (linkar quando tocar `@PreAuthorize` como anotação, se couber).

### 3.2. MOC do galho

`03-Dominios/Tecnologia/Java/Segurança/index.md`:
- `type: moc`, `status: growing`
- Frontmatter padrão (`title: "Segurança"`, tags `java`/`seguranca`/`moc`, aliases `["Segurança", "Spring Security", "Segurança em Java", "Galho 12 - Segurança"]`)
- TL;DR callout (galho cobre a camada que protege a borda web do Galho 9 usando o mecanismo do Galho 8: o filter chain, autenticação e password encoding, autorização URL-based e method-level, JWT, OAuth2/OIDC, CSRF/CORS, session management e security headers, e o OWASP Top 10 mapeado pras defesas do Spring Security)
- "Sobre este galho" + audiência primária/secundária + nota de que é galho híbrido (poda integral do tronco `Spring Security.md` + pesquisa pras partes version-specific) e de **dupla fronteira** (usa o mecanismo AOP do Galho 8, protege a borda web do Galho 9)
- Conteúdo agrupado em 3 H2 (`## Iniciado` / `## Adepto` / `## Magus`) com wikilinks pras 18 notas (uma linha descritiva cada)
- **Rotas alternativas (5):**
  - **Completa** — 01 → 18 em ordem
  - **Entrevista internacional** — 01 → 03 → 06 → 07 → 08 → 09 → 17 (filter chain, autenticação, method security, JWT, Resource Server, request autenticada ponta-a-ponta — o que mais cai)
  - **API stateless com JWT** — 01 → 08 → 09 → 10 → 13 → 17 (filter chain, JWT, Resource Server, CSRF off, refresh tokens, trace)
  - **Autorização do grosso ao fino** — 05 → 07 → 14 → 16 (URL-based, method security, AuthorizationManager/RBAC/ABAC, OWASP)
  - **Protegendo a borda web** (a ponte com o Galho 9) — 01 → 06 → 10 → 11 → 15 + notas do Galho 9 (DispatcherServlet, Interceptors vs Filters)
- "Veja também": MOC central `[[03-Dominios/Tecnologia/Java/index|Trilha Java]]`, **Galho 8** (Spring Core e Boot — o mecanismo AOP que faz method security funcionar), **Galho 9** (Web e APIs REST — a borda que a segurança protege), **Galho 7** (Jakarta EE — a Servlet API por baixo do filter chain), nota existente [[Redes e Protocolos]] (HTTPS/TLS), Dicionário de Java; Galhos 13/16/17 como texto "(planejado)" sem wikilink
- Dataview "Todas as notas do galho"

### 3.3. Dicionário de Java (EXPANSÃO — não recriar)

`03-Dominios/Tecnologia/Java/Dicionário de Java.md` já existe (**327 verbetes** após o Galho 11, `type: glossary`, `updated: 2026-06-10`, seções alfabéticas únicas `## A`…`## Z` com verbetes `### `). Este galho **expande** o arquivo existente inserindo os verbetes **em ordem alfabética case-insensitive (sem acento)** nas seções de letra apropriadas. **Nunca recriar o arquivo nem reordenar verbetes existentes.** Manter `updated: 2026-06-10` (mesmo dia do Galho 11).

Verbetes a inserir (~35, conferir dups antes):

`@AuthenticationPrincipal`, `@EnableMethodSecurity`, `@PreAuthorize / @PostAuthorize`, `@WithMockUser`, `ABAC (attribute-based)`, `alg: none (ataque JWT)`, `AuthenticationManager`, `AuthenticationProvider`, `authorizeHttpRequests`, `AuthorizationManager`, `BCryptPasswordEncoder`, `BearerTokenAuthenticationFilter`, `client credentials (grant)`, `CORS`, `CSRF`, `CsrfFilter`, `DelegatingPasswordEncoder`, `ExceptionTranslationFilter`, `FilterChainProxy`, `GrantedAuthority`, `hasRole vs hasAuthority`, `JWKS (JSON Web Key Set)`, `JWT (JSON Web Token)`, `JwtAuthenticationConverter`, `OAuth2`, `OAuth2 Client`, `OAuth2 Resource Server`, `OIDC (OpenID Connect)`, `OWASP Top 10`, `PasswordEncoder`, `PKCE / authorization code`, `RBAC (role-based)`, `refresh token`, `RoleHierarchy`, `SecurityContextHolder`, `SecurityFilterChain`, `session fixation`, `SessionCreationPolicy (STATELESS)`, `Spring Security`, `UserDetailsService`.

Cada verbete: definição curta (1-3 linhas) em PT-BR + `Veja também:` apontando pra(s) nota(s) canônica(s) do galho. **Conferir com grep os verbetes já existentes** (possíveis dups do Galho 9: `CORS` — tratado como config MVC; `Filter` / `Servlet` (Galho 7/9); `DispatcherServlet`; `access token`/`scope` se já houver) para **não duplicar** — quando um termo tocar um já existente, **linkar entre si** em vez de criar segundo verbete (ex.: `CORS` do Galho 12 ↔ `CORS` do Galho 9 se existir; `Filter` genérico ↔ `SecurityFilterChain`). **Conferir 1:1** que os headings dos verbetes batem EXATAMENTE com as âncoras `[[Dicionário de Java#...]]` usadas nas notas (extrair as âncoras das notas via grep e conferir, como nos Galhos 4-11).

### 3.4. MOC central (ativação do Galho 12)

`03-Dominios/Tecnologia/Java/index.md` já existe. Task **mínima**: trocar a linha 42 (atualmente `12. Segurança *(planejado)* — Spring Security, JWT, OAuth2/OIDC, CSRF/CORS`) por wikilink ativo no padrão dos galhos fechados:

```markdown
12. [[03-Dominios/Tecnologia/Java/Segurança/index|Segurança]] — Spring Security e o filter chain, autenticação e password encoding, autorização URL-based e method-level, JWT, OAuth2/OIDC, CSRF/CORS, session management, security headers e OWASP no contexto Java
```

Atualizar `updated` para `2026-06-10`. Não mexer no resto do MOC central.

### 3.5. Poda INTEGRAL do tronco `Backend/Spring Security.md`

O tronco dedicado deste galho (1116 linhas, `publish: false`). **Poda integral** (padrão JavaFX/Galho 6): substituir **todo o corpo** (da linha após o frontmatter até o fim) por:
- frontmatter preservado, com `publish: false` (mantém — é tronco de trabalho) e `updated: 2026-06-10`;
- H1 `# Spring Security`;
- 1-2 frases de intro neutras (sem fabricação);
- um único callout `[!nota] Migrado para galho próprio` com wikilink pro MOC do galho + ~5-6 notas representativas (01, 06, 08, 09, 12, 18), formato herdado do JavaFX/Galho 10:

```markdown
> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Tecnologia/Java/Segurança/index|Segurança]]. Veja [[03-Dominios/Tecnologia/Java/Segurança/01 - O que é Spring Security — authn, authz e o filter chain|O que é Spring Security]], [[03-Dominios/Tecnologia/Java/Segurança/06 - A arquitetura do filter chain em profundidade|A arquitetura do filter chain]], [[03-Dominios/Tecnologia/Java/Segurança/08 - JWT — estrutura, assinatura e validação|JWT]], [[03-Dominios/Tecnologia/Java/Segurança/09 - OAuth2 Resource Server — validando JWT na API|OAuth2 Resource Server]] e [[03-Dominios/Tecnologia/Java/Segurança/18 - Capstone — projetando a segurança de uma API Spring production-grade|Capstone de segurança]].
```

**Toda a fabricação some** (`Patient`/`Doctor`/`Appointment`/`MedEspecialista`, `## Na prática (da minha experiência)` com os "incidentes memoráveis" fabricados — `alg: none` no pentest, NPE em SecurityContext sob carga, os "3 fluxos de autenticação" do MedEspecialista —, `## How to explain in English` em 1ª pessoa, `### Frases úteis em entrevista`). O nome de arquivo `Spring Security.md` permanece (qualquer wikilink `[[Spring Security]]` continua resolvendo — vira ponteiro pro hub). Confirmar números de linha na execução (lendo o tronco primeiro — política §9 do roadmap).

**NÃO TOCAR em outros troncos:** `Backend/Spring Boot.md` (já podado pelos Galhos 8/9/10), `Backend/Spring Data JPA.md` (hub do Galho 10), `Backend/Kafka/` (Galho 14), `Backend/gRPC e Go.md` (Galho 14), `Backend/Testes em Java.md` (Galho 13). O `## Veja também` do tronco podado recebe wikilink pro MOC do Galho 12.

### 3.6. Dívida reversa (ganchos "Galho 12 / planejado")

Pré-flight localizou **6 ponteiros inline + 3 parágrafos de fronteira** a quitar após as notas existirem. Viram wikilinks pras notas do Galho 12; a segurança deixa de ser texto "(planejado)" **nesses pontos específicos**:

| # | Arquivo:linha | Texto atual (resumo) | Vira wikilink pra |
|---|---|---|---|
| 1 | `index.md:42` (MOC central) | `12. Segurança *(planejado)*` | ativação (§3.4) |
| 2 | `Spring Core e Boot/17 - Actuator:52` | "Segurança de endpoints ... é tema do Galho 12 (planejado)." | **nota 05** (autorização URL-based / proteger `/actuator/**`) |
| 3 | `Spring Core e Boot/17 - Actuator:111` | "Proteção com Spring Security é abordada no Galho 12 (planejado)." | **nota 05** ou MOC |
| 4 | `Spring Core e Boot/17 - Actuator:288` | "proteja com Spring Security (Galho 12, planejado)." | **nota 05** ou MOC |
| 5 | `Web e APIs REST/12 - OpenAPI:167` | "Segurança de API é assunto do Galho 12 (planejado)." | **nota 01** (o filter chain protege a API) ou MOC |
| 6 | `Web e APIs REST/11 - Interceptors vs Filters:357` | "Autenticação, CSRF e autorização pertencem ao Galho 12 ... explora a camada de filtros do Spring Security em profundidade." | **nota 06** (a arquitetura do filter chain) |
| P1 | `Spring Core e Boot/index.md:32` (parágrafo fronteira) | "Spring Security (Galho 12) ... são planejados" | trecho do Galho 12 → wikilink pro **MOC do galho** |
| P2 | `Web e APIs REST/index.md:32` (parágrafo fronteira) | "Spring Security (Galho 12) ... são planejados" | trecho do Galho 12 → wikilink pro **MOC do galho** |
| P3 | `Persistência de dados/index.md:32` (parágrafo fronteira) | "segurança de dados (Galho 12) ... são planejados" | trecho do Galho 12 → wikilink pro **MOC do galho** (mantendo honesto: row-level/field-level fica de leve) |

**NÃO quitar (fronteira pra frente — permanece "(planejado)"):**
- `Programação Reativa/index.md:35` — "segurança reativa (Galho 12) ... são planejados". A **segurança reativa (WebFlux Security)** está **fora do escopo** deste galho (foco servlet/MVC) — permanece texto "(planejado)".
- **Horizonte-lists de uma linha** (`Spring Core e Boot/index.md:97`, `Web e APIs REST/index.md:95`, `Persistência de dados/index.md:92`) — listas-resumo de galhos futuros que os galhos anteriores deixaram intactas (padrão estabelecido); 13/16/17 permanecem "(planejado)" lá.

Em todos os pontos, manter como texto "(planejado)" qualquer referência a galhos **ainda** inexistentes (13/16/17). Confirmar os números de linha na execução (podem ter deslocado) via grep `"Galho 12"`/`"planejado"`.

## 4. Convenções por nota

Herda §7 do roadmap e §4 dos specs dos Galhos 8/9/10/11. Reforços específicos:

### 4.1. Frontmatter

```yaml
---
title: "<título>"
created: 2026-06-10
updated: 2026-06-10
type: concept
status: seedling
publish: true
fase: iniciado | adepto | magus
tags:
  - java
  - seguranca
  - <fase>
  - <tags específicas: spring-security, filter-chain, autenticacao, autorizacao, password, jwt, oauth2, oidc, method-security, csrf, cors, session, rbac, owasp, ...>
aliases:
  - <aliases opcionais>
---
```

H1 `# Título` após o frontmatter (padrão dos galhos publicados).

### 4.2. Estrutura H2 obrigatória

- `> [!abstract] TL;DR` (callout, NÃO H2) — 2-4 linhas: conceito + regra prática + por que importa
- `## O que é` / `## Por que importa` / `## Como funciona` (≥3 subseções H3 em notas Adepto/Magus)
- `## Na prática` — exemplos compiláveis; framing **neutro** (`Order`/`Customer`/`User`/`Role`/`OrderController`/`UserService`); "padrão observado em apps Spring Security"; NUNCA `Patient`/`MedEspecialista`/"no meu projeto"/"durante um pentest" (o tronco está cheio disso — **contraexemplo**)
- `## Armadilhas` — **≥2** (Iniciado) / **≥3** (Adepto/Magus), cada uma com `### (N) Título` (H3 numerado, NÃO callout `[!warning]`) + descrição + exemplo curto de código demonstrando o problema + fix em 1 linha
- `## Em entrevista` — subheading `### Frase pronta (inglês)` com **3+ sentenças** (trade-off + decisão + caveat) + subheading `### Vocabulário` com tabela `| Termo PT | Termo EN |` de **6+ termos**
- `## Veja também` — wikilinks **SEM backticks**, **SEM âncoras same-file**; sempre inclui notas relacionadas do galho + `[[03-Dominios/Tecnologia/Java/Segurança/index|MOC do galho]]` + `[[03-Dominios/Tecnologia/Java/index|Trilha Java]]` + (quando tocar o mecanismo AOP/method security/bean) a nota do **Galho 8** + (quando tocar filter/DispatcherServlet/CORS/borda web) a nota do **Galho 9** + (nota 06) a Servlet API do **Galho 7** + verbetes do Dicionário
- `## Referências` — docs oficiais (`docs.spring.io/spring-security/reference/`, OAuth2/OIDC specs, OWASP cheat sheets). Afirmações version-specific fundadas em fonte verificada via WebFetch.

### 4.3. Restrições absolutas

1. **Dupla fronteira-assinatura (linkar de volta aos Galhos 8 e 9)** — todo conceito que usa o mecanismo (method security/`SecurityFilterChain` bean) aponta pra nota do **Galho 8** ("o mecanismo é o proxy AOP / é um bean", sem re-explicar); todo conceito que protege a borda (filter chain na frente do `DispatcherServlet`, `Filter` genérico vs `SecurityFilterChain`, CORS) aponta pra nota do **Galho 9** ("é a camada web", sem re-explicar o pipeline). A Servlet API do **Galho 7** é toque leve (só nota 06). Galhos 13/16/17 = texto "(planejado)", sem wikilink.
2. **Sem fabricação** de experiência pessoal. Exemplos neutros (`Order`, `Customer`, `User`, `Role`) — NUNCA `Patient`/`josenaldo`/`MedEspecialista`/1ª pessoa/"durante um pentest"/"incidente memorável". **O tronco é matéria-prima a higienizar, jamais a copiar** (tem `## Na prática (da minha experiência)` com 3 incidentes fabricados e `## How to explain in English` — contraexemplo). **Zero estatística de adoção/segurança inventada** — vale especialmente pro OWASP (nota 16): mapeamento conceitual Top 10 → defesas, **NUNCA "X% das brechas são..."**.
3. **Sem invenção** de APIs/comportamentos. WebFetch obrigatório no Step 1 das notas version-specific (01, 04, 05, 07, 09, 10) e pra **toda afirmação version-specific**. Pontos minados verificados via WebFetch: **`WebSecurityConfigurerAdapter` removido na 6.0**; **`authorizeHttpRequests` substituiu `authorizeRequests`**; **`requestMatchers` substituiu `antMatchers`**; **`@EnableMethodSecurity` substituiu `@EnableGlobalMethodSecurity`**; **CSRF habilitado por default**; `DelegatingPasswordEncoder`/prefixo `{id}`; OAuth2 Resource Server (JWKS, `issuer-uri`) vs Client. Spring Boot 3.x / Spring Security 6.x como **baseline** (`jakarta.*`, Java 17), citando 7.x/Boot 4.x como "mais recente" quando relevante. Fonte: `docs.spring.io/spring-security/reference/`. Nada "de memória".
4. **Code samples compiláveis** — Java moderno (records pra DTO/claims, `var`, switch); imports `jakarta.servlet.*` (Boot 3); lambda DSL no `SecurityFilterChain`; `properties`/`yaml`/`json` em fences corretas.
5. **Comparações justas** — authn vs authz, URL-based vs method-level, `hasRole` vs `hasAuthority`, RS256 vs HS256, Resource Server vs Client, CSRF on vs off, RBAC vs ABAC, stateless vs stateful, optimistic vs pessimistic (n/a aqui): sempre "quando X" E "quando Y". As capstones (17/18) são o ápice (trace + checklist production-grade, sem dogma).
6. **Wikilinks sem backticks** em "Veja também"; MOC do galho + MOC central obrigatórios. **Não linkar galhos inexistentes** (13/16/17) — texto "(planejado)".
7. **Code fences corretos:** ` ```java ` pra código, ` ```yaml `/` ```properties ` pra config, ` ```json ` pra payloads/claims, ` ```html ` pra form CSRF, ` ```text ` pra diagrama do filter chain/output. Sempre fechadas.
8. **`fase:` no frontmatter + na tag** — obrigatório.
9. **Higiene de commits** — sem `Co-Authored-By: Claude`, sem `--no-verify`, `git add <path>` nominal (nunca `-A` — bot de backup Obsidian Git roda em timer), 1 commit por nota, controlador commita (subagents write-only). Guardar contra `.git/index.lock`.
10. **Tom pedagógico graduado** — Iniciado assume Galhos 1-2 + 8 (container/AOP básico) + 9 (a camada web); Magus assume o galho inteiro + Galhos 8-9.

## 5. Conteúdo por nota (síntese)

Esboço do recorte. Todas as notas partem do tronco `Spring Security.md` refinado e higienizado; afirmações version-specific re-fundadas em doc oficial via WebFetch. Fonte-base: `docs.spring.io/spring-security/reference/` (+ OAuth2/OIDC RFCs e OWASP cheat sheets nas notas específicas).

- **01 — O que é Spring Security (refator, opus).** Authn vs authz; o filter chain como modelo mental (request → `FilterChainProxy` → `SecurityFilterChain` → `DispatcherServlet`); config 6.x (`SecurityFilterChain` bean + lambda DSL; `WebSecurityConfigurerAdapter` removido na 6.0 — **WebFetch**). A **dupla fronteira numa frase**: o chain senta na frente do `DispatcherServlet` (G9), method security roda sobre AOP (G8). Armadilhas: misturar authn e authz; `WebSecurityConfigurerAdapter` (legado, removido); achar que "Spring Security = login form". Fonte: docs.spring.io/spring-security (architecture).
- **02 — SecurityContext, Authentication e Principal (refator).** `SecurityContextHolder` (`ThreadLocal`); `Authentication` (extends `Principal`) com `getPrincipal`/`getAuthorities`/`getCredentials`; `GrantedAuthority`; `@AuthenticationPrincipal`. Armadilhas: `getPrincipal()` sem checar tipo (`ClassCastException`); `SecurityContextHolder` vazando auth entre requests em thread pool (clear); assumir principal sempre não-nulo. Fonte: docs.spring.io/spring-security (authentication architecture).
- **03 — Autenticação (refator, opus).** Tabela "tipos de auth / quando usar"; `UserDetailsService.loadUserByUsername` (auto-detectado como bean, mapeia `User`/`Role` → `UserDetails`); `AuthenticationManager` → `AuthenticationProvider` → `UserDetailsService`/`PasswordEncoder`; Form login vs HTTP Basic (HTTPS). Armadilhas: erro de auth vazando info ("user not found" vs "wrong password"); Basic sem HTTPS; não tratar `UsernameNotFoundException`. Fonte: docs.spring.io/spring-security (authentication, UserDetailsService).
- **04 — Password encoding (refator + research).** Nunca plain text; `PasswordEncoder` (`encode`/`matches`); BCrypt (default, work factor, slow-by-design) vs Argon2 vs Pbkdf2; `DelegatingPasswordEncoder` (prefixo `{bcrypt}$...`, migração). **WebFetch** (encoders atuais, `NoOpPasswordEncoder` deprecated). Armadilhas: plain text; `NoOpPasswordEncoder` em produção; work factor baixo demais. Fonte: docs.spring.io/spring-security (password storage).
- **05 — Autorização baseada em URL (refator + research).** `authorizeHttpRequests` (substituiu `authorizeRequests` — **WebFetch**) + `requestMatchers` (substituiu `antMatchers`); `permitAll`/`authenticated`/`hasRole`/`hasAuthority`/`denyAll`; `hasRole("ADMIN")` → `ROLE_ADMIN`; matcher por `HttpMethod`; RBAC básico. **Quita a dívida do Actuator** (proteger `/actuator/**`). Armadilhas: `antMatchers`/`authorizeRequests` legados; `hasRole("ROLE_ADMIN")` (prefixo duplicado); ordem de matchers (mais específico primeiro); `permitAll` em endpoint sensível. Fonte: docs.spring.io/spring-security (authorize-http-requests).
- **06 — A arquitetura do filter chain em profundidade (refator, opus).** `FilterChainProxy`; a ordem dos filtros (diagrama higienizado); múltiplos `SecurityFilterChain` (`securityMatcher`); `ExceptionTranslationFilter` (401 vs 403); `addFilterBefore`/`After`. **`Filter` genérico (G9 nota 11) vs `SecurityFilterChain`** — o contraste explícito. Linka **G9 nota 11**, **G7 nota 03** (Servlet API). Armadilhas: filtro custom na posição errada; assumir 1 só chain; confundir `Filter` (Servlet) com `SecurityFilterChain`. Fonte: docs.spring.io/spring-security (architecture, FilterChainProxy).
- **07 — Method security (refator + research, opus).** `@EnableMethodSecurity` (substituiu `@EnableGlobalMethodSecurity` — **WebFetch**); `@PreAuthorize`/`@PostAuthorize`/`@PreFilter`/`@PostFilter`; SpEL (`hasRole`, `#param`, `authentication.principal`, `@bean`); URL-based grossa vs method-level granular. **O mecanismo é o proxy AOP** → linka **G8 nota 09** (AOP) + **nota 10** (`@PreAuthorize` em `private`/self-invocation não funciona). Armadilhas: esquecer `@EnableMethodSecurity` (anotação ignorada silenciosamente); `@PreAuthorize` em método `private` (proxy); `@PostAuthorize` carregando dado caro antes de negar. Fonte: docs.spring.io/spring-security (method security).
- **08 — JWT (refator, opus).** Header/payload/signature (base64, não cripto); claims (`iss`/`sub`/`aud`/`exp`/`nbf`/`jti`); RS256/ES256 (assimétrico) vs HS256; **`alg: none` e whitelist**; stateless; prós/contras (revogação → forward-link nota 13). Armadilhas: `alg: none` aceito; não validar `aud`/`iss`; claim sensível no payload (é base64); JWT em localStorage (XSS). Fonte: docs.spring.io/spring-security (oauth2 jwt), OWASP JWT cheat sheet, RFC 7519.
- **09 — OAuth2 Resource Server (refator + research, opus).** `oauth2ResourceServer().jwt()`; `issuer-uri`/`jwk-set-uri` (**JWKS**, rotação); `JwtAuthenticationConverter` (claim → authority, prefixo `SCOPE_`/`ROLE_`); `@AuthenticationPrincipal Jwt`; `STATELESS` + CSRF off. **WebFetch.** Armadilhas: CSRF on numa API stateless (quebra clients); não configurar `issuer-uri` (não valida `iss`); converter ausente (authorities vazias). Fonte: docs.spring.io/spring-security (oauth2 resource server jwt).
- **10 — CSRF (refator + research).** O ataque; **CSRF on por default** (**WebFetch**); web app com sessão **mantém** (token em form/`CookieCsrfTokenRepository`); API stateless com JWT **desliga** (header não enviado automaticamente); SPA + cookie (`X-XSRF-TOKEN`). Armadilhas: desabilitar CSRF em web app com sessão; manter CSRF em API stateless; SPA sem ler o cookie `XSRF-TOKEN`. Fonte: docs.spring.io/spring-security (csrf).
- **11 — CORS (refator).** Mecanismo do **browser** (não server-side — `curl` bypassa); `CorsConfigurationSource`; preflight OPTIONS; `allowedOrigins("*")`+`allowCredentials(true)` rejeitado; `.cors()` no filter chain. **vs CORS como config MVC do G9** (aqui é a borda de segurança). Linka **G9**. Armadilhas: `*` + credentials; assumir que CORS protege o servidor; preflight não permitido. Fonte: docs.spring.io/spring-security (cors).
- **12 — OAuth2/OIDC Client e grant types (refator, opus).** `oauth2Login`/`OidcUser`; OAuth2 (delegação) vs OIDC (identidade, `id_token`); authorization code + PKCE; client credentials; implicit/password deprecated. OAuth2 em gateway/microservices → G16 (texto). Armadilhas: implicit flow em código novo; client secret no front-end (SPA → PKCE); confundir OAuth2 (authz) com OIDC (authn). Fonte: docs.spring.io/spring-security (oauth2 client), OIDC Core, RFC 6749/9700.
- **13 — Refresh tokens e revogação (refator).** Trade-off stateless vs revogação; access curto + refresh server-side (UUID); rotação; tabela `refresh_tokens`; revogação imediata (logout/troca de senha); blacklist quebra stateless; armazenamento (HttpOnly Secure SameSite vs localStorage). Armadilhas: refresh token como JWT (revogação difícil); refresh em localStorage; não rotacionar refresh. Fonte: docs.spring.io/spring-security, OWASP (session/token management).
- **14 — Autorização avançada (refator).** `AuthorizationManager` + `.access()`; RBAC (cobre a maioria) vs ABAC (SpEL/atributos) vs ReBAC (OpenFGA/SpiceDB — menção); `RoleHierarchy`; "owner só vê o próprio recurso". Armadilhas: lógica de negócio demais no SpEL (ilegível); RBAC onde o domínio pedia ABAC; role hierarchy implícita esquecida. Fonte: docs.spring.io/spring-security (authorization, AuthorizationManager).
- **15 — Session management e security headers (refator).** STATELESS (JWT) vs stateful (`JSESSIONID`); session fixation (`migrateSession` — default); concurrent sessions; Spring Session/Redis (menção); security headers (HSTS, CSP, `X-Frame-Options`, `nosniff`, `Referrer-Policy`). Armadilhas: stateful numa API que devia ser stateless; CSP `unsafe-inline` derrotando o propósito; esquecer HSTS atrás de proxy (`ForwardedHeaderFilter`). Fonte: docs.spring.io/spring-security (session management, headers).
- **16 — OWASP Top 10 no contexto Java (refator, síntese).** Top 10 → defesas do galho (Broken Access Control → method security/authz; Crypto Failures → BCrypt/HTTPS/JWT assinado; Injection → JPA params (G10); Misconfiguration → CSRF/CORS/headers; Auth Failures → password/session/refresh). **Sem estatística inventada.** Defense-in-depth conceitual. Armadilhas de raciocínio: "auth perfeita basta" (monitoramento conta); "CORS protege o servidor"; "framework cobre tudo automaticamente". Fonte: OWASP Top 10, OWASP cheat sheets (Authentication, Access Control).
- **17 — Capstone-trace: uma request autenticada do token à autorização no método (refator, opus).** **Trace:** `Authorization: Bearer <jwt>` → `BearerTokenAuthenticationFilter` → validação (assinatura/JWKS, `iss`/`aud`/`exp`) → `JwtAuthenticationConverter` → `Authentication` no `SecurityContextHolder` → `AuthorizationFilter` (URL) → `DispatcherServlet` → controller → `@PreAuthorize` (proxy AOP — G8) → service; caminho do 401 vs 403 via `ExceptionTranslationFilter`. Armadilhas de raciocínio: "o token chega direto no controller" (há o filter chain); "autorização é só no controller" (URL + método); "validar JWT é só checar assinatura" (`iss`/`aud`/`exp`/`alg`). Fonte: docs.spring.io/spring-security (architecture, oauth2).
- **18 — Capstone-checklist: projetando a segurança de uma API production-grade (refator, opus).** Checklist (`SecurityFilterChain` + lambda DSL; stateless + Resource Server; CSRF off/on; CORS explícito; method security; `DelegatingPasswordEncoder`; headers; refresh server-side). **Tabela "Galho 12 → mecanismo (G8) / borda (G9)"** (`@PreAuthorize`↔proxy AOP, `SecurityFilterChain`↔bean+Filter, CORS↔borda vs config MVC). **Menção** de teste de segurança (`@WithMockUser`/`with(jwt())`) → Galho 13 (texto). Cheatsheet nota→problema. Munição de entrevista. Armadilhas de raciocínio: desabilitar proteção "temporariamente"; confiar em dado do client pra authz; CORS como segurança. Fonte: docs.spring.io/spring-security, OWASP cheat sheets.

## 6. Pré-flight: verificações feitas

Executado nesta fase de brainstorming (2026-06-10); itens version-specific re-confirmados na execução de cada nota via WebFetch:

1. **Tronco mapeado** — `Backend/Spring Security.md` (1116 linhas, `publish: false`, `status: evergreen`) lido **inteiro**. Cobre todo o escopo do galho de forma monolítica. **Poda integral** (padrão JavaFX/Galho 6). Seções: O que é, Evolução da configuração (5.x legado vs 6.x), Filter Chain (+ SecurityContextHolder, Authentication vs Principal), Autenticação (tipos, Form, Basic, UserDetailsService, AuthenticationManager, Password encoding), JWT, OAuth2/OIDC, Autorização (URL, method-level, AuthorizationManager, RBAC/ABAC/ReBAC), CSRF, CORS, Session management, Security headers, Testando, Armadilhas comuns, Na prática (fabricação), How to explain in English (fabricação), Recursos, Veja também.
2. **Fabricação confirmada** — `Spring Security.md`: `Patient`/`Doctor`/`Appointment` no corpo (ex.: `PatientService` ~615, `@PreAuthorize` ~617-634, CORS `medespecialista.com` ~755, JWT `issuer-uri` ~361); `## Na prática (da minha experiência)` (~963-999, "3 fluxos de autenticação do MedEspecialista", "incidente memorável — JWT com `alg: none`" num pentest, "NPE em SecurityContext sob carga"); `## How to explain in English` 1ª pessoa (~1003-1032) + `### Frases úteis em entrevista`. **Some toda com a poda integral.** Notas usam `Order`/`Customer`/`User`/`Role` neutros.
3. **Dupla fronteira-assinatura confirmada** — Galho 8 (AOP nota 09, self-invocation nota 10, ApplicationContext nota 06) e Galho 9 (DispatcherServlet nota 06, Interceptors vs Filters nota 11) existem em `main`. Galho 7 nota 03 (Servlet API) existe. A nota 11 do Galho 9 (`:357`) **espera** o link-back deste galho.
4. **Dívida reversa localizada** — 6 ponteiros inline + 3 parágrafos de fronteira (§3.6), em: MOC central :42, Actuator (G8/17) :52/:111/:288, OpenAPI (G9/12) :167, Interceptors vs Filters (G9/11) :357, e os parágrafos Spring Core index :32 / Web index :32 / Persistência index :32. **NÃO quitar**: Reativa index :35 (segurança reativa = fronteira pra frente) e os horizonte-lists de uma linha (Spring Core :97, Web :95, Persistência :92). Confirmar linhas na execução.
5. **Dicionário** — **327 verbetes** após o Galho 11; seções alfabéticas únicas `## A`…`## Z`; verbetes `### `; `updated: 2026-06-10`. Verbetes possivelmente já existentes (Galho 7/9: `CORS`, `Filter`, `Servlet`, `DispatcherServlet`, `access token`/`scope`) — conferir e linkar, nunca duplicar. Expansão alfabética (~35), nunca recriar/reordenar; conferir âncoras 1:1.
6. **MOC central** — `03-Dominios/Tecnologia/Java/index.md:42` é a linha do Galho 12 (`*(planejado)*`); galhos ativos usam `N. [[path/index|Title]] — summary`; `updated: 2026-06-10`.
7. **Troncos intocáveis** — `Backend/Spring Boot.md` (podado 8/9/10), `Backend/Spring Data JPA.md` (hub Galho 10), `Backend/Kafka/` + `Backend/gRPC e Go.md` (Galho 14), `Backend/Testes em Java.md` (Galho 13). Pasta `Segurança/` ainda **não existe**.
8. **Versões a cravar via WebFetch na execução** — Spring Security 6.x (baseline Boot 3.x, `jakarta.*`, Java 17): `WebSecurityConfigurerAdapter` removido na 6.0; `authorizeHttpRequests`/`requestMatchers`; `@EnableMethodSecurity`; CSRF default on; `DelegatingPasswordEncoder`; OAuth2 Resource Server (JWKS/`issuer-uri`) vs Client; PKCE no authorization code. Citando Security 7.x / Boot 4.x como "mais recente" quando relevante. Fonte: `docs.spring.io/spring-security/reference/`, OAuth2/OIDC RFCs, OWASP cheat sheets.

Nenhum número de adoção/segurança é inventado. Quando faltar fato verificável, **PERGUNTAR** antes de escrever.

## 7. Critérios de aceitação do galho

Além dos critérios gerais (§10 do roadmap):

1. 18 notas em `03-Dominios/Tecnologia/Java/Segurança/`, frontmatter completo com `fase:`, `publish: true`, distribuídas 5/6/7.
2. MOC do galho com 3 subseções de fase + 5 rotas alternativas + dataview + folder-link resolve (`index.md` presente).
3. Dicionário de Java **expandido** (não recriado) com ~35 verbetes; verbetes dos Galhos 1-11 intactos; `updated: 2026-06-10`; dups conferidos e linkados (não duplicar `CORS`/`Filter`/`Servlet`/`DispatcherServlet`/`scope`/`access token` se vierem dos Galhos 7/9); headings conferidos 1:1 com as âncoras usadas nas notas (via grep).
4. MOC central `Java/index.md` com Galho 12 ativado (linha 42 vira wikilink); resto intacto.
5. **Poda integral do tronco executada**: `Spring Security.md` reduzido a hub (poda integral, fabricação do MedEspecialista/incidentes/`How to explain` some, `publish: false` mantido). **Outros troncos intactos** (`Spring Boot.md`, `Spring Data JPA.md`, `Kafka/`, `Testes em Java.md`).
6. **Dívida reversa quitada**: os 6 ponteiros inline + 3 parágrafos de fronteira com wikilinks corretos (Actuator :52/:111/:288→nota 05, OpenAPI :167→nota 01/MOC, Interceptors :357→nota 06, parágrafos →MOC do galho); galhos ainda inexistentes (13/16/17) permanecem texto "(planejado)"; Reativa index :35 (segurança reativa) e horizonte-lists intactos.
7. Cada nota: TL;DR; code samples compiláveis (Java moderno, lambda DSL, `jakarta.*`, fences corretas — `java`/`yaml`/`json`/`html`/`text`); "Em entrevista" com `### Frase pronta (inglês)` 3+ sentenças + `### Vocabulário` tabela 6+ termos PT→EN; "Armadilhas" com `### (N) Título` numerado + exemplo + fix (≥2 Iniciado, ≥3 Adepto/Magus); wikilinks (galho + MOC central + Galho 8 quando tocar mecanismo/method security + Galho 9 quando tocar filter/borda + Galho 7 na nota 06 + Dicionário); "Referências" com docs oficiais verificadas.
8. **Dupla fronteira-assinatura respeitada**: cada conceito que usa o mecanismo (method security/`SecurityFilterChain` bean) linka de volta ao Galho 8 sem re-explicar AOP; cada conceito que protege a borda (filter chain/CORS) linka o Galho 9 sem re-explicar o pipeline; Servlet API (G7) só na nota 06; galhos 13/16/17 só como texto "(planejado)"; nenhum wikilink pra galho inexistente.
9. **Fronteiras de escopo respeitadas**: segurança **servlet/MVC** (WebFlux Security/reativa = menção "(planejado)"); proteção dos endpoints do Actuator quitada (nota 05), observabilidade = Galho 17; OAuth2 em gateway/microservices = Galho 16 (texto); testes de segurança só citados (`@WithMockUser`/`with(jwt())`/Keycloak = Galho 13); segurança a nível de dados (row-level/field encryption/`AuditorAware`) tocada de leve; zero conteúdo profundo de Reativa/Microservices/Test/Dados.
10. Zero fabricação de experiência pessoal; zero estatística de adoção/segurança inventada (vale pro OWASP); afirmações version-specific citam a versão verificada via WebFetch.
11. 1 commit por nota; sem `Co-Authored-By: Claude`; sem `--no-verify`; stage nominal (nunca `-A`); subagents write-only, controlador commita.
12. `verificar-wikilinks` roda limpo na pasta do galho (as quebras legadas da árvore Java NÃO são deste galho; evitar âncoras same-file).

## 8. Riscos e mitigações

| Risco | Mitigação |
|---|---|
| **Re-explicar o mecanismo (AOP/proxy do `@PreAuthorize`, bean)** em vez de linkar ao Galho 8 (1ª face) | Restrição 4.3.1; a nota 07 cobre **method security** (comportamento), linka o **mecanismo** (G8 notas 09/10); review por fase; capstone mapeia em tabela. |
| **Re-explicar a camada web (DispatcherServlet, Filter, pipeline)** em vez de linkar ao Galho 9 (2ª face) | Restrição 4.3.1; notas 01/06/11 linkam G9 notas 06/11; o filter chain é a **camada de segurança** sobre o pipeline, não o pipeline. |
| **Copiar fabricação do tronco** (`Patient`/MedEspecialista/"incidente memorável"/"durante um pentest"/`alg: none` no MedEspecialista) pras notas | O tronco é contraexemplo (restrição 4.3.2); poda integral faz a fabricação sumir; exemplos neutros `Order`/`Customer`/`User`/`Role`; review por fase grep `Patient\|MedEspecialista\|minha\|Doctor\|Appointment\|pentest\|incidente memorável`. |
| **Inventar estatística de segurança** (OWASP "X% das brechas...") | Restrição 4.3.2; nota 16 é mapeamento **conceitual** Top 10 → defesas, sem número; review da nota 16. |
| **Poda integral perder conteúdo bom** do `Spring Security.md` | O conteúdo bom **migra pras notas** (refinado/higienizado) ANTES da poda; a poda é o último passo; commit reversível. |
| **Config legada/stale do tronco** (`WebSecurityConfigurerAdapter`, `authorizeRequests`, `antMatchers`, `@EnableGlobalMethodSecurity`) vazar pras notas como se fosse atual | WebFetch no Step 1 das notas 01/05/07; o legado aparece **só** como "armadilha: isso foi removido na 6.0, use X"; baseline Security 6.x. |
| **Inventar API/versão "de memória"** (CSRF default, JWKS, PKCE, encoders) | WebFetch no Step 1 das notas version-specific (01/04/05/07/09/10); Referências com fonte oficial; nada "de memória". |
| **Invadir Galho 16 (microservices)** ao falar de OAuth2/gateway | OAuth2 num gateway/SSO entre serviços = texto "(planejado)"; o foco é a app única (Resource Server/Client); review por fase. |
| **Invadir Galho 13 (testes)** ao falar de `@WithMockUser`/Testcontainers | Citar que se testa com mock user / JWT de teste, sem ensinar a stack; capstone (18) menciona como fronteira. |
| **Invadir segurança reativa** (WebFlux Security) | Foco servlet/MVC; `ReactiveSecurityContextHolder`/`Mono<Authentication>` = menção "(planejado)"; Reativa index :35 permanece "(planejado)". |
| Galho denso (18 notas) inflar notas individuais (filter chain/JWT/OAuth2/method security) | Distribuição 5/6/7 fixada; se uma nota passar de ~600 linhas, dividir nota (não galho — Resource Server ficou separado de JWT, Client de Resource Server, headers junto de session); capstones com cheatsheet enxuto. |
| Dicionário: duplicar verbete já existente (`CORS`, `Filter`, `Servlet`, `scope`) | Grep dos existentes antes de inserir; quando tocar um existente, **linkar** em vez de duplicar; inserção alfabética, nunca recriar; conferir âncoras 1:1. |
| Bot de backup (Obsidian Git) commitando no meio | Padrão dos Galhos 2-11: subagents write-only; controlador commita imediatamente após cada nota com `git add` nominal (nunca `-A`); guardar contra `.git/index.lock`. |

## 9. Próximos passos

1. **Aprovação deste spec**
2. **Plano de execução** via skill `superpowers:writing-plans` → `docs/superpowers/plans/2026-06-10-java-galho-12-seguranca-execution.md`
3. **Execução** via `superpowers:subagent-driven-development` **direto na `main`** (subagents write-only; sonnet por padrão, opus nas notas 01/03/06/07/08/09/12/17/18; review **por fase** + fix loop; push manual do usuário)
4. **Verificação** de wikilinks + conferência de âncoras do Dicionário
5. **Atualização da memória** `project_trilha_java` (Galho 12 completo) antes do próximo galho

## 10. Documentos relacionados

- `2026-06-02-java-senior-roadmap-design.md` — roadmap macro (18 galhos)
- `2026-06-09-java-galho-10-persistencia-design.md` / `...-execution.md` — Galho 10 (molde direto de **poda integral** de tronco monolítico + dupla/tripla fronteira + dívida reversa; este galho usa-o como template direto)
- `2026-06-10-java-galho-11-reativa-design.md` / `...-execution.md` — Galho 11 (molde mais recente de poda cirúrgica + dívida reversa + fronteira honesta; segurança reativa fica como fronteira pra frente)
- `2026-06-08-java-galho-09-web-rest-design.md` — Galho 9 (dependência: a camada web que a segurança protege; a nota 11 espera o link-back)
- `2026-06-08-java-galho-08-spring-core-design.md` — Galho 8 (dependência: o mecanismo AOP que faz method security funcionar; o `SecurityFilterChain` é um bean)
- Galho 6 (JavaFX) — template de **poda integral** de tronco monolítico (`Frontend/JavaFX.md` reduzido a hub)
- Artefatos a atualizar: `03-Dominios/Tecnologia/Java/Dicionário de Java.md`, `03-Dominios/Tecnologia/Java/index.md`, `03-Dominios/Tecnologia/Java/Backend/Spring Security.md` (poda integral), `Spring Core e Boot/17 - Actuator`, `Spring Core e Boot/index.md`, `Web e APIs REST/11 - Interceptors vs Filters`, `Web e APIs REST/12 - OpenAPI`, `Web e APIs REST/index.md`, `Persistência de dados/index.md` (dívida reversa)
- Fonte-base do galho: `docs.spring.io/spring-security/reference/` (+ OAuth2/OIDC RFCs 6749/9700/OIDC Core, OWASP Top 10 + cheat sheets nas notas específicas)
- Memórias: [[project_trilha_java]], [[project_trilhas_fases_aprendizado]], [[project_tronco_galhos_pattern]], [[feedback_galhos_direto_main]], [[feedback_no_fabrication]], [[feedback_quartz_index]], [[feedback_commits]], [[feedback_dataview_inline_code]], [[feedback_notas_atomicas]], [[feedback_enriquecimento_feynman]]
