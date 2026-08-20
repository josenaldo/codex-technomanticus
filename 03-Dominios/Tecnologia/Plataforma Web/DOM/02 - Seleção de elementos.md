---
title: "Seleção de elementos"
created: 2026-06-28
updated: 2026-06-28
type: note
fase: iniciado
tags:
  - plataforma-web
  - dom
  - browser
  - javascript
  - entrevista
publish: true
---

# Seleção de elementos

> [!abstract] TL;DR
> `querySelector` e `querySelectorAll` são a forma moderna de selecionar elementos — usam seletores CSS, são expressivos e retornam resultados previsíveis (estáticos). As APIs legadas (`getElementById`, `getElementsBy*`) ainda existem e `getElementById` é a mais rápida por busca de ID direto. `closest()` e `matches()` são complementos essenciais para navegar contexto e verificar seletores.

---

## A família `querySelector`

```javascript
// querySelector: retorna o PRIMEIRO elemento que bate ou null
const btn = document.querySelector('.btn--primary');
const input = document.querySelector('form input[type="email"]');
const firstLi = document.querySelector('ul > li:first-child');

// querySelectorAll: retorna NodeList estática (todos os matches)
const cards = document.querySelectorAll('.card');
const inputs = document.querySelectorAll('form input:not([type="submit"])');

// NodeList: iterar com forEach (nativo), Array.from, ou spread
cards.forEach(card => card.classList.add('loaded'));
[...cards].map(card => card.dataset.id);
Array.from(cards).filter(card => card.classList.contains('active'));
```

`querySelectorAll` aceita **qualquer seletor CSS válido** — incluindo seletores modernos:

```javascript
// :has(), :is(), :not() — funcionam em querySelector
const cardsWithImg = document.querySelectorAll('.card:has(img)');
const headings = document.querySelectorAll(':is(h1, h2, h3)');
const notActive = document.querySelectorAll('.item:not(.active)');
```

---

## APIs legadas — quando ainda valem

```javascript
// getElementById: mais rápido para busca por ID (O(1) via hashtable)
const modal = document.getElementById('main-modal');
// Retorna Element ou null — sem # no argumento

// getElementsByClassName: HTMLCollection ao vivo
const cards = document.getElementsByClassName('card');

// getElementsByTagName: HTMLCollection ao vivo
const inputs = document.getElementsByTagName('input');

// getElementsByName: HTMLCollection ao vivo — útil para radio buttons
const options = document.getElementsByName('gender');
```

`getElementById` é o mais rápido de todos — o browser mantém uma hashtable de IDs. Para performance crítica (seleção de um elemento específico repetida muitas vezes), `getElementById` vence.

| Método | Retorna | Ao vivo | Velocidade |
|---|---|---|---|
| `getElementById` | `Element\|null` | — | Mais rápido (hashtable) |
| `getElementsByClassName` | `HTMLCollection` | Sim | Rápido |
| `getElementsByTagName` | `HTMLCollection` | Sim | Rápido |
| `querySelector` | `Element\|null` | Não | Rápido (otimizado) |
| `querySelectorAll` | `NodeList` | Não | Rápido |

---

## Escopo de seleção

Por padrão, `querySelector` e `querySelectorAll` buscam em todo o `document`. Mas podem ser chamados em qualquer Element:

```javascript
// Busca só dentro do card
const card = document.querySelector('.card');
const cardTitle = card.querySelector('.card__title');
const cardLinks = card.querySelectorAll('a');

// Cuidado: :scope define o elemento de contexto
const children = card.querySelectorAll(':scope > div'); // filhos diretos <div>
// sem :scope, > div buscaria em todo o document com o card como base — bugado em browsers antigos
```

---

## `closest()` — subir a árvore

`closest()` sobe a árvore DOM a partir do elemento e retorna o primeiro ancestral que bate o seletor (incluindo o próprio elemento):

```javascript
// Clique em um botão dentro de um card — encontrar o card
document.addEventListener('click', (event) => {
  const card = event.target.closest('.card');
  if (!card) return; // clique fora de qualquer card
  
  const cardId = card.dataset.id;
  console.log(`Clicou no card ${cardId}`);
});

// Verificar se o elemento está dentro de um formulário
const input = document.querySelector('input');
const form = input.closest('form');   // ancestor form ou null
const modal = input.closest('.modal'); // ancestor .modal ou null
```

`closest()` é a chave do **event delegation** — ao invés de adicionar um listener em cada item de uma lista, adiciona um no container e usa `closest()` para identificar qual item foi clicado.

---

## `matches()` — verificar seletor

`matches()` retorna `true` se o elemento satisfaz o seletor CSS:

```javascript
const btn = document.querySelector('button');

btn.matches('.btn')             // true se tem a classe btn
btn.matches('[disabled]')       // true se tem atributo disabled
btn.matches('.modal .btn')      // true se dentro de .modal e tem classe .btn
btn.matches(':not(.secondary)') // true se não tem classe secondary

// Caso de uso: filtrar dentro de event handler
document.addEventListener('click', (event) => {
  if (event.target.matches('.btn--delete')) {
    handleDelete(event.target);
  }
});
```

---

## Patterns de seleção segura

```javascript
// ❌ Assumir que o elemento existe — NullPointerError silencioso
document.querySelector('.modal').addEventListener('click', handler);

// ✅ Verificar antes de usar
const modal = document.querySelector('.modal');
modal?.addEventListener('click', handler);

// ✅ Ou verificar explicitamente
const modal = document.querySelector('.modal');
if (modal) modal.addEventListener('click', handler);

// ❌ querySelectorAll com forEach sem conversão (NodeList.forEach existe, mas não map/filter)
document.querySelectorAll('.card').map(card => card.id); // TypeError

// ✅ Converter para Array
Array.from(document.querySelectorAll('.card')).map(card => card.id);
[...document.querySelectorAll('.card')].map(card => card.id);
```

---

## Cache de seleções — quando faz diferença

Seleção de DOM tem custo. Em loops ou handlers frequentes, guarde a referência:

```javascript
// ❌ Seleciona o elemento a cada iteração
for (let i = 0; i < 1000; i++) {
  document.querySelector('.counter').textContent = i;
}

// ✅ Seleciona uma vez, usa a referência
const counter = document.querySelector('.counter');
for (let i = 0; i < 1000; i++) {
  counter.textContent = i;
}

// ✅ Cache em closures de componentes
function makeCounter(containerEl) {
  const display = containerEl.querySelector('.count'); // seleção única
  const btn = containerEl.querySelector('.btn');       // seleção única

  let count = 0;
  btn.addEventListener('click', () => {
    count++;
    display.textContent = count; // sem re-seleção
  });
}
```

---

> [!question] Para fixar
> 1. Qual a diferença entre `querySelector('.card')` e `getElementById('main-card')`? Quando usar cada um?
> 2. Por que iterar um `HTMLCollection` enquanto remove elementos pode causar bugs? O que `querySelectorAll` retorna de diferente?
> 3. Como `closest()` funciona? Escreva um event handler que, ao clicar em qualquer elemento dentro de uma lista, encontra o `<li>` pai.
> 4. O que `:scope` faz em `el.querySelectorAll(':scope > div')`? Por que é necessário?
> 5. `document.querySelectorAll('.btn').map(...)` lança um erro. Por que? Como corrigir?

---

## Veja também

- [[03-Dominios/Tecnologia/Plataforma Web/DOM/01 - O DOM como árvore|01 — O DOM como árvore]] — anterior
- [[03-Dominios/Tecnologia/Plataforma Web/DOM/03 - Traversal|03 — Traversal]] — próxima
- [[03-Dominios/Tecnologia/Plataforma Web/Eventos/04 - Event delegation|Eventos 04 — Event delegation]] — `closest()` como peça central
