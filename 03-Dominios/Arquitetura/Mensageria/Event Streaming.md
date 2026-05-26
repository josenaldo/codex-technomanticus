---
title: "Event Streaming"
created: 2026-04-01
updated: 2026-04-10
type: concept
status: evergreen
tags:
  - arquitetura
  - mensageria
  - entrevista
publish: false
---

# Event Streaming

Modelo arquitetural onde **eventos** (fatos imutáveis) são publicados em um log persistente e consumidos de forma contínua. É a base das arquiteturas event-driven modernas — mais que apenas mensageria, é uma forma diferente de pensar o estado do sistema. Enquanto [[Mensageria]] cobre o domínio geral e [[03-Dominios/Arquitetura/Mensageria/Kafka]] é o deep dive na plataforma, esta nota foca nos **conceitos arquiteturais** de streams, event-driven, event sourcing e CQRS.

## O que é

Event streaming trata o sistema como uma **sequência contínua de fatos**. Cada mudança de estado é um evento imutável, publicado em um log. O estado atual do sistema é derivado desses eventos — ou consumido em tempo real por múltiplos serviços independentes.

**A mudança de mindset:**

- **Banco de dados tradicional:** "qual é o estado?" → consulta a linha atual
- **Event streaming:** "o que aconteceu?" → lê a sequência de eventos

O log **é** a fonte de verdade; o estado é uma projeção derivada.

Em entrevistas, o que diferencia um senior em event streaming:

1. **Entender que um evento é um fato imutável** — passado, não presente. `OrderPlaced`, não `PlaceOrder`.
2. **Separar Event Notification de Event-Carried State Transfer de Event Sourcing** — três conceitos que são frequentemente confundidos.
3. **Saber quando Event Sourcing é apropriado** — é poderoso mas caro. Não é default.
4. **Desenhar schemas de evento com evolução em mente** — schemas são contratos de longo prazo.
5. **Projetar para idempotência e eventual consistency** — eventos são async por natureza.

---

## Event: o conceito fundamental

Um **event** é um **fato imutável que aconteceu no passado**. Não é um comando, não é uma intenção — é um registro.

```json
{
  "id": "evt-7f8a9b2c",
  "type": "OrderPlaced",
  "version": 1,
  "occurred_at": "2026-04-10T14:23:11Z",
  "aggregate_id": "order-42",
  "data": {
    "customer_id": "cust-123",
    "items": [...],
    "total_cents": 15000,
    "currency": "BRL"
  },
  "metadata": {
    "correlation_id": "req-abc",
    "causation_id": "cmd-xyz",
    "user_id": "user-42"
  }
}
```

### Anatomia de um bom evento

- **Nome no passado** — `OrderPlaced`, `PaymentProcessed`, `UserRegistered`. Não `PlaceOrder` (isso é comando).
- **ID único** — para dedup, tracing, idempotência
- **Timestamp** — quando aconteceu (não quando foi publicado)
- **Versão do schema** — para evolução
- **Aggregate ID** — referência à entidade afetada (padrão DDD)
- **Data** — o payload do que aconteceu
- **Metadata** — correlation_id (trace), causation_id (qual comando causou), user_id (quem fez)

### Event vs Message vs Command

Três conceitos frequentemente misturados:

| | Command | Event | Message |
| --- | --- | --- | --- |
| Tempo | Imperativo (fazer) | Passado (aconteceu) | Neutro |
| Destinatário | Específico (1 handler) | Aberto (0..N consumers) | Depende |
| Expectativa | Pode ser rejeitado | Não pode ser rejeitado | Depende |
| Exemplo | `PlaceOrder` | `OrderPlaced` | qualquer dos dois |

**Regra mental:** comando pede algo para acontecer; evento anuncia o que aconteceu.

---

## Três estilos de event-driven

Martin Fowler distinguiu três usos diferentes de eventos — que são frequentemente confundidos e causam debates sem fim.

### 1. Event Notification

"Algo aconteceu. Se for de seu interesse, vá buscar os detalhes."

O evento é **minimalista** — carrega apenas o ID do aggregate afetado. Consumers que precisarem de mais dados fazem callback ao serviço producer.

```json
{
  "type": "OrderPlaced",
  "aggregate_id": "order-42"
}
```

Consumer faz: `GET /orders/order-42` para obter os detalhes.

**Prós:**
- Payload minúsculo
- Schema raramente muda
- Consumer sempre tem dados atualizados

**Contras:**
- **Acoplamento temporal** — producer precisa estar disponível quando consumer processa
- **Latência** — cada evento causa callbacks adicionais
- **Não serve para análise histórica** — dados do momento do evento se perdem

### 2. Event-Carried State Transfer

O evento carrega **tudo** que o consumer pode precisar. Não há necessidade de callback ao producer.

```json
{
  "type": "OrderPlaced",
  "aggregate_id": "order-42",
  "data": {
    "customer_id": "cust-123",
    "customer_name": "Maria Silva",
    "customer_email": "maria@example.com",
    "items": [
      { "product_id": "prod-1", "name": "Consulta Cardiologia", "price_cents": 15000, "quantity": 1 }
    ],
    "total_cents": 15000,
    "payment_method": "credit_card",
    "address": {...}
  }
}
```

**Prós:**
- **Desacoplamento total** — consumer não precisa do producer para processar
- **Resiliência** — se producer está fora, consumers continuam
- **Dados históricos fiéis** — o evento registra o estado no momento

**Contras:**
- Payload maior
- Schema complexo (mais pontos de evolução)
- Dados podem ficar stale no consumer (mas isso frequentemente é aceitável)

**Quando usar:** default para arquitetura event-driven em microserviços. Resiliência vale mais que economia de bytes.

### 3. Event-Sourced

O evento não é só uma notificação — **é** o estado. O sistema armazena a sequência de eventos como source of truth, e o estado atual é derivado reproduzindo os eventos.

```
Eventos do aggregate "order-42":
  1. OrderPlaced(items=[...], total=15000)
  2. PaymentProcessed(amount=15000, method="credit_card")
  3. OrderShipped(tracking="BR123456")
  4. OrderDelivered(at="2026-04-11T10:00Z")

Estado derivado:
  Order { id: "order-42", status: "delivered", ... }
```

Ver seção Event Sourcing abaixo.

### Qual escolher?

- **Event Notification** — integrações leves, sistemas legados, quando consumer sempre consulta o producer mesmo
- **Event-Carried State Transfer** — **default** para microserviços event-driven. Mais resiliente, mais desacoplado.
- **Event Sourced** — quando o histórico importa como fonte de verdade (auditoria, financeiro, compliance, debugging retroativo)

**Erro comum:** misturar os três sem saber. "Estamos fazendo event-driven" pode significar coisas muito diferentes. Seja explícito sobre qual padrão você está usando.

---

## Event Sourcing

Padrão avançado onde o **log de eventos é a fonte de verdade** do sistema. Ao invés de salvar o estado atual, você salva cada mudança como um evento imutável. O estado é derivado reproduzindo (replay) os eventos.

### Como funciona

```
Tradicional (state-oriented):
  UPDATE accounts SET balance = 250 WHERE id = 42;
  → você perdeu: "balance era 500, virou 250 quando o cliente sacou 250"

Event-sourced:
  INSERT INTO events (aggregate_id, type, data)
  VALUES ('account-42', 'MoneyWithdrawn', '{"amount": 250}');
  → você sabe: o que aconteceu, quando, por quê, em que ordem
```

### Reconstruindo estado

```java
public class Account {
    private String id;
    private Money balance;

    public static Account replay(String id, List<DomainEvent> events) {
        Account account = new Account();
        account.id = id;
        account.balance = Money.zero();
        for (DomainEvent event : events) {
            account.apply(event);
        }
        return account;
    }

    private void apply(DomainEvent event) {
        switch (event) {
            case AccountCreated e -> this.balance = e.initialBalance();
            case MoneyDeposited e -> this.balance = this.balance.add(e.amount());
            case MoneyWithdrawn e -> this.balance = this.balance.subtract(e.amount());
        }
    }

    // Command — gera um novo evento
    public MoneyWithdrawn withdraw(Money amount) {
        if (this.balance.isLessThan(amount)) {
            throw new InsufficientFundsException();
        }
        MoneyWithdrawn event = new MoneyWithdrawn(this.id, amount, Instant.now());
        this.apply(event);  // atualiza estado local
        return event;        // retorna para persistir
    }
}
```

### Snapshots

Replay de 1 milhão de eventos para reconstruir uma conta é caro. **Snapshot:** salve o estado a cada N eventos, e reproduza apenas a partir do último snapshot.

```
events:   e1, e2, e3, ..., e100, snapshot@100, e101, e102, e103
reconstrução de estado em e103:
  → carrega snapshot@100
  → aplica e101, e102, e103
```

### Vantagens do Event Sourcing

- **Auditoria completa** — histórico de tudo que aconteceu, imutável
- **Debug temporal** — "como chegamos neste estado?" — reproduza até o momento do bug
- **Time travel** — estado de qualquer momento no passado (retroactive analytics)
- **Novos insights sem reestruturar** — consumer novo processa histórico inteiro
- **Integra naturalmente com event-driven** — cada evento já é publicado
- **Reversão / compensação** — emita evento compensatório, não mude o passado

### Desafios do Event Sourcing

- **Complexidade alta** — curva de aprendizado, paradigma diferente
- **Schema evolution é crucial** — você nunca edita eventos antigos. Evoluir schemas exige upcasters ou versionamento.
- **Queries são difíceis** — não dá para fazer `SELECT * WHERE status = ...` sem projeções
- **Snapshots e replays** — performance exige snapshots bem pensados
- **GDPR / right to be forgotten** — eventos são imutáveis, mas você pode precisar apagar dados (cryptographic erasure resolve)
- **Consistência eventual** — projeções têm lag
- **Testing** — exige mindset diferente (test events, not state)

### Quando usar (e quando NÃO)

**Use Event Sourcing quando:**
- Auditoria é requisito regulatório (financeiro, saúde, compliance)
- Você precisa explicar "como chegamos neste estado"
- Há requisito claro de replay / reprocessamento
- O domínio tem comportamento rico modelável como eventos (DDD forte)

**NÃO use Event Sourcing quando:**
- CRUD simples resolve
- Equipe não tem experiência (curva alta)
- Não há requisitos de auditoria ou histórico
- Performance de queries é crítica e você não quer investir em projeções

**Regra prática:** Event Sourcing é raramente necessário. A maioria dos sistemas "event-driven" usa event-carried state transfer, não event sourcing. Não confunda.

---

## CQRS (Command Query Responsibility Segregation)

Padrão onde **modelo de escrita (commands)** e **modelo de leitura (queries)** são separados. Frequentemente — mas não necessariamente — combinado com Event Sourcing.

### O conceito

```
                     ┌────────────────┐
  Command  ───────→  │ Write Model    │
  (CreateOrder)      │ (normalized,   │
                     │  SQL, ACID)    │
                     └────────┬───────┘
                              │
                              │ Events
                              ↓
                     ┌────────────────┐
                     │ Read Model(s)  │
                     │ (denormalized, │
                     │  Redis/ES,     │
                     │  optimized     │
                     │  for queries)  │
                     └────────┬───────┘
                              ↑
  Query    ─────────────────────
  (GetOrderSummary)
```

**Write side:** modelo rico, normalizado, focado em validação e regras de negócio.

**Read side:** modelo desnormalizado, otimizado para cada tipo de consulta. Pode ser múltiplos (um para dashboard, outro para API pública, outro para analytics).

**Sincronização:** write publica eventos; consumers atualizam read models.

### Quando CQRS vale a pena

- **Read:write ratio muito alta** — cada read model pode ser otimizado independentemente
- **Queries complexas que não performam no modelo normalizado**
- **Diferentes views dos mesmos dados** — dashboard admin vs API mobile vs analytics
- **Escalar read e write separadamente** — bancos diferentes, caches diferentes

### Quando CQRS é overkill

- **CRUD simples** — um único modelo resolve
- **Equipe pequena** — manter 2 modelos sincronizados aumenta complexidade
- **Consistência forte obrigatória** — CQRS introduz eventual consistency entre write e read

**Exemplo prático:**

No MedEspecialista, o modelo de agendamentos usa **CQRS parcial**:
- **Write:** PostgreSQL com strong consistency (evita double-booking)
- **Read (disponibilidade):** Redis cache populado por eventos Kafka, atualizado em segundos

O usuário pode ver um slot "disponível" que acabou de ser reservado (stale por segundos), mas ao tentar reservar, a operação de write valida e pode retornar "já reservado". Eventual consistency aceitável no read; strong consistency no write.

### CQRS + Event Sourcing

Dupla natural: eventos do event sourcing alimentam read models.

```
Command → Write Model (event store)
              ↓
          Events published
              ↓
      ┌───────┼───────┐
      ↓       ↓       ↓
  Read Model Read Model Read Model
  (summary)  (search)   (analytics)
```

Cada read model é uma **projeção** — processa o stream e mantém sua visão.

---

## Stream Processing

Event streaming frequentemente é consumido por **stream processors** — aplicações que processam eventos conforme chegam, aplicam transformações, e produzem novos streams ou atualizam estado.

### Operações comuns

- **Filter** — só eventos que atendem critério
- **Map / Transform** — reformatar evento
- **Enrich** — adicionar dados de outras fontes (join)
- **Aggregate** — somar, contar, agrupar por janela de tempo
- **Windowing** — agrupar por tempo (tumbling, hopping, session)
- **Join** — combinar dois streams correlacionados
- **Materialization** — manter estado derivado (read model / view)

### Windowing

Eventos são contínuos, mas análise precisa de "períodos". Tipos de janela:

- **Tumbling** — janelas fixas, sem sobreposição. Ex.: contagem por minuto.
- **Hopping** — janelas fixas, com sobreposição. Ex.: média móvel dos últimos 5 min a cada 1 min.
- **Session** — janelas dinâmicas baseadas em gap de inatividade. Ex.: "sessão" do usuário.

```java
// Kafka Streams: contagem de pedidos por minuto
orders
    .groupByKey()
    .windowedBy(TimeWindows.ofSizeWithNoGrace(Duration.ofMinutes(1)))
    .count()
    .toStream()
    .to("orders-per-minute");
```

### Event time vs processing time

**Event time** — quando o evento aconteceu (timestamp no evento).

**Processing time** — quando o consumer processou.

Podem divergir drasticamente em replays, atrasos de rede, ou catch-up após incidente. **Sempre que possível, agrege por event time** — senão suas métricas mentem.

**Late-arriving events** — o que fazer com um evento de 10min atrás chegando agora? Depende do caso: descartar, incluir em janela antiga (reprocessar), ou mandar para side output.

### Ferramentas

| Ferramenta | Stack | Estilo |
| --- | --- | --- |
| Kafka Streams | Java (biblioteca) | Embedded, sem cluster separado |
| ksqlDB | SQL sobre Kafka | Declarativo |
| Apache Flink | Java/Scala (cluster) | Batch e stream unificado |
| Apache Spark Streaming | Java/Scala/Python (cluster) | Micro-batches |
| Faust | Python | Kafka Streams em Python |
| RxJS / streams libraries | Node.js | In-process streams |

---

## Event-Driven Architecture (EDA)

Arquitetura onde serviços se comunicam primariamente via eventos.

```
  ┌──────────────┐     event     ┌──────────────┐
  │ Order Service│ ───────────→  │ Event Broker │
  └──────────────┘               │    (Kafka)   │
                                 └──────┬───────┘
                                        ↓
          ┌─────────────────┬──────────┴──────────┬─────────────────┐
          ↓                 ↓                     ↓                 ↓
  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
  │ Inventory    │  │ Notification │  │ Analytics    │  │ Audit        │
  │ Service      │  │ Service      │  │ Service      │  │ Service      │
  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘
```

### Vantagens

- **Desacoplamento** — Order não sabe quem consome seus eventos
- **Evolução independente** — adicionar um novo consumer não afeta producers
- **Resiliência** — se Inventory cai, Order continua funcionando
- **Escalabilidade** — cada consumer escala independentemente
- **Auditoria natural** — log de eventos é auditável por design

### Desafios

- **Debugging distribuído** — rastrear o que aconteceu exige distributed tracing
- **Eventual consistency** — não existe "commit de transação cross-service"
- **Schema evolution** — mudar um evento afeta todos os consumers
- **Complexidade operacional** — mais peças móveis, mais monitoramento
- **Ordem e idempotência** — eventos podem chegar fora de ordem ou duplicados

### Quando adotar

**Adote EDA quando:**
- Você tem múltiplos domínios que precisam reagir aos mesmos fatos
- Serviços têm fronteiras claras (bounded contexts)
- Resiliência é crítica (não pode um serviço derrubar outros)
- Auditoria importa

**Adie EDA quando:**
- Monolito simples resolve
- Equipe é pequena e ainda aprendendo microserviços
- Fluxos são sequenciais e precisam de resposta imediata (síncrono é mais simples)

---

## Schema evolution

Eventos são contratos de longo prazo. Um evento publicado hoje pode ser consumido daqui a 5 anos em replay. Mudar schema requer disciplina.

### Regras

1. **Adicionar campo com default é seguro** — consumers antigos ignoram.
2. **Remover campo nunca é seguro** — um consumer ainda pode depender dele.
3. **Renomear campo é remover + adicionar** — quebra. Nunca faça.
4. **Mudar tipo é breaking** — `int` → `long` às vezes passa, `int` → `string` nunca.
5. **Adicionar enum value pode quebrar consumers que fazem switch exaustivo** — projete defensivo.

### Schema Registry

Centraliza schemas, valida compatibility em tempo de publicação. Confluent Schema Registry (Avro, Protobuf, JSON Schema) é o padrão.

**Compatibility modes:**
- **BACKWARD** — consumer novo lê dados do producer antigo
- **FORWARD** — consumer antigo lê dados do producer novo
- **FULL** — ambos
- **NONE** — sem checks (perigoso)

### Versionamento de evento

Inclua a versão no evento:

```json
{
  "type": "OrderPlaced",
  "version": 2,
  "data": {...}
}
```

Ou no próprio nome do tipo: `OrderPlaced.v2`. Consumers podem lidar com múltiplas versões ou aplicar upcaster (transforma v1 → v2 antes de processar).

### Upcaster pattern

```java
public OrderPlacedV2 upcast(OrderPlacedV1 v1) {
    return new OrderPlacedV2(
        v1.orderId(),
        v1.customerId(),
        v1.items(),
        v1.total(),
        "BRL"  // novo campo com default sensato
    );
}
```

Todo event-sourced system sério precisa de upcasters para lidar com histórico.

---

## Armadilhas comuns

- **Confundir event notification com event-sourced** — falar "event-driven" sem saber exatamente qual estilo
- **Eventos no tempo presente** — `OrderPlace` em vez de `OrderPlaced`. Eventos são fatos passados.
- **Eventos anêmicos em ESC** — carregar só ID quando o consumer precisa de dados (force callback, quebra desacoplamento)
- **Eventos gigantes em event sourcing** — carregar demais, events viram BLOBs
- **Event Sourcing quando CRUD resolve** — complexidade enorme sem benefício
- **CQRS sem necessidade** — 2 modelos para manter sem razão clara
- **Ignorar idempotência** — consumers devem tolerar duplicação e reordenação
- **Schema sem registry** — mudança quebra silenciosamente em produção
- **Reprocessar histórico sem pensar em side effects** — replay reenviando emails, cobrando de novo
- **Event time vs processing time misturados** — métricas mentem quando há replay
- **Acoplamento por evento** — consumer depende de campo específico; producer não pode mais remover
- **Sem distributed tracing** — debugar fluxo event-driven vira arqueologia
- **Um tópico enorme para tudo** — perde bounded context, misturar schemas
- **Evento como comando** — `SendEmail` publicado como evento. É comando disfarçado.
- **Falta de correlation_id / causation_id** — impossível rastrear causa e efeito
- **Mudar comportamento de projeção sem replay** — dados antigos ficam inconsistentes com a nova lógica

---

## Na prática (da minha experiência)

> **Muvz — Event-Carried State Transfer entre microserviços:**
> Na arquitetura com 5 microserviços, todos os eventos seguiam o padrão **event-carried state transfer**. O evento `ConsultaConfirmada` carregava todos os dados necessários: médico, paciente, valor, horário, local. Isso era crítico para resiliência — o serviço de notificação não precisava consultar o serviço de agendamento para enviar o email, o que significava que ele funcionava mesmo se o outro estivesse fora.
>
> **Decisão consciente de NÃO usar Event Sourcing:** consideramos, mas decidimos que a complexidade não se justificava. Usamos events como **forma de comunicação**, não como **source of truth**. O PostgreSQL continuava sendo a fonte de verdade; o Kafka era o canal de propagação.
>
> **MedEspecialista — CQRS parcial:**
> Implementei CQRS onde fazia sentido: o modelo de **leitura de slots disponíveis** é um Redis cache denormalizado, populado por eventos Kafka. O modelo de **escrita** (reservar um slot) é PostgreSQL com transação. O read model tem lag de segundos; aceitamos isso porque o write sempre valida. A performance de leitura melhorou em 10x — slots disponíveis são consultados centenas de vezes antes de cada reserva.
>
> **Onde acabamos não fazendo CQRS:** no módulo de cadastro de pacientes. A taxa de leitura não é tão alta, e manter dois modelos sincronizados adicionava complexidade sem benefício. CRUD direto no Postgres.
>
> **Schema Registry salvou vidas:** todas as evoluções de schema passavam pelo Schema Registry com BACKWARD compatibility. Uma vez tentei renomear um campo e o Schema Registry me impediu. Teria quebrado 3 consumers em produção.
>
> **Lição sobre replay:** em um incidente, precisei reprocessar eventos de 2 semanas para corrigir bug na projeção. O cuidado crítico: **garantir que o replay não dispara side effects**. Criei flag no consumer para "modo replay" que desativa o envio de notificações durante o reprocessamento. Sem isso, clientes teriam recebido milhares de emails duplicados.
>
> **A lição principal:** event-driven é poderoso, mas cada padrão tem custo. Seja consciente de qual padrão você está usando, por quê, e quais são os trade-offs. "Vamos fazer event-driven" não é uma decisão arquitetural — é marketing.

---

## How to explain in English

> "Event streaming is how I think about state changes in distributed systems. Instead of treating data as a current snapshot, I treat it as a sequence of immutable facts — events — that describe what happened. This mental shift enables replay, auditing, and decoupled consumers that can react to the same events independently.
>
> I make an explicit distinction between three patterns: Event Notification, Event-Carried State Transfer, and Event Sourcing. They're often conflated but solve different problems. For microservices communication, my default is Event-Carried State Transfer — the event carries all the data a consumer might need, so consumers don't have to call back to the producer. This maximizes decoupling and resilience.
>
> I reserve Event Sourcing for cases where the historical sequence of events itself is valuable — typically for auditing, financial systems, or debugging how the system reached a particular state. It's powerful but carries significant complexity, so I don't default to it.
>
> CQRS pairs naturally with event streaming — I separate the write model, which enforces invariants and business rules, from read models, which are projections optimized for specific queries. At MedEspecialista, the booking write model uses PostgreSQL with strong consistency to prevent double-bookings, while the read model for available slots is a Redis cache populated by Kafka events. Eventual consistency on reads is acceptable because writes always validate.
>
> Schema evolution is the hardest part of event streaming. Once an event is published, it's a long-term contract. I use Schema Registry with Avro and BACKWARD compatibility enforced — breaking changes fail at the producer level, before hitting production. And for versioned events, I use upcasters to transform old formats to new ones at consumption time."

### Frases úteis em entrevista

- "I distinguish explicitly between event notification, event-carried state transfer, and event sourcing."
- "My default for microservices is event-carried state transfer for maximum decoupling."
- "Event sourcing is powerful but complex — I reserve it for cases where the historical log itself is valuable."
- "CQRS separates write and read models, which can be optimized independently."
- "Schema Registry with BACKWARD compatibility catches breaking changes before production."
- "Events are immutable facts in the past — never commands."
- "I always include correlation_id and causation_id in event metadata for distributed tracing."
- "Replay must not trigger side effects — I design consumers with a replay mode that disables external calls."
- "For windowing, I aggregate by event time, not processing time, to keep metrics accurate during catch-up."

### Key vocabulary

- fluxo de eventos → event streaming
- arquitetura orientada a eventos → event-driven architecture (EDA)
- notificação de evento → event notification
- transferência de estado via evento → event-carried state transfer (ESC/ECST)
- event sourcing → event sourcing
- segregação de responsabilidade de comandos e consultas → CQRS
- modelo de escrita → write model / command model
- modelo de leitura → read model / query model
- projeção → projection
- agregado → aggregate (DDD)
- loja de eventos → event store
- upcaster → upcaster
- janela deslizante → sliding / hopping window
- janela fixa → tumbling window
- janela de sessão → session window
- tempo do evento → event time
- tempo de processamento → processing time
- evento atrasado → late-arriving event
- id de correlação → correlation id
- id de causação → causation id
- reprocessamento → replay / reprocessing

---

## Recursos

### Livros

- *Designing Event-Driven Systems* — Ben Stopford (Confluent, gratuito)
- *Event Sourcing and CQRS in .NET Core* — Alexey Zimarev (conceitos vale para qualquer stack)
- *Versioning in an Event Sourced System* — Greg Young (livro gratuito sobre o desafio mais difícil de ES)
- *Designing Data-Intensive Applications* — Martin Kleppmann (capítulos sobre stream processing)
- *Streaming Systems* — Tyler Akidau et al. (teoria de stream processing)

### Artigos

- [Martin Fowler — What do you mean by "Event-Driven"?](https://martinfowler.com/articles/201701-event-driven.html) — a distinção entre os 3 estilos
- [Martin Fowler — Event Sourcing](https://martinfowler.com/eaaDev/EventSourcing.html)
- [Martin Fowler — CQRS](https://martinfowler.com/bliki/CQRS.html)
- [Greg Young — CQRS Documents](https://cqrs.wordpress.com/documents/)
- [Confluent Blog — Event streaming patterns](https://www.confluent.io/blog/event-driven-microservices-kafka/)

### Online

- [Event Store](https://www.eventstore.com/) — banco especializado em event sourcing
- [Axon Framework](https://www.axoniq.io/) — framework Java para CQRS + Event Sourcing
- [EventStoreDB](https://github.com/EventStore/EventStore)

---

## Veja também

- [[Event Storming]] — workshop para descobrir eventos de domínio (DDD)
- [[03-Dominios/Arquitetura/Mensageria/Kafka]] — a plataforma de event streaming mais usada
- [[Mensageria]] — contexto geral, comparação com queues
- [[Arquitetura de Software]] — DDD, bounded contexts, EDA como estilo
- [[System Design]] — CQRS em walkthroughs
- [[API Design]] — webhooks como notificação de eventos
- [[Banco de dados]] — outbox pattern, CDC, strong vs eventual consistency
