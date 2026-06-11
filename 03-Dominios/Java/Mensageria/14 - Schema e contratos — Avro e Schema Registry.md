---
title: "Schema e contratos — Avro e Schema Registry"
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
  - kafka
aliases:
  - "Schema Registry"
---

# Schema e contratos — Avro e Schema Registry

> [!abstract] TL;DR
> Sem schema explícito, producer e consumer compartilham um contrato invisível: qualquer renomeação de campo quebra o consumer em produção sem aviso. O Confluent Schema Registry resolve isso centralizando o registro de schemas (Avro, Protobuf ou JSON Schema), atribuindo um `schema_id` único a cada versão e impondo políticas de compatibilidade (BACKWARD, FORWARD, FULL) que protegem o pipeline antes do deploy.

---

## O que é

O **Confluent Schema Registry** é um serviço REST que armazena, versiona e valida schemas para mensagens Kafka. Cada schema registrado recebe um ID numérico único e globalmente crescente. Na produção de uma mensagem, o `KafkaAvroSerializer` não envia o schema inteiro: envia apenas 1 byte mágico (`0x00`) + 4 bytes com o `schema_id` + o payload Avro binário. O consumer, ao receber, lê o ID, consulta o registry e usa o schema para desserializar.

O registry suporta três formatos de serialização:

- **Apache Avro** — binário compacto, schema em JSON (`.avsc`)
- **Protocol Buffers (Protobuf)** — IDL própria, geração de código
- **JSON Schema (JSON_SR)** — validação de documentos JSON

---

## Por que importa

Em pipelines Kafka, producer e consumer são desacoplados no tempo: o consumer pode estar offline quando a mensagem é produzida, e pode processar a mensagem horas ou dias depois. Se o contrato for implícito (classe Java ou dicionário JSON compartilhado via convenção), qualquer mudança de campo — renomear, trocar tipo, remover — quebra silenciosamente o consumer.

O Schema Registry transforma esse contrato implícito em um **contrato explícito, versionado e validado na borda de produção**. Um producer que tenta registrar um schema incompatível com a política configurada recebe erro imediatamente, antes de qualquer mensagem chegar ao tópico.

---

## Como funciona

### Por que schema explícito

Producer e consumer num sistema de mensageria são independentes: não há chamada direta, não há compilação conjunta, não há garantia de deploy simultâneo. O JSON "funciona" até o dia em que alguém renomeia `userId` para `user_id` — o campo simplesmente some para o consumer sem exceção, apenas `null`.

Avro e outros formatos baseados em schema invertem isso: o schema **é o contrato**, e qualquer violação é detectada no registro — não no consumer em produção às 3h da manhã.

### Avro + Schema Registry

O Avro define schemas em arquivos `.avsc` (JSON). Um schema de record tem:

```json
{
  "type": "record",
  "namespace": "br.com.exemplo.mensageria",
  "name": "PedidoCriado",
  "fields": [
    { "name": "pedidoId", "type": "string" },
    { "name": "clienteId", "type": "string" },
    { "name": "valorTotal", "type": "double" },
    { "name": "status", "type": "string", "default": "PENDENTE" }
  ]
}
```

Cada schema é registrado num **subject**. Por padrão (estratégia `TopicNameStrategy`), o subject de um tópico `pedidos` será `pedidos-value` para o value e `pedidos-key` para a key. O registry mantém versões: `v1`, `v2`, `v3`… e cada versão tem um ID único.

O wire format de uma mensagem Avro no Kafka:

```
[ 0x00 ] [ schema_id: 4 bytes big-endian ] [ payload Avro binário ]
```

O consumer lê o ID, busca o schema no registry e desserializa. O schema não trafega na mensagem — só o ID.

### Compatibilidade

O registry impõe uma política de compatibilidade por subject (configurável também globalmente):

| Política | O que garante | Operações seguras |
|---|---|---|
| **BACKWARD** (padrão) | Consumer com schema novo lê dados antigos | Adicionar campo com `default`; remover campo opcional |
| **FORWARD** | Consumer com schema antigo lê dados novos | Remover campo com `default`; adicionar campo opcional |
| **FULL** | Ambas ao mesmo tempo | Só mudanças que satisfazem as duas |
| **NONE** | Sem verificação | Qualquer mudança |
| **BACKWARD_ALL** / **FORWARD_ALL** / **FULL_ALL** | Variantes transitivas: compara contra *todas* as versões anteriores, não só a última | Mais restritivo |

BACKWARD é o padrão porque o padrão de deploy mais seguro é atualizar consumers antes de producers: o consumer novo precisa conseguir ler mensagens antigas que ainda estão no tópico.

---

## Na prática

### Dependência Maven (Spring Boot 3.x + Confluent)

```xml
<dependency>
    <groupId>io.confluent</groupId>
    <artifactId>kafka-avro-serializer</artifactId>
    <version>7.6.0</version>
</dependency>
```

### Configuração do producer

```yaml
spring:
  kafka:
    bootstrap-servers: localhost:9092
    producer:
      key-serializer: org.apache.kafka.common.serialization.StringSerializer
      value-serializer: io.confluent.kafka.serializers.KafkaAvroSerializer
    properties:
      schema.registry.url: http://localhost:8081
      auto.register.schemas: true          # dev only; false em produção
      use.latest.version: false
```

### Configuração do consumer

```yaml
spring:
  kafka:
    consumer:
      key-deserializer: org.apache.kafka.common.serialization.StringDeserializer
      value-deserializer: io.confluent.kafka.serializers.KafkaAvroDeserializer
    properties:
      schema.registry.url: http://localhost:8081
      specific.avro.reader: true           # usa classe gerada, não GenericRecord
```

### REST API básica do registry

```bash
# Listar todos os subjects registrados
GET /subjects

# Listar versões de um subject
GET /subjects/pedidos-value/versions

# Registrar novo schema
POST /subjects/pedidos-value/versions
Content-Type: application/vnd.schemaregistry.v1+json
{ "schema": "{...avsc como string escapada...}" }

# Testar compatibilidade antes de registrar
POST /compatibility/subjects/pedidos-value/versions/latest
```

### Protobuf e JSON Schema como alternativas

O registry suporta os três formatos com a mesma lógica de subjects/versions/compatibilidade. A escolha é de trade-off:

- **Avro** — binário compacto, schema externo obrigatório, maduro no ecossistema Kafka/Hadoop
- **Protobuf** — IDL própria, geração de código mais tipada, usado em gRPC
- **JSON Schema** — mantém legibilidade JSON, útil quando o consumer não é JVM

---

## Armadilhas

### (1) Mudança incompatível quebrando consumers em produção

Renomear um campo (`userId` → `user_id`) ou trocar o tipo (`int` → `string`) sem política de compatibilidade configurada, ou com política NONE, faz o registry aceitar o novo schema. O producer passa a enviar dados no novo formato. Consumers antigos — que ainda estão rodando, processando o backlog — tentam desserializar com o schema antigo e encontram dados que não batem. O resultado é exceção de desserialização em massa ou, pior, leitura silenciosa de `null` em campos críticos.

**Mitigação**: configurar política BACKWARD ou FULL no subject antes do primeiro deploy; nunca remover campos sem `default`; tratar renomeação como remoção + adição.

### (2) Sem registry — contrato implícito no código

Times que não adotam o registry tendem a compartilhar DTOs Java entre producer e consumer via biblioteca interna, ou confiam em "todo mundo sabe que o campo se chama X". Funciona até a primeira mudança assíncrona de times. Sem um ponto central de validação, a divergência entre schemas é detectada apenas em tempo de execução, muitas vezes apenas em produção.

**Mitigação**: adotar o registry desde o primeiro tópico; o custo de implantação é baixo (um container), o custo de não ter é alto.

### (3) Evoluir schema sem política de compatibilidade definida

Deixar a política como NONE (ou nunca configurar, aceitando o padrão global sem revisar) cria uma falsa sensação de segurança: o registry existe, os schemas estão registrados, mas nada impede um producer de registrar um schema completamente incompatível. O contrato existe no papel, mas não é enforced.

**Mitigação**: definir explicitamente a política por subject via API ou no provisionamento de infraestrutura; documentar no ADR do time qual política é usada e por quê.

---

## Em entrevista

### Frase pronta (inglês)

- *"Schema Registry enforces explicit contracts between producers and consumers at registration time, not at runtime."*
- *"BACKWARD compatibility means a new consumer can read old data — that's the safe default when you deploy consumers before producers."*
- *"The schema ID in the wire format means only 5 bytes of overhead per message instead of repeating the full schema."*
- *"Without schema governance, any field rename is a silent breaking change waiting to surface in production."*

### Vocabulário

| Termo | Significado |
|---|---|
| subject | Unidade de versionamento no registry (ex: `pedidos-value`) |
| schema ID | Inteiro único e crescente atribuído a cada schema registrado |
| wire format | Formato binário do payload Kafka: magic byte + schema ID + payload |
| BACKWARD compatibility | Consumer novo consegue ler dados produzidos com schema antigo |
| FORWARD compatibility | Consumer antigo consegue ler dados produzidos com schema novo |
| TopicNameStrategy | Estratégia padrão: subject = `{topic}-value` / `{topic}-key` |
| specific.avro.reader | Config que faz o consumer usar a classe Java gerada, não GenericRecord |

---

## Veja também

- [[03-Dominios/Java/Mensageria/index|Mensageria (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Web e APIs REST/05 - Serialização JSON com Jackson|Serialização JSON com Jackson]]
- [[03-Dominios/Java/Mensageria/24 - Versionamento e evolução de eventos|Versionamento e evolução de eventos]]
- [[03-Dominios/Java/Mensageria/27 - Protocol Buffers — a IDL e a serialização binária|Protocol Buffers]]
- [[03-Dominios/Java/Mensageria/09 - (De)serialização de mensagens|(De)serialização de mensagens]]
- [[03-Dominios/Java/Dicionário de Java|Dicionário de Java]]

---

## Referências

- Confluent. *Schema Registry Overview*. Confluent Documentation. Disponível em: https://docs.confluent.io/platform/current/schema-registry/
- Confluent. *Schema Registry API Reference*. Disponível em: https://docs.confluent.io/platform/current/schema-registry/develop/api.html
- Apache Software Foundation. *Apache Avro*. Disponível em: https://avro.apache.org/
