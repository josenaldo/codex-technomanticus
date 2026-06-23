---
title: "Engenharia"
type: moc
camada: Engenharia
publish: true
created: 2026-06-23
updated: 2026-06-23
status: seedling
tags:
  - moc
  - camada
  - engenharia
aliases:
  - Engenharia
  - Engenharia de Software
---
# Engenharia

> [!abstract] TL;DR
> Camada do *como construir e operar bem* — disciplinas neutras de stack. O que vale aqui
> independe de linguagem: como desenhar, comunicar, testar, proteger e operar sistemas. A
> teoria mora aqui; a implementação concreta vive nos domínios de [[03-Dominios/Tecnologia/index|Tecnologia]].

## Sobre esta camada

Engenharia é o andar entre a [[03-Dominios/Ciência/index|Ciência da Computação]] (o *porquê* atemporal)
e a [[03-Dominios/Tecnologia/index|Tecnologia]] (o *como em X*). São as disciplinas de craft que a
indústria construiu: arquitetura, design, testes, segurança, comunicação entre sistemas, dados e
operação. A regra de ouro: **a fundamentação fica aqui; cada tecnologia linka pra cá e cuida das suas
particularidades** (ex.: os princípios de RBAC ficam em [[03-Dominios/Engenharia/Segurança/index|Segurança]];
*como implementar RBAC no Spring* fica no galho de Spring).

## Domínios

- [[03-Dominios/Engenharia/Arquitetura/index|Arquitetura]] — forma macro do sistema: system design, distribuídos, modelagem
- [[03-Dominios/Engenharia/Complexidade de Software/index|Complexidade de Software]] — essencial vs. acidental, abstração, dívida técnica
- [[03-Dominios/Engenharia/Segurança/index|Segurança]] — princípios, autenticação, autorização, RBAC, OWASP
- [[03-Dominios/Engenharia/Testes/index|Testes]] — pirâmide de testes, TDD, mocking, cobertura
- [[03-Dominios/Engenharia/Design de Software/index|Design de Software]] — OO como craft, SOLID, design patterns, clean code
- [[03-Dominios/Engenharia/Comunicação entre Sistemas/index|Comunicação entre Sistemas]] — APIs, REST, GraphQL, gRPC, mensageria, contratos
- [[03-Dominios/Engenharia/Dados/index|Dados]] — engenharia de dados em escala: modelagem dimensional, warehousing, pipelines
- [[03-Dominios/Engenharia/Operação/index|Operação]] — operar em produção: SRE, SLO/SLI, deploy, observabilidade, incidentes

## Veja também

- [[03-Dominios/index|Domínios]] — todas as camadas
- [[03-Dominios/Ciência/index|Ciência da Computação]] — a base teórica abaixo
- [[03-Dominios/Tecnologia/index|Tecnologia]] — a implementação concreta acima
