---
title: "Tipos de injeção — constructor, setter, field"
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
  - di
aliases:
  - "constructor injection"
  - "field injection"
---

# Tipos de injeção — constructor, setter, field

> [!abstract] TL;DR
> Existem três formas de o Spring injetar dependências em um bean: **constructor injection** (via construtor), **setter injection** (via método setter) e **field injection** (via `@Autowired` direto no campo). A recomendação oficial do Spring é **sempre preferir constructor injection**: ela torna os campos `final`, garante que o objeto nasce 100% inicializado, elimina a possibilidade de dependência nula e facilita testes sem container. Setter injection fica para dependências **opcionais**. Field injection deve ser evitada — ela esconde dependências, impede o uso de `final` e dificulta o teste unitário. Desde o Spring Boot 2.6, dependências circulares são **proibidas por padrão**; a flag `spring.main.allow-circular-references=true` restaura o comportamento antigo, mas o correto é repensar o design.

## O que é

Quando o container Spring cria um bean, ele precisa fornecer (injetar) as dependências que esse bean declara. Há três mecanismos disponíveis:

| Mecanismo | Como funciona |
|---|---|
| **Constructor injection** | O container chama o construtor passando cada dependência como argumento |
| **Setter injection** | O container instancia o bean com o construtor padrão e depois chama métodos setter |
| **Field injection** | O container usa reflexão para preencher diretamente o campo anotado com `@Autowired` |

A escolha entre eles não é só estilo: ela afeta imutabilidade, testabilidade, detecção de erros e a própria legibilidade do código.

## Por que importa

Em entrevistas para vagas sênior, a pergunta "qual tipo de injeção você prefere e por quê?" é clássica. A resposta esperada não é "tanto faz" — é uma justificativa técnica sobre imutabilidade, fail-fast e testabilidade.

Além disso, entender os trade-offs ajuda a identificar problemas reais em código legado:
- Campos `@Autowired` sem construtor indicam que a classe não pode ser testada de forma isolada.
- Ciclos de dependência mascarados por setter injection são bugs latentes que viram exceções em produção.

## Como funciona

### Constructor injection (recomendado e por quê)

O container invoca o construtor do bean e fornece cada dependência como argumento. Desde o Spring 4.3, se a classe tem **um único construtor**, a anotação `@Autowired` é dispensável — o Spring a infere automaticamente.

```java
@Service
public class OrderService {

    private final CustomerRepository customerRepository;

    // @Autowired é opcional quando há um único construtor (Spring 4.3+)
    public OrderService(CustomerRepository customerRepository) {
        this.customerRepository = customerRepository;
    }
}
```

Vantagens que justificam a recomendação oficial do Spring:

- **Imutabilidade real**: o campo pode ser `final`, impossibilitando reassignment acidental.
- **Fail-fast**: o container falha na inicialização se a dependência não existir — o erro aparece no boot, não em runtime.
- **Objeto sempre válido**: o bean retorna ao chamador em estado completamente inicializado.
- **Testável sem container**: basta `new OrderService(mockRepository)` no teste unitário.
- **Design feedback**: um construtor com 7+ parâmetros é um sinal claro de que a classe tem responsabilidades demais (SRP violado).

### Setter injection (dependências opcionais)

O container instancia o bean via construtor sem argumentos e, em seguida, chama os setters anotados com `@Autowired`. O campo **não** pode ser `final`.

```java
@Service
public class OrderService {

    private CustomerRepository customerRepository;

    @Autowired
    public void setCustomerRepository(CustomerRepository customerRepository) {
        this.customerRepository = customerRepository;
    }
}
```

Quando faz sentido:
- Dependências genuinamente **opcionais** (o bean funciona mesmo sem elas, com um comportamento degradado).
- Casos em que a dependência precisa ser **reinjetada** após a criação (raro, mas existe em cenários de JMX ou testes de integração específicos).

O time Spring recomenda explicitamente: **não use setter injection para dependências obrigatórias**.

### Field injection (`@Autowired` em campo — por que evitar)

O container usa reflexão para preencher o campo diretamente, sem construtor nem setter público.

```java
@Service
public class OrderService {

    @Autowired  // evitar
    private CustomerRepository customerRepository;
}
```

Por que evitar:

1. **Impede `final`**: o campo não pode ser imutável.
2. **Esconde dependências**: a classe não declara o que precisa em nenhuma interface pública — a dependência só é visível se o código-fonte for lido linha a linha.
3. **Dificulta testes**: não há como injetar um mock sem um framework de reflexão (Mockito com `@InjectMocks`) ou o próprio container Spring — testes ficam pesados.
4. **Viola encapsulamento**: o container precisa acessar um campo privado por reflexão.

IDEs como IntelliJ IDEA exibem aviso para field injection por esses motivos.

### Dependências circulares proibidas por default no Boot 2.6+

Uma **dependência circular** ocorre quando o bean A depende do bean B, que depende do bean A (diretamente ou em cadeia). Com constructor injection, isso é detectado e rejeitado pelo container.

Até o Spring Boot 2.5, o container tentava resolver ciclos silenciosamente usando setter ou field injection como válvula de escape — um bean era injetado **antes de estar totalmente inicializado**, o que criava estados inconsistentes difíceis de rastrear.

Desde o **Spring Boot 2.6**, dependências circulares são **proibidas por padrão**. Ao detectar um ciclo, o boot falha com `BeanCurrentlyInCreationException` e uma mensagem descritiva indicando a cadeia.

Para restaurar o comportamento antigo (não recomendado):

```properties
# application.properties
spring.main.allow-circular-references=true
```

A forma correta de resolver é refatorar: extrair a responsabilidade compartilhada para um terceiro bean, ou reorganizar as dependências para quebrar o ciclo.

## Na prática

As três formas lado a lado, usando o mesmo cenário (`OrderService` dependendo de `CustomerRepository`):

```java
// ──────────────────────────────────────────────
// 1. Constructor injection (RECOMENDADO)
// ──────────────────────────────────────────────
@Service
public class OrderService {

    private final CustomerRepository customerRepository;

    public OrderService(CustomerRepository customerRepository) {
        this.customerRepository = customerRepository;  // final, não-nulo, fail-fast
    }

    public Order placeOrder(Long customerId, Long productId) {
        Customer customer = customerRepository.findById(customerId)
                .orElseThrow(() -> new IllegalArgumentException("Cliente não encontrado"));
        // lógica de pedido...
        return new Order(customer, productId);
    }
}

// ──────────────────────────────────────────────
// 2. Setter injection (para dependência opcional)
// ──────────────────────────────────────────────
@Service
public class OrderService {

    private CustomerRepository customerRepository;

    @Autowired
    public void setCustomerRepository(CustomerRepository customerRepository) {
        this.customerRepository = customerRepository;  // mutável; pode ser nulo
    }
}

// ──────────────────────────────────────────────
// 3. Field injection (EVITAR)
// ──────────────────────────────────────────────
@Service
public class OrderService {

    @Autowired
    private CustomerRepository customerRepository;  // reflexão; sem final; sem visibilidade pública
}
```

Teste unitário comparando constructor vs. field injection:

```java
// Com constructor injection — sem container, sem reflexão
@Test
void placeOrder_deveRetornarPedido() {
    CustomerRepository mockRepo = Mockito.mock(CustomerRepository.class);
    OrderService service = new OrderService(mockRepo);  // simples
    // ...
}

// Com field injection — precisa de @ExtendWith(MockitoExtension.class) e @InjectMocks
@ExtendWith(MockitoExtension.class)
class OrderServiceTest {

    @Mock
    private CustomerRepository customerRepository;

    @InjectMocks
    private OrderService orderService;  // Mockito usa reflexão para preencher o campo
}
```

## Armadilhas

### (1) Field injection em código que precisa de teste unitário

**Problema**: `@Autowired` direto no campo torna a dependência invisível para quem instancia a classe fora do container. Em testes unitários puros, `new OrderService()` cria um objeto com `customerRepository == null`, lançando `NullPointerException` no primeiro uso.

```java
// Campo @Autowired — armadilha clássica
@Service
public class OrderService {
    @Autowired
    private CustomerRepository customerRepository;
}

// Teste que explode em NullPointerException
@Test
void teste_quebrado() {
    OrderService service = new OrderService();
    service.placeOrder(1L, 2L);  // NullPointerException aqui
}
```

**Fix**: migrar para constructor injection. O campo fica `final`, o construtor deixa explícita a dependência, e o teste passa a ser `new OrderService(mock)`.

### (2) `@Autowired` redundante em construtor único (desnecessário desde Spring 4.3)

**Problema**: muitos projetos legados (ou exemplos de blog antigos) ainda anotam o construtor com `@Autowired` quando ele é o único. A partir do Spring 4.3, isso é desnecessário e polui o código.

```java
// Redundante — Spring 4.3+ infere @Autowired em construtor único
@Service
public class OrderService {

    private final CustomerRepository customerRepository;

    @Autowired  // <— desnecessário
    public OrderService(CustomerRepository customerRepository) {
        this.customerRepository = customerRepository;
    }
}
```

**Fix**: remover o `@Autowired`. O comportamento é idêntico, o código fica mais limpo.

### (3) Ciclo de dependência mascarado por setter injection

**Problema**: antes do Spring Boot 2.6, dependências circulares entre beans eram "resolvidas" silenciosamente quando o ciclo envolvia setter ou field injection. Um bean era injetado no outro **antes de ter seus próprios setters chamados**, criando estados inconsistentes que só se manifestavam em runtime, longe do ponto de criação.

```java
// Ciclo mascarado (comportamento pré-Boot 2.6)
@Service
public class OrderService {
    @Autowired
    private InvoiceService invoiceService;  // InvoiceService depende de OrderService
}

@Service
public class InvoiceService {
    @Autowired
    private OrderService orderService;  // ciclo — antes do Boot 2.6, "funcionava"
}
```

**Fix**: desde o Boot 2.6, o container rejeita o ciclo com `BeanCurrentlyInCreationException`. A solução correta é extrair a responsabilidade compartilhada para um terceiro serviço (ex.: `OrderInvoiceCoordinator`) ou reorganizar as dependências para eliminar o ciclo.

## Em entrevista

### Frase pronta (inglês)

"I always favor constructor injection for mandatory dependencies because it makes fields `final`, guarantees the object is fully initialized when returned from the constructor, and surfaces missing dependencies at startup rather than at runtime. Setter injection is appropriate for optional dependencies where the bean has a sensible default behavior without them. I avoid field injection entirely: it hides the dependency contract, prevents immutability, and forces tests to rely on reflection frameworks or a Spring context instead of a simple `new`. Since Spring Boot 2.6, circular references are rejected by default, which is a great guardrail — if you hit a `BeanCurrentlyInCreationException`, the right fix is to refactor the design, not to flip `spring.main.allow-circular-references=true`."

### Vocabulário

| Termo | Definição rápida |
|---|---|
| **constructor injection** | Dependências fornecidas como argumentos do construtor; permite `final` e fail-fast |
| **setter injection** | Dependências fornecidas via métodos setter após instanciação; para dependências opcionais |
| **field injection** | Dependências preenchidas por reflexão direto no campo; evitar em produção |
| **`@Autowired`** | Anotação Spring que marca onde o container deve injetar uma dependência |
| **circular dependency** | Ciclo onde bean A depende de B e B depende de A; proibido por padrão no Boot 2.6+ |
| **`BeanCurrentlyInCreationException`** | Exceção lançada pelo container ao detectar dependência circular irresolvível |
| **fail-fast** | Comportamento de falhar imediatamente na inicialização em vez de mais tarde em runtime |
| **immutability** | Propriedade de um objeto cujo estado não pode mudar após construção; `final` fields |

## Veja também

- [[03-Dominios/Java/Spring Core e Boot/02 - IoC e injeção de dependência no Spring|IoC e injeção de dependência no Spring]]
- [[03-Dominios/Java/Spring Core e Boot/03 - Beans e estereótipos — @Component, @Service, @Repository, @Controller|Beans e estereótipos]]
- [[03-Dominios/Java/Jakarta EE/04 - CDI — beans e injeção|CDI — beans e injeção]] (`@Inject` em campo/construtor/método na spec)
- [[03-Dominios/Java/Spring Core e Boot/index|Spring Core e Boot (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Dicionário de Java#constructor injection|constructor injection]]

## Referências

- Spring Framework Reference — Dependency Injection: <https://docs.spring.io/spring-framework/reference/core/beans/dependencies/factory-collaborators.html>
- Spring Boot 2.6 Release Notes — Circular References Prohibited by Default: <https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-2.6-Release-Notes>
