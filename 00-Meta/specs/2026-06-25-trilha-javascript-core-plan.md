---
title: "Plano — Trilha JavaScript (core)"
type: spec
created: 2026-06-25
updated: 2026-06-25
status: draft
tags:
  - spec
  - trilha
  - javascript
  - frontend
aliases:
  - Plano JavaScript core
---

# Plano — Trilha JavaScript (core) — 3 fases

## Objetivo

`Tecnologia/JavaScript` deixa de ser monólito (`JavaScript Fundamentals.md`) e vira **a trilha atômica da linguagem em si**, em 3 fases (Iniciado/Adepto/Magus), padrão capítulo de livro. Alvo: prep entrevistas internacionais, eixo frontend-web, perfil Senior Fullstack. É a **Onda A, prioridade nº 1** do [[00-Meta/Roadmap|Roadmap]] — fecha a base que o índice do TypeScript já referencia e que hoje não existe atomizada.

**Tese:** JavaScript é uma linguagem **dinâmica, single-thread, baseada em protótipos, com coerção e tipagem fraca em runtime** — e quase toda armadilha e decisão de design sai dessas propriedades. O eixo da trilha é ir do **modelo mental** (o que a engine faz com seu código) até **execução assíncrona, metaprogramação e o JS moderno (ES2026)**.

## Princípios

- **Escrita do ZERO com pesquisa web profunda** (estado 2026). O monólito `JavaScript Fundamentals.md` serve como UMA referência de tópicos; o conteúdo é reescrito e aprofundado, não migrado.
- **Padrão capítulo** ([[feedback_padrao_capitulo_livro]]): problema-primeiro, registro Feynman ([[feedback_enriquecimento_feynman]]), exemplos trabalhados, diagramas Mermaid onde agregam, "Como explicar em inglês" + tabela PT↔EN, armadilhas comuns. Notas profundas com diagramas ([[feedback_notas_profundas_diagramas]]).
- **Calibração por fase** ([[project_trilhas_fases_aprendizado]]): Iniciado = modelo mental e fundamentos; Adepto = mecanismos júnior→pleno; Magus = profundidade sênior, runtime-aware, moderno.
- **Redundância entre notas é reforço** ([[feedback_redundancia_entre_notas]]): linkar os seams, não podar.
- **Notas atômicas** ([[feedback_notas_atomicas]]): dividir se uma nota cobrir 2+ tópicos ou estourar; brotos para sub-tópicos avançados ([[project_broto_galho_convention]]).

## Fronteiras (seams)

A regra de ouro: **"o que a linguagem é e como eu uso" fica aqui; "como o runtime/ferramenta executa por baixo" é linkado.**

| Tema | Fica no JS core | Linka para |
| ---- | --------------- | ---------- |
| Async / event loop | semântica de Promises/async-await, padrões, iterators/generators, modelo de execução em nível de spec (call stack, fila de jobs/microtasks) | internals do motor e fases → [[03-Dominios/Tecnologia/Node/Runtime e Event Loop/index\|Node/Runtime e Event Loop]] |
| Módulos | sintaxe ESM da linguagem: `import`/`export`, dynamic `import()`, escopo de módulo, live bindings | resolução, CJS interop, dual packages, bundling → [[03-Dominios/Tecnologia/Tooling e Build/06 - ESM e CJS e o sistema de módulos\|Tooling 06]] |
| Tipos | sistema de tipos em runtime: 7 primitivos + object, `typeof`, coerção, `==`/`===`, wrappers | tipagem estática → [[03-Dominios/Tecnologia/TypeScript/index\|TypeScript]] |
| APIs de browser | nada de DOM | DOM, eventos, fetch, storage, Web APIs → [[03-Dominios/Tecnologia/Plataforma Web/index\|Plataforma Web]] |
| Testes | nada de framework | Vitest/Jest/Testing Library/Playwright → trilha **Testes em JS** (Onda B) |
| ES2026 | Temporal, Explicit Resource Management, features por ano (conteúdo Magus) | — |

## Roster (26 notas — 9 / 9 / 8)

### 🟢 Iniciado — modelo mental e fundamentos (9)
1. **O que é JavaScript** — ECMAScript, engines (V8/JSC/SpiderMonkey), parse→JIT, single-thread; o modelo mental da linguagem
2. **Tipos em runtime** — os 7 primitivos + object, `typeof`, wrappers, `null` vs `undefined`
3. **Coerção e igualdade** — `==` vs `===`, truthy/falsy, conversões implícitas, `Object.is` *(clássica de entrevista)*
4. **Variáveis e escopo** — `var`/`let`/`const`, hoisting, TDZ, escopo léxico, block scope
5. **Funções** — declaration vs expression vs arrow, params (default/rest), first-class, IIFE
6. **`this`** — as 4 regras de binding, `call`/`apply`/`bind`, arrow vs regular
7. **Objetos** — criação, property descriptors, getters/setters, spread, destructuring
8. **Arrays e métodos** — `map`/`filter`/`reduce`, mutável vs imutável, iteração
9. **Strings, template literals e regex** — manipulação, tagged templates, regex essencial

### 🟡 Adepto — mecanismos júnior→pleno (9)
10. **Closures** — escopo capturado, module pattern, currying/memoização, pitfalls (loop+`var`)
11. **Prototypes e herança** — prototype chain, `__proto__` vs `prototype`, `Object.create`, `class` como açúcar
12. **Map, Set, WeakMap, WeakSet** — quando usar vs objeto puro; chaves, garbage-collectability
13. **Números, BigInt e precisão** — ponto flutuante (IEEE 754), `Number` vs `BigInt`, `Math`, `Intl.NumberFormat`
14. **Promises** — estados, `then`/`catch`/`finally`, encadeamento, propagação de erro
15. **async/await** — semântica, `try/catch`, sequencial vs paralelo, `Promise.all`/`allSettled`/`race`/`any`
16. **Iterators e generators** — protocolo iterable, `function*`/`yield`, lazy evaluation, async iterators/`for-await-of`
17. **Módulos ESM** — `import`/`export`, named/default, dynamic `import()`, module scope, live bindings *(seam Tooling 06)*
18. **Error handling** — tipos de `Error`, custom errors, erros assíncronos, `throw` vs `reject`, `cause`

### 🔴 Magus — profundidade sênior, runtime-aware, moderno (8)
19. **Modelo de execução a fundo** — call stack, a fila de microtasks/jobs da spec, ordem sync→microtask *(link Node pras fases do event loop)*
20. **Cópia, serialização e imutabilidade** — shallow vs deep, JSON (`parse`/`stringify`, reviver/replacer), `structuredClone`, `Object.freeze`, padrões imutáveis
21. **Memory management** — GC (mark-sweep/geracional), reference vs value, leaks comuns, closures e memória, `WeakRef`/`FinalizationRegistry`
22. **Metaprogramação** — `Proxy`, `Reflect`, `Symbol` e symbols bem-conhecidos (`Symbol.iterator`, etc.)
23. **Recursos modernos (ES2020→ES2025)** — optional chaining, nullish coalescing, top-level await, `Array.prototype` recentes, etc.
24. **ES2026 e o futuro** — Temporal (e por que o `Date` legado é quebrado), Explicit Resource Management (`using`), decorators, status de Records & Tuples
25. **Armadilhas e quirks** — `NaN`, ponto flutuante, coerção bizarra, `this` perdido, `typeof null`, hoisting surpresa *(entrevista)*
26. **Capstone** — JS na prática + entrevista: decision points, "como explicar em inglês", mapa de revisão da trilha, perguntas-modelo

## Artefatos do domínio

- **`Dicionário de JavaScript`** (type: glossary) — criar; o domínio não tem glossário e JS é denso em termos. Habilita verbetes/lente Conexões no futuro.
- **`Biblioteca de JavaScript`** — já existe; manter.
- **`index.md`** — reescrever como MOC das 3 fases ao fim, preservando os links pra `Testes em JavaScript`, `Validação`, `Biblioteca`, `Full Stack Open` e a seção "Veja também".

## Execução

1. **Escrever a trilha fresca** (com pesquisa), em ondas por fase, revisão entre fases. Criar `Dicionário de JavaScript`.
2. **Pós-escrita (commit próprio):** podar/aposentar `JavaScript Fundamentals.md` (vira stub que aponta pra trilha, ou removido com inbounds repointados), reescrever `index.md` como MOC, repointar inbounds (Sendas, índice do TypeScript que cita a base JS). Verificar 0 quebras de wikilink.
3. **Ciclo de qualidade (opcional, como no Tooling):** `/plantar-duvidas` → `/colher-duvidas` no galho; `/verificar-wikilinks`.

## Fora de escopo

- Frameworks de teste (Vitest/Jest/Playwright) → trilha **Testes em JS** (Onda B).
- DOM e APIs de browser → **Plataforma Web**.
- Internals do event loop e fases → **Node/Runtime e Event Loop**.
- Tipagem estática → **TypeScript** (pronta).
- TypeScript-specific (generics, utility types) → **TypeScript**.

## Padrões e referências

- [[00-Meta/Roadmap|Roadmap de Trilhas]] (Onda A, item 1)
- [[project_trilhas_fases_aprendizado]], [[feedback_padrao_capitulo_livro]], [[feedback_notas_profundas_diagramas]], [[feedback_notas_atomicas]], [[project_broto_galho_convention]], [[project_artefatos_dominio]]
- Trilhas-modelo já construídas: [[03-Dominios/Tecnologia/TypeScript/index|TypeScript]] (27), [[03-Dominios/Tecnologia/Tooling e Build/index|Tooling e Build]] (26)
