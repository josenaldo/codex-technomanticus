---
title: "Domínio 3 — Orientação a objetos"
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
  - "Domínio 3 OCP"
  - "Orientação a objetos na OCP"
---

# Domínio 3 — Orientação a objetos

> [!abstract] TL;DR
> Este é o domínio de **maior peso** da prova — e o mais traiçoeiro. A Oracle não testa se você "entende OO"; testa se você sabe a **regra exata** que o compilador e a JVM aplicam num caso de canto: ordem de inicialização, hiding vs override, resolução de overload, semântica de `final`. A pegadinha quase nunca é conceitual; é uma linha que compila (ou não) por um detalhe. Decore as regras, não as intuições.

> [!info] Títulos oficiais
> - **1Z0-830 (Java 21):** *Using Object-Oriented Concepts in Java*
> - **1Z0-831 (Java 25):** *Applying Object-Oriented Principles in Java Programs*
>
> O título evolui de *Using* (Java 21) para *Applying* (Java 25), sinalizando ênfase crescente em aplicar princípios — mas o miolo cobrado é o mesmo bloco de regras abaixo.

## O que a Oracle cobra

- **Classes, objetos e construtores** — construtor default (gerado só se você não declara nenhum), chaining com `this()` e `super()` (sempre na **primeira** linha; nunca os dois juntos), e a **ordem de inicialização** completa.
- **Initializers e final fields** — `static` initializer vs instance initializer, blank `final` que precisa ser atribuído exatamente uma vez antes do fim do construtor.
- **Métodos** — `varargs` (no máximo um, e por último), covariância de retorno (subtipo no override), passagem de parâmetro por valor.
- **Encapsulamento e modificadores de acesso** — `private`, default (package-private), `protected`, `public`; o que `protected` libera de outro pacote (só via herança, sobre o próprio tipo).
- **Herança, `@Override`, polimorfismo** — `extends`, regras de assinatura no override (mesmo nome+params, retorno covariante, visibilidade não pode encolher, checked exceptions não podem alargar), **dynamic dispatch** (o método chamado depende do tipo em runtime).
- **Casting, `instanceof`, pattern matching** — upcast implícito, downcast explícito, `ClassCastException`, `instanceof` com binding de variável, pattern matching em `switch`.
- **Classes abstratas vs interfaces** — quando usar cada, métodos abstratos, campos (interface = `public static final` implícito).
- **Default methods** — diamond problem, regra de resolução (classe vence interface; interface mais específica vence), chamada explícita `Interface.super.method()`.
- **`static` e `final`** — semântica exata: static pertence ao tipo, final impede reatribuição/herança/override.
- **Inner classes** — static nested, inner (não-estática, segura referência à instância externa), local (dentro de método), anônima.
- **Enums** — com métodos e construtores, `values()`, `valueOf()`, constantes com corpo (body-specific override).
- **Records** — componentes, compact constructor, `equals`/`hashCode`/`toString` gerados, accessors.
- **Sealed classes** — `sealed`, `permits`, e a obrigação de cada subtipo permitido ser `final`, `sealed` ou `non-sealed`.

## Mapa de revisão

- [[03-Dominios/Java/Linguagem e sintaxe moderna/06 - Classes, objetos e encapsulamento|Classes, objetos e encapsulamento (G1)]]
- [[03-Dominios/Java/Linguagem e sintaxe moderna/07 - Herança e polimorfismo|Herança e polimorfismo (G1)]]
- [[03-Dominios/Java/Linguagem e sintaxe moderna/08 - Interfaces e classes abstratas|Interfaces e classes abstratas (G1)]]
- [[03-Dominios/Java/Linguagem e sintaxe moderna/09 - Enums|Enums (G1)]]
- [[03-Dominios/Java/Linguagem e sintaxe moderna/11 - Annotations|Annotations (G1)]]
- [[03-Dominios/Java/Linguagem e sintaxe moderna/12 - Generics em profundidade|Generics em profundidade (G1)]]
- [[03-Dominios/Java/Linguagem e sintaxe moderna/13 - Records e record patterns|Records e record patterns (G1)]]
- [[03-Dominios/Java/Linguagem e sintaxe moderna/14 - Sealed classes e pattern matching|Sealed classes e pattern matching (G1)]]

## Pegadinhas deste domínio

**1. Ordem de inicialização.** A sequência exata, e a prova adora misturá-la com herança. Para uma instância: super primeiro, e dentro de cada classe os fields/instance initializers rodam **na ordem do código**, depois o corpo do construtor.

```java
class A {
    static { System.out.print("1"); }   // static block (uma vez, no class-load)
    { System.out.print("3"); }           // instance initializer
    A() { System.out.print("4"); }       // construtor
}
// ordem ao criar new A(): static (1) → instance initializer (3) → construtor (4)
// com herança: static do pai → static do filho → (super) instance+ctor do pai → instance+ctor do filho
```

**2. Sobrescrita de método `static` NÃO existe — é hiding.** Métodos estáticos não participam de dynamic dispatch. A chamada é resolvida em **compile-time** pelo **tipo declarado** da referência, não pelo objeto real.

```java
class Pai    { static String quem() { return "Pai"; } }
class Filho extends Pai { static String quem() { return "Filho"; } }

Pai p = new Filho();
System.out.println(p.quem());   // "Pai" — hiding, resolvido pelo tipo declarado (Pai)
```

**3. Resolução de overload com autoboxing.** O compilador tenta em fases, e **nunca** pula etapas: **exact match → widening → autoboxing → varargs**. Um `int` prefere `long` (widening) a `Integer` (autoboxing).

```java
void f(long x)    { }   // widening
void f(Integer x) { }   // autoboxing
f(5);   // chama f(long) — widening ganha de autoboxing
```

**4. Enum constructor é sempre implicitamente `private`.** Você não pode chamar `new` numa enum, e declarar o construtor `public`/`protected` não compila. Ele roda **uma vez por constante**, na ordem em que as constantes aparecem, no primeiro uso da enum.

**5. Record component é `final`.** Não há setter, e você não reatribui o componente no corpo de método nenhum. No compact constructor você pode **validar/normalizar** os parâmetros (que ainda não foram atribuídos), mas a atribuição final aos campos é implícita.

```java
record Range(int lo, int hi) {
    Range {                          // compact constructor
        if (lo > hi) throw new IllegalArgumentException();
        // lo = 0;  // OK aqui: ajusta o PARÂMETRO antes da atribuição implícita
    }
    // void set(int v) { lo = v; }   // NÃO compila — lo é final
}
```

**6. `final` em parâmetro não afeta o caller.** Java é sempre pass-by-value. `final` num parâmetro só impede reatribuir a variável **dentro** do método; a variável do chamador é intocável de qualquer jeito. É decoração local, nunca contrato.

**7. Generics e type erasure.** Em runtime, a informação de tipo genérico some. Dois `List` de parametrizações diferentes compartilham a **mesma** classe.

```java
List<String>  ls = new ArrayList<>();
List<Integer> li = new ArrayList<>();
System.out.println(ls.getClass() == li.getClass());   // true — erasure
```

Para o arsenal completo, veja o [[03-Dominios/Java/Certificação OCP/15 - O catálogo de pegadinhas clássicas|catálogo de pegadinhas]].

## Em entrevista

Não reivindique a credencial até tê-la em mãos — mas a clareza conceitual aparece. Sobre static hiding:

> "A `static` method isn't polymorphic — it's **hidden**, not **overridden**. The call binds at compile time to the declared type, so dynamic dispatch never kicks in. Only instance methods are virtually dispatched."

**Vocabulário PT|EN:** sobrescrita → *override* · sobrecarga → *overload* · ocultação → *hiding* · despacho dinâmico → *dynamic dispatch*.

## Veja também

- [[03-Dominios/Java/Certificação OCP/04 - O mapa objetivo → galho — revisar a trilha pra prova|O mapa objetivo → galho]]
- [[03-Dominios/Java/Certificação OCP/08 - Domínio 4 — Exceções|Domínio 4 — Exceções]]
- [[03-Dominios/Java/Certificação OCP/index|Certificação OCP (MOC do galho)]]

## Referências

- [Enthuware — OCP Java 21 Exam Syllabus](https://enthuware.com/oca-ocp-java-certification-resources/290-ocp-java-21-exam-syllabus)
