---
title: "Python — Cloud-native e produção"
created: 2026-07-12
type: moc
status: growing
publish: true
tags:
  - python
  - moc
aliases:
  - "Galho 18 - Cloud-native e produção"
---

# Cloud-native e produção

> [!abstract] TL;DR
> Galho 18 da trilha Python: Kubernetes na prática (Deployment/Service/ConfigMap/Secret aplicados aos serviços da trilha), recursos e limites (requests/limits, OOMKill), rolling deploy sem downtime, autoscaling (HPA baseado em métrica), e serverless com AWS Lambda (Mangum, cold start, quando faz sentido). Fecha com capstone deployando os dois serviços — um em Kubernetes com HPA, outro avaliado como Lambda. Fase Magus; 8 notas. Último galho do bloco "Plataforma distribuída e produção" (14-18), antes da Certificação.

## Sobre este galho

Este galho pressupõe o que já foi construído: Dockerfile multi-stage e health checks (`/health`/`/ready`) já em [[03-Dominios/Tecnologia/Python/Observabilidade e produção/07 - Deploy básico — Dockerfile e CI-CD|Galho 17 nota 07]] e [[03-Dominios/Tecnologia/Python/Observabilidade e produção/06 - Health checks e probes|nota 06]], graceful shutdown já em [[03-Dominios/Tecnologia/Python/Observabilidade e produção/05 - Configuração de servidor de produção — workers, timeouts e graceful shutdown|nota 05]], métricas já em [[03-Dominios/Tecnologia/Python/Observabilidade e produção/03 - Métricas com OpenTelemetry e Prometheus client|nota 03]]. Este galho é sobre ORQUESTRAR isso de verdade — Kubernetes de fato, não só o contrato que o código expõe — e sobre a alternativa serverless.

**Fronteiras anti-duplicação:** Dockerfile/imagem em si → Galho 17 nota 07, reusado. Health checks/probes como CONTRATO → Galho 17 nota 06, aqui é o manifest Kubernetes que os consome. Graceful shutdown → Galho 17 nota 05, reusado. Métricas → Galho 17 nota 03, usadas aqui pra autoscaling. Java/Cloud-native e produção (22 notas, mistura observabilidade+deploy) é exemplar de outra stack, referenciado pra contraste sem repetir.

**Audiência:** quem já tem os dois serviços Python prontos pra produção (Galho 17) e precisa saber COMO de fato rodar isso num cluster ou como serverless.

## Magus

1. [[01 - Panorama — orquestrar de verdade|01 — Panorama: orquestrar de verdade]]
2. [[02 - Kubernetes na prática — Deployment, Service, ConfigMap e Secret|02 — Kubernetes na prática: Deployment, Service, ConfigMap e Secret]]
3. [[03 - Recursos e limites — requests, limits e OOMKill|03 — Recursos e limites: requests, limits e OOMKill]]
4. [[04 - Rolling deploy sem downtime no Kubernetes|04 — Rolling deploy sem downtime no Kubernetes]]
5. [[05 - Autoscaling — HPA baseado em métrica|05 — Autoscaling: HPA baseado em métrica]]
6. [[06 - Serverless com AWS Lambda — Mangum e cold start|06 — Serverless com AWS Lambda: Mangum e cold start]]
7. [[07 - Containers vs serverless — trade-offs honestos|07 — Containers vs serverless: trade-offs honestos]]
8. [[08 - Capstone — os dois serviços em produção de verdade|08 — Capstone: os dois serviços em produção de verdade]] — recapitula o galho e fecha o bloco "Plataforma distribuída e produção".

## Todas as notas

```dataview
TABLE fase, status FROM "03-Dominios/Tecnologia/Python/Cloud-native e produção" WHERE type = "concept" SORT file.name ASC
```

## Veja também

- [[03-Dominios/Tecnologia/Python/index|Trilha Python]] (MOC central)
- [[03-Dominios/Tecnologia/Python/Observabilidade e produção/index|Observabilidade e produção]] — Galho 17 (Dockerfile, health checks, métricas, graceful shutdown reusados aqui)
- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/index|Java — Cloud-native e produção]] — trilha irmã, escopo mais amplo (mistura observabilidade+deploy)
