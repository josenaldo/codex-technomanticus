---
title: "Tipando reducers e state machines"
created: 2026-04-26
updated: 2026-04-26
type: concept
status: seedling
publish: true
tags: [typescript, react, typescript-react, frontend, useReducer, discriminated-unions, state-machines]
aliases:
  - useReducer tipado
  - Discriminated unions em React
---

# Tipando reducers e state machines

> [!abstract] TL;DR
> Actions tipadas como discriminated union pelo `type`. Reducer com `switch` força exhaustiveness via `never` no default. State machine completa (idle/loading/success/error) substitui múltiplos `useState` e força narrowing no render. Comparado com 3 booleans paralelos, a discriminated union elimina **estados inválidos** no tipo.

## O que é

Uma **discriminated union** (também chamada de *tagged union* ou *algebraic data type*) é uma união de tipos onde cada variant carrega uma propriedade comum — o **discriminator** — cujo tipo é um literal distinto em cada membro. Essa propriedade tem nome convencional (`type`, `kind`, `status`, `tag`), mas o que importa é a propriedade técnica: como cada variant declara um valor literal diferente para o mesmo campo, o TypeScript consegue **narrow** automaticamente o tipo dentro de blocos `if`, `switch` e ternários que checam esse discriminator.

```typescript
type Shape =
  | { kind: 'circle'; radius: number }
  | { kind: 'square'; side: number };

function area(s: Shape): number {
  if (s.kind === 'circle') {
    return Math.PI * s.radius ** 2;  // s narrowed para { kind: 'circle'; radius: number }
  }
  return s.side ** 2;  // s narrowed para { kind: 'square'; side: number }
}
```

`useReducer` se beneficia diretamente desse mecanismo. O reducer recebe `(state, action)` e retorna o próximo state; quando `action` é uma discriminated union pelo `type`, um `switch (action.type)` narroweia o `action` em cada `case` para o variant correspondente, e o TS reconhece quais payloads estão disponíveis em cada ramo. O mesmo pattern se aplica ao **state**: ao modelar uma state machine como discriminated union (`{ status: 'idle' } | { status: 'success'; data: T } | ...`), o consumer precisa checar o `status` antes de acessar campos específicos, e o TS força essa checagem em compile time.

A relação com `useReducer` da React 19 é direta. A API é estável desde os primeiros hooks: `const [state, dispatch] = useReducer(reducer, initialArg, init?)`. O `dispatch` aceita "qualquer tipo" segundo a documentação, mas a convenção idiomática — reforçada por Redux, Redux Toolkit e XState — é objetos com a propriedade `type`. Em TypeScript, o ganho é gigante: tipar `Action` como discriminated union dá ao consumer autocomplete para os `type` válidos, autocomplete para os payloads específicos de cada `type`, e erro em compile time se um payload errado é passado.

## Por que importa

A pergunta não é "discriminated union vs. nada" — é "discriminated union vs. modelar com booleans/flags paralelos". E a diferença qualitativa é que **booleans paralelos permitem estados inválidos**, enquanto discriminated unions os eliminam no tipo.

Considere um componente que faz fetch de um usuário. Modelado com 3 `useState` separados — `data`, `error`, `isLoading` — o tipo cartesiano dos estados possíveis é o produto: `(User | undefined) × (Error | null) × boolean = 8 combinações`. Dessas, **apenas 4 são válidas** no domínio do problema: aguardando início, carregando, sucesso, erro. As outras 4 são representáveis pelo tipo mas não fazem sentido no domínio:

- `isLoading: true` com `data: User` populado — "estou carregando, mas já tenho os dados".
- `data: User` com `error: Error` — "tive sucesso e erro ao mesmo tempo".
- `isLoading: true` com `error: Error` — "estou carregando depois de já ter falhado".
- Tudo `null/false/undefined` — indistinguível de "ainda não comecei" e "já terminei sem dados".

Cada um desses estados é uma bomba-relógio: nenhum compilador acusa, mas a UI vai apresentar combinações sem sentido se um setter for esquecido. A solução clássica é uma cadeia de `if`s no render que tenta decidir o que mostrar quando — `if (error) return <Error />; if (isLoading) return <Spinner />; if (data) return <Data />`. A ordem desses ifs vira regra de negócio implícita: se um setter de `isLoading: false` for esquecido após erro, o spinner roda para sempre.

A discriminated union elimina essas combinações no tipo. Modelando como `{ status: 'idle' } | { status: 'loading' } | { status: 'success'; data: User } | { status: 'error'; error: Error }`, o estado total tem **exatamente 4 valores possíveis**, cada um carregando apenas os campos que fazem sentido. Não existe `{ status: 'loading'; data: User }` porque o tipo não declara essa variante. O setter passa a ser uma transição de estado completa, não um conjunto de flags individuais que podem ficar dessincronizadas.

O segundo ganho é o **exhaustiveness check**. Um `switch (state.status)` sem default `never` aceita silenciosamente um novo variant adicionado depois. Com `default: { const _: never = state; ... }`, qualquer adição de variant quebra todos os switches que tratam o tipo até serem atualizados. Isso é exatamente o que se espera de refatoração tipada: o compilador aponta cada lugar que precisa receber o novo case, em vez de deixar o caso silenciosamente cair no default em runtime.

## Como funciona

### Sample 1 — Counter reducer com discriminated union

```typescript
import { useReducer } from 'react';

type Action =
  | { type: 'inc' }
  | { type: 'dec' }
  | { type: 'set'; value: number }
  | { type: 'reset' };

function reducer(state: number, action: Action): number {
  switch (action.type) {
    case 'inc':
      return state + 1;
    case 'dec':
      return state - 1;
    case 'set':
      return action.value;  // narrowed: action é { type: 'set'; value: number }
    case 'reset':
      return 0;
    default: {
      const _exhaustive: never = action;
      return state;
    }
  }
}

function Counter() {
  const [count, dispatch] = useReducer(reducer, 0);
  return (
    <div>
      <button onClick={() => dispatch({ type: 'dec' })}>-</button>
      <span>{count}</span>
      <button onClick={() => dispatch({ type: 'inc' })}>+</button>
      <button onClick={() => dispatch({ type: 'set', value: 100 })}>Set 100</button>
    </div>
  );
}
```

Pontos a notar:

- `dispatch({ type: 'set' })` sem `value` é erro em compile time — o TS exige o payload do variant `'set'`.
- `dispatch({ type: 'inc', value: 5 })` é erro — o variant `'inc'` não declara `value`, e excess property check pega.
- Dentro do `case 'set'`, `action.value` é `number` sem narrowing manual — o `switch` no discriminator fez o trabalho.

### Sample 2 — Exhaustiveness check com `never`

```typescript
type Action = { type: 'a' } | { type: 'b' } | { type: 'c' };

function reducer(state: number, action: Action): number {
  switch (action.type) {
    case 'a':
      return state + 1;
    case 'b':
      return state - 1;
    // Esqueci 'c' — o compilador detecta:
    default: {
      const _: never = action;
      // ERRO: Type '{ type: "c" }' is not assignable to type 'never'.
      return state;
    }
  }
}
```

A asserção `const _: never = action` só compila se `action` já tiver sido narrowed para `never` — ou seja, se todos os variants foram tratados antes. Se um case faltar, o variant restante "vaza" para o default, e a atribuição falha.

O ganho aparece em refator. Quando alguém adiciona um novo `{ type: 'd' }` ao tipo `Action`, **todos** os reducers que usam exhaustiveness check quebram em compile time, forçando atualização. É refactoring seguro: a ferramenta aponta cada call site que precisa de atenção, em vez de deixar o novo case cair silenciosamente no default em runtime.

### Sample 3 — State machine completa (idle/loading/success/error)

```typescript
import { useReducer, useEffect } from 'react';

type FetchState<T> =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: Error };

type FetchAction<T> =
  | { type: 'start' }
  | { type: 'resolve'; data: T }
  | { type: 'reject'; error: Error }
  | { type: 'reset' };

function fetchReducer<T>(
  state: FetchState<T>,
  action: FetchAction<T>,
): FetchState<T> {
  switch (action.type) {
    case 'start':
      return { status: 'loading' };
    case 'resolve':
      return { status: 'success', data: action.data };
    case 'reject':
      return { status: 'error', error: action.error };
    case 'reset':
      return { status: 'idle' };
  }
}

function UserView({ id }: { id: string }) {
  const [state, dispatch] = useReducer(
    fetchReducer<User>,
    { status: 'idle' } as FetchState<User>,
  );

  useEffect(() => {
    dispatch({ type: 'start' });
    fetchUser(id)
      .then((data) => dispatch({ type: 'resolve', data }))
      .catch((error: Error) => dispatch({ type: 'reject', error }));
  }, [id]);

  switch (state.status) {
    case 'idle':
      return <p>Aguardando...</p>;
    case 'loading':
      return <Spinner />;
    case 'success':
      return <UserCard user={state.data} />;       // narrowed: state.data: User
    case 'error':
      return <ErrorMessage error={state.error} />;  // narrowed: state.error: Error
  }
}
```

Pontos a notar:

- `state.data` só é acessível dentro de `case 'success'`. Em `case 'loading'`, tentar `state.data` é erro — o variant `'loading'` não declara esse campo.
- O `switch` retorna em todos os cases, então o TS infere que o componente sempre retorna um `JSX.Element`. Se um case for esquecido, o tipo de retorno vira `JSX.Element | undefined` (ou erro, dependendo do `noImplicitReturns`), denunciando o gap.
- Não há `default: never` aqui porque os 4 cases cobrem o discriminator inteiro; o TS reconhece a cobertura total. Em códigos em evolução, manter o `default: never` é mais seguro.

### Sample 4 — Comparação: 3 useState vs discriminated union

```typescript
// Pobre — 3 booleans paralelos permitem estados inválidos
function UserViewBad({ id }: { id: string }) {
  const [data, setData] = useState<User | undefined>(undefined);
  const [error, setError] = useState<Error | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  // Estados representáveis no tipo mas inválidos no domínio:
  // - isLoading: true, data: User       (loading com dados antigos)
  // - data: User, error: Error          (sucesso e erro simultâneos)
  // - isLoading: true, error: Error     (loading e erro simultâneos)
  // - tudo undefined/null/false         (idle indistinguível de unknown)
  // O TS aceita todas. O bug aparece em runtime quando um setter é esquecido.

  useEffect(() => {
    setIsLoading(true);
    fetchUser(id)
      .then((d) => {
        setData(d);
        setIsLoading(false);
        // Se eu esquecer setError(null), erro antigo persiste com data novo
      })
      .catch((e: Error) => {
        setError(e);
        setIsLoading(false);
        // Se eu esquecer setData(undefined), data antigo persiste com erro
      });
  }, [id]);

  // Ordem dos ifs vira regra de negócio implícita
  if (error) return <ErrorMessage error={error} />;
  if (isLoading) return <Spinner />;
  if (data) return <UserCard user={data} />;
  return null;  // estado "idle" indistinguível de "terminou sem dados"
}

// Rico — discriminated union elimina inválidos no tipo
function UserViewGood({ id }: { id: string }) {
  const [state, dispatch] = useReducer(
    fetchReducer<User>,
    { status: 'idle' } as FetchState<User>,
  );

  // Apenas 4 estados representáveis: idle | loading | success(data) | error(error)
  // Não existe `{ status: 'loading'; data: User }` — o tipo não permite.
  // Cada transição é uma action: dispatch({ type: 'start' }) zera tudo de uma vez.

  useEffect(() => {
    dispatch({ type: 'start' });
    fetchUser(id)
      .then((data) => dispatch({ type: 'resolve', data }))
      .catch((error: Error) => dispatch({ type: 'reject', error }));
  }, [id]);

  // Render é exhaustive switch — cada case sabe exatamente o que tem disponível
  switch (state.status) {
    case 'idle':    return <p>Aguardando...</p>;
    case 'loading': return <Spinner />;
    case 'success': return <UserCard user={state.data} />;
    case 'error':   return <ErrorMessage error={state.error} />;
  }
}
```

A diferença não é estilística. A versão `Bad` exige disciplina manual para manter os 3 setters consistentes; cada esquecimento vira bug. A versão `Good` torna estados inválidos **inexpressáveis** — não há como construir `{ status: 'loading'; data: User }` porque o tipo não declara essa variante. Bug eliminado por design, não por revisão de código.

## Na prática

Três bibliotecas amplamente usadas em 2026 codificam exatamente esse pattern:

- **TanStack Query** expõe um `status` discriminado (`'pending' | 'success' | 'error'`) no resultado de `useQuery`, com narrowing automático: dentro de `if (query.status === 'success')`, `query.data` é não-undefined. O nome `status` (em vez de `type`) é convenção da lib, mas o mecanismo é o mesmo. Consumers que tratam estados via `query.isLoading`/`query.isError`/`query.isSuccess` (booleans derivados) abrem mão dessa garantia e voltam ao mundo dos booleans paralelos.

- **Redux Toolkit** mantém a tradição Redux de actions discriminadas pelo `type`, mas gera os action creators e os tipos automaticamente via `createSlice`. O reducer interno usa Immer para mutação imperativa, mas a discriminated union ainda é o que faz o TypeScript inferir o payload de cada action no `extraReducers`/`builder.addCase`.

- **XState** leva o pattern ao extremo: state machines explícitas onde cada estado é um nó nomeado, transições são tipadas pelo evento, e o tipo de `state.context` muda conforme `state.matches('loading')` etc. O ganho é o mesmo do `useReducer + discriminated union`, com a diferença de que XState modela a máquina como dado declarativo e oferece visualização, hierarquia e *guards* tipados.

O denominador comum entre as três: **estado é uma união discriminada, não um produto de booleans**. A propriedade discriminante muda de nome (`status` em RQ, `type` em RTK actions, nome do estado em XState), mas o mecanismo é o mesmo — uma propriedade literal que o TS pode narrow.

## Armadilhas

- **Esquecer `default: { const _: never = action }`.** Sem o exhaustiveness check, novos variants adicionados ao tipo `Action` (ou ao `State`) caem silenciosamente no default e a UI ignora a transição. O bug aparece em runtime, sem aviso do compilador. Em códigos em evolução, esse default é o que diferencia "refator seguro" de "refator com regressões silenciosas".

- **Usar `string` em vez de literal no discriminator.** `type Action = { type: string; ... }` parece equivalente, mas não narroweia. O TS não consegue distinguir `case 'inc'` de `case 'dec'` quando o tipo é `string`, e o payload específico de cada variant não fica disponível em cada `case`. A discriminação precisa de **literal types** (`'inc' | 'dec' | 'set'`), não de `string` aberto. Se o discriminator vem de uma fonte externa (ex.: API), narrow no boundary com Zod ou type guard antes de entrar no reducer.

- **Modelar com booleans paralelos quando os estados são mutuamente exclusivos.** Se `isLoading` e `isError` nunca devem ser ambos `true`, eles não são variáveis independentes — são rótulos de um mesmo estado. Modelar como `status: 'loading' | 'error' | ...` evita o bug onde os dois flags ficam dessincronizados. A regra prática: se documentar o componente exige uma frase como "isLoading e isError nunca são true ao mesmo tempo", isso é um sinal de que o estado quer ser uma discriminated union.

- **Esquecer cobertura no switch sem `default: never`.** Sem o exhaustiveness check, um `switch (state.status)` que esquece o case `'error'` compila tranquilamente — o TS só denuncia se o tipo de retorno do bloco não cobrir todos os caminhos (ex.: função declarada `(): JSX.Element` em modo `noImplicitReturns`). Adicionar o `default: never` torna o esquecimento explícito em vez de depender de configurações tangentes.

- **Anotar o initial state sem cobrir todos os variants do tipo.** `useReducer(reducer, { status: 'idle' })` infere o initial state como `{ status: 'idle' }` (literal específico), não como `FetchState<T>`. Em variants com payloads, o `dispatch` pode reclamar de incompatibilidade. Anotar explicitamente — `useReducer(reducer, { status: 'idle' } as FetchState<User>)` ou usando o terceiro argumento `init` com tipo de retorno explícito — resolve o problema.

## Em entrevista

> "Discriminated unions are my go-to for state in React with TypeScript. The pattern: each variant has a literal-typed discriminator — `type`, `kind`, `status` — and TS narrows automatically when you check it in a switch. For reducers, action types are a union of `{ type: '...'; ...payload }`, and the reducer's switch on `action.type` narrows the payload per case. For state machines, the same pattern represents mutually exclusive states like idle/loading/success/error, where each carries only the fields that make sense — `data` only in success, `error` only in error. Two essential techniques: an exhaustiveness check with `default: { const _: never = action; ... }` so adding a new variant breaks compile until I handle it; and discriminated unions in the state itself, not just actions, to eliminate invalid combinations like 'loading and data populated' that three parallel booleans would allow."

**Vocabulário-chave:** *discriminated union*, *discriminator*, *narrowing*, *exhaustiveness check*, *invalid state*, *make illegal states unrepresentable*.

## Veja também

- [[04 - interface vs type vs satisfies para props]] — `type` é o tool certo para discriminated unions; `interface` não suporta union types diretos.
- [[07 - Tipando hooks customizados]] — discriminated union no return de hook (Sample 5: `useFetchUser` com status).
- [[11 - Tipando data fetching]] — TanStack Query usa o `status` discriminado como API pública.
- [[TypeScript]] — seção "Discriminated unions" cobre o pattern fora do contexto React (Result types, branded types, state machines).
