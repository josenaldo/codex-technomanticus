---
title: "Serialização JSON com Jackson"
created: 2026-06-08
updated: 2026-06-09
type: concept
progress: backlog
status: seedling
publish: true
fase: iniciado
tags:
  - java
  - web
  - iniciado
  - json
aliases:
  - "Jackson no Spring MVC"
---

# Serialização JSON com Jackson

> [!abstract] TL;DR
> O Spring serializa o retorno de um handler em JSON via `MappingJackson2HttpMessageConverter`, que envolve o Jackson internamente. Sempre que `@ResponseBody` (ou `@RestController`) está presente e o Jackson está no classpath, o retorno do método vira JSON automaticamente. Regra de ouro: **exponha DTOs, nunca entidades JPA**. Isso evita serialização de proxies lazy, ciclos de relacionamento e vazamento de campos internos.

## O que é

Jackson é a biblioteca Java de serialização/desserialização JSON mais usada no ecossistema Spring. O Spring MVC delega a conversão de objetos Java ↔ JSON ao `MappingJackson2HttpMessageConverter`, que fica registrado como conversor padrão quando o Jackson está no classpath (o que acontece automaticamente com o `spring-boot-starter-web`).

A integração funciona sem nenhuma configuração manual: o Spring Boot detecta o Jackson, registra o conversor e disponibiliza um `ObjectMapper` pré-configurado com suporte a tipos Java modernos — incluindo `java.time.*` via `JavaTimeModule`.

## Por que importa

- **Ubíquo em APIs REST**: toda resposta de um `@RestController` passa pelo Jackson, seja um objeto simples, uma lista ou um `ResponseEntity`.
- **Controle fino de payload**: as anotações Jackson permitem renomear campos, ocultar dados sensíveis, controlar valores nulos e formatar datas — sem alterar o modelo de domínio.
- **Segurança por design**: expor diretamente uma entidade JPA pode vazar campos de auditoria, senhas hasheadas ou estruturas internas. DTOs delimitam exatamente o contrato da API.
- **Compatibilidade com frontends**: o Jackson serializa `LocalDateTime` como string ISO-8601 quando corretamente configurado, o que é o formato esperado pelo JavaScript.

## Como funciona

### @ResponseBody e o converter Jackson padrão

Quando um método de controller retorna um objeto Java e está anotado com `@ResponseBody` (ou quando a classe tem `@RestController`), o Spring dispara o processo de negociação de conteúdo e escolhe o conversor adequado. Para `application/json`, ele usa o `MappingJackson2HttpMessageConverter`.

```java
@RestController
@RequestMapping("/orders")
public class OrderController {

    private final OrderService orderService;

    public OrderController(OrderService orderService) {
        this.orderService = orderService;
    }

    @GetMapping("/{id}")
    public OrderDto findById(@PathVariable Long id) {
        // O Spring serializa OrderDto → JSON automaticamente
        return orderService.findById(id);
    }
}
```

O fluxo interno é:

1. O dispatcher invoca o método do controller.
2. O retorno (`OrderDto`) é interceptado pelo `HandlerMethodReturnValueHandler`.
3. O `MappingJackson2HttpMessageConverter` verifica se consegue escrever o tipo para `application/json`.
4. O `ObjectMapper` serializa o objeto e escreve no `HttpServletResponse`.

Para customizar a serialização, você ajusta o `ObjectMapper` via `Jackson2ObjectMapperBuilderCustomizer` (ou pelas propriedades `spring.jackson.*`) — o Spring Boot aplica a customização ao `MappingJackson2HttpMessageConverter` padrão, sem você precisar registrar o conversor à mão.

### Anotações Jackson (@JsonProperty, @JsonIgnore, @JsonInclude, @JsonFormat)

As anotações Jackson controlam como os campos são serializados/desserializados. Podem ser colocadas nos campos, getters ou no próprio record/classe.

| Anotação | Propósito |
|---|---|
| `@JsonProperty("nome")` | Renomeia o campo no JSON |
| `@JsonIgnore` | Exclui o campo da serialização e desserialização |
| `@JsonInclude(NON_NULL)` | Omite o campo quando o valor for `null` |
| `@JsonInclude(NON_EMPTY)` | Omite o campo quando `null` ou coleção/string vazia |
| `@JsonFormat(pattern = "...")` | Define formato de data/hora como string |
| `@JsonAlias({"alias1", "alias2"})` | Aceita nomes alternativos na desserialização |

Exemplo com record (DTO moderno):

```java
import com.fasterxml.jackson.annotation.JsonFormat;
import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import java.time.LocalDateTime;
import java.math.BigDecimal;

@JsonInclude(JsonInclude.Include.NON_NULL)
public record OrderDto(

    @JsonProperty("order_id")
    Long id,

    @JsonProperty("customer_name")
    String customerName,

    BigDecimal totalAmount,

    @JsonFormat(pattern = "yyyy-MM-dd'T'HH:mm:ss")
    LocalDateTime createdAt,

    @JsonIgnore
    String internalTrackingCode
) {}
```

Payload gerado para uma instância com `internalTrackingCode = "XYZ"` e `totalAmount = null`:

```json
{
  "order_id": 42,
  "customer_name": "Alice",
  "createdAt": "2026-06-08T10:30:00"
}
```

Observe: `totalAmount` foi omitido por ser `null` (`NON_NULL`), e `internalTrackingCode` foi excluído pelo `@JsonIgnore`.

### DTO vs entidade: por que não vazar a entidade JPA

Usar a entidade JPA diretamente como retorno de um controller é um antipadrão com três consequências graves:

1. **LazyInitializationException**: coleções lazy (ex.: `@OneToMany(fetch = LAZY)`) podem não estar carregadas quando o Jackson tentar serializá-las fora de uma transação ativa.
2. **Ciclos de serialização**: relacionamentos bidirecionais (`@ManyToOne` ↔ `@OneToMany`) causam `StackOverflowError` ou loop infinito ao serializar.
3. **Over-exposure**: campos de auditoria (`createdBy`, `version`), colunas internas ou dados sensíveis são expostos sem querer.

A solução é sempre criar um DTO (preferencialmente como `record`) e converter a entidade para ele antes de retornar. A camada de persistência e suas regras ficam isoladas (o galho [[03-Dominios/Tecnologia/Java/Persistência de dados/10 - Projections e DTOs — não vazar a entidade|Persistência de dados]]).

```java
// Entidade JPA (não sai do service/repository)
@Entity
@Table(name = "orders")
public class Order {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String customerName;
    private BigDecimal totalAmount;
    private LocalDateTime createdAt;
    private String internalTrackingCode;  // campo interno, nunca expor

    // getters/setters omitidos por brevidade
}

// DTO que sai pela API
public record OrderDto(
    Long id,
    String customerName,
    BigDecimal totalAmount,
    LocalDateTime createdAt
) {}

// Conversão no service (ou num Mapper dedicado)
public OrderDto toDto(Order order) {
    return new OrderDto(
        order.getId(),
        order.getCustomerName(),
        order.getTotalAmount(),
        order.getCreatedAt()
    );
}
```

### Datas: JavaTimeModule e ISO-8601

O Spring Boot registra automaticamente o `JavaTimeModule` do Jackson, que ensina o `ObjectMapper` a lidar com tipos `java.time.*` (`LocalDate`, `LocalDateTime`, `ZonedDateTime`, `Instant`, etc.).

Por padrão, sem configuração adicional, o Jackson serializa datas como **array de números** (`[2026,6,8,10,30,0]`), o que é pouco legível. Para obter strings ISO-8601, basta adicionar ao `application.properties`:

```properties
spring.jackson.serialization.write-dates-as-timestamps=false
```

Com isso, `LocalDateTime.of(2026, 6, 8, 10, 30)` vira `"2026-06-08T10:30:00"` — formato nativo do JavaScript e do padrão ISO-8601.

Para sobrescrever o formato em um campo específico (independente da configuração global), usa-se `@JsonFormat`:

```java
@JsonFormat(pattern = "dd/MM/yyyy", timezone = "America/Sao_Paulo")
LocalDate deliveryDate;
```

> [!tip] Prefira ISO-8601 globalmente
> Configurar `write-dates-as-timestamps=false` no `application.properties` é a abordagem preferida — garante consistência em toda a API sem precisar anotar cada campo.

## Na prática

O cenário mais comum: uma entidade `Order` com campos internos que não devem sair pela API; um record `OrderDto` expondo apenas o necessário; `@JsonInclude(NON_NULL)` para omitir campos opcionais.

```java
import com.fasterxml.jackson.annotation.JsonFormat;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import java.math.BigDecimal;
import java.time.LocalDateTime;

@JsonInclude(JsonInclude.Include.NON_NULL)
public record OrderDto(

    Long id,

    @JsonProperty("customer")
    String customerName,

    BigDecimal total,

    @JsonFormat(pattern = "yyyy-MM-dd'T'HH:mm:ss")
    LocalDateTime placedAt,

    // campo opcional — só aparece no JSON se não for null
    String notes
) {}
```

Controller que usa o DTO:

```java
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/orders")
public class OrderController {

    private final OrderService orderService;

    public OrderController(OrderService orderService) {
        this.orderService = orderService;
    }

    @GetMapping("/{id}")
    public ResponseEntity<OrderDto> getOrder(@PathVariable Long id) {
        return orderService.findById(id)
            .map(ResponseEntity::ok)
            .orElse(ResponseEntity.notFound().build());
    }

    @GetMapping
    public List<OrderDto> listOrders() {
        return orderService.findAll();
    }
}
```

Exemplo de resposta JSON para um pedido sem `notes`:

```json
{
  "id": 42,
  "customer": "Alice",
  "total": 299.90,
  "placedAt": "2026-06-08T10:30:00"
}
```

O campo `notes` foi omitido porque era `null` e o DTO tem `@JsonInclude(NON_NULL)`.

## Armadilhas

### (1) Serializar entidade JPA diretamente

**Problema**: retornar uma entidade JPA num `@RestController` parece conveniente, mas abre três buracos:

- Coleções lazy disparam `LazyInitializationException` ao serem acessadas pelo Jackson fora da transação.
- Relacionamentos bidirecionais causam recursão infinita: `Order` → `Customer` → `List<Order>` → `Order` → ...
- Campos de uso interno (auditoria, versão, identificadores técnicos) são expostos inadvertidamente.

**Exemplo problemático**:

```java
// ERRADO — entidade diretamente no retorno
@GetMapping("/{id}")
public Order getOrder(@PathVariable Long id) {
    return orderRepository.findById(id).orElseThrow();
    // Jackson tenta serializar Order → acessa orders.items (lazy) → exceção
}
```

**Fix**: sempre converter para DTO antes de retornar.

```java
// CORRETO — DTO expõe apenas o necessário
@GetMapping("/{id}")
public OrderDto getOrder(@PathVariable Long id) {
    Order order = orderRepository.findById(id).orElseThrow();
    return orderMapper.toDto(order);
}
```

### (2) Data serializada como array de números

**Problema**: sem configuração, `LocalDateTime` vira `[2026,6,8,10,30,0]` no JSON. O frontend não sabe o que fazer com isso.

**Exemplo do payload problemático**:

```json
{
  "id": 1,
  "placedAt": [2026, 6, 8, 10, 30, 0]
}
```

**Fix**: adicionar ao `application.properties`:

```properties
spring.jackson.serialization.write-dates-as-timestamps=false
```

Resultado após o fix:

```json
{
  "id": 1,
  "placedAt": "2026-06-08T10:30:00"
}
```

### (3) Expor campo sensível por falta de DTO

**Problema**: mesmo sem relacionamentos lazy, a entidade pode ter campos que nunca deveriam sair pela API — senha (mesmo hasheada), tokens internos, flags de controle de workflow.

**Exemplo**:

```java
// Entidade com campo sensível
public class Customer {
    private Long id;
    private String name;
    private String passwordHash;  // NUNCA deve ir pra API
}
```

Se o controller retornar `Customer` diretamente, `passwordHash` aparece no JSON. Um `@JsonIgnore` no campo ajuda, mas é frágil: basta alguém remover a anotação ou adicionar um novo campo sensível e o vazamento está de volta.

**Fix estrutural**: usar DTO. O DTO define explicitamente o que sai — qualquer campo novo na entidade fica fora da API até ser adicionado conscientemente ao DTO.

```java
// DTO — apenas o que o frontend precisa
public record CustomerDto(Long id, String name) {}
```

## Em entrevista

### Frase pronta (inglês)

"In Spring MVC, when a controller method is annotated with `@ResponseBody` — or the class with `@RestController` — the return value is serialized to JSON by the `MappingJackson2HttpMessageConverter`, which wraps Jackson's `ObjectMapper`. Spring Boot auto-configures this converter and registers the `JavaTimeModule` so that `java.time` types are handled out of the box. The key best practice is to always return DTOs rather than JPA entities, because serializing entities directly can cause `LazyInitializationException`, infinite recursion from bidirectional relationships, and accidental exposure of internal fields. Jackson annotations like `@JsonProperty`, `@JsonIgnore`, and `@JsonInclude` give you fine-grained control over the JSON shape without changing your domain model."

### Vocabulário

| Português | Inglês |
|---|---|
| Conversor de mensagens | Message converter |
| Serialização / Desserialização | Serialization / Deserialization |
| Objeto de transferência de dados | Data Transfer Object (DTO) |
| Negociação de conteúdo | Content negotiation |
| Inicialização lazy | Lazy initialization |
| Vazamento de dados | Data leakage / Over-exposure |
| Ciclo de serialização | Serialization cycle / Circular reference |
| Módulo Java Time | JavaTimeModule |
| Formato ISO-8601 | ISO-8601 format |
| Propriedade de inclusão | Inclusion policy |

## Veja também

- [[03-Dominios/Tecnologia/Java/Web e APIs REST/04 - ResponseEntity e status codes|ResponseEntity e status codes]]
- [[03-Dominios/Tecnologia/Java/Web e APIs REST/07 - Content negotiation|Content negotiation]]
- [[03-Dominios/Tecnologia/Java/Web e APIs REST/index|Web e APIs REST]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- Verbetes: [[03-Dominios/Tecnologia/Java/Dicionário de Java#Jackson|Jackson]], [[03-Dominios/Tecnologia/Java/Dicionário de Java#HttpMessageConverter|HttpMessageConverter]]

Persistência JPA/Hibernate (incluindo mapeamentos lazy e relacionamentos bidirecionais) → [[03-Dominios/Tecnologia/Java/Persistência de dados/index|Galho 10 (Persistência de dados)]].

## Referências

- [Spring Framework 6.x — @ResponseBody](https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-controller/ann-methods/responsebody.html)
- [Spring Boot — Customizing Jackson](https://docs.spring.io/spring-boot/how-to/spring-mvc.html)
- [Jackson Annotations — JavaDoc 2.x](https://fasterxml.github.io/jackson-annotations/javadoc/2.9/com/fasterxml/jackson/annotation/package-summary.html)
- [Jackson Wiki — JacksonHome](https://github.com/FasterXML/jackson)
