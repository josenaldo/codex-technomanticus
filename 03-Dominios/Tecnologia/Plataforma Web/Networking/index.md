---
title: "Networking — índice"
created: 2026-05-04
updated: 2026-06-28
type: moc
tags:
  - plataforma-web
  - networking
  - moc
publish: true
---

# Networking

Comunicação HTTP é o coração de qualquer aplicação frontend: fetch, streaming, WebSockets, cancelamento e clientes como Axios. Este galho cobre o protocolo e as APIs do browser de forma profunda, com o nível de detalhe exigido em entrevistas sênior.

---

## Iniciado

- [[03-Dominios/Tecnologia/Plataforma Web/Networking/01 - fetch em profundidade|01 — fetch em profundidade]] — Response.ok, body, credentials, cache, mode
- [[03-Dominios/Tecnologia/Plataforma Web/Networking/02 - JSON FormData e tipos de body|02 — JSON, FormData e tipos de body]] — JSON, FormData sem Content-Type, URLSearchParams, Blob
- [[03-Dominios/Tecnologia/Plataforma Web/Networking/03 - HTTP no cliente|03 — HTTP no cliente]] — métodos, idempotência, status codes, CORS, retry com backoff

## Adepto

- [[03-Dominios/Tecnologia/Plataforma Web/Networking/04 - Streams e SSE|04 — Streams e SSE]] — ReadableStream, download com progresso, SSE e autenticação
- [[03-Dominios/Tecnologia/Plataforma Web/Networking/05 - WebSockets|05 — WebSockets]] — reconexão manual, heartbeat, autenticação, protocolo de mensagens
- [[03-Dominios/Tecnologia/Plataforma Web/Networking/06 - AbortController|06 — AbortController]] — cancelamento de fetch, event listeners, AbortSignal.timeout e any
- [[03-Dominios/Tecnologia/Plataforma Web/Networking/07 - Axios e HTTP clients|07 — Axios e HTTP clients]] — axios.create, interceptors, refresh de token, onUploadProgress

## Magus

- [[03-Dominios/Tecnologia/Plataforma Web/Networking/08 - Networking em entrevista|08 — Networking em entrevista]] — mindmap, top 10 perguntas, armadilhas clássicas

---

## Veja também

- [[03-Dominios/Tecnologia/Plataforma Web/index|Plataforma Web — índice]] — MOC do domínio
- [[03-Dominios/Tecnologia/Plataforma Web/Workers/index|Workers]] — galho adjacente; Service Worker e Push
- [[03-Dominios/Tecnologia/Plataforma Web/Storage/index|Storage]] — galho adjacente; Cache API e offline-first
