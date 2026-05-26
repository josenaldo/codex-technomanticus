---
title: "gRPC com grpc-js"
created: 2026-05-12
updated: 2026-05-12
type: concept
status: growing
publish: true
tags:
  - node
  - grpc
  - rpc
  - integrações
aliases:
  - grpc-js
  - gRPC Node
  - Protobuf Node
---

# gRPC com grpc-js

> [!abstract] TL;DR
> **`@grpc/grpc-js`** é a implementação oficial de gRPC para [[Node.js]], escrita em JavaScript puro, sem binários nativos compilados — elimina a bagunça de `node-gyp` do legado `grpc` package. Contratos são definidos em arquivos `.proto` usando **Protocol Buffers (protobuf)** como IDL (Interface Definition Language); o `@grpc/proto-loader` carrega esses arquivos dinamicamente em runtime sem gerar código. O protocolo suporta **4 padrões de RPC**: unary (1 req → 1 resp), server streaming (1 req → N resps), client streaming (N reqs → 1 resp) e bidi streaming (N reqs → N resps). Credenciais são gerenciadas via `grpc.credentials`: `createInsecure()` para desenvolvimento e `createSsl()` para TLS mútuo em produção. Veja [[03-Dominios/Node/Integrações/index|Integrações]] para o contexto completo do galho.

## Como funciona

### Definição de serviço em `.proto` e carregamento dinâmico

O contrato entre cliente e servidor é definido num arquivo `.proto` usando a sintaxe **Protocol Buffers v3**. Esse arquivo descreve mensagens (tipos) e serviços (RPC methods).

Há duas formas de consumir o `.proto` em Node.js:

1. **Geração estática** — usa o compilador `protoc` com o plugin `ts-protoc-gen` (ou `grpc_tools_node_protoc_ts`) para gerar arquivos `.d.ts` e `.js` em tempo de build. Requer CI com `protoc` instalado, mas entrega type-safety total.
2. **Carregamento dinâmico** — usa `@grpc/proto-loader` para ler o `.proto` em runtime e gerar um service descriptor. É mais simples para projetos menores e não exige `protoc` local.

Em projetos TypeScript com monorepo, a abordagem estática é preferida. Em ferramentas internas ou POCs, o dinâmico é mais ágil.

### Servidor: `grpc.Server`, `addService` e credenciais

O servidor é criado com `new grpc.Server()`. Os serviços são registrados com `server.addService(serviceDefinition, implementation)`. O binding usa `server.bindAsync(address, credentials, callback)`.

As credenciais controlam segurança da conexão:

| Credencial | Uso |
|---|---|
| `grpc.ServerCredentials.createInsecure()` | Desenvolvimento local — sem TLS |
| `grpc.ServerCredentials.createSsl(rootCerts, [{ private_key, cert_chain }], true)` | Produção — TLS mútuo (mTLS) |

O endereço segue o formato `host:port`, com `0.0.0.0:50051` sendo o padrão para escutar em todas as interfaces.

### Os 4 tipos de RPC

| Tipo | Request | Response | Caso de uso |
|---|---|---|---|
| **Unary** | 1 | 1 | Busca de usuário, criação de recurso |
| **Server Streaming** | 1 | N (stream) | Logs em tempo real, listas grandes |
| **Client Streaming** | N (stream) | 1 | Upload de arquivo em chunks, agregação |
| **Bidi Streaming** | N (stream) | N (stream) | Chat, jogos multiplayer, telemetria bidirecional |

No **unary**, o handler recebe `(call, callback)` e invoca `callback(null, responseObj)`.

No **server streaming**, o handler recebe `call` como `ServerWritableStream`: usa `call.write(msg)` para cada chunk e `call.end()` ao terminar.

No **client streaming**, o handler recebe `call` como `ServerReadableStream`: escuta `call.on('data', ...)`, `call.on('end', ...)` e ao final chama `callback(null, responseObj)`.

No **bidi streaming**, o handler recebe `call` como `ServerDuplexStream`: combina `call.write()` + `call.on('data')` simultaneamente.

## Snippets de código

### Snippet 1 — Definição `.proto` com serviço Unary

```protobuf
syntax = "proto3";

package users;

// Mensagem de request
message GetUserRequest {
  string id = 1;
}

// Mensagem de response
message GetUserResponse {
  string id    = 1;
  string name  = 2;
  string email = 3;
}

// Mensagem para server streaming de logs
message LogEntry {
  string timestamp = 1;
  string level     = 2;
  string message   = 3;
}

message GetLogsRequest {
  string user_id   = 1;
  int32  last_n    = 2;
}

service UserService {
  // Unary
  rpc GetUser (GetUserRequest) returns (GetUserResponse);

  // Server streaming
  rpc StreamLogs (GetLogsRequest) returns (stream LogEntry);
}
```

### Snippet 2 — Servidor gRPC com proto-loader

```typescript
import * as grpc from "@grpc/grpc-js";
import * as protoLoader from "@grpc/proto-loader";
import path from "path";

const PROTO_PATH = path.resolve(__dirname, "./proto/users.proto");

const packageDef = protoLoader.loadSync(PROTO_PATH, {
  keepCase: true,
  longs: String,
  enums: String,
  defaults: true,
  oneofs: true,
});

const grpcObject = grpc.loadPackageDefinition(packageDef) as any;
const UserService = grpcObject.users.UserService;

// --- Handlers ---

function getUser(
  call: grpc.ServerUnaryCall<{ id: string }, { id: string; name: string; email: string }>,
  callback: grpc.sendUnaryData<{ id: string; name: string; email: string }>
): void {
  const { id } = call.request;

  // Simulate DB lookup — in production this would query your database
  const user: { id: string; name: string; email: string } | null =
    id === 'known-id' ? { id, name: 'Alice', email: 'alice@example.com' } : null;

  if (!user) {
    return callback({
      code: grpc.status.NOT_FOUND,
      message: `User ${id} not found`,
    });
  }

  callback(null, user);
}

function streamLogs(
  call: grpc.ServerWritableStream<{ user_id: string; last_n: number }, { timestamp: string; level: string; message: string }>
): void {
  const { user_id, last_n } = call.request;
  const logs = generateFakeLogs(user_id, last_n);

  for (const entry of logs) {
    call.write(entry);
  }

  call.end();
}

function generateFakeLogs(userId: string, n: number) {
  return Array.from({ length: n }, (_, i) => ({
    timestamp: new Date(Date.now() - i * 1000).toISOString(),
    level: i % 3 === 0 ? "WARN" : "INFO",
    message: `Log entry ${i} for user ${userId}`,
  }));
}

// --- Bootstrap ---

function main(): void {
  const server = new grpc.Server();

  server.addService(UserService.service, { getUser, streamLogs });

  server.bindAsync(
    "0.0.0.0:50051",
    grpc.ServerCredentials.createInsecure(), // TLS em produção
    (err, port) => {
      if (err) {
        console.error("Failed to bind server:", err);
        process.exit(1);
      }
      console.log(`gRPC server running on port ${port}`);
    }
  );
}

main();
```

### Snippet 3 — Cliente gRPC Unary com tratamento de erro

```typescript
import * as grpc from "@grpc/grpc-js";
import * as protoLoader from "@grpc/proto-loader";
import path from "path";

const PROTO_PATH = path.resolve(__dirname, "./proto/users.proto");

const packageDef = protoLoader.loadSync(PROTO_PATH, {
  keepCase: true,
  longs: String,
  enums: String,
  defaults: true,
  oneofs: true,
});

const grpcObject = grpc.loadPackageDefinition(packageDef) as any;

// Cria o stub — o canal é criado internamente
const client = new grpcObject.users.UserService(
  "localhost:50051",
  grpc.credentials.createInsecure()
);

// Wrapper com deadline e tratamento de erro tipado
function getUser(id: string): Promise<{ id: string; name: string; email: string }> {
  return new Promise((resolve, reject) => {
    const deadline = new Date(Date.now() + 5_000); // 5 segundos

    // import { randomUUID } from 'node:crypto'; // use this import for Node.js 18
    const metadata = new grpc.Metadata();
    metadata.add("x-request-id", crypto.randomUUID());

    client.getUser({ id }, metadata, { deadline }, (err: grpc.ServiceError | null, response: any) => {
      if (err) {
        if (err.code === grpc.status.NOT_FOUND) {
          return reject(new Error(`User not found: ${id}`));
        }
        if (err.code === grpc.status.DEADLINE_EXCEEDED) {
          return reject(new Error("gRPC call timed out"));
        }
        return reject(err);
      }
      resolve(response);
    });
  });
}

async function run(): Promise<void> {
  try {
    const user = await getUser("user-42");
    console.log("User:", user);
  } catch (err) {
    console.error("Error:", (err as Error).message);
  } finally {
    // Fechar o canal é OBRIGATÓRIO em aplicações de vida curta (scripts, lambdas)
    client.close();
  }
}

run();
```

### Snippet 4 — Server Streaming: cliente consome stream de logs

```typescript
import * as grpc from "@grpc/grpc-js";
import * as protoLoader from "@grpc/proto-loader";
import path from "path";

const PROTO_PATH = path.resolve(__dirname, "./proto/users.proto");
const packageDef = protoLoader.loadSync(PROTO_PATH, { keepCase: true, defaults: true });
const grpcObject = grpc.loadPackageDefinition(packageDef) as any;

const client = new grpcObject.users.UserService(
  "localhost:50051",
  grpc.credentials.createInsecure()
);

function streamUserLogs(userId: string, lastN: number): void {
  const deadline = new Date(Date.now() + 30_000); // 30s para streaming

  const call = client.streamLogs(
    { user_id: userId, last_n: lastN },
    { deadline }
  ) as grpc.ClientReadableStream<{ timestamp: string; level: string; message: string }>;

  call.on("data", (entry) => {
    console.log(`[${entry.timestamp}] ${entry.level}: ${entry.message}`);
  });

  call.on("end", () => {
    console.log("Stream finished.");
    client.close();
  });

  call.on("error", (err: grpc.ServiceError) => {
    if (err.code === grpc.status.DEADLINE_EXCEEDED) {
      console.error("Stream timed out after 30s");
    } else {
      console.error("Stream error:", err.message);
    }
    client.close();
  });
}

streamUserLogs("user-42", 10);
```

### Snippet 5 — Interceptor de cliente para bearer token

```typescript
import * as grpc from "@grpc/grpc-js";

// Um interceptor de cliente recebe (options, nextCall) e retorna um InterceptingCall
function bearerTokenInterceptor(token: string): grpc.Interceptor {
  return (options, nextCall) => {
    const requester: grpc.FullRequester = {
      start(metadata, listener, next) {
        // Injeta o header de autorização em TODA chamada feita por este canal
        metadata.add("authorization", `Bearer ${token}`);
        next(metadata, listener);
      },
      sendMessage(message, next) {
        next(message);
      },
      halfClose(next) {
        next();
      },
      cancel(next) {
        next();
      },
    };
    return new grpc.InterceptingCall(nextCall(options), requester);
  };
}

// Uso: injeta o interceptor no canal do cliente
function createAuthenticatedClient(address: string, token: string, ServiceStub: any) {
  return new ServiceStub(address, grpc.credentials.createInsecure(), {
    interceptors: [bearerTokenInterceptor(token)],
  });
}

// No lado do servidor, leia o token via call.metadata.get("authorization")
function getUser(call: grpc.ServerUnaryCall<any, any>, callback: grpc.sendUnaryData<any>): void {
  const authHeader = call.metadata.get("authorization")[0] as string;

  if (!authHeader?.startsWith("Bearer ")) {
    return callback({ code: grpc.status.UNAUTHENTICATED, message: "Missing bearer token" });
  }

  const token = authHeader.slice(7);
  // Validar token aqui (JWT.verify, etc.)
  callback(null, { id: "user-1", name: "Alice", email: "alice@example.com" });
}
```

## Armadilhas

> [!danger] Não usar TLS em produção
> Por padrão, `grpc.credentials.createInsecure()` trafega todos os dados **em texto plano** — incluindo payloads sensíveis e tokens de autenticação. Em produção, use `grpc.ServerCredentials.createSsl(rootCerts, [{ private_key: keyBuffer, cert_chain: certBuffer }], true)` no servidor e `grpc.credentials.createSsl(rootCerts, clientKey, clientCert)` no cliente. Considere **mTLS** (TLS mútuo) para autenticação bidirecional entre microserviços. Nunca use `createInsecure()` fora de rede local controlada ou localhost.

> [!warning] Código desatualizado após mudança no `.proto` (stale codegen)
> Se você usa geração estática com `protoc`, qualquer alteração no `.proto` exige regenerar os arquivos de código. É comum durante desenvolvimento esquecer de rodar o script de geração, resultando em clientes e servidores com contratos distintos — o erro manifesta como falha de serialização silenciosa ou campos `undefined`. Inclua a geração de código no pipeline de CI e trate os arquivos gerados como **artefatos de build** (não os commite, ou commite e falhe o CI quando diferirem). Com `proto-loader` dinâmico, o problema é menor mas o arquivo `.proto` ainda precisa estar sincronizado entre cliente e servidor.

> [!warning] Não tratar `DEADLINE_EXCEEDED`
> gRPC suporta **deadlines** (prazos absolutos), e toda chamada de produção deveria ter um. Sem deadline, uma requisição pendente pode travar indefinidamente — especialmente problemático em cascata de microserviços onde um serviço lento bloqueia outros. No cliente, passe sempre `{ deadline: new Date(Date.now() + N) }`. Trate `grpc.status.DEADLINE_EXCEEDED` explicitamente (retry com backoff, circuit breaker, fallback). No servidor, use `call.cancelled` para abortar processamento quando o cliente já desistiu.

> [!warning] Esquecer de fechar o canal do cliente (`client.close()`)
> O cliente gRPC mantém um canal persistente com connection pool. Em aplicações de longa duração (como servidores HTTP que fazem chamadas gRPC), o canal deve ser compartilhado como singleton. Em scripts, lambdas ou testes, `client.close()` deve ser chamado no `finally` — caso contrário o processo Node.js fica suspenso aguardando o canal fechar por timeout. Prefira encapsular o cliente num módulo que expõe `connect()` e `disconnect()` explícitos.

## Comparação: gRPC vs REST vs GraphQL

| Critério | gRPC | REST | GraphQL |
|---|---|---|---|
| **Acoplamento** | Alto (contrato `.proto` obrigatório) | Baixo (convenções HTTP) | Médio (schema GraphQL) |
| **Performance** | Alta (HTTP/2 + binário protobuf) | Média (HTTP/1.1 + JSON texto) | Média (HTTP/1.1 + JSON texto) |
| **Streaming** | Nativo (4 padrões) | SSE / WebSocket (ad-hoc) | Subscriptions (WebSocket) |
| **Browser support** | Limitado (requer grpc-web proxy) | Total | Total |
| **Quando usar** | Comunicação interna entre microserviços, latência crítica, streaming bidirecional | APIs públicas, integrações externas, CRUD simples | BFF para mobile/web com múltiplos recursos |

## Em entrevista

### What is the difference between gRPC and REST?

gRPC uses HTTP/2 as transport and Protocol Buffers as the serialization format, while REST typically uses HTTP/1.1 with JSON. This makes gRPC significantly more efficient in terms of bandwidth and latency: protobuf messages are binary and much smaller than equivalent JSON, and HTTP/2 allows multiplexing multiple calls over a single TCP connection. REST is a loose architectural style with no enforced contract, whereas gRPC is contract-first — both client and server must agree on the same `.proto` definition, which catches integration mismatches at compile time rather than at runtime. REST has universal browser support and is easier to debug with plain tools like `curl`, while gRPC requires specific tooling (like `grpcurl` or `grpcui`) and a proxy layer (grpc-web) for browser clients. Choose gRPC for internal microservice communication where performance and strong contracts matter; choose REST for public-facing APIs where broad compatibility is more important.

### When should you use streaming RPC instead of unary?

Use **server streaming** when the response is too large to fit in memory at once or when results arrive progressively — for example, exporting millions of database rows, tailing log files, or pushing real-time price updates to a client. Use **client streaming** when the client needs to send a large amount of data before the server can respond — file uploads split into chunks or aggregating sensor readings are good examples. Use **bidi streaming** when both sides need to communicate concurrently and independently — chat applications, collaborative editing, or interactive game sessions benefit from this pattern. Avoid streaming when unary is sufficient: streaming adds complexity to error handling, backpressure, and reconnection logic. Remember that each streaming RPC holds an open HTTP/2 stream; too many concurrent streams on a single channel can cause resource pressure, so set appropriate deadlines and respect server-side flow control.

### How do you version a protobuf schema without breaking changes?

Protocol Buffers are designed for forward and backward compatibility when you follow the rules. The most important rule is to **never reuse a field number** — even if you delete a field, mark it as `reserved` so it cannot be reused by future fields with different types. Adding new optional fields with new field numbers is always safe: old clients ignore unknown fields, and new clients see the default value (zero/empty/false) when talking to old servers. To remove a field, mark it `reserved` by both number and name to prevent accidental reuse. Breaking changes include renaming a field (field names matter in proto3 JSON mode), changing a field type incompatibly (e.g., `int32` to `string`), changing a field number, and removing a field without reserving its number. For service-level versioning, use package namespaces (`v1`, `v2`) in the proto package declaration and maintain both service versions in parallel during the deprecation window.

### How do you authenticate gRPC calls?

The idiomatic gRPC authentication mechanism uses **Metadata** — key-value pairs sent alongside the RPC call, similar to HTTP headers. The most common pattern is passing a `Bearer` JWT token in the `authorization` metadata key; the server extracts and validates it in every handler or in a server-side interceptor. On the client side, use a **client interceptor** to inject the token into metadata automatically for all outgoing calls — this keeps auth logic out of individual call sites. For service-to-service authentication in Kubernetes environments, **mTLS (mutual TLS)** is preferred: each service has its own certificate, and the TLS handshake itself authenticates both parties without application-level tokens. gRPC also supports Google's `CallCredentials` API, which integrates with OAuth2 and service account credentials when running on GCP. Always combine transport-level TLS with application-level token validation for defense in depth.

## Vocabulário

| Termo | Definição |
|---|---|
| **protobuf** | Protocol Buffers — formato binário de serialização criado pela Google, mais compacto e rápido que JSON; define tipos com fields numerados que permitem evolução de schema |
| **IDL** | Interface Definition Language — linguagem para descrever contratos de API de forma agnóstica à linguagem de programação; no gRPC o IDL é a sintaxe `.proto` |
| **Unary RPC** | Padrão de chamada clássico: um request, um response; equivalente a uma chamada de função remota normal |
| **Server Streaming** | O cliente envia um único request e o servidor responde com um stream de mensagens até chamar `end()`; útil para grandes conjuntos de dados ou atualizações em tempo real |
| **Client Streaming** | O cliente envia múltiplas mensagens em stream e o servidor responde com uma única mensagem ao final; útil para uploads e agregações |
| **Bidi Streaming** | Ambos cliente e servidor trocam streams independentes simultaneamente sobre a mesma conexão HTTP/2; viabiliza comunicação full-duplex como chat e telemetria interativa |
| **Channel** | Abstração de conexão HTTP/2 entre cliente e servidor; mantém connection pool e gerencia reconexão automática; deve ser compartilhado como singleton |
| **Stub** | Objeto gerado (ou dinâmico) no lado do cliente que expõe os métodos RPC como chamadas locais; esconde os detalhes de serialização e transporte |
| **Deadline** | Prazo absoluto (timestamp) até quando uma chamada deve completar; diferente de timeout (relativo); deve ser sempre definido em produção para evitar chamadas pendentes indefinidamente |
| **Metadata** | Pares chave-valor enviados fora do payload da mensagem (similar a headers HTTP); usados para autenticação, tracing, e informações de contexto |
| **Interceptor** | Middleware que envolve chamadas gRPC no cliente ou servidor; permite injetar lógica transversal como autenticação, logging, métricas e retry sem modificar os handlers |
| **proto-loader** | Pacote `@grpc/proto-loader` que carrega arquivos `.proto` dinamicamente em runtime, sem necessidade de compilação prévia com `protoc`; retorna um `PackageDefinition` usado com `grpc.loadPackageDefinition()` |

## Veja também

- [[03-Dominios/Node/Integrações/index|Integrações]]
- [[Node.js]]
- [gRPC Node.js — documentação oficial](https://grpc.io/docs/languages/node/)
- [grpc-js no GitHub (googleapis/grpc-node)](https://github.com/grpc/grpc-node/tree/master/packages/grpc-js)
- [Protocol Buffers Language Guide (proto3)](https://protobuf.dev/programming-guides/proto3/)
