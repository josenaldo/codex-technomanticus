---
title: "O padrão Outbox"
fase: Magus
tags:
  - java
  - mensageria
  - magus
  - outbox
created: 2026-06-11
updated: 2026-06-11
type: concept
status: seedling
publish: true
alias: "Outbox pattern"
---

# O padrão Outbox

> [!abstract] TL;DR
> Você acabou de salvar um `Order` no Postgres e precisa publicar um evento `OrderCreated` no Kafka. São **dois sistemas distintos** — o banco e o broker — e você não consegue tornar as duas escritas atômicas sem *two-phase commit*. Esse é o **dual-write problem**: um lado pode confirmar e o outro falhar, deixando o sistema inconsistente. A solução é o **transactional outbox**: em vez de publicar no broker, você grava o evento numa tabela `outbox` **dentro da mesma transação** do negócio (uma única escrita, atômica de graça). Depois, um **relay** lê a tabela e publica no broker — seja por *polling*, seja por **CDC** (o [[03-Dominios/Tecnologia/Java/Mensageria/19 - Kafka Connect pela ótica da app|Debezium]] lê o WAL/binlog do banco e empurra cada linha nova para o Kafka). O evento sai pelo menos uma vez (at-least-once), então o consumidor downstream precisa ser **idempotente**.

## O que é

O **padrão Outbox** (transactional outbox) é uma técnica para publicar eventos de forma confiável a partir de um serviço que também escreve num banco de dados relacional. A ideia central é simples: trocar duas escritas em dois sistemas por **uma única escrita transacional no banco**, e delegar a publicação de fato para um processo separado.

Em vez de fazer o serviço dizer "salva o pedido **e** publica o evento", ele diz "salva o pedido **e** registra o evento numa tabela `outbox`" — ambas as instruções na mesma transação SQL. Como o banco garante atomicidade de transações locais, ou as duas linhas são commitadas, ou nenhuma é. Um componente à parte, o **relay** (ou *message relay* / *publisher*), lê depois as linhas da `outbox` e as entrega ao broker.

O nome vem da metáfora postal: a `outbox` é a "caixa de saída". Você deposita a carta na caixa de forma confiável; o carteiro (o relay) a recolhe e entrega mais tarde. A entrega não é instantânea nem síncrona com o seu commit — e está tudo bem.

> [!info] Onde isso se encaixa
> O Outbox é a resposta sênior para a pergunta "como faço para que o banco e o Kafka concordem?". Ele aparece logo depois das [[03-Dominios/Tecnologia/Java/Mensageria/13 - Transações e exactly-once no Spring Kafka|transações Kafka]], porque é justamente o caso que a EOS do Kafka **não** cobre: escrever num sistema externo ao broker.

## Por que importa

Numa arquitetura orientada a eventos, quase todo serviço precisa fazer as duas coisas ao mesmo tempo: **mudar seu estado** (gravar no banco) e **contar ao mundo** que mudou (emitir um evento). A tentação natural é escrever as duas coisas em sequência. Essa sequência é uma armadilha de consistência.

Pense num serviço de pagamentos. Ele debita a conta (escrita no Postgres) e publica `PaymentConfirmed` no Kafka para que o serviço de pedidos libere a entrega. Se o banco commitar mas o publish falhar, o dinheiro saiu e ninguém liberou o pedido — cliente pagou e não recebeu. Se você inverte a ordem e publica antes de commitar, pode publicar `PaymentConfirmed` e o commit no banco falhar logo depois — o pedido é liberado para um pagamento que nunca existiu.

Não há ordenação esperta que resolva isso, porque a falha pode cair **entre** as duas operações. É um problema estrutural de coordenar dois sistemas sem uma transação que os abrace. O Outbox importa porque é a forma pragmática e amplamente adotada de eliminar essa janela, sem arrastar o peso operacional de um *distributed transaction coordinator* (XA / 2PC).

## Como funciona

### O dual-write problem

O **dual-write problem** é o nome do equívoco: tentar escrever em **dois sistemas independentes** (o banco e o broker) e esperar que ambos confirmem ou ambos falhem juntos. Eles não compartilham transação.

```java
// ❌ Dual-write: NÃO faça isso
@Transactional
public void confirmarPagamento(Payment payment) {
    paymentRepository.save(payment);          // sistema 1: Postgres
    kafkaTemplate.send("payments", event);    // sistema 2: Kafka — fora da transação!
}
```

Há quatro desfechos possíveis e dois deles são catastróficos:

| Banco commitou? | Broker recebeu? | Resultado |
| --- | --- | --- |
| ✅ | ✅ | Consistente (o caso feliz) |
| ❌ | ❌ | Consistente (nada aconteceu) |
| ✅ | ❌ | **Estado mudou, ninguém soube** |
| ❌ | ✅ | **Evento fantasma de algo que não existe** |

A única forma de garantir atomicidade entre dois recursos heterogêneos seria *two-phase commit* (2PC / XA): um coordenador faz `prepare` em ambos e só então `commit`. Mas 2PC é lento, frágil sob partições de rede, mal suportado por brokers modernos (o Kafka não fala XA) e operacionalmente odiado. O Outbox o evita por completo, reduzindo o problema a **uma só transação local**.

### Transactional outbox

A virada do Outbox é parar de escrever em dois sistemas. Você grava o evento numa **tabela `outbox`**, no mesmo banco e na **mesma transação** da escrita de negócio:

```java
// ✅ Outbox: uma transação, um sistema (o banco)
@Transactional
public void confirmarPagamento(Payment payment) {
    paymentRepository.save(payment);   // escrita de negócio
    outboxRepository.save(             // evento, MESMA transação
        new OutboxEvent("Payment", payment.getId(), "PaymentConfirmed", toJson(payment))
    );
}
```

Agora só existe um recurso transacional: o Postgres. Ou ambas as linhas são commitadas atomicamente, ou nenhuma é. O dual-write desapareceu — não porque ficou atômico, mas porque **deixou de ser dual**.

O preço é que a publicação no broker virou **assíncrona**. O evento está garantidamente na tabela, mas ainda não no Kafka. Quem o leva até lá é o relay. E como o relay pode crashar depois de publicar mas antes de marcar a linha como enviada, a entrega é fatalmente **at-least-once** — daí a exigência de idempotência no consumo (ver [[03-Dominios/Tecnologia/Java/Mensageria/20 - Idempotência — o pilar do at-least-once|Idempotência]]).

> [!note] Não estamos re-explicando o `@Transactional`
> O `@Transactional` acima é o mesmo de sempre: propagação, isolamento, rollback automático em `RuntimeException`. O detalhe que **faz** o Outbox funcionar é apenas que as duas escritas compartilham *a mesma* transação — o resto é o comportamento padrão estudado em [[03-Dominios/Tecnologia/Java/Persistência de dados/12 - Transações operacionais — @Transactional propagação, isolamento, rollback, readOnly|Transações operacionais]].

### CDC com Debezium vs polling publisher

Existem dois jeitos de implementar o relay. A diferença está em **como** ele descobre que há linhas novas na `outbox`.

**Polling publisher.** Um job da própria aplicação varre a tabela periodicamente (`SELECT ... WHERE published = false ORDER BY created_at`), publica cada evento no broker e marca a linha como enviada (ou a deleta). É simples, vive dentro do seu serviço e não exige infraestrutura extra. Em troca, paga o custo de *polling*: latência ligada ao intervalo, carga constante de queries no banco e a necessidade de cuidar de concorrência se houver várias instâncias varrendo a mesma tabela.

**CDC com Debezium.** *Change Data Capture* é log-based: em vez de consultar a tabela, você lê o **log de transações** do próprio banco. O **Debezium** é um conector de CDC (roda sobre o Kafka Connect) que, segundo a documentação oficial:

- no **PostgreSQL**, lê a partir de um **stream de replicação lógica** (o WAL — *write-ahead log* — via *logical decoding*);
- no **MySQL/MariaDB**, lê o **binlog** através de uma biblioteca cliente de replicação.

Cada `INSERT` commitado na `outbox` aparece no log e o Debezium o transforma num evento Kafka — sem nenhuma query de polling, com baixa latência e sem carga adicional de leitura na tabela. O Debezium ainda oferece o **Outbox Event Router**, uma SMT (*single message transformation*) que entende uma `outbox` com colunas convencionais (`id`, `aggregateid`, `aggregatetype`, `payload`, `type`) e roteia cada evento para o tópico certo com base no tipo de agregado — extraindo o `payload` como corpo da mensagem e usando o `aggregateid` como chave Kafka.

| | Polling publisher | CDC (Debezium) |
| --- | --- | --- |
| Como detecta | `SELECT` periódico na tabela | lê o WAL/binlog do banco |
| Latência | ligada ao intervalo de polling | baixa (quase tempo real) |
| Carga no banco | queries recorrentes | mínima (lê o log, não a tabela) |
| Infra extra | nenhuma (vive na app) | Kafka Connect + conector |
| Acoplamento | código de relay na aplicação | externo à aplicação |

CDC é a opção sênior para volume alto e latência baixa; polling é a opção pragmática para começar sem montar um cluster Connect.

## Na prática

A tabela `outbox` segue a convenção que o Debezium Outbox Event Router espera por padrão (`aggregatetype`, `aggregateid`, `type`, `payload`):

```sql
CREATE TABLE outbox (
    id             UUID         PRIMARY KEY DEFAULT gen_random_uuid(),
    aggregatetype  VARCHAR(255) NOT NULL,   -- ex: "Order", "Payment" → roteia o tópico
    aggregateid    VARCHAR(255) NOT NULL,   -- id da entidade → vira a chave Kafka
    type           VARCHAR(255) NOT NULL,   -- ex: "OrderCreated", "PaymentConfirmed"
    payload        JSONB        NOT NULL,   -- o evento serializado
    created_at     TIMESTAMP    NOT NULL DEFAULT now(),
    published      BOOLEAN      NOT NULL DEFAULT false  -- usado só pelo relay de polling
);
```

A entidade JPA correspondente e a escrita transacional, com domínios neutros `Order`/`Payment`:

```java
@Entity
@Table(name = "outbox")
class OutboxEvent {
    @Id
    private UUID id = UUID.randomUUID();
    private String aggregatetype;   // "Order"
    private String aggregateid;     // pedido.getId()
    private String type;            // "OrderCreated"
    @Column(columnDefinition = "jsonb")
    private String payload;         // JSON do evento

    // construtor, getters omitidos
}

@Service
class OrderService {

    private final OrderRepository orders;
    private final OutboxRepository outbox;
    private final ObjectMapper mapper;

    @Transactional
    public Order place(Order order) {
        Order saved = orders.save(order);                  // 1. escrita de negócio
        outbox.save(new OutboxEvent(                       // 2. evento, MESMA transação
            "Order",
            saved.getId().toString(),
            "OrderCreated",
            toJson(saved)
        ));
        return saved;
        // commit único: ou as DUAS linhas entram, ou nenhuma
    }
}
```

Esboço de um **relay de polling** (a alternativa sem Debezium), só para tornar concreto o que o CDC faria automaticamente:

```java
@Component
class OutboxPollingRelay {

    private final OutboxRepository outbox;
    private final KafkaTemplate<String, String> kafka;

    @Scheduled(fixedDelay = 1000)
    @Transactional
    public void publishPending() {
        // lê um lote ordenado de eventos ainda não publicados
        List<OutboxEvent> batch = outbox.findTop100ByPublishedFalseOrderByCreatedAt();
        for (OutboxEvent e : batch) {
            // tópico derivado do agregado; chave = aggregateid garante ordenação por entidade
            kafka.send("outbox.event." + e.getAggregatetype().toLowerCase(),
                       e.getAggregateid(),
                       e.getPayload());
            e.markPublished();   // se crashar aqui, republica no próximo ciclo → at-least-once
        }
    }
}
```

Com **Debezium**, esse relay inteiro some: você não escreve código de publicação. Configura um conector apontando para a tabela `outbox`, liga o Outbox Event Router e o WAL/binlog faz o trabalho. A aplicação fica responsável **apenas** pela escrita transacional do bloco anterior.

## Armadilhas

### (1) Publicar no broker dentro do `@Transactional`

A armadilha clássica de quem "quase" entendeu o padrão: manter o `kafkaTemplate.send()` dentro do método `@Transactional`, achando que estar sob a transação o torna seguro.

```java
@Transactional
public void place(Order order) {
    orders.save(order);
    kafka.send("orders", event);   // ❌ ainda é dual-write
}
```

Isso **continua sendo dual-write**. O broker não participa da transação do banco: ele não faz rollback se a transação SQL abortar depois do `send`. Se o `save` ou um trigger posterior falhar e a transação reverter, a mensagem **já saiu** e não volta — evento fantasma. O ponto inteiro do Outbox é que a única escrita externalizada na transação é a linha da `outbox`; nada de broker ali dentro.

### (2) Outbox sem limpeza ou arquivamento

A tabela `outbox` é um *log*, não um estado permanente. Se você só insere e nunca remove, ela cresce sem limite: índices incham, vacuum do Postgres sofre, e uma tabela que deveria ter centenas de linhas "em trânsito" acumula milhões de eventos já entregues.

Estratégias: o relay de polling pode **deletar** a linha após publicar (em vez de só marcar `published = true`); com Debezium é comum a aplicação deletar a linha logo após inserir (o `INSERT` já apareceu no WAL, então o `DELETE` subsequente não perde o evento) ou rodar um job de **arquivamento/purga** periódico para linhas antigas. O importante é tratar retenção como parte do design, não como um problema futuro.

### (3) Relay sem idempotência no consumidor downstream

O Outbox entrega **at-least-once** por construção: tanto o polling quanto o CDC podem reentregar um evento se o relay crashar entre publicar e confirmar o progresso. Logo, o consumidor downstream **vai** ver duplicatas eventualmente.

Se esse consumidor não for idempotente — se processar `PaymentConfirmed` duas vezes debitar duas vezes — o Outbox terá apenas trocado a inconsistência de "evento perdido" pela de "evento processado em dobro". A robustez do padrão depende de fechar essa ponta: o consumidor precisa deduplicar por uma chave de evento estável (o `id` da `outbox` serve bem). Ver [[03-Dominios/Tecnologia/Java/Mensageria/20 - Idempotência — o pilar do at-least-once|Idempotência]].

## Em entrevista

### Frase pronta (inglês)

> The outbox pattern solves the **dual-write problem**: when a service must both persist state to its database and publish an event to a broker, there is no way to make those two writes atomic without two-phase commit — one can succeed while the other fails, leaving the system inconsistent. Instead of writing to both systems, the service writes the event into an `outbox` table **within the same local database transaction** as the business change, so the two writes commit or roll back together. A separate relay then publishes those rows to the broker, either by **polling** the table or via **change data capture** — for example, Debezium reading the database's transaction log (the WAL in Postgres, the binlog in MySQL). Because delivery is at-least-once, the downstream consumer must be **idempotent**.

### Vocabulário

| Termo (EN) | Em uma frase |
| --- | --- |
| Dual-write problem | Escrever em dois sistemas (banco + broker) sem atomicidade entre eles. |
| Transactional outbox | Gravar o evento numa tabela `outbox` na mesma transação do negócio. |
| Message relay | Processo que lê a `outbox` e publica os eventos no broker. |
| Change data capture (CDC) | Captar mudanças lendo o log de transações do banco, não a tabela. |
| Write-ahead log (WAL) / binlog | O log de transações que o Debezium lê (Postgres / MySQL). |
| Polling publisher | Relay que varre a `outbox` periodicamente via `SELECT`. |
| Two-phase commit (2PC/XA) | Coordenação atômica entre recursos distintos — o que o Outbox evita. |
| At-least-once delivery | Garantia de que o evento sai ao menos uma vez (pode duplicar). |

## Veja também

- [[03-Dominios/Tecnologia/Java/Mensageria/index|Mensageria (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Persistência de dados/12 - Transações operacionais — @Transactional propagação, isolamento, rollback, readOnly|Transações operacionais]]
- [[03-Dominios/Tecnologia/Java/Mensageria/13 - Transações e exactly-once no Spring Kafka|Transações e exactly-once no Spring Kafka]]
- [[03-Dominios/Tecnologia/Java/Mensageria/20 - Idempotência — o pilar do at-least-once|Idempotência]]
- [[03-Dominios/Tecnologia/Java/Mensageria/19 - Kafka Connect pela ótica da app|Kafka Connect pela ótica da app]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java|Dicionário de Java]]

## Referências

- Debezium Documentation — **Outbox Event Router** (transformations/outbox-event-router): descreve a SMT, a estrutura da tabela `outbox` (`id`, `aggregateid`, `aggregatetype`, `payload`, `type`) e o roteamento por agregado.
- Debezium Documentation — **Architecture**: o conector MySQL lê o binlog via biblioteca cliente; o conector PostgreSQL lê de um stream de replicação lógica (WAL).
- Chris Richardson, *Microservices Patterns* — capítulos sobre **Transactional Outbox**, **Polling Publisher** e **Transaction Log Tailing**.
- Gunnar Morling, "Reliable Microservices Data Exchange With the Outbox Pattern" (blog da Debezium) — referenciado na própria doc do Outbox Event Router.
