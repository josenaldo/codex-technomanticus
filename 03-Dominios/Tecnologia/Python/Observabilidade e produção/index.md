---
title: "Python — Observabilidade e produção"
created: 2026-07-12
type: moc
status: growing
publish: true
tags:
  - python
  - moc
aliases:
  - "Galho 17 - Observabilidade e produção"
---

# Observabilidade e produção

> [!abstract] TL;DR
> Galho 17 da trilha Python: logging estruturado (`structlog`/`logging` correlacionado com trace_id), métricas com OpenTelemetry/Prometheus client, WSGI vs ASGI na prática (`gunicorn`/`uvicorn`, o combo padrão de produção), configuração de servidor (workers, timeouts, graceful shutdown), health checks/probes, deploy básico. Fecha com capstone instrumentando os dois serviços do Galho 15/16 pra produção de verdade. Fase Magus; 8 notas. Quarto galho do bloco "Plataforma distribuída e produção" (14-18).

## Sobre este galho

Este galho é ferramental — a FILOSOFIA de observabilidade (SLI/SLO, alerting sem fadiga, incident response, postmortems blameless) já está coberta em profundidade e de forma agnóstica de linguagem em [[03-Dominios/Engenharia/Operação/4 - Observar e responder/index|Engenharia/Operação — Observar e responder]]. O TRACING distribuído já foi construído com código real no [[03-Dominios/Tecnologia/Python/Microservices e sistemas distribuídos/06 - Tracing distribuído com OpenTelemetry|Galho 15 nota 06]]. Este galho completa os outros dois pilares da observabilidade (logs e métricas) e cobre o que falta pra rodar um serviço Python em produção de verdade: servidor WSGI/ASGI configurado corretamente, health checks, deploy básico.

**Fronteiras anti-duplicação:** filosofia de observabilidade, SLI/SLO, alerting, incident response, postmortems → [[03-Dominios/Engenharia/Operação/4 - Observar e responder/index|Engenharia/Operação]], só referenciado. Tracing distribuído com OpenTelemetry → [[03-Dominios/Tecnologia/Python/Microservices e sistemas distribuídos/06 - Tracing distribuído com OpenTelemetry|Galho 15 nota 06]], já construído, reusado. Secrets/configuração segura → [[03-Dominios/Tecnologia/Python/Segurança/06 - Secrets e configuração segura|Galho 11 nota 06]]. Containers/Kubernetes/serverless em profundidade → Galho 18 futuro (Cloud-native e produção), aqui só mencionados como destino do deploy.

**Audiência:** quem já tem os dois serviços Python (Tarefas e Notificações) construídos, testados, com tooling consistente (Galhos 9-16) e precisa saber se algo quebrar em produção às 3 da manhã, dar pra diagnosticar.

## Magus

1. [[01 - Panorama — o que falta pra produção de verdade|01 — Panorama: o que falta pra produção de verdade]]
2. [[02 - Logging estruturado — structlog e correlação com trace|02 — Logging estruturado: structlog e correlação com trace]]
3. [[03 - Métricas com OpenTelemetry e Prometheus client|03 — Métricas com OpenTelemetry e Prometheus client]]
4. [[04 - WSGI vs ASGI na prática — gunicorn e uvicorn|04 — WSGI vs ASGI na prática: gunicorn e uvicorn]]
5. [[05 - Configuração de servidor de produção — workers, timeouts e graceful shutdown|05 — Configuração de servidor de produção: workers, timeouts e graceful shutdown]]
6. [[06 - Health checks e probes|06 — Health checks e probes]]
7. [[07 - Deploy básico — Dockerfile e CI-CD|07 — Deploy básico: Dockerfile e CI/CD]]
8. [[08 - Capstone — os dois serviços prontos pra produção|08 — Capstone: os dois serviços prontos pra produção]] — recapitula o galho.

## Todas as notas

```dataview
TABLE fase, status FROM "03-Dominios/Tecnologia/Python/Observabilidade e produção" WHERE type = "concept" SORT file.name ASC
```

## Veja também

- [[03-Dominios/Tecnologia/Python/index|Trilha Python]] (MOC central)
- [[03-Dominios/Engenharia/Operação/4 - Observar e responder/index|Operação — Observar e responder]] — filosofia de observabilidade, agnóstica de linguagem
- [[03-Dominios/Tecnologia/Python/Microservices e sistemas distribuídos/06 - Tracing distribuído com OpenTelemetry|Tracing distribuído]] — Galho 15 nota 06
- [[03-Dominios/Tecnologia/Python/Build e tooling/index|Build e tooling]] — Galho 16 (os dois serviços com tooling consistente que este galho leva pra produção)
