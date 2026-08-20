---
title: "Kafka numa página para o dev de aplicação"
created: 2026-06-11
updated: 2026-06-11
type: concept
status: seedling
publish: true
fase: iniciado
tags:
  - java
  - mensageria
  - iniciado
  - kafka
aliases:
  - "Kafka para devs"
---

# Kafka numa página para o dev de aplicação

> [!abstract] TL;DR
> Como dev de aplicação, você precisa saber três coisas sobre Kafka: onde sua mensagem vai parar (tópico + partição determinada pela chave), quem a lê (consumer group com escala limitada pelo número de partições) e que o Kafka 4.0 removeu o ZooKeeper — você não precisa mais gerenciar um segundo cluster de metadados. O restante — replicação, ISR, líderes de partição — é responsabilidade da infraestrutura. Este documento dá o modelo de app; os internals ficam nos links de [[03-Dominios/Tecnologia/Java/Backend/Kafka/Kafka Concepts/index|Kafka Concepts]].

---

## O que é

Kafka é um **log distribuído de commits** — uma sequência imutável de registros ordenados por tempo de chegada, persistida em disco e replicada entre brokers.

A metáfora central é o **append-only log**: ninguém apaga uma linha do meio do caderno; só se escreve no final. Consumir uma mensagem não a remove: ela fica disponível enquanto a política de retenção permitir (por tempo ou por tamanho). Isso significa que múltiplos sistemas podem ler o mesmo evento de forma independente, cada um avançando no próprio ritmo.

Para o dev de aplicação, o Kafka não é uma fila clássica (onde a mensagem some após consumida). É um **barramento de eventos duráveis** que desacopla produtores de consumidores no tempo e no espaço.

---

## Por que importa

- **Desacoplamento real**: o produtor não sabe quem consome nem quando — publica no tópico e segue em frente.
- **Escala horizontal**: adicionar partições aumenta o throughput de produção e permite mais consumidores em paralelo dentro de um grupo.
- **Reprocessamento**: como os eventos ficam retidos, é possível "rebobinar" o offset e re-processar um lote de mensagens após um bug corrigido.
- **Padrão de mercado**: é o backbone de arquiteturas event-driven em escala (finanças, e-commerce, streaming de dados). Aparecer em entrevistas para posições senior sem saber Kafka é um sinal de alerta.

---

## Como funciona

### Tópico, partição e offset — visão de app

Um **tópico** é o nome lógico do canal de eventos (ex.: `pedido-criado`, `pagamento-processado`). Ao publicar, o producer envia para um tópico.

Internamente, cada tópico é dividido em **partições** — arquivos de log independentes. A partição para onde uma mensagem vai é determinada pela **chave** (`key`) da mensagem:

- Mesma chave → sempre a mesma partição (garantia de ordenação por chave).
- Sem chave → round-robin entre partições disponíveis.

O **offset** é a posição da mensagem dentro de uma partição — um número inteiro sequencial que começa em zero. O offset identifica unicamente uma mensagem dentro de uma partição. O consumer controla até qual offset já leu.

> [!important] O que NÃO é seu problema aqui
> Replicação entre brokers, líderes de partição, ISR (In-Sync Replicas) — tudo isso é responsabilidade da infra. Como dev de app, você escolhe a chave, o tópico e configura o `acks`. O restante fica transparente. Detalhes em [[03-Dominios/Tecnologia/Java/Backend/Kafka/Kafka Concepts/7. Partitions|Partitions]] e [[03-Dominios/Tecnologia/Java/Backend/Kafka/Kafka Concepts/12. Consumer Offsets|Consumer Offsets]].

### Consumer group

Um **consumer group** é um conjunto de instâncias da sua aplicação que divide o trabalho de consumir um tópico. O Kafka garante que **cada partição é lida por no máximo um consumer dentro do grupo** ao mesmo tempo.

Regra de ouro para escala:

```text
consumers ativos no grupo ≤ número de partições do tópico
```

Se você tem 3 partições e sobe 5 instâncias no mesmo grupo, 2 ficarão ociosas. Se sobe 2 instâncias, uma delas lê 2 partições. O **rebalance** redistribui as partições automaticamente quando instâncias entram ou saem do grupo.

Desde o Kafka 4.0, o protocolo de rebalance foi reescrito (KIP-848) para eliminar o "stop-the-world rebalance" — o grupo não para de consumir enquanto um novo consumer entra.

Detalhes em [[03-Dominios/Tecnologia/Java/Backend/Kafka/Kafka Concepts/11. Consumer Groups|Consumer Groups]].

### KRaft — o fim do ZooKeeper

Antes do Kafka 4.0, qualquer cluster precisava de um ensemble Apache ZooKeeper separado para gerenciar metadados (quem é o líder de qual partição, lista de tópicos, etc.). Isso significava operar dois sistemas distribuídos ao mesmo tempo.

**No Apache Kafka 4.0.0 (lançado em 18/03/2025), o ZooKeeper foi completamente removido.** A documentação oficial afirma:

> *"Kafka 4.0 is a significant milestone, marking the first major release to operate entirely without Apache ZooKeeper®."*

O **KRaft** (Kafka Raft Metadata) é agora o único modo de metadados. O próprio cluster Kafka gerencia seus metadados internamente usando o protocolo Raft. Para o dev de aplicação, isso não muda nenhuma linha de código — muda a vida de quem opera a infra.

---

## Na prática

Configuração mínima de uma aplicação Spring Boot que fala com Kafka:

```yaml
spring:
  kafka:
    bootstrap-servers: localhost:9092
    consumer:
      group-id: meu-servico-grupo
      auto-offset-reset: earliest
      key-deserializer: org.apache.kafka.common.serialization.StringDeserializer
      value-deserializer: org.springframework.kafka.support.serializer.JsonDeserializer
      properties:
        spring.json.trusted.packages: "com.exemplo.eventos"
    producer:
      key-serializer: org.apache.kafka.common.serialization.StringSerializer
      value-serializer: org.springframework.kafka.support.serializer.JsonSerializer
```

O que cada linha faz do ponto de vista do dev de app:

| Propriedade | Por que importa |
|---|---|
| `bootstrap-servers` | Endereço de entrada do cluster — não precisa listar todos os brokers |
| `group-id` | Nome do consumer group desta aplicação |
| `auto-offset-reset` | O que fazer quando não há offset salvo: `earliest` = do início, `latest` = só novos |
| `trusted.packages` | Segurança: quais pacotes o deserializador JSON aceita |

Para consumir, basta anotar um método com `@KafkaListener` — veja [[03-Dominios/Tecnologia/Java/Mensageria/08 - @KafkaListener — consumindo mensagens|@KafkaListener]].

---

## Armadilhas

### (1) Mais consumers que partições — consumers ociosos

É o erro de escala mais comum. Se o tópico `pedido-criado` tem 4 partições e você sobe 6 pods, 2 pods ficam completamente ociosos — nunca recebem uma mensagem. O remédio é aumentar as partições do tópico (operação de infra, não de app) ou reduzir as instâncias ao número certo.

> [!caution] Cuidado ao aumentar partições
> Aumentar partições de um tópico existente quebra a garantia de ordenação por chave para mensagens já publicadas, pois a chave pode ir parar em uma partição diferente. Planeje o número de partições antes de ir para produção.

### (2) Tentar reaprender internals quando o modelo de app é suficiente

Num projeto com prazo ou numa entrevista com 30 minutos de tempo, entrar em replicação, ISR, eleição de líder e compacção de log é perda de foco quando o problema em mãos é "o consumer não está lendo as mensagens". O debug de app passa por: offset correto? group-id correto? deserializador compatível? partições suficientes para o número de instâncias? Os internals estão linkados abaixo para quando você precisar deles.

---

## Em entrevista

### Frase pronta (inglês)

"Kafka is a distributed commit log where producers append events to topics, and each topic is split into partitions for parallel processing. Consumer groups allow horizontal scaling by assigning each partition to exactly one consumer within the group, so the maximum parallelism is bounded by the partition count. Since Kafka 4.0, ZooKeeper has been removed — the cluster manages its own metadata through KRaft, the built-in Raft-based consensus protocol."

### Vocabulário

| Português | Inglês | Contexto de uso |
|---|---|---|
| tópico | topic | "publish to a topic", "subscribe to a topic" |
| partição | partition | "the number of partitions determines max parallelism" |
| deslocamento | offset | "commit the offset after processing" |
| grupo de consumidores | consumer group | "each service has its own consumer group" |
| retenção | retention | "retention policy: 7 days or 100 GB" |
| chave | key | "messages with the same key go to the same partition" |
| metadados | metadata | "KRaft manages cluster metadata without ZooKeeper" |
| rebalanceamento | rebalance | "consumer group rebalance when a pod restarts" |

---

## Veja também

- [[03-Dominios/Tecnologia/Java/Mensageria/index|Mensageria (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Backend/Kafka/Kafka Concepts/index|Kafka Concepts (os fundamentos de infra)]]
- [[03-Dominios/Tecnologia/Java/Backend/Kafka/Kafka Concepts/7. Partitions|Partitions]]
- [[03-Dominios/Tecnologia/Java/Backend/Kafka/Kafka Concepts/11. Consumer Groups|Consumer Groups]]
- [[03-Dominios/Tecnologia/Java/Backend/Kafka/Kafka Concepts/12. Consumer Offsets|Consumer Offsets]]
- [[03-Dominios/Tecnologia/Java/Mensageria/08 - @KafkaListener — consumindo mensagens|@KafkaListener]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java|Dicionário de Java]]

---

## Referências

- Apache Kafka 4.0.0 Release Announcement (18/03/2025): https://kafka.apache.org/blog/2025/03/18/apache-kafka-4.0.0-release-announcement/
- Apache Kafka Documentation: https://kafka.apache.org/documentation/
- KIP-848 — The Next Generation of the Consumer Rebalance Protocol: https://cwiki.apache.org/confluence/display/KAFKA/KIP-848
