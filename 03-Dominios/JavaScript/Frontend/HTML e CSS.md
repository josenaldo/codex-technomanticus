---
title: "HTML e CSS"
created: 2026-04-01
updated: 2026-04-11
type: concept
status: evergreen
tags:
  - javascript
  - frontend
  - web
  - entrevista
publish: true
---

# HTML e CSS

Deep dive em **HTML semântico moderno** e **CSS 2026** — layout (Flexbox, Grid, Subgrid), responsividade (container queries), design tokens, acessibilidade, performance e frameworks utility-first (Tailwind). Para React, ver [[React]]. Para JavaScript, ver [[JavaScript Fundamentals]].

## O que é

**HTML (HyperText Markup Language)** — a linguagem de marcação que estrutura documentos na web. HTML é estrutura e semântica.

**CSS (Cascading Style Sheets)** — linguagem de estilo que define apresentação visual. CSS é layout, cores, tipografia, animações.

**Separação de preocupações clássica:**

- **HTML** — estrutura (o que é)
- **CSS** — apresentação (como parece)
- **JavaScript** — comportamento (o que faz)

Em 2026, CSS moderno é poderoso o suficiente para resolver problemas que antes exigiam JavaScript (animações complexas, layouts dinâmicos, estados via `:has`, container queries).

Em entrevistas, o que diferencia um senior em HTML/CSS:

1. **Semantic HTML** — não todo elemento é `<div>`, acessibilidade importa
2. **Box model** — content, padding, border, margin, e `box-sizing`
3. **Layout mastery** — Flexbox vs Grid vs Subgrid, quando cada um
4. **Responsive design** — mobile-first, container queries, fluid typography
5. **Specificity e cascade** — por que seu CSS não funciona
6. **CSS variables** — design tokens e theming
7. **Acessibilidade (a11y)** — ARIA, keyboard navigation, color contrast
8. **Performance** — critical CSS, content-visibility, reflow/repaint
9. **CSS-in-JS vs Tailwind vs CSS Modules** — trade-offs
10. **Novidades 2024-2026** — `:has`, container queries, cascade layers, nesting

---

## HTML semântico

HTML semântico **significa usar elementos pelo significado**, não pela aparência. `<div>` é o último recurso.

### Elementos estruturais (HTML5)

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Minha página</title>
</head>
<body>
    <header>
        <nav>
            <ul>
                <li><a href="/">Home</a></li>
                <li><a href="/about">About</a></li>
            </ul>
        </nav>
    </header>

    <main>
        <article>
            <header>
                <h1>Título do artigo</h1>
                <time datetime="2026-04-11">11 de abril de 2026</time>
            </header>
            <section>
                <h2>Seção</h2>
                <p>Conteúdo...</p>
            </section>
            <aside>
                <h3>Relacionado</h3>
                <ul>...</ul>
            </aside>
            <footer>
                <p>Autor: Maria</p>
            </footer>
        </article>
    </main>

    <footer>
        <p>&copy; 2026 MedEspecialista</p>
    </footer>
</body>
</html>
```

**Principais tags estruturais:**

| Tag         | Uso                                           |
| ----------- | --------------------------------------------- |
| `<header>`  | Cabeçalho de página OU de seção/artigo        |
| `<nav>`     | Navegação principal                           |
| `<main>`    | Conteúdo principal (1 por página)             |
| `<article>` | Conteúdo auto-contido (post, card, notícia)   |
| `<section>` | Agrupamento temático com heading              |
| `<aside>`   | Conteúdo relacionado mas secundário (sidebar) |
| `<footer>`  | Rodapé de página OU de seção/artigo           |

### Elementos inline importantes

```html
<strong>importante</strong>        <!-- mais forte que <b> -->
<em>ênfase</em>                     <!-- mais forte que <i> -->
<mark>destacado</mark>              <!-- highlight -->
<code>código</code>
<kbd>Ctrl+C</kbd>                   <!-- teclado -->
<samp>output</samp>                  <!-- saída de programa -->
<var>x</var>                         <!-- variável matemática -->
<abbr title="HyperText Markup Language">HTML</abbr>
<cite>Título de obra</cite>
<q>citação curta</q>
<blockquote cite="https://...">citação longa</blockquote>
<time datetime="2026-04-11T10:00">11 de abril às 10h</time>
<address>
    <a href="mailto:contact@example.com">contact@example.com</a>
</address>
```

### Formulários

```html
<form action="/submit" method="POST">
    <fieldset>
        <legend>Dados pessoais</legend>

        <div>
            <label for="name">Nome</label>
            <input type="text" id="name" name="name" required autocomplete="name">
        </div>

        <div>
            <label for="email">Email</label>
            <input type="email" id="email" name="email" required autocomplete="email">
        </div>

        <div>
            <label for="password">Senha</label>
            <input
                type="password"
                id="password"
                name="password"
                required
                minlength="8"
                autocomplete="new-password"
            >
        </div>

        <div>
            <label for="birth">Nascimento</label>
            <input type="date" id="birth" name="birth">
        </div>

        <div>
            <label for="role">Função</label>
            <select id="role" name="role" required>
                <option value="">Selecione...</option>
                <option value="patient">Paciente</option>
                <option value="doctor">Médico</option>
            </select>
        </div>

        <div>
            <label>
                <input type="checkbox" name="terms" required>
                Aceito os termos
            </label>
        </div>
    </fieldset>

    <button type="submit">Enviar</button>
    <button type="button">Cancelar</button>
</form>
```

**Input types modernos:**

| Type                               | Uso                                           |
| ---------------------------------- | --------------------------------------------- |
| `text`                             | Texto genérico                                |
| `email`                            | Valida formato email, teclado mobile adaptado |
| `tel`                              | Teclado numérico em mobile                    |
| `url`                              | Valida formato URL                            |
| `number`                           | Só números, com spinners                      |
| `date` / `time` / `datetime-local` | Date picker nativo                            |
| `month` / `week`                   | Seleção mês/semana                            |
| `color`                            | Color picker                                  |
| `range`                            | Slider                                        |
| `search`                           | Search com ícone nativo                       |
| `password`                         | Oculta input                                  |
| `file`                             | File picker                                   |
| `hidden`                           | Não visível, envia valor                      |
| `checkbox` / `radio`               | Escolhas                                      |

**Atributos de validação:**

```html
<input
    type="email"
    required
    minlength="5"
    maxlength="100"
    pattern="[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$"
    autocomplete="email"
    inputmode="email"
>
```

### Acessibilidade — ARIA e roles

```html
<!-- Landmark roles (implícitos via HTML5 semântico) -->
<nav role="navigation">          <!-- redundante, nav já é navigation -->
<main role="main">                <!-- redundante -->
<section role="region" aria-labelledby="title-1">
    <h2 id="title-1">Seção</h2>
</section>

<!-- Botão icon-only precisa de label -->
<button aria-label="Fechar modal" onClick={close}>
    <svg>...</svg>
</button>

<!-- Live regions -->
<div role="status" aria-live="polite">
    Item adicionado ao carrinho
</div>

<div role="alert" aria-live="assertive">
    Erro: conexão perdida
</div>

<!-- Formulário com erro -->
<input
    id="email"
    aria-invalid="true"
    aria-describedby="email-error"
>
<span id="email-error" role="alert">Email inválido</span>

<!-- Botão desativado semantically -->
<button aria-disabled="true">Disabled</button>
```

**Regras de ouro de a11y:**

1. **HTML semântico primeiro** — `<button>`, não `<div onClick>`
2. **Alt em imagens** — `alt=""` para decorativas, descritivo para conteúdo
3. **Labels em forms** — `<label for>` ou envolvendo o input
4. **Heading hierarchy** — h1 → h2 → h3, não pule níveis
5. **Keyboard navigation** — tudo interativo acessível por Tab
6. **Focus visible** — não esconda `:focus`
7. **Color contrast** — texto normal 4.5:1, large 3:1 (WCAG AA)
8. **Skip link** — `<a href="#main">Pular para conteúdo</a>`

### HTML APIs úteis

```html
<!-- Lazy loading de imagens -->
<img src="hero.jpg" alt="..." loading="lazy" decoding="async">

<!-- Srcset responsive -->
<img
    src="photo-800.jpg"
    srcset="photo-400.jpg 400w, photo-800.jpg 800w, photo-1600.jpg 1600w"
    sizes="(max-width: 600px) 400px, (max-width: 1200px) 800px, 1600px"
    alt="..."
>

<!-- Picture — arte direção -->
<picture>
    <source media="(max-width: 600px)" srcset="mobile.jpg">
    <source media="(max-width: 1200px)" srcset="tablet.jpg">
    <img src="desktop.jpg" alt="...">
</picture>

<!-- Dialog (modal nativo) -->
<dialog id="modal">
    <form method="dialog">
        <p>Confirmar ação?</p>
        <button value="cancel">Cancelar</button>
        <button value="confirm">OK</button>
    </form>
</dialog>
<script>
    document.getElementById('modal').showModal();
</script>

<!-- Details / summary -->
<details>
    <summary>Clique para expandir</summary>
    <p>Conteúdo escondido</p>
</details>

<!-- Popover (HTML5, 2024) -->
<button popovertarget="my-popover">Toggle</button>
<div id="my-popover" popover>Popover content</div>
```

---

## CSS fundamentals

### Box model

```
┌─────────────────────────────────────┐
│          margin                     │
│  ┌───────────────────────────────┐  │
│  │         border                │  │
│  │  ┌─────────────────────────┐  │  │
│  │  │       padding           │  │  │
│  │  │  ┌───────────────────┐  │  │  │
│  │  │  │     content       │  │  │  │
│  │  │  └───────────────────┘  │  │  │
│  │  └─────────────────────────┘  │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
```

**`box-sizing`:**

```css
/* Default do browser — width é só o content */
.box {
    box-sizing: content-box;
    width: 200px;        /* content = 200 */
    padding: 20px;       /* total = 240px */
    border: 2px solid;   /* total = 244px */
}

/* Moderno — width inclui padding e border */
.box {
    box-sizing: border-box;
    width: 200px;        /* total = 200px */
    padding: 20px;       /* content = 156px */
    border: 2px solid;   /* content = 156px */
}

/* Reset global — recomendado */
*, *::before, *::after {
    box-sizing: border-box;
}
```

### Display e positioning

```css
/* Display */
.block       { display: block; }
.inline      { display: inline; }
.inline-block { display: inline-block; }
.flex         { display: flex; }
.grid         { display: grid; }
.none         { display: none; }
.contents     { display: contents; }  /* remove o elemento mas mantém filhos */

/* Position */
.static    { position: static; }     /* default */
.relative  { position: relative; }   /* referência para children absolute */
.absolute  { position: absolute; }   /* removido do fluxo */
.fixed     { position: fixed; }      /* relativo ao viewport */
.sticky    { position: sticky; top: 0; }  /* fixa quando scroll atinge */
```

### Cores

```css
/* Named */
color: red;
color: transparent;

/* Hex */
color: #ff0000;
color: #ff0000aa;  /* com alpha */
color: #f00;

/* RGB */
color: rgb(255 0 0);
color: rgb(255 0 0 / 0.5);

/* HSL — mais intuitivo */
color: hsl(0 100% 50%);
color: hsl(0 100% 50% / 0.5);

/* Modernos (2022+) */
color: oklch(50% 0.2 10);  /* perceptually uniform */
color: lch(50% 80 10);
color: color(display-p3 1 0 0);  /* wide gamut */
```

**`oklch`** é recomendado em 2026 — espaço perceptualmente uniforme, melhor para animações de cor.

### Tipografia

```css
.texto {
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    font-size: 1rem;           /* 16px por default */
    font-weight: 400;          /* normal, 700=bold */
    line-height: 1.5;          /* sem unidade é recomendado */
    letter-spacing: 0.01em;
    word-spacing: 0.05em;
    text-transform: uppercase; /* uppercase, lowercase, capitalize */
    text-decoration: underline;
    text-align: left;          /* left, center, right, justify */
    font-style: italic;
    font-variant-numeric: tabular-nums;  /* números alinhados */
}
```

**System font stack:**

```css
font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
```

### Unidades

| Unidade               | O que é                        | Quando usar                         |
| --------------------- | ------------------------------ | ----------------------------------- |
| `px`                  | Pixel absoluto                 | Bordas, pequenos offsets            |
| `rem`                 | Relativo ao root (html)        | **Default para font-size, spacing** |
| `em`                  | Relativo ao elemento pai       | Para escalar com contexto           |
| `%`                   | Relativo ao pai                | Widths, heights                     |
| `vw` / `vh`           | Viewport width/height          | Layouts full-screen                 |
| `svh` / `lvh` / `dvh` | Small/large/dynamic vh (2023+) | Mobile com barra de URL             |
| `vmin` / `vmax`       | Menor/maior do viewport        | Responsividade                      |
| `ch`                  | Largura do '0' da fonte        | Line length                         |
| `ex`                  | Altura do 'x'                  | Raramente                           |
| `fr`                  | Fraction do grid               | CSS Grid                            |
| `auto`                | Automático                     | Layout, margins                     |

**Unidades modernas (2023+):**

- **`svh` / `lvh` / `dvh`** — viewport height considerando barras dinâmicas em mobile
- **Container query units** — `cqw`, `cqh`, `cqi`, `cqb`, `cqmin`, `cqmax`

---

## CSS moderno — features essenciais

### CSS Variables (Custom Properties)

Design tokens em CSS puro:

```css
:root {
    /* Colors */
    --color-primary: oklch(60% 0.15 250);
    --color-primary-hover: oklch(55% 0.18 250);
    --color-bg: oklch(98% 0.01 250);
    --color-text: oklch(20% 0.02 250);

    /* Spacing */
    --space-xs: 0.25rem;
    --space-sm: 0.5rem;
    --space-md: 1rem;
    --space-lg: 2rem;
    --space-xl: 4rem;

    /* Typography */
    --font-base: 1rem;
    --font-lg: 1.25rem;
    --font-xl: 1.5rem;

    /* Radius */
    --radius-sm: 0.25rem;
    --radius-md: 0.5rem;

    /* Shadows */
    --shadow-sm: 0 1px 2px rgb(0 0 0 / 0.1);
    --shadow-md: 0 4px 6px rgb(0 0 0 / 0.1);
}

.button {
    background: var(--color-primary);
    color: var(--color-bg);
    padding: var(--space-sm) var(--space-md);
    border-radius: var(--radius-md);
    font-size: var(--font-base);
}

.button:hover {
    background: var(--color-primary-hover);
}
```

**Dark mode via variables:**

```css
:root {
    --color-bg: white;
    --color-text: black;
}

@media (prefers-color-scheme: dark) {
    :root {
        --color-bg: #111;
        --color-text: #eee;
    }
}

/* Ou toggleable */
[data-theme="dark"] {
    --color-bg: #111;
    --color-text: #eee;
}
```

### @property (2022+)

Declara tipo para variables — permite animação de custom properties:

```css
@property --hue {
    syntax: '<number>';
    inherits: false;
    initial-value: 0;
}

.element {
    background: oklch(60% 0.15 var(--hue));
    transition: --hue 1s;
}

.element:hover {
    --hue: 250;  /* anima de 0 para 250 */
}
```

### Nesting (2023+)

CSS suporta nesting nativamente — não precisa mais de Sass só por isso:

```css
.card {
    padding: 1rem;
    border: 1px solid #ddd;

    & .title {
        font-size: 1.5rem;
    }

    & .content {
        color: #666;

        & a {
            color: blue;
        }
    }

    &:hover {
        border-color: blue;
    }

    @media (min-width: 768px) {
        padding: 2rem;
    }
}
```

### Cascade layers (`@layer`)

Controla especificidade por camadas:

```css
@layer reset, base, components, utilities;

@layer reset {
    * { margin: 0; padding: 0; }
}

@layer base {
    body { font-family: sans-serif; }
    h1 { font-size: 2rem; }
}

@layer components {
    .btn {
        padding: 0.5rem 1rem;
    }
}

@layer utilities {
    .mt-4 { margin-top: 1rem; }
}
```

**Ordem de especificidade:** layer `utilities` > `components` > `base` > `reset`, **independente** de especificidade do seletor dentro de cada layer.

### `:has()` — parent selector (2023+)

O selector mais pedido da história do CSS finalmente chegou. Permite estilizar um elemento baseado em **seus filhos**.

```css
/* Card com imagem tem padding extra */
.card:has(img) {
    padding-top: 0;
}

/* Form inválido */
form:has(input:invalid) button {
    opacity: 0.5;
    pointer-events: none;
}

/* Quando contém um .error */
.section:has(.error) {
    border-color: red;
}

/* Não tem filhos */
.list:not(:has(*)) {
    display: none;
}
```

### Container queries (2023+)

Queries responsivas baseadas no **container**, não no viewport. Permite componentes verdadeiramente reutilizáveis.

```css
.card {
    container-type: inline-size;
    container-name: card;
}

@container card (min-width: 400px) {
    .card__content {
        display: flex;
        gap: 1rem;
    }
}

@container (min-width: 600px) {
    .card {
        padding: 2rem;
    }
}
```

**Container query units:**

```css
.card__title {
    font-size: 5cqi;  /* 5% do inline container size */
}
```

### Nova sintaxe de media queries

```css
/* Antigo */
@media (min-width: 768px) and (max-width: 1024px) { ... }

/* Moderno (range syntax) */
@media (768px <= width <= 1024px) { ... }
@media (width >= 768px) { ... }
```

### Media features modernas

```css
@media (prefers-color-scheme: dark) { ... }
@media (prefers-reduced-motion: reduce) { ... }
@media (prefers-contrast: more) { ... }
@media (pointer: coarse) { ... }  /* touch device */
@media (hover: hover) { ... }      /* pode fazer hover */
@media (orientation: landscape) { ... }
@media print { ... }
```

### Subgrid (2023+)

Permite grid items herdarem grid do pai:

```css
.main-grid {
    display: grid;
    grid-template-columns: 200px 1fr;
    grid-template-rows: auto 1fr auto;
}

.card {
    display: grid;
    grid-template-columns: subgrid;  /* herda colunas do pai */
    grid-column: 1 / -1;
}
```

---

## Layout — Flexbox

Flexbox é para layouts **unidimensionais** (row OU column).

```css
.container {
    display: flex;
    flex-direction: row;           /* row, row-reverse, column, column-reverse */
    flex-wrap: wrap;               /* nowrap (default), wrap, wrap-reverse */
    justify-content: space-between; /* ao longo do eixo principal */
    align-items: center;            /* ao longo do eixo cruzado */
    gap: 1rem;                      /* espaçamento entre items */
}

.item {
    flex-grow: 1;       /* cresce proporcionalmente */
    flex-shrink: 0;     /* não encolhe */
    flex-basis: 200px;  /* base antes de crescer/encolher */
    /* shorthand */
    flex: 1 0 200px;
}
```

### Justify-content

| Valor           | Efeito                                           |
| --------------- | ------------------------------------------------ |
| `flex-start`    | Itens no início                                  |
| `flex-end`      | Itens no fim                                     |
| `center`        | Itens no centro                                  |
| `space-between` | Espaço entre itens, primeiro e último encostados |
| `space-around`  | Espaço igual ao redor de cada item               |
| `space-evenly`  | Espaço igual entre todos (incluindo pontas)      |

### Align-items

| Valor                     | Efeito                           |
| ------------------------- | -------------------------------- |
| `stretch` (default)       | Esticam para altura do container |
| `flex-start` / `flex-end` | Início / fim                     |
| `center`                  | Centro                           |
| `baseline`                | Alinha pela baseline do texto    |

### Patterns clássicos

```css
/* Centralizar absolutamente */
.center {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}

/* Card com header, conteúdo, footer — push footer to bottom */
.card {
    display: flex;
    flex-direction: column;
    min-height: 400px;
}
.card__content {
    flex: 1;  /* ocupa espaço restante */
}

/* Navbar com logo + links + botão */
.navbar {
    display: flex;
    align-items: center;
    gap: 1rem;
}
.navbar__logo { margin-right: auto; }  /* empurra resto para direita */

/* Sidebar + main */
.layout {
    display: flex;
    gap: 1rem;
}
.sidebar { flex: 0 0 250px; }
.main    { flex: 1; }
```

---

## Layout — CSS Grid

Grid é para layouts **bidimensionais**.

```css
.grid {
    display: grid;
    grid-template-columns: 200px 1fr 200px;   /* 3 colunas */
    grid-template-rows: auto 1fr auto;         /* 3 linhas */
    gap: 1rem;
    grid-template-areas:
        "header header header"
        "sidebar main   aside"
        "footer footer  footer";
}

.header  { grid-area: header; }
.sidebar { grid-area: sidebar; }
.main    { grid-area: main; }
.aside   { grid-area: aside; }
.footer  { grid-area: footer; }
```

### Repeat e fr

```css
/* 3 colunas iguais */
grid-template-columns: repeat(3, 1fr);

/* 12 colunas */
grid-template-columns: repeat(12, 1fr);

/* Mistura */
grid-template-columns: 200px repeat(3, 1fr) 100px;
```

### Auto-fit vs auto-fill

```css
/* Fit — colunas expandem para preencher */
grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));

/* Fill — cria slots vazios */
grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
```

**Use `auto-fit`** na maioria dos casos — responsividade automática sem media queries.

### Grid lines

```css
.item {
    grid-column: 1 / 3;        /* da coluna 1 até 3 (2 colunas) */
    grid-column: 1 / -1;        /* toda largura */
    grid-column: span 2;        /* ocupa 2 colunas */
    grid-row: 2 / 4;
}
```

### Alignment

```css
.grid {
    /* Colunas */
    justify-items: center;    /* items no eixo horizontal */
    justify-content: center;  /* grid todo no eixo horizontal */

    /* Linhas */
    align-items: center;      /* items no eixo vertical */
    align-content: center;    /* grid todo no eixo vertical */

    /* Shorthand */
    place-items: center;      /* align + justify items */
    place-content: center;    /* align + justify content */
}
```

### Flexbox vs Grid

|             | Flexbox                          | Grid                         |
| ----------- | -------------------------------- | ---------------------------- |
| Dimensões   | 1D (linha OU coluna)             | 2D (linha E coluna)          |
| Alinhamento | Content-first                    | Layout-first                 |
| Responsivo  | Baseado em wrap                  | Baseado em template          |
| Uso         | Nav, formulários, cards internos | Layout de página, dashboards |

**Regra prática:**

- **Grid** para layout da página/seção
- **Flex** para alinhamento dentro de componentes

Frequentemente se combinam: Grid para o macro, Flex para o micro.

---

## Responsive design

### Mobile-first

Escreva CSS base para mobile, adicione media queries para telas maiores.

```css
/* Mobile default */
.card {
    padding: 1rem;
    font-size: 1rem;
}

/* Tablet+ */
@media (width >= 768px) {
    .card {
        padding: 2rem;
        font-size: 1.125rem;
    }
}

/* Desktop+ */
@media (width >= 1024px) {
    .card {
        padding: 3rem;
    }
}
```

**Por que mobile-first:**

- Mobile é a maioria dos usuários
- Cascade adiciona, não sobrescreve
- CSS mais limpo

### Breakpoints comuns

```css
/* Tailwind/Bootstrap-like */
@media (width >= 640px)  { /* sm */ }
@media (width >= 768px)  { /* md */ }
@media (width >= 1024px) { /* lg */ }
@media (width >= 1280px) { /* xl */ }
@media (width >= 1536px) { /* 2xl */ }
```

**Regra:** escolha breakpoints baseados no seu conteúdo, não em devices específicos.

### Fluid typography

Texto que escala suavemente com a viewport:

```css
/* clamp(min, preferred, max) */
h1 {
    font-size: clamp(2rem, 4vw + 1rem, 4rem);
}

p {
    font-size: clamp(1rem, 1vw + 0.875rem, 1.25rem);
    line-height: 1.6;
}
```

**Linha de texto ideal:** 60-80 caracteres. Use `max-width`:

```css
p {
    max-width: 65ch;  /* 65 chars */
}
```

### Container queries vs media queries

**Media queries** — responde ao viewport. **Container queries** — responde ao container do componente.

```css
.sidebar {
    container-type: inline-size;
}

.card {
    display: grid;
    grid-template-columns: 1fr;
}

@container (min-width: 400px) {
    .card {
        grid-template-columns: 150px 1fr;
    }
}
```

Mesmo card se adapta corretamente independente de onde está (sidebar estreita vs main ampla).

---

## Specificity e cascade

Quando múltiplas regras se aplicam, CSS usa **specificity** para decidir.

### Cálculo de specificity

Notação `(A, B, C, D)`:

- **A** — `!important` (evite)
- **B** — IDs (`#id`)
- **C** — Classes (`.class`), atributos (`[type]`), pseudo-classes (`:hover`)
- **D** — Elementos (`div`), pseudo-elements (`::before`)

```css
div           (0, 0, 0, 1)
.btn          (0, 0, 1, 0)
.btn.primary  (0, 0, 2, 0)
#header       (0, 1, 0, 0)
#header .btn  (0, 1, 1, 0)
```

**Mais alto ganha.** Em empate, última regra ganha.

### Cascade — ordem de precedência

1. **`!important`** no autor → ganha tudo (evite)
2. **Specificity**
3. **Ordem** no arquivo
4. **Origem** (browser default < user < author)
5. **Cascade layers** (`@layer`)

### Evitando problemas

```css
/* RUIM — usar !important */
.btn { color: red !important; }

/* RUIM — seletores super específicos */
body > div > main > section > .card > .btn { ... }

/* BOM — BEM ou cascade layers */
.btn--primary { ... }

/* BOM — layers */
@layer components {
    .btn { ... }
}
```

### BEM (Block Element Modifier)

Convenção de nomenclatura:

```css
.card { }                    /* Block */
.card__title { }             /* Element */
.card__title--large { }      /* Modifier */
.card--featured { }

.button { }
.button--primary { }
.button__icon { }
```

Simples, escalável, evita problemas de especificidade. Substituído frequentemente por utility-first (Tailwind) ou CSS-in-JS em projetos modernos.

---

## Animações e transitions

### Transitions

```css
.btn {
    background: blue;
    transform: scale(1);
    transition: background 0.2s ease, transform 0.2s ease;
    /* ou */
    transition: all 0.2s ease;  /* cuidado com performance */
}

.btn:hover {
    background: darkblue;
    transform: scale(1.05);
}
```

**Transition properties:**

```css
transition-property: background, transform;
transition-duration: 200ms;
transition-timing-function: ease;  /* linear, ease-in, ease-out, ease-in-out, cubic-bezier() */
transition-delay: 0s;
```

### Keyframe animations

```css
@keyframes slide-in {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.modal {
    animation: slide-in 0.3s ease-out;
}
```

**Animation properties:**

```css
animation-name: slide-in;
animation-duration: 0.3s;
animation-timing-function: ease-out;
animation-delay: 0s;
animation-iteration-count: 1;  /* infinite, 3, etc. */
animation-direction: normal;   /* reverse, alternate */
animation-fill-mode: forwards; /* backwards, both */
animation-play-state: running; /* paused */

/* Shorthand */
animation: slide-in 0.3s ease-out forwards;
```

### Performance

**Propriedades que animam bem (GPU):**

- `transform` (translate, scale, rotate)
- `opacity`

**Propriedades que causam layout reflow (evite animar):**

- `width`, `height`, `top`, `left`, `margin`, `padding`
- `font-size`, `color` (repaint, aceitável)

```css
/* RUIM */
.box {
    left: 0;
    transition: left 0.3s;
}
.box:hover { left: 100px; }

/* BOM */
.box {
    transform: translateX(0);
    transition: transform 0.3s;
}
.box:hover { transform: translateX(100px); }
```

### Respeitar prefers-reduced-motion

```css
@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}
```

### View Transitions API (2024+)

```css
/* CSS */
::view-transition-old(root),
::view-transition-new(root) {
    animation-duration: 0.3s;
}
```

```javascript
// JS
document.startViewTransition(() => {
    updateDOM();
});
```

Permite transições suaves entre estados de página — fallback para browsers sem suporte é instantâneo.

---

## Tailwind CSS — utility-first

Em 2026, **Tailwind CSS 4** é a abordagem dominante em projetos modernos. Em vez de escrever classes customizadas, você compõe utilities.

```html
<!-- Antes -->
<div class="card">
    <h2 class="card__title">Hello</h2>
    <p class="card__content">...</p>
</div>

<style>
.card {
    padding: 1rem;
    border: 1px solid #e5e7eb;
    border-radius: 0.5rem;
    background: white;
    box-shadow: 0 1px 2px rgb(0 0 0 / 0.1);
}
.card__title { font-size: 1.5rem; font-weight: bold; margin-bottom: 0.5rem; }
.card__content { color: #6b7280; }
</style>

<!-- Com Tailwind -->
<div class="p-4 border border-gray-200 rounded-lg bg-white shadow-sm">
    <h2 class="text-2xl font-bold mb-2">Hello</h2>
    <p class="text-gray-500">...</p>
</div>
```

**Vantagens:**

- **Sem naming stress** — não precisa inventar nome para cada card
- **Sem CSS morto** — se o HTML sai, classes saem junto
- **Consistência via design system** — cores, spacing pré-definidos
- **Responsive built-in** — `md:p-8 lg:p-12`
- **Hover, focus, dark mode** — `hover:bg-blue-600 dark:bg-gray-800`
- **Fácil dar manutenção** — o que você vê no HTML é o que está aplicado

**Desvantagens:**

- HTML verboso
- Curva de aprendizado (memorizar classes)
- Requer build step
- Pode ficar sujo sem extração em componentes

### Tailwind 4 novidades (2025)

- **Oxide engine** — muito mais rápido
- **Zero config** — sem `tailwind.config.js` obrigatório
- **CSS-first** — config em CSS (`@theme`)
- **Container queries** nativos
- **Cascade layers** automáticos

```css
@import "tailwindcss";

@theme {
    --color-brand: oklch(60% 0.15 250);
    --font-display: 'Inter', sans-serif;
}
```

### Tailwind + shadcn/ui

Padrão comum em 2026: Tailwind para estilos + shadcn/ui para componentes (copy-paste de Radix primitives). Personalização total sem depender de biblioteca.

---

## CSS-in-JS vs CSS Modules vs Tailwind

### CSS-in-JS (Emotion, styled-components)

```tsx
import styled from '@emotion/styled';

const Button = styled.button`
    padding: 0.5rem 1rem;
    background: ${props => props.primary ? 'blue' : 'gray'};
    color: white;
    border-radius: 0.25rem;

    &:hover {
        opacity: 0.9;
    }
`;

<Button primary>Click</Button>
```

**Em 2026:** perdendo relevância. Problemas de performance (runtime), bundle size, e compatibilidade com RSC. Zero-runtime alternatives (Panda CSS, vanilla-extract, styled-components no compile-time) são o futuro.

### CSS Modules

```tsx
// Button.module.css
.button {
    padding: 0.5rem 1rem;
}

// Button.tsx
import styles from './Button.module.css';

<button className={styles.button}>Click</button>
```

**Prós:** scoping automático, familiar, sem runtime.
**Contras:** menos produtivo que Tailwind.

### Tailwind

Ver seção anterior. **Default em 2026 para novos projetos React.**

### Vanilla-extract

Zero-runtime CSS-in-TypeScript. Gera CSS em build time, tem tipagem.

```typescript
// button.css.ts
import { style } from '@vanilla-extract/css';

export const button = style({
    padding: '0.5rem 1rem',
    ':hover': { opacity: 0.9 }
});
```

**Vantagem sobre Tailwind:** tipagem completa, mais controle. **Desvantagem:** menos ergonômico.

---

## Performance CSS

### Critical CSS

CSS mínimo para o first paint inline no `<head>`, resto carrega assíncrono:

```html
<style>
    /* Critical CSS inline — só o necessário para above-the-fold */
</style>
<link rel="preload" href="/styles.css" as="style" onload="this.rel='stylesheet'">
```

Next.js, Vite plugins fazem isso automaticamente.

### content-visibility

Diz ao browser para não renderizar elementos fora do viewport (skip layout/paint):

```css
.item {
    content-visibility: auto;
    contain-intrinsic-size: 200px;  /* altura estimada */
}
```

Ganho significativo em listas longas.

### will-change

Hint para o browser otimizar:

```css
.animating {
    will-change: transform;
}
```

**Cuidado:** não aplicar sempre. É custoso em memória. Use só durante animação, remova depois.

### Outras otimizações

- **CSS Grid e Flex** em vez de `float` e `position: absolute`
- **`transform` e `opacity`** em animações (GPU)
- **`object-fit`** em imagens
- **Preload fontes críticas:** `<link rel="preload" as="font" href="/fonts/inter.woff2" crossorigin>`
- **Font-display:** `font-display: swap` para não bloquear render

---

## Armadilhas comuns

- **Não usar `box-sizing: border-box`** — defaults quebram layouts
- **Margins colapsando** — pai de filho com margin não aumenta como esperado
- **Z-index sem stacking context** — z-index alto que não funciona
- **Flexbox filho com `min-width`** — filho não encolhe
- **Grid com items de tamanhos variados** — usar `minmax(0, 1fr)` para evitar overflow
- **Específicidade explosiva** — `!important` e seletores super específicos
- **Animação de propriedades que causam reflow** — use `transform` e `opacity`
- **`position: absolute` sem `position: relative` no pai** — vai para a janela
- **`overflow: hidden` sem considerar acessibilidade** — esconde focus
- **`display: none` vs `visibility: hidden`** — o primeiro remove do fluxo, o segundo não
- **Fonts sem fallback** — FOIT (flash of invisible text)
- **Imagens sem `width`/`height`** — layout shift (CLS)
- **Classes órfãs após refactoring** — CSS morto
- **Media queries para mobile-first mas com `max-width`** — inconsistente
- **Não considerar dark mode**
- **Color contrast baixo** — inacessível
- **Focus outline removido sem substituto** — keyboard users ficam perdidos
- **`em` em vez de `rem`** — compounding imprevisível
- **`%` para height sem pai com height definido** — não funciona
- **`viewport-fit=cover` sem considerar safe areas** — iOS notch

---

## Na prática (da minha experiência)

> **Stack de styling no MedEspecialista:**
>
> **1. Tailwind CSS 4 + shadcn/ui.** Tailwind 4 com oxide engine é rápido, config em CSS, e shadcn/ui dá primitives de alto nível que customizo com Tailwind. Combo imbatível em 2026.
>
> **2. Design tokens via CSS variables.** Mesmo com Tailwind, defino tokens core em CSS variables para permitir themes dinâmicos e uso fora do Tailwind quando preciso.
>
> **3. Mobile-first religiosamente.** Começo com layout mobile, adiciono breakpoints para telas maiores. Código mais limpo.
>
> **4. Container queries para componentes reutilizáveis.** Cards e sidebar items se adaptam ao container, não ao viewport. Permite reutilização sem media queries por posição.
>
> **5. `prefers-reduced-motion` sempre respeitado.** Animações reduzidas para quem configurou. Acessibilidade não é negociável.
>
> **6. Semantic HTML primeiro.** `<button>`, `<nav>`, `<main>`, `<article>` — não `<div>` genérico. Passa por screen readers e facilita testes com Testing Library (`getByRole`).
>
> **7. A11y testing.** axe-core (Vitest) + Lighthouse CI. Acessibilidade é parte do PR review.
>
> **Incidente memorável — layout shift severo:**
>
> Landing page tinha CLS (Cumulative Layout Shift) de 0.8 (ruim). Causa: imagens sem `width`/`height` explicit, fonts carregando depois do texto, e CLS massivo. Correções:
>
> 1. `width` e `height` em todas as imagens, browser reserva espaço
> 2. `font-display: optional` com fallback metric-compatible
> 3. `aspect-ratio` em containers de imagem
> 4. Preload fontes críticas
>
> CLS caiu para 0.02. LCP melhorou 40% também.
>
> **Outro — specificity war:**
>
> Projeto antigo tinha CSS com `!important` em tudo. Ninguém conseguia override porque todos usavam `!important`. Migrei gradualmente para cascade layers — `@layer reset, base, components, utilities`. Utilities sempre vencem components sem precisar de `!important`. Paz.
>
> **CSS variables como design tokens:**
>
> ```css
> :root {
>     --space-1: 0.25rem;
>     --space-2: 0.5rem;
>     --space-4: 1rem;
>     --space-8: 2rem;
> }
> ```
>
> Quando o designer muda o spacing system, mudo em um lugar. Componentes usam as variables. Dark mode é só mudar as variables de color em `[data-theme="dark"]`.
>
> **A lição principal:** CSS moderno em 2026 é **incrivelmente poderoso**. Grid e Flexbox resolvem 95% dos layouts. `:has`, container queries, cascade layers resolvem o resto. HTML semântico + CSS moderno + Tailwind = produtividade máxima. Invista em entender o box model, specificity, e layout — o resto é vocabulário.

---

## How to explain in English

> "Modern HTML and CSS in 2026 are genuinely enjoyable. HTML semantic elements like `<main>`, `<article>`, `<section>` give you accessibility and SEO benefits for free. I use `<button>`, `<nav>`, `<dialog>` instead of `<div>` with JavaScript whenever possible — Testing Library's `getByRole` rewards this approach directly.
>
> For layout, Flexbox handles one-dimensional alignment (navigation, cards, centered content) and Grid handles two-dimensional layouts (full page structure, dashboards). I combine both — Grid for the macro, Flex for the micro. Subgrid, added in 2023, lets nested items align to the parent grid, which is finally a proper solution for complex forms and cards.
>
> Container queries changed how I think about responsive design. Instead of responding to the viewport, components respond to their container, which means truly reusable components that adapt whether they're in a sidebar or the main content area.
>
> For the styling stack, I use Tailwind CSS 4 with shadcn/ui components in React projects. Tailwind 4's Oxide engine is blazingly fast and the CSS-first config is nicer than the old JavaScript config. Utility-first means no naming stress, no dead CSS, and consistent spacing through a design system.
>
> Custom properties — CSS variables — are the backbone of my design tokens. Colors, spacing, typography scale, all defined in `:root` with dark mode overrides via `[data-theme="dark"]`. Even with Tailwind, I keep core tokens as CSS variables.
>
> Accessibility is not optional. I test with keyboard navigation, screen readers, and axe-core in CI. I respect `prefers-reduced-motion`, ensure 4.5:1 contrast, use labels on form fields, and never remove focus outlines without a proper replacement.
>
> Performance — I optimize what matters: avoid layout shift with explicit image dimensions, use `transform` and `opacity` for animations, load fonts with `font-display: swap`, and use `content-visibility: auto` for long lists. Lighthouse CI catches regressions."

### Frases úteis em entrevista

- "Semantic HTML first — `<button>` not `<div onClick>`."
- "Grid for 2D layout, Flex for 1D alignment — often combined."
- "Container queries for truly reusable components."
- "Mobile-first with `min-width` media queries, always."
- "`box-sizing: border-box` reset as baseline."
- "CSS variables for design tokens — theming becomes trivial."
- "Tailwind for productivity, shadcn/ui for components."
- "Animate only `transform` and `opacity` for GPU acceleration."
- "Always respect `prefers-reduced-motion`."
- "Never remove focus outlines without a replacement."
- "`content-visibility` and lazy loading for long lists."
- "Accessibility is not optional — tested in CI with axe-core."

### Key vocabulary

- marcação semântica → semantic markup
- acessibilidade → accessibility (a11y)
- caixa → box (model)
- preenchimento → padding
- margem → margin
- borda → border
- flutuante → float
- especificidade → specificity
- cascata → cascade
- camadas de cascata → cascade layers
- consulta de mídia → media query
- consulta de contêiner → container query
- propriedade customizada → custom property (CSS variable)
- tokens de design → design tokens
- desempenho → performance
- reflow / repaint → reflow / repaint
- deslocamento de layout → layout shift (CLS)
- leitor de tela → screen reader
- contraste de cor → color contrast
- navegação por teclado → keyboard navigation
- apresentação → presentation
- estrutura → structure
- utility-first → utility-first

---

## Recursos

### Documentação

- [MDN HTML](https://developer.mozilla.org/en-US/docs/Web/HTML)
- [MDN CSS](https://developer.mozilla.org/en-US/docs/Web/CSS)
- [MDN Accessibility](https://developer.mozilla.org/en-US/docs/Web/Accessibility)
- [Web.dev](https://web.dev/) — Google, performance + a11y + modern features
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [Can I Use](https://caniuse.com/) — browser support

### Blogs e tutoriais

- [Josh Comeau](https://www.joshwcomeau.com/) — tutorials CSS visuais fantásticos
- [CSS Tricks](https://css-tricks.com/)
- [Smashing Magazine](https://www.smashingmagazine.com/)
- [Ahmad Shadeed](https://ishadeed.com/) — deep CSS
- [Web Dev Simplified](https://www.youtube.com/@WebDevSimplified)
- [Kevin Powell](https://www.youtube.com/@KevinPowell) — CSS YouTube essential

### Livros

- **CSS: The Definitive Guide** — Eric Meyer
- **Responsive Web Design** — Ethan Marcotte
- **Inclusive Components** — Heydon Pickering
- **Refactoring UI** — Adam Wathan, Steve Schoger (criadores do Tailwind)

### Cursos

- [Full Stack Open Part 2 e 7](https://fullstackopen.com/en/) — CSS em React
- [Josh Comeau — CSS for JavaScript Developers](https://css-for-js.dev/)
- [Kevin Powell — Conquering Responsive Layouts](https://courses.kevinpowell.co/conquering-responsive-layouts)

### Ferramentas

- [axe DevTools](https://www.deque.com/axe/) — a11y testing
- [Lighthouse](https://developer.chrome.com/docs/lighthouse) — performance + a11y
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [CSS Grid Generator](https://cssgrid-generator.netlify.app/)
- [Flexbox Froggy](https://flexboxfroggy.com/) — aprender Flex brincando
- [Grid Garden](https://cssgridgarden.com/) — aprender Grid brincando
- [Coolors](https://coolors.co/) — paletas
- [Fontsource](https://fontsource.org/) — fontes self-hosted

### Referências de design system

- [Radix UI](https://www.radix-ui.com/) — primitives acessíveis
- [shadcn/ui](https://ui.shadcn.com/)
- [Material Design](https://m3.material.io/)
- [Apple HIG](https://developer.apple.com/design/human-interface-guidelines/)
- [GOV.UK Design System](https://design-system.service.gov.uk/) — accessibility-first

---

## Veja também

- [[React]] — integração com React
- [[JavaScript Fundamentals]] — base da web
- [[TypeScript]] — tipagem
- [[Testes em JavaScript]] — testes de componentes e a11y
- [[Full Stack Open - Guia de Revisão]] — CSS em React apps
- [[API Design]] — APIs que alimentam UIs
- [[System Design]] — performance em sistemas distribuídos
- [[Bootstrap]] — framework CSS
- [[Material UI]] — React components
- [[03-Dominios/JavaScript/Frontend/Mantine]] — React components
