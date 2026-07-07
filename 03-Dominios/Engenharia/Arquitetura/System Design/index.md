---
title: "System Design"
type: moc
publish: true
tags:
  - system-design
  - moc
created: 2026-07-06
updated: 2026-07-07
---

# System Design — trilha de entrevista sênior

A habilidade de **desenhar sistemas em escala no whiteboard**: conduzir os 45-60 min de uma entrevista de system design com estrutura, estimativas defensáveis e trade-offs explícitos. Trilha em 3 fases (Iniciado → Adepto → Magus), organizada em quatro sub-galhos + um capstone.

> [!info] Onde isto se encaixa
> Esta trilha é a **forma macro sob escala**. O ofício de arquitetura (estilos, DDD, SOLID, Conway) vive em [[Arquitetura de Software]]; a modelagem de domínio em [[Event Storming]]; os contratos entre sistemas em [[03-Dominios/Engenharia/Comunicação entre Sistemas/index|Comunicação entre Sistemas]]. Aqui, tópicos desses galhos reaparecem **sob a ótica de system design** — reforço com cross-link, não duplicação.

## Sub-galhos

### 1 · Framework de entrevista *(Iniciado)*
O processo antes do conteúdo: como não travar nos primeiros 10 minutos.
- [[1 - Framework de entrevista/index|Framework de entrevista]]

### 2 · Building blocks *(Adepto)*
O vocabulário de escala: load balancing, caching, sharding, filas, CAP, CDN.
- [[2 - Building blocks/index|Building blocks]]

### 3 · Padrões recorrentes *(Adepto)*
Pub/Sub, CQRS, Event Sourcing, Rate Limiting, Circuit Breaker, API Gateway — sob a ótica de escala.
- [[3 - Padrões recorrentes/index|Padrões recorrentes]]

### 4 · Walkthroughs *(Magus)*
Os oito designs clássicos ponta a ponta, cada um aplicando os blocos e padrões.
- [[4 - Walkthroughs/index|Walkthroughs]]

### ★ Capstone *(Magus)*
A performance que costura tudo: gestão de tempo, leitura de sinais, recuperação quando trava, e a pergunta de produção.
- [[Conduzindo a entrevista completa]]

## Como usar esta trilha

Leia na ordem 1 → 2 → 3 → 4 se está começando: o framework dá o roteiro, os building blocks o vocabulário, os padrões as combinações, e os walkthroughs mostram tudo em ação. Se já domina o básico, vá direto aos [[4 - Walkthroughs/index|walkthroughs]] e use os sub-galhos anteriores como referência. Feche com o [[Conduzindo a entrevista completa|capstone]] e depois **pratique em voz alta**, cronometrando.

## Recursos

### Livros
- *Designing Data-Intensive Applications* — Martin Kleppmann (o livro essencial; cobre replicação a consistência)
- *System Design Interview Vol. 1 & 2* — Alex Xu (walkthroughs práticos, excelente para entrevistas)
- *Building Microservices* — Sam Newman (patterns de decomposição e comunicação)
- *Database Internals* — Alex Petrov (o "como" por trás dos bancos distribuídos)

### Online
- [System Design Primer (GitHub)](https://github.com/donnemartin/system-design-primer) — referência completa e gratuita
- [ByteByteGo](https://bytebytego.com/) — Alex Xu, diagramas visuais excelentes
- [Hello Interview — System Design in a Hurry](https://www.hellointerview.com/learn/system-design/in-a-hurry/introduction) — moderno (2024+), de ex-entrevistadores FAANG
- [Martin Fowler's blog](https://martinfowler.com/) — CQRS, Event Sourcing, microservices patterns
- [High Scalability](http://highscalability.com/) — case studies de arquiteturas reais

### Vídeos
> [!info] SYSTEM DESIGN: ALÉM DA ENTREVISTA
> [https://www.youtube.com/live/-8tdjn30SSw?si=kcvd_nTLIYMNIrM6](https://www.youtube.com/live/-8tdjn30SSw?si=kcvd_nTLIYMNIrM6)

> [!info] 18 System Design Concepts Every Engineer Must Know
> [https://www.designgurus.io/blog/system-design-interview-fundamentals](https://www.designgurus.io/blog/system-design-interview-fundamentals)

## Veja também

- [[API Design]] — design de APIs REST, GraphQL, gRPC
- [[03-Dominios/Ciência/Banco de Dados/index|Banco de Dados]] — SQL, NoSQL, ACID, indexação, replicação, sharding
- [[Redes e Protocolos]] — TCP/UDP, DNS, HTTP, WebSocket, load balancing, CDN, caching HTTP
- [[03-Dominios/Engenharia/Comunicação entre Sistemas/Mensageria/Kafka]] — event streaming, partições, consumers
- [[RabbitMQ]] — message queuing, routing, dead letter queues
- [[Arquitetura de Software]] — patterns arquiteturais, microserviços, monolito
- [[Event Storming]] — event sourcing, domain events
- [[Spring Boot]] — troubleshooting Java em produção
- [[System Design Practice]] — exercícios práticos
- [[03-Dominios/Engenharia/Arquitetura/index|Arquitetura]] — o domínio
