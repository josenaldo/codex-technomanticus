---
title: "Tipando hooks customizados"
created: 2026-04-26
updated: 2026-04-26
type: concept
status: seedling
publish: true
tags: [typescript, react, typescript-react, frontend, hooks, custom-hooks, generics, overloads]
aliases:
  - Custom hooks tipados
  - Hook return types
---

# Tipando hooks customizados

> [!abstract] TL;DR
> Hooks customizados retornam tupla `as const` (não objeto, na maioria dos casos) para preservar nomes posicionais. Generics inferidos do parâmetro permitem `useFetch<User>('/api/me')`. Overloads cobrem assinaturas múltiplas (ex: `useStorage(key)` vs `useStorage(key, default)`). Discriminated union no return cobre estados (loading/data/error).

## O que é

Um hook customizado é uma função que começa com `use` e compõe hooks built-in para encapsular lógica reutilizável. Em TypeScript, três decisões definem a qualidade da API que o hook expõe — e cada uma tem uma resposta idiomática diferente conforme o caso:

1. **Forma do retorno: tupla, objeto ou discriminated union.** Tupla com `as const` (`[value, setValue] as const`) preserva nomes posicionais e funciona bem para hooks pequenos com 2-3 valores; o consumer renomeia no destructuring. Objeto com chaves nomeadas (`{ data, error, isLoading }`) escala melhor para retornos com 4+ valores e quando ordem não tem significado intrínseco. Discriminated union (`{ status: 'idle' } | { status: 'success'; data: T } | ...`) é o nível mais preciso — modela estados mutuamente exclusivos e força exhaustiveness no consumer.

2. **Generics vs anotação concreta.** Quando o tipo do retorno **depende** de um parâmetro de entrada — `useFetch<T>(url)` retornando `T | undefined`, `useStorage<T>(key)` lendo/escrevendo `T` em `localStorage` — o hook recebe um type parameter e o consumer especializa no call site. Quando o tipo é fixo (`useToggle` retorna sempre `[boolean, () => void]`), generic é desnecessário.

3. **Overloads para múltiplas assinaturas.** Quando a mesma função é chamada de formas diferentes com **tipos de retorno diferentes** dependendo dos argumentos — `useStorage<T>(key)` retornando `[T | null, ...]` vs `useStorage<T>(key, default)` retornando `[T, ...]` — overloads de função (assinaturas múltiplas + uma implementação) descrevem isso com precisão. O consumer recebe o tipo certo para cada chamada sem precisar fazer narrow manual.

A regra prática que guia as três decisões: **o tipo do retorno é o contrato público do hook**. Quanto mais preciso o tipo, menos o consumer precisa lidar com casos impossíveis (`data` populado durante `loading`, valor `null` quando havia default explícito).

## Por que importa

Tupla com `as const` é o pattern certo para hooks pequenos por uma razão semântica: o consumer **renomeia** no destructuring (`const [isOpen, toggleOpen] = useToggle()`), e o nome local fica natural ao caso de uso. Sem `as const`, o TS infere `(boolean | (() => void))[]` — array genérico — e a posição é apagada: `[0]` e `[1]` viram `boolean | (() => void)`, exigindo cast em todo uso. Com `as const`, o tipo vira `readonly [boolean, () => void]`, e cada posição mantém seu tipo concreto. A asserção é o que torna o pattern de tupla utilizável.

Objetos com chaves nomeadas, por outro lado, são melhores quando há muitas propriedades ou quando ordem não tem significado: TanStack Query retorna `{ data, error, isLoading, isFetching, isPending, refetch, ... }` — uma tupla com 7+ elementos seria ilegível, e o consumer não precisaria renomear cada um. A chave nomeada é a documentação.

Discriminated union elimina **estados inválidos** que ficariam representáveis com booleans separados. Três `useState` paralelos (`isLoading: boolean`, `data: T | undefined`, `error: Error | null`) permitem combinações que não fazem sentido — `isLoading: true` com `data` populado, `error` e `data` ambos não-null. Modelando como discriminated union, esses casos simplesmente **não existem no tipo**: cada variant tem só os campos que pertencem àquele estado, e o switch no render força o consumer a tratar cada caso explicitamente. O TS faz o narrow automático: dentro do `case 'success'`, `state.data` é `T` (não `T | undefined`).

Generics fazem o hook reutilizável sem perder precisão. `useFetch<T>(url)` é a mesma função para qualquer payload, mas o consumer recebe `data: User | undefined` ou `data: Order | undefined` conforme o `T` passado — sem cast, sem `unknown`, sem `any`. Anotar o retorno como `unknown` e exigir cast em cada chamada é a alternativa pobre: o consumer faz o trabalho que o hook deveria fazer.

Overloads resolvem o caso onde a mesma função muda de tipo conforme os argumentos. Sem overloads, `useStorage<T>(key, default?)` retornaria `[T | null, ...]` mesmo quando o default está presente — e o consumer faria narrow manual ou aceitaria o `null` "extra" no tipo. Com overloads, cada call signature tem return type próprio: `useStorage('user')` é `[User | null, ...]`; `useStorage('theme', 'light')` é `['light' | 'dark', ...]`. O hook fica mais inteligente; o consumer não precisa pensar.

## Como funciona

### Sample 1 — `useToggle` retornando tupla `as const`

```typescript
import { useState, useCallback } from 'react';

function useToggle(initial = false) {
  const [on, setOn] = useState(initial);
  const toggle = useCallback(() => setOn(s => !s), []);
  return [on, toggle] as const;
}

// Uso:
const [isOpen, toggleOpen] = useToggle();
// isOpen: boolean
// toggleOpen: () => void

const [isDark, toggleDark] = useToggle(true);
// nomeia conforme o caso de uso, sem precisar criar variantes do hook
```

A combinação `tupla + as const + destructuring` é o ergonomic sweet spot para hooks pequenos. O consumer escolhe os nomes locais, e o TS preserva a posição: `isOpen` é o `boolean` da posição 0, `toggleOpen` é a função da posição 1. Sem `as const`, o tipo retornado seria array misto e o destructuring perderia precisão (próximo sample mostra o contraste).

### Sample 2 — Por que `as const` é necessário

```typescript
// Sem as const — array misto, posições apagadas
function useToggleBroken(initial = false) {
  const [on, setOn] = useState(initial);
  return [on, () => setOn(s => !s)];
}
// Tipo inferido: (boolean | (() => void))[]
// Destructuring:
const [isOpen, toggleOpen] = useToggleBroken();
// isOpen:    boolean | (() => void)  ← perdeu o tipo posicional
// toggleOpen: boolean | (() => void)  ← idem; chamada gera erro

// toggleOpen();  // ERRO: Not all constituents of type 'boolean | (() => void)' are callable.

// Com as const — tupla readonly, posições preservadas
function useToggleFixed(initial = false) {
  const [on, setOn] = useState(initial);
  return [on, () => setOn(s => !s)] as const;
}
// Tipo: readonly [boolean, () => void]
const [isOpen2, toggleOpen2] = useToggleFixed();
// isOpen2:    boolean         ← posição 0 preservada
// toggleOpen2: () => void     ← posição 1 preservada
toggleOpen2();  // ok
```

Esse contraste é a justificativa central do pattern. A inferência default do TS para `[a, b]` é "array do *best common type* de a e b" — quando `a` e `b` têm tipos diferentes, o resultado é union, e o array perde semântica posicional. `as const` instrui o compilador a tratar a expressão como tupla literal, fixando cada posição no seu tipo exato. Sem essa asserção, hooks que retornam array de elementos heterogêneos são essencialmente inutilizáveis em modo strict.

### Sample 3 — `useFetch<T>` com generic explícito

```typescript
import { useState, useEffect } from 'react';

function useFetch<T>(url: string): {
  data: T | undefined;
  error: Error | null;
  isLoading: boolean;
} {
  const [data, setData] = useState<T | undefined>(undefined);
  const [error, setError] = useState<Error | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    setIsLoading(true);
    fetch(url)
      .then(r => r.json())
      .then((d: T) => {
        if (!cancelled) {
          setData(d);
          setIsLoading(false);
        }
      })
      .catch((e: Error) => {
        if (!cancelled) {
          setError(e);
          setIsLoading(false);
        }
      });
    return () => { cancelled = true; };
  }, [url]);

  return { data, error, isLoading };
}

// Uso — generic explícito no call site:
type User = { id: string; name: string };
const { data, error, isLoading } = useFetch<User>('/api/me');
// data: User | undefined
// error: Error | null
// isLoading: boolean
```

`<T>` é o type parameter declarado pelo hook; quem chama escolhe o `T` concreto (`<User>`, `<Order>`, `<Product[]>`). O retorno é objeto porque três propriedades nomeadas escalam melhor que tupla — e a ordem `data | error | isLoading` não tem significado posicional. Note que o return type **é anotado** explícito: o contrato fica documentado na assinatura, e refatorar o corpo do hook sem mexer na assinatura não muda a API pública (princípio de [[02 - Inferir vs anotar - quando deixar o TS trabalhar]]).

### Sample 4 — `useStorage` com overloads

```typescript
import { useState } from 'react';

// Overloads — duas assinaturas públicas
function useStorage<T>(key: string): readonly [T | null, (value: T) => void];
function useStorage<T>(key: string, defaultValue: T): readonly [T, (value: T) => void];

// Implementação — assinatura compatível com todos os overloads
function useStorage<T>(key: string, defaultValue?: T) {
  const [value, setValue] = useState<T | null>(() => {
    const stored = localStorage.getItem(key);
    if (stored !== null) return JSON.parse(stored) as T;
    return defaultValue ?? null;
  });

  const setStoredValue = (v: T) => {
    setValue(v);
    localStorage.setItem(key, JSON.stringify(v));
  };

  return [value, setStoredValue] as const;
}

// Uso 1: sem default — pode retornar null
const [user] = useStorage<User>('user');
// user: User | null

// Uso 2: com default — sempre retorna T
const [theme] = useStorage<'light' | 'dark'>('theme', 'light');
// theme: 'light' | 'dark'  ← sem null, porque o default cobre o caso vazio
```

As duas linhas de `function useStorage<T>(...)` no topo são as **assinaturas públicas** — é o que o TS expõe ao consumer. A terceira `function useStorage<T>(...)` é a **implementação**, e seu tipo precisa ser compatível com as duas assinaturas (parâmetros opcionais cobrindo a versão sem `defaultValue`, retorno cobrindo os dois shapes via `as const`). O consumer só vê as duas assinaturas listadas; a implementação não aparece no autocomplete. Esse pattern é canônico em libs como TanStack Query (`useQuery` tem múltiplos overloads para cobrir variações de `enabled`, `select`, etc.).

### Sample 5 — Hook que retorna discriminated union (state machine)

```typescript
import { useState, useEffect } from 'react';

type FetchState<T> =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: Error };

declare function fetchUser(id: string): Promise<User>;

function useFetchUser(id: string): FetchState<User> {
  const [state, setState] = useState<FetchState<User>>({ status: 'idle' });

  useEffect(() => {
    let cancelled = false;
    setState({ status: 'loading' });
    fetchUser(id)
      .then(data => { if (!cancelled) setState({ status: 'success', data }); })
      .catch((error: Error) => { if (!cancelled) setState({ status: 'error', error }); });
    return () => { cancelled = true; };
  }, [id]);

  return state;
}

// Uso com switch exhaustivo — força cobertura de todos os estados:
function UserView({ id }: { id: string }) {
  const state = useFetchUser(id);
  switch (state.status) {
    case 'idle':    return <p>Aguardando...</p>;
    case 'loading': return <Spinner />;
    case 'success': return <UserCard user={state.data} />;        // narrowed: data: User
    case 'error':   return <ErrorMessage error={state.error} />;  // narrowed: error: Error
  }
}
```

Cada variant da union tem **só os campos que pertencem àquele estado** — `data` aparece apenas em `'success'`, `error` apenas em `'error'`. O TS faz narrow automático dentro de cada `case`: depois de `case 'success':`, `state.data` é `User` (sem `undefined`); depois de `case 'error':`, `state.error` é `Error` (sem `null`). Estados inválidos como "loading com data populado" não existem no tipo — não há como construí-los. Comparado com três `useState` separados (`isLoading`, `data`, `error`), a expressividade ganha é estrutural: o tipo elimina combinações sem sentido em vez de delegar a checagem ao runtime. Aprofundamento em [[09 - Tipando reducers e state machines]].

## Na prática

Pattern observado no ecossistema React:

- **Libs grandes com retornos ricos** (TanStack Query, useSWR) preferem **objeto com `data`/`error`/`isLoading`** porque há muitas propriedades e ordem não importa. `useQuery` retorna 10+ chaves; tupla seria ilegível, e o consumer não renomearia 10 nomes posicionais. A chave nomeada serve de documentação no call site.

- **Hooks pequenos com 2-3 valores** (useToggle, useDisclosure, useCounter, useDebounce) preferem **tupla `as const`** porque destructuring fica natural. O consumer renomeia conforme o caso (`const [isOpen, toggleOpen] = useToggle()` em uma feature, `const [isDark, toggleDark] = useToggle()` em outra) — a posição é o contrato, o nome é local.

- **Hooks que representam estados mutuamente exclusivos** (data fetching, async actions, multi-step flows) preferem **discriminated union**. O ganho é eliminar estados inválidos no tipo e forçar exhaustiveness no consumer — útil principalmente quando o render branches por estado.

- **Hooks parametrizados em tipo** (useFetch, useStorage, useLocalState) usam **generics** porque o retorno depende do payload. Sem generic, o consumer faria cast manual em cada uso.

A regra prática derivada: comece simples (tupla), promova para objeto quando passar de 3 valores, promova para discriminated union quando o estado tem variants mutuamente exclusivas. Aprofundamento de discriminated unions em [[09 - Tipando reducers e state machines]].

## Armadilhas

- **Esquecer `as const` em retorno de tupla.** Sintoma: destructuring perde tipos posicionais, e o TS aceita ou rejeita usos errados conforme o *best common type* dos elementos. `return [value, setValue]` infere `(T | typeof setValue)[]`; `return [value, setValue] as const` infere `readonly [T, typeof setValue]`. A asserção é obrigatória sempre que o retorno é tupla heterogênea.

- **Tentar inferir generic a partir do retorno.** TS só infere generics a partir de **argumentos** — se o type parameter aparece só no return type (`function useStuff<T>(): T`), o consumer **precisa** passar explícito (`useStuff<User>()`). Sem o explícito, `T` vira `unknown`. Isso é desenho da inferência, não bug: o compilador infere "para trás" de argumentos para tipos, nunca de uso futuro do retorno para o tipo.

- **Over-engineering com discriminated union em hooks simples.** `useToggle` não precisa de variants `idle | on | off | toggling` — booleano resolve. Discriminated union faz sentido quando há **3+ estados mutuamente exclusivos** que carregam dados diferentes (loading sem data, success com data, error com error). Para "ligado/desligado" puro, o overhead de tipo + switch é ruído.

- **Nomear chaves do objeto inconsistentemente entre hooks do mesmo app.** Se um hook expõe `{ isLoading }`, outro expõe `{ loading }`, e um terceiro expõe `{ pending }`, o consumer perde tempo lembrando qual é qual. Convencione um vocabulário (TanStack Query usa `isLoading` / `isPending` / `isFetching` com semântica precisa; useSWR usa `isLoading` / `isValidating`) e siga em todos os hooks do app. Consistência de nomes nas chaves é parte do contrato.

- **Misturar return types parcialmente anotados.** Anotar metade do retorno (`function useThing(): { data: User } & ReturnType<...>`) e deixar o resto inferir cria contratos frágeis: alterar a implementação muda parte do tipo público sem aviso. Para hooks que viram parte da camada compartilhada, anote o return type **inteiro** explícito; para hooks privados de uma feature, deixe inferir tudo.

## Em entrevista

> "When designing a custom hook, I think about three decisions. First, what shape should the return be? Tuples with `as const` are great for small hooks like `useToggle` because destructuring keeps the names where I want them. Objects are better when there are many properties — TanStack Query returns `{ data, error, isLoading }` because positional ordering wouldn't scale. Discriminated unions are the most precise — they encode mutually exclusive states like idle/loading/success/error and force exhaustive handling at the call site. Second, do I use generics? Yes, when the hook is parameterized — `useFetch<User>` infers `data: User | undefined`. Third, do I need overloads? When the call signature changes meaningfully (with vs. without a default value, for example), overloads give precise return types per signature."

**Vocabulário-chave:** *as const tuple*, *function overload*, *discriminated union*, *generic constraint*, *return type contract*.

**Pergunta típica de senior interview:** *"Why `as const` in a hook return tuple?"* — resposta defensiva: without it, TypeScript infers the array as the union of all element types — `(boolean | (() => void))[]` — and destructuring loses positional types. With `as const`, the return becomes a `readonly` tuple — `readonly [boolean, () => void]` — preserving the type at each index. It's the assertion that makes the tuple-return pattern usable; without it, the consumer has to cast.

## Veja também

- [[02 - Inferir vs anotar - quando deixar o TS trabalhar]] — quando anotar return type de hook
- [[05 - Tipando state e refs]] — `useState`/`useRef` que esses hooks compõem por dentro
- [[09 - Tipando reducers e state machines]] — discriminated unions em ação
- [[12 - Generic components]] — generics em React além de hooks
- [[TypeScript]] — seções "Generics", "Discriminated unions"
