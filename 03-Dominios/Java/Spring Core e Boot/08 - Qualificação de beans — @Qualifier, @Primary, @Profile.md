---
title: "Qualificação de beans — @Qualifier, @Primary, @Profile"
created_at: 2026-06-08
updated_at: 2026-06-08
type: concept
progress: backlog
status: seedling
publish: true
fase: adepto
tags:
  - java
  - spring
  - adepto
  - beans
aliases:
  - "@Qualifier"
  - "@Primary"
---

# Qualificação de beans — @Qualifier, @Primary, @Profile

> [!tip] TL;DR
> Quando o Spring encontra mais de um bean do mesmo tipo no contexto, ele lança `NoUniqueBeanDefinitionException`. `@Qualifier` aponta qual bean usar pelo nome ou por anotação customizada; `@Primary` elege um candidato padrão; `@Profile` registra o bean apenas quando um perfil de ambiente está ativo. Os três mecanismos colaboram: `@Profile` filtra *quais* beans existem, `@Primary` define o padrão entre os restantes, e `@Qualifier` escolhe um específico na injeção.

## O que é

**Qualificação de beans** é o conjunto de mecanismos que o Spring usa para resolver ambiguidade de tipo durante a injeção de dependências. Quando o contêiner precisa injetar uma interface e há dois ou mais beans que a implementam, ele precisa de uma dica extra. Essa dica pode vir de:

- `@Qualifier` — indicação direta no ponto de injeção ou no bean.
- `@Primary` — marcação no bean que deve ser preferido por padrão.
- `@Profile` — restrição que faz o bean existir apenas em certos ambientes.

Todos operam sobre o mesmo conceito central: o mapa de beans do `ApplicationContext`.

## Por que importa

Aplicações reais raramente têm uma única implementação por interface. É comum ter:

- uma implementação real e um stub para testes;
- duas implementações de `PaymentGateway` (ex.: Stripe e PayPal);
- um `DataSource` de desenvolvimento (H2 em memória) e outro de produção (PostgreSQL).

Sem qualificação, o Spring falha em tempo de startup com `NoUniqueBeanDefinitionException`. Entender esses três mecanismos é obrigatório para qualquer código Spring moderadamente complexo.

## Como funciona

### Ambiguidade de tipo (NoUniqueBeanDefinitionException)

O erro ocorre quando o `BeanFactory` encontra mais de um bean compatível com o tipo requerido e não tem como decidir qual usar:

```
org.springframework.beans.factory.NoUniqueBeanDefinitionException:
No qualifying bean of type 'com.example.PaymentGateway' available:
expected single matching bean but found 2: stripeGateway, paypalGateway
```

O Spring não escolhe aleatoriamente — ele falha explicitamente. A resolução passa por um dos mecanismos abaixo.

### @Qualifier (custom e por nome)

`@Qualifier` restringe a seleção de candidatos por tipo a um subconjunto identificado por um rótulo (string ou anotação customizada).

**Por nome de bean** — o valor do `@Qualifier` corresponde ao nome do bean (atributo `value` de `@Component` ou `@Bean`):

```java
@Component("stripeGateway")
public class StripeGateway implements PaymentGateway { ... }

@Component("paypalGateway")
public class PaypalGateway implements PaymentGateway { ... }

@Service
public class CheckoutService {

    private final PaymentGateway gateway;

    public CheckoutService(@Qualifier("stripeGateway") PaymentGateway gateway) {
        this.gateway = gateway;
    }
}
```

**Qualifier customizado** — cria uma anotação meta-anotada com `@Qualifier` para desacoplar o código do nome literal do bean:

```java
@Target({ElementType.FIELD, ElementType.PARAMETER})
@Retention(RetentionPolicy.RUNTIME)
@Qualifier
public @interface Stripe {}

// No bean:
@Component
@Stripe
public class StripeGateway implements PaymentGateway { ... }

// No ponto de injeção:
@Service
public class CheckoutService {
    public CheckoutService(@Stripe PaymentGateway gateway) { ... }
}
```

Qualifiers customizados são preferíveis em código de produção porque uma renomeação de bean não quebra os pontos de injeção.

### @Primary e @Profile como condicionais

**`@Primary`** elege um bean como candidato padrão quando nenhum `@Qualifier` está presente no ponto de injeção. É útil para cenários onde existe uma implementação "principal" e opções alternativas:

```java
@Component
@Primary
public class StripeGateway implements PaymentGateway { ... }

@Component
public class PaypalGateway implements PaymentGateway { ... }

@Service
public class CheckoutService {
    // Injeta StripeGateway sem necessidade de @Qualifier
    public CheckoutService(PaymentGateway gateway) { ... }
}
```

> [!warning] Dois `@Primary` causam o mesmo `NoUniqueBeanDefinitionException`
> Marcar dois beans com `@Primary` não resolve a ambiguidade — ela apenas se desloca para outro nível. O contêiner ainda não sabe qual dos dois primários preferir.

**`@Profile`** é um mecanismo condicional: o bean só é registrado no contexto se o perfil indicado estiver ativo. Ele não resolve ambiguidade diretamente — ele *evita* que a ambiguidade surja ao controlar quais beans existem em cada ambiente:

```java
@Configuration
public class DataSourceConfig {

    @Bean
    @Profile("development")
    public DataSource h2DataSource() {
        return new EmbeddedDatabaseBuilder()
                .setType(EmbeddedDatabaseType.H2)
                .build();
    }

    @Bean
    @Profile("production")
    public DataSource postgresDataSource() {
        // configura DataSource PostgreSQL
        return ...;
    }
}
```

O perfil ativo é definido via `spring.profiles.active` (propriedade, variável de ambiente ou argumento de linha de comando). Expressões booleanas são suportadas: `@Profile("production & us-east")`, `@Profile("!production")`.

### Injeção de coleções (List\<T\>, Map\<String,T\>) e @Order

Quando o ponto de injeção declara uma coleção do tipo `T`, o Spring injeta **todos** os beans daquele tipo registrados no contexto:

```java
@Service
public class NotificationService {

    private final List<NotificationChannel> channels;

    // Injeta todos os beans do tipo NotificationChannel
    public NotificationService(List<NotificationChannel> channels) {
        this.channels = channels;
    }
}
```

Para controlar a ordem dos elementos na lista, use `@Order` (ou implemente `Ordered`):

```java
@Component
@Order(1)
public class EmailChannel implements NotificationChannel { ... }

@Component
@Order(2)
public class SmsChannel implements NotificationChannel { ... }
```

Com `Map<String, T>`, o Spring usa o nome do bean como chave:

```java
// Resulta em: {"emailChannel" -> EmailChannel, "smsChannel" -> SmsChannel}
private final Map<String, NotificationChannel> channelsByName;
```

Esse padrão permite despachar para implementações pelo nome sem `if`/`switch`.

## Na prática

Dois beans implementam `PaymentGateway`; o serviço usa `@Primary` como padrão e `@Qualifier` para o caso alternativo:

```java
public interface PaymentGateway {
    void charge(String customerId, long amountCents);
}

@Component
@Primary                        // padrão quando não há @Qualifier
public class StripeGateway implements PaymentGateway {
    @Override
    public void charge(String customerId, long amountCents) {
        System.out.println("Stripe: charging " + customerId);
    }
}

@Component("paypal")            // nome explícito para @Qualifier
public class PaypalGateway implements PaymentGateway {
    @Override
    public void charge(String customerId, long amountCents) {
        System.out.println("PayPal: charging " + customerId);
    }
}

@Service
public class CheckoutService {

    private final PaymentGateway defaultGateway;  // injeta StripeGateway (@Primary)
    private final PaymentGateway paypal;           // injeta PaypalGateway (@Qualifier)

    public CheckoutService(
            PaymentGateway defaultGateway,
            @Qualifier("paypal") PaymentGateway paypal) {
        this.defaultGateway = defaultGateway;
        this.paypal = paypal;
    }
}
```

Em testes, basta criar um bean `@TestConfiguration` com `@Primary` para sobrescrever o padrão sem alterar código de produção.

## Armadilhas

- **Dois `@Primary` no mesmo tipo:** o contêiner não elege um dos dois — ele lança `NoUniqueBeanDefinitionException` igualmente. Use `@Primary` em no máximo um bean por tipo.
- **`@Qualifier` com nome errado:** o Spring lança `NoSuchBeanDefinitionException` em startup se o nome do qualifier não corresponder a nenhum bean registrado. Qualifiers customizados (anotações) evitam esse risco.
- **`List<T>` injeta todos os beans do tipo:** ao injetar uma coleção, o Spring não filtra por `@Qualifier` — ele coleta todos os candidatos compatíveis. Se apenas um subconjunto for desejado, use qualifiers customizados nas implementações e no ponto de injeção.
- **`@Profile` sem perfil ativo levanta `NoSuchBeanDefinitionException`:** se todos os beans de um tipo estiverem sob `@Profile` e nenhum perfil correspondente estiver ativo, a injeção falha. Sempre forneça um bean default (`@Profile("default")`) ou garanta que pelo menos um perfil esteja ativo.

## Em entrevista

### Frase pronta (inglês)

- *"When multiple beans of the same type exist in the context, Spring throws `NoUniqueBeanDefinitionException`. `@Qualifier` resolves the ambiguity at the injection point by matching a bean name or a custom qualifier annotation. `@Primary` marks the default candidate so you don't need a qualifier everywhere."*
- *"`@Profile` is a conditional mechanism — it controls whether a bean is registered at all based on the active environment profile, so it prevents ambiguity rather than resolving it."*
- *"Injecting `List<T>` collects all beans of that type in one shot; combine it with `@Order` to control the iteration order, and use a `Map<String, T>` when you need to dispatch by bean name at runtime."*

### Vocabulário

| Termo PT | Termo EN |
|---|---|
| Ambiguidade de tipo | Type ambiguity |
| Qualificação de bean | Bean qualification |
| Candidato primário | Primary candidate |
| Perfil de ambiente | Environment profile |
| Ponto de injeção | Injection point |
| Qualifier customizado | Custom qualifier annotation |
| Injeção de coleção | Collection injection |
| Ativação de perfil | Profile activation |

## Veja também

- [[03-Dominios/Java/Spring Core e Boot/03 - Beans e estereótipos — @Component, @Service, @Repository, @Controller|Beans e estereótipos]] — como os beans são declarados e nomeados
- [[03-Dominios/Java/Spring Core e Boot/12 - Configuração e profiles|Configuração e profiles]] — `@Profile` em detalhe, `application.properties` por ambiente
- [[03-Dominios/Java/Jakarta EE/06 - CDI — qualifiers, producers e eventos|CDI — qualifiers, producers e eventos]] — qualifiers na spec Jakarta (para comparação, sem re-explicar aqui)
- [[03-Dominios/Java/Spring Core e Boot/index|Spring Core e Boot (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Dicionário de Java#@Qualifier (Spring)|@Qualifier (Spring)]] — verbete no dicionário
- [[03-Dominios/Java/Dicionário de Java#@Primary|@Primary]] — verbete no dicionário

## Referências

- [Fine-tuning Annotation-based Autowiring with Qualifiers — Spring Framework Docs](https://docs.spring.io/spring-framework/reference/core/beans/annotation-config/autowired-qualifiers.html)
- [Environment Abstraction — Spring Framework Docs](https://docs.spring.io/spring-framework/reference/core/beans/environment.html)
- [Core Annotations — Spring Boot Reference](https://docs.spring.io/spring-boot/docs/current/reference/html/application-properties.html)
