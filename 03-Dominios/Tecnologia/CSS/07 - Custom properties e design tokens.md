---
title: "Custom properties e design tokens"
created: 2026-06-27
updated: 2026-06-27
type: note
fase: adepto
tags:
  - css
  - frontend
  - web
  - design-tokens
  - custom-properties
  - entrevista
publish: true
---

# Custom properties e design tokens

> [!abstract] TL;DR
> Custom properties (variáveis CSS) são a infraestrutura de design tokens em CSS puro — sem pré-processadores. A diferença fundamental das variáveis Sass: custom properties **vivem no DOM**, são herdadas, e podem ser lidas e escritas por JavaScript em tempo de execução. `@property` adiciona tipagem, validação, e habilita animação de valores que normalmente não são animáveis. Dark mode, theming e spacing systems consistentes se tornam triviais quando a base é bem estruturada em `:root`.

---

## O que são custom properties

Custom properties são declaradas com `--` e acessadas com `var()`:

```css
:root {
  --color-primary: oklch(60% 0.18 250);
  --space-md: 1rem;
}

.btn {
  background: var(--color-primary);
  padding: var(--space-md);
}
```

Diferença fundamental das variáveis Sass (`$variavel`):
- **Sass**: compilada em tempo de build, não existe no browser, não pode ser alterada em runtime
- **Custom properties**: existem no DOM, são herdadas, lidas/escritas por JS, afetadas pela cascade

```javascript
// Ler custom property
const root = document.documentElement;
const primary = getComputedStyle(root).getPropertyValue('--color-primary').trim();

// Escrever custom property
root.style.setProperty('--color-primary', 'oklch(55% 0.20 30)');
// Todos os elementos que usam var(--color-primary) atualizam instantaneamente
```

---

## Herança e escopo

Custom properties se propagam pelo DOM como propriedades CSS herdadas:

```css
/* Global — disponível em todo o documento */
:root {
  --space-md: 1rem;
}

/* Local — sobrescreve para este elemento e seus descendentes */
.card {
  --space-md: 0.75rem;
}

/* .card usa 0.75rem; elementos fora usam 1rem */
```

Isso permite **theming por componente** sem classes modificadoras:

```css
/* Componente usa --color-accent, sem saber qual cor é */
.badge {
  background: var(--color-accent);
  color: var(--color-accent-text);
}

/* Diferentes contextos definem cores diferentes */
.success-context {
  --color-accent: oklch(65% 0.18 145);
  --color-accent-text: white;
}

.danger-context {
  --color-accent: oklch(55% 0.22 25);
  --color-accent-text: white;
}
```

---

## Valores de fallback

`var()` aceita um segundo argumento como fallback — usado quando a variável não está definida:

```css
.elemento {
  /* Fallback simples */
  color: var(--color-text, #1a1a1a);

  /* Fallback em cadeia */
  color: var(--color-text, var(--color-fallback, black));

  /* Fallback com função */
  background: var(--color-bg, oklch(98% 0.01 250));
}
```

> [!warning] Fallback não valida o tipo
> Se `--color-text` está definida mas com um valor inválido (ex: `--color-text: nao-e-cor`), o fallback **não é usado** — o CSS usa o valor inicial da propriedade. Fallback só entra quando a variável **não está definida**.

---

## Design tokens: estrutura em `:root`

Design tokens são os valores primitivos que definem a identidade visual — cores, espaçamento, tipografia, sombras, radii. A estrutura recomendada em `:root`:

```css
:root {
  /* ========== CORES ========== */

  /* Paleta primitiva — valores brutos */
  --blue-50:  oklch(97% 0.03 250);
  --blue-100: oklch(93% 0.07 250);
  --blue-500: oklch(60% 0.18 250);
  --blue-700: oklch(45% 0.20 250);
  --blue-900: oklch(25% 0.12 250);

  --gray-50:  oklch(98% 0.01 250);
  --gray-100: oklch(95% 0.01 250);
  --gray-500: oklch(60% 0.01 250);
  --gray-900: oklch(18% 0.01 250);

  /* Tokens semânticos — mapeiam a paleta para papéis */
  --color-primary:       var(--blue-500);
  --color-primary-hover: var(--blue-700);
  --color-primary-text:  white;

  --color-bg:        var(--gray-50);
  --color-bg-raised: white;
  --color-text:      var(--gray-900);
  --color-text-muted: var(--gray-500);
  --color-border:    var(--gray-100);

  --color-danger:   oklch(55% 0.22 25);
  --color-success:  oklch(65% 0.18 145);
  --color-warning:  oklch(75% 0.18 80);
  --color-info:     oklch(65% 0.15 220);

  /* ========== ESPAÇAMENTO ========== */
  /* Escala em múltiplos de 4px (0.25rem = 4px) */
  --space-1:  0.25rem;  /* 4px */
  --space-2:  0.5rem;   /* 8px */
  --space-3:  0.75rem;  /* 12px */
  --space-4:  1rem;     /* 16px */
  --space-6:  1.5rem;   /* 24px */
  --space-8:  2rem;     /* 32px */
  --space-12: 3rem;     /* 48px */
  --space-16: 4rem;     /* 64px */

  /* ========== TIPOGRAFIA ========== */
  --font-sans:  system-ui, -apple-system, sans-serif;
  --font-mono:  ui-monospace, 'JetBrains Mono', monospace;

  --text-xs:  0.75rem;  /* 12px */
  --text-sm:  0.875rem; /* 14px */
  --text-base: 1rem;    /* 16px */
  --text-lg:  1.125rem; /* 18px */
  --text-xl:  1.25rem;  /* 20px */
  --text-2xl: 1.5rem;   /* 24px */
  --text-3xl: 1.875rem; /* 30px */

  --leading-tight:  1.25;
  --leading-normal: 1.5;
  --leading-relaxed: 1.75;

  /* ========== GEOMETRIA ========== */
  --radius-sm:  0.25rem;
  --radius-md:  0.5rem;
  --radius-lg:  0.75rem;
  --radius-xl:  1rem;
  --radius-full: 9999px; /* pill */

  /* ========== SOMBRAS ========== */
  --shadow-sm: 0 1px 2px oklch(0% 0 0 / 0.08);
  --shadow-md: 0 4px 6px oklch(0% 0 0 / 0.07), 0 2px 4px oklch(0% 0 0 / 0.06);
  --shadow-lg: 0 10px 15px oklch(0% 0 0 / 0.10), 0 4px 6px oklch(0% 0 0 / 0.05);

  /* ========== TRANSIÇÕES ========== */
  --duration-fast:   150ms;
  --duration-normal: 250ms;
  --duration-slow:   400ms;
  --ease-default:    ease;
  --ease-spring:     cubic-bezier(0.34, 1.56, 0.64, 1);
}
```

---

## Dark mode com custom properties

A vantagem dos tokens semânticos: dark mode é apenas redefinir os tokens — o código dos componentes não muda:

```css
/* Light mode (default) */
:root {
  --color-bg:     oklch(98% 0.01 250);
  --color-bg-raised: white;
  --color-text:   oklch(18% 0.01 250);
  --color-border: oklch(90% 0.01 250);
}

/* Dark mode via preferência do sistema */
@media (prefers-color-scheme: dark) {
  :root {
    --color-bg:     oklch(12% 0.01 250);
    --color-bg-raised: oklch(16% 0.01 250);
    --color-text:   oklch(92% 0.01 250);
    --color-border: oklch(25% 0.01 250);
  }
}

/* Dark mode via atributo (toggle manual) */
[data-theme="dark"] {
  --color-bg:     oklch(12% 0.01 250);
  --color-bg-raised: oklch(16% 0.01 250);
  --color-text:   oklch(92% 0.01 250);
  --color-border: oklch(25% 0.01 250);
}

/* Informar ao browser sobre o esquema para ajustar scrollbars, inputs etc. */
:root {
  color-scheme: light dark;
}

[data-theme="dark"] {
  color-scheme: dark;
}
```

```javascript
// Toggle de dark mode
function toggleTheme() {
  const root = document.documentElement;
  const current = root.getAttribute('data-theme');
  root.setAttribute('data-theme', current === 'dark' ? 'light' : 'dark');
  localStorage.setItem('theme', root.getAttribute('data-theme'));
}

// Restaurar preferência salva
const saved = localStorage.getItem('theme');
if (saved) document.documentElement.setAttribute('data-theme', saved);
```

---

## `@property` — tipagem de custom properties

`@property` declara explicitamente o tipo de uma custom property, habilita valores iniciais, e crucialmente, **permite animação**:

```css
@property --hue {
  syntax: '<number>';
  inherits: false;
  initial-value: 250;
}

@property --opacity-overlay {
  syntax: '<number>';
  inherits: true;
  initial-value: 0;
}

@property --progress {
  syntax: '<percentage>';
  inherits: false;
  initial-value: 0%;
}
```

Sem `@property`, custom properties não são animáveis — o browser as trata como strings opacas:

```css
/* ❌ Sem @property: não anima — muda instantaneamente */
.elemento {
  --hue: 250;
  background: oklch(60% 0.15 var(--hue));
  transition: --hue 1s; /* ignorado */
}
.elemento:hover { --hue: 30; }

/* ✅ Com @property: anima suavemente */
@property --hue {
  syntax: '<number>';
  inherits: false;
  initial-value: 250;
}

.elemento {
  background: oklch(60% 0.15 var(--hue));
  transition: --hue 0.8s ease;
}
.elemento:hover { --hue: 30; }
/* Fundo anima suavemente de azul para laranja */
```

### Tipos suportados por `@property`

```css
@property --tamanho {
  syntax: '<length>';          /* rem, px, em, etc. */
  inherits: true;
  initial-value: 0px;
}

@property --cor {
  syntax: '<color>';           /* qualquer valor de cor */
  inherits: false;
  initial-value: transparent;
}

@property --angulo {
  syntax: '<angle>';           /* deg, rad, turn */
  inherits: false;
  initial-value: 0deg;
}

@property --numero {
  syntax: '<number>';          /* sem unidade */
  inherits: false;
  initial-value: 0;
}

@property --porcentagem {
  syntax: '<percentage>';      /* com % */
  inherits: false;
  initial-value: 0%;
}

@property --inteiro {
  syntax: '<integer>';
  inherits: false;
  initial-value: 0;
}
```

---

## Custom properties em JavaScript

```javascript
// Lendo o valor computado
const el = document.querySelector('.btn');
const primary = getComputedStyle(el).getPropertyValue('--color-primary').trim();

// Setando no elemento
el.style.setProperty('--color-primary', 'oklch(55% 0.22 25)');

// Setando globalmente (afeta todos)
document.documentElement.style.setProperty('--color-primary', 'oklch(55% 0.22 25)');

// Removendo (volta ao valor da cascade)
el.style.removeProperty('--color-primary');

// Theming dinâmico — mudar múltiplos tokens de uma vez
function applyTheme(tokens) {
  const root = document.documentElement;
  Object.entries(tokens).forEach(([key, value]) => {
    root.style.setProperty(key, value);
  });
}

applyTheme({
  '--color-primary': 'oklch(60% 0.22 30)',  /* laranja */
  '--radius-md': '0px',                      /* bordas retas */
});
```

---

## Anti-padrões comuns

```css
/* ❌ Tokens com nomes não-semânticos */
:root {
  --blue: #3b82f6;   /* nome descreve cor, não papel */
}
.btn { background: var(--blue); }
/* Se o design mudar para verde, o token chama "blue" mas é verde */

/* ✅ Tokens semânticos */
:root {
  --color-primary: oklch(60% 0.18 250);
}
.btn { background: var(--color-primary); }

/* ❌ Custom property sem fallback onde pode não estar definida */
.widget { color: var(--widget-color); }
/* Se --widget-color não existir, color usa valor inicial — pode ser inesperado */

/* ✅ Com fallback */
.widget { color: var(--widget-color, var(--color-text)); }

/* ❌ Usar custom property onde não é necessário */
:root { --margin-left-do-botao-especifico: 12px; }
/* Excesso de tokens polui o espaço global */

/* ✅ Escopo local para tokens de componente */
.botao-especifico { margin-left: 12px; }
```

---

> [!question] Para fixar
> 1. Qual a diferença fundamental entre variáveis CSS (`--cor`) e variáveis Sass (`$cor`)? Quando cada uma é mais adequada?
> 2. Por que tokens semânticos (`--color-primary`) são preferíveis a tokens de paleta (`--blue-500`) para o código dos componentes?
> 3. Como você implementaria dark mode usando custom properties e um atributo `data-theme`? Escreva o padrão completo.
> 4. O que `@property` adiciona a uma custom property que a declaração `--nome: valor` não tem? Dê um exemplo concreto.
> 5. Custom properties são herdadas pelo DOM. Como você usaria isso para criar theming por componente sem classes modificadoras?
> 6. Um valor `var(--cor, azul)` onde `--cor` está definida como `vermelho-invalido`. Qual cor é usada? Por quê?

---

## Veja também

- [[03-Dominios/Tecnologia/CSS/06 - Design responsivo - media queries e container queries|06 — Design responsivo]] — anterior
- [[03-Dominios/Tecnologia/CSS/08 - Seletores modernos - has, is, where e nesting|08 — Seletores modernos]] — próxima
- [[03-Dominios/Tecnologia/CSS/09 - Animações e transitions|09 — Animações]] — `@property` animável em ação
- [[03-Dominios/Tecnologia/CSS/02 - Unidades, cores e tipografia|02 — Unidades e cores]] — `oklch` como base dos tokens de cor
