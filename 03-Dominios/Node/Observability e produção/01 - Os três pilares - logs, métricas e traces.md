---
title: "Os três pilares: logs, métricas e traces"
created: 2026-05-08
updated: 2026-05-08
type: concept
status: seedling
publish: true
tags:
  - node
  - observability
  - logs
  - metricas
  - traces
  - slo
  - sli
aliases:
  - Observability Node
  - Três pilares
  - Golden signals
---

# Os três pilares: logs, métricas e traces

> [!abstract] TL;DR
> Observability é a capacidade de entender o estado interno de um sistema a partir de suas saídas externas.
> Os três pilares — logs, métricas e traces — respondem perguntas diferentes e se complementam: logs explicam *o quê* aconteceu, métricas mostram *quantas vezes* e *quão rápido*, traces revelam *onde* o tempo foi gasto numa requisição distribuída.
> Golden signals (latência, tráfego, erros, saturação) são o subconjunto mínimo de métricas que toda API em produção deve monitorar.
> SLI define o que medir, SLO define a meta, SLA define a consequência contratual — confundir os três é erro clássico em entrevista e em PRs de infra.

Esta nota é a porta de entrada do [[03-Dominios/Node/Observability e produção/index]] e estabelece o vocabulário e o modelo mental usados em todas as notas do galho. Leia-a antes de qualquer outra.

## O que é

**Observability** (observabilidade) é a propriedade de um sistema que permite inferir seu estado interno a partir das saídas que ele emite para o ambiente externo. O termo vem da teoria de controle: um sistema é "observável" se, dados os outputs suficientes, é possível reconstruir o estado interno sem instrumentação adicional.

Na prática de engenharia de software, observability se traduz em três tipos de dados que um sistema emite:

| Pilar | Pergunta respondida | Cardinalidade | Custo de armazenamento | Caso de uso típico |
|---|---|---|---|---|
| **Logs** | O que aconteceu? Qual foi o contexto? | Alta (cada evento é único) | Alto (texto, volume cresce com tráfego) | Debug de erros pontuais, auditoria, rastreamento de fluxo |
| **Métricas** | Quantas vezes? Quão rápido? Quão cheio? | Baixa (agregações numéricas) | Baixo (séries temporais comprimíveis) | Alertas, dashboards, SLO tracking, capacity planning |
| **Traces** | Onde o tempo foi gasto? Qual serviço causou a lentidão? | Média (uma árvore de spans por requisição) | Médio (dependente de sampling rate) | Diagnóstico de latência, mapeamento de dependências, debugging distribuído |

Os três pilares **não são substitutos entre si** — são lentes complementares sobre o mesmo sistema. Um incidente típico começa com uma métrica fora do threshold (alerta dispara), usa traces para identificar qual serviço ou operação é o gargalo, e termina com logs para entender o contexto exato do erro.

## Por que importa

Em desenvolvimento local, erros são visíveis no terminal e reproduzíveis na sua máquina. Em produção, você não tem acesso ao processo em execução, não pode pausar o tempo, e o estado que causou o problema pode ter desaparecido antes de você ser notificado.

Sem observability, o ciclo de debugging em produção é: receber reclamação do usuário → tentar reproduzir localmente (muitas vezes impossível) → adicionar logs → fazer deploy → esperar o problema se repetir. Esse ciclo pode levar horas ou dias.

Com observability bem instrumentada:

- **Detecção proativa**: alertas disparam antes que usuários reportem problemas.
- **Diagnóstico rápido**: você sabe exatamente qual serviço, qual operação e qual linha de código está falhando.
- **Redução de MTTR**: Mean Time To Recovery cai de horas para minutos.
- **Confiança em deploys**: ao instrumentar os golden signals, você sabe em segundos se um deploy degradou performance.

Node.js em particular merece atenção especial em observability porque seu modelo single-thread significa que um problema de performance ou memory leak afeta *todas* as requisições simultâneas — não apenas as de um usuário específico. O impacto é global e imediato.

## Como funciona

### Os três pilares em detalhe

Os três pilares instrumentam a mesma operação de formas diferentes. O exemplo abaixo mostra a operação "criar usuário" instrumentada com cada um dos três pilares separadamente:

**Logs** — capturam o contexto narrativo de um evento específico:

```javascript
// Usando pino (logging estruturado)
import pino from 'pino';

const logger = pino({ level: 'info' });

async function criarUsuario(dados) {
  const requestId = dados.requestId;

  logger.info(
    { requestId, email: dados.email, action: 'user.create.start' },
    'Iniciando criação de usuário'
  );

  try {
    const usuario = await db.usuarios.inserir(dados);

    logger.info(
      {
        requestId,
        userId: usuario.id,
        email: usuario.email,
        action: 'user.create.success',
        durationMs: Date.now() - dados.startTime,
      },
      'Usuário criado com sucesso'
    );

    return usuario;
  } catch (err) {
    logger.error(
      {
        requestId,
        email: dados.email,
        action: 'user.create.error',
        err: { message: err.message, code: err.code },
      },
      'Falha ao criar usuário'
    );
    throw err;
  }
}
```

O log gerado em caso de sucesso seria um JSON como:

```json
{
  "level": 30,
  "time": 1746700800000,
  "pid": 12345,
  "requestId": "req-abc-123",
  "userId": 42,
  "email": "joao@exemplo.com",
  "action": "user.create.success",
  "durationMs": 47,
  "msg": "Usuário criado com sucesso"
}
```

**Métricas** — capturam agregações numéricas ao longo do tempo:

```javascript
// Usando prom-client
import { Counter, Histogram } from 'prom-client';

const userCreateTotal = new Counter({
  name: 'user_create_total',
  help: 'Total de tentativas de criação de usuário',
  labelNames: ['status'], // 'success' | 'error'
});

const userCreateDuration = new Histogram({
  name: 'user_create_duration_seconds',
  help: 'Duração da criação de usuário em segundos',
  buckets: [0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1],
});

async function criarUsuario(dados) {
  const end = userCreateDuration.startTimer();

  try {
    const usuario = await db.usuarios.inserir(dados);
    userCreateTotal.inc({ status: 'success' });
    end(); // registra a duração no histogram
    return usuario;
  } catch (err) {
    userCreateTotal.inc({ status: 'error' });
    end();
    throw err;
  }
}
```

**Traces** — capturam o fluxo de execução com timestamps precisos:

```javascript
// Usando OpenTelemetry
import { trace, SpanStatusCode } from '@opentelemetry/api';

const tracer = trace.getTracer('user-service', '1.0.0');

async function criarUsuario(dados) {
  return tracer.startActiveSpan('user.create', async (span) => {
    span.setAttributes({
      'user.email': dados.email,
      'db.system': 'postgresql',
      'db.operation': 'insert',
    });

    try {
      const usuario = await db.usuarios.inserir(dados);
      span.setAttributes({ 'user.id': usuario.id });
      span.setStatus({ code: SpanStatusCode.OK });
      return usuario;
    } catch (err) {
      span.recordException(err);
      span.setStatus({
        code: SpanStatusCode.ERROR,
        message: err.message,
      });
      throw err;
    } finally {
      span.end();
    }
  });
}
```

A diferença fundamental:
- O **log** diz "às 10:32:15, o usuário joao@exemplo.com foi criado com ID 42 em 47ms."
- A **métrica** diz "entre 10h e 11h, 1.247 usuários foram criados, p99 de latência = 89ms, taxa de erro = 0.3%."
- O **trace** diz "esta requisição específica levou 47ms no total: 2ms na validação, 44ms no INSERT do banco, 1ms na serialização da resposta."

### Golden signals

Golden signals são os quatro indicadores definidos pelo Google SRE como o mínimo suficiente para monitorar qualquer serviço. Cada um responde a uma pergunta diferente sobre a saúde do sistema:

| Signal | Pergunta | Métrica típica |
|---|---|---|
| **Latency** | Quão rápido respondemos? | p50, p95, p99 de duração das requisições |
| **Traffic** | Quanta carga estamos recebendo? | Requests por segundo (RPS) |
| **Errors** | Com que frequência falhamos? | Taxa de erros (5xx / total) |
| **Saturation** | Quão próximos do limite estamos? | CPU %, heap usado, connection pool ocupado |

Exemplos de queries PromQL para cada golden signal:

```promql
# Latency — p99 de duração das requisições HTTP nos últimos 5 minutos
histogram_quantile(
  0.99,
  sum(rate(http_request_duration_seconds_bucket[5m])) by (le, route)
)

# Traffic — taxa de requisições por segundo, por rota
sum(rate(http_requests_total[1m])) by (route, method)

# Errors — proporção de requisições com status 5xx
sum(rate(http_requests_total{status=~"5.."}[5m]))
  /
sum(rate(http_requests_total[5m]))

# Saturation — uso do heap Node.js como percentual do limite
nodejs_heap_used_bytes / nodejs_heap_size_limit_bytes
```

A filosofia por trás dos golden signals: em vez de monitorar dezenas de métricas internas (e se perder em falsos positivos), foque nos quatro indicadores que os *usuários percebem diretamente*. Se latência, tráfego, erros e saturação estão dentro do esperado, o serviço está saudável do ponto de vista do usuário.

### SLI, SLO e SLA

Esses três termos formam a hierarquia de confiabilidade que todo time de produção precisa dominar:

**SLI — Service Level Indicator** (Indicador de nível de serviço)
Uma métrica mensurável e específica que representa a qualidade do serviço. O SLI é o *o quê* você mede.

Exemplos:
- Proporção de requisições respondidas em menos de 200ms
- Disponibilidade medida como `(requisições bem-sucedidas / total de requisições) × 100%`
- Taxa de erros da API de pagamentos

**SLO — Service Level Objective** (Objetivo de nível de serviço)
Uma meta para um SLI, medida em uma janela de tempo. O SLO é o *quanto* você quer atingir.

Exemplos:
- "p99 de latência < 200ms em 99,9% do tempo, medido em janela de 30 dias"
- "Disponibilidade >= 99,95% por mês"
- "Taxa de erros da API de pagamentos < 0,1% por semana"

**SLA — Service Level Agreement** (Acordo de nível de serviço)
Um contrato *formal e externo* com o cliente, geralmente com consequências financeiras (créditos, reembolsos) em caso de descumprimento. O SLA é baseado no SLO, mas tipicamente com meta menos agressiva para dar margem de segurança.

Exemplo prático completo para uma API de criação de usuários:

| Camada | Definição |
|---|---|
| SLI | `rate(http_requests_total{route="/users",status=~"2.."}[30d]) / rate(http_requests_total{route="/users"}[30d])` |
| SLO | Disponibilidade >= 99,9% (permite ~43 minutos de downtime por mês) |
| SLA | Disponibilidade >= 99,5% (cliente recebe crédito se cair abaixo disso) |

O **error budget** deriva do SLO: se o SLO é 99,9%, o time tem um orçamento de 0,1% de erros para gastar em deploys, manutenções e incidentes. Quando o error budget se esgota, o time para deploys até o orçamento ser reposto no próximo período.

### O triângulo de diagnóstico

Logs, métricas e traces formam um triângulo de diagnóstico que é a base do processo de debugging em produção. Cada vértice é um ponto de entrada diferente para um incidente:

```
Alerta (métrica) → identifica QUE há um problema e sua magnitude
        |
        v
Trace  → identifica ONDE na cadeia de chamadas o problema está
        |
        v
Log    → explica O QUÊ exatamente aconteceu e qual foi o contexto
```

Exemplo de workflow num incidente real:

1. **Alerta dispara**: "p99 de latência da rota `POST /users` ultrapassou 500ms."
2. **Métricas**: o dashboard mostra que a latência aumentou às 14h32, coincidindo com um deploy. O aumento é específico para a rota `/users`.
3. **Traces**: filtrando traces lentos da rota `/users` após 14h32, percebe-se que o span `db.query` está levando 450ms em média — antes era 8ms.
4. **Logs**: filtrando logs com `action: "user.create.start"` e `durationMs > 200`, encontra-se que todas as queries lentas incluem o atributo `plan: "Seq Scan"` no log do PostgreSQL — indicando ausência de índice.

O diagnóstico completo — da detecção até a causa raiz — foi possível porque os três pilares estavam correlacionados via `requestId` (nos logs e spans) e via timestamps alinhados.

A chave para o triângulo funcionar é a **correlação**: o mesmo `traceId` que aparece no span deve aparecer no log da mesma requisição. Isso é feito via context propagation, que é o tema da nota [[03 - Correlation IDs e context propagation]].

## Na prática

Cenário: uma rota `POST /users` que cria um usuário. Veja como cada pilar captura esse evento.

**Log (pino):**

```javascript
// pino — registra intenção, resultado e contexto narrativo
logger.info(
  { requestId, email, action: 'user.create.start' },
  'Iniciando criação de usuário'
);

// ... operação ...

logger.info(
  { requestId, userId: usuario.id, action: 'user.create.success', durationMs },
  'Usuário criado com sucesso'
);
```

**Métrica (prom-client):**

```javascript
// prom-client — conta tentativas e mede duração por status
const userCreateTotal = new Counter({
  name: 'user_create_total',
  help: 'Total de criações de usuário por status',
  labelNames: ['status'],
});

const userCreateDuration = new Histogram({
  name: 'user_create_duration_seconds',
  help: 'Duração da criação de usuário',
  buckets: [0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1],
});

const endTimer = userCreateDuration.startTimer();
// ... operação ...
userCreateTotal.inc({ status: 'success' });
endTimer({ status: 'success' });
```

**Trace (OpenTelemetry):**

```javascript
// OpenTelemetry — span com atributos e status da operação
const tracer = trace.getTracer('user-service', '1.0.0');

return tracer.startActiveSpan('user.create', async (span) => {
  span.setAttributes({ 'user.email': email, 'request.id': requestId });

  try {
    const usuario = await db.usuarios.inserir({ email, nome });
    span.setAttributes({ 'user.id': usuario.id });
    span.setStatus({ code: SpanStatusCode.OK });
    return usuario;
  } catch (err) {
    span.recordException(err);
    span.setStatus({ code: SpanStatusCode.ERROR, message: err.message });
    throw err;
  } finally {
    span.end();
  }
});
```

**Tudo junto — endpoint completo (Fastify):**

```javascript
import Fastify from 'fastify';
import pino from 'pino';
import { Counter, Histogram, register } from 'prom-client';
import { trace, SpanStatusCode, context } from '@opentelemetry/api';

const app = Fastify({
  logger: pino({ level: 'info' }),
});

// --- Métricas ---
const userCreateTotal = new Counter({
  name: 'user_create_total',
  help: 'Total de criações de usuário por status',
  labelNames: ['status'],
});

const userCreateDuration = new Histogram({
  name: 'user_create_duration_seconds',
  help: 'Duração da criação de usuário',
  buckets: [0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5],
});

// --- Tracer ---
const tracer = trace.getTracer('user-service', '1.0.0');

// --- Rota ---
app.post('/users', async (request, reply) => {
  const { email, nome } = request.body;
  const requestId = request.id; // Fastify gera automaticamente
  const startTime = Date.now();

  // Log: início da operação
  request.log.info(
    { requestId, email, action: 'user.create.start' },
    'Iniciando criação de usuário'
  );

  // Trace: span pai da operação
  return tracer.startActiveSpan('user.create', async (span) => {
    span.setAttributes({
      'user.email': email,
      'request.id': requestId,
    });

    // Métrica: timer de duração
    const endTimer = userCreateDuration.startTimer();

    try {
      // Operação de banco (com span filho automático via auto-instrumentation)
      const usuario = await db.usuarios.inserir({ email, nome });

      const durationMs = Date.now() - startTime;

      // Log: sucesso com contexto completo
      request.log.info(
        {
          requestId,
          userId: usuario.id,
          email,
          action: 'user.create.success',
          durationMs,
        },
        'Usuário criado com sucesso'
      );

      // Métricas: contador de sucesso + duração
      userCreateTotal.inc({ status: 'success' });
      endTimer({ status: 'success' });

      // Trace: atributos do resultado + status OK
      span.setAttributes({ 'user.id': usuario.id, 'duration.ms': durationMs });
      span.setStatus({ code: SpanStatusCode.OK });

      return reply.status(201).send({ id: usuario.id, email });
    } catch (err) {
      const durationMs = Date.now() - startTime;

      // Log: erro com stack e contexto
      request.log.error(
        {
          requestId,
          email,
          action: 'user.create.error',
          durationMs,
          err: { message: err.message, code: err.code },
        },
        'Falha ao criar usuário'
      );

      // Métricas: contador de erro + duração
      userCreateTotal.inc({ status: 'error' });
      endTimer({ status: 'error' });

      // Trace: exceção registrada + status de erro
      span.recordException(err);
      span.setStatus({ code: SpanStatusCode.ERROR, message: err.message });

      throw err;
    } finally {
      span.end();
    }
  });
});

// --- Endpoint de métricas para o Prometheus ---
app.get('/metrics', async (request, reply) => {
  reply.header('Content-Type', register.contentType);
  return register.metrics();
});
```

O que este exemplo demonstra na prática:

- **Log de início**: captura intenção + contexto antes de qualquer I/O — essencial para correlacionar com logs do banco.
- **Log de resultado**: captura `userId` e `durationMs` — permite filtrar operações lentas ou anômalas.
- **Contador com label `status`**: permite calcular taxa de erro com uma query simples (`status="error" / total`).
- **Histogram de duração com label `status`**: permite comparar latência de sucessos vs erros (erros são mais rápidos? Mais lentos? Isso indica a causa).
- **Span com atributos**: o `requestId` no span permite correlacionar traces com logs no backend de observability (Jaeger, Tempo, etc).

## Armadilhas

### Armadilha 1: Logar apenas em caso de erro

A armadilha mais comum é instrumentar logs só no `catch`. Sem o log de início e de sucesso, é impossível saber se uma operação sequer começou, ou estimar a proporção de erros.

```javascript
// Ruim: só loga erros
async function criarUsuario(dados) {
  try {
    return await db.usuarios.inserir(dados);
  } catch (err) {
    logger.error({ err }, 'Erro ao criar usuário'); // única linha de log
    throw err;
  }
}

// Bom: loga início, sucesso e erro
async function criarUsuario(dados) {
  logger.info({ action: 'user.create.start', email: dados.email }, 'Iniciando');
  try {
    const u = await db.usuarios.inserir(dados);
    logger.info({ action: 'user.create.success', userId: u.id }, 'Criado');
    return u;
  } catch (err) {
    logger.error({ action: 'user.create.error', err }, 'Falha');
    throw err;
  }
}
```

### Armadilha 2: Usar alta cardinalidade como label de métrica

Labels de alta cardinalidade — como `userId`, `email` ou `requestId` — explodem o número de séries temporais no Prometheus e podem derrubar o servidor de métricas.

```javascript
// Perigoso: userId como label cria milhões de séries
const contador = new Counter({
  name: 'user_requests_total',
  labelNames: ['userId'], // NUNCA faça isso
});
contador.inc({ userId: req.user.id }); // nova série para cada usuário!

// Correto: labels com cardinalidade baixa e previsível
const contador = new Counter({
  name: 'user_requests_total',
  labelNames: ['status', 'route'], // cardinalidade: ~10 × ~20 = ~200 séries
});
contador.inc({ status: 'success', route: '/users' });
```

### Armadilha 3: Confundir SLO com SLA em discussões de time

SLO é interno e serve para guiar decisões de engenharia (when to stop deploys, prioritize reliability). SLA é externo e tem consequência contratual. Usar SLA como target de alerta interno significa que, quando o alerta dispara, você já violou o contrato com o cliente.

A prática correta é: alertar no SLO (antes de violar o SLA), tratar o SLA como linha de emergência que nunca deveria ser atingida.

### Armadilha 4: Traces sem sampling em produção de alto volume

Capturar 100% dos traces em alta volumetria é economicamente inviável e pode introduzir latência adicional pelo overhead de serialização e envio. Sem sampling, o custo de armazenamento cresce linearmente com o tráfego.

```javascript
// Sem sampling: coleta tudo (perigoso em alta volumetria)
const provider = new NodeTracerProvider({
  sampler: new AlwaysOnSampler(), // captura 100% dos traces
});

// Com tail-based sampling: decide se salva o trace DEPOIS de vê-lo completo
// Útil para garantir que erros e traces lentos sejam sempre salvos
const provider = new NodeTracerProvider({
  sampler: new ParentBasedSampler({
    root: new TraceIdRatioBasedSampler(0.1), // 10% de sampling
  }),
});
```

Para garantir que erros e traces lentos sejam sempre capturados mesmo com sampling baixo, use tail-based sampling no collector (OpenTelemetry Collector suporta isso nativamente).

### Armadilha 5: Não correlacionar logs com traces

Logs e traces produzidos pelo mesmo request mas sem um identificador comum são inúteis para diagnóstico conjunto. O `traceId` deve aparecer em ambos.

```javascript
// Sem correlação: logs e traces não se encontram
logger.info({ userId: 42 }, 'Usuário criado'); // sem traceId

// Com correlação: logs incluem o traceId do span ativo
import { trace } from '@opentelemetry/api';

function logComTrace(logger, level, dados, msg) {
  const span = trace.getActiveSpan();
  const traceContext = span
    ? { traceId: span.spanContext().traceId, spanId: span.spanContext().spanId }
    : {};
  logger[level]({ ...dados, ...traceContext }, msg);
}

logComTrace(logger, 'info', { userId: 42 }, 'Usuário criado');
// Saída: { userId: 42, traceId: "abc123...", spanId: "def456...", msg: "Usuário criado" }
```

## Em entrevista

**Explaining the three pillars:**

Logs, metrics, and traces are the three pillars of observability, and they answer fundamentally different questions: logs tell you *what* happened in a specific event, including all the contextual details like user IDs, request parameters, and error messages; metrics tell you *how often* and *how fast* things are happening as aggregated numbers over time, which makes them ideal for alerting and dashboards; and traces tell you *where* time was spent across a distributed request, allowing you to pinpoint which service or database call is responsible for latency.

**Explaining golden signals:**

The four golden signals — latency, traffic, errors, and saturation — are the minimum set of metrics that every production service should monitor. Latency measures how long requests take (focusing on p99, not averages, because averages hide tail latencies); traffic measures request rate so you can distinguish a sudden spike from normal growth; errors measure the proportion of requests that fail, which directly maps to user experience; and saturation measures how close the system is to its limits, such as CPU usage, heap memory, or database connection pool exhaustion.

**Explaining SLI, SLO, and SLA:**

An SLI is the specific metric you use to measure service quality — for example, "the proportion of requests served in under 200 milliseconds." An SLO is the target you set for that metric — "99.9% of requests must complete in under 200ms, measured over a 30-day rolling window." An SLA is the formal external contract with your customers, typically set below the SLO to give the engineering team a buffer — if the SLO is 99.9%, the SLA might commit to 99.5% so that when you're close to the SLO limit, you have time to react before triggering contractual consequences.

**Explaining trace correlation:**

In a distributed system, a single user request may touch five or more services. Without a trace ID that propagates through every service call, log entry, and database query, it is nearly impossible to reconstruct what happened during a specific request. By injecting the trace ID into every structured log line and ensuring that each service forwards the trace context in HTTP headers (using W3C TraceContext or B3 propagation), you can correlate logs, metrics, and traces from every service into a single coherent timeline for any given request.

## Vocabulário

| Português | Inglês | Nota |
|---|---|---|
| Observabilidade | Observability | Capacidade de inferir estado interno a partir de saídas externas |
| Pilares (três) | Three pillars | Logs, métricas e traces |
| Registros / Logs | Logs | Eventos discretos com contexto narrativo |
| Métricas | Metrics | Agregações numéricas medidas ao longo do tempo |
| Rastreamentos | Traces | Árvores de spans que mapeiam o fluxo de uma requisição |
| Sinais dourados | Golden signals | Latência, tráfego, erros e saturação |
| Indicador de nível de serviço | SLI — Service Level Indicator | O que você mede |
| Objetivo de nível de serviço | SLO — Service Level Objective | A meta que você quer atingir |
| Acordo de nível de serviço | SLA — Service Level Agreement | O contrato externo com consequência |
| Orçamento de erro | Error budget | Margem de falhas permitida pelo SLO |
| Amostragem | Sampling | Técnica de coletar apenas uma fração dos traces |
| Propagação de contexto | Context propagation | Transmissão do traceId entre serviços via headers |
| Span | Span | Unidade mínima de um trace (operação + duração) |

## Fontes

- [OpenTelemetry Documentation — Observability Primer](https://opentelemetry.io/docs/concepts/observability-primer/) — definição canônica dos três pilares e suas relações.
- [Google SRE Book — Chapter 6: Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/) — origem dos golden signals e das definições de SLI/SLO/SLA.
- [Charity Majors — "Observability — A Manifesto"](https://charity.wtf/2016/05/05/glitch-the-amazing-disappearing-feature/) — artigo fundacional sobre a diferença entre monitoring e observability.
- [pino documentation](https://getpino.io/) — logging estruturado de alta performance para Node.js.
- [prom-client documentation](https://github.com/siimon/prom-client) — cliente Prometheus oficial para Node.js.
- [OpenTelemetry JS SDK](https://github.com/open-telemetry/opentelemetry-js) — SDK JavaScript/Node.js para instrumentação de traces e métricas.

## Veja também

- [[03-Dominios/Node/Observability e produção/index]] — MOC do galho completo
- [[02 - Logging estruturado com pino]] — implementação detalhada de logs estruturados
- [[03 - Correlation IDs e context propagation]] — como correlacionar logs, métricas e traces
- [[04 - Métricas com prom-client]] — instrumentação completa de métricas Prometheus
- [[06 - Tracing distribuído com OpenTelemetry]] — traces distribuídos em profundidade
- [[12 - SLOs, dashboards, alertas e cheatsheet]] — implementação prática de SLOs
