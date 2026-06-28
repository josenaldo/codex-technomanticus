---
title: "Background Sync e Push"
created: 2026-06-28
updated: 2026-06-28
type: note
fase: Adepto
tags:
  - plataforma-web
  - workers
  - browser
  - javascript
  - push
  - background-sync
  - pwa
  - entrevista
publish: true
---

# Background Sync e Push

> [!abstract] TL;DR
> Background Sync permite agendar operações para quando o browser tiver conexão — ideal para formulários que precisam ser enviados offline. Push API permite que o servidor envie notificações mesmo com o browser fechado, via Service Worker. Ambas são APIs avançadas de PWA que completam a experiência offline.

---

## Background Sync

Cenário: usuário preenche um formulário offline. Quando a conexão retornar, o Service Worker envia automaticamente.

### Registrar sincronização

```javascript
// main.js — salvar dados e agendar sync
async function submitFormOffline(formData) {
  // 1. Salvar os dados localmente (IndexedDB)
  const db = await openDB('outbox', 1, {
    upgrade(db) { db.createObjectStore('pending', { autoIncrement: true }); }
  });
  
  await db.add('pending', {
    url: '/api/comments',
    method: 'POST',
    body: JSON.stringify(formData),
    timestamp: Date.now(),
  });
  
  // 2. Registrar a tag de sincronização
  const registration = await navigator.serviceWorker.ready;
  
  try {
    await registration.sync.register('sync-comments');
    console.log('Sincronização agendada');
  } catch (err) {
    // Background Sync não suportado — tentar enviar agora
    await fetch('/api/comments', { method: 'POST', body: JSON.stringify(formData) });
  }
}
```

### Processar no Service Worker

```javascript
// sw.js
self.addEventListener('sync', (event) => {
  if (event.tag === 'sync-comments') {
    event.waitUntil(syncComments());
  }
});

async function syncComments() {
  const db = await openDB('outbox', 1);
  const pending = await db.getAll('pending');
  
  for (const item of pending) {
    try {
      const response = await fetch(item.url, {
        method: item.method,
        body: item.body,
        headers: { 'Content-Type': 'application/json' },
      });
      
      if (response.ok) {
        // Remover da fila após sucesso
        await db.delete('pending', item.id);
      }
    } catch (error) {
      // Falhou de novo — o browser vai tentar novamente automaticamente
      console.error('Sync falhou:', error);
      throw error; // re-throw para o browser saber que falhou
    }
  }
}
```

> [!info] Suporte ao Background Sync
> Background Sync está disponível no Chrome/Edge. Firefox e Safari não têm suporte completo (2024). Sempre implemente um fallback de "tentar enviar agora" + IndexedDB.

---

## Periodic Background Sync

Para sincronização periódica (ex: atualizar feed a cada hora, mesmo sem abrir o app):

```javascript
// main.js
const registration = await navigator.serviceWorker.ready;

// Verificar e solicitar permissão
const status = await navigator.permissions.query({ name: 'periodic-background-sync' });
if (status.state === 'granted') {
  await registration.periodicSync.register('update-feed', {
    minInterval: 60 * 60 * 1000, // no mínimo a cada hora
  });
}

// sw.js
self.addEventListener('periodicsync', (event) => {
  if (event.tag === 'update-feed') {
    event.waitUntil(updateFeedCache());
  }
});

async function updateFeedCache() {
  const response = await fetch('/api/feed?limit=20');
  const data = await response.json();
  
  const cache = await caches.open('feed-cache');
  await cache.put('/api/feed', new Response(JSON.stringify(data), {
    headers: { 'Content-Type': 'application/json' }
  }));
}
```

---

## Push API

A Push API permite que servidores enviem mensagens ao SW, mesmo com o browser fechado.

### Fluxo completo

```
Browser                    Push Service (ex: FCM)    Server
  |                              |                      |
  |---- subscribe() ------------>|                      |
  |<--- PushSubscription --------|                      |
  |---- enviar subscription -----|--------------------->|
  |                              |<--- push message ----|
  |<--- push event no SW --------|                      |
```

### Subscrever

```javascript
// main.js
async function subscribeToPush() {
  const registration = await navigator.serviceWorker.ready;
  
  // VAPID public key do servidor (base64url)
  const VAPID_PUBLIC_KEY = 'BEl62iUYgUivxIkv69yViEuiBIa-Ib9-SkvMeAtA3LFgDzkrxZJjSgSnfckjBJuBkr3qBZYIIlXdu7oICg';
  
  const subscription = await registration.pushManager.subscribe({
    userVisibleOnly: true, // obrigatório — sempre mostrar notificação
    applicationServerKey: urlBase64ToUint8Array(VAPID_PUBLIC_KEY),
  });
  
  // Enviar subscription para o servidor
  await fetch('/api/push/subscribe', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(subscription),
  });
}

// Helper: converter VAPID key
function urlBase64ToUint8Array(base64String) {
  const padding = '='.repeat((4 - base64String.length % 4) % 4);
  const base64 = (base64String + padding).replace(/-/g, '+').replace(/_/g, '/');
  const rawData = atob(base64);
  return Uint8Array.from([...rawData].map(char => char.charCodeAt(0)));
}
```

### Receber push no Service Worker

```javascript
// sw.js
self.addEventListener('push', (event) => {
  const data = event.data?.json() ?? { title: 'Nova notificação', body: '' };
  
  event.waitUntil(
    self.registration.showNotification(data.title, {
      body: data.body,
      icon: '/icons/icon-192.png',
      badge: '/icons/badge.png',
      data: data.url,
      actions: [
        { action: 'open', title: 'Abrir' },
        { action: 'dismiss', title: 'Descartar' },
      ],
    })
  );
});

self.addEventListener('notificationclick', (event) => {
  event.notification.close();
  
  if (event.action === 'open' || !event.action) {
    event.waitUntil(
      clients.matchAll({ type: 'window' }).then(clientList => {
        // Focar aba existente se houver
        for (const client of clientList) {
          if (client.url === event.notification.data && 'focus' in client) {
            return client.focus();
          }
        }
        // Abrir nova aba
        return clients.openWindow(event.notification.data);
      })
    );
  }
});
```

### Enviar push do servidor (Node.js)

```javascript
// server.js (Node.js com web-push)
import webpush from 'web-push';

webpush.setVapidDetails(
  'mailto:dev@exemplo.com',
  process.env.VAPID_PUBLIC_KEY,
  process.env.VAPID_PRIVATE_KEY
);

async function sendPushNotification(subscription, payload) {
  try {
    await webpush.sendNotification(
      subscription,
      JSON.stringify({
        title: 'Nova mensagem',
        body: payload.message,
        url: `/messages/${payload.id}`,
      })
    );
  } catch (error) {
    if (error.statusCode === 410) {
      // Subscription expirou — remover do banco
      await removeSubscription(subscription.endpoint);
    }
    throw error;
  }
}
```

---

## Comparativo: Background Sync vs Push

| | Background Sync | Push API |
|---|---|---|
| Iniciador | Browser (quando retorna conectado) | Servidor |
| App fechado | Sim | Sim (com notificação) |
| Silencioso (sem notificação) | Sim | Não (`userVisibleOnly: true`) |
| Caso de uso | Fila de envio offline | Notificações em tempo real |
| Suporte | Chrome/Edge | Chrome, Firefox, Edge, Safari 16+ |

---

> [!question] Para fixar
> 1. Por que você salva os dados no IndexedDB antes de registrar um Background Sync?
> 2. O que acontece com o evento `sync` se a Promise rejeitar?
> 3. O que é VAPID? Por que é necessário para Push API?
> 4. Por que `userVisibleOnly: true` é obrigatório na Push API?
> 5. O que fazer quando o servidor recebe um 410 (Gone) ao enviar uma push notification?

---

## Veja também

- [[03-Dominios/Tecnologia/Plataforma Web/Workers/03 - Service Workers e ciclo de vida|03 — Service Workers e ciclo de vida]] — anterior
- [[03-Dominios/Tecnologia/Plataforma Web/Workers/05 - Workers em entrevista|05 — Workers em entrevista]] — próxima e capstone
- [[03-Dominios/Tecnologia/Plataforma Web/Web APIs/05 - Notifications e Permissions API|Web APIs 05 — Notifications]] — Notification API e permissões
