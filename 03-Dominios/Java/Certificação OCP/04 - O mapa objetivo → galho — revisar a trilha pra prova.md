---
title: "O mapa objetivo → galho — revisar a trilha pra prova"
created: 2026-06-13
updated: 2026-06-13
type: concept
status: seedling
publish: true
fase: sobre-a-prova
tags:
  - java
  - certificacao-ocp
  - sobre-a-prova
aliases:
  - "Mapa objetivo galho"
  - "Revisar a trilha pra OCP"
---

# O mapa objetivo → galho — revisar a trilha pra prova

> [!abstract] TL;DR
> Se você já percorreu a trilha Java, esta é a porta de revisão pra prova: cada domínio oficial do exame aponta para as notas exatas que o cobrem. As duas provas (1Z0-830/Java 21 e 1Z0-831/Java 25) compartilham os mesmos 10 domínios, então o mapa serve as duas.

## Como usar este mapa

Identifique o domínio em que você está fraco — talvez você acerte tudo de Streams mas trave em concorrência, ou domine OO mas escorregue em datas. Vá às notas linkadas na coluna "Onde revisar na trilha" e releia com calma; depois passe pela nota de domínio desta pasta, que destila o que a prova cobra. Antes de fechar o ciclo, atravesse o [[03-Dominios/Java/Certificação OCP/15 - O catálogo de pegadinhas clássicas|catálogo de pegadinhas]] — é onde mora a maior parte dos pontos que se perde por desatenção, não por desconhecimento. Os três domínios marcados "Parcial" têm gaps que a trilha não cobre por inteiro; nesses casos, a seção "Lacuna da trilha" da nota do próprio domínio carrega o que falta.

## O mapa

| Domínio | Onde revisar na trilha | Nota deste galho | Cobertura |
| --- | --- | --- | --- |
| Domínio 1 — Datas, texto, números e booleanos | [[03-Dominios/Java/Linguagem e sintaxe moderna/02 - Tipos, variáveis e operadores\|Tipos e operadores]], [[03-Dominios/Java/Linguagem e sintaxe moderna/04 - Strings e text blocks\|Strings e text blocks]], [[03-Dominios/Java/Collections e Streams/11 - java.time — Date e Time API\|java.time]] | [[03-Dominios/Java/Certificação OCP/05 - Domínio 1 — Datas, texto, números e booleanos\|Domínio 1]] | Cheia |
| Domínio 2 — Controle de fluxo | [[03-Dominios/Java/Linguagem e sintaxe moderna/03 - Estruturas de controle e fluxo\|Controle e fluxo]], [[03-Dominios/Java/Linguagem e sintaxe moderna/14 - Sealed classes e pattern matching\|Sealed e pattern matching]] | [[03-Dominios/Java/Certificação OCP/06 - Domínio 2 — Controle de fluxo\|Domínio 2]] | Cheia |
| Domínio 3 — Orientação a objetos | [[03-Dominios/Java/Linguagem e sintaxe moderna/06 - Classes, objetos e encapsulamento\|Classes e encapsulamento]], [[03-Dominios/Java/Linguagem e sintaxe moderna/07 - Herança e polimorfismo\|Herança e polimorfismo]], [[03-Dominios/Java/Linguagem e sintaxe moderna/08 - Interfaces e classes abstratas\|Interfaces e abstratas]], [[03-Dominios/Java/Linguagem e sintaxe moderna/09 - Enums\|Enums]], [[03-Dominios/Java/Linguagem e sintaxe moderna/11 - Annotations\|Annotations]], [[03-Dominios/Java/Linguagem e sintaxe moderna/12 - Generics em profundidade\|Generics]], [[03-Dominios/Java/Linguagem e sintaxe moderna/13 - Records e record patterns\|Records]], [[03-Dominios/Java/Linguagem e sintaxe moderna/14 - Sealed classes e pattern matching\|Sealed classes]] | [[03-Dominios/Java/Certificação OCP/07 - Domínio 3 — Orientação a objetos\|Domínio 3]] | Cheia |
| Domínio 4 — Exceções | [[03-Dominios/Java/Linguagem e sintaxe moderna/10 - Exceções e tratamento de erros\|Exceções e tratamento de erros]] | [[03-Dominios/Java/Certificação OCP/08 - Domínio 4 — Exceções\|Domínio 4]] | Cheia |
| Domínio 5 — Arrays e coleções | [[03-Dominios/Java/Linguagem e sintaxe moderna/05 - Arrays e varargs\|Arrays e varargs]], [[03-Dominios/Java/Collections e Streams/01 - O Collections Framework\|Collections Framework]], [[03-Dominios/Java/Collections e Streams/02 - Listas, conjuntos e filas\|Listas, conjuntos e filas]], [[03-Dominios/Java/Collections e Streams/03 - Mapas\|Mapas]], [[03-Dominios/Java/Collections e Streams/06 - Comparable e Comparator\|Comparable e Comparator]], [[03-Dominios/Java/Collections e Streams/14 - SequencedCollection e SequencedMap\|Sequenced collections]] | [[03-Dominios/Java/Certificação OCP/09 - Domínio 5 — Arrays e coleções\|Domínio 5]] | Cheia |
| Domínio 6 — Streams e lambdas | [[03-Dominios/Java/Collections e Streams/04 - Lambdas e interfaces funcionais\|Lambdas e interfaces funcionais]], [[03-Dominios/Java/Collections e Streams/05 - Introdução à Stream API\|Stream API]], [[03-Dominios/Java/Collections e Streams/07 - Operações de Stream — intermediárias e terminais\|Operações de Stream]], [[03-Dominios/Java/Collections e Streams/08 - Collectors e agrupamento\|Collectors]], [[03-Dominios/Java/Collections e Streams/09 - Streams primitivos\|Streams primitivos]], [[03-Dominios/Java/Collections e Streams/10 - Optional\|Optional]], [[03-Dominios/Java/Collections e Streams/13 - Composição funcional e funções de alta ordem\|Composição funcional]], [[03-Dominios/Java/Collections e Streams/15 - Collectors customizados e Gatherers\|Collectors e Gatherers]] | [[03-Dominios/Java/Certificação OCP/10 - Domínio 6 — Streams e lambdas\|Domínio 6]] | Cheia |
| Domínio 7 — Empacotamento, deployment e módulos | [[03-Dominios/Java/JVM/08 - JPMS — o sistema de módulos\|JPMS (módulos)]], [[03-Dominios/Java/JavaFX/13 - Empacotamento — módulos, jlink e jpackage\|jlink e jpackage]], [[03-Dominios/Java/Linguagem e sintaxe moderna/15 - A evolução do Java (8 a 25)\|Evolução do Java]] | [[03-Dominios/Java/Certificação OCP/11 - Domínio 7 — Empacotamento, deployment e módulos\|Domínio 7]] | Parcial |
| Domínio 8 — Concorrência | [[03-Dominios/Java/Concorrência e paralelismo/02 - Threads e seu ciclo de vida\|Threads]], [[03-Dominios/Java/Concorrência e paralelismo/03 - Exclusão mútua com synchronized\|synchronized]], [[03-Dominios/Java/Concorrência e paralelismo/06 - Atômicos e operações lock-free\|Atômicos]], [[03-Dominios/Java/Concorrência e paralelismo/07 - Concurrent collections\|Concurrent collections]], [[03-Dominios/Java/Concorrência e paralelismo/08 - Executors e thread pools\|Executors]], [[03-Dominios/Java/Concorrência e paralelismo/10 - CompletableFuture e composição assíncrona\|CompletableFuture]], [[03-Dominios/Java/Concorrência e paralelismo/11 - Java Memory Model em profundidade\|Java Memory Model]], [[03-Dominios/Java/Concorrência e paralelismo/12 - Virtual Threads e Project Loom\|Virtual Threads]], [[03-Dominios/Java/Concorrência e paralelismo/15 - Parallel streams e fork-join\|Parallel streams]] | [[03-Dominios/Java/Certificação OCP/12 - Domínio 8 — Concorrência\|Domínio 8]] | Cheia |
| Domínio 9 — I/O | [[03-Dominios/Java/Collections e Streams/12 - I-O moderno com java.nio.file\|I/O com java.nio.file]] | [[03-Dominios/Java/Certificação OCP/13 - Domínio 9 — I-O\|Domínio 9]] | Parcial |
| Domínio 10 — Localização | [[03-Dominios/Java/Collections e Streams/11 - java.time — Date e Time API\|java.time (DateTimeFormatter)]] | [[03-Dominios/Java/Certificação OCP/14 - Domínio 10 — Localização\|Domínio 10]] | Parcial |

## Os três domínios que a trilha não cobre por inteiro

A trilha Java foi pensada para formar engenheiros, não para casar 1:1 com um syllabus de prova — então três domínios chegam ao exame com cobertura apenas **Parcial**. Cada nota de domínio correspondente carrega o que falta numa seção "Lacuna da trilha", e este é um recorte honesto: melhor declarar o gap do que fingir que a trilha cobre tudo.

- **Domínio 7 — Empacotamento, deployment e módulos**: a trilha cobre JPMS, jlink e jpackage, mas falta o `jar` clássico (manifest, classpath), o JShell e o `instance main` (compactos / launch protocol).
- **Domínio 9 — I/O**: a trilha cobre `java.nio.file` moderno, mas falta o `java.io` clássico (streams de bytes/chars, `Reader`/`Writer`), serialização e o `Console`.
- **Domínio 10 — Localização**: a trilha cobre `DateTimeFormatter` via `java.time`, mas falta `Locale`, `ResourceBundle` e `NumberFormat`.

## Veja também

- [[03-Dominios/Java/Certificação OCP/15 - O catálogo de pegadinhas clássicas|O catálogo de pegadinhas clássicas]]
- [[03-Dominios/Java/Certificação OCP/02 - Qual prova mirar — Java 21 (1Z0-830) vs Java 25 (1Z0-831)|Qual prova mirar]]
- [[03-Dominios/Java/Certificação OCP/index|Certificação OCP (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]

## Referências

- Enthuware syllabus 21: https://enthuware.com/oca-ocp-java-certification-resources/290-ocp-java-21-exam-syllabus
- Enthuware syllabus 25: https://enthuware.com/oca-ocp-java-certification-resources/297-ocp-java-25-exam-syllabus
