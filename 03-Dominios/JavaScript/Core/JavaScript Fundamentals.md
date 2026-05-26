---
title: "JavaScript Fundamentals"
created: 2026-04-01
updated: 2026-04-11
type: concept
status: evergreen
tags:
  - javascript
  - entrevista
publish: false
---

# JavaScript Fundamentals

Guia comprehensive da linguagem JavaScript moderna — do modelo de execução (event loop, call stack, microtasks) aos recursos mais recentes do ES2025/ES2026. Para um senior fullstack, dominar JavaScript significa entender **como a linguagem realmente funciona por baixo**, não apenas a sintaxe. Para tipagem estática, ver [[TypeScript]]. Para concorrência e Node.js-specific, ver [[Node.js]]. Para testes, ver [[Testes em JavaScript]].

## O que é

JavaScript é uma linguagem **dinâmica**, **fracamente tipada**, **interpretada (JIT compiled)**, com **garbage collection** e **closures de primeira classe**. Criada por **Brendan Eich em 1995** em 10 dias, padronizada como **ECMAScript (ECMA-262)**. Roda no browser, servidor (Node.js, Deno, Bun), edge (Cloudflare Workers), mobile (React Native), e até microcontroladores.

Em 2026, é a **linguagem mais usada do mundo**, e TypeScript é a **primeira linguagem do GitHub**. Entender JavaScript profundamente é pré-requisito para produtividade real no ecossistema.

Em entrevistas, o que diferencia um senior em JavaScript:

1. **Entender o event loop** — macrotasks, microtasks, render phase, starvation
2. **Dominar closures, `this` e prototypes** — os 3 conceitos mais mal compreendidos
3. **Async moderno** — Promises, async/await, AsyncIterator, cancellation
4. **Tipos e coerção** — por que `[] == ![]` é true e outras pegadinhas
5. **Modules** — ESM vs CJS, dynamic import, module graph, tree shaking
6. **Memory management** — heap, retenção, leaks, WeakMap/WeakRef
7. **Features modernas** — ES2020+ até ES2026 (Temporal, Iterator Helpers, Resource Management)
8. **Runtime diferences** — V8 (Chrome, Node), SpiderMonkey (Firefox), JavaScriptCore (Safari), Bun

---

## O modelo de execução

### Call stack, heap e queues

JavaScript é **single-threaded** com **event loop**. Isso significa: uma thread executa seu código, operações assíncronas vão para filas, e o event loop decide o que rodar em seguida.

```
┌─────────────────────────────────────────────────────────────┐
│ Runtime JavaScript                                           │
│                                                              │
│  ┌──────────────┐     ┌────────────────────────────────┐    │
│  │ Call Stack   │     │ Heap                           │    │
│  │              │     │  (objetos, closures,           │    │
│  │  [frame 3]   │     │   funções, arrays, ...)        │    │
│  │  [frame 2]   │     │                                │    │
│  │  [frame 1]   │     │                                │    │
│  └──────┬───────┘     └────────────────────────────────┘    │
│         │                                                    │
│         ↓ (quando vazio)                                     │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Event Loop                                            │   │
│  │                                                       │   │
│  │  1. Executa uma macrotask                            │   │
│  │  2. Processa TODAS as microtasks                     │   │
│  │  3. Render (se no browser)                           │   │
│  │  4. Volta ao passo 1                                 │   │
│  └──────────────────────────────────────────────────────┘   │
│         ↑                            ↑                       │
│         │                            │                       │
│  ┌──────┴──────┐            ┌────────┴──────────┐           │
│  │  Macrotask  │            │    Microtask      │           │
│  │  Queue      │            │    Queue          │           │
│  │             │            │                   │           │
│  │ setTimeout  │            │ Promise.then      │           │
│  │ setInterval │            │ queueMicrotask    │           │
│  │ I/O         │            │ MutationObserver  │           │
│  │ UI events   │            │                   │           │
│  └─────────────┘            └───────────────────┘           │
└─────────────────────────────────────────────────────────────┘
```

**Call stack** — pilha de frames de execução. Cada chamada de função empilha um frame; cada `return` desempilha.

**Heap** — onde objetos, closures, funções e arrays vivem. Gerenciado pelo GC.

**Task queue (macrotask)** — fila de "tasks" pendentes: callbacks de `setTimeout`, `setInterval`, I/O do Node, eventos DOM.

**Microtask queue** — fila de maior prioridade: `Promise.then`, `queueMicrotask`, `MutationObserver`.

**Event loop** — o loop que orquestra tudo. Ciclo simplificado:

1. Pega a **próxima macrotask** do queue e executa até o call stack esvaziar
2. Processa **todas** as microtasks acumuladas (drena a queue)
3. (Browser) Faz render/layout/paint se necessário
4. Volta ao passo 1

**Consequência crítica:** microtasks têm prioridade. Se você enfileira microtasks dentro de microtasks, elas rodam antes da próxima macrotask. Isso pode causar **starvation** da macrotask queue.

### Exemplo clássico — ordem de execução

```javascript
console.log("1");

setTimeout(() => console.log("2"), 0);

Promise.resolve().then(() => console.log("3"));

console.log("4");

// Saída: 1, 4, 3, 2
```

**Por quê:**

1. `console.log("1")` — sync
2. `setTimeout(..., 0)` — enfileira macrotask
3. `Promise.resolve().then(...)` — enfileira microtask
4. `console.log("4")` — sync
5. Call stack vazio → drena microtasks → `"3"`
6. Próxima macrotask → `"2"`

### Microtask starvation

```javascript
// RUIM — macrotask nunca roda
function recursiveMicrotask() {
    queueMicrotask(recursiveMicrotask);
}
recursiveMicrotask();
setTimeout(() => console.log("nunca"), 0);
```

Microtasks infinitas impedem o event loop de avançar. Em Node, causa alta CPU sem I/O. Em browser, UI congela.

### Node.js event loop — mais detalhado

Node.js tem **fases** distintas no event loop (libuv):

```
   ┌───────────────────────────┐
┌─►│           timers          │  setTimeout, setInterval
│  └─────────────┬─────────────┘
│  ┌─────────────┴─────────────┐
│  │     pending callbacks     │  I/O errors retidos
│  └─────────────┬─────────────┘
│  ┌─────────────┴─────────────┐
│  │       idle, prepare       │
│  └─────────────┬─────────────┘    ┌───────────────┐
│  ┌─────────────┴─────────────┐    │   incoming:   │
│  │           poll            │◄───┤ connections,  │
│  └─────────────┬─────────────┘    │   data, etc.  │
│  ┌─────────────┴─────────────┐    └───────────────┘
│  │           check           │  setImmediate
│  └─────────────┬─────────────┘
│  ┌─────────────┴─────────────┐
└──┤      close callbacks      │  'close' events
   └───────────────────────────┘
```

**Microtasks** (`process.nextTick`, Promise callbacks) rodam **entre cada fase**. `process.nextTick` é ainda mais prioritário que `Promise.then` em Node.

**`setImmediate` vs `setTimeout(fn, 0)`:**

```javascript
// Em contexto I/O, setImmediate roda primeiro
fs.readFile('file', () => {
    setTimeout(() => console.log('timeout'), 0);
    setImmediate(() => console.log('immediate'));
    // → imprime 'immediate' primeiro
});
```

---

## Variáveis e escopo

### var, let, const

```javascript
var a = 1;    // function-scoped, hoisted, pode redeclarar
let b = 2;    // block-scoped, temporal dead zone, não pode redeclarar
const c = 3;  // como let, mas não pode reassignar
```

**`var` — evite em código novo.**

```javascript
function exemplo() {
    console.log(x);  // undefined (hoisted)
    var x = 10;

    if (true) {
        var y = 20;
    }
    console.log(y);  // 20 — var vaza para fora do bloco
}
```

**`let` e `const` — default moderno.**

```javascript
{
    let x = 10;
}
console.log(x);  // ReferenceError — block-scoped

// Temporal Dead Zone
console.log(a);  // ReferenceError
let a = 5;
```

**`const` não é imutável** — apenas a reference é imutável. Objetos continuam mutáveis.

```javascript
const arr = [1, 2, 3];
arr.push(4);  // OK — mutação permitida
// arr = [];  // erro — reassign proibido

// Para imutabilidade real, use Object.freeze ou Immer
Object.freeze(arr);
arr.push(5);  // silenciosamente ignorado (ou erro em strict mode)
```

### Escopo lexical

Funções capturam variáveis do escopo onde foram **definidas**, não onde são chamadas.

```javascript
function criarContador() {
    let count = 0;
    return function() {
        count++;
        return count;
    };
}

const contador = criarContador();
contador();  // 1
contador();  // 2
contador();  // 3
// 'count' continua vivo por causa do closure
```

---

## Closures — o conceito mais fundamental

**Closure** é uma função que "lembra" o escopo onde foi criada. Todas as funções em JavaScript são closures.

### Uso prático 1 — encapsulamento

```javascript
function criarConta(saldoInicial) {
    let saldo = saldoInicial;  // "privado"

    return {
        depositar(valor) {
            if (valor <= 0) throw new Error('valor inválido');
            saldo += valor;
        },
        sacar(valor) {
            if (valor > saldo) throw new Error('saldo insuficiente');
            saldo -= valor;
        },
        consultarSaldo() {
            return saldo;
        }
    };
}

const conta = criarConta(100);
conta.depositar(50);
conta.consultarSaldo();  // 150
// conta.saldo → undefined (não existe)
```

### Uso prático 2 — memoization

```javascript
function memoize(fn) {
    const cache = new Map();
    return function(...args) {
        const key = JSON.stringify(args);
        if (!cache.has(key)) {
            cache.set(key, fn.apply(this, args));
        }
        return cache.get(key);
    };
}

const fibMemo = memoize(function fib(n) {
    return n < 2 ? n : fibMemo(n - 1) + fibMemo(n - 2);
});
```

### Armadilha clássica — loop + closure + var

```javascript
// BUG clássico
for (var i = 0; i < 3; i++) {
    setTimeout(() => console.log(i), 0);
}
// Imprime: 3, 3, 3

// Solução moderna — let
for (let i = 0; i < 3; i++) {
    setTimeout(() => console.log(i), 0);
}
// Imprime: 0, 1, 2
```

### Memory leak via closure

Closure mantém referências vivas no heap. Cuidado com closures que capturam objetos grandes.

```javascript
function processarDadosGrandes() {
    const dadosEnormes = carregarMuitosDados();  // 100 MB
    const resultado = calcular(dadosEnormes);

    return function mostrarResultado() {
        console.log(resultado);
        // dadosEnormes continua no heap até este closure ser GC'd
    };
}
```

---

## this — o "monstro de sete cabeças"

O `this` em JavaScript é determinado em **tempo de execução**, não em tempo de declaração. O valor depende de **como** a função foi chamada.

### As 5 regras de binding

**1. Default binding — função normal**

```javascript
function foo() {
    console.log(this);
}
foo();  // window (ou global em Node) em sloppy mode
        // undefined em strict mode ('use strict')
```

**2. Implicit binding — método de objeto**

```javascript
const obj = {
    name: 'Maria',
    saudar() {
        console.log(`Olá, ${this.name}`);
    }
};
obj.saudar();  // "Olá, Maria" — this = obj
```

**Perdendo o `this`:**

```javascript
const fn = obj.saudar;
fn();  // "Olá, undefined" — this perdido
```

**3. Explicit binding — `call`, `apply`, `bind`**

```javascript
function saudar(saudacao) {
    console.log(`${saudacao}, ${this.name}`);
}

const pessoa = { name: 'João' };

saudar.call(pessoa, 'Olá');        // "Olá, João"
saudar.apply(pessoa, ['Hey']);     // "Hey, João"
const saudarJoao = saudar.bind(pessoa);
saudarJoao('Oi');                  // "Oi, João"
```

**4. new binding — construtor**

```javascript
function Pessoa(nome) {
    this.nome = nome;  // this é o novo objeto
}
const maria = new Pessoa('Maria');
```

**5. Arrow functions — herdam `this` do escopo léxico**

```javascript
const obj = {
    name: 'Maria',
    saudar() {
        setTimeout(function() {
            console.log(this.name);  // undefined — this é global/undefined
        }, 100);
    },
    saudarCerto() {
        setTimeout(() => {
            console.log(this.name);  // "Maria" — arrow herda this de saudarCerto
        }, 100);
    }
};
```

**Arrow functions não têm `this` próprio**, e também não têm `arguments`, `super`, ou `new.target`. Não podem ser construtores.

### Perdendo `this` em callbacks

```javascript
class Contador {
    count = 0;

    increment() {
        this.count++;
    }
}

const c = new Contador();
button.addEventListener('click', c.increment);  // this = button, não c!

// Soluções
button.addEventListener('click', () => c.increment());  // arrow mantém c
button.addEventListener('click', c.increment.bind(c));  // bind fixa this

// Ou arrow method (class field)
class Contador2 {
    count = 0;
    increment = () => {
        this.count++;  // this fixado por instância
    };
}
```

---

## Prototypes e herança

JavaScript tem **prototype-based inheritance**, não class-based (apesar da sintaxe `class`).

### O que é prototype

Cada objeto tem um **link interno** (`[[Prototype]]`) para outro objeto. Quando você acessa uma propriedade que não existe, JS sobe pela **cadeia de prototypes**.

```javascript
const pai = { sobrenome: 'Silva' };
const filho = Object.create(pai);
filho.nome = 'Maria';

console.log(filho.nome);       // "Maria" (próprio)
console.log(filho.sobrenome);  // "Silva" (via prototype)
console.log(filho.__proto__ === pai);  // true
```

### Funções e prototype

```javascript
function Pessoa(nome) {
    this.nome = nome;
}

Pessoa.prototype.saudar = function() {
    return `Olá, ${this.nome}`;
};

const maria = new Pessoa('Maria');
maria.saudar();  // "Olá, Maria"
// saudar não é cópia — existe uma vez em Pessoa.prototype
```

### Class syntax — açúcar sobre prototype

```javascript
class Pessoa {
    #idade;  // private field (ES2022)

    constructor(nome, idade) {
        this.nome = nome;
        this.#idade = idade;
    }

    saudar() {
        return `Olá, ${this.nome}`;
    }

    get idade() {
        return this.#idade;
    }

    static criarAnonimo() {
        return new Pessoa('Anônimo', 0);
    }
}

class Medico extends Pessoa {
    constructor(nome, idade, especialidade) {
        super(nome, idade);
        this.especialidade = especialidade;
    }

    saudar() {
        return `${super.saudar()}, especialista em ${this.especialidade}`;
    }
}
```

### Private fields (ES2022)

```javascript
class Contador {
    #count = 0;

    increment() {
        this.#count++;
    }

    get value() {
        return this.#count;
    }
}

const c = new Contador();
c.#count;  // SyntaxError — truly private
```

---

## Tipos e coerção

JavaScript tem **7 tipos primitivos** + **Object**:

| Tipo | Exemplo | Typeof |
| --- | --- | --- |
| `undefined` | `undefined` | `"undefined"` |
| `null` | `null` | `"object"` (bug histórico) |
| `boolean` | `true`, `false` | `"boolean"` |
| `number` | `42`, `3.14`, `NaN`, `Infinity` | `"number"` |
| `bigint` (ES2020) | `42n` | `"bigint"` |
| `string` | `"hello"` | `"string"` |
| `symbol` (ES6) | `Symbol('id')` | `"symbol"` |
| `object` | `{}`, `[]`, functions | `"object"` ou `"function"` |

### typeof null — o bug mais famoso

```javascript
typeof null;  // "object" (!)
```

Bug histórico do JavaScript original (1995) que nunca foi corrigido por compatibilidade. Para verificar null: `x === null`.

### Coerção: explícita vs implícita

**Explícita:**

```javascript
Number("42");      // 42
String(42);        // "42"
Boolean(0);        // false
parseInt("42px", 10);  // 42
parseFloat("3.14");    // 3.14
```

**Implícita — pegadinhas:**

```javascript
"5" + 3    // "53" — + vira concatenação se há string
"5" - 3    // 2  — - sempre aritmético
[] + []    // ""
[] + {}    // "[object Object]"
```

**Regras de `==` (loose equality):**

- `null == undefined` → `true`
- `null == 0` → `false`
- `"" == false` → `true`
- `[] == false` → `true`
- `[] == ![]` → `true` (!)
- `NaN == NaN` → `false` (!)

**Regra prática:** **sempre use `===`**. `==` só é útil para `if (x == null)` que pega null e undefined.

### Falsy values

```javascript
// Valores falsy em JavaScript:
false
0
-0
0n
""
null
undefined
NaN

// Tudo mais é truthy, incluindo:
[]        // array vazio é truthy!
{}        // objeto vazio é truthy!
"0"       // string "0" é truthy!
"false"   // string "false" é truthy!
```

### NaN e floats

```javascript
0.1 + 0.2 === 0.3;  // false — IEEE 754
0.1 + 0.2;          // 0.30000000000000004

// Para dinheiro, NÃO use number
// Use BigInt em centavos ou biblioteca decimal.js
```

### BigInt (ES2020)

```javascript
const big = 9007199254740993n;  // note o 'n'
const huge = BigInt(Number.MAX_SAFE_INTEGER) + 1n;

// Não pode misturar com number
big + 1;   // TypeError
big + 1n;  // OK
```

---

## Arrays

### Criação

```javascript
const arr1 = [1, 2, 3];
const arr2 = new Array(5);         // [undefined × 5]
const arr3 = Array.from("hello");  // ['h', 'e', 'l', 'l', 'o']
const arr4 = Array.of(1, 2, 3);    // [1, 2, 3]
const arr5 = Array.from({length: 5}, (_, i) => i * 2);  // [0, 2, 4, 6, 8]
```

### Métodos imutáveis (retornam novo array)

```javascript
arr.map(fn)              // transforma
arr.filter(fn)           // filtra
arr.reduce(fn, init)     // reduz
arr.find(fn)             // primeiro que satisfaz
arr.findIndex(fn)
arr.findLast(fn)         // ES2023
arr.some(fn)             // algum satisfaz?
arr.every(fn)            // todos satisfazem?
arr.includes(x)
arr.indexOf(x)
arr.slice(start, end)    // cópia parcial
arr.concat(other)
arr.flat(depth)
arr.flatMap(fn)
arr.join(sep)
arr.at(-1)               // ES2022, suporta negativo
```

### Métodos mutáveis (modificam original)

```javascript
arr.push(x)              // adiciona no fim
arr.pop()                // remove do fim
arr.shift()              // remove do início
arr.unshift(x)           // adiciona no início
arr.splice(start, deleteCount, ...items)
arr.sort((a, b) => ...)  // in-place
arr.reverse()            // in-place
arr.fill(value, start, end)
```

### Imutáveis modernos (ES2023)

```javascript
arr.toSorted((a, b) => ...)  // novo array ordenado
arr.toReversed()              // novo array invertido
arr.toSpliced(start, deleteCount, ...items)
arr.with(index, value)        // novo array com index substituído
```

### Iterator Helpers (ES2025)

Operações lazy em iterators, sem criar arrays intermediários:

```javascript
Iterator.from([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    .map(x => x * 2)
    .filter(x => x > 10)
    .take(3)
    .toArray();
```

### Destructuring

```javascript
const [a, b, ...rest] = [1, 2, 3, 4, 5];
// a = 1, b = 2, rest = [3, 4, 5]

const [x = 10, y = 20] = [5];  // x = 5, y = 20 (default)

const { name, age, ...others } = { name: 'Maria', age: 30, city: 'SP' };

// Aninhado
const { address: { city } } = user;

// Renomeando
const { name: nome } = { name: 'Maria' };
```

---

## Objetos

### Criação e propriedades

```javascript
const obj = {
    nome: 'Maria',
    idade: 30,
    // Shorthand
    saudar() {
        return `Olá, ${this.nome}`;
    },
    // Computed property
    ['key_' + Date.now()]: 'value',
    // Spread
    ...outroObjeto
};
```

### Métodos de Object

```javascript
Object.keys(obj)
Object.values(obj)
Object.entries(obj)
Object.fromEntries(entries)
Object.assign(target, ...sources)
Object.freeze(obj)
Object.isFrozen(obj)
Object.create(proto)
Object.getPrototypeOf(obj)
Object.setPrototypeOf(obj, proto)
Object.hasOwn(obj, key)  // ES2022 — melhor que hasOwnProperty
Object.groupBy(arr, fn)  // ES2024
Map.groupBy(arr, fn)     // ES2024
```

### Deep clone

```javascript
// RUIM — perde Date, Map, funções
const clone = JSON.parse(JSON.stringify(obj));

// BOM — built-in moderno
const deep = structuredClone(obj);
```

### Map e Set

**Map** — dicionário com qualquer tipo de chave.

```javascript
const map = new Map();
map.set('key', 'value');
map.set(objetoComoChave, 'value2');
map.get('key');
map.has('key');
map.delete('key');
map.size;

for (const [k, v] of map) { ... }
```

**Por que Map e não Object:**

- Map aceita qualquer chave, Object aceita só string/symbol
- Map preserva ordem de inserção
- Map tem `.size`
- Map é otimizado para adições/remoções

**Set** — coleção de valores únicos.

```javascript
const set = new Set([1, 2, 3, 3, 4]);  // {1, 2, 3, 4}
set.add(5);
set.has(3);
set.delete(1);
[...set]  // converter para array
```

### Set Methods (ES2025)

```javascript
const a = new Set([1, 2, 3, 4]);
const b = new Set([3, 4, 5, 6]);

a.intersection(b);       // Set {3, 4}
a.union(b);              // Set {1, 2, 3, 4, 5, 6}
a.difference(b);         // Set {1, 2}
a.symmetricDifference(b);// Set {1, 2, 5, 6}
a.isSubsetOf(b);
a.isSupersetOf(b);
a.isDisjointFrom(b);
```

### WeakMap e WeakRef

**WeakMap** — map com chaves **fracamente referenciadas**:

```javascript
const wm = new WeakMap();
let obj = { id: 1 };
wm.set(obj, 'metadata');

obj = null;  // { id: 1 } pode ser GC'd, entry sai do wm
```

**Uso:** armazenar metadata de objetos sem impedir GC.

**WeakRef** (ES2021):

```javascript
const ref = new WeakRef(heavyObject);
// heavyObject pode ser GC'd
const obj = ref.deref();  // retorna objeto ou undefined
```

---

## Funções

### Declaration vs expression vs arrow

```javascript
// Declaration — hoisted
foo();  // OK
function foo() { }

// Expression — não hoisted
bar();  // TypeError
const bar = function() { };

// Arrow
const baz = () => { };
```

### Parâmetros

```javascript
// Default
function greet(name = 'stranger') { }

// Rest
function sum(...nums) {
    return nums.reduce((a, b) => a + b, 0);
}

// Destructuring
function processUser({ name, age = 18 }) { }
processUser({ name: 'Maria' });

// Named parameters (convenção)
function criarBotao({ texto, cor = 'blue', onClick }) { }
```

### Higher-order functions

```javascript
function multiplier(factor) {
    return (x) => x * factor;
}
const double = multiplier(2);
double(5);  // 10
```

### Composition

```javascript
const pipe = (...fns) => x => fns.reduce((v, f) => f(v), x);
const compose = (...fns) => x => fns.reduceRight((v, f) => f(v), x);

const processUser = pipe(
    trimName,
    toLowerCase,
    validateEmail
);
```

### Generators

```javascript
function* counter() {
    let i = 0;
    while (true) yield i++;
}

const gen = counter();
gen.next();  // {value: 0, done: false}
gen.next();  // {value: 1, done: false}

// Range
function* range(start, end) {
    for (let i = start; i < end; i++) yield i;
}
for (const n of range(1, 5)) console.log(n);
```

---

## Promises e Async/Await

### Promise — o modelo

Uma Promise representa um valor **que ainda não existe**, mas existirá no futuro (ou falhará).

```javascript
const promise = new Promise((resolve, reject) => {
    setTimeout(() => {
        if (Math.random() > 0.5) resolve('sucesso');
        else reject(new Error('falhou'));
    }, 1000);
});

promise
    .then(value => console.log('ok:', value))
    .catch(err => console.error('erro:', err))
    .finally(() => console.log('sempre'));
```

**Estados:** `pending`, `fulfilled`, `rejected`, `settled`.

### Chaining

```javascript
fetchUser(id)
    .then(user => fetchOrders(user.id))
    .then(orders => orders.filter(o => o.active))
    .then(active => active.length)
    .catch(err => { console.error(err); return 0; });
```

### async/await

```javascript
async function processar() {
    try {
        const user = await fetchUser(id);
        const orders = await fetchOrders(user.id);
        return orders.filter(o => o.active).length;
    } catch (err) {
        console.error(err);
        return 0;
    }
}
```

**`async function` sempre retorna Promise.** `await` só funciona em `async function` (ou top-level em módulos ESM).

### Paralelismo — Promise.all, allSettled, race, any

```javascript
// Rejeita se qualquer uma falhar
const [users, orders, products] = await Promise.all([
    fetchUsers(),
    fetchOrders(),
    fetchProducts()
]);

// Não rejeita — array com {status, value|reason}
const results = await Promise.allSettled([p1, p2, p3]);

// Primeira a fulfill OU reject
const first = await Promise.race([p1, p2, p3]);

// Primeira a fulfill (ignora rejects)
const any = await Promise.any([p1, p2, p3]);  // ES2021
```

### Promise.try (ES2025)

```javascript
Promise.try(() => mightThrow())
    .then(...)
    .catch(...);
```

### Anti-patterns comuns

```javascript
// RUIM — await sequencial que podia ser paralelo
const results = [];
for (const id of ids) {
    results.push(await fetchUser(id));  // lento
}

// BOM
const results = await Promise.all(ids.map(id => fetchUser(id)));

// RUIM — forEach com async
users.forEach(async (u) => {
    await processUser(u);  // não espera!
});

// BOM
await Promise.all(users.map(u => processUser(u)));
// ou sequencial:
for (const u of users) {
    await processUser(u);
}
```

### Cancelation — AbortController

```javascript
const controller = new AbortController();

fetch('/api/data', { signal: controller.signal })
    .then(r => r.json())
    .catch(err => {
        if (err.name === 'AbortError') return;
        throw err;
    });

// Cancelar
controller.abort();

// Com timeout (ES2022)
fetch('/api/data', { signal: AbortSignal.timeout(5000) });
```

### Top-level await (ES2022)

```javascript
// Em módulos ESM, await funciona no nível do arquivo
import { db } from './db.mjs';
await db.connect();
export const ready = true;
```

---

## Iterators e AsyncIterators

### Iterator protocol

```javascript
class Range {
    constructor(start, end) {
        this.start = start;
        this.end = end;
    }

    *[Symbol.iterator]() {
        for (let i = this.start; i < this.end; i++) yield i;
    }
}

for (const n of new Range(1, 5)) console.log(n);  // 1, 2, 3, 4
```

### AsyncIterators — pagination, streaming

```javascript
async function* fetchPages() {
    let page = 1;
    while (true) {
        const data = await fetch(`/api?page=${page}`).then(r => r.json());
        if (data.length === 0) break;
        yield data;
        page++;
    }
}

for await (const page of fetchPages()) {
    console.log(page);
}
```

---

## Modules (ESM)

### ESM (padrão moderno)

```javascript
// math.mjs
export function sum(a, b) { return a + b; }
export function mul(a, b) { return a * b; }
export default function identity(x) { return x; }

// main.mjs
import identity, { sum, mul } from './math.mjs';
import * as math from './math.mjs';
import { sum as add } from './math.mjs';
```

**Características:**

- Static imports (tree shaking)
- Strict mode sempre ligado
- `this` é undefined no top level
- Async — suporta top-level await
- Live bindings

### Dynamic import

```javascript
// Carregamento sob demanda
async function loadLazy() {
    const { default: heavyLib } = await import('./heavy.mjs');
    heavyLib.doStuff();
}
```

### CJS vs ESM

| | CJS | ESM |
| --- | --- | --- |
| Sintaxe | `require` / `module.exports` | `import` / `export` |
| Loading | Síncrono | Assíncrono |
| Tree shaking | ❌ | ✅ |
| Top-level await | ❌ | ✅ |
| Strict mode | Opcional | Sempre |

**Em Node moderno (22+):** use ESM. Node 22.18+ suporta TypeScript nativamente.

### Import Attributes (ES2025)

```javascript
import data from './data.json' with { type: 'json' };
import styles from './styles.css' with { type: 'css' };
```

---

## Error handling

### try/catch/finally

```javascript
try {
    JSON.parse(invalid);
} catch (err) {
    if (err instanceof SyntaxError) {
        console.log('JSON inválido');
    } else {
        throw err;
    }
} finally {
    cleanup();
}
```

### Custom errors

```javascript
class ValidationError extends Error {
    constructor(message, field) {
        super(message);
        this.name = 'ValidationError';
        this.field = field;
    }
}
```

### Error.cause (ES2022)

```javascript
try {
    await db.query(sql);
} catch (err) {
    throw new Error('Failed to save user', { cause: err });
}
```

### Error.isError() (ES2026)

```javascript
Error.isError(new Error());     // true
Error.isError({ name: 'Error' }); // false
```

---

## Temporal API (ES2026)

Substitui `Date`. API moderna inspirada em Java Time.

```javascript
// Instante no tempo (UTC)
const now = Temporal.Now.instant();

// Data sem timezone
const date = Temporal.PlainDate.from('2026-04-11');
const date2 = date.add({ days: 30 });

// Data + hora com timezone
const zoned = Temporal.Now.zonedDateTimeISO('America/Sao_Paulo');

// Duração
const dur = Temporal.Duration.from({ hours: 2, minutes: 30 });

// Formatação
const formatted = zoned.toLocaleString('pt-BR', { dateStyle: 'long' });
```

**Até Temporal ser suportado universalmente**, use `date-fns` ou `dayjs` (evite `moment`).

---

## Explicit Resource Management (ES2026)

`using` e `DisposableStack` — `try-with-resources` em JavaScript.

```javascript
// Antes
let file;
try {
    file = openFile('data.txt');
} finally {
    file?.close();
}

// Com using (ES2026)
{
    using file = openFile('data.txt');
    // usar file
}  // file.Symbol.dispose() chamado automaticamente

// Async
{
    await using db = connect();
}  // db.Symbol.asyncDispose() chamado

// Implementar disposable
class Connection {
    [Symbol.dispose]() {
        this.close();
    }
}
```

---

## Memory management

### Garbage Collection

JavaScript tem **automatic GC** baseado em **reachability**. Um objeto é coletado quando não há mais referências vivas.

**V8 específicamente:**

- **Young generation (new space)** — objetos novos, coleção rápida frequente
- **Old generation** — objetos que sobreviveram, coleção menos frequente
- **Large object space** — objetos grandes

### Memory leaks comuns

**1. Global variables acidentais**

```javascript
function foo() {
    leak = 'bar';  // sem const/let/var — vira global
}
```

**2. Timers não limpos**

```javascript
const interval = setInterval(() => { ... }, 1000);
// Esqueceu clearInterval — nunca é GC'd
```

**3. Event listeners não removidos**

```javascript
element.addEventListener('click', handler);
// removeu o element do DOM, mas handler ainda tem referência
```

**4. Closures retendo objetos grandes**

```javascript
function processarHuge() {
    const hugeData = loadHuge();  // 100 MB
    return function() {
        console.log('done');  // hugeData retido
    };
}
```

### Detectando leaks

- **Chrome DevTools — Memory panel** — heap snapshots, comparação
- **`process.memoryUsage()`** em Node
- **`node --inspect`** + Chrome DevTools

---

## Features modernas por ano

### ES2020

- Optional chaining — `obj?.foo?.bar`
- Nullish coalescing — `x ?? default`
- BigInt — `42n`
- Dynamic import
- `globalThis`
- `Promise.allSettled`

### ES2021

- Logical assignment — `a ??= b`
- `Promise.any`
- `String.replaceAll`
- Numeric separators — `1_000_000`
- WeakRef

### ES2022

- Class fields e private — `#name`
- `at()` — `arr.at(-1)`
- Top-level `await` em ESM
- `Object.hasOwn`
- `Error.cause`

### ES2023

- `findLast`, `findLastIndex`
- `toSorted`, `toReversed`, `toSpliced`, `with`

### ES2024

- `Object.groupBy`, `Map.groupBy`
- `Promise.withResolvers()`

### ES2025

- Iterator helpers — lazy map/filter/take
- Set methods — intersection, union, difference
- `RegExp.escape`
- `Promise.try`
- Import attributes

### ES2026 (expected)

- **Temporal API** — data/hora nativo
- **Explicit Resource Management** — `using`
- `Array.fromAsync`
- `Error.isError()`
- `Math.sumPrecise`
- Base64/Hex encoding

---

## Runtime diferences

| Runtime | Engine | Uso |
| --- | --- | --- |
| **Chrome/Edge** | V8 | Browser |
| **Node.js** | V8 | Server |
| **Bun** | JavaScriptCore | Server, package manager |
| **Deno** | V8 | Server, security-first |
| **Firefox** | SpiderMonkey | Browser |
| **Safari** | JavaScriptCore | Browser |
| **Cloudflare Workers** | V8 isolate | Edge |

### Node 22+ — TypeScript nativo

```bash
node --experimental-strip-types app.ts
```

Não precisa mais de `tsx` ou `ts-node`. Em Node 24+, é estável.

### Bun

- Package manager 10x mais rápido que npm
- Runtime JS/TS completo
- Bundler e test runner built-in
- Em 2026, adquirido pela Anthropic

### Deno

- Runtime pensado em segurança (permissions explícitas)
- TypeScript first-class
- Deno 2 — compatibilidade com Node via `deno install npm:`

---

## Armadilhas comuns

- **`==` vs `===`** — sempre use `===`
- **`typeof null === 'object'`** — bug histórico
- **`this` perdido** em callbacks — use arrow ou bind
- **Mutação via spread** — spread é shallow
- **Floats para dinheiro** — `0.1 + 0.2 !== 0.3`
- **`forEach` com async** — não espera. Use for...of + await ou Promise.all.
- **Unhandled promise rejections** — sempre capture
- **Memory leaks com closures** — cuidado com referências
- **`JSON.parse(JSON.stringify())` para clone** — perde Date, Map, funções. Use `structuredClone`.
- **`Array(5).fill([])` compartilha referência** — use `Array.from({length: 5}, () => [])`
- **Hoisting de `var`** — prefira `let`/`const`
- **`parseInt` sem radix** — `parseInt("08", 10)`
- **`Number.MAX_SAFE_INTEGER = 2^53 - 1`** — acima, use BigInt
- **Comparar arrays com `===`** — compara referência
- **Nullish vs falsy** — `||` pega falsy; `??` só null/undefined
- **`await` em forEach** — não espera
- **Loop infinito via microtasks** — bloqueia event loop

---

## Na prática (da minha experiência)

> **Patterns que padronizei:**
>
> **1. TypeScript estrito desde o dia 1.** JavaScript puro em projeto novo é negligência. TS `strict: true`, `noUncheckedIndexedAccess`. Detalhes em [[TypeScript]].
>
> **2. ESM em todo lugar.** `"type": "module"` no package.json. Node 22+. Top-level await, tree shaking, código mais limpo.
>
> **3. `structuredClone` em vez de `JSON.parse(JSON.stringify(...))`.** Clone real, incluindo Date, Map, Set, circular references.
>
> **4. `Promise.all` + `map` em vez de loop.** Paralelize quando possível. Se precisar de limite, use `p-limit`.
>
> **5. AbortController em toda chamada externa.** Timeout, cancelamento, cleanup em React useEffect.
>
> **6. `??` em vez de `||` para defaults.** `||` pega `0`, `""`, `false` como "falsy".
>
> **7. Map e Set** em vez de objetos/arrays quando a semântica é dicionário/conjunto.
>
> **8. `for...of` em vez de `forEach`** quando preciso de `await`, `break`, ou `continue`.
>
> **9. `Date` → `date-fns` ou `dayjs`** (e Temporal quando disponível).
>
> **Incidente memorável — race condition com fetch:**
>
> Componente React fazendo fetch no useEffect tinha race condition sob trocas rápidas. Usuário digitava "abc" na busca → dispara 3 fetches → resposta de "ab" chegava depois de "abc" → estado errado. Solução: AbortController no cleanup do effect.
>
> ```tsx
> useEffect(() => {
>     const controller = new AbortController();
>     fetch(`/api/search?q=${query}`, { signal: controller.signal })
>         .then(r => r.json())
>         .then(setResults)
>         .catch(err => { if (err.name !== 'AbortError') throw err; });
>     return () => controller.abort();
> }, [query]);
> ```
>
> **Outro incidente — memory leak:**
>
> Singleton global retinha referências a componentes React antigos via event listener não removido. Heap subia 2-3 MB por navegação. Descobri via Chrome DevTools Memory → heap snapshot comparison. Solução: `WeakRef` ou garantir `removeEventListener` no cleanup.
>
> **A lição principal:** JavaScript moderno é poderoso mas abundante em armadilhas. Use TypeScript para tipos, ESLint strict para cultura, e tenha reflexos automáticos: `===`, `??`, Promise.all, cleanup, imutabilidade.

---

## How to explain in English

> "JavaScript is multi-paradigm — imperative, object-oriented with prototypes, and functional. Understanding it deeply means understanding three things: the event loop, closures, and the prototype chain.
>
> The event loop makes JavaScript 'single-threaded but concurrent'. A call stack executes code synchronously. When the stack is empty, the event loop picks the next macrotask — a setTimeout callback, an I/O completion — and runs it. Between macrotasks, all pending microtasks are drained, which is why `Promise.then` always runs before `setTimeout(..., 0)`.
>
> Closures are functions that capture their lexical scope. Every function in JavaScript is a closure, used for data privacy, memoization, and event handlers with state. The classic gotcha is `var` in loops — all closures share the same binding. `let` fixes this.
>
> Prototypes are the real inheritance model. `class` is just syntactic sugar. Every object has an internal link to another object, and property lookups walk up the chain.
>
> For async, I use `async/await` for linear code, `Promise.all` to parallelize independent operations, and `AbortController` for cancellation. I never use `forEach` with async — I use `for...of` with `await` for sequential, or `Promise.all(arr.map(...))` for parallel.
>
> Modern JavaScript (ES2020+) is concise and safe with optional chaining, nullish coalescing, destructuring, and spread. ES2025 brought Iterator Helpers and Set methods. ES2026 is bringing the Temporal API — finally a proper date/time replacement — and Explicit Resource Management with `using`, similar to Java's try-with-resources.
>
> For memory, the runtime handles GC, but I watch for common leaks: unremoved event listeners, uncleared timers, closures retaining large objects. Chrome DevTools Memory panel is my first tool for diagnosis."

### Frases úteis em entrevista

- "JavaScript is single-threaded but concurrent through the event loop."
- "Microtasks always drain before the next macrotask."
- "Every function is a closure — it captures its lexical scope."
- "`class` is syntactic sugar over prototype-based inheritance."
- "Arrow functions don't have their own `this`."
- "I never use `==`, only `===`. And `??` for defaults, not `||`."
- "For parallelism, I use `Promise.all`. For cancellation, `AbortController`."
- "`structuredClone` is my default for deep cloning."
- "Avoid `forEach` with `async` — it doesn't wait."
- "Temporal API in ES2026 finally replaces the broken `Date`."

### Key vocabulary

- laço de eventos → event loop
- pilha de chamadas → call stack
- microtarefa / macrotarefa → microtask / macrotask
- fechamento → closure
- função de ordem superior → higher-order function
- içamento → hoisting
- coerção → coercion
- estritamente igual → strictly equal (`===`)
- protótipo → prototype
- cadeia de protótipos → prototype chain
- coleta de lixo → garbage collection
- vazamento de memória → memory leak
- promessa → promise
- assíncrono / aguardar → async / await
- gerador → generator
- módulo → module
- importação dinâmica → dynamic import
- desestruturação → destructuring
- espalhamento → spread
- encadeamento opcional → optional chaining
- coalescência nula → nullish coalescing

---

## Recursos

### Livros

- **You Don't Know JS Yet** — Kyle Simpson (gratuito)
- **Eloquent JavaScript** — Marijn Haverbeke (gratuito)
- **JavaScript: The Definitive Guide** — David Flanagan

### Documentação

- [MDN JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
- [TC39 Proposals](https://github.com/tc39/proposals)
- [V8 Blog](https://v8.dev/blog)

### Cursos

- [freeCodeCamp — JavaScript](https://www.freecodecamp.org/learn/javascript-v9/)
- [freeCodeCamp — Full JavaScript Course](https://www.freecodecamp.org/news/full-javascript-course-for-beginners/)
- [Full Stack Open](https://fullstackopen.com/en/) — ver [[Full Stack Open - Guia de Revisão]]
- [JavaScript.info](https://javascript.info/)

### Blogs

- [2ality](https://2ality.com/) — Dr. Axel Rauschmayer
- [Frontend Masters Blog](https://frontendmasters.com/blog/)
- [What to Know in JavaScript 2026](https://frontendmasters.com/blog/what-to-know-in-javascript-2026-edition/)

### Tools

- [Node.js Docs](https://nodejs.org/docs/latest/api/)
- [compat-table](https://compat-table.github.io/compat-table/)
- [Can I Use](https://caniuse.com/)
- [Bundlephobia](https://bundlephobia.com/)

---

## Veja também

- [[TypeScript]] — sistema de tipos estáticos
- [[Node.js]] — runtime server-side
- [[Testes em JavaScript]] — Jest, Vitest, Testing Library, Playwright
- [[React]] — framework UI
- [[HTML e CSS]] — base do frontend
- [[Full Stack Open - Guia de Revisão]] — resumo do curso
- [[API Design]] — consumindo APIs em JS/TS
- [[System Design]] — JavaScript em system design
- [[Java Concurrency]] — comparar com concorrência na JVM
