---
title: "Padrões avançados de eventos"
created: 2026-06-28
updated: 2026-06-28
type: note
fase: magus
tags:
  - plataforma-web
  - eventos
  - browser
  - javascript
  - acessibilidade
  - entrevista
publish: true
---

# Padrões avançados de eventos

> [!abstract] TL;DR
> Drag and Drop nativo usa `dragstart`/`dragover`/`drop` com DataTransfer. Pointer Lock API captura o ponteiro para controles de câmera/jogo. Intersection Observer integrado com scroll eventos é mais performático que ouvir `scroll` diretamente. `passive: true` em handlers de `wheel`/`touchstart` é obrigatório para não bloquear o scroll nativo.

---

## Drag and Drop nativo

A API de Drag and Drop é verbosa mas funcional sem bibliotecas:

```html
<!-- Elemento arrastável -->
<div class="card" draggable="true" data-card-id="42">
  Conteúdo
</div>

<!-- Zona de drop -->
<div class="dropzone" data-column="done">
  Solte aqui
</div>
```

```javascript
// No elemento arrastável
document.querySelectorAll('.card').forEach(card => {
  card.addEventListener('dragstart', (event) => {
    // Salvar dados para transferir ao drop
    event.dataTransfer.setData('text/plain', card.dataset.cardId);
    event.dataTransfer.effectAllowed = 'move';
    
    card.classList.add('dragging');
    
    // Imagem customizada de drag (opcional)
    // event.dataTransfer.setDragImage(customEl, offsetX, offsetY);
  });

  card.addEventListener('dragend', () => {
    card.classList.remove('dragging');
  });
});

// Na zona de drop
document.querySelectorAll('.dropzone').forEach(zone => {
  zone.addEventListener('dragover', (event) => {
    event.preventDefault(); // necessário para permitir o drop
    event.dataTransfer.dropEffect = 'move';
    zone.classList.add('drag-over');
  });

  zone.addEventListener('dragleave', () => {
    zone.classList.remove('drag-over');
  });

  zone.addEventListener('drop', (event) => {
    event.preventDefault();
    zone.classList.remove('drag-over');

    const cardId = event.dataTransfer.getData('text/plain');
    const column = zone.dataset.column;
    
    moveCard(cardId, column);
  });
});
```

### DataTransfer — dados e efeitos

```javascript
event.dataTransfer.setData('text/plain', 'texto');
event.dataTransfer.setData('application/json', JSON.stringify(data));
event.dataTransfer.getData('text/plain');

// Tipos disponíveis
event.dataTransfer.types; // ['text/plain', 'application/json']

// Arquivos soltos de fora do browser
event.dataTransfer.files; // FileList — para upload por drag

// Efeitos visuais
event.dataTransfer.effectAllowed = 'move' | 'copy' | 'link' | 'all';
event.dataTransfer.dropEffect = 'move' | 'copy' | 'link';
```

### Drag and Drop com Pointer Events — mais controle

Para drag complexo (reordenação de lista, canvas), Pointer Events dão mais controle:

```javascript
function makeSortable(list) {
  let dragEl = null;
  let placeholder = null;

  list.addEventListener('pointerdown', (event) => {
    const item = event.target.closest('.sortable-item');
    if (!item) return;

    dragEl = item;
    dragEl.setPointerCapture(event.pointerId);
    
    // Criar placeholder na posição original
    placeholder = document.createElement('div');
    placeholder.className = 'sortable-placeholder';
    placeholder.style.height = dragEl.offsetHeight + 'px';
    dragEl.after(placeholder);
    
    // Posicionar o item sendo arrastado
    dragEl.classList.add('dragging');
  });

  list.addEventListener('pointermove', (event) => {
    if (!dragEl) return;
    
    // Mover o item visualmente
    dragEl.style.transform = `translateY(${event.clientY}px)`;
    
    // Encontrar onde inserir o placeholder
    const afterEl = getDragAfterElement(list, event.clientY);
    if (afterEl) {
      list.insertBefore(placeholder, afterEl);
    } else {
      list.appendChild(placeholder);
    }
  });

  list.addEventListener('pointerup', () => {
    if (!dragEl) return;
    
    dragEl.classList.remove('dragging');
    dragEl.style.transform = '';
    placeholder.replaceWith(dragEl);
    
    dragEl = null;
    placeholder = null;
  });
}

function getDragAfterElement(container, y) {
  const items = [...container.querySelectorAll('.sortable-item:not(.dragging)')];
  return items.find(item => {
    const box = item.getBoundingClientRect();
    return y < box.top + box.height / 2;
  });
}
```

---

## Intersection Observer integrado com eventos

Melhor alternativa ao listener de `scroll` para detectar visibilidade:

```javascript
// ❌ Listener de scroll — executa muitas vezes, força layout (getBoundingClientRect)
window.addEventListener('scroll', () => {
  const el = document.querySelector('.target');
  const rect = el.getBoundingClientRect();
  if (rect.top < window.innerHeight) {
    animateIn(el);
  }
}, { passive: true });

// ✅ Intersection Observer — não polui o scroll, não força reflow
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      animateIn(entry.target);
      observer.unobserve(entry.target); // parar de observar após animar
    }
  });
}, {
  threshold: 0.2,      // 20% visível para disparar
  rootMargin: '0px 0px -50px 0px', // recuar 50px do bottom
});

document.querySelectorAll('.animate-on-scroll').forEach(el => {
  observer.observe(el);
});
```

---

## Pointer Lock API — mouse sem limites

Para jogos e editores 3D, Pointer Lock captura o ponteiro dentro do elemento — o mouse não encontra bordas:

```javascript
const canvas = document.querySelector('canvas');

canvas.addEventListener('click', () => {
  canvas.requestPointerLock();
});

document.addEventListener('pointerlockchange', () => {
  if (document.pointerLockElement === canvas) {
    console.log('Pointer capturado');
    document.addEventListener('mousemove', onMouseMove);
  } else {
    console.log('Pointer liberado');
    document.removeEventListener('mousemove', onMouseMove);
  }
});

function onMouseMove(event) {
  // event.movementX / movementY: deslocamento relativo (sem limites de borda)
  camera.rotateY(event.movementX * 0.002);
  camera.rotateX(event.movementY * 0.002);
}

// Sair: Escape automaticamente sai do Pointer Lock
```

---

## `passive: true` — por que e quando

```javascript
// ❌ Sem passive: o browser aguarda o handler antes de rolar (latência)
window.addEventListener('wheel', handler);
window.addEventListener('touchstart', handler);

// ✅ Com passive: o browser rola imediatamente e executa o handler em paralelo
window.addEventListener('wheel', handler, { passive: true });
window.addEventListener('touchstart', handler, { passive: true });

// Só use passive: false quando PRECISAR chamar event.preventDefault()
window.addEventListener('wheel', (event) => {
  event.preventDefault(); // bloquear scroll (ex: zoom customizado)
  handleZoom(event);
}, { passive: false }); // precisa ser false para preventDefault funcionar
```

Scroll em apps modernos frequentemente falha por terceiros registrando handlers de wheel/touch sem `passive: true`. O Chrome avisa no DevTools quando isso acontece.

---

## `window.onerror` — capturar erros globais

```javascript
// Capturar erros de JavaScript não tratados
window.addEventListener('error', (event) => {
  const { message, filename, lineno, colno, error } = event;
  sendToMonitoring({
    type: 'js-error',
    message,
    stack: error?.stack,
    location: `${filename}:${lineno}:${colno}`,
  });
  
  // Retornar true previne o log padrão no console (não recomendado)
});

// Capturar promises rejeitadas sem catch
window.addEventListener('unhandledrejection', (event) => {
  const { reason, promise } = event;
  sendToMonitoring({
    type: 'unhandled-rejection',
    reason: reason?.message || String(reason),
    stack: reason?.stack,
  });

  event.preventDefault(); // previne o log no console
});

// Capturar erros de recursos (imagens 404, scripts que falharam)
// Usa capture: true porque erros de recursos não borbulham
window.addEventListener('error', (event) => {
  if (event.target !== window && event.target.tagName) {
    sendToMonitoring({
      type: 'resource-error',
      element: event.target.tagName,
      source: event.target.src || event.target.href,
    });
  }
}, { capture: true });
```

---

> [!question] Para fixar
> 1. Quais eventos são necessários para implementar drag and drop nativo? Por que `dragover` precisa de `preventDefault`?
> 2. Por que Intersection Observer é mais performático que ouvir `scroll` para detectar visibilidade?
> 3. O que Pointer Lock faz? Qual a diferença entre `event.clientX` e `event.movementX` quando o pointer está locked?
> 4. Quando você PRECISARIA de `passive: false`? O que acontece se você declarar `passive: true` e chamar `preventDefault`?
> 5. Como capturar erros globais de JavaScript E promises rejeitadas sem catch? Quais eventos ouvir em qual objeto?

---

## Veja também

- [[03-Dominios/Tecnologia/Plataforma Web/Eventos/06 - Timers e microtasks|06 — Timers e microtasks]] — anterior
- [[03-Dominios/Tecnologia/Plataforma Web/Eventos/08 - Eventos em entrevista|08 — Eventos em entrevista]] — próxima e capstone
- [[03-Dominios/Tecnologia/Plataforma Web/Web APIs/01 - Intersection Observer|Web APIs 01 — Intersection Observer]] — aprofunda observação de visibilidade
