---
title: "Kafka Streams pela API Java"
created: 2026-06-11
updated: 2026-06-11
type: concept
status: seedling
publish: true
fase: adepto
tags:
  - java
  - mensageria
  - adepto
  - kafka
aliases:
  - "Kafka Streams"
---

# Kafka Streams pela API Java

> **TL;DR** — Kafka Streams é uma biblioteca Java (não um cluster, não um servidor separado) que você embute na sua aplicação para processar dados de tópicos Kafka com operações encadeadas, stateless ou stateful. A topologia é declarada via `StreamsBuilder`; os tipos centrais são `KStream` (fluxo contínuo), `KTable` (snapshot particionado) e `GlobalKTable` (snapshot replicado em todas as instâncias). Para a mecânica de infra (partições, consumer groups, rebalance interno), veja [[03-Dominios/Java/Backend/Kafka/Kafka Concepts/18. Kafka Streams|Kafka Streams (infra)]].

---

## O que é

**Kafka Streams** é uma biblioteca cliente do Apache Kafka para processamento de streams — você adiciona o jar `kafka-streams` ao seu projeto, escreve código Java e a lógica de stream roda **dentro do processo da sua aplicação**, sem cluster externo adicional (Spark, Flink, etc.).

A API central é o **`StreamsBuilder`**: você declara uma topologia de operações sobre tópicos de entrada e a biblioteca cuida do consumo, do processamento e da produção dos resultados.

---

## Por que importa

- **Sem infraestrutura extra**: toda a execução é dentro da JVM; o único requisito externo é o broker Kafka.
- **Processamento com estado**: agregações, janelas temporais e joins — tudo mantido localmente com recuperação automática via changelog topic.
- **Escalabilidade elástica**: adicionar instâncias da aplicação distribui automaticamente as partições entre os processos (Kafka cuida do rebalance).
- **Integração Spring Boot**: `@EnableKafkaStreams` + um bean `KafkaStreamsConfiguration` é suficiente para subir a topologia no contexto do Spring — `StreamsBuilderFactoryBean` gerencia o ciclo de vida.

---

## Como funciona

### KStream, KTable e GlobalKTable

Os três tipos representam formas diferentes de "ver" os dados de um tópico:

| Abstração | O que representa | Particionamento |
|---|---|---|
| **KStream** | Fluxo de registros imutáveis; cada mensagem é um evento isolado | Particionado (cada instância processa um subconjunto) |
| **KTable** | Changelog stream interpretado como tabela: última mensagem por chave "vence" | Particionado (como KStream) |
| **GlobalKTable** | Igual ao KTable, mas **todos os dados são replicados em todas as instâncias** | Global — útil para tabelas de lookup pequenas |

> **KTable vs GlobalKTable**: use `GlobalKTable` quando a tabela é pequena (enriquecimento, lookup de produtos, etc.) e você precisa que qualquer instância responda sem depender de co-partitioning. Use `KTable` para dados grandes que devem ser particionados.

### Topologia e operações

`StreamsBuilder` é o ponto de entrada para declarar a topologia — um DAG (grafo acíclico dirigido) de **Source Processors**, **Stream Processors** e **Sink Processors**.

**Operações stateless** — transformam registro a registro, sem acumular estado:

| Operação | Descrição |
|---|---|
| `map` / `mapValues` | Transforma chave e/ou valor |
| `filter` / `filterNot` | Filtra registros por predicado |
| `flatMap` / `flatMapValues` | Um registro pode gerar zero ou mais registros |
| `peek` | Efeito colateral (log, métrica) sem alterar o registro |
| `to` / `through` | Produz em tópico de saída |

**Operações stateful** — acumulam estado local, precisam de state store:

| Operação | Descrição |
|---|---|
| `groupByKey` + `aggregate` | Agrega registros por chave num store |
| `groupByKey` + `count` | Conta ocorrências por chave |
| `windowedBy` | Aplica janela temporal (tumbling, hopping, session) antes de aggregate/count |
| `join` / `leftJoin` / `outerJoin` | Junta KStream com KStream, KTable ou GlobalKTable |

### State stores

Operações stateful materializam o estado em um **state store local** (por padrão RocksDB, em disco). Cada state store tem um **changelog topic** no Kafka — a cada mudança de estado, um registro é escrito nesse tópico. Em caso de falha ou rebalance, a instância que assume lê o changelog topic e reconstrói o estado local do zero.

Esse mecanismo é o que torna o Kafka Streams tolerante a falhas **sem depender de um banco externo para o estado intermediário**.

---

## Na prática

Configuração Spring Boot com `@EnableKafkaStreams`:

```java
@Configuration
@EnableKafka
@EnableKafkaStreams
public class KafkaStreamsConfig {

    @Bean(name = KafkaStreamsDefaultConfiguration.DEFAULT_STREAMS_CONFIG_BEAN_NAME)
    public KafkaStreamsConfiguration kStreamsConfigs() {
        Map<String, Object> props = new HashMap<>();
        props.put(StreamsConfig.APPLICATION_ID_CONFIG, "pedidos-streams");
        props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
        props.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG,
                Serdes.String().getClass().getName());
        props.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG,
                Serdes.String().getClass().getName());
        return new KafkaStreamsConfiguration(props);
    }
}
```

Topologia: contar pedidos por categoria e publicar o resultado em outro tópico:

```java
@Bean
public KStream<String, String> pedidosPorCategoria(StreamsBuilder builder) {

    // Lê o tópico de entrada
    KStream<String, String> pedidos = builder.stream("pedidos-recebidos");

    // Stateless: filtra apenas pedidos confirmados
    KStream<String, String> confirmados = pedidos
            .filter((categoria, status) -> "CONFIRMADO".equals(status));

    // Stateful: conta por chave (categoria)
    KTable<String, Long> contagem = confirmados
            .groupByKey()
            .count(Materialized.as("store-contagem-por-categoria"));

    // Converte KTable para KStream e publica
    contagem
            .toStream()
            .mapValues(Object::toString)
            .to("pedidos-contagem-por-categoria");

    return pedidos;
}
```

> `APPLICATION_ID_CONFIG` identifica a aplicação no broker — consumer group, changelog topics e state store names derivam desse ID. Dois deploys com o mesmo ID competem pelas mesmas partições (comportamento esperado para escalar horizontalmente).

---

## Armadilhas

### (1) Join sem co-partitioning quebra em runtime

Ao fazer join entre `KStream` e `KTable`, ambos **devem ter o mesmo número de partições e as mesmas chaves mapeadas para as mesmas partições** (co-partitioning). Se os tópicos foram criados com partições diferentes, a topologia lança `TopologyException` na inicialização. `GlobalKTable` contorna essa exigência porque todos os dados ficam em todas as instâncias — mas ao custo de replicar todo o tópico localmente.

### (2) State store sem changelog topic causa perda de estado no rebalance

Por padrão, stores criados via `Materialized.as(...)` são persistidos com changelog habilitado. Se você criar um store manual com `Stores.inMemoryKeyValueStore(...)` e não configurar o changelog, o estado é perdido ao reiniciar ou redistribuir partições. Em produção, jamais desabilite o changelog de state stores que acumulam dados críticos.

### (3) Kafka Streams não é Kafka Connect — são camadas completamente diferentes

**Kafka Streams** é uma biblioteca que você inclui no código da sua aplicação — o processamento roda dentro do processo Java, consome e produz tópicos. **Kafka Connect** é uma camada de infraestrutura separada (cluster de workers) para mover dados entre Kafka e sistemas externos (bancos, S3, Elasticsearch) via plugins de conector. São complementares: Connect integra fontes/destinos externos, Streams processa os dados em trânsito. Confundir os dois leva a soluções mal dimensionadas (rodar lógica de negócio num conector é um antipadrão).

---

## Em entrevista

Frases de partida em inglês:

- *"Kafka Streams is a client library — it runs inside your application process, so there's no additional cluster to manage beyond the Kafka broker itself."*
- *"KTable represents the latest state per key, backed by a local state store and a changelog topic for fault tolerance; GlobalKTable replicates the full table to every application instance, which removes the co-partitioning requirement for joins."*
- *"Stateful operations like aggregations and windowed counts use a local RocksDB store; on failure or rebalance, the store is rebuilt by replaying the changelog topic."*
- *"The key difference between Kafka Streams and Kafka Connect is that Streams is application code doing stream processing, while Connect is infrastructure for moving data between Kafka and external systems."*

**Vocabulário para usar:**

| Termo | Uso |
|---|---|
| **topology** | O grafo de processadores declarado via `StreamsBuilder` |
| **state store** | Armazenamento local (RocksDB/in-memory) que suporta operações stateful |
| **changelog topic** | Tópico Kafka que persiste mutações do state store para recuperação |
| **co-partitioning** | Requisito de que dois streams/tables tenham o mesmo particionamento para joins |
| **windowing** | Segmentar o stream em janelas temporais (tumbling, hopping, session) |
| **materialized view** | KTable ou resultado de aggregate exposto como store consultável |

---

## Veja também

- [[03-Dominios/Java/Mensageria/index|MOC — Galho 14: Mensageria e eventos]]
- [[03-Dominios/Java/index|Trilha Java Senior]]
- [[03-Dominios/Java/Backend/Kafka/Kafka Concepts/18. Kafka Streams|Kafka Streams (infra)]]
- [[03-Dominios/Java/Mensageria/19 - Kafka Connect pela ótica da app|Kafka Connect pela ótica da app]]
- [[03-Dominios/Java/Dicionário de Java|Dicionário de Java]]

---

## Referências

- Spring for Apache Kafka — Apache Kafka Streams Support. Disponível em: <https://docs.spring.io/spring-kafka/reference/streams.html>. Acesso em: 2026-06-11.
- Apache Kafka — Kafka Streams Introduction. Disponível em: <https://kafka.apache.org/documentation/streams/>. Acesso em: 2026-06-11.
