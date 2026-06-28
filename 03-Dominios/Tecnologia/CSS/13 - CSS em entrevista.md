---
title: "CSS em entrevista"
created: 2026-06-27
updated: 2026-06-27
type: note
fase: Magus
tags:
  - css
  - frontend
  - web
  - entrevista
  - capstone
publish: true
---

# CSS em entrevista

> [!abstract] TL;DR
> Entrevistas de CSS testam três dimensões: fundamentos (cascade, especificidade, box model), layout (Flexbox vs Grid, responsividade), e sistema (custom properties, arquitetura, performance). A maioria dos candidatos erra nas nuances dos fundamentos — especificidade, stacking context, margin collapsing — não no CSS moderno. Conhecer "como e quando" é mais valioso do que listar propriedades.

---

## Mapa do galho

```mermaid
mindmap
  root((CSS))
    Fundamentos
      Cascade
        Origem + importância
        Especificidade A,B,C
        Ordem no fonte
      Herança
        typographic props herdam
        layout não herda
        inherit/initial/unset/revert
      Box Model
        content-box vs border-box
        margin collapsing
        display e formatting context
    Unidades e Cores
      rem vs em vs px
      svh/dvh para viewport mobile
      oklch e color-mix
      clamp para fluid scaling
    Layout
      Flexbox
        eixo principal vs cruzado
        flex-grow/shrink/basis
        min-width 0
      Grid
        fr e repeat/minmax
        auto-fit vs auto-fill
        grid-template-areas
        subgrid
    Responsivo
      Mobile-first
      Range syntax
      Container queries
      prefers-reduced-motion
      Logical properties
    Sistema
      Custom properties
        herança e escopo DOM
        @property animável
        design tokens
        dark mode
      @layer
        ordem de camadas
        !important invertido
        isolamento de terceiros
    Seletores Modernos
      :has() parent selector
      :is() e :where()
      CSS Nesting
    Animações
      transition vs @keyframes
      transform e opacity GPU
      prefers-reduced-motion
      @property animável
    Arquitetura
      CSS Modules
      CSS-in-JS runtime
      Zero-runtime
      Tailwind utility-first
    Performance
      Critical CSS inline
      Render-blocking
      contain e content-visibility
      CLS e Core Web Vitals
```

---

## Top 10 perguntas em entrevista

### 1. "Explique o algoritmo de cascade"

O cascade resolve qual declaração vence quando múltiplas regras concorrem. Avalia na ordem:

1. **Transições em curso** — máxima prioridade
2. **`!important` do browser** — acessibilidade
3. **`!important` do usuário** — high contrast
4. **`!important` do autor** — seu CSS
5. **Animações em curso**
6. **CSS normal do autor** (especificidade → posição no fonte)
7. **CSS normal do usuário**
8. **CSS normal do browser**

Na prática do dia a dia: a maioria das decisões acontece no nível 6 — seu CSS, resolvido por **especificidade**. Especificidade é o trio (A, B, C): IDs = A, classes/pseudo-classes/atributos = B, elementos/pseudo-elementos = C. Comparação da esquerda para a direita — um ID sempre supera infinitas classes.

### 2. "Qual a diferença entre `display: block`, `inline`, e `inline-block`?"

| Valor | Ocupa linha inteira | Width/Height | Margem vertical |
|---|---|---|---|
| `block` | sim | sim | sim |
| `inline` | não | não | não |
| `inline-block` | não | sim | sim |

`display: flex` e `display: grid` criam um **formatting context** — seus filhos diretos participam do layout flex/grid em vez do fluxo normal.

### 3. "Explique o box model e `box-sizing`"

Todo elemento tem: `margin > border > padding > content`. Por padrão, `width` refere-se apenas ao **content box** (`box-sizing: content-box`): `width: 200px` + `padding: 20px` + `border: 1px` = 242px de largura real.

`box-sizing: border-box` muda o referencial: `width: 200px` inclui padding e border — o content area encolhe. É o reset mais adotado:

```css
*, *::before, *::after { box-sizing: border-box; }
```

### 4. "Quando usar Flexbox e quando usar Grid?"

| Flexbox | Grid |
|---|---|
| Layout em **uma dimensão** (linha ou coluna) | Layout em **duas dimensões** (linhas e colunas) |
| O conteúdo determina o espaço | O template determina o espaço |
| Navbar, listas, botão com ícone | Página, grade de cards, formulários multi-coluna |

Na prática: Grid para a arquitetura da página, Flexbox para os componentes internos. Os dois convivem — Grid no `body`, Flex dentro do `.card`.

### 5. "O que é stacking context e por que `z-index` às vezes não funciona?"

Um stacking context é um espaço 3D isolado de z-ordering. `z-index` só funciona **dentro do mesmo stacking context**. Elementos em stacking contexts diferentes são comparados pelo z-index de seus contextos, não o deles próprios.

O que cria um stacking context:
- `position: relative/absolute/fixed/sticky` com `z-index` diferente de `auto`
- `opacity < 1`
- `transform`, `filter`, `perspective`
- `will-change` com qualquer valor
- `isolation: isolate` (o mais previsível — cria sem efeito visual)

```css
/* ❌ z-index: 9999 não funciona porque o pai tem transform */
.pai { transform: translateZ(0); }
.filho { z-index: 9999; } /* limitado ao stacking context do pai */

/* ✅ Mover o elemento para o mesmo stacking context */
/* Ou usar um portal no React */

/* ✅ Criar stacking context explícito sem efeito visual */
.isolado { isolation: isolate; }
```

### 6. "O que são custom properties e como diferem de variáveis Sass?"

| Sass `$var` | CSS `--var` |
|---|---|
| Compilada, não existe no browser | Vive no DOM, herdada |
| Não pode ser lida/escrita por JS | `getComputedStyle` + `setProperty` |
| Não é afetada pela cascade em runtime | É uma propriedade CSS — herança e cascade se aplicam |
| Não é animável | Com `@property`, é animável |

Custom properties se propagam pelo DOM — um elemento pode definir `--color-accent` e todos os seus descendentes herdam automaticamente, sem passar como props.

### 7. "Como você implementaria dark mode?"

A abordagem mais robusta combina tokens semânticos e dual strategy (media + selector):

```css
:root {
  --color-bg:   oklch(98% 0.01 250);
  --color-text: oklch(18% 0.01 250);
}

/* Preferência do sistema */
@media (prefers-color-scheme: dark) {
  :root {
    --color-bg:   oklch(12% 0.01 250);
    --color-text: oklch(92% 0.01 250);
  }
}

/* Toggle manual */
[data-theme="dark"] {
  --color-bg:   oklch(12% 0.01 250);
  --color-text: oklch(92% 0.01 250);
}
```

Componentes só usam os tokens semânticos (`bg-[var(--color-bg)]`) — nunca cores diretas. Trocar de tema é apenas redefinir os tokens.

### 8. "Explique `@layer`"

`@layer` define uma hierarquia explícita de camadas CSS. Regras em camadas superiores vencem regras de camadas inferiores, **independente da especificidade dos seletores**:

```css
@layer reset, base, components, utilities;
/* utilities > components > base > reset */
/* .mt-4 em utilities vence .btn em components, mesmo com mesma especificidade */
```

O principal uso: isolar CSS de terceiros. CSS importado em uma layer perde para seu CSS normal:

```css
@layer external { @import url('bootstrap.min.css'); }
.btn { /* vence qualquer .btn do Bootstrap */ }
```

### 9. "Como `:has()` funciona e para que serve?"

`:has()` seleciona um elemento que **contém** um descendente correspondente ao seletor dentro dos parênteses. É o "parent selector" que o CSS nunca teve:

```css
/* Card sem imagem: padding normal */
.card { padding: 1.5rem; }

/* Card com imagem no topo: remove padding-top */
.card:has(> img:first-child) { padding-top: 0; }

/* Label muda quando seu input está em foco */
label:has(input:focus) { color: var(--color-primary); }

/* Form com campos inválidos */
form:has(:invalid) { border-color: var(--color-danger); }

/* Selecionar irmão ANTERIOR — impossível antes */
li:has(+ li:hover) { opacity: 0.5; }
```

### 10. "Por que `transform` é mais performático para animação do que `width`?"

O rendering pipeline tem etapas: Layout → Paint → Composite. Animar `width` ou `margin` aciona **Layout** — o browser recalcula a posição de todos os elementos afetados em cada frame. Em 60fps, isso é 16ms disponíveis por frame.

`transform` e `opacity` são **compositor-only** — o browser eleva o elemento para uma layer GPU e aplica a transformação sem repassar por Layout ou Paint. O resto da página não é afetado. `will-change: transform` faz o browser criar a layer antecipadamente.

---

## Perguntas de design de componente

### "Como você implementaria um accordion nativo sem JavaScript?"

```html
<!-- details/summary são nativos — sem JS necessário -->
<details name="faq">  <!-- name: todos com o mesmo nome se comportam como grupo -->
  <summary>Pergunta 1</summary>
  <p>Resposta 1</p>
</details>
<details name="faq">
  <summary>Pergunta 2</summary>
  <p>Resposta 2</p>
</details>
```

```css
/* Animação suave com @starting-style */
details[open] > :not(summary) {
  animation: slide-down 250ms ease;
}

@keyframes slide-down {
  from { opacity: 0; transform: translateY(-8px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* Remover triângulo padrão */
summary { list-style: none; cursor: pointer; }
summary::marker { display: none; }

/* Indicador customizado */
summary::after { content: '▾'; transition: transform 200ms; }
details[open] summary::after { transform: rotate(180deg); }
```

### "Como você implementaria um card grid que vai de 1 a 3 colunas automaticamente?"

```css
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
}
/* Zero media queries. auto-fit colapsa colunas vazias; minmax(280px, 1fr)
   define mínimo de 280px por coluna. Qualquer largura → colunas corretas. */
```

### "Como você faria um layout full-height com footer colado na base?"

```css
/* Abordagem 1: Flexbox */
body {
  display: flex;
  flex-direction: column;
  min-height: 100svh;
}
main { flex: 1; }

/* Abordagem 2: Grid */
body {
  display: grid;
  grid-template-rows: auto 1fr auto;
  min-height: 100svh;
}
```

---

## Armadilhas clássicas

### Margin collapsing

```css
/* Dois elementos block adjacentes — margens colapsam */
.a { margin-bottom: 2rem; }
.b { margin-top: 1rem; }
/* Gap entre eles: 2rem (o maior), não 3rem */

/* Quando NÃO colapsa: */
/* - display: flex/grid (filhos não colapsam) */
/* - padding ou border entre eles */
/* - overflow: hidden no pai */
/* - elementos com position: absolute/fixed */
```

### `min-width: 0` em flex items

```css
/* Flex item com texto longo causa overflow */
.flex-child { flex: 1; /* min-width: auto */ }

/* Fix: permite encolher abaixo do tamanho mínimo do conteúdo */
.flex-child { flex: 1; min-width: 0; }
```

### Especificidade inesperada com `:is()`

```css
/* :is() herda a especificidade mais alta */
:is(h1, #titulo, .header) { font-size: 2rem; }
/* Especificidade: (1, 0, 0) — por causa de #titulo */
/* .header que você esperava sobrescrever é mais difícil agora */
```

### `position: fixed` e `transform`

```css
/* position: fixed fica relativo ao viewport... exceto quando */
.pai { transform: translateZ(0); }
/* Qualquer transform/filter/perspective cria um stacking context
   e position: fixed no filho fica relativo a esse contexto, não ao viewport */
```

### Fallback de `var()` não usa valor de fallback

```css
:root { --cor: nao-e-uma-cor; }
p { color: var(--cor, black); }
/* Resultado: NÃO usa black — usa o valor inicial de color (preto, mas por razão errada).
   Fallback só entra quando a variável não está DEFINIDA, não quando é inválida. */
```

---

## Checklist pré-entrega de CSS

```markdown
## Fundamentos
- [ ] `*, *::before, *::after { box-sizing: border-box; }` no reset
- [ ] Nenhum `!important` sem comentário explicando necessidade
- [ ] Nenhum ID em seletores de componentes
- [ ] `isolation: isolate` em componentes que precisam de stacking context

## Layout
- [ ] Nenhuma propriedade `float` para layout (só para text wrapping)
- [ ] `min-width: 0` em flex items que podem ter overflow de texto
- [ ] `minmax(0, 1fr)` em vez de `1fr` em grids com conteúdo dinâmico
- [ ] Grid de cards com `repeat(auto-fit, minmax(Xpx, 1fr))` em vez de media queries

## Responsividade
- [ ] Mobile-first: CSS base sem media query, `min-width` para expandir
- [ ] Viewport meta tag no HTML: `<meta name="viewport" content="width=device-width">`
- [ ] `@media (prefers-reduced-motion: reduce)` para todas as animações
- [ ] Imagens com `width` e `height` explícitos (prevenção de CLS)
- [ ] Fontes com `font-display: swap` ou `optional`

## Custom properties
- [ ] Tokens semânticos (não de paleta) nos componentes
- [ ] Dark mode implementado via redefinição de tokens (não de propriedades individuais)
- [ ] `@property` para custom properties que precisam ser animadas

## Performance
- [ ] Animações apenas em `transform` e `opacity` (nunca `width`, `height`, `margin`)
- [ ] `will-change` apenas em elementos que definitivamente animam
- [ ] CSS crítico inline; restante assíncrono
```

---

## Veja também

- [[03-Dominios/Tecnologia/CSS/12 - Performance CSS|12 — Performance CSS]] — anterior
- [[03-Dominios/Tecnologia/CSS/01 - O modelo mental do CSS - cascade, herança e box model|01 — Modelo mental]] — cascade e box model em profundidade
- [[03-Dominios/Tecnologia/CSS/05 - Especificidade, cascade e layer|05 — Especificidade e @layer]] — algoritmo completo
- [[03-Dominios/Tecnologia/CSS/07 - Custom properties e design tokens|07 — Custom properties]] — dark mode e tokens
- [[03-Dominios/Tecnologia/HTML/12 - HTML em entrevista|HTML 12 — HTML em entrevista]] — capstone do galho HTML
