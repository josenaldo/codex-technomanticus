---
title: "Microservices e sistemas distribuídos"
created: 2026-06-12
updated: 2026-06-12
type: moc
status: growing
publish: true
tags:
  - java
  - microservices
  - moc
aliases:
  - "Microservices e sistemas distribuídos"
  - "Microservices"
  - "Microsserviços"
  - "Spring Cloud"
  - "Sistemas distribuídos"
  - "Galho 16 - Microservices"
---

# Microservices e sistemas distribuídos

> [!abstract] TL;DR
> Este galho cobre como vários serviços formam uma plataforma distribuída: o modelo e a tese honesta, o ecossistema Spring Cloud, service discovery, API Gateway, resiliência com Resilience4j, comunicação síncrona entre serviços, segurança serviço a serviço, tracing distribuído com OpenTelemetry, consistência e service mesh. A tese que atravessa tudo: microservices é um **trade-off**, não o default. Quase sempre o **monólito modular basta**, e a **rede é o inimigo** — toda chamada que vira HTTP ganha latência, falha parcial e complexidade operacional. São **24 notas em 3 fases** (Iniciado, Adepto, Magus).

## Sobre este galho

A audiência é o desenvolvedor **pleno avançando para senior**, preparando-se para entrevista internacional, que precisa não só conhecer os padrões de Spring Cloud mas saber **defender quando NÃO usá-los**. Este é um galho **híbrido**: parte de pesquisa nova sobre o ecossistema distribuído e parte de **poda reversa do tronco `Spring Boot.md`**, extraindo o conteúdo de microservices que estava acoplado ao monólito.

A **fronteira-assinatura é dupla**. Atrás dele fica o **Galho 14 (Mensageria e eventos)** — saga, outbox, idempotência e gRPC vivem lá, porque são a face *assíncrona* do problema distribuído. À frente fica o **[[03-Dominios/Tecnologia/Java/Cloud-native e produção/index|Galho 17 (Cloud-native e produção)]]** — containers, orquestração e operação em produção. Este galho 16 ocupa o meio: a plataforma síncrona de serviços, sua descoberta, seu roteamento e sua resiliência.

## Iniciado

- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/01 - O que são microservices e a tese honesta|O que são microservices e a tese honesta]] — definição, promessas, custos reais e por que o default deveria ser o monólito modular.
- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/02 - Monorepo vs multi-repo|Monorepo vs multi-repo]] — como organizar o código de vários serviços e os trade-offs de cada estratégia.
- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/03 - Os 12 fatores e o serviço cloud-native|Os 12 fatores e o serviço cloud-native]] — o checklist do Twelve-Factor App aplicado a um serviço Spring.
- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/04 - Panorama do Spring Cloud — e o que morreu|Panorama do Spring Cloud — e o que morreu]] — o mapa do ecossistema, o que sobreviveu e os projetos descontinuados (Ribbon, Hystrix, Zuul).
- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/05 - Comunicação inter-serviços — síncrono vs assíncrono|Comunicação inter-serviços — síncrono vs assíncrono]] — os dois estilos de comunicação e quando cada um é a escolha certa.

## Adepto

- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/06 - Service discovery — o conceito e o Eureka|Service discovery — o conceito e o Eureka]] — por que serviços precisam se encontrar dinamicamente e como o Eureka resolve isso.
- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/07 - Discovery — Consul e Kubernetes-native|Discovery — Consul e Kubernetes-native]] — alternativas ao Eureka e o discovery que o próprio Kubernetes oferece.
- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/08 - Client-side load balancing — Spring Cloud LoadBalancer|Client-side load balancing — Spring Cloud LoadBalancer]] — balanceamento no cliente após a morte do Ribbon.
- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/09 - Comunicação síncrona — OpenFeign e HTTP Interface|Comunicação síncrona — OpenFeign e HTTP Interface]] — clientes declarativos para chamadas HTTP entre serviços.
- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/10 - API Gateway — papel, roteamento, predicates e filters|API Gateway — papel, roteamento, predicates e filters]] — a porta de entrada da plataforma e seu modelo de roteamento.
- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/11 - Gateway reativo vs MVC — as duas variantes|Gateway reativo vs MVC — as duas variantes]] — Spring Cloud Gateway reativo versus a variante baseada em Servlet/MVC.
- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/12 - Config centralizado — Spring Cloud Config|Config centralizado — Spring Cloud Config]] — configuração externalizada e centralizada para muitos serviços.
- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/13 - Resiliência I — a falha distribuída e o Circuit Breaker|Resiliência I — a falha distribuída e o Circuit Breaker]] — por que a falha parcial existe e como o Circuit Breaker do Resilience4j a contém.
- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/14 - Resiliência II — Retry e Time Limiter|Resiliência II — Retry e Time Limiter]] — repetição segura de chamadas e limites de tempo.
- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/15 - Resiliência III — Bulkhead e Rate Limiter|Resiliência III — Bulkhead e Rate Limiter]] — isolamento de recursos e controle de vazão.
- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/16 - Resiliência IV — compondo os padrões|Resiliência IV — compondo os padrões]] — a ordem correta de empilhar os decorators e o efeito combinado.
- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/17 - Segurança entre serviços|Segurança entre serviços]] — propagação de identidade, tokens e mTLS na comunicação serviço a serviço.
- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/18 - Tracing distribuído I — correlação no código|Tracing distribuído I — correlação no código]] — spans, contexto e correlação com Micrometer Tracing.
- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/19 - Tracing distribuído II — exportando o trace|Tracing distribuído II — exportando o trace]] — exportação via OpenTelemetry para backends como Tempo, Jaeger ou Zipkin.

## Magus

- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/20 - Consistência em sistemas distribuídos|Consistência em sistemas distribuídos]] — CAP, consistência eventual e os limites do que a rede permite garantir.
- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/21 - Os padrões de falha distribuída|Os padrões de falha distribuída]] — anti-padrões e armadilhas recorrentes em arquiteturas distribuídas.
- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/22 - Service mesh — quando a resiliência sai do código|Service mesh — quando a resiliência sai do código]] — Istio, Linkerd e o trade-off de mover resiliência para a infraestrutura.
- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/23 - Quando NÃO fazer microservices|Quando NÃO fazer microservices]] — os sinais de que o monólito modular é a resposta certa.
- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/24 - Capstone — uma requisição ponta a ponta na plataforma|Capstone — uma requisição ponta a ponta na plataforma]] — o trajeto completo de uma requisição cruzando gateway, discovery, resiliência e tracing.

## Rotas alternativas

- **Completa**: 01 → 02 → 03 → 04 → 05 → 06 → 07 → 08 → 09 → 10 → 11 → 12 → 13 → 14 → 15 → 16 → 17 → 18 → 19 → 20 → 21 → 22 → 23 → 24, em ordem.
- **Entrevista internacional**: 01 (a tese honesta) → 04 (panorama Spring Cloud) → 05 (síncrono vs assíncrono) → 13 (Circuit Breaker) → 16 (compondo a resiliência) → 18 (tracing no código) → 20 (consistência) → 23 (quando NÃO fazer) → 24 (capstone ponta a ponta).
- **A plataforma Spring Cloud na prática**: 04 (panorama) → 06 (discovery/Eureka) → 08 (load balancing) → 09 (OpenFeign/HTTP Interface) → 10 (API Gateway) → 11 (reativo vs MVC) → 12 (config centralizado).
- **Resiliência (meio galho, cai muito)**: 13 (Circuit Breaker) → 14 (Retry e Time Limiter) → 15 (Bulkhead e Rate Limiter) → 16 (compondo os padrões) → 21 (padrões de falha distribuída).
- **Arquitetura e julgamento**: 01 (a tese honesta) → 02 (monorepo vs multi-repo) → 03 (12 fatores) → 20 (consistência) → 22 (service mesh) → 23 (quando NÃO fazer).

## Veja também

- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Mensageria/index|Mensageria e eventos (Galho 14)]]
- [[03-Dominios/Tecnologia/Java/Segurança/index|Segurança (Galho 12)]]
- [[03-Dominios/Tecnologia/Java/Programação Reativa/index|Programação Reativa (Galho 11)]]
- [[03-Dominios/Tecnologia/Java/Web e APIs REST/index|Web e APIs REST (Galho 9)]]
- [[03-Dominios/Tecnologia/Java/Build e tooling/index|Build e tooling (Galho 15)]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java|Dicionário de Java]]
- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/index|Cloud-native e produção (Galho 17)]]
- Galho 18 — OCP / Certificação (planejado)
