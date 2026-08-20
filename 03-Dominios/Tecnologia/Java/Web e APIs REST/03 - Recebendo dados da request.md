---
title: "Recebendo dados da request"
created: 2026-06-08
updated: 2026-06-08
type: concept
progress: backlog
status: seedling
publish: true
fase: Iniciado
tags:
  - java
  - web
  - iniciado
  - controller
aliases:
  - "Request binding no Spring MVC"
---

# Recebendo dados da request

> [!abstract] TL;DR
> Um handler recebe dados da requisição HTTP através de anotações específicas: `@PathVariable` extrai segmentos dinâmicos da URL (`/orders/{id}`), `@RequestParam` captura parâmetros de query string ou formulários (com `required`/`defaultValue` para controlar obrigatoriedade), `@RequestBody` desserializa o corpo JSON para um objeto Java via `HttpMessageConverter`, e `@RequestHeader` acessa cabeçalhos HTTP. Para uploads multipart, `@RequestPart` combina arquivo e metadados JSON em uma única requisição.

## O que é

Quando o Spring MVC despacha uma requisição para um método handler, ele precisa extrair dados de diferentes partes do protocolo HTTP — a URL, a query string, o corpo, os cabeçalhos — e converter esses dados brutos (sempre `String` no nível HTTP) para os tipos Java declarados no método. Esse processo se chama **request binding** (ou *parameter binding*).

O binding é feito por anotações que funcionam como instruções de montagem para o framework:

| Anotação | De onde lê | Exemplo |
| --- | --- | --- |
| `@PathVariable` | Segmento da URL (`/orders/{id}`) | `id` em `GET /orders/42` |
| `@RequestParam` | Query string ou form data | `?page=2&size=10` |
| `@RequestBody` | Corpo da requisição (JSON/XML) | Payload de `POST /orders` |
| `@RequestHeader` | Cabeçalhos HTTP | `Authorization`, `Accept-Language` |
| `@RequestPart` | Parte de multipart/form-data | Arquivo + JSON no mesmo form |

O Spring Boot 3.x / Spring Framework 6.x usa `jakarta.*` em vez de `javax.*` (migração para Jakarta EE 10). Todos os exemplos abaixo seguem essa convenção.

## Por que importa

- **Todo endpoint precisa de dados.** Sem binding, um controller seria apenas uma casca vazia que ignora a requisição. Saber qual anotação usar para cada parte do HTTP é o alfabeto do desenvolvimento web com Spring.
- **Erros de binding são 400 Bad Request.** Se um `@RequestParam` obrigatório não chega, ou o JSON do corpo não desserializa, o Spring retorna 400 automaticamente — entender as regras do binding é entender por que seus endpoints falham.
- **Entrevistas técnicas.** "Qual a diferença entre `@PathVariable` e `@RequestParam`?" é uma das perguntas mais frequentes em triagens de back-end Java. A resposta correta exige saber de onde cada um lê, o que acontece quando o parâmetro está ausente e como configurar valores padrão.
- **Integração com Jackson.** O `@RequestBody` não é mágica — ele delega para um `HttpMessageConverter` (no caso de JSON, o `MappingJackson2HttpMessageConverter`). Entender essa cadeia ajuda a depurar problemas de desserialização.

## Como funciona

### Path e query: @PathVariable e @RequestParam (required/defaultValue)

**`@PathVariable`** extrai um segmento variável do path da URL, declarado com `{}` no mapeamento:

```java
@GetMapping("/orders/{id}")
public OrderResponse getOrder(@PathVariable Long id) {
    return orderService.findById(id);
}
```

O Spring converte automaticamente o segmento (`String` no nível HTTP) para o tipo declarado (`Long` aqui). Se o nome do parâmetro Java for diferente do nome entre chaves, o mapeamento deve ser explícito:

```java
@GetMapping("/orders/{orderId}")
public OrderResponse getOrder(@PathVariable("orderId") Long id) {
    return orderService.findById(id);
}
```

Por padrão, variáveis de path são **obrigatórias** — a URL simplesmente não corresponde à rota se o segmento estiver ausente. Para variáveis opcionais, use `required = false` junto com `Optional<T>`:

```java
@GetMapping({"/orders/{id}", "/orders"})
public OrderResponse getOrder(@PathVariable(required = false) Long id) {
    return id != null ? orderService.findById(id) : orderService.findLatest();
}
```

---

**`@RequestParam`** lê parâmetros da query string (`?key=value`) ou de formulários `application/x-www-form-urlencoded`:

```java
// Ambos os parâmetros são obrigatórios por padrão (required = true)
@GetMapping("/products")
public List<ProductResponse> list(
        @RequestParam String category,
        @RequestParam int page) {
    return productService.findByCategory(category, page);
}
```

Para parâmetros **opcionais**, use `required = false` ou forneça um `defaultValue` (que implica `required = false` automaticamente):

```java
@GetMapping("/products")
public List<ProductResponse> list(
        @RequestParam(defaultValue = "0") int page,
        @RequestParam(defaultValue = "10") int size,
        @RequestParam(required = false) String category) {
    return productService.list(page, size, category);
}
```

> [!info] Conversão de tipo automática
> O Spring converte strings para `int`, `Long`, `boolean`, `LocalDate` e outros tipos automaticamente usando os `Converter` e `Formatter` registrados. Para tipos personalizados, registre um `Converter<String, MeuTipo>` no `FormattingConversionService`.

---

### Corpo: @RequestBody (desserialização via converter)

**`@RequestBody`** lê o **corpo inteiro** da requisição HTTP e o converte para o tipo Java declarado. O mecanismo interno é a cadeia de `HttpMessageConverter`: o Spring inspeciona o `Content-Type` da requisição, seleciona o converter adequado (geralmente `MappingJackson2HttpMessageConverter` para `application/json`) e delega a desserialização para o Jackson `ObjectMapper`.

```text
Corpo HTTP (JSON bytes)
  ↓ Content-Type: application/json
  ↓ MappingJackson2HttpMessageConverter
  ↓ Jackson ObjectMapper
Java Object (CreateOrderRequest.class)
```

Usando um **record** Java como DTO (preferível em código moderno):

```java
public record CreateOrderRequest(
    Long customerId,
    List<Long> productIds,
    String shippingAddress
) {}

@PostMapping("/orders")
public OrderResponse createOrder(@RequestBody CreateOrderRequest request) {
    return orderService.create(request);
}
```

Para adicionar validação de Bean Validation, combine com `@Valid`:

```java
public record CreateOrderRequest(
    @NotNull Long customerId,
    @NotEmpty List<Long> productIds,
    @NotBlank String shippingAddress
) {}

@PostMapping("/orders")
public OrderResponse createOrder(@RequestBody @Valid CreateOrderRequest request) {
    return orderService.create(request);
}
```

Se a validação falhar, o Spring lança `MethodArgumentNotValidException` (que resulta em 400).

---

### Headers e multipart: @RequestHeader, @RequestPart

**`@RequestHeader`** acessa cabeçalhos HTTP individuais:

```java
@GetMapping("/products")
public List<ProductResponse> list(
        @RequestHeader("Accept-Language") String acceptLanguage,
        @RequestHeader(value = "X-Request-ID", required = false) String requestId) {
    return productService.listLocalized(acceptLanguage);
}
```

Para acessar **todos** os cabeçalhos de uma vez, declare o parâmetro como `HttpHeaders` ou `Map<String, String>`:

```java
@GetMapping("/debug/headers")
public Map<String, String> echoHeaders(@RequestHeader Map<String, String> headers) {
    return headers;
}
```

---

**`@RequestPart`** é usado em requisições `multipart/form-data`, onde cada parte pode ter seu próprio `Content-Type`. Isso permite enviar um arquivo **e** metadados JSON no mesmo request:

```java
public record ProductMetadata(String name, String description, BigDecimal price) {}

@PostMapping(value = "/products", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
public ProductResponse createWithImage(
        @RequestPart("image") MultipartFile image,
        @RequestPart("metadata") ProductMetadata metadata) {
    return productService.createWithImage(metadata, image);
}
```

> [!tip] @RequestParam vs @RequestPart para arquivos
> `@RequestParam` pode receber um `MultipartFile` para uploads simples. Use `@RequestPart` quando uma das partes precisar ser desserializada com um `HttpMessageConverter` (ex.: JSON) — o `@RequestParam` trata tudo como `String` ou `MultipartFile`, sem passar pelo converter chain.

## Na prática

**Cenário 1 — leitura com `@PathVariable` e `@RequestParam`:**

```java
@RestController
@RequestMapping("/orders")
public class OrderController {

    private final OrderService orderService;

    public OrderController(OrderService orderService) {
        this.orderService = orderService;
    }

    // GET /orders/42?includeItems=true
    @GetMapping("/{id}")
    public OrderResponse getOrder(
            @PathVariable Long id,
            @RequestParam(defaultValue = "false") boolean includeItems) {
        return orderService.findById(id, includeItems);
    }
}
```

**Cenário 2 — criação com `@RequestBody` usando record DTO:**

```java
public record CreateOrderRequest(
    @NotNull Long customerId,
    @NotEmpty List<Long> productIds
) {}

public record OrderResponse(Long id, String status, Long customerId) {}

@RestController
@RequestMapping("/orders")
public class OrderController {

    private final OrderService orderService;

    public OrderController(OrderService orderService) {
        this.orderService = orderService;
    }

    // POST /orders
    // Content-Type: application/json
    // Body: { "customerId": 1, "productIds": [10, 11] }
    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public OrderResponse createOrder(@RequestBody @Valid CreateOrderRequest request) {
        return orderService.create(request);
    }
}
```

O record `CreateOrderRequest` é imutável, não precisa de getters explícitos e é desserializado pelo Jackson sem configuração adicional (Jackson 2.12+ suporta records nativamente).

## Armadilhas

### (1) @RequestParam obrigatório sem defaultValue → 400 quando ausente

**O problema:**

```java
// ARMADILHA: se o cliente não enviar ?page=..., o Spring retorna 400
@GetMapping("/products")
public List<ProductResponse> list(@RequestParam int page) {
    return productService.list(page);
}
```

Qualquer chamada a `GET /products` (sem `?page=...`) retorna `400 Bad Request` com a mensagem "Required request parameter 'page' for method parameter type int is not present". Isso é correto conforme a especificação, mas frequentemente inesperado para quem só quer um parâmetro opcional com padrão razoável.

**Fix:**

```java
// CORRETO: parâmetros de paginação quase sempre têm padrões razoáveis
@GetMapping("/products")
public List<ProductResponse> list(
        @RequestParam(defaultValue = "0") int page,
        @RequestParam(defaultValue = "20") int size) {
    return productService.list(page, size);
}
```

Use `defaultValue` para parâmetros que têm um valor sensato quando ausentes, e `required = false` (retornando `null` ou `Optional`) para parâmetros genuinamente opcionais onde a ausência muda a lógica.

---

### (2) Nome do {placeholder} diferente do nome do parâmetro Java

**O problema:**

```java
@GetMapping("/orders/{orderId}")
// ARMADILHA: placeholder é "orderId" mas o parâmetro se chama "id"
public OrderResponse getOrder(@PathVariable Long id) {
    return orderService.findById(id);
}
```

Isso lança `IllegalStateException` em tempo de execução (ou `MissingPathVariableException`): o Spring procura um template variable chamado `id` na URL, mas o mapeamento declara `orderId`.

> [!warning] Compilação com -parameters
> Em alguns cenários (especialmente com AOT no Spring Boot 3.x ou classes sem informação de debug), o Spring pode não conseguir inferir o nome do parâmetro via reflexão. O comportamento varia conforme as flags de compilação.

**Fix:** sempre seja explícito quando os nomes diferem:

```java
@GetMapping("/orders/{orderId}")
public OrderResponse getOrder(@PathVariable("orderId") Long id) {
    return orderService.findById(id);
}
```

Ou, melhor ainda, mantenha os nomes consistentes:

```java
@GetMapping("/orders/{id}")
public OrderResponse getOrder(@PathVariable Long id) {
    return orderService.findById(id);
}
```

---

### (3) @RequestBody em um método GET (sem corpo)

**O problema:**

```java
// ARMADILHA: GET não tem corpo — a spec HTTP desencoraja body em GET
@GetMapping("/orders/search")
public List<OrderResponse> search(@RequestBody SearchCriteria criteria) {
    return orderService.search(criteria);
}
```

Requisições `GET` tecnicamente *podem* ter corpo (a spec HTTP não proíbe), mas a maioria dos clientes, proxies e ferramentas **ignora ou rejeita** o corpo de um GET. O Spring pode até ler o corpo, mas o comportamento é não-determinístico dependendo do servidor HTTP subjacente (Tomcat, Netty) e do cliente.

**Fix:** use `@RequestParam` para critérios simples em GETs, ou mude para `POST` se o payload for complexo:

```java
// Para critérios simples — use @RequestParam
@GetMapping("/orders/search")
public List<OrderResponse> search(
        @RequestParam(required = false) String status,
        @RequestParam(required = false) Long customerId) {
    return orderService.search(status, customerId);
}

// Para critérios complexos — use POST (padrão "search endpoint")
@PostMapping("/orders/search")
public List<OrderResponse> search(@RequestBody SearchCriteria criteria) {
    return orderService.search(criteria);
}
```

## Em entrevista

### Frase pronta (inglês)

> "In Spring MVC, handler methods receive request data through binding annotations: `@PathVariable` extracts URI template segments — the `{id}` placeholders in the mapping — while `@RequestParam` reads query string or form parameters, with `required` and `defaultValue` attributes to control whether absence causes a 400 or falls back to a sensible default. `@RequestBody` reads the entire request body and delegates deserialization to an `HttpMessageConverter` — typically Jackson's `MappingJackson2HttpMessageConverter` for JSON — so a plain record DTO just works out of the box in Boot 3.x. For headers, `@RequestHeader` gives direct access with the same required/defaultValue semantics. One thing I always flag in reviews is the name mismatch pitfall: if the path template uses `{orderId}` but the parameter is named `id`, Spring throws at runtime — so I keep the names consistent or always pass the name explicitly to the annotation."

### Vocabulário

| Termo PT | Termo EN |
| --- | --- |
| Vinculação de parâmetros | Request/parameter binding |
| Segmento de caminho | Path segment / URI template variable |
| Parâmetro de query | Query parameter / query string parameter |
| Corpo da requisição | Request body |
| Conversor de mensagem HTTP | `HttpMessageConverter` |
| Desserialização | Deserialization |
| Parâmetro obrigatório | Required parameter |
| Valor padrão | Default value |
| Dados multipart | Multipart form data |
| Cabeçalho HTTP | HTTP request header |

## Veja também

- [[03-Dominios/Tecnologia/Java/Web e APIs REST/02 - @RestController e os mapeamentos|@RestController e os mapeamentos]]
- [[03-Dominios/Tecnologia/Java/Web e APIs REST/05 - Serialização JSON com Jackson|Serialização JSON com Jackson]]
- [[03-Dominios/Tecnologia/Java/Jakarta EE/07 - JAX-RS — REST declarativo|JAX-RS]] (@PathParam/@QueryParam — os params tipados da spec)
- [[03-Dominios/Tecnologia/Java/Web e APIs REST/index|Web e APIs REST]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- Verbetes: [[03-Dominios/Tecnologia/Java/Dicionário de Java#@PathVariable|@PathVariable]], [[03-Dominios/Tecnologia/Java/Dicionário de Java#@RequestParam|@RequestParam]], [[03-Dominios/Tecnologia/Java/Dicionário de Java#@RequestBody|@RequestBody]], [[03-Dominios/Tecnologia/Java/Dicionário de Java#@RequestHeader|@RequestHeader]]

## Referências

- Spring Framework Reference — *Annotated Controllers: Handler Methods — Method Arguments*: <https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-controller/ann-methods/arguments.html>
- Spring Framework Reference — *@PathVariable*: <https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-controller/ann-methods/arguments.html#mvc-ann-arguments>
- Spring Framework Reference — *@RequestBody*: <https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-controller/ann-methods/requestbody.html>
- Spring Framework Reference — *@RequestHeader*: <https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-controller/ann-methods/requestheader.html>
- Spring Framework Reference — *Multipart Forms*: <https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-controller/ann-methods/multipart-forms.html>
- Spring Framework Reference — *HTTP Message Converters*: <https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-config/message-converters.html>
