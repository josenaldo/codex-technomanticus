---
title: "Idempotência — o pilar do at-least-once"
fase: magus
tags:
  - java
  - mensageria
  - magus
  - idempotencia
created: 2026-06-11
updated: 2026-06-11
type: concept
status: seedling
publish: true
aliases:
  - "Idempotência"
---

# Idempotência — o pilar do at-least-once

> [!abstract] TL;DR
> Sistemas de mensageria reais entregam **at-least-once**: a mesma mensagem pode chegar duas vezes (retry, rebalance, redelivery). Você não conserta isso *na entrega* — conserta no **efeito**. Uma operação é **idempotente** quando aplicá-la N vezes produz o mesmo estado que aplicá-la uma vez. Logo, o consumidor é que carrega o fardo: ou a operação é naturalmente idempotente (upsert, `set status = X`), ou você deduplica por uma **chave de idempotência** persistida. Cuidado com a falsa amizade: o `enable.idempotence=true` do Kafka resolve a duplicação do **produtor em retry** — não tem nada a ver com a duplicação de **entrega** que o consumidor sofre. A frase que fecha entrevista: *você não obtém exactly-once por configuração; você obtém com at-least-once + consumidor idempotente.*

## O que é

Uma operação é **idempotente** quando executá-la repetidas vezes deixa o sistema no mesmo estado final que executá-la uma única vez. `f(f(x)) = f(x)`.

Exemplos do mundo real:
- **Idempotente**: "definir o status do pedido 42 para `PAID`". Rodou uma vez, rodou cinco vezes — o status é `PAID`. Fim.
- **NÃO idempotente**: "adicionar R$ 100 ao saldo". Rodou uma vez, +100. Rodou três vezes, +300. Cada execução muda o resultado.

Em mensageria, isso importa porque a infraestrutura **não promete entrega única**. Ela promete que a mensagem chega *pelo menos* uma vez — e, na prática, às vezes mais. A idempotência é o contrato que o **consumidor** assina para que "pelo menos uma vez" se comporte, do ponto de vista do efeito de negócio, como "exatamente uma vez".

## Por que importa

Esta é a nota-pilar do galho de Mensageria porque ela sustenta a tese honesta sobre garantias de entrega: o famigerado *exactly-once* end-to-end não é um botão que você liga. É uma **propriedade emergente** de dois ingredientes — entrega at-least-once (que o broker te dá) somada a um consumidor idempotente (que *você* constrói).

Sem idempotência no consumidor, at-least-once vira um gerador de bugs silenciosos: o pagamento cobrado duas vezes, o e-mail de boas-vindas enviado em duplicata, o estoque decrementado a mais. O sistema *funciona* na maioria das vezes — até o dia em que um rebalance do consumer group reentrega o último lote de mensagens e o relatório financeiro não bate.

Idempotência é, portanto, o que transforma uma garantia *fraca* da infraestrutura (at-least-once) em uma garantia *forte* do negócio (efeito único), sem a complexidade e o custo das transações distribuídas de exactly-once verdadeiro.

## Como funciona

### Por que at-least-once EXIGE consumidor idempotente

A cadeia de causa e efeito é mecânica. O consumidor faz três coisas, nesta ordem lógica: (1) recebe a mensagem, (2) processa o efeito de negócio, (3) confirma (commit do offset / ack). Se a máquina morre, a rede cai ou o rebalance dispara **entre o passo 2 e o passo 3**, o efeito já aconteceu mas o offset não foi confirmado. O broker, fiel ao at-least-once, **reentrega** a mensagem. O consumidor processa o efeito de novo.

> [!warning] A entrega pode duplicar — o efeito não pode
> Não existe ponto na linha em que você consiga garantir, de forma atômica e gratuita, "processei E confirmei". A janela entre processar e confirmar é onde a duplicata nasce. Você não fecha essa janela com mais configuração de broker; você a torna **inofensiva** fazendo o efeito ser idempotente.

Por isso a frase: at-least-once *exige* consumidor idempotente. Não é recomendação de boas práticas — é a única forma de a duplicata inevitável não virar dano.

### Estratégias de deduplicação

Há duas grandes famílias de solução.

**1. Operações naturalmente idempotentes.** Quando o efeito de negócio já é idempotente por natureza, você não precisa deduplicar nada — só escrever a operação certa:

| Operação | Idempotente? | Por quê |
|---|---|---|
| `UPDATE order SET status = 'PAID'` | Sim | Reprocessar reescreve o mesmo valor |
| `UPSERT` (insert-or-update por PK) | Sim | A segunda vez vira update no mesmo registro |
| `SET saldo = 500` (valor absoluto) | Sim | Estado final independe de quantas vezes roda |
| `balance = balance + 100` (incremento) | **Não** | Cada execução acumula |
| `INSERT` de um evento de auditoria | **Não** | Cada execução cria uma linha nova |
| Enviar e-mail / chamar API externa | **Não** | Efeito colateral irreversível e acumulativo |

A regra mental: **set absoluto é idempotente; delta relativo não é**.

**2. Chave de idempotência + tabela de dedup.** Quando a operação *não* é naturalmente idempotente (incremento, insert, efeito externo), você adiciona uma camada explícita de deduplicação. Cada mensagem carrega uma **chave de idempotência** estável (um `messageId`, `eventId`, ou hash do payload). Antes de processar, o consumidor pergunta: "já vi essa chave?". Se sim, descarta. Se não, processa e registra a chave.

A forma mais limpa de tornar esse "registra a chave" atômico com o processamento é usar uma restrição de unicidade no banco e deixar o próprio banco rejeitar a duplicata:

```sql
INSERT INTO processed_messages (idempotency_key, processed_at)
VALUES ('evt-abc-123', now())
ON CONFLICT (idempotency_key) DO NOTHING;
```

Se o `INSERT` afetou 0 linhas, a chave já existia — a mensagem é duplicata e você pula o efeito. Se afetou 1 linha, é a primeira vez — você prossegue. Idealmente o `INSERT` da chave e a escrita de negócio acontecem na **mesma transação** de banco, para que ou ambos comitam ou ambos revertem.

### Idempotent producer (`enable.idempotence=true`)

Aqui mora a confusão mais comum em entrevistas. O Kafka tem uma feature chamada **idempotent producer**, ligada pelo config `enable.idempotence=true` (default `true` nos produtores modernos, desde o Kafka 3.0). Ela resolve um problema **completamente diferente** da dedup do consumidor.

O cenário do produtor: ele envia uma mensagem, o broker grava, mas o **ack se perde na volta**. O produtor, achando que falhou, **reenvia**. Sem idempotência, isso grava a mensagem **duas vezes na partição** — uma duplicata criada pelo *retry do produtor*, antes mesmo de qualquer consumidor existir.

O idempotent producer fecha essa porta: o produtor anexa um `producerId` e um número de sequência a cada mensagem, e o broker descarta sequências repetidas. Resultado: cada produção lógica resulta em **exatamente uma** gravação na partição, mesmo com retries de rede. A documentação do Confluent confirma os requisitos que acompanham essa garantia — `acks=all` e `retries > 0` (e ordenação preservada via `max.in.flight.requests.per.connection`).

> [!important] Dois problemas, dois donos
> O idempotent producer protege contra **duplicação na gravação por retry do produtor**. Ele NÃO protege contra **duplicação na entrega ao consumidor** (rebalance, redelivery, reprocessamento). Mesmo com `enable.idempotence=true`, seu consumidor ainda precisa ser idempotente. São camadas distintas do pipeline — confundi-las é o erro clássico.

## Na prática

Consumidor de pagamentos em Spring Kafka, deduplicando por chave numa tabela. O efeito ("registrar pagamento") **não** é naturalmente idempotente — então usamos chave de idempotência + `ON CONFLICT`.

```java
@Component
public class PaymentConsumer {

    private final JdbcTemplate jdbc;

    public PaymentConsumer(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @KafkaListener(topics = "payments", groupId = "payment-processor")
    @Transactional // dedup + efeito de negócio na MESMA transação de banco
    public void onPayment(PaymentEvent event) {
        // 1) Tenta reservar a chave de idempotência.
        int inserted = jdbc.update("""
            INSERT INTO processed_messages (idempotency_key, processed_at)
            VALUES (?, now())
            ON CONFLICT (idempotency_key) DO NOTHING
            """, event.eventId());

        // 2) Se 0 linhas, já processamos esta mensagem antes: é duplicata.
        if (inserted == 0) {
            // Idempotente: não cobra de novo, apenas confirma o offset.
            return;
        }

        // 3) Primeira vez: aplica o efeito de negócio.
        jdbc.update("""
            INSERT INTO payments (order_id, amount, status)
            VALUES (?, ?, 'CONFIRMED')
            """, event.orderId(), event.amount());
    }
}
```

Tabela de deduplicação. Repare no `created_at` — ele existe para a limpeza (TTL), não por decoração:

```sql
CREATE TABLE processed_messages (
    idempotency_key VARCHAR(255) PRIMARY KEY,  -- UNIQUE garante a dedup
    processed_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Job periódico de limpeza: descarta chaves além da janela de redelivery plausível.
DELETE FROM processed_messages
WHERE processed_at < now() - INTERVAL '7 days';
```

Quando o efeito *é* naturalmente idempotente, nada disso é necessário — basta escrever o upsert e deixar a duplicata reescrever o mesmo estado:

```sql
-- Idempotente por natureza: reprocessar reescreve o mesmo status.
UPDATE orders SET status = 'PAID', paid_at = ? WHERE id = ?;
```

## Armadilhas

### (1) Consumidor não-idempotente em at-least-once

Tratar at-least-once como se fosse exactly-once. O consumidor faz um `balance = balance + amount` ou um `INSERT` cru, sem chave de dedup, e tudo parece funcionar nos testes. Em produção, um rebalance reentrega o lote e o cliente é **cobrado duas vezes**. É o bug mais caro e mais silencioso da mensageria: não quebra nada, só corrompe o estado de negócio devagar. Toda operação não-idempotente num consumidor at-least-once é uma duplicata esperando acontecer.

### (2) Tabela de dedup sem TTL/limpeza

Você acerta a dedup com `ON CONFLICT`, mas esquece que a tabela `processed_messages` **cresce para sempre**. Cada mensagem já processada deixa uma linha eterna. Em meses, são bilhões de linhas, o índice da PK incha, o `INSERT ... ON CONFLICT` fica lento, e a dedup vira o gargalo do consumidor. A correção é um TTL: chaves além da janela de redelivery plausível (horas, dias) podem ser apagadas, porque o broker não vai reentregar algo tão antigo. Dedup sem janela de expiração é vazamento de armazenamento disfarçado de correção.

### (3) Confundir idempotent producer com idempotência do consumidor

Ligar `enable.idempotence=true`, ver "idempotence" no nome e concluir que o pipeline está protegido contra duplicatas. Não está. O idempotent producer só impede a duplicação **na gravação por retry do produtor**; ele é cego para a duplicação **na entrega ao consumidor**. Você pode ter o produtor idempotente perfeitamente configurado e ainda cobrar o cliente duas vezes, porque o consumidor reprocessou após um rebalance. São camadas independentes — uma não substitui a outra.

## Em entrevista

### Frase pronta (inglês)

> In any real messaging system, delivery is at-least-once — the same message can arrive more than once after a retry, a rebalance, or a redelivery. The honest truth is that **you don't achieve exactly-once by configuration; you achieve it with at-least-once delivery plus idempotent consumers.** So I design the consumer's side effect to be idempotent: either the operation is naturally idempotent, like an upsert or setting an absolute value, or I deduplicate using a stable idempotency key persisted in a table with a unique constraint and `ON CONFLICT DO NOTHING`. One subtlety I always flag is that Kafka's `enable.idempotence` on the producer is a different concern — it prevents duplicate *writes* from producer retries, not duplicate *processing* on the consumer side. Those are two distinct layers of the pipeline, and conflating them is a classic mistake.

### Vocabulário

| Termo | Significado |
|---|---|
| Idempotency key | Identificador estável da mensagem (`eventId`, `messageId`) usado para detectar reprocessamento |
| Deduplication table | Tabela que registra chaves já processadas; a restrição de unicidade barra a duplicata |
| At-least-once | Garantia de entrega em que a mensagem chega uma ou mais vezes (nunca zero) |
| Effective / de-facto exactly-once | Comportamento de efeito único alcançado por at-least-once + consumidor idempotente |
| Idempotent producer | Feature do Kafka (`enable.idempotence`) que evita gravações duplicadas por retry do produtor |
| Side effect | Efeito observável da operação (cobrança, e-mail, escrita); o que precisa ser idempotente |
| Natural idempotency | Propriedade de operações como upsert ou `set` absoluto, idempotentes sem dedup explícita |

## Veja também

- [[03-Dominios/Tecnologia/Java/Mensageria/index|Mensageria (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Mensageria/03 - Garantias de entrega — e a falácia do exactly-once|Garantias de entrega]]
- [[03-Dominios/Tecnologia/Java/Mensageria/13 - Transações e exactly-once no Spring Kafka|Transações e exactly-once no Spring Kafka]]
- [[03-Dominios/Tecnologia/Java/Mensageria/21 - O padrão Outbox|O padrão Outbox]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java|Dicionário de Java]]

## Referências

- [Apache Kafka — Documentation (Producer Configs)](https://kafka.apache.org/documentation/) — `enable.idempotence`, requisitos de `acks` e `retries`.
- [Confluent Platform — Producer Configuration Reference](https://docs.confluent.io/platform/current/installation/configuration/producer-configs.html) — idempotência requer `acks=all` e `retries > 0`.
- Galhos 15/16/17/18 da trilha de Mensageria: (planejado).
