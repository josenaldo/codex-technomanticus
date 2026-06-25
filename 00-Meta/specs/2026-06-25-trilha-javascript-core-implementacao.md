---
title: "Plano de Implementação — Trilha JavaScript core"
type: spec
created: 2026-06-25
updated: 2026-06-25
status: draft
tags:
  - spec
  - plano
  - javascript
aliases:
  - Implementação JavaScript core
---

# Plano de Implementação — Trilha JavaScript core

> **Para executores:** este plano implementa o spec [[00-Meta/specs/2026-06-25-trilha-javascript-core-plan|Plano — Trilha JavaScript core]]. Padrão de execução: **subagente-por-nota**, em ondas por fase, com gate de qualidade entre fases. Passos usam checkbox (`- [ ]`).

**Objetivo:** transformar o domínio `Tecnologia/JavaScript` de monólito numa trilha atômica de 26 notas em 3 fases, escrita do zero com pesquisa 2026, padrão capítulo.

**Abordagem:** cada nota é escrita por um subagente seguindo a skill `/escrever-nota` (núcleo capítulo + registro Feynman), pesquisando o estado 2026 via WebSearch. Notas commitadas em sub-lotes. Gate `/verificar-nota` por fase; `/verificar-wikilinks` no teardown.

**Stack/convenções:** Obsidian + Quartz; padrão capítulo de livro; fases Iniciado/Adepto/Magus; PT-BR com seção "Como explicar em inglês".

## Global Constraints (valem para TODA nota)

- **Escrita do ZERO com pesquisa** — o monólito `JavaScript Fundamentals.md` é referência de tópicos, NÃO fonte de migração. Pesquisar estado 2026 (WebSearch) e citar em `## Referências`.
- **Padrão capítulo** — problema-primeiro; registro Feynman (analogias, perguntas retóricas, camadas, resumo em 1 linha); exemplos de código trabalhados; Mermaid onde agrega; seção "Como explicar em inglês" + tabela PT↔EN; "Armadilhas comuns" (≥3 `[!warning]`).
- **Fase calibra a régua** — Iniciado: sem assumir base; Adepto: pleno; Magus: sênior/runtime-aware.
- **Frontmatter** — `type: concept`, `fase: <iniciado|adepto|magus>`, `created: 2026-06-25`, `updated: 2026-06-25`, `status: seedling`, `publish: true`, `tags` (incluindo `javascript`, `entrevista`, e a fase).
- **Seams (linkar, não duplicar):** event-loop internals → [[03-Dominios/Tecnologia/Node/Runtime e Event Loop/index|Node]]; ESM internals → Tooling 06; tipos estáticos → TypeScript; DOM/browser → Plataforma Web; frameworks de teste → trilha Testes em JS.
- **Wikilinks só para alvos confirmados** (`ls` antes; sem alvos inventados). Sem glossário ainda no início → criar `Dicionário de JavaScript` na Wave 0 e linkar verbetes conforme surgirem.
- **Anti-fabricação** ([[feedback_no_fabrication]]): nunca inventar dados/experiências do usuário.
- **Numeração** das notas conforme o roster do spec (`01 - ...` a `26 - ...`).
- **Não criar notas fora do roster** (sub-tópico avançado vira broto, não nota nova sem aprovação).

## Estrutura de arquivos

Pasta-alvo: `03-Dominios/Tecnologia/JavaScript/`

- **Criar (26):** `01 - O que é JavaScript.md` … `26 - Capstone ...md` (títulos exatos do roster do spec)
- **Criar (1):** `Dicionário de JavaScript.md` (`type: glossary`)
- **Reescrever (teardown):** `index.md` → MOC das 3 fases
- **Aposentar (teardown):** `JavaScript Fundamentals.md` → stub apontando pra trilha (ou remover com inbounds repointados)
- **Manter:** `Biblioteca de JavaScript.md`, `Testes em JavaScript.md`, `Full Stack Open - Guia de Revisão.md`, `Validação/`

---

## Procedimento por nota (template aplicado a cada uma das 26)

Cada "task de nota" segue este ciclo (um subagente por nota):

- [ ] **1. Pesquisar** o tópico (WebSearch dirigido, estado 2026): semântica, edge cases, o que separa júnior de sênior, mudanças recentes da spec.
- [ ] **2. Escrever** a nota via `/escrever-nota` no path exato, fase indicada, cobrindo o escopo da linha do roster + os seams (linkando, não duplicando). Registro Feynman obrigatório.
- [ ] **3. Auto-gate** `/verificar-nota` no arquivo; corrigir o que reprovar (estrutura, profundidade, tamanho, links, inglês).
- [ ] **4. Reportar** ao orquestrador: o que cobriu, fontes, wikilinks criados, linhas, score.

O orquestrador **commita por sub-lote** (paths explícitos, sem assinatura) e roda `/verificar-wikilinks` ao fim de cada fase.

---

## Wave 0 — Setup

### Task 0.1: Criar o Dicionário de JavaScript
- [ ] Criar `03-Dominios/Tecnologia/JavaScript/Dicionário de JavaScript.md` com `type: glossary`, seções A–Z (ou por bloco alfabético), seed com ~10 termos centrais (closure, hoisting, TDZ, coerção, prototype, this, event loop, microtask, Promise, ESM).
- [ ] Commit: `feat(js): cria Dicionário de JavaScript (glossary do domínio)`

## Wave 1 — Iniciado (notas 01–09)

Sub-lotes de até 5 subagentes em paralelo (teto de fan-out), um por nota. Escopo de cada nota = linha correspondente do roster do spec.

- [ ] **01 - O que é JavaScript** — ECMAScript, engines (V8/JSC/SpiderMonkey), parse→JIT, single-thread; modelo mental
- [ ] **02 - Tipos em runtime** — 7 primitivos + object, `typeof`, wrappers, `null` vs `undefined`
- [ ] **03 - Coerção e igualdade** — `==` vs `===`, truthy/falsy, conversões implícitas, `Object.is`
- [ ] **04 - Variáveis e escopo** — `var`/`let`/`const`, hoisting, TDZ, escopo léxico, block scope
- [ ] **05 - Funções** — declaration/expression/arrow, params (default/rest), first-class, IIFE
- [ ] **06 - this** — 4 regras de binding, `call`/`apply`/`bind`, arrow vs regular
- [ ] **07 - Objetos** — criação, descriptors, getters/setters, spread, destructuring
- [ ] **08 - Arrays e métodos** — `map`/`filter`/`reduce`, mutável vs imutável, iteração
- [ ] **09 - Strings, template literals e regex** — manipulação, tagged templates, regex essencial
- [ ] **Gate fase Iniciado:** commit por sub-lote; `/verificar-wikilinks 03-Dominios/Tecnologia/JavaScript`; corrigir quebras reais.

## Wave 2 — Adepto (notas 10–18)

- [ ] **10 - Closures** — escopo capturado, module pattern, currying/memoização, pitfalls (loop+`var`)
- [ ] **11 - Prototypes e herança** — prototype chain, `__proto__` vs `prototype`, `Object.create`, `class`
- [ ] **12 - Map, Set, WeakMap, WeakSet** — quando usar vs objeto; chaves, GC-ability
- [ ] **13 - Números, BigInt e precisão** — IEEE 754, `Number` vs `BigInt`, `Math`, `Intl.NumberFormat`
- [ ] **14 - Promises** — estados, `then`/`catch`/`finally`, encadeamento, propagação de erro
- [ ] **15 - async/await** — semântica, `try/catch`, sequencial vs paralelo, `Promise.all`/`allSettled`/`race`/`any`
- [ ] **16 - Iterators e generators** — protocolo iterable, `function*`/`yield`, lazy, async iterators/`for-await`
- [ ] **17 - Módulos ESM** — `import`/`export`, dynamic `import()`, module scope, live bindings (seam Tooling 06)
- [ ] **18 - Error handling** — tipos de `Error`, custom errors, erros assíncronos, `throw` vs `reject`, `cause`
- [ ] **Gate fase Adepto:** commit por sub-lote; `/verificar-wikilinks`; corrigir quebras reais.

## Wave 3 — Magus (notas 19–26)

- [ ] **19 - Modelo de execução a fundo** — call stack, fila de microtasks/jobs da spec, ordem (link Node pras fases)
- [ ] **20 - Cópia, serialização e imutabilidade** — shallow/deep, JSON (reviver/replacer), `structuredClone`, `Object.freeze`
- [ ] **21 - Memory management** — GC (mark-sweep/geracional), leaks, closures e memória, `WeakRef`/`FinalizationRegistry`
- [ ] **22 - Metaprogramação** — `Proxy`, `Reflect`, `Symbol` e symbols bem-conhecidos
- [ ] **23 - Recursos modernos (ES2020→ES2025)** — optional chaining, nullish, top-level await, etc.
- [ ] **24 - ES2026 e o futuro** — Temporal (e por que `Date` é quebrado), Explicit Resource Management (`using`), decorators, Records & Tuples
- [ ] **25 - Armadilhas e quirks** — `NaN`, ponto flutuante, coerção bizarra, `this` perdido, `typeof null`
- [ ] **26 - Capstone** — JS na prática + entrevista: decision points, "como explicar em inglês", mapa de revisão, perguntas-modelo (deve costurar wikilinks pras 25 irmãs — confirmar cada um via `ls`)
- [ ] **Gate fase Magus:** commit por sub-lote; `/verificar-wikilinks`; corrigir quebras reais.

## Wave 4 — Teardown e integração

- [ ] **4.1 Reescrever `index.md`** como MOC das 3 fases (links pras 26), preservando links pra `Testes em JavaScript`, `Validação`, `Biblioteca`, `Full Stack Open`, e "Veja também".
- [ ] **4.2 Aposentar o monólito** `JavaScript Fundamentals.md`: virar stub curto que aponta pra trilha (ou remover). Repointar inbounds (Sendas que citam `[[JavaScript Fundamentals]]`, índice do TypeScript que cita a base JS, `JavaScript/index`).
- [ ] **4.3 `/verificar-wikilinks 03-Dominios/Tecnologia/JavaScript`** — 0 quebras reais.
- [ ] **4.4 Atualizar o [[00-Meta/Roadmap|Roadmap]]:** mover JavaScript (core) de 🧱 para ✅; marcar Onda A item 1 concluído.
- [ ] **4.5 (Opcional) Ciclo de qualidade:** `/plantar-duvidas` → `/colher-duvidas` no galho; `/enriquecer-nota` com lente mídia nas Magus.
- [ ] **4.6 Commit final** + atualizar este plano para `status: done`.

---

## Self-review (cobertura do spec)

- Roster 26/26 → Waves 1–3 cobrem item a item ✓
- Seams (Node/Tooling/TS/Plataforma Web/Testes) → Global Constraints + linhas 17/19 ✓
- Dicionário de JavaScript → Wave 0 ✓
- Reescrita do index + aposentar monólito → Wave 4 ✓
- Escrita-fresca-com-pesquisa → Procedimento por nota passo 1 + Global Constraints ✓
- Atualização do Roadmap → Wave 4.4 ✓
