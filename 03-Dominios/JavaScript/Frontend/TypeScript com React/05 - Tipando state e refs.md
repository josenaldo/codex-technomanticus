---
title: "Tipando state e refs"
created: 2026-04-26
updated: 2026-04-26
type: concept
status: seedling
publish: true
tags: [typescript, react, typescript-react, frontend, state, refs, useState, useRef]
aliases:
  - useState e useRef tipados
  - DOM refs vs mutable refs
---

# Tipando state e refs

> [!abstract] TL;DR
> `useState` infere de primitivos mas precisa anotar com `null`/`[]`/`{}`. Em React 19, `useRef` foi unificado: todo `useRef` retorna `RefObject<T>` (com `.current` mutável e nullable), e o argumento é **obrigatório**. A distinção legacy `RefObject` vs `MutableRefObject` desapareceu. Callback refs (`(node) => void`) cobrem casos onde o nó precisa ser observado, não armazenado.

## O que é

Em React há duas formas canônicas de armazenar valores que sobrevivem entre renders, e elas resolvem problemas distintos:

- **State (`useState`)** — valor que **dispara re-render** quando muda. É a fonte da UI: o componente pinta o valor atual de state em JSX, e mudar o valor reativa o pipeline de render. TypeScript infere o tipo do *initializer* quando ele "fala por si" (`useState(0)` → `number`); quando não fala (`null`, `[]`, `{}`), exige anotação explícita.
- **Ref (`useRef`)** — container persistente entre renders que **não dispara re-render**. É escape hatch: serve para guardar coisas que o React não precisa observar — um nó DOM para focar, um timer ID, um contador imperativo, uma instância de classe. Em React 19, o comportamento foi unificado e a tipagem ficou consistente.

Na prática, refs aparecem em duas categorias:

- **DOM ref** — você passa para JSX (`<input ref={ref}>`), e o React preenche `ref.current` com o nó DOM correspondente após o mount. Tipo canônico: `RefObject<HTMLInputElement>` (ou o `HTMLElement` correspondente à tag).
- **Mutable ref** — controle do dev. Nada de DOM: você guarda um ID de timer, um contador que não precisa pintar, uma instância de objeto pesado. O *initializer* é o valor inicial, e você muta `.current` à vontade dentro de handlers e effects.

A distinção é semântica, não sintática — em React 19 ambas usam `useRef<T>(initial)` com a mesma forma de retorno. O que muda é **quem escreve** em `.current`: o React (DOM ref) ou o seu código (mutable ref).

## Por que importa

Antes do React 19, `useRef` tinha overloads diferentes que confundiam: `useRef<HTMLDivElement>(null)` retornava `RefObject<T>` com `.current` *read-only* (porque era o React que ia escrever ali), enquanto `useRef<number>(0)` retornava `MutableRefObject<T>` com `.current` mutável. Era a mesma função, com retornos diferentes conforme você passasse `null` literal ou um valor concreto. O resultado: erros de tipo confusos quando o dev tentava mutar um ref de DOM (legítimo em alguns casos) ou esquecia que o ref mutável não permitia `null` na inicialização sem virar `MutableRefObject<T | null>`.

React 19 unificou: todo `useRef<T>(initial)` retorna `RefObject<T>` com `.current: T` mutável. O argumento agora é obrigatório — `useRef()` sem argumento dá erro de tipo, e a forma de inicializar "vazio" é passar explícito (`useRef<Timer | null>(null)` ou `useRef<number | undefined>(undefined)`). A simplificação reduz a superfície de surpresas, mas em codebases mistos (libs com `@types/react@18` ainda presentes) os dois mundos convivem — entender qual versão está em jogo evita perda de tempo decifrando erros que mudaram de forma.

Já em `useState`, a frustração canônica é `useState(null)`. O TS infere `null` literal (não `null | T`), então `setUser(novoUsuario)` falha com `Type 'User' is not assignable to type 'null'`. A correção é anotar o generic — `useState<User | null>(null)` — e essa armadilha aparece tantas vezes na prática que vira instinto. Mesma lógica para `useState([])` (infere `never[]` em strict mode) e `useState({})` (infere `{}` sem props conhecidas).

## Como funciona

### Sample 1 — `useState<T>` quando o initializer não diz o tipo

```typescript
import { useState } from 'react';

const [user, setUser] = useState<User | null>(null);
const [items, setItems] = useState<Item[]>([]);
const [form, setForm] = useState<Partial<FormData>>({});
const [cache, setCache] = useState<Map<string, User>>(new Map());

// Inferidos (não precisam de generic):
const [count, setCount] = useState(0);              // number
const [name, setName] = useState('');               // string
const [enabled, setEnabled] = useState(false);      // boolean
```

A regra é a mesma de [[02 - Inferir vs anotar - quando deixar o TS trabalhar|02]]: se o initializer fala por si, deixe inferir; se ele é uma "ausência representada como valor" (`null`, `[]`, `{}`, `new Map()`), anote o generic. O caso de `Partial<FormData>` é interessante — o tipo da `FormData` completa é o objetivo, mas o initializer começa parcial; `Partial` documenta isso no tipo.

### Sample 2 — `useRef` para DOM (React 19)

```typescript
import { useRef, useEffect } from 'react';

function AutoFocusInput() {
  const inputRef = useRef<HTMLInputElement>(null);
  // inputRef: RefObject<HTMLInputElement>
  // inputRef.current: HTMLInputElement | null

  useEffect(() => {
    inputRef.current?.focus();  // narrow com optional chaining
  }, []);

  return <input ref={inputRef} />;
}
```

O generic `<HTMLInputElement>` informa ao TS qual tipo de nó DOM esse ref vai receber. O initializer `null` é obrigatório — antes do mount, o React ainda não preencheu `ref.current`, então o tipo correto é `HTMLInputElement | null`. O optional chaining (`inputRef.current?.focus()`) faz o narrow seguro: se `current` for `null`, a chamada simplesmente não acontece.

### Sample 3 — `useRef` para mutable (React 19, exige argumento)

```typescript
import { useRef } from 'react';

function Stopwatch() {
  const counter = useRef(0);                       // RefObject<number>, .current sempre mutável
  const timerId = useRef<number | null>(null);     // RefObject<number | null>

  function start() {
    timerId.current = window.setInterval(() => {
      counter.current++;
    }, 1000);
  }

  function stop() {
    if (timerId.current !== null) {
      clearInterval(timerId.current);
      timerId.current = null;
    }
  }

  return <button onClick={start}>start</button>;
}

// useRef() sem argumento — ERRO em React 19:
// const x = useRef();
//          ~~~~~~~~ Expected 1 arguments, but got 0.

// Para ref "vazio", inicialize explícito:
// const x = useRef<Foo | undefined>(undefined);
```

O contador é incrementado dentro do callback de `setInterval`, e como ref **não dispara re-render**, esse valor é o "estado paralelo" do componente — útil quando o dev precisa de algo persistente entre renders mas que não deve causar repaint. Note que o TS aqui infere `RefObject<number>` para `counter` (initializer `0` fala por si) e `RefObject<number | null>` para `timerId` (anotado explícito porque o valor inicial é `null`). Em ambos os casos, `.current` é mutável — não há mais a divisão `RefObject` vs `MutableRefObject` da era pré-19.

### Sample 4 — Callback ref (quando precisa de lógica no mount/unmount)

```typescript
import { useCallback } from 'react';

function ObservedDiv() {
  const setRef = useCallback((node: HTMLDivElement | null) => {
    if (node) {
      // executar lógica quando o nó é mounted
      const observer = new IntersectionObserver(([entry]) => {
        console.log('intersection:', entry.isIntersecting);
      });
      observer.observe(node);
    }
    // node é null quando unmounted — momento de cleanup, se preciso
  }, []);

  return <div ref={setRef}>...</div>;
}
```

Callback ref é uma alternativa a `useRef` quando o dev precisa **observar o nó** no momento exato do mount/unmount, não apenas guardar uma referência para usar depois. O React chama o callback com o nó DOM logo após o mount e com `null` no unmount. É o pattern certo para casos de `IntersectionObserver`, `ResizeObserver`, ou qualquer setup de side effect que dependa do nó concreto. Em React 19, o callback pode opcionalmente retornar uma cleanup function — o tipo TS rejeita retorno implícito que não seja uma função (ex: `ref={node => (instance = node)}` precisa virar `ref={node => { instance = node; }}`).

### Sample 5 — `useImperativeHandle` tipado para expor API customizada

```typescript
import { useRef, useImperativeHandle, forwardRef } from 'react';

type InputHandle = {
  focus: () => void;
  clear: () => void;
};

const FancyInput = forwardRef<InputHandle, { placeholder?: string }>(
  function FancyInput({ placeholder }, ref) {
    const innerRef = useRef<HTMLInputElement>(null);

    useImperativeHandle(ref, () => ({
      focus: () => innerRef.current?.focus(),
      clear: () => {
        if (innerRef.current) innerRef.current.value = '';
      },
    }), []);

    return <input ref={innerRef} placeholder={placeholder} />;
  }
);

// Uso:
const handleRef = useRef<InputHandle>(null);
<FancyInput ref={handleRef} />;
handleRef.current?.focus();
```

`useImperativeHandle` permite que um componente filho exponha uma API customizada (não o nó DOM bruto) para o pai via ref. Os generics em `forwardRef<InputHandle, Props>` declaram: "o ref aponta para `InputHandle`, e as props têm shape `{ placeholder?: string }`". O resultado é um componente onde o pai recebe `RefObject<InputHandle>` e pode chamar `handleRef.current?.focus()` ou `handleRef.current?.clear()` sem saber nada da estrutura DOM interna.

Em React 19, `forwardRef` é **opcional**: `ref` virou prop normal em function components, então o mesmo componente pode ser escrito sem o wrapper:

```typescript
function FancyInput({
  placeholder,
  ref,
}: {
  placeholder?: string;
  ref?: React.Ref<InputHandle>;
}) {
  const innerRef = useRef<HTMLInputElement>(null);
  useImperativeHandle(ref, () => ({ /* ... */ }), []);
  return <input ref={innerRef} placeholder={placeholder} />;
}
```

A versão sem `forwardRef` é o caminho idiomático em React 19 para componentes novos — `forwardRef` continua exportado para compatibilidade, mas a documentação oficial sinaliza depreciação futura. `useImperativeHandle` permanece relevante: é o hook que define a API exposta, independente de como o `ref` chega ao componente. Aprofundamento de polimorfismo de ref em [[13 - Polymorphic components com as prop|nota 13]].

## Na prática

Pattern comum no ecossistema React: hooks customizados que retornam um ref já configurado, escondendo o setup interno do consumidor. O exemplo canônico é um `useFocusOnMount`, que abstrai o boilerplate de `useRef` + `useEffect` em um único valor:

```typescript
import { useRef, useEffect, type RefObject } from 'react';

function useFocusOnMount<T extends HTMLElement>(): RefObject<T | null> {
  const ref = useRef<T>(null);

  useEffect(() => {
    ref.current?.focus();
  }, []);

  return ref;
}

// Uso:
function LoginForm() {
  const emailRef = useFocusOnMount<HTMLInputElement>();
  return <input ref={emailRef} type="email" />;
}
```

O hook abstrai três decisões em uma assinatura: o tipo do nó (via generic `<T extends HTMLElement>`), o initializer (`null`, obrigatório em React 19), e o efeito de focar no mount. O consumidor passa apenas o tipo concreto (`<HTMLInputElement>`) e usa o ref retornado como qualquer DOM ref. Esse é o pattern observado em libs como `react-use`, `usehooks-ts` e similares: hooks pequenos que encapsulam setup de ref + effect e retornam o ref pronto para uso.

A regra prática derivada: quando o mesmo padrão de `useRef` + `useEffect` aparece em mais de dois componentes do app, vale extrair para hook customizado. O return type explícito (`RefObject<T | null>`) torna a API contratual — útil principalmente quando o hook vira parte da camada compartilhada entre features. Aprofundamento em [[07 - Tipando hooks customizados]].

## Armadilhas

- **`useRef<T>(null!)` é anti-pattern.** O `!` força o TS a tratar o initializer como não-null, mas isso transfere o ônus de checagem para todo *call site* — se algum acesso a `ref.current` acontecer antes do mount (em SSR, ou em código que executa fora de `useEffect`), o tipo mente. Prefira `useRef<T>(null)` e tratar `null` no consumer com optional chaining (`ref.current?.focus()`) ou guard explícito (`if (ref.current) ...`).

- **Em React 18 e anterior, `useRef<HTMLDivElement>(null)` retornava `RefObject` com `.current` *read-only*; em React 19 todos os refs são mutáveis.** A diferença importa em codebases mistos onde libs ainda usam `@types/react@18` em algum sub-pacote — um ref que parecia imutável passa a aceitar mutação direta, e código que dependia da imutabilidade como invariante perde essa garantia. Verifique a versão do `@types/react` na lockfile antes de assumir o comportamento.

- **Confundir DOM ref com mutable ref.** DOM ref é o que você passa para JSX (`<input ref={ref}>`); o React escreve em `.current` no mount. Mutable ref é o que você muta no seu próprio código (`counter.current++`); o React não toca em `.current`. Sintoma de confusão: passar um ref de timer ID para JSX (`<div ref={timerRef}>`), o que faz o React tentar escrever um nó DOM por cima do número e quebra o invariante esperado. Refs DOM tipam com `HTMLElement` e descendentes; refs mutáveis tipam com o que faz sentido para o valor (number, Map, instância de classe).

- **`useState(null)` infere `null` literal.** Sintoma: `setUser(novoUser)` falha com `Type 'User' is not assignable to type 'null'`. Sempre que o initializer é `null`, anote: `useState<User | null>(null)`. Mesma armadilha em `useState([])` (infere `never[]`) e `useState({})` (infere `{}` sem props), discutida em [[01 - A tripla inferência - props, state, hooks|01]] e [[02 - Inferir vs anotar - quando deixar o TS trabalhar|02]].

- **Acessar `ref.current` durante o render.** Refs não são garantidos antes do mount: em DOM refs, `ref.current` é `null` até o React preencher, e ler o valor durante o render do próprio componente que monta o nó dá `null` mesmo. A regra documentada é acessar `ref.current` apenas em `useEffect`, event handlers ou callbacks assíncronos — ou seja, em código que roda *depois* da fase de render. Sintoma de violação: `Cannot read property 'focus' of null` em runtime, mesmo o JSX parecendo correto.

## Em entrevista

> "In React 19, `useRef` was unified — it always returns `RefObject<T>` with a mutable, nullable `.current`, and the argument is required. Before React 19, there were two variants — `RefObject` for DOM refs and `MutableRefObject` for mutable values — which confused developers. Now there's one shape. For DOM, pass the ref to JSX and access `ref.current` after mount. For mutable values that survive re-renders without triggering them, treat the ref as a side container. For exposing imperative APIs to parents, `useImperativeHandle` paired with `forwardRef` is still the pattern, although `ref` is now a regular prop in function components, so `forwardRef` is increasingly optional."

**Vocabulário-chave:** *RefObject*, *callback ref*, *imperative handle*, *initial value*, *DOM node*.

**Pergunta típica de senior interview:** *"What's the difference between `useState` and `useRef`, and when do you reach for each?"* — resposta defensiva: `useState` for values that should trigger re-renders when they change — anything the UI reads from. `useRef` for values that need to persist across renders without triggering them — DOM nodes, timer IDs, imperative counters. The TypeScript signal is the same: `useState` annotation is needed when the initializer is `null`, `[]`, or `{}`; `useRef` in React 19 always returns `RefObject<T>` with a mutable `.current`, and the initializer argument is required.

## Veja também

- [[01 - A tripla inferência - props, state, hooks]]
- [[06 - Tipando event handlers]]
- [[13 - Polymorphic components com as prop]]
- [[React]] — seção "Hooks essenciais"
