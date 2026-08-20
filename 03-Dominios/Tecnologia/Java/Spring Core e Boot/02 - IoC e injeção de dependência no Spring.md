---
title: "IoC e injeção de dependência no Spring"
created: 2026-06-08
updated: 2026-06-08
type: concept
progress: backlog
status: seedling
publish: true
fase: Iniciado
tags:
  - java
  - spring
  - iniciado
  - ioc
  - di
aliases:
  - "IoC no Spring"
  - "DI no Spring"
  - "Inversão de controle"
---

# IoC e injeção de dependência no Spring

> [!abstract] TL;DR
> **IoC** (inversão de controle) é o princípio em que o framework — e não o seu código — controla a **criação** e o **wiring** (a ligação) dos objetos. **DI** (injeção de dependência) é a forma concreta de implementar esse princípio: o container *injeta* nas suas classes as dependências de que elas precisam, em vez de elas mesmas as construírem.
>
> No Spring, quem faz isso é o **container IoC** (a `ApplicationContext`). É exatamente a mesma ideia da spec [[03-Dominios/Tecnologia/Java/Jakarta EE/04 - CDI — beans e injeção|CDI — beans e injeção]] do Galho 7 — só que com um container **próprio do Spring**, não com uma implementação de CDI. É isso que aquele `@Autowired` discreto esconde: uma máquina inteira que cria, configura e conecta objetos por você.

## O que é

Há dois conceitos empilhados aqui, e confundi-los é a primeira armadilha de toda entrevista.

**IoC (Inversion of Control) é o princípio.** Num programa "normal", o *seu* código está no controle: ele decide quando instanciar cada colaborador, com qual implementação, em que ordem. Com IoC, você **inverte** esse controle: entrega ao framework a responsabilidade de instanciar e montar o grafo de objetos. Você passa a declarar *o que* precisa; o framework decide *como e quando* prover. A documentação oficial do Spring abre o capítulo dizendo, sem rodeios, que ele cobre "Spring's Inversion of Control (IoC) container".

**DI (Dependency Injection) é a implementação.** IoC é abstrato demais para programar diretamente — ele se materializa de alguma forma. A forma que o Spring (e o CDI, e tantos outros) escolhe é a injeção de dependência: o container **injeta** as dependências de um objeto a partir de fora, em vez de o objeto criá-las ou buscá-las. Daí a relação de hierarquia:

- IoC = o **princípio** (controle invertido).
- DI = uma **técnica** que realiza esse princípio.

> [!info] Nem todo IoC é DI
> Service Locator, callbacks e templates também são formas de IoC. DI é apenas a mais usada — e a que o Spring adota como cidadã de primeira classe.

**O container é a peça central.** No Spring, o objeto que personifica o container IoC é a `ApplicationContext` (uma extensão do `BeanFactory` mais primitivo). É ele quem lê os *metadados de configuração*, **instancia**, **configura** e **monta** (*instantiate, configure, assemble*) os objetos que ele gerencia. Esses objetos gerenciados pelo container têm um nome: **beans**.

## Por que importa

- **Desacoplamento.** Suas classes deixam de depender de *implementações concretas* e passam a depender de *abstrações* (interfaces). Quem decide qual implementação concreta entra é o container, não o código que a usa. Trocar uma implementação por outra deixa de exigir recompilar quem a consome.
- **Testabilidade.** Se a dependência chega por injeção, um teste pode passar um *mock* ou *stub* trivialmente — basta instanciar a classe com o dublê no lugar do colaborador real. Sem DI, um `new` escondido dentro do método torna o teste refém da implementação concreta.
- **É a base de todo o galho.** Beans, estereótipos, escopos, autoconfiguração do Boot — tudo isso é construído *em cima* do container IoC. Entender IoC/DI primeiro é o que torna o resto do Spring legível, em vez de mágica.
- **Entrevista.** "Explique IoC e DI" é pergunta de aquecimento garantida para qualquer vaga que cite Spring. Saber separar princípio (IoC) de técnica (DI) — e dizer que DI não é a única forma de IoC — já te coloca acima da resposta decorada.

## Como funciona

### Antes e depois: acoplamento com `new` vs dependência injetada

Considere um `OrderService` que precisa de um `CustomerRepository`. **Sem** inversão de controle, o serviço cria a própria dependência:

```java
// ANTES — o serviço está no controle (acoplado)
public class OrderService {
    private final CustomerRepository repository;

    public OrderService() {
        // o serviço escolhe a implementação concreta e a constrói
        this.repository = new JdbcCustomerRepository();
    }
}
```

O problema não é o `new` em si — é *quem* o chama. Aqui o `OrderService` está amarrado a `JdbcCustomerRepository`: não dá para trocar por uma versão em memória num teste, nem por outra implementação em produção, sem editar e recompilar o serviço.

**Com** inversão de controle, o serviço apenas *declara* o que precisa e recebe pronto:

```java
// DEPOIS — o controle foi invertido (desacoplado)
public class OrderService {
    private final CustomerRepository repository;

    // declara a dependência; quem a fornece é problema de outrem
    public OrderService(CustomerRepository repository) {
        this.repository = repository;
    }
}
```

Repare no `final`: a dependência chega no construtor, é atribuída uma vez e nunca mais muda. O serviço não sabe — e não quer saber — se recebeu uma implementação JDBC, um mock ou um fake em memória. Essa ignorância é o desacoplamento na prática.

### O container: quem cria e conecta os beans

Mas se o `OrderService` não constrói o `CustomerRepository`, **quem** constrói? O container. No Spring, a `ApplicationContext`:

1. **Lê os metadados de configuração** — anotações (`@Component`, `@Bean`), classpath scanning, ou até XML legado. É a "receita" de quais objetos existem e como eles se ligam.
2. **Instancia** cada bean declarado.
3. **Resolve as dependências**: ao construir o `OrderService`, percebe que o construtor pede um `CustomerRepository`, procura no container um bean que satisfaça esse tipo e o passa adiante.
4. **Monta o grafo** completo de objetos, com tudo conectado, antes de entregar a aplicação pronta para rodar.

```text
            lê metadados
ApplicationContext ──────────▶ [ CustomerRepository ]  (cria o bean)
        │                              │
        │ injeta no construtor         │
        ▼                              ▼
   [ OrderService ] ◀──────────────────┘  (recebe a dependência pronta)
```

O `@Autowired` (e, desde o Spring 4.3, sua omissão em construtores únicos) é só o *marcador* que diz ao container: "este ponto precisa ser preenchido por você". A mecânica de como o container *lê* essas anotações via reflexão é assunto de [[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/11 - Annotations|Annotations]] (Galho 1) — aqui nos basta saber que o container as usa como instruções de montagem.

### Spring vs CDI: mesma ideia, container próprio

Se você veio do Galho 7, isso vai soar familiar: o [[03-Dominios/Tecnologia/Java/Jakarta EE/04 - CDI — beans e injeção|CDI — beans e injeção]] resolve exatamente o mesmo problema — beans gerenciados, injeção de dependência, um container que monta o grafo. A **ideia** é idêntica. O que muda é o **mecanismo**:

| Aspecto | CDI (Jakarta EE) | Spring |
| --- | --- | --- |
| Natureza | Uma **especificação** (com implementações: Weld, OpenWebBeans) | Um **framework** com container próprio |
| Container | `BeanManager` / `CDI` | `ApplicationContext` / `BeanFactory` |
| Anotação de injeção | `@Inject` | `@Autowired` (também aceita `@Inject`) |

> [!warning] O Spring NÃO é uma implementação de CDI
> Este é o ponto que mais gera confusão. O Spring **não** implementa a spec CDI — ele tem seu próprio modelo de container, anterior ao CDI inclusive. Por compatibilidade, o Spring *suporta* as anotações `jakarta.inject` (`@Inject`, `@Named`), mas o motor por baixo é dele. Dizer "Spring é a implementação de CDI" numa entrevista é um erro factual.

Não vamos re-explicar o CDI aqui — para o detalhe da spec, siga o wikilink. O assunto desta nota é o container do **Spring**.

## Na prática

O cenário mínimo: um `OrderService` que depende de um `CustomerRepository`, montado pelo container.

```java
// 1) Uma dependência declarada como bean (estereótipo @Repository)
@Repository
public class JdbcCustomerRepository implements CustomerRepository {
    @Override
    public Customer findById(Long id) {
        // ... acesso a dados
        return new Customer(id, "Ada Lovelace");
    }
}
```

```java
// 2) O serviço recebe a dependência por construtor — sem @Autowired
//    explícito, porque há um único construtor (Spring 4.3+)
@Service
public class OrderService {
    private final CustomerRepository repository;

    public OrderService(CustomerRepository repository) {
        this.repository = repository;
    }

    public Order placeOrder(Long customerId, Product product) {
        Customer customer = repository.findById(customerId);
        return new Order(customer, product);
    }
}
```

```java
// 3) O container sobe, lê os metadados e monta o grafo
@Configuration
@ComponentScan("com.example.shop")
public class AppConfig { }

public class Main {
    public static void main(String[] args) {
        ApplicationContext context =
            new AnnotationConfigApplicationContext(AppConfig.class);

        // pedimos um OrderService PRONTO — já com o repository injetado
        OrderService service = context.getBean(OrderService.class);
        Order order = service.placeOrder(42L, new Product("Livro"));
    }
}
```

```java
// 4) Testabilidade: sem o container, injetando um dublê direto
class OrderServiceTest {
    @Test
    void placeOrderUsesInjectedRepository() {
        CustomerRepository fake =
            id -> new Customer(id, "Cliente de Teste");

        // a DI por construtor torna isso trivial — nenhum 'new' escondido
        OrderService service = new OrderService(fake);

        Order order = service.placeOrder(7L, new Product("Caneta"));
        assertEquals("Cliente de Teste", order.getCustomer().getName());
    }
}
```

Repare no exemplo 4: porque a dependência **entra pelo construtor**, o teste não precisa do Spring nem de mock framework — passa um `fake` e pronto. Essa é a recompensa concreta da DI.

## Armadilhas

### (1) Dar `new` manual e contornar o container

```java
@Service
public class OrderService {
    // ARMADILHA: cria a própria dependência, ignorando o container
    private final CustomerRepository repository = new JdbcCustomerRepository();
}
```

**Por que dói:** o objeto criado com `new` **não** é um bean. Ele não recebe injeções, não participa de transações (`@Transactional`), não tem proxies de AOP, não respeita escopo. Você acha que está usando Spring, mas criou um objeto solto que o container nem enxerga. E volta o acoplamento de `JdbcCustomerRepository`.

**Fix:** declare a dependência e deixe o container injetá-la.

```java
@Service
public class OrderService {
    private final CustomerRepository repository;

    public OrderService(CustomerRepository repository) {
        this.repository = repository; // agora é o container quem fornece
    }
}
```

### (2) Field injection que esconde as dependências

```java
@Service
public class OrderService {
    @Autowired
    private CustomerRepository repository; // injeção em campo
}
```

**Por que dói:** parece conveniente, mas esconde a dependência. Não há como instanciar `OrderService` num teste passando um dublê — o campo só é preenchido pelo container, via reflexão. Some também o `final`, então a dependência deixa de ser imutável. E uma classe com cinco `@Autowired` em campos disfarça que ela tem dependências demais (provável violação de responsabilidade única).

**Fix:** prefira **constructor injection**. As dependências ficam explícitas na assinatura do construtor, podem ser `final`, e o teste injeta dubles sem container. O detalhe completo dos três tipos (construtor, setter, campo) e quando usar cada um está em [[03-Dominios/Tecnologia/Java/Spring Core e Boot/04 - Tipos de injeção — constructor, setter, field|Tipos de injeção]].

### (3) Achar que "Spring é CDI"

```text
"O Spring implementa a especificação CDI do Jakarta EE."  ← falso
```

**Por que dói:** num desafio técnico ou entrevista, afirmar isso revela um modelo mental errado. O Spring tem container próprio, anterior e independente do CDI; ele apenas *interopera* com as anotações `jakarta.inject` por compatibilidade.

**Fix:** a frase correta é "Spring e CDI resolvem o mesmo problema (IoC/DI) com mecanismos diferentes; o Spring tem seu próprio container, não é uma implementação de CDI". Veja [[03-Dominios/Tecnologia/Java/Jakarta EE/04 - CDI — beans e injeção|CDI — beans e injeção]] para a spec equivalente.

## Em entrevista

### Frase pronta (inglês)

> "Inversion of Control is the principle where the framework, not my code, controls how objects are created and wired together; Dependency Injection is the technique Spring uses to implement it — the container injects a class's collaborators instead of the class building them with `new`. The main trade-off is that you give up the explicitness of seeing object creation in your own code, but you gain decoupling and testability: I depend on interfaces, and the container decides the concrete implementation, so I can swap a real repository for a mock in tests without touching the service. One caveat I always mention is that Spring is *not* a CDI implementation — it has its own container and predates CDI; it merely supports the `jakarta.inject` annotations for interoperability."

### Vocabulário

| Termo PT | Termo EN |
| --- | --- |
| Inversão de controle | Inversion of Control (IoC) |
| Injeção de dependência | Dependency Injection (DI) |
| Container IoC | IoC container |
| Bean (objeto gerenciado) | (managed) bean |
| Wiring / ligação dos objetos | wiring |
| Injeção por construtor | constructor injection |
| Injeção em campo | field injection |
| Acoplamento / desacoplamento | coupling / decoupling |
| Metadados de configuração | configuration metadata |

## Veja também

- [[03-Dominios/Tecnologia/Java/Spring Core e Boot/03 - Beans e estereótipos — @Component, @Service, @Repository, @Controller|Beans e estereótipos]] — como declarar os objetos que o container vai gerenciar.
- [[03-Dominios/Tecnologia/Java/Spring Core e Boot/04 - Tipos de injeção — constructor, setter, field|Tipos de injeção]] — os três jeitos de injetar e por que construtor é o preferido (continua a armadilha 2).
- [[03-Dominios/Tecnologia/Java/Spring Core e Boot/06 - ApplicationContext — o container e seu ciclo|ApplicationContext — o container e seu ciclo]] — o container por dentro: criação, ciclo de vida, fechamento.
- [[03-Dominios/Tecnologia/Java/Jakarta EE/04 - CDI — beans e injeção|CDI — beans e injeção]] — a spec equivalente do Galho 7: **mesma ideia** (IoC/DI), mas com mecanismo **próprio do Spring**, não com CDI.
- [[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/11 - Annotations|Annotations]] — como o container lê `@Autowired` e companhia via reflexão (Galho 1).
- [[03-Dominios/Tecnologia/Java/Spring Core e Boot/index|Spring Core e Boot (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#IoC / inversão de controle (Spring)|IoC / inversão de controle (Spring)]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#@Autowired|@Autowired]]

## Referências

- Spring Framework Reference — *Introduction to the Spring IoC Container and Beans*: <https://docs.spring.io/spring-framework/reference/core/beans.html>
- Spring Framework Reference — *Container Overview*: <https://docs.spring.io/spring-framework/reference/core/beans/basics.html>
- Spring Framework Reference — *Dependency Injection*: <https://docs.spring.io/spring-framework/reference/core/beans/dependencies/factory-collaborators.html>
