---
title: "Roadmap — Python Observabilidade e produção"
created: 2026-07-12
type: meta
publish: false
tags:
  - meta
  - roadmap
  - python
---

# Roadmap — Observabilidade e produção (galho 17)

Roadmap-folha do galho `Python/Observabilidade e produção`. Fase **Magus** — logging, OpenTelemetry, WSGI/ASGI (gunicorn/uvicorn), deploy. Spec: [[00-Meta/specs/2026-07-09-python-trilha-design]]. EXEMPLAR de estrutura: `Python/Build e tooling/index.md` e `roadmap.md` (galho anterior).

**Fronteira cravada:** filosofia de observabilidade (SLI/SLO, alerting, incident response) já em [[03-Dominios/Engenharia/Operação/4 - Observar e responder/index|Engenharia/Operação]]; tracing distribuído já construído no [[03-Dominios/Tecnologia/Python/Microservices e sistemas distribuídos/06 - Tracing distribuído com OpenTelemetry|Galho 15 nota 06]]. Este galho completa logs+métricas e cobre servidor de produção/deploy básico. Containers/K8s/serverless em profundidade → Galho 18.

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

#### 01 - Panorama — o que falta pra produção de verdade
- **Estado:** ✅ feita (2026-07-12) · fase: Magus
- **Resultado:** 153 linhas / 3476 palavras (nota-mapa mais leve). Abre com os dois serviços caindo às 3h sem log/métrica; mapeia os 3 pilares (tracing já feito no Galho 15, logs+métricas pendentes); roteiro do galho.
- **Escopo:** mapa dos 3 pilares da observabilidade (logs, métricas, traces — tracing já feito no Galho 15, aqui completa os outros 2) + servidor de produção + deploy básico. Referencia a filosofia de Operação sem repetir.

#### 02 - Logging estruturado — structlog e correlação com trace
- **Estado:** ✅ feita (2026-07-12) · fase: Magus
- **Resultado:** 333 linhas / 4786 palavras. Abre com busca de 40min via regex em log não estruturado vs filtro trivial pós-structlog; `structlog` bound loggers, processor customizado injetando `trace_id`/`span_id` do Galho 15 nota 06, JSON produção vs console dev.
- **Escopo:** `logging` stdlib vs `structlog` (logs como dicionários/JSON, não strings formatadas — facilita busca/agregação em produção), correlação de log com `trace_id` do OpenTelemetry (Galho 15 nota 06, referenciado sem repetir) via `contextvars`, níveis de log e quando usar cada um.

#### 03 - Métricas com OpenTelemetry e Prometheus client
- **Estado:** ✅ feita (2026-07-12) · fase: Magus
- **Resultado:** 394 linhas / 6133 palavras. Abre com degradação gradual de latência (80ms→340ms) não pega por log de erro; Counter/Histogram/UpDownCounter via `opentelemetry-sdk` e `prometheus_client`, 4 golden signals aplicados a `POST /tarefas`, cardinalidade alta como armadilha.
- **Escopo:** métricas (contador, histograma, gauge) via `opentelemetry-api`/`prometheus_client`, instrumentação de endpoint FastAPI (latência, contagem de requests, taxa de erro — os "4 golden signals" na prática), referenciando SLI/SLO da Operação sem repetir o conceito, aqui é só a instrumentação.

#### 04 - WSGI vs ASGI na prática — gunicorn e uvicorn
- **Estado:** ✅ feita (2026-07-12) · fase: Magus
- **Resultado:** 285 linhas / 4634 palavras. Abre com `uvicorn` sozinho usando 1 de 8 cores; combo `gunicorn -k uvicorn.workers.UvicornWorker`, regra `(2×núcleos)+1` condicionada a I/O-bound vs CPU-bound (Galho 6/7), `uvicorn --workers` standalone como alternativa.
- **Escopo:** `gunicorn` (WSGI, workers síncronos, maduro) vs `uvicorn` (ASGI, referenciando o protocolo cru do Galho 8 nota 05 sem repetir), o combo padrão de produção `gunicorn -k uvicorn.workers.UvicornWorker` (gunicorn como process manager, uvicorn workers como ASGI de fato), número de workers (regra prática `2*CPU+1`).

#### 05 - Configuração de servidor de produção — workers, timeouts e graceful shutdown
- **Estado:** ✅ feita (2026-07-12) · fase: Magus
- **Resultado:** 291 linhas / 4059 palavras. Abre com pico de 502 toda sexta às 17h por rolling deploy sem graceful shutdown; `--timeout`/`--graceful-timeout`/`--preload`/`--max-requests`, checklist completo em `gunicorn.conf.py`.
- **Escopo:** timeouts de worker (`--timeout`), graceful shutdown (`SIGTERM` handling — dar tempo pra requisições em andamento terminarem antes de matar o processo, crucial em deploy rolling), preload de app, restart automático de worker (`--max-requests` pra evitar memory leak acumulado).

#### 06 - Health checks e probes
- **Estado:** ✅ feita (2026-07-12) · fase: Magus
- **Resultado:** 235 linhas / 4110 palavras. Abre com rolling deploy mandando tráfego antes do pool de banco abrir; liveness (`/health` burro) vs readiness (`/ready` checando Postgres+RabbitMQ do Galho 14), armadilha de readiness cascateando falha.
- **Escopo:** endpoint `/health`/`/ready` simples, distinção liveness (processo está vivo?) vs readiness (processo está pronto pra receber tráfego? — ex: conexão de banco ainda não estabelecida no boot), menção a como Kubernetes usa isso (probe, sem desenvolver K8s a fundo — fica pro Galho 18).

#### 07 - Deploy básico — Dockerfile e CI/CD
- **Estado:** ✅ feita (2026-07-12) · fase: Magus
- **Resultado:** 343 linhas / 4191 palavras. Abre com imagem de 1.2GB por incluir toolchain+.git+cache; Dockerfile multi-stage com `uv sync --frozen`, usuário não-root, `.dockerignore`, pipeline GitHub Actions 2 jobs (test→build) com ruff/pytest como gate.
- **Escopo:** `Dockerfile` mínimo pra um serviço Python (multi-stage build com `uv`, referenciando o Galho 16 sem repetir), pipeline CI/CD conceitual (build→test→deploy, referenciando Engenharia/Operação sem repetir a filosofia de release). Não desenvolve Kubernetes/orquestração (Galho 18).

#### 08 - Capstone — os dois serviços prontos pra produção
- **Estado:** ✅ feita (2026-07-12) · fase: Magus
- **Escopo:** recapitula o galho instrumentando os dois serviços (Tarefas e Notificações) com logging estruturado correlacionado a trace, métricas expostas, servidor gunicorn+uvicorn configurado com graceful shutdown, health checks, Dockerfile. Cenário prático integrador. Aponta para o Galho 18 (Cloud-native e produção) como próximo passo.
- **Resultado:** 538 linhas / 6209 palavras. 5 peças amarrando as 7 notas nos 2 serviços reais, com assimetria deliberada onde faz sentido (readiness checks diferentes por serviço). Síntese: incidente simulado de lentidão de banco diagnosticado em 8 minutos usando os 3 pilares juntos (métrica detecta, trace localiza, log correlacionado explica). Fecha o galho.

> [!success] Galho 17 completo — 8/8 notas (2026-07-12)
> Panorama dos 3 pilares (01) → logging estruturado correlacionado (02) → métricas/golden signals (03) → gunicorn+uvicorn (04) → configuração de servidor/graceful shutdown (05) → health checks (06) → Dockerfile/CI-CD (07) → capstone com incidente simulado provando o valor conjunto (08). Tracing (Galho 15) e filosofia de observabilidade (Engenharia/Operação) nunca repetidos. Próximo da trilha: Galho 18 — Cloud-native e produção.

## Decisões e fronteiras registradas

- Filosofia de observabilidade (SLI/SLO, alerting, incident response, postmortems) → Engenharia/Operação SG4; referenciado, não repetido.
- Tracing distribuído → Galho 15 nota 06; reusado, não reconstruído.
- Secrets/config segura → Galho 11 nota 06; reusado.
- Kubernetes/containers/serverless em profundidade → Galho 18 futuro; aqui só mencionados como destino.
