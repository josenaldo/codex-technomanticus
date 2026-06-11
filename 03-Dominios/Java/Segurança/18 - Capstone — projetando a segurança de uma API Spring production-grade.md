---
title: "Capstone — projetando a segurança de uma API Spring production-grade"
created: 2026-06-10
updated: 2026-06-10
type: concept
progress: backlog
status: seedling
publish: true
fase: magus
tags:
  - java
  - seguranca
  - magus
  - spring-security
aliases:
  - "Capstone de segurança"
  - "segurança production-grade"
---

# Capstone — projetando a segurança de uma API Spring production-grade

> [!abstract] TL;DR
> Uma API Spring **production-grade** se monta a partir de um checklist costurado pelas notas deste galho: um `SecurityFilterChain` declarado com **lambda DSL**, autenticação **stateless** via **OAuth2 Resource Server** com JWT validado por **JWKS** (verificando `iss`/`aud`/`exp` e fazendo whitelist de `alg`), autorização em duas camadas (URL + **method security** com SpEL), **password encoding** forte (`DelegatingPasswordEncoder`/BCrypt), **CSRF** desligado no fluxo stateless e ligado em sessão, **CORS** com origens explícitas (nunca `*` com credenciais), **security headers** (HSTS/CSP/frame-options) e **refresh tokens** guardados no servidor. Nenhum item é opcional: cada um fecha uma classe de ataque distinta.

## O que é

Esta é a nota de fechamento do galho de Segurança. O objetivo não é introduzir conceito novo, e sim **consolidar tudo num checklist acionável** — a sequência de decisões que se toma ao desenhar a segurança de uma API Spring do zero, com cada decisão amarrada à nota que a explica em profundidade.

A pergunta que organiza esta nota é a mesma que aparece em entrevista: *"você recebeu um serviço REST sem nenhuma proteção. Como você desenha a segurança dele?"* A resposta não é um truque; é uma ordem de montagem. Filtramos a request antes do controller, decidimos quem é o usuário (authn), decidimos o que ele pode fazer (authz), e endurecemos as bordas (headers, CORS, CSRF). Cada camada assume que a anterior pode falhar — por isso autorização nunca confia só na URL, e o servidor nunca confia em dado vindo do cliente.

## O checklist production-grade

Os itens abaixo são a espinha do galho. Trate como um checklist de revisão de PR de segurança: se um item está faltando ou desabilitado "temporariamente", a API não está pronta para produção.

### Config — o ponto de entrada

- Declare um bean `SecurityFilterChain` e configure tudo via **lambda DSL** (o estilo moderno, sem `WebSecurityConfigurerAdapter`). Um bean por cadeia; use `securityMatcher` quando precisar de cadeias distintas (ex.: API vs. actuator).
- Veja [[03-Dominios/Java/Segurança/01 - O que é Spring Security — authn, authz e o filter chain|O que é Spring Security]] e [[03-Dominios/Java/Segurança/06 - SecurityFilterChain e a lambda DSL — configuração moderna|SecurityFilterChain e a lambda DSL]].

### Autenticação — stateless por padrão

- Para uma API, prefira **stateless**: `sessionCreationPolicy(STATELESS)`, sem `JSESSIONID`. A identidade vem em cada request via token.
- Use **OAuth2 Resource Server** com JWT. O servidor de recursos **não emite** tokens; ele os **valida**.
- Valide o token contra o **JWKS** do emissor (chaves públicas rotacionáveis), e cheque as claims: `iss` (emissor esperado), `aud` (este serviço é o público-alvo), `exp` (não expirado). Faça **whitelist de `alg`** — nunca aceite `none` nem confie cegamente no header do token.
- Veja [[03-Dominios/Java/Segurança/08 - OAuth2 e OIDC — o resource server valida, não emite|OAuth2 e OIDC]] e [[03-Dominios/Java/Segurança/09 - Validando JWT — JWKS, claims e a whitelist de algoritmos|Validando JWT]].

### Autorização — duas camadas

- Camada de **URL**: `authorizeHttpRequests` com matchers explícitos. Negue por padrão (`anyRequest().authenticated()` no fim).
- Camada de **método**: ative method security e use `@PreAuthorize` com **SpEL** para regras finas (`hasRole`, `hasAuthority`, comparação com o principal). É a defesa que sobrevive a um matcher de URL mal configurado.
- Veja [[03-Dominios/Java/Segurança/05 - Autorização por URL — authorizeHttpRequests e matchers|Autorização por URL]], [[03-Dominios/Java/Segurança/07 - Method security — @PreAuthorize, @PostAuthorize e SpEL|Method security]] e [[03-Dominios/Java/Segurança/14 - SpEL em segurança — expressões de autorização|SpEL em segurança]].

### Password — encoding forte

- Use `DelegatingPasswordEncoder` (prefixo `{bcrypt}`, `{argon2}` etc.) para suportar migração de algoritmo sem quebrar hashes antigos. BCrypt é o default seguro.
- Nunca compare senha em texto puro; nunca use hash rápido (MD5/SHA-1) para senha. (OWASP: armazenar senhas com hashing forte + salt, comparação em tempo constante.)
- Veja [[03-Dominios/Java/Segurança/04 - PasswordEncoder — BCrypt, DelegatingPasswordEncoder e migração|PasswordEncoder]].

### CSRF — depende do estado

- **Stateless (API com token em header)**: CSRF pode/deve ficar **off** — não há cookie de sessão para o browser anexar automaticamente, então o vetor não existe.
- **Com sessão (cookie)**: CSRF **on**, com token sincronizado. Desligar CSRF "porque dá erro" em fluxo de sessão abre a porta.
- Veja [[03-Dominios/Java/Segurança/10 - CSRF — quando ligar, quando desligar e por quê|CSRF]].

### CORS — origens explícitas

- Liste **origens explícitas**. **Nunca** combine `allowedOrigins("*")` com `allowCredentials(true)` — é proibido pela spec e perigoso.
- CORS é configuração de borda, não substituto de autenticação.
- Veja [[03-Dominios/Java/Segurança/11 - CORS — origens explícitas e o erro do wildcard com credenciais|CORS]].

### Headers — endureça o browser

- Garanta **HSTS** (força HTTPS), **CSP** (restringe origem de scripts/recursos) e **frame-options** (anti-clickjacking). O Spring Security já liga vários headers por padrão; ajuste CSP ao seu front.
- Veja [[03-Dominios/Java/Segurança/15 - Security headers — HSTS, CSP e frame-options|Security headers]].

### Refresh tokens — server-side

- Access tokens curtos; **refresh tokens** guardados e revogáveis **no servidor** (não no localStorage do cliente como verdade única). Permite revogar sessão sem esperar o `exp`.
- Veja [[03-Dominios/Java/Segurança/13 - Refresh tokens — rotação, revogação e armazenamento server-side|Refresh tokens]].

## A dupla fronteira numa tabela

Segurança não vive isolada: cada mecanismo deste galho se apoia em algo que outro galho explica. A coluna **Galho 8** é o *mecanismo Spring* que faz a peça funcionar; a coluna **Galho 9** é a *borda da plataforma web* onde ela atua.

| Peça do Galho 12 (Segurança) | Mecanismo (Galho 8 — Spring core) | Borda (Galho 9 — Web/Servlet) |
| --- | --- | --- |
| `@PreAuthorize` | Proxy AOP em torno do bean (interceptor de método) | Decisão acontece dentro do controller, depois do dispatch |
| `SecurityFilterChain` (bean) | Bean gerenciado pelo container + `Filter` | Registrado como filtro na frente do `DispatcherServlet` |
| Filter chain de segurança | `DelegatingFilterProxy` ligando ao contexto Spring | Roda **antes** do `DispatcherServlet`, na cadeia de filtros do servlet |
| CORS | Bean `CorsConfigurationSource` | Borda de segurança (preflight) **vs.** config CORS do MVC — escolha uma fonte de verdade |

A leitura da tabela: quando o `@PreAuthorize` "não dispara", o problema costuma ser de **proxy AOP** (Galho 8) — auto-invocação dentro da mesma classe pula o proxy. Quando o filtro de segurança não roda, o problema é de **ordem na cadeia de filtros** (Galho 9). Saber em qual galho mora o defeito é metade do diagnóstico.

## Testando a segurança

A segurança também se **testa**, e o teste é uma fronteira para o próximo galho. O padrão: você dispara requests contra a aplicação com uma identidade simulada — um **mock user** (`@WithMockUser`) para autorização baseada em roles, ou um **JWT de teste** (`with(jwt())`) para o fluxo Resource Server — e verifica os status (`200`/`401`/`403`) e o comportamento via `MockMvc`.

A montagem completa dessa stack de teste (slices, `MockMvc`, fixtures de identidade, asserts) é assunto do **galho de Testes (Galho 13, planejado)**. Aqui fica só a fronteira: se você desenhou a segurança como acima, você a valida com mock user / JWT de teste — não testando no navegador na unha.

## Cheatsheet nota → problema

Tabela de bolso para entrevista e para revisão. Bateu o problema, pule direto para a nota.

| Problema / pergunta | Nota do galho |
| --- | --- |
| Como funciona o filter chain de ponta a ponta? | [[03-Dominios/Java/Segurança/01 - O que é Spring Security — authn, authz e o filter chain\|nota 01]] |
| Como guardo senha sem fazer besteira? | [[03-Dominios/Java/Segurança/04 - PasswordEncoder — BCrypt, DelegatingPasswordEncoder e migração\|nota 04]] |
| Como protejo URLs por padrão? | [[03-Dominios/Java/Segurança/05 - Autorização por URL — authorizeHttpRequests e matchers\|nota 05]] |
| Como configuro tudo com a lambda DSL moderna? | [[03-Dominios/Java/Segurança/06 - SecurityFilterChain e a lambda DSL — configuração moderna\|nota 06]] |
| Por que `@PreAuthorize` não funciona? | [[03-Dominios/Java/Segurança/07 - Method security — @PreAuthorize, @PostAuthorize e SpEL\|nota 07]] |
| Quem emite e quem valida o token? | [[03-Dominios/Java/Segurança/08 - OAuth2 e OIDC — o resource server valida, não emite\|nota 08]] |
| Como valido um JWT (JWKS, claims, `alg`)? | [[03-Dominios/Java/Segurança/09 - Validando JWT — JWKS, claims e a whitelist de algoritmos\|nota 09]] |
| Ligo ou desligo CSRF? | [[03-Dominios/Java/Segurança/10 - CSRF — quando ligar, quando desligar e por quê\|nota 10]] |
| Por que CORS com `*` e credenciais quebra? | [[03-Dominios/Java/Segurança/11 - CORS — origens explícitas e o erro do wildcard com credenciais\|nota 11]] |
| Como revogo uma sessão antes do `exp`? | [[03-Dominios/Java/Segurança/13 - Refresh tokens — rotação, revogação e armazenamento server-side\|nota 13]] |
| Como escrevo regra de autorização em SpEL? | [[03-Dominios/Java/Segurança/14 - SpEL em segurança — expressões de autorização\|nota 14]] |
| Quais headers de segurança ligar? | [[03-Dominios/Java/Segurança/15 - Security headers — HSTS, CSP e frame-options\|nota 15]] |
| Onde isso tudo encaixa no OWASP Top 10? | [[03-Dominios/Java/Segurança/16 - OWASP Top 10 no contexto Java\|nota 16]] |
| Como é uma request autenticada de ponta a ponta? | [[03-Dominios/Java/Segurança/17 - Uma request autenticada do token à autorização no método\|nota 17]] |

## Armadilhas

Estas são armadilhas de **raciocínio** — o tipo de decisão que parece inofensiva no momento e vira incidente depois.

### (1) Desabilitar uma proteção "temporariamente"

O clássico: `csrf().disable()` ou `cors` aberto "só para destravar o front agora, depois ajusto". O "depois" não chega; o flag desabilitado vai para produção e fica. Toda desabilitação de proteção é uma decisão de segurança, não de conveniência.

**Fix**: nada de proteção desligada chega à `main`. Se precisa relaxar algo em dev, faça por **profile** (`@Profile("dev")` / `application-dev.yml`) e deixe a `main`/produção com o default seguro. Code review de PR deve barrar `disable()` sem justificativa explícita.

### (2) Confiar em dado do cliente para decisão de autorização

Decidir "este usuário é admin" a partir de um campo do corpo do request, de um header customizado, ou de uma claim não verificada do JWT. Qualquer coisa que o cliente controla, o cliente forja.

**Fix**: a decisão de autorização sai **sempre** de algo validado no servidor — o `Authentication` populado pelo filter chain após validar o token contra o JWKS. Role e ownership se checam contra o principal, nunca contra um valor que o cliente mandou junto.

### (3) Tratar CORS como camada de segurança

"O CORS bloqueia outras origens, então minha API está protegida." CORS é uma política aplicada **pelo navegador** — um cliente não-browser (curl, script, app) ignora CORS por completo. Ele não autentica ninguém.

**Fix**: CORS é configuração de **interoperabilidade de browser**, não de segurança. A proteção real é a **autenticação obrigatória** + autorização em cada endpoint. Configure CORS com origens explícitas, mas saiba que ele nunca substitui o `authenticated()`.

## Em entrevista

### Frase pronta (inglês)

> If I were designing security for a Spring API from scratch, I'd start with a single `SecurityFilterChain` bean using the lambda DSL, run it stateless as an OAuth2 Resource Server, and validate every incoming JWT against the issuer's JWKS — checking `iss`, `aud`, and `exp`, and whitelisting the signing algorithm so I never accept `none`. Authorization would be layered: URL rules that deny by default, plus method security with `@PreAuthorize` so a misconfigured matcher can't leak an endpoint. Then I'd harden the edges — strong password encoding with a delegating encoder, CSRF off for the stateless token flow but on for any session-cookie flow, CORS limited to explicit origins, security headers like HSTS and CSP, and refresh tokens kept server-side so I can revoke a session before the access token expires.

### Vocabulário

| Termo (EN) | Como usar |
| --- | --- |
| security filter chain | "the filter chain runs before the dispatcher servlet" |
| stateless authentication | "I keep the API stateless and carry identity in the token" |
| resource server | "the resource server validates tokens, it doesn't issue them" |
| JWKS endpoint | "I fetch the signing keys from the issuer's JWKS endpoint" |
| algorithm whitelist | "I whitelist the signing algorithm to reject `none`" |
| method security | "I add `@PreAuthorize` as a second authorization layer" |
| deny by default | "URL rules deny by default, then I allow explicitly" |
| token revocation | "server-side refresh tokens let me revoke before expiry" |

## Veja também

- [[03-Dominios/Java/Segurança/01 - O que é Spring Security — authn, authz e o filter chain|O que é Spring Security]]
- [[03-Dominios/Java/Segurança/17 - Uma request autenticada do token à autorização no método|Uma request autenticada de ponta a ponta]]
- [[03-Dominios/Java/Segurança/16 - OWASP Top 10 no contexto Java|OWASP Top 10 no contexto Java]]
- [[03-Dominios/Java/Segurança/index|Segurança (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Dicionário de Java]]

## Referências

- Spring Security Reference — https://docs.spring.io/spring-security/reference/
- OAuth2 Resource Server / JWT — https://docs.spring.io/spring-security/reference/servlet/oauth2/resource-server/jwt.html
- Method Security — https://docs.spring.io/spring-security/reference/servlet/authorization/method-security.html
- Password Storage (PasswordEncoder) — https://docs.spring.io/spring-security/reference/servlet/authentication/passwords/password-encoder.html
- CSRF — https://docs.spring.io/spring-security/reference/servlet/exploits/csrf.html
- CORS — https://docs.spring.io/spring-security/reference/servlet/integrations/cors.html
- Security Headers — https://docs.spring.io/spring-security/reference/servlet/exploits/headers.html
- OWASP Authentication Cheat Sheet — https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html
