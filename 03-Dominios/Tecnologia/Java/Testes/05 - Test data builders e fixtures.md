---
title: "Test data builders e fixtures"
created: 2026-06-11
updated: 2026-06-11
type: concept
progress: backlog
status: seedling
publish: true
fase: Iniciado
tags:
  - java
  - testes
  - iniciado
aliases:
  - "test data builders"
  - "fixtures de teste"
  - "object mother"
---

# Test data builders e fixtures

> [!abstract] TL;DR
> Test data builders constroem objetos de teste de forma fluente (`anOrder().withTotal(...).build()`), evitando construtores de 15 argumentos e setup duplicado espalhado pelos testes. Eles deixam cada teste legível e focado no que realmente importa para o cenário, em vez de afogá-lo em ruído de montagem. Bibliotecas como o **Instancio** vão além e geram objetos inteiros com defaults automáticos via reflexão, deixando você sobrescrever só os campos relevantes.

## O que é

Um **test data builder** é um objeto auxiliar, vivendo no código de teste, cujo único trabalho é fabricar instâncias de uma classe de domínio com valores sensatos por padrão. Em vez de chamar um construtor com dez parâmetros — metade dos quais irrelevante para o teste atual —, você escreve `anOrder().build()` e recebe um `Order` completo e válido.

O padrão tem um primo próximo, o **object mother**: uma classe (frequentemente com métodos estáticos) que oferece instâncias pré-configuradas, tipo `OrderMother.paidOrder()`. A diferença é de ênfase. O object mother entrega objetos prontos e nomeados; o builder entrega uma fábrica encadeável que você customiza ponto a ponto. Na prática, os dois se combinam: um builder com métodos semânticos é, de certa forma, um object mother fluente.

A motivação é antiga e simples: o código de teste também é código, e merece o mesmo cuidado com legibilidade e duplicação. Quando a montagem do dado domina o teste, a intenção do teste se perde.

## Por que importa

Sem builders, três problemas crescem juntos conforme a suíte de testes envelhece:

- **Construtores telescópicos.** Objetos de domínio reais têm muitos campos. Passar todos em cada teste é verboso e frágil: mude a assinatura do construtor e dezenas de testes quebram de uma vez, mesmo os que não se importam com o campo novo.
- **Setup duplicado.** O mesmo bloco de montagem aparece copiado em vinte testes. Quando a regra de negócio muda, você precisa caçar e ajustar todas as cópias.
- **Intenção soterrada.** Um teste deveria gritar *o que* está verificando. Se as primeiras quinze linhas só montam um pedido, o leitor precisa garimpar para achar a asserção que importa.

O builder resolve os três de uma vez. O construtor fica escondido atrás de defaults; a duplicação some porque a montagem mora num lugar só; e a intenção volta ao primeiro plano, porque o teste menciona apenas os atributos relevantes ao cenário.

## Como funciona

### O builder / object mother: defaults sensatos + overrides

A espinha dorsal de um builder são **defaults válidos**. Ao instanciar o builder, todos os campos já recebem valores plausíveis: um cliente qualquer, um total positivo, um status inicial coerente. O objeto resultante de `anOrder().build()`, sem nenhuma customização, deve ser válido por construção.

Sobre esses defaults, métodos `with...` permitem sobrescrever campo a campo. Cada `withTotal(...)` ou `withCustomer(...)` devolve o próprio builder, viabilizando o encadeamento fluente. O teste então declara apenas os desvios em relação ao padrão — exatamente os atributos que o cenário exige.

### Métodos semânticos (asPaid(), asCancelled()) que expressam intenção

Builders bons não param em setters genéricos. Eles oferecem métodos que codificam **estados de negócio** com nome falante: `asPaid()`, `asCancelled()`, `asShipped()`. Cada um ajusta o conjunto de campos coerente com aquele estado (status, data de pagamento, flags) de uma vez só.

A diferença de leitura é grande. Compare `anOrder().withStatus(CANCELLED).withCancelledAt(now)` com `anOrder().asCancelled()`. O segundo expressa a *intenção* — "um pedido cancelado" — em vez do *mecanismo*. O teste passa a falar a língua do domínio.

### @BeforeEach vs builder: quando cada um

`@BeforeEach` (JUnit 5) roda antes de cada teste e é o lugar clássico para preparar fixtures: dependências, mocks, recursos. Builder e `@BeforeEach` não competem — colaboram. A regra prática:

- Use **`@BeforeEach`** para o que é *infraestrutura comum a todos os testes da classe*: instanciar o sistema sob teste, configurar mocks compartilhados, abrir/limpar um recurso.
- Use **builders** para o *dado específico de cada cenário*. Cada teste chama `anOrder().asPaid().build()` localmente, deixando explícito o dado de que precisa.

O antipadrão é jogar dado de cenário no `@BeforeEach`: vira uma fixture genérica que serve mal a todos (veja Armadilhas).

### Geração automática: Instancio (menção)

Quando o objeto tem muitos campos irrelevantes ao teste e você só quer *algo válido*, escrever builders à mão pode ser exagero. O **Instancio** automatiza isso: via reflexão, ele popula todos os campos — inclusive objetos aninhados, genéricos e coleções — com valores aleatórios, e você sobrescreve só o que importa com `set()`, `generate()` ou `supply()`.

Os valores aleatórios são um recurso, não um bug: cada execução usa dados diferentes, o que pode revelar casos de borda que dados fixos esconderiam; quando um teste falha, o Instancio imprime um *seed* para reproduzir a execução. Builders manuais e Instancio coexistem: builders para os tipos centrais cujos estados de negócio você modela explicitamente; geração automática para os periféricos.

## Na prática

```java
// Builder neutro, vivendo no código de teste.
public class OrderBuilder {

    // Defaults sensatos: o objeto sai válido sem customização.
    private Customer customer = new Customer("default-customer");
    private BigDecimal total = new BigDecimal("100.00");
    private OrderStatus status = OrderStatus.NEW;
    private Instant paidAt = null;
    private Instant cancelledAt = null;

    // Ponto de entrada fluente.
    public static OrderBuilder anOrder() {
        return new OrderBuilder();
    }

    public OrderBuilder withCustomer(Customer customer) {
        this.customer = customer;
        return this;
    }

    public OrderBuilder withTotal(BigDecimal total) {
        this.total = total;
        return this;
    }

    // Métodos semânticos: expressam estados de negócio, não campos soltos.
    public OrderBuilder asPaid() {
        this.status = OrderStatus.PAID;
        this.paidAt = Instant.now();
        return this;
    }

    public OrderBuilder asCancelled() {
        this.status = OrderStatus.CANCELLED;
        this.cancelledAt = Instant.now();
        return this;
    }

    public Order build() {
        return new Order(customer, total, status, paidAt, cancelledAt);
    }
}
```

```java
import static com.example.test.OrderBuilder.anOrder;
import static org.assertj.core.api.Assertions.assertThat;

class RefundServiceTest {

    private final RefundService refundService = new RefundService();

    @Test
    void cancelledOrderIsNotRefundable() {
        // O teste menciona só o que importa: um pedido cancelado.
        Order order = anOrder().asCancelled().build();

        boolean refundable = refundService.isRefundable(order);

        assertThat(refundable).isFalse();
    }
}
```

A asserção fica em primeiro plano. O leitor entende em uma linha que o cenário é "pedido cancelado" — sem precisar inspecionar status, datas ou cliente.

## Armadilhas

### (1) Builder mutável compartilhado entre testes

Tentado a economizar, alguém transforma o builder num singleton estático ou guarda uma instância reaproveitada num campo da classe de teste. Como o builder é mutável, o estado configurado por um teste **vaza** para o seguinte, criando dependência de ordem e falhas intermitentes difíceis de diagnosticar.

```java
// RUIM: builder estático e mutável, compartilhado entre testes.
public class SharedBuilders {
    public static final OrderBuilder ORDER = new OrderBuilder(); // armadilha
}

// Teste A faz ORDER.asPaid()... e o Teste B herda um pedido pago sem saber.
```

**Fix:** sempre comece um builder *novo* por cenário, via fábrica (`anOrder()` retorna `new OrderBuilder()`). Cada teste customiza sua própria instância; nada é compartilhado. Se quiser garantir imutabilidade, faça cada `with...` retornar uma cópia em vez de mutar `this`.

### (2) Fixture gigante "pra tudo"

A outra tentação é criar uma única fixture monstro — um `@BeforeEach` que monta um grafo enorme de objetos "para qualquer teste usar". Cada teste passa a carregar dado irrelevante, e ninguém sabe quais campos importam para qual cenário. Mudar a fixture quebra testes por motivos que parecem mágicos.

```java
// RUIM: fixture genérica que serve mal a todos.
@BeforeEach
void setUp() {
    order = new Order(/* 15 campos preenchidos "pra dar conta de tudo" */);
    customer = new Customer(/* ... */);
    // ...e os testes nem usam metade disso.
}
```

**Fix:** prefira **builders específicos por cenário**, montados *dentro* de cada teste. Deixe o `@BeforeEach` só para infraestrutura genuinamente comum (sistema sob teste, mocks). Assim cada teste declara exatamente o dado de que depende, e nada mais.

## Em entrevista

### Frase pronta (inglês)

> Test code is still code, so I treat readability and duplication there as seriously as in production. I lean on test data builders — fluent factories like `anOrder().asCancelled().build()` — to hide telescoping constructors behind sensible defaults and let each test mention only the attributes that matter to its scenario. I add semantic methods such as `asPaid()` or `asCancelled()` so the test speaks the domain language instead of fiddling with individual fields, and I reserve `@BeforeEach` for shared infrastructure rather than scenario-specific data. When an object has many irrelevant fields, I reach for a library like Instancio to auto-generate a valid instance and override only what I care about.

### Vocabulário

| Termo (EN) | Significado |
| --- | --- |
| test data builder | fábrica fluente que monta objetos de teste com defaults sensatos |
| object mother | classe que fornece instâncias de teste pré-configuradas e nomeadas |
| fixture | dado/estado preparado antes de um teste rodar |
| sensible defaults | valores padrão plausíveis que tornam o objeto válido por construção |
| fluent interface | API encadeável onde cada método retorna o próprio objeto |
| telescoping constructor | construtor com muitos parâmetros, difícil de ler e frágil |
| semantic method | método cujo nome expressa um estado de negócio (`asPaid()`) |
| shared mutable state | estado compartilhado e mutável que vaza entre testes |

## Veja também

- [[03-Dominios/Tecnologia/Java/Testes/04 - Testes parametrizados e organização|Testes parametrizados e organização]]
- [[03-Dominios/Tecnologia/Java/Testes/06 - Mockito — mocks, stubbing e matchers|Mockito]]
- [[03-Dominios/Tecnologia/Java/Testes/21 - Capstone — a estratégia de testes de uma app Spring production-grade|Capstone de testes]]
- [[03-Dominios/Tecnologia/Java/Testes/index|Testes (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java]] (verbete test data builder)

## Referências

- Instancio — biblioteca de geração automática de dados de teste em Java: <https://www.instancio.org/>
