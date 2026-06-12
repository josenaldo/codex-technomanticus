# Galho 16 — Microservices e sistemas distribuídos (Java Senior) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Criar o Galho 16 da trilha Java Senior — 24 notas atômicas (o modelo e a tese honesta, monorepo/multi-repo, 12-factor, panorama Spring Cloud, comunicação síncrona/assíncrona, service discovery, load balancing, gateway reativo/MVC, config centralizado, resiliência I-IV com Resilience4j, segurança entre serviços, tracing I-II, consistência CAP/PACELC, padrões de falha, service mesh, quando NÃO fazer microservices, capstone) em 3 fases + MOC do galho + expansão do Dicionário + ativação do MOC central + **poda reversa substancial** (3 seções de `Backend/Spring Boot.md` viram callouts) + **quitação de ~10 ganchos "(planejado) G16"** + correção de numeração defasada.

**Architecture:** Padrão galhos + 3 fases (Iniciado/Adepto/Magus). Pasta flat `03-Dominios/Java/Microservices e sistemas distribuídos/`, notas `publish: true` em PT-BR, numeração global 01-24 (5/14/5). **Galho HÍBRIDO** (pesquisa pesada + **poda reversa substancial**: as seções `## Spring Cloud — visão geral`, `### API timeout e cascading failures`/Resilience4j e `### Distributed tracing` de `Spring Boot.md` viram callouts "Migrado para galho próprio" + wikilinks — espelhando WebFlux/Spring Core no mesmo arquivo). **Fronteira-assinatura dupla**: G14 (saga/outbox/idempotência/event-driven/gRPC/Protobuf — atrás, linka) e G17 (containers/K8s/GraalVM native/deploy/operação de observabilidade — frente, texto "planejado"). **Tese honesta**: microservices é trade-off organizacional/de escala, não default técnico (o monólito modular basta); a rede é o inimigo (resiliência não é opcional); o ecossistema se moveu (Zuul/Ribbon/Hystrix morreram, Sleuth→Micrometer Tracing, OpenFeign→`@HttpExchange`). Galhos 17/18 = texto "(planejado)", sem wikilink. **Direto na `main`** ([[feedback_galhos_direto_main]]); push manual do usuário.

**Tech Stack:** Obsidian Flavored Markdown, frontmatter YAML, wikilinks, callouts, Dataview, Quartz v4. Verificação via WebFetch (spring.io/projects/spring-cloud, docs.spring.io, resilience4j.readme.io, micrometer.io, opentelemetry.io, 12factor.net, martinfowler.com, istio.io, linkerd.io).

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
  - microservices
  - <fase>
  - <1-3 tags de conceito: spring-cloud, discovery, gateway, resiliencia, resilience4j, circuit-breaker, tracing, observability, consistencia, service-mesh, config, load-balancing, feign, seguranca, arquitetura>
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
5. `## Na prática` — código/config **válido**; framing neutro; **NUNCA** 1ª pessoa, `MedEspecialista`, `josenaldo`, "da minha experiência", "na minha plataforma", "incidente de produção". Domínios neutros: `com.example`, serviços `order-service`/`payment-service`/`inventory-service`, classes `Order`/`Payment`/`OrderService`.
6. `## Armadilhas` — ≥2 (Iniciado) / ≥3 (Adepto/Magus). Cada uma: `### (N) Título` + descrição + exemplo curto + fix em 1 linha (H3 numerado, NÃO callout `[!warning]`).
7. `## Em entrevista` — `### Frase pronta (inglês)` com **3+ sentenças** + `### Vocabulário` **6+ termos** em tabela `| Termo PT | Termo EN |`.
8. `## Veja também` — wikilinks SEM backticks, SEM âncoras same-file. Sempre: notas do galho + `[[03-Dominios/Java/Microservices e sistemas distribuídos/index|Microservices e sistemas distribuídos (MOC do galho)]]` + `[[03-Dominios/Java/index|Trilha Java]]` + (quando aplicável) a nota da fronteira + verbetes do Dicionário.
9. `## Referências` — docs oficiais consultadas.

**Tamanho:** 200-500 linhas (densas até 600 — limite de [[feedback_notas_atomicas]]). Se passar de 600, dividir nota (não galho).

**Registro Feynman** (de [[feedback_enriquecimento_feynman]]) onde couber: analogias (circuit breaker = disjuntor elétrico; bulkhead = compartimentos estanques do navio; service registry = lista telefônica; gateway = portaria do prédio; eventual consistency = "todo mundo concorda, só não ao mesmo tempo"; sidecar = "carona ao lado do serviço"), perguntas retóricas, callouts. Sem inflar.

**Restrições absolutas:**
- **FRONTEIRA-ASSINATURA (linkar de volta, NUNCA re-explicar).** Mapeamento de link-back (paths confirmados na Task 0):
  - **G14 (Mensageria) — atrás:** saga → `03-Dominios/Java/Mensageria/22 - Saga — transações distribuídas por eventos`; idempotência → `Mensageria/20 - Idempotência — o pilar do at-least-once`; outbox → `Mensageria/21 - O padrão Outbox`; event sourcing/CQRS → `Mensageria/23 - Event sourcing e CQRS`; gRPC → `Mensageria/28 - gRPC em Java — RPC síncrono sobre HTTP_2`; Protobuf → `Mensageria/27 - Protocol Buffers — a IDL e a serialização binária`. **NÃO re-explicar saga/outbox/idempotência/gRPC.**
  - **G12 (Segurança):** OAuth2/OIDC/JWT/filter chain → `03-Dominios/Java/Segurança/12 - OAuth2 e OIDC Client e os grant types` + `Segurança/index`. **A nota 17 cobre só propagação distribuída (token relay).**
  - **G11 (Reativa):** WebFlux/Netty/backpressure → `03-Dominios/Java/Programação Reativa/10 - Spring WebFlux — o stack não-bloqueante sobre Netty e o DispatcherHandler` + `Programação Reativa/index`.
  - **G9 (Web/REST):** clientes HTTP/RestClient → `03-Dominios/Java/Web e APIs REST/15 - Clientes HTTP — RestClient, WebClient, RestTemplate`.
  - **G15 (Build):** multi-módulo/BOM → `03-Dominios/Java/Build e tooling/12 - Projetos multi-módulo`.
  - **G13 (Testes):** contract testing/Pact → `03-Dominios/Java/Testes/20 - Contract testing — Pact`.
- **Galhos 17/18 só como texto "(planejado)", SEM wikilink.** Greps de review checam `\[\[[^]]*(Galho (17|18)|container|Docker|Kubernetes|native image|GraalVM native|deploy)`.
- Sem fabricação ([[feedback_no_fabrication]]); domínios neutros. **Zero estatística de adoção/market-share inventada** (o pré-flight não achou fonte — **proibido citar "X% das empresas usam microservices/Istio/Kafka"**); números só com fonte verificável.
- **Pesquisa pras partes version-specific (quase todas as notas):** WebFetch no Step 1. **Fatos cravados no pré-flight (2026-06-12) — re-confirmar, são a base:**
  - **Spring Cloud release train:** **2025.1.x "Oakwood"** (sobre **Spring Boot 4 / Spring Framework 7**, módulos em **5.0.0**, lançado 24-25/nov/2025; Jackson 3, JSpecify) coexistindo com **2025.0.x "Northfields"** (Boot **3.5.x**). Estável mais recente: **2025.1.2 (11/jun/2026)**. **Boot 4 já saiu; 3.x ainda mantido.**
  - **Gateway — duas variantes:** reativa `spring-cloud-starter-gateway-server-webflux` (WebFlux/Netty) e **MVC** `spring-cloud-starter-gateway-server-webmvc` (servlet). **Starters renomeados no trem 2025.x** (antes `spring-cloud-starter-gateway` / `...-gateway-mvc`).
  - **Resilience4j:** estável **2.3.0 (jan/2025), baseline Java 17**. **v3/Java 21 = roadmap NÃO lançado** (sem artefato 3.x no Maven Central — descartar alucinações de "3.x em 2026"). Módulos: CircuitBreaker, RateLimiter, Retry, Bulkhead (**Semaphore** vs **ThreadPool**), TimeLimiter, Cache. CircuitBreaker: **CLOSED/OPEN/HALF_OPEN** + DISABLED/FORCED_OPEN; sliding window count/time; `failureRateThreshold` default **50%**, `slowCallDurationThreshold` default **60s**, `minimumNumberOfCalls` default **100**. **Ordem dos aspectos:** `Retry(CircuitBreaker(RateLimiter(TimeLimiter(Bulkhead(fn)))))`. Starter Boot 3: `resilience4j-spring-boot3`. Abstração: **Spring Cloud Circuit Breaker** (`spring-cloud-starter-circuitbreaker-resilience4j`).
  - **O que morreu:** **Ribbon, Hystrix, Zuul(1) removidos no trem 2020.0.0 "Ilford" (22/dez/2020)** → **LoadBalancer, Resilience4j (via Circuit Breaker), Gateway**. **Eureka NÃO morreu** (Netflix **5.0.2** @ Oakwood); só Archaius/Hystrix/Ribbon/Turbine/Zuul estão em maintenance mode.
  - **Discovery:** Eureka (client-side); **Consul** (`spring-cloud-starter-consul-discovery`, HTTP API + DNS + KV); **Spring Cloud Kubernetes** (`fabric8`/`client` starters + modo nativo DNS — server-side). Client-side vs server-side discovery.
  - **Tracing:** **Sleuth descontinuado** (foi pro `spring-attic`, **não roda em Boot 3.x**); migrado pra **Micrometer Tracing** desde **Boot 3.0**. **Micrometer Observation API** ("instrument once"). Bridges `io.micrometer:micrometer-tracing-bridge-otel` (→ OTel/OTLP) e `...-bridge-brave` (→ Zipkin). Propagação default **W3C**; traceId/spanId no **MDC**.
  - **OpenFeign feature-complete** desde **2022.0.0 "Kilburn" (16/dez/2022)**; a Spring recomenda **HTTP Interface clients `@HttpExchange`** (**Spring Framework 6.1+**, sobre RestClient/WebClient, sem precisar de Spring Cloud); **2025.1 adicionou LB + circuit breaking a HTTP service groups**.
  - **OpenTelemetry:** projeto **CNCF**, vendor-neutral; **spec (API) + SDK + semantic conventions + OTLP** (protocolo). Não é backend.
  - **Conceitos:** **CAP** (Brewer conjectura 2000; Gilbert-Lynch prova 2002 — sob partição, escolha C **ou** A). **PACELC** (Abadi 2010 blog / 2012 paper — se Partição: A/C; senão (Else): Latency/Consistency). **12-factor** (Adam Wiggins/Heroku, 2011); **Beyond the Twelve-Factor App** (Kevin Hoffman, 2016). **MonolithFirst**/**Microservice Premium** (Fowler, 2015). **Service mesh:** data plane (sidecar Envoy) + control plane; **Istio** (sidecar vs **ambient** = ztunnel+waypoint; ambient GA single-cluster desde **1.22**; doc ~**1.30.x**); **Linkerd** (**2.19**, micro-proxy em Rust).
- **Não re-explicar o que é de outro galho:** saga/outbox/idempotência/event-driven/gRPC/Protobuf → G14 (linkar); OAuth2/OIDC/JWT → G12 (linkar); RestClient/MVC → G9 (linkar); WebFlux/Netty/backpressure → G11 (linkar); multi-módulo/BOM → G15 (linkar); Pact → G13 (linkar). Containers/K8s/GraalVM native/deploy/operação-de-observabilidade/secrets-Vault-operacional → G17 (texto "planejado"); OCP → G18 (texto).
- Comparações justas (quando X E quando Y): microservices vs monólito modular, síncrono vs assíncrono, Eureka vs Consul vs k8s-native, client-side vs server-side discovery/LB, gateway reativo vs MVC, OpenFeign vs `@HttpExchange`, in-app resilience vs mesh, strong vs eventual consistency.
- Code fences: ` ```java ` (anotações/beans/config), ` ```yaml `/` ```properties ` (application.yml — Resilience4j/gateway routes/config/tracing), ` ```xml ` (POM com starters/coordenadas cravadas), ` ```kotlin ` (build.gradle.kts), ` ```bash ` (CLI), ` ```text ` (diagramas/waterfall/output). Sempre fechadas. **Usar os nomes de starter cravados** (`spring-cloud-starter-gateway-server-webflux`/`-webmvc`, `resilience4j-spring-boot3`).
- Commits: sem `Co-Authored-By: Claude`; sem `--no-verify`; `git add <path>` nominal (bot de backup roda em timer — NUNCA `-A`; guardar contra `.git/index.lock`); 1 commit por nota/artefato; direto na `main`; **sem push, sem deploy**. Subagents NÃO rodam git — o controlador commita.

**Modelo por nota:** sonnet por padrão; **opus** nas **01** (assinatura/tese), **04** (panorama Spring Cloud, version-heavy), **16** (composição de resiliência), **20** (consistência CAP/PACELC), **22** (service mesh), **23** (quando NÃO), **24** (capstone). (7 opus.)

**Fontes oficiais (base):**
- Spring Cloud: `https://spring.io/projects/spring-cloud` + `https://github.com/spring-cloud/spring-cloud-release/wiki`
- Docs: `https://docs.spring.io/spring-cloud-gateway/reference/`, `.../spring-cloud-config/reference/`, `.../spring-cloud-netflix/reference/`, `.../spring-cloud-consul/reference/`, `.../spring-cloud-kubernetes/reference/`, `.../spring-cloud-openfeign/reference/`, `.../spring-cloud-circuitbreaker/`, `https://docs.spring.io/spring-framework/reference/integration/rest-clients.html`, `https://docs.spring.io/spring-boot/reference/actuator/tracing.html`, `https://docs.spring.io/spring-security/reference/`
- Resilience4j: `https://resilience4j.readme.io/docs`
- Tracing: `https://docs.micrometer.io/micrometer/reference/observation.html` + `https://docs.micrometer.io/tracing/reference/` ; `https://opentelemetry.io/docs/`
- Conceitos: `https://12factor.net/` ; `https://martinfowler.com/` (microservices, MonolithFirst, MicroservicePremium) ; `https://istio.io/latest/docs/` ; `https://linkerd.io/`

---

## Task 0: Pré-flight — pasta, terreno, baselines e linhas de poda/ganchos

**Files:**
- Create: `03-Dominios/Java/Microservices e sistemas distribuídos/` (pasta)

- [ ] **Step 1:** Confirmar `main` limpa: `git status` e `git branch --show-current` (deve ser `main`).
- [ ] **Step 2:** Criar a pasta do galho: `mkdir -p "03-Dominios/Java/Microservices e sistemas distribuídos"`.
- [ ] **Step 3:** Confirmar os paths EXATOS das notas-fronteira (devem existir; usar nos wikilinks):
```bash
ls "03-Dominios/Java/Mensageria/22 - Saga — transações distribuídas por eventos.md" \
   "03-Dominios/Java/Mensageria/20 - Idempotência — o pilar do at-least-once.md" \
   "03-Dominios/Java/Mensageria/21 - O padrão Outbox.md" \
   "03-Dominios/Java/Mensageria/23 - Event sourcing e CQRS.md" \
   "03-Dominios/Java/Mensageria/28 - gRPC em Java — RPC síncrono sobre HTTP_2.md" \
   "03-Dominios/Java/Mensageria/27 - Protocol Buffers — a IDL e a serialização binária.md" \
   "03-Dominios/Java/Segurança/12 - OAuth2 e OIDC Client e os grant types.md" \
   "03-Dominios/Java/Programação Reativa/10 - Spring WebFlux — o stack não-bloqueante sobre Netty e o DispatcherHandler.md" \
   "03-Dominios/Java/Web e APIs REST/15 - Clientes HTTP — RestClient, WebClient, RestTemplate.md" \
   "03-Dominios/Java/Build e tooling/12 - Projetos multi-módulo.md" \
   "03-Dominios/Java/Testes/20 - Contract testing — Pact.md"
```
- [ ] **Step 4:** Confirmar a linha do Galho 16 no MOC central e o estado do Dicionário:
```bash
grep -n "16\. Microservices" "03-Dominios/Java/index.md"   # ~linha 49
grep -c "^### " "03-Dominios/Java/Dicionário de Java.md"   # baseline ~475
grep -ni "updated:" "03-Dominios/Java/Dicionário de Java.md" | head -1
```
- [ ] **Step 5:** Localizar os pontos de poda reversa em `Spring Boot.md` (números de linha p/ a Task 31):
```bash
grep -n "## Spring Cloud\|### API timeout\|cascading\|### Distributed tracing\|## Quando usar\|Resilience4j\|OpenFeign\|Micrometer Tracing" "03-Dominios/Java/Backend/Spring Boot.md"
```
- [ ] **Step 6:** Localizar os ~10 ganchos "(planejado) G16" p/ a Task 32:
```bash
grep -rn "Galho 16\|(planejado)" \
  "03-Dominios/Java/Web e APIs REST/15 - Clientes HTTP — RestClient, WebClient, RestTemplate.md" \
  "03-Dominios/Java/Web e APIs REST/index.md" \
  "03-Dominios/Java/Programação Reativa/index.md" \
  "03-Dominios/Java/Build e tooling/12 - Projetos multi-módulo.md" \
  "03-Dominios/Java/Segurança/12 - OAuth2 e OIDC Client e os grant types.md" \
  "03-Dominios/Java/Segurança/index.md" \
  "03-Dominios/Java/Mensageria/22 - Saga — transações distribuídas por eventos.md" \
  "03-Dominios/Java/Persistência de dados/index.md" \
  "03-Dominios/Java/Testes/20 - Contract testing — Pact.md" \
  "03-Dominios/Java/Testes/21 - Capstone — a estratégia de testes de uma app Spring production-grade.md"
```
- [ ] **Step 7:** Conferir possíveis verbetes duplicados no Dicionário (linkar, não duplicar): `grep -ni "^### \(retry\|saga\|Spring Cloud\|idempot\|backpressure\|circuit\|bulkhead\|service\)" "03-Dominios/Java/Dicionário de Java.md"`. Anotar quais já existem (esperado: `retry / retryWhen`, `saga`, `Spring Cloud Stream`).

> Nenhum commit nesta task (só pasta vazia — preenchida nas tasks seguintes; o `git add` da pasta acontece no 1º commit de nota).

---

## Fase Iniciado (notas 01-05)

> Cada nota: dispatch de subagente write-only com o texto da task + o bloco de Convenções. WebFetch no Step 1. Controlador commita após cada nota.

### Task 1: Nota 01 — O que são microservices e a tese honesta *(opus, assinatura)*

**Files:**
- Create: `03-Dominios/Java/Microservices e sistemas distribuídos/01 - O que são microservices e a tese honesta.md`

- [ ] **Step 1 (WebFetch):** `martinfowler.com/articles/microservices.html` + `martinfowler.com/bliki/MonolithFirst.html` + `martinfowler.com/bliki/MicroservicePremium.html` — confirmar as características, o "premium" e o argumento MonolithFirst.
- [ ] **Step 2 (escrever):** fase `iniciado`. O modelo: serviços pequenos, deployáveis independentemente, **database-per-service**, descentralização. **A tese-assinatura:** microservices é **trade-off organizacional/de escala, não default técnico** — o "microservice premium" (Fowler), **Conway's Law**, bounded contexts difíceis de acertar cedo; o **monólito modular** (Newman) geralmente basta. A fronteira dupla (G14 atrás / G17 frente). Aponta a nota 23 (quando NÃO). Armadilhas (≥2): microservices como default; dividir por camada técnica em vez de business capability. "Em entrevista" (3+ sentenças com trade-off) + "Veja também" (notas 02/05/23, Trilha) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Java/Microservices e sistemas distribuídos/01 - O que são microservices e a tese honesta.md"
git commit -m "feat(java): galho 16 nota 01 — o que são microservices e a tese honesta"
```

### Task 2: Nota 02 — Monorepo vs multi-repo

**Files:**
- Create: `03-Dominios/Java/Microservices e sistemas distribuídos/02 - Monorepo vs multi-repo.md`

- [ ] **Step 1 (WebFetch):** `martinfowler.com/` (monorepo / "MonorepoVsManyRepos" se existir) + uma fonte confiável sobre monorepo (ex.: `monorepo.tools`) — confirmar os trade-offs sem inventar números.
- [ ] **Step 2 (escrever):** fase `iniciado`. Topologia de **repositórios** (não de build — **fronteira G15**, a nota 12 multi-módulo é estrutura de UM build): **multi-repo** (um serviço, um repo, release/ownership independente) vs **monorepo** (vários serviços, um repo, tooling/refactor atômico unificado). Trade-offs: isolamento vs consistência atômica, CI, descoberta de código. **Fecha o gancho do Build G15** (linka `Build e tooling/12 - Projetos multi-módulo`). Armadilhas (≥2): confundir multi-módulo (build) com multi-repo (deploy); monorepo sem tooling vira gargalo de CI. "Em entrevista" + "Veja também" (notas 01/05, G15 multi-módulo) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Java/Microservices e sistemas distribuídos/02 - Monorepo vs multi-repo.md"
git commit -m "feat(java): galho 16 nota 02 — monorepo vs multi-repo"
```

### Task 3: Nota 03 — Os 12 fatores e o serviço cloud-native

**Files:**
- Create: `03-Dominios/Java/Microservices e sistemas distribuídos/03 - Os 12 fatores e o serviço cloud-native.md`

- [ ] **Step 1 (WebFetch):** `12factor.net/` (os 12 fatores) + `12factor.net/config` + `12factor.net/backing-services` + `12factor.net/processes` — confirmar os nomes e a redação.
- [ ] **Step 2 (escrever):** fase `iniciado`. Os 12 fatores (Wiggins/Heroku 2011) com foco na **arquitetura**: config no ambiente, backing services como recursos anexados, processos **stateless**, port binding, disposability, dev/prod parity, logs como event stream. **Deploy/build-release-run → G17 (texto "planejado")**. Menção a "Beyond the Twelve-Factor" (Hoffman 2016). Armadilhas (≥2): estado em memória do processo (quebra escala/disposability); config hardcoded no jar. "Em entrevista" + "Veja também" (notas 01/12, Trilha) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Java/Microservices e sistemas distribuídos/03 - Os 12 fatores e o serviço cloud-native.md"
git commit -m "feat(java): galho 16 nota 03 — os 12 fatores e o serviço cloud-native"
```

### Task 4: Nota 04 — Panorama do Spring Cloud — e o que morreu *(opus, version-heavy)*

**Files:**
- Create: `03-Dominios/Java/Microservices e sistemas distribuídos/04 - Panorama do Spring Cloud — e o que morreu.md`

- [ ] **Step 1 (WebFetch):** `spring.io/projects/spring-cloud` (release trains) + `github.com/spring-cloud/spring-cloud-release/wiki/Supported-Versions` + `cloud.spring.io/spring-cloud-netflix/multi/multi__modules_in_maintenance_mode.html` — confirmar **Oakwood 2025.1.x (Boot 4) / Northfields 2025.0.x (Boot 3.5.x)**, e o maintenance mode (Zuul/Ribbon/Hystrix mortos, **Eureka vivo**).
- [ ] **Step 2 (escrever):** fase `iniciado`. O **release train** (2025.1.x "Oakwood" sobre Boot 4/Framework 7; 2025.0.x "Northfields" sobre Boot 3.5.x; estável 2025.1.2); os projetos (Config, Gateway, LoadBalancer, OpenFeign, Circuit Breaker, Consul/Kubernetes — cada um aponta sua nota); **o que MORREU**: Zuul→Gateway, Ribbon→LoadBalancer (removido em 2020.0.0 Ilford), Hystrix→Resilience4j; Sleuth→Micrometer Tracing. **Eureka NÃO morreu**. **Absorve a tabela podada do tronco** (Task 31). ` ```text ` (tabela de projetos × morto/vivo). Armadilhas (≥2): usar Zuul/Ribbon/Hystrix hoje; achar que "Spring Cloud morreu junto com o Netflix stack" (Eureka/Gateway/LoadBalancer seguem). "Em entrevista" + "Veja também" (notas 06/08/13/18, Trilha) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Java/Microservices e sistemas distribuídos/04 - Panorama do Spring Cloud — e o que morreu.md"
git commit -m "feat(java): galho 16 nota 04 — panorama do Spring Cloud e o que morreu"
```

### Task 5: Nota 05 — Comunicação inter-serviços — síncrono vs assíncrono

**Files:**
- Create: `03-Dominios/Java/Microservices e sistemas distribuídos/05 - Comunicação inter-serviços — síncrono vs assíncrono.md`

- [ ] **Step 1 (WebFetch):** `martinfowler.com/articles/microservices.html` (smart endpoints/dumb pipes) + `docs.spring.io` (visão de comunicação) — confirmar o framing síncrono vs event-driven.
- [ ] **Step 2 (escrever):** fase `iniciado`. O eixo de decisão central: **síncrono** (REST/Feign/`@HttpExchange`, gRPC) — acoplamento temporal, simples, mas propaga falha em cadeia; vs **assíncrono** (eventos/mensageria) — desacopla, resiliente, mas eventual. **gRPC e saga/event-driven são fronteira G14 — LINKA, não re-explica** (→ `Mensageria/28 - gRPC`, `Mensageria/22 - Saga`). O resto do galho aprofunda o lado síncrono + resiliência. ` ```text ` (diagrama dos dois eixos). Armadilhas (≥2): tudo síncrono (acoplamento temporal, cascata de falha); async sem necessidade (complexidade eventual onde uma chamada bastava). "Em entrevista" + "Veja também" (notas 09/21, G14 saga/gRPC) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Java/Microservices e sistemas distribuídos/05 - Comunicação inter-serviços — síncrono vs assíncrono.md"
git commit -m "feat(java): galho 16 nota 05 — comunicação inter-serviços (síncrono vs assíncrono)"
```

### Task 6: Review da fase Iniciado (01-05)

- [ ] **Step 1:** dispatch de subagente revisor (spec compliance + qualidade) lendo as 5 notas. Checa: frontmatter+`fase`; estrutura H2; **zero fabricação** (grep `MedEspecialista|josenaldo|minha experiência|minha plataforma|incidente`); **zero estatística inventada** (grep `%`); **zero re-explicação de fronteira** (saga/gRPC/multi-módulo devem LINKAR G14/G15); zero wikilink pra galho 17/18; versões cravadas corretas (Oakwood/Northfields, Eureka vivo, Zuul/Ribbon/Hystrix mortos); "Em entrevista" 3+ sentenças + 6+ termos; **a tese honesta presente (01/05)**.
- [ ] **Step 2:** fix loop (implementador corrige) até aprovado. Se corrige, commit `fix(java): galho 16 — ajustes da fase Iniciado`.

---

## Fase Adepto (notas 06-19)

### Task 7: Nota 06 — Service discovery — o conceito e o Eureka

**Files:**
- Create: `03-Dominios/Java/Microservices e sistemas distribuídos/06 - Service discovery — o conceito e o Eureka.md`

- [ ] **Step 1 (WebFetch):** `docs.spring.io/spring-cloud-netflix/reference/spring-cloud-netflix.html` — confirmar Eureka server/client, registro/heartbeat, e que **Eureka NÃO está em maintenance mode** (Netflix 5.0.2).
- [ ] **Step 2 (escrever):** fase `adepto`. **Client-side vs server-side discovery** (o cliente consulta o registry e escolhe vs a infra resolve); o **service registry**; **Netflix Eureka** (server + client; registro/renovação/heartbeat/self-preservation). ` ```java ` (`@EnableEurekaServer`/`@EnableDiscoveryClient`) + ` ```yaml ` (eureka config). Armadilhas (≥3): client-side discovery quando o k8s já resolve (→ nota 07); heartbeat/TTL mal configurado (instâncias zumbis); self-preservation mal entendido. "Em entrevista" + "Veja também" (notas 07/08/04) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Java/Microservices e sistemas distribuídos/06 - Service discovery — o conceito e o Eureka.md"
git commit -m "feat(java): galho 16 nota 06 — service discovery e o Eureka"
```

### Task 8: Nota 07 — Discovery — Consul e Kubernetes-native

**Files:**
- Create: `03-Dominios/Java/Microservices e sistemas distribuídos/07 - Discovery — Consul e Kubernetes-native.md`

- [ ] **Step 1 (WebFetch):** `docs.spring.io/spring-cloud-consul/reference/discovery.html` + `docs.spring.io/spring-cloud-kubernetes/reference/discovery-client.html` + `.../discovery-kubernetes-native.html` — confirmar Consul (HTTP/DNS/KV) e os starters do k8s.
- [ ] **Step 2 (escrever):** fase `adepto`. **HashiCorp Consul** (Spring Cloud Consul, discovery via HTTP API + DNS, KV store, health checks); **Spring Cloud Kubernetes** (discovery nativo via API server / DNS do k8s, `fabric8`/`client` starters) — o modelo **server-side** que muitos preferem hoje (a infra resolve, sem registry na app). Quando cada um. ` ```yaml ` (consul/k8s discovery). Armadilhas (≥3): dois discoveries concorrendo (Eureka + k8s); ignorar o DNS nativo do k8s e duplicar; assumir que Consul é só discovery (é também KV/config). "Em entrevista" + "Veja também" (notas 06/08/12) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Java/Microservices e sistemas distribuídos/07 - Discovery — Consul e Kubernetes-native.md"
git commit -m "feat(java): galho 16 nota 07 — discovery (Consul e Kubernetes-native)"
```

### Task 9: Nota 08 — Client-side load balancing — Spring Cloud LoadBalancer

**Files:**
- Create: `03-Dominios/Java/Microservices e sistemas distribuídos/08 - Client-side load balancing — Spring Cloud LoadBalancer.md`

- [ ] **Step 1 (WebFetch):** `docs.spring.io/spring-cloud-commons/reference/` (spring-cloud-loadbalancer) + `cloud.spring.io/spring-cloud-netflix/multi/multi__modules_in_maintenance_mode.html` — confirmar **Ribbon removido → LoadBalancer** (blocking/reativo).
- [ ] **Step 2 (escrever):** fase `adepto`. **Ribbon morreu** (removido em 2020.0.0); o substituto é o **Spring Cloud LoadBalancer** (client-side LB, blocking e reativo; round-robin/random; `@LoadBalanced` no `RestClient`/`WebClient`/`RestTemplate`, URI `lb://service-id`); integração com discovery; **client-side LB vs server-side** (mesh/k8s Service balanceiam na infra). ` ```java ` (`@LoadBalanced` bean) + ` ```yaml `. Armadilhas (≥3): procurar Ribbon (não existe mais); client-side LB sobre um mesh que já balanceia (duplo balanceamento); esquecer o `@LoadBalanced` (resolve `lb://` como host literal). "Em entrevista" + "Veja também" (notas 06/09/22) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Java/Microservices e sistemas distribuídos/08 - Client-side load balancing — Spring Cloud LoadBalancer.md"
git commit -m "feat(java): galho 16 nota 08 — client-side load balancing (Spring Cloud LoadBalancer)"
```

### Task 10: Nota 09 — Comunicação síncrona — OpenFeign e @HttpExchange

**Files:**
- Create: `03-Dominios/Java/Microservices e sistemas distribuídos/09 - Comunicação síncrona — OpenFeign e HTTP Interface.md`

- [ ] **Step 1 (WebFetch):** `docs.spring.io/spring-cloud-openfeign/reference/` (feature-complete) + `docs.spring.io/spring-framework/reference/integration/rest-clients.html` (HTTP Interface `@HttpExchange`) + `spring.io/blog/2025/09/23/http-service-client-enhancements/` — confirmar Feign feature-complete e a recomendação do `@HttpExchange`.
- [ ] **Step 2 (escrever):** fase `adepto`. **OpenFeign** (`@FeignClient`, `@EnableFeignClients`) está **feature-complete desde 2022.0.0 (Kilburn, 16/dez/2022)**; a Spring recomenda os **HTTP Interface clients** (`@HttpExchange`, Framework 6.1+, sobre RestClient/WebClient — **não precisa de Spring Cloud**); **2025.1 trouxe LB + circuit breaking pra HTTP service groups**. **Liga G9 (RestClient — linka `Web e APIs REST/15`)**. **Fecha o gancho Feign do Web/REST.** ` ```java ` (`@FeignClient` + `@HttpExchange` lado a lado) + ` ```yaml ` (feign config). Armadilhas (≥3): começar projeto novo só com Feign (preferir `@HttpExchange`); confiar no Feign pra evoluir (feature-complete = só bugfix); chamada síncrona sem timeout/circuit breaker (→ notas 13/14). "Em entrevista" + "Veja também" (notas 05/16, G9 clientes HTTP) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Java/Microservices e sistemas distribuídos/09 - Comunicação síncrona — OpenFeign e HTTP Interface.md"
git commit -m "feat(java): galho 16 nota 09 — comunicação síncrona (OpenFeign e @HttpExchange)"
```

### Task 11: Nota 10 — API Gateway — papel, roteamento, predicates e filters

**Files:**
- Create: `03-Dominios/Java/Microservices e sistemas distribuídos/10 - API Gateway — papel, roteamento, predicates e filters.md`

- [ ] **Step 1 (WebFetch):** `docs.spring.io/spring-cloud-gateway/reference/` (routes, predicates, filters) — confirmar os tipos de predicate/filter e o modelo de roteamento.
- [ ] **Step 2 (escrever):** fase `adepto`. O **gateway** como porta única (roteamento + cross-cutting: auth, rate limit, CORS, rewrite, retry); **Spring Cloud Gateway**: **routes**, **predicates** (Path/Method/Header/Query/...) e **filters** (pre/post; `GatewayFilter` vs `GlobalFilter`); integração com discovery (`lb://`). A variante de runtime (reativo vs MVC) é a **nota 11**. ` ```yaml ` (routes/predicates/filters) + ` ```java ` (RouteLocator). Armadilhas (≥3): lógica de negócio no gateway (vira monólito disfarçado); gateway como SPOF sem HA; ordem de filters mal entendida. "Em entrevista" + "Veja também" (notas 11/17/08) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Java/Microservices e sistemas distribuídos/10 - API Gateway — papel, roteamento, predicates e filters.md"
git commit -m "feat(java): galho 16 nota 10 — API Gateway (papel, roteamento, predicates e filters)"
```

### Task 12: Nota 11 — Gateway reativo vs MVC — as duas variantes

**Files:**
- Create: `03-Dominios/Java/Microservices e sistemas distribuídos/11 - Gateway reativo vs MVC — as duas variantes.md`

- [ ] **Step 1 (WebFetch):** `docs.spring.io/spring-cloud-gateway/reference/spring-cloud-gateway-server-webflux/starter.html` + a ref do server-webmvc — confirmar os **starters renomeados** (`spring-cloud-starter-gateway-server-webflux` / `-webmvc`) no trem 2025.x.
- [ ] **Step 2 (escrever):** fase `adepto`. As **duas variantes vivas**: **reativo** (`spring-cloud-starter-gateway-server-webflux`, sobre WebFlux/Netty — **fronteira G11**, non-blocking, o original) vs **MVC** (`spring-cloud-starter-gateway-server-webmvc`, servlet/blocking — o novo, pra quem não quer o stack reativo); a **renomeação dos starters** no trem 2025.x (antes `spring-cloud-starter-gateway`/`...-gateway-mvc`); quando cada um. **Linka G11 (WebFlux/Netty), não re-explica o modelo reativo.** ` ```xml `/` ```kotlin ` (os dois starters) + ` ```yaml `. Armadilhas (≥3): usar o starter antigo (renomeado); gateway reativo num time sem experiência WebFlux (debug/backpressure → G11); misturar blocking I/O no gateway reativo. "Em entrevista" + "Veja também" (nota 10, G11 WebFlux) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Java/Microservices e sistemas distribuídos/11 - Gateway reativo vs MVC — as duas variantes.md"
git commit -m "feat(java): galho 16 nota 11 — gateway reativo vs MVC"
```

### Task 13: Nota 12 — Config centralizado — Spring Cloud Config

**Files:**
- Create: `03-Dominios/Java/Microservices e sistemas distribuídos/12 - Config centralizado — Spring Cloud Config.md`

- [ ] **Step 1 (WebFetch):** `docs.spring.io/spring-cloud-config/reference/` — confirmar Config Server/Client, backends, `@RefreshScope`, Bus.
- [ ] **Step 2 (escrever):** fase `adepto`. **Config Server** (backends Git/Vault/JDBC) + **Config Client**; `@RefreshScope` e o `/actuator/refresh`; **Spring Cloud Bus** (difundir refresh via broker); o trade-off vs config nativo do k8s (ConfigMap/Secret). **Segredos/Vault operacional → G17 (texto "planejado")**. Liga o fator "config no ambiente" da nota 03. ` ```yaml ` (config server + client). Armadilhas (≥3): segredo em Git plano (sem cripto/Vault); refresh sem `@RefreshScope` (bean não atualiza); config server como SPOF sem fallback local. "Em entrevista" + "Veja também" (notas 03/04, Trilha) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Java/Microservices e sistemas distribuídos/12 - Config centralizado — Spring Cloud Config.md"
git commit -m "feat(java): galho 16 nota 12 — config centralizado (Spring Cloud Config)"
```

### Task 14: Nota 13 — Resiliência I — a falha distribuída e o Circuit Breaker

**Files:**
- Create: `03-Dominios/Java/Microservices e sistemas distribuídos/13 - Resiliência I — a falha distribuída e o Circuit Breaker.md`

- [ ] **Step 1 (WebFetch):** `resilience4j.readme.io/docs/circuitbreaker` + `resilience4j.readme.io/docs/getting-started-3` — confirmar estados, sliding window, thresholds, starter `resilience4j-spring-boot3`, versão **2.3.0 (Java 17; v3 não lançado)**.
- [ ] **Step 2 (escrever):** fase `adepto`. **A rede é o inimigo**: falha parcial, latência, cascading failure. **Resilience4j 2.3.0** (Java 17; **v3/Java 21 é roadmap não lançado**); o **CircuitBreaker** (analogia disjuntor): estados **CLOSED/OPEN/HALF_OPEN** + DISABLED/FORCED_OPEN; **sliding window** count-based vs time-based; `failureRateThreshold` (default 50%), slow-call detection (`slowCallDurationThreshold` 60s), `minimumNumberOfCalls` (100); `@CircuitBreaker` + fallback. **Absorve o bloco Resilience4j podado (Task 31).** ` ```yaml ` (resilience4j config) + ` ```java ` (`@CircuitBreaker`). Armadilhas (≥3): sliding window mal dimensionada (abre cedo/tarde demais); CB sem fallback (exceção propaga); achar que existe Resilience4j 3.x estável. "Em entrevista" + "Veja também" (notas 14/16/21) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Java/Microservices e sistemas distribuídos/13 - Resiliência I — a falha distribuída e o Circuit Breaker.md"
git commit -m "feat(java): galho 16 nota 13 — resiliência I (circuit breaker)"
```

### Task 15: Nota 14 — Resiliência II — Retry e Time Limiter

**Files:**
- Create: `03-Dominios/Java/Microservices e sistemas distribuídos/14 - Resiliência II — Retry e Time Limiter.md`

- [ ] **Step 1 (WebFetch):** `resilience4j.readme.io/docs/retry` + `resilience4j.readme.io/docs/timeout` — confirmar config de retry (backoff) e TimeLimiter.
- [ ] **Step 2 (escrever):** fase `adepto`. **Retry** (`@Retry`, max-attempts, wait/exponential backoff, `retryExceptions`/`ignoreExceptions`) — **retry só em operações idempotentes/seguras → idempotência é G14, LINKA** (`Mensageria/20 - Idempotência`); **TimeLimiter** (`@TimeLimiter`, timeout de chamadas async/`CompletableFuture`). Por que retry sem idempotência é perigoso (duplicação). **Absorve parte do bloco podado.** ` ```yaml ` + ` ```java `. Armadilhas (≥3): retry sem idempotência (efeito colateral duplicado); retry storm sem backoff/jitter (amplifica a falha); TimeLimiter em chamada blocking (precisa ser async). "Em entrevista" + "Veja também" (notas 13/15/21, G14 idempotência) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Java/Microservices e sistemas distribuídos/14 - Resiliência II — Retry e Time Limiter.md"
git commit -m "feat(java): galho 16 nota 14 — resiliência II (retry e time limiter)"
```

### Task 16: Nota 15 — Resiliência III — Bulkhead e Rate Limiter

**Files:**
- Create: `03-Dominios/Java/Microservices e sistemas distribuídos/15 - Resiliência III — Bulkhead e Rate Limiter.md`

- [ ] **Step 1 (WebFetch):** `resilience4j.readme.io/docs/bulkhead` + `resilience4j.readme.io/docs/ratelimiter` — confirmar SemaphoreBulkhead vs ThreadPoolBulkhead e o rate limiter.
- [ ] **Step 2 (escrever):** fase `adepto`. **Bulkhead** (analogia compartimentos estanques do navio: isolar pra que a falha de um serviço não esgote todas as threads): **SemaphoreBulkhead** (limita concorrência na thread chamadora) vs **ThreadPoolBulkhead** (pool dedicado + fila, async); **RateLimiter** (limitar chamadas por janela). ` ```yaml ` + ` ```java `. Armadilhas (≥3): pool único compartilhado pra tudo (um serviço lento derruba todos); rate limit no lugar errado (no cliente em vez da borda); ThreadPoolBulkhead com chamada que precisa de contexto da thread (ThreadLocal/segurança). "Em entrevista" + "Veja também" (notas 13/16/21) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Java/Microservices e sistemas distribuídos/15 - Resiliência III — Bulkhead e Rate Limiter.md"
git commit -m "feat(java): galho 16 nota 15 — resiliência III (bulkhead e rate limiter)"
```

### Task 17: Nota 16 — Resiliência IV — compondo os padrões *(opus)*

**Files:**
- Create: `03-Dominios/Java/Microservices e sistemas distribuídos/16 - Resiliência IV — compondo os padrões.md`

- [ ] **Step 1 (WebFetch):** `resilience4j.readme.io/docs/getting-started-3` (aspect order) + `docs.spring.io/spring-cloud-circuitbreaker/` — confirmar a **ordem dos aspectos** `Retry(CB(RateLimiter(TimeLimiter(Bulkhead(fn)))))` e a abstração Spring Cloud Circuit Breaker.
- [ ] **Step 2 (escrever):** fase `adepto`. A **ordem dos aspectos** (`Retry( CircuitBreaker( RateLimiter( TimeLimiter( Bulkhead( fn ) ) ) ) )`) e por que importa (Retry é o mais externo; a issue conhecida do Retry inflar o contador do CB — workaround com `aspectOrder`); **fallback** (`fallbackMethod`, assinatura com `Throwable`); **Spring Cloud Circuit Breaker** (a abstração `CircuitBreakerFactory` sobre Resilience4j, `spring-cloud-starter-circuitbreaker-resilience4j`); o starter `resilience4j-spring-boot3` (requer actuator + aop). ` ```java ` (composição de anotações + fallback) + ` ```yaml `. Armadilhas (≥3): ordem errada inflando o CB (Retry dentro do CB); abstração escondendo o tuning (CircuitBreakerFactory genérico); fallback que mascara falha real (devolve dado errado silenciosamente). "Em entrevista" + "Veja também" (notas 13/14/15/21) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Java/Microservices e sistemas distribuídos/16 - Resiliência IV — compondo os padrões.md"
git commit -m "feat(java): galho 16 nota 16 — resiliência IV (compondo os padrões)"
```

### Task 18: Nota 17 — Segurança entre serviços

**Files:**
- Create: `03-Dominios/Java/Microservices e sistemas distribuídos/17 - Segurança entre serviços.md`

- [ ] **Step 1 (WebFetch):** `docs.spring.io/spring-security/reference/` (oauth2 client / client-credentials) + `docs.spring.io/spring-cloud-gateway/reference/` (TokenRelay filter) — confirmar token relay e client-credentials.
- [ ] **Step 2 (escrever):** fase `adepto`. Propagação de identidade entre serviços: **token relay** (repassar o JWT do usuário downstream, `TokenRelay` filter no gateway), **OAuth2 client-credentials** (serviço-a-serviço sem usuário), a borda no gateway. **O mecanismo OAuth2/OIDC/JWT/filter chain é G12 — LINKA, não re-explica** (`Segurança/12 - OAuth2`). Aqui é só o ângulo distribuído. Fronteira: **mTLS via mesh → nota 22**. **Fecha os ganchos da Segurança (12-OAuth2 e index).** ` ```java `/` ```yaml `. Armadilhas (≥3): repassar token sem validar audience/scope; serviço interno sem authz ("rede interna é confiável" = falso, zero-trust); client-credentials com segredo no código (→ config/Vault). "Em entrevista" + "Veja também" (nota 22, G12 OAuth2) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Java/Microservices e sistemas distribuídos/17 - Segurança entre serviços.md"
git commit -m "feat(java): galho 16 nota 17 — segurança entre serviços"
```

### Task 19: Nota 18 — Tracing distribuído I — correlação no código

**Files:**
- Create: `03-Dominios/Java/Microservices e sistemas distribuídos/18 - Tracing distribuído I — correlação no código.md`

- [ ] **Step 1 (WebFetch):** `docs.micrometer.io/micrometer/reference/observation.html` + `docs.micrometer.io/tracing/reference/index.html` + `github.com/spring-attic/spring-cloud-sleuth` — confirmar Observation API, Micrometer Tracing, **Sleuth descontinuado (attic, não roda Boot 3.x)**, propagação W3C, MDC.
- [ ] **Step 2 (escrever):** fase `adepto`. O problema: uma request atravessa N serviços. **Micrometer Observation API** ("instrument once") + **Micrometer Tracing** (substituiu o **Sleuth**, que foi pro attic e não roda em Boot 3.x; migrado desde Boot 3.0); **traceId/spanId**, propagação de contexto **W3C** entre serviços (headers), injeção no **MDC** pra logs correlacionados; context propagation ao trocar de thread. **Absorve o bloco Distributed tracing podado (parte código).** ` ```java ` (Observation) + ` ```yaml ` (tracing) + ` ```text ` (log com traceId). Armadilhas (≥3): log sem traceId (impossível correlacionar); perder o contexto ao trocar de thread (ThreadLocal — context propagation); achar que ainda se usa Sleuth no Boot 3. "Em entrevista" + "Veja também" (nota 19, G11 reativa context) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Java/Microservices e sistemas distribuídos/18 - Tracing distribuído I — correlação no código.md"
git commit -m "feat(java): galho 16 nota 18 — tracing distribuído I (correlação no código)"
```

### Task 20: Nota 19 — Tracing distribuído II — exportando o trace

**Files:**
- Create: `03-Dominios/Java/Microservices e sistemas distribuídos/19 - Tracing distribuído II — exportando o trace.md`

- [ ] **Step 1 (WebFetch):** `opentelemetry.io/docs/what-is-opentelemetry/` + `docs.micrometer.io/tracing/reference/index.html` (bridges) + `docs.spring.io/spring-boot/reference/actuator/tracing.html` — confirmar bridges `-otel`/`-brave`, OTLP, e a config de export/sampling.
- [ ] **Step 2 (escrever):** fase `adepto`. Os **bridges**: `micrometer-tracing-bridge-otel` (→ **OpenTelemetry**/OTLP) vs `micrometer-tracing-bridge-brave` (→ Zipkin); o que é **OpenTelemetry** (CNCF, vendor-neutral: spec + SDK + semantic conventions + **OTLP**); config de export (endpoint OTLP, `management.tracing.sampling.probability`) e leitura do **waterfall** (Jaeger/Zipkin). **SEAM G17 marcado (callout explícito):** *operar* coletor/dashboard/profiling/sampling-de-produção é **Galho 17 (planejado)** — aqui é só instrumentar e exportar. ` ```xml ` (bridge deps) + ` ```yaml ` (otlp endpoint/sampling) + ` ```text ` (waterfall). Armadilhas (≥3): sampling 100% em produção (custo/volume); confundir a instrumentação (Micrometer) com o backend (Jaeger/coletor); dois bridges no classpath ao mesmo tempo. "Em entrevista" + "Veja também" (nota 18; G17 "planejado" texto) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Java/Microservices e sistemas distribuídos/19 - Tracing distribuído II — exportando o trace.md"
git commit -m "feat(java): galho 16 nota 19 — tracing distribuído II (exportando o trace)"
```

### Task 21: Review da fase Adepto (06-19)

- [ ] **Step 1:** dispatch de subagente revisor lendo as 14 notas. Checa: frontmatter+`fase`; estrutura H2 (≥3 H3; ≥3 armadilhas); **fronteira respeitada** (nota 09 LINKA G9; nota 11 LINKA G11; nota 14 LINKA G14 idempotência; nota 17 LINKA G12 — NÃO re-explicam); **versões corretas** (Resilience4j 2.3.0/v3 não lançado, starters de gateway renomeados, Eureka vivo, Sleuth morto, OpenFeign feature-complete, ordem de aspectos `Retry(CB(...))`); **nota 19 marca o seam G17** (config de export sim, operação não); zero fabricação/estatística; zero wikilink galho 17/18; "Em entrevista" completo; code/config válido (YAML/Java bem-formado, nomes de starter cravados).
- [ ] **Step 2:** fix loop até aprovado. Se corrige, commit `fix(java): galho 16 — ajustes da fase Adepto`.

---

## Fase Magus (notas 20-24)

### Task 22: Nota 20 — Consistência em sistemas distribuídos *(opus)*

**Files:**
- Create: `03-Dominios/Java/Microservices e sistemas distribuídos/20 - Consistência em sistemas distribuídos.md`

- [ ] **Step 1 (WebFetch):** `en.wikipedia.org/wiki/CAP_theorem` + `en.wikipedia.org/wiki/PACELC_design_principle` + `martinfowler.com/articles/microservices.html` (decentralized data) — confirmar CAP (Brewer/Gilbert-Lynch), PACELC (Abadi), database-per-service.
- [ ] **Step 2 (escrever):** fase `magus`. **CAP** (Brewer 2000 conjectura; Gilbert-Lynch 2002 prova — sob partição, escolha C **ou** A; P não é negociável); a crítica **PACELC** (Abadi — sem partição, ainda há trade-off **Latency vs Consistency**); **strong vs eventual consistency**; **database-per-service** força eventual entre serviços. **Como SE resolve a consistência entre serviços (saga/outbox/idempotência) é G14 — LINKA, não re-deriva** (`Mensageria/22 - Saga`, `Mensageria/21 - Outbox`). ` ```text ` (CAP/PACELC diagrama). Armadilhas (≥3): esperar strong consistency entre serviços (não há transação distribuída barata); ignorar o trade-off latency/consistency (PACELC, presente o tempo todo); usar "eventual" como desculpa pra inconsistência permanente. "Em entrevista" + "Veja também" (notas 05/21, G14 saga/outbox) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Java/Microservices e sistemas distribuídos/20 - Consistência em sistemas distribuídos.md"
git commit -m "feat(java): galho 16 nota 20 — consistência em sistemas distribuídos"
```

### Task 23: Nota 21 — Os padrões de falha distribuída

**Files:**
- Create: `03-Dominios/Java/Microservices e sistemas distribuídos/21 - Os padrões de falha distribuída.md`

- [ ] **Step 1 (WebFetch):** `resilience4j.readme.io/docs` (overview) + `martinfowler.com/` (CircuitBreaker bliki, se existir) — confirmar os padrões; reaproveitar o que as notas 13-16 cravaram.
- [ ] **Step 2 (escrever):** fase `magus`. A síntese da resiliência no nível de **arquitetura** (não a config das notas 13-16): **timeouts** em toda chamada remota, **retries idempotentes** (→ G14), **cascading failure** e como o circuit breaker o quebra, **backpressure distribuído** (→ **fronteira G11** Reativa — linka `Programação Reativa/index`), graceful degradation. **Fecha o gancho da Reativa (index).** ` ```text ` (diagrama de cascata). Armadilhas (≥3): chamada remota sem timeout (thread presa pra sempre); degradação que vira falha total (sem fallback); retry amplificando a sobrecarga (retry storm). "Em entrevista" + "Veja também" (notas 13/16/20, G11 backpressure) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Java/Microservices e sistemas distribuídos/21 - Os padrões de falha distribuída.md"
git commit -m "feat(java): galho 16 nota 21 — os padrões de falha distribuída"
```

### Task 24: Nota 22 — Service mesh — quando a resiliência sai do código *(opus)*

**Files:**
- Create: `03-Dominios/Java/Microservices e sistemas distribuídos/22 - Service mesh — quando a resiliência sai do código.md`

- [ ] **Step 1 (WebFetch):** `istio.io/latest/docs/overview/dataplane-modes/` + `linkerd.io/2-edge/features/` — confirmar data/control plane, sidecar vs ambient (Istio), Linkerd, e o que o mesh entrega.
- [ ] **Step 2 (escrever):** fase `magus`. **Data plane** (sidecar proxy, ex. Envoy — analogia "carona ao lado do serviço") + **control plane**; o que o mesh entrega (mTLS, retries, circuit breaking, traffic shaping, observability) **movendo a lógica do código pra infra**; **Istio** (sidecar vs **ambient**/ztunnel+waypoint; ambient GA single-cluster desde 1.22; ~1.30.x) e **Linkerd** (2.19, micro-proxy em Rust); **a tese: quando o mesh torna Resilience4j redundante** (a tensão in-app vs malha — não duplicar retries/CB). **Conceitual, sem instalar infra (instalação/operação é G17).** ` ```text ` (diagrama sidecar). Armadilhas (≥3): resiliência duplicada (app + mesh fazem retry → multiplicação); adotar mesh sem necessidade (complexidade operacional); achar que mesh dispensa pensar resiliência (timeouts/budget ainda são decisão). "Em entrevista" + "Veja também" (notas 13/17/21) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Java/Microservices e sistemas distribuídos/22 - Service mesh — quando a resiliência sai do código.md"
git commit -m "feat(java): galho 16 nota 22 — service mesh"
```

### Task 25: Nota 23 — Quando NÃO fazer microservices *(opus, capstone de julgamento)*

**Files:**
- Create: `03-Dominios/Java/Microservices e sistemas distribuídos/23 - Quando NÃO fazer microservices.md`

- [ ] **Step 1 (WebFetch):** `martinfowler.com/bliki/MonolithFirst.html` + `martinfowler.com/bliki/MicroservicePremium.html` + `infoq.com/news/2020/05/monolith-decomposition-newman/` — confirmar MonolithFirst, premium, e o modular monolith de Newman (sem inventar citação literal).
- [ ] **Step 2 (escrever):** fase `magus`. O capstone do julgamento: os **custos reais** (rede não-confiável, consistência eventual, observabilidade distribuída, overhead operacional, complexidade cognitiva); **monólito modular** como default (Newman — "altamente subestimado") e o caminho **modular → extração** (strangler fig, quando a dor justifica); decompor por **business capability/bounded context**, não por camada técnica; Conway. Fecha o arco aberto na nota 01. ` ```text ` (árvore de decisão "devo extrair?"). Armadilhas (≥3): microservices prematuro (antes do product-market fit / sem escala que justifique); decompor por camada técnica (cria monólito distribuído); extrair sem bounded context claro. "Em entrevista" (3+ sentenças — quando NÃO) + "Veja também" (notas 01/02/20, Trilha) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Java/Microservices e sistemas distribuídos/23 - Quando NÃO fazer microservices.md"
git commit -m "feat(java): galho 16 nota 23 — quando NÃO fazer microservices"
```

### Task 26: Nota 24 — Capstone — uma requisição ponta a ponta na plataforma *(opus, síntese)*

**Files:**
- Create: `03-Dominios/Java/Microservices e sistemas distribuídos/24 - Capstone — uma requisição ponta a ponta na plataforma.md`

- [ ] **Step 1 (WebFetch):** `docs.spring.io/spring-cloud-gateway/reference/` + `resilience4j.readme.io/docs` — confirmar a sintaxe dos snippets do fluxo (gateway route + resilient call).
- [ ] **Step 2 (escrever):** fase `magus`. **Uma request atravessando a plataforma** (`order-service` → `payment-service`): entra pelo **gateway** (nota 10/11) → resolve via **discovery** (06/07) → **load balancing** (08) → chamada **resiliente** síncrona (timeout + circuit breaker + retry — 13/14/16) OU evento async (→ **G14**, linka) → **trace** propagado (traceId — 18/19) → **consistência eventual** (20). **Tabela de decisão** (síncrono vs async; quando gateway; quando mesh; Eureka vs k8s; quando resiliência in-app vs mesh). **Cheatsheet nota→problema** (usar os **títulos EXATOS** das 24 notas). Munição de entrevista. ` ```text ` (diagrama do fluxo + tabela) + ` ```java `/` ```yaml ` (trechos do fluxo). Armadilhas de raciocínio (≥3): "microservices é mais escalável por definição"; "circuit breaker resolve tudo"; "mesh dispensa pensar resiliência". "Em entrevista" + "Veja também" (todas as fases + MOC) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Java/Microservices e sistemas distribuídos/24 - Capstone — uma requisição ponta a ponta na plataforma.md"
git commit -m "feat(java): galho 16 nota 24 — capstone (requisição ponta a ponta)"
```

### Task 27: Review da fase Magus (20-24)

- [ ] **Step 1:** dispatch de subagente revisor lendo as 5 notas. Checa: frontmatter+`fase`; estrutura; **nota 20 LINKA G14** (não re-deriva saga/outbox); **nota 21 LINKA G11** (backpressure); **nota 22 conceitual** (não instala infra — operação é G17); versões (CAP/PACELC atribuições, Istio ambient/1.22, Linkerd 2.19); **capstone usa títulos EXATOS das 24 notas** (sem inventar — lição G12); zero fabricação/estatística (sem % de adoção de microservices/mesh); zero wikilink galho 17/18; tabela de decisão sem dogma; **a tese honesta fecha o arco (23)**.
- [ ] **Step 2:** fix loop até aprovado. Se corrige, commit `fix(java): galho 16 — ajustes da fase Magus`.

---

## Task 28: MOC do galho (`index.md`)

**Files:**
- Create: `03-Dominios/Java/Microservices e sistemas distribuídos/index.md`

- [ ] **Step 1 (escrever):** `type: moc`, `status: growing`, `publish: true`, `created`/`updated: 2026-06-12`, `title: "Microservices e sistemas distribuídos"`, tags `java`/`microservices`/`moc`, aliases `["Microservices e sistemas distribuídos", "Microservices", "Microsserviços", "Spring Cloud", "Sistemas distribuídos", "Galho 16 - Microservices"]`. Conteúdo conforme spec §3.2:
  - `> [!abstract] TL;DR` (galho cobre como vários serviços formam uma plataforma distribuída; tese: microservices = trade-off, não default; o monólito modular basta; a rede é o inimigo; **24 notas em 3 fases**)
  - "Sobre este galho" + audiência + nota de galho HÍBRIDO com **poda reversa substancial** (Spring Boot.md) + **fronteira-assinatura dupla** (G14 atrás / G17 frente)
  - 3 H2 (`## Iniciado` / `## Adepto` / `## Magus`) com wikilinks pras 24 notas (1 linha descritiva cada — usar títulos EXATOS dos arquivos)
  - **5 rotas alternativas** (Completa 01→24; Entrevista internacional 01→04→05→13→16→18→20→23→24; A plataforma Spring Cloud na prática 04→06→08→09→10→11→12; Resiliência 13→14→15→16→21; Arquitetura e julgamento 01→02→03→20→22→23)
  - "Veja também" (Trilha central, G14 Mensageria, G12 Segurança, G11 Reativa, G9 Web/REST, G15 Build, Dicionário; Galhos 17/18 = texto "(planejado)" SEM wikilink)
  - Dataview "Todas as notas" (TABLE fase/status; **inline code nunca começa com `=`** — [[feedback_dataview_inline_code]])
- [ ] **Step 2 (commit):**
```bash
git add "03-Dominios/Java/Microservices e sistemas distribuídos/index.md"
git commit -m "feat(java): galho 16 MOC — Microservices e sistemas distribuídos"
```

---

## Task 29: Expansão do Dicionário de Java

**Files:**
- Modify: `03-Dominios/Java/Dicionário de Java.md`

- [ ] **Step 1 (conferir dups):** `grep -ni "^### " "03-Dominios/Java/Dicionário de Java.md"` filtrando os candidatos a colisão (do Task 0 Step 7): `retry / retryWhen`, `saga`, `Spring Cloud Stream`, `idempotência`, `backpressure`. Onde já existir, **linkar/complementar** (não duplicar) — ex.: `retry` ganha o ângulo Resilience4j; `saga` aponta pra G14.
- [ ] **Step 2 (inserir):** inserir ~40 verbetes em ordem alfabética (case-insensitive, sem acento, ignorando símbolos) nas seções `## A`…`## Z` existentes. Lista (spec §3.3): `ambient mesh`, `API Gateway`, `backpressure distribuído`, `bounded context`, `Brave (tracer)`, `bulkhead`, `CAP theorem`, `cascading failure`, `circuit breaker`, `client-side discovery`, `client-side load balancing`, `Conway's Law`, `Consul`, `control plane`, `correlation ID`, `data plane`, `database-per-service`, `Eureka`, `eventual consistency`, `Feign / OpenFeign`, `@HttpExchange (HTTP Interface)`, `Istio`, `Linkerd`, `Micrometer Observation API`, `Micrometer Tracing`, `microservices`, `modular monolith (monólito modular)`, `monorepo`, `multi-repo`, `mTLS`, `OpenTelemetry`, `OTLP`, `PACELC`, `rate limiter`, `Resilience4j`, `service discovery`, `service mesh`, `service registry`, `sidecar`, `Spring Cloud`, `Spring Cloud Config`, `Spring Cloud Gateway`, `Spring Cloud LoadBalancer`, `strangler fig`, `time limiter`, `token relay`, `twelve-factor (12-factor)`, `traceId / spanId`, `Zuul`. Cada verbete: definição curta (1-3 linhas) PT-BR + `Veja também:` apontando pra nota canônica do galho. **Atualizar `updated: 2026-06-12`; NÃO recriar/reordenar verbetes existentes.**
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Java/Dicionário de Java.md"
git commit -m "feat(java): expande Dicionário de Java com verbetes do galho 16 (Microservices)"
```

---

## Task 30: Ativação do MOC central

**Files:**
- Modify: `03-Dominios/Java/index.md`

- [ ] **Step 1:** Ler `03-Dominios/Java/index.md` e localizar a linha do Galho 16 (Task 0 confirmou ~linha 49: `16. Microservices e sistemas distribuídos *(planejado)* — ...`).
- [ ] **Step 2:** Trocar por wikilink ativo (spec §3.4):
```markdown
16. [[03-Dominios/Java/Microservices e sistemas distribuídos/index|Microservices e sistemas distribuídos]] — o modelo e a tese honesta (microservices vs monólito modular), Spring Cloud (service discovery, gateway, config centralizado), resiliência com Resilience4j (circuit breaker, retry, bulkhead, rate limiter, time limiter), comunicação síncrona (OpenFeign/@HttpExchange), segurança entre serviços, tracing distribuído (Micrometer Tracing/OpenTelemetry), consistência (CAP/PACELC) e service mesh
```
Atualizar `updated: 2026-06-12`. **Não mexer no resto.** Galhos 17/18 permanecem `*(planejado)*`.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Java/index.md"
git commit -m "feat(java): ativa Galho 16 (Microservices) no MOC central"
```

---

## Task 31: Poda reversa em `Spring Boot.md` (substancial, com callout)

**Files:**
- Modify: `03-Dominios/Java/Backend/Spring Boot.md`

- [ ] **Step 1 (confirmar linhas):** rodar o grep do Task 0 Step 5 de novo (linhas podem ter mudado).
- [ ] **Step 2 (poda — `## Spring Cloud — visão geral`, ~102-175):** **substituir a seção inteira** (tabela de projetos + OpenFeign exemplo/config + "alternativa moderna") por um callout, espelhando o tratamento de WebFlux/Spring Core no mesmo arquivo:
```markdown
## Spring Cloud — visão geral

> [!nota] Migrado para galho próprio
> O ecossistema Spring Cloud (service discovery, gateway, config centralizado, OpenFeign, resiliência) foi expandido no galho [[03-Dominios/Java/Microservices e sistemas distribuídos/index|Microservices e sistemas distribuídos]]. Veja [[03-Dominios/Java/Microservices e sistemas distribuídos/04 - Panorama do Spring Cloud — e o que morreu|Panorama do Spring Cloud]], [[03-Dominios/Java/Microservices e sistemas distribuídos/06 - Service discovery — o conceito e o Eureka|Service discovery]], [[03-Dominios/Java/Microservices e sistemas distribuídos/09 - Comunicação síncrona — OpenFeign e HTTP Interface|OpenFeign e @HttpExchange]] e [[03-Dominios/Java/Microservices e sistemas distribuídos/10 - API Gateway — papel, roteamento, predicates e filters|API Gateway]].
```
- [ ] **Step 3 (poda — `### API timeout e cascading failures`/Resilience4j, ~577-619):** substituir por callout → notas 13/14/16:
```markdown
### API timeout e cascading failures

> [!nota] Migrado para galho próprio
> A resiliência com Resilience4j (circuit breaker, retry, time limiter, bulkhead, fallback) foi expandida no galho [[03-Dominios/Java/Microservices e sistemas distribuídos/index|Microservices e sistemas distribuídos]]. Veja [[03-Dominios/Java/Microservices e sistemas distribuídos/13 - Resiliência I — a falha distribuída e o Circuit Breaker|Circuit Breaker]], [[03-Dominios/Java/Microservices e sistemas distribuídos/14 - Resiliência II — Retry e Time Limiter|Retry e Time Limiter]] e [[03-Dominios/Java/Microservices e sistemas distribuídos/16 - Resiliência IV — compondo os padrões|compondo os padrões]].
```
- [ ] **Step 4 (poda — `### Distributed tracing`, ~672-691):** substituir por callout → notas 18/19:
```markdown
### Distributed tracing

> [!nota] Migrado para galho próprio
> O tracing distribuído (Micrometer Tracing, OpenTelemetry, propagação de contexto) foi expandido no galho [[03-Dominios/Java/Microservices e sistemas distribuídos/index|Microservices e sistemas distribuídos]]. Veja [[03-Dominios/Java/Microservices e sistemas distribuídos/18 - Tracing distribuído I — correlação no código|correlação no código]] e [[03-Dominios/Java/Microservices e sistemas distribuídos/19 - Tracing distribuído II — exportando o trace|exportando o trace]]. (A operação de coletores/dashboards de produção fica para o Galho 17, planejado.)
```
- [ ] **Step 5 (`## Quando usar`, ~697):** ajustar o bullet "Spring Cloud" pra apontar o wikilink da nota 04 (ou manter a menção curta + link). **NÃO TOCAR** nas seções `### Graceful shutdown`, `### Database migrations seguras (Flyway)`, `### Memory leak e GC tuning`, `### Connection pool exausto`, `### N+1 queries`, `### LazyInitializationException`, `### @Transactional`.
- [ ] **Step 6 (commit):**
```bash
git add "03-Dominios/Java/Backend/Spring Boot.md"
git commit -m "refactor(java): poda reversa do galho 16 — Spring Cloud/Resilience4j/tracing viram callouts"
```

---

## Task 32: Quitação de ganchos "(planejado) G16" + correção de numeração

**Files:**
- Modify: até 10 arquivos dos Galhos 9-15 (§3.6 da spec)

- [ ] **Step 1 (confirmar linhas):** rodar o grep do Task 0 Step 6 de novo.
- [ ] **Step 2 (quitar ganchos substantivos):** em cada arquivo abaixo, trocar a menção "Galho 16 (planejado)" pelo wikilink ativo (manter G17 como "(planejado)" onde aparecer junto):
  - `Web e APIs REST/15 - Clientes HTTP — RestClient, WebClient, RestTemplate.md` (~303): `@FeignClient ... Galho 16 (planejado)` → wikilink pra `09 - Comunicação síncrona — OpenFeign e HTTP Interface`.
  - `Web e APIs REST/index.md` (~32): "Microservices (Galho 16)" → wikilink pra `Microservices e sistemas distribuídos/index`.
  - `Programação Reativa/index.md` (~35): "resiliência/backpressure distribuído (Galho 16)" → wikilink pra `21 - Os padrões de falha distribuída`.
  - `Build e tooling/12 - Projetos multi-módulo.md` (~99, ~203): "topologia de repositórios ... Galho 16" → wikilink pra `02 - Monorepo vs multi-repo`.
  - `Segurança/12 - OAuth2 e OIDC Client e os grant types.md` (~88): "token relay ... Galho 16" → wikilink pra `17 - Segurança entre serviços`.
  - `Segurança/index.md` (~32): "segurança em microservices (Galho 16 planejado)" → wikilink pra `17 - Segurança entre serviços` (manter G17 "(planejado)").
  - `Mensageria/22 - Saga — transações distribuídas por eventos.md` (~205): "coordenação de sagas ... Galho 16" → wikilink pra `05 - Comunicação inter-serviços — síncrono vs assíncrono` (ou `24 - Capstone`).
  - `Persistência de dados/index.md` (~32): "dados distribuídos/saga (Galho 16)" → wikilink pra `20 - Consistência em sistemas distribuídos`.
  - `Testes/20 - Contract testing — Pact.md` (~107): "orquestração do broker ... Galho 16" → wikilink pra `Microservices e sistemas distribuídos/index` (menção de fronteira).
- [ ] **Step 3 (corrigir numeração defasada — `Testes/21`, ~192):** reescrever a frase "observabilidade (Galho 14, planejado), mensageria (Galho 16, planejado) e deploy/cloud (Galho 17, planejado)" pra refletir a numeração atual: **Mensageria é o Galho 14 (fechado)**; **Microservices é o Galho 16**; **Cloud-native/observabilidade de produção é o Galho 17 (planejado)**. Linkar Mensageria e Microservices (fechados), manter G17 "(planejado)".
- [ ] **Step 4 (commit):**
```bash
git add "03-Dominios/Java/Web e APIs REST/15 - Clientes HTTP — RestClient, WebClient, RestTemplate.md" \
        "03-Dominios/Java/Web e APIs REST/index.md" \
        "03-Dominios/Java/Programação Reativa/index.md" \
        "03-Dominios/Java/Build e tooling/12 - Projetos multi-módulo.md" \
        "03-Dominios/Java/Segurança/12 - OAuth2 e OIDC Client e os grant types.md" \
        "03-Dominios/Java/Segurança/index.md" \
        "03-Dominios/Java/Mensageria/22 - Saga — transações distribuídas por eventos.md" \
        "03-Dominios/Java/Persistência de dados/index.md" \
        "03-Dominios/Java/Testes/20 - Contract testing — Pact.md" \
        "03-Dominios/Java/Testes/21 - Capstone — a estratégia de testes de uma app Spring production-grade.md"
git commit -m "docs(java): quita ganchos (planejado) do Galho 16 e corrige numeração defasada"
```

---

## Task 33: Verificação final (wikilinks + spec compliance)

- [ ] **Step 1 (verificar-wikilinks):** rodar a skill `verificar-wikilinks` na pasta `03-Dominios/Java/Microservices e sistemas distribuídos/` + nos arquivos tocados (Dicionário, MOC central, Spring Boot.md, e os 10 da Task 32). Corrigir quebrados. Atenção aos **títulos EXATOS** das notas-fronteira (em-dash `—`) e do Dicionário.
- [ ] **Step 2 (grep de sanidade):**
```bash
# zero wikilink pra galho inexistente (17/18) ou conteúdo de produção
grep -rn "\[\[[^]]*\(Galho 1[78]\|container\|Docker\|Kubernetes\|native image\|GraalVM native\|deploy\)" "03-Dominios/Java/Microservices e sistemas distribuídos/"
# zero fabricação
grep -rni "MedEspecialista\|josenaldo\|minha experiência\|minha plataforma\|incidente de produção" "03-Dominios/Java/Microservices e sistemas distribuídos/"
# zero percentual de adoção inventado
grep -rn "% \(dos\|das\|usa\|adota\|das empresas\)" "03-Dominios/Java/Microservices e sistemas distribuídos/"
# Resilience4j 3.x não deve aparecer como versão estável
grep -rni "Resilience4j 3\|resilience4j-spring-boot3.*3\." "03-Dominios/Java/Microservices e sistemas distribuídos/"
# 24 notas + index
ls "03-Dominios/Java/Microservices e sistemas distribuídos/" | wc -l   # deve ser 25
```
- [ ] **Step 3 (review final):** dispatch de subagente revisor cross-galho — confere os 12 critérios de aceitação (spec §7): 24 notas 5/14/5, MOC com 5 rotas + dataview, Dicionário expandido (não recriado, dups linkados), MOC central ativado, **poda substancial executada (3 callouts; seções não-G16 intactas)**, **ganchos quitados + numeração corrigida**, fronteira dupla respeitada (G14 atrás / G17 frente), versões cravadas corretas, capstone com títulos exatos, seam G17 do tracing marcado.
- [ ] **Step 4 (fix loop):** corrigir o que o review apontar; commit `fix(java): galho 16 — ajustes finais`.

---

## Task 34: Atualização da memória

**Files:**
- Modify: `/home/josenaldo/.claude/projects/-home-josenaldo-repos-personal-codex-technomanticus/memory/project_trilha_java.md`

- [ ] **Step 1:** Atualizar o registro `project_trilha_java`: Galho 16 (Microservices e sistemas distribuídos) **COMPLETO em main**; 24 notas (5/14/5) na pasta `Microservices e sistemas distribuídos/`; versões cravadas (Spring Cloud 2025.1.x Oakwood/Boot 4 + 2025.0.x Northfields/Boot 3.5.x; Resilience4j 2.3.0/Java 17, v3 não lançado; Eureka vivo, Zuul/Ribbon/Hystrix mortos desde 2020.0.0; Sleuth→Micrometer Tracing; OpenFeign feature-complete→@HttpExchange Framework 6.1+; gateway starters renomeados webflux/webmvc; CAP/PACELC; Istio ambient GA 1.22/Linkerd 2.19); poda reversa de 3 seções do Spring Boot.md (Spring Cloud/Resilience4j/tracing → callouts); fronteira dupla G14 (saga/gRPC atrás) / G17 (containers/native/produção frente); próximo sugerido: **Galho 17 (Cloud-native e produção)**. Não duplicar — editar o arquivo existente. Atualizar também o índice `MEMORY.md` se a linha resumo mudar.
- [ ] **Step 2:** (não commitar — a memória fica fora do repo do vault.)

---

## Resumo de tasks

| Task | Conteúdo | Modelo |
|------|----------|--------|
| 0 | Pré-flight (pasta, paths de fronteira, baselines, linhas de poda/ganchos) | — |
| 1-5 | Notas 01-05 (Iniciado) | opus: 01/04; resto sonnet |
| 6 | Review Iniciado | sonnet |
| 7-20 | Notas 06-19 (Adepto, 14 notas) | opus: 16; resto sonnet |
| 21 | Review Adepto | sonnet |
| 22-26 | Notas 20-24 (Magus, 5 notas) | opus: 20/22/23/24; resto sonnet |
| 27 | Review Magus | sonnet |
| 28 | MOC do galho | sonnet |
| 29 | Expansão do Dicionário (~40 verbetes) | sonnet |
| 30 | Ativação do MOC central | sonnet |
| 31 | Poda reversa Spring Boot.md (3 callouts) | sonnet |
| 32 | Quitação de ganchos + correção de numeração | sonnet |
| 33 | Verificação final (wikilinks + compliance) | sonnet (review opus se necessário) |
| 34 | Atualização da memória | — |

**Total:** 24 notas + MOC + Dicionário + MOC central + poda substancial + quitação de ganchos + verificação. Opus em 01/04/16/20/22/23/24 (7 notas).
