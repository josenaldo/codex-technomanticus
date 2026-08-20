---
title: "JAX-RS — REST declarativo"
created: 2026-06-07
updated: 2026-06-08
type: concept
progress: backlog
status: seedling
publish: true
fase: adepto
tags:
  - java
  - jakarta-ee
  - adepto
  - jax-rs
aliases:
  - "JAX-RS"
  - "REST Jakarta"
  - "Jakarta RESTful Web Services"
---

# JAX-RS — REST declarativo

> [!abstract] TL;DR
> JAX-RS mapeia HTTP para métodos Java por annotations — resource classes, params tipados, content negotiation e providers. Roda sobre a Servlet API por baixo (nota [[03 - Servlet API — o alicerce HTTP]]); controllers do Spring ([[03-Dominios/Tecnologia/Java/Web e APIs REST/02 - @RestController e os mapeamentos|@RestController]]) são outro caminho para o mesmo problema. Entender a spec é o diferencial em entrevista: você explica *por que* funciona, não só *como* usar.

## O que é

**Jakarta RESTful Web Services 4.0** (JAX-RS 4.0) é a especificação oficial da plataforma Jakarta EE 11 para construção de serviços web REST. Requer Java SE 17 ou superior. A spec define um modelo declarativo baseado em annotations: você anota classes e métodos Java e o runtime cuida do mapeamento HTTP ↔ Java.

O modelo é simples conceitualmente:

- **Resource classes** são POJOs anotados com `@Path` — o container os instancia e roteia as requisições para eles.
- **Providers** são componentes de extensão: leem e escrevem representações (`MessageBodyReader/Writer`), mapeiam exceções para respostas HTTP (`ExceptionMapper`), e resolvem contextos especializados (`ContextResolver`).
- A **Client API** (via `ClientBuilder`) espelha o mesmo modelo para consumir endpoints REST de outros serviços.

As implementações de referência são **Eclipse Jersey 4.0** (implementação de referência oficial) e **RESTEasy 7.0** (Red Hat/WildFly). Ambas implementam a spec completa.

## Por que importa

REST é o protocolo de integração dominante na indústria — APIs REST são a interface padrão entre microsserviços, entre frontend e backend, e entre sistemas de parceiros. Entender JAX-RS significa entender como um request HTTP se transforma em chamada de método Java e como a resposta faz o caminho inverso.

O modelo de **providers** é particularmente valioso porque explica algo que frameworks "mágicos" escondem: *como o JSON vira objeto*. Quando você injeta um `Order` de um request body, existe um `MessageBodyReader` que faz essa conversão — geralmente via **JSON-B** (Jakarta JSON Binding) ou **JSON-P** (Jakarta JSON Processing). Saber isso resolve problemas de deserialização que aparecem constantemente em produção.

Em entrevista, saber a spec é o diferencial porque você consegue comparar abordagens: JAX-RS (spec portável), Spring MVC ([[03-Dominios/Tecnologia/Java/Web e APIs REST/index|Web e APIs REST]]), ou Quarkus/Micronaut (que implementam JAX-RS por baixo). Quem conhece só o framework não sabe o que acontece quando a magia falha.

## Como funciona

### Resources (`@Path` em classe/método; templates `/orders/{id}`; verbos)

`@Path` pode ser aplicada na classe (path base) e/ou no método (sub-path). O runtime concatena os dois.

```java
import jakarta.ws.rs.GET;
import jakarta.ws.rs.POST;
import jakarta.ws.rs.PUT;
import jakarta.ws.rs.DELETE;
import jakarta.ws.rs.Path;

@Path("/orders")                         // path base do resource
public class OrderResource {

    @GET                                 // GET /orders
    public List<OrderDto> listAll() { ... }

    @GET
    @Path("/{id}")                       // GET /orders/{id}  — template URI
    public OrderDto findById(@PathParam("id") Long id) { ... }

    @POST                                // POST /orders
    public Response create(OrderDto dto) { ... }

    @PUT
    @Path("/{id}")                       // PUT /orders/{id}
    public Response update(@PathParam("id") Long id, OrderDto dto) { ... }

    @DELETE
    @Path("/{id}")                       // DELETE /orders/{id}
    public Response delete(@PathParam("id") Long id) { ... }
}
```

Templates URI usam `{variavel}` e podem ter expressões regulares: `{id: [0-9]+}` restringe o match.

### Params (`@PathParam`/`@QueryParam`/`@HeaderParam` — conversão de tipos)

O runtime converte automaticamente strings HTTP para tipos Java primitivos, `String`, e qualquer tipo com construtor `String` ou método estático `valueOf(String)`.

```java
import jakarta.ws.rs.PathParam;
import jakarta.ws.rs.QueryParam;
import jakarta.ws.rs.HeaderParam;
import jakarta.ws.rs.FormParam;
import jakarta.ws.rs.DefaultValue;

@GET
@Path("/{id}")
public OrderDto findById(
    @PathParam("id")   Long id,              // /orders/42       → id=42
    @QueryParam("lang") @DefaultValue("pt") String lang  // ?lang=en
) { ... }

@GET
public List<OrderDto> search(
    @QueryParam("status") String status,     // ?status=PENDING
    @QueryParam("page")   @DefaultValue("0") int page
) { ... }

@POST
@Path("/{id}/notes")
public Response addNote(
    @PathParam("id")     Long id,
    @HeaderParam("X-User-Id") String userId, // header HTTP
    @FormParam("text")   String noteText     // form body
) { ... }
```

`@BeanParam` agrega múltiplos parâmetros em um único objeto — útil quando o método tem muitos params.

### Content negotiation (`@Produces`/`@Consumes` com media types)

> [!warning] Homônimo: `@Produces` do JAX-RS vs CDI
> `@Produces` existe em dois pacotes distintos e com significados completamente diferentes:
> - `jakarta.ws.rs.Produces` — declara o media type que o método **produz** (HTTP `Content-Type`)
> - `jakarta.enterprise.inject.Produces` — marca um método como **factory de bean CDI** (ver [[06 - CDI — qualifiers, producers e eventos]])
>
> O import errado compila sem erro mas o comportamento em runtime é silenciosamente incorreto. Sempre verifique o import.

```java
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.Consumes;
import jakarta.ws.rs.core.MediaType;

@GET
@Path("/{id}")
@Produces(MediaType.APPLICATION_JSON)        // responde JSON
public OrderDto findById(@PathParam("id") Long id) { ... }

@POST
@Consumes(MediaType.APPLICATION_JSON)        // aceita JSON no body
@Produces(MediaType.APPLICATION_JSON)        // responde JSON
public Response create(OrderDto dto) { ... }

@GET
@Path("/{id}/report")
@Produces({ MediaType.APPLICATION_JSON,
             MediaType.APPLICATION_XML })    // suporta dois formatos
public OrderDto report(@PathParam("id") Long id) { ... }
```

O runtime usa o header `Accept` do request para escolher qual media type retornar quando há múltiplas opções. `@Produces` e `@Consumes` podem ser colocadas na classe (aplica a todos os métodos) ou por método (sobrescreve a classe).

### Respostas (`Response` builder: status, headers, entity; vs retorno direto)

Retornar o tipo diretamente (ex.: `OrderDto`) é a forma simples: o runtime infere status 200 e serializa o objeto. Quando você precisa de controle fino — status customizado, headers de resposta, location — use o `Response` builder.

```java
import jakarta.ws.rs.core.Response;
import jakarta.ws.rs.core.UriInfo;
import jakarta.ws.rs.core.Context;
import java.net.URI;

@POST
@Consumes(MediaType.APPLICATION_JSON)
@Produces(MediaType.APPLICATION_JSON)
public Response create(OrderDto dto, @Context UriInfo uriInfo) {
    Order saved = orderService.save(dto);

    URI location = uriInfo.getAbsolutePathBuilder()
        .path(String.valueOf(saved.getId()))
        .build();

    return Response
        .created(location)               // 201 Created + Location header
        .entity(OrderDto.from(saved))    // body da resposta
        .build();
}

@GET
@Path("/{id}")
@Produces(MediaType.APPLICATION_JSON)
public Response findById(@PathParam("id") Long id) {
    return orderService.findById(id)
        .map(order -> Response.ok(OrderDto.from(order)).build())
        .orElse(Response.status(Response.Status.NOT_FOUND).build()); // 404
}
```

Constantes úteis: `Response.Status.OK`, `NOT_FOUND`, `BAD_REQUEST`, `CREATED`, `NO_CONTENT`.

### Providers (`MessageBodyReader/Writer` — a ponte objeto↔representação; `ExceptionMapper` — exceção→status; JSON-B/JSON-P; `ContextResolver` em menção)

**Providers** são anotados com `@Provider` e registrados automaticamente pelo runtime.

`MessageBodyReader<T>` converte o corpo HTTP em objeto Java. `MessageBodyWriter<T>` faz o caminho inverso. Na prática, você raramente escreve os seus — **JSON-B** (Jakarta JSON Binding) fornece um `MessageBodyReader/Writer` para JSON que o runtime inclui automaticamente em qualquer container Jakarta EE completo.

**JSON-B** usa o pacote `jakarta.json.bind.*` e serializa/deserializa POJOs por convenção (getters/setters). **JSON-P** (`jakarta.json.*`) oferece uma API de streaming e de árvore (similar ao Jackson JsonNode) para quando você precisa de controle manual.

`ExceptionMapper<E extends Throwable>` traduz exceções para respostas HTTP. É a forma correta de converter exceções de domínio em status codes sem poluir o código dos resource methods.

`ContextResolver<T>` fornece instâncias de contexto customizadas (ex.: um `ObjectMapper` configurado) — é mencionado como extensão avançada; consulte a spec para detalhes.

### Bootstrap e Client API (`Application`/`@ApplicationPath`; `ClientBuilder` para consumir)

**Bootstrap do lado servidor:**

```java
import jakarta.ws.rs.ApplicationPath;
import jakarta.ws.rs.core.Application;

@ApplicationPath("/api")                // todas as rotas ficam sob /api
public class RestApplication extends Application {
    // body vazio: o runtime descobre os resources por scanning
    // ou sobrescreva getClasses()/getSingletons() para registro explícito
}
```

Em Jakarta EE completo, `Application` + `@ApplicationPath` é suficiente — não é necessário nenhum XML adicional.

**Client API — consumir endpoints REST:**

```java
import jakarta.ws.rs.client.ClientBuilder;
import jakarta.ws.rs.client.Client;
import jakarta.ws.rs.client.WebTarget;
import jakarta.ws.rs.core.Response;

Client client = ClientBuilder.newClient();

WebTarget target = client
    .target("https://api.example.com/orders")
    .path("/{id}")
    .resolveTemplate("id", 42);

Response response = target
    .request(MediaType.APPLICATION_JSON)
    .get();

if (response.getStatus() == 200) {
    OrderDto order = response.readEntity(OrderDto.class);
}

client.close();  // libera recursos — importante!
```

`ClientBuilder` é o ponto de entrada. `WebTarget` representa o endpoint (suporta URI templates). `request()` prepara a invocação; `.get()`, `.post()`, `.put()`, `.delete()` a executam.

## Na prática

Exemplo completo: resource + exception mapper + chamada cliente.

```java
package com.example.orders;

import jakarta.inject.Inject;
import jakarta.ws.rs.Consumes;
import jakarta.ws.rs.DELETE;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.POST;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.PathParam;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.core.Context;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;
import jakarta.ws.rs.core.UriInfo;
import java.net.URI;
import java.util.List;

@Path("/orders")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class OrderResource {

    @Inject
    private OrderService orderService;

    /** GET /orders — lista todos */
    @GET
    public List<OrderDto> listAll() {
        return orderService.findAll();
    }

    /** GET /orders/{id} — busca por id; 404 se não encontrar */
    @GET
    @Path("/{id}")
    public Response findById(@PathParam("id") Long id) {
        Order order = orderService.findById(id)
            .orElseThrow(() -> new OrderNotFoundException(id));
        return Response.ok(OrderDto.from(order)).build();
    }

    /** POST /orders — cria; retorna 201 + Location */
    @POST
    public Response create(OrderDto dto, @Context UriInfo uriInfo) {
        Order saved = orderService.create(dto);

        URI location = uriInfo.getAbsolutePathBuilder()
            .path(String.valueOf(saved.getId()))
            .build();

        return Response
            .created(location)
            .entity(OrderDto.from(saved))
            .build();
    }
}
```

```java
package com.example.orders;

import jakarta.ws.rs.core.Response;
import jakarta.ws.rs.ext.ExceptionMapper;
import jakarta.ws.rs.ext.Provider;
import java.util.logging.Logger;

@Provider
public class OrderNotFoundExceptionMapper
        implements ExceptionMapper<OrderNotFoundException> {

    private static final Logger LOG =
        Logger.getLogger(OrderNotFoundExceptionMapper.class.getName());

    @Override
    public Response toResponse(OrderNotFoundException ex) {
        LOG.warning("Order not found: " + ex.getMessage()); // nunca engolir!
        return Response
            .status(Response.Status.NOT_FOUND)
            .entity(new ErrorDto("ORDER_NOT_FOUND", ex.getMessage()))
            .build();
    }
}
```

```java
package com.example.orders;

import jakarta.ws.rs.client.ClientBuilder;
import jakarta.ws.rs.client.Client;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;

public class OrderClient {

    public OrderDto fetchOrder(Long id) {
        Client client = ClientBuilder.newClient();
        try {
            Response response = client
                .target("https://api.example.com/orders/{id}")
                .resolveTemplate("id", id)
                .request(MediaType.APPLICATION_JSON)
                .get();

            if (response.getStatus() == 200) {
                return response.readEntity(OrderDto.class);
            }
            throw new RuntimeException("Unexpected status: " + response.getStatus());
        } finally {
            client.close();
        }
    }
}
```

## Armadilhas

### (1) Esquecer `Application`/`@ApplicationPath` — nada responde

**Problema:** Você escreve os resource classes e sobe o servidor, mas todas as rotas retornam 404. O runtime JAX-RS precisa de um ponto de entrada para descobrir os resources.

```java
// ERRADO: sem Application, o runtime não sabe onde começar
@Path("/orders")
public class OrderResource { ... }
```

**Fix:** Declare uma subclasse de `Application` com `@ApplicationPath`:

```java
import jakarta.ws.rs.ApplicationPath;
import jakarta.ws.rs.core.Application;

@ApplicationPath("/api")
public class RestApplication extends Application { }
// O runtime descobre os resources por classpath scanning automaticamente
```

### (2) `ExceptionMapper` que engole a exceção sem log

**Problema:** O mapper mapeia a exceção para 404 ou 500, mas não loga nada. Em produção, exceções inesperadas somem silenciosamente — impossível diagnosticar.

```java
// ERRADO: exceção engolida, zero rastreabilidade
@Override
public Response toResponse(SomeException ex) {
    return Response.status(500).build();
}
```

**Fix:** Sempre logue antes de retornar a resposta:

```java
// CORRETO
@Override
public Response toResponse(SomeException ex) {
    LOG.severe("Unhandled exception: " + ex.getMessage()); // log primeiro
    return Response.status(500)
        .entity(new ErrorDto("INTERNAL_ERROR", "Unexpected error"))
        .build();
}
```

### (3) Import errado do `@Produces` — CDI no lugar do JAX-RS

**Problema:** O IDE autocompleta `@Produces` com o import do CDI (`jakarta.enterprise.inject.Produces`). O código compila normalmente, mas o método não declara o media type — o runtime usa negociação de conteúdo padrão (ou falha com erro 500 de serialização).

```java
import jakarta.enterprise.inject.Produces; // ERRADO para resource JAX-RS

@GET
@Produces(MediaType.APPLICATION_JSON)       // @Produces do CDI não faz isso
public OrderDto findById(...) { ... }
```

**Fix:** Confirme o import correto:

```java
import jakarta.ws.rs.Produces;             // CORRETO para resource JAX-RS

@GET
@Produces(MediaType.APPLICATION_JSON)
public OrderDto findById(...) { ... }
```

Regra prática: em classes anotadas com `@Path`, todos os imports devem ser `jakarta.ws.rs.*`.

### (4) Retornar entidade JPA crua — acoplamento e armadilhas de serialização

**Problema:** Retornar a entidade JPA diretamente no resource expõe o modelo de dados interno, cria acoplamento forte entre a API e o banco, e frequentemente causa problemas de serialização com relacionamentos lazy (o JSON-B tenta serializar coleções que não foram carregadas).

```java
// ERRADO: entidade JPA exposta diretamente
@GET
@Path("/{id}")
@Produces(MediaType.APPLICATION_JSON)
public Order findById(@PathParam("id") Long id) {
    return orderRepository.find(id); // Order é uma @Entity JPA
}
```

**Fix:** Sempre use DTOs como fronteira da API:

```java
// CORRETO: DTO como fronteira — isolamento e controle
@GET
@Path("/{id}")
@Produces(MediaType.APPLICATION_JSON)
public OrderDto findById(@PathParam("id") Long id) {
    Order order = orderRepository.find(id);
    return OrderDto.from(order); // converte explicitamente
}
```

DTOs definem exatamente o que a API expõe — nada mais, nada menos.

## Em entrevista

### Frase pronta (inglês)

"JAX-RS is the Jakarta EE specification for building RESTful services using a declarative annotation model — you annotate resource classes with `@Path` and HTTP verb annotations, and the runtime handles request routing, parameter binding, and content negotiation. Providers like `MessageBodyReader` and `ExceptionMapper` are the extension points that explain how JSON gets converted to Java objects and how domain exceptions become proper HTTP responses. Knowing the spec means I can reason about what happens under the hood regardless of which implementation — Jersey, RESTEasy, or a framework like Quarkus that sits on top of JAX-RS."

### Vocabulário

| Termo PT | Termo EN |
|---|---|
| Classe de recurso | Resource class |
| Negociação de conteúdo | Content negotiation |
| Mapeador de exceção | Exception mapper |
| Leitor/escritor de corpo de mensagem | Message body reader/writer |
| Template de URI | URI template |
| Parâmetro de caminho | Path parameter |
| Parâmetro de query | Query parameter |
| Provedor | Provider |
| Caminho da aplicação | Application path |
| API de cliente | Client API |

## Veja também

- [[03 - Servlet API — o alicerce HTTP]]
- [[06 - CDI — qualifiers, producers e eventos]]
- [[08 - Bean Validation]]
- [[09 - JPA — a especificação de persistência]]
- [[03-Dominios/Tecnologia/Java/Jakarta EE/index|Jakarta EE (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#JAX-RS (Jakarta RESTful Web Services)|JAX-RS (Dicionário)]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#ExceptionMapper|ExceptionMapper (Dicionário)]]

## Referências

- Jakarta RESTful Web Services 4.0 — especificação oficial: <https://jakarta.ee/specifications/restful-ws/4.0/> (acesso 2026-06-07)
- Javadoc `jakarta.ws.rs`: <https://jakarta.ee/specifications/restful-ws/4.0/apidocs/jakarta.ws.rs/jakarta/ws/rs/package-summary> (acesso 2026-06-07)
- Javadoc Client API `jakarta.ws.rs.client`: <https://jakarta.ee/specifications/restful-ws/4.0/apidocs/jakarta.ws.rs/jakarta/ws/rs/client/package-summary> (acesso 2026-06-07)
- Eclipse Jersey 4.0 (impl de referência): <https://eclipse-ee4j.github.io/jersey/> (acesso 2026-06-07)
- RESTEasy 7.0 (impl Red Hat/WildFly): <https://resteasy.dev/> (acesso 2026-06-07)
