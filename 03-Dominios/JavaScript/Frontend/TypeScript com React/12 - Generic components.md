---
title: "Generic components"
created: 2026-04-26
updated: 2026-04-26
type: concept
status: seedling
publish: true
tags: [typescript, react, typescript-react, frontend, generics, components, advanced]
aliases:
  - Componentes genéricos React
  - <T,> em tsx
---

# Generic components

> [!abstract] TL;DR
> Function declarations suportam generics naturalmente (`function List<T>(props: { items: T[] })`). Arrow functions em `.tsx` precisam de hack — vírgula extra (`<T,>`) ou constraint (`<T extends unknown>`) — porque JSX confunde `<T>` com tag de abertura. Constraint preserva inferência (`T extends { id: string }` força `id` presente sem perder o `T` específico).

## O que é

Um *generic component* é um componente cujo tipo das props depende de um *type parameter* declarado pelo próprio componente. Em vez de fixar o shape dos dados em compile time (`items: User[]`), o componente recebe um `T` que é resolvido no *call site* a partir das props passadas: `<List items={users} />` faz o TS inferir `T = User`, e qualquer callback que receba `item: T` aparece tipado como `User` para o consumer.

A motivação é a mesma de uma função genérica em TypeScript "puro" — `function identity<T>(x: T): T` — adaptada à API de componente. Sem generic, há duas saídas, ambas pobres: anotar `items: any[]` (perde checagem completa) ou `items: unknown[]` (força o consumer a fazer narrow/cast em todo callback). Com generic, o componente atua como uma "passagem" que carrega o tipo do dado de uma prop para outras (renderItem, keyExtractor, onSelect) sem perder precisão.

A mecânica é a mesma de generics em hooks ([[07 - Tipando hooks customizados]] já mostrou `useFetch<T>` e `useStorage<T>`): declarar `<T>` na assinatura, usar `T` nos parâmetros, deixar o TS inferir. A diferença em React é só sintática — JSX e generics em arrow function brigam pelo mesmo `<T>`, e essa briga gera o workaround de vírgula que ocupa metade desta nota.

## Por que importa

Componentes reutilizáveis de coleção — `<List>`, `<Select>`, `<Table>`, `<Combobox>`, `<DataGrid>` — vivem ou morrem pela qualidade do tipo que expõem ao consumer. O que diferencia uma `<List>` boa de uma ruim não é o render do `<ul>` (qualquer dev faz em 5 minutos): é se o `renderItem` do consumer recebe `(user: User) => ReactNode` ou `(user: unknown) => ReactNode`. No primeiro caso, autocomplete funciona, refactors quebram em compile time, bugs de shape viram erros visíveis. No segundo, cada callback do consumer precisa fazer narrow manual, e qualquer mudança no shape do `User` passa silenciosa pela `<List>` até estourar em runtime.

Generics resolvem isso preservando o tipo do dado **end-to-end**: o `T` entra pelo prop `items`, é usado no `renderItem`, no `keyExtractor`, no `onSelect`, e sai inferido no callback do consumer. Não há cast intermediário, não há `unknown` no caminho. O componente continua reutilizável (uma definição serve para `User`, `Order`, `Product`, qualquer shape), mas paga o preço da reusabilidade em tempo de design — não no consumer.

A alternativa sem generic — escrever `<UserList>`, `<OrderList>`, `<ProductList>` separados — desencoraja reuso e cria divergência: cada cópia evolui em direção ligeiramente diferente, regras de acessibilidade são reimplementadas em cada uma, e o design system fragmenta. Generic é o que permite uma `<List>` única ser **a** primitiva de listagem do app sem que o time pague em tipo.

## Como funciona

### Sample 1 — `List<T>` com function declaration

```typescript
type ListProps<T> = {
  items: T[];
  renderItem: (item: T) => React.ReactNode;
  keyExtractor: (item: T) => string;
};

function List<T>({ items, renderItem, keyExtractor }: ListProps<T>) {
  return (
    <ul>
      {items.map(item => (
        <li key={keyExtractor(item)}>{renderItem(item)}</li>
      ))}
    </ul>
  );
}

// Uso — TS infere T do prop items:
type User = { id: string; name: string };
const users: User[] = [/* ... */];

<List
  items={users}
  renderItem={user => <span>{user.name}</span>}  // user: User (inferido)
  keyExtractor={user => user.id}                // user: User (inferido)
/>
```

Function declaration é o caminho ergonômico. `<T>` aparece imediatamente após o nome da função, antes dos parâmetros, e o parser de TS não tem ambiguidade — `function` é uma palavra-chave reservada, qualquer `<T>` que segue é inequivocamente um type parameter. O consumer escreve `<List items={users} ...>` e o TS infere `T = User` a partir da única fonte que importa: o tipo do prop `items`. Os outros callbacks "herdam" o `T` inferido — `renderItem` e `keyExtractor` recebem `user: User` sem anotação explícita.

### Sample 2 — Mesmo componente com arrow function (workaround)

```typescript
// Em .tsx, generic em arrow function precisa de truque
// PROBLEMA: <T> é parsed como JSX
// const List = <T>({ items }: ListProps<T>) => ...  // ERRO: JSX element 'T' has no corresponding closing tag

// Solução 1: vírgula extra <T,>
const List = <T,>({ items, renderItem, keyExtractor }: ListProps<T>) => (
  <ul>
    {items.map(item => (
      <li key={keyExtractor(item)}>{renderItem(item)}</li>
    ))}
  </ul>
);

// Solução 2: constraint <T extends unknown>
const ListAlt = <T extends unknown>({ items, renderItem, keyExtractor }: ListProps<T>) => (
  <ul>
    {items.map(item => (
      <li key={keyExtractor(item)}>{renderItem(item)}</li>
    ))}
  </ul>
);

// Function declaration não tem esse problema:
function ListBest<T>({ items, renderItem, keyExtractor }: ListProps<T>) {
  return (
    <ul>
      {items.map(item => (
        <li key={keyExtractor(item)}>{renderItem(item)}</li>
      ))}
    </ul>
  );
}
```

A ambiguidade existe porque `.tsx` reusa `<` para abrir tanto generics quanto JSX tags. Quando o parser vê `<T>` em posição de expressão, sem outras pistas, ele assume JSX. A vírgula `<T,>` é o desambiguador mínimo — JSX não aceita lista separada por vírgula no nome da tag, então o parser só pode interpretar como type parameter list. `<T extends unknown>` resolve pela mesma razão: `extends` em JSX não é gramática válida. Esse workaround **continua necessário em TS 5.x** ([fonte: macwright.com TIL TypeScript and TSX](https://macwright.com/2024/08/01/til-typescript-tsx); [Ashby Engineering Blog](https://www.ashbyhq.com/blog/engineering/generic-arrow-function-in-tsx)) — não há plano de mudança porque o conflito é estrutural na gramática JSX, não bug do compiler. Function declaration evita o problema sem custo, e por isso é a escolha default em codebases que padronizam.

### Sample 3 — Inferência preservada e constraints

```typescript
// Constraint força propriedade comum, mas mantém T específico
type SelectProps<T extends { id: string; label: string }> = {
  options: T[];
  value: T['id'];
  onSelect: (option: T) => void;
};

function Select<T extends { id: string; label: string }>({
  options,
  value,
  onSelect,
}: SelectProps<T>) {
  return (
    <select
      value={value}
      onChange={e => {
        const found = options.find(o => o.id === e.target.value);
        if (found) onSelect(found);
      }}
    >
      {options.map(o => (
        <option key={o.id} value={o.id}>{o.label}</option>
      ))}
    </select>
  );
}

// Uso — onSelect recebe o tipo T preservado:
type User = { id: string; label: string; email: string };
const users: User[] = [/* ... */];

<Select<User>
  options={users}
  value={users[0].id}
  onSelect={user => console.log(user.email)}  // user: User (não { id; label } só)
/>
```

`T extends { id: string; label: string }` é a fórmula central de generic com constraint: o componente exige duas propriedades específicas (sem elas, não consegue renderizar `<option key={o.id} value={o.id}>{o.label}</option>`), mas **mantém** o `T` concreto que o consumer passou. Sem constraint, o `Select` não saberia que `o.id` ou `o.label` existem — `o` seria `unknown`. Com constraint excessiva (`T = { id: string; label: string }` fixo), o `onSelect` receberia só `{ id; label }` e o `user.email` daria erro. A constraint diz "exijo essas chaves, mas o resto do shape é seu" — é o equilíbrio que faz o pattern funcionar.

### Sample 4 — Tabela genérica com inferência preservada nos columns

```typescript
type Column<T> = {
  key: keyof T;
  header: string;
  render?: (value: T[keyof T], row: T) => React.ReactNode;
};

type TableProps<T> = {
  rows: T[];
  columns: Column<T>[];
};

function Table<T extends { id: string | number }>({ rows, columns }: TableProps<T>) {
  return (
    <table>
      <thead>
        <tr>
          {columns.map(c => <th key={String(c.key)}>{c.header}</th>)}
        </tr>
      </thead>
      <tbody>
        {rows.map(row => (
          <tr key={row.id}>
            {columns.map(c => (
              <td key={String(c.key)}>
                {c.render ? c.render(row[c.key], row) : String(row[c.key])}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}

// Uso:
type Order = { id: number; total: number; customer: string };
const orders: Order[] = [/* ... */];

<Table<Order>
  rows={orders}
  columns={[
    { key: 'customer', header: 'Cliente' },
    { key: 'total', header: 'Total', render: v => `R$ ${v}` },
  ]}
/>
```

`Table` combina dois usos de generic: o `T` no `rows: T[]` e o `keyof T` no `Column<T>['key']`. O ganho é que `key: 'customer'` só é aceito se `customer` existir em `T` — o consumer recebe autocomplete e erro de compile se digitar uma chave inexistente. A constraint `T extends { id: string | number }` é puro contrato de uso: o componente precisa de `id` para o `key` do `<tr>`, então exige; o resto do shape (`total`, `customer`, ...) fica livre. `T[keyof T]` no `render` é o tipo do valor da célula — sempre uma das propriedades de `T`. Esse pattern aparece em libs reais (próxima seção).

### Sample 5 — Generic + default type (raro mas útil)

```typescript
type FetcherProps<T = unknown> = {
  url: string;
  parse?: (raw: unknown) => T;
  render: (data: T) => React.ReactNode;
};

function Fetcher<T = unknown>({ url, parse, render }: FetcherProps<T>) {
  // ... fetch + parse + render
  return null;  // simplificação
}

// Uso sem generic — T = unknown
<Fetcher url="/api/health" render={data => <pre>{JSON.stringify(data)}</pre>} />

// Uso com generic — T = User
type User = { id: string; name: string };
declare const userSchema: { parse: (raw: unknown) => User };

<Fetcher<User>
  url="/api/me"
  parse={u => userSchema.parse(u)}
  render={u => <h1>{u.name}</h1>}
/>
```

Default type (`<T = unknown>`) é o equivalente de "default parameter" para generics: quando o consumer não passa nem infere, o `T` cai no default em vez de ficar não-resolvido. Útil em componentes que aceitam configuração tipada **opcional** — `Fetcher` pode ser usado sem se preocupar com o shape (`data: unknown`, JSON cru), ou pode ser especializado com `<User>` quando há um schema. Sem default, o consumer "casual" precisa passar `<unknown>` explícito, ou aceitar erro de inferência. `unknown` como default é a escolha defensiva — força o consumer a fazer narrow se quiser tocar nos campos.

## Na prática

Generic components são pattern dominante no ecossistema React de UI/data:

- **Tabelas** — TanStack Table expõe `<DataTable<User> ...>` com generic explícito, e os `columns` ficam tipados (`accessorKey` aceita só `keyof User`). É o uso canônico de [[#Sample 4 — Tabela genérica com inferência preservada nos columns|Sample 4]] em escala de lib.

- **Selects e comboboxes** — Mantine, Headless UI e Radix expõem `<Combobox<T>>` / `<Listbox<T>>` genéricos, onde `value` e `onChange` carregam o tipo do item. Em design systems internos, `<Select<User>>` é tão comum quanto `<Button>`.

- **Virtualização** — `react-window` e `react-virtuoso` aceitam `<VirtualList<Item>>` com generic no item, preservando tipo no callback de render.

- **Forms** — `react-hook-form` é construído inteiro em torno de `<FormProvider<TFormData>>` e `<Controller<TFormData, TName>>`, com generics encadeados que carregam o shape do form até o nome do campo (autocomplete em `name="user.address.city"`).

Em design systems internos, `<List<T>>` / `<Select<T>>` / `<Table<T>>` formam a tríade base — qualquer componente de coleção é genérico por default. O pattern combina com [[13 - Polymorphic components com as prop|polymorphic]] (`<List as="ol" items={...}>`) quando o componente também precisa variar a tag HTML — generic + polymorphic é o ponto de chegada para componentes maximamente reutilizáveis.

## Armadilhas

- **Esquecer a vírgula em arrow function `.tsx`.** Sintoma: `JSX element 'T' has no corresponding closing tag`. Causa: `<T>` foi parsed como abertura de JSX, não como type parameter. Correção: `<T,>` (vírgula extra) ou `<T extends unknown>` (constraint vazia). Function declaration evita o problema — adote como convenção quando o time padroniza generic components.

- **Esperar inferência a partir do return type.** TS infere generics só de **argumentos**, não de uso futuro do retorno. Se `T` aparece só no JSX renderizado e não em nenhum prop, o consumer **precisa** passar explícito (`<List<User> ...>`); sem o explícito, `T` vira `unknown`. Inferência funciona "para trás" do prop ao type parameter — não "para frente" do retorno ao type parameter.

- **Constraint mal calibrada.** `<T extends object>` é permissiva demais — não restringe nada útil; o consumer pode passar `{}` vazio. `<T extends { id: string }>` força um shape específico mas perde flexibilidade se o app usa `id: number` em algumas tabelas. Calibrar conforme o caso: a constraint deve ser **o mínimo necessário para o componente funcionar**, nada mais. Tudo extra invade o shape do consumer e gera fricção.

- **Confundir generic component com generic function por dentro.** Em React, o type parameter vai antes dos parâmetros da função do componente: `function List<T>(props: ListProps<T>)`. Não é `function List(props: <T>ListProps<T>)`, e não é em prop ou em hook interno. Misturar a posição do `<T>` é erro comum em quem está aprendendo — leva a TS aceitar mas perder inferência (o `T` fica isolado no escopo errado).

- **`defaultValue` literal em prop genérica.** Se o componente tem prop `defaultValue: T` e o consumer passa `defaultValue="light"`, TS pode inferir `T = "light"` (literal) em vez de `T = string`. O resultado: o resto da API "trava" no literal e callbacks de mudança ficam inutilizáveis. Workaround: usar default no generic (`<T = string>`) ou anotar explícito (`<MyComponent<string> defaultValue="light">`). Esse caso aparece principalmente em selects e inputs controlados.

## Em entrevista

> "Generic components preserve type inference from the caller's data through the component's API. The pattern: declare a type parameter on the component (`function List<T>(props: { items: T[]; render: (item: T) => ReactNode })`), and TypeScript infers `T` from the `items` prop at the call site. The render callback then receives the exact item type, not `unknown` or `any`. The classic gotcha is in `.tsx` files: arrow functions can't use `<T>` because the parser thinks it's a JSX tag — you either add a trailing comma (`<T,>`) or a constraint (`<T extends unknown>`). Function declarations don't have this problem. Inference is the goal: `<List items={users} render={u => u.name} />` should give the consumer a typed `u: User` without any explicit annotation. Constraints (`T extends { id: string }`) shape the contract while keeping the specific type — they're how you require an `id` field without losing the rest of the user's structure."

**Vocabulário-chave:** *type parameter*, *type inference*, *generic constraint*, *JSX ambiguity*, *call-site inference*.

## Veja também

- [[04 - interface vs type vs satisfies para props]]
- [[07 - Tipando hooks customizados]] — generics em hooks (mesma mecânica)
- [[13 - Polymorphic components com as prop]] — generic + polymorphic combinados
- [[TypeScript]] — seção "Generics"
