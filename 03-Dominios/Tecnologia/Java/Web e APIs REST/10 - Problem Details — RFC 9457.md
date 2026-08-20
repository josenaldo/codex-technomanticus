---
title: "Problem Details — RFC 9457"
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
  - problem-details
  - exception-handling
aliases:
  - "ProblemDetail"
  - "RFC 9457"
---

# Problem Details — RFC 9457

> [!abstract] TL;DR
> Problem Details (RFC 9457, que obsoletou a RFC 7807) é o formato padrão de erro HTTP (`application/problem+json`); o Spring 6+ traz a classe `ProblemDetail` pronta para padronizar respostas de erro da sua API sem reinventar a roda.

## O que é

Problem Details for HTTP APIs é uma especificação publicada pelo IETF que define um formato padronizado para representar erros em APIs HTTP. A RFC 9457 (julho de 2023) substituiu a RFC 7807 (março de 2016), corrigindo ambiguidades e alinhando o vocabulário com práticas consolidadas.

O formato é baseado em JSON (ou XML) e usa o media type `application/problem+json`. Qualquer cliente que entenda esse formato consegue processar erros de forma genérica, independentemente da API que os gerou.

O Spring Framework 6.0 introduziu suporte nativo à RFC 9457 por meio da classe `ProblemDetail` e das interfaces `ErrorResponse` e `ErrorResponseException`, eliminando a necessidade de bibliotecas externas como Zalando Problem.

## Por que importa

Sem um formato padrão, cada endpoint da API inventa sua própria estrutura de erro. Um endpoint retorna `{ "message": "..." }`, outro retorna `{ "error": "...", "code": 42 }`, e um terceiro retorna HTML quando algo explode no filtro. O cliente precisa tratar N formatos diferentes.

A RFC 9457 resolve isso com um contrato único: campos bem definidos, um media type registrado no IANA, e um mecanismo de extensão para campos extras sem quebrar clientes existentes.

Para quem trabalha em entrevistas internacionais, conhecer Problem Details é sinal de maturidade em design de APIs REST — é o padrão que frameworks como Spring, Micronaut e Quarkus adotaram por padrão.

## Como funciona

### O formato application/problem+json (RFC 9457, que obsoletou a RFC 7807)

Uma resposta de erro Problem Details é um objeto JSON servido com o media type `application/problem+json` e os seguintes campos padrão:

| Campo | Tipo | Descrição |
|---|---|---|
| `type` | URI | Identifica a categoria do problema. Padrão: `"about:blank"`. |
| `title` | string | Resumo legível do tipo do problema. Deve ser consistente entre ocorrências. |
| `status` | number | Código HTTP da resposta (`400`, `404`, `422`, etc.). |
| `detail` | string | Explicação específica desta ocorrência. Foca em ajudar o cliente a resolver. |
| `instance` | URI | Referência única para esta ocorrência específica do problema. |

Além dos cinco campos padrão, o formato permite **propriedades de extensão** (campos extras definidos pelo servidor). Clientes que não reconhecem uma extensão devem simplesmente ignorá-la — esse é o contrato explícito da RFC.

Exemplo canônico do RFC 9457:

```json
{
  "type": "https://example.com/probs/out-of-credit",
  "title": "You do not have enough credit.",
  "detail": "Your current balance is 30, but that costs 50.",
  "instance": "/account/12345/msgs/abc",
  "balance": 30,
  "accounts": ["/account/12345", "/account/67890"]
}
```

Os campos `balance` e `accounts` são extensões específicas desse tipo de problema.

### ProblemDetail no Spring (Framework 6+): forStatusAndDetail, setType, setProperty

O Spring Framework 6.0 introduziu a classe `org.springframework.http.ProblemDetail`, que é um container direto para o formato RFC 9457.

Métodos principais:

- `ProblemDetail.forStatus(HttpStatus)` — cria uma instância com apenas o status.
- `ProblemDetail.forStatusAndDetail(HttpStatus, String)` — cria com status e `detail`.
- `setType(URI)` — define o campo `type` (identifica o tipo do problema).
- `setTitle(String)` — define o campo `title`.
- `setDetail(String)` — define o campo `detail`.
- `setInstance(URI)` — define o campo `instance`. Se não definido, o Spring preenche automaticamente com o path da requisição atual.
- `setProperty(String, Object)` — adiciona uma propriedade de extensão. O Jackson serializa essas propriedades no nível raiz do JSON.

```java
ProblemDetail pd = ProblemDetail.forStatusAndDetail(
    HttpStatus.UNPROCESSABLE_ENTITY,
    "Os dados do pedido são inválidos."
);
pd.setType(URI.create("https://api.example.com/errors/validation-failed"));
pd.setTitle("Falha de validação");
pd.setProperty("errors", List.of("campo 'quantidade' deve ser positivo"));
```

> [!info] 422 ou 400?
> Aqui usamos `422 Unprocessable Entity` por escolha semântica (o payload é sintaticamente válido, mas falha em regra). O *default* do Spring para `MethodArgumentNotValidException` (falha de `@Valid`) é **400 Bad Request** — ver [[03-Dominios/Tecnologia/Java/Web e APIs REST/08 - Validação na borda|Validação na borda]]. Os dois são defensáveis; o importante é ser consistente na API inteira.

### ErrorResponse, ErrorResponseException e a integração com @RestControllerAdvice (nota 09); spring.mvc.problemdetails.enabled

**`ErrorResponse`** é uma interface que expõe os detalhes de uma resposta de erro HTTP: status, cabeçalhos e o body como `ProblemDetail`. Todas as exceções nativas do Spring MVC (como `MethodArgumentNotValidException`, `HttpRequestMethodNotSupportedException`, etc.) implementam essa interface.

**`ErrorResponseException`** é uma implementação base de `ErrorResponse` que você pode usar como superclasse das suas próprias exceções:

```java
public class OrderNotFoundException extends ErrorResponseException {
    public OrderNotFoundException(Long id) {
        super(HttpStatus.NOT_FOUND,
              ProblemDetail.forStatusAndDetail(
                  HttpStatus.NOT_FOUND,
                  "Pedido " + id + " não encontrado."
              ),
              null);
    }
}
```

**`ResponseEntityExceptionHandler`** é uma classe base para `@RestControllerAdvice` que já trata todas as exceções Spring MVC nativas e as serializa como Problem Details. Ao estendê-la, você herda esse comportamento gratuitamente.

**`spring.mvc.problemdetails.enabled=true`** é a propriedade do Spring Boot que ativa um `ResponseEntityExceptionHandler` pré-configurado com order `0`. Com ela ligada, erros de validação, method not allowed, media type não suportado e outros já saem automaticamente no formato `application/problem+json` sem nenhum código extra.

```properties
# application.properties
spring.mvc.problemdetails.enabled=true
```

Se você precisar de um handler personalizado e também quiser o comportamento padrão do Boot, anote seu handler com `@Order(-1)` para que ele seja processado antes.

## Na prática

Um `@ExceptionHandler` devolvendo `ProblemDetail` com a extensão `errors` para erros de validação:

```java
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ProblemDetail;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import java.net.URI;
import java.util.List;

// --- Handler global ---
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ProblemDetail handleValidation(MethodArgumentNotValidException ex) {
        ProblemDetail pd = ProblemDetail.forStatusAndDetail(
            HttpStatus.UNPROCESSABLE_ENTITY,
            "Um ou mais campos falharam na validação."
        );
        pd.setType(URI.create("https://api.example.com/errors/validation-failed"));
        pd.setTitle("Falha de validação");

        List<String> errors = ex.getBindingResult()
            .getFieldErrors()
            .stream()
            .map(fe -> fe.getField() + ": " + fe.getDefaultMessage())
            .toList();

        pd.setProperty("errors", errors);
        return pd;
    }
}
```

JSON de resposta resultante para uma requisição com campo inválido:

```json
HTTP/1.1 422 Unprocessable Entity
Content-Type: application/problem+json

{
  "type": "https://api.example.com/errors/validation-failed",
  "title": "Falha de validação",
  "status": 422,
  "detail": "Um ou mais campos falharam na validação.",
  "instance": "/orders",
  "errors": [
    "quantity: deve ser maior que zero",
    "productId: não deve ser nulo"
  ]
}
```

O campo `instance` foi preenchido automaticamente pelo Spring com o path `/orders`. O campo `errors` é a extensão customizada.

## Armadilhas

### (1) Formato de erro ad-hoc por endpoint

**Problema:** cada controller define sua própria estrutura `{ "message": "...", "code": 42 }`. O cliente precisa tratar N formatos diferentes e qualquer mudança quebra consumidores.

**Exemplo do problema:**
```java
// Não faça isso — estrutura proprietária sem padrão
return ResponseEntity.badRequest()
    .body(Map.of("message", "inválido", "code", 400));
```

**Fix:** use sempre `ProblemDetail` (via `@ExceptionHandler` centralizado) e habilite `spring.mvc.problemdetails.enabled=true` no Boot para cobrir os casos do framework automaticamente.

### (2) Vazar stack trace ou SQL no campo `detail`

**Problema:** colocar `ex.getMessage()` diretamente no `detail` pode expor detalhes internos de implementação (nomes de tabela, queries SQL, stack traces) para clientes externos, criando risco de segurança.

**Exemplo do problema:**
```java
// Perigoso — ex.getMessage() pode conter "Table 'orders' doesn't exist"
pd.setDetail(ex.getMessage());
```

**Fix:** escreva mensagens de `detail` voltadas ao cliente, não ao desenvolvedor. Use logging para registrar a causa real internamente.

```java
log.error("Erro inesperado ao processar pedido", ex);
pd.setDetail("Não foi possível processar o pedido. Tente novamente.");
```

### (3) Ignorar o campo `type` URI — deixar como "about:blank"

**Problema:** sem um `type` URI real, clientes não conseguem distinguir tipos de erro programaticamente. `"about:blank"` é o valor padrão e indica que nenhum tipo foi definido — é como retornar um erro sem código.

**Exemplo do problema:**
```java
// type ficará "about:blank" — sem valor para o cliente
ProblemDetail pd = ProblemDetail.forStatusAndDetail(
    HttpStatus.NOT_FOUND, "Produto não encontrado."
);
// setType nunca chamado
```

**Fix:** defina URIs de tipo estáveis, de preferência apontando para documentação real (ou pelo menos um path consistente):

```java
pd.setType(URI.create("https://api.example.com/errors/product-not-found"));
```

### (4) Reinventar o que o ProblemDetail já entrega

**Problema:** criar classes `ErrorResponse` próprias com campos `message`, `timestamp`, `path` sem conhecer o que o Spring já oferece, resultando em código duplicado, sem o media type correto e sem integração automática com o framework.

**Fix:** use `ProblemDetail` como base. Para campos extras (timestamp, traceId), use `setProperty`. Para tipos de problema reutilizáveis, crie subclasses de `ErrorResponseException`. O Spring já cuida do media type, da serialização e da integração com `ResponseEntityExceptionHandler`.

## Em entrevista

### Frase pronta (inglês)

"RFC 9457, which obsoletes RFC 7807, defines a standard JSON format for HTTP error responses using the `application/problem+json` media type. The five core fields are `type`, `title`, `status`, `detail`, and `instance`, and you can add custom extension properties without breaking existing clients. Spring Framework 6 ships with `ProblemDetail` as a first-class citizen, so you get this format out of the box — you just need to return `ProblemDetail` from your `@ExceptionHandler` methods, or enable `spring.mvc.problemdetails.enabled=true` in Spring Boot to cover all framework exceptions automatically."

### Vocabulário

| Português | Inglês |
|---|---|
| Detalhes de problema | Problem Details |
| Tipo do problema | Problem type (`type` URI) |
| Instância do problema | Problem instance (`instance` URI) |
| Propriedade de extensão | Extension member / extension property |
| Tipo de mídia | Media type |
| Manipulador de exceções global | Global exception handler |
| Resposta de erro | Error response |
| Negociação de conteúdo | Content negotiation |

## Veja também

- [[03-Dominios/Tecnologia/Java/Web e APIs REST/09 - Tratamento de exceções com @ControllerAdvice|Tratamento de exceções com @ControllerAdvice]]
- [[03-Dominios/Tecnologia/Java/Web e APIs REST/04 - ResponseEntity e status codes|ResponseEntity e status codes]]
- [[03-Dominios/Tecnologia/Java/Web e APIs REST/index|Web e APIs REST]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- Verbete: [[03-Dominios/Tecnologia/Java/Dicionário de Java#ProblemDetail (RFC 9457)|ProblemDetail (RFC 9457)]]

## Referências

- Spring Framework — Error Responses (MVC): https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-ann-rest-exceptions.html
- RFC 9457 — Problem Details for HTTP APIs (IETF): https://datatracker.ietf.org/doc/html/rfc9457
- RFC 7807 — Problem Details for HTTP APIs (obsoletada pela RFC 9457): https://datatracker.ietf.org/doc/html/rfc7807
