---
title: "Tailwind CSS 4: utility-first na prática"
created: 2026-06-27
updated: 2026-06-27
type: note
fase: magus
tags:
  - css
  - frontend
  - web
  - tailwind
  - utility-first
  - entrevista
publish: true
---

# Tailwind CSS 4: utility-first na prática

> [!abstract] TL;DR
> Tailwind CSS é um framework utility-first: em vez de classes semânticas (`.btn-primary`), você compõe estilos com classes atômicas (`bg-blue-500 text-white px-4 py-2 rounded`). A v4 (2025) reescreveu o engine em Rust, eliminou `tailwind.config.js` em favor de `@import "tailwindcss"` + configuração em CSS, e adotou custom properties nativas para design tokens. O resultado: build 10× mais rápido e integração direta com a cascade do browser. A crítica de "HTML poluído" perde relevância com componentes (React, Vue, Svelte) — cada componente isola seu markup.

---

## O modelo mental utility-first

Utility-first é o oposto do CSS semântico tradicional:

```html
<!-- CSS semântico: classe descreve o papel -->
<button class="btn btn--primary btn--large">Enviar</button>

<!-- Utility-first: classes descrevem os estilos -->
<button class="bg-blue-500 hover:bg-blue-600 text-white font-semibold
               px-6 py-3 rounded-lg transition-colors duration-200">
  Enviar
</button>
```

Por que isso funciona em escala:

1. **Sem invenção de nomes**: nomear coisas é custoso cognitivamente. `.product-card-image-wrapper-inner` não é melhor do que `aspect-square overflow-hidden rounded-lg`.
2. **Sem arquivo CSS separado**: estilos co-localizados com o HTML reduzem o contexto-switching.
3. **Sem crescimento de bundle**: o CSS para de crescer depois de um ponto — as mesmas classes são reutilizadas.
4. **Design constraint built-in**: a escala de espaçamento/cores do Tailwind impede inconsistências.

A crítica válida: em HTML puro sem componentes, repetição de classes é dolorosa. A resposta: use componentes.

---

## Tailwind CSS v4 — o que mudou

### Novo engine em Rust (Lightning CSS)

A v4 usa um engine interno escrito em Rust, substituindo o PostCSS. Resultado:

- Builds full: de ~500ms para ~50ms
- Builds incremental: de ~100ms para ~5ms
- Sem dependência de `postcss.config.js` separado

### Configuração em CSS puro

A v4 eliminou o `tailwind.config.js`:

```css
/* tailwind.config.js (v3) — REMOVIDO */

/* v4: tudo em CSS */
@import "tailwindcss";

@theme {
  /* Sobrescrever ou adicionar tokens */
  --color-primary: oklch(60% 0.18 250);
  --color-primary-hover: oklch(48% 0.20 250);

  --font-sans: 'Inter', system-ui, sans-serif;

  --spacing-18: 4.5rem;
  --spacing-22: 5.5rem;

  --radius-card: 0.75rem;
}
```

`@theme` define tokens que o Tailwind mapeia para classes utilitárias automaticamente:

```html
<!-- --color-primary gera bg-primary, text-primary, border-primary -->
<div class="bg-primary text-white rounded-card">...</div>

<!-- --spacing-18 gera p-18, m-18, gap-18, etc. -->
<div class="p-18">...</div>
```

### Custom properties nativas

Na v4, as utilities do Tailwind são definidas via custom properties reais no CSS gerado — não strings fixas:

```css
/* v3: valores hard-coded no CSS gerado */
.text-blue-500 { color: #3b82f6; }

/* v4: custom properties no :root, classes referenciam */
:root {
  --color-blue-500: oklch(60.83% 0.1894 250.89);
}
.text-blue-500 { color: var(--color-blue-500); }
```

Isso significa que dark mode, theming, e overrides funcionam via custom properties — o CSS do Tailwind se integra com o sistema de design da nota 07.

### Dark mode com media query vs seletor

```css
/* v4: configurar estratégia de dark mode */
@import "tailwindcss";

/* Usando variante media (default) */
/* dark: classes ativam com @media (prefers-color-scheme: dark) */

/* Usando variante selector (para toggle manual) */
@variant dark (&:where(.dark, .dark *));
```

```html
<!-- Dark mode via media query (default) -->
<div class="bg-white dark:bg-gray-900 text-gray-900 dark:text-white">

<!-- Dark mode via selector (após configurar variant) -->
<html class="dark">
  <div class="bg-white dark:bg-gray-900">
```

---

## Classes essenciais — referência rápida

### Layout

```html
<!-- Flexbox -->
<div class="flex items-center justify-between gap-4">
<div class="flex flex-col gap-2">
<div class="inline-flex items-center gap-2">

<!-- Grid -->
<div class="grid grid-cols-3 gap-4">
<div class="grid grid-cols-[repeat(auto-fit,minmax(250px,1fr))] gap-4">

<!-- Grid areas via arbitrary values -->
<div class="grid [grid-template-areas:'header_header''sidebar_main''footer_footer']
            grid-rows-[auto_1fr_auto] min-h-screen">

<!-- Posicionamento -->
<div class="relative">
  <div class="absolute inset-0 bg-black/50">      <!-- overlay -->
  <div class="absolute top-4 right-4">            <!-- badge -->
  <div class="fixed bottom-6 right-6">            <!-- FAB -->
  <div class="sticky top-0 z-10">                 <!-- sticky nav -->
```

### Espaçamento

```html
<!-- padding: p-{n} = padding em todos os lados -->
<div class="p-4">           <!-- padding: 1rem -->
<div class="px-4 py-2">    <!-- horizontal + vertical -->
<div class="pt-6 pb-4">    <!-- top + bottom -->

<!-- margin -->
<div class="m-4 mx-auto">  <!-- centralizar -->
<div class="mt-8 mb-4">

<!-- gap (em flex/grid) -->
<div class="flex gap-4">
<div class="grid gap-x-6 gap-y-4">
```

### Tipografia

```html
<h1 class="text-3xl font-bold tracking-tight">
<p  class="text-base text-gray-700 leading-relaxed">
<span class="text-sm font-medium uppercase tracking-wider">
<a   class="text-blue-600 hover:text-blue-800 underline">

<!-- Clamp nativo via arbitrary value -->
<h1 class="text-[clamp(1.75rem,4vw+0.5rem,3rem)] font-bold">
```

### Cores e backgrounds

```html
<div class="bg-blue-500 text-white">
<div class="bg-gradient-to-r from-blue-500 to-purple-600">
<div class="bg-gray-50 border border-gray-200">

<!-- Transparência com /opacidade -->
<div class="bg-black/50">          <!-- rgba(0,0,0,0.5) -->
<div class="text-gray-900/80">
```

### Bordas e sombras

```html
<div class="border border-gray-200 rounded-lg shadow-md">
<div class="border-2 border-blue-500 rounded-full">
<div class="ring-2 ring-blue-500 ring-offset-2">  <!-- focus ring -->
```

### Estado e interação

```html
<!-- Hover, focus, active -->
<button class="bg-blue-500 hover:bg-blue-600 active:bg-blue-700
               focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500">

<!-- Disabled -->
<button class="disabled:opacity-50 disabled:cursor-not-allowed">

<!-- Group hover — pai controla filho -->
<div class="group">
  <img class="group-hover:scale-105 transition-transform">
  <p class="opacity-0 group-hover:opacity-100 transition-opacity">
</div>

<!-- Peer — irmão controla irmão -->
<input id="email" class="peer">
<label for="email" class="peer-focus:text-blue-500 peer-invalid:text-red-500">
```

### Responsividade

Tailwind usa mobile-first com prefixos de breakpoint:

```html
<!-- Mobile: 1 coluna | md (768px+): 2 colunas | lg (1024px+): 3 colunas -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">

<!-- Espaçamento que aumenta -->
<div class="p-4 md:p-6 lg:p-8">

<!-- Visibilidade -->
<nav class="hidden md:block">     <!-- esconde mobile, mostra tablet+ -->
<button class="md:hidden">       <!-- mostra só mobile -->
```

Breakpoints padrão v4:

| Prefixo | `min-width` |
|---|---|
| `sm:` | 640px |
| `md:` | 768px |
| `lg:` | 1024px |
| `xl:` | 1280px |
| `2xl:` | 1536px |

---

## Arbitrary values — valores customizados

Quando nenhuma classe padrão serve, use `[valor]`:

```html
<!-- Tamanho específico -->
<div class="w-[384px] h-[280px]">

<!-- Grid complexo -->
<div class="grid grid-cols-[200px_1fr_100px]">
<div class="grid grid-rows-[auto_1fr_auto] min-h-screen">

<!-- Cor que não está na paleta -->
<div class="bg-[#ff6b6b]">
<div class="bg-[oklch(60%_0.18_25)]">

<!-- Calc e clamp -->
<div class="w-[calc(100%-2rem)]">
<p class="text-[clamp(1rem,2vw+0.5rem,1.5rem)]">

<!-- Custom property -->
<div class="bg-[var(--color-brand)]">
<div class="p-[var(--space-section)]">
```

---

## Componentes com `@apply` — quando usar

`@apply` extrai classes utilitárias para uma classe CSS semântica:

```css
@layer components {
  .btn {
    @apply inline-flex items-center gap-2 px-4 py-2 rounded-md font-medium
           transition-colors duration-200 focus-visible:outline-none
           focus-visible:ring-2 focus-visible:ring-offset-2;
  }

  .btn--primary {
    @apply bg-blue-500 text-white hover:bg-blue-600
           focus-visible:ring-blue-500;
  }

  .btn--secondary {
    @apply bg-gray-100 text-gray-900 hover:bg-gray-200
           focus-visible:ring-gray-500;
  }
}
```

```html
<!-- Mais limpo no template -->
<button class="btn btn--primary">Enviar</button>
```

> [!warning] `@apply` é para padrões repetidos
> Não use `@apply` para cada componente — isso reproduz o problema do CSS semântico sem os benefícios do utility-first. Reserve para patterns genuinamente repetidos (botões, inputs, cards). Em projetos com framework de componentes (React/Vue/Svelte), prefira extrair o componente em vez de `@apply`.

---

## Configuração de tema (v4)

```css
@import "tailwindcss";

@theme {
  /* Cores */
  --color-brand: oklch(60% 0.18 250);
  --color-brand-dark: oklch(45% 0.20 250);

  /* Extender a paleta padrão (não substituir) */
  --color-gray-950: oklch(12% 0.01 250);

  /* Fontes */
  --font-display: 'Cal Sans', system-ui, sans-serif;

  /* Espaçamento extra */
  --spacing-18: 4.5rem;
  --spacing-22: 5.5rem;
  --spacing-128: 32rem;

  /* Breakpoints */
  --breakpoint-xs: 480px;
  --breakpoint-3xl: 1800px;

  /* Radii */
  --radius-card: 0.75rem;
  --radius-modal: 1rem;

  /* Sombras */
  --shadow-card: 0 4px 20px oklch(0% 0 0 / 0.08);
}
```

---

> [!question] Para fixar
> 1. O que mudou entre Tailwind v3 e v4? Quais são as implicações práticas para um projeto novo?
> 2. Como `group` e `peer` funcionam no Tailwind? Escreva um exemplo de card que muda o texto ao hover no container.
> 3. Quando você usaria `@apply` e quando preferiria extrair um componente React/Vue? Qual é o critério?
> 4. Como o Tailwind v4 integra com o sistema de custom properties do browser? Como você usaria um token `--color-brand` tanto no CSS manual quanto em uma classe Tailwind?
> 5. Um design pede `font-size: clamp(1rem, 2vw + 0.5rem, 1.5rem)`. Como você expressa isso no Tailwind sem adicionar ao tema?
> 6. Qual é a diferença de estratégia de dark mode entre `@media (prefers-color-scheme: dark)` e a variante `selector` do Tailwind?

---

## Veja também

- [[03-Dominios/Tecnologia/CSS/09 - Animações e transitions|09 — Animações]] — anterior
- [[03-Dominios/Tecnologia/CSS/11 - Arquitetura de estilos - CSS Modules, CSS-in-JS e zero-runtime|11 — Arquitetura de estilos]] — próxima
- [[03-Dominios/Tecnologia/CSS/07 - Custom properties e design tokens|07 — Custom properties]] — tokens que o Tailwind v4 usa internamente
- [[03-Dominios/Tecnologia/CSS/06 - Design responsivo - media queries e container queries|06 — Design responsivo]] — mobile-first em Tailwind
