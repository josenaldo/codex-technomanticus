---
title: "Versionamento e evolução de eventos"
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
  - eventos
---

# Versionamento e evolução de eventos

> [!abstract] TL;DR
> Eventos são contratos públicos e duradouros: uma vez publicados, vivem para sempre no log. Evoluir um evento com segurança exige adicionar apenas campos opcionais com valor padrão — renomear ou remover campos obrigatórios quebra consumidores desconhecidos silenciosamente. O Confluent Schema Registry impõe compatibilidade BACKWARD/FORWARD/FULL antes do deploy, e o padrão de upcasting transforma eventos antigos em novos na leitura, desacoplando produtor e consumidor no tempo.

---

## O que é

**Versionamento de eventos** é o conjunto de práticas e ferramentas que permite que o schema de um evento mude ao longo do tempo sem quebrar produtores e consumidores já em operação.

Em arquiteturas orientadas a eventos, um evento publicado não pode ser "desfeito": ele já está gravado no log do broker e pode ser reprocessado a qualquer momento — inclusive por consumidores que ainda nem existiam quando o evento foi produzido. Isso torna o schema do evento um contrato de API pública com duração indefinida.

O Confluent Schema Registry, confirmado por sua documentação oficial, fornece o mecanismo central: cada versão de schema recebe um ID único, e políticas de compatibilidade configúráveis determinam quais mudanças são permitidas antes de qualquer deploy.

---

## Por que importa

### Eventos são contratos públicos e duradouros

Ao contrário de uma chamada REST entre dois serviços com versões alinhadas, um evento Kafka pode ser consumido por:

- Múltiplos consumidores em times diferentes
- Consumidores lendo a partir do início do tópico (reprocessamento)
- Consumidores que ainda serão escritos no futuro

Isso significa que **o produtor não conhece todos os seus consumidores**. Uma mudança de schema que parece local pode silenciosamente quebrar um consumidor em outro serviço, em outro time, em outro país — sem erro visível no produtor.

> [!warning] A regra de ouro
> Um evento publicado vive para sempre. Trate o schema como uma API pública versionada, não como um campo interno de uma classe Java.

### O custo de não versionar

Sem controle de compatibilidade:
- Renomear um campo de `customerId` para `clientId` quebra qualquer consumidor que leia `customerId`
- Remover um campo obrigatório gera `NullPointerException` em consumidores que dependem dele
- Mudar o tipo de `String` para `Long` corrompe a desserialização sem exceção clara

---

## Como funciona

### Schema evolution: o que é permitido e o que não é

Com base na documentação do Confluent Schema Registry, as regras de evolução segura são:

| Mudança | Permitido? | Por quê |
|---|---|---|
| Adicionar campo opcional com `default` | **Sim** | Consumidores antigos ignoram o campo; novos usam o default se o campo ausente |
| Remover campo opcional | **Sim** (com cuidado) | Consumidores que usavam o campo passam a receber o default |
| Adicionar campo obrigatório (sem default) | **Não** | Consumidores antigos não enviam o campo; novos falham ao ler dados antigos |
| Remover campo obrigatório | **Não** | Consumidores novos falham ao processar eventos antigos sem o campo |
| Renomear campo | **Não** | Equivale a remover o antigo e adicionar um novo — quebra ambos os lados |
| Mudar tipo (widening, ex: int→long) | Depende do formato | Avro suporta type promotion em alguns casos |

Em Avro, o padrão canônico para campo opcional é usar union com null como primeiro tipo:

```json
{
  "name": "couponCode",
  "type": ["null", "string"],
  "default": null
}
```

Esse padrão garante que consumidores antigos (que não conhecem o campo) leiam `null` como default ao processar eventos novos.

### Compatibilidade no Schema Registry

O Confluent Schema Registry (documentação oficial) define quatro modos principais:

- **BACKWARD**: consumidores com schema **novo** conseguem ler dados escritos com schema **antigo**. Requer upgrade do consumidor primeiro. Permite adicionar campos opcionais e remover campos opcionais.
- **FORWARD**: consumidores com schema **antigo** conseguem ler dados escritos com schema **novo**. Requer upgrade do produtor primeiro.
- **FULL**: combinação de BACKWARD e FORWARD. Permite somente mudanças que são seguras em ambos os sentidos (adicionar/remover campos opcionais com default).
- **NONE**: desativa verificação de compatibilidade (usar apenas em desenvolvimento).

Variantes **transitive** (`BACKWARD_TRANSITIVE`, etc.) checam compatibilidade com **todas** as versões anteriores, não apenas a última — recomendado para tópicos com reprocessamento.

### Upcasting e tolerância a campos desconhecidos

**Upcasting** é a transformação de um evento de formato antigo para o formato atual no momento da leitura, sem modificar o dado armazenado.

Estratégias complementares:

- **Ignore unknown fields**: ao desserializar, ignorar campos presentes no evento que não existem no schema atual do consumidor. Avro faz isso nativamente; JSON requer configuração explícita (ex: `@JsonIgnoreProperties(ignoreUnknown = true)` no Jackson).
- **Default values**: campos novos no schema do consumidor, ausentes no evento antigo, recebem o valor default declarado no schema.
- **Event upcaster**: padrão de design em que uma camada de transformação (implementada no consumidor ou em um componente dedicado) converte representações antigas para a representação atual antes de entregar ao handler de negócio.

---

## Na prática

### Exemplo: evolução de `OrderPlacedEvent`

**Versão 1** — schema original:

```json
{
  "type": "record",
  "name": "OrderPlacedEvent",
  "namespace": "com.example.orders.events",
  "fields": [
    { "name": "orderId",    "type": "string" },
    { "name": "customerId", "type": "string" },
    { "name": "totalAmount","type": "double" }
  ]
}
```

**Versão 2** — evolução compatível (adicionar campo opcional):

```json
{
  "type": "record",
  "name": "OrderPlacedEvent",
  "namespace": "com.example.orders.events",
  "fields": [
    { "name": "orderId",    "type": "string" },
    { "name": "customerId", "type": "string" },
    { "name": "totalAmount","type": "double" },
    {
      "name": "couponCode",
      "type": ["null", "string"],
      "default": null
    }
  ]
}
```

Consumidores na Versão 1 continuam funcionando: o campo `couponCode` está ausente nos eventos antigos e o Avro usa o default `null`. Consumidores na Versão 2 recebem `null` ao processar eventos antigos. Compatibilidade FULL mantida.

**Evolução incompatível** — o que NÃO fazer:

```java
// ANTES (Versão 1)
public record OrderPlacedEvent(
    String orderId,
    String customerId,   // <- campo usado por 3 consumidores
    double totalAmount
) {}

// DEPOIS (Versão 2 — QUEBRA consumidores)
public record OrderPlacedEvent(
    String orderId,
    String clientId,     // RENOMEADO: customerId virou clientId
    double totalAmount,
    String couponCode    // OBRIGATÓRIO sem default: eventos antigos não têm esse campo
) {}
```

O Schema Registry com compatibilidade FULL rejeitaria o registro da Versão 2 antes mesmo do deploy.

### Upcaster em Java (padrão)

```java
@Component
public class OrderPlacedEventUpcaster {

    public OrderPlacedEventV2 upcast(OrderPlacedEventV1 v1) {
        return new OrderPlacedEventV2(
            v1.orderId(),
            v1.customerId(),
            v1.totalAmount(),
            null   // couponCode ausente em eventos V1 recebe null
        );
    }
}
```

---

## Armadilhas

### (1) Renomear campo — a armadilha mais comum

Renomear `customerId` para `clientId` **não é uma mudança de schema**: é a combinação de remover `customerId` (campo obrigatório) e adicionar `clientId` (sem default). Ambos os passos são incompatíveis.

A estratégia correta é deprecar progressivamente:
1. Adicionar o novo campo `clientId` como opcional, mantendo `customerId`
2. Migrar produtores para preencher ambos
3. Migrar todos os consumidores para usar `clientId`
4. Deprecar `customerId` (marcar como opcional com default)
5. Remover `customerId` após período de carência

### (2) Remover campo sem deprecação

Remover um campo obrigatório imediatamente quebra consumidores que dependem dele. Mesmo um campo que "ninguém usa" pode ser lido por um consumidor de auditoria, um job de reprocessamento histórico, ou um consumidor de outro time que não participou da decisão.

Regra: campos obrigatórios nunca são removidos diretamente. Eles são primeiro tornados opcionais (com default), os consumidores são migrados, e só então removidos — com janela de tempo explícita documentada no schema ou no changelog do tópico.

### (3) Mudar o significado de um campo mantendo o nome

A armadilha mais insidiosa: manter o nome e o tipo, mas mudar a semântica. Exemplo: o campo `amount` passa de "valor em centavos" para "valor em reais". Não há como detectar isso via Schema Registry — o schema é idêntico.

Consequências: consumidores antigos continuam processando sem erro, mas produzem resultados incorretos (pedidos com valor 100x errado, por exemplo).

A solução é tratar mudanças semânticas como mudanças de contrato: criar um novo campo (`amountInCents` → `amountInReais`) e deprecar o antigo via o processo acima, ou versionar o nome do evento (`OrderPlacedEventV2`).

---

## Em entrevista

### Frase pronta (inglês)

"Event schemas are public contracts with an indefinite lifespan — once an event is published to a Kafka topic, it can be consumed by unknown future services or replayed from the beginning of the log. Safe schema evolution means only adding optional fields with explicit defaults; renaming or removing required fields is a breaking change that silently corrupts consumers. We enforce this at the infrastructure level using Confluent Schema Registry with FULL compatibility mode, which rejects any non-backward-forward-compatible schema before it reaches production."

### Vocabulário

| Termo | Definição |
|---|---|
| **Schema evolution** | Processo de modificar um schema ao longo do tempo mantendo compatibilidade com versões anteriores ou posteriores |
| **Backward compatibility** | Consumidores com schema novo conseguem ler dados escritos com schema antigo |
| **Forward compatibility** | Consumidores com schema antigo conseguem ler dados escritos com schema novo |
| **Full compatibility** | Schema novo é simultaneamente backward e forward compatível com a versão anterior |
| **Transitive compatibility** | Compatibilidade verificada contra todas as versões do histórico, não apenas a última |
| **Upcasting** | Transformação de um evento em formato antigo para o formato atual na leitura, sem alterar o dado armazenado |
| **Schema Registry** | Serviço centralizado que armazena, versiona e valida schemas, atribuindo um ID único a cada versão |
| **Default value** | Valor usado para um campo ausente em eventos produzidos antes de esse campo existir no schema |

---

## Veja também

- [[03-Dominios/Java/Mensageria/index|Mensageria (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Mensageria/14 - Schema e contratos — Avro e Schema Registry|Schema e contratos]]
- [[03-Dominios/Java/Mensageria/23 - Event sourcing e CQRS|Event sourcing e CQRS]]
- [[03-Dominios/Java/Dicionário de Java|Dicionário de Java]]

---

## Referências

- Confluent. *Schema Evolution and Compatibility*. Confluent Platform Documentation. Disponível em: https://docs.confluent.io/platform/current/schema-registry/fundamentals/schema-evolution.html
- Apache Software Foundation. *Apache Avro*. Disponível em: https://avro.apache.org/
