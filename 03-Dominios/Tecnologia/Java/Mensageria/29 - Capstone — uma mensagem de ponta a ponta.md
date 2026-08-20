---
title: "Capstone — uma mensagem de ponta a ponta"
created: 2026-06-11
updated: 2026-06-11
type: concept
status: seedling
publish: true
fase: Magus
tags:
  - java
  - mensageria
  - magus
  - capstone
aliases:
  - "Capstone Mensageria"
---

# Capstone — uma mensagem de ponta a ponta

> [!abstract] TL;DR
> Esta é a nota que costura o Galho 14 num único trace. Siga **um** comando — "criar o pedido" — do clique do cliente até o efeito colateral lá na ponta (o pacote despachado), e veja **onde cada uma das 28 notas entra**. A tese do galho inteiro cabe em duas frases: **mensageria é desacoplamento, não velocidade** — você troca uma chamada síncrona por uma assíncrona porque quer que produtor e consumidor evoluam, escalem e falhem de forma independente, não porque "é mais rápido". E **exactly-once distribuído é um mito**: o que existe de verdade é **at-least-once + idempotência**, com a entrega podendo se repetir e o consumidor se defendendo. Se você internalizar só isso, já não cai nas duas maiores ciladas da área.

## O fluxo completo

A história tem domínios neutros de propósito: um serviço **Order**, um serviço **Payment** e um serviço **Shipment**. Um comando chega ao Order. Acompanhe a mensagem nascer, viajar e morrer (bem).

```text
  [Cliente]
     │  POST /orders  (comando síncrono via HTTP/REST)
     ▼
 ┌─────────────────────────── Order Service ───────────────────────────┐
 │                                                                      │
 │  ① UMA transação de banco:                                           │
 │     ├── INSERT INTO orders        (estado de negócio)                │
 │     └── INSERT INTO outbox        (o evento, na MESMA tx) ── nota 21 │
 │                                                                      │
 │  ② commit  ──► estado e intenção-de-publicar gravados atomicamente   │
 └──────────────────────────────────┬───────────────────────────────────┘
                                     │
       ③ Relay / Debezium lê a outbox e publica ──────── nota 21 / 19
                                     │  KafkaTemplate.send(...) ── nota 07
                                     ▼
                        ┌────────────────────────┐
                        │  Tópico Kafka          │
                        │  "orders.created"      │  particionado por orderId
                        │  (durável, replicado)  │  ── notas 05 / 02
                        └───────────┬────────────┘
                                    │  at-least-once ── nota 03
                ┌───────────────────┴───────────────────┐
                ▼                                        ▼
   ┌──────── Payment Service ────────┐      ┌──────── Shipment Service ───────┐
   │  ④ @KafkaListener  ── nota 08    │      │  @KafkaListener (outro grupo)   │
   │  ⑤ consumidor IDEMPOTENTE        │      │  reage ao "payment.captured"    │
   │     (dedup por orderId/msgId)    │      │  publica "shipment.dispatched"  │
   │     ── nota 20                    │      └─────────────────────────────────┘
   │  ⑥ efeito: captura o pagamento   │
   │     publica "payment.captured"   │
   │                                   │
   │  ⑦ em ERRO no consumo:            │
   │     retry com backoff ── nota 11  │
   │       │  esgotou as tentativas?   │
   │       ▼                           │
   │     Dead Letter Topic ── nota 12  │
   └───────────────────────────────────┘
                │
   ⑧ Observabilidade transversal ── nota 26
      ├── consumer lag (a fila está crescendo?)
      └── tracing distribuído (traceId atravessa Order→Payment→Shipment)
```

Lendo passo a passo, com os pontos onde "cada nota acende":

1. **O comando chega.** O cliente faz um `POST /orders`. Repare: a *borda* do sistema ainda é **síncrona** (REST). Mensageria não é obrigação na entrada — é uma escolha sobre o que acontece *depois* do commit (nota 01).
2. **Grava estado + outbox na mesma transação.** O Order insere o pedido **e** o evento `OrderCreated` numa tabela `outbox`, dentro da **mesma** transação de banco. É o [[03-Dominios/Tecnologia/Java/Mensageria/21 - O padrão Outbox|padrão Outbox]] resolvendo o problema clássico do "dual write": você **não** pode escrever no banco e publicar no broker em duas operações separadas e fingir que é atômico — uma das duas pode falhar. A outbox transforma "gravar + publicar" em **uma única** escrita transacional.
3. **O relay publica.** Um processo separado (um relay polling, ou Debezium via CDC lendo o log do banco — nota 19) lê a outbox e publica no Kafka usando o [[03-Dominios/Tecnologia/Java/Mensageria/07 - KafkaTemplate — produzindo mensagens|KafkaTemplate]]. Aqui mora a verdade incômoda: esse relay garante **at-least-once**. Se ele publicar e cair antes de marcar a linha como enviada, ele republica no restart. **Duplicata é o estado normal**, não a exceção (nota 03).
4. **O consumidor consome.** Payment escuta o tópico com [[03-Dominios/Tecnologia/Java/Mensageria/08 - @KafkaListener — consumindo mensagens|@KafkaListener]]. O container do Spring puxa do broker, desserializa (nota 09) e entrega ao seu método.
5. **O consumidor é idempotente.** Antes de fazer qualquer efeito, Payment checa: "já processei essa mensagem?". Isso é o pilar do [[03-Dominios/Tecnologia/Java/Mensageria/20 - Idempotência — o pilar do at-least-once|consumidor idempotente]]. Como a entrega é at-least-once, a *única* defesa contra processar duas vezes é o consumidor reconhecer o que já viu — por um `messageId` único, por chave de negócio, por estado-alvo. **Idempotência é o que torna at-least-once seguro.**
6. **O efeito acontece.** Pagamento capturado. Payment publica `payment.captured`, que Shipment consome e reage despachando o pacote. Note o encadeamento: cada serviço reage a um evento e emite o próximo. Ninguém *chama* ninguém — todos *reagem*. Esse é o desacoplamento da nota 01 em ação.
7. **Em erro: retry, depois DLQ.** Se o consumo falha (banco fora, payload corrompido, downstream indisponível), entra o [[03-Dominios/Tecnologia/Java/Mensageria/11 - Tratamento de erro no consumo|tratamento de erro]]: retry com backoff para falhas transitórias. Esgotadas as tentativas, a mensagem vai para o [[03-Dominios/Tecnologia/Java/Mensageria/12 - Dead Letter Topic — o padrão DLQ|Dead Letter Topic]] — ela sai do caminho quente para não travar a partição inteira, e fica num lugar onde alguém pode inspecionar e reprocessar. Um *poison message* nunca deve bloquear o fluxo dos pedidos saudáveis.
8. **Observabilidade fecha o ciclo.** Transversal a tudo, a [[03-Dominios/Tecnologia/Java/Mensageria/26 - Observabilidade em mensageria|observabilidade]]: o **consumer lag** te diz se o consumo está acompanhando a produção (fila crescendo = você está afundando), e o **tracing distribuído** carrega um `traceId` de Order → Payment → Shipment, para que um pedido "perdido" possa ser seguido através dos saltos assíncronos. Sem isso, mensageria vira uma caixa-preta onde mensagens somem sem rastro.

Esse é o trace inteiro. Cada nota do galho é uma lupa sobre um trecho dele.

## A tabela de decisão

Antes de jogar Kafka em tudo, passe pela árvore de decisão. A pergunta nunca é "qual broker?" — é "**eu preciso mesmo de mensageria aqui?**".

| Pergunta | Quando uma resposta | Quando a outra |
| --- | --- | --- |
| **Preciso de um broker, ou um event bus in-process basta?** (nota 16) | Use `ApplicationEvent` / `@EventListener` **in-process** quando produtor e consumidor vivem no **mesmo processo/deploy**, sem necessidade de durabilidade ou de cruzar fronteira de serviço. Zero infra extra. | Use um **broker** (Kafka/Rabbit) quando o evento precisa **sobreviver a um restart**, **cruzar serviços** ou **escalar consumidores** de forma independente. O preço é uma peça de infra a operar. |
| **Kafka ou RabbitMQ?** (notas 04 / 15) | **Kafka** quando você quer um **log durável e reprodutível** — alto throughput, retenção, *replay*, várias equipes lendo o mesmo stream, event sourcing. O consumidor controla o offset. | **RabbitMQ** quando você quer **roteamento rico** e semântica de *fila de trabalho* — exchanges, routing keys, prioridades, RPC, e a mensagem some depois do ack. O broker empurra e descarta. |
| **A interação é síncrona por natureza (preciso da resposta agora)?** (nota 28) | Se você **precisa da resposta para continuar** (request/response, baixa latência, contrato forte), use **gRPC** (planejado, nota 28) — RPC tipado sobre HTTP/2. Isso **não é** mensageria; é chamada síncrona. Não force um broker no meio só por moda. | Se o chamador **não precisa esperar** o resultado — pode reagir depois, ou nunca — então é assíncrono: publique um evento e siga em frente. |
| **Que garantia de entrega eu assumo?** (notas 03 / 20) | Assuma **at-least-once** como default e **torne o consumidor idempotente** (nota 20). Isso cobre 99% dos casos de negócio com robustez real. | "Exactly-once" só faz sentido **dentro de um cluster Kafka** via transações (nota 13), e mesmo lá tem fronteiras. Atravessou pro banco ou pra outro serviço? Voltou a ser at-least-once + idempotência. **Não prometa exactly-once de ponta a ponta** — não existe. |

## Cheatsheet — nota → problema que resolve

| # | Nota | Problema que resolve |
| --- | --- | --- |
| 01 | [[03-Dominios/Tecnologia/Java/Mensageria/01 - O que é mensageria e arquitetura orientada a eventos\|Mensageria e EDA]] | Por que e quando desacoplar serviços por eventos em vez de chamadas diretas. |
| 02 | [[03-Dominios/Tecnologia/Java/Mensageria/02 - Os modelos de mensageria — queue vs topic\|Queue vs topic]] | Um consumidor por mensagem (fila) ou broadcast pra muitos (tópico)? |
| 03 | [[03-Dominios/Tecnologia/Java/Mensageria/03 - Garantias de entrega — e a falácia do exactly-once\|Garantias de entrega]] | At-most / at-least / "exactly"-once e por que o último é miragem. |
| 04 | [[03-Dominios/Tecnologia/Java/Mensageria/04 - O ecossistema de brokers na JVM\|Ecossistema de brokers]] | Que broker escolher na JVM e os trade-offs de cada um. |
| 05 | [[03-Dominios/Tecnologia/Java/Mensageria/05 - Kafka numa página para o dev de aplicação\|Kafka numa página]] | O modelo mental de Kafka (log, partição, offset, grupo) sem operar cluster. |
| 06 | [[03-Dominios/Tecnologia/Java/Mensageria/06 - Spring para mensageria — o panorama\|Spring para mensageria]] | Que abstrações o Spring oferece e qual usar quando. |
| 07 | [[03-Dominios/Tecnologia/Java/Mensageria/07 - KafkaTemplate — produzindo mensagens\|KafkaTemplate]] | Como publicar com garantias (acks, key, partição) a partir da app. |
| 08 | [[03-Dominios/Tecnologia/Java/Mensageria/08 - @KafkaListener — consumindo mensagens\|@KafkaListener]] | Como consumir de forma declarativa com o container do Spring. |
| 09 | [[03-Dominios/Tecnologia/Java/Mensageria/09 - (De)serialização de mensagens\|(De)serialização]] | Como bytes viram objetos e vice-versa, e onde isso quebra. |
| 10 | [[03-Dominios/Tecnologia/Java/Mensageria/10 - Ack modes e commit de offset\|Ack e offset]] | Quando o offset é commitado — e como isso define a garantia real. |
| 11 | [[03-Dominios/Tecnologia/Java/Mensageria/11 - Tratamento de erro no consumo\|Erro no consumo]] | Retry com backoff, falhas transitórias vs permanentes. |
| 12 | [[03-Dominios/Tecnologia/Java/Mensageria/12 - Dead Letter Topic — o padrão DLQ\|DLQ]] | Onde colocar a *poison message* para não travar a partição. |
| 13 | [[03-Dominios/Tecnologia/Java/Mensageria/13 - Transações e exactly-once no Spring Kafka\|Transações no Spring Kafka]] | O "exactly-once" possível: read-process-write transacional *dentro* do Kafka. |
| 14 | [[03-Dominios/Tecnologia/Java/Mensageria/14 - Schema e contratos — Avro e Schema Registry\|Schema e contratos]] | Como impor um contrato à mensagem e validar compatibilidade. |
| 15 | [[03-Dominios/Tecnologia/Java/Mensageria/15 - Spring AMQP e RabbitMQ\|Spring AMQP / RabbitMQ]] | Roteamento por exchange e semântica de fila de trabalho. |
| 16 | [[03-Dominios/Tecnologia/Java/Mensageria/16 - Eventos in-process do Spring\|Eventos in-process]] | Desacoplar *dentro* do processo sem pagar infra de broker. |
| 17 | [[03-Dominios/Tecnologia/Java/Mensageria/17 - Spring Cloud Stream — a abstração de binders\|Spring Cloud Stream]] | Escrever lógica de stream agnóstica ao broker via binders. |
| 18 | [[03-Dominios/Tecnologia/Java/Mensageria/18 - Kafka Streams pela API Java\|Kafka Streams]] | Processar/transformar streams (join, agregação) como topologia. |
| 19 | [[03-Dominios/Tecnologia/Java/Mensageria/19 - Kafka Connect pela ótica da app\|Kafka Connect]] | Mover dados entre sistemas e banco↔Kafka (CDC) sem código de cola. |
| 20 | [[03-Dominios/Tecnologia/Java/Mensageria/20 - Idempotência — o pilar do at-least-once\|Idempotência]] | Tornar at-least-once seguro: reprocessar sem duplicar efeito. |
| 21 | [[03-Dominios/Tecnologia/Java/Mensageria/21 - O padrão Outbox\|Outbox]] | Resolver o dual-write: gravar estado e publicar atomicamente. |
| 22 | [[03-Dominios/Tecnologia/Java/Mensageria/22 - Saga — transações distribuídas por eventos\|Saga]] | Coordenar uma transação de negócio entre serviços, com compensação. |
| 23 | [[03-Dominios/Tecnologia/Java/Mensageria/23 - Event sourcing e CQRS\|Event sourcing e CQRS]] | Tratar o log de eventos como fonte da verdade e separar leitura/escrita. |
| 24 | [[03-Dominios/Tecnologia/Java/Mensageria/24 - Versionamento e evolução de eventos\|Evolução de eventos]] | Evoluir o schema sem quebrar consumidores antigos. |
| 25 | [[03-Dominios/Tecnologia/Java/Mensageria/25 - Mensageria reativa — Reactor Kafka\|Mensageria reativa]] | Consumir/produzir com backpressure no modelo reativo. |
| 26 | [[03-Dominios/Tecnologia/Java/Mensageria/26 - Observabilidade em mensageria\|Observabilidade]] | Consumer lag e tracing distribuído para enxergar o assíncrono. |
| 27 | [[03-Dominios/Tecnologia/Java/Mensageria/27 - Protocol Buffers — a IDL e a serialização binária\|Protocol Buffers]] | Contrato tipado e serialização binária compacta entre serviços. |
| 28 | [[03-Dominios/Tecnologia/Java/Mensageria/28 - gRPC em Java — RPC síncrono sobre HTTP_2\|gRPC em Java]] | RPC síncrono tipado — a alternativa quando você precisa da resposta agora. |

## Armadilhas de raciocínio

### (1) "Evento pra tudo"

A empolgação com EDA leva a publicar um evento para cada espirro do sistema, criando uma teia onde ninguém entende mais quem dispara o quê. Eventos introduzem **acoplamento temporal** invertido e custo cognitivo: um fluxo que era uma chamada de método legível vira uma caça ao tesouro entre tópicos. Quando produtor e consumidor estão no **mesmo processo** e não há ganho de durabilidade ou escala independente, um evento in-process (nota 16) — ou simplesmente uma chamada de método síncrona, ou um gRPC (nota 28) quando você precisa da resposta — é mais honesto. **Mensageria é uma ferramenta de desacoplamento entre fronteiras, não um tempero universal.**

### (2) "Exactly-once resolve"

A frase "vou configurar exactly-once e parar de me preocupar com duplicatas" é a cilada mais cara do galho. **Exactly-once de ponta a ponta, atravessando serviços e bancos, não existe** — é um teorema sobre sistemas distribuídos, não uma flag. O que o Kafka oferece (nota 13) é exactly-once *dentro* de um ciclo read-process-write *no próprio cluster*. Assim que o efeito toca um banco externo ou outro serviço, você está de volta ao mundo real: **at-least-once**. A resposta correta nunca é caçar a entrega perfeita; é **assumir a duplicata e neutralizá-la com idempotência** (nota 20). Quem entende isso projeta consumidores robustos; quem não entende projeta sistemas que parecem corretos até a primeira reentrega.

### (3) "Broker é o default"

Adicionar Kafka "porque microserviços usam Kafka" é decisão por modismo, não por engenharia. Um broker é **infraestrutura nova para operar, monitorar, versionar schema e debugar** — e introduz consistência eventual onde antes havia uma transação simples. Mensageria é um **trade-off**: você ganha desacoplamento, resiliência e escala independente, e paga com complexidade operacional, eventual consistency e a necessidade de idempotência, DLQ e observabilidade. Para muitos casos, uma chamada síncrona, um evento in-process ou um job agendado resolvem com uma fração do custo. **Escolha mensageria deliberadamente, pesando o que ganha contra o que passa a ter que sustentar.**

## Em entrevista

### Frase pronta (inglês)

> Messaging is fundamentally about **decoupling**, not speed. We introduce a broker between services so that producer and consumer can scale, evolve, and fail independently — the latency of the broker itself is a cost we accept, not a benefit we chase. The single most important thing to internalize is that **distributed exactly-once is a myth**: real systems deliver **at-least-once**, so duplicates are the normal case, and the consumer must be **idempotent** to make that safe. Everything else — the Outbox pattern to avoid dual writes, retries and a dead-letter topic for poison messages, consumer lag and distributed tracing for observability, and Sagas to coordinate a business transaction across services with compensation — is built on top of that single, sober assumption.

### Vocabulário

| Termo (EN) | Em PT-BR / o que significa |
| --- | --- |
| At-least-once delivery | Entrega ao menos uma vez — a mensagem pode chegar repetida; o default realista. |
| Idempotent consumer | Consumidor idempotente — processar a mesma mensagem N vezes tem o mesmo efeito que processá-la uma vez. |
| Dual write problem | Problema do dual-write — gravar no banco e publicar no broker em duas operações não é atômico; resolvido pelo Outbox. |
| Dead-letter topic (DLQ) | Tópico de mensagens mortas — destino da mensagem que falhou após os retries, para não travar a partição. |
| Consumer lag | Atraso do consumidor — distância entre o último offset produzido e o consumido; fila crescendo = afundando. |
| Saga | Transação distribuída por eventos, com passos compensatórios em vez de rollback global. |

## Veja também

- [[03-Dominios/Tecnologia/Java/Mensageria/index|Mensageria (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Mensageria/03 - Garantias de entrega — e a falácia do exactly-once|Garantias de entrega — a falácia do exactly-once]]
- [[03-Dominios/Tecnologia/Java/Mensageria/20 - Idempotência — o pilar do at-least-once|Idempotência — o pilar do at-least-once]]
- [[03-Dominios/Tecnologia/Java/Mensageria/21 - O padrão Outbox|O padrão Outbox]]
- [[03-Dominios/Tecnologia/Java/Mensageria/22 - Saga — transações distribuídas por eventos|Saga — transações distribuídas]]
- [[03-Dominios/Tecnologia/Java/Mensageria/28 - gRPC em Java — RPC síncrono sobre HTTP_2|gRPC em Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java|Dicionário de Java]]

## Referências

- Hohpe, Gregor; Woolf, Bobby. *Enterprise Integration Patterns* — o cânone dos padrões de mensageria (Outbox, DLQ, roteamento, idempotência).
- Kleppmann, Martin. *Designing Data-Intensive Applications*, cap. 11 (Stream Processing) — garantias de entrega, logs e a discussão honesta sobre exactly-once.
- Richardson, Chris. *Microservices Patterns* — Saga, Outbox/Transactional Outbox, CDC e EDA aplicados a microserviços.
- Documentação Apache Kafka — semântica de entrega, transações e idempotência do producer.
- Documentação Spring for Apache Kafka — `KafkaTemplate`, `@KafkaListener`, error handling, DLQ e suporte transacional.
