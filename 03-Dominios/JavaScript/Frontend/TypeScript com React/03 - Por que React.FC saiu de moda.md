---
title: "Por que React.FC saiu de moda"
created: 2026-04-26
updated: 2026-04-26
type: concept
status: seedling
publish: true
tags: [typescript, react, typescript-react, frontend, mental-model, components, history]
aliases:
  - React.FC vs annotation
  - FunctionComponent
---

# Por que React.FC saiu de moda

> [!abstract] TL;DR
> `React.FC` (alias `React.FunctionComponent`) era o padrão para tipar componentes funcionais até por volta de 2020-2021. A comunidade se afastou por três razões: (1) injetava `children` implicitamente em todos os componentes; (2) atrapalhava componentes genéricos; (3) padrões com `defaultProps` ficavam *awkward*. Hoje o idiomático é anotar props como parâmetro: `function Button({ ... }: Props)`.

## O que é

`React.FC<Props>` é um *type alias* exportado pelo `@types/react` que descreve a assinatura completa de um componente funcional. Historicamente, antes da atualização para `@types/react@18`, ele tipava o componente como `(props: Props & { children?: ReactNode }) => ReactElement | null` — ou seja, um componente que aceita `Props` *mais* `children` automaticamente, e retorna um elemento React. `React.FunctionComponent` é o nome longo; `React.FC` é apenas o alias curto. Os dois são literalmente a mesma coisa, exportados lado a lado em `@types/react`.

## História

Entre 2018 e 2020, `React.FC` era a forma mais comum de tipar componentes funcionais em projetos TypeScript. O *template* TypeScript oficial do Create React App o utilizava por padrão, e muitos *boilerplates*, tutoriais e exemplos da comunidade seguiam o mesmo caminho. Era considerado "o jeito React+TS" por ser explícito (a anotação na linha do `const` deixa claro "isto é um componente") e por trazer `children` "de graça".

A virada começou em janeiro de 2020. No PR [facebook/create-react-app#8177](https://github.com/facebook/create-react-app/pull/8177) (autor: Retsam, mergeado em 22 de janeiro de 2020), o template TypeScript do CRA removeu `React.FC` da sua amostra inicial. A descrição do PR enumera exatamente os problemas que viraram consenso na comunidade: `children` implícito, ausência de suporte a *generics* não resolvidos, fricção em padrões de "componente como *namespace*", incompatibilidade com `defaultProps`. Esse PR não foi a "causa única" da virada — várias discussões aconteciam em paralelo no DefinitelyTyped e em posts da comunidade — mas ele consolidou em texto público o argumento contra, e mudou a "primeira impressão" que devs novos em React+TS recebiam ao iniciar um projeto.

Em paralelo, o DefinitelyTyped reagiu ao mesmo problema do `children` implícito introduzindo, no PR [DefinitelyTyped/DefinitelyTyped#46643](https://github.com/DefinitelyTyped/DefinitelyTyped/pull/46643) (autor: awmottaz, mergeado em 26 de agosto de 2020), o tipo `VoidFunctionComponent` (alias `VFC`): idêntico a `FC`, mas **sem** `children` implícito. Foi uma solução paliativa — quem queria a "marca" de componente sem o `children` automático passava a usar `VFC`. A adoção foi limitada porque, nesse mesmo período, a comunidade estava migrando para um padrão mais simples: parar de usar o alias e anotar diretamente.

A correção definitiva veio com a atualização para o React 18. O PR [DefinitelyTyped/DefinitelyTyped#56210](https://github.com/DefinitelyTyped/DefinitelyTyped/pull/56210) (autor: eps1lon, mergeado em 7 de abril de 2022), que publicou as *typings* oficiais para o React 18, removeu o `children` implícito tanto de `React.FunctionComponent` quanto de `React.Component`. A partir desse ponto, `React.FC<Props>` deixou de injetar `children` — quem quisesse aceitar filhos passou a precisar declarar a prop explicitamente, exatamente como na anotação direta. O `VFC` foi marcado como *deprecated* e equivalente a `FC` no `@types/react@18`.

Em 2026, o consenso público da comunidade é que `React.FC` "não é necessário" — o [React TypeScript Cheatsheet](https://react-typescript-cheatsheet.netlify.app/docs/basic/getting-started/function_components) afirma textualmente que o consenso geral é que `React.FunctionComponent` (ou o atalho `React.FC`) "não é necessário". A inércia da escolha tomada nos *starters* e cheatsheets entre 2020 e 2022 fixou a anotação direta de props como o idioma. `React.FC` ainda funciona — não foi removido, não está *deprecated* —, mas raramente é a primeira opção em código novo.

## Por que importa

A questão não é "qual sintaxe parece mais bonita". `React.FC` carregava três problemas concretos que aparecem em código real, e entender cada um é útil em entrevista (onde a pergunta "por que `React.FC` saiu de moda?" é frequente em *senior interviews*) e em revisão de código legado, onde aparecer um `React.FC` ainda é comum.

### Problema 1 — `children` implícito (em `@types/react` pré-18)

```typescript
// Antigamente (com React.FC injetando children automaticamente)
const Heading: React.FC<{ title: string }> = ({ title, children }) => (
  <h1>{title}{children}</h1>
);
// O dev nem precisava declarar children — apareceu via FC.
// Resultado: <Heading title="X">qualquer coisa</Heading> compilava sempre,
// mesmo quando o componente não deveria aceitar children.
```

O efeito é vazamento de API: qualquer componente tipado com `React.FC` aceitava silenciosamente filhos, mesmo quando o autor pretendia o contrário. Não havia forma de dizer "este componente é *void* — não aceita filhos" sem deixar de usar `FC`. Em código de design system, isso virava bug recorrente: alguém aninhava `<Icon><span>...</span></Icon>` e nada falhava em tempo de compilação, mesmo que o `Icon` ignorasse os filhos no JSX renderizado.

A partir de `@types/react@18` (publicado via PR #56210), `React.FC` foi atualizado e **não** injeta mais `children`. Esse problema específico tecnicamente desapareceu nas versões modernas. O ponto histórico, porém, é que a inércia da comunidade já tinha movido para a anotação direta antes da correção chegar — quem trocou em 2020-2021 não tinha motivo para voltar em 2022.

### Problema 2 — generics ficam estranhos

```typescript
// Tentativa ingênua de generic component com React.FC — não funciona
// (T não está em escopo no lado direito da atribuição)
const List: React.FC<{ items: T[] }> = ({ items }) => (/* ... */);
//                          ^ T não declarado

// Workaround antigo — arrow function com generic explícito + React.ReactElement
const List = <T,>({ items }: { items: T[] }): React.ReactElement => (
  <ul>{items.map((item) => /* ... */ null)}</ul>
);
// Não é mais React.FC; o "tipo de componente" passou para o return.

// Idiomático moderno (sem React.FC) — declaração de função suporta generics natural
function List<T>({ items }: { items: T[] }) {
  return <ul>{items.map((item) => /* ... */ null)}</ul>;
}
```

`React.FC` recebe um único parâmetro de tipo (`Props`), e não há sintaxe que permita passar um generic *não resolvido* através dele. Em prática, isso significava que componentes como `<List<User> items={...} />` ou `<Select<Option> options={...} />` — que dependem de inferir um `T` do *call site* — exigiam abandonar `React.FC` ou usar *workarounds* que perdiam toda a vantagem ergonômica do alias. A declaração de função simples (`function List<T>(...)`) suporta generics nativamente. O aprofundamento desse pattern está em [[12 - Generic components]].

### Problema 3 — o que usar hoje

```typescript
type ButtonProps = {
  onClick: () => void;
  variant?: 'primary' | 'secondary';
  children: React.ReactNode; // explícito quando o componente aceitar
};

// Anotação direta com declaração de função — idiomática
function Button({ onClick, variant = 'primary', children }: ButtonProps) {
  return (
    <button onClick={onClick} className={variant}>
      {children}
    </button>
  );
}

// Arrow function com anotação no parâmetro — também válido e comum
const Button = ({ onClick, variant = 'primary', children }: ButtonProps) => (
  <button onClick={onClick} className={variant}>
    {children}
  </button>
);
```

A regra: anote as props como tipo do parâmetro, deixe o TS inferir o resto. `children` vira uma prop como qualquer outra — se o componente aceita filhos, declare; se não aceita, não declare. Não há `FC` envolvido, e nenhuma das três armadilhas acima aparece. O return type é inferido (`JSX.Element` ou `React.ReactElement` na prática), e generics passam a funcionar sem ginástica sintática.

## Quando ainda faz sentido

Casos onde `React.FC` continua aceitável (ainda que raramente *preferível*):

- **Codebases legadas onde o padrão já é `React.FC` em todo lugar.** Trocar tudo de uma vez gera ruído desnecessário em PRs e diffs. Manter `FC` em código existente e introduzir anotação direta apenas em código novo é uma estratégia razoável.
- **Quando o autor quer marcar visualmente "isto é um componente".** Algumas pessoas preferem ler `const Button: React.FC<Props> = ...` por sinalizar a intenção de forma explícita. É preferência de estilo legítima.
- **Em ambos os casos, é decisão de estilo.** Funcionalmente, anotação direta cobre tudo que `React.FC` cobre nas versões modernas — o inverso (cobrir generics com `FC`) não é verdade.

Em código novo, em projeto novo, sem restrição de consistência com legado, a recomendação é anotação direta.

## Armadilhas

- **Trocar `React.FC` por anotação direta sem adicionar `children` no tipo quando o componente realmente aceita filhos.** Em `@types/react` pré-18, `FC` injetava `children` "de graça" — ao migrar para anotação direta, é preciso lembrar de declarar `children: React.ReactNode` (ou `?` quando opcional). Em `@types/react@18+`, `FC` também não injeta mais — então quem migrou hoje provavelmente nem tinha esse hábito, mas vale o aviso para quem mexe em código que migrou parcialmente.

- **Confundir `React.FC` com `React.FunctionComponent`.** São aliases idênticos exportados juntos do `@types/react`. `React.FC = React.FunctionComponent`. Trocar um pelo outro não muda absolutamente nada do comportamento. Em revisão de código, ver os dois no mesmo projeto é sinal de inconsistência de estilo, não de bug.

- **Em `@types/react@18+`, `React.FC` *sem* `children` implícito é o default — ainda assim, anotação direta é preferida pela comunidade.** O argumento "agora que `FC` não injeta mais `children`, posso voltar a usar?" tem mérito do ponto de vista isolado, mas ignora que (a) generics ainda continuam não funcionando bem com `FC`, e (b) a comunidade já consolidou a anotação direta como idioma, então código novo escrito com `FC` parece datado para revisores que entraram no React depois de 2021.

- **Esquecer que `VFC` (`VoidFunctionComponent`) virou redundante em `@types/react@18`.** O alias ainda existe por retrocompatibilidade, mas marca o componente como sem `children` — exatamente o que `FC` passou a fazer também. Em código novo, não há motivo para usar `VFC`.

## Em entrevista

> "`React.FC` was the standard until around 2020-2021. The community moved away from it for three reasons. First, it injected `children` implicitly into every component, even ones that shouldn't accept them — that was fixed in `@types/react@18`, but the community had already moved on. Second, generic components became awkward — you can't easily express `React.FC<Props<T>>` because there's no place to declare `T`. Third, `defaultProps` patterns didn't compose well with it. Today the idiom is annotating props as the parameter: `function Button({ onClick, children }: Props)`. It's simpler, plays well with generics, and forces you to be explicit about whether `children` is part of the API."

**Vocabulário-chave:** *function component*, *children prop*, *implicit*, *idiomatic*, *type alias*.

**Pergunta típica de senior interview:** *"Why did the React community stop recommending `React.FC`?"* — resposta defensiva: três razões concretas (children implícito, fricção com generics, padrões com `defaultProps`), além da fricção menor de não ser mais conciso que a alternativa direta. Mencionar o PR do CRA (#8177, jan/2020) como momento simbólico da virada é um plus.

## Veja também

- [[01 - A tripla inferência - props, state, hooks]] — props vêm da assinatura do componente; `React.FC` é só uma das formas de declarar essa assinatura
- [[02 - Inferir vs anotar - quando deixar o TS trabalhar]] — anotar props como parâmetro é o caso canônico de "anotar na fronteira"
- [[04 - interface vs type vs satisfies para props]] — escolha do construtor de tipo para o `Props`, ortogonal a usar ou não `FC`
- [[12 - Generic components]] — o problema 2 (generics) aprofundado
- [[React]] — seção "Componentes e JSX"
