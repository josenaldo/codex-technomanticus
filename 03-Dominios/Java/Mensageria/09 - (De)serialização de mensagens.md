---
title: "(De)serialização de mensagens"
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
  - spring-kafka
aliases:
  - "Kafka serialization deserialization"
  - "JsonSerializer JsonDeserializer"
  - "ErrorHandlingDeserializer"
---

# (De)serialização de mensagens

> [!abstract] TL;DR
> Kafka transporta apenas `byte[]`. Serializers convertem objetos Java em bytes no producer; deserializers fazem o caminho inverso no consumer. O `JsonSerializer`/`JsonDeserializer` do Spring Kafka resolve o caso mais comum, mas exige cuidado com **type headers**, **trusted packages** e o cenário do **poison pill** — mensagem que falha na desserialização e trava o consumer indefinidamente se não houver o `ErrorHandlingDeserializer` na frente.

## O que é

Kafka é agnóstico a formato: cada record é um par de arrays de bytes (chave + valor). A responsabilidade de transformar objetos Java em bytes — e bytes de volta em objetos — pertence ao **serializer** (lado producer) e ao **deserializer** (lado consumer).

O Spring Kafka encapsula as implementações do cliente Kafka (`kafka-clients`) e acrescenta serializadores/desserializadores próprios, incluindo suporte a JSON via Jackson e mecanismos de tratamento de falhas.

## Por que importa

- **Formato errado quebra silenciosamente.** Um consumer com o deserializer errado pode consumir mensagens sem lançar exceção, produzindo lixo no objeto.
- **O poison pill para tudo.** Quando um record não pode ser desserializado, o Kafka não avança o offset — o consumer fica em loop lendo o mesmo record inválido, paralisando toda a partição.
- **Evolução de schema acoplada ao FQCN.** Por padrão, o `JsonDeserializer` usa o nome completo da classe Java como type header. Renomear o pacote no producer quebra todos os consumers existentes.
- **trusted.packages como vetor de ataque.** Aceitar classes arbitrárias via desserialização é a mesma família de risco do Java Object deserialization (embora menos grave em JSON).

## Como funciona

### Serializers e deserializers disponíveis

O cliente Kafka fornece implementações de baixo nível:

| Implementação | Uso |
|---|---|
| `StringSerializer` / `StringDeserializer` | Strings UTF-8 (mais simples, sem metadados) |
| `ByteArraySerializer` / `ByteArrayDeserializer` | Bytes crus; útil quando o formato já vem pronto |
| `BytesSerializer` / `BytesDeserializer` | Wrapper `Bytes` imutável do Kafka |

O Spring Kafka adiciona:

| Implementação | Uso |
|---|---|
| `JsonSerializer` / `JsonDeserializer` | JSON via Jackson; envia type header por padrão |
| `ErrorHandlingDeserializer` | Envelope que captura falhas de desserialização |
| `DelegatingByTypeSerializer` | Roteia para serializer diferente por tipo de objeto |
| `RetryingDeserializer` | Tenta novamente em falhas transitórias |

### Type headers e trusted.packages

Quando o `JsonSerializer` envia uma mensagem, ele inclui por padrão um header HTTP-style no record Kafka:

```
__TypeId__: com.example.pedidos.Pedido
```

O `JsonDeserializer` no consumer lê esse header para saber em qual classe Java desserializar — sem precisar configurar o tipo explicitamente.

**O problema:** o header carrega o FQCN do producer. Se o consumer estiver em outro serviço (ou o pacote for renomeado), o tipo não é encontrado e a desserialização falha.

**Solução idiomática — type mapping:** Ambos os lados mapeiam um token neutro para sua classe local:

```yaml
# producer application.yml
spring:
  kafka:
    producer:
      value-serializer: org.springframework.kafka.support.serializer.JsonSerializer
      properties:
        spring.json.type.mapping: "pedido:com.producer.pedidos.Pedido"
```

```yaml
# consumer application.yml
spring:
  kafka:
    consumer:
      value-deserializer: org.springframework.kafka.support.serializer.JsonDeserializer
      properties:
        spring.json.type.mapping: "pedido:com.consumer.pedidos.Pedido"
        spring.json.trusted.packages: "com.consumer.pedidos"
```

O `trusted.packages` autoriza explicitamente quais pacotes podem ser instanciados durante a desserialização. Definir `spring.json.trusted.packages=*` elimina qualquer restrição e **não deve ser usado em produção**: qualquer classe presente no classpath pode ser instanciada a partir de um record mal-formado.

### ErrorHandlingDeserializer e o poison pill

O `ErrorHandlingDeserializer` é um **wrapper** — ele envolve o deserializer real e intercepta qualquer exceção lançada durante a conversão.

Sem ele, o comportamento padrão do Spring Kafka é lançar `ListenerExecutionFailedException` a cada tentativa de processar o record inválido. Dependendo da política de retry, isso pode manter o consumer preso na mesma mensagem indefinidamente (poison pill).

Com o `ErrorHandlingDeserializer`:
- O record inválido é consumido normalmente (offset avança).
- O payload do record problemático chega ao listener como `null`.
- A exceção original é serializada e colocada em um header especial (`DeserializationExceptionHeader`) que pode ser inspecionado pelo listener ou pelo `DefaultErrorHandler`.

O consumer não trava e pode rotear a mensagem para uma DLT (Dead Letter Topic).

## Na prática

### Configuração básica com JsonDeserializer e type mapping

```java
@Bean
public ConsumerFactory<String, Pedido> consumerFactory() {
    Map<String, Object> props = new HashMap<>();
    props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
    props.put(ConsumerConfig.GROUP_ID_CONFIG, "pedidos-group");

    // Deserializer configurado programaticamente (alternativa ao application.yml)
    JsonDeserializer<Pedido> deserializer = new JsonDeserializer<>(Pedido.class);
    deserializer.addTrustedPackages("com.example.pedidos");
    // Preserva o type header para o listener inspecionar
    deserializer.setRemoveTypeHeaders(false);
    deserializer.setUseTypeMapperForKey(false);

    return new DefaultKafkaConsumerFactory<>(
        props,
        new StringDeserializer(),
        deserializer
    );
}
```

### Envolvendo com ErrorHandlingDeserializer

```java
@Bean
public ConsumerFactory<String, Pedido> consumerFactory() {
    Map<String, Object> props = new HashMap<>();
    props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
    props.put(ConsumerConfig.GROUP_ID_CONFIG, "pedidos-group");
    // Deserializer interno
    props.put(ErrorHandlingDeserializer.VALUE_DESERIALIZER_CLASS,
              JsonDeserializer.class.getName());
    // Tipo padrão quando o type header estiver ausente
    props.put(JsonDeserializer.VALUE_DEFAULT_TYPE,
              "com.example.pedidos.Pedido");
    props.put(JsonDeserializer.TRUSTED_PACKAGES,
              "com.example.pedidos");

    return new DefaultKafkaConsumerFactory<>(
        props,
        new StringDeserializer(),
        new ErrorHandlingDeserializer<>(new JsonDeserializer<>(Pedido.class))
    );
}
```

Equivalente em YAML (Boot 3.x):

```yaml
spring:
  kafka:
    consumer:
      value-deserializer: >
        org.springframework.kafka.support.serializer.ErrorHandlingDeserializer
      properties:
        spring.deserializer.value.delegate.class: >
          org.springframework.kafka.support.serializer.JsonDeserializer
        spring.json.value.default.type: com.example.pedidos.Pedido
        spring.json.trusted.packages: com.example.pedidos
```

### Lendo o header de falha no listener

```java
@KafkaListener(topics = "pedidos")
public void processar(
        @Payload(required = false) Pedido pedido,
        @Header(KafkaHeaders.RECEIVED_TOPIC) String topic,
        ConsumerRecord<String, Pedido> record) {

    if (pedido == null) {
        // Record chegou como null — falha de desserialização
        byte[] exceptionBytes = (byte[]) record.headers()
            .lastHeader(SerializationUtils.VALUE_DESERIALIZER_EXCEPTION_HEADER)
            .value();
        DeserializationException ex =
            SerializationUtils.byteArrayToDeserializationException(log, exceptionBytes);
        // encaminhar para DLT ou logar e seguir
        return;
    }
    // processamento normal
}
```

> [!note] Ponte para Avro
> Para contratos formais entre serviços (especialmente com múltiplos consumers ou times diferentes), o JSON com type mapping ainda acopla ao formato Java. A nota [[03-Dominios/Java/Mensageria/14 - Schema e contratos — Avro e Schema Registry|Schema e contratos]] aborda Avro + Schema Registry como alternativa evolutível com validação centralizada.

## Armadilhas

### (1) Poison pill parando o consumer indefinidamente

Sem o `ErrorHandlingDeserializer`, qualquer record cujo payload não possa ser convertido para o tipo esperado faz o consumer entrar em loop. O offset não avança porque a exceção é lançada **antes** do listener ser chamado — logo, os mecanismos de erro do listener (como `DefaultErrorHandler`) não chegam a ser acionados.

**Solução:** Sempre usar `ErrorHandlingDeserializer` como wrapper em ambientes de produção, combinado com uma DLT para isolar os records inválidos.

### (2) trusted.packages=* em produção

Aceitar qualquer classe do classpath é equivalente a desabilitar a verificação de tipo. Um atacante com acesso ao broker pode injetar records com headers apontando para classes sensíveis.

**Solução:** Listar explicitamente apenas os pacotes que o consumer precisa instanciar. Em ambientes internos controlados o risco é menor, mas a boa prática é sempre ser restritivo.

### (3) Acoplar ao FQCN do producer

Quando o type mapping não é configurado, o header `__TypeId__` carrega o nome completo da classe do producer (por exemplo, `com.meuprojeto.producer.eventos.PedidoCriado`). Qualquer renomeação de pacote ou classe no producer quebra imediatamente todos os consumers — sem aviso em tempo de compilação.

**Solução:** Sempre configurar `spring.json.type.mapping` com tokens neutros em ambos os lados. O token (`pedido-criado`, `order-created`, etc.) torna-se o contrato, não o nome da classe.

## Em entrevista

### Frase pronta (inglês)

"If a Kafka record can't be deserialized, what happens by default, and how do you prevent the consumer from getting stuck?"

"By default, the deserialization exception is thrown before the listener is invoked, so the offset doesn't advance and the consumer keeps retrying the same record — that's the poison-pill scenario. The standard fix in Spring Kafka is to wrap the real deserializer with `ErrorHandlingDeserializer`. When deserialization fails, the wrapper catches the exception, delivers a null payload to the listener, and attaches the exception to a record header. The listener can then inspect that header and route the record to a dead-letter topic instead of blocking the partition."

### Vocabulário

| Termo EN | Termo PT-BR |
|---|---|
| serializer / deserializer | serializador / desserializador |
| poison pill | mensagem envenenada |
| type header | header de tipo |
| trusted packages | pacotes autorizados |
| dead-letter topic (DLT) | tópico de mensagens mortas |
| offset | posição de leitura na partição |

## Veja também

- [[03-Dominios/Java/Mensageria/index|Mensageria (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Mensageria/14 - Schema e contratos — Avro e Schema Registry|Schema e contratos]]
- [[03-Dominios/Java/Web e APIs REST/05 - Serialização JSON com Jackson|Serialização JSON com Jackson]]
- [[03-Dominios/Java/Mensageria/11 - Tratamento de erro no consumo|Tratamento de erro no consumo]]
- [[03-Dominios/Java/Dicionário de Java|Dicionário de Java]]

## Referências

- Spring for Apache Kafka — Reference Documentation: [Serialization/Deserialization](https://docs.spring.io/spring-kafka/reference/kafka/serdes.html)
- `ErrorHandlingDeserializer` Javadoc: `org.springframework.kafka.support.serializer.ErrorHandlingDeserializer`
- `JsonSerializer` / `JsonDeserializer` Javadoc: `org.springframework.kafka.support.serializer`
