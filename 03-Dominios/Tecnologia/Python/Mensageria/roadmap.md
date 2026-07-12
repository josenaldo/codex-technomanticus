---
title: "Roadmap — Python Mensageria"
created: 2026-07-12
type: meta
publish: false
tags:
  - meta
  - roadmap
  - python
---

# Roadmap — Mensageria (galho 14)

Roadmap-folha do galho `Python/Mensageria`. Fase **Adepto→Magus** — Celery, RQ, aio-pika, kafka-python/aiokafka. Spec: [[00-Meta/specs/2026-07-09-python-trilha-design]]. EXEMPLAR de estrutura: `Python/Arquitetura e Design Patterns/index.md` e `roadmap.md` (galho anterior, mesmo padrão). Primeiro galho do bloco **"Plataforma distribuída e produção"** (14-18) — muda de registro em relação ao bloco anterior (9-13, construção da API em si): aqui o assunto é como sistemas Python se comunicam de forma desacoplada em produção.

**Fronteira cravada:** conceitos de mensageria (queue vs streaming, garantias de entrega, Outbox/Saga, legado enterprise) já cobertos em [[03-Dominios/Engenharia/Comunicação entre Sistemas/4 - Comunicação assíncrona/index|Comunicação entre Sistemas — Comunicação assíncrona]] (6 notas); brokers em si (Kafka/RabbitMQ) já em [[03-Dominios/Engenharia/Comunicação entre Sistemas/Mensageria/index|Comunicação entre Sistemas — Mensageria]]. Java/Mensageria (29 notas) é o exemplar de como uma trilha de linguagem aplica esses conceitos com o ferramental do ecossistema — este galho faz o equivalente Python, mas na escala já estabelecida da trilha (8 notas, não 29).

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 8 |
| ⬜ pendente | 0 |
| ✅ feita | 8 |
| 🔄 em andamento | 0 |
| % concluído | 100% |

---

## Notas

#### 01 - Panorama — Celery vs RQ vs aio-pika vs aiokafka
- **Estado:** ✅ feita (2026-07-12) · fase: Adepto
- **Resultado:** 426 linhas / 6374 palavras. Abre com welcome-email bloqueando request via SMTP síncrono; resolve o mesmo problema nos 4 ferramentais lado a lado, diagrama de decisão task-queue/broker-direto/streaming, 3 cenários de produção, observabilidade (Flower/rq-dashboard vs tooling externo).
- **Escopo:** panorama comparativo do ferramental Python de mensageria — Celery (task queue madura, abstrai o broker — Redis ou RabbitMQ por baixo, foco em execução de tarefas em background), RQ (Redis Queue, mais simples, menos features, mais fácil de debugar), aio-pika (cliente assíncrono direto pro protocolo AMQP/RabbitMQ, você fala com o broker, não com uma abstração de "tarefa"), kafka-python/aiokafka (cliente Kafka, producer/consumer, para event streaming, não task queue). Critérios de escolha: task queue (fire-and-forget, retry automático) vs comunicação direta com broker (mais controle, mais código).

#### 02 - Celery fundamentos — broker, worker e tasks
- **Estado:** ✅ feita (2026-07-12) · fase: Adepto
- **Resultado:** 432 linhas / 4950 palavras. Abre com `Session` do SQLAlchemy passada como argumento de task (falha JSON explícita, ou pickle "funcionando" com `DetachedInstanceError` sutil depois); arquitetura app→broker→worker→backend opcional, `.delay()`/`.apply_async()`, JSON como padrão referenciando o risco de pickle do Galho 11 nota 02.
- **Escopo:** arquitetura do Celery (aplicação Python define tasks, broker — Redis/RabbitMQ — enfileira, worker(s) separados consomem), `@shared_task`/`@app.task`, `.delay()` vs `.apply_async()` (com `countdown`/`eta`/`queue`), o resultado assíncrono (`AsyncResult`, backend de resultado opcional), serialização de argumentos (JSON por padrão, cuidado com objetos não serializáveis).

#### 03 - Celery em produção — retries, idempotência e Celery Beat
- **Estado:** ✅ feita (2026-07-12) · fase: Adepto
- **Resultado:** 423 linhas / 5125 palavras. Abre com e-mail de boas-vindas enviado duas vezes por retry sobre entrega já bem-sucedida; `autoretry_for`/`retry_backoff`/`retry_jitter`, idempotência com tabela de deduplicação transacional/`select_for_update`/`ON CONFLICT`, Celery Beat (`crontab()`, armadilha da instância única de Beat), Flower.
- **Escopo:** retries automáticos (`autoretry_for`, `retry_backoff`, `max_retries`), idempotência aplicada na prática (referenciando o conceito já coberto em Comunicação entre Sistemas sem repetir — aqui é código Python real: chave de idempotência, upsert em vez de insert cego), Celery Beat (tarefas agendadas/periódicas, contraste com cron tradicional), monitoramento básico (Flower).

#### 04 - RQ — a fila simples sobre Redis
- **Estado:** ✅ feita (2026-07-12) · fase: Adepto
- **Resultado:** 305 linhas / 4156 palavras (contraste com Celery, deliberadamente mais curta). Abre com time afogado em config Celery pra um único e-mail; `Queue.enqueue()` sem decorator, `Retry()` mais simples, `rq-scheduler` menos maduro que Beat, `rq-dashboard`; tabela de contraste e ponto de virada pra migrar de RQ pra Celery.
- **Escopo:** `Queue`/`enqueue()`, worker `rq worker`, contraste DIRETO com Celery (RQ não tem retry automático sofisticado nem scheduling nativo maduro — é deliberadamente mais simples), quando a simplicidade do RQ compensa a menor feature-set (projetos pequenos, times que não querem a complexidade operacional do Celery).

#### 05 - aio-pika — RabbitMQ assíncrono
- **Estado:** ✅ feita (2026-07-12) · fase: Adepto→Magus
- **Resultado:** 370 linhas / 5201 palavras. Abre com 3 produtores desacoplados roteados por routing key via exchange topic (Celery/RQ não modelam bem); `connect_robust()`, exchange/queue/binding, publish/consume assíncrono, ack manual vs auto-ack vs `message.process()`, back-pressure via `Semaphore`, competing consumers.
- **Escopo:** cliente assíncrono pro protocolo AMQP, `connect_robust()` (reconexão automática), declarar exchange/queue/binding (conceitos do broker em si, referenciando Comunicação entre Sistemas/Mensageria sem repetir), publish/consume com `async`/`await` (referenciando asyncio do Galho 7-8 desta trilha sem repetir event loop). Diferença de propósito vs Celery: aqui você fala DIRETO com o broker, sem abstração de "tarefa".

#### 06 - kafka-python e aiokafka — producer e consumer
- **Estado:** ✅ feita (2026-07-12) · fase: Adepto→Magus
- **Resultado:** 431 linhas / 5576 palavras. Abre com evento "tarefa concluída" precisando de 3 consumers independentes (notificação/analytics/auditoria); `KafkaProducer`/`AIOKafkaProducer`, `group_id`/partições/rebalance referenciado sem repetir, JSON+menção breve a Avro/Schema Registry, auto-commit vs manual commit com warning de perda silenciosa.
- **Escopo:** `KafkaProducer`/`KafkaConsumer` (síncrono, `kafka-python`) vs `AIOKafkaProducer`/`AIOKafkaConsumer` (assíncrono, `aiokafka`), (de)serialização de mensagens (JSON simples, menção a Avro/Schema Registry sem desenvolver — já mencionado en passant na trilha Java se existir), consumer groups (conceito do broker, referenciar Mensageria/Kafka sem repetir), commit de offset manual vs automático.

#### 07 - Garantias de entrega na prática — DLQ e Outbox em Python
- **Estado:** ✅ feita (2026-07-12) · fase: Magus
- **Resultado:** 448 linhas / 5557 palavras. Abre com matrícula confirmada no banco mas evento nunca chegou ao broker (dual-write); DLQ nativa do RabbitMQ (`x-dead-letter-exchange`) vs padrão manual do Celery; Outbox com `OutboxEvent`/SQLAlchemy, UoW do Galho 13 gravando na mesma transação, worker Celery Beat fazendo polling e publicando via aio-pika.
- **Escopo:** aplica os PADRÕES já ensinados conceitualmente em Comunicação entre Sistemas (DLQ, Outbox) com código Python real — Dead Letter Queue configurada no Celery (`task_reject_on_worker_lost`) e no RabbitMQ (fila de erro dedicada via aio-pika), Outbox pattern implementado com SQLAlchemy (referenciando a Unit of Work do Galho 13 — a UoW grava o evento na mesma transação da mudança de estado, um processo separado lê a tabela outbox e publica no broker).

#### 08 - Capstone — processamento assíncrono na API de Tarefas
- **Estado:** ✅ feita (2026-07-12) · fase: Magus
- **Escopo:** recapitula o galho dando processamento assíncrono de verdade à API de Tarefas hexagonal do Galho 13 — publica um Domain Event (`TarefaConcluida`) via Outbox (nota 07) quando uma tarefa é concluída, um worker Celery (nota 02/03) consome esse evento e envia a notificação (usando o `AbstractNotificador`/`SlackAdapter` já construído no Galho 13 nota 07), desacoplando a API do tempo de resposta do envio de notificação. Cenário prático integrador. Aponta para o Galho 15 (Microservices) como próximo passo — a mesma API, agora falando com um broker, está a um passo de virar parte de um sistema distribuído de verdade.
- **Resultado:** 580 linhas / 6290 palavras. `Tarefa.concluir()` gera `TarefaConcluida` como invariante; UoW grava no outbox na mesma transação; Celery Beat faz polling; publica via aio-pika; consumer chama `SlackAdapter` do Galho 13; DLQ protege contra falha repetida; menção honesta de quando migrar pra Kafka (múltiplos consumers independentes). 2 diagramas Mermaid.

> [!success] Galho 14 completo — 8/8 notas (2026-07-12) — abre o bloco "Plataforma distribuída e produção"
> Panorama Celery/RQ/aio-pika/aiokafka (01) → Celery fundamentos (02) → Celery em produção/idempotência/Beat (03) → RQ (04) → aio-pika/RabbitMQ assíncrono (05) → kafka-python/aiokafka (06) → DLQ/Outbox na prática (07) → capstone dando processamento assíncrono real à API de Tarefas (08). Conceitos de mensageria (queue vs streaming, garantias de entrega, Outbox/Saga) nunca repetidos — sempre referenciados a Comunicação entre Sistemas. Próximo da trilha: Galho 15 — Microservices e sistemas distribuídos.

## Decisões e fronteiras registradas

- Conceitos de mensageria (queue vs streaming, garantias de entrega, Outbox/Saga, legado) → [[03-Dominios/Engenharia/Comunicação entre Sistemas/4 - Comunicação assíncrona/index|Comunicação assíncrona]]; aqui é só a aplicação Python.
- Brokers em si (arquitetura interna do Kafka/RabbitMQ) → [[03-Dominios/Engenharia/Comunicação entre Sistemas/Mensageria/index|Mensageria (Engenharia)]]; aqui é só o cliente Python.
- `asyncio`/event loop → Galhos 7-8 desta trilha; usado por `aio-pika`/`aiokafka`, não reexplicado.
- Domain Events como conceito arquitetural → Galho 13 (capstone); aqui eles finalmente saem pro mundo via broker real.
- Schema Registry/Avro em profundidade → fora do escopo (menção breve na nota 06), é tema de contrato de dados mais avançado que a trilha não aprofunda em Python.
- Escala 8 notas (não 29 como Java) — Java aplica o padrão Spring completo (KafkaTemplate/@KafkaListener/Spring Cloud Stream/Kafka Streams/gRPC); Python trilha mantém ritmo estabelecido de 8-9 notas por galho, sem cobrir Kafka Streams/Kafka Connect/gRPC (fora do escopo do spec original, que só cita Celery/RQ/aio-pika/kafka-python/aiokafka).
