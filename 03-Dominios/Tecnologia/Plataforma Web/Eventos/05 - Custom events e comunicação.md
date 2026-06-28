---
title: "Custom events e comunicação entre componentes"
created: 2026-06-28
updated: 2026-06-28
type: note
fase: Adepto
tags:
  - plataforma-web
  - eventos
  - browser
  - javascript
  - web-components
  - entrevista
publish: true
---

# Custom events e comunicação entre componentes

> [!abstract] TL;DR
> `CustomEvent` permite criar eventos semânticos próprios — em vez de emitir `click`, você emite `product:added-to-cart` com `detail: { productId, quantity }`. Componentes comunicam entre si sem acoplamento direto: o filho dispara um evento, o ancestral ouve. `bubbles: true` permite que o evento suba a árvore para ser capturado no nível certo. `composed: true` faz o evento atravessar o Shadow DOM boundary — essencial para Web Components.

---

## `CustomEvent` — criar um evento semântico

```javascript
// Criar um custom event
const event = new CustomEvent('produto:adicionado', {
  detail: {          // dados arbitrários — qualquer coisa serializável
    productId: 42,
    quantity: 1,
    price: 99.90,
  },
  bubbles: true,     // sobe a árvore DOM (padrão: false)
  cancelable: true,  // permite preventDefault() (padrão: false)
  composed: false,   // atravessa Shadow DOM boundary (padrão: false)
});

// Disparar no elemento
const btn = document.querySelector('.btn--add-cart');
btn.dispatchEvent(event);
```

---

## `dispatchEvent` — disparar um evento

```javascript
// Disparar no elemento — o evento começa aqui e (com bubbles:true) sobe
element.dispatchEvent(new CustomEvent('meu:evento', { bubbles: true }));

// Disparar no document — ouvido por qualquer listener de 'meu:evento'
document.dispatchEvent(new CustomEvent('app:logout'));

// Disparar no window — global
window.dispatchEvent(new CustomEvent('tema:alterado', { detail: { tema: 'dark' } }));
```

`dispatchEvent` é **síncrono** — os handlers são executados antes de `dispatchEvent` retornar.

---

## Comunicação pai → filho vs filho → pai

Custom events são ideais para comunicação **filho → pai** (ou entre irmãos via ancestral comum):

```javascript
// Componente filho: ProductCard
const card = document.querySelector('.product-card');

// Filho emite um evento com dados
function addToCart(product) {
  card.dispatchEvent(new CustomEvent('cart:add', {
    bubbles: true,    // sobe até o ancestral que ouve
    cancelable: true,
    detail: { productId: product.id, quantity: 1 },
  }));
}

// Componente ancestral: CartManager (separado, sem referência ao card)
document.querySelector('.app').addEventListener('cart:add', (event) => {
  const { productId, quantity } = event.detail;
  
  // Checar se foi cancelado (outro handler chamou preventDefault)
  if (!event.defaultPrevented) {
    updateCart(productId, quantity);
  }
});
```

### `cancelable` e `defaultPrevented`

Quando o evento é `cancelable: true`, um handler pode "vetar" a ação chamando `event.preventDefault()`:

```javascript
// Listener que pode cancelar o evento
document.addEventListener('cart:add', (event) => {
  const { productId } = event.detail;
  
  if (isOutOfStock(productId)) {
    event.preventDefault(); // cancela a adição
    showNotification('Produto fora de estoque');
  }
});

// O disparador verifica se foi cancelado
const added = card.dispatchEvent(event); // dispatchEvent retorna false se foi preventDefault'd
if (!added) {
  console.log('Adição cancelada por um handler');
}
```

---

## Pattern pub/sub com CustomEvents

Custom Events implementam um pub/sub simples sem bibliotecas:

```javascript
// Centralize os nomes de eventos para evitar typos
const Events = {
  CART_ADD: 'cart:add',
  CART_REMOVE: 'cart:remove',
  USER_LOGOUT: 'user:logout',
  THEME_CHANGE: 'theme:change',
};

// Publisher — qualquer módulo pode publicar
function publishCartAdd(product) {
  document.dispatchEvent(new CustomEvent(Events.CART_ADD, {
    detail: { product },
    bubbles: false, // sem bubbles quando dispara no document diretamente
  }));
}

// Subscriber — qualquer módulo pode assinar
document.addEventListener(Events.CART_ADD, (event) => {
  const { product } = event.detail;
  updateCartBadge(product);
});

document.addEventListener(Events.CART_ADD, (event) => {
  const { product } = event.detail;
  logAnalytics('add_to_cart', product);
});

// Múltiplos subscribers — todos recebem o mesmo evento
```

---

## `composed: true` — atravessar o Shadow DOM

Por padrão, eventos não atravessam o Shadow DOM boundary — ficam encapsulados no shadow root. Para comunicar de dentro do Shadow DOM para o exterior, use `composed: true`:

```javascript
// Dentro de um Web Component
class ProductCard extends HTMLElement {
  connectedCallback() {
    this.shadow = this.attachShadow({ mode: 'open' });
    this.shadow.innerHTML = `
      <button class="add-btn">Adicionar</button>
    `;
    
    this.shadow.querySelector('.add-btn').addEventListener('click', () => {
      // Sem composed: true, esse evento não sai do shadow root
      this.dispatchEvent(new CustomEvent('product:selected', {
        detail: { id: this.dataset.productId },
        bubbles: true,
        composed: true, // atravessa a shadow boundary para o DOM principal
      }));
    });
  }
}

// No DOM principal — recebe o evento que saiu do shadow root
document.querySelector('.product-list').addEventListener('product:selected', (event) => {
  console.log('Produto selecionado:', event.detail.id);
  console.log('Origem:', event.target); // o <product-card> host element
  console.log('Composto:', event.composedPath()); // o caminho completo dentro do shadow
});
```

---

## `event.composedPath()` — o caminho real dentro do shadow

```javascript
element.addEventListener('click', (event) => {
  // Retorna o path completo, incluindo o shadow DOM interno
  event.composedPath();
  // [<button> (shadow), <shadow-root>, <product-card>, <div>, <body>, <html>, <document>, <window>]
  
  // event.target com composed: caminho "retargeted" (aponta para o host element fora do shadow)
  event.target; // <product-card> (não o <button> interno)
});
```

---

## Comunicação bidirecional — request/response via Custom Events

```javascript
// Padrão de "request": um componente pede dado, outro responde via detalhe mutável
function requestCartCount() {
  const event = new CustomEvent('cart:count-request', {
    detail: { count: null }, // mutável — o handler vai preencher
    bubbles: true,
    cancelable: false,
  });

  document.dispatchEvent(event);
  return event.detail.count; // lê o valor preenchido pelo handler
}

// Handler responde modificando event.detail
document.addEventListener('cart:count-request', (event) => {
  event.detail.count = getCartItems().length;
});

// Uso
const count = requestCartCount(); // síncrono — funciona porque dispatchEvent é síncrono
```

---

> [!question] Para fixar
> 1. Qual a diferença entre um `Event` regular e um `CustomEvent`? O que `detail` armazena?
> 2. Por que `bubbles: true` é importante em custom events? Quando você usaria `bubbles: false`?
> 3. O que `composed: true` faz? Em qual cenário você precisaria disso?
> 4. `dispatchEvent` é síncrono ou assíncrono? O que isso implica para o padrão request/response?
> 5. Como `event.target` difere de `event.composedPath()[0]` quando o evento veio de dentro de um Shadow DOM?

---

## Veja também

- [[03-Dominios/Tecnologia/Plataforma Web/Eventos/04 - Event delegation|04 — Event delegation]] — anterior
- [[03-Dominios/Tecnologia/Plataforma Web/Eventos/06 - Timers e microtasks|06 — Timers e microtasks]] — próxima
- [[03-Dominios/Tecnologia/Plataforma Web/DOM/07 - template e cloneNode|DOM 07 — Web Components]] — contexto de Shadow DOM e custom elements
