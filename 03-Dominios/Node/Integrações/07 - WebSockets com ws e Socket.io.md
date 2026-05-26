---
title: "WebSockets com ws e Socket.io"
created: 2026-05-12
updated: 2026-05-12
type: concept
status: growing
publish: true
tags:
  - node
  - websockets
  - realtime
  - integrações
aliases:
  - ws Node
  - Socket.io Node
  - WebSocket Node
---

# WebSockets com ws e Socket.io

> [!abstract] TL;DR
> **`ws`** é a biblioteca WebSocket minimalista do ecossistema Node.js: protocolo puro RFC 6455, sem abstrações de alto nível, sem fallback — ideal quando você quer controle total sobre frames e precisa de performance máxima em ambientes que garantem suporte a WebSocket. **Socket.io v4** adiciona uma camada de protocolo própria sobre WebSocket com fallback automático para HTTP Long Polling (útil em ambientes com proxy/load balancer que não suportam upgrade), além de rooms, namespaces e acknowledgements nativos. O padrão de **heartbeat/ping-pong** é essencial em ambos: clientes que caem silenciosamente (zumbis) precisam ser detectados e removidos para evitar leak de memória. Para **escalamento horizontal**, Socket.io requer um adapter compartilhado — o `@socket.io/redis-adapter` é o padrão de produção, garantindo que eventos emitidos em um pod cheguem a clientes conectados em outros pods. Veja [[03-Dominios/Node/Integrações/index|Integrações]] para o contexto completo do galho.

## Como funciona

### Handshake HTTP → Upgrade para WebSocket e ciclo de vida da conexão

O protocolo WebSocket começa como uma requisição HTTP comum. O cliente envia um `GET` com os headers `Upgrade: websocket` e `Connection: Upgrade`, além de `Sec-WebSocket-Key` (nonce base64 aleatório). O servidor responde com `101 Switching Protocols`, calculando `Sec-WebSocket-Accept` como SHA-1(`key + GUID`). A partir desse momento, a conexão TCP subjacente é promovida: o protocolo HTTP sai de cena e os dois lados trocam **frames** binários ou texto diretamente.

O ciclo de vida de uma conexão WebSocket tem quatro eventos principais:

| Evento | Descrição |
|---|---|
| `open` | Handshake concluído; canal bidirecional estabelecido |
| `message` | Frame recebido do outro lado |
| `ping` / `pong` | Heartbeat — detecta clientes silenciosamente desconectados |
| `close` | Conexão encerrada (código + razão disponíveis) |
| `error` | Erro de rede ou protocolo; sempre precede `close` |

O fato de o WebSocket reutilizar a porta 80/443 e iniciar com HTTP significa que firewalls e proxies reversos comuns (Nginx, AWS ALB) suportam nativamente o upgrade — desde que configurados com `proxy_http_version 1.1` e `proxy_set_header Upgrade $http_upgrade` no Nginx.

### `ws.Server` e `ws.WebSocket` — broadcast pattern

A biblioteca `ws` expõe duas classes principais: `WebSocketServer` (o servidor) e `WebSocket` (instâncias de cliente). O servidor mantém um `Set` de clientes ativos em `wss.clients`. O padrão de **broadcast** itera esse conjunto e filtra clientes cujo `readyState` seja `OPEN`:

```typescript
import { WebSocketServer, WebSocket } from 'ws';

const wss = new WebSocketServer({ port: 8080 });

wss.on('connection', (ws: WebSocket) => {
  ws.on('message', (data: Buffer | string) => {
    // Broadcast para todos os clientes conectados
    for (const client of wss.clients) {
      if (client !== ws && client.readyState === WebSocket.OPEN) {
        client.send(data.toString());
      }
    }
  });

  ws.on('close', () => {
    console.log('Client disconnected. Total clients:', wss.clients.size);
  });

  ws.send(JSON.stringify({ type: 'welcome', message: 'Connected to ws server' }));
});

console.log('WebSocket server running on ws://localhost:8080');
```

A `ws` não tem salas, namespaces ou acknowledgements — você os implementa na camada de aplicação usando um `Map<string, Set<WebSocket>>` ou delegando para Socket.io.

### Socket.io `Server` e `Socket` — rooms, namespaces e acknowledgements

O Socket.io adiciona um protocolo de aplicação sobre WebSocket (ou Long Polling). Cada `Socket` representa uma conexão de um cliente. Os **namespaces** são canais lógicos dentro do mesmo servidor (`/chat`, `/notifications`) — clientes se conectam a um namespace específico. As **rooms** são grupos dentro de um namespace — um socket pode entrar em múltiplas rooms com `socket.join(room)` e emitir para todos os membros com `socket.to(room).emit(event, data)`.

Os **acknowledgements** são callbacks que o emissor passa junto ao `emit`. O receptor invoca esse callback quando conclui o processamento, confirmando a entrega de ponta a ponta. Isso não é nativo ao protocolo WebSocket — é uma abstração do protocolo Socket.io construída sobre o canal de mensagens.

```
socket.emit('event', data, (ack) => { ... })
   ↓
servidor recebe evento
   ↓
servidor chama callback(responseData)
   ↓
cliente recebe responseData no callback
```

A diferença crítica: Socket.io **não é** WebSocket puro. Um cliente WebSocket nativo não consegue conectar a um servidor Socket.io sem a biblioteca cliente correspondente, porque o protocolo de handshake customizado (`EIO=4`) não é HTTP WebSocket padrão.

## Snippets

### Snippet 1 — Servidor WebSocket com `ws` e broadcast

```typescript
import { WebSocketServer, WebSocket, RawData } from 'ws';
import http from 'http';

interface BroadcastMessage {
  type: string;
  payload: unknown;
  from?: string;
}

const server = http.createServer();
const wss = new WebSocketServer({ server });

function broadcast(sender: WebSocket, message: BroadcastMessage): void {
  const serialized = JSON.stringify(message);
  for (const client of wss.clients) {
    if (client !== sender && client.readyState === WebSocket.OPEN) {
      client.send(serialized);
    }
  }
}

wss.on('connection', (ws: WebSocket, req: http.IncomingMessage) => {
  const clientIp = req.socket.remoteAddress ?? 'unknown';
  console.log(`New connection from ${clientIp}. Total: ${wss.clients.size}`);

  ws.send(JSON.stringify({ type: 'welcome', payload: { total: wss.clients.size } }));

  ws.on('message', (data: RawData) => {
    try {
      const parsed: BroadcastMessage = JSON.parse(data.toString());
      broadcast(ws, { ...parsed, from: clientIp });
    } catch {
      ws.send(JSON.stringify({ type: 'error', payload: 'Invalid JSON' }));
    }
  });

  ws.on('close', (code: number, reason: Buffer) => {
    console.log(`Client disconnected: code=${code} reason=${reason.toString()}`);
    broadcast(ws, { type: 'system', payload: `${clientIp} left` });
  });

  ws.on('error', (err: Error) => {
    console.error(`WebSocket error for ${clientIp}:`, err.message);
  });
});

server.listen(8080, () => {
  console.log('HTTP + WebSocket server on port 8080');
});
```

### Snippet 2 — Heartbeat com `ping`/`pong` e detecção de clientes zumbis

```typescript
import { WebSocketServer, WebSocket } from 'ws';

// Extende WebSocket para rastrear se o cliente ainda está vivo
interface AliveSocket extends WebSocket {
  isAlive: boolean;
}

const wss = new WebSocketServer({ port: 8080 });

const HEARTBEAT_INTERVAL_MS = 30_000; // 30 segundos

wss.on('connection', (ws: WebSocket) => {
  const socket = ws as AliveSocket;
  socket.isAlive = true;

  // Quando o cliente responde ao ping com pong, marca como vivo
  socket.on('pong', () => {
    socket.isAlive = true;
  });

  socket.on('message', (data) => {
    console.log('Received:', data.toString());
  });
});

// Ciclo de heartbeat: a cada HEARTBEAT_INTERVAL_MS, faz ping em todos os clientes
const heartbeat = setInterval(() => {
  for (const rawClient of wss.clients) {
    const client = rawClient as AliveSocket;

    if (!client.isAlive) {
      // Cliente não respondeu ao ping anterior — terminar conexão
      console.warn('Terminating zombie client');
      client.terminate(); // fecha sem handshake de close — libera recursos imediatamente
      continue;
    }

    // Marca como potencialmente morto; espera pong para remarcar como vivo
    client.isAlive = false;
    client.ping(); // envia frame ping; cliente WebSocket padrão responde automaticamente com pong
  }
}, HEARTBEAT_INTERVAL_MS);

wss.on('close', () => {
  clearInterval(heartbeat);
});

console.log('WebSocket server with heartbeat on port 8080');
```

### Snippet 3 — Socket.io com rooms e `socket.to(room).emit()`

```typescript
import { createServer } from 'http';
import { Server, Socket } from 'socket.io';

interface ServerToClientEvents {
  message: (data: { text: string; from: string; room: string }) => void;
  notification: (data: { text: string }) => void;
  userJoined: (data: { userId: string; room: string }) => void;
  userLeft: (data: { userId: string; room: string }) => void;
}

interface ClientToServerEvents {
  joinRoom: (room: string) => void;
  leaveRoom: (room: string) => void;
  sendMessage: (data: { room: string; text: string }) => void;
}

interface InterServerEvents {
  ping: () => void;
}

interface SocketData {
  userId: string;
}

const httpServer = createServer();
const io = new Server<
  ClientToServerEvents,
  ServerToClientEvents,
  InterServerEvents,
  SocketData
>(httpServer, {
  cors: { origin: '*' },
});

io.on('connection', (socket: Socket<ClientToServerEvents, ServerToClientEvents, InterServerEvents, SocketData>) => {
  const userId = socket.handshake.auth.userId ?? socket.id;
  socket.data.userId = userId;

  console.log(`Socket connected: ${socket.id} (user: ${userId})`);

  socket.on('joinRoom', (room: string) => {
    socket.join(room);
    // Emite para todos no room EXCETO o próprio socket
    socket.to(room).emit('userJoined', { userId, room });
    // Emite somente para o socket que fez join (confirmação)
    socket.emit('notification', { text: `You joined room: ${room}` });
    console.log(`${userId} joined room: ${room}`);
  });

  socket.on('leaveRoom', (room: string) => {
    socket.leave(room);
    socket.to(room).emit('userLeft', { userId, room });
  });

  socket.on('sendMessage', ({ room, text }) => {
    // Emite para todos no room incluindo o remetente
    io.to(room).emit('message', { text, from: userId, room });
  });

  socket.on('disconnect', (reason) => {
    console.log(`Socket disconnected: ${socket.id} reason=${reason}`);
  });
});

httpServer.listen(3000, () => {
  console.log('Socket.io server running on http://localhost:3000');
});
```

### Snippet 4 — Socket.io com acknowledgements

```typescript
import { createServer } from 'http';
import { Server, Socket } from 'socket.io';

interface ServerToClientEvents {
  newOrder: (order: { id: string; items: string[]; total: number }) => void;
}

interface ClientToServerEvents {
  createOrder: (
    payload: { items: string[]; total: number },
    callback: (response: { orderId: string; status: string }) => void
  ) => void;
}

const httpServer = createServer();
const io = new Server<ClientToServerEvents, ServerToClientEvents>(httpServer);

io.on('connection', (socket: Socket<ClientToServerEvents, ServerToClientEvents>) => {
  // Cliente envia 'createOrder' com um callback — servidor processa e invoca o callback
  socket.on('createOrder', async (payload, callback) => {
    try {
      // Simula persistência do pedido
      const orderId = `order_${Date.now()}`;
      console.log(`Creating order ${orderId}:`, payload);

      // Invoca o callback do cliente com a resposta
      // O cliente só chama o callback quando o servidor invoca esta função
      callback({ orderId, status: 'created' });

      // Notifica outros clientes sobre o novo pedido
      // broadcast.emit NÃO suporta ack — use io.timeout().emit() se precisar de confirmação
      socket.broadcast.emit('newOrder', { id: orderId, ...payload });
    } catch (err) {
      // Em caso de erro, invoca o callback com status de erro
      callback({ orderId: '', status: 'error' });
    }
  });
});

// Exemplo de como o CLIENTE usaria o acknowledgement:
// socket.emit('createOrder', { items: ['pizza'], total: 45.90 }, (response) => {
//   if (response.status === 'created') {
//     console.log('Order confirmed:', response.orderId);
//   }
// });

httpServer.listen(3000);
```

### Snippet 5 — Socket.io com Redis adapter para escalamento horizontal

```typescript
import { createServer } from 'http';
import { Server } from 'socket.io';
import { createAdapter } from '@socket.io/redis-adapter';
import { createClient, RedisClientType } from 'redis';

async function bootstrap(): Promise<void> {
  const httpServer = createServer();
  const io = new Server(httpServer, {
    cors: { origin: '*' },
    // Configura Long Polling como fallback — necessário quando o load balancer
    // não suporta sticky sessions e o cliente pode reconectar em um pod diferente
    transports: ['websocket', 'polling'],
  });

  // Cria dois clientes Redis: pubClient (publica) e subClient (subscreve)
  // O Redis Adapter usa pub/sub do Redis para sincronizar eventos entre pods
  const pubClient: RedisClientType = createClient({
    url: process.env.REDIS_URL ?? 'redis://localhost:6379',
  });

  // subClient deve ser uma cópia do pubClient — não reutilize a mesma instância
  const subClient: RedisClientType = pubClient.duplicate();

  // Conecta ambos antes de configurar o adapter
  await Promise.all([pubClient.connect(), subClient.connect()]);

  // Configura o adapter: a partir daqui, io.emit() e io.to(room).emit()
  // publicam via Redis e chegam a TODOS os pods
  io.adapter(createAdapter(pubClient, subClient));

  io.on('connection', (socket) => {
    socket.on('joinRoom', (room: string) => {
      socket.join(room);
    });

    socket.on('broadcast', (data: { room: string; message: string }) => {
      // Este emit vai via Redis para todos os pods — funciona mesmo em cluster
      io.to(data.room).emit('message', data.message);
    });

    socket.on('disconnect', () => {
      console.log(`Disconnected: ${socket.id}`);
    });
  });

  // Graceful shutdown
  process.on('SIGTERM', async () => {
    io.close();
    await pubClient.quit();
    await subClient.quit();
  });

  httpServer.listen(Number(process.env.PORT) || 3000, () => {
    console.log(`Socket.io pod running on port ${process.env.PORT || 3000}`);
  });
}

bootstrap().catch(console.error);
```

## Armadilhas

> [!danger] Não implementar heartbeat em `ws` — clientes zumbis acumulam
> A biblioteca `ws` não tem heartbeat automático. Quando um cliente perde conectividade de rede abruptamente (queda de Wi-Fi, reinicialização de roteador), o servidor **não recebe** o evento `close`. O socket fica no `Set` `wss.clients` com `readyState = OPEN` indefinidamente. Em produção com centenas de conexões concorrentes, isso é um leak de memória garantido. **Solução**: implemente o ciclo de `ping`/`pong` como mostrado no Snippet 2. O Socket.io tem heartbeat automático configurável via `pingInterval` e `pingTimeout`.

> [!danger] Escalar horizontalmente sem adapter — mensagens não chegam em outros pods
> Por padrão, o Socket.io mantém o estado de rooms e sockets **em memória no processo**. Se você tiver 3 pods e um cliente conectado ao Pod A emitir para uma room, apenas os clientes no Pod A vão receber. Clientes no Pod B e C não existem na visão do Pod A. **Solução**: configure o `@socket.io/redis-adapter` antes de aceitar conexões. Sem isso, sticky sessions no load balancer são um paliativo parcial — resolve o mesmo cliente, mas não o fanout para outras conexões.

> [!warning] Não autenticar na fase de handshake — autenticar em cada mensagem é ineficiente
> Um erro comum é validar o JWT apenas nos eventos de mensagem. Isso significa que conexões não autenticadas ficam estabelecidas consumindo recursos até enviarem o primeiro evento. **Solução**: use o middleware de conexão do Socket.io (`io.use((socket, next) => { ... })`) ou o evento `upgrade` do `ws` para validar o token antes de aceitar a conexão. No `ws`, inspecione `req.headers.authorization` no handler de `upgrade` do servidor HTTP antes de promover para WebSocket.

> [!warning] Enviar payloads grandes via WebSocket sem chunking
> WebSocket não fragmenta automaticamente payloads na camada de aplicação da mesma forma que HTTP. Enviar um blob de 50MB em um único `send()` bloqueia o canal do socket durante a serialização e pode acionar limites de tamanho de frame do lado do cliente ou do servidor. **Solução**: para payloads grandes, use chunking manual com uma sequência de frames menores (ex: `{ chunk: number, total: number, data: string }`), ou reconsidere se WebSocket é o canal certo — objetos grandes geralmente são melhor servidos via HTTP com streaming (`Content-Type: application/octet-stream`).

## Comparativo: `ws` vs Socket.io vs SSE

| Critério | `ws` | Socket.io | SSE (Server-Sent Events) |
|---|---|---|---|
| **Fallback HTTP** | Nenhum — WebSocket ou falha | HTTP Long Polling automático | HTTP nativo — funciona em todo browser |
| **Bidirecional** | Sim — full-duplex | Sim — full-duplex | Não — servidor → cliente apenas |
| **Complexidade** | Baixa — protocolo puro | Média — protocolo próprio + libs cliente/servidor | Baixa — `EventSource` nativo no browser |
| **Rooms/namespaces** | Manual (você implementa) | Nativo — `socket.join()`, `/namespace` | Não aplicável |
| **Acknowledgements** | Manual | Nativo — callback no `emit()` | Não aplicável |
| **Escalamento** | Manual (você sincroniza via Redis pub/sub) | `@socket.io/redis-adapter` | Stateless — qualquer pod responde |
| **Quando usar** | Protocolo puro, máxima performance, controle total de frame | Produto com rooms, reconnect automático, fallback necessário | Notificações push, feeds de eventos unidirecionais |

## Em entrevista

### What is the difference between WebSocket and SSE (Server-Sent Events)?

WebSocket is a full-duplex protocol that allows both the client and the server to send messages at any time over a single persistent TCP connection. SSE (Server-Sent Events) is a unidirectional channel built on top of plain HTTP: the server streams events to the client, but the client cannot push data back through the same connection. WebSocket requires an HTTP Upgrade handshake (101 Switching Protocols) and a dedicated protocol framing layer, while SSE is simply a long-lived HTTP response with `Content-Type: text/event-stream`. For use cases like live score updates, stock tickers, or notification feeds — where the server pushes data and the client only listens — SSE is simpler, works through standard HTTP proxies without extra configuration, and leverages HTTP/2 multiplexing for free. For chat, collaborative editing, or any scenario where the client also sends frequent messages, WebSocket is the correct choice because SSE would require a separate HTTP request for each client-to-server message, negating the benefit of a persistent connection.

### How would you scale Socket.io horizontally across multiple pods?

By default, Socket.io stores all room memberships and socket state in memory within the process, which means a message emitted on Pod A only reaches clients connected to Pod A. To scale horizontally, you replace the default in-memory adapter with a distributed adapter backed by a shared message broker. The `@socket.io/redis-adapter` is the standard production choice: it uses Redis Pub/Sub so that when one pod calls `io.to(room).emit()`, the message is published to a Redis channel and all other pods subscribed to that channel deliver it to their locally connected clients. You instantiate a `pubClient` and a `subClient` (a duplicate of the same Redis connection — they cannot share a single client because a subscribed Redis connection cannot issue other commands), connect both, and call `io.adapter(createAdapter(pubClient, subClient))` before the server starts accepting connections. An important complementary concern is the HTTP Long Polling fallback: if your load balancer does not use sticky sessions, a client's polling requests may hit different pods during the handshake negotiation phase, causing 400 errors. Either configure sticky sessions or enforce `transports: ['websocket']` to skip polling entirely, which is safe in modern environments that support WebSocket.

### How do you authenticate WebSocket connections?

The recommended approach is to validate credentials at the handshake phase rather than on every message, which would be both inefficient and insecure. In Socket.io, you use the `io.use()` middleware: it receives the socket and a `next` function before the connection is fully established, so you can inspect `socket.handshake.auth.token`, verify the JWT, attach the decoded user to `socket.data`, and call `next(new Error('unauthorized'))` to reject invalid connections. In plain `ws`, you intercept the HTTP Upgrade request by passing a `handleProtocols` function or by hooking into the `upgrade` event on the underlying `http.Server` — inspect `req.headers.authorization` or a query parameter (for clients that cannot set custom headers, such as browser `WebSocket`), validate the token, and call `socket.destroy()` before the upgrade completes if the token is invalid. Never authenticate only on the first message after connection: a rejected connection at the handshake releases the TCP socket immediately and prevents the unauthenticated client from consuming server resources or receiving events intended for other users.

### When would you prefer `ws` over Socket.io?

You should prefer `ws` over Socket.io when you need to interoperate with clients that implement the WebSocket protocol natively — IoT devices, mobile SDKs, or other servers — because Socket.io uses its own framing protocol and a native WebSocket client cannot connect to a Socket.io server without the Socket.io client library. `ws` is also the better choice when you need maximum throughput and minimum overhead: there is no abstraction layer, no heartbeat negotiation overhead from Socket.io's engine, and no binary protocol translation. In microservices that communicate server-to-server over WebSocket (for example, a streaming data pipeline between internal services), `ws` is leaner and easier to reason about. Finally, if you are building a custom real-time protocol with your own application-level framing, rooms, and fan-out logic, starting with `ws` gives you a clean foundation without inheriting Socket.io's architectural decisions around namespaces and rooms, which may not map to your domain.

## Vocabulário

| Termo | Definição |
|---|---|
| **WebSocket** | Protocolo de comunicação full-duplex sobre TCP, iniciado via HTTP Upgrade (RFC 6455); mantém conexão persistente para troca bidirecional de mensagens em tempo real |
| **handshake** | Negociação inicial entre cliente e servidor para estabelecer o canal WebSocket; o cliente envia `Upgrade: websocket` e o servidor responde com `101 Switching Protocols` |
| **upgrade** | Header HTTP `Upgrade: websocket` que solicita a promoção da conexão HTTP para o protocolo WebSocket; o servidor confirma com `Connection: Upgrade` |
| **heartbeat** | Mecanismo periódico para verificar se uma conexão ainda está ativa; no WebSocket, implementado via frames `ping`/`pong` |
| **ping/pong** | Par de frames de controle do protocolo WebSocket: o servidor envia `ping`, o cliente responde automaticamente com `pong`; ausência de pong indica cliente zumbi |
| **room** | Agrupamento lógico de sockets no Socket.io dentro de um namespace; um socket pode estar em múltiplas rooms simultaneamente via `socket.join()` |
| **namespace** | Canal lógico isolado dentro de um servidor Socket.io (ex: `/chat`, `/admin`); cada namespace tem seus próprios eventos e rooms, permitindo separação de contextos |
| **acknowledgement** | Mecanismo do Socket.io onde o emissor passa um callback junto ao `emit()`; o receptor invoca o callback quando termina o processamento, confirmando a entrega ponta-a-ponta |
| **Redis adapter** | `@socket.io/redis-adapter` — substitui o adapter in-memory padrão do Socket.io por um que usa Redis Pub/Sub para sincronizar eventos entre múltiplos pods/processos |
| **fallback** | Mecanismo do Socket.io para degradar graciosamente de WebSocket para HTTP Long Polling quando o ambiente não suporta o Upgrade (proxies, load balancers legados) |
| **long polling** | Técnica HTTP onde o cliente faz uma requisição e o servidor a mantém aberta até ter dados para enviar; simula push server-to-client sobre HTTP puro |
| **SSE** | Server-Sent Events — API HTTP nativa para streaming unidirecional servidor → cliente (`Content-Type: text/event-stream`); simples, stateless, não requer biblioteca extra |

## Veja também

- [[03-Dominios/Node/Integrações/index|Integrações]]
- [[Node.js]]
- [ws — documentação oficial](https://github.com/websockets/ws/blob/master/README.md)
- [Socket.io — documentação oficial](https://socket.io/docs/v4/)
- [Socket.io Redis Adapter](https://socket.io/docs/v4/redis-adapter/)
- [[03-Dominios/Node/Integrações/06 - GraphQL com Apollo Server e Mercurius]] — subscriptions GraphQL via WebSocket
- [[03-Dominios/Node/Integrações/08 - Clientes HTTP - fetch, axios, got e undici]] — clientes HTTP para comparação com SSE
