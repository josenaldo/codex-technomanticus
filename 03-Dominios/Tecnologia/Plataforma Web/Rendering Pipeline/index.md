---
title: "Rendering Pipeline — índice"
created: 2026-06-28
updated: 2026-06-28
type: index
tags:
  - plataforma-web
  - rendering
  - browser
  - performance
publish: true
---

# Rendering Pipeline

Galho 3 da trilha Plataforma Web. Cobre como o browser transforma HTML + CSS em pixels: parse, render tree, layout, paint, compositing, e como otimizar cada etapa.

---

## Fase Iniciado

- [[03-Dominios/Tecnologia/Plataforma Web/Rendering Pipeline/01 - Parse e construção do DOM e CSSOM|01 — Parse e construção do DOM e CSSOM]] — parsing incremental, CSS render-blocking, async/defer
- [[03-Dominios/Tecnologia/Plataforma Web/Rendering Pipeline/02 - Render tree, layout e paint|02 — Render tree, layout e paint]] — DOM+CSSOM → render tree, o que aciona reflow vs repaint
- [[03-Dominios/Tecnologia/Plataforma Web/Rendering Pipeline/03 - Compositing e GPU layers|03 — Compositing e GPU layers]] — GPU layers, will-change, transform/opacity, layer explosion

## Fase Adepto

- [[03-Dominios/Tecnologia/Plataforma Web/Rendering Pipeline/04 - Reflow e repaint|04 — Reflow e repaint]] — layout thrashing, forced synchronous layout, batch reads/writes
- [[03-Dominios/Tecnologia/Plataforma Web/Rendering Pipeline/05 - Critical Rendering Path otimizado|05 — Critical Rendering Path otimizado]] — CSS crítico inline, async CSS, preload/preconnect, Web Vitals

## Fase Magus

- [[03-Dominios/Tecnologia/Plataforma Web/Rendering Pipeline/06 - requestAnimationFrame e animação imperativa|06 — requestAnimationFrame]] — delta time, FLIP animations, game loop, requestIdleCallback
- [[03-Dominios/Tecnologia/Plataforma Web/Rendering Pipeline/07 - Rendering em entrevista|07 — Rendering em entrevista]] — URL ao pixel, reflow vs repaint, LCP/CLS/INP, armadilhas, capstone

---

## Próximo galho

[[03-Dominios/Tecnologia/Plataforma Web/Web APIs/index|G4 — Web APIs]] — Intersection Observer, MutationObserver, History API, Clipboard
