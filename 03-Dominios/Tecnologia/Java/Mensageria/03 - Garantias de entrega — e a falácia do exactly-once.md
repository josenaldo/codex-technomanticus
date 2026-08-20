---
title: "Garantias de entrega — e a falácia do exactly-once"
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
  - eventos
aliases:
  - "Delivery guarantees"
  - "Exactly-once"
---

# Garantias de entrega — e a falácia do exactly-once

> [!abstract] TL;DR
> Existem três garantias de entrega: **at-most-once** (pode perder), **at-least-once** (pode duplicar) e **exactly-once** (uma vez só). Mas a entrega distribuída ponta-a-ponta é, na prática, **at-least-once**. O *efeito* exactly-once não vem de uma config mágica — vem de **idempotência no consumidor**. O EOS (exactly-once semantics) do Kafka existe e é real, mas só cobre o que acontece **dentro do Kafka**; ele não cuida dos seus *side-effects* externos (gravar num banco, chamar uma API). Logo: "configurei exactly-once" nunca dispensa o consumidor de ser idempotente.

## O que é

Garantia de entrega é o **contrato** que o sistema de mensageria oferece sobre quantas vezes uma mensagem chega ao seu destino quando algo falha (rede cai, broker reinicia, consumidor morre no meio do processamento). São três níveis clássicos:

- **At-most-once** — a mensagem chega **zero ou uma vez**. Nunca duplica, mas pode se perder.
- **At-least-once** — a mensagem chega **uma ou mais vezes**. Nunca se perde, mas pode duplicar.
- **Exactly-once** — a mensagem chega **exatamente uma vez**. Não se perde nem duplica.

A definição é sobre o que acontece **diante de falha**. Sem falha alguma, qualquer sistema entrega "uma vez". O nível de garantia descreve para onde o sistema escorrega quando o caminho feliz quebra.

## Por que importa

A garantia de entrega não é um detalhe de tuning: ela **define toda a sua estratégia de confiabilidade**. Cada nível impõe um custo a quem escreve o código:

- Se o sistema é **at-most-once**, você aceita perder eventos — só serve para telemetria descartável.
- Se é **at-least-once** (o caso prático da maioria), você **tem** que projetar o consumidor para tolerar duplicatas. A duplicata não é um bug raro: é o comportamento garantido sob falha.
- Se você acredita ter **exactly-once de graça**, você vai escrever um consumidor ingênuo, ele vai processar a mesma mensagem duas vezes num retry, e o cliente vai ser cobrado em dobro.

Entender o nível real (e não o prometido pelo marketing) é o que separa um sistema de eventos confiável de um que corrompe dados silenciosamente.

## Como funciona

A garantia depende de **quando você confirma (commit) o consumo** em relação a **quando você processa** a mensagem. Essa ordem é a chave de tudo.

> [!note] Internals do Kafka
> Aqui tratamos das *semânticas*, não dos mecanismos do broker. Para offset, commit e como o consumidor confirma posição, veja a nota dedicada do galho (linkada em **Veja também**); para o lado transacional, veja [[03-Dominios/Tecnologia/Java/Mensageria/13 - Transações e exactly-once no Spring Kafka|Transações e exactly-once no Spring Kafka]].

### At-most-once — commit antes de processar (pode perder)

O consumidor **confirma o consumo primeiro** e processa depois:

```text
1. recebe a mensagem
2. commit do offset   <- "já dei como lida"
3. processa a mensagem
```

Se o processo morre **entre o passo 2 e o 3**, a mensagem já foi marcada como consumida mas nunca foi processada. Ela **se perde** e não volta. Em troca, você nunca processa nada duas vezes. É a garantia mais fraca; serve para dados onde perder um evento é tolerável.

### At-least-once — processa antes do commit (pode duplicar; o DEFAULT prático)

O consumidor **processa primeiro** e só confirma depois:

```text
1. recebe a mensagem
2. processa a mensagem
3. commit do offset   <- "agora sim, terminei"
```

Se o processo morre **entre o passo 2 e o 3**, o offset **não** foi confirmado. Ao reiniciar, o consumidor lê a mesma mensagem de novo e a **processa novamente** — duplicata. Nada se perde, mas pode haver repetição.

Este é o **default prático** de praticamente todo sistema de eventos sério, porque perder dado costuma ser pior do que reprocessar. A consequência é direta: **se o seu sistema é at-least-once, o consumidor precisa ser idempotente.** Não é opcional.

### Exactly-once e a falácia

A garantia desejada por todo mundo. O problema é que, numa entrega **distribuída ponta-a-ponta**, ela é essencialmente impossível de obter só com configuração — porque o consumidor e o produtor podem falhar **fora** do alcance do sistema de mensageria. A própria documentação é honesta sobre isso:

> "Many systems claim to provide exactly once delivery semantics, but this might not always be what you think it is. For example, these systems may not account for cases where a consumer or producer **outside of the system** has failed."

Onde isso desmorona na prática: o consumidor processa a mensagem com sucesso, vai confirmar o offset, e **morre antes do commit**. No reinício, recebe a mesma mensagem. Do ponto de vista da entrega, **isso é at-least-once** — e é o melhor que a rede te dá. **Retry duplica** por construção: a única forma de garantir que algo chegou é reenviar quando você não recebeu o ACK, e às vezes o ACK se perdeu mas a mensagem chegou. Reenviar ⇒ duplicata.

A saída não é uma flag. É **idempotência no consumidor**: projetar o processamento para que aplicar a mesma mensagem N vezes tenha o mesmo efeito que aplicá-la uma vez (ver [[03-Dominios/Tecnologia/Java/Mensageria/20 - Idempotência — o pilar do at-least-once|Idempotência]]). Você não impede a duplicata de **chegar**; você faz a duplicata ser **inofensiva**. O resultado observável é "processado uma vez" — o **efeito** exactly-once — construído sobre uma entrega que continua sendo at-least-once.

**E o EOS do Kafka, então?** Ele existe e é real — idempotent producer + transações conseguem garantir exactly-once **dentro** do Kafka, no laço *consume → process → produce* onde tudo (mensagens de saída **e** offsets de entrada) é escrito atomicamente em tópicos do próprio Kafka. Mas o escopo é justamente esse: **só o que está dentro do Kafka.** Como diz o blog da Confluent:

> "if the event streaming app [...] makes an RPC call to update some remote stores, or if it uses a customized client to directly read or write to a Kafka topic, the resulting side effects would not be guaranteed exactly once."

Ou seja: gravar num banco externo, chamar uma API de terceiros, enviar um e-mail — **esses side-effects não estão cobertos pelo EOS.** Para eles, você está de volta ao at-least-once + idempotência. Essa é a falácia: achar que ligar o EOS te dá exactly-once para o mundo todo. Ele te dá para o jardim murado do Kafka, e só.

> [!info] Ordering: por partição, não global
> A ordem das mensagens é garantida **dentro de uma partição**, não através do tópico inteiro. Mensagens que precisam ser ordenadas entre si têm que cair na mesma partição (em geral via chave). Isso interage com duplicatas: um retry pode não só duplicar, mas, sem cuidado, reordenar — outra razão para idempotência tratar o estado, não a sequência de chegada.

## Na prática

Imagine um consumidor que recebe um `OrderPlacedEvent` e, ao processá-lo, **debita o estoque** e **cobra o cartão**:

```text
Evento: OrderPlacedEvent { orderId: "A-1001", itens: [...], total: 250 }

Consumidor (ingênuo, at-least-once sem proteção):
  1. processa OrderPlacedEvent
  2. debita estoque + cobra R$250 no cartão   <- side-effect externo
  3. commit do offset
```

Se o consumidor morre **entre o passo 2 e o 3**, no reinício ele recebe o **mesmo** `OrderPlacedEvent` de novo. Resultado: estoque debitado duas vezes e cliente cobrado **R$500**. Nenhuma config de exactly-once do broker salva isso, porque a cobrança é um **side-effect externo** — fora do escopo do EOS.

A correção é idempotência: usar o `orderId` (ou um ID de evento) como **chave de deduplicação** antes de aplicar o efeito.

```text
Consumidor idempotente:
  1. recebe OrderPlacedEvent { orderId: "A-1001" }
  2. JÁ processei "A-1001"?  -> se sim, ignora (no-op) e faz commit
  3. se não: debita estoque + cobra, registra "A-1001" como processado
  4. commit do offset
```

Agora a duplicata **chega** (a entrega continua at-least-once), mas o segundo processamento é um **no-op**. O efeito observável é "cobrado uma vez". Esse é o exactly-once que existe de verdade no mundo: at-least-once + consumidor idempotente.

## Armadilhas

### (1) Achar que "exactly-once" configurado dispensa idempotência

A armadilha mais cara. Você liga o EOS no Kafka, lê "exactly-once" na config e conclui que o consumidor pode ser ingênuo. Errado: o EOS cobre o laço **interno** do Kafka, não os seus side-effects externos (banco, API, e-mail). No momento em que o seu processamento toca qualquer coisa fora do Kafka, você está de volta ao at-least-once. **A idempotência no consumidor é a defesa real e ela continua obrigatória**, com ou sem EOS ligado.

### (2) Assumir que retry não duplica

Retry **duplica por construção**. A entrega confiável funciona reenviando a mensagem quando o ACK não chega — mas o ACK pode ter se perdido **depois** de a mensagem ter sido entregue. O remetente não tem como distinguir "não chegou" de "chegou mas o ACK se perdeu"; na dúvida, reenvia. Qualquer raciocínio que assuma "se deu retry é porque a primeira falhou" está errado. Projete contando com a duplicata, não rezando contra ela.

## Em entrevista

### Frase pronta (inglês)

> "There are three delivery guarantees: at-most-once, where messages may be lost but never duplicated; at-least-once, where messages are never lost but may be duplicated; and exactly-once. In a distributed end-to-end system, true exactly-once delivery is a myth — the network gives you at-least-once, because any retry can duplicate. What you actually achieve is at-least-once delivery plus idempotent consumers, so duplicates arrive but are harmless. Kafka's exactly-once semantics are real, but they only cover what happens inside Kafka; external side-effects like writing to a database still require idempotency on the consumer side."

### Vocabulário

| Português | Inglês |
| --- | --- |
| entrega | delivery |
| duplicata | duplicate |
| perda (de mensagem) | (message) loss |
| idempotência | idempotency |
| semântica (de entrega) | (delivery) semantics |
| garantia | guarantee |
| efeito colateral | side-effect |
| desduplicação | deduplication |

## Veja também

- [[03-Dominios/Tecnologia/Java/Mensageria/index|Mensageria (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Mensageria/20 - Idempotência — o pilar do at-least-once|Idempotência]]
- [[03-Dominios/Tecnologia/Java/Mensageria/13 - Transações e exactly-once no Spring Kafka|Transações e exactly-once no Spring Kafka]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java|Dicionário de Java]]

Tópicos correlatos ainda não cobertos: garantias em outros brokers (planejado), padrões de resiliência e DLQ (planejado), observabilidade de pipelines de eventos (planejado).

## Referências

- Apache Kafka — Documentation, *Design › Message Delivery Semantics*: https://kafka.apache.org/documentation/
- Confluent Documentation — *Kafka Design › Delivery Semantics*: https://docs.confluent.io/platform/current/
- Confluent Blog — *Exactly-Once Semantics Are Possible: Here's How Apache Kafka Does It*: https://www.confluent.io/blog/exactly-once-semantics-are-possible-heres-how-apache-kafka-does-it/
