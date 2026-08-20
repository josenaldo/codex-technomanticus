---
title: "@RestController e os mapeamentos"
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
  - rest
aliases:
  - "@RestController"
---

# @RestController e os mapeamentos

> [!abstract] TL;DR
> `@RestController` marca a classe como handler REST: é a combinação de `@Controller` (registra o bean como handler HTTP) com `@ResponseBody` (serializa o retorno direto no corpo da resposta, sem passar por view resolver). `@GetMapping`, `@PostMapping`, `@PutMapping`, `@DeleteMapping` e `@PatchMapping` são atalhos para `@RequestMapping(method = …)` que mapeiam métodos a pares URL + verbo HTTP. O atributo `path` define a URL; `produces`/`consumes` restringem os media types aceitos e produzidos; `params`/`headers` adicionam condições extras sobre parâmetros de query e cabeçalhos.

## O que é

`@RestController` é uma **anotação composta** introduzida no Spring 4 que reúne duas responsabilidades em uma só declaração:

| Componente | Papel |
|---|---|
| `@Controller` | Declara a classe como um bean Spring e a registra no `DispatcherServlet` como handler de requisições HTTP |
| `@ResponseBody` | Instrui o Spring a serializar o valor de retorno de cada método diretamente no corpo da resposta HTTP (por padrão, como JSON via Jackson) |

Sem `@ResponseBody`, o Spring MVC tentaria interpretar a `String` retornada como o nome de uma **view** (um template Thymeleaf, por exemplo), o que gera erros em APIs REST puras.

`@RequestMapping` é a anotação base que define os critérios de correspondência de uma requisição HTTP a um método Java. Seus **atalhos por verbo** são anotações compostas meta-anotadas com `@RequestMapping`:

| Atalho | Equivalente |
|---|---|
| `@GetMapping` | `@RequestMapping(method = RequestMethod.GET)` |
| `@PostMapping` | `@RequestMapping(method = RequestMethod.POST)` |
| `@PutMapping` | `@RequestMapping(method = RequestMethod.PUT)` |
| `@DeleteMapping` | `@RequestMapping(method = RequestMethod.DELETE)` |
| `@PatchMapping` | `@RequestMapping(method = RequestMethod.PATCH)` |

## Por que importa

APIs REST são o contrato público de praticamente todo serviço backend moderno. `@RestController` e os mapeamentos são o ponto de entrada de cada operação: errar o verbo, a URL ou o media type significa errar a API antes mesmo de chegar na lógica de negócio.

Do ponto de vista de entrevista sênior, as perguntas mais frequentes nessa área são:

- "Qual a diferença entre `@Controller` e `@RestController`?" — A presença implícita de `@ResponseBody`.
- "Por que usar `@GetMapping` em vez de `@RequestMapping(method = GET)`?" — É mais legível, expressivo e menos verboso; é o estilo recomendado desde Spring 4.3.
- "`produces` e `consumes` afetam roteamento ou só serialização?" — Afetam o **roteamento**: uma requisição sem o `Content-Type` correto recebe `415 Unsupported Media Type` antes de chegar ao método.

## Como funciona

### @Controller vs @RestController (view vs body)

Em Spring MVC o fluxo padrão de um `@Controller` é:

1. O método do controller retorna uma `String` (nome da view) ou um `ModelAndView`.
2. O `ViewResolver` localiza o template correspondente.
3. O template é renderizado e enviado como HTML.

Com `@ResponseBody` (ou `@RestController`), o fluxo muda:

1. O método retorna um objeto Java (POJO, `ResponseEntity`, `List`, etc.).
2. Um `HttpMessageConverter` (geralmente Jackson) serializa o objeto para JSON/XML.
3. O payload serializado é escrito diretamente no corpo da resposta.

Não existe view resolver envolvido. O `Content-Type` da resposta é determinado pelo `Accept` do cliente e pelo atributo `produces` do mapeamento.

### @RequestMapping e os atalhos por verbo HTTP

`@RequestMapping` pode ser aplicado no nível da **classe** (prefixo de rota comum) e no nível do **método** (rota e verbo específicos):

```java
@RestController
@RequestMapping("/orders")          // prefixo comum para todos os métodos
public class OrderController {

    @GetMapping                     // GET /orders
    public List<Order> listAll() { … }

    @GetMapping("/{id}")            // GET /orders/{id}
    public Order findById(@PathVariable Long id) { … }

    @PostMapping                    // POST /orders
    @ResponseStatus(HttpStatus.CREATED)
    public Order create(@RequestBody Order order) { … }

    @PutMapping("/{id}")            // PUT /orders/{id}
    public Order replace(@PathVariable Long id, @RequestBody Order order) { … }

    @PatchMapping("/{id}/status")   // PATCH /orders/{id}/status
    public Order updateStatus(@PathVariable Long id,
                               @RequestBody StatusUpdate update) { … }

    @DeleteMapping("/{id}")         // DELETE /orders/{id}
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void delete(@PathVariable Long id) { … }
}
```

A URL final de cada método é a concatenação do `path` da classe com o `path` do método.

### Atributos: path, method, produces/consumes, params/headers

**`path`** (alias: `value`) — padrão de URL. Suporta variáveis de template (`{id}`), wildcards (`*`, `**`) e expressões regex (`{version:\\d+\\.\\d+}`):

```java
@GetMapping("/products/{id}")           // variável simples
@GetMapping("/files/**")                // qualquer subpath
@GetMapping("/v{version:\\d+}/orders")  // versão numérica na URL
```

**`method`** — verbo(s) HTTP aceitos. Os atalhos fazem isso implicitamente; use `@RequestMapping(method = {RequestMethod.GET, RequestMethod.HEAD})` quando precisar de múltiplos verbos no mesmo mapeamento.

**`produces`** — restringe o mapeamento ao `Accept` do cliente. A requisição só é roteada para o método se o cliente aceitar um dos media types declarados:

```java
@GetMapping(path = "/orders/{id}", produces = "application/json")
public Order findById(@PathVariable Long id) { … }

// Ou usando constante:
@GetMapping(path = "/orders/{id}", produces = MediaType.APPLICATION_JSON_VALUE)
public Order findById(@PathVariable Long id) { … }
```

Se nenhum método for compatível com o `Accept`, o Spring retorna `406 Not Acceptable`.

**`consumes`** — restringe o mapeamento ao `Content-Type` do corpo enviado pelo cliente. Essencial para `POST`/`PUT`/`PATCH`:

```java
@PostMapping(path = "/orders", consumes = MediaType.APPLICATION_JSON_VALUE)
public Order create(@RequestBody Order order) { … }
```

Se o `Content-Type` não bater, o Spring retorna `415 Unsupported Media Type`.

**`params`** — filtra por parâmetros de query. Raramente usado em REST puro, mas útil para versionar por query param ou para feature flags:

```java
@GetMapping(path = "/orders", params = "status=PENDING")
public List<Order> listPending() { … }

@GetMapping(path = "/orders", params = "!status")   // sem param "status"
public List<Order> listAll() { … }
```

**`headers`** — filtra por cabeçalhos HTTP arbitrários (mesma sintaxe de `params`). Para `Content-Type` e `Accept`, prefira `consumes`/`produces`; use `headers` para cabeçalhos customizados:

```java
@GetMapping(path = "/orders", headers = "X-API-Version=2")
public List<OrderV2> listAllV2() { … }
```

> [!note] Precedência de `produces`/`consumes` no nível do método
> Quando declarados no método, **substituem** (não estendem) os valores da classe. Se a classe declara `produces = "application/json"` e o método declara `produces = "application/xml"`, o método aceita apenas XML.

## Na prática

Exemplo completo de um controller de pedidos com os principais mapeamentos:

```java
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping(
    path = "/orders",
    produces = MediaType.APPLICATION_JSON_VALUE
)
public class OrderController {

    private final OrderService orderService;

    public OrderController(OrderService orderService) {
        this.orderService = orderService;
    }

    // GET /orders  — lista todos os pedidos
    @GetMapping
    public List<Order> listAll() {
        return orderService.findAll();
    }

    // GET /orders/{id}  — busca por ID
    @GetMapping("/{id}")
    public ResponseEntity<Order> findById(@PathVariable Long id) {
        return orderService.findById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    // POST /orders  — cria novo pedido
    @PostMapping(consumes = MediaType.APPLICATION_JSON_VALUE)
    @ResponseStatus(HttpStatus.CREATED)
    public Order create(@Valid @RequestBody Order order) {
        return orderService.save(order);
    }

    // PUT /orders/{id}  — substitui pedido inteiro
    @PutMapping(path = "/{id}", consumes = MediaType.APPLICATION_JSON_VALUE)
    public Order replace(@PathVariable Long id,
                         @Valid @RequestBody Order order) {
        return orderService.replace(id, order);
    }

    // PATCH /orders/{id}/status  — atualiza status parcialmente
    @PatchMapping(path = "/{id}/status", consumes = MediaType.APPLICATION_JSON_VALUE)
    public Order updateStatus(@PathVariable Long id,
                               @RequestBody StatusUpdate update) {
        return orderService.updateStatus(id, update.status());
    }

    // DELETE /orders/{id}  — remove pedido
    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void delete(@PathVariable Long id) {
        orderService.delete(id);
    }
}
```

Pontos destacados:
- `produces` declarado na classe aplica a todos os métodos (todos respondem JSON).
- `consumes` declarado em cada método de escrita garante que apenas JSON é aceito no corpo.
- `ResponseEntity` permite controlar o status HTTP dinamicamente (ex.: `404` quando não encontrado).
- Construtor injection (sem `@Autowired` no campo) é o estilo recomendado para beans Spring.

## Armadilhas

### (1) Usar `@Controller` sem `@ResponseBody` em uma API REST

**Problema:** Ao usar `@Controller` puro em um endpoint REST, o Spring MVC interpreta o valor de retorno como um **nome de view**. Se não existir um `ViewResolver` configurado para aquele nome, a aplicação lança `jakarta.servlet.ServletException: Could not resolve view with name '...'` ou retorna `500`.

**Exemplo que falha:**

```java
@Controller
@RequestMapping("/products")
public class ProductController {

    @GetMapping("/{id}")
    public Product findById(@PathVariable Long id) {  // Spring tenta resolver "Product@7f3d..." como view
        return productService.findById(id);
    }
}
```

**Fix:** Trocar `@Controller` por `@RestController`, ou adicionar `@ResponseBody` no método:

```java
@Controller
@RequestMapping("/products")
public class ProductController {

    @GetMapping("/{id}")
    @ResponseBody   // serializa o retorno como JSON
    public Product findById(@PathVariable Long id) {
        return productService.findById(id);
    }
}
```

### (2) Dois métodos com mapeamento ambíguo

**Problema:** Definir dois métodos com o mesmo verbo e o mesmo path gera `IllegalStateException` na inicialização do contexto Spring: `Ambiguous mapping. Cannot map '…' method`.

**Exemplo que falha:**

```java
@GetMapping("/orders")
public List<Order> listAll() { … }

@GetMapping("/orders")          // mesmo verbo + mesmo path → ambiguidade
public List<Order> listActive() { … }
```

**Fix:** Diferenciar os mapeamentos por path, por `params` ou por `headers`:

```java
@GetMapping("/orders")
public List<Order> listAll() { … }

@GetMapping(path = "/orders", params = "active=true")
public List<Order> listActive() { … }
```

Ou, mais idiomático em REST: usar path diferente (`/orders` vs `/orders?active=true` tratado via `@RequestParam` num único método).

### (3) `@PostMapping` sem `consumes` aceitando qualquer `Content-Type`

**Problema:** Sem `consumes`, o Spring aceita qualquer `Content-Type` no corpo. Se o cliente enviar `text/plain` ou `application/x-www-form-urlencoded` por engano, o Jackson pode falhar ao desserializar com `HttpMessageNotReadableException`, retornando `400 Bad Request` com mensagem de erro pouco descritiva. Pior: ambiguidades de mapeamento entre form-encoded e JSON ficam silenciosas.

**Exemplo sem restrição:**

```java
@PostMapping("/orders")
public Order create(@RequestBody Order order) { … }   // aceita qualquer Content-Type
```

**Fix:** Declarar explicitamente `consumes`:

```java
@PostMapping(path = "/orders", consumes = MediaType.APPLICATION_JSON_VALUE)
public Order create(@RequestBody Order order) { … }
```

Agora requisições com `Content-Type` errado recebem `415 Unsupported Media Type` antes de chegar ao método — resposta clara, sem stack trace no log.

## Em entrevista

### Frase pronta (inglês)

"`@RestController` is a composed annotation that combines `@Controller` and `@ResponseBody`, so the return value of each handler method is serialized directly into the HTTP response body — typically as JSON — rather than being resolved as a view name. For routing, `@GetMapping`, `@PostMapping`, and the other shortcuts are composed annotations built on top of `@RequestMapping` that bind a method to a specific HTTP verb and path. The `produces` and `consumes` attributes go further: they narrow the mapping based on the `Accept` and `Content-Type` headers, so if a client sends the wrong content type, Spring rejects the request with `415 Unsupported Media Type` before the method body even runs."

### Vocabulário

| Termo PT | Termo EN |
|---|---|
| Mapeamento de requisição | Request mapping |
| Anotação composta | Composed annotation |
| Corpo da resposta | Response body |
| Resolvedor de view | View resolver |
| Tipo de media (conteúdo) | Media type / Content type |
| Verbo HTTP | HTTP method / HTTP verb |
| Atalho de anotação | Annotation shortcut / shorthand |
| Serialização | Serialization |
| Desserialização | Deserialization |
| Negociação de conteúdo | Content negotiation |

## Veja também

- [[03-Dominios/Tecnologia/Java/Web e APIs REST/01 - O que é Spring MVC — a camada web sobre o container|O que é Spring MVC]]
- [[03-Dominios/Tecnologia/Java/Web e APIs REST/03 - Recebendo dados da request|Recebendo dados da request]]
- [[03-Dominios/Tecnologia/Java/Jakarta EE/07 - JAX-RS — REST declarativo|JAX-RS]] (resource methods da spec — o outro caminho)
- [[03-Dominios/Tecnologia/Java/Spring Core e Boot/03 - Beans e estereótipos — @Component, @Service, @Repository, @Controller|Beans e estereótipos]] (o controller é um estereótipo/bean)
- [[03-Dominios/Tecnologia/Java/Web e APIs REST/index|Web e APIs REST]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- Verbetes: [[03-Dominios/Tecnologia/Java/Dicionário de Java#@RestController|@RestController]], [[03-Dominios/Tecnologia/Java/Dicionário de Java#@RequestMapping|@RequestMapping]], [[03-Dominios/Tecnologia/Java/Dicionário de Java#@GetMapping / @PostMapping (mapeamentos HTTP)|@GetMapping / @PostMapping]]

## Referências

- Spring Framework Reference — Handler Methods: Request Mapping: <https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-controller/ann-requestmapping.html>
