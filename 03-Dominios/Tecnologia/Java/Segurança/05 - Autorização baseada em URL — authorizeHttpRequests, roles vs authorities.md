---
title: "Autorização baseada em URL — authorizeHttpRequests, roles vs authorities"
created: 2026-06-10
updated: 2026-06-10
type: concept
progress: backlog
status: seedling
publish: true
fase: iniciado
tags:
  - java
  - seguranca
  - iniciado
  - autorizacao
  - rbac
aliases:
  - "Autorização baseada em URL"
  - "authorizeHttpRequests"
---

# Autorização baseada em URL — authorizeHttpRequests, roles vs authorities

> [!abstract] TL;DR
> Autenticação responde "quem é você?"; **autorização** responde "o que você pode acessar?". Depois que o usuário já está autenticado, a autorização baseada em URL decide quais requests ele pode tocar. O método atual é **`authorizeHttpRequests`** (que substituiu o `authorizeRequests`, hoje legado): você casa requests com **`requestMatchers`** e amarra cada padrão a uma regra — `permitAll()`, `authenticated()`, `hasRole(...)`, `hasAuthority(...)`, `denyAll()`. Detalhe que pega todo mundo: **`hasRole("ADMIN")` busca a authority `ROLE_ADMIN`** — o prefixo `ROLE_` é convenção e o Security adiciona sozinho, então **nunca** repita o prefixo. A ordem dos matchers importa: do mais específico para o mais genérico, com `anyRequest()` por último.

## O que é

Autorização baseada em URL é a camada que, request a request, decide se o usuário **autenticado** tem permissão para chegar ao endpoint. Ela roda no `AuthorizationFilter` (no Security 6.x), bem dentro do filter chain, e funciona como uma lista de pares "padrão de URL → regra de acesso".

Você descreve essa lista dentro de um `@Bean SecurityFilterChain`, usando o DSL do `HttpSecurity`:

- **`authorizeHttpRequests(...)`** abre o bloco de autorização por URL.
- **`requestMatchers(...)`** descreve quais requests aquela regra cobre (por path, por `HttpMethod`, ou ambos).
- Métodos como **`permitAll()`**, **`authenticated()`**, **`hasRole(...)`**, **`hasAnyRole(...)`**, **`hasAuthority(...)`** e **`denyAll()`** dizem o que é exigido para passar.

O `AuthorizationFilter` percorre a lista **na ordem em que você declarou** e aplica **a primeira regra que casar** com o request — por isso a ordem é parte da semântica, não detalhe estético.

> [!info] Roles vs authorities em uma frase
> Uma **authority** é qualquer permissão granular (`orders:read`, `db`). Uma **role** é só uma authority com o prefixo convencional `ROLE_` (`ROLE_ADMIN`). `hasRole("ADMIN")` é açúcar para "tem a authority `ROLE_ADMIN`".

## Por que importa

Sem essa camada, qualquer usuário autenticado acessaria qualquer endpoint — autenticação sozinha não separa um `Customer` comum de um administrador. A autorização por URL é a primeira linha de defesa, declarativa e centralizada, e cobre casos clássicos:

- Endpoints públicos (login, healthcheck, página "sobre") liberados com `permitAll()`.
- Áreas administrativas restritas a quem tem `ROLE_ADMIN`.
- **Endpoints de gestão (Actuator) protegidos** para não vazar métricas, configs e beans para qualquer um.
- Regras por método HTTP: ler é mais liberal, escrever exige mais privilégio.

É também o ponto onde mais se erra em entrevista e em produção: confundir role com authority, duplicar o prefixo `ROLE_`, ou ordenar os matchers de forma que uma regra genérica "engole" uma específica.

## Como funciona

### authorizeHttpRequests + requestMatchers (o que substituiu authorizeRequests/antMatchers)

No Spring Security 6.x / Spring Boot 3.x, o DSL canônico é **`authorizeHttpRequests`**, que liga o `AuthorizationFilter`. Ele **substituiu** o antigo `authorizeRequests` (que usava o `FilterSecurityInterceptor` e hoje está deprecated/removido).

Dentro dele, os padrões de URL são descritos por **`requestMatchers(...)`**, que **substituiu** `antMatchers` e `mvcMatchers`. Um único `requestMatchers` cobre ambos os mundos: você passa o path (`/api/admin/**`) ou um `HttpMethod` mais o path.

```java
http.authorizeHttpRequests(auth -> auth
    .requestMatchers("/api/public/**").permitAll()
    .anyRequest().authenticated());
```

Cada linha é um par "matcher → regra". O filtro avalia de cima para baixo e para na primeira que bater.

### hasRole vs hasAuthority: o prefixo ROLE_ e quando usar cada

Esta é a distinção que mais cai:

- **`hasAuthority("orders:read")`** exige a authority **exatamente** como escrita. Nada é adicionado.
- **`hasRole("ADMIN")`** exige a authority **`ROLE_ADMIN`**. O Security **adiciona o prefixo `ROLE_` automaticamente** — por isso você passa só `"ADMIN"`.

Ou seja, `hasRole("ADMIN")` é equivalente a `hasAuthority("ROLE_ADMIN")`. São duas formas de exigir a mesma authority; `hasRole` é o atalho que assume a convenção `ROLE_`.

> [!tip] Regra prática
> Use **`hasRole`** para papéis amplos (ADMIN, USER, MANAGER) e **`hasAuthority`** para permissões granulares (`orders:read`, `orders:write`). E **nunca** escreva o prefixo dentro de `hasRole` — ele já está implícito.

### RBAC básico: roles → acesso

RBAC (Role-Based Access Control) é o modelo onde o acesso é decidido pela **role** do usuário, não pela identidade individual. O fluxo é:

1. O usuário se autentica e recebe um conjunto de authorities (ex.: `ROLE_USER`, `ROLE_ADMIN`).
2. Cada endpoint declara qual role/authority exige.
3. O `AuthorizationFilter` cruza as authorities do usuário com a exigência da rota.

Em termos de domínio: um `Customer` carrega `ROLE_USER` e enxerga seus próprios `Order`s; um operador carrega `ROLE_ADMIN` e acessa `/api/admin/**`. As authorities vêm do `UserDetails` (ver as notas de autenticação do galho). A autorização por URL é o lado consumidor desse RBAC.

> [!info] Granularidade
> RBAC por URL cobre o "quadro geral" (quem entra onde). Para regras mais finas — "só o dono daquele `Order`" — entra a [[03-Dominios/Tecnologia/Java/Segurança/07 - Method security — @PreAuthorize, @PostAuthorize e SpEL|method security]] e a [[03-Dominios/Tecnologia/Java/Segurança/14 - Autorização avançada — AuthorizationManager, RBAC vs ABAC|autorização avançada]].

### Ordem dos matchers e matcher por HttpMethod

O `AuthorizationFilter` aplica **a primeira regra que casar**. Logo, declare os matchers **do mais específico para o mais genérico**, e deixe **`anyRequest()` por último** como rede de segurança (`.anyRequest().authenticated()` ou `.anyRequest().denyAll()`).

Se você colocar um matcher genérico antes de um específico, o específico **nunca é alcançado** — a regra genérica casa primeiro.

Você também pode restringir por método HTTP passando um `HttpMethod`:

```java
.requestMatchers(HttpMethod.GET, "/api/orders/**").hasAuthority("orders:read")
.requestMatchers(HttpMethod.POST, "/api/orders/**").hasAuthority("orders:write")
```

Assim, `GET` (leitura) e `POST` (escrita) no mesmo path exigem authorities diferentes — um padrão comum de separar leitura de mutação.

## Na prática

Um `SecurityFilterChain` típico amarrando tudo: público liberado, área admin e Actuator restritos a `ROLE_ADMIN`, leitura de pedidos por authority granular, e o resto exigindo autenticação.

```java
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpMethod;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.web.SecurityFilterChain;

@Configuration
public class SecurityConfig {

    @Bean
    SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http
            .authorizeHttpRequests(auth -> auth
                // 1. público: liberado para todos
                .requestMatchers("/api/public/**").permitAll()
                // 2. área administrativa: exige a authority ROLE_ADMIN
                .requestMatchers("/api/admin/**").hasRole("ADMIN")
                // 3. endpoints de gestão (Actuator) também só para admin
                .requestMatchers("/actuator/**").hasRole("ADMIN")
                // 4. leitura de pedidos: authority granular por método
                .requestMatchers(HttpMethod.GET, "/api/orders/**").hasAuthority("orders:read")
                // 5. rede de segurança: tudo o mais exige usuário autenticado
                .anyRequest().authenticated())
            .httpBasic(withDefaults -> {});
        return http.build();
    }
}
```

Pontos a notar:

- **`/actuator/**` está protegido com `hasRole("ADMIN")`** — sem isso, métricas, env e beans ficariam expostos. Combine com a configuração de exposição do [[03-Dominios/Tecnologia/Java/Spring Core e Boot/17 - Actuator e observabilidade|Actuator]].
- `hasRole("ADMIN")` busca `ROLE_ADMIN` (sem repetir o prefixo).
- `hasAuthority("orders:read")` exige a authority literal — útil para permissões finas.
- A ordem vai do específico (`/api/public/**`, `/api/admin/**`) ao genérico (`anyRequest()`).

## Armadilhas

### (1) Usar `antMatchers`/`authorizeRequests` legados

`authorizeRequests`, `antMatchers` e `mvcMatchers` foram **substituídos** no Security 6.x (o `authorizeRequests` está deprecated/removido junto com o `FilterSecurityInterceptor`). Código copiado de tutoriais antigos simplesmente não compila ou não tem o comportamento esperado.

```java
// ERRADO (API legada do Security 5.x)
http.authorizeRequests(auth -> auth
    .antMatchers("/api/admin/**").hasRole("ADMIN"));
```

**Fix:** use o DSL atual.

```java
// CERTO (Security 6.x)
http.authorizeHttpRequests(auth -> auth
    .requestMatchers("/api/admin/**").hasRole("ADMIN"));
```

### (2) Duplicar o prefixo `ROLE_` em `hasRole`

`hasRole` **já adiciona** `ROLE_`. Se você escrever `hasRole("ROLE_ADMIN")`, o Security passa a procurar a authority `ROLE_ROLE_ADMIN`, que ninguém tem — e todo mundo recebe 403.

```java
// ERRADO: vira ROLE_ROLE_ADMIN
.requestMatchers("/api/admin/**").hasRole("ROLE_ADMIN")
```

**Fix:** passe só o nome da role; se precisar mesmo da authority com prefixo, use `hasAuthority`.

```java
// CERTO
.requestMatchers("/api/admin/**").hasRole("ADMIN")
// ou, explicitamente:
.requestMatchers("/api/admin/**").hasAuthority("ROLE_ADMIN")
```

### (3) Ordem errada dos matchers

Como vale a **primeira regra que casa**, um matcher genérico colocado antes de um específico "engole" o específico, que nunca é avaliado.

```java
// ERRADO: anyRequest casa /api/admin/** antes da regra de ADMIN
.anyRequest().authenticated()
.requestMatchers("/api/admin/**").hasRole("ADMIN") // inalcançável
```

**Fix:** do mais específico para o mais genérico, com `anyRequest()` por último.

```java
// CERTO
.requestMatchers("/api/admin/**").hasRole("ADMIN")
.anyRequest().authenticated()
```

### (4) `permitAll()` num endpoint sensível por engano

Um `requestMatchers("/api/**").permitAll()` colocado para "destravar testes" e esquecido em produção libera a API inteira. Pior: por casar cedo e ser genérico, ele ainda anula regras mais restritivas que viessem depois.

```java
// ERRADO: libera tudo sob /api, inclusive /api/admin
.requestMatchers("/api/**").permitAll()
```

**Fix:** seja cirúrgico no `permitAll()` (apenas paths realmente públicos) e mantenha o default fechado com `anyRequest().authenticated()` ou `denyAll()`.

```java
// CERTO
.requestMatchers("/api/public/**").permitAll()
.anyRequest().authenticated()
```

## Em entrevista

### Frase pronta (inglês)

> In Spring Security 6, I configure URL-based authorization with `authorizeHttpRequests`, which replaced the old `authorizeRequests`, and I match requests using `requestMatchers` instead of the deprecated `antMatchers`. Each matcher is bound to a rule such as `permitAll`, `authenticated`, `hasRole`, or `hasAuthority`, and the `AuthorizationFilter` applies the first matcher that matches, so I always order them from most specific to most generic with `anyRequest` last. One detail I'm careful about is that `hasRole("ADMIN")` actually checks for the authority `ROLE_ADMIN` — the `ROLE_` prefix is a convention added automatically, so I never repeat it. For coarse, role-based access I use `hasRole`, and for fine-grained permissions like `orders:read` I use `hasAuthority`.

### Vocabulário

| Termo (EN) | Tradução / sentido |
| --- | --- |
| URL-based authorization | autorização baseada em URL |
| request matcher | casador de requisição (`requestMatchers`) |
| role | papel (authority com prefixo `ROLE_`) |
| authority | permissão granular |
| `ROLE_` prefix convention | convenção do prefixo `ROLE_` |
| coarse-grained access | acesso de granularidade grossa (por role) |
| fine-grained permission | permissão de granularidade fina |
| catch-all rule | regra "pega-tudo" (`anyRequest()`) |
| filter chain | cadeia de filtros |

## Veja também

- [[03-Dominios/Tecnologia/Java/Segurança/01 - O que é Spring Security — authn, authz e o filter chain|O que é Spring Security]]
- [[03-Dominios/Tecnologia/Java/Segurança/07 - Method security — @PreAuthorize, @PostAuthorize e SpEL|Method security]]
- [[03-Dominios/Tecnologia/Java/Segurança/14 - Autorização avançada — AuthorizationManager, RBAC vs ABAC|Autorização avançada]]
- [[03-Dominios/Tecnologia/Java/Spring Core e Boot/17 - Actuator e observabilidade|Actuator e observabilidade]] (proteger os endpoints)
- [[03-Dominios/Tecnologia/Java/Segurança/index|Segurança (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java]] (verbetes authorizeHttpRequests / hasRole vs hasAuthority / RBAC)

## Referências

- Spring Security Reference — Authorize HttpServletRequests: https://docs.spring.io/spring-security/reference/servlet/authorization/authorize-http-requests.html
