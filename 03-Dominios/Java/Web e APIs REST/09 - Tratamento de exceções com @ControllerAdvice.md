---
title: "Tratamento de exceções com @ControllerAdvice"
created: 2026-06-08
updated: 2026-06-08
type: concept
progress: backlog
status: seedling
publish: true
fase: adepto
tags:
  - java
  - web
  - adepto
  - exception-handling
aliases:
  - "@ControllerAdvice"
  - "@RestControllerAdvice"
---

# Tratamento de exceções com @ControllerAdvice

> [!abstract] TL;DR
> Em vez de espalhar `try/catch` por todos os controllers, você centraliza o tratamento de erro num único `@RestControllerAdvice`: uma classe com `@ExceptionHandler`s que mapeiam exceções de domínio (como `OrderNotFoundException`) para status HTTP corretos (404, 400, 409...). O **mecanismo** que intercepta a exceção lançada no controller é o mesmo AOP/proxy do [[03-Dominios/Java/Spring Core e Boot/09 - AOP e proxies no Spring|Galho 8]] — aqui você só configura *qual* exceção vira *qual* resposta. O **formato** dessa resposta de erro, padronizado segundo a RFC 9457 (`ProblemDetail`), é o assunto da [[03-Dominios/Java/Web e APIs REST/10 - Problem Details — RFC 9457|nota 10 deste galho]].

## O que é

`@ControllerAdvice` é uma anotação que marca uma classe como um "conselheiro" (advice) global para todos os controllers da aplicação. Dentro dela, métodos anotados com `@ExceptionHandler(XException.class)` interceptam exceções daquele tipo lançadas em *qualquer* controller e produzem uma resposta HTTP no lugar.

Existem duas anotações na família:

- **`@ControllerAdvice`** — versão MVC tradicional. Os métodos podem retornar nomes de view, `Model`, etc.
- **`@RestControllerAdvice`** — é exatamente `@ControllerAdvice` + `@ResponseBody`. O retorno de cada handler é serializado direto no corpo da resposta (JSON, via Jackson). É a anotação que você usa em APIs REST.

A regra mental: se a sua aplicação é uma API REST, use sempre `@RestControllerAdvice`. Caso contrário você teria que anotar cada handler individualmente com `@ResponseBody`.

Spring ainda oferece uma classe-base pronta, `ResponseEntityExceptionHandler`, que já traz `@ExceptionHandler`s para todas as exceções internas do Spring MVC (validação, JSON malformado, método HTTP errado...). Você estende essa classe quando quer um ponto único que trate tanto os erros de domínio quanto os erros de framework.

## Por que importa

Sem centralização, o tratamento de erro vira um problema de manutenção:

- **Duplicação** — cada controller repete `try/catch` para as mesmas exceções, com risco de retornarem status diferentes para o mesmo erro.
- **Inconsistência de contrato** — um endpoint devolve `{"error": "..."}`, outro devolve `{"message": "..."}`, outro um texto puro. O cliente não consegue parsear erros de forma uniforme.
- **Vazamento de stack trace** — sem um handler global de fallback, uma exceção não tratada chega ao cliente como uma página de erro HTML do servidor, possivelmente expondo nomes de classe e caminhos internos.

Com um `@RestControllerAdvice` único, você define o contrato de erro da API em **um só lugar**. Toda exceção de domínio tem um mapeamento explícito para status HTTP, todo corpo de erro segue o mesmo formato, e o controller volta a ser código de *caminho feliz* — ele apenas lança a exceção e confia no advice para traduzi-la.

## Como funciona

### @ExceptionHandler local vs @RestControllerAdvice global (padrão recomendado)

Há dois escopos para um `@ExceptionHandler`:

- **Local** — o método fica dentro de uma classe `@Controller`/`@RestController`. Ele só trata exceções lançadas *por aquele controller*. Útil para um tratamento muito específico de um único endpoint, mas vira fonte de duplicação se usado como regra geral.
- **Global** — o método fica numa classe `@RestControllerAdvice` separada. Ele trata exceções de *todos* os controllers.

```java
// Local — só vale para esse controller (evite como padrão)
@RestController
class OrderController {

    @ExceptionHandler(OrderNotFoundException.class)
    ResponseEntity<String> handle(OrderNotFoundException ex) {
        return ResponseEntity.status(HttpStatus.NOT_FOUND).body(ex.getMessage());
    }
}
```

O **padrão recomendado** para uma API é o global: uma única classe de advice. Se um handler local e um global existirem para a mesma exceção, o **local tem prioridade** — Spring procura primeiro no próprio controller, depois nos advices.

### Mapear exceção de domínio → status HTTP

O coração do advice é a tradução *exceção → status*. Cada exceção do seu domínio recebe um handler que escolhe o status HTTP semanticamente correto:

| Exceção de domínio        | Status HTTP            |
| ------------------------- | ---------------------- |
| `OrderNotFoundException`  | 404 Not Found          |
| `InvalidOrderException`   | 400 Bad Request        |
| `OrderAlreadyPaidException` | 409 Conflict         |
| `PaymentDeniedException`  | 402 Payment Required   |

Você tem duas estratégias para fixar o status:

1. **No handler** — chamar `ResponseEntity.status(...)` ou `ProblemDetail.forStatusAndDetail(...)` dentro do método. É o mais flexível e o que veremos na prática.
2. **Na exceção** — anotar a classe da exceção com `@ResponseStatus(HttpStatus.NOT_FOUND)`. Funciona até sem advice, mas acopla o status HTTP à exceção (uma exceção de domínio "saber" sobre HTTP é discutível) e perde a chance de customizar o corpo.

A primeira mantém a regra HTTP concentrada na camada web, que é onde ela pertence.

### ResponseEntityExceptionHandler (os handlers built-in do Spring) e ordem/especificidade

Nem toda exceção vem do seu domínio. Quando o cliente manda um JSON quebrado, omite um parâmetro obrigatório ou falha na validação de `@Valid`, quem lança é o próprio Spring MVC:

- `MethodArgumentNotValidException` → 400 (falha de `@Valid` no corpo)
- `HttpMessageNotReadableException` → 400 (JSON malformado)
- `MissingServletRequestParameterException` → 400 (query param ausente)
- `HttpRequestMethodNotSupportedException` → 405 (verbo HTTP errado)
- `HttpMediaTypeNotSupportedException` → 415 (`Content-Type` não suportado)
- `NoHandlerFoundException` → 404 (rota inexistente)

A classe `ResponseEntityExceptionHandler` já traz `@ExceptionHandler`s para todas elas. Estendendo-a, você herda esse comportamento e ainda pode sobrescrever métodos `protected` (como `handleMethodArgumentNotValid`) para customizar o corpo. No Spring Boot, basta ativar `spring.mvc.problemdetails.enabled=true` para que essas exceções já saiam como `ProblemDetail`.

**Ordem e especificidade.** Quando uma exceção é lançada, Spring escolhe o handler **mais específico** disponível, usando um `ExceptionDepthComparator`: ele mede a "distância" na hierarquia de herança entre o tipo lançado e o tipo declarado em cada `@ExceptionHandler`. Um handler de `OrderNotFoundException` ganha de um handler de `RuntimeException` quando a exceção é, de fato, `OrderNotFoundException`. Spring também inspeciona as *causas* aninhadas: se nenhum handler casa com a exceção raiz, ele procura por handlers que casem com `getCause()`, em profundidade arbitrária — mas um match na raiz sempre vence um match na causa.

Quando há **múltiplos `@RestControllerAdvice`**, a ordem entre eles é decidida por `@Order`/`Ordered` (menor valor = maior prioridade). É assim que o Spring Boot deixa o seu advice de domínio (`@Order(1)`) rodar antes do `ResponseEntityExceptionHandler` autoconfigurado (`order 0`)... cuidado: na verdade o autoconfigurado tem ordem mais alta; para sobrepor um built-in, declare seu advice com prioridade *maior* que a dele. A regra prática que basta lembrar: dentro de uma mesma classe, a especificidade do tipo resolve sozinha; entre classes, use `@Order`.

### Logar sem engolir a stack

Um handler que captura a exceção *é* o ponto onde a stack trace para de subir. Se você não logar ali, a informação se perde — o cliente recebe um 500 limpo e você fica sem nada no log para depurar.

A disciplina é: **erros do cliente (4xx) você não precisa logar como erro** (são esperados — um 404 não é um bug do servidor); **erros do servidor (5xx) você sempre loga com a exceção inteira**, passando o `Throwable` como argumento para o logger (não apenas `ex.getMessage()`), para preservar a stack:

```java
@ExceptionHandler(Exception.class)
ProblemDetail handleUnexpected(Exception ex) {
    log.error("Erro não tratado processando a requisição", ex); // stack preservada
    return ProblemDetail.forStatusAndDetail(
            HttpStatus.INTERNAL_SERVER_ERROR, "Erro interno");
}
```

Passar `ex` como segundo argumento (e não concatená-lo na mensagem) é o que faz o framework de log imprimir a stack trace completa.

## Na prática

Um advice global típico para a API de pedidos: um handler para a exceção de domínio `OrderNotFoundException`, um para a falha de validação `MethodArgumentNotValidException`, e um fallback para qualquer coisa inesperada. Todos devolvem `ProblemDetail` — o formato detalhado na [[03-Dominios/Java/Web e APIs REST/10 - Problem Details — RFC 9457|nota 10]].

```java
package com.example.shop.web;

import jakarta.servlet.http.HttpServletRequest;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.ProblemDetail;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import java.net.URI;
import java.time.Instant;
import java.util.HashMap;
import java.util.Map;

@RestControllerAdvice
public class GlobalExceptionHandler {

    private static final Logger log = LoggerFactory.getLogger(GlobalExceptionHandler.class);

    // Exceção de domínio → 404. Teaser da nota 10: o corpo é um ProblemDetail.
    @ExceptionHandler(OrderNotFoundException.class)
    public ProblemDetail handleOrderNotFound(OrderNotFoundException ex) {
        ProblemDetail problem = ProblemDetail.forStatusAndDetail(
                HttpStatus.NOT_FOUND, ex.getMessage());
        problem.setTitle("Pedido não encontrado");
        problem.setType(URI.create("https://api.example.com/errors/order-not-found"));
        problem.setProperty("orderId", ex.getOrderId());
        problem.setProperty("timestamp", Instant.now());
        return problem; // 4xx esperado: não logamos como erro
    }

    // Falha de @Valid no corpo → 400, com o mapa de campos inválidos.
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ProblemDetail handleValidation(MethodArgumentNotValidException ex) {
        Map<String, String> errors = new HashMap<>();
        ex.getBindingResult().getFieldErrors().forEach(fieldError ->
                errors.put(fieldError.getField(), fieldError.getDefaultMessage()));

        ProblemDetail problem = ProblemDetail.forStatusAndDetail(
                HttpStatus.BAD_REQUEST, "Um ou mais campos estão inválidos");
        problem.setTitle("Falha de validação");
        problem.setProperty("errors", errors);
        return problem;
    }

    // Fallback: qualquer exceção não mapeada → 500, com a stack logada.
    @ExceptionHandler(Exception.class)
    public ProblemDetail handleUnexpected(Exception ex, HttpServletRequest request) {
        log.error("Erro inesperado em {} {}",
                request.getMethod(), request.getRequestURI(), ex); // stack preservada
        return ProblemDetail.forStatusAndDetail(
                HttpStatus.INTERNAL_SERVER_ERROR,
                "Ocorreu um erro inesperado. Tente novamente mais tarde.");
    }
}
```

O controller, livre de `try/catch`, apenas lança:

```java
@GetMapping("/orders/{id}")
public OrderResponse findById(@PathVariable String id) {
    return orderService.findById(id)
            .orElseThrow(() -> new OrderNotFoundException(id));
}
```

Repare que o handler de `OrderNotFoundException` é mais específico que o de `Exception` — pela regra de profundidade, ele ganha sempre que a exceção for de fato um pedido não encontrado, e o fallback só roda para o que não foi previsto.

## Armadilhas

### (1) Devolver 200 com o erro no corpo

Tentação clássica: o handler retorna um objeto de erro mas esquece de definir o status, e a resposta sai como **200 OK** com uma mensagem de erro dentro. O cliente, que confia no status, trata o erro como sucesso.

```java
// ERRADO — status default é 200 OK
@ExceptionHandler(OrderNotFoundException.class)
public Map<String, String> handle(OrderNotFoundException ex) {
    return Map.of("error", ex.getMessage()); // 200 com erro no body!
}
```

**Fix:** sempre fixe o status, via `ProblemDetail.forStatusAndDetail(...)`, `ResponseEntity.status(...)` ou `@ResponseStatus` no método. Status HTTP é o canal primário de sinalização de erro.

```java
@ExceptionHandler(OrderNotFoundException.class)
public ProblemDetail handle(OrderNotFoundException ex) {
    return ProblemDetail.forStatusAndDetail(HttpStatus.NOT_FOUND, ex.getMessage());
}
```

### (2) `catch` que engole a stack sem log

Um handler de fallback que captura `Exception`, devolve um 500 genérico e **não loga nada**, ou loga só `ex.getMessage()`. Quando o 500 acontece em produção, não há stack trace para investigar — você sabe *que* falhou, mas não *onde*.

```java
// ERRADO — stack trace evaporou
@ExceptionHandler(Exception.class)
public ProblemDetail handle(Exception ex) {
    log.error("Erro: " + ex.getMessage()); // sem o Throwable: sem stack
    return ProblemDetail.forStatusAndDetail(HttpStatus.INTERNAL_SERVER_ERROR, "Erro");
}
```

**Fix:** passe a exceção como argumento do logger (`log.error("...", ex)`), nunca apenas a mensagem. Assim a stack completa vai para o log.

### (3) Ordem ambígua de handlers

Declarar um handler genérico (`RuntimeException`) e um específico (`OrderNotFoundException`) e confiar na sorte. Embora o `ExceptionDepthComparator` *normalmente* escolha o mais específico, depender de hierarquias amplas (como capturar `Exception` num advice de domínio enquanto outro advice também o captura) gera resolução imprevisível.

```java
// AMBÍGUO — qual roda para uma OrderNotFoundException?
@ExceptionHandler(RuntimeException.class)
ProblemDetail handleGeneric(RuntimeException ex) { ... }

@ExceptionHandler(OrderNotFoundException.class)
ProblemDetail handleSpecific(OrderNotFoundException ex) { ... }
```

**Fix:** declare a exceção **mais específica antes**, mantenha o genérico apenas como fallback de último recurso (`Exception.class`), e quando houver vários advices, ordene-os explicitamente com `@Order`. A regra: o específico vence o genérico — então deixe a hierarquia clara e o fallback amplo num único lugar.

### (4) `@ExceptionHandler` espalhado por controllers

Repetir o mesmo `@ExceptionHandler(OrderNotFoundException.class)` dentro de `OrderController`, `CustomerController`, `ProductController`... Cada cópia pode divergir (um devolve 404, outro 400) e qualquer mudança no contrato de erro exige editar N arquivos.

```java
// ERRADO — duplicado em cada controller
@RestController
class OrderController {
    @ExceptionHandler(OrderNotFoundException.class)
    ProblemDetail handle(OrderNotFoundException ex) { ... }
}
@RestController
class CustomerController {
    @ExceptionHandler(CustomerNotFoundException.class)
    ProblemDetail handle(CustomerNotFoundException ex) { ... } // mesma lógica, copiada
}
```

**Fix:** centralize tudo num único `@RestControllerAdvice`. O handler local só se justifica para um tratamento genuinamente exclusivo de um endpoint — o que é raro.

## Em entrevista

### Frase pronta (inglês)

> In a Spring Boot REST API, I centralize error handling in a single `@RestControllerAdvice` class, which is shorthand for `@ControllerAdvice` plus `@ResponseBody`. Each `@ExceptionHandler` maps a domain exception to the correct HTTP status — for example, `OrderNotFoundException` to 404, a validation failure to 400 — and returns a `ProblemDetail` body following RFC 9457, so every error in the API shares one consistent contract. Under the hood, the advice is wired in through Spring's AOP proxy mechanism, the same one that powers `@Transactional`; for framework exceptions like `MethodArgumentNotValidException` I extend `ResponseEntityExceptionHandler` to reuse Spring's built-in handlers, and I always log unexpected 5xx errors with the full stack trace before returning a generic message to the client.

### Vocabulário

| Português                       | English                          |
| ------------------------------- | -------------------------------- |
| tratamento centralizado de erro | centralized error handling       |
| exceção de domínio              | domain exception                 |
| conselheiro global de controller | global controller advice        |
| mapear para um status HTTP      | to map to an HTTP status         |
| handler de fallback             | fallback handler                 |
| especificidade do handler       | handler specificity              |
| engolir a stack trace           | to swallow the stack trace       |
| corpo de erro padronizado       | standardized error body          |

## Veja também

- [[03-Dominios/Java/Web e APIs REST/04 - ResponseEntity e status codes|ResponseEntity e status codes]]
- [[03-Dominios/Java/Web e APIs REST/10 - Problem Details — RFC 9457|Problem Details — RFC 9457]]
- [[03-Dominios/Java/Web e APIs REST/06 - O pipeline do DispatcherServlet|O pipeline do DispatcherServlet]]
- [[03-Dominios/Java/Spring Core e Boot/09 - AOP e proxies no Spring|AOP e proxies no Spring]] (o mecanismo que intercepta)
- [[03-Dominios/Java/Web e APIs REST/index|Web e APIs REST]]
- [[03-Dominios/Java/index|Trilha Java]]
- Verbetes: [[03-Dominios/Java/Dicionário de Java#@ControllerAdvice / @RestControllerAdvice|@ControllerAdvice / @RestControllerAdvice]], [[03-Dominios/Java/Dicionário de Java#@ExceptionHandler|@ExceptionHandler]]

## Referências

- Spring Framework Reference — Web MVC, `@ExceptionHandler`: https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-controller/ann-exceptionhandler.html
- Spring Framework Reference — Web MVC, Error Responses (`ResponseEntityExceptionHandler`, `ProblemDetail`, RFC 9457): https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-ann-rest-exceptions.html
