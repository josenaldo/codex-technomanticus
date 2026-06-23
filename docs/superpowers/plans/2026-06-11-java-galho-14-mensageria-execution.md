# Galho 14 — Mensageria e eventos (Java Senior) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Criar o Galho 14 da trilha Java Senior — 29 notas atômicas (modelo/garantias, Spring Kafka produção/consumo/serialização/ack/erro/DLQ/transação, Avro/schema, RabbitMQ, eventos in-process, Cloud Stream, Kafka Streams/Connect, idempotência, outbox, saga, event sourcing/CQRS, versionamento, mensageria reativa, observabilidade, Protobuf, gRPC, capstone) em 3 fases + MOC do galho + expansão do Dicionário + ativação do MOC central + **migração/higiene** do `Backend/gRPC e Go.md` + **cross-link** do cluster Kafka existente + **quitação da dívida reversa**.

**Architecture:** Padrão galhos + 3 fases (Iniciado/Adepto/Magus). Pasta flat `03-Dominios/Tecnologia/Java/Mensageria/`, notas `publish: true` em PT-BR, numeração global 01-29 (6/12/11). **Galho NOVO/PESQUISA** (como 5/7/11 — sem tronco a podar) + **migração** de 1 arquivo pequeno (`gRPC e Go.md`, ângulo Java não Go) + **COEXISTÊNCIA** com o cluster Kafka de infra existente (`Backend/Kafka/`, 19 notas — linka, NÃO move/poda). **Fronteira-assinatura sêxtupla**: internals do Kafka → cluster de infra; event bus in-process → G8; transação/outbox → G10; reativo → G11; concorrência → G4; testes → G13. **Tese honesta**: mensageria = desacoplamento, não velocidade; exactly-once distribuído é mito → idempotência. Paga a dívida do Reactor Kafka (G11 `Reativa/index:35`). Galhos 15/16/17/18 = texto "(planejado)", sem wikilink. **Direto na `main`** ([[feedback_galhos_direto_main]]); push manual do usuário.

**Tech Stack:** Obsidian Flavored Markdown, frontmatter YAML, wikilinks, callouts, Dataview, Quartz v4. Verificação via WebFetch (docs.spring.io/spring-kafka, spring-amqp, spring-cloud-stream; kafka.apache.org; docs.confluent.io; rabbitmq.com; projectreactor.io/docs/kafka; debezium.io; protobuf.dev; grpc.io).

---

## Convenções aplicadas a TODAS as notas (ler antes de qualquer task)

**Frontmatter** (ajustar `title`/`fase`/`tags`/`aliases` por nota; `created`/`updated: 2026-06-11`):

```yaml
---
title: "<título sem prefixo numérico>"
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
  - <1-3 tags de conceito: kafka, spring-kafka, rabbitmq, amqp, eventos, idempotencia, outbox, saga, event-sourcing, cqrs, reativa, grpc, protobuf, observabilidade>
aliases:
  - <aliases>
---
```

H1 `# Título` após o frontmatter.

**Estrutura H2 obrigatória** (nesta ordem):

1. `> [!abstract] TL;DR` — 2-4 linhas. Callout, NÃO H2.
2. `## O que é` — definição.
3. `## Por que importa` — relevância pra senior/entrevista.
4. `## Como funciona` — H3s; mínimo 3 em Adepto/Magus.
5. `## Na prática` — código compilável; framing neutro; **NUNCA** 1ª pessoa, `Patient`, `Maria`, `Josenaldo`, `MedEspecialista`, "da minha experiência", "quando comecei o projeto", "incidente de produção". Domínios neutros: `Order`, `Customer`, `Payment`, `Shipment`, `OrderService`, `OrderPlacedEvent`. Imports corretos (`org.springframework.kafka.*`, `org.springframework.amqp.*`, `org.apache.kafka.clients.*`, `io.grpc.*`).
6. `## Armadilhas` — ≥2 (Iniciado) / ≥3 (Adepto/Magus). Cada uma: `### (N) Título` + descrição + exemplo curto + fix em 1 linha (H3 numerado, NÃO callout `[!warning]`).
7. `## Em entrevista` — `### Frase pronta (inglês)` com **3+ sentenças** + `### Vocabulário` **6+ termos** em tabela `| Termo PT | Termo EN |`.
8. `## Veja também` — wikilinks SEM backticks, SEM âncoras same-file. Sempre: notas do galho + `[[03-Dominios/Tecnologia/Java/Mensageria/index|Mensageria (MOC do galho)]]` + `[[03-Dominios/Tecnologia/Java/index|Trilha Java]]` + (quando aplicável) a nota da camada/galho dono + verbetes do Dicionário.
9. `## Referências` — docs oficiais consultadas.

**Tamanho:** 200-500 linhas (densas até 600 — limite de [[feedback_notas_atomicas]]).

**Restrições absolutas:**
- **FRONTEIRA-ASSINATURA (linkar de volta, NUNCA re-explicar).** Mapeamento de link-back (paths confirmados na Task 0):
  - **Cluster Kafka de infra** (internals: partições/offsets/replication/groups/KRaft/log compaction/Streams/Connect) → `03-Dominios/Tecnologia/Java/Backend/Kafka/Kafka Concepts/index` + notas específicas (`9. Producers`, `10. Consumers`, `11. Consumer Groups`, `12. Consumer Offsets`, `17. Kafka Connect`, `18. Kafka Streams`) e o MOC `03-Dominios/Tecnologia/Java/Backend/Kafka/index`. **NUNCA re-explicar internals — apontar.**
  - **G8** (event bus in-process) → `03-Dominios/Tecnologia/Java/Spring Core e Boot/11 - Eventos do ApplicationContext`.
  - **G10** (transação/outbox) → `03-Dominios/Tecnologia/Java/Persistência de dados/12 - Transações operacionais — @Transactional propagação, isolamento, rollback, readOnly`.
  - **G11** (reativo) → `03-Dominios/Tecnologia/Java/Programação Reativa/09 - Backpressure — request(n) e as estratégias BUFFER, DROP, LATEST` + `03-Dominios/Tecnologia/Java/Programação Reativa/index`.
  - **G4** (concorrência) → `03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index`.
  - **G13** (testes) → `03-Dominios/Tecnologia/Java/Testes/11 - Testcontainers — infra real em testes` + `03-Dominios/Tecnologia/Java/Testes/14 - Testando código assíncrono — Awaitility`.
  - **G9** (serialização, pra nota 14 de schema) → `03-Dominios/Tecnologia/Java/Web e APIs REST/05 - Serialização JSON com Jackson`.
- **Galhos 15/16/17/18 só como texto "(planejado)", SEM wikilink.** Greps de review checam `\[\[[^]]*(Galho (15|16|17|18)|Spring Cloud Gateway|Eureka|service discovery)`.
- Sem fabricação ([[feedback_no_fabrication]]); usar `Order`/`Customer`/`Payment`/`Shipment`. **Zero estatística de adoção inventada** (ex.: "X% das empresas usam Kafka"). **O artigo de terceiro `Backend/Kafka/Otimizando Kafka consumers.md` NÃO pode ser copiado nem absorvido** (é de outro autor; coexistência = intocado).
- **Pesquisa pras partes version-specific:** notas 05/07/08/11/12/13/14/15/17/18/20/21/25/26/27/28 fundam-se em WebFetch (Step 1); qualquer outra que cravar versão também confirma. **Fatos minados a confirmar:** **Zookeeper removido no Kafka 4.0 / KRaft only**; Spring Kafka 3.x atual; **`DefaultErrorHandler` substituiu `SeekToCurrentErrorHandler` (Spring Kafka 2.8+)**; `@RetryableTopic`; `DeadLetterPublishingRecoverer`; `KafkaTransactionManager`/EOS v2/`read_committed`; `enable.idempotence` default; **`@StreamListener` REMOVIDO** (Cloud Stream modelo funcional `Supplier`/`Function`/`Consumer`); Spring AMQP (quorum queues, streams no RabbitMQ 4.x); Reactor Kafka (`KafkaReceiver`/`KafkaSender`); Debezium atual; Avro + Confluent Schema Registry; proto3; grpc-java/grpc-spring-boot-starter; Micrometer Observation (tracing). Baseline Spring Boot 3.x (`jakarta.*`, Java 17), citando Boot 4.x como "mais recente". Nada de memória.
- **Não re-explicar o que é de outro galho/infra:** partições/offsets/replication/consumer-group internals → cluster Kafka (linkar); `@EventListener`/`ApplicationEvent` mecanismo → G8 (linkar); `@Transactional` mecanismo → G10 (linkar); Reactor/Mono/Flux → G11 (linkar); threads/async → G4 (linkar); testar → G13 (linkar). Microservices/Spring Cloud → G16 (texto); cloud-native/deploy → G17 (texto); operar cluster → infra (texto/link).
- Comparações justas (quando X E quando Y): Kafka vs RabbitMQ, queue vs topic, síncrono-RPC vs assíncrono-evento, broker vs event bus in-process, coreografia vs orquestração, at-least-once vs exactly-once, polling vs CDC.
- Code fences: ` ```java `, ` ```xml ` (pom), ` ```yaml `/` ```properties ` (config), ` ```protobuf ` (.proto), ` ```bash ` (CLI), ` ```json ` (payloads), ` ```text ` (diagramas). Sempre fechadas.
- Commits: sem `Co-Authored-By: Claude`; sem `--no-verify`; `git add <path>` nominal (bot de backup roda em timer — NUNCA `-A`; guardar contra `.git/index.lock`); 1 commit por nota; direto na `main`; **sem push, sem deploy**. Subagents NÃO rodam git — o controlador commita.

**Modelo por nota:** sonnet por padrão; **opus** nas **01** (assinatura/modelo), **03** (garantias/exactly-once), **08** (@KafkaListener core), **13** (transações/EOS), **20** (idempotência), **21** (outbox), **22** (saga), **28** (gRPC), **29** (capstone).

**Fontes oficiais (base):**
- Spring Kafka: `https://docs.spring.io/spring-kafka/reference/`
- Spring AMQP: `https://docs.spring.io/spring-amqp/reference/`
- Spring Cloud Stream: `https://docs.spring.io/spring-cloud-stream/reference/`
- Apache Kafka: `https://kafka.apache.org/documentation/`
- Confluent (EOS, Schema Registry, Connect): `https://docs.confluent.io/platform/current/`
- RabbitMQ: `https://www.rabbitmq.com/docs`
- Reactor Kafka: `https://projectreactor.io/docs/kafka/release/reference/`
- Debezium: `https://debezium.io/documentation/`
- Protocol Buffers: `https://protobuf.dev/`
- gRPC: `https://grpc.io/docs/` + `https://github.com/grpc/grpc-java`

---

## Task 0: Pré-flight — pasta, terreno e baselines

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Mensageria/` (pasta)

- [ ] **Step 1: Confirmar `main`**
```bash
git branch --show-current
```
Expected: `main`. NÃO criar branch.

- [ ] **Step 2: Criar a pasta do galho**
```bash
mkdir -p "03-Dominios/Tecnologia/Java/Mensageria"
```

- [ ] **Step 3: Confirmar os paths EXATOS dos arquivos de infra Kafka e das notas dos galhos linkados de volta**
```bash
ls "03-Dominios/Tecnologia/Java/Backend/Kafka/Kafka Concepts/" | grep -E "^(9|10|11|12|17|18)[.-] "
ls "03-Dominios/Tecnologia/Java/Backend/Kafka/" | grep -iE "index"
ls "03-Dominios/Tecnologia/Java/Spring Core e Boot/" | grep -E "^11 "
ls "03-Dominios/Tecnologia/Java/Persistência de dados/" | grep -E "^12 "
ls "03-Dominios/Tecnologia/Java/Programação Reativa/" | grep -E "^09 "
ls "03-Dominios/Tecnologia/Java/Web e APIs REST/" | grep -E "^05 "
ls "03-Dominios/Tecnologia/Java/Testes/" | grep -E "^(11|14) "
```
Expected (anotar os nomes EXATOS — o cluster Kafka tem pontuação irregular: `9. Producers.md`, `10. Consumers.md`, `11. Consumer Groups.md`, `12. Consumer Offsets.md`, `17. Kafka Connect.md`, `18. Kafka Streams.md`; G8 `11 - Eventos do ApplicationContext`; G10 `12 - Transações operacionais — @Transactional propagação, isolamento, rollback, readOnly`; G11 `09 - Backpressure — request(n) e as estratégias BUFFER, DROP, LATEST`; G9 `05 - Serialização JSON com Jackson`; G13 `11 - Testcontainers — infra real em testes`, `14 - Testando código assíncrono — Awaitility`). **Anotar divergências** — usar os nomes reais nos wikilinks.

- [ ] **Step 4: Relocalizar a dívida reversa e os ganchos inline (linhas podem ter mudado ou não existir)**
```bash
grep -n "Galho 14\|Mensageria\|Reactor Kafka\|planejado" "03-Dominios/Tecnologia/Java/Programação Reativa/index.md"
grep -n "Mensageria\|Kafka\|Galho 14\|planejado" "03-Dominios/Tecnologia/Java/index.md"
grep -rn "Galho 14\|Kafka.*planejado\|mensageria" "03-Dominios/Tecnologia/Java/Testes/11 - Testcontainers — infra real em testes.md" "03-Dominios/Tecnologia/Java/Testes/14 - Testando código assíncrono — Awaitility.md" "03-Dominios/Tecnologia/Java/Spring Core e Boot/11 - Eventos do ApplicationContext.md"
```
Expected (anotar linhas reais pra Tasks 35/37): MOC central tem item 14 (`*(planejado)*`); `Reativa/index` tem o parágrafo "Mensageria reativa/Reactor Kafka (Galho 14)" (~35). Os ganchos em Testes/11, Testes/14, Spring Core/11 podem ou não existir — **quitar só se existirem**. **NÃO tocar:** horizonte-lists de uma linha.

- [ ] **Step 5: Baseline do Dicionário**
```bash
grep -cE "^### " "03-Dominios/Tecnologia/Java/Dicionário de Java.md"
```
Expected: **403** (baseline pós-Galho 13). Anotar o número real.

- [ ] **Step 6: Conferir dups potenciais no Dicionário (pra Task 34)**
```bash
grep -niE "^### (@EventListener|@TransactionalEventListener|ApplicationEvent|evento|backpressure|Netty|Kafka|partition|offset|consumer group)" "03-Dominios/Tecnologia/Java/Dicionário de Java.md"
```
Expected: `@EventListener`/`@TransactionalEventListener`/`ApplicationEvent`/`backpressure` provavelmente existem (G8/G11). Anotar — na Task 34 **linkar**, não duplicar.

- [ ] **Step 7: Ler o `gRPC e Go.md` (pra Task 36) e conferir frontmatter/publish**
```bash
head -20 "03-Dominios/Tecnologia/Java/Backend/gRPC e Go.md"
grep -n "publish\|^---\|go install\|GOPATH\|protoc" "03-Dominios/Tecnologia/Java/Backend/gRPC e Go.md"
```
Expected: 52 linhas, dump de links (protobuf.dev, grpc.io) + instalação Go (`go install`/`GOPATH`). Anotar se há frontmatter (provavelmente não — começa em `# Protocol Buffers`). Na Task 36 vira hub + apêndice de referências; instalação Go sai.

- [ ] **Step 8 (NÃO commitar): registrar os achados** em comentário mental/notas para as tasks seguintes (paths exatos de infra, linhas da dívida, baseline Dicionário, dups). Nenhum commit nesta task.

---

## Fase Iniciado (notas 01-06)

> Cada nota: dispatch de subagente write-only com o texto da task + o bloco de Convenções. WebFetch no Step 1 quando version-specific. Controlador commita após cada nota.

### Task 1: Nota 01 — O que é mensageria e arquitetura orientada a eventos *(opus, assinatura)*

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Mensageria/01 - O que é mensageria e arquitetura orientada a eventos.md`

- [ ] **Step 1 (WebFetch):** `docs.spring.io/spring-kafka` (overview) + `kafka.apache.org/documentation` (intro) — confirmar terminologia (event/record, producer/consumer, topic).
- [ ] **Step 2 (escrever):** fase `iniciado`. Conteúdo: síncrono vs assíncrono; **desacoplamento temporal e espacial**; **comando vs evento** (intenção dirigida a 1 destino vs fato publicado a N); pub/sub como inversão de dependência (o producer não conhece os consumers); por que mensageria **≠ "mais rápido"** (é desacoplamento/resiliência/elasticidade). **A nota-assinatura:** declara que este galho é a **camada de aplicação Java/Spring** sobre a infra de Kafka já documentada (`[[03-Dominios/Tecnologia/Java/Backend/Kafka/index|cluster Kafka]]`) e linka as fronteiras (G4/G8/G10/G11/G13). Armadilhas (≥2): "mensageria = performance"; acoplar o consumer ao schema interno do producer. "Em entrevista" + "Veja também" (MOC galho, Trilha, cluster Kafka, G8 eventos) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Mensageria/01 - O que é mensageria e arquitetura orientada a eventos.md"
git commit -m "feat(java): galho 14 nota 01 — o que é mensageria e arquitetura orientada a eventos"
```

### Task 2: Nota 02 — Os modelos de mensageria — queue vs topic

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Mensageria/02 - Os modelos de mensageria — queue vs topic.md`

- [ ] **Step 1 (WebFetch):** `rabbitmq.com/docs` (exchanges/queues) + `kafka.apache.org/documentation` (topics/consumer groups) — confirmar semântica queue (competing consumers) vs topic (broadcast).
- [ ] **Step 2 (escrever):** fase `iniciado`. Point-to-point (queue, 1 consumidor efetivo por mensagem) vs publish-subscribe (topic, N consumidores independentes); o broker como intermediário; **JMS** como spec histórica da plataforma Jakarta (e por que Kafka/RabbitMQ **não** são JMS); push (broker empurra, RabbitMQ) vs pull (consumer puxa, Kafka). Armadilhas (≥2): usar topic onde queria competing consumers; assumir ordering global num topic particionado. "Em entrevista" + "Veja também" + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Mensageria/02 - Os modelos de mensageria — queue vs topic.md"
git commit -m "feat(java): galho 14 nota 02 — os modelos de mensageria (queue vs topic)"
```

### Task 3: Nota 03 — Garantias de entrega — e a falácia do exactly-once *(opus)*

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Mensageria/03 - Garantias de entrega — e a falácia do exactly-once.md`

- [ ] **Step 1 (WebFetch):** `kafka.apache.org/documentation` (delivery semantics) + `docs.confluent.io` (EOS) — confirmar at-most/least/exactly e a definição precisa de EOS.
- [ ] **Step 2 (escrever):** fase `iniciado`. At-most-once (commit antes de processar — pode perder); at-least-once (processa antes de commit — pode duplicar, o **default prático**); exactly-once. **A tese:** a **entrega** ponta-a-ponta é at-least-once; o **efeito** exactly-once se obtém com **idempotência** (linka nota 20); EOS do Kafka existe mas só dentro do Kafka (não cobre side-effects externos). Duplicação e perda; ordering por partição. Armadilhas (≥2): "configurei exactly-once, não preciso de idempotência"; achar que retry não duplica. "Em entrevista" + "Veja também" (nota 20, nota 13) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Mensageria/03 - Garantias de entrega — e a falácia do exactly-once.md"
git commit -m "feat(java): galho 14 nota 03 — garantias de entrega e a falácia do exactly-once"
```

### Task 4: Nota 04 — O ecossistema de brokers na JVM

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Mensageria/04 - O ecossistema de brokers na JVM.md`

- [ ] **Step 1 (WebFetch):** `kafka.apache.org` + `rabbitmq.com/docs` — confirmar posicionamento (Kafka = log distribuído/replay/alta vazão; RabbitMQ = broker AMQP/roteamento rico). ActiveMQ Artemis e cloud (SQS/SNS, Pub/Sub) podem ser tratados em texto.
- [ ] **Step 2 (escrever):** fase `iniciado`. Tabela comparativa Kafka vs RabbitMQ vs Artemis (JMS) vs cloud (SQS/SNS, GCP Pub/Sub, EventBridge); critérios de escolha (ordering, retenção/replay, throughput, roteamento, custo operacional). Armadilhas (≥2): escolher por hype; Kafka pra fila de tarefas de baixo volume (overkill operacional). "Em entrevista" + "Veja também" + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Mensageria/04 - O ecossistema de brokers na JVM.md"
git commit -m "feat(java): galho 14 nota 04 — o ecossistema de brokers na JVM"
```

### Task 5: Nota 05 — Kafka numa página para o dev de aplicação *(research + infra-link)*

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Mensageria/05 - Kafka numa página para o dev de aplicação.md`

- [ ] **Step 1 (WebFetch):** `kafka.apache.org/documentation` — confirmar **KRaft e a remoção do Zookeeper no Kafka 4.0** (ponto minado), modelo log/tópico/partição/offset/consumer-group.
- [ ] **Step 2 (escrever):** fase `iniciado`. Log distribuído, tópico/partição/offset e consumer group **na visão do dev de aplicação** (não do operador); **KRaft (Zookeeper removido no Kafka 4.0, WebFetch)**. **NÃO re-explicar internals** — apontar pra `[[03-Dominios/Tecnologia/Java/Backend/Kafka/Kafka Concepts/index|Kafka Concepts]]` (use o path/nome confirmado na Task 0) pra partições/replication/offsets. Armadilhas (≥2): mais consumers que partições (consumers ociosos); tentar re-explicar internals em vez de linkar. "Em entrevista" + "Veja também" (cluster Kafka de infra ×2-3 notas específicas) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Mensageria/05 - Kafka numa página para o dev de aplicação.md"
git commit -m "feat(java): galho 14 nota 05 — Kafka numa página para o dev de aplicação"
```

### Task 6: Nota 06 — Spring para mensageria — o panorama

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Mensageria/06 - Spring para mensageria — o panorama.md`

- [ ] **Step 1 (WebFetch):** `docs.spring.io/spring-kafka`, `docs.spring.io/spring-amqp`, `docs.spring.io/spring-cloud-stream` (overviews) — confirmar o escopo de cada projeto.
- [ ] **Step 2 (escrever):** fase `iniciado`. O mapa: **Spring Kafka** (cliente Kafka idiomático), **Spring AMQP** (RabbitMQ), **Spring Cloud Stream** (abstração de binders), **Spring Integration** (EIP — só menção, sem nota própria); o que cada um resolve e quando usar a abstração (Cloud Stream) vs o cliente direto. Armadilhas (≥2): Cloud Stream quando bastava o cliente direto; misturar abstrações no mesmo serviço. "Em entrevista" + "Veja também" + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Mensageria/06 - Spring para mensageria — o panorama.md"
git commit -m "feat(java): galho 14 nota 06 — Spring para mensageria (o panorama)"
```

### Task 7: Review da fase Iniciado (01-06)

- [ ] **Step 1:** dispatch de subagente revisor (spec compliance + qualidade) lendo as 6 notas. Checa: frontmatter+`fase`; estrutura H2; **zero fabricação** (grep `Patient|Maria|MedEspecialista|minha experiência|quando comecei|incidente`); **zero estatística inventada**; **zero re-explicação de internals do Kafka** (deve linkar a infra); zero wikilink pra galho 15/16/17/18; "Em entrevista" 3+ sentenças + 6+ termos; tese honesta presente (01/03). 
- [ ] **Step 2:** fix loop (implementador corrige) até aprovado. Sem commit novo se nada muda; se corrige, commit `fix(java): galho 14 — ajustes da fase Iniciado`.

---

## Fase Adepto (notas 07-18)

### Task 8: Nota 07 — KafkaTemplate — produzindo mensagens *(research)*

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Mensageria/07 - KafkaTemplate — produzindo mensagens.md`

- [ ] **Step 1 (WebFetch):** `docs.spring.io/spring-kafka/reference/` (KafkaTemplate) + `kafka.apache.org/documentation/#producerconfigs` — confirmar API e configs (`acks`, `linger.ms`, `batch.size`).
- [ ] **Step 2 (escrever):** fase `adepto`. `KafkaTemplate.send`, `ProducerRecord`, serializers (`JsonSerializer`/String/Avro→nota 14), **chave → partição** (ordering por chave; linka infra Producers/Keys), send assíncrono + `CompletableFuture`/callback, `ProducerConfig` essencial (`acks=all`, `linger.ms`, `batch.size`, idempotência→nota 20). ` ```java ` + ` ```yaml `. Armadilhas (≥3): `acks=1` esperando durabilidade; ignorar o future (perda silenciosa); chave nula esperando ordering. "Em entrevista" + "Veja também" (infra Producers, nota 08/14/20) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Mensageria/07 - KafkaTemplate — produzindo mensagens.md"
git commit -m "feat(java): galho 14 nota 07 — KafkaTemplate (produzindo mensagens)"
```

### Task 9: Nota 08 — @KafkaListener — consumindo mensagens *(opus, research)*

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Mensageria/08 - @KafkaListener — consumindo mensagens.md`

- [ ] **Step 1 (WebFetch):** `docs.spring.io/spring-kafka/reference/` (`@KafkaListener`, listener containers, `ConcurrentKafkaListenerContainerFactory`) — confirmar concorrência × partições, `auto.offset.reset`.
- [ ] **Step 2 (escrever):** fase `adepto`. `@KafkaListener`, o **listener container**, `ConcurrentKafkaListenerContainerFactory`, **concorrência × nº de partições** (concorrência > partições = threads ociosas — linka **G4** concorrência), `ConsumerRecord`, `@Header`/`@Payload`, `group.id`, `auto.offset.reset` (earliest/latest). Linka infra Consumers/Consumer Groups. Armadilhas (≥3): concorrência > partições; processamento longo bloqueando (rebalance/`max.poll.interval.ms`); `latest` perdendo mensagens no 1º deploy. "Em entrevista" + "Veja também" (infra Consumers, G4, nota 10) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Mensageria/08 - @KafkaListener — consumindo mensagens.md"
git commit -m "feat(java): galho 14 nota 08 — @KafkaListener (consumindo mensagens)"
```

### Task 10: Nota 09 — (De)serialização de mensagens *(research)*

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Mensageria/09 - (De)serialização de mensagens.md`

- [ ] **Step 1 (WebFetch):** `docs.spring.io/spring-kafka/reference/` (serialization, `JsonSerializer`/`JsonDeserializer`, `ErrorHandlingDeserializer`, `trusted.packages`).
- [ ] **Step 2 (escrever):** fase `adepto`. `JsonSerializer`/`JsonDeserializer` + type headers e `spring.json.trusted.packages`; `ErrorHandlingDeserializer` (poison pill — desserialização que falha antes do listener); String/ByteArray; ponte pra Avro (nota 14). Armadilhas (≥3): poison pill parando o consumer; `trusted.packages=*` (risco de classe arbitrária); acoplar ao FQCN do producer. "Em entrevista" + "Veja também" (nota 14, G9 serialização) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Mensageria/09 - (De)serialização de mensagens.md"
git commit -m "feat(java): galho 14 nota 09 — (de)serialização de mensagens"
```

### Task 11: Nota 10 — Ack modes e commit de offset *(research)*

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Mensageria/10 - Ack modes e commit de offset.md`

- [ ] **Step 1 (WebFetch):** `docs.spring.io/spring-kafka/reference/` (`AckMode`, `Acknowledgment`, container properties) + `kafka.apache.org` (offset commit).
- [ ] **Step 2 (escrever):** fase `adepto`. `AckMode` (RECORD/BATCH/MANUAL/MANUAL_IMMEDIATE/TIME/COUNT); por que o Spring desliga `enable.auto.commit`; commit síncrono vs assíncrono; at-least-once na prática (processar → commit); `Acknowledgment` no MANUAL. Linka infra Consumer Offsets. Armadilhas (≥3): auto-commit + processamento async (perde at-least-once); commit antes de processar (at-most-once acidental); MANUAL sem chamar `acknowledge()`. "Em entrevista" + "Veja também" (infra Offsets, nota 08/11) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Mensageria/10 - Ack modes e commit de offset.md"
git commit -m "feat(java): galho 14 nota 10 — ack modes e commit de offset"
```

### Task 12: Nota 11 — Tratamento de erro no consumo *(research)*

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Mensageria/11 - Tratamento de erro no consumo.md`

- [ ] **Step 1 (WebFetch):** `docs.spring.io/spring-kafka/reference/` (`DefaultErrorHandler`, `CommonErrorHandler`, `BackOff`) — confirmar que **`DefaultErrorHandler` substituiu `SeekToCurrentErrorHandler` (2.8+)**.
- [ ] **Step 2 (escrever):** fase `adepto`. `DefaultErrorHandler` (ex-`SeekToCurrentErrorHandler`, WebFetch), `FixedBackOff`/`ExponentialBackOff`, exceções não-retentáveis (`addNotRetryableExceptions`), `CommonErrorHandler`; o caminho até a DLQ (nota 12). Armadilhas (≥3): retry infinito bloqueando a partição; retentar erro de desserialização (não-retentável); backoff fixo sob falha persistente. "Em entrevista" + "Veja também" (nota 12) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Mensageria/11 - Tratamento de erro no consumo.md"
git commit -m "feat(java): galho 14 nota 11 — tratamento de erro no consumo"
```

### Task 13: Nota 12 — Dead Letter Topic — o padrão DLQ *(research)*

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Mensageria/12 - Dead Letter Topic — o padrão DLQ.md`

- [ ] **Step 1 (WebFetch):** `docs.spring.io/spring-kafka/reference/` (`DeadLetterPublishingRecoverer`, `@RetryableTopic`) + `rabbitmq.com/docs/dlx`.
- [ ] **Step 2 (escrever):** fase `adepto`. `DeadLetterPublishingRecoverer`, `@RetryableTopic` (retry topics + DLT, WebFetch), convenção de nome `*-dlt`, reprocessamento; DLQ no RabbitMQ (dead-letter-exchange) como contraponto. Armadilhas (≥3): DLQ sem alarme (mensagens morrem em silêncio); reprocessar DLQ sem corrigir a causa-raiz; retry topics multiplicando partições. "Em entrevista" + "Veja também" (nota 11/15) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Mensageria/12 - Dead Letter Topic — o padrão DLQ.md"
git commit -m "feat(java): galho 14 nota 12 — Dead Letter Topic (o padrão DLQ)"
```

### Task 14: Nota 13 — Transações e exactly-once no Spring Kafka *(opus, research)*

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Mensageria/13 - Transações e exactly-once no Spring Kafka.md`

- [ ] **Step 1 (WebFetch):** `docs.spring.io/spring-kafka/reference/` (transactions, `KafkaTransactionManager`) + `docs.confluent.io` (EOS v2) + `kafka.apache.org` (transactions/`isolation.level`).
- [ ] **Step 2 (escrever):** fase `adepto`. `KafkaTransactionManager`, `transactional.id`, **read-process-write** atômico, `isolation.level=read_committed`, EOS v2 (WebFetch); **o limite crítico**: a transação Kafka cobre só o que está dentro do Kafka — efeito em DB externo precisa do **outbox** (linka nota 21). Armadilhas (≥3): achar que a transação Kafka cobre o DB (dual-write); `transactional.id` reusado entre instâncias; misturar produção transacional e não-transacional. "Em entrevista" + "Veja também" (nota 03/20/21) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Mensageria/13 - Transações e exactly-once no Spring Kafka.md"
git commit -m "feat(java): galho 14 nota 13 — transações e exactly-once no Spring Kafka"
```

### Task 15: Nota 14 — Schema e contratos — Avro e Schema Registry *(research)*

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Mensageria/14 - Schema e contratos — Avro e Schema Registry.md`

- [ ] **Step 1 (WebFetch):** `docs.confluent.io/platform/current/schema-registry/` (Avro, compatibility) + `avro.apache.org`.
- [ ] **Step 2 (escrever):** fase `adepto`. Por que schema (contrato explícito entre producer/consumer desacoplados no tempo); **Avro** + Confluent Schema Registry (subject, versions); compatibilidade (BACKWARD/FORWARD/FULL); JSON Schema e Protobuf como alternativas (ponte pra nota 27). Linka **G9** serialização. Armadilhas (≥3): mudança incompatível quebrando consumers em produção; sem registry (contrato implícito no código); evoluir sem política de compatibilidade. "Em entrevista" + "Veja também" (G9 serialização, nota 24/27) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Mensageria/14 - Schema e contratos — Avro e Schema Registry.md"
git commit -m "feat(java): galho 14 nota 14 — schema e contratos (Avro e Schema Registry)"
```

### Task 16: Nota 15 — Spring AMQP e RabbitMQ *(research)*

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Mensageria/15 - Spring AMQP e RabbitMQ.md`

- [ ] **Step 1 (WebFetch):** `docs.spring.io/spring-amqp/reference/` + `rabbitmq.com/docs` (exchanges, quorum queues, streams).
- [ ] **Step 2 (escrever):** fase `adepto`. Modelo AMQP (exchange → binding → queue, routing key; tipos direct/topic/fanout/headers); `RabbitTemplate`, `@RabbitListener`, ack/nack/requeue; quorum queues e streams (RabbitMQ 4.x, WebFetch); **Kafka vs RabbitMQ** lado a lado (roteamento rico vs log/replay). Armadilhas (≥3): requeue infinito (poison message); fanout achando que filtra; confundir o modelo de roteamento do AMQP com o de partições do Kafka. "Em entrevista" + "Veja também" (nota 04, nota 12) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Mensageria/15 - Spring AMQP e RabbitMQ.md"
git commit -m "feat(java): galho 14 nota 15 — Spring AMQP e RabbitMQ"
```

### Task 17: Nota 16 — Eventos in-process do Spring *(research + G8-link)*

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Mensageria/16 - Eventos in-process do Spring.md`

- [ ] **Step 1 (WebFetch):** `docs.spring.io/spring-framework/reference/core/beans/context-introduction.html` (events) — `@EventListener`, `@TransactionalEventListener`, async events.
- [ ] **Step 2 (escrever):** fase `adepto`. `ApplicationEvent`/`@EventListener` **assíncrono** (`@Async`), `@TransactionalEventListener` (`phase=AFTER_COMMIT`); **o ângulo de arquitetura: quando o event bus interno substitui um broker** (monólito, mesmo processo, sem garantia de durabilidade entre processos). **Linka G8 nota 11 sem re-explicar o mecanismo** — foco em "broker vs in-process". Armadilhas (≥3): `@EventListener` síncrono achando que é async (mesma thread/transação); publicar evento mas o commit falhar (use AFTER_COMMIT); usar event bus interno esperando durabilidade entre serviços. "Em entrevista" + "Veja também" (**G8 Eventos do ApplicationContext**, nota 01) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Mensageria/16 - Eventos in-process do Spring.md"
git commit -m "feat(java): galho 14 nota 16 — eventos in-process do Spring"
```

### Task 18: Nota 17 — Spring Cloud Stream — a abstração de binders *(research)*

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Mensageria/17 - Spring Cloud Stream — a abstração de binders.md`

- [ ] **Step 1 (WebFetch):** `docs.spring.io/spring-cloud-stream/reference/` — confirmar **modelo funcional** (`Supplier`/`Function`/`Consumer` beans) e que **`@StreamListener` foi removido**.
- [ ] **Step 2 (escrever):** fase `adepto`. O modelo funcional (`Supplier`/`Function`/`Consumer` como beans; `@StreamListener` **removido**, WebFetch), binders (Kafka/Rabbit), `spring.cloud.stream.bindings`, destination/group; quando a indireção vale (trocar broker sem trocar código) e quando atrapalha (debugging, leaky abstraction). Armadilhas (≥3): indireção sem ganho real; binder errado em produção; esperar portabilidade total entre Kafka e Rabbit. "Em entrevista" + "Veja também" (nota 06, nota 25) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Mensageria/17 - Spring Cloud Stream — a abstração de binders.md"
git commit -m "feat(java): galho 14 nota 17 — Spring Cloud Stream (a abstração de binders)"
```

### Task 19: Nota 18 — Kafka Streams pela API Java *(research)*

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Mensageria/18 - Kafka Streams pela API Java.md`

- [ ] **Step 1 (WebFetch):** `kafka.apache.org/documentation/streams/` + `docs.spring.io/spring-kafka/reference/` (`@EnableKafkaStreams`, `StreamsBuilderFactoryBean`).
- [ ] **Step 2 (escrever):** fase `adepto`. `KStream`/`KTable`/`GlobalKTable`, topologia (`StreamsBuilder`), stateless (`map`/`filter`) vs stateful (`aggregate`/`join`/windowing), state stores; integração Spring (`@EnableKafkaStreams`). **Linka infra Kafka Streams (nota 18 do cluster)** pra o conceito de infra. Armadilhas (≥3): join sem co-partitioning; state store sem changelog (perda no rebalance); confundir Kafka Streams (lib na app) com Connect (infra). "Em entrevista" + "Veja também" (infra Kafka Streams, nota 19) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Mensageria/18 - Kafka Streams pela API Java.md"
git commit -m "feat(java): galho 14 nota 18 — Kafka Streams pela API Java"
```

### Task 20: Review da fase Adepto (07-18)

- [ ] **Step 1:** dispatch de subagente revisor lendo as 12 notas. Checa: frontmatter+`fase`; estrutura; **version-specific confirmado via WebFetch** (`DefaultErrorHandler`/ex-SeekToCurrent, `@RetryableTopic`, `@StreamListener` removido, EOS, KRaft); zero fabricação; zero re-explicação de internals (linka infra); ≥3 armadilhas; code fences corretas; "Em entrevista" completo; sobreposição entre 07-13 (cada uma foco distinto); nota 16 linka G8 sem re-explicar. 
- [ ] **Step 2:** fix loop até aprovado; commit `fix(java): galho 14 — ajustes da fase Adepto` se houver mudança.

---

## Fase Magus (notas 19-29)

### Task 21: Nota 19 — Kafka Connect pela ótica da app *(research)*

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Mensageria/19 - Kafka Connect pela ótica da app.md`

- [ ] **Step 1 (WebFetch):** `docs.confluent.io/platform/current/connect/` + `kafka.apache.org/documentation/#connect`.
- [ ] **Step 2 (escrever):** fase `magus`. Source/sink connectors; quando integrar via Connect (CDC, sink pra banco/S3/Elastic) vs produzir/consumir você mesmo; SMTs (single message transforms); **Connect é infra, não código de app**. Linka infra Kafka Connect (nota 17 do cluster). Armadilhas (≥3): reinventar Connect na mão (consumer custom pra sink trivial); Connect pra lógica de negócio (é para movimentação de dados); ignorar idempotência do sink. "Em entrevista" + "Veja também" (infra Connect, nota 21 CDC) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Mensageria/19 - Kafka Connect pela ótica da app.md"
git commit -m "feat(java): galho 14 nota 19 — Kafka Connect pela ótica da app"
```

### Task 22: Nota 20 — Idempotência — o pilar do at-least-once *(opus, research)*

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Mensageria/20 - Idempotência — o pilar do at-least-once.md`

- [ ] **Step 1 (WebFetch):** `kafka.apache.org` (`enable.idempotence`, idempotent producer) + `docs.confluent.io`.
- [ ] **Step 2 (escrever):** fase `magus`. Por que at-least-once **exige** consumidor idempotente; chaves de deduplicação (idempotency key), tabela de dedup / `INSERT ... ON CONFLICT DO NOTHING`, idempotent producer (`enable.idempotence=true`, WebFetch — evita dup do producer em retry); operações naturalmente idempotentes (upsert/set) vs não (increment). Liga **nota 03**. Armadilhas (≥3): consumer não-idempotente em at-least-once (efeito duplicado); dedup sem TTL (tabela cresce infinito); confundir idempotent producer (dup do producer) com idempotência do consumer (dup de entrega). "Em entrevista" + "Veja também" (nota 03/13/21) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Mensageria/20 - Idempotência — o pilar do at-least-once.md"
git commit -m "feat(java): galho 14 nota 20 — idempotência (o pilar do at-least-once)"
```

### Task 23: Nota 21 — O padrão Outbox *(opus, research)*

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Mensageria/21 - O padrão Outbox.md`

- [ ] **Step 1 (WebFetch):** `debezium.io/documentation/` (outbox event router, CDC).
- [ ] **Step 2 (escrever):** fase `magus`. O **dual-write problem** (escrever no DB **e** publicar no broker atomicamente é impossível sem 2PC); **transactional outbox** (gravar o evento numa tabela na **mesma transação** do negócio + um relay publica depois); **CDC com Debezium** (WebFetch — lê o WAL/binlog) vs polling publisher. Liga **G10** transação (`12 - Transações operacionais`). Armadilhas (≥3): publicar no broker dentro do `@Transactional` (dual-write — o broker não faz rollback); outbox sem limpeza (tabela cresce); relay sem idempotência (linka nota 20). "Em entrevista" + "Veja também" (**G10 Transações**, nota 13/20, nota 19 Connect/CDC) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Mensageria/21 - O padrão Outbox.md"
git commit -m "feat(java): galho 14 nota 21 — o padrão Outbox"
```

### Task 24: Nota 22 — Saga — transações distribuídas por eventos *(opus, research)*

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Mensageria/22 - Saga — transações distribuídas por eventos.md`

- [ ] **Step 1 (WebFetch):** `microservices.io/patterns/data/saga.html` (texto/conceito) — confirmar coreografia vs orquestração e compensação. (Sem cravar produto.)
- [ ] **Step 2 (escrever):** fase `magus`. Por que **não há transação ACID entre serviços**; saga como sequência de transações locais + eventos; **coreografia** (serviços reagem a eventos, descentralizado) vs **orquestração** (um coordenador central comanda); **compensação** (undo semântico, não rollback). **Microservices/Spring Cloud = Galho 16 (texto, sem wikilink).** Armadilhas (≥3): saga sem compensação (estado inconsistente permanente); coreografia complexa virando spaghetti de eventos sem visibilidade; orquestrador como ponto único de falha. "Em entrevista" + "Veja também" (nota 21/23) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Mensageria/22 - Saga — transações distribuídas por eventos.md"
git commit -m "feat(java): galho 14 nota 22 — saga (transações distribuídas por eventos)"
```

### Task 25: Nota 23 — Event sourcing e CQRS *(research)*

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Mensageria/23 - Event sourcing e CQRS.md`

- [ ] **Step 1 (WebFetch):** `martinfowler.com/eaaDev/EventSourcing.html` + `martinfowler.com/bliki/CQRS.html` (texto/conceito).
- [ ] **Step 2 (escrever):** fase `magus`. O **evento como fonte da verdade** (append-only log) vs estado mutável; rebuild do estado por replay; snapshots; **CQRS** (separar write model de read models/projections); **quando NÃO usar** (a complexidade — versionamento, replay, eventual consistency — raramente paga). Armadilhas (≥3): event sourcing por moda (complexidade desnecessária); CQRS sem read model que justifique; assumir consistência forte entre write e read. "Em entrevista" + "Veja também" (nota 22/24) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Mensageria/23 - Event sourcing e CQRS.md"
git commit -m "feat(java): galho 14 nota 23 — event sourcing e CQRS"
```

### Task 26: Nota 24 — Versionamento e evolução de eventos *(research)*

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Mensageria/24 - Versionamento e evolução de eventos.md`

- [ ] **Step 1 (WebFetch):** `docs.confluent.io/platform/current/schema-registry/fundamentals/schema-evolution.html` + `avro.apache.org` (schema resolution).
- [ ] **Step 2 (escrever):** fase `magus`. Eventos são **contratos públicos e duradouros** (consumidores desconhecidos no futuro); schema evolution (adicionar campo opcional com default ✓, remover/renomear campo obrigatório ✗); upcasting (transformar evento velho em novo na leitura); tolerância (ignore unknown fields); compatibilidade forward/backward/full. Liga **nota 14**. Armadilhas (≥3): renomear campo (quebra consumers); remover campo sem deprecação; mudar o significado de um campo mantendo o nome. "Em entrevista" + "Veja também" (nota 14, nota 23) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Mensageria/24 - Versionamento e evolução de eventos.md"
git commit -m "feat(java): galho 14 nota 24 — versionamento e evolução de eventos"
```

### Task 27: Nota 25 — Mensageria reativa — Reactor Kafka *(research)*

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Mensageria/25 - Mensageria reativa — Reactor Kafka.md`

- [ ] **Step 1 (WebFetch):** `projectreactor.io/docs/kafka/release/reference/` (`KafkaReceiver`/`KafkaSender`).
- [ ] **Step 2 (escrever):** fase `magus`. `KafkaReceiver`/`KafkaSender` (reactor-kafka, WebFetch); **backpressure no consumo** (linka **G11** `09 - Backpressure`); Spring Cloud Stream reativo (`Function<Flux<T>, Flux<R>>`); **quando o reativo paga no consumo de stream** (e quando os Virtual Threads tornam o imperativo suficiente — linka G11/G4). **Paga a dívida do `Reativa/index:35`.** Armadilhas (≥3): bloquear dentro do pipeline reativo (trava o event loop); reativo no consumo sem necessidade real; commit de offset fora do fluxo reativo. "Em entrevista" + "Veja também" (**G11 Backpressure + Programação Reativa index**, nota 08) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Mensageria/25 - Mensageria reativa — Reactor Kafka.md"
git commit -m "feat(java): galho 14 nota 25 — mensageria reativa (Reactor Kafka)"
```

### Task 28: Nota 26 — Observabilidade em mensageria *(research)*

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Mensageria/26 - Observabilidade em mensageria.md`

- [ ] **Step 1 (WebFetch):** `docs.spring.io/spring-kafka/reference/` (observability/Micrometer) + `micrometer.io/docs/observation` — confirmar context propagation/tracing via Micrometer Observation.
- [ ] **Step 2 (escrever):** fase `magus`. **Consumer lag** (a métrica nº 1 — fila acumulando); **tracing distribuído através do broker** (context propagation via headers da mensagem, Micrometer Observation/OpenTelemetry, WebFetch); métricas de producer/consumer; por que log não basta num fluxo assíncrono (correlação perdida). Armadilhas (≥3): só logar sem correlação (trace quebra no broker); ignorar lag até a fila estourar; não propagar o trace context nos headers. "Em entrevista" + "Veja também" (nota 08/10) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Mensageria/26 - Observabilidade em mensageria.md"
git commit -m "feat(java): galho 14 nota 26 — observabilidade em mensageria"
```

### Task 29: Nota 27 — Protocol Buffers — a IDL e a serialização binária *(migração + research)*

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Mensageria/27 - Protocol Buffers — a IDL e a serialização binária.md`

- [ ] **Step 1 (WebFetch):** `protobuf.dev/` (proto3 language guide, Java generated code) — confirmar tipos, field numbers, `reserved`, `protoc` + plugin Java.
- [ ] **Step 2 (escrever):** fase `magus`. `.proto` (proto3), tipos escalares/message/enum/repeated, serialização binária compacta, **schema evolution** (field numbers estáveis, `reserved` pra campos removidos); `protoc` + plugin **Java** (`protoc-gen-grpc-java`/protobuf-maven-plugin); protobuf vs JSON vs Avro. **Migra parte do `gRPC e Go.md` — ângulo Java, NÃO Go** (nada de `go install`/`GOPATH`). ` ```protobuf ` pra o `.proto`. Armadilhas (≥3): reusar field number (corrompe dados); mudar o tipo de um campo; renumerar campos. "Em entrevista" + "Veja também" (nota 28/14) + Referências (protobuf.dev).
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Mensageria/27 - Protocol Buffers — a IDL e a serialização binária.md"
git commit -m "feat(java): galho 14 nota 27 — Protocol Buffers (a IDL e a serialização binária)"
```

### Task 30: Nota 28 — gRPC em Java — RPC síncrono sobre HTTP/2 *(opus, migração + research)*

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Mensageria/28 - gRPC em Java — RPC síncrono sobre HTTP_2.md`

> Nota: o nome do arquivo usa `HTTP_2` (underscore) para evitar `/` no path. O `title` no frontmatter usa "HTTP/2".

- [ ] **Step 1 (WebFetch):** `grpc.io/docs/` + `github.com/grpc/grpc-java` — confirmar os 4 tipos de chamada, geração de stub, grpc-spring-boot-starter.
- [ ] **Step 2 (escrever):** fase `magus`. Os **4 tipos de chamada** (unary, server-streaming, client-streaming, bidirectional), HTTP/2 (multiplexação), stubs gerados (blocking/async stub), `grpc-java` + grpc-spring-boot-starter (WebFetch); **gRPC vs REST vs mensageria** (o eixo síncrono-RPC vs assíncrono-evento — gRPC é RPC ponto-a-ponto, não desacopla no tempo); quando RPC é a escolha certa (baixa latência, contrato forte, streaming entre serviços). **Migra parte do `gRPC e Go.md` — ângulo Java.** Armadilhas (≥3): gRPC onde mensageria desacoplaria melhor; streaming sem necessidade; expor gRPC ao browser (precisa de grpc-web/gateway). "Em entrevista" + "Veja também" (nota 27, nota 01/04 — síncrono vs assíncrono) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Mensageria/28 - gRPC em Java — RPC síncrono sobre HTTP_2.md"
git commit -m "feat(java): galho 14 nota 28 — gRPC em Java (RPC síncrono sobre HTTP/2)"
```

### Task 31: Nota 29 — Capstone — uma mensagem de ponta a ponta *(opus, checklist + síntese)*

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Mensageria/29 - Capstone — uma mensagem de ponta a ponta.md`

- [ ] **Step 1:** receber do controlador a **lista EXATA dos títulos das 28 notas anteriores** (01-28) e dos arquivos de infra linkados (paths confirmados na Task 0). **NÃO inventar títulos** (lição do Galho 12 — a nota 18 inventou 20 títulos). WebFetch só se precisar reconfirmar algum fato.
- [ ] **Step 2 (escrever):** fase `magus`. O **fluxo completo** numa narrativa: comando → transação + **outbox** (nota 21) → relay/Debezium → tópico Kafka (`KafkaTemplate`, nota 07) → **`@KafkaListener`** (nota 08) → **consumidor idempotente** (nota 20) → efeito → erro → retry (nota 11) → **DLQ** (nota 12) → **observabilidade** (lag/tracing, nota 26). **Tabela de decisão** ("preciso de broker, ou o event bus in-process basta? Kafka ou RabbitMQ? síncrono → gRPC?"); cheatsheet **nota → problema que resolve** (com os títulos EXATOS); munição de entrevista. Armadilhas de raciocínio (≥3): "evento pra tudo" (acoplamento temporal desnecessário); "exactly-once resolve" (é idempotência); "broker é default" (in-process/síncrono muitas vezes basta). "Em entrevista" (frase de síntese 3+ sentenças) + "Veja também" (MOC do galho + capstones/ramos relacionados) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Mensageria/29 - Capstone — uma mensagem de ponta a ponta.md"
git commit -m "feat(java): galho 14 nota 29 — capstone (uma mensagem de ponta a ponta)"
```

### Task 32: Review da fase Magus (19-29)

- [ ] **Step 1:** dispatch de subagente revisor lendo as 11 notas. Checa: frontmatter+`fase`; estrutura; **a tese honesta** (idempotência > exactly-once; quando NÃO usar mensageria); **nota 28 em ângulo Java** (zero `go install`/`GOPATH`); saga/CQRS **não invadem Galho 16** (Spring Cloud = texto); observabilidade **não invade Galho 17** (deploy/produção = texto); **o capstone usa os títulos EXATOS** (sem invenção — lição G12); zero fabricação; ≥3 armadilhas. 
- [ ] **Step 2:** fix loop até aprovado; commit `fix(java): galho 14 — ajustes da fase Magus` se houver mudança.

---

## Artefatos de fechamento

### Task 33: MOC do galho (`index.md`)

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Mensageria/index.md`

- [ ] **Step 1 (escrever):** seguir §3.2 da spec. `type: moc`, `status: growing`, tags `java`/`mensageria`/`moc`, aliases `["Mensageria e eventos", "Mensageria", "Messaging", "Event-Driven", "Galho 14 - Mensageria"]`. TL;DR (29 notas, 3 fases, camada de aplicação Java/Spring + tese honesta). "Sobre este galho" (NOVO/PESQUISA + coexistência com infra Kafka + migração gRPC + fronteira sêxtupla + tese). 3 H2 de fase com wikilinks descritivos pras 29 notas (uma linha cada). **5 rotas alternativas** (Completa; Entrevista internacional 01→03→07→08→12→20→21→22→28→29; Spring Kafka operacional 05→07→08→09→10→11→12→13; Confiabilidade/event-driven 03→20→21→22→23→24; Síncrono vs assíncrono 01→02→27→28→29). "Veja também" (Trilha; **cluster Kafka** `[[03-Dominios/Tecnologia/Java/Backend/Kafka/index|Kafka]]`; G8 eventos; G4 concorrência; G11 reativa; G13 testes; Dicionário; 16/17 texto "(planejado)"). Dataview `TABLE fase, status FROM "03-Dominios/Tecnologia/Java/Mensageria" WHERE type = "concept" SORT file.name ASC`.
- [ ] **Step 2 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Mensageria/index.md"
git commit -m "feat(java): galho 14 MOC — Mensageria e eventos"
```

### Task 34: Dicionário de Java (EXPANSÃO — não recriar)

**Files:**
- Modify: `03-Dominios/Tecnologia/Java/Dicionário de Java.md`

- [ ] **Step 1:** dispatch de subagente com os ~35 verbetes pré-escritos (§3.3 da spec) + os dups achados na Task 0 Step 6. Regras: inserir **em ordem alfabética case-insensitive (ignorando `@`/acento)** nas seções `## A`…`## Z` existentes; **não recriar, não reordenar**; **não duplicar** `@EventListener`/`@TransactionalEventListener`/`ApplicationEvent`/`backpressure` (G8/G11) — se existirem, **linkar** (adicionar 2ª linha "Veja também" cruzada, como o G11 fez com `WebClient`); cada verbete novo: definição 1-3 linhas PT-BR + `Veja também:` pra nota(s) canônica(s). Manter `updated: 2026-06-11`.
- [ ] **Step 2 (verificar):**
```bash
grep -cE "^### " "03-Dominios/Tecnologia/Java/Dicionário de Java.md"
```
Expected: baseline (403) + nº de verbetes realmente novos (≈ +30-35, menos os linkados). Conferir ordenação alfabética nas seções tocadas e ausência de linhas em branco duplas.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Dicionário de Java.md"
git commit -m "feat(java): expande Dicionário de Java com verbetes do galho 14 (Mensageria)"
```

### Task 35: MOC central — ativação do Galho 14

**Files:**
- Modify: `03-Dominios/Tecnologia/Java/index.md` (linha do galho 14 — confirmada na Task 0)

- [ ] **Step 1:** trocar a linha `14. Mensageria e eventos *(planejado)* — ...` pelo wikilink ativo (§3.4 da spec). Atualizar `updated: 2026-06-11`. Não mexer no resto.
- [ ] **Step 2 (verificar):**
```bash
grep -n "Mensageria" "03-Dominios/Tecnologia/Java/index.md"
```
Expected: linha 14 vira `14. [[03-Dominios/Tecnologia/Java/Mensageria/index|Mensageria e eventos]] — ...`.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/index.md"
git commit -m "feat(java): ativa Galho 14 (Mensageria e eventos) no MOC central"
```

### Task 36: Migração/higiene do `Backend/gRPC e Go.md`

**Files:**
- Modify: `03-Dominios/Tecnologia/Java/Backend/gRPC e Go.md`

- [ ] **Step 1:** ler o arquivo inteiro (confirmar frontmatter/publish da Task 0 Step 7). Reescrever como **hub de referência**: frontmatter (criar se não houver, `publish: true` como o resto do Backend, `updated: 2026-06-11`); H1 `# gRPC e Protocol Buffers`; 1-2 frases neutras; callout `[!nota] Migrado para galho próprio` apontando pra `[[03-Dominios/Tecnologia/Java/Mensageria/27 - Protocol Buffers — a IDL e a serialização binária|Protocol Buffers]]`, `[[03-Dominios/Tecnologia/Java/Mensageria/28 - gRPC em Java — RPC síncrono sobre HTTP_2|gRPC em Java]]` e o MOC do galho; **apêndice de referências** preservando os links úteis (protobuf.dev, grpc.io/docs, repos). **Remover** os passos de instalação Go (`go install`/`GOPATH`/`protoc-gen-go`) — são Go, fora do escopo Java. 
- [ ] **Step 2 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Backend/gRPC e Go.md"
git commit -m "refactor(java): migra gRPC e Go.md para hub do galho 14 (ângulo Java)"
```

### Task 37: Dívida reversa e cross-links do cluster Kafka

**Files:**
- Modify: `03-Dominios/Tecnologia/Java/Programação Reativa/index.md` (~35)
- Modify: `03-Dominios/Tecnologia/Java/Backend/Kafka/index.md`
- Modify: `03-Dominios/Tecnologia/Java/Backend/index.md`
- Modify (se os ganchos existirem — Task 0 Step 4): `03-Dominios/Tecnologia/Java/Testes/11 - Testcontainers — infra real em testes.md`, `03-Dominios/Tecnologia/Java/Testes/14 - Testando código assíncrono — Awaitility.md`, `03-Dominios/Tecnologia/Java/Spring Core e Boot/11 - Eventos do ApplicationContext.md`

- [ ] **Step 1:** `Reativa/index` — o parágrafo "Mensageria reativa/Reactor Kafka (Galho 14)" vira wikilink pra `[[03-Dominios/Tecnologia/Java/Mensageria/25 - Mensageria reativa — Reactor Kafka|Mensageria reativa]]`; manter 16/17 como texto "(planejado)". `updated: 2026-06-11`.
- [ ] **Step 2:** `Backend/Kafka/index.md` — adicionar em "Veja também" wikilink pro MOC do galho (`[[03-Dominios/Tecnologia/Java/Mensageria/index|Mensageria e eventos]]` — "a camada de aplicação Java/Spring sobre estes fundamentos"). `updated: 2026-06-11`.
- [ ] **Step 3:** `Backend/index.md` — adicionar referência ao MOC do galho Mensageria na lista/Veja também (o item `[[gRPC e Go]]` segue válido — virou hub). `updated: 2026-06-11`.
- [ ] **Step 4 (se existirem):** quitar ganchos inline "Kafka/mensageria = Galho 14 (planejado)" em `Testes/11`→nota 05/08, `Testes/14`→nota 08, `Spring Core/11`→nota 16. **Só se o grep da Task 0 achou** — senão, pular. Manter horizonte-lists intactos; 15/16/17/18 seguem "(planejado)".
- [ ] **Step 5 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Programação Reativa/index.md" "03-Dominios/Tecnologia/Java/Backend/Kafka/index.md" "03-Dominios/Tecnologia/Java/Backend/index.md"
# + os arquivos de Testes/Spring Core SE tocados:
# git add "03-Dominios/Tecnologia/Java/Testes/11 - Testcontainers — infra real em testes.md" ...
git commit -m "refactor(java): quita dívida reversa do galho 14 — ponteiros de mensageria viram wikilinks"
```

### Task 38: Verificação de wikilinks

- [ ] **Step 1:** rodar o detector na pasta do galho:
```bash
python3 .agents/skills/verificar-wikilinks/scripts/check_wikilinks.py "03-Dominios/Tecnologia/Java/Mensageria" --respect-public-only
```
- [ ] **Step 2:** ler o JSON. **Atenção especial aos paths longos do cluster Kafka** (pontuação irregular: `9. Producers`, `12. Consumer Offsets` etc.) e ao arquivo `28 ... HTTP_2`. Expected: **0 quebras**. Se houver, corrigir (provável: título de infra divergente do confirmado na Task 0, ou âncora same-file). Re-rodar até limpo.
- [ ] **Step 3 (commit, se houve correção):**
```bash
git add "03-Dominios/Tecnologia/Java/Mensageria/"
git commit -m "fix(java): galho 14 — corrige wikilinks quebrados"
```

### Task 39: Verificação estrutural final + memória + relatório

- [ ] **Step 1 (estrutura):**
```bash
ls "03-Dominios/Tecnologia/Java/Mensageria/" | grep -cE "\.md$"          # 30 (29 notas + index)
grep -rl "fase: iniciado" "03-Dominios/Tecnologia/Java/Mensageria/" | wc -l   # 6
grep -rl "fase: adepto" "03-Dominios/Tecnologia/Java/Mensageria/" | wc -l     # 12
grep -rl "fase: magus" "03-Dominios/Tecnologia/Java/Mensageria/" | wc -l      # 11
```
Expected: 30 / 6 / 12 / 11.
- [ ] **Step 2 (anti-fabricação + anti-galho-inexistente + anti-Go):**
```bash
grep -rniE "Patient|Maria|MedEspecialista|minha experiência|quando comecei|incidente de produção" "03-Dominios/Tecnologia/Java/Mensageria/"     # vazio
grep -rnE "\[\[[^]]*(Galho (15|16|17|18)|Spring Cloud Gateway|Eureka)" "03-Dominios/Tecnologia/Java/Mensageria/"                                 # vazio
grep -rniE "go install|GOPATH|protoc-gen-go " "03-Dominios/Tecnologia/Java/Mensageria/"                                                          # vazio (gRPC em ângulo Java)
```
Expected: todos vazios.
- [ ] **Step 3 (cada nota: 3+ seções de fase, 1 TL;DR, Em entrevista):** spot-check via grep `^## ` e `\[!abstract\] TL;DR` numa amostra.
- [ ] **Step 4 (memória):** atualizar `project_trilha_java.md` (bloco de status do Galho 14 completo: 29 notas 6/12/11, opus list, fronteira sêxtupla, coexistência com infra Kafka, migração gRPC, dívida reversa quitada, fatos WebFetch cravados — Zookeeper removido no Kafka 4.0, `DefaultErrorHandler`, `@StreamListener` removido, EOS, Reactor Kafka etc.) + "Próximo galho sugerido" → 15 (Build/tooling) ou 16 (Microservices). Atualizar linha 27 do `MEMORY.md`.
- [ ] **Step 5 (relatório de fechamento, sem commit):** reportar ao usuário: 29 notas (6/12/11), MOC, Dicionário (403→~435), MOC central ativado, gRPC migrado, cluster Kafka cross-linkado (coexistência), dívida reversa quitada, wikilinks 0 quebras, fatos version-specific cravados. Não iniciar Galho 15/16 sem confirmação.

---

## Self-review do plano (preenchido)

**1. Cobertura da spec:** §3.1 (29 notas) → Tasks 1-6, 8-19, 21-31; §3.2 (MOC) → Task 33; §3.3 (Dicionário) → Task 34; §3.4 (MOC central) → Task 35; §3.5 (migração gRPC) → Task 36; §3.6 (dívida reversa/cross-link) → Task 37; pré-flight → Task 0; reviews por fase → Tasks 7/20/32; wikilinks → Task 38; aceitação/memória → Task 39. Sem lacunas.

**2. Placeholders:** nenhum "TBD"/"implementar depois". Os "se existirem" (ganchos inline da Task 37 Step 4) são condicionais legítimos resolvidos por grep na Task 0/Task 37, não placeholders.

**3. Consistência:** numeração 01-29 e distribuição 6/12/11 batem entre header, tasks e Task 39. Opus list (01/03/08/13/20/21/22/28/29) idêntica entre Convenções, spec §3.1/§9 e as tasks. Paths de link-back (cluster Kafka, G8/G10/G11/G4/G13/G9) idênticos entre Convenções e tasks; todos confirmados na Task 0 antes do uso. Nome do arquivo da nota 28 (`HTTP_2`) consistente entre Task 30 e Task 37/38.
