---
title: "Logs estruturados em produção"
created: 2026-06-12
updated: 2026-06-12
type: concept
status: seedling
publish: true
fase: Adepto
tags:
  - java
  - cloud-native
  - adepto
  - observabilidade
aliases:
  - "Structured logging"
  - "Logs estruturados"
---

# Logs estruturados em produção

> [!abstract] TL;DR
> Em produção, log é dado — não é prosa pra humano ler linha a linha. **Structured logging** emite cada evento como um objeto JSON com campos nomeados (`level`, `message`, `traceId`, `service.name`), o que torna o log **parseável, indexável e consultável** num agregador. Desde o **Spring Boot 3.4**, isso é nativo: basta `logging.structured.format.console=ecs` (ou `gelf`, `logstash`) — sem encoder customizado de Logback. Com tracing ativo, **todo par chave-valor do MDC entra no JSON**, incluindo `traceId`/`spanId`, o que permite pivotar de um log direto pro trace correspondente.

## O que é

Log estruturado é a prática de emitir cada evento de log como um **registro com campos nomeados** — tipicamente um objeto JSON — em vez de uma linha de texto livre.

Compare. Um log de texto tradicional:

```
2026-06-12 10:15:00.067  INFO 39599 --- [main] c.e.OrderService : pedido 4821 confirmado para cliente 77
```

O mesmo evento, estruturado:

```json
{"@timestamp":"2026-06-12T10:15:00.067Z","log":{"level":"INFO"},"message":"pedido confirmado","order_id":4821,"customer_id":77,"service":{"name":"order-service"}}
```

A diferença é que, no segundo caso, `order_id` e `customer_id` são **campos**, não substring espremida no meio de uma frase. Uma ferramenta de agregação consegue filtrar `order_id:4821` sem regex frágil.

> [!info] Por que era difícil antes do Boot 3.4
> Até o Spring Boot 3.3, emitir JSON estruturado exigia um **encoder de Logback customizado** (tipicamente `logstash-logback-encoder`) configurado na unha no `logback-spring.xml`. A partir do **Boot 3.4**, três formatos vêm prontos de fábrica via uma propriedade só.

## Por que importa

Em uma aplicação local, você lê o log no terminal — texto é confortável. Em produção, com dezenas de instâncias atrás de um load balancer, **ninguém lê log linha a linha**: você consulta. E consulta exige estrutura.

- **Parse confiável** — campos nomeados eliminam o regex frágil que quebra quando alguém muda o formato da mensagem.
- **Query e pivot** — num agregador (Loki, Elasticsearch), você filtra por `level`, `service.name`, `customer_id` como se fosse SQL. Texto puro só permite `grep`.
- **Correlação log ↔ trace** — com `traceId` no JSON, você salta de um log de erro direto pro trace distribuído daquela requisição. É o elo que conecta as três fontes de observabilidade (logs, métricas, traces).
- **Padrão de schema** — formatos como ECS dão nomes de campo convencionados, então dashboards e alertas funcionam entre serviços diferentes sem retrabalho.

## Como funciona

### Structured logging nativo no Boot 3.4 (ECS / GELF / Logstash)

A partir do **Spring Boot 3.4**, duas propriedades controlam a saída estruturada:

- `logging.structured.format.console` — formata o log do **console** (stdout).
- `logging.structured.format.file` — formata o log de **arquivo**.

Cada uma aceita um de três formatos JSON prontos de fábrica:

| Formato | Sigla | Origem / uso típico |
|---|---|---|
| `ecs` | **E**lastic **C**ommon **S**chema | Padrão da Elastic; campos como `log.level`, `service.name`, `ecs.version`. Casa direto com Elasticsearch/Kibana. |
| `gelf` | **G**raylog **E**xtended **L**og **F**ormat | Formato do Graylog; campos `short_message`, `level` numérico, extras com prefixo `_`. |
| `logstash` | (Logstash JSON) | Campos `@timestamp`, `@version`, `logger_name`, `level_value`. |

Um arranjo comum em produção é **console humano + arquivo JSON**, ou — mais frequente em container — **console em JSON** (porque o stdout do container é o que o coletor de log captura). Você ainda pode adicionar campos fixos de serviço:

```properties
logging.structured.ecs.service.name=order-service
logging.structured.ecs.service.version=1.4.0
logging.structured.ecs.service.environment=production
```

E refinar o JSON sem encoder customizado: excluir caminhos (`logging.structured.json.exclude`), renomear membros (`...json.rename.*`) ou adicionar campos fixos (`...json.add.*`).

### Correlação traceId/spanId via MDC

O **MDC** (Mapped Diagnostic Context) é um mapa thread-local de pares chave-valor que o SLF4J carrega junto de cada log. A regra-chave do Boot 3.4 é simples:

> Com structured logging ativo, **todo par chave-valor do MDC entra automaticamente no JSON**.

Quando o **tracing está ativo** (Micrometer Tracing), o framework popula o MDC com `traceId` e `spanId` da requisição em curso. Logo, eles aparecem no JSON sem você fazer nada — é o que permite, num agregador, clicar num log e pular pro trace.

Você não escreve `traceId` à mão: ele vem da **instrumentação de trace no código**, que é assunto do Galho 16. Aqui basta saber que *se* o trace está instrumentado, o `traceId` propaga para o log de graça.

> [!tip] Adicionando contexto de negócio ao log
> Além do que o MDC injeta, a API fluente do SLF4J adiciona campos pontuais a um log específico:
> ```java
> logger.atInfo()
>     .addKeyValue("order_id", order.id())
>     .addKeyValue("customer_id", order.customerId())
>     .log("pedido confirmado");
> ```
> Esses pares viram campos do JSON — sem concatenar string na mensagem.

### Agregação: Loki, ELK (conceitual)

Emitir JSON é metade do caminho. A outra metade é **agregar**: um coletor (Promtail/Alloy, Fluent Bit, Logstash) lê o stdout dos containers, e um backend indexa.

- **ELK** (Elasticsearch + Logstash + Kibana) — Logstash/Beats ingere, Elasticsearch indexa cada campo, Kibana consulta. O formato ECS é desenhado pra esse caminho.
- **Loki** (stack Grafana) — indexa **labels** (poucos, baratos) e guarda o corpo do log sem indexar tudo; consulta-se com LogQL. Mais barato, menos índice.

O ponto conceitual: porque o log já é JSON, o backend **não precisa adivinhar** a estrutura — ele lê `level`, `traceId`, `service.name` como campos prontos. JSON na origem é o que torna a agregação consultável em vez de só armazenada.

## Na prática

Configuração de produção típica — `application-prod.properties` de um `order-service` num container:

```yaml
logging:
  structured:
    format:
      console: ecs        # stdout em JSON ECS (o coletor lê o stdout)
    ecs:
      service:
        name: order-service
        version: 1.4.0
        environment: production
  level:
    com.example.order: INFO
```

Com tracing ativo, um log de erro sai assim (campos abreviados):

```json
{
  "@timestamp": "2026-06-12T10:15:00.067Z",
  "log": { "level": "ERROR", "logger": "com.example.order.OrderService" },
  "service": { "name": "order-service", "version": "1.4.0", "environment": "production" },
  "trace": { "id": "8f1c2a9b4e7d6f30" },
  "span": { "id": "a1b2c3d4e5f60718" },
  "message": "falha ao reservar estoque",
  "order_id": 4821,
  "customer_id": 77,
  "ecs": { "version": "8.11" }
}
```

Com `trace.id` no registro, no agregador você filtra `trace.id:8f1c2a9b...` e enxerga **todos os logs daquela requisição**, em todos os serviços que ela atravessou — e dali pivota pro trace distribuído correspondente.

## Armadilhas

### (1) Log de texto não-parseável em produção

Manter o formato de console humano (texto multilinha, cores ANSI) em produção é o erro mais comum. O agregador recebe linhas que ele não consegue separar em campos, e você acaba dependendo de `grep` e regex frágeis. Em ambiente de container, **emita JSON no stdout** — o conforto humano fica pro perfil de dev local.

### (2) Logar dado sensível / PII

Campos estruturados facilitam consulta — e também facilitam **vazar PII em escala**. Um `addKeyValue("cpf", ...)` ou um objeto de pedido serializado inteiro deposita dado pessoal num índice consultável e retido por meses. Trate o log como superfície de exposição: nunca logue senha, token, cartão ou CPF; mascare ou omita campos sensíveis na origem, não no agregador.

### (3) Não correlacionar com traceId — impossível pivotar log ↔ trace

Sem `traceId` no log (tracing desativado, ou MDC não propagado por trabalho assíncrono), você tem dois silos isolados: logs que dizem *o quê* e traces que dizem *onde*, sem ponte entre eles. Num incidente, você acha o log de erro mas não consegue saltar pro trace daquela requisição — perde justamente o ganho que estrutura + tracing deveriam dar juntos.

### (4) Tratar todo evento como mensagem em vez de campo

Espremer dados na string da mensagem (`"pedido " + id + " falhou para " + cliente`) derrota o propósito: vira texto dentro do JSON, não campo consultável. Use `addKeyValue` / MDC para dados; deixe a `message` como descrição estável e curta do evento.

## Em entrevista

### Frase pronta (inglês)

> In production we use structured logging — every event is emitted as a JSON object with named fields instead of a free-text line, which makes logs parseable and queryable in an aggregator like Loki or the ELK stack. Since Spring Boot 3.4 this is built in: you just set `logging.structured.format.console` to `ecs`, `gelf`, or `logstash`, and you no longer need a custom Logback encoder. With tracing enabled, every MDC key-value pair — including `traceId` and `spanId` — is automatically added to the JSON, so I can pivot straight from a log line to the corresponding distributed trace. That correlation is the whole point: logs tell me what happened, traces tell me where, and the shared `traceId` is the bridge.

### Vocabulário

| Português | Inglês |
|---|---|
| log estruturado | structured logging |
| formato JSON | JSON format |
| esquema comum Elastic | Elastic Common Schema (ECS) |
| contexto de diagnóstico (MDC) | Mapped Diagnostic Context (MDC) |
| correlação | correlation |
| agregação de logs | log aggregation |
| dado sensível / PII | sensitive data / PII |
| campo consultável | queryable field |

## Veja também

- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/13 - Observabilidade de operação — o panorama e os 3 seams|Observabilidade de operação]]
- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/16 - OpenTelemetry Collector e sampling de produção|OpenTelemetry Collector e sampling]]
- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/18 - Tracing distribuído I — correlação no código|Tracing distribuído I (Galho 16)]]
- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/index|Cloud-native e produção (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]

## Referências

- Spring Boot Reference — Logging (Structured Logging): https://docs.spring.io/spring-boot/reference/features/logging.html
- Spring Blog — Structured Logging in Spring Boot 3.4 (2024-08-23): https://spring.io/blog/2024/08/23/structured-logging-in-spring-boot-3-4/
