---
title: "Validação na borda"
created: 2026-06-08
updated: 2026-06-09
type: concept
progress: backlog
status: seedling
publish: true
fase: adepto
tags:
  - java
  - web
  - adepto
  - validation
aliases:
  - "Validação no controller Spring MVC"
---

# Validação na borda

> [!abstract] TL;DR
> `@Valid` e `@Validated` no controller acionam a spec Bean Validation (Galho 7) na **borda** da API — o ponto de entrada dos dados externos. Uma constraint violada dispara um 400 automático, sem código extra. A distinção essencial: validar **formato** (campo não pode ser vazio, e-mail tem que ser válido) pertence à borda; validar **regra de negócio** (pedido não pode ter quantidade maior que o estoque) pertence ao serviço ([[03-Dominios/Java/Persistência de dados/12 - Transações operacionais — @Transactional propagação, isolamento, rollback, readOnly|Galho 10]]).

## O que é

Validação na borda é o processo de checar se os dados recebidos pelo controller respeitam as restrições de formato e estrutura **antes** de qualquer lógica de negócio ser executada. O Spring MVC integra a spec Jakarta Bean Validation para que essa checagem aconteça de forma declarativa — basta anotar os parâmetros e o framework faz o resto.

As anotações de constraint (`@NotBlank`, `@Email`, `@Size`, `@Positive`, etc.) vêm da spec Bean Validation e são detalhadas no [[03-Dominios/Java/Jakarta EE/08 - Bean Validation|Galho 7 — Bean Validation]]. Esta nota foca na **integração com o controller**: onde colocar `@Valid` ou `@Validated`, que exceção é lançada e como o 400 é gerado automaticamente.

## Por que importa

- **Falha rápida**: dados inválidos são rejeitados antes de chegarem ao banco de dados ou a qualquer serviço, reduzindo carga e superfície de erros.
- **Mensagens de erro consistentes**: o Spring traduz as violações para um corpo 400 estruturado que os clientes da API conseguem interpretar.
- **Código limpo**: nenhum `if (name == null || name.isBlank())` no controller; a intenção fica nas anotações do DTO.
- **Separação de responsabilidades**: formato e estrutura ficam na borda; regra de negócio fica no serviço.

Em entrevistas internacionais, saber articular essa separação ("input validation vs. business rule validation") é um diferencial.

## Como funciona

### @Valid no @RequestBody (→ MethodArgumentNotValidException)

Quando o controller recebe um body JSON, o argumento anotado com `@RequestBody` é desserializado e, se marcado com `@Valid`, **a spec Bean Validation é acionada sobre o objeto inteiro**.

```java
@PostMapping("/orders")
public ResponseEntity<OrderResponse> createOrder(
        @Valid @RequestBody CreateOrderRequest request) {
    // Só chega aqui se todas as constraints passarem
    return ResponseEntity.status(HttpStatus.CREATED)
                         .body(service.create(request));
}
```

Se alguma constraint falhar, o Spring lança `MethodArgumentNotValidException`. No Spring Boot 3 / Framework 6, o handler built-in do Spring (o `ResponseEntityExceptionHandler`, base do tratamento padrão de exceções do MVC) converte essa exceção em **400 Bad Request** automaticamente; com `spring.mvc.problemdetails.enabled=true`, a resposta já sai no formato `ProblemDetail`. Para incluir os detalhes de cada campo inválido no corpo, você customiza esse handler num `@RestControllerAdvice` — ver [[03-Dominios/Java/Web e APIs REST/09 - Tratamento de exceções com @ControllerAdvice|Tratamento de exceções com @ControllerAdvice]].

### @Validated na classe para validar @PathVariable e @RequestParam (→ ConstraintViolationException / HandlerMethodValidationException)

Para validar parâmetros avulsos (path variables, query params), é preciso anotar a **classe do controller** com `@Validated`. As constraints são colocadas diretamente nos parâmetros do método.

```java
@Validated
@RestController
@RequestMapping("/orders")
public class OrderController {

    @GetMapping("/{id}")
    public OrderResponse findById(
            @Min(1) @PathVariable Long id) {
        return service.findById(id);
    }

    @GetMapping
    public List<OrderResponse> search(
            @NotBlank @RequestParam String customerEmail) {
        return service.search(customerEmail);
    }
}
```

No **Spring Framework 6.1+** (Boot 3.2+), a validação de método é built-in — ela levanta `HandlerMethodValidationException`. Em versões anteriores (6.0 / Boot 3.0–3.1), a validação era delegada a um proxy AOP e levantava `ConstraintViolationException`. É seguro tratar **ambas** com um `@ExceptionHandler`, pois o comportamento depende da versão exata em uso.

> [!tip] Regra prática
> `@Valid` no parâmetro → valida o **objeto**. `@Validated` na **classe** → valida **parâmetros avulsos** do método.

### O 400 automático e o BindingResult (quando tratar manualmente)

Por padrão, o Spring trata as exceções de validação e devolve 400 sem código extra. Quando é necessário **controle manual** da resposta — por exemplo, retornar um corpo customizado ou tomar decisões baseadas nos erros específicos — usa-se `BindingResult` logo após o parâmetro validado:

```java
@PostMapping("/orders")
public ResponseEntity<?> createOrder(
        @Valid @RequestBody CreateOrderRequest request,
        BindingResult bindingResult) {          // deve ser imediatamente após

    if (bindingResult.hasErrors()) {
        List<String> erros = bindingResult.getFieldErrors()
                .stream()
                .map(e -> e.getField() + ": " + e.getDefaultMessage())
                .toList();
        return ResponseEntity.badRequest().body(Map.of("erros", erros));
    }
    return ResponseEntity.status(HttpStatus.CREATED)
                         .body(service.create(request));
}
```

Quando `BindingResult` está presente, o Spring **não lança a exceção** automaticamente — o controller fica responsável por inspecionar e reagir. Para a maioria dos casos, um `@ExceptionHandler` global (ver nota 09) é preferível, pois centraliza o tratamento sem poluir cada endpoint.

## Na prática

```java
// DTO — as constraints vêm da spec (Galho 7)
public record CreateOrderRequest(
    @NotBlank(message = "customerEmail é obrigatório")
    @Email(message = "customerEmail deve ser um e-mail válido")
    String customerEmail,

    @NotBlank(message = "productSku é obrigatório")
    String productSku,

    @Positive(message = "quantity deve ser maior que zero")
    int quantity
) {}
```

```java
// Controller
@RestController
@RequestMapping("/orders")
public class OrderController {

    private final OrderService service;

    public OrderController(OrderService service) {
        this.service = service;
    }

    @PostMapping
    public ResponseEntity<OrderResponse> create(
            @Valid @RequestBody CreateOrderRequest request) {
        OrderResponse response = service.create(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }
}
```

Se `customerEmail` vier em branco, a resposta será:

```json
{
  "type": "about:blank",
  "title": "Bad Request",
  "status": 400,
  "detail": "Invalid request content.",
  "instance": "/orders"
}
```

O corpo detalhado com cada campo inválido aparece quando o `ProblemDetails` está habilitado (`spring.mvc.problemdetails.enabled=true`) ou quando há um `@ExceptionHandler` dedicado (ver nota 09).

## Armadilhas

### (1) Esquecer o `@Valid` — a request inválida passa direto

O parâmetro `@RequestBody` **não** é validado automaticamente só por ter constraints no DTO. Sem `@Valid`, os dados chegam ao serviço sem checagem.

```java
// ERRADO — @Valid ausente; constraints ignoradas
@PostMapping("/orders")
public ResponseEntity<OrderResponse> create(
        @RequestBody CreateOrderRequest request) { ... }

// CORRETO
@PostMapping("/orders")
public ResponseEntity<OrderResponse> create(
        @Valid @RequestBody CreateOrderRequest request) { ... }
```

**Fix**: sempre colocar `@Valid` antes de `@RequestBody` quando o objeto tem constraints.

### (2) Declarar `BindingResult` e nunca checá-lo

Quando `BindingResult` está presente no método, o Spring não lança exceção. Se o código não checa `bindingResult.hasErrors()`, dados inválidos são silenciosamente aceitos.

```java
// ERRADO — BindingResult presente mas nunca verificado
@PostMapping("/orders")
public ResponseEntity<OrderResponse> create(
        @Valid @RequestBody CreateOrderRequest request,
        BindingResult bindingResult) {
    return ResponseEntity.ok(service.create(request)); // dados inválidos passam!
}

// CORRETO
@PostMapping("/orders")
public ResponseEntity<?> create(
        @Valid @RequestBody CreateOrderRequest request,
        BindingResult bindingResult) {
    if (bindingResult.hasErrors()) {
        return ResponseEntity.badRequest().body(bindingResult.getAllErrors());
    }
    return ResponseEntity.ok(service.create(request));
}
```

**Fix**: se usar `BindingResult`, verificar `hasErrors()` imediatamente. Caso contrário, prefira o tratamento centralizado com `@ExceptionHandler`.

### (3) Esquecer `@Validated` na classe para validar parâmetros avulsos

Constraints em `@PathVariable` e `@RequestParam` **não funcionam** sem a anotação `@Validated` na classe do controller. O Spring não aplica validação de método por padrão nesses casos.

```java
// ERRADO — @Validated ausente; @Min ignorado
@RestController
@RequestMapping("/orders")
public class OrderController {
    @GetMapping("/{id}")
    public OrderResponse findById(@Min(1) @PathVariable Long id) { ... }
}

// CORRETO
@Validated   // <— necessário na classe
@RestController
@RequestMapping("/orders")
public class OrderController {
    @GetMapping("/{id}")
    public OrderResponse findById(@Min(1) @PathVariable Long id) { ... }
}
```

**Fix**: anotar a classe do controller com `@Validated` quando houver constraints diretas em parâmetros de método.

### (4) Misturar validação de formato com validação de regra de negócio

A borda é o lugar certo para checar **formato e estrutura** — campo obrigatório, formato de e-mail, intervalo numérico. Regras como "cliente não pode ter mais de 3 pedidos abertos" ou "produto precisa estar em estoque" são **regras de negócio** e pertencem à camada de serviço ([[03-Dominios/Java/Persistência de dados/12 - Transações operacionais — @Transactional propagação, isolamento, rollback, readOnly|Galho 10]]).

```java
// ERRADO — regra de negócio implementada como constraint customizada no DTO
// e disparada na borda (dificulta teste, acoplamento ao repositório)
public record CreateOrderRequest(
    @MaxOpenOrders(3) String customerId,  // acessa banco na validação!
    ...
) {}

// CORRETO — formato na borda; regra no serviço
public record CreateOrderRequest(
    @NotBlank String customerId,
    ...
) {}

// No OrderService:
public OrderResponse create(CreateOrderRequest request) {
    if (orderRepository.countOpenByCustomer(request.customerId()) >= 3) {
        throw new BusinessRuleException("Limite de pedidos abertos atingido");
    }
    ...
}
```

**Fix**: manter nas constraints do DTO apenas checagens que não dependem de estado persistido. Tudo que precisa de banco ou de contexto de negócio vai no serviço.

## Em entrevista

### Frase pronta (inglês)

"In Spring MVC, I annotate the controller method parameter with `@Valid` to trigger Bean Validation on the request body — any constraint violation automatically returns a 400 Bad Request via `MethodArgumentNotValidException`. For path variables and query parameters, I add `@Validated` at the class level, which enables method-level validation. I keep format and structural constraints at the edge of the API, while business rules — things that require database state or domain logic — belong in the service layer."

### Vocabulário

| Português                      | English                              |
|-------------------------------|--------------------------------------|
| Validação na borda            | Edge / input validation              |
| Restrição de formato          | Format / structural constraint       |
| Regra de negócio              | Business rule                        |
| Violação de constraint        | Constraint violation                 |
| Parâmetro avulso              | Standalone / method parameter        |
| Tratamento centralizado       | Centralized exception handling       |
| Resultado de vinculação       | Binding result                       |
| Resposta de erro estruturada  | Structured error response            |

## Veja também

- [[03-Dominios/Java/Web e APIs REST/03 - Recebendo dados da request|Recebendo dados da request]]
- [[03-Dominios/Java/Web e APIs REST/09 - Tratamento de exceções com @ControllerAdvice|Tratamento de exceções com @ControllerAdvice]]
- [[03-Dominios/Java/Jakarta EE/08 - Bean Validation|Bean Validation]] (a spec — as constraints `@NotBlank`/`@Email`/...)
- [[03-Dominios/Java/Spring Core e Boot/12 - Configuração e profiles|Configuração e profiles]] (`@Validated` na config)
- [[03-Dominios/Java/Web e APIs REST/index|Web e APIs REST]]
- [[03-Dominios/Java/index|Trilha Java]]
- Verbete: [[03-Dominios/Java/Dicionário de Java#MethodArgumentNotValidException|MethodArgumentNotValidException]]

## Referências

- Spring Framework — Validation: https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-controller/ann-validation.html
- Jakarta Bean Validation spec (Galho 7): [[03-Dominios/Java/Jakarta EE/08 - Bean Validation|Bean Validation]]
