---
title: "Versionamento de API"
created: 2026-06-08
updated: 2026-06-08
type: concept
progress: backlog
status: seedling
publish: true
fase: magus
tags:
  - java
  - web
  - magus
  - versioning
aliases:
  - "API versioning"
---

# Versionamento de API

> [!abstract] TL;DR
> Versionar uma API é o ato de criar contratos explícitos e estáveis para os seus clientes — eles não atualizam junto com você, e quebrar a interface significa quebrar produção deles. As quatro estratégias principais (URI path, request param, custom header, media-type) têm trade-offs distintos de visibilidade, cache e purismo REST; escolher a errada para o contexto é tão problemático quanto não versionar. O ciclo completo inclui comunicar deprecação antecipada via headers `Deprecation` e `Sunset` antes de qualquer remoção.

## O que é

Versionamento de API é a prática de expor múltiplas versões de um mesmo contrato HTTP ao mesmo tempo, de modo que clientes existentes continuem funcionando enquanto versões novas são desenvolvidas e adotadas gradualmente.

Uma "versão" representa um conjunto de endpoints, schemas de request/response e comportamentos que permanece estável durante um período acordado. Quando uma mudança incompatível (breaking change) é necessária — alterar o tipo de um campo, remover um atributo, mudar a semântica de um parâmetro — ela é publicada em uma nova versão, sem tocar na anterior.

O versionamento é diferente de versionamento semântico de biblioteca (SemVer): aqui o foco é o contrato de rede, não o código interno.

## Por que importa

APIs públicas ou consumidas por sistemas externos têm um ciclo de vida desacoplado dos clientes. Uma aplicação mobile, por exemplo, pode estar na versão que o usuário instalou há dois anos; um sistema de parceiro pode ter sido integrado e nunca mais modificado. Esses clientes **não atualizam junto com o servidor**.

Sem versionamento, qualquer mudança no servidor é um risco direto de regressão em produção para esses clientes. Com versionamento bem definido:

- Mudanças incompatíveis são introduzidas em nova versão sem remover a anterior imediatamente.
- A equipe pode comunicar antecipadamente quais versões serão descontinuadas e quando.
- Clientes têm tempo hábil para migrar sem pressão de emergência.
- O contrato de cada versão pode ser documentado (via OpenAPI) de forma independente.

Em cenários de microserviços, onde dezenas de serviços se comunicam entre si, a ausência de versionamento multiplica o risco de deploys coordenados obrigatórios (lock-step deployments) — um dos piores gargalos operacionais.

## Como funciona

### Por que versionar — contrato com clientes que não atualizam juntos

O princípio fundamental é: **quem expõe a API não controla quando os clientes atualizam**. Isso gera uma assimetria: o servidor pode evoluir com frequência, mas os clientes evoluem no próprio ritmo.

Versionar é formalizar essa assimetria como uma promessa: "enquanto você usar `/v1/...`, o contrato não muda". A quebra dessa promessa sem aviso prévio é chamada de *breaking change silencioso* e é uma das causas mais comuns de incidentes em integrações.

Exemplos de breaking changes que exigem nova versão:
- Remover ou renomear um campo no response.
- Alterar o tipo de um campo (de `string` para `int`, de objeto para array).
- Tornar obrigatório um parâmetro que era opcional.
- Mudar a semântica de um código de status retornado.

Exemplos de mudanças que **não** exigem nova versão (non-breaking):
- Adicionar novos campos opcionais ao response.
- Adicionar novos endpoints.
- Melhorar mensagens de erro sem mudar o schema.

### As 4 estratégias

#### 1. URI Path (`/v1/orders`)

A versão faz parte da URL:

```
GET /v1/orders
GET /v2/orders
```

É a abordagem mais visível: o número da versão aparece no browser, nos logs, nas ferramentas de monitoramento, e é fácil de testar com `curl`. Recursos diferentes têm URLs distintas, o que simplifica o roteamento em gateways e proxies.

A crítica do ponto de vista REST estrito é que a versão não identifica um *recurso diferente*, mas sim uma *representação diferente do mesmo recurso* — portanto, violaria o princípio de URI estável. Na prática, muitas equipes aceitam essa concessão pela simplicidade operacional.

#### 2. Request Parameter (`?version=2` ou `?v=2`)

A versão é passada como query parameter:

```
GET /orders?version=2
GET /orders?v=1
```

Mantém a URL base limpa, mas polui a query string. Funciona bem para APIs usadas principalmente por scripts ou ferramentas internas onde a URL completa é montada programaticamente. Tende a ser menos clara em logs e mais difícil de tratar em configurações de cache HTTP (que costumam ignorar ou tratar query params de forma inconsistente).

#### 3. Custom Header

A versão é enviada em um header HTTP customizado:

```
GET /orders
X-Api-Version: 2
```

Mantém a URL completamente limpa. É a abordagem preferida quando se quer que a mesma URL represente o mesmo recurso independentemente da versão. O principal custo é a invisibilidade: a versão não aparece na URL e é ignorada por ferramentas que não examinam headers, como alguns proxies de cache ou clientes HTTP simples.

#### 4. Media Type / Content Negotiation (`Accept: application/vnd.company.v2+json`)

A versão é negociada via o header `Accept`, usando um vendor media type:

```
GET /orders
Accept: application/vnd.company.v2+json
```

O servidor inspeciona o `Accept` e seleciona o handler compatível. É a abordagem mais alinhada com os princípios REST (representa literalmente a negociação de representação do recurso). Também é a mais complexa de implementar e de depurar — errar o media type resulta em 406 Not Acceptable, e testar com `curl` requer mais argumentos.

### Trade-offs, deprecação e headers `Deprecation`/`Sunset`

| Critério | URI Path | Request Param | Custom Header | Media Type |
|---|---|---|---|---|
| Visibilidade | Alta | Média | Baixa | Baixa |
| Cache HTTP | Fácil | Problemático | Problemático | Problemático |
| Roteamento em gateway | Trivial | Requer parsing | Requer header routing | Requer header routing |
| Purismo REST | Baixo | Baixo | Médio | Alto |
| Facilidade de teste | Alta | Alta | Média | Baixa |

**Deprecação antecipada** é tão importante quanto a estratégia de versionamento em si. O ciclo correto é:

1. Publicar a nova versão.
2. Anunciar a deprecação da versão anterior (data fim definida).
3. Retornar headers de aviso em todas as respostas da versão depreciada.
4. Remover a versão depreciada somente após o prazo.

Os headers padronizados para esse ciclo são:

- **`Deprecation`** (RFC 9745): indica que o endpoint está depreciado. O valor pode ser `true` ou uma data HTTP no formato `@<timestamp-unix>`.
- **`Sunset`** (RFC 8594): indica a data em que o endpoint será removido. Formato: data HTTP (`Tue, 01 Jul 2025 00:00:00 GMT`).
- **`Link`** (RFC 8594): pode apontar para a versão substituta ou para documentação de migração.

```
HTTP/1.1 200 OK
Deprecation: @1735689600
Sunset: Tue, 01 Jul 2025 00:00:00 GMT
Link: <https://api.example.com/v2/orders>; rel="successor-version"
```

O Spring Framework 7.0 traz suporte nativo a esses headers via `ApiVersionDeprecationHandler` / `StandardApiVersionDeprecationHandler`, configurável pelo MVC Config.

## Na prática

### URI Path — Spring MVC clássico (Spring Boot 3 / Spring Framework 6.x)

No baseline do Spring Boot 3, o versionamento por URI path é feito criando controllers separados ou usando prefixo de URL nos mapeamentos:

```java
// Versão 1 — mantida para compatibilidade
@RestController
@RequestMapping("/v1/orders")
public class OrderControllerV1 {

    @GetMapping("/{id}")
    public OrderV1Response getOrder(@PathVariable Long id) {
        // retorna schema antigo
        return orderService.findV1(id);
    }
}

// Versão 2 — novo contrato
@RestController
@RequestMapping("/v2/orders")
public class OrderControllerV2 {

    @GetMapping("/{id}")
    public OrderV2Response getOrder(@PathVariable Long id) {
        // retorna schema novo com campos adicionais
        return orderService.findV2(id);
    }
}
```

### Media Type / Content Negotiation

```java
@RestController
@RequestMapping("/orders")
public class OrderController {

    // Versão 1 — media type padrão
    @GetMapping(
        value = "/{id}",
        produces = "application/json"
    )
    public OrderV1Response getOrderV1(@PathVariable Long id) {
        return orderService.findV1(id);
    }

    // Versão 2 — vendor media type com versão explícita
    @GetMapping(
        value = "/{id}",
        produces = "application/vnd.company.v2+json"
    )
    public OrderV2Response getOrderV2(@PathVariable Long id) {
        return orderService.findV2(id);
    }
}
```

Testando via `curl`:

```bash
# Acessa versão 1 (Accept padrão)
curl -H "Accept: application/json" \
     http://localhost:8080/orders/42

# Acessa versão 2 via vendor media type
curl -H "Accept: application/vnd.company.v2+json" \
     http://localhost:8080/orders/42

# Acessa versão 1 via URI path
curl http://localhost:8080/v1/orders/42

# Acessa versão 2 via URI path
curl http://localhost:8080/v2/orders/42
```

### Spring Framework 7 — suporte nativo via atributo `version`

O Spring Framework 7.0 (mais recente) introduz o atributo `version` diretamente no `@RequestMapping` e derivados, eliminando a necessidade de controllers duplicados. O framework resolve a versão da request via `ApiVersionStrategy` configurada no MVC Config:

```java
// Spring Framework 7 — versões no mesmo controller
@RestController
@RequestMapping("/orders/{id}")
public class OrderController {

    @GetMapping
    public OrderV1Response getOrderDefault() {
        // sem versão: atende qualquer request sem versão explícita
        return orderService.findV1(/* ... */);
    }

    @GetMapping(version = "1.1")
    public OrderV1Response getOrderV1_1() {
        // atende exatamente version=1.1
        return orderService.findV1_1(/* ... */);
    }

    @GetMapping(version = "2.0+")
    public OrderV2Response getOrderV2() {
        // atende 2.0 e qualquer versão suportada acima
        return orderService.findV2(/* ... */);
    }
}
```

> [!note] Versão do framework
> O atributo `version` em `@RequestMapping` é uma adição do **Spring Framework 7.0**. No Spring Boot 3 / Spring Framework 6.x (baseline atual), o versionamento ainda é feito de forma manual (controllers separados, URL prefix, ou custom `HandlerMapping`).

## Armadilhas

### (1) Nunca versionar e quebrar clientes existentes

**Descrição:** A equipe publica breaking changes diretamente no endpoint existente sem versionar, confiando que todos os clientes serão atualizados ao mesmo tempo.

**Exemplo:**
```java
// Antes: campo "name" no response
record ProductResponse(Long id, String name) {}

// Depois: campo renomeado para "productName" SEM nova versão
record ProductResponse(Long id, String productName) {}
// Qualquer cliente que lia "name" quebra silenciosamente (null ou erro de desserialização)
```

**Fix:** Qualquer mudança incompatível exige nova versão. Se o projeto ainda não versiona, adotar URI path é o caminho de menor atrito para começar. Nunca renomear/remover campos em versão existente.

### (2) Versionar cedo demais — complexidade sem necessidade

**Descrição:** Adicionar versionamento em uma API interna, consumida por um único time no mesmo monorepo, gera overhead de manutenção sem benefício real. Cada nova versão precisa ser mantida até ser removida.

**Exemplo:**
```
/v1/internal/config
/v2/internal/config   ← nunca chegou a ter clientes externos
/v3/internal/config   ← todos no mesmo deploy
```

**Fix:** Versionar apenas quando há clientes externos ao time ou quando o ciclo de deploy é desacoplado. Para APIs internas com controle total dos clientes, prefira refatoração coordenada.

### (3) Misturar estratégias incoerentemente

**Descrição:** Parte da API usa URI path, parte usa header customizado, parte usa query param. Clientes precisam aprender três mecanismos diferentes para consumir a mesma API.

**Exemplo:**
```
GET /v2/orders          ← URI path
GET /products?version=2 ← query param
GET /customers          com header X-Api-Version: 2  ← header
```

**Fix:** Escolher uma única estratégia e aplicá-la de forma consistente em toda a API. Documentar a escolha no `README` e no contrato OpenAPI. Mudanças de estratégia exigem período de transição com suporte duplo.

### (4) "v2" que muda semântica sem comunicar a deprecação

**Descrição:** Uma nova versão é publicada, mas a versão anterior continua disponível indefinidamente sem qualquer aviso de deprecação. Clientes nunca migram porque não sabem que precisam, e a equipe acumula N versões antigas para manter.

**Exemplo:**
```java
// v1 continua ativa, sem headers Deprecation/Sunset
// v2 existe há 8 meses
// v3 foi lançada ontem
// nenhum cliente foi avisado de nada
```

**Fix:** No momento do lançamento de v2, definir já a data de remoção de v1 e começar a retornar os headers `Deprecation` e `Sunset` em todas as respostas de v1. Comunicar ativamente via changelog, email ou portal de desenvolvedores.

## Em entrevista

### Frase pronta (inglês)

"API versioning is about honoring your contract with clients that don't update on your schedule. The core trade-off is between visibility and REST purity: URI path versioning is the most operationally simple — it shows up in logs, browsers, and gateways without any special configuration — but it violates the REST principle that a URI should identify a stable resource. Media-type negotiation via vendor Accept headers is the most REST-aligned approach, but it adds friction for testing and debugging. In practice, I'd pick URI path for public-facing APIs and content negotiation when the team already has strong HTTP client conventions. Either way, versioning is incomplete without a deprecation lifecycle: Deprecation and Sunset headers give clients concrete deadlines to migrate, which is what separates a planned evolution from a surprise outage."

### Vocabulário

| Português | Inglês |
|---|---|
| Versionamento de API | API versioning |
| Mudança incompatível | Breaking change |
| Negociação de conteúdo | Content negotiation |
| Tipo de mídia do fornecedor | Vendor media type |
| Depreciação | Deprecation |
| Pôr do sol (data de remoção) | Sunset |
| Contrato de API | API contract |
| Versão de linha de base | Baseline version |
| Roteamento em gateway | Gateway routing |
| Deploy sem coordenação | Independent deployment |

## Veja também

- [[03-Dominios/Tecnologia/Java/Web e APIs REST/02 - @RestController e os mapeamentos|@RestController e os mapeamentos]]
- [[03-Dominios/Tecnologia/Java/Web e APIs REST/07 - Content negotiation|Content negotiation]]
- [[03-Dominios/Tecnologia/Java/Web e APIs REST/12 - Documentando a API com OpenAPI e Swagger|Documentando a API com OpenAPI e Swagger]]
- [[03-Dominios/Tecnologia/Java/Web e APIs REST/index|Web e APIs REST]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- Verbete: [[03-Dominios/Tecnologia/Java/Dicionário de Java#API versioning|API versioning]]

## Referências

- Spring Framework Reference — Request Mapping (versioning): https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-controller/ann-requestmapping.html
- Spring Framework Reference — API Versioning: https://docs.spring.io/spring-framework/reference/web/webmvc-versioning.html
- RFC 9745 — The Deprecation HTTP Header Field: https://www.rfc-editor.org/rfc/rfc9745
- RFC 8594 — The Sunset HTTP Header Field: https://www.rfc-editor.org/rfc/rfc8594
