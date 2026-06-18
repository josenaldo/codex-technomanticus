---
title: "Paradigmas de Programação"
created: 2026-06-18
updated: 2026-06-18
type: moc
status: growing
publish: true
tags:
  - fundamentos
  - paradigmas
  - funcional
  - entrevista
  - moc
aliases:
  - Paradigmas
  - Paradigmas de Programação
  - Paradigmas de programação
  - Programming Paradigms
  - Galho - Paradigmas
---

# Paradigmas de Programação

> [!abstract] TL;DR
> Galho de Fundamentos sobre os **modelos mentais** de programar — imperativo, orientado a objetos,
> declarativo, funcional, lógico, reativo. Um paradigma não é uma linguagem: é um jeito de *pensar* o
> problema, e as linguagens modernas misturam vários. O coração do galho é o **paradigma funcional**
> (pureza, imutabilidade, composição, tipos algébricos) — o estilo que mais saiu do nicho para o
> mainstream. A tese final: paradigma é ferramenta, não religião; o senior escolhe por problema.

## Sobre este galho

Este galho é **stack-agnóstico**: trata os paradigmas como conceitos, com exemplos mínimos em várias
linguagens e ponteiros para o ferramental concreto.

**Fronteiras (linka, não duplica):**
- **OO em profundidade** (os 4 pilares, composição, modelagem) → [[Orientação a Objetos]]. Aqui OO é
  tratado *como um paradigma entre vários*.
- **Programação reativa com Reactor/WebFlux** → [[Programação Reativa]] (estante Java). Aqui fica o conceito
  de paradigma reativo/dataflow.
- **Funcional na prática com ferramental** → [[03-Dominios/Java/Collections e Streams/index|Streams (Java)]] e [[TypeScript]].
- **Concorrência e paralelismo** (atores, CSP, memória compartilhada) → futuro galho da Camada B; aqui só
  mencionados em prosa, como benefício da imutabilidade.
- **Princípios de design** → [[SOLID]]; **raciocínio sobre complexidade/estado** → [[Complexidade de Software]].

**Audiência:** dev senior em preparação para entrevista internacional. Cada nota tem seção "Em entrevista"
com frases prontas em inglês e vocabulário técnico PT→EN. (O tema cai *parcialmente* em entrevista, mas é
fundamento real.)

## Iniciado — o mapa e os mundos base

1. [[01 - O que é um paradigma de programação]] — modelo mental, não linguagem; imperativo × declarativo; multi-paradigma.
2. [[02 - O paradigma imperativo]] — estado + comandos + controle de fluxo; von Neumann; procedural e estruturada.
3. [[03 - O paradigma orientado a objetos]] — OO como paradigma (estado + mensagens); linka o galho de OO.
4. [[04 - O paradigma declarativo]] — dizer O QUE, não COMO; o guarda-chuva (funcional, lógico, SQL, config).

## Adepto — o mergulho funcional

5. [[05 - O paradigma funcional]] — funções de primeira classe, HOF; por que FP virou mainstream.
6. [[06 - Composição e recursão]] — compor funções, point-free, recursão e fold como motor do loop.
7. [[07 - Funções puras e efeitos colaterais]] — pureza, transparência referencial, efeitos na borda.
8. [[08 - Imutabilidade e estado]] — dados imutáveis, structural sharing, persistent data structures.
9. [[09 - Avaliação preguiçosa, currying e aplicação parcial]] — lazy eval, thunks, currying.
10. [[10 - Tipos algébricos, pattern matching e erros sem exceção]] — ADTs, pattern matching, Option/Either, o "M-word".

## Magus — outros estilos, tipos e síntese

11. [[11 - O paradigma lógico]] — fatos, regras, unificação, backtracking (Prolog); onde aparece hoje.
12. [[12 - Programação reativa e dataflow]] — streams/observables, FRP, propagação de mudança; linka Java reativo.
13. [[13 - Sistemas de tipos]] — estático × dinâmico, inferência, forte/fraca, nominal/estrutural (eixo transversal).
14. [[14 - Linguagens multi-paradigma]] — linguagens misturam estilos; o paradigma é escolha por problema.
15. [[15 - Programação funcional na prática]] — map/filter/reduce, imutabilidade por padrão, adoção gradual.
16. [[16 - Paradigmas na prática e em entrevista]] — escolher por problema, comparar, inglês, vocabulário, armadilhas.

## Rotas alternativas

### O essencial em entrevista
01 → 05 → 07 → 08 → 14 → 16. O mapa, o funcional, pureza e imutabilidade, multi-paradigma e o capstone.

### Mergulho funcional
05 → 06 → 07 → 08 → 09 → 10 → 15. Toda a fase Adepto mais a prática.

### A divisão imperativo × declarativo
01 → 02 → 04 → 11 → 12. O mapa, o imperativo, o declarativo, o lógico e o reativo.

## Todas as notas

```dataview
TABLE fase, status, updated
FROM "03-Dominios/Fundamentos/Paradigmas"
WHERE type = "concept"
SORT file.name ASC
```

## Veja também

- [[03-Dominios/Fundamentos/index|Fundamentos (MOC do domínio)]]
- [[Orientação a Objetos]] — OO em profundidade (os pilares, composição, modelagem)
- [[Programação Reativa]] — o paradigma reativo com Reactor/WebFlux (estante Java)
- [[Complexidade de Software]] — simplicidade, estado e raciocínio sobre código
- [[Dicionário de Fundamentos]]
