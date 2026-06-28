---
title: "SharedWorker e BroadcastChannel"
created: 2026-06-28
updated: 2026-06-28
type: note
fase: Iniciado
tags:
  - plataforma-web
  - workers
  - browser
  - javascript
  - comunicacao
  - entrevista
publish: true
---

# SharedWorker e BroadcastChannel

> [!abstract] TL;DR
> `SharedWorker` é um worker compartilhado entre múltiplas abas e iframes da mesma origem — ideal para centralizar estado ou WebSockets (um só socket para todas as abas). `BroadcastChannel` é mais simples: permite broadcast de mensagens entre contextos da mesma origem sem um intermediário. Para sincronização simples entre abas, BroadcastChannel; para lógica centralizada, SharedWorker.

---

## SharedWorker

Enquanto um Web Worker comum é exclusivo de uma aba, um SharedWorker é compartilhado entre todas as abas da mesma origem que o criarem com o mesmo URL.

```javascript
// main.js (em cada aba)
const worker = new SharedWorker('/shared-worker.js');

// SharedWorker usa port para comunicação (diferente do postMessage direto)
worker.port.start();

// Enviar mensagem
worker.port.postMessage({ type: 'GREET', name: 'Alice' });

// Receber mensagem
worker.port.onmessage = (event) => {
  console.log('Resposta do shared worker:', event.data);
};

// Alternativa: addEventListener
worker.port.addEventListener('message', (event) => {
  console.log(event.data);
});
worker.port.start(); // obrigatório quando usar addEventListener
```

```javascript
// shared-worker.js
const ports = new Set(); // manter referência a todos os ports conectados

self.onconnect = (event) => {
  const port = event.ports[0];
  ports.add(port);
  port.start();
  
  port.onmessage = (event) => {
    const { type, ...data } = event.data;
    
    if (type === 'GREET') {
      // Responder só para este port
      port.postMessage({ type: 'GREETING', message: `Olá, ${data.name}!` });
    }
    
    if (type === 'BROADCAST') {
      // Repassar para TODOS os ports (todas as abas)
      broadcast({ type: 'NOTIFICATION', ...data }, port);
    }
  };
  
  // Detectar aba fechada (não confiável, mas melhor que nada)
  port.addEventListener('messageerror', () => {
    ports.delete(port);
  });
};

function broadcast(message, exceptPort = null) {
  ports.forEach(p => {
    if (p !== exceptPort) {
      p.postMessage(message);
    }
  });
}
```

---

## Caso de uso: WebSocket compartilhado

Uma conexão WebSocket por aba é ineficiente. SharedWorker permite uma única conexão para todas:

```javascript
// websocket-worker.js
let socket = null;
const ports = new Set();

self.onconnect = (event) => {
  const port = event.ports[0];
  ports.add(port);
  port.start();
  
  // Criar socket apenas na primeira conexão
  if (!socket) {
    socket = new WebSocket('wss://api.exemplo.com/ws');
    
    socket.onmessage = (event) => {
      // Repassar mensagem para todas as abas
      ports.forEach(p => p.postMessage(JSON.parse(event.data)));
    };
    
    socket.onclose = () => {
      socket = null;
      // Opcional: reconectar com backoff
    };
  }
  
  port.onmessage = (event) => {
    if (socket?.readyState === WebSocket.OPEN) {
      socket.send(JSON.stringify(event.data));
    }
  };
};

// main.js
const worker = new SharedWorker('/websocket-worker.js');
worker.port.start();
worker.port.postMessage({ type: 'SEND', payload: { action: 'subscribe', channel: 'news' } });
worker.port.onmessage = (event) => updateUI(event.data);
```

---

## BroadcastChannel

Mais simples que SharedWorker — broadcast direto entre contextos da mesma origem:

```javascript
// Em qualquer aba/worker/iframe da mesma origem
const channel = new BroadcastChannel('app-channel');

// Enviar para TODAS as outras instâncias do mesmo canal
channel.postMessage({ type: 'USER_LOGGED_OUT', userId: '123' });

// Receber mensagens de outras instâncias
channel.onmessage = (event) => {
  const { type, ...data } = event.data;
  
  if (type === 'USER_LOGGED_OUT') {
    clearUserState();
    redirectToLogin();
  }
};

// Alternativa com addEventListener
channel.addEventListener('message', handleMessage);

// Fechar (não recebe mais mensagens)
channel.close();
```

> [!info] BroadcastChannel vs evento `storage`
> O evento `storage` do localStorage é parecido mas limitado: só dispara em outras abas, só para localStorage, só ao fechar/abrir, sem contexto de quem enviou. `BroadcastChannel` é mais explícito, suporta objetos (sem stringify), e funciona entre workers, iframes e abas.

---

## Padrão: logout sincronizado entre abas

```javascript
// auth.js — executado em cada aba
const authChannel = new BroadcastChannel('auth');

function logout() {
  clearLocalState(); // limpar tokens em memória
  sessionStorage.clear();
  
  // Notificar outras abas
  authChannel.postMessage({ type: 'LOGOUT', timestamp: Date.now() });
  
  redirectToLogin();
}

// Reagir ao logout feito em outra aba
authChannel.onmessage = (event) => {
  if (event.data.type === 'LOGOUT') {
    clearLocalState();
    redirectToLogin();
  }
};
```

---

## Padrão: estado global sincronizado

```javascript
// store-channel.js — sincronizar store Zustand/Redux entre abas
const storeChannel = new BroadcastChannel('store');
let isIncoming = false; // evitar loop

function setupCrossTabSync(store) {
  // Enviar mudanças de estado para outras abas
  store.subscribe((newState, prevState) => {
    if (!isIncoming) {
      storeChannel.postMessage({
        type: 'STATE_CHANGE',
        patch: diff(prevState, newState), // só enviar o que mudou
      });
    }
  });
  
  // Aplicar mudanças recebidas de outras abas
  storeChannel.onmessage = (event) => {
    if (event.data.type === 'STATE_CHANGE') {
      isIncoming = true;
      store.setState(applyPatch(store.getState(), event.data.patch));
      isIncoming = false;
    }
  };
}
```

---

## Comparativo: SharedWorker vs BroadcastChannel

| | SharedWorker | BroadcastChannel |
|---|---|---|
| Complexidade | Alta (ports, connect event) | Baixa (postMessage direto) |
| Lógica centralizada | Sim (toda a lógica no worker) | Não (só mensageria) |
| Estado persistente entre recarregamentos | Sim (enquanto uma aba aberta) | Não |
| Disponibilidade | Boa (exceto Safari antes de 16) | Excelente |
| Comunicação bidirecional | Sim | Sim |
| Suporte a WebSocket centralizado | Sim | Não diretamente |
| Uso típico | Autenticação, WebSocket, cache | Sincronização de UI, logout, notificações |

---

> [!question] Para fixar
> 1. Por que SharedWorker usa `port` em vez de `postMessage` diretamente?
> 2. Qual o evento que SharedWorker recebe quando uma nova aba se conecta?
> 3. Qual o benefício de ter um único WebSocket em um SharedWorker vs. um por aba?
> 4. O BroadcastChannel dispara na mesma aba que enviou a mensagem?
> 5. Qual das duas APIs (SharedWorker vs BroadcastChannel) é melhor para sincronizar logout entre abas? Por quê?

---

## Veja também

- [[03-Dominios/Tecnologia/Plataforma Web/Workers/01 - Web Workers|01 — Web Workers]] — anterior
- [[03-Dominios/Tecnologia/Plataforma Web/Workers/03 - Service Workers e ciclo de vida|03 — Service Workers e ciclo de vida]] — próxima
- [[03-Dominios/Tecnologia/Plataforma Web/Storage/01 - Cookies e Web Storage|Storage 01 — evento storage]] — alternativa simples ao BroadcastChannel
