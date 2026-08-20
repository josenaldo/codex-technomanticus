---
title: Ack modes e commit de offset
fase: adepto
tags:
  - java
  - mensageria
  - adepto
  - spring-kafka
  - kafka
created: 2026-06-11
updated: 2026-06-11
type: concept
status: seedling
publish: true
---

# Ack modes e commit de offset

> [!abstract] TL;DR
> O Spring Kafka desativa `enable.auto.commit` e assume o controle do commit de offset via `AckMode`. Os modos vão de automático-por-registro (`RECORD`) até totalmente manual (`MANUAL_IMMEDIATE`). A regra de ouro do at-least-once: **processe primeiro, commite depois**.

## O que é

**Offset** é a posição de leitura de um consumer dentro de uma partição. **Commit de offset** é o ato de registrar no Kafka até qual mensagem o consumer já processou — equivale a dizer "processei até aqui, na próxima reinicialização pode começar do próximo".

O Spring Kafka expõe esse controle através da enum `AckMode`, configurada no container do listener (`ConcurrentKafkaListenerContainerFactory`). Cada modo define *quando* o commit acontece.

## Por que importa

Sem controle explícito de offset, o comportamento do consumer em caso de falha é imprevisível. Commitar cedo demais causa **perda de mensagens** (at-most-once); commitar tarde demais ou nunca causa **reprocessamento** (at-least-once). A escolha do `AckMode` é a principal alavanca para definir a semântica de entrega da sua aplicação.

Além disso, o `enable.auto.commit` nativo do Kafka commita em background a cada `auto.commit.interval.ms` — completamente alheio ao estado do processamento. Por isso o Spring Kafka o desativa por padrão (desde a versão 2.3) para assumir o controle.

## Como funciona

### O que é commit de offset

Cada partição Kafka mantém um cursor por consumer group. Quando o consumer chama `commitSync()` ou `commitAsync()`, ele grava no tópico interno `__consumer_offsets` a posição do próximo registro a ser lido.

Se o consumer reinicia antes de commitar, ele relê a partir do último offset commitado — podendo reprocessar mensagens já tratadas. Esse é o custo do at-least-once: **duplicatas são possíveis, mas perdas não**.

> [!info] Quer entender como o Kafka armazena offsets internamente?
> Veja [[03-Dominios/Tecnologia/Java/Backend/Kafka/Kafka Concepts/12. Consumer Offsets|Consumer Offsets (infra)]] — este documento foca no controle via Spring.

### AckMode no Spring

O Spring Kafka oferece sete modos de acknowledgment. A tabela abaixo usa como referência a documentação oficial (Spring Kafka 4.1):

| AckMode | Quando commita |
|---|---|
| `RECORD` | Imediatamente após cada registro ser processado |
| `BATCH` | Após todos os registros de um `poll()` serem processados (padrão) |
| `TIME` | Após o processamento, se `ackTime` ms já se passou desde o último commit |
| `COUNT` | Após o processamento, se `ackCount` registros foram recebidos desde o último commit |
| `COUNT_TIME` | Se qualquer condição de `TIME` **ou** `COUNT` for satisfeita |
| `MANUAL` | O listener chama `acknowledge()` manualmente; semântica equivalente ao `BATCH` |
| `MANUAL_IMMEDIATE` | O commit ocorre imediatamente quando `acknowledge()` é chamado |

**Por que o Spring desativa o auto-commit?**

A partir da versão 2.3, o Spring Kafka define `enable.auto.commit=false` incondicionalmente — a menos que você o sobrescreva explicitamente no `ConsumerFactory`. Isso é intencional: o auto-commit do Kafka roda em uma thread separada, sem conhecimento do estado do processamento, e tornaria todos os modos acima ineficazes.

### At-least-once na prática

A regra central é: **execute o processamento antes de commitar o offset**.

```
poll() → processa registro → commit offset
```

Se a aplicação crashar entre o poll e o commit, o registro será relido no próximo reinício — gerando uma duplicata, mas **nunca uma perda**. Isso é at-least-once.

**Commit síncrono vs assíncrono** (`syncCommits`, padrão `true`):

- **Síncrono**: bloqueia até o broker confirmar. Mais lento, mas garante que o commit foi efetivado antes de continuar.
- **Assíncrono**: dispara o commit e segue em frente. Mais rápido, mas uma falha antes da confirmação pode reprocessar registros que pareciam commitados. Use `commitCallback` para tratar erros assíncronos.

## Na prática

### Configuração com `AckMode.MANUAL_IMMEDIATE`

```yaml
# application.yml
spring:
  kafka:
    listener:
      ack-mode: manual_immediate
    consumer:
      group-id: meu-grupo
      auto-offset-reset: earliest
      # enable-auto-commit NÃO deve ser definido aqui — Spring gerencia
```

```java
// Configuração do container factory
@Bean
public ConcurrentKafkaListenerContainerFactory<String, PedidoEvent> kafkaListenerContainerFactory(
        ConsumerFactory<String, PedidoEvent> consumerFactory) {

    var factory = new ConcurrentKafkaListenerContainerFactory<String, PedidoEvent>();
    factory.setConsumerFactory(consumerFactory);
    factory.getContainerProperties().setAckMode(ContainerProperties.AckMode.MANUAL_IMMEDIATE);
    return factory;
}
```

```java
// Listener com acknowledgment manual
@KafkaListener(topics = "pedidos", groupId = "meu-grupo")
public void processar(PedidoEvent evento, Acknowledgment ack) {
    try {
        processarPedido(evento);  // processa ANTES
        ack.acknowledge();        // commita DEPOIS
    } catch (Exception e) {
        // NÃO chama ack.acknowledge() — offset não é commitado
        // O registro será relido na próxima reinicialização
        log.error("Falha ao processar pedido {}", evento.id(), e);
        throw e;
    }
}
```

> [!tip] Interface `AcknowledgingMessageListener`
> Para usar `Acknowledgment`, o listener deve receber o parâmetro na assinatura do método. O Spring injeta automaticamente quando o `AckMode` é `MANUAL` ou `MANUAL_IMMEDIATE`.

### Quando usar cada modo

| Cenário | Modo recomendado |
|---|---|
| Processamento simples, baixa criticidade | `BATCH` (padrão) |
| Controle fino por registro, sem transação | `MANUAL_IMMEDIATE` |
| Processamento em lote com commit ao fim | `MANUAL` |
| Reduzir overhead de commits em alto volume | `COUNT` ou `TIME` |

## Armadilhas

### (1) `enable.auto.commit` ativado com processamento assíncrono

Se você sobrescrever `enable.auto.commit=true` no `ConsumerFactory`, o Kafka committará offsets em background a cada `auto.commit.interval.ms` — independentemente de o processamento ter terminado. Se o processamento for assíncrono (ex.: envio a outro serviço), o offset pode ser commitado antes da confirmação de entrega, **quebrando a garantia de at-least-once** silenciosamente.

> [!danger] Regra
> Nunca ative `enable.auto.commit` quando o processamento tiver efeitos colaterais externos (banco, HTTP, outro tópico). Deixe o Spring gerenciar.

### (2) Commitar ANTES de processar — at-most-once acidental

```java
// ERRADO — at-most-once: se processarPedido() lançar exceção, a mensagem é perdida
@KafkaListener(topics = "pedidos")
public void processar(PedidoEvent evento, Acknowledgment ack) {
    ack.acknowledge();        // commit ANTES
    processarPedido(evento);  // processa DEPOIS — se crashar, perda garantida
}
```

Commitar antes de processar transforma at-least-once em **at-most-once**: uma falha pós-commit significa que o registro nunca será relido. Em sistemas financeiros ou de auditoria, isso equivale a perda de dados.

### (3) `AckMode.MANUAL` sem chamar `acknowledge()`

```java
// ERRADO — reprocesso infinito
@KafkaListener(topics = "pedidos")
public void processar(PedidoEvent evento, Acknowledgment ack) {
    processarPedido(evento);
    // ack.acknowledge() esquecido!
    // O offset nunca é commitado — na reinicialização, relê do início
}
```

Com `MANUAL` ou `MANUAL_IMMEDIATE`, esquecer de chamar `acknowledge()` faz com que o consumer nunca avance o offset. No reinício, ele relê todas as mensagens desde o último commit gravado. Em ambientes com retenção longa, isso pode significar reprocessar dias de histórico.

## Em entrevista

### Frase pronta (inglês)

- *"Spring Kafka takes over offset management by setting `enable.auto.commit` to false and exposing the `AckMode` abstraction."*
- *"With `MANUAL_IMMEDIATE`, the offset is committed right when `acknowledge()` is called, giving fine-grained control at the record level."*
- *"The golden rule for at-least-once is: process first, commit after — never the other way around."*
- *"Committing before processing accidentally turns at-least-once into at-most-once, which means data loss on crashes."*

### Vocabulário

| Termo | Significado resumido |
|---|---|
| `AckMode` | Enum que controla quando o Spring commita offsets |
| `enable.auto.commit` | Propriedade nativa do Kafka que o Spring desativa |
| at-least-once | Semântica que tolera duplicatas mas não perdas |
| at-most-once | Semântica que tolera perdas mas não duplicatas |
| `Acknowledgment` | Interface Spring para commit manual de offset |
| `syncCommits` | Flag que controla se o commit bloqueia até confirmação |
| `__consumer_offsets` | Tópico interno do Kafka que armazena offsets commitados |

## Veja também

- [[03-Dominios/Tecnologia/Java/Mensageria/index|Mensageria (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Backend/Kafka/Kafka Concepts/12. Consumer Offsets|Consumer Offsets (infra)]]
- [[03-Dominios/Tecnologia/Java/Mensageria/08 - @KafkaListener — consumindo mensagens|@KafkaListener]]
- [[03-Dominios/Tecnologia/Java/Mensageria/11 - Tratamento de erro no consumo|Tratamento de erro no consumo]]
- [[03-Dominios/Tecnologia/Java/Mensageria/03 - Garantias de entrega — e a falácia do exactly-once|Garantias de entrega]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java|Dicionário de Java]]

## Referências

- [Spring Kafka — Message Listener Containers](https://docs.spring.io/spring-kafka/reference/kafka/receiving-messages/message-listener-container.html)
- [Spring Kafka — Container Properties](https://docs.spring.io/spring-kafka/reference/kafka/container-props.html)
- [Spring Kafka — Manually Committing Offsets](https://docs.spring.io/spring-kafka/reference/kafka/receiving-messages/ooo-commits.html)
- [Apache Kafka — Consumer Configs (`enable.auto.commit`)](https://kafka.apache.org/documentation/#consumerconfigs_enable.auto.commit)
