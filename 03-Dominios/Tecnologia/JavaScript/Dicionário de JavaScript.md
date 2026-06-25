---
title: "Dicionário de JavaScript"
created: 2026-06-25
updated: 2026-06-25
type: glossary
status: seedling
aliases: []
tags:
  - glossary
  - javascript
  - frontend
lang: pt
publish: true
---

# Dicionário de JavaScript

> Termos e conceitos da linguagem JavaScript: execução, tipos, escopo, protótipos, assíncrono e módulos. Os internals do runtime vivem em [[03-Dominios/Tecnologia/Node/index|Node]]; a tipagem estática em [[03-Dominios/Tecnologia/TypeScript/index|TypeScript]].

## Linguagem e execução

### ECMAScript
A especificação que define a linguagem JavaScript, mantida pelo TC39 e publicada anualmente (ES2015, ES2016, …). "JavaScript" é a implementação dessa spec pelas engines; "ECMAScript" é o contrato.

### event loop
O mecanismo que coordena a execução de código síncrono e a fila de tarefas assíncronas numa thread única. A *spec* da linguagem define só a fila de jobs (microtasks); as fases completas são detalhe do runtime — ver [[03-Dominios/Tecnologia/Node/Runtime e Event Loop/index|Node/Runtime e Event Loop]].

### hoisting
O comportamento pelo qual declarações de `var` e funções são "elevadas" ao topo do escopo durante a fase de criação, antes da execução. `let`/`const` também são hoisted, mas ficam na TDZ até a declaração.

### JIT (Just-In-Time)
Técnica das engines modernas (V8, JSC, SpiderMonkey) que compila o JavaScript para código de máquina em tempo de execução, otimizando os caminhos quentes em vez de interpretar tudo.

### microtask
Unidade de trabalho assíncrono com prioridade sobre tarefas comuns (macrotasks): callbacks de Promise e `queueMicrotask` rodam ao esvaziar a call stack, antes do próximo render ou timer.

### TDZ (Temporal Dead Zone)
A janela entre o início do escopo e a linha de declaração de uma variável `let`/`const`, na qual acessá-la lança `ReferenceError`. É o que distingue o hoisting de `let`/`const` do de `var`.

## Tipos e valores

### coerção
A conversão implícita de um valor de um tipo para outro, disparada por operadores (`+`, `==`) ou contextos (condições). A fonte de boa parte das armadilhas clássicas da linguagem.

### primitivo
Um dos 7 tipos de valor imutável: `string`, `number`, `bigint`, `boolean`, `undefined`, `symbol`, `null`. Tudo que não é primitivo é `object`.

### truthy/falsy
Como um valor é avaliado em contexto booleano. Os falsy são exatamente: `false`, `0`, `-0`, `0n`, `""`, `null`, `undefined`, `NaN`. Todo o resto é truthy.

## Funções e escopo

### closure
Função que "lembra" o escopo léxico onde foi criada, mantendo acesso às variáveis daquele escopo mesmo depois que ele terminou de executar. Base de module pattern, currying e memoização.

### escopo léxico
A regra de que o escopo de uma variável é determinado pela posição dela no código-fonte (onde foi escrita), não por onde a função é chamada. É o que torna closures previsíveis.

## Objetos e protótipos

### prototype chain
A cadeia de objetos pela qual o JavaScript resolve propriedades: se um objeto não tem a propriedade, busca no seu `[[Prototype]]`, e assim por diante até `null`. É o mecanismo de herança da linguagem.

### this
Referência cujo valor é determinado por *como* a função é chamada (não onde é definida): binding default, implícito, explícito (`call`/`apply`/`bind`) ou `new`. Arrow functions não têm `this` próprio — herdam do escopo léxico.

## Assíncrono

### Promise
Objeto que representa o resultado eventual de uma operação assíncrona, em um de três estados: pending, fulfilled ou rejected. Base sintática de `async/await`.

## Módulos

### ESM (ECMAScript Modules)
O sistema de módulos nativo da linguagem (`import`/`export`), com bindings vivos (live bindings) e escopo de módulo. A resolução e o interop com CommonJS são detalhe de tooling — ver [[03-Dominios/Tecnologia/Tooling e Build/06 - ESM e CJS e o sistema de módulos|Tooling 06]].

### live binding
Em ESM, um `import` é uma referência viva ao slot de memória do export, não uma cópia: se o módulo exportador atualiza o valor, o importador enxerga a mudança.
