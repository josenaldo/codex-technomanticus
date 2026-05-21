---
title: "Clientes HTTP - fetch, axios, got e undici"
created: 2026-05-12
updated: 2026-05-12
type: concept
status: growing
publish: true
tags:
  - node
  - http
  - clientes
  - integrações
aliases:
  - HTTP clients Node
  - fetch Node
  - axios Node
  - undici
---

# Clientes HTTP - fetch, axios, got e undici

> [!abstract] TL;DR
> O Node.js 18+ trouxe `fetch` nativo baseado no padrão WHATWG — a escolha padrão para novos projetos sem dependências extras. **`axios`** permanece popular por seu sistema de **interceptors** (middleware de request/response), cancelamento via `AbortController` e tratamento automático de erros HTTP.
>
> **`got`** é a opção mais rica em features sem overhead excessivo: retry automático com backoff configurável, hooks de ciclo de vida e streaming de primeira classe. **`undici`** é o motor que alimenta o `fetch` nativo do Node — acessá-lo diretamente com `Pool` e `Agent` dá máximo controle sobre connection pooling, pipeline e throughput em cenários de alto volume.
>
> Critério de escolha: `fetch` para padrão moderno, `undici` para performance crítica, `got` para retry/stream embutidos, `axios` quando interceptors ou legado exigem. Veja [[03-Dominios/Node/Integrações/index|Integrações]] para o contexto completo do galho.

## Como funciona

### fetch API — Request, Response e Headers

A Fetch API do WHATWG é baseada em três primitivas imutáveis: `Request`, `Response` e `Headers`. Uma chamada `fetch(url, init)` retorna uma `Promise<Response>` que **resolve assim que os headers chegam** — o body ainda não foi lido. Para consumir o body você chama `.json()`, `.text()`, `.arrayBuffer()` ou `.body` (ReadableStream).

O ponto crítico que pega todo mundo: **`fetch` não rejeita a Promise em respostas HTTP de erro (4xx/5xx)**. A Promise só rejeita por falha de rede (DNS, conexão recusada, timeout de rede). Para detectar erros HTTP você precisa verificar `response.ok` (booleano: `true` quando status está entre 200–299) ou `response.status` explicitamente.

Timeout em `fetch` nativo é feito via `AbortController` — não há opção `timeout` no `init`. O padrão moderno usa `AbortSignal.timeout(ms)` disponível a partir do Node 17.3+, que cria um sinal que aborta automaticamente após o prazo especificado.

```
fetch  ──► Promise<Response>
               │
               ├── response.ok?  true  → body.json() / body.text()
               └── response.ok?  false → throw new Error / retornar erro
```

### Interceptors em axios

O `axios` expõe dois stacks de interceptors: `axios.interceptors.request` e `axios.interceptors.response`. Cada um é uma pilha LIFO (last-in, first-out) de handlers que recebem config/response e podem transformá-los ou rejeitar a Promise.

O interceptor de **request** é ideal para injetar tokens de autenticação, adicionar headers de correlação ou logar saídas. O de **response** é usado para tratar erros globalmente (refresh de token em 401, log estruturado de 5xx) e para normalizar formatos de resposta antes de chegar no código de negócio.

Diferente do `fetch`, o `axios` **lança exceção automaticamente para respostas 4xx e 5xx**, colocando o objeto response dentro de `error.response`. Isso simplifica o tratamento de erros sem `if (response.ok)` em cada chamada.

O cancelamento de requisições no `axios` usa o mesmo `AbortController` do Web Platform, unificando o padrão com o `fetch` nativo (a API legada de `CancelToken` foi depreciada na v1).

### Hooks em got

O `got` organiza o ciclo de vida de uma requisição em **hooks tipados**: `beforeRequest`, `beforeRedirect`, `beforeRetry`, `afterResponse` e `beforeError`. Cada hook recebe o estado atual da requisição e pode modificá-lo ou lançar uma exceção para interromper o ciclo.

O **retry automático** do `got` é configurável por: número de tentativas, códigos de status que ativam retry, métodos HTTP retentáveis e estratégia de backoff (exponencial por padrão com jitter). Isso elimina a necessidade de implementar retry manualmente, um padrão que frequentemente tem bugs em implementações ad hoc.

O suporte a **streaming** é de primeira classe: `got.stream(url)` retorna um `Readable` padrão do Node que pode ser conectado via `.pipe()` ou consumido com `for await`. O stream já processa gzip/deflate automaticamente e emite eventos de progresso via `downloadProgress`.

### Pool e Agent em undici para controle de conexão

O `undici` implementa o protocolo HTTP/1.1 from scratch no Node (substitui o `http.request` interno). Ele expõe três clientes com diferentes trade-offs:

| Classe | Uso |
|---|---|
| `Client` | Uma única conexão para um origin; máximo controle |
| `Pool` | N conexões paralelas para o mesmo origin; alto throughput |
| `Dispatcher` | Interface base; permite implementar transports customizados |

O `Pool` mantém um conjunto de conexões TCP persistentes (keep-alive) para o mesmo host. Em vez de abrir e fechar conexão a cada request, as conexões são reutilizadas da pool — elimina o overhead de TCP handshake e TLS em cada chamada.

As configurações críticas do `Pool` são:
- `connections`: número máximo de conexões simultâneas para o origin
- `pipelining`: quantos requests podem ser enfileirados numa mesma conexão (HTTP/1.1 pipelining)
- `keepAliveTimeout`: quanto tempo manter conexão idle antes de fechar

O `undici` também é o motor por trás do `fetch` global do Node 18+ — quando você chama `fetch()`, internamente é um `undici.fetch()` com um `Agent` global padrão. Acessar o `Pool` diretamente permite tunar parâmetros que não são expostos pela Fetch API.

## Snippets

### Snippet 1 — fetch nativo com timeout via AbortController

```typescript
// fetch nativo com AbortSignal.timeout (Node 17.3+ / Node 18+)
// AbortSignal.timeout() cria um sinal que aborta automaticamente após o prazo

interface GitHubUser {
  login: string;
  name: string | null;
  public_repos: number;
}

async function fetchGitHubUser(username: string): Promise<GitHubUser> {
  // AbortSignal.timeout(ms) — forma moderna; sem necessidade de AbortController manual
  const signal = AbortSignal.timeout(5_000); // 5 segundos

  const response = await fetch(`https://api.github.com/users/${username}`, {
    headers: { Accept: 'application/vnd.github.v3+json' },
    signal,
  });

  // fetch NÃO lança exceção em 4xx/5xx — checar response.ok é obrigatório
  if (!response.ok) {
    const errorBody = await response.text();
    throw new Error(
      `GitHub API error: ${response.status} ${response.statusText} — ${errorBody}`
    );
  }

  return response.json() as Promise<GitHubUser>;
}

// Uso com tratamento de timeout
async function main(): Promise<void> {
  try {
    const user = await fetchGitHubUser('nodejs');
    console.log(`${user.login} has ${user.public_repos} public repos`);
  } catch (error) {
    if (error instanceof DOMException && error.name === 'TimeoutError') {
      console.error('Request timed out after 5s');
    } else if (error instanceof Error) {
      console.error('Request failed:', error.message);
    }
  }
}

main();
```

### Snippet 2 — axios com interceptors de request e response

```typescript
import axios, { AxiosInstance, InternalAxiosRequestConfig, AxiosResponse, AxiosError } from 'axios';

interface ApiUser {
  id: number;
  name: string;
  email: string;
}

// Cria instância configurada com interceptors
function createApiClient(baseURL: string, getToken: () => string | null): AxiosInstance {
  const client = axios.create({
    baseURL,
    timeout: 8_000, // 8 segundos — axios suporta timeout nativo
    headers: { 'Content-Type': 'application/json' },
  });

  // Interceptor de REQUEST — injeta Authorization header
  client.interceptors.request.use(
    (config: InternalAxiosRequestConfig): InternalAxiosRequestConfig => {
      const token = getToken();
      if (token) {
        config.headers.set('Authorization', `Bearer ${token}`);
      }
      console.log(`[REQ] ${config.method?.toUpperCase()} ${config.url}`);
      return config;
    },
    (error: AxiosError) => Promise.reject(error)
  );

  // Interceptor de RESPONSE — loga erros estruturados
  client.interceptors.response.use(
    (response: AxiosResponse): AxiosResponse => {
      console.log(`[RES] ${response.status} ${response.config.url}`);
      return response;
    },
    (error: AxiosError): Promise<never> => {
      if (error.response) {
        // Servidor respondeu com status fora de 2xx
        console.error(
          `[ERR] ${error.response.status} ${error.config?.url} —`,
          error.response.data
        );
      } else if (error.request) {
        // Request enviado mas sem resposta (timeout, rede)
        console.error('[ERR] No response received:', error.message);
      }
      return Promise.reject(error);
    }
  );

  return client;
}

// Demonstração de uso
async function fetchUser(userId: number): Promise<ApiUser> {
  const client = createApiClient('https://jsonplaceholder.typicode.com', () => 'my-jwt-token');
  const { data } = await client.get<ApiUser>(`/users/${userId}`);
  return data;
}

async function main(): Promise<void> {
  const user = await fetchUser(1);
  console.log(`Fetched user: ${user.name} <${user.email}>`);
}

main();
```

### Snippet 3 — got com retry automático, timeout por fase e streaming

```typescript
import got, { Options as GotOptions } from 'got';
import { createWriteStream } from 'node:fs';
import { pipeline } from 'node:stream/promises';

// got com retry automático e timeout por fase
async function fetchWithRetry(url: string): Promise<string> {
  const body = await got.get(url, {
    retry: {
      limit: 3,                        // máximo 3 tentativas extras
      methods: ['GET', 'HEAD'],
      statusCodes: [429, 500, 502, 503, 504],
      calculateDelay: ({ attemptCount }) =>
        // backoff exponencial com jitter: 500ms, 1000ms, 2000ms (± 20%)
        Math.floor(500 * 2 ** attemptCount * (0.8 + Math.random() * 0.4)),
    },
    timeout: {
      connect: 2_000,    // TCP handshake
      send: 5_000,       // envio do request
      response: 10_000,  // aguardar primeiro byte do response
    },
    hooks: {
      beforeRetry: [
        (error, retryCount) => {
          console.warn(`Retry #${retryCount} after error: ${error.message}`);
        },
      ],
    },
  } satisfies GotOptions).text();

  return body;
}

// got.stream — baixar arquivo sem carregar tudo em memória
async function downloadFile(url: string, destPath: string): Promise<void> {
  const downloadStream = got.stream(url, {
    timeout: { response: 30_000 },
  });

  // Progresso de download
  downloadStream.on('downloadProgress', ({ transferred, total, percent }) => {
    if (total) {
      process.stdout.write(`\rDownloading: ${(percent * 100).toFixed(1)}% (${transferred}/${total})`);
    }
  });

  // pipeline garante que todos os streams são fechados corretamente em caso de erro
  await pipeline(downloadStream, createWriteStream(destPath));
  console.log(`\nDownloaded to ${destPath}`);
}

async function main(): Promise<void> {
  const html = await fetchWithRetry('https://nodejs.org/en');
  console.log(`Fetched ${html.length} chars`);

  await downloadFile(
    'https://nodejs.org/dist/latest/node-latest.tar.gz',
    '/tmp/node-latest.tar.gz'
  );
}

main();
```

### Snippet 4 — undici.Pool com alto throughput

```typescript
import { Pool, Dispatcher } from 'undici';

interface NpmPackage {
  name: string;
  version: string;
  description: string;
}

// Pool reutilizável para o mesmo origin — criar UMA instância e reusar
const npmPool = new Pool('https://registry.npmjs.org', {
  connections: 10,          // 10 conexões TCP simultâneas para o origin
  pipelining: 1,            // requests por conexão (1 = sem pipelining; seguro para HTTP/1.1)
  keepAliveTimeout: 30_000, // mantém conexão idle por 30s antes de fechar
  keepAliveMaxTimeout: 60_000,
  connectTimeout: 5_000,    // timeout para estabelecer conexão TCP
  headersTimeout: 10_000,   // timeout para receber headers da resposta
  bodyTimeout: 30_000,      // timeout para receber body completo
});

async function fetchPackage(name: string): Promise<NpmPackage> {
  const { statusCode, body } = await npmPool.request({
    path: `/${encodeURIComponent(name)}/latest`,
    method: 'GET',
    headers: { accept: 'application/json' },
  });

  if (statusCode < 200 || statusCode >= 300) {
    // Consumir o body para liberar a conexão de volta ao pool
    await body.dump();
    throw new Error(`npm registry error: ${statusCode} for package "${name}"`);
  }

  const data = await body.json() as NpmPackage;
  return data;
}

// Buscar múltiplos pacotes em paralelo — pool distribui nas 10 conexões
async function fetchMultiplePackages(names: string[]): Promise<NpmPackage[]> {
  const results = await Promise.all(names.map(name => fetchPackage(name)));
  return results;
}

async function main(): Promise<void> {
  const packages = await fetchMultiplePackages(['express', 'fastify', 'hono', 'koa', 'nestjs']);
  for (const pkg of packages) {
    console.log(`${pkg.name}@${pkg.version} — ${pkg.description}`);
  }

  // Sempre fechar o pool ao encerrar a aplicação para liberar conexões TCP
  await npmPool.destroy();
}

main();
```

### Snippet 5 — Mock de fetch em testes com vi.stubGlobal (Vitest)

```typescript
// arquivo: src/user-service.ts
export interface User {
  id: number;
  name: string;
  email: string;
}

export async function fetchUserById(id: number): Promise<User> {
  const signal = AbortSignal.timeout(5_000);
  const response = await fetch(`https://api.example.com/users/${id}`, { signal });

  if (!response.ok) {
    throw new Error(`Failed to fetch user ${id}: ${response.status} ${response.statusText}`);
  }

  return response.json() as Promise<User>;
}
```

```typescript
// arquivo: src/user-service.test.ts
import { describe, it, expect, vi, afterEach } from 'vitest';
import { fetchUserById, User } from './user-service';

// Helper para criar um Response mock com corpo JSON
function mockJsonResponse(data: unknown, status = 200): Response {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}

describe('fetchUserById', () => {
  afterEach(() => {
    vi.unstubAllGlobals(); // restaura o fetch global após cada teste (stubGlobal não é desfeito por restoreAllMocks)
  });

  it('retorna o usuário quando a API responde 200', async () => {
    const mockUser: User = { id: 1, name: 'Alice', email: 'alice@example.com' };

    // vi.stubGlobal substitui o fetch global no ambiente de teste
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue(mockJsonResponse(mockUser)));

    const user = await fetchUserById(1);

    expect(user).toEqual(mockUser);
    expect(fetch).toHaveBeenCalledOnce();
    expect(fetch).toHaveBeenCalledWith(
      'https://api.example.com/users/1',
      expect.objectContaining({ signal: expect.any(AbortSignal) })
    );
  });

  it('lança erro quando a API responde 404', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue(mockJsonResponse({ message: 'Not Found' }, 404))
    );

    await expect(fetchUserById(999)).rejects.toThrow('Failed to fetch user 999: 404');
  });

  it('lança erro de rede quando fetch rejeita', async () => {
    vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new TypeError('Network error')));

    await expect(fetchUserById(1)).rejects.toThrow('Network error');
  });
});
```

> [!tip] MSW como alternativa
> Para testes de integração mais realistas, o [MSW (Mock Service Worker)](https://mswjs.io/) intercepta requests na camada de rede usando Service Workers (browser) ou `@mswjs/interceptors` (Node), permitindo mock declarativo por handler sem alterar o código de produção.

## Armadilhas

> [!danger] Não configurar timeout — request pendente indefinidamente
> O `fetch` nativo **não tem timeout padrão**. Uma requisição para um servidor que aceita a conexão mas nunca responde ficará pendente para sempre, consumindo um file descriptor e potencialmente travando toda a aplicação em ambientes sem retry. Sempre configure `AbortSignal.timeout(ms)` ou um `AbortController` com `setTimeout`. O mesmo vale para `undici` sem `headersTimeout`/`bodyTimeout`.

> [!danger] Ignorar response.ok em fetch — 404 e 500 passam silenciosamente
> O maior gotcha do `fetch`: um `GET` que retorna `404 Not Found` **resolve** a Promise com sucesso. Se você fizer `const data = await (await fetch(url)).json()`, vai receber o body do erro (geralmente `{"message":"Not Found"}`) como se fosse dado válido. Sempre verifique `response.ok` antes de consumir o body, ou encapsule em um helper que lança automaticamente.

> [!warning] Não reutilizar undici.Pool para o mesmo host
> Criar um `new Pool(...)` por request derrota completamente o propósito de connection pooling — cada instância abre e fecha suas próprias conexões TCP, gastando handshake e TLS em cada chamada. Instâncias de `Pool` e `Client` devem ser criadas **uma vez** (escopo de módulo ou singleton) e reutilizadas durante todo o ciclo de vida da aplicação.

> [!warning] axios em bundles edge sem verificar tamanho
> O `axios` não é tree-shakeable e adiciona ~13 KB gzipped ao bundle. Em **Edge Runtimes** (Cloudflare Workers, Vercel Edge Functions, Deno Deploy) que têm limite de bundle size, prefira o `fetch` nativo ou `undici` que já está disponível como dependência do Node. Além disso, alguns adaptadores do axios usam APIs do Node (`http`, `https`) que não existem em Edge environments.

> [!warning] got em ambientes Edge e ESM vs CJS
> O `got` v12+ é **ESM puro** — não funciona com `require()` em projetos CJS sem transformação. Em projetos legados CommonJS, use `got` v11 ou migre para `fetch`/`axios`. Em Edge runtimes, o `got` usa internamente `node:http` e **não funciona** — use `fetch` nativo nesses ambientes.

> [!tip] Interceptors do axios não se propagam para instâncias filhas
> Interceptors configurados em `axios` (instância global) **não são herdados** por instâncias criadas com `axios.create()`. Cada instância tem sua própria stack de interceptors. Configure interceptors sempre na instância retornada por `create()`, não no objeto global.

## Comparação

| Feature | `fetch` nativo | `axios` | `got` | `undici` (direto) |
|---|---|---|---|---|
| **Bundle size** | 0 KB (built-in) | ~13 KB gzip | ~35 KB gzip | 0 KB (built-in) |
| **Node versão mínima** | 18.0+ (global) | qualquer | 16+ (ESM) | 16.5+ |
| **Timeout nativo** | Via `AbortSignal` | `timeout` option | Por fase (connect/send/response) | Por fase (headersTimeout/bodyTimeout) |
| **Retry automático** | Não | Não (precisa lib) | Sim (built-in) | Não |
| **Interceptors/Hooks** | Não | Interceptors (request/response) | Hooks tipados (5 fases) | Não |
| **Streaming** | `response.body` (ReadableStream) | `responseType: 'stream'` | `got.stream()` (Node Readable) | `body` como `Readable` |
| **Lança em 4xx/5xx** | Não (`response.ok`) | Sim (automático) | Sim (HTTPError) | Não (`statusCode`) |
| **Connection Pool** | Agent global (undici) | Sem controle direto | Sem controle direto | `Pool` configurável |
| **Edge Runtime** | Sim | Parcial (adaptadores) | Não | Não |
| **HTTP/2** | Não (Node nativo) | Não | Sim (experimental) | Sim |
| **TypeScript** | Tipos nativos (lib.dom) | Tipos inclusos | Tipos inclusos | Tipos inclusos |

## Em entrevista

### Why doesn't fetch throw an exception on a 404 response?

The `fetch` API follows the WHATWG specification, which separates **network-level failures** from **HTTP-level errors** by design. A Promise rejection in `fetch` means the request never reached the server or the connection was lost — for example, DNS resolution failure, refused connection, or a network timeout. A `404 Not Found` response, however, is a perfectly valid HTTP response: the server received the request, processed it, and communicated that the resource doesn't exist. From the network protocol perspective, this is a successful transaction. To detect HTTP errors, you must inspect `response.ok` (which is `true` only for 2xx status codes) or check `response.status` explicitly and throw accordingly.

### How would you implement retry with exponential backoff using native fetch?

Native `fetch` has no built-in retry mechanism, so you need to implement it yourself using a recursive or iterative wrapper function. The key elements are: a maximum attempt count, a delay calculation function (typically `baseDelay * 2^attempt + random jitter` to avoid thundering herd), and criteria for which responses or errors are retryable. You should retry on network errors (`TypeError` from `fetch`) and on specific HTTP status codes like `429`, `503`, and `504`, but not on `400` or `404` which indicate client errors that won't change on retry. Each iteration must create a fresh `AbortSignal` because a cancelled signal cannot be reused, and `AbortSignal.timeout()` is single-use. For production use, libraries like `got` or `p-retry` handle edge cases (max delay cap, jitter, error classification) that are easy to miss in hand-rolled implementations.

### What is the difference between undici and fetch in Node 18+?

`undici` is the HTTP/1.1 client library that **implements** the `fetch` global in Node 18+. When you call `fetch()` in Node 18, you are calling `undici.fetch()` internally, using a shared global `undici.Agent` with default settings. The key difference is the level of control: the `fetch` API exposes only what the WHATWG spec defines — you cannot configure connection pool size, pipelining, or per-origin timeouts through `fetch`. Accessing `undici` directly via `import { Pool } from 'undici'` lets you configure `connections` (pool size), `keepAliveTimeout`, `headersTimeout`, `bodyTimeout`, and `pipelining` per origin, which is essential for high-throughput services that make thousands of outbound requests per second. In summary: `fetch` is the standards-compliant surface for general use, while `undici` direct access is the performance escape hatch when you need to squeeze every millisecond.

### When should you prefer got or axios over fetch?

Prefer **`got`** when you need battle-tested retry logic with exponential backoff out of the box, typed hooks for every phase of the request lifecycle, or first-class streaming with progress events — all without writing the plumbing yourself. `got` also handles edge cases like following redirects with proper method changes (302 POST → GET), automatic decompression, and detailed error objects (`RequestError`, `HTTPError`, `TimeoutError`) with rich context. Prefer **`axios`** when you are working on a project that already uses it, need to share an `axios` instance with interceptors across many services, or require compatibility with environments where `fetch` is polyfilled inconsistently. `axios` also supports older Node versions and has a larger ecosystem of adapters and plugins. Use **`fetch`** directly when you want zero dependencies, are targeting Edge runtimes (Cloudflare Workers, Vercel Edge), or when the request logic is simple enough that adding a library creates more complexity than it removes.

## Vocabulário

| Termo | Definição |
|---|---|
| `AbortController` | Interface do Web Platform que expõe um `signal` e um método `abort()`. Permite cancelar operações assíncronas como `fetch` que aceitam um `AbortSignal`. |
| `AbortSignal` | Objeto passado para `fetch` (e outras APIs) via `{ signal }` que, quando ativado, cancela a operação em andamento e lança um `DOMException` com `name: 'AbortError'` ou `'TimeoutError'`. |
| `response.ok` | Propriedade booleana do objeto `Response` do `fetch`: `true` quando `status >= 200 && status <= 299`. É a forma idiomática de verificar sucesso HTTP no `fetch`, já que ele não lança exceção em erros de status. |
| interceptor | No contexto do `axios`: função registrada em `interceptors.request` ou `interceptors.response` que é executada para cada request/response antes que o código de negócio o receba. Equivalente ao middleware de HTTP no lado do cliente. |
| hook | No contexto do `got`: callback tipado registrado por fase do ciclo de vida da requisição (`beforeRequest`, `beforeRetry`, `afterResponse`, etc.). Similar aos interceptors do axios, mas com nomenclatura de fase explícita e tipagem mais granular. |
| connection pool | Conjunto de conexões TCP persistentes mantidas abertas para reutilização com o mesmo host, evitando o overhead de TCP handshake e TLS negotiation em cada requisição. |
| `undici.Pool` | Classe do `undici` que gerencia N conexões TCP paralelas para um único origin. Aceita configurações de `connections`, `pipelining`, `keepAliveTimeout` e timeouts por fase. É o mecanismo de pooling usado internamente pelo `fetch` nativo do Node. |
| keep-alive | Diretiva HTTP (`Connection: keep-alive`) que instrui o servidor a manter a conexão TCP aberta após o response, permitindo que requests subsequentes reutilizem o mesmo socket sem novo handshake. |
| `agent` | Objeto (no Node `http.Agent` ou no undici) responsável por gerenciar conexões para um determinado host, controlando reuso, pool size e timeouts. Em `axios` e `got`, pode ser injetado via opção `agent` para customizar comportamento de conexão. |
| timeout por fase | Estratégia de timeout que define prazos separados para cada fase da requisição: tempo para estabelecer conexão TCP (`connect`), tempo para enviar o request (`send`), e tempo para receber o primeiro byte do response (`response`). Mais preciso que um timeout único para toda a operação. |
| `response.body` | Propriedade do objeto `Response` do `fetch` que expõe o body como `ReadableStream`. Permite consumo incremental de payloads grandes sem carregar tudo na memória, via `getReader()` ou `pipeThrough()`. |
| thundering herd | Problema em retry sem jitter: múltiplos clientes que falham simultaneamente tentam novamente ao mesmo tempo, amplificando a carga no servidor. Resolvido adicionando aleatoriedade ao delay de retry (`jitter`). |
