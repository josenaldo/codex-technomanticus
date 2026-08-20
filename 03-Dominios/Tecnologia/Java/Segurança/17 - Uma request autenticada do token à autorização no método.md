---
title: "Uma request autenticada do token à autorização no método"
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
  - filter-chain
  - jwt
aliases:
  - "request autenticada de ponta a ponta"
  - "trace de uma request autenticada"
---

# Uma request autenticada do token à autorização no método

> [!abstract] TL;DR
> Um cabeçalho `Authorization: Bearer <jwt>` entra pelo filter chain do Spring Security. O `BearerTokenAuthenticationFilter` extrai o token; o `JwtDecoder` faz decode e validação (assinatura via JWKS, mais `iss`/`aud`/`exp` e a whitelist de `alg`); o `JwtAuthenticationConverter` monta um `Authentication` que vai pro `SecurityContextHolder`. Daí o `AuthorizationFilter` aplica as regras de URL, o `DispatcherServlet` despacha pro controller, e quando o controller chama o service o proxy AOP do `@PreAuthorize` intercepta antes do método. Qualquer falha é traduzida pelo `ExceptionTranslationFilter` em **401** (não-autenticado) ou **403** (não-autorizado). Esta nota costura todas essas peças num fluxo único.

## O que é

Esta é uma nota de **trace**: ela não introduz nenhum conceito novo, ela amarra os conceitos já vistos no galho numa sequência cronológica. A pergunta que ela responde é simples de enunciar e fácil de errar: *"o que exatamente acontece, em ordem, entre a request chegar com um JWT no header e a regra `@PreAuthorize` liberar (ou barrar) o método de service?"*

A resposta não é "o token chega, o Spring valida, pronto". São várias estações, em duas camadas de autorização distintas, com dois caminhos de erro semanticamente diferentes. Ver o fluxo inteiro de uma vez é o que separa quem decora nomes de filtros de quem entende a arquitetura.

## Por que importa

Em entrevista senior, a pergunta "explique o que acontece quando uma request autenticada chega na sua API" é um teste de profundidade. Quem responde só com "tem um filtro que valida o token" para na superfície. Quem traça a sequência — filtro de extração, validação multi-claim, montagem do `Authentication`, autorização de URL, despacho, autorização de método, tradução de erro — demonstra que entende o sistema como um pipeline, não como uma caixa-preta.

No dia a dia, esse mapa mental é o que te faz debugar rápido: um 401 e um 403 apontam para estações completamente diferentes do fluxo. Saber onde cada coisa acontece é saber onde colocar o breakpoint.

## O fluxo passo a passo

### 1. BearerTokenAuthenticationFilter: extrai o token do header

A request chega ao filter chain. Antes de qualquer lógica de negócio, ela atravessa uma fila ordenada de `Filter`s. O primeiro relevante aqui é o `BearerTokenAuthenticationFilter`.

A função dele é estreita: ler o cabeçalho `Authorization`, verificar o esquema `Bearer`, e extrair o valor cru do token. Com isso ele monta um `BearerTokenAuthenticationToken` — uma *tentativa* de autenticação, ainda não validada — e entrega ao `AuthenticationManager`.

Repare: nesse ponto o token é só uma string opaca. Nada foi verificado. Se o header estiver ausente ou malformado, o filtro simplesmente não autentica e deixa a request seguir como anônima — a barragem virá depois, na autorização.

### 2. Decode + validação (assinatura/JWKS, iss/aud/exp, whitelist de alg)

O `AuthenticationManager` delega ao `JwtAuthenticationProvider`, que usa um `JwtDecoder` (na prática o `NimbusJwtDecoder`) para fazer o trabalho pesado. E "validar o JWT" é mais coisa do que a maioria imagina:

- **Assinatura via JWKS** — o decoder busca as chaves públicas no endpoint JWKS do issuer (descoberto a partir do `issuer-uri`) e verifica a assinatura. As chaves rotacionam, e o Spring atualiza o cache automaticamente.
- **Whitelist de `alg`** — só algoritmos permitidos passam (default `RS256`). Isso fecha a porta para o ataque clássico de `alg: none` ou downgrade para HMAC com a chave pública.
- **`exp` / `nbf`** — o `JwtTimestampValidator` rejeita token expirado ou ainda-não-válido, com tolerância de clock skew (60s por padrão).
- **`iss`** — o `JwtIssuerValidator` confirma que o token foi emitido por quem você espera.
- **`aud`** — um validador de audiência (configurável) confirma que o token foi emitido *para esta API*, não para outro serviço do mesmo emissor.

Esses validadores são compostos via `DelegatingOAuth2TokenValidator`. Falha em qualquer um deles e o resultado é uma `AuthenticationException` — que vira 401 lá na frente.

### 3. JwtAuthenticationConverter monta o Authentication → SecurityContextHolder

Token decodificado e validado, falta transformá-lo num objeto que o resto do Spring entende. É o papel do `JwtAuthenticationConverter`: ele lê os claims (tipicamente `scope`/`scp`, ou `roles`) e os mapeia para `GrantedAuthority` — por padrão com prefixo `SCOPE_`, ou `ROLE_` quando configurado. O principal vira o próprio `Jwt`, e o nome da autenticação vira o claim `sub`.

O resultado é um `Authentication` autenticado (um `JwtAuthenticationToken`), que o filtro deposita no `SecurityContextHolder`. A partir daqui, "quem é o usuário e o que ele pode fazer" está disponível para todo o resto da request — controller, service, qualquer ponto que consulte o contexto de segurança.

### 4. AuthorizationFilter: regras de URL (authorizeHttpRequests)

Com o `Authentication` no contexto, a request chega ao `AuthorizationFilter` (sucessor do antigo `FilterSecurityInterceptor`). Esta é a **primeira camada de autorização**: a de *URL*.

É aqui que as regras declaradas em `authorizeHttpRequests` são aplicadas — por exemplo, `/api/orders/**` exige autenticação, `/actuator/health` é público. O filtro consulta as authorities do `Authentication` e decide se a request pode prosseguir. Se não puder, lança `AccessDeniedException` (rumo ao 403) ou, se nem autenticado havia, dispara o caminho de 401.

Ponto-chave: essa camada raciocina sobre *caminhos e métodos HTTP*, não sobre regras de domínio. Ela diz "esse path exige `ROLE_ADMIN`", não "esse usuário pode editar *este* pedido específico".

### 5. DispatcherServlet → controller (Galho 9)

Passada a autorização de URL, a request finalmente sai do filter chain e entra na camada MVC. O `DispatcherServlet` faz o despacho para o `@Controller` apropriado — handler mapping, argument resolvers, tudo o que já vimos.

Não vou re-explicar o despacho aqui; o mecanismo do `DispatcherServlet` está detalhado no Galho 9. O que importa para *este* trace é só a posição dele na linha do tempo: o controller só executa depois que o usuário já foi autenticado e a URL já foi autorizada.

> Detalhe do trace: o controller roda **depois** de duas estações de segurança (extração/validação do token e autorização de URL). Ele nunca é o primeiro a ver a request.

### 6. @PreAuthorize: o proxy AOP intercepta antes do método (Galho 8)

O controller chama o service. E é aqui que entra a **segunda camada de autorização**: a de *método*. Quando um método de service está anotado com `@PreAuthorize`, a chamada não vai direto pro objeto real — vai pra um *proxy*.

Esse proxy AOP intercepta a invocação, avalia a expressão SpEL do `@PreAuthorize` (consultando o `Authentication` que ainda está no `SecurityContextHolder`), e só então delega para o método real — ou lança `AccessDeniedException` se a expressão for falsa.

O mecanismo de proxy e AOP em si está no Galho 8; não vou repetir como o Spring cria o proxy. O ponto do trace é a *ordem*: a checagem de método acontece **depois** do controller começar a executar, numa granularidade que a camada de URL não alcança — `@PreAuthorize("hasRole('ADMIN') or #userId == authentication.name")` raciocina sobre os argumentos da chamada.

### O caminho do erro: 401 (não-autenticado) vs 403 (não-autorizado) via ExceptionTranslationFilter

As exceções de segurança não viram stack trace cru pro cliente. Um filtro dedicado, o `ExceptionTranslationFilter`, fica posicionado no chain *envolvendo* a autorização e captura o que vier de baixo, traduzindo para HTTP:

- **`AuthenticationException`** (ou request não-autenticada) → **401 Unauthorized**. O filtro limpa o `SecurityContextHolder`, salva a request no `RequestCache` e invoca o `AuthenticationEntryPoint` (numa API stateless, tipicamente devolve `WWW-Authenticate` e 401).
- **`AccessDeniedException` com usuário já autenticado** → **403 Forbidden**, via `AccessDeniedHandler`.

A regra de decisão é exatamente essa: *já tinha gente autenticada?* Se não (ou se a exceção é de autenticação), é 401 — "eu não sei quem você é". Se sim, mas faltou permissão, é 403 — "eu sei quem você é, e você não pode". Essa distinção vale tanto para a falha na camada de URL (passo 4) quanto na de método (passo 6): o `AccessDeniedException` do `@PreAuthorize` sobe pelo chain e cai no mesmo tradutor.

## Na prática

O fluxo completo, com paths neutros:

```text
Request:  GET /api/orders/42
          Authorization: Bearer eyJhbGciOiJSUzI1NiI...

┌─────────────────────────── FILTER CHAIN ───────────────────────────┐
│                                                                     │
│  [ExceptionTranslationFilter]  ── envolve tudo abaixo ──┐           │
│        │                                                │           │
│        ▼                                                │           │
│  (1) BearerTokenAuthenticationFilter                    │           │
│        │  extrai "eyJ..." do header Authorization       │           │
│        ▼                                                │           │
│  (2) JwtDecoder (NimbusJwtDecoder)                      │           │
│        │  assinatura via JWKS + alg whitelist           │           │
│        │  iss / aud / exp / nbf                          │  falha?  │
│        ▼                                                │  ──► 401  │
│  (3) JwtAuthenticationConverter                         │           │
│        │  claims → GrantedAuthority (SCOPE_/ROLE_)      │           │
│        ▼  Authentication ──► SecurityContextHolder      │           │
│  (4) AuthorizationFilter (URL: authorizeHttpRequests)   │  falha?  │
│        │  "/api/orders/** exige autenticação"           │  ──► 403  │
│        ▼                                                │  (ou 401) │
└────────┼────────────────────────────────────────────────┘          │
         ▼                                                            │
  (5) DispatcherServlet  ─────────────────────────────► OrderController
         │                                                            │
         ▼                                                            │
  (6) OrderService.findById(42)                                       │
         │  proxy AOP do @PreAuthorize intercepta ANTES               │
         │  avalia SpEL contra o SecurityContext         falha? ──► 403
         ▼                                                            │
       método real executa ──► 200 OK                                 │
```

O código mínimo que materializa cada etapa — config de Resource Server stateless mais o `@PreAuthorize` no service:

```java
@Configuration
@EnableWebSecurity
@EnableMethodSecurity // habilita @PreAuthorize (proxy AOP — Galho 8)
class SecurityConfig {

    @Bean
    SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .csrf(csrf -> csrf.disable())
            .sessionManagement(sm ->
                sm.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            // passo 4: autorização de URL
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/actuator/health").permitAll()
                .requestMatchers("/api/orders/**").authenticated()
                .anyRequest().denyAll())
            // passos 1-3: Resource Server JWT
            .oauth2ResourceServer(oauth2 -> oauth2.jwt(Customizer.withDefaults()));
        return http.build();
    }
}
```

```yaml
# application.yml — dispara a config automática do decoder + validadores
spring:
  security:
    oauth2:
      resourceserver:
        jwt:
          issuer-uri: https://idp.example.com   # descobre JWKS + valida iss
          audiences: https://orders-api.example.com  # valida aud
```

```java
@Service
class OrderService {

    // passo 6: o proxy AOP avalia ANTES de o método real rodar
    @PreAuthorize("hasRole('ADMIN') or #userId == authentication.name")
    public Order findForUser(Long orderId, String userId) {
        // só executa se a expressão acima for verdadeira
        return repository.findByIdAndOwner(orderId, userId);
    }
}
```

## Armadilhas

### (1) "O token chega direto no controller"

A intuição ingênua é que o controller recebe a request e "pega o token". Errado: quando o método do controller executa, o token **já foi extraído, decodificado, validado e transformado em `Authentication`** — tudo no filter chain, antes de qualquer código de MVC rodar. O controller nunca vê o header `Authorization` cru no fluxo normal; ele vê (se quiser) um `Authentication` pronto no `SecurityContext`.

**Fix:** lembre que o filter chain inteiro (passos 1–4) acontece *antes* do `DispatcherServlet`. Para acessar o usuário no controller, injete `@AuthenticationPrincipal Jwt jwt` ou leia o `SecurityContextHolder` — nunca parseie o header à mão.

### (2) "Autorização é só no controller"

Tratar autorização como uma coisa só, no controller, é misturar duas camadas distintas. Há **autorização de URL** (passo 4, `AuthorizationFilter`, antes do controller) **e** **autorização de método** (passo 6, `@PreAuthorize`, dentro do service). São granularidades diferentes: URL raciocina sobre paths e roles grossas; método raciocina sobre argumentos e regras de domínio finas.

**Fix:** desenhe as duas camadas de propósito. URL barra o tráfego óbvio cedo e barato (`/admin/**` exige `ROLE_ADMIN`); método protege a regra de negócio fina (`#userId == authentication.name`). Confiar só numa delas deixa buraco — só URL não vê os argumentos; só método deixa endpoints inteiros expostos.

### (3) "Validar JWT é só checar a assinatura"

Verificar só a assinatura te protege contra forja, mas não contra reuso indevido. Um token com assinatura válida ainda pode estar **expirado** (`exp`), emitido por **outro issuer** (`iss`), destinado a **outra API** (`aud`), ou assinado com um **algoritmo perigoso** que você deveria recusar (`alg`).

**Fix:** confie na config automática do Resource Server, que já encadeia `JwtTimestampValidator` (`exp`/`nbf`) e `JwtIssuerValidator` (`iss`), e adicione explicitamente o validador de `aud` quando o emissor serve várias APIs. Mantenha a whitelist de `alg` restrita (assimétrico, `RS256`/`ES256`) — nunca aceite `none`.

## Em entrevista

### Frase pronta (inglês)

> When an authenticated request hits the API, it doesn't reach the controller first — it travels through the security filter chain. The `BearerTokenAuthenticationFilter` extracts the JWT from the `Authorization: Bearer` header, the `JwtDecoder` validates the signature against the issuer's JWKS endpoint and checks the `iss`, `aud`, and `exp` claims plus the allowed algorithms, and a converter turns the validated token into an `Authentication` stored in the `SecurityContextHolder`. Only then does the `AuthorizationFilter` enforce URL rules, the `DispatcherServlet` dispatches to the controller, and `@PreAuthorize` — via an AOP proxy — runs method-level checks before the service method executes. If anything fails, the `ExceptionTranslationFilter` translates it into a 401 when the caller isn't authenticated, or a 403 when they are authenticated but lack permission.

### Vocabulário

| Termo (EN) | Significado |
| --- | --- |
| security filter chain | fila ordenada de filtros que processa a request antes do MVC |
| bearer token | token portador enviado no header `Authorization: Bearer` |
| JWKS endpoint | endpoint que publica as chaves públicas para verificar a assinatura |
| claims validation | checagem de `iss`/`aud`/`exp`/`nbf` além da assinatura |
| algorithm whitelist | lista de algoritmos de assinatura aceitos (recusa `none`/downgrade) |
| URL authorization | autorização por path/método HTTP no `AuthorizationFilter` |
| method security | autorização por método via `@PreAuthorize` (proxy AOP) |
| 401 vs 403 | não-autenticado (não sei quem é) vs não-autorizado (sei, mas não pode) |

## Veja também

- [[03-Dominios/Tecnologia/Java/Segurança/06 - A arquitetura do filter chain em profundidade|A arquitetura do filter chain]]
- [[03-Dominios/Tecnologia/Java/Segurança/09 - OAuth2 Resource Server — validando JWT na API|OAuth2 Resource Server]]
- [[03-Dominios/Tecnologia/Java/Segurança/18 - Capstone — projetando a segurança de uma API Spring production-grade|Capstone de segurança]]
- [[03-Dominios/Tecnologia/Java/Spring Core e Boot/09 - AOP e proxies no Spring|AOP e proxies no Spring]]
- [[03-Dominios/Tecnologia/Java/Segurança/index|Segurança (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java]]

## Referências

- Spring Security Reference — Architecture (Servlet): https://docs.spring.io/spring-security/reference/servlet/architecture.html
- Spring Security Reference — OAuth2 Resource Server JWT: https://docs.spring.io/spring-security/reference/servlet/oauth2/resource-server/jwt.html
