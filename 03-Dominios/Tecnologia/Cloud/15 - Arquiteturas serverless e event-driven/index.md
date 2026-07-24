---
title: "Cloud — Arquiteturas serverless e event-driven"
created: 2026-07-24
updated: 2026-07-24
type: moc
status: growing
publish: true
tags:
  - cloud
  - moc
  - serverless
  - event-driven
  - arquitetura
aliases:
  - "Arquiteturas serverless e event-driven"
  - "Galho 15 - Arquiteturas serverless e event-driven"
---

# Arquiteturas serverless e event-driven

> [!abstract] TL;DR
> Galho 15 da trilha Cloud, e o **capstone do Bloco 3 (Serverless e arquiteturas modernas)**. Os galhos 11 a 14 deram as peças separadas — FaaS (Lambda), containers gerenciados, mensageria e API Gateway. Este galho costura essas peças numa arquitetura completa: recapitula o paradigma event-driven (borda síncrona, miolo assíncrono), formaliza a decisão central — **orquestração** (Step Functions, um maestro que sabe a partitura inteira) vs **coreografia** (eventos, ninguém manda, todos reagem) — aprofunda Step Functions como motor de workflow, mostra o pipeline de dados serverless como aplicação concreta do padrão, cataloga os padrões maduros e os anti-padrões que incendeiam produção, e fecha com uma arquitetura de referência que segue um pedido de e-commerce do clique ao e-mail de confirmação — e abre a ponte honesta pro Bloco 4. 6 notas, 3 fases, lente dupla AWS ↔ DigitalOcean.

## Sobre este galho

Um sistema event-driven não nasce de uma peça só — nasce do encaixe entre elas. Este galho não introduz um serviço gerenciado novo; ele pega o que os quatro galhos anteriores já ensinaram (função, container, fila, gateway) e responde à pergunta que fica de fora de cada um isoladamente: como essas peças se organizam numa arquitetura que alguém consegue operar, debugar e evoluir?

O fio condutor sobe da recapitulação à síntese. Primeiro o *paradigma* — o que é, de fato, um evento, os três papéis (produtor/evento/consumidor), e a regra de bolso borda-síncrona/miolo-assíncrono que atravessa o galho inteiro. Depois a *decisão central*, em duas notas: orquestração vs coreografia como dois jeitos de responder "e agora, o quê?" depois de um evento, e Step Functions a fundo como o motor que materializa a orquestração (state machine em ASL, standard vs express, saga com compensação, error handling). Depois duas notas de *aplicação*: o pipeline de dados serverless como o padrão event-driven mais comum na prática (S3→Lambda, Kinesis→Firehose, fan-out via Map), e os padrões maduros vs anti-padrões que separam um sistema desacoplado de um distributed monolith disfarçado. E por fim o *capstone* — uma arquitetura de referência completa, o pedido de e-commerce ponta a ponta, a tabela de decisão do Bloco 3 inteiro, e a ponte pro Bloco 4 (operar, sustentar, governar).

**Audiência primária:** quem já usa Lambda, filas e API Gateway isoladamente mas nunca projetou um sistema onde as três peças conversam entre si, nem sabe quando escolher orquestração sobre coreografia. **Audiência secundária:** quem já orquestra com Step Functions ou coreografa com EventBridge mas nunca formalizou os anti-padrões que corroem esse tipo de arquitetura em produção (Lambda monolítica, chamada síncrona escondida, estado em memória, distributed monolith).

> [!info] Fronteira
> Os **building blocks individuais** — FaaS/Lambda (galho 11), containers gerenciados (galho 12), mensageria e eventos (galho 13), API Gateway (galho 14) — não são reexplicados aqui, só encaixados. **IaC** (declarar essa arquitetura como código) é o Bloco 4; **observabilidade** (tracing distribuído, medir o sistema desacoplado em produção) também é Bloco 4; **FinOps** (custo agregado da arquitetura) idem. O **conceito de coreografia/coordenação distribuída** em abstrato vive em [[03-Dominios/Engenharia/Comunicação entre Sistemas/index|Comunicação entre Sistemas]]; este galho trata a decisão orquestração-vs-coreografia e os padrões *na nuvem*, com os serviços gerenciados como protagonistas.

## Iniciado

1. [[03-Dominios/Tecnologia/Cloud/15 - Arquiteturas serverless e event-driven/01 - O paradigma event-driven completo|01 — O paradigma event-driven completo]] — recap dos galhos 11-14 encaixados numa arquitetura: os três papéis (produtor/evento/consumidor), os building blocks recapitulados, a regra síncrono-na-borda/assíncrono-no-miolo com um pedido de e-commerce como fio condutor.

## Adepto

2. [[03-Dominios/Tecnologia/Cloud/15 - Arquiteturas serverless e event-driven/02 - Orquestração vs coreografia|02 — Orquestração vs coreografia]] — quem decide "e agora, o quê?": orquestração (um maestro, uma partitura — Step Functions) vs coreografia (ninguém manda, todos reagem — eventos), o padrão saga que aparece dos dois lados, trade-offs lado a lado.
3. [[03-Dominios/Tecnologia/Cloud/15 - Arquiteturas serverless e event-driven/03 - Step Functions a fundo|03 — Step Functions a fundo]] — o motor da orquestração: a state machine em Amazon States Language, tipos de estado, Standard vs Express workflows, saga com compensação para transações distribuídas, fan-out sobre uma lista (Map), error handling e retry.
4. [[03-Dominios/Tecnologia/Cloud/15 - Arquiteturas serverless e event-driven/04 - Pipeline de dados serverless|04 — Pipeline de dados serverless]] — o padrão event-driven mais comum na prática: como o dado entra no pipeline, landing→trigger→transform→load, S3→Lambda, Kinesis→Firehose→S3, fan-out orquestrado, armadilhas comuns de ETL serverless.
5. [[03-Dominios/Tecnologia/Cloud/15 - Arquiteturas serverless e event-driven/05 - Padrões e anti-padrões serverless|05 — Padrões e anti-padrões serverless]] — os padrões maduros (função de propósito único, fan-out/fan-in, idempotência, DLQ em tudo) e os anti-padrões que incendeiam produção (Lambda monolítica, chamada síncrona escondida, estado em memória, distributed monolith), e por que a observabilidade não é opcional aqui.

## Magus

6. [[03-Dominios/Tecnologia/Cloud/15 - Arquiteturas serverless e event-driven/06 - Arquitetura serverless de referência (capstone do Bloco 3)|06 — Arquitetura serverless de referência (capstone do Bloco 3)]] — a costura das dez peças dos galhos 8-15 numa arquitetura completa: um pedido de e-commerce do clique ao e-mail de confirmação, a tabela de decisão do Bloco 3 inteiro, quando essa arquitetura é a certa (e quando é over-engineering), e a ponte pro Bloco 4. Capstone do bloco.

## Rotas alternativas

### Completa

01 → 02 → 03 → 04 → 05 → 06. Percurso linear — o paradigma, a decisão central em duas notas, a aplicação em duas notas, e a arquitetura de referência no fim.

### Já uso Lambda e filas, quero fechar a arquitetura

02 (a decisão orquestração vs coreografia que toda entrevista de arquitetura cobra) → 05 (os anti-padrões que provavelmente já estão no seu sistema) → 06 (a arquitetura de referência e a tabela de decisão do bloco inteiro).

## Todas as notas

```dataview
TABLE fase, status FROM "03-Dominios/Tecnologia/Cloud/15 - Arquiteturas serverless e event-driven" WHERE type = "concept" SORT file.name ASC
```

## Veja também

- [[03-Dominios/Tecnologia/Cloud/index|Cloud]] (MOC do domínio)
- [[03-Dominios/Tecnologia/Cloud/11 - Serverless e FaaS — Lambda a fundo/index|Serverless e FaaS]] — Galho 11, o Lambda que este galho usa como consumidor/produtor de eventos
- [[03-Dominios/Tecnologia/Cloud/13 - Mensageria e eventos gerenciados/index|Mensageria e eventos gerenciados]] — Galho 13, os canais (SQS/SNS/EventBridge) que carregam o evento
- [[03-Dominios/Tecnologia/Cloud/14 - API Gateway e edge de aplicação/index|API Gateway e edge de aplicação]] — Galho 14, a borda síncrona por onde o sistema recebe o pedido
- [[03-Dominios/Engenharia/Comunicação entre Sistemas/index|Comunicação entre Sistemas]] — o conceito de coordenação distribuída e coreografia que este galho aplica com serviços gerenciados
