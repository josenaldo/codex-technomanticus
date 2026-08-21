---
title: "TypeScript com React"
type: moc
publish: true
tags: [typescript, react, typescript-react, frontend, moc]
created: 2026-04-26
updated: 2026-04-26
---

# TypeScript com React

Esta trilha cobre a intersecção idiomática entre TypeScript e React — não é um curso de TS isolado nem de React isolado, mas o que acontece quando os dois encostam: tipagem de props, hooks customizados, Context, generics em componentes e os patterns de type-level que distinguem código senior de código pleno. Em 2026, TypeScript é default em qualquer projeto React sério, mas a intersecção tem soluções não-óbvias que aparecem com frequência em entrevistas internacionais e em revisões de código de design systems.

Em 15 notas, a trilha vai do mental model fundamental ("como o TS pensa em React") ao type-level avançado (polymorphic components, compound components tipados), passando pelos idiomas práticos do dia a dia. Cada nota tem seção "Em entrevista" para preparação internacional.

> [!info] Como ler
> A trilha pressupõe que você consultará [[03-Dominios/Tecnologia/TypeScript/index|TypeScript]] e [[React]] como referências paralelas. Cada nota linka explicitamente para a seção mãe quando precisa de um conceito de TS ou React que não é o foco. Para uma primeira leitura, siga a sequência 01 → 15. Para reforço pontual ou preparação de entrevista, use as rotas alternativas abaixo.

## Comece por aqui

Trilha sequencial recomendada — leia na ordem para construir o terreno do mental model até o type-level avançado.

- [[01 - A tripla inferência - props, state, hooks|01 - A tripla inferência]] — como o TS pensa em React: props declaradas, state inferido, hooks tipados pela lib
- [[02 - Inferir vs anotar - quando deixar o TS trabalhar|02 - Inferir vs anotar]] — a regra prática: anote inputs públicos, deixe inferir o resto
- [[03 - Por que React.FC saiu de moda]] — a história, os problemas e o que usar no lugar
- [[04 - interface vs type vs satisfies para props|04 - interface vs type vs satisfies]] — a decisão idiomática: extensão e merging vs unions e mapped types
- [[05 - Tipando state e refs|05 - Tipando state e refs]] — `useState`, `useRef`, DOM refs vs mutable refs, `useImperativeHandle`
- [[06 - Tipando event handlers|06 - Tipando event handlers]] — synthetic events, `ChangeEvent`, `currentTarget` vs `target`
- [[07 - Tipando hooks customizados|07 - Tipando hooks customizados]] — return types preservando inferência, tuplas com `as const`, overloads
- [[08 - Tipando Context API|08 - Tipando Context API]] — default null pattern, narrowing por custom hook, sem `null!`
- [[09 - Tipando reducers e state machines|09 - Tipando reducers e state machines]] — discriminated unions em ação, switch exhaustivo
- [[10 - Tipando formulários|10 - Tipando formulários]] — RHF + Zod, schema-driven typing, controlled vs uncontrolled
- [[11 - Tipando data fetching|11 - Tipando data fetching]] — React Query, validação no boundary, Suspense, Server Actions
- [[12 - Generic components|12 - Generic components]] — `function List<T>` que preserva inferência no consumidor
- [[13 - Polymorphic components com as prop|13 - Polymorphic components]] — `<Box as="a" href="..." />` tipado corretamente
- [[14 - Compound components, slots, render props|14 - Compound components, slots, render props]] — composição tipada com Context coordenado
- [[15 - Armadilhas, tsconfig, ferramentas|15 - Armadilhas, tsconfig, ferramentas]] — checklist final + tsconfig React+Vite/Next + ESLint + ts-reset

## Rotas alternativas

### Rota entrevista (preparar perguntas frequentes em entrevistas internacionais)
[[03 - Por que React.FC saiu de moda]] → [[04 - interface vs type vs satisfies para props|04 - interface vs type vs satisfies]] → [[07 - Tipando hooks customizados]] → [[09 - Tipando reducers e state machines]] → [[12 - Generic components]] → [[13 - Polymorphic components com as prop|13 - Polymorphic components]]

### Rota produção (escrever bem no dia a dia, sem type-level avançado)
[[01 - A tripla inferência - props, state, hooks|01 - A tripla inferência]] → [[02 - Inferir vs anotar - quando deixar o TS trabalhar|02 - Inferir vs anotar]] → [[05 - Tipando state e refs]] → [[06 - Tipando event handlers]] → [[08 - Tipando Context API]] → [[10 - Tipando formulários]] → [[11 - Tipando data fetching]] → [[15 - Armadilhas, tsconfig, ferramentas]]

### Rota library author (escrever componentes reutilizáveis)
[[04 - interface vs type vs satisfies para props|04 - interface vs type vs satisfies]] → [[07 - Tipando hooks customizados]] → [[12 - Generic components]] → [[13 - Polymorphic components com as prop|13 - Polymorphic components]] → [[14 - Compound components, slots, render props|14 - Compound components]]

### Rota completa
Sequencial 01 → 15. Recomendada na primeira leitura.

## Veja também

- [[03-Dominios/Tecnologia/TypeScript/index|TypeScript]] — deep dive da linguagem (referência paralela)
- [[React]] — deep dive da biblioteca (referência paralela)
- [[JavaScript Fundamentals]] — base da linguagem
- [[Testes em JavaScript]] — para testes de componentes tipados
- [[Senda Frontend]] — trilha de aprendizado mais ampla
