---
title: "HATEOAS"
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
  - hateoas
  - rest
aliases:
  - "Spring HATEOAS"
  - "Richardson Maturity Model"
---

# HATEOAS

> [!abstract] TL;DR
> HATEOAS (Hypermedia as the Engine of Application State) é o nível 3 do Richardson Maturity Model: a resposta carrega os links das próximas ações possíveis, tornando o cliente "guiado" pela API. O Spring HATEOAS implementa isso via `EntityModel`, `Link`, `WebMvcLinkBuilder` e serialização HAL (`application/hal+json`). Na prática, o custo de manter os links raramente compensa — a maioria das APIs comerciais para no nível 2 (verbos HTTP corretos). HATEOAS aparece mais em entrevistas e discussões de maturidade REST do que em produção.

## O que é

HATEOAS é um princípio arquitetural proposto por Roy Fielding como parte da definição original de REST. O nome é um acrônimo para *Hypermedia as the Engine of Application State*: o estado da aplicação cliente é conduzido pelos links hipermídia presentes na resposta, não por conhecimento prévio dos endpoints.

Em termos concretos: uma resposta HAL não devolve apenas dados do recurso. Ela também inclui um objeto `_links` com relações nomeadas — `self`, `next`, `cancel`, `update` — que descrevem o que o cliente pode fazer a seguir e para onde deve navegar. O cliente não precisa montar URLs, apenas seguir links.

O formato mais comum de hipermídia em APIs REST é o **HAL** (Hypertext Application Language), cujo `Content-Type` é `application/hal+json`.

## Por que importa

- **Desacoplamento evolutivo**: clientes que seguem links em vez de hardcodar URLs resistem melhor a mudanças na estrutura de endpoints.
- **Descoberta de capacidades**: a resposta indica quais ações estão disponíveis *naquele estado* do recurso — por exemplo, `cancel` só aparece se o pedido ainda pode ser cancelado.
- **Interoperabilidade**: APIs nível 3 são mais próximas do que Tim Berners-Lee e Roy Fielding definiram como a web funcionando corretamente.
- **Sinalização de maturidade**: em entrevistas para vagas sênior, saber explicar HATEOAS e quando *não* usá-lo demonstra senioridade de projeto.

Na prática, a maioria das APIs públicas (GitHub, Stripe, Twilio) opera no nível 2. A adoção do nível 3 é rara, concentrada em sistemas que precisam de navegação dinâmica — como APIs hipermídia de e-commerce ou sistemas bancários regulamentados. Dizer "raramente adotado" é honesto; inventar percentual não é.

## Como funciona

### Hypermedia as the engine of application state — a ideia

A ideia central é análoga a navegar na web: você não precisa memorizar URLs, você clica em links. Em uma API HATEOAS, o cliente faz uma requisição inicial (geralmente para um ponto de entrada raiz) e recebe links para o que pode fazer em seguida. Cada resposta subsequente traz novos links — ou omite os que não estão disponíveis no estado atual.

Isso contrasta com APIs nível 2, onde o cliente conhece antecipadamente a estrutura de URLs e constrói requisições por conta própria. No nível 3, o servidor é o único detentor da verdade sobre os endpoints.

### Richardson Maturity Model (0 RPC → 1 recursos → 2 verbos → 3 hypermedia)

Leonard Richardson propôs um modelo de 4 níveis para classificar a maturidade de APIs REST. Martin Fowler popularizou o modelo no artigo ["Richardson Maturity Model"](https://martinfowler.com/articles/richardsonMaturityModel.html).

| Nível | Nome | Característica principal |
|-------|------|--------------------------|
| **0** | POX / RPC sobre HTTP | Um único endpoint, HTTP como túnel de transporte. Verbos e semântica HTTP ignorados. |
| **1** | Recursos | Endpoints distintos por recurso (`/orders/42`, `/customers/7`). Ainda sem uso correto de verbos. |
| **2** | Verbos HTTP | GET para leitura (seguro, cacheável), POST/PUT/PATCH para mutação, DELETE para remoção. Status codes semânticos (201, 404, 409). |
| **3** | Hypermedia (HATEOAS) | Resposta inclui `_links` descrevendo ações disponíveis. Cliente navega pela API sem conhecimento prévio de URLs. |

Roy Fielding é direto: "REST" de verdade exige o nível 3. A maioria do que chamamos de "API REST" no mercado é nível 2 — e isso é perfeitamente funcional para a maioria dos casos.

### Spring HATEOAS (EntityModel, Link, WebMvcLinkBuilder, HAL)

O Spring HATEOAS oferece três abstrações principais para construir respostas hipermídia:

**`RepresentationModel`** — classe base. Qualquer DTO pode estendê-la para ganhar suporte a links. Raramente usada diretamente; prefira as subclasses.

**`EntityModel<T>`** — wrapper para um único recurso. Encapsula o DTO e uma coleção de links.

```java
EntityModel<OrderDto> model = EntityModel.of(orderDto,
    linkTo(methodOn(OrderController.class).findById(orderDto.id())).withSelfRel()
);
```

**`CollectionModel<T>`** — wrapper para coleções de recursos, com links no nível da coleção.

**`Link`** — tipo imutável representando um hyperlink com uma relação nomeada (`rel`) e um `href`.

```java
Link cancelLink = Link.of("/orders/42/cancel", "cancel");
Link allLink = linkTo(methodOn(OrderController.class).findAll()).withRel("all-orders");
```

**`WebMvcLinkBuilder` + `linkTo(methodOn(...))`** — utilitário que deriva URLs diretamente dos métodos do controller, eliminando strings hardcoded.

```java
import static org.springframework.hateoas.server.mvc.WebMvcLinkBuilder.*;

Link selfLink = linkTo(methodOn(OrderController.class).findById(42L)).withSelfRel();
// Gera: { "rel": "self", "href": "http://localhost/orders/42" }
```

**HAL (Hypertext Application Language)** — formato padrão do Spring HATEOAS. As respostas são serializadas com `_links` no nível raiz. Para coleções, recursos aninhados ficam em `_embedded`.

### Quando (não) usar — o custo vs o benefício (honesto)

**Use quando:**
- Você controla tanto o servidor quanto clientes que efetivamente vão navegar pelos links.
- A API precisa de descoberta dinâmica: ações disponíveis variam por estado do recurso (ex.: `pay` só aparece em pedidos confirmados).
- O contrato de API muda frequentemente e clientes devem absorver mudanças sem redeployment.

**Evite quando:**
- Clientes são SPAs ou apps mobile com URLs hardcoded — os links nunca serão consumidos.
- Time pequeno: manter `_links` consistentes em todos os endpoints tem custo não trivial de teste e revisão.
- API é interna e bem documentada: o benefício de descoberta é mínimo.

O trade-off honesto: HATEOAS adiciona payload, aumenta complexidade de manutenção e exige clientes que realmente naveguem pelos links. Se o cliente ignora `_links`, você carrega o custo sem ganhar o benefício.

## Na prática

Cenário: API de pedidos com recursos para buscar um pedido e listar todos.

```java
// OrderDto como record Java moderno
public record OrderDto(Long id, String product, String status) {}

// Controller
@RestController
@RequestMapping("/orders")
public class OrderController {

    @GetMapping("/{id}")
    public ResponseEntity<EntityModel<OrderDto>> findById(@PathVariable Long id) {
        // Em produção: buscar do serviço
        OrderDto order = new OrderDto(id, "Laptop Pro", "CONFIRMED");

        EntityModel<OrderDto> model = EntityModel.of(order,
            linkTo(methodOn(OrderController.class).findById(id))
                .withSelfRel(),
            linkTo(methodOn(OrderController.class).findAll())
                .withRel("all-orders"),
            Link.of("/orders/" + id + "/cancel")
                .withRel("cancel")
        );

        return ResponseEntity.ok(model);
    }

    @GetMapping
    public ResponseEntity<CollectionModel<EntityModel<OrderDto>>> findAll() {
        // simplificado
        return ResponseEntity.ok(CollectionModel.empty(
            linkTo(methodOn(OrderController.class).findAll()).withSelfRel()
        ));
    }
}
```

JSON HAL resultante para `GET /orders/42`:

```json
{
  "id": 42,
  "product": "Laptop Pro",
  "status": "CONFIRMED",
  "_links": {
    "self": {
      "href": "http://localhost/orders/42"
    },
    "all-orders": {
      "href": "http://localhost/orders"
    },
    "cancel": {
      "href": "/orders/42/cancel"
    }
  }
}
```

O cliente pode navegar para `_links.cancel.href` sem conhecer previamente a URL de cancelamento. Se o pedido estiver no estado `SHIPPED`, o servidor simplesmente omite o link `cancel` — o cliente descobre que a ação não está disponível sem precisar codificar essa regra de negócio.

Dependência Maven necessária:

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-hateoas</artifactId>
</dependency>
```

## Armadilhas

### (1) Confundir "REST" com nível 2

**Problema:** A maioria das APIs do mercado usa verbos HTTP corretamente (nível 2) e se autodenomina "RESTful". Isso é pragmaticamente aceitável, mas tecnicamente o nível 2 não é REST segundo Fielding.

**Risco:** Em entrevista ou design review, afirmar que uma API é "REST de verdade" porque usa `GET`/`POST`/`DELETE` pode gerar questionamentos. A resposta correta é: "nossa API é nível 2 do Richardson Maturity Model, o que é suficiente para nossos requisitos".

**Fix:** Seja preciso na linguagem. "API HTTP com recursos e verbos semânticos" descreve nível 2 sem a carga do termo REST.

### (2) Adicionar links que nenhum cliente consome

**Problema:** Implementar HATEOAS completo em todos os endpoints quando os clientes (SPA, app mobile, CLI) constroem URLs hardcoded e ignoram `_links`.

```java
// Custo real: todos esses links são construídos, serializados e ignorados pelo cliente
EntityModel.of(product,
    linkTo(methodOn(ProductController.class).findById(id)).withSelfRel(),
    linkTo(methodOn(ProductController.class).findAll()).withRel("products"),
    linkTo(methodOn(CategoryController.class).findById(product.categoryId())).withRel("category"),
    linkTo(methodOn(CartController.class).addItem(null)).withRel("add-to-cart")
);
```

**Fix:** Valide se os clientes reais navegam pelos links antes de implementar. Se não navegam, nível 2 é suficiente — e mais simples de manter.

### (3) Achar HATEOAS obrigatório para "ser REST"

**Problema:** Pressionar o time a implementar HATEOAS em APIs internas apenas para "seguir o padrão REST corretamente", ignorando o custo de manutenção dos links e a ausência de clientes que os consumam.

**Sintoma:** Controllers com assemblers complexos, testes de links frágeis, e documentação de `_links` que ninguém lê.

**Fix:** REST é uma escolha de estilo arquitetural, não um requisito de compliance. A decisão de ir para nível 3 deve ser baseada em necessidades reais de descoberta dinâmica, não em purismo técnico. Em APIs internas bem documentadas, contrato explícito (OpenAPI) costuma ser mais prático que HATEOAS.

## Em entrevista

### Frase pronta (inglês)

"HATEOAS is the third level of the Richardson Maturity Model, where API responses include hypermedia links describing available next actions — like `cancel`, `pay`, or `update` — rather than requiring clients to know the URL structure upfront. In Spring, we implement this using `EntityModel`, `WebMvcLinkBuilder`, and HAL serialization. That said, most production APIs stop at level two because HATEOAS only pays off when clients actually navigate the links, and that's rarely the case in practice."

"The key benefit is decoupling: clients follow links instead of constructing URLs, so the server can change its URL structure without breaking clients. The key cost is maintenance — every endpoint needs to return consistent, state-aware links, which adds significant testing and review overhead."

"I'd choose HATEOAS when the API has complex workflows where available actions depend on resource state — for example, a payment API where `capture` only appears after `authorize`. I'd skip it for straightforward CRUD APIs where the client just needs a stable contract."

### Vocabulário

| Português | English |
|-----------|---------|
| Hipermídia como motor de estado | Hypermedia as the Engine of Application State |
| Modelo de maturidade de Richardson | Richardson Maturity Model |
| Relação de link | Link relation (`rel`) |
| Recurso hipermídia | Hypermedia resource |
| Nível 3 REST | Level 3 REST / Hypermedia controls |
| Montagem de URL no cliente | Client-side URL construction |
| Ações disponíveis por estado | State-aware available actions |
| Formato HAL | HAL (Hypertext Application Language) |

## Veja também

- [[03-Dominios/Tecnologia/Java/Web e APIs REST/04 - ResponseEntity e status codes|ResponseEntity e status codes]]
- [[03-Dominios/Tecnologia/Java/Web e APIs REST/13 - Versionamento de API|Versionamento de API]]
- [[03-Dominios/Tecnologia/Java/Web e APIs REST/index|Web e APIs REST]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- Verbetes: [[03-Dominios/Tecnologia/Java/Dicionário de Java#HATEOAS|HATEOAS]], [[03-Dominios/Tecnologia/Java/Dicionário de Java#Spring HATEOAS|Spring HATEOAS]], [[03-Dominios/Tecnologia/Java/Dicionário de Java#Richardson Maturity Model|Richardson Maturity Model]]

## Referências

- [Spring HATEOAS — Reference Documentation](https://docs.spring.io/spring-hateoas/docs/current/reference/html/)
- [Richardson Maturity Model — Martin Fowler](https://martinfowler.com/articles/richardsonMaturityModel.html)
- [Hypertext Application Language (HAL) — Draft Specification](https://tools.ietf.org/html/draft-kelly-json-hal)
- [Roy Fielding — Architectural Styles and the Design of Network-based Software Architectures (REST original)](https://www.ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm)
