---
title: "Roadmap — Python Cloud-native e produção"
created: 2026-07-12
type: meta
publish: false
tags:
  - meta
  - roadmap
  - python
---

# Roadmap — Cloud-native e produção (galho 18)

Roadmap-folha do galho `Python/Cloud-native e produção`. Fase **Magus** — containers Python, serverless/Lambda Python. Spec: [[00-Meta/specs/2026-07-09-python-trilha-design]]. EXEMPLAR de estrutura: `Python/Observabilidade e produção/index.md` e `roadmap.md` (galho anterior). Último galho do bloco "Plataforma distribuída e produção" (14-18), antes da Certificação (19).

**Fronteira cravada:** Dockerfile/health checks/graceful shutdown/métricas já construídos no Galho 17 (notas 03/05/06/07) — reusados, não repetidos. Java/Cloud-native e produção (22 notas) mistura observabilidade+deploy — Python já separou isso (observabilidade = Galho 17, deploy/orquestração = este galho).

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 8 |
| ⬜ pendente | 0 |
| ✅ feita | 8 |
| 🔄 em andamento | 0 |
| % concluído | 100% |

---

## Notas

#### 01 - Panorama — orquestrar de verdade
- **Estado:** ✅ feita (146 linhas) · fase: Magus
- **Escopo:** mapa do galho — temos imagem Docker (Galho 17), mas rodar "em algum lugar" de verdade significa Kubernetes de fato OU serverless. Panorama dos dois caminhos, honestidade sobre custo operacional de cada um.

#### 02 - Kubernetes na prática — Deployment, Service, ConfigMap e Secret
- **Estado:** ✅ feita (437 linhas) · fase: Magus
- **Escopo:** os 4 manifests essenciais aplicados aos serviços da trilha — `Deployment` (réplicas, template do Pod, `livenessProbe`/`readinessProbe` consumindo os endpoints do Galho 17 nota 06), `Service` (ClusterIP, DNS interno já mencionado no Galho 15 nota 05), `ConfigMap` (variáveis não-sensíveis), `Secret` (variáveis sensíveis, referenciando `pydantic-settings`/secrets do Galho 11 nota 06 sem repetir).

#### 03 - Recursos e limites — requests, limits e OOMKill
- **Estado:** ✅ feita (384 linhas) · fase: Magus
- **Escopo:** `resources.requests`/`resources.limits` de CPU/memória no manifest do Pod, o que acontece quando um Pod excede o limit de memória (OOMKill — processo morto abruptamente, SEM graceful shutdown, contraste com o shutdown gracioso do Galho 17 nota 05), como dimensionar requests/limits com base nas métricas já expostas (Galho 17 nota 03).

#### 04 - Rolling deploy sem downtime no Kubernetes
- **Estado:** ✅ feita (322 linhas) · fase: Magus
- **Escopo:** `RollingUpdate` strategy (`maxSurge`/`maxUnavailable`), como o Kubernetes coordena com o `readinessProbe` (Galho 17 nota 06) e o `graceful shutdown` (Galho 17 nota 05) do próprio processo Python pra garantir zero downtime — amarra os dois conceitos já ensinados na orquestração real.

#### 05 - Autoscaling — HPA baseado em métrica
- **Estado:** ✅ feita (424 linhas) · fase: Magus
- **Escopo:** `HorizontalPodAutoscaler` baseado em CPU (básico) e em métrica CUSTOMIZADA (baseado nas métricas OpenTelemetry/Prometheus já expostas no Galho 17 nota 03 — ex: escalar baseado em latência ou fila de mensagens do RabbitMQ do Galho 14) via `Prometheus Adapter`, mencionado sem desenvolver a fundo a configuração do adapter.

#### 06 - Serverless com AWS Lambda — Mangum e cold start
- **Estado:** ✅ feita (378 linhas) · fase: Magus
- **Escopo:** `Mangum` (adapter que traduz evento Lambda↔ASGI, permitindo rodar a MESMA aplicação FastAPI como Lambda sem reescrever nada), handler pattern, cold start (o que é, por que acontece, mitigação com provisioned concurrency), quando serverless faz sentido pro serviço de Notificações (tráfego esporádico/em rajadas) vs quando não faz (o serviço de Tarefas, com tráfego constante, é mais barato como container sempre rodando).

#### 07 - Containers vs serverless — trade-offs honestos
- **Estado:** ✅ feita (261 linhas) · fase: Magus
- **Escopo:** comparação direta — custo (serverless paga por invocação, container paga por tempo rodando independente de uso), cold start vs sempre-quente, controle operacional (container dá mais controle, serverless abstrai infra), limites de execução (Lambda tem timeout máximo, não serve pra processamento longo).

#### 08 - Capstone — os dois serviços em produção de verdade
- **Estado:** ✅ feita (574 linhas) · fase: Magus
- **Escopo:** recapitula o galho — o serviço de Tarefas deployado em Kubernetes com manifests completos (Deployment/Service/ConfigMap/Secret), recursos dimensionados, rolling deploy configurado, HPA baseado em métrica; o serviço de Notificações AVALIADO como candidato a Lambda (dado seu padrão de tráfego esporádico via consumo de fila), com a decisão sendo tomada explicitamente com os trade-offs da nota 07. Cenário prático integrador. Fecha o bloco "Plataforma distribuída e produção" (14-18) inteiro, apontando pro Galho 19 (Certificação) como último passo da trilha.

## Decisões e fronteiras registradas

- Dockerfile/imagem, health checks, graceful shutdown, métricas → Galho 17; reusados, não repetidos.
- Java/Cloud-native (observabilidade+deploy misturados) → referenciado pra contraste estrutural, não repetido em conteúdo.
- GraalVM Native Image/AOT (equivalente Java) → não existe equivalente direto em Python, fora do escopo.
- Service mesh, Helm charts, GitOps → fora do escopo (fica implícito como "próximo degrau" sem desenvolver, é infra avançada demais pra trilha de linguagem).
