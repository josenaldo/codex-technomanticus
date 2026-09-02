---
title: "Web Performance & Core Web Vitals"
type: moc
publish: true
created: 2026-07-05
updated: 2026-07-06
tags:
  - moc
  - web-performance
  - core-web-vitals
aliases:
  - Web Performance
  - Core Web Vitals
  - Performance Web
---

# Web Performance & Core Web Vitals

> [!abstract] TL;DR
> A **lente de medição e produto** da performance web: como o browser entrega uma página ao usuário, como medir essa entrega (Core Web Vitals: **LCP, INP, CLS**), o que as métricas significam para usuário, negócio e SEO, e como diagnosticar e sustentar performance ao longo do tempo. Não é sobre uma linguagem nem um framework — é sobre a **experiência percebida** e como prová-la com números.

Este domínio existe porque performance é um tema de entrevista senior por si só, e o vault já tinha performance **espalhada** por várias trilhas sem uma ótica unificadora. A aposta central: *você não otimiza o que não mede*. Antes de falar em resource hints ou main thread, você precisa saber **qual métrica está ruim, para quem, e quanto isso custa** ao produto.

O domínio segue a **linha do tempo da experiência do usuário** — *medir → carregar → responder → sustentar* —, que mapeia limpo nos três Core Web Vitals e minimiza sobreposição entre galhos.

---

## Galhos

| # | Galho | O quê | Core Web Vital âncora |
|---|-------|-------|-----------------------|
| 1 | [[03-Dominios/Tecnologia/Web Performance/Medição e Core Web Vitals/index\|G1 — Medição & Core Web Vitals]] | LCP/INP/CLS, thresholds, lab vs field (RUM), Lighthouse, PageSpeed, CrUX, lib `web-vitals`, budgets como conceito | os 3 |
| 2 | [[03-Dominios/Tecnologia/Web Performance/Performance de Carregamento/index\|G2 — Performance de Carregamento]] | critical rendering path, resource hints, lazy loading, imagens, fontes, compressão, cache/CDN, HTTP/2-3 | LCP |
| 3 | [[03-Dominios/Tecnologia/Web Performance/Performance de Runtime e Rendering/index\|G3 — Performance de Runtime & Rendering]] | main thread, long tasks, INP a fundo, reflow/repaint, layout thrashing, compositing, Workers | INP, CLS |
| 4 | [[03-Dominios/Tecnologia/Web Performance/Performance em Produção/index\|G4 — Performance em Produção]] | budgets no CI, RUM/monitoramento, detecção de regressão, DevTools Performance panel, cultura de perf | — |

---

## Fronteiras — performance que já mora em outras trilhas

Este domínio é a **lente de medição**; ele **linka** as notas abaixo como reforço, **nunca as reescreve** (redundância entre notas = reforço). Cada uma cobre a *técnica* de otimização na sua camada; aqui você aprende *o que medir e por quê*.

- [[03-Dominios/Tecnologia/CSS/12 - Performance CSS|CSS 12 — Performance CSS]] — custo de seletores, contain, will-change, animações compostas.
- [[03-Dominios/Tecnologia/HTML/10 - Performance em HTML - resource hints e critical path|HTML 10 — Resource hints e critical path]] — preload/preconnect, ordem de carregamento.
- [[03-Dominios/Tecnologia/React/React core/17 - Performance no React|React core 17 — Performance no React]] — memoização, re-render, custo de hidratação.
- [[03-Dominios/Tecnologia/Plataforma Web/Rendering Pipeline/index|Plataforma Web — Rendering Pipeline]] — parse, reflow/repaint, compositing no browser.
- [[03-Dominios/Tecnologia/Plataforma Web/Networking/index|Plataforma Web — Networking]] — fetch, HTTP, streams, latência.
- [[03-Dominios/Tecnologia/Tooling e Build/17 - Otimização de bundle|Tooling 17 — Otimização de bundle]] — code splitting, tree shaking, tamanho de JS entregue.

---

## Veja também

- [[03-Dominios/Engenharia/Operação/index|Engenharia — Operação]] — onde budgets no CI e monitoramento de regressão (Galho 4) tocam DevOps/SRE.
- [[03-Dominios/Ciência/Redes e Protocolos/index|Redes e Protocolos]] — fundamentos de rede que a performance de carregamento explora.
