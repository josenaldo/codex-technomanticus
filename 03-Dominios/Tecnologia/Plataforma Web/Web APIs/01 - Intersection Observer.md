---
title: "Intersection Observer"
created: 2026-06-28
updated: 2026-06-28
type: note
fase: Iniciado
tags:
  - plataforma-web
  - web-apis
  - browser
  - javascript
  - performance
  - entrevista
publish: true
---

# Intersection Observer

> [!abstract] TL;DR
> Intersection Observer detecta quando um elemento entra ou sai do viewport (ou de outro elemento de referência) sem ouvir o evento `scroll` — que é caro e precisa de `getBoundingClientRect` a cada tick. O Observer é assíncrono, não bloqueia o main thread, e entrega notificações em batch após o layout. Ideal para: lazy loading de imagens, animações on-scroll, infinite scroll, tracking de visibilidade de anúncios.

---

## Criar um observer

```javascript
const observer = new IntersectionObserver(callback, options);
```

```javascript
const observer = new IntersectionObserver(
  (entries, observer) => {
    // entries: array de IntersectionObserverEntry
    // Um entry por elemento observado que mudou de estado de intersecção
    entries.forEach(entry => {
      entry.target;           // o elemento observado
      entry.isIntersecting;   // boolean — está visível?
      entry.intersectionRatio; // 0.0 a 1.0 — fração visível
      entry.intersectionRect; // DOMRect da área de intersecção
      entry.boundingClientRect; // DOMRect do elemento
      entry.rootBounds;       // DOMRect da raiz (viewport ou root option)
      entry.time;             // timestamp
    });
  },
  {
    root: null,               // null = viewport; ou outro elemento como container
    rootMargin: '0px',        // margem ao redor da raiz (CSS shorthand)
    threshold: 0,             // 0 = qualquer pixel; 1.0 = 100% visível; array = múltiplos
  }
);
```

---

## Observar elementos

```javascript
// Observar um elemento
observer.observe(element);

// Parar de observar
observer.unobserve(element);

// Parar todos os elementos
observer.disconnect();
```

---

## Lazy loading de imagens

O uso mais comum — carregar imagens apenas quando estão próximas do viewport:

```javascript
const imageObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (!entry.isIntersecting) return;

    const img = entry.target;
    img.src = img.dataset.src;     // trocar src placeholder pelo real
    img.srcset = img.dataset.srcset || '';
    img.classList.remove('lazy'); // remover classe de placeholder
    
    imageObserver.unobserve(img); // parar de observar — já carregou
  });
}, {
  rootMargin: '200px', // começar 200px ANTES de entrar no viewport
});

document.querySelectorAll('img[data-src]').forEach(img => {
  imageObserver.observe(img);
});
```

```html
<!-- HTML: placeholder e src real em data-src -->
<img
  src="placeholder.jpg"
  data-src="real-image.jpg"
  data-srcset="real-400.jpg 400w, real-800.jpg 800w"
  alt="Imagem"
  class="lazy"
  loading="lazy"
>
```

> [!tip] `loading="lazy"` nativo
> O atributo `loading="lazy"` em `<img>` faz lazy loading sem JavaScript. Use-o para imagens simples. Intersection Observer ainda é necessário para: lazy loading de backgrounds CSS, animações on-scroll, infinite scroll, e lógica customizada de visibilidade.

---

## Animações on-scroll — reveal

```javascript
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      revealObserver.unobserve(entry.target); // anima uma vez
    }
  });
}, {
  threshold: 0.15,             // 15% visível para disparar
  rootMargin: '0px 0px -80px 0px', // recuar 80px do bottom (anima um pouco antes)
});

document.querySelectorAll('.reveal').forEach(el => {
  revealObserver.observe(el);
});
```

```css
.reveal {
  opacity: 0;
  transform: translateY(30px);
  transition: opacity 0.6s ease, transform 0.6s ease;
}
.reveal.visible {
  opacity: 1;
  transform: translateY(0);
}

/* Respeitar preferência do usuário */
@media (prefers-reduced-motion: reduce) {
  .reveal,
  .reveal.visible {
    opacity: 1;
    transform: none;
    transition: none;
  }
}
```

---

## Infinite scroll

```javascript
// Observar o "sentinel" — um elemento no final da lista
const sentinel = document.querySelector('.scroll-sentinel');

const scrollObserver = new IntersectionObserver((entries) => {
  if (entries[0].isIntersecting && !isLoading) {
    loadMoreItems();
  }
}, {
  rootMargin: '100px', // carregar 100px antes de chegar ao sentinel
});

scrollObserver.observe(sentinel);

async function loadMoreItems() {
  isLoading = true;
  
  const items = await fetchNextPage();
  if (items.length === 0) {
    scrollObserver.disconnect(); // sem mais páginas
    return;
  }
  
  renderItems(items);
  isLoading = false;
}
```

---

## `threshold` — múltiplos gatilhos

```javascript
// Disparar em 0%, 25%, 50%, 75%, 100% de visibilidade
const progressObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    const ratio = entry.intersectionRatio;
    const bar = entry.target.querySelector('.progress-bar');
    bar.style.width = `${ratio * 100}%`;
  });
}, {
  threshold: [0, 0.25, 0.5, 0.75, 1.0],
});

// Tracking de tempo visível (para analytics de leitura)
const readTimeObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.dataset.visibleSince = Date.now();
    } else {
      const visibleFor = Date.now() - entry.target.dataset.visibleSince;
      trackReadTime(entry.target.id, visibleFor);
    }
  });
}, { threshold: 0.5 }); // 50% visível para contar como "lendo"
```

---

## `rootMargin` — margem ao redor da raiz

```javascript
// rootMargin funciona como CSS margin (top right bottom left)
// Valores negativos reduzem a área; positivos expandem

{
  rootMargin: '50px',          // expandir 50px em todos os lados
  rootMargin: '0px 0px 100px', // expandir 100px embaixo
  rootMargin: '-20% 0px',      // reduzir 20% de cima e baixo (gatilho mais tardio)
  rootMargin: '200px 0px -50px 0px', // pré-carregar 200px antes, 50px menos embaixo
}
```

---

## `root` customizado — scroll dentro de um container

```javascript
const container = document.querySelector('.scrollable-container');

const containerObserver = new IntersectionObserver(callback, {
  root: container,         // usar o container como raiz em vez do viewport
  rootMargin: '0px',
  threshold: 0.1,
});

// Observar itens dentro do container
container.querySelectorAll('.item').forEach(item => {
  containerObserver.observe(item);
});
```

---

> [!question] Para fixar
> 1. Por que Intersection Observer é mais performático que ouvir `scroll` com `getBoundingClientRect`?
> 2. O que `rootMargin: '200px'` faz? Em qual caso de uso isso é especialmente útil?
> 3. Você quer disparar uma animação toda vez que o elemento entra no viewport (não só na primeira vez). O que muda no código?
> 4. O que `threshold: [0, 0.5, 1.0]` faz? O callback dispara quantas vezes por elemento?
> 5. Como você implementaria infinite scroll com Intersection Observer? Qual elemento você observaria?

---

## Veja também

- [[03-Dominios/Tecnologia/Plataforma Web/Web APIs/02 - MutationObserver e ResizeObserver|02 — MutationObserver e ResizeObserver]] — próxima
- [[03-Dominios/Tecnologia/Plataforma Web/Rendering Pipeline/04 - Reflow e repaint|Rendering Pipeline 04]] — por que evitar getBoundingClientRect em scroll handlers
- [[03-Dominios/Tecnologia/Plataforma Web/Eventos/07 - Padrões avançados|Eventos 07 — Padrões avançados]] — passive:true para scroll handlers
