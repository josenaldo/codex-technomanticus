---
title: "Event delegation"
created: 2026-06-28
updated: 2026-06-28
type: note
fase: adepto
tags:
  - plataforma-web
  - eventos
  - browser
  - javascript
  - performance
  - entrevista
publish: true
---

# Event delegation

> [!abstract] TL;DR
> Event delegation é o padrão de colocar um único listener no container (em vez de um por item filho) e usar `event.target.closest()` para identificar qual item foi clicado. Funciona porque eventos borbulham. Vantagens: menos memória, suporte automático a itens adicionados dinamicamente, código mais simples. A única armadilha: elementos que não borbulham (`focus`, `blur`) — use `focusin`/`focusout` no lugar.

---

## O problema com um listener por item

```javascript
// ❌ Um listener por item — N listeners para N items
const items = document.querySelectorAll('.todo-item');
items.forEach(item => {
  item.addEventListener('click', (event) => {
    toggleTodo(item.dataset.id);
  });
});

// Problemas:
// 1. Memória: 1000 itens = 1000 listeners
// 2. Itens adicionados dinamicamente não têm listener
// 3. Ao remover itens do DOM, os listeners precisam ser removidos manualmente
```

---

## Event delegation — um listener no container

```javascript
// ✅ Um único listener no container
const list = document.querySelector('.todo-list');

list.addEventListener('click', (event) => {
  // event.target = o elemento que foi CLICADO
  // closest() sobe até encontrar o item — independente de qual filho foi clicado
  const item = event.target.closest('.todo-item');
  if (!item) return; // clique fora de qualquer item

  toggleTodo(item.dataset.id);
});
```

Se a estrutura do item for:
```html
<li class="todo-item" data-id="42">
  <input type="checkbox">
  <span class="todo-item__label">Fazer compras</span>
  <button class="btn btn--delete">✕</button>
</li>
```

Clicar no `<span>`, no `<input>` ou no `<button>` — em todos os casos, `event.target.closest('.todo-item')` retorna o `<li>` correto.

---

## Múltiplas ações no mesmo container

```javascript
const list = document.querySelector('.task-list');

list.addEventListener('click', (event) => {
  // Verificar qual botão foi clicado usando closest() e matches()
  const deleteBtn = event.target.closest('.btn--delete');
  const editBtn = event.target.closest('.btn--edit');
  const checkbox = event.target.closest('input[type="checkbox"]');

  if (deleteBtn) {
    const item = deleteBtn.closest('.task-item');
    deleteTask(item.dataset.id);
    return;
  }

  if (editBtn) {
    const item = editBtn.closest('.task-item');
    openEditor(item.dataset.id);
    return;
  }

  if (checkbox) {
    const item = checkbox.closest('.task-item');
    toggleTask(item.dataset.id);
    return;
  }
});
```

### Pattern alternativo com `data-action`

Mais declarativo — a responsabilidade de "o que fazer" fica no HTML:

```html
<li class="task-item" data-id="42">
  <input type="checkbox" data-action="toggle">
  <span class="task-item__label">Tarefa</span>
  <button data-action="edit">Editar</button>
  <button data-action="delete">Deletar</button>
</li>
```

```javascript
const handlers = {
  toggle: (el) => toggleTask(el.closest('.task-item').dataset.id),
  edit:   (el) => openEditor(el.closest('.task-item').dataset.id),
  delete: (el) => deleteTask(el.closest('.task-item').dataset.id),
};

list.addEventListener('click', (event) => {
  const trigger = event.target.closest('[data-action]');
  if (!trigger) return;
  
  const action = trigger.dataset.action;
  const handler = handlers[action];
  if (handler) handler(trigger);
});
```

---

## Suporte automático a itens dinâmicos

O maior benefício de delegation: itens adicionados depois do listener já são cobertos.

```javascript
// Lista com delegation já registrado
const list = document.querySelector('.todo-list');
list.addEventListener('click', handleListClick);

// Adicionar item depois — automaticamente ouve os eventos
function addTodoItem(todo) {
  const li = document.createElement('li');
  li.className = 'todo-item';
  li.dataset.id = todo.id;
  li.innerHTML = `
    <span>${escapeHtml(todo.label)}</span>
    <button data-action="delete">✕</button>
  `;
  list.appendChild(li); // o listener do container já cobre este novo item
}
```

---

## Armadilhas do event delegation

### 1. Eventos que não borbulham

```javascript
// ❌ focus e blur não borbulham — delegation não funciona
list.addEventListener('focus', handleFocus); // não pega os inputs filhos

// ✅ Use focusin/focusout (borbulham)
list.addEventListener('focusin', handleFocus);
list.addEventListener('focusout', handleBlur);

// ✅ Ou use capture: true (o evento desce e você o pega)
list.addEventListener('focus', handleFocus, { capture: true });
```

### 2. `stopPropagation` em filhos quebra delegation

```javascript
// Se algum handler filho para a propagação, o container não recebe o evento
item.addEventListener('click', (event) => {
  event.stopPropagation(); // ❌ mata o delegation do container!
  doSomething();
});

// ✅ Evite stopPropagation quando usando delegation
// Prefira event.preventDefault() se precisar bloquear comportamento do browser
```

### 3. Múltiplas funções `closest()` — performatico, mas pode ser repetitivo

```javascript
// Se você chama closest() muitas vezes com o mesmo seletor, pode ser custoso em listas grandes
// Solução: chamar uma vez e reutilizar
const item = event.target.closest('.item');
if (!item) return;
const id = item.dataset.id;
const label = item.querySelector('.item__label'); // dentro do item encontrado
```

---

## Delegation em tabelas — armadilha de CSS

Tabelas com `border-collapse: collapse` têm um comportamento peculiar: o `<td>` recebe o evento de clique, mas o `<tr>` pode não ser o ancestral imediato dependendo de como o DOM da tabela está estruturado.

```html
<table>
  <tbody>
    <tr data-row-id="1" class="data-row">
      <td>João</td>
      <td>30</td>
      <td><button data-action="edit">Editar</button></td>
    </tr>
  </tbody>
</table>
```

```javascript
const table = document.querySelector('table');
table.addEventListener('click', (event) => {
  // ✅ closest() resolve a ambiguidade
  const row = event.target.closest('.data-row');
  if (!row) return;
  
  const action = event.target.closest('[data-action]')?.dataset.action;
  if (action === 'edit') editRow(row.dataset.rowId);
  else selectRow(row.dataset.rowId);
});
```

---

## Implementar um mini event emitter com delegation

```javascript
// Sistema de eventos declarativo baseado em delegation
function createEventSystem(root) {
  const handlers = new Map(); // action → [handlers]

  root.addEventListener('click', (event) => {
    const trigger = event.target.closest('[data-action]');
    if (!trigger) return;
    
    const action = trigger.dataset.action;
    const list = handlers.get(action) || [];
    list.forEach(fn => fn(trigger, event));
  });

  return {
    on(action, handler) {
      if (!handlers.has(action)) handlers.set(action, []);
      handlers.get(action).push(handler);
    },
    off(action, handler) {
      const list = handlers.get(action) || [];
      handlers.set(action, list.filter(fn => fn !== handler));
    }
  };
}

const app = createEventSystem(document.querySelector('#app'));
app.on('save', (el) => saveItem(el.closest('[data-id]').dataset.id));
app.on('delete', (el) => deleteItem(el.closest('[data-id]').dataset.id));
```

---

> [!question] Para fixar
> 1. Explique event delegation em uma frase. Por que funciona?
> 2. Uma lista tem 500 itens com um botão de deletar cada. Compare o uso de memória entre: 500 listeners individuais vs delegation no container.
> 3. Você adiciona 10 novos itens à lista após o DOMContentLoaded. Com delegation, eles precisam de listeners novos?
> 4. Por que `delegation` não funciona com `focus` diretamente? Como resolver?
> 5. O que acontece com o delegation no container se um handler filho chama `stopPropagation()`?

---

## Veja também

- [[03-Dominios/Tecnologia/Plataforma Web/Eventos/03 - Eventos de formulário e foco|03 — Formulário e foco]] — anterior
- [[03-Dominios/Tecnologia/Plataforma Web/Eventos/05 - Custom events e comunicação|05 — Custom events]] — próxima
- [[03-Dominios/Tecnologia/Plataforma Web/DOM/02 - Seleção de elementos|DOM 02 — Seleção]] — closest() como base do delegation
