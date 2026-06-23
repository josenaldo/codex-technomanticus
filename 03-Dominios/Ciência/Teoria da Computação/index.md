---
title: "Teoria da Computação"
created: 2026-06-19
updated: 2026-06-19
type: moc
status: growing
publish: true
tags:
  - ciencia-da-computacao
  - teoria-da-computacao
  - entrevista
  - moc
aliases:
  - Teoria da Computação
  - Computability
  - Theory of Computation
  - Galho - Teoria da Computação
---

# Teoria da Computação

> [!abstract] TL;DR
> Galho de Ciência da Computação sobre as duas perguntas que nenhum framework responde: **o que pode ser computado** e
> **a que custo**. Sobe a "torre de poder" dos modelos de computação — autômato finito → autômato de pilha →
> máquina de Turing — e, no topo, esbarra nos dois muros: o que **nenhuma** máquina computa (indecidibilidade:
> o problema da parada, Rice) e o que máquina nenhuma computa **barato** (complexidade: P, NP, NP-completo,
> P vs NP). Teoria pura, mas com resgate prático em cada limite: é *por isso* que regex não parseia HTML, que
> linter não pega todo loop infinito, e que você para de caçar o ótimo e aproxima.

## Sobre este galho
Este é o andar mais **teórico** da Ciência da Computação — e o mais antigo da Ciência da Computação (Turing, Church e
Gödel, anos 1930, antes de existir computador). Ele dá o vocabulário formal para falar de *limites*: o que a
computação **não** pode fazer, e o que ela só faz a um custo proibitivo.

**Fronteiras (linka, não duplica):**
- **A face prática de P/NP** (NP-difícil como sinal, aproximação, heurística) → [[03-Dominios/Ciência/Algoritmos/13 - Intratabilidade|Intratabilidade]]. Aqui mora o **formal** (Cook-Levin, redução polinomial, P vs NP).
- **Parsing e lexer na prática** → futuro galho de Compiladores e Linguagens. Aqui é a teoria das **linguagens formais** e dos autômatos.
- **Lógica, provas, conjuntos, combinatória** → futuro galho de Matemática para Computação. Aqui se **usa** prova e diagonalização; não se ensina.
- **Complexidade de Software** ([[Complexidade de Software]]) é complexidade **cognitiva/de manutenção** — coisa OUTRA, não confundir com complexidade computacional.
- **λ-cálculo pelo ângulo de estilo** → [[03-Dominios/Ciência/Paradigmas/index|Paradigmas de Programação]] (a nota da tese de Church-Turing linka de volta).

**Audiência:** dev senior em preparação para entrevista internacional. Cada nota tem seção "Em entrevista" com
frases prontas em inglês e vocabulário técnico PT→EN. (O tema cai *raramente* em entrevista, mas é fundamento real.)

## Iniciado — o mundo regular (máquinas sem memória de verdade)
1. [[01 - O que é computação]] — modelo de computação; decidir × reconhecer; a torre de poder; as duas grandes perguntas.
2. [[02 - Linguagens formais e a hierarquia de Chomsky]] — alfabeto/palavra/linguagem; gramática; Chomsky tipo 3→0 como mapa-mestre.
3. [[03 - Autômatos finitos - DFA e NFA]] — estados/transições; NFA↔DFA (subset construction); a máquina sem memória.
4. [[04 - Linguagens regulares e expressões regulares]] — Kleene (regex↔AF↔gramática); fechamento; por que regex não parseia HTML.
5. [[05 - O pumping lemma para linguagens regulares]] — a ferramenta de provar não-regularidade; aⁿbⁿ; o jogo adversarial.

## Adepto — máquinas mais fortes e a máquina universal
6. [[06 - Autômatos de pilha e gramáticas livres de contexto]] — a memória de pilha; GLC, parse trees, ambiguidade.
7. [[07 - O pumping lemma para livres de contexto]] — aⁿbⁿcⁿ não é LC; fechamento; por que linguagens reais escapam da gramática.
8. [[08 - A máquina de Turing]] — fita, cabeça, estados; robustez; aceitar × decidir × computar função.
9. [[09 - A tese de Church-Turing]] — λ-cálculo/recursivas/MT convergem; Turing-completude.
10. [[10 - Decidível, reconhecível e a máquina universal]] — recursiva × r.e. × co-r.e.; UTM; diagonalização de Cantor.

## Magus — os muros: o incomputável e o caro
11. [[11 - O problema da parada]] — o enunciado; a prova por auto-referência; por que linter nenhum pega todo loop infinito.
12. [[12 - Reduções e indecidibilidade em cascata]] — redução de mapeamento; provar indecidível reduzindo da parada.
13. [[13 - O teorema de Rice]] — toda propriedade não-trivial de comportamento é indecidível; por que análise estática perfeita não existe.
14. [[14 - Complexidade computacional formal - classes de tempo, P e NP]] — MT com relógio; P e NP; certificado; o formal que Algoritmos/13 deferiu.
15. [[15 - NP-completude - Cook-Levin e a cadeia de Karp]] — redução polinomial; SAT é NP-completo; reconhecer NP-completo.
16. [[16 - P vs NP e o mapa das classes]] — a pergunta do milênio; PSPACE/EXPTIME; o mapa das classes.
17. [[17 - A teoria da computação na vida do dev]] — cada limite → consequência prática; inglês; vocabulário; armadilhas.

## Rotas alternativas

### O essencial (a torre em 6 paradas)
01 → 03 → 06 → 08 → 11 → 14. Modelo, autômato finito, pilha, Turing, o muro do incomputável, o muro do caro.

### Computabilidade a fundo (os limites)
08 → 10 → 11 → 12 → 13. Da máquina de Turing à parada, às reduções e a Rice.

### Complexidade a fundo (P vs NP)
14 → 15 → 16 + [[03-Dominios/Ciência/Algoritmos/13 - Intratabilidade|a face prática em Algoritmos]].

### O resgate prático (por que isso importa pro dev)
04 → 11 → 13 → 15 → 17. Regex, halting, Rice, NP-completo e o capstone.

## Todas as notas

```dataview
TABLE fase, status, updated
FROM "03-Dominios/Ciência/Teoria da Computação"
WHERE type = "concept"
SORT file.name ASC
```

## Veja também

- [[03-Dominios/Ciência/index|Fundamentos (MOC do domínio)]]
- [[03-Dominios/Ciência/Algoritmos/13 - Intratabilidade|Intratabilidade]] — a face prática de P/NP (NP-difícil, aproximação, heurística)
- [[03-Dominios/Ciência/Paradigmas/index|Paradigmas de Programação]] — funcional e λ-cálculo pelo ângulo de estilo
- [[Dicionário de Ciência da Computação]]
