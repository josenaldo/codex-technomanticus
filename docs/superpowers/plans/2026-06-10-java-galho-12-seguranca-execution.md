# Galho 12 — Segurança (Java Senior) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Criar o Galho 12 da trilha Java Senior — 18 notas atômicas (filter chain, SecurityContext, autenticação, password encoding, autorização URL, method security, JWT, OAuth2 Resource Server, CSRF, CORS, OAuth2/OIDC Client, refresh tokens, autorização avançada, session+headers, OWASP, capstone-trace, capstone-checklist) em 3 fases + MOC do galho + expansão do Dicionário + ativação do MOC central + **poda INTEGRAL** do tronco `Backend/Spring Security.md` + **quitação de 6 ponteiros inline + 3 parágrafos de dívida reversa**.

**Architecture:** Padrão galhos + 3 fases (Iniciado/Adepto/Magus). Pasta flat `03-Dominios/Java/Segurança/`, notas `publish: true` em PT-BR, numeração global 01-18 (5/6/7). **Galho HÍBRIDO — REFATOR (poda integral de tronco monolítico) + PESQUISA:** o tronco `Spring Security.md` (1116 linhas, `publish: false`) cobre todo o escopo de forma monolítica e contaminada de fabricação → **poda INTEGRAL** (padrão JavaFX/Galho 10 — vira hub de ~20 linhas, toda a fabricação MedEspecialista/pentest/incidentes evapora); as notas nascem higienizadas, com afirmações version-specific re-fundadas em doc oficial via WebFetch. **DUPLA fronteira-assinatura:** cada conceito que usa o mecanismo (method security/`SecurityFilterChain` bean) linka de volta ao **Galho 8** (sem re-explicar AOP); cada conceito que protege a borda web (filter chain na frente do `DispatcherServlet`, `Filter` genérico vs `SecurityFilterChain`, CORS) linka o **Galho 9** (sem re-explicar o pipeline); a Servlet API por baixo (toque leve) linka o **Galho 7** só na nota 06. **Foco servlet/MVC:** segurança reativa (WebFlux Security) = menção "(planejado)". Galhos 13/16/17 = texto "(planejado)", sem wikilink. **Direto na `main`** ([[feedback_galhos_direto_main]]); push manual do usuário.

**Tech Stack:** Obsidian Flavored Markdown, frontmatter YAML, wikilinks, callouts, Dataview, Quartz v4. Verificação via WebFetch (`docs.spring.io/spring-security/reference/`, OAuth2/OIDC RFCs, OWASP Top 10 + cheat sheets).

---

## Convenções aplicadas a TODAS as notas (ler antes de qualquer task)

**Frontmatter** (ajustar `title`/`fase`/`tags`/`aliases` por nota; `created`/`updated: 2026-06-10`):

```yaml
---
title: "<título sem prefixo numérico>"
created: 2026-06-10
updated: 2026-06-10
type: concept
progress: backlog
status: seedling
publish: true
fase: iniciado | adepto | magus
tags:
  - java
  - seguranca
  - <fase>
  - <1-3 tags de conceito: spring-security, filter-chain, autenticacao, autorizacao, password, jwt, oauth2, oidc, method-security, csrf, cors, session, rbac, owasp>
aliases:
  - <aliases>
---
```

H1 `# Título` após o frontmatter (padrão dos galhos publicados).

**Estrutura H2 obrigatória** (nesta ordem):

1. `> [!abstract] TL;DR` — 2-4 linhas. Callout, NÃO H2.
2. `## O que é` — definição.
3. `## Por que importa` — relevância pra senior/entrevista. (Pode fundir com "O que é" em Iniciado curtas.)
4. `## Como funciona` — H3s; mínimo 3 em Adepto/Magus.
5. `## Na prática` — código compilável; framing neutro; **NUNCA** 1ª pessoa, `Patient`, `Doctor`, `Appointment`, `Josenaldo`, `MedEspecialista`, "durante um pentest", "incidente memorável". Domínios neutros: `Order`, `Customer`, `User`, `Role`, `OrderController`, `UserService`. Records pra DTO/claims. Imports `jakarta.servlet.*` (Boot 3); lambda DSL no `SecurityFilterChain`.
6. `## Armadilhas` — ≥2 (Iniciado) / ≥3 (Adepto/Magus). Cada uma: `### (N) Título` + descrição + exemplo curto + fix em 1 linha (H3 numerado, NÃO callout `[!warning]`).
7. `## Em entrevista` — `### Frase pronta (inglês)` com **3+ sentenças** (trade-off + decisão + caveat) + `### Vocabulário` **6+ termos** em tabela `| Termo PT | Termo EN |`.
8. `## Veja também` — wikilinks SEM backticks, SEM âncoras same-file `[[#...]]`. Sempre: notas do galho + `[[03-Dominios/Java/Segurança/index|Segurança (MOC do galho)]]` + `[[03-Dominios/Java/index|Trilha Java]]` + (quando tocar mecanismo AOP/method security/bean) a nota do **Galho 8** + (quando tocar filter/DispatcherServlet/CORS/borda) a nota do **Galho 9** + (nota 06) a Servlet API do **Galho 7** + verbetes do Dicionário.
9. `## Referências` — docs oficiais consultadas (`docs.spring.io/spring-security/...`, OAuth2/OIDC RFCs, OWASP cheat sheets).

**Tamanho:** 200-500 linhas (densas até 600 — limite de [[feedback_notas_atomicas]]).

**Restrições absolutas:**
- **DUPLA fronteira-assinatura.** Mapeamento de link-back **Galho 8** (o mecanismo, não re-explicar AOP): method security/`@PreAuthorize` roda sobre proxy → `Spring Core e Boot/09 - AOP e proxies no Spring`; o limite do proxy (`private`/`final`/self-invocation) → `Spring Core e Boot/10 - Self-invocation e os limites do proxy`; o `SecurityFilterChain` é um bean → `Spring Core e Boot/06 - ApplicationContext — o container e seu ciclo`. Mapeamento **Galho 9** (a camada web que a segurança protege): o filter chain na frente do DispatcherServlet → `Web e APIs REST/06 - O pipeline do DispatcherServlet`; `Filter` genérico vs `SecurityFilterChain` → `Web e APIs REST/11 - Interceptors vs Filters`; CORS como config MVC → `Web e APIs REST/11 - Interceptors vs Filters` (o ponto onde o Galho 9 tratou filtros) e a borda. Mapeamento **Galho 7** (toque leve, só nota 06): a Servlet API por baixo do chain → `Jakarta EE/03 - Servlet API — o alicerce HTTP`.
- **Galhos 13/16/17 só como texto "(planejado)", SEM wikilink.** Greps de review checam `\[\[[^]]*(Galho (13|16|17)|Testcontainers|Keycloak|Spring Cloud|circuit breaker|WebFlux Security|ReactiveSecurityContext)`.
- Sem fabricação ([[feedback_no_fabrication]]); usar `Order`/`Customer`/`User`/`Role`. **Zero estatística de adoção/segurança inventada** — vale **DOBRADO** pra nota 16 (OWASP): mapeamento **conceitual** Top 10 → defesas, sem "X% das brechas são...", sem "a maioria dos ataques", sem market share. O tronco tem `## Na prática (da minha experiência)` com 3 incidentes fabricados e `## How to explain in English` em 1ª pessoa — **contraexemplo, jamais copiar**.
- **Pesquisa pras partes version-specific:** notas 01/04/05/07/09/10 fundam-se em WebFetch (Step 1); qualquer outra que cravar versão também confirma. Toda afirmação version-specific verificada: **`WebSecurityConfigurerAdapter` removido na 6.0** (usa-se `SecurityFilterChain` bean + lambda DSL); **`authorizeHttpRequests` substituiu `authorizeRequests`**; **`requestMatchers` substituiu `antMatchers`**; **`@EnableMethodSecurity` substituiu `@EnableGlobalMethodSecurity`**; **CSRF habilitado por default**; `DelegatingPasswordEncoder`/prefixo `{id}`; OAuth2 Resource Server (JWKS/`issuer-uri`) vs Client; PKCE no authorization code. Spring Security 7.x / Boot 4.x já existem — **manter Security 6.x / Boot 3.x como baseline** (como os Galhos 8/9/10/11; `jakarta.*`, Java 17), citando 7.x/4.x como "mais recente" quando relevante. Nada de memória.
- **Não re-explicar o que é de outro galho:** AOP/proxy/self-invocation/IoC/bean/container → Galho 8 (linkar); DispatcherServlet/`Filter` genérico/pipeline MVC/CORS como config MVC → Galho 9 (linkar); Servlet API por baixo → Galho 7 (linkar, só nota 06); SQL injection (mecânica de query) → Galho 10 (linkar na nota 16); HTTPS/TLS/certificados → nota [[Redes e Protocolos]] (linkar); testes de segurança (`@WithMockUser`/`with(jwt())`/Testcontainers/Keycloak) → Galho 13 (texto — citar, sem ensinar); OAuth2 em gateway/SSO microservices → Galho 16 (texto); segurança reativa (WebFlux Security/`ReactiveSecurityContextHolder`) → fora do escopo, menção "(planejado)"; observabilidade do Actuator → Galho 17 (texto — mas a **proteção** dos endpoints é quitada aqui).
- Comparações justas (quando X E quando Y): authn vs authz, URL-based vs method-level, `hasRole` vs `hasAuthority`, RS256 vs HS256, Resource Server vs Client, CSRF on vs off, RBAC vs ABAC, stateless vs stateful.
- Code fences: ` ```java `, ` ```yaml `/` ```properties ` (config), ` ```json ` (claims/payload), ` ```html ` (form CSRF), ` ```text ` (diagrama do filter chain/output). Sempre fechadas.
- Commits: sem `Co-Authored-By: Claude`; sem `--no-verify`; `git add <path>` nominal (bot de backup roda em timer — NUNCA `-A`; guardar contra `.git/index.lock`); 1 commit por nota; direto na `main`; **sem push, sem deploy**. Subagents NÃO rodam git — o controlador commita.

**Modelo por nota:** sonnet por padrão; **opus** nas **01** (assinatura/filter chain), **03** (autenticação), **06** (filter chain a fundo), **07** (method security + AOP), **08** (JWT), **09** (Resource Server), **12** (OAuth2/OIDC Client), **17** (capstone-trace) e **18** (capstone-checklist).

**Fontes oficiais (base):**
- Spring Security reference: `https://docs.spring.io/spring-security/reference/`
- Architecture / FilterChainProxy: `https://docs.spring.io/spring-security/reference/servlet/architecture.html`
- Authentication / UserDetailsService: `https://docs.spring.io/spring-security/reference/servlet/authentication/index.html`
- Password storage: `https://docs.spring.io/spring-security/reference/features/authentication/password-storage.html`
- Authorize HTTP requests: `https://docs.spring.io/spring-security/reference/servlet/authorization/authorize-http-requests.html`
- Method security: `https://docs.spring.io/spring-security/reference/servlet/authorization/method-security.html`
- OAuth2 Resource Server (JWT): `https://docs.spring.io/spring-security/reference/servlet/oauth2/resource-server/jwt.html`
- OAuth2 Client / login: `https://docs.spring.io/spring-security/reference/servlet/oauth2/client/index.html`
- CSRF: `https://docs.spring.io/spring-security/reference/servlet/exploits/csrf.html`
- CORS: `https://docs.spring.io/spring-security/reference/servlet/integrations/cors.html`
- Session management: `https://docs.spring.io/spring-security/reference/servlet/authentication/session-management.html`
- Security HTTP headers: `https://docs.spring.io/spring-security/reference/servlet/exploits/headers.html`
- OWASP Top 10: `https://owasp.org/www-project-top-ten/` · cheat sheets: `https://cheatsheetseries.owasp.org/`
- RFCs: OAuth2 `https://datatracker.ietf.org/doc/html/rfc6749`, BCP `https://datatracker.ietf.org/doc/html/rfc9700`, JWT `https://datatracker.ietf.org/doc/html/rfc7519`, OIDC `https://openid.net/specs/openid-connect-core-1_0.html`

---

## Task 0: Pré-flight — pasta, terreno e baselines

**Files:**
- Create: `03-Dominios/Java/Segurança/` (pasta)

- [ ] **Step 1: Confirmar `main`**

```bash
git branch --show-current
```
Expected: `main`. NÃO criar branch.

- [ ] **Step 2: Criar a pasta do galho**

```bash
mkdir -p "03-Dominios/Java/Segurança"
```

- [ ] **Step 3: Confirmar títulos exatos das notas dos Galhos 7/8/9 (linkadas de volta)**

```bash
ls "03-Dominios/Java/Spring Core e Boot/" | grep -E "^(06|09|10|17) "
ls "03-Dominios/Java/Web e APIs REST/" | grep -E "^(06|11|12) "
ls "03-Dominios/Java/Jakarta EE/" | grep -E "^03 "
```
Expected: G8 — `06 - ApplicationContext — o container e seu ciclo`, `09 - AOP e proxies no Spring`, `10 - Self-invocation e os limites do proxy`, `17 - Actuator e observabilidade`; G9 — `06 - O pipeline do DispatcherServlet`, `11 - Interceptors vs Filters`, `12 - Documentando a API com OpenAPI e Swagger`; G7 — `03 - Servlet API — o alicerce HTTP`. Anotar divergências.

- [ ] **Step 4: Relocalizar a dívida reversa (6 ponteiros inline + 3 parágrafos — linhas podem ter mudado)**

```bash
grep -rn "Galho 12\|galho 12\|planejado" "03-Dominios/Java/Spring Core e Boot/17 - Actuator e observabilidade.md" "03-Dominios/Java/Spring Core e Boot/index.md" "03-Dominios/Java/Web e APIs REST/11 - Interceptors vs Filters.md" "03-Dominios/Java/Web e APIs REST/12 - Documentando a API com OpenAPI e Swagger.md" "03-Dominios/Java/Web e APIs REST/index.md" "03-Dominios/Java/Persistência de dados/index.md"
grep -n "Segurança\|planejado" "03-Dominios/Java/index.md"
```
Expected (anotar linhas reais pra Task 23): MOC central item 12 (`~42`); Actuator :52/:111/:288 (3 ponteiros); OpenAPI :167; Interceptors vs Filters :357; parágrafos de fronteira Spring Core index :32, Web index :32, Persistência index :32. **NÃO tocar:** Reativa index :35 ("segurança reativa Galho 12" — fronteira pra frente) e horizonte-lists Spring Core :97 / Web :95 / Persistência :92 (mantêm 13/16/17 "(planejado)").

- [ ] **Step 5: Baseline do Dicionário**

```bash
grep -cE "^### " "03-Dominios/Java/Dicionário de Java.md"
```
Expected: **327** (baseline pós-Galho 11). Anotar o número real.

- [ ] **Step 6: Ler o tronco a podar (pra Task 22) e mapear seções + fabricação**

```bash
grep -nE "^## " "03-Dominios/Java/Backend/Spring Security.md"
grep -niE "Patient|Doctor|Appointment|MedEspecialista|minha experiência|pentest|incidente memorável|How to explain" "03-Dominios/Java/Backend/Spring Security.md"
```
Expected: tronco monolítico `Backend/Spring Security.md` (1116 linhas, `publish: false`) com seções O que é / Evolução da configuração / Filter Chain / Autenticação / JWT / OAuth2 e OIDC / Autorização / CSRF / CORS / Session management / Security headers / Testando / Armadilhas comuns / **Na prática (da minha experiência)** (~963, fabricação) / **How to explain in English** (~1003, fabricação 1ª pessoa) / Recursos / Veja também. **Poda INTEGRAL** (todo o corpo vira hub). Anotar a linha do frontmatter pra preservar.

- [ ] **Step 7: Fixar fatos a verificar via WebFetch** — `WebSecurityConfigurerAdapter` removido na 6.0 (usa-se `SecurityFilterChain` bean + lambda DSL); `authorizeHttpRequests` substituiu `authorizeRequests`; `requestMatchers` substituiu `antMatchers`; `@EnableMethodSecurity` substituiu `@EnableGlobalMethodSecurity`; CSRF default on; `DelegatingPasswordEncoder` (`NoOpPasswordEncoder` deprecated); OAuth2 Resource Server (`issuer-uri`/JWKS) vs Client; PKCE no authorization code; baseline Security 6.x / Boot 3.x. Nada de memória.

- [ ] **Step 8: Sem commit** (preparação).

---

## Fase INICIADO (notas 01-05)

### Task 1: Nota 01 — O que é Spring Security — authn, authz e o filter chain ⟦opus⟧

**Files:**
- Create: `03-Dominios/Java/Segurança/01 - O que é Spring Security — authn, authz e o filter chain.md`

- [ ] **Step 1: Pesquisar (version-specific)** — WebFetch `https://docs.spring.io/spring-security/reference/servlet/architecture.html` + `https://docs.spring.io/spring-security/reference/servlet/getting-started.html`. CONFIRMAR: authentication (quem) vs authorization (o quê); `FilterChainProxy`/`SecurityFilterChain`; a config 6.x (`SecurityFilterChain` bean + lambda DSL; `@EnableWebSecurity`); **`WebSecurityConfigurerAdapter` removido na 6.0** (não usar). **WebFetch obrigatório.**

- [ ] **Step 2: Escrever** — `fase: iniciado`, tags `[java, seguranca, iniciado, spring-security, filter-chain]`, aliases `["Spring Security", "o que é Spring Security", "filter chain"]`. **Nota-assinatura da DUPLA fronteira.** Conteúdo:
  - TL;DR: Spring Security protege a app via um **filter chain** que intercepta cada request antes do `DispatcherServlet`; separa **autenticação** (quem você é) de **autorização** (o que pode); a config moderna (6.x) é um bean `SecurityFilterChain` com lambda DSL — o `WebSecurityConfigurerAdapter` foi removido.
  - `## O que é` — authn vs authz; o framework de segurança do ecossistema Spring.
  - `## Por que importa` — toda app séria precisa; entrevista cobra "o que é o filter chain e como uma request flui".
  - `## Como funciona` — H3s: "Autenticação vs autorização: dois conceitos, não misturar", "O filter chain: request → `FilterChainProxy` → `SecurityFilterChain` → `DispatcherServlet`", "Config 6.x: o bean `SecurityFilterChain` + lambda DSL (`WebSecurityConfigurerAdapter` foi removido na 6.0)", "A dupla fronteira: o chain senta na frente do DispatcherServlet (Galho 9), method security roda sobre AOP (Galho 8)".
  - `## Na prática` — um `SecurityFilterChain` mínimo (```java): `http.authorizeHttpRequests(...).httpBasic(...).build()`; o diagrama do fluxo request→chain→controller (```text).
  - `## Armadilhas` — ≥2: (1) misturar authn e authz (são coisas diferentes); (2) usar `WebSecurityConfigurerAdapter` (legado, removido na 6.0 — use o bean `SecurityFilterChain`); (3) achar que "Spring Security = formulário de login" (é o filter chain inteiro).
  - `## Em entrevista` + `## Veja também` ([[02 - SecurityContext, Authentication e Principal — o usuário atual]], [[06 - A arquitetura do filter chain em profundidade]], **[[03-Dominios/Java/Web e APIs REST/11 - Interceptors vs Filters|Interceptors vs Filters]]** (o `Filter` genérico vs o `SecurityFilterChain`), **[[03-Dominios/Java/Web e APIs REST/06 - O pipeline do DispatcherServlet|O pipeline do DispatcherServlet]]** (o chain senta na frente dele), MOC galho, MOC central, verbetes `Spring Security`/`SecurityFilterChain`/`FilterChainProxy`) + `## Referências`.

- [ ] **Step 3: Verificar**
```bash
grep -cE "^## (O que é|Por que importa|Como funciona|Na prática|Armadilhas|Em entrevista|Veja também|Referências)" "03-Dominios/Java/Segurança/01 - O que é Spring Security — authn, authz e o filter chain.md"
grep -riE "Patient|Doctor|Appointment|MedEspecialista|minha experiência|pentest" "03-Dominios/Java/Segurança/01 - O que é Spring Security — authn, authz e o filter chain.md"
grep -c "Web e APIs REST/11" "03-Dominios/Java/Segurança/01 - O que é Spring Security — authn, authz e o filter chain.md"
```
Expected: ≥7 seções; segundo grep **VAZIO**; terceiro ≥1 (link de volta ao Galho 9).

- [ ] **Step 4: Commit** — `git add "<path>"` && `git commit -m "feat(java): galho 12 nota 01 — o que é Spring Security (authn, authz e o filter chain)"`

### Task 2: Nota 02 — SecurityContext, Authentication e Principal — o usuário atual

**Files:**
- Create: `03-Dominios/Java/Segurança/02 - SecurityContext, Authentication e Principal — o usuário atual.md`

- [ ] **Step 1: Pesquisar** — WebFetch `https://docs.spring.io/spring-security/reference/servlet/authentication/architecture.html`. CONFIRMAR: `SecurityContextHolder` (`ThreadLocal` por default); `SecurityContext`; `Authentication` (extends `Principal`) com `getPrincipal`/`getAuthorities`/`getCredentials`/`isAuthenticated`; `GrantedAuthority`; `@AuthenticationPrincipal`.

- [ ] **Step 2: Escrever** — `fase: iniciado`, tags `[java, seguranca, iniciado, spring-security]`. Conteúdo:
  - TL;DR: o usuário autenticado vive no `SecurityContextHolder` (um `ThreadLocal`) durante o request; o `Authentication` carrega o `Principal` (quem é) e os `GrantedAuthority` (o que pode); `@AuthenticationPrincipal` injeta o principal no controller.
  - H3s: "`SecurityContextHolder`: o 'usuário atual' (um `ThreadLocal`)", "`Authentication`: principal + credentials + authorities", "`Principal` vs `Authorities`: quem é vs o que pode", "Acessando no controller: `@AuthenticationPrincipal`".
  - `## Na prática` — ler o `Authentication` via `SecurityContextHolder.getContext().getAuthentication()`; `@AuthenticationPrincipal UserDetails user` num `@GetMapping("/me")` (```java).
  - `## Armadilhas` — ≥2: (1) `auth.getPrincipal()` sem checar o tipo (`ClassCastException` — pode ser `UserDetails`, `Jwt` ou `OidcUser`); (2) `SecurityContextHolder` vazando auth entre requests num thread pool (limpar/`clearContext`); (3) assumir `getAuthentication()` sempre não-nulo (anonymous/sem auth retorna `AnonymousAuthenticationToken` ou null conforme config).
  - `## Veja também` — [[01 - O que é Spring Security — authn, authz e o filter chain]], [[03 - Autenticação — UserDetailsService, AuthenticationManager, Form e Basic]], [[17 - Uma request autenticada do token à autorização no método]], verbetes `SecurityContextHolder`/`GrantedAuthority`/`@AuthenticationPrincipal`.

- [ ] **Step 3: Verificar** — ≥7 seções; anti-fabricação VAZIO; `grep -i "SecurityContextHolder\|Authentication"` ≥3.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 12 nota 02 — SecurityContext, Authentication e Principal"`

### Task 3: Nota 03 — Autenticação — UserDetailsService, AuthenticationManager, Form e Basic ⟦opus⟧

**Files:**
- Create: `03-Dominios/Java/Segurança/03 - Autenticação — UserDetailsService, AuthenticationManager, Form e Basic.md`

- [ ] **Step 1: Pesquisar (version-specific)** — WebFetch `https://docs.spring.io/spring-security/reference/servlet/authentication/index.html` + `.../authentication/passwords/user-details-service.html` + `.../authentication/passwords/basic.html`. CONFIRMAR: `UserDetailsService.loadUserByUsername` (auto-detectado como bean); `UserDetails`/`User.builder()`; `AuthenticationManager` → `AuthenticationProvider` (`DaoAuthenticationProvider`) → `UserDetailsService` + `PasswordEncoder`; HTTP Basic vs Form login.

- [ ] **Step 2: Escrever** — `fase: iniciado`, tags `[java, seguranca, iniciado, autenticacao]`. Conteúdo:
  - TL;DR: autenticação prova quem é o usuário; o `UserDetailsService` carrega o usuário do banco, o `AuthenticationManager` (via `AuthenticationProvider`) confere a senha com o `PasswordEncoder`; HTTP Basic é simples (sempre HTTPS), Form login usa sessão.
  - Tabela "tipos de auth / quando usar" (Basic, Form, JWT, OAuth2 — apontando pras notas 08/09/12).
  - H3s: "`UserDetailsService`: carregando o usuário do banco", "`AuthenticationManager` → `AuthenticationProvider` → `UserDetailsService` + `PasswordEncoder`", "Form login (sessão) vs HTTP Basic (header, sempre HTTPS)", "Autenticação programática (`authManager.authenticate(...)`)".
  - `## Na prática` — um `UserDetailsServiceImpl` mapeando `User`/`Role` (neutros!) → `UserDetails` com `User.builder()...authorities("ROLE_" + role)`; config `http.httpBasic(...)` e `http.formLogin(...)` (```java).
  - `## Armadilhas` — ≥2: (1) erro de auth vazando info ("user not found" vs "wrong password" — information disclosure; retorne genérico); (2) HTTP Basic sem HTTPS (credencial em cleartext a cada request); (3) não tratar `UsernameNotFoundException`.
  - `## Veja também` — [[02 - SecurityContext, Authentication e Principal — o usuário atual]], [[04 - Password encoding — BCrypt, Argon2 e o DelegatingPasswordEncoder]], [[08 - JWT — estrutura, assinatura e validação]], verbetes `UserDetailsService`/`AuthenticationManager`/`AuthenticationProvider`.

- [ ] **Step 3: Verificar** — ≥7 seções; ≥2 armadilhas; anti-fabricação VAZIO (atenção: o tronco tem `UserDetailsServiceImpl` com `User`, mas a config de exemplo do tronco está OK — só não copiar Patient/MedEspecialista).

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 12 nota 03 — autenticação (UserDetailsService, AuthenticationManager, Form e Basic)"`

### Task 4: Nota 04 — Password encoding — BCrypt, Argon2 e o DelegatingPasswordEncoder

**Files:**
- Create: `03-Dominios/Java/Segurança/04 - Password encoding — BCrypt, Argon2 e o DelegatingPasswordEncoder.md`

- [ ] **Step 1: Pesquisar (version-specific)** — WebFetch `https://docs.spring.io/spring-security/reference/features/authentication/password-storage.html`. CONFIRMAR: `PasswordEncoder` (`encode`/`matches`); BCrypt (default, work factor, slow-by-design) vs Argon2 vs Pbkdf2/Scrypt; **`DelegatingPasswordEncoder`** (`PasswordEncoderFactories.createDelegatingPasswordEncoder()`, prefixo `{bcrypt}$...`); `NoOpPasswordEncoder` deprecated. **WebFetch obrigatório.**

- [ ] **Step 2: Escrever** — `fase: iniciado`, tags `[java, seguranca, iniciado, password]`. Conteúdo:
  - TL;DR: nunca armazene senha em plain text; `PasswordEncoder` faz o hash (BCrypt é o default razoável, slow-by-design); `DelegatingPasswordEncoder` põe um prefixo `{id}` no hash pra permitir migração entre algoritmos sem quebrar logins.
  - H3s: "`PasswordEncoder`: `encode` e `matches` (nunca decode — hash é one-way)", "BCrypt (default), Argon2, Pbkdf2: o que muda e o work factor", "`DelegatingPasswordEncoder`: o prefixo `{bcrypt}$...` e a migração gradual", "Por que slow-by-design protege contra brute force".
  - `## Na prática` — `@Bean PasswordEncoder` retornando `BCryptPasswordEncoder` ou `PasswordEncoderFactories.createDelegatingPasswordEncoder()`; `encoder.encode("...")`/`encoder.matches(...)` (```java).
  - `## Armadilhas` — ≥2: (1) plain text ou hash rápido (MD5/SHA — não slow); (2) `NoOpPasswordEncoder` em produção (deprecated, sem hash); (3) work factor baixo demais ou alto demais (latência de login).
  - `## Veja também` — [[03 - Autenticação — UserDetailsService, AuthenticationManager, Form e Basic]], [[16 - OWASP Top 10 no contexto Java]], verbetes `PasswordEncoder`/`BCryptPasswordEncoder`/`DelegatingPasswordEncoder`.

- [ ] **Step 3: Verificar** — ≥7 seções; anti-fabricação VAZIO; `grep -i "BCrypt\|DelegatingPasswordEncoder"` ≥2.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 12 nota 04 — password encoding (BCrypt, Argon2, DelegatingPasswordEncoder)"`

### Task 5: Nota 05 — Autorização baseada em URL — authorizeHttpRequests, roles vs authorities

**Files:**
- Create: `03-Dominios/Java/Segurança/05 - Autorização baseada em URL — authorizeHttpRequests, roles vs authorities.md`

- [ ] **Step 1: Pesquisar (version-specific)** — WebFetch `https://docs.spring.io/spring-security/reference/servlet/authorization/authorize-http-requests.html`. CONFIRMAR: **`authorizeHttpRequests`** (substituiu `authorizeRequests`); **`requestMatchers`** (substituiu `antMatchers`); `permitAll`/`authenticated`/`hasRole`/`hasAnyRole`/`hasAuthority`/`denyAll`; **`hasRole("ADMIN")` busca a authority `ROLE_ADMIN`** (prefixo convenção); matcher por `HttpMethod`. **WebFetch obrigatório.**

- [ ] **Step 2: Escrever** — `fase: iniciado`, tags `[java, seguranca, iniciado, autorizacao, rbac]`. Conteúdo:
  - TL;DR: autorização decide o que o usuário autenticado pode acessar; `authorizeHttpRequests` (que substituiu `authorizeRequests`) casa requests por `requestMatchers` e exige `hasRole`/`hasAuthority`; `hasRole("ADMIN")` busca a authority `ROLE_ADMIN` — o prefixo `ROLE_` é convenção.
  - H3s: "`authorizeHttpRequests` + `requestMatchers` (o que substituiu `authorizeRequests`/`antMatchers`)", "`hasRole` vs `hasAuthority`: o prefixo `ROLE_` e quando usar cada", "RBAC básico: roles → acesso", "Ordem dos matchers e matcher por `HttpMethod`".
  - `## Na prática` — um `SecurityFilterChain` com `requestMatchers("/api/public/**").permitAll().requestMatchers("/api/admin/**").hasRole("ADMIN").requestMatchers("/actuator/**").hasRole("ADMIN").anyRequest().authenticated()` (```java). **Este exemplo quita a dívida do Actuator** (proteger `/actuator/**`).
  - `## Armadilhas` — ≥2: (1) `antMatchers`/`authorizeRequests` legados (removidos/substituídos na 6.x); (2) `hasRole("ROLE_ADMIN")` (prefixo duplicado — vira `ROLE_ROLE_ADMIN`); (3) ordem errada de matchers (o mais específico primeiro; `anyRequest()` por último); (4) `permitAll()` num endpoint sensível por engano.
  - `## Veja também` — [[01 - O que é Spring Security — authn, authz e o filter chain]], [[07 - Method security — @PreAuthorize, @PostAuthorize e SpEL]], [[14 - Autorização avançada — AuthorizationManager, RBAC vs ABAC]], **[[03-Dominios/Java/Spring Core e Boot/17 - Actuator e observabilidade|Actuator e observabilidade]]** (proteger os endpoints), verbetes `authorizeHttpRequests`/`hasRole vs hasAuthority`/`RBAC (role-based)`.

- [ ] **Step 3: Verificar** — ≥7 seções; anti-fabricação VAZIO; `grep -i "authorizeHttpRequests\|requestMatchers"` ≥2; `grep -c "Spring Core e Boot/17"` ≥1.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 12 nota 05 — autorização baseada em URL (authorizeHttpRequests, roles vs authorities)"`

---

## Fase ADEPTO (notas 06-11)

### Task 6: Nota 06 — A arquitetura do filter chain em profundidade ⟦opus⟧

**Files:**
- Create: `03-Dominios/Java/Segurança/06 - A arquitetura do filter chain em profundidade.md`

- [ ] **Step 1: Pesquisar** — WebFetch `https://docs.spring.io/spring-security/reference/servlet/architecture.html`. CONFIRMAR: `DelegatingFilterProxy` → `FilterChainProxy` → lista de `SecurityFilterChain`; a ordem dos filtros (`SecurityContextHolderFilter`, `HeaderWriterFilter`, `CorsFilter`, `CsrfFilter`, auth filters, `ExceptionTranslationFilter`, `AuthorizationFilter`); múltiplos `SecurityFilterChain` por `securityMatcher`; `ExceptionTranslationFilter` (401 vs 403); `addFilterBefore`/`addFilterAfter`.

- [ ] **Step 2: Escrever** — `fase: adepto`, tags `[java, seguranca, adepto, filter-chain]`. **Liga a borda do Galho 9.** ≥3 H3s: "`FilterChainProxy`: o `Filter` único que delega pra cadeia", "A ordem dos filtros: do `SecurityContextHolderFilter` ao `AuthorizationFilter`", "Múltiplos `SecurityFilterChain` (`securityMatcher`): cadeias diferentes por path", "`ExceptionTranslationFilter`: 401 (não-autenticado) vs 403 (não-autorizado)", "Adicionando filtro custom: `addFilterBefore`/`addFilterAfter`". **O contraste explícito: `Filter` genérico (Galho 9 nota 11) vs `SecurityFilterChain`** — o `SecurityFilterChain` é, no fundo, **um `Filter` da plataforma Servlet (Galho 7)** que delega pra uma cadeia ordenada de filtros de segurança. `## Na prática` — o diagrama da ordem dos filtros (```text, higienizado — sem `medespecialista`); um filtro custom via `addFilterBefore(myFilter, UsernamePasswordAuthenticationFilter.class)` (```java). `## Armadilhas` ≥3: (1) filtro custom na posição errada (antes do `SecurityContextHolderFilter` não tem contexto); (2) assumir um único `SecurityFilterChain` (a primeira cadeia que casa o request ganha — ordem importa); (3) confundir `Filter` (Servlet, Galho 9) com `SecurityFilterChain` (a cadeia de segurança). `## Veja também` — [[01 - O que é Spring Security — authn, authz e o filter chain]], [[10 - CSRF — por que ligado por default e quando desligar]], **[[03-Dominios/Java/Web e APIs REST/11 - Interceptors vs Filters|Interceptors vs Filters]]** (o `Filter` genérico), **[[03-Dominios/Java/Web e APIs REST/06 - O pipeline do DispatcherServlet|O pipeline do DispatcherServlet]]** (o chain senta na frente), **[[03-Dominios/Java/Jakarta EE/03 - Servlet API — o alicerce HTTP|Servlet API]]** (o `Filter` da plataforma por baixo), verbetes `FilterChainProxy`/`SecurityFilterChain`/`ExceptionTranslationFilter`.

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; anti-fabricação VAZIO; `grep -c "Web e APIs REST/11"` ≥1; `grep -c "Jakarta EE/03"` ≥1.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 12 nota 06 — a arquitetura do filter chain em profundidade"`

### Task 7: Nota 07 — Method security — @PreAuthorize, @PostAuthorize e SpEL ⟦opus⟧

**Files:**
- Create: `03-Dominios/Java/Segurança/07 - Method security — @PreAuthorize, @PostAuthorize e SpEL.md`

- [ ] **Step 1: Pesquisar (version-specific)** — WebFetch `https://docs.spring.io/spring-security/reference/servlet/authorization/method-security.html`. CONFIRMAR: **`@EnableMethodSecurity`** (substituiu `@EnableGlobalMethodSecurity`; `prePostEnabled` default true); `@PreAuthorize`/`@PostAuthorize`/`@PreFilter`/`@PostFilter`; SpEL (`hasRole`, `hasAuthority`, `#param`, `authentication`, `principal`, `@bean.method()`). **WebFetch obrigatório.**

- [ ] **Step 2: Escrever** — `fase: adepto`, tags `[java, seguranca, adepto, method-security, autorizacao]`. **A 1ª face da fronteira-assinatura (mecanismo = AOP do Galho 8).** ≥3 H3s: "`@EnableMethodSecurity` (o que substituiu `@EnableGlobalMethodSecurity`)", "`@PreAuthorize`/`@PostAuthorize`: antes vs depois da execução", "`@PreFilter`/`@PostFilter`: filtrando coleções", "SpEL: `hasRole`, `#param`, `authentication.principal`, `@bean`", "URL-based (grossa) vs method-level (granular)". **O mecanismo é o proxy AOP** — `@PreAuthorize` só funciona em método `public` chamado **por fora** (igual `@Transactional`): linka **Galho 8 nota 09** (AOP) e **nota 10** (o limite do proxy). `## Na prática` — `@PreAuthorize("hasRole('ADMIN')")` e `@PreAuthorize("hasRole('ADMIN') or #order.ownerId == authentication.principal.id")` num `UserService` (neutro!); `@PostFilter("filterObject.ownerId == authentication.principal.id")` (```java). `## Armadilhas` ≥3: (1) esquecer `@EnableMethodSecurity` (anotação ignorada **silenciosamente** — sem erro); (2) `@PreAuthorize` em método `private`/`final` ou self-invocation (não passa pelo proxy — Galho 8); (3) `@PostAuthorize` carregando dado caro antes de negar (avalia depois de executar). `## Veja também` — [[05 - Autorização baseada em URL — authorizeHttpRequests, roles vs authorities]], [[14 - Autorização avançada — AuthorizationManager, RBAC vs ABAC]], **[[03-Dominios/Java/Spring Core e Boot/09 - AOP e proxies no Spring|AOP e proxies no Spring]]** (o mecanismo), **[[03-Dominios/Java/Spring Core e Boot/10 - Self-invocation e os limites do proxy|Self-invocation e os limites do proxy]]** (por que não funciona em `private`), verbetes `@EnableMethodSecurity`/`@PreAuthorize / @PostAuthorize`.

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; anti-fabricação VAZIO; `grep -c "Spring Core e Boot/09"` ≥1; `grep -c "Spring Core e Boot/10"` ≥1.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 12 nota 07 — method security (@PreAuthorize, @PostAuthorize, SpEL)"`

### Task 8: Nota 08 — JWT — estrutura, assinatura e validação ⟦opus⟧

**Files:**
- Create: `03-Dominios/Java/Segurança/08 - JWT — estrutura, assinatura e validação.md`

- [ ] **Step 1: Pesquisar** — WebFetch `https://datatracker.ietf.org/doc/html/rfc7519` (claims) + `https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html`. CONFIRMAR: header/payload/signature (base64url, **não criptografia**); claims (`iss`/`sub`/`aud`/`exp`/`nbf`/`iat`/`jti`); RS256/ES256 (assimétrico) vs HS256 (simétrico); **`alg: none` e a whitelist**; validar SEMPRE `iss`/`aud`/`exp`.

- [ ] **Step 2: Escrever** — `fase: adepto`, tags `[java, seguranca, adepto, jwt]`. ≥3 H3s: "As 3 partes: header.payload.signature (base64url — não é cripto)", "Claims: `iss`/`sub`/`aud`/`exp`/`nbf`/`jti` + claims customizadas", "Assinatura: RS256/ES256 (assimétrico) vs HS256 (simétrico)", "`alg: none` e a whitelist de algoritmos", "Stateless: prós (portável, self-contained) e contras (revogação)". `## Na prática` — um JWT decodificado (```json com header/payload); nota de que o payload é **legível** (base64), não criptografado. A revogação difícil → forward-link **nota 13** (refresh tokens). `## Armadilhas` ≥3: (1) `alg: none` aceito (forja qualquer token — sempre whitelist); (2) não validar `aud`/`iss` (aceita token de qualquer emissor); (3) claim sensível no payload (é base64, qualquer um lê); (4) JWT em `localStorage` (XSS rouba). `## Veja também` — [[09 - OAuth2 Resource Server — validando JWT na API]], [[13 - Refresh tokens e revogação de token]], [[17 - Uma request autenticada do token à autorização no método]], verbetes `JWT (JSON Web Token)`/`alg: none (ataque JWT)`.

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; anti-fabricação VAZIO (atenção: o tronco tem o "incidente memorável" do `alg: none` num pentest — **NÃO copiar**, ensinar o conceito de forma neutra); `grep -i "alg: none\|RS256"` ≥1.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 12 nota 08 — JWT (estrutura, assinatura e validação)"`

### Task 9: Nota 09 — OAuth2 Resource Server — validando JWT na API ⟦opus⟧

**Files:**
- Create: `03-Dominios/Java/Segurança/09 - OAuth2 Resource Server — validando JWT na API.md`

- [ ] **Step 1: Pesquisar (version-specific)** — WebFetch `https://docs.spring.io/spring-security/reference/servlet/oauth2/resource-server/jwt.html`. CONFIRMAR: `spring-boot-starter-oauth2-resource-server`; `oauth2ResourceServer().jwt()`; `issuer-uri`/`jwk-set-uri` (**JWKS**); `JwtAuthenticationConverter` + `JwtGrantedAuthoritiesConverter` (claim → authority, prefixo `SCOPE_`/`ROLE_`); `@AuthenticationPrincipal Jwt`; `SessionCreationPolicy.STATELESS`. **WebFetch obrigatório.**

- [ ] **Step 2: Escrever** — `fase: adepto`, tags `[java, seguranca, adepto, oauth2, jwt]`. ≥3 H3s: "O cenário: sua API valida JWTs emitidos por um IdP (Keycloak/Auth0/Cognito)", "Config: `issuer-uri`/`jwk-set-uri` (JWKS — rotação de chave sem downtime)", "`JwtAuthenticationConverter`: claim `scope`/`roles` → `GrantedAuthority`", "Stateless: `SessionCreationPolicy.STATELESS` + CSRF off (forward-link notas 10/15)", "Acessando: `@AuthenticationPrincipal Jwt`". `## Na prática` — `application.yml` com `spring.security.oauth2.resourceserver.jwt.issuer-uri` (neutro — `https://auth.example.com`, **não medespecialista**); `oauth2ResourceServer(o -> o.jwt(j -> j.jwtAuthenticationConverter(conv)))`; um `@GetMapping("/me")` com `@AuthenticationPrincipal Jwt jwt` (```java + ```yaml). `## Armadilhas` ≥3: (1) CSRF on numa API stateless (quebra clients que não mandam o token); (2) não configurar `issuer-uri`/`aud` (não valida emissor/audiência); (3) converter ausente (authorities vazias — todo `hasRole` falha). `## Veja também` — [[08 - JWT — estrutura, assinatura e validação]], [[10 - CSRF — por que ligado por default e quando desligar]], [[12 - OAuth2 e OIDC Client e os grant types]], verbetes `OAuth2 Resource Server`/`JWKS (JSON Web Key Set)`/`JwtAuthenticationConverter`.

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; anti-fabricação VAZIO (o tronco usa `auth.medespecialista.com` — usar `auth.example.com`); `grep -i "issuer-uri\|JWKS\|jwk-set-uri"` ≥1.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 12 nota 09 — OAuth2 Resource Server (validando JWT na API)"`

### Task 10: Nota 10 — CSRF — por que ligado por default e quando desligar

**Files:**
- Create: `03-Dominios/Java/Segurança/10 - CSRF — por que ligado por default e quando desligar.md`

- [ ] **Step 1: Pesquisar (version-specific)** — WebFetch `https://docs.spring.io/spring-security/reference/servlet/exploits/csrf.html`. CONFIRMAR: **CSRF habilitado por default**; o token por request mutating (POST/PUT/DELETE/PATCH); `CookieCsrfTokenRepository.withHttpOnlyFalse()`; `CsrfTokenRequestAttributeHandler`; por que API stateless com JWT em `Authorization` header não precisa. **WebFetch obrigatório.**

- [ ] **Step 2: Escrever** — `fase: adepto`, tags `[java, seguranca, adepto, csrf]`. ≥3 H3s: "O ataque: request autenticada forjada via cookie (o browser envia o cookie sozinho)", "CSRF on por default: token sincronizado em cada request mutating", "Web app com sessão cookie: **mantenha** CSRF", "API stateless com JWT no header: **desligue** (o browser não envia `Authorization` automaticamente)", "SPA + cookie session: `CookieCsrfTokenRepository` + `X-XSRF-TOKEN`". `## Na prática` — o `<input type="hidden" name="${_csrf.parameterName}">` num form (```html); `http.csrf(c -> c.disable())` pra API stateless e `http.csrf(c -> c.csrfTokenRepository(CookieCsrfTokenRepository.withHttpOnlyFalse()))` pra SPA (```java). `## Armadilhas` ≥3: (1) desabilitar CSRF num web app com sessão (vulnerável); (2) manter CSRF numa API stateless com JWT (quebra clients que não mandam o token); (3) SPA sem ler o cookie `XSRF-TOKEN` e reenviar no header. `## Veja também` — [[09 - OAuth2 Resource Server — validando JWT na API]], [[11 - CORS — a borda, o preflight e a config de segurança]], [[06 - A arquitetura do filter chain em profundidade]] (o `CsrfFilter` na cadeia), verbetes `CSRF`/`CsrfFilter`.

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; anti-fabricação VAZIO; `grep -i "csrf"` ≥3.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 12 nota 10 — CSRF (por que ligado por default e quando desligar)"`

### Task 11: Nota 11 — CORS — a borda, o preflight e a config de segurança

**Files:**
- Create: `03-Dominios/Java/Segurança/11 - CORS — a borda, o preflight e a config de segurança.md`

- [ ] **Step 1: Pesquisar** — WebFetch `https://docs.spring.io/spring-security/reference/servlet/integrations/cors.html`. CONFIRMAR: CORS é mecanismo do **browser** (não server-side); `CorsConfigurationSource`/`UrlBasedCorsConfigurationSource`; `allowedOrigins`/`allowedMethods`/`allowedHeaders`/`allowCredentials`/`maxAge`; **preflight OPTIONS**; `allowedOrigins("*")` + `allowCredentials(true)` rejeitado pelo browser; `.cors()` no filter chain (antes do auth).

- [ ] **Step 2: Escrever** — `fase: adepto`, tags `[java, seguranca, adepto, cors]`. **Liga a borda do Galho 9 (CORS tratado como config MVC lá).** ≥3 H3s: "CORS é do **browser**, não do servidor (`curl` bypassa — **não é segurança server-side**)", "`CorsConfigurationSource`: origens/métodos/headers/credentials", "O preflight OPTIONS: quando o browser pergunta antes", "`allowedOrigins('*')` + `allowCredentials(true)`: por que o browser rejeita", "CORS no filter chain (Spring Security) vs config MVC (Galho 9)". `## Na prática` — um `CorsConfigurationSource` com `allowedOrigins(List.of("https://app.example.com"))` (neutro!), `allowCredentials(true)`, `maxAge`; `http.cors(Customizer.withDefaults())` (```java). `## Armadilhas` ≥3: (1) `allowedOrigins("*")` + `allowCredentials(true)` (browser rejeita); (2) assumir que CORS protege o servidor (só o browser — `curl`/Postman ignoram; a auth ainda é obrigatória); (3) preflight OPTIONS não permitido (request "complexo" falha). `## Veja também` — [[10 - CSRF — por que ligado por default e quando desligar]], [[06 - A arquitetura do filter chain em profundidade]] (o `CorsFilter` na cadeia), **[[03-Dominios/Java/Web e APIs REST/11 - Interceptors vs Filters|Interceptors vs Filters]]** (onde o Galho 9 tratou filtros/CORS na camada MVC), verbetes `CORS`.

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; anti-fabricação VAZIO (o tronco usa `medespecialista.com` — usar `example.com`); `grep -c "Web e APIs REST/11"` ≥1.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 12 nota 11 — CORS (a borda, o preflight e a config de segurança)"`

---

## Fase MAGUS (notas 12-18)

### Task 12: Nota 12 — OAuth2 e OIDC Client e os grant types ⟦opus⟧

**Files:**
- Create: `03-Dominios/Java/Segurança/12 - OAuth2 e OIDC Client e os grant types.md`

- [ ] **Step 1: Pesquisar (version-specific)** — WebFetch `https://docs.spring.io/spring-security/reference/servlet/oauth2/client/index.html` + `https://datatracker.ietf.org/doc/html/rfc9700` (BCP). CONFIRMAR: `spring-boot-starter-oauth2-client`; `oauth2Login`; `OidcUser`/`OAuth2User`; OAuth2 (delegação) vs OIDC (identidade, `id_token`); **authorization code + PKCE**; **client credentials** (server-to-server); implicit/password **deprecated**.

- [ ] **Step 2: Escrever** — `fase: magus`, tags `[java, seguranca, magus, oauth2, oidc]`. ≥3 H3s: "OAuth2 (delegação de acesso) vs OIDC (camada de identidade, `id_token`)", "Login social: `oauth2Login` + `@AuthenticationPrincipal OidcUser`", "Authorization Code + PKCE: o fluxo seguro pra web e mobile", "Client Credentials: server-to-server, sem usuário", "Implicit/Password: deprecated — não use em código novo", "Resource Server (nota 09) vs Client (aqui)". `## Na prática` — `application.yml` com `spring.security.oauth2.client.registration.google` (neutro); `http.oauth2Login(...)`; um `@GetMapping("/me")` com `OidcUser` (```java + ```yaml); o diagrama do authorization code flow (```text). **OAuth2 num gateway/SSO de microservices → Galho 16 (texto "(planejado)").** `## Armadilhas` ≥3: (1) implicit flow em código novo (deprecated — use code + PKCE); (2) client secret no front-end/SPA (use PKCE, sem secret); (3) confundir OAuth2 (autorização/delegação) com OIDC (autenticação/identidade). `## Veja também` — [[09 - OAuth2 Resource Server — validando JWT na API]], [[08 - JWT — estrutura, assinatura e validação]], [[13 - Refresh tokens e revogação de token]], verbetes `OAuth2 Client`/`OIDC (OpenID Connect)`/`PKCE / authorization code`/`client credentials (grant)`.

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; anti-fabricação VAZIO; `grep -i "PKCE\|client credentials\|OIDC"` ≥1.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 12 nota 12 — OAuth2 e OIDC Client e os grant types"`

### Task 13: Nota 13 — Refresh tokens e revogação de token

**Files:**
- Create: `03-Dominios/Java/Segurança/13 - Refresh tokens e revogação de token.md`

- [ ] **Step 1: Pesquisar** — WebFetch `https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html` + `https://datatracker.ietf.org/doc/html/rfc9700`. CONFIRMAR: o trade-off stateless vs revogação; access token curto + refresh token server-side; rotação; armazenamento seguro (HttpOnly Secure SameSite vs localStorage).

- [ ] **Step 2: Escrever** — `fase: magus`, tags `[java, seguranca, magus, jwt, oauth2]`. **Deepening do JWT (nota 08).** ≥3 H3s: "O trade-off: JWT é stateless, mas isso torna a revogação difícil", "O par: access token curto (~15min) + refresh token server-side (UUID, não JWT)", "Rotação: novo refresh a cada uso, o antigo é revogado", "Revogação imediata: tabela `refresh_tokens` (logout/troca de senha)", "Blacklist de access token quebra o stateless (o trade-off honesto)", "Armazenamento: HttpOnly Secure SameSite cookie vs `localStorage` (XSS)". `## Na prática` — o fluxo login → access+refresh, `POST /auth/refresh` (```text); um esquema de tabela `refresh_tokens(token_hash, user_id, expires_at, revoked)` (```sql). `## Armadilhas` ≥3: (1) refresh token como JWT (revogação volta a ser difícil — use UUID opaco server-side); (2) refresh token em `localStorage` (XSS); (3) não rotacionar o refresh (token roubado vale até expirar). `## Veja também` — [[08 - JWT — estrutura, assinatura e validação]], [[12 - OAuth2 e OIDC Client e os grant types]], [[16 - OWASP Top 10 no contexto Java]], verbetes `refresh token`/`JWT (JSON Web Token)`.

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; anti-fabricação VAZIO (o tronco tem a tabela `refresh_tokens` do MedEspecialista — usar genérico, sem `device_info`/contexto fabricado); `grep -i "refresh token\|revoga"` ≥2.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 12 nota 13 — refresh tokens e revogação de token"`

### Task 14: Nota 14 — Autorização avançada — AuthorizationManager, RBAC vs ABAC

**Files:**
- Create: `03-Dominios/Java/Segurança/14 - Autorização avançada — AuthorizationManager, RBAC vs ABAC.md`

- [ ] **Step 1: Pesquisar** — WebFetch `https://docs.spring.io/spring-security/reference/servlet/authorization/architecture.html`. CONFIRMAR: `AuthorizationManager<RequestAuthorizationContext>` + `.access(...)`; `RoleHierarchy`; RBAC vs ABAC vs ReBAC (OpenFGA/SpiceDB).

- [ ] **Step 2: Escrever** — `fase: magus`, tags `[java, seguranca, magus, autorizacao, rbac]`. ≥3 H3s: "`AuthorizationManager` + `.access()`: lógica de autorização custom", "RBAC (roles → permissões): simples, cobre a maioria", "ABAC (atributos via SpEL): decisão por atributo do usuário/recurso/contexto", "ReBAC (Zanzibar — OpenFGA/SpiceDB): 'Alice compartilhou X com Bob' (menção)", "`RoleHierarchy`: ADMIN herda USER". `## Na prática` — um `AuthorizationManager` checando se o `principal` é dono do recurso (`#resource.ownerId == authentication.principal.id` — neutro); `requestMatchers("/api/orders/{id}").access(orderAuthManager)`; `RoleHierarchyImpl` (```java). `## Armadilhas` ≥3: (1) lógica de negócio demais no SpEL (ilegível e não-testável — extraia pro `AuthorizationManager`); (2) RBAC onde o domínio pedia ABAC (explosão de roles tipo `ADMIN_REGION_X`); (3) role hierarchy implícita esquecida (ADMIN não herda USER sem `RoleHierarchy`). `## Veja também` — [[05 - Autorização baseada em URL — authorizeHttpRequests, roles vs authorities]], [[07 - Method security — @PreAuthorize, @PostAuthorize e SpEL]], [[16 - OWASP Top 10 no contexto Java]], verbetes `AuthorizationManager`/`RBAC (role-based)`/`ABAC (attribute-based)`/`RoleHierarchy`.

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; anti-fabricação VAZIO; `grep -i "AuthorizationManager\|RBAC\|ABAC"` ≥2.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 12 nota 14 — autorização avançada (AuthorizationManager, RBAC vs ABAC)"`

### Task 15: Nota 15 — Session management e security headers

**Files:**
- Create: `03-Dominios/Java/Segurança/15 - Session management e security headers.md`

- [ ] **Step 1: Pesquisar (version-specific)** — WebFetch `https://docs.spring.io/spring-security/reference/servlet/authentication/session-management.html` + `https://docs.spring.io/spring-security/reference/servlet/exploits/headers.html`. CONFIRMAR: `SessionCreationPolicy` (STATELESS/IF_REQUIRED/ALWAYS/NEVER); session fixation (`migrateSession` — default); `maximumSessions`; security headers que o Spring adiciona por default (HSTS, CSP, `X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy`).

- [ ] **Step 2: Escrever** — `fase: magus`, tags `[java, seguranca, magus, session]`. ≥3 H3s: "STATELESS (JWT) vs stateful (`HttpSession`/`JSESSIONID`)", "Session fixation: `migrateSession` (default — nova sessão após login)", "Concurrent sessions: `maximumSessions`", "Sessão distribuída: Spring Session/Redis (multi-instância — menção)", "Security headers: HSTS, CSP (anti-XSS), `X-Frame-Options` (anti-clickjacking), `nosniff`, `Referrer-Policy`". `## Na prática` — `http.sessionManagement(sm -> sm.sessionCreationPolicy(STATELESS))` e a versão stateful com `sessionFixation().migrateSession().maximumSessions(1)`; `http.headers(h -> h.contentSecurityPolicy(...).frameOptions(fo -> fo.deny()))` (```java). `## Armadilhas` ≥3: (1) stateful numa API que devia ser stateless (sessão desnecessária, não escala); (2) CSP com `unsafe-inline` (derrota o propósito anti-XSS); (3) esquecer HSTS/headers atrás de proxy (configurar `ForwardedHeaderFilter` pra `X-Forwarded-*`). `## Veja também` — [[09 - OAuth2 Resource Server — validando JWT na API]], [[16 - OWASP Top 10 no contexto Java]], [[06 - A arquitetura do filter chain em profundidade]] (o `HeaderWriterFilter`/`SessionManagementFilter`), verbetes `SessionCreationPolicy (STATELESS)`/`session fixation`.

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; anti-fabricação VAZIO; `grep -i "STATELESS\|fixation\|HSTS\|CSP"` ≥2.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 12 nota 15 — session management e security headers"`

### Task 16: Nota 16 — OWASP Top 10 no contexto Java

**Files:**
- Create: `03-Dominios/Java/Segurança/16 - OWASP Top 10 no contexto Java.md`

- [ ] **Step 1: Pesquisar** — WebFetch `https://owasp.org/www-project-top-ten/` + `https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html`. CONFIRMAR: as categorias atuais do Top 10 (Broken Access Control, Cryptographic Failures, Injection, Insecure Design, Security Misconfiguration, Vulnerable Components, Identification/Auth Failures, Software/Data Integrity, Logging/Monitoring Failures, SSRF). **NÃO inventar estatística.**

- [ ] **Step 2: Escrever** — `fase: magus`, tags `[java, seguranca, magus, owasp]`. **A nota-síntese — mapeia o Top 10 pras defesas do galho.** ≥3 H3s: "Broken Access Control → method security (07) / authz (05,14)", "Cryptographic Failures → BCrypt (04) / HTTPS / JWT assinado (08)", "Injection → JPA params (Galho 10) / `PreparedStatement` / Bean Validation (Galho 9)", "Security Misconfiguration → CSRF/CORS/headers (10,11,15)", "Identification & Auth Failures → password encoding (04), session (15), refresh tokens (13)", "Defense-in-depth: nenhuma camada é suficiente sozinha". `## Na prática` — uma **tabela** "Categoria OWASP → defesa Spring Security → nota do galho" (sem código pesado; é síntese). `## Armadilhas` (de raciocínio) ≥3: (1) "auth perfeita basta" (sem logging/monitoramento, brute force/anomalia passa); (2) "CORS protege o servidor" (só o browser — a auth é obrigatória); (3) "o framework cobre tudo automaticamente" (config é 80% dos bugs — teste cada endpoint). **Linka SQL injection → Galho 10 (texto, JPA params).** `## Veja também` — [[04 - Password encoding — BCrypt, Argon2 e o DelegatingPasswordEncoder]], [[10 - CSRF — por que ligado por default e quando desligar]], [[14 - Autorização avançada — AuthorizationManager, RBAC vs ABAC]], [[18 - Capstone — projetando a segurança de uma API Spring production-grade]], verbetes `OWASP Top 10`.

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; **grep anti-estatística VAZIO**: `grep -riE "% d[ao]s|market share|maioria d[ao]s (ataques|brechas|breaches)|[0-9]+% (das|dos)" "<path>"`; anti-fabricação VAZIO.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 12 nota 16 — OWASP Top 10 no contexto Java"`

### Task 17: Nota 17 — Uma request autenticada do token à autorização no método ⟦opus⟧

**Files:**
- Create: `03-Dominios/Java/Segurança/17 - Uma request autenticada do token à autorização no método.md`

- [ ] **Step 1: Pesquisar** — WebFetch `https://docs.spring.io/spring-security/reference/servlet/architecture.html` + `https://docs.spring.io/spring-security/reference/servlet/oauth2/resource-server/jwt.html`. CONFIRMAR: `BearerTokenAuthenticationFilter`; a sequência decode → validação → `Authentication` → `SecurityContextHolder` → `AuthorizationFilter` → controller → `@PreAuthorize` (proxy AOP); 401 vs 403 via `ExceptionTranslationFilter`.

- [ ] **Step 2: Escrever** — `fase: magus`, tags `[java, seguranca, magus, filter-chain, jwt]`. **Capstone-trace.** Conteúdo:
  - TL;DR: o trace completo de uma request autenticada — `Authorization: Bearer <jwt>` entra pelo filter chain, é validado, vira `Authentication` no `SecurityContext`, passa pela autorização de URL, chega ao controller e bate no `@PreAuthorize` (proxy AOP) antes do service.
  - `## O fluxo passo a passo` (H3s): "1. `BearerTokenAuthenticationFilter`: extrai o token do header", "2. Decode + validação (assinatura/JWKS, `iss`/`aud`/`exp`, whitelist de `alg`)", "3. `JwtAuthenticationConverter` monta o `Authentication` → `SecurityContextHolder`", "4. `AuthorizationFilter`: regras de URL (`authorizeHttpRequests`)", "5. `DispatcherServlet` → controller (Galho 9)", "6. `@PreAuthorize`: o proxy AOP intercepta antes do método (Galho 8)", "O caminho do erro: 401 (não-autenticado) vs 403 (não-autorizado) via `ExceptionTranslationFilter`".
  - `## Na prática` — o diagrama completo do fluxo (```text, higienizado); o código mínimo que materializa cada etapa (config Resource Server + `@PreAuthorize` no service) (```java).
  - `## Armadilhas` (de raciocínio) ≥3: (1) "o token chega direto no controller" (há o filter chain inteiro antes); (2) "autorização é só no controller" (é URL **e** método — duas camadas); (3) "validar JWT é só checar a assinatura" (`iss`/`aud`/`exp`/`alg` também). `## Veja também` — [[06 - A arquitetura do filter chain em profundidade]], [[09 - OAuth2 Resource Server — validando JWT na API]], [[18 - Capstone — projetando a segurança de uma API Spring production-grade]], **[[03-Dominios/Java/Spring Core e Boot/09 - AOP e proxies no Spring|AOP e proxies no Spring]]** (o proxy do `@PreAuthorize`), verbetes `BearerTokenAuthenticationFilter`/`ExceptionTranslationFilter`.

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; anti-fabricação VAZIO; `grep -c "Spring Core e Boot/09"` ≥1.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 12 nota 17 — uma request autenticada do token à autorização no método"`

### Task 18: Nota 18 — Capstone — projetando a segurança de uma API Spring production-grade ⟦opus⟧

**Files:**
- Create: `03-Dominios/Java/Segurança/18 - Capstone — projetando a segurança de uma API Spring production-grade.md`

- [ ] **Step 1: Pesquisar** — WebFetch `https://docs.spring.io/spring-security/reference/` (índice) + `https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html`. CONFIRMAR/reforçar o checklist; o teste de segurança (`@WithMockUser`/`with(jwt())`) só como menção de fronteira (Galho 13).

- [ ] **Step 2: Escrever** — `fase: magus`, tags `[java, seguranca, magus, spring-security]`. **Capstone-checklist + síntese.** Conteúdo:
  - TL;DR: o checklist production-grade de segurança de uma API Spring — `SecurityFilterChain` + lambda DSL, stateless + Resource Server, CSRF off/on conforme o caso, CORS explícito, method security, password encoding forte, security headers, refresh tokens server-side.
  - `## O checklist` (H3s ou lista): config (`SecurityFilterChain` bean + lambda DSL); autenticação (stateless + OAuth2 Resource Server, JWKS, valida `iss`/`aud`/`exp`, whitelist de `alg`); autorização (URL + method security com SpEL); password (`DelegatingPasswordEncoder`/BCrypt); CSRF (off stateless / on sessão); CORS (origens explícitas, nunca `*`+credentials); headers (HSTS/CSP/frame-options); refresh tokens server-side.
  - `## A dupla fronteira numa tabela` — tabela "Galho 12 → mecanismo (Galho 8) / borda (Galho 9)": `@PreAuthorize` ↔ proxy AOP (G8); `SecurityFilterChain` ↔ bean + `Filter` (G8/G7); filter chain ↔ na frente do DispatcherServlet (G9); CORS ↔ borda de segurança vs config MVC (G9).
  - `## Testando a segurança` — **menção** de `@WithMockUser`/`with(jwt())`/MockMvc como fronteira → **Galho 13 (texto "(planejado)", sem wikilink)**; "se testa com mock user / JWT de teste, a stack de teste é do galho de Testes".
  - `## Cheatsheet nota → problema` — tabela "problema → nota do galho".
  - `## Armadilhas` (de raciocínio) ≥3: (1) desabilitar proteção "temporariamente" (vira permanente); (2) confiar em dado do client pra decisão de autorização (valide no server); (3) CORS como segurança (é do browser).
  - `## Em entrevista` (munição: como você desenharia a segurança de uma API do zero) + `## Veja também` — [[01 - O que é Spring Security — authn, authz e o filter chain]], [[17 - Uma request autenticada do token à autorização no método]], [[16 - OWASP Top 10 no contexto Java]], MOC galho, MOC central + `## Referências`.

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; anti-fabricação VAZIO; **grep fronteira VAZIO**: `grep -rE "\[\[[^]]*(Galho (13|16|17)|Testcontainers|Keycloak|WebFlux Security)" "<path>"`.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 12 nota 18 — capstone (projetando a segurança de uma API Spring production-grade)"`

---

## Task 19: MOC do galho

**Files:**
- Create: `03-Dominios/Java/Segurança/index.md`

- [ ] **Step 1: Escrever** — modelar pelo `03-Dominios/Java/Programação Reativa/index.md`. Frontmatter: `type: moc`, `status: growing`, `publish: true`, `title: "Segurança"`, tags `[java, seguranca, moc]`, aliases `["Segurança", "Spring Security", "Segurança em Java", "Galho 12 - Segurança"]`, `created`/`updated: 2026-06-10`. Conteúdo:
  - TL;DR — Galho 12; a camada que protege a borda web do Galho 9 usando o mecanismo do Galho 8: o filter chain, autenticação e password encoding, autorização URL-based e method-level, JWT, OAuth2/OIDC, CSRF/CORS, session management e headers, e o OWASP Top 10 mapeado pras defesas do Spring Security; 18 notas em 3 fases.
  - `## Sobre este galho` — escopo + audiência + **galho híbrido** (poda integral do tronco `Spring Security.md` + pesquisa version-specific) + **dupla fronteira** (usa o mecanismo AOP do Galho 8; protege a borda web do Galho 9; toca a Servlet API do Galho 7 de leve) + foco **servlet/MVC** (segurança reativa/WebFlux = fronteira pra frente; Galhos 13/16/17 planejados, texto).
  - `## Iniciado` (01-05) / `## Adepto` (06-11) / `## Magus` (12-18) — wikilinks + 1 linha cada.
  - `## Rotas alternativas` — 5: **Completa** (01→18); **Entrevista internacional** (01→03→06→07→08→09→17); **API stateless com JWT** (01→08→09→10→13→17); **Autorização do grosso ao fino** (05→07→14→16); **Protegendo a borda web** (01→06→10→11→15 + Galho 9 DispatcherServlet/Interceptors).
  - `## Todas as notas` — Dataview (`FROM "03-Dominios/Java/Segurança"`, `WHERE type = "concept"`).
  - `## Veja também` — MOC central, **[[03-Dominios/Java/Spring Core e Boot/index|Spring Core e Boot]]** (o mecanismo AOP), **[[03-Dominios/Java/Web e APIs REST/index|Web e APIs REST]]** (a borda protegida), **[[03-Dominios/Java/Jakarta EE/index|Jakarta EE]]** (a Servlet API por baixo), [[Redes e Protocolos]] (HTTPS/TLS), Dicionário; Galhos 13/16/17 como texto "(planejado)" SEM wikilink.

- [ ] **Step 2: Verificar**
```bash
grep -cE "^## (Iniciado|Adepto|Magus|Rotas alternativas)" "03-Dominios/Java/Segurança/index.md"
grep -c "\[\[" "03-Dominios/Java/Segurança/index.md"
grep -E "\[\[[^]]*(Galho (13|16|17))" "03-Dominios/Java/Segurança/index.md"
```
Expected: 4 headings; ≥18 wikilinks; **último grep VAZIO**.

- [ ] **Step 3: Commit** — `git add "<path>"` && `git commit -m "feat(java): galho 12 MOC — Segurança"`

---

## Task 20: Expandir o Dicionário de Java (NÃO recriar)

**Files:**
- Modify: `03-Dominios/Java/Dicionário de Java.md`

- [ ] **Step 1: Extrair as âncoras realmente usadas pelas notas**
```bash
grep -rhoE "Dicionário de Java#[^]|]+" "03-Dominios/Java/Segurança/" | sort -u
```
A fonte da verdade é o que as notas usaram. Lista esperada (~35): `@AuthenticationPrincipal`, `@EnableMethodSecurity`, `@PreAuthorize / @PostAuthorize`, `ABAC (attribute-based)`, `alg: none (ataque JWT)`, `AuthenticationManager`, `AuthenticationProvider`, `authorizeHttpRequests`, `AuthorizationManager`, `BCryptPasswordEncoder`, `BearerTokenAuthenticationFilter`, `client credentials (grant)`, `CORS`, `CSRF`, `CsrfFilter`, `DelegatingPasswordEncoder`, `ExceptionTranslationFilter`, `FilterChainProxy`, `GrantedAuthority`, `hasRole vs hasAuthority`, `JWKS (JSON Web Key Set)`, `JWT (JSON Web Token)`, `JwtAuthenticationConverter`, `OAuth2 Client`, `OAuth2 Resource Server`, `OIDC (OpenID Connect)`, `OWASP Top 10`, `PasswordEncoder`, `PKCE / authorization code`, `RBAC (role-based)`, `refresh token`, `RoleHierarchy`, `SecurityContextHolder`, `SecurityFilterChain`, `session fixation`, `SessionCreationPolicy (STATELESS)`, `Spring Security`, `UserDetailsService`.

- [ ] **Step 2: Ler o Dicionário e conferir duplicatas** — formato `### Termo` + 1-3 linhas + `Veja também:`. **NÃO recriar/reordenar.** **Conferir verbetes já existentes pra NÃO duplicar** e **linkar entre si**: `CORS` (Galho 9 — pode existir como config MVC; complementar/linkar, **não duplicar**); `Filter`/`Servlet`/`DispatcherServlet` (Galhos 7/9 — linkar de `FilterChainProxy`/`SecurityFilterChain`, não duplicar); `scope`/`access token` (se já houver). Conferir com:
```bash
grep -nE "^### (CORS|Filter|Servlet|DispatcherServlet|access token|scope|JWT|OAuth2)" "03-Dominios/Java/Dicionário de Java.md"
```

- [ ] **Step 3: Inserir em ordem alfabética** (case-insensitive, sem acento; verbetes iniciados em `@`/minúscula entram conforme o padrão do arquivo — conferir vizinhos). Cada verbete: heading EXATO da âncora + definição fiel às notas + `Veja também:` pra nota canônica (Spring Security/SecurityFilterChain/FilterChainProxy→01,06; SecurityContextHolder/GrantedAuthority/@AuthenticationPrincipal→02; UserDetailsService/AuthenticationManager/AuthenticationProvider→03; PasswordEncoder/BCryptPasswordEncoder/DelegatingPasswordEncoder→04; authorizeHttpRequests/hasRole.../RBAC→05; ExceptionTranslationFilter→06; @EnableMethodSecurity/@PreAuthorize→07; JWT/alg: none→08; OAuth2 Resource Server/JWKS/JwtAuthenticationConverter/BearerTokenAuthenticationFilter→09; CSRF/CsrfFilter→10; CORS→11; OAuth2 Client/OIDC/PKCE.../client credentials→12; refresh token→13; AuthorizationManager/ABAC/RoleHierarchy→14; SessionCreationPolicy/session fixation→15; OWASP Top 10→16). Manter `updated: 2026-06-10`.

- [ ] **Step 4: Verificar**
```bash
grep -E "^### (SecurityFilterChain|JWT \(JSON|OAuth2 Resource Server|CSRF|OWASP Top 10|@PreAuthorize)" "03-Dominios/Java/Dicionário de Java.md"
grep -cE "^### " "03-Dominios/Java/Dicionário de Java.md"
```
Expected: novos presentes; contagem subiu ~35 vs baseline (327 → ~360, descontando os que já existiam e foram linkados em vez de duplicados).

- [ ] **Step 5: Commit** — `git add "<path>"` && `git commit -m "feat(java): expande Dicionário de Java com verbetes do galho 12 (Segurança)"`

---

## Task 21: Ativar o Galho 12 no MOC central

**Files:**
- Modify: `03-Dominios/Java/index.md`

- [ ] **Step 1: Trocar a linha do item 12** (localizar por conteúdo: `12. Segurança *(planejado)* — Spring Security, JWT, OAuth2/OIDC, CSRF/CORS`) por:
```markdown
12. [[03-Dominios/Java/Segurança/index|Segurança]] — Spring Security e o filter chain, autenticação e password encoding, autorização URL-based e method-level, JWT, OAuth2/OIDC, CSRF/CORS, session management, security headers e OWASP no contexto Java
```
Atualizar `updated: 2026-06-10`. Não mexer no resto (13/16/17 permanecem "(planejado)").

- [ ] **Step 2: Verificar**
```bash
grep -E "Segurança/index" "03-Dominios/Java/index.md"
grep -c "planejado" "03-Dominios/Java/index.md"
```
Expected: wikilink ativo; "planejado" caiu exatamente 1 vs baseline.

- [ ] **Step 3: Commit** — `git add "<path>"` && `git commit -m "feat(java): ativa Galho 12 (Segurança) no MOC central"`

---

## Task 22: Poda INTEGRAL do tronco (`Backend/Spring Security.md`) — vira hub

**Files:**
- Modify: `03-Dominios/Java/Backend/Spring Security.md`

- [ ] **Step 1: Ler o tronco e confirmar o frontmatter** (política §9 — ler antes de podar)
```bash
sed -n '1,16p' "03-Dominios/Java/Backend/Spring Security.md"
```
Confirmar o bloco de frontmatter (linhas 1-14, `publish: false`, tags incluindo `seguranca`) a **preservar**; o corpo (linha 16 em diante, o H1 `# Spring Security` e tudo até o fim) será **substituído**.

- [ ] **Step 2: Poda INTEGRAL** — reescrever o arquivo inteiro (preservando o frontmatter com `updated: 2026-06-10`, `publish: false`) com H1 + 1-2 frases de intro neutras + um único callout `[!nota] Migrado para galho próprio`:
```markdown
# Spring Security

Segurança na stack Spring — autenticação, autorização, JWT, OAuth2/OIDC, CSRF, CORS e o filter chain. Conteúdo migrado para galho próprio na trilha Java Senior.

> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Java/Segurança/index|Segurança]]. Veja [[03-Dominios/Java/Segurança/01 - O que é Spring Security — authn, authz e o filter chain|O que é Spring Security]], [[03-Dominios/Java/Segurança/06 - A arquitetura do filter chain em profundidade|A arquitetura do filter chain]], [[03-Dominios/Java/Segurança/08 - JWT — estrutura, assinatura e validação|JWT]], [[03-Dominios/Java/Segurança/09 - OAuth2 Resource Server — validando JWT na API|OAuth2 Resource Server]], [[03-Dominios/Java/Segurança/12 - OAuth2 e OIDC Client e os grant types|OAuth2 e OIDC Client]] e o [[03-Dominios/Java/Segurança/18 - Capstone — projetando a segurança de uma API Spring production-grade|Capstone de segurança]].
```
**Toda a fabricação some** (`Patient`/`Doctor`/`Appointment`/`MedEspecialista`, `## Na prática (da minha experiência)`, `## How to explain in English`, os "incidentes memoráveis"/pentest, `### Frases úteis em entrevista`).

- [ ] **Step 3: Verificar (poda integral — só o hub sobra)**
```bash
wc -l "03-Dominios/Java/Backend/Spring Security.md"
grep -c "Migrado para galho próprio" "03-Dominios/Java/Backend/Spring Security.md"
grep -riE "Patient|Doctor|Appointment|MedEspecialista|minha experiência|pentest|incidente memorável|How to explain|alg: none" "03-Dominios/Java/Backend/Spring Security.md"
grep -E "^publish: false" "03-Dominios/Java/Backend/Spring Security.md"
```
Expected: ~10-12 linhas (frontmatter + hub); ≥1 callout; **terceiro grep VAZIO** (toda a fabricação sumiu); `publish: false` presente.

- [ ] **Step 4: Confirmar troncos vizinhos intocados**
```bash
git status --short "03-Dominios/Java/Backend/Spring Boot.md" "03-Dominios/Java/Backend/Spring Data JPA.md" "03-Dominios/Java/Backend/Kafka/" "03-Dominios/Java/Backend/Testes em Java.md"
```
Expected: **VAZIO** (nenhum outro tronco modificado).

- [ ] **Step 5: Commit** — `git add "03-Dominios/Java/Backend/Spring Security.md"` && `git commit -m "refactor(java): poda integral do tronco Spring Security — vira hub do galho 12"`

---

## Task 23: Quitar a dívida reversa (6 ponteiros inline + 3 parágrafos → wikilinks)

**Files:**
- Modify: `03-Dominios/Java/Spring Core e Boot/17 - Actuator e observabilidade.md`
- Modify: `03-Dominios/Java/Web e APIs REST/12 - Documentando a API com OpenAPI e Swagger.md`
- Modify: `03-Dominios/Java/Web e APIs REST/11 - Interceptors vs Filters.md`
- Modify: `03-Dominios/Java/Spring Core e Boot/index.md`
- Modify: `03-Dominios/Java/Web e APIs REST/index.md`
- Modify: `03-Dominios/Java/Persistência de dados/index.md`

- [ ] **Step 1: Relocalizar (por conteúdo — linhas podem ter mudado)**
```bash
grep -rn "Galho 12\|galho 12" "03-Dominios/Java/Spring Core e Boot/17 - Actuator e observabilidade.md" "03-Dominios/Java/Web e APIs REST/12 - Documentando a API com OpenAPI e Swagger.md" "03-Dominios/Java/Web e APIs REST/11 - Interceptors vs Filters.md" "03-Dominios/Java/Spring Core e Boot/index.md" "03-Dominios/Java/Web e APIs REST/index.md" "03-Dominios/Java/Persistência de dados/index.md"
```

- [ ] **Step 2: Aplicar os wikilinks** — em cada ponteiro, trocar "Galho 12 (planejado)" pelo wikilink, **mantendo natural a frase** e atualizando `updated: 2026-06-10` no frontmatter de cada arquivo tocado:
  - **Spring Core/17 - Actuator (:52):** "Segurança de endpoints (autenticação e autorização do Actuator) é tema do Galho 12 (planejado)." → "...é tema do galho [[03-Dominios/Java/Segurança/05 - Autorização baseada em URL — authorizeHttpRequests, roles vs authorities|Segurança]]."
  - **Spring Core/17 - Actuator (:111):** "Proteção com Spring Security é abordada no Galho 12 (planejado)." → "Proteção com Spring Security é abordada no galho [[03-Dominios/Java/Segurança/05 - Autorização baseada em URL — authorizeHttpRequests, roles vs authorities|Segurança]]."
  - **Spring Core/17 - Actuator (:288):** "...exponha apenas o necessário e proteja com Spring Security (Galho 12, planejado)." → "...exponha apenas o necessário e proteja com Spring Security ([[03-Dominios/Java/Segurança/index|Galho 12 — Segurança]])."
  - **Web/12 - OpenAPI (:167):** "Segurança de API é assunto do Galho 12 (planejado)." → "Segurança de API é assunto do galho [[03-Dominios/Java/Segurança/01 - O que é Spring Security — authn, authz e o filter chain|Segurança]]."
  - **Web/11 - Interceptors vs Filters (:357):** "Autenticação, CSRF e autorização pertencem ao Galho 12 (Segurança com Spring Security — planejado), que explora a camada de filtros do Spring Security em profundidade." → "Autenticação, CSRF e autorização pertencem ao galho [[03-Dominios/Java/Segurança/06 - A arquitetura do filter chain em profundidade|Segurança]], que explora a camada de filtros do Spring Security em profundidade."
  - **Spring Core e Boot/index (:32, parágrafo de fronteira):** "...Spring Security (Galho 12), Testes no ecossistema Spring (Galho 13), e Microservices/Cloud com Spring Cloud (Galhos 16 e 17) são planejados..." → "...Spring Security é o galho [[03-Dominios/Java/Segurança/index|Segurança]]; Testes no ecossistema Spring (Galho 13) e Microservices/Cloud com Spring Cloud (Galhos 16 e 17) são planejados..." **NÃO tocar o horizonte-list :97.**
  - **Web e APIs REST/index (:32, parágrafo de fronteira):** "...Spring Security (Galho 12), Testes no ecossistema Spring (Galho 13), Microservices (Galho 16) e Spring Cloud (Galho 17) são planejados..." → "...Spring Security é o galho [[03-Dominios/Java/Segurança/index|Segurança]]; Testes no ecossistema Spring (Galho 13), Microservices (Galho 16) e Spring Cloud (Galho 17) são planejados..." **NÃO tocar o horizonte-list :95.**
  - **Persistência de dados/index (:32, parágrafo de fronteira):** "...segurança de dados (Galho 12), testes de repositório (Galho 13) e dados distribuídos/saga (Galho 16) são planejados, sem cobertura aqui." → "...segurança (incluindo a ponte com `AuditorAware`/`SecurityContext`) é o galho [[03-Dominios/Java/Segurança/index|Segurança]]; testes de repositório (Galho 13) e dados distribuídos/saga (Galho 16) são planejados, sem cobertura aqui." **NÃO tocar o horizonte-list :92.** (Manter honesto: row-level/field-level fica de leve no Galho 12.)

- [ ] **Step 3: Verificar**
```bash
grep -rn "Galho 12\|galho 12" "03-Dominios/Java/Spring Core e Boot/17 - Actuator e observabilidade.md" "03-Dominios/Java/Web e APIs REST/12 - Documentando a API com OpenAPI e Swagger.md" "03-Dominios/Java/Web e APIs REST/11 - Interceptors vs Filters.md" "03-Dominios/Java/Spring Core e Boot/index.md" "03-Dominios/Java/Web e APIs REST/index.md" "03-Dominios/Java/Persistência de dados/index.md" | grep -iE "planejado" | grep -vE ":(95|97|92):"
grep -rn "Segurança/index\|Segurança/01\|Segurança/05\|Segurança/06" "03-Dominios/Java/Spring Core e Boot/17 - Actuator e observabilidade.md" "03-Dominios/Java/Web e APIs REST/12 - Documentando a API com OpenAPI e Swagger.md" "03-Dominios/Java/Web e APIs REST/11 - Interceptors vs Filters.md" "03-Dominios/Java/Spring Core e Boot/index.md" "03-Dominios/Java/Web e APIs REST/index.md" "03-Dominios/Java/Persistência de dados/index.md"
```
Expected: primeiro grep **VAZIO** ou só horizonte-lists :95/:97/:92 (que mantêm 13/16/17 "(planejado)"); segundo grep ≥9 (todos os wikilinks aplicados). Conferir manualmente que cada "Galho 12" remanescente vem acompanhado do wikilink "Segurança", e que **Reativa index :35** (segurança reativa) e os horizonte-lists permanecem intactos.

- [ ] **Step 4: Confirmar que Reativa index :35 NÃO foi tocado**
```bash
grep -n "segurança reativa (Galho 12)" "03-Dominios/Java/Programação Reativa/index.md"
```
Expected: ≥1 (permanece como texto "(planejado)" — segurança reativa é fronteira pra frente, fora do escopo deste galho).

- [ ] **Step 5: Commit** — `git add` nominal dos 6 arquivos && `git commit -m "refactor(java): quita dívida reversa do galho 12 — ponteiros de segurança viram wikilinks"`

---

## Task 24: Verificação final do galho

**Files:** (somente leitura/verificação)

- [ ] **Step 1: 18 notas + MOC**
```bash
ls "03-Dominios/Java/Segurança/" | sort
```
Expected: 01..18 + index.md (19 arquivos).

- [ ] **Step 2: Fases (5/6/7)**
```bash
for f in "03-Dominios/Java/Segurança/"[0-9]*.md; do grep -H "^fase:" "$f"; done
```
Expected: 01-05 `iniciado`, 06-11 `adepto`, 12-18 `magus`.

- [ ] **Step 3: Seções obrigatórias (3 por nota)**
```bash
for f in "03-Dominios/Java/Segurança/"[0-9]*.md; do echo "$f: $(grep -cE '^## (Em entrevista|Armadilhas|Veja também)' "$f")"; done
```
Expected: 3 em todas.

- [ ] **Step 4: Anti-fabricação + estatística inventada + fronteiras (greps decisivos)**
```bash
grep -riE "minha experiência|no meu projeto|josenaldo|Patient|Doctor|Appointment|MedEspecialista|pentest|incidente memorável|medespecialista\.com|% d[ao]s (brechas|ataques|breaches|dev|empresas)|maioria d[ao]s (ataques|brechas)" "03-Dominios/Java/Segurança/"
grep -rE "\[\[[^]]*(Galho (13|16|17)|Testcontainers|Keycloak|Spring Cloud|circuit breaker|WebFlux Security|ReactiveSecurityContext)" "03-Dominios/Java/Segurança/"
grep -rn '\[\[#' "03-Dominios/Java/Segurança/"
```
Expected: **todos VAZIOS**.

- [ ] **Step 5: Dupla fronteira-assinatura (links de volta aos Galhos 8 e 9 presentes; Galho 7 na nota 06)**
```bash
grep -rl "Spring Core e Boot/09" "03-Dominios/Java/Segurança/" | sort
grep -rl "Spring Core e Boot/10" "03-Dominios/Java/Segurança/" | sort
grep -rl "Web e APIs REST/(06|11)" "03-Dominios/Java/Segurança/" | sort
grep -rl "Jakarta EE/03" "03-Dominios/Java/Segurança/" | sort
```
Expected: notas 07/17 linkam pro Galho 8 nota 09 (AOP); nota 07 linka pro Galho 8 nota 10 (self-invocation); notas 01/06/11 linkam pro Galho 9 (DispatcherServlet/Interceptors); nota 06 linka pro Galho 7 nota 03 (Servlet API).

- [ ] **Step 6: Frase pronta (1 por nota)**
```bash
for f in "03-Dominios/Java/Segurança/"[0-9]*.md; do echo "$f: $(grep -c '### Frase pronta (inglês)' "$f")"; done
```
Expected: 1 em todas.

- [ ] **Step 7: Tronco — poda integral confirmada; vizinhos intocados**
```bash
wc -l "03-Dominios/Java/Backend/Spring Security.md"
grep -c "Migrado para galho próprio" "03-Dominios/Java/Backend/Spring Security.md"
grep -riE "Patient|MedEspecialista|How to explain|## Na prática" "03-Dominios/Java/Backend/Spring Security.md"
git status --short "03-Dominios/Java/Backend/Spring Boot.md" "03-Dominios/Java/Backend/Spring Data JPA.md" "03-Dominios/Java/Backend/Kafka/" "03-Dominios/Java/Backend/Testes em Java.md"
```
Expected: `Spring Security.md` ~10-12 linhas só com o hub (≥1 callout; terceiro grep **VAZIO**); troncos vizinhos **sem modificação** (último comando VAZIO).

- [ ] **Step 8: Skill `verificar-wikilinks`** — rodar na pasta `03-Dominios/Java/Segurança/` + conferir os arquivos tocados fora (MOC central, Dicionário, o tronco Spring Security, os 6 arquivos da dívida reversa). Âncoras `Dicionário de Java#...` resolvem 1:1 (cross-check com o grep da Task 20 Step 1). As quebras legadas da árvore Java NÃO são deste galho — só corrigir o que este galho introduziu. Corrigir e commitar à parte se houver.

- [ ] **Step 9: Resumo de fechamento (sem commit)** — reportar: 18 notas (5/6/7), ~35 verbetes (327→~360), MOC galho + MOC central, **poda integral** (tronco `Spring Security.md` vira hub; toda a fabricação MedEspecialista/pentest/`How to explain` sumiu), **dívida reversa quitada** (6 ponteiros inline + 3 parágrafos; horizonte-lists e galhos 13/16/17 preservados como "(planejado)"; Reativa index :35 intacto — segurança reativa é fronteira pra frente), troncos vizinhos intocados (mostrar o `git status`), wikilinks limpos, **OWASP sem estatística inventada**. Commits locais na `main`; **push manual do usuário; sem deploy**. Atualizar memória [[project_trilha_java]] com Galho 12 completo + fatos cravados via WebFetch (`WebSecurityConfigurerAdapter` removido na 6.0, `authorizeHttpRequests`/`requestMatchers`, `@EnableMethodSecurity`, CSRF default on, baseline Security 6.x/Boot 3.x).

---

## Self-Review (preenchido na escrita do plano)

**Spec coverage:** Tasks 1-18 ↔ spec §3.1 (18 notas, escopos idênticos, opus 01/03/06/07/08/09/12/17/18, distribuição 5/6/7); Task 19 ↔ §3.2 (MOC, 5 rotas iguais); Task 20 ↔ §3.3 (~35 verbetes, âncoras 1:1 por grep, dups conferidos/linkados com Galhos 7/9: CORS/Filter/Servlet/DispatcherServlet/scope); Task 21 ↔ §3.4 (item 12); Task 22 ↔ §3.5 (poda integral — tronco `Spring Security.md` vira hub; fabricação some; `publish: false` mantido; troncos vizinhos intocados); Task 23 ↔ §3.6 (6 ponteiros inline + 3 parágrafos, mapeamento idêntico; Actuator :52/:111/:288→nota 05, OpenAPI :167→nota 01, Interceptors :357→nota 06, parágrafos→MOC; horizonte-lists :95/:97/:92 e Reativa :35 preservados; galhos 13/16/17 como texto); Task 0 ↔ §6 (pré-flight, baseline 327, leitura do tronco); Task 24 ↔ §7. Dupla fronteira-assinatura (§4.3.1) garantida por links obrigatórios pros Galhos 8/9 nas Tasks 1/5/6/7/10/11/17 (+ Galho 7 na Task 6) e pelo grep da Task 24 Step 5; fronteira galhos 13/16/17 pelo grep da Task 24 Step 4.

**Placeholder scan:** sem TBD/TODO; cada nota tem fonte WebFetch nomeada com URL, frontmatter concreto, H3s, armadilhas mínimas com conteúdo real, tamanho-alvo herdado das convenções. Pontos version-sensitive marcados com "verificar/confirmar" são instruções de verificação WebFetch (a essência da parte pesquisa), não placeholders: `WebSecurityConfigurerAdapter` removido na 6.0, `authorizeHttpRequests`/`requestMatchers`, `@EnableMethodSecurity`, CSRF default on, `DelegatingPasswordEncoder`, JWKS/`issuer-uri`, PKCE. A confirmação dos ranges/linhas do tronco e da dívida reversa (Tasks 0/22/23) é resolução-na-execução por política §9 do roadmap (ler antes de podar/editar).

**Type/naming consistency:** numeração 01-18 idêntica entre tasks, MOC, Dicionário, dívida reversa, poda e cheatsheets das capstones; distribuição 5/6/7 consistente; opus 01/03/06/07/08/09/12/17/18 marcadas ⟦opus⟧ (9 notas, batendo com spec §3.1 e convenções); filenames com em dash (sem `:`/`/` — notas usam "—" e vírgula, sem dois-pontos); mapeamento de link-back Galho 8→notas 09/10/06, Galho 9→notas 06/11, Galho 7→nota 03 consistente entre spec §3.1/§4.3.1, convenções e Tasks; âncoras do Dicionário extraídas por grep antes de inserir (Task 20) e validadas na Task 24; verbetes adjacentes (`CORS` G9↔G12, `Filter`/`Servlet`/`DispatcherServlet` G7/G9↔`SecurityFilterChain`/`FilterChainProxy`) linkados, não duplicados.
