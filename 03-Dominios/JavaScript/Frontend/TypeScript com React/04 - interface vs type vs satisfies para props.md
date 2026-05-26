---
title: "interface vs type vs satisfies para props"
created: 2026-04-26
updated: 2026-04-26
type: concept
status: seedling
publish: true
tags: [typescript, react, typescript-react, frontend, mental-model, props, interface, type, satisfies]
aliases:
  - Interface vs type para props
  - satisfies em props React
---

# interface vs type vs satisfies para props

> [!abstract] TL;DR
> Para props de componentes: `interface` quando você quer **declaration merging** (estender tipos de libs externas) ou está escrevendo uma lib que outros vão estender. `type` quando precisa de unions, intersections, mapped, conditional. `satisfies` para validar props parciais sem perder literal types. Convenção: sufixo `Props` (ex: `ButtonProps`).

## O que é

Os três construtores resolvem problemas distintos. Para detalhes da diferença em geral (não só em props), ver [[TypeScript]] na seção "Interfaces e Type aliases".

`interface` define o **shape de um objeto**. Tem duas características que `type` não tem: **declaration merging** (duas declarações da mesma `interface User { ... }` no mesmo escopo se fundem em uma só) e a sintaxe `extends` para herança de shape. É a ferramenta canônica para tipos que outros vão **estender** — a partir do código próprio (`extends`) ou do código deles (re-declarando a mesma interface).

`type` é um **alias** para qualquer tipo. Aceita tudo que `interface` aceita, mais: *unions* (`A | B`), *intersections* (`A & B`), *mapped types* (`{ [K in keyof T]: ... }`), *conditional types* (`T extends U ? X : Y`), *tuplas*, *template literals* e renomear primitivos. Não suporta declaration merging — duas `type Foo = ...` no mesmo escopo dão erro de redeclaração.

`satisfies` (TS 4.9+) é um **operador de validação**. Verifica que um valor obedece a um tipo sem fazer *widening* — ao contrário da anotação `:`, que troca o tipo inferido pelo tipo declarado. Em props, aparece quando você quer um *default partial* ou um *config* que valida shape mas mantém os literais específicos de cada chave. A nota anterior ([[02 - Inferir vs anotar - quando deixar o TS trabalhar|02]]) já cobriu `satisfies` em configs gerais; aqui o foco é o uso específico em props.

## Por que importa

A escolha entre `interface` e `type` não é cosmética em três cenários concretos:

1. **Componentes que estendem props de elementos HTML.** Padrões como `interface ButtonProps extends React.ComponentPropsWithoutRef<'button'>` versus `type ButtonProps = React.ComponentPropsWithoutRef<'button'> & { ... }` parecem equivalentes — e em uso direto são — mas a versão `interface` permite que **outros** estendam `ButtonProps` por sua vez sem ginástica sintática. Em design systems, isso vira ergonomia de API.

2. **Componentes que aceitam props variantes.** Um `<Button>` que muda quais props aceita conforme `variant: 'icon' | 'text' | 'split'` precisa de **discriminated union**. Unions só existem com `type`. Tentar expressar isso com `interface` simplesmente não compila.

3. **Componentes em libs públicas.** Quem consome uma lib pode querer estender as props publicadas para criar um wrapper. `interface` permite — declaration merging é a ferramenta mais flexível para extensibilidade entre módulos. `type` força quem consome a fazer `MyProps & { extra: X }` em cada *call site*.

A regra prática que se desprende: **`interface` quando outros vão estender; `type` quando o tipo é "fechado" do meu lado**. E `satisfies` quando preciso de um default que não pode perder literais.

## Como funciona

### Sample 1 — `interface` para extensão

```typescript
// Quando quero permitir que outros estendam
interface ButtonProps extends React.ComponentPropsWithoutRef<'button'> {
  variant?: 'primary' | 'secondary';
}

// Outra lib pode estender:
interface FancyButtonProps extends ButtonProps {
  glow: boolean;
}
```

`interface ... extends` lê de cima para baixo: `ButtonProps` herda tudo de `ComponentPropsWithoutRef<'button'>` (todas as props nativas do `<button>`) e adiciona `variant`. Em seguida, `FancyButtonProps` herda tudo de `ButtonProps` e adiciona `glow`. A cadeia é explícita, e quem lê o tipo entende a intenção sem precisar decifrar uma intersection longa.

### Sample 2 — `type` para união de variants

```typescript
// Discriminated union — props mudam conforme variant
type ButtonProps =
  | { variant: 'icon'; icon: React.ReactNode; label: string }
  | { variant: 'text'; children: React.ReactNode }
  | { variant: 'split'; primary: React.ReactNode; secondary: React.ReactNode };

// TS força handler a verificar variant antes de acessar a prop específica
function Button(props: ButtonProps) {
  if (props.variant === 'icon') return <span>{props.icon}</span>;
  // props.children não existe aqui — narrowed
  // ...
}
```

Esse é o caso onde `interface` não serve: não há `interface A | B`. O *discriminated union* é construído com `type` e a propriedade `variant` faz o papel de *discriminator* — quando o handler verifica `props.variant === 'icon'`, o TS estreita o tipo para o ramo correspondente da union, e só as props daquele ramo ficam acessíveis. É o pattern canônico para componentes com modos mutuamente exclusivos.

### Sample 3 — `satisfies` para defaults parciais

```typescript
const DEFAULT_BUTTON_PROPS = {
  variant: 'primary',
  size: 'md',
  disabled: false,
} satisfies Partial<ButtonProps>;

// satisfies valida shape sem widening:
// DEFAULT_BUTTON_PROPS.variant: 'primary' (literal preservado)
// vs
// const X: Partial<ButtonProps> = { variant: 'primary', ... };
// X.variant: ButtonProps['variant'] | undefined (widened)
```

A diferença é sutil mas importa: anotar com `: Partial<ButtonProps>` faz o tipo de `DEFAULT_BUTTON_PROPS.variant` virar `ButtonProps['variant'] | undefined` — você perde a informação de que aquele valor específico é literalmente `'primary'`. `satisfies` valida o shape (acusa typos, exige que `variant` seja um valor válido de `ButtonProps['variant']`) e mantém o literal `'primary'`. Útil para defaults que serão `spread` em JSX (`<Button {...DEFAULT_BUTTON_PROPS} {...overrides} />`) ou consultados em outros lugares com tipo preciso.

### Sample 4 — convenção de nomenclatura

```typescript
// Sufixo Props — convenção do ecossistema
type ButtonProps = { /* ... */ };
type ModalProps = { /* ... */ };
type FormProps = { /* ... */ };

// Não use I-prefix (anti-pattern em TS):
// interface IButtonProps { ... }  // ruim — convenção C#/Java, não TS
```

Sufixo `Props` é convenção observada amplamente em projetos React+TS — cheatsheets, exemplos oficiais e libs do ecossistema usam o pattern. O prefixo `I` (`IButtonProps`) é herança de C#/Java e considerado *anti-pattern* em TS: a [orientação oficial do TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/declaration-files/do-s-and-don-ts.html) e a maioria das *style guides* recomendam evitar. O argumento é que TS usa structural typing (não nominal), então marcar visualmente "isto é uma interface" não comunica nada útil ao consumidor — o que ele precisa saber é o **shape**, não se o construtor foi `interface` ou `type`.

## Na prática

Padrão observado em libs grandes do ecossistema React (cheatsheet oficial, exemplos do Handbook, documentação de várias libs maduras): **`type` é a escolha default** quando o tipo é "fechado" no lado da lib, com `interface` aparecendo em cenários onde `extends` ou declaration merging trazem ganho real (props públicas que serão estendidas por consumidores, integração com tipos de libs externas via merging). O [React TypeScript Cheatsheet](https://react-typescript-cheatsheet.netlify.app/docs/basic/getting-started/basic_type_example) é explícito sobre isso: o exemplo canônico de `Props` usa `type`, com a ressalva *"use `interface` if exporting so that consumers can extend"*.

A regra prática derivada: **`interface` quando outros vão estender; `type` quando o tipo é "fechado" do meu lado**. Em apps de produto (não libs), `type` é mais simples e cobre 95% dos casos — o tipo das props de `<UserProfile>` raramente precisa ser estendido por outro código no mesmo app. Em libs públicas, `interface` em props exportadas dá flexibilidade para quem vai consumir a lib criar wrappers e variantes sem fricção.

`satisfies` entra em camadas adjacentes às props: defaults parciais, mapas de variantes (`const VARIANTS = { primary: {...}, secondary: {...} } satisfies Record<Variant, Style>`), tabelas de configuração que viram props via spread. Não é "como tipar props" no sentido estrito — é "como construir valores que viram props sem perder informação no caminho".

## Armadilhas

- **Misturar `interface` e `type` no mesmo codebase sem critério.** Inconsistência local é pior que qualquer escolha. Se metade dos componentes usa `type Props` e a outra metade usa `interface Props` sem diferença justificável, revisores perdem tempo decidindo o que importa em cada PR. Defina a regra do projeto (a mais comum: `type` por default, `interface` quando precisa de `extends`/merging) e siga.

- **Tentar union com `interface` (não funciona).** `interface ButtonProps = { variant: 'icon' } | { variant: 'text' }` simplesmente não compila — `interface` não tem sintaxe para union. Erro comum de quem está migrando para discriminated unions sem trocar o construtor. Sintoma: `'=' expected` ou `An interface can only extend an object type or intersection of object types with statically known members`. Corrige trocando `interface` por `type`.

- **Esquecer que `interface` permite declaration merging acidental.** Se você declara `interface ButtonProps { ... }` e em outro lugar do mesmo escopo (mesmo arquivo, mesmo `namespace`, mesmo módulo `declare`-ado) outra `interface ButtonProps { ... }` aparece, as duas se fundem silenciosamente. Em código próprio é raro, mas em projeto com vários arquivos de tipos globais (`global.d.ts`, ambient declarations) pode causar bugs sutis — o tipo público passa a ter props que o autor original nem sabe que estão lá. `type ButtonProps = ...` redeclarado dá erro imediato, o que é mais seguro como default.

- **Usar `interface` por hábito quando precisa de mapped/conditional types.** `interface PartialButtonProps = { [K in keyof ButtonProps]?: ButtonProps[K] }` não compila — *mapped types* só existem em `type`. Quando o tipo é "função de outro tipo" (Pick, Omit, Partial, custom mappings), `type` é a única opção. Tentar forçar `interface` aqui leva a workarounds que perdem a expressividade do mapped.

## Em entrevista

> "For component props, my rule is: `interface` when consumers might want to extend the type — declaration merging works on interfaces, not types. `type` when I need unions, intersections, mapped types, or conditional types — interfaces can't do those. In practice, in product code I default to `type` because it's simpler and covers most cases. In library code, I lean toward `interface` for public APIs because users can extend them. For partial defaults or configs, I use `satisfies` instead of `:` annotation, because `satisfies` validates shape without widening literal types."

**Vocabulário-chave:** *declaration merging*, *type alias*, *literal type widening*, *discriminated union*.

**Pergunta típica de senior interview:** *"When would you choose `interface` over `type` for component props?"* — resposta defensiva: when consumers (or other modules) need to extend the props — declaration merging and `extends` are interface-only features. For closed types, especially anything involving unions, mapped types, or conditional types, `type` is the only option that works.

## Veja também

- [[02 - Inferir vs anotar - quando deixar o TS trabalhar]]
- [[09 - Tipando reducers e state machines]] — discriminated unions em ação
- [[12 - Generic components]]
- [[TypeScript]] — seção "Interfaces e Type aliases"
