---
title: Spring Cloud Stream — a abstração de binders
aliases:
  - Spring Cloud Stream
tags:
  - java
  - mensageria
  - adepto
  - spring-kafka
fase: Adepto
type: concept
status: seedling
publish: true
created: 2026-06-11
updated: 2026-06-11
---

# Spring Cloud Stream — a abstração de binders

> [!abstract] TL;DR
> Spring Cloud Stream coloca uma camada de abstração entre seu código e o broker de mensagens. Você escreve `Supplier`, `Function` e `Consumer` como beans Java padrão; o framework conecta esses beans ao Kafka ou RabbitMQ via **binders**. A indireção vale quando a troca de broker é um requisito real — e atrapalha quando não é.

---

## O que é

Spring Cloud Stream (SCSt) é um projeto do ecossistema Spring que padroniza a forma de produzir e consumir mensagens em diferentes brokers (Kafka, RabbitMQ, Pulsar e outros).

A ideia central: em vez de usar a API específica do broker, você programa contra contratos de alto nível — **bindings** — e o SCSt cuida de traduzir esses contratos para o broker configurado via **binder**.

> [!info] Versão de referência
> Estas notas cobrem Spring Cloud Stream 4.x e 5.x (Spring Boot 3.x). A API de anotações legacy foi **removida** na versão 4.0.

---

## Por que importa

- **Portabilidade declarativa**: trocar Kafka por RabbitMQ em teoria exige apenas alterar dependências e configuração, sem tocar no código de negócio.
- **Modelo uniforme**: Kafka, RabbitMQ e Pulsar recebem o mesmo modelo funcional — reduz a curva de aprendizado quando a stack muda.
- **Integração com Spring**: funciona com Spring Boot autoconfig, Spring Integration e Spring Cloud Function.
- **Relevante em entrevistas**: aparece em perguntas sobre arquitetura de microsserviços orientados a eventos e sobre como o Spring abstrai brokers.

---

## Como funciona

### O modelo funcional — `Supplier`, `Function`, `Consumer`

A partir do Spring Cloud Stream 3.x, o modelo recomendado é puramente funcional: você expõe beans de `java.util.function.Supplier`, `Function` ou `Consumer` e o framework os conecta automaticamente a bindings.

```java
@Bean
public Supplier<Order> novasOrdens() {
    return () -> orderRepository.findNextPending();
}

@Bean
public Function<Order, Shipment> processarOrdem() {
    return order -> shippingService.createShipment(order);
}

@Bean
public Consumer<Shipment> registrarEnvio() {
    return shipment -> auditLog.record(shipment);
}
```

> [!warning] `@StreamListener` foi REMOVIDO
> As anotações `@StreamListener`, `@EnableBinding`, `@Input` e `@Output` foram **depreciadas** no Spring Cloud Stream 3.x e **removidas** na versão 4.0. Código com essas anotações não compila com SCSt 4.x+. Use exclusivamente o modelo funcional.

O Spring Cloud Function (integrado ao SCSt) descobre automaticamente beans únicos desses tipos. Para múltiplos beans ou quando o nome é ambíguo, use a propriedade:

```properties
spring.cloud.function.definition=processarOrdem
```

Composição de funções com `|` (pipe):

```properties
spring.cloud.function.definition=validarOrdem|processarOrdem
```

---

### Binders e bindings

O **binder** é o componente que sabe falar com o broker. Você declara a dependência do binder no `pom.xml` e o SCSt usa autoconfiguração para ativá-lo:

```xml
<!-- Kafka -->
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-stream-binder-kafka</artifactId>
</dependency>

<!-- RabbitMQ -->
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-stream-binder-rabbit</artifactId>
</dependency>
```

O **binding** é a ponte entre o bean funcional e o tópico/fila. O nome segue a convenção:

```
<nomeDaFunção>-in-<índice>   → binding de entrada (Consumer ou Function)
<nomeDaFunção>-out-<índice>  → binding de saída (Supplier ou Function)
```

Configuração dos bindings:

```yaml
spring:
  cloud:
    stream:
      bindings:
        processarOrdem-in-0:
          destination: ordens              # tópico Kafka ou exchange RabbitMQ
          group: processamento-envio       # consumer group
        processarOrdem-out-0:
          destination: envios
```

A propriedade `destination` mapeia para o **tópico** no Kafka e para o **exchange** no RabbitMQ. A propriedade `group` define o consumer group — sem ela, cada instância recebe todas as mensagens (semântica de broadcast).

---

### Quando a indireção vale e quando atrapalha

**Vale a pena quando:**

- A portabilidade de broker é um requisito explícito do negócio (ex.: produto SaaS que suporta Kafka e RabbitMQ).
- A equipe já usa Spring Cloud e quer uniformidade de modelo entre serviços.
- Você precisa de composição declarativa de pipelines de transformação.

**Atrapalha quando:**

- O broker nunca vai mudar — a camada extra dificulta o debugging (você depura binding, binder e broker ao mesmo tempo).
- Você precisa de recursos avançados do Kafka (transações exatas, consumer group rebalancing fine-grained, offsets manuais complexos) — o SCSt expõe parte dessas features, mas com mais fricção que o `@KafkaListener` direto.
- A equipe não conhece o modelo funcional do SCSt — a curva de aprendizado pode custar mais do que a abstração economiza.

> [!quote] Leaky abstraction
> As semânticas de Kafka (partições, offsets, rebalanceamento) e RabbitMQ (exchanges, routing keys, acks) são fundamentalmente diferentes. O SCSt unifica a configuração, mas não elimina as diferenças semânticas — você ainda precisa entender o broker subjacente para operar em produção.

---

## Na prática

Cenário: serviço que recebe `Order` e produz `Shipment`.

```java
// ProcessamentoApplication.java
@SpringBootApplication
public class ProcessamentoApplication {

    @Bean
    public Function<Order, Shipment> processarOrdem(ShippingService shippingService) {
        return order -> shippingService.createShipment(order);
    }
}
```

```yaml
# application.yml
spring:
  cloud:
    function:
      definition: processarOrdem
    stream:
      bindings:
        processarOrdem-in-0:
          destination: topic-ordens
          group: servico-envios
        processarOrdem-out-0:
          destination: topic-envios
      kafka:
        binder:
          brokers: localhost:9092
```

Com essa configuração:

1. O SCSt detecta o bean `processarOrdem` do tipo `Function<Order, Shipment>`.
2. Cria automaticamente o binding `processarOrdem-in-0` apontando para o tópico `topic-ordens`.
3. Cada mensagem recebida é deserializada para `Order`, processada e o resultado `Shipment` é publicado em `topic-envios`.
4. Para trocar para RabbitMQ: substitua a dependência do binder e ajuste as propriedades — o bean `processarOrdem` não muda.

---

## Armadilhas

### (1) Indireção sem ganho real — over-engineering

Se o broker nunca vai mudar e o time não usa outros recursos do SCSt (composição, bindings múltiplos), adicionar a abstração só aumenta o número de camadas para debugar. Uma falha de conexão pode exibir erros do binder, do binding e do broker — rastrear a causa raiz leva mais tempo do que com `@KafkaListener` direto.

**Diagnóstico**: habilite `logging.level.org.springframework.cloud.stream=DEBUG` para ver o que o framework está fazendo.

### (2) Binder errado ou configuração divergente em produção

É comum o ambiente local usar configuração simplificada e produção ter propriedades adicionais (SSL, SASL, particionamento). Se a configuração do binder em produção divergir da local, o comportamento pode ser silenciosamente diferente — por exemplo, o grupo do consumer pode não estar configurado, fazendo a instância receber todas as mensagens.

**Regra**: mantenha os profiles de configuração explícitos e valide o binding de destino e grupo em cada ambiente com `actuator/bindings`.

### (3) Esperar portabilidade total entre Kafka e RabbitMQ

As semânticas são diferentes por design:

| Aspecto | Kafka | RabbitMQ |
|---|---|---|
| Retenção | Configurável (dias/tamanho) | Mensagem removida após ack |
| Replay | Sim (rewind de offset) | Não (por padrão) |
| Routing | Partições por chave | Exchanges + routing keys |
| Consumer group | Gerenciado pelo broker | Gerenciado pelo RabbitMQ |

Código que funciona perfeitamente com Kafka (ex.: dependente de ordenação por partição) pode se comportar de forma diferente com RabbitMQ, mesmo com a mesma configuração SCSt.

---

## Em entrevista

### Frase pronta (inglês)

- *"Spring Cloud Stream decouples application logic from the messaging broker by introducing a binder abstraction."*
- *"Instead of using broker-specific APIs, we define `Supplier`, `Function`, and `Consumer` beans, and the framework handles the binding to Kafka or RabbitMQ."*
- *"The annotation-based model with `@StreamListener` and `@EnableBinding` was removed in version 4.0 — the functional model is the only supported approach today."*
- *"The binding naming convention is `functionName-in-0` for input and `functionName-out-0` for output."*

### Vocabulário

| Termo PT | Termo EN |
|---|---|
| adaptador de broker | binder |
| mapeamento funcional-tópico | binding |
| destino | destination |
| grupo de consumidores | consumer group |
| definição funcional | functional definition |
| abstração com vazamento | leaky abstraction |

---

## Veja também

- [[03-Dominios/Tecnologia/Java/Mensageria/index|Mensageria (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Mensageria/06 - Spring para mensageria — o panorama|Spring para mensageria]]
- [[03-Dominios/Tecnologia/Java/Mensageria/25 - Mensageria reativa — Reactor Kafka|Mensageria reativa]] (planejado)
- [[03-Dominios/Tecnologia/Java/Dicionário de Java|Dicionário de Java]]

---

## Referências

- [Spring Cloud Stream Reference Documentation](https://docs.spring.io/spring-cloud-stream/reference/) — documentação oficial (versão 5.x)
- [Producing and Consuming Messages](https://docs.spring.io/spring-cloud-stream/reference/spring-cloud-stream/producing-and-consuming-messages.html) — modelo funcional detalhado
- [Binding Properties](https://docs.spring.io/spring-cloud-stream/reference/spring-cloud-stream/binding-properties.html) — `destination`, `group`, `contentType`
- [Functional Binding Names](https://docs.spring.io/spring-cloud-stream/reference/spring-cloud-stream/functional-binding-names.html) — convenção `functionName-in-0`
- [Spring Cloud Stream 3.2.x — Notable Deprecations](https://docs.spring.io/spring-cloud-stream/docs/3.2.x/reference/html/spring-cloud-stream.html) — `@EnableBinding`, `@StreamListener` e relacionadas marcadas como deprecated em 3.x
