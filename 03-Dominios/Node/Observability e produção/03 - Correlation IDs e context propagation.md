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
  - context-propagation
  - async-local-storage
  - opentelemetry
aliases:
  - Correlation ID
  - Context Propagation Node
  - AsyncLocalStorage
---

# Correlation IDs e context propagation

> [!abstract] TL;DR
> Um **correlation ID** é um identificador único gerado no início de cada requisição e carregado por todos os logs, métricas e traces produzidos durante aquele ciclo de vida — sem ele, logs de 200 requisições concorrentes se misturam e rastrear um bug vira arqueologia.
> `AsyncLocalStorage` (estável no Node 16+, módulo `node:async_hooks`) é o mecanismo nativo para propagar contexto de forma transparente por toda a cadeia assíncrona sem passar o ID como parâmetro em cada função.
> O padrão moderno é gerar o ID no middleware de entrada (ou reutilizar o `traceId` do header W3C `traceparent`), armazená-lo no `AsyncLocalStorage` e lê-lo em serializers do pino e em spans do OpenTelemetry.
> Em microsserviços, o ID deve ser encaminhado nos headers das chamadas HTTP de saída (`x-request-id` ou `traceparent`) para que o serviço downstream possa continuar o mesmo "fio" de observabilidade.

Esta nota aprofunda a correlação entre os três pilares apresentados em [[02 - Logging estruturado com pino]] e faz parte do galho [[03-Dominios/Node/Observability e produção/index]]. A integração completa com spans é detalhada em [[06 - Tracing distribuído com OpenTelemetry]].

---

## O que é

Em um servidor Node.js que atende dezenas de requisições simultâneas, todas compartilham o mesmo processo. Os logs de todas essas requisições são escritos no mesmo stream de saída — e sem algum campo de correlação, o resultado é um entrelaçamento caótico:

```
[12:00:01.001] INFO  Recebendo requisição POST /orders
[12:00:01.002] INFO  Recebendo requisição GET  /users/42
[12:00:01.010] INFO  Consultando banco de dados
[12:00:01.015] INFO  Consultando banco de dados
[12:00:01.050] ERROR Timeout ao conectar no banco
[12:00:01.055] INFO  Usuário encontrado
```

Qual requisição sofreu o timeout? Qual era o payload? Quem foi o usuário? Impossível saber sem olhar o código, adivinhar, ou ter um sistema de tríagem manual caro.

Um **correlation ID** (também chamado de _request ID_, _trace ID_ ou _context ID_ dependendo do contexto) é um identificador único atribuído a cada requisição no momento em que ela entra no sistema. Esse ID é então:

- **embutido em todos os logs** produzidos durante o processamento daquela requisição;
- **incluído em métricas** como label para permitir drill-down;
- **associado a spans de tracing** como `traceId`;
- **propagado nos headers HTTP** de chamadas a serviços downstream.

Com o correlation ID, o log acima se transforma em:

```json
{"time":"12:00:01.001","requestId":"a1b2c3","msg":"Recebendo requisição POST /orders"}
{"time":"12:00:01.002","requestId":"d4e5f6","msg":"Recebendo requisição GET /users/42"}
{"time":"12:00:01.010","requestId":"a1b2c3","msg":"Consultando banco de dados"}
{"time":"12:00:01.015","requestId":"d4e5f6","msg":"Consultando banco de dados"}
{"time":"12:00:01.050","requestId":"a1b2c3","level":"error","msg":"Timeout ao conectar no banco"}
{"time":"12:00:01.055","requestId":"d4e5f6","msg":"Usuário encontrado"}
```

Agora `jq 'select(.requestId=="a1b2c3")'` isola imediatamente os 3 eventos do POST /orders com problema.

---

## Por que importa

### O pesadelo dos microsserviços sem correlação

Em um sistema monolítico, um stack trace já localiza o problema. Em uma arquitetura de microsserviços com dez serviços, uma única operação de negócio pode gerar logs em quatro serviços diferentes, cada um com seu próprio sistema de logging, cada um com timestamps ligeiramente diferentes (NTP drift), cada um com sua própria noção de "o que aconteceu".

Sem correlation IDs, o SRE de plantão olha para um dashboard mostrando erro 500 no `checkout-service` às 03:47 e precisa:

1. Identificar em qual instância do `checkout-service` ocorreu o erro;
2. Puxar os logs daquela instância naquele intervalo de tempo;
3. Adivinhar qual `order-service` foi chamado e quando;
4. Cruzar manualmente os timestamps;
5. Torcer para que os clocks estejam sincronizados.

Isso pode levar 30-60 minutos. Com correlation IDs, é uma query: `traceId:abc123`.

### Por que o Node precisa de uma solução explícita

Em linguagens com thread-por-request (Java, PHP tradicional), é trivial guardar o correlation ID em uma variável local à thread (ThreadLocal). Em Node.js, que é single-threaded com event loop, não existe "thread local" — uma async chain pode passar por dezenas de callbacks e microtasks, e a stack original se perde.

Antes do `AsyncLocalStorage`, as soluções eram gambiarras: `cls-hooked` (baseado no API `domain`, depreciado), passar o ID explicitamente em todos os parâmetros, ou usar objetos globais mutáveis (perigo de vazamento entre requisições).

### Relevância em entrevistas

Correlation IDs aparecem em perguntas sobre:

- "Como você implementaria distributed tracing do zero?"
- "Como você garantiria que logs de uma mesma requisição possam ser filtrados?"
- "O que é context propagation em microsserviços?"

---

## Como funciona

### AsyncLocalStorage — o mecanismo nativo

`AsyncLocalStorage` é uma classe disponível em `node:async_hooks`. Disponível desde Node 12.17 (experimental), sem flag desde Node 14, **estável desde Node 16**. Para produção, exija Node 16+. Ela implementa um storage que é automaticamente **herdado por toda a cadeia assíncrona** iniciada dentro de um `run()`, sem necessidade de passar o contexto como parâmetro.

```typescript
// context-store.ts
import { AsyncLocalStorage } from 'node:async_hooks';

export interface RequestContext {
  requestId: string;
  userId?: string;
  startTime: number;
  traceId?: string; // preenchido pelo otel-bridge após o span ser criado
}

// Uma única instância por módulo — é thread-safe por design do Node
export const asyncLocalStorage = new AsyncLocalStorage<RequestContext>();

// Helpers convenientes
export function getStore(): RequestContext | undefined {
  return asyncLocalStorage.getStore();
}

export function getRequestId(): string {
  return asyncLocalStorage.getStore()?.requestId ?? 'no-context';
}
```

O padrão de uso é `store.run(context, callback)`: tudo que for executado dentro de `callback` — incluindo todas as Promises e callbacks assíncronos que nascerem daí — enxerga o mesmo objeto `context` via `getStore()`.

```typescript
// Exemplo básico de run() e getStore()
import { asyncLocalStorage, getRequestId } from './context-store';

async function consultarBanco(): Promise<string> {
  // Não precisa receber requestId como parâmetro
  const requestId = getRequestId();
  console.log(`[${requestId}] Executando query`);
  await new Promise(resolve => setTimeout(resolve, 10)); // simula I/O
  console.log(`[${requestId}] Query concluída`);
  return 'resultado';
}

async function processarRequisicao(requestId: string): Promise<void> {
  const context = { requestId, startTime: Date.now() };

  await asyncLocalStorage.run(context, async () => {
    // Tudo aqui dentro — e em qualquer async que nascer aqui — herda o contexto
    console.log(`[${getRequestId()}] Iniciando processamento`);
    const resultado = await consultarBanco(); // contexto propagado automaticamente
    console.log(`[${getRequestId()}] Resultado: ${resultado}`);
  });
}

// Simulação de duas requisições concorrentes
Promise.all([
  processarRequisicao('req-aaa'),
  processarRequisicao('req-bbb'),
]);
// Saída (intercalada, mas IDs corretos):
// [req-aaa] Iniciando processamento
// [req-bbb] Iniciando processamento
// [req-aaa] Executando query
// [req-bbb] Executando query
// [req-aaa] Query concluída
// [req-bbb] Query concluída
// [req-aaa] Resultado: resultado
// [req-bbb] Resultado: resultado
```

O ponto crucial: `consultarBanco` não recebe `requestId` como parâmetro e mesmo assim o exibe corretamente para cada requisição, sem nenhuma variável global.

### Geração e injeção do correlation ID

O correlation ID deve ser gerado **antes** de qualquer trabalho assíncrono. O local correto é o middleware de entrada HTTP, que é o primeiro código a rodar para cada requisição.

Estratégias de geração:

| Estratégia | Prós | Contras |
|---|---|---|
| `crypto.randomUUID()` | Nativo, sem dependência | 36 chars com hifens |
| `nanoid()` | Compacto (21 chars), URL-safe | Dependência extra |
| Reutilizar `traceId` do OTel | Correlação automática com spans | Depende do OTel estar ativo |
| Extrair do header `traceparent` | Compatível com W3C TraceContext | Requer parsing do header |

O header `traceparent` segue o formato W3C TraceContext:

```
traceparent: 00-{traceId-32hex}-{spanId-16hex}-{flags-2hex}
              00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01
```

Na prática, o middleware verifica na seguinte ordem:

1. Existe `traceparent` no request? → extrai o `traceId` (16 bytes / 32 hex chars);
2. Existe `x-request-id`? → usa como correlation ID;
3. Nenhum dos dois? → gera um novo UUID.

```typescript
// middleware/correlation-id.ts
import { randomUUID } from 'node:crypto';

/**
 * Extrai o traceId de um header W3C traceparent.
 * Formato: 00-{traceId}-{spanId}-{flags}
 */
const HEX_32 = /^[0-9a-f]{32}$/

export function extractTraceId(traceparent: string | undefined): string | null {
  if (!traceparent) return null;
  const parts = traceparent.split('-');
  // versão(0) + traceId(1) + spanId(2) + flags(3)
  if (parts.length !== 4 || !HEX_32.test(parts[1])) return null;
  return parts[1];
}

export function resolveCorrelationId(headers: Record<string, string | string[] | undefined>): string {
  const traceparent = headers['traceparent'] as string | undefined;
  const requestId = headers['x-request-id'] as string | undefined;

  return extractTraceId(traceparent) ?? requestId ?? randomUUID();
}
```

### Propagação automática com AsyncLocalStorage

Uma vez que o contexto está no `AsyncLocalStorage`, ele se propaga automaticamente para `Promise.then`, `await`, `setTimeout`, `setImmediate`, e callbacks de I/O do Node — tudo que usa a maquinaria de async hooks internamente.

```typescript
// Demonstração: contexto disponível em toda a cadeia async
import { asyncLocalStorage, getRequestId } from './context-store';
import { randomUUID } from 'node:crypto';

async function nivel3(): Promise<void> {
  // Três níveis de async abaixo do run() — ainda funciona
  await new Promise(resolve => setImmediate(resolve));
  console.log(`nivel3 — requestId: ${getRequestId()}`);
}

async function nivel2(): Promise<void> {
  await new Promise(resolve => setTimeout(resolve, 5));
  await nivel3();
  console.log(`nivel2 — requestId: ${getRequestId()}`);
}

async function nivel1(): Promise<void> {
  await nivel2();
  console.log(`nivel1 — requestId: ${getRequestId()}`);
}

asyncLocalStorage.run({ requestId: randomUUID(), startTime: Date.now() }, async () => {
  await nivel1();
});
```

**Armadilha com `Promise.all`**: cada branch do `Promise.all` herda o mesmo contexto do ponto de criação, então funciona corretamente. O problema seria se você chamar `asyncLocalStorage.run()` dentro de um dos branches para criar um sub-contexto — os outros branches não seriam afetados (o que geralmente é o comportamento desejado).

```typescript
// Promise.all propaga corretamente o contexto pai
asyncLocalStorage.run({ requestId: 'req-xyz', startTime: Date.now() }, async () => {
  await Promise.all([
    consultarUsuario(),    // vê requestId: req-xyz
    consultarProdutos(),   // vê requestId: req-xyz
    consultarEstoque(),    // vê requestId: req-xyz
  ]);
});
```

### Integração com logs, métricas e traces

O verdadeiro poder do `AsyncLocalStorage` aparece quando os três pilares de observabilidade passam a ler o correlation ID de forma automática:

**Pino via mixin**: o campo `requestId` é injetado em cada log sem chamadas explícitas.

```typescript
// logger.ts
import pino from 'pino';
import { getStore } from './context-store';

export const logger = pino({
  level: process.env.LOG_LEVEL ?? 'info',
  mixin() {
    // Chamado toda vez que um log é emitido
    const store = getStore();
    if (!store) return {};
    return {
      requestId: store.requestId,
      userId: store.userId,
    };
  },
});
```

**OpenTelemetry**: ao criar um span, o `traceId` do span ativo pode ser sincronizado com o `requestId` do store para que logs e traces sejam correlacionáveis por ID.

```typescript
// otel-bridge.ts
import { trace } from '@opentelemetry/api';
import { getStore } from './context-store';

export function enrichSpanWithRequestId(): void {
  const store = getStore();
  if (!store) return;

  const activeSpan = trace.getActiveSpan();
  if (activeSpan) {
    activeSpan.setAttribute('app.requestId', store.requestId);
    // Também podemos adicionar o traceId ao store para aparecer nos logs
    // Adicionado uma vez no setup, antes de qualquer leitura concorrente —
    // diferente da mutação durante o handler (ver Armadilhas)
    const traceId = activeSpan.spanContext().traceId;
    store.traceId = traceId;
  }
}
```

Com isso, uma entrada de log contém `requestId` (gerado pelo app), e o sistema de tracing contém `app.requestId` como atributo do span — permitindo navegar de um log para o span correspondente.

---

## Na prática

Middleware completo para Express que integra todas as peças:

```typescript
// middleware/request-context.middleware.ts
import { Request, Response, NextFunction } from 'express';
import { randomUUID } from 'node:crypto';
import { asyncLocalStorage, RequestContext } from '../context-store';
import { logger } from '../logger';

/**
 * Extrai o traceId do header W3C traceparent.
 * Formato: 00-{32hex traceId}-{16hex spanId}-{2hex flags}
 */
const HEX_32 = /^[0-9a-f]{32}$/

function extractTraceId(traceparent: string | undefined): string | null {
  if (!traceparent) return null;
  const parts = traceparent.split('-');
  if (parts.length !== 4 || !HEX_32.test(parts[1])) return null;
  return parts[1];
}

export function requestContextMiddleware(
  req: Request,
  res: Response,
  next: NextFunction,
): void {
  // 1. Resolver o correlation ID: traceparent > x-request-id > novo UUID
  const traceparent = req.headers['traceparent'] as string | undefined;
  const incomingRequestId = req.headers['x-request-id'] as string | undefined;
  const requestId = extractTraceId(traceparent) ?? incomingRequestId ?? randomUUID();

  // 2. Montar o contexto da requisição
  const context: RequestContext = {
    requestId,
    startTime: Date.now(),
    userId: undefined, // será preenchido pelo middleware de autenticação
  };

  // 3. Rodar toda a cadeia de handlers dentro do AsyncLocalStorage
  asyncLocalStorage.run(context, () => {
    // 4. Expor o ID no header de resposta para o cliente e serviços downstream
    res.setHeader('x-request-id', requestId);

    // 5. Log de início da requisição (requestId já vem do mixin do pino)
    logger.info({ method: req.method, path: req.path }, 'Request received');

    // 6. Log de fim com duração ao fechar a resposta
    // Context propagates through event emitter listeners registered inside run()
    // Verified behavior on Node 18+; test on older versions if targeting Node 16
    res.on('finish', () => {
      // getStore() works here on Node 18+
      const duration = Date.now() - context.startTime;
      logger.info(
        { method: req.method, path: req.path, status: res.statusCode, duration },
        'Request completed',
      );
    });

    next();
  });
}
```

Registro no app Express:

```typescript
// app.ts
import express from 'express';
import { requestContextMiddleware } from './middleware/request-context.middleware';
import { logger } from './logger';

const app = express();

// Deve ser o PRIMEIRO middleware — antes de qualquer lógica de negócio
app.use(requestContextMiddleware);
app.use(express.json());

app.get('/orders/:id', async (req, res) => {
  // Não precisa passar requestId — o pino injeta automaticamente via mixin
  logger.info({ orderId: req.params.id }, 'Fetching order');
  // ... lógica de negócio
  res.json({ orderId: req.params.id, status: 'ok' });
});

app.listen(3000, () => logger.info('Server running on :3000'));
```

---

## Propagação para serviços downstream

Quando o serviço A chama o serviço B, o correlation ID deve ser incluído nos headers da requisição de saída. Dessa forma, o serviço B pode extrair o mesmo ID e continuar o "fio" de observabilidade sem gerar um novo ID.

```typescript
// http-client.ts
import { getRequestId } from './context-store';

/**
 * Wrapper sobre fetch que propaga automaticamente o correlation ID
 * para serviços downstream via x-request-id.
 */
export async function fetchWithCorrelation(
  url: string,
  options: RequestInit = {},
): Promise<Response> {
  const requestId = getRequestId();

  const headers = new Headers(options.headers);
  headers.set('x-request-id', requestId);
  // Se você usar W3C TraceContext, propague também o traceparent
  // headers.set('traceparent', buildTraceparent(requestId));

  return fetch(url, { ...options, headers });
}

// Uso em qualquer parte do código — sem passar requestId como parâmetro
async function buscarEstoque(produtoId: string): Promise<number> {
  const response = await fetchWithCorrelation(
    `https://estoque-service/produtos/${produtoId}`,
  );
  const data = await response.json();
  return data.quantidade;
}
```

Com esse padrão, o log do `estoque-service` terá o mesmo `requestId` que o log do serviço que o chamou, permitindo que uma query `requestId:abc123` retorne logs de todos os serviços envolvidos em uma única operação de negócio.

---

## Armadilhas

> [!warning] Gerar o ID após código assíncrono
> O `asyncLocalStorage.run()` deve envolver **toda** a lógica da requisição. Se você gerar o ID dentro de um `setTimeout`, um `setImmediate`, ou qualquer outro callback assíncrono iniciado antes do `run()`, o contexto não estará disponível nas chamadas que vieram antes desse ponto.
>
> ```typescript
> // ERRADO — o run() começa depois do primeiro await
> app.use(async (req, res, next) => {
>   await autenticarToken(req); // contexto ainda não existe aqui!
>   const requestId = randomUUID();
>   asyncLocalStorage.run({ requestId, startTime: Date.now() }, () => next());
> });
>
> // CORRETO — o run() é o primeiro passo
> app.use((req, res, next) => {
>   const requestId = randomUUID();
>   asyncLocalStorage.run({ requestId, startTime: Date.now() }, () => next());
> });
> ```

> [!warning] Não propagar o ID nos headers de saída
> O correlation ID só é útil em microsserviços se viajar junto com as requisições HTTP de saída. Um erro comum é armazenar o ID no `AsyncLocalStorage` mas esquecer de incluí-lo nos headers do `fetch` / `axios` / `got` que chamam serviços externos. O resultado: o serviço downstream gera um novo ID e o "fio" de observabilidade é cortado.

> [!warning] Usar `cls-hooked` ou `domain` em vez de `AsyncLocalStorage`
> `domain` está marcado como depreciado desde Node 4 e pode causar comportamentos imprevisíveis com Promises modernas. `cls-hooked` é uma biblioteca de terceiros construída sobre `domain`. Ambos são soluções legadas que **não devem ser usadas em projetos novos**. `AsyncLocalStorage` é a API oficial, mantida pela equipe do Node, e está estável desde Node 16.

> [!warning] Confundir `requestId` com `traceId` (W3C traceparent)
> São conceitos relacionados mas distintos:
> - `requestId` (ou `x-request-id`): identificador gerado pelo seu aplicativo, formato livre, não padronizado entre vendors.
> - `traceId`: parte do header W3C `traceparent` (`00-{traceId}-{spanId}-{flags}`), 128 bits / 32 hex chars, compartilhado entre todos os serviços que fazem parte do mesmo trace distribuído e entendido por ferramentas como Jaeger, Zipkin, Datadog.
>
> Idealmente, use o `traceId` do OpenTelemetry como `requestId` do seu aplicativo — assim você tem um único ID que funciona tanto nos seus logs quanto nas ferramentas de tracing.

> [!warning] Modificar o store diretamente pode causar vazamento
> `asyncLocalStorage.getStore()` retorna uma referência ao objeto de contexto. Se você modificar o objeto em um branch assíncrono, a modificação é visível em todos os outros branches que compartilham o mesmo contexto (pois é o mesmo objeto). Para criar sub-contextos isolados, use um novo `asyncLocalStorage.run()` com um objeto clonado: `asyncLocalStorage.run({ ...currentStore, userId: '42' }, callback)`.

---

## Em entrevista

**What is a correlation ID and why is it important?**
A correlation ID is a unique identifier, typically a UUID or a W3C trace ID, that is generated at the entry point of a request and attached to every log entry, metric label, and trace span produced during that request's lifecycle. Without it, in a high-concurrency Node.js server, log entries from hundreds of concurrent requests are interleaved in the same output stream, making it impossible to isolate the sequence of events that led to a specific error.

**Why is AsyncLocalStorage the modern approach for context propagation in Node.js?**
`AsyncLocalStorage`, available natively in `node:async_hooks` since Node 16, provides a per-async-chain storage that is automatically inherited by all child Promises, callbacks, and async operations that are spawned within an `asyncLocalStorage.run()` call. This means the correlation ID can be stored once at the request boundary and read anywhere downstream — in service functions, database clients, logger serializers — without passing it as a function parameter, which would pollute every function signature in the codebase. Older approaches like `domain` or the `cls-hooked` library are deprecated and should not be used.

**How do you propagate context across microservice boundaries?**
When service A makes an outgoing HTTP call to service B, it must include the correlation ID in the request headers — typically as `x-request-id` for internal convention, or as `traceparent` if following the W3C TraceContext standard. Service B's request middleware then extracts the incoming ID instead of generating a new one, stores it in its own `AsyncLocalStorage`, and continues producing logs and spans with the same ID. This creates a unified thread of observability across all services involved in a single business operation, which can then be queried by a single `requestId` in a log aggregation tool like Datadog or Loki.

---

## Vocabulário

| Português | English |
|---|---|
| Correlação (de logs/traces) | Correlation |
| Propagação de contexto | Context propagation |
| Armazenamento local assíncrono | Async local storage |
| Cabeçalho HTTP | HTTP header |
| Middleware de entrada | Ingress middleware |
| Rastreamento distribuído | Distributed tracing |
| Âncora de contexto | Context anchor |
| Contexto W3C TraceContext | W3C TraceContext |
| Identificador de requisição | Request ID / correlation ID |
| Serializer de log | Log serializer |
| Cadeia assíncrona | Async chain |
| Herança de contexto | Context inheritance |

---

## Fontes

- [Node.js Docs — AsyncLocalStorage](https://nodejs.org/api/async_context.html#class-asynclocalstorage)
- [W3C TraceContext Specification](https://www.w3.org/TR/trace-context/)
- [OpenTelemetry Context Propagation](https://opentelemetry.io/docs/concepts/context-propagation/)
- [Pino — mixin option](https://getpino.io/#/docs/api?id=mixin-function)
