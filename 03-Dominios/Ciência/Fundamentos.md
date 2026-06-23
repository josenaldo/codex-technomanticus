---
title: "Fundamentos"
type: moc
publish: true
---

# Fundamentos

Conceitos base de ciência da computação e engenharia de software.

## Estruturas de Dados e Algoritmos

- [[03-Dominios/Ciência/Algoritmos/index|Algoritmos]] — galho de 14 notas (complexidade, recorrências e algoritmos clássicos)
- [[03-Dominios/Ciência/Estruturas de Dados/index|Estruturas de Dados]] — galho de 13 notas (comparação Java/TS/Python/Go)

## Teoria da Computação

- [[03-Dominios/Ciência/Teoria da Computação/index|Teoria da Computação]] — galho de 17 notas (autômatos finitos/de pilha e linguagens formais, hierarquia de Chomsky, pumping lemmas, máquina de Turing e tese de Church-Turing, computabilidade — problema da parada, reduções, teorema de Rice — e complexidade formal — P, NP, NP-completude/Cook-Levin, P vs NP; dono do tratamento formal de P/NP que Algoritmos defere)

## Matemática para Computação

- [[03-Dominios/Ciência/Matemática para Computação/index|Matemática para Computação]] — galho de 22 notas (lógica proposicional e de predicados, técnicas de prova e indução matemática/estrutural, somatórios/logaritmos/crescimento, conjuntos/funções/relações, combinatória e princípios combinatórios, cardinalidade e diagonalização, teoria dos números e aritmética modular/RSA, grafos e árvores como objeto matemático, probabilidade/esperança e estruturas aleatorizadas; dona das ferramentas que Algoritmos e Teoria da Computação usam)

## Organização de Computadores

- [[03-Dominios/Ciência/Organização de Computadores/index|Organização de Computadores]] — galho de 19 notas (representação binária/IEEE 754/endianness, lógica digital, von Neumann e ciclo de instrução, ISA/assembly, pipeline e hazards, hierarquia de memória e cache, execução fora de ordem/branch prediction/especulação, multicore/coerência MESI, SIMD e GPU, I/O/interrupções/DMA, performance CPI/Amdahl; a máquina física por baixo do SO — mechanical sympathy)

## Banco de Dados

- [[03-Dominios/Ciência/Banco de Dados/index|Banco de Dados]] — galho de 16 notas (modelo relacional, SQL, transações, índices/EXPLAIN, performance, concorrência, distribuídos e NoSQL)

## Paradigmas

- [[03-Dominios/Ciência/Paradigmas/index|Paradigmas de Programação]] — galho de 16 notas (imperativo, OO e funcional como paradigmas, declarativo, lógico, reativo, imutabilidade, sistemas de tipos, multi-paradigma)
- [[03-Dominios/Engenharia/Orientação a Objetos/index|Orientação a Objetos]] — galho de 13 notas (pilares, composição, modelagem rica, divergência cross-language)
- [[03-Dominios/Engenharia/SOLID/index|SOLID]] — galho de 8 notas (os cinco princípios + DI/IoC + crítica)

## Concorrência

- [[03-Dominios/Ciência/Concorrência e Paralelismo/index|Concorrência e Paralelismo]] — galho de 18 notas (race conditions, atomicidade/visibilidade/ordenação, locks/semáforos, deadlock, lock-free, STM, os 5 modelos — memória compartilhada/CSP/atores/event loop/dados —, leis de escala e padrões; stack-agnóstico, linka Java)
- [[03-Dominios/Ciência/Sistemas Operacionais/index|Sistemas Operacionais]] — galho de 14 notas (kernel/user, system calls, processos/threads, escalonamento, memória virtual/paginação, thrashing, IPC, I/O, sistemas de arquivos, journaling, virtualização/containers; teoria, linka Infraestrutura)

## Qualidade de Software

- [[03-Dominios/Engenharia/Testes/index|Testes]] — galho de 16 notas (pirâmide, tipos, test doubles, TDD, técnicas de caso/edge cases, flaky, coverage/mutation, CI/CD; stack-agnóstico, linka Java/JS)

## Redes e Infraestrutura

- [[03-Dominios/Ciência/Redes e Protocolos/index|Redes e Protocolos]] — galho de 15 notas (camadas, TCP/UDP/DNS/TLS, HTTP e sua evolução, caching, CORS, REST/GraphQL/gRPC, WebSocket/SSE, latência, load balancing/CDN, resiliência)

## Complexidade de Software

- [[03-Dominios/Engenharia/Complexidade de Software/index|Complexidade de Software]] — galho 12: complexidade essencial vs. acidental, abstração, dívidas (técnica/cognitiva/intenção), entropia e sistemas

## Segurança

- [[03-Dominios/Engenharia/Segurança/index|Segurança Conceitual]] — galho de 22 notas (CIA/AAA e modelo adversarial, modelagem de ameaças/STRIDE, economia e fator humano, princípios de Saltzer & Schroeder/Kerckhoffs, aleatoriedade/CSPRNG, hashing e password hashing, criptografia simétrica/assimétrica/troca de chaves/MAC-assinaturas/PKI, autenticação/MFA/passkeys, autorização DAC-MAC-RBAC-ABAC/OAuth2-OIDC, cripto em trânsito/repouso, ataques a sistemas cripto/side channels, classes de vulnerabilidade/OWASP, Trusting Trust e supply chain, gestão de chaves/KMS-HSM, zero trust, privacidade × segurança e criptografia pós-quântica; confiança sob adversário — não appsec aplicado)

## Compiladores e Linguagens

- [[03-Dominios/Ciência/Compiladores e Linguagens/index|Compiladores e Linguagens]] — galho de 20 notas (o pipeline de tradução front/middle/back-end e compilação×interpretação×JIT; análise léxica — scanner/tokens/maximal munch; parsing — gramáticas/AST, recursive descent/Pratt, LL FIRST-FOLLOW e LR/LALR; tabela de símbolos/escopo, análise semântica e checagem de tipos/inferência Hindley-Milner; IR e SSA, otimização — dataflow/constant folding/DCE/inlining; geração de código/seleção de instruções, alocação de registradores/graph coloring; runtime/stack frames, garbage collection, JIT a fundo/deoptimization; capstone, linking/loading e bootstrapping/self-hosting/ataque de Thompson; a engenharia da tradução — linka Teoria da Computação para autômatos/gramáticas, Org para ISA/assembly, Segurança para Trusting Trust)

---

```dataview
LIST
FROM "Fundamentos"
WHERE type != "moc"
SORT file.name ASC
```
