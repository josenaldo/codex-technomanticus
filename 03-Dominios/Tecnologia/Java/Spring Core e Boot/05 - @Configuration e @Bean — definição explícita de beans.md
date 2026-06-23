---
title: "@Configuration e @Bean — definição explícita de beans"
created: 2026-06-08
updated: 2026-06-08
type: concept
progress: backlog
status: seedling
publish: true
fase: iniciado
tags:
  - java
  - spring
  - iniciado
  - beans
aliases:
  - "@Configuration"
  - "@Bean"
---

# @Configuration e @Bean — definição explícita de beans

> [!abstract] TL;DR
> Além de detectar classes via component scanning, o Spring permite declarar beans **explicitamente**: basta criar uma classe anotada com `@Configuration` e definir métodos anotados com `@Bean`. Cada método retorna uma instância que o container registra e gerencia. Essa abordagem é indispensável para configurar bibliotecas externas (que você não pode anotar), centralizar construção complexa e fazer overrides pontuais. O detalhe crítico está no **modo full vs lite** (`proxyBeanMethods`): no modo full (padrão), o Spring envolve a classe com CGLIB e intercepta chamadas entre métodos `@Bean`, garantindo o singleton; no modo lite, não há proxy e cada chamada direta cria uma nova instância.

## O que é

`@Configuration` é uma anotação de nível de classe que marca o objeto como **fonte de definições de beans** para o container. Dentro dela, cada método anotado com `@Bean` representa uma receita de criação: o nome do método vira o ID do bean, o tipo de retorno vira o tipo registrado, e o corpo do método contém a lógica de instanciação.

```java
@Configuration
public class AppConfig {

    @Bean
    public OrderService orderService() {
        return new OrderServiceImpl();
    }
}
```

O container chama esse método **uma única vez** (por escopo) e armazena o resultado. Qualquer componente que precise de `OrderService` receberá a mesma instância gerenciada.

## Por que importa

O component scanning (`@Component`, `@Service`, etc.) só funciona com classes **que você controla** — você adiciona a anotação e o Spring as detecta automaticamente. Quando a classe pertence a uma biblioteca externa (Jackson, Resilience4j, um cliente HTTP), você não pode anotá-la. É aí que `@Configuration` + `@Bean` entra: você escreve o código de instanciação explicitamente e o Spring assume o gerenciamento do objeto resultante.

Além disso, construções complexas — configuração condicional, múltiplos construtores, parâmetros derivados de propriedades — ficam mais legíveis em um método `@Bean` do que dispersas em construtores e `@Value` espalhados pela aplicação.

## Como funciona

### `@Configuration` + `@Bean`: declarar explicitamente

O fluxo básico:

1. O container encontra a classe `@Configuration` (via scanning ou passagem direta ao `AnnotationConfigApplicationContext`).
2. Para cada método `@Bean`, ele gera uma definição de bean com o nome e tipo correspondentes.
3. Na primeira solicitação do bean, o container invoca o método e armazena o resultado.

Dependências entre beans são declaradas como **parâmetros do método** — o container os injeta automaticamente:

```java
@Configuration
public class OrderConfig {

    @Bean
    public ProductRepository productRepository(DataSource dataSource) {
        return new JdbcProductRepository(dataSource);
    }

    @Bean
    public OrderService orderService(ProductRepository productRepository) {
        return new OrderServiceImpl(productRepository);
    }
}
```

### Quando usar (libs externas, construção complexa, override) vs component scanning

| Situação | Abordagem recomendada |
|---|---|
| Classe própria, simples | `@Component` / estereótipo + scanning |
| Classe de lib externa (Jackson, OkHttp…) | `@Bean` em `@Configuration` |
| Construção com lógica condicional | `@Bean` em `@Configuration` |
| Override de bean já registrado | `@Bean` com `@Primary` ou `@Qualifier` |
| Múltiplos beans do mesmo tipo | Vários métodos `@Bean` com nomes distintos |

### `@Import` e composição de configs

Configurations grandes podem ser divididas em classes menores e compostas com `@Import`:

```java
@Configuration
@Import({ DatabaseConfig.class, SecurityConfig.class })
public class AppConfig {
    // beans desta classe + os importados de DatabaseConfig e SecurityConfig
}
```

Isso evita uma única classe de configuração monolítica e facilita testes que carregam apenas um subconjunto das configs.

### Full vs lite mode (`proxyBeanMethods`)

Por padrão (`proxyBeanMethods = true`), o Spring gera em tempo de inicialização uma **subclasse CGLIB** da sua `@Configuration`. Essa subclasse intercepta toda chamada a um método `@Bean` e verifica primeiro se o bean já existe no container — retornando o singleton em vez de criar uma nova instância.

```java
@Configuration  // full mode (padrão)
public class AppConfig {

    @Bean
    public CustomerRepository customerRepository() {
        return new JdbcCustomerRepository();
    }

    @Bean
    public CustomerService customerService() {
        // Em full mode: retorna o MESMO singleton já no container
        return new CustomerServiceImpl(customerRepository());
    }
}
```

No **lite mode** (`proxyBeanMethods = false`), não há proxy CGLIB. Cada chamada a `customerRepository()` dentro do código executa o método Java normalmente, criando uma **nova instância**:

```java
@Configuration(proxyBeanMethods = false)  // lite mode
public class AppConfig {

    @Bean
    public CustomerRepository customerRepository() {
        return new JdbcCustomerRepository();
    }

    @Bean
    public CustomerService customerService(CustomerRepository repo) {
        // Correto em lite mode: receba a dependência via parâmetro
        return new CustomerServiceImpl(repo);
    }
}
```

> [!tip] Regra prática
> Em lite mode, **sempre declare dependências como parâmetros** do método `@Bean`. Nunca chame outro método `@Bean` diretamente.

## Na prática

Cenário: configurar um `ObjectMapper` (Jackson) e um `RestClient` (Spring 6+) — classes de bibliotecas externas que você não pode anotar com `@Component`.

```java
@Configuration
public class HttpClientConfig {

    @Bean
    public ObjectMapper objectMapper() {
        return JsonMapper.builder()
                .addModule(new JavaTimeModule())
                .disable(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS)
                .build();
    }

    @Bean
    public RestClient orderApiClient(RestClient.Builder builder) {
        return builder
                .baseUrl("https://api.orders.example.com")
                .defaultHeader(HttpHeaders.ACCEPT, MediaType.APPLICATION_JSON_VALUE)
                .build();
    }
}
```

Agora qualquer bean que precise de `ObjectMapper` ou `RestClient` simplesmente declara o tipo como parâmetro do construtor — o Spring injeta os beans definidos acima.

## Armadilhas

### (1) Chamar método `@Bean` diretamente em lite mode

**Sintoma**: dois serviços distintos recebem instâncias **diferentes** do repositório, quebrando consistência transacional ou estado compartilhado.

```java
@Configuration(proxyBeanMethods = false)  // lite mode
public class AppConfig {

    @Bean
    public ProductRepository productRepository() {
        return new JdbcProductRepository();  // Nova instância a cada chamada!
    }

    @Bean
    public OrderService orderService() {
        return new OrderServiceImpl(productRepository());  // ERRADO em lite mode
    }

    @Bean
    public ReportService reportService() {
        return new ReportServiceImpl(productRepository());  // Outra instância!
    }
}
```

**Fix**: declare a dependência como parâmetro — o container garante o singleton:

```java
@Bean
public OrderService orderService(ProductRepository productRepository) {
    return new OrderServiceImpl(productRepository);  // Correto
}
```

### (2) `@Bean` em `@Component` não é o mesmo que em `@Configuration`

Colocar `@Bean` em uma classe `@Component` (ou `@Service`, `@Controller`) funciona — o bean é registrado — mas **não há proxy CGLIB**. O comportamento é equivalente ao lite mode, mesmo sem declarar `proxyBeanMethods = false`. Chamadas entre métodos `@Bean` dentro de um `@Component` criam novas instâncias em vez de retornar o singleton.

```java
@Component  // Não é @Configuration!
public class AppBeans {

    @Bean
    public CustomerRepository customerRepository() {
        return new JdbcCustomerRepository();
    }

    @Bean
    public CustomerService customerService() {
        // Cria uma NOVA instância de CustomerRepository — não o bean registrado
        return new CustomerServiceImpl(customerRepository());
    }
}
```

**Fix**: use `@Configuration` quando precisar de inter-bean method calls, ou use parâmetros de método em qualquer dos dois casos.

## Em entrevista

### Frase pronta (inglês)

"In Spring, you use `@Configuration` with `@Bean` methods to explicitly define beans — this is the go-to approach when you need to configure third-party classes you can't annotate directly, or when the instantiation logic is too complex for a simple stereotype. The key subtlety is the `proxyBeanMethods` attribute: in full mode (the default), Spring wraps the configuration class with CGLIB so that inter-bean method calls return the container-managed singleton rather than creating a fresh instance each time. In lite mode, there's no proxy, so you must always take dependencies as method parameters instead of calling other `@Bean` methods directly."

### Vocabulário

| Termo PT | Termo EN |
| --- | --- |
| configuração explícita | explicit configuration |
| modo completo | full mode |
| modo enxuto | lite mode |
| chamada inter-bean | inter-bean method call |
| definição de bean | bean definition |
| subclasse em tempo de execução | CGLIB subclass / runtime proxy |
| métodos com proxy | proxied bean methods |
| importação de configuração | configuration import |

## Veja também

- [[03-Dominios/Tecnologia/Java/Spring Core e Boot/02 - IoC e injeção de dependência no Spring|IoC e injeção de dependência no Spring]]
- [[03-Dominios/Tecnologia/Java/Jakarta EE/06 - CDI — qualifiers, producers e eventos|CDI — qualifiers, producers e eventos]] — o `@Produces` do CDI resolve a mesma necessidade (fabricar objetos que não são beans anotáveis), mas com mecanismo próprio do padrão Jakarta
- [[03-Dominios/Tecnologia/Java/Spring Core e Boot/14 - Conditional beans — @Conditional e os @ConditionalOn|Conditional beans]] — combinando `@Bean` com `@ConditionalOnMissingBean` para registros opcionais
- [[03-Dominios/Tecnologia/Java/Spring Core e Boot/index|Spring Core e Boot (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#@Configuration|@Configuration]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#@Bean|@Bean]]

## Referências

- Spring Framework Reference — Java-based Container Configuration: https://docs.spring.io/spring-framework/reference/core/beans/java.html
- Spring Framework Reference — Using the `@Configuration` Annotation: https://docs.spring.io/spring-framework/reference/core/beans/java/configuration-annotation.html
