---
title: "Atributos, propriedades e dataset"
created: 2026-06-28
updated: 2026-06-28
type: note
fase: adepto
tags:
  - plataforma-web
  - dom
  - browser
  - javascript
  - entrevista
publish: true
---

# Atributos, propriedades e dataset

> [!abstract] TL;DR
> HTML tem **atributos** (o que está no marcador HTML) e o DOM tem **propriedades** (o estado atual do objeto JavaScript). Eles começam iguais mas divergem — `input.value` é o valor atual digitado; `input.getAttribute('value')` é o valor inicial do HTML. `classList` é a API moderna para classes CSS. `dataset` é o acesso limpo a `data-*` attributes. Saber a diferença atributo vs propriedade é uma pegunta clássica de entrevista.

---

## Atributos vs Propriedades — a distinção fundamental

Quando o browser parseia `<input type="text" value="inicial">`, cria um objeto DOM com:
- **Atributo** `value` = `"inicial"` (vive no HTML, persistente)
- **Propriedade** `value` = `"inicial"` (vive no objeto DOM, reflete o estado atual)

Quando o usuário digita "novo texto":
- **Atributo** `value` = ainda `"inicial"` (não muda)
- **Propriedade** `value` = `"novo texto"` (reflete o que está na tela)

```javascript
const input = document.querySelector('input');

// Propriedade — valor ATUAL (o que o usuário digitou)
input.value;                    // "novo texto"
input.checked;                  // true/false (checkbox)
input.disabled;                 // true/false

// Atributo — valor ORIGINAL do HTML
input.getAttribute('value');    // "inicial" (não muda com input do usuário)
input.getAttribute('disabled'); // "disabled" ou null (string, não boolean)
```

---

## API de atributos

```javascript
const el = document.querySelector('.card');

// Ler
el.getAttribute('data-id');          // string ou null
el.getAttribute('class');            // "card card--featured"
el.hasAttribute('hidden');           // true/false

// Escrever
el.setAttribute('aria-expanded', 'true');
el.setAttribute('data-count', 42);  // converte para string "42"

// Remover
el.removeAttribute('hidden');        // remove completamente o atributo

// Iterar todos os atributos
for (const attr of el.attributes) {
  console.log(attr.name, attr.value);
}
```

---

## Mapeamento atributo → propriedade

Nem todo atributo mapeia 1:1 para uma propriedade com o mesmo nome:

| Atributo HTML | Propriedade DOM | Tipo |
|---|---|---|
| `class="btn"` | `.className` | `string` |
| `for="input-id"` | `.htmlFor` | `string` |
| `readonly` | `.readOnly` | `boolean` |
| `colspan="2"` | `.colSpan` | `number` |
| `tabindex="0"` | `.tabIndex` | `number` |
| `checked` | `.defaultChecked` / `.checked` | `boolean` |

```javascript
// Atributo class → propriedade className
el.className;                      // string completa: "card card--active"
el.className = 'card';             // substitui TODA a string de classes

// Atributos boolean: presença = true, ausência = false
const btn = document.querySelector('button');
btn.disabled;                      // true se <button disabled>, false se não
btn.setAttribute('disabled', ''); // qualquer valor = true (inclusive "false"!)
btn.removeAttribute('disabled');   // para reabilitar

// ❌ Armadilha clássica:
btn.setAttribute('disabled', 'false'); // NÃO desabilita — 'false' é uma string truthy
btn.disabled = false;                  // ✅ Forma correta via propriedade
```

---

## `classList` — a API moderna de classes

`classList` é a forma correta de manipular classes CSS — mais legível e segura que editar `className`:

```javascript
const el = document.querySelector('.card');

// Verificar
el.classList.contains('active');          // true/false

// Adicionar
el.classList.add('active');
el.classList.add('active', 'visible', 'loaded'); // múltiplas

// Remover
el.classList.remove('active');
el.classList.remove('active', 'visible');

// Toggle — adiciona se não tem, remove se tem
el.classList.toggle('active');
el.classList.toggle('active', condition); // force: true = add, false = remove

// Substituir
el.classList.replace('primary', 'secondary'); // true se substituiu, false se 'primary' não existia

// Iterar
for (const cls of el.classList) {
  console.log(cls);
}

// Converter para array
const classes = [...el.classList];
```

### Pattern com `toggle` + force

```javascript
// toggle com condição boolean é mais limpo que if/else
const isExpanded = /* alguma lógica */;

// ❌ Verboso
if (isExpanded) {
  btn.classList.add('expanded');
} else {
  btn.classList.remove('expanded');
}

// ✅ Limpo
btn.classList.toggle('expanded', isExpanded);
btn.setAttribute('aria-expanded', String(isExpanded));
```

---

## `dataset` — atributos `data-*`

`data-*` attributes são a forma oficial de embutir dados no HTML que o JavaScript vai ler. `dataset` é a API para acessá-los:

```html
<div
  class="product-card"
  data-product-id="42"
  data-product-name="Teclado"
  data-in-stock="true"
  data-price="299.90"
></div>
```

```javascript
const card = document.querySelector('.product-card');

// Ler — kebab-case vira camelCase
card.dataset.productId;    // "42" (sempre string!)
card.dataset.productName;  // "Teclado"
card.dataset.inStock;      // "true" (string, não boolean)
card.dataset.price;        // "299.90" (string, não number)

// Sempre converter o tipo se necessário
const id = Number(card.dataset.productId);        // 42
const inStock = card.dataset.inStock === 'true';  // true (boolean)
const price = parseFloat(card.dataset.price);     // 299.90

// Escrever
card.dataset.productId = 99;
card.dataset.newField = 'valor'; // cria data-new-field no HTML

// Deletar
delete card.dataset.productName; // remove o atributo data-product-name

// Iterar todos os data attributes
for (const [key, value] of Object.entries(card.dataset)) {
  console.log(key, value); // camelCase key
}
```

---

## `dataset` como contrato de componente

Um padrão robusto é usar `data-*` para ligar HTML e JS sem classes CSS:

```html
<!-- HTML define o comportamento declarativamente -->
<button data-action="toggle" data-target="#menu" data-animation="slide">
  Menu
</button>

<nav id="menu" data-state="closed">
  ...
</nav>
```

```javascript
// JS lê os data attributes para descobrir o que fazer
document.addEventListener('click', (event) => {
  const trigger = event.target.closest('[data-action]');
  if (!trigger) return;

  const action = trigger.dataset.action;
  const targetId = trigger.dataset.target;
  const target = document.querySelector(targetId);

  if (action === 'toggle' && target) {
    const isOpen = target.dataset.state === 'open';
    target.dataset.state = isOpen ? 'closed' : 'open';
  }
});
```

```css
/* CSS reage ao estado via attribute selector */
[data-state="open"] { display: block; }
[data-state="closed"] { display: none; }
```

---

## Atributos ARIA

Atributos ARIA (`aria-*`) são atributos especiais para acessibilidade — sempre use via `setAttribute` ou propriedades ARIA:

```javascript
const btn = document.querySelector('.btn--toggle');
const panel = document.querySelector('.panel');

// Ler e escrever atributos ARIA
btn.getAttribute('aria-expanded');             // "true" ou "false" (string)
btn.setAttribute('aria-expanded', 'true');
btn.setAttribute('aria-controls', 'panel-id');
btn.setAttribute('aria-label', 'Fechar menu');

panel.setAttribute('role', 'region');
panel.setAttribute('aria-labelledby', 'panel-title');
panel.hidden = true; // equivale a setAttribute('hidden', '')

// Via propriedades ARIA (mais moderno — não suportado em todos os browsers)
// btn.ariaExpanded = 'true'; // string mesmo assim
```

---

> [!question] Para fixar
> 1. Um checkbox começa com `checked` no HTML. O usuário desmarca, depois você chama `input.getAttribute('checked')` — o que retorna? E `input.checked`?
> 2. O que acontece se você fizer `btn.setAttribute('disabled', 'false')`? Por que não desabilita o botão?
> 3. Um elemento tem `data-user-name="João"`. Como você lê isso via `dataset`? Como você deletaria esse atributo?
> 4. Qual a diferença entre `el.className = 'nova-classe'` e `el.classList.add('nova-classe')`?
> 5. Por que `el.classList.toggle('open', isOpen)` é melhor que `if/else` com `add`/`remove`?

---

## Veja também

- [[03-Dominios/Tecnologia/Plataforma Web/DOM/04 - Manipulação de DOM|04 — Manipulação de DOM]] — anterior
- [[03-Dominios/Tecnologia/Plataforma Web/DOM/06 - DocumentFragment e batch mutations|06 — DocumentFragment]] — próxima
- [[03-Dominios/Tecnologia/HTML/index|HTML]] — atributos HTML semânticos e ARIA
