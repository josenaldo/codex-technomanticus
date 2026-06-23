---
title: "Comunicação entre Sistemas"
type: moc
publish: true
created: 2026-06-23
updated: 2026-06-23
status: growing
tags:
  - moc
  - comunicacao-entre-sistemas
aliases:
  - Comunicação entre Sistemas
  - Comunicação entre sistemas
---
# Comunicação entre Sistemas

> [!abstract] TL;DR
> A camada de aplicação acima do fio — como sistemas conversam: APIs (REST, GraphQL, gRPC),
> mensageria assíncrona, contratos, idempotência e versionamento. A fundamentação fica aqui;
> *como implementar REST no Spring* ou *consumir API no React* vive nos domínios de tecnologia.

## Sobre este domínio

Sobre o transporte (TCP/HTTP/DNS, que vive em [[03-Dominios/Ciência/Redes e Protocolos/index|Redes e Protocolos]])
mora a camada de *contrato*: como desenhar uma API, escolher entre síncrono e assíncrono, versionar sem
quebrar consumidores, garantir entrega e idempotência. Disciplina neutra de stack — cada tecnologia
implementa e linka pra cá.

## Conteúdo

- [[03-Dominios/Engenharia/Comunicação entre Sistemas/API Design|API Design]] — desenho de APIs: REST/RESTful, recursos, versionamento, contratos
- [[03-Dominios/Engenharia/Comunicação entre Sistemas/Mensageria/index|Mensageria]] — comunicação assíncrona, filas, eventos, padrões de integração

## Veja também

- [[03-Dominios/Engenharia/index|Engenharia]] — a camada
- [[03-Dominios/Ciência/Redes e Protocolos/index|Redes e Protocolos]] — o transporte (o fio) abaixo
- [[03-Dominios/Engenharia/Arquitetura/index|Arquitetura]] — a forma do sistema que se comunica
