---
title: "ResponseEntity e status codes"
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
  - rest
aliases:
  - "ResponseEntity"
---

# ResponseEntity e status codes

> [!abstract] TL;DR
> A resposta HTTP se monta com `ResponseEntity<T>` (status + headers + body) ou com `@ResponseStatus` (declarativo). Usar o status certo é parte do contrato REST: 201 + `Location` no create, 204 no delete, 4xx para erros de cliente e 5xx para falhas do servidor. Um status errado quebra clientes, caches e ferramentas de monitoração antes mesmo de qualquer lógica de negócio.

## O que é

`ResponseEntity<T>` é a classe do Spring que representa **a resposta HTTP completa**: status code, cabeçalhos e corpo. Ela estende `HttpEntity<T>` e é retornada diretamente de métodos de controller para dar controle total sobre a resposta.

```java
// Assinatura simplificada
public class ResponseEntity<T> extends HttpEntity<T> {
    // status, headers e body encapsulados
}
```

Complementarmente, `@ResponseStatus` é uma anotação que define o código de status de forma declarativa, sem precisar instanciar `ResponseEntity` — útil em casos simples ou para anotar classes de exceção.

## Por que importa

Em REST, o status HTTP **é o contrato**. O corpo da resposta carrega dados, mas é o status que diz ao cliente o que aconteceu:

- **Criação bem-sucedida** deve retornar 201 + `Location`, não 200.
- **Deleção** deve retornar 204, não 200 com `"success": true` no corpo.
- **Erro de validação** deve ser 422 (ou 400), não 500.

Ferramentas de monitoração, gateways de API, caches HTTP e clientes front-end tomam decisões com base no status antes de olhar o corpo. Retornar 200 para tudo é uma violação silenciosa do protocolo que acumula dívida técnica.

## Como funciona

### ResponseEntity<T>: status + headers + body

A classe oferece uma API fluente via factory methods estáticos:

```java
// 200 OK com body
ResponseEntity.ok(produto);

// 200 OK com headers customizados e body
ResponseEntity.ok()
    .header("X-Custom-Header", "valor")
    .body(produto);

// 201 Created com header Location obrigatório
URI location = URI.create("/produtos/" + produto.getId());
ResponseEntity.created(location).body(produto);

// 204 No Content (sem body)
ResponseEntity.noContent().build();

// Status customizado
ResponseEntity.status(HttpStatus.CONFLICT).body(erroDto);

// Atalhos para erros comuns
ResponseEntity.badRequest().body(erroDto);   // 400
ResponseEntity.notFound().build();           // 404
```

O tipo genérico `<T>` é serializado pelos `HttpMessageConverters` do Spring (JSON via Jackson, por padrão). Se `<T>` for `Void`, não há body na resposta.

### @ResponseStatus (declarativo)

Quando não é necessário controlar headers dinamicamente, `@ResponseStatus` simplifica o código:

```java
// No método do controller
@DeleteMapping("/{id}")
@ResponseStatus(HttpStatus.NO_CONTENT)
public void delete(@PathVariable Long id) {
    service.delete(id);
    // void: sem body, Spring aplica 204 automaticamente
}
```

`@ResponseStatus` também pode ser colocado em classes de exceção para mapear automaticamente o código de retorno quando a exceção sobe até o framework:

```java
@ResponseStatus(HttpStatus.NOT_FOUND)
public class ProdutoNaoEncontradoException extends RuntimeException {
    public ProdutoNaoEncontradoException(Long id) {
        super("Produto não encontrado: " + id);
    }
}
```

> [!warning] @ResponseStatus em exceções e @ControllerAdvice
> Se a exceção for tratada por um `@ExceptionHandler` em um `@ControllerAdvice`, a anotação `@ResponseStatus` da classe de exceção é **ignorada** — o status retornado é o do handler, não da anotação.

### O catálogo de status (200 / 201+Location / 204 / 400 / 404 / 409 / 422 / 500)

| Código | Nome | Quando usar |
|--------|------|-------------|
| 200 | OK | GET, PUT/PATCH com body de retorno, qualquer leitura bem-sucedida |
| 201 | Created | POST que cria recurso; **obrigatório** incluir `Location` |
| 204 | No Content | DELETE bem-sucedido, PUT/PATCH sem body de retorno |
| 400 | Bad Request | Parâmetro malformado, JSON inválido, erro de binding |
| 404 | Not Found | Recurso não existe |
| 409 | Conflict | Conflito de estado (ex.: duplicata, versão desatualizada) |
| 422 | Unprocessable Entity | Payload válido estruturalmente, mas inválido semanticamente. O *default* do Spring para falha de `@Valid`/Bean Validation é **400**; 422 é uma escolha explícita de design |
| 500 | Internal Server Error | Falha inesperada do servidor; nunca retornar intencionalmente |

## Na prática

Exemplo completo de um CRUD básico com os status corretos:

```java
@RestController
@RequestMapping("/produtos")
public class ProdutoController {

    private final ProdutoService service;

    public ProdutoController(ProdutoService service) {
        this.service = service;
    }

    // GET /produtos/{id} → 200 OK ou 404
    @GetMapping("/{id}")
    public ResponseEntity<ProdutoResponse> buscar(@PathVariable Long id) {
        return service.buscar(id)
            .map(ResponseEntity::ok)
            .orElse(ResponseEntity.notFound().build());
    }

    // POST /produtos → 201 Created + Location
    @PostMapping
    public ResponseEntity<ProdutoResponse> criar(
            @RequestBody @Valid ProdutoCriarRequest body,
            UriComponentsBuilder uriBuilder) {

        ProdutoResponse criado = service.criar(body);
        URI location = uriBuilder
            .path("/produtos/{id}")
            .buildAndExpand(criado.id())
            .toUri();

        return ResponseEntity.created(location).body(criado);
    }

    // PUT /produtos/{id} → 200 OK com body atualizado
    @PutMapping("/{id}")
    public ResponseEntity<ProdutoResponse> atualizar(
            @PathVariable Long id,
            @RequestBody @Valid ProdutoAtualizarRequest body) {

        ProdutoResponse atualizado = service.atualizar(id, body);
        return ResponseEntity.ok(atualizado);
    }

    // DELETE /produtos/{id} → 204 No Content
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deletar(@PathVariable Long id) {
        service.deletar(id);
        return ResponseEntity.noContent().build();
    }
}
```

Pontos importantes no exemplo:
- `UriComponentsBuilder` é injetado automaticamente pelo Spring MVC para construir a URI do `Location`.
- O retorno de `Optional.map(ResponseEntity::ok).orElse(notFound)` evita null e é idiomático.
- `ResponseEntity<Void>` deixa explícito que não há body no DELETE.

## Armadilhas

### (1) 200 pra tudo — inclusive erros

**Problema**: retornar 200 com um corpo de erro (`{"error": "not found"}`) viola o protocolo HTTP. Clientes não conseguem diferenciar sucesso de falha sem parsear o body, caches armazenam respostas de erro e ferramentas de APM reportam tudo como saudável.

```java
// Errado: 200 com body indicando erro
@GetMapping("/{id}")
public ResponseEntity<Object> buscar(@PathVariable Long id) {
    if (!service.existe(id)) {
        return ResponseEntity.ok(Map.of("error", "not found")); // 200 errado!
    }
    return ResponseEntity.ok(service.buscar(id));
}
```

```java
// Correto: 404 com body de erro (opcional)
@GetMapping("/{id}")
public ResponseEntity<ProdutoResponse> buscar(@PathVariable Long id) {
    return service.buscar(id)
        .map(ResponseEntity::ok)
        .orElse(ResponseEntity.notFound().build());
}
```

### (2) 201 sem header Location

**Problema**: RFC 9110 define que 201 Created **deve** incluir o header `Location` apontando para o recurso criado. Omitir o header obriga o cliente a fazer uma segunda requisição ou hardcodar a URL — acoplamento desnecessário.

```java
// Errado: 201 sem Location
return ResponseEntity.status(HttpStatus.CREATED).body(criado);

// Correto: created() já constrói o header Location
URI location = uriBuilder.path("/produtos/{id}").buildAndExpand(criado.id()).toUri();
return ResponseEntity.created(location).body(criado);
```

### (3) 200 no DELETE que devia ser 204

**Problema**: um DELETE que retorna 200 com body `"deleted"` ou `true` vai contra a convenção REST. Clientes que seguem a RFC esperam 204 sem body. Body em resposta de DELETE também desperdiça banda desnecessariamente.

```java
// Errado: 200 com body no DELETE
@DeleteMapping("/{id}")
public ResponseEntity<String> deletar(@PathVariable Long id) {
    service.deletar(id);
    return ResponseEntity.ok("deletado"); // 200 errado
}

// Correto: 204 sem body
@DeleteMapping("/{id}")
public ResponseEntity<Void> deletar(@PathVariable Long id) {
    service.deletar(id);
    return ResponseEntity.noContent().build();
}
```

### (4) Status code repetido no corpo em vez de no header

**Problema**: alguns padrões antigos incluem o status HTTP dentro do corpo JSON (`{"status": 200, "data": ...}`). Isso cria redundância e pode gerar inconsistência quando o status do envelope difere do status HTTP real — além de poluir o contrato da API.

```json
// Evitar: status duplicado no body
{
  "status": 200,
  "message": "success",
  "data": { ... }
}
```

O status pertence ao protocolo HTTP (cabeçalho de resposta). O body deve conter apenas os dados do domínio, ou um objeto de erro padronizado (RFC 9457 `ProblemDetail`) quando há falha.

## Em entrevista

### Frase pronta (inglês)

"In REST, the HTTP status code is part of the contract between server and client. I always return 201 with a `Location` header on resource creation, 204 with no body on deletion, and proper 4xx codes for client errors rather than burying the error inside a 200 response. Spring's `ResponseEntity` gives me full control over status, headers, and body in a single fluent call, while `@ResponseStatus` covers simple cases where I don't need dynamic headers."

"The most common mistake I've seen is treating HTTP status as optional documentation — returning 200 for everything and encoding success or failure only in the JSON body. This breaks HTTP caching, monitoring tools, and any client that follows the spec."

"When I need consistent error responses across the whole API, I combine `ResponseEntity` with `@ControllerAdvice` and `@ExceptionHandler`, so status codes are centralized rather than scattered across every controller method."

### Vocabulário

| Português | Inglês |
|-----------|--------|
| Código de status | Status code |
| Corpo da resposta | Response body |
| Cabeçalho de resposta | Response header |
| Recurso criado | Created resource |
| Resposta sem conteúdo | No content response |
| Entidade de resposta | Response entity |
| Método de fábrica | Factory method |
| Localização do recurso | Resource location |

## Veja também

- [[03-Dominios/Tecnologia/Java/Web e APIs REST/02 - @RestController e os mapeamentos|@RestController e os mapeamentos]]
- [[03-Dominios/Tecnologia/Java/Web e APIs REST/09 - Tratamento de exceções com @ControllerAdvice|Tratamento de exceções com @ControllerAdvice]] (status de erro)
- [[03-Dominios/Tecnologia/Java/Web e APIs REST/index|Web e APIs REST]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- Verbetes: [[03-Dominios/Tecnologia/Java/Dicionário de Java#@ResponseStatus|@ResponseStatus]], [[03-Dominios/Tecnologia/Java/Dicionário de Java#@ResponseBody|@ResponseBody]]

## Referências

- Spring Framework 6.x — ResponseEntity: https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-controller/ann-methods/responseentity.html
- Spring Framework 6.x — Error Responses (RFC 9457): https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-ann-rest-exceptions.html
- RFC 9110 — HTTP Semantics (status codes): https://www.rfc-editor.org/rfc/rfc9110
- RFC 9457 — Problem Details for HTTP APIs: https://www.rfc-editor.org/rfc/rfc9457
