---
title: "Compositing e GPU layers"
created: 2026-06-28
updated: 2026-06-28
type: note
fase: Iniciado
tags:
  - plataforma-web
  - rendering
  - browser
  - performance
  - gpu
  - entrevista
publish: true
---

# Compositing e GPU layers

> [!abstract] TL;DR
> O browser divide a página em **layers** (camadas de bitmap) que são compostas pelo GPU. Elementos em sua própria layer são animados sem reflow ou repaint — só recomposição. `will-change: transform` ou `transform: translateZ(0)` promovem um elemento para sua própria GPU layer. O DevTools Layers panel mostra as layers ativas. Criar layers demais (layer explosion) usa memória excessiva — promova com critério.

---

## O que é compositing

Após layout e paint, o browser tem bitmaps renderizados para cada região da página. O **compositor** combina esses bitmaps no frame final usando o GPU:

```
Layout → Paint (bitmaps por região) → Compositor GPU (combina em frame)
```

Elementos em **layers separadas** podem ser movidos, escalados ou alterados em opacidade pelo GPU sem retornar ao CPU para layout ou paint. É por isso que `transform` e `opacity` são gratuitos para animação.

---

## O que cria uma GPU layer

O browser promove automaticamente elementos que têm:

```css
/* Posição 3D */
transform: translateZ(0);
transform: translate3d(0, 0, 0);
transform: perspective(500px);

/* Declaração explícita de mudança futura */
will-change: transform;
will-change: opacity;
will-change: transform, opacity;

/* Outros criadores automáticos */
position: fixed;
/* iframe e plugin elements */
/* canvas com hardware acceleration */
/* video */
/* Elementos com filter ou backdrop-filter */
filter: blur(2px);
backdrop-filter: blur(8px);

/* Filho 3D de um elemento com transform-style: preserve-3d */
transform-style: preserve-3d;

/* Elemento com mix-blend-mode diferente de normal */
mix-blend-mode: multiply;
```

---

## `will-change` — anunciar mudanças futuras

`will-change` é a forma moderna e semântica de criar layers:

```css
/* ✅ Para elementos que VÃO animar */
.modal {
  will-change: transform, opacity;
}

/* ✅ Adicionar via JS antes da animação, remover depois */
```

```javascript
// Pattern correto: adicionar before animação, remover after
const modal = document.querySelector('.modal');

function showModal() {
  modal.style.willChange = 'transform, opacity';
  modal.classList.add('visible');

  // Remover após a animação terminar — libera memória
  modal.addEventListener('transitionend', () => {
    modal.style.willChange = 'auto';
  }, { once: true });
}
```

> [!warning] Não abuse de `will-change`
> Cada layer ocupa memória de GPU (o bitmap inteiro do elemento). Em dispositivos móveis com memória limitada, dezenas de layers podem degradar performance. Use `will-change` apenas quando a animação é iminente e frequente.

---

## `transform: translateZ(0)` — o hack antigo

Antes de `will-change`, o hack era usar uma transformação 3D trivial para forçar uma layer:

```css
/* Hack antigo — ainda funciona mas semântico é will-change */
.needs-layer {
  transform: translateZ(0);
  -webkit-transform: translateZ(0); /* Safari */
}
```

Em código moderno, prefira `will-change`. O hack ainda aparece em codebases legados.

---

## Animações compositor-only

Propriedades que o compositor pode animar sem CPU:

| Propriedade | Aciona reflow? | Aciona paint? | Pode animar no GPU? |
|---|---|---|---|
| `transform` | Não | Não | ✅ Sim |
| `opacity` | Não | Não | ✅ Sim |
| `filter` | Não | Depende | Parcialmente |
| `width`, `height` | Sim | Sim | ❌ Não |
| `top`, `left` (position) | Sim | Sim | ❌ Não |
| `background-color` | Não | Sim | ❌ Não |
| `box-shadow` | Não | Sim | ❌ Não |

```css
/* ✅ Animação fluida — só GPU */
.card {
  transition: transform 0.3s ease, opacity 0.3s ease;
  will-change: transform, opacity;
}
.card:hover {
  transform: translateY(-4px) scale(1.02);
  opacity: 0.9;
}

/* ❌ Animação cara — layout + paint a cada frame */
.card-slow {
  transition: width 0.3s, top 0.3s, background-color 0.3s;
}
```

---

## DevTools Layers panel

O Chrome DevTools tem um painel Layers para inspecionar layers ativas:

1. Abrir DevTools → More Tools → Layers
2. Ou: DevTools → Rendering → ☑ Layer borders (mostra bordas das layers em azul/laranja)

O que observar:
- **Número de layers**: muitas layers é sinal de "layer explosion"
- **Tamanho de cada layer**: layers grandes usam mais memória de GPU
- **Por que foi promovido**: o painel mostra o motivo (will-change, transform 3D, etc.)

---

## Layer explosion — o problema oposto

Criar layers demais tem custo real de memória:

```css
/* ❌ Aplicar will-change em todos os itens de uma lista longa */
.list-item {
  will-change: transform; /* 1000 itens = 1000 layers = memória excessiva */
}
```

```javascript
// ✅ Adicionar will-change só nos itens ativos/em hover
list.addEventListener('mouseover', (event) => {
  const item = event.target.closest('.list-item');
  if (item) item.style.willChange = 'transform';
});

list.addEventListener('mouseout', (event) => {
  const item = event.target.closest('.list-item');
  if (item) item.style.willChange = 'auto';
});
```

---

## Debugging de performance visual

```javascript
// Detectar se o browser está fazendo paint desnecessário
// DevTools → More Tools → Rendering → ☑ Paint flashing
// Áreas que repintam ficam verdes

// Para animações, verificar se o compositor está sendo usado:
// DevTools → Performance → gravar → buscar "Composite Layers" (barato)
// vs "Layout" ou "Paint" em amarelo/laranja (caro)

// Medir tempo de frame:
let lastTime = performance.now();
function measureFrameTime() {
  const now = performance.now();
  const frameTime = now - lastTime;
  lastTime = now;
  
  if (frameTime > 16.7) { // mais lento que 60fps
    console.warn(`Frame lento: ${frameTime.toFixed(1)}ms`);
  }
  requestAnimationFrame(measureFrameTime);
}
requestAnimationFrame(measureFrameTime);
```

---

## `@layer` CSS e camadas de composição — não confundir

`@layer` do CSS (cascata) não tem relação com GPU layers. São conceitos diferentes:

- **CSS `@layer`**: controla a ordem de cascade/specificity — afeta *quais estilos ganham*
- **GPU layers** (compositor layers): controlam como o browser compõe pixels na tela — afeta *performance de rendering*

---

> [!question] Para fixar
> 1. Por que `transform: translateX(100px)` é mais rápido para animação que `left: 100px` (com `position: relative`)?
> 2. O que `will-change: transform` faz? Por que você deveria remover após a animação terminar?
> 3. O que é "layer explosion"? Dê um exemplo de código que o causaria e como corrigir.
> 4. Quais são as duas propriedades que podem ser animadas pelo GPU sem layout ou paint?
> 5. Como você usaria o DevTools para verificar se uma animação está sendo feita no compositor ou causando paint?

---

## Veja também

- [[03-Dominios/Tecnologia/Plataforma Web/Rendering Pipeline/02 - Render tree, layout e paint|02 — Render tree, layout e paint]] — anterior
- [[03-Dominios/Tecnologia/Plataforma Web/Rendering Pipeline/04 - Reflow e repaint|04 — Reflow e repaint]] — próxima
- [[03-Dominios/Tecnologia/CSS/09 - Animações e transitions|CSS 09 — Animações]] — animações GPU-only na prática
