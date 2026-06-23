---
title: "Qual prova mirar — Java 21 (1Z0-830) vs Java 25 (1Z0-831)"
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
  - "1Z0-830"
  - "1Z0-831"
  - "OCP Java 21 vs 25"
---

# Qual prova mirar — Java 21 (1Z0-830) vs Java 25 (1Z0-831)

> [!abstract] TL;DR
> Em 2026 há **duas provas OCP vigentes**: o **1Z0-830** (Java SE 21) e o **1Z0-831** (Java SE 25, lançado em 01/mai/2026). O mapeamento da trilha pra prova serve **as duas** — os 10 domínios são praticamente idênticos. A escolha é de bom senso: mire o **21** se quer **material maduro** (livro Sybex, mocks Enthuware consolidados) ou o **25** se quer a **LTS mais nova** e já absorveu seus recursos pela trilha. Sem dogma.

## As versões vigentes

A Oracle atualiza a certificação a cada nova LTS. Em 2026, o quadro é este:

| Certificação | Prova | Versão | Status | Material |
| --- | --- | --- | --- | --- |
| **OCP Java SE 25** | 1Z0-831 | LTS 25 | Lançada em 01/mai/2026 | Sem livro Sybex ainda |
| **OCP Java SE 21** | 1Z0-830 | LTS 21 | Atual e consolidada | Livro Sybex + Enthuware maduros |
| OCP Java SE 17 | 1Z0-829 | LTS 17 | Ainda válida | Use se já estudou pra ela |
| Java 11 (1Z0-819) e Java 8 (1Z0-809) | — | LTS 11 / 8 | Legadas | Evite |

Repare que **não há uma "prova mais certa"**: 830 e 831 estão **ambas ativas** e cobrem o mesmo corpo de conhecimento. A diferença prática é a maturidade do material de estudo, não o conteúdo.

> [!warning] Sobre o futuro do 1Z0-830
> A Oracle **não anunciou** aposentadoria (retirement) do 1Z0-830 nem data pra isso. Não dá pra afirmar que ele será descontinuado — apenas que, no momento, **continua ativo** ao lado do 1Z0-831.

## A linhagem — de OCA+OCP a prova única

Quem pesquisa certificação Java esbarra em siglas de várias eras. Vale entender a consolidação pra não estudar material errado:

- **Era Java 8 (e antes):** o caminho era **duas provas** — OCA (Associate, 1Z0-808) e depois OCP (Professional, 1Z0-809). A OCA era pré-requisito pro OCP.
- **A morte da OCA (Java 11):** desde o Java 11, a Oracle **fundiu** as duas trilhas. O par OCA **1Z0-815 + 1Z0-816** foi **consolidado no 1Z0-819** (em ago/2020), uma prova única que já cobria do básico ao avançado.
- **A linhagem moderna:** dali em diante a numeração seguiu reta — **1Z0-819 (Java 11) → 1Z0-829 (Java 17) → 1Z0-830 (Java 21) → 1Z0-831 (Java 25)**.

Conclusão prática: **hoje não existe pré-requisito OCA**. Se você encontrar material falando de "OCA", "Associate" ou de fazer "duas provas", é coisa da era Java 8 — ignore.

## Os 10 domínios são quase iguais

Esta é a notícia que dispensa ansiedade: **os objetivos das duas provas são os mesmos 10 domínios**, só com a redação levemente diferente. O Oracle reescreveu alguns títulos no 1Z0-831 (mais verbosos, mais "academicamente formais"), mas o assunto coberto é o mesmo. Compare:

| # | 1Z0-830 (Java 21) | 1Z0-831 (Java 25) |
| --- | --- | --- |
| 1 | Handling Date, Time, Text, Numeric and Boolean Values | Handling Date, Time, Text, Numeric and Boolean Values |
| 2 | Controlling Program Flow | Implementing Program Flow Control Using Decision and Looping Constructs |
| 3 | Using Object-Oriented Concepts in Java | Applying Object-Oriented Principles in Java Programs |
| 4 | Handling Exceptions | Implementing Exception Handling in Java Applications |
| 5 | Working with Arrays and Collections | Using Arrays and Collections to Store and Retrieve Data |
| 6 | Working with Streams and Lambda expressions | Processing Data Using Streams and Lambda Expressions |
| 7 | Packaging and Deploying Java Code | Packaging and Deploying Java Code |
| 8 | Managing Concurrent Code Execution | Implementing Multithreading for Concurrent Code Execution |
| 9 | Using Java I/O API | Performing Input and Output Operations Using the Java I/O API |
| 10 | Implementing Localization | Developing Applications with Localization Support |

Como os domínios são equivalentes, **o mapeamento de estudo é o mesmo pras duas provas**. O [[03-Dominios/Tecnologia/Java/Certificação OCP/04 - O mapa objetivo → galho — revisar a trilha pra prova|mapa objetivo → galho]] que liga cada domínio a uma trilha do grimório **serve tanto o 1Z0-830 quanto o 1Z0-831** — você não precisa de dois planos de estudo.

## Qual escolher

Não há resposta universal. Escolha pelo seu contexto:

- **Mire o 1Z0-830 (Java 21)** se você valoriza **material de estudo maduro**. É a prova com o **livro Sybex** (Boyarsky & Selikoff, ISBN-13 9781394286614, 2024) escrito sob medida, com os **mocks da Enthuware** já consolidados e revisados por milhares de candidatos. Pra quem quer o caminho mais batido e com menos surpresas, é a escolha segura.
- **Mire o 1Z0-831 (Java 25)** se você quer a **LTS mais recente** no currículo e **já absorveu os recursos do Java 25 pela trilha** — virtual threads, structured concurrency, scoped values, sequenced collections, gatherers. Como os domínios são os mesmos, a diferença real é estudar com material ainda menos consolidado (o livro Sybex pro 25 **ainda não existe**) em troca da versão mais nova.

> [!tip] Sem dogma
> As duas certificam praticamente o mesmo conhecimento. Se o que te trava é decidir, escolha o **21** pelo conforto do material; se já domina o Java 25 e quer a etiqueta mais nova, vá de **25**. Nenhuma das duas é "errada".

## Veja também

- [[03-Dominios/Tecnologia/Java/Certificação OCP/04 - O mapa objetivo → galho — revisar a trilha pra prova|O mapa objetivo → galho]]
- [[03-Dominios/Tecnologia/Java/Certificação OCP/03 - Formato, logística e mecânica da prova|Formato e logística]]
- [[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/15 - A evolução do Java (8 a 25)|A evolução do Java (Galho 1)]]
- [[03-Dominios/Tecnologia/Java/Certificação OCP/index|Certificação OCP (MOC do galho)]]

## Referências

- 1Z0-830 (Java SE 21 Developer Professional): https://education.oracle.com/java-se-21-developer-professional/pexam_1Z0-830
- 1Z0-831 (Java SE 25 Developer Professional): https://education.oracle.com/java-se-25-developer-professional/pexam_1Z0-831
- Enthuware — syllabus OCP Java 21: https://enthuware.com/oca-ocp-java-certification-resources/290-ocp-java-21-exam-syllabus
- Enthuware — syllabus OCP Java 25: https://enthuware.com/oca-ocp-java-certification-resources/297-ocp-java-25-exam-syllabus
