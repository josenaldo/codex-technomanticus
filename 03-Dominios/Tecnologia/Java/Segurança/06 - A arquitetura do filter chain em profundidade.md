---
title: "A arquitetura do filter chain em profundidade"
created: 2026-06-10
updated: 2026-06-10
type: concept
progress: backlog
status: seedling
publish: true
fase: adepto
tags:
  - java
  - seguranca
  - adepto
  - filter-chain
aliases:
  - "filter chain em profundidade"
  - "FilterChainProxy"
  - "SecurityFilterChain"
---

# A arquitetura do filter chain em profundidade

> [!abstract] TL;DR
> Toda a segurança do Spring acontece numa cadeia ordenada de filtros — o `SecurityFilterChain` — gerida por um único `FilterChainProxy` que, do ponto de vista da plataforma Servlet, é apenas mais um `Filter`. Autenticação, CSRF, headers e autorização são cada um um filtro com posição fixa nessa fila. Entender a ordem dos filtros e onde encaixar customizações é, na prática, entender o Spring Security. Esta nota destrincha o `FilterChainProxy`, a ordem canônica, a seleção de múltiplas cadeias por `securityMatcher`, a tradução 401 vs 403 no `ExceptionTranslationFilter` e como inserir filtros próprios.

## O que é

O **filter chain** do Spring Security é uma sequência ordenada de objetos `Filter` (a interface da plataforma Servlet) que processa cada request HTTP antes de ele chegar ao controller. Essa sequência é encapsulada num `SecurityFilterChain` — uma cadeia de segurança associada a um `RequestMatcher` que decide quais requests ela atende.

O ponto de entrada é o `DelegatingFilterProxy`, registrado no container Servlet, que delega para o `FilterChainProxy` (um bean Spring). O `FilterChainProxy` escolhe, entre uma ou mais `SecurityFilterChain`, a primeira cuja `RequestMatcher` casa com o request, e executa os filtros de segurança daquela cadeia em ordem.

Cada filtro tem uma responsabilidade única: carregar o `SecurityContext`, escrever headers de segurança, validar CSRF, autenticar, lidar com anônimos, traduzir exceções, autorizar. Nada de segurança no Spring acontece fora dessa fila.

## Por que importa

Quando você configura `http.csrf(...)`, `http.httpBasic(...)` ou `http.authorizeHttpRequests(...)`, você não está ligando flags soltas — está **adicionando e ordenando filtros** numa cadeia. O comportamento observável (um 401 num endpoint, um 403 noutro, um CSRF que dispara antes da autenticação) é consequência direta da ordem dos filtros.

Para um sênior, essa visão muda três coisas no dia a dia:

- **Debugar** falhas de segurança vira ler o log de filtros (`logging.level.org.springframework.security=TRACE`) e descobrir qual filtro abortou o request e por quê.
- **Customizar** (um filtro de tenant, de rate limit, de header proprietário) exige saber a posição exata onde inserir — antes ou depois de qual filtro de referência.
- **Modelar** múltiplas políticas (uma API stateless com Bearer token, um painel admin com form login) vira modelar múltiplas `SecurityFilterChain`, cada uma com seu `securityMatcher`.

Sem o modelo mental da cadeia, você trata o Spring Security como caixa-preta e cada bug vira tentativa-e-erro.

## Como funciona

### FilterChainProxy: o Filter único que delega pra cadeia

Do ponto de vista do container Servlet, todo o Spring Security é **um único `Filter`**. O `DelegatingFilterProxy` é registrado no container e, em vez de implementar lógica própria, busca um bean Spring (o `FilterChainProxy`) e delega o `doFilter` pra ele. Isso resolve o descompasso de ciclo de vida: o container instancia filtros cedo, antes do `ApplicationContext` estar pronto; o `DelegatingFilterProxy` adia a busca do bean pro momento do request.

O `FilterChainProxy` é o coração. Ele:

1. Aplica a proteção do `HttpFirewall` (rejeita requests malformados antes de qualquer filtro).
2. Itera a lista de `SecurityFilterChain` e seleciona **a primeira** cujo `RequestMatcher` casa.
3. Executa, em ordem, os filtros de segurança daquela cadeia.

A consequência importante da fronteira: o `SecurityFilterChain` é, no fundo, **um `Filter` da plataforma Servlet** ([[03-Dominios/Tecnologia/Java/Jakarta EE/03 - Servlet API — o alicerce HTTP|Servlet API — o alicerce HTTP]], Galho 7) que delega pra uma cadeia ordenada de filtros de segurança. Ele convive com — mas não se confunde com — o `Filter` genérico do Servlet e os `Interceptor`s do Spring MVC, que vivem em outra camada e foram tratados no Galho 9 (ver [[03-Dominios/Tecnologia/Java/Web e APIs REST/11 - Interceptors vs Filters|Interceptors vs Filters]]). O ponto a fixar: tudo que o `FilterChainProxy` orquestra acontece **antes** do request chegar ao [[03-Dominios/Tecnologia/Java/Web e APIs REST/06 - O pipeline do DispatcherServlet|pipeline do DispatcherServlet]] — a cadeia de segurança senta na frente dele.

### A ordem dos filtros: do SecurityContextHolderFilter ao AuthorizationFilter

A ordem é fixa e definida pelo Spring (Security 6.x / Boot 3.x). Não é alfabética nem arbitrária — cada filtro depende do estado preparado pelos anteriores. A ordem canônica relevante:

1. `DisableEncodeUrlFilter` — impede que o session id vaze na URL.
2. `WebAsyncManagerIntegrationFilter` — integra o `SecurityContext` com requests assíncronos.
3. `SecurityContextHolderFilter` — **carrega** o `SecurityContext` (ex.: da sessão) no início e o limpa no fim. Tudo que precisa saber "quem está autenticado" tem que vir depois dele.
4. `HeaderWriterFilter` — escreve headers de segurança (X-Content-Type-Options, etc.).
5. `CorsFilter` — trata CORS (quando configurado).
6. `CsrfFilter` — valida o token CSRF. Dispara cedo, **antes** dos filtros de autenticação.
7. `LogoutFilter` — processa logout.
8. Filtros de autenticação, na ordem em que são adicionados:
   - `UsernamePasswordAuthenticationFilter` (form login)
   - `BasicAuthenticationFilter` (HTTP Basic)
   - `BearerTokenAuthenticationFilter` (Bearer token / OAuth2 Resource Server)
9. `RequestCacheAwareFilter` — re-executa um request salvo após o login.
10. `SecurityContextHolderAwareRequestFilter` — embrulha o request com a API de segurança do Servlet.
11. `AnonymousAuthenticationFilter` — se ninguém autenticou até aqui, atribui uma identidade anônima (assim a autorização sempre tem um `Authentication` pra avaliar).
12. `ExceptionTranslationFilter` — captura exceções de segurança lançadas pelos filtros seguintes e as traduz em resposta HTTP.
13. `AuthorizationFilter` — **o último**. Aqui se decide se o `Authentication` corrente tem permissão pro endpoint. Como é o último, é também onde as exceções de autorização nascem — e por isso o `ExceptionTranslationFilter` vem logo antes, pra capturá-las.

O detalhe sênior: `ExceptionTranslationFilter` vem **antes** do `AuthorizationFilter` exatamente porque precisa estar na pilha de chamadas quando o `AuthorizationFilter` lançar `AccessDeniedException`. Filtro que vem antes captura exceção de filtro que vem depois (try/catch envolvendo o `filterChain.doFilter`).

### Múltiplos SecurityFilterChain (securityMatcher): cadeias diferentes por path

Você raramente quer a mesma política pra toda a aplicação. Uma API REST stateless com Bearer token tem necessidades diferentes de um painel admin com form login e sessão. A resposta são **múltiplas** `SecurityFilterChain`, cada uma com seu `securityMatcher`.

O `FilterChainProxy` avalia as cadeias **em ordem** e usa **a primeira** cujo matcher casa — as demais nem são consultadas. Por isso a ordem de declaração dos beans (via `@Order`) é parte da configuração, não detalhe.

```java
@Bean
@Order(1)
SecurityFilterChain apiChain(HttpSecurity http) throws Exception {
    http
        .securityMatcher("/api/**")
        .csrf(csrf -> csrf.disable())
        .sessionManagement(sm -> sm.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
        .authorizeHttpRequests(auth -> auth.anyRequest().authenticated())
        .oauth2ResourceServer(oauth -> oauth.jwt(Customizer.withDefaults()));
    return http.build();
}

@Bean
@Order(2)
SecurityFilterChain webChain(HttpSecurity http) throws Exception {
    http
        .authorizeHttpRequests(auth -> auth.anyRequest().authenticated())
        .formLogin(Customizer.withDefaults());
    return http.build();
}
```

Um request `/api/orders` casa a cadeia `apiChain` (`@Order(1)`) e nunca chega na `webChain`. Qualquer outro request cai na `webChain` (que, sem `securityMatcher`, casa tudo o que sobrou). Se você inverter os `@Order`, a cadeia web sem matcher engole `/api/orders` antes — bug clássico.

### ExceptionTranslationFilter: 401 (não-autenticado) vs 403 (não-autorizado)

O `ExceptionTranslationFilter` não decide nada de segurança — ele **traduz** exceções de segurança lançadas pelos filtros seguintes (sobretudo o `AuthorizationFilter`) em respostas HTTP. A lógica, em pseudocódigo:

```text
try {
    filterChain.doFilter(request, response);   // segue pra AuthorizationFilter etc.
} catch (AuthenticationException ou AccessDeniedException ex) {
    if (request não autenticado || ex instanceof AuthenticationException) {
        // 401: dispara o AuthenticationEntryPoint
        //   - salva o request no RequestCache (pra replay pós-login)
        //   - redireciona pro login ou envia WWW-Authenticate
        startAuthentication();
    } else {
        // 403: invoca o AccessDeniedHandler
        accessDenied();
    }
}
```

A regra mental:

- **401 (Unauthorized)** = "não sei quem você é". O request é anônimo (ou a credencial falhou). Dispara o `AuthenticationEntryPoint` — que pode redirecionar pro form login ou devolver um header `WWW-Authenticate` num cliente de API.
- **403 (Forbidden)** = "sei quem você é, mas você não pode". O `Authentication` é válido e autenticado, porém sem a authority exigida. Invoca o `AccessDeniedHandler`.

A nomenclatura HTTP é traiçoeira: `401 Unauthorized` na verdade significa **não-autenticado**, e `403 Forbidden` significa **autenticado mas não-autorizado**. O `ExceptionTranslationFilter` é o ponto onde essa distinção vira código.

### Adicionando filtro custom: addFilterBefore / addFilterAfter

Quando você precisa de lógica própria na cadeia (validar um header de tenant, aplicar rate limit, logar auditoria), o `HttpSecurity` oferece:

- `addFilterBefore(filter, ClasseDeReferencia.class)` — insere antes de um filtro existente.
- `addFilterAfter(filter, ClasseDeReferencia.class)` — insere depois.
- `addFilterAt(filter, ClasseDeReferencia.class)` — substitui um filtro na mesma posição (use com cautela).

O segredo é a **posição relativa**, ancorada num filtro de referência conhecido. Um guia prático de onde encaixar:

| Natureza do filtro custom | Posicione depois de | O que já está pronto |
| --- | --- | --- |
| Proteção contra exploit (CSRF-like, sanitização) | `SecurityContextHolderFilter` | `SecurityContext` carregado |
| Autenticação custom | `LogoutFilter` | Proteções de exploit aplicadas |
| Autorização / regras de negócio | `AnonymousAuthenticationFilter` | Autenticação resolvida (real ou anônima) |

Se o seu filtro precisa do usuário autenticado, ele tem que vir **depois** dos filtros de autenticação — caso contrário o `SecurityContextHolder` ainda estará vazio (ou só com o anônimo). Inserir antes do `SecurityContextHolderFilter` é garantir que nem o contexto existe.

## Na prática

A ordem da cadeia, visualizada (paths neutros, baseline Security 6.x):

```text
Request HTTP  GET /api/orders
      │
      ▼
DelegatingFilterProxy            (registrado no container Servlet)
      │  delega
      ▼
FilterChainProxy                 (bean Spring; aplica HttpFirewall)
      │  seleciona a 1ª SecurityFilterChain que casa o RequestMatcher
      ▼
SecurityFilterChain  (securityMatcher = /api/**)
      │
      ├─ DisableEncodeUrlFilter
      ├─ WebAsyncManagerIntegrationFilter
      ├─ SecurityContextHolderFilter        ← carrega o SecurityContext
      ├─ HeaderWriterFilter
      ├─ CorsFilter
      ├─ CsrfFilter                          ← (desligado em /api/** stateless)
      ├─ LogoutFilter
      ├─ BearerTokenAuthenticationFilter     ← autenticação (Bearer/JWT)
      ├─ RequestCacheAwareFilter
      ├─ SecurityContextHolderAwareRequestFilter
      ├─ AnonymousAuthenticationFilter       ← identidade anônima se ninguém autenticou
      ├─ ExceptionTranslationFilter          ← traduz 401 / 403
      └─ AuthorizationFilter                 ← decisão final (último)
      │
      ▼
DispatcherServlet  →  Controller  →  /api/orders
```

Um filtro custom de tenant, inserido antes da autenticação por usuário/senha:

```java
public class TenantHeaderFilter extends OncePerRequestFilter {

    @Override
    protected void doFilterInternal(HttpServletRequest request,
                                    HttpServletResponse response,
                                    FilterChain chain)
            throws ServletException, IOException {

        String tenantId = request.getHeader("X-Tenant-Id");
        if (tenantId == null || tenantId.isBlank()) {
            response.sendError(HttpServletResponse.SC_BAD_REQUEST,
                    "Missing X-Tenant-Id header");
            return; // aborta a cadeia: nada depois roda
        }

        TenantContext.set(tenantId);
        try {
            chain.doFilter(request, response); // segue pra cadeia de segurança
        } finally {
            TenantContext.clear(); // sempre limpa o ThreadLocal
        }
    }
}

@Bean
SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
    http
        .authorizeHttpRequests(auth -> auth
            .requestMatchers("/api/admin/**").hasRole("ADMIN")
            .anyRequest().authenticated())
        .httpBasic(Customizer.withDefaults())
        // insere o TenantHeaderFilter antes do filtro de form login
        .addFilterBefore(new TenantHeaderFilter(),
                         UsernamePasswordAuthenticationFilter.class);
    return http.build();
}
```

O `addFilterBefore(..., UsernamePasswordAuthenticationFilter.class)` garante que o tenant é resolvido antes de qualquer tentativa de autenticação por formulário — mas depois do `SecurityContextHolderFilter`, então o contexto de segurança já existe se algum filtro anterior tiver populado.

## Armadilhas

### (1) Filtro custom na posição errada

Inserir um filtro **antes** do `SecurityContextHolderFilter` e depender do usuário autenticado dentro dele. Nessa posição o `SecurityContextHolder` ainda não foi carregado — `getAuthentication()` retorna `null` (ou um anônimo, se você empurrou o filtro pra depois do `AnonymousAuthenticationFilter` mas confunde anônimo com não-autenticado).

```java
// PROBLEMA: filtro de auditoria que lê o usuário, mas roda cedo demais
http.addFilterBefore(new AuditFilter(), SecurityContextHolderFilter.class);
// dentro do AuditFilter: SecurityContextHolder.getContext().getAuthentication() == null
```

**Fix:** ancore o filtro num ponto onde o estado de que ele depende já existe. Para ler o usuário autenticado, insira **depois** dos filtros de autenticação (ex.: `addFilterAfter(new AuditFilter(), AuthorizationFilter.class)` ou depois do `AnonymousAuthenticationFilter`, conforme a necessidade). Consulte a tabela de posicionamento.

### (2) Assumir um único SecurityFilterChain

Configurar duas `SecurityFilterChain` e esperar que ambas se apliquem ao mesmo request, ou ignorar a ordem dos `@Order`. O `FilterChainProxy` usa **só a primeira** cadeia cujo matcher casa; as demais não são consultadas.

```java
@Bean @Order(1)
SecurityFilterChain webChain(HttpSecurity http) throws Exception {
    http.authorizeHttpRequests(a -> a.anyRequest().authenticated())
        .formLogin(Customizer.withDefaults());     // SEM securityMatcher → casa TUDO
    return http.build();
}

@Bean @Order(2)
SecurityFilterChain apiChain(HttpSecurity http) throws Exception {
    http.securityMatcher("/api/**")               // nunca alcançado: webChain casa /api/** antes
        .oauth2ResourceServer(o -> o.jwt(Customizer.withDefaults()));
    return http.build();
}
```

**Fix:** ordene da cadeia **mais específica** pra mais genérica. A cadeia com `securityMatcher("/api/**")` vem com `@Order` menor que a cadeia "pega-tudo" sem matcher. A genérica sempre por último.

### (3) Confundir Filter (Servlet, Galho 9) com SecurityFilterChain (a cadeia de segurança)

Tratar `Filter`, `Interceptor` e `SecurityFilterChain` como a mesma coisa. O `Filter` genérico e os `Interceptor`s do Spring MVC são da camada web (Galho 9, ver [[03-Dominios/Tecnologia/Java/Web e APIs REST/11 - Interceptors vs Filters|Interceptors vs Filters]]); o `SecurityFilterChain` é a cadeia específica de segurança orquestrada pelo `FilterChainProxy`, que por sua vez é **um** `Filter` da plataforma. Misturar isso leva a registrar segurança no lugar errado — ex.: tentar fazer autorização num `HandlerInterceptor`, que roda **depois** de toda a cadeia de segurança e do `DispatcherServlet`.

```java
// PROBLEMA: autorização tardia num interceptor MVC, fora da cadeia de segurança
public class AuthInterceptor implements HandlerInterceptor {
    // roda DEPOIS do AuthorizationFilter já ter liberado o request
}
```

**Fix:** regras de autorização ficam na cadeia de segurança (`authorizeHttpRequests` ou filtro custom posicionado na cadeia). Interceptors MVC servem pra preocupações de view/handler (logging de handler, modificação de model), não pra controle de acesso.

## Em entrevista

### Frase pronta (inglês)

> Spring Security is, at its core, a single Servlet `Filter` called `FilterChainProxy` that the `DelegatingFilterProxy` registers with the container. It holds an ordered list of `SecurityFilterChain` instances, and for each request it runs the first chain whose `RequestMatcher` matches — selection is order-sensitive, so I declare the most specific `securityMatcher` first and the catch-all last. Inside a chain the filter order is fixed and meaningful: `SecurityContextHolderFilter` loads the context, the authentication filters run, `AnonymousAuthenticationFilter` provides a fallback identity, and `AuthorizationFilter` decides access last. The `ExceptionTranslationFilter` sits just before it to translate failures into a 401 via the `AuthenticationEntryPoint` when the user is unauthenticated, or a 403 via the `AccessDeniedHandler` when they're authenticated but lack the authority. When I need custom logic I anchor it with `addFilterBefore` or `addFilterAfter` relative to a known filter, so it runs once the state it depends on is already in place.

### Vocabulário

| Termo (inglês) | Tradução / sentido |
| --- | --- |
| filter chain | cadeia de filtros que processa cada request |
| delegate to a bean | delegar a execução pra um bean Spring |
| request matcher | objeto que decide se uma cadeia atende o request |
| order-sensitive | sensível à ordem (a primeira cadeia que casa vence) |
| authentication entry point | ponto que dispara o fluxo de autenticação (401) |
| access denied handler | handler que responde quando falta permissão (403) |
| anchor a filter | ancorar um filtro relativo a outro (before/after) |
| unauthenticated vs unauthorized | não-autenticado (401) vs não-autorizado (403) |

## Veja também

- [[03-Dominios/Tecnologia/Java/Segurança/01 - O que é Spring Security — authn, authz e o filter chain|O que é Spring Security]]
- [[03-Dominios/Tecnologia/Java/Segurança/10 - CSRF — por que ligado por default e quando desligar|CSRF]]
- [[03-Dominios/Tecnologia/Java/Web e APIs REST/11 - Interceptors vs Filters|Interceptors vs Filters]]
- [[03-Dominios/Tecnologia/Java/Web e APIs REST/06 - O pipeline do DispatcherServlet|O pipeline do DispatcherServlet]]
- [[03-Dominios/Tecnologia/Java/Jakarta EE/03 - Servlet API — o alicerce HTTP|Servlet API — o alicerce HTTP]]
- [[03-Dominios/Tecnologia/Java/Segurança/index|Segurança (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java]]

## Referências

- Spring Security Reference — Servlet Architecture: https://docs.spring.io/spring-security/reference/servlet/architecture.html
