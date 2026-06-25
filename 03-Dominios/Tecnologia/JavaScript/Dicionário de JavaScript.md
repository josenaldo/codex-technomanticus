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

### BigInt
Tipo primitivo introduzido no ES2020 para representar inteiros com **precisão arbitrária**, sem o teto de `Number.MAX_SAFE_INTEGER` (`2⁵³ − 1`). Criado com o sufixo `n` (`9007199254740993n`) ou via `BigInt(valor)`. Restrições fundamentais: não aceita decimais (`3n / 2n === 1n`, trunca), não se mistura com `number` em operações aritméticas (lança `TypeError`), e não é serializável com `JSON.stringify` (também lança `TypeError`). Comparação com `==` funciona por coerção (`3n == 3` é `true`), mas `===` não (`3n === 3` é `false`). Use para IDs além do safe range, criptografia e timestamps em nanossegundos.

### coerção
A conversão implícita de um valor de um tipo para outro, disparada por operadores (`+`, `==`) ou contextos (condições). A fonte de boa parte das armadilhas clássicas da linguagem.

### IEEE 754
Padrão internacional que define a representação e aritmética de números em ponto flutuante. JavaScript usa **double-precision** (64 bits): 1 bit de sinal, 11 bits de expoente e 52 bits de mantissa (+ 1 implícito), totalizando ~15–17 dígitos decimais significativos. A consequência prática é que nem todo decimal base-10 tem representação binária exata — `0.1` em binário é uma dízima infinita truncada, o que explica `0.1 + 0.2 !== 0.3`. Inteiros são exatos até `2⁵³ − 1` (`Number.MAX_SAFE_INTEGER`); acima disso, dois inteiros distintos podem ter a mesma representação float. Valores especiais do padrão incluídos no `number` do JavaScript: `NaN`, `Infinity`, `-Infinity` e `-0`.

### Intl.NumberFormat
API nativa de formatação de números com suporte a locales, definida pelo padrão ECMA-402 (internacionalização do ECMAScript). Formata números como moeda, porcentagem, unidade de medida e notação compacta, seguindo as convenções do locale especificado. Criar o objeto tem custo (carrega tabelas de locale) — deve ser instanciado fora de laços e reutilizado. Disponível em todos os browsers modernos e Node.js desde a v13.
```js
new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(1234.56)
// "R$ 1.234,56"
```

### NaN
*Not a Number* — valor especial do padrão IEEE 754 produzido por operações aritméticas indeterminadas (`0/0`, `Math.sqrt(-1)`, `Number("abc")`). Propriedade única no JavaScript: `NaN !== NaN` (`NaN` é o único valor não igual a si mesmo). Para detectar corretamente, use `Number.isNaN(valor)` — nunca compare diretamente com `NaN` nem use o global `isNaN()` (que coerce o argumento antes de testar). `NaN` é "contagioso": qualquer operação com ele produz `NaN`. Em contexto booleano, é *falsy*. `Map` e `Set` tratam `NaN` como chave válida via [[Dicionário de JavaScript#SameValueZero\|SameValueZero]] (`NaN === NaN` é `true` nesse algoritmo).

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

### AbortController
Interface da Web API que permite cancelar operações assíncronas (como `fetch`) que suportam `AbortSignal`. O controller expõe um `signal` que é passado para a operação e um método `abort()` que dispara o cancelamento. Métodos estáticos modernos: `AbortSignal.timeout(ms)` cria um sinal que aborta automaticamente após o prazo; `AbortSignal.any([s1, s2])` combina múltiplos sinais em um, abortando quando qualquer deles disparar. Suporte: browsers modernos (Chrome 66+) e Node.js 15+.

### async iterator
Objeto que implementa o protocolo de iteração assíncrona: possui um método `[Symbol.asyncIterator]()` que retorna um objeto com `.next()` retornando uma Promise de `{ value, done }`. Consumível via `for await...of`. Generators assíncronos (`async function*`) implementam o protocolo automaticamente. Diferentemente de iterables síncronos, cada passo pode aguardar I/O antes de produzir o próximo valor.

### executor
Função passada como argumento para `new Promise(executor)`. É chamada **sincronamente** no momento da criação da Promise e recebe dois callbacks: `resolve` (para marcar a Promise como fulfilled com um valor) e `reject` (para rejeitá-la com um motivo). Qualquer código após chamar `resolve` ou `reject` ainda executa — use `return` para encerrar o executor após a decisão. Erros lançados dentro do executor são automaticamente convertidos em rejeição da Promise.

### Promise
Objeto que representa o resultado eventual de uma operação assíncrona, em um de três estados: pending, fulfilled ou rejected. Base sintática de `async/await`.

### thenable
Qualquer objeto que possua um método `.then(onFulfilled, onRejected)`, independente de ser uma Promise nativa. O algoritmo `Promise.resolve()` detecta thenables e os "assimila" — chama `.then(resolve, reject)` e adota o estado resultante. Isso garante interoperabilidade com bibliotecas Promise de terceiros (jQuery Deferred, Bluebird, etc.) sem conversão explícita. A spec ECMAScript define thenable assimilation em §27.2.1.1.

## Módulos

### ESM (ECMAScript Modules)
O sistema de módulos nativo da linguagem (`import`/`export`), com bindings vivos (live bindings) e escopo de módulo. A resolução e o interop com CommonJS são detalhe de tooling — ver [[03-Dominios/Tecnologia/Tooling e Build/06 - ESM e CJS e o sistema de módulos|Tooling 06]].

### live binding
Em ESM, um `import` é uma referência viva ao slot de memória do export, não uma cópia: se o módulo exportador atualiza o valor, o importador enxerga a mudança.
