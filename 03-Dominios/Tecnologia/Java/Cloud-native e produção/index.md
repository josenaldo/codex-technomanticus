---
title: "Cloud-native e produção"
created: 2026-06-12
updated: 2026-06-12
type: moc
status: growing
publish: true
tags:
  - java
  - cloud-native
  - moc
aliases:
  - "Cloud-native e produção"
  - "Cloud-native"
  - "Produção"
  - "Containers e Kubernetes"
  - "GraalVM Native Image"
  - "Observabilidade de operação"
  - "Galho 17 - Cloud-native e produção"
---

# Cloud-native e produção

> [!abstract] TL;DR
> Este galho fecha o ciclo: pega o `jar` que os galhos anteriores produziram e o leva **a produção, num cluster** — empacotamento em imagem (Dockerfile, Buildpacks, Jib), a JVM ciente do container, GraalVM Native Image, o contrato com o Kubernetes (probes, config, graceful shutdown), a observabilidade de operação (métricas, traces, logs), profiling sob carga e o pipeline de CI/CD. A tese que atravessa tudo: **"production-ready" não é uma feature que se liga, é uma sequência de contratos** — com o build, com a JVM, com o orquestrador, com o coletor de observabilidade. Cada nota é uma estação dessa linha de montagem. São **22 notas em 3 fases** (Iniciado, Adepto, Magus).

## Sobre este galho

A audiência é o desenvolvedor **pleno avançando para senior**, preparando-se para entrevista internacional de plataforma/SRE, que precisa não só "fazer subir no Kubernetes" mas **defender cada decisão**: por que distroless, por que `MaxRAMPercentage` e não `-Xmx`, quando native vale o trade-off, por que readiness e liveness são contratos distintos, e onde o trace daquele pod vai parar.

Este é o **último galho do bloco de plataforma distribuída e produção**. A **fronteira-assinatura é sêxtupla** — este galho **linka, não re-explica**:

- **Galho 3 (JVM)** — a mecânica interna de heap, GC, JFR, heap/thread dumps e tuning. Aqui só se decide **quanto** heap a JVM se concede do cgroup e **quando** disparar cada sinal; o **como** ler é lá.
- **Galho 8 (Spring Core e Boot)** — o Actuator e seus endpoints de saúde/métricas. Aqui se usa o Actuator como fachada; sua configuração-base é lá.
- **Galho 15 (Build e tooling)** — empacotamento do jar (fat/thin/layered) e supply chain/SBOM. Aqui se consome o layered jar e se escaneia a imagem; a mecânica de build é lá.
- **Galho 16 (Microservices)** — o tracing distribuído no código (spans, correlação). Aqui se opera o **stack** que recebe esse trace (Collector, sampling); a instrumentação em código é lá.
- **Galho 13 (Testes)** — JMH e microbenchmark. Aqui o profiling de produção é o contraponto operacional; o benchmark controlado é lá.
- **Galho 6 (JavaFX)** — empacotamento desktop (jlink, jpackage). Paralelo conceitual de "imagem auto-contida", mas para outro alvo.

## Iniciado

- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/01 - Production-ready e cloud-native — a tese honesta|Production-ready e cloud-native — a tese honesta]] — o que "pronto para produção" realmente significa e por que é uma sequência de contratos, não um checkbox.
- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/02 - A JVM dentro de um container|A JVM dentro de um container]] — container-awareness, cgroup, `MaxRAMPercentage` vs `-Xmx` fixo e o OOM-kill.
- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/03 - Empacotando o app numa imagem — o panorama|Empacotando o app numa imagem — o panorama]] — o mapa das três formas de virar imagem (Dockerfile, Buildpacks, Jib) antes do detalhe de cada uma.

## Adepto

- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/04 - Dockerfile na prática — multi-stage e layered jar|Dockerfile na prática — multi-stage e layered jar]] — multi-stage, extração do layered jar (`jarmode=tools`) e cache eficiente de camadas.
- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/05 - Imagem enxuta e segura — distroless e scanning|Imagem enxuta e segura — distroless e scanning]] — bases distroless, usuário não-root e scan de CVE no pipeline.
- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/06 - Buildpacks — imagem sem Dockerfile|Buildpacks — imagem sem Dockerfile]] — Cloud Native Buildpacks/Paketo via `spring-boot:build-image`, convenção sobre configuração.
- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/07 - Jib — imagem daemonless|Jib — imagem daemonless]] — construir imagem sem Docker daemon, ideal para CI.
- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/08 - GraalVM Native Image — conceito e trade-offs|GraalVM Native Image — conceito e trade-offs]] — compilação AOT closed-world, o que se ganha (startup, footprint) e o que se perde.
- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/09 - Native Image com Spring — Spring AOT na prática|Native Image com Spring — Spring AOT na prática]] — Spring AOT, hints de reflexão/proxy e `native:compile`.
- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/10 - Health e probes — o contrato com o orquestrador|Health e probes — o contrato com o orquestrador]] — liveness vs readiness como contratos distintos com o Kubernetes.
- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/11 - Config e recursos no Kubernetes|Config e recursos no Kubernetes]] — ConfigMap/Secret → env, e `requests`/`limits` casados com o heap da JVM.
- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/12 - Graceful shutdown e deploy sem downtime|Graceful shutdown e deploy sem downtime]] — drenar conexões no SIGTERM, `preStop` e `terminationGracePeriodSeconds`.
- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/13 - Observabilidade de operação — o panorama e os 3 seams|Observabilidade de operação — o panorama e os 3 seams]] — os três sinais (métrica, trace, log) e onde cada seam (G3/G16/G17) começa e termina.
- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/14 - Métricas em produção — Micrometer e Prometheus|Métricas em produção — Micrometer e Prometheus]] — Micrometer como fachada, `/actuator/prometheus` e o modelo de scraping.
- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/15 - Dashboards e alertas — Grafana|Dashboards e alertas — Grafana]] — visualizar as métricas e disparar alertas sobre elas.
- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/16 - OpenTelemetry Collector e sampling de produção|OpenTelemetry Collector e sampling de produção]] — operar o stack que recebe o trace; head vs tail sampling.
- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/17 - Logs estruturados em produção|Logs estruturados em produção]] — JSON no stdout, correlação por `traceId` e o coletor de logs.

## Magus

- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/18 - Profiling e diagnóstico sob carga — produção|Profiling e diagnóstico sob carga — produção]] — o workflow de incidente sintoma → sinal → ferramenta, capturando sem derrubar o pod.
- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/19 - Continuous profiling no cluster — Pyroscope e async-profiler|Continuous profiling no cluster — Pyroscope e async-profiler]] — perfilar a frota inteira o tempo todo, com baixo overhead, correlacionado ao trace.
- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/20 - CI-CD e o caminho até produção|CI-CD e o caminho até produção]] — o pipeline que constrói, testa, escaneia, publica e aplica o manifesto sem humano no terminal.
- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/21 - Native vs JVM — a decisão honesta|Native vs JVM — a decisão honesta]] — o trade-off de plataforma decidido por perfil de carga, sem dogma e sem benchmark de blog.
- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/22 - Capstone — do jar ao cluster|Capstone — do jar ao cluster]] — o `order-service` indo a produção ponta a ponta, com tabelas de decisão e cheatsheet problema → nota.

## Rotas alternativas

- **Completa**: 01 → 02 → 03 → 04 → 05 → 06 → 07 → 08 → 09 → 10 → 11 → 12 → 13 → 14 → 15 → 16 → 17 → 18 → 19 → 20 → 21 → 22, em ordem.
- **Entrevista internacional**: 01 (a tese honesta) → 02 (JVM no container) → 08 (native, conceito) → 10 (probes) → 12 (graceful shutdown) → 13 (os 3 seams) → 18 (profiling sob carga) → 21 (native vs JVM) → 22 (capstone ponta a ponta).
- **Empacotamento e imagem**: 03 (panorama) → 04 (Dockerfile) → 05 (distroless e scanning) → 06 (Buildpacks) → 07 (Jib) → 08 (native, conceito) → 09 (Spring AOT).
- **O contrato com o Kubernetes**: 02 (JVM no container) → 10 (probes) → 11 (config e recursos) → 12 (graceful shutdown) → 22 (capstone).
- **Observabilidade e diagnóstico**: 13 (os 3 seams) → 14 (métricas) → 15 (Grafana) → 16 (Collector e sampling) → 17 (logs) → 18 (profiling sob carga) → 19 (continuous profiling).

## Veja também

- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/index|Microservices e sistemas distribuídos (Galho 16)]]
- [[03-Dominios/Tecnologia/Java/Build e tooling/index|Build e tooling (Galho 15)]]
- [[03-Dominios/Tecnologia/Java/JVM/index|JVM (Galho 3)]]
- [[03-Dominios/Tecnologia/Java/Spring Core e Boot/index|Spring Core e Boot (Galho 8)]]
- [[03-Dominios/Tecnologia/Java/Testes/index|Testes (Galho 13)]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java|Dicionário de Java]]

## Notas do galho

```dataview
TABLE fase, status
FROM "03-Dominios/Tecnologia/Java/Cloud-native e produção"
WHERE type = "concept"
SORT file.name ASC
```
