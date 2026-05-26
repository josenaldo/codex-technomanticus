---
title: "TypeScript"
created: 2026-04-01
updated: 2026-04-11
type: concept
status: evergreen
tags:
  - javascript
  - typescript
  - entrevista
publish: false
---

# TypeScript

Deep dive em **TypeScript** — sistema de tipos estáticos para JavaScript. Para fundamentos da linguagem base, ver [[JavaScript Fundamentals]]. Para React com TypeScript, ver [[React]]. Para testes com TS, ver [[Testes em JavaScript]].

## O que é

TypeScript é um **superset tipado** de JavaScript criado pela Microsoft (2012, Anders Hejlsberg — criador do C#). Adiciona **tipos estáticos opcionais** ao JavaScript, compilando para JS puro (ou, desde Node 22.18+, rodando nativamente via type stripping).

**Em 2026:**

- **#1 linguagem no GitHub** (ultrapassou JavaScript)
- **TypeScript 7** lançamento previsto mid-2026, com compilador reescrito em Go (10x mais rápido)
- **Node 22+ suporta TS nativamente** via `--experimental-strip-types`
- **Default em novos projetos** JavaScript sérios

**Por que TypeScript:**

- **Erros detectados em compile time**, não em runtime
- **IDE intelligence** — autocomplete, rename refactoring, go-to-definition
- **Documentação viva** — tipos são docs que nunca desatualizam
- **Refactoring seguro** — o compilador avisa onde você quebrou coisas
- **Contrato entre camadas** — backend → OpenAPI → frontend com tipos gerados

Em entrevistas, o que diferencia um senior em TypeScript:

1. **Structural typing** — por que duck typing funciona em TS
2. **Type narrowing** — como TS "aprende" o tipo em runtime via type guards
3. **Generics avançados** — constraints, defaults, inference, conditional types
4. **Utility types e Mapped types** — `Partial`, `Pick`, `Omit`, e criar os seus
5. **`unknown` vs `any` vs `never`** — semântica precisa
6. **Discriminated unions** — patterns para state machines e Result types
7. **Strict mode flags** — `strict: true` não é suficiente
8. **Type-level programming** — template literal types, infer, recursive types
9. **Declaration files** — `.d.ts`, DefinitelyTyped, ambient declarations
10. **Module resolution** — `paths`, `baseUrl`, ESM vs CJS em TS

---

## TypeScript vs JavaScript

### Structural typing

TypeScript usa **structural typing** (duck typing): se dois tipos têm a mesma forma, são compatíveis.

```typescript
type Point = { x: number; y: number };
type Coord = { x: number; y: number; z?: number };

function print(p: Point) { }

const c: Coord = { x: 1, y: 2 };
print(c);  // OK — Coord tem pelo menos as propriedades de Point
```

Isso é **diferente de Java/C#** (nominal typing), onde dois tipos com a mesma estrutura mas nomes diferentes são incompatíveis.

### Excess property checking

Literais de objeto passados diretamente são verificados estritamente:

```typescript
print({ x: 1, y: 2, z: 3 });  // ERRO — z não está em Point
```

Mas se passar via variável, o check é relaxado:

```typescript
const obj = { x: 1, y: 2, z: 3 };
print(obj);  // OK — structural match
```

---

## Tipos básicos

```typescript
// Primitivos
let nome: string = 'Maria';
let idade: number = 30;
let ativo: boolean = true;
let nada: null = null;
let indefinido: undefined = undefined;
let big: bigint = 42n;
let sym: symbol = Symbol('id');

// Arrays
let numeros: number[] = [1, 2, 3];
let nomes: Array<string> = ['a', 'b'];  // sintaxe alternativa

// Tuples
let par: [string, number] = ['Maria', 30];
let comOpcional: [string, number?] = ['Maria'];
let comRest: [string, ...number[]] = ['Maria', 1, 2, 3];
let nomeado: [first: string, last: string] = ['Ana', 'Silva'];

// Objetos
let user: { nome: string; idade: number } = { nome: 'Maria', idade: 30 };

// any — desliga a verificação (evite)
let qualquer: any = 'anything';

// unknown — precisa narrowing antes de usar
let desconhecido: unknown = 'hello';
// desconhecido.toUpperCase();  // ERRO
if (typeof desconhecido === 'string') {
    desconhecido.toUpperCase();  // OK — narrowed
}

// never — nunca acontece (funções que lançam, loops infinitos)
function fail(msg: string): never {
    throw new Error(msg);
}

// void — função sem retorno
function log(msg: string): void {
    console.log(msg);
}
```

### any vs unknown vs never

| | `any` | `unknown` | `never` |
| --- | --- | --- | --- |
| Aceita qualquer valor | ✅ | ✅ | ❌ |
| Pode ser atribuído a qualquer tipo | ✅ | ❌ (só any/unknown) | ✅ |
| Permite qualquer operação | ✅ | ❌ (precisa narrowing) | N/A |
| Uso | **evite** | input não confiável | casos impossíveis |

**Regra:** substitua `any` por `unknown` sempre que possível. `unknown` força você a verificar o tipo antes de usar.

---

## Interfaces e Type aliases

Ambos definem formas. Diferenças:

```typescript
// Interface
interface User {
    name: string;
    age: number;
}

// Type alias
type UserType = {
    name: string;
    age: number;
};
```

### Quando usar interface

- Definir **formas de objetos** que outras partes podem estender
- **Declaration merging** — útil para estender tipos de bibliotecas

```typescript
interface User {
    name: string;
}
interface User {
    age: number;  // merged — User agora tem name + age
}

// Exemplo real — estender window
declare global {
    interface Window {
        myApp: { version: string };
    }
}
```

### Quando usar type

- **Unions e intersections**
- **Tuples**
- **Mapped types**
- **Template literal types**
- **Primitivos renomeados**

```typescript
type Status = 'active' | 'inactive' | 'pending';
type Point = [number, number];
type UserId = string;
type Keys = keyof User;
```

### Regra prática

Use `interface` para "shapes" (APIs públicas, objetos); `type` para tudo mais (unions, utility-driven, etc.). Inconsistência aqui importa menos que outras decisões.

### Extending

```typescript
// Interface extends
interface Animal { name: string; }
interface Dog extends Animal {
    breed: string;
}

// Type intersection
type Animal2 = { name: string };
type Dog2 = Animal2 & { breed: string };

// Interface extends type
type Named = { name: string };
interface Labeled extends Named {
    label: string;
}
```

---

## Union e Intersection types

### Union types (`|`)

```typescript
type ID = string | number;

function format(id: ID): string {
    if (typeof id === 'string') {
        return id.toUpperCase();  // narrowed para string
    }
    return id.toString();  // narrowed para number
}
```

### Intersection types (`&`)

```typescript
type Named = { name: string };
type Aged = { age: number };
type Person = Named & Aged;

const p: Person = { name: 'Maria', age: 30 };
```

**Cuidado com conflitos:**

```typescript
type A = { x: string };
type B = { x: number };
type C = A & B;  // x: never — intersecção impossível
```

### Discriminated unions — o pattern mais importante

```typescript
type Result<T> =
    | { success: true; data: T }
    | { success: false; error: string };

function handle<T>(result: Result<T>): T {
    if (result.success) {
        return result.data;  // narrowed para { success: true; data: T }
    } else {
        throw new Error(result.error);  // narrowed para { success: false; error: string }
    }
}
```

**Uso em state machines:**

```typescript
type LoadingState =
    | { status: 'idle' }
    | { status: 'loading' }
    | { status: 'success'; data: User }
    | { status: 'error'; error: string };

function render(state: LoadingState) {
    switch (state.status) {
        case 'idle':    return 'Waiting...';
        case 'loading': return 'Loading...';
        case 'success': return `Hello, ${state.data.name}`;
        case 'error':   return `Error: ${state.error}`;
    }
}
```

**Exhaustiveness checking:**

```typescript
function render(state: LoadingState): string {
    switch (state.status) {
        case 'idle':    return '...';
        case 'loading': return '...';
        case 'success': return '...';
        // Falta 'error'
        default:
            const _exhaustive: never = state;  // ERRO — state é LoadingState<error>
            return _exhaustive;
    }
}
```

---

## Type narrowing

TypeScript usa **control flow analysis** para restringir tipos baseado em checks em runtime.

### typeof guards

```typescript
function process(value: string | number) {
    if (typeof value === 'string') {
        return value.toUpperCase();  // string
    }
    return value.toFixed(2);  // number
}
```

### instanceof guards

```typescript
function logError(err: Error | string) {
    if (err instanceof Error) {
        console.log(err.stack);  // Error
    } else {
        console.log(err);  // string
    }
}
```

### in operator

```typescript
type Cat = { meow: () => void };
type Dog = { bark: () => void };

function speak(animal: Cat | Dog) {
    if ('meow' in animal) {
        animal.meow();  // Cat
    } else {
        animal.bark();  // Dog
    }
}
```

### Discriminant property

```typescript
type Shape =
    | { kind: 'circle'; radius: number }
    | { kind: 'square'; side: number };

function area(s: Shape): number {
    switch (s.kind) {
        case 'circle': return Math.PI * s.radius ** 2;
        case 'square': return s.side ** 2;
    }
}
```

### Custom type guards (user-defined)

```typescript
interface Cat { meow: () => void; }
interface Dog { bark: () => void; }

function isCat(animal: Cat | Dog): animal is Cat {
    return 'meow' in animal;
}

function speak(animal: Cat | Dog) {
    if (isCat(animal)) {
        animal.meow();  // TS sabe que é Cat
    } else {
        animal.bark();  // TS sabe que é Dog
    }
}
```

### Assertion functions (TS 3.7+)

```typescript
function assertDefined<T>(x: T | undefined): asserts x is T {
    if (x === undefined) throw new Error('undefined!');
}

function process(user?: User) {
    assertDefined(user);
    console.log(user.name);  // TS sabe que user é User
}
```

### Non-null assertion (`!`)

```typescript
const user = users.find(u => u.id === id)!;  // força não-null
// Use com cuidado — você promete ao compilador que não é null
```

**Regra:** `!` é um "confio em mim" — evite quando possível. Prefira narrowing explícito.

---

## Generics

Tipos parametrizados — funções e tipos que trabalham com múltiplos tipos.

### Funções genéricas

```typescript
function identity<T>(value: T): T {
    return value;
}

identity<string>('hello');  // explicit
identity(42);               // inferred como number

// Multi-parâmetros
function pair<A, B>(a: A, b: B): [A, B] {
    return [a, b];
}

const p = pair('Maria', 30);  // [string, number]
```

### Constraints

```typescript
interface HasLength {
    length: number;
}

function longer<T extends HasLength>(a: T, b: T): T {
    return a.length >= b.length ? a : b;
}

longer('hello', 'world');       // OK — string tem length
longer([1, 2], [3, 4, 5]);      // OK — array tem length
// longer(1, 2);                 // ERRO — number não tem length
```

### Default generic types

```typescript
function create<T = string>(value: T): T[] {
    return [value];
}

create(42);             // T = number
create('hello');        // T = string
create();               // T = string (default)
```

### Generic classes

```typescript
class Stack<T> {
    private items: T[] = [];

    push(item: T): void {
        this.items.push(item);
    }

    pop(): T | undefined {
        return this.items.pop();
    }

    peek(): T | undefined {
        return this.items[this.items.length - 1];
    }

    get size(): number {
        return this.items.length;
    }
}

const s = new Stack<number>();
s.push(1);
s.push(2);
s.pop();  // 2
```

### Generic interfaces

```typescript
interface Repository<T, ID = string> {
    findById(id: ID): Promise<T | null>;
    save(entity: T): Promise<T>;
    delete(id: ID): Promise<void>;
}

interface UserRepository extends Repository<User, number> {
    findByEmail(email: string): Promise<User | null>;
}
```

### Conditional types

```typescript
type IsString<T> = T extends string ? true : false;

type A = IsString<'hello'>;  // true
type B = IsString<42>;        // false

// Extrair tipo de array
type ElementOf<T> = T extends (infer U)[] ? U : never;

type Str = ElementOf<string[]>;  // string
type Num = ElementOf<number[]>;  // number

// Distributive conditional types
type ToArray<T> = T extends any ? T[] : never;
type Mixed = ToArray<string | number>;  // string[] | number[]
```

### Infer

Extrai tipos de dentro de outros:

```typescript
// Extrair tipo de retorno de função
type ReturnOf<T> = T extends (...args: any[]) => infer R ? R : never;

type R = ReturnOf<() => Promise<User>>;  // Promise<User>

// Extrair tipo de Promise
type Awaited<T> = T extends Promise<infer U> ? U : T;

type A = Awaited<Promise<string>>;  // string
type B = Awaited<Promise<Promise<number>>>;  // Promise<number> (não recursivo)
```

---

## Utility types

TypeScript inclui vários utility types. Os mais importantes:

### Partial, Required, Readonly

```typescript
interface User {
    id: number;
    name: string;
    email: string;
}

// Todos os campos opcionais
type UserUpdate = Partial<User>;
// { id?: number; name?: string; email?: string }

// Todos os campos obrigatórios (remove optional)
type RequiredUser = Required<UserUpdate>;

// Todos readonly
type FrozenUser = Readonly<User>;
// frozen.name = 'x';  // ERRO
```

### Pick, Omit

```typescript
// Só os campos escolhidos
type UserPreview = Pick<User, 'id' | 'name'>;
// { id: number; name: string }

// Todos exceto os escolhidos
type UserWithoutEmail = Omit<User, 'email'>;
// { id: number; name: string }
```

### Record

```typescript
type UsersByName = Record<string, User>;
// { [key: string]: User }

type RoleCapabilities = Record<'admin' | 'user' | 'guest', string[]>;
// { admin: string[]; user: string[]; guest: string[] }
```

### Exclude, Extract

```typescript
type T1 = Exclude<'a' | 'b' | 'c', 'a'>;  // 'b' | 'c'
type T2 = Extract<'a' | 'b' | 'c', 'a' | 'c'>;  // 'a' | 'c'
```

### NonNullable

```typescript
type T = NonNullable<string | null | undefined>;  // string
```

### ReturnType, Parameters

```typescript
function createUser(name: string, age: number): User {
    return { id: 1, name, age };
}

type R = ReturnType<typeof createUser>;  // User
type P = Parameters<typeof createUser>;  // [name: string, age: number]
```

### Awaited

```typescript
type R = Awaited<Promise<User>>;  // User
type R2 = Awaited<Promise<Promise<User>>>;  // User (recursivo)
```

### Uppercase, Lowercase, Capitalize

```typescript
type UpperStatus = Uppercase<'active' | 'inactive'>;  // 'ACTIVE' | 'INACTIVE'
type CapName = Capitalize<'maria'>;  // 'Maria'
```

---

## Mapped types

Criar novos tipos baseados em outros.

```typescript
// Fazer todos readonly
type Readonly<T> = {
    readonly [K in keyof T]: T[K];
};

// Fazer todos opcionais
type Partial<T> = {
    [K in keyof T]?: T[K];
};

// Adicionar prefixo nas chaves
type Prefixed<T, Prefix extends string> = {
    [K in keyof T as `${Prefix}${Capitalize<string & K>}`]: T[K];
};

type User = { name: string; age: number };
type PrefixedUser = Prefixed<User, 'user'>;
// { userName: string; userAge: number }
```

### Key remapping (TS 4.1+)

```typescript
// Remover chaves por padrão
type RemoveField<T, K extends keyof T> = {
    [P in keyof T as P extends K ? never : P]: T[P];
};

// Criar getters
type Getters<T> = {
    [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K];
};

type UserGetters = Getters<User>;
// { getName: () => string; getAge: () => number }
```

---

## Template literal types

Tipos baseados em template strings.

```typescript
type Greeting = `Hello, ${string}`;

const g1: Greeting = 'Hello, Maria';  // OK
const g2: Greeting = 'Hi, Maria';     // ERRO

// Combinando unions
type Size = 'small' | 'medium' | 'large';
type Color = 'red' | 'green' | 'blue';
type Variant = `${Size}-${Color}`;
// 'small-red' | 'small-green' | ... (9 combinações)

// Route params
type Route = `/users/${string}` | `/posts/${string}`;

// Event handlers
type EventName<T extends string> = `on${Capitalize<T>}`;
type ClickHandler = EventName<'click'>;  // 'onClick'
```

---

## typeof e keyof operators

### typeof

Em TypeScript, `typeof` em **tipos** retorna o tipo de uma variável/expressão:

```typescript
const user = { name: 'Maria', age: 30 };
type User = typeof user;
// { name: string; age: number }

const config = {
    api: { host: 'localhost', port: 3000 },
    db: { url: 'postgres://...' }
} as const;

type Config = typeof config;
// Infere todas as propriedades como readonly literals
```

### keyof

Extrai as chaves de um tipo como union:

```typescript
interface User {
    id: number;
    name: string;
    email: string;
}

type UserKey = keyof User;  // 'id' | 'name' | 'email'

// Uso típico — getter genérico
function get<T, K extends keyof T>(obj: T, key: K): T[K] {
    return obj[key];
}

const user: User = { id: 1, name: 'Maria', email: '...' };
const name = get(user, 'name');  // string (inferred)
// const x = get(user, 'foo');    // ERRO
```

### const assertions

```typescript
const point = { x: 10, y: 20 };
// tipo: { x: number; y: number }

const point2 = { x: 10, y: 20 } as const;
// tipo: { readonly x: 10; readonly y: 20 }

const colors = ['red', 'green', 'blue'] as const;
// tipo: readonly ['red', 'green', 'blue']
// colors[0] é 'red', não string

type Color = typeof colors[number];  // 'red' | 'green' | 'blue'
```

**Padrão útil:**

```typescript
const roles = ['admin', 'user', 'guest'] as const;
type Role = typeof roles[number];  // 'admin' | 'user' | 'guest'
```

---

## Enums vs Union types vs const objects

### Enum — evite em código novo

```typescript
enum Status {
    Active,
    Inactive,
    Pending
}
// Gera código JavaScript — não é "só tipo"
```

**Problemas:**

- Gera código em runtime (bundle maior)
- Comportamento estranho (reverse mapping)
- Não é tree-shakeable
- Não é type-safe 100%

### String enum — melhor

```typescript
enum Status {
    Active = 'active',
    Inactive = 'inactive',
    Pending = 'pending'
}
```

### Union de literais — **recomendado**

```typescript
type Status = 'active' | 'inactive' | 'pending';

function set(status: Status) { }
set('active');  // OK
// set('unknown');  // ERRO
```

### `as const` object — ainda melhor

```typescript
const Status = {
    Active: 'active',
    Inactive: 'inactive',
    Pending: 'pending'
} as const;

type Status = typeof Status[keyof typeof Status];
// 'active' | 'inactive' | 'pending'

Status.Active;  // 'active' (como constante)
```

**Vantagens:** tree-shakeable, sem runtime overhead além do objeto, funciona como enum e como union, permite `Status.Active`.

---

## Strict mode e tsconfig

### strict: true

```json
{
    "compilerOptions": {
        "strict": true
    }
}
```

Ativa:

- `noImplicitAny`
- `strictNullChecks`
- `strictFunctionTypes`
- `strictBindCallApply`
- `strictPropertyInitialization`
- `noImplicitThis`
- `useUnknownInCatchVariables`
- `alwaysStrict`

**`strict: true` não é suficiente.** Adicione:

```json
{
    "compilerOptions": {
        "strict": true,
        "noUncheckedIndexedAccess": true,
        "exactOptionalPropertyTypes": true,
        "noImplicitReturns": true,
        "noFallthroughCasesInSwitch": true,
        "noUnusedLocals": true,
        "noUnusedParameters": true,
        "noImplicitOverride": true,
        "noPropertyAccessFromIndexSignature": true,
        "forceConsistentCasingInFileNames": true
    }
}
```

### noUncheckedIndexedAccess

```typescript
const arr = ['a', 'b', 'c'];

// Sem a flag
const x = arr[0];  // string
arr[999].toUpperCase();  // compila, mas crasha em runtime

// Com a flag
const y = arr[0];  // string | undefined
arr[999].toUpperCase();  // ERRO — precisa verificar
```

**Recomendo ativar sempre.** Força verificação de bounds.

### exactOptionalPropertyTypes

```typescript
interface User {
    name: string;
    middleName?: string;  // string | undefined
}

// Sem a flag
const u: User = { name: 'Maria', middleName: undefined };  // OK

// Com a flag
const u: User = { name: 'Maria', middleName: undefined };  // ERRO
// middleName é string | missing, não string | undefined
const u2: User = { name: 'Maria' };  // OK
```

Distingue entre "propriedade ausente" e "propriedade = undefined".

---

## Configuração tsconfig.json

Exemplo para projeto moderno (Node 22+, ESM, strict):

```json
{
    "compilerOptions": {
        "target": "ES2023",
        "module": "NodeNext",
        "moduleResolution": "NodeNext",
        "lib": ["ES2023"],
        "types": ["node"],

        "strict": true,
        "noUncheckedIndexedAccess": true,
        "exactOptionalPropertyTypes": true,
        "noImplicitReturns": true,
        "noFallthroughCasesInSwitch": true,
        "noUnusedLocals": true,
        "noUnusedParameters": true,
        "noImplicitOverride": true,

        "esModuleInterop": true,
        "allowSyntheticDefaultImports": true,
        "forceConsistentCasingInFileNames": true,
        "skipLibCheck": true,
        "resolveJsonModule": true,

        "outDir": "./dist",
        "rootDir": "./src",
        "declaration": true,
        "declarationMap": true,
        "sourceMap": true,

        "baseUrl": ".",
        "paths": {
            "@/*": ["src/*"]
        }
    },
    "include": ["src/**/*"],
    "exclude": ["node_modules", "dist", "**/*.test.ts"]
}
```

**Flags importantes:**

- **`target`** — versão de JavaScript gerada. ES2022/2023 moderno.
- **`module`** — sistema de módulos. `NodeNext` para ESM, `CommonJS` para CJS legado.
- **`moduleResolution`** — como resolver imports. `NodeNext` para Node moderno, `Bundler` para Vite/esbuild.
- **`lib`** — APIs disponíveis (DOM, ES2023, WebWorker).
- **`esModuleInterop`** — interop com CJS.
- **`skipLibCheck`** — pula check em `.d.ts` de node_modules (acelera build).
- **`paths`** — aliases para imports.

---

## Modules

### ESM vs CJS

```typescript
// ESM (moderno)
import { foo } from './module.js';  // nota: .js mesmo importando .ts
export { bar };
export default baz;

// CJS (legado)
const { foo } = require('./module');
module.exports = { bar };
```

### Node 22+ TypeScript nativo

```bash
# Sem transpilação
node --experimental-strip-types app.ts
```

Em Node 24+, estável. Funciona com sintaxe TS que é "apenas tipos" (sem enums que geram código, sem JSX).

### Type-only imports

```typescript
import type { User } from './types';
import { type User, createUser } from './user';

// Garantido removido no output (não gera require/import)
```

**Uso:** evitar dependências circulares, garantir que tipos não gerem código runtime.

### Path aliases

```json
{
    "compilerOptions": {
        "baseUrl": ".",
        "paths": {
            "@/*": ["src/*"],
            "@ui/*": ["src/components/ui/*"]
        }
    }
}
```

```typescript
// Em vez de
import { Button } from '../../../components/ui/Button';

// Com alias
import { Button } from '@ui/Button';
```

**Cuidado:** TypeScript resolve paths, mas Node runtime **não**. Precisa de bundler (Vite, esbuild) ou `tsconfig-paths` em runtime.

---

## Declaration files (`.d.ts`)

Declaração de tipos sem implementação. Usado para:

- Descrever tipos de bibliotecas JavaScript puras
- Ambient declarations (global types)
- Module augmentation

```typescript
// types/legacy-lib.d.ts
declare module 'legacy-lib' {
    export function doStuff(input: string): number;
    export interface Config {
        apiKey: string;
    }
}

// Global types
declare global {
    interface Window {
        myApp: {
            version: string;
        };
    }
}

// Ambient module augmentation
declare module 'express-session' {
    interface SessionData {
        userId: string;
    }
}
```

### DefinitelyTyped

Biblioteca sem tipos próprios? Tem `@types/`:

```bash
npm install --save-dev @types/node @types/express @types/lodash
```

**Não publica tipos?** Crie `.d.ts` local.

---

## TypeScript em frontend (React)

### Componentes tipados

```typescript
// Functional component
type ButtonProps = {
    onClick: () => void;
    children: React.ReactNode;
    variant?: 'primary' | 'secondary';
    disabled?: boolean;
};

const Button: React.FC<ButtonProps> = ({ onClick, children, variant = 'primary', disabled }) => {
    return (
        <button onClick={onClick} className={variant} disabled={disabled}>
            {children}
        </button>
    );
};

// Prefira assinatura explícita em vez de React.FC
const Button2 = ({ onClick, children }: ButtonProps) => { ... };
```

### Hooks tipados

```typescript
// useState — inferido
const [count, setCount] = useState(0);  // number

// Tipo explícito necessário quando o valor inicial é null/undefined
const [user, setUser] = useState<User | null>(null);

// useRef
const inputRef = useRef<HTMLInputElement>(null);

// useReducer com discriminated union
type Action =
    | { type: 'increment' }
    | { type: 'decrement' }
    | { type: 'set'; value: number };

function reducer(state: number, action: Action): number {
    switch (action.type) {
        case 'increment': return state + 1;
        case 'decrement': return state - 1;
        case 'set':       return action.value;
    }
}
```

### Event handlers

```typescript
const onChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    console.log(e.target.value);
};

const onSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
};

const onClick = (e: React.MouseEvent<HTMLButtonElement>) => { };
```

→ Para deep dive em React, ver [[React]]

---

## TypeScript em backend (Node/Express)

```typescript
import express, { Request, Response, NextFunction } from 'express';

const app = express();

// Request tipado
interface CreateUserBody {
    name: string;
    email: string;
}

app.post<
    {},                     // params
    User,                   // response body
    CreateUserBody,         // request body
    { page?: string }       // query
>('/users', async (req, res) => {
    const { name, email } = req.body;  // typed
    const page = req.query.page;       // string | undefined
    const user = await createUser({ name, email });
    res.status(201).json(user);
});

// Middleware tipado
const authMiddleware = (req: Request, res: Response, next: NextFunction) => {
    // ...
};
```

### Fastify — melhor TS support

Fastify tem suporte TypeScript de primeira classe via JSON Schema:

```typescript
import Fastify from 'fastify';

const fastify = Fastify({ logger: true });

fastify.get<{
    Params: { id: string };
    Reply: User | { error: string };
}>('/users/:id', async (request, reply) => {
    const user = await findUser(request.params.id);
    if (!user) return reply.code(404).send({ error: 'not found' });
    return user;
});
```

---

## Runtime validation — Zod

TypeScript é **compile-time only**. Em runtime, dados externos (HTTP, DB) podem não ter o tipo que você espera. **Zod** resolve isso.

```typescript
import { z } from 'zod';

const UserSchema = z.object({
    id: z.number(),
    name: z.string().min(1),
    email: z.string().email(),
    age: z.number().int().positive().optional(),
    role: z.enum(['admin', 'user', 'guest']),
    createdAt: z.coerce.date()
});

// Inferir tipo automaticamente
type User = z.infer<typeof UserSchema>;
// { id: number; name: string; email: string; age?: number; role: 'admin' | 'user' | 'guest'; createdAt: Date }

// Validar em runtime
const rawData = await fetchFromAPI();
const user = UserSchema.parse(rawData);  // throws se inválido
// ou
const result = UserSchema.safeParse(rawData);
if (!result.success) {
    console.error(result.error.issues);
}
```

**Use Zod para:**

- Request body validation (API)
- Environment variables parsing
- Dados externos (API responses, storage)
- Form validation (com react-hook-form)

**Alternativas:** Valibot (menor bundle), Yup (legado), Arktype, io-ts.

---

## Template Result types e pattern matching

### Result type pattern

```typescript
type Result<T, E = Error> =
    | { ok: true; value: T }
    | { ok: false; error: E };

const ok = <T>(value: T): Result<T> => ({ ok: true, value });
const err = <E>(error: E): Result<never, E> => ({ ok: false, error });

async function fetchUser(id: number): Promise<Result<User>> {
    try {
        const user = await api.get(`/users/${id}`);
        return ok(user);
    } catch (e) {
        return err(e as Error);
    }
}

// Uso
const result = await fetchUser(42);
if (result.ok) {
    console.log(result.value.name);
} else {
    console.error(result.error.message);
}
```

**Vantagens sobre throw:**

- Erros são parte do tipo — compilador força lidar
- Sem unhandled exceptions
- Mais funcional

**Bibliotecas:** `neverthrow`, `ts-results`, `fp-ts`.

---

## Evolução do TypeScript

### TypeScript 4.x (2020-2023)

- Template literal types
- Variadic tuple types
- Recursive types
- `satisfies` operator

### TypeScript 5.0 (2023)

- Decorators (stage 3, padronizado)
- `const` type parameters
- `--verbatimModuleSyntax`
- Melhor performance

### TypeScript 5.x (2023-2025)

- **5.1**: return type inference em JSX
- **5.2**: `using` keyword, copy array methods
- **5.3**: `Import Attributes`
- **5.4**: `NoInfer` utility
- **5.5**: `const` assertions em funções, inferred type predicates
- **5.6**: melhoras em type narrowing
- **5.7**: inferência melhor em generics

### TypeScript 6.0 (2025)

- Remoção de features deprecated
- Compiler simplifications

### TypeScript 7.0 (2026 — esperado)

- **Compiler reescrito em Go** — 10x mais rápido
- Nome interno: Corsa
- Sem breaking changes na linguagem (só performance)

---

## Armadilhas comuns

- **`any`** — remove toda segurança. Use `unknown` quando não souber.
- **`as` (type assertion) abusivo** — diz "confia em mim" ao compilador. Use com cuidado.
- **`as const` esquecido em arrays** — perde literal types.
- **`Object.keys` retorna `string[]`** — não `keyof T`. Use `as (keyof T)[]` ou for-in.
- **`JSON.parse` retorna `any`** — valide com Zod.
- **`fetch` retorna `any`** — tipe explicitamente ou valide.
- **`catch (e)` é `unknown`** (strict) — narrow com `instanceof Error`.
- **Enum em vez de union literal** — enum gera código, union não.
- **`React.FC`** — adiciona `children` implicit (antigamente); hoje menos necessário.
- **Generics não inferidos** — se TS infere `unknown`, adicione constraint ou tipo explícito.
- **Dependências circulares** — use `import type`.
- **`noUncheckedIndexedAccess` desligado** — arr[999] parece string mas pode ser undefined.
- **`exactOptionalPropertyTypes` ignorado** — `undefined` vs ausente é diferente.
- **`strict: true` sem as flags extras** — só parcialmente strict.
- **Excess property check bypassed** — passar via variável pula o check.
- **`!` em produção** — force unwrap mascara bugs.
- **Validação de runtime vs tipos** — tipos são compile-time. Valide inputs.
- **`interface` e `type` inconsistentes** — escolha uma convenção.
- **`@types/*` desatualizado** — biblioteca atualizou, tipos não. Use declaration augmentation.
- **tsconfig compartilhado sem `extends`** — duplicação, configurações divergem.

---

## Na prática (da minha experiência)

> **MedEspecialista — stack TypeScript padronizada:**
>
> **1. Strict mode + todas as flags extras:**
>
> ```json
> {
>     "strict": true,
>     "noUncheckedIndexedAccess": true,
>     "exactOptionalPropertyTypes": true,
>     "noImplicitReturns": true,
>     "noFallthroughCasesInSwitch": true,
>     "noUnusedLocals": true,
>     "noUnusedParameters": true
> }
> ```
>
> Sem esse conjunto, metade dos benefícios do TS ficam dormentes.
>
> **2. Zod para toda entrada externa:**
> - HTTP request bodies
> - Environment variables (`z.object({ DATABASE_URL: z.string().url() }).parse(process.env)`)
> - Respostas de APIs externas
> - localStorage/sessionStorage
>
> Zod schema é a source of truth — tipo é inferido de lá.
>
> **3. OpenAPI → tipos:**
> Backend (Spring Boot) gera OpenAPI via SpringDoc. Frontend consome com `openapi-typescript` que gera tipos. Quando o backend muda um campo, o TypeScript quebra no frontend — erro de compilação, não runtime. Esse loop economiza tempo enorme.
>
> **4. Result types em domain code:**
> Services retornam `Result<T, DomainError>` em vez de throwing. Força o caller a lidar com erros. Nos boundaries (controllers), converto para HTTP response.
>
> **5. Discriminated unions para state:**
> Componentes React com `LoadingState = { status: 'idle' } | { status: 'loading' } | { status: 'success'; data: T } | { status: 'error'; error: E }`. Switch exhaustivo no render.
>
> **6. Branded types para IDs:**
>
> ```typescript
> type Brand<K, T> = K & { readonly __brand: T };
> type UserId = Brand<string, 'UserId'>;
> type OrderId = Brand<string, 'OrderId'>;
> // UserId e OrderId não são intercambiáveis mesmo sendo ambos strings
> ```
>
> Evita trocar IDs no código — erro de compile-time.
>
> **7. `import type` sempre:**
> Imports de tipos com `import type` para garantir que são removidos do JS. Melhora tree shaking.
>
> **8. Path aliases (`@/*`):**
> Evita imports relativos horríveis. Configurado em tsconfig + Vite/Next/Jest.
>
> **Incidente memorável — `any` vazou:**
>
> Função helper antiga tinha tipo `function parse(json: string): any`. Esse `any` foi propagado por toda a aplicação. Um campo renomeado no backend quebrou em runtime — nenhum erro de compile. Refactor: substituí por `unknown` + Zod validation. Compilador encontrou dezenas de lugares onde o código assumia shape errado. Bugs escondidos descobertos por tipos.
>
> **Outro — `Object.keys` typing:**
>
> ```typescript
> const obj = { a: 1, b: 'str' };
> Object.keys(obj).forEach(key => {
>     console.log(obj[key]);  // TS reclama: key é string, não 'a' | 'b'
> });
> ```
>
> Solução: `(Object.keys(obj) as (keyof typeof obj)[])`. Ou usar `for (const key in obj)` que narra melhor.
>
> **A lição principal:** TypeScript é uma **ferramenta de pensamento**. Quando os tipos estão difíceis de expressar, é sinal de que o design está ruim — não de que TS está atrapalhando. Domine o sistema de tipos avançado (generics, conditionals, mapped types) e você modela domínios complexos com segurança enorme.

---

## How to explain in English

> "TypeScript is a typed superset of JavaScript that I use by default in any serious project. The value isn't just catching typos — it's using types as a thinking tool. When types are hard to express, it signals the design needs work.
>
> My baseline tsconfig is strict mode plus several additional flags: `noUncheckedIndexedAccess` so array access returns `T | undefined`, `exactOptionalPropertyTypes` to distinguish between missing and undefined, and `noImplicitReturns` to catch logic gaps. Without these, you only get partial safety.
>
> I leverage the type system heavily. Discriminated unions for state — a `LoadingState` type with variants for idle, loading, success, and error makes UI exhaustive switches automatic. Branded types for IDs prevent accidentally passing a UserId where an OrderId is expected. Generic constraints and conditional types for library code. Template literal types for API paths.
>
> Since TypeScript is compile-time only, I use Zod for runtime validation of anything external — request bodies, environment variables, responses from third-party APIs. Zod schemas are the source of truth, and types are inferred from them. That loop catches mismatches between what the runtime sees and what the types claim.
>
> For frontend-backend contracts, I generate TypeScript types from OpenAPI schemas. When the backend changes a field, the frontend fails to compile — not at runtime. That feedback loop is invaluable.
>
> I avoid `any` religiously — it disables type checking entirely. When I don't know a type, I use `unknown` and narrow before using. `as` assertions are 'trust me' markers and I treat them as a last resort.
>
> For async, I sometimes use Result types instead of throw. A function returning `Result<User, UserError>` forces the caller to handle both cases explicitly. It's more functional and harder to forget errors."

### Frases úteis em entrevista

- "I use TypeScript as a thinking tool, not just type safety."
- "Strict mode isn't enough — `noUncheckedIndexedAccess` and `exactOptionalPropertyTypes` catch real bugs."
- "Discriminated unions are my go-to for state machines and Result types."
- "I use Zod for runtime validation at system boundaries."
- "Types are compile-time — always validate external data at runtime."
- "`any` disables checking. `unknown` forces narrowing. I prefer `unknown`."
- "Branded types prevent accidentally passing the wrong ID type."
- "I generate TypeScript types from OpenAPI for backend contracts."
- "I avoid enums — const objects with `as const` are tree-shakeable and give you literal types."
- "Type assertions (`as`) are 'trust me' markers — last resort."

### Key vocabulary

- tipagem estrutural → structural typing
- estreitamento de tipo → type narrowing
- proteção de tipo → type guard
- tipo utilitário → utility type
- tipo mapeado → mapped type
- tipo condicional → conditional type
- tipo literal de template → template literal type
- união discriminada → discriminated union
- interseção → intersection
- genérico → generic
- restrição → constraint
- inferência → inference
- asserção de tipo → type assertion
- declaração de tipo → type declaration
- arquivo de declaração → declaration file
- módulo ambiente → ambient module
- validação em tempo de execução → runtime validation
- tipo marcado → branded type
- nunca → never
- desconhecido → unknown

---

## Recursos

### Documentação oficial

- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html)
- [TypeScript Playground](https://www.typescriptlang.org/play)
- [tsconfig reference](https://www.typescriptlang.org/tsconfig)
- [Release notes](https://devblogs.microsoft.com/typescript/)

### Livros e tutoriais

- **Programming TypeScript** — Boris Cherny
- **Effective TypeScript** — Dan Vanderkam (62 specific ways)
- **TypeScript in 50 Lessons** — Stefan Baumgartner
- [Total TypeScript](https://www.totaltypescript.com/) — Matt Pocock (excelente)
- [Type Challenges](https://github.com/type-challenges/type-challenges)

### Cursos

- [Full Stack Open — Part 9 TypeScript](https://fullstackopen.com/en/part9)
- [TypeScript Deep Dive](https://basarat.gitbook.io/typescript/)
- [Matt Pocock YouTube](https://www.youtube.com/@mattpocockuk)

### Ferramentas

- [Zod](https://zod.dev/) — runtime validation, o default
- [Valibot](https://valibot.dev/) — alternativa menor
- [ts-reset](https://github.com/total-typescript/ts-reset) — fixes de tipos built-in
- [openapi-typescript](https://github.com/drwpow/openapi-typescript) — gerar tipos de OpenAPI
- [tsx](https://github.com/privatenumber/tsx) — runner TypeScript para Node
- [tsup](https://tsup.egoist.dev/) — bundler TS

### Blog posts essenciais

- [TypeScript Release Notes](https://devblogs.microsoft.com/typescript/)
- [Matt Pocock's TypeScript tips](https://www.mattpocock.com/)
- [Total TypeScript blog](https://www.totaltypescript.com/articles)

---

## Veja também

- [[JavaScript Fundamentals]] — linguagem base
- [[Node.js]] — runtime, TS nativo em Node 22+
- [[React]] — React com TypeScript
- [[TypeScript com React]] — trilha completa sobre a intersecção idiomática TS+React (mental model, idiomas práticos, type-level avançado)
- [[Testes em JavaScript]] — tipagem em testes
- [[Full Stack Open - Guia de Revisão]] — Parte 9 é sobre TS
- [[API Design]] — OpenAPI, contract types
- [[Banco de dados]] — Prisma, Drizzle (ORMs TS-first)
- [[Arquitetura de Software]] — DDD com TS
