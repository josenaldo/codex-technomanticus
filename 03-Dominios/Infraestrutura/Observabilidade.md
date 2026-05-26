---
title: "Observabilidade"
created: 2026-04-11
updated: 2026-04-11
type: concept
status: evergreen
tags:
  - infraestrutura
  - devops
  - sre
  - entrevista
publish: false
---

# Observabilidade

Deep dive em **observabilidade** para sistemas modernos — **logs**, **metrics**, **traces** (os 3 pilares), mais eventos, profiles, e como montar uma stack completa. Para Linux basics, ver [[Linux]]. Para K8s monitoring, ver [[Kubernetes]]. Para CI/CD monitoring, ver [[CI-CD]].

## O que é

**Observabilidade** (observability, abreviado "o11y") é a capacidade de **entender o estado interno de um sistema** a partir das **saídas externas** que ele produz. Vem da teoria de sistemas — um sistema é "observável" se você consegue reconstruir seu estado interno observando outputs.

**Em engineering:** é sua capacidade de **responder perguntas novas** sobre o sistema **sem precisar mexer no código**.

**Observability ≠ Monitoring:**

- **Monitoring** — você define o que quer olhar (dashboards, alertas). Responde perguntas **conhecidas**. "CPU está OK?"
- **Observability** — você pode fazer drill-down em qualquer dimensão. Responde perguntas **desconhecidas**. "Por que esse endpoint ficou lento para usuários premium no horário de pico na segunda-feira?"

Monitoring é **subset** de observability.

**Em 2026**, o padrão de facto é **OpenTelemetry** (unifica tracing, metrics, logs) + **Prometheus** (metrics) + **Loki / ELK** (logs) + **Jaeger / Tempo** (traces) + **Grafana** (UI).

Em entrevistas, o que diferencia um senior em observabilidade:

1. **Os 3 pilares** — logs, metrics, traces — quando usar cada
2. **RED e USE methods** — frameworks de metric design
3. **SLI, SLO, SLA, error budget** — ligar métricas a negócio
4. **Cardinality** — por que labels matam Prometheus
5. **Sampling** — como decidir o que guardar em traces
6. **OpenTelemetry** — o padrão universal
7. **Logs estruturados** — JSON, não texto
8. **Alertas efetivos** — action oriented, sem noise
9. **Debug de incidente** — como usar observability na crise
10. **Cost control** — observabilidade é cara, disciplina importa

---

## Os 3 pilares — visão geral

### Logs

**Evento discreto** com contexto. "Algo aconteceu".

```json
{
    "timestamp": "2026-04-11T14:23:11Z",
    "level": "ERROR",
    "service": "payment-service",
    "trace_id": "abc123",
    "user_id": "user-42",
    "message": "Payment failed",
    "error": "Insufficient funds",
    "amount_cents": 15000
}
```

**Fortes em:** debugging profundo, audit trail, contexto rico.

**Fracos em:** cardinality alta, agregação, visão geral.

### Metrics

**Números agregáveis** ao longo do tempo. "Quantos? Quão rápido?"

```
http_requests_total{method="POST",route="/api/login",status="200"} 145234
http_request_duration_seconds{method="POST",route="/api/login"} 0.423
```

**Fortes em:** trends, dashboards, alertas, capacity planning.

**Fracos em:** cardinality — labels explodem em memória.

### Traces

**Fluxo de um request** através de múltiplos serviços. "Quanto tempo gastamos onde?"

```
Client → api-gateway (2ms) → auth-service (12ms) →
         ↓
      payment-service (150ms) ← GARGALO
         ↓
      notification-service (8ms)
```

**Fortes em:** distributed systems, latência, causality.

**Fracos em:** volume (sampling obrigatório), armazenamento caro.

### Usando os 3 juntos

Exemplo clássico: "usuário reclama de lentidão".

1. **Metrics** — detecta spike em latência p99 do endpoint X
2. **Traces** — trace de um request lento mostra que gargalo é no serviço Y
3. **Logs** — logs do serviço Y com trace_id correlato mostram stack trace

**Correlação** entre os 3 é essencial. **`trace_id` é a cola.**

---

## Logs

### Logs estruturados

**Regra #1 em 2026:** logue em **JSON**, não em texto.

```
❌ Texto
2026-04-11 14:23:11 ERROR Failed to charge user Maria (id=42): insufficient funds for amount 150.00

✅ JSON
{"time":"2026-04-11T14:23:11Z","level":"error","msg":"Failed to charge user","user":"Maria","user_id":42,"amount":150.00,"currency":"USD","error":"insufficient funds"}
```

**Vantagens do JSON:**

- Machine readable — busca por campo, filtragem, agregação
- Extensível — adiciona campos sem quebrar parser
- Tools (ELK, Loki, Datadog) entendem nativamente

### Níveis de log

| Nível | Uso |
| --- | --- |
| **TRACE** | Muito verboso, debugging profundo |
| **DEBUG** | Informação útil em dev |
| **INFO** | Eventos normais (request served, job started) |
| **WARN** | Algo anômalo mas não quebrou |
| **ERROR** | Erro recuperável ou handled |
| **FATAL** / **CRITICAL** | App vai morrer |

**Produção:** `INFO` geralmente. `DEBUG` em ambiente específico quando investigando.

### O que logar

**Sempre:**

- Timestamp (ISO 8601 com timezone)
- Level
- Message
- Service name
- Trace ID (correlação)

**Quando relevante:**

- User ID (sem PII sensível)
- Request ID
- Tenant ID (multi-tenant)
- Duração
- Status code
- IP (se debugging)

### O que NÃO logar

- **Senhas, tokens, secrets**
- **PII desnecessária** (CPF completo, cartão de crédito)
- **Dados sensíveis** (LGPD, HIPAA, PCI)
- **Objetos enormes** (logs inflados, custos)
- **Informação repetida** (stack trace 5x em cada log level)

### Exemplo Java (Spring Boot)

```xml
<!-- logback-spring.xml -->
<appender name="JSON" class="ch.qos.logback.core.ConsoleAppender">
    <encoder class="net.logstash.logback.encoder.LogstashEncoder">
        <customFields>{"service":"payment-service"}</customFields>
        <includeMdcKeyName>traceId</includeMdcKeyName>
        <includeMdcKeyName>userId</includeMdcKeyName>
    </encoder>
</appender>
```

```java
// Correlação via MDC
import org.slf4j.MDC;

MDC.put("traceId", request.getTraceId());
MDC.put("userId", user.getId());
try {
    log.info("Processing payment");
    // ...
} finally {
    MDC.clear();
}
```

### Exemplo Node.js (Pino)

```javascript
import pino from 'pino';

const log = pino({
    level: 'info',
    formatters: {
        level: (label) => ({ level: label })
    }
});

log.info({ userId: 42, amount: 150 }, 'payment processed');
// {"level":"info","time":..., "userId":42, "amount":150, "msg":"payment processed"}
```

### Collectors e stack

**Pattern comum:**

```
App (JSON stdout) → Collector → Storage → Query/UI
```

**Collectors:**

- **Fluent Bit** — leve, C, eficiente. Default em K8s modernos.
- **Fluentd** — Ruby, mais pesado, plugins variados
- **Vector** (Datadog, Rust) — crescendo, performático
- **Promtail** — collector do Loki

**Storage:**

- **Loki** (Grafana) — barato, usa labels como Prometheus. **Popular em 2026.**
- **Elasticsearch** — full-text search, caro em volume grande
- **Datadog Logs** — SaaS, fácil mas caro
- **CloudWatch Logs** (AWS) — integrado
- **ClickHouse** — OLAP, crescendo para observability

**UI:**

- **Grafana** — Loki, Elasticsearch, muitos datasources
- **Kibana** — Elasticsearch-specific
- **Datadog** — all-in-one

### Log rotation e retention

```
- Produção: 7-30 dias de logs quentes (query rápida)
- Arquivamento: 90 dias - 7 anos (compliance)
- Cold storage: S3 Glacier, Azure Archive
```

**Custo cresce exponencialmente** com retention. Seja preciso no que precisa.

### Sampling de logs

Em alto volume, samplar logs menos importantes:

- **100% errors**
- **50% warnings**
- **1% info** (pode reduzir mais em requests de health check)

Mas nunca sample o que precisa para compliance.

---

## Metrics — Prometheus

### Por que Prometheus

Em 2026, **Prometheus é o padrão de facto** para metrics. Criado pelo SoundCloud (2012), CNCF graduated. Pull-based, time-series DB, linguagem de query (PromQL), ecosystem imenso.

**Alternativas:**

- **InfluxDB** — push-based, bom para IoT
- **Graphite** — antigo, ainda usado
- **Datadog** — SaaS, all-in-one
- **VictoriaMetrics** — compatible com Prom, mais performático
- **Mimir** (Grafana) — Prom-compatible, escala horizontal
- **CloudWatch** (AWS), **Cloud Monitoring** (GCP), **Azure Monitor**

### Modelo

```
┌─────────────────┐
│  Application    │
│  (expõe         │
│   /metrics HTTP)│
└────────┬────────┘
         │ pull (scrape)
         ↓
┌─────────────────┐      ┌──────────────┐
│  Prometheus     │      │  Grafana     │
│  (TSDB, scheduler│───→ │  (UI, query) │
│   rules engine) │      │              │
└────────┬────────┘      └──────────────┘
         │
         ↓
┌─────────────────┐
│  Alertmanager   │
│  (rotas alertas)│
└─────────────────┘
```

### Metric types

**4 tipos:**

**1. Counter** — só cresce (ou reseta para zero em restart).

```
http_requests_total{status="200"} 145234
```

Uso: contadores de requests, erros, eventos.

**2. Gauge** — pode aumentar ou diminuir.

```
memory_usage_bytes 1234567890
active_connections 42
queue_depth 156
```

Uso: valores atuais (temperatura, memória, queue depth).

**3. Histogram** — distribuição de valores em buckets.

```
http_request_duration_seconds_bucket{le="0.1"} 24054
http_request_duration_seconds_bucket{le="0.5"} 33444
http_request_duration_seconds_bucket{le="1.0"} 100392
http_request_duration_seconds_bucket{le="+Inf"} 144320
http_request_duration_seconds_sum 53423
http_request_duration_seconds_count 144320
```

Uso: latências, tamanhos de response.

**4. Summary** — similar a histogram mas calcula percentis client-side.

```
http_request_duration_seconds{quantile="0.5"} 0.052
http_request_duration_seconds{quantile="0.9"} 0.3
http_request_duration_seconds{quantile="0.99"} 1.2
```

**Regra:** use **histogram** > summary. Histograms agregam cross-instance.

### Exposição de metrics

**Java (Spring Boot Actuator + Micrometer):**

```yaml
# application.yml
management:
    endpoints:
        web:
            exposure:
                include: health, metrics, prometheus
    metrics:
        tags:
            application: ${spring.application.name}
        distribution:
            percentiles-histogram:
                http.server.requests: true
```

```xml
<dependency>
    <groupId>io.micrometer</groupId>
    <artifactId>micrometer-registry-prometheus</artifactId>
</dependency>
```

Endpoint: `http://host:port/actuator/prometheus`

```java
@Autowired private MeterRegistry registry;

// Custom metric
Counter counter = Counter.builder("orders_created")
    .tag("type", "premium")
    .register(registry);
counter.increment();

Timer timer = registry.timer("query.duration");
timer.record(() -> db.query(...));
```

**Node.js (prom-client):**

```javascript
import client from 'prom-client';
import express from 'express';

const register = new client.Registry();
client.collectDefaultMetrics({ register });

const httpDuration = new client.Histogram({
    name: 'http_request_duration_seconds',
    help: 'HTTP request duration',
    labelNames: ['method', 'route', 'status'],
    buckets: [0.01, 0.05, 0.1, 0.5, 1, 2, 5]
});
register.registerMetric(httpDuration);

const app = express();

app.use((req, res, next) => {
    const end = httpDuration.startTimer();
    res.on('finish', () => {
        end({ method: req.method, route: req.route?.path, status: res.statusCode });
    });
    next();
});

app.get('/metrics', async (req, res) => {
    res.set('Content-Type', register.contentType);
    res.end(await register.metrics());
});
```

**Python (prometheus_client):**

```python
from prometheus_client import Counter, Histogram, start_http_server

REQUEST_COUNT = Counter('requests_total', 'Total requests', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('request_latency_seconds', 'Request latency')

start_http_server(9090)

@REQUEST_LATENCY.time()
def process_request():
    REQUEST_COUNT.labels(method='GET', endpoint='/api').inc()
```

### Prometheus config

```yaml
# prometheus.yml
global:
    scrape_interval: 15s
    evaluation_interval: 15s

scrape_configs:
    - job_name: 'prometheus'
      static_configs:
          - targets: ['localhost:9090']

    - job_name: 'myapp'
      static_configs:
          - targets: ['app1:8080', 'app2:8080']
      metrics_path: /actuator/prometheus

    - job_name: 'kubernetes-pods'
      kubernetes_sd_configs:
          - role: pod
      relabel_configs:
          - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
            action: keep
            regex: true

rule_files:
    - /etc/prometheus/rules/*.yml

alerting:
    alertmanagers:
        - static_configs:
              - targets: ['alertmanager:9093']
```

### PromQL — queries

```promql
# Total de requests
http_requests_total

# Rate por segundo (última 5 min)
rate(http_requests_total[5m])

# Requests/s por status
rate(http_requests_total{status=~"5.."}[5m])

# Error rate
sum(rate(http_requests_total{status=~"5.."}[5m]))
/
sum(rate(http_requests_total[5m]))

# p95 latency
histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))

# Top 5 endpoints por latência
topk(5, histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, route)))

# Memory usage
process_resident_memory_bytes / 1024 / 1024    # em MB

# Taxa de crescimento
increase(user_registrations_total[1h])

# Alerta — erro rate > 5% por 5 min
(
    sum(rate(http_requests_total{status=~"5.."}[5m]))
    /
    sum(rate(http_requests_total[5m]))
) > 0.05
```

### Cardinality — a armadilha clássica

**Cardinality** = número único de combinações de labels. Prometheus guarda **uma time series por combinação**.

```
http_requests_total{method="GET", route="/users", status="200", user_id="42"}
http_requests_total{method="GET", route="/users", status="200", user_id="43"}
# ...
```

Com 1M usuários, você cria 1M time series. **Prometheus cai em memória.**

**Regra:** labels devem ter **baixa cardinalidade**. Use user_id em **logs ou traces**, não em metrics.

**OK em metrics:**

- `method` (GET, POST, PUT, DELETE, ...)
- `route` (`/users`, `/orders/:id` — normalizada)
- `status` (200, 404, 500, ...)
- `environment` (prod, staging)
- `region` (us-east-1, eu-west-1)

**NÃO OK em metrics:**

- `user_id` — milhões
- `request_id` — cada request é único
- `email` — milhões
- `path` sem normalizar (`/users/42` vs `/users/43`)

**Limite prático:** mantenha total de time series < 1M por instância Prometheus.

### Recording rules

Pre-computa queries caras:

```yaml
groups:
    - name: http_performance
      interval: 30s
      rules:
          - record: job:http_request_errors:rate5m
            expr: sum(rate(http_requests_total{status=~"5.."}[5m])) by (job)

          - record: job:http_request_latency_p99:5m
            expr: histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (job, le))
```

Dashboard usa a rule recorded, não a query cara em tempo real.

### Alerting rules

```yaml
groups:
    - name: myapp
      rules:
          - alert: HighErrorRate
            expr: |
                (
                    sum(rate(http_requests_total{status=~"5.."}[5m]))
                    /
                    sum(rate(http_requests_total[5m]))
                ) > 0.05
            for: 5m
            labels:
                severity: critical
            annotations:
                summary: "High error rate on {{ $labels.instance }}"
                description: "Error rate is {{ $value | humanizePercentage }}"
                runbook_url: "https://wiki.example.com/runbooks/high-error-rate"

          - alert: HighLatency
            expr: histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le)) > 2
            for: 10m
            labels:
                severity: warning
            annotations:
                summary: "p99 latency above 2s"
```

**`for`** — sustenta condição por X tempo antes de disparar. Evita alertas flapping.

### Alertmanager

Recebe alertas, deduplica, roteia, silencia:

```yaml
route:
    receiver: default
    group_by: [alertname, cluster]
    group_wait: 30s
    group_interval: 5m
    repeat_interval: 4h
    routes:
        - match:
              severity: critical
          receiver: pagerduty
        - match:
              severity: warning
          receiver: slack

receivers:
    - name: pagerduty
      pagerduty_configs:
          - service_key: ...

    - name: slack
      slack_configs:
          - api_url: https://hooks.slack.com/...
            channel: '#alerts'

    - name: default
      email_configs:
          - to: ops@example.com
```

---

## RED e USE methods

Frameworks para decidir **o que medir**.

### RED Method (services)

**Rate, Errors, Duration** — Tom Wilkie (Grafana).

Para **cada serviço**, meça:

- **Rate** — requests/s
- **Errors** — errors/s (ou error rate)
- **Duration** — latência (distribuição, não só média)

```promql
# Rate
sum(rate(http_requests_total[5m])) by (service)

# Errors
sum(rate(http_requests_total{status=~"5.."}[5m])) by (service)

# Duration (p99)
histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (service, le))
```

Estes 3 dashboards por serviço respondem 80% das perguntas operacionais.

### USE Method (resources)

**Utilization, Saturation, Errors** — Brendan Gregg.

Para **cada recurso** (CPU, memória, disco, rede, GPU), meça:

- **Utilization** — % do tempo ocupado
- **Saturation** — trabalho esperando (queue depth)
- **Errors** — erros do recurso

**CPU:**

- Utilization: `100 - (avg(irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)`
- Saturation: load average, run queue
- Errors: —

**Memory:**

- Utilization: `(total - available) / total`
- Saturation: swap usage, OOM kills
- Errors: ECC errors

**Disk:**

- Utilization: `node_disk_io_time_seconds_total / time`
- Saturation: disk queue
- Errors: read/write errors

### Quando usar cada

- **RED** — para services (HTTP APIs, gRPC, workers)
- **USE** — para recursos (machines, containers, devices)

**Use ambos.** Complementares.

### Golden signals (Google SRE)

Similar ao RED + saturation:

1. **Latency** — quanto tempo requests levam
2. **Traffic** — quantos requests
3. **Errors** — quantos falham
4. **Saturation** — quão "cheio" o serviço está

---

## SLI, SLO, SLA, Error Budget

### Definições

- **SLI (Service Level Indicator)** — métrica que você mede. "% de requests que retornam 2xx em menos de 500ms"
- **SLO (Service Level Objective)** — target interno. "99.9% das requests em 30 dias"
- **SLA (Service Level Agreement)** — promessa contratual com penalidade. "99.5% ou dinheiro de volta"
- **Error Budget** — quanto de "erro" você pode "gastar" antes de violar o SLO

### Error Budget — a ideia brilhante

Se seu SLO é 99.9%, você tem 0.1% de error budget.

**Em 30 dias:** 0.1% × 43200 min = 43.2 minutos de downtime permitidos.

**Durante o mês:**

- Se está **gastando pouco** (0.02%), está ok para deployar features arriscadas
- Se está **esgotando** (0.08% e ainda é dia 15), deploys viram conservadores — só bug fixes

**Error budget é "dinheiro"** — permite decisões baseadas em trade-offs objetivos, não discussões de opinião.

### Definindo SLOs bons

**Regra 1:** SLO deve refletir experiência do usuário, não componentes internos.

- ✅ "95% das pesquisas retornam resultados em < 500ms"
- ❌ "Latency média do DB < 50ms"

**Regra 2:** SLO deve ser **alcançável** e **agressivo o suficiente para importar**.

- 100% é impossível (e caro)
- 99.999% ("5 nines") é ~5 min/ano — apenas sistemas críticos
- 99.9% ("3 nines") é ~43 min/mês — maioria dos sistemas web
- 99% (~7h/mês) é baixo mas OK para sistemas internos

**Regra 3:** SLO é **promessa**, não **goal**. Baseado em o que você consegue entregar consistentemente.

### Exemplo

```yaml
# SLI: Availability
expr: |
    sum(rate(http_requests_total{status!~"5.."}[30d]))
    /
    sum(rate(http_requests_total[30d]))

# SLO: 99.9%
target: 0.999

# Error budget:
# 30 dias = 43,200 min
# 0.1% = 43.2 min de "down" permitidos
```

### Burn rate alerts

Alerta que detecta **esgotamento rápido do error budget**:

```yaml
# Gastando 5% do budget em 1 hora = vai zerar em ~20 horas
- alert: HighBurnRate
  expr: |
      (
          sum(rate(http_requests_total{status=~"5.."}[1h]))
          /
          sum(rate(http_requests_total[1h]))
      ) > (14.4 * 0.001)   # 14.4x o budget rate
  for: 2m
  labels:
      severity: critical
```

Ver [SRE Workbook — Alerting on SLOs](https://sre.google/workbook/alerting-on-slos/).

---

## Distributed Tracing

### Conceitos

- **Trace** — um request completo através do sistema
- **Span** — uma operação individual (chamada de método, query, request HTTP)
- **Span context** — metadata propagada entre services (trace_id, span_id, parent_id)
- **Sampling** — decidir quais traces guardar (volume é enorme)

### Exemplo de trace

```
[── client ──────────────────────────────────── 450ms ──]
  [── api-gateway (5ms) ──]
    [── auth-service (30ms) ──]
      [── db query (20ms) ──]
    [── order-service (400ms) ────────────────────]
      [── get user (10ms) ──]
      [── create order (50ms) ──]
      [── payment-service (300ms) ──────]  ← BOTTLENECK
        [── external API (290ms) ──]
      [── notification (15ms) ──]
```

Cada `[── ──]` é um span. Trace completo mostra a cadeia, latências, gargalos.

### OpenTelemetry — o padrão

**OpenTelemetry (OTel)** é o padrão universal (CNCF). Unifica tracing, metrics, e logs em uma API/SDK.

**Arquitetura:**

```
┌─────────────────┐
│  Application    │
│  (OTel SDK)     │
└────────┬────────┘
         │ OTLP
         ↓
┌─────────────────┐
│  OTel Collector │  (recebe, processa, exporta)
└────────┬────────┘
         │
    ┌────┴────┐
    ↓         ↓         ↓
┌───────┐ ┌──────┐ ┌──────────┐
│Jaeger │ │Loki  │ │Prometheus│
│(trace)│ │(log) │ │(metrics) │
└───────┘ └──────┘ └──────────┘
```

**Em 2026:** OTel é **default em novos projetos**. Substitui as SDKs separadas (OpenTracing, OpenCensus, Jaeger client, Zipkin client).

### Setup Java (Spring Boot 3)

```xml
<!-- pom.xml -->
<dependency>
    <groupId>io.micrometer</groupId>
    <artifactId>micrometer-tracing-bridge-otel</artifactId>
</dependency>
<dependency>
    <groupId>io.opentelemetry</groupId>
    <artifactId>opentelemetry-exporter-otlp</artifactId>
</dependency>
```

```yaml
# application.yml
management:
    tracing:
        sampling:
            probability: 1.0        # 100% em dev, 0.1 em prod
    otlp:
        tracing:
            endpoint: http://otel-collector:4318/v1/traces
```

Spring Boot 3 + Micrometer Tracing injeta trace ID automaticamente em logs via MDC.

### Setup Node.js

```bash
npm install @opentelemetry/sdk-node @opentelemetry/auto-instrumentations-node @opentelemetry/exporter-trace-otlp-http
```

```javascript
// instrumentation.js
import { NodeSDK } from '@opentelemetry/sdk-node';
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http';

const sdk = new NodeSDK({
    traceExporter: new OTLPTraceExporter({
        url: 'http://otel-collector:4318/v1/traces'
    }),
    instrumentations: [getNodeAutoInstrumentations()]
});

sdk.start();
```

```bash
# Start com instrumentação
node --require ./instrumentation.js app.js
```

Auto-instrumentação captura Express, HTTP, Postgres, Redis, MongoDB, etc. Sem mudanças no código.

### Manual spans

```typescript
import { trace } from '@opentelemetry/api';

const tracer = trace.getTracer('my-service');

async function processOrder(orderId: string) {
    return tracer.startActiveSpan('processOrder', async (span) => {
        try {
            span.setAttribute('order.id', orderId);
            const order = await fetchOrder(orderId);
            const result = await charge(order);
            span.setAttribute('order.amount', result.amount);
            return result;
        } catch (error) {
            span.recordException(error);
            span.setStatus({ code: 2 });    // ERROR
            throw error;
        } finally {
            span.end();
        }
    });
}
```

### Context propagation

Para trace cross-service funcionar, **trace context precisa ser propagado** nos headers HTTP:

```
traceparent: 00-abc123...-xyz456...-01
tracestate: vendor1=value1,vendor2=value2
```

Auto-instrumentação faz isso. Manualmente:

```typescript
import { propagation, context } from '@opentelemetry/api';

const headers = {};
propagation.inject(context.active(), headers);
await fetch(url, { headers });
```

### Sampling

Em produção, **não samplear 100%** — volume é enorme, custo explode.

**Estratégias:**

- **Head sampling** — decide no início do trace (simples, mas pode perder trace importante)
- **Tail sampling** — decide após o trace completar (pega erros, traces lentos, mas requer buffering)
- **Probabilistic** — x% dos traces
- **Rate limit** — N traces/s
- **Adaptive** — ajusta baseado em load

**Regra:** 1-10% amostra em produção, 100% de errors, 100% de traces lentos (> p99).

### Backends de trace

- **Jaeger** — CNCF, open source, mais popular
- **Tempo** (Grafana) — object storage (S3), barato
- **Zipkin** — antigo, ainda usado
- **Datadog APM** — SaaS
- **New Relic** — SaaS
- **AWS X-Ray** — AWS native
- **Honeycomb** — comercial, focado em "wide events" e high cardinality

**Em 2026, Tempo + Grafana é a stack open-source mais popular** — integra com Loki e Prometheus via Grafana.

---

## Grafana

**A UI** da observabilidade moderna. Open source, multi-datasource, dashboards poderosos.

### Datasources

- Prometheus, Thanos, Mimir, VictoriaMetrics
- Loki, Elasticsearch, CloudWatch Logs
- Tempo, Jaeger, Zipkin
- PostgreSQL, MySQL, MongoDB
- Datadog, New Relic, Azure Monitor

### Dashboard anatomy

- **Variables** — dropdowns para filtros (environment, service, instance)
- **Panels** — gráficos (time series, gauge, table, heatmap)
- **Rows** — agrupamento visual
- **Annotations** — eventos no gráfico (deploys, incidents)

### Explore

UI ad-hoc para exploração — queries manuais, drill-down, comparação de períodos.

### Loki correlation

Grafana permite **"logs in context"**: clicar em span em Tempo → ver logs correspondentes em Loki via `trace_id`.

### Dashboards as code

```
# JSON exportado do Grafana → git
# Provisionar com grafana-as-code
# Ou usar Grafonnet (Jsonnet) ou Terraform provider
```

**Regra:** dashboards importantes em git, revisados em PR.

---

## Profiling

Quarto pilar emergente. Profile contínuo em produção.

### Conceitos

- **CPU profile** — onde CPU é gasto
- **Memory profile** — alocações, leaks
- **Goroutine profile** (Go) — goroutine count
- **Lock profile** — contention

### Ferramentas

- **Pyroscope** (Grafana, agora) — continuous profiling
- **Parca** — open source
- **Datadog Continuous Profiler**
- **AWS CodeGuru Profiler**

### Uso

Permite responder "por que essa função é lenta?" em **produção**, sem reproduzir localmente.

```
[função A: 40% CPU]
  ├── [função B: 25% CPU]
  │    └── [função C: 15% CPU]
  └── [função D: 15% CPU]
```

Flame graphs visuais — conheça seu perfil, otimize o que importa.

---

## Alertas — princípios

### O que alertar

**Regra de ouro:** **alerte em sintomas, não causas.**

- ✅ "Usuários não conseguem fazer login" (sintoma)
- ❌ "CPU em 90%" (causa — pode ser normal)

**Ou seja, alerte em SLO violations**, não em "o recurso X passou do threshold Y".

### Alertas efetivos

Cada alerta deve:

1. **Indicar um problema real** (não noise)
2. **Ser acionável** (você pode fazer algo)
3. **Ter runbook** (o que fazer quando disparar)
4. **Ter severity** (critical, warning, info)

**Critical** — precisa ação imediata, acorda alguém.
**Warning** — precisa ação no horário de trabalho.
**Info** — FYI, dashboard.

### Anti-patterns

- **Alerta para tudo** — alert fatigue, ignorado
- **Alerta em CPU > 80%** — não é problema até ser
- **Alerta sem runbook** — on-call engineer perdido
- **Pager noise** — acorda ninguém é bom, acorda toda hora é ruim
- **Email alerts** — ninguém lê

### Melhores:

- **PagerDuty / Opsgenie** — pra críticos
- **Slack** — warnings
- **Email** — info, semanal

### On-call hygiene

- **Rotação** — ninguém deve estar on-call full-time
- **Runbooks atualizados** — cada alerta → runbook → solução
- **Post-mortems blameless** — aprenda com incidentes
- **Weekly review** — alertas que dispararam mas não eram ação = ajustar

---

## Debugging incidentes

### Metodologia

**1. Detect** — alerta disparou
**2. Assess** — qual o impacto real? quantos users afetados?
**3. Mitigate** — pare o sangramento (rollback, scale up, feature flag off)
**4. Diagnose** — causa raiz
**5. Fix** — solução definitiva
**6. Learn** — post-mortem

**Key insight:** **mitigar antes de diagnosticar**. Rollback em 30s vale mais que debug perfeito em 30 min.

### Ferramentas na crise

```
1. Dashboard principal — o que está afetado?
2. Deploy history — mudou algo recentemente?
3. Logs com trace_id do error — o que aconteceu?
4. Traces — onde está o gargalo?
5. Metrics por serviço — quem está errado?
6. Kubernetes events — algo mudou no cluster?
```

### 5 Whys

Técnica clássica. Pergunte "por quê?" 5 vezes para chegar à causa raiz.

```
1. Why — site ficou lento
2. Why — database lento
3. Why — query sem índice
4. Why — migração não aplicou índice
5. Why — processo de review não pegou
→ fix: lint em migrations para checar índices
```

### Post-mortem

Blameless. Foco em **systems and processes**, não pessoas.

**Template:**

- Summary (2 parágrafos)
- Timeline
- Root cause
- Impact (quantos users, duração, receita perdida)
- What went well
- What went wrong
- Action items (com owners e prazos)

### Tracking MTTR

**Mean Time To Restore** — quanto tempo entre incidente e resolução. DORA metric.

Meça, acompanhe, reduza. MTTR < 1h é elite tier.

---

## Stack completa open source

**A stack recomendada em 2026:**

```
App → OpenTelemetry SDK → OTel Collector →
    Metrics → Prometheus → Grafana
    Logs    → Loki       → Grafana
    Traces  → Tempo      → Grafana
    Profile → Pyroscope  → Grafana
```

**Vantagens:**

- **Tudo open source**
- **Tudo integrado no Grafana** (uma UI)
- **OpenTelemetry agnóstico** — muda backend sem mudar código
- **Alta correlação** via trace_id entre metrics, logs, traces
- **Cost-effective** — rodar em Kubernetes é cheap

### Alternativa SaaS

- **Datadog** — all-in-one, caro mas excelente
- **New Relic**
- **Honeycomb** — focado em high cardinality
- **Grafana Cloud** — OSS hostado
- **Chronosphere** — Prometheus hostado

**Trade-off:** SaaS é mais caro mas menos operação. OSS é cheaper mas precisa de time para manter.

---

## Cost control

Observability é **cara**. Principal gasto:

- **Volume de logs**
- **Cardinalidade de metrics**
- **Retention**
- **Traces sampled demais**

### Estratégias

**Logs:**

- Não logue DEBUG em produção
- Sample info logs (não errors)
- Retention curta para dev/staging
- S3 para cold storage

**Metrics:**

- Cuidado com labels — no max 1M time series
- Recording rules pré-computadas
- Downsample em retention longa (5m → 1h após 30 dias)

**Traces:**

- Sampling agressivo (1-10%)
- Tail sampling para pegar erros/slow
- Retention curta

**Monitore seu cost de observability.** Meta-observability.

---

## Armadilhas comuns

- **Cardinalidade explosiva** — user_id em label mata Prometheus
- **Logs sem estrutura** — text logs são impossíveis de agregar
- **Sem trace_id em logs** — correlação perdida
- **100% trace sampling** em produção — cost explosion
- **Alertas em causas, não sintomas** — alert fatigue
- **Dashboards sem context** — não sabe o que é "normal"
- **Alertas sem runbook** — pânico na crise
- **Post-mortem com blame** — ninguém reporta incidentes
- **Monitoramento sem SLOs** — não sabe o que é "OK"
- **Logs com secrets** — vazamento + compliance
- **Metrics average apenas** — esconde outliers
- **Summary em vez de histogram** — não agrega
- **No retention strategy** — disco cheio em 6 meses
- **Mistura de stacks (Datadog + Prometheus + X-Ray + ...)** — cost multiply
- **Dev sem observability** — só instrumentam em produção
- **Frontend sem RUM** — blind spot gigante
- **Sem uptime checks externos** — DNS down = nenhuma métrica diz
- **Over-alerting** — ninguém mais lê
- **Under-alerting** — incidentes descobertos por user
- **Trace context não propagado** — traces quebradas
- **Health check sem depth** — "200 OK" mas banco fora
- **Sem budget alerts** — surprise bill
- **Acordar por warning** — Sev diferenciada mal feita

---

## Na prática (da minha experiência)

> **MedEspecialista — stack de observability:**
>
> **OpenTelemetry Collector** recebe tudo de todas as apps (Java, Node, Python, Go), faz processing (drop, sample, enrich) e exporta:
>
> - **Metrics** → Prometheus (local) + remote write para Mimir (retention longa)
> - **Logs** → Loki com labels mínimos (`service`, `env`, `level`)
> - **Traces** → Tempo com tail sampling (100% errors, 5% outros)
> - **UI** — Grafana com datasources integrados
>
> **Padrões que estabeleci:**
>
> **1. trace_id em todo log.** Backend propaga via MDC (Java) ou async_hooks (Node). Frontend gera trace_id e envia no header `traceparent`.
>
> **2. JSON logs sempre.** Pino (Node), Logback Logstash encoder (Java), structlog (Python). Nunca texto.
>
> **3. RED dashboard por serviço.** Rate, Errors, Duration padronizado. Onboarding de novo serviço = criar a partir de template.
>
> **4. SLOs publicados em docs.** Cada serviço tem SLO declarado. Error budget visível no dashboard.
>
> **5. Alertas só em SLO burn rate.** Não alerta em CPU alta ou disco cheio diretamente — só se afetar usuários.
>
> **6. Runbook para cada alerta.** Link direto do alerta → wiki. "Se dispara, faça isso."
>
> **7. Post-mortems blameless.** Template, timeline, action items com owners. Lidos na retrospectiva.
>
> **8. Dashboard de deploy.** Grafana annotation quando deploy acontece. Correlaciona com spike de erros.
>
> **Incidente memorável — cardinalidade matou Prometheus:**
>
> Dev adicionou `user_id` como label em métrica custom "thinking it'd be useful". Prometheus começou a consumir 50GB de RAM, ficou OOM. 30 min de downtime no monitoring. **Lição:** revisão de code em cada custom metric. Label `user_id` = proibido explicitamente em guideline.
>
> **Outro — alertas noisy:**
>
> PagerDuty disparando 5x por noite. On-call engineer esgotado. Investigação: 80% dos alertas eram "flaps" — métrica oscilando perto do threshold. Solução: `for: 5m` em vez de disparar imediatamente, `hysteresis` (threshold alto para disparar, baixo para parar), e revisão mensal de alertas que disparam mas não são ação.
>
> **Terceiro — blind spot em deploy:**
>
> Deploy fora do horário. Métricas começaram a subir, mas on-call só notou no dia seguinte. Causa: alerta em latência não incluía lookback period, disparou no pico mas foi dismissed. Fix: alerta com burn rate (esgotando budget em X horas) + deploy annotation no Grafana + regra "qualquer deploy deve ser acompanhado até 30 min depois".
>
> **A lição principal:** observabilidade é investimento que paga sozinho. Cada incidente que você resolve em 10 min em vez de 10 horas economiza dinheiro. Invista em instrumentação, SLOs claros, alertas disciplinados, e cultura de post-mortem. Sem isso, você voa cego em produção.

---

## How to explain in English

> "Observability in 2026 is the three pillars — logs, metrics, traces — unified under OpenTelemetry with Prometheus for metrics, Loki for logs, Tempo for traces, and Grafana as the query and dashboard layer. All correlated via trace_id so I can move from a latency spike in a metric dashboard to the exact logs and distributed trace for the affected request.
>
> For metrics, I follow the RED method for services — Rate, Errors, Duration — and USE for resources. I'm very disciplined about cardinality; user IDs, request IDs, and any high-cardinality dimensions go in logs or traces, never as Prometheus labels. I've seen teams kill Prometheus by adding user_id to a counter.
>
> For logs, everything is structured JSON with standard fields: timestamp, level, service, trace_id, message. I never log secrets, PII, or huge objects. Log levels are used correctly: INFO for normal events, WARN for anomalies, ERROR for failures.
>
> For traces, OpenTelemetry auto-instrumentation covers most use cases — Express, Spring, HTTP clients, database drivers. Sampling in production is around 5-10%, with 100% of errors and slow traces captured via tail sampling. That keeps cost reasonable while preserving the traces I actually need.
>
> For alerting, the key principle is alerting on symptoms, not causes. I alert on SLO burn rate — if we're consuming error budget too fast, wake someone up. I never alert on 'CPU at 80%' because that's not a problem until users feel it. Every alert has a runbook linked, a severity level, and rotation on-call.
>
> SLOs are published for every service — 99.9% availability, p99 latency under 500ms, whatever makes sense. Error budgets tell the team whether we have room to deploy risky features or need to lock down and fix stability.
>
> For debugging incidents, I mitigate first and diagnose second. Rollback in 30 seconds beats perfect debugging in 30 minutes. Post-mortems are blameless, focused on systems and processes. Every incident produces action items with owners and deadlines.
>
> Common pitfalls I watch for: high cardinality in metrics, text logs without structure, 100% trace sampling in production, alerts without runbooks, and the classic — waking someone up for something that's not actionable."

### Frases úteis em entrevista

- "Observability is answering unknown questions; monitoring is known ones."
- "RED method for services, USE for resources."
- "Cardinality is the enemy — user_id goes in logs, not metric labels."
- "Alert on symptoms, not causes. SLO burn rate, not CPU."
- "Structured JSON logs with trace_id for correlation."
- "Sampling traces at 5% in production with tail sampling for errors."
- "OpenTelemetry unifies everything; backend-agnostic instrumentation."
- "SLOs define what 'good enough' means. Error budget gives you a currency."
- "Mitigate first, diagnose second. Rollback beats debug."
- "Post-mortems are blameless and produce action items with owners."
- "Every alert has a runbook. Every runbook has an owner."

### Key vocabulary

- observabilidade → observability
- monitoramento → monitoring
- registros → logs
- métricas → metrics
- rastros → traces
- pilar → pillar
- cardinalidade → cardinality
- amostragem → sampling
- indicador de nível de serviço → service level indicator (SLI)
- objetivo de nível de serviço → service level objective (SLO)
- acordo de nível de serviço → service level agreement (SLA)
- orçamento de erro → error budget
- sinal dourado → golden signal
- sintoma → symptom
- causa raiz → root cause
- livro de execução → runbook
- post-mortem sem culpa → blameless post-mortem
- tempo médio de restauração → mean time to restore (MTTR)
- tempo médio entre falhas → mean time between failures (MTBF)
- saturação → saturation
- utilização → utilization
- disponibilidade → availability
- confiabilidade → reliability
- latência → latency
- throughput → throughput

---

## Recursos

### Livros

- **Observability Engineering** — Charity Majors, Liz Fong-Jones, George Miranda (Honeycomb team)
- **Site Reliability Engineering** — Google (gratuito online)
- **The SRE Workbook** — Google (gratuito online)
- **Prometheus Up & Running** — Brian Brazil
- **Distributed Tracing in Practice** — Austin Parker et al.

### Documentação

- [Prometheus Docs](https://prometheus.io/docs/)
- [Grafana Docs](https://grafana.com/docs/)
- [OpenTelemetry Docs](https://opentelemetry.io/docs/)
- [Loki Docs](https://grafana.com/docs/loki/latest/)
- [Tempo Docs](https://grafana.com/docs/tempo/latest/)
- [Google SRE Book](https://sre.google/books/)

### Blogs

- [Honeycomb Blog](https://www.honeycomb.io/blog)
- [Grafana Blog](https://grafana.com/blog/)
- [Datadog Blog](https://www.datadoghq.com/blog/)
- [Charity Majors](https://charity.wtf/) — observability thought leader
- [Brendan Gregg](https://www.brendangregg.com/) — performance and flame graphs

### Ferramentas OSS

- [Prometheus](https://prometheus.io/)
- [Grafana](https://grafana.com/)
- [Loki](https://grafana.com/oss/loki/)
- [Tempo](https://grafana.com/oss/tempo/)
- [Mimir](https://grafana.com/oss/mimir/) — Prometheus escalável
- [OpenTelemetry](https://opentelemetry.io/)
- [Jaeger](https://www.jaegertracing.io/)
- [Alertmanager](https://prometheus.io/docs/alerting/latest/alertmanager/)
- [Pyroscope](https://grafana.com/oss/pyroscope/)
- [kube-prometheus-stack](https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack)
- [OpenSearch](https://opensearch.org/) — fork do Elasticsearch
- [Vector](https://vector.dev/) — log/metric router

### SaaS

- [Datadog](https://www.datadoghq.com/)
- [New Relic](https://newrelic.com/)
- [Honeycomb](https://www.honeycomb.io/)
- [Grafana Cloud](https://grafana.com/products/cloud/)
- [Splunk](https://www.splunk.com/)
- [Chronosphere](https://chronosphere.io/)

---

## Veja também

- [[Docker]] — container stdout/stderr
- [[Kubernetes]] — metrics, logs, probes
- [[Linux]] — system metrics
- [[Nginx]] — access logs, stub_status
- [[CI-CD]] — pipeline observability
- [[System Design]] — observability em arquitetura
- [[Java Concurrency]] — JFR, thread dumps
- [[Spring Boot]] — Actuator, Micrometer
- [[Node.js]] — prom-client, pino
- [[API Design]] — trace correlation via trace_id
