---
title: "Spec — Galho 16 da trilha Java Senior (Microservices e sistemas distribuídos)"
date: 2026-06-12
author: Josenaldo
status: draft
type: spec
publish: false
---

# Spec — Galho 16 da trilha Java Senior (Microservices e sistemas distribuídos)

## 1. Contexto e motivação

Este é o **décimo sexto galho** da trilha Java Senior (roadmap em `docs/superpowers/specs/2026-06-02-java-senior-roadmap-design.md`, §5, Galho 16, linha 175). Pressupõe leitura do roadmap, que estabelece topologia flat, esquema de 3 fases (Iniciado/Adepto/Magus), padrões editoriais e política de poda. Os Galhos 1 a 15 já fecharam em `main` — seus artefatos são o **template de padrão e qualidade** deste galho. É o **segundo galho do bloco "Plataforma distribuída e produção"**, depois de Mensageria (14) e Build (15). Conceitualmente depende de 8 (Spring Core/Boot), 9 (Web/REST), 11 (Reativa), 12 (Segurança), 14 (Mensageria/saga) e 15 (multi-módulo/build).

**Galho HÍBRIDO (PESQUISA pesada + PODA REVERSA substancial):**

- **Parte PESQUISA (a maior):** o galho cobre **como vários serviços formam uma plataforma distribuída** — o modelo de microservices e a tese honesta (trade-off organizacional, não default técnico; quando NÃO usar), os 12 fatores cloud-native (só a arquitetura), service discovery (Eureka/Consul/k8s-native), client-side load balancing (Spring Cloud LoadBalancer), API Gateway (reativo e MVC), config centralizado (Spring Cloud Config), resiliência (Resilience4j: circuit breaker, retry, rate limiter, bulkhead, time limiter), comunicação síncrona (OpenFeign/`@HttpExchange`), segurança entre serviços (token relay), correlação/tracing distribuído (Micrometer Tracing + OpenTelemetry), consistência (CAP/PACELC/eventual) e service mesh. Quase tudo nasce de doc oficial via WebFetch (ZERO memória): `spring.io/projects/spring-cloud`, `docs.spring.io`, `resilience4j.readme.io`, `micrometer.io`, `opentelemetry.io`, `12factor.net`, `martinfowler.com`, `istio.io`, `linkerd.io`.

- **Parte PODA REVERSA (substancial e localizada):** o pré-flight (2026-06-12) confirmou **dívida reversa real** — uma seção inteira `## Spring Cloud — visão geral` + um bloco Resilience4j + um bloco Distributed tracing no tronco legado `Backend/Spring Boot.md` (`publish: false`, já em poda progressiva via callouts "Migrado para galho próprio" — WebFlux e Spring Core já foram). Como é **explicação substancial** (não menção incidental), a regra do pré-flight manda **podar/migrar**: a explicação canônica passa a viver no galho 16; no tronco fica um callout "Migrado para galho próprio" + wikilink, idêntico ao tratamento já dado a WebFlux/Spring Core no mesmo arquivo (§3.5).

**A fronteira-assinatura é DUPLA e define o escopo:**

- **Galho 14 (Mensageria) — para trás:** saga, outbox, idempotência distribuída, event sourcing/CQRS, **gRPC e Protocol Buffers** já estão **fechados lá**. O eixo "comunicação assíncrona/event-driven" do galho 16 **aponta pra G14, não re-explica**. O galho 16 cobre o **resto da plataforma** (síncrono, discovery, gateway, resiliência, tracing, consistência conceitual).
- **Galho 17 (Cloud-native e produção, planejado) — para frente:** containers/Docker, Kubernetes, GraalVM native image, deploy, CI/CD, e a **operação** da observabilidade de produção (rodar coletores, dashboards, profiling, estratégia de sampling em produção). **É a fronteira mais delicada do galho**, e fica no tracing: o galho 16 cobre a **correlação no código + a config de export** (decisão do brainstorming, §nota 18/19), mas marca o seam — **operar** o coletor/Jaeger/Grafana/profiling é G17.

**A tese honesta do galho:** microservices é um **trade-off organizacional e de escala, não um default técnico**. O custo (rede não-confiável, consistência eventual, observabilidade distribuída, overhead operacional — o "microservice premium" de Fowler) só compensa quando a complexidade e a estrutura de times justificam (Conway). Para a maioria, o **monólito modular basta** — e a decisão de quando NÃO usar é metade do galho (Fowler "MonolithFirst", Newman). No nível técnico: **a rede é o inimigo** — toda chamada remota pode falhar, atrasar ou duplicar, então resiliência (timeouts, circuit breaker, retry idempotente, bulkhead) deixa de ser opcional. E **o ecossistema se moveu**: Zuul/Ribbon/Hystrix morreram (→ Gateway/LoadBalancer/Resilience4j), Sleuth virou Micrometer Tracing, OpenFeign está feature-complete (→ `@HttpExchange`), e parte da resiliência migrou do código pra infra (service mesh).

**Os Galhos 17/18 ainda não existem** — toda referência a containers/K8s/GraalVM native/deploy/produção (Galho 17) e OCP (Galho 18) permanece como texto "(planejado)", sem wikilink.

## 2. Objetivo

Produzir, em uma sessão de execução dedicada, **24 notas atômicas + 1 MOC do galho + expansão do Dicionário de Java + ativação do MOC central (Galho 16) + poda reversa substancial em `Backend/Spring Boot.md` + quitação dos ganchos "(planejado) G16" + correção de numeração defasada + cross-links**, em `03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/` e `03-Dominios/Tecnologia/Java/`, todas `publish: true`, em PT-BR, distribuídas em 3 fases (**5 Iniciado + 14 Adepto + 5 Magus**).

Ao terminar o galho, o leitor deve conseguir:

- **Decidir em inglês** se um sistema deve ser microservices ou um monólito modular, justificando com o trade-off honesto (microservice premium, Conway, bounded contexts), e descrever a topologia (monorepo vs multi-repo).
- **Desenhar a plataforma Spring Cloud**: service discovery (client-side vs server-side; Eureka vs Consul vs k8s-native), client-side load balancing (Spring Cloud LoadBalancer), API Gateway (reativo vs MVC), config centralizado (Spring Cloud Config) — sabendo **o que morreu** (Zuul/Ribbon/Hystrix) e por quê.
- **Tornar a comunicação resiliente**: escolher síncrono (OpenFeign feature-complete vs `@HttpExchange` moderno) vs assíncrono (→ G14), e aplicar os padrões do Resilience4j (circuit breaker, retry, rate limiter, bulkhead, time limiter) com a **ordem de aspectos correta** e fallback.
- **Propagar contexto entre serviços**: segurança (token relay, OAuth2 client-credentials → fronteira G12) e tracing (Micrometer Observation/Tracing, traceId/spanId, OpenTelemetry/OTLP), sabendo onde para o código e começa a operação (G17).
- **Raciocinar sobre consistência distribuída** (CAP, PACELC, eventual consistency → saga é G14) e **sobre service mesh** (Istio/Linkerd, sidecar vs ambient, quando o mesh tira a resiliência do código).
- **Julgar quando NÃO fazer microservices** e descrever o caminho monólito modular → extração.

A barra é "projetar, justificar e operar uma plataforma de microservices Java production-grade, escolhendo os componentes (discovery, gateway, resiliência, tracing) com critério — e saber quando NÃO usá-los" — não "decorar anotações do Spring Cloud". O foco é o **modelo mental + a decisão de engenharia**, com snippets corretos como apoio.

## 3. Saídas concretas

### 3.1. Notas (`03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/`)

Pasta **nova**, flat. 24 notas + 1 MOC (`index.md`, obrigatório pro folder-link do Quartz). Numeração global por galho (não reinicia por fase). **Nome da pasta no disco: `Microservices e sistemas distribuídos`** (sem vírgula, casa com o padrão "X e Y" das pastas-irmãs; espelha o título do roadmap).

#### Iniciado (5 notas — o modelo, a tese, o terreno)

| # | Nota | Escopo nuclear |
|---|------|----------------|
| 01 | O que são microservices e a tese honesta *(opus, assinatura)* | O modelo: serviços pequenos, deployáveis independentemente, **database-per-service**, descentralização. **A tese-assinatura:** microservices é **trade-off organizacional/de escala, não default técnico** — o "microservice premium" (Fowler), Conway's Law, bounded contexts difíceis de acertar cedo (Fowler "MonolithFirst"); o **monólito modular** (Newman) geralmente basta. A fronteira dupla (G14 atrás / G17 frente). Fontes: martinfowler.com (MonolithFirst, MicroservicePremium, microservices). |
| 02 | Monorepo vs multi-repo | Topologia de **repositórios** (não de build — fronteira G15): multi-repo (um serviço, um repo, release independente) vs monorepo (vários serviços, um repo, tooling unificado). Trade-offs: isolamento vs consistência atômica, ownership, CI. **Fecha o gancho do Build G15 (nota 12 multi-módulo).** Fontes: martinfowler.com, doc de monorepo (WebFetch). |
| 03 | Os 12 fatores e o serviço cloud-native | Os 12 fatores (Wiggins/Heroku 2011) com foco na **arquitetura** (config no ambiente, backing services como recursos anexados, processos stateless, port binding, disposability, dev/prod parity, logs como event stream); deploy/build-release-run → G17. "Beyond the Twelve-Factor" (Hoffman 2016). Fontes: 12factor.net. |
| 04 | Panorama do Spring Cloud — e o que morreu *(opus, version-heavy)* | O **release train** (2025.1.x "Oakwood" sobre Boot 4/Framework 7; 2025.0.x "Northfields" sobre Boot 3.5.x), os projetos (Config, Gateway, LoadBalancer, OpenFeign, Circuit Breaker, Consul/Kubernetes); **o que MORREU**: Zuul→Gateway, Ribbon→LoadBalancer (removido em 2020.0.0 Ilford), Hystrix→Resilience4j; Sleuth→Micrometer Tracing. Eureka **segue vivo**. **Absorve a tabela podada do tronco.** Tudo WebFetch. |
| 05 | Comunicação inter-serviços — o eixo síncrono vs assíncrono | O eixo de decisão central: **síncrono** (REST/Feign/`@HttpExchange`, gRPC) — acoplamento temporal, simples, mas propaga falha; vs **assíncrono** (eventos/mensageria) — desacopla, resiliente, mas eventual. **gRPC e saga/event-driven são fronteira G14 (linka, não re-explica).** O resto do galho aprofunda o lado síncrono + resiliência. Fontes: martinfowler.com, docs.spring.io. |

#### Adepto (14 notas — a plataforma com Spring, hands-on)

| # | Nota | Escopo nuclear |
|---|------|----------------|
| 06 | Service discovery — o conceito e o Eureka | **Client-side vs server-side discovery** (o cliente consulta o registry e escolhe vs a infra resolve); o **service registry**; **Netflix Eureka** (server + client, **ainda mantido** — Netflix 5.0.2 @ Oakwood, NÃO em maintenance mode); registro/heartbeat/renovação. Fontes: docs.spring.io/spring-cloud-netflix. |
| 07 | Discovery: Consul e Kubernetes-native | **HashiCorp Consul** (Spring Cloud Consul, discovery via HTTP API + DNS, KV store); **Spring Cloud Kubernetes** (discovery nativo via API server / DNS do k8s, `fabric8`/`client` starters) — o modelo **server-side** que muitos preferem hoje. Quando cada um. Fontes: docs.spring.io/spring-cloud-consul, .../spring-cloud-kubernetes. |
| 08 | Client-side load balancing — Spring Cloud LoadBalancer | **Ribbon morreu** (removido em 2020.0.0); o substituto é o **Spring Cloud LoadBalancer** (client-side LB, blocking e reativo); round-robin/random, integração com discovery (`@LoadBalanced`, `lb://`); client-side LB vs server-side (mesh/k8s Service). Fontes: docs.spring.io, cloud.spring.io/spring-cloud-netflix (maintenance). |
| 09 | Comunicação síncrona — OpenFeign e `@HttpExchange` | **OpenFeign** (`@FeignClient`, `@EnableFeignClients`) está **feature-complete desde 2022.0.0 (Kilburn)**; a Spring recomenda os **HTTP Interface clients** (`@HttpExchange`, Framework 6.1+, sobre RestClient/WebClient — **não precisa de Spring Cloud**); 2025.1 trouxe LB+circuit breaking pra HTTP service groups. Liga **G9 (clientes HTTP — RestClient)**. **Fecha o gancho Feign do Web/REST.** Fontes: docs.spring.io/spring-cloud-openfeign, spring-framework rest-clients. |
| 10 | API Gateway — o papel, roteamento, predicates e filters | O **gateway** como porta única (roteamento, cross-cutting: auth, rate limit, CORS, rewrite); **Spring Cloud Gateway**: routes, **predicates** (Path/Method/Header/...) e **filters** (pre/post, GatewayFilter vs GlobalFilter); integração com discovery (`lb://`). Fontes: docs.spring.io/spring-cloud-gateway. |
| 11 | Gateway reativo vs MVC — as duas variantes | As **duas variantes vivas**: **reativo** (`spring-cloud-starter-gateway-server-webflux`, sobre WebFlux/Netty — **fronteira G11**, non-blocking, o original) vs **MVC** (`spring-cloud-starter-gateway-server-webmvc`, servlet/blocking — o novo, pra quem não quer o stack reativo). A renomeação dos starters no trem 2025.x; quando cada um. Fontes: docs.spring.io/spring-cloud-gateway (starter webflux/webmvc). |
| 12 | Config centralizado — Spring Cloud Config | **Config Server** (backends Git/Vault/JDBC) + **Config Client**; `@RefreshScope` e o `/actuator/refresh`; **Spring Cloud Bus** (difundir refresh via broker); o trade-off vs config nativo do k8s (ConfigMap/Secret). Segredos/Vault operacional → fronteira G17. Fontes: docs.spring.io/spring-cloud-config. |
| 13 | Resiliência I — a falha distribuída e o Circuit Breaker | **A rede é o inimigo**: falha parcial, latência, cascading failure. **Resilience4j 2.3.0** (Java 17; v3/Java 21 é roadmap não lançado); o **CircuitBreaker**: estados **CLOSED/OPEN/HALF_OPEN** + DISABLED/FORCED_OPEN; **sliding window** count-based vs time-based; `failureRateThreshold` (default 50%), slow-call detection; `@CircuitBreaker`. **Absorve o bloco Resilience4j podado.** Fontes: resilience4j.readme.io. |
| 14 | Resiliência II — Retry e Time Limiter | **Retry** (`@Retry`, max-attempts, wait/backoff, exponential, retry só em exceções seguras → **idempotência é G14, linka**); **TimeLimiter** (`@TimeLimiter`, timeout de chamadas async/`CompletableFuture`). Por que retry sem idempotência é perigoso. **Absorve parte do bloco podado.** Fontes: resilience4j.readme.io. |
| 15 | Resiliência III — Bulkhead e Rate Limiter | **Bulkhead** (isolamento: **SemaphoreBulkhead** vs **ThreadPoolBulkhead** — conter o esgotamento de threads); **RateLimiter** (limitar chamadas por janela). A metáfora do navio (compartimentos estanques). Fontes: resilience4j.readme.io. |
| 16 | Resiliência IV — compondo os padrões | A **ordem dos aspectos**: `Retry( CircuitBreaker( RateLimiter( TimeLimiter( Bulkhead( fn ) ) ) ) )` e por que importa (a issue do Retry inflar o CB); **fallback** (`fallbackMethod`); **Spring Cloud Circuit Breaker** (a abstração `CircuitBreakerFactory` sobre Resilience4j, `spring-cloud-starter-circuitbreaker-resilience4j`); o starter `resilience4j-spring-boot3`. Fontes: resilience4j.readme.io, docs.spring.io/spring-cloud-circuitbreaker. |
| 17 | Segurança entre serviços | Propagação de identidade entre serviços: **token relay** (repassar o JWT do usuário), **OAuth2 client-credentials** (serviço-a-serviço sem usuário), a propagação no gateway. **O mecanismo OAuth2/OIDC/JWT é G12 (linka, não re-explica)** — aqui é só o ângulo distribuído. **Fecha o gancho da Segurança (12-OAuth2 e index).** Fronteira: mTLS via mesh → nota 22. Fontes: docs.spring.io/spring-security (oauth2 client), spring-cloud-gateway (TokenRelay). |
| 18 | Tracing distribuído I — correlação no código | O problema: uma request atravessa N serviços. **Micrometer Observation API** ("instrument once") + **Micrometer Tracing** (substituiu o **Sleuth**, que foi pro attic e não roda em Boot 3.x; migrado desde Boot 3.0); **traceId/spanId**, propagação de contexto **W3C** entre serviços (headers), injeção no **MDC** pra logs correlacionados. **Absorve o bloco Distributed tracing podado (parte código).** Fontes: micrometer.io (observation, tracing), docs.spring.io. |
| 19 | Tracing distribuído II — exportando o trace | Os **bridges**: `micrometer-tracing-bridge-otel` (→ **OpenTelemetry**/OTLP) vs `micrometer-tracing-bridge-brave` (→ Zipkin); o que é **OpenTelemetry** (CNCF, vendor-neutral: spec + SDK + semantic conventions + **OTLP**); config de export (endpoint OTLP, `sampling.probability`) e leitura do **waterfall** (Jaeger/Zipkin). **Seam G17 marcado:** *operar* coletor/dashboard/profiling/sampling-em-produção é Galho 17. Fontes: opentelemetry.io, micrometer.io, docs.spring.io/actuator/tracing. |

#### Magus (5 notas — julgamento e síntese)

| # | Nota | Escopo nuclear |
|---|------|----------------|
| 20 | Consistência em sistemas distribuídos *(opus)* | **CAP** (Brewer 2000, Gilbert-Lynch 2002 — sob partição, escolha C ou A) e a crítica **PACELC** (Abadi — sem partição, ainda há trade-off Latency vs Consistency); **strong vs eventual consistency**; **database-per-service** força eventual entre serviços. **Saga/outbox/idempotência (como SE resolve) é G14 — linka.** Fontes: CAP/PACELC (fontes acadêmicas), martinfowler.com (decentralized data). |
| 21 | Os padrões de falha distribuída | A síntese da resiliência no nível de arquitetura: **timeouts** em toda chamada, **retries idempotentes** (→ G14), **cascading failure** e como o circuit breaker o quebra, **backpressure distribuído** (→ fronteira G11 Reativa), graceful degradation. **Fecha o gancho da Reativa (index — resiliência/backpressure distribuído).** Fontes: resilience4j.readme.io, martinfowler.com. |
| 22 | Service mesh — quando a resiliência sai do código *(opus)* | **Data plane** (sidecar proxy, ex. Envoy) + **control plane**; o que o mesh entrega (mTLS, retries, circuit breaking, traffic shaping, observability) **movendo a lógica do código pra infra**; **Istio** (sidecar vs **ambient**/ztunnel+waypoint, GA single-cluster desde 1.22, ~1.30.x) e **Linkerd** (2.19, micro-proxy em Rust); **a tese: quando o mesh torna Resilience4j redundante** (a tensão in-app vs malha). Conceitual, sem instalar infra. Fontes: istio.io, linkerd.io. |
| 23 | Quando NÃO fazer microservices *(opus, capstone de julgamento)* | O capstone do julgamento: os **custos reais** (rede, consistência eventual, observabilidade, overhead operacional, complexidade cognitiva); **monólito modular** como default (Newman) e o caminho **modular → extração** (strangler fig, quando a dor justifica); decompor por **business capability/bounded context**, não por camada técnica. Fontes: martinfowler.com, Newman (InfoQ — sem inventar citação). |
| 24 | Capstone — uma requisição ponta a ponta na plataforma | **Uma request atravessando a plataforma** (`order-service` → `payment-service`): entra pelo **gateway** → resolve via **discovery** → **load balancing** → chamada **resiliente** (timeout + circuit breaker + retry) síncrona OU evento async (→ G14) → **trace** propagado (traceId) → **consistência eventual**. Junta os 23 conceitos; **tabela de decisão** (síncrono vs async; quando gateway; quando mesh; Eureka vs k8s); cheatsheet nota→problema; munição de entrevista. Fontes: docs.spring.io. |

**Notas opus (6):** 01 (assinatura/tese), 04 (panorama Spring Cloud — denso e version-heavy), 20 (consistência — CAP/PACELC, conceitualmente escorregadio), 22 (service mesh — a tensão in-app vs infra), 23 (quando NÃO — julgamento), 24 (capstone — síntese). As demais → sonnet. **Quase todas as notas são version-specific** e fazem WebFetch no Step 1 (ver §4.3.3 e §6).

**Decisões de fronteira (escopo de outro dono — link-back ou texto "(planejado)"):**
- **Saga, outbox, event sourcing/CQRS, idempotência, gRPC, Protocol Buffers, mensageria reativa** → Galho 14. As notas 05/14/16/20/21/24 linkam (`Mensageria/22 - Saga`, `.../20 - Idempotência`, `.../28 - gRPC em Java`, etc.) — **nunca re-explicam**.
- **Mecanismo OAuth2/OIDC/JWT/filter chain** → Galho 12. A nota 17 cobre só **propagação distribuída** (token relay, client-credentials); o mecanismo é lá.
- **Clientes HTTP (RestClient/WebClient/RestTemplate), Spring MVC/DispatcherServlet** → Galho 9. A nota 09 linka o RestClient como base; o gateway reativo (nota 11) linka WebFlux/Netty → **Galho 11**.
- **Multi-módulo (estrutura de build de UM projeto), BOM** → Galho 15. A nota 02 (monorepo vs multi-repo) é **topologia de repositórios**, eixo diferente — linka G15.
- **Contract testing / Pact / Pact Broker** → Galho 13. O galho 16 menciona como a orquestração distribuída do broker se encaixa, mas a técnica é lá.
- **Containers/Docker/Kubernetes (deploy), GraalVM native image, CI/CD, deploy, OPERAÇÃO de observabilidade (coletor/dashboard/profiling/sampling em produção), secrets/Vault operacional** → Galho 17 (planejado, texto). O galho 16 para no **código + config de export** do tracing.
- **OCP** → Galho 18 (planejado).

### 3.2. MOC do galho

`03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/index.md`:
- `type: moc`, `status: growing`, `publish: true`, `created`/`updated: 2026-06-12`
- Frontmatter padrão (`title: "Microservices e sistemas distribuídos"`, tags `java`/`microservices`/`moc`, aliases `["Microservices e sistemas distribuídos", "Microservices", "Microsserviços", "Spring Cloud", "Sistemas distribuídos", "Galho 16 - Microservices"]`)
- `> [!abstract] TL;DR` callout — 2-4 linhas: galho cobre como vários serviços formam uma plataforma distribuída (modelo + tese honesta, Spring Cloud, discovery, gateway, resiliência/Resilience4j, comunicação síncrona, segurança entre serviços, tracing/OpenTelemetry, consistência, service mesh); a tese (microservices = trade-off, não default; o monólito modular basta; a rede é o inimigo); **24 notas em 3 fases**
- "Sobre este galho" + audiência primária/secundária + nota de que é galho **HÍBRIDO** (pesquisa + **poda reversa substancial** de `Backend/Spring Boot.md`) + a **fronteira-assinatura dupla** (G14 atrás / G17 frente)
- Conteúdo em 3 H2 (`## Iniciado` / `## Adepto` / `## Magus`) com wikilinks pras 24 notas (uma linha descritiva cada)
- **Rotas alternativas (5):**
  - **Completa** — 01 → 24 em ordem
  - **Entrevista internacional** — 01 → 04 → 05 → 13 → 16 → 18 → 20 → 23 → 24 (tese, Spring Cloud, comunicação, circuit breaker, composição, tracing, consistência, quando-não, capstone — o que mais cai)
  - **A plataforma Spring Cloud na prática** — 04 → 06 → 08 → 09 → 10 → 11 → 12 (panorama, discovery, LB, síncrono, gateway, variantes, config)
  - **Resiliência (meio galho, cai muito)** — 13 → 14 → 15 → 16 → 21 (circuit breaker, retry/timeout, bulkhead/ratelimit, composição, padrões de falha)
  - **Arquitetura e julgamento** — 01 → 02 → 03 → 20 → 22 → 23 (modelo, repos, 12-factor, consistência, mesh, quando-não)
- "Veja também": MOC central `[[03-Dominios/Tecnologia/Java/index|Trilha Java]]`, **G14** (Mensageria — saga/gRPC/eventos), **G12** (Segurança — OAuth2/JWT), **G11** (Reativa — WebFlux/Netty do gateway), **G9** (Web/REST — clientes HTTP), **G15** (Build — multi-módulo), Dicionário de Java; Galhos 17/18 como texto "(planejado)" sem wikilink
- Dataview "Todas as notas do galho" (TABLE fase/status; **inline code nunca começa com `=`** — lição da memória `feedback_dataview_inline_code`)

### 3.3. Dicionário de Java (EXPANSÃO — não recriar)

`03-Dominios/Tecnologia/Java/Dicionário de Java.md` já existe (**~475 verbetes** após o Galho 15, `type: glossary`, seções alfabéticas únicas `## A`…`## Z` com verbetes `### `). Este galho **expande** o arquivo inserindo os verbetes **em ordem alfabética case-insensitive (sem acento, ignorando símbolos iniciais)** nas seções de letra apropriadas. **Nunca recriar o arquivo nem reordenar verbetes existentes.** Atualizar `updated: 2026-06-12`.

Verbetes a inserir (~40, conferir dups antes via grep):

`ambient mesh`, `API Gateway`, `backpressure distribuído`, `bounded context`, `Brave (tracer)`, `bulkhead`, `CAP theorem`, `cascading failure`, `circuit breaker`, `client-side discovery`, `client-side load balancing`, `Conway's Law`, `Consul`, `control plane`, `correlation ID`, `data plane`, `database-per-service`, `Eureka`, `eventual consistency`, `Feign / OpenFeign`, `@HttpExchange (HTTP Interface)`, `Istio`, `Linkerd`, `Micrometer Observation API`, `Micrometer Tracing`, `microservices`, `modular monolith (monólito modular)`, `monorepo`, `multi-repo`, `mTLS`, `OpenTelemetry`, `OTLP`, `PACELC`, `rate limiter`, `Resilience4j`, `service discovery`, `service mesh`, `service registry`, `sidecar`, `Spring Cloud`, `Spring Cloud Config`, `Spring Cloud Gateway`, `Spring Cloud LoadBalancer`, `strangler fig`, `time limiter`, `token relay`, `twelve-factor (12-factor)`, `traceId / spanId`, `Zuul`.

Cada verbete: definição curta (1-3 linhas) em PT-BR + `Veja também:` apontando pra(s) nota(s) canônica(s) do galho. **Conferir com grep os verbetes já existentes** para **não duplicar** — colisões conhecidas do pré-flight: `retry / retryWhen` (existe — contexto Reactor; **linkar/complementar com o ângulo Resilience4j**, não duplicar), `saga` (existe — G14, linkar), `Spring Cloud Stream` (existe — G14, linkar). Possíveis outras: `idempotência` (G14), `backpressure` (G11/G14 — distinguir o distribuído). Quando um termo tocar um já existente, **linkar entre si** em vez de criar segundo verbete. **Conferir 1:1** que os headings batem com âncoras `[[Dicionário de Java#...]]` usadas nas notas.

### 3.4. MOC central (ativação do Galho 16)

`03-Dominios/Tecnologia/Java/index.md` já existe. Task **mínima**: trocar a linha do Galho 16 (atualmente, na **linha 49**, `16. Microservices e sistemas distribuídos *(planejado)* — Spring Cloud, gateway, resilience, sagas, tracing`) por wikilink ativo no padrão dos galhos fechados:

```markdown
16. [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/index|Microservices e sistemas distribuídos]] — o modelo e a tese honesta (microservices vs monólito modular), Spring Cloud (service discovery, gateway, config centralizado), resiliência com Resilience4j (circuit breaker, retry, bulkhead, rate limiter, time limiter), comunicação síncrona (OpenFeign/@HttpExchange), segurança entre serviços, tracing distribuído (Micrometer Tracing/OpenTelemetry), consistência (CAP/PACELC) e service mesh
```

Atualizar `updated` para `2026-06-12`. Não mexer no resto do MOC central. **Confirmar o número da linha na execução** (lendo o arquivo primeiro — hoje é a linha 49).

### 3.5. Poda reversa em `Backend/Spring Boot.md` (substancial, com callout)

O pré-flight confirmou **dívida reversa substancial**, toda em `Backend/Spring Boot.md` (`publish: false`, tronco legado já em poda progressiva — WebFlux e Spring Core já viraram callouts "Migrado para galho próprio"). Política: **a explicação canônica passa a viver no galho 16**; no tronco, cada seção podada vira um **callout `> [!nota] Migrado para galho próprio` + wikilink(s)** pras notas novas — espelhando exatamente o tratamento já dado a WebFlux (linha ~97) e Spring Core (linha ~21) no mesmo arquivo.

| # | Seção no tronco (linha aprox., confirmar via grep) | Conteúdo | Ação |
|---|---|---|---|
| 1 | `## Spring Cloud — visão geral` (~102-175) | tabela completa de projetos + OpenFeign (exemplo + config) + "alternativa moderna" (k8s/Istio/Vault/OTel) | **Substituir a seção inteira** por callout "Migrado para galho próprio" → notas **04** (panorama), **06/07** (discovery), **08** (LB), **09** (Feign/`@HttpExchange`), **10/11** (gateway), **12** (config). |
| 2 | `### API timeout e cascading failures` (~577-619) | Resilience4j: `@CircuitBreaker`/`@TimeLimiter`/`@Retry`, config YAML, fallback | **Substituir** por callout → notas **13** (circuit breaker), **14** (retry/timeout), **16** (composição). |
| 3 | `### Distributed tracing` (~672-691) | Micrometer Tracing + bridge OTel + OTLP/Jaeger | **Substituir** por callout → notas **18** (correlação no código) e **19** (export). |
| 4 | `## Quando usar` (~697, bullet "Spring Cloud") | menção de uma linha | Ajustar pro wikilink da nota 04 (ou manter como menção curta + link). |

**NÃO TOCAR** (não são G16): `### Graceful shutdown` (~621 → G17), `### Database migrations seguras (Flyway)` (~647 → G10), `### Memory leak e GC tuning` (~546 → G3), `### Connection pool exausto`/`### N+1`/`### LazyInitializationException`/`### @Transactional` (G8/G10). **NÃO TOCAR** em `Backend/Spring Data JPA.md`, `Backend/Spring Security.md`, `Backend/Testes em Java.md`, `Backend/Kafka/**`, `Backend/gRPC e Go.md`. **Confirmar todos os números de linha via grep na execução** (`Spring Cloud`, `Resilience4j`, `cascading`, `Distributed tracing`, `Quando usar`).

### 3.6. Quitação de ganchos "(planejado) G16" e cross-links (após as notas existirem)

O pré-flight achou ~10 ganchos "(planejado) Galho 16" deixados por galhos anteriores. **Quitar os substantivos** (promessas de nota que agora têm dono) trocando "(planejado)" por wikilink ativo; **conservador** nos horizonte-lists genéricos de índice.

| # | Arquivo | Ação |
|---|---|---|
| 1 | `03-Dominios/Tecnologia/Java/index.md` | ativação do Galho 16 (§3.4) |
| 2 | `Web e APIs REST/15 - Clientes HTTP — RestClient, WebClient, RestTemplate.md` (~303) | a menção "@FeignClient ... é tema do Galho 16 (planejado)" → **wikilink ativo** pra **nota 09** |
| 3 | `Web e APIs REST/index.md` (~32) | "Microservices (Galho 16) ... planejados" → ativar o link de microservices pra **MOC do galho** (manter G17 como "(planejado)") |
| 4 | `Programação Reativa/index.md` (~35) | "resiliência/backpressure distribuído (Galho 16) ... planejados" → **wikilink** pra **nota 21** |
| 5 | `Build e tooling/12 - Projetos multi-módulo.md` (~99, ~203) | "topologia de repositórios ... Galho 16 (planejado)" → **wikilink** pra **nota 02** (monorepo vs multi-repo) |
| 6 | `Segurança/12 - OAuth2 e OIDC Client e os grant types.md` (~88) | "token relay ... Galho 16 (planejado)" → **wikilink** pra **nota 17** |
| 7 | `Segurança/index.md` (~32) | "segurança em microservices (Galho 16 planejado)" → **wikilink** pra **nota 17** (manter G17 "(planejado)") |
| 8 | `Mensageria/22 - Saga — transações distribuídas por eventos.md` (~205) | "coordenação de sagas no contexto da plataforma G16 (planejado)" → **wikilink** pra **nota 24/05** (o capstone/o eixo) |
| 9 | `Persistência de dados/index.md` (~32) | "dados distribuídos/saga (Galho 16) ... planejados" → **wikilink** pra **nota 20** (consistência) |
| 10 | `Testes/20 - Contract testing — Pact.md` (~107) | "orquestração distribuída do broker ... Galho 16 (planejado)" → **wikilink** pra MOC do galho (menção de fronteira) |
| 11 | `Testes/21 - Capstone — a estratégia de testes...md` (~192) | **CORRIGIR numeração defasada**: hoje diz "observabilidade (Galho 14), mensageria (Galho 16), deploy (Galho 17)" — mas Mensageria é o **Galho 14** (fechado) e observabilidade/microservices/cloud mudaram de número. Reescrever pra refletir a numeração atual (Mensageria=14 fechado; Microservices=16; Cloud-native/observabilidade de produção=17 planejado). |

**Conservador:** o grosso da ligação é **das notas novas → notas-fronteira** (sempre). Cross-links de volta só nos pontos acima (que são promessas explícitas) e onde a nota-dona já tem seção "Veja também". **Não inflar** notas fechadas. Galho 17/18 permanecem texto "(planejado)" em todo lugar; horizonte-lists genéricos intactos.

## 4. Convenções por nota

Herda §7 do roadmap e §4 dos specs dos galhos de pesquisa (5/7/11/14/15). Reforços específicos:

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
  - microservices
  - <fase>
  - <tags específicas: spring-cloud, discovery, gateway, resiliencia, resilience4j, circuit-breaker, tracing, observability, consistencia, service-mesh, config, load-balancing, feign, seguranca, arquitetura, ...>
aliases:
  - <aliases opcionais>
---
```

H1 `# Título` após o frontmatter.

### 4.2. Estrutura H2 obrigatória

- `> [!abstract] TL;DR` (callout, NÃO H2) — 2-4 linhas: conceito + regra prática + por que importa
- `## O que é` / `## Por que importa` / `## Como funciona` (≥3 subseções H3 em notas Adepto/Magus)
- `## Na prática` — exemplos compiláveis; framing **neutro** (`com.example`, serviços `order-service`/`payment-service`, classes `Order`/`Payment`/`OrderService`); "padrão observado em plataformas Java"; NUNCA `MedEspecialista`/"da minha experiência"/"no meu projeto"/"quando montei a plataforma"
- `## Armadilhas` — **≥2** (Iniciado) / **≥3** (Adepto/Magus), cada uma com `### (N) Título` (H3 numerado, NÃO callout `[!warning]`) + descrição + exemplo curto + fix em 1 linha
- `## Em entrevista` — `### Frase pronta (inglês)` com **3+ sentenças** (trade-off + decisão + caveat) + `### Vocabulário` com tabela `| Termo PT | Termo EN |` de **6+ termos**
- `## Veja também` — wikilinks **SEM backticks**, **SEM âncoras same-file**; sempre inclui notas relacionadas do galho + `[[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/index|MOC do galho]]` + `[[03-Dominios/Tecnologia/Java/index|Trilha Java]]` + (quando aplicável) a nota da fronteira (G14 saga/gRPC/eventos, G12 OAuth2/JWT, G11 WebFlux/Netty, G9 clientes HTTP, G15 multi-módulo) + verbetes do Dicionário
- `## Referências` — docs oficiais (`spring.io`, `docs.spring.io`, `resilience4j.readme.io`, `micrometer.io`, `opentelemetry.io`, `12factor.net`, `martinfowler.com`, `istio.io`, `linkerd.io`)

### 4.3. Restrições absolutas

1. **Fronteira-assinatura (linkar de volta, não re-explicar)** — saga/outbox/idempotência/event-driven/gRPC/Protobuf → G14; mecanismo OAuth2/OIDC/JWT → G12; clientes HTTP/MVC → G9; WebFlux/Netty/backpressure → G11; multi-módulo/BOM → G15; contract testing/Pact → G13. **Nunca re-explicar** a saga, o filter chain de segurança, o RestClient, o modelo reativo, ou o reactor multi-módulo — apontar. Containers/K8s/GraalVM native/deploy/operação-de-observabilidade = Galho 17 "(planejado)", sem wikilink; OCP = Galho 18 "(planejado)".
2. **Sem fabricação** de experiência pessoal. Exemplos neutros (`com.example`, `order-service`/`payment-service`, `Order`/`Payment`) — NUNCA `MedEspecialista`/`josenaldo`/1ª pessoa/"na minha plataforma"/"incidente de produção em microservices". **Zero estatística de adoção inventada** (ex.: "X% das empresas usam microservices/Istio"); o pré-flight não achou fonte de market-share → **não citar percentuais**. Números só com fonte verificável.
3. **Sem invenção** de versões/APIs/comportamentos. WebFetch obrigatório no Step 1 das notas version-specific e pra **toda afirmação version-specific**. **Versões cravadas no pré-flight (2026-06-12) — re-confirmar na execução, mas estes são os fatos-base:**
   - **Spring Cloud release train:** **2025.1.x "Oakwood"** (sobre **Spring Boot 4 / Spring Framework 7**, módulos em **5.0.0**, lançado 24-25/nov/2025; Jackson 3, JSpecify nullability) **coexistindo** com **2025.0.x "Northfields"** (Boot **3.5.x**, pra quem fica no 3). Estável mais recente: **2025.1.2 (11/jun/2026)**. **Boot 4 já saiu; 3.x ainda mantido.**
   - **Spring Cloud Gateway — duas variantes:** reativa `spring-cloud-starter-gateway-server-webflux` (sobre WebFlux/Netty) e **MVC** `spring-cloud-starter-gateway-server-webmvc` (servlet). **Starters renomeados no trem 2025.x** (antes `spring-cloud-starter-gateway` / `...-gateway-mvc`).
   - **Resilience4j:** estável **2.3.0 (jan/2025), baseline Java 17**. A **v3/Java 21 é roadmap NÃO lançado** (não há artefato 3.x no Maven Central — descartar o que resumos de IA alucinaram sobre "3.x em 2026"). Módulos: CircuitBreaker, RateLimiter, Retry, Bulkhead (**Semaphore** vs **ThreadPool**), TimeLimiter, Cache. CircuitBreaker: **CLOSED/OPEN/HALF_OPEN** + DISABLED/FORCED_OPEN; sliding window count/time; `failureRateThreshold` default **50%**, `slowCallDurationThreshold` default **60s**, `minimumNumberOfCalls` default **100**. **Ordem dos aspectos:** `Retry(CircuitBreaker(RateLimiter(TimeLimiter(Bulkhead(fn)))))`. Starter Boot 3: `resilience4j-spring-boot3`. Abstração: **Spring Cloud Circuit Breaker** (`spring-cloud-starter-circuitbreaker-resilience4j`).
   - **O que morreu:** **Ribbon, Hystrix, Zuul (1) removidos do Spring Cloud no trem 2020.0.0 "Ilford" (22/dez/2020)** → **LoadBalancer, Resilience4j (via Circuit Breaker), Gateway** respectivamente. **Eureka NÃO morreu** — segue mantido (Netflix **5.0.2** @ Oakwood); só Archaius/Hystrix/Ribbon/Turbine/Zuul estão em maintenance mode.
   - **Discovery:** Eureka (client-side); **Consul** (`spring-cloud-starter-consul-discovery`); **Spring Cloud Kubernetes** (`fabric8`/`client` starters + modo nativo DNS, server-side). Client-side vs server-side discovery.
   - **Tracing:** **Sleuth descontinuado** (foi pro `spring-attic`, **não roda em Boot 3.x**); migrado pra **Micrometer Tracing** desde **Boot 3.0**. **Micrometer Observation API** ("instrument once"). Bridges `io.micrometer:micrometer-tracing-bridge-otel` (→ OTel/OTLP) e `...-bridge-brave` (→ Zipkin). Propagação default **W3C**; traceId/spanId no **MDC**.
   - **OpenFeign feature-complete** desde **2022.0.0 "Kilburn" (16/dez/2022)**; a Spring recomenda **HTTP Interface clients `@HttpExchange`** (**Spring Framework 6.1+**, sobre RestClient/WebClient, sem precisar de Spring Cloud); **2025.1 adicionou LB + circuit breaking a HTTP service groups**.
   - **OpenTelemetry:** projeto **CNCF**, vendor-neutral (fusão OpenTracing+OpenCensus); **spec (API) + SDK + semantic conventions + OTLP** (protocolo). Não é backend.
   - **Conceitos:** **CAP** (Brewer conjectura 2000; Gilbert-Lynch prova 2002 — sob partição, escolha C **ou** A). **PACELC** (Abadi 2010 blog / 2012 paper — se Partição: A/C; senão (Else): Latency/Consistency). **12-factor** (Adam Wiggins/Heroku, 2011); **Beyond the Twelve-Factor App** (Kevin Hoffman, 2016). **MonolithFirst** e **Microservice Premium** (Fowler, 2015). **Service mesh**: data plane (sidecar Envoy) + control plane; **Istio** (sidecar vs **ambient** = ztunnel + waypoint; ambient GA single-cluster desde **1.22**; doc ~**1.30.x**); **Linkerd** (**2.19**, micro-proxy em Rust).
4. **Code samples compiláveis/válidos** — Java (`@FeignClient`, `@HttpExchange`, `@CircuitBreaker`, `@LoadBalanced`, config beans), `application.yml`/`.properties` (Resilience4j, gateway routes, config client, tracing), `pom.xml`/`build.gradle.kts` (starters com coordenadas reais e versões cravadas). Fences corretas: ` ```java `, ` ```yaml `, ` ```properties `, ` ```xml ` (POM), ` ```kotlin ` (build.gradle.kts), ` ```bash ` (CLI), ` ```text ` (diagramas/output/waterfall). Sempre fechadas. **Usar os nomes de starter cravados** (ex.: `spring-cloud-starter-gateway-server-webflux`, não o nome antigo).
5. **Comparações justas** — microservices vs monólito modular, síncrono vs assíncrono, Eureka vs Consul vs k8s-native, client-side vs server-side discovery/LB, gateway reativo vs MVC, OpenFeign vs `@HttpExchange`, in-app resilience (Resilience4j) vs mesh, strong vs eventual consistency: sempre "quando X" E "quando Y". A nota 23 (quando NÃO) e a 24 (capstone) são o ápice do julgamento, sem dogma.
6. **Wikilinks sem backticks** em "Veja também"; MOC do galho + MOC central obrigatórios. **Não linkar galhos inexistentes** (17/18) — texto "(planejado)". Wikilinks pras notas-fronteira usam **path completo** e o **título EXATO** do arquivo (conferir 1:1 — lição do Galho 12: os paths de fronteira têm nomes longos com em-dash `—`, ex.: `[[03-Dominios/Tecnologia/Java/Mensageria/22 - Saga — transações distribuídas por eventos|Saga]]`).
7. **`fase:` no frontmatter + na tag** — obrigatório.
8. **Higiene de commits** — sem `Co-Authored-By: Claude` (memória `feedback_commits`), sem `--no-verify`, `git add <path>` nominal (nunca `-A` — bot de backup Obsidian Git roda em timer), 1 commit por nota/artefato, controlador commita (subagents write-only). Guardar contra `.git/index.lock`.
9. **Tom pedagógico graduado** — Iniciado assume Galhos 1-9 (linguagem + Spring + Web) e que o leitor já fez uma API REST monolítica; Adepto assume que já usou Spring Boot a sério (G8) e quer distribuir; Magus assume o stack inteiro + a tese honesta (microservices é trade-off; a rede é o inimigo; o mesh redistribui responsabilidades).
10. **Registro Feynman onde couber** (memória `feedback_enriquecimento_feynman`): analogias pro abstrato (o circuit breaker como o disjuntor elétrico; o bulkhead como os compartimentos estanques de um navio; o service registry como a lista telefônica; o gateway como a portaria do prédio; eventual consistency como "todo mundo concorda, só não ao mesmo tempo"), perguntas retóricas, callouts. Sem inflar — registro didático, não enchimento.

## 5. Conteúdo por nota (síntese)

Notas de pesquisa fundadas em doc oficial via WebFetch. Fontes-base: `spring.io/projects/spring-cloud` + `github.com/spring-cloud/spring-cloud-release/wiki`, `docs.spring.io` (spring-cloud-gateway, -config, -netflix, -consul, -kubernetes, -openfeign, -circuitbreaker; spring-framework rest-clients; spring-boot actuator/tracing; spring-security), `resilience4j.readme.io`, `micrometer.io` (observation, tracing), `opentelemetry.io`, `12factor.net`, `martinfowler.com`, `istio.io`, `linkerd.io`.

- **01 — O que são microservices e a tese honesta (pesquisa, opus, assinatura).** O modelo + o trade-off (premium, Conway, bounded contexts); monólito modular. Armadilhas: microservices como default; dividir por camada técnica; ignorar Conway. Fontes: martinfowler.com.
- **02 — Monorepo vs multi-repo (pesquisa).** Topologia de repos (≠ build, fronteira G15). Armadilhas: confundir multi-módulo com multi-repo; monorepo sem tooling. Fontes: martinfowler.com.
- **03 — Os 12 fatores (pesquisa).** Os 12 fatores, foco arquitetura; Beyond 12-factor. Armadilhas: estado em processo; config no código. Fontes: 12factor.net.
- **04 — Panorama do Spring Cloud + o que morreu (pesquisa, opus, version-heavy).** Release train, projetos, mortes (Zuul/Ribbon/Hystrix). **Absorve poda.** Armadilhas: usar Zuul/Ribbon/Hystrix hoje; achar que Eureka morreu. Fontes: spring.io, github spring-cloud-release.
- **05 — Comunicação inter-serviços (pesquisa).** Eixo síncrono vs assíncrono; gRPC/saga = G14. Armadilhas: tudo síncrono (acoplamento temporal); tudo async sem necessidade. Fontes: martinfowler.com, docs.spring.io.
- **06 — Service discovery + Eureka (pesquisa).** Client/server-side; registry; Eureka (vivo). Armadilhas: client-side discovery quando o k8s já resolve; TTL/heartbeat mal configurado. Fontes: docs.spring.io/spring-cloud-netflix.
- **07 — Consul e Kubernetes-native (pesquisa).** Consul (HTTP/DNS/KV); Spring Cloud Kubernetes (nativo). Armadilhas: dois discoveries concorrendo; ignorar o DNS do k8s. Fontes: docs.spring.io (consul, kubernetes).
- **08 — Spring Cloud LoadBalancer (pesquisa).** Ribbon morreu; LoadBalancer (blocking/reativo); `@LoadBalanced`/`lb://`. Armadilhas: procurar Ribbon; client-side LB sobre um mesh que já balanceia. Fontes: docs.spring.io, cloud.spring.io/netflix.
- **09 — OpenFeign e `@HttpExchange` (pesquisa).** Feign feature-complete; `@HttpExchange` (Framework 6.1+). **Fecha gancho Web/REST.** Armadilhas: começar projeto novo só com Feign; misturar os dois sem critério. Fontes: docs.spring.io/spring-cloud-openfeign, spring-framework rest-clients.
- **10 — API Gateway: papel/roteamento (pesquisa).** Routes, predicates, filters, `lb://`. Armadilhas: lógica de negócio no gateway; gateway como SPOF sem HA. Fontes: docs.spring.io/spring-cloud-gateway.
- **11 — Gateway reativo vs MVC (pesquisa).** As duas variantes/starters (WebFlux/Netty vs servlet); renomeação 2025.x. Fronteira G11. Armadilhas: usar o starter antigo; gateway reativo num time sem WebFlux. Fontes: docs.spring.io/spring-cloud-gateway.
- **12 — Spring Cloud Config (pesquisa).** Config Server/Client; `@RefreshScope`; Bus. Vault operacional = G17. Armadilhas: segredo em Git plano; refresh sem `@RefreshScope`. Fontes: docs.spring.io/spring-cloud-config.
- **13 — Resiliência I: Circuit Breaker (pesquisa).** A rede como inimigo; Resilience4j 2.3.0; estados/janela/thresholds. **Absorve poda.** Armadilhas: sliding window mal dimensionada; sem fallback. Fontes: resilience4j.readme.io.
- **14 — Resiliência II: Retry e Time Limiter (pesquisa).** Retry/backoff (idempotência=G14); TimeLimiter. **Absorve poda.** Armadilhas: retry sem idempotência; retry storm sem backoff. Fontes: resilience4j.readme.io.
- **15 — Resiliência III: Bulkhead e Rate Limiter (pesquisa).** Semaphore vs ThreadPool bulkhead; rate limiter. Armadilhas: pool único pra tudo; rate limit no lugar errado. Fontes: resilience4j.readme.io.
- **16 — Resiliência IV: composição (pesquisa, opus).** Ordem dos aspectos; fallback; Spring Cloud Circuit Breaker. Armadilhas: ordem errada inflando o CB; abstração escondendo o tuning. Fontes: resilience4j.readme.io, docs.spring.io/spring-cloud-circuitbreaker.
- **17 — Segurança entre serviços (pesquisa).** Token relay; client-credentials; propagação no gateway. Mecanismo = G12. **Fecha gancho Segurança.** Armadilhas: repassar token sem validar audience; serviço interno sem authz. Fontes: docs.spring.io/spring-security, spring-cloud-gateway (TokenRelay).
- **18 — Tracing I: correlação no código (pesquisa).** Observation API; Micrometer Tracing (ex-Sleuth); traceId/spanId; W3C; MDC. **Absorve poda.** Armadilhas: log sem traceId; perder contexto ao trocar de thread (→ context propagation). Fontes: micrometer.io, docs.spring.io.
- **19 — Tracing II: exportando (pesquisa).** Bridges otel/brave; OpenTelemetry/OTLP; sampling; waterfall. **Seam G17.** Armadilhas: sampling 100% em produção; confundir instrumentação com o backend. Fontes: opentelemetry.io, micrometer.io, docs.spring.io/actuator/tracing.
- **20 — Consistência distribuída (pesquisa, opus).** CAP, PACELC, eventual vs strong, database-per-service. Saga=G14. Armadilhas: esperar strong consistency entre serviços; ignorar o trade-off latency/consistency (PACELC). Fontes: CAP/PACELC, martinfowler.com.
- **21 — Padrões de falha distribuída (pesquisa).** Timeouts, retries idempotentes, cascading failure, backpressure distribuído (G11), graceful degradation. **Fecha gancho Reativa.** Armadilhas: chamada sem timeout; degradação que vira falha total. Fontes: resilience4j.readme.io, martinfowler.com.
- **22 — Service mesh (pesquisa, opus).** Data/control plane; Istio (sidecar/ambient) e Linkerd; quando o mesh torna Resilience4j redundante. Armadilhas: resiliência duplicada (app + mesh); adotar mesh sem necessidade. Fontes: istio.io, linkerd.io.
- **23 — Quando NÃO fazer microservices (pesquisa, opus, julgamento).** Custos reais; monólito modular; strangler fig. Armadilhas: microservices prematuro; decompor por camada. Fontes: martinfowler.com, Newman (InfoQ — sem inventar citação literal).
- **24 — Capstone: requisição ponta a ponta (pesquisa).** order→payment atravessando gateway/discovery/LB/resiliência/trace/consistência; tabela de decisão; cheatsheet. Armadilhas de raciocínio: "microservices é mais escalável por definição"; "circuit breaker resolve tudo"; "mesh dispensa pensar resiliência". Fontes: docs.spring.io.

## 6. Pré-flight: verificações feitas

Executado na fase de pré-flight + brainstorming (2026-06-12); itens version-specific re-confirmados na execução de cada nota via WebFetch:

1. **Estrutura da trilha confirmada** — MOC central é `03-Dominios/Tecnologia/Java/index.md` (`Java.md` é legado); Galho 16 listado como `*(planejado)*` na **linha 49**. Padrão de nota `type: concept`/`fase`/`publish: true`; template de MOC e de nota = Galhos 14/15.
2. **Galho HÍBRIDO confirmado** — pesquisa pesada (Spring Cloud é território novo no vault) + **poda reversa substancial** em `Backend/Spring Boot.md`: `## Spring Cloud — visão geral` (~102-175), `### API timeout e cascading failures`/Resilience4j (~577-619), `### Distributed tracing` (~672-691). Tronco `publish: false` já em poda progressiva (WebFlux/Spring Core já viraram callout). **Poda com callout "Migrado para galho próprio"** (§3.5).
3. **Fronteira-assinatura dupla confirmada (paths exatos a linkar):**
   - **G14** (atrás) → `Mensageria/22 - Saga — transações distribuídas por eventos.md`, `Mensageria/20 - Idempotência — o pilar do at-least-once.md`, `Mensageria/21 - O padrão Outbox.md`, `Mensageria/23 - Event sourcing e CQRS.md`, `Mensageria/28 - gRPC em Java — RPC síncrono sobre HTTP_2.md`, `Mensageria/27 - Protocol Buffers — a IDL e a serialização binária.md`
   - **G12** → `Segurança/12 - OAuth2 e OIDC Client e os grant types.md`, `Segurança/index.md`
   - **G11** → `Programação Reativa/index.md`, `Programação Reativa/10 - Spring WebFlux — o stack não-bloqueante sobre Netty e o DispatcherHandler.md`
   - **G9** → `Web e APIs REST/15 - Clientes HTTP — RestClient, WebClient, RestTemplate.md`, `Web e APIs REST/index.md`
   - **G15** → `Build e tooling/12 - Projetos multi-módulo.md`
   - **G13** → `Testes/20 - Contract testing — Pact.md`, `Testes/21 - Capstone — a estratégia de testes...md`
4. **Ganchos "(planejado) G16"** — ~10 pontos a quitar (§3.6) + 1 correção de numeração defasada (Testes/21, ~192).
5. **Dicionário** — **~475 verbetes** após o Galho 15; seções `## A`…`## Z`; verbetes `### `. Dups conhecidos a linkar (não duplicar): `retry / retryWhen` (Reactor — complementar com ângulo Resilience4j), `saga` (G14), `Spring Cloud Stream` (G14). Expansão alfabética (~40), nunca recriar/reordenar; `updated: 2026-06-12`.
6. **MOC central** — linha 49 (`16. Microservices e sistemas distribuídos *(planejado)*`); galhos ativos usam `N. [[path/index|Title]] — summary`; `updated: 2026-06-12`. Confirmar a linha na execução.
7. **Versões CRAVADAS via WebFetch (2026-06-12)** — Spring Cloud 2025.1.x Oakwood (Boot 4/Framework 7) + 2025.0.x Northfields (Boot 3.5.x), latest 2025.1.2; Gateway webflux/webmvc starters renomeados; Resilience4j 2.3.0 (Java 17; v3 roadmap não lançado); Ribbon/Hystrix/Zuul removidos no 2020.0.0, Eureka vivo (Netflix 5.0.2); Sleuth→Micrometer Tracing desde Boot 3.0; OpenFeign feature-complete desde 2022.0.0, `@HttpExchange` (Framework 6.1+); OTel CNCF/OTLP; CAP (Brewer/Gilbert-Lynch), PACELC (Abadi); 12-factor (Wiggins 2011); Istio 1.30.x (ambient GA single-cluster desde 1.22)/Linkerd 2.19. (Detalhes em §4.3.3.) **Re-confirmar na execução.**
8. **Troncos/arquivos intocáveis** — todos os artefatos dos Galhos 1-15 exceto: ativação do MOC central (§3.4), poda substancial em `Backend/Spring Boot.md` (§3.5), quitação dos ganchos + correção de numeração (§3.6). Pasta `Microservices e sistemas distribuídos/` ainda **não existe**.

Nenhum número de adoção/market-share é inventado (o pré-flight não achou fonte — **não citar percentuais**). Quando faltar fato verificável, **PERGUNTAR** antes de escrever.

## 7. Critérios de aceitação do galho

Além dos critérios gerais (§10 do roadmap):

1. 24 notas em `03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/`, frontmatter completo com `fase:`, `publish: true`, distribuídas 5/14/5.
2. MOC do galho com 3 subseções de fase + 5 rotas alternativas + dataview (inline code nunca inicia com `=`) + folder-link resolve (`index.md` presente).
3. Dicionário de Java **expandido** (não recriado) com ~40 verbetes; verbetes dos Galhos 1-15 intactos; `updated: 2026-06-12`; dups conferidos e linkados (não duplicar `retry`/`saga`/`Spring Cloud Stream`).
4. MOC central `Java/index.md` com Galho 16 ativado (linha 49 vira wikilink); resto intacto; `updated: 2026-06-12`.
5. **Poda reversa executada (substancial, com callout)**: as 3 seções de `Backend/Spring Boot.md` (Spring Cloud overview, Resilience4j/cascading, Distributed tracing) substituídas por callouts "Migrado para galho próprio" + wikilinks pras notas do galho; **as seções NÃO-G16 (graceful shutdown, Flyway, GC, pool, N+1, @Transactional) intactas**; outros troncos intactos.
6. **Ganchos quitados**: os ~10 pontos "(planejado) G16" viram wikilinks ativos (§3.6); a numeração defasada do `Testes/21` corrigida; Galhos 17/18 permanecem texto "(planejado)" em todo lugar.
7. Cada nota: TL;DR; code samples válidos (Java/yaml/properties/POM/build.gradle.kts; starters com nomes cravados); "Em entrevista" com `### Frase pronta (inglês)` 3+ sentenças + `### Vocabulário` tabela 6+ termos PT→EN; "Armadilhas" com `### (N) Título` numerado + exemplo + fix (≥2 Iniciado, ≥3 Adepto/Magus); wikilinks (galho + MOC central + fronteira quando aplicável + Dicionário); "Referências" com docs oficiais verificadas.
8. **Fronteira-assinatura respeitada**: saga/gRPC/eventos → G14; OAuth2/JWT → G12; clientes HTTP → G9; WebFlux/Netty → G11; multi-módulo → G15; Pact → G13; nada re-explicado; galhos 17/18 só texto "(planejado)".
9. **Fronteiras de escopo respeitadas**: containers/K8s/GraalVM native/deploy/CI-CD/operação-de-observabilidade/secrets-Vault-operacional = Galho 17; OCP = Galho 18. O tracing para no **código + config de export**; operar coletor/dashboard/profiling/sampling-de-produção é G17.
10. Zero fabricação de experiência pessoal; zero estatística de adoção inventada; afirmações version-specific citam a versão verificada via WebFetch (Spring Cloud/Resilience4j/Micrometer/OpenFeign/Eureka/Istio).
11. 1 commit por nota/artefato; sem `Co-Authored-By: Claude`; sem `--no-verify`; stage nominal (nunca `-A`); subagents write-only, controlador commita.
12. `verificar-wikilinks` roda limpo na pasta do galho (evitar âncoras same-file; conferir os títulos EXATOS das notas-fronteira — nomes longos com em-dash; lição do Galho 12).

## 8. Riscos e mitigações

| Risco | Mitigação |
|---|---|
| **Inventar versão "de memória"** (Spring Cloud train, Resilience4j 3, Gateway starters, Istio) | Versões cravadas no pré-flight (§4.3.3); WebFetch no Step 1; Referências oficiais. Pontos minados: **Resilience4j 3/Java 21 NÃO lançado** (estável é 2.3.0/Java 17); **Spring Boot 4 já saiu** (train Oakwood) mas 3.x mantido; **starters de gateway renomeados**; **Eureka NÃO morreu** (só Zuul/Ribbon/Hystrix); **Sleuth morreu** → Micrometer Tracing; **OpenFeign feature-complete** → `@HttpExchange`. |
| **Re-explicar fronteiras** (saga, gRPC, OAuth2/JWT, RestClient, WebFlux, multi-módulo) | Restrição 4.3.1; notas linkam G14/G12/G9/G11/G15 explicitamente; review por fase confere link-back. O eixo async (nota 05) e a consistência (nota 20) apontam pra G14, não re-derivam saga/outbox. |
| **Invadir Galho 17** (containers, K8s, GraalVM native, deploy, operação de observabilidade) | A fronteira mais delicada. A decisão do brainstorming: tracing para no **código + config de export** (notas 18/19); **operar** coletor/dashboard/profiling/sampling-de-produção = texto "(planejado)" G17. Config centralizado (nota 12) para no mecanismo; Vault operacional = G17. Review por fase confere o seam. |
| **Inventar estatística de adoção** ("X% usa microservices/Istio/Kafka") | Pré-flight não achou fonte → **proibido citar percentuais**; comparações qualitativas; números só com fonte verificável. |
| **Hype/dogma** ("microservices é mais escalável", "monólito é legado", "todo mundo usa service mesh") | A tese honesta (trade-off, não default; a rede é o inimigo; o monólito modular basta) fixada em 01/05/20/22/23; "quando X E quando Y" obrigatório; a nota 23 (quando NÃO) é o contrapeso explícito; review por fase. |
| **Poda reversa: deixar buraco no tronco** ou poda agressiva em seção não-G16 | Callout "Migrado para galho próprio" + wikilink (não deleção cega); confirmar linhas via grep; **NÃO TOCAR** graceful shutdown/Flyway/GC/pool/N+1/@Transactional (§3.5); review confere que `Spring Boot.md` só perdeu o que migrou e ganhou os callouts. |
| **Code samples inválidos** (starter antigo, anotação errada, ordem de aspecto errada) | Snippets compiláveis; **nomes de starter cravados** (gateway-server-webflux/webmvc, resilience4j-spring-boot3); a ordem `Retry(CB(...))` correta; fences certas; review confere. |
| **Exemplos de domínio sensível / 1ª pessoa** | Framing neutro (`com.example`, `order-service`/`payment-service`, `Order`/`Payment`); NUNCA MedEspecialista/1ª pessoa/"na minha plataforma"; review por fase. |
| **Sobreposição entre as 4 notas de resiliência** (13-16) | Foco distinto: 13 (CB + a falha distribuída), 14 (retry+timeout), 15 (bulkhead+ratelimit), 16 (composição+abstração); review checa sobreposição. Se uma passar de ~600 linhas, dividir nota (não galho). |
| **Capstone/notas inventarem títulos de nota-fronteira** (lição Galho 12) | Passar aos subagentes os títulos EXATOS das 24 notas + das notas-fronteira (em-dash); `verificar-wikilinks` ao fim; review do capstone confere 1:1. |
| **Dicionário: duplicar verbete existente** (`retry`, `saga`, `Spring Cloud Stream`) | Grep dos existentes antes de inserir; tocar existente → **linkar**, não duplicar; inserção alfabética, nunca recriar. |
| **Bot de backup (Obsidian Git) commitando no meio** | Padrão dos Galhos 2-15: subagents write-only; controlador commita após cada nota com `git add` nominal (nunca `-A`); guardar contra `.git/index.lock`. |
| Galho denso (24 notas) inflar notas individuais | Distribuição 5/14/5 fixada; se uma nota passar de ~600 linhas, dividir nota (não galho); capstone com cheatsheet enxuto. |

## 9. Próximos passos

1. **Aprovação deste spec**
2. **Plano de execução** via skill `superpowers:writing-plans` → `docs/superpowers/plans/2026-06-12-java-galho-16-microservices-execution.md`
3. **Execução** via `superpowers:subagent-driven-development` **direto na `main`** (subagents write-only; sonnet por padrão, opus nas notas 01/04/20/22/23/24; review **por fase** + fix loop; push manual do usuário)
4. **Verificação** de wikilinks (incluindo os paths longos das notas-fronteira) + conferência de âncoras do Dicionário
5. **Atualização da memória** `project_trilha_java` (Galho 16 completo; próximo sugerido: 17 Cloud-native e produção) antes do próximo galho

## 10. Documentos relacionados

- `2026-06-02-java-senior-roadmap-design.md` — roadmap macro (18 galhos); Galho 16 em §5 (linha 175)
- `2026-06-11-java-galho-15-build-tooling-design.md` / `...-execution.md` — Galho 15 (galho anterior; molde de galho híbrido + MOC + Dicionário + ativação + poda)
- `2026-06-11-java-galho-14-mensageria-design.md` — Galho 14 (dono de saga/outbox/idempotência/gRPC/event-driven — fronteira-assinatura atrás das notas 05/14/16/20/21/24)
- `2026-06-10-java-galho-12-seguranca-design.md` — Galho 12 (dono de OAuth2/OIDC/JWT — fronteira da nota 17; alvo de quitação de gancho)
- `2026-06-10-java-galho-11-reativa-design.md` — Galho 11 (dono de WebFlux/Netty/backpressure — fronteira das notas 11/21; alvo de quitação de gancho)
- Galho 9 (Web e APIs REST) — dono dos clientes HTTP (fronteira da nota 09; alvo de quitação de gancho)
- Galhos 5/7/11/14/15 — template de **galho de pesquisa/híbrido**
- Artefatos a criar/atualizar: `03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/**` (24 notas + MOC), `03-Dominios/Tecnologia/Java/Dicionário de Java.md`, `03-Dominios/Tecnologia/Java/index.md`, `03-Dominios/Tecnologia/Java/Backend/Spring Boot.md` (poda substancial), e os ~10 arquivos de quitação de gancho (§3.6)
- Fontes-base do galho: `spring.io/projects/spring-cloud`, `docs.spring.io` (gateway/config/netflix/consul/kubernetes/openfeign/circuitbreaker/security/actuator), `resilience4j.readme.io`, `micrometer.io`, `opentelemetry.io`, `12factor.net`, `martinfowler.com`, `istio.io`, `linkerd.io`
- Memórias: [[project_trilha_java]], [[project_trilhas_fases_aprendizado]], [[project_tronco_galhos_pattern]], [[feedback_galhos_direto_main]], [[feedback_no_fabrication]], [[feedback_quartz_index]], [[feedback_commits]], [[feedback_dataview_inline_code]], [[feedback_notas_atomicas]], [[feedback_enriquecimento_feynman]], [[feedback_redundancia_entre_notas]]
