---
title: "Beans e estereótipos — @Component, @Service, @Repository, @Controller"
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
  - "estereótipos Spring"
  - "@Component"
---

# Beans e estereótipos — @Component, @Service, @Repository, @Controller

> [!abstract] TL;DR
> **Bean** é qualquer objeto instanciado e gerenciado pelo container Spring (o ApplicationContext). As anotações `@Component`, `@Service`, `@Repository` e `@Controller` são **estereótipos**: elas dizem ao container "registre esta classe como bean via component scanning". Tecnicamente as quatro fazem a mesma coisa — registrar o bean — mas semanticamente cada uma comunica a camada onde a classe atua. A única que **adiciona comportamento real** é `@Repository`: ela ativa um post-processor que converte exceções de persistência em `DataAccessException`, uniformizando o tratamento de erros independente do ORM usado.

## O que é

O container Spring (ApplicationContext) precisa saber quais classes instanciar e gerenciar. Há duas formas de informar isso:

1. **Configuração explícita** — declarar beans manualmente com `@Bean` dentro de uma classe `@Configuration`.
2. **Component scanning** — anotar as classes com um estereótipo e deixar o Spring descobri-las automaticamente no classpath.

Os **estereótipos** são anotações que marcam uma classe como candidata ao component scanning. Todas são meta-anotadas com `@Component`, o que as torna reconhecíveis pelo scanner:

| Anotação | Camada semântica |
|---|---|
| `@Component` | Genérica — qualquer componente Spring |
| `@Service` | Camada de serviço / lógica de negócio |
| `@Repository` | Camada de persistência (DAO) |
| `@Controller` | Camada web / handler HTTP (detalhado no Galho 9, planejado) |

## Por que importa

Escolher o estereótipo correto vai além de documentação. O Spring e frameworks integrados usam essas anotações para aplicar comportamentos específicos:

- **`@Repository`** ativa o `PersistenceExceptionTranslationPostProcessor`, que intercepta exceções lançadas pela camada de persistência (Hibernate, JPA, JDBC) e as converte para a hierarquia `DataAccessException` do Spring. Sem isso, uma `HibernateException` ou `PersistenceException` vaza diretamente para camadas superiores — acoplando o código de negócio ao ORM escolhido.
- **`@Service`** não adiciona comportamento técnico hoje, mas é o ponto de entrada padrão para aspectos AOP transacionais (`@Transactional`) e interceptors, além de sinalizar claramente a camada.
- **`@Controller`** (e `@RestController`) são detectados pelo Spring MVC para registrar handlers de requisições HTTP — tema do Galho 9, planejado.

Para entrevistas sênior, a pergunta clássica é: **"Qual a diferença entre `@Component`, `@Service` e `@Repository`?"** Saber que `@Repository` é o único com comportamento técnico adicional diferencia a resposta.

## Como funciona

### Component scanning e `@ComponentScan` / `@SpringBootApplication`

O component scanning varre o classpath em busca de classes anotadas com estereótipos e registra suas definições de bean no ApplicationContext. Para ativá-lo, usa-se `@ComponentScan` em uma classe `@Configuration`:

```java
@Configuration
@ComponentScan(basePackages = "com.exemplo.pedido")
public class AppConfig { }
```

A anotação aceita múltiplos pacotes:

```java
@ComponentScan(basePackages = {"com.exemplo.pedido", "com.exemplo.catalogo"})
```

O scanner é recursivo: varre o pacote especificado e todos os seus subpacotes. Classes fora da árvore de pacotes declarada **não são encontradas** — armadilha comum discutida na seção de erros.

Em aplicações Spring Boot, `@SpringBootApplication` já inclui `@ComponentScan` implicitamente, usando o pacote da classe principal como raiz:

```java
@SpringBootApplication   // inclui @ComponentScan no pacote corrente
public class PedidoApplication {
    public static void main(String[] args) {
        SpringApplication.run(PedidoApplication.class, args);
    }
}
```

Isso significa que **todas as classes anotadas no mesmo pacote (e subpacotes) da classe principal** são detectadas automaticamente — sem nenhuma configuração extra.

### Os 4 estereótipos e o que cada um adiciona (`@Repository` → `DataAccessException`)

Internamente, `@Service`, `@Repository` e `@Controller` são anotações simples que carregam `@Component` como meta-anotação. O scanner detecta qualquer anotação que seja, direta ou indiretamente, meta-anotada com `@Component`.

```java
// Como @Service é definida internamente
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@Documented
@Component          // ← aqui está o gancho do scanner
public @interface Service {
    @AliasFor(annotation = Component.class)
    String value() default "";
}
```

O diferencial de `@Repository` é o bean `PersistenceExceptionTranslationPostProcessor`. Quando presente no contexto (registrado automaticamente com `@ComponentScan`), esse post-processor envolve os beans anotados com `@Repository` em um proxy AOP que captura exceções de persistência e as relança como subclasses de `DataAccessException`:

```
HibernateException  ─┐
PersistenceException ─┤  →  DataAccessException  (hierarquia Spring)
JdbcSQLException    ─┘
```

Resultado prático: a camada de serviço trata `DataAccessException` sem saber se o ORM é Hibernate, EclipseLink ou JDBC puro.

### `@Controller` / `@RestController`: handlers HTTP (citados — detalhe no Galho 9, planejado)

`@Controller` marca a classe para o dispatcher do Spring MVC, que mapeia métodos anotados com `@GetMapping`, `@PostMapping` etc. a URLs. `@RestController` combina `@Controller` + `@ResponseBody`, tornando cada método retornando diretamente o corpo da resposta HTTP (normalmente JSON). O funcionamento completo desses dois estereótipos é coberto no Galho 9 (Spring MVC e REST — planejado).

## Na prática

```java
// Camada de serviço — lógica de negócio
@Service
public class OrderService {

    private final OrderRepository orderRepository;

    // Injeção via construtor (preferida)
    public OrderService(OrderRepository orderRepository) {
        this.orderRepository = orderRepository;
    }

    public Order placeOrder(Order order) {
        // lógica de negócio
        return orderRepository.save(order);
    }
}
```

```java
// Camada de persistência — acesso a dados
@Repository
public class CustomerRepository {

    private final EntityManager em;

    public CustomerRepository(EntityManager em) {
        this.em = em;
    }

    public Customer findById(Long id) {
        return em.find(Customer.class, id);
    }

    // Se o EntityManager lançar PersistenceException aqui,
    // o proxy de @Repository a converte em DataAccessException
}
```

```java
// Componente genérico — não se encaixa em serviço nem repositório
@Component
public class ProductCodeGenerator {
    public String generate(String prefix) {
        return prefix + "-" + System.currentTimeMillis();
    }
}
```

> [!tip] Nome do bean
> Por padrão, o nome do bean é o nome simples da classe com a primeira letra minúscula: `OrderService` → `orderService`. É possível sobrescrever: `@Service("ordemPedido")`.

## Armadilhas

### (1) Classe fora do pacote escaneado — bean não registrado

**Problema:** a classe está anotada com `@Service` mas o Spring não a encontra. A aplicação sobe sem erros, mas ao tentar injetar o bean recebe `NoSuchBeanDefinitionException`.

**Causa:** a classe está em um pacote que não está sob a raiz definida pelo `@ComponentScan` (ou pelo pacote da classe `@SpringBootApplication`).

```
com.exemplo.pedido          ← raiz do scan (classe principal aqui)
  └── service/
       └── OrderService     ← encontrado ✓

com.util.codigo             ← fora da árvore
  └── ProductCodeGenerator  ← NÃO encontrado ✗
```

**Fix:** mover a classe para dentro da árvore de pacotes escaneada, ou adicionar o pacote externo ao `@ComponentScan`:

```java
@SpringBootApplication
@ComponentScan(basePackages = {"com.exemplo.pedido", "com.util.codigo"})
public class PedidoApplication { ... }
```

### (2) `@Component` onde cabia `@Repository` — perde a tradução de exceção

**Problema:** a classe acessa o banco de dados mas está anotada com `@Component`. O código compila e roda, mas exceções de persistência (ex.: `ConstraintViolationException`) chegam até a camada de serviço sem conversão para `DataAccessException`.

**Causa:** o `PersistenceExceptionTranslationPostProcessor` só envolve beans anotados com `@Repository`. Usando `@Component`, o proxy AOP de tradução não é aplicado.

```java
// ERRADO — perde tradução de exceção
@Component
public class CustomerRepository {
    // ...save() pode lançar HibernateException diretamente
}

// CORRETO
@Repository
public class CustomerRepository {
    // ...save() lança DataAccessException (já traduzida)
}
```

**Fix:** substituir `@Component` por `@Repository` em qualquer classe de acesso a dados.

## Em entrevista

### Frase pronta (inglês)

"In Spring, stereotype annotations like `@Component`, `@Service`, `@Repository`, and `@Controller` tell the component scanner to register the class as a managed bean. They are technically equivalent in terms of registration, but semantically distinct: each communicates the architectural layer the class belongs to. The only one that adds real runtime behavior is `@Repository`, which activates AOP-based exception translation — any persistence exception thrown inside a repository bean is automatically converted to a `DataAccessException`, decoupling the service layer from the underlying ORM. In Spring Boot applications, `@SpringBootApplication` already includes `@ComponentScan` pointing at the main class's package, so you rarely need to configure scanning explicitly."

### Vocabulário

| Termo | Definição |
|---|---|
| bean | Objeto instanciado e gerenciado pelo ApplicationContext do Spring |
| stereotype annotation | Anotação que marca uma classe para registro via component scanning (`@Component` e derivadas) |
| component scanning | Varredura automática do classpath para detectar e registrar beans |
| `@ComponentScan` | Anotação que ativa o component scanning e define os pacotes raiz a varrer |
| `DataAccessException` | Hierarquia de exceções não-checadas do Spring que abstrai erros de persistência de qualquer ORM |
| `PersistenceExceptionTranslationPostProcessor` | Bean post-processor que aplica um proxy AOP em `@Repository` para traduzir exceções de persistência |
| meta-annotation | Anotação aplicada a outra anotação; `@Component` é meta-anotação de `@Service`, `@Repository` e `@Controller` |
| `NoSuchBeanDefinitionException` | Exceção lançada quando o container não encontra um bean do tipo ou nome solicitado |

## Veja também

- [[03-Dominios/Java/Spring Core e Boot/02 - IoC e injeção de dependência no Spring|IoC e injeção de dependência no Spring]]
- [[03-Dominios/Java/Spring Core e Boot/04 - Tipos de injeção — constructor, setter, field|Tipos de injeção]]
- [[03-Dominios/Java/Jakarta EE/04 - CDI — beans e injeção|CDI — beans e injeção]] (bean discovery na spec)
- [[03-Dominios/Java/Spring Core e Boot/index|Spring Core e Boot (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Dicionário de Java#@Component / estereótipos Spring|@Component / estereótipos Spring]]
- [[03-Dominios/Java/Dicionário de Java#component scanning|component scanning]]

## Referências

- Spring Framework Reference — Classpath Scanning and Managed Components: <https://docs.spring.io/spring-framework/reference/core/beans/classpath-scanning.html>
