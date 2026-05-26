---
title: "SLOs, dashboards, alertas e cheatsheet"
created: 2026-05-09
updated: 2026-05-09
type: concept
status: seedling
publish: true
tags:
  - node
  - observability
  - slo
  - sli
  - alertas
  - grafana
  - prometheus
  - cheatsheet
---

# SLOs, dashboards, alertas e cheatsheet

> [!abstract] TL;DR
> - **SLI** é a medição real (ex: % de requests bem-sucedidas); **SLO** é o alvo acordado internamente (ex: 99,9%); **SLA** é o contrato externo com penalidades — sempre viole o SLO antes de chegar no SLA.
> - **Error budget** = 1 − SLO target: com 99,9% de alvo, você tem 0,1% de falhas permitidas (43,8 min/mês). Quando o budget acaba, para de lançar features até estabilizar.
> - **Burn rate** quantifica quão rápido você consome o budget — alertas multi-janela (1 h + 6 h) capturam queimas rápidas E lentas sem alert fatigue.
> - Dashboard Grafana de referência tem 5 painéis: availability gauge, latency p50/p95/p99, error budget burndown, throughput (RPS) e saturação.
> - Alertmanager roteia `critical` (PagerDuty) e `warning` (Slack) com deduplicação por grupo e `repeat_interval` distintos.

SLOs transformam "o sistema está lento" em uma conversa concreta: quanto do orçamento de erros já foi consumido este mês? Isso alinha produto, engenharia e operações em torno de uma métrica compartilhada em vez de percepções subjetivas de qualidade. Este guia cobre a cadeia completa — definir SLIs em PromQL, calcular burn rate, configurar alertas multi-janela, montar o dashboard de referência e finalizar com o cheatsheet consolidado de toda a trilha de Observability e produção.

## O que é

**SLI (Service Level Indicator)** é uma medição quantitativa real de comportamento do serviço: percentual de requests com status 2xx, latência p99, disponibilidade calculada em janela de tempo. É sempre uma fração ou percentil — um número entre 0 e 1 (ou 0% e 100%).

**SLO (Service Level Objective)** é o alvo interno acordado para um SLI: "99,9% das requests retornam status 2xx". Não tem penalidade formal — é um sinal de operação saudável.

**SLA (Service Level Agreement)** é o contrato externo com o cliente, normalmente menos rigoroso que o SLO e com penalidades financeiras. A ideia é que o SLO seja mais difícil de bater que o SLA: você viola o SLO antes do SLA, o que dá tempo de agir.

**Error budget** é o complemento do SLO:

```
error_budget = 1 - SLO_target

Exemplo: SLO = 99,9%
  error_budget = 0,1%
  Em um mês de 30 dias (43.200 min):
    43.200 × 0,001 = 43,2 minutos de indisponibilidade permitida
```

Quando o budget acaba antes do fim do mês, a política padrão é congelar lançamentos de features e priorizar confiabilidade. Quando sobra budget, a equipe pode aceitar mais risco (ex: deploys sem staging).

## Por que importa

Alertar em cada anomalia cria alert fatigue: oncall ignora alertas porque 90% são falsos positivos ou não requerem ação imediata. SLOs invertem esse racional — você só alerta quando o serviço está consumindo error budget mais rápido do que o sustentável para o mês.

A consequência prática é que engenheiros dormem melhor (menos alertas noturnos desnecessários) e o product manager tem uma linguagem clara para negociar prioridades: "gastamos 80% do budget este mês com esse bug, então a próxima sprint vai para confiabilidade". Sem SLOs esse trade-off é sempre subjetivo.

Por fim, SLOs expõem dependências ocultas. Quando seu serviço tem 99,95% de disponibilidade mas chama dois serviços com 99,9% cada, sua disponibilidade real é 99,95% × 99,9% × 99,9% ≈ 99,75% — abaixo do SLO. O error budget torna essa matemática visível.

## Como funciona

### SLIs como queries PromQL

Um SLI de disponibilidade mede a fração de requests bem-sucedidas em uma janela de tempo:

```promql
# SLI de disponibilidade — fração de requests não-5xx em janela de 5 min
sum(rate(http_requests_total{status!~"5.."}[5m]))
  /
sum(rate(http_requests_total[5m]))

# SLI de latência — fração de requests abaixo de 300 ms
sum(rate(http_request_duration_seconds_bucket{le="0.3"}[5m]))
  /
sum(rate(http_request_duration_seconds_count[5m]))

# Recording rule (pré-compute para burn rate e alertas)
# Salva no Prometheus como slo:sli_error:ratio_rate5m
record: slo:sli_error:ratio_rate5m
expr: |
  1 - (
    sum(rate(http_requests_total{status!~"5.."}[5m]))
    / sum(rate(http_requests_total[5m]))
  )
```

Recording rules são essenciais: o burn rate precisa da taxa de erro calculada em múltiplas janelas (5m, 30m, 1h, 6h) e recomputar isso em cada painel do Grafana é ineficiente e inconsistente.

### Error budget e burn rate

Burn rate é a velocidade de consumo do error budget em relação à baseline mensal:

```
burn_rate = error_rate_atual / (1 - SLO_target)

Exemplo: SLO = 99,9%, error_rate atual = 1,44%
  burn_rate = 0,0144 / 0,001 = 14,4×

Interpretação: consumindo budget 14,4× mais rápido que o sustentável.
Com burn rate 14,4×, o budget mensal acaba em ≈ 2 dias (30 dias ÷ 14,4 ≈ 50 horas).
```

A escolha dos limiares de alerta é padronizada pela Google SRE:
- **14,4× burn rate** (janela de 1h): queima rápida — página o oncall imediatamente
- **6× burn rate** (janela de 6h): queima moderada — ticket, monitora de perto
- **3× burn rate** (janela de 3 dias): queima lenta — revisão semanal

### Alertas multi-janela

O padrão multi-janela usa duas janelas para cada limiar: uma curta (detecta queima em andamento) e uma longa (confirma que não é um spike isolado). Isso elimina alertas falsos de spikes de 30 segundos.

```yaml
groups:
  - name: slo_alerts
    rules:
      # Recording rules — pré-computadas para uso nos alertas
      - record: slo:sli_error:ratio_rate5m
        expr: |
          1 - (sum(rate(http_requests_total{status!~"5.."}[5m]))
               / sum(rate(http_requests_total[5m])))
      - record: slo:sli_error:ratio_rate30m
        expr: |
          1 - (sum(rate(http_requests_total{status!~"5.."}[30m]))
               / sum(rate(http_requests_total[30m])))
      - record: slo:sli_error:ratio_rate1h
        expr: |
          1 - (sum(rate(http_requests_total{status!~"5.."}[1h]))
               / sum(rate(http_requests_total[1h])))
      - record: slo:sli_error:ratio_rate6h
        expr: |
          1 - (sum(rate(http_requests_total{status!~"5.."}[6h]))
               / sum(rate(http_requests_total[6h])))
      - record: slo:sli_error:ratio_rate3d
        expr: |
          1 - (sum(rate(http_requests_total{status!~"5.."}[3d]))
               / sum(rate(http_requests_total[3d])))

      # Alerta crítico: burn rate 14.4× em 1h OU 6× em 6h
      - alert: HighErrorBudgetBurn
        expr: |
          (
            slo:sli_error:ratio_rate1h > (14.4 * 0.001)
            and
            slo:sli_error:ratio_rate5m > (14.4 * 0.001)
          )
          or
          (
            slo:sli_error:ratio_rate6h > (6 * 0.001)
            and
            slo:sli_error:ratio_rate30m > (6 * 0.001)
          )
        for: 2m
        labels:
          severity: critical
          service: my-service
          team: backend
        annotations:
          summary: "High error budget burn rate"
          description: "{{ $labels.service }} está queimando o error budget {{ $value | humanizePercentage }} mais rápido que o alvo"

      # Alerta de aviso: burn rate 3× em 3 dias (multi-janela: 3d longa + 6h curta)
      - alert: LowErrorBudgetBurn
        expr: |
          slo:sli_error:ratio_rate3d > (3 * 0.001)
          and
          slo:sli_error:ratio_rate6h > (3 * 0.001)
        for: 1h
        labels:
          severity: warning
          service: my-service
          team: backend
        annotations:
          summary: "Slow error budget burn — review this week"
```

O valor `0.001` é `1 - SLO_target` para um SLO de 99,9%. Para 99,95%, use `0.0005`.

### Dashboard Grafana — 5 painéis

O dashboard de referência para um serviço Node.js tem exatamente 5 painéis, organizados em duas linhas:

**Linha 1 — Estado atual (gauges e números)**

| Painel | Tipo | PromQL |
| ------ | ---- | ------ |
| 1. Availability | Gauge (verde/vermelho) | `1 - slo:sli_error:ratio_rate1h` |
| 2. Latência p50/p95/p99 | Time series | `histogram_quantile(N, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))` com N = 0.5, 0.95, 0.99 — três séries no mesmo painel |

**Linha 2 — Tendências (time series)**

| Painel | Tipo | PromQL |
| ------ | ---- | ------ |
| 3. Error budget burndown | Time series | `(sum(increase(http_requests_total{status!~"5.."}[30d])) / sum(increase(http_requests_total[30d])) - 0.999) / 0.001` |
| 4. Throughput (RPS) | Time series | `sum(rate(http_requests_total[5m])) by (status)` |
| 5. Saturação | Time series | `db_pool_pending_acquires`, `rate(process_cpu_seconds_total[5m])`, `process_heap_used_bytes` |

O painel de burndown mostra um número que começa em 1 (100% do budget disponível no início do mês) e decresce. Se chega a 0 antes do fim do mês, o SLO foi violado.

### Routing no Alertmanager

```yaml
# alertmanager.yml
global:
  resolve_timeout: 5m

route:
  receiver: default
  group_by: [alertname, service, team]
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h
  routes:
    - match:
        severity: critical
      receiver: pagerduty
      repeat_interval: 1h
      continue: false
    - match:
        severity: warning
      receiver: slack
      repeat_interval: 4h

receivers:
  - name: default
    slack_configs:
      - api_url: '<WEBHOOK_URL>'
        channel: '#alerts-backend'
        title: '[{{ .Status | toUpper }}] {{ .CommonAnnotations.summary }}'

  - name: pagerduty
    pagerduty_configs:
      - service_key: '<SECRET>'
        description: '{{ .CommonAnnotations.description }}'

  - name: slack
    slack_configs:
      - api_url: '<WEBHOOK_URL>'
        channel: '#alerts-backend'
        title: '[WARNING] {{ .CommonAnnotations.summary }}'
        text: '{{ .CommonAnnotations.description }}'

inhibit_rules:
  - source_match:
      severity: critical
    target_match:
      severity: warning
    equal: [alertname, service]
```

A regra `inhibit_rules` suprime alertas `warning` quando um `critical` do mesmo serviço já está ativo — evita inundar Slack enquanto PagerDuty está acionado.

## Na prática

Exemplo completo: serviço Node.js com SLIs expostos, recording rules em ConfigMap Kubernetes e histograma com buckets alinhados ao target de latência (300ms).

```typescript
// src/metrics.ts
import { Registry, Histogram, Counter, Gauge, collectDefaultMetrics } from 'prom-client';

export const registry = new Registry();
collectDefaultMetrics({ register: registry, prefix: 'node_' });

export const httpRequestDuration = new Histogram({
  name: 'http_request_duration_seconds',
  help: 'Duration of HTTP requests in seconds',
  labelNames: ['method', 'route', 'status'],
  // buckets alinhados ao SLI target de 300ms
  buckets: [0.01, 0.05, 0.1, 0.2, 0.3, 0.5, 1, 2, 5],
  registers: [registry],
});

export const httpRequestsTotal = new Counter({
  name: 'http_requests_total',
  help: 'Total number of HTTP requests',
  labelNames: ['method', 'route', 'status'],
  registers: [registry],
});

export const dbPoolPending = new Gauge({
  name: 'db_pool_pending_acquires',
  help: 'Number of requests waiting for a DB connection',
  registers: [registry],
});

// Middleware Express para instrumentação automática
export function metricsMiddleware(req: Request, res: Response, next: NextFunction) {
  const end = httpRequestDuration.startTimer({
    method: req.method,
    route: req.route?.path ?? req.path,
  });
  res.on('finish', () => {
    const labels = { method: req.method, route: req.route?.path ?? req.path, status: String(res.statusCode) };
    end(labels);
    httpRequestsTotal.inc(labels);
  });
  next();
}

// Endpoint /metrics
app.get('/metrics', async (_req, res) => {
  res.set('Content-Type', registry.contentType);
  res.end(await registry.metrics());
});
```

```yaml
# k8s/prometheus-rule.yml — ConfigMap com recording rules e alertas
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: slo-rules
  namespace: backend
  labels:
    prometheus: kube-prometheus
spec:
  groups:
    - name: slo_recording
      interval: 30s
      rules:
        - record: slo:sli_error:ratio_rate5m
          expr: |
            1 - (
              sum(rate(http_requests_total{status!~"5.."}[5m]))
              / sum(rate(http_requests_total[5m]))
            )
        - record: slo:sli_error:ratio_rate30m
          expr: |
            1 - (
              sum(rate(http_requests_total{status!~"5.."}[30m]))
              / sum(rate(http_requests_total[30m]))
            )
        - record: slo:sli_error:ratio_rate1h
          expr: |
            1 - (
              sum(rate(http_requests_total{status!~"5.."}[1h]))
              / sum(rate(http_requests_total[1h]))
            )
        - record: slo:sli_error:ratio_rate6h
          expr: |
            1 - (
              sum(rate(http_requests_total{status!~"5.."}[6h]))
              / sum(rate(http_requests_total[6h]))
            )
        - record: slo:sli_error:ratio_rate3d
          expr: |
            1 - (
              sum(rate(http_requests_total{status!~"5.."}[3d]))
              / sum(rate(http_requests_total[3d]))
            )

    - name: slo_alerts
      rules:
        - alert: HighErrorBudgetBurn
          expr: |
            (slo:sli_error:ratio_rate1h > (14.4 * 0.001) and slo:sli_error:ratio_rate5m > (14.4 * 0.001))
            or
            (slo:sli_error:ratio_rate6h > (6 * 0.001) and slo:sli_error:ratio_rate30m > (6 * 0.001))
          for: 2m
          labels:
            severity: critical
            service: my-service
            team: backend
          annotations:
            summary: "Error budget burn too high"
```

## Em entrevista

**How do you approach setting and monitoring SLOs for a Node.js service?**

I start by identifying the right SLIs — for most APIs that means availability (fraction of non-5xx responses) and latency (fraction of responses under a target threshold like 300ms). I avoid using averages as SLIs because they hide tail latency: a p99 of 2 seconds is invisible in the average if 98% of requests are fast.

For setting the initial SLO target, I look at 30 days of historical data and pick the p30 of the availability distribution — something the service already achieves comfortably. I then tighten the target each quarter as reliability improves. Starting at 99.99% on day one without data is a fast path to alert fatigue.

Once the SLI and SLO are defined, I define the error budget as `1 - SLO_target`, then configure multi-window burn rate alerts: 14.4× over one hour triggers a page, 6× over six hours triggers a ticket. The two-window approach is critical — a single-window alert on the one-hour window can page on a 30-second spike that self-resolves before anyone responds.

For the dashboard I use five panels: an availability gauge colored by SLO threshold, a latency time series showing p50/p95/p99, an error budget burndown showing what fraction of the monthly budget remains, throughput in RPS, and saturation metrics (pool pending acquires, CPU, heap). The burndown panel is the most actionable — if it crosses 50% at the start of week three, I know we have a reliability story for the next sprint.

Finally, I make sure the error budget feeds into planning. If a team ships frequently and the SLO holds, great — more deployments are safe. If the error budget is almost gone, feature work stops until we fix it. That's how SLOs create accountability without micromanagement.

## Vocabulário

| PT | EN |
| -- | -- |
| indicador de nível de serviço | Service Level Indicator (SLI) |
| objetivo de nível de serviço | Service Level Objective (SLO) |
| acordo de nível de serviço | Service Level Agreement (SLA) |
| orçamento de erros | error budget |
| taxa de queima | burn rate |
| disponibilidade | availability |
| saturação | saturation |
| alerta multi-janela | multi-window alert |
| painel de burndown | burndown panel |
| regra de gravação | recording rule |
| inibição de alerta | alert inhibition |
| percentil de latência | latency percentile |

## Armadilhas

> [!warning] SLO apertado demais sem dados históricos
> Começar com 99,99% sem validar se o serviço já atinge isso gera alert fatigue imediato. O SLO inicial deve refletir a confiabilidade real atual — comece conservador e aperte com dados.

> [!warning] Alerta em symptom sem investigar causa
> Alertar em "latência alta" sem links para traces (Jaeger) ou profiles (clinic.js) faz o oncall acordar sem saber o que verificar. O alerta deve incluir um runbook com os primeiros três passos de diagnóstico.

> [!warning] Error budget ignorado no planejamento de produto
> Se o error budget não influencia decisões de sprint (feature freeze quando budget acaba), ele vira métrica decorativa. O budget precisa de uma política escrita: quem decide parar lançamentos e quando.

> [!warning] Alerta de janela única captura só queimas rápidas
> Um alerta só na janela de 1 hora detecta incidentes agudos mas não queimas lentas de 3–4 dias que consomem o budget silenciosamente. Use sempre o par (janela curta AND janela longa) para cada nível de burn rate.

> [!warning] Usar média de latência como SLI
> A latência média é inútil como SLI: se 1% das requests demoram 10 segundos e 99% demoram 10ms, a média é ≈ 110ms — parece saudável enquanto 1% dos usuários sofrem. Use sempre percentis (p95, p99) como SLI de latência.

> [!warning] Recording rules ausentes causam inconsistência
> Calcular o mesmo SLI diretamente em cada painel do Grafana e em cada regra de alerta resulta em valores ligeiramente diferentes (janelas de avaliação distintas). Defina recording rules canônicas no Prometheus e referencie-as em todos os lugares.

## Cheatsheet consolidado

Esta seção resume toda a trilha **Observability e produção** em tabelas de referência rápida para entrevistas e revisão técnica.

### Ferramentas por categoria

| Categoria | Ferramenta | Quando usar |
| --------- | ---------- | ----------- |
| Logging | pino | Produção — performance máxima e JSON estruturado |
| Logging | winston | Legado ou múltiplos transports críticos |
| Métricas | prom-client | Qualquer serviço Node.js com Prometheus |
| Tracing | @opentelemetry/sdk-node | Microsserviços — rastrear requests entre serviços |
| Profiling | clinic.js | Diagnóstico local de CPU, memória e event loop |
| Circuit breaker | opossum | Chamadas HTTP e DB com necessidade de fallback |
| Pool DB | knex + tarn | PostgreSQL com controle fino de pool por pod |
| Pool DB | Prisma | ORM com pool via `connection_limit` na DATABASE_URL |
| SLO / alertas | Prometheus + Alertmanager | Stack completo de métricas, recording rules e alertas |
| Dashboard | Grafana | Visualização de SLIs, burndown e saturação |

### Checklist de produção

- [ ] Logging estruturado (pino) com correlation ID em cada request
- [ ] Métricas de RED (Rate, Errors, Duration) expostas em `/metrics`
- [ ] SLIs definidos como PromQL com recording rules pré-computadas
- [ ] Alertas multi-janela de burn rate configurados (14,4× e 6×)
- [ ] Dashboard Grafana com 5 painéis essenciais (availability, latency, burndown, RPS, saturation)
- [ ] Graceful shutdown com SIGTERM + draining de requests em andamento
- [ ] Circuit breaker em chamadas externas críticas (opossum com fallback)
- [ ] Pool dimensionado por pod: `pool_por_pod = (max_connections × 0,8) / num_pods`
- [ ] Memory leak monitorado via `process_heap_used_bytes` + clinic.js em staging
- [ ] Correlation ID propagado via AsyncLocalStorage através de toda a stack

### Comandos de diagnóstico rápido

| Problema suspeito | Comando / abordagem |
| ----------------- | ------------------- |
| Event loop travado | `clinic doctor -- node server.js` |
| Memory leak | `node --inspect` + heap snapshot no Chrome DevTools |
| Pool DB exausto | `SELECT state, count(*) FROM pg_stat_activity WHERE datname = 'mydb' GROUP BY state` |
| Request lento (qual span?) | Jaeger UI → buscar trace por `correlation-id` do log |
| Latência alta (qual função?) | `clinic flame -- node server.js` |
| Circuit breaker aberto? | `GET /health` → checar campo `circuitBreaker.opened` |
| Burn rate alto (qual endpoint?) | Grafana → breakdown por `route` label no painel de errors |
| Container OOM killed | `kubectl describe pod` → `OOMKilled`; reduzir `--max-old-space-size` |

### Configurações de referência por ferramenta

| Ferramenta | Parâmetro | Valor típico | Observação |
| ---------- | --------- | ------------ | ---------- |
| knex | `acquireTimeoutMillis` | `30_000` | Falha explícita antes do timeout do cliente HTTP |
| knex | `max` (pool) | `10` | Ajustar por pod: `(max_conn × 0,8) / pods` |
| knex | `idleTimeoutMillis` | `10_000` | Fecha conexões ociosas antes do timeout do servidor |
| Prisma | `connection_limit` | `10` | Na `DATABASE_URL` após `?connection_limit=10` |
| Prisma | `pool_timeout` | `30` | Segundos antes de lançar erro de pool exausto |
| opossum | `timeout` | `3_000` | 3× o p95 de latência normal do serviço dependente |
| opossum | `errorThresholdPercentage` | `50` | Abre após 50% de falhas na janela de stats |
| opossum | `resetTimeout` | `10_000` | Tenta fechar (half-open) após 10 s |
| pino | `level` | `'info'` em prod | `'debug'` só em staging ou com feature flag |
| prom-client | `collectDefaultMetrics` interval | `10_000` | 10 s é granularidade suficiente para Prometheus 15s scrape |
| Alertmanager | `group_wait` | `30s` | Aguarda antes de enviar o primeiro alerta do grupo |
| Alertmanager | `repeat_interval` critical | `1h` | Repete página se incidente não resolvido |
| Alertmanager | `repeat_interval` warning | `4h` | Slack não fica spam para alertas de aviso |

### Padrões e anti-padrões — decisões rápidas

| Situação | Fazer | Evitar |
| -------- | ----- | ------ |
| SLO inicial sem dados | p30 da disponibilidade histórica | 99,99% arbitrário |
| Latência como SLI | p95 ou p99 de requests | Média (oculta tail) |
| Alerta de queima | Janela curta AND longa (multi-window) | Janela única |
| Transaction no knex | `try/catch` com `rollback` explícito | `async/await` sem catch no callback |
| Circuit breaker aberto | Retornar fallback (cache ou valor degradado) | Propagar erro para o cliente |
| Pool em ambiente multi-pod | `pool = (max_conn × 0,8) / pods` | Pool fixo sem considerar escala |
| Métricas Prisma | `prisma_pool_connections_busy` (sobe com pressão) | `prisma_pool_connections_idle` (sinal invertido) |
| Logging de erros | `logger.error({ err, correlationId }, 'msg')` | `console.error(err.message)` (perde stack e contexto) |

## Veja também

- [[MOC - Observability e produção]]
- [[01 - Os três pilares]]
- [[04 - Métricas com prom-client]]
- [[06 - Tracing distribuído com OpenTelemetry]]
- [[09 - Graceful shutdown profundo]]
- [[10 - Circuit breaker e fallback com opossum]]
- [[11 - Connection pool tuning]]

## Fontes

- [Prometheus — Recording rules](https://prometheus.io/docs/prometheus/latest/configuration/recording_rules/)
- [Prometheus — Alerting rules](https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/)
- [Grafana — SLO overview](https://grafana.com/docs/grafana/latest/dashboards/build-dashboards/best-practices/)
- [Google SRE Book — Chapter 4: Service Level Objectives](https://sre.google/sre-book/service-level-objectives/)
- [Google SRE Workbook — Alerting on SLOs](https://sre.google/workbook/alerting-on-slos/)
- [OpenSLO specification](https://openslo.com/)
