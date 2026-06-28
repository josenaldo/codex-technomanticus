---
title: "Workers — índice"
created: 2026-06-28
updated: 2026-06-28
type: index
tags:
  - plataforma-web
  - workers
  - browser
  - javascript
publish: true
---

# Workers

Galho 6 da trilha Plataforma Web. Cobre os três tipos de workers do browser: Web Workers para processamento paralelo sem bloquear o main thread, SharedWorker para estado compartilhado entre abas, e Service Worker como proxy de rede para PWAs offline.

---

## Fase Iniciado

- [[03-Dominios/Tecnologia/Plataforma Web/Workers/01 - Web Workers|01 — Web Workers]] — thread separada, postMessage, cópia vs transferência, SharedArrayBuffer, padrão serviço com ID
- [[03-Dominios/Tecnologia/Plataforma Web/Workers/02 - SharedWorker e BroadcastChannel|02 — SharedWorker e BroadcastChannel]] — worker compartilhado entre abas, WebSocket centralizado, broadcast, logout sincronizado

## Fase Adepto

- [[03-Dominios/Tecnologia/Plataforma Web/Workers/03 - Service Workers e ciclo de vida|03 — Service Workers e ciclo de vida]] — install/activate/fetch, skipWaiting, clients.claim, comunicação com a página, depuração
- [[03-Dominios/Tecnologia/Plataforma Web/Workers/04 - Background Sync e Push|04 — Background Sync e Push]] — fila offline com IndexedDB, sync event, Push API com VAPID, web-push Node.js

## Fase Magus

- [[03-Dominios/Tecnologia/Plataforma Web/Workers/05 - Workers em entrevista|05 — Workers em entrevista]] — mindmap, comparativo dos tipos, top 10, armadilhas, capstone

---

## Próximo galho

[[03-Dominios/Tecnologia/Plataforma Web/Networking/index|G7 — Networking]] — fetch em profundidade, HTTP no cliente, SSE, WebSockets, AbortController, Streams
