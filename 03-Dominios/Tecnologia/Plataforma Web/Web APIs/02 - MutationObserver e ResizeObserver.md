---
title: "MutationObserver e ResizeObserver"
created: 2026-06-28
updated: 2026-06-28
type: note
fase: iniciado
tags:
  - plataforma-web
  - web-apis
  - browser
  - javascript
  - dom
  - entrevista
publish: true
---

# MutationObserver e ResizeObserver

> [!abstract] TL;DR
> `MutationObserver` detecta mudanças no DOM: atributos adicionados, filhos inseridos/removidos, texto alterado. Substitui o deprecated `DOMSubtreeModified` event. `ResizeObserver` detecta mudanças de tamanho em elementos — mais preciso que ouvir `window.resize` (que não pega elementos que crescem por conteúdo ou contêiner). Ambos são assíncronos e entregam notificações em batch após layout.

---

## MutationObserver

```javascript
const observer = new MutationObserver((mutations, observer) => {
  mutations.forEach(mutation => {
    mutation.type;             // "childList" | "attributes" | "characterData"
    mutation.target;           // o nó que mudou
    mutation.addedNodes;       // NodeList de nós adicionados (childList)
    mutation.removedNodes;     // NodeList de nós removidos (childList)
    mutation.attributeName;    // nome do atributo (attributes)
    mutation.oldValue;         // valor anterior (se attributeOldValue: true)
  });
});

observer.observe(element, {
  childList: true,          // observar filhos adicionados/removidos
  subtree: true,            // observar descendentes também (não só filhos diretos)
  attributes: true,         // observar mudanças de atributos
  attributeFilter: ['class', 'data-state'], // só esses atributos (opcional)
  attributeOldValue: true,  // incluir valor anterior em mutation.oldValue
  characterData: true,      // observar mudanças de texto
  characterDataOldValue: true,
});

// Parar de observar
observer.disconnect();

// Ler mutações pendentes sem esperar o callback
const pending = observer.takeRecords();
observer.disconnect();
```

---

## Casos de uso para MutationObserver

### 1. Reagir a elementos adicionados dinamicamente

```javascript
// Aguardar que um elemento apareça no DOM (ex: adicionado por terceiro)
function waitForElement(selector) {
  return new Promise(resolve => {
    const existing = document.querySelector(selector);
    if (existing) { resolve(existing); return; }

    const observer = new MutationObserver((mutations) => {
      const el = document.querySelector(selector);
      if (el) {
        observer.disconnect();
        resolve(el);
      }
    });

    observer.observe(document.body, { childList: true, subtree: true });
  });
}

// Uso
const modal = await waitForElement('.modal');
modal.addEventListener('click', handleModalClick);
```

### 2. Sincronizar com mudanças de terceiros

```javascript
// Monitorar mudanças feitas por bibliotecas externas
const thirdPartyEl = document.getElementById('third-party-widget');
const observer = new MutationObserver((mutations) => {
  mutations.forEach(mutation => {
    if (mutation.type === 'attributes' && mutation.attributeName === 'class') {
      const newClass = mutation.target.className;
      syncOwnState(newClass);
    }
  });
});

observer.observe(thirdPartyEl, {
  attributes: true,
  attributeFilter: ['class'],
  attributeOldValue: true,
});
```

### 3. Implementar um hot-reload de componentes

```javascript
// Detectar quando a estrutura de um componente muda (development tool)
const devObserver = new MutationObserver((mutations) => {
  const changed = mutations.some(m =>
    m.type === 'childList' ||
    (m.type === 'attributes' && m.attributeName === 'data-component')
  );
  if (changed) reRenderComponent(element);
});

devObserver.observe(element, {
  childList: true,
  attributes: true,
  attributeFilter: ['data-component'],
  subtree: true,
});
```

---

## Armadilha: ciclo infinito com MutationObserver

Se o callback modifica o DOM que está sendo observado, o observer dispara novamente — loop infinito:

```javascript
// ❌ Ciclo infinito
const observer = new MutationObserver((mutations) => {
  mutations.forEach(mutation => {
    if (mutation.type === 'attributes') {
      mutation.target.setAttribute('data-processed', 'true'); // dispara outro mutation!
    }
  });
});
observer.observe(el, { attributes: true });

// ✅ Verificar antes de mudar, ou desconectar temporariamente
const observer = new MutationObserver((mutations) => {
  mutations.forEach(mutation => {
    if (mutation.attributeName !== 'data-processed') { // ignora o próprio atributo
      mutation.target.setAttribute('data-processed', 'true');
    }
  });
});
```

---

## ResizeObserver

```javascript
const observer = new ResizeObserver((entries) => {
  entries.forEach(entry => {
    // contentRect: tamanho do conteúdo (sem padding)
    const { width, height } = entry.contentRect;

    // borderBoxSize: tamanho incluindo padding e borda
    const borderBox = entry.borderBoxSize[0];
    borderBox.inlineSize; // largura
    borderBox.blockSize;  // altura

    // contentBoxSize: tamanho do conteúdo
    const contentBox = entry.contentBoxSize[0];

    // devicePixelContentBoxSize: em pixels de dispositivo (para canvas)
    const deviceBox = entry.devicePixelContentBoxSize?.[0];

    entry.target; // o elemento
  });
});

observer.observe(element);
observer.observe(otherElement, { box: 'border-box' }); // opção de qual box observar
observer.unobserve(element);
observer.disconnect();
```

---

## Casos de uso para ResizeObserver

### 1. Layout responsivo baseado no tamanho do componente

```javascript
// "Container queries" antes de existirem nativamente no CSS
const observer = new ResizeObserver((entries) => {
  for (const entry of entries) {
    const { width } = entry.contentRect;
    const el = entry.target;

    // Aplicar classes baseadas no tamanho do componente (não da janela)
    el.classList.toggle('compact', width < 400);
    el.classList.toggle('medium', width >= 400 && width < 800);
    el.classList.toggle('wide', width >= 800);
  }
});

observer.observe(document.querySelector('.adaptive-widget'));
```

> [!tip] CSS Container Queries
> CSS Container Queries (`@container`) são a solução nativa para isso e têm bom suporte desde 2023. Use ResizeObserver quando precisar de lógica JavaScript que reage ao tamanho, não apenas CSS.

### 2. Canvas responsivo com DPR correto

```javascript
const canvas = document.querySelector('canvas');
const ctx = canvas.getContext('2d');

const observer = new ResizeObserver((entries) => {
  for (const entry of entries) {
    const dpr = window.devicePixelRatio || 1;
    
    if (entry.devicePixelContentBoxSize) {
      // Usar tamanho em device pixels diretamente (mais preciso)
      canvas.width = entry.devicePixelContentBoxSize[0].inlineSize;
      canvas.height = entry.devicePixelContentBoxSize[0].blockSize;
    } else {
      // Fallback: contentRect × DPR
      canvas.width = Math.round(entry.contentRect.width * dpr);
      canvas.height = Math.round(entry.contentRect.height * dpr);
    }
    
    ctx.scale(dpr, dpr);
    redraw();
  }
});

observer.observe(canvas, { box: 'device-pixel-content-box' });
```

### 3. Sincronizar posição de elementos relativos

```javascript
// Reposicionar um dropdown quando o trigger muda de tamanho
const trigger = document.querySelector('.dropdown-trigger');
const dropdown = document.querySelector('.dropdown');

const positionObserver = new ResizeObserver(() => {
  const rect = trigger.getBoundingClientRect();
  dropdown.style.top = `${rect.bottom}px`;
  dropdown.style.left = `${rect.left}px`;
  dropdown.style.width = `${rect.width}px`;
});

positionObserver.observe(trigger);
```

---

## Comparação dos três observers

| Observer | Detecta | Quando usar |
|---|---|---|
| `IntersectionObserver` | Entrada/saída do viewport | Lazy loading, animações on-scroll, infinite scroll |
| `MutationObserver` | Mudanças de DOM (atributos, filhos, texto) | Reagir a mudanças de terceiros, observar elementos dinâmicos |
| `ResizeObserver` | Mudanças de tamanho de elementos | Layout responsivo por componente, canvas responsivo |

---

> [!question] Para fixar
> 1. O que `subtree: true` faz no MutationObserver? Quando você precisaria disso?
> 2. Como você esperaria que um elemento aparecesse no DOM sem polling? Escreva o código.
> 3. O que causa ciclo infinito com MutationObserver? Dê um exemplo e como evitar.
> 4. Qual a diferença entre `contentRect` e `borderBoxSize` no ResizeObserver?
> 5. Por que `ResizeObserver` é melhor que `window.addEventListener('resize', ...)` para reagir ao tamanho de um componente específico?

---

## Veja também

- [[03-Dominios/Tecnologia/Plataforma Web/Web APIs/01 - Intersection Observer|01 — Intersection Observer]] — anterior
- [[03-Dominios/Tecnologia/Plataforma Web/Web APIs/03 - History API e SPA routing|03 — History API]] — próxima
- [[03-Dominios/Tecnologia/Plataforma Web/DOM/06 - DocumentFragment e batch mutations|DOM 06 — Batch mutations]] — context de DOM mutations
