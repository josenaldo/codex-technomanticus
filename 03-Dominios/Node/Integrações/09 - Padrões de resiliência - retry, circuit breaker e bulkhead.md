---
title: "Padrões de resiliência - retry, circuit breaker e bulkhead"
created: 2026-05-12
updated: 2026-05-12
type: concept
status: growing
publish: true
tags:
  - node
  - resiliência
  - circuit-breaker
  - integrações
aliases:
  - Retry Node
  - Circuit Breaker Node
  - Resiliência Node
---

# Padrões de resiliência - retry, circuit breaker e bulkhead

> [!abstract] TL;DR
> Três padrões complementares protegem sistemas distribuídos contra falhas em cascata. **Retry com backoff exponencial + jitter** reintenta chamadas falhas com espera crescente e aleatoriedade — o jitter elimina o _thundering herd_, onde centenas de clientes reintentam ao mesmo tempo e derrubam o serviço que estava se recuperando.
>
> **Circuit breaker** implementa uma máquina de estados (closed → open → half-open): após N falhas consecutivas abre o circuito e falha rápido sem chamar o serviço, evitando desperdício de recursos; após um timeout entra em half-open para testar se o serviço voltou.
>
> **Bulkhead** isola domínios de falha com semáforos ou pools de concorrência — se o serviço A sobrecarregar seu slot, o serviço B continua operando normalmente no próprio slot. A biblioteca [`cockatiel`](https://github.com/connor4312/cockatiel) cobre os três padrões e permite compô-los com `Policy.wrap()`; [`opossum`](https://github.com/nodeshift/opossum) é especializado em circuit breaker com uma API orientada a eventos.
>
> Veja [[03-Dominios/Node/Integrações/index|Integrações]] para o contexto completo do galho.

## Como funciona

### Máquina de estados do circuit breaker

O circuit breaker transita entre três estados:

```
CLOSED ──(N falhas consecutivas)──► OPEN
  ▲                                    │
  │                                    │
  │                             (resetTimeout)
  │                                    │
  └──(chamada ok em half-open)── HALF-OPEN
```

- **Closed**: estado normal; todas as chamadas passam. O breaker conta falhas.
- **Open**: o circuito está aberto; chamadas retornam imediatamente com erro (fail-fast) sem tocar o serviço downstream. Um timer (`resetTimeout`) conta o tempo de espera.
- **Half-open**: após o timer expirar, o breaker permite **uma** chamada de teste. Se ela tiver sucesso, volta para closed; se falhar, volta para open e reinicia o timer.

A transição closed → open é disparada quando a porcentagem de falhas em uma janela deslizante ultrapassa `errorThresholdPercentage`. Isso evita que uma única falha esporádica abra o circuito.

### Retry com backoff exponencial e jitter

O retry simples com intervalo fixo é perigoso: se 500 instâncias falharem ao mesmo tempo, todas retentarão no mesmo instante, criando um pico que derruba o serviço novamente (_thundering herd_).

O **backoff exponencial** aumenta o intervalo a cada tentativa: `delay = initialDelay * exponent^attempt`. O **jitter** adiciona aleatoriedade: `delay = random(0, initialDelay * exponent^attempt)`. Isso dispersa as retentativas ao longo do tempo e alivia a pressão sobre o serviço em recuperação.

O `cockatiel` expõe isso via `ExponentialBackoff` com as opções `initialDelay`, `maxDelay` e `exponent`. A condição de retry é configurada com `Policy.handleAll()` (qualquer erro/exceção) ou `Policy.handleWhenResult(fn)` (rejeitar resultados específicos, como status HTTP 503).

### Bulkhead com semáforo de concorrência

O bulkhead (antepara) separa recursos em compartimentos estanques. Implementado como semáforo: só `maxConcurrent` chamadas rodam em paralelo; até `maxQueue` chamadas aguardam na fila; o restante é rejeitado imediatamente com `BulkheadRejectedError`.

Sem bulkhead, um serviço lento pode esgotar todas as threads/event-loop slots disponíveis e derrubar funcionalidades não relacionadas. Com bulkhead, o serviço A tem seu próprio semáforo e o serviço B não é afetado pela lentidão de A.

## Snippets

### Snippet 1 — Retry com `cockatiel`

```typescript
import { retry, ExponentialBackoff, Policy } from 'cockatiel';

// Política de retry: até 5 tentativas com backoff exponencial + jitter
const retryPolicy = retry(Policy.handleAll(), {
  maxAttempts: 5,
  backoff: new ExponentialBackoff({
    initialDelay: 100,   // 100ms na primeira retentativa
    maxDelay: 30_000,    // nunca esperar mais de 30s
    exponent: 2,         // dobra a cada tentativa
  }),
});

// Executa uma chamada HTTP com retry automático
async function fetchWithRetry(url: string): Promise<Response> {
  return retryPolicy.execute(() => fetch(url));
}

// Uso: retry apenas em status 5xx (erros do servidor, não do cliente)
const retryOn5xx = retry(
  Policy.handleWhenResult((res) => res instanceof Response && res.status >= 500),
  { maxAttempts: 3, backoff: new ExponentialBackoff({ initialDelay: 200, maxDelay: 5_000 }) },
);

async function fetchApi(url: string): Promise<Response> {
  const response = await retryOn5xx.execute(() => fetch(url));
  return response;
}
```

### Snippet 2 — Circuit breaker com `opossum`

```typescript
import CircuitBreaker from 'opossum';

// Função que será protegida pelo circuit breaker
async function callPaymentService(orderId: string): Promise<{ status: string }> {
  const res = await fetch(`https://payments.example.com/orders/${orderId}`);
  if (!res.ok) throw new Error(`Payment service error: ${res.status}`);
  return res.json() as Promise<{ status: string }>;
}

const breaker = new CircuitBreaker(callPaymentService, {
  timeout: 3000,                   // 3s para considerar a chamada como falha
  errorThresholdPercentage: 50,    // abre se >= 50% das chamadas falharem
  resetTimeout: 10_000,            // 10s em open antes de tentar half-open
  volumeThreshold: 5,              // mínimo de chamadas para ativar o breaker
});

// Fallback executado quando o circuito está aberto
breaker.fallback((orderId: string) => ({
  status: 'pending',
  message: `Payment service unavailable for order ${orderId}`,
}));

// Monitoramento de estado
breaker.on('open', () => console.warn('[breaker] Payment service circuit OPEN'));
breaker.on('halfOpen', () => console.info('[breaker] Payment service circuit HALF-OPEN'));
breaker.on('close', () => console.info('[breaker] Payment service circuit CLOSED'));

// Chamada protegida
async function processOrder(orderId: string) {
  const result = await breaker.fire(orderId);
  return result;
}
```

### Snippet 3 — Bulkhead com `cockatiel`

```typescript
import { bulkhead, BulkheadRejectedError } from 'cockatiel';

// No máximo 10 chamadas simultâneas; fila de até 20; o resto é rejeitado
const paymentBulkhead = bulkhead(10, 20);
// Sem fila: rejeita imediatamente se já há 5 chamadas ativas
const criticalBulkhead = bulkhead(5, 0);

async function callExternalApi(id: string): Promise<string> {
  return `result-${id}`;
}

async function protectedCall(id: string): Promise<string | null> {
  try {
    // execute() envolve a chamada dentro do semáforo
    return await paymentBulkhead.execute(() => callExternalApi(id));
  } catch (err) {
    if (err instanceof BulkheadRejectedError) {
      console.warn(`[bulkhead] Request rejected for id=${id}: semaphore full`);
      return null;
    }
    throw err;
  }
}

// Demonstração: disparar 35 chamadas; 10 ativas + 20 na fila + 5 rejeitadas
async function demonstrateBulkhead() {
  const results = await Promise.allSettled(
    Array.from({ length: 35 }, (_, i) => protectedCall(String(i))),
  );
  const rejected = results.filter((r) => r.status === 'fulfilled' && r.value === null).length;
  console.info(`Rejected by bulkhead: ${rejected}`);
}

demonstrateBulkhead().catch(console.error);
```

### Snippet 4 — Composição de políticas com `cockatiel`

```typescript
import { retry, circuitBreaker, ConsecutiveBreaker, ExponentialBackoff, bulkhead, Policy } from 'cockatiel';

// 1. Retry: 4 tentativas com backoff exponencial
const retryPolicy = retry(Policy.handleAll(), {
  maxAttempts: 4,
  backoff: new ExponentialBackoff({ initialDelay: 150, maxDelay: 10_000 }),
});

// 2. Circuit breaker: abre após 3 falhas em 30s, aguarda 15s antes de half-open
const cbPolicy = circuitBreaker(Policy.handleAll(), {
  halfOpenAfter: 15_000,
  breaker: new ConsecutiveBreaker(3),
});

// 3. Bulkhead: 8 slots paralelos, fila de 16
const bhPolicy = bulkhead(8, 16);

// Composição: wrap aplica as políticas de fora para dentro
// ordem de execução: retry → circuitBreaker → bulkhead → chamada real
// retry é o mais externo porque deve envolver o circuitBreaker
const resilientPolicy = Policy.wrap(retryPolicy, cbPolicy, bhPolicy);

async function fetchData(endpoint: string): Promise<unknown> {
  const response = await resilientPolicy.execute(async () => {
    const res = await fetch(endpoint);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
  });
  return response;
}

// Uso em produção
async function getUser(userId: string) {
  return fetchData(`https://api.example.com/users/${userId}`);
}
```

### Snippet 5 — Timeout com `AbortController`

```typescript
import { retry, ExponentialBackoff, Policy } from 'cockatiel';

// Timeout como política independente: cancela a chamada após N milissegundos
// Funciona com fetch, grpc, qualquer API que aceite AbortSignal

// Abordagem 1: AbortSignal.timeout (Node 18+, mais limpo)
async function fetchWithNativeTimeout(url: string, timeoutMs = 5000): Promise<unknown> {
  const signal = AbortSignal.timeout(timeoutMs);
  const res = await fetch(url, { signal });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

// Abordagem 2: AbortController manual (compatível com Node 16+)
async function fetchWithManualTimeout(url: string, timeoutMs = 5000): Promise<unknown> {
  const controller = new AbortController();
  const timerId = setTimeout(() => controller.abort(new Error(`Timeout after ${timeoutMs}ms`)), timeoutMs);

  try {
    const res = await fetch(url, { signal: controller.signal });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
  } finally {
    clearTimeout(timerId); // sempre limpa o timer para evitar memory leak
  }
}

// Composição: timeout + retry via cockatiel
const retryWithTimeout = retry(Policy.handleAll(), {
  maxAttempts: 3,
  backoff: new ExponentialBackoff({ initialDelay: 100, maxDelay: 3000 }),
});

async function resilientFetch(url: string): Promise<unknown> {
  return retryWithTimeout.execute(() => fetchWithNativeTimeout(url, 4000));
}
```

## Armadilhas

> [!danger] Retry sem jitter causa thundering herd
> Se todas as instâncias do serviço falharem ao mesmo tempo (ex: restart de um serviço downstream), o backoff exponencial sem jitter fará **todas** retentarem no exato mesmo instante. Resultado: pico de carga imediato que derruba o serviço que estava se recuperando. Use sempre `jitter: true` ou uma implementação manual com `Math.random()`.

> [!danger] Retry em operações não idempotentes causa duplicação de dados
> Nunca faça retry automático em `POST` sem um **idempotency key**. Se a requisição chegou ao servidor mas a resposta foi perdida na rede, o retry criará um segundo registro (pedido duplicado, cobrança duplicada). Use retry apenas em operações idempotentes (`GET`, `PUT`) ou em `POST` que aceitem `Idempotency-Key` no header.

> [!warning] Circuit breaker sem half-open nunca se recupera
> Um circuit breaker que só transita entre closed e open fica preso em open para sempre após um surto de falhas. O estado half-open é obrigatório: ele permite uma chamada de sonda após o `resetTimeout` para verificar se o serviço se recuperou. Certifique-se de configurar `resetTimeout` com um valor razoável (10–60s dependendo do SLA do serviço).

> [!warning] Bulkhead sem `maxQueue` deixa a fila crescer sem limite
> `bulkhead(10)` sem segundo argumento pode acumular milhares de requisições na fila se o serviço ficar lento, consumindo memória indefinidamente. Sempre defina `maxQueue` explicitamente. Para cenários de real-time onde requisições velhas são inúteis, use `bulkhead(N, 0)` para rejeitar imediatamente qualquer requisição além da capacidade ativa.

> [!warning] Não monitorar o estado do circuit breaker é falha silenciosa
> Um circuit breaker aberto retorna respostas degradadas (fallback) sem lançar exceção. Se você não monitora o evento `'open'`, pode ter o sistema operando em modo degradado por horas sem alertas. Registre logs/métricas nos eventos `open`, `halfOpen` e `close`. Integre com seu APM (Datadog, New Relic, OpenTelemetry) para criar alertas quando o circuito abrir.

## Comparação: cockatiel vs opossum vs implementação manual

| Critério | `cockatiel` | `opossum` | Implementação manual |
|---|---|---|---|
| Retry com backoff | Nativo (`ExponentialBackoff`) | Não tem | Trabalhoso e propenso a bug |
| Circuit breaker | Nativo (`circuitBreaker`) | Especialidade principal | Muito complexo de fazer certo |
| Bulkhead/semáforo | Nativo (`bulkhead`) | Não tem | Simples com `p-limit` |
| Composição de políticas | `Policy.wrap()` elegante | Não tem | Manual e frágil |
| Monitoramento/eventos | Eventos por política | Eventos ricos no CB | Você implementa tudo |
| Tamanho do bundle | ~15 KB | ~12 KB | 0 KB |
| API | Standalone functions + `Policy.wrap()` | Orientada a eventos | Qualquer coisa |
| Typescript | Excelente suporte | Tipos incluídos | Você define |
| Melhor para | Composição de múltiplas políticas | Somente circuit breaker robusto | Aprender ou caso muito específico |

## Em entrevista

**Q: What is the difference between a retry and a circuit breaker? When should you use each?**

Retry and circuit breaker are complementary patterns that operate at different timescales. Retry handles transient failures — short-lived issues like a brief network hiccup, a pod restart, or an occasional timeout — by re-executing the call after a delay. Circuit breaker handles sustained failures — when a downstream service is down for an extended period — by stopping all calls immediately rather than letting each one timeout.

The key insight is that retry alone is dangerous without a circuit breaker: if the downstream service is down for 5 minutes and you have 1000 requests per second, each retrying 3 times with a 2s delay, you'll generate an enormous load of failed requests that wastes threads, connections, and memory. The circuit breaker acts as a fuse: after N failures, it opens and all subsequent calls fail fast (microseconds instead of seconds), preserving system resources. Once the service recovers, the half-open state allows a probe request to confirm recovery before resuming normal traffic.

**Q: How does the bulkhead pattern isolate failures? Can you give a concrete example?**

Bulkhead is named after the watertight compartments in a ship's hull — if one compartment floods, the others remain dry and the ship stays afloat. In software, it means allocating separate resource pools (thread pools, connection pools, or semaphores) to different dependencies so that one misbehaving dependency cannot exhaust the shared pool and bring down unrelated functionality.

Consider a Node.js API that calls three services: User Service, Payment Service, and Notification Service. Without bulkhead, if Payment Service becomes slow (10s response time), concurrent requests accumulate in the event loop. With enough load, all available concurrency slots are occupied waiting for payment responses, and even fast requests to User Service start timing out. With bulkhead, Payment Service gets its own semaphore of 10 concurrent slots — when those are full, excess requests are rejected immediately with a clear error, while User Service and Notification Service continue operating normally with their own semaphores. The failure is contained to the payment domain.

**Q: Why is jitter essential in exponential backoff? What happens without it?**

Without jitter, exponential backoff creates a phenomenon called the thundering herd problem. Imagine 500 client instances all receive errors at the same time — a common scenario during a service restart or brief outage. All 500 clients schedule their first retry at exactly `initialDelay` milliseconds. This synchronized retry wave hits the recovering service all at once, potentially overwhelming it before it finishes starting up, causing another wave of failures and retries.

Jitter breaks this synchronization by randomizing each client's wait time. With full jitter, the delay becomes `random(0, initialDelay * 2^attempt)`, spreading retries across the entire backoff window. With 500 clients and a 1-second backoff window, retries arrive roughly uniformly at about 500/1000ms = 0.5 requests per millisecond — a gentle ramp that gives the service time to recover. AWS Engineering's 2015 blog post "Exponential Backoff And Jitter" demonstrated empirically that full jitter dramatically reduces both total wait time and load on the recovering service compared to fixed or unjittered backoff.

**Q: What is the correct order to compose retry, circuit breaker, and bulkhead? Why does order matter?**

The correct execution order from inside out is: **bulkhead → circuit breaker → retry**. In `cockatiel`'s `Policy.wrap()`, the outermost policy (first argument) wraps all others, so the call is: `Policy.wrap(retry, circuitBreaker, bulkhead)`.

Order matters because each policy has a different responsibility boundary. The bulkhead should be innermost (closest to the actual call) because it limits concurrent executions of the real operation — we want the bulkhead to count only actual in-flight requests, not retries-in-progress waiting at the circuit breaker. The circuit breaker wraps the bulkhead: when the circuit is open, it short-circuits before even acquiring a bulkhead slot, which is correct behavior. Retry is outermost because it needs to re-execute the entire pipeline (check circuit breaker state, acquire semaphore, make the call) on each attempt. If retry were inside the circuit breaker, a failed call would retry without checking whether the circuit has opened after the first failure, defeating the purpose of the circuit breaker entirely.

## Vocabulário

| Termo | Definição |
|---|---|
| **retry** | Padrão que reexecuta uma operação falha após um intervalo de espera, com limite de tentativas configurável |
| **exponential backoff** | Estratégia de espera onde o intervalo cresce exponencialmente a cada tentativa: `delay = base * exponent^attempt` |
| **jitter** | Aleatoriedade adicionada ao backoff para dessincronizar retentativas de múltiplos clientes e evitar o thundering herd |
| **thundering herd** | Pico de carga causado por múltiplos clientes retentando simultaneamente, potencialmente derrubando o serviço em recuperação |
| **circuit breaker** | Padrão que monitora falhas e abre o circuito (fail-fast) quando a taxa de falhas excede um threshold, protegendo o serviço downstream |
| **closed state** | Estado normal do circuit breaker; todas as chamadas passam; falhas são contadas |
| **open state** | Estado de falha do circuit breaker; chamadas retornam erro imediatamente sem tocar o serviço downstream |
| **half-open state** | Estado de sonda do circuit breaker; uma chamada de teste é permitida para verificar se o serviço se recuperou |
| **fallback** | Resposta alternativa executada quando o circuito está aberto ou quando todas as tentativas de retry falharam |
| **bulkhead** | Padrão que isola recursos em compartimentos separados (semáforos/pools), evitando que a falha de um serviço afete outros |
| **semaphore** | Primitiva de controle de concorrência que limita o número de execuções simultâneas de uma operação |
| **concurrency limit** | Número máximo de chamadas paralelas permitidas por um bulkhead antes de começar a enfileirar ou rejeitar requisições |
| **idempotent** | Operação que produz o mesmo resultado independente de quantas vezes é executada — segura para retry automático |
| **resetTimeout** | Tempo que o circuit breaker permanece em estado open antes de transitar para half-open e tentar recuperação |
| **errorThresholdPercentage** | Porcentagem de falhas em uma janela de tempo que dispara a abertura do circuit breaker |
