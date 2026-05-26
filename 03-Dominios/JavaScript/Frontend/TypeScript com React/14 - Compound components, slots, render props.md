---
title: "Compound components, slots, render props"
created: 2026-04-26
updated: 2026-04-26
type: concept
status: seedling
publish: true
tags: [typescript, react, typescript-react, frontend, compound-components, slots, render-props, composition, advanced]
aliases:
  - Compound components tipados
  - Slot pattern Radix
  - Render props tipados
---

# Compound components, slots, render props

> [!abstract] TL;DR
> Três patterns de composição que tipam diferente: **compound components** (`<Tabs>`, `<Tabs.List>`, `<Tabs.Tab>`) compartilham state via Context interno tipado; **slots** (Radix `<Slot>` / `asChild`) substituem o wrapper pelo child mantendo props; **render props** (function-as-children) preservam inferência via generics no callback. Cada um resolve um caso diferente de "componentes que coordenam entre si".

## O que é

Componentes não vivem isolados — eles coordenam. Um `<Tabs>` precisa saber qual tab está ativa para mostrar o painel certo; um `<Tooltip>` precisa adicionar comportamento ao botão que dispara o tooltip; um `<DataLoader>` precisa expor `data`, `loading`, `error` para o consumidor decidir como renderizar. Os três patterns desta nota são respostas idiomáticas a famílias diferentes desse problema, e cada um tem uma assinatura de tipo que conta a história:

1. **Compound components** — um componente "raiz" expõe sub-componentes anexados como propriedades (`<Tabs>` exporta `Tabs.List`, `Tabs.Tab`, `Tabs.Panel`). O *root* mantém o estado coordenado em um Context interno; os sub-componentes leem esse Context via custom hook que faz throw se forem usados fora do root. A API explicita a estrutura visual (um `<Tabs>` tem uma `<List>` com `<Tab>`s e múltiplos `<Panel>`s), e o TS valida o uso correto através do contrato Context+hook.

2. **Slots / asChild** — um componente aceita uma prop booleana (`asChild`) que troca seu modo de operação: em vez de renderizar uma tag fixa, ele clona o filho único e injeta as próprias props nele. O canônico é `<Tooltip asChild><MyButton /></Tooltip>` — o `Tooltip` injeta `onMouseEnter`, `onMouseLeave`, `aria-describedby` etc. no `MyButton` em vez de criar um `<div>` wrapper. A primitiva de implementação é o `<Slot>` do Radix (`@radix-ui/react-slot`), que faz o merge de props com regras claras (event handlers do parent rodam depois do child, `className` concatena, `style` mescla).

3. **Render props** — o componente delega o render ao consumer, passando estado interno como argumento de uma função. A forma mais comum é *function-as-children*: `<DataLoader>{({ data }) => <View />}</DataLoader>`. Em TypeScript, o componente declara um generic (`T`) que percorre o estado interno, e o callback recebe esse `T` tipado — `data: User | undefined` se o consumer fez `parse: raw => userSchema.parse(raw)` retornar `User`. É a forma menos opinada das três sobre como o consumer renderiza, em troca de menos affordance visual na API.

## Por que importa

Os três patterns existem porque o problema "componentes que coordenam" tem variantes que diferem em **onde mora o controle do render** e **quem precisa ver qual estado**.

Compound components fazem sentido quando a estrutura visual é **fixa e nomeável**: um Tabs *é* uma lista de tabs com painéis correspondentes; uma Dialog *é* um trigger, um overlay e um content; um Select *é* um trigger e uma lista de options. A API que expõe `<Tabs.List>` e `<Tabs.Tab>` separadamente comunica imediatamente a hierarquia esperada, e o consumer compõe a árvore exata que ele quer (incluindo elementos arbitrários entre as tabs, layout customizado, etc.) sem precisar passar dezenas de props ao root. O custo é que o root precisa coordenar o state, e essa coordenação acontece via Context interno — o que liga este pattern direto à [[08 - Tipando Context API|nota 08]].

Slots resolvem um problema diferente: **adicionar comportamento sem adicionar wrapper na DOM**. Sem slot, um `<Tooltip><Button>Save</Button></Tooltip>` produz `<div data-tooltip-trigger><button>Save</button></div>` — duas camadas, eventos duplicados, ARIA quebrado, cascata de CSS imprevista. Com `asChild`, o `<Tooltip asChild><Button>Save</Button></Tooltip>` produz só `<button data-tooltip-trigger>Save</button>` — uma camada, props mescladas, comportamento adicionado ao próprio botão. Para tooltips, popovers, dropdown triggers e qualquer caso onde o "comportamento" deve viver no elemento existente, o slot é a forma idiomática.

Render props resolvem o caso onde **o componente possui estado mas não tem opinião sobre o render**. `<DataLoader>` sabe fazer fetch, parse, error handling; não sabe (e não deveria saber) se o consumer quer um spinner, um skeleton, uma mensagem inline ou nada. Em vez de aceitar 8 props (`renderLoading`, `renderError`, `renderSuccess`, `renderEmpty`...), o componente passa o estado completo em um único callback. O consumer decide tudo. Em TypeScript, o generic preserva o tipo do `data` end-to-end — o consumer escreve `parse={schema.parse}` e recebe no callback `data: T | undefined` com `T` inferido do retorno do parse.

A escolha entre os três geralmente é forçada pelo problema, não estética. Estado coordenado entre múltiplos sub-componentes pede compound. Comportamento sobre um único elemento existente pede slot. Estado interno + render livre pede render prop. Libs maduras combinam os três — o Radix usa compound + slot intensivamente, o TanStack Table usa render props para layout customizável.

## Como funciona

### Sample 1 — Compound component básico (anexar sub-components)

```typescript
import { useState, type ReactNode } from 'react';

type TabsProps = {
  defaultValue: string;
  children: ReactNode;
};

function TabsRoot({ defaultValue, children }: TabsProps) {
  const [value, setValue] = useState(defaultValue);
  return (
    <TabsContext value={{ value, setValue }}>{children}</TabsContext>
  );
}

function TabsList({ children }: { children: ReactNode }) {
  return <div role="tablist">{children}</div>;
}

function Tab({ value, children }: { value: string; children: ReactNode }) {
  const ctx = useTabsContext();
  const isActive = ctx.value === value;
  return (
    <button
      role="tab"
      aria-selected={isActive}
      onClick={() => ctx.setValue(value)}
    >
      {children}
    </button>
  );
}

function TabPanel({ value, children }: { value: string; children: ReactNode }) {
  const ctx = useTabsContext();
  if (ctx.value !== value) return null;
  return <div role="tabpanel">{children}</div>;
}

// Anexar sub-components ao root como propriedades
export const Tabs = Object.assign(TabsRoot, {
  List: TabsList,
  Tab: Tab,
  Panel: TabPanel,
});

// Uso:
<Tabs defaultValue="profile">
  <Tabs.List>
    <Tabs.Tab value="profile">Profile</Tabs.Tab>
    <Tabs.Tab value="settings">Settings</Tabs.Tab>
  </Tabs.List>
  <Tabs.Panel value="profile"><ProfileForm /></Tabs.Panel>
  <Tabs.Panel value="settings"><SettingsForm /></Tabs.Panel>
</Tabs>
```

A peça que faz o pattern funcionar é o `Object.assign(TabsRoot, { List, Tab, Panel })`. O resultado é um valor que continua sendo callable como componente (`<Tabs ...>`) e ao mesmo tempo carrega `Tabs.List`, `Tabs.Tab`, `Tabs.Panel` como propriedades acessíveis. O TS infere o tipo correto naturalmente — não há cast envolvido, e cada sub-component preserva sua assinatura individual (incluindo generics, se houver). A alternativa "imperativa" — `Tabs.List = TabsList` em statements separados — funciona em runtime, mas o TS perde o link entre o tipo de `Tabs` e os sub-components, e o consumer perde autocomplete em `Tabs.`. O `Object.assign` resolve ambos os problemas de uma vez.

### Sample 2 — Context interno tipado

```typescript
import { createContext, useContext } from 'react';

type TabsContextValue = {
  value: string;
  setValue: (value: string) => void;
};

const TabsContext = createContext<TabsContextValue | null>(null);

function useTabsContext(): TabsContextValue {
  const ctx = useContext(TabsContext);
  if (!ctx) {
    throw new Error('Tabs.Tab/Tabs.Panel must be used inside <Tabs>');
  }
  return ctx;
}
```

Esse é o pattern *default null + custom hook* da [[08 - Tipando Context API|nota 08]] aplicado ao caso compound. O Context é intencionalmente privado (não é exportado do módulo), e a única forma de acessar o estado coordenado é via os sub-components que o leem internamente. A mensagem do throw é específica — `"Tabs.Tab/Tabs.Panel must be used inside <Tabs>"` em vez de um genérico — para que, se um consumer escreve `<Tabs.Tab value="x">` órfão (fora de `<Tabs>`), o erro aponte direto para o problema. Esse é o detalhe que a Radix UI executa com cuidado em todos os primitives: cada `Trigger`, `Content`, `Item` tem mensagem própria, com o nome exato do componente raiz esperado.

Note a sintaxe de Provider: `<TabsContext value={...}>` direto, sem `.Provider`. Em React 19, o objeto retornado por `createContext` é renderizável como JSX, e `<Context value={...}>` é equivalente a `<Context.Provider value={...}>`. Detalhe da [[08 - Tipando Context API|nota 08]].

### Sample 3 — Slot pattern (estilo Radix)

```typescript
import { Slot } from '@radix-ui/react-slot';
import type { ComponentPropsWithoutRef, ReactNode } from 'react';

type ButtonProps = {
  asChild?: boolean;
  children: ReactNode;
} & ComponentPropsWithoutRef<'button'>;

function Button({ asChild, children, ...props }: ButtonProps) {
  const Comp = asChild ? Slot : 'button';
  return <Comp {...props}>{children}</Comp>;
}

// Sem asChild — renderiza <button>
<Button onClick={handleClick}>Save</Button>
// → <button onClick={...}>Save</button>

// Com asChild — substitui pelo child, mas injeta props (onClick, etc.) no child
<Button asChild>
  <a href="/profile" onClick={handleClick}>Profile</a>
</Button>
// → <a href="/profile" onClick={mergedHandler}>Profile</a>
//   — sem wrapper extra de <button>
```

O `Slot` do `@radix-ui/react-slot` é a primitiva: ele aceita `children` (deve ser um único elemento React válido) e clona esse elemento mesclando as props passadas para o `Slot`. Event handlers seguem regra de precedência clara — handlers do child rodam primeiro, depois os do parent (do `Slot`); cada um pode chamar `preventDefault()` para interromper. `className` é concatenado, `style` é mesclado, `ref` é forwardado para o child via composição de refs. O resultado em DOM é um único elemento — o do child — com as props acumuladas dos dois lados.

Para o TS, o `ComponentPropsWithoutRef<'button'>` herda todas as props nativas de `<button>`, e a prop `asChild` é o switch de modo. O consumer não precisa saber sobre o `Slot` — basta `asChild` na API pública. O custo é que, com `asChild`, o consumer **deve** passar exatamente um child válido (não uma string, não múltiplos elementos). Esse contrato é parte da convenção do pattern; o TS não consegue forçá-lo no tipo (children continua `ReactNode`), e o erro vem em runtime se a regra é violada.

### Sample 4 — Render prop tipado com generic

```typescript
import { useEffect, useState, type ReactNode } from 'react';

type DataLoaderProps<T> = {
  url: string;
  parse: (raw: unknown) => T;
  children: (state: {
    data: T | undefined;
    error: Error | null;
    isLoading: boolean;
  }) => ReactNode;
};

function DataLoader<T>({ url, parse, children }: DataLoaderProps<T>) {
  const [data, setData] = useState<T | undefined>(undefined);
  const [error, setError] = useState<Error | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetch(url)
      .then((r) => r.json())
      .then((raw: unknown) => {
        setData(parse(raw));
        setIsLoading(false);
      })
      .catch((e: Error) => {
        setError(e);
        setIsLoading(false);
      });
  }, [url, parse]);

  return <>{children({ data, error, isLoading })}</>;
}

// Uso — TS infere T do retorno de parse:
<DataLoader
  url="/api/me"
  parse={(raw) => userSchema.parse(raw)}  // (raw: unknown) => User
>
  {({ data, isLoading }) =>
    isLoading ? <Spinner /> : <h1>{data?.name}</h1>  // data: User | undefined
  }
</DataLoader>
```

A engrenagem de inferência aqui é a mesma da [[12 - Generic components|nota 12]]: `T` é declarado como type parameter no componente, e o TS infere `T` a partir do retorno de `parse`. Se `parse` é `(raw: unknown) => User`, então `T = User`, e o callback children recebe `{ data: User | undefined, error, isLoading }` automaticamente. O consumer não anota `T` em lugar nenhum — escreve `parse={schema.parse}`, e a inferência percorre o componente até o callback.

Detalhe importante: `parse` está nas dependências do `useEffect`. Se o consumer passa `parse={raw => schema.parse(raw)}` inline, uma nova função é criada a cada render do parent, e o effect re-dispara em cada render. A correção é envolver com `useCallback` no consumer, ou — mais idiomático — passar a referência estável `parse={schema.parse}` quando o método já é uma função stable (caso típico com Zod, Valibot, etc.). Isso é discutido em mais detalhe em [[11 - Tipando data fetching]].

### Sample 5 — Validação de children com `Children.forEach`

```typescript
import { Children, isValidElement, type ReactNode } from 'react';

type TabsListProps = {
  children: ReactNode;
};

function TabsList({ children }: TabsListProps) {
  // Validação opcional em desenvolvimento: avisa se children não é Tabs.Tab
  if (process.env.NODE_ENV === 'development') {
    Children.forEach(children, (child) => {
      if (!isValidElement(child) || child.type !== Tab) {
        console.warn('Tabs.List should only contain Tabs.Tab children');
      }
    });
  }

  return <div role="tablist">{children}</div>;
}
```

`React.Children` (`Children.map`, `Children.forEach`, `Children.toArray`, `Children.count`) é a API histórica para iterar sobre `children` quando o tipo é o `ReactNode` opaco. Funciona em React 19, mas a documentação oficial é explícita: *"Using `Children` is uncommon and can lead to fragile code"* ([fonte](https://react.dev/reference/react/Children)). O motivo é que `children` só contém o JSX literal passado pelo consumer — se o consumer passa `<MoreTabs />` (um componente que internamente renderiza vários `<Tab>`s), o `Children.forEach` vê um único filho (o `MoreTabs`), não os tabs renderizados por ele. A iteração é estrutural, não semântica.

A recomendação atual é evitar quando possível. Para o caso "validar shape dos filhos", as alternativas modernas são:

- **Aceitar arrays como prop tipada** em vez de children — `<Tabs items={[{ value, label, panel }]} />` em vez de `<Tabs><Tabs.Tab .../></Tabs>`. Funciona, mas perde a expressividade da hierarquia compound.
- **Confiar no Context** — em compound components, o sub-component (`Tab`) lê o Context e reclama via throw se está fora do root. O consumer recebe erro claro sem precisar de validação no parent.
- **Usar o pattern só em dev** — como no sample, gated por `process.env.NODE_ENV === 'development'`. Console warning em dev, no-op em prod. É o compromisso que libs como Mantine usam para diagnóstico sem peso em runtime de produção.

`Children.forEach` é escolha defensável quando o uso é diagnóstico e não load-bearing. Para code crítico (montar/transformar estrutura), as alternativas são preferíveis.

## Na prática

Os três patterns aparecem combinados em libs maduras do ecossistema React.

**Radix UI Primitives** usa compound + Slot intensivamente. `<Dialog.Root>` é o root que mantém estado de abertura via Context interno; `<Dialog.Trigger asChild>` aplica o slot ao child (`<Dialog.Trigger asChild><MyButton /></Dialog.Trigger>` injeta `onClick`, `aria-expanded`, `aria-controls` em `MyButton`); `<Dialog.Portal>`, `<Dialog.Overlay>`, `<Dialog.Content>`, `<Dialog.Title>`, `<Dialog.Description>`, `<Dialog.Close>` compõem a estrutura ([fonte](https://www.radix-ui.com/primitives/docs/components/dialog)). Cada sub-component tem mensagem de erro específica se for usado fora do root — execução cuidadosa do pattern Context+narrow.

**TanStack Table** é o exemplo canônico de render props para customização. O `useReactTable` retorna um objeto `table` com toda a API (rows, columns, headers, sorting state, etc.), e o consumer monta o JSX que quiser. A lib não impõe layout — render props levados ao extremo. A inferência de TypeScript é extensiva: o tipo dos dados das linhas propaga do schema das columns até cada cell renderer.

**shadcn/ui** usa Radix por baixo (`@radix-ui/react-dialog`, `@radix-ui/react-tabs`, etc.) e expõe componentes compound com estilos Tailwind customizáveis via copiar-e-colar. Herda o `asChild` do Radix em todos os componentes onde faz sentido (botão de trigger, links em menus, etc.).

**Headless UI** (Tailwind Labs) é o ponto canônico de render props + compound combinados. `<Combobox>` expõe sub-components (`Combobox.Input`, `Combobox.Options`, `Combobox.Option`) e cada um aceita render prop como children — `<Combobox.Option value={item}>{({ active, selected }) => ...}</Combobox.Option>`. O consumer recebe o estado interno (active, selected) e renderiza como quiser.

A linha geral: bibliotecas headless (que entregam comportamento + acessibilidade sem estilo) tendem a maximizar render props. Bibliotecas com opinião visual (Mantine, Chakra, MUI) tendem a maximizar polymorphic + compound, com slot/asChild como escape hatch para casos específicos. Não há vencedor universal; a escolha reflete o nível de opinião que a lib tem sobre o render final.

## Armadilhas

- **`Tabs.List = TabsList` em statements separados em vez de `Object.assign`.** Funciona em runtime, mas o TS perde o link entre `Tabs` e os sub-components — `Tabs.List` aparece como `any` ou disparam erros de "Property 'List' does not exist on type ...". Se o sub-component for genérico (ex: `Tab<T>`), os generics são perdidos. `Object.assign(TabsRoot, { List, Tab, Panel })` preserva tipos e generics em uma só atribuição.

- **`Children.map` / `Children.forEach` perdem tipos do children original.** Cada `child` na iteração é tipado como `ReactNode`, não como o tipo específico que o consumer passou. Para acessar `child.props`, é preciso `isValidElement(child)` para narrow para `ReactElement`, e mesmo assim `child.props` é `unknown` ou `any` — depende da versão de tipos do React. O pattern só funciona bem quando combinado com checagem de identidade (`child.type === Tab`) e `// @ts-expect-error` ou cast quando se tem certeza.

- **Render props criam closure nova a cada render.** O callback `{({ data }) => ...}` em function-as-children é uma função nova a cada render do parent. Se o componente filho renderizado por essa closure é memoizado (`React.memo`), o memo não funciona — referências de função são sempre diferentes. Correção: extrair o callback com `useCallback` e passá-lo, ou evitar `React.memo` em filhos cujo único prop é uma closure de render prop. O custo geralmente é pequeno; vale a pena profile antes de otimizar.

- **Slot pattern requer que o child aceite as props injetadas.** `<Button asChild><a /></Button>` funciona porque `<a>` aceita `onClick`, `ref`, `className` etc. Mas `<Button asChild><CustomThing /></Button>` só funciona se `CustomThing` repassa essas props para um elemento DOM. Se `CustomThing` ignora `onClick`, o botão não dispara — bug silencioso, sem erro de TS. Convenção em libs como Radix: documentar explicitamente que o child de `asChild` deve aceitar `onClick`, `ref`, `aria-*`, etc., ou implementar o child com `forwardRef` e spread completo de props.

- **Compound components com children livres permitem composições sem sentido.** `<Tabs><Tabs.Panel value="x" /><Tabs.List>...</Tabs.List></Tabs>` (panel antes de list) é tecnicamente válido pelo TS — `children: ReactNode` aceita qualquer ordem e qualquer combinação. O Context só checa "está dentro do root", não "está na ordem certa". Esse é o trade-off do pattern: alta flexibilidade visual em troca de menos garantia estrutural. Para forçar estrutura, a alternativa é `<Tabs items={[...]} />` (array prop), perdendo a expressividade compound.

## Em entrevista

> "Composition in React with TypeScript falls into three patterns. Compound components — like Radix's `<Dialog.Root>` plus `<Dialog.Trigger>` plus `<Dialog.Content>` — share state via an internal Context, with a custom hook that throws if a sub-component is used outside the root. The TypeScript machinery is mostly the Context typing pattern from earlier in the trail. Slots, like Radix's `<Slot>` and the `asChild` prop, replace the wrapper element with the child while injecting the parent's props, useful when you want to add a button's behavior to an `<a>` without a `<button>` wrapper in the DOM. Render props — function-as-children — let consumers control the render while the parent owns state; with generics, the inferred state type flows through the callback. Each pattern resolves a specific composition problem, and Radix is the canonical reference for combining compound and slots in production."

**Vocabulário-chave:** *compound component*, *slot*, *render prop*, *function-as-children*, *coordinated state*.

**Pergunta típica de senior interview:** *"How do you implement a `<Tabs>` component where `<Tabs.Tab>` and `<Tabs.Panel>` know which tab is active?"* — resposta defensiva: a `<Tabs>` root holds state with `useState` and exposes it through an internal Context — `createContext<TabsContextValue | null>(null)` plus a `useTabsContext` hook that throws if used outside the root. Sub-components (`Tab`, `Panel`) read this Context to know the active value. The sub-components are attached to the root with `Object.assign(TabsRoot, { List, Tab, Panel })`, which preserves their types and generics so the consumer gets autocomplete on `Tabs.`. The Context itself is not exported — only the compound component and its API are public, so the contract stays under control of the module.

## Veja também

- [[08 - Tipando Context API]] — Context interno é o coração do compound pattern
- [[12 - Generic components]] — generics em render props
- [[13 - Polymorphic components com as prop]] — alternativa relacionada (asChild vs as)
- [[React]] — seção "Componentes e JSX"
- [[TypeScript]] — seção "TypeScript em frontend (React)"
