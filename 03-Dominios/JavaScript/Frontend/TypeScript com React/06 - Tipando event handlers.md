---
title: "Tipando event handlers"
created: 2026-04-26
updated: 2026-04-26
type: concept
status: seedling
publish: true
tags: [typescript, react, typescript-react, frontend, events, handlers]
aliases:
  - Synthetic events tipados
  - React event types
---

# Tipando event handlers

> [!abstract] TL;DR
> Eventos React são *synthetic* (wrappers em torno do DOM nativo). Os tipos vivem em `React.MouseEvent<T>`, `React.ChangeEvent<T>`, `React.FormEvent<T>`, etc. O genérico `T` é o elemento HTML que originou o evento (`HTMLButtonElement`, `HTMLInputElement`...). Cuidado com `currentTarget` (o elemento que tem o listener — sempre `T`) vs `target` (qualquer node, pode ser child).

## O que é

Eventos em React não são os mesmos eventos DOM nativos que você manipula com `addEventListener`. O React intercepta a árvore inteira no root e expõe os handlers via JSX (`onClick`, `onChange`, `onSubmit`...) através de um sistema próprio chamado **synthetic events**. Cada evento sintético é um wrapper sobre o evento DOM original, com a mesma API conceitual (`preventDefault`, `stopPropagation`, `target`, `currentTarget`) e algumas garantias adicionais — principalmente compatibilidade cross-browser, normalização de campos e integração com o ciclo de render.

A distinção operacional importa porque os tipos TypeScript são diferentes em cada universo:

- **Em props JSX** (`onClick={...}`, `onChange={...}`) — você recebe um `React.SyntheticEvent` (ou um descendente especializado: `MouseEvent`, `ChangeEvent`, `FormEvent`, `KeyboardEvent`, `FocusEvent`, `PointerEvent`, etc). Todos vivem no namespace `React.`.
- **Em listeners imperativos** (`window.addEventListener('mousemove', ...)`, dentro de um `useEffect`) — você recebe o evento DOM **nativo**: `MouseEvent` global, `KeyboardEvent` global, `FocusEvent` global. Sem prefixo `React.`. São tipos distintos no `lib.dom.d.ts` do TS.

Os synthetic events especializados são genéricos no elemento que originou o handler: `React.MouseEvent<HTMLButtonElement>`, `React.ChangeEvent<HTMLInputElement>`, `React.FormEvent<HTMLFormElement>`. Esse generic `T` determina o tipo de `currentTarget` (sempre `T`) e, em alguns casos, o tipo das props específicas do evento — em `ChangeEvent<HTMLInputElement>`, por exemplo, `e.target.value` existe porque o `target` foi estreitado para `HTMLInputElement`. Trocar o generic por outro elemento (`ChangeEvent<HTMLDivElement>`) faz `e.target.value` deixar de existir, porque `<div>` não tem `value`.

## Por que importa

Tipar eventos errado é uma das fontes mais comuns de bugs sutis em React+TS, principalmente porque o sintoma quase sempre é runtime, não compile-time. Três armadilhas recorrentes ilustram o custo:

A primeira é acessar `e.target.value` em handlers que não são de input. Um `onClick` em `<div>` recebe `React.MouseEvent<HTMLDivElement>`, e `e.target` é `EventTarget` genérico — não tem `.value`. Sem tipagem, o dev escreve `(e) => console.log(e.target.value)` e em runtime recebe `undefined`. Com tipagem correta, o TS recusa: `Property 'value' does not exist on type 'EventTarget'`. O erro vira instantâneo em vez de virar suporte.

A segunda é confundir `target` com `currentTarget`. `currentTarget` é o elemento que tem o listener — sempre tipado como o generic `T`. `target` é o elemento concreto onde o evento aconteceu, que pode ser qualquer descendente (event bubbling). Em uma `<ul onClick>` com `<li>` filhos, clicar num `<li>` faz `e.target` ser `HTMLLIElement` e `e.currentTarget` ser `HTMLUListElement`. Tratar os dois como se fossem a mesma coisa quebra event delegation, padrão comum no ecossistema.

A terceira é cair no `(e: any) =>` quando o handler "fica complicado". O `any` apaga toda a segurança que o React+TS oferece — preventDefault em evento sem default, leitura de campos inexistentes, tudo passa silenciosamente. Pior: os autocompletes do editor desaparecem, e o dev passa a copiar nomes de propriedades de cabeça. A regra prática é não usar `any` em handlers — se o tipo correto é difícil de descobrir, hover no `onClick` da JSX revela a assinatura esperada.

## Como funciona

### Sample 1 — `onClick` em `<button>`

```typescript
function Button() {
  const onClick = (e: React.MouseEvent<HTMLButtonElement>) => {
    e.preventDefault();
    console.log(e.currentTarget); // HTMLButtonElement
  };

  return <button onClick={onClick}>OK</button>;
}
```

`React.MouseEvent<HTMLButtonElement>` é o tipo canônico para `onClick` em `<button>`. O generic `<HTMLButtonElement>` informa ao TS que `e.currentTarget` é o próprio botão — útil quando o handler precisa ler `disabled`, `form`, `dataset` ou outros atributos do elemento. `e.preventDefault()` cancela o comportamento default (relevante quando o botão está dentro de `<form>` e o tipo default é `submit`).

### Sample 2 — `onChange` em `<input>` text

```typescript
function TextInput() {
  const onChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    console.log(e.target.value); // string — disponível em <input>
  };

  return <input type="text" onChange={onChange} />;
}
```

Em `ChangeEvent<HTMLInputElement>`, o `target` é estreitado para `HTMLInputElement`, e portanto `.value` é acessível e tipado como `string`. Esse é um dos poucos casos onde usar `e.target` é seguro e idiomático — o generic já garantiu que o target é o elemento esperado. Para `<select>`, troque por `HTMLSelectElement`; para `<textarea>`, `HTMLTextAreaElement`.

### Sample 3 — `onSubmit` em `<form>`

```typescript
function MyForm() {
  const onSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    // currentTarget é HTMLFormElement — sempre
    const email = formData.get('email');
    console.log(email);
  };

  return (
    <form onSubmit={onSubmit}>
      <input name="email" type="email" />
      <button type="submit">Enviar</button>
    </form>
  );
}
```

`FormEvent<HTMLFormElement>` é o tipo canônico para `onSubmit`. `e.preventDefault()` é quase sempre obrigatório — sem ele, o browser tenta fazer submit nativo (recarrega a página). `new FormData(e.currentTarget)` é o pattern idiomático para extrair valores de forma genérica: o `currentTarget` é tipado como `HTMLFormElement`, e `FormData` aceita exatamente esse tipo. Usar `e.target` ali daria erro de tipo (`EventTarget` não é assinable a `HTMLFormElement` sem narrowing).

### Sample 4 — `currentTarget` vs `target` (a confusão clássica)

```typescript
function ListClickable() {
  const onClick = (e: React.MouseEvent<HTMLUListElement>) => {
    // currentTarget: HTMLUListElement (o <ul> — onde o listener está)
    console.log(e.currentTarget.tagName); // "UL"

    // target: EventTarget — qualquer node descendente que recebeu o clique
    // Não é tipado com T; é genérico.
    if (e.target instanceof HTMLLIElement) {
      console.log(e.target.dataset.id); // narrow primeiro
    }
  };

  return (
    <ul onClick={onClick}>
      <li data-id="1">A</li>
      <li data-id="2">B</li>
    </ul>
  );
}
```

Esse é o pattern canônico de **event delegation**: um único listener no `<ul>` cobre todos os filhos `<li>`. `currentTarget` é sempre o `<ul>` (onde o handler está registrado), enquanto `target` é o elemento concreto que recebeu o clique — pode ser um `<li>`, ou um nó de texto dentro dele. O TS força narrowing: `e.target instanceof HTMLLIElement` estreita o tipo para `HTMLLIElement` no bloco do `if`, e só então `dataset.id` é acessível. Sem o narrow, `e.target.dataset` falha com `Property 'dataset' does not exist on type 'EventTarget'`.

### Sample 5 — Handler reutilizável tipado

```typescript
import { useState } from 'react';

// Handler genérico para forms — adiciona name/value ao state
function makeChangeHandler<T extends Record<string, unknown>>(
  setState: React.Dispatch<React.SetStateAction<T>>
) {
  return (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setState(prev => ({ ...prev, [name]: value }));
  };
}

// Uso:
function ProfileForm() {
  const [form, setForm] = useState({ name: '', email: '' });
  const handleChange = makeChangeHandler(setForm);

  return (
    <form>
      <input name="name" value={form.name} onChange={handleChange} />
      <input name="email" value={form.email} onChange={handleChange} />
    </form>
  );
}
```

A factory `makeChangeHandler` recebe o `setState` do estado-objeto e devolve um `onChange` reutilizável que distribui o valor pelo campo nomeado. O constraint `T extends Record<string, unknown>` garante que o estado é um objeto indexável por string, condição para o spread `{ ...prev, [name]: value }` ser seguro. `React.Dispatch<React.SetStateAction<T>>` é o tipo canônico do segundo elemento retornado por `useState<T>` — usar esse tipo na assinatura comunica claramente que o handler espera o setter, não o valor. Essa fábrica é o esqueleto de patterns mais sofisticados em libs como Formik e React Hook Form, cobertos em [[10 - Tipando formulários|nota 10]].

### Sample 6 — Listener nativo (em `useEffect` com `addEventListener`)

```typescript
import { useEffect } from 'react';

function MouseTracker() {
  useEffect(() => {
    // Aqui é DOM nativo, não synthetic — usa MouseEvent direto, sem React.
    const handler = (e: MouseEvent) => {
      console.log(e.clientX, e.clientY);
    };

    window.addEventListener('mousemove', handler);
    return () => window.removeEventListener('mousemove', handler);
  }, []);

  return <div>move o mouse</div>;
}
```

Quando o handler é registrado via `addEventListener` (na `window`, em refs DOM, em `document`), o tipo do evento é o **DOM nativo** — `MouseEvent` sem prefixo, vindo do `lib.dom.d.ts`. Os campos são parecidos (`clientX`, `clientY`, `target`, `currentTarget`), mas é um tipo diferente de `React.MouseEvent`. Misturar os dois (passar um `React.MouseEvent` para `addEventListener` ou vice-versa) dá erro de tipo. A regra mnemônica: **se o handler chega via prop JSX, é synthetic; se chega via `addEventListener`, é nativo**.

### Sample 7 — `KeyboardEvent` em input

```typescript
function SearchBox({ onSubmit }: { onSubmit: () => void }) {
  const onKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      onSubmit();
    }
  };

  return <input type="search" onKeyDown={onKeyDown} />;
}
```

`KeyboardEvent<HTMLInputElement>` cobre `onKeyDown`, `onKeyUp`, `onKeyPress` (deprecated, evite). O campo `e.key` é a string da tecla (`'Enter'`, `'Escape'`, `'a'`); `e.code` é o código físico da tecla no teclado (`'KeyA'`, `'Enter'`, `'Escape'`), independente do layout. Para shortcuts, `e.key` é o caminho idiomático.

## Na prática

Pattern dominante no ecossistema é o handler único que escuta todos os campos de um form e despacha pelo `name`. A versão minimalista cabe numa linha:

```typescript
const handleChange = (e: React.ChangeEvent<HTMLInputElement>) =>
  setForm(f => ({ ...f, [e.target.name]: e.target.value }));
```

Aplicado num form-objeto:

```typescript
const [form, setForm] = useState({ name: '', email: '', age: '' });

return (
  <>
    <input name="name" value={form.name} onChange={handleChange} />
    <input name="email" value={form.email} onChange={handleChange} />
    <input name="age" value={form.age} onChange={handleChange} />
  </>
);
```

Funciona porque `e.target.name` é a string do atributo `name="..."` do `<input>`, e `e.target.value` é o valor atual. O spread `{ ...f, [e.target.name]: e.target.value }` substitui apenas a chave correspondente, mantendo as outras intactas. É suficiente para forms simples, mas tem limites: validação inline, transformação de tipos (string → number), feedback granular por campo — tudo isso é onde libs como React Hook Form + Zod entram. Aprofundamento em [[10 - Tipando formulários|nota 10]].

## Armadilhas

- **Acessar `e.target.value` em `onClick`.** O `target` em `MouseEvent<HTMLButtonElement>` (ou em qualquer mouse event) é `EventTarget` genérico — não tem `.value`. O TS rejeita corretamente, mas em código com `any` ou type assertion abusiva o erro vira `undefined` em runtime. A propriedade `.value` só está em `ChangeEvent<HTMLInputElement>` (e similares para select/textarea), porque ali o target foi estreitado. Para ler valores em handlers de mouse, use `e.currentTarget` (que é tipado como o generic `T`) ou puxe o valor via ref.

- **Confundir `MouseEvent` (DOM nativo) com `React.MouseEvent` (synthetic).** Em listeners imperativos (`addEventListener`, `removeEventListener`), o tipo é o nativo (`MouseEvent` sem prefixo). Em props JSX (`onClick`, `onMouseMove`), é o synthetic (`React.MouseEvent`). São tipos diferentes — passar um por outro causa erros de assignability tipo `Type 'MouseEvent' is not assignable to type 'React.MouseEvent<HTMLDivElement>'`. A pista mnemônica: se você vê `addEventListener` perto, é nativo.

- **Usar `any` em handlers.** Sintoma: `(e: any) => { ... }`. Custo: TS perde toda a checagem, autocomplete some, propriedades inexistentes passam silenciosamente. Quando o tipo certo é difícil de adivinhar, hover na prop JSX (`onClick`) no editor revela a assinatura esperada. Última opção é `React.SyntheticEvent` (o pai de todos), que pelo menos preserva `preventDefault`, `stopPropagation`, `target` e `currentTarget` genericamente.

- **Esquecer o generic em `React.ChangeEvent` (ou em qualquer event tipado).** Sem `<HTMLInputElement>`, `e.target` vira `EventTarget` genérico e `.value` desaparece. O TS reclama com `Property 'value' does not exist on type 'EventTarget'`. A correção é sempre passar o generic do elemento que originou o handler: `React.ChangeEvent<HTMLInputElement>`, `React.MouseEvent<HTMLButtonElement>`, `React.FormEvent<HTMLFormElement>`.

- **Tipar `e.target` como o elemento, em vez de narrow via `instanceof`.** Em casos de event delegation (handler num pai, clique vem de filho), `e.target` é genuinamente `EventTarget` — não dá pra estreitar via generic do evento, porque o pai não sabe quem é o filho que vai disparar. A solução idiomática é narrow runtime: `if (e.target instanceof HTMLLIElement) { ... }`. Forçar com `as HTMLLIElement` mente para o TS e quebra silenciosamente quando o clique vem de outro descendente.

## Em entrevista

> "React events are synthetic — wrappers around the native DOM events. The TypeScript types live in `React.MouseEvent<T>`, `React.ChangeEvent<T>`, `React.FormEvent<T>`, and so on. The generic `T` is the HTML element that originated the event — it determines what `currentTarget` is. The most common mistake is confusing `currentTarget` with `target`: `currentTarget` is the element that has the listener (always typed as `T`), while `target` can be any descendant element that bubbled. For native listeners added via `addEventListener` in a `useEffect`, you use the DOM native types — `MouseEvent` without the `React.` prefix."

**Vocabulário-chave:** *synthetic event*, *native event*, *currentTarget*, *target*, *event bubbling*, *event delegation*.

**Pergunta típica de senior interview:** *"What's the difference between `e.target` and `e.currentTarget` in a React event handler?"* — resposta defensiva: `currentTarget` is the element the handler is attached to — it's typed as the generic `T` you passed to `React.MouseEvent<T>` or similar, so you always know its concrete type. `target` is the actual element where the event originated, which can be any descendant due to event bubbling. It's typed as `EventTarget` and requires runtime narrowing — typically `instanceof HTMLLIElement` or similar — before you can access element-specific properties. Event delegation patterns rely on this distinction: one listener on the parent, runtime narrowing to figure out which child triggered.

## Veja também

- [[05 - Tipando state e refs]]
- [[10 - Tipando formulários]]
- [[React]] — seção "Hooks essenciais" (eventos em handlers)
