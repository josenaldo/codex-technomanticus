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

### hidden class
Estrutura interna (também chamada *shape* ou *map*) que o V8 cria para rastrear o formato de um objeto JavaScript — quais propriedades existem e em que offset de memória cada uma fica. Objetos com as mesmas propriedades na mesma ordem compartilham uma hidden class, permitindo que o JIT faça acesso direto à memória em vez de buscas dinâmicas. Mudar a ordem das propriedades, adicionar propriedades após a criação ou usar `delete` cria novas hidden classes e pode causar deoptimização.

### hoisting
O comportamento pelo qual declarações de `var` e funções são "elevadas" ao topo do escopo durante a fase de criação, antes da execução. `let`/`const` também são hoisted, mas ficam na TDZ até a declaração.

### JIT (Just-In-Time)
Técnica das engines modernas (V8, JSC, SpiderMonkey) que compila o JavaScript para código de máquina em tempo de execução, otimizando os caminhos quentes em vez de interpretar tudo.

### microtask
Unidade de trabalho assíncrono com prioridade sobre tarefas comuns (macrotasks): callbacks de Promise e `queueMicrotask` rodam ao esvaziar a call stack, antes do próximo render ou timer.

### TDZ (Temporal Dead Zone)
A janela entre o início do escopo e a linha de declaração de uma variável `let`/`const`, na qual acessá-la lança `ReferenceError`. É o que distingue o hoisting de `let`/`const` do de `var`.

## Tipos e valores

### autoboxing
O mecanismo pelo qual o JavaScript envolve automaticamente um valor primitivo num objeto wrapper temporário (`String`, `Number`, `Boolean`) quando você acessa uma propriedade ou chama um método nele — e descarta o wrapper em seguida. É o que permite `"hello".toUpperCase()` funcionar sem que você precise escrever `new String("hello")`. Não se aplica a `null` e `undefined`.

### coerção
A conversão implícita de um valor de um tipo para outro, disparada por operadores (`+`, `==`) ou contextos (condições). A fonte de boa parte das armadilhas clássicas da linguagem.

### primitivo
Um dos 7 tipos de valor imutável: `string`, `number`, `bigint`, `boolean`, `undefined`, `symbol`, `null`. Tudo que não é primitivo é `object`.

### ToPrimitive
Algoritmo interno da spec (ECMAScript §7.1.1) que converte um objeto para um valor primitivo quando necessário (em `+`, `==`, template literals, operações aritméticas). Recebe um `hint` (`"number"`, `"string"` ou `"default"`) que determina a ordem de chamada: hint `"number"` tenta `valueOf()` primeiro; hint `"string"` tenta `toString()` primeiro. Pode ser sobrescrito via `Symbol.toPrimitive`. `Date` é a única exceção nativa: trata hint `"default"` como `"string"`.

### truthy/falsy
Como um valor é avaliado em contexto booleano. Os falsy são exatamente: `false`, `0`, `-0`, `0n`, `""`, `null`, `undefined`, `NaN`. Todo o resto é truthy.

## Funções e escopo

### arrow function
Sintaxe de função introduzida no ES6 (`=>`). Diferencia-se das funções regulares em três aspectos fundamentais: não tem `this` próprio (herda o `this` léxico do escopo onde foi criada), não tem o objeto `arguments`, e não pode ser usada como construtora com `new`.

### closure
Função que "lembra" o escopo léxico onde foi criada, mantendo acesso às variáveis daquele escopo mesmo depois que ele terminou de executar. Base de module pattern, currying e memoização.

### debounce
Técnica que adia a execução de uma função até que um determinado tempo de inatividade passe após a última invocação. Em vez de executar a cada disparo (ex: cada keystroke), aguarda o "silêncio" de N ms antes de agir. Implementado via closure que mantém um `timer` entre chamadas: cada nova invocação cancela o timer anterior e agenda um novo. Ver padrão em [[10 - Closures]].

### escopo de bloco
Regra aplicada a `let` e `const`: a variável existe apenas dentro do par de `{}` onde foi declarada. Qualquer `if`, `for`, `while` ou bloco avulso cria uma barreira — a variável não vaza para fora.

### escopo de função
Regra aplicada a `var`: a variável existe em toda a função onde foi declarada, independente do bloco onde está. Blocos `if`, `for` e similares não criam barreiras para `var` — apenas `function` cria.

### escopo léxico
A regra de que o escopo de uma variável é determinado pela posição dela no código-fonte (onde foi escrita), não por onde a função é chamada. É o que torna closures previsíveis.

### first-class function (função de primeira classe)
Propriedade de uma linguagem em que funções são tratadas como valores de pleno direito: podem ser atribuídas a variáveis, passadas como argumentos e retornadas de outras funções — exatamente como números ou strings. JavaScript é uma linguagem com funções de primeira classe.

### higher-order function (função de ordem superior)
Função que recebe outra função como argumento, retorna uma função, ou ambos. `Array.prototype.map`, `filter` e `reduce` são os exemplos mais conhecidos. É uma consequência natural das funções de primeira classe.

### IIFE (Immediately Invoked Function Expression)
Função que é definida e executada imediatamente na mesma expressão: `(function() { ... })()`. Cria um escopo privado para variáveis sem poluir o escopo global. Padrão legado substituído em boa parte por módulos ESM e `let`/`const`, mas ainda presente em código mais antigo.

### rest parameter (parâmetro rest)
Sintaxe `...nome` na assinatura de uma função que coleta todos os argumentos excedentes em um **Array real**. Substitui o objeto legado `arguments` (que não é um array). Deve ser o último parâmetro da lista: `function fn(a, b, ...resto)`.

### scope chain (cadeia de escopos)
A sequência de Environment Records percorrida pelo motor para resolver um nome de variável: do escopo mais interno ao mais externo, até o global. Se o nome não for encontrado em nenhum nível, lança `ReferenceError`.

### shadowing (sombreamento)
Quando uma variável em um escopo interno declara o mesmo nome de uma variável em escopo externo. A variável interna "cobre" a externa dentro de seu escopo, sem modificá-la.

### strict mode (modo estrito)
Modo de execução ativado com a diretiva `"use strict"` (no topo de um arquivo ou função) ou automaticamente em módulos ESM e corpos de classe. Em strict mode: funções chamadas sem contexto têm `this === undefined` em vez de receber o objeto global; atribuições a variáveis não declaradas lançam `ReferenceError`; e vários comportamentos silenciosamente problemáticos do JavaScript legado se tornam erros explícitos.

## Objetos e protótipos

### accessor descriptor (descriptor acessor)
Tipo de descriptor de propriedade que define `get` e/ou `set` em vez de um `value`. Quando a propriedade é lida, o getter executa; quando é escrita, o setter executa. Incompatível com data descriptor — tentar combinar `get` com `value` ou `writable` no mesmo `Object.defineProperty` lança `TypeError`. Compartilha `enumerable` e `configurable` com o data descriptor.

### data descriptor (descriptor de dado)
Tipo de descriptor de propriedade que armazena um `value` diretamente e controla se ele pode ser alterado via `writable`. Incompatível com accessor descriptor — não pode coexistir com `get` ou `set` no mesmo descriptor. Compartilha `enumerable` e `configurable` com o accessor descriptor.

### Object.hasOwn
Método estático introduzido no ES2022 que verifica se um objeto possui uma propriedade própria (não herdada) sem os riscos de `hasOwnProperty`. Funciona corretamente para objetos sem protótipo (`Object.create(null)`) e para objetos onde `hasOwnProperty` foi sobrescrito como propriedade própria. Uso recomendado: `Object.hasOwn(obj, "chave")` em vez de `obj.hasOwnProperty("chave")`.

### prototype chain
A cadeia de objetos pela qual o JavaScript resolve propriedades: se um objeto não tem a propriedade, busca no seu `[[Prototype]]`, e assim por diante até `null`. É o mecanismo de herança da linguagem.

### structuredClone
Função global (disponível desde 2022 em browsers modernos e Node.js 17+) que cria uma cópia profunda de um objeto, incluindo todos os níveis aninhados. Suporta `Map`, `Set`, `Date`, `RegExp` e referências circulares. Diferente de `JSON.parse(JSON.stringify())`, preserva os tipos originais. Lança `TypeError` ao tentar clonar funções ou nós do DOM.

### this
Referência cujo valor é determinado por *como* a função é chamada (não onde é definida): binding default, implícito, explícito (`call`/`apply`/`bind`) ou `new`. Arrow functions não têm `this` próprio — herdam do escopo léxico.

## Coleções

### cópia rasa (shallow copy)
Uma cópia onde apenas o primeiro nível é duplicado — elementos primitivos são copiados por valor, mas elementos que são objetos ou arrays ainda compartilham a mesma referência. Em JavaScript, `[...arr]`, `arr.slice()` e `Array.from(arr)` produzem cópia rasa. Consequência: mutar um objeto dentro da cópia muta também o original. Para cópia que atravessa todos os níveis, use `structuredClone()`.

### Iterator Helpers
Conjunto de métodos introduzidos no ES2025 em `Iterator.prototype` que permitem pipelines lazy sobre qualquer iterável: `filter()`, `map()`, `flatMap()`, `take()`, `drop()`, `reduce()`, `forEach()`, `some()`, `find()`, `toArray()`. Diferente dos métodos de array, são **lazy** — processam um elemento por vez sem criar arrays intermediários, o que reduz uso de memória para conjuntos grandes. Disponível em Node 22 LTS+, Bun 1.1.31+ e browsers modernos (Baseline Newly Available, março 2025). `Iterator.from(qualquerIteravel)` envolve qualquer iterável na cadeia.

### Map
Coleção de pares chave→valor onde a chave pode ser de qualquer tipo (objeto, número, função, etc.), ao contrário do objeto puro que coerce tudo para string. Preserva ordem de inserção e expõe `.size` nativo. Usa SameValueZero para comparação de chaves.

### method chaining (encadeamento de métodos)
Padrão onde chamadas de método são encadeadas diretamente no retorno da chamada anterior, formando uma pipeline de transformações legível da esquerda para a direita. Possível em arrays porque `map`, `filter`, `slice`, `flat` e similares retornam novos arrays. Custo: cada método na cadeia cria um array intermediário completo — para volumes grandes, [[Dicionário de JavaScript#Iterator Helpers\|Iterator Helpers]] (ES2025) eliminam esse overhead com avaliação lazy.

### Set
Coleção de valores únicos com inserção ordenada. Adicionar um valor já existente é ignorado. A partir do ES2025, suporta métodos nativos de teoria dos conjuntos: `.union()`, `.intersection()`, `.difference()`, `.symmetricDifference()`, `.isSubsetOf()`, `.isSupersetOf()`, `.isDisjointFrom()`.

### SameValueZero
Algoritmo de comparação de igualdade usado por Map e Set: idêntico a `===` exceto que `NaN === NaN` é `true`. É o motivo pelo qual `NaN` pode ser usado como chave de Map de forma confiável.

### WeakMap
Variante de Map onde as chaves devem ser objetos e são mantidas por referência fraca. O GC pode coletar a chave (e a entrada correspondente) quando não houver outras referências ao objeto-chave. Não é iterável — não expõe `.size`, `.keys()` ou `.entries()`.

### WeakSet
Variante de Set onde os valores devem ser objetos mantidos por referência fraca. Usado para rastrear objetos sem impedir sua coleta pelo GC. Não é iterável.

## Assíncrono

### Promise
Objeto que representa o resultado eventual de uma operação assíncrona, em um de três estados: pending, fulfilled ou rejected. Base sintática de `async/await`.

## Módulos

### ESM (ECMAScript Modules)
O sistema de módulos nativo da linguagem (`import`/`export`), com bindings vivos (live bindings) e escopo de módulo. A resolução e o interop com CommonJS são detalhe de tooling — ver [[03-Dominios/Tecnologia/Tooling e Build/06 - ESM e CJS e o sistema de módulos|Tooling 06]].

### live binding
Em ESM, um `import` é uma referência viva ao slot de memória do export, não uma cópia: se o módulo exportador atualiza o valor, o importador enxerga a mudança.
