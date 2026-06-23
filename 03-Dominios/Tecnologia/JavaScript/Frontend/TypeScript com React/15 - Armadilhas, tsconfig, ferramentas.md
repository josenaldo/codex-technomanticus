---
title: "Armadilhas, tsconfig, ferramentas"
created: 2026-04-26
updated: 2026-04-26
type: reference
status: seedling
publish: true
tags: [typescript, react, typescript-react, frontend, tsconfig, eslint, tooling, pitfalls, react-compiler, ts-reset]
aliases:
  - Cheatsheet TypeScript React
  - tsconfig React+Vite
  - tsconfig React+Next
---

# Armadilhas, tsconfig, ferramentas

> [!abstract] TL;DR
> Checklist de armadilhas TS+React (≥12 itens) + tsconfig específico React+Vite + tsconfig React+Next 16 + ESLint plugins essenciais (`react-hooks`, `react-compiler`) + `ts-reset` para corrigir tipos built-in problemáticos. Esta nota é referência rápida — abra antes de fechar PR ou começar projeto novo.

## O que é

Esta nota é diferente das demais da trilha — não tem estrutura narrativa "O que é → Por que importa → Como funciona". Funciona como **agregador**: lista de armadilhas para revisar antes de PR, tsconfig pronto para colar em projetos novos, ferramentas que valem ativar. Cada item linka para a nota específica que aprofunda o tema. Use como cheatsheet — abra antes de começar projeto novo, antes de fechar PR, ou antes de uma entrevista para refrescar os pontos-chave de cada nota da trilha.

## Armadilhas comuns

Lista numerada de armadilhas que aparecem em PRs reais e custam horas para diagnosticar quando passam despercebidas. Cada uma com o sintoma, o exemplo curto e o fix.

1. **`useRef<T>(null!)` em vez de `useRef<T | null>(null)`** — o `null!` é um non-null assertion que mente sobre o tipo: o TS acredita que `ref.current` é sempre `T`, mas em runtime o valor inicial é `null` até a ref ser anexada. Em React 19, a forma correta é `useRef<HTMLInputElement>(null)` — o tipo retornado já inclui `T | null` e força o narrow no uso. Veja [[05 - Tipando state e refs|nota 05]].

2. **`as any` em casts de events** — `onClick={(e: any) => ...}` ou `(e as any).target.value` perdem toda segurança de tipo do handler. A forma correta é tipar com `React.MouseEvent<HTMLButtonElement>`, `React.ChangeEvent<HTMLInputElement>`, etc., ou deixar o TS inferir do JSX (em handlers inline, normalmente é o melhor caminho). Veja [[06 - Tipando event handlers|nota 06]].

3. **Esquecer `as const` em retorno de tupla de hook customizado** — `return [value, setValue]` infere `(T | typeof setValue)[]` (array misto), o que quebra a desestruturação no consumer (`const [v, set] = useFoo()` perde tipos específicos por posição). `return [value, setValue] as const` infere a tupla preservada `readonly [T, typeof setValue]`. Veja [[07 - Tipando hooks customizados|nota 07]].

4. **`createContext<T>(null!)` em vez de `<T | null>(null)` + custom hook narrow** — o `null!` mente sobre o valor default; se algum consumer usar fora do `<Provider>`, recebe `null` em runtime sem aviso do TS. A forma correta é `createContext<T | null>(null)` mais um custom hook (`useFooContext`) que faz `if (!ctx) throw new Error(...)` — isso narrow o tipo para `T` e produz erro claro em dev. Veja [[08 - Tipando Context API|nota 08]].

5. **`useState([])` esquecido sem generic** — sem anotação, `useState([])` infere `never[]`, e a primeira chamada `setItems([{ id: 1 }])` falha com "Type '{ id: number; }' is not assignable to type 'never'". Anote sempre com `useState<Item[]>([])`. Veja [[02 - Inferir vs anotar - quando deixar o TS trabalhar|nota 02]].

6. **Generic em arrow function `.tsx` sem vírgula** — `<T>(props: Props<T>) => ...` é parseado como JSX (`<T>` é tag) e quebra. Use `<T,>(props: Props<T>) => ...` (vírgula force tuple parsing) ou `<T extends unknown>(props: Props<T>) => ...` ou `function Component<T>(...)` (function declaration). Veja [[12 - Generic components|nota 12]].

7. **`e.target.value` em handlers que não são input** — `target` é qualquer node descendente do elemento que disparou o evento (por bubbling), não necessariamente o elemento listening. Em `<button onClick={e => e.target.value}>`, `target` pode ser um `<span>` filho do botão e não tem `.value`. Use `e.currentTarget` para acessar o elemento que tem o listener. Veja [[06 - Tipando event handlers|nota 06]].

8. **`Object.keys(obj)` retorna `string[]`** — não `(keyof T)[]`. O TS é correto aqui: objetos em JS podem ter chaves não declaradas em runtime, então `keyof T` seria mentira. O fix é castar quando se tem certeza: `(Object.keys(obj) as (keyof typeof obj)[])` — ou usar `for...in` com type guard. Veja [[TypeScript]] seção armadilhas.

9. **`JSON.parse` retorna `any`** — `const data = JSON.parse(response)` injeta `any` no código, contaminando tudo que toca `data`. Sempre validar com Zod no boundary: `const data = userSchema.parse(JSON.parse(response))`. Veja [[10 - Tipando formulários|nota 10]] e [[11 - Tipando data fetching|nota 11]].

10. **`catch (e)` é `unknown` em strict mode** — `catch (e) { console.log(e.message) }` falha porque `e` é `unknown`. Narrow com `instanceof Error`: `if (e instanceof Error) { console.log(e.message) }`. Para erros customizados, criar classe (`class FetchError extends Error`) e narrow com `instanceof FetchError`.

11. **`React.FC` com generic não funciona naturalmente** — `const List: React.FC<Props<T>> = ...` exige declarar `T` na assinatura, e `React.FC` não permite generics no callsite. Use anotação direta: `function List<T>({ items, render }: Props<T>) { ... }`. Veja [[03 - Por que React.FC saiu de moda|nota 03]].

12. **Confundir `MouseEvent` (DOM nativo) com `React.MouseEvent` (synthetic)** — em listeners imperativos via `element.addEventListener('click', handler)`, o handler recebe `MouseEvent` nativo do lib.dom; em props JSX (`<div onClick={...}>`), recebe `React.MouseEvent` synthetic. Os tipos não são intercambiáveis; importar do lugar certo. Veja [[06 - Tipando event handlers|nota 06]].

13. **Children como `JSX.Element` em vez de `React.ReactNode`** — `JSX.Element` é só o tipo retornado por componentes (basicamente `ReactElement`); `React.ReactNode` aceita strings, números, fragmentos, arrays, `null`, `undefined`, booleans — o que children realmente pode ser na prática. Tipar `children: JSX.Element` rejeita `<Foo>texto</Foo>` ou `<Foo>{items.map(...)}</Foo>`.

14. **Memoizar inline com deps array vazio + objeto literal** — `useMemo(() => ({ a: 1 }), [])` parece uma constante, mas se a dependência for um objeto/array literal nas deps (`[someObj]`), o memo invalida a cada render porque `someObj` é referência nova. Para constantes verdadeiras, use `useRef` ou state pattern, ou mova para fora do componente.

15. **`defaultProps` em function components** — deprecated em React 19 (warning em dev, removido em versões futuras). Use destructuring default: `function Btn({ variant = 'primary' }: Props) { ... }`. Mais idiomático, sem dependência de propriedade estática anexada à função.

## tsconfig.json — React + Vite (2026)

Template para projeto React + Vite + TypeScript em 2026, focado em rigor máximo no compilador e compatibilidade com o pipeline do Vite.

```json
{
  "compilerOptions": {
    "target": "ES2023",
    "lib": ["ES2023", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "jsx": "react-jsx",

    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "noImplicitReturns": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,

    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "isolatedModules": true,
    "allowImportingTsExtensions": true,
    "noEmit": true,
    "resolveJsonModule": true,

    "baseUrl": ".",
    "paths": { "@/*": ["./src/*"] }
  },
  "include": ["src"]
}
```

Comentários sobre as flags-chave em React+Vite:

- **`jsx: "react-jsx"`** — JSX transform moderno (sem precisar `import React from 'react'` em cada arquivo).
- **`moduleResolution: "Bundler"`** — Vite resolve módulos via bundler (esbuild/Rollup), não Node. Permite imports sem extensão `.js` em paths relativos e resolve `package.json#exports` corretamente.
- **`isolatedModules: true`** — força cada arquivo a ser standalone (sem dependência cross-file no tipo); necessário para Vite/esbuild compilar arquivo a arquivo em paralelo.
- **`allowImportingTsExtensions: true`** — Vite resolve `.ts` e `.tsx` direto; com `noEmit: true`, o TS permite escrever `import './foo.ts'` sem reclamar.
- **`noUncheckedIndexedAccess: true`** — `arr[0]` vira `T | undefined` em vez de `T`. Captura categoria inteira de bugs de acesso a array fora de bound.
- **`exactOptionalPropertyTypes: true`** — distingue `prop?: T` de `prop: T | undefined`. Impede passar `prop: undefined` explicitamente quando o tipo só permite ausência.
- **`paths`** — alias `@/*` → `./src/*` para imports absolutos. Vite precisa do mesmo alias em `vite.config.ts` (`resolve.alias`).

## tsconfig.json — React + Next 16 (2026)

Template para projeto React + Next 16 + TypeScript. Difere do Vite em pontos-chave porque Next usa SWC (não TS) para transformar JSX e gera tipos automáticos para rotas.

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["dom", "dom.iterable", "esnext"],
    "module": "esnext",
    "moduleResolution": "bundler",
    "jsx": "preserve",

    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,

    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "isolatedModules": true,
    "incremental": true,
    "resolveJsonModule": true,
    "noEmit": true,

    "plugins": [{ "name": "next" }],

    "paths": { "@/*": ["./*"] }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

Diferenças relevantes do template do Next:

- **`jsx: "preserve"`** — Next usa SWC (não TypeScript) para transformar JSX. O TS deixa o JSX intacto e o SWC processa downstream.
- **`plugins: [{ "name": "next" }]`** — TypeScript plugin do Next dá autocomplete em route handlers, layout props, `params`/`searchParams`, e checagem de `Link href` contra rotas existentes.
- **`incremental: true`** — build TS incremental (Next mantém cache em `.next/cache`), reduz drasticamente type-check em re-runs.
- **`include` com `.next/types/**/*.ts`** — Next gera tipos para rotas e layouts em `.next/types` durante build/dev; precisam estar no include para o autocomplete funcionar.

## ESLint essencial

Plugins mínimos que valem ativar em qualquer projeto React+TS de 2026.

```json
{
  "extends": [
    "plugin:@typescript-eslint/recommended",
    "plugin:react/recommended",
    "plugin:react-hooks/recommended",
    "plugin:react-compiler/recommended"
  ],
  "plugins": ["@typescript-eslint", "react", "react-hooks", "react-compiler"],
  "rules": {
    "react/react-in-jsx-scope": "off",
    "react/jsx-uses-react": "off"
  }
}
```

Plugins essenciais:

- **`react-hooks/recommended`** — habilita `rules-of-hooks` (chamadas de hook em ordem fixa, fora de condicionais/loops) e `exhaustive-deps` (deps array de `useEffect`/`useMemo`/`useCallback` deve listar todas as dependências reativas). Captura categoria inteira de bugs de stale closure e dependência incorreta.
- **`react-compiler/recommended`** — captura código que viola Rules of React e por isso não pode ser otimizado pelo compiler (mutação de props/state, side effects no render, refs lidas no render). Se você ativa o React Compiler, este plugin é obrigatório para confiar no resultado.
- **`@typescript-eslint/recommended`** — regras genéricas de TS (`no-explicit-any`, `no-unused-vars` aware de tipos, `consistent-type-imports`, etc.).

ESLint flat config (`eslint.config.js`) é o padrão moderno em vez de `.eslintrc.json`; ambos suportados em 2026 mas flat config é a recomendação oficial e a forma como os plugins documentam install. As regras `react/react-in-jsx-scope` e `react/jsx-uses-react` ficam off porque o JSX transform moderno (`jsx: "react-jsx"` no tsconfig) não exige `import React`.

## ts-reset — corrige tipos built-in

`ts-reset` (Matt Pocock, MIT) é "um CSS reset para TypeScript": corrige tipos imprecisos do `lib.dom.d.ts` e do `lib.es*.d.ts` que o TypeScript mantém por compatibilidade histórica mas que produzem `any` ou comportamento permissivo demais.

Correções principais:

- `JSON.parse(...)` retorna `any` por default → ts-reset torna `unknown` (força validação no consumer).
- `fetch(...).then(r => r.json())` retorna `any` → ts-reset força `unknown` (mesma lógica — nunca confie em response sem validar).
- `[].includes(item)` aceita qualquer string sem reclamar → ts-reset estreita para o tipo do array (catches typos em literal unions).
- `.filter(Boolean)` agora narrow corretamente (`(T | null | undefined)[].filter(Boolean) → T[]`).

Instalação:

```bash
npm install --save-dev @total-typescript/ts-reset
```

```typescript
// reset.d.ts
import '@total-typescript/ts-reset';
```

```json
// tsconfig.json
{
  "include": ["src", "reset.d.ts"]
}
```

Adicionar em todo projeto novo. Captura categorias inteiras de bugs sem custo de runtime — é só refinamento de tipo no compile time.

## React Compiler (2026)

React Compiler automatiza memoization. Não precisa mais `useMemo`/`useCallback`/`memo()` na maioria dos casos — o compiler analisa o código em build time e adiciona memoization onde necessário, com granularidade que humanos raramente atingem manualmente. **Pré-condição:** o código precisa obedecer Rules of React (sem mutação de props/state, sem side effects no render, hooks chamados em ordem fixa). Quando essas regras são violadas, o compiler skippa otimização do componente em vez de produzir código quebrado — silencioso, mas observável via `eslint-plugin-react-compiler` que detecta as violações em lint.

Setup em Vite:

```bash
npm install --save-dev babel-plugin-react-compiler eslint-plugin-react-compiler
```

```javascript
// vite.config.js
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [
    react({
      babel: {
        plugins: ['babel-plugin-react-compiler']
      }
    })
  ]
});
```

Em Next.js 16, ativar via `experimental.reactCompiler: true` no `next.config.js`. O plugin Babel é incluído automaticamente quando a flag está ativa.

## Em entrevista

> "My checklist for TypeScript + React in 2026 production: strict mode plus the extra flags that strict alone misses — `noUncheckedIndexedAccess` for array bounds, `exactOptionalPropertyTypes` to distinguish missing from undefined. ESLint with `react-hooks` and `react-compiler` plugins to catch hooks violations and code that breaks the optimizer. `ts-reset` to fix `JSON.parse` and `Array.includes` returning `any` or accepting wrong types. Zod for runtime validation at every boundary — fetch responses, FormData, environment variables — because TypeScript is compile-time only. And React Compiler when the codebase obeys Rules of React, which lets me drop most manual memoization."

**Vocabulário-chave:** *strict mode flags*, *exhaustive-deps*, *Rules of React*, *runtime validation*, *flat config*.

## Veja também

- [[TypeScript com React]] — MOC da trilha
- [[01 - A tripla inferência - props, state, hooks]]
- [[02 - Inferir vs anotar - quando deixar o TS trabalhar]]
- [[03 - Por que React.FC saiu de moda]]
- [[04 - interface vs type vs satisfies para props]]
- [[05 - Tipando state e refs]]
- [[06 - Tipando event handlers]]
- [[07 - Tipando hooks customizados]]
- [[08 - Tipando Context API]]
- [[09 - Tipando reducers e state machines]]
- [[10 - Tipando formulários]]
- [[11 - Tipando data fetching]]
- [[12 - Generic components]]
- [[13 - Polymorphic components com as prop]]
- [[14 - Compound components, slots, render props]]
- [[TypeScript]] — nota mãe
- [[React]] — nota mãe
