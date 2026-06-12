---
title: "Dashboards e alertas — Grafana"
created: 2026-06-12
updated: 2026-06-12
type: concept
status: seedling
publish: true
fase: adepto
tags:
  - java
  - cloud-native
  - adepto
  - observabilidade
  - grafana
aliases:
  - "Grafana"
  - "RED e USE"
---

# Dashboards e alertas — Grafana

> [!abstract] TL;DR
> **Grafana** é a camada de **visualização** que se conecta ao Prometheus (e a outras fontes) e transforma séries temporais em **dashboards** e **alertas**. Coletar métrica é só metade do trabalho — sem painel ninguém olha, e sem alerta ninguém é avisado. Dois métodos guiam *o que medir*: **RED** (Rate, Errors, Duration) para **serviços** e **USE** (Utilization, Saturation, Errors) para **recursos**. Um bom dashboard de serviço Spring mostra taxa de request, latência p95/p99, erros 5xx e saturação do pool de conexões — e os alertas miram **sintoma** (SLO violado), não ruído.

## O que é

Grafana é uma plataforma open-source de **visualização e monitoramento**. Ela não armazena métricas: ela **lê** de fontes de dados (Prometheus, Loki para logs, bancos SQL, e mais de 150 plugins) e desenha **dashboards** — coleções de painéis (*panels*) com gráficos, tabelas e heatmaps.

Pensando na pilha de observabilidade: o [[03-Dominios/Java/Cloud-native e produção/14 - Métricas em produção — Micrometer e Prometheus|Micrometer instrumenta e o Prometheus armazena]]; o Grafana é onde um humano *enxerga* esses números. A linha atual é a **13.x** (Grafana 13.0 trouxe templates de dashboard, sugestões de visualização e Git Sync para versionar painéis).

> [!tip] A analogia
> Prometheus é o **arquivo** cheio de medições; Grafana é a **sala de controle** com os mostradores na parede. Você não decide *o que está acontecendo* lendo o arquivo linha a linha — você olha o painel.

## Por que importa

Métrica que ninguém visualiza é métrica morta. O valor de observabilidade aparece quando:

- **Diagnóstico fica rápido.** Em um incidente, um dashboard bem montado responde "o serviço está lento ou está retornando erro?" em segundos, sem precisar escrever PromQL na hora.
- **Alertas avisam antes do usuário.** Um alerta sobre taxa de erro 5xx subindo dispara antes do cliente abrir um ticket.
- **Há um vocabulário compartilhado.** RED e USE dão à equipe um critério objetivo do que colocar no painel, evitando dashboards que viram "decoração".

Em entrevista de nível pleno/sênior, saber *citar RED e USE* e explicar *por que* um alerta deve mirar sintoma (não causa) separa quem só "configurou Grafana uma vez" de quem entende monitoramento.

## Como funciona

### Grafana sobre Prometheus

O Grafana adiciona o Prometheus como **data source** e consulta via **PromQL**. Cada painel guarda uma query; o Grafana a executa periodicamente e renderiza o resultado. O fluxo:

```text
Spring Boot  →  /actuator/prometheus  →  Prometheus (scrape + storage)  →  Grafana (PromQL + render)
   (Micrometer)        (exposição)            (TSDB)                          (dashboards/alertas)
```

Grafana **não** faz scrape nem guarda histórico de métricas — quem faz isso é o Prometheus. O Grafana é stateless quanto aos dados: ele só pergunta e desenha. Isso o torna intercambiável (a mesma instância serve Prometheus, Loki, etc.).

### RED para serviços

O método **RED** define o mínimo a medir para qualquer serviço que atende requisições:

- **Rate** — quantas requisições por segundo.
- **Errors** — quantas dessas falham (ex.: respostas 5xx).
- **Duration** — quanto tempo levam (distribuição de latência, não só a média).

RED é orientado ao **request**: ele descreve a experiência de quem chama o serviço. É o ponto de partida para qualquer microsserviço Spring — antes de qualquer métrica de negócio, garanta que Rate, Errors e Duration estão no painel.

### USE para recursos

O método **USE** olha para os **recursos** que sustentam o serviço (CPU, memória, threads, pool de conexões, fila de mensagens):

- **Utilization** — quanto do recurso está em uso (ex.: 70% das conexões do pool ocupadas).
- **Saturation** — quanto de trabalho está **enfileirado** esperando o recurso (ex.: threads bloqueadas aguardando conexão).
- **Errors** — eventos de erro do próprio recurso (ex.: timeouts ao adquirir conexão).

RED e USE são complementares: RED diz *que o serviço está lento*; USE diz *por quê* — frequentemente é um recurso saturado (pool de conexões esgotado, CPU no teto, GC tomando tempo).

### Alerting, SLO e SLI

Sobre os mesmos dados, o Grafana (ou o Alertmanager do Prometheus) avalia **regras de alerta**: uma expressão PromQL que, ao virar verdadeira por um período, dispara notificação.

A disciplina que dá rigor a isso é a de **SLO/SLI**:

- **SLI** (*Service Level Indicator*) — a métrica que mede a qualidade percebida, ex.: "% de requests com latência < 300 ms".
- **SLO** (*Service Level Objective*) — a meta sobre o SLI, ex.: "99,9% dos requests abaixo de 300 ms ao longo de 30 dias".

A regra prática (Google SRE): **alerte sobre sintoma, não sobre causa**. Em vez de alertar "CPU acima de 80%" (que pode ser inofensivo), alerte "SLO de latência sendo queimado rápido demais" — porque é isso que o usuário sente.

## Na prática

Como se monta um dashboard RED para um serviço Spring chamado `order-service`. As queries abaixo são **ilustrativas** (os números são exemplos de threshold, não dados medidos):

**Rate — requisições por segundo, por status:**

```promql
sum(rate(http_server_requests_seconds_count{application="order-service"}[5m])) by (status)
```

**Duration — latência p95 (a partir de um histograma):**

```promql
histogram_quantile(
  0.95,
  sum(rate(http_server_requests_seconds_bucket{application="order-service"}[5m])) by (le)
)
```

**Errors — proporção de respostas 5xx:**

```promql
sum(rate(http_server_requests_seconds_count{application="order-service", status=~"5.."}[5m]))
/
sum(rate(http_server_requests_seconds_count{application="order-service"}[5m]))
```

> [!note] De onde vêm essas métricas
> `http_server_requests_seconds_*` é o que o **Micrometer** expõe automaticamente para controllers Spring MVC/WebFlux (timer com buckets de histograma). É por isso que a nota 14 vem antes: o Grafana só desenha o que o Micrometer instrumentou.

Estrutura típica de um dashboard de serviço — uma linha RED no topo, uma linha USE abaixo:

```text
Dashboard: order-service
├── Linha 1 — RED (visão do request)
│   ├── Painel: Request rate (req/s) por status
│   ├── Painel: Latência p50 / p95 / p99
│   └── Painel: Taxa de erro 5xx (%)  ← com alerta vinculado
├── Linha 2 — USE (visão dos recursos)
│   ├── Painel: Pool de conexões — uso vs. máximo (HikariCP)
│   ├── Painel: Threads ativas / saturação (fila de espera)
│   └── Painel: JVM heap + tempo de GC
└── Linha 3 — Negócio (opcional, depois do RED/USE)
    └── Painel: Pedidos confirmados por minuto
```

## Armadilhas

### (1) O dashboard que ninguém olha

Painéis bonitos não são monitoramento. Um dashboard com 40 gráficos coloridos que ninguém abre durante um incidente é decoração. Sintoma: ninguém sabe dizer qual painel responde "o serviço está saudável?". **Antídoto:** comece pelo RED em uma única linha visível; se um painel não muda uma decisão, ele não merece estar ali.

### (2) Alertas ruidosos e fadiga de alerta (*alert fatigue*)

Alertar demais é pior que alertar de menos. Quando todo alerta dispara sem que nada esteja realmente quebrado, a equipe aprende a **ignorar** — e o alerta de verdade se perde no ruído. Alertas sobre causa ("CPU > 80%", "uma instância reiniciou") são os maiores ofensores. **Antídoto:** alertar sobre **sintoma com impacto no usuário** (SLO sendo queimado), poucos e acionáveis; cada alerta deve responder "o que eu faço agora?".

### (3) Medir *vanity metrics* em vez de RED/USE

Total acumulado de requests desde o boot, número bruto de usuários, contadores que só sobem — números que parecem importantes mas não guiam nenhuma ação. Eles dão sensação de controle sem fornecer diagnóstico. **Antídoto:** todo painel operacional deve mapear para RED (serviço) ou USE (recurso); métrica de negócio entra **depois**, não no lugar.

## Em entrevista

### Frase pronta (inglês)

> Grafana is the visualization layer on top of Prometheus: it doesn't store metrics, it queries them with PromQL and turns time series into dashboards and alerts. To decide *what* to put on a dashboard, I lean on two methods — the RED method (Rate, Errors, Duration) for services, and the USE method (Utilization, Saturation, Errors) for resources. For a Spring service, that means request rate, p95/p99 latency, 5xx error ratio, and connection-pool saturation. And when it comes to alerting, I follow the SRE principle of alerting on symptoms tied to an SLO rather than on raw causes — otherwise you get alert fatigue and the team starts ignoring the pages.

### Vocabulário

| Português | Inglês |
| --- | --- |
| painel | dashboard / panel |
| alerta | alert |
| taxa, erros e duração | RED method (Rate, Errors, Duration) |
| utilização, saturação e erros | USE method (Utilization, Saturation, Errors) |
| percentil (p95/p99) | percentile |
| fadiga de alerta | alert fatigue |
| fonte de dados | data source |
| objetivo de nível de serviço | SLO (Service Level Objective) |
| indicador de nível de serviço | SLI (Service Level Indicator) |
| consulta | query |

## Veja também

- [[03-Dominios/Java/Cloud-native e produção/14 - Métricas em produção — Micrometer e Prometheus|Métricas em produção]]
- [[03-Dominios/Java/Cloud-native e produção/16 - OpenTelemetry Collector e sampling de produção|OpenTelemetry Collector e sampling]]
- [[03-Dominios/Java/Cloud-native e produção/18 - Profiling e diagnóstico sob carga — produção|Profiling e diagnóstico sob carga]]
- [[03-Dominios/Java/Cloud-native e produção/index|Cloud-native e produção (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]

## Referências

- Grafana — visão geral do produto e linha 13.x. https://grafana.com/oss/grafana/
- Prometheus — best practices (naming, histograms, instrumentation, alerting). https://prometheus.io/docs/practices/
- Tom Wilkie — *The RED Method*: métricas-chave para serviços (Rate, Errors, Duration). https://grafana.com/blog/2018/08/02/the-red-method-how-to-instrument-your-services/
- Brendan Gregg — *The USE Method*: Utilization, Saturation, Errors para recursos. https://www.brendangregg.com/usemethod.html
- Google SRE Book — *Service Level Objectives* e alerting sobre sintoma. https://sre.google/sre-book/service-level-objectives/
