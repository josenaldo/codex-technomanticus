---
title: "Cache API e offline-first"
created: 2026-06-28
updated: 2026-06-28
type: note
fase: iniciado
tags:
  - plataforma-web
  - storage
  - browser
  - javascript
  - cache
  - offline
  - pwa
  - entrevista
publish: true
---

# Cache API e offline-first

> [!abstract] TL;DR
> A Cache API armazena pares Request/Response — diferente de localStorage (strings) e IndexedDB (objetos), ela guarda respostas HTTP completas. É usada principalmente dentro de Service Workers para implementar estratégias de cache de assets e dados da API. Junto com IndexedDB, é a base de apps offline-first e PWAs.

---

## Cache API

```javascript
// Abrir (ou criar) um cache por nome
const cache = await caches.open('v1');

// Adicionar um único URL (faz o fetch internamente)
await cache.add('/styles/app.css');

// Adicionar múltiplos URLs (falha se qualquer um falhar)
await cache.addAll([
  '/',
  '/styles/app.css',
  '/scripts/app.js',
  '/offline.html',
]);

// Salvar um par Request/Response manualmente
const response = await fetch('/api/products');
await cache.put('/api/products', response.clone()); // clone porque response é stream única

// Buscar do cache
const cached = await cache.match('/styles/app.css');
// cached: Response ou undefined

// Buscar em todos os caches
const fromAny = await caches.match('/styles/app.css');

// Listar todas as chaves
const requests = await cache.keys();

// Deletar entrada
await cache.delete('/api/products');

// Deletar cache inteiro
await caches.delete('v1');

// Listar caches disponíveis
const cacheNames = await caches.keys();
```

---

## Cache em Service Workers

O uso mais comum da Cache API é dentro de Service Workers. O Service Worker intercepta requests e decide se serve do cache ou da rede.

```javascript
// sw.js
const CACHE_NAME = 'app-v1';
const STATIC_ASSETS = [
  '/',
  '/app.css',
  '/app.js',
  '/offline.html',
];

// Install: pré-cachear assets estáticos
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(STATIC_ASSETS))
  );
  self.skipWaiting(); // ativar imediatamente sem esperar aba fechar
});

// Activate: limpar caches antigos
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then(names =>
      Promise.all(
        names
          .filter(name => name !== CACHE_NAME)
          .map(name => caches.delete(name))
      )
    )
  );
  self.clients.claim(); // controlar abas imediatamente
});
```

---

## Estratégias de cache

### Cache First (melhor para assets estáticos imutáveis)

```javascript
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then(cached => {
      return cached ?? fetch(event.request);
    })
  );
});
```

### Network First (melhor para dados da API)

```javascript
self.addEventListener('fetch', (event) => {
  event.respondWith(
    fetch(event.request)
      .then(response => {
        // Atualizar cache com resposta fresca
        const clone = response.clone();
        caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
        return response;
      })
      .catch(() => caches.match(event.request)) // fallback ao cache se offline
  );
});
```

### Stale-While-Revalidate (melhor para dados que mudam mas aceitam staleness)

```javascript
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.open(CACHE_NAME).then(async cache => {
      const cached = await cache.match(event.request);
      
      // Buscar nova versão em background (não aguardar)
      const fetchPromise = fetch(event.request).then(response => {
        cache.put(event.request, response.clone());
        return response;
      });

      // Retornar cache imediatamente; na próxima visita estará atualizado
      return cached ?? fetchPromise;
    })
  );
});
```

### Cache Only (para assets que nunca mudam)

```javascript
self.addEventListener('fetch', (event) => {
  event.respondWith(caches.match(event.request));
});
```

---

## Estratégia por tipo de recurso

```javascript
self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);
  
  // Assets estáticos versionados (/app.abc123.js) — Cache First
  if (url.pathname.match(/\.[a-f0-9]{8}\.(js|css)$/)) {
    event.respondWith(cacheFirst(event.request));
    return;
  }
  
  // API de dados — Network First
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(networkFirst(event.request));
    return;
  }
  
  // Páginas HTML — Stale-While-Revalidate
  if (event.request.mode === 'navigate') {
    event.respondWith(staleWhileRevalidate(event.request));
    return;
  }
});
```

---

## Página offline

```javascript
// Fallback para página offline quando navegação falha
self.addEventListener('fetch', (event) => {
  if (event.request.mode !== 'navigate') return;
  
  event.respondWith(
    fetch(event.request).catch(() => caches.match('/offline.html'))
  );
});
```

```html
<!-- offline.html -->
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <title>Sem conexão</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>
  <h1>Você está offline</h1>
  <p>Verifique sua conexão com a internet e tente novamente.</p>
  <button onclick="location.reload()">Tentar novamente</button>
</body>
</html>
```

---

## Workbox — abstração de alto nível

Workbox (Google) abstrai as estratégias acima em configuração declarativa:

```javascript
import { registerRoute } from 'workbox-routing';
import { CacheFirst, NetworkFirst, StaleWhileRevalidate } from 'workbox-strategies';
import { ExpirationPlugin } from 'workbox-expiration';

// Assets JS/CSS — Cache First com expiração de 30 dias
registerRoute(
  ({ request }) => request.destination === 'script' || request.destination === 'style',
  new CacheFirst({
    cacheName: 'static-assets',
    plugins: [new ExpirationPlugin({ maxAgeSeconds: 30 * 24 * 60 * 60 })],
  })
);

// Imagens — Cache First com limite de 50 entradas
registerRoute(
  ({ request }) => request.destination === 'image',
  new CacheFirst({
    cacheName: 'images',
    plugins: [new ExpirationPlugin({ maxEntries: 50 })],
  })
);

// API — Network First com fallback
registerRoute(
  ({ url }) => url.pathname.startsWith('/api/'),
  new NetworkFirst({ cacheName: 'api-cache', networkTimeoutSeconds: 3 })
);
```

---

> [!question] Para fixar
> 1. Qual a diferença entre a Cache API e o cache HTTP padrão do browser?
> 2. Por que você precisa de `response.clone()` antes de salvar no cache?
> 3. Quando você usaria Cache First vs Network First vs Stale-While-Revalidate?
> 4. O que `self.skipWaiting()` faz no Service Worker? Quando é importante usar?
> 5. O que acontece com caches de versões antigas se você não os limpar no evento `activate`?

---

## Veja também

- [[03-Dominios/Tecnologia/Plataforma Web/Storage/02 - IndexedDB|02 — IndexedDB]] — anterior
- [[03-Dominios/Tecnologia/Plataforma Web/Storage/04 - Storage em entrevista|04 — Storage em entrevista]] — próxima e capstone
- [[03-Dominios/Tecnologia/Plataforma Web/Workers/03 - Service Workers e ciclo de vida|Workers 03 — Service Workers]] — context completo do Service Worker
