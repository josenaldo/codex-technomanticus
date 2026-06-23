# Galho 17 — Cloud-native e produção (Java Senior) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Criar o Galho 17 da trilha Java Senior — 22 notas atômicas (production-ready/cloud-native, JVM no container, empacotamento de imagem, Dockerfile/Buildpacks/Jib/distroless, GraalVM Native Image + Spring AOT, contrato com k8s/probes/config/graceful-shutdown, observabilidade de operação/Micrometer-Prometheus-Grafana/OTel-Collector/sampling/logs estruturados, profiling em produção e continuous profiling, CI/CD, native-vs-JVM, capstone) em 3 fases + MOC do galho + expansão do Dicionário + ativação do MOC central + **poda reversa modesta** em `Backend/Spring Boot.md` + **quitação de ~23 ganchos "(planejado) G17"**.

**Architecture:** Padrão galhos + 3 fases (Iniciado/Adepto/Magus). Pasta flat `03-Dominios/Tecnologia/Java/Cloud-native e produção/`, notas `publish: true` em PT-BR, numeração global 01-22 (3/14/5). **Galho HÍBRIDO** = pesquisa pesada (containers/native/observabilidade-de-operação) + **poda reversa modesta** (`### Graceful shutdown` + `### Memory leak e GC tuning` do `Spring Boot.md` → callouts) + **INTEGRAÇÃO intensa** (quita ~23 ganchos "(planejado) G17"). **Fronteira-assinatura SÊXTUPLA**: G3 (JFR/heap/GC/AOT-JIT), G8 (Actuator), G15 (empacotamento/SBOM), G16 (tracing-no-código/mesh), G13 (JMH), G6 (jpackage). **Seam de observabilidade de 3 pontas**: G3 (JVM-interno) / G16 (trace-no-código) / G17 (operar-o-stack). **Tese honesta**: production-ready = postura, não feature; cloud-native = nível de deploy/operação (arquitetura é G16); native image = trade-off de plataforma, não upgrade. Galho 18 (OCP) = texto "(planejado)". **Direto na `main`** ([[feedback_galhos_direto_main]]); push manual.

**Tech Stack:** Obsidian Flavored Markdown, frontmatter YAML, wikilinks, callouts, Dataview, Quartz v4. Verificação via WebFetch (graalvm.org, graalvm.github.io/native-build-tools, docs.spring.io/spring-boot, buildpacks.io/paketo.io, github.com/GoogleContainerTools/jib+/distroless, micrometer.io, prometheus.io, grafana.com, opentelemetry.io).

---

## Convenções aplicadas a TODAS as notas (ler antes de qualquer task)

**Frontmatter** (ajustar `title`/`fase`/`tags`/`aliases` por nota; `created`/`updated: 2026-06-12`):

```yaml
---
title: "<título sem prefixo numérico>"
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
  - <1-3 tags de conceito: container, docker, kubernetes, native-image, graalvm, observabilidade, prometheus, grafana, opentelemetry, profiling, ci-cd, deploy, actuator>
aliases:
  - <aliases>
---
```

H1 `# Título` após o frontmatter.

**Estrutura H2 obrigatória** (nesta ordem):

1. `> [!abstract] TL;DR` — 2-4 linhas. Callout, NÃO H2.
2. `## O que é` — definição.
3. `## Por que importa` — relevância pra senior/entrevista.
4. `## Como funciona` — H3s; mínimo 3 em Adepto/Magus.
5. `## Na prática` — código/config **válido**; framing neutro; **NUNCA** 1ª pessoa, `MedEspecialista`, `josenaldo`, "da minha experiência", "no meu cluster", "incidente de produção que tive". Domínios neutros: `com.example`, serviços `order-service`/`payment-service`, imagem `order-service:1.4.2`.
6. `## Armadilhas` — ≥2 (Iniciado) / ≥3 (Adepto/Magus). Cada uma: `### (N) Título` + descrição + exemplo curto + fix em 1 linha (H3 numerado, NÃO callout `[!warning]`).
7. `## Em entrevista` — `### Frase pronta (inglês)` com **3+ sentenças** + `### Vocabulário` **6+ termos** em tabela `| Termo PT | Termo EN |`.
8. `## Veja também` — wikilinks SEM backticks, SEM âncoras same-file. Sempre: notas do galho + `[[03-Dominios/Tecnologia/Java/Cloud-native e produção/index|Cloud-native e produção (MOC do galho)]]` + `[[03-Dominios/Tecnologia/Java/index|Trilha Java]]` + (quando aplicável) a nota da fronteira + verbetes do Dicionário.
9. `## Referências` — docs oficiais consultadas.

**Tamanho:** 200-500 linhas (densas até 600 — limite de [[feedback_notas_atomicas]]). Se passar de 600, dividir nota (não galho).

**Registro Feynman** (de [[feedback_enriquecimento_feynman]]) onde couber: analogias (container-awareness = "a JVM que enfim lê o tamanho do quarto onde mora"; layered jar = "malas despachadas que mudam de peso em ritmos diferentes"; liveness vs readiness = "estou vivo?" vs "posso atender agora?"; native image = "fotografar o prédio pronto vs filmar a obra"; tail-based sampling = "decidir guardar a gravação depois de ver o fim do jogo"), perguntas retóricas, callouts. Sem inflar.

**Restrições absolutas:**
- **FRONTEIRA-ASSINATURA (linkar de volta, NUNCA re-explicar).** Mapeamento de link-back (paths confirmados na Task 0):
  - **G3 (JVM) — o mais importante:** JFR/JMC → `03-Dominios/Tecnologia/Java/JVM/13 - JFR e JMC — observabilidade de produção`; heap/thread dump → `JVM/12 - Diagnóstico — heap dumps, thread dumps e jcmd`; GC tuning → `JVM/11 - Tuning de GC — metodologia e prática`; GC logs → `JVM/10 - GC logs — unified logging e leitura`; performance síntese → `JVM/14 - Performance da JVM — síntese`; JIT → `JVM/07 - JIT — C1, C2 e tiered compilation`; AOT/native em nível JVM → `JVM/01 - A JVM — o que é e o pipeline de execução`; GC conceito → `JVM/03 - Garbage Collection — o conceito`. **NÃO re-explicar heap dump, JFR, GC, AOT/JIT.**
  - **G8 (Spring) — Actuator:** `03-Dominios/Tecnologia/Java/Spring Core e Boot/17 - Actuator e observabilidade`, `Spring Core e Boot/16 - SpringApplication e o embedded server`. Mecanismo é lá; aqui é o uso operacional.
  - **G15 (Build):** empacotamento → `03-Dominios/Tecnologia/Java/Build e tooling/15 - Empacotamento — fat jar, thin jar e repackage`; SBOM → `Build e tooling/18 - Supply chain e SBOM`. Build do jar é lá; aqui é imagem/deploy.
  - **G16 (Microservices):** tracing → `03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/18 - Tracing distribuído I — correlação no código` + `/19 - Tracing distribuído II — exportando o trace`; mesh → `/22 - Service mesh — quando a resiliência sai do código`. Código é lá; aqui é operar.
  - **G13 (Testes):** JMH → `03-Dominios/Tecnologia/Java/Testes/18 - Performance — JMH e microbenchmarks`. Microbenchmark ≠ profiling de produção.
  - **G6 (JavaFX):** jpackage/native desktop → `03-Dominios/Tecnologia/Java/JavaFX/13 - Empacotamento — módulos, jlink e jpackage`.
- **Galho 18 (OCP) só como texto "(planejado)", SEM wikilink.** Greps de review checam `\[\[[^]]*(Galho 18|OCP)`.
- **Operar cluster/mesh/Vault = FORA DE ESCOPO** (kubectl, Service/Ingress, operators, HPA, instalar Istio, operar Vault) — só menção de fronteira. O galho cobre o **contrato do app** + 1 Deployment YAML ilustrativo.
- Sem fabricação ([[feedback_no_fabrication]]); domínios neutros. **Zero estatística de adoção/market-share inventada** (proibido "X% usa Kubernetes/native/Docker"); números só com fonte verificável.
- **Pesquisa pras partes version-specific (quase todas as notas):** WebFetch no Step 1. **Fatos cravados no pré-flight (2026-06-12) — re-confirmar, são a base:**
  - **GraalVM 25** (16/set/2025; JDK 21/24/25; cadência mensal desde 25.1). **Oracle GraalVM = GFTC** (grátis prod comercial); **Community = GPLv2+CPE**. Honestidade: GraalVM for JDK 24 foi o último sob produtos Oracle Java SE; Oracle desfocou GraalVM como produto Java — **mas Native Image segue mantido** (citar sem drama).
  - **Native Image** = AOT closed-world; **reachability metadata** (`reachability-metadata.json` em `META-INF/native-image/`, ex-"reflection config"; Tracing Agent `-agentlib:native-image-agent`). **native-build-tools 1.1.2** (`org.graalvm.buildtools`): Maven `native:compile`/`native:test`, Gradle `nativeCompile`/`nativeTest`.
  - **Spring AOT desde Spring Boot 3.0** (nov/2022): AOT engine gera `*__BeanDefinitions` + hints; `RuntimeHintsRegistrar`/`@RegisterReflectionForBinding`; `@Profile`/`@ConditionalOnProperty` em runtime são limitados. Dois caminhos: native-build-tools (GraalVM local) ou Buildpacks `BP_NATIVE_IMAGE=true`.
  - **Spring Boot**: **3.5.x** (último 3.x, OSS até **30/06/2026**) + **4.0.x** (GA **20/11/2025**, Framework 7, Java 25/compat 17); doc current 4.1.x. Boot 3.x baseline, 4.x recente.
  - **Probes**: `management.endpoint.health.probes.enabled` default **true** (auto em k8s); `/actuator/health/liveness` + `/readiness`; `ApplicationAvailability`/`LivenessState`(CORRECT/BROKEN)/`ReadinessState`(ACCEPTING/REFUSING_TRAFFIC). **Sem startup probe dedicado** (reusa liveness). `add-additional-paths` → `/livez`/`/readyz`. Health UP/DOWN/OUT_OF_SERVICE/UNKNOWN; DOWN/OUT_OF_SERVICE → **503**.
  - **Graceful shutdown**: `server.shutdown=graceful` **default no Boot**; `spring.lifecycle.timeout-per-shutdown-phase` default **30s**; readiness → `REFUSING_TRAFFIC` no shutdown; coordenar com **preStop sleep** + `terminationGracePeriodSeconds`.
  - **JVM container**: `-XX:+UseContainerSupport` default **Java 10**; `-XX:MaxRAMPercentage` default **25.0**; cgroup v2 desde **JDK 17/11.0.16/8u372**; `-XX:ActiveProcessorCount`. `-Xmx` fixo tem precedência sobre percentagem (e é frágil em container).
  - **Imagem**: layered jar (`dependencies`/`spring-boot-loader`/`snapshot-dependencies`/`application`, `layers.idx`); `java -Djarmode=tools ... extract --layers` (Boot 3.x; era `-Djarmode=layertools` no 2.x). **bootBuildImage**/`spring-boot:build-image` desde Boot 2.3 (builder default `paketobuildpacks/builder-noble-java-tiny`, **precisa de daemon**), `BP_JVM_VERSION`/`BP_NATIVE_IMAGE`. **Jib v3.5.x** (daemonless, sem Dockerfile, reproducible). **Distroless** `gcr.io/distroless/java21-debian13` (sem shell, non-root, exec-form). **CNB** = CNCF incubating.
  - **Observabilidade**: **Micrometer 1.17.x** ("SLF4J para métricas"); **Prometheus 3.12** (pull/scrape, `/actuator/prometheus`); **Grafana 13**; **OpenTelemetry Collector v0.154** (receivers/processors/exporters, separado do app); **head vs tail-based sampling** (tail exige Collector stateful); **structured logging nativo desde Boot 3.4** (`logging.structured.format.console=ecs`, ECS/GELF/Logstash, traceId via MDC).
  - **Continuous profiling**: **Grafana Pyroscope 2.x** (usa **async-profiler** para Java; correlaciona profile↔métrica↔trace); distinto do JFR local (G3).
- Comparações justas (quando X E quando Y): Dockerfile vs Buildpacks vs Jib, JVM vs native, head vs tail sampling, pull vs push, rolling vs blue-green vs canary, distroless vs base completa.
- Code fences: ` ```dockerfile `, ` ```yaml ` (application.yml/k8s/prometheus), ` ```xml `/` ```kotlin ` (build), ` ```bash ` (CLI `docker`/`java -Djarmode`/`mvnw native:compile`), ` ```json ` (reachability metadata/logs), ` ```text ` (diagramas/output). Sempre fechadas. **Usar os nomes/flags cravados** (`-Djarmode=tools`, `MaxRAMPercentage`, `native:compile`, `BP_NATIVE_IMAGE`).
- Commits: sem `Co-Authored-By: Claude`; sem `--no-verify`; `git add <path>` nominal (bot de backup roda em timer — NUNCA `-A`; guardar contra `.git/index.lock`); 1 commit por nota/artefato; direto na `main`; **sem push, sem deploy**. Subagents NÃO rodam git — o controlador commita.

**Modelo por nota:** sonnet por padrão; **opus** nas **01** (assinatura/tese), **08** (native conceito, version-heavy), **13** (panorama/seam de 3 pontas), **16** (Collector/sampling), **21** (native vs JVM), **22** (capstone).

**Fontes oficiais (base):**
- GraalVM: `https://www.graalvm.org/latest/reference-manual/native-image/` ; native-build-tools: `https://graalvm.github.io/native-build-tools/latest/`
- Spring Boot: `https://docs.spring.io/spring-boot/reference/` (packaging/container-images, packaging/native-image, actuator, web/graceful-shutdown, features/logging)
- Containers: `https://buildpacks.io/docs/`, `https://paketo.io/docs/`, `https://github.com/GoogleContainerTools/jib`, `https://github.com/GoogleContainerTools/distroless`
- Observabilidade: `https://docs.micrometer.io/micrometer/reference/`, `https://prometheus.io/docs/`, `https://grafana.com/oss/grafana/`, `https://opentelemetry.io/docs/collector/`, `https://opentelemetry.io/docs/concepts/sampling/`
- Profiling: `https://grafana.com/docs/pyroscope/latest/`
- Container-awareness JVM: `https://developers.redhat.com/articles/2022/04/19/java-17-whats-new-openjdks-container-awareness`

---

## Task 0: Pré-flight — pasta, terreno, baselines e linhas de poda/ganchos

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Cloud-native e produção/` (pasta)

- [ ] **Step 1:** Confirmar `main` limpa: `git status` e `git branch --show-current` (deve ser `main`).
- [ ] **Step 2:** Criar a pasta do galho: `mkdir -p "03-Dominios/Tecnologia/Java/Cloud-native e produção"`.
- [ ] **Step 3:** Confirmar os paths EXATOS das notas-fronteira (devem existir):
```bash
ls "03-Dominios/Tecnologia/Java/JVM/13 - JFR e JMC — observabilidade de produção.md" \
   "03-Dominios/Tecnologia/Java/JVM/12 - Diagnóstico — heap dumps, thread dumps e jcmd.md" \
   "03-Dominios/Tecnologia/Java/JVM/11 - Tuning de GC — metodologia e prática.md" \
   "03-Dominios/Tecnologia/Java/JVM/14 - Performance da JVM — síntese.md" \
   "03-Dominios/Tecnologia/Java/JVM/01 - A JVM — o que é e o pipeline de execução.md" \
   "03-Dominios/Tecnologia/Java/Spring Core e Boot/17 - Actuator e observabilidade.md" \
   "03-Dominios/Tecnologia/Java/Build e tooling/15 - Empacotamento — fat jar, thin jar e repackage.md" \
   "03-Dominios/Tecnologia/Java/Build e tooling/18 - Supply chain e SBOM.md" \
   "03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/18 - Tracing distribuído I — correlação no código.md" \
   "03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/22 - Service mesh — quando a resiliência sai do código.md" \
   "03-Dominios/Tecnologia/Java/Testes/18 - Performance — JMH e microbenchmarks.md" \
   "03-Dominios/Tecnologia/Java/JavaFX/13 - Empacotamento — módulos, jlink e jpackage.md"
```
- [ ] **Step 4:** Confirmar a linha do Galho 17 no MOC central e o estado do Dicionário:
```bash
grep -n "17\. Cloud-native" "03-Dominios/Tecnologia/Java/index.md"
grep -c "^### " "03-Dominios/Tecnologia/Java/Dicionário de Java.md"   # baseline ~524
grep -ni "updated:" "03-Dominios/Tecnologia/Java/Dicionário de Java.md" | head -1
```
- [ ] **Step 5:** Localizar os pontos de poda reversa em `Spring Boot.md` (para a Task 31):
```bash
grep -n "### Graceful shutdown\|### Memory leak e GC tuning\|## Actuator" "03-Dominios/Tecnologia/Java/Backend/Spring Boot.md"
```
- [ ] **Step 6:** Listar os ganchos "(planejado) G17" (para a Task 32):
```bash
grep -rln "Galho 17" "03-Dominios/Tecnologia/Java/" | grep -v "Dicionário"
```
- [ ] **Step 7:** Conferir dups no Dicionário (linkar, não duplicar): `grep -niE "^### (heap dump|JFR|Micrometer|OpenTelemetry|OTLP|sidecar|SBOM|twelve-factor|AOT|GraalVM)" "03-Dominios/Tecnologia/Java/Dicionário de Java.md"`. Anotar quais já existem.

> Nenhum commit nesta task (só pasta vazia).

---

## Fase Iniciado (notas 01-03)

> Cada nota: dispatch de subagente write-only com o texto da task + o bloco de Convenções. WebFetch no Step 1. Controlador commita após cada nota.

### Task 1: Nota 01 — "Production-ready" e cloud-native, a tese honesta *(opus, assinatura)*

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Cloud-native e produção/01 - Production-ready e cloud-native — a tese honesta.md`

- [ ] **Step 1 (WebFetch):** `12factor.net/` (build-release-run, disposability, logs) + `docs.spring.io/spring-boot/reference/` (production-ready features overview) — confirmar o framing.
- [ ] **Step 2 (escrever):** fase `iniciado`. "Production-ready" = **postura/conjunto de contratos** (observável, descartável, config externa, health declarado), NÃO feature. "Cloud-native" no nível de **deploy/operação** (a arquitetura distribuída é o Galho 16 — LINKA, não repete). O lado **build/release/run + disposability + logs-as-streams** dos 12 fatores (a parte de arquitetura é G16 — linka). **A nota-assinatura:** apresenta os **3 seams** (G3 JVM-interno / G16 trace-no-código / G17 operar-o-stack) e a fronteira sêxtupla. Armadilhas (≥2): "production-ready é uma checklist de features"; confundir cloud-native-arquitetura (G16) com cloud-native-operação (este galho). "Em entrevista" + "Veja também" (notas 02/13/22, G16 índice) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Cloud-native e produção/01 - Production-ready e cloud-native — a tese honesta.md"
git commit -m "feat(java): galho 17 nota 01 — production-ready e cloud-native (a tese honesta)"
```

### Task 2: Nota 02 — A JVM dentro de um container

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Cloud-native e produção/02 - A JVM dentro de um container.md`

- [ ] **Step 1 (WebFetch):** `developers.redhat.com/articles/2022/04/19/java-17-whats-new-openjdks-container-awareness` + `docs.oracle.com` (ou OpenJDK) — confirmar `UseContainerSupport` (default Java 10), `MaxRAMPercentage` (default 25.0), cgroup v2 (JDK 17), `ActiveProcessorCount`.
- [ ] **Step 2 (escrever):** fase `iniciado`. **Container-awareness**: `-XX:+UseContainerSupport` (lê cgroup), `-XX:MaxRAMPercentage`/`InitialRAMPercentage` (heap relativo ao limite do container) em vez de `-Xmx` fixo; cgroup v2; `-XX:ActiveProcessorCount`. Por que `-Xmx` fixo é frágil (não acompanha o limite no redeploy; precedência sobre o percentual). **Fronteira G3** (GC/heap é lá — linka `JVM/03`). ` ```bash ` (flags) + ` ```yaml ` (k8s resources resumido). Armadilhas (≥2): `-Xmx` fixo num container com limite menor → OOM-kill; rodar JDK antigo em host cgroup-v2-only (sem detecção). "Em entrevista" + "Veja também" (notas 01/11, G3 GC) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Cloud-native e produção/02 - A JVM dentro de um container.md"
git commit -m "feat(java): galho 17 nota 02 — a JVM dentro de um container"
```

### Task 3: Nota 03 — Empacotando o app numa imagem, o panorama

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Cloud-native e produção/03 - Empacotando o app numa imagem — o panorama.md`

- [ ] **Step 1 (WebFetch):** `docs.spring.io/spring-boot/reference/packaging/container-images/` (efficient-images, dockerfiles) — confirmar layered jar (`layers.idx`, 4 camadas) e `java -Djarmode=tools ... extract`.
- [ ] **Step 2 (escrever):** fase `iniciado`. Do `jar` à **imagem OCI**: o **layered jar** (camadas `dependencies`/`spring-boot-loader`/`snapshot-dependencies`/`application`, `layers.idx`; o porquê do cache de layers) e `java -Djarmode=tools -jar app.jar extract --layers` (era `-Djarmode=layertools` no Boot 2.x); **as 3 vias** (Dockerfile à mão, Buildpacks, Jib) em resumo, cada uma apontando sua nota (04/06/07). **Fronteira G15** (o build do jar/empacotamento é lá — linka `Build/15`; aqui é a imagem). ` ```bash ` (jarmode) + ` ```text ` (camadas). Armadilhas (≥2): jar gordo numa camada só (perde cache); confundir o empacotamento do jar (G15) com a imagem. "Em entrevista" + "Veja também" (notas 04/06/07, G15 Empacotamento) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Cloud-native e produção/03 - Empacotando o app numa imagem — o panorama.md"
git commit -m "feat(java): galho 17 nota 03 — empacotando o app numa imagem (panorama)"
```

### Task 4: Review da fase Iniciado (01-03)

- [ ] **Step 1:** dispatch de subagente revisor lendo as 3 notas. Checa: frontmatter+`fase`; estrutura H2; **zero fabricação** (grep `MedEspecialista|josenaldo|meu cluster|minha experiência|incidente de produção`); **zero estatística inventada** (grep `%`); **zero re-explicação de fronteira** (GC/heap → G3 linka; empacotamento → G15 linka); zero wikilink pra galho 18; versões cravadas (UseContainerSupport Java 10, MaxRAMPercentage 25.0, jarmode=tools); "Em entrevista" 3+ sentenças + 6+ termos tabela; **a tese honesta presente (01)**; **os 3 seams apresentados (01)**.
- [ ] **Step 2:** fix loop até aprovado. Se corrige, commit `fix(java): galho 17 — ajustes da fase Iniciado`.

---

## Fase Adepto (notas 04-17)

### Task 5: Nota 04 — Dockerfile na prática, multi-stage e layered jar

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Cloud-native e produção/04 - Dockerfile na prática — multi-stage e layered jar.md`

- [ ] **Step 1 (WebFetch):** `docs.spring.io/spring-boot/reference/packaging/container-images/dockerfiles.html` — confirmar o exemplo multi-stage e o `COPY` por camada.
- [ ] **Step 2 (escrever):** fase `adepto`. **Multi-stage build** (builder extrai camadas com `jarmode=tools`, runtime só copia); um `COPY` por camada pra cache; base JRE (`bellsoft/liberica-openjre`/`eclipse-temurin`); rodar como **non-root** (`USER`); `ENTRYPOINT` exec-form. Liga a nota 02 (container-awareness no runtime). ` ```dockerfile ` (multi-stage completo). Armadilhas (≥3): rodar como root; `ENTRYPOINT` shell-form (não recebe SIGTERM direito → quebra graceful shutdown, aponta nota 12); copiar o jar inteiro em vez das camadas. "Em entrevista" + "Veja também" (notas 02/05/12) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Cloud-native e produção/04 - Dockerfile na prática — multi-stage e layered jar.md"
git commit -m "feat(java): galho 17 nota 04 — Dockerfile na prática (multi-stage e layered jar)"
```

### Task 6: Nota 05 — Imagem enxuta e segura, distroless e scanning

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Cloud-native e produção/05 - Imagem enxuta e segura — distroless e scanning.md`

- [ ] **Step 1 (WebFetch):** `github.com/GoogleContainerTools/distroless` — confirmar imagens Java (`gcr.io/distroless/java21-debian13`), sem shell, non-root, exec-form.
- [ ] **Step 2 (escrever):** fase `adepto`. **Distroless** (só app + runtime; sem shell/package manager → superfície de ataque reduzida, melhor scanning; `ENTRYPOINT` exec-form obrigatório; `java*-debian*`); **non-root user**; **image scanning** (Trivy/Grype — conceitual, sem cravar versão se não confirmar); minimizar CVEs/camadas. ` ```dockerfile ` (distroless) + ` ```bash ` (scan conceitual). Armadilhas (≥3): debugar sem shell (precisa de imagem debug); base "latest" sem pin; achar que distroless dispensa scanning. "Em entrevista" + "Veja também" (notas 04/06, G15 SBOM) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Cloud-native e produção/05 - Imagem enxuta e segura — distroless e scanning.md"
git commit -m "feat(java): galho 17 nota 05 — imagem enxuta e segura (distroless e scanning)"
```

### Task 7: Nota 06 — Buildpacks, imagem sem Dockerfile

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Cloud-native e produção/06 - Buildpacks — imagem sem Dockerfile.md`

- [ ] **Step 1 (WebFetch):** `buildpacks.io/docs/` + `paketo.io/docs/howto/java/` + `docs.spring.io/spring-boot/maven-plugin/build-image.html` — confirmar CNB (builder/buildpack/lifecycle), Paketo, `bootBuildImage` (default builder, daemon).
- [ ] **Step 2 (escrever):** fase `adepto`. **Cloud Native Buildpacks** (spec CNCF incubating: builder/buildpack/lifecycle; imagem OCI sem Dockerfile) + **Paketo** (impl. Java/Spring); `spring-boot:build-image`/`bootBuildImage` (desde Boot 2.3, builder default `paketobuildpacks/builder-noble-java-tiny`, **precisa de Docker daemon**, imagens non-root), `BP_JVM_VERSION`. ` ```bash ` (`./mvnw spring-boot:build-image`) + ` ```kotlin ` (config Gradle). Armadilhas (≥3): esquecer que precisa do daemon; builder desatualizado; não fixar `BP_JVM_VERSION` (instala a target detectada). "Em entrevista" + "Veja também" (notas 03/07/09) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Cloud-native e produção/06 - Buildpacks — imagem sem Dockerfile.md"
git commit -m "feat(java): galho 17 nota 06 — Buildpacks (imagem sem Dockerfile)"
```

### Task 8: Nota 07 — Jib, imagem daemonless

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Cloud-native e produção/07 - Jib — imagem daemonless.md`

- [ ] **Step 1 (WebFetch):** `github.com/GoogleContainerTools/jib` — confirmar daemonless, sem Dockerfile, layering automático, reproducible, v3.5.x.
- [ ] **Step 2 (escrever):** fase `adepto`. **Jib** (`com.google.cloud.tools:jib`, v3.5.x): builda imagem OCI **sem Docker daemon e sem Dockerfile**, layering automático (separa deps de classes), reproducible (mesmo conteúdo → mesma imagem); plugins Maven/Gradle, push direto pro registry. **Buildpacks vs Jib** (lifecycle CNB + daemon vs plugin direto, daemonless). ` ```xml ` (plugin Maven) + ` ```bash ` (`mvn jib:build`). Armadilhas (≥3): assumir que precisa de Docker (não precisa); customização de imagem mais limitada que Dockerfile; credenciais de registry. "Em entrevista" + "Veja também" (notas 03/06) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Cloud-native e produção/07 - Jib — imagem daemonless.md"
git commit -m "feat(java): galho 17 nota 07 — Jib (imagem daemonless)"
```

### Task 9: Nota 08 — GraalVM Native Image, conceito e trade-offs *(opus)*

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Cloud-native e produção/08 - GraalVM Native Image — conceito e trade-offs.md`

- [ ] **Step 1 (WebFetch):** `graalvm.org/latest/reference-manual/native-image/` + `graalvm.org/release-notes/` — confirmar **GraalVM 25**, AOT closed-world, reachability metadata, licença GFTC/Community.
- [ ] **Step 2 (escrever):** fase `adepto`. **GraalVM 25** (GFTC Oracle / GPLv2+CPE Community; JDK 21/24/25). **Native Image** = AOT **closed-world** (só código alcançável a partir do `main`); **reachability metadata** (`reachability-metadata.json`, ex-"reflection config"; Tracing Agent; Reachability Metadata Repository como conceito) pra reflection/proxies/resources/serialization. **Trade-offs honestos**: startup/footprint em ms vs **sem JIT** (sem otimização especulativa de pico), build lento, restrições ao dinamismo. **Honestidade de mercado:** GraalVM for JDK 24 foi o último sob produtos Oracle Java SE; Oracle desfocou o GraalVM como produto Java — **Native Image segue mantido** (citar sem drama, com fonte). **Fronteira G3** (AOT/JIT como mecanismo de JVM — LINKA `JVM/01`/`JVM/07`/`JVM/14`, não re-explica). ` ```bash ` (`native-image`) + ` ```text ` (closed-world). Armadilhas (≥3): esquecer hints de reflection (falha em runtime, não build); esperar throughput de pico igual à JVM; achar que toda app deve virar native. "Em entrevista" + "Veja também" (notas 09/21, G3 A JVM/JIT) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Cloud-native e produção/08 - GraalVM Native Image — conceito e trade-offs.md"
git commit -m "feat(java): galho 17 nota 08 — GraalVM Native Image (conceito e trade-offs)"
```

### Task 10: Nota 09 — Native Image com Spring, Spring AOT na prática

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Cloud-native e produção/09 - Native Image com Spring — Spring AOT na prática.md`

- [ ] **Step 1 (WebFetch):** `docs.spring.io/spring-boot/reference/packaging/native-image/` + `graalvm.github.io/native-build-tools/latest/` — confirmar Spring AOT (desde Boot 3.0), hints, native-build-tools 1.1.2, os dois caminhos.
- [ ] **Step 2 (escrever):** fase `adepto`. **Spring AOT engine** (desde Boot 3.0, nov/2022): em build-time gera `*__BeanDefinitions` estáticos + hints sob `META-INF/native-image/` (reflect/resource/proxy-config); **`RuntimeHintsRegistrar`** (`registerHints`) / **`@RegisterReflectionForBinding`**; limitações (`@Profile`/`@ConditionalOnProperty` em runtime). **Dois caminhos**: `native-build-tools` 1.1.2 (`native:compile`/`nativeCompile`, exige GraalVM local) vs Buildpacks `BP_NATIVE_IMAGE=true` (no container). ` ```java ` (RuntimeHintsRegistrar) + ` ```bash ` (`./mvnw -Pnative native:compile`) + ` ```xml ` (native-maven-plugin). Armadilhas (≥3): reflection numa lib sem metadata (precisa de hint manual); `@ConditionalOnProperty` que não funciona em native; build de CI lento sem cache. "Em entrevista" + "Veja também" (notas 08/06/21) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Cloud-native e produção/09 - Native Image com Spring — Spring AOT na prática.md"
git commit -m "feat(java): galho 17 nota 09 — Native Image com Spring (Spring AOT na prática)"
```

### Task 11: Nota 10 — Health e probes, o contrato com o orquestrador

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Cloud-native e produção/10 - Health e probes — o contrato com o orquestrador.md`

- [ ] **Step 1 (WebFetch):** `docs.spring.io/spring-boot/reference/actuator/endpoints.html` (Kubernetes Probes) — confirmar `probes.enabled` (default true), `/actuator/health/liveness`+`/readiness`, sem startup probe, estados.
- [ ] **Step 2 (escrever):** fase `adepto`. O **Actuator** (mecanismo é G8 — LINKA `Spring Core e Boot/17`): `/actuator/health`, exposição (`management.endpoints.web.exposure.include`, default só health); **probes k8s** (`management.endpoint.health.probes.enabled` default true, auto em k8s; `/actuator/health/liveness` + `/readiness`; `ApplicationAvailability`/`LivenessState`/`ReadinessState`); **sem startup probe dedicado** (reusa liveness pra boot lento); `add-additional-paths` → `/livez`/`/readyz`; estados UP/DOWN/OUT_OF_SERVICE (503). **Liveness não depende de check externo** (evita restart em cascata). ` ```yaml ` (actuator config) + ` ```yaml ` (probes no Deployment). Armadilhas (≥3): liveness checando o DB (DB cai → app reinicia em loop); readiness sem checar dependências; expor todos os endpoints (`*`) em produção. "Em entrevista" + "Veja também" (notas 11/12, G8 Actuator) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Cloud-native e produção/10 - Health e probes — o contrato com o orquestrador.md"
git commit -m "feat(java): galho 17 nota 10 — health e probes (o contrato com o orquestrador)"
```

### Task 12: Nota 11 — Config e recursos no Kubernetes

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Cloud-native e produção/11 - Config e recursos no Kubernetes.md`

- [ ] **Step 1 (WebFetch):** `docs.spring.io/spring-boot/reference/features/external-config.html` (env/config) + `kubernetes.io/docs/concepts/configuration/` (ConfigMap/Secret — só referência conceitual) — confirmar mapeamento env→property.
- [ ] **Step 2 (escrever):** fase `adepto`. Config externa: **env vars** (relaxed binding `MY_PROP` → `my.prop`), **ConfigMap/Secret** mapeados pro app (12-factor config no ambiente — linka nota 01); **resource limits** (requests/limits) e a relação com `MaxRAMPercentage` (nota 02); **o Deployment YAML ilustrativo** (probes + resources + env/configMapRef) — a ótica do app que CONSOME o contrato. **Operar cluster (kubectl/Service/Ingress/operators) = fora de escopo** (menção); secrets management operacional/Vault = fronteira (G16 nota 12 mencionou). ` ```yaml ` (Deployment + ConfigMap) + ` ```yaml ` (application.yml com env). Armadilhas (≥3): secret em ConfigMap (não em Secret); `-Xmx` brigando com o limit (nota 02); config sensível em env logada. "Em entrevista" + "Veja também" (notas 02/10/12) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Cloud-native e produção/11 - Config e recursos no Kubernetes.md"
git commit -m "feat(java): galho 17 nota 11 — config e recursos no Kubernetes"
```

### Task 13: Nota 12 — Graceful shutdown e deploy sem downtime

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Cloud-native e produção/12 - Graceful shutdown e deploy sem downtime.md`

- [ ] **Step 1 (WebFetch):** `docs.spring.io/spring-boot/reference/web/graceful-shutdown.html` + `docs.spring.io/spring-boot/how-to/deployment/cloud.html` — confirmar `server.shutdown=graceful` (default), 30s, REFUSING_TRAFFIC, preStop.
- [ ] **Step 2 (escrever):** fase `adepto`. **`server.shutdown=graceful`** (default no Boot), `spring.lifecycle.timeout-per-shutdown-phase` (30s; requests em andamento completam, novos rejeitados); coordenação com **SIGTERM + preStop hook** (race condition de roteamento; `terminationGracePeriodSeconds` > timeout); readiness vira **`REFUSING_TRAFFIC`** (→ OUT_OF_SERVICE/503) no shutdown pra k8s parar de rotear; `@PreDestroy` pra cleanup. **Deploy sem downtime**: rolling vs blue-green vs canary (conceitual). **RECEBE a poda do `### Graceful shutdown`.** ` ```yaml ` (graceful config + preStop) + ` ```java ` (`@PreDestroy`). Armadilhas (≥3): SIGTERM cortando requests (sem graceful); `terminationGracePeriodSeconds` menor que o timeout (SIGKILL corta o graceful); `ENTRYPOINT` shell-form não propaga SIGTERM (aponta nota 04). "Em entrevista" + "Veja também" (notas 04/10/20) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Cloud-native e produção/12 - Graceful shutdown e deploy sem downtime.md"
git commit -m "feat(java): galho 17 nota 12 — graceful shutdown e deploy sem downtime"
```

### Task 14: Nota 13 — Observabilidade de operação, o panorama e os 3 seams *(opus)*

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Cloud-native e produção/13 - Observabilidade de operação — o panorama e os 3 seams.md`

- [ ] **Step 1 (WebFetch):** `micrometer.io/` + `opentelemetry.io/docs/` + `docs.spring.io/spring-boot/reference/actuator/` — confirmar os 3 pilares e o papel do Actuator como ponte.
- [ ] **Step 2 (escrever):** fase `adepto`. Os **3 pilares** (métricas, logs, traces). **O seam de TRÊS pontas** (a nota-chave): **G3** observabilidade interna da JVM (JFR/heap/GC — LINKA `JVM/13`), **G16** correlação de trace no código (LINKA `Microservices/18`), **G17** operar o stack no cluster (a tríade de notas 14-17). **Actuator** como ponte app↔ferramentas (mecanismo é G8 — LINKA `Spring Core e Boot/17`). Não re-explica nada das fronteiras — emoldura. ` ```text ` (diagrama dos 3 seams + 3 pilares). Armadilhas (≥3): instrumentar sem coletar (dado que ninguém vê); confundir os 3 seams (re-fazer no app o que o coletor faz); métricas sem cardinalidade controlada. "Em entrevista" + "Veja também" (notas 14/16/18, G3 JFR, G16 tracing) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Cloud-native e produção/13 - Observabilidade de operação — o panorama e os 3 seams.md"
git commit -m "feat(java): galho 17 nota 13 — observabilidade de operação (panorama e os 3 seams)"
```

### Task 15: Nota 14 — Métricas em produção, Micrometer e Prometheus

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Cloud-native e produção/14 - Métricas em produção — Micrometer e Prometheus.md`

- [ ] **Step 1 (WebFetch):** `docs.micrometer.io/micrometer/reference/` + `prometheus.io/docs/introduction/overview/` + `docs.spring.io/spring-boot/reference/actuator/metrics.html` — confirmar Micrometer 1.17.x, registries, `/actuator/prometheus`, pull/scrape.
- [ ] **Step 2 (escrever):** fase `adepto`. **Micrometer 1.17.x** ("SLF4J para métricas/observability facade"), os **registries** (Prometheus, OTLP…); **`/actuator/prometheus`** (precisa `micrometer-registry-prometheus`); **Prometheus 3.12** = modelo **pull/scrape** sobre HTTP (`scrape_configs` com `metrics_path: /actuator/prometheus`); tipos counter/gauge/timer/histogram (conceito). Liga ao Actuator (G8). ` ```yaml ` (prometheus.yml scrape + application.yml) + ` ```java ` (custom metric com `MeterRegistry`). Armadilhas (≥3): cardinalidade explosiva (tag com user-id); expor `/actuator/prometheus` sem proteção; push vs pull mal entendido. "Em entrevista" + "Veja também" (notas 13/15/16, G8 Actuator) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Cloud-native e produção/14 - Métricas em produção — Micrometer e Prometheus.md"
git commit -m "feat(java): galho 17 nota 14 — métricas em produção (Micrometer e Prometheus)"
```

### Task 16: Nota 15 — Dashboards e alertas, Grafana

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Cloud-native e produção/15 - Dashboards e alertas — Grafana.md`

- [ ] **Step 1 (WebFetch):** `grafana.com/oss/grafana/` + `prometheus.io/docs/practices/` — confirmar Grafana 13, modelo de dashboards; RED/USE como métodos conhecidos.
- [ ] **Step 2 (escrever):** fase `adepto`. **Grafana 13** = camada de visualização/dashboards sobre Prometheus (e outras fontes); os métodos **RED** (Rate/Errors/Duration — para serviços) e **USE** (Utilization/Saturation/Errors — para recursos); **alerting** (conceitual); **SLO/SLI** (menção). Como um dashboard de serviço Spring se monta (taxa de request, p95/p99, erros 5xx, saturação de pool). ` ```text ` (estrutura de dashboard/PromQL exemplo) + ` ```promql ` se útil. Armadilhas (≥3): dashboard que ninguém olha; alertas ruidosos (alert fatigue); medir vanity metrics em vez de RED/USE. "Em entrevista" + "Veja também" (notas 14/16/18) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Cloud-native e produção/15 - Dashboards e alertas — Grafana.md"
git commit -m "feat(java): galho 17 nota 15 — dashboards e alertas (Grafana)"
```

### Task 17: Nota 16 — OpenTelemetry Collector e sampling de produção *(opus)*

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Cloud-native e produção/16 - OpenTelemetry Collector e sampling de produção.md`

- [ ] **Step 1 (WebFetch):** `opentelemetry.io/docs/collector/` + `opentelemetry.io/docs/concepts/sampling/` — confirmar Collector v0.154 (receivers/processors/exporters, separado), head vs tail-based.
- [ ] **Step 2 (escrever):** fase `adepto`. **OTel Collector v0.154** = componente **SEPARADO do app** (receivers → processors → exporters; OTLP in/out); a distinção **instrumentação no app** (Micrometer/OTel SDK gera o dado — é G16, LINKA `Microservices/19`) **vs Collector** (recebe/roteia, fora do app). **Sampling**: **head-based** (cedo, no SDK/app, por trace-id+%) vs **tail-based** (no Collector stateful, depois do trace completo — mantém traces com erro/lentidão; exige bufferizar). **RECEBE o seam do G16** (lá é código/config de export; aqui é operar o coletor e decidir sampling de produção). ` ```yaml ` (collector config receivers/processors/exporters) + ` ```text ` (head vs tail diagrama). Armadilhas (≥3): tail-based sem o Collector (impossível); head 100% em produção (custo); rodar o Collector como sidecar sem entender o trade-off. "Em entrevista" + "Veja também" (notas 13/17, G16 tracing) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Cloud-native e produção/16 - OpenTelemetry Collector e sampling de produção.md"
git commit -m "feat(java): galho 17 nota 16 — OpenTelemetry Collector e sampling de produção"
```

### Task 18: Nota 17 — Logs estruturados em produção

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Cloud-native e produção/17 - Logs estruturados em produção.md`

- [ ] **Step 1 (WebFetch):** `docs.spring.io/spring-boot/reference/features/logging.html` + `spring.io/blog/2024/08/23/structured-logging-in-spring-boot-3-4/` — confirmar structured logging desde Boot 3.4, ECS/GELF/Logstash, MDC traceId.
- [ ] **Step 2 (escrever):** fase `adepto`. **Structured logging nativo desde Boot 3.4** (`logging.structured.format.console=ecs`; formatos **ECS/GELF/Logstash** JSON out-of-the-box); **correlação traceId/spanId via MDC** (com tracing ativo — LINKA G16); **agregação** (Loki/ELK, conceitual). Por que JSON > texto em produção (parse/query/pivot log↔trace). ` ```yaml ` (logging.structured) + ` ```json ` (log estruturado com traceId). Armadilhas (≥3): log de texto não-parseável em produção; logar dado sensível (PII); não correlacionar com traceId (impossível pivotar log↔trace). "Em entrevista" + "Veja também" (notas 13/16, G16 tracing) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Cloud-native e produção/17 - Logs estruturados em produção.md"
git commit -m "feat(java): galho 17 nota 17 — logs estruturados em produção"
```

### Task 19: Review da fase Adepto (04-17)

- [ ] **Step 1:** dispatch de subagente revisor lendo as 14 notas. Checa: frontmatter+`fase: adepto`; estrutura H2 (≥3 H3; ≥3 armadilhas); **fronteira respeitada** (nota 08 LINKA G3 AOT/JIT; nota 10 LINKA G8 Actuator; nota 16 LINKA G16 tracing — NÃO re-explicam); **versões corretas** (GraalVM 25, native-build-tools 1.1.2, Spring AOT desde 3.0, probes default true/sem startup probe, graceful default+30s, jarmode=tools, MaxRAMPercentage 25.0, Jib 3.5.x, Micrometer 1.17/Prometheus 3.12/Grafana 13/Collector v0.154, structured logging Boot 3.4); **nota 13 apresenta o seam de 3 pontas**; **nota 11 tem o Deployment YAML ilustrativo mas NÃO ensina operar cluster**; zero fabricação/estatística; zero wikilink galho 18; "Em entrevista" completo (tabela vocab); code/config válido (Dockerfile/yaml/k8s bem-formado, flags cravados).
- [ ] **Step 2:** fix loop até aprovado. Se corrige, commit `fix(java): galho 17 — ajustes da fase Adepto`.

---

## Fase Magus (notas 18-22)

### Task 20: Nota 18 — Profiling e diagnóstico sob carga, produção

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Cloud-native e produção/18 - Profiling e diagnóstico sob carga — produção.md`

- [ ] **Step 1 (WebFetch):** `docs.spring.io` (production diagnostics) — reaproveitar; o miolo de heap/JFR/GC é do G3 (link-back, não re-pesquisar a mecânica).
- [ ] **Step 2 (escrever):** fase `magus`. O **workflow de incidente em produção** (sintoma → qual sinal → qual ferramenta → correlacionar com o stack de obs das notas 14-17). Heap dump, thread dump, GC log sob carga, JFR contínuo — **tudo é mecânica do Galho 3 (LINKA pesado `JVM/12`/`JVM/13`/`JVM/10`/`JVM/11`), NÃO re-explica**; aqui é o **ângulo operacional/cluster** (como esses sinais entram na rotina). **Distinção com JMH/G13** (microbenchmark de código ≠ profiling de produção — LINKA `Testes/18`). ` ```text ` (árvore de decisão de incidente) + ` ```bash ` (jcmd/JFR trigger — curto, apontando G3). Armadilhas (≥3): tirar heap dump num pod sob OOM e derrubá-lo; confundir microbenchmark (G13) com profiling de produção; profiling sem correlacionar com métricas/traces. "Em entrevista" + "Veja também" (notas 19/13, G3 JFR/Diagnóstico, G13 JMH) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Cloud-native e produção/18 - Profiling e diagnóstico sob carga — produção.md"
git commit -m "feat(java): galho 17 nota 18 — profiling e diagnóstico sob carga (produção)"
```

### Task 21: Nota 19 — Continuous profiling no cluster, Pyroscope e async-profiler

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Cloud-native e produção/19 - Continuous profiling no cluster — Pyroscope e async-profiler.md`

- [ ] **Step 1 (WebFetch):** `grafana.com/docs/pyroscope/latest/` + `grafana.com/docs/pyroscope/latest/configure-client/language-sdks/java/` — confirmar Pyroscope 2.x, async-profiler para Java, correlação.
- [ ] **Step 2 (escrever):** fase `magus`. O **4º sinal emergente**: profiling **contínuo** de toda a frota. **Grafana Pyroscope 2.x** (multi-tenant; usa **async-profiler** por baixo para Java; saída JFR); **correlacionar profile↔métrica↔log↔trace** ("o flamegraph do span lento"). **Distinto do JFR local (G3)**: aqui é agregação distribuída na plataforma, contínua, com baixo overhead. ` ```yaml ` (config do agent Pyroscope) + ` ```text ` (flamegraph conceitual). Armadilhas (≥3): confundir com JFR pontual do G3; overhead de profiling agressivo em produção; profile sem correlação (flamegraph órfão). "Em entrevista" + "Veja também" (notas 18/13, G3 JFR) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Cloud-native e produção/19 - Continuous profiling no cluster — Pyroscope e async-profiler.md"
git commit -m "feat(java): galho 17 nota 19 — continuous profiling no cluster (Pyroscope e async-profiler)"
```

### Task 22: Nota 20 — CI/CD e o caminho até produção

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Cloud-native e produção/20 - CI-CD e o caminho até produção.md`

- [ ] **Step 1 (WebFetch):** `docs.spring.io` + `buildpacks.io` (o passo de imagem no CI) — confirmar o framing; SBOM é G15 (link).
- [ ] **Step 2 (escrever):** fase `magus`. O **pipeline** build→test→imagem→deploy; o gate de qualidade (quality gates — LINKA `Build/16` se existir, ou G15); **supply chain no deploy** (assinar imagem, **SBOM** — LINKA `Build/18 - Supply chain e SBOM`); **GitOps** (conceitual — repo declara estado desejado, sem aprofundar ferramenta); estratégias de deploy (recap rolling/blue-green/canary da nota 12). ` ```yaml ` (pipeline conceitual build→image→deploy) + ` ```text ` (fluxo). Armadilhas (≥3): build de imagem fora do CI (não-reprodutível); deploy sem SBOM/assinatura; promover artefato diferente do testado. "Em entrevista" + "Veja também" (notas 12/22, G15 SBOM) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Cloud-native e produção/20 - CI-CD e o caminho até produção.md"
git commit -m "feat(java): galho 17 nota 20 — CI/CD e o caminho até produção"
```

### Task 23: Nota 21 — Native vs JVM, a decisão honesta *(opus)*

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Cloud-native e produção/21 - Native vs JVM — a decisão honesta.md`

- [ ] **Step 1 (WebFetch):** `docs.spring.io/spring-boot/reference/packaging/native-image/introducing-graalvm-native-images.html` + `graalvm.org` — confirmar os trade-offs pra decisão.
- [ ] **Step 2 (escrever):** fase `magus`. O framework de decisão com tudo na mão: **quando native vale** (serverless/FaaS, scale-to-zero, CLI, alta densidade, startup domina o SLA) **vs quando a JVM tradicional vence** (throughput de pico via JIT — LINKA `JVM/07`/`JVM/14`; build rápido; dinamismo/agentes; libs sem reachability metadata); o custo de build/CI da native (notas 08/09); o trade-off de **plataforma, não upgrade**. **Sem dogma** — "quando X E quando Y". ` ```text ` (tabela/árvore de decisão native vs JVM). Armadilhas (≥3): migrar pra native por hype (sem startup-bound real); subestimar o custo de build/CI; assumir paridade de throughput. "Em entrevista" (3+ sentenças, trade-off) + "Veja também" (notas 08/09/22, G3 JIT) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Cloud-native e produção/21 - Native vs JVM — a decisão honesta.md"
git commit -m "feat(java): galho 17 nota 21 — native vs JVM (a decisão honesta)"
```

### Task 24: Nota 22 — Capstone, do jar ao cluster *(opus, síntese)*

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Cloud-native e produção/22 - Capstone — do jar ao cluster.md`

- [ ] **Step 1 (WebFetch):** `docs.spring.io/spring-boot/reference/` — confirmar a sintaxe dos trechos do fluxo ponta a ponta.
- [ ] **Step 2 (escrever):** fase `magus`. **Um serviço Spring levado a produção ponta a ponta** (`order-service`): layered jar → imagem (Dockerfile/Buildpacks/Jib) → JVM container-aware → probes + graceful shutdown → Deployment YAML → métricas/Prometheus/Grafana + trace/Collector + logs estruturados → CI/CD. **Tabela de decisão** (Dockerfile vs Buildpacks vs Jib; JVM vs native; head vs tail sampling; quando cada coisa). **Cheatsheet nota→problema** usando os **títulos EXATOS** das 22 notas. Munição de entrevista de plataforma/SRE. ` ```text ` (fluxo + tabela) + ` ```yaml `/` ```dockerfile ` (trechos do fluxo). Armadilhas de raciocínio (≥3): "production-ready é só adicionar Actuator"; "tudo deve ser native"; "observabilidade é só ligar o Prometheus". "Em entrevista" + "Veja também" (todas as fases + MOC) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Cloud-native e produção/22 - Capstone — do jar ao cluster.md"
git commit -m "feat(java): galho 17 nota 22 — capstone (do jar ao cluster)"
```

### Task 25: Review da fase Magus (18-22)

- [ ] **Step 1:** dispatch de subagente revisor lendo as 5 notas. Checa: frontmatter+`fase: magus`; estrutura; **nota 18 NÃO re-explica heap/JFR/GC** (LINKA G3) e distingue JMH/G13; **nota 19 distingue do JFR local do G3**; **nota 21 sem dogma** (quando X E quando Y); **capstone usa títulos EXATOS das 22 notas** (sem inventar — lição G12/G16); zero fabricação/estatística (sem % de adoção de k8s/native); zero wikilink galho 18; tabela de decisão presente; **a tese honesta fecha o arco (21)**.
- [ ] **Step 2:** fix loop até aprovado. Se corrige, commit `fix(java): galho 17 — ajustes da fase Magus`.

---

## Task 26: MOC do galho (`index.md`)

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Cloud-native e produção/index.md`

- [ ] **Step 1 (escrever):** `type: moc`, `status: growing`, `publish: true`, `created`/`updated: 2026-06-12`, `title: "Cloud-native e produção"`, tags `java`/`cloud-native`/`moc`, aliases `["Cloud-native e produção", "Cloud-native", "Produção", "Containers e Kubernetes", "GraalVM Native Image", "Observabilidade de produção", "Galho 17 - Cloud-native"]`. Conteúdo conforme spec §3.2:
  - `> [!abstract] TL;DR` (galho cobre levar um serviço Java do jar ao cluster e operá-lo; tese: production-ready = postura, não feature; native = trade-off de plataforma; **22 notas em 3 fases**)
  - "Sobre este galho" + audiência + nota de galho HÍBRIDO com poda reversa modesta + **integração intensa** (~23 ganchos) + **fronteira-assinatura sêxtupla** + **seam de observabilidade de 3 pontas** (G3/G16/G17)
  - 3 H2 (`## Iniciado` / `## Adepto` / `## Magus`) com wikilinks pras 22 notas (1 linha descritiva cada — títulos EXATOS dos arquivos)
  - **5 rotas alternativas** (Completa 01→22; Entrevista internacional 01→02→08→10→12→13→16→21→22; Containerização 02→03→04→05→06→07; Native image 08→09→21; Observabilidade de operação 13→14→15→16→17→18→19)
  - "Veja também" (Trilha central, G3 JVM/JFR/GC, G8 Actuator, G15 Build/SBOM, G16 Microservices/tracing/mesh, G13 Testes/JMH, Dicionário; Galho 18 OCP = texto "(planejado)" SEM wikilink)
  - Dataview "Todas as notas" (TABLE fase/status; **inline code nunca começa com `=`** — [[feedback_dataview_inline_code]])
- [ ] **Step 2 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Cloud-native e produção/index.md"
git commit -m "feat(java): galho 17 MOC — Cloud-native e produção"
```

---

## Task 27: Expansão do Dicionário de Java

**Files:**
- Modify: `03-Dominios/Tecnologia/Java/Dicionário de Java.md`

- [ ] **Step 1 (conferir dups):** `grep -niE "^### (heap dump|JFR|Micrometer|OpenTelemetry|OTLP|sidecar|SBOM|twelve-factor|AOT|GraalVM)" "03-Dominios/Tecnologia/Java/Dicionário de Java.md"`. Onde já existir, **linkar/complementar** (não duplicar) — `heap dump`/`JFR` (G3), `Micrometer*`/`OpenTelemetry`/`OTLP`/`sidecar` (G16), `SBOM` (G15), `twelve-factor` (G16); `AOT` se existir do G3 → complementar com ângulo native image.
- [ ] **Step 2 (inserir):** inserir ~35 verbetes em ordem alfabética (case-insensitive, sem acento, ignorando símbolos) nas seções `## A`…`## Z`. Lista (spec §3.3): `AOT compilation (native)`, `async-profiler`, `blue-green deployment`, `bootBuildImage`, `canary deployment`, `cgroup (container)`, `Cloud Native Buildpacks`, `container image (OCI)`, `container-awareness (JVM)`, `continuous profiling`, `distroless`, `Dockerfile (multi-stage)`, `GitOps`, `GraalVM`, `GraalVM Native Image`, `graceful shutdown`, `Grafana`, `head-based sampling`, `health probe (liveness/readiness)`, `Jib`, `layered jar`, `liveness probe`, `MaxRAMPercentage`, `OpenTelemetry Collector`, `Paketo Buildpacks`, `Prometheus`, `reachability metadata`, `readiness probe`, `RED method`, `rolling deployment`, `Spring AOT`, `structured logging`, `tail-based sampling`, `USE method`, `UseContainerSupport`. Cada verbete: definição curta (1-3 linhas) PT-BR + `Veja também:` apontando pra nota canônica do galho. **Atualizar `updated: 2026-06-12`; NÃO recriar/reordenar verbetes existentes.** Conferir ordenação alfabética com o vizinho antes de inserir (lição: o galho 16 errou API Gateway/AMQP).
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Dicionário de Java.md"
git commit -m "feat(java): expande Dicionário de Java com verbetes do galho 17 (Cloud-native e produção)"
```

---

## Task 28: Ativação do MOC central

**Files:**
- Modify: `03-Dominios/Tecnologia/Java/index.md`

- [ ] **Step 1:** Ler `03-Dominios/Tecnologia/Java/index.md` e localizar a linha do Galho 17 (Task 0 confirmou: `17. Cloud-native e produção *(planejado)* — ...`).
- [ ] **Step 2:** Trocar por wikilink ativo (spec §3.4):
```markdown
17. [[03-Dominios/Tecnologia/Java/Cloud-native e produção/index|Cloud-native e produção]] — levar um serviço Java do jar ao cluster e operá-lo: containerização (Dockerfile multi-stage, layered jar, Buildpacks/Jib, distroless), GraalVM Native Image (AOT, Spring AOT, trade-offs), o contrato do app com o Kubernetes (health probes, config, graceful shutdown, resource limits), observabilidade de operação (Micrometer/Prometheus/Grafana, OpenTelemetry Collector, sampling, logs estruturados), profiling sob carga e continuous profiling, e CI/CD
```
Confirmar `updated: 2026-06-12`. **Não mexer no resto.** Galho 18 permanece `*(planejado)*`.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/index.md"
git commit -m "feat(java): ativa Galho 17 (Cloud-native e produção) no MOC central"
```

---

## Task 29: Poda reversa em `Spring Boot.md` (modesta, com callout)

**Files:**
- Modify: `03-Dominios/Tecnologia/Java/Backend/Spring Boot.md`

- [ ] **Step 1 (confirmar linhas):** rodar o grep do Task 0 Step 5 de novo (linhas podem ter mudado).
- [ ] **Step 2 (poda — `### Graceful shutdown`):** substituir a seção por callout:
```markdown
### Graceful shutdown

> [!nota] Migrado para galho próprio
> O graceful shutdown e o deploy sem downtime (SIGTERM/preStop, readiness REFUSING_TRAFFIC) foram expandidos no galho [[03-Dominios/Tecnologia/Java/Cloud-native e produção/index|Cloud-native e produção]]. Veja [[03-Dominios/Tecnologia/Java/Cloud-native e produção/12 - Graceful shutdown e deploy sem downtime|Graceful shutdown e deploy sem downtime]].
```
- [ ] **Step 3 (poda — `### Memory leak e GC tuning`):** substituir por callout que aponta G3 (mecânica) + nota 18 (produção), SEM re-explicar GC:
```markdown
### Memory leak e GC tuning

> [!nota] Migrado para galho próprio
> O diagnóstico de memória e o tuning de GC são tratados em profundidade no galho [[03-Dominios/Tecnologia/Java/JVM/index|JVM por dentro]] — veja [[03-Dominios/Tecnologia/Java/JVM/12 - Diagnóstico — heap dumps, thread dumps e jcmd|Diagnóstico (heap/thread dumps)]] e [[03-Dominios/Tecnologia/Java/JVM/11 - Tuning de GC — metodologia e prática|Tuning de GC]]. O ângulo de produção/cluster (workflow de incidente) está em [[03-Dominios/Tecnologia/Java/Cloud-native e produção/18 - Profiling e diagnóstico sob carga — produção|Profiling e diagnóstico sob carga]].
```
- [ ] **Step 4 (`## Actuator` — atualizar o parêntese):** trocar "(Observabilidade distribuída… Galho 17, planejado)" por wikilink ativo pra nota 13. Ler a linha (~91) e ajustar só o parêntese: `(Observabilidade de operação — métricas, OpenTelemetry, sampling — é o galho [[03-Dominios/Tecnologia/Java/Cloud-native e produção/13 - Observabilidade de operação — o panorama e os 3 seams|Cloud-native e produção]].)`.
- [ ] **Step 5 (não tocar):** `### Connection pool exausto`, `### N+1 queries`, `### LazyInitializationException`, `### @Transactional: problemas sutis`, `### Database migrations seguras (Flyway)`, callouts do G16 (`### API timeout`/`### Distributed tracing`), `## Camadas típicas`.
- [ ] **Step 6 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Backend/Spring Boot.md"
git commit -m "refactor(java): poda reversa do galho 17 — graceful shutdown e memory/GC viram callouts"
```

---

## Task 30: Quitação de ganchos "(planejado) G17"

**Files:**
- Modify: até ~22 arquivos dos Galhos 1-16 (§3.6 da spec)

- [ ] **Step 1 (confirmar):** rodar o grep do Task 0 Step 6 de novo; para cada arquivo, `grep -n "Galho 17"`.
- [ ] **Step 2 (quitar ganchos substantivos):** em cada arquivo, trocar a menção "Galho 17 (planejado)" por wikilink ativo pra nota-alvo (manter "(planejado)" só onde apontar pro Galho 18 ou onde for genuinamente fora de escopo — operar cluster/Vault). Mapa de destino (spec §3.6):
  - **Containers/native** → notas 08/09 (native) ou 03/04 (imagem): `Build/09 - Distribuições do JDK` (GraalVM/AOT→08), `Build/15 - Empacotamento` (layered jar em imagem→03/04), `Build/index`, `Spring Core e Boot/16 - SpringApplication` (native+tuning servidor→08/02), `JVM/01 - A JVM` (native image→08), `JVM/14 - Performance da JVM — síntese` (native image→08/21), `JavaFX/13 - Empacotamento` (native desktop — fronteira inversa; linka 08 ou mantém menção).
  - **Observabilidade** → notas 13/16/18/19: `Microservices/18` (coletor/dashboard→16), `/19` (operar→16), `/21` (operar resiliência→18), `/22` (operar mesh→menção, mesh-ops é fora de escopo), `Mensageria/26 - Observabilidade em mensageria` (infra→13), `Testes/18 - Performance — JMH` (profiling produção→18), `Spring Core e Boot/17 - Actuator` (observabilidade distribuída→13).
  - **k8s/secrets** → notas 10/11: `Microservices/07 - Discovery` (operar k8s→11 ou menção), `Microservices/12 - Config` (Vault operacional→menção, fora de escopo), `Segurança/index` (secrets/cloud security→11 ou menção).
  - **Índices/genéricos** → MOC do galho: `Web/index`, `Microservices/index`, `Microservices/01`, `Testes/21 - Capstone`.
- [ ] **Step 3 (commit):**
```bash
# git add nominal de cada arquivo tocado
git commit -m "docs(java): quita ganchos (planejado) do Galho 17 nos galhos anteriores"
```

---

## Task 31: Verificação final (wikilinks + spec compliance)

- [ ] **Step 1 (verificar-wikilinks):** rodar a skill `verificar-wikilinks` na pasta `03-Dominios/Tecnologia/Java/Cloud-native e produção/` + nos arquivos tocados (Dicionário, MOC central, Spring Boot.md, e os da Task 30). Corrigir quebrados. Atenção aos **títulos EXATOS** das notas-fronteira (em-dash `—`).
- [ ] **Step 2 (grep de sanidade):**
```bash
B="03-Dominios/Tecnologia/Java/Cloud-native e produção"
# zero wikilink pra galho inexistente (18/OCP)
grep -rEn "\[\[[^]]*(Galho 18|OCP)" "$B"/
# zero fabricação
grep -rEni "MedEspecialista|josenaldo|minha experiência|meu cluster|incidente de produção que" "$B"/
# zero percentual de adoção inventado
grep -rEn "[0-9]+% (dos|das|das empresas|usa|adota)" "$B"/
# 22 notas + index
ls "$B"/*.md | wc -l   # deve ser 23
# pipes escapados fora de tabela (revisar manual se houver)
grep -rn '\\|' "$B"/*.md | grep '\[\[' | head
```
- [ ] **Step 3 (review final):** dispatch de subagente revisor cross-galho — confere os 12 critérios de aceitação (spec §7): 22 notas 3/14/5, MOC com 5 rotas + dataview, Dicionário expandido (não recriado, dups linkados, ordenação alfabética conferida), MOC central ativado, **poda modesta executada (graceful shutdown + memory/GC → callouts; seções não-G17 intactas)**, **ganchos quitados**, fronteira sêxtupla respeitada (G3 não re-explicado), seam de 3 pontas presente (nota 13), versões cravadas, capstone com títulos exatos.
- [ ] **Step 4 (fix loop):** corrigir o que o review apontar; commit `fix(java): galho 17 — ajustes finais`.

---

## Task 32: Atualização da memória

**Files:**
- Modify: `/home/josenaldo/.claude/projects/-home-josenaldo-repos-personal-codex-technomanticus/memory/project_trilha_java.md` + `MEMORY.md`

- [ ] **Step 1:** Atualizar `project_trilha_java`: Galho 17 (Cloud-native e produção) **COMPLETO em main**; 22 notas (3/14/5) na pasta `Cloud-native e produção/`; versões cravadas (GraalVM 25/GFTC, native-build-tools 1.1.2, Spring AOT desde Boot 3.0, Boot 3.5.x+4.0.x, graceful default+30s, probes sem startup, MaxRAMPercentage 25.0/UseContainerSupport Java 10, jarmode=tools, Buildpacks/Jib 3.5.x, distroless, Micrometer 1.17/Prometheus 3.12/Grafana 13/OTel Collector v0.154, head vs tail sampling, structured logging Boot 3.4, Pyroscope 2.x); seam de observabilidade de 3 pontas (G3/G16/G17); fronteira sêxtupla; poda reversa modesta (graceful shutdown + memory/GC); ~23 ganchos G17 quitados; **bloco distribuído/produção FECHADO**; **falta só o Galho 18 (OCP)**. Atualizar a linha-índice em `MEMORY.md` (1-17 completos; próximo: 18 OCP). Não duplicar — editar.
- [ ] **Step 2:** (não commitar — memória fica fora do repo do vault.)

---

## Resumo de tasks

| Task | Conteúdo | Modelo |
|------|----------|--------|
| 0 | Pré-flight (pasta, paths de fronteira, baselines, linhas de poda/ganchos) | — |
| 1-3 | Notas 01-03 (Iniciado) | opus: 01; resto sonnet |
| 4 | Review Iniciado | sonnet |
| 5-18 | Notas 04-17 (Adepto, 14 notas) | opus: 08/13/16; resto sonnet |
| 19 | Review Adepto | sonnet |
| 20-24 | Notas 18-22 (Magus, 5 notas) | opus: 21/22; resto sonnet |
| 25 | Review Magus | sonnet |
| 26 | MOC do galho | sonnet |
| 27 | Expansão do Dicionário (~35 verbetes) | sonnet |
| 28 | Ativação do MOC central | sonnet |
| 29 | Poda reversa Spring Boot.md (2 callouts + 1 parêntese) | sonnet |
| 30 | Quitação de ~23 ganchos "(planejado) G17" | sonnet |
| 31 | Verificação final (wikilinks + compliance) | sonnet (review opus se necessário) |
| 32 | Atualização da memória | — |

**Total:** 22 notas + MOC + Dicionário + MOC central + poda modesta + quitação de ~23 ganchos + verificação. Opus em 01/08/13/16/21/22 (6 notas).
