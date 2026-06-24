---
title: "A tripla inferência - props, state, hooks"
created: 2026-04-26
updated: 2026-04-26
type: concept
progress: backlog
status: seedling
publish: true
tags: [typescript, react, typescript-react, frontend, mental-model, jsx, inference]
aliases:
  - Tripla inferência
  - JSX e tipos
---

# A tripla inferência - props, state, hooks

> [!abstract] TL;DR
> Em React+TS, há três fontes distintas de inferência de tipos: (1) **props** — declaradas pelo dev na assinatura do componente; (2) **state** — inferido do *initializer* ou anotado quando começa em `null`/`[]`/`{}`; (3) **hooks** — *return types* vêm da lib (React, TanStack Query, etc). Entender as três como sistemas separados elimina a maior parte dos erros confusos do iniciante.

## O que é

JSX não é mágica. Cada `<button onClick={...}>` é apenas açúcar sintático: o compilador transforma a tag no equivalente a `React.createElement('button', { onClick: ... })` (ou em uma chamada para `jsx-runtime` no transform moderno). O TypeScript sabe disso e checa cada elemento JSX contra as tipagens publicadas pela lib — não contra mágica embutida no compilador.

Para descobrir as props que `<button>` aceita, o TS consulta a interface `IntrinsicElements` no namespace JSX da lib. Em React 19, esse namespace é `React.JSX` (escopado), e a interface relevante é `React.JSX.IntrinsicElements`. O nome `JSX.IntrinsicElements` (global) ainda funciona como *fallback*, mas o handbook do TypeScript recomenda explicitamente o namespace escopado para evitar conflitos quando outras libs JSX (ex: Solid, Preact) coexistem no mesmo projeto. Cada chave dessa interface — `'button'`, `'div'`, `'svg'`, etc — define o objeto de props que o TS espera ver.

Já componentes customizados expõem suas props via assinatura da função. Não há registro central, decorador, nem coisa parecida: o TS lê `function Button(props: ButtonProps)` e sabe que `<Button ...>` deve receber um `ButtonProps`. Ponto. E hooks têm tipos que vêm das libs: `useState` tem inferência sofisticada do *initializer*; `useRef` em React 19 retorna sempre `RefObject<T>` (a distinção legacy `MutableRefObject` foi descontinuada na atualização do `@types/react` que acompanha o React 19); libs externas como TanStack Query expõem retornos genéricos que inferem do *queryFn*. Três fontes diferentes, três caminhos de inferência diferentes.

## Por que importa

A maioria das mensagens de erro confusas em React+TS vem de não saber **de onde** o compilador está tentando inferir o tipo. Quando o TS reclama `Type '{ children: Element[] }' is missing the following properties from type 'ButtonProps': variant, onClick`, o iniciante pensa que o erro está no JSX; o senior lê na hora: *"a assinatura do componente exige `variant` e `onClick`, eu esqueci de passar"*. A diferença é o mental model das três fontes — qual delas está envolvida em cada erro?

Sem esse modelo, o dev "luta com o compilador": adiciona `as any`, copia tipos do StackOverflow sem entender, evita generics. Com o modelo, ele "lê" o que o compilador diz: *isso é uma prop que faltou, isso é um initializer ambíguo, isso é o return type de um hook que precisa de generic explícito*. As próximas notas da trilha ([[02 - Inferir vs anotar - quando deixar o TS trabalhar|02]], [[05 - Tipando state e refs|05]], [[06 - Tipando event handlers|06]]) refinam cada uma das três fontes, mas todas pressupõem essa distinção.

## Como funciona

### 1. Props vêm da assinatura do componente

```typescript
type ButtonProps = {
  variant: 'primary' | 'secondary';
  onClick: () => void;
  children: React.ReactNode;
};

function Button({ variant, onClick, children }: ButtonProps) {
  return (
    <button onClick={onClick} className={variant}>
      {children}
    </button>
  );
}

// TS rejeita props inválidas:
// <Button variant="danger" onClick={() => {}}>X</Button>
//                ^^^^^^^^ Type '"danger"' is not assignable to type '"primary" | "secondary"'
```

O contrato é a assinatura. Quem chama `<Button .../>` deve satisfazer `ButtonProps`. Não há mágica — o TS lê o tipo do parâmetro e valida o JSX contra ele.

### 2. State é inferido do initializer (quando dá)

```typescript
import { useState } from 'react';

const [count, setCount] = useState(0);              // count: number (inferido do 0)
const [name, setName] = useState('');               // name: string (inferido da '')

// Quando o initializer não diz o tipo, anote:
const [user, setUser] = useState<User | null>(null);   // null sozinho não dá pra inferir
const [items, setItems] = useState<Item[]>([]);        // array vazio infere never[] — quase sempre indesejado
const [form, setForm] = useState<Partial<FormData>>({}); // {} infere objeto vazio sem props
```

A regra é simples: se o valor inicial **fala por si**, deixe inferir. Se é uma das "ausências representadas como valor" (`null`, `[]`, `{}`), anote o generic `useState<T>(...)`. Esse padrão é tão comum que vira segunda natureza — mas no início, ver `setItems(['a'])` falhar com `Type 'string' is not assignable to type 'never'` confunde até saber que o problema veio do `[]` inicial.

### 3. Return types de hooks vêm das libs

```typescript
import { useQuery } from '@tanstack/react-query';

const { data, error, isLoading } = useQuery({
  queryKey: ['user', id],
  queryFn: () => fetchUser(id), // suponha fetchUser(id): Promise<User>
});
// data: User | undefined  (inferido pelo return de queryFn)
// error: Error | null     (default da TanStack)
// isLoading: boolean      (sempre)
```

Nada aqui está embutido no React. A TanStack Query publica os tipos genéricos de `useQuery` e o TS infere o `TData` a partir do `queryFn`. O mesmo princípio vale para `useForm` (React Hook Form), `useStore` (Zustand), `useAtom` (Jotai), e qualquer hook customizado próprio: o tipo de retorno é decisão da lib, e quem consome só precisa saber **ler** o que a lib promete.

### 4. JSX intrinsic elements via React.JSX.IntrinsicElements

```typescript
// Em React 19, o namespace é React.JSX (escopado)
type ButtonNativeProps = React.JSX.IntrinsicElements['button'];
// ButtonNativeProps tem TODAS as props nativas do <button>:
// onClick, disabled, type, form, formAction, autoFocus, etc.

type MyButtonProps = ButtonNativeProps & { variant: 'primary' | 'secondary' };
// MyButton aceita TUDO que <button> aceita + variant

function MyButton({ variant, ...rest }: MyButtonProps) {
  return <button className={variant} {...rest} />;
}
```

Em projetos legados pode aparecer `JSX.IntrinsicElements['button']` (sem o `React.` na frente). Funciona ainda — o handbook descreve o namespace global como *fallback* quando o factory não expõe o JSX próprio. Em código novo, `React.JSX.IntrinsicElements` é o caminho recomendado pelo handbook do TypeScript, e o que libs sérias usam internamente. Na prática diária, `React.ComponentPropsWithoutRef<'button'>` (que envolve essa lookup) é ainda mais idiomático e está discutido em [[13 - Polymorphic components com as prop|13]].

## Na prática

Padrão observado em libs do ecossistema (Radix UI, Mantine, MUI, shadcn/ui): props customizadas estendem `React.ComponentPropsWithoutRef<'button'>` (ou similar para `'a'`, `'input'`, etc) para herdar todos os atributos HTML nativos sem ter que listá-los um a um. O resultado é um `<MyButton>` que aceita `aria-label`, `disabled`, `type`, `form`, e qualquer outro atributo válido em `<button>`, mais as props customizadas (`variant`, `loading`, `leftIcon`...).

Esse pattern é convenção do ecossistema porque resolve um problema real: redeclarar manualmente todos os atributos HTML é tedioso, propenso a esquecimentos (`onPointerEnter`, `formNoValidate`, etc) e fica desatualizado quando o HTML evolui. Deixar o TS herdar de `IntrinsicElements` mantém o componente alinhado com as definições oficiais do `@types/react`. A [[13 - Polymorphic components com as prop|nota 13]] aprofunda esse pattern, incluindo a versão genérica `<Box as="a" .../>` que muda o tipo das props aceitas conforme o `as`.

## Armadilhas

- **`useState(null)` infere `null` literal** — não `null | T`. O compilador não tem como adivinhar qual o tipo eventual; sem anotação, qualquer `setUser(novoUsuario)` vai falhar com `Type 'User' is not assignable to type 'null'`. Anote sempre: `useState<User | null>(null)`.

- **`useRef` em React 19 mudou.** Toda chamada de `useRef` retorna `RefObject<T>` agora — `MutableRefObject` deixou de ser o retorno de `useRef` (o tipo ainda é exportado de `@types/react@19` para retrocompatibilidade, mas não aparece nos overloads do hook). A propriedade `.current` é sempre mutável, mesmo quando inicializada com `null`. Em `@types/react` antigos, `useRef<HTMLDivElement>(null)` retornava `RefObject<HTMLDivElement>` com `.current` *read-only*, enquanto `useRef<number>(0)` retornava `MutableRefObject<number>` com `.current` mutável — uma distinção que confundia. Em React 19, ambos retornam `RefObject` mutável e `useRef` agora **exige** um argumento explícito (`useRef()` sem argumento dá erro de tipo; passe `useRef(undefined)` se for esse o caso). [[05 - Tipando state e refs|Nota 05]] cobre as variantes em detalhe.

- **`<Component<T> />` em arquivo `.tsx` precisa de truque sintático.** O parser de JSX confunde `<T>` com tag de abertura. As soluções idiomáticas: `<Component<T,> />` (vírgula extra no generic) ou `<Component<T extends unknown> />` (constraint que esclarece que é generic, não JSX). Em `.ts` puro o problema não aparece — só em arquivos onde JSX e generics convivem. [[12 - Generic components|Nota 12]] aprofunda.

## Em entrevista

> "In React with TypeScript, there are three sources of type inference. Props come from the component's signature — I declare them and TS validates the JSX against them. State is inferred from `useState`'s initial value when it's a primitive, but I have to annotate when starting with `null` or empty arrays. Hooks return types come from the library — `useQuery` from TanStack, for example, infers the data type from my `queryFn` return. Knowing these three sources separately makes confusing error messages readable instead of intimidating."

**Vocabulário-chave:** *intrinsic elements*, *type inference*, *initial value*, *return type*, *generic parameter*.

**Pergunta típica de senior interview:** *"How does TypeScript know what props `<button>` accepts?"* — resposta defensiva: via `React.JSX.IntrinsicElements['button']`, the interface React publishes for native HTML elements. Modern code uses `React.ComponentPropsWithoutRef<'button'>` as a more ergonomic helper that resolves to the same thing.

## Veja também

- [[02 - Inferir vs anotar - quando deixar o TS trabalhar]] — a regra prática derivada deste mental model
- [[05 - Tipando state e refs]] — aprofundamento da fonte 2 (state) e refs em React 19
- [[12 - Generic components]] — quando os componentes viram fontes inferidas pelo consumidor
- [[13 - Polymorphic components com as prop]] — `ComponentPropsWithoutRef` aplicado a fundo
- [[03-Dominios/Tecnologia/TypeScript/index|TypeScript]] — seções "Generics" e "TypeScript em frontend (React)"
- [[React]] — seção "Componentes e JSX"
