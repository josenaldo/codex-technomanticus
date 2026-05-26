---
title: "Spring Security"
created: 2026-04-11
updated: 2026-04-11
type: concept
status: evergreen
tags:
  - java
  - backend
  - seguranca
  - entrevista
publish: false
---

# Spring Security

Deep dive em **autenticação**, **autorização**, **JWT**, **OAuth2/OIDC**, **method security**, **CSRF**, **CORS** e patterns de segurança na stack Spring. Para fundamentos de auth em APIs, ver [[API Design]] (seção Autenticação). Para Spring Boot em geral, ver [[Spring Boot]].

## O que é

Spring Security é o framework de segurança do ecossistema Spring. Lida com **autenticação** (quem você é) e **autorização** (o que você pode fazer), além de proteção contra ataques comuns (CSRF, session fixation, clickjacking, XSS).

É construído sobre o conceito de **Filter Chain** — uma pipeline de filtros que intercepta requests antes de chegarem aos controllers. Cada filtro tem uma responsabilidade específica: autenticação, autorização, CSRF, CORS, headers de segurança, etc.

Em entrevistas, o que diferencia um senior em Spring Security:

1. **Entender a Filter Chain** — como requests fluem, onde customizar
2. **Authentication vs Authorization** — conceitos, não misturar
3. **Dominar JWT** — como validar, limitações, refresh tokens, revogação
4. **OAuth2 + OIDC** — fluxos (authorization code, client credentials), resource server vs client
5. **Method-level security** — `@PreAuthorize`, `@PostAuthorize`, expressions
6. **CSRF e quando desabilitar** — APIs stateless vs web tradicional
7. **CORS correto** — origens, headers, credentials
8. **Password storage** — BCrypt, Argon2, quando usar qual
9. **Session management** — stateless vs stateful, fixation, concurrent sessions
10. **Common vulnerabilities** — OWASP Top 10 em Spring

---

## Evolução da configuração

Spring Security mudou sua API várias vezes. Em 2026, você verá código de várias eras. **Aprenda a versão moderna (Spring Security 6+)**, mas reconheça o legado.

### Spring Security 6+ (atual, 2023+)

Component-based, sem herança de `WebSecurityConfigurerAdapter` (que foi removido).

```java
@Configuration
@EnableWebSecurity
@EnableMethodSecurity
public class SecurityConfig {

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        return http
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/api/public/**").permitAll()
                .requestMatchers("/api/admin/**").hasRole("ADMIN")
                .anyRequest().authenticated()
            )
            .oauth2ResourceServer(oauth2 -> oauth2.jwt(Customizer.withDefaults()))
            .sessionManagement(sm -> sm.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .csrf(csrf -> csrf.disable())  // stateless API
            .build();
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }
}
```

### Spring Security 5.x (legacy mas comum)

Com `WebSecurityConfigurerAdapter`:

```java
// LEGADO — removido em Spring Security 6
@EnableWebSecurity
public class SecurityConfig extends WebSecurityConfigurerAdapter {
    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http.authorizeRequests()
            .antMatchers("/public/**").permitAll()
            .anyRequest().authenticated();
    }
}
```

**Mudança principal:** `antMatchers` → `requestMatchers`, configuração via lambda em vez de método chain.

---

## Filter Chain — a arquitetura central

Toda a magia do Spring Security acontece via **filter chain**. Entender isso é entender Spring Security.

```
HTTP Request
    ↓
Servlet Container (Tomcat)
    ↓
FilterChainProxy (Spring Security)
    ↓
[SecurityFilterChain] — lista ordenada de filtros
    ↓
 1. DisableEncodeUrlFilter
 2. WebAsyncManagerIntegrationFilter
 3. SecurityContextHolderFilter     ← carrega SecurityContext da session
 4. HeaderWriterFilter               ← headers de segurança (X-Frame-Options, etc.)
 5. CorsFilter                       ← CORS
 6. CsrfFilter                       ← CSRF protection
 7. LogoutFilter                     ← logout handling
 8. OAuth2AuthorizationRequestRedirectFilter  ← OAuth2 (se configurado)
 9. Saml2WebSsoAuthenticationFilter  ← SAML (se configurado)
10. UsernamePasswordAuthenticationFilter ← form login
11. DefaultLoginPageGeneratingFilter
12. DefaultLogoutPageGeneratingFilter
13. ConcurrentSessionFilter
14. DigestAuthenticationFilter
15. BasicAuthenticationFilter        ← HTTP Basic auth
16. RequestCacheAwareFilter
17. SecurityContextHolderAwareRequestFilter
18. AnonymousAuthenticationFilter    ← cria "anonymous" auth se não houver
19. SessionManagementFilter
20. ExceptionTranslationFilter       ← converte exceções em responses HTTP
21. AuthorizationFilter              ← último — valida autorização
    ↓
Controller
```

Cada filtro verifica o que é relevante para ele e passa para o próximo. Se algo falha (ex.: não autenticado), `ExceptionTranslationFilter` traduz em 401 ou redirect.

### SecurityContextHolder

É o "current user" — onde o principal autenticado fica durante o request.

```java
SecurityContext context = SecurityContextHolder.getContext();
Authentication auth = context.getAuthentication();

String username = auth.getName();
Collection<? extends GrantedAuthority> authorities = auth.getAuthorities();
Object principal = auth.getPrincipal();  // tipicamente UserDetails ou Jwt
```

Em Spring Boot com virtual threads, `SecurityContextHolder` usa `ThreadLocal` por default — funciona, mas considere **scoped values** em Java 25+ para eficiência.

### Authentication vs Principal

- **`Authentication`** — objeto que representa a tentativa ou resultado de autenticação. Contém principal, credentials, authorities.
- **`Principal`** — "quem" é o user (tipicamente `UserDetails`, `Jwt`, ou `OidcUser`).
- **`Authorities`** — o que o user pode fazer (roles, permissions, scopes).

```java
public interface Authentication extends Principal, Serializable {
    Collection<? extends GrantedAuthority> getAuthorities();
    Object getCredentials();
    Object getDetails();
    Object getPrincipal();
    boolean isAuthenticated();
    // ...
}
```

---

## Autenticação

### Tipos de autenticação comuns

| Tipo | Quando usar |
| --- | --- |
| **HTTP Basic** | Internal, simples, sempre com HTTPS |
| **Form Login** | Web apps tradicionais com sessão |
| **JWT (Resource Server)** | APIs REST stateless, microserviços |
| **OAuth2 / OIDC Client** | Login social (Google, GitHub), delegação |
| **OAuth2 Authorization Server** | Você é o provedor de identidade |
| **API Key** | Server-to-server, integrações B2B |
| **mTLS** | Zero trust, microserviços internos, altamente sensível |
| **SAML** | Enterprise SSO (Active Directory, Okta) |

### Form Login (web tradicional)

```java
@Bean
public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
    return http
        .authorizeHttpRequests(auth -> auth
            .requestMatchers("/login", "/css/**").permitAll()
            .anyRequest().authenticated()
        )
        .formLogin(form -> form
            .loginPage("/login")
            .loginProcessingUrl("/perform_login")
            .defaultSuccessUrl("/dashboard", true)
            .failureUrl("/login?error=true")
        )
        .logout(logout -> logout
            .logoutUrl("/perform_logout")
            .logoutSuccessUrl("/login?logout=true")
            .deleteCookies("JSESSIONID")
        )
        .build();
}
```

**Caso de uso:** aplicações web server-rendered (Thymeleaf, JSP). Para APIs, prefira JWT.

### HTTP Basic

```java
http.httpBasic(Customizer.withDefaults());
```

Simples, mas cada request envia `Authorization: Basic base64(user:pass)`. **Sempre use sobre HTTPS.**

**Uso típico:** APIs internas simples, server-to-server trusted, ou endpoints de emergência.

### UserDetailsService — carregando users do banco

```java
@Service
@RequiredArgsConstructor
public class UserDetailsServiceImpl implements UserDetailsService {

    private final UserRepository userRepository;

    @Override
    public UserDetails loadUserByUsername(String email) throws UsernameNotFoundException {
        return userRepository.findByEmail(email)
            .map(user -> User.builder()
                .username(user.getEmail())
                .password(user.getPasswordHash())
                .authorities(user.getRoles().stream()
                    .map(role -> new SimpleGrantedAuthority("ROLE_" + role.getName()))
                    .toList())
                .accountExpired(false)
                .accountLocked(!user.isActive())
                .credentialsExpired(false)
                .disabled(!user.isActive())
                .build())
            .orElseThrow(() -> new UsernameNotFoundException("User not found: " + email));
    }
}
```

**Default do Spring Security:** Spring Security detecta automaticamente um bean `UserDetailsService` e usa para autenticar.

### AuthenticationManager

O coração da autenticação. Recebe `Authentication` object e retorna `Authentication` populada (com authorities) se sucesso.

```java
@Bean
public AuthenticationManager authenticationManager(
        AuthenticationConfiguration config) throws Exception {
    return config.getAuthenticationManager();
}
```

Você raramente interage diretamente — os filtros fazem o trabalho. Mas pode usar para autenticação programática:

```java
Authentication auth = authManager.authenticate(
    new UsernamePasswordAuthenticationToken(email, password)
);
SecurityContextHolder.getContext().setAuthentication(auth);
```

### Password encoding

**Nunca armazene senha em plain text.** Spring Security oferece múltiplos encoders:

| Encoder | Quando usar |
| --- | --- |
| **BCryptPasswordEncoder** | **Default recomendado**. Slow-by-design, work factor ajustável |
| **Argon2PasswordEncoder** | Mais moderno, vencedor do Password Hashing Competition 2015 |
| **Scrypt** | Alternativa, menos usado |
| **Pbkdf2PasswordEncoder** | Compatibilidade com padrões FIPS |
| **DelegatingPasswordEncoder** | Permite migração entre algoritmos |

```java
@Bean
public PasswordEncoder passwordEncoder() {
    return new BCryptPasswordEncoder(12);  // work factor 12 (default 10)
}

// Uso
String hash = passwordEncoder.encode("senha-do-user");
boolean matches = passwordEncoder.matches("senha-do-user", hash);
```

**Migração de senhas legadas:**

```java
@Bean
public PasswordEncoder passwordEncoder() {
    String defaultEncoderId = "bcrypt";
    Map<String, PasswordEncoder> encoders = new HashMap<>();
    encoders.put("bcrypt", new BCryptPasswordEncoder());
    encoders.put("argon2", new Argon2PasswordEncoder(...));
    encoders.put("noop", NoOpPasswordEncoder.getInstance());  // legacy

    return new DelegatingPasswordEncoder(defaultEncoderId, encoders);
}
```

Hashes ficam no formato `{bcrypt}$2a$10$...` — o prefixo identifica o algoritmo. Permite migração gradual.

---

## JWT (JSON Web Tokens)

JWT é o padrão de facto para autenticação em APIs stateless. Spring Security 5.2+ tem suporte nativo via **OAuth2 Resource Server**.

### Estrutura de um JWT

```
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.signature
|__________ header ______________||__________ payload ______________||_signature_|
```

Três partes separadas por `.`:

1. **Header** — algoritmo de assinatura (`alg`), tipo (`typ`)
2. **Payload** — claims (dados do user, expiração, etc.)
3. **Signature** — assinatura verificando que não foi alterado

**Claims comuns:**

- `iss` — issuer (quem emitiu)
- `sub` — subject (user ID)
- `aud` — audience (para quem é)
- `exp` — expiration time
- `nbf` — not before
- `iat` — issued at
- `jti` — JWT ID (único, permite revogação)
- Claims customizadas — `roles`, `email`, `tenant_id`, etc.

### Resource Server (validar JWTs)

Cenário comum: sua API recebe JWTs emitidos por outro sistema (Auth0, Keycloak, Cognito) e precisa validá-los.

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-oauth2-resource-server</artifactId>
</dependency>
```

```yaml
spring:
  security:
    oauth2:
      resourceserver:
        jwt:
          issuer-uri: https://auth.medespecialista.com
          # ou jwk-set-uri: https://auth.medespecialista.com/.well-known/jwks.json
```

```java
@Bean
public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
    return http
        .authorizeHttpRequests(auth -> auth
            .requestMatchers("/api/public/**").permitAll()
            .requestMatchers("/api/admin/**").hasAuthority("SCOPE_admin")
            .anyRequest().authenticated()
        )
        .oauth2ResourceServer(oauth2 -> oauth2
            .jwt(jwt -> jwt.jwtAuthenticationConverter(jwtAuthConverter()))
        )
        .sessionManagement(sm -> sm.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
        .csrf(csrf -> csrf.disable())
        .build();
}

@Bean
public JwtAuthenticationConverter jwtAuthConverter() {
    JwtGrantedAuthoritiesConverter authsConverter = new JwtGrantedAuthoritiesConverter();
    authsConverter.setAuthorityPrefix("ROLE_");
    authsConverter.setAuthoritiesClaimName("roles");  // ou "scope"

    JwtAuthenticationConverter converter = new JwtAuthenticationConverter();
    converter.setJwtGrantedAuthoritiesConverter(authsConverter);
    return converter;
}
```

### Acessando o JWT no controller

```java
@GetMapping("/me")
public UserInfo me(@AuthenticationPrincipal Jwt jwt) {
    return new UserInfo(
        jwt.getSubject(),
        jwt.getClaimAsString("email"),
        jwt.getClaimAsStringList("roles")
    );
}
```

### Emitindo JWTs (Authorization Server)

Se você é o emissor, use **Spring Authorization Server** (substituiu o legacy Spring Security OAuth):

```xml
<dependency>
    <groupId>org.springframework.security</groupId>
    <artifactId>spring-security-oauth2-authorization-server</artifactId>
</dependency>
```

Ou implemente manualmente com **jjwt** ou **Nimbus JOSE+JWT**:

```java
@Service
public class JwtService {

    private final JwtEncoder jwtEncoder;

    public String generateToken(Authentication auth) {
        Instant now = Instant.now();

        String scope = auth.getAuthorities().stream()
            .map(GrantedAuthority::getAuthority)
            .collect(Collectors.joining(" "));

        JwtClaimsSet claims = JwtClaimsSet.builder()
            .issuer("medespecialista")
            .issuedAt(now)
            .expiresAt(now.plus(1, ChronoUnit.HOURS))
            .subject(auth.getName())
            .claim("scope", scope)
            .build();

        return jwtEncoder.encode(JwtEncoderParameters.from(claims)).getTokenValue();
    }
}
```

### JWT: prós e contras

**Prós:**

- **Stateless** — servidor não armazena sessão
- **Portável** — mesma credential funciona em múltiplos serviços (microserviços)
- **Self-contained** — claims dentro do token, sem query ao DB a cada request
- **Standardizado** — RFC 7519, ecossistema maduro

**Contras:**

- **Revogação difícil** — token válido até expirar (ou você mantém blacklist, o que quebra stateless)
- **Tamanho** — sempre maior que session ID
- **Claims sensíveis** — NÃO coloque dados sensíveis, é apenas base64 (não criptografia)
- **Key management** — rotação de chaves, JWKS endpoint
- **Armadilhas clássicas** — `alg: none`, HS256/RS256 confusion, key confusion

### Boas práticas JWT

1. **Use RS256 ou ES256** (assimétrico) — permite verificação sem compartilhar secret
2. **Valide SEMPRE: iss, aud, exp, nbf**
3. **Nunca confie no `alg` do header** sem validar contra whitelist
4. **Tokens curtos** — 15min a 1h. Use refresh tokens para UX.
5. **Refresh tokens server-side** — permite revogação imediata
6. **JWKS endpoint** — rotação de chaves sem downtime
7. **HTTPS obrigatório** — JWT em cleartext é suicídio
8. **HttpOnly cookies ou Authorization header**, não localStorage (XSS)

### Refresh tokens

Problema: JWT expira rápido (segurança), mas você não quer forçar login a cada hora.

**Solução:** par de tokens:

- **Access token** (JWT curto, 15min) — enviado em toda request
- **Refresh token** (UUID longo, 30 dias) — armazenado server-side, usado para pegar novo access token

```
Login → Access + Refresh

Request API:
  Authorization: Bearer <access_token>

Access expira → client usa refresh token:
  POST /auth/refresh
  { "refresh_token": "..." }
  → novo access + (opcional) novo refresh

Refresh revogado server-side → user precisa logar de novo
```

**Armazenamento:**

- Access token: memória do client (SPA) ou HttpOnly cookie
- Refresh token: HttpOnly Secure SameSite=Strict cookie, ou storage seguro mobile
- Server: tabela `refresh_tokens` com `(token_hash, user_id, expires_at, revoked)`

---

## OAuth2 e OpenID Connect (OIDC)

**OAuth2** — protocolo de **delegação de acesso**. Permite um app acessar recursos de outro em nome do user, sem saber a senha.

**OpenID Connect (OIDC)** — camada de **identidade** sobre OAuth2. Adiciona `id_token` (JWT) que identifica o user.

### OAuth2 Client (login social)

Cenário: "Login com Google/GitHub/Microsoft".

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-oauth2-client</artifactId>
</dependency>
```

```yaml
spring:
  security:
    oauth2:
      client:
        registration:
          google:
            client-id: ${GOOGLE_CLIENT_ID}
            client-secret: ${GOOGLE_CLIENT_SECRET}
            scope: openid, profile, email
          github:
            client-id: ${GITHUB_CLIENT_ID}
            client-secret: ${GITHUB_CLIENT_SECRET}
```

```java
@Bean
public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
    return http
        .authorizeHttpRequests(auth -> auth
            .requestMatchers("/", "/login").permitAll()
            .anyRequest().authenticated()
        )
        .oauth2Login(oauth2 -> oauth2
            .loginPage("/login")
            .defaultSuccessUrl("/dashboard")
        )
        .build();
}

@GetMapping("/me")
public Map<String, Object> me(@AuthenticationPrincipal OidcUser principal) {
    return Map.of(
        "name", principal.getFullName(),
        "email", principal.getEmail(),
        "picture", principal.getPicture()
    );
}
```

### Fluxos OAuth2

**Authorization Code Flow (com PKCE)** — o mais seguro, recomendado para web e mobile apps:

```
1. Client redireciona user para authorization server com PKCE challenge
2. User autentica no authorization server
3. Authorization server redireciona de volta com authorization code
4. Client troca code + PKCE verifier por access token (no backend)
5. Client usa access token para chamar API
```

**Client Credentials Flow** — server-to-server, sem user:

```
Service A → POST /token (client_id + client_secret)
         → access_token
         → GET /api/resource (Authorization: Bearer ...)
```

**Implicit Flow** e **Password Flow** — **deprecated**, não use em código novo.

---

## Autorização

Após autenticar (quem é), autorizar (o que pode fazer).

### Baseado em URL

```java
http.authorizeHttpRequests(auth -> auth
    .requestMatchers("/api/public/**").permitAll()
    .requestMatchers("/api/user/**").hasRole("USER")
    .requestMatchers("/api/admin/**").hasRole("ADMIN")
    .requestMatchers(HttpMethod.GET, "/api/read-only/**").hasAuthority("READ")
    .requestMatchers(HttpMethod.POST, "/api/read-only/**").denyAll()
    .anyRequest().authenticated()
);
```

**`hasRole("ADMIN")`** internamente busca authority `ROLE_ADMIN`. Prefixo `ROLE_` é convenção.

### Method-level security

Anotações no Service ou Controller — mais granular.

```java
@Configuration
@EnableMethodSecurity(prePostEnabled = true, securedEnabled = true)
public class SecurityConfig { }

@Service
public class PatientService {

    @PreAuthorize("hasRole('ADMIN')")
    public void deletePatient(Long id) { ... }

    @PreAuthorize("hasAuthority('PATIENT_READ')")
    public Patient findById(Long id) { ... }

    // Expressões complexas com SpEL
    @PreAuthorize("hasRole('ADMIN') or #patient.ownerId == authentication.principal.id")
    public Patient update(Patient patient) { ... }

    // @PostAuthorize — valida APÓS execução (acesso ao resultado)
    @PostAuthorize("returnObject.ownerId == authentication.principal.id or hasRole('ADMIN')")
    public Patient findPrivate(Long id) { ... }

    // @PreFilter / @PostFilter — filtra coleções
    @PostFilter("filterObject.ownerId == authentication.principal.id")
    public List<Patient> findAll() { ... }
}
```

**SpEL no @PreAuthorize:**

- `hasRole('ADMIN')` / `hasAnyRole('ADMIN', 'USER')`
- `hasAuthority('scope:read')` / `hasAnyAuthority(...)`
- `isAuthenticated()` / `isAnonymous()` / `isFullyAuthenticated()`
- `principal` / `authentication` — acesso ao user atual
- `#paramName` — acesso a parâmetros do método
- `@beanName.method(...)` — chamar método de outro bean

### Authorization customizada com AuthorizationManager

Para lógica complexa que não cabe em expressões, implemente `AuthorizationManager`:

```java
@Component
public class PatientAuthorizationManager implements AuthorizationManager<RequestAuthorizationContext> {

    @Override
    public AuthorizationDecision check(Supplier<Authentication> auth,
                                        RequestAuthorizationContext ctx) {
        HttpServletRequest req = ctx.getRequest();
        String patientId = ctx.getVariables().get("id");
        Authentication authentication = auth.get();

        // Lógica customizada — ex.: verificar se user tem acesso ao tenant do patient
        boolean granted = hasAccessToPatient(authentication, patientId);
        return new AuthorizationDecision(granted);
    }
}

// Uso
http.authorizeHttpRequests(auth -> auth
    .requestMatchers("/api/patients/{id}").access(patientAuthManager)
);
```

### RBAC vs ABAC vs ReBAC

- **RBAC (Role-Based)** — user tem roles, roles têm permissões. Simples, cobre a maioria.
- **ABAC (Attribute-Based)** — decisão baseada em atributos (user, recurso, contexto). Flexível.
- **ReBAC (Relationship-Based)** — Google Zanzibar style. Ideal para "Alice compartilhou X com Bob".

Spring Security suporta bem RBAC e ABAC (via `@PreAuthorize` com SpEL). Para ReBAC, considere ferramentas como **OpenFGA** ou **SpiceDB**.

---

## CSRF (Cross-Site Request Forgery)

Ataque onde um site malicioso faz o browser do user enviar requisições autenticadas ao seu site.

**Exemplo de ataque:**

```html
<!-- site malicioso -->
<img src="https://meubanco.com/transferir?valor=1000&destino=atacante" />
<!-- se o user está logado, cookie vai junto, transfer acontece -->
```

### Quando Spring protege contra CSRF

Por default, **CSRF está ativado** no Spring Security. Cada request "state-changing" (POST, PUT, DELETE, PATCH) exige um token CSRF.

```java
// Spring gera token automaticamente para forms
<form method="post" th:action="@{/salvar}">
    <input type="hidden" name="${_csrf.parameterName}" value="${_csrf.token}"/>
    ...
</form>
```

### Quando desabilitar CSRF

**APIs REST stateless** (com JWT em Authorization header) **não precisam** de CSRF porque:

1. Não usam cookies de sessão
2. Browser não envia Authorization header automaticamente (diferente de cookies)
3. Requer ataque mais sofisticado que tradicional CSRF

```java
// APIs JWT stateless
http.csrf(csrf -> csrf.disable());
```

**Web apps com sessão cookie** **precisam** de CSRF. Não desabilite:

```java
// Web app tradicional — mantenha CSRF
http.csrf(csrf -> csrf
    .csrfTokenRepository(CookieCsrfTokenRepository.withHttpOnlyFalse())
);
```

### CSRF com SPA + cookie session

Se você tem SPA (React, Vue) com session cookie:

```java
http.csrf(csrf -> csrf
    .csrfTokenRepository(CookieCsrfTokenRepository.withHttpOnlyFalse())
    .csrfTokenRequestHandler(new CsrfTokenRequestAttributeHandler())
);
```

SPA lê o cookie `XSRF-TOKEN`, e envia o valor no header `X-XSRF-TOKEN` em toda request mutating.

---

## CORS (Cross-Origin Resource Sharing)

Mecanismo do **browser** que restringe requests de um domínio para outro. Sem CORS configurado no servidor, o browser bloqueia.

```java
@Configuration
public class CorsConfig {

    @Bean
    public CorsConfigurationSource corsConfigurationSource() {
        CorsConfiguration config = new CorsConfiguration();
        config.setAllowedOrigins(List.of("https://app.medespecialista.com"));
        config.setAllowedMethods(List.of("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"));
        config.setAllowedHeaders(List.of("*"));
        config.setExposedHeaders(List.of("X-Total-Count", "Location"));
        config.setAllowCredentials(true);  // cookies / Authorization
        config.setMaxAge(3600L);  // cache preflight 1h

        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/api/**", config);
        return source;
    }
}

@Bean
public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
    return http
        .cors(Customizer.withDefaults())  // usa o bean acima
        // ... outras configurações
        .build();
}
```

**Armadilhas CORS:**

- **`allowedOrigins("*")` + `allowCredentials(true)`** — browsers rejeitam. Liste origens explícitas.
- **CORS NÃO é segurança do servidor** — é do browser. `curl` bypassa completamente. Não confunda com autenticação.
- **Preflight OPTIONS** — para requests "complexos" (headers customizados, content-type não simples), o browser envia OPTIONS antes. Precisa ser permitido.
- **Devolver `*` em `Access-Control-Allow-Origin` sem credentials** — funciona, mas permite qualquer site fazer request.

---

## Session management

### Stateless vs Stateful

**Stateless** (APIs JWT) — servidor não mantém estado do user, tudo vem no token.

```java
http.sessionManagement(sm -> sm.sessionCreationPolicy(SessionCreationPolicy.STATELESS));
```

**Stateful** (web apps) — servidor mantém `HttpSession` com o user autenticado, `JSESSIONID` no cookie.

```java
http.sessionManagement(sm -> sm
    .sessionCreationPolicy(SessionCreationPolicy.IF_REQUIRED)  // default
    .sessionFixation().migrateSession()  // previne session fixation
    .maximumSessions(1)  // um user = 1 sessão ativa
    .maxSessionsPreventsLogin(false)  // nova sessão kicka antiga
);
```

### Session fixation

Ataque onde o atacante fixa o session ID **antes** do login e depois sequestra.

**Proteção:** `sessionFixation().migrateSession()` — após login, Spring cria nova session e copia atributos. **Default em Spring Security.**

### Concurrent sessions

Controlar quantas sessões ativas por user:

```java
http.sessionManagement(sm -> sm
    .maximumSessions(1)
    .maxSessionsPreventsLogin(true)  // bloqueia nova sessão se já há uma
);
```

### Session distribuída (multi-instance)

Em ambiente com múltiplas instâncias, sessões em memória não funcionam. Use **Spring Session**:

```xml
<dependency>
    <groupId>org.springframework.session</groupId>
    <artifactId>spring-session-data-redis</artifactId>
</dependency>
```

```yaml
spring:
  session:
    store-type: redis
  data:
    redis:
      host: localhost
      port: 6379
```

Sessões ficam no Redis, compartilhadas entre instâncias.

---

## Security headers

Spring Security adiciona headers de segurança automaticamente. Você pode customizar:

```java
http.headers(headers -> headers
    .contentSecurityPolicy(csp -> csp
        .policyDirectives("default-src 'self'; script-src 'self' 'unsafe-inline'"))
    .frameOptions(fo -> fo.deny())
    .xssProtection(xss -> xss.headerValue(XXssProtectionHeaderWriter.HeaderValue.ENABLED_MODE_BLOCK))
    .httpStrictTransportSecurity(hsts -> hsts
        .maxAgeInSeconds(31536000)
        .includeSubDomains(true))
    .referrerPolicy(rp -> rp.policy(ReferrerPolicy.STRICT_ORIGIN_WHEN_CROSS_ORIGIN))
);
```

**Headers importantes:**

- **`Strict-Transport-Security`** (HSTS) — força HTTPS
- **`Content-Security-Policy`** (CSP) — previne XSS
- **`X-Frame-Options`** — previne clickjacking
- **`X-Content-Type-Options: nosniff`** — previne MIME sniffing
- **`Referrer-Policy`** — controla info de referrer
- **`Permissions-Policy`** — controla APIs do browser (camera, mic)

---

## Testando Spring Security

### @WithMockUser

```java
@SpringBootTest
@AutoConfigureMockMvc
class PatientControllerTest {

    @Autowired private MockMvc mockMvc;

    @Test
    @WithMockUser(username = "alice", roles = "USER")
    void shouldReturnOkForAuthenticatedUser() throws Exception {
        mockMvc.perform(get("/api/me"))
            .andExpect(status().isOk());
    }

    @Test
    @WithMockUser(roles = "USER")
    void shouldReturnForbiddenForNonAdmin() throws Exception {
        mockMvc.perform(delete("/api/patients/1"))
            .andExpect(status().isForbidden());
    }

    @Test
    void shouldReturnUnauthorizedWithoutAuth() throws Exception {
        mockMvc.perform(get("/api/me"))
            .andExpect(status().isUnauthorized());
    }
}
```

### JWT em testes

```java
@Test
void shouldAcceptValidJwt() throws Exception {
    mockMvc.perform(get("/api/protected")
            .with(jwt().jwt(jwt -> jwt
                .subject("user-42")
                .claim("scope", "read write")
            )))
        .andExpect(status().isOk());
}
```

### Custom UserDetails em testes

```java
@Test
@WithUserDetails(value = "alice@example.com",
                 userDetailsServiceBeanName = "userDetailsService")
void testWithRealUser() { ... }
```

---

## Armadilhas comuns

- **`antMatchers` em Spring Security 6+** — use `requestMatchers`
- **Desabilitar CSRF em web apps com session** — vulnerável a CSRF
- **Manter CSRF habilitado em API stateless com JWT** — quebra clients que não enviam o token
- **Armazenar JWT em localStorage** — vulnerável a XSS
- **`allowedOrigins("*")` + `allowCredentials(true)`** — browsers rejeitam
- **`permitAll()` em endpoints sensíveis por engano** — teste cada endpoint
- **Esquecer `hasRole` vs `hasAuthority`** — `hasRole("ADMIN")` busca `ROLE_ADMIN` automaticamente
- **Password em plain text** — sempre hash com BCrypt/Argon2
- **SQL injection em queries manuais** — use PreparedStatement / JPA parameters
- **Assumir que CORS protege o servidor** — só protege o browser; `curl` bypassa
- **JWT sem validar `aud` e `iss`** — aceita token de qualquer issuer
- **JWT com `alg: none` aceito** — sempre whitelist de algoritmos
- **Tokens JWT muito longos (>24h)** — dificulta revogação
- **`@PreAuthorize` em método privado** — não funciona (AOP via proxy)
- **Esquecer `@EnableMethodSecurity`** — `@PreAuthorize` ignorado silenciosamente
- **`Authentication.getPrincipal()` sem verificar tipo** — `ClassCastException`
- **Trusting `X-Forwarded-For` sem config** — spoofable. Configure `ForwardedHeaderFilter`.
- **Rate limit no nível da app em vez do gateway** — app é vulnerável antes mesmo de avaliar
- **Não monitorar tentativas de login** — brute force passa despercebido
- **Logar credentials** — senhas, tokens, refresh tokens nunca devem ir pro log
- **Erros de auth vazando info** — "user not found" vs "wrong password" é information disclosure
- **Misturar autenticação e autorização** — são coisas diferentes
- **`SecurityContextHolder.clearContext()` esquecido** — pode vazar auth entre requests em thread pool

---

## Na prática (da minha experiência)

> **MedEspecialista — arquitetura de autenticação:**
>
> O sistema tem 3 fluxos de autenticação distintos:
>
> **1. API mobile/web (pacientes e médicos):** JWT stateless via Resource Server. Keycloak como authorization server, Spring Boot como resource server validando JWTs. Tokens curtos (15 min) + refresh tokens (30 dias) server-side. Refresh com rotação a cada uso — token antigo revogado, novo emitido.
>
> **2. Dashboard admin (staff interno):** Login SAML via Active Directory. Spring Security SAML2 + provisioning automático na primeira entrada.
>
> **3. APIs B2B (planos de saúde integrando):** API keys com prefixo (`sk_live_...`), hash SHA256 no banco, rotacionadas semestralmente. Rate limit por key no Kong API Gateway.
>
> **Decisões importantes:**
>
> **1. `@EnableMethodSecurity` + `@PreAuthorize` granular:** autorização baseada em URL (`hasRole("ADMIN")`) é muito grossa. Uso method-level com SpEL — `@PreAuthorize("hasRole('ADMIN') or #patientId == authentication.principal.claim('patient_id')")`. Permite lógica como "médicos só veem seus próprios pacientes".
>
> **2. BCrypt com work factor 12:** default é 10, mas em 2026 12 é mais razoável. Senha leva ~300ms para hash, aceitável para login.
>
> **3. CSRF desabilitado em API stateless:** não tenho session cookie, JWTs vêm em Authorization header. Browser não envia Authorization automaticamente (diferente de cookies), então CSRF clássico não se aplica. Se fosse web app com cookie, manteria habilitado.
>
> **4. CORS com origens explícitas:** `setAllowedOriginPatterns(List.of("https://*.medespecialista.com"))` — subdomínios permitidos, mais nada. Nunca `*` com credentials.
>
> **5. Refresh tokens server-side:** tabela `refresh_tokens` com `(token_hash, user_id, expires_at, revoked, device_info)`. Permite revogação imediata quando user faz logout ou troca senha. Token em si é UUID, não JWT — refresh token JWT dificulta revogação.
>
> **6. Password reset com tokens de uso único:** token gerado, enviado por email, expira em 1h, invalidado após uso. Tabela similar ao refresh_tokens.
>
> **7. Rate limiting em 2 camadas:** Kong API Gateway (global por key/IP) + Spring Boot (específico por endpoint crítico como login). Defense in depth.
>
> **8. Audit log de eventos de segurança:** login sucedido, login falhou, password reset, role change. Tabela `security_events` com retenção de 2 anos. Detecta padrões anômalos.
>
> **Incidente memorável — JWT com `alg: none`:**
> Durante um pentest, descobrimos que uma biblioteca JWT antiga aceitava tokens com `alg: none` (sem assinatura). Atacante podia forjar qualquer token e o backend aceitava. Solução: whitelist explícita de algoritmos (`RS256` só). Lesson learned: nunca aceite `alg` do header sem validar.
>
> **Outro incidente — NPE em SecurityContext:**
> Sob carga alta, virtual threads processando requests paralelos tinham `SecurityContextHolder.getContext().getAuthentication()` retornando null intermitentemente. Causa: race condition com thread locals e async. Solução: passar Authentication explícito em vez de depender do holder em código async. Em Java 25, pretendo migrar para Scoped Values.
>
> **A lição principal:** Spring Security é poderoso mas complexo. 80% dos bugs são de configuração, não de código. Teste sempre auth com mock users, nunca desabilite proteções "temporariamente", audit logs são essenciais para detecção, e assume breach — mesmo com auth perfeita, monitoramento é crucial.

---

## How to explain in English

> "Spring Security handles authentication and authorization in the Spring ecosystem. I use it extensively across different scenarios — JWT resource servers for stateless APIs, OAuth2 clients for social login, and method-level security with `@PreAuthorize` for fine-grained authorization.
>
> The architecture center is the filter chain. Every HTTP request passes through a series of filters before reaching the controller — CSRF, CORS, authentication, authorization. Understanding this pipeline is key because customization happens by adding, removing, or reordering filters.
>
> For APIs, I use JWT with Spring Security's OAuth2 Resource Server. Short-lived access tokens, refresh tokens stored server-side for revocation. I enforce stateless sessions, disable CSRF because there's no session cookie to protect, and validate tokens via a JWKS endpoint with issuer and audience checks. I never trust the `alg` claim — always validate against a whitelist.
>
> For authorization, I prefer method-level `@PreAuthorize` with SpEL expressions over URL-based rules. URL-based is too coarse for real business logic — method-level lets me express things like 'doctors can only see their own patients' directly on the service method.
>
> For passwords, BCrypt with work factor 12 is my default. I use `DelegatingPasswordEncoder` to allow gradual migration if I ever need to move to Argon2.
>
> CSRF protection is enabled for traditional web apps with sessions, and disabled for stateless JWT APIs — the JWT in the Authorization header isn't automatically sent by browsers, so classic CSRF doesn't apply. CORS is configured with explicit allowed origins, never wildcards with credentials.
>
> For testing, `@WithMockUser` and MockMvc's `with(jwt())` let me test security rules without real authentication infrastructure. For integration tests, I run a real Keycloak instance via Testcontainers.
>
> The biggest lessons from production: audit everything security-related, never trust client-provided data for authorization decisions, and remember that CORS is browser-only — it's not server-side security. The backend must still validate every request."

### Frases úteis em entrevista

- "I distinguish clearly between authentication — who you are — and authorization — what you can do."
- "For APIs, JWT with resource server is my default. Short-lived access tokens plus server-side refresh tokens for revocation."
- "I use method-level `@PreAuthorize` for fine-grained authorization — URL-based is too coarse."
- "BCrypt with work factor 12 is my default password encoder. Argon2 if starting fresh today."
- "CSRF is enabled for web apps with sessions, disabled for stateless JWT APIs."
- "I always validate JWT issuer, audience, expiration, and never trust the `alg` claim without a whitelist."
- "Refresh tokens stay server-side so I can revoke them immediately on logout or password change."
- "CORS is browser-only — it's not server-side security. I always enforce auth separately."
- "I use `@WithMockUser` for unit tests and Testcontainers with Keycloak for integration tests."
- "Security events — login failures, role changes — go to a dedicated audit log with long retention."

### Key vocabulary

- autenticação → authentication
- autorização → authorization
- cadeia de filtros → filter chain
- provedor de identidade → identity provider (IdP)
- servidor de recursos → resource server
- servidor de autorização → authorization server
- token de acesso → access token
- token de atualização → refresh token
- escopo → scope
- permissão → authority / permission
- função / papel → role
- sessão → session
- cookie de sessão → session cookie
- falsificação de requisição entre sites → cross-site request forgery (CSRF)
- compartilhamento de recursos entre origens → cross-origin resource sharing (CORS)
- redirecionamento → redirect
- codificador de senha → password encoder
- hash de senha → password hash
- fator de trabalho → work factor (BCrypt)
- chave de API → API key
- controle de acesso baseado em papéis → role-based access control (RBAC)
- controle de acesso baseado em atributos → attribute-based access control (ABAC)
- cabeçalho de segurança → security header
- política de segurança de conteúdo → content security policy (CSP)

---

## Recursos

### Documentação

- [Spring Security Reference](https://docs.spring.io/spring-security/reference/)
- [Spring Security Architecture](https://docs.spring.io/spring-security/reference/servlet/architecture.html)
- [Spring Authorization Server](https://docs.spring.io/spring-authorization-server/reference/)
- [Spring Security 6 Migration Guide](https://docs.spring.io/spring-security/reference/6.0/migration/)

### Livros

- **Spring Security in Action** — Laurențiu Spilcă (2ª ed. para Spring Security 6)
- **OAuth 2 in Action** — Justin Richer, Antonio Sanso
- **Security Engineering** — Ross Anderson (clássico da área)

### Padrões e referências

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [OWASP JWT Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html)
- [OAuth 2.0 (RFC 6749)](https://datatracker.ietf.org/doc/html/rfc6749)
- [OAuth 2.0 Security Best Current Practice (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)
- [OpenID Connect Core](https://openid.net/specs/openid-connect-core-1_0.html)
- [JWT (RFC 7519)](https://datatracker.ietf.org/doc/html/rfc7519)

### Ferramentas

- [Keycloak](https://www.keycloak.org/) — open-source IdP (Red Hat)
- [Auth0](https://auth0.com/) — managed IdP
- [Okta](https://www.okta.com/) — enterprise SSO
- [AWS Cognito](https://aws.amazon.com/cognito/) — managed identity (AWS)
- [jwt.io](https://jwt.io/) — decodificador JWT
- [OWASP ZAP](https://www.zaproxy.org/) — pentest de web apps
- [Testcontainers Keycloak module](https://github.com/dasniko/testcontainers-keycloak)

### Blogs e artigos

- [Baeldung Spring Security](https://www.baeldung.com/security-spring)
- [Spring Security blog](https://spring.io/blog/category/security)
- [Troy Hunt's blog](https://www.troyhunt.com/) — web security
- [Okta Developer Blog — Spring](https://developer.okta.com/blog/?tag=spring-boot)

---

## Veja também

- [[Spring Boot]] — IoC, AOP, Filter Chain context
- [[Spring Data JPA]] — UserDetailsService, auditoria
- [[API Design]] — autenticação em APIs, JWT, webhooks
- [[Java Fundamentals]] — a linguagem
- [[Testes em Java]] — `@WithMockUser`, test slices
- [[Redes e Protocolos]] — HTTPS, TLS, certificados
- [[System Design]] — rate limiting, WAF, defense in depth
- [[Arquitetura de Software]] — Hexagonal, bounded contexts
