---
title: "TypeScript"
type: moc
publish: true
created: 2026-05-03
updated: 2026-06-23
status: growing
tags:
  - typescript
  - moc
aliases:
  - TS
---

# TypeScript

> [!abstract] TL;DR
> Trilha de TypeScript em 3 fases (Iniciado/Adepto/Magus). A tese: **TS é um sistema de tipos *estrutural*, *gradual* e *apagado em runtime* colado sobre o JavaScript** — essas três propriedades explicam quase toda decisão de design e armadilha. Vai do modelo mental até type-level programming e a fronteira type↔runtime.

Estante de TypeScript: do sistema de tipos do dia a dia até programação no nível de tipos e a fronteira com o runtime. A base da linguagem JS vive em [[03-Dominios/Tecnologia/JavaScript/index|JavaScript]]; a teoria de sistemas de tipos em [[03-Dominios/Ciência/Paradigmas/13 - Sistemas de tipos|Sistemas de tipos]]; o TS aplicado a React no galho [[03-Dominios/Tecnologia/React/TypeScript com React/index|TypeScript com React]].

## 🟢 Iniciado — o sistema de tipos do dia a dia

- [[01 - O que é TypeScript - gradual, estrutural, apagado]] — o modelo mental: as três propriedades que explicam tudo
- [[02 - Tipos primitivos, literais e inferência]] — primitivos, literal types e deixar o `tsc` inferir
- [[03 - Arrays, tuplas e as const]] — estruturas literais e o `as const` pra derivar tipos
- [[04 - any, unknown e never]] — o topo, o fundo e o buraco do sistema; soundness
- [[05 - strictNullChecks - null, undefined e optional]] — o erro de um bilhão de dólares, resolvido
- [[06 - Objetos - interface vs type]] — tipar objetos e a pergunta clássica de entrevista
- [[07 - Union e intersection types]] — a álgebra de `|` e `&`
- [[08 - Discriminated unions e exhaustiveness]] — o pattern de modelagem mais importante
- [[09 - Type narrowing e type guards]] — como o TS estreita tipos via control flow
- [[10 - Tipando funções - assinaturas, overloads, contextual typing]] — funções, overloads e inferência contextual

## 🟡 Adepto — type-level programming e configuração

- [[11 - Generics - funções e constraints]] — `<T>`, inferência de type args e constraints
- [[12 - Generics - defaults, classes e interfaces genéricas]] — defaults, containers genéricos, variância
- [[13 - Conditional types]] — `T extends U ? X : Y` e distribuição sobre unions
- [[14 - infer e extração de tipos]] — pattern matching no nível de tipos
- [[15 - keyof, typeof e indexed access types]] — a ponte valor↔tipo
- [[16 - Mapped types e key remapping]] — iterar sobre chaves pra construir tipos
- [[17 - Template literal types]] — strings no nível de tipos
- [[18 - Utility types - e como reconstruí-los]] — os embutidos, desmontados (consolidação)
- [[19 - Enums, const objects e modelagem de constantes]] — como modelar conjuntos fechados
- [[20 - tsconfig e strict mode a fundo]] — o compilador como type-checker configurável

## 🔴 Magus — fronteiras, runtime, escala, produção *(a escrever)*

- 21 — Modules: ESM, CJS e type-only imports
- 22 — Declaration files (`.d.ts`) e o ecossistema de tipos
- 23 — A fronteira type↔runtime: parse, don't validate
- 24 — Type-driven design: branded types, Result e estados impossíveis
- 25 — TypeScript em escala: performance do compilador e project references
- 26 — Lendo o compilador: erros comuns e como decifrar mensagens
- 27 — TypeScript em entrevista

## Referência

- [[Biblioteca de TypeScript]] — recursos externos curados (Total TypeScript, TS Handbook, Effective TS, Type Challenges)

> [!note] Migração em curso
> A nota monolítica `TypeScript.md` está sendo dissolvida nesta trilha (fase Iniciado feita); será aposentada quando Adepto e Magus estiverem escritas.

## Veja também

- [[03-Dominios/Tecnologia/JavaScript/index|JavaScript]] — a linguagem base
- [[03-Dominios/Tecnologia/React/TypeScript com React/index|TypeScript com React]] — TS aplicado a React
- [[03-Dominios/Ciência/Paradigmas/index|Paradigmas]] — a teoria de sistemas de tipos
- [[03-Dominios/Tecnologia/Tooling e Build/index|Tooling e Build]] — bundlers e transpilação
