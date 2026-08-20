---
title: "Seletores modernos: :has(), :is(), :where() e nesting"
created: 2026-06-27
updated: 2026-06-27
type: note
fase: adepto
tags:
  - css
  - frontend
  - web
  - seletores
  - has
  - nesting
  - entrevista
publish: true
---

# Seletores modernos: :has(), :is(), :where() e nesting

> [!abstract] TL;DR
> `:has()` é o "parent selector" que a web não tinha — seleciona um elemento baseado nos seus descendentes ou irmãos, abrindo patterns impossíveis antes. `:is()` e `:where()` eliminam seletor repetitivo (mesmo resultado, especificidades diferentes). CSS Nesting elimina o pré-processador para estrutura de seletores. Juntos, esses quatro recursos tornam o CSS mais expressivo sem aumentar a contagem de bytes.

---

## `:is()` — agrupamento sem repetição

Antes de `:is()`, agrupar seletores com contextos diferentes exigia repetir os sufixos:

```css
/* ❌ Repetitivo */
.card h1, .card h2, .card h3,
.modal h1, .modal h2, .modal h3,
.article h1, .article h2, .article h3 {
  line-height: 1.25;
}

/* ✅ Com :is() */
:is(.card, .modal, .article) :is(h1, h2, h3) {
  line-height: 1.25;
}
```

A especificidade de `:is()` é a do **seletor mais específico** dentro dos parênteses:

```css
:is(h1, h2, .titulo) { color: blue; }
/* Especificidade: (0, 1, 0) — .titulo é o mais específico */

:is(#destaque, .card, p) { margin: 0; }
/* Especificidade: (1, 0, 0) — #destaque é o mais específico */
```

> [!warning] Armadilha de especificidade
> Se você misturar IDs com classes em `:is()`, todos os seletores herdam a especificidade mais alta. Prefira `:where()` quando quiser especificidade zero, ou mantenha `:is()` com seletores de mesmo nível de especificidade.

---

## `:where()` — agrupamento sem especificidade

`:where()` funciona exatamente como `:is()` mas **tem especificidade zero** — sempre:

```css
:where(h1, h2, h3, h4, h5, h6) { line-height: 1.25; }
/* Especificidade: (0, 0, 0) — qualquer outro seletor vence */
```

Isso torna `:where()` ideal para resets, estilos base, e bibliotecas de componentes onde você quer que o usuário possa sobrescrever facilmente:

```css
/* Reset que nunca vai entrar em guerra de especificidade */
:where(*, *::before, *::after) {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

/* Estilos base que qualquer classe simples pode sobrescrever */
:where(h1, h2, h3, h4, h5, h6) {
  font-weight: 700;
  line-height: 1.25;
}

/* O usuário sobrescreve com (0, 1, 0) — especificidade baixíssima, já suficiente */
.section-title { font-weight: 400; }
```

### `:is()` vs `:where()` — quando usar cada um

| Situação | Use |
|---|---|
| Resets e estilos base de biblioteca | `:where()` — especificidade zero facilita override |
| Agrupamento de seletores no seu CSS | `:is()` — especificidade do argumento mais alto |
| Você quer que usuários sobrescrevam facilmente | `:where()` |
| Você quer consistência de especificidade | `:is()` com seletores do mesmo nível |

---

## `:not()` — exclusão com lógica de lista

`:not()` aceita lista de seletores (desde Selectors Level 4):

```css
/* Seleciona todos os li exceto o primeiro e o último */
li:not(:first-child, :last-child) {
  border-top: 1px solid var(--color-border);
}

/* Links externos (com href que começa com http) */
a:not([href^="/"]):not([href^="#"]) {
  color: var(--color-external);
}

/* Input que não é checkbox, radio nem submit */
input:not([type="checkbox"], [type="radio"], [type="submit"]) {
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
}

/* Todo card exceto o destacado */
.card:not(.card--featured) {
  opacity: 0.8;
}
```

A especificidade de `:not()` é a do seletor mais específico dentro:

```css
:not(#id) { /* especificidade: (1, 0, 0) */ }
:not(.class) { /* especificidade: (0, 1, 0) */ }
:not(div) { /* especificidade: (0, 0, 1) */ }
```

---

## `:has()` — o seletor de pai (e contexto)

`:has()` é a mudança mais significativa em CSS seletores em uma década. Seleciona um elemento que **tem** um descendente correspondente ao argumento:

```css
/* Seleciona .card que contém uma img */
.card:has(img) {
  padding: 0;
}

/* Seleciona label que contém um input em foco */
label:has(input:focus) {
  color: var(--color-primary);
  font-weight: 600;
}

/* Seleciona form com campos inválidos */
form:has(:invalid) {
  border-color: var(--color-danger);
}

/* Parágrafo imediatamente após um h2 */
h2 + p { }
/* Mas com :has(), selecionar o h2 que tem um p como próximo irmão */
h2:has(+ p) {
  margin-bottom: 0;
}
```

### Casos de uso que `:has()` desbloqueia

**1. Layout condicional baseado no conteúdo**

```css
/* Card sem imagem → padding normal */
.card { padding: 1.5rem; }

/* Card com imagem → sem padding no topo (imagem sangra até a borda) */
.card:has(> .card__image:first-child) {
  padding-top: 0;
}

/* Grid de 3 colunas quando há 3+ items */
.grid:has(.item:nth-child(3)) {
  grid-template-columns: repeat(3, 1fr);
}
```

**2. Form UX sem JavaScript**

```css
/* Label muda quando seu input está preenchido */
.field:has(input:not(:placeholder-shown)) .field__label {
  transform: translateY(-1.5rem) scale(0.85);
  color: var(--color-primary);
}

/* Mensagem de erro aparece quando input é inválido E já foi tocado */
.field:has(input:invalid:not(:focus):not(:placeholder-shown)) .field__error {
  display: block;
}

/* Botão de submit desabilitado visualmente quando form tem inválidos */
form:has(:invalid) .btn--submit {
  opacity: 0.5;
  cursor: not-allowed;
}
```

**3. Seleção de irmão anterior — impossível antes**

```css
/* :has() com seletor de irmão + e ~ */

/* li anterior ao li em hover (via pai) */
li:has(+ li:hover) {
  opacity: 0.5; /* o item antes do hovered fica opaco */
}

/* Todos os li antes do hovered */
li:has(~ li:hover) {
  opacity: 0.5;
}
```

**4. Dark mode de componente baseado em contexto**

```css
/* Nav especial quando o header tem classe .hero */
header:has(.hero) nav {
  background: transparent;
  color: white;
}
```

---

## `:nth-child()` com seletor — refinamento

CSS Selectors 4 permite passar um seletor de filtro para `:nth-child()`:

```css
/* O 2° elemento p (ignora outros elementos) */
p:nth-child(2 of p) { }

/* O 1° .card — entre todos os filhos, o 1° que é .card */
.card:nth-child(1 of .card) { }
/* Antes: :first-child só funcionava se .card fosse o 1° filho real */

/* Todo .card par */
.card:nth-child(even of .card) {
  background: var(--color-bg-raised);
}
```

---

## CSS Nesting

CSS Nesting (nativo, sem Sass) permite escrever seletores aninhados dentro de regras pai:

```css
/* Sem nesting — repetição de contexto */
.card { border: 1px solid var(--color-border); }
.card:hover { border-color: var(--color-primary); }
.card .card__title { font-size: 1.25rem; }
.card .card__title:first-child { margin-top: 0; }
.card--featured { border-color: var(--color-primary); }

/* Com nesting — co-localizado, sem repetição */
.card {
  border: 1px solid var(--color-border);

  &:hover {
    border-color: var(--color-primary);
  }

  .card__title {
    font-size: 1.25rem;

    &:first-child {
      margin-top: 0;
    }
  }

  &--featured {                         /* .card--featured */
    border-color: var(--color-primary);
  }
}
```

### Regras de nesting

O `&` representa o seletor pai. Pode ser omitido em alguns casos, mas é mais seguro e legível incluir:

```css
.parent {
  color: blue;

  /* & explícito — recomendado */
  & .child { color: red; }
  &:hover { color: green; }
  &.modifier { color: purple; }

  /* Sem & — só funciona com seletores de elemento/classe/id */
  .child { color: red; }          /* equivale a .parent .child */

  /* & pode aparecer em qualquer posição */
  .grandparent & { color: orange; } /* .grandparent .parent */
}
```

### Nesting com at-rules

```css
.card {
  padding: 1rem;

  /* Media query aninhada */
  @media (width >= 768px) {
    padding: 2rem;
    display: grid;
    grid-template-columns: 150px 1fr;
  }

  /* Container query aninhada */
  @container (width >= 400px) {
    flex-direction: row;
  }

  /* Layer aninhado */
  @layer overrides {
    &.special { border: 2px solid red; }
  }
}
```

### Nesting BEM — o melhor dos dois mundos

```css
.card {
  /* Block */
  display: flex;
  flex-direction: column;

  /* Elements */
  &__header {
    padding: 1rem;
    border-bottom: 1px solid var(--color-border);
  }

  &__body {
    flex: 1;
    padding: 1rem;
  }

  &__footer {
    padding: 0.75rem 1rem;
    background: var(--color-bg);
  }

  /* Modifiers */
  &--featured {
    border: 2px solid var(--color-primary);
  }

  &--compact {
    .card__header,
    .card__body,
    .card__footer { padding: 0.5rem; }
  }

  /* States */
  &:hover { box-shadow: var(--shadow-md); }
  &:focus-within { outline: 2px solid var(--color-primary); }
}
```

---

## Combinação: `:has()` + nesting

```css
/* Formulário que se adapta ao estado dos inputs, todo co-localizado */
.field {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;

  &__label {
    font-size: var(--text-sm);
    color: var(--color-text-muted);
    transition: color var(--duration-fast);
  }

  &__input {
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    padding: 0.5rem 0.75rem;

    &:focus {
      outline: 2px solid var(--color-primary);
      border-color: var(--color-primary);
    }

    &:invalid:not(:focus):not(:placeholder-shown) {
      border-color: var(--color-danger);
    }
  }

  &__error {
    display: none;
    font-size: var(--text-xs);
    color: var(--color-danger);
  }

  /* :has() no pai reage ao estado do filho */
  &:has(.field__input:focus) .field__label {
    color: var(--color-primary);
  }

  &:has(.field__input:invalid:not(:focus):not(:placeholder-shown)) {
    .field__error { display: block; }
    .field__label { color: var(--color-danger); }
  }
}
```

---

## Suporte e fallbacks

| Recurso | Suporte |
|---|---|
| `:is()` e `:where()` | Todos os browsers modernos (desde 2021) |
| `:has()` | Chrome 105+, Safari 15.4+, Firefox 121+ (2024) |
| CSS Nesting | Chrome 112+, Safari 16.5+, Firefox 117+ (2023) |
| `:nth-child(n of selector)` | Chrome 111+, Safari 15.4+, Firefox 113+ |

Para `:has()`, o progressive enhancement é a abordagem correta — estilos sem `:has()` como base, e refinamentos com `:has()` que degradam graciosamente:

```css
/* Base: funciona em todos os browsers */
.card { padding: 1.5rem; }

/* Refinamento com :has() — browsers sem suporte ignoram */
@supports selector(:has(img)) {
  .card:has(> img:first-child) { padding-top: 0; }
}
```

---

> [!question] Para fixar
> 1. Qual a diferença de especificidade entre `:is(.card, #destaque)` e `:where(.card, #destaque)`? O que isso implica na prática?
> 2. O que `:has()` permite fazer que era impossível em CSS antes? Dê dois exemplos concretos.
> 3. Como você seleciona o `label` imediatamente antes de um `input:focus` usando só CSS (sem JavaScript)?
> 4. O que `&--modifier` dentro de `.block { }` gera? Qual seletor final?
> 5. Como `li:has(+ li:hover)` funciona? O que `+` faz dentro de `:has()`?
> 6. Quando você usaria `:nth-child(2 of .card)` em vez de `.card:nth-child(2)`? Qual é a diferença?

---

## Veja também

- [[03-Dominios/Tecnologia/CSS/07 - Custom properties e design tokens|07 — Custom properties]] — anterior
- [[03-Dominios/Tecnologia/CSS/09 - Animações e transitions|09 — Animações]] — próxima
- [[03-Dominios/Tecnologia/CSS/05 - Especificidade, cascade e layer|05 — Especificidade]] — cálculo de especificidade de `:is()` e `:not()`
- [[03-Dominios/Tecnologia/CSS/06 - Design responsivo - media queries e container queries|06 — Design responsivo]] — media queries dentro de nesting
