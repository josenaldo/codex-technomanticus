---
title: "Performance de Carregamento — índice"
created: 2026-07-06
updated: 2026-07-06
type: index
tags:
  - web-performance
  - carregamento
  - lcp
publish: true
---

# Performance de Carregamento

Galho 2 da trilha Web Performance. Depois de aprender a **medir** (Galho 1), aqui você aprende a **carregar rápido** — o "carregar" da metáfora *medir → carregar → responder → sustentar*. É o galho do **LCP**: como o browser transforma bytes em pixels, o que atrasa esse caminho, e como remover cada gargalo — do primeiro byte até a imagem hero na tela.

A ordem das notas segue o próprio caminho do carregamento: primeiro o **caminho crítico** (o que precisa acontecer antes de qualquer pixel), depois os **recursos pesados** (imagens, fontes, bytes), e por fim a **camada de entrega** (cache, CDN, protocolo).

---

## Fase Iniciado

- [[03-Dominios/Tecnologia/Web Performance/Performance de Carregamento/01 - O Critical Rendering Path|01 — O Critical Rendering Path]] — como o browser vai de HTML/CSS/JS a pixels, e onde o tempo mora
- [[03-Dominios/Tecnologia/Web Performance/Performance de Carregamento/02 - Recursos que bloqueiam a renderização|02 — Recursos que bloqueiam a renderização]] — CSS e JS render-blocking, `async`/`defer`, critical CSS
- [[03-Dominios/Tecnologia/Web Performance/Performance de Carregamento/03 - Resource hints e prioridade|03 — Resource hints e prioridade]] — preconnect, preload, prefetch, `fetchpriority`, priority hints

## Fase Adepto

- [[03-Dominios/Tecnologia/Web Performance/Performance de Carregamento/04 - Otimização de imagens|04 — Otimização de imagens]] — AVIF/WebP, `srcset`/`sizes`, lazy loading, a imagem-LCP
- [[03-Dominios/Tecnologia/Web Performance/Performance de Carregamento/05 - Fontes web|05 — Fontes web]] — FOIT/FOUT, `font-display`, preload, subsetting, self-host
- [[03-Dominios/Tecnologia/Web Performance/Performance de Carregamento/06 - Compressão e minificação|06 — Compressão e minificação]] — Brotli/gzip, minificação, o custo real dos bytes
- [[03-Dominios/Tecnologia/Web Performance/Performance de Carregamento/07 - Cache e CDN|07 — Cache e CDN]] — cache HTTP, `Cache-Control`, immutable, CDN e edge

## Fase Magus

- [[03-Dominios/Tecnologia/Web Performance/Performance de Carregamento/08 - HTTP moderno e estratégia de carregamento|08 — HTTP moderno e estratégia de carregamento]] — HTTP/2, HTTP/3, Early Hints, e como orquestrar tudo. **Capstone**

---

## Próximo galho

**G3 — Performance de Runtime & Rendering** *(a construir)* — quando a página já carregou: main thread, long tasks, INP a fundo, reflow/repaint. Ataca o INP e o CLS que o Galho 1 mede e o Galho 2 não resolve.
