---
title: "OAuth2 e OIDC Client e os grant types"
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
  - oauth2
  - oidc
aliases:
  - "OAuth2 Client"
  - "OIDC"
  - "login social"
  - "grant types"
---

# OAuth2 e OIDC Client e os grant types

> [!abstract] TL;DR
> OAuth2 delega **acesso** (deixa um app agir em nome do usuário sem nunca ver a senha dele); OIDC empilha **identidade** por cima, adicionando o `id_token` (quem é o usuário). O login social no Spring sai de uma linha: `http.oauth2Login(...)`. O grant type seguro pra web e mobile é **authorization code + PKCE** (o recomendado pela RFC 9700); **client credentials** é pra server-to-server sem usuário; e **implicit** e **password** estão deprecated — não entram em código novo. Esta nota cobre o lado **cliente** (login social, obter tokens); validar o JWT na API é o lado Resource Server, na nota 09.

## O que é

**OAuth2** (RFC 6749) é um protocolo de **delegação de autorização**. O problema que ele resolve: um app de terceiros precisa acessar um recurso seu (sua agenda, seu e-mail, seu perfil) sem que você entregue sua senha pra ele. Em vez da senha, o usuário autoriza no provedor (Google, GitHub, Keycloak) e o app recebe um **access token** com escopo limitado.

**OIDC** (OpenID Connect) é uma **camada de identidade** construída sobre o OAuth2. O OAuth2 puro responde "este app pode acessar tal recurso?" — ele não foi desenhado pra dizer **quem** é o usuário. O OIDC fecha essa lacuna adicionando o **`id_token`** (um JWT padronizado com claims como `sub`, `email`, `name`), um endpoint de `userinfo` e o escopo `openid`. Sem OIDC, "login com Google" seria um abuso do OAuth2; com OIDC, é o uso correto.

No Spring Security 6.x / Boot 3.x, o lado **cliente** vive na dependência `spring-boot-starter-oauth2-client` e gira em torno de três peças: o `ClientRegistrationRepository` (quem são os provedores), o `OAuth2AuthorizedClientManager`/`OAuth2AuthorizedClientProvider` (como obter e renovar tokens) e o filtro de `oauth2Login`.

## Por que importa

Num sistema senior real, raramente você implementa autenticação do zero. Você **delega** pra um Identity Provider (IdP) — seja um provedor público (Google, GitHub) ou um corporativo (Keycloak, Auth0, Entra ID). Saber distinguir os grant types não é trivia acadêmica: escolher o errado é uma vulnerabilidade. Implicit flow em SPA nova, client secret embutido num front-end, ou password grant "porque é mais simples" são erros que aparecem em auditorias e em code review de segurança.

Além disso, o lado cliente e o lado servidor são responsabilidades **diferentes**: o cliente **obtém** tokens (te loga, guarda o access token pra chamar APIs); o Resource Server **valida** tokens (checa assinatura e claims do JWT que chega). Confundir os dois leva a configuração redundante ou a buracos de segurança. Esta nota é o lado cliente.

## Como funciona

### OAuth2 (delegação de acesso) vs OIDC (camada de identidade, id_token)

A distinção que mais cai em entrevista:

| Eixo | OAuth2 | OIDC |
|---|---|---|
| Pergunta que responde | "Este app pode **acessar** X?" | "**Quem** é o usuário?" |
| Token central | `access_token` (autorização) | `id_token` (identidade, JWT) |
| Especificação | RFC 6749 | OpenID Connect Core (sobre OAuth2) |
| Escopo gatilho | escopos de recurso (`read`, `write`) | inclui `openid` |
| Caso de uso | API atuando em nome do usuário | login social / SSO |

OIDC **não substitui** OAuth2 — ele o estende. Quando você pede o escopo `openid`, o provedor devolve, além do `access_token`, um `id_token`. O Spring detecta esse `openid` e usa o fluxo OIDC automaticamente, expondo o usuário como `OidcUser` (que carrega o `id_token` e os claims) em vez de um `OAuth2User` genérico.

### Login social: oauth2Login + @AuthenticationPrincipal OidcUser

O `oauth2Login` é o filtro que orquestra o handshake completo: redireciona o usuário pro provedor, recebe o `code` no callback, troca pelo token, busca o `userinfo` e materializa um `Authentication` na `SecurityContext`. Você habilita com uma linha e o Boot autoconfigura o resto a partir das properties.

Dentro de um controller, o usuário autenticado vem injetado por `@AuthenticationPrincipal`:

- `OidcUser` — quando o fluxo é OIDC (escopo `openid` presente). Dá acesso a `getEmail()`, `getFullName()`, `getIdToken()` e aos claims padronizados.
- `OAuth2User` — quando é OAuth2 puro (provedor sem OIDC, ex.: GitHub clássico). Os atributos vêm via `getAttribute("...")`, sem garantia de claims padronizados.

A regra prática: pediu `openid`, recebe `OidcUser`; não pediu, recebe `OAuth2User`.

### Authorization Code + PKCE: o fluxo seguro pra web e mobile

Este é **o** grant type que você usa por padrão. O fluxo:

1. O app redireciona o usuário pro provedor (authorization endpoint).
2. O usuário se autentica e **consente** com os escopos.
3. O provedor redireciona de volta com um **`code`** de uso único (não com o token — o token nunca passa pela URL/navegador).
4. O backend troca o `code` pelo **`access_token`** (e `id_token`, em OIDC) num canal direto e seguro (token endpoint).

O **PKCE** (Proof Key for Code Exchange, RFC 7636) fortalece esse fluxo contra interceptação do `code`. O cliente gera um `code_verifier` aleatório, envia seu hash (`code_challenge`) no passo 1, e no passo 4 prova posse enviando o `verifier` original. Mesmo que um atacante intercepte o `code`, sem o `verifier` ele não troca por token.

A RFC 9700 (OAuth 2.0 Security Best Current Practice) é categórica: **"Public clients MUST use PKCE"** e os authorization servers **"MUST support PKCE"**; pra clientes confidenciais, PKCE é **RECOMMENDED**. Ou seja: PKCE deixou de ser opcional e virou baseline. No Spring Security 6.x, o PKCE é aplicado automaticamente pros clientes públicos.

### Client Credentials: server-to-server, sem usuário

Quando **não há usuário** na jogada — um serviço batch chamando outra API, um cron job, microservices se falando — o grant é **client credentials**. O cliente se autentica com `client-id` + `client-secret` direto no token endpoint e recebe um `access_token` que representa **a aplicação**, não uma pessoa. Não há redirect, não há consent, não há `id_token` (não há identidade de usuário a afirmar).

No Spring, isso é orquestrado pelo `OAuth2AuthorizedClientManager` com um `OAuth2AuthorizedClientProvider` configurado pro grant `client_credentials` — tipicamente pra um `WebClient`/`RestClient` chamar uma API protegida. O `authorization-grant-type` na registration vira `client_credentials`.

> OAuth2 como SSO/gateway entre microservices (propagação de token, token relay) é assunto do Galho 16 (planejado).

### Implicit e Password: deprecated — não use em código novo

Dois grants legados que você precisa **reconhecer pra rejeitar**:

- **Implicit grant** (`response_type=token`): retornava o access token direto na resposta de autorização (na fragment da URL). A RFC 9700 diz que clientes **"SHOULD NOT use the implicit grant"** — ele é vulnerável a vazamento e replay do token. Substituto: authorization code + PKCE (que cobre o caso SPA que o implicit tentava resolver).
- **Resource Owner Password Credentials** (`password`): o usuário entrega usuário+senha **direto pro app**, que repassa pro IdP. A RFC 9700 é taxativa: **"The resource owner password credentials grant MUST NOT be used"** — destrói todo o propósito do OAuth2 (não compartilhar a senha) e aumenta a superfície de ataque.

Regra de ouro: **código novo só usa authorization code + PKCE (com usuário) ou client credentials (sem usuário)**.

### Resource Server (nota 09) vs Client (aqui)

Mesmo ecossistema OAuth2, papéis opostos — e é comum confundir:

| | Client (esta nota) | Resource Server (nota 09) |
|---|---|---|
| Responsabilidade | **Obtém** tokens (loga o usuário, chama APIs) | **Valida** o token que chega |
| Dependência | `spring-boot-starter-oauth2-client` | `spring-boot-starter-oauth2-resource-server` |
| DSL | `http.oauth2Login(...)` / `oauth2Client(...)` | `http.oauth2ResourceServer(...)` |
| Faz handshake/redirect? | Sim | Não — só checa o `Bearer` token |
| Conhece o `client-secret`? | Sim (pra trocar `code` por token) | Não — só a chave pública/JWKS |

Detalhe de validação do JWT (assinatura, claims, `exp`) é a [[03-Dominios/Java/Segurança/08 - JWT — estrutura, assinatura e validação|nota 08]] e o lado Resource Server é a nota 09. Aqui o foco é **chegar** ao token.

## Na prática

Configuração de uma registration OIDC (Google como provedor genérico real). O Spring já conhece o provider `google` por nome, então basta o `client-id`/`client-secret`:

```yaml
spring:
  security:
    oauth2:
      client:
        registration:
          google:
            client-id: ${GOOGLE_CLIENT_ID}
            client-secret: ${GOOGLE_CLIENT_SECRET}
            scope:
              - openid
              - profile
              - email
        # provider 'google' é conhecido pelo Spring;
        # pra um IdP custom (Keycloak/Auth0) você declararia:
        # provider:
        #   keycloak:
        #     issuer-uri: https://idp.exemplo.com/realms/app
```

Habilitar o login social — uma linha na cadeia de filtros:

```java
@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Bean
    SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .authorizeHttpRequests(auth -> auth
                .anyRequest().authenticated()
            )
            // PKCE é aplicado automaticamente pra clientes públicos
            .oauth2Login(Customizer.withDefaults());
        return http.build();
    }
}
```

Lendo o usuário autenticado no controller. Como pedimos o escopo `openid`, o principal chega como `OidcUser`:

```java
@RestController
public class ProfileController {

    @GetMapping("/me")
    public Map<String, String> me(@AuthenticationPrincipal OidcUser principal) {
        return Map.of(
            "email", principal.getEmail(),
            "name", principal.getFullName()
        );
    }
}
```

Diagrama do authorization code flow (com PKCE no pano de fundo):

```text
Usuário          App (cliente)            Provedor (Google/IdP)
  |                  |                          |
  | clica "entrar"   |                          |
  |----------------->|  redirect + code_challenge|
  |                  |------------------------->|
  |        autentica e consente (login + scopes)|
  |<-------------------------------------------- |
  |  redirect de volta com ?code=XYZ            |
  |----------------->|                          |
  |                  |  troca code + verifier   |
  |                  |------------------------->|
  |                  |  access_token + id_token |
  |                  |<------------------------- |
  |   sessão criada  |                          |
  |<-----------------|                          |
```

O token **nunca** trafega pela URL no navegador — só o `code` de uso único, que é inútil sem o `code_verifier` que ficou no backend.

## Armadilhas

### (1) Implicit flow em código novo

Ainda aparece em tutoriais antigos e configs herdadas: SPA configurada com `response_type=token` pra "simplificar" e evitar o roundtrip do backend.

**Exemplo:** uma SPA pede o access token direto no fragment da URL de redirect, sem trocar um `code`.

**Por que dói:** o token fica exposto no histórico do navegador, em logs de proxy e vulnerável a replay. A RFC 9700 diz "clients SHOULD NOT use the implicit grant".

**Fix:** use **authorization code + PKCE**. É exatamente o caso que o PKCE foi desenhado pra resolver em clientes públicos — segurança equivalente sem o backend precisar guardar secret.

### (2) Client secret no front-end / SPA

Tentar reusar um fluxo confidencial (com `client-secret`) num cliente que roda no navegador ou no dispositivo do usuário.

**Exemplo:** o `client-secret` aparece no bundle JavaScript da SPA ou num app mobile descompilável.

**Por que dói:** qualquer um abre o devtools (ou descompila o APK) e extrai o secret. Um secret que o usuário consegue ler **não é secret** — e permite forjar trocas de token.

**Fix:** clientes públicos (SPA, mobile) **não usam secret**. Usam **PKCE**, que prova posse via `code_verifier` dinâmico sem nenhum segredo estático embutido. O `client-secret` só existe em clientes confidenciais server-side.

### (3) Confundir OAuth2 (autorização) com OIDC (autenticação)

Usar OAuth2 puro pra "fazer login" e tratar a posse de um `access_token` como prova de identidade.

**Exemplo:** o app recebe um `access_token` válido e assume "logado como fulano" — sem pedir `openid`, sem validar `id_token`. Isso é o clássico **"confused deputy"**: um access token emitido pra **outro** app pode ser aceito como login (token substitution).

**Por que dói:** access token afirma **autorização** (pode acessar X), não **identidade** (é o usuário Y). Tratá-lo como login abre falha de autenticação.

**Fix:** pra login, use **OIDC** — peça o escopo `openid`, receba e valide o **`id_token`** (cujo `aud` amarra o token ao seu cliente). No Spring, isso é o `oauth2Login` com `OidcUser`.

## Em entrevista

### Frase pronta (inglês)

> OAuth2 is a delegation protocol: it lets an app act on the user's behalf without ever seeing their password, using scoped access tokens. OIDC is an identity layer on top of it — it adds the `id_token`, a JWT that tells you *who* the user is, which is what makes "social login" correct rather than an abuse of OAuth2. For any new code, the only grant types I'd use are **authorization code with PKCE** for web and mobile — PKCE is required for public clients per RFC 9700 — and **client credentials** for server-to-server with no user. Implicit and password grants are deprecated and I'd flag them in review. In Spring it's `oauth2Login` on the client side, which is a separate concern from the resource server that validates the incoming JWT.

### Vocabulário

| Termo | Significado |
|---|---|
| Authorization Code grant | Fluxo via `code` de uso único trocado no backend; padrão seguro |
| PKCE | Proof Key for Code Exchange (RFC 7636); prova de posse que protege o `code` |
| Access token | Token de **autorização** — o que o portador pode acessar |
| `id_token` | JWT de **identidade** (OIDC) — quem é o usuário |
| Client credentials | Grant server-to-server, sem usuário; autentica a aplicação |
| Confidential vs public client | Confidencial guarda `client-secret`; público (SPA/mobile) não — usa PKCE |
| Consent screen | Tela onde o usuário autoriza os escopos solicitados |
| IdP (Identity Provider) | Quem autentica o usuário e emite tokens (Google, Keycloak, Auth0) |

## Veja também

- [[03-Dominios/Java/Segurança/09 - OAuth2 Resource Server — validando JWT na API|OAuth2 Resource Server]]
- [[03-Dominios/Java/Segurança/08 - JWT — estrutura, assinatura e validação|JWT]]
- [[03-Dominios/Java/Segurança/13 - Refresh tokens e revogação de token|Refresh tokens e revogação de token]]
- [[03-Dominios/Java/Segurança/index|Segurança (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Dicionário de Java]]

## Referências

- Spring Security Reference — OAuth 2.0 Client: https://docs.spring.io/spring-security/reference/servlet/oauth2/client/index.html
- Spring Security Reference — OAuth 2.0 Login: https://docs.spring.io/spring-security/reference/servlet/oauth2/login/index.html
- RFC 9700 — Best Current Practice for OAuth 2.0 Security: https://datatracker.ietf.org/doc/html/rfc9700
- RFC 6749 — The OAuth 2.0 Authorization Framework: https://datatracker.ietf.org/doc/html/rfc6749
- RFC 7636 — Proof Key for Code Exchange (PKCE): https://datatracker.ietf.org/doc/html/rfc7636
- OpenID Connect Core 1.0: https://openid.net/specs/openid-connect-core-1_0.html
