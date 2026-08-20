---
title: "Segurança entre serviços"
created: 2026-06-12
updated: 2026-06-12
type: concept
status: seedling
publish: true
fase: adepto
tags:
  - java
  - microservices
  - adepto
  - seguranca
aliases:
  - "Segurança entre serviços"
  - "Token relay"
  - "Client credentials"
---

# Segurança entre serviços

> [!abstract] TL;DR
> Num monólito, autenticar é um problema só: o usuário entra, a sessão vive no processo. Numa malha de serviços, a pergunta muda — quando o `order-service` chama o `payment-service`, **quem está pedindo, e em nome de quem?** Há duas respostas, e elas não competem: **token relay** repassa o JWT do usuário downstream (o `payment-service` sabe *qual usuário* iniciou a compra); **OAuth2 client-credentials** autentica um serviço falando por si mesmo, sem usuário (um job noturno reconcilia pagamentos). O *mecanismo* — emitir, assinar e validar token, configurar a filter chain — é o [[03-Dominios/Tecnologia/Java/Segurança/12 - OAuth2 e OIDC Client e os grant types|Galho 12 (Segurança)]]. Esta nota é só o ângulo distribuído: **propagação de identidade através da rede**, sob a premissa de **zero-trust** — a rede interna não é confiável.

## O que é

Segurança *entre* serviços é o problema de carregar a identidade — de um usuário ou de um serviço — através de um salto de rede, de forma que o serviço de destino possa decidir, com confiança, se a chamada é legítima.

Dois cenários, dois mecanismos:

- **Token relay** — há um usuário humano na origem. O gateway recebeu o JWT dele, e cada serviço downstream precisa saber *quem* é esse usuário para autorizar a operação. O token do usuário viaja com a requisição, salto a salto.
- **OAuth2 client-credentials** — não há usuário. Um serviço chama outro por iniciativa própria (um cron, um consumidor de fila, uma reconciliação). O serviço autentica *a si mesmo* obtendo um token com suas próprias credenciais.

> [!info] Fronteira com o Galho 12
> Esta nota **não re-explica** OAuth2, OIDC, a anatomia do JWT, nem como montar a `SecurityFilterChain`. Tudo isso é o [[03-Dominios/Tecnologia/Java/Segurança/12 - OAuth2 e OIDC Client e os grant types|Galho 12]] — e os grant types (authorization code, client credentials) são definidos lá. Aqui assumimos que você já sabe o que é um access token e como um *resource server* valida um. O foco é o que muda **quando a chamada cruza a rede**.

## Por que importa

A premissa que torna isso necessário tem nome: **zero-trust**.

No modelo antigo (*perimeter security*, ou "castelo e fosso"), você fortificava a borda — firewall, DMZ — e tratava tudo *dentro* da rede como confiável. Um serviço interno chamava outro sem cerimônia: "estamos na mesma VPC, então somos amigos".

Zero-trust derruba essa premissa. A regra é: **a localização na rede não confere confiança.** Estar dentro do perímetro não prova nada. Toda chamada — interna ou externa — carrega e valida identidade.

Por quê? Porque o castelo cai. Um atacante que comprometeu *um* serviço (uma dependência vulnerável, um pod sequestrado) ganha, no modelo antigo, livre trânsito lateral por toda a rede interna. Esse movimento lateral é o que transforma uma brecha pequena num vazamento catastrófico. Zero-trust contém o estrago: o serviço comprometido ainda precisa de um token válido para falar com qualquer outro, e tokens têm escopo, audiência e validade.

> [!tip] A frase que resume tudo
> "Never trust, always verify." Não importa de onde a chamada vem — ela prova quem é, toda vez.

## Como funciona

### Token relay: repassar o JWT do usuário downstream

Quando o usuário faz login, o gateway recebe um access token (JWT) que o identifica. A questão é: como esse token chega ao `payment-service`, três saltos depois?

A resposta no Spring Cloud Gateway é o filtro **TokenRelay**. Ele extrai o access token OAuth2 da requisição autenticada e o injeta no header `Authorization: Bearer <token>` da requisição que sai para o serviço downstream. A identidade do usuário viaja junto.

Cada serviço no caminho atua como **resource server**: recebe o Bearer token, valida assinatura/expiração/audiência (mecanismo do [[03-Dominios/Tecnologia/Java/Segurança/12 - OAuth2 e OIDC Client e os grant types|Galho 12]]) e autoriza com base no *subject* e nos *scopes* do usuário.

> [!example] A analogia do crachá
> Pense no JWT do usuário como um crachá com foto. No token relay, o usuário entra pela portaria (gateway) e o crachá vai com ele para cada sala. Toda porta lê o mesmo crachá e decide se aquele usuário pode entrar ali. Ninguém "vira" outra pessoa — é sempre o usuário original, do começo ao fim.

### OAuth2 client-credentials: serviço-a-serviço, sem usuário

Nem toda chamada nasce de um usuário. Um job que roda às 3h reconciliando pagamentos não tem ninguém logado. Aqui não há crachá de usuário para repassar — o serviço precisa de identidade *própria*.

O grant **client-credentials** existe para isso. O serviço apresenta suas credenciais (client id + client secret) ao Authorization Server e recebe de volta um access token que representa *o serviço*, não um usuário. Esse token é então usado na chamada downstream.

No Spring Security OAuth2 Client, habilita-se o provider de client-credentials:

```java
OAuth2AuthorizedClientProvider authorizedClientProvider =
    OAuth2AuthorizedClientProviderBuilder.builder()
        .clientCredentials()
        .build();
```

O `OAuth2AuthorizedClientManager` cuida de obter, cachear e renovar esse token automaticamente — você só configura o `client_credentials` grant na registration e usa um `RestClient`/`WebClient` integrado.

> [!note] Quem fala em nome de quem
> Token relay carrega a identidade **do usuário** (subject = pessoa). Client-credentials carrega a identidade **do serviço** (subject = a própria aplicação). Misturar os dois é erro de design: nunca use um token de serviço onde a autorização deveria ser por usuário, nem vice-versa.

### A borda: onde o gateway entra

O [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/10 - API Gateway — papel, roteamento, predicates e filters|API Gateway]] é o ponto natural de autenticação na borda. É ele quem recebe o login do usuário (`oauth2Login()`) e quem hospeda o filtro de token relay.

Configurar TokenRelay no gateway é declarativo. No Spring Cloud Gateway (WebFlux):

```yaml
spring:
  cloud:
    gateway:
      server:
        webflux:
          routes:
            - id: order
              uri: http://order-service:8080
              predicates:
                - Path=/orders/**
              filters:
                - TokenRelay=
```

O `TokenRelay=` (sem `clientRegistrationId`) usa o token da sessão autenticada via `oauth2Login()`. Pré-requisito: a dependência `spring-boot-starter-oauth2-client` e as propriedades `spring.security.oauth2.client.*` configuradas — sem elas, o `TokenRelayGatewayFilterFactory` nem é criado.

> [!warning] Borda autentica, mas não substitui authz interna
> O gateway autenticar na borda **não** dispensa cada serviço de autorizar. O token chega validado, mas é o `payment-service` que decide se *aquele* usuário pode disparar *aquele* pagamento. Borda ≠ delegação de confiança total. (Veja Armadilha 2.)

## Na prática

Cenário: `order-service` cria um pedido (em nome do usuário) e, num passo assíncrono, um job de reconciliação chama o `payment-service` (sem usuário).

### Fluxo 1 — Token relay (usuário presente)

O gateway repassa o JWT do usuário; o `order-service` o recebe e, ao chamar o `payment-service`, propaga adiante:

```yaml
# gateway — application.yml
spring:
  cloud:
    gateway:
      server:
        webflux:
          routes:
            - id: orders
              uri: http://order-service:8080
              predicates:
                - Path=/orders/**
              filters:
                - TokenRelay=
  security:
    oauth2:
      client:
        provider:
          idp:
            issuer-uri: https://auth.internal/realms/app
        registration:
          gateway:
            provider: idp
            client-id: gateway
            authorization-grant-type: authorization_code
            scope: openid, profile
```

```java
// order-service — chamando payment-service com o token do usuário propagado.
// O Bearer token atual da requisição é reaproveitado downstream.
@RestController
class OrderController {

    private final RestClient paymentClient; // configurado com base-url do payment-service

    @PostMapping("/orders")
    OrderResult create(@RequestBody OrderRequest req,
                       @AuthenticationPrincipal Jwt userToken) {
        // identidade do usuário (subject) viaja adiante
        return paymentClient.post()
            .uri("/charges")
            .header(HttpHeaders.AUTHORIZATION, "Bearer " + userToken.getTokenValue())
            .body(req)
            .retrieve()
            .body(OrderResult.class);
    }
}
```

### Fluxo 2 — Client-credentials (sem usuário)

O job de reconciliação não tem usuário logado: o `order-service` autentica *a si mesmo*.

```yaml
# order-service — registration de client-credentials (sem usuário)
spring:
  security:
    oauth2:
      client:
        provider:
          idp:
            issuer-uri: https://auth.internal/realms/app
        registration:
          reconciliation:
            provider: idp
            client-id: order-service
            client-secret: ${ORDER_SERVICE_SECRET}   # do ambiente, NUNCA no código
            authorization-grant-type: client_credentials
            scope: payments.read
```

```java
// order-service — RestClient que obtém e anexa um token de SERVIÇO automaticamente.
@Configuration
class M2mClientConfig {

    @Bean
    RestClient paymentReconClient(RestClient.Builder builder,
                                  OAuth2AuthorizedClientManager manager) {
        var interceptor = new OAuth2ClientHttpRequestInterceptor(manager);
        interceptor.setClientRegistrationIdResolver(req -> "reconciliation");
        return builder
            .baseUrl("http://payment-service:8080")
            .requestInterceptor(interceptor)
            .build();
        // o manager obtém o access token via client_credentials e o injeta no header;
        // cacheia e renova quando expira — sem usuário envolvido.
    }
}
```

O `payment-service`, como resource server, valida o token em ambos os fluxos da mesma forma — a diferença está no *subject* (usuário vs. serviço) e nos *scopes*.

## Armadilhas

### (1) Repassar o token sem validar audience/scope

Token relay não é "encaminhar header e confiar". Se o `payment-service` aceita qualquer Bearer token sem checar a **audiência** (`aud`) e o **escopo** (`scope`), ele aceita tokens que nunca foram destinados a ele. Um token emitido para o `report-service` (com scope `reports.read`) não deveria autorizar uma cobrança. Cada resource server valida `aud` e os scopes que *ele* exige — repasse não dispensa validação no destino.

### (2) Serviço interno sem authz — "a rede interna é confiável" é falso

A armadilha mais perigosa, porque parece economia razoável: "o `payment-service` só é chamado pelo `order-service`, ambos na mesma VPC, então pulo a autenticação ali." Isso é exatamente o modelo castelo-e-fosso que o zero-trust rejeita. Um único serviço comprometido, ou um atacante com acesso à rede interna, chama o `payment-service` à vontade — não há nada validando a identidade. **Endpoint interno também autentica e autoriza.** A rede não é uma credencial.

### (3) Client-credentials com o segredo no código

O `client_secret` é a senha do serviço. Commitar `client-secret: super-secret-123` no `application.yml` versionado vaza essa senha para todo mundo com acesso ao repositório — e ela some do histórico do Git só com reescrita dolorosa. O secret vem do ambiente (`${ORDER_SERVICE_SECRET}`), de um cofre (Vault, Secrets Manager) ou de um secret do orquestrador. Bônus: secrets de longa duração são frágeis — prefira rotação automática e, onde a malha permitir, identidade de workload (SPIFFE/mTLS) em vez de segredos estáticos.

## Em entrevista

### Frase pronta (inglês)

> In a zero-trust microservice architecture, the network is never a credential — every call proves its identity, even internal ones. We handle two distinct cases: when a user is present, we use **token relay**, propagating the user's JWT downstream so each service authorizes against the original subject; the API gateway's TokenRelay filter takes care of that. When there's no user — a scheduled job, a queue consumer — the calling service authenticates as itself with the **OAuth2 client-credentials** grant, getting a token that represents the service, not a person. The key discipline is that propagating a token never replaces validation at the destination: every service validates audience and scope, and no internal endpoint skips authorization just because it sits inside the perimeter.

### Vocabulário

| Português | Inglês | Nota |
| --- | --- | --- |
| Repasse de token | Token relay | Propagar o JWT do usuário salto a salto downstream |
| Credenciais de cliente | Client credentials | Grant serviço-a-serviço, sem usuário |
| Confiança zero | Zero-trust | A rede interna não confere confiança; sempre verificar |
| Audiência | Audience (`aud`) | Para qual destinatário o token foi emitido |
| Escopo | Scope | Permissões que o token concede; validadas no destino |
| Propagação de identidade | Identity propagation | Carregar quem-pede através dos saltos de rede |
| Movimento lateral | Lateral movement | Atacante saltando entre serviços internos após uma brecha |
| Servidor de recurso | Resource server | Serviço que recebe e valida o access token |

## Veja também

- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/10 - API Gateway — papel, roteamento, predicates e filters|API Gateway]]
- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/22 - Service mesh — quando a resiliência sai do código|Service mesh (mTLS)]]
- [[03-Dominios/Tecnologia/Java/Segurança/12 - OAuth2 e OIDC Client e os grant types|OAuth2 e OIDC (Galho 12)]]
- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/index|Microservices e sistemas distribuídos (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]

## Referências

- Spring Security — OAuth2 Client (client-credentials grant): https://docs.spring.io/spring-security/reference/servlet/oauth2/client/index.html
- Spring Cloud Gateway — TokenRelay GatewayFilter Factory: https://docs.spring.io/spring-cloud-gateway/reference/spring-cloud-gateway-server-webflux/gatewayfilter-factories/tokenrelay-factory.html
- Spring Cloud Gateway — referência geral: https://docs.spring.io/spring-cloud-gateway/reference/
