---
title: "Tipando Context API"
created: 2026-04-26
updated: 2026-04-26
type: concept
status: seedling
publish: true
tags: [typescript, react, typescript-react, frontend, context, providers, narrowing]
aliases:
  - Context API tipado
  - Default null pattern
---

# Tipando Context API

> [!abstract] TL;DR
> `createContext<T>(null!)` é anti-pattern: vaza `null` para consumers ou mente sobre o tipo. Padrão idiomático: `createContext<T | null>(null)` + custom hook que faz narrowing e throw se usado fora do provider. Provider memoiza `value` quando o objeto é construído. Em React 19, `<Context>` é renderizável direto — `<Context.Provider>` ainda funciona mas é opcional.

## O que é

Context API é o mecanismo do React para compartilhar valores entre componentes sem prop drilling — um provider injeta um valor na árvore, e qualquer descendente pode lê-lo via `useContext`. Em TypeScript, há **dois pontos onde o tipo aparece** ao criar um Context, e entender essa dualidade é o que separa Context bem tipado de Context que mente:

1. **Tipo do valor** — o `T` em `createContext<T>(...)`. É o que `useContext(Ctx)` retorna no consumer. Esse tipo precisa cobrir todas as possibilidades reais: o valor passado pelo provider e a "ausência de provider" (caso o consumer esteja fora da árvore que tem o provider).

2. **Tipo do default** — o argumento passado em `createContext<T>(default)`. É o valor que `useContext` retorna quando **nenhum provider** está acima do consumer na árvore. Esse default não é o "valor inicial" do context (no sentido de `useState`); é o valor de **fallback** quando o consumer está desconectado.

A consequência prática: sem custom hook que faça narrowing, o consumer **lida com o default toda vez**. Se o tipo é `User | null` e o default é `null`, todo `useContext(UserContext).name` vira `useContext(UserContext)?.name` — porque o TS sabe que `null` é um valor possível em qualquer call site, mesmo dentro de um provider. O custom hook resolve isso movendo a verificação para um único ponto: ele lê o context, faz narrow, e devolve o valor já garantidamente não-null para o consumer.

## Por que importa

A tentação inicial ao tipar Context é escolher entre dois extremos, e ambos são pobres por razões diferentes.

O primeiro extremo é `createContext<User>(null!)`. O `!` é a *non-null assertion* — uma instrução para o TS tratar `null` como se fosse `User`. O initializer continua sendo `null` em runtime, mas o tipo público do context é `User`, sem nullable. O consumer escreve `useContext(UserContext).name` sem optional chaining, e tudo parece limpo. O problema aparece quando algum consumer é renderizado **fora do provider** — por engano, por refator, por composição imprevista — e o `useContext` retorna o `null` real. O acesso `.name` em `null` crasha em runtime com a clássica `Cannot read property 'name' of null`. O tipo mentiu para o compilador, e o erro só aparece quando o usuário final dispara o caminho errado. Pior: o tipo não dá pista alguma de que isso pode acontecer; o erro é silencioso até virar página em branco.

O segundo extremo é `createContext<User | null>(null)` — honesto sobre o default, mas vaza o `null` para todo consumer. Toda vez que alguém escreve `const user = useContext(UserContext)`, o `user` tem tipo `User | null`. Para acessar `user.name`, é preciso narrow: optional chaining (`user?.name`), guard explícito (`if (user) { ... }`), ou non-null assertion local (`user!.name`, que reintroduz o problema do extremo anterior). O resultado: o consumer faz a mesma checagem em dezenas de lugares, e qualquer esquecimento vira bug.

O pattern idiomático sintetiza os dois: o tipo do context é honesto (`T | null`), o default é honesto (`null`), mas o **acesso** acontece através de um custom hook que centraliza o narrowing. O hook lê o context, verifica se está dentro de um provider, e ou retorna o valor narrow para `T`, ou faz throw com mensagem clara. O consumer chama `useUser()` em vez de `useContext(UserContext)`, recebe `User` (não `User | null`), e ganha um erro explícito no boundary se algum descendente foi montado fora do provider — em vez de um crash genérico em algum acesso `.name` páginas adentro do código.

A diferença prática é a localização do erro. Sem o hook, o erro aparece em runtime, no consumer, sem contexto sobre o que está faltando. Com o hook, o erro aparece imediatamente na chamada do hook, com mensagem auto-documentada (`useUser must be used inside <UserProvider>`), apontando exatamente o que precisa ser corrigido. É a mesma diferença qualitativa entre asserção de invariante no boundary e crash em algum acesso aleatório lá no fundo.

## Como funciona

### Sample 1 — Anti-pattern (`null!`)

```typescript
import { createContext, useContext } from 'react';

type User = { id: string; name: string };

// NÃO use — força non-null mas pode crashar em runtime
const UserContext = createContext<User>(null!);

function Profile() {
  const user = useContext(UserContext);
  // user: User — segundo o TS
  // mas se Profile for renderizado fora do provider,
  // user é null em runtime, e o acesso abaixo crasha
  return <h1>{user.name}</h1>;
  //              ^^^^ Cannot read property 'name' of null
}
```

A `null!` é a *non-null assertion* aplicada ao initializer: instrui o TS a tratar `null` como se fosse `User`. O tipo público do context vira `User`, sem `null`, e o consumer escreve acessos diretos sem narrowing. O custo é que a mentira só aparece em runtime: se algum consumer for renderizado fora do provider — por engano, por composição imprevista, por unit test que esqueceu de envolver com o provider — o `useContext` retorna o `null` real, e o acesso crasha. O TS não sinaliza isso porque a assinatura do tipo o convenceu de que o valor é sempre `User`. O pattern é especialmente perigoso em apps grandes, onde a relação entre provider e consumer pode estar separada por muitas camadas.

### Sample 2 — Padrão idiomático (default null + custom hook)

```typescript
import { createContext, useContext } from 'react';

type User = { id: string; name: string };

// 1) Type explícito incluindo null no default
const UserContext = createContext<User | null>(null);

// 2) Custom hook que narroweia e throw se usado fora
function useUser(): User {
  const user = useContext(UserContext);
  if (!user) {
    throw new Error('useUser must be used inside <UserProvider>');
  }
  return user;  // narrowed para User (sem null)
}

// 3) Componente — sem checagem, valor garantido
function Profile() {
  const user = useUser();
  return <h1>{user.name}</h1>;  // user: User
}
```

O hook centraliza a verificação em um único ponto: ele lê o context, checa se há valor (i.e., se há provider acima), e ou retorna o valor já narrow, ou lança erro descritivo. O consumer (`Profile`) chama `useUser()`, recebe `User` — não `User | null` — e usa o valor sem optional chaining. Se algum dia `Profile` for renderizado fora do provider, o erro aparece **na chamada do hook**, com mensagem clara indicando o que está faltando, em vez de um crash genérico em algum `.name` lá adentro. Esse é o pattern documentado por libs como React Router, Radix UI e TanStack Router: o context cru não é parte da API pública; o que se exporta é o hook que já fez o narrow.

### Sample 3 — Provider tipado com `children` e `useMemo`

```typescript
import { createContext, useContext, useState, useMemo, type ReactNode } from 'react';

type User = { id: string; name: string };

type UserContextValue = {
  user: User | null;
  login: (u: User) => void;
  logout: () => void;
};

const UserContext = createContext<UserContextValue | null>(null);

function UserProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);

  // Memoiza o objeto de valor para evitar re-renders desnecessários
  const value = useMemo<UserContextValue>(
    () => ({
      user,
      login: (u) => setUser(u),
      logout: () => setUser(null),
    }),
    [user]
  );

  // React 19: <UserContext> é equivalente a <UserContext.Provider>
  return <UserContext.Provider value={value}>{children}</UserContext.Provider>;
}

// Custom hook
function useUser() {
  const ctx = useContext(UserContext);
  if (!ctx) throw new Error('useUser must be used inside UserProvider');
  return ctx;
}
```

O `useMemo` aqui não é optimization-theater — é um requisito de correção do pattern. Sem ele, toda vez que `UserProvider` re-renderiza (por causa de qualquer parent re-render), o objeto `{ user, login, logout }` é reconstruído como nova referência, e o React faz `Object.is` entre o `value` antigo e o novo. Como `{...}` !== `{...}`, todos os consumers que leem esse context são marcados para re-render — mesmo que `user` continue idêntico. Em apps com dezenas de consumers escutando o mesmo context, isso vira cascata de re-renders desnecessária. Com `useMemo([user])`, o `value` só muda quando `user` muda; objetos com a mesma identidade pulam o re-render.

A escolha de tipar `children` como `ReactNode` em vez de `JSX.Element` é deliberada: `ReactNode` cobre todos os tipos válidos de filhos (elementos, strings, números, fragments, arrays, `null`, `undefined`, `boolean`), enquanto `JSX.Element` cobre só elementos JSX. Para um provider que aceita qualquer subtree, `ReactNode` é o tipo certo — discutido em detalhes em [[03 - Por que React.FC saiu de moda]].

### Sample 4 — React 19: Context renderizável direto

```typescript
import { createContext, useState, useMemo, type ReactNode } from 'react';

type User = { id: string; name: string };

type UserContextValue = {
  user: User | null;
  setUser: (u: User | null) => void;
};

const UserContext = createContext<UserContextValue | null>(null);

// React 19+ — <Context> sem .Provider
function UserProviderModern({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const value = useMemo(() => ({ user, setUser }), [user]);
  return <UserContext value={value}>{children}</UserContext>;
}

// Funciona idêntico ao <UserContext.Provider value={value}>{children}</UserContext.Provider>
// Sintaxe mais limpa, mesma semântica.
// React 19 mantém .Provider para retrocompatibilidade, mas a docs oficial
// sinaliza depreciação futura — código novo já pode adotar a sintaxe direta.
```

Em React 19, o objeto retornado por `createContext` é diretamente renderizável como JSX, eliminando o sufixo `.Provider`. A semântica é idêntica: `<UserContext value={value}>` e `<UserContext.Provider value={value}>` produzem o mesmo comportamento em runtime, mesma propagação para consumers, mesma reatividade ao `value`. A diferença é apenas sintática — uma chamada a menos no path. A versão `.Provider` continua exportada para retrocompatibilidade (libs com peerDeps em React 18 ainda usam), mas a [documentação oficial](https://react.dev/blog/2024/12/05/react-19) sinaliza depreciação futura: código novo pode adotar a sintaxe direta sem reservas.

## Na prática

O pattern de `createContext<T | null>(null)` + custom hook com narrowing é o que aparece em libs idiomáticas do ecossistema React.

**React Router** expõe `RouterProvider` no topo e hooks como `useParams`, `useNavigate`, `useLocation` para o consumer. Internamente, esses hooks leem contexts privados (não exportados diretamente) e fazem o narrowing antes de devolver o valor. O usuário nunca toca em `RouterContext` cru — chama os hooks e recebe valores já tipados e validados.

**Radix UI** segue o mesmo princípio em todos os primitives. Cada componente composto (`<Dialog.Root>`, `<Tabs.Root>`, etc.) tem um context interno, e os subcomponents (`<Dialog.Trigger>`, `<Dialog.Content>`) leem esse context via hooks privados que fazem throw se forem usados fora do `Root`. A mensagem de erro é específica: `"Dialog.Trigger must be used within Dialog.Root"`, não um crash genérico. Esse detalhe é parte da experiência de DX que torna a lib agradável de usar.

**TanStack Router** usa o pattern intensivamente. O `RouterContext` carrega o estado da rota atual, e hooks como `useRouterState`, `useMatch`, `useLoaderData` fazem o narrowing antes de devolver dados ao consumer. O type safety chega ao ponto de ter generics na route definition propagando para os hooks — mas o pattern de base continua sendo "context com `T | null`, hook que narrow e throw fora do provider".

**Mantine** e a maioria das libs de UI seguem variantes do mesmo padrão: o context é detalhe de implementação, o hook é a API pública. O consumer importa `useMantineTheme()` ou similar; o `MantineThemeContext` cru pode até estar exportado, mas usá-lo diretamente não é o caminho idiomático.

A regra prática derivada: **trate o context como detalhe de implementação interno do módulo que o cria, e exporte o custom hook como a API pública**. Quem consome o módulo importa `useUser`, não `UserContext`; isso isola a lib do consumer e permite refatorar o context (mudar shape, adicionar middleware, trocar storage) sem quebrar quem chama o hook. Quando o context é exportado direto, ele vira parte do contrato público, e mudanças nele são breaking changes — sem necessidade.

## Armadilhas

- **`createContext<T>(null!)` (force non-null) é anti-pattern absoluto.** Crash silencioso em runtime sempre que algum consumer for renderizado fora do provider. O `!` mente para o compilador sem deixar pista no tipo, e o erro só aparece quando o usuário final dispara o caminho errado. A correção é sempre `createContext<T | null>(null)` + custom hook que narrow.

- **Esquecer `useMemo` no `value` do Provider.** Sintoma: cada parent re-render do provider dispara re-render em **todos os consumers** do context, mesmo quando o valor "lógico" não mudou. Causa: o objeto `{ ... }` no `value={...}` é reconstruído como nova referência a cada render, e o React faz `Object.is` entre antiga e nova — sempre falso para objetos novos. Correção: `const value = useMemo(() => ({ ... }), [deps])`. Em provider com várias funções (login, logout, etc.), também envolva as funções com `useCallback` se elas forem passadas para hooks dependency arrays nos consumers.

- **Criar Context per-component sem necessidade.** Context **não é state management**; é mecanismo de propagação que evita prop drilling. Para a maioria dos casos onde dev considera "vou criar um context para X", `useState` local + composition resolveriam melhor — context tem custo de re-render cascade, complexidade adicional na árvore, e dificulta testes unitários. Use context quando **vários descendentes não-relacionados** precisam do mesmo valor (theme, auth, i18n, router); para estado local de uma feature, deixe state na feature.

- **Anotar Context com tipo positivo + object literal vazio (`createContext<User>({} as User)`).** Pior que `null!` porque mente sem ser explícito. O `{} as User` é um objeto vazio cast como `User` — em runtime, o consumer recebe `{}`, e qualquer acesso a campo (`user.name`) retorna `undefined`. Diferente de `null!`, que pelo menos crasha cedo, esse pattern faz o app rodar com valores `undefined` espalhados — bugs sutis em vez de crash claro. Sempre prefira `null` explícito + narrowing.

- **Exportar o `Context` cru como API pública.** Se `UserContext` é exportado direto, qualquer consumidor pode chamar `useContext(UserContext)` ignorando o hook narrow. O context cru é detalhe de implementação; exporte só o `UserProvider` e o `useUser`. Isso preserva o invariante "todo acesso passa pelo narrow" e permite refatorar o context internamente sem quebrar consumers.

## Em entrevista

> "When typing Context, my rule is: `createContext<T | null>(null)` plus a custom hook that narrows and throws if used outside the provider. The alternative — `createContext<T>(null!)` — lies to the compiler: it claims the value is `T` but in reality it's `null` until a provider wraps the consumer, so any code using the context outside a provider crashes silently. The narrowing hook turns that runtime crash into a clear error message at the boundary, and after the hook, consumers get a guaranteed non-null value. Two more things: memoize the provider value with `useMemo` so re-renders don't cascade through every consumer, and remember that in React 19 you can render `<Context value={...}>` directly without `.Provider`."

**Vocabulário-chave:** *narrowing*, *non-null assertion*, *provider*, *consumer*, *re-render cascade*.

**Pergunta típica de senior interview:** *"Why is `createContext<T>(null!)` an anti-pattern?"* — resposta defensiva: it lies to the compiler. The runtime initializer is `null`, but the type asserts the value is always `T`, so the consumer skips narrowing. If any consumer is rendered outside the provider — by mistake, by refactor, in a unit test that forgot the wrapper — `useContext` returns the real `null`, and the consumer crashes silently with a generic property access error. The narrowing-hook pattern moves that failure to a single boundary with a descriptive error message, and gives consumers a guaranteed non-null value after the hook returns.

## Veja também

- [[05 - Tipando state e refs]]
- [[09 - Tipando reducers e state machines]] — quando usar reducer dentro do provider
- [[React]] — seção "State management"
