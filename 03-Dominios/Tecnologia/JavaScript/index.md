---
title: "JavaScript"
type: moc
publish: true
created: 2026-05-03
updated: 2026-06-25
status: evergreen
tags:
  - javascript
  - moc
aliases:
  - JS
  - JavaScript
---

# JavaScript

> [!abstract] TL;DR
> Trilha da linguagem JavaScript em 3 fases (Iniciado/Adepto/Magus). A tese: **JS é uma linguagem dinâmica, single-thread, baseada em protótipos, com coerção e tipagem fraca em runtime** — e quase toda armadilha e decisão de design sai dessas propriedades. Vai do modelo mental (o que a engine faz com seu código) até execução assíncrona, metaprogramação e o JS moderno (ES2026). Os internals do runtime vivem em [[03-Dominios/Tecnologia/Node/index|Node]]; a tipagem estática em [[03-Dominios/Tecnologia/TypeScript/index|TypeScript]]; as APIs do navegador em [[03-Dominios/Tecnologia/Plataforma Web/index|Plataforma Web]].

## 🟢 Iniciado — o modelo mental e os fundamentos da linguagem

- [[01 - O que é JavaScript]] — ECMAScript, engines, JIT, single-thread; o modelo mental
- [[02 - Tipos em runtime]] — os 7 primitivos + object, `typeof`, wrappers, `null` vs `undefined`
- [[03 - Coerção e igualdade]] — `==` vs `===`, truthy/falsy, conversões implícitas
- [[04 - Variáveis e escopo]] — `var`/`let`/`const`, hoisting, TDZ, escopo léxico
- [[05 - Funções]] — declaration vs expression vs arrow, params, first-class, IIFE
- [[06 - this]] — as 4 regras de binding, `call`/`apply`/`bind`, arrow vs regular
- [[07 - Objetos]] — criação, descriptors, getters/setters, spread, destructuring
- [[08 - Arrays e métodos]] — `map`/`filter`/`reduce`, mutável vs imutável, iteração
- [[09 - Strings, template literals e regex]] — manipulação, tagged templates, regex essencial

## 🟡 Adepto — os mecanismos que separam júnior de pleno

- [[10 - Closures]] — escopo capturado, module pattern, currying/memoização
- [[11 - Prototypes e herança]] — prototype chain, `Object.create`, `class` como açúcar
- [[12 - Map, Set, WeakMap, WeakSet]] — quando usar vs objeto puro; garbage-collectability
- [[13 - Números, BigInt e precisão]] — IEEE 754, `BigInt`, `Math`, `Intl.NumberFormat`
- [[14 - Promises]] — estados, encadeamento, combinadores, propagação de erro
- [[15 - async-await]] — semântica, `try/catch`, sequencial vs paralelo
- [[16 - Iterators e generators]] — protocolo iterable, `function*`, lazy, async iterators
- [[17 - Módulos ESM]] — `import`/`export`, dynamic `import()`, module scope, live bindings
- [[18 - Error handling]] — tipos de `Error`, custom errors, erros assíncronos, `cause`

## 🔴 Magus — profundidade sênior, runtime-aware e moderno

- [[19 - Modelo de execução a fundo]] — call stack, fila de microtasks/jobs, ordem de execução
- [[20 - Cópia, serialização e imutabilidade]] — shallow vs deep, JSON, `structuredClone`, `Object.freeze`
- [[21 - Memory management]] — GC (mark-sweep), leaks, `WeakRef`/`FinalizationRegistry`
- [[22 - Metaprogramação]] — `Proxy`, `Reflect`, `Symbol` e well-known symbols
- [[23 - Recursos modernos (ES2020 a ES2025)]] — optional chaining, nullish, Set methods, Iterator Helpers
- [[24 - ES2026 e o futuro]] — Temporal, Explicit Resource Management (`using`), decorators
- [[25 - Armadilhas e quirks]] — `NaN`, ponto flutuante, coerção bizarra, `this` perdido
- [[26 - Capstone - JavaScript na prática e em entrevista]] — síntese, decision points, perguntas de entrevista

## Artefatos do domínio

- [[Dicionário de JavaScript]] — glossário de termos da linguagem
- [[Biblioteca de JavaScript]] — utilitários e libs do ecossistema
- [[Testes em JavaScript]] — Vitest, Testing Library, MSW, Playwright
- [[03-Dominios/Tecnologia/JavaScript/Validação/index|Validação]] — schema validation em runtime (Zod, Yup, Joi)

## Guias

- [[Full Stack Open - Guia de Revisão]] — resumo do curso da Universidade de Helsinki (pt-BR)

## Veja também

- [[03-Dominios/Tecnologia/TypeScript/index|TypeScript]] — o sistema de tipos sobre JS
- [[03-Dominios/Tecnologia/Node/index|Node]] — JS no servidor (runtime e event loop)
- [[03-Dominios/Tecnologia/React/index|React]] — UI no cliente
- [[03-Dominios/Tecnologia/Plataforma Web/index|Plataforma Web]] — APIs do navegador
- [[03-Dominios/Tecnologia/Tooling e Build/index|Tooling e Build]] — o ecossistema de build do JS/TS
- [[Senda JS-TS]] · [[Senda Frontend]] · [[Senda Fullstack Java-Spring + TS-React-Nextjs 15]]
