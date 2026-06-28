---
title: "Plataforma Web"
type: moc
publish: true
created: 2026-06-23
updated: 2026-06-28
tags:
  - moc
  - plataforma-web
aliases:
  - Plataforma Web
---

# Plataforma Web

> [!abstract] TL;DR
> As APIs e capacidades do **navegador** que independem de framework — o que o browser expõe ao JavaScript que roda nele. DOM, eventos, rendering pipeline, Web APIs nativas, storage, workers e comunicação em rede. O *como o navegador funciona para quem programa em cima dele*.

Domínio reúne o que é da **plataforma web** em si — não da linguagem JavaScript nem de um framework específico. A fundamentação conceitual de rede/HTTP vive em [[03-Dominios/Ciência/Redes e Protocolos/index|Redes e Protocolos]]; aqui ficam as APIs concretas que o cliente usa.

---

## Galhos

- [[03-Dominios/Tecnologia/Plataforma Web/DOM/index|G1 — DOM]] — árvore, seleção, manipulação, DocumentFragment, Web Components
- [[03-Dominios/Tecnologia/Plataforma Web/Eventos/index|G2 — Eventos]] — model, propagação, delegation, Custom Events, timers e microtasks
- [[03-Dominios/Tecnologia/Plataforma Web/Rendering Pipeline/index|G3 — Rendering Pipeline]] — parse, CSSOM, reflow/repaint, compositing, rAF
- [[03-Dominios/Tecnologia/Plataforma Web/Web APIs/index|G4 — Web APIs]] — Observers (Intersection/Mutation/Resize), History, Clipboard, Notifications, Geolocation, MediaDevices
- [[03-Dominios/Tecnologia/Plataforma Web/Storage/index|G5 — Storage]] — cookies, localStorage, IndexedDB, Cache API, offline-first
- [[03-Dominios/Tecnologia/Plataforma Web/Workers/index|G6 — Workers]] — Web Workers, SharedWorker, BroadcastChannel, Service Workers, Background Sync, Push
- [[03-Dominios/Tecnologia/Plataforma Web/Networking/index|G7 — Networking]] — fetch, body types, HTTP, Streams, SSE, WebSockets, AbortController, Axios

---

## Veja também

- [[03-Dominios/Ciência/Redes e Protocolos/index|Redes e Protocolos]] — fundamentos: HTTP, TCP, CORS, caching conceitual
- [[03-Dominios/Tecnologia/JavaScript/index|JavaScript]] — a linguagem: closures, event loop, Promises, async/await
- [[03-Dominios/Tecnologia/React/index|React]] — framework: reconciliation, hooks, Router
- [[03-Dominios/Tecnologia/CSS/index|CSS]] — cascade, layout, performance de CSS
