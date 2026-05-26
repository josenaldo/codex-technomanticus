---
title: "Node-specific metrics: event loop lag, GC e heap"
created: 2026-05-08
updated: 2026-05-08
type: concept
status: seedling
publish: true
tags:
  - node
  - observability
  - metrics
  - event-loop
  - gc
  - heap
  - performance
aliases:
  - Event Loop Lag
  - GC Metrics Node
  - Heap Metrics Node
---

# Node-specific metrics: event loop lag, GC e heap

> [!abstract] TL;DR
> Node.js tem métricas que não existem em outras runtimes: atraso do event loop, coleta de lixo do V8 e gestão de heap — sinais vitais exclusivos do modelo single-threaded.
> Um event loop bloqueado por mais de 100 ms degrada o p99 de latência de toda a aplicação; acima de 500 ms, o sistema está efetivamente indisponível para requisições novas.
> Pressão de GC se manifesta como picos de latência intermitentes — `major GC` frequente é sinal de que o heap está cheio e o V8 está lutando para recuperar memória.
> O trio `nodejs_eventloop_lag_p99_seconds`, `nodejs_heap_size_used_bytes / nodejs_heap_size_total_bytes` e `nodejs_gc_duration_seconds` deve constar em todo dashboard Node.js de produção.

Esta nota faz parte de [[03-Dominios/Node/Observability e produção/index]] e expande as métricas de runtime expostas por `collectDefaultMetrics()` do [[04 - Métricas com prom-client]]. A nota [[08 - Detecção e diagnóstico de memory leaks]] retoma o tema de heap e GC com ferramentas de diagnóstico mais profundas (heap snapshots, clinic.js).

## O que é

Toda aplicação em produção precisa de métricas. A maioria dos stacks cobre métricas de nível de aplicação (requisições por segundo, latência HTTP, taxa de erro) e de nível de infraestrutura (CPU, memória do SO, disco). Node.js, porém, tem uma camada intermediária obrigatória: as **métricas de runtime**.

Essas métricas não existem em outros runtimes por uma razão simples: Node.js tem características arquiteturais únicas que criam pontos de falha únicos.

### Por que Node.js tem métricas exclusivas

**Single-threaded event loop.** Todo código JavaScript no Node.js executa em uma única thread. Quando um trecho de código síncrono demora mais do que o esperado — um loop pesado, uma deserialização de JSON grande, uma operação de criptografia não delegada ao thread pool — o event loop fica bloqueado. Durante esse bloqueio, nenhuma outra requisição é processada. Isso não existe da mesma forma em linguagens com threads por requisição (Java, Go com goroutines independentes): lá, uma thread lenta afeta apenas ela mesma.

**V8 como engine JavaScript.** O V8 (engine do Node.js e Chrome) usa um garbage collector geracional com fases distintas — coleta rápida da geração jovem (Scavenge) e coleta completa da geração antiga (MarkSweepCompact). Essas fases pausam ou interferem com a execução do código (stop-the-world nas fases completas). Quanto mais memória o processo usa, mais frequentes e longas ficam as coletas completas.

**Heap gerenciado pelo V8.** O Node.js não usa `malloc/free` diretamente para objetos JavaScript. O V8 gerencia um heap próprio dividido em espaços com finalidades específicas. Quando o heap se esgota, o processo termina com `FATAL ERROR: CALL_AND_RETRY_LAST Allocation failed - JavaScript heap out of memory` — sem aviso prévio se você não monitorar.

Esses três fatores tornam as métricas de runtime Node.js **sinais vitais** — não métricas opcionais. Um sistema sem alertas em event loop lag e heap ratio está voando sem instrumentos.

## Por que importa

### Event loop lag = latência degradada para todos

O event loop lag é o intervalo entre o momento em que uma callback é agendada e o momento em que ela efetivamente executa. Em condições normais esse valor fica abaixo de 10 ms. Quando o loop está bloqueado por código síncrono pesado:

- Requisições HTTP ficam em fila esperando o loop estar disponível
- Timeouts de cliente disparam antes das respostas chegarem
- O p99 de latência sobe drasticamente — mesmo que o p50 pareça normal
- Health checks `/health` podem não responder, causando reinícios prematuros do orquestrador

> [!warning] O p50 mente quando o loop está bloqueado
> Se um endpoint leva 5 ms em média mas tem event loop lag de 300 ms, seu p99 real pode ser 305 ms ou mais. O dashboard de latência de aplicação vai mostrar uma linha plana enquanto 1% dos usuários sofre timeouts. Monitore event loop lag separadamente — não confie só na latência HTTP para detectar esse problema.

### GC pressure = picos de latência imprevisíveis

O garbage collector do V8 roda na mesma thread principal (para operações de stop-the-world). Durante um `MarkSweepCompact` (GC major), o JavaScript fica pausado. Uma coleta de heap de 200 MB pode levar 50–200 ms. Se isso acontece a cada 30 segundos, você tem picos de latência periódicos que parecem misteriosos nos logs — nenhum código lento, nenhum banco de dados travado, mas o p99 sobe periodicamente.

**GC major frequente não é normal.** Se o coletor de lixo está rodando coletas completas várias vezes por minuto, isso indica que objetos estão sendo promovidos para a geração antiga (old space) mais rápido do que o GC consegue coletar. O problema geralmente é um memory leak ou padrões de alocação que geram muitos objetos de longa vida.

### Heap exhaustion = crash sem aviso

O V8 tem um limite de heap padrão que varia com a versão e a memória disponível (tipicamente 1.5 GB em sistemas de 64 bits, mas configurável via `--max-old-space-size`). Quando o heap atinge 100%, o processo trava com OOM. Não há exception para capturar, não há graceful shutdown — o processo morre.

Alertar apenas em OOM é alertar tarde demais. O alerta correto é em **85% de uso do heap** — o processo ainda está de pé, há tempo para investigar, drenar conexões e reiniciar de forma controlada.

### Active handles = file descriptor leaks

Handles são recursos do sistema mantidos pelo libuv: sockets TCP, file descriptors, timers, streams. O Node.js não fecha automaticamente handles quando você esquece de chamar `.destroy()` ou `.close()`. Handles que acumulam consomem file descriptors do SO — quando o limite (`ulimit -n`) é atingido, o processo não consegue mais abrir conexões, aceitar requisições ou escrever logs.

## Como funciona

### Event loop lag

O **event loop lag** (atraso do loop de eventos) é o tempo que uma microtarefa ou callback espera antes de ser executada após ter sido agendada. Em condições ideais, esse valor é próximo de zero — apenas o overhead de scheduling do SO. Em condições de carga ou de código bloqueante, ele cresce.

**Por que `Date.now()` é o jeito errado de medir:**

```js
// ERRADO — medir com Date.now() afeta o próprio loop e é impreciso
const start = Date.now();
setImmediate(() => {
  const lag = Date.now() - start;
  console.log(`lag: ${lag}ms`); // resolução de 1ms, overhead de Date.now() acumula
});
```

Esse padrão é impreciso (resolução de milissegundo), intrusivo (o próprio `setImmediate` adiciona ao lag medido) e não fornece percentis — você só tem o valor instantâneo, não a distribuição.

**A forma correta: `node:perf_hooks` com `monitorEventLoopDelay()`**

O módulo `node:perf_hooks` expõe `monitorEventLoopDelay()`, que usa um mecanismo interno de alta precisão (nanosegundos) para medir o atraso entre as iterações do event loop. Ele retorna um `IntervalHistogram` que acumula amostras ao longo do tempo e permite consultar percentis como p50, p95 e p99.

```js
// event-loop-lag.js
import { monitorEventLoopDelay } from 'node:perf_hooks';
import { Gauge } from 'prom-client';

// resolution: intervalo de amostragem em ms (padrão: 10ms)
// valores menores = mais preciso, mais overhead
const histogram = monitorEventLoopDelay({ resolution: 20 });
histogram.enable();

// Gauge para expor o p99 do lag ao Prometheus
const eventLoopLagP99 = new Gauge({
  name: 'nodejs_eventloop_lag_p99_seconds',
  help: 'P99 do atraso do event loop em segundos (medido com monitorEventLoopDelay)',
});

const eventLoopLagMean = new Gauge({
  name: 'nodejs_eventloop_lag_mean_seconds',
  help: 'Média do atraso do event loop em segundos',
});

// Atualiza a cada 5 segundos (ou no intervalo de scrape do Prometheus)
// histogram.percentile(99) retorna nanosegundos — dividir por 1e9 para segundos
setInterval(() => {
  const p99Ns = histogram.percentile(99);
  const meanNs = histogram.mean;

  eventLoopLagP99.set(p99Ns / 1e9);
  eventLoopLagMean.set(meanNs / 1e9);

  // Reset do histograma para a próxima janela de coleta
  histogram.reset();
}, 5_000);
```

> [!info] Thresholds de alerta para event loop lag
> - **< 50 ms** — normal (tráfego leve a moderado)
> - **50–100 ms** — atenção (investigar código síncrono pesado)
> - **100–500 ms** — amarelo / degradado (p99 de usuários está sendo afetado)
> - **> 500 ms** — vermelho / crítico (aplicação efetivamente bloqueada)

**Nota sobre `collectDefaultMetrics()`:** O `prom-client` expõe automaticamente `nodejs_eventloop_lag_seconds` quando você chama `collectDefaultMetrics()`. A métrica customizada acima é útil quando você precisa de controle sobre a janela de amostragem ou quer separar mean de p99 como gauges independentes.

### GC metrics

O V8 executa diferentes tipos de coleta de lixo conforme a necessidade:

| Tipo | Nome técnico | Quando ocorre | Impacto |
|------|-------------|---------------|---------|
| **Scavenge** | Minor GC | Geração jovem (new space) está cheia | Rápido (< 5 ms tipicamente), frequente |
| **MarkSweepCompact** | Major GC | Geração antiga (old space) está cheia | Lento (50–500 ms), para o mundo |
| **IncrementalMarking** | Incremental | Preventivo, entre Scavenges | Distribuído, menor impacto por iteração |
| **ProcessWeakCallbacks** | Weak refs | Limpeza de referências fracas | Muito rápido |

**`collectDefaultMetrics()` expõe `nodejs_gc_duration_seconds`** como um histograma com label `gc_type`. Isso permite calcular tanto a frequência quanto a duração de cada tipo de GC:

```promql
# Taxa de GC major por minuto
rate(nodejs_gc_duration_seconds_count{gc_type="MarkSweepCompact"}[5m]) * 60

# Duração média de GC major
rate(nodejs_gc_duration_seconds_sum{gc_type="MarkSweepCompact"}[5m])
/ rate(nodejs_gc_duration_seconds_count{gc_type="MarkSweepCompact"}[5m])
```

**Como detectar GC pressure:**
- GC major (MarkSweepCompact) mais de 2–3 vezes por minuto indica pressão
- Duração de GC major crescendo ao longo do tempo indica heap aumentando
- Proporção Scavenge:MarkSweep caindo indica que objetos estão sendo promovidos para old space mais rápido do que o esperado

**`PerformanceObserver` para eventos de GC em detalhe:**

O `PerformanceObserver` com `entryTypes: ['gc']` fornece acesso a cada evento de GC individualmente, com tipo, duração e flags adicionais. É útil para logging detalhado ou para métricas customizadas por tipo de GC.

```js
// gc-observer.js
import { PerformanceObserver } from 'node:perf_hooks';
import { Histogram } from 'prom-client';

// Histograma customizado por tipo de GC
const gcDuration = new Histogram({
  name: 'app_gc_duration_ms',
  help: 'Duração de eventos de GC em milissegundos',
  labelNames: ['kind'],
  buckets: [1, 5, 10, 25, 50, 100, 200, 500],
});

// Mapeamento dos tipos numéricos do V8 para nomes legíveis
const GC_KIND = {
  1: 'Scavenge',
  2: 'MarkSweepCompact',
  4: 'IncrementalMarking',
  8: 'ProcessWeakCallbacks',
};

const obs = new PerformanceObserver((list) => {
  for (const entry of list.getEntries()) {
    // entry.duration: duração em ms (ponto flutuante)
    // entry.detail.kind: tipo de GC como inteiro (ver GC_KIND acima)
    const kind = GC_KIND[entry.detail.kind] ?? `unknown_${entry.detail.kind}`;

    gcDuration.observe({ kind }, entry.duration);

    // Log apenas GCs lentos para não inundar os logs
    if (entry.duration > 50) {
      console.log({
        msg: 'slow GC detected',
        kind,
        durationMs: entry.duration.toFixed(2),
      });
    }
  }
});

obs.observe({ entryTypes: ['gc'] });
```

> [!tip] `entry.detail` requer Node.js >= 16
> Em versões antigas, `entry.detail` pode ser `undefined`. Use `entry.entryType === 'gc'` como guard e consulte a documentação da versão específica.

### Heap e memória

O heap do V8 é dividido em **espaços** com finalidades distintas. Entender essa estrutura é fundamental para diagnosticar problemas de memória:

| Espaço | Função | O que vai parar lá |
|--------|--------|-------------------|
| `new_space` | Geração jovem | Objetos recém-alocados; GC aqui é rápido |
| `old_space` | Geração antiga | Objetos que sobreviveram a 2+ Scavenges |
| `code_space` | Código JIT | Bytecode compilado pelo V8 |
| `large_object_space` | Objetos grandes | Objetos > ~500 KB (alocados diretamente) |
| `map_space` | Hidden classes | Metadados de forma de objetos (internos ao V8) |

**`process.memoryUsage()` — os campos:**

```js
// memory-snapshot.js
function logMemoryUsage() {
  const mem = process.memoryUsage();
  // mem.rss: Resident Set Size — memória total do processo no SO (heap + stack + código)
  // mem.heapTotal: tamanho total do heap V8 alocado (pode crescer sob demanda)
  // mem.heapUsed: heap V8 efetivamente em uso por objetos JavaScript
  // mem.external: memória C++ fora do heap V8 (Buffers, bindings nativos)
  // mem.arrayBuffers: subconjunto de external — alocações de ArrayBuffer/Buffer

  const heapRatio = mem.heapUsed / mem.heapTotal;

  console.log({
    msg: 'memory snapshot',
    rss_mb: (mem.rss / 1024 / 1024).toFixed(1),
    heap_used_mb: (mem.heapUsed / 1024 / 1024).toFixed(1),
    heap_total_mb: (mem.heapTotal / 1024 / 1024).toFixed(1),
    external_mb: (mem.external / 1024 / 1024).toFixed(1),
    array_buffers_mb: (mem.arrayBuffers / 1024 / 1024).toFixed(1),
    heap_ratio: heapRatio.toFixed(3),
  });

  if (heapRatio > 0.85) {
    console.warn({ msg: 'heap usage critical', heap_ratio: heapRatio });
  }
}

setInterval(logMemoryUsage, 30_000);
```

**`v8.getHeapSpaceStatistics()` — snapshot detalhado por espaço:**

```js
// heap-spaces.js
import v8 from 'node:v8';

function logHeapSpaces() {
  const spaces = v8.getHeapSpaceStatistics();
  // Retorna array de objetos com: space_name, space_size, space_used_size,
  // space_available_size, physical_space_size

  for (const space of spaces) {
    const usedMb = (space.space_used_size / 1024 / 1024).toFixed(2);
    const totalMb = (space.space_size / 1024 / 1024).toFixed(2);
    const ratio = space.space_size > 0
      ? (space.space_used_size / space.space_size).toFixed(3)
      : '0.000';

    console.log({
      msg: 'heap space snapshot',
      space: space.space_name,   // e.g. "old_space", "new_space"
      used_mb: usedMb,
      total_mb: totalMb,
      ratio,
    });
  }
}

logHeapSpaces();
```

**Métricas de heap expostas pelo `prom-client` via `collectDefaultMetrics()`:**

| Métrica | Tipo | Descrição |
|---------|------|-----------|
| `nodejs_heap_size_used_bytes` | Gauge | `process.memoryUsage().heapUsed` |
| `nodejs_heap_size_total_bytes` | Gauge | `process.memoryUsage().heapTotal` |
| `nodejs_external_memory_bytes` | Gauge | `process.memoryUsage().external` |
| `nodejs_heap_space_size_used_bytes` | Gauge | Por espaço (label `space`) |
| `nodejs_heap_space_size_total_bytes` | Gauge | Por espaço (label `space`) |
| `nodejs_heap_space_size_available_bytes` | Gauge | Por espaço (label `space`) |

### Active handles e requests

**Handles** são recursos do libuv mantidos pelo event loop: sockets TCP/UDP, file descriptors, timers (`setTimeout`, `setInterval`), streams, child processes. O event loop continua rodando enquanto houver handles ativos — e o processo não encerra naturalmente se handles ficarem abertos.

**Requests** são operações assíncronas em andamento no libuv: leituras de arquivo, conexões TCP sendo estabelecidas, queries DNS.

**`collectDefaultMetrics()` expõe:**

| Métrica | O que mede |
|---------|-----------|
| `nodejs_active_handles_total` | Total de handles abertos no libuv |
| `nodejs_active_handles` | Por tipo (label `type`: `WriteStream`, `Socket`, `Timer`, etc.) |
| `nodejs_active_requests_total` | Total de operações assíncronas em andamento |

**O que um valor alto de active handles indica:**

- **`Socket` alto** — conexões TCP não fechadas. Pode ser connection pool com `maxConnections` mal configurado, ou ausência de `socket.destroy()` em handlers de erro.
- **`Timer` alto** — `setInterval` ou `setTimeout` criados sem serem limpos (`clearTimeout`, `clearInterval`). Comum em código que cria timers dentro de loops ou handlers sem cleanup.
- **`WriteStream` / `ReadStream` alto** — file descriptors não fechados. `fs.createReadStream()` sem `.destroy()` em caso de erro.

> [!warning] Limite de file descriptors
> Em sistemas Linux, o limite padrão de file descriptors por processo é 1024 (`ulimit -n`). Cada handle de socket, arquivo ou pipe consome um file descriptor. Quando o limite é atingido, `EMFILE: too many open files` começa a aparecer nos logs — geralmente a causa é handles não fechados acumulados ao longo de horas ou dias.

## Na prática

### Setup completo: event loop lag, GC e heap

```js
// observability/node-metrics.js
import { monitorEventLoopDelay, PerformanceObserver } from 'node:perf_hooks';
import v8 from 'node:v8';
import { Gauge, Histogram, collectDefaultMetrics, Registry } from 'prom-client';

export function setupNodeMetrics(registry = new Registry()) {
  // 1. Métricas padrão do prom-client (inclui heap, GC, handles, eventloop)
  collectDefaultMetrics({ register: registry });

  // 2. Event loop lag customizado com percentis
  const elHistogram = monitorEventLoopDelay({ resolution: 20 });
  elHistogram.enable();

  const elLagP50 = new Gauge({
    name: 'app_eventloop_lag_p50_seconds',
    help: 'P50 do atraso do event loop em segundos',
    registers: [registry],
  });

  const elLagP99 = new Gauge({
    name: 'app_eventloop_lag_p99_seconds',
    help: 'P99 do atraso do event loop em segundos',
    registers: [registry],
  });

  setInterval(() => {
    elLagP50.set(elHistogram.percentile(50) / 1e9);
    elLagP99.set(elHistogram.percentile(99) / 1e9);
    elHistogram.reset();
  }, 5_000).unref(); // .unref() para não impedir shutdown do processo

  // 3. GC observer para logging de GCs lentos
  const GC_KIND = {
    1: 'Scavenge',
    2: 'MarkSweepCompact',
    4: 'IncrementalMarking',
    8: 'ProcessWeakCallbacks',
  };

  const gcObs = new PerformanceObserver((list) => {
    for (const entry of list.getEntries()) {
      const kind = GC_KIND[entry.detail?.kind] ?? 'unknown';
      if (entry.duration > 100) {
        console.warn({ msg: 'slow GC', kind, durationMs: entry.duration.toFixed(2) });
      }
    }
  });
  gcObs.observe({ entryTypes: ['gc'] });

  // 4. Heap spaces gauge
  const heapSpaceUsed = new Gauge({
    name: 'app_heap_space_used_bytes',
    help: 'Bytes em uso por espaço do heap V8',
    labelNames: ['space'],
    registers: [registry],
  });

  setInterval(() => {
    for (const space of v8.getHeapSpaceStatistics()) {
      heapSpaceUsed.set({ space: space.space_name }, space.space_used_size);
    }
  }, 15_000).unref();

  return registry;
}
```

### PromQL: alertas essenciais para Node.js

```yaml
# alertas/node-runtime.yml
groups:
  - name: node_runtime
    rules:
      # Event loop lag crítico (p99 > 500ms)
      - alert: NodeEventLoopLagCritical
        expr: nodejs_eventloop_lag_p99_seconds * 1000 > 500
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Event loop lag crítico em {{ $labels.instance }}"
          description: "P99 do event loop lag está em {{ $value | humanizeDuration }}"

      # Event loop lag degradado (p99 > 100ms)
      - alert: NodeEventLoopLagWarning
        expr: nodejs_eventloop_lag_p99_seconds * 1000 > 100
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "Event loop lag elevado em {{ $labels.instance }}"

      # Heap acima de 85% — alerta antes do OOM
      - alert: NodeHeapUsageHigh
        expr: >
          nodejs_heap_size_used_bytes / nodejs_heap_size_total_bytes > 0.85
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Uso de heap alto em {{ $labels.instance }}"
          description: "Heap em uso: {{ $value | humanizePercentage }}"

      # GC major frequente (mais de 3x por minuto)
      - alert: NodeGCMajorFrequent
        expr: >
          rate(nodejs_gc_duration_seconds_count{gc_type="MarkSweepCompact"}[5m]) * 60 > 3
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "GC major frequente em {{ $labels.instance }}"
          description: "Mais de 3 coletas full GC por minuto — investigar memory leak"
```

> [!info] Convertendo lag para milissegundos no PromQL
> `nodejs_eventloop_lag_p99_seconds` está em segundos. Multiplique por 1000 para obter milissegundos antes de comparar com thresholds em ms: `nodejs_eventloop_lag_p99_seconds * 1000 > 100`.

### Consultas PromQL para dashboard

```promql
# Heap ratio (usar em gauge do dashboard)
nodejs_heap_size_used_bytes / nodejs_heap_size_total_bytes

# Uso de heap em MB
nodejs_heap_size_used_bytes / 1024 / 1024

# Taxa de GC major por minuto
rate(nodejs_gc_duration_seconds_count{gc_type="MarkSweepCompact"}[5m]) * 60

# Duração média de GC Scavenge nos últimos 5 minutos
rate(nodejs_gc_duration_seconds_sum{gc_type="Scavenge"}[5m])
/ rate(nodejs_gc_duration_seconds_count{gc_type="Scavenge"}[5m])

# Event loop lag p99 em milissegundos
nodejs_eventloop_lag_p99_seconds * 1000

# Active handles por tipo
nodejs_active_handles{job="my-api"}
```

## Armadilhas

### 1. Medir event loop lag com `Date.now()` ou `setImmediate` manual

```js
// ERRADO — padrão que parece razoável mas é problemático
setImmediate(() => {
  const lag = Date.now() - expectedTime; // resolução de 1ms, drift acumula
});
```

O problema é duplo: `Date.now()` tem resolução de 1 ms (o lag real pode ser de frações de milissegundo), e o próprio `setImmediate` adiciona overhead ao loop que está sendo medido. O resultado é uma medição que subestima o lag real e distorce as estatísticas. Use sempre `monitorEventLoopDelay()` de `node:perf_hooks`.

### 2. Alertar apenas em OOM — tarde demais

Um processo que atingiu 100% do heap já está morto ou em processo de morte. O V8 vai executar GCs desesperados, cada vez mais longos, antes de desistir e lançar o erro fatal. O correto é alertar em **85% de uso** (`heapUsed / heapTotal > 0.85`), quando ainda há tempo para:

- Investigar o que está consumindo memória (`--inspect` + heap snapshot)
- Drenar conexões e reiniciar o processo de forma controlada
- Escalar horizontalmente enquanto o problema é investigado

Alertar em 95% ou "quando cair" significa que você vai ser acordado às 3h para um post-mortem, não para uma mitigação.

### 3. Ignorar `nodejs_active_handles` alto

Handles ativos acumulando é um dos leaks mais silenciosos em Node.js. O processo parece saudável (CPU baixo, latência normal), mas lentamente consome todos os file descriptors disponíveis. Quando `nodejs_active_handles` cresce continuamente ao longo do tempo (não apenas com carga — de forma permanente), isso indica handles não sendo fechados. Os candidatos mais comuns são:

- Sockets de banco de dados que abriram mas não voltaram para o pool
- `fs.createReadStream()` em handlers de erro sem `.destroy()`
- `setInterval` criados dentro de handlers de requisição sem `clearInterval`

Coloque um alerta se `nodejs_active_handles` crescer mais de 20% em 30 minutos sem crescimento equivalente de carga.

### 4. GC major frequente "não é feature, é bug"

É tentador normalizar GC major frequente em aplicações com alto throughput. Mas GC major frequente significa que a geração antiga está constantemente cheia, o que significa que objetos com vida longa estão se acumulando mais rápido do que o GC consegue coletar. Isso é quase sempre um memory leak ou um padrão de alocação patológico (ex.: acumular requisições em memória antes de processar em batch, sem limite de tamanho).

A resposta correta para GC major frequente é investigar com heap snapshot (ver [[08 - Detecção e diagnóstico de memory leaks]]), não aumentar `--max-old-space-size` indefinidamente.

### 5. Bônus: confiar em `heapTotal` como limite real

`heapTotal` é o tamanho **atual** do heap alocado pelo V8 — não o limite máximo. O V8 pode crescer o heap até `--max-old-space-size` sob demanda. A razão `heapUsed / heapTotal` pode parecer saudável (ex.: 60%) enquanto `heapTotal` ainda está crescendo e se aproximando do limite. Para alertas mais precisos, considere também monitorar `heapTotal` absoluto e comparar com o limite configurado.

## Em entrevista

**What is event loop lag and why does it matter for a Node.js service?**
Event loop lag is the delay between when a callback or microtask is scheduled and when it actually executes on the single JavaScript thread. In a healthy Node.js process under normal load, this lag is typically under 10 milliseconds; when synchronous CPU-intensive code blocks the event loop, this value can spike to hundreds of milliseconds, causing all pending HTTP requests to queue up and dramatically increasing the p99 latency for every client connected to the service.

**How do you measure event loop lag accurately in production?**
The correct approach is to use `monitorEventLoopDelay()` from the built-in `node:perf_hooks` module, which uses high-resolution nanosecond timers and returns an `IntervalHistogram` that accumulates samples over time — you call `.enable()` to start sampling, then read `.percentile(99)` to get the p99 in nanoseconds and divide by `1e9` to convert to seconds for Prometheus; using `Date.now()` with `setImmediate` is unreliable because it has only 1ms resolution and the measurement itself adds to the lag being measured.

**Why is frequent major GC a warning sign rather than normal behavior?**
A V8 major GC (MarkSweepCompact) performs a full stop-the-world collection of the old generation heap, which can pause JavaScript execution for 50 to 500 milliseconds depending on heap size; if this happens multiple times per minute, it means objects are being promoted from the young generation to the old generation faster than the collector can reclaim them, which is almost always a symptom of a memory leak or an unbounded accumulation pattern — the correct response is to take a heap snapshot and identify what objects are being retained, not to increase `--max-old-space-size` as a workaround.

## Vocabulário

| Português | English |
|-----------|---------|
| Atraso do loop de eventos | Event loop lag |
| Coleta de lixo | Garbage collection (GC) |
| Heap / pilha de memória | Heap |
| Espaço de pilha | Heap space |
| Handles ativos | Active handles |
| Pressão de memória | Memory pressure |
| Geração jovem | Young generation / new space |
| Geração antiga | Old generation / old space |
| Coleta completa / GC major | Major GC / MarkSweepCompact |
| Coleta rápida / GC minor | Minor GC / Scavenge |
| Uso de heap | Heap usage / heap ratio |
| Esgotamento de memória | Out of memory (OOM) |
| Limite de descritores de arquivo | File descriptor limit |
| Estatísticas de espaço de heap | Heap space statistics |

## Veja também

- [[03-Dominios/Node/Observability e produção/index]] — MOC do galho 5
- [[04 - Métricas com prom-client]] — base de métricas com prom-client
- [[07 - Profiling avançado com clinic.js]] — profiling de CPU e event loop
- [[08 - Detecção e diagnóstico de memory leaks]] — heap snapshots e diagnóstico de memory leaks
- [[03-Dominios/Node/Runtime e Event Loop/index]] — event loop phases e libuv (galho 1)
- [[Node.js]] — tronco

## Fontes

- [Node.js Documentation — `node:perf_hooks` — `monitorEventLoopDelay`](https://nodejs.org/api/perf_hooks.html#perf_hooksmonitoreventloopdelayoptions)
- [prom-client — Default Metrics](https://github.com/siimon/prom-client#default-metrics)
- [V8 — Understanding V8's Garbage Collection](https://v8.dev/blog/trash-talk)
- [Node.js Documentation — `process.memoryUsage()`](https://nodejs.org/api/process.html#processmemoryusage)
- [Node.js Documentation — `v8.getHeapSpaceStatistics()`](https://nodejs.org/api/v8.html#v8getheapspacestatistics)
