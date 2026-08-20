---
title: "O ecossistema de brokers na JVM"
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
  - kafka
  - rabbitmq
aliases:
  - "Kafka vs RabbitMQ"
---

# O ecossistema de brokers na JVM

> [!abstract] TL;DR
> Kafka é uma plataforma de event streaming baseada em log distribuído — ideal para alta vazão, retenção configurável e replay. RabbitMQ é um broker AMQP com roteamento rico por exchange e baixa latência — ideal para orquestração de tarefas e filas de trabalho. A escolha depende do requisito, não do hype.

---

## O que é

Um **message broker** é um intermediário que desacopla produtores de consumidores: quem envia uma mensagem não precisa saber quem a processa, nem quando. Esse desacoplamento permite escalar, versionar e falhar partes do sistema de forma independente.

No ecossistema JVM, as opções principais são:

- **Apache Kafka** — plataforma de event streaming baseada em log distribuído.
- **RabbitMQ** — broker de mensageria que implementa AMQP com roteamento por exchange.
- **ActiveMQ Artemis** — broker JMS clássico, amplamente usado em sistemas legados Jakarta EE.
- **Brokers gerenciados na nuvem** — Amazon SQS/SNS, AWS EventBridge, Google Cloud Pub/Sub; eliminam a operação do broker em troca de lock-in e custo variável.

Cada opção resolve um conjunto diferente de problemas. Usar a errada significa pagar caro mais tarde.

---

## Por que importa

A escolha do broker molda a arquitetura inteira do sistema:

- Define se mensagens podem ser **reprocessadas** após uma falha (replay vs. descarte).
- Determina se há **ordenação** garantida entre eventos.
- Impacta o **custo operacional** — Kafka tem overhead de cluster que não faz sentido para filas de baixo volume.
- Estabelece o **modelo de roteamento** — AMQP permite regras finas por routing key; Kafka não.
- Afeta como você **escala consumidores** — consumer groups vs. competing consumers.

Escolher Kafka por ser moderno quando o requisito é uma fila de tarefas simples é um erro clássico de engenharia orientada a hype.

---

## Como funciona

### Kafka — log distribuído, replay e alta vazão

Kafka se define como uma **plataforma de event streaming** com três capacidades fundamentais:

1. **Publicar e subscrever** fluxos de eventos.
2. **Armazenar eventos de forma durável** — os eventos não são apagados após o consumo.
3. **Processar eventos** em tempo real ou retroativamente (replay).

A unidade central é o **tópico**, que funciona como um log append-only particionado entre múltiplos brokers. Cada partição garante ordenação interna: eventos com a mesma chave sempre vão para a mesma partição, e consumidores leem nessa mesma ordem.

**Retenção configurável**: você define por quanto tempo o Kafka guarda os eventos (por tempo ou por tamanho). Dentro desse janela, qualquer consumidor pode reler o histórico do início — isso é o **replay**.

**Consumer groups**: múltiplos consumidores em um mesmo grupo dividem as partições entre si (escala horizontal). Grupos distintos recebem cópias independentes do mesmo stream — padrão fan-out sem replicar mensagens.

> [!note] Internals do Kafka
> Para detalhes de partições, offsets, ISR e compactação de log, veja as notas de fase Adepto do Galho 14 (planejado).

### RabbitMQ — broker AMQP, roteamento rico e filas

RabbitMQ implementa o protocolo **AMQP** (Advanced Message Queuing Protocol) e tem como abstração central o par **exchange → queue**.

O produtor publica mensagens em um **exchange**, não diretamente em uma fila. O exchange decide para quais filas rotear a mensagem com base em regras:

| Tipo de exchange | Comportamento |
|------------------|---------------|
| `direct`         | Roteia pela chave exata (`routing key`) |
| `topic`          | Roteia por padrão com wildcards (`*.error`, `order.#`) |
| `fanout`         | Entrega para todas as filas vinculadas, ignora chave |
| `headers`        | Roteia por atributos do header da mensagem |

Filas armazenam as mensagens até um consumidor retirá-las. Após o consumo (e ACK), a mensagem é removida — **não há replay nativo** sem plugins adicionais.

RabbitMQ brilha em cenários onde o **roteamento é o requisito**: enviar notificações apenas para serviços que se inscreveram em eventos específicos, distribuir tarefas entre workers com lógica de prioridade, ou implementar RPC assíncrono.

### JMS e cloud — ActiveMQ Artemis e brokers gerenciados

**ActiveMQ Artemis** é a implementação de referência do **JMS** (Jakarta Messaging). JMS é uma API Java padronizada; o broker pode ser substituído desde que implemente a spec. É comum em sistemas legados Jakarta EE e em contextos onde a portabilidade da API é mais importante que a performance de ponta.

**Brokers gerenciados na nuvem**:

- **Amazon SQS / SNS**: SQS é fila pura (pull); SNS é pub/sub com fan-out para SQS, Lambda, HTTP.
- **AWS EventBridge**: barramento de eventos com roteamento por regras JSON; integra nativamente com serviços AWS.
- **Google Cloud Pub/Sub**: modelo pub/sub gerenciado com entrega garantida e suporte a replay via snapshot.

A principal vantagem é zerar o custo operacional do cluster. A desvantagem é o lock-in no provedor e o custo variável por mensagem em alto volume.

### Tabela comparativa

| Critério             | Kafka                         | RabbitMQ                        | ActiveMQ Artemis        | SQS / Pub/Sub             |
|----------------------|-------------------------------|----------------------------------|-------------------------|---------------------------|
| Modelo               | Log distribuído               | Broker AMQP                      | Broker JMS              | Fila / Pub-Sub gerenciado |
| Ordenação            | Por partição                  | Por fila (FIFO)                  | Por fila (FIFO)         | SQS FIFO opcional         |
| Retenção / Replay    | Sim (configurável)            | Não nativo (plugin)              | Não nativo              | Limitado (Pub/Sub sim)    |
| Throughput           | Muito alto                    | Alto                             | Moderado                | Varia por serviço         |
| Roteamento           | Por chave de partição         | Rico (exchange + binding)        | Por destino JMS         | Regras JSON (EventBridge) |
| Custo operacional    | Alto (cluster dedicado)       | Médio                            | Médio                   | Baixo (sem infra própria) |

---

## Na prática

**Quando escolher Kafka:**

- Pipeline de eventos de alto volume onde o histórico importa (logs de auditoria, clickstream, telemetria).
- Necessidade de reprocessar eventos após uma correção de bug (replay).
- Múltiplos consumidores independentes precisam do mesmo stream sem duplicar mensagens.
- Integração com Kafka Streams ou ksqlDB para processamento em tempo real.

**Quando escolher RabbitMQ:**

- Orquestração de tarefas com roteamento fino — apenas certos workers recebem certos tipos de tarefa.
- Filas de trabalho com baixo volume e necessidade de ACK granular por mensagem.
- RPC assíncrono sobre infraestrutura de mensageria.
- Time familiarizado com AMQP e sem requisito de replay.

**Quando usar broker gerenciado:**

- Startup ou time pequeno sem capacidade de operar cluster Kafka/RabbitMQ.
- Workload variável onde pagar por mensagem é mais barato que manter cluster ocioso.
- Já existe forte dependência do provedor de nuvem no restante da stack.

---

## Armadilhas

### (1) Escolher por hype, não por requisito

Kafka é excelente — e também é complexo de operar: requer cluster de brokers, gerenciamento de partições, monitoramento de lag de consumer group e tunning de retenção. Para uma fila de envio de e-mails com 50 mensagens/dia, esse overhead não tem retorno.

A pergunta correta não é "qual broker é melhor?" mas "qual problema eu preciso resolver?". Se a resposta for "entregar tarefas para workers com ACK", RabbitMQ ou até SQS resolvem com menos complexidade.

### (2) Kafka para fila de tarefas de baixo volume (overkill operacional)

Kafka não é otimizado para o padrão clássico de fila de tarefas (competing consumers com ACK por mensagem). Seu modelo natural é fan-out por consumer group, não distribuição de carga por mensagem entre instâncias do mesmo grupo dentro de uma partição.

Para distribuir tarefas entre N workers onde qualquer worker pode processar qualquer mensagem, RabbitMQ com competing consumers é a solução direta. Em Kafka, você precisaria mapear workers para partições manualmente — o que adiciona complexidade e limita a escala ao número de partições.

---

## Em entrevista

### Frase pronta (inglês)

> "Kafka and RabbitMQ solve different problems. Kafka is a distributed log optimized for high-throughput event streaming with configurable retention and replay — you read events from an immutable log, and messages are not deleted after consumption. RabbitMQ is an AMQP broker built around rich routing — producers publish to exchanges, which route messages to queues based on binding rules, and messages are removed after acknowledgment. Choosing between them is a matter of requirements: if you need replay, high throughput, or multiple independent consumers on the same stream, Kafka is the natural fit; if you need fine-grained routing, task distribution with per-message ACK, or lower operational overhead, RabbitMQ is usually the better choice."

### Vocabulário

| Português            | Inglês               |
|----------------------|----------------------|
| Corretor / intermediário | broker           |
| Retenção             | retention            |
| Reprocessamento      | replay               |
| Vazão                | throughput           |
| Roteamento           | routing              |
| Gerenciado (nuvem)   | managed              |
| Confirmação de recebimento | acknowledgment (ACK) |
| Fila de tarefas      | task queue / work queue |
| Consumidores concorrentes | competing consumers |
| Defasagem de consumo | consumer lag         |

---

## Veja também

- [[03-Dominios/Tecnologia/Java/Mensageria/index|Mensageria (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Mensageria/02 - Os modelos de mensageria — queue vs topic|Queue vs topic]]
- [[03-Dominios/Tecnologia/Java/Mensageria/15 - Spring AMQP e RabbitMQ|Spring AMQP e RabbitMQ]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java|Dicionário de Java]]

---

## Referências

- Apache Kafka. *Apache Kafka Documentation*. Disponível em: https://kafka.apache.org/documentation/
- Apache Kafka. *Introduction to Apache Kafka*. Disponível em: https://kafka.apache.org/intro
- RabbitMQ. *RabbitMQ Documentation*. Disponível em: https://www.rabbitmq.com/docs
- RabbitMQ. *RabbitMQ Tutorials*. Disponível em: https://www.rabbitmq.com/tutorials
