---
title: "React"
created: 2026-04-01
updated: 2026-04-11
type: concept
status: evergreen
tags:
  - javascript
  - frontend
  - entrevista
publish: true
---

# React

Deep dive em **React** — biblioteca para construção de interfaces via componentes declarativos. Foco em React 19+ (2026), Hooks, state management, performance e patterns modernos. Para JavaScript base, ver [[JavaScript Fundamentals]]. Para TypeScript com React, ver [[TypeScript]]. Para testes de componentes, ver [[Testes em JavaScript]]. Para HTML/CSS, ver [[HTML e CSS]].

## O que é

React é uma **biblioteca JavaScript** (não framework) criada pelo Facebook (2013) para construir UIs através de **componentes compostos**. Em 2026, é a base da maioria dos sistemas web modernos, e **React 19** trouxe mudanças significativas: **React Compiler**, **Server Components**, **Server Actions**, e mudanças em APIs legacy.

**Em 2026:**

- **React 19** é o mainstream, com React Compiler opcional
- **Next.js 16** com Turbopack por default é o meta-framework dominante
- **TanStack Router + React Router 7** convergem
- **Vite 8** é o bundler padrão para SPAs
- **Server Components** mudam fundamentalmente o modelo mental

Em entrevistas, o que diferencia um senior em React:

1. **Entender reconciliation** — como React decide o que re-renderizar
2. **Hooks profundamente** — dependency arrays, closures stale, rules of hooks
3. **State management** — quando useState, quando Context, quando Zustand/Redux, quando server state
4. **Performance** — memo, useMemo, useCallback, React Compiler, Profiler
5. **Server vs Client Components** — RSC, boundaries, "use client"
6. **Forms avançados** — react-hook-form, validation, controlled vs uncontrolled
7. **Data fetching moderno** — React Query, Suspense, streaming SSR
8. **Testing** — Testing Library philosophy, user-centric
9. **Arquitetura** — feature-based, containers vs presenters, hooks custom

---

## React 19 — o que mudou

### React Compiler

Compilador opt-in que **automatiza memoization**. Não precisa mais de `useMemo`, `useCallback`, `memo()` na maioria dos casos — o compilador descobre.

```tsx
// Sem React Compiler — memoization manual
const MemoChild = memo(Child);
const handleClick = useCallback(() => doStuff(id), [id]);
const filtered = useMemo(() => items.filter(x => x.active), [items]);

// Com React Compiler — nada disso, compilador otimiza
const handleClick = () => doStuff(id);
const filtered = items.filter(x => x.active);
// Compilador gera memoization onde necessário
```

**Como ativar:**

```javascript
// vite.config.ts
import react from '@vitejs/plugin-react';
import { compilerPlugin } from 'babel-plugin-react-compiler';

export default {
    plugins: [react({ babel: { plugins: ['babel-plugin-react-compiler'] } })]
};
```

**Cuidados:**

- Compilador assume código obedecendo **Rules of React** (sem mutação, sem side effects em render)
- ESLint plugin `eslint-plugin-react-compiler` detecta violações
- Ainda experimental em 2026, mas ganhando adoção rápida

### Server Components e Server Actions

**Server Components (RSC)** — componentes que rodam **apenas no servidor**, retornam markup, não vão ao client JS bundle.

```tsx
// app/page.tsx — Server Component por default em Next.js 13+
async function BlogList() {
    const posts = await db.posts.findMany();  // direto do DB, sem API
    return (
        <ul>
            {posts.map(p => <li key={p.id}>{p.title}</li>)}
        </ul>
    );
}
```

**Benefícios:**

- Acesso direto a dados server-side (DB, filesystem)
- Zero JavaScript no client para esses componentes
- SEO e performance iniciais excelentes

**Limitações:**

- Sem `useState`, `useEffect`, event handlers — são Server, não Client
- Não podem usar browser APIs

### Client Components

Para interatividade, use `'use client'` no topo do arquivo:

```tsx
'use client';

import { useState } from 'react';

export default function Counter() {
    const [count, setCount] = useState(0);
    return <button onClick={() => setCount(count + 1)}>{count}</button>;
}
```

**Regra:** comece com Server Components, adicione `'use client'` só quando precisar de interatividade.

### Server Actions

Mutações diretas do servidor, sem API layer:

```tsx
// app/actions.ts
'use server';

export async function createPost(formData: FormData) {
    const title = formData.get('title') as string;
    await db.posts.create({ data: { title } });
    revalidatePath('/blog');
}

// app/page.tsx
import { createPost } from './actions';

export default function NewPostForm() {
    return (
        <form action={createPost}>
            <input name="title" />
            <button type="submit">Create</button>
        </form>
    );
}
```

### Novos hooks do React 19

**`use()`** — unwrap Promise ou Context dentro de componentes:

```tsx
function UserProfile({ userPromise }) {
    const user = use(userPromise);  // suspende até resolver
    return <h1>{user.name}</h1>;
}
```

**`useActionState()`** — gerencia state de actions:

```tsx
function Form() {
    const [state, formAction, isPending] = useActionState(createPost, { error: null });

    return (
        <form action={formAction}>
            <input name="title" />
            {state.error && <p>{state.error}</p>}
            <button disabled={isPending}>Create</button>
        </form>
    );
}
```

**`useOptimistic()`** — updates otimistas enquanto aguarda server:

```tsx
function Comments({ initial }) {
    const [optimistic, addOptimistic] = useOptimistic(
        initial,
        (state, newComment) => [...state, newComment]
    );

    async function submit(formData) {
        addOptimistic({ text: formData.get('text'), pending: true });
        await createComment(formData);
    }

    return (
        <>
            {optimistic.map(c => <li>{c.text}</li>)}
            <form action={submit}>...</form>
        </>
    );
}
```

**`useFormStatus()`** — status do form pai:

```tsx
function SubmitButton() {
    const { pending } = useFormStatus();
    return <button disabled={pending}>{pending ? 'Saving...' : 'Save'}</button>;
}
```

### Depreciações em React 19

- **`PropTypes`** — removido, use TypeScript
- **`defaultProps` em function components** — use defaults de destructuring
- **`contextTypes` / `childContextTypes`** — removidos
- **`forwardRef` menos necessário** — refs agora passam como prop normal
- **`string refs`** — removidos

---

## Componentes e JSX

### Function components

```tsx
type ButtonProps = {
    onClick: () => void;
    variant?: 'primary' | 'secondary';
    disabled?: boolean;
    children: React.ReactNode;
};

export function Button({ onClick, variant = 'primary', disabled, children }: ButtonProps) {
    return (
        <button
            onClick={onClick}
            className={`btn btn-${variant}`}
            disabled={disabled}
        >
            {children}
        </button>
    );
}
```

### Class components (legacy)

```tsx
// Raramente usado em código novo. Hooks substituíram.
class Counter extends React.Component<{}, { count: number }> {
    state = { count: 0 };

    increment = () => this.setState({ count: this.state.count + 1 });

    render() {
        return <button onClick={this.increment}>{this.state.count}</button>;
    }
}
```

**Em 2026, class components são legacy.** Manter por compatibilidade, mas escreva function components com hooks.

### JSX — syntactic sugar

```tsx
const element = <h1 className="title">Hello, {name}</h1>;

// Compila para
const element = React.createElement('h1', { className: 'title' }, 'Hello, ', name);
```

**Regras:**

- Tags minúsculas → elementos HTML (`<div>`, `<span>`)
- Tags maiúsculas → componentes React (`<Button>`, `<UserCard>`)
- Atributos camelCase (`className`, não `class`; `onClick`, não `onclick`)
- Self-closing para tags vazias (`<br />`, não `<br>`)
- JavaScript expressions em `{}`

### Fragments

```tsx
// Em vez de wrapper desnecessário
return (
    <>
        <h1>Title</h1>
        <p>Content</p>
    </>
);

// Com key (para loops)
return items.map(item => (
    <React.Fragment key={item.id}>
        <dt>{item.term}</dt>
        <dd>{item.description}</dd>
    </React.Fragment>
));
```

### Conditional rendering

```tsx
// Ternário
{isLoggedIn ? <Dashboard /> : <LoginForm />}

// &&
{hasError && <ErrorMessage />}

// Short-circuit — CUIDADO
{count && <Badge count={count} />}  // se count === 0, renderiza '0' (!)
{count > 0 && <Badge count={count} />}  // melhor

// Null para nada
{condition ? <Component /> : null}
```

### Listas e keys

```tsx
{users.map(user => (
    <UserCard key={user.id} user={user} />
))}
```

**Regras de key:**

- **Única entre irmãos** (não globalmente)
- **Estável** (não mude entre renders)
- **Previsível** (não use `Math.random()`)
- **Prefira ID do domínio**, não índice do array

**Por que index como key é problema:**

```tsx
// RUIM — ao remover item no meio, React confunde estado
{items.map((item, i) => <Input key={i} defaultValue={item} />)}

// Se remover o primeiro:
// Antes:  key=0 "a", key=1 "b", key=2 "c"
// Depois: key=0 "b", key=1 "c"
// React reutiliza DOM mas com valor errado
```

---

## Hooks essenciais

Regras universais:

1. **Só chame hooks no top level** — nunca em condições, loops, nested functions
2. **Só chame hooks de componentes React ou hooks customizados**
3. **Nome deve começar com `use`** para hooks customizados

ESLint plugin `eslint-plugin-react-hooks` verifica estas regras.

### useState

```tsx
const [count, setCount] = useState(0);
const [user, setUser] = useState<User | null>(null);

// Lazy initialization — função só roda 1x
const [state, setState] = useState(() => expensiveInit());

// Updater function — use quando o novo state depende do anterior
setCount(prev => prev + 1);
setCount(c => c + 1);  // equivalente

// Múltiplos updates na mesma função — batched em React 18+
setCount(c => c + 1);
setCount(c => c + 1);  // final: count + 2
```

### useEffect

Executa side effects após o render.

```tsx
// Sem dependency — roda após CADA render
useEffect(() => {
    console.log('runs on every render');
});

// Array vazio — roda uma vez (mount)
useEffect(() => {
    console.log('runs on mount');
    return () => console.log('runs on unmount');
}, []);

// Com dependências — roda quando dependency muda
useEffect(() => {
    fetch(`/api/users/${id}`).then(...);
}, [id]);

// Cleanup
useEffect(() => {
    const controller = new AbortController();

    fetch('/api/data', { signal: controller.signal })
        .then(r => r.json())
        .then(setData)
        .catch(err => {
            if (err.name !== 'AbortError') throw err;
        });

    return () => controller.abort();
}, []);
```

**Armadilhas clássicas:**

```tsx
// BUG — stale closure
function Counter() {
    const [count, setCount] = useState(0);

    useEffect(() => {
        const id = setInterval(() => setCount(count + 1), 1000);
        return () => clearInterval(id);
    }, []);  // count nunca atualiza — closure captura count=0

    return <div>{count}</div>;
}

// FIX — updater function
useEffect(() => {
    const id = setInterval(() => setCount(c => c + 1), 1000);
    return () => clearInterval(id);
}, []);  // não precisa de count no deps
```

**`useEffect` em Strict Mode:** React 18+ em strict mode roda effects **2x** em dev para detectar effects com side effects. Se seu effect quebra quando roda 2x, tem bug (falta de cleanup).

### useReducer

Alternativa a `useState` para lógica complexa.

```tsx
type State = { count: number; step: number };
type Action =
    | { type: 'increment' }
    | { type: 'decrement' }
    | { type: 'setStep'; step: number };

function reducer(state: State, action: Action): State {
    switch (action.type) {
        case 'increment': return { ...state, count: state.count + state.step };
        case 'decrement': return { ...state, count: state.count - state.step };
        case 'setStep':   return { ...state, step: action.step };
    }
}

function Counter() {
    const [state, dispatch] = useReducer(reducer, { count: 0, step: 1 });

    return (
        <>
            <p>{state.count}</p>
            <button onClick={() => dispatch({ type: 'increment' })}>+</button>
        </>
    );
}
```

**Quando usar useReducer vs useState:**

- **useState** — state simples, 1-2 valores, transições simples
- **useReducer** — múltiplos valores relacionados, transições complexas, testabilidade

### useContext

Compartilha dados entre componentes sem prop drilling.

```tsx
// Criar o context
const ThemeContext = createContext<'light' | 'dark'>('light');

// Provider
function App() {
    const [theme, setTheme] = useState<'light' | 'dark'>('light');
    return (
        <ThemeContext.Provider value={theme}>
            <Toolbar />
        </ThemeContext.Provider>
    );
}

// Consumer
function Toolbar() {
    const theme = useContext(ThemeContext);
    return <div className={theme}>...</div>;
}
```

**Cuidado:** Context re-renderiza TODOS os consumers quando o value muda. Não coloque estado que muda muito.

**Patterns:**

- **Split contexts** — user, theme, settings em contexts separados
- **Provider + custom hook:**

    ```tsx
    function useTheme() {
        const ctx = useContext(ThemeContext);
        if (!ctx) throw new Error('useTheme must be inside ThemeProvider');
        return ctx;
    }
    ```

### useRef

Referência mutável que não causa re-render.

```tsx
// Referência a elemento DOM
function TextInput() {
    const ref = useRef<HTMLInputElement>(null);

    const focus = () => ref.current?.focus();

    return <input ref={ref} />;
}

// Valor mutável sem re-render
function Timer() {
    const intervalRef = useRef<number | null>(null);

    useEffect(() => {
        intervalRef.current = setInterval(() => { ... }, 1000);
        return () => {
            if (intervalRef.current) clearInterval(intervalRef.current);
        };
    }, []);
}
```

### useMemo e useCallback

Memoization para evitar recálculos/recriação desnecessários.

```tsx
// useMemo — memoize valor computado
const filteredItems = useMemo(
    () => items.filter(item => item.active),
    [items]
);

// useCallback — memoize função
const handleClick = useCallback(() => {
    console.log(id);
}, [id]);
```

**Quando usar:**

- Cálculos caros
- Props estáveis para componentes memoized (React.memo)
- Dependencies de outros hooks

**Cuidado:** memoization tem custo. Aplicar em tudo deixa o código mais complicado **sem ganho**. Meça primeiro.

**Em React 19 com Compiler:** largely obsolete — compilador faz automaticamente.

### useLayoutEffect

Como useEffect, mas roda **sincronamente** após DOM update, antes do browser pintar. Use para medições de DOM.

```tsx
useLayoutEffect(() => {
    const rect = elementRef.current?.getBoundingClientRect();
    setHeight(rect?.height ?? 0);
}, []);
```

**Cuidado:** bloqueia o paint. Use com parcimônia.

### useTransition (React 18+)

Marca updates como "não urgentes".

```tsx
function SearchResults() {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState([]);
    const [isPending, startTransition] = useTransition();

    const handleChange = (e) => {
        setQuery(e.target.value);  // urgente
        startTransition(() => {
            setResults(expensiveSearch(e.target.value));  // não urgente
        });
    };

    return (
        <>
            <input value={query} onChange={handleChange} />
            {isPending && <Spinner />}
            <ResultsList results={results} />
        </>
    );
}
```

### useDeferredValue

Valor "atrasado" para filtros/searches pesados.

```tsx
function Search() {
    const [query, setQuery] = useState('');
    const deferredQuery = useDeferredValue(query);

    return (
        <>
            <input value={query} onChange={e => setQuery(e.target.value)} />
            <HeavyList query={deferredQuery} />
        </>
    );
}
```

### Custom hooks

Extraia lógica reutilizável em hooks custom. Convenção: começam com `use`.

```tsx
function useDebounce<T>(value: T, delay: number): T {
    const [debounced, setDebounced] = useState(value);

    useEffect(() => {
        const timer = setTimeout(() => setDebounced(value), delay);
        return () => clearTimeout(timer);
    }, [value, delay]);

    return debounced;
}

// Uso
function Search() {
    const [query, setQuery] = useState('');
    const debouncedQuery = useDebounce(query, 300);

    useEffect(() => {
        if (debouncedQuery) searchAPI(debouncedQuery);
    }, [debouncedQuery]);

    return <input value={query} onChange={e => setQuery(e.target.value)} />;
}
```

**Patterns comuns:**

- `useLocalStorage` — state persistido no localStorage
- `useMediaQuery` — responder a media queries
- `useFetch` — fetch com loading/error (melhor: React Query)
- `useClickOutside` — detectar clique fora de elemento
- `useKeyPress` — atalhos de teclado
- `useIntersectionObserver` — lazy loading, infinite scroll
- `useWindowSize` — dimensões da window

---

## State management

### Decisão — onde colocar o state

```
Escopo do state     →  Onde colocar
──────────────────────────────────────────
1 componente        →  useState local
Alguns componentes  →  lift state up
Vários componentes  →  Context (se não muda muito)
Global              →  Zustand / Redux / Jotai
Server state        →  React Query / SWR / tRPC
URL state           →  React Router / searchParams
Form state          →  React Hook Form
```

**Regra fundamental:** **server state não é client state**. Dados do servidor são cache local, não "estado" da aplicação.

### Lift state up

```tsx
// Compartilha state entre siblings pelo pai comum
function Parent() {
    const [filter, setFilter] = useState('');

    return (
        <>
            <SearchBar filter={filter} onChange={setFilter} />
            <ResultsList filter={filter} />
        </>
    );
}
```

### Zustand — state global simples

```tsx
import { create } from 'zustand';

interface CartStore {
    items: CartItem[];
    addItem: (item: CartItem) => void;
    removeItem: (id: string) => void;
    clear: () => void;
}

const useCart = create<CartStore>((set) => ({
    items: [],
    addItem: (item) => set((state) => ({ items: [...state.items, item] })),
    removeItem: (id) => set((state) => ({
        items: state.items.filter(i => i.id !== id)
    })),
    clear: () => set({ items: [] })
}));

// Uso
function Cart() {
    const items = useCart(state => state.items);
    const removeItem = useCart(state => state.removeItem);

    return (
        <ul>
            {items.map(item => (
                <li key={item.id}>
                    {item.name}
                    <button onClick={() => removeItem(item.id)}>Remove</button>
                </li>
            ))}
        </ul>
    );
}
```

**Por que Zustand em vez de Redux em 2026:**

- API minimalista, sem boilerplate (actions, reducers, selectors)
- Sem provider wrapping (opcional)
- TypeScript first-class
- Bundle pequeno (~1KB)
- Compatível com devtools

### Redux (legacy, ainda comum)

```tsx
// Redux Toolkit (forma moderna)
import { createSlice, configureStore } from '@reduxjs/toolkit';

const cartSlice = createSlice({
    name: 'cart',
    initialState: { items: [] },
    reducers: {
        addItem: (state, action) => {
            state.items.push(action.payload);  // Immer permite "mutação"
        },
        removeItem: (state, action) => {
            state.items = state.items.filter(i => i.id !== action.payload);
        }
    }
});

const store = configureStore({
    reducer: { cart: cartSlice.reducer }
});

// Uso em componentes
const items = useSelector(state => state.cart.items);
const dispatch = useDispatch();
dispatch(cartSlice.actions.addItem(item));
```

Em 2026, Redux ainda é comum em projetos legacy. Para novo código, **Zustand é mais simples**.

### Jotai — atomic state

```tsx
import { atom, useAtom } from 'jotai';

const countAtom = atom(0);

function Counter() {
    const [count, setCount] = useAtom(countAtom);
    return <button onClick={() => setCount(c => c + 1)}>{count}</button>;
}

// Derived atoms
const doubleCountAtom = atom(get => get(countAtom) * 2);
```

**Quando usar:** state com muita derivação, granular reactivity.

---

## Server state — React Query

**O maior ganho de produtividade em React dos últimos anos.** React Query (agora `@tanstack/react-query`) gerencia cache, refetch, invalidation, background updates — tudo que você faria manualmente.

```tsx
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

function UserProfile({ id }) {
    const { data: user, isLoading, error } = useQuery({
        queryKey: ['user', id],
        queryFn: () => fetch(`/api/users/${id}`).then(r => r.json()),
        staleTime: 5 * 60 * 1000,  // 5 minutos
        gcTime: 10 * 60 * 1000     // 10 minutos em cache
    });

    if (isLoading) return <Spinner />;
    if (error) return <ErrorMessage />;

    return <h1>{user.name}</h1>;
}
```

### Mutations

```tsx
function EditUser({ user }) {
    const queryClient = useQueryClient();

    const mutation = useMutation({
        mutationFn: (updated) => fetch(`/api/users/${user.id}`, {
            method: 'PUT',
            body: JSON.stringify(updated)
        }),
        onSuccess: () => {
            // Invalida cache, força refetch
            queryClient.invalidateQueries({ queryKey: ['user', user.id] });
        }
    });

    return (
        <form onSubmit={(e) => {
            e.preventDefault();
            mutation.mutate({ name: 'New name' });
        }}>
            <button disabled={mutation.isPending}>Save</button>
        </form>
    );
}
```

### Features

- **Cache automático** — mesmo query key reutiliza dados
- **Refetch on focus** — dados atualizados quando tab volta ao foco
- **Refetch on reconnect** — ao recuperar conexão
- **Stale-while-revalidate** — mostra cached, refetch em background
- **Optimistic updates** — UI atualiza antes do server confirmar
- **Infinite queries** — paginação e scroll infinito
- **Prefetching** — carregar antes de precisar
- **Paralelismo** — múltiplas queries em paralelo automaticamente

### Alternativas

- **SWR** — menor, da Vercel. API similar.
- **Apollo Client** — para GraphQL
- **tRPC** — para APIs typesafe end-to-end
- **Relay** — GraphQL, da Meta

**Em 2026, React Query é o default para REST. tRPC cresceu muito em stacks TS-only.**

---

## Rendering e Reconciliation

### Virtual DOM

React mantém uma representação do DOM em memória (Virtual DOM ou Fiber tree). Quando o state muda:

1. React gera nova árvore
2. Compara com árvore anterior (**diffing**)
3. Calcula **mínimas mudanças** no DOM real
4. Aplica as mudanças

### Reconciliation — o algoritmo

React usa 3 heuristics para diffing rápido:

1. **Elementos de tipos diferentes → substituir completo**

    ```tsx
    // Re-cria árvore inteira
    <div><Counter /></div>  →  <span><Counter /></span>
    ```

2. **Mesmo tipo de elemento → atualizar props**

    ```tsx
    <div className="before" />  →  <div className="after" />
    // React só muda className
    ```

3. **Listas → comparar por `key`**

    ```tsx
    {items.map(item => <Item key={item.id} data={item} />)}
    ```

### Fiber architecture

Desde React 16, o algoritmo de rendering é **interruptible** — React pode pausar trabalho e continuar depois. Permite:

- **Priorização** — updates urgentes primeiro
- **Suspense** — pausar render enquanto dados carregam
- **Concurrent features** — transitions, deferred values

### When components re-render

Um componente re-renderiza quando:

1. **Seu state muda** (via setState, dispatch)
2. **Suas props mudam** (pai re-renderizou e passou novas)
3. **Context que ele consome muda**
4. **Pai re-renderiza** — mesmo sem mudanças, filho re-renderiza (a menos que memoized)

**Não re-renderiza:**

- Mutação direta de objeto (`obj.field = x`) — use imutável
- Ref change (`ref.current = x`)

### Evitando re-renders desnecessários

**1. React.memo — componentes**

```tsx
const ExpensiveList = memo(function List({ items }) {
    // só re-renderiza se items mudar (shallow compare)
    return items.map(i => <Item key={i.id} {...i} />);
});
```

**Custom compare:**

```tsx
const Component = memo(MyComponent, (prev, next) => {
    return prev.id === next.id;  // true = SKIP render
});
```

**2. useMemo — valores**

```tsx
const sortedItems = useMemo(
    () => items.toSorted((a, b) => a.name.localeCompare(b.name)),
    [items]
);
```

**3. useCallback — funções**

```tsx
const handleClick = useCallback(() => {
    doSomething(id);
}, [id]);

// Importante quando passar como prop para componente memoized
<MemoChild onClick={handleClick} />
```

**Em React 19 com Compiler:** tudo isso é automático.

### Profiler

```tsx
import { Profiler } from 'react';

<Profiler id="App" onRender={(id, phase, actualDuration) => {
    console.log(`${id} [${phase}] took ${actualDuration}ms`);
}}>
    <App />
</Profiler>
```

**React DevTools** tem Profiler UI — grava interações, mostra qual componente causou re-render, quanto tempo levou.

---

## Formulários

### Controlled vs Uncontrolled

**Controlled** — state React é a source of truth:

```tsx
function ControlledForm() {
    const [name, setName] = useState('');

    return (
        <input
            value={name}
            onChange={(e) => setName(e.target.value)}
        />
    );
}
```

**Uncontrolled** — DOM é a source of truth:

```tsx
function UncontrolledForm() {
    const ref = useRef<HTMLInputElement>(null);

    const handleSubmit = () => {
        console.log(ref.current?.value);
    };

    return <input ref={ref} defaultValue="" />;
}
```

**Quando usar cada:**

- **Controlled** — validação em tempo real, condicional render baseado em value
- **Uncontrolled** — forms simples, performance (sem re-render em cada keystroke)

### React Hook Form — o padrão moderno

Em 2026, **React Hook Form** é o default para formulários não triviais. Uncontrolled por default (performance), validação via schema.

```tsx
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const schema = z.object({
    email: z.string().email(),
    password: z.string().min(8),
    age: z.number().int().positive()
});

type FormData = z.infer<typeof schema>;

function LoginForm() {
    const {
        register,
        handleSubmit,
        formState: { errors, isSubmitting }
    } = useForm<FormData>({
        resolver: zodResolver(schema)
    });

    const onSubmit = async (data: FormData) => {
        await login(data);
    };

    return (
        <form onSubmit={handleSubmit(onSubmit)}>
            <input {...register('email')} type="email" />
            {errors.email && <p>{errors.email.message}</p>}

            <input {...register('password')} type="password" />
            {errors.password && <p>{errors.password.message}</p>}

            <input {...register('age', { valueAsNumber: true })} type="number" />
            {errors.age && <p>{errors.age.message}</p>}

            <button disabled={isSubmitting}>Submit</button>
        </form>
    );
}
```

**Vantagens:**

- Performance (uncontrolled, sem re-render por keystroke)
- Validação via Zod (type-safe)
- Error handling robusto
- TypeScript first-class

### TanStack Form

Nova entrada em 2025 — similar a React Hook Form mas com foco em TypeScript e agnóstico de framework.

---

## Router

### React Router 7 (2026)

```tsx
import { createBrowserRouter, RouterProvider, Link, Outlet, useParams } from 'react-router-dom';

const router = createBrowserRouter([
    {
        path: '/',
        element: <Layout />,
        children: [
            { index: true, element: <Home /> },
            { path: 'about', element: <About /> },
            {
                path: 'users/:id',
                element: <UserProfile />,
                loader: async ({ params }) => {
                    return await fetch(`/api/users/${params.id}`);
                }
            },
            { path: '*', element: <NotFound /> }
        ]
    }
]);

function App() {
    return <RouterProvider router={router} />;
}

function UserProfile() {
    const { id } = useParams();
    return <h1>User {id}</h1>;
}
```

### TanStack Router

Alternativa type-safe ao React Router. Crescendo rápido em 2026.

```tsx
import { createRouter, createRoute } from '@tanstack/react-router';

const userRoute = createRoute({
    getParentRoute: () => rootRoute,
    path: 'users/$id',
    component: UserProfile,
    loader: ({ params }) => fetchUser(params.id),
    validateSearch: z.object({ tab: z.enum(['info', 'posts']) })
});
```

**Vantagens:** type-safe URL params e search params, inference end-to-end.

---

## Arquitetura de projeto

### Feature-based structure

```
src/
├── features/
│   ├── auth/
│   │   ├── components/
│   │   │   ├── LoginForm.tsx
│   │   │   └── SignupForm.tsx
│   │   ├── hooks/
│   │   │   └── useAuth.ts
│   │   ├── api/
│   │   │   └── authApi.ts
│   │   └── index.ts
│   └── patients/
│       ├── components/
│       ├── hooks/
│       ├── api/
│       └── index.ts
├── shared/
│   ├── ui/                # componentes genéricos (Button, Card, Modal)
│   ├── hooks/             # hooks genéricos
│   └── lib/               # utilities
├── app/                   # ou pages/
│   ├── routes.tsx
│   └── layouts/
└── main.tsx
```

**Vantagens vs "by type" (components/, services/, etc.):**

- Mudanças de feature ficam num só diretório
- Fácil mover ou deletar features
- Limites claros entre features

### Container vs Presentational (classic pattern)

```tsx
// Container — smart, lida com state e data
function UserListContainer() {
    const { data: users, isLoading } = useQuery({
        queryKey: ['users'],
        queryFn: fetchUsers
    });

    if (isLoading) return <Spinner />;
    return <UserList users={users} />;
}

// Presentational — dumb, só renderiza props
function UserList({ users }: { users: User[] }) {
    return (
        <ul>
            {users.map(u => <UserCard key={u.id} user={u} />)}
        </ul>
    );
}
```

**Em 2026:** menos rígido. Com hooks, separação é natural via custom hooks em vez de componentes dedicados.

---

## Performance

### Identificando problemas

**React DevTools Profiler** é a primeira ferramenta:

1. Record interação
2. Ver flame graph de renders
3. Identificar componentes caros ou re-renders desnecessários

**Web Vitals:**

- **LCP** (Largest Contentful Paint) — < 2.5s
- **FID/INP** (Interaction to Next Paint) — < 200ms
- **CLS** (Cumulative Layout Shift) — < 0.1

### Otimizações

**1. Code splitting**

```tsx
const HeavyComponent = lazy(() => import('./HeavyComponent'));

function App() {
    return (
        <Suspense fallback={<Spinner />}>
            <HeavyComponent />
        </Suspense>
    );
}
```

**2. List virtualization** — render só visível

```tsx
import { useVirtualizer } from '@tanstack/react-virtual';

function BigList({ items }) {
    const parentRef = useRef(null);

    const virtualizer = useVirtualizer({
        count: items.length,
        getScrollElement: () => parentRef.current,
        estimateSize: () => 35
    });

    return (
        <div ref={parentRef} style={{ height: '400px', overflow: 'auto' }}>
            <div style={{ height: virtualizer.getTotalSize() }}>
                {virtualizer.getVirtualItems().map(virtualRow => (
                    <div
                        key={virtualRow.index}
                        style={{
                            position: 'absolute',
                            top: virtualRow.start,
                            height: virtualRow.size
                        }}
                    >
                        {items[virtualRow.index].name}
                    </div>
                ))}
            </div>
        </div>
    );
}
```

**3. React.memo, useMemo, useCallback** — ver seção anterior

**4. Image optimization**

```tsx
// Next.js
import Image from 'next/image';
<Image src="/hero.jpg" width={1200} height={600} alt="Hero" priority />

// Vite/SPA — use srcset e lazy loading
<img
    src="/image.jpg"
    srcSet="/image-400.jpg 400w, /image-800.jpg 800w"
    sizes="(max-width: 600px) 400px, 800px"
    loading="lazy"
    alt="..."
/>
```

**5. Bundle analysis**

```bash
# Vite
npx vite-bundle-visualizer

# webpack
npm install -D webpack-bundle-analyzer
```

### Web Workers para CPU heavy

```tsx
// worker.ts
self.addEventListener('message', (e) => {
    const result = heavyComputation(e.data);
    self.postMessage(result);
});

// Component
const worker = useMemo(() => new Worker(new URL('./worker.ts', import.meta.url)), []);

useEffect(() => {
    worker.onmessage = (e) => setResult(e.data);
    return () => worker.terminate();
}, [worker]);

worker.postMessage(data);
```

---

## Suspense e Concurrent features

### Suspense

```tsx
<Suspense fallback={<Spinner />}>
    <LazyComponent />
</Suspense>
```

Suspende até o componente estar pronto (code loaded, data fetched).

### Error boundaries

```tsx
class ErrorBoundary extends React.Component<
    { children: React.ReactNode; fallback: React.ReactNode },
    { hasError: boolean }
> {
    state = { hasError: false };

    static getDerivedStateFromError() {
        return { hasError: true };
    }

    componentDidCatch(error, info) {
        console.error(error, info);
    }

    render() {
        if (this.state.hasError) return this.props.fallback;
        return this.props.children;
    }
}

// Uso
<ErrorBoundary fallback={<ErrorMessage />}>
    <App />
</ErrorBoundary>
```

**Limitação:** não pega erros em:

- Event handlers (use try/catch)
- Async code (use .catch ou try/catch)
- SSR
- Erros no próprio error boundary

**`react-error-boundary`** — biblioteca popular com API baseada em hooks.

---

## Meta-frameworks

### Next.js

```tsx
// app/users/[id]/page.tsx
async function UserPage({ params }: { params: { id: string } }) {
    const user = await fetchUser(params.id);  // Server Component
    return <UserProfile user={user} />;
}
```

**Features:**

- App Router com Server Components (default em 14+)
- Server Actions
- API routes
- Image optimization
- Turbopack (default em 16)
- Deployment otimizado para Vercel (e outros)

**Em 2026, Next.js 16 com Turbopack é o default** para apps React em produção.

### Remix / React Router 7

Framework fullstack focado em web standards. Se fundiu com React Router em 2024-2025.

### Astro

Static-first, JS mínimo. Bom para blogs, docs, sites de marketing. Suporta React "islands" (interatividade pontual).

### TanStack Start

Framework fullstack novo em 2026, TanStack router + Start. Type-safe end-to-end.

---

## Testing

Deep dive em [[Testes em JavaScript]]. Resumo:

```tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect } from 'vitest';
import { LoginForm } from './LoginForm';

describe('LoginForm', () => {
    it('should submit with valid data', async () => {
        const user = userEvent.setup();
        const onSubmit = vi.fn();

        render(<LoginForm onSubmit={onSubmit} />);

        await user.type(screen.getByLabelText(/email/i), 'maria@test.com');
        await user.type(screen.getByLabelText(/password/i), 'secret');
        await user.click(screen.getByRole('button', { name: /log in/i }));

        expect(onSubmit).toHaveBeenCalledWith({
            email: 'maria@test.com',
            password: 'secret'
        });
    });
});
```

---

## Armadilhas comuns

- **Stale closures em useEffect** — use updater functions ou adicione ao deps
- **Missing dependencies no useEffect** — eslint plugin pega
- **useEffect com setInterval sem cleanup** — vazamento
- **Key como index** — problemas em listas que reordenam
- **Mutação direta de state** — `state.push(x)`. Use spread ou bibliotecas como Immer.
- **Context para state que muda muito** — re-renders em massa
- **Re-criar funções/objetos em cada render sem memo** — passa novas props para filhos memoized
- **Otimizar sem medir** — memo/useMemo/useCallback em tudo deixa código complexo
- **useState para server state** — use React Query
- **`{condition && <Component />}` com 0** — renderiza '0'
- **Async no useEffect diretamente** — useEffect não aceita async function
- **Esquecer cleanup em useEffect** — subscriptions, timers, fetch
- **Re-render loop** — setState no render sem condição
- **Props drilling** — profundo demais, use Context ou state management
- **Strict mode quebrando effects** — effects devem ser idempotentes
- **Forms controlled gigantes** — re-render em cada keystroke. Use React Hook Form.
- **`useMemo` sem dependência correta** — valor stale
- **ForwardRef confuso** — em React 19, ref é prop normal
- **`defaultProps` em function components** — removido em React 19, use destructuring defaults
- **Importar diretamente de `react`** sem necessidade — dead imports
- **Esquecer `'use client'`** em Server Components com hooks

---

## Na prática (da minha experiência)

> **Stack do MedEspecialista frontend:**
>
> **1. React 19 + Next.js 16** (App Router, Server Components default)
> **2. TypeScript estrito** desde o dia 1
> **3. Tailwind CSS** para estilos
> **4. React Hook Form + Zod** para formulários
> **5. React Query** para server state
> **6. Zustand** para client state global (pequeno)
> **7. shadcn/ui** como base de componentes
> **8. Vitest + Testing Library + MSW** para testes
> **9. Playwright** para E2E
> **10. Storybook** para desenvolvimento de componentes
>
> **Patterns que padronizei:**
>
> **1. Feature-based folders** — cada feature é auto-contida
>
> **2. Hooks customizados para lógica de domínio** — componentes ficam "burros", hooks têm a lógica
>
> ```tsx
> function usePatient(id: string) {
>     return useQuery({
>         queryKey: ['patient', id],
>         queryFn: () => api.getPatient(id)
>     });
> }
> ```
>
> **3. Server Components first, Client opt-in** — `'use client'` só quando preciso de estado/efeito
>
> **4. Zod schemas compartilhados backend/frontend** — validação idêntica nos dois lados
>
> **5. Error boundaries por feature** — erro em uma não derruba tudo
>
> **6. Suspense + React Query** — loading states declarativos
>
> **7. TanStack Virtual** para listas grandes — tabelas de 10k+ pacientes
>
> **Incidente memorável — stale closure em useEffect:**
>
> Notification bell tinha polling a cada 30s. State dos notifications não atualizava — stale closure clássico. Fix:
>
> ```tsx
> // Antes (bug)
> useEffect(() => {
>     const id = setInterval(() => {
>         fetchNotifications().then(newOnes => setAll([...all, ...newOnes]));
>     }, 30000);
>     return () => clearInterval(id);
> }, []);  // all nunca atualiza
>
> // Fix
> useEffect(() => {
>     const id = setInterval(() => {
>         fetchNotifications().then(newOnes => setAll(prev => [...prev, ...newOnes]));
>     }, 30000);
>     return () => clearInterval(id);
> }, []);
> ```
>
> Melhor ainda: React Query com `refetchInterval`. Substituí todo polling manual por queries automaticamente.
>
> **Outro incidente — Context causando re-renders globais:**
>
> UserContext armazenava `{ user, setUser, preferences, setPreferences, ... }`. Qualquer mudança em qualquer campo re-renderizava a app inteira (1000+ componentes). Solução: split em 3 contexts separados (UserContext, PreferencesContext, ThemeContext) + Zustand para state com updates frequentes.
>
> **A lição principal:** React é simples conceitualmente, mas produtivo exige patterns — server state separado de client state, hooks custom para reutilização, memoization consciente (ou React Compiler), Suspense para loading, error boundaries para resiliência. Domine o modelo mental (componentes, reconciliation, hooks) e o resto é prática.

---

## How to explain in English

> "React is a library for building UIs through composable components. In 2026, I use React 19 with Next.js 16 and the App Router, which makes Server Components the default. The mental shift is significant — components that don't need interactivity run on the server, have direct database access, and ship zero JavaScript to the client. I only add `'use client'` when I actually need state, effects, or browser APIs.
>
> For state management, my rule is: server state is not client state. I use React Query for anything that comes from an API — it handles caching, refetch, invalidation, and optimistic updates. For global client state, Zustand is my default because it's minimal and type-safe. For URL state, the router. For form state, React Hook Form with Zod resolvers.
>
> The hooks I use most are useState, useEffect, and custom hooks that encapsulate feature logic. I follow Rules of Hooks strictly with the ESLint plugin. With React 19 Compiler becoming stable, I'm dropping most manual memoization — the compiler handles it automatically as long as I follow Rules of React.
>
> For performance, I measure before optimizing. React DevTools Profiler is my first tool. Common wins: list virtualization for large datasets, code splitting for routes, proper key usage in lists, and avoiding unnecessary Context re-renders by splitting contexts by concern.
>
> For testing, I use Vitest with React Testing Library and MSW for component and integration tests, and Playwright for end-to-end. The philosophy is test what users see, not implementation details. I use `getByRole` as the primary query because it aligns with accessibility.
>
> Common pitfalls I watch for: stale closures in useEffect, mutation of state objects, Context causing unnecessary re-renders, forgetting cleanup in effects, and using useState for server state when React Query is the right tool."

### Frases úteis em entrevista

- "Server state is not client state — React Query for one, Zustand for the other."
- "I start with Server Components, add `'use client'` only when necessary."
- "Stale closures are the classic bug in useEffect — fix with updater functions or correct deps."
- "React Compiler in React 19 makes most manual memoization obsolete."
- "I use `getByRole` as my primary query in Testing Library — accessibility-aligned."
- "Performance: measure first with Profiler, optimize second."
- "Feature-based folder structure, not by type."
- "Zod schemas shared between backend and frontend — single source of validation truth."
- "Error boundaries isolate failures — one feature crashing doesn't kill the app."
- "Forms: React Hook Form uncontrolled + Zod, not useState for every field."

### Key vocabulary

- componente → component
- renderização → rendering
- reconciliação → reconciliation
- estado → state
- propriedades → props
- gancho → hook
- efeito colateral → side effect
- montagem / desmontagem → mount / unmount
- memoização → memoization
- lazy loading → lazy loading
- suspensão → suspense
- limite de erro → error boundary
- componente de servidor → server component
- componente de cliente → client component
- ação de servidor → server action
- fechamento obsoleto → stale closure
- controlado / não controlado → controlled / uncontrolled
- elevação de estado → lift state up
- prop drilling → prop drilling
- virtualização → virtualization
- divisão de código → code splitting

---

## Recursos

### Documentação

- [React Docs](https://react.dev/) — nova docs (substitui reactjs.org)
- [Next.js Docs](https://nextjs.org/docs)
- [React Router](https://reactrouter.com/)
- [TanStack Query](https://tanstack.com/query/latest)
- [TanStack Router](https://tanstack.com/router/latest)

### Livros e cursos

- [React.dev tutorial](https://react.dev/learn) — oficial, bem escrito
- [Full Stack Open](https://fullstackopen.com/en/) — partes 1, 2, 5, 6, 7 sobre React
- [Epic React](https://epicreact.dev/) — Kent C. Dodds, pago mas excelente
- [React Patterns](https://reactpatterns.com/)

### Blogs essenciais

- [overreacted.io](https://overreacted.io/) — Dan Abramov, profundo
- [Josh Comeau](https://www.joshwcomeau.com/) — tutorials visuais ótimos
- [Kent C. Dodds](https://kentcdodds.com/) — Testing Library, hooks, patterns
- [Robin Wieruch](https://www.robinwieruch.de/)
- [Rodrigo Pombo](https://pomb.us/)

### Ferramentas

- [React DevTools](https://react.dev/learn/react-developer-tools) — essencial
- [shadcn/ui](https://ui.shadcn.com/) — componentes copy-paste baseados em Radix
- [Radix UI](https://www.radix-ui.com/) — componentes acessíveis unstyled
- [Headless UI](https://headlessui.com/)
- [Tailwind CSS](https://tailwindcss.com/)
- [React Hook Form](https://react-hook-form.com/)
- [Zod](https://zod.dev/)
- [Framer Motion](https://www.framer.com/motion/) — animações
- [TanStack Table](https://tanstack.com/table/latest) — tabelas complexas
- [TanStack Virtual](https://tanstack.com/virtual/latest) — virtualization
- [Storybook](https://storybook.js.org/)

### Newsletters

- [This Week in React](https://thisweekinreact.com/)
- [React Status](https://react.statuscode.com/)
- [Bytes](https://bytes.dev/)

---

## Veja também

- [[JavaScript Fundamentals]] — linguagem base
- [[TypeScript]] — tipagem em React
- [[TypeScript com React]] — trilha completa sobre tipagem em React (mental model, idiomas práticos, type-level avançado)
- [[Testes em JavaScript]] — Testing Library, Playwright
- [[HTML e CSS]] — fundação do frontend
- [[Node.js]] — backend para React
- [[Full Stack Open - Guia de Revisão]] — curso da Universidade de Helsinki
- [[API Design]] — consumindo APIs em React
- [[Arquitetura de Software]] — patterns arquiteturais
- [[System Design]] — React em system design
