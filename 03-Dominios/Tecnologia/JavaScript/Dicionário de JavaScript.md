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

### TC39
Comitê técnico da ECMA International responsável por padronizar o ECMAScript. Reúne representantes de empresas (Google, Apple, Mozilla, Microsoft, Bloomberg, etc.) e contribuidores independentes. Toda proposta passa por 5 estágios: **Stage 0** (ideia); **Stage 1** (problema definido, champion designado); **Stage 2** (spec inicial rascunhada); **Stage 3** (spec completa, feedback de implementação em engines reais); **Stage 4** (aprovado para merge na spec anual — feature "pronta"). Features atingindo Stage 4 até o início de um ano entram no corte daquele ECMAScript (ex.: Stage 4 em março/2026 → ES2026). Ver [[24 - ES2026 e o futuro]] para exemplos concretos do processo.

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

### Temporal
Namespace global introduzido no ES2026 (Stage 4 em março/2026) que substitui a API `Date` com tipos imutáveis e timezone-aware. Cada tipo representa uma semântica distinta: `Temporal.Instant` (momento exato, timestamp UTC), `Temporal.ZonedDateTime` (data + hora + timezone, o mais completo), `Temporal.PlainDate` (data sem hora/tz, ex.: datas de nascimento), `Temporal.PlainTime`, `Temporal.PlainDateTime`, `Temporal.PlainYearMonth`, `Temporal.PlainMonthDay` e `Temporal.Duration`. Meses são **1-indexed** (12 = dezembro). Todos os métodos de modificação retornam novos objetos — nunca mutam o original. Shipping nativo: Firefox 139+ (mai/2025), Chrome/Edge 144+ (jan/2026), Node.js 26+ (mai/2026); Safari em Technology Preview. O polyfill `@js-temporal/polyfill` cobre Safari. Ver [[24 - ES2026 e o futuro#Temporal API: o Date finalmente consertado|ES2026 → Temporal]].

### using / Explicit Resource Management
Declaração introduzida no ES2026 (Stage 4 em junho/2025) que garante chamada automática de `Symbol.dispose` ao sair do escopo — seja por execução normal, `return`, `throw` ou `break`. Para recursos com cleanup assíncrono, usa-se `await using` (que chama `Symbol.asyncDispose`). Múltiplos recursos são descartados em ordem LIFO (último aberto, primeiro fechado). Se o `dispose` lançar enquanto já há um erro em voo, ambos são encapsulados em `SuppressedError { error, suppressed }` — nenhum contexto é perdido. Equivalente conceitual ao `with` do Python e ao `using` do C#. Para implementar: adicione `[Symbol.dispose]()` ou `[Symbol.asyncDispose]()` à sua classe. Ver [[24 - ES2026 e o futuro#Explicit Resource Management: `using` e `await using`|ES2026 → ERM]].

## Tipos e valores

### autoboxing
O mecanismo pelo qual o JavaScript envolve automaticamente um valor primitivo num objeto wrapper temporário (`String`, `Number`, `Boolean`) quando você acessa uma propriedade ou chama um método nele — e descarta o wrapper em seguida. É o que permite `"hello".toUpperCase()` funcionar sem que você precise escrever `new String("hello")`. Não se aplica a `null` e `undefined`.

### BigInt
Tipo primitivo introduzido no ES2020 para representar inteiros com **precisão arbitrária**, sem o teto de `Number.MAX_SAFE_INTEGER` (`2⁵³ − 1`). Criado com o sufixo `n` (`9007199254740993n`) ou via `BigInt(valor)`. Restrições fundamentais: não aceita decimais (`3n / 2n === 1n`, trunca), não se mistura com `number` em operações aritméticas (lança `TypeError`), e não é serializável com `JSON.stringify` (também lança `TypeError`). Comparação com `==` funciona por coerção (`3n == 3` é `true`), mas `===` não (`3n === 3` é `false`). Use para IDs além do safe range, criptografia e timestamps em nanossegundos.

### coerção
A conversão implícita de um valor de um tipo para outro, disparada por operadores (`+`, `==`) ou contextos (condições). A fonte de boa parte das armadilhas clássicas da linguagem.

### footgun
Jargão da área para uma funcionalidade de uma linguagem ou API que é válida e documentada, mas tão propensa a erros não-óbvios que o usuário acaba "atirando no próprio pé". Em JavaScript, os candidatos clássicos são o operador `==` (coerção silenciosa), `sort()` sem comparador (ordena como string) e `typeof null === "object"` (bug histórico). O termo não é exclusivo do JS — existe em toda a engenharia de software — mas a combinação de coerção implícita + herança legacy faz do JavaScript um campo especialmente fértil. Ver [[25 - Armadilhas e quirks]].

### IEEE 754
Padrão internacional que define a representação e aritmética de números em ponto flutuante. JavaScript usa **double-precision** (64 bits): 1 bit de sinal, 11 bits de expoente e 52 bits de mantissa (+ 1 implícito), totalizando ~15–17 dígitos decimais significativos. A consequência prática é que nem todo decimal base-10 tem representação binária exata — `0.1` em binário é uma dízima infinita truncada, o que explica `0.1 + 0.2 !== 0.3`. Inteiros são exatos até `2⁵³ − 1` (`Number.MAX_SAFE_INTEGER`); acima disso, dois inteiros distintos podem ter a mesma representação float. Valores especiais do padrão incluídos no `number` do JavaScript: `NaN`, `Infinity`, `-Infinity` e `-0`.

### Intl.NumberFormat
API nativa de formatação de números com suporte a locales, definida pelo padrão ECMA-402 (internacionalização do ECMAScript). Formata números como moeda, porcentagem, unidade de medida e notação compacta, seguindo as convenções do locale especificado. Criar o objeto tem custo (carrega tabelas de locale) — deve ser instanciado fora de laços e reutilizado. Disponível em todos os browsers modernos e Node.js desde a v13.
```js
new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(1234.56)
// "R$ 1.234,56"
```

### nullish coalescing (`??`)
Operador binário introduzido no ES2020 que retorna o operando direito apenas se o esquerdo for `null` ou `undefined`. Diferente de `||`, não considera `0`, `''`, `false` ou `NaN` como "ausentes" — esses valores legítimos são mantidos. Uso canônico: `const porta = config.port ?? 3000` preserva `port = 0`, enquanto `|| 3000` erroneamente usaria o padrão. Compõe naturalmente com optional chaining: `usuario?.perfil?.nome ?? 'Anônimo'`.

### optional chaining (`?.`)
Operador introduzido no ES2020 que curto-circuita o acesso a propriedades quando o receptor é `null` ou `undefined`, retornando `undefined` em vez de lançar `TypeError`. Funciona em três formas: acesso a propriedade (`obj?.prop`), acesso dinâmico (`obj?.[expr]`) e chamada de método (`obj?.method()`). O curto-circuito se propaga: `a?.b.c` não avalia `.c` se `a` for nullish. Substitui cadeias defensivas como `a && a.b && a.b.c`. Ver [[23 - Recursos modernos (ES2020 a ES2025)]] para contexto de uso.

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

## Metaprogramação

### Decorator (TC39)
Função que recebe um valor decorado (classe, método, campo ou acessor) mais um objeto `context` (com `.name`, `.kind`, `.metadata`, etc.) e opcionalmente retorna um substituto. A sintaxe usa `@` antes da declaração. Permite cross-cutting concerns (logging, validação, memoização, autorização) declarativamente, sem repetição no corpo de cada método. Stage 3 desde 2022; suportado via TypeScript 5.0+ (sem `experimentalDecorators`), Babel e Deno. **Atenção:** a spec Stage 3 é incompatível com o modo legado `experimentalDecorators: true` do TypeScript — APIs e semântica mudaram completamente; não misture as duas formas no mesmo projeto. Ver [[24 - ES2026 e o futuro#Decorators: metaprogramação declarativa em classes|ES2026 → Decorators]].

### metaprogramação
Técnica em que código observa, intercepta ou modifica o comportamento da própria linguagem em tempo de execução — sem alterar a lógica de negócio diretamente. Em JavaScript, os três pilares são: **Symbol** (chaves primitivas únicas que permitem ao objeto participar de protocolos nativos como `for...of` e `instanceof`), **Proxy** (intercepta operações fundamentais como leitura, escrita e deleção de propriedades) e **Reflect** (repassa a operação padrão com a semântica correta a partir de dentro de um trap). Ver [[22 - Metaprogramação]].

### Proxy
Objeto que envolve ("wraps") outro objeto (o *target*) e intercepta operações fundamentais por meio de funções chamadas *traps*, definidas em um *handler*. Criado com `new Proxy(target, handler)`. O motor JS executa o trap em vez da operação original; se o trap chamar `Reflect.<método>`, a operação padrão é repassada. Proxies são detectados como "megamórficos" pelo JIT do V8, o que gera overhead de 5–20% em hot paths — use fora de loops críticos. Ver [[22 - Metaprogramação#Proxy — interceptando operações fundamentais|Proxy]].

### Proxy.revocable
Variante de Proxy que retorna `{ proxy, revoke }`. Chamar `revoke()` desativa permanentemente o proxy — qualquer acesso posterior lança `TypeError: Cannot perform 'get' on a proxy that has been revoked`. Útil para tokens temporários de acesso, sandboxing de plugins e ciclos de vida explícitos via `Symbol.dispose` (ES2026). Ver [[22 - Metaprogramação#Proxy.revocable — Proxy com prazo de validade|Proxy.revocable]].

### Reflect
Objeto estático (sem construtor) cujos métodos espelham os traps de Proxy um-a-um: `Reflect.get`, `Reflect.set`, `Reflect.has`, `Reflect.apply`, `Reflect.construct`, etc. Dentro de um trap, usar `Reflect.<método>` em vez de `target[prop]` preserva o `receiver` correto (o `this` para getters em protótipos) e evita loops infinitos. `Reflect.ownKeys(obj)` é o único jeito nativo de listar todas as chaves próprias, incluindo Symbols.

### trap (armadilha de Proxy)
Função definida no `handler` de um `Proxy` que intercepta uma operação específica do motor JavaScript. Cada trap corresponde a um método interno (`[[Get]]`, `[[Set]]`, `[[Has]]`, etc.) da spec ECMAScript. O motor verifica **invariantes** após o retorno do trap — se o resultado violar uma propriedade `non-configurable` ou `non-writable` do target, lança `TypeError` automaticamente, independente do que o trap retornou.

### well-known Symbol
Symbol pré-definido no motor JavaScript (registrado em `Symbol.*`) que serve como "gancho" para protocolos nativos da linguagem. Os mais usados: `Symbol.iterator` (habilita `for...of`), `Symbol.asyncIterator` (`for await...of`), `Symbol.toPrimitive` (coerção de tipo), `Symbol.hasInstance` (`instanceof`), `Symbol.toStringTag` (tag em `Object.prototype.toString`), `Symbol.species` (construtor usado em métodos como `map`). Ver [[22 - Metaprogramação#Well-known Symbols — protocolos da linguagem|Well-known Symbols]].

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

### cópia profunda (deep copy)
Uma cópia onde todos os níveis da estrutura são duplicados — nenhum objeto interno é compartilhado entre o original e a cópia. Qualquer mutação em um lado não afeta o outro. Em JavaScript, `structuredClone()` é a solução nativa moderna (Baseline Widely Available em 2026); `JSON.parse(JSON.stringify())` funciona para dados JSON-safe mas perde tipos ricos (`Date` vira string, `Map`/`Set` viram `{}`/`[]`, `undefined` e funções somem). Veja detalhes em [[20 - Cópia, serialização e imutabilidade]].

### cópia rasa (shallow copy)
Uma cópia onde apenas o primeiro nível é duplicado — elementos primitivos são copiados por valor, mas elementos que são objetos ou arrays ainda compartilham a mesma referência. Em JavaScript, `[...arr]`, `arr.slice()` e `Array.from(arr)` produzem cópia rasa. Consequência: mutar um objeto dentro da cópia muta também o original. Para cópia que atravessa todos os níveis, use `structuredClone()`.

### imutabilidade
Propriedade de um valor ou estrutura que não pode ser alterada após a criação. Em JavaScript, primitivos são imutáveis por natureza. Objetos e arrays são mutáveis por padrão — `Object.freeze()` congela apenas o nível superficial; para imutabilidade profunda real é preciso `deepFreeze` recursivo ou bibliotecas como **Immer** (imutabilidade por convenção via `produce`) ou **Immutable.js** (coleções persistentes com [[Dicionário de JavaScript#structural sharing (compartilhamento estrutural)|structural sharing]]). A proposta TC39 de Records & Tuples (primitivos imutáveis com comparação por valor) foi retirada em abril de 2025. Veja em [[20 - Cópia, serialização e imutabilidade]].

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

### structural sharing (compartilhamento estrutural)
Técnica usada por bibliotecas de imutabilidade (Immer, Immutable.js) onde, ao "modificar" uma estrutura, apenas o caminho até o nó alterado é copiado — o restante da árvore é compartilhado entre a versão antiga e a nova. Isso torna atualizações imutáveis O(log n) em vez de O(n), evitando a necessidade de copiar estruturas inteiras a cada mudança. É o que torna Redux eficiente com estado profundo. Veja contexto em [[20 - Cópia, serialização e imutabilidade]].

### WeakMap
Variante de Map onde as chaves devem ser objetos e são mantidas por referência fraca. O GC pode coletar a chave (e a entrada correspondente) quando não houver outras referências ao objeto-chave. Não é iterável — não expõe `.size`, `.keys()` ou `.entries()`.

### WeakRef
Referência fraca a um objeto (ES2021): não impede a coleta pelo GC. O objeto-alvo é acessado via `.deref()`, que retorna `undefined` se já foi coletado. A semântica é intencionalmente não-determinística — o GC pode coletar o objeto a qualquer momento após ele perder todas as referências fortes, e o tempo varia por motor, geração e pressão de memória. Use apenas como otimização não-crítica (ex: caches best-effort). Para lógica de negócio, sempre trate o retorno `undefined`. Prefira [[Dicionário de JavaScript#WeakMap\|WeakMap]] quando a associação é objeto→dado.

### WeakSet
Variante de Set onde os valores devem ser objetos mantidos por referência fraca. Usado para rastrear conjuntos de objetos sem impedir sua coleta pelo GC. Não é iterável.

## Memória e GC

### FinalizationRegistry
API (ES2021) que permite registrar um callback a ser chamado *após* um objeto ser coletado pelo GC. O callback recebe um valor de limpeza (*held value*) previamente registrado. Semântica não-garantida: a spec permite que o callback seja chamado muito tarde, raramente ou nunca — por questões de portabilidade entre engines e para evitar timing attacks via observabilidade do GC. Use apenas para cleanup não-crítico (logs, debugging). Para recursos críticos (handles de arquivo, conexões), use `try/finally`, `Symbol.dispose` (ES2026) ou métodos `dispose()`/`close()` explícitos. Ver [[21 - Memory management]].

### GC roots (raízes do GC)
Conjunto de pontos de ancoragem a partir dos quais o garbage collector percorre o grafo de referências para determinar o que é alcançável. Em JavaScript: variáveis globais (`window`, `globalThis`), a call stack atual (variáveis locais de funções em execução), closures ativas e referências internas do motor (inline caches). Qualquer objeto alcançável a partir de um root está protegido da coleta; objetos sem caminho de referência até nenhum root são elegíveis para liberação.

### mark-and-sweep
Algoritmo base de coleta de lixo em JavaScript: (1) o GC parte dos roots, percorre o grafo de referências e *marca* todos os objetos alcançáveis; (2) percorre o heap e *libera* os não-marcados. Resolve referências circulares porque o critério é alcançabilidade, não contagem de referências. O V8 usa uma versão incremental e concurrent desse algoritmo no old generation (projeto Orinoco). Ver [[21 - Memory management]].

### reachability (alcançabilidade)
Critério usado pelo GC para decidir o que pode ser liberado: um objeto é *alcançável* se existe algum caminho de referência partindo de um [[Dicionário de JavaScript#GC roots (raízes do GC)\|root]] até ele. O conceito substitui a noção intuitiva de "objeto ainda está sendo usado" — um objeto pode estar sendo "guardado" mas nunca mais ser acessado, e ainda assim bloquear a coleta enquanto houver referência forte.

### retained size (tamanho retido)
No contexto de heap profiling (DevTools Memory, `v8.writeHeapSnapshot()`): a quantidade total de memória que seria liberada se um determinado objeto fosse coletado — incluindo todos os objetos que só são alcançáveis *através* dele. Contrasta com *shallow size* (apenas a memória do objeto em si, sem o que ele referencia). Um objeto com shallow size de 64 bytes mas retained size de 20 MB está "segurando" a vida de muita coisa. Métrica essencial para priorizar investigações de vazamento. Ver [[21 - Memory management]].

## Assíncrono

### AbortController
Interface da Web API que permite cancelar operações assíncronas (como `fetch`) que suportam `AbortSignal`. O controller expõe um `signal` que é passado para a operação e um método `abort()` que dispara o cancelamento. Métodos estáticos modernos: `AbortSignal.timeout(ms)` cria um sinal que aborta automaticamente após o prazo; `AbortSignal.any([s1, s2])` combina múltiplos sinais em um, abortando quando qualquer deles disparar. Suporte: browsers modernos (Chrome 66+) e Node.js 15+.

### async iterator
Objeto que implementa o protocolo de iteração assíncrona: possui um método `[Symbol.asyncIterator]()` que retorna um objeto com `.next()` retornando uma Promise de `{ value, done }`. Consumível via `for await...of`. Generators assíncronos (`async function*`) implementam o protocolo automaticamente. Diferentemente de iterables síncronos, cada passo pode aguardar I/O antes de produzir o próximo valor.

### executor
Função passada como argumento para `new Promise(executor)`. É chamada **sincronamente** no momento da criação da Promise e recebe dois callbacks: `resolve` (para marcar a Promise como fulfilled com um valor) e `reject` (para rejeitá-la com um motivo). Qualquer código após chamar `resolve` ou `reject` ainda executa — use `return` para encerrar o executor após a decisão. Erros lançados dentro do executor são automaticamente convertidos em rejeição da Promise.

### Promise
Objeto que representa o resultado eventual de uma operação assíncrona, em um de três estados: pending, fulfilled ou rejected. Base sintática de `async/await`.

### Promise.withResolvers
Método estático introduzido no ES2024 que retorna um objeto com três propriedades: `{ promise, resolve, reject }`. Evita o padrão verbose de vazar `resolve`/`reject` para fora do construtor via variáveis auxiliares. Útil para integrar callbacks legados com código baseado em Promise ou para criar canais de sinalização entre partes assíncronas desconexas. Internamente equivale a criar uma Promise cujo executor apenas captura as referências.

### thenable
Qualquer objeto que possua um método `.then(onFulfilled, onRejected)`, independente de ser uma Promise nativa. O algoritmo `Promise.resolve()` detecta thenables e os "assimila" — chama `.then(resolve, reject)` e adota o estado resultante. Isso garante interoperabilidade com bibliotecas Promise de terceiros (jQuery Deferred, Bluebird, etc.) sem conversão explícita. A spec ECMAScript define thenable assimilation em §27.2.1.1.

## Módulos

### ESM (ECMAScript Modules)
O sistema de módulos nativo da linguagem (`import`/`export`), com bindings vivos (live bindings) e escopo de módulo. A resolução e o interop com CommonJS são detalhe de tooling — ver [[03-Dominios/Tecnologia/Tooling e Build/06 - ESM e CJS e o sistema de módulos|Tooling 06]].

### live binding
Em ESM, um `import` é uma referência viva ao slot de memória do export, não uma cópia: se o módulo exportador atualiza o valor, o importador enxerga a mudança.
