---
title: "Domínio 1 — Datas, texto, números e booleanos"
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
  - "Domínio 1 OCP"
  - "Datas, texto e números na OCP"
---

# Domínio 1 — Datas, texto, números e booleanos

> [!abstract] TL;DR
> O primeiro objetivo da prova mistura quatro mundos — primitivos/wrappers, `String`, `java.time` e `BigDecimal` — e é onde moram as pegadinhas mais famosas (Integer cache, pool de Strings, `BigDecimal` a partir de `double`). A linguagem em si você já estudou nos galhos; aqui o foco é o que a Oracle cobra e como ela arma as armadilhas.

> [!info] Títulos oficiais
> - **1Z0-830 (Java 21):** *Handling Date, Time, Text, Numeric and Boolean Values*
> - **1Z0-831 (Java 25):** *Handling Date, Time, Text, Numeric and Boolean Values*
>
> Os títulos são idênticos nas duas versões da prova — este domínio não mudou de redação entre Java 21 e 25.

## O que a Oracle cobra

- **Primitivos e wrappers** — autoboxing/unboxing, range de cada tipo (`byte` -128..127, `int` ~±2,1 bi, `long`, `char` sem sinal, etc.).
- **Literais numéricos** — separador `_` (`100_000`), binário `0b1010`, hexadecimal `0xFF`, sufixo `long` `42L`, sufixo `float` `3.14f`.
- **Operadores** — precedência, associatividade, avaliação curta (*short-circuit*) `&&`/`||` vs lógicos `&`/`|`.
- **`String`** — imutabilidade, *string pool*, `equals` vs `==`, `compareTo`, `format`, *text blocks*.
- **`StringBuilder`** — quando preferir a `String` para concatenação em laço.
- **Date/Time API** — `LocalDate`, `LocalTime`, `LocalDateTime`, `ZonedDateTime`, `Instant`, `Duration`, `Period`.
- **`DateTimeFormatter`** — formatos ISO prontos vs *patterns* customizados.
- **`BigDecimal`** — por que evitar `float`/`double` para dinheiro, `setScale`, `RoundingMode`.
- **Valores booleanos** — `boolean` vs `Boolean`, autoboxing e o risco de `null`.

## Mapa de revisão

- [[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/02 - Tipos, variáveis e operadores|Tipos, variáveis e operadores (G1)]] — primitivos, wrappers, literais, operadores.
- [[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/04 - Strings e text blocks|Strings e text blocks (G1)]] — String, pool, text blocks, StringBuilder.
- [[03-Dominios/Tecnologia/Java/Collections e Streams/11 - java.time — Date e Time API|java.time — Date e Time API (G2)]] — toda a API de data/hora e formatação.

## Pegadinhas deste domínio

**1. Integer cache (`==` em wrappers).** A JVM mantém um *cache* de objetos `Integer` para a faixa **-128 a 127**. Comparar com `==` dentro dessa faixa devolve `true` (mesmo objeto); fora dela, `false` (objetos distintos).

```java
Integer a = 127, b = 127;
System.out.println(a == b);   // true  — vêm do cache

Integer c = 128, d = 128;
System.out.println(c == d);   // false — objetos diferentes
System.out.println(c.equals(d)); // true — sempre compare valor com equals
```

Regra de prova: **nunca compare wrappers com `==`**; use `equals` ou desempacote para primitivo.

**2. String pool (literal vs `new` vs `intern`).** Literais idênticos compartilham o mesmo objeto no *pool*; `new String(...)` força um objeto novo no *heap*; `intern()` devolve a referência do *pool*.

```java
String x = "ocp";
String y = "ocp";
String z = new String("ocp");

System.out.println(x == y);          // true  — mesmo literal no pool
System.out.println(x == z);          // false — z é objeto novo no heap
System.out.println(x == z.intern()); // true  — intern() volta ao pool
```

**3. `BigDecimal` a partir de `double`.** O construtor `new BigDecimal(double)` herda a imprecisão binária do `double`. Para valores exatos (dinheiro!), use `BigDecimal.valueOf` ou o construtor de `String`.

```java
new BigDecimal(0.1);            // 0.1000000000000000055511151231257827021181583404541015625
BigDecimal.valueOf(0.1);        // 0.1  — usa Double.toString por baixo
new BigDecimal("0.1");          // 0.1  — exato

new BigDecimal("10.005").setScale(2, RoundingMode.HALF_UP); // 10.01
```

**4. Autoboxing com `null` → NPE.** Desempacotar um wrapper `null` para primitivo lança `NullPointerException` em tempo de execução — não é erro de compilação.

```java
Integer total = null;
int n = total;   // NullPointerException no unboxing
```

Para o conjunto completo, veja o [[03-Dominios/Tecnologia/Java/Certificação OCP/15 - O catálogo de pegadinhas clássicas|catálogo de pegadinhas]].

## Em entrevista

> "I always use `BigDecimal` for monetary values to avoid floating-point rounding errors, and I never compare boxed wrappers with `==` because of the Integer cache."

| PT | EN |
| --- | --- |
| autoboxing | autoboxing |
| arredondamento | rounding |
| ponto flutuante | floating point |
| imutabilidade | immutability |
| desempacotar | unboxing |

## Veja também

- [[03-Dominios/Tecnologia/Java/Certificação OCP/04 - O mapa objetivo → galho — revisar a trilha pra prova|O mapa objetivo → galho]]
- [[03-Dominios/Tecnologia/Java/Certificação OCP/06 - Domínio 2 — Controle de fluxo|Domínio 2 — Controle de fluxo]]
- [[03-Dominios/Tecnologia/Java/Certificação OCP/index|Certificação OCP (MOC do galho)]]

## Referências

- Enthuware — *OCP Java 21 Exam Syllabus*: https://enthuware.com/oca-ocp-java-certification-resources/290-ocp-java-21-exam-syllabus
