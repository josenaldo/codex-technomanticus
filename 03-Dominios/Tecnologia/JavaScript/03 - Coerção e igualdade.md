---
title: "Coerção e igualdade"
created: 2026-06-25
updated: 2026-06-25
type: concept
status: seedling
fase: iniciado
tags:
  - javascript
  - iniciado
  - entrevista
  - coercao
publish: true
---

# Coerção e igualdade

> [!abstract] TL;DR
> JavaScript converte valores entre tipos automaticamente — isso se chama **coerção implícita**. O operador `==` aplica o algoritmo de *Abstract Equality* antes de comparar, o que gera resultados contraintuitivos. `===` compara sem converter. Os únicos **8 valores falsy** da linguagem são `false`, `0`, `-0`, `0n`, `""`, `null`, `undefined`, `NaN` — todo o resto é truthy, incluindo `[]` e `{}`. Use sempre `===`, com a única exceção deliberada do idiom `== null`.

---

Imagine que você está em uma entrevista de emprego e o entrevistador pergunta: "Quanto vale `[] == ![]` em JavaScript?" Você pisca. Como um array vazio pode ser igual ao *negativo* de si mesmo? A resposta é `true`, e entender por quê é entender o coração de uma das partes mais traiçoeiras da linguagem.

Coerção não é um bug — é uma *feature* intencional do design original do JavaScript, pensada para ser conveniente numa web dos anos 1990. Com o tempo, revelou ser fonte de bugs sutis. Dominar as regras de coerção é, hoje, diferencial em entrevistas e proteção real no dia a dia.

---

## O que é coerção

Coerção é a conversão de um valor de um tipo para outro — disparada *pela linguagem*, não por você.

Existem dois sabores:

- **Explícita**: você pede a conversão — `Number("42")`, `String(true)`, `Boolean(0)`.
- **Implícita**: a linguagem converte por você, silenciosamente, ao avaliar expressões como `"5" + 3` ou `if (valor)`.

É a coerção implícita que surpreende. Ela aparece em três contextos principais:

| Contexto | Exemplo | O que acontece |
|---|---|---|
| Operador `+` com string | `"5" + 3` | Número vira string → `"53"` |
| Operadores aritméticos | `"5" - 3` | String vira número → `2` |
| Contexto booleano | `if ([])` | Valor vira booleano → `true` |
| Operador `==` | `0 == false` | Ambos viram número → `true` |

> [!info] Coerção no [[Dicionário de JavaScript]]
> O Dicionário define **coerção** como "a conversão implícita de um valor de um tipo para outro, disparada por operadores (`+`, `==`) ou contextos (condições)." **truthy/falsy** também está lá definido — consulte para a definição canônica do vault.

---

## O operador `+`: o camaleão

O `+` é o único operador aritmético que também serve para concatenar strings. Essa dualidade é a fonte de muita confusão.

**Regra:** se *qualquer* operando for `string`, o `+` concatena. Caso contrário, converte tudo para `number` e soma.

```js
"5" + 3       // "53"   — 3 vira string, concatena
5 + "3"       // "53"   — 5 vira string, concatena
5 + 3         // 8      — ambos são número, soma
5 - "3"       // 2      — "-" não concatena, "3" vira número
true + 1      // 2      — true vira 1
false + 1     // 1      — false vira 0
null + 1      // 1      — null vira 0
undefined + 1 // NaN    — undefined vira NaN
```

> [!question]- Por que `"5" + 3` é `"53"` mas `"5" - 3` é `2`?
> O `+` tem dupla personalidade: soma números *e* concatena strings. Quando vê uma string, assume papel de concatenador. Já `-`, `*` e `/` são *exclusivamente* aritméticos — não há semântica de string, então convertem tudo para número antes de operar.

---

## Truthy e falsy: a lista que você precisa decorar

Toda vez que JavaScript precisa de um `boolean` — em `if`, `while`, `? :`, `||`, `&&` — ele converte o valor. Esse processo é chamado de **coerção booleana**.

Os valores que se tornam `false` são chamados de **falsy**. São exatamente **8**:

```js
false
0
-0
0n        // BigInt zero
""        // string vazia (aspas simples ou duplas ou template)
null
undefined
NaN
```

**Todo o resto é truthy.** Isso inclui:

```js
[]         // array vazio — TRUTHY
{}         // objeto vazio — TRUTHY
"0"        // string "zero" — TRUTHY (não é vazia!)
"false"    // string com texto — TRUTHY
-1         // qualquer número não-zero — TRUTHY
Infinity   // TRUTHY
```

> [!warning] Armadilha: array vazio é truthy
> `if ([])` entra no bloco — `[]` é truthy. Mas `[] == false` é `true` (via coerção numérica). Os dois comportamentos parecem contradizer um ao outro. A diferença: coerção booleana (`if`) e algoritmo `==` são mecanismos distintos.

---

## `==` vs `===`: dois algoritmos diferentes

### Igualdade estrita `===`

Simples: compara **tipo** e **valor**. Se os tipos forem diferentes, retorna `false` sem mais conversa.

```js
1 === "1"    // false — tipos diferentes
1 === 1      // true
null === undefined  // false — tipos diferentes
```

### Igualdade abstrata `==` (Abstract Equality Comparison)

Aqui entra a coerção. O algoritmo da spec (ECMAScript §7.2.14) é:

```
Dados x e y:
1. Se Type(x) === Type(y): compare como === (com regras especiais para NaN)
2. null == undefined → true (e undefined == null → true)
3. null ou undefined == qualquer outra coisa → false
4. Se um é número e o outro é string: converte a string para número, recompara
5. Se um é boolean: converte o boolean para número, recompara
6. Se um é objeto e o outro é string, número ou symbol: converte o objeto via ToPrimitive(), recompara
```

Visualizando as conversões prioritárias:

```mermaid
%%{init: {"theme": "base", "themeVariables": {"primaryColor": "#4A90D9", "edgeLabelBackground": "#ffffff"}}}%%
flowchart TD
    START([x == y]) --> SAMETYPE{Mesmo tipo?}
    SAMETYPE -->|sim| STRICT[Compara como ===]
    SAMETYPE -->|não| NULLCHECK{null ou undefined?}
    NULLCHECK -->|null == undefined| TRUE([true])
    NULLCHECK -->|null/undef == outro| FALSE([false])
    NULLCHECK -->|outros tipos| BOOLCHECK{Algum é boolean?}
    BOOLCHECK -->|sim| TONUMBER1[Converte boolean → Number\nentão recompara]
    BOOLCHECK -->|não| STRNUM{String e Number?}
    STRNUM -->|sim| TONUMBER2[Converte string → Number\nentão recompara]
    STRNUM -->|não| OBJCHECK{Algum é objeto?}
    OBJCHECK -->|sim| TOPRIM[ToPrimitive no objeto\nentão recompara]
    OBJCHECK -->|não| FALSE2([false])

    style TRUE fill:#4A90D9,color:#fff
    style FALSE fill:#D0021B,color:#fff
    style FALSE2 fill:#D0021B,color:#fff
    style TONUMBER1 fill:#F5A623,color:#fff
    style TONUMBER2 fill:#F5A623,color:#fff
    style TOPRIM fill:#F5A623,color:#fff
```

---

## A tabela de coerção do `==`

As comparações que mais aparecem em entrevistas:

| Comparação | Resultado | Por quê |
|---|---|---|
| `null == undefined` | `true` | Regra especial da spec |
| `null == false` | `false` | null só iguala undefined |
| `null == 0` | `false` | null só iguala undefined |
| `0 == false` | `true` | false → 0; 0 == 0 |
| `"" == false` | `true` | false → 0; "" → 0; 0 == 0 |
| `"1" == 1` | `true` | "1" → 1; 1 == 1 |
| `"0" == false` | `true` | false → 0; "0" → 0; 0 == 0 |
| `[] == false` | `true` | false → 0; [] → "" → 0; 0 == 0 |
| `[] == 0` | `true` | [] → "" → 0; 0 == 0 |
| `{} == false` | `false` | {} → "[object Object]" → NaN; NaN ≠ 0 |

---

## As pegadinhas clássicas — passo a passo

### `[] + []`

```
Passo 1: + com dois objetos → tenta concatenar (nenhum é string ainda)
Passo 2: ToPrimitive([]) → toString([]) → ""
Passo 3: ToPrimitive([]) → ""
Passo 4: "" + "" → ""
Resultado: "" (string vazia)
```

### `[] + {}`

```
Passo 1: ToPrimitive([]) → ""
Passo 2: ToPrimitive({}) → "[object Object]"
Passo 3: "" + "[object Object]" → "[object Object]"
Resultado: "[object Object]"
```

> [!warning] Armadilha: `{} + []` parece diferente no console
> No console do navegador, `{} + []` pode retornar `0` porque o `{}` é interpretado como **bloco vazio**, não objeto literal. O `+[]` vira `+""` vira `0`. Mas numa expressão `({}) + []`, com o objeto entre parênteses, retorna `"[object Object]"`.

### `[] == ![]`

Esta é a mais famosa. Vamos devagar:

```
Passo 1: Avalia o lado direito primeiro — ![]
  ![] → !true → false   ([] é truthy, ! nega → false)

Passo 2: Agora a comparação é [] == false

Passo 3: Regra 5 — um dos lados é boolean
  false → Number(false) → 0
  Agora: [] == 0

Passo 4: Regra 6 — um lado é objeto
  ToPrimitive([]) → [].toString() → ""
  Agora: "" == 0

Passo 5: Regra 4 — string e número
  Number("") → 0
  Agora: 0 == 0 → true

Resultado: true
```

> [!question]- Por que `ToPrimitive([])` vira `""`?
> Arrays têm um método `toString()` que junta os elementos com vírgula. Um array vazio não tem elementos, então `[].toString()` retorna `""`. Um array `[1, 2, 3].toString()` retorna `"1,2,3"`. É por isso que `[1] == 1` também é `true`: `"1"` → `1`.

---

## `Object.is`: igualdade sem surpresas

O ECMAScript 2015 introduziu `Object.is()` para cobrir os dois edge cases onde `===` se comporta estranhamente:

| Comparação | `===` | `Object.is()` |
|---|---|---|
| `NaN === NaN` | `false` | `true` |
| `0 === -0` | `true` | `false` |
| `1 === 1` | `true` | `true` |
| `null === null` | `true` | `true` |

### Por que `NaN !== NaN`?

`NaN` significa *Not a Number* — o resultado de operações matemáticas inválidas. A pergunta "esse resultado inválido é igual àquele resultado inválido?" não faz sentido semântico: `0/0` e `Math.sqrt(-1)` são ambos `NaN`, mas representam erros diferentes. A spec IEEE 754 (que define ponto flutuante) manda que NaN != NaN.

```js
NaN === NaN        // false — por definição
Object.is(NaN, NaN) // true — quando você PRECISA verificar se é NaN
Number.isNaN(NaN)  // true — a forma correta de checar NaN
isNaN("hello")     // true — CUIDADO: converte antes de checar (evite)
```

### Por que `-0`?

`-0` existe por causa do ponto flutuante IEEE 754. Representa a direção de aproximação ao zero (vindo de negativo). Na maioria dos casos não importa, mas em cálculos de direção/ângulo pode ser relevante.

```js
0 === -0            // true — === ignora o sinal
Object.is(0, -0)   // false — Object.is preserva o sinal
1 / 0              // Infinity
1 / -0             // -Infinity — aqui a diferença aparece
```

---

## Boas práticas

**Regra de ouro: sempre use `===`.**

A única exceção deliberada aceita pela comunidade é o idiom de checagem de nulo:

```js
// Idiom == null: captura tanto null quanto undefined com um só teste
if (valor == null) {
  // entra aqui se valor for null OU undefined
}

// Equivalente verboso:
if (valor === null || valor === undefined) {
  // mesmo comportamento
}
```

Por quê esse é o único `==` tolerado? Porque `null == undefined` é uma das poucas regras do algoritmo que é *intuitiva* e *estável* — nunca muda, não envolve conversão numérica, e a semântica ("não tenho valor algum") faz sentido.

```js
// Exemplos concretos de boas práticas

// ✗ evite
if (x == 0)       // "" também passa, false também passa
if (x == false)   // "" e 0 também passam

// ✓ prefira
if (x === 0)      // só zero exato
if (x === false)  // só false
if (!x)           // se você quer falsy explicitamente (documente o motivo)
if (x == null)    // único == tolerado — null ou undefined
```

---

## Armadilhas comuns

> [!warning] Armadilha 1: `typeof NaN === "number"`
> `NaN` é do tipo `"number"` — é um valor numérico especial que representa "não é um número válido". Para verificar NaN, use `Number.isNaN(valor)`, não `valor === NaN` (que sempre é `false`) e não `isNaN(valor)` (que converte antes de checar).

> [!warning] Armadilha 2: `"0"` é truthy, mas `"0" == false` é `true`
> A coerção booleana (`if ("0")`) e o algoritmo `==` são mecanismos independentes. `"0"` não é string vazia, então é truthy em contexto booleano. Mas `"0" == false` passa por: `false → 0`, depois `"0" → 0`, e `0 == 0` é `true`. Dois sistemas, dois resultados — daí a importância de usar `===`.

> [!warning] Armadilha 3: `null + 1` vs `undefined + 1`
> `null` em contexto numérico vira `0` — então `null + 1 === 1`. `undefined` vira `NaN` — então `undefined + 1 === NaN`. Isso afeta loops e acumuladores que partem de valor padrão: inicialize sempre com `0`, não com `null`.

> [!warning] Armadilha 4: `parseInt` e coerção de string
> `parseInt("10px")` retorna `10` — para de converter no primeiro caractere não-numérico. `Number("10px")` retorna `NaN`. Em validação de inputs, `Number()` é mais seguro porque rejeita strings parcialmente numéricas.

---

## Como explicar em inglês

In JavaScript, **type coercion** is the automatic conversion of values between types. The loose equality operator (`==`) triggers the *Abstract Equality Comparison* algorithm, which converts operands before comparing — this is why `[] == ![]` evaluates to `true`. Strict equality (`===`) compares type and value without any conversion, making it the safe default. The eight **falsy values** are `false`, `0`, `-0`, `0n`, `""`, `null`, `undefined`, and `NaN` — everything else, including empty arrays and objects, is **truthy**. `Object.is()` is the most precise equality check, correctly handling `NaN` (equal to itself) and `-0` (distinct from `+0`).

| PT | EN |
|---|---|
| coerção implícita | implicit coercion / type coercion |
| coerção explícita | explicit coercion / type casting |
| igualdade estrita | strict equality |
| igualdade abstrata | abstract equality / loose equality |
| valor falsy | falsy value |
| valor truthy | truthy value |
| conversão de tipo | type conversion |
| primitivo | primitive |
| algoritmo de comparação | comparison algorithm |

---

## O que vem a seguir

Coerção e tipos caminham juntos — entender *quais* tipos existem em JavaScript e como eles se comportam em memória é o passo natural antes (ou imediatamente depois) de dominar as regras de coerção.

- `[[02 - Tipos em runtime]]` — os 8 tipos primitivos e o tipo `object`: como são representados, como verificar com `typeof`/`instanceof`, e por que isso importa para coerção (nota a ser criada)
- `[[Dicionário de JavaScript]]` — definições canônicas de coerção, truthy/falsy e primitivo no contexto do vault

---

## Fontes

- **MDN Web Docs** — [*Equality comparisons and sameness*](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Equality_comparisons_and_sameness) — referência canônica para `==`, `===` e `Object.is()`, com a tabela completa de sameness
- **MDN Web Docs** — [*Equality (==)*](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Equality) — documentação do operador `==` com exemplos e o algoritmo Abstract Equality Comparison
- **Dr. Axel Rauschmayer / ExploringJS** — [*Type coercion in JavaScript*](https://exploringjs.com/deep-js/ch_type-coercion.html) — análise profunda das regras de coerção, com foco em ToPrimitive e Abstract Equality; fonte autoritativa
- **FreeCodeCamp** — [*JavaScript type coercion explained*](https://www.freecodecamp.org/news/js-type-coercion-explained-27ba3d9a2839/) — exemplos práticos das pegadinhas clássicas (`[] + []`, `[] == ![]`) com passo a passo
- **Stefan Judis** — [*+-0, NaN and Object.is in JavaScript*](https://www.stefanjudis.com/today-i-learned/0-nan-and-object-is-in-javascript/) — explicação concisa dos edge cases de `Object.is()` vs `===`
