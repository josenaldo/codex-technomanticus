---
title: "Arquitetura de Eventos"
created: 2026-07-31
updated: 2026-07-31
type: moc
status: evergreen
publish: true
tags:
  - moc
  - design-de-software
  - arquitetura-de-eventos
  - eda
  - acoplamento
aliases:
  - Arquitetura de Eventos
  - Event-Driven Architecture
  - EDA
  - Galho - Arquitetura de Eventos
---

# Arquitetura de Eventos

> [!abstract] TL;DR
> Os padrões que aparecem quando um sistema comunica por **fatos ocorridos** em vez de comandos diretos.
> Quinta família do galho-pai
> [[03-Dominios/Engenharia/Design de Software/Padrões de Projeto/index|Padrões de Projeto]]. "Event-driven"
> não nomeia uma coisa: nomeia os **quatro estilos** que Fowler separou — Event Notification,
> Event-Carried State Transfer, Event Sourcing e CQRS —, e duas equipes podem usar o termo descrevendo
> sistemas com propriedades opostas. A lente aqui é uma pergunta só: **o que o evento carrega, e a quem
> isso amarra**.

## Sobre esta família

Catálogo de consulta, com notas autocontidas e **Armadilhas** pesando no *quando não usar*.

**Esta é a família com maior sobreposição do galho, e a lente existe por causa disso.** Event Sourcing,
CQRS, Saga, Outbox e pub-sub já têm casa profunda no vault; esta família não os repete — olha-os pelo
eixo do **acoplamento**, que aquelas notas não cobrem. A divisão de trabalho, reafirmada em cada nota:

| Galho | Pergunta que responde |
| --- | --- |
| [[03-Dominios/Engenharia/Arquitetura/System Design/3 - Padrões recorrentes/index\|System Design]] | *quanto aguenta?* — throughput, snapshots, projeções em escala |
| [[03-Dominios/Engenharia/Comunicação entre Sistemas/4 - Comunicação assíncrona/index\|Comunicação assíncrona]] | *como chega?* — broker, entrega, ordenação, CDC, dual-write |
| **Esta família** | ***o que acopla?*** — o que o evento carrega, quem depende de quem |

**Eixo dorsal:** [[03 - Event Notification]] × [[04 - Event-Carried State Transfer]] — o evento magro
contra o gordo. É a decisão mais consequente da família, e ela é **por fluxo**, não por sistema.

## Iniciado — o que é um evento, e o estilo mais magro

1. [[01 - Panorama da arquitetura de eventos]] — os quatro estilos como mapa; evento × comando × documento; a inversão de controle e o preço dela.
2. [[02 - Domain Events]] — o evento como elemento do modelo, e a fronteira entre evento de domínio e de integração.
3. [[03 - Event Notification]] — o evento magro: desacopla dados, acopla disponibilidade.

## Adepto — o que ele carrega, e como coordenar

4. [[04 - Event-Carried State Transfer]] — o evento gordo: autonomia comprada com réplica local e contrato de payload.
5. [[05 - Outbox]] — o *dual-write problem*; garante at-least-once, nunca *exactly-once*.
6. [[06 - Idempotent Consumer (Inbox)]] — processar duas vezes com efeito de uma, inclusive onde não há rollback.
7. [[07 - Saga]] — a transação distribuída que não existe; coreografia × orquestração, e o limite da compensação.

## Magus — os estilos que reorganizam o sistema

8. [[08 - Process Manager]] — o coordenador stateful e durável; quem responde "em que etapa está?".
9. [[09 - Event Sourcing]] — o log como fonte da verdade, e o esquema de eventos como contrato com o futuro.
10. [[10 - CQRS]] — dois modelos para os mesmos dados; **fecha a família** com o mapa de escolha dos 10 padrões e a síntese do espectro de acoplamento.

> [!tip] Atalho para quem tem um problema concreto
> A nota [[10 - CQRS]] termina com um **mapa de escolha** que parte do sintoma — "gravei no banco e o
> evento não saiu", "o cliente foi cobrado duas vezes", "ninguém sabe em que etapa o processo está" —
> e leva ao padrão e à nota. É o índice mais útil da família em campo.

## Todas as notas

```dataview
TABLE fase, status, updated
FROM "03-Dominios/Engenharia/Design de Software/Padrões de Projeto/Arquitetura de Eventos"
WHERE type = "concept"
SORT file.name ASC
```

## Veja também

- [[03-Dominios/Engenharia/Design de Software/Padrões de Projeto/index|Padrões de Projeto]] — o galho-pai e as seis famílias.
- [[03-Dominios/Engenharia/Design de Software/Padrões de Projeto/Integração Empresarial (EIP)/index|Integração Empresarial (EIP)]] — o vocabulário de canais e roteamento por baixo destes padrões.
- [[03-Dominios/Engenharia/Design de Software/Padrões de Projeto/Aplicação Corporativa/index|Aplicação Corporativa]] — a família anterior; o Process Manager é o Application Controller distribuído.
- [[03-Dominios/Engenharia/Comunicação entre Sistemas/index|Comunicação entre Sistemas]] — a infraestrutura de mensageria.
