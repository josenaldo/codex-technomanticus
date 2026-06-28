---
title: "Eventos de formulário e foco"
created: 2026-06-28
updated: 2026-06-28
type: note
fase: Iniciado
tags:
  - plataforma-web
  - eventos
  - browser
  - formulario
  - javascript
  - entrevista
publish: true
---

# Eventos de formulário e foco

> [!abstract] TL;DR
> Formulários têm três camadas de eventos: entrada do usuário (`input`/`change`), foco (`focus`/`blur`/`focusin`/`focusout`), e submissão (`submit`/`reset`). A distinção crítica: `input` dispara a cada caractere digitado; `change` dispara ao perder o foco com valor diferente (ou ao selecionar em checkboxes/selects). `submit` é o lugar certo para validar e enviar — não `click` no botão. A Constraint Validation API permite validação nativa sem JS.

---

## Eventos de entrada — `input` vs `change`

```javascript
const input = document.querySelector('input[type="text"]');

// input: dispara a cada mudança de valor (cada tecla, cada colagem)
input.addEventListener('input', (event) => {
  console.log('Valor atual:', event.target.value);
  // Ideal para: busca em tempo real, contagem de caracteres, validação on-the-fly
});

// change: dispara quando o valor muda E o elemento perde o foco
input.addEventListener('change', (event) => {
  console.log('Valor final:', event.target.value);
  // Ideal para: validação ao sair do campo, persistência
});
```

### Comportamento por tipo de input

| Elemento | `input` | `change` |
|---|---|---|
| `<input type="text">` | A cada caractere | Ao perder foco com valor diferente |
| `<input type="checkbox">` | Ao clicar | Ao clicar (sincrônico) |
| `<input type="radio">` | Ao selecionar | Ao selecionar (sincrônico) |
| `<input type="range">` | Ao arrastar | Ao soltar |
| `<select>` | Ao selecionar opção | Ao selecionar opção (sincrônico) |
| `<input type="file">` | Ao selecionar arquivo | Ao selecionar arquivo |

```javascript
// Checkbox — change é o evento correto
checkbox.addEventListener('change', (event) => {
  console.log('Marcado:', event.target.checked);
});

// Select — change é o evento correto
select.addEventListener('change', (event) => {
  console.log('Selecionado:', event.target.value);
});

// Range — use input para feedback em tempo real
range.addEventListener('input', (event) => {
  output.textContent = event.target.value;
});
```

### `beforeinput` — interceptar antes da mudança

```javascript
// beforeinput: dispara ANTES de `input`, permite cancelar a entrada
input.addEventListener('beforeinput', (event) => {
  // Só permite dígitos
  if (event.inputType === 'insertText' && !/^\d$/.test(event.data)) {
    event.preventDefault(); // cancela a entrada
  }
  
  // event.inputType: "insertText", "deleteContentBackward", "insertFromPaste", etc.
  // event.data: o texto que seria inserido
});
```

---

## Eventos de foco

```javascript
const input = document.querySelector('input');

// focus / blur — NÃO borbulham
input.addEventListener('focus', () => {
  console.log('Focado');
  // Não propaga — handlers em ancestrais não recebem
});
input.addEventListener('blur', () => {
  console.log('Desfocado');
});

// focusin / focusout — BORBULHAM
form.addEventListener('focusin', (event) => {
  console.log('Algum filho ganhou foco:', event.target);
});
form.addEventListener('focusout', (event) => {
  console.log('Algum filho perdeu foco:', event.target);
});
```

### Rastrear se o foco está dentro de um container

```javascript
const container = document.querySelector('.search-container');

container.addEventListener('focusin', () => {
  container.classList.add('focused');
});

container.addEventListener('focusout', (event) => {
  // focusout dispara antes de focusin do próximo elemento
  // Checar se o foco foi para dentro do mesmo container
  if (!container.contains(event.relatedTarget)) {
    container.classList.remove('focused');
  }
});
```

`event.relatedTarget`: o elemento que recebe o foco (em `blur`/`focusout`) ou o elemento que perde o foco (em `focus`/`focusin`).

### Foco programático

```javascript
// Focar um elemento
input.focus();
input.focus({ preventScroll: true }); // sem scroll automático

// Desfoca o elemento que tem foco atualmente
document.activeElement.blur();

// Verificar qual elemento tem foco
document.activeElement; // o elemento com foco atual
document.hasFocus();    // se o documento tem foco (em foreground)

// Tornar qualquer elemento focável
el.setAttribute('tabindex', '0');    // focável pelo Tab, sem alterar a ordem natural
el.setAttribute('tabindex', '-1');   // focável via .focus(), mas não pelo Tab
el.setAttribute('tabindex', '1');    // ❌ evite: altera a ordem natural do Tab
```

---

## Submissão de formulário — `submit`

```javascript
const form = document.querySelector('form');

// ✅ Sempre ouvir 'submit' no form — não 'click' no botão
// submit dispara ao clicar em <button type="submit">, pressionar Enter em input, etc.
form.addEventListener('submit', (event) => {
  event.preventDefault(); // impede a submissão nativa (reload da página)

  // Coletar dados
  const data = new FormData(form);
  const payload = Object.fromEntries(data.entries());
  // Ou acessar individualmente:
  data.get('email');
  data.getAll('skills'); // para múltiplos values (checkboxes, multi-select)

  // Enviar
  fetch('/api/submit', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
});
```

### `FormData` — coletar dados do formulário

```javascript
const form = document.querySelector('form');
const data = new FormData(form);

// Ler
data.get('name');           // string (primeiro valor)
data.getAll('hobbies');     // array de strings
data.has('name');           // boolean

// Modificar antes de enviar
data.set('name', 'João');
data.append('tag', 'novo');
data.delete('campo_interno');

// Iterar
for (const [key, value] of data) {
  console.log(key, value);
}

// Enviar arquivos: FormData encode corretamente como multipart/form-data
const fileInput = document.querySelector('input[type="file"]');
const formData = new FormData();
formData.append('file', fileInput.files[0]);
fetch('/upload', { method: 'POST', body: formData });
// Não colocar Content-Type manualmente — o browser define com o boundary correto
```

### `reset`

```javascript
form.addEventListener('reset', (event) => {
  // Dispara antes de os campos serem resetados
  // event.preventDefault() cancela o reset
  console.log('Form sendo resetado');
});

// Programático
form.reset(); // reseta todos os campos para os valores iniciais do HTML
```

---

## Constraint Validation API — validação nativa

HTML5 tem validação nativa sem JavaScript:

```html
<form>
  <input type="email" required placeholder="email@exemplo.com">
  <input type="text" minlength="3" maxlength="50" pattern="[A-Za-z]+">
  <input type="number" min="0" max="100" step="5">
  <input type="url" required>
</form>
```

```javascript
// Verificar validade programaticamente
const input = document.querySelector('input[type="email"]');
input.checkValidity();        // boolean — true se válido
input.validity.valueMissing;  // required mas vazio
input.validity.typeMismatch;  // tipo errado (email com @, etc.)
input.validity.patternMismatch; // não bate com pattern
input.validity.tooShort;      // menor que minlength
input.validity.tooLong;       // maior que maxlength
input.validity.rangeUnderflow; // menor que min
input.validity.rangeOverflow;  // maior que max

// Validação customizada
input.setCustomValidity('Email já cadastrado');  // marca como inválido
input.setCustomValidity('');                      // limpa (marca como válido)

// Validar o form inteiro
form.checkValidity(); // false se algum campo inválido
form.reportValidity(); // false + mostra tooltip de erro nativo
```

```javascript
// Pattern de validação customizada + native
form.addEventListener('submit', (event) => {
  // Validar primeiro com a API nativa
  if (!form.checkValidity()) {
    form.reportValidity();
    event.preventDefault();
    return;
  }

  // Validações extras que HTML não cobre
  const password = form.querySelector('[name="password"]');
  const confirm = form.querySelector('[name="confirm-password"]');
  if (password.value !== confirm.value) {
    confirm.setCustomValidity('Senhas não coincidem');
    confirm.reportValidity();
    event.preventDefault();
    return;
  }
  confirm.setCustomValidity(''); // limpar antes de submeter
  
  event.preventDefault();
  submitForm();
});
```

### Estilizar com pseudo-classes de validação

```css
/* Estados de validação sem JavaScript */
input:valid { border-color: green; }
input:invalid { border-color: red; }

/* Só após interação do usuário */
input:user-valid { border-color: green; }
input:user-invalid { border-color: red; }

/* required + vazio */
input:placeholder-shown { /* campo com placeholder visível (provavelmente vazio) */ }
```

---

> [!question] Para fixar
> 1. Qual a diferença entre `input` e `change` para `<input type="text">`? E para `<input type="checkbox">`?
> 2. Por que `focus` não borbulha? Como você detectaria quando qualquer input dentro de um form ganhou foco?
> 3. Por que ouvir `submit` no form é melhor que ouvir `click` no botão de submit?
> 4. O que `new FormData(form)` faz? Como você enviaria um arquivo usando FormData?
> 5. O que `input.setCustomValidity('Mensagem')` faz? Como você limparia o erro depois?

---

## Veja também

- [[03-Dominios/Tecnologia/Plataforma Web/Eventos/02 - Eventos de teclado e ponteiro|02 — Teclado e ponteiro]] — anterior
- [[03-Dominios/Tecnologia/Plataforma Web/Eventos/04 - Event delegation|04 — Event delegation]] — próxima
- [[03-Dominios/Tecnologia/HTML/index|HTML]] — formulários semânticos e atributos de validação
