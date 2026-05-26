# Galho 5 — Observability e produção: Plano de Execução

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Criar 12 notas atômicas + 1 MOC em `03-Dominios/Node/Observability e produção/` cobrindo os três pilares de observability (logs, métricas, traces), ferramentas idiomáticas do ecossistema Node (pino, prom-client, OpenTelemetry), diagnóstico avançado (clinic.js, heap snapshots) e patterns de resiliência (graceful shutdown, circuit breaker, connection pool tuning), e podar as seções correspondentes do tronco `Node.js.md`.

**Architecture:** Cada nota é um arquivo Markdown independente em `03-Dominios/Node/Observability e produção/`. O MOC serve como ponto de entrada com rotas alternativas. O tronco é podado ao final com callouts de migração.

**Tech Stack:** Obsidian Flavored Markdown, frontmatter YAML, wikilinks `[[]]`, callouts `[!abstract]`, dataview query no MOC. Ferramentas cobertas: pino 9, prom-client 15, OpenTelemetry JS 2, clinic.js, 0x, opossum 8+, asyncLocalStorage (Node 16+).

---

## REGRAS CRÍTICAS PARA O AGENTE EXECUTOR

> ⚠️ **ONE commit per note, NOT bundled.** Cada task = 1 nota = 1 commit dedicado. Commitar múltiplas notas em 1 commit é violação do workflow.
>
> ⚠️ **Nenhuma nota abaixo do mínimo de linhas declarado.** Abaixo do mínimo a nota perde profundidade para o nível senior exigido. O mínimo é piso, não teto.
>
> ⚠️ **"Em entrevista" obrigatoriamente 3+ sentenças em inglês interligadas.** Proibido one-liner.
>
> ⚠️ **Sem Co-Authored-By em commits.** Mensagens seguem o formato: `feat(node/g5): add <número> - <título>`.
>
> ⚠️ **Self-check antes de cada commit** — ver checklist na seção Self-Check abaixo.

## Self-Check (executar antes de cada commit de nota)

```
[ ] Frontmatter completo: title, created, updated, type, status, publish, tags, aliases
[ ] TL;DR callout [!abstract] presente com conteúdo denso (> 3 linhas)
[ ] Contagem de linhas >= mínimo declarado para esta nota
[ ] "Em entrevista" tem 3+ sentenças em inglês (não one-liner)
[ ] "Vocabulário PT→EN" tem >= 6 termos com tradução
[ ] Cada armadilha tem: (a) descrição + (b) código-problema + (c) fix
[ ] "Como funciona" tem >= 4 subsecções (headings ###)
[ ] Número de exemplos de código >= mínimo declarado para esta nota
[ ] Wikilinks para [[Node.js]] e galhos anteriores presentes
[ ] "Fontes" com pelo menos 1 link oficial da ferramenta principal
```

---

## Estrutura de arquivos

**Criar:**

```
03-Dominios/Node/Observability e produção/
├── Observability e produção.md          (MOC)
├── 01 - Os três pilares - logs, métricas e traces.md
├── 02 - Logging estruturado com pino.md
├── 03 - Correlation IDs e context propagation.md
├── 04 - Métricas com prom-client.md
├── 05 - Node-specific metrics - event loop lag, GC, heap.md
├── 06 - Tracing distribuído com OpenTelemetry.md
├── 07 - Profiling avançado com clinic.js.md
├── 08 - Detecção e diagnóstico de memory leaks.md
├── 09 - Graceful shutdown profundo.md
├── 10 - Circuit breaker e fallback com opossum.md
├── 11 - Connection pool tuning.md
└── 12 - SLOs, dashboards, alertas e cheatsheet.md
```

**Modificar:**

```
03-Dominios/JavaScript/Backend/Node.js.md     (poda: 4 seções → callouts)
03-Dominios/Node/index.md                     (adicionar galho 5)
```

---

## Task 1: MOC — Observability e produção

**Files:**
- Create: `03-Dominios/Node/Observability e produção/Observability e produção.md`

- [ ] **Step 1: Criar o arquivo MOC**

Criar `03-Dominios/Node/Observability e produção/Observability e produção.md` com o conteúdo abaixo:

```markdown
---
title: "Observability e produção"
created: 2026-05-08
updated: 2026-05-08
type: moc
status: seedling
publish: true
tags:
  - node
  - observability
  - producao
  - moc
aliases:
  - Observability Node
  - Galho 5 - Observability
---

# Observability e produção

> [!abstract] TL;DR
> Galho 5 da trilha Node Senior. Cobre os três pilares de observability (logs, métricas, traces) com ferramentas idiomáticas do ecossistema (pino, prom-client, OpenTelemetry), diagnóstico avançado de performance e memória (clinic.js, heap snapshots), e os patterns de resiliência que toda API precisa conhecer (graceful shutdown, circuit breaker, connection pool tuning). Pré-requisitos: galho 1 (Runtime e Event Loop) e galho 4 (Frameworks e arquitetura).

## Sobre este galho

Este galho cobre **observability e produção em Node.js**: os três pilares (logs, métricas, traces), golden signals, SLO/SLA, ferramentas idiomáticas do ecossistema (pino, prom-client, OpenTelemetry), diagnóstico avançado (clinic.js, heap snapshots) e patterns de resiliência (graceful shutdown, circuit breaker, connection pool tuning).

**Pré-requisitos:**
- [[Runtime e Event Loop]] (galho 1) — event loop phases, libuv thread pool, bloqueio — necessário para entender event loop lag e clinic.js
- [[Frameworks e arquitetura]] (galho 4) — middleware pipeline e hooks de shutdown nos frameworks

**Audiência primária:** dev senior em prep para entrevista internacional. Cada nota tem seção "Em entrevista" com frase pronta em inglês + vocabulário PT→EN.

**Audiência secundária:** o mesmo dev instrumentando ou debugando uma API em produção.

## Comece por aqui — trilha completa (12 notas)

### Bloco A — Visão geral

1. [[01 - Os três pilares - logs, métricas e traces]]

### Bloco B — Os três pilares

2. [[02 - Logging estruturado com pino]]
3. [[03 - Correlation IDs e context propagation]]
4. [[04 - Métricas com prom-client]]
5. [[05 - Node-specific metrics - event loop lag, GC, heap]]
6. [[06 - Tracing distribuído com OpenTelemetry]]

### Bloco C — Diagnóstico avançado

7. [[07 - Profiling avançado com clinic.js]]
8. [[08 - Detecção e diagnóstico de memory leaks]]

### Bloco D — Resiliência

9. [[09 - Graceful shutdown profundo]]
10. [[10 - Circuit breaker e fallback com opossum]]
11. [[11 - Connection pool tuning]]

### Bloco E — Fechamento

12. [[12 - SLOs, dashboards, alertas e cheatsheet]]

## Rotas alternativas

### Rota entrevista internacional

01 → 02 → 04 → 06 → 09 → 10 → 12. Foco em explicar os três pilares e patterns de resiliência para entrevistador.

### Rota produção e debugging

01 → 07 → 08 → 09 → 11 → 12. Para quem está debugando um problema em produção agora.

### Rota Node-specific metrics

04 → 05 → 07 → 12. Para instrumentar métricas específicas do runtime Node (event loop lag, GC, heap).

### Rota resiliência/SRE

09 → 10 → 11 → 12. Para quem está configurando resiliência numa API existente.

### Rota OpenTelemetry completa

01 → 03 → 06 → 12. Para quem quer entender distributed tracing do zero.

## Todas as notas

```dataview
TABLE status, updated
FROM "03-Dominios/Node/Observability e produção"
WHERE type = "concept"
SORT file.name ASC
```

## Veja também

- [[03-Dominios/Node/index|Node.js (MOC central)]]
- [[Node.js]] — tronco
- [[03-Dominios/Node/Runtime e Event Loop/index]] — galho 1
- [[03-Dominios/Node/Paralelismo/index]] — galho 2
- [[03-Dominios/Node/Streams/index]] — galho 3
- [[03-Dominios/Node/Frameworks e arquitetura/index]] — galho 4
```

- [ ] **Step 2: Verificar se a pasta foi criada corretamente**

```bash
ls "03-Dominios/Node/Observability e produção/"
```

Expected: `Observability e produção.md`

- [ ] **Step 3: Commit**

```bash
git add "03-Dominios/Node/Observability e produção/Observability e produção.md"
git commit -m "feat(node/g5): add MOC - Observability e produção"
```

---

## Task 2: Nota 01 — Os três pilares

**Files:**
- Create: `03-Dominios/Node/Observability e produção/01 - Os três pilares - logs, métricas e traces.md`

**Mínimo:** 380 linhas. **Código mínimo:** 5 exemplos.

- [ ] **Step 1: Criar a nota 01**

Criar `03-Dominios/Node/Observability e produção/01 - Os três pilares - logs, métricas e traces.md` com o seguinte conteúdo **completo**. A nota deve cobrir obrigatoriamente:

**Frontmatter:**
```yaml
---
title: "Os três pilares da observability: logs, métricas e traces"
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
```

**Seções obrigatórias com conteúdo mínimo:**

1. **TL;DR** (`[!abstract]`): descrever em 4+ linhas o que são os 3 pilares, golden signals e SLO/SLA.

2. **O que é**: definir log (registro imutável de evento), metric (agregação numérica no tempo), trace (caminho de uma request através de serviços). Incluir tabela comparativa com: tipo / quando usar / exemplo concreto / ferramenta Node.

3. **Por que importa**: os três são necessários juntos — métrica sinaliza problema, log detalha, trace localiza. Sem os três, metade do diagnóstico está cega.

4. **Como funciona** (mínimo 4 subsecções `###`):
   - **Os três pilares em detalhe**: log vs metric vs trace com critério de decisão ("quando o problema é de log, de metric ou de trace")
   - **Golden signals** (latência, tráfego, erros, saturação): definição e exemplo de query PromQL para cada um. Exemplo:
     ```promql
     # Error rate
     rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m])
     
     # P95 latência
     histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
     
     # Saturação (event loop lag)
     node_eventloop_lag_seconds > 0.05
     ```
   - **SLI, SLO, SLA**: definições, relações e exemplos concretos. SLI = métrica real; SLO = meta percentual; SLA = contrato com cliente. Exemplo: "SLI: P95 latência medida; SLO: P95 < 200ms em 99.9% das requests nos últimos 30 dias; SLA: compensação financeira se SLO for violado."
   - **O triângulo de diagnóstico**: fluxo: metric spike → log search → trace view. Exemplo narrativo de um bug real diagnosticado com os três.

5. **Na prática**: snippet de log estruturado (pino), snippet de counter (prom-client), snippet de span (OTEL) — três exemplos lado a lado para o mesmo "criar usuário":
   ```typescript
   // Log: o que aconteceu
   logger.info({ userId, duration }, 'user created');
   
   // Metric: quantas vezes e quanto tempo
   userCreateCounter.inc({ status: 'success' });
   userCreateHistogram.observe(duration);
   
   // Trace: onde no caminho
   const span = tracer.startSpan('user.create');
   span.setAttribute('user.id', userId);
   span.end();
   ```

6. **Armadilhas** (mínimo 4, cada uma com código-problema + fix):
   - Usar só logs: escalar logging para substituir métricas (código: log de cada request → storage explode; fix: counter)
   - Métricas sem cardinality control: label com userId → cardinalidade explosiva
   - Trace sem sampling: todo request trackeado → storage e CPU explode
   - Confundir SLI com SLO: SLI é a query, SLO é a meta — definir um sem o outro é inútil

7. **Em entrevista** (3+ sentenças interligadas em inglês cobrindo o que são, trade-off e caveat):
   ```
   "Observability has three pillars: logs, metrics, and traces. Logs are immutable records of specific events — they answer 'what happened.' Metrics are numerical aggregations over time — they answer 'how much' and 'how often,' making them ideal for alerting. Distributed traces capture the path of a single request through multiple services — they answer 'where in the system did this take too long.' In practice, you need all three: a metric spike tells you something is wrong, logs narrow down the error type, and traces pinpoint which service or database call is the bottleneck."
   ```

8. **Vocabulário PT→EN** (mínimo 8 termos):
   - log de evento → event log
   - métrica → metric
   - rastreamento → trace / distributed trace
   - trecho de execução → span
   - sinal dourado → golden signal
   - indicador de nível de serviço → SLI (Service Level Indicator)
   - objetivo de nível de serviço → SLO (Service Level Objective)
   - acordo de nível de serviço → SLA (Service Level Agreement)
   - saturação → saturation
   - taxa de erro → error rate

9. **Fontes**: links para OpenTelemetry docs, Google SRE Book (SLI/SLO chapter).

10. **Veja também**: links para notas 02, 04, 06, 12 do galho + [[Node.js]].

- [ ] **Step 2: Self-check**

Rodar o self-check da seção de regras críticas. Verificar contagem de linhas >= 380.

- [ ] **Step 3: Commit**

```bash
git add "03-Dominios/Node/Observability e produção/01 - Os três pilares - logs, métricas e traces.md"
git commit -m "feat(node/g5): add 01 - Os três pilares - logs, métricas e traces"
```

---

## Task 3: Nota 02 — Logging estruturado com pino

**Files:**
- Create: `03-Dominios/Node/Observability e produção/02 - Logging estruturado com pino.md`

**Mínimo:** 350 linhas. **Código mínimo:** 6 exemplos.

- [ ] **Step 1: Criar a nota 02**

**Frontmatter:**
```yaml
---
title: "Logging estruturado com pino"
created: 2026-05-08
updated: 2026-05-08
type: concept
status: seedling
publish: true
tags:
  - node
  - observability
  - logging
  - pino
aliases:
  - pino logger
  - structured logging
---
```

**Seções obrigatórias com conteúdo mínimo:**

1. **TL;DR**: pino é o logger estruturado padrão do ecossistema Node. Async JSON serialization, menor overhead no hot path. Serializers para reduzir objetos grandes. Redaction para dados sensíveis. Child loggers para contexto por request.

2. **O que é**: pino vs `console.log` — structured JSON vs texto livre. Por que logging estruturado importa (searchable, parseable, compatível com Loki/Datadog/CloudWatch). Por que pino especificamente: benchmark (2-3x mais rápido que winston), thread worker para serialização.

3. **Por que importa**: console.log em produção é pesquisável por grep; logging estruturado é pesquisável por campo. `grep 'userId: 123'` vs `jq 'select(.userId == 123)'`.

4. **Como funciona** (mínimo 4 subsecções `###`):

   - **Configuração básica**:
     ```typescript
     import pino from 'pino';
     
     const logger = pino({
       level: process.env.LOG_LEVEL ?? 'info',
       transport: process.env.NODE_ENV !== 'production'
         ? { target: 'pino-pretty', options: { colorize: true } }
         : undefined,
     });
     
     logger.info({ userId: '123', action: 'login' }, 'user logged in');
     logger.error({ err, requestId }, 'payment failed');
     ```

   - **Serializers** — customizar como objetos são serializados (reduzir request a campos essenciais):
     ```typescript
     const logger = pino({
       serializers: {
         req: (req) => ({
           method: req.method,
           url: req.url,
           id: req.id,
         }),
         err: pino.stdSerializers.err,
       },
     });
     ```

   - **Redaction** — remover campos sensíveis antes de logar:
     ```typescript
     const logger = pino({
       redact: {
         paths: [
           'req.headers.authorization',
           'body.password',
           'body.creditCard',
           '*.token',
         ],
         censor: '[REDACTED]',
       },
     });
     ```

   - **Child loggers** — adicionar contexto por request (requestId, userId, traceId):
     ```typescript
     // Middleware Express
     app.use((req, _res, next) => {
       req.log = logger.child({ requestId: req.id, method: req.method, url: req.url });
       next();
     });
     
     // No handler
     req.log.info({ duration }, 'request completed');
     ```

   - **Integração com Express (pino-http)** e **NestJS (nestjs-pino)**:
     ```typescript
     // Express
     import pinoHttp from 'pino-http';
     app.use(pinoHttp({ logger }));
     
     // NestJS — app.module.ts
     import { LoggerModule } from 'nestjs-pino';
     @Module({
       imports: [LoggerModule.forRoot({ pinoHttp: { level: 'info' } })],
     })
     ```

   - **Log levels por ambiente**: TRACE para dev intenso, DEBUG para dev, INFO para produção, WARN para degradação, ERROR para falha recuperável, FATAL para falha não-recuperável.

5. **Na prática**: setup completo recomendado — config com level via env + redact de auth/password + pretty dev/json prod + serializer de req.

6. **Armadilhas** (mínimo 4 com código-problema + fix):
   - Logar objetos completos (req inteiro → MB de logs): serializer resolve
   - `console.log` em handlers: bypass do logger, sem estrutura; fix: substituir por `logger.info`
   - Log level TRACE em produção: volume de dados + custo; fix: `LOG_LEVEL=info` por default em prod
   - Strings em vez de objetos: `logger.info('user ' + id + ' created')` perde estrutura; fix: `logger.info({ userId }, 'user created')`

7. **Em entrevista** (3+ sentenças):
   ```
   "For production Node.js apps, I use pino as the structured logger because it has the lowest overhead among the popular options — it serializes to JSON asynchronously using a worker thread, so the hot path is unaffected. I configure serializers to reduce large objects like the request to just method, URL, and request ID, and use redaction to remove sensitive fields like authorization headers and passwords before they ever reach the log sink. Child loggers per request let me propagate context like request ID and trace ID to every log line without passing them as explicit parameters."
   ```

8. **Vocabulário PT→EN** (mínimo 6):
   - log estruturado → structured log
   - serializador → serializer
   - redação de campos → field redaction
   - logger filho → child logger
   - nível de log → log level
   - transporte → transport (pino-pretty, pino/file)

9. **Fontes**: [pino docs](https://getpino.io/), [nestjs-pino](https://github.com/iamolegga/nestjs-pino).

10. **Veja também**: notas 03, 04, 12 do galho + [[Node.js]].

- [ ] **Step 2: Self-check**

Verificar contagem de linhas >= 350. Verificar 6+ exemplos de código.

- [ ] **Step 3: Commit**

```bash
git add "03-Dominios/Node/Observability e produção/02 - Logging estruturado com pino.md"
git commit -m "feat(node/g5): add 02 - Logging estruturado com pino"
```

---

## Task 4: Nota 03 — Correlation IDs e context propagation

**Files:**
- Create: `03-Dominios/Node/Observability e produção/03 - Correlation IDs e context propagation.md`

**Mínimo:** 380 linhas. **Código mínimo:** 5 exemplos.

- [ ] **Step 1: Criar a nota 03**

**Frontmatter:**
```yaml
---
title: "Correlation IDs e context propagation"
created: 2026-05-08
updated: 2026-05-08
type: concept
status: seedling
publish: true
tags:
  - node
  - observability
  - correlation-id
  - asynclocalstorage
  - context-propagation
aliases:
  - AsyncLocalStorage
  - requestId propagation
  - W3C Trace Context
---
```

**Seções obrigatórias com conteúdo mínimo:**

1. **TL;DR**: AsyncLocalStorage permite propagar contexto (requestId, traceId, userId) por toda a call stack sem passar por parâmetro. Middleware gera o ID → ALS armazena → child logger lê → downstream recebe via header `traceparent`.

2. **O que é**: sem correlation ID, logs de uma request são ilhas em múltiplos serviços. Com ID propagado, correlacionamos todos os eventos de um request com um único campo de busca.

3. **Por que importa**: em sistemas distribuídos, uma request chama 3-5 serviços. Sem correlation ID, o log do serviço B não tem nenhuma ligação com o log do serviço A para o mesmo request. Debug vira adivinhação.

4. **Como funciona** (mínimo 4 subsecções `###`):

   - **AsyncLocalStorage — API e ciclo de vida**:
     ```typescript
     import { AsyncLocalStorage } from 'node:async_hooks';
     
     interface RequestContext {
       requestId: string;
       traceId?: string;
       userId?: string;
     }
     
     export const asyncContext = new AsyncLocalStorage<RequestContext>();
     
     // Uso em qualquer ponto do call stack
     const ctx = asyncContext.getStore();
     logger.info({ requestId: ctx?.requestId }, 'processing');
     ```

   - **Middleware gerando e propagando requestId** (Express + uuid):
     ```typescript
     import { randomUUID } from 'node:crypto';
     
     app.use((req, res, next) => {
       const requestId = (req.headers['x-request-id'] as string) ?? randomUUID();
       res.setHeader('x-request-id', requestId);
       
       asyncContext.run({ requestId }, () => {
         req.log = logger.child({ requestId });
         next();
       });
     });
     ```

   - **Integrando com pino child logger via ALS**:
     ```typescript
     // Helper global — qualquer módulo pode chamar
     export function getLogger() {
       const ctx = asyncContext.getStore();
       return ctx ? logger.child(ctx) : logger;
     }
     
     // No service layer — sem precisar passar logger como parâmetro
     export class UserService {
       async createUser(data: CreateUserInput) {
         getLogger().info({ email: data.email }, 'creating user');
         // ...
       }
     }
     ```

   - **Propagando para downstream via W3C Trace Context**:
     ```typescript
     // Outgoing HTTP call — propaga o contexto
     async function callOrderService(orderId: string) {
       const ctx = asyncContext.getStore();
       return fetch(`${ORDER_SERVICE_URL}/orders/${orderId}`, {
         headers: {
           'x-request-id': ctx?.requestId ?? '',
           'traceparent': ctx?.traceId ?? '',
         },
       });
     }
     ```

   - **Limitação: ALS não atravessa Worker Threads** — cada Worker tem seu próprio contexto ALS. Para propagar, passar o contexto explicitamente via `workerData`.

5. **Na prática**: exemplo end-to-end completo — middleware Express → ALS → service → downstream call — todos com mesmo requestId no log.

6. **Armadilhas** (mínimo 4 com código-problema + fix):
   - ALS perdida após `setTimeout` sem `run()` aninhado: a store fica undefined
     ```typescript
     // RUIM
     asyncContext.run({ requestId }, () => {
       setTimeout(() => {
         asyncContext.getStore(); // ainda disponível — setTimeout herda o contexto
       }, 100);
     });
     // Na verdade setTimeout herda — o problema real é ao passar callback para lib que não herda
     
     // PROBLEMA REAL: callback passado para worker externo
     const worker = new Worker('./worker.js');
     worker.postMessage({ requestId: asyncContext.getStore()?.requestId }); // deve ser explícito
     ```
   - ALS em Worker Threads — não atravessa boundary
   - Usar `run()` em múltiplos escopos concorrentes — cada `run()` cria contexto isolado (isso é feature, mas confunde)
   - Múltiplos `AsyncLocalStorage` para diferentes contextos — manter 1 store com objeto rico é mais simples que múltiplos stores

7. **Em entrevista** (3+ sentenças):
   ```
   "I use AsyncLocalStorage to propagate request context — request ID, trace ID, user ID — throughout the entire call stack without passing it as a function parameter. The middleware creates the context with `als.run()`, and any service or utility in the call chain can call `als.getStore()` to read it and add it to their log lines. For cross-service propagation, I follow W3C Trace Context and pass the trace ID in the `traceparent` header — this way, querying by trace ID in Grafana Loki or Datadog gives you logs from all services involved in a single request."
   ```

8. **Vocabulário PT→EN** (mínimo 6):
   - ID de correlação → correlation ID / request ID
   - propagação de contexto → context propagation
   - armazenamento local assíncrono → AsyncLocalStorage
   - cabeçalho de rastreamento → trace header (`traceparent`)
   - escopo de execução → execution scope
   - contexto de requisição → request context

9. **Fontes**: [AsyncLocalStorage MDN/Node docs](https://nodejs.org/api/async_context.html), [W3C Trace Context](https://www.w3.org/TR/trace-context/).

10. **Veja também**: nota 02 (pino), nota 06 (OTEL), [[03-Dominios/Node/Runtime e Event Loop/index]] (Worker Threads e contexto).

- [ ] **Step 2: Self-check**

Verificar contagem de linhas >= 380.

- [ ] **Step 3: Commit**

```bash
git add "03-Dominios/Node/Observability e produção/03 - Correlation IDs e context propagation.md"
git commit -m "feat(node/g5): add 03 - Correlation IDs e context propagation"
```

---

## Task 5: Nota 04 — Métricas com prom-client

**Files:**
- Create: `03-Dominios/Node/Observability e produção/04 - Métricas com prom-client.md`

**Mínimo:** 400 linhas. **Código mínimo:** 6 exemplos.

- [ ] **Step 1: Criar a nota 04**

**Frontmatter:**
```yaml
---
title: "Métricas com prom-client"
created: 2026-05-08
updated: 2026-05-08
type: concept
status: seedling
publish: true
tags:
  - node
  - observability
  - metricas
  - prometheus
  - prom-client
aliases:
  - prom-client
  - Prometheus Node
  - metrics endpoint
---
```

**Seções obrigatórias com conteúdo mínimo:**

1. **TL;DR**: prom-client é a biblioteca padrão para expor métricas Prometheus em Node. 4 tipos: Counter (só sobe), Gauge (sobe e desce), Histogram (distribuição), Summary (quantis). Endpoint `/metrics` expõe em formato scrape. Labels adicionam dimensões — cuidado com cardinalidade alta.

2. **O que é**: Prometheus é um sistema de monitoramento pull-based. Node expõe `/metrics`; Prometheus faz scrape periodicamente. prom-client cria e registra métricas num Registry global.

3. **Por que importa**: métricas habilitam alertas em tempo real, dashboards e SLOs. Logs são post-mortem; métricas são real-time. `rate(errors[5m]) > 0.01` pode disparar alerta em 5 minutos; busca em logs pode levar horas.

4. **Como funciona** (mínimo 4 subsecções `###`):

   - **Os 4 tipos com exemplos**:
     ```typescript
     import { Counter, Gauge, Histogram, Summary } from 'prom-client';
     
     // Counter — só sobe; use para events (requests, errors, jobs processed)
     const requestsTotal = new Counter({
       name: 'http_requests_total',
       help: 'Total HTTP requests',
       labelNames: ['method', 'route', 'status_code'],
     });
     
     // Gauge — sobe e desce; use para estado atual (jobs ativos, conexões abertas, queue size)
     const activeJobs = new Gauge({
       name: 'active_jobs',
       help: 'Currently active background jobs',
     });
     
     // Histogram — distribuição; use para latência, tamanho de payload
     const requestDuration = new Histogram({
       name: 'http_request_duration_seconds',
       help: 'HTTP request duration in seconds',
       labelNames: ['method', 'route'],
       buckets: [0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5],
     });
     
     // Summary — quantis calculados no cliente; use com cautela (não agregável cross-instance)
     const payloadSize = new Summary({
       name: 'request_payload_bytes',
       help: 'Request payload size',
       percentiles: [0.5, 0.9, 0.99],
     });
     ```

   - **Configuração do Registry e endpoint `/metrics`**:
     ```typescript
     import { register, collectDefaultMetrics } from 'prom-client';
     
     // Coleta métricas padrão do Node (CPU, heap, event loop, GC)
     collectDefaultMetrics();
     
     // Express
     app.get('/metrics', async (_req, res) => {
       res.set('Content-Type', register.contentType);
       res.end(await register.metrics());
     });
     ```

   - **Middleware de timing automático** (integração com Express):
     ```typescript
     app.use((req, res, next) => {
       const end = requestDuration.startTimer({ method: req.method, route: req.route?.path ?? 'unknown' });
       res.on('finish', () => {
         requestsTotal.inc({ method: req.method, route: req.route?.path ?? 'unknown', status_code: res.statusCode });
         end();
       });
       next();
     });
     ```

   - **Labels e cardinalidade**: adicionar label `userId` ou `orderId` → cardinalidade explosiva (1 série por usuário). Labels devem ter baixa cardinalidade (method, status_code, route, environment). Regra prática: < 100 valores distintos por label.

   - **Histogram buckets**: buckets defaults são ruins para latência web. Definir buckets baseados no SLO: se SLO é P95 < 200ms, ter buckets em 100ms, 200ms, 500ms.

   - **Push vs pull**: Prometheus é pull (scrape). Para jobs de curta duração (cron), usar pushgateway.

5. **Na prática**: setup completo — Registry + collectDefaultMetrics + Counter + Histogram + middleware timing + endpoint `/metrics`.

6. **Armadilhas** (mínimo 4):
   - Cardinalidade alta: label com userId → Prometheus com milhões de series → OOM
   - Buckets default inadequados: `[0.005, 0.01, ..., 10]` vs SLO de 200ms
   - Summary vs Histogram: Summary não é agregável cross-instance (não dá para federar de múltiplos pods)
   - Counter reset: após restart, Counter volta a 0 — usar `rate()` não `delta()` para detectar

7. **Em entrevista** (3+ sentenças):
   ```
   "I use prom-client to expose Prometheus metrics from Node.js apps. The four types serve different purposes: Counter for monotonically increasing values like request count and error count, Gauge for current state like active connections or queue depth, and Histogram for latency distributions which let you calculate P95 and P99 at query time. One critical decision is cardinality — labels like method and status code are fine, but user ID or order ID as a label would create millions of time series and crash Prometheus. I always define custom histogram buckets aligned with the SLO target rather than using the defaults."
   ```

8. **Vocabulário PT→EN** (mínimo 8):
   - métrica → metric
   - contador → counter
   - medidor → gauge
   - histograma → histogram
   - sumário → summary
   - cardinalidade → cardinality (número de séries distintas)
   - raspagem → scrape (Prometheus coleta métricas por scrape)
   - rótulo → label
   - série temporal → time series
   - quantil → quantile / percentile

9. **Fontes**: [prom-client GitHub](https://github.com/siimon/prom-client), [Prometheus docs](https://prometheus.io/docs/).

10. **Veja também**: notas 01, 05, 12 do galho + [[Node.js]].

- [ ] **Step 2: Self-check**

Verificar contagem de linhas >= 400. Verificar 6+ exemplos.

- [ ] **Step 3: Commit**

```bash
git add "03-Dominios/Node/Observability e produção/04 - Métricas com prom-client.md"
git commit -m "feat(node/g5): add 04 - Métricas com prom-client"
```

---

## Task 6: Nota 05 — Node-specific metrics

**Files:**
- Create: `03-Dominios/Node/Observability e produção/05 - Node-specific metrics - event loop lag, GC, heap.md`

**Mínimo:** 380 linhas. **Código mínimo:** 5 exemplos.

- [ ] **Step 1: Criar a nota 05**

**Frontmatter:**
```yaml
---
title: "Node-specific metrics: event loop lag, GC, heap"
created: 2026-05-08
updated: 2026-05-08
type: concept
status: seedling
publish: true
tags:
  - node
  - observability
  - metricas
  - event-loop
  - gc
  - heap
  - performance
aliases:
  - event loop lag
  - GC metrics
  - heap metrics Node
---
```

**Seções obrigatórias com conteúdo mínimo:**

1. **TL;DR**: métricas genéricas (CPU, RAM) não diagnosticam problemas específicos de Node. Event loop lag > 10ms indica bloqueio. GC pause longa causa jank em real-time. Heap growing steadily indica leak. Active handles crescendo indica leak de recursos.

2. **O que é**: métricas Node-specific que complementam as métricas padrão do prom-client — elas expõem o estado interno do runtime Node que `collectDefaultMetrics()` não cobre com granularidade suficiente.

3. **Por que importa**: event loop lag de 50ms pode não aparecer em CPU (Node está "idle" entre ticks) mas está degradando latência de todas as requests. Só um event loop lag gauge específico detecta.

4. **Como funciona** (mínimo 4 subsecções `###`):

   - **Event loop lag gauge** — `perf_hooks.monitorEventLoopDelay()`:
     ```typescript
     import { monitorEventLoopDelay } from 'node:perf_hooks';
     import { Gauge } from 'prom-client';
     
     const eventLoopLag = new Gauge({
       name: 'nodejs_eventloop_lag_seconds',
       help: 'Event loop lag in seconds (p99)',
     });
     
     const histogram = monitorEventLoopDelay({ resolution: 10 }); // ms
     histogram.enable();
     
     setInterval(() => {
       eventLoopLag.set(histogram.percentile(99) / 1e9); // ns → s
     }, 5000);
     ```

   - **GC metrics** — `PerformanceObserver` para entries de tipo `gc`:
     ```typescript
     import { PerformanceObserver, constants } from 'node:perf_hooks';
     import { Histogram } from 'prom-client';
     
     const gcDuration = new Histogram({
       name: 'nodejs_gc_duration_seconds',
       help: 'GC pause duration',
       labelNames: ['kind'],
       buckets: [0.001, 0.005, 0.01, 0.05, 0.1, 0.5],
     });
     
     const obs = new PerformanceObserver((list) => {
       for (const entry of list.getEntries()) {
         const kind = entry.detail?.kind === constants.NODE_PERFORMANCE_GC_MAJOR ? 'major' : 'minor';
         gcDuration.observe({ kind }, entry.duration / 1000); // ms → s
       }
     });
     obs.observe({ type: 'gc' });
     ```

   - **Heap stats** — `process.memoryUsage()`:
     ```typescript
     import { Gauge } from 'prom-client';
     
     const heapUsed = new Gauge({ name: 'nodejs_heap_used_bytes', help: 'Heap used bytes' });
     const heapTotal = new Gauge({ name: 'nodejs_heap_total_bytes', help: 'Heap total bytes' });
     const rss = new Gauge({ name: 'nodejs_rss_bytes', help: 'Resident set size' });
     const external = new Gauge({ name: 'nodejs_external_bytes', help: 'C++ objects bound to JS' });
     
     setInterval(() => {
       const mem = process.memoryUsage();
       heapUsed.set(mem.heapUsed);
       heapTotal.set(mem.heapTotal);
       rss.set(mem.rss);
       external.set(mem.external);
     }, 5000);
     ```

   - **Active handles e requests** (diagnóstico de resource leaks):
     ```typescript
     const activeHandles = new Gauge({
       name: 'nodejs_active_handles',
       help: 'Active libuv handles (sockets, timers, etc.)',
     });
     
     setInterval(() => {
       activeHandles.set((process as any)._getActiveHandles().length);
     }, 5000);
     ```

   - **O que cada campo de `process.memoryUsage()` significa**:
     - `heapUsed`: memória JS realmente usada
     - `heapTotal`: memória JS alocada (pode crescer sem leak)
     - `rss`: total na RAM (heap + stack + C++ objects)
     - `external`: objetos C++ (Buffers, `ArrayBuffer`)
     - `arrayBuffers`: Buffers alocados fora do heap JS

5. **Na prática**: wrapper completo que registra todos os gauges acima num `setInterval` de 5s, pronto para copiar e adaptar.

6. **Armadilhas** (mínimo 4 com código + fix):
   - Monitorar event loop lag sem baseline: 5ms em dev é ok; em prod com tráfego real, 5ms pode já ser preocupante. Definir threshold baseado em P99 com zero carga primeiro.
   - Confundir `heapTotal` com "memória usada": heap pode ter 1GB alocado com só 300MB em uso — olhar `heapUsed`
   - GC minor vs major: minor é rápido (< 1ms), major pode pausar por 10-100ms. Alertar só em major.
   - `_getActiveHandles()` é API privada: funciona mas pode quebrar — usar apenas em diagnostics, não em produção crítica

7. **Em entrevista** (3+ sentenças):
   ```
   "Standard infrastructure metrics like CPU and memory don't tell you much about Node-specific bottlenecks. I instrument two additional signals: event loop lag using `monitorEventLoopDelay()` from perf_hooks, and GC pause duration using PerformanceObserver on GC entries. Event loop lag above 50 milliseconds tells me the event loop is being blocked — usually by a synchronous operation or a tight computation loop — even though CPU might look normal. Major GC pauses above 100ms cause observable latency spikes in real-time APIs, and I alert separately on those versus minor GCs which are typically sub-millisecond."
   ```

8. **Vocabulário PT→EN** (mínimo 6):
   - atraso do event loop → event loop lag
   - pausa de GC → GC pause
   - heap usado → heap used
   - conjunto residente → resident set size (RSS)
   - coleta de lixo → garbage collection (GC)
   - observador de performance → PerformanceObserver

9. **Fontes**: [Node.js perf_hooks](https://nodejs.org/api/perf_hooks.html), [Node.js diagnostics guide](https://nodejs.org/en/docs/guides/diagnostics).

10. **Veja também**: notas 04, 07, 08 do galho + [[03-Dominios/Node/Runtime e Event Loop/index]] (galho 1).

- [ ] **Step 2: Self-check**

Verificar contagem de linhas >= 380.

- [ ] **Step 3: Commit**

```bash
git add "03-Dominios/Node/Observability e produção/05 - Node-specific metrics - event loop lag, GC, heap.md"
git commit -m "feat(node/g5): add 05 - Node-specific metrics - event loop lag, GC, heap"
```

---

## Task 7: Nota 06 — Tracing distribuído com OpenTelemetry

**Files:**
- Create: `03-Dominios/Node/Observability e produção/06 - Tracing distribuído com OpenTelemetry.md`

**Mínimo:** 420 linhas. **Código mínimo:** 6 exemplos.

- [ ] **Step 1: Criar a nota 06**

**Frontmatter:**
```yaml
---
title: "Tracing distribuído com OpenTelemetry"
created: 2026-05-08
updated: 2026-05-08
type: concept
status: seedling
publish: true
tags:
  - node
  - observability
  - tracing
  - opentelemetry
  - distributed-tracing
aliases:
  - OpenTelemetry Node
  - OTEL tracing
  - distributed tracing
---
```

**Seções obrigatórias com conteúdo mínimo:**

1. **TL;DR**: OpenTelemetry é o padrão aberto para instrumentação. Um trace é composto de spans. Auto-instrumentation instrumenta HTTP/Express/pino automaticamente. Manual instrumentation cria spans para operações importantes. Propagação via `traceparent` header.

2. **O que é**: em sistemas com múltiplos serviços, um request chama vários endpoints. Trace mostra o caminho completo com timing de cada hop. Span = unidade de trabalho rastreada (ex: "query ao banco", "chamada ao serviço de pagamento").

3. **Por que importa**: log mostra que falhou; metric mostra que o error rate subiu; trace mostra que o serviço de pagamento levou 4 segundos na step 3 do request. Sem trace, o bottleneck num sistema distribuído é invisível.

4. **Como funciona** (mínimo 5 subsecções `###`):

   - **Setup do SDK — tracing.ts (inicializar antes de qualquer import)**:
     ```typescript
     // tracing.ts — DEVE ser o primeiro arquivo importado
     import { NodeSDK } from '@opentelemetry/sdk-node';
     import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http';
     import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';
     import { W3CTraceContextPropagator } from '@opentelemetry/core';
     import { Resource } from '@opentelemetry/resources';
     import { SEMRESATTRS_SERVICE_NAME } from '@opentelemetry/semantic-conventions';
     
     const sdk = new NodeSDK({
       resource: new Resource({
         [SEMRESATTRS_SERVICE_NAME]: process.env.SERVICE_NAME ?? 'api',
       }),
       traceExporter: new OTLPTraceExporter({
         url: process.env.OTLP_ENDPOINT ?? 'http://localhost:4318/v1/traces',
       }),
       instrumentations: [getNodeAutoInstrumentations()],
       textMapPropagator: new W3CTraceContextPropagator(),
     });
     
     sdk.start();
     process.on('SIGTERM', () => sdk.shutdown());
     ```

   - **Entry point — inicializar antes dos imports do app**:
     ```typescript
     // server.ts
     import './tracing'; // PRIMEIRO — antes de qualquer import de framework
     import express from 'express';
     // ...
     ```

   - **Auto-instrumentation** — o que `getNodeAutoInstrumentations()` cobre automaticamente:
     - HTTP (`http`, `https`): todo request recebe span
     - Express: cada rota recebe span
     - `pg`, `mysql2`, `mongoose`: queries recebem span com texto SQL
     - `pino`: logs são correlacionados com o trace ativo

   - **Manual instrumentation — criar spans para operações importantes**:
     ```typescript
     import { trace, SpanStatusCode } from '@opentelemetry/api';
     
     const tracer = trace.getTracer('user-service');
     
     export async function createUser(data: CreateUserInput) {
       return tracer.startActiveSpan('user.create', async (span) => {
         try {
           span.setAttribute('user.email', data.email);
           span.setAttribute('user.role', data.role);
           
           const user = await db.insert(users).values(data).returning();
           
           span.setAttribute('user.id', user[0].id);
           span.setStatus({ code: SpanStatusCode.OK });
           return user[0];
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

   - **Sampling — tail-based vs head-based**:
     ```typescript
     import { ParentBasedSampler, TraceIdRatioBased } from '@opentelemetry/sdk-trace-base';
     
     // Sample 10% das requests, mas sempre sample se o parent pediu
     const sampler = new ParentBasedSampler({
       root: new TraceIdRatioBased(0.1),
     });
     
     const sdk = new NodeSDK({ sampler, /* ... */ });
     ```

   - **OTEL Metrics vs prom-client** (framing sem dogma):
     - Use **prom-client** quando: já tem Prometheus, equipe conhece PromQL, sem plano de OTEL unificado
     - Use **OTEL Metrics** quando: quer usar um único SDK para traces + metrics + logs, exportar para múltiplos backends (Datadog, Grafana Cloud) sem trocar código

5. **Na prática**: setup mínimo funcional em 3 arquivos (tracing.ts + server.ts entry point + um handler com span manual).

6. **Armadilhas** (mínimo 4 com código + fix):
   - Inicializar SDK depois do `import express`: a auto-instrumentation do Express não funciona se o require do Express veio antes do SDK
     ```typescript
     // RUIM
     import express from 'express'; // express importado antes do SDK
     import './tracing';
     
     // BOM
     import './tracing'; // sempre primeiro
     import express from 'express';
     ```
   - Spans não fechados: memory leak silencioso; sempre usar `startActiveSpan` com `finally { span.end() }` ou `withSpan`
   - Sampling 100% em produção: custo de armazenamento explode; usar 1-10% + always-sample para errors
   - Auto-instrumentation sem custo: cada query SQL gera um span — em hot paths com centenas de queries por request, o overhead pode ser perceptível

7. **Em entrevista** (3+ sentenças):
   ```
   "I use OpenTelemetry as the instrumentation layer because it's vendor-neutral — I can switch from Jaeger to Datadog to Grafana Tempo without changing application code. The key setup detail is that the SDK must be initialized before any framework imports, otherwise auto-instrumentation patches don't take effect. For sampling, I use a parent-based sampler with 10% head sampling in production — this keeps storage costs manageable while ensuring that errors and slow requests are always captured if I add tail-based sampling at the collector layer. Manual instrumentation is reserved for business-critical operations like payment processing, where I want explicit span attributes like order ID and amount."
   ```

8. **Vocabulário PT→EN** (mínimo 8):
   - rastreamento → trace
   - trecho de execução → span
   - contexto de rastreamento → trace context
   - propagação → propagation
   - instrumentação automática → auto-instrumentation
   - instrumentação manual → manual instrumentation
   - exportador → exporter (OTLP, Jaeger, Zipkin)
   - amostragem → sampling

9. **Fontes**: [OpenTelemetry JS](https://opentelemetry.io/docs/languages/js/), [W3C Trace Context](https://www.w3.org/TR/trace-context/).

10. **Veja também**: notas 01, 03, 04, 12 do galho + [[Node.js]].

- [ ] **Step 2: Self-check**

Verificar contagem de linhas >= 420. Verificar 6+ exemplos.

- [ ] **Step 3: Commit**

```bash
git add "03-Dominios/Node/Observability e produção/06 - Tracing distribuído com OpenTelemetry.md"
git commit -m "feat(node/g5): add 06 - Tracing distribuído com OpenTelemetry"
```

---

## Task 8: Nota 07 — Profiling avançado com clinic.js

**Files:**
- Create: `03-Dominios/Node/Observability e produção/07 - Profiling avançado com clinic.js.md`

**Mínimo:** 380 linhas. **Código mínimo:** 5 exemplos.

- [ ] **Step 1: Criar a nota 07**

**Frontmatter:**
```yaml
---
title: "Profiling avançado com clinic.js"
created: 2026-05-08
updated: 2026-05-08
type: concept
status: seedling
publish: true
tags:
  - node
  - performance
  - profiling
  - clinic
  - flame-graph
aliases:
  - clinic.js
  - flame graph Node
  - 0x profiler
  - autocannon
---
```

**Seções obrigatórias com conteúdo mínimo:**

1. **TL;DR**: clinic.js é o toolkit de diagnóstico de performance padrão do ecossistema Node. Doctor diagnostica a categoria do problema; Flame gera CPU flame graph; Bubbleprof mostra onde o tempo passa entre ticks do event loop; Heapprof rastreia alocações. `0x` é alternativa direta para flame graphs com menor overhead.

2. **O que é**: profiling é medir onde o tempo vai — CPU ou I/O? qual função? qual operação async? clinic.js automatiza a coleta e gera relatórios HTML navegáveis.

3. **Por que importa**: otimização sem profiling é adivinhação. A maioria dos "problemas de performance" que parecem ser de event loop são na verdade queries lentas ou falta de índice — clinic doctor revela em 1 minuto.

4. **Como funciona** (mínimo 4 subsecções `###`):

   - **clinic doctor** — diagnóstico rápido (qual categoria?):
     ```bash
     # Instalar
     npm install -g clinic autocannon
     
     # Rodar doctor enquanto gera carga
     clinic doctor -- node app.js &
     autocannon -c 100 -d 20 http://localhost:3000/api/users
     
     # Doctor para automaticamente quando o processo termina
     # Gera relatório HTML com diagnóstico: CPU? Event loop? I/O? Memory?
     ```
     Doctor classifica: "Event loop issue detected" → use Flame ou Bubbleprof. "Memory issue" → use Heapprof.

   - **clinic flame** — CPU flame graph (onde o CPU vai):
     ```bash
     clinic flame -- node app.js &
     autocannon -c 100 -d 20 http://localhost:3000/api/slow
     
     # Relatório HTML com flame graph interativo
     # Wide bar = função consumindo muito CPU
     # Barras de plataforma (V8, Node internals) geralmente podem ser ignoradas
     ```

   - **clinic bubbleprof** — onde o tempo passa entre ticks (async):
     ```bash
     clinic bubbleprof -- node app.js &
     autocannon -c 10 -d 30 http://localhost:3000/api/slow
     
     # Mostra "bubbles" — grupos de operações async
     # Bubble grande = tempo passado esperando nessa operação (ex: banco, rede)
     ```

   - **clinic heapprof** — rastrear alocações (onde memória é criada):
     ```bash
     clinic heapprof -- node app.js &
     autocannon -c 50 -d 60 http://localhost:3000/api/slow
     
     # Diferente de heap snapshot: mostra ONDE foi alocado, não O QUE está vivo
     ```

   - **0x — alternativa direta para flame graphs**:
     ```bash
     npm install -g 0x
     
     # Menor overhead que clinic flame, mesmo output visual
     0x -- node app.js
     # Ctrl+C para parar → gera HTML com flame graph
     ```
     Use `0x` quando quiser flame graph com mínimo overhead. Use `clinic flame` quando quiser integração no workflow de clinic.

   - **Workflow integrado completo**:
     ```bash
     # 1. Doctor: identificar categoria
     clinic doctor -- node app.js &
     autocannon -c 100 -d 20 http://localhost:3000
     # → detectou "CPU issue"
     
     # 2. Flame: identificar hot path
     clinic flame -- node app.js &
     autocannon -c 100 -d 20 http://localhost:3000
     # → wide bar em `parseJsonDeep` na rota /api/report
     
     # 3. Otimizar (reduzir JSON parsing)
     
     # 4. Validar com autocannon antes/depois
     autocannon -c 100 -d 30 http://localhost:3000 > before.txt
     # aplicar fix
     autocannon -c 100 -d 30 http://localhost:3000 > after.txt
     # comparar throughput e latência P99
     ```

   - **Lendo um flame graph**: eixo horizontal = tempo (largura = CPU relativa); eixo vertical = call stack (cima = mais específico). Identificar wide bars no topo da stack — essas são as funções para otimizar.

5. **Na prática**: diagnóstico completo passo a passo de um handler lento (`/api/report` com parsing de JSON profundo) → flame → identificar → otimizar → validar.

6. **Armadilhas** (mínimo 4 com código + fix):
   - Profiling sem warm-up: JIT não aqueceu → resultados não representam produção. Rodar 10s de carga antes de coletar.
   - Profiling com `--inspect` ativo: muda o comportamento do V8 (desativa otimizações JIT). Não usar `--inspect` durante profiling de produção.
   - Confundir heapprof com heap snapshot: heapprof = onde foi alocado; heap snapshot = o que está vivo. Para leaks, usar heap snapshot.
   - autocannon com `-c` muito alto: pode saturar o servidor e o profiler ao mesmo tempo → resultados distorcidos. Começar com `-c 20-50`.

7. **Em entrevista** (3+ sentenças):
   ```
   "My performance debugging workflow always starts with clinic doctor to categorize the problem — is it CPU, event loop, async waiting, or memory? This prevents spending time on flame graphs when the actual bottleneck is a slow database query. If doctor points to CPU, I use clinic flame or 0x to generate a flame graph and look for wide bars — functions that consume disproportionate CPU time. I validate fixes with autocannon benchmarks before and after, comparing P99 latency and throughput, because perceived performance improvements without measurement are unreliable."
   ```

8. **Vocabulário PT→EN** (mínimo 6):
   - grafo de chamas → flame graph
   - perfil de performance → performance profile
   - perfil de heap → heap profile
   - ponto quente → hot path / hotspot
   - largura de banda de CPU → CPU throughput
   - aquecimento → warm-up (JIT warm-up)

9. **Fontes**: [clinic.js](https://clinicjs.org/), [0x GitHub](https://github.com/davidmarkclements/0x), [autocannon](https://github.com/mcollina/autocannon).

10. **Veja também**: notas 05, 08, 12 do galho + [[03-Dominios/Node/Runtime e Event Loop/index]] (galho 1, event loop blocking).

- [ ] **Step 2: Self-check**

Verificar contagem de linhas >= 380.

- [ ] **Step 3: Commit**

```bash
git add "03-Dominios/Node/Observability e produção/07 - Profiling avançado com clinic.js.md"
git commit -m "feat(node/g5): add 07 - Profiling avançado com clinic.js"
```

---

## Task 9: Nota 08 — Detecção e diagnóstico de memory leaks

**Files:**
- Create: `03-Dominios/Node/Observability e produção/08 - Detecção e diagnóstico de memory leaks.md`

**Mínimo:** 380 linhas. **Código mínimo:** 5 exemplos.

- [ ] **Step 1: Criar a nota 08**

**Frontmatter:**
```yaml
---
title: "Detecção e diagnóstico de memory leaks"
created: 2026-05-08
updated: 2026-05-08
type: concept
status: seedling
publish: true
tags:
  - node
  - performance
  - memory-leak
  - heap-snapshot
  - gc
aliases:
  - memory leak Node
  - heap snapshot
  - heapUsed crescendo
---
```

**Seções obrigatórias com conteúdo mínimo:**

1. **TL;DR**: memory leaks em Node crescem devagar e só aparecem em produção com carga sustentada. Sinal: `heapUsed` crescendo monotonicamente em métricas. Diagnóstico: heap snapshot via `--inspect` + Chrome DevTools. Comparar 2 snapshots revela objetos que só crescem. Causas: event listeners não removidos, closures, Map/Set sem TTL, timers.

2. **O que é**: memory leak = objeto que deveria ser coletado pelo GC não é coletado porque algo mantém uma referência viva. Em Node, GC é geracional — objetos que sobrevivem a várias minor GCs vão para old generation e custam mais para coletar.

3. **Por que importa**: leak de 1MB/req em serviço com 100 req/s = 100MB/s de crescimento. Em 15 minutos, OOM. Sintoma: pod reinicia periodicamente; heapUsed não decresce após GC major.

4. **Como funciona** (mínimo 4 subsecções `###`):

   - **Monitorar com métricas como sinal inicial**:
     ```typescript
     // Gauge de heapUsed (nota 05) + alert PromQL
     // Alerta: heapUsed crescendo > 10MB em 5 minutos consecutivos
     // PromQL: rate(nodejs_heap_used_bytes[5m]) > 10_000_000
     ```

   - **Workflow com `--inspect` e Chrome DevTools**:
     ```bash
     # Iniciar com inspector
     node --inspect app.js
     # Abrir: chrome://inspect → Open dedicated DevTools for Node
     # Memory tab → Take Heap Snapshot (snapshot 1 — após warm-up)
     # Gerar carga por 5 minutos
     # Memory tab → Take Heap Snapshot (snapshot 2)
     # Selecionar snapshot 2, "Comparison" mode vs snapshot 1
     # Filtrar: # Delta > 0 → objetos que cresceram
     ```

   - **Lendo o heap snapshot**:
     - **Shallow size**: memória do objeto em si
     - **Retained size**: memória que seria liberada SE esse objeto fosse coletado (inclui tudo que ele retém)
     - **Retaining tree**: o que está mantendo esse objeto vivo (o path de referência da GC root)
     - Procurar: objetos com retained size alto e constructor inesperado (ex: `Array`, `Object`, `Closure`)

   - **Forçar GC antes do snapshot** (snapshot mais limpo):
     ```bash
     node --expose-gc app.js
     ```
     ```typescript
     // Em handler de diagnóstico — apenas dev/debug
     app.get('/debug/gc', (_req, res) => {
       global.gc?.();
       res.json(process.memoryUsage());
     });
     ```

   - **Causas comuns e fixes**:
     ```typescript
     // 1. Event listeners não removidos
     // RUIM
     class RequestHandler {
       setup() {
         eventEmitter.on('data', this.handleData); // nunca removido
       }
     }
     // BOM
     class RequestHandler {
       setup() { eventEmitter.on('data', this.handleData); }
       teardown() { eventEmitter.off('data', this.handleData); }
     }
     
     // 2. Cache Map sem TTL
     // RUIM
     const cache = new Map(); // cresce para sempre
     cache.set(userId, userData);
     
     // BOM — LRU com tamanho máximo
     import { LRUCache } from 'lru-cache';
     const cache = new LRUCache({ max: 1000, ttl: 1000 * 60 * 5 }); // 5min
     
     // 3. Closure capturando array grande
     function processLargeData(data: Buffer) {
       const processed = transformData(data); // data é mantido na closure
       return () => processed; // data nunca é coletado enquanto a função existe
     }
     
     // 4. setInterval sem clearInterval
     // RUIM — interval mantém o processo vivo e referências vivas
     const interval = setInterval(() => poll(), 1000);
     // BOM
     const interval = setInterval(() => poll(), 1000);
     process.on('SIGTERM', () => clearInterval(interval));
     ```

   - **WeakMap e WeakRef para caches que não devem impedir GC**:
     ```typescript
     // WeakMap — chave é referência fraca; quando objeto é coletado, entrada some
     const domainCache = new WeakMap<Request, ParsedDomain>();
     
     // WeakRef — referência fraca para o objeto; pode ser null após GC
     const weakRef = new WeakRef(largeObject);
     const obj = weakRef.deref(); // pode ser undefined após GC
     ```

5. **Na prática**: exemplo de leak completo (Map crescendo sem TTL num handler de request) → diagnóstico passo a passo com heap snapshot → fix com LRUCache.

6. **Armadilhas** (mínimo 4 com código + fix):
   - Confundir `heapTotal` crescendo com leak: GC pode aumentar `heapTotal` para performance (menos major GCs). Olhar `heapUsed` não decrescente.
   - Não forçar GC antes do snapshot: objetos "mortos" que ainda não foram coletados aparecem no snapshot e confundem a análise.
   - Shallow vs retained: focar em shallow size ignora o objeto que retém 50MB via referências profundas.
   - Listeners em testes: tests que não limpam listeners deixam estado global contaminado entre testes — use `emitter.removeAllListeners()` no `afterEach`.

7. **Em entrevista** (3+ sentenças):
   ```
   "I diagnose memory leaks with a two-phase approach. First, I confirm the leak with a Prometheus alert on monotonically increasing heap usage — if `nodejs_heap_used_bytes` grows consistently over 15 minutes without decreasing after a major GC, that's a leak signal. Then I take two heap snapshots in Chrome DevTools with a load generation period between them, switch to 'Comparison' mode, and filter by positive delta to find objects growing unexpectedly. The most common causes I've seen in production are Maps used as caches without eviction policies, event listeners added but never removed, and closures in request handlers that inadvertently retain large buffers."
   ```

8. **Vocabulário PT→EN** (mínimo 6):
   - vazamento de memória → memory leak
   - snapshot de heap → heap snapshot
   - tamanho retido → retained size
   - tamanho raso → shallow size
   - referência fraca → weak reference (WeakRef, WeakMap)
   - coleta de lixo geracional → generational garbage collection

9. **Fontes**: [Node.js memory debugging](https://nodejs.org/en/docs/guides/diagnostics/memory), [clinic heapprof](https://clinicjs.org/heapprof/).

10. **Veja também**: notas 05, 07, 12 do galho + [[03-Dominios/Node/Runtime e Event Loop/index]] (galho 1).

- [ ] **Step 2: Self-check**

Verificar contagem de linhas >= 380.

- [ ] **Step 3: Commit**

```bash
git add "03-Dominios/Node/Observability e produção/08 - Detecção e diagnóstico de memory leaks.md"
git commit -m "feat(node/g5): add 08 - Detecção e diagnóstico de memory leaks"
```

---

## Task 10: Nota 09 — Graceful shutdown profundo

**Files:**
- Create: `03-Dominios/Node/Observability e produção/09 - Graceful shutdown profundo.md`

**Mínimo:** 420 linhas. **Código mínimo:** 6 exemplos.

- [ ] **Step 1: Criar a nota 09**

**Frontmatter:**
```yaml
---
title: "Graceful shutdown profundo"
created: 2026-05-08
updated: 2026-05-08
type: concept
status: seedling
publish: true
tags:
  - node
  - producao
  - graceful-shutdown
  - sigterm
  - kubernetes
aliases:
  - graceful shutdown Node
  - SIGTERM handler
  - K8s pod termination
---
```

**Seções obrigatórias com conteúdo mínimo:**

1. **TL;DR**: graceful shutdown = parar de aceitar novas requests, drenar as em andamento, fechar recursos (DB, Redis, filas), sair com código 0. K8s envia SIGTERM antes de remover o pod do load balancer — há um gap de ~5s. Sem graceful shutdown, deploys matam requests em andamento e deixam conexões DB abertas.

2. **O que é**: quando um pod vai ser terminado (deploy, scale-down, node replacement), K8s envia SIGTERM. O processo tem `terminationGracePeriodSeconds` (default: 30s) para limpar. Após esse tempo, K8s força SIGKILL.

3. **Por que importa**: sem SIGTERM handler, `process.exit(0)` imediato mata: (a) requests em andamento com 500 forçado, (b) conexões DB abertas (pool fica sujo), (c) jobs em processamento (dados inconsistentes). Em deploys frequentes, isso vira chuva de erros nos clientes.

4. **Como funciona** (mínimo 5 subsecções `###`):

   - **Fases do graceful shutdown**:
     ```
     1. Receber SIGTERM
     2. Parar de aceitar novas connections (server.close())
     3. Drenar requests em andamento (aguardar handlers terminarem)
     4. Fechar recursos em ordem: DB → Redis → filas → cache
     5. process.exit(0)
     6. Timeout forçado: setTimeout(() => process.exit(1), 30_000)
     ```

   - **Implementação Express**:
     ```typescript
     import express from 'express';
     import { PrismaClient } from '@prisma/client';
     
     const app = express();
     const prisma = new PrismaClient();
     const server = app.listen(3000);
     
     async function shutdown(signal: string) {
       console.log(`Received ${signal}, starting graceful shutdown`);
       
       // Timeout forçado — evitar shutdown pendurado
       const forceExit = setTimeout(() => {
         console.error('Graceful shutdown timeout, forcing exit');
         process.exit(1);
       }, 30_000);
       forceExit.unref(); // não impede shutdown natural
       
       // Parar de aceitar novas connections
       server.close(async () => {
         try {
           await prisma.$disconnect();
           // fechar Redis, filas, etc.
           console.log('Shutdown complete');
           clearTimeout(forceExit);
           process.exit(0);
         } catch (err) {
           console.error('Error during shutdown', err);
           process.exit(1);
         }
       });
     }
     
     process.on('SIGTERM', () => shutdown('SIGTERM'));
     process.on('SIGINT', () => shutdown('SIGINT'));
     ```

   - **Implementação NestJS** — `enableShutdownHooks()` + `onModuleDestroy()`:
     ```typescript
     // main.ts
     const app = await NestFactory.create(AppModule);
     app.enableShutdownHooks(); // captura SIGTERM automaticamente
     await app.listen(3000);
     
     // Em qualquer provider/module
     @Injectable()
     export class DatabaseModule implements OnModuleDestroy {
       async onModuleDestroy() {
         await this.prisma.$disconnect();
       }
     }
     ```

   - **Implementação Fastify**:
     ```typescript
     const fastify = Fastify();
     
     process.on('SIGTERM', async () => {
       try {
         await fastify.close(); // fecha connections + drena
         process.exit(0);
       } catch (err) {
         process.exit(1);
       }
     });
     ```

   - **O gap K8s: SIGTERM → pod-removal do load balancer**:
     ```
     K8s envia SIGTERM ao pod
     ↓ (simultâneo, não sequencial)
     K8s remove pod dos endpoints do Service (~2-5s de propagação)
     
     Durante esses 2-5s, o load balancer ainda pode rotear requests ao pod
     que já está em shutdown. Por isso, adicionar um sleep antes de server.close():
     ```
     ```typescript
     process.on('SIGTERM', async () => {
       // Aguardar propagação de endpoints (~5s)
       await new Promise(r => setTimeout(r, 5000));
       // Agora sim fechar
       server.close(async () => { /* cleanup */ });
     });
     ```
     Alternativamente: readiness probe retorna 503 imediatamente ao receber SIGTERM.

   - **Keep-alive connections bloqueando server.close()**: em Node < 18.2, `server.close()` não fecha keep-alive connections ativas — o processo fica pendurado.
     ```typescript
     // Node 18.2+ — fecha todas as connections incluindo keep-alive
     server.closeAllConnections();
     
     // Node < 18.2 — workaround manual
     const connections = new Set<Socket>();
     server.on('connection', (conn) => {
       connections.add(conn);
       conn.on('close', () => connections.delete(conn));
     });
     
     // No shutdown:
     connections.forEach(conn => conn.destroy());
     ```

5. **Na prática**: código completo Express + Prisma + Redis, pronto para uso.

6. **Armadilhas** (mínimo 5 com código + fix):
   - Não capturar SIGTERM: `process.exit()` imediato sem cleanup
   - Não ter timeout forçado: shutdown pendura se uma connection não fechar; fix: `setTimeout(() => process.exit(1), 30_000)`
   - Esquecer Redis/filas no cleanup: DB fecha mas Redis fica com conexões pendentes
   - Keep-alive bloqueando `server.close()` em Node < 18.2 (ver acima)
   - Ignorar o gap K8s: requests chegando durante SIGTERM → errors desnecessários

7. **Em entrevista** (3+ sentenças):
   ```
   "Graceful shutdown in Node has two parts: application-level and Kubernetes-level. At the application level, the handler captures SIGTERM, stops the HTTP server with `server.close()` to refuse new connections, waits for in-flight requests to complete, then closes external resources — database pool, Redis, message queues — in order, with a forced timeout as a safety net. The Kubernetes complication is that there's a propagation delay of a few seconds between when K8s sends SIGTERM and when the pod is actually removed from the load balancer endpoints, so requests can still arrive during early shutdown. I handle this by either adding a short sleep before closing the server, or by having the readiness probe return 503 immediately on SIGTERM, which signals the load balancer to stop routing faster."
   ```

8. **Vocabulário PT→EN** (mínimo 6):
   - encerramento elegante → graceful shutdown
   - drenagem → draining (requests in flight)
   - sinal de terminação → SIGTERM (termination signal)
   - tempo de graça → grace period / terminationGracePeriodSeconds
   - sonda de prontidão → readiness probe
   - conexão keep-alive → keep-alive connection

9. **Fontes**: [Kubernetes pod lifecycle](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/), [Node.js process signals](https://nodejs.org/api/process.html#signal-events).

10. **Veja também**: notas 10, 11 do galho + [[03-Dominios/Node/Frameworks e arquitetura/index]] (galho 4).

- [ ] **Step 2: Self-check**

Verificar contagem de linhas >= 420.

- [ ] **Step 3: Commit**

```bash
git add "03-Dominios/Node/Observability e produção/09 - Graceful shutdown profundo.md"
git commit -m "feat(node/g5): add 09 - Graceful shutdown profundo"
```

---

## Task 11: Nota 10 — Circuit breaker e fallback com opossum

**Files:**
- Create: `03-Dominios/Node/Observability e produção/10 - Circuit breaker e fallback com opossum.md`

**Mínimo:** 380 linhas. **Código mínimo:** 5 exemplos.

- [ ] **Step 1: Criar a nota 10**

**Frontmatter:**
```yaml
---
title: "Circuit breaker e fallback com opossum"
created: 2026-05-08
updated: 2026-05-08
type: concept
status: seedling
publish: true
tags:
  - node
  - resiliencia
  - circuit-breaker
  - opossum
  - fallback
aliases:
  - circuit breaker Node
  - opossum
  - resiliência Node
---
```

**Seções obrigatórias com conteúdo mínimo:**

1. **TL;DR**: circuit breaker isola falhas de dependências. 3 estados: closed (passando), open (bloqueando), half-open (testando). opossum é a biblioteca padrão Node. Fallback define o que retornar quando open. Sem circuit breaker, dependência lenta degrada todo o sistema por cascata.

2. **O que é**: pattern para evitar falha em cascata. Em vez de esperar timeout de 30s em cada request quando o serviço externo está down, o breaker "abre" após N% de falhas e retorna imediatamente o fallback.

3. **Por que importa**: um serviço de pagamento lento com timeout de 10s, sem circuit breaker, pode segurar 100 threads/conexões por 10s cada. Com circuit breaker open, retorna em < 1ms com fallback.

4. **Como funciona** (mínimo 4 subsecções `###`):

   - **Estados e transições**:
     ```
     CLOSED → requests passam → se error rate > threshold → OPEN
     OPEN → requests bloqueados → retorna fallback → após resetTimeout → HALF-OPEN
     HALF-OPEN → deixa passar 1 request → se ok → CLOSED; se falha → OPEN
     ```

   - **opossum — configuração básica**:
     ```typescript
     import CircuitBreaker from 'opossum';
     
     async function callPaymentService(orderId: string) {
       return fetch(`${PAYMENT_URL}/orders/${orderId}`).then(r => r.json());
     }
     
     const breaker = new CircuitBreaker(callPaymentService, {
       timeout: 3000,                  // falha se > 3s
       errorThresholdPercentage: 50,   // abre após 50% de falhas
       resetTimeout: 30_000,           // tenta half-open após 30s
       volumeThreshold: 5,             // mínimo de requests antes de avaliar % (evita abrir por 1 falha)
     });
     
     // Fallback — retornado quando breaker está open
     breaker.fallback(async (orderId: string) => {
       const cached = await cache.get(`order:${orderId}`);
       if (cached) return cached;
       return { status: 'unavailable', retry: true };
     });
     
     // Uso
     const result = await breaker.fire(orderId);
     ```

   - **Eventos + métricas prom-client**:
     ```typescript
     import { Gauge, Counter } from 'prom-client';
     
     const breakerState = new Gauge({
       name: 'circuit_breaker_state',
       help: '0=closed, 1=open, 2=half-open',
       labelNames: ['name'],
     });
     
     const breakerFallbacks = new Counter({
       name: 'circuit_breaker_fallbacks_total',
       help: 'Total fallbacks triggered',
       labelNames: ['name'],
     });
     
     breaker.on('open', () => breakerState.set({ name: 'payment' }, 1));
     breaker.on('close', () => breakerState.set({ name: 'payment' }, 0));
     breaker.on('halfOpen', () => breakerState.set({ name: 'payment' }, 2));
     breaker.on('fallback', () => breakerFallbacks.inc({ name: 'payment' }));
     ```

   - **Decision tree: circuit breaker vs alternativas** (sem dogma):
     - **Timeout simples**: quando a dependência é crítica e não há fallback útil. Mais simples, mas não isola falhas cumulativas.
     - **Retry com exponential backoff**: quando falhas são transientes (rede flaky). Combina bem com circuit breaker (retry dentro do breaker).
     - **Circuit breaker (opossum)**: quando a dependência pode ficar down por minutos e há fallback útil (cache, valor default).
     - **Bulkhead**: isolar recursos (pool de threads ou conexões) por dependência. Escopo diferente — evita que 1 dependência consuma todo o pool.

   - **Health check manual**:
     ```typescript
     breaker.healthCheck(async () => {
       const res = await fetch(`${PAYMENT_URL}/health`);
       if (!res.ok) throw new Error('payment service unhealthy');
     });
     ```

5. **Na prática**: breaker para HTTP externo + breaker para query DB com fallback de cache Redis.

6. **Armadilhas** (mínimo 4 com código + fix):
   - `volumeThreshold` muito baixo: abre após 1 falha; fix: 5-10 mínimo para reduzir falsos positivos
   - Fallback que também pode falhar: cache down → fallback lança exceção → não há segunda barreira; fix: `try/catch` no fallback
   - `timeout` > `resetTimeout`: breaker nunca chega em half-open porque cada tentativa expira antes de resetTimeout; fix: `timeout < resetTimeout`
   - Não expor estado em métricas: breaker open em produção sem alerta → operadores não sabem

7. **Em entrevista** (3+ sentenças):
   ```
   "A circuit breaker protects against cascading failures from slow or failing dependencies. When a downstream service starts returning errors or timing out, the breaker opens after reaching the error threshold and immediately returns a fallback response instead of waiting for each request to time out. This is different from simple timeouts — timeouts still let all requests through, burning threads while waiting; an open circuit breaker rejects instantly. I use opossum in Node.js, expose the breaker state as a Prometheus gauge, and alert when it stays open for more than a few minutes, which usually indicates a real infrastructure problem rather than a transient spike."
   ```

8. **Vocabulário PT→EN** (mínimo 6):
   - disjuntor → circuit breaker
   - fallback → fallback (retorno alternativo)
   - limiar de erro → error threshold
   - tempo de reset → reset timeout
   - falha em cascata → cascading failure
   - semi-aberto → half-open

9. **Fontes**: [opossum docs](https://nodeshift.dev/opossum/), [Martin Fowler Circuit Breaker](https://martinfowler.com/bliki/CircuitBreaker.html).

10. **Veja também**: notas 04, 09, 11 do galho + [[Node.js]].

- [ ] **Step 2: Self-check**

Verificar contagem de linhas >= 380.

- [ ] **Step 3: Commit**

```bash
git add "03-Dominios/Node/Observability e produção/10 - Circuit breaker e fallback com opossum.md"
git commit -m "feat(node/g5): add 10 - Circuit breaker e fallback com opossum"
```

---

## Task 12: Nota 11 — Connection pool tuning

**Files:**
- Create: `03-Dominios/Node/Observability e produção/11 - Connection pool tuning.md`

**Mínimo:** 380 linhas. **Código mínimo:** 5 exemplos.

- [ ] **Step 1: Criar a nota 11**

**Frontmatter:**
```yaml
---
title: "Connection pool tuning"
created: 2026-05-08
updated: 2026-05-08
type: concept
status: seedling
publish: true
tags:
  - node
  - resiliencia
  - database
  - connection-pool
  - prisma
  - knex
aliases:
  - connection pool Node
  - pool tuning
  - pool exausto
---
```

**Seções obrigatórias com conteúdo mínimo:**

1. **TL;DR**: pool exausto = requests travando aguardando conexão disponível. Cada instância de app tem seu pool — com 10 pods e pool de 20, são 200 conexões no banco. Knex/pg-pool: configurar `min`, `max`, `acquireTimeoutMillis`. Prisma: `connection_limit` na URL. HTTP: `agent` keepalive com `maxSockets`.

2. **O que é**: pool de conexões mantém N conexões abertas para reutilização. Abrir uma conexão TCP + TLS + handshake Postgres custa ~10-50ms — sem pool, cada query paga esse custo.

3. **Por que importa**: pool exausto é silencioso. Não aparece como "banco lento" — aparece como "requests travadas esperando conexão disponível". Timeout do pool vira 500 pro cliente, sem nenhuma query executada.

4. **Como funciona** (mínimo 4 subsecções `###`):

   - **Dimensionamento do pool**:
     ```
     Regra prática: pool_size = (num_cores × 2) + effective_spindle_count
     Para SSDs: effective_spindle_count = 1
     Exemplo: servidor 4 cores → pool = 4×2 + 1 = 9 ≈ 10
     
     IMPORTANTE: com múltiplas instâncias (K8s pods), o total é:
     total_connections = pool_size × num_pods
     10 pods × 20 conexões = 200 conexões no Postgres
     Verificar max_connections do Postgres (default: 100!)
     ```

   - **knex / pg-pool — configuração completa**:
     ```typescript
     const knex = Knex({
       client: 'pg',
       connection: process.env.DATABASE_URL,
       pool: {
         min: 2,               // mínimo de conexões idle
         max: 10,              // máximo (por instância)
         acquireTimeoutMillis: 30_000,  // timeout para adquirir conexão do pool
         idleTimeoutMillis: 10_000,     // liberar conexão idle após 10s
         reapIntervalMillis: 1000,      // checar por connections idle a cada 1s
         createTimeoutMillis: 5000,     // timeout para criar nova conexão
       },
     });
     
     // Gauge prom-client para monitorar pool
     const poolWaiting = new Gauge({
       name: 'db_pool_waiting_requests',
       help: 'Requests waiting for a connection from the pool',
     });
     setInterval(() => {
       poolWaiting.set(knex.client.pool.numPendingAcquires());
     }, 5000);
     ```

   - **Prisma — connection_limit via URL**:
     ```typescript
     // .env
     DATABASE_URL="postgresql://user:pass@host/db?connection_limit=10&pool_timeout=30"
     
     // prisma.ts
     import { PrismaClient } from '@prisma/client';
     
     const prisma = new PrismaClient({
       log: ['warn', 'error'],
     });
     
     // Conectar explicitamente no startup (detecta problemas cedo)
     await prisma.$connect();
     
     // Desconectar no shutdown
     process.on('SIGTERM', async () => {
       await prisma.$disconnect();
     });
     ```

   - **Transações sem finally — leak de conexão**:
     ```typescript
     // RUIM — se der throw, conexão nunca volta ao pool
     const trx = await knex.transaction();
     const result = await trx('users').insert(data);
     // se der erro aqui, trx nunca é committed/rolled back → conexão presa
     await trx.commit();
     
     // BOM — try/finally garante rollback
     const trx = await knex.transaction();
     try {
       const result = await trx('users').insert(data);
       await trx.commit();
       return result;
     } catch (err) {
       await trx.rollback();
       throw err;
     }
     ```

   - **HTTP keepalive com axios / node-fetch**:
     ```typescript
     import http from 'node:http';
     import https from 'node:https';
     import axios from 'axios';
     
     const httpAgent = new http.Agent({
       keepAlive: true,
       maxSockets: 50,         // conexões HTTP simultâneas
       maxFreeSockets: 10,     // manter 10 idle
       timeout: 60_000,
       keepAliveMsecs: 30_000,
     });
     
     const httpsAgent = new https.Agent({
       keepAlive: true,
       maxSockets: 50,
     });
     
     const client = axios.create({
       httpAgent,
       httpsAgent,
       timeout: 5000,
     });
     ```

   - **Diagnóstico de pool exausto em produção**:
     ```sql
     -- Ver conexões ativas no Postgres
     SELECT count(*), state, wait_event_type, wait_event
     FROM pg_stat_activity
     WHERE datname = 'mydb'
     GROUP BY state, wait_event_type, wait_event;
     
     -- Conexões por aplicação
     SELECT application_name, count(*)
     FROM pg_stat_activity
     GROUP BY application_name;
     ```

5. **Na prática**: configuração completa recomendada para app com Prisma + axios + prom-client monitoring.

6. **Armadilhas** (mínimo 5 com código + fix):
   - Múltiplos pods com pool grande: 20 pods × 20 = 400 conexões > `max_connections` do Postgres; fix: calcular total e ajustar por pod
   - Transação sem rollback no catch: conexão fica presa para sempre (ver exemplo acima)
   - Node HTTP agent padrão sem keepalive: cada request abre nova conexão TCP; fix: `http.Agent({ keepAlive: true })`
   - Pool muito pequeno em app I/O-bound: 2 conexões para app com 1000 req/s paralelas → pool exausto; fix: medir throughput real
   - Não monitorar `pool.waiting`: pool exausto silencioso até virar timeout no cliente

7. **Em entrevista** (3+ sentenças):
   ```
   "Connection pool exhaustion is one of the most common silent failures in Node.js APIs — it looks like slow requests or timeouts rather than database errors. The root cause is usually pool misconfiguration: either too small for the load, transactions that aren't rolled back on error causing connections to leak, or multiple pods each holding a large pool that collectively exceeds the database's max_connections. I monitor pool utilization with a Prometheus gauge on pending acquires — if that gauge grows under normal load, it's a pool sizing problem; if it spikes only occasionally, it's likely a transaction leak. For Prisma, I set connection_limit in the database URL; for knex, I configure acquireTimeoutMillis to get an explicit error rather than hanging requests."
   ```

8. **Vocabulário PT→EN** (mínimo 6):
   - pool de conexões → connection pool
   - pool exausto → pool exhaustion
   - aquisição de conexão → connection acquire
   - timeout de aquisição → acquire timeout
   - conexão idle → idle connection
   - keep-alive HTTP → HTTP keepalive

9. **Fontes**: [knex connection pool](https://knexjs.org/guide/#pool), [Prisma connection pool](https://www.prisma.io/docs/orm/prisma-client/setup-and-configuration/databases-connections/connection-pool).

10. **Veja também**: notas 09, 10 do galho + [[Node.js]].

- [ ] **Step 2: Self-check**

Verificar contagem de linhas >= 380.

- [ ] **Step 3: Commit**

```bash
git add "03-Dominios/Node/Observability e produção/11 - Connection pool tuning.md"
git commit -m "feat(node/g5): add 11 - Connection pool tuning"
```

---

## Task 13: Nota 12 — SLOs, dashboards, alertas e cheatsheet

**Files:**
- Create: `03-Dominios/Node/Observability e produção/12 - SLOs, dashboards, alertas e cheatsheet.md`

**Mínimo:** 420 linhas. **Código mínimo:** 6 exemplos (incluindo PromQL e Alertmanager).

- [ ] **Step 1: Criar a nota 12**

**Frontmatter:**
```yaml
---
title: "SLOs, dashboards, alertas e cheatsheet"
created: 2026-05-08
updated: 2026-05-08
type: concept
status: seedling
publish: true
tags:
  - node
  - observability
  - slo
  - prometheus
  - alerting
  - cheatsheet
aliases:
  - SLO Node
  - PromQL cheatsheet
  - observability cheatsheet
---
```

**Seções obrigatórias com conteúdo mínimo:**

1. **TL;DR**: SLI = query PromQL que mede o que importa. SLO = meta percentual. Error budget = o quanto pode falhar antes de violar o SLO. Alertar em burn rate, não em symptom direto. Dashboard de API Node: 5 painéis essenciais.

2. **O que é**: fechamento do galho — como conectar todas as métricas, logs e traces instrumentados nas notas anteriores em SLOs acionáveis e dashboards operacionais.

3. **Por que importa**: instrumentação sem SLO é ruído. SLO sem instrumentação é ficção. A combinação define o que "sistema saudável" significa e quando agir.

4. **Como funciona** (mínimo 4 subsecções `###`):

   - **SLIs como queries PromQL**:
     ```promql
     # Error rate (SLI)
     sum(rate(http_requests_total{status_code=~"5.."}[5m]))
       / sum(rate(http_requests_total[5m]))
     
     # P95 latência (SLI)
     histogram_quantile(0.95,
       sum(rate(http_request_duration_seconds_bucket[5m])) by (le)
     )
     
     # Availability (SLI)
     sum(rate(http_requests_total{status_code!~"5.."}[5m]))
       / sum(rate(http_requests_total[5m]))
     
     # Event loop lag (SLI Node-specific)
     nodejs_eventloop_lag_seconds > 0.05
     ```

   - **Alertas com burn rate** (multi-window, menos ruidoso que threshold simples):
     ```yaml
     # Alertmanager rule
     groups:
       - name: api.slos
         rules:
           - alert: HighErrorBurnRate
             expr: |
               (
                 sum(rate(http_requests_total{status_code=~"5.."}[1h]))
                 / sum(rate(http_requests_total[1h]))
               ) > 14 * 0.001
               and
               (
                 sum(rate(http_requests_total{status_code=~"5.."}[5m]))
                 / sum(rate(http_requests_total[5m]))
               ) > 14 * 0.001
             for: 2m
             labels:
               severity: critical
             annotations:
               summary: "Error burn rate 14x above SLO budget"
     ```

   - **Correlação entre os três pilares em debug real**:
     ```
     1. Metric spike: error rate > 5% às 14:32
     2. Log search (Loki): jq 'select(.level == "error" and .time > "14:32")' → "Connection timeout"
     3. Trace view (Jaeger): trace ID dos logs → span "db.query" de 5000ms
     4. Diagnóstico: connection pool exausto → expandir pool ou reduzir query concurrency
     ```

   - **5 painéis essenciais do dashboard Grafana**:
     ```
     Painel 1: Request rate — rate(http_requests_total[5m]) by route
     Painel 2: Error rate — sum(rate(http_requests_total{status_code=~"5.."}[5m])) / sum(...)
     Painel 3: Latência P50/P95/P99 — histogram_quantile(0.99, ...)
     Painel 4: Event loop lag — nodejs_eventloop_lag_seconds
     Painel 5: DB pool waiting — db_pool_waiting_requests
     ```

5. **Cheatsheet consolidado** (obrigatório — este é o principal diferencial desta nota):

   **Tabela: pino vs winston vs bunyan**

   | | pino | winston | bunyan |
   |---|---|---|---|
   | Performance | Mais rápido (async thread) | Médio | Lento |
   | JSON nativo | Sim | Sim (com formatter) | Sim |
   | Redaction | Nativo | Via plugin | Via serializer |
   | Ecossistema | nestjs-pino, pino-http | Amplamente adotado | Legado |
   | Recomendação 2026 | ✅ Default | Projetos legados | Evitar |

   **Tabela: tipos de métricas**

   | Tipo | Comportamento | Quando usar | Exemplo |
   |---|---|---|---|
   | Counter | Só sobe | Events (requests, errors) | `http_requests_total` |
   | Gauge | Sobe e desce | Estado atual | `active_connections` |
   | Histogram | Distribuição | Latência, tamanho | `request_duration_seconds` |
   | Summary | Quantis no cliente | Raramente — não agregar cross-pod | Evitar em sistemas distribuídos |

   **Tabela: estados do circuit breaker**

   | Estado | Comportamento | Transição |
   |---|---|---|
   | Closed | Requests passam normalmente | → Open se error_rate > threshold |
   | Open | Rejeita imediatamente, retorna fallback | → Half-open após resetTimeout |
   | Half-open | Deixa passar 1 request teste | → Closed se ok; → Open se falha |

   **Checklist de graceful shutdown**

   ```
   [ ] Captura SIGTERM e SIGINT
   [ ] server.close() para parar novas connections
   [ ] server.closeAllConnections() (Node 18.2+) ou workaround para keep-alive
   [ ] Timeout forçado com process.exit(1) após 30s
   [ ] DB disconnect no finally
   [ ] Redis/filas fechados em ordem
   [ ] Sleep de 5s para gap K8s (ou readiness probe 503)
   ```

   **Queries PromQL essenciais**

   ```promql
   # Error rate 5min
   sum(rate(http_requests_total{status_code=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))
   
   # P95 latência
   histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))
   
   # Throughput (req/s)
   sum(rate(http_requests_total[5m]))
   
   # Event loop lag P99
   nodejs_eventloop_lag_seconds
   
   # Heap crescendo (sinal de leak)
   rate(nodejs_heap_used_bytes[10m]) > 10_000_000
   
   # Pool waiting
   db_pool_waiting_requests > 0
   ```

   **Comandos clinic.js**

   | Comando | Quando usar |
   |---|---|
   | `clinic doctor` | Primeira análise — identificar categoria do problema |
   | `clinic flame` | Problema de CPU — encontrar hot paths |
   | `clinic bubbleprof` | Problema de async — onde o tempo passa entre ticks |
   | `clinic heapprof` | Problema de memória — o que está sendo alocado |
   | `0x -- node app.js` | Flame graph com menor overhead que clinic flame |

   **Causas comuns de memory leak**

   | Causa | Sintoma | Fix |
   |---|---|---|
   | Event listener não removido | Objetos acumulam no snapshot | `emitter.off()` no teardown |
   | Map/Set sem limite | Retained size cresce | LRUCache com `max` e `ttl` |
   | Closure capturando buffer grande | Buffer no retaining tree | Não capturar referências grandes |
   | setInterval sem clearInterval | Processo não termina naturalmente | `clearInterval` no shutdown |
   | Variável global acumulando | Object no root scope do snapshot | Usar escopo de request |

6. **Armadilhas** (mínimo 3):
   - SLO muito apertado no início: P99 < 50ms viola constantemente → alert fatigue → ignorados; fix: começar com P95 baseado em baseline real
   - Alertar em symptom e não em causa: "error rate > 0%" dispara por 1 erro em período calmo; fix: usar burn rate com janela de 1h mínima
   - Error budget sem uso: calcular error budget mas não usá-lo para priorizar trabalho esvaziou o propósito

7. **Em entrevista** (3+ sentenças):
   ```
   "I define SLOs starting from user-observable behavior, not from infrastructure metrics. For an API, the primary SLIs are error rate and latency percentiles — usually P95 or P99 — measured over a rolling window. I write these as PromQL queries against the histograms from prom-client and set the SLO target based on the baseline established in the first weeks of production, rather than guessing. For alerting, I use multi-window burn rate rules rather than simple thresholds, because a spike of 10 errors in a quiet period is very different from a sustained 5% error rate — burn rate captures the latter while ignoring the former."
   ```

8. **Vocabulário PT→EN** (mínimo 8):
   - indicador de nível de serviço → SLI
   - objetivo de nível de serviço → SLO
   - orçamento de erros → error budget
   - taxa de queima → burn rate
   - alerta em sintoma → symptom-based alerting
   - alerta em causa → cause-based alerting
   - painel → dashboard
   - consulta → query (PromQL query)

9. **Fontes**: [Google SRE Book](https://sre.google/sre-book/table-of-contents/), [Prometheus alerting rules](https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/), [Grafana dashboards](https://grafana.com/docs/).

10. **Veja também**: notas 01, 04, 05 do galho + [[Node.js]].

- [ ] **Step 2: Self-check**

Verificar contagem de linhas >= 420. Verificar 6+ exemplos incluindo PromQL e Alertmanager.

- [ ] **Step 3: Commit**

```bash
git add "03-Dominios/Node/Observability e produção/12 - SLOs, dashboards, alertas e cheatsheet.md"
git commit -m "feat(node/g5): add 12 - SLOs, dashboards, alertas e cheatsheet"
```

---

## Task 14: Poda do tronco + atualização do index

**Files:**
- Modify: `03-Dominios/JavaScript/Backend/Node.js.md`
- Modify: `03-Dominios/Node/index.md`

**IMPORTANTE:** Ler o tronco antes de modificar para confirmar os níveis reais de heading das seções a podar.

- [ ] **Step 1: Ler o tronco e identificar as seções**

```bash
grep -n "### Connection pool\|### Memory leak\|### Graceful shutdown\|### Circuit breaker" "03-Dominios/JavaScript/Backend/Node.js.md"
```

Anotar os números de linha das 4 seções.

- [ ] **Step 2: Substituir seção "Connection pool exausto"**

Substituir o conteúdo da seção `### Connection pool exausto` (do heading até o próximo `###` ou `##`) por:

```markdown
### Connection pool exausto

> [!nota] Migrado para galho próprio
> Connection pool exausto foi expandido em [[Observability e produção]]. Veja em particular [[11 - Connection pool tuning]] (dimensionamento, configuração Prisma/knex, diagnóstico em produção).
```

- [ ] **Step 3: Substituir seção "N+1 queries"**

A seção de N+1 queries NÃO migra para o galho de observability — pertence ao tópico de banco de dados. **Manter intacta**.

- [ ] **Step 4: Substituir seção "Memory leak"**

Substituir o conteúdo da seção `### Memory leak` por:

```markdown
### Memory leak

> [!nota] Migrado para galho próprio
> Diagnóstico e prevenção de memory leaks foram expandidos em [[Observability e produção]]. Veja em particular [[08 - Detecção e diagnóstico de memory leaks]] (heap snapshots, workflow de comparação, causas comuns e fixes).
```

- [ ] **Step 5: Substituir seção "Graceful shutdown"**

Substituir o conteúdo da seção `### Graceful shutdown` por:

```markdown
### Graceful shutdown

> [!nota] Migrado para galho próprio
> Graceful shutdown foi expandido em [[Observability e produção]]. Veja em particular [[09 - Graceful shutdown profundo]] (SIGTERM, draining, cleanup de recursos, integração K8s).
```

- [ ] **Step 6: Substituir seção "Circuit breaker"**

Substituir o conteúdo da seção `### Circuit breaker` por:

```markdown
### Circuit breaker

> [!nota] Migrado para galho próprio
> Circuit breaker foi expandido em [[Observability e produção]]. Veja em particular [[10 - Circuit breaker e fallback com opossum]] (estados, opossum, fallback, métricas de estado).
```

- [ ] **Step 7: Atualizar frontmatter do tronco**

Atualizar `updated: 2026-05-08` no frontmatter.

Adicionar no `## Veja também` do tronco:

```markdown
- [[Observability e produção]] — galho 5 da trilha Node Senior; observability (logs, métricas, traces), profiling, memory leaks, graceful shutdown, circuit breaker e SLOs
```

- [ ] **Step 8: Atualizar index.md**

Em `03-Dominios/Node/index.md`, na seção "Galhos da trilha Node Senior", adicionar após a linha do galho 4:

```markdown
- [[Observability e produção]] — galho 5: os três pilares (logs, métricas, traces), pino, prom-client, OpenTelemetry, profiling com clinic.js, memory leaks, graceful shutdown, circuit breaker e SLOs
```

- [ ] **Step 9: Commit da poda + index**

```bash
git add "03-Dominios/JavaScript/Backend/Node.js.md" "03-Dominios/Node/index.md"
git commit -m "chore(node/g5): prune trunk - 4 sections migrated to observability galho"
```

---

## Verificação final

- [ ] Pasta `03-Dominios/Node/Observability e produção/` tem 13 arquivos (1 MOC + 12 notas)
- [ ] Todos com `publish: true`
- [ ] `03-Dominios/Node/index.md` lista galho 5
- [ ] `03-Dominios/JavaScript/Backend/Node.js.md` tem 4 callouts de migração para G5
- [ ] Total de commits: 15 (1 MOC + 12 notas + 1 poda + 1 index combinado com poda)

```bash
# Verificar arquivos
ls -la "03-Dominios/Node/Observability e produção/" | wc -l

# Verificar commits do galho
git log --oneline | grep "node/g5"

# Verificar callouts no tronco
grep -c "Migrado para galho próprio" "03-Dominios/JavaScript/Backend/Node.js.md"
```

Expected: 13+ arquivos, 14 commits feat/chore g5, 11+ callouts no tronco (7 anteriores + 4 novos).
