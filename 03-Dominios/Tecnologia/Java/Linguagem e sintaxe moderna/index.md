---
title: "Linguagem e sintaxe moderna"
created: 2026-06-02
updated: 2026-06-02
type: moc
status: growing
publish: true
tags:
  - java
  - linguagem
  - moc
aliases:
  - Linguagem Java
  - Galho 1 - Linguagem
---

# Linguagem e sintaxe moderna

> [!abstract] TL;DR
> Galho 1 da trilha Java Senior. Cobre a camada de linguagem do Java moderno — da sintaxe básica e tipos até records, sealed classes e pattern matching. Base obrigatória de todos os outros galhos da trilha (JVM, Collections, Streams, Concorrência).

## Sobre este galho

Este galho cobre a **linguagem** Java de ponta a ponta: tipos primitivos e de referência, estruturas de controle, strings e text blocks, arrays, OOP clássica (classes, herança, polimorfismo, interfaces, enums), exceções, annotations e generics. Termina com as features modernas introduzidas nos últimos releases — records, sealed classes, pattern matching e switch expressions. Não cobre JVM/memória, Collections, Streams/lambdas, nem Concorrência — esses tópicos têm galhos próprios.

**Audiência primária:** dev senior em preparação para entrevista internacional. Cada nota tem seção "Em entrevista" com frases prontas em inglês e vocabulário técnico. **Audiência secundária:** o mesmo dev em contexto de decisões de design e code review — cada nota expõe o "porquê" por trás das escolhas de linguagem e as armadilhas mais cobradas.

## Iniciado

1. [[01 - O modelo da linguagem Java]] — visão panorâmica: plataforma, JVM, JDK vs JRE, o ciclo compilar-carregar-executar.
2. [[02 - Tipos, variáveis e operadores]] — tipos primitivos, wrappers, autoboxing, casting, operadores e precedência.
3. [[03 - Estruturas de controle e fluxo]] — if/else, switch clássico, for/while/do-while, break/continue/labeled.
4. [[04 - Strings e text blocks]] — imutabilidade, pool, métodos essenciais, `StringBuilder`, text blocks (Java 15+).
5. [[05 - Arrays e varargs]] — arrays unidimensionais e multidimensionais, `Arrays` utilitário, varargs e armadilhas.

## Adepto

6. [[06 - Classes, objetos e encapsulamento]] — construtores, `this`, getters/setters, modificadores de acesso, `static`, `final`.
7. [[07 - Herança e polimorfismo]] — `extends`, override vs overload, `super`, cast de referência, Liskov na prática.
8. [[08 - Interfaces e classes abstratas]] — `interface` vs `abstract class`, `default`/`static`/`private` em interfaces, múltipla herança de tipo.
9. [[09 - Enums]] — enums como classes, campos e métodos, `EnumSet`/`EnumMap`, uso em switch.
10. [[10 - Exceções e tratamento de erros]] — hierarquia checked/unchecked, try-with-resources, multi-catch, boas práticas de design.
11. [[11 - Annotations]] — meta-anotações, anotações built-in (`@Override`, `@FunctionalInterface`), retenção e processamento.

## Magus

12. [[12 - Generics em profundidade]] — type erasure, wildcards (`? extends`/`? super`), bounded type parameters, PECS.
13. [[13 - Records e record patterns]] — `record` como carrier imutável, compact constructors, record patterns no `instanceof`/switch.
14. [[14 - Sealed classes e pattern matching]] — `sealed`/`permits`, pattern matching para `instanceof`, switch expressions exaustivos.
15. [[15 - A evolução do Java (8 a 25)]] — linha do tempo das features por versão, LTS releases, o que cobrar em cada nível de senioridade.

## Rotas alternativas

### Completa

01 → 02 → 03 → 04 → 05 → 06 → 07 → 08 → 09 → 10 → 11 → 12 → 13 → 14 → 15. Percurso linear do básico ao avançado.

### Entrevista internacional

01 → 07 → 10 → 12 → 13 → 14. Foco em explicar OOP, tratamento de erros, generics e features modernas para um entrevistador sênior.

### Features modernas (Java recente)

03 → 04 → 13 → 14 → 15. Records, sealed classes, pattern matching, switch expressions e text blocks — o Java dos últimos releases.

### Revisão pré-OCP

02 → 05 → 07 → 08 → 10 → 12. Tópicos com maior peso na certificação Oracle Certified Professional Java SE.

### Fundamentos OOP

06 → 07 → 08 → 09. Firmar a orientação a objetos clássica antes de avançar para features modernas.

## Todas as notas

```dataview
TABLE fase, status, updated
FROM "03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna"
WHERE type = "concept"
SORT file.name ASC
```

## Veja também

- [[03-Dominios/Tecnologia/Java/index|Java (MOC central)]]
- [[Java Fundamentals]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java|Dicionário de Java]]
- [[03-Dominios/Tecnologia/Java/Core/Helsinki MOOC - Guia de Revisão|Helsinki MOOC]]
