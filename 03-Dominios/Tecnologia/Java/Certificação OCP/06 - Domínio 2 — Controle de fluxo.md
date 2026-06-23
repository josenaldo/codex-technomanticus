---
title: "Domínio 2 — Controle de fluxo"
created: 2026-06-13
updated: 2026-06-13
type: concept
status: seedling
publish: true
fase: dominios
tags:
  - java
  - certificacao-ocp
  - dominios
aliases:
  - "Domínio 2 OCP"
  - "Controle de fluxo na OCP"
---

# Domínio 2 — Controle de fluxo

> [!abstract] TL;DR
> Este é o domínio que separa quem decorou a sintaxe de quem entende a **semântica** do `switch`. A prova cobra `if`/`else`, loops e labels — coisa de iniciado — mas o que realmente pega é a fronteira entre **switch statement** (dois pontos, com fall-through) e **switch expression** (seta, sem fall-through), o **pattern matching em switch** com record patterns e guards (`when`), e a **exaustividade** exigida quando o switch é uma expressão sobre `enum` ou tipo `sealed`. Você já estudou tudo isto no Galho 1 — aqui é só recolocar os óculos de prova.

> [!info] Títulos oficiais
> - **1Z0-830 (Java 21):** *Controlling Program Flow*
> - **1Z0-831 (Java 25):** *Implementing Program Flow Control Using Decision and Looping Constructs*

## O que a Oracle cobra

- **`if`/`else`** — blocos e *nesting* (aninhamento); o clássico `if` sem chaves grudando só na primeira instrução.
- **`switch` statement vs `switch` expression** (Java 14+) — a diferença de sintaxe (`:` vs `->`) carrega uma diferença de semântica que a prova adora explorar.
- **Pattern matching em `switch`** (Java 21) — type patterns, **record patterns** (desestruturação) e **guards** com a cláusula `when`.
- **Loops** — `for` clássico, `enhanced for` (for-each), `while`, `do-while`.
- **Labels** — `break label;` e `continue label;` para controlar loops aninhados.
- **`return`, `break`, `continue`** — fluxo de saída e o efeito de cada um dentro de loops e switches.

## Mapa de revisão

- [[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/03 - Estruturas de controle e fluxo|Estruturas de controle e fluxo (G1)]] — if/switch/loops/labels.
- [[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/14 - Sealed classes e pattern matching|Sealed classes e pattern matching (G1)]] — pattern matching em switch, record patterns, exaustividade.

## Pegadinhas deste domínio

**1. Fall-through: o switch statement vaza, o switch expression não.**

O switch *statement* com dois pontos (`:`) executa em cascata a partir do `case` casado até encontrar um `break` — isto é o *fall-through*.

```java
int x = 2;
switch (x) {
    case 1: System.out.print("um ");
    case 2: System.out.print("dois ");   // entra aqui...
    case 3: System.out.print("três ");   // ...e cai pra cá
    default: System.out.print("default");
}
// Saída: dois três default
```

Já o switch *expression* com seta (`->`) **não** tem fall-through: cada braço é isolado.

```java
int x = 2;
switch (x) {
    case 1 -> System.out.print("um");
    case 2 -> System.out.print("dois");   // só isto roda
    case 3 -> System.out.print("três");
    default -> System.out.print("default");
}
// Saída: dois
```

**2. `yield`, não `return`, dentro de um bloco de switch expression.**

Quando o braço da seta vira um bloco `{ ... }`, o valor sai por `yield`. Usar `return` ali tenta sair do *método*, não do switch — erro de compilação ou comportamento errado.

```java
int dobro = switch (x) {
    case 1 -> 10;
    case 2 -> {
        int temp = calcula();
        yield temp * 2;   // yield, NÃO return
    }
    default -> 0;
};
```

**3. Exaustividade: switch expression sobre `enum`/`sealed` precisa cobrir tudo.**

Como o switch expression *produz um valor*, o compilador exige que **todos** os caminhos estejam cobertos. Sobre um `enum` ou tipo `sealed`, ou você lista todos os casos ou inclui um `default` — senão é erro de compilação. A graça do `sealed` + record patterns é que, com todos os subtipos cobertos, o compilador **infere** a exaustividade e você pode dispensar o `default`.

```java
sealed interface Forma permits Circulo, Quadrado {}
double area = switch (forma) {
    case Circulo(double r) -> Math.PI * r * r;
    case Quadrado(double l) -> l * l;
    // sem default: o compilador sabe que cobriu tudo
};
```

**4. `case null` agora é permitido (Java 21).**

Antes, um `switch` sobre `null` lançava `NullPointerException`. Desde o Java 21, dá pra ter um braço `case null` explícito — e combiná-lo como `case null, default ->`.

Mais armadilhas de sintaxe e semântica no [[03-Dominios/Tecnologia/Java/Certificação OCP/15 - O catálogo de pegadinhas clássicas|catálogo de pegadinhas]].

## Em entrevista

Você raramente vai *citar* a prova numa entrevista — mas o vocabulário aparece quando explicam por que preferem código moderno. Uma frase honesta:

> "I lean on switch expressions and pattern matching for control flow — they're exhaustive by construction over sealed types, so the compiler catches missing cases for me."

Sem reivindicar credencial que você ainda não tem. Vocabulário PT|EN:

- *fall-through* (cascata entre `case`s sem `break`)
- exaustividade → *exhaustiveness*
- guarda → *guard* (a cláusula `when`)

## Veja também

- [[03-Dominios/Tecnologia/Java/Certificação OCP/04 - O mapa objetivo → galho — revisar a trilha pra prova|O mapa objetivo → galho]]
- [[03-Dominios/Tecnologia/Java/Certificação OCP/07 - Domínio 3 — Orientação a objetos|Domínio 3 — Orientação a objetos]]
- [[03-Dominios/Tecnologia/Java/Certificação OCP/index|Certificação OCP (MOC do galho)]]

## Referências

- [OCP Java 21 Exam Syllabus (Enthuware)](https://enthuware.com/oca-ocp-java-certification-resources/290-ocp-java-21-exam-syllabus)
