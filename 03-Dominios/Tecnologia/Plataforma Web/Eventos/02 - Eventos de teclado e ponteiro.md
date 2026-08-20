---
title: "Eventos de teclado e ponteiro"
created: 2026-06-28
updated: 2026-06-28
type: note
fase: iniciado
tags:
  - plataforma-web
  - eventos
  - browser
  - javascript
  - entrevista
publish: true
---

# Eventos de teclado e ponteiro

> [!abstract] TL;DR
> Teclado: use `keydown` e `keyup`; `keypress` está deprecated. A propriedade `event.key` retorna o valor legível ("Enter", "a", "ArrowLeft"); `event.code` retorna a tecla física ("Enter", "KeyA") — independe do layout do teclado. Ponteiro: Pointer Events (`pointerdown`/`pointermove`/`pointerup`) unificam mouse, touch e stylus — prefira-os sobre eventos de mouse e touch separados. `click` borbulha e funciona para mouse e touch.

---

## Eventos de teclado

### A família de eventos de teclado

| Evento | Quando | Deprecated? |
|---|---|---|
| `keydown` | Tecla pressionada — repete se mantida | Não |
| `keyup` | Tecla solta | Não |
| `keypress` | Tecla pressionada (só caracteres imprimíveis) | ✅ Sim |

Sempre use `keydown` — captura todas as teclas (incluindo Escape, Delete, setas) e é o padrão moderno. `keyup` é útil quando você quer aguardar a soltura (ex: finalizar arraste).

### `event.key` vs `event.code`

```javascript
document.addEventListener('keydown', (event) => {
  event.key;    // valor lógico: "a", "A", "Enter", "ArrowLeft", "Control"
  event.code;   // posição física: "KeyA", "Enter", "ArrowLeft", "ControlLeft"
});
```

**`event.key`**: o que a tecla *produz* — depende do layout e do shift:
- Pressionar `a` sem shift → `"a"`
- Pressionar `a` com shift → `"A"`
- Em teclado AZERTY (francês), onde `a` está em `q` → `"a"` também

**`event.code`**: a posição física da tecla — independente do layout:
- A tecla física `A` sempre retorna `"KeyA"`, mesmo em layout AZERTY
- Útil para atalhos de jogo (WASD → "KeyW"/"KeyA"/"KeyS"/"KeyD")

```javascript
// ✅ Para atalhos de texto e UI — use event.key
document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape') closeModal();
  if (event.key === 'Enter') submitForm();
  if (event.key === 'ArrowUp') navigateUp();
});

// ✅ Para controles de jogo / posição física — use event.code
document.addEventListener('keydown', (event) => {
  if (event.code === 'KeyW') moveForward();
  if (event.code === 'KeyA') moveLeft();
  // Funciona mesmo em layout AZERTY onde a tecla QWERTY-W não produz 'w'
});
```

### Modificadores

```javascript
document.addEventListener('keydown', (event) => {
  event.ctrlKey;   // Ctrl pressionado
  event.altKey;    // Alt/Option pressionado
  event.shiftKey;  // Shift pressionado
  event.metaKey;   // Cmd (Mac) / Win key

  // Atalho cross-platform: Ctrl+K no Windows/Linux, Cmd+K no Mac
  if ((event.ctrlKey || event.metaKey) && event.key === 'k') {
    event.preventDefault(); // previne comportamento padrão do browser
    openCommandPalette();
  }
});
```

### Teclas especiais e `event.key` values

```javascript
// Navegação
'ArrowUp' | 'ArrowDown' | 'ArrowLeft' | 'ArrowRight'
'Home' | 'End' | 'PageUp' | 'PageDown'

// Edição
'Backspace' | 'Delete' | 'Insert'
'Tab' | 'Enter'

// UI
'Escape' | 'Space' | 'F1'-'F12'
'CapsLock' | 'NumLock' | 'ScrollLock'

// Modificadores sozinhos
'Control' | 'Alt' | 'Shift' | 'Meta'

// event.repeat: true se a tecla está sendo mantida
document.addEventListener('keydown', (event) => {
  if (event.repeat) return; // ignora repetição de keydown
});
```

---

## Eventos de ponteiro

### Pointer Events — a API unificada

Pointer Events unificam mouse, touch e stylus em uma única API:

```javascript
element.addEventListener('pointerdown', (event) => {
  event.pointerId;    // ID único (para rastrear multi-touch)
  event.pointerType;  // "mouse" | "touch" | "pen"
  event.isPrimary;    // true para o primeiro toque (multi-touch)
  event.pressure;     // 0-1 (útil para stylus)
  event.clientX;      // posição
  event.clientY;
  event.width;        // área de contato (touch)
  event.height;
});
```

| Evento | Quando |
|---|---|
| `pointerdown` | Início do toque/clique |
| `pointermove` | Movimento com botão pressionado ou dedo movendo |
| `pointerup` | Soltar |
| `pointercancel` | Touch cancelado (ligação recebida, scroll, etc.) |
| `pointerenter` | Entrada no elemento (não borbulha) |
| `pointerleave` | Saída do elemento (não borbulha) |
| `pointerover` | Entrada no elemento ou filho (borbulha) |
| `pointerout` | Saída (borbulha) |

### `click` — o evento de ação

`click` funciona para mouse E touch, borbulha, e é o evento correto para ações de UI:

```javascript
btn.addEventListener('click', handleAction);
// Dispara em mouse click E tap mobile — não use pointerdown para ações de UI
// ✅ Preferido para botões, links, cards clicáveis
```

### Drag imperativo com Pointer Events

```javascript
function makeDraggable(element) {
  let isDragging = false;
  let startX, startY, offsetX, offsetY;

  element.addEventListener('pointerdown', (event) => {
    isDragging = true;
    element.setPointerCapture(event.pointerId); // garante que pointermove continua no elemento

    startX = event.clientX;
    startY = event.clientY;
    const rect = element.getBoundingClientRect();
    offsetX = startX - rect.left;
    offsetY = startY - rect.top;
  });

  element.addEventListener('pointermove', (event) => {
    if (!isDragging) return;
    element.style.left = (event.clientX - offsetX) + 'px';
    element.style.top = (event.clientY - offsetY) + 'px';
  });

  element.addEventListener('pointerup', () => {
    isDragging = false;
  });

  element.addEventListener('pointercancel', () => {
    isDragging = false;
  });
}
```

> [!tip] `setPointerCapture`
> Quando você chama `element.setPointerCapture(pointerId)`, todos os eventos daquele ponteiro são entregues ao elemento, mesmo que o ponteiro saia dos seus limites. Essencial para drag-and-drop — sem isso, rápidos movimentos do mouse saem do elemento e o drag para.

---

## Eventos de mouse — ainda relevantes

```javascript
// Clique e botões
element.addEventListener('click', handler);        // clique esquerdo (ou tap)
element.addEventListener('dblclick', handler);     // duplo clique
element.addEventListener('contextmenu', handler);  // clique direito (abre menu)
element.addEventListener('auxclick', handler);     // botão do meio ou outros

// Hover
element.addEventListener('mouseenter', handler);   // entrada no elemento (não borbulha)
element.addEventListener('mouseleave', handler);   // saída (não borbulha)
element.addEventListener('mouseover', handler);    // entrada + filhos (borbulha)
element.addEventListener('mouseout', handler);     // saída (borbulha)
element.addEventListener('mousemove', handler);    // movimento

// Botões do mouse
event.button;  // 0=esquerdo, 1=meio, 2=direito
event.buttons; // bitmask: 1=esq, 2=dir, 4=meio (múltiplos pressionados)
```

### `mouseenter` vs `mouseover`

```javascript
// mouseenter: dispara só ao entrar no PRÓPRIO elemento (não borbulha)
parent.addEventListener('mouseenter', () => {
  console.log('entrou no parent');
});
// Mover de parent → child: NÃO dispara novamente (mouseenter não borbulha de child)

// mouseover: dispara ao entrar no elemento OU em qualquer filho
parent.addEventListener('mouseover', (event) => {
  console.log('mouseover em:', event.target);
});
// Mover de parent → child: dispara com target = child (borbulhou do child para parent)
```

---

## Wheel e scroll

```javascript
// wheel: evento da roda do mouse/trackpad (não o scroll em si)
element.addEventListener('wheel', (event) => {
  event.deltaX;    // scroll horizontal
  event.deltaY;    // scroll vertical (positivo = para baixo)
  event.deltaZ;    // scroll de profundidade (raro)
  event.deltaMode; // 0=pixels, 1=linhas, 2=páginas

  event.preventDefault(); // bloqueia o scroll nativo (útil para zoom customizado)
}, { passive: false }); // passive:false necessário para poder chamar preventDefault

// scroll: dispara quando o elemento JÁ scrollou
window.addEventListener('scroll', (event) => {
  window.scrollY; // pixels scrollados verticalmente
  window.scrollX;
});
```

> [!warning] `passive: true` e performance de scroll
> Por padrão, o browser precisa aguardar o handler de `wheel`/`touch` para saber se você vai chamar `preventDefault()`. Isso adiciona latência ao scroll. Se você **não** vai chamar `preventDefault()`, declare `{ passive: true }` — o browser pode fazer o scroll imediatamente:
> ```javascript
> // ✅ Para handlers de scroll que não bloqueiam o comportamento padrão
> document.addEventListener('wheel', handler, { passive: true });
> ```
> Declarar `passive: true` e depois chamar `preventDefault()` lança um aviso no console e o `preventDefault` é ignorado.

---

> [!question] Para fixar
> 1. Por que `keypress` está deprecated? Qual evento usar no lugar?
> 2. Qual a diferença entre `event.key === 'a'` e `event.code === 'KeyA'`? Dê um exemplo de quando a diferença importa.
> 3. O que `setPointerCapture` faz? Por que é essencial para drag-and-drop?
> 4. Por que `mouseenter` é preferido a `mouseover` para hover effects em um elemento com filhos?
> 5. O que significa um event listener ser `passive`? Qual o impacto de desabilitar o passive em handlers de scroll?

---

## Veja também

- [[03-Dominios/Tecnologia/Plataforma Web/Eventos/01 - O event model do browser|01 — O event model]] — anterior
- [[03-Dominios/Tecnologia/Plataforma Web/Eventos/03 - Eventos de formulário e foco|03 — Eventos de formulário e foco]] — próxima
- [[03-Dominios/Tecnologia/Plataforma Web/Eventos/07 - Padrões avançados|07 — Drag and drop nativo]] — arraste com Pointer Events aprofundado
