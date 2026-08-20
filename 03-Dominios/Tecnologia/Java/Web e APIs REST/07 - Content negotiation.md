---
title: "Content negotiation"
created: 2026-06-08
updated: 2026-06-08
type: concept
progress: backlog
status: seedling
publish: true
fase: Adepto
tags:
  - java
  - web
  - adepto
  - json
aliases:
  - "Negociação de conteúdo"
---

# Content negotiation

> [!abstract] TL;DR
> Content negotiation é o mecanismo pelo qual o Spring decide **em qual formato serializar a resposta** — JSON, XML, texto puro etc. O cliente declara o que aceita via header `Accept`; o handler declara o que produz via atributo `produces`; o Spring encontra a interseção usando uma cadeia de `HttpMessageConverter`. Quando a interseção está vazia o resultado é um **406 Not Acceptable** (nada agrada o cliente) ou um **415 Unsupported Media Type** (o corpo da requisição não é suportado). Entender esse fluxo é o que separa quem depura esses erros em segundos de quem passa horas no stack trace.

## O que é

**Content negotiation** (negociação de conteúdo) é o processo pelo qual cliente e servidor concordam sobre o formato dos dados trocados em uma requisição HTTP.

O protocolo HTTP define dois vetores de negociação:

| Direção | Header HTTP | Exemplo |
|---|---|---|
| Cliente → Servidor (resposta) | `Accept` | `Accept: application/json` |
| Cliente → Servidor (requisição) | `Content-Type` | `Content-Type: application/json` |

No Spring MVC, o foco principal está no lado da **resposta**: dado que o handler retorna um objeto Java, qual representação serializada deve ser enviada ao cliente?

A decisão envolve três atores:
- O **cliente**, que anuncia preferências via `Accept`
- O **handler**, que declara capacidades via `produces`
- O **`HttpMessageConverter`**, que efetivamente realiza a serialização

## Por que importa

- **Erros 406/415 são frequentes em APIs REST** e confusos sem conhecimento do mecanismo.
- **Múltiplos clientes, múltiplos formatos**: uma API pode servir JSON para frontends e XML para sistemas legados — sem duplicar endpoints.
- **Segurança**: a estratégia baseada em extensão de arquivo (`/orders.json`) foi desativada por padrão no Spring 5.3 por vulnerabilidade de *Reflected File Download* (RFD). Quem não sabe disso fica procurando por que o endpoint "parou de funcionar".
- **Compatibilidade de bibliotecas**: adicionar `jackson-dataformat-xml` ao classpath habilita XML silenciosamente; o comportamento muda sem aviso explícito no código.

## Como funciona

### Como o Spring escolhe a representação (Accept header e produces)

O fluxo de decisão ocorre no `AbstractMessageConverterMethodProcessor`, chamado durante o processamento da resposta do handler:

1. **Coletar tipos aceitos pelo cliente**: lê o header `Accept` da requisição. `Accept: */*` significa "qualquer coisa".
2. **Coletar tipos produzíveis pelo handler**: lê o atributo `produces` da anotação de mapeamento (ex.: `@GetMapping(produces = "application/json")`). Se `produces` estiver ausente, todos os converters registrados são considerados.
3. **Calcular a interseção** entre os dois conjuntos, ordenada por especificidade e por `q` (quality factor).
4. **Selecionar o melhor tipo** e delegar ao `HttpMessageConverter` capaz de escrevê-lo.

```java
// Handler sem produces → Spring usa o Accept do cliente
@GetMapping("/products/{id}")
public Product getProduct(@PathVariable Long id) {
    return productService.findById(id);
}

// Handler com produces explícito → Spring rejeita Accept incompatível com 406
@GetMapping(value = "/products/{id}", produces = MediaType.APPLICATION_JSON_VALUE)
public Product getProductJson(@PathVariable Long id) {
    return productService.findById(id);
}
```

### ContentNegotiationStrategy (header vs param vs path-extension desativada)

O Spring abstrai as diferentes formas de descobrir o tipo desejado por meio da interface `ContentNegotiationStrategy`. O `ContentNegotiationManager` agrega várias estratégias, consultadas em ordem até que uma retorne resultado:

| Estratégia | Como funciona | Status padrão (Spring 6.x / Boot 3.x) |
|---|---|---|
| `HeaderContentNegotiationStrategy` | Lê o header `Accept` | **Ativa** (padrão) |
| `ParameterContentNegotiationStrategy` | Usa query param `?format=json` | Desativada; ativar via `configurer.favorParameter(true)` |
| `PathExtensionContentNegotiationStrategy` | Detecta extensão na URL (`/orders.json`) | **Desativada** por padrão desde Spring 5.3 (RFD) |
| `FixedContentNegotiationStrategy` | Tipo fixo configurado no servidor | Raramente usada |

Para ativar a estratégia de parâmetro (alternativa segura à extensão):

```java
@Configuration
public class WebConfig implements WebMvcConfigurer {

    @Override
    public void configureContentNegotiation(ContentNegotiationConfigurer configurer) {
        configurer
            .favorParameter(true)           // ativa ?format=json
            .parameterName("format")        // nome do parâmetro
            .mediaType("json", MediaType.APPLICATION_JSON)
            .mediaType("xml", MediaType.APPLICATION_XML);
    }
}
```

### A cadeia de HttpMessageConverter e os erros 406/415

`HttpMessageConverter<T>` é a interface que converte objetos Java em bytes (e vice-versa). Cada implementação declara:
- `getSupportedMediaTypes()` — tipos que suporta
- `canWrite(Class, MediaType)` — se consegue serializar aquele tipo Java naquele media type
- `write(T, MediaType, HttpOutputMessage)` — realiza a serialização

Converters registrados por padrão no Boot 3.x (com jackson no classpath):

| Converter | Tipos suportados |
|---|---|
| `MappingJackson2HttpMessageConverter` | `application/json`, `application/*+json` |
| `StringHttpMessageConverter` | `text/plain`, `*/*` |
| `ByteArrayHttpMessageConverter` | `application/octet-stream` |
| `ResourceHttpMessageConverter` | `*/*` (para `Resource`) |
| `MappingJackson2XmlHttpMessageConverter` | `application/xml` (se `jackson-dataformat-xml` presente) |

**406 Not Acceptable**: nenhum converter consegue produzir um tipo que satisfaça o `Accept` do cliente. Spring retorna 406 sem corpo.

**415 Unsupported Media Type**: o `Content-Type` do corpo da requisição (`@RequestBody`) não é suportado por nenhum converter que possa ler aquele tipo Java. Spring retorna 415.

## Na prática

Cenário: endpoint que retorna um produto; cliente pode pedir JSON ou, se XML estiver disponível, XML.

```java
@RestController
@RequestMapping("/api/products")
public class ProductController {

    private final ProductService productService;

    public ProductController(ProductService productService) {
        this.productService = productService;
    }

    // Aceita qualquer formato que o Spring consiga produzir
    @GetMapping("/{id}")
    public Product getProduct(@PathVariable Long id) {
        return productService.findById(id);
    }

    // Restrito a JSON — qualquer outro Accept retorna 406
    @GetMapping(value = "/{id}/json", produces = MediaType.APPLICATION_JSON_VALUE)
    public Product getProductJson(@PathVariable Long id) {
        return productService.findById(id);
    }

    // Suporta JSON e XML explicitamente
    @GetMapping(
        value = "/{id}/negotiated",
        produces = { MediaType.APPLICATION_JSON_VALUE, MediaType.APPLICATION_XML_VALUE }
    )
    public Product getProductNegotiated(@PathVariable Long id) {
        return productService.findById(id);
    }
}
```

Chamadas via `curl` para testar cada cenário:

```bash
# Pede JSON — resposta: 200 application/json
curl -H "Accept: application/json" http://localhost:8080/api/products/1

# Pede XML (se jackson-dataformat-xml no classpath) — resposta: 200 application/xml
curl -H "Accept: application/xml" http://localhost:8080/api/products/1

# Pede tipo inexistente — resposta: 406 Not Acceptable
curl -H "Accept: application/pdf" http://localhost:8080/api/products/1/json

# Accept wildcard — Spring escolhe o tipo preferido (JSON normalmente)
curl -H "Accept: */*" http://localhost:8080/api/products/1

# Enviando JSON no corpo (POST) com Content-Type incorreto — resposta: 415
curl -X POST -H "Content-Type: text/plain" \
     -d '{"name":"Widget"}' \
     http://localhost:8080/api/products
```

## Armadilhas

### (1) Depender de extensão de arquivo na URL

**Problema**: código legado ou tutoriais antigos usam `/orders.json` ou `/orders.xml` para selecionar o formato. A partir do Spring 5.3, a `PathExtensionContentNegotiationStrategy` está desativada por padrão.

**Sintoma**: endpoint responde normalmente para `/orders` mas retorna 404 para `/orders.json`, ou ignora a extensão e retorna o tipo padrão independente da extensão.

**Fix**: migrar para o header `Accept` (preferencial) ou ativar a estratégia de parâmetro (`?format=json`). Nunca reativar a estratégia de extensão em produção.

```java
// EVITE — comportamento não garantido no Spring 6.x
GET /orders.json HTTP/1.1

// PREFIRA — semântica clara e segura
GET /orders HTTP/1.1
Accept: application/json
```

### (2) produces incompatível com o Accept do cliente → 406

**Problema**: o handler declara `produces = "application/json"` mas o cliente envia `Accept: application/xml`. Ou o cliente envia `Accept: text/html` (navegador) e o handler só produz JSON.

**Sintoma**: resposta 406 sem corpo; no log aparece `No acceptable representation`.

**Fix**: alinhar o `produces` com os tipos que a API realmente suporta e documentar isso (OpenAPI). Para APIs consumidas por navegadores, garantir que o cliente inclua `application/json` no `Accept` ou usar `Accept: */*`.

```java
// Causa 406 quando Accept: application/xml
@GetMapping(value = "/orders", produces = MediaType.APPLICATION_JSON_VALUE)
public List<Order> listOrders() { ... }

// Evita 406 ao suportar ambos
@GetMapping(
    value = "/orders",
    produces = { MediaType.APPLICATION_JSON_VALUE, MediaType.APPLICATION_XML_VALUE }
)
public List<Order> listOrders() { ... }
```

### (3) Assumir JSON quando há um converter de XML no classpath

**Problema**: ao adicionar `jackson-dataformat-xml` (ou `spring-boot-starter-data-rest` que o inclui), o Spring registra `MappingJackson2XmlHttpMessageConverter`. Se o cliente enviar `Accept: application/xml` — ou `Accept: */*` com preferência XML declarada via `q` — a resposta pode chegar em XML inesperadamente.

**Sintoma**: testes unitários passam (mocados com JSON), mas testes de integração ou clientes reais recebem XML; deserialização falha no cliente que esperava JSON.

**Fix**: usar `produces = MediaType.APPLICATION_JSON_VALUE` nos endpoints que devem sempre retornar JSON, tornando explícita a intenção e evitando que um novo converter no classpath altere o comportamento.

```java
// FRÁGIL — comportamento muda se XML converter for adicionado ao classpath
@GetMapping("/orders")
public List<Order> listOrders() { ... }

// EXPLÍCITO — sempre JSON, independente do classpath
@GetMapping(value = "/orders", produces = MediaType.APPLICATION_JSON_VALUE)
public List<Order> listOrders() { ... }
```

## Em entrevista

### Frase pronta (inglês)

"Content negotiation in Spring MVC is the process by which the framework resolves the media type for an HTTP response. The default strategy relies on the `Accept` request header; the handler further constrains the options through the `produces` attribute on the mapping annotation. Spring then walks the registered `HttpMessageConverter` chain, picks the first converter that can write the negotiated type, and serializes the return value — returning a 406 if no match is found, or a 415 if the request body's `Content-Type` is unsupported. One important detail for interviews: path-extension-based negotiation (e.g., `/orders.json`) was disabled by default in Spring 5.3 due to Reflected File Download vulnerabilities, so the recommended alternatives are the `Accept` header or the query-parameter strategy."

### Vocabulário

| Termo PT | Termo EN |
|---|---|
| Negociação de conteúdo | Content negotiation |
| Conversor de mensagem | `HttpMessageConverter` |
| Tipo de mídia | Media type |
| Cabeçalho de aceitação | `Accept` header |
| Não aceitável | 406 Not Acceptable |
| Tipo de mídia não suportado | 415 Unsupported Media Type |
| Estratégia de negociação | `ContentNegotiationStrategy` |
| Gerenciador de negociação | `ContentNegotiationManager` |
| Extensão de caminho (desativada) | Path extension (disabled) |
| Estratégia de parâmetro | Parameter strategy (`?format=`) |

## Veja também

- [[03-Dominios/Tecnologia/Java/Web e APIs REST/05 - Serialização JSON com Jackson|Serialização JSON com Jackson]]
- [[03-Dominios/Tecnologia/Java/Web e APIs REST/06 - O pipeline do DispatcherServlet|O pipeline do DispatcherServlet]]
- [[03-Dominios/Tecnologia/Java/Web e APIs REST/index|Web e APIs REST]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- Verbetes: [[03-Dominios/Tecnologia/Java/Dicionário de Java#content negotiation|content negotiation]], [[03-Dominios/Tecnologia/Java/Dicionário de Java#HttpMessageConverter|HttpMessageConverter]]

## Referências

- Spring Framework 6.x — Content Negotiation Config: https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-config/content-negotiation.html
- Spring Framework 6.x — @ResponseBody: https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-controller/ann-methods/responsebody.html
