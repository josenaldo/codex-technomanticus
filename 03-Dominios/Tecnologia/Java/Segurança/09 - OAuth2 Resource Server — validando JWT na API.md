---
title: "OAuth2 Resource Server — validando JWT na API"
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
  - oauth2
  - jwt
aliases:
  - "OAuth2 Resource Server"
  - "validando JWT"
---

# OAuth2 Resource Server — validando JWT na API

> [!abstract] TL;DR
> Quando a sua API recebe JWTs emitidos por um Identity Provider externo (Keycloak, Auth0, Cognito), o **Resource Server** do Spring Security os valida automaticamente. Você só aponta o `issuer-uri` (ou o `jwk-set-uri`, o endpoint **JWKS**) e o Spring busca as chaves públicas, valida a assinatura, e checa `iss`, `aud` e `exp` em cada requisição. Do JWT válido ele monta o `Authentication` e expõe o token como `@AuthenticationPrincipal Jwt`. Como não há sessão, combine com `SessionCreationPolicy.STATELESS` e CSRF desligado. A sua API é um **consumidor** de tokens — ela não loga ninguém, não guarda senha, não emite token: só verifica.

## O que é

O **OAuth2 Resource Server** é o papel que a sua API exerce no fluxo OAuth2/OIDC: ela protege recursos (endpoints) e exige um **Bearer Token** — um JWT — no header `Authorization`. Quem emite esse token é outro ator, o **Authorization Server** (o IdP). A sua API nunca conversa diretamente com o usuário sobre credenciais; ela apenas recebe o token que o cliente já obteve do IdP e decide se ele é válido e o que ele autoriza.

No Spring Security 6.x (Boot 3.x), todo esse trabalho cabe atrás de uma linha de configuração: `http.oauth2ResourceServer(oauth2 -> oauth2.jwt(...))`. A partir daí o filtro `BearerTokenAuthenticationFilter` extrai o token, um `JwtDecoder` valida assinatura e claims, e um conversor transforma os claims em `GrantedAuthority`.

> [!info] JWT é a nota 08
> Aqui tratamos da **integração que valida** o JWT. A anatomia do token em si — header, payload, assinatura, como ele é assinado e verificado — está em [[03-Dominios/Tecnologia/Java/Segurança/08 - JWT — estrutura, assinatura e validação|JWT]]. Não vamos re-explicar isso.

## Por que importa

É o cenário de segurança mais comum em APIs modernas: microsserviços, SPAs e apps móveis que delegam a autenticação a um IdP centralizado. Em vez de cada serviço implementar login, hash de senha e gestão de sessão, todos viram **Resource Servers** que confiam num emissor comum. Isso é o que torna SSO (single sign-on) e arquiteturas distribuídas viáveis.

Para uma entrevista sênior, é o ponto onde se separa quem decorou "Spring Security tem login" de quem entende o modelo: a API stateless não tem sessão, valida o token por requisição via chave pública (sem chamar o IdP a cada request, graças ao cache do JWKS), e a rotação de chave do IdP não derruba a sua API — o JWKS expõe múltiplas chaves e o Spring busca a certa pelo `kid` do header. Saber configurar o conversor de authorities é o que faz `hasRole`/`hasAuthority` realmente funcionar.

## Como funciona

### O cenário: sua API valida JWTs emitidos por um IdP (Keycloak/Auth0/Cognito)

O fluxo, do ponto de vista da sua API, é simples porque a parte difícil acontece fora dela:

1. O cliente (SPA, app, outro serviço) se autentica no **IdP** e recebe um `access_token` JWT.
2. O cliente chama a sua API com `Authorization: Bearer <jwt>`.
3. A sua API (Resource Server) valida o token e responde — ou rejeita com `401`/`403`.

A sua API **não** redireciona para tela de login, **não** guarda senha, **não** mantém sessão. Ela é puramente um verificador. As chaves para verificar a assinatura vêm do IdP via o endpoint **JWKS**.

São necessárias duas dependências (o Boot starter agrega ambas):

```xml
<dependency>
    <groupId>org.springframework.security</groupId>
    <artifactId>spring-security-oauth2-resource-server</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.security</groupId>
    <artifactId>spring-security-oauth2-jose</artifactId>
</dependency>
```

Na prática, com Spring Boot você adiciona o starter `spring-boot-starter-oauth2-resource-server`, que traz as duas (`oauth2-resource-server` para o suporte geral e `oauth2-jose` para decodificar/verificar JWTs).

### Config: issuer-uri / jwk-set-uri (JWKS — rotação de chave sem downtime)

Há dois jeitos de dizer ao Spring onde estão as chaves públicas:

- **`issuer-uri`** — o caminho mais limpo. Você informa o emissor (o valor do claim `iss`) e o Spring faz **discovery**: bate no endpoint `.well-known/openid-configuration` do IdP, descobre o `jwks_uri`, e se auto-configura. Bônus: ele passa a validar o `iss` automaticamente.

```yaml
spring:
  security:
    oauth2:
      resourceserver:
        jwt:
          issuer-uri: https://auth.example.com
```

- **`jwk-set-uri`** — quando o IdP não expõe o endpoint de discovery, você aponta direto o **JWKS** (JSON Web Key Set), a URL que retorna o conjunto de chaves públicas em JSON:

```yaml
spring:
  security:
    oauth2:
      resourceserver:
        jwt:
          issuer-uri: https://auth.example.com
          jwk-set-uri: https://auth.example.com/.well-known/jwks.json
```

O **JWKS** é a peça que torna a operação resiliente. É um documento com **várias** chaves, cada uma com um `kid` (key id). O header de cada JWT carrega o `kid` da chave que o assinou. Quando o IdP **rotaciona** a chave de assinatura, ele publica a nova chave no JWKS **antes** de começar a usá-la e mantém a antiga até os tokens emitidos com ela expirarem. A sua API, que faz cache do JWKS e o re-busca ao ver um `kid` desconhecido, troca de chave **sem downtime** e sem deploy. É por isso que apontar para o JWKS (em vez de colar uma chave pública estática) é a prática correta.

### JwtAuthenticationConverter: claim scope/roles → GrantedAuthority

Validar a assinatura diz que o token é autêntico; ainda falta traduzir o que ele **autoriza**. Quem faz isso é o `JwtAuthenticationConverter`, apoiado no `JwtGrantedAuthoritiesConverter`.

Por padrão, o Spring lê o claim **`scope`** (ou `scp`) e prefixa cada valor com `SCOPE_`:

```
claim:        { "scope": "order:read order:write" }
authorities:  [ SCOPE_order:read, SCOPE_order:write ]
```

Isso casa com `.access(hasScope("order:read"))` ou `hasAuthority("SCOPE_order:read")`. Mas muitos IdPs (Keycloak, por exemplo) emitem papéis num claim **`roles`**. Para que `hasRole("ADMIN")` funcione, você precisa de duas coisas: ler o claim certo (`setAuthoritiesClaimName("roles")`) e usar o prefixo que o Spring espera para roles (`setAuthorityPrefix("ROLE_")`, já que `hasRole("ADMIN")` procura a authority `ROLE_ADMIN`).

```java
JwtGrantedAuthoritiesConverter authorities = new JwtGrantedAuthoritiesConverter();
authorities.setAuthoritiesClaimName("roles");
authorities.setAuthorityPrefix("ROLE_");
```

Para remover o prefixo de vez: `setAuthorityPrefix("")`. E para ler **scopes e roles ao mesmo tempo**, há o `DelegatingJwtGrantedAuthoritiesConverter`, que combina vários conversores.

### Stateless: SessionCreationPolicy.STATELESS + CSRF off

JWT é **autocontido**: tudo o que a API precisa para autorizar está no próprio token, validado a cada requisição. Não existe estado de sessão no servidor. Logo, você desliga a criação de sessão:

```java
.sessionManagement(sm -> sm.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
```

E como a defesa contra CSRF do Spring se baseia em sessão + cookie, ela é inútil (e atrapalha) numa API que se autentica por header `Authorization: Bearer`. O ataque CSRF explora credenciais enviadas **automaticamente** pelo browser (cookies); um Bearer token vai num header que o atacante não consegue forjar via formulário cross-site. Por isso, em API JWT stateless, CSRF se desliga. O porquê detalhado está em [[03-Dominios/Tecnologia/Java/Segurança/10 - CSRF — por que ligado por default e quando desligar|CSRF]].

### Acessando o token: @AuthenticationPrincipal Jwt

Depois da validação, o `Authentication#getPrincipal` é, por padrão, um objeto `Jwt`. No controller você o injeta direto:

```java
@GetMapping("/me")
public Map<String, Object> me(@AuthenticationPrincipal Jwt jwt) {
    return Map.of(
        "subject", jwt.getSubject(),                       // o claim "sub"
        "roles",   jwt.getClaimAsStringList("roles"),
        "expira",  jwt.getExpiresAt()
    );
}
```

`jwt.getSubject()` devolve o claim `sub`; `getClaimAsStringList`, `getClaimAsString`, `getClaimAsMap` leem qualquer claim com tipagem. Para o ID do usuário, prefira o `sub` (estável) a `email` ou `username` (mutáveis).

## Na prática

`application.yml` — apontar para o emissor neutro:

```yaml
spring:
  security:
    oauth2:
      resourceserver:
        jwt:
          issuer-uri: https://auth.example.com
          # audiences: https://api.example.com   # valida o claim "aud" (ver Armadilha 2)
```

Configuração de segurança completa, statelss e com conversor de roles:

```java
@Configuration
@EnableWebSecurity
public class ResourceServerConfig {

    @Bean
    SecurityFilterChain filterChain(HttpSecurity http,
                                    JwtAuthenticationConverter conv) throws Exception {
        http
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/orders/**").hasRole("USER")
                .anyRequest().authenticated()
            )
            .oauth2ResourceServer(o -> o
                .jwt(j -> j.jwtAuthenticationConverter(conv))
            )
            .sessionManagement(sm -> sm
                .sessionCreationPolicy(SessionCreationPolicy.STATELESS)
            )
            .csrf(c -> c.disable());
        return http.build();
    }

    @Bean
    JwtAuthenticationConverter jwtAuthenticationConverter() {
        JwtGrantedAuthoritiesConverter authorities = new JwtGrantedAuthoritiesConverter();
        authorities.setAuthoritiesClaimName("roles");  // IdP emite papéis em "roles"
        authorities.setAuthorityPrefix("ROLE_");        // hasRole("USER") -> ROLE_USER

        JwtAuthenticationConverter converter = new JwtAuthenticationConverter();
        converter.setJwtGrantedAuthoritiesConverter(authorities);
        return converter;
    }
}
```

Controller lendo o token autenticado:

```java
@RestController
public class ProfileController {

    @GetMapping("/me")
    public Map<String, Object> me(@AuthenticationPrincipal Jwt jwt) {
        return Map.of(
            "userId", jwt.getSubject(),
            "roles",  jwt.getClaimAsStringList("roles")
        );
    }
}
```

## Armadilhas

### (1) CSRF habilitado numa API stateless

O Spring Security liga a proteção CSRF por padrão. Numa API JWT, isso quebra todo cliente que não envia o token CSRF (toda chamada não-`GET` falha com `403`):

```java
// requisição POST /orders com Bearer válido -> 403 Forbidden
// porque falta o header/token CSRF que o browser injetaria via sessão
```

**Fix:** numa API stateless autenticada por Bearer token, desligue CSRF — `.csrf(c -> c.disable())`. A defesa CSRF protege fluxos baseados em cookie de sessão, que aqui não existem. (Detalhes em [[03-Dominios/Tecnologia/Java/Segurança/10 - CSRF — por que ligado por default e quando desligar|CSRF]].)

### (2) Não configurar issuer-uri/audience

Se você aponta só o `jwk-set-uri` sem `issuer-uri`, o Spring valida a **assinatura**, mas não o **emissor** — ele aceita qualquer JWT assinado com aquela chave, mesmo de outro contexto. Pior, sem validar `aud` (audience), um token legítimo emitido para **outra** API do mesmo IdP é aceito pela sua:

```yaml
# FRÁGIL: valida assinatura, mas não checa "iss" nem "aud"
spring.security.oauth2.resourceserver.jwt.jwk-set-uri: https://auth.example.com/.well-known/jwks.json
```

**Fix:** prefira `issuer-uri` (ele valida o `iss` automaticamente) e, quando o IdP serve várias APIs, adicione `audiences` para garantir que o token foi emitido **para você**:

```yaml
spring:
  security:
    oauth2:
      resourceserver:
        jwt:
          issuer-uri: https://auth.example.com
          audiences: https://api.example.com
```

### (3) Esquecer o JwtAuthenticationConverter

Se o seu IdP coloca os papéis num claim `roles` mas você usa o conversor padrão (que só lê `scope` e prefixa com `SCOPE_`), as authorities de role ficam **vazias**. O token é válido, o usuário autentica, mas `hasRole("ADMIN")` **falha silenciosamente** com `403` — sem erro de assinatura, sem log óbvio:

```java
// token tem { "roles": ["ADMIN"] }, mas o conversor default só olha "scope"
.requestMatchers("/admin/**").hasRole("ADMIN")   // sempre 403
```

**Fix:** registre um `@Bean JwtAuthenticationConverter` configurando `setAuthoritiesClaimName("roles")` e `setAuthorityPrefix("ROLE_")` (ou `DelegatingJwtGrantedAuthoritiesConverter` para ler scopes e roles juntos).

## Em entrevista

### Frase pronta (inglês)

> "When my API acts as an OAuth2 Resource Server, it doesn't handle login — it just validates the JWTs that an external identity provider issues. I point Spring Security at the `issuer-uri`, and it discovers the JWKS endpoint, fetches the public keys, and validates each token's signature, issuer, audience, and expiry on every request. Because there's no session, I make the chain stateless and disable CSRF, and I plug in a `JwtAuthenticationConverter` so the `roles` claim maps to `ROLE_` authorities instead of the default `SCOPE_` prefix. Relying on the JWKS endpoint also means the IdP can rotate its signing key with no downtime on my side."

### Vocabulário

| Termo | Significado |
| --- | --- |
| Resource Server | Papel da API que protege recursos e exige um Bearer token (JWT). |
| Identity Provider (IdP) | Quem autentica o usuário e emite o token (Keycloak, Auth0, Cognito). |
| JWKS (JSON Web Key Set) | Endpoint que publica as chaves públicas usadas para validar a assinatura do JWT. |
| `issuer-uri` | URL do emissor; habilita discovery automático e valida o claim `iss`. |
| Audience (`aud`) | Claim que diz para qual API o token foi emitido; deve ser validado. |
| `JwtAuthenticationConverter` | Componente que mapeia claims (`scope`/`roles`) para `GrantedAuthority`. |
| Stateless | Sem sessão no servidor; cada requisição é autorizada só pelo token. |

## Veja também

- [[03-Dominios/Tecnologia/Java/Segurança/08 - JWT — estrutura, assinatura e validação|JWT]]
- [[03-Dominios/Tecnologia/Java/Segurança/10 - CSRF — por que ligado por default e quando desligar|CSRF]]
- [[03-Dominios/Tecnologia/Java/Segurança/12 - OAuth2 e OIDC Client e os grant types|OAuth2 e OIDC Client]]
- [[03-Dominios/Tecnologia/Java/Segurança/index|Segurança (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java]] (verbetes OAuth2 Resource Server / JWKS / JwtAuthenticationConverter)

## Referências

- Spring Security Reference — OAuth 2.0 Resource Server JWT: https://docs.spring.io/spring-security/reference/servlet/oauth2/resource-server/jwt.html
