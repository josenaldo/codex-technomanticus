---
title: "Spec — Sub-trilha Observability e produção (Galho 5)"
date: 2026-05-08
author: Josenaldo
status: draft
type: spec
publish: false
---

# Spec — Sub-trilha "Observability e produção" (Galho 5)

## 1. Contexto e motivação

Esta é a **quinta sub-trilha** (galho 5) do roadmap descrito em `2026-05-07-node-roadmap-design.md`. Pressupõe leitura desse roadmap — a metáfora tronco/galhos, os padrões editoriais comuns, e a política de poda do `Node.js.md` monolítico não são repetidos aqui.

Escrever código que funciona em dev é o piso. Em produção, o que diferencia um senior é a capacidade de **instrumentar, observar, diagnosticar e recuperar** um sistema sob carga real. Este galho cobre exatamente isso: os três pilares de observability (logs, métricas, traces), as ferramentas do ecossistema Node idiomático (pino, prom-client, OpenTelemetry), diagnóstico avançado (clinic.js, heap snapshots), e os patterns de resiliência que toda API precisa conhecer (graceful shutdown, circuit breaker, connection pool tuning).

A motivação para criar este galho separado é que o tronco (`Node.js.md`) já tem 4 seções sobre esses temas que cresceram o suficiente para merecer profundidade própria (connection pool exausto, memory leak, graceful shutdown, circuit breaker). Mas faltam os outros 8 tópicos — logs, métricas, traces, profiling, SLOs — que completam o cenário de produção.

Pré-requisitos:
- **Galho 1 (Runtime e Event Loop):** event loop phases, libuv thread pool, bloqueio — o leitor precisa entender por que `--inspect` e o event loop lag gauge importam
- **Galho 4 (Frameworks e arquitetura):** middleware pipeline e como hooks de shutdown se integram ao framework

## 2. Objetivo

Produzir **12 notas atômicas + 1 MOC** (13 arquivos) em `03-Dominios/Node/Observability e produção/`, todas `publish: true`, em PT-BR, cobrindo os três pilares de observability, ferramentas idiomáticas do ecossistema, diagnóstico avançado e patterns de resiliência.

A trilha precisa ser:

- **Atômica** — cada nota linkável e citável separadamente
- **Híbrida em camadas** — TL;DR + corpo técnico, no padrão do roadmap
- **Orientada a produção** — código real, configurações reais, armadilhas reais
- **Idiomática 2026** — Node 22 LTS / 24, pino 9, prom-client 15, OpenTelemetry JS 2, opossum 8+
- **Sem dogma** — onde há tensão legítima (prom-client vs OTEL metrics; clinic.js vs 0x; opossum vs resilience4j) declarar critério pragmático de decisão
- **Orientada a entrevistas internacionais** — cada nota tem "Em entrevista" com frase pronta em inglês (3+ sentenças, não one-liner) + vocabulário PT→EN

## 3. Escopo

### Em escopo

- 13 arquivos markdown em `03-Dominios/Node/Observability e produção/`
- Todos com `publish: true`
- Idioma: PT-BR; termos técnicos em inglês mantidos (log, metric, span, trace, heap, event loop, etc.)
- Wikilinks densos para `[[Node.js]]` (tronco), `[[Runtime e Event Loop]]` (galho 1, especialmente event loop lag e bloqueio), `[[Frameworks e arquitetura]]` (galho 4, hooks de shutdown)
- Pesquisa baseada em fontes primárias (pino docs, prom-client docs, OpenTelemetry JS docs, clinic.js docs, opossum docs)
- 4 tasks de poda do tronco ao fechar o galho (connection pool, memory leak, graceful shutdown, circuit breaker)

### Fora de escopo

- **APM completo (Datadog, New Relic, Dynatrace)** — ferramentas comerciais mencionadas em contexto, mas implementação é out
- **Observability de outras linguagens/runtimes** — esse galho é Node-specific
- **Kubernetes deep dive** — menções pontuais (liveness/readiness probes no contexto de graceful shutdown), não é o foco
- **Kafka consumer observability** — relevante mas escopo separado ([[BullMQ]], [[Kafka]])
- **Frontend observability (Core Web Vitals, Sentry RUM)** — outros domínios
- **Database performance tuning** — connection pool cobre o boundary Node→DB; o que acontece dentro do Postgres é fora
- **Security observability (SIEM, audit logs)** — galho 6 (Segurança)
- **Distributed systems patterns além de circuit breaker** — saga, bulkhead, etc. pertencem a System Design

## 4. Audiência e barra de qualidade

**Audiência primária:** dev senior em prep para entrevista internacional. Já sabe que "logs existem", talvez use `console.log` estruturado. Não sabe configurar pino com redação de campos sensíveis, não tem mental model claro sobre a diferença entre span e metric, nunca configurou um event loop lag gauge.

**Audiência secundária:** o mesmo dev instrumentando ou debugando uma API em produção.

**Barra de qualidade:** ao terminar a sub-trilha, o leitor deve **compreender ao nível exigido de um senior** — decidir, justificar, reconhecer patterns e armadilhas em code review. Concretamente:

1. Explicar em inglês a diferença entre log, metric e trace — quando usar cada um, por que os três são necessários
2. Configurar pino com serializers, redação de campos sensíveis e log levels adequados por ambiente
3. Expor métricas para Prometheus via prom-client com pelo menos Counter, Gauge e Histogram; e adicionar métricas Node-specific (event loop lag, heap used)
4. Instrumentar uma rota com OpenTelemetry para emitir um span com atributos relevantes
5. Diagnosticar um memory leak usando heap snapshots no Chrome DevTools ou `node --inspect`
6. Diagnosticar um event loop bloqueado usando clinic.js ou `--prof`
7. Implementar graceful shutdown com SIGTERM, draining de requests em andamento e cleanup de conexões
8. Configurar opossum com threshold, timeout e fallback; interpretar estados open/half-open/closed
9. Dimensionar connection pool e detectar sintoma de pool exausto antes que vire timeout
10. Definir SLIs/SLOs para uma API simples e traduzir em queries PromQL

## 5. Especificação das notas

### MOC — Observability e produção

**Arquivo:** `Observability e produção.md`

**Frontmatter:**

```yaml
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
```

**Seções obrigatórias:**

- TL;DR callout `[!abstract]` descrevendo o galho em 3-4 linhas
- "Sobre este galho" — contexto, pré-requisitos, audiências
- "Comece por aqui — trilha completa" — wikilinks numerados, organizados em blocos temáticos (A: Visão geral, B: Pilares, C: Diagnóstico, D: Resiliência, E: Fechamento)
- "Rotas alternativas" — 5 rotas: completa + entrevista + produção/debugging + Node-specific metrics + resiliência/SRE
- "Todas as notas" — bloco dataview
- "Veja também" — links para tronco, galhos 1 e 4, e notas externas relevantes

---

### 01 — Os três pilares: logs, métricas e traces

**Arquivo:** `01 - Os três pilares - logs, métricas e traces.md`

**Objetivo:** estabelecer o mental model comum antes de mergulhar em ferramentas. Leitor deve sair com a diferença clara entre os três pilares, os golden signals, e o que são SLI/SLO/SLA.

**Seções obrigatórias:**

- TL;DR (`[!abstract]`)
- O que é
- Por que importa
- Como funciona
  - Os três pilares — definição e quando usar cada um
  - Golden signals (latência, tráfego, erros, saturação) com definição e exemplo de query PromQL
  - SLI, SLO, SLA — definições, relações e exemplos concretos (ex: "P95 latency < 200ms em 99.9% das requests")
  - O triângulo de decisão: quando o problema é de log, de metric ou de trace
- Na prática — como os três se complementam num debug real (ex: métrica sinaliza erro rate alto → log mostra o erro → trace mostra onde no caminho a falha acontece)
- Armadilhas — pelo menos 4, com código demonstrando o problema + fix
- Em entrevista — frase pronta com 3+ sentenças em inglês
- Vocabulário PT→EN — mínimo 8 termos
- Veja também

**Tamanho:** mínimo 380 linhas.

**Código mínimo:** 5 exemplos (pelo menos 1 query PromQL, 1 snippet de trace span, 1 snippet de log estruturado).

---

### 02 — Logging estruturado com pino

**Arquivo:** `02 - Logging estruturado com pino.md`

**Objetivo:** domínio prático de pino — configuração, serializers, redação de dados sensíveis, log levels por ambiente, integração com frameworks.

**Seções obrigatórias:**

- TL;DR
- O que é
- Por que importa — por que logging estruturado importa vs `console.log`, por que pino especificamente (benchmark, serialização JSON assíncrona via async-thread, menor overhead no hot path)
- Como funciona
  - Instalação e configuração básica (logger.info, logger.error, campos padrão)
  - Serializers — customizar como objetos são serializados (ex: reduzir `req` a `{method, url, id}`)
  - Redaction — `redact: ['req.headers.authorization', 'body.password']`
  - Log levels por ambiente — TRACE em dev, INFO em produção, configurável via env var
  - Child loggers — adicionar contexto por request (requestId, userId)
  - Integração com Express (pino-http) e NestJS (nestjs-pino)
  - pino-pretty para dev vs JSON raw para produção
- Na prática — setup completo recomendado (10-15 linhas de configuração, não apenas 2)
- Armadilhas — pelo menos 4, com código problema + fix
- Em entrevista — frase pronta 3+ sentenças
- Vocabulário PT→EN — mínimo 6 termos
- Veja também

**Tamanho:** mínimo 350 linhas.

**Código mínimo:** 6 exemplos (configuração completa, serializer customizado, redaction, child logger, integração Express, integração NestJS).

---

### 03 — Correlation IDs e context propagation

**Arquivo:** `03 - Correlation IDs e context propagation.md`

**Objetivo:** ensinar AsyncLocalStorage como mecanismo para propagar contexto (requestId, traceId, userId) por toda a call stack sem passar por parâmetro — problema que todo sistema distribuído tem.

**Seções obrigatórias:**

- TL;DR
- O que é
- Por que importa — sem correlation ID, logs de request são ilhas; com ele, correlacionamos todos os eventos de uma request
- Como funciona
  - AsyncLocalStorage — API e ciclo de vida
  - Gerando e propagando o requestId via middleware
  - Integrando com pino child loggers via AsyncLocalStorage
  - Propagando para downstream services via headers (W3C Trace Context: `traceparent`)
  - Integração com NestJS (middleware customizado + injection)
  - Como a propagação funciona no contexto de Worker Threads (ALS não atravessa)
- Na prática — exemplo end-to-end: middleware → ALS → log → downstream call → log com mesmo requestId
- Armadilhas — pelo menos 4 (ALS perdida após setTimeout, ALS em Worker Threads, cost de run(), múltiplos stores)
- Em entrevista — 3+ sentenças
- Vocabulário PT→EN — mínimo 6 termos
- Veja também — link para galho 1 (Worker Threads), galho 2 (parallelismo e ALS)

**Tamanho:** mínimo 380 linhas.

**Código mínimo:** 5 exemplos.

---

### 04 — Métricas com prom-client

**Arquivo:** `04 - Métricas com prom-client.md`

**Objetivo:** configurar prom-client para expor métricas no endpoint `/metrics` com os 4 tipos principais, usar labels corretamente e entender o custo de cardinalidade alta.

**Seções obrigatórias:**

- TL;DR
- O que é
- Por que importa — métricas para decisões em tempo real (alertas, dashboards); diferente de logs (post-mortem) e traces (path de uma request)
- Como funciona
  - Os 4 tipos: Counter, Gauge, Histogram, Summary — quando usar cada um com exemplo concreto
  - Configuração do Registry e endpoint `/metrics`
  - Default metrics — o que `collectDefaultMetrics()` expõe automaticamente
  - Labels — adicionar `method`, `status_code`, `route` com cuidados de cardinalidade
  - Histogram buckets — definir buckets adequados para latência (não usar os defaults cegamente)
  - Push vs pull model (Prometheus pull vs pushgateway para cron jobs)
  - Integração com Express e Fastify
- Na prática — setup completo: Counter de requests, Histogram de latência, Gauge de jobs ativos
- Armadilhas — pelo menos 4 (cardinalidade alta, buckets inadequados, labels no hot path, reset do Counter após restart)
- Em entrevista — 3+ sentenças
- Vocabulário PT→EN — mínimo 8 termos
- Veja também

**Tamanho:** mínimo 400 linhas.

**Código mínimo:** 6 exemplos (um por tipo de metric + setup completo + integração com framework).

---

### 05 — Node-specific metrics: event loop lag, GC, heap

**Arquivo:** `05 - Node-specific metrics - event loop lag, GC, heap.md`

**Objetivo:** instrumentar as métricas que são específicas do runtime Node — event loop lag, GC pause duration, heap used/total, active handles/requests — porque os defaults do prom-client não as expõem com granularidade suficiente.

**Seções obrigatórias:**

- TL;DR
- O que é
- Por que importa — métricas genéricas (CPU, memory) não diagnosticam problemas específicos de Node; event loop lag >10ms já é sinal de problema; GC pause causa jank em real-time
- Como funciona
  - Event loop lag gauge — usando `perf_hooks.monitorEventLoopDelay()` ou sampling manual com `hrtime()`
  - GC metrics — usando `node --expose-gc` + `PerformanceObserver` para `gc` entries
  - Heap stats — `process.memoryUsage()` e o que cada campo significa (rss vs heapUsed vs heapTotal vs external)
  - Active handles e requests — `process._getActiveHandles()` e o que handle leaks parecem em métricas
  - Libuv thread pool saturation — como diagnosticar quando o pool está saturado
  - Node.js built-in diagnostics_channel (Node 16+) para hooks de diagnóstico
- Na prática — gauge de event loop lag integrado ao prom-client com threshold de alerta
- Armadilhas — pelo menos 4 (monitorar lag sem baseline, confundir heapTotal com memória usada, GC minor vs major, handles leak silencioso)
- Em entrevista — 3+ sentenças
- Vocabulário PT→EN — mínimo 6 termos
- Veja também — link galho 1 (event loop, bloqueio), nota 04 (prom-client)

**Tamanho:** mínimo 380 linhas.

**Código mínimo:** 5 exemplos (cada métrica com snippet de configuração).

---

### 06 — Tracing distribuído com OpenTelemetry

**Arquivo:** `06 - Tracing distribuído com OpenTelemetry.md`

**Objetivo:** instrumentar uma aplicação Node com OTEL para emitir spans e exportá-los para Jaeger ou OTLP-compatible backend. Entender a anatomia de um trace (span, trace context, baggage).

**Seções obrigatórias:**

- TL;DR
- O que é
- Por que importa — em sistemas distribuídos, um request atravessa múltiplos serviços; trace mostra o path completo com timing, enquanto logs apenas mostram o que aconteceu em cada serviço isolado
- Como funciona
  - Anatomia de um trace: span, trace ID, parent span, baggage
  - OpenTelemetry SDK para Node — setup do TracerProvider, Exporter (OTLP/Jaeger), Propagator (W3C)
  - Auto-instrumentation — `@opentelemetry/auto-instrumentations-node` instrumenta HTTP, Express, pino automaticamente
  - Manual instrumentation — criar spans customizados para operações importantes (DB query, chamada a serviço externo)
  - Atributos de span — `SpanAttributes`, `SemanticAttributes` para padronizar
  - Sampling — tail-based vs head-based; como configurar taxa de sampling
  - Propagação cross-service via `traceparent` header (W3C Trace Context)
  - OTEL Metrics vs prom-client — quando usar cada um (framing sem dogma)
- Na prática — setup mínimo funcional: `sdk.start()` no entry point + 1 span manual num handler crítico
- Armadilhas — pelo menos 4 (inicializar SDK depois do require dos instrumentados, spans não fechados, sampling incorreto em produção, custo de auto-instrumentação sem sampling)
- Em entrevista — 3+ sentenças cobrindo diferença trace/log/metric + como OTEL padroniza
- Vocabulário PT→EN — mínimo 8 termos
- Veja também

**Tamanho:** mínimo 420 linhas.

**Código mínimo:** 6 exemplos (setup TracerProvider, auto-instrumentation, span manual, atributos, exportador, sampling).

---

### 07 — Profiling avançado com clinic.js

**Arquivo:** `07 - Profiling avançado com clinic.js.md`

**Objetivo:** domínio do workflow de profiling com clinic.js (Doctor, Flame, Bubbleprof, Heapprof) para diagnosticar gargalos de CPU, event loop, async e memória. Incluir `0x` como alternativa direta para flame graphs.

**Seções obrigatórias:**

- TL;DR
- O que é
- Por que importa — profiling é a diferença entre otimização baseada em evidência e otimização baseada em intuição; clinic.js é o padrão de facto do ecossistema Node para diagnóstico de performance
- Como funciona
  - `clinic doctor` — diagnóstico rápido: qual categoria de problema? (CPU, event loop, async, I/O)
  - `clinic flame` — CPU flame graph: encontrar hot paths (wrapper de `0x`)
  - `clinic bubbleprof` — async flame: onde o tempo passa entre ticks do event loop
  - `clinic heapprof` — heap allocation profiling: o que está sendo alocado (diferente de heap snapshot)
  - `0x` diretamente — quando usar no lugar de clinic flame (menor overhead, mesmo output)
  - Lendo um flame graph — como identificar wide bars, platform code vs app code, linha de "idle"
  - Workflow integrado: doctor → identifica categoria → flame/bubbleprof/heapprof → diagnóstico → otimização → validação com autocannon
  - `autocannon` para gerar carga durante profiling — setup básico
- Na prática — diagnóstico passo a passo de um endpoint lento
- Armadilhas — pelo menos 4 (profiling em produção sem sampling, confundir heapprof com heap snapshot, JIT warm-up afetando resultados, profiling com `--inspect` ligado muda o comportamento)
- Em entrevista — 3+ sentenças
- Vocabulário PT→EN — mínimo 6 termos
- Veja também — link para notas 05 (Node metrics) e 08 (memory leak)

**Tamanho:** mínimo 380 linhas.

**Código mínimo:** 5 exemplos (comandos clinic + autocannon + leitura de flame graph com anotações).

---

### 08 — Detecção e diagnóstico de memory leaks

**Arquivo:** `08 - Detecção e diagnóstico de memory leaks.md`

**Objetivo:** ensinar o workflow completo de detecção de memory leaks: monitorar crescimento de heap via métricas, confirmar com heap snapshot, identificar o objeto vazando com comparação de dois snapshots, e corrigir as causas comuns.

**Seções obrigatórias:**

- TL;DR
- O que é
- Por que importa — memory leaks em Node são insidiosos: crescem devagar, só aparecem em produção com carga sustentada, e derrubar e reiniciar esconde o sintoma sem resolver a causa
- Como funciona
  - Monitorar heapUsed via prom-client como sinal inicial
  - `node --inspect` + Chrome DevTools → Memory tab → Heap snapshot
  - Workflow de comparação: 2 snapshots em tempos diferentes → objetos que só crescem
  - Lendo o heap snapshot: retained size vs shallow size, retaining tree, constructor
  - `clinic heapprof` para ver onde a alocação acontece (complementar ao snapshot)
  - `--expose-gc` + `global.gc()` para forçar GC antes do snapshot (snapshot mais limpo)
  - Causes comuns: event listeners não removidos, closures, Map/Set sem limite, timers não limpos, caches sem TTL
  - Como `WeakMap` e `WeakRef` ajudam com caches que não precisam manter objetos vivos
- Na prática — código de um leak real (closure que retém array crescente) + diagnóstico passo a passo
- Armadilhas — pelo menos 4 (confundir heapTotal com leak, GC antes de snapshots, shallow vs retained, listeners não removidos em testes)
- Em entrevista — 3+ sentenças
- Vocabulário PT→EN — mínimo 6 termos
- Veja também — link galho 1 (event loop), nota 07 (profiling), nota 05 (heap metrics)

**Tamanho:** mínimo 380 linhas.

**Código mínimo:** 5 exemplos (leak clássico + fix, WeakMap cache, listener cleanup, forçar GC, comando clinic heapprof).

---

### 09 — Graceful shutdown profundo

**Arquivo:** `09 - Graceful shutdown profundo.md`

**Objetivo:** implementar graceful shutdown robusto — captura de sinais (SIGTERM, SIGINT), draining de requests em andamento, cleanup de recursos (DB, cache, message queue), timeout forçado, e integração com liveness/readiness probes do Kubernetes.

**Seções obrigatórias:**

- TL;DR
- O que é
- Por que importa — sem graceful shutdown, deploy mata requests em andamento e deixa conexões DB abertas; K8s envia SIGTERM antes de remover o pod do load balancer — há um gap de ~5s
- Como funciona
  - Fases do graceful shutdown: receber sinal → parar de aceitar novas → drenar em andamento → fechar recursos → exit(0)
  - Captura de SIGTERM e SIGINT
  - `server.close()` vs `server.closeAllConnections()` (Node 18.2+)
  - Timeout forçado: `setTimeout(() => process.exit(1), 30_000)`
  - Fechar recursos em ordem (DB connections, Redis, message queues, caches)
  - Integração com Express — server.close + cleanup manual
  - Integração com NestJS — `app.enableShutdownHooks()` + `onModuleDestroy()`
  - Integração com Fastify — `fastify.close()`
  - K8s: `terminationGracePeriodSeconds`, readinessProbe durante shutdown, o gap SIGTERM→pod-removal
  - Readiness probe retornando 503 durante shutdown
- Na prática — código completo de graceful shutdown Express/NestJS/Fastify, pronto para usar
- Armadilhas — pelo menos 5 (não capturar SIGTERM, não ter timeout forçado, esquecer conexões Redis, keep-alive connections bloqueando server.close(), gap K8s)
- Em entrevista — 3+ sentenças cobrindo gap K8s + draining + sequência de shutdown
- Vocabulário PT→EN — mínimo 6 termos
- Veja também — galho 4 (frameworks), nota 11 (connection pool), nota 04 (health metrics)

**Tamanho:** mínimo 420 linhas.

**Código mínimo:** 6 exemplos (Express, NestJS, Fastify, timeout forçado, readiness probe 503, fechar DB).

---

### 10 — Circuit breaker e fallback com opossum

**Arquivo:** `10 - Circuit breaker e fallback com opossum.md`

**Objetivo:** entender o pattern circuit breaker (estados, transições, threshold), implementá-lo com opossum, e saber quando usar vs alternativas (timeout simples, retry com backoff, bulkhead).

**Seções obrigatórias:**

- TL;DR
- O que é
- Por que importa — sem circuit breaker, uma dependência lenta degrada toda a aplicação por cascata; o breaker isola a falha e permite recovery controlado
- Como funciona
  - Estados: closed, open, half-open — transições e triggers
  - `opossum` API: CircuitBreaker, `options` (timeout, errorThresholdPercentage, resetTimeout, volumeThreshold)
  - Fallback — o que retornar quando o breaker está open (cache, valor default, erro explícito)
  - Eventos — `open`, `close`, `halfOpen`, `fallback`, `success`, `failure` — integração com métricas
  - Health check manual — `breaker.healthCheck(fn)` para testar se dependência voltou
  - Decision tree: circuit breaker vs timeout vs retry com exponential backoff vs bulkhead — quando cada um
  - `opossum` + `axios` / `node-fetch` / `pg` — wrappers de funções async
  - Emitindo métricas de estado do breaker via prom-client
- Na prática — breaker para chamada HTTP externa + breaker para query DB com fallback de cache
- Armadilhas — pelo menos 4 (volumeThreshold muito baixo, timeout maior que resetTimeout, fallback que também pode falhar, não expor estado em métricas)
- Em entrevista — 3+ sentenças cobrindo trade-off circuit breaker vs simples timeout
- Vocabulário PT→EN — mínimo 6 termos
- Veja também — nota 04 (métricas), nota 11 (connection pool), nota 09 (graceful shutdown)

**Tamanho:** mínimo 380 linhas.

**Código mínimo:** 5 exemplos (CircuitBreaker básico, fallback, eventos + métricas, health check, wrapping DB call).

---

### 11 — Connection pool tuning

**Arquivo:** `11 - Connection pool tuning.md`

**Objetivo:** entender como dimensionar pool de conexões DB e HTTP keepalive, detectar pool exausto antes que vire timeout, e configurar corretamente em produção com Prisma, knex/pg-pool, e axios.

**Seções obrigatórias:**

- TL;DR
- O que é
- Por que importa — pool exausto é uma das falhas mais comuns em APIs Node em produção; não é o banco que ficou lento, são as conexões que acabaram
- Como funciona
  - Fundamentos: por que pools existem (custo de abrir conexão TCP + TLS + handshake Postgres)
  - Dimensionamento: regra prática `pool_size = (num_cpus * 2) + effective_spindle_count`; cuidados com múltiplas instâncias (cada pod tem seu pool)
  - knex / pg-pool — configuração de `min`, `max`, `acquireTimeoutMillis`, `idleTimeoutMillis`, `reapIntervalMillis`
  - Prisma — `connection_limit` e `pool_timeout` via URL; `$connect()` explícito
  - Detectar pool exausto — métricas de `pool.waiting`, timeouts, gauge de idle connections
  - Transações sem finally — como uma transação não fechada consome uma conexão do pool para sempre
  - HTTP keepalive — `http.globalAgent.maxSockets`; usando `agent` customizado no axios/node-fetch
  - `agentkeepalive` para controlar keepalive com timeout
  - Diagnóstico em produção: `SHOW pg_stat_activity` + número de conexões ativas
- Na prática — configuração recomendada completa para Prisma + pg-pool + axios em produção
- Armadilhas — pelo menos 5 (múltiplos pods com pool gigante, transação sem rollback, keepalive padrão no Node <18, pool muito pequeno em I/O-bound, não monitorar `pool.waiting`)
- Em entrevista — 3+ sentenças cobrindo pool exausto + detecção + fix
- Vocabulário PT→EN — mínimo 6 termos
- Veja também — nota 10 (circuit breaker), nota 09 (graceful shutdown), nota 04 (métricas)

**Tamanho:** mínimo 380 linhas.

**Código mínimo:** 5 exemplos (pg-pool config, Prisma URL config, axios agent, gauge de pool, diagnóstico SQL).

---

### 12 — SLOs, dashboards, alertas e cheatsheet

**Arquivo:** `12 - SLOs, dashboards, alertas e cheatsheet.md`

**Objetivo:** fechar o galho com uma visão de gestão de SLO — como definir SLIs a partir das métricas do galho, escrever queries PromQL, estruturar alertas que não sejam ruidosos, e condensar tudo num cheatsheet de referência rápida.

**Seções obrigatórias:**

- TL;DR
- O que é
- Por que importa — SLO sem instrumentação é ficção; instrumentação sem SLO é ruído
- Como funciona
  - SLI como query PromQL — transformar métricas do prom-client em SLIs concretos (error rate, P95 latência, availability)
  - SLO como meta percentual — "P95 < 200ms em 99.9% das requests nos últimos 30 dias"
  - Error budget — o que é, como calcular, como usar para priorização
  - Alertas que não são ruidosos — burn rate alerting (multi-window), Alertmanager, `for:` duration
  - Estrutura de dashboard Grafana — 5 painéis recomendados para API Node (request rate, error rate, P50/P95/P99, event loop lag, pool waiting)
  - Queries PromQL prontas para as métricas criadas no galho
  - Correlação entre os três pilares em produção: como usar log → metric → trace juntos num debug
- Cheatsheet consolidado
  - Comparativo: pino vs winston vs bunyan (tabela)
  - Tipos de métricas: Counter/Gauge/Histogram/Summary (tabela)
  - Estados do circuit breaker (tabela)
  - Causas comuns de memory leak (tabela)
  - Comandos clinic.js (tabela)
  - Queries PromQL essenciais (tabela)
  - Checklist de graceful shutdown
- Armadilhas — pelo menos 3 (SLO muito apertado no início, alertar em symptom não em cause, error budget como número sem uso)
- Em entrevista — 3+ sentenças cobrindo como definiria SLOs para uma API nova
- Vocabulário PT→EN — mínimo 8 termos
- Veja também

**Tamanho:** mínimo 420 linhas (cheatsheet justifica o tamanho).

**Código mínimo:** 6 exemplos (pelo menos 4 queries PromQL + 1 Alertmanager rule + 1 estrutura de dashboard JSON/YAML parcial).

---

## 6. MOC central e poda do tronco

### Atualização do index.md

`03-Dominios/Node/index.md` deve ganhar uma linha na seção "Galhos da trilha Node Senior":

```markdown
- [[Observability e produção]] — galho 5: os três pilares (logs, métricas, traces), pino, prom-client, OpenTelemetry, profiling com clinic.js, memory leaks, graceful shutdown, circuit breaker e SLOs
```

### Poda do tronco (Node.js.md)

**Executar ao fechar o galho, não no meio.** Ler o tronco antes de podar para confirmar headings reais.

Substituir cada seção que migrou por callout:

**Seção "Connection pool exausto"** → substituir por:

```markdown
> [!nota] Migrado para galho próprio
> Connection pool exausto foi expandido em [[Observability e produção]]. Veja em particular [[11 - Connection pool tuning]] (dimensionamento, configuração Prisma/knex, diagnóstico em produção).
```

**Seção "Memory leak"** → substituir por:

```markdown
> [!nota] Migrado para galho próprio
> Diagnóstico e prevenção de memory leaks foram expandidos em [[Observability e produção]]. Veja em particular [[08 - Detecção e diagnóstico de memory leaks]] (heap snapshots, workflow de comparação, causas comuns e fixes).
```

**Seção "Graceful shutdown"** → substituir por:

```markdown
> [!nota] Migrado para galho próprio
> Graceful shutdown foi expandido em [[Observability e produção]]. Veja em particular [[09 - Graceful shutdown profundo]] (SIGTERM, draining, cleanup de recursos, integração K8s).
```

**Seção "Circuit breaker"** → substituir por:

```markdown
> [!nota] Migrado para galho próprio
> Circuit breaker foi expandido em [[Observability e produção]]. Veja em particular [[10 - Circuit breaker e fallback com opossum]] (estados, opossum, fallback, métricas de estado).
```

Atualizar `updated:` no frontmatter do tronco.

Adicionar no `## Veja também` do tronco:

```markdown
- [[Observability e produção]] — galho 5 da trilha Node Senior
```

---

## 7. Padrões editoriais comuns (herdados do roadmap)

### Idioma e termos técnicos

- PT-BR exclusivo; termos técnicos em inglês mantidos (log, metric, span, trace, heap, event loop, circuit breaker, etc.)
- Nunca inventar experiências profissionais do autor — se faltar contexto, omitir ou perguntar

### Estrutura por nota

Todas as notas seguem este template (adaptado por nota):

```
TL;DR (callout [!abstract]) → O que é → Por que importa → Como funciona → Na prática → Armadilhas → Em entrevista → Vocabulário PT→EN → Fontes → Veja também
```

### Framing "sem dogma"

Quando o galho cobre tema com tensão legítima (prom-client vs OTEL metrics; clinic.js vs 0x; opossum vs resilience4j), declarar critério pragmático:

> "Use X quando condição A; use Y quando condição B."

Sem isso, a nota envelhece mal.

### Wikilinks

- Todo link para outra nota do galho: `[[01 - Os três pilares - logs, métricas e traces]]`
- Links para galhos anteriores: `[[Runtime e Event Loop]]`, `[[Paralelismo]]`, `[[Streams]]`, `[[Frameworks e arquitetura]]`
- Link para o tronco: `[[Node.js]]`

---

## 8. Critérios de aceitação e richness rubric

Esta seção é especialmente importante quando o plano é executado por outro agente. Os critérios abaixo são **mensuráveis** — não estruturais.

### Por nota atômica

**Tamanho mínimo:** conforme especificado por nota (350-420 linhas). Abaixo do mínimo a nota perde profundidade para o nível senior exigido. O mínimo é piso, não teto — temas densos podem ir até 600-700 linhas.

**"Em entrevista":** obrigatório ter frase pronta com **3+ sentenças interligadas** em inglês cobrindo (a) o que é/como funciona, (b) um trade-off ou decisão, (c) um caveat ou armadilha. Proibido one-liner.

**"Vocabulário PT→EN":** mínimo **6 termos** com tradução, não apenas lista de palavras — formato `termo em PT → English term` ou `termo técnico (PT) → termo em EN` com breve contexto quando necessário.

**Armadilhas:** cada armadilha deve ter:
- (a) Descrição do problema — o que acontece
- (b) Exemplo curto de código demonstrando o problema (2-10 linhas)
- (c) Fix em 1-2 linhas de código ou instrução clara

**"Como funciona":** mínimo **4 subsecções** (headings `###`). Notas com tema denso (nota 06 OTel, nota 09 graceful shutdown) devem ter 5-6 subsecções.

**Código mínimo:** conforme especificado por nota (5-6 exemplos). Cada exemplo deve ser funcional ou claramente didático — não pseudocódigo ambíguo.

**Fontes:** pelo menos 1 link para documentação oficial da ferramenta principal coberta.

### Commit por nota

**ONE commit per note, NOT bundled.** Cada nota = 1 commit dedicado. Exemplo correto:

```
feat(node/g5): add 01 - Os três pilares
feat(node/g5): add 02 - Logging estruturado com pino
feat(node/g5): add 03 - Correlation IDs e context propagation
```

Bundlar múltiplas notas em 1-3 commits é considerado violação do workflow e perde rastreabilidade.

**Mensagens de commit:** `feat(node/g5): add <número> - <título>` — sem Co-Authored-By.

### Self-check antes de cada commit

Antes de commitar cada nota, verificar:

1. Frontmatter completo: title, created, updated, type, status, publish, tags, aliases
2. TL;DR callout presente com conteúdo denso (não uma linha)
3. Contagem de linhas >= mínimo declarado
4. "Em entrevista" tem 3+ sentenças em inglês
5. Vocabulário tem >= 6 termos com tradução
6. Cada armadilha tem: descrição + código-problema + fix
7. "Como funciona" tem >= 4 subsecções (`###`)
8. Número de exemplos de código >= mínimo declarado
9. Wikilinks para tronco e galhos anteriores presentes
10. "Fontes" com pelo menos 1 link oficial

### Poda do tronco

- Ler o tronco antes de podar para confirmar níveis de heading reais
- Substituir as 4 seções conforme § 6 deste spec
- Atualizar `updated:` no frontmatter do tronco
- Adicionar link para [[03-Dominios/Node/Observability e produção/index]] no ## Veja também do tronco
- 1 commit para a poda: `chore(node/g5): prune trunk - 4 sections migrated`

---

## 9. Sequência de entrega

1. MOC (`Observability e produção.md`)
2. Notas 01–12 em ordem (cada uma = 1 commit)
3. Poda do tronco (1 commit)
4. Atualização do `index.md` (1 commit — pode ser junto com poda)

Total: 15 commits (1 MOC + 12 notas + 1 poda + 1 index).

---

## 10. Referências primárias

- [pino](https://getpino.io/) — docs oficiais
- [prom-client](https://github.com/siimon/prom-client) — metrics para Node
- [OpenTelemetry JS](https://opentelemetry.io/docs/languages/js/) — tracing/metrics/logs
- [clinic.js](https://clinicjs.org/) — performance profiling
- [opossum](https://nodeshift.dev/opossum/) — circuit breaker
- [Prometheus querying](https://prometheus.io/docs/prometheus/latest/querying/basics/) — PromQL
- [Node.js diagnostics](https://nodejs.org/en/docs/guides/diagnostics) — guia oficial de diagnóstico
- [AsyncLocalStorage](https://nodejs.org/api/async_context.html) — context propagation
- [W3C Trace Context](https://www.w3.org/TR/trace-context/) — traceparent header
