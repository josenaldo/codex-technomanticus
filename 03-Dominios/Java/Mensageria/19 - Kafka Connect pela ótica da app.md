---
title: "Kafka Connect pela ótica da app"
fase: magus
tags:
  - java
  - mensageria
  - magus
  - kafka
created: 2026-06-11
updated: 2026-06-11
type: concept
status: seedling
publish: true
aliases:
  - Kafka Connect
---

# Kafka Connect pela ótica da app

> [!abstract] TL;DR
> Kafka Connect é a camada de integração do ecossistema Kafka: move dados *entre sistemas externos e tópicos* sem que você precise escrever um producer ou consumer para isso. Source connectors puxam dados para o Kafka; sink connectors empurram dados do Kafka para destinos. SMTs (Single Message Transforms) permitem transformações leves em trânsito. Como dev de aplicação, sua principal decisão é: "isso é movimentação de dados ou lógica de negócio?" — Connect resolve o primeiro caso; código de app resolve o segundo.

---

## O que é

Kafka Connect é um framework de integração de dados distribuído, parte nativa do Apache Kafka, projetado para mover dados entre o Kafka e sistemas externos de forma declarativa — via configuração JSON, não código.

Ele roda como um *cluster de workers* independente da sua aplicação. Você envia uma configuração via REST API e o Connect cuida de:

- gerenciar tasks (unidades de paralelismo dentro de um conector),
- reiniciar tasks falhas automaticamente,
- armazenar offsets de forma separada do consumer group da sua app,
- escalar horizontalmente distribuindo tasks entre workers.

A nota [[03-Dominios/Java/Backend/Kafka/Kafka Concepts/17. Kafka Connect|Kafka Connect (infra)]] cobre a arquitetura interna, workers standalone vs. distributed e o modelo de tasks. Esta nota foca em **quando e como usar Connect do ponto de vista de quem desenvolve serviços**.

---

## Por que importa

Em sistemas distribuídos é comum precisar replicar dados para sistemas de busca, data lakes, caches, bancos analíticos ou sistemas legados. A alternativa ingênua — escrever um consumer dedicado para cada destino — gera código boilerplate, reinventa gerenciamento de offset e falha de formas imprevisíveis.

Connect oferece:

- **Conectores prontos** para centenas de sistemas (Elasticsearch, S3, JDBC, Debezium, HDFS…), mantidos pela comunidade e vendors.
- **Gerenciamento de ciclo de vida** via REST API (start, pause, restart, delete).
- **Dead Letter Queue** integrada para registros com erro de conversão ou entrega.
- **Monitoramento** por JMX/Prometheus sem instrumentação manual.

---

## Como funciona

### Source vs sink connectors

**Source connectors** leem de um sistema externo e publicam em tópico(s) Kafka.
Exemplos canônicos:

- Debezium MySQL/PostgreSQL Source: captura o binlog e emite eventos de mudança de linha.
- File Source: lê arquivos de log ou CSV e publica linha a linha.
- JDBC Source: faz polling de tabelas com coluna de timestamp ou incremento.

**Sink connectors** consomem de tópico(s) Kafka e escrevem em sistema externo.
Exemplos canônicos:

- Elasticsearch Sink: indexa documentos a partir de eventos.
- S3 Sink: grava arquivos Avro/Parquet/JSON no bucket para data lake.
- JDBC Sink: faz upsert em banco relacional a partir de eventos.

Tanto source quanto sink são *stateless do ponto de vista da sua app*: você não escreve um consumer group, não gerencia offsets, não cuida de retentativas — o framework faz tudo isso.

### Quando usar Connect vs produzir/consumir você mesmo

A regra prática é simples:

| Cenário | Ferramenta correta |
|---|---|
| CDC de banco para Kafka | Source connector (Debezium) |
| Kafka → Elasticsearch para busca | Sink connector |
| Kafka → S3 para data lake | Sink connector |
| Kafka → banco de réplica de leitura | Sink connector (JDBC) |
| Processamento com lógica de negócio | Producer/Consumer da app ou Kafka Streams |
| Enriquecimento stateful de eventos | Kafka Streams / Spring Kafka |
| Orquestração de saga | Consumer na app (não Connect) |

A fronteira é: **Connect é movimentação de dados; sua app é transformação com semântica de negócio**. Quando a lógica cabe num SMT simples, Connect é suficiente. Quando precisa de join com banco, decisão condicional complexa ou chamada HTTP, escreva código.

### SMT (Single Message Transforms)

SMTs são transformações aplicadas registro a registro, em pipeline, antes de o conector publicar (source) ou escrever (sink). São configuradas declarativamente como uma lista de transforms na config do conector.

Transformações disponíveis no Connect embutido:

- `ReplaceField` — remove ou renomeia campos,
- `MaskField` — mascara valores sensíveis (ex.: PII),
- `InsertField` — adiciona campo estático ou timestamp,
- `ExtractField` — promove campo aninhado para raiz,
- `Filter` — descarta registros que não atendem predicado,
- `ValueToKey` — define a chave da mensagem a partir de campo do valor.

SMTs encadeiam-se: cada transform recebe o registro do anterior. Confluent documenta que transformações *complexas ou que envolvem múltiplos registros* devem ir para ksqlDB ou Kafka Streams — SMT não é substituto de stream processing.

---

## Na prática

Config JSON de um sink connector Elasticsearch enviada via REST API (`POST /connectors`):

```json
{
  "name": "search-index-sink",
  "config": {
    "connector.class": "io.confluent.connect.elasticsearch.ElasticsearchSinkConnector",
    "tasks.max": "2",
    "topics": "catalog.items.updated",
    "connection.url": "http://elasticsearch:9200",
    "type.name": "_doc",
    "key.ignore": "true",
    "schema.ignore": "true",
    "value.converter": "org.apache.kafka.connect.json.JsonConverter",
    "value.converter.schemas.enable": "false",
    "errors.tolerance": "all",
    "errors.deadletterqueue.topic.name": "catalog.items.updated.dlq",
    "errors.deadletterqueue.context.headers.enable": "true",
    "transforms": "dropInternalFields",
    "transforms.dropInternalFields.type": "org.apache.kafka.connect.transforms.ReplaceField$Value",
    "transforms.dropInternalFields.blacklist": "_internalMeta,_version"
  }
}
```

Pontos de atenção nesta config:

- `tasks.max` controla o paralelismo dentro do conector — não exceda o número de partições do tópico.
- `errors.tolerance: all` + DLQ evita que um único registro malformado trave o conector inteiro.
- `errors.deadletterqueue.context.headers.enable: true` adiciona headers com stack trace e config do conector ao registro da DLQ, facilitando diagnóstico.
- `schema.ignore: true` é útil quando o tópico usa JSON sem Schema Registry; para produção com Avro, use `AvroConverter` e remova essa opção.

Para gerenciar o ciclo de vida:

```bash
# Listar conectores
GET /connectors

# Status de um conector
GET /connectors/search-index-sink/status

# Reiniciar uma task específica
POST /connectors/search-index-sink/tasks/0/restart

# Pausar
PUT /connectors/search-index-sink/pause

# Deletar
DELETE /connectors/search-index-sink
```

---

## Armadilhas

### (1) Reinventar Connect com consumer customizado para sink trivial

O erro mais comum é escrever um `@KafkaListener` em Spring que apenas lê eventos e grava em Elasticsearch ou S3. Para movimentação pura de dados sem lógica de negócio, isso significa:

- Gerenciar offset manualmente (commit no modo errado → duplicatas ou perda).
- Reescrever retry, backoff e DLQ do zero.
- Criar um serviço que precisa de deploy, healthcheck e monitoramento extras.
- Perder a API REST de gerenciamento que Connect já oferece.

Use Connect para isso. Reserve o consumer da app para lógica que só o seu domínio sabe executar.

### (2) Usar Connect para lógica de negócio complexa

O caminho inverso é igualmente problemático. Connect com SMTs encadeados demais vira um pipeline frágil e impossível de testar unitariamente. Se a transformação exige:

- join com outro tópico ou banco,
- decisão condicional baseada em estado acumulado,
- chamada a serviço externo,
- semântica transacional da aplicação,

então a ferramenta certa é Kafka Streams, a API Java da sua app, ou ambos. SMT resolve renomear campo; não resolve calcular desconto com base em histórico.

### (3) Ignorar idempotência e semântica de entrega do sink

Connect garante *at-least-once* por padrão. Isso significa que o sink pode receber o mesmo registro mais de uma vez após falha e reinício. Se o destino não for idempotente por natureza (ex.: Elasticsearch aceita `_id` duplicado como upsert; S3 com chave determinística sobrescreve), você precisa garantir idempotência explicitamente:

- Configure `key.ignore: false` e defina uma chave estável no tópico.
- Para JDBC Sink, use `insert.mode: upsert` com `pk.mode: record_key`.
- Ative `exactly.once.support` (disponível desde Connect 3.3 com KIP-618) apenas se o source connector e o broker suportarem transações — adiciona overhead e complexidade.

Não assuma que "Connect garante exatamente uma entrega" sem verificar a documentação do conector específico.

---

## Em entrevista

### Frase pronta (inglês)

"Kafka Connect is the integration layer of the Kafka ecosystem — it moves data between external systems and Kafka topics declaratively, without requiring custom producer or consumer code. Source connectors ingest data into Kafka, for example using Debezium for CDC from a relational database. Sink connectors export data from Kafka to targets like Elasticsearch, S3, or a JDBC-compatible database. The key design decision is knowing when Connect is the right tool: it excels at data movement, but complex business logic — joins, stateful transformations, domain decisions — belongs in Kafka Streams or the application layer."

### Vocabulário

| Termo PT | Termo EN |
|---|---|
| Conector de origem | Source connector |
| Conector de destino | Sink connector |
| Transformação de mensagem única | Single Message Transform (SMT) |
| Worker distribuído | Distributed worker |
| Captura de dados de mudança | Change Data Capture (CDC) |
| Fila de mensagens mortas | Dead Letter Queue (DLQ) |
| Modo de inserção | Insert mode (upsert / insert) |
| Tolerância a erros | Errors tolerance |

---

## Veja também

- [[03-Dominios/Java/Mensageria/index|Mensageria (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Backend/Kafka/Kafka Concepts/17. Kafka Connect|Kafka Connect (infra)]]
- [[03-Dominios/Java/Mensageria/21 - O padrão Outbox|O padrão Outbox]]
- [[03-Dominios/Java/Mensageria/18 - Kafka Streams pela API Java|Kafka Streams pela API Java]]
- [[03-Dominios/Java/Dicionário de Java|Dicionário de Java]]

---

## Referências

- Confluent Documentation — Kafka Connect Overview: <https://docs.confluent.io/platform/current/connect/>
- Apache Kafka Documentation — Kafka Connect: <https://kafka.apache.org/documentation/#connect>
- Confluent — Single Message Transforms (SMT): <https://docs.confluent.io/platform/current/connect/transforms/overview.html>
- Confluent — Elasticsearch Sink Connector: <https://docs.confluent.io/kafka-connectors/elasticsearch/current/overview.html>
- KIP-618 — Exactly-Once Support for Source Connectors: <https://cwiki.apache.org/confluence/display/KAFKA/KIP-618%3A+Exactly-Once+Support+for+Source+Connectors>
