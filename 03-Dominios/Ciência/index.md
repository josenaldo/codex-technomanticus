---
title: "Ciência da Computação"
type: moc
publish: true
created: 2026-05-21
updated: 2026-06-23
status: seedling
tags:
  - moc
  - ciencia-da-computacao
camada: Ciência
aliases:
  - Ciência da Computação
  - Fundamentos
  - Fundamentos de CC
  - Fundamentos de Ciência da Computação
---
# Ciência da Computação

> [!abstract] TL;DR
> A camada do **porquê** — a ciência atemporal que sustenta qualquer prática de desenvolvimento: o conhecimento que sobrevive à troca de linguagem, framework ou paradigma. Algoritmos, estruturas de dados, teoria da computação, matemática, a máquina física, linguagens, banco de dados e redes.

Esta camada reúne os fundamentos científicos da computação — o terreno comum que conecta todas as outras estantes técnicas. Onde a [[03-Dominios/Engenharia/index|Engenharia]] pergunta *como construir e operar bem* e a [[03-Dominios/Tecnologia/index|Tecnologia]] pergunta *como fazer em X*, a Ciência da Computação pergunta *por que funciona*. É o andar mais estável do grimório: o que se aprende aqui não envelhece com a próxima versão do framework.

## Algoritmos e Estruturas de Dados

- [[03-Dominios/Ciência/Algoritmos/index|Algoritmos]] — galho: análise de complexidade (Big-O, recorrências, Teorema Mestre) e algoritmos clássicos (ordenação, busca, two pointers, divisão e conquista, DP, greedy, backtracking)
- [[03-Dominios/Ciência/Estruturas de Dados/index|Estruturas de Dados]] — galho: arrays, listas, hash, árvores, heaps, tries, grafos e especializadas, com comparação de implementação Java/TS/Python/Go

## Teoria e Matemática

- [[03-Dominios/Ciência/Teoria da Computação/index|Teoria da Computação]] — galho: o que pode ser computado e a que custo — a torre de poder (autômatos finitos, de pilha, máquina de Turing), linguagens formais e hierarquia de Chomsky, computabilidade (problema da parada, reduções, teorema de Rice) e complexidade formal (P, NP, NP-completude, P vs NP). Dono do tratamento formal de P/NP que Algoritmos defere
- [[03-Dominios/Ciência/Matemática para Computação/index|Matemática para Computação]] — galho: matemática discreta como ferramenta (lógica proposicional e de predicados, técnicas de prova e indução matemática/estrutural, somatórios/logaritmos/crescimento, conjuntos/funções/relações, combinatória, cardinalidade e diagonalização, teoria dos números e aritmética modular, grafos e árvores como objeto matemático, probabilidade e estruturas aleatorizadas). Dona das ferramentas que Algoritmos e Teoria da Computação usam

## A máquina por baixo

- [[03-Dominios/Ciência/Organização de Computadores/index|Organização de Computadores]] — galho: a máquina física por baixo do SO — representação binária/IEEE 754/endianness, lógica digital, von Neumann e o ciclo de instrução, ISA/assembly, pipeline, hierarquia de memória e cache, execução fora de ordem/especulação, multicore/coerência (MESI), SIMD/GPU, I/O/DMA e a equação de performance (CPI/Amdahl). Mechanical sympathy: por que `int` estoura, por que floats enganam, por que cache manda na performance
- [[03-Dominios/Ciência/Sistemas Operacionais/index|Sistemas Operacionais]] — galho: a teoria do SO (kernel × user, system calls, processos e threads, escalonamento, memória virtual e paginação, thrashing, IPC, I/O, sistemas de arquivos, journaling, virtualização e containers) — conceitual, linka Infraestrutura para o uso
- [[03-Dominios/Ciência/Concorrência e Paralelismo/index|Concorrência e Paralelismo]] — galho: os perigos universais (race conditions, deadlock, atomicidade/visibilidade/ordenação), primitivas (locks, semáforos, atômicos, STM) e os cinco modelos de concorrência (memória compartilhada, CSP, atores, event loop, dados), com leis de escala e padrões — stack-agnóstico

## Linguagens

- [[03-Dominios/Ciência/Paradigmas/index|Paradigmas de Programação]] — galho: os modelos mentais de programar (imperativo, OO, funcional, declarativo, lógico, reativo), imutabilidade e efeitos, sistemas de tipos e linguagens multi-paradigma
- [[03-Dominios/Ciência/Compiladores e Linguagens/index|Compiladores e Linguagens]] — galho: a engenharia de traduzir código em algo que roda — o pipeline (front/middle/back-end), análise léxica (scanner, tokens), parsing (gramáticas, AST, recursive descent/Pratt, LL e LR), análise semântica e checagem de tipos (inferência Hindley-Milner), IR e SSA, otimização (dataflow, constant folding/DCE/inlining), geração de código e alocação de registradores, runtime (stack frames, garbage collection), JIT (tiered compilation, deoptimization), linking/loading e bootstrapping/Trusting Trust. A teoria (autômatos/gramáticas) vira a *construção* do tradutor — não tutorial de toolchain

## Dados e Redes

- [[03-Dominios/Ciência/Banco de Dados/index|Banco de Dados]] — galho: modelo relacional, SQL, normalização, transações (ACID), índices/EXPLAIN, performance, concorrência, distribuídos e NoSQL
- [[03-Dominios/Ciência/Redes e Protocolos/index|Redes e Protocolos]] — galho: modelo de camadas, TCP/UDP/DNS/TLS, HTTP (métodos, caching, CORS, HTTP/2-3), REST/GraphQL/gRPC, WebSocket/SSE, latência, load balancing/CDN e resiliência

## Referência

- [[Dicionário de Ciência da Computação]] — glossário de termos fundamentais

## Veja também

- [[03-Dominios/index|Domínios]] — índice das quatro camadas
- [[03-Dominios/Engenharia/index|Engenharia]] — onde a teoria daqui vira prática de construção: [[03-Dominios/Engenharia/Design de Software/Orientação a Objetos/index|Orientação a Objetos]] e [[03-Dominios/Engenharia/Design de Software/SOLID/index|SOLID]] (aplicam Paradigmas), [[03-Dominios/Engenharia/Testes/index|Testes]], [[03-Dominios/Engenharia/Segurança/index|Segurança Conceitual]] e [[03-Dominios/Engenharia/Complexidade de Software/index|Complexidade de Software]]
- [[04-Sendas/index|Sendas]] — trilhas que cruzam a ciência com as outras camadas
