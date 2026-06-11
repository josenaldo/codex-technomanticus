---
title: "Session management e security headers"
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
  - session
aliases:
  - "session management"
  - "security headers"
  - "session fixation"
---

# Session management e security headers

> [!abstract] TL;DR
> Uma API JWT é **stateless** (`SessionCreationPolicy.STATELESS`) — não cria `HttpSession`, escala horizontalmente sem esforço. Um web app é **stateful** (`JSESSIONID`) e precisa de proteção contra **session fixation** (default: `migrateSession`/`changeSessionId` — a sessão muda de identidade após o login). Além disso, o Spring adiciona **security headers** por default (HSTS, `X-Frame-Options`, nosniff, `Cache-Control`) e oferece **CSP** opt-in — defendendo contra XSS e clickjacking sem você escrever um byte de filtro.

## O que é

Há duas decisões de segurança que andam juntas mas resolvem problemas diferentes.

A primeira é **gerenciamento de sessão**: o Spring Security precisa decidir se mantém estado entre requisições. Numa API REST autenticada por token, cada request carrega tudo que precisa (o JWT no header) — não há sessão. Num web app tradicional com formulário de login, o servidor guarda o usuário autenticado numa `HttpSession`, identificada por um cookie `JSESSIONID`. Essa escolha é controlada por `SessionCreationPolicy`.

A segunda é a emissão de **HTTP response headers** de segurança: instruções que o servidor manda ao navegador dizendo "force HTTPS", "não me embuta num iframe", "não adivinhe o MIME type", "só execute scripts da minha própria origem". São defesas declarativas que vivem na resposta HTTP, não no código de negócio.

## Por que importa

Errar a política de sessão tem custo direto de escala e segurança. Uma API que cria `HttpSession` sem necessidade vira **stateful**: cada instância guarda sessões em memória, e um load balancer precisa de sticky sessions ou de uma store distribuída só pra não deslogar o usuário a cada request. Pior, sessão herdada antes do login abre brecha de **session fixation** — um atacante planta um `JSESSIONID` conhecido na vítima e, se a sessão não mudar de identidade no login, herda a sessão autenticada.

Já os security headers são a camada barata que para classes inteiras de ataque no navegador: **clickjacking** (sua página embutida num iframe malicioso), **XSS** (injeção de script), **MIME sniffing** (o browser tratando um upload como HTML executável) e downgrade pra HTTP. O Spring liga os principais por default — mas o CSP, que é o mais forte contra XSS, é opt-in e fácil de esquecer.

## Como funciona

### STATELESS (JWT) vs stateful (HttpSession / JSESSIONID)

`SessionCreationPolicy` tem quatro valores:

| Política | Comportamento |
| --- | --- |
| `STATELESS` | Nunca cria nem usa `HttpSession`. Usa `NullSecurityContextRepository` e desliga o cache de requests na sessão. É o modo de API JWT. |
| `IF_REQUIRED` | **Default**. Cria sessão só quando algo precisa (ex.: guardar o `SecurityContext` após login form). |
| `ALWAYS` | Cria sessão eagerly pra todo request, mesmo sem necessidade. |
| `NEVER` | Não cria sessão, mas usa uma existente se já houver. |

> [!info] Detalhe do `NEVER`
> Mesmo com `NEVER`, você pode ver o app criando `HttpSession` — o request cache do Spring ainda usa sessão. `STATELESS` é a garantia real de "zero sessão".

Numa API stateless, o JWT carrega a autenticação (ver a nota linkada sobre Resource Server) e não há `JSESSIONID`. Num web app stateful, o `JSESSIONID` é o ponteiro pra sessão server-side.

### Session fixation: migrateSession (default — nova sessão após login)

Session fixation é o ataque em que o agressor força a vítima a usar um identificador de sessão que ele já conhece, e então "herda" a sessão depois que ela autentica. A defesa: **trocar a identidade da sessão no momento do login**.

O Spring Security faz isso por default. O comportamento exato depende do container:

- **Servlet 3.1+** (a baseline do Boot 3.x / Security 6.x): `changeSessionId()` — pede ao container pra trocar o ID da sessão nativamente, sem recriar nada.
- **Servlet 3.0 ou anterior**: `migrateSession()` — cria uma sessão nova e copia os atributos da antiga.

Em ambos, o ponto é o mesmo: o ID que o atacante plantou deixa de valer após o login. Você pode forçar `migrateSession()` explicitamente, ou usar `newSession()` (sessão limpa, sem copiar atributos pré-login).

### Concurrent sessions: maximumSessions

Você pode limitar quantas sessões simultâneas um mesmo usuário mantém com `maximumSessions(int)`:

```java
.sessionManagement(sm -> sm
    .maximumSessions(1)
)
```

Por default, abrir uma nova sessão **expira a mais antiga** (estilo "te deslogou no outro dispositivo"). Pra inverter — barrar o novo login em vez de matar o antigo — use `maxSessionsPreventsLogin(true)`. O controle de concorrência exige registrar um bean `HttpSessionEventPublisher`, senão o Spring não sabe quando uma sessão é destruída.

### Sessão distribuída: Spring Session/Redis (multi-instância — menção)

Quando você roda múltiplas instâncias atrás de um load balancer e quer manter `HttpSession`, guardar a sessão em memória local não escala (sticky sessions são frágeis). A solução canônica é **Spring Session** com uma store externa — tipicamente **Redis**: a sessão vira uma entrada num data store compartilhado, e qualquer instância resolve o `JSESSIONID` lendo do Redis. A configuração detalhada vive na documentação do Spring Session; aqui basta saber que é assim que se faz sessão stateful **horizontalmente escalável**. (Numa API JWT stateless, esse problema simplesmente não existe — não há sessão pra distribuir.)

### Security headers: HSTS, CSP (anti-XSS), X-Frame-Options (anti-clickjacking), nosniff, Referrer-Policy

O Spring Security é **secure-by-default**: adiciona automaticamente, a toda resposta, um conjunto de headers.

Habilitados por default:

| Header | Defende contra | Efeito |
| --- | --- | --- |
| `Strict-Transport-Security` (HSTS) | downgrade pra HTTP / man-in-the-middle | Browser força HTTPS no domínio por `max-age` segundos. |
| `X-Frame-Options: DENY` | clickjacking | Proíbe embutir a página em iframe (customizável pra `SAMEORIGIN`). |
| `X-Content-Type-Options: nosniff` | MIME sniffing | Browser não "adivinha" content type. |
| `Cache-Control` | vazamento de resposta sensível em cache | Marca respostas como não-cacheáveis. |

Opt-in (você precisa configurar):

| Header | Defende contra | Nota |
| --- | --- | --- |
| `Content-Security-Policy` (CSP) | XSS | A defesa mais forte contra script injection: declara quais origens podem carregar scripts/styles/etc. |
| `Referrer-Policy` | vazamento de URL no header `Referer` | Controla quanto da URL de origem é enviado. |
| `Permissions-Policy` | abuso de APIs do browser (câmera, geo) | Substitui o antigo `Feature-Policy`. |

Os métodos do DSL são, respectivamente, `httpStrictTransportSecurity(...)`, `contentSecurityPolicy(...)`, `frameOptions(...)`, `contentTypeOptions(...)`, `cacheControl(...)`, `referrerPolicy(...)` e `permissionsPolicy(...)`, todos dentro de `http.headers(...)`. Sob o capô, quem escreve esses headers é o `HeaderWriterFilter` — ver a nota do filter chain linkada abaixo.

## Na prática

API REST autenticada por JWT — stateless, sem sessão:

```java
import static org.springframework.security.config.http.SessionCreationPolicy.STATELESS;

@Bean
SecurityFilterChain apiChain(HttpSecurity http) throws Exception {
    http
        .sessionManagement(sm -> sm.sessionCreationPolicy(STATELESS))
        // ... oauth2ResourceServer(...) etc.
        ;
    return http.build();
}
```

Web app stateful — protegido contra fixation e limitado a uma sessão por usuário:

```java
@Bean
SecurityFilterChain webChain(HttpSecurity http) throws Exception {
    http
        .sessionManagement(sm -> sm
            .sessionFixation(sf -> sf.migrateSession())
            .maximumSessions(1)
        )
        .formLogin(Customizer.withDefaults());
    return http.build();
}
```

Endurecendo os headers — CSP restritivo, frame deny, HSTS com subdomínios:

```java
@Bean
SecurityFilterChain headersChain(HttpSecurity http) throws Exception {
    http
        .headers(h -> h
            .contentSecurityPolicy(csp -> csp.policyDirectives("default-src 'self'"))
            .frameOptions(fo -> fo.deny())
            .httpStrictTransportSecurity(hsts -> hsts.includeSubDomains(true))
        );
    return http.build();
}
```

Modele entidades de negócio neutras (`Order`, `Customer`, `User`) ao testar esses fluxos — o ponto é a sessão e os headers, não o domínio.

## Armadilhas

### (1) Stateful numa API que devia ser stateless

Deixar a política default (`IF_REQUIRED`) numa API REST faz o Spring criar `HttpSession` em fluxos de login/erro sem você perceber. A API passa a guardar estado em memória local: o load balancer precisa de sticky sessions, e cada instância segura sessões que ninguém deveria ter.

```java
// RUIM: API sem política explícita — herda IF_REQUIRED, pode criar sessão
http.formLogin(Customizer.withDefaults());
```

Fix: declare `STATELESS` explicitamente em chains de API. Sem sessão, escala horizontal é trivial — qualquer instância atende qualquer request.

```java
http.sessionManagement(sm -> sm.sessionCreationPolicy(STATELESS));
```

### (2) CSP com `'unsafe-inline'`

Adicionar `'unsafe-inline'` ao CSP "pra resolver os scripts que não carregavam" desliga justamente a proteção que o CSP oferece: scripts inline injetados por um atacante voltam a executar.

```java
// RUIM: 'unsafe-inline' anula o propósito anti-XSS do CSP
http.headers(h -> h.contentSecurityPolicy(csp ->
    csp.policyDirectives("default-src 'self'; script-src 'self' 'unsafe-inline'")));
```

Fix: use **nonces** ou **hashes** pros scripts legítimos e mantenha `script-src 'self'` (ou `'strict-dynamic'`). Inline vira exceção controlada, não regra aberta.

```java
http.headers(h -> h.contentSecurityPolicy(csp ->
    csp.policyDirectives("default-src 'self'; script-src 'self'")));
```

### (3) Esquecer HSTS/headers atrás de proxy

Atrás de um reverse proxy / load balancer que termina TLS, a aplicação vê o request como **HTTP**. O Spring então omite HSTS (que só é enviado em conexões consideradas seguras), e redirects/headers saem com esquema errado. Tudo "funciona" em dev e falha em produção.

```text
Cliente --HTTPS--> [Proxy/LB termina TLS] --HTTP--> App Spring
                                                    (não vê o request como seguro -> sem HSTS)
```

Fix: registre um `ForwardedHeaderFilter` (ou `server.forward-headers-strategy=framework` no Boot) pra que o app honre os headers `X-Forwarded-Proto`/`X-Forwarded-*` e reconheça o request como HTTPS.

```java
@Bean
ForwardedHeaderFilter forwardedHeaderFilter() {
    return new ForwardedHeaderFilter();
}
```

## Em entrevista

### Frase pronta (inglês)

> For a REST API authenticated by JWT, I set `SessionCreationPolicy.STATELESS` so Spring never creates an `HttpSession` — every request is self-contained and the service scales horizontally without sticky sessions. For a traditional stateful web app, I rely on Spring Security's default session fixation protection, which changes the session identity at login (`changeSessionId` on Servlet 3.1+), and I can cap concurrent sessions with `maximumSessions`. On top of that, Spring is secure-by-default for response headers: it ships HSTS, `X-Frame-Options`, and `nosniff` out of the box, and I explicitly add a strict `Content-Security-Policy` to harden against XSS — avoiding `'unsafe-inline'`, which would defeat the whole point.

### Vocabulário

| Termo (EN) | PT-BR | Nota |
| --- | --- | --- |
| stateless | sem estado | API JWT: nenhuma sessão server-side |
| session fixation | fixação de sessão | atacante planta um ID de sessão conhecido |
| session identity change | troca de identidade da sessão | defesa default no login |
| clickjacking | clickjacking | página embutida em iframe malicioso (`X-Frame-Options`) |
| MIME sniffing | adivinhação de tipo | bloqueada por `nosniff` |
| concurrent session control | controle de sessões simultâneas | `maximumSessions` |
| secure-by-default | seguro por default | headers ligados sem configuração |
| reverse proxy | proxy reverso | termina TLS antes do app (`X-Forwarded-*`) |

## Veja também

- [[03-Dominios/Java/Segurança/09 - OAuth2 Resource Server — validando JWT na API|OAuth2 Resource Server]]
- [[03-Dominios/Java/Segurança/16 - OWASP Top 10 no contexto Java|OWASP Top 10 no contexto Java]]
- [[03-Dominios/Java/Segurança/06 - A arquitetura do filter chain em profundidade|A arquitetura do filter chain]]
- [[03-Dominios/Java/Segurança/index|Segurança (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Dicionário de Java]]

## Referências

- Spring Security Reference — Session Management: https://docs.spring.io/spring-security/reference/servlet/authentication/session-management.html
- Spring Security Reference — HTTP Response Headers: https://docs.spring.io/spring-security/reference/servlet/exploits/headers.html
- Spring Session (clustered sessions / Redis): https://docs.spring.io/spring-session/reference/index.html
