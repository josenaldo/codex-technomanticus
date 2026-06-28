---
title: "CSS"
type: moc
publish: true
created: 2026-06-23
updated: 2026-06-27
status: evergreen
tags:
  - moc
  - css
aliases:
  - CSS
---
# CSS

> [!abstract] TL;DR
> A linguagem de **estilo** da web — cascade, box model, layout (Flexbox, Grid, Subgrid), responsividade (container queries), design tokens (custom properties, dark mode), seletores modernos (`:has()`, nesting), animações, arquitetura de estilos e utility-first (Tailwind). A marcação vive em [[03-Dominios/Tecnologia/HTML/index|HTML]].

## Trilha — 13 notas, 3 fases

### Iniciado

- [[03-Dominios/Tecnologia/CSS/01 - O modelo mental do CSS - cascade, herança e box model|01 — O modelo mental do CSS]] — cascade, especificidade, herança, box model, stacking context
- [[03-Dominios/Tecnologia/CSS/02 - Unidades, cores e tipografia|02 — Unidades, cores e tipografia]] — rem/em/px/svh, oklch, clamp(), font-display
- [[03-Dominios/Tecnologia/CSS/03 - Flexbox - layout unidimensional|03 — Flexbox]] — eixos, flex-grow/shrink/basis, gap, patterns de navbar/card
- [[03-Dominios/Tecnologia/CSS/04 - CSS Grid - layout bidimensional|04 — CSS Grid]] — fr/repeat/minmax, auto-fit vs auto-fill, template-areas, subgrid

### Adepto

- [[03-Dominios/Tecnologia/CSS/05 - Especificidade, cascade e layer|05 — Especificidade, cascade e @layer]] — algoritmo completo, :is()/:where(), @layer, isolamento de terceiros
- [[03-Dominios/Tecnologia/CSS/06 - Design responsivo - media queries e container queries|06 — Design responsivo]] — mobile-first, container queries, prefers-reduced-motion, logical properties
- [[03-Dominios/Tecnologia/CSS/07 - Custom properties e design tokens|07 — Custom properties e design tokens]] — escopo DOM, tokens semânticos, @property animável, dark mode
- [[03-Dominios/Tecnologia/CSS/08 - Seletores modernos - has, is, where e nesting|08 — Seletores modernos]] — :has() parent selector, :is()/:where(), :not(), CSS nesting
- [[03-Dominios/Tecnologia/CSS/09 - Animações e transitions|09 — Animações e transitions]] — transition vs @keyframes, GPU-only props, prefers-reduced-motion, @property

### Magus

- [[03-Dominios/Tecnologia/CSS/10 - Tailwind CSS 4 - utility-first na prática|10 — Tailwind CSS 4]] — utility-first, v4 engine Rust, @theme, group/peer, dark mode
- [[03-Dominios/Tecnologia/CSS/11 - Arquitetura de estilos - CSS Modules, CSS-in-JS e zero-runtime|11 — Arquitetura de estilos]] — CSS Modules, styled-components, vanilla-extract, ITCSS
- [[03-Dominios/Tecnologia/CSS/12 - Performance CSS|12 — Performance CSS]] — critical CSS, contain, content-visibility, CLS, Core Web Vitals
- [[03-Dominios/Tecnologia/CSS/13 - CSS em entrevista|13 — CSS em entrevista]] — mapa mental, top 10 perguntas, armadilhas clássicas, checklist

## Veja também

- [[03-Dominios/Tecnologia/HTML/index|HTML]] · [[03-Dominios/Tecnologia/React/index|React]] · [[03-Dominios/Tecnologia/Tooling e Build/index|Tooling e Build]]
