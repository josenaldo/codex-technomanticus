---
title: "Notifications e Permissions API"
created: 2026-06-28
updated: 2026-06-28
type: note
fase: adepto
tags:
  - plataforma-web
  - web-apis
  - browser
  - javascript
  - notificacoes
  - permissoes
  - entrevista
publish: true
---

# Notifications e Permissions API

> [!abstract] TL;DR
> A Notifications API exibe notificações nativas do sistema operacional — úteis para alertas mesmo quando o usuário está em outra aba ou app. A Permissions API consulta e observa o estado de permissões do browser (câmera, microfone, notificações, geolocalização) sem triggar o prompt. Juntas, permitem criar fluxos onde você só pede permissão quando há valor real para o usuário, evitando o popup imediato ao entrar na página.

---

## Permissions API — consultar sem pedir

A Permissions API permite verificar o estado atual de uma permissão **sem disparar o prompt** de solicitação:

```javascript
// Consultar estado de uma permissão
const result = await navigator.permissions.query({ name: 'notifications' });

result.state;
// 'granted'  — usuário concedeu
// 'denied'   — usuário negou (prompt não vai aparecer novamente)
// 'prompt'   — ainda não foi solicitado

// Observar mudanças de estado
result.addEventListener('change', () => {
  console.log('Permissão de notificação mudou para:', result.state);
  updateNotificationUI(result.state);
});
```

**Permissões consultáveis:**

```javascript
// Exemplos de permissões que podem ser consultadas
const names = [
  'notifications',
  'geolocation',
  'camera',
  'microphone',
  'clipboard-read',
  'clipboard-write',
  'persistent-storage',
  'push',
  'screen-wake-lock',
];
```

---

## Notifications API

```javascript
// 1. Verificar suporte
if (!('Notification' in window)) {
  console.log('Este browser não suporta notificações');
  return;
}

// 2. Pedir permissão (só funciona após gesto do usuário no Chrome)
const permission = await Notification.requestPermission();
// 'granted' | 'denied' | 'default'

// 3. Exibir notificação
if (permission === 'granted') {
  const notification = new Notification('Nova mensagem', {
    body: 'Você tem 3 mensagens não lidas',
    icon: '/icons/message.png',
    badge: '/icons/badge.png',
    image: '/images/preview.jpg',
    tag: 'mensagens',           // agrupa notificações com a mesma tag
    requireInteraction: false,  // true = não fechar automaticamente
    silent: false,              // true = sem som
    data: { url: '/messages' }, // dados customizados
    actions: [                  // botões (só em Service Worker)
      { action: 'reply', title: 'Responder', icon: '/icons/reply.png' },
      { action: 'dismiss', title: 'Descartar' },
    ],
  });

  notification.addEventListener('click', (event) => {
    window.focus();
    window.location.href = notification.data.url;
    notification.close();
  });

  notification.addEventListener('close', () => {
    console.log('Notificação fechada');
  });

  // Fechar programaticamente após 5s
  setTimeout(() => notification.close(), 5000);
}
```

> [!warning] Restrições do Chrome
> `Notification.requestPermission()` requer gesto do usuário no Chrome — não pode ser chamado ao carregar a página. Sempre peça permissão em resposta a uma ação (clique num botão "Ativar notificações").

---

## Fluxo de UX correto para permissões

```javascript
class NotificationManager {
  // Não pedir permissão ao carregar — verificar estado primeiro
  async init() {
    const { state } = await navigator.permissions.query({ name: 'notifications' });
    this.updateUI(state);
    
    // Observar mudanças (usuário pode mudar nas configurações do browser)
    const permResult = await navigator.permissions.query({ name: 'notifications' });
    permResult.onchange = () => this.updateUI(permResult.state);
  }

  updateUI(state) {
    const btn = document.getElementById('notification-btn');
    
    if (state === 'granted') {
      btn.textContent = 'Notificações ativadas ✓';
      btn.disabled = true;
    } else if (state === 'denied') {
      btn.textContent = 'Notificações bloqueadas (mude nas configurações)';
      btn.disabled = true;
    } else {
      // 'prompt' — usuário ainda não decidiu
      btn.textContent = 'Ativar notificações';
      btn.disabled = false;
      btn.onclick = () => this.requestPermission();
    }
  }

  async requestPermission() {
    const permission = await Notification.requestPermission();
    this.updateUI(permission);
    
    if (permission === 'granted') {
      this.showWelcomeNotification();
    }
  }

  showWelcomeNotification() {
    new Notification('Notificações ativadas!', {
      body: 'Você receberá alertas importantes aqui.',
      icon: '/icons/check.png',
      tag: 'welcome',
    });
  }
  
  // Mostrar notificação (verificar permissão antes)
  notify(title, options = {}) {
    if (Notification.permission !== 'granted') return;
    return new Notification(title, options);
  }
}
```

---

## Notificações via Service Worker

Para notificações Push (mesmo com a aba fechada), é necessário usar Service Worker:

```javascript
// main.js — registrar o Service Worker
const registration = await navigator.serviceWorker.register('/sw.js');
await navigator.serviceWorker.ready;

// Exibir notificação via Service Worker
// (mais recursos: actions, vibration, persistent)
await registration.showNotification('Novo pedido!', {
  body: 'Seu pedido #1234 foi confirmado',
  icon: '/icons/order.png',
  badge: '/icons/badge.png',
  tag: 'order-1234',
  data: { orderId: '1234' },
  actions: [
    { action: 'view', title: 'Ver pedido' },
    { action: 'dismiss', title: 'Ok' },
  ],
  vibrate: [200, 100, 200], // padrão de vibração (mobile)
});
```

```javascript
// sw.js — reagir ao clique na notificação
self.addEventListener('notificationclick', (event) => {
  event.notification.close();
  
  if (event.action === 'view') {
    event.waitUntil(
      clients.openWindow(`/pedidos/${event.notification.data.orderId}`)
    );
  }
});
```

---

## Screen Wake Lock — manter tela ligada

```javascript
let wakeLock = null;

async function requestWakeLock() {
  const { state } = await navigator.permissions.query({ name: 'screen-wake-lock' });
  
  try {
    wakeLock = await navigator.wakeLock.request('screen');
    
    wakeLock.addEventListener('release', () => {
      console.log('Wake lock liberado');
    });
    
    console.log('Tela não vai desligar enquanto você estiver lendo');
  } catch (err) {
    console.error('Wake lock negado:', err);
  }
}

// Wake lock é liberado automaticamente quando a aba fica inativa
// Reativar quando o usuário volta
document.addEventListener('visibilitychange', async () => {
  if (document.visibilityState === 'visible' && wakeLock !== null) {
    wakeLock = await navigator.wakeLock.request('screen');
  }
});

// Liberar manualmente
async function releaseWakeLock() {
  await wakeLock?.release();
  wakeLock = null;
}
```

---

> [!question] Para fixar
> 1. Por que usar `navigator.permissions.query()` antes de `Notification.requestPermission()`?
> 2. O que acontece se você chamar `Notification.requestPermission()` programaticamente ao carregar a página no Chrome?
> 3. Qual a diferença entre `new Notification()` e `registration.showNotification()`? Quando usar cada um?
> 4. O que o campo `tag` faz em uma notificação?
> 5. Por que o wake lock é liberado automaticamente quando a aba fica inativa? Como você lidaria com isso?

---

## Veja também

- [[03-Dominios/Tecnologia/Plataforma Web/Web APIs/04 - Clipboard e File API|04 — Clipboard e File API]] — anterior
- [[03-Dominios/Tecnologia/Plataforma Web/Web APIs/06 - Geolocation e Device APIs|06 — Geolocation e Device APIs]] — próxima
- [[03-Dominios/Tecnologia/Plataforma Web/Workers/03 - Service Workers e ciclo de vida|Workers 03 — Service Workers]] — context de push notifications
