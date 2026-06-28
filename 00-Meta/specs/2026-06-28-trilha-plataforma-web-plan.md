---
title: "Plano — Trilha Plataforma Web (A5)"
type: spec
created: 2026-06-28
updated: 2026-06-28
status: done
tags:
  - spec
  - plataforma-web
  - frontend
  - web
---

# Trilha Plataforma Web — Plano A5

> **Fonte:** meta-plano `2026-06-27-meta-plano-stack-web-js.md` §A5

## Visão

Plataforma Web cobre as APIs e capacidades do **browser** que independem de framework — o que o browser expõe ao JavaScript que roda nele. Diferente do JavaScript (a linguagem em si) e do React/CSS (camadas de abstração), Plataforma Web trata de: como o browser representa o documento (DOM), como eventos propagam, como o browser renderiza, e quais APIs nativas existem para storage, comunicação, workers e observação.

**Fronteiras:**
- `Fundamentos/Redes e Protocolos` → TCP, HTTP/2, CORS, caching conceitual; não repetir aqui
- `JavaScript` → linguagem: closures, event loop, Promises, async/await; não repetir aqui
- `CSS` → cascade, layout, performance de CSS; não repetir aqui
- `HTML` → semântica, formulários, atributos; não repetir aqui
- `React` → reconciliation (Virtual DOM), hooks, Router; não repetir aqui

---

## Estrutura: 7 galhos

| # | Galho | Notas | Fases |
|---|-------|-------|-------|
| G1 | DOM — estrutura, seleção e manipulação | 8 | 3/3/2 |
| G2 | Eventos — model, propagação e patterns | 8 | 3/3/2 |
| G3 | Rendering Pipeline | 7 | 3/2/2 |
| G4 | Web APIs — Observers, History, Clipboard | 8 | 3/3/2 |
| G5 | Storage — cookies, localStorage, IndexedDB, Cache API | 7 | 3/2/2 |
| G6 | Workers — Web Workers, Service Workers | 7 | 3/2/2 |
| G7 | Networking — Fetch, Streams, SSE, WebSockets | 9 | 3/3/3 |
| **Total** | | **54** | |

---

## G1 — DOM: estrutura, seleção e manipulação

**Pasta:** `Plataforma Web/DOM/`

### Fase Iniciado
- 01 — O DOM como árvore — o que é o DOM, relação com HTML, tipos de nó (Element/Text/Comment), `document`, `window`, hierarquia do objeto global
- 02 — Seleção de elementos — `querySelector`/`querySelectorAll`, `getElementById`, `getElementsByClassName`; NodeList vs HTMLCollection; `closest()`, `matches()`
- 03 — Traversal — `parentElement`, `children`, `firstElementChild`/`lastElementChild`, `nextElementSibling`, `previousElementSibling`, `contains()`

### Fase Adepto
- 04 — Manipulação de DOM — `createElement`, `appendChild`, `prepend`, `insertAdjacentHTML`, `insertAdjacentElement`, `remove()`, `replaceWith()`; `innerHTML` vs `textContent` vs `innerText`
- 05 — Atributos, propriedades e dataset — `getAttribute`/`setAttribute`/`removeAttribute`; diferença atributo vs propriedade; `dataset`, `classList` (add/remove/toggle/contains/replace)
- 06 — DocumentFragment e batch mutations — por que inserções diretas no DOM causam reflow; `DocumentFragment`, `replaceChildren()`, padrão acumular→inserir

### Fase Magus
- 07 — `<template>` e `cloneNode` — `<template>` nativo, `content.cloneNode(true)`, `importNode`; Web Components basics (customElements, shadowRoot)
- 08 — DOM em entrevista — virtual DOM vs DOM real, reconciliation conceitual, reflow vs repaint no contexto de manipulação, armadilhas clássicas

---

## G2 — Eventos: model, propagação e patterns

**Pasta:** `Plataforma Web/Eventos/`

### Fase Iniciado
- 01 — O event model do browser — `addEventListener`, fases (capture → target → bubble), `event.target` vs `event.currentTarget`, `stopPropagation` vs `stopImmediatePropagation`
- 02 — Eventos de teclado e ponteiro — `keydown`/`keyup`/`keypress` (deprecated), `click`/`dblclick`, `pointerdown`/`pointermove`/`pointerup`, `touch*`, `wheel`
- 03 — Eventos de formulário e foco — `input`/`change`/`submit`/`reset`, `focus`/`blur`/`focusin`/`focusout`, `beforeinput`, form constraint API

### Fase Adepto
- 04 — Event delegation — padrão de delegação, por que é performático, `event.target.closest()` como ferramenta central, armadilhas com elementos que não propagam (`<td>` e `border-collapse`)
- 05 — Custom events e comunicação — `new CustomEvent()`, `detail`, `bubbles`/`cancelable`/`composed`, pattern pub/sub via CustomEvents, `dispatchEvent()`
- 06 — Timers e microtasks — `setTimeout`/`setInterval`/`clearTimeout`, `requestAnimationFrame`, `queueMicrotask`, `MessageChannel`; relação com a call stack

### Fase Magus
- 07 — Padrões avançados — drag and drop (API nativa), Pointer Lock API, Intersection Observer integrado com eventos de scroll, `passive: true` e performance de scroll
- 08 — Eventos em entrevista — capture vs bubble, event delegation, "como você implementaria um handler global de erros?", `window.onerror` vs `addEventListener('error')`

---

## G3 — Rendering Pipeline

**Pasta:** `Plataforma Web/Rendering Pipeline/`

### Fase Iniciado
- 01 — Parse e construção do DOM/CSSOM — parsing incremental de HTML, tokenizer, como `<script>` bloqueia o parser, `async`/`defer`, DOMContentLoaded vs load
- 02 — Render tree, layout e paint — como DOM + CSSOM geram a Render Tree, layout (reflow) e paint; o que aciona cada etapa
- 03 — Compositing e GPU layers — como o browser cria layers, `will-change`, `transform`/`opacity` como compositor-only, DevTools Layers panel

### Fase Adepto
- 04 — Reflow e repaint — o que aciona reflow (list de propriedades), o que aciona só repaint; como medir com DevTools Performance; batch de leituras antes de escritas
- 05 — Critical Rendering Path otimizado — CRP diagram, above-the-fold CSS inline, resource hints revisitados (preload/preconnect), `fetchpriority`

### Fase Magus
- 06 — requestAnimationFrame e animação imperativa — rAF como o lugar correto de manipular DOM antes do próximo paint; padrão game loop; `requestIdleCallback` para trabalho de baixa prioridade
- 07 — Rendering em entrevista — "explique o que acontece do URL até a primeira pintura", CRP, paint flashing, layout thrashing

---

## G4 — Web APIs: Observers, History e outras

**Pasta:** `Plataforma Web/Web APIs/`

### Fase Iniciado
- 01 — Intersection Observer — uso para lazy loading e animações on-scroll, `threshold`, `rootMargin`, `unobserve()`, pattern de reveal-on-scroll
- 02 — MutationObserver e ResizeObserver — detectar mudanças de DOM (`childList`/`attributes`/`subtree`) e de tamanho; quando usar cada um; armadilhas de ciclo infinito
- 03 — History API e SPA routing — `pushState`/`replaceState`, `popstate`, como SPAs constroem roteamento sobre isso

### Fase Adepto
- 04 — Clipboard e drag-and-drop — `navigator.clipboard` (read/write), permissões, Clipboard Events (`cut`/`copy`/`paste`), DataTransfer
- 05 — Notifications e Permissions API — `Notification.requestPermission()`, `new Notification()`, `navigator.permissions.query()`, padrão de verificação antes de pedir
- 06 — Geolocation e DeviceOrientation — `navigator.geolocation.getCurrentPosition()`, `watchPosition()`, `DeviceOrientationEvent`, privacidade e permissões

### Fase Magus
- 07 — URL, URLSearchParams e Web Share — `new URL()`, `searchParams`, construção de query strings, `navigator.share()` e detecção de suporte
- 08 — Web APIs em entrevista — lazy loading sem biblioteca, implementar infinite scroll com Intersection Observer, como SPA routing funciona sem `#`

---

## G5 — Storage: cookies, localStorage, IndexedDB, Cache API

**Pasta:** `Plataforma Web/Storage/`

### Fase Iniciado
- 01 — Cookies — `document.cookie`, `Set-Cookie` (HttpOnly/Secure/SameSite), expiração, escopo por path/domain; cookies vs tokens de sessão
- 02 — localStorage e sessionStorage — API, limites (~5MB), síncrono (bloqueante), casos de uso corretos, storage event para cross-tab sync
- 03 — IndexedDB — banco de dados client-side; API assíncrona, object stores, índices, transações, quando usar (dados estruturados grandes, offline)

### Fase Adepto
- 04 — Cache API — `caches.open()`, `cache.put()`/`cache.match()`, uso em Service Workers, estratégias (cache-first, network-first, stale-while-revalidate)
- 05 — Storage em entrevista — qual mecanismo para qual caso, Storage API (`navigator.storage.estimate()`), eviction, private/incognito gotchas

### Fase Magus
- 06 — Offline-first com Storage + Service Worker — combinação de IndexedDB + Cache API para app offline; pattern de sync em background; Workbox overview
- 07 — Storage em entrevista avançada — "implemente um carrinho persistente", segurança (XSS e localStorage), cookies HttpOnly como barreira

---

## G6 — Workers: Web Workers, Service Workers e Worklets

**Pasta:** `Plataforma Web/Workers/`

### Fase Iniciado
- 01 — Web Workers — o que é um worker thread no browser, `new Worker()`, `postMessage`/`onmessage`, transferable objects; o que pode e não pode ser feito num worker
- 02 — Shared Workers e Broadcast Channel — `SharedWorker` para comunicação cross-tab, `BroadcastChannel` como alternativa simples
- 03 — Service Workers — ciclo de vida (install → activate → fetch), escopo, registro, `clients.claim()`; por que é a base de PWAs

### Fase Adepto
- 04 — Estratégias de cache com Service Workers — cache-first, network-first, stale-while-revalidate, network-only, cache-only; `workbox` como abstração
- 05 — Background Sync e Push Notifications — `SyncManager`, `PushManager`/`PushSubscription`, payload via Web Push Protocol

### Fase Magus
- 06 — Worklets — `CSS.paintWorklet`, `AudioWorklet`; quando usar; limitações; Houdini overview
- 07 — Workers em entrevista — "como você offloadaria processamento pesado do main thread?", "o que um Service Worker pode interceptar?", debugging de SWs no DevTools

---

## G7 — Networking: Fetch, Streams, SSE e WebSockets

**Pasta:** `Plataforma Web/Networking/` (reformar os 3 stubs existentes)

### Fase Iniciado
- 01 — `fetch` em profundidade — `Request`/`Response`/`Headers`, opções (`method`, `headers`, `body`, `credentials`, `signal`), CORS e preflight, `AbortController`
- 02 — JSON, FormData e outros body types — `.json()`, `.text()`, `.blob()`, `.formData()`; enviar FormData e arquivos; `multipart/form-data`
- 03 — HTTP no cliente — status codes relevantes, cache headers (`Cache-Control`), `ETag`/`If-None-Match`, `Last-Modified`; como o browser caches fetch responses

### Fase Adepto
- 04 — Streams — `ReadableStream`, `WritableStream`, `TransformStream`; streaming de resposta (`response.body`); `TextDecoderStream`; streaming parcial de LLMs
- 05 — Server-Sent Events — `EventSource`, formato do protocolo, `id`/`retry`, reconnect automático; SSE vs WebSocket; quando usar cada um
- 06 — WebSockets — `new WebSocket()`, `send()`/`onmessage`/`onclose`, subprotocols, binary data (`ArrayBuffer`/`Blob`), heartbeat pattern

### Fase Magus
- 07 — AbortController e cancelamento — `AbortSignal`, `signal.aborted`, cancelamento de fetch em cadeia, `AbortSignal.timeout()`, `AbortSignal.any()`
- 08 — Axios — o que adiciona sobre fetch (interceptors, baseURL, timeout, transformData); quando vale a pena; migration para fetch puro
- 09 — Networking em entrevista — "implemente um retry com backoff exponencial", "diferença entre SSE e WebSocket", CORS troubleshooting, throttling e debounce de requests

---

## Sequência de execução

```
G1 (DOM) → G2 (Eventos) → G3 (Rendering)
                                ↓
                          G4 (Web APIs) → G5 (Storage) → G6 (Workers) → G7 (Networking)
```

G1 e G2 são pré-requisitos para G3 e G4. G5 e G6 são independentes entre si. G7 fecha o domínio.

## Anti-duplicação

- Não repetir event loop (JavaScript galho Concorrência)
- Não repetir HTTP/TCP/DNS conceitualmente (Fundamentos/Redes)
- Não repetir CRP de CSS (CSS galho 12/HTML galho 10) — apenas o ângulo de manipulação DOM
- Não repetir fetch patterns no React (React/Ecossistema galho Server State)
