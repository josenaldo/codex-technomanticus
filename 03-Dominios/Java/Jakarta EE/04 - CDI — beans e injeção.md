---
title: "CDI — beans e injeção"
created: 2026-06-07
updated: 2026-06-07
type: concept
progress: backlog
status: seedling
publish: true
fase: iniciado
tags:
  - java
  - jakarta-ee
  - iniciado
  - cdi
aliases:
  - "CDI"
  - "Injeção de dependência Jakarta"
  - "@Inject"
---

# CDI — beans e injeção

> [!abstract] TL;DR
> CDI é a especificação de **Contexts and Dependency Injection** da plataforma Jakarta EE: o container constrói o grafo de objetos por você, gerencia o ciclo de vida de cada instância e resolve automaticamente quem depende de quem. **É isso que o `@Autowired` esconde** — o Spring (Galho 8, planejado) implementa um container próprio inspirado nesse modelo; entender CDI torna o Spring transparente, não o contrário.

## O que é

**CDI 4.1** (parte do **Jakarta EE 11**) define a especificação de _Contexts and Dependency Injection_ para a plataforma Java. A sigla resume dois conceitos intimamente ligados:

- **Dependency Injection (DI):** o container instancia os objetos e injeta as dependências — você declara _o que_ precisa, não _como_ obter.
- **Contexts:** cada bean existe dentro de um contexto com um escopo definido (`@ApplicationScoped`, `@RequestScoped`, `@Dependent`, etc.) que determina por quanto tempo a instância vive e com quem ela é compartilhada. Escopos são o tema da nota seguinte.

A combinação das duas ideias é o que se chama de **Inversão de Controle (IoC):** o controle sobre a criação e o ciclo de vida dos objetos sai do código de negócio e passa para o container.

> [!info] Versão cravada
> CDI 4.1 integra o Jakarta EE 11. A implementação de referência é o **Weld** (Red Hat/JBoss); a spec CDI em si é mantida pela Eclipse Foundation.

## Por que importa

CDI é o coração da plataforma Jakarta EE moderna. Quase toda especificação do ecossistema — Jakarta Persistence (JPA), Jakarta Transactions (JTA), Jakarta REST, Jakarta Faces — integra com o modelo de beans e injeção do CDI. Sem entender DI, cada especificação parece ter sua própria magia; com CDI, o modelo mental se unifica.

Para entrevistas técnicas de nível sênior, a pergunta clássica é: **"Como o container sabe o que injetar?"** A resposta passa por managed beans, typesafe resolution e bean discovery — exatamente o conteúdo desta nota.

Para o código do dia a dia, DI reduz acoplamento: em vez de `new OrderService(new OrderRepository())`, você declara a dependência e o container a satisfaz — incluindo escopo, interceptors e eventos, que seriam impossíveis com `new` manual.

## Como funciona

### O que é um bean (managed bean)

O CDI chama de **managed bean** qualquer classe Java que o container descobre, instancia e gerencia. Para uma classe ser elegível como managed bean ela deve atender a todos os critérios abaixo (conforme a spec CDI 4.1):

- Não é uma inner class não-estática (nested static é elegível).
- Não é abstrata.
- Não implementa `jakarta.enterprise.inject.spi.Extension` nem `BuildCompatibleExtension`.
- Não está anotada com `@Vetoed` (nem pertence a um pacote `@Vetoed`).
- Tem um **construtor sem argumentos** _ou_ um construtor anotado com `@Inject`.

Quando todos esses critérios são atendidos e o bean é descoberto pelo container (ver _Bean discovery_ abaixo), o container passa a ser o dono: ele instancia, injeta as dependências e destrói a instância quando o escopo expira.

> [!warning] Campos públicos não-estáticos
> Beans em **escopos normais** (`@ApplicationScoped`, `@RequestScoped`, etc.) não podem ter campos públicos não-estáticos. O container usa proxies para gerenciar esses escopos e campos públicos quebram a transparência do proxy. Use `@Dependent` se precisar de campos públicos — mas prefira encapsulamento.

### `@Inject` (campo vs. construtor vs. método)

A anotação `@Inject` (pacote `jakarta.inject`) marca um **ponto de injeção**: o container lê o tipo declarado e resolve qual bean entregar.

**Por campo:**

```java
@ApplicationScoped
public class OrderService {

    @Inject
    private OrderRepository repository; // o container injeta após instanciar
}
```

Funciona, mas dificulta testes: para trocar `repository` por um mock você precisa de reflection (ou um framework como Mockito com `@InjectMocks`). Evite em código novo.

**Por construtor (preferido):**

```java
@ApplicationScoped
public class OrderService {

    private final OrderRepository repository;

    @Inject
    public OrderService(OrderRepository repository) {
        this.repository = repository;
    }
}
```

Por que preferir? Duas razões concretas:

1. **Testabilidade:** no teste unitário, basta chamar `new OrderService(mockRepository)` — sem reflection, sem framework de mock.
2. **Imutabilidade:** o campo pode ser `final`, garantindo que a dependência não muda depois da construção.

**Por método inicializador:**

```java
@ApplicationScoped
public class OrderService {

    private OrderRepository repository;

    @Inject
    public void setRepository(OrderRepository repository) {
        this.repository = repository; // chamado pelo container após instanciar
    }
}
```

O container chama o método após instanciar o bean. Útil quando a lógica de inicialização precisa de múltiplas dependências resolvidas em conjunto, mas o construtor por injeção cobre a maioria dos casos.

### Bean discovery (`annotated` vs. `all`)

O container precisa saber _quais_ classes do classpath devem ser gerenciadas como beans. Esse processo é o **bean discovery** e é controlado pelo arquivo `beans.xml` e pelo atributo `bean-discovery-mode`.

| Modo | O que é descoberto | Quando usar |
|---|---|---|
| `annotated` (**padrão no CDI 4.x**) | Apenas classes com _bean defining annotations_ (`@ApplicationScoped`, `@RequestScoped`, `@Dependent`, estereótipos, etc.) | Aplicações novas — escopo explícito, sem surpresas |
| `all` | Toda classe do archive é candidata a bean | Migração de código legado sem anotações de escopo |

**Como configurar via `beans.xml`:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="https://jakarta.ee/xml/ns/jakartaee"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="https://jakarta.ee/xml/ns/jakartaee
           https://jakarta.ee/xml/ns/jakartaee/beans_4_0.xsd"
       version="4.0"
       bean-discovery-mode="all">
</beans>
```

**Comportamento resumido:**

- **Sem `beans.xml`:** modo `annotated` — só classes com _bean defining annotations_ são descobertas.
- **`beans.xml` vazio:** mesmo comportamento do modo `annotated` (padrão CDI 4.x).
- **`bean-discovery-mode="all"`:** todas as classes elegíveis no archive são beans, mesmo sem anotação de escopo.

> [!tip] Regra prática
> Em projetos novos com CDI 4.1, anote cada bean com o escopo correto (`@ApplicationScoped`, `@RequestScoped`, etc.) e deixe o modo padrão `annotated`. O modo `all` é uma saída de emergência para código legado.

### Resolução typesafe

Quando o container encontra um ponto de injeção, ele resolve qual bean entregar usando **resolução typesafe**: o tipo Java declarado no ponto de injeção é a chave principal de busca.

O processo, simplificado:

1. O container coleta todos os beans cujo _bean type_ é compatível com o tipo do ponto de injeção.
2. Filtra pelos qualifiers — por padrão, todo ponto de injeção sem qualifier explícito recebe `@Default`, e todo bean sem qualifier explícito também recebe `@Default`.
3. Se sobrar **exatamente um** bean: injeção bem-sucedida.
4. Se sobrar **zero**: `UnsatisfiedResolutionException` em tempo de deploy.
5. Se sobrar **mais de um**: `AmbiguousResolutionException` em tempo de deploy.

O caso de ambiguidade (item 5) acontece quando há duas implementações do mesmo tipo sem distinção — a solução são os **qualifiers**, tema da [[06 - CDI — qualifiers, producers e eventos]].

### Annotations por baixo

CDI usa o sistema de annotations do Java para declarar tudo: escopos, qualifiers, interceptors, producers. A resolução typesafe ocorre **em tempo de deploy**, via reflection sobre os metadados das annotations — que precisam de retention `RUNTIME` para estarem disponíveis nessa fase.

Se você ainda não conhece bem annotations e retention policies, leia primeiro: [[03-Dominios/Java/Linguagem e sintaxe moderna/11 - Annotations|Annotations (Galho 1)]]. CDI é um uso intenso de annotations RUNTIME + reflection; entender a mecânica base evita confusão.

## Na prática

Cenário: uma aplicação de pedidos com `OrderRepository` (interface) e sua implementação, e um `OrderService` que depende do repositório.

```java
// Contrato — interface pura, sem anotação CDI necessária aqui
public interface OrderRepository {
    void save(Order order);
    Order findById(long id);
}
```

```java
import jakarta.enterprise.context.ApplicationScoped;

// Implementação: @ApplicationScoped torna a classe um bean gerenciado
// Uma única instância por contexto de aplicação (singleton lógico)
@ApplicationScoped
public class JpaOrderRepository implements OrderRepository {

    @Override
    public void save(Order order) {
        // lógica JPA aqui
    }

    @Override
    public Order findById(long id) {
        // lógica JPA aqui
        return null;
    }
}
```

```java
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;

@ApplicationScoped
public class OrderService {

    private final OrderRepository repository;

    @Inject // construtor: testável e imutável
    public OrderService(OrderRepository repository) {
        this.repository = repository;
    }

    public void place(Order order) {
        repository.save(order);
    }
}
```

O container descobre `JpaOrderRepository` (tem `@ApplicationScoped` → bean defining annotation → descoberta em modo `annotated`). Quando resolve o `OrderService`, vê que o construtor requer `OrderRepository`, encontra `JpaOrderRepository` como única implementação compatível e injeta.

**Bootstrapping com Weld (impl de referência):**

Em ambientes Jakarta EE completos (WildFly, Payara, GlassFish), o bootstrap é automático. Para testes ou aplicações SE, pode-se usar o **Weld** diretamente:

```java
import org.jboss.weld.environment.se.Weld;
import org.jboss.weld.environment.se.WeldContainer;

public class Main {
    public static void main(String[] args) {
        try (WeldContainer container = new Weld().initialize()) {
            OrderService service = container.select(OrderService.class).get();
            service.place(new Order());
        } // container fechado: beans destruídos
    }
}
```

> [!info] Weld é a implementação de referência
> Weld (Red Hat/JBoss) é o projeto de referência (RI) do CDI. Em servidores de aplicação Jakarta EE certificados, outra implementação CDI pode ser usada internamente — mas Weld é o padrão de facto e o que você vai encontrar no WildFly/JBoss.

**Contraexemplo — o que acontece com `new`:**

```java
// NÃO faça isso dentro de código gerenciado pelo container:
OrderRepository repo = new JpaOrderRepository();
OrderService service = new OrderService(repo); // funciona, mas...
```

O objeto criado com `new` existe **fora do container**: sem escopo (ciclo de vida não gerenciado), sem interceptors (sem logging, transações, segurança automáticos) e sem eventos CDI. Você abre mão de toda a infraestrutura da plataforma. Veja os teasers em [[05 - CDI — escopos e contextos]] e [[13 - CDI avançado — interceptors, decorators e extensões]].

## Armadilhas

### (1) Injeção por campo dificulta testes

**Problema:** campo `@Inject private OrderRepository repo` é privado. O teste unitário não consegue substituir por um mock sem usar reflection — acoplamento invisível entre o código e o framework de teste.

```java
// Problemático: sem framework de mock, impossível trocar no teste
@ApplicationScoped
public class OrderService {
    @Inject
    private OrderRepository repository; // privado — inacessível no teste
}
```

**Fix:** use injeção por construtor. No teste, `new OrderService(fakeRepository)` e pronto.

```java
@ApplicationScoped
public class OrderService {
    private final OrderRepository repository;

    @Inject
    public OrderService(OrderRepository repository) {
        this.repository = repository;
    }
}

// No teste:
OrderService svc = new OrderService(new FakeOrderRepository());
```

### (2) Duas implementações do mesmo tipo causam `AmbiguousResolutionException`

**Problema:** o container encontra `JpaOrderRepository` e `InMemoryOrderRepository`, ambas implementando `OrderRepository`, sem distinção. A resolução typesafe falha em tempo de deploy.

```java
@ApplicationScoped
public class JpaOrderRepository implements OrderRepository { ... }

@ApplicationScoped
public class InMemoryOrderRepository implements OrderRepository { ... }

// Ponto de injeção:
@Inject
OrderRepository repo; // → AmbiguousResolutionException: qual das duas?
```

**Fix:** use qualifiers para distinguir as implementações — tema detalhado em [[06 - CDI — qualifiers, producers e eventos]]. O teaser: você cria uma annotation `@Jpa` e outra `@InMemory` e anota cada impl e cada ponto de injeção correspondente.

### (3) `new` em classe gerenciada pelo container

**Problema:** instanciar manualmente uma classe que o container poderia gerenciar significa perder escopo, interceptors (transações, segurança, logging) e a capacidade de participar de eventos CDI.

```java
// Dentro de um bean gerenciado:
OrderService svc = new OrderService(new JpaOrderRepository());
svc.place(order); // funciona, mas: sem transação automática, sem auditoria, sem escopo
```

**Fix:** deixe o container instanciar. Injete `OrderService` via `@Inject` no ponto de uso. Se precisar criar dinamicamente (ex.: objetos com parâmetros de runtime), use `jakarta.enterprise.inject.Instance<T>` ou um Producer — temas da nota 06.

## Em entrevista

### Frase pronta (inglês)

"CDI is the dependency injection and context management specification in the Jakarta EE platform. The container owns the lifecycle of managed beans — you declare what you need at injection points and the container performs typesafe resolution at deploy time to wire the object graph. Using constructor injection is the recommended pattern because it keeps beans testable without any reflection tricks and allows fields to be declared final, improving immutability guarantees."

### Vocabulário

| Termo PT | Termo EN |
|---|---|
| Injeção de dependência | Dependency Injection (DI) |
| Inversão de controle | Inversion of Control (IoC) |
| Bean gerenciado | Managed bean |
| Ponto de injeção | Injection point |
| Descoberta de beans | Bean discovery |
| Resolução typesafe | Typesafe resolution |
| Qualificador | Qualifier |
| Escopo | Scope / Context |
| Implementação de referência | Reference Implementation (RI) |

## Veja também

- [[01 - O modelo Jakarta EE — especificações e implementações]]
- [[05 - CDI — escopos e contextos]]
- [[06 - CDI — qualifiers, producers e eventos]]
- [[13 - CDI avançado — interceptors, decorators e extensões]]
- [[03-Dominios/Java/Linguagem e sintaxe moderna/11 - Annotations|Annotations (Galho 1)]]
- [[03-Dominios/Java/Jakarta EE/index|Jakarta EE (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Dicionário de Java#CDI (Contexts and Dependency Injection)|CDI (Dicionário)]]
- [[03-Dominios/Java/Dicionário de Java#bean (CDI)|bean (Dicionário)]]
- [[03-Dominios/Java/Dicionário de Java#@Inject|@Inject (Dicionário)]]
- [[03-Dominios/Java/Dicionário de Java#bean discovery / beans.xml|bean discovery (Dicionário)]]

## Referências

- Jakarta CDI 4.1 Specification: <https://jakarta.ee/specifications/cdi/4.1/jakarta-cdi-spec-4.1> (acesso: 2026-06-07)
- Jakarta CDI 4.1 — página da especificação: <https://jakarta.ee/specifications/cdi/4.1/> (acesso: 2026-06-07)
- Weld — implementação de referência do CDI: <https://weld.cdi-spec.org/> (acesso: 2026-06-07)
