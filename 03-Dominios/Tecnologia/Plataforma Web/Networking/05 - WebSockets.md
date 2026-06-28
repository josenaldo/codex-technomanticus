---
title: "WebSockets"
created: 2026-06-28
updated: 2026-06-28
type: note
fase: Adepto
tags:
  - plataforma-web
  - networking
  - browser
  - javascript
  - websocket
  - entrevista
publish: true
---

# WebSockets

> [!abstract] TL;DR
> WebSocket é um protocolo bidirecional full-duplex que começa como HTTP e faz upgrade para WS. Diferente do SSE (só servidor→cliente), WebSocket permite que ambos os lados enviem a qualquer momento — essencial para chat, jogos, edição colaborativa, dashboards em tempo real. A conexão é persistente; o cliente deve implementar reconexão manual com backoff.

---

## WebSocket básico

```javascript
// Criar conexão
const ws = new WebSocket('wss://api.exemplo.com/ws');
// 'wss://' = WebSocket seguro (TLS) — use sempre em produção
// 'ws://' = sem TLS — só em localhost

// Estados
ws.readyState; // WebSocket.CONNECTING (0) | OPEN (1) | CLOSING (2) | CLOSED (3)

// Eventos
ws.onopen = (event) => {
  console.log('Conectado!');
  ws.send('Olá servidor!'); // só enviar quando conectado
};

ws.onmessage = (event) => {
  const data = event.data; // string ou Blob ou ArrayBuffer
  
  if (typeof data === 'string') {
    const message = JSON.parse(data);
    handleMessage(message);
  }
};

ws.onerror = (event) => {
  console.error('Erro WebSocket'); // poucos detalhes por segurança
};

ws.onclose = (event) => {
  event.code;     // código numérico (1000 = fechamento normal, 1006 = anormal)
  event.reason;   // string da razão
  event.wasClean; // boolean
};

// Enviar dados
ws.send('texto simples');
ws.send(JSON.stringify({ type: 'message', text: 'Olá!' }));
ws.send(new Blob([data]));         // binário
ws.send(new ArrayBuffer(16));      // binário

// Fechar graciosamente
ws.close(1000, 'Usuário saiu'); // (code, reason)
```

---

## Reconexão automática

WebSocket não reconecta automaticamente — o cliente deve implementar isso:

```javascript
class ReconnectingWebSocket {
  constructor(url, options = {}) {
    this.url = url;
    this.reconnectDelay = options.reconnectDelay ?? 1000;
    this.maxDelay = options.maxDelay ?? 30000;
    this.onmessage = options.onmessage ?? (() => {});
    this.onopen = options.onopen ?? (() => {});
    this.onclose = options.onclose ?? (() => {});
    
    this._currentDelay = this.reconnectDelay;
    this._intentionalClose = false;
    this.connect();
  }

  connect() {
    this._ws = new WebSocket(this.url);
    
    this._ws.onopen = (event) => {
      this._currentDelay = this.reconnectDelay; // reset backoff
      this.onopen(event);
    };
    
    this._ws.onmessage = this.onmessage;
    
    this._ws.onclose = (event) => {
      this.onclose(event);
      
      if (!this._intentionalClose) {
        console.log(`Reconectando em ${this._currentDelay}ms...`);
        setTimeout(() => this.connect(), this._currentDelay);
        
        // Backoff exponencial
        this._currentDelay = Math.min(this._currentDelay * 2, this.maxDelay);
      }
    };
  }

  send(data) {
    if (this._ws.readyState === WebSocket.OPEN) {
      this._ws.send(typeof data === 'object' ? JSON.stringify(data) : data);
    } else {
      console.warn('WebSocket não está aberto');
    }
  }

  close() {
    this._intentionalClose = true;
    this._ws.close(1000, 'Client closed');
  }
}

// Uso
const ws = new ReconnectingWebSocket('wss://api.exemplo.com/ws', {
  onmessage: (event) => handleMessage(JSON.parse(event.data)),
  onopen: () => console.log('Conectado'),
});
```

---

## Protocolo de mensagens: padrão action/type

```javascript
// Convenção para mensagens tipadas
const MESSAGES = {
  // Tipos enviados pelo cliente
  CLIENT: {
    JOIN_ROOM: 'join-room',
    LEAVE_ROOM: 'leave-room',
    SEND_MESSAGE: 'send-message',
    TYPING: 'typing',
  },
  // Tipos enviados pelo servidor
  SERVER: {
    USER_JOINED: 'user-joined',
    USER_LEFT: 'user-left',
    NEW_MESSAGE: 'new-message',
    TYPING: 'typing',
    ERROR: 'error',
  },
};

// Cliente
ws.send(JSON.stringify({
  type: MESSAGES.CLIENT.JOIN_ROOM,
  roomId: 'general',
}));

// Servidor
ws.onmessage = (event) => {
  const { type, ...payload } = JSON.parse(event.data);
  
  switch (type) {
    case MESSAGES.SERVER.NEW_MESSAGE:
      renderMessage(payload);
      break;
    case MESSAGES.SERVER.USER_JOINED:
      addUserToList(payload.user);
      break;
    case MESSAGES.SERVER.ERROR:
      showError(payload.message);
      break;
  }
};
```

---

## Heartbeat — manter conexão viva

Algumas infraestruturas (load balancers, firewalls) fecham conexões idle:

```javascript
function setupHeartbeat(ws, intervalMs = 30000) {
  const pingInterval = setInterval(() => {
    if (ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({ type: 'ping' }));
    }
  }, intervalMs);
  
  ws.onclose = () => clearInterval(pingInterval);
  
  return () => clearInterval(pingInterval); // cleanup
}

// Servidor deve responder com pong
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  if (data.type === 'ping') {
    ws.send(JSON.stringify({ type: 'pong' }));
  }
};
```

---

## WebSocket com autenticação

WebSocket não suporta headers customizados no handshake (limitação do browser):

```javascript
// Opção 1: Token na query string (cuidado: fica em logs de servidor)
const ws = new WebSocket(`wss://api.exemplo.com/ws?token=${token}`);

// Opção 2: Cookie (automático se HttpOnly + SameSite configurado)
// O browser envia cookies no handshake de upgrade

// Opção 3: Enviar token como primeira mensagem após conexão
const ws = new WebSocket('wss://api.exemplo.com/ws');
ws.onopen = () => {
  ws.send(JSON.stringify({ type: 'auth', token }));
};
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  if (data.type === 'auth-success') {
    startNormalOperation();
  } else if (data.type === 'auth-failed') {
    ws.close();
    redirectToLogin();
  }
};
```

---

## Binário via WebSocket

```javascript
// Configurar para receber como ArrayBuffer (default: 'blob')
ws.binaryType = 'arraybuffer';

ws.onmessage = (event) => {
  if (event.data instanceof ArrayBuffer) {
    const view = new DataView(event.data);
    const messageType = view.getUint8(0); // primeiro byte = tipo
    const payload = new Uint8Array(event.data, 1); // resto = payload
    
    processeBinaryMessage(messageType, payload);
  }
};

// Enviar binário
const buffer = new ArrayBuffer(4);
const view = new DataView(buffer);
view.setUint8(0, 1);    // tipo: 1
view.setFloat32(1, 3.14); // dado
ws.send(buffer);
```

---

> [!question] Para fixar
> 1. Por que WebSocket é bidirecional enquanto SSE não é?
> 2. O que é `readyState`? Quais os 4 valores possíveis?
> 3. Por que WebSocket não reconecta automaticamente? Como você implementaria isso?
> 4. Como você autenticaria uma conexão WebSocket se não pode enviar headers no handshake?
> 5. O que o heartbeat resolve? Por que load balancers fecham conexões idle?

---

## Veja também

- [[03-Dominios/Tecnologia/Plataforma Web/Networking/04 - Streams e SSE|04 — Streams e SSE]] — anterior; comparativo SSE vs WebSocket
- [[03-Dominios/Tecnologia/Plataforma Web/Networking/06 - AbortController e cancelamento|06 — AbortController]] — próxima
- [[03-Dominios/Tecnologia/Plataforma Web/Workers/02 - SharedWorker e BroadcastChannel|Workers 02 — SharedWorker]] — WebSocket compartilhado entre abas
