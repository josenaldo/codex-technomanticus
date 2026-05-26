---
title: "06 - Tracing distribuído com OpenTelemetry"
tags:
  - node
  - observability
  - opentelemetry
  - tracing
  - distributed-systems
type: note
status: growing
progresso: andamento
created: 2026-05-09
updated: 2026-05-09
publish: true
---

# Tracing distribuído com OpenTelemetry

> [!abstract] TL;DR
> - **Distributed tracing** reconstrói o caminho completo de uma requisição através de múltiplos serviços, mostrando onde o tempo foi gasto e onde os erros ocorreram — o que logs e métricas isolados não conseguem revelar.
> - Um **trace** é uma árvore de **spans**; cada span representa uma operação com nome, horário de início/fim, atributos e status. Spans filhos são linkados ao pai via **context propagation** (header `traceparent` no formato W3C TraceContext).
> - **OpenTelemetry** (OTel) é o padrão CNCF graduado para instrumentação vendor-neutral: um único SDK produz dados compatíveis com Jaeger, Zipkin, Grafana Tempo, Datadog, Honeycomb e qualquer backend OTLP.
> - O arquivo `tracing.ts` **deve ser importado antes de qualquer outro módulo** — ele instala os patches de auto-instrumentação em tempo de load; se você importar `express` antes, os spans de requisição HTTP não serão gerados.
> - **Sampling** é obrigatório em produção: `ALWAYS_ON` com tráfego real cria volume absurdo; use `TraceIdRatioBased(0.1)` (10%) ou `ParentBasedSampler` para respeitar a decisão do serviço upstream.

O tracing distribuído é o terceiro pilar da observabilidade — o que permite responder "onde o tempo foi gasto?" em vez de apenas "quantos erros aconteceram?". Enquanto logs registram eventos pontuais e métricas agregam comportamento ao longo do tempo, traces reconstroem o fluxo completo de uma requisição, cruzando processos e serviços. OpenTelemetry é hoje o padrão da indústria para capturar e exportar esses dados de forma vendor-neutral.

## O que é

**OpenTelemetry** (OTel) é um projeto de código aberto graduado pela CNCF (_Cloud Native Computing Foundation_) que define APIs, SDKs e protocolos para coleta de sinais de observabilidade — traces, métricas e logs. A principal vantagem é ser **vendor-neutral**: você instrumenta seu código uma vez e pode enviar os dados para qualquer backend (Jaeger, Zipkin, Grafana Tempo, Datadog, Honeycomb, New Relic) apenas trocando o exporter.

### Conceitos centrais

Um **trace** é a representação completa do ciclo de vida de uma requisição distribuída — do ponto de entrada até a resposta final. Estruturalmente, um trace é uma **árvore de spans**.

Um **span** é a unidade básica de trabalho: uma operação com nome, timestamps de início e fim, atributos (chave-valor), eventos e status. Cada span pertence a exatamente um trace e pode ter um span pai, formando a hierarquia pai-filho que define o grafo de execução.

**Context propagation** é o mecanismo que carrega o contexto do trace entre processos. O padrão W3C TraceContext define o header HTTP `traceparent` com o seguinte formato:

```
traceparent: 00-<traceId-32hex>-<spanId-16hex>-<flags-2hex>
```

Exemplo real:

```
traceparent: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01
```

Os campos são:
- `00` — versão do formato (sempre `00` hoje)
- `4bf92f3577b34da6a3ce929d0e0e4736` — trace ID (128 bits, 32 hex chars)
- `00f067aa0ba902b7` — span ID do chamador (64 bits, 16 hex chars)
- `01` — flags (bit 0 = sampled)

Quando o serviço downstream recebe esse header, ele extrai o trace ID e o span ID do pai e cria seu próprio span como filho — mantendo o mesmo fio através de múltiplos serviços. Dentro de um único processo Node.js, essa propagação acontece automaticamente via `AsyncLocalStorage`, sem necessidade de passar contexto manualmente entre funções.

## Como funciona

### Arquitetura

O pipeline de tracing no OpenTelemetry segue esta sequência:

```
Aplicação Node.js
      │
      ▼
  SDK (NodeSDK)          ← você configura aqui: instrumentações, sampler, exporter
      │
      ▼
  SpanProcessor          ← processa spans antes de exportar
  (SimpleSpanProcessor   ← síncrono, para dev
   BatchSpanProcessor)   ← assíncrono com buffer, para produção
      │
      ▼
  Exporter               ← destino dos dados
  (OTLP HTTP/gRPC        ← protocolo padrão, envia para Collector ou backend direto
   Console               ← stdout, útil para debug local
   Zipkin / Jaeger)      ← exporters legados (menos recomendados)
      │
      ▼
  OTel Collector         ← processo separado (opcional mas recomendado)
  (recebe, processa,
   filtra, exporta)
      │
      ▼
  Backend de traces
  (Jaeger / Zipkin / Grafana Tempo / Datadog / Honeycomb)
```

O **OTel Collector** é um componente opcional mas fortemente recomendado em produção. Ele age como intermediário entre a aplicação e o backend final, permitindo: agregar dados de múltiplos serviços, aplicar sampling tail-based, transformar atributos, filtrar traces desnecessários, e trocar o backend sem tocar no código da aplicação.

### Setup com NodeSDK

O arquivo `tracing.ts` deve ser o primeiro código executado na aplicação. Em Node.js, use `--require ./tracing.js` na linha de comando (ou `NODE_OPTIONS='--require ./tracing.js'`) para garantir que os patches de instrumentação sejam aplicados antes de qualquer import de módulo instrumentado.

Versão mínima para desenvolvimento (com `ConsoleSpanExporter`):

```typescript
// tracing.ts - setup mínimo para desenvolvimento
import { NodeSDK } from '@opentelemetry/sdk-node';
import { ConsoleSpanExporter, SimpleSpanProcessor } from '@opentelemetry/sdk-trace-node';
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';

const sdk = new NodeSDK({
  spanProcessor: new SimpleSpanProcessor(new ConsoleSpanExporter()),
  instrumentations: [getNodeAutoInstrumentations()],
});

sdk.start();

process.on('SIGTERM', () => {
  sdk.shutdown().finally(() => process.exit(0)); // simplificado — veja exemplo completo em Na prática
});
```

Versão com OTLPTraceExporter para envio ao Collector ou backend:

```typescript
// tracing.ts - DEVE ser o primeiro arquivo importado
import { NodeSDK } from '@opentelemetry/sdk-node';
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http';
import { SimpleSpanProcessor } from '@opentelemetry/sdk-trace-node';
import { ParentBasedSampler, TraceIdRatioBased } from '@opentelemetry/sdk-trace-base';

const exporter = new OTLPTraceExporter({
  url: process.env.OTEL_EXPORTER_OTLP_ENDPOINT ?? 'http://localhost:4318/v1/traces',
});

const sdk = new NodeSDK({
  spanProcessor: new SimpleSpanProcessor(exporter),
  instrumentations: [getNodeAutoInstrumentations()],
  sampler: new ParentBasedSampler({
    root: new TraceIdRatioBased(Number(process.env.OTEL_SAMPLE_RATIO ?? '0.1')),
  }),
});

sdk.start();

process.on('SIGTERM', () => {
  sdk.shutdown().finally(() => process.exit(0)); // simplificado — veja exemplo completo em Na prática
});
```

Para usar em `package.json` ou `.env`:

```jsonc
// package.json
{
  "scripts": {
    "start": "node --require ./dist/tracing.js dist/index.js",
    "dev": "ts-node --require ./src/tracing.ts src/index.ts"
  }
}
```

Variáveis de ambiente úteis:

```bash
OTEL_SERVICE_NAME=meu-servico
OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4318
OTEL_TRACES_SAMPLER=parentbased_traceidratio
OTEL_TRACES_SAMPLER_ARG=0.1
OTEL_SAMPLE_RATIO=0.1
```

### Auto-instrumentação

O pacote `@opentelemetry/auto-instrumentations-node` instala automaticamente instrumentações para os módulos mais comuns do ecossistema Node.js. Ao chamar `getNodeAutoInstrumentations()`, o SDK patcha os módulos em tempo de load e injeta criação de spans sem nenhuma modificação no código da aplicação.

Módulos cobertos pela auto-instrumentação (seleção):

| Categoria | Módulos |
|---|---|
| HTTP | `http`, `https`, `node:http` |
| Frameworks | `express`, `fastify`, `koa`, `hapi`, `nestjs` |
| Banco de dados | `pg`, `mysql`, `mysql2`, `mongodb`, `mongoose` |
| Cache | `redis`, `ioredis`, `memcached` |
| Filas | `amqplib` (RabbitMQ), `kafkajs` |
| DNS | `dns` |
| gRPC | `@grpc/grpc-js` |

É possível desabilitar instrumentações específicas ou configurá-las individualmente:

```typescript
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';

const instrumentations = getNodeAutoInstrumentations({
  // desabilitar instrumentação de DNS (gera muito ruído)
  '@opentelemetry/instrumentation-dns': { enabled: false },
  // configurar instrumentação do Express para capturar o nome da rota
  '@opentelemetry/instrumentation-express': {
    enabled: true,
    requestHook: (span, info) => {
      span.setAttribute('http.route', info.route);
    },
  },
  // limitar quais queries SQL são capturadas
  '@opentelemetry/instrumentation-pg': {
    enabled: true,
    addSqlCommenterCommentToQueries: true,
    enhancedDatabaseReporting: false, // não capturar valores dos parâmetros
  },
});
```

### Spans manuais

Auto-instrumentação captura operações de infraestrutura (HTTP, banco, cache), mas a lógica de negócio — "processou o pedido", "validou o pagamento", "enviou o e-mail" — precisa de spans manuais para aparecer no trace.

O padrão correto usa `startActiveSpan` com bloco try/catch/finally:

```typescript
import { trace, SpanStatusCode, SpanKind } from '@opentelemetry/api';

const tracer = trace.getTracer('order-service', '1.0.0');

async function processOrder(orderId: string): Promise<OrderResult> {
  return tracer.startActiveSpan('processOrder', async (span) => {
    try {
      // Atributos de negócio — aparecem nos detalhes do span no Jaeger/Tempo
      span.setAttribute('order.id', orderId);
      span.setAttribute('service.component', 'order-processor');

      const order = await fetchOrder(orderId);
      span.setAttribute('order.customer_id', order.customerId);
      span.setAttribute('order.item_count', order.items.length);
      span.setAttribute('order.total_cents', order.totalCents);

      const result = await fulfillOrder(order);
      span.setAttribute('order.fulfillment_id', result.fulfillmentId);

      return result;
    } catch (err) {
      // Registrar a exceção associa o stack trace ao span
      span.recordException(err as Error);
      // Marcar o span como erro — aparece em vermelho no Jaeger
      span.setStatus({
        code: SpanStatusCode.ERROR,
        message: (err as Error).message,
      });
      throw err;
    } finally {
      // OBRIGATÓRIO: todo span iniciado deve ser finalizado
      span.end();
    }
  });
}
```

Para spans aninhados (sub-operações dentro de um span ativo):

```typescript
async function fulfillOrder(order: Order): Promise<FulfillmentResult> {
  // startActiveSpan automaticamente cria este span como filho do span ativo atual
  return tracer.startActiveSpan('fulfillOrder', async (span) => {
    try {
      span.setAttribute('fulfillment.warehouse', order.warehouseId);

      // Criar evento no span (timestamp + atributos, sem criar span filho)
      span.addEvent('inventory_checked', {
        'inventory.available': true,
        'inventory.reserved_units': order.items.length,
      });

      const shipment = await createShipment(order);
      span.setAttribute('shipment.tracking_number', shipment.trackingNumber);

      return { fulfillmentId: shipment.id, trackingNumber: shipment.trackingNumber };
    } catch (err) {
      span.recordException(err as Error);
      span.setStatus({ code: SpanStatusCode.ERROR, message: (err as Error).message });
      throw err;
    } finally {
      span.end();
    }
  });
}
```

### Sampling

Sampling é a decisão de "vou registrar este trace ou descartar?". Sem sampling, um serviço com 1.000 req/s geraria 1.000 traces por segundo — volume proibitivo para armazenar e consultar.

OpenTelemetry suporta os seguintes samplers built-in:

| Sampler | Comportamento | Uso recomendado |
|---|---|---|
| `AlwaysOnSampler` | 100% dos traces registrados | Desenvolvimento e debug local |
| `AlwaysOffSampler` | 0% — descarta tudo | Testes de carga onde tracing é irrelevante |
| `TraceIdRatioBased(ratio)` | Probabilístico baseado no trace ID | Produção com baixo overhead |
| `ParentBasedSampler` | Respeita decisão do span pai; usa sampler raiz para novos traces | Produção — recomendado |

O `ParentBasedSampler` é o mais importante: ele garante que se o serviço upstream decidiu amostrar um trace, todos os serviços downstream também o farão — evitando traces parciais onde apenas parte da árvore foi registrada.

```typescript
import {
  ParentBasedSampler,
  TraceIdRatioBased,
  AlwaysOnSampler,
} from '@opentelemetry/sdk-trace-base';

// Produção: 10% de novos traces, mas sempre completa traces iniciados upstream
const productionSampler = new ParentBasedSampler({
  root: new TraceIdRatioBased(0.1),
});

// Desenvolvimento: 100%
const devSampler = new AlwaysOnSampler();

const sampler = process.env.NODE_ENV === 'production' ? productionSampler : devSampler;
```

Via variáveis de ambiente (sem modificar código):

```bash
# Sampler baseado em ratio de 10%
OTEL_TRACES_SAMPLER=parentbased_traceidratio
OTEL_TRACES_SAMPLER_ARG=0.1

# Samplers disponíveis:
# always_on, always_off, traceidratio, parentbased_always_on,
# parentbased_always_off, parentbased_traceidratio
```

## Na prática

### `tracing.ts` completo para produção

Este é o arquivo de inicialização recomendado para um serviço Node.js em produção, com suporte a diferentes ambientes via variáveis de ambiente:

```typescript
// src/tracing.ts
// ATENÇÃO: Este arquivo DEVE ser o primeiro a ser importado/executado.
// Use: node --require ./dist/tracing.js dist/index.js
import { NodeSDK } from '@opentelemetry/sdk-node';
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http';
import {
  SimpleSpanProcessor,
  BatchSpanProcessor,
  ConsoleSpanExporter,
} from '@opentelemetry/sdk-trace-node';
import {
  ParentBasedSampler,
  TraceIdRatioBased,
  AlwaysOnSampler,
} from '@opentelemetry/sdk-trace-base';
import { Resource } from '@opentelemetry/resources';
import { ATTR_SERVICE_NAME, ATTR_SERVICE_VERSION } from '@opentelemetry/semantic-conventions';

const isDev = process.env.NODE_ENV !== 'production';
const serviceName = process.env.OTEL_SERVICE_NAME ?? 'unknown-service';
const serviceVersion = process.env.npm_package_version ?? '0.0.0';
const sampleRatio = Number(process.env.OTEL_SAMPLE_RATIO ?? (isDev ? '1.0' : '0.1'));

// Resource identifica o serviço em todos os backends
const resource = new Resource({
  [ATTR_SERVICE_NAME]: serviceName,
  [ATTR_SERVICE_VERSION]: serviceVersion,
  'deployment.environment': process.env.NODE_ENV ?? 'development',
});

// Escolher exporter conforme ambiente
const spanProcessor = isDev
  ? new SimpleSpanProcessor(new ConsoleSpanExporter())
  : new BatchSpanProcessor(
      new OTLPTraceExporter({
        url: process.env.OTEL_EXPORTER_OTLP_ENDPOINT ?? 'http://localhost:4318/v1/traces',
        headers: {
          // Adicionar auth headers se o backend exigir (ex: Honeycomb)
          ...(process.env.OTEL_EXPORTER_OTLP_HEADERS
            ? Object.fromEntries(
                process.env.OTEL_EXPORTER_OTLP_HEADERS.split(',').map((h) => h.split('='))
              )
            : {}),
        },
      }),
      {
        // Configurações do BatchSpanProcessor para produção
        maxQueueSize: 2048,
        maxExportBatchSize: 512,
        scheduledDelayMillis: 5000,
        exportTimeoutMillis: 30000,
      }
    );

const sampler = new ParentBasedSampler({
  root: isDev ? new AlwaysOnSampler() : new TraceIdRatioBased(sampleRatio),
});

const sdk = new NodeSDK({
  resource,
  spanProcessor,
  sampler,
  instrumentations: [
    getNodeAutoInstrumentations({
      '@opentelemetry/instrumentation-dns': { enabled: false },
      '@opentelemetry/instrumentation-fs': { enabled: false }, // muito verboso
    }),
  ],
});

sdk.start();

// Graceful shutdown — essencial para não perder spans em buffer no BatchSpanProcessor
const shutdown = () => {
  sdk
    .shutdown()
    .then(() => {
      console.log('OpenTelemetry SDK encerrado com sucesso');
      process.exit(0);
    })
    .catch((err) => {
      console.error('Erro ao encerrar OpenTelemetry SDK', err);
      process.exit(1);
    });
};

process.on('SIGTERM', shutdown);
process.on('SIGINT', shutdown);
```

### Uso em serviço real com tratamento de erros

Exemplo de um serviço de pagamentos com spans manuais, atributos semânticos e propagação de contexto:

```typescript
// src/services/payment-service.ts
import { trace, context, propagation, SpanStatusCode, SpanKind } from '@opentelemetry/api';
import { ATTR_DB_SYSTEM, ATTR_DB_OPERATION } from '@opentelemetry/semantic-conventions';

const tracer = trace.getTracer('payment-service', '1.0.0');

interface PaymentRequest {
  orderId: string;
  customerId: string;
  amountCents: number;
  currency: string;
}

interface PaymentResult {
  transactionId: string;
  status: 'approved' | 'declined';
}

export async function processPayment(req: PaymentRequest): Promise<PaymentResult> {
  return tracer.startActiveSpan(
    'payment.process',
    {
      kind: SpanKind.INTERNAL,
      attributes: {
        'payment.order_id': req.orderId,
        'payment.customer_id': req.customerId,
        'payment.amount_cents': req.amountCents,
        'payment.currency': req.currency,
      },
    },
    async (span) => {
      try {
        // Verificar fraude — span filho gerado automaticamente via startActiveSpan
        const fraudScore = await checkFraud(req);
        span.setAttribute('payment.fraud_score', fraudScore);

        if (fraudScore > 0.8) {
          span.setAttribute('payment.blocked_reason', 'high_fraud_score');
          span.setStatus({ code: SpanStatusCode.ERROR, message: 'Transação bloqueada por risco de fraude' });
          return { transactionId: '', status: 'declined' };
        }

        // Cobrar no gateway
        const result = await chargeGateway(req);
        span.setAttribute('payment.transaction_id', result.transactionId);
        span.setAttribute('payment.gateway_response', result.status);

        if (result.status !== 'approved') {
          span.setStatus({ code: SpanStatusCode.ERROR, message: `Gateway recusou: ${result.status}` });
        }

        return result;
      } catch (err) {
        span.recordException(err as Error);
        span.setStatus({
          code: SpanStatusCode.ERROR,
          message: (err as Error).message,
        });
        throw err;
      } finally {
        span.end(); // Sempre, sempre, sempre
      }
    }
  );
}

async function checkFraud(req: PaymentRequest): Promise<number> {
  return tracer.startActiveSpan('payment.fraud_check', async (span) => {
    try {
      span.setAttribute('fraud.model_version', 'v2.3');
      // ... lógica de verificação
      const score = Math.random(); // placeholder
      span.setAttribute('fraud.score', score);
      return score;
    } finally {
      span.end();
    }
  });
}
```

### Docker Compose para Jaeger all-in-one (desenvolvimento local)

```yaml
# docker-compose.yml
version: '3.8'

services:
  jaeger:
    image: jaegertracing/all-in-one:1.57
    ports:
      - '16686:16686'   # UI do Jaeger
      - '4317:4317'     # OTLP gRPC
      - '4318:4318'     # OTLP HTTP
      - '14268:14268'   # Jaeger HTTP (legado)
    environment:
      COLLECTOR_OTLP_ENABLED: 'true'
    networks:
      - observability

  otel-collector:
    image: otel/opentelemetry-collector-contrib:0.99.0
    command: ['--config=/etc/otelcol/config.yaml']
    volumes:
      - ./otel-collector-config.yaml:/etc/otelcol/config.yaml
    ports:
      - '4317'    # OTLP gRPC (interno)
      - '4318'    # OTLP HTTP (interno)
    depends_on:
      - jaeger
    networks:
      - observability

  app:
    build: .
    environment:
      NODE_ENV: development
      OTEL_SERVICE_NAME: meu-servico
      OTEL_EXPORTER_OTLP_ENDPOINT: http://otel-collector:4318/v1/traces
      OTEL_SAMPLE_RATIO: '1.0'
    depends_on:
      - otel-collector
    networks:
      - observability

networks:
  observability:
    driver: bridge
```

Acesse a UI do Jaeger em `http://localhost:16686` para visualizar os traces.

## Em entrevista

**What is distributed tracing and why does it matter?**

Distributed tracing is a technique for tracking a single request as it flows through multiple services in a distributed system. Each service creates one or more spans — timestamped records of work performed — and links them together using a shared trace ID that is propagated via HTTP headers. The result is a tree of spans that visually reconstructs the request's entire journey, showing which service was slow, where an error originated, and how latency compounds across service boundaries. Without distributed tracing, debugging a slow request in a microservices architecture means correlating logs from five different services by hand, which is error-prone and time-consuming.

**How does OpenTelemetry work in a Node.js application?**

OpenTelemetry provides a Node.js SDK that instruments your application through two mechanisms: automatic and manual. The auto-instrumentation package patches popular modules like Express, pg, redis, and the built-in HTTP client at module load time, creating spans for every incoming request, outgoing HTTP call, and database query without any code changes. Manual instrumentation lets you add business-level spans using `tracer.startActiveSpan()`, attach custom attributes like order IDs or customer tiers, and record exceptions with full stack traces. The SDK sends this data to a backend — Jaeger, Grafana Tempo, or a commercial provider — via the OTLP protocol, which means you can switch backends without changing your instrumentation code. The key constraint is that the SDK initialization file must be loaded before any other module, because the patches are applied at import time.

**When and how do you use sampling in production?**

Sampling is the practice of recording only a fraction of traces to control storage costs and query performance. In development, you typically use `AlwaysOnSampler` to capture everything. In production, `TraceIdRatioBased(0.1)` records 10% of traces probabilistically — enough to detect trends and catch most errors, at one-tenth the cost. The more sophisticated choice is `ParentBasedSampler`, which wraps the ratio sampler as its "root" decision but defers to the upstream service's sampling decision for inbound requests. This ensures trace completeness: if Service A decided to sample a trace and propagated that decision via the `traceparent` header's sampled flag, Service B will also record its spans for that trace rather than creating an orphan fragment. The correct sampling ratio depends on traffic volume and budget — a service handling 10,000 req/s might use 1% (100 traces/s), while a low-traffic internal service might safely use 100%.

## Vocabulário

**Span**: unidade básica de trabalho em um trace. Representa uma operação nomeada com timestamps de início e fim, atributos chave-valor, eventos e status (OK, ERROR, UNSET). Todo span pertence a um trace e pode ter um span pai.

**Trace**: coleção de spans relacionados que representam o caminho completo de uma requisição através de um ou mais serviços. Identificado por um trace ID único de 128 bits (32 hex chars). Estruturalmente é uma árvore de spans.

**Context propagation**: mecanismo de transporte do trace ID e span ID entre processos (via headers HTTP) e entre funções assíncronas dentro do mesmo processo (via `AsyncLocalStorage`). Sem propagação, spans de serviços diferentes não podem ser correlacionados em um único trace.

**W3C TraceContext**: padrão W3C (recomendação desde 2021) que define o formato do header `traceparent` para propagação de contexto entre serviços HTTP. Substituiu formatos proprietários como B3 (Zipkin) e X-B3 (Google). OpenTelemetry usa TraceContext por padrão.

**OTLP** (OpenTelemetry Protocol): protocolo binário baseado em Protocol Buffers para transmissão de traces, métricas e logs entre SDKs, Collectors e backends. Suporta transporte via gRPC (porta 4317) e HTTP/JSON (porta 4318). É o protocolo nativo do ecossistema OTel.

**Exporter**: componente que serializa spans e os envia para um destino específico. Exemplos: `OTLPTraceExporter` (para OTel Collector ou backend OTLP), `ConsoleSpanExporter` (stdout, para debug), `ZipkinExporter`, `JaegerExporter`. Trocar o exporter é a principal forma de mudar de backend sem alterar instrumentação.

**Collector**: processo separado (daemon ou sidecar) que recebe dados dos SDKs, aplica transformações (filtros, atributos, sampling tail-based) e os exporta para um ou mais backends. O `otelcol-contrib` é a distribuição oficial com suporte a dezenas de receivers, processors e exporters.

**Sampler**: componente do SDK que decide, para cada novo trace, se ele será registrado ou descartado. Roda localmente, antes de qualquer exportação. Tipos principais: `AlwaysOnSampler`, `AlwaysOffSampler`, `TraceIdRatioBased`, `ParentBasedSampler`.

**Instrumentation library**: biblioteca que adiciona instrumentação a um módulo específico (ex: `@opentelemetry/instrumentation-express`). Funciona patchando o módulo alvo em tempo de load para injetar criação de spans, propagação de contexto e coleta de atributos automaticamente.

**SpanProcessor**: componente que processa spans antes de exportá-los. `SimpleSpanProcessor` exporta um span de cada vez ao ser finalizado (adequado para dev). `BatchSpanProcessor` acumula spans em buffer e exporta em lotes (adequado para produção, menor overhead).

## Armadilhas

> [!warning] `tracing.ts` deve ser o PRIMEIRO import — sem exceção
> Os patches de auto-instrumentação são aplicados em tempo de load do módulo. Se você importar `express`, `pg` ou `redis` antes de inicializar o SDK, esses módulos já terão sido carregados sem instrumentação, e nenhum span será gerado para eles. A solução é usar `--require ./tracing.js` na linha de comando do Node (ou `NODE_OPTIONS='--require ./tracing.js'`) ou garantir que `import './tracing'` seja a primeira linha do `index.ts`, antes de qualquer outra importação.

> [!warning] `startActiveSpan` vs `startSpan` — não são intercambiáveis
> `startActiveSpan` define o span criado como o "span ativo" atual no `AsyncLocalStorage`, fazendo com que todos os spans criados dentro do callback se tornem automaticamente filhos dele — é isso que cria a hierarquia do trace. `startSpan` cria um span mas não o ativa no contexto: spans criados depois não serão automaticamente filhos. Em quase todos os casos você quer `startActiveSpan`. Use `startSpan` apenas quando precisar de controle explícito sobre o contexto pai.

> [!warning] Nunca esqueça de chamar `span.end()`
> Todo span iniciado que não for finalizado vaza memória — o SDK mantém referências a spans abertos. Em código assíncrono com `await`, erros podem impedir que `span.end()` seja chamado. O padrão correto é sempre usar try/catch/finally com `span.end()` no bloco `finally`. A alternativa é usar o callback de `startActiveSpan`, onde o span é o argumento da função — mas ainda assim você precisa chamar `span.end()` manualmente (o SDK não fecha automaticamente).

> [!warning] `ALWAYS_ON` em produção cria volume insustentável
> Um serviço com 500 req/s com `AlwaysOnSampler` gera 500 traces/s × 365 dias = ~15 bilhões de traces/ano. Backends como Jaeger sem retenção configurada vão simplesmente encher o disco. Use `TraceIdRatioBased(0.1)` ou menor em produção. O valor adequado depende do volume de tráfego e do orçamento de armazenamento. Como regra geral: comece com 1–10%, meça o custo, ajuste.

> [!warning] Auto-instrumentação patcheia módulos no import — não depois
> O `getNodeAutoInstrumentations()` registra patches que são aplicados quando o módulo alvo é importado pela primeira vez. Se você chama `sdk.start()` depois de já ter importado `express` ou `pg` em outro lugar no mesmo processo, os patches não terão efeito. Isso acontece frequentemente com imports circulares ou com arquivos que importam dependências instrumentadas no nível de módulo (fora de funções/classes). A solução definitiva é `--require ./tracing.js` como flag do Node, garantindo que o SDK rode antes de qualquer código da aplicação.

> [!tip] BatchSpanProcessor em produção, SimpleSpanProcessor em dev
> `SimpleSpanProcessor` exporta cada span imediatamente ao ser finalizado — bom para ver traces em tempo real durante desenvolvimento, mas gera overhead de I/O em produção. `BatchSpanProcessor` acumula spans e exporta em lotes a cada N segundos ou quando o buffer enche, com muito menor impacto na latência da aplicação. Configure `scheduledDelayMillis` e `maxExportBatchSize` conforme o volume de tráfego esperado.

## Veja também

- [[03-Dominios/Node/Observability e produção/index]] — MOC do galho 5
- [[01 - Os três pilares - logs, métricas e traces]] — visão geral de observabilidade: logs, métricas e traces como pilares complementares
- [[03 - Correlation IDs e context propagation]] — propagação de contexto manual com `AsyncLocalStorage` antes de usar OTel
- [[Node.js]] — tronco principal do domínio

## Fontes

- [OpenTelemetry JavaScript — documentação oficial](https://opentelemetry.io/docs/languages/js/) — referência completa da API, SDK e convenções semânticas para JavaScript/TypeScript
- [OpenTelemetry Node.js — Getting Started](https://opentelemetry.io/docs/languages/js/getting-started/nodejs/) — guia oficial de instalação e configuração do NodeSDK
- [W3C TraceContext Recommendation](https://www.w3.org/TR/trace-context/) — especificação do header `traceparent` e propagação de contexto entre serviços
- [OpenTelemetry Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/) — convenções de nomenclatura para atributos de spans (HTTP, banco de dados, mensageria, etc.)
- [OTel Collector — documentação](https://opentelemetry.io/docs/collector/) — guia do Collector para pipelines de observabilidade em produção
