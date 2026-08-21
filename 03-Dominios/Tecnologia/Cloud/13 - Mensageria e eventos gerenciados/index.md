---
title: "Cloud — Mensageria e eventos gerenciados"
created: 2026-07-24
updated: 2026-07-24
type: moc
status: growing
publish: true
tags:
  - cloud
  - moc
  - mensageria
  - eventos
  - sqs
  - sns
  - eventbridge
aliases:
  - "Mensageria e eventos gerenciados"
  - "Galho 13 - Mensageria e eventos gerenciados"
---

# Mensageria e eventos gerenciados

> [!abstract] TL;DR
> Galho 13 da trilha Cloud, dentro do **Bloco 3 (Serverless e arquiteturas modernas)**. Como os componentes de um sistema na nuvem conversam sem acoplamento síncrono frágil: os serviços gerenciados de mensageria e eventos. O galho sobe do *porquê* ao *como escolher*: primeiro o problema que toda mensageria resolve (acoplamento síncrono, fila vs tópico vs bus), depois cada serviço da AWS por dentro — **SQS** (fila), **SNS** (pub/sub) e **EventBridge** (event bus) —, depois os **padrões event-driven** que esses serviços habilitam em conjunto (fan-out durável, idempotência, ordenação seletiva, outbox, DLQ com estratégia), e fecha com a **árvore de decisão** do capstone: SQS vs SNS vs EventBridge vs Kinesis/MSK, e a distinção mais cara de confundir — fila de trabalho vs. stream de dados. 6 notas, 3 fases, lente dupla AWS ↔ DigitalOcean (que aqui é a mais assimétrica da trilha: a DO não tem equivalente nativo a nenhum dos três serviços centrais).

## Sobre este galho

Mensageria gerenciada é a encarnação, como serviço-por-API, de um princípio de arquitetura que a trilha de Comunicação entre Sistemas já ensina em abstrato: publicar uma mensagem em vez de chamar diretamente quebra a corrente de acoplamento síncrono que faz uma falha periférica (um provedor de e-mail lento) virar uma indisponibilidade central (checkout fora do ar). O que este galho acrescenta não é a teoria — é como esse princípio ganha corpo em três serviços da AWS com contratos, limites e trade-offs bem diferentes entre si, e como eles se compõem em arquiteturas reais.

O fio condutor sobe do problema ao critério. Primeiro o *porquê* — o acoplamento síncrono e o que a mensageria assíncrona compra em troca (desacoplamento no tempo, buffer de pico, resiliência a falha parcial), e o panorama dos três sabores conceituais: fila (1 mensagem, 1 consumidor), pub/sub (1 mensagem, N assinantes) e event bus (roteamento por conteúdo). Depois a *mecânica*, serviço a serviço: SQS por dentro (visibility timeout, Standard vs FIFO, DLQ, long polling, at-least-once), SNS e o fan-out (push, filter policies, o padrão canônico SNS→SQS), EventBridge e o roteamento por conteúdo (event pattern, rules, targets, Scheduler, partner event sources, archive/replay). Depois os *padrões* que amarram os três num sistema coerente — fan-out durável, idempotência como consequência inevitável de at-least-once, ordenação seletiva, outbox na cloud, DLQ com alarme e redrive disciplinado. E por fim a *decisão* — a árvore que distingue fila de pub/sub de event bus de stream (Kinesis/MSK), e mostra como os quatro se compõem numa arquitetura de e-commerce real.

**Audiência primária:** quem já usa Lambda ou API Gateway mas nunca decidiu, com intenção, entre SQS, SNS e EventBridge — ou que ouviu os três nomes em entrevista e não sabe articular quando cada um vence. **Audiência secundária:** quem já opera SQS/SNS no dia a dia mas nunca formalizou os padrões de arquitetura por trás (por que SNS→SQS e não SNS→Lambda direto, como fazer idempotência de verdade, quando FIFO vale o custo de throughput que ele cobra).

> [!info] Fronteira
> O **conceito de fila, pub/sub, event-driven, idempotência, ordenação, outbox e saga** vive em [[03-Dominios/Engenharia/Comunicação entre Sistemas/index|Comunicação entre Sistemas]] — este galho assume essa teoria como pré-requisito e mostra como ela se encarna em serviço gerenciado, sem reensiná-la. O **modelo de eventos do Lambda** (SQS/SNS/EventBridge como *fontes* de evento, olhando de fora pra dentro) é o Galho 11 (nota 03) — este galho olha os mesmos serviços de dentro, por si mesmos. **Streaming a fundo** (Kinesis, MSK/Kafka) é tocado no capstone só o suficiente pra distinguir de fila/pub-sub, sem aprofundar — se este galho ganhar um sub-galho dedicado a streaming no futuro, é lá que Kinesis/MSK merecem tratamento completo. **Orquestração explícita** (Step Functions, máquinas de estado, sagas orquestradas) é o próximo galho da trilha. **API Gateway e a porta síncrona de entrada** também vêm depois.

## Iniciado

1. [[03-Dominios/Tecnologia/Cloud/13 - Mensageria e eventos gerenciados/01 - Por que mensageria na nuvem|01 — Por que mensageria na nuvem]] — o problema do acoplamento síncrono (A chama B, B cai, A cai junto), o que assíncrono compra (desacoplamento no tempo, buffer de pico, resiliência a falha parcial), os três sabores conceituais (fila, pub/sub, event bus) e o que "gerenciado" tira do seu prato; AWS tem o catálogo completo, DigitalOcean não tem paridade nenhuma (só Managed Kafka).

## Adepto

2. [[03-Dominios/Tecnologia/Cloud/13 - Mensageria e eventos gerenciados/02 - SQS a fundo|02 — SQS a fundo]] — a fila gerenciada por dentro: ciclo `SendMessage`/`ReceiveMessage`/`DeleteMessage`, visibility timeout como coração do mecanismo, long vs short polling, Standard (throughput quase ilimitado, ordem best-effort) vs FIFO (ordem exata por `MessageGroupId`, dedupe de 5min), dead-letter queue e redrive, retenção/delay/tamanho de mensagem, e por que idempotência é responsabilidade do consumidor, não do SQS.
3. [[03-Dominios/Tecnologia/Cloud/13 - Mensageria e eventos gerenciados/03 - SNS e pub-sub|03 — SNS e pub/sub]] — o tópico gerenciado e o fan-out via push: tipos de assinatura (SQS, Lambda, HTTP/S, email, SMS), Standard vs FIFO topic, o padrão canônico SNS→múltiplas SQS (por que a fila entre tópico e consumidor dá durabilidade), filter policies como roteamento sem lógica no publisher, A2P (alertas via SMS/email) e o contraste push (SNS) vs pull (SQS).
4. [[03-Dominios/Tecnologia/Cloud/13 - Mensageria e eventos gerenciados/04 - EventBridge e o event bus|04 — EventBridge e o event bus]] — o roteador de eventos por conteúdo: event bus (default/custom/partner), rules com event pattern casando o JSON inteiro (não só atributos), até 5 targets com input transformer, EventBridge Scheduler (cron gerenciado), partner event sources, schema registry, archive/replay, EventBridge Pipes; comparação direta com SNS (granularidade de filtro vs fan-out em massa) e a ausência quase total de equivalente na DigitalOcean.
5. [[03-Dominios/Tecnologia/Cloud/13 - Mensageria e eventos gerenciados/05 - Padrões event-driven na cloud|05 — Padrões event-driven na cloud]] — os padrões que transformam peças em arquitetura: fan-out durável (SNS→SQS, não SNS→Lambda direto), idempotência via escrita condicional no DynamoDB, ordenação seletiva (standard vs FIFO, o custo real em throughput), outbox na cloud (quem faz o papel do relay — Lambda agendado, AWS DMS, EventBridge Pipes), DLQ com estratégia (alarme + redrive disciplinado, nunca redrive sem corrigir a causa raiz), e a prévia de coreografia (EventBridge/SNS→SQS) vs orquestração (Step Functions).

## Magus

6. [[03-Dominios/Tecnologia/Cloud/13 - Mensageria e eventos gerenciados/06 - Escolher o serviço de mensageria (capstone)|06 — Escolher o serviço de mensageria]] — a árvore de decisão que amarra o galho: trabalho a distribuir (SQS) vs fato a publicar pra N assinantes (SNS/SNS→SQS) vs roteamento por conteúdo/SaaS/cron (EventBridge) vs stream ordenado e replayável (Kinesis Data Streams ou MSK); a distinção-chave fila (dono do cursor = o serviço) vs stream (dono do cursor = você); Kinesis vs MSK (portabilidade e ecossistema Kafka); um diagrama de arquitetura real compondo os quatro; anti-padrões (fila pra request-response síncrono, EventBridge pra alto throughput de streaming); ponte pro próximo galho (API Gateway, orquestração via Step Functions). Capstone do galho.

## Rotas alternativas

### Completa

01 → 02 → 03 → 04 → 05 → 06. Percurso linear — o problema, os três serviços por dentro, os padrões que os amarram, e a árvore de decisão final.

### Já uso SQS/SNS, quero fechar as lacunas de arquitetura

05 (os padrões — fan-out durável, idempotência, outbox, DLQ com estratégia — que separam quem opera mensageria de quem só usa) → 06 (a árvore que distingue fila de pub/sub de event bus de stream, e resolve a pergunta de entrevista "SQS, SNS ou EventBridge?" de vez).

## Veja também

- [[03-Dominios/Tecnologia/Cloud/index|Cloud]] (MOC do domínio)
- [[03-Dominios/Tecnologia/Cloud/11 - Serverless e FaaS — Lambda a fundo/03 - O modelo de eventos: triggers e integrações|O modelo de eventos (galho 11)]] — os mesmos três serviços vistos de fora, como fontes de evento que disparam Lambda
- [[03-Dominios/Engenharia/Comunicação entre Sistemas/index|Comunicação entre Sistemas]] — o conceito de fila, pub/sub, idempotência, ordenação, outbox e saga que este galho encarna em serviço gerenciado
