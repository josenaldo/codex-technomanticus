---
title: "Cloud — Observabilidade na cloud"
created: 2026-07-24
updated: 2026-07-24
type: moc
status: growing
publish: true
tags:
  - cloud
  - moc
  - observabilidade
  - cloudwatch
  - xray
aliases:
  - "Observabilidade na cloud"
  - "Galho 17 - Observabilidade na cloud"
---

# Observabilidade na cloud

> [!abstract] TL;DR
> Galho 17 da trilha Cloud, dentro do **Bloco 4**. Como enxergar um sistema distribuído rodando na nuvem, onde nenhuma peça sozinha sabe contar a história inteira de um pedido. O galho sobe pelos **três pilares** — logs, métricas, traces — na sua encarnação gerenciada na AWS: **CloudWatch** (logs, métricas, alarmes, dashboards) e **X-Ray** (tracing distribuído), separando o que é conveniência específica do provedor do que é portável via **OpenTelemetry**. Depois cobre a disciplina de **alarmes e resposta a incidente** (o material bruto que a cloud oferece; SLO/error budget de raspão), a observabilidade peculiar de **serverless** (a função que só existe por 100ms), e fecha com um **capstone** que instrumenta, ponta a ponta, a arquitetura de referência do Galho 15 — e assume, sem rodeios, a lacuna real da DigitalOcean. 6 notas, 3 fases, lente dupla AWS ↔ DigitalOcean.

## Sobre este galho

Observabilidade é a resposta a uma pergunta que os blocos anteriores empurraram para debaixo do tapete: depois de desenhar uma arquitetura distribuída — VMs elásticas, serviços gerenciados, funções serverless, filas e tópicos — como você sabe, de fato, o que ela está fazendo agora, e por que um pedido específico deu errado? Este galho não trata observabilidade como acessório de fim de projeto; trata como a lente que torna um sistema distribuído legível, e ensina a mecânica gerenciada da AWS a fundo, sem esconder onde ela amarra você ao provedor.

O fio condutor sobe do *porquê* ao *operar*. Primeiro o modelo mental — os três pilares (logs, métricas, traces), a diferença entre monitoramento (perguntas que você já sabia fazer) e observabilidade (perguntas que você não previu), e o panorama de ferramentas nativas vs. portáveis. Depois a mecânica em duas notas: CloudWatch a fundo (logs em log groups/streams, métricas com namespace/dimensions, Embedded Metric Format, dashboards, o custo que cresce sem avisar) e tracing distribuído (X-Ray, trace ID que atravessa hops, segments, service map, e o padrão neutro OpenTelemetry por trás dos dois mundos). Depois a disciplina de **agir** sobre o que se observa — alarmes de métrica, composite alarms, o filtro do sintoma-não-causa, SLO/error budget de raspão, e onde a cloud para e a Engenharia de Operação assume. Depois o caso específico e traiçoeiro do **serverless** — a função que não tem host pra logar, o que a AWS empurra de graça pro CloudWatch/X-Ray, e a armadilha do lock-in que cresce junto com a conveniência. E por fim o **capstone**, que pega o "pedido perdido" da arquitetura de referência do Galho 15 e o rastreia ponta a ponta, fechando com a escolha entre nativo, OpenTelemetry portável, ou SaaS terceirizado.

**Audiência primária:** quem já operou VMs e serviços gerenciados nos blocos anteriores mas nunca instrumentou um sistema distribuído de propósito — não sabe por onde começar quando um pedido "some" entre cinco peças gerenciadas. **Audiência secundária:** quem já usa CloudWatch/X-Ray no dia a dia mas nunca formalizou a diferença entre monitoramento e observabilidade, nem decidiu, com intenção, o quanto vale a pena amarrar a stack de observabilidade ao provedor.

> [!info] Fronteira
> A **disciplina de SLO/error budget e resposta a incidente** (runbooks, postmortem, on-call maduro) pertence a [[03-Dominios/Engenharia/Operação/index|Operação]] — aqui é só o material bruto que a cloud oferece (alarmes, thresholds, notificação) pra sustentá-la. A **arquitetura serverless que este galho instrumenta** é a do [[03-Dominios/Tecnologia/Cloud/15 - Arquiteturas serverless e event-driven/index|Galho 15]]. **FinOps** (otimização de custo a fundo, inclusive o custo de operar observabilidade) é o Galho 19. Este galho trata a mecânica de ver e alarmar — logs, métricas, traces, thresholds — e linka essas fronteiras em vez de reexplicá-las.

## Iniciado

1. [[03-Dominios/Tecnologia/Cloud/17 - Observabilidade na cloud/01 - Por que observabilidade na cloud|01 — Por que observabilidade na cloud]] — o sistema distribuído opaco (o pedido que sumiu entre seis peças gerenciadas), monitoramento vs. observabilidade, os três pilares (logs, métricas, traces), o panorama de ferramentas e a tradução de nomes entre provedores; AWS CloudWatch+X-Ray ↔ DO Monitoring (sem tracing).

## Adepto

2. [[03-Dominios/Tecnologia/Cloud/17 - Observabilidade na cloud/02 - CloudWatch a fundo|02 — CloudWatch a fundo]] — o hub de observabilidade nativo da AWS por dentro: log groups/streams e retenção, logs estruturados e Logs Insights, métricas (namespace, dimensions, resolução standard vs. high-resolution, degradação da retenção), Embedded Metric Format, dashboards e Contributor Insights, alarmes (do threshold à ação), e a armadilha do custo que cresce peça a peça; CloudWatch ↔ DigitalOcean Monitoring.
3. [[03-Dominios/Tecnologia/Cloud/17 - Observabilidade na cloud/03 - Tracing distribuído|03 — Tracing distribuído]] — o que só o trace responde ("o que aconteceu com ESTE pedido, através de todos os serviços"): um ID que nasce no primeiro hop e viaja em todo header seguinte, o AWS X-Ray como serviço gerenciado (segments, subsegments, sampling, service map), debugando o pedido sumido com o service map, e o padrão neutro OpenTelemetry que promete instrumentar uma vez e mandar pra qualquer lugar; X-Ray ↔ ausência de equivalente na DO.
4. [[03-Dominios/Tecnologia/Cloud/17 - Observabilidade na cloud/04 - Alarmes, SLO e resposta|04 — Alarmes, SLO e resposta]] — dado sem ação é decoração: o alarme bom dispara no sintoma que o usuário sente, não em cada causa interna (alert fatigue); alarmes de métrica e composite alarms (AND/OR pra reduzir ruído), detecção de anomalia como alternativa ao threshold fixo, do alarme até a pessoa via SNS (e-mail, Slack, PagerDuty, auto-remediação), SLO/SLI/error budget de raspão, e onde a cloud para e a Operação assume; CloudWatch Alarms ↔ DO monitoring básico (sem composite alarms).
5. [[03-Dominios/Tecnologia/Cloud/17 - Observabilidade na cloud/05 - Observabilidade de serverless e o específico do provedor|05 — Observabilidade de serverless e o específico do provedor]] — observar uma caixa que só existe por 100ms: o que a AWS empurra de graça pra Lambda (logs START/END/REPORT, métricas automáticas), quando o REPORT não basta e X-Ray entra (e o preço do lock-in), a armadilha de logar demais em escala, casos práticos (filtrando cold starts, achando a REPORT mais lenta via Logs Insights), e a escolha nativo-cômodo vs. OTel-neutro; Lambda Insights/X-Ray ↔ DO Functions com monitoring básico, sem X-Ray.

## Magus

6. [[03-Dominios/Tecnologia/Cloud/17 - Observabilidade na cloud/06 - Operar a observabilidade (capstone)|06 — Operar a observabilidade (capstone)]] — a arquitetura serverless de referência do Galho 15 instrumentada peça por peça (o que logar, medir, tracear em cada uma), o trace_id costurando tudo, rastreando o pedido perdido ponta a ponta como se faria às 3 da manhã com o pager tocando, a estratégia dos três pilares aplicada a um sistema real, o custo de operar observabilidade, e a escolha final entre nativo (CloudWatch/X-Ray), OpenTelemetry portável, ou SaaS terceirizado — com a fronteira honesta AWS vs. DigitalOcean. Capstone do galho; ponte→Galho 18.

## Rotas alternativas

### Completa

01 → 02 → 03 → 04 → 05 → 06. Percurso linear — os três pilares, a mecânica do CloudWatch, o tracing, a disciplina de alarmes, o caso serverless, e a instrumentação de ponta a ponta no capstone.

### Já uso CloudWatch, quero fechar as lacunas

03 (o tracing que ninguém configura até precisar) → 04 (o alarme que dispara no sintoma certo, não em ruído) → 06 (como tudo isso se costura numa arquitetura real, com trace_id atravessando os serviços).

## Veja também

- [[03-Dominios/Tecnologia/Cloud/index|Cloud]] (MOC do domínio)
- [[03-Dominios/Tecnologia/Cloud/15 - Arquiteturas serverless e event-driven/index|Arquiteturas serverless e event-driven]] — Galho 15, a arquitetura de referência que o capstone deste galho instrumenta
- [[03-Dominios/Engenharia/Operação/index|Operação]] — a disciplina de SLO, error budget e resposta a incidente que este galho só toca de raspão
