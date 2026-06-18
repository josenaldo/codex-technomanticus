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

## Banco de Dados

- [[03-Dominios/Fundamentos/Banco de Dados/index|Banco de Dados]] — galho de 16 notas (modelo relacional, SQL, transações, índices/EXPLAIN, performance, concorrência, distribuídos e NoSQL)

## Paradigmas

- [[03-Dominios/Fundamentos/Paradigmas/index|Paradigmas de Programação]] — galho de 16 notas (imperativo, OO e funcional como paradigmas, declarativo, lógico, reativo, imutabilidade, sistemas de tipos, multi-paradigma)
- [[03-Dominios/Fundamentos/Orientação a Objetos/index|Orientação a Objetos]] — galho de 13 notas (pilares, composição, modelagem rica, divergência cross-language)
- [[03-Dominios/Fundamentos/SOLID/index|SOLID]] — galho de 8 notas (os cinco princípios + DI/IoC + crítica)

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
