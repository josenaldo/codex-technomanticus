---
title: "Plano — Trilha CSS (13 notas, 3 fases)"
type: spec
created: 2026-06-27
updated: 2026-06-27
status: active
tags:
  - spec
  - css
  - frontend
---

# Plano: Trilha CSS

**Visão**: CSS como linguagem de _apresentação com regras próprias_ — não uma coleção de propriedades decorativas, mas um sistema com cascade, herança, especificidade e um modelo de layout evoluído. A nota de capstone demonstra que CSS moderno 2026 elimina grande parte do JavaScript que antes era necessário para UI.

**Monólito**: `CSS.md` (1263 ln) — absorvido e aposentado ao final.

**Fronteiras**:
- HTML: estrutura e semântica → não aqui
- Plataforma Web: DOM, eventos → não aqui
- React: className, CSS Modules no contexto de componentes → menção, não detalhe
- TypeScript: tipagem de props de estilo → não aqui

---

## Roster

### 🟢 Iniciado — fundamentos obrigatórios (4 notas)

**01 — O modelo mental do CSS: cascade, herança e box model**
O que é CSS *de verdade*: não um conjunto de propriedades decorativas, mas um sistema com três mecanismos — cascade (quem vence em conflito), herança (o que desce pelo DOM), e box model (como o espaço é calculado). Normal flow e como `display` o quebra. `box-sizing: border-box` e por que `content-box` é o default problemático. O que é uma propriedade herdada vs não-herdada. `initial`, `inherit`, `unset`, `revert`.

**02 — Unidades, cores e tipografia**
As unidades do CSS e quando usar cada uma: `px` (bordas), `rem` (font-size e spacing — relativo ao root), `em` (scaling contextual), `%` (relativo ao pai), `vw/vh` (viewport), `svh/dvh/lvh` (mobile com UI dinâmica), `ch` (line length), `fr` (grid). Cores modernas: hex, rgb(), hsl(), `oklch` (perceptualmente uniforme, 2026-padrão). Tipografia: `font-family`, `font-size`, `font-weight`, `line-height` (sem unidade), `letter-spacing`, `font-display`. System font stack. `font-variant-numeric: tabular-nums`.

**03 — Flexbox: layout unidimensional**
Flexbox resolve alinhamento em uma dimensão. Container: `display: flex`, `flex-direction`, `flex-wrap`, `justify-content`, `align-items`, `align-content`, `gap`. Item: `flex-grow`, `flex-shrink`, `flex-basis` → shorthand `flex`. `align-self`, `order`. Patterns clássicos: centralizar absolutamente, navbar com `margin-right: auto`, card com footer colado ao fundo via `flex: 1`, sidebar + main.

**04 — CSS Grid: layout bidimensional**
Grid para layouts 2D. `grid-template-columns`, `grid-template-rows`, `grid-template-areas`. `fr`, `repeat()`, `minmax()`, `auto-fit` vs `auto-fill`. Grid lines: `grid-column: 1 / -1`, `span`. Nomeação de áreas. `gap`. Alignment: `justify-items`, `align-items`, `place-items`. Subgrid. Flexbox vs Grid: quando cada um. Pattern mais pedido: card grid responsivo sem media query (`repeat(auto-fit, minmax(250px, 1fr))`).

---

### 🟡 Adepto — especificidade, responsivo e features modernas (5 notas)

**05 — Especificidade, cascade e @layer**
O algoritmo de cascade completo: importância (origin + `!important`) → especificidade → ordem. Cálculo de especificidade: (A, B, C) — IDs vs classes vs elementos. `:is()` e `:where()` e como afetam especificidade. Cascade layers (`@layer`): por que resolvem wars de especificidade, ordem de declaração de layers, `@layer` anônimo, `!important` dentro de layer (inversão). BEM como solução de nomenclatura antes de layers. Por que `!important` é quase sempre sinal de design errado.

**06 — Design responsivo: media queries e container queries**
Mobile-first: base para mobile, `min-width` para telas maiores. Sintaxe moderna de range (`768px <= width <= 1024px`). `@media` features: `prefers-color-scheme`, `prefers-reduced-motion`, `prefers-contrast`, `pointer: coarse`, `hover: hover`, `print`. Container queries: `container-type: inline-size`, `container-name`, `@container`. Container query units: `cqw`, `cqi`. `clamp()` para fluid typography. `svh/dvh/lvh` para mobile viewport. Media queries vs container queries: quando cada um.

**07 — Custom properties e design tokens**
`--nome: valor` e `var(--nome, fallback)`. Cascade e herança de custom properties (se propagam pelo DOM). Escopo: `:root` para global, `.componente` para local. `@property`: declara tipo, sintaxe, `inherits`, `initial-value` — habilita animação de custom properties. Dark mode com custom properties: `@media (prefers-color-scheme: dark)` e `[data-theme="dark"]`. Design tokens via custom properties: cores, spacing, tipografia, shadows, radii. Por que custom properties são superiores a variáveis Sass para tokens.

**08 — Seletores modernos: :has(), :is(), :where() e nesting**
`:has()` como "parent selector" — estilizar pai baseado em filhos. Casos práticos: form com input inválido, card com imagem, lista vazia. `:is()` como agrupador — especificidade do seletor mais específico dentro. `:where()` — especificidade zero (útil em reset/base layers). `:not()` moderno (aceita seletor complexo). Nesting nativo (2023+): `&`, `&:hover`, `@media` dentro de regra, diferença de Sass. Pseudo-elements: `::before`, `::after`, `::selection`, `::placeholder`, `::backdrop` (para `<dialog>`).

**09 — Animações e transitions**
`transition`: property, duration, timing-function, delay. `transition: all` e por que é problemático. `@keyframes`: from/to vs percentual, múltiplos breakpoints. `animation`: shorthand completo, `fill-mode: forwards`, `iteration-count: infinite`, `play-state: paused`. Timing functions: `ease`, `linear`, `cubic-bezier()`, `steps()`. Performance: animar apenas `transform` e `opacity` (GPU compositor layer). Por que animar `width`, `height`, `top` causa reflow. `will-change`: quando usar e por que não usar sempre. `prefers-reduced-motion`: implementação correta. View Transitions API: `startViewTransition`, `::view-transition-old/new`.

---

### 🔴 Magus — arquitetura de estilos, performance e entrevista (4 notas)

**10 — Tailwind CSS 4: utility-first na prática**
O problema que Tailwind resolve: naming stress, CSS morto, inconsistência de escala. Filosofia utility-first vs component-first. Tailwind 4: Oxide engine, zero-config, `@import "tailwindcss"`, `@theme` em vez de `tailwind.config.js`. Responsive: `md:p-8`, `hover:bg-blue-600`, `dark:bg-gray-800`. Container queries nativas no Tailwind 4. `shadcn/ui` como camada de componentes sobre Tailwind + Radix. Quando Tailwind não é a resposta. Extração de componentes: `@apply` vs componente React. Contraste com BEM e CSS Modules.

**11 — Arquitetura de estilos: CSS Modules, CSS-in-JS e zero-runtime**
CSS Modules: scoping automático, `composes`, quando é a escolha certa. CSS-in-JS runtime (Emotion, styled-components): props dinâmicas, `ThemeProvider`, problema de performance (serialização em runtime, bundle, RSC incompatível). Zero-runtime CSS-in-JS: vanilla-extract (TypeScript tipado, build-time), Panda CSS, Linaria. Por que runtime CSS-in-JS perdeu relevância em 2026. Comparação de abordagens: Tailwind / CSS Modules / vanilla-extract — critérios de escolha por tipo de projeto. CSS no Server Components (Next.js): o que funciona.

**12 — Performance CSS**
Critical CSS: o que é, como o browser identifica CSS render-blocking, inline do crítico no `<head>`, carregamento assíncrono do restante. `content-visibility: auto` + `contain-intrinsic-size`: skip de layout/paint fora da viewport (listas longas). Font performance: `font-display` (swap vs optional vs fallback), `preload` de fontes críticas com `crossorigin`, `font-variant-numeric: tabular-nums`, `font-synthesis`. `object-fit` e `object-position` para imagens responsivas sem distorção. Containing: `contain: layout style paint`. `@layer` como otimização de parse. Evitar CSS que causa reflow: propriedades de layout vs compositing. `pointer-events: none` como hack de performance.

**13 — CSS em entrevista (capstone)**
Mapa mental do galho. As perguntas mais frequentes: box model (content-box vs border-box), diferença Flex vs Grid, o que é specificity, como funciona herança, quando usar `em` vs `rem`. Perguntas de design: "construa um layout de 3 colunas responsivo", "centralize vertical e horizontalmente", "implemente dark mode com CSS puro". Armadilhas clássicas: margin collapsing, z-index sem stacking context, flexbox filho com `min-width: 0`, `%` em height sem pai com height. Checklist final de código CSS de qualidade.

---

## Sequência de execução

1. Criar as 13 notas (fase a fase)
2. Atualizar `index.md` com MOC completo
3. Aposentar `CSS.md` e `Bootstrap.md`
4. Atualizar Roadmap e meta-plano

## Convenções

- Fase Iniciado: ~440-480 linhas
- Fase Adepto/Magus: ~440-540 linhas
- Mermaid: ao menos 1-2 diagramas por nota (flowchart, mindmap, comparação)
- Callouts: `[!abstract]` TL;DR no topo, `[!warning]` para armadilhas, `[!tip]` para boas práticas, `[!question]` no final
- Seção "Veja também" com wikilinks para notas relacionadas do galho
