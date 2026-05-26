---
title: "Inferir vs anotar - quando deixar o TS trabalhar"
created: 2026-04-26
updated: 2026-04-26
type: concept
status: seedling
publish: true
tags: [typescript, react, typescript-react, frontend, mental-model, inference, satisfies]
aliases:
  - Quando anotar tipos em React
  - satisfies operator
---

# Inferir vs anotar - quando deixar o TS trabalhar

> [!abstract] TL;DR
> A regra: anote inputs públicos (props, parâmetros, return types de funções exportadas), deixe inferir o resto. Quando inferência falha (initializers `null`, `[]`, `{}`), anote explicitamente. Use `satisfies` (TS 4.9+) quando quiser validar shape sem perder literal types.

## O que é

**Inferência** é o mecanismo pelo qual o TypeScript deduz o tipo de uma variável a partir do valor atribuído, sem precisar de anotação explícita. `const x = 5` é o suficiente para o compilador concluir que `x: number`. O handbook chama isso de *type inference* e descreve dois mecanismos centrais: o *best common type* (escolher um tipo compatível com todos os candidatos de uma expressão) e o *contextual typing* (inferir a partir do contexto de uso, ex: o tipo do parâmetro de um callback que vai para `addEventListener`). Em React, inferência funciona excepcionalmente bem para os casos comuns: `useState(0)` infere `number`, `useState('')` infere `string`, `const items = ['a', 'b']` infere `string[]`.

**Anotação** é a forma explícita: `const x: User = ...`. Necessária em duas situações distintas. A primeira: quando o tipo simplesmente não pode ser deduzido do valor — `useState(null)` infere `null` literal, então sem `useState<User | null>(null)` qualquer tentativa de chamar `setUser(novoUser)` falha. A segunda: quando você quer ser explícito **como contrato** — props de componentes exportados, return types de funções públicas, assinaturas que outras partes do código vão depender. Aqui anotar não é redundância, é declaração de API.

**`satisfies`** (TS 4.9+) é a ferramenta intermediária. Valida que um valor satisfaz um tipo sem fazer *widening*: a anotação normal `const palette: Record<string, string | RGB> = {...}` faz com que `palette.red` passe a ser `string | RGB`, perdendo a informação específica de cada chave; `const palette = {...} satisfies Record<string, string | RGB>` valida o shape **e** preserva os literais. Útil em configs, mapas de rotas, design tokens, tabelas de constantes.

## Por que importa

Excesso de anotação polui o código e frequentemente *piora* a inferência. Anotar `const items: string[] = ['a', 'b']` parece "explícito", mas perde o que poderia ter sido um literal `readonly ['a', 'b']` se combinado com `as const`. Em hooks customizados, anotar variáveis intermediárias (`const count: number = 5`) é ruído visual sem ganho. A regra "tipo é melhor explícito" — comum em outras linguagens — não traduz bem para TS, que foi desenhado para inferir o máximo possível.

Falta de anotação em fronteiras públicas é o erro oposto e mais grave. Sem anotar props, o TS infere `{}` ou erra com *implicit any* (em modo `strict`); o componente vira black box do ponto de vista do consumidor, e mudanças de implementação quebram silenciosamente quem chama. Sem anotar return type de hook customizado, o tipo "vaza" da implementação: refatorar o `useToggle` por dentro pode mudar o tipo público sem aviso. A regra "anote o que atravessa boundary, deixe inferir o resto" evita os dois extremos — o código fica limpo onde pode ser limpo, e contratual onde tem que ser contratual.

## Como funciona

### Sample 1 — quando inferir é melhor

```typescript
// Inferido — limpo e correto
const [count, setCount] = useState(0);  // number — claro
const items = ['a', 'b', 'c'];          // string[] — claro
const user = { name: 'Maria', age: 30 }; // { name: string; age: number } — claro

// Anotação aqui é poluição:
// const [count, setCount]: [number, React.Dispatch<React.SetStateAction<number>>] = useState<number>(0);
// Mais código, mesma informação que o TS já tinha.
```

Em todos esses casos o initializer fala por si — o tipo é óbvio para o compilador. Anotar duplica informação e adiciona ruído visual.

### Sample 2 — quando anotar é necessário

```typescript
// useState com null — o initializer não diz qual o tipo eventual
const [user, setUser] = useState<User | null>(null);

// Array vazio — TS inferiria never[] (em strict mode)
const [items, setItems] = useState<Item[]>([]);

// Objeto vazio — TS inferiria {}, sem props conhecidas
const [form, setForm] = useState<Partial<FormData>>({});

// Map/Set — não há literal type útil para inferir
const [cache, setCache] = useState<Map<string, User>>(new Map());
```

São as "ausências representadas como valor" — `null`, `[]`, `{}`, `new Map()` — onde inferência simplesmente não tem o que deduzir. Esses são os casos canônicos onde anotação explícita não é opcional, é obrigatória.

### Sample 3 — anotação em fronteira pública (props)

```typescript
// Sem anotação — TS reclama de implicit any em strict mode
function Button({ onClick, children }) {
  // ERRO: Parameter '{ onClick, children }' implicitly has an 'any' type.
  return <button onClick={onClick}>{children}</button>;
}

// Com anotação — contrato claro, consumidor sabe o que passar
type ButtonProps = {
  onClick: () => void;
  children: React.ReactNode;
};

function Button({ onClick, children }: ButtonProps) {
  return <button onClick={onClick}>{children}</button>;
}
```

Props são o exemplo canônico de boundary: o componente é consumido de fora, e quem consome precisa saber exatamente o que a API aceita. Inferir aqui não funciona — o TS não tem como adivinhar quais props um componente promete aceitar olhando só para o JSX interno. A anotação é o contrato.

### Sample 4 — `satisfies` para validar sem perder literal

```typescript
// Sem satisfies — anotação normal apaga os literais
type RouteMap = Record<string, string>;
const ROUTES: RouteMap = {
  home: '/',
  user: '/users/:id',
};
// ROUTES.home: string  (genérico, perdeu o '/')

// Com as const — preserva literal mas não valida shape
const ROUTES = {
  home: '/',
  user: '/users/:id',
} as const;
// ROUTES.home: '/' (literal preservado, mas nada garante o shape)

// Com satisfies — valida shape E preserva literal
const ROUTES = {
  home: '/',
  user: '/users/:id',
} satisfies RouteMap;
// ROUTES.home: '/' (literal preservado E shape validado)

// Bonus: satisfies pega typos
const PALETTE = {
  red: '#ff0000',
  green: '#00ff00',
  bleu: '#0000ff',  // ERRO: 'bleu' (esperava 'blue' se Colors fosse 'red' | 'green' | 'blue')
} satisfies Record<'red' | 'green' | 'blue', string>;
```

Esse é o caso onde anotar **destruiria** a inferência útil que você quer manter. `satisfies` foi introduzido em TS 4.9 exatamente para esse cenário: validar conformidade sem widening. O exemplo canônico do release notes é o `palette` com valores de tipos diferentes (`string | RGB`) — anotar perderia a info de qual chave tem qual tipo; `satisfies` mantém.

### Sample 5 — return de hook customizado: anotar ou inferir?

```typescript
// Inferido — o tipo "vaza" da implementação
function useToggle(initial = false) {
  const [on, setOn] = useState(initial);
  return [on, () => setOn(s => !s)] as const;
}
// Tipo público: readonly [boolean, () => void]
// Se eu trocar a implementação, o tipo público pode mudar sem aviso.

// Anotado — contrato explícito
function useToggle(initial = false): readonly [boolean, () => void] {
  const [on, setOn] = useState(initial);
  return [on, () => setOn(s => !s)] as const;
}
// API explícita: o consumidor confia na assinatura, não na implementação.
```

Os dois compilam, e em uso direto são idênticos. A diferença aparece em manutenção: hook customizado é parte da API do app (ou da lib, se for público). Anotar o return é declarar "isto é o contrato; a implementação pode mudar sem mexer aqui". Aprofundamento desse pattern (incluindo overloads e generics) está em [[07 - Tipando hooks customizados]].

## Na prática

Padrão observado em libs do ecossistema React (TanStack, Radix UI, MUI, Mantine): tipos exportados são sempre anotados — props de componentes públicos, return types de hooks expostos, assinaturas de funções utilitárias que aparecem na API. Tipos internos — variáveis locais dentro de um componente, valores intermediários de cálculos, callbacks passados inline — deixam inferir. O critério é "isto atravessa um boundary?" — se o tipo aparece na superfície que outro código consome, anotar. Se vive só dentro do escopo da função, deixar inferir.

Esse princípio é convenção do ecossistema porque resolve um trade-off real: anotação dá contrato e estabilidade de API, mas custa verbosidade; inferência dá ergonomia, mas custa estabilidade quando vaza para fora. Usar cada um no escopo certo aproveita o melhor dos dois — o código fica enxuto onde pode ser enxuto, e contratual onde precisa ser contratual.

## Armadilhas

- **Anotar variáveis locais com tipos primitivos.** `const x: number = 5` é poluição; o TS já infere `number` perfeitamente. Anotação faz sentido na fronteira (params, returns, props), não em variáveis intermediárias dentro de uma função.

- **Não anotar return de hook customizado.** Sem o return type explícito, o tipo público do hook passa a ser "o que a implementação atual retorna" — refatorar a implementação pode mudar a API sem aviso, e quem consome o hook quebra silenciosamente. Para hooks que viram parte da API do app, anote o return type.

- **Confundir `as const` com `satisfies`.** `as const` *altera* o tipo, deixando-o mais estreito (literal types, readonly arrays/tuplas, propriedades readonly). `satisfies` apenas *valida* contra um tipo, sem alterar o tipo inferido. Os dois são compostos com frequência (`{...} as const satisfies SomeShape`), mas confundi-los leva a tipos errados — `as const` em um config dá readonly que pode atrapalhar consumidores; `satisfies` sem `as const` não preserva literais primitivos como `string` literal.

- **Esquecer de anotar arrays e objetos vazios.** `useState([])` infere `never[]` em strict mode, e qualquer `setItems([newItem])` depois falha com `Type 'X' is not assignable to type 'never'`. Mesma armadilha com `useState({})` (`{}` sem props), `useReducer((s, a) => s, [])` ou `useState(new Map())` (sem generic, infere `Map<unknown, unknown>` ou similar). Sempre anote o generic quando o initializer é uma "estrutura vazia".

## Em entrevista

> "My rule: annotate what crosses a boundary, infer the rest. Component props, exported function signatures, custom hook return types — those need explicit annotations because they're contracts other code depends on. Local variables, intermediate values, primitives — those should infer; annotating them is just noise. The exception is when inference fails: `useState(null)` infers `null` literally, `useState([])` infers `never[]`, so I annotate. For configs and constants where I want to validate shape but keep literal types, I use `satisfies`."

**Vocabulário-chave:** *type widening*, *literal types*, *contract*, *satisfies operator*, *contextual typing*, *best common type*.

**Pergunta típica de senior interview:** *"When would you use `satisfies` instead of a normal type annotation?"* — resposta defensiva: when I want to validate that a value matches a shape but keep the specific inferred types of each property. Normal annotation widens to the declared type, losing the literal info per key. `satisfies` validates without widening — perfect for route maps, design tokens, configs where each entry has a specific value I want to query later.

## Veja também

- [[01 - A tripla inferência - props, state, hooks]] — o mental model que esta nota refina em regra prática
- [[04 - interface vs type vs satisfies para props]] — `satisfies` aplicado especificamente a props de componentes
- [[07 - Tipando hooks customizados]] — return types como contrato, overloads, generics em hooks
- [[TypeScript]] — seção "Tipos básicos" para fundamentos de inferência e widening
