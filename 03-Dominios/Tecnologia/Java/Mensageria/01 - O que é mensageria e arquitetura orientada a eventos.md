---
title: "O que é mensageria e arquitetura orientada a eventos"
created: 2026-06-11
updated: 2026-06-11
type: concept
status: seedling
publish: true
fase: Iniciado
tags:
  - java
  - mensageria
  - iniciado
  - eventos
aliases:
  - "Arquitetura orientada a eventos"
  - "Event-Driven Architecture"
---

# O que é mensageria e arquitetura orientada a eventos

> [!abstract] TL;DR
> Mensageria é, antes de tudo, **desacoplamento** — temporal e espacial — e não uma técnica de "ir mais rápido". Em vez de um serviço chamar o outro diretamente, ele publica uma mensagem em um intermediário (o *broker*) e segue sua vida; quem se interessa consome quando puder.
> Este galho é a **camada de aplicação Java/Spring** que se assenta sobre a infra Kafka já documentada no vault. Aqui falamos de eventos, comandos, producers e consumers; os internals do broker (partições, offsets) ficam na trilha de infra, que linkamos.

## O que é

Quando você aprendeu a programar, todo trabalho era **síncrono**: o método A chama o método B, espera B terminar, recebe o retorno e só então continua. Em uma chamada HTTP entre serviços a ideia é a mesma — o serviço A faz a requisição e fica bloqueado esperando a resposta do serviço B. Se B estiver lento, A fica lento. Se B estiver fora do ar, A falha.

Mensageria troca esse modelo por um **assíncrono**. A unidade de comunicação deixa de ser "uma chamada com retorno" e passa a ser **a mensagem**: um pacote de dados autocontido que descreve algo (um pedido, um fato, uma ordem). Em vez de entregar a mensagem na mão do destinatário, o remetente a deposita em um **intermediário** — o *broker* (no nosso caso, o Kafka) — que a guarda e a entrega a quem deve recebê-la.

A documentação do Kafka define o conceito-âncora desse modelo de forma seca e útil:

> "An event records the fact that 'something happened' in the world or in your business."

Ou seja, um **evento** (também chamado *record* ou *message* na terminologia Kafka) é o registro de um fato. Guarde essa definição — ela volta na seção sobre comando vs evento.

Os três papéis básicos:

- **Producer** (produtor): a aplicação que publica mensagens no broker.
- **Consumer** (consumidor): a aplicação que lê e processa essas mensagens.
- **Broker**: o servidor intermediário que recebe, guarda de forma durável e entrega as mensagens, organizadas em **tópicos** (categorias nomeadas, como pastas em um sistema de arquivos).

## Por que importa

Três propriedades emergem quando você coloca um broker no meio:

- **Desacoplamento**: o producer não conhece o consumer. Ele publica no tópico `orders` e pronto. Pode haver zero, um ou dez consumers — o producer não muda. Isso é o coração de tudo o que vem a seguir.
- **Resiliência**: se o consumer cai, as mensagens **não se perdem** — ficam guardadas no broker até ele voltar e processá-las. Em uma chamada síncrona, a queda do destinatário derruba a operação inteira.
- **Elasticidade**: picos de carga são absorvidos pela fila. O producer continua publicando no seu ritmo; os consumers processam no ritmo deles. Você pode adicionar mais consumers para escoar um acúmulo sem tocar no producer.

Por que isso cai em **entrevista senior**? Porque separa quem entende sistemas distribuídos de quem só sabe encadear chamadas REST. A pergunta clássica — *"por que você usaria mensageria aqui?"* — tem uma armadilha embutida: o candidato júnior responde "para ser mais rápido". O sênior responde "para desacoplar e ganhar resiliência; a latência percebida até pode melhorar, mas não é o objetivo nem a garantia". Mais sobre isso nas Armadilhas.

## Como funciona

### Desacoplamento temporal e espacial

Esses são os dois eixos do desacoplamento, e vale separá-los porque entrevistadores gostam de ouvir os dois nomes.

**Desacoplamento temporal**: producer e consumer **não precisam estar vivos ao mesmo tempo**. O producer publica às 14h; o consumer pode estar em deploy nesse instante e só ler a mensagem às 14h05. O broker segura a mensagem no intervalo. Em uma chamada síncrona isso seria impossível — os dois lados têm que estar de pé simultaneamente.

**Desacoplamento espacial**: producer e consumer **não precisam se conhecer**. O producer não tem o endereço, o host, nem sequer a noção de quantos consumers existem. Ele conhece apenas o tópico. A documentação do Kafka é explícita sobre o porquê disso ser um princípio de design, não um efeito colateral:

> "In Kafka, producers and consumers are fully decoupled and agnostic of each other, which is a key design element to achieve the high scalability that Kafka is known for."

### Comando vs evento

Nem toda mensagem é igual. A distinção mais importante para modelar bem é entre **comando** e **evento**.

- **Comando**: expressa uma **intenção**, dirigida a **um** destinatário específico, que se espera que **execute** algo. Nome no imperativo: `CreateOrder`, `ChargePayment`. Há uma expectativa de que alguém faça aquilo. Conceitualmente, o emissor *sabe* que quer um efeito.
- **Evento**: expressa um **fato já consumado**, publicado para **N** interessados, sem dirigir-se a ninguém em particular. Nome no passado: `OrderPlaced`, `PaymentApproved`. Ninguém é obrigado a reagir; quem se interessa, reage. Casa exatamente com a definição do Kafka: *"records the fact that something happened"*.

A regra prática: se você se pega nomeando a mensagem no imperativo e pensando "preciso que **aquele** serviço faça isso", é um comando — e talvez uma chamada síncrona fosse mais honesta. Se a mensagem é um fato no passado que outros podem querer saber, é um evento, e a mensageria brilha.

### Pub/sub como inversão de dependência

O padrão **publish/subscribe** (publicar/assinar) é o que materializa o desacoplamento espacial. O producer **publica** em um tópico; consumers **assinam** o tópico. O producer não tem referência alguma aos consumers.

Se você já estudou os princípios SOLID, vai reconhecer isto: pub/sub é uma **inversão de dependência** em escala de arquitetura. Sem mensageria, o módulo de pedidos *depende* do módulo de e-mail (precisa chamá-lo para mandar a confirmação), do módulo de estoque, do módulo de antifraude... cada novo interessado vira uma nova dependência de código no pedido. Com pub/sub, o pedido apenas anuncia `OrderPlaced`; e-mail, estoque e antifraude assinam por conta própria. A seta de dependência se inverte: os interessados dependem do **contrato do evento**, não o pedido dos interessados.

> [!note] Não confunda com o event bus in-process
> O Spring tem um mecanismo de eventos *dentro* de um mesmo processo (o `ApplicationEventPublisher`, visto no Galho 8). Ele aplica a mesma ideia de pub/sub, mas **dentro da JVM** — não sobrevive a uma queda do processo nem cruza a fronteira de rede entre serviços. Mensageria com broker é o mesmo padrão levado para o mundo **distribuído e durável**. Veja [[03-Dominios/Tecnologia/Java/Spring Core e Boot/11 - Eventos do ApplicationContext|Eventos do ApplicationContext]].

## Na prática

Vamos modelar um fato neutro: um pedido foi feito. O evento é um `record` Java imutável — um bom contrato é um dado simples, sem lógica.

```java
// O contrato: um fato, no passado, autocontido.
public record OrderPlacedEvent(
        String orderId,
        String customerId,
        long amountCents) {
}
```

Do lado de quem produz, a aplicação publica o evento em um tópico após concluir sua operação local. Em termos conceituais (a API real do Spring Kafka vem nos próximos galhos):

```java
public class OrderService {

    private final EventPublisher publisher; // abstração conceitual sobre o broker

    public OrderService(EventPublisher publisher) {
        this.publisher = publisher;
    }

    public void placeOrder(Order order) {
        // 1. faz o trabalho de domínio (persiste o pedido, etc.)
        // 2. anuncia o fato — e segue em frente, sem esperar ninguém
        publisher.publish("orders", new OrderPlacedEvent(
                order.id(), order.customerId(), order.amountCents()));
    }
}
```

Note que `placeOrder` **não chama** o serviço de e-mail nem o de estoque. Ele publica e termina. Do outro lado, quem se interessa assina o tópico e reage:

```java
// Um listener conceitual. No Spring Kafka isto vira um método anotado
// com @KafkaListener — coberto adiante no galho.
public class PaymentListener {

    public void onOrderPlaced(OrderPlacedEvent event) {
        // reage ao fato: inicia a cobrança do pagamento
        // o producer (OrderService) nunca soube que este listener existe
        chargeCustomer(event.customerId(), event.amountCents());
    }

    private void chargeCustomer(String customerId, long amountCents) {
        // ... lógica de cobrança
    }
}
```

Se amanhã o time de marketing quiser disparar um e-mail de boas-vindas ao primeiro pedido de um `Customer`, basta criar um novo listener que assina `orders`. O `OrderService` não muda **uma linha**. Esse é o desacoplamento espacial pagando dividendos.

## Armadilhas

### (1) Tratar mensageria como otimização de performance

A confusão mais comum entre iniciados: "vou usar fila para ficar mais rápido". Mensageria **não é sobre velocidade**, é sobre desacoplamento. Em muitos casos você até *adiciona* latência fim-a-fim (a mensagem passa pelo broker, é persistida, depois entregue). O que você ganha é que o **producer** não fica bloqueado e o sistema absorve picos — a *throughput* e a *resiliência* melhoram, não necessariamente o tempo de uma operação individual.

> Exemplo: trocar uma chamada REST de 50 ms por um evento que o consumer processa 200 ms depois não deixou nada "mais rápido" — deixou o producer livre e o sistema tolerante a falhas do consumer.

**Fix**: justifique a escolha por desacoplamento/resiliência/elasticidade; se o requisito real é resposta imediata e síncrona, mensageria é a ferramenta errada.

### (2) Acoplar o consumer ao schema interno do producer

Você publica `OrderPlacedEvent` e, por preguiça, serializa a entidade `Order` inteira do banco — com campos internos, colunas de auditoria, FKs. O consumer passa a depender desse formato. Quando o producer refatora a tabela `Order`, **todos os consumers quebram**. Você reintroduziu, pela porta dos fundos, exatamente o acoplamento que a mensageria veio eliminar.

> Exemplo: enviar `Order` (JPA entity) no evento em vez de um `OrderPlacedEvent` enxuto e estável faz o consumer refém da modelagem de persistência do producer.

**Fix**: o contrato do evento é uma API pública — modele um DTO/record estável e versionável, independente do schema interno do producer.

## Em entrevista

### Frase pronta (inglês)

> "I'd reach for messaging here primarily to decouple the services, not to make any single call faster. By publishing an `OrderPlaced` event to a broker, the order service stays available even if downstream consumers are slow or temporarily down — the broker buffers the events and they get processed when consumers recover. The important caveat is that messaging is about decoupling, not speed: end-to-end latency can actually grow, so if the business needs an immediate synchronous response, I'd keep that path as a direct call and only move the fire-and-forget, fan-out work onto the broker."

### Vocabulário

| Termo PT | Termo EN |
| --- | --- |
| mensageria | messaging |
| evento (record) | event (record) |
| comando | command |
| fila | queue |
| tópico | topic |
| broker (intermediário) | broker |
| desacoplamento | decoupling |
| publicar/assinar | publish/subscribe |
| produtor / consumidor | producer / consumer |
| orientado a eventos | event-driven |

## Veja também

- [[03-Dominios/Tecnologia/Java/Mensageria/index|Mensageria (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Backend/Kafka/index|Kafka (a infra)]] — os fundamentos de infra (partições, offsets, replicação) que este galho assume e não re-explica
- [[03-Dominios/Tecnologia/Java/Spring Core e Boot/11 - Eventos do ApplicationContext|Eventos do ApplicationContext]] — o event bus in-process do Spring (Galho 8)
- [[03-Dominios/Tecnologia/Java/Mensageria/03 - Garantias de entrega — e a falácia do exactly-once|Garantias de entrega]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java|Dicionário de Java]]

Galhos seguintes da trilha — Build (planejado), Microservices (planejado), Cloud (planejado) e OCP (planejado) — vão se apoiar nos conceitos abertos aqui.

## Referências

- [Apache Kafka — Introduction](https://kafka.apache.org/intro) — definição oficial de *event* ("records the fact that something happened") e do desacoplamento total entre producers e consumers.
- [Spring for Apache Kafka — Reference](https://docs.spring.io/spring-kafka/reference/) — a camada de aplicação: `KafkaTemplate` como abstração de alto nível para envio e `@KafkaListener` para POJOs orientados a mensagens.
- [Apache Kafka — Documentation](https://kafka.apache.org/documentation/) — documentação de referência do broker.
