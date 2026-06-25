---
title: "11 - Prototypes e herança"
created: 2026-06-25
updated: 2026-06-25
type: concept
status: seedling
fase: adepto
tags:
  - javascript
  - adepto
  - entrevista
  - prototypes
publish: true
---

# Prototypes e herança

> [!abstract] TL;DR
> JavaScript não tem herança clássica — tem **herança por protótipos**. Cada objeto carrega um ponteiro interno `[[Prototype]]` que aponta para outro objeto, formando uma cadeia. Quando você acessa uma propriedade que o objeto não tem, o motor escala a cadeia até encontrá-la ou chegar em `null`. Funções construtoras + `new` e a sintaxe `class` são formas de montar essa cadeia — mas a cadeia é sempre a mesma coisa por baixo. Entender a diferença entre `[[Prototype]]` (do objeto) e `prototype` (da função) é o divisor de águas entre quem briga com herança em JS e quem a usa com confiança.

---

Você acabou de entrar numa entrevista técnica. O entrevistador pergunta: "Como herança funciona em JavaScript?". Se você responde "com `class extends`", está certo — mas só na superfície. A resposta que impressiona vai um nível abaixo: *JavaScript não tem herança de classes. Tem delegação por protótipos.* A sintaxe `class` é açúcar. O mecanismo real é a prototype chain.

Mas por que isso importa na prática? Porque quando você estende um built-in errado, ou perde um método ao reassignar um `prototype`, ou se pergunta por que `instanceof` retornou `false` de forma inesperada — a resposta está sempre na cadeia de protótipos. Entender o mecanismo te dá a bússola.

---

## O problema que protótipos resolvem

Imagine que você tem mil objetos representando usuários. Cada usuário precisa de um método `saudacao()`. A abordagem mais ingênua:

```js
const user1 = {
  nome: "Ana",
  saudacao() { return `Olá, ${this.nome}!`; }
};
const user2 = {
  nome: "Bruno",
  saudacao() { return `Olá, ${this.nome}!`; }  // cópia idêntica
};
```

Você acabou de criar mil cópias da mesma função em memória. Desperdício. Protótipos resolvem isso: você coloca o método **uma vez** num objeto compartilhado (o protótipo), e todos os usuários delegam a busca para ele.

---

## `[[Prototype]]`: o ponteiro interno

Todo objeto JavaScript tem um slot interno chamado `[[Prototype]]`. Você não acessa esse slot diretamente — ele é parte do spec. O que você pode fazer:

- **Ler com segurança:** `Object.getPrototypeOf(obj)`
- **Definir na criação:** `Object.create(proto)`
- **Legado (evitar em produção):** `obj.__proto__` — existe por compatibilidade, mas não use em código novo

```js
const animal = { tipo: "mamífero" };
const cachorro = Object.create(animal);

console.log(cachorro.tipo);                          // "mamífero" — subiu a cadeia
console.log(Object.getPrototypeOf(cachorro) === animal); // true
console.log(cachorro.hasOwnProperty("tipo"));        // false — é do protótipo
```

> [!question]- Por que `__proto__` é legado se funciona?
> `__proto__` foi originalmente um hack não-padrão do Firefox que todos os browsers acabaram implementando. A spec o formalizou no ES2015 apenas para compatibilidade retroativa. Em código novo, use `Object.getPrototypeOf` / `Object.create` / `Object.setPrototypeOf` — a semântica é explícita e o runtime pode otimizar melhor.

---

## A prototype chain: resolução de propriedades

Quando você faz `obj.prop`, o motor segue um algoritmo preciso:

1. O objeto `obj` tem a propriedade `prop` diretamente (own property)? → retorna.
2. Não tem? Sobe para `obj.[[Prototype]]` e tenta de novo.
3. Repete até encontrar ou chegar em `null` → retorna `undefined`.

```mermaid
%%{init: {"theme": "base", "themeVariables": {"primaryColor": "#4A90D9", "edgeLabelBackground": "#ffffff"}}}%%
graph TD
    A["cachorro\n{ nome: 'Rex' }"]
    B["animal\n{ tipo: 'mamífero', respirar() }"]
    C["Object.prototype\n{ toString(), hasOwnProperty(), ... }"]
    D["null"]

    A -->|"[[Prototype]]"| B
    B -->|"[[Prototype]]"| C
    C -->|"[[Prototype]]"| D

    style A fill:#4A90D9,color:#fff
    style B fill:#4A90D9,color:#fff
    style C fill:#4A90D9,color:#fff
    style D fill:#888,color:#fff
```

Pense numa cadeia de postos de trabalho: você pergunta algo ao seu líder imediato; se ele não sabe, ele pergunta ao dele, e assim por diante. A resposta vem do primeiro que sabe. Se ninguém sabe (`null`), você recebe `undefined`.

---

## `prototype` da função: não confunda com `[[Prototype]]`

Aqui está a confusão mais comum. Quando você cria uma função, o JavaScript automaticamente cria um objeto chamado `NomeDaFuncao.prototype`. Esse objeto vai se tornar o `[[Prototype]]` de qualquer instância criada com `new NomeDaFuncao()`.

Portanto:
- `[[Prototype]]`: slot interno do **objeto** (toda instância)
- `.prototype`: propriedade da **função** construtora (não da instância)

```js
function Animal(nome) {
  this.nome = nome;
}
Animal.prototype.falar = function() {
  return `${this.nome} faz um som.`;
};

const gato = new Animal("Miau");

// [[Prototype]] do gato aponta para Animal.prototype
console.log(Object.getPrototypeOf(gato) === Animal.prototype); // true

// Mas gato não tem .prototype — isso é coisa de função
console.log(gato.prototype); // undefined
```

O diagrama mental:

```mermaid
%%{init: {"theme": "base", "themeVariables": {"primaryColor": "#4A90D9"}}}%%
graph LR
    F["Função Animal"]
    P["Animal.prototype\n{ falar() }"]
    I["instância gato\n{ nome: 'Miau' }"]

    F -->|".prototype"| P
    I -->|"[[Prototype]]"| P

    style F fill:#F5A623,color:#fff
    style P fill:#4A90D9,color:#fff
    style I fill:#4A90D9,color:#fff
```

---

## `new`: os quatro passos que você precisa saber

Quando você faz `new Animal("Rex")`, o motor executa exatamente quatro etapas:

1. **Cria** um objeto vazio: `const obj = {}`.
2. **Liga o protótipo:** `obj.[[Prototype]] = Animal.prototype`.
3. **Executa** a função construtora com `this = obj`: preenche as propriedades próprias.
4. **Retorna** `obj` (ou o valor retornado, se a função retornar um objeto explicitamente).

```js
// Simulando `new` manualmente
function meuNew(Construtora, ...args) {
  const obj = Object.create(Construtora.prototype); // passos 1 e 2
  const resultado = Construtora.apply(obj, args);   // passo 3
  return typeof resultado === "object" && resultado !== null
    ? resultado
    : obj;                                           // passo 4
}

const dog = meuNew(Animal, "Rex");
console.log(dog.nome);   // "Rex"
console.log(dog.falar()); // "Rex faz um som."
```

Saber os quatro passos responde perguntas como: "por que esquecer `new` quebra tudo?" (sem `new`, `this` vira o objeto global), e "o que acontece se o construtor retornar um objeto?" (esse objeto substitui a instância).

---

## `Object.create`: herança sem construtora

`Object.create(proto)` cria um objeto cujo `[[Prototype]]` é `proto`. É a forma mais direta de expressar herança sem funções construtoras.

```js
const veiculoBase = {
  ligar() { return `${this.modelo} ligando...`; },
  desligar() { return `${this.modelo} desligando.`; }
};

const carro = Object.create(veiculoBase);
carro.modelo = "Fusca";

console.log(carro.ligar());   // "Fusca ligando..."
console.log(carro.hasOwnProperty("ligar")); // false — veio do proto
```

`Object.create(null)` cria um objeto sem nenhum protótipo — sem `toString`, sem `hasOwnProperty`. Útil para mapas de dados puros onde você não quer poluição da cadeia.

---

## `class`: açúcar sintático sobre protótipos

A sintaxe `class` foi introduzida no ES2015. Ela não muda o modelo de herança — reescreve a cadeia de protótipos com uma sintaxe mais familiar para quem vem de Java ou Python.

```js
class Animal {
  constructor(nome) {
    this.nome = nome;     // own property — direto na instância
  }

  falar() {               // vai para Animal.prototype
    return `${this.nome} faz um som.`;
  }
}

class Cachorro extends Animal {
  constructor(nome, raca) {
    super(nome);          // chama Animal.constructor — obrigatório antes de this
    this.raca = raca;
  }

  falar() {               // shadowing: sobrescreve Animal.prototype.falar
    return `${this.nome} late!`;
  }
}

const d = new Cachorro("Rex", "Labrador");
console.log(d.falar());  // "Rex late!" — shadow local
console.log(d instanceof Cachorro); // true
console.log(d instanceof Animal);   // true — cadeia inclui ambos
```

### Desugarização manual

O que o `class Cachorro extends Animal` faz por baixo:

```js
// Equivalente sem class — didático, não copie em produção
function Cachorro(nome, raca) {
  Animal.call(this, nome);   // super(nome)
  this.raca = raca;
}

// Liga a cadeia de protótipos
Object.setPrototypeOf(Cachorro.prototype, Animal.prototype);

// Método override — shadow em Cachorro.prototype
Cachorro.prototype.falar = function() {
  return `${this.nome} late!`;
};
```

> [!info] `class` vs. função construtora — o que realmente muda
> 1. `class` sempre opera em strict mode.
> 2. Não sofre hoisting como `function` — não pode usar antes de declarar.
> 3. Não pode ser chamada sem `new` (lança TypeError).
> 4. `super` só existe dentro de `class` — não tem equivalente fácil sem ela.

---

## Campos de classe, privados e blocos estáticos (ES2022+)

Campos de classe declarados no corpo vão **diretamente na instância**, não no protótipo:

```js
class Contador {
  // Campo público — vai para cada instância (own property)
  contagem = 0;

  // Campo privado — só acessível dentro da classe
  #segredo = 42;

  // Bloco estático — executado uma vez quando a classe é avaliada
  static {
    console.log("Classe Contador carregada!");
  }

  incrementar() { this.contagem++; }
  revelar() { return this.#segredo; }
}

const c = new Contador();
c.incrementar();
console.log(c.contagem);   // 1
console.log(c.#segredo);   // SyntaxError — privado!
```

> [!warning] Campos de classe quebram a cadeia em um ponto sutil
> Campos declarados no corpo (`contagem = 0`) são **own properties da instância**, não estão no protótipo. Isso significa que `Object.keys(instancia)` os lista, mas `instancia.hasOwnProperty("contagem")` retorna `true`. Se você esperava que todos os métodos viessem do protótipo, os campos são a exceção.

---

## Shadowing: quando o filho oculta o pai

Se uma instância (ou um protótipo filho) tem uma propriedade com o mesmo nome que um ancestral, o motor para na primeira ocorrência — nunca sobe a cadeia para aquele nome:

```js
Animal.prototype.tipo = "animal";
const d = new Cachorro("Rex", "Labrador");

d.tipo = "cachorro domesticado"; // cria own property em d
console.log(d.tipo);                   // "cachorro domesticado" — shadow
console.log(Animal.prototype.tipo);    // "animal" — intacto

delete d.tipo;
console.log(d.tipo); // "animal" — voltou a subir a cadeia
```

Shadowing é poderoso mas silencioso — você nunca recebe erro ao criar uma propriedade que obscurece um ancestral.

---

## `instanceof` e `hasOwnProperty`

`instanceof` verifica se o `prototype` da construtora aparece em algum lugar da cadeia do objeto:

```js
console.log(d instanceof Cachorro); // true
console.log(d instanceof Animal);   // true
console.log(d instanceof Array);    // false
```

`hasOwnProperty` verifica se a propriedade é **própria** do objeto, sem subir a cadeia:

```js
console.log(d.hasOwnProperty("nome")); // true — own property
console.log(d.hasOwnProperty("falar")); // false — está no prototype
```

> [!question]- Por que `"falar" in d` retorna `true` mas `hasOwnProperty` retorna `false`?
> O operador `in` sobe a cadeia inteira — verifica se a propriedade existe em qualquer ponto. `hasOwnProperty` olha só a camada imediata do objeto. Para saber se algo é herdado, combine os dois: `"prop" in obj && !obj.hasOwnProperty("prop")`.

---

## Casos práticos

### Cenário 1: Mixin — composição em vez de herança profunda

Herança de classe cria cadeias rígidas: `A → B → C`. Quando você precisa de comportamento de múltiplas fontes, use **mixins** — funções que copiam métodos para um target:

```js
// Mixin de serialização
const Serializavel = (Base) => class extends Base {
  toJSON() {
    return JSON.stringify(this);
  }
  toString() {
    return JSON.stringify(this, null, 2);
  }
};

// Mixin de validação
const Validavel = (Base) => class extends Base {
  validar(schema) {
    return Object.keys(schema).every(k => schema[k](this[k]));
  }
};

class Produto {
  constructor(nome, preco) {
    this.nome = nome;
    this.preco = preco;
  }
}

// Composição: Produto + serialização + validação
class ProdutoRico extends Serializavel(Validavel(Produto)) {}

const p = new ProdutoRico("Teclado", 199.90);
console.log(p.toJSON()); // '{"nome":"Teclado","preco":199.9}'

const schema = { nome: v => typeof v === "string", preco: v => v > 0 };
console.log(p.validar(schema)); // true
```

Mixins com funções de ordem superior (`(Base) => class extends Base`) funcionam porque `extends` aceita qualquer expressão que resulte em uma função construtora, não apenas um nome de classe literal.

### Cenário 2: Estender built-ins com cuidado

Estender `Array`, `Error` ou `Map` tem armadilhas históricas — principalmente porque esses built-ins criam instâncias do tipo original internamente, não do subtipo. A partir do ES2015, `class extends` resolve isso corretamente:

```js
class ListaOrdenada extends Array {
  ordenar() {
    return [...this].sort((a, b) => a - b);
  }

  somente(predicado) {
    return this.filter(predicado); // retorna ListaOrdenada, não Array
  }
}

const lista = new ListaOrdenada();
lista.push(3, 1, 4, 1, 5);

console.log(lista.ordenar());            // [1, 1, 3, 4, 5]
console.log(lista.somente(n => n > 2));  // ListaOrdenada [3, 4, 5]
console.log(lista.somente(n => n > 2) instanceof ListaOrdenada); // true
```

O motivo de `filter` retornar `ListaOrdenada` e não `Array` é o `Symbol.species`. Por padrão, `Array` usa `this.constructor` para criar resultados de métodos derivados. Como `ListaOrdenada` estende `Array`, `this.constructor` é `ListaOrdenada`.

> [!warning] Estender built-ins com funções construtoras (pré-ES6) é quebrado
> Com funções construtoras clássicas, `extends` equivalente não funciona para built-ins: `Array.call(this)` não inicializa o array corretamente porque `Array` ignora o `this` passado por `call`. Com `class extends`, o motor usa o mecanismo interno correto via `Reflect.construct`. Se você ainda suporta ambientes muito antigos e usa transpilação, verifique: Babel e TypeScript em alvos ES5 podem quebrar `extends Array`.

---

## Armadilhas comuns

> [!warning] Confundir `.prototype` com `[[Prototype]]`
> **O que acontece:** `instancia.prototype` retorna `undefined`; você esperava os métodos.
> **Por quê:** `.prototype` é propriedade da *função construtora*, não da instância. A instância tem `[[Prototype]]`, acessado via `Object.getPrototypeOf(instancia)`.
> **Como evitar:** Memorize: funções têm `.prototype`; objetos/instâncias têm `[[Prototype]]`. Nunca mexa em `.prototype` de arrow functions (são `undefined`).

> [!warning] Mutação de `prototype` após instâncias já criadas
> **O que acontece:** Você adiciona método ao `prototype` depois de criar objetos — e funciona. Você *reassigna* o prototype inteiro — e instâncias antigas param de herdar.
> **Por quê:** Adicionar propriedade ao objeto apontado por `.prototype` propaga para todas as instâncias, pois a referência é viva. Reassignar `Animal.prototype = { ... }` cria um novo objeto e rompe a referência das instâncias antigas.
> **Como evitar:** Sempre *adicione* ao prototype existente em vez de substituí-lo: `Animal.prototype.novoMetodo = fn` em vez de `Animal.prototype = { novoMetodo: fn }`.

> [!warning] `instanceof` falha com múltiplos realms (iframes, workers)
> **O que acontece:** `array instanceof Array` retorna `false` quando o `array` veio de um `iframe`.
> **Por quê:** Cada realm (contexto de execução) tem seu próprio `Array.prototype`. O `instanceof` compara ponteiros — os `Array.prototype` de realms diferentes não são o mesmo objeto.
> **Como evitar:** Use `Array.isArray(valor)` para arrays; `Object.prototype.toString.call(valor)` para verificação de tipo universal.

> [!warning] Esquecendo `super()` antes de `this` em subclasses
> **O que acontece:** `ReferenceError: Must call super constructor in derived class before accessing 'this'`.
> **Por quê:** Em uma subclasse (`extends`), o objeto `this` é criado pelo construtor pai (`super()`). Até essa chamada, `this` não existe no escopo da subclasse.
> **Como evitar:** Sempre coloque `super(args)` como primeira linha do `constructor` de uma subclasse. Se você não declarar `constructor`, isso acontece implicitamente.

> [!warning] Campos privados `#` não são herdados pelo prototype
> **O que acontece:** Um método do filho tenta acessar `this.#campo` definido no pai — SyntaxError.
> **Por quê:** Campos privados `#` são ligados lexicalmente à classe onde foram declarados. Eles *existem* na instância (são own properties), mas só são acessíveis no corpo da classe que os declara.
> **Como evitar:** Se o filho precisar de acesso, use campos `protected` via convenção (`_campo`) ou exposição explícita por método getter/setter na classe pai.

---

## Como explicar em inglês

JavaScript inheritance is **prototype-based, not class-based**. Every object has an internal `[[Prototype]]` link that forms a chain — when you access a property, the engine walks up the chain until it finds it or hits `null`. The `class` syntax introduced in ES2015 is purely syntactic sugar: it rewires the prototype chain for you, but the underlying delegation model is the same. Private fields (`#`) are a genuine language-level addition — they live in the instance but are lexically scoped to the declaring class.

| PT | EN |
|----|-----|
| cadeia de protótipos | prototype chain |
| herança por protótipos | prototypal inheritance |
| função construtora | constructor function |
| propriedade própria | own property |
| sombreamento | shadowing / property shadowing |
| açúcar sintático | syntactic sugar |
| campo privado | private field |
| bloco estático | static initialization block |
| delegação | delegation |
| instanciar | to instantiate |

---

## Prototype em uma frase

Herança em JavaScript é **delegação por cadeia de objetos**: propriedades que o objeto não tem são buscadas em seus ancestrais, e `class` é apenas uma forma mais legível de montar essa cadeia.

---

## O que vem a seguir

Agora que você entende como os objetos se ligam via prototype, o próximo passo é lidar com código assíncrono — onde objetos, closures e o event loop se encontram num mesmo fluxo de execução.

- [[03-Dominios/Tecnologia/JavaScript/06 - this|06 - this]] — como o `this` de um método se comporta ao longo da cadeia de herança; por que arrow functions em métodos de classe mudam o binding
- [[03-Dominios/Tecnologia/JavaScript/07 - Objetos|07 - Objetos]] — fundamentos de criação e descriptores que alimentam a cadeia de protótipos

---

## Veja também

- [[03-Dominios/Tecnologia/JavaScript/Dicionário de JavaScript#prototype chain|Dicionário de JavaScript · prototype chain]] — definição concisa do mecanismo

---

## Fontes

- **MDN Web Docs** — [*Inheritance and the prototype chain*](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Inheritance_and_the_prototype_chain) — referência canônica do spec, atualizada até novembro de 2025
- **MDN Web Docs** — [*Object prototypes*](https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Advanced_JavaScript_objects/Object_prototypes) — tutorial com exemplos de `Object.create` e cadeia
- **Dr. Axel Rauschmayer** — [*Classes ES6 · Exploring JavaScript (ES2025 Edition)*](https://exploringjs.com/js/book/ch_classes.html) — cobertura completa de `class`, desugarização, private fields e static blocks
- **MDN Web Docs** — [*Object.setPrototypeOf()*](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/setPrototypeOf) — cuidados de performance e equivalência com `extends`
