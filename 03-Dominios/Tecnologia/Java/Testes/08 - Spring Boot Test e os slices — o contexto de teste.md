---
title: "Spring Boot Test e os slices — o contexto de teste"
created: 2026-06-11
updated: 2026-06-11
type: concept
progress: backlog
status: seedling
publish: true
fase: Adepto
tags:
  - java
  - testes
  - adepto
  - spring-test
aliases:
  - "Spring Boot Test"
  - "test slices"
---

# Spring Boot Test e os slices — o contexto de teste

> [!abstract] TL;DR
> O Spring Boot oferece **slices de teste** (`@WebMvcTest`/`@DataJpaTest`/`@JsonTest`/...) que carregam só uma fatia do contexto, e `@SpringBootTest`, que carrega o contexto **inteiro**. O contexto de teste **é um `ApplicationContext`** (o mesmo container do [[03-Dominios/Tecnologia/Java/Spring Core e Boot/06 - ApplicationContext — o container e seu ciclo|Galho 8]]) e é **cacheado entre testes** com a mesma config — por isso variar a config sem necessidade cria contextos novos e deixa a suíte lenta. A partir do Boot 3.4, `@MockitoBean` substituiu o `@MockBean` (deprecated).

## O que é

`spring-boot-starter-test` (mais precisamente, o módulo `spring-boot-test-autoconfigure`) traz um conjunto de anotações que montam um `ApplicationContext` de teste sob medida.

Há duas famílias:

- **`@SpringBootTest`** — sobe o contexto completo da aplicação, exatamente como em produção (todos os beans, toda a auto-configuration). É o teste de integração de alto nível.
- **Os slices** (`@WebMvcTest`, `@DataJpaTest`, `@JsonTest`, `@RestClientTest`, `@WebFluxTest`, `@JdbcTest`, `@DataRedisTest`, `@DataMongoTest`, ...) — sobem **apenas a fatia** de auto-configuration e os beans relevantes para aquela camada. O resto fica de fora.

A documentação resume a premissa de um teste completo assim:

> "A Spring Boot application is a Spring `ApplicationContext`, so nothing very special has to be done to test it beyond what you would normally do with a vanilla Spring context."

E justifica os slices logo em seguida:

> "Spring Boot's auto-configuration system works well for applications but can sometimes be a little too much for tests. It often helps to load only the parts of the configuration that are required to test a 'slice' of your application."

## Por que importa

Subir o mundo inteiro para testar uma única classe é caro: cada bean instanciado, cada auto-config avaliada, cada conexão aberta é tempo de boot multiplicado pelo número de contextos distintos da suíte.

Os slices resolvem isso de duas formas: carregam menos (boot mais rápido por contexto) e **isolam** a camada sob teste — um `@WebMvcTest` não toca no banco, um `@DataJpaTest` não sobe o `DispatcherServlet`. Você testa o controller sem a persistência atrapalhar, e vice-versa.

Mas há um efeito de segunda ordem que separa quem entende de quem decora: o **cache do contexto de teste**. O Spring reaproveita o mesmo `ApplicationContext` entre classes de teste que compartilham a mesma configuração. Saber escolher o slice certo *e* manter a config estável é o que mantém uma suíte de centenas de testes rápida.

## Como funciona

### Os slices: a tabela do que cada um carrega

Cada slice é uma meta-anotação que liga um subconjunto da auto-configuration. O `@WebMvcTest`, por exemplo, restringe o scan de beans à camada web — a doc é explícita:

> "auto-configures the Spring MVC infrastructure and limits scanned beans to `@Controller`, `@ControllerAdvice`, `@JsonComponent`, `Converter`, `GenericConverter`, `Filter`, `HandlerInterceptor`, `WebMvcConfigurer`, `WebMvcRegistrations`, and `HandlerMethodArgumentResolver`. Regular `@Component` and `@ConfigurationProperties` beans are not scanned."

Ou seja: seu `OrderService` (um `@Service`/`@Component`) **não** entra num `@WebMvcTest`. Se o controller depende dele, você fornece um mock — é aí que entra o `@MockitoBean`.

### @SpringBootTest (contexto completo) vs slice (parcial)

A diferença é o tamanho do contexto que sobe:

- **`@SpringBootTest`** parte de `@SpringBootApplication` (ou da config que você apontar) e aplica **toda** a auto-config. É o que você quer quando o teste cruza várias camadas (controller → service → repository → banco) e você precisa que a integração real funcione.
- **Slice** sobe só as auto-configs daquela fatia. Mais rápido, mais isolado, mas você precisa mockar as dependências de fora da fatia.

Regra de bolso: `@SpringBootTest` para testes de integração de fluxo; slice para testar uma camada com suas vizinhas mockadas; nenhum dos dois para testar lógica pura (aí é JUnit sem Spring — veja a Armadilha 1).

### O contexto de teste é um ApplicationContext — e o cache que acelera a suíte (Galho 8)

O contexto que esses testes montam **é exatamente** o `ApplicationContext` do [[03-Dominios/Tecnologia/Java/Spring Core e Boot/06 - ApplicationContext — o container e seu ciclo|Galho 8]] — mesmo container, mesmo ciclo de vida, mesma resolução de beans. Não há um "contexto de teste" mágico à parte.

A consequência prática é o **cache**. A doc:

> "Spring's test framework caches application contexts between tests. Therefore, as long as your tests share the same configuration (no matter how it is discovered), the potentially time-consuming process of loading the context happens only once."

A chave do cache é a configuração efetiva do teste (classes de config, profiles ativos, properties, qual slice, mocks declarados, etc.). Duas classes de teste com a **mesma** chave reusam o **mesmo** `ApplicationContext` — sobe uma vez só. Cada variação na chave força um contexto novo. Numa suíte grande, controlar quantos contextos distintos existem é o que define se ela roda em segundos ou minutos.

### @MockitoBean (substituiu @MockBean) e @ActiveProfiles

Quando um bean da fatia depende de algo que está **fora** dela (ou de algo que você quer simular), você substitui esse bean no contexto por um mock:

> "Spring Framework includes a `@MockitoBean` annotation that can be used to define a Mockito mock for a bean inside your `ApplicationContext`. Additionally, `@MockitoSpyBean` can be used to define a Mockito spy."

**Importante (Boot 3.4+):** `@MockitoBean` é do `spring-framework` (pacote `org.springframework.test.context.bean.override.mockito`) e **substitui** o antigo `@MockBean` do Spring Boot, agora **deprecated**. Código novo usa `@MockitoBean`/`@MockitoSpyBean`.

Detalhe que pega gente: `@MockitoBean` **muda a chave do cache** — um contexto com um mock declarado é diferente de um sem. Isso é desejável, mas reforça a Armadilha 2.

`@ActiveProfiles("test")` ativa um ou mais profiles durante o teste, fazendo subir as configs específicas (`application-test.yml`, beans anotados com `@Profile("test")`, etc.). Também faz parte da chave do cache — então mantenha os profiles consistentes entre classes que deveriam compartilhar contexto.

## Na prática

| Slice | O que carrega | Use case |
| --- | --- | --- |
| `@SpringBootTest` | contexto completo (toda auto-config) | integração de ponta a ponta |
| `@WebMvcTest` | camada MVC (`@Controller`, advice, conversores, filtros) + `MockMvc` | testar um controller, mockando o service |
| `@DataJpaTest` | JPA, repositórios, EntityManager, banco em memória | testar queries/repositories |
| `@JsonTest` | serialização/desserialização JSON (Jackson, etc.) | testar (de)serialização de DTOs |
| `@RestClientTest` | `RestClient`/`RestTemplate` + servidor mockado | testar um cliente HTTP |
| `@WebFluxTest` | camada WebFlux + `WebTestClient` | testar controllers reativos |
| `@JdbcTest` | `JdbcTemplate` + DataSource em memória | testar acesso JDBC puro |
| `@DataRedisTest` | infraestrutura Redis | testar repositórios Redis |

Contexto completo, com profile de teste:

```java
@SpringBootTest
@ActiveProfiles("test")
class OrderIntegrationTest {

    @Autowired
    private OrderService orderService;

    @Test
    void createsOrderEndToEnd() {
        Order order = orderService.create(new OrderRequest("SKU-1", 2));
        assertThat(order.getId()).isNotNull();
        assertThat(order.getStatus()).isEqualTo(OrderStatus.CREATED);
    }
}
```

Slice da camada web, com o service mockado via `@MockitoBean`:

```java
@WebMvcTest(OrderController.class)
class OrderControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockitoBean
    private OrderService orderService; // fora da fatia web → entra como mock

    @Test
    void returnsOrderById() throws Exception {
        when(orderService.findById(42L))
            .thenReturn(new Order(42L, OrderStatus.CREATED));

        mockMvc.perform(get("/orders/42"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.id").value(42));
    }
}
```

> [!info] Auto-configuration por trás dos slices
> Cada slice é, no fundo, uma seleção de auto-configs ligadas/desligadas — o mesmo mecanismo de [[03-Dominios/Tecnologia/Java/Spring Core e Boot/15 - Auto-configuration e starters|auto-configuration e starters]] do Galho 8, só que recortado para uma camada. Não há motor novo aqui; há um recorte do motor que você já conhece.

## Armadilhas

### (1) `@SpringBootTest` para testar um método isolado

Subir o contexto inteiro para verificar uma regra de negócio pura é desperdício — carrega o mundo (banco, web, mensageria) para exercitar um `if`.

```java
// ❌ contexto completo só para testar um cálculo
@SpringBootTest
class DiscountTest {
    @Autowired OrderService orderService;

    @Test
    void appliesTenPercent() {
        assertThat(orderService.discount(100)).isEqualTo(90);
    }
}
```

**Fix:** se a lógica não precisa de Spring, teste sem Spring (JUnit puro, instanciando a classe). Se precisa de uma camada só, use o slice correspondente. Reserve `@SpringBootTest` para integração real entre camadas.

```java
// ✅ sem Spring: instantânea e isolada
class DiscountTest {
    private final OrderService orderService = new OrderService(/* deps mockadas */);

    @Test
    void appliesTenPercent() {
        assertThat(orderService.discount(100)).isEqualTo(90);
    }
}
```

### (2) Config diferente por classe de teste quebra o cache do contexto

Cada variação na configuração efetiva (properties, profiles, mocks, `@TestConfiguration` ad-hoc) cria uma **chave de cache nova** — e, portanto, um `ApplicationContext` novo, com seu custo de boot.

```java
// ❌ três classes, três contextos distintos — três boots
@SpringBootTest @ActiveProfiles("test")            class A { /* ... */ }
@SpringBootTest @TestPropertySource(properties = "feature.x=true") class B { /* ... */ }
@SpringBootTest(properties = "server.port=0")      class C { /* ... */ }
```

**Fix:** padronize a configuração entre classes que deveriam compartilhar contexto — uma classe-base anotada, um profile comum, properties no `application-test.yml` em vez de espalhadas em cada teste. Quanto **menos** chaves distintas, mais reúso de contexto e mais rápida a suíte. Customize só quando o teste realmente exige.

### (3) `@MockBean` (deprecated no Boot 3.4+)

`@MockBean` (e `@SpyBean`) do `org.springframework.boot.test.mock.mockito` está **deprecated** desde o Spring Boot 3.4.

```java
// ❌ deprecated
import org.springframework.boot.test.mock.mockito.MockBean;

@WebMvcTest(OrderController.class)
class OrderControllerTest {
    @MockBean OrderService orderService;
}
```

**Fix:** use `@MockitoBean` (e `@MockitoSpyBean`) do `org.springframework.test.context.bean.override.mockito` — a substituição oficial, agora no próprio Spring Framework.

```java
// ✅ Boot 3.4+
import org.springframework.test.context.bean.override.mockito.MockitoBean;

@WebMvcTest(OrderController.class)
class OrderControllerTest {
    @MockitoBean OrderService orderService;
}
```

## Em entrevista

### Frase pronta (inglês)

> Spring Boot gives you test slices like `@WebMvcTest` or `@DataJpaTest` that load only a portion of the context, versus `@SpringBootTest`, which boots the full application context. The test context is just a regular `ApplicationContext`, and Spring caches it across test classes that share the same configuration, so the expensive context startup happens only once. That's why I keep the test configuration as uniform as possible — every distinct profile, property, or mock declaration creates a new cache key and a new context. For dependencies outside the slice I use `@MockitoBean`, which replaced the now-deprecated `@MockBean` in Spring Boot 3.4.

### Vocabulário

| Termo (EN) | Tradução / sentido |
| --- | --- |
| test slice | fatia de teste — carrega só parte do contexto |
| application context | container de beans do Spring; também é o contexto de teste |
| context caching | reúso do contexto entre testes com a mesma config |
| full context | contexto completo, carregado por `@SpringBootTest` |
| cache key | configuração efetiva que identifica o contexto cacheado |
| mock bean | bean substituído por um mock (`@MockitoBean`) |
| active profile | profile ativo no teste (`@ActiveProfiles`) |
| auto-configuration | configuração automática recortada por cada slice |

## Veja também

- [[03-Dominios/Tecnologia/Java/Testes/09 - @WebMvcTest — testando controllers com MockMvc|@WebMvcTest]]
- [[03-Dominios/Tecnologia/Java/Testes/10 - @DataJpaTest — testando repositories|@DataJpaTest]]
- [[03-Dominios/Tecnologia/Java/Spring Core e Boot/06 - ApplicationContext — o container e seu ciclo|ApplicationContext — o container e seu ciclo]]
- [[03-Dominios/Tecnologia/Java/Spring Core e Boot/15 - Auto-configuration e starters|Auto-configuration e starters]]
- [[03-Dominios/Tecnologia/Java/Testes/index|Testes (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java]]

## Referências

- Spring Boot Reference — Testing Spring Boot Applications: https://docs.spring.io/spring-boot/reference/testing/spring-boot-applications.html
