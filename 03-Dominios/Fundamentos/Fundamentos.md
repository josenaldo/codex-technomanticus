---
title: "Fundamentos"
type: moc
publish: true
---

# Fundamentos

Conceitos base de ciência da computação e engenharia de software.

## Estruturas de Dados e Algoritmos

- [[03-Dominios/Fundamentos/Algoritmos/index|Algoritmos]] — galho de 14 notas (complexidade, recorrências e algoritmos clássicos)
- [[03-Dominios/Fundamentos/Estruturas de Dados/index|Estruturas de Dados]] — galho de 13 notas (comparação Java/TS/Python/Go)

## Teoria da Computação

- [[03-Dominios/Fundamentos/Teoria da Computação/index|Teoria da Computação]] — galho de 17 notas (autômatos finitos/de pilha e linguagens formais, hierarquia de Chomsky, pumping lemmas, máquina de Turing e tese de Church-Turing, computabilidade — problema da parada, reduções, teorema de Rice — e complexidade formal — P, NP, NP-completude/Cook-Levin, P vs NP; dono do tratamento formal de P/NP que Algoritmos defere)

## Matemática para Computação

- [[03-Dominios/Fundamentos/Matemática para Computação/index|Matemática para Computação]] — galho de 22 notas (lógica proposicional e de predicados, técnicas de prova e indução matemática/estrutural, somatórios/logaritmos/crescimento, conjuntos/funções/relações, combinatória e princípios combinatórios, cardinalidade e diagonalização, teoria dos números e aritmética modular/RSA, grafos e árvores como objeto matemático, probabilidade/esperança e estruturas aleatorizadas; dona das ferramentas que Algoritmos e Teoria da Computação usam)

## Banco de Dados

- [[03-Dominios/Fundamentos/Banco de Dados/index|Banco de Dados]] — galho de 16 notas (modelo relacional, SQL, transações, índices/EXPLAIN, performance, concorrência, distribuídos e NoSQL)

## Paradigmas

- [[03-Dominios/Fundamentos/Paradigmas/index|Paradigmas de Programação]] — galho de 16 notas (imperativo, OO e funcional como paradigmas, declarativo, lógico, reativo, imutabilidade, sistemas de tipos, multi-paradigma)
- [[03-Dominios/Fundamentos/Orientação a Objetos/index|Orientação a Objetos]] — galho de 13 notas (pilares, composição, modelagem rica, divergência cross-language)
- [[03-Dominios/Fundamentos/SOLID/index|SOLID]] — galho de 8 notas (os cinco princípios + DI/IoC + crítica)

## Concorrência

- [[03-Dominios/Fundamentos/Concorrência e Paralelismo/index|Concorrência e Paralelismo]] — galho de 18 notas (race conditions, atomicidade/visibilidade/ordenação, locks/semáforos, deadlock, lock-free, STM, os 5 modelos — memória compartilhada/CSP/atores/event loop/dados —, leis de escala e padrões; stack-agnóstico, linka Java)
- [[03-Dominios/Fundamentos/Sistemas Operacionais/index|Sistemas Operacionais]] — galho de 14 notas (kernel/user, system calls, processos/threads, escalonamento, memória virtual/paginação, thrashing, IPC, I/O, sistemas de arquivos, journaling, virtualização/containers; teoria, linka Infraestrutura)

## Qualidade de Software

- [[03-Dominios/Fundamentos/Testes/index|Testes]] — galho de 16 notas (pirâmide, tipos, test doubles, TDD, técnicas de caso/edge cases, flaky, coverage/mutation, CI/CD; stack-agnóstico, linka Java/JS)

## Redes e Infraestrutura

- [[03-Dominios/Fundamentos/Redes e Protocolos/index|Redes e Protocolos]] — galho de 15 notas (camadas, TCP/UDP/DNS/TLS, HTTP e sua evolução, caching, CORS, REST/GraphQL/gRPC, WebSocket/SSE, latência, load balancing/CDN, resiliência)

## Complexidade de Software

- [[03-Dominios/Fundamentos/Complexidade de Software/index|Complexidade de Software]] — galho 12: complexidade essencial vs. acidental, abstração, dívidas (técnica/cognitiva/intenção), entropia e sistemas

---

```dataview
LIST
FROM "Fundamentos"
WHERE type != "moc"
SORT file.name ASC
```
