---
title: "template e cloneNode — reutilizar estrutura HTML"
created: 2026-06-28
updated: 2026-06-28
type: note
fase: Magus
tags:
  - plataforma-web
  - dom
  - browser
  - javascript
  - web-components
publish: true
---

# template e cloneNode — reutilizar estrutura HTML

> [!abstract] TL;DR
> `<template>` é um elemento HTML inerte — seu conteúdo existe no DOM mas não renderiza, não carrega imagens, não executa scripts. Você clona o seu `content` com `cloneNode(true)` e insere no documento. É a base dos Web Components nativos. `cloneNode` sozinho serve para duplicar qualquer subárvore sem precisar do `<template>`. Juntos, são o mecanismo de "componentes" antes dos frameworks existirem — e ainda relevantes para Web Components e performance.

---

## O elemento `<template>`

`<template>` define um fragmento HTML inerte que pode ser reutilizado pelo JavaScript:

```html
<template id="card-template">
  <article class="product-card">
    <img class="product-card__img" alt="">
    <h3 class="product-card__title"></h3>
    <p class="product-card__price"></p>
    <button type="button" class="btn btn--add-cart">Adicionar</button>
  </article>
</template>
```

O que torna `<template>` especial:
- **Inerte**: não renderiza na página
- **Sem side effects**: imagens não carregam, scripts não executam, iframes não navegam
- **Disponível no DOM**: pode ser selecionado e clonado
- Seu conteúdo está em `template.content` — um `DocumentFragment`

---

## Clonar e usar o template

```javascript
const template = document.getElementById('card-template');

function createProductCard(product) {
  // cloneNode(true) = deep clone — clona o content inteiro
  const clone = template.content.cloneNode(true);

  // Agora popula o clone (antes de inserir no DOM)
  clone.querySelector('.product-card__img').src = product.imageUrl;
  clone.querySelector('.product-card__img').alt = product.name;
  clone.querySelector('.product-card__title').textContent = product.name;
  clone.querySelector('.product-card__price').textContent =
    `R$ ${product.price.toFixed(2)}`;

  clone.querySelector('.btn--add-cart').addEventListener('click', () => {
    addToCart(product.id);
  });

  return clone; // DocumentFragment com o card pronto
}

// Renderizar lista de produtos
const container = document.querySelector('.product-grid');
const fragment = document.createDocumentFragment();

products.forEach(product => {
  fragment.appendChild(createProductCard(product));
});

container.replaceChildren(fragment);
```

---

## `cloneNode` — clonar qualquer elemento

`cloneNode` funciona em qualquer `Node`, não só em `template.content`:

```javascript
const original = document.querySelector('.card');

// cloneNode(false) — só o elemento, sem filhos
const shallowClone = original.cloneNode(false);

// cloneNode(true) — deep clone: elemento + toda a subárvore de filhos
const deepClone = original.cloneNode(true);

// Importante: cloneNode NÃO copia event listeners
// Os listeners precisam ser re-adicionados manualmente
```

### Quando usar cada um

```javascript
// cloneNode(false): útil para criar um container igual ao original
const newCard = original.cloneNode(false); // mesmas classes, atributos, sem filhos
newCard.appendChild(customContent);
container.appendChild(newCard);

// cloneNode(true): duplicar estrutura completa
const copy = template.content.cloneNode(true); // ✅ mais comum com <template>
```

---

## `document.importNode` — clonar de outro documento

Quando o template vem de um documento diferente (como Shadow DOM ou outro contexto):

```javascript
// importNode: como cloneNode, mas para nós de outros documentos
const externalNode = externalDocument.querySelector('.widget');
const imported = document.importNode(externalNode, true); // true = deep
document.body.appendChild(imported);

// Na prática mais comum: importar de shadow host
const host = document.querySelector('my-component');
const templateContent = host.shadowRoot.querySelector('template').content;
const clone = document.importNode(templateContent, true);
```

---

## Web Components — o uso canônico de `<template>`

Web Components usa `<template>` + `<slot>` + Shadow DOM juntos:

```html
<!-- Definição do template com slot -->
<template id="tooltip-template">
  <style>
    :host {
      position: relative;
      display: inline-block;
    }
    .tooltip {
      position: absolute;
      bottom: 125%;
      left: 50%;
      transform: translateX(-50%);
      background: #333;
      color: white;
      padding: 4px 8px;
      border-radius: 4px;
      font-size: 12px;
      white-space: nowrap;
      opacity: 0;
      transition: opacity 0.2s;
      pointer-events: none;
    }
    :host(:hover) .tooltip { opacity: 1; }
  </style>
  <slot></slot>
  <div class="tooltip"><slot name="tip">Tooltip</slot></div>
</template>

<!-- Uso do componente -->
<my-tooltip>
  Passe o mouse aqui
  <span slot="tip">Texto do tooltip</span>
</my-tooltip>
```

```javascript
class MyTooltip extends HTMLElement {
  constructor() {
    super();
    // Attach shadow root
    const shadow = this.attachShadow({ mode: 'open' });

    // Clonar e inserir o template
    const template = document.getElementById('tooltip-template');
    shadow.appendChild(template.content.cloneNode(true));
  }
}

// Registrar o custom element
customElements.define('my-tooltip', MyTooltip);
```

### Ciclo de vida dos Custom Elements

```javascript
class MyComponent extends HTMLElement {
  // Chamado quando o elemento é criado (antes de inserido no DOM)
  constructor() {
    super();
    this._shadow = this.attachShadow({ mode: 'open' });
  }

  // Chamado quando o elemento é inserido no documento
  connectedCallback() {
    this.render();
  }

  // Chamado quando o elemento é removido do documento
  disconnectedCallback() {
    this.cleanup();
  }

  // Chamado quando um atributo observado muda
  static get observedAttributes() {
    return ['data-count', 'disabled'];
  }
  attributeChangedCallback(name, oldValue, newValue) {
    if (name === 'data-count') this.render();
  }
}
```

---

## Pattern: factory de elementos com template

```javascript
// Template definido uma vez no HTML
// <template id="notification-tpl">
//   <div class="notification" role="alert">
//     <span class="notification__icon"></span>
//     <p class="notification__message"></p>
//     <button type="button" class="notification__close" aria-label="Fechar">×</button>
//   </div>
// </template>

const notificationTemplate = document.getElementById('notification-tpl');

function createNotification({ message, type = 'info', duration = 5000 }) {
  const clone = notificationTemplate.content.cloneNode(true);
  const root = clone.querySelector('.notification');

  root.dataset.type = type;
  clone.querySelector('.notification__icon').textContent =
    ({ info: 'ℹ', success: '✓', warning: '⚠', error: '✕' })[type];
  clone.querySelector('.notification__message').textContent = message;

  const closeBtn = clone.querySelector('.notification__close');
  closeBtn.addEventListener('click', () => root.remove());

  if (duration) {
    setTimeout(() => root.remove(), duration);
  }

  return clone;
}

// Uso
const container = document.querySelector('.notifications-container');
container.appendChild(createNotification({
  message: 'Operação concluída com sucesso',
  type: 'success'
}));
```

---

> [!question] Para fixar
> 1. Por que imagens dentro de um `<template>` não carregam até o template ser clonado e inserido?
> 2. Qual a diferença entre `cloneNode(false)` e `cloneNode(true)`? Quando usar cada um?
> 3. Por que `cloneNode` não copia event listeners? Como você adicionaria listeners ao clone?
> 4. O que é Shadow DOM? Qual a diferença entre `mode: 'open'` e `mode: 'closed'`?
> 5. No ciclo de vida de Web Components, quando `connectedCallback` é chamado? E `disconnectedCallback`?

---

## Veja também

- [[03-Dominios/Tecnologia/Plataforma Web/DOM/06 - DocumentFragment e batch mutations|06 — DocumentFragment]] — anterior
- [[03-Dominios/Tecnologia/Plataforma Web/DOM/08 - DOM em entrevista|08 — DOM em entrevista]] — próxima e capstone
- [[03-Dominios/Tecnologia/Plataforma Web/Rendering Pipeline/01 - Parse e construção do DOM e CSSOM|Rendering Pipeline 01]] — como o browser parseia templates
