---
title: "Fundamentos"
type: moc
publish: true
created: 2026-05-21
updated: 2026-06-07
status: seedling
tags:
  - moc
  - fundamentos
aliases:
  - Fundamentos de CC
  - Fundamentos de Ciência da Computação
---
# Fundamentos

> [!abstract] TL;DR
> Base teórica de ciência da computação, independente de linguagem ou stack: algoritmos, estruturas de dados, OO, banco de dados, redes e testes.

Esta estante reúne os fundamentos que sustentam qualquer prática de desenvolvimento — o conhecimento que sobrevive à troca de linguagem, framework ou paradigma. Aqui ficam as notas sobre **algoritmos** e suas análises de complexidade, **estruturas de dados** clássicas, princípios de **orientação a objetos**, modelagem e teoria de **banco de dados**, **redes e protocolos** que sustentam a comunicação entre sistemas, e práticas de **testes** automatizados. É o terreno comum que conecta todas as outras estantes técnicas.

## Conteúdo

- [[Fundamentos]] — visão geral da área
- [[03-Dominios/Fundamentos/Algoritmos/index|Algoritmos]] — galho: análise de complexidade (Big-O, recorrências, Teorema Mestre) e algoritmos clássicos (ordenação, busca, two pointers, divisão e conquista, DP, greedy, backtracking)
- [[03-Dominios/Fundamentos/Estruturas de Dados/index|Estruturas de Dados]] — galho: arrays, listas, hash, árvores, heaps, tries, grafos e especializadas, com comparação de implementação Java/TS/Python/Go
- [[03-Dominios/Fundamentos/Orientação a Objetos/index|Orientação a Objetos]] — galho: pilares (encapsulamento, abstração, herança, polimorfismo), interfaces, composição sobre herança, acoplamento/coesão, modelagem rica e como o modelo OO diverge entre linguagens
- [[03-Dominios/Fundamentos/SOLID/index|SOLID]] — galho: os cinco princípios de design OO (SRP, OCP, LSP, ISP, DIP), DI/IoC e a leitura crítica
- [[03-Dominios/Fundamentos/Paradigmas/index|Paradigmas de Programação]] — galho: os modelos mentais de programar (imperativo, OO, funcional, declarativo, lógico, reativo), imutabilidade e efeitos, sistemas de tipos e linguagens multi-paradigma
- [[03-Dominios/Fundamentos/Concorrência e Paralelismo/index|Concorrência e Paralelismo]] — galho: os perigos universais (race conditions, deadlock, atomicidade/visibilidade/ordenação), primitivas (locks, semáforos, atômicos, STM) e os cinco modelos de concorrência (memória compartilhada, CSP, atores, event loop, dados), com leis de escala e padrões — stack-agnóstico
- [[03-Dominios/Fundamentos/Sistemas Operacionais/index|Sistemas Operacionais]] — galho: a teoria do SO (kernel × user, system calls, processos e threads, escalonamento, memória virtual e paginação, thrashing, IPC, I/O, sistemas de arquivos, journaling, virtualização e containers) — conceitual, linka Infraestrutura para o uso
- [[03-Dominios/Fundamentos/Teoria da Computação/index|Teoria da Computação]] — galho: o que pode ser computado e a que custo — a torre de poder (autômatos finitos, de pilha, máquina de Turing), linguagens formais e hierarquia de Chomsky, computabilidade (problema da parada, reduções, teorema de Rice) e complexidade formal (P, NP, NP-completude, P vs NP). Dono do tratamento formal de P/NP que Algoritmos defere
- [[03-Dominios/Fundamentos/Matemática para Computação/index|Matemática para Computação]] — galho: matemática discreta como ferramenta (lógica proposicional e de predicados, técnicas de prova e indução matemática/estrutural, somatórios/logaritmos/crescimento, conjuntos/funções/relações, combinatória, cardinalidade e diagonalização, teoria dos números e aritmética modular, grafos e árvores como objeto matemático, probabilidade e estruturas aleatorizadas). Dona das ferramentas que Algoritmos (logaritmos/somatórios/recorrências) e Teoria da Computação (diagonalização) usam
- [[03-Dominios/Fundamentos/Banco de Dados/index|Banco de Dados]] — galho: modelo relacional, SQL, normalização, transações (ACID), índices/EXPLAIN, performance, concorrência, distribuídos e NoSQL
- [[03-Dominios/Fundamentos/Redes e Protocolos/index|Redes e Protocolos]] — galho: modelo de camadas, TCP/UDP/DNS/TLS, HTTP (métodos, caching, CORS, HTTP/2-3), REST/GraphQL/gRPC, WebSocket/SSE, latência, load balancing/CDN e resiliência
- [[03-Dominios/Fundamentos/Testes/index|Testes]] — galho: estratégia de testes, pirâmide, tipos, test doubles, TDD, técnicas de caso/edge cases, flaky, coverage/mutation e CI/CD (stack-agnóstico)
- [[03-Dominios/Fundamentos/Complexidade de Software/index|Complexidade de Software]] — galho: o que torna software difícil e como gerenciá-lo (essencial vs. acidental, abstração, as três dívidas, sistemas). Inclui [[04 - O programa como teoria|O programa como teoria]] (Naur) e [[06 - Abstrações que vazam|Abstrações que vazam]] (Spolsky)
- [[Dicionário de Fundamentos]] — glossário de termos fundamentais

## Veja também

- [[03-Dominios/index|Domínios]] — índice das estantes
- [[03-Dominios/Arquitetura/index|Arquitetura]] — aplicação dos fundamentos em design de sistemas
- [[04-Sendas/index|Sendas]] — trilhas que cruzam fundamentos com outras áreas
