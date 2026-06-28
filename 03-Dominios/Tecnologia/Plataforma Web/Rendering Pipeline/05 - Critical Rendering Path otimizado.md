---
title: "Critical Rendering Path otimizado"
created: 2026-06-28
updated: 2026-06-28
type: note
fase: Adepto
tags:
  - plataforma-web
  - rendering
  - browser
  - performance
  - web-vitals
  - entrevista
publish: true
---

# Critical Rendering Path otimizado

> [!abstract] TL;DR
> O Critical Rendering Path (CRP) é a sequência de passos do browser do HTML recebido até o primeiro pixel pintado. Otimizar CRP significa: entregar o CSS crítico inline (elimina round-trip de rede), carregar CSS não-crítico de forma assíncrona, usar `defer`/`async` em scripts, e usar resource hints (`preload`, `preconnect`) para antecipar downloads. O objetivo final é minimizar o LCP (Largest Contentful Paint) — a métrica de velocidade percebida mais importante.

---

## O Critical Rendering Path

```
Receber HTML
    ↓
Parsear HTML → DOM
    ↓ (em paralelo)
Parsear CSS → CSSOM
    ↓
Combine → Render Tree
    ↓
Layout
    ↓
Paint → First Paint / First Contentful Paint
    ↓
LCP (Largest Contentful Paint)
```

O "caminho crítico" são os recursos que bloqueiam este fluxo: CSS e scripts síncronos são os principais.

---

## CSS crítico inline

O CSS "crítico" é o CSS necessário para renderizar o conteúdo **above the fold** (visível sem scroll). Inlinar no `<head>` elimina um round-trip de rede:

```html
<!DOCTYPE html>
<html>
<head>
  <!-- ✅ CSS crítico inline — zero round-trip, sem render blocking -->
  <style>
    /* Apenas o CSS acima da dobra */
    body { margin: 0; font-family: system-ui, sans-serif; }
    .header { background: #0077cc; color: white; padding: 1rem; }
    .hero { min-height: 60vh; display: flex; align-items: center; }
    .hero__title { font-size: 2.5rem; margin: 0; }
  </style>

  <!-- CSS não-crítico carregado de forma assíncrona -->
  <link
    rel="preload"
    href="/static/styles.css"
    as="style"
    onload="this.rel='stylesheet'"
  >
  <noscript><link rel="stylesheet" href="/static/styles.css"></noscript>
</head>
```

O truque do `preload` + `onload`:
1. `rel="preload"` baixa o arquivo com alta prioridade *sem bloquear o render*
2. `onload="this.rel='stylesheet'"` aplica o CSS quando termina de baixar
3. `<noscript>` garante que usuários sem JS recebem o CSS normalmente

---

## Ferramentas para extrair CSS crítico

```bash
# critical — extrai CSS above-the-fold para um viewport específico
npx critical public/index.html --width 1300 --height 900 --inline

# PurgeCSS — remove CSS não utilizado antes de extrair o crítico
```

Na prática para apps React/Next.js:
- Next.js faz isso automaticamente com CSS Modules
- Para styled-components/Emotion, o servidor extrai o CSS das rotas renderizadas

---

## Resource hints — antecipar downloads

```html
<head>
  <!-- preconnect: estabelecer TCP + TLS com a origem antecipadamente -->
  <!-- Use para origens que você sabe que vai usar (fonts, CDN, APIs) -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

  <!-- dns-prefetch: só resolve DNS (mais barato que preconnect) -->
  <!-- Use para origens de terceiros que podem não ser usadas -->
  <link rel="dns-prefetch" href="https://analytics.example.com">

  <!-- preload: baixar recurso crítico com alta prioridade -->
  <!-- Use para: LCP image, fonte, script crítico -->
  <link rel="preload" href="/fonts/inter.woff2" as="font" crossorigin>
  <link rel="preload" href="/hero.jpg" as="image">
  <link rel="preload" href="/critical-data.json" as="fetch" crossorigin>

  <!-- prefetch: baixar recurso de baixa prioridade para próxima navegação -->
  <link rel="prefetch" href="/about.js">
  <link rel="prefetch" href="/about.css">

  <!-- modulepreload: preload de ES modules -->
  <link rel="modulepreload" href="/src/main.js">
  <link rel="modulepreload" href="/src/router.js"> <!-- imports de main.js -->
</head>
```

---

## `fetchpriority` — ajustar prioridade de carregamento

O browser atribui prioridades automaticamente, mas você pode ajustá-las:

```html
<!-- LCP image — alta prioridade (browser às vezes trata como baixa por estar em img lazy) -->
<img
  src="/hero.jpg"
  alt="Hero"
  width="1200"
  height="600"
  fetchpriority="high"
>

<!-- Imagem below the fold — baixa prioridade + lazy loading -->
<img
  src="/feature.jpg"
  alt="Feature"
  loading="lazy"
  fetchpriority="low"
  decoding="async"
>

<!-- Script de análise não crítico -->
<script src="analytics.js" async fetchpriority="low"></script>
```

---

## Imagens — as maiores oportunidades de CRP

```html
<!-- ✅ Dimensões explícitas — evita CLS (layout shift quando a imagem carrega) -->
<img src="product.jpg" alt="Produto" width="800" height="600">

<!-- ✅ Lazy loading para imagens below the fold -->
<img src="product.jpg" alt="Produto" loading="lazy" decoding="async">

<!-- ✅ Imagem LCP — sem lazy, com preload, com fetchpriority -->
<img src="hero.jpg" alt="Hero" fetchpriority="high" decoding="sync">

<!-- ✅ Responsive images — o browser escolhe o tamanho certo -->
<img
  src="hero-800.jpg"
  srcset="hero-400.jpg 400w, hero-800.jpg 800w, hero-1200.jpg 1200w"
  sizes="(max-width: 600px) 400px, (max-width: 900px) 800px, 1200px"
  alt="Hero"
  fetchpriority="high"
>

<!-- ✅ Formato moderno — WebP/AVIF com fallback -->
<picture>
  <source srcset="hero.avif" type="image/avif">
  <source srcset="hero.webp" type="image/webp">
  <img src="hero.jpg" alt="Hero">
</picture>
```

---

## Core Web Vitals — as métricas que importam

| Métrica | O que mede | Bom | Ruim |
|---|---|---|---|
| **LCP** (Largest Contentful Paint) | Velocidade de carregamento percebida | < 2.5s | > 4s |
| **CLS** (Cumulative Layout Shift) | Estabilidade visual | < 0.1 | > 0.25 |
| **INP** (Interaction to Next Paint) | Responsividade a interação | < 200ms | > 500ms |

### Otimizar LCP

O LCP element é tipicamente um `<img>`, `<video>`, ou bloco grande de texto. Para melhorar:

```html
<!-- 1. Identificar o LCP element (DevTools → Performance → LCP) -->
<!-- 2. Garantir que é carregado com alta prioridade -->
<img src="hero.jpg" fetchpriority="high" alt="Hero">

<!-- 3. Preload se necessário -->
<link rel="preload" href="hero.jpg" as="image">

<!-- 4. Hosting próximo ao usuário (CDN) -->
<!-- 5. Formato eficiente (WebP/AVIF) -->
<!-- 6. Tamanho adequado (srcset responsivo) -->
```

### Evitar CLS

```html
<!-- ✅ Dimensões explícitas em imagens -->
<img src="img.jpg" width="400" height="300" alt="">

<!-- ✅ Reservar espaço para anúncios e embeds -->
<div style="min-height: 250px;">
  <!-- conteúdo dinâmico -->
</div>
```

```css
/* ✅ Fontes customizadas — evitar FOUT que causa shift */
@font-face {
  font-display: swap;   /* exibe fallback imediatamente, troca quando a fonte carrega */
  /* Alternativa: optional — usa a fonte só se já estiver no cache */
}

/* ✅ Reservar espaço para conteúdo de tamanho variável */
.skeleton { min-height: 200px; }
```

### Melhorar INP

```javascript
// INP = tempo entre interação do usuário e próximo paint

// ✅ Usar requestAnimationFrame para agendar updates visuais
btn.addEventListener('click', () => {
  // Processamento rápido (< 50ms) no handler
  const data = processInput();

  // Visual na rAF — garante que acontece no próximo frame
  requestAnimationFrame(() => {
    updateUI(data);
  });
});

// ✅ Para trabalho pesado (> 50ms), usar setTimeout para não bloquear o frame atual
btn.addEventListener('click', () => {
  updateUIImmediately(); // feedback visual imediato
  setTimeout(() => {
    heavyProcessing(); // trabalho pesado depois
  }, 0);
});
```

---

> [!question] Para fixar
> 1. O que é o Critical Rendering Path? Quais recursos o bloqueiam?
> 2. Como você carregaria CSS não-crítico de forma assíncrona? Escreva o HTML completo.
> 3. Qual a diferença entre `preload` e `prefetch`? Quando usar cada um?
> 4. O que é CLS? Como dimensões explícitas em imagens evitam CLS?
> 5. O que LCP mede? Se o LCP da sua página é 4s, quais são as principais causas prováveis?

---

## Veja também

- [[03-Dominios/Tecnologia/Plataforma Web/Rendering Pipeline/04 - Reflow e repaint|04 — Reflow e repaint]] — anterior
- [[03-Dominios/Tecnologia/Plataforma Web/Rendering Pipeline/06 - requestAnimationFrame e animação imperativa|06 — requestAnimationFrame]] — próxima
- [[03-Dominios/Tecnologia/CSS/12 - Performance CSS|CSS 12 — Performance CSS]] — critical CSS pelo ângulo do CSS
