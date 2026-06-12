---
title: "Spec — Galho 17 da trilha Java Senior (Cloud-native e produção)"
date: 2026-06-12
author: Josenaldo
status: draft
type: spec
publish: false
---

# Spec — Galho 17 da trilha Java Senior (Cloud-native e produção)

## 1. Contexto e motivação

Este é o **décimo sétimo galho** da trilha Java Senior (roadmap em `docs/superpowers/specs/2026-06-02-java-senior-roadmap-design.md`, §5, Galho 17). Pressupõe leitura do roadmap (topologia flat, 3 fases Iniciado/Adepto/Magus, padrões editoriais, política de poda). Os Galhos 1 a 16 já fecharam em `main` — seus artefatos são o **template de padrão e qualidade**. É o **último galho do bloco "Plataforma distribuída e produção"** (depois de 14 Mensageria, 15 Build, 16 Microservices) e o **penúltimo da trilha** — só o 18 (OCP) vem depois. O roadmap define dependências: **Galhos 3 (JVM), 8 (Spring), 16 (Microservices)** — e na prática também **15 (Build)**.

**Galho HÍBRIDO (PESQUISA pesada + PODA REVERSA modesta + INTEGRAÇÃO intensa):**

- **Parte PESQUISA (a maior):** o galho cobre **como um serviço Java sai do `jar` e vai para produção num cluster** — containerização (Dockerfile multi-stage, layered jar, Buildpacks/Jib, distroless), **GraalVM Native Image** (AOT, Spring AOT, trade-offs), o **contrato do app com o orquestrador** (health probes, config, resource limits, graceful shutdown), a **observabilidade de operação** (métricas Micrometer/Prometheus/Grafana, OpenTelemetry Collector, sampling de produção, logs estruturados), **profiling sob carga** e **continuous profiling**, e **CI/CD** até o deploy. Quase tudo nasce de doc oficial via WebFetch (ZERO memória): `graalvm.org`, `graalvm.github.io/native-build-tools`, `docs.spring.io/spring-boot`, `buildpacks.io`/`paketo.io`, `github.com/GoogleContainerTools/jib` e `.../distroless`, `micrometer.io`, `prometheus.io`, `grafana.com`, `opentelemetry.io/docs/collector`.

- **Parte PODA REVERSA (modesta):** o pré-flight (2026-06-12) confirmou — apesar de o roadmap dizer "tronco a podar: nenhum" — **dívida reversa real e localizada** no tronco legado `Backend/Spring Boot.md` (`publish: false`, já em poda progressiva): `### Graceful shutdown` (explicação substancial → migra com callout para a nota de graceful shutdown) e `### Memory leak e GC tuning` (heap dump/MAT/GC tuning — quase tudo é território do **Galho 3**, já coberto em notas completas; vira callout apontando G3 para heap/GC + a nota de profiling deste galho). O `## Actuator — production-ready features` já é um callout (migrado ao G8); só precisa ter o parêntese "(... Galho 17, planejado)" trocado por wikilink.

- **Parte INTEGRAÇÃO (assinatura deste galho):** o Galho 17 é o **destinatário de ~23 ganchos "(planejado) Galho 17"** deixados por TODOS os galhos anteriores. Quitar esses ganchos (trocar "(planejado)" por wikilink ativo, mantendo "(planejado)" só onde apontam para o Galho 18) é metade do trabalho. Lista em §3.6.

**A fronteira-assinatura é SÊXTUPLA.** Este galho é o ponto de convergência da trilha de produção — ele *opera* o que os outros galhos *construíram*. Cada nota linka de volta sem re-explicar:

- **Galho 3 (JVM) — o mais importante:** o G3 **já possui notas completas e publicadas** que cobrem o profiling/observabilidade **interna da JVM**: `JVM/13 - JFR e JMC — observabilidade de produção`, `JVM/12 - Diagnóstico — heap dumps, thread dumps e jcmd`, `JVM/10 - GC logs`, `JVM/11 - Tuning de GC`, `JVM/14 - Performance da JVM — síntese`, `JVM/03 - Garbage Collection`. **AOT/JIT e o mecanismo de native image em nível de JVM** também são do G3. As notas 08/18 deste galho **linkam pesado, nunca re-explicam** heap dump, JFR, GC ou o mecanismo AOT.
- **Galho 8 (Spring) — Actuator:** o **mecanismo** do Actuator e da auto-configuration está em `Spring Core e Boot/17 - Actuator e observabilidade`. As notas 10/13/14 deste galho usam o Actuator no ângulo **operacional** (probes em k8s, métricas em produção), linkando o mecanismo.
- **Galho 15 (Build) — empacotamento e SBOM:** `Build e tooling/15 - Empacotamento — fat jar, thin jar e repackage` (o layered jar como artefato de build) e `Build e tooling/18 - Supply chain e SBOM`. As notas 03/04/20 linkam — aqui é a **imagem de container** e o **deploy**, não o build do jar.
- **Galho 16 (Microservices) — tracing e mesh:** `Microservices/18,19 - Tracing distribuído` (correlação no código + config de export) e `Microservices/22 - Service mesh` (conceitual). As notas 13/16 deste galho recebem o **seam** que o G16 deixou explícito: lá é instrumentar/exportar **no código**; aqui é **operar** o coletor/dashboard/sampling de produção e instalar/operar o mesh.
- **Galho 13 (Testes) — JMH:** `Testes/18 - Performance — JMH e microbenchmarks` é microbenchmark de **código isolado**; a nota 18 deste galho é **profiling de produção sob carga real** — linka a distinção.
- **Galho 6 (JavaFX) — jpackage/native desktop:** `JavaFX/13 - Empacotamento — módulos, jlink e jpackage` cobriu native desktop (Gluon Substrate); a nota 08/09 deste galho é **native image de serviço backend** — linka a fronteira.

**O seam de observabilidade é de TRÊS pontas** (a decisão de escopo mais importante do galho, aprovada no brainstorm): **G3** = observabilidade *interna da JVM* (JFR/JMC, heap, GC); **G16** = correlação de trace *no código* (Micrometer Tracing, traceId); **G17** = *operar o stack* no cluster (Micrometer→Prometheus→Grafana, OpenTelemetry Collector, sampling de produção, logs estruturados, continuous profiling). A nota 13 explicita esse seam de três pontas.

**A tese honesta do galho:** "production-ready" é uma **postura, não uma feature** — é o conjunto de contratos que o app honra para ser operável (observável, descartável, configurável de fora, com health declarado). "Cloud-native" aqui é o nível de **deploy/operação** (o Galho 16 foi a *arquitetura* distribuída; este galho é *levar ao cluster e operar*). E **native image é trade-off de plataforma, não upgrade**: ganha startup/footprint em ms (serverless, scale-to-zero, alta densidade) ao custo do JIT especulativo (throughput de pico), de builds lentos e de restrições ao dinamismo — vale quando o startup domina o SLA, não por default.

**O Galho 18 (OCP) ainda não existe** — toda referência permanece texto "(planejado)", sem wikilink.

## 2. Objetivo

Produzir, em uma sessão de execução dedicada, **22 notas atômicas + 1 MOC do galho + expansão do Dicionário de Java + ativação do MOC central (Galho 17) + poda reversa modesta em `Backend/Spring Boot.md` + quitação de ~23 ganchos "(planejado) G17" + cross-links**, em `03-Dominios/Java/Cloud-native e produção/` e `03-Dominios/Java/`, todas `publish: true`, em PT-BR, distribuídas em 3 fases (**3 Iniciado + 14 Adepto + 5 Magus**).

Ao terminar o galho, o leitor deve conseguir:

- **Explicar em inglês** o que torna um serviço "production-ready" (contratos de observabilidade, disposability, config externa, health declarado) e o que "cloud-native" significa no nível de deploy.
- **Containerizar um app Spring com critério**: Dockerfile multi-stage com layered jar, ou Buildpacks (`bootBuildImage`), ou Jib — sabendo o trade-off de cada um; usar imagem enxuta/segura (distroless, non-root); e fazer a **JVM respeitar os limites do container** (`MaxRAMPercentage` em vez de `-Xmx` fixo).
- **Decidir e construir uma Native Image**: entender AOT closed-world, reachability metadata e o Spring AOT engine; saber **quando native vale vs JVM** (serverless/scale-to-zero vs throughput de pico).
- **Honrar o contrato com o Kubernetes**: expor liveness/readiness probes via Actuator, fazer graceful shutdown coordenado com SIGTERM/preStop, ler config de ConfigMap/Secret/env, e declarar resource limits — sabendo ler um Deployment YAML representativo.
- **Operar a observabilidade**: expor métricas (Micrometer→`/actuator/prometheus`), montar dashboards (Grafana), rotear telemetria pelo OpenTelemetry Collector com sampling de produção (head vs tail), e emitir logs estruturados correlacionados por traceId.
- **Diagnosticar produção**: conduzir o workflow de incidente (qual sinal → qual ferramenta → correlacionar), sabendo que heap/thread dump, JFR e GC tuning são do Galho 3 (linka), e usar continuous profiling (Pyroscope/async-profiler) para correlacionar profile↔métrica↔trace.
- **Levar ao deploy**: desenhar um pipeline CI/CD build→test→imagem→deploy com supply chain (SBOM/G15) e estratégia de rollout.

A barra é "levar um serviço Java do `jar` ao cluster e operá-lo em produção com critério — escolhendo empacotamento, runtime (JVM vs native), contrato de orquestração e stack de observabilidade" — não "decorar flags de Docker/k8s". O foco é o **modelo mental + a decisão de engenharia de plataforma**, com snippets corretos como apoio.

## 3. Saídas concretas

### 3.1. Notas (`03-Dominios/Java/Cloud-native e produção/`)

Pasta **nova**, flat. 22 notas + 1 MOC (`index.md`, obrigatório pro folder-link do Quartz). Numeração global por galho (não reinicia por fase). **Nome da pasta no disco: `Cloud-native e produção`** (casa com o título do roadmap; tag de galho sugerida `cloud-native`).

#### Iniciado (3 notas — a tese, a JVM no container, o panorama de empacotamento)

| # | Nota | Escopo nuclear |
|---|------|----------------|
| 01 | "Production-ready" e cloud-native — a tese honesta *(opus, assinatura)* | "Production-ready" = postura/conjunto de contratos (observável, descartável, config externa, health declarado), NÃO feature. "Cloud-native" no nível de **deploy/operação** (a arquitetura é G16 — linka). O lado **build/release/run + disposability + logs-as-streams** dos 12 fatores (a parte de arquitetura é G16 — linka, não repete). **A nota-assinatura:** apresenta os 3 seams do galho (G3 JVM-interno / G16 trace-no-código / G17 operar-o-stack) e a fronteira sêxtupla. Fontes: 12factor.net, docs.spring.io. |
| 02 | A JVM dentro de um container | **Container-awareness**: `-XX:+UseContainerSupport` (default Java 10, lê cgroup), `-XX:MaxRAMPercentage` (default 25.0) / `InitialRAMPercentage` em vez de `-Xmx` fixo, cgroup v2 (desde JDK 17), `-XX:ActiveProcessorCount`. Por que `-Xmx` fixo é frágil (não acompanha o limite do container). Fronteira G3 (GC/heap é lá). Fontes: docs Oracle/OpenJDK, Red Hat developers. |
| 03 | Empacotando o app numa imagem — o panorama | Do `jar` à **imagem OCI**: o **layered jar** (camadas `dependencies`/`spring-boot-loader`/`snapshot-dependencies`/`application`, `layers.idx`) e `java -Djarmode=tools ... extract` (era `layertools` no Boot 2.x); as **3 vias** (Dockerfile à mão, Buildpacks, Jib) em resumo, cada uma apontando sua nota. **Fronteira G15** (o build do jar é lá; aqui é a imagem). Fontes: docs.spring.io (container-images). |

#### Adepto (14 notas — containers, native, contrato k8s, observabilidade de operação)

| # | Nota | Escopo nuclear |
|---|------|----------------|
| 04 | Dockerfile na prática — multi-stage e layered jar | Multi-stage build (builder extrai camadas, runtime copia); `COPY` por camada para cache; base JRE (ex. `bellsoft/liberica-openjre`/`eclipse-temurin`); rodar como **non-root**; `ENTRYPOINT` exec-form. Fontes: docs.spring.io (dockerfiles). |
| 05 | Imagem enxuta e segura — distroless e scanning | **Distroless** (`gcr.io/distroless/java21-debian13` — sem shell/package manager, superfície de ataque reduzida, exec-form obrigatório); non-root; **image scanning** (Trivy/Grype, conceitual); minimizar camadas/CVEs. Fontes: github.com/GoogleContainerTools/distroless. |
| 06 | Buildpacks — imagem sem Dockerfile | **Cloud Native Buildpacks** (spec CNCF: builder/buildpack/lifecycle) + **Paketo** (impl. Java); `spring-boot:build-image`/`bootBuildImage` (desde Boot 2.3, builder default `paketobuildpacks/builder-noble-java-tiny`, **precisa de Docker daemon**), `BP_JVM_VERSION`. Fontes: buildpacks.io, paketo.io, docs.spring.io (maven/gradle plugin). |
| 07 | Jib — imagem daemonless | **Jib** (`com.google.cloud.tools:jib`, v3.5.x): builda imagem OCI **sem Docker daemon e sem Dockerfile**, layering automático (deps vs classes), reproducible; **Buildpacks vs Jib** (lifecycle CNB + daemon vs plugin direto + push). Fontes: github.com/GoogleContainerTools/jib. |
| 08 | GraalVM Native Image — conceito e trade-offs *(opus)* | **GraalVM 25** (GFTC Oracle / GPLv2+CPE Community; JDK 21/24/25); **Native Image** = AOT **closed-world** (só código alcançável a partir do `main`); **reachability metadata** (`reachability-metadata.json`, era "reflection config"; Tracing Agent; Reachability Metadata Repository) para reflection/proxies/resources/serialization. Trade-offs: startup/footprint em ms vs **sem JIT** (sem otimização especulativa de pico), build lento, restrições ao dinamismo. **Fronteira G3** (AOT/JIT como mecanismo de JVM — linka `JVM/01`/`JVM/07`/`JVM/14`). Fontes: graalvm.org. |
| 09 | Native Image com Spring — Spring AOT na prática | **Spring AOT engine** (desde Boot 3.0, nov/2022): em build-time gera `*__BeanDefinitions` estáticos + hints sob `META-INF/native-image/`; **`RuntimeHintsRegistrar`** / `@RegisterReflectionForBinding`; limitações (`@Profile`/`@ConditionalOnProperty` em runtime). **Dois caminhos**: `native-build-tools` 1.1.2 (`native:compile`/`nativeCompile`, exige GraalVM local) vs Buildpacks `BP_NATIVE_IMAGE=true` (no container). Fontes: docs.spring.io (native-image), graalvm.github.io/native-build-tools. |
| 10 | Health e probes — o contrato com o orquestrador | **Actuator** (mecanismo é G8 — linka `Spring Core e Boot/17`): `/actuator/health`, exposição (`management.endpoints.web.exposure.include`); **probes k8s** (`management.endpoint.health.probes.enabled` default true, auto em k8s; `/actuator/health/liveness` + `/readiness`; `ApplicationAvailability`/`LivenessState`/`ReadinessState`); **sem startup probe dedicado** (reusa liveness); `add-additional-paths` → `/livez`/`/readyz`; estados UP/DOWN/OUT_OF_SERVICE (503). Liveness não depende de check externo. Fontes: docs.spring.io (actuator/endpoints). |
| 11 | Config e recursos no Kubernetes | Config externa: env vars, **ConfigMap/Secret** mapeados pro `application.yml`/env (12-factor config no ambiente — linka nota 01); **resource limits** (requests/limits) e a relação com `MaxRAMPercidentage` (nota 02); **o Deployment YAML ilustrativo** (probes + resources + env) — a ótica do app que CONSOME o contrato, **sem ensinar operar cluster** (kubectl/Service/Ingress/operators = fora de escopo). Secrets management operacional/Vault = menção de fronteira. Fontes: docs.spring.io, kubernetes.io (probes — só referência). |
| 12 | Graceful shutdown e deploy sem downtime | **`server.shutdown=graceful`** (default no Boot), `spring.lifecycle.timeout-per-shutdown-phase` (30s); coordenação com **SIGTERM + preStop hook** (race condition de roteamento; `terminationGracePeriodSeconds`); readiness vira **`REFUSING_TRAFFIC`** (→ OUT_OF_SERVICE/503) no shutdown; `@PreDestroy`. **Deploy sem downtime**: rolling vs blue-green vs canary (conceitual). **Recebe a poda do `### Graceful shutdown`.** Fontes: docs.spring.io (graceful-shutdown, cloud deployment). |
| 13 | Observabilidade de operação — o panorama e os 3 seams *(opus)* | Os **3 pilares** (métricas, logs, traces). **O seam de TRÊS pontas** (a nota-chave): **G3** observabilidade interna da JVM (JFR/heap/GC — linka), **G16** correlação de trace no código (linka), **G17** operar o stack no cluster (esta tríade de notas 14-17). **Actuator** como a ponte app↔ferramentas (mecanismo é G8 — linka). Fontes: micrometer.io, docs.spring.io, opentelemetry.io. |
| 14 | Métricas em produção — Micrometer e Prometheus | **Micrometer 1.17.x** ("SLF4J para métricas/observability facade"), os **registries** (Prometheus, OTLP…); **`/actuator/prometheus`** (precisa `micrometer-registry-prometheus`); **Prometheus 3.12** = modelo **pull/scrape** sobre HTTP (`scrape_configs` com `metrics_path: /actuator/prometheus`); counters/gauges/timers/histograms (conceito). Fontes: micrometer.io, prometheus.io, docs.spring.io (metrics). |
| 15 | Dashboards e alertas — Grafana | **Grafana 13** = visualização/dashboards sobre Prometheus; os métodos **RED** (Rate/Errors/Duration) e **USE** (Utilization/Saturation/Errors); alerting (conceitual); SLO/SLI (menção). Fontes: grafana.com, prometheus.io. |
| 16 | OpenTelemetry Collector e sampling de produção *(opus)* | **OTel Collector v0.154** = componente **SEPARADO do app** (receivers → processors → exporters; OTLP in/out); a distinção **instrumentação no app** (Micrometer/OTel SDK gera o dado — G16) **vs Collector** (recebe/roteia, fora do app). **Sampling**: **head-based** (cedo, no SDK/app) vs **tail-based** (no Collector stateful, depois do trace completo — mantém traces com erro/lentidão). **Recebe o seam do G16** (notas 18/19 lá são código/config; aqui é operar). Fontes: opentelemetry.io/docs/collector, /docs/concepts/sampling. |
| 17 | Logs estruturados em produção | **Structured logging nativo desde Boot 3.4** (`logging.structured.format.console=ecs`; formatos ECS/GELF/Logstash JSON); **correlação traceId/spanId via MDC** (com tracing ativo — linka G16); agregação (Loki/ELK, conceitual). Por que JSON > texto em produção (parse/query/pivot log↔trace). Fontes: docs.spring.io (logging), spring.io/blog. |

#### Magus (5 notas — diagnóstico, profiling, deploy, decisão, capstone)

| # | Nota | Escopo nuclear |
|---|------|----------------|
| 18 | Profiling e diagnóstico sob carga — produção | O **workflow de incidente em produção** (qual sintoma → qual sinal → qual ferramenta → correlacionar com o stack de obs). Heap dump, thread dump, GC log sob carga real, JFR contínuo — **tudo isso é mecânica do Galho 3 (linka pesado `JVM/12`/`JVM/13`/`JVM/10`/`JVM/11`), NÃO re-explica**; aqui é o **ângulo operacional/cluster** (como esses sinais entram na rotina de produção). **Distinção com JMH/G13** (microbenchmark de código ≠ profiling de produção). Fontes: docs.spring.io, JVM notes (link-back). |
| 19 | Continuous profiling no cluster — Pyroscope e async-profiler | O **4º sinal emergente**: profiling **contínuo** de toda a frota. **Grafana Pyroscope 2.x** (multi-tenant; usa **async-profiler** por baixo para Java; saída JFR); **correlacionar profile↔métrica↔log↔trace** ("flamegraph do span lento"). Distinto do JFR local (G3): aqui é agregação distribuída na plataforma. Fontes: grafana.com/docs/pyroscope, github async-profiler. |
| 20 | CI/CD e o caminho até produção | O **pipeline** build→test→imagem→deploy; o gate de qualidade (quality gates/G15 linka), **supply chain no deploy** (assinar imagem, SBOM — linka `Build/18`); **GitOps** (conceitual, sem ferramenta específica); estratégias de deploy (recap rolling/blue-green/canary da nota 12). Fontes: docs (conceitual), buildpacks/jib para o passo de imagem. |
| 21 | Native vs JVM — a decisão honesta *(opus)* | O framework de decisão com tudo na mão: **quando native vale** (serverless/FaaS, scale-to-zero, CLI, alta densidade, startup domina o SLA) **vs quando JVM tradicional vence** (throughput de pico via JIT, build rápido, dinamismo/agentes, libs sem metadata); o custo de build/CI da native; o trade-off de plataforma (não upgrade). **Sem dogma** — "quando X E quando Y". Fontes: graalvm.org, docs.spring.io, JVM/14 (link). |
| 22 | Capstone — do jar ao cluster *(opus, síntese)* | **Um serviço Spring levado a produção ponta a ponta**: layered jar → imagem (Dockerfile/Buildpacks/Jib) → JVM container-aware → probes + graceful shutdown → Deployment YAML → métricas/Prometheus/Grafana + trace/Collector + logs estruturados → CI/CD. **Tabela de decisão** (Dockerfile vs Buildpacks vs Jib; JVM vs native; head vs tail sampling; quando cada coisa). **Cheatsheet nota→problema** (títulos EXATOS das 22 notas). Munição de entrevista de plataforma/SRE. Fontes: docs.spring.io. |

**Notas opus (6):** 01 (assinatura/tese), 08 (native conceito — denso, version-heavy), 13 (panorama/seam de 3 pontas — conceitualmente central), 16 (Collector/sampling — nuançado), 21 (native vs JVM — decisão), 22 (capstone — síntese). As demais → sonnet. **Quase todas as notas são version-specific** e fazem WebFetch no Step 1 (§4.3.3 e §6).

**Decisões de fronteira (escopo de outro dono — link-back ou texto "(planejado)"):**
- **JFR/JMC, heap/thread dump, GC log, GC tuning, JVM performance, o mecanismo AOT/JIT** → Galho 3. As notas 02/08/18 linkam (`JVM/13`/`/12`/`/11`/`/10`/`/14`/`/07`/`/01`) — **nunca re-explicam**.
- **Mecanismo do Actuator / auto-configuration** → Galho 8 (`Spring Core e Boot/17`). Notas 10/13/14 usam no ângulo operacional.
- **Empacotamento do jar (fat/thin/layered como artefato de build), SBOM, quality gates** → Galho 15 (`Build/15`, `/18`, `/16`). Notas 03/04/20 linkam; aqui é imagem e deploy.
- **Tracing/correlação no código (Micrometer Tracing, traceId), service mesh conceitual** → Galho 16 (`Microservices/18`, `/19`, `/22`). Notas 13/16 recebem o seam.
- **JMH microbenchmark** → Galho 13 (`Testes/18`). Nota 18 distingue.
- **jpackage / native desktop** → Galho 6 (`JavaFX/13`). Notas 08/09 linkam a fronteira.
- **Operar cluster Kubernetes** (kubectl, Service/Ingress, networking, operators, HPA), **operar Istio/Linkerd**, **operar Vault/secrets management** → fora de escopo (DevOps/infra puro); menção de fronteira, sem aprofundar. O galho cobre o **contrato do app** + um Deployment YAML ilustrativo.
- **OCP** → Galho 18 (planejado).

### 3.2. MOC do galho

`03-Dominios/Java/Cloud-native e produção/index.md`:
- `type: moc`, `status: growing`, `publish: true`, `created`/`updated: 2026-06-12`
- Frontmatter padrão (`title: "Cloud-native e produção"`, tags `java`/`cloud-native`/`moc`, aliases `["Cloud-native e produção", "Cloud-native", "Produção", "Containers e Kubernetes", "GraalVM Native Image", "Observabilidade de produção", "Galho 17 - Cloud-native"]`)
- `> [!abstract] TL;DR` — 2-4 linhas: o galho cobre levar um serviço Java do `jar` ao cluster e operá-lo (containers, native image, contrato k8s, observabilidade de operação, profiling, CI/CD); a tese (production-ready = postura, não feature; native = trade-off de plataforma); **22 notas em 3 fases**
- "Sobre este galho" + audiência + nota de que é galho **HÍBRIDO** (pesquisa + poda reversa modesta do `Spring Boot.md` + **integração intensa**: quita ~23 ganchos) + a **fronteira-assinatura sêxtupla** e o **seam de observabilidade de 3 pontas** (G3/G16/G17)
- 3 H2 (`## Iniciado` / `## Adepto` / `## Magus`) com wikilinks pras 22 notas (1 linha descritiva cada — títulos EXATOS)
- **Rotas alternativas (5):**
  - **Completa** — 01 → 22 em ordem
  - **Entrevista internacional** — 01 → 02 → 08 → 10 → 12 → 13 → 16 → 21 → 22
  - **Containerização** — 02 → 03 → 04 → 05 → 06 → 07
  - **Native image** — 08 → 09 → 21
  - **Observabilidade de operação** — 13 → 14 → 15 → 16 → 17 → 18 → 19
- "Veja também": MOC central `[[03-Dominios/Java/index|Trilha Java]]`, **G3** (JVM/JFR/GC), **G8** (Actuator), **G15** (Build/SBOM), **G16** (Microservices/tracing/mesh), **G13** (Testes/JMH), Dicionário; Galho 18 (OCP) como texto "(planejado)" sem wikilink
- Dataview "Todas as notas do galho" (TABLE fase/status; **inline code/DQL nunca começa com `=`** — memória `feedback_dataview_inline_code`)

### 3.3. Dicionário de Java (EXPANSÃO — não recriar)

`03-Dominios/Java/Dicionário de Java.md` já existe (**524 verbetes** após o Galho 16, `type: glossary`, seções `## A`…`## Z` com verbetes `### `). Este galho **expande** inserindo verbetes **em ordem alfabética case-insensitive (sem acento, ignorando símbolos)** nas seções de letra apropriadas. **Nunca recriar nem reordenar.** Atualizar `updated: 2026-06-12`.

Verbetes a inserir (~35, conferir dups antes via grep):

`AOT compilation (native)`, `async-profiler`, `blue-green deployment`, `bootBuildImage`, `canary deployment`, `cgroup (container)`, `Cloud Native Buildpacks`, `container image (OCI)`, `container-awareness (JVM)`, `continuous profiling`, `distroless`, `Dockerfile (multi-stage)`, `GitOps`, `GraalVM`, `GraalVM Native Image`, `graceful shutdown`, `Grafana`, `head-based sampling`, `health probe (liveness/readiness)`, `Jib`, `layered jar`, `liveness probe`, `MaxRAMPercentage`, `OpenTelemetry Collector`, `Paketo Buildpacks`, `Prometheus`, `reachability metadata`, `readiness probe`, `RED method`, `rolling deployment`, `Spring AOT`, `structured logging`, `tail-based sampling`, `USE method`, `UseContainerSupport`.

Cada verbete: definição curta (1-3 linhas) PT-BR + `Veja também:` apontando pra(s) nota(s) canônica(s) do galho. **Conferir dups via grep** — colisões conhecidas do pré-flight (LINKAR, não duplicar): `heap dump`, `JFR (Java Flight Recorder)` (G3); `Micrometer Observation API`, `Micrometer Tracing`, `OpenTelemetry`, `OTLP`, `sidecar` (G16); `SBOM (Software Bill of Materials)` (G15); `twelve-factor (12-factor)` (G16). Conferir também `AOT` (pode existir do G3 — se sim, complementar com o ângulo native image, não duplicar). **Conferir 1:1** que headings batem com âncoras `[[Dicionário de Java#...]]` usadas nas notas.

### 3.4. MOC central (ativação do Galho 17)

`03-Dominios/Java/index.md` já existe. Task **mínima**: trocar a linha do Galho 17 (atualmente, **linha 17 do bloco** — confirmar na execução; hoje `17. Cloud-native e produção *(planejado)* — containers, GraalVM native, Micrometer/OpenTelemetry, profiling`) por wikilink ativo:

```markdown
17. [[03-Dominios/Java/Cloud-native e produção/index|Cloud-native e produção]] — levar um serviço Java do jar ao cluster e operá-lo: containerização (Dockerfile multi-stage, layered jar, Buildpacks/Jib, distroless), GraalVM Native Image (AOT, Spring AOT, trade-offs), o contrato do app com o Kubernetes (health probes, config, graceful shutdown, resource limits), observabilidade de operação (Micrometer/Prometheus/Grafana, OpenTelemetry Collector, sampling, logs estruturados), profiling sob carga e continuous profiling, e CI/CD
```

Atualizar `updated` para `2026-06-12` (já é, mas confirmar). Não mexer no resto. **Confirmar o número da linha na execução.** Galho 18 permanece `*(planejado)*`.

### 3.5. Poda reversa em `Backend/Spring Boot.md` (modesta, com callout)

Política: a explicação **canônica** passa a viver no galho 17 / Galho 3; no tronco fica um **callout `> [!nota] Migrado para galho próprio` + wikilink(s)**, espelhando o tratamento já dado a WebFlux/Spring Cloud/Resilience4j no mesmo arquivo.

| # | Seção (linha aprox., confirmar via grep) | Conteúdo | Ação |
|---|---|---|---|
| 1 | `### Graceful shutdown` (~510-534) | `server.shutdown=graceful`, `timeout-per-shutdown-phase`, `@PreDestroy` | **Substituir** por callout → nota **12** (graceful shutdown e deploy sem downtime). |
| 2 | `### Memory leak e GC tuning` (~475-504) | heap dump, MAT/VisualVM, G1/ZGC tuning, monitorar via Actuator | **Substituir** por callout → **Galho 3** (`JVM/12 - Diagnóstico`, `JVM/11 - Tuning de GC`) para heap/GC + nota **18** deste galho (profiling em produção). NÃO re-explicar GC — é do G3. |
| 3 | `## Actuator — production-ready features` (~88-91, já é callout) | parêntese "(Observabilidade distribuída… Galho 17, planejado)" | Trocar o "(… Galho 17, planejado)" por wikilink ativo pra nota **13** (observabilidade de operação). |

**NÃO TOCAR** (não são G17): `### Connection pool exausto`, `### N+1 queries`, `### LazyInitializationException`, `### @Transactional: problemas sutis` (G8/G10, já cobertos), `### Database migrations seguras (Flyway)` (G10), `### API timeout`/`### Distributed tracing` (já são callouts do G16), `## Camadas típicas`/`### Persistência`/`### Bean Validation`. **Confirmar todos os números de linha via grep na execução.**

### 3.6. Quitação de ganchos "(planejado) G17" + cross-links (após as notas existirem)

O pré-flight achou **~23 arquivos** com gancho "(planejado) Galho 17". **Quitar os substantivos** trocando "(planejado)" por wikilink ativo; manter "(planejado)" onde apontar para o Galho 18. Grupos:

| Tema | Arquivos (linha a confirmar via grep) | Nota-alvo |
|---|---|---|
| Containers/native image | `Build e tooling/09 - Distribuições do JDK` (GraalVM/AOT), `Build e tooling/15 - Empacotamento` (layered jar em imagem), `Build e tooling/index`, `Spring Core e Boot/16 - SpringApplication` (native + tuning de servidor), `JVM/01 - A JVM`, `JVM/14 - Performance da JVM — síntese`, `JavaFX/13 - Empacotamento` (native desktop — fronteira inversa) | notas 08/09 (native), 03/04 (imagem) |
| Observabilidade de operação | `Microservices/18`, `/19` (coletor/dashboard/sampling), `/21` (operar resiliência), `/22` (operar mesh), `Mensageria/26 - Observabilidade em mensageria`, `Testes/18 - Performance — JMH` (profiling de produção), `Spring Core e Boot/17 - Actuator e observabilidade` | notas 13/16/18/19 |
| k8s/secrets | `Microservices/07 - Discovery` (operar k8s), `Microservices/12 - Config centralizado` (Vault operacional), `Segurança/index` (secrets/cloud security) | notas 10/11 |
| Índices/genéricos | `Web e APIs REST/index`, `Microservices/index`, `Microservices/01`, `Testes/21 - Capstone` | MOC do galho |
| Tronco | `Backend/Spring Boot.md` | §3.5 (poda) |

**Conservador:** o grosso da ligação é **das notas novas → notas-fronteira** (sempre). Cross-links de volta só nos ganchos explícitos acima. **Não inflar** notas fechadas. Galho 18 permanece texto "(planejado)" em todo lugar; horizonte-lists genéricos intactos.

## 4. Convenções por nota

Herda §7 do roadmap e §4 dos specs dos galhos de pesquisa (5/7/11/14/15/16). Reforços específicos:

### 4.1. Frontmatter

```yaml
---
title: "<título>"
created: 2026-06-12
updated: 2026-06-12
type: concept
status: seedling
publish: true
fase: iniciado | adepto | magus
tags:
  - java
  - cloud-native
  - <fase>
  - <tags específicas: container, docker, kubernetes, native-image, graalvm, observabilidade, prometheus, grafana, opentelemetry, profiling, ci-cd, deploy, actuator, ...>
aliases:
  - <aliases opcionais>
---
```

H1 `# Título` após o frontmatter.

### 4.2. Estrutura H2 obrigatória

- `> [!abstract] TL;DR` (callout, NÃO H2) — 2-4 linhas: conceito + regra prática + por que importa
- `## O que é` / `## Por que importa` / `## Como funciona` (≥3 subseções H3 em notas Adepto/Magus)
- `## Na prática` — exemplos válidos; framing **neutro** (`com.example`, serviços `order-service`/`payment-service`, imagem `order-service:1.4.2`); "padrão observado em apps Java em produção"; NUNCA `MedEspecialista`/"da minha experiência"/"no meu cluster"/"quando subi em produção"
- `## Armadilhas` — **≥2** (Iniciado) / **≥3** (Adepto/Magus), cada uma com `### (N) Título` (H3 numerado, NÃO callout `[!warning]`) + descrição + exemplo curto + fix em 1 linha
- `## Em entrevista` — `### Frase pronta (inglês)` com **3+ sentenças** (trade-off + decisão + caveat) + `### Vocabulário` com tabela `| Termo PT | Termo EN |` de **6+ termos**
- `## Veja também` — wikilinks **SEM backticks**, **SEM âncoras same-file**; sempre inclui notas relacionadas do galho + `[[03-Dominios/Java/Cloud-native e produção/index|MOC do galho]]` + `[[03-Dominios/Java/index|Trilha Java]]` + (quando aplicável) a nota da fronteira (G3 JVM, G8 Actuator, G15 Build, G16 Microservices, G13 Testes) + verbetes do Dicionário
- `## Referências` — docs oficiais (`graalvm.org`, `docs.spring.io`, `buildpacks.io`/`paketo.io`, `micrometer.io`, `prometheus.io`, `grafana.com`, `opentelemetry.io`)

### 4.3. Restrições absolutas

1. **Fronteira-assinatura (linkar de volta, não re-explicar)** — JFR/heap/GC/GC-tuning/JVM-perf/AOT-JIT-mecanismo → G3; Actuator-mecanismo → G8; empacotamento-do-jar/SBOM/quality-gates → G15; tracing-no-código/service-mesh → G16; JMH → G13; jpackage/native-desktop → G6. **Nunca re-explicar** heap dump, JFR, GC, o mecanismo do Actuator, o build do jar, a instrumentação de trace no código, ou JMH — apontar. Operar cluster/mesh/Vault = fora de escopo (menção). Galho 18 = texto "(planejado)", sem wikilink.
2. **Sem fabricação** de experiência pessoal. Exemplos neutros (`com.example`, `order-service`/`payment-service`, `order-service:1.4.2`) — NUNCA `MedEspecialista`/`josenaldo`/1ª pessoa/"no meu cluster"/"incidente de produção que tive". **Zero estatística de adoção inventada** (ex.: "X% usa Kubernetes/native image"); o pré-flight não achou fonte de market-share → **não citar percentuais de adoção**. Números só com fonte verificável.
3. **Sem invenção** de versões/APIs/comportamentos. WebFetch obrigatório no Step 1 das notas version-specific. **Versões cravadas no pré-flight (2026-06-12) — re-confirmar na execução, mas estes são os fatos-base:**
   - **GraalVM 25** (16/set/2025; JDK 21/24/25; cadência mensal desde 25.1). **Oracle GraalVM = GFTC** (grátis em produção comercial), **Community = GPLv2+CPE**. Honestidade: GraalVM for JDK 24 foi o último sob produtos Oracle Java SE; Oracle desfocou GraalVM como produto Java — **mas Native Image segue mantido** (citar sem drama).
   - **Native Image** = AOT closed-world; **reachability metadata** (`reachability-metadata.json` em `META-INF/native-image/`, antes "reflection config"; Tracing Agent `-agentlib:native-image-agent`; Reachability Metadata Repository como conceito). **native-build-tools 1.1.2** (`org.graalvm.buildtools`): Maven `native:compile`/`native:test`, Gradle `nativeCompile`/`nativeTest`.
   - **Spring AOT desde Spring Boot 3.0** (nov/2022): AOT engine gera `*__BeanDefinitions` + hints (`reflect-config.json` etc.); `RuntimeHintsRegistrar`/`@RegisterReflectionForBinding`; limitações com `@Profile`/`@ConditionalOnProperty` em runtime. Dois caminhos: native-build-tools (GraalVM local) ou Buildpacks `BP_NATIVE_IMAGE=true`.
   - **Spring Boot**: **3.5.x** (último 3.x, OSS support até **30/06/2026**) e **4.0.x** (GA **20/11/2025**, Spring Framework 7, Java 25 com compat 17); doc current 4.1.x. Citar Boot 3.x como baseline, 4.x como recente.
   - **Probes**: `management.endpoint.health.probes.enabled` (default **true**, auto-ativa em k8s), `/actuator/health/liveness` + `/readiness`, `ApplicationAvailability`/`LivenessState`(CORRECT/BROKEN)/`ReadinessState`(ACCEPTING/REFUSING_TRAFFIC). **Não há startup probe dedicado** (reusa liveness). `add-additional-paths` → `/livez`/`/readyz`. Estados health UP/DOWN/OUT_OF_SERVICE/UNKNOWN; DOWN/OUT_OF_SERVICE → **503**.
   - **Graceful shutdown**: `server.shutdown=graceful` é **default no Boot**; `spring.lifecycle.timeout-per-shutdown-phase` default **30s**; readiness → `REFUSING_TRAFFIC` no shutdown; coordenar com **preStop sleep** (race) e `terminationGracePeriodSeconds`.
   - **JVM container**: `-XX:+UseContainerSupport` default **Java 10**; `-XX:MaxRAMPercentage` default **25.0**; cgroup v2 desde **JDK 17/11.0.16/8u372**; `-XX:ActiveProcessorCount`. `-Xmx` fixo tem precedência sobre percentagem (e é frágil).
   - **Imagem**: layered jar (`dependencies`/`spring-boot-loader`/`snapshot-dependencies`/`application`, `layers.idx`), `java -Djarmode=tools ... extract --layers` (Boot 3.x; era `-Djarmode=layertools` no 2.x). **bootBuildImage**/`spring-boot:build-image` desde Boot 2.3 (builder default `paketobuildpacks/builder-noble-java-tiny`, **precisa de daemon**), `BP_JVM_VERSION`/`BP_NATIVE_IMAGE`. **Jib v3.5.x** (daemonless, sem Dockerfile, reproducible). **Distroless** `gcr.io/distroless/java21-debian13` (sem shell, non-root, exec-form). **CNB** = projeto CNCF incubating.
   - **Observabilidade**: **Micrometer 1.17.x** (facade de métricas); **Prometheus 3.12** (pull/scrape, `/actuator/prometheus`); **Grafana 13**; **OpenTelemetry Collector v0.154** (receivers/processors/exporters, separado do app); **head-based vs tail-based sampling** (tail exige Collector stateful); **structured logging nativo desde Boot 3.4** (`logging.structured.format.console=ecs`, ECS/GELF/Logstash, traceId via MDC).
   - **Continuous profiling**: **Grafana Pyroscope 2.x** (usa **async-profiler** para Java; correlaciona profile↔métrica↔trace); distinto do JFR local (G3).
4. **Code samples válidos** — `Dockerfile` (multi-stage real), `application.yml`/`.properties` (Actuator/probes/graceful/structured-logging), Deployment YAML (k8s — probes/resources/env), `pom.xml`/`build.gradle.kts` (native-build-tools/jib/buildpacks com coordenadas reais), `prometheus.yml` (scrape), CLI (`docker`/`java -Djarmode`/`./mvnw native:compile`). Fences corretas: ` ```dockerfile `, ` ```yaml ` (application.yml/k8s/prometheus), ` ```xml `/` ```kotlin ` (build), ` ```bash ` (CLI), ` ```json ` (reachability metadata/logs estruturados), ` ```text ` (diagramas/output). Sempre fechadas. **Usar os nomes/flags cravados** (`-Djarmode=tools`, `MaxRAMPercentage`, `native:compile`).
5. **Comparações justas** — Dockerfile vs Buildpacks vs Jib, JVM vs native image, head vs tail sampling, pull vs push (Prometheus), rolling vs blue-green vs canary, distroless vs base completa: sempre "quando X" E "quando Y". As notas 21 (native vs JVM) e 22 (capstone) são o ápice do julgamento.
6. **Wikilinks sem backticks** em "Veja também"; MOC do galho + MOC central obrigatórios. **Não linkar galho inexistente** (18) — texto "(planejado)". Wikilinks pras notas-fronteira usam **path completo** e o **título EXATO** (conferir 1:1 — lição do Galho 12; os paths de fronteira têm nomes longos com em-dash `—`, ex.: `[[03-Dominios/Java/JVM/13 - JFR e JMC — observabilidade de produção|JFR]]`).
7. **`fase:` no frontmatter + na tag** — obrigatório.
8. **Higiene de commits** — sem `Co-Authored-By: Claude` (memória `feedback_commits`), sem `--no-verify`, `git add <path>` nominal (nunca `-A` — bot de backup Obsidian Git roda em timer), 1 commit por nota/artefato, controlador commita (subagents write-only). Guardar contra `.git/index.lock`.
9. **Tom pedagógico graduado** — Iniciado assume Galhos 1-3/8 (JVM + Spring) e que o leitor já rodou um `jar`; Adepto assume que já fez deploy de algo e quer fazer direito; Magus assume o stack inteiro + a tese (production-ready é postura; native é trade-off; observabilidade é três pontas).
10. **Registro Feynman onde couber** (memória `feedback_enriquecimento_feynman`): analogias pro abstrato (container-awareness = "a JVM que enfim lê o tamanho do quarto onde mora"; layered jar = "bagagem despachada em malas que mudam de peso em ritmos diferentes"; liveness vs readiness = "estou vivo?" vs "posso atender agora?"; native image = "tirar a foto do prédio pronto vs filmar a construção"; tail-based sampling = "decidir guardar a gravação depois de ver como o jogo terminou"), perguntas retóricas, callouts. Sem inflar.

## 5. Conteúdo por nota (síntese)

Notas de pesquisa fundadas em doc oficial via WebFetch. Fontes-base: `graalvm.org/latest/reference-manual/native-image`, `graalvm.github.io/native-build-tools`, `docs.spring.io/spring-boot/reference` (packaging/container-images, packaging/native-image, actuator, web/graceful-shutdown, features/logging), `buildpacks.io`, `paketo.io`, `github.com/GoogleContainerTools/jib` + `/distroless`, `micrometer.io`, `prometheus.io`, `grafana.com`, `opentelemetry.io/docs/collector` + `/docs/concepts/sampling`, `developers.redhat.com` (container-awareness).

(Escopo nuclear de cada nota nas tabelas de §3.1. Cada nota version-specific faz WebFetch no Step 1 e crava as versões de §4.3.3.)

## 6. Pré-flight: verificações feitas

Executado na fase de pré-flight + brainstorming (2026-06-12); itens version-specific re-confirmados na execução de cada nota via WebFetch:

1. **Estrutura da trilha confirmada** — MOC central é `03-Dominios/Java/index.md`; Galho 17 listado como `*(planejado)*` na linha 17 do bloco "Plataforma distribuída e produção". Template de MOC/nota = Galhos 14/15/16.
2. **Galho HÍBRIDO confirmado** — pesquisa pesada + poda reversa modesta em `Backend/Spring Boot.md` (`### Graceful shutdown`, `### Memory leak e GC tuning`; o `## Actuator` já é callout) + **integração intensa** (~23 ganchos "(planejado) G17").
3. **🔴 Achado que moldou o escopo:** o **Galho 3 já cobre profiling/observabilidade interna da JVM** com notas completas (`JVM/13 - JFR e JMC — observabilidade de produção`, `JVM/12 - Diagnóstico — heap dumps...`, `JVM/10 - GC logs`, `JVM/11 - Tuning de GC`, `JVM/14 - Performance da JVM — síntese`). Por isso o eixo "profiling" do G17 **encolheu para link-back** (notas 18/19 linkam G3, não re-explicam) e a **observabilidade virou um seam de TRÊS pontas** (G3 JVM-interno / G16 trace-no-código / G17 operar-o-stack) — decisão do brainstorm.
4. **Decisões do usuário no brainstorm:** amplitude **granular (22 notas, 3/14/5)**; **profiling expandido em 2 notas** (18 diagnóstico-em-produção + 19 continuous-profiling); **corte k8s = contrato do app + manifesto ilustrativo** (probes/config/resources + um Deployment YAML; sem operar cluster).
5. **Dicionário** — **524 verbetes**; dups a linkar (não duplicar): `heap dump`/`JFR` (G3), `Micrometer Observation API`/`Micrometer Tracing`/`OpenTelemetry`/`OTLP`/`sidecar` (G16), `SBOM` (G15), `twelve-factor` (G16); conferir `AOT`. Expansão alfabética (~35), nunca recriar/reordenar; `updated: 2026-06-12`.
6. **Fronteira-assinatura sêxtupla (paths exatos confirmados):**
   - G3 → `JVM/13 - JFR e JMC — observabilidade de produção`, `JVM/12 - Diagnóstico — heap dumps, thread dumps e jcmd`, `JVM/11 - Tuning de GC — metodologia e prática`, `JVM/10 - GC logs — unified logging e leitura`, `JVM/14 - Performance da JVM — síntese`, `JVM/07 - JIT — C1, C2 e tiered compilation`, `JVM/01 - A JVM — o que é e o pipeline de execução`, `JVM/03 - Garbage Collection — o conceito`
   - G8 → `Spring Core e Boot/17 - Actuator e observabilidade`, `Spring Core e Boot/16 - SpringApplication e o embedded server`
   - G15 → `Build e tooling/15 - Empacotamento — fat jar, thin jar e repackage`, `Build e tooling/18 - Supply chain e SBOM`
   - G16 → `Microservices e sistemas distribuídos/18 - Tracing distribuído I — correlação no código`, `/19 - Tracing distribuído II — exportando o trace`, `/22 - Service mesh — quando a resiliência sai do código`
   - G13 → `Testes/18 - Performance — JMH e microbenchmarks`
   - G6 → `JavaFX/13 - Empacotamento — módulos, jlink e jpackage`
7. **Versões CRAVADAS via WebFetch (2026-06-12)** — GraalVM 25 (GFTC/Community), native-build-tools 1.1.2, Spring AOT desde Boot 3.0; Spring Boot 3.5.x (OSS até 30/06/2026) + 4.0.x (GA nov/2025); probes `probes.enabled` default true + sem startup probe; graceful shutdown default + 30s; JVM `UseContainerSupport` (Java 10)/`MaxRAMPercentage` 25.0/cgroup v2 (JDK 17); `jarmode=tools`/layered jar; bootBuildImage (Paketo, daemon) vs Jib 3.5.x (daemonless); distroless; Micrometer 1.17.x/Prometheus 3.12/Grafana 13/OTel Collector v0.154; head vs tail sampling; structured logging desde Boot 3.4; Pyroscope 2.x + async-profiler. (Detalhes em §4.3.3.) **Re-confirmar na execução.**
8. **Troncos/arquivos intocáveis** — todos os artefatos dos Galhos 1-16 exceto: ativação do MOC central (§3.4), poda modesta em `Backend/Spring Boot.md` (§3.5), quitação dos ganchos "(planejado) G17" (§3.6). Pasta `Cloud-native e produção/` ainda **não existe**.

Nenhum número de adoção/market-share é inventado (**não citar percentuais**). Quando faltar fato verificável, **PERGUNTAR** antes de escrever.

## 7. Critérios de aceitação do galho

Além dos critérios gerais (§10 do roadmap):

1. 22 notas em `03-Dominios/Java/Cloud-native e produção/`, frontmatter com `fase:`, `publish: true`, distribuídas 3/14/5.
2. MOC do galho com 3 subseções de fase + 5 rotas alternativas + dataview (inline code nunca inicia com `=`) + folder-link resolve (`index.md` presente).
3. Dicionário de Java **expandido** (não recriado) com ~35 verbetes; verbetes dos Galhos 1-16 intactos; `updated: 2026-06-12`; dups conferidos e linkados (não duplicar `heap dump`/`JFR`/`OpenTelemetry`/`OTLP`/`SBOM`/`sidecar`/`12-factor`).
4. MOC central `Java/index.md` com Galho 17 ativado (linha vira wikilink); resto intacto; `updated: 2026-06-12`.
5. **Poda reversa executada (modesta, com callout)**: `### Graceful shutdown` → callout (nota 12); `### Memory leak e GC tuning` → callout (G3 heap/GC + nota 18); o parêntese do `## Actuator` → wikilink (nota 13). **Seções não-G17 intactas** (pool/N+1/LazyInit/@Transactional/Flyway). Outros troncos intactos.
6. **Ganchos quitados**: os ~23 pontos "(planejado) G17" viram wikilinks ativos (§3.6); Galho 18 permanece texto "(planejado)".
7. Cada nota: TL;DR; code samples válidos (Dockerfile/yaml/k8s/build/CLI; flags cravados); "Em entrevista" com `### Frase pronta (inglês)` 3+ sentenças + `### Vocabulário` tabela 6+ termos PT→EN; "Armadilhas" com `### (N) Título` numerado + exemplo + fix (≥2 Iniciado, ≥3 Adepto/Magus); wikilinks (galho + MOC central + fronteira quando aplicável + Dicionário); "Referências" com docs oficiais verificadas.
8. **Fronteira-assinatura respeitada**: JFR/heap/GC/AOT-JIT → G3; Actuator-mecanismo → G8; empacotamento-do-jar/SBOM → G15; tracing-no-código/mesh → G16; JMH → G13; jpackage → G6; nada re-explicado; galho 18 só texto "(planejado)".
9. **Fronteiras de escopo respeitadas**: operar cluster k8s (kubectl/Service/Ingress/operators/HPA), operar Istio/Linkerd, operar Vault = fora de escopo (menção); o galho cobre o **contrato do app** + Deployment YAML ilustrativo. **Profiling não re-explica G3** (heap/JFR/GC = link).
10. Zero fabricação de experiência pessoal; zero estatística de adoção inventada; afirmações version-specific citam a versão verificada via WebFetch (GraalVM/Spring Boot/Micrometer/Prometheus/OTel/Pyroscope).
11. 1 commit por nota/artefato; sem `Co-Authored-By: Claude`; sem `--no-verify`; stage nominal (nunca `-A`); subagents write-only, controlador commita.
12. `verificar-wikilinks` roda limpo na pasta do galho (evitar âncoras same-file; conferir os títulos EXATOS das notas-fronteira — nomes longos com em-dash; lição do Galho 12).

## 8. Riscos e mitigações

| Risco | Mitigação |
|---|---|
| **Re-explicar o Galho 3** (JFR, heap dump, GC, AOT/JIT) — o risco nº 1 deste galho | A decisão do brainstorm: profiling do G17 é **link-back** (notas 02/08/18 linkam `JVM/13`/`/12`/`/11`/`/07`); a nota 18 é **ângulo operacional/workflow de incidente**, não a mecânica. Review por fase confere que não há re-explicação de GC/heap/JFR. |
| **Inventar versão "de memória"** (GraalVM, Spring Boot, native-build-tools, Pyroscope, Collector) | Versões cravadas no pré-flight (§4.3.3); WebFetch no Step 1. Pontos minados: **graceful shutdown é DEFAULT** no Boot; **sem startup probe dedicado**; **`jarmode=tools`** (não `layertools`) no 3.x; **MaxRAMPercentage default 25.0**; GraalVM 25/GFTC; Spring AOT desde Boot 3.0; structured logging desde Boot 3.4. |
| **Invadir DevOps/infra puro** (operar cluster k8s, Service/Ingress, operar Istio/Vault) | Corte do brainstorm: **contrato do app + 1 Deployment YAML ilustrativo**; operar cluster/mesh/Vault = menção de fronteira. Review confere que não há tutorial de kubectl/operators. |
| **Sobreposição entre as notas de observabilidade** (13-17) e com G3/G16 | Foco distinto: 13 panorama/seam, 14 métricas, 15 dashboards, 16 Collector/sampling, 17 logs; o seam de 3 pontas (nota 13) deixa explícito o que é G3/G16. Review checa sobreposição. |
| **Inventar estatística de adoção** ("X% usa Kubernetes/native/Docker") | Pré-flight não achou fonte → **proibido citar percentuais**; comparações qualitativas. |
| **Hype/dogma** ("native image é o futuro", "tudo em container", "microservices precisa de k8s") | A tese honesta (production-ready = postura; native = trade-off de plataforma, não upgrade; "quando X E quando Y") fixada em 01/08/21; a nota 21 (native vs JVM) é o contrapeso; review por fase. |
| **Code samples inválidos** (Dockerfile/k8s/native config errados) | Snippets válidos; flags cravados (`-Djarmode=tools`, `MaxRAMPercentage`, `native:compile`, `BP_NATIVE_IMAGE`); Deployment YAML bem-formado; review confere. |
| **Exemplos de domínio sensível / 1ª pessoa** | Framing neutro (`com.example`, `order-service:1.4.2`); NUNCA MedEspecialista/1ª pessoa/"no meu cluster"; review por fase. |
| **Poda reversa: re-explicar GC ao migrar `Memory leak e GC tuning`** | O callout aponta G3 (heap/GC) + nota 18 (profiling); NÃO duplica a mecânica de GC; confirmar linhas via grep; **NÃO TOCAR** pool/N+1/LazyInit/@Transactional/Flyway. |
| **Capstone/notas inventarem títulos de nota-fronteira** (lição Galho 12, reincidente no G16) | Passar aos subagentes os títulos EXATOS das 22 notas + das notas-fronteira (em-dash); `verificar-wikilinks` ao fim; review do capstone confere 1:1. **Atenção especial:** o G16 teve a nota 09 e o capstone inventando títulos/pasta — reforçar. |
| **Dicionário: duplicar verbete existente** (`heap dump`, `JFR`, `OpenTelemetry`, `SBOM`) | Grep dos existentes antes de inserir; tocar existente → **linkar**, não duplicar; inserção alfabética, nunca recriar. |
| **Bot de backup (Obsidian Git) commitando no meio** | Subagents write-only; controlador commita após cada nota com `git add` nominal (nunca `-A`); guardar contra `.git/index.lock`. |
| Galho denso (22 notas) inflar notas | Distribuição 3/14/5 fixada; se uma nota passar de ~600 linhas, dividir nota (não galho); capstone com cheatsheet enxuto. |

## 9. Próximos passos

1. **Aprovação deste spec**
2. **Plano de execução** via skill `superpowers:writing-plans` → `docs/superpowers/plans/2026-06-12-java-galho-17-cloud-native-producao-execution.md`
3. **Execução** via `superpowers:subagent-driven-development` **direto na `main`** (subagents write-only; sonnet por padrão, opus nas notas 01/08/13/16/21/22; review **por fase** + fix loop; push manual do usuário)
4. **Verificação** de wikilinks (incluindo os paths longos das notas-fronteira) + conferência de âncoras do Dicionário
5. **Atualização da memória** `project_trilha_java` (Galho 17 completo; **bloco distribuído/produção FECHADO**; próximo e último: 18 OCP) antes do próximo galho

## 10. Documentos relacionados

- `2026-06-02-java-senior-roadmap-design.md` — roadmap macro (18 galhos); Galho 17 em §5
- `2026-06-12-java-galho-16-microservices-design.md` / `...-execution.md` — Galho 16 (galho anterior; molde de galho híbrido + poda + quitação de ganchos; dono do tracing/mesh — fronteira das notas 13/16)
- `2026-06-11-java-galho-15-build-tooling-design.md` — Galho 15 (dono de empacotamento/SBOM — fronteira das notas 03/04/20)
- `2026-06-05-java-galho-03-jvm-design.md` — Galho 3 (dono de JFR/heap/GC/AOT-JIT — fronteira-assinatura nº 1, notas 02/08/18)
- `2026-06-08-java-galho-08-spring-core-design.md` — Galho 8 (dono do Actuator — fronteira das notas 10/13/14)
- Galhos 5/7/11/14/15/16 — template de **galho de pesquisa/híbrido**
- Artefatos a criar/atualizar: `03-Dominios/Java/Cloud-native e produção/**` (22 notas + MOC), `03-Dominios/Java/Dicionário de Java.md`, `03-Dominios/Java/index.md`, `03-Dominios/Java/Backend/Spring Boot.md` (poda modesta), e os ~23 arquivos de quitação de gancho (§3.6)
- Fontes-base do galho: `graalvm.org`, `graalvm.github.io/native-build-tools`, `docs.spring.io/spring-boot`, `buildpacks.io`, `paketo.io`, `github.com/GoogleContainerTools/jib`+`/distroless`, `micrometer.io`, `prometheus.io`, `grafana.com`, `opentelemetry.io`
- Memórias: [[project_trilha_java]], [[project_trilhas_fases_aprendizado]], [[project_tronco_galhos_pattern]], [[feedback_galhos_direto_main]], [[feedback_no_fabrication]], [[feedback_quartz_index]], [[feedback_commits]], [[feedback_dataview_inline_code]], [[feedback_notas_atomicas]], [[feedback_enriquecimento_feynman]], [[feedback_redundancia_entre_notas]]
