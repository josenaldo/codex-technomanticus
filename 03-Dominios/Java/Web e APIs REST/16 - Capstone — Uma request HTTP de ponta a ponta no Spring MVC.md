---
title: "Capstone — Uma request HTTP de ponta a ponta no Spring MVC"
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
  - spring-mvc
  - rest
aliases:
  - "Capstone Web"
  - "Request HTTP de ponta a ponta"
---

# Capstone — Uma request HTTP de ponta a ponta no Spring MVC

> [!abstract] TL;DR
> Uma request REST atravessa um pipeline inteiro antes de tocar no seu código: `Filter` → `DispatcherServlet` → `HandlerMapping` → `HandlerInterceptor` → `HandlerAdapter` → `HandlerMethodArgumentResolver` → `@Valid` → controller → `ResponseEntity` → `HttpMessageConverter`. Quando algo dá errado, a exceção desvia para a cadeia de `HandlerExceptionResolver` → `@RestControllerAdvice` → `ProblemDetail` (RFC 9457). Projetar uma API REST decente é, no fundo, dominar esse caminho de ponta a ponta — saber onde cada decisão (status, validação, serialização, erro) é tomada e por qual componente.

## O que é

Esta é a **nota de fechamento** do galho "Web e APIs REST". As notas anteriores dissecaram cada componente em isolamento: o que é o Spring MVC, como mapear endpoints, como receber dados, como devolver `ResponseEntity`, como o Jackson serializa, como o `DispatcherServlet` orquestra tudo, como negociar conteúdo, validar na borda, tratar exceções e padronizar erros com Problem Details.

Aqui a gente **costura tudo num único fio**: seguimos uma request REST concreta — um `POST /orders` para criar um pedido — do primeiro byte que chega no servlet container até o último byte que volta para o cliente. E seguimos também o **caminho alternativo**: o que acontece quando a request é inválida ou o controller lança uma exceção.

Pense neste capstone como o **mapa do metrô** do galho. Cada estação é uma nota; aqui você vê a linha inteira e como baldear entre elas.

## Por que importa

Um desenvolvedor júnior pensa: "eu anoto `@PostMapping`, recebo o objeto, devolvo outro, pronto". Um desenvolvedor sênior **enxerga o pipeline**. Essa diferença de altitude muda como você:

- **Debuga.** Um 415 não é "o JSON está errado" — é o `HttpMessageConverter` recusando o `Content-Type`. Um 400 com corpo vazio raramente é o controller; é o argument resolver ou o `@Valid` falhando antes do método rodar. Saber em qual estação o trem parou é metade da depuração.
- **Decide.** Logging de request deve ir num `Filter` ou num `HandlerInterceptor`? Validação cara deve ficar na borda ou no service? Onde colocar autenticação? Cada resposta depende de entender a ordem dos componentes.
- **Conversa em entrevista.** "Walk me through what happens when a request hits your Spring controller" é uma pergunta de sistema clássica. A resposta separa quem decorou anotações de quem entende a arquitetura.

E há um ganho conceitual transversal: o Spring MVC é uma **implementação opinativa** sobre as specs Jakarta (Servlet, Bean Validation). Entender o pipeline também te ensina o que é Spring e o que é a plataforma portável por baixo — o tema da nota [[03-Dominios/Java/Jakarta EE/14 - Jakarta EE hoje — a plataforma sob o Spring|Jakarta EE hoje]].

## Como funciona

### Da request à resposta: o caminho completo (POST /orders válida)

Vamos seguir uma request bem-comportada. O cliente envia:

```text
POST /orders HTTP/1.1
Host: api.exemplo.com
Content-Type: application/json
Accept: application/json

{ "customerId": 42, "productId": 7, "quantity": 3 }
```

E o controller que a recebe:

```java
@RestController
@RequestMapping("/orders")
class OrderController {

    private final OrderService orderService;

    OrderController(OrderService orderService) {
        this.orderService = orderService;
    }

    @PostMapping
    ResponseEntity<OrderResponse> create(@Valid @RequestBody CreateOrderRequest req) {
        Order order = orderService.place(req.customerId(), req.productId(), req.quantity());
        URI location = URI.create("/orders/" + order.id());
        return ResponseEntity.created(location).body(OrderResponse.from(order));
    }
}
```

O que acontece entre o byte que chega e o byte que volta:

```text
                          REQUEST: POST /orders { ... }
                                     │
   ┌─────────────────────────────────▼─────────────────────────────────┐
   │ 1. Servlet Filter chain                                            │  ← [[Nota 11]]
   │    (CORS, encoding, segurança, logging, tracing)                   │
   │    Atua sobre o byte cru; NÃO conhece o controller ainda.          │
   └─────────────────────────────────┬─────────────────────────────────┘
                                     ▼
   ┌───────────────────────────────────────────────────────────────────┐
   │ 2. DispatcherServlet.doDispatch()                                  │  ← [[Nota 06]]
   │    O front controller. Orquestra todas as estações abaixo.         │
   └─────────────────────────────────┬─────────────────────────────────┘
                                     ▼
   ┌───────────────────────────────────────────────────────────────────┐
   │ 3. HandlerMapping (RequestMappingHandlerMapping)                   │  ← [[Nota 02]]
   │    Casa POST + /orders → OrderController#create.                   │  ← [[Nota 06]]
   │    Devolve um HandlerExecutionChain (handler + interceptors).      │
   │    Sem match → 404 aqui mesmo.                                     │
   └─────────────────────────────────┬─────────────────────────────────┘
                                     ▼
   ┌───────────────────────────────────────────────────────────────────┐
   │ 4. HandlerInterceptor.preHandle()                                  │  ← [[Nota 11]]
   │    JÁ sabe qual handler vai rodar (auth por rota, métricas).       │
   │    Retornar false aqui aborta a request.                          │
   └─────────────────────────────────┬─────────────────────────────────┘
                                     ▼
   ┌───────────────────────────────────────────────────────────────────┐
   │ 5. HandlerAdapter (RequestMappingHandlerAdapter)                   │  ← [[Nota 06]]
   │    Sabe INVOCAR um método @RequestMapping. Coordena 6, 7, 8.       │
   └─────────────────────────────────┬─────────────────────────────────┘
                                     ▼
   ┌───────────────────────────────────────────────────────────────────┐
   │ 6. HandlerMethodArgumentResolver                                   │  ← [[Nota 03]]
   │    Resolve cada parâmetro. Para @RequestBody chama o...            │
   │      └─ HttpMessageConverter (Jackson) → JSON vira                 │  ← [[Nota 05]]
   │         CreateOrderRequest. Content-Type errado → 415.             │  ← [[Nota 07]]
   └─────────────────────────────────┬─────────────────────────────────┘
                                     ▼
   ┌───────────────────────────────────────────────────────────────────┐
   │ 7. @Valid → Bean Validation                                       │  ← [[Nota 08]]
   │    quantity > 0? customerId não-nulo? Falha → desvia para o        │
   │    CAMINHO DE ERRO (próxima seção). Controller NÃO roda.           │
   └─────────────────────────────────┬─────────────────────────────────┘
                                     ▼
   ┌───────────────────────────────────────────────────────────────────┐
   │ 8. OrderController#create(...)  ← FINALMENTE o SEU código          │
   │    Chama o service, monta o ResponseEntity.                       │  ← [[Nota 04]]
   └─────────────────────────────────┬─────────────────────────────────┘
                                     ▼
   ┌───────────────────────────────────────────────────────────────────┐
   │ 9. HandlerMethodReturnValueHandler                                 │  ← [[Nota 04]]
   │    Lê o ResponseEntity: status 201, header Location, corpo.       │
   │      └─ HttpMessageConverter (Jackson) → OrderResponse vira JSON  │  ← [[Nota 05]]
   │         conforme o Accept (content negotiation).                  │  ← [[Nota 07]]
   └─────────────────────────────────┬─────────────────────────────────┘
                                     ▼
   ┌───────────────────────────────────────────────────────────────────┐
   │ 10. HandlerInterceptor.postHandle() e afterCompletion()           │  ← [[Nota 11]]
   │     Volta pela cadeia de interceptors (ordem inversa).            │
   │     afterCompletion roda mesmo se houve exceção (cleanup).        │
   └─────────────────────────────────┬─────────────────────────────────┘
                                     ▼
   ┌───────────────────────────────────────────────────────────────────┐
   │ 11. Filter chain (caminho de volta) → bytes vão para o cliente    │  ← [[Nota 11]]
   └─────────────────────────────────┬─────────────────────────────────┘
                                     ▼
                          RESPONSE: 201 Created
                          Location: /orders/1001
                          { "id": 1001, "status": "PLACED", ... }
```

O ponto mental a fixar: **seu controller é a estação 8 de 11**. Há sete componentes que rodam *antes* dele e três *depois*. A maior parte do que parece "mágica do Spring" — desserializar JSON, validar, escolher status, serializar de volta — acontece nas estações ao redor do seu método, não dentro dele.

> [!note] Resumo em uma linha
> A request entra crua pelo `Filter`, é roteada pelo `DispatcherServlet`+`HandlerMapping`, tem os argumentos montados e validados pelos resolvers+`@Valid`, toca seu controller por um instante, e sai serializada pelo `HttpMessageConverter`.

### O caminho de erro (exceção → HandlerExceptionResolver → @RestControllerAdvice → ProblemDetail)

E se a `quantity` vier como `0`? A estação 7 (`@Valid`) lança `MethodArgumentNotValidException`. E se o `OrderService` lançar `CustomerNotFoundException` na estação 8? Em ambos os casos, o trem **descarrila do trilho normal** e entra na linha de erro:

```text
   Estação 7 (@Valid) ou 8 (controller/service) lança uma exceção
                                     │
                                     ▼
   ┌───────────────────────────────────────────────────────────────────┐
   │ DispatcherServlet CAPTURA a exceção e consulta a cadeia de         │
   │ HandlerExceptionResolver, EM ORDEM:                               │
   │                                                                   │
   │   1. ExceptionHandlerExceptionResolver                            │
   │      → procura um @ExceptionHandler casável (no controller ou     │
   │        num @RestControllerAdvice global). É AQUI que seu          │
   │        advice entra.                                              │  ← [[Nota 09]]
   │   2. ResponseStatusExceptionResolver                             │
   │      → honra @ResponseStatus / ResponseStatusException.          │
   │   3. DefaultHandlerExceptionResolver                            │
   │      → mapeia exceções padrão do MVC (415, 405, 400...).         │
   └─────────────────────────────────┬─────────────────────────────────┘
                                     ▼
   ┌───────────────────────────────────────────────────────────────────┐
   │ @RestControllerAdvice (estende ResponseEntityExceptionHandler)    │  ← [[Nota 09]]
   │   Mapeia a exceção para um ProblemDetail (RFC 9457):             │  ← [[Nota 10]]
   │     type, title, status, detail, instance + props extras.        │
   └─────────────────────────────────┬─────────────────────────────────┘
                                     ▼
   ┌───────────────────────────────────────────────────────────────────┐
   │ HttpMessageConverter serializa o ProblemDetail como              │  ← [[Nota 05]]
   │ application/problem+json (media type preferido na negociação).    │  ← [[Nota 07]]
   └─────────────────────────────────┬─────────────────────────────────┘
                                     ▼
                          RESPONSE: 404 Not Found
                          Content-Type: application/problem+json
```

O advice que materializa esse caminho:

```java
@RestControllerAdvice
class ApiExceptionHandler extends ResponseEntityExceptionHandler {

    @ExceptionHandler(CustomerNotFoundException.class)
    ProblemDetail handleCustomerNotFound(CustomerNotFoundException ex) {
        ProblemDetail problem = ProblemDetail.forStatusAndDetail(
                HttpStatus.NOT_FOUND, ex.getMessage());
        problem.setType(URI.create("https://api.exemplo.com/errors/customer-not-found"));
        problem.setTitle("Customer Not Found");
        problem.setProperty("customerId", ex.customerId());
        return problem;
    }
    // handleMethodArgumentNotValid já vem de ResponseEntityExceptionHandler
}
```

O JSON que volta ao cliente:

```text
{
  "type": "https://api.exemplo.com/errors/customer-not-found",
  "title": "Customer Not Found",
  "status": 404,
  "detail": "No customer with id 42",
  "instance": "/orders",
  "customerId": 42
}
```

A grande sacada: o caminho de erro **não é um if no seu controller**. É uma segunda esteira, paralela à principal, ativada pelo `DispatcherServlet` quando uma exceção borbulha. Por isso seus controllers ficam limpos — eles *lançam* exceções e deixam o advice + os Problem Details transformarem isso num contrato HTTP padronizado. Quem estende `ResponseEntityExceptionHandler` ainda ganha de graça o tratamento de todas as exceções built-in do MVC já no formato RFC 9457.

### Spring MVC → spec Jakarta

O Spring MVC não inventou HTTP em Java. Ele é uma camada opinativa **sobre** a Servlet API e reusa specs Jakarta para validação. Saber distinguir o que é Spring do que é a spec portável é o que separa "sei usar o Spring" de "entendo a plataforma" — é **o caminho do Spring vs a spec portável**. A mesma intenção tem duas materializações:

| Componente Spring MVC | Spec Jakarta equivalente | O que faz |
| --- | --- | --- |
| `DispatcherServlet` | **Servlet API** (`jakarta.servlet.http.HttpServlet`) | É, literalmente, *um* `Servlet` registrado no container. Todo o pipeline roda dentro de `service()`. Veja [[03-Dominios/Java/Jakarta EE/03 - Servlet API — o alicerce HTTP|Servlet API]]. |
| `@RestController` + `@RequestMapping` | **JAX-RS** (`@Path`, `@GET`, `@Produces`) | Roteamento declarativo de HTTP para métodos. O Spring usa convenção própria; JAX-RS é a spec portável. Veja [[03-Dominios/Java/Jakarta EE/07 - JAX-RS — REST declarativo\|JAX-RS]]. |
| `@Valid` no `@RequestBody` | **Bean Validation** (`jakarta.validation`, `@NotNull`, `@Min`) | A *especificação* de validação é Jakarta; o Spring só decide *onde* e *quando* dispará-la no pipeline. Veja [[03-Dominios/Java/Jakarta EE/08 - Bean Validation\|Bean Validation]]. |
| `HandlerInterceptor` | **Servlet Filter** (`jakarta.servlet.Filter`) | Ambos interceptam, mas em alturas diferentes: o `Filter` envolve o servlet inteiro (byte cru, agnóstico de handler); o `HandlerInterceptor` roda dentro do MVC, já sabendo qual controller vai atender. Veja [[03-Dominios/Java/Web e APIs REST/11 - Interceptors vs Filters\|Interceptors vs Filters]]. |

A leitura: o que você escreve com anotações Spring tem um equivalente conceitual na plataforma. Se um dia você migrar para Quarkus ou Helidon (que falam JAX-RS direto), são os *mesmos conceitos* com outra fachada. O container por baixo do Spring continua sendo o mundo Jakarta — tema de [[03-Dominios/Java/Spring Core e Boot/index|Spring Core e Boot]].

## Na prática

### Checklist REST API production-grade

Antes de declarar uma API "pronta", passe por estas estações. Cada item ancora numa nota deste galho ou do galho Jakarta:

- [ ] **Status codes corretos.** 201 + `Location` ao criar, 200/204 ao atualizar, 404 vs 422 vs 400 distintos. O status é parte do contrato, não enfeite. → [[03-Dominios/Java/Web e APIs REST/04 - ResponseEntity e status codes|ResponseEntity e status codes]]
- [ ] **DTO de borda, nunca a entidade.** Exponha `OrderResponse`, não `Order` (a entidade JPA). Desacopla o modelo persistente do contrato HTTP e evita vazar campos internos / lazy-loading na serialização. → [[03-Dominios/Java/Web e APIs REST/05 - Serialização JSON com Jackson|Serialização JSON com Jackson]]
- [ ] **Validação na borda** com `@Valid` no `@RequestBody`, falhando rápido com 400 antes de tocar a regra de negócio. → [[03-Dominios/Java/Web e APIs REST/08 - Validação na borda|Validação na borda]]
- [ ] **Erro padronizado (RFC 9457).** Um `@RestControllerAdvice` central que emite `ProblemDetail`/`application/problem+json` para todo erro previsível. → [[03-Dominios/Java/Web e APIs REST/10 - Problem Details — RFC 9457|Problem Details — RFC 9457]]
- [ ] **OpenAPI / Swagger** gerado e versionado, para que o contrato seja descobrível e testável por consumidores. → [[03-Dominios/Java/Web e APIs REST/12 - Documentando a API com OpenAPI e Swagger|Documentando a API com OpenAPI e Swagger]]
- [ ] **Estratégia de versionamento** explícita (path `/v1`, header, ou media type) decidida *antes* do primeiro cliente externo. Versionar depois é caro. *(planejado neste galho)*
- [ ] **Timeouts no cliente HTTP.** Se sua API chama outras APIs, todo `RestClient`/`WebClient` precisa de connect + read timeout. Cliente sem timeout é vazamento de threads esperando a eternidade. *(planejado neste galho)*

### O mapa em uma frase por estação

| Estação | Pergunta que ela responde |
| --- | --- |
| `Filter` | "Devo nem deixar isso entrar?" (CORS, auth crua, encoding) |
| `HandlerMapping` | "Qual método atende essa URL+verbo?" |
| `HandlerInterceptor` | "Antes/depois deste handler específico, faço algo?" |
| Argument resolver + converter | "Como transformo bytes/params nos parâmetros do método?" |
| `@Valid` | "Os dados de entrada são aceitáveis?" |
| Controller | "Qual é a regra de negócio?" |
| Return handler + converter | "Como transformo o retorno em bytes HTTP?" |
| `HandlerExceptionResolver` + advice | "E se algo explodir?" |

## Armadilhas

### (1) "O controller é chamado direto pela request"

**O erro de raciocínio.** Imaginar que o servlet container chama seu `@PostMapping` diretamente, como se a anotação fosse um atalho do HTTP para o seu método.

**Por que é falso.** Há sete componentes antes dele (estações 1–7). Roteamento, desserialização, resolução de argumentos e validação acontecem *fora* do seu método. Quando você acha que "o controller está com bug", muitas vezes o trem nem chegou na estação 8 — parou no converter (415) ou no `@Valid` (400).

**O fix.** Internalize o pipeline. Ao debugar, pergunte primeiro: *o método foi sequer invocado?* Um breakpoint na primeira linha do controller responde isso em segundos e elimina metade das hipóteses erradas.

### (2) "Qualquer 2xx serve" (status é decoração)

**O erro de raciocínio.** Devolver sempre 200 OK porque "deu certo é deu certo", tratando o status como cosmético.

**Por que é falso.** O status code é **contrato semântico**. 201 diz "criei e aqui está o `Location`"; 200 diz "aqui está o recurso"; 204 diz "feito, sem corpo"; 202 diz "aceitei, processo depois". Clientes, caches, proxies e CDNs *agem* sobre o status. Devolver 200 onde deveria ser 201/204 corrói a interoperabilidade e confunde quem consome.

**O fix.** Trate status como parte do design do endpoint. Use `ResponseEntity.created(uri)`, `.noContent()`, `.ok()` deliberadamente — veja [[03-Dominios/Java/Web e APIs REST/04 - ResponseEntity e status codes|ResponseEntity e status codes]].

### (3) "Validação é só responsabilidade do service"

**O erro de raciocínio.** Achar que validar entrada é trabalho da camada de negócio, então o controller só repassa.

**Por que é falso.** Validação tem **duas naturezas**. A *sintática/estrutural* (campo obrigatório, formato, faixa) pertence à borda — falhe rápido com 400 antes de gastar transação, conexão de banco e lógica. A *de invariantes de domínio* (regras de negócio) pertence ao service. Empurrar tudo para o service faz o controller aceitar lixo e o erro vir tarde, caro e mal formatado.

**O fix.** `@Valid` na borda para o que é estrutural; regras de negócio no domínio lançando exceções tratadas pelo advice. Os dois caminhos convergem no mesmo `ProblemDetail`. Veja [[03-Dominios/Java/Web e APIs REST/08 - Validação na borda|Validação na borda]].

### (4) Escolher cliente HTTP ou esquema de versionamento por hype

**O erro de raciocínio.** "Time X usa `WebClient` reativo, então vou usar"; ou "vi um blog versionando por header, vou copiar" — decisões guiadas por moda, não por requisito.

**Por que é falso.** `WebClient` reativo brilha sob alta concorrência e backpressure; num serviço bloqueante simples, ele adiciona complexidade de `Mono`/`Flux` sem ganho. Versionamento por path é trivial de cachear e debugar; por media type é elegante mas exige clientes disciplinados. Não há escolha universalmente certa — há a certa *para a sua carga e seus consumidores*.

**O fix.** Decida por requisito explícito (modelo de concorrência, perfil dos clientes, necessidade de cache) e registre a decisão. Esses temas são *(planejados neste galho)* — quando chegarem, a régua será trade-off, não hype.

## Em entrevista

### Frase pronta (inglês)

> "When a request hits a Spring MVC endpoint, it doesn't go straight to my controller. It first passes through the servlet filter chain, then the `DispatcherServlet` acts as a front controller: it asks a `HandlerMapping` which method handles the URL, runs any `HandlerInterceptor`, and a `HandlerAdapter` invokes the method — resolving and validating the arguments first, deserializing the body with an `HttpMessageConverter`. My controller is really just one stage in a pipeline. On the way out, the same converters serialize the `ResponseEntity` according to content negotiation. If anything throws, the request diverts to a chain of `HandlerExceptionResolver`s, where my `@RestControllerAdvice` maps the exception to a `ProblemDetail` following RFC 9457 — so the error path is a parallel track, not an `if` inside my handler."

### Vocabulário

| Português | English |
| --- | --- |
| Front controller (controlador frontal) | Front controller |
| Pipeline de processamento da request | Request processing pipeline |
| Resolvedor de argumentos do método | Handler method argument resolver |
| Negociação de conteúdo | Content negotiation |
| Conselho de controlador (advice global) | Controller advice |
| Tratador de exceções | Exception handler / resolver |
| Detalhes do problema (RFC 9457) | Problem Details |
| Validação na borda | Edge / boundary validation |
| Filtro de servlet | Servlet filter |
| Cabeçalho de localização | Location header |

### Cheatsheet

| Nota do galho | Problema que ela resolve |
| --- | --- |
| [[03-Dominios/Java/Web e APIs REST/01 - O que é Spring MVC — a camada web sobre o container|01 — O que é Spring MVC]] | "O que está rodando por baixo do meu controller?" |
| [[03-Dominios/Java/Web e APIs REST/06 - O pipeline do DispatcherServlet|06 — Pipeline do DispatcherServlet]] | "Quem chama meu método e em que ordem?" |
| [[03-Dominios/Java/Web e APIs REST/03 - Recebendo dados da request|03 — Recebendo dados da request]] | "Como params/body viram parâmetros do método?" |
| [[03-Dominios/Java/Web e APIs REST/04 - ResponseEntity e status codes|04 — ResponseEntity e status codes]] | "Como controlo status, headers e corpo da resposta?" |
| [[03-Dominios/Java/Web e APIs REST/07 - Content negotiation|07 — Content negotiation]] | "Como o Spring decide JSON vs XML?" |
| [[03-Dominios/Java/Web e APIs REST/08 - Validação na borda|08 — Validação na borda]] | "Onde rejeito entrada inválida?" |
| [[03-Dominios/Java/Web e APIs REST/09 - Tratamento de exceções com @ControllerAdvice|09 — @ControllerAdvice]] | "Onde centralizo o tratamento de erros?" |
| [[03-Dominios/Java/Web e APIs REST/10 - Problem Details — RFC 9457|10 — Problem Details]] | "Qual o formato padrão de erro HTTP?" |

## Veja também

- [[03-Dominios/Java/Web e APIs REST/06 - O pipeline do DispatcherServlet|O pipeline do DispatcherServlet]]
- [[03-Dominios/Java/Web e APIs REST/09 - Tratamento de exceções com @ControllerAdvice|Tratamento de exceções com @ControllerAdvice]]
- [[03-Dominios/Java/Web e APIs REST/10 - Problem Details — RFC 9457|Problem Details — RFC 9457]]
- [[03-Dominios/Java/Web e APIs REST/08 - Validação na borda|Validação na borda]]
- [[03-Dominios/Java/Jakarta EE/07 - JAX-RS — REST declarativo|JAX-RS]] (a spec — o outro caminho)
- [[03-Dominios/Java/Spring Core e Boot/index|Spring Core e Boot]] (o container)
- [[03-Dominios/Java/Web e APIs REST/index|Web e APIs REST]]
- [[03-Dominios/Java/index|Trilha Java]]

## Referências

- Spring Framework Reference — Web MVC: https://docs.spring.io/spring-framework/reference/web/webmvc.html
- Spring Framework Reference — Error Responses (RFC 9457): https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-ann-rest-exceptions.html
- RFC 9457 — Problem Details for HTTP APIs: https://www.rfc-editor.org/rfc/rfc9457
- Jakarta Servlet 6.0 Specification: https://jakarta.ee/specifications/servlet/6.0/
- Jakarta Bean Validation 3.0 Specification: https://jakarta.ee/specifications/bean-validation/3.0/
