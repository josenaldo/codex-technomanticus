---
title: "10 - Circuit breaker e fallback com opossum"
tags:
  - node
  - observability
  - resilience
  - circuit-breaker
  - opossum
type: note
status: growing
progresso: andamento
created: 2026-05-09
updated: 2026-05-09
publish: true
---

# Circuit breaker e fallback com opossum

> [!abstract] TL;DR
> - **Circuit breaker** é um pattern de resiliência que protege um serviço de falhas em cascata: em vez de deixar todas as chamadas falharem lentamente (e sobrecarregar o downstream), o circuito "abre" e rejeita requisições imediatamente quando a taxa de erro ultrapassa um threshold.
> - O circuito tem três estados: **CLOSED** (normal — requisições passam), **OPEN** (falha rápida — requisições são rejeitadas sem chamar a função) e **HALF_OPEN** (tentativa de recuperação — uma requisição-sonda passa; se sucede, fecha; se falha, abre de novo).
> - **opossum** é a biblioteca padrão de circuit breaker no ecossistema Node.js; envolve qualquer função assíncrona com `new CircuitBreaker(fn, options)` e expõe eventos para logging e métricas.
> - **Fallback** (`breaker.fallback(fn)`) define o que retornar quando o circuito está OPEN ou quando a requisição falha — normalmente dados em cache, lista vazia ou valor padrão degradado; nunca deve lançar exceção.
> - Integração com **prom-client** via `opossum-prometheus` expõe contadores e histogramas prontos para Prometheus sem código manual.
> - Armadilha comum: `timeout` em opossum é o tempo máximo de execução da função (em ms), **não** o tempo que o circuito fica OPEN — esse é `resetTimeout`.

O circuit breaker é um dos patterns de resiliência mais importantes em arquiteturas de microsserviços. Sem ele, um serviço downstream lento ou indisponível pode saturar a thread pool do chamador com requisições pendentes, esgotar o connection pool do banco, e derrubar em cascata serviços que estavam funcionando. Com ele, o sistema degrada de forma controlada: o cliente recebe uma resposta degradada (mas rápida) e o downstream tem espaço para se recuperar. Este galho cobre o pattern do zero e sua implementação em Node.js com opossum.

## O que é

O **circuit breaker** (disjuntor) é um pattern de resiliência que envolve uma chamada potencialmente instável (HTTP externo, banco de dados, fila) e monitora sua taxa de falha. Quando a taxa ultrapassa um limite configurado, o circuito "abre" e passa a rejeitar requisições **imediatamente**, sem tentar chamar o serviço downstream — assim como um disjuntor elétrico que desliga o circuito ao detectar sobrecarga, protegendo os demais componentes.

A analogia com o disjuntor elétrico é precisa: o disjuntor doméstico não sabe por que há sobrecarga — só sabe que a corrente ultrapassou o limite seguro. Ele desliga o circuito para proteger a fiação e os aparelhos. Para religar, você vai ao quadro elétrico e testa manualmente. O circuit breaker de software funciona da mesma forma: após um tempo de espera (`resetTimeout`), ele entra num estado de "meia abertura" e testa se o serviço downstream se recuperou antes de voltar ao normal.

### Por que não é apenas um timeout ou retry

Timeouts evitam que uma única chamada fique pendente para sempre, mas não evitam que centenas de chamadas simultâneas fiquem esperando o timeout. Retries com backoff ajudam para falhas transitórias, mas amplificam a carga num serviço já sobrecarregado. O circuit breaker complementa ambos: **fail fast** quando o padrão de falha já está estabelecido, dando ao downstream tempo de respirar.

### Falhas em cascata

Sem circuit breaker, a sequência típica de falha em cascata é:

1. Serviço B (downstream) fica lento ou indisponível.
2. Serviço A (chamador) acumula requisições esperando resposta de B.
3. Threads/conexões de A se esgotam.
4. A começa a falhar para seus clientes.
5. Serviço C, que depende de A, também começa a falhar.
6. Todo o sistema entra em degradação total — por causa de uma falha pontual em B.

O circuit breaker interrompe o ciclo no passo 2: quando B está com alta taxa de erro, A falha rápido, libera recursos, e o impacto não se propaga.

## Como funciona

### Estados do circuito

O circuit breaker opera como uma máquina de estados com três estados bem definidos:

```
CLOSED → (errorThreshold exceeded) → OPEN
OPEN → (resetTimeout elapsed) → HALF_OPEN
HALF_OPEN → (probe succeeds) → CLOSED
HALF_OPEN → (probe fails) → OPEN
```

**CLOSED — estado normal**

O circuito está fechado: as requisições passam normalmente pela função protegida. O circuit breaker monitora cada chamada e contabiliza sucessos e falhas dentro de uma janela de tempo. Enquanto a taxa de falha permanecer abaixo do `errorThresholdPercentage`, o circuito fica CLOSED. Este é o estado padrão — o circuit breaker é transparente para o fluxo normal da aplicação.

**OPEN — falha rápida**

Quando a taxa de erro supera o threshold, o circuito abre. Em estado OPEN, as requisições **não chegam à função protegida**: o circuit breaker rejeita imediatamente com um erro do tipo `OpenCircuitError` (ou chama o fallback, se configurado). Isso acontece sem latência de rede, sem consumo de thread pool, sem impacto no downstream. O circuito permanece OPEN por `resetTimeout` milissegundos.

**HALF_OPEN — sonda de recuperação**

Após `resetTimeout` expirar, o circuito entra em HALF_OPEN. Uma única requisição-sonda é deixada passar. Se ela for bem-sucedida, o circuito retorna ao estado CLOSED e o tráfego normal é restaurado. Se ela falhar, o circuito volta imediatamente para OPEN e o timer `resetTimeout` recomeça. HALF_OPEN implementa um mecanismo de auto-healing sem expor o downstream a uma enxurrada de requisições assim que ele volta a responder.

### opossum

**opossum** é o pacote npm de referência para circuit breaker em Node.js. Ele envolve qualquer função assíncrona (que retorne `Promise`) e expõe a máquina de estados descrita acima com configuração declarativa.

Instalação:

```bash
npm install opossum
# TypeScript types incluídos no pacote
```

Uso básico:

```typescript
import CircuitBreaker from 'opossum';

async function fetchUser(userId: string): Promise<User> {
  const response = await fetch(`https://user-service/users/${userId}`);
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }
  return response.json();
}

const options = {
  timeout: 3000,                  // Função deve completar em 3s ou recebe timeout
  errorThresholdPercentage: 50,   // Abre se > 50% das requisições falharem
  resetTimeout: 30_000,           // Após 30s em OPEN, tenta HALF_OPEN
};

const breaker = new CircuitBreaker(fetchUser, options);

// Dispara a função protegida
const user = await breaker.fire('user-123');
```

**Opções principais:**

| Opção | Tipo | Padrão | Descrição |
|---|---|---|---|
| `timeout` | `number` | `10000` | Tempo máximo (ms) de execução da função antes de gerar erro de timeout |
| `errorThresholdPercentage` | `number` | `50` | % de erros para abrir o circuito |
| `resetTimeout` | `number` | `30000` | Tempo (ms) em OPEN antes de tentar HALF_OPEN |
| `volumeThreshold` | `number` | `0` | Nº mínimo de requisições antes de começar a avaliar o threshold |
| `rollingCountTimeout` | `number` | `10000` | Tamanho da janela deslizante (ms) para contagem de erros |
| `rollingCountBuckets` | `number` | `10` | Nº de buckets na janela deslizante |
| `enabled` | `boolean` | `true` | Desabilita o circuit breaker sem remover o código (útil em testes) |

> [!tip] volumeThreshold
> Por padrão, `volumeThreshold: 0` significa que **uma única falha** pode abrir o circuito se a taxa de erro for 100%. Em produção, configure `volumeThreshold: 10` ou similar para evitar que um spike isolado trip o circuito antes de haver amostragem suficiente.

### Fallback

O fallback é a resposta alternativa retornada quando o circuito está OPEN ou quando a requisição protegida falha. Configure com `breaker.fallback(fn)`:

```typescript
// O fallback recebe os mesmos argumentos da função original
breaker.fallback((userId: string) => ({
  id: userId,
  name: 'Unknown',
  email: null,
  fromCache: true,
}));

// A partir daqui, breaker.fire('user-123') nunca rejeita:
// - Em CLOSED: chama fetchUser normalmente
// - Em OPEN: retorna o objeto degradado imediatamente
// - Se fetchUser rejeitar: retorna o objeto degradado
```

**Boas práticas para fallbacks:**

- **Nunca lance exceção no fallback.** Se o fallback falhar, o caller recebe um erro — o circuit breaker não captura erros do fallback.
- **Prefira dados em cache** a valores inventados quando possível. Um cache Redis com TTL longo serve como fallback natural para dados de referência.
- **Documente o contrato degradado.** O caller precisa saber que `fromCache: true` significa que o dado pode estar desatualizado.
- **Fallback não redefine o estado do circuito.** O circuito continua OPEN enquanto o fallback responde — o caller recebe dados, mas o downstream ainda está sendo poupado.

Exemplo com cache Redis como fallback:

```typescript
import CircuitBreaker from 'opossum';
import { redisClient } from './redis';

const breaker = new CircuitBreaker(fetchUser, {
  timeout: 3000,
  errorThresholdPercentage: 50,
  resetTimeout: 30_000,
});

breaker.fallback(async (userId: string) => {
  // Tenta o cache antes de retornar dado vazio
  const cached = await redisClient.get(`user:${userId}`);
  if (cached) {
    return { ...JSON.parse(cached), fromCache: true };
  }
  // Dado vazio como último recurso — nunca lança
  return { id: userId, name: 'Unknown', fromCache: true };
});
```

### Eventos

opossum emite eventos para cada transição de estado e para cada resultado de chamada. Use-os para logging, métricas e alertas:

```typescript
// Transições de estado
breaker.on('open', () => {
  logger.warn({ circuit: 'user-service' }, 'Circuit breaker OPEN');
});

breaker.on('close', () => {
  logger.info({ circuit: 'user-service' }, 'Circuit breaker CLOSED');
});

breaker.on('halfOpen', () => {
  logger.info({ circuit: 'user-service' }, 'Circuit breaker HALF_OPEN — probe request');
});

// Resultado de cada chamada
breaker.on('success', (result, latencyMs) => {
  logger.debug({ latencyMs }, 'Circuit breaker call succeeded');
});

breaker.on('failure', (error, latencyMs) => {
  logger.error({ err: error, latencyMs }, 'Circuit breaker call failed');
});

breaker.on('timeout', () => {
  logger.warn({ circuit: 'user-service' }, 'Circuit breaker timeout');
});

breaker.on('reject', () => {
  // Chamada rejeitada porque o circuito está OPEN
  logger.debug({ circuit: 'user-service' }, 'Circuit breaker rejected (OPEN)');
});

breaker.on('fallback', (result) => {
  logger.info({ result }, 'Circuit breaker using fallback');
});
```

**Lista completa de eventos:**

| Evento | Quando | Parâmetros |
|---|---|---|
| `success` | Função concluiu com sucesso | `result, latencyMs` |
| `failure` | Função rejeitou ou lançou exceção | `error, latencyMs` |
| `timeout` | Função excedeu `timeout` ms | — |
| `reject` | Circuito OPEN, chamada rejeitada sem executar | — |
| `open` | Circuito transitou para OPEN | — |
| `close` | Circuito transitou para CLOSED | — |
| `halfOpen` | Circuito transitou para HALF_OPEN | — |
| `fallback` | Fallback foi acionado | `result` |
| `fire` | `breaker.fire()` foi chamado | `args` |
| `cacheHit` | Resultado veio do cache interno (se habilitado) | `result` |

### Métricas com prom-client

A forma mais rápida de expor métricas de circuit breaker para Prometheus é com o pacote `opossum-prometheus`:

```typescript
import CircuitBreaker from 'opossum';
import { PrometheusMetrics } from 'opossum-prometheus';

const breaker = new CircuitBreaker(fetchUser, { timeout: 3000, errorThresholdPercentage: 50, resetTimeout: 30_000 });

// Registra automaticamente no default registry do prom-client
const metrics = new PrometheusMetrics({ circuits: [breaker] });

// Métricas expostas automaticamente:
// opossum_circuit_open{name="fetchUser"}
// opossum_circuit_half_open{name="fetchUser"}
// opossum_circuit_closed{name="fetchUser"}
// opossum_successful{name="fetchUser"}
// opossum_failed{name="fetchUser"}
// opossum_rejected{name="fetchUser"}
// opossum_timeout{name="fetchUser"}
// opossum_fallback{name="fetchUser"}
// opossum_latency_mean{name="fetchUser"}
// opossum_latency_bucket{name="fetchUser"}
```

Para customizar o nome da métrica (útil quando há vários breakers):

```typescript
const breaker = new CircuitBreaker(fetchUser, {
  name: 'user-service',   // Usado como label `name` nas métricas
  timeout: 3000,
  errorThresholdPercentage: 50,
  resetTimeout: 30_000,
});
```

Se preferir métricas manuais com prom-client puro (mais controle):

```typescript
import { Counter, Histogram } from 'prom-client';

const cbStateGauge = new Counter({
  name: 'circuit_breaker_state_transitions_total',
  help: 'Total de transições de estado do circuit breaker',
  labelNames: ['circuit', 'from_state', 'to_state'],
});

const cbCallsTotal = new Counter({
  name: 'circuit_breaker_calls_total',
  help: 'Total de chamadas ao circuit breaker',
  labelNames: ['circuit', 'outcome'], // outcome: success | failure | timeout | reject | fallback
});

const cbLatency = new Histogram({
  name: 'circuit_breaker_call_duration_seconds',
  help: 'Latência das chamadas protegidas pelo circuit breaker',
  labelNames: ['circuit', 'outcome'],
  buckets: [0.05, 0.1, 0.25, 0.5, 1, 2.5, 5],
});

breaker.on('open', () => {
  cbStateGauge.inc({ circuit: 'user-service', from_state: 'closed', to_state: 'open' });
});
breaker.on('close', () => {
  cbStateGauge.inc({ circuit: 'user-service', from_state: 'open', to_state: 'closed' });
});
breaker.on('success', (_, latencyMs) => {
  cbCallsTotal.inc({ circuit: 'user-service', outcome: 'success' });
  cbLatency.observe({ circuit: 'user-service', outcome: 'success' }, latencyMs / 1000);
});
breaker.on('failure', (_, latencyMs) => {
  cbCallsTotal.inc({ circuit: 'user-service', outcome: 'failure' });
  cbLatency.observe({ circuit: 'user-service', outcome: 'failure' }, latencyMs / 1000);
});
breaker.on('reject', () => {
  cbCallsTotal.inc({ circuit: 'user-service', outcome: 'reject' });
});
breaker.on('fallback', () => {
  cbCallsTotal.inc({ circuit: 'user-service', outcome: 'fallback' });
});
```

## Na prática

### Setup básico envolving uma chamada HTTP

```typescript
import CircuitBreaker from 'opossum';

interface User {
  id: string;
  name: string;
  email: string;
}

// Função pura que faz a chamada — sem nenhum conhecimento de circuit breaker
async function fetchUser(userId: string): Promise<User> {
  const response = await fetch(`https://user-service.internal/users/${userId}`, {
    headers: { 'Content-Type': 'application/json' },
  });

  if (!response.ok) {
    throw new Error(`user-service responded with ${response.status}`);
  }

  return response.json() as Promise<User>;
}

// Circuit breaker envolve a função
const userBreaker = new CircuitBreaker(fetchUser, {
  name: 'user-service',
  timeout: 3000,                  // 3s: tempo máximo de execução da função
  errorThresholdPercentage: 50,   // Abre se > 50% de erros na janela
  resetTimeout: 30_000,           // Tenta recuperar após 30s
  volumeThreshold: 5,             // Precisa de ao menos 5 chamadas para avaliar
  rollingCountTimeout: 10_000,    // Janela de 10s para contagem
});

// Uso — idêntico à chamada direta, mas protegido
async function getUser(userId: string): Promise<User> {
  return userBreaker.fire(userId);
}
```

### Com fallback retornando dado cacheado

```typescript
import CircuitBreaker from 'opossum';
import NodeCache from 'node-cache';

const cache = new NodeCache({ stdTTL: 300 }); // cache de 5 minutos

async function fetchUser(userId: string): Promise<User> {
  const response = await fetch(`https://user-service.internal/users/${userId}`);
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  const user = await response.json() as User;

  // Popula o cache no caminho feliz
  cache.set(`user:${userId}`, user);
  return user;
}

const userBreaker = new CircuitBreaker(fetchUser, {
  name: 'user-service',
  timeout: 3000,
  errorThresholdPercentage: 50,
  resetTimeout: 30_000,
  volumeThreshold: 5,
});

// Fallback: tenta cache, depois retorna esqueleto degradado
userBreaker.fallback((userId: string): User => {
  const cached = cache.get<User>(`user:${userId}`);
  if (cached) {
    return cached; // dado do cache — pode estar um pouco desatualizado
  }
  // Último recurso: resposta degradada mínima
  return {
    id: userId,
    name: 'Unknown',
    email: '',
  };
});
```

### Event listeners para logging e métricas

```typescript
import CircuitBreaker from 'opossum';
import { PrometheusMetrics } from 'opossum-prometheus';
import pino from 'pino';

const logger = pino({ name: 'circuit-breaker' });

const userBreaker = new CircuitBreaker(fetchUser, {
  name: 'user-service',
  timeout: 3000,
  errorThresholdPercentage: 50,
  resetTimeout: 30_000,
});

// Métricas automáticas via opossum-prometheus
const _metrics = new PrometheusMetrics({ circuits: [userBreaker] });

// Logging das transições de estado (crítico para alertas)
userBreaker.on('open', () => {
  logger.warn({ circuit: 'user-service' }, 'Circuit breaker OPEN — rejecting calls');
});

userBreaker.on('close', () => {
  logger.info({ circuit: 'user-service' }, 'Circuit breaker CLOSED — service recovered');
});

userBreaker.on('halfOpen', () => {
  logger.info({ circuit: 'user-service' }, 'Circuit breaker HALF_OPEN — sending probe request');
});

// Logging detalhado de cada chamada (pode ser verbose em produção — ajuste o level)
userBreaker.on('success', (_result, latencyMs) => {
  logger.debug({ latencyMs, circuit: 'user-service' }, 'call succeeded');
});

userBreaker.on('failure', (error, latencyMs) => {
  logger.warn({ err: error, latencyMs, circuit: 'user-service' }, 'call failed');
});

userBreaker.on('timeout', () => {
  logger.warn({ circuit: 'user-service' }, 'call timed out');
});

userBreaker.on('reject', () => {
  logger.debug({ circuit: 'user-service' }, 'call rejected — circuit is OPEN');
});

userBreaker.on('fallback', (result) => {
  logger.info({ result, circuit: 'user-service' }, 'fallback response delivered');
});
```

### Testando o circuit breaker

opossum expõe métodos para controle manual de estado — essenciais para testes determinísticos:

```typescript
import CircuitBreaker from 'opossum';
import { describe, it, expect, vi } from 'vitest';

describe('userBreaker', () => {
  const mockFetch = vi.fn();
  let breaker: CircuitBreaker<[string], User>;

  beforeEach(() => {
    mockFetch.mockReset();
    breaker = new CircuitBreaker(mockFetch, {
      timeout: 1000,
      errorThresholdPercentage: 50,
      resetTimeout: 5000,
      volumeThreshold: 2,
    });

    // Fallback simples para testes
    breaker.fallback((userId: string) => ({ id: userId, name: 'fallback', email: '' }));
  });

  it('retorna resultado quando o serviço responde', async () => {
    mockFetch.mockResolvedValue({ id: '1', name: 'Alice', email: 'alice@example.com' });
    const result = await breaker.fire('1');
    expect(result.name).toBe('Alice');
  });

  it('usa fallback quando o circuito está OPEN', async () => {
    // Força o circuito para OPEN sem precisar simular falhas
    breaker.open();
    expect(breaker.opened).toBe(true);

    const result = await breaker.fire('1');
    expect(result.name).toBe('fallback');
  });

  it('chama a função após fechar o circuito', async () => {
    mockFetch.mockResolvedValue({ id: '1', name: 'Alice', email: '' });

    breaker.open();
    breaker.close(); // Força CLOSED

    const result = await breaker.fire('1');
    expect(mockFetch).toHaveBeenCalledWith('1');
    expect(result.name).toBe('Alice');
  });

  it('registra evento de fallback quando OPEN', async () => {
    const fallbackSpy = vi.fn();
    breaker.on('fallback', fallbackSpy);

    breaker.open();
    await breaker.fire('1');

    expect(fallbackSpy).toHaveBeenCalled();
  });

  afterEach(() => {
    breaker.shutdown(); // Limpa timers internos
  });
});
```

> [!important] breaker.shutdown()
> Sempre chame `breaker.shutdown()` no `afterEach`/`afterAll` de testes. opossum mantém timers internos para `resetTimeout` e para a janela deslizante — sem `shutdown()`, os timers vazam entre testes e podem causar comportamentos não-determinísticos.

## Em entrevista

**What is a circuit breaker pattern?**

A circuit breaker is a resilience pattern that wraps a potentially failing remote call — typically an HTTP request, database query, or message broker operation — and monitors its error rate. When the error rate exceeds a configured threshold (say, 50% of calls in a 10-second window), the circuit "opens" and starts rejecting new calls immediately, without actually invoking the downstream service. This prevents cascading failures: instead of saturating the thread pool with pending requests to an unavailable service, the system fails fast and preserves resources for calls that can succeed.

**What are the three states?**

The circuit breaker operates as a state machine with three states. **CLOSED** is the normal operating state: requests flow through to the protected function, and the breaker monitors results. **OPEN** is the failing-fast state: the downstream showed high error rates, so the breaker short-circuits all calls and either rejects them or invokes the fallback function. No network call is made, so there is no latency cost. **HALF_OPEN** is the recovery probe state: after a configured time (`resetTimeout`), the breaker lets a single probe request through. If that request succeeds, the circuit transitions back to CLOSED and normal traffic resumes. If it fails, the circuit returns to OPEN and the timer resets. HALF_OPEN is what makes the circuit breaker self-healing — it automatically discovers when the downstream has recovered.

**How does opossum implement this in Node.js?**

opossum wraps any async function with `new CircuitBreaker(fn, options)`. You configure `timeout` (max execution time in ms), `errorThresholdPercentage` (the failure rate that trips the circuit), and `resetTimeout` (time spent in OPEN before probing). You call `breaker.fire(...args)` instead of calling the function directly. opossum emits named events — `open`, `close`, `halfOpen`, `success`, `failure`, `fallback`, `reject` — which you use to wire in logging and Prometheus metrics. The `breaker.fallback(fn)` method registers a function that receives the same arguments as the original and returns a degraded response; opossum calls it automatically when the circuit is OPEN or when a call fails.

## Vocabulário

| Termo | Definição |
|---|---|
| **circuit breaker** | Pattern de resiliência que interrompe chamadas a um serviço com alta taxa de falha para evitar falhas em cascata |
| **CLOSED state** | Estado normal do circuit breaker — requisições passam para a função protegida |
| **OPEN state** | Estado de falha rápida — requisições são rejeitadas sem chamar a função; downstream é poupado |
| **HALF_OPEN state** | Estado de recuperação — uma requisição-sonda passa; sucesso fecha, falha reabre o circuito |
| **fallback** | Função alternativa chamada quando o circuito está OPEN ou a chamada falha; deve retornar resposta degradada sem lançar exceção |
| **error threshold** | Percentual de erros (dentro da janela deslizante) que dispara a abertura do circuito (`errorThresholdPercentage`) |
| **reset timeout** | Tempo (ms) que o circuito permanece em OPEN antes de tentar HALF_OPEN (`resetTimeout`) |
| **cascading failure** | Falha em cascata — uma falha num serviço downstream se propaga e derruba serviços upstream que dependem dele |
| **bulkhead** | Pattern complementar ao circuit breaker: isola recursos (thread pools, connection pools) por serviço para que a falha num não afete os outros |
| **fail fast** | Princípio de rejeitar a chamada imediatamente (sem esperar timeout) quando se sabe que ela vai falhar |
| **probe request** | Requisição-sonda enviada em HALF_OPEN para testar se o downstream se recuperou |
| **volumeThreshold** | Número mínimo de chamadas necessárias na janela antes de o opossum avaliar o `errorThresholdPercentage` |

## Armadilhas

> [!warning] `timeout` vs `resetTimeout` — nomes enganosos
> A opção `timeout` em opossum é o **tempo máximo de execução da função protegida** (em ms). Se a função não resolver/rejeitar em `timeout` ms, o opossum a considera falha e emite o evento `timeout`. Isso é completamente diferente de `resetTimeout`, que é o tempo que o circuito permanece em OPEN antes de tentar HALF_OPEN. Confundir os dois leva a configurações onde o circuito fica OPEN por 3 segundos (em vez de 30) ou a função tem 30 segundos para responder (em vez de 3).

> [!warning] `errorThresholdPercentage` baixo demais trip em picos normais
> Um threshold de 10% significa que 1 falha em cada 10 chamadas abre o circuito. Em serviços com tráfego baixo ou com variância natural (rede, GC pause), isso pode abrir o circuito durante picos completamente normais. Calibre o threshold com base no seu SLO: se o SLO de disponibilidade do downstream é 99%, o threshold deveria ser algo como 30–50%, não 10%. Use `volumeThreshold` para garantir que há amostragem suficiente antes de avaliar.

> [!warning] Fallback que lança exceção vira erro invisível
> O opossum não captura erros lançados dentro do fallback. Se o fallback jogar uma exceção (ex: falha no Redis ao buscar dado cacheado), o erro vai se propagar para o caller sem passar pelos event listeners de `failure`. O caller recebe um erro que parece ter vindo do fallback, não do serviço protegido — difícil de debugar. Sempre envolva o fallback em `try/catch` interno e retorne um valor degradado como último recurso.

> [!warning] Wrapping de funções síncronas ou que nunca rejeitam
> O circuit breaker foi projetado para funções assíncronas que podem rejeitar. Envolver uma função síncrona ou uma que trata todos os erros internamente e nunca rejeita (retornando `null` em vez de lançar) faz com que o breaker nunca contabilize falhas — o circuito nunca abre, mesmo quando o serviço está falhando silenciosamente. A função protegida precisa **rejeitar** (ou exceder o timeout) para que o breaker funcione.

> [!warning] Não chamar `breaker.shutdown()` em testes
> opossum usa `setInterval` internamente para a janela deslizante e `setTimeout` para o `resetTimeout`. Se você criar um `CircuitBreaker` num teste e não chamar `breaker.shutdown()` no teardown, esses timers vazam entre suites. O Jest/Vitest pode exibir warnings de "open handles" ou, pior, os timers de um teste podem afetar o estado de outro. Sempre use `afterEach(() => breaker.shutdown())`.

> [!warning] `breaker.open()` / `breaker.close()` bypassam os contadores internos
> Chamar `breaker.open()` ou `breaker.close()` manualmente força a transição de estado **sem passar pela máquina de estados interna** — os contadores de `breaker.stats` (sucessos, falhas, rejeições) não são atualizados. Isso tem duas implicações práticas: (1) após `breaker.open()`, `breaker.stats.failures` continua em 0, então testes que verificam estatísticas após abertura manual não refletem o comportamento real de produção; (2) `breaker.close()` não reinicia os contadores da janela deslizante, então o circuito pode reabrir imediatamente se a janela ainda tiver erros suficientes. Para testar comportamento dependente de stats, prefira injetar falhas reais na função mockada e deixar o opossum abrir o circuito organicamente — use `breaker.open()` apenas para forçar o estado em testes que verificam o comportamento do fallback, não das métricas.

> [!warning] Múltiplos breakers sem `name` diferente geram métricas sobrepostas
> Se você criar dois circuit breakers sem a opção `name` (ou com o mesmo `name`) e usar `opossum-prometheus`, as métricas do Prometheus vão colidir — os contadores de um breaker somam com os do outro. Dê um nome único e descritivo para cada breaker: `name: 'payment-service'`, `name: 'user-service'`, etc.

## Veja também

- [[03-Dominios/Node/Observability e produção/index]] — MOC do galho 5
- [[04 - Métricas com prom-client]] — métricas para monitorar o circuito
- [[09 - Graceful shutdown profundo]] — resiliência no shutdown
- [[Node.js]] — tronco

## Fontes

- [opossum — GitHub (noderaider/opossum)](https://github.com/noderaider/opossum) — documentação oficial, API reference e exemplos de uso
- [opossum — npm](https://www.npmjs.com/package/opossum) — versões e changelog
- [Martin Fowler — CircuitBreaker](https://martinfowler.com/bliki/CircuitBreaker.html) — artigo original que formalizou o pattern
- [Release It! — Michael T. Nygard](https://pragprog.com/titles/mnee2/release-it-second-edition/) — livro de referência para patterns de estabilidade em produção, incluindo circuit breaker e bulkhead
- [opossum-prometheus — npm](https://www.npmjs.com/package/opossum-prometheus) — integração com prom-client
