---
title: "Bean Validation"
created: 2026-06-07
updated: 2026-06-08
type: concept
progress: backlog
status: seedling
publish: true
fase: Adepto
tags:
  - java
  - jakarta-ee
  - adepto
  - validation
aliases:
  - "Bean Validation"
  - "Jakarta Validation"
  - "@Valid"
---

# Bean Validation

> [!abstract] TL;DR
> Bean Validation (Jakarta Validation 3.1) declara restrições no modelo com annotations e valida em um ponto centralizado — standalone via `Validator` programático ou integrada ao container (JAX-RS valida a request automaticamente e devolve 400 em caso de violação). O `@Valid` que você vê no Spring MVC é esta mesma spec por baixo ([[03-Dominios/Tecnologia/Java/Web e APIs REST/08 - Validação na borda|validação na borda no Spring MVC]]). Hibernate Validator 8.x/9.x é a implementação de referência.

---

## O que é

**Jakarta Validation 3.1** é a especificação de validação declarativa do Jakarta EE 11. Ela define:

- Um modelo de **annotations de restrição** (`@NotNull`, `@Size`, `@Pattern`…) aplicáveis a campos, getters, parâmetros, valores de retorno e — a partir da 3.1 — **record components**;
- Um contrato de **`Validator`** que executa as restrições e devolve `Set<ConstraintViolation<T>>`;
- Um mecanismo de **validação em cascata** (`@Valid`) para grafos de objetos;
- Um modelo de **constraint customizada** (`@Constraint` + `ConstraintValidator<A, T>`);
- **Groups** e `@GroupSequence` para validação condicional;
- **`ExecutableValidator`** para validação de parâmetros e retornos de métodos/construtores.

> [!info] Implementação de referência
> **Hibernate Validator** (8.0.x para EE 10 / 9.x para EE 11) é a implementação de referência da spec. Toda API usada nesta nota é `jakarta.validation.*` — agnóstica de implementação.

A 3.1 traz como novidade principal a **clarificação do suporte a Records** (JEP 395): record components podem receber constraints diretamente, e a validação acessa os accessors gerados automaticamente pelo compilador.

---

## Por que importa

O anti-pattern mais comum em sistemas legados é a **validação espalhada**: `if (name == null || name.isBlank()) throw ...` dentro de services, controllers e repositórios — cada camada re-valida à sua maneira, com mensagens inconsistentes.

Bean Validation resolve isso declarando as regras **no modelo**, perto dos dados:

```java
public class Order {
    @NotNull
    @Size(min = 1, max = 50)
    private String customerId;

    @Valid
    @NotEmpty
    private List<OrderItem> items;
}
```

A partir daí, qualquer camada integrada ao container (JAX-RS, CDI, JPA) valida automaticamente. Fora do container, basta chamar `validator.validate(order)`.

**Em entrevista**, duas perguntas clássicas emergem desta spec:

1. *"Onde você valida os dados?"* — resposta correta: nas camadas de entrada (parâmetros do resource JAX-RS) e no modelo de domínio, usando Bean Validation, não `if`s manuais.
2. *"Como você valida diferente em criação vs. atualização?"* — resposta: **groups**.

---

## Como funciona

### Constraints built-in

A spec define as seguintes constraints no pacote `jakarta.validation.constraints`:

| Constraint | Aplica a | O que valida |
|---|---|---|
| `@NotNull` | qualquer tipo | valor não é `null` (string vazia **passa**) |
| `@NotBlank` | `CharSequence` | não `null` e pelo menos 1 char não-espaço |
| `@NotEmpty` | `CharSequence`, `Collection`, `Map`, array | não `null` e tamanho > 0 |
| `@Size(min, max)` | `CharSequence`, `Collection`, `Map`, array | tamanho entre min e max |
| `@Pattern(regexp)` | `CharSequence` | casa com a expressão regular |
| `@Email` | `CharSequence` | formato de e-mail válido |
| `@Min(value)` | inteiros e `BigDecimal`/`BigInteger` | valor ≥ min |
| `@Max(value)` | inteiros e `BigDecimal`/`BigInteger` | valor ≤ max |
| `@DecimalMin(value, inclusive)` | numéricos e `CharSequence` | valor ≥ (ou >) decimal |
| `@DecimalMax(value, inclusive)` | numéricos e `CharSequence` | valor ≤ (ou <) decimal |
| `@Positive` | numéricos | valor > 0 |
| `@PositiveOrZero` | numéricos | valor ≥ 0 |
| `@Negative` | numéricos | valor < 0 |
| `@NegativeOrZero` | numéricos | valor ≤ 0 |
| `@Digits(integer, fraction)` | numéricos e `CharSequence` | máximo de dígitos inteiros e decimais |
| `@Future` | `Date`, `Calendar`, tipos `java.time` | data/hora no futuro |
| `@FutureOrPresent` | tipos temporais | data/hora agora ou no futuro |
| `@Past` | tipos temporais | data/hora no passado |
| `@PastOrPresent` | tipos temporais | data/hora agora ou no passado |
| `@AssertTrue` | `boolean` / `Boolean` | valor é `true` |
| `@AssertFalse` | `boolean` / `Boolean` | valor é `false` |
| `@Null` | qualquer tipo | valor é `null` |

> [!tip] As três "nots" — diferença crucial
> - `@NotNull` — `null` é inválido, `""` é válido.
> - `@NotEmpty` — `null` e `""` são inválidos, `" "` (só espaço) é válido.
> - `@NotBlank` — `null`, `""` e `" "` são todos inválidos. Use em strings de texto livre.

---

### Onde anotar

As constraints podem ser colocadas em:

| Local | Exemplo |
|---|---|
| Campo de instância | `@NotNull private String name;` |
| Getter (property) | `@Email public String getEmail()` |
| Parâmetro de método | `void save(@Valid @NotNull Order o)` |
| Valor de retorno de método | `@NotNull public Order find(Long id)` |
| Parâmetro de construtor | `Customer(@NotBlank String name)` |
| Record component *(3.1)* | `record Product(@NotBlank String sku, @Positive BigDecimal price) {}` |

**Records (Jakarta Validation 3.1):** a especificação 3.1 clarificou o suporte a records. Constraints anotadas nos components de um record são aplicadas via os accessors gerados automaticamente — o mecanismo é o mesmo da validação de getters, e o comportamento é compatível com `@Valid` em cascata.

---

### Cascata com `@Valid`

`@Valid` instrui o `Validator` a percorrer o grafo de objetos recursivamente:

```java
public class Order {
    @Valid                    // valida cada OrderItem da lista
    @NotEmpty
    private List<OrderItem> items;

    @Valid                    // valida o objeto Address aninhado
    @NotNull
    private Address shippingAddress;
}

public class OrderItem {
    @NotBlank
    private String productId;

    @Positive
    private int quantity;
}
```

`@Valid` também funciona em elementos de container:

```java
private List<@NotNull @Valid OrderItem> items;
```

Sem `@Valid`, o `Validator` para no campo `items` e verifica apenas as constraints do próprio campo (`@NotEmpty`) — os objetos `OrderItem` dentro da lista **não são validados**.

---

### Custom constraints

Uma constraint customizada requer duas peças:

**1. A annotation de constraint:**

```java
import jakarta.validation.Constraint;
import jakarta.validation.Payload;
import java.lang.annotation.*;

@Documented
@Constraint(validatedBy = SkuValidator.class)
@Target({ElementType.FIELD, ElementType.PARAMETER, ElementType.METHOD})
@Retention(RetentionPolicy.RUNTIME)
public @interface ValidSku {
    String message() default "SKU inválido: deve ter formato XXX-000";
    Class<?>[] groups() default {};
    Class<? extends Payload>[] payload() default {};
}
```

Os três atributos `message`, `groups` e `payload` são **obrigatórios** pela spec.

**2. O `ConstraintValidator`:**

```java
import jakarta.validation.ConstraintValidator;
import jakarta.validation.ConstraintValidatorContext;

public class SkuValidator implements ConstraintValidator<ValidSku, String> {

    private static final java.util.regex.Pattern SKU_PATTERN =
        java.util.regex.Pattern.compile("^[A-Z]{3}-\\d{3}$");

    @Override
    public void initialize(ValidSku annotation) {
        // acessa atributos da annotation se necessário
    }

    @Override
    public boolean isValid(String value, ConstraintValidatorContext ctx) {
        if (value == null) return true; // null é responsabilidade do @NotNull
        return SKU_PATTERN.matcher(value).matches();
    }
}
```

> [!note] Mensagens e interpolação
> O atributo `message` suporta interpolação com `{atributo}` da própria annotation (ex: `"deve ter entre {min} e {max} caracteres"`) e com resource bundles em `ValidationMessages.properties`.

---

### Groups e sequências

Groups permitem executar subconjuntos de constraints em contextos diferentes:

```java
// markers de grupo (interfaces vazias por convenção)
public interface OnCreate {}
public interface OnUpdate {}

public class Customer {
    @Null(groups = OnCreate.class)   // em criação, id deve ser null
    @NotNull(groups = OnUpdate.class) // em atualização, id é obrigatório
    private Long id;

    @NotBlank(groups = {OnCreate.class, OnUpdate.class})
    private String name;
}
```

Validação seletiva:

```java
// valida apenas regras do grupo OnCreate
Set<ConstraintViolation<Customer>> violations =
    validator.validate(customer, OnCreate.class);
```

**`@GroupSequence`** define a ordem de execução — o segundo grupo só é validado se o primeiro passar:

```java
@GroupSequence({OnCreate.class, OnUpdate.class})
public interface OrderedChecks {}
```

---

### Standalone vs. integrada

**API programática (standalone):**

```java
import jakarta.validation.Validation;
import jakarta.validation.Validator;
import jakarta.validation.ValidatorFactory;
import jakarta.validation.ConstraintViolation;
import java.util.Set;

ValidatorFactory factory = Validation.buildDefaultValidatorFactory();
Validator validator = factory.getValidator();

Order order = new Order();  // sem customerId, sem items
Set<ConstraintViolation<Order>> violations = validator.validate(order);

violations.forEach(v ->
    System.out.println(v.getPropertyPath() + " — " + v.getMessage())
);
// validator.validate() NUNCA lança exceção por si só fora do container
// — você precisa checar o Set e reagir
```

**Method validation com `ExecutableValidator` (CDI/container):**

Em ambientes CDI, a validação de métodos ocorre automaticamente via interceptors quando os parâmetros ou retornos têm constraints. O `ExecutableValidator` expõe a mesma lógica de forma programática:

```java
ExecutableValidator execVal = validator.forExecutables();
// valida parâmetros antes de invocar o método
Method method = OrderService.class.getMethod("save", Order.class);
Set<ConstraintViolation<OrderService>> v =
    execVal.validateParameters(service, method, new Object[]{order});
```

**Integração JAX-RS:**

Em recursos JAX-RS, anotar parâmetros ou o corpo com `@Valid` faz o container validar automaticamente antes de invocar o método. Quando a validação falha, o container produz uma resposta HTTP 400 (Bad Request):

```java
@POST
@Path("/orders")
@Consumes(MediaType.APPLICATION_JSON)
public Response createOrder(@Valid @NotNull Order order) {
    // só chega aqui se order for válido
    return Response.status(Response.Status.CREATED).entity(saved).build();
}
```

> [!info] Comportamento do 400 em JAX-RS
> A especificação JAX-RS define que exceções de validação resultam em HTTP 400. O comportamento exato (mensagens de erro no corpo da resposta, formato JSON/XML) depende da implementação — Jersey, RESTEasy e outros podem customizar o `ExceptionMapper<ConstraintViolationException>`.

---

## Na prática

```java
import jakarta.validation.Valid;
import jakarta.validation.constraints.*;
import jakarta.validation.Validation;
import jakarta.validation.Validator;
import jakarta.validation.ValidatorFactory;
import jakarta.validation.ConstraintViolation;
import jakarta.validation.Constraint;
import jakarta.validation.ConstraintValidator;
import jakarta.validation.ConstraintValidatorContext;
import jakarta.validation.Payload;
import jakarta.ws.rs.*;
import jakarta.ws.rs.core.*;
import java.math.BigDecimal;
import java.util.List;
import java.util.Set;
import java.lang.annotation.*;

// --- Modelo com constraints ---

public class Order {

    @NotNull
    @Size(min = 3, max = 50)
    private String customerId;

    @NotNull
    @DecimalMin(value = "0.01")
    private BigDecimal totalAmount;

    @Valid           // cascata: valida cada OrderItem
    @NotEmpty
    private List<OrderItem> items;

    // getters e setters omitidos
}

public class OrderItem {

    @ValidSku                        // constraint customizada
    private String sku;

    @Positive
    private int quantity;

    @DecimalMin("0.00")
    private BigDecimal unitPrice;
}

// --- Custom constraint: @ValidSku ---

@Documented
@Constraint(validatedBy = SkuValidator.class)
@Target({ElementType.FIELD, ElementType.PARAMETER})
@Retention(RetentionPolicy.RUNTIME)
@interface ValidSku {
    String message() default "SKU inválido: formato esperado XXX-000";
    Class<?>[] groups() default {};
    Class<? extends Payload>[] payload() default {};
}

class SkuValidator implements ConstraintValidator<ValidSku, String> {
    private static final java.util.regex.Pattern P =
        java.util.regex.Pattern.compile("^[A-Z]{3}-\\d{3}$");

    @Override
    public boolean isValid(String value, ConstraintValidatorContext ctx) {
        return value == null || P.matcher(value).matches();
    }
}

// --- Uso programático ---

class ValidationExample {
    public static void main(String[] args) {
        ValidatorFactory factory = Validation.buildDefaultValidatorFactory();
        Validator validator = factory.getValidator();

        Order order = new Order(); // customerId null, items null

        Set<ConstraintViolation<Order>> violations = validator.validate(order);
        if (!violations.isEmpty()) {
            violations.forEach(v ->
                System.out.println("[" + v.getPropertyPath() + "] " + v.getMessage())
            );
            throw new IllegalArgumentException("Order inválida: " + violations.size() + " violação(ões)");
        }
    }
}

// --- Recurso JAX-RS com @Valid (conecta nota 07) ---

@Path("/orders")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
class OrderResource {

    @POST
    public Response create(@Valid @NotNull Order order) {
        // container valida antes de chegar aqui;
        // se @Valid falhar → HTTP 400 automático
        return Response.status(Response.Status.CREATED).build();
    }
}
```

---

## Armadilhas

### (1) Chamar `validate()` e ignorar o retorno

`Validator.validate()` **não lança exceção sozinho** fora do container. Ele devolve um `Set<ConstraintViolation<T>>` que você deve inspecionar.

```java
// ERRADO — parece que "validou", mas nenhuma regra foi aplicada
validator.validate(order);
order.save(); // executa mesmo com dados inválidos

// CERTO
Set<ConstraintViolation<Order>> v = validator.validate(order);
if (!v.isEmpty()) {
    throw new ConstraintViolationException(v);
    // ou mapeie para a resposta de erro da sua API
}
```

---

### (2) Usar `@NotNull` onde a intenção era `@NotBlank`

`@NotNull` aceita strings vazias e com espaços em branco. Para texto livre (nome, descrição, e-mail), o correto quase sempre é `@NotBlank`.

```java
// ERRADO — aceita "   " como nome válido
@NotNull
private String customerName;

// CERTO
@NotBlank
private String customerName;
```

---

### (3) Esquecer `@Valid` no campo aninhado

Sem `@Valid`, o validator verifica as constraints do campo em si (`@NotNull`, `@NotEmpty`), mas **não percorre o grafo interno**. Os objetos aninhados ficam sem validação.

```java
// ERRADO — items não-nulos passam, mas seus campos nunca são checados
@NotEmpty
private List<OrderItem> items;

// CERTO — cascade explícita
@Valid
@NotEmpty
private List<OrderItem> items;
```

---

### (4) Lógica pesada ou I/O dentro de `ConstraintValidator`

O `isValid()` é chamado a cada execução de `validator.validate()` — potencialmente muitas vezes por request. Consultas ao banco, chamadas HTTP ou processamento caro dentro do validador degradam performance e tornam o validador frágil.

```java
// ERRADO — query ao banco dentro do validator
@Override
public boolean isValid(String cpf, ConstraintValidatorContext ctx) {
    return cpfRepository.findByCpf(cpf).isEmpty(); // I/O!
}

// CERTO — @ValidSku só verifica formato; unicidade vai para a camada de serviço
@Override
public boolean isValid(String sku, ConstraintValidatorContext ctx) {
    return sku == null || SKU_PATTERN.matcher(sku).matches(); // puro, rápido
}
```

---

## Em entrevista

### Frase pronta (inglês)

> "Bean Validation — now Jakarta Validation 3.1 — lets you declare constraints as annotations on your model classes and have them enforced at a single point, whether standalone through the programmatic `Validator` API or automatically by the container — JAX-RS intercepts invalid requests and returns HTTP 400 before your method even runs. Custom constraints are composed of a marker annotation with `@Constraint(validatedBy = ...)` and a `ConstraintValidator` implementation that keeps validation logic pure and free of side effects. For scenarios requiring different rules at creation versus update time, validation groups and `@GroupSequence` let you partition and sequence constraints without duplicating the model."

### Vocabulário

| Termo PT | Termo EN |
|---|---|
| Restrição / Constraint | Constraint |
| Violação de restrição | Constraint violation |
| Validação em cascata | Cascading validation |
| Grupo de validação | Validation group |
| Sequência de grupos | Group sequence |
| Validação de método | Method validation |
| Fábrica de validador | Validator factory |
| Constraint customizada | Custom constraint |
| Componente de record | Record component |
| Interpolação de mensagem | Message interpolation |

---

## Veja também

- [[04 - CDI — beans e injeção]]
- [[07 - JAX-RS — REST declarativo]]
- [[09 - JPA — a especificação de persistência]]
- [[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/11 - Annotations|Annotations (Galho 1)]]
- [[03-Dominios/Tecnologia/Java/Jakarta EE/index|Jakarta EE (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#Bean Validation (Jakarta Validation)|Bean Validation (Dicionário)]]

---

## Referências

- [Jakarta Validation 3.1 — Specification Page](https://jakarta.ee/specifications/bean-validation/3.1/) — acesso 2026-06-07
- [Jakarta Validation 3.1 — API Javadoc (`jakarta.validation`)](https://jakarta.ee/specifications/bean-validation/3.1/apidocs/jakarta/validation/package-summary) — acesso 2026-06-07
- [Jakarta Validation 3.1 — `ExecutableValidator` Javadoc](https://jakarta.ee/specifications/bean-validation/3.1/apidocs/jakarta/validation/executable/executablevalidator) — acesso 2026-06-07
- [Hibernate Validator 9.x — Reference Guide](https://docs.hibernate.org/stable/validator/reference/en-US/html_single/) — acesso 2026-06-07
- [Jakarta EE Specifications Index](https://jakarta.ee/specifications/) — acesso 2026-06-07
