---
title: "Manipulação de DOM"
created: 2026-06-28
updated: 2026-06-28
type: note
fase: Adepto
tags:
  - plataforma-web
  - dom
  - browser
  - javascript
  - entrevista
publish: true
---

# Manipulação de DOM

> [!abstract] TL;DR
> Manipulação de DOM é criar, inserir, mover, modificar e remover elementos. As APIs modernas (`append`, `prepend`, `insertAdjacentHTML`, `replaceWith`, `remove`) são mais ergonômicas que as legadas (`appendChild`, `insertBefore`, `removeChild`). A distinção crítica: `innerHTML` re-parseia HTML e é vetor de XSS quando o conteúdo vem do usuário; `textContent` é seguro e define texto puro; `innerText` considera estilo (mais lento, use menos).

---

## Criar elementos

```javascript
// Criar um elemento
const div = document.createElement('div');
const img = document.createElement('img');
const text = document.createTextNode('Olá');

// Criar com atributos imediatamente
const link = document.createElement('a');
link.href = 'https://exemplo.com';
link.textContent = 'Clique aqui';
link.className = 'link--external';
link.target = '_blank';
link.rel = 'noopener noreferrer'; // segurança

// Criar via innerHTML (cria subárvore — cuidado com XSS)
const wrapper = document.createElement('div');
wrapper.innerHTML = '<p class="texto">Conteúdo <strong>negrito</strong></p>';
// Só é seguro quando o conteúdo é seu próprio código, não dado de usuário
```

---

## Inserir elementos — API moderna

```javascript
const parent = document.querySelector('.container');
const newEl = document.createElement('p');
newEl.textContent = 'Novo parágrafo';

// append: no FIM do pai (aceita múltiplos, aceita strings)
parent.append(newEl);
parent.append('texto puro', document.createElement('br'), newEl2);

// prepend: no INÍCIO do pai
parent.prepend(newEl);

// before / after: antes/depois do elemento (como irmão)
const existing = document.querySelector('.existing');
existing.before(newEl);   // newEl fica antes de .existing
existing.after(newEl);    // newEl fica depois de .existing

// replaceWith: substituir o elemento
existing.replaceWith(newEl);
```

### `insertAdjacentHTML` — inserir HTML em posições específicas

```javascript
const el = document.querySelector('.card');

// Posições possíveis:
el.insertAdjacentHTML('beforebegin', '<div>antes do card</div>');
// ↳ [AQUI]<div class="card">...</div>

el.insertAdjacentHTML('afterbegin', '<header>início do card</header>');
// ↳ <div class="card">[AQUI]...</div>

el.insertAdjacentHTML('beforeend', '<footer>fim do card</footer>');
// ↳ <div class="card">...[AQUI]</div>

el.insertAdjacentHTML('afterend', '<div>após o card</div>');
// ↳ <div class="card">...</div>[AQUI]

// insertAdjacentElement: mesmo mas com Element (não string)
el.insertAdjacentElement('afterend', document.createElement('hr'));

// insertAdjacentText: texto puro (seguro para user input)
el.insertAdjacentText('beforeend', userInputText);
```

---

## APIs legadas — ainda comuns em código existente

```javascript
// appendChild: append um filho (só um Element, não string)
parent.appendChild(newEl);

// insertBefore: inserir antes de um filho referência
parent.insertBefore(newEl, referenceEl);
// Equivalente moderno: referenceEl.before(newEl)

// removeChild: remover um filho específico
parent.removeChild(childEl);
// Equivalente moderno: childEl.remove()

// replaceChild: substituir filho
parent.replaceChild(newEl, oldEl);
// Equivalente moderno: oldEl.replaceWith(newEl)
```

---

## Remover e mover elementos

```javascript
const el = document.querySelector('.removable');

// Remover da árvore
el.remove();

// Mover (inserir em outro lugar — remove do antigo automaticamente)
const target = document.querySelector('.new-parent');
target.append(el); // el é removido de onde estava e inserido aqui

// Limpar todos os filhos
parent.replaceChildren(); // sem argumentos — remove tudo
parent.innerHTML = '';    // alternativa (mas re-parseia)
```

---

## `innerHTML` vs `textContent` vs `innerText`

Esta é uma das distinções mais importantes para performance e segurança:

| Propriedade | Lê | Escreve | Parseia HTML | Considera CSS | Seguro para user input |
|---|---|---|---|---|---|
| `innerHTML` | HTML completo | Re-parseia HTML | Sim | Não | ❌ XSS |
| `textContent` | Texto bruto de todos os filhos | Substitui conteúdo como texto | Não | Não | ✅ |
| `innerText` | Texto visível (como renderizado) | Substitui como texto | Não | Sim (slow) | ✅ |
| `outerHTML` | HTML do elemento + filhos | Substitui o próprio elemento | Sim | Não | ❌ XSS |

```javascript
const el = document.querySelector('.output');

// textContent — SEMPRE para output de dados do usuário
el.textContent = userInput; // tags HTML ficam como texto literal (seguro)

// innerHTML — APENAS para HTML de strings template de código seu
el.innerHTML = `<strong>${formatName(user.name)}</strong>`; // OK se você controla formatName
el.innerHTML = userInput; // ❌ XSS: se userInput = '<img src=x onerror=alert(1)>'

// innerText — evite; é lento porque força layout (precisa saber o que é visível)
el.innerText = text; // OK mas use textContent quando possível
```

> [!warning] `innerHTML` e XSS
> Nunca insira dados de usuário, URL params, ou conteúdo externo via `innerHTML` sem sanitização. Use `textContent` para texto, ou bibliotecas como DOMPurify para HTML que precisa ser renderizado:
> ```javascript
> import DOMPurify from 'dompurify';
> el.innerHTML = DOMPurify.sanitize(untrustedHTML);
> ```

---

## Modificar conteúdo existente

```javascript
const el = document.querySelector('.card');

// Ler e escrever texto
const text = el.textContent;      // todo texto incluindo descendentes
el.textContent = 'Novo conteúdo'; // substitui TODOS os filhos por texto

// Ler e escrever HTML
const html = el.innerHTML;         // HTML interno como string
el.innerHTML = '<p>Novo HTML</p>'; // substitui filhos (re-parseia)

// Ler e escrever o elemento em si (inclusive)
const outerHtml = el.outerHTML;
el.outerHTML = '<div class="novo">...</div>'; // substitui o próprio elemento
```

---

## `replaceChildren` — substituir todos os filhos

```javascript
const list = document.querySelector('ul');

// Substituir todos os filhos de uma vez (limpo e eficiente)
const items = data.map(item => {
  const li = document.createElement('li');
  li.textContent = item.name;
  return li;
});

list.replaceChildren(...items);
// Equivalente a: list.innerHTML = '' + append de cada item
// Mas mais eficiente e sem re-parse
```

---

## Mover elemento sem perder event listeners

Um elemento que é `append`-ado é *movido* — não copiado. Seus event listeners se mantêm:

```javascript
const el = document.querySelector('.widget');
el.addEventListener('click', handler); // listener registrado

// Mover para outro container
document.querySelector('.other-container').append(el);
// O listener de 'click' continua ativo no elemento movido

// Para COPIAR sem listeners:
const clone = el.cloneNode(false);  // false = sem filhos
const deepClone = el.cloneNode(true); // true = com filhos
// cloneNode NÃO copia event listeners
```

---

> [!question] Para fixar
> 1. Qual a diferença entre `el.append('texto')` e `el.appendChild(document.createTextNode('texto'))`?
> 2. Por que `innerHTML = userInput` é um vetor de XSS? Dê um exemplo de payload malicioso e como a exploração ocorreria.
> 3. Qual a diferença entre `textContent` e `innerText`? Quando `innerText` retorna algo diferente de `textContent`?
> 4. O que `insertAdjacentHTML('afterend', html)` faz de diferente de `el.after(novoEl)`?
> 5. Um elemento tem 3 event listeners registrados. Você move ele para outro container com `append()` — os listeners são preservados? E se você usar `cloneNode(true)`?

---

## Veja também

- [[03-Dominios/Tecnologia/Plataforma Web/DOM/03 - Traversal|03 — Traversal]] — anterior
- [[03-Dominios/Tecnologia/Plataforma Web/DOM/05 - Atributos, propriedades e dataset|05 — Atributos e dataset]] — próxima
- [[03-Dominios/Tecnologia/Plataforma Web/DOM/06 - DocumentFragment e batch mutations|06 — DocumentFragment]] — performance de inserções em lote
