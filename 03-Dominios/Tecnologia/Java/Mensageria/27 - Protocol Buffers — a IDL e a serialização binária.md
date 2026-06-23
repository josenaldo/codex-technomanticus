---
title: "Protocol Buffers — a IDL e a serialização binária"
created: 2026-06-11
updated: 2026-06-11
type: concept
status: seedling
publish: true
fase: magus
tags:
  - java
  - mensageria
  - magus
  - protobuf
  - grpc
aliases:
  - "Protocol Buffers"
  - "protobuf"
---

# Protocol Buffers — a IDL e a serialização binária

> [!abstract] TL;DR
> Protocol Buffers (protobuf) é a IDL e o formato de serialização binária do Google: você descreve dados em arquivos `.proto`, roda o compilador `protoc` para gerar código Java fortemente tipado, e obtém payloads até dez vezes menores que JSON com parse mais rápido. A identidade de cada campo na wire format é o **field number** — não o nome —, o que torna a evolução de schema controlada: adicione campos novos com números novos, reserve os removidos e nunca reutilize um número.

---

## O que é

**Protocol Buffers** (protobuf) é a linguagem de definição de interface (IDL) e o mecanismo de serialização binária desenvolvido pelo Google e disponibilizado como open source. Um schema protobuf vive em um arquivo `.proto`, que é compilado pelo `protoc` para gerar código nativo em diversas linguagens — incluindo Java.

O formato atual é **proto3**, que simplificou o proto2: todos os campos são opcionais por padrão (presença implícita), enums começam obrigatoriamente em zero, e a codificação `packed` é automática para campos numéricos repetidos.

Protobuf é o formato de serialização padrão do **gRPC**, mas também é usado de forma independente em tópicos Kafka, filas de mensagens e APIs REST binárias.

---

## Por que importa

Em sistemas distribuídos Java de nível sênior, protobuf aparece em três contextos frequentes:

1. **gRPC** — todo contrato de serviço gRPC é definido em proto3; o `protoc` gera stubs Java para client e server.
2. **Kafka com contratos binários** — o Confluent Schema Registry aceita schemas Protobuf ao lado de Avro, com compatibilidade versionada.
3. **APIs internas de alta frequência** — onde o overhead de JSON (parsing textual, ausência de tipos nativos) é inaceitável.

Comparando com as alternativas:

| Formato | Tipagem | Tamanho | Schema obrigatório | Legível por humanos |
|---|---|---|---|---|
| JSON | Dinâmica | Grande | Não | Sim |
| Avro | Forte | Pequeno | Sim (em runtime) | Parcialmente |
| **Protobuf** | **Forte** | **Muito pequeno** | **Sim (em compilação)** | Não |

A geração de código em tempo de compilação elimina toda uma classe de bugs de contratos implícitos.

---

## Como funciona

### A IDL proto3

Um arquivo `.proto` declara um `package`, opções de geração de código Java e as definições de `message` e `enum`:

```protobuf
syntax = "proto3";

package br.com.exemplo.pedido;

option java_package = "br.com.exemplo.pedido.proto";
option java_multiple_files = true;
option java_outer_classname = "PedidoProtos";

enum StatusPedido {
  STATUS_PEDIDO_UNSPECIFIED = 0;
  STATUS_PEDIDO_PENDENTE    = 1;
  STATUS_PEDIDO_PAGO        = 2;
  STATUS_PEDIDO_CANCELADO   = 3;
}

message ItemPedido {
  string produto_id = 1;
  int32  quantidade  = 2;
  double preco_unit  = 3;
}

message Pedido {
  string                 pedido_id   = 1;
  string                 cliente_id  = 2;
  repeated ItemPedido    itens       = 3;
  StatusPedido           status      = 4;
  map<string, string>    metadata    = 5;
}
```

**Tipos escalares proto3 e seus equivalentes Java:**

| Proto3 | Java | Observação |
|---|---|---|
| `int32` | `int` | Var-length; ineficiente para negativos |
| `int64` | `long` | Var-length |
| `sint32` | `int` | ZigZag; eficiente para negativos |
| `uint32` | `int` | Sem sinal no proto, mas `int` no Java |
| `fixed32` | `int` | Sempre 4 bytes |
| `fixed64` | `long` | Sempre 8 bytes |
| `float` | `float` | IEEE 754 |
| `double` | `double` | IEEE 754 |
| `bool` | `boolean` | |
| `string` | `String` | UTF-8 ou ASCII-7 |
| `bytes` | `ByteString` | Sequência arbitrária de bytes |

`repeated` indica zero ou mais ocorrências (equivale a `List` no Java gerado). `map<K, V>` gera um `Map<K, V>` e não pode ser `repeated`.

### Serialização binária e field numbers

O nome de um campo em `.proto` é irrelevante na **wire format**: o que identifica o campo na serialização binária é o **field number** (o inteiro após o `=`). Cada campo codificado começa com uma tag que combina o field number e o wire type (varint, 64-bit, length-delimited, 32-bit).

```text
tag = (field_number << 3) | wire_type
```

Isso tem duas consequências diretas:

- **Renomear um campo no `.proto` não quebra compatibilidade** — a serialização não usa o nome.
- **Alterar o field number de um campo já existente corrompe silenciosamente os dados** — o decoder lerá o valor no campo errado.

Campos com valor igual ao default (zero para números, string vazia, false para bool) **não são emitidos** na wire format, o que mantém o payload compacto.

### Schema evolution

A evolução de schema em protobuf é regida por três regras simples:

**1. Adicionar campos é seguro** — use um field number nunca antes utilizado. Readers antigos ignoram campos desconhecidos (campo `unknown_fields` preservado).

**2. Remover campos requer reserva** — use `reserved` para garantir que o field number e o nome jamais sejam reaproveitados:

```protobuf
message Pedido {
  reserved 6, 7;           // field numbers aposentados
  reserved "desconto_id";  // nomes aposentados

  string pedido_id  = 1;
  string cliente_id = 2;
  // ...
}
```

**3. Nunca mude o tipo de um campo existente** — `int32` virar `string` no mesmo field number corrompe todos os dados já serializados.

Comparando estratégias de evolução:

| Estratégia | JSON | Avro | Protobuf |
|---|---|---|---|
| Campos desconhecidos | Preservados (maioria dos parsers) | Descartados | Preservados |
| Compatibilidade verificada | Não | Em runtime (Schema Registry) | Em compilação |
| Renomear campo | Quebra | Quebra (Avro usa nome) | **Seguro** (usa field number) |
| Remover campo | Quebra consumers | Regras BACKWARD/FORWARD | `reserved` |

---

## Na prática

### Definição do contrato — `Order.proto`

```protobuf
syntax = "proto3";

package br.com.exemplo.loja;

option java_package        = "br.com.exemplo.loja.proto";
option java_multiple_files = true;

message Order {
  string order_id    = 1;
  string customer_id = 2;
  int64  created_at  = 3;  // epoch millis
  repeated OrderItem items  = 4;
  OrderStatus        status = 5;

  reserved 6;              // antigo "coupon_code" — aposentado
  reserved "coupon_code";
}

message OrderItem {
  string product_id = 1;
  int32  quantity   = 2;
  double unit_price = 3;
}

enum OrderStatus {
  ORDER_STATUS_UNSPECIFIED = 0;
  ORDER_STATUS_PENDING     = 1;
  ORDER_STATUS_PAID        = 2;
  ORDER_STATUS_SHIPPED     = 3;
  ORDER_STATUS_CANCELLED   = 4;
}
```

### Toolchain Java — dependência e geração de código

Adicione a dependência runtime ao `pom.xml`:

```xml
<dependency>
  <groupId>com.google.protobuf</groupId>
  <artifactId>protobuf-java</artifactId>
  <version>4.28.2</version>
</dependency>
```

Para gerar o código Java automaticamente no build Maven, use o `protobuf-maven-plugin`:

```xml
<plugin>
  <groupId>io.github.ascopes</groupId>
  <artifactId>protobuf-maven-plugin</artifactId>
  <version>2.6.0</version>
  <configuration>
    <protocVersion>4.28.2</protocVersion>
  </configuration>
  <executions>
    <execution>
      <goals>
        <goal>generate</goal>
      </goals>
    </execution>
  </executions>
</plugin>
```

Coloque os arquivos `.proto` em `src/main/protobuf/`. O plugin roda o `protoc` e deposita as classes geradas em `target/generated-sources/protobuf/`.

Como alternativa, invoque o `protoc` manualmente:

```bash
protoc \
  --proto_path=src/main/protobuf \
  --java_out=target/generated-sources/protobuf \
  src/main/protobuf/order.proto
```

### Usando o código gerado em Java

O `protoc` gera classes imutáveis com builder fluente:

```java
// Construção
Order order = Order.newBuilder()
    .setOrderId("ord-001")
    .setCustomerId("cust-42")
    .setCreatedAt(System.currentTimeMillis())
    .setStatus(OrderStatus.ORDER_STATUS_PENDING)
    .addItems(OrderItem.newBuilder()
        .setProductId("prod-7")
        .setQuantity(2)
        .setUnitPrice(49.90)
        .build())
    .build();

// Serialização
byte[] bytes = order.toByteArray();

// Desserialização
Order parsed = Order.parseFrom(bytes);

// Uso com OutputStream / InputStream
order.writeTo(outputStream);
Order fromStream = Order.parseFrom(inputStream);
```

`parseFrom` lança `InvalidProtocolBufferException` se os bytes estiverem corrompidos ou se o field number não corresponder ao wire type esperado.

---

## Armadilhas

### (1) Reutilizar um field number aposentado

Se o campo `6` foi `coupon_code` (string) e você o remove sem `reserved`, um desenvolvedor futuro pode criar um novo campo `int32 loyalty_points = 6`. Mensagens antigas ainda contêm bytes codificados como string no field 6: ao tentar ler como `int32`, o decoder lança exceção ou retorna lixo silencioso. **Use sempre `reserved` ao remover campos.**

### (2) Mudar o tipo de um campo existente

Trocar `int32 quantity = 2` por `string quantity = 2` no mesmo field number produz corrupção de dados para mensagens já serializadas. O wire type muda (varint → length-delimited), e a decodificação falha ou gera valores sem sentido. Se precisar mudar o tipo, crie um novo campo com um novo field number e deprecate o antigo.

### (3) Renumerar campos ("limpar" a sequência)

Ao remover campos intermediários e renumerar os restantes para "reorganizar", você efetivamente reaponta field numbers para outros campos — com os mesmos efeitos da armadilha 1. Field numbers são permanentes: gaps na sequência são absolutamente normais e esperados.

> [!warning] Regra de ouro
> Field numbers são identidades permanentes. Uma vez atribuído a um campo, um número nunca muda e nunca é reutilizado — mesmo após o campo ser removido.

---

## Em entrevista

### Frase pronta (inglês)

"Protocol Buffers define a contract using a `.proto` IDL file, which the `protoc` compiler uses to generate strongly-typed Java classes with an immutable builder pattern. Fields are identified by their field number in the binary wire format, not by their name, which means renaming is safe but reusing a number after removal silently corrupts data. Schema evolution is managed by always reserving retired field numbers and names, adding new fields with fresh numbers, and never changing the type of an existing field — ensuring backward and forward compatibility without a central registry."

### Vocabulário

| Termo | Definição |
|---|---|
| **IDL** (Interface Definition Language) | Linguagem para descrever estruturas de dados e contratos de API de forma independente de linguagem |
| **field number** | Inteiro positivo único dentro de uma `message` que identifica o campo na wire format; imutável após definido |
| **wire type** | Código de 3 bits combinado com o field number na tag; indica como o valor está codificado (varint, fixed, length-delimited) |
| **`reserved`** | Declaração que aposenta um field number ou nome, impedindo reuso acidental |
| **wire format** | Representação binária compacta produzida pela serialização protobuf; menor e mais rápida de parsear que JSON |
| **`protoc`** | Compilador de arquivos `.proto`; gera código de cliente e servidor em diversas linguagens, incluindo Java |
| **packed encoding** | Codificação padrão de campos `repeated` numéricos em proto3; agrupa todos os valores em um único bloco length-delimited |
| **schema evolution** | Capacidade de alterar um schema ao longo do tempo sem quebrar producers ou consumers existentes |

---

## Veja também

- [[03-Dominios/Tecnologia/Java/Mensageria/index|Mensageria (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Mensageria/28 - gRPC em Java — RPC síncrono sobre HTTP_2|gRPC em Java]]
- [[03-Dominios/Tecnologia/Java/Mensageria/14 - Schema e contratos — Avro e Schema Registry|Schema e contratos]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java|Dicionário de Java]]

---

## Referências

- [Protocol Buffers — Language Guide (proto3)](https://protobuf.dev/programming-guides/proto3/) — Google, 2024
- [Java Generated Code Reference](https://protobuf.dev/reference/java/java-generated/) — protobuf.dev
- [Protocol Buffers Java Tutorial](https://protobuf.dev/getting-started/javatutorial/) — protobuf.dev
- [com.google.protobuf:protobuf-java](https://mvnrepository.com/artifact/com.google.protobuf/protobuf-java) — Maven Central
- [protobuf-maven-plugin (ascopes)](https://github.com/ascopes/protobuf-maven-plugin) — GitHub
