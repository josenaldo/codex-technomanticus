---
title: "Certificação Java OCP"
created: 2026-06-13
updated: 2026-06-13
type: moc
status: growing
publish: true
tags:
  - java
  - certificacao-ocp
  - moc
aliases:
  - "Certificação OCP"
  - "Galho 18 - Certificação OCP"
  - "OCP Java SE"
  - "1Z0-830"
  - "1Z0-831"
---

# Certificação Java OCP

> [!abstract] TL;DR
> Galho atípico: não re-ensina a linguagem, é o guia das provas OCP mapeado aos galhos 1-4 (e ao 6). Cobre as duas provas vigentes — Java 21 (1Z0-830) e Java 25 (1Z0-831, esta lançada em 01/mai/2026) — com os 10 domínios oficiais, as pegadinhas clássicas, formato e estratégia.
> São 17 notas em 3 grupos de certificação: sobre a prova, os domínios do exame, e pegadinhas/estratégia/dia da prova.
> É o último galho — fecha a trilha de 18.

## Sobre este galho

Este galho é deliberadamente atípico. Os outros 17 são trilhas conceituais: ensinam mecânica de linguagem, JVM, concorrência, Spring, sistemas distribuídos. Este não. Ele é um **guia de prova**. Seu valor não está em explicar o que é um `Stream` ou como funciona o `var` — isso a trilha já fez — mas no **ângulo de certificação**: o que a Oracle de fato cobra, como as questões mentem (alternativas que compilam mas não fazem o que parecem, código que parece correto e lança exceção em runtime), e onde o desenvolvedor senior tropeça justamente por excesso de confiança. Quem programa Java há anos costuma reprovar não por ignorância, mas por não conhecer as regras exatas do jogo: precedência de operadores em casos-limite, autoboxing escondido, ordem de inicialização, comportamento de `finally` com `return`.

A **fronteira-assinatura** deste galho é que ele **linka, não re-explica**. A mecânica da linguagem mora em outro lugar e é de lá que se estuda; aqui fica só o recorte de prova. Concretamente: o [[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/index|Galho 1]] cobre linguagem e sintaxe; o [[03-Dominios/Tecnologia/Java/Collections e Streams/index|Galho 2]] cobre collections, streams, `java.time` e I/O com NIO; o [[03-Dominios/Tecnologia/Java/JVM/index|Galho 3]] cobre a JVM e o sistema de módulos (JPMS); o [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Galho 4]] cobre concorrência; e o Galho 6 cobre `jlink`/`jpackage`. Cada domínio do exame aqui aponta de volta para essas notas. Não duplique conteúdo — siga o link.

## Sobre a prova

- [[03-Dominios/Tecnologia/Java/Certificação OCP/01 - A certificação OCP — o que é, por que (e por que não) fazer|A certificação OCP — o que é, por que (e por que não) fazer]] — o valor real e as críticas honestas; OCA acabou.
- [[03-Dominios/Tecnologia/Java/Certificação OCP/02 - Qual prova mirar — Java 21 (1Z0-830) vs Java 25 (1Z0-831)|Qual prova mirar — Java 21 (1Z0-830) vs Java 25 (1Z0-831)]] — as duas provas vigentes e como escolher.
- [[03-Dominios/Tecnologia/Java/Certificação OCP/03 - Formato, logística e mecânica da prova|Formato, logística e mecânica da prova]] — 50 questões, ~68%, online proctored, as características traiçoeiras.
- [[03-Dominios/Tecnologia/Java/Certificação OCP/04 - O mapa objetivo → galho — revisar a trilha pra prova|O mapa objetivo → galho — revisar a trilha pra prova]] — a nota-coração: cada domínio do exame mapeado às notas exatas dos galhos.

## Os domínios do exame

- [[03-Dominios/Tecnologia/Java/Certificação OCP/05 - Domínio 1 — Datas, texto, números e booleanos|Domínio 1 — Datas, texto, números e booleanos]]
- [[03-Dominios/Tecnologia/Java/Certificação OCP/06 - Domínio 2 — Controle de fluxo|Domínio 2 — Controle de fluxo]]
- [[03-Dominios/Tecnologia/Java/Certificação OCP/07 - Domínio 3 — Orientação a objetos|Domínio 3 — Orientação a objetos]]
- [[03-Dominios/Tecnologia/Java/Certificação OCP/08 - Domínio 4 — Exceções|Domínio 4 — Exceções]]
- [[03-Dominios/Tecnologia/Java/Certificação OCP/09 - Domínio 5 — Arrays e coleções|Domínio 5 — Arrays e coleções]]
- [[03-Dominios/Tecnologia/Java/Certificação OCP/10 - Domínio 6 — Streams e lambdas|Domínio 6 — Streams e lambdas]]
- [[03-Dominios/Tecnologia/Java/Certificação OCP/11 - Domínio 7 — Empacotamento, deployment e módulos|Domínio 7 — Empacotamento, deployment e módulos]] *(cobertura parcial)*
- [[03-Dominios/Tecnologia/Java/Certificação OCP/12 - Domínio 8 — Concorrência|Domínio 8 — Concorrência]]
- [[03-Dominios/Tecnologia/Java/Certificação OCP/13 - Domínio 9 — I-O|Domínio 9 — I/O]] *(cobertura parcial)*
- [[03-Dominios/Tecnologia/Java/Certificação OCP/14 - Domínio 10 — Localização|Domínio 10 — Localização]] *(cobertura parcial)*

## Pegadinhas, estratégia e dia da prova

- [[03-Dominios/Tecnologia/Java/Certificação OCP/15 - O catálogo de pegadinhas clássicas|O catálogo de pegadinhas clássicas]] — Integer cache, String pool, try/finally, static hiding, type erasure e companhia.
- [[03-Dominios/Tecnologia/Java/Certificação OCP/16 - Estratégia de estudo e recursos|Estratégia de estudo e recursos]] — plano, livro Sybex, Enthuware, caderno de erros.
- [[03-Dominios/Tecnologia/Java/Certificação OCP/17 - O dia da prova e depois|O dia da prova e depois]] — gestão de tempo, mentalidade, após passar ou reprovar.

## Rotas alternativas

- **Completa**: 01 → 02 → 03 → 04 → 05 → … → 17, em ordem.
- **Reta-final (pré-prova)**: 04 (mapa) → 15 (pegadinhas) → 03 (formato) → 17 (dia da prova).
- **Só-pegadinhas**: 15 → domínios com mais armadilhas (07, 10, 12).
- **Por-domínio**: 04 (mapa) → identifique o domínio fraco → nota do domínio → galho mapeado.
- **Decidir a prova**: 01 → 02 → 03.

## Veja também

- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/index|Linguagem e sintaxe moderna (Galho 1)]]
- [[03-Dominios/Tecnologia/Java/Collections e Streams/index|Collections e Streams (Galho 2)]]
- [[03-Dominios/Tecnologia/Java/JVM/index|JVM (Galho 3)]]
- [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Concorrência e paralelismo (Galho 4)]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java|Dicionário de Java]]
- [[03-Dominios/Tecnologia/Java/Core/Certificação Java OCP|Certificação OCP (tronco legado)]]

## Notas do galho

```dataview
TABLE fase, status
FROM "03-Dominios/Tecnologia/Java/Certificação OCP"
WHERE type = "concept"
SORT file.name ASC
```
