---
title: "Spec — Galho 14 da trilha Java Senior (Mensageria e eventos)"
date: 2026-06-11
author: Josenaldo
status: draft
type: spec
publish: false
---

# Spec — Galho 14 da trilha Java Senior (Mensageria e eventos)

## 1. Contexto e motivação

Este é o **décimo quarto galho** da trilha Java Senior (roadmap em `docs/superpowers/specs/2026-06-02-java-senior-roadmap-design.md`, §5, bloco "Fundamentos enterprise e Spring"). Pressupõe leitura do roadmap, que estabelece topologia flat, esquema de 3 fases, padrões editoriais e política de poda. Os Galhos 1 a 13 já fecharam em `main` — seus artefatos são o **template de padrão e qualidade** deste galho. As dependências diretas são os **Galhos 4 e 8** (roadmap): o Galho 4 é a concorrência (threads de consumo, async, blocking no listener); o Galho 8 é o **container** e o **event bus in-process** (`ApplicationContext` events / `@EventListener` / `@TransactionalEventListener`).

**Galho NOVO/PESQUISA** (como os Galhos 5/7/11 — roadmap: "tronco a podar: nenhum") **+ migração/higiene de um arquivo pequeno** (`Backend/gRPC e Go.md`) **+ coexistência com o cluster Kafka existente**:

- **Parte PESQUISA (a maior):** o galho cobre a **camada de aplicação Java/Spring da mensageria** — Spring Kafka, Spring AMQP/RabbitMQ, Spring Cloud Stream, eventos in-process, padrões de confiabilidade (idempotência, outbox, DLQ, exactly-once), arquitetura event-driven (saga, event sourcing, CQRS), mensageria reativa, observabilidade, e o contraste RPC síncrono (Protobuf/gRPC). Quase tudo nasce de doc oficial via WebFetch (ZERO memória): `docs.spring.io/spring-kafka`, `docs.spring.io/spring-amqp`, `docs.spring.io/spring-cloud-stream`, `kafka.apache.org/documentation`, `docs.confluent.io`, `rabbitmq.com`, `projectreactor.io` (Reactor Kafka), `debezium.io`, `protobuf.dev`, `grpc.io`.

- **Parte MIGRAÇÃO (pequena):** `Backend/gRPC e Go.md` (52 linhas, hoje dump de links + passos de instalação do `protoc` para **Go**) é **migrado e higienizado**: o conteúdo conceitual (Protobuf, gRPC) vira as notas 27/28 deste galho, com ângulo **Java** (não Go); o arquivo original vira um hub apontando pro galho, preservando os links de referência (`protobuf.dev`, `grpc.io`) como apêndice. Confirmar frontmatter/`publish` na execução.

- **Parte COEXISTÊNCIA (decisão do usuário no brainstorming):** o cluster `Backend/Kafka/` existente (19 notas-conceito de **infra** em `Kafka Concepts/` + dumps de referência `Kafka.md`/`Vídeos.md`/`Setting Up Kafka.md` + o artigo de terceiro `Otimizando Kafka consumers.md`) **NÃO é movido nem podado**. Ele permanece como **camada de fundamentos de infra** (broker, partições, offsets, replication, consumer groups, KRaft), e o galho novo **linka de volta** a ele sem re-explicar os internals do Kafka — exatamente como a fronteira-assinatura faz com os galhos. Mexer no cluster existente fica restrito a: (a) atualizar `Backend/Kafka/index.md` e `Backend/index.md` para cross-linkar o galho como "a camada de aplicação Java/Spring"; (b) **nada mais** — o artigo de terceiro e as notas de infra ficam intocados.

**A fronteira-assinatura é MÚLTIPLA (sêxtupla).** A camada de aplicação da mensageria sobe sobre infra e mecanismos que outros galhos (ou o cluster existente) já cobrem. Cada nota linka de volta sem re-explicar:

- **Cluster Kafka existente (a infra):** internals do Kafka (partições, offsets, replication, consumer groups, KRaft, log compaction) → `[[03-Dominios/Java/Backend/Kafka/Kafka Concepts/index|Kafka Concepts]]` e notas específicas (ex.: `[[03-Dominios/Java/Backend/Kafka/Kafka Concepts/9. Producers|Producers]]`, `[[03-Dominios/Java/Backend/Kafka/Kafka Concepts/11. Consumer Groups|Consumer Groups]]`, `[[03-Dominios/Java/Backend/Kafka/Kafka Concepts/12. Consumer Offsets|Consumer Offsets]]`). O galho assume esses fundamentos.
- **Galho 8 (o event bus in-process):** `@EventListener`/`@TransactionalEventListener`/`ApplicationEvent` → `[[03-Dominios/Java/Spring Core e Boot/11 - Eventos do ApplicationContext|Eventos do ApplicationContext]]`. A nota 16 linka de volta sem re-explicar o mecanismo (ângulo: "quando o event bus interno substitui um broker").
- **Galho 10 (transação/persistência):** o padrão Outbox é dual-write + transação → `[[03-Dominios/Java/Persistência de dados/12 - Transações operacionais — @Transactional propagação, isolamento, rollback, readOnly|Transações operacionais]]`. `@TransactionalEventListener` depende do ciclo transacional.
- **Galho 11 (reativo):** mensageria reativa/Reactor Kafka, backpressure no consumo → `[[03-Dominios/Java/Programação Reativa/09 - Backpressure — request(n) e as estratégias BUFFER, DROP, LATEST|Backpressure]]`, `[[03-Dominios/Java/Programação Reativa/index|Programação Reativa]]`. **Paga a dívida** que o Galho 11 deixou explícita (`Reativa/index:35` "Mensageria reativa/Reactor Kafka (Galho 14)").
- **Galho 4 (concorrência):** threads de consumo, `ConcurrentKafkaListenerContainerFactory`, blocking no listener → `[[03-Dominios/Java/Concorrência e paralelismo/index|Concorrência e paralelismo]]`.
- **Galho 13 (testes):** testar mensageria com `@EmbeddedKafka`/Testcontainers/Awaitility → `[[03-Dominios/Java/Testes/11 - Testcontainers — infra real em testes|Testcontainers]]`, `[[03-Dominios/Java/Testes/14 - Testando código assíncrono — Awaitility|Awaitility]]`. O Galho 13 (notas 11/14) **deixou ganchos** "Kafka = Galho 14 (planejado)".

**A tese honesta do galho:** mensageria é **desacoplamento temporal e espacial**, não "velocidade". O `exactly-once` distribuído é majoritariamente um **mito operacional** — o que existe na prática é **at-least-once + consumidor idempotente**. Por isso confiabilidade (idempotência, outbox, DLQ) ocupa metade do bloco Magus, e o contraste **RPC síncrono (gRPC) vs mensageria assíncrona** fecha o galho como decisão de arquitetura, não como hype de tecnologia.

Os Galhos 11 e 13 deixaram **ganchos "Galho 14 (planejado)"** em texto esperando exatamente este galho (dívida reversa — §3.6). Este galho **quita** essa dívida.

## 2. Objetivo

Produzir, em uma sessão de execução dedicada, **29 notas atômicas + 1 MOC do galho + expansão do Dicionário de Java + ativação do MOC central + migração/higiene do `gRPC e Go.md` + cross-link do cluster Kafka existente + quitação da dívida reversa**, em `03-Dominios/Java/Mensageria/` e `03-Dominios/Java/`, todas `publish: true`, em PT-BR, distribuídas em 3 fases (**6 Iniciado + 12 Adepto + 11 Magus**).

Ao terminar o galho, o leitor deve conseguir:

- **Explicar em inglês** o modelo de mensageria (point-to-point vs pub/sub, comando vs evento, desacoplamento temporal), as garantias de entrega (at-most/at-least/exactly-once) e por que o exactly-once distribuído é uma falácia que se resolve com **idempotência**.
- **Produzir e consumir** com Spring Kafka (`KafkaTemplate`/`@KafkaListener`), configurar serializers, ack modes, error handling, retry e DLQ, e saber quando usar RabbitMQ/Spring AMQP em vez de Kafka.
- **Projetar confiabilidade**: por que at-least-once exige consumidor idempotente, o padrão Outbox para o dual-write problem (com CDC/Debezium), saga (coreografia vs orquestração) para transações distribuídas, e versionamento/evolução de eventos.
- **Reconhecer quando NÃO usar mensageria**: quando o event bus in-process do Spring (Galho 8) basta, quando RPC síncrono (gRPC) é a escolha certa, e o custo operacional/cognitivo de um broker.
- **Contrastar gRPC e mensageria**: os 4 tipos de chamada do gRPC, Protobuf como IDL, e o eixo síncrono-RPC vs assíncrono-evento.

A barra é "projetar e justificar uma arquitetura orientada a eventos production-grade em Java/Spring, sabendo escolher broker, garantir confiabilidade e reconhecer quando o desacoplamento não vale o custo" — não "operar um cluster Kafka" (isso é a infra existente) nem "implementar um broker".

## 3. Saídas concretas

### 3.1. Notas (`03-Dominios/Java/Mensageria/`)

Pasta **nova**, flat. 29 notas + 1 MOC (`index.md`, obrigatório pro folder-link do Quartz). Numeração global por galho (não reinicia por fase).

#### Iniciado (6 notas — o modelo, antes da API)

| # | Nota | Escopo nuclear |
|---|------|----------------|
| 01 | O que é mensageria e arquitetura orientada a eventos *(opus, assinatura)* | Síncrono vs assíncrono; desacoplamento temporal e espacial; **comando vs evento** (intenção vs fato); pub/sub como inversão de dependência; por que mensageria ≠ "velocidade". **A nota-assinatura:** o galho é a camada de aplicação sobre a infra existente; linka de volta ao cluster Kafka e aos Galhos 4/8/10/11/13. |
| 02 | Os modelos de mensageria — queue vs topic | Point-to-point (queue, 1 consumidor efetivo) vs publish-subscribe (topic, N consumidores); o broker como intermediário; **JMS** como spec histórica da plataforma (e por que Kafka/Rabbit não são JMS); push vs pull. |
| 03 | Garantias de entrega — e a falácia do exactly-once *(opus)* | At-most-once / at-least-once / exactly-once; por que **exactly-once distribuído end-to-end é um mito** (a entrega é at-least-once; o efeito é exactly-once via idempotência); duplicação e perda; ordering. Liga **nota 20** (idempotência). |
| 04 | O ecossistema de brokers na JVM | Kafka (log distribuído, replay, alta vazão) vs RabbitMQ (broker AMQP, roteamento rico, filas) vs ActiveMQ Artemis (JMS) vs cloud (SQS/SNS, Pub/Sub, EventBridge); critérios de escolha (ordering, retenção, throughput, roteamento, ops). |
| 05 | Kafka numa página para o dev de aplicação | Log distribuído, tópico/partição/offset, consumer group **na visão do dev de app** (não do operador); **linka a infra existente** (`Kafka Concepts`) para os internals; **KRaft (Zookeeper removido no Kafka 4.0 — WebFetch)**. NÃO re-explica partições/replication — aponta. |
| 06 | Spring para mensageria — o panorama | O mapa: Spring Kafka, Spring AMQP, Spring Cloud Stream, Spring Integration; o que cada um resolve e onde se encaixa; quando usar a abstração (Cloud Stream) vs o cliente direto (Spring Kafka). |

#### Adepto (12 notas — Spring Kafka, RabbitMQ e eventos in-process)

| # | Nota | Escopo nuclear |
|---|------|----------------|
| 07 | KafkaTemplate — produzindo mensagens | `KafkaTemplate.send`, `ProducerRecord`, serializers (`JsonSerializer`/String/Avro), **chave → partição** (ordering por chave), send assíncrono + `CompletableFuture`/callback, `ProducerConfig` essencial (`acks`, `linger.ms`, `batch.size`). Liga infra (Producers). |
| 08 | @KafkaListener — consumindo mensagens *(opus)* | `@KafkaListener`, o **listener container**, `ConcurrentKafkaListenerContainerFactory`, **concorrência × nº de partições** (liga **G4**), `ConsumerRecord`, `@Header`/`@Payload`, group id, `auto.offset.reset`. Liga infra (Consumers/Consumer Groups). |
| 09 | (De)serialização de mensagens | `JsonSerializer`/`JsonDeserializer` + type headers/`trusted.packages`, `ErrorHandlingDeserializer` (poison pill), String/ByteArray, ponte pra Avro (nota 14). Armadilha do poison-pill. |
| 10 | Ack modes e commit de offset | `AckMode` (RECORD/BATCH/MANUAL/MANUAL_IMMEDIATE), `enable.auto.commit=false` no Spring, commit síncrono vs assíncrono, at-least-once na prática, `Acknowledgment`. Liga infra (Consumer Offsets). |
| 11 | Tratamento de erro no consumo | `DefaultErrorHandler` (substituiu `SeekToCurrentErrorHandler` no Spring Kafka 2.8+, WebFetch), `BackOff`/`FixedBackOff`/`ExponentialBackOff`, exceções não-retentáveis (`addNotRetryableExceptions`), `CommonErrorHandler`. |
| 12 | Dead Letter Topic — o padrão DLQ | `DeadLetterPublishingRecoverer`, `@RetryableTopic` (retry topics + DLT, WebFetch), naming `*-dlt`, reprocessamento; DLQ no RabbitMQ (dead-letter-exchange) como contraponto. |
| 13 | Transações e exactly-once no Spring Kafka *(opus)* | `KafkaTransactionManager`, `transactional.id`, **read-process-write** atômico, `isolation.level=read_committed`, EOS (exactly-once semantics v2, WebFetch); o limite (só dentro do Kafka — DB externo precisa de outbox). Liga **nota 21**. |
| 14 | Schema e contratos — Avro e Schema Registry | Por que schema (contrato entre producer/consumer desacoplados); **Avro** + Confluent Schema Registry; compatibilidade (backward/forward/full); JSON Schema e Protobuf como alternativas. Liga serialização (**G9**). |
| 15 | Spring AMQP e RabbitMQ | Modelo AMQP (exchange → binding → queue, routing key, tipos direct/topic/fanout/headers); `RabbitTemplate`, `@RabbitListener`, ack/nack/requeue; quorum queues/streams (WebFetch); **Kafka vs RabbitMQ** lado a lado. |
| 16 | Eventos in-process do Spring | `ApplicationEvent`/`@EventListener` **assíncrono** (`@Async`), `@TransactionalEventListener` (`AFTER_COMMIT`); **quando o event bus interno substitui um broker** (monólito, mesmo processo). Liga **G8 nota 11** — não re-explica o mecanismo. |
| 17 | Spring Cloud Stream — a abstração de binders | O modelo funcional (`Supplier`/`Function`/`Consumer` beans; `@StreamListener` **removido**, WebFetch), binders (Kafka/Rabbit), `spring.cloud.stream.bindings`, destination/group; quando a indireção vale (trocar broker sem trocar código) e quando atrapalha. |
| 18 | Kafka Streams pela API Java | `KStream`/`KTable`/`GlobalKTable`, topologia (`StreamsBuilder`), stateless (map/filter) vs stateful (aggregate/join/windowing), state stores; `spring-kafka` + `@EnableKafkaStreams`/`StreamsBuilderFactoryBean`. Liga infra (Kafka Streams, nota 18). |

#### Magus (11 notas — arquitetura, confiabilidade e o contraste RPC)

| # | Nota | Escopo nuclear |
|---|------|----------------|
| 19 | Kafka Connect pela ótica da app | Source/sink connectors, quando integrar via Connect (CDC, sink pra banco/S3) vs produzir/consumir você mesmo; SMTs; Connect como infra, não código. Liga infra (Kafka Connect, nota 17). |
| 20 | Idempotência — o pilar do at-least-once *(opus)* | Por que at-least-once **exige** consumidor idempotente; chaves de deduplicação (idempotency key), tabela de dedup/`INSERT ... ON CONFLICT`, idempotent producer (`enable.idempotence=true`, WebFetch); operações naturalmente idempotentes vs não. Liga **nota 03**. |
| 21 | O padrão Outbox *(opus)* | O **dual-write problem** (escrever no DB e publicar no broker atomicamente é impossível sem 2PC); transactional outbox (gravar evento na mesma transação + relay); **CDC com Debezium** (WebFetch) vs polling publisher. Liga **G10** (transação). |
| 22 | Saga — transações distribuídas por eventos *(opus)* | Por que não há transação ACID entre serviços; saga como sequência de transações locais + eventos; **coreografia** (eventos, descentralizado) vs **orquestração** (coordenador central); compensação (undo semântico). |
| 23 | Event sourcing e CQRS | O evento como **fonte da verdade** (append-only log) vs estado mutável; rebuild por replay; CQRS (separar write model de read models/projections); quando (não) usar — a complexidade raramente paga. |
| 24 | Versionamento e evolução de eventos | Eventos são contratos públicos e duradouros; schema evolution (adicionar campo opcional ✓, remover/renomear ✗), upcasting, tolerância (`trusted.packages`/ignore unknown); compatibilidade fwd/bwd. Liga **nota 14**. |
| 25 | Mensageria reativa — Reactor Kafka | `KafkaReceiver`/`KafkaSender` (reactor-kafka, WebFetch), backpressure no consumo (liga **G11**), Spring Cloud Stream reativo (`Function<Flux,Flux>`); quando o reativo paga no consumo de stream. **Paga a dívida** do `Reativa/index:35`. |
| 26 | Observabilidade em mensageria | **Consumer lag** (a métrica nº 1), tracing distribuído **através do broker** (context propagation via headers, Micrometer/OpenTelemetry, WebFetch), métricas de producer/consumer; por que log não basta num fluxo assíncrono. |
| 27 | Protocol Buffers — a IDL e a serialização binária | `.proto` (proto3), tipos, serialização binária compacta, **schema evolution** (field numbers, reserved); `protoc` + plugin Java; protobuf vs JSON/Avro. **Migra parte do `gRPC e Go.md`** (ângulo Java, não Go). |
| 28 | gRPC em Java — RPC síncrono sobre HTTP/2 *(opus)* | Os **4 tipos de chamada** (unary / server-streaming / client-streaming / bidirectional), HTTP/2, stubs gerados, `grpc-java`/grpc-spring-boot-starter (WebFetch); **gRPC vs REST vs mensageria** (síncrono-RPC vs assíncrono-evento); quando RPC é a escolha certa. **Migra parte do `gRPC e Go.md`**. |
| 29 | Capstone — uma mensagem de ponta a ponta *(opus, checklist + síntese)* | O fluxo completo: comando → transação + **outbox** → relay/Debezium → tópico Kafka → **@KafkaListener** → **consumidor idempotente** → efeito → erro → **DLQ** → **observabilidade** (lag/tracing). **Tabela de decisão** ("preciso de broker? in-process basta? Kafka ou Rabbit? síncrono → gRPC?"); cheatsheet nota→problema; munição de entrevista. |

**Notas opus (9):** 01 (assinatura/modelo), 03 (garantias/exactly-once), 08 (`@KafkaListener` core), 13 (transações/EOS), 20 (idempotência), 21 (outbox), 22 (saga), 28 (gRPC), 29 (capstone). As demais → sonnet. Notas version-specific (05, 07, 08, 11, 12, 13, 14, 15, 17, 18, 20, 21, 25, 26, 27, 28) fazem WebFetch no Step 1 independentemente do modelo.

**Decisões de fronteira (escopo de outro dono — link-back ou texto "(planejado)"):**
- **Internals do Kafka** (partições, offsets, replication, consumer groups, KRaft, log compaction, brokers, Connect/Streams como infra) → **cluster `Backend/Kafka/` existente** (coexistência). **Linkar de volta, nunca re-explicar.** Faces da fronteira-assinatura.
- **Event bus in-process** (mecanismo de `@EventListener`/`ApplicationEvent`) → Galho 8 nota 11. A nota 16 cobre o **ângulo de arquitetura** (quando substitui um broker), não o mecanismo.
- **Transação/persistência** (o `@Transactional` que o outbox usa) → Galho 10. A nota 21 cobre o **padrão**, não o mecanismo do proxy AOP.
- **Reativo** (Reactor, Mono/Flux, backpressure) → Galho 11. A nota 25 cobre **Reactor Kafka**, não o Reactor.
- **Testar mensageria** (`@EmbeddedKafka`/Testcontainers Kafka/Awaitility) → Galho 13. Mencionar e linkar; profundidade de teste é lá.
- **Microservices / Spring Cloud (service discovery, gateway, resiliência distribuída)** → Galho 16 (planejado). A saga/coreografia cobre o **padrão de dados**, não a plataforma de microservices.
- **Cloud-native / Kubernetes / deploy de broker / produção** → Galho 17 (planejado).
- **Spring Integration aprofundado (EIP completo)** → mencionado no panorama (nota 06); sem nota dedicada (YAGNI — escopo de entrevista é Kafka/Rabbit/eventos).

### 3.2. MOC do galho

`03-Dominios/Java/Mensageria/index.md`:
- `type: moc`, `status: growing`
- Frontmatter padrão (`title: "Mensageria e eventos"`, tags `java`/`mensageria`/`moc`, aliases `["Mensageria e eventos", "Mensageria", "Messaging", "Event-Driven", "Galho 14 - Mensageria"]`)
- TL;DR callout (galho cobre a camada de aplicação Java/Spring da mensageria: modelo e garantias de entrega, Spring Kafka e RabbitMQ, eventos in-process, padrões de confiabilidade — idempotência/outbox/DLQ/exactly-once —, arquitetura event-driven — saga/event sourcing/CQRS —, mensageria reativa, observabilidade e o contraste com gRPC; **29 notas em 3 fases**)
- "Sobre este galho" + audiência primária/secundária + nota de que é galho **NOVO/PESQUISA** que **coexiste** com o cluster Kafka de infra existente (linka, não move) e **migra** o `gRPC e Go.md`; a **tese honesta** (mensageria = desacoplamento, não velocidade; exactly-once distribuído é mito → idempotência); a fronteira-assinatura sêxtupla
- Conteúdo agrupado em 3 H2 (`## Iniciado` / `## Adepto` / `## Magus`) com wikilinks pras 29 notas (uma linha descritiva cada)
- **Rotas alternativas (5):**
  - **Completa** — 01 → 29 em ordem
  - **Entrevista internacional** — 01 → 03 → 07 → 08 → 12 → 20 → 21 → 22 → 28 → 29 (modelo, garantias, produzir/consumir, DLQ, idempotência, outbox, saga, gRPC, capstone)
  - **Spring Kafka operacional** — 05 → 07 → 08 → 09 → 10 → 11 → 12 → 13 (Kafka, produção, consumo, serialização, ack, erro, DLQ, transação)
  - **Confiabilidade e arquitetura event-driven** — 03 → 20 → 21 → 22 → 23 → 24 (garantias, idempotência, outbox, saga, event sourcing/CQRS, versionamento)
  - **Síncrono vs assíncrono (a ponte com gRPC)** — 01 → 02 → 27 → 28 → 29 (modelo, queue vs topic, Protobuf, gRPC, o mapa de decisão)
- "Veja também": MOC central `[[03-Dominios/Java/index|Trilha Java]]`, **cluster Kafka existente** `[[03-Dominios/Java/Backend/Kafka/index|Kafka]]` (a infra), **Galho 8** (o event bus in-process), **Galho 4** (concorrência/threads de consumo), **Galho 11** (mensageria reativa), **Galho 13** (testar mensageria), Dicionário de Java; Galhos 16/17 como texto "(planejado)" sem wikilink
- Dataview "Todas as notas do galho"

### 3.3. Dicionário de Java (EXPANSÃO — não recriar)

`03-Dominios/Java/Dicionário de Java.md` já existe (**403 verbetes** após o Galho 13, `type: glossary`, `updated: 2026-06-11`, seções alfabéticas únicas `## A`…`## Z` com verbetes `### `). Este galho **expande** o arquivo existente inserindo os verbetes **em ordem alfabética case-insensitive (sem acento, ignorando `@`)** nas seções de letra apropriadas. **Nunca recriar o arquivo nem reordenar verbetes existentes.** Manter `updated: 2026-06-11`.

Verbetes a inserir (~35, conferir dups antes):

`@KafkaListener`, `@RabbitListener`, `@RetryableTopic`, `ack mode (Spring Kafka)`, `AMQP`, `at-least-once`, `at-most-once`, `Avro`, `broker (mensageria)`, `CDC (Change Data Capture)`, `coreografia vs orquestração`, `comando vs evento`, `consumer lag`, `CQRS`, `dead letter queue (DLQ)`, `Debezium`, `DefaultErrorHandler`, `event sourcing`, `event-driven architecture`, `exactly-once semantics (EOS)`, `gRPC`, `idempotência (consumidor idempotente)`, `JMS`, `KafkaTemplate`, `KRaft`, `outbox pattern`, `point-to-point (queue)`, `Protocol Buffers (protobuf)`, `publish-subscribe (topic)`, `RabbitMQ`, `Reactor Kafka`, `saga`, `schema registry`, `Spring AMQP`, `Spring Cloud Stream`, `Spring Kafka`.

Cada verbete: definição curta (1-3 linhas) em PT-BR + `Veja também:` apontando pra(s) nota(s) canônica(s) do galho. **Conferir com grep os verbetes já existentes** para **não duplicar** — possíveis colisões: `@EventListener`/`@TransactionalEventListener`/`ApplicationEvent`/`evento` (Galho 8); `backpressure` (Galho 11); `Kafka Streams`/`Kafka Connect`/`partition`/`offset`/`consumer group` (se já existirem do material de infra, embora o Dicionário seja da trilha nova — conferir); `Netty` (Galho 11). Quando um termo tocar um já existente, **linkar entre si** em vez de criar segundo verbete. **Conferir 1:1** que os headings batem com âncoras `[[Dicionário de Java#...]]` usadas nas notas (extrair via grep e conferir; se as notas linkarem o Dicionário sem âncora, basta inserção alfabética).

### 3.4. MOC central (ativação do Galho 14)

`03-Dominios/Java/index.md` já existe. Task **mínima**: trocar a linha do Galho 14 (atualmente `14. Mensageria e eventos *(planejado)* — ...`) por wikilink ativo no padrão dos galhos fechados:

```markdown
14. [[03-Dominios/Java/Mensageria/index|Mensageria e eventos]] — o modelo de mensageria e as garantias de entrega, Spring Kafka e RabbitMQ, eventos in-process, padrões de confiabilidade (idempotência, outbox, DLQ, exactly-once), arquitetura event-driven (saga, event sourcing, CQRS), mensageria reativa, observabilidade e o contraste com gRPC
```

Atualizar `updated` para `2026-06-11`. Não mexer no resto do MOC central. **Confirmar o número da linha na execução** (lendo o arquivo primeiro).

### 3.5. Migração/higiene do `Backend/gRPC e Go.md`

O arquivo (52 linhas, hoje dump de links + instalação Go-cêntrica do `protoc`) **não é tronco de poda integral** — é uma **migração**: seu conteúdo conceitual (Protobuf, gRPC) vira as notas 27/28 com **ângulo Java**. O arquivo original vira um **hub de referência**:
- frontmatter (criar se não houver; `publish` conforme o atual — confirmar na execução; provavelmente `publish: true` como o resto do `Backend/`);
- H1 `# gRPC e Protocol Buffers`;
- 1-2 frases de intro neutras;
- callout `[!nota] Migrado para galho próprio` apontando pras notas 27 (Protobuf) e 28 (gRPC em Java) + o MOC do galho;
- **apêndice de referência** preservando os links úteis (`protobuf.dev`, `grpc.io/docs`, repositórios) e, se quiser, a seção de instalação Go como "referência (toolchain Go)" claramente rotulada — ou removê-la (é Go, fora do escopo Java). **Decisão default: preservar os links de referência, remover os passos de instalação Go** (são específicos de Go e o galho é Java; o `protoc`+plugin Java fica na nota 27). Confirmar na execução.

**NÃO TOCAR no cluster Kafka** (`Backend/Kafka/**`) além do cross-link do índice (§3.6); **NÃO TOCAR** em `Backend/Spring Boot.md`, `Spring Data JPA.md`, `Spring Security.md`, `Testes em Java.md`.

### 3.6. Dívida reversa e cross-links

Pré-flight localizou os pontos a quitar/cross-linkar após as notas existirem:

| # | Arquivo:linha | Texto atual (resumo) | Ação |
|---|---|---|---|
| 1 | `index.md` (MOC central, linha do galho 14) | `14. Mensageria e eventos *(planejado)*` | ativação (§3.4) |
| 2 | `Programação Reativa/index.md:35` | "Mensageria reativa/Reactor Kafka (Galho 14) ... planejados" | **nota 25** (mensageria reativa) — quita a parte do Galho 14; mantém 16/17 como texto |
| 3 | `Backend/Kafka/index.md` | MOC do cluster de infra | adicionar em "Veja também" wikilink pro **MOC do galho** ("a camada de aplicação Java/Spring") |
| 4 | `Backend/index.md` | MOC do Backend (lista `[[gRPC e Go]]`, `[[Spring Boot]]` etc.) | adicionar referência ao **MOC do galho** Mensageria; o item `[[gRPC e Go]]` continua válido (o arquivo vira hub) |
| 5 | `Testes/11 - Testcontainers:?` | "módulo Kafka ... Galho 14 (planejado)" (se houver gancho inline) | **nota 05 ou 08** (Kafka/consumo) se o gancho existir; confirmar via grep |
| 6 | `Testes/14 - Testando código assíncrono — Awaitility:?` | "consumir evento Kafka ... Galho 14" (se houver gancho inline) | **nota 08** (@KafkaListener) se o gancho existir; confirmar via grep |
| 7 | `Spring Core e Boot/11 - Eventos do ApplicationContext:?` | possível gancho "mensageria/broker = Galho 14" (se houver) | **nota 16** (eventos in-process) se o gancho existir; confirmar via grep |

**NÃO quitar (permanece "(planejado)"):**
- **Horizonte-lists de uma linha** nos índices dos galhos (ex.: `Spring Core e Boot/index.md`, `Web e APIs REST/index.md`, `Persistência de dados/index.md`, `Programação Reativa/index.md`, `Segurança/index.md`, `Testes/index.md`) que listam "14 (Mensageria), 16, 17 — planejados" — padrão estabelecido; 16/17 permanecem "(planejado)", e o 14 também se aparecer nessas listas-resumo de uma linha (não convém caçar todas; só os ganchos inline acionáveis acima).

Em todos os pontos, manter como texto "(planejado)" qualquer referência a galhos **ainda** inexistentes (15/16/17/18). **Confirmar os números de linha na execução** via grep `"Galho 14"`/`"Mensageria"`/`"planejado"` (podem ter deslocado ou não existir).

## 4. Convenções por nota

Herda §7 do roadmap e §4 dos specs dos Galhos 11/13 (galhos de pesquisa). Reforços específicos:

### 4.1. Frontmatter

```yaml
---
title: "<título>"
created: 2026-06-11
updated: 2026-06-11
type: concept
status: seedling
publish: true
fase: iniciado | adepto | magus
tags:
  - java
  - mensageria
  - <fase>
  - <tags específicas: kafka, spring-kafka, rabbitmq, amqp, eventos, idempotencia, outbox, saga, event-sourcing, cqrs, reativa, grpc, protobuf, observabilidade, ...>
aliases:
  - <aliases opcionais>
---
```

H1 `# Título` após o frontmatter (padrão dos galhos publicados).

### 4.2. Estrutura H2 obrigatória

- `> [!abstract] TL;DR` (callout, NÃO H2) — 2-4 linhas: conceito + regra prática + por que importa
- `## O que é` / `## Por que importa` / `## Como funciona` (≥3 subseções H3 em notas Adepto/Magus)
- `## Na prática` — exemplos compiláveis; framing **neutro** (`Order`/`Customer`/`Payment`/`OrderEvent`/`OrderService`/`OrderPlacedEvent`); "padrão observado em sistemas event-driven"; NUNCA `Patient`/`MedEspecialista`/"da minha experiência"/"quando comecei o projeto"/"incidente no Kafka"
- `## Armadilhas` — **≥2** (Iniciado) / **≥3** (Adepto/Magus), cada uma com `### (N) Título` (H3 numerado, NÃO callout `[!warning]`) + descrição + exemplo curto + fix em 1 linha
- `## Em entrevista` — subheading `### Frase pronta (inglês)` com **3+ sentenças** (trade-off + decisão + caveat) + subheading `### Vocabulário` com tabela `| Termo PT | Termo EN |` de **6+ termos**
- `## Veja também` — wikilinks **SEM backticks**, **SEM âncoras same-file**; sempre inclui notas relacionadas do galho + `[[03-Dominios/Java/Mensageria/index|MOC do galho]]` + `[[03-Dominios/Java/index|Trilha Java]]` + (quando aplicável) a nota da camada/galho dono (cluster Kafka de infra, G8 eventos, G10 transação, G11 reativo, G4 concorrência, G13 testes) + verbetes do Dicionário
- `## Referências` — docs oficiais (docs.spring.io spring-kafka/spring-amqp/spring-cloud-stream, kafka.apache.org, docs.confluent.io, rabbitmq.com, projectreactor.io reactor-kafka, debezium.io, protobuf.dev, grpc.io)

### 4.3. Restrições absolutas

1. **Fronteira-assinatura (linkar de volta, não re-explicar)** — internals do Kafka → cluster de infra existente; event bus in-process → G8; transação → G10; reativo → G11; concorrência → G4; testes → G13. Galhos 15/16/17/18 = texto "(planejado)", sem wikilink. **Nunca re-explicar partições/offsets/replication/consumer-group internals** — apontar pra `Kafka Concepts`.
2. **Sem fabricação** de experiência pessoal. Exemplos neutros (`Order`, `Customer`, `Payment`, `Shipment`, `OrderPlacedEvent`) — NUNCA `Patient`/`Maria`/`josenaldo`/`MedEspecialista`/1ª pessoa/"quando comecei o projeto"/"incidente de produção". O artigo de terceiro `Otimizando Kafka consumers.md` é material **de outro autor** — **não copiar** nem absorver (coexistência: fica intocado). **Zero estatística de adoção inventada** (ex.: "X% das empresas usam Kafka"); números só com fonte verificável.
3. **Sem invenção** de APIs/comportamentos/versões. WebFetch obrigatório no Step 1 das notas version-specific e pra **toda afirmação version-specific**. Pontos minados a verificar via WebFetch: **KRaft / remoção do Zookeeper no Kafka 4.0**; versão atual do **Spring Kafka** (3.x) e Spring Boot baseline; **`DefaultErrorHandler` substituiu `SeekToCurrentErrorHandler` (Spring Kafka 2.8+)**; **`@RetryableTopic`**; **`@StreamListener` removido** (Spring Cloud Stream modelo funcional `Supplier`/`Function`/`Consumer`); EOS v2 (exactly-once semantics); `enable.idempotence` default; Spring AMQP (quorum queues, streams no RabbitMQ); **Reactor Kafka** (`KafkaReceiver`/`KafkaSender`); Debezium atual; Avro/Confluent Schema Registry; proto3; `grpc-java`/grpc-spring-boot-starter atual; context propagation/tracing (Micrometer Observation). Spring Boot 3.x baseline (`jakarta.*`, Java 17), citando Boot 4.x como "mais recente" quando relevante. Fonte: docs oficiais. Nada "de memória".
4. **Code samples compiláveis** — Java moderno (records pra eventos/DTO, `var`, text blocks); imports corretos (`org.springframework.kafka.*`, `org.springframework.amqp.*`, `org.apache.kafka.clients.*`, `io.grpc.*`); fences corretas (`java`/`xml`/`yaml`/`properties`/`protobuf`/`bash`/`json`/`text`). Snippets de `.proto` com fence ` ```protobuf ` (ou ` ```proto `).
5. **Comparações justas** — Kafka vs RabbitMQ, queue vs topic, síncrono-RPC vs assíncrono-evento, broker vs event bus in-process, coreografia vs orquestração, at-least-once vs exactly-once, polling publisher vs CDC: sempre "quando X" E "quando Y". O capstone (29) é o ápice (o mapa de decisão, sem dogma de tecnologia).
6. **Wikilinks sem backticks** em "Veja também"; MOC do galho + MOC central obrigatórios. **Não linkar galhos inexistentes** (15/16/17/18) — texto "(planejado)". Os wikilinks pro cluster Kafka de infra usam o **path completo** (`[[03-Dominios/Java/Backend/Kafka/...]]`) — conferir que resolvem (a pasta de infra tem `index.md`).
7. **Code fences corretos:** ` ```java ` pra código, ` ```xml `/` ```yaml `/` ```properties ` pra config/pom, ` ```protobuf ` pra `.proto`, ` ```bash ` pra CLI, ` ```json ` pra payloads, ` ```text ` pra diagramas. Sempre fechadas.
8. **`fase:` no frontmatter + na tag** — obrigatório.
9. **Higiene de commits** — sem `Co-Authored-By: Claude`, sem `--no-verify`, `git add <path>` nominal (nunca `-A` — bot de backup Obsidian Git roda em timer), 1 commit por nota, controlador commita (subagents write-only). Guardar contra `.git/index.lock`.
10. **Tom pedagógico graduado** — Iniciado assume Galhos 1-2 (linguagem) + o cluster de infra como fundamento; Adepto assume Galho 8 (container/eventos); Magus assume o stack inteiro (8-13) + a tese honesta (mensageria é trade-off, não default).

## 5. Conteúdo por nota (síntese)

Esboço do recorte. Notas de pesquisa fundadas em doc oficial via WebFetch; o cluster de infra existente é **fonte de fronteira** (linkar, não copiar). Fontes-base: `docs.spring.io/spring-kafka/reference/`, `docs.spring.io/spring-amqp/reference/`, `docs.spring.io/spring-cloud-stream/reference/`, `kafka.apache.org/documentation/`, `docs.confluent.io/platform/current/`, `rabbitmq.com/docs`, `projectreactor.io/docs/kafka/`, `debezium.io/documentation/`, `protobuf.dev/`, `grpc.io/docs/`.

- **01 — O que é mensageria e event-driven (pesquisa, opus, assinatura).** Sync vs async; desacoplamento temporal/espacial; comando vs evento; pub/sub; a assinatura (camada de app sobre a infra existente). Armadilhas: "mensageria = mais rápido"; acoplar consumer ao schema interno do producer. Fontes: docs.spring.io, kafka.apache.org.
- **02 — Queue vs topic (pesquisa).** Point-to-point vs pub/sub; broker; JMS como spec; push vs pull. Armadilhas: usar topic onde queria competing consumers; assumir ordering global. Fontes: rabbitmq.com, kafka.apache.org.
- **03 — Garantias de entrega (pesquisa, opus).** At-most/least/exactly; a falácia do exactly-once distribuído; dup/perda; ordering. Armadilhas: "configurei exactly-once, logo não preciso de idempotência"; achar que retry não duplica. Fontes: kafka.apache.org, confluent.io.
- **04 — Ecossistema de brokers (pesquisa).** Kafka vs Rabbit vs Artemis vs cloud; critérios. Armadilhas: escolher por hype; Kafka pra fila de tarefas com baixo volume. Fontes: kafka.apache.org, rabbitmq.com, docs AWS (texto).
- **05 — Kafka numa página (pesquisa + infra-link).** Log/tópico/partição/offset/group na visão de app; **KRaft/Zookeeper removido no Kafka 4.0 (WebFetch)**; linka `Kafka Concepts`. Armadilhas: mais consumers que partições (ociosos); re-explicar internals (não — apontar). Fontes: kafka.apache.org + cluster de infra.
- **06 — Spring para mensageria (pesquisa).** Spring Kafka/AMQP/Cloud Stream/Integration; o que cada um resolve. Armadilhas: Cloud Stream quando bastava o cliente; misturar abstrações. Fontes: docs.spring.io.
- **07 — KafkaTemplate (pesquisa).** send/ProducerRecord/serializers/chave→partição/async/acks/linger. Armadilhas: `acks=1` esperando durabilidade; ignorar o future (perda silenciosa); chave nula e esperar ordering. Fontes: docs.spring.io/spring-kafka, kafka.apache.org (producer configs).
- **08 — @KafkaListener (pesquisa, opus).** listener container/ConcurrentKafkaListenerContainerFactory/concorrência×partições (liga G4)/group/auto.offset.reset. Armadilhas: concorrência > partições; blocking longo no listener (rebalance); `latest` perdendo mensagens no 1º deploy. Fontes: docs.spring.io/spring-kafka.
- **09 — (De)serialização (pesquisa).** JsonSerializer + type headers/trusted.packages; ErrorHandlingDeserializer (poison pill). Armadilhas: poison pill parando o consumer; `trusted.packages=*`; acoplar ao FQCN do producer. Fontes: docs.spring.io/spring-kafka.
- **10 — Ack modes e offset (pesquisa).** AckMode/enable.auto.commit=false/commit sync vs async/Acknowledgment. Armadilhas: auto-commit + processamento async (perde at-least-once); commit antes de processar. Fontes: docs.spring.io/spring-kafka, kafka.apache.org (consumer offsets).
- **11 — Erro no consumo (pesquisa).** DefaultErrorHandler (ex-SeekToCurrent, 2.8+, WebFetch)/BackOff/não-retentáveis. Armadilhas: retry infinito bloqueando a partição; retentar erro de desserialização (não-retentável). Fontes: docs.spring.io/spring-kafka.
- **12 — Dead Letter Topic (pesquisa).** DeadLetterPublishingRecoverer/@RetryableTopic/DLT naming; DLX no Rabbit. Armadilhas: DLQ sem alarme (mensagens morrem em silêncio); reprocessar DLQ sem corrigir a causa. Fontes: docs.spring.io/spring-kafka, rabbitmq.com.
- **13 — Transações/EOS (pesquisa, opus).** KafkaTransactionManager/transactional.id/read-process-write/read_committed/EOS v2 (WebFetch); o limite (DB externo → outbox). Armadilhas: achar que a transação Kafka cobre o DB; transactional.id reusado. Fontes: docs.spring.io/spring-kafka, kafka.apache.org (EOS).
- **14 — Schema e Avro (pesquisa).** Por que schema; Avro + Schema Registry; compat backward/forward/full; JSON Schema/Protobuf. Liga G9. Armadilhas: mudança incompatível quebrando consumers; sem registry (contrato implícito). Fontes: docs.confluent.io (schema registry), avro.apache.org.
- **15 — Spring AMQP/RabbitMQ (pesquisa).** AMQP (exchange/binding/queue/routing, tipos); RabbitTemplate/@RabbitListener/ack-nack-requeue; quorum queues/streams (WebFetch); Kafka vs Rabbit. Armadilhas: requeue infinito (poison); fanout achando que filtra. Fontes: docs.spring.io/spring-amqp, rabbitmq.com.
- **16 — Eventos in-process (pesquisa + G8-link).** @EventListener async/@Async/@TransactionalEventListener (AFTER_COMMIT); quando substitui broker. Liga **G8 nota 11**. Armadilhas: @EventListener síncrono achando que é async; evento publicado mas commit falha (use AFTER_COMMIT). Fontes: docs.spring.io (core/events).
- **17 — Spring Cloud Stream (pesquisa).** Modelo funcional (Supplier/Function/Consumer; @StreamListener removido, WebFetch)/binders/bindings/destination-group. Armadilhas: indireção sem ganho; binder errado em produção. Fontes: docs.spring.io/spring-cloud-stream.
- **18 — Kafka Streams (pesquisa).** KStream/KTable/GlobalKTable/topologia/stateless vs stateful/state stores; @EnableKafkaStreams. Liga infra (Kafka Streams). Armadilhas: join sem co-partitioning; state store sem changelog (perda no rebalance). Fontes: kafka.apache.org (streams), docs.spring.io/spring-kafka.
- **19 — Kafka Connect (pesquisa).** Source/sink/quando usar vs produzir; SMT; Connect = infra. Liga infra (Connect). Armadilhas: reinventar Connect na mão; Connect pra lógica de negócio. Fontes: docs.confluent.io (connect), kafka.apache.org.
- **20 — Idempotência (pesquisa, opus).** At-least-once exige idempotência; dedup key/tabela/ON CONFLICT; idempotent producer (enable.idempotence, WebFetch). Liga nota 03. Armadilhas: consumer não-idempotente em at-least-once (efeito duplicado); dedup sem TTL (cresce infinito). Fontes: kafka.apache.org, confluent.io.
- **21 — Outbox (pesquisa, opus).** Dual-write problem; transactional outbox + relay; CDC/Debezium (WebFetch) vs polling. Liga **G10**. Armadilhas: publicar no broker dentro do `@Transactional` (dual-write); outbox sem limpeza. Fontes: debezium.io, microservices.io (texto).
- **22 — Saga (pesquisa, opus).** Sem ACID distribuído; transações locais + eventos; coreografia vs orquestração; compensação. Armadilhas: saga sem compensação (estado inconsistente); coreografia complexa virando spaghetti de eventos. Fontes: microservices.io (texto), docs.spring.io (texto).
- **23 — Event sourcing e CQRS (pesquisa).** Evento como fonte da verdade; replay; CQRS write/read models; quando não usar. Armadilhas: event sourcing por moda (complexidade); CQRS sem necessidade de read model. Fontes: martinfowler.com (texto), docs gerais.
- **24 — Versionamento de eventos (pesquisa).** Evento é contrato durável; schema evolution (add opcional ✓, remove ✗); upcasting; compat fwd/bwd. Liga nota 14. Armadilhas: renomear campo (quebra); remover sem deprecação. Fontes: confluent.io (schema evolution), avro.apache.org.
- **25 — Mensageria reativa (pesquisa).** Reactor Kafka (KafkaReceiver/KafkaSender, WebFetch)/backpressure no consumo (liga **G11**)/Cloud Stream reativo. **Paga a dívida Reativa/index:35.** Armadilhas: bloquear no pipeline reativo; reativo no consumo sem necessidade. Fontes: projectreactor.io/docs/kafka.
- **26 — Observabilidade (pesquisa).** Consumer lag; tracing através do broker (context propagation via headers, Micrometer Observation/OpenTelemetry, WebFetch); métricas. Armadilhas: só logar (sem correlação no fluxo async); ignorar lag até a fila estourar. Fontes: docs.spring.io (observability), micrometer.io.
- **27 — Protocol Buffers (migração + pesquisa).** `.proto` proto3/tipos/serialização binária/schema evolution (field numbers/reserved)/`protoc`+plugin Java; protobuf vs JSON/Avro. **Migra parte do gRPC e Go.md (ângulo Java).** Armadilhas: reusar field number (corrompe); mudar tipo de um campo. Fontes: protobuf.dev.
- **28 — gRPC em Java (migração + pesquisa, opus).** 4 tipos de chamada/HTTP/2/stubs/grpc-java/grpc-spring-boot-starter (WebFetch); gRPC vs REST vs mensageria; quando RPC. **Migra parte do gRPC e Go.md.** Armadilhas: gRPC onde mensageria desacoplaria melhor; streaming sem necessidade. Fontes: grpc.io, github.com/grpc/grpc-java.
- **29 — Capstone (pesquisa, opus, checklist).** Fluxo ponta a ponta (comando→outbox→relay→tópico→listener→idempotente→DLQ→observabilidade); **tabela de decisão** (broker? in-process? Kafka/Rabbit? síncrono→gRPC?); cheatsheet nota→problema; munição de entrevista. Armadilhas de raciocínio: "evento pra tudo"; "exactly-once resolve"; "broker é default". Fontes: docs.spring.io, kafka.apache.org.

## 6. Pré-flight: verificações feitas

Executado nesta fase de brainstorming (2026-06-11); itens version-specific re-confirmados na execução de cada nota via WebFetch:

1. **Cluster Kafka existente mapeado** — `Backend/Kafka/`: `index.md` (MOC, `publish: true`), `Kafka.md` (dump de links/recursos), `Vídeos.md`, `Setting Up Kafka.md` (guia de setup), `Otimizando Kafka consumers.md` (**reprodução de artigo de Álvaro Bacelar/Medium — material de terceiro**, com imagem `Untitled 4.png`), e `Kafka Concepts/` com 19 notas-conceito numeradas (1-19: Introdução, Cluster, Broker, Zookeeper, KRaft, Topics, Partitions, Replication, Producers, Consumers, Consumer Groups, Offsets, Keys, Messages, Partições/Replicação, Log Compaction, Connect, Streams, Segurança) — infra/conceito, ~40-64 linhas cada, `publish: true`, na topologia ANTIGA `Backend/`. **Decisão do usuário: COEXISTÊNCIA** — não mover, não podar; linkar como fundamentos de infra.
2. **`Backend/gRPC e Go.md` mapeado** — 52 linhas, dump de links (protobuf.dev, grpc.io) + instalação Go-cêntrica do `protoc`. **Decisão do usuário: gRPC entra como bloco próprio** (notas 27/28, ângulo Java); arquivo vira hub (§3.5).
3. **Fronteira-assinatura confirmada** — cluster Kafka de infra (internals), Galho 8 (event bus in-process, nota 11), Galho 10 (transação/outbox), Galho 11 (reativo/backpressure), Galho 4 (concorrência), Galho 13 (testes/Testcontainers/Awaitility) existem em `main`. Os Galhos 11/13 **deixaram ganchos** "Galho 14 (planejado)".
4. **Dívida reversa localizada** — `Reativa/index:35` (Reactor Kafka Galho 14 → nota 25); cross-link de `Backend/Kafka/index.md` + `Backend/index.md` pro MOC do galho; possíveis ganchos inline em `Testes/11`, `Testes/14`, `Spring Core/11` (confirmar via grep na execução). MOC central: linha do galho 14. **NÃO quitar**: horizonte-lists de uma linha.
5. **Dicionário** — **403 verbetes** após o Galho 13; seções alfabéticas únicas `## A`…`## Z`; verbetes `### `; `updated: 2026-06-11`. Possíveis dups: `@EventListener`/`@TransactionalEventListener`/`ApplicationEvent`/`evento` (G8), `backpressure` (G11). Conferir e linkar, nunca duplicar. Expansão alfabética (~35), nunca recriar/reordenar.
6. **MOC central** — `03-Dominios/Java/index.md` tem a linha do Galho 14 (`*(planejado)*`); galhos ativos usam `N. [[path/index|Title]] — summary`; `updated: 2026-06-11`. Confirmar o número da linha na execução.
7. **Troncos/arquivos intocáveis** — `Backend/Spring Boot.md`, `Backend/Spring Data JPA.md` (hub G10), `Backend/Spring Security.md` (hub G12), `Backend/Testes em Java.md` (hub G13), e **todo o `Backend/Kafka/**`** (coexistência). Só toca `Backend/gRPC e Go.md` (migração) + cross-link dos índices `Backend/index.md` e `Backend/Kafka/index.md`. Pasta `Mensageria/` ainda **não existe**.
8. **Versões a cravar via WebFetch na execução** — **Zookeeper removido no Kafka 4.0 / KRaft only**; Spring Kafka 3.x atual; **`DefaultErrorHandler` (ex-`SeekToCurrentErrorHandler`, 2.8+)**; **`@RetryableTopic`**; EOS v2; `enable.idempotence` default true (producers modernos); **`@StreamListener` removido** (Cloud Stream funcional); Spring AMQP (quorum queues/streams); Reactor Kafka (`KafkaReceiver`/`KafkaSender`); Debezium; Avro/Confluent Schema Registry; proto3; grpc-java/grpc-spring-boot-starter; Micrometer Observation (tracing). Baseline Spring Boot 3.x (`jakarta.*`, Java 17), citando Boot 4.x como "mais recente". Fonte: docs oficiais.

Nenhum número de adoção é inventado. Quando faltar fato verificável, **PERGUNTAR** antes de escrever.

## 7. Critérios de aceitação do galho

Além dos critérios gerais (§10 do roadmap):

1. 29 notas em `03-Dominios/Java/Mensageria/`, frontmatter completo com `fase:`, `publish: true`, distribuídas 6/12/11.
2. MOC do galho com 3 subseções de fase + 5 rotas alternativas + dataview + folder-link resolve (`index.md` presente).
3. Dicionário de Java **expandido** (não recriado) com ~35 verbetes; verbetes dos Galhos 1-13 intactos; `updated: 2026-06-11`; dups conferidos e linkados (não duplicar `@EventListener`/`@TransactionalEventListener`/`backpressure` se vierem dos Galhos 8/11).
4. MOC central `Java/index.md` com Galho 14 ativado (linha vira wikilink); resto intacto.
5. **Migração do gRPC executada**: `Backend/gRPC e Go.md` vira hub apontando pras notas 27/28 (referências preservadas, instalação Go removida ou rotulada). **Cluster Kafka intocado** (só cross-link do índice). **Outros troncos intactos**.
6. **Dívida reversa quitada**: `Reativa/index:35`→nota25; `Backend/Kafka/index` + `Backend/index` cross-linkam o MOC do galho; ganchos inline em `Testes/11`/`Testes/14`/`Spring Core/11` quitados **se existirem** (grep); galhos ainda inexistentes (15/16/17/18) permanecem texto "(planejado)"; horizonte-lists intactos.
7. Cada nota: TL;DR; code samples compiláveis (Java moderno, imports corretos, fences `java`/`xml`/`yaml`/`properties`/`protobuf`/`bash`/`json`/`text`); "Em entrevista" com `### Frase pronta (inglês)` 3+ sentenças + `### Vocabulário` tabela 6+ termos PT→EN; "Armadilhas" com `### (N) Título` numerado + exemplo + fix (≥2 Iniciado, ≥3 Adepto/Magus); wikilinks (galho + MOC central + galho/cluster dono quando aplicável + Dicionário); "Referências" com docs oficiais verificadas.
8. **Fronteira-assinatura respeitada**: internals do Kafka linkam o cluster de infra (nunca re-explicados); event bus → G8; transação → G10; reativo → G11; concorrência → G4; testes → G13; galhos 15/16/17/18 só como texto "(planejado)"; nenhum wikilink pra galho inexistente.
9. **Fronteiras de escopo respeitadas**: microservices/Spring Cloud = Galho 16; cloud-native/deploy/produção = Galho 17; operar cluster Kafka = infra existente; teste profundo = Galho 13; zero conteúdo de operação de broker.
10. Zero fabricação de experiência pessoal; zero estatística de adoção inventada; o artigo de terceiro intocado e não copiado; afirmações version-specific citam a versão verificada via WebFetch.
11. 1 commit por nota; sem `Co-Authored-By: Claude`; sem `--no-verify`; stage nominal (nunca `-A`); subagents write-only, controlador commita.
12. `verificar-wikilinks` roda limpo na pasta do galho (evitar âncoras same-file; conferir os títulos EXATOS das notas E dos arquivos de infra linkados nos cheatsheets/checklist — lição do Galho 12, onde a nota 18 inventou títulos; os paths do cluster Kafka têm nomes longos com pontuação — conferir 1:1).

## 8. Riscos e mitigações

| Risco | Mitigação |
|---|---|
| **Re-explicar os internals do Kafka** (partições/offsets/replication) em vez de linkar o cluster de infra | Restrição 4.3.1; a nota 05 é explicitamente "na visão de app, linka a infra"; review por fase; conferir que notas apontam pra `Kafka Concepts`. |
| **Copiar/absorver o artigo de terceiro** (`Otimizando Kafka consumers.md`) | Coexistência = intocado; é material de outro autor; notas nascem de doc oficial via WebFetch; review por fase grep contra trechos do artigo. |
| **Inventar API/versão "de memória"** (KRaft/Zookeeper, `DefaultErrorHandler`, `@RetryableTopic`, `@StreamListener` removido, EOS) | WebFetch no Step 1 das notas version-specific; Referências com fonte oficial; nada "de memória". Ponto crítico: **Zookeeper removido no Kafka 4.0** (mudança recente — confirmar). |
| **Hype de tecnologia** ("Kafka resolve tudo", "exactly-once garante") em vez da tese honesta | A tese (desacoplamento ≠ velocidade; exactly-once distribuído é mito → idempotência) é fixada na nota 01/03/20/29; "quando NÃO usar" em 16 (in-process basta) e 28 (síncrono é melhor); review por fase. |
| **Inventar estatística de adoção** ("X% usa Kafka") | Zero estatística inventada; comparações qualitativas; números só com fonte. |
| **gRPC virar conteúdo Go** (o arquivo original é Go-cêntrico) | Notas 27/28 são **ângulo Java** (protoc plugin Java, grpc-java, grpc-spring-boot-starter); a instalação Go sai; review confere zero `go install`/`GOPATH` nas notas. |
| **Cheatsheet/checklist do capstone inventar títulos** (lição do Galho 12, nota 18) | Passar aos subagentes os **títulos EXATOS** das notas do galho **e dos arquivos de infra** linkados (paths longos com pontuação); `verificar-wikilinks` ao fim; review do capstone confere 1:1. |
| **Invadir Galho 16 (microservices)** ao falar de saga/Cloud Stream | Saga = padrão de **dados**; Spring Cloud (discovery/gateway/resiliência) = texto "(planejado)"; review por fase. |
| **Invadir Galho 17 (produção)** ao falar de observabilidade/deploy de broker | Observabilidade = lag/tracing **da aplicação**; deploy/operação de cluster = texto "(planejado)"; review por fase. |
| **Sobreposição entre notas de Spring Kafka** (07-13 muito parecidas) | Cada nota tem foco distinto (07 produção, 08 consumo, 09 serialização, 10 ack, 11 erro, 12 DLQ, 13 transação); review por fase checa sobreposição. |
| **Sobreposição nota 16 × Galho 8 nota 11** (eventos in-process) | A nota 16 é **ângulo de arquitetura** (quando substitui broker), linka G8 sem re-explicar o mecanismo; aprovado no brainstorming. |
| Galho denso (29 notas) inflar notas individuais | Distribuição 6/12/11 fixada; se uma nota passar de ~600 linhas, dividir nota (não galho); capstone com cheatsheet enxuto. |
| Dicionário: duplicar verbete já existente (`@EventListener`, `backpressure`) | Grep dos existentes antes de inserir; quando tocar um existente, **linkar** em vez de duplicar; inserção alfabética, nunca recriar. |
| Bot de backup (Obsidian Git) commitando no meio | Padrão dos Galhos 2-13: subagents write-only; controlador commita imediatamente após cada nota com `git add` nominal (nunca `-A`); guardar contra `.git/index.lock`. |

## 9. Próximos passos

1. **Aprovação deste spec**
2. **Plano de execução** via skill `superpowers:writing-plans` → `docs/superpowers/plans/2026-06-11-java-galho-14-mensageria-execution.md`
3. **Execução** via `superpowers:subagent-driven-development` **direto na `main`** (subagents write-only; sonnet por padrão, opus nas notas 01/03/08/13/20/21/22/28/29; review **por fase** + fix loop; push manual do usuário)
4. **Verificação** de wikilinks (incluindo os paths longos do cluster de infra) + conferência de âncoras do Dicionário
5. **Atualização da memória** `project_trilha_java` (Galho 14 completo) antes do próximo galho

## 10. Documentos relacionados

- `2026-06-02-java-senior-roadmap-design.md` — roadmap macro (18 galhos)
- `2026-06-11-java-galho-13-testes-design.md` / `...-execution.md` — Galho 13 (galho anterior; deixou ganchos Kafka; molde de galho de convergência)
- `2026-06-10-java-galho-11-reativa-design.md` — Galho 11 (galho de pesquisa; dono do reativo que a nota 25 usa; deixou a dívida do Reactor Kafka)
- `2026-06-08-java-galho-08-spring-core-design.md` — Galho 8 (dependência: o event bus in-process da nota 16; a concorrência/eventos do container)
- `2026-06-09-java-galho-10-persistencia-design.md` — Galho 10 (a transação que o outbox usa)
- `2026-06-03-java-galho-04-concorrencia-design.md` — Galho 4 (dependência: threads de consumo/async)
- Galhos 5/7/11 — template de **galho de pesquisa** (sem tronco a podar)
- Artefatos a criar/atualizar: `03-Dominios/Java/Mensageria/**` (29 notas + MOC), `03-Dominios/Java/Dicionário de Java.md`, `03-Dominios/Java/index.md`, `03-Dominios/Java/Backend/gRPC e Go.md` (migração/hub), `03-Dominios/Java/Backend/Kafka/index.md` + `03-Dominios/Java/Backend/index.md` (cross-link), `Programação Reativa/index.md` (dívida reversa), e ganchos inline em `Testes/11`/`Testes/14`/`Spring Core e Boot/11` (se existirem)
- Cluster de infra (coexistência, fronteira de link): `03-Dominios/Java/Backend/Kafka/Kafka Concepts/**` (19 notas), `Backend/Kafka/Kafka.md`, `Setting Up Kafka.md`
- Fontes-base do galho: `docs.spring.io/spring-kafka`, `docs.spring.io/spring-amqp`, `docs.spring.io/spring-cloud-stream`, `kafka.apache.org/documentation`, `docs.confluent.io`, `rabbitmq.com`, `projectreactor.io/docs/kafka`, `debezium.io`, `protobuf.dev`, `grpc.io`
- Memórias: [[project_trilha_java]], [[project_trilhas_fases_aprendizado]], [[project_tronco_galhos_pattern]], [[feedback_galhos_direto_main]], [[feedback_no_fabrication]], [[feedback_quartz_index]], [[feedback_commits]], [[feedback_dataview_inline_code]], [[feedback_notas_atomicas]], [[feedback_enriquecimento_feynman]]
