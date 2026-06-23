---
title: "Capstone — do jar ao cluster"
created: 2026-06-12
updated: 2026-06-12
type: concept
status: seedling
publish: true
fase: magus
tags:
  - java
  - cloud-native
  - magus
  - capstone
aliases:
  - "Capstone Cloud-native"
  - "Do jar ao cluster"
---

# Capstone — do jar ao cluster

> [!abstract] TL;DR
> Este é o **fio que costura o galho inteiro**. Pegamos um serviço Spring Boot neutro — o `order-service` — e o levamos a produção **ponta a ponta**: `jar` em camadas → imagem (Dockerfile, Buildpacks ou Jib) → JVM ciente do container → probes + graceful shutdown → `Deployment` no Kubernetes → métricas/traces/logs → CI/CD. A tese que atravessa tudo: **"production-ready" não é uma feature que se liga, é uma sequência de contratos** — com o build, com a JVM, com o orquestrador, com o coletor de observabilidade. Cada nota do galho é uma estação dessa linha. Aqui você vê o **trajeto completo** e ganha as **tabelas de decisão** (Dockerfile vs Buildpacks vs Jib; JVM vs native; head vs tail sampling) e o **cheatsheet "problema → nota"** que vira munição direta em entrevista de plataforma/SRE.

## O que é

Uma **capstone** não ensina nada novo. Ela **monta** o que as 21 notas anteriores ensinaram em pedaços e mostra o sistema funcionando como um todo. A pergunta que ela responde não é *"o que é um probe?"* nem *"o que é um layered jar?"* — essas já foram respondidas. A pergunta é:

> **"Eu tenho um `order-service.jar` compilado. O que precisa acontecer, em ordem, para ele estar rodando num cluster, observável, atualizável sem downtime e com diagnóstico sob carga?"**

A resposta é uma **linha de montagem de contratos**. Cada estação entrega o artefato para a próxima num formato que ela entende:

1. **Build** entrega um `jar` em **camadas** (layered jar) — para que a imagem seja eficiente.
2. **Empacotamento** entrega uma **imagem OCI** enxuta — via Dockerfile, Buildpacks ou Jib.
3. **A JVM dentro do container** precisa **enxergar os limites** do cgroup — senão dimensiona heap pela máquina inteira.
4. **Probes** entregam ao orquestrador um **contrato de saúde** — liveness e readiness separados.
5. **Graceful shutdown** entrega um **encerramento limpo** no SIGTERM — drena conexões antes de morrer.
6. **O `Deployment` YAML** entrega ao cluster o **estado desejado** — réplicas, recursos, config.
7. **Observabilidade** entrega ao operador os **três sinais** — métricas, traces e logs.
8. **CI/CD** entrega tudo isso **de forma repetível** — sem humano colando comando no terminal.

> [!info] O `order-service` é um domínio neutro de propósito
> Não é um sistema real de ninguém. É um serviço genérico — recebe pedidos, persiste, expõe HTTP — escolhido só para ter um nome concreto nos exemplos. Substitua mentalmente por qualquer serviço Spring que você opere.

## Por que importa

Quem domina **uma estação** parece competente. Quem domina **a linha inteira** parece sênior. A diferença em entrevista de plataforma/SRE é exatamente essa: o júnior sabe escrever um `Dockerfile`; o sênior sabe **por que** aquele `Dockerfile` tem multi-stage, **como** ele interage com o dimensionamento de heap da JVM, **o que** o readiness probe protege durante o rollout, e **onde** o trace gerado por esse pod vai parar.

A capstone também expõe os **acoplamentos invisíveis** entre estações — as decisões que parecem locais mas vazam:

- Escolher **native image** (estação 2) muda o **profiling** (estação 8): você perde JFR e ganha outro ferramental.
- Configurar **readiness** errado (estação 4) **quebra o deploy sem downtime** (estação 6): o cluster manda tráfego antes da app estar pronta.
- Esquecer de a JVM **ler os limites do cgroup** (estação 3) faz o pod ser **morto por OOM** independentemente de quão bons sejam seus probes.

> [!tip] Feynman: a fábrica de carros
> Pense numa linha de montagem de carro. A lataria (jar) sai da prensa; a pintura (imagem) só funciona se a lataria veio limpa; o motor (JVM) precisa caber no compartimento (cgroup); os sensores de bordo (probes) avisam à central (orquestrador) se o carro liga; a inspeção final (CI/CD) garante que **todo** carro sai igual. Ninguém entrega um carro montando peças à mão a cada unidade — e ninguém deveria fazer deploy assim.

## Como funciona

### O fluxo ponta a ponta, estação por estação

O percurso canônico, do `jar` ao tráfego em produção:

1. **Compilar e empacotar em camadas.** O Spring Boot já gera um *layered jar* por padrão. As camadas (dependências, dependências-snapshot, recursos da aplicação, classes da aplicação) mudam em ritmos diferentes — dependências raramente, código a cada commit. Separá-las faz o cache de imagem reaproveitar o que não mudou. Detalhe em [[03-Dominios/Tecnologia/Java/Cloud-native e produção/04 - Dockerfile na prática — multi-stage e layered jar|Dockerfile na prática]].
2. **Construir a imagem.** Três caminhos (decididos na tabela abaixo): `Dockerfile` multi-stage, Buildpacks (`mvn spring-boot:build-image`), ou Jib. Todos produzem uma imagem OCI; diferem em controle, reprodutibilidade e dependência do Docker daemon.
3. **Enxugar e escanear.** Base distroless ou enxuta, usuário não-root, scan de CVE no pipeline — ver [[03-Dominios/Tecnologia/Java/Cloud-native e produção/05 - Imagem enxuta e segura — distroless e scanning|Imagem enxuta e segura]].
4. **A JVM dentro do container.** A JVM moderna é *container-aware*: lê os limites do cgroup e dimensiona heap por `MaxRAMPercentage`. Sem isso, ela acha que tem a RAM da máquina inteira e o kernel mata o pod. Ver [[03-Dominios/Tecnologia/Java/Cloud-native e produção/02 - A JVM dentro de um container|A JVM dentro de um container]].
5. **Probes.** O Actuator expõe `/actuator/health/liveness` e `/actuator/health/readiness` como contratos distintos: *liveness* = "estou vivo, não me reinicie"; *readiness* = "posso receber tráfego agora?". Ver [[03-Dominios/Tecnologia/Java/Cloud-native e produção/10 - Health e probes — o contrato com o orquestrador|Health e probes]].
6. **Config e recursos.** Config vem de fora (ConfigMap/Secret → variáveis de ambiente), e `requests`/`limits` declaram o apetite do pod. Ver [[03-Dominios/Tecnologia/Java/Cloud-native e produção/11 - Config e recursos no Kubernetes|Config e recursos no Kubernetes]].
7. **Graceful shutdown.** No SIGTERM, o app marca readiness como *down*, drena conexões em voo e morre dentro do timeout — casado com o `preStop` e `terminationGracePeriodSeconds` do pod. Ver [[03-Dominios/Tecnologia/Java/Cloud-native e produção/12 - Graceful shutdown e deploy sem downtime|Graceful shutdown e deploy sem downtime]].
8. **Observabilidade.** Os três *seams*: **métricas** via Micrometer → Prometheus; **traces** via OpenTelemetry → Collector; **logs** estruturados (JSON) no stdout. Panorama em [[03-Dominios/Tecnologia/Java/Cloud-native e produção/13 - Observabilidade de operação — o panorama e os 3 seams|Observabilidade — o panorama]].
9. **CI/CD.** Um pipeline constrói, testa, escaneia, publica a imagem e aplica o manifesto. Ver [[03-Dominios/Tecnologia/Java/Cloud-native e produção/20 - CI-CD e o caminho até produção|CI-CD e o caminho até produção]].

### As escolhas no caminho

A linha não é única — ela **bifurca** em pontos de decisão, e a sabedoria sênior é escolher conscientemente:

- **Como construir a imagem?** Dockerfile (controle total, mais manutenção) vs Buildpacks (zero Dockerfile, opinativo) vs Jib (daemonless, ótimo em CI). Tabela abaixo.
- **JVM ou native?** A JVM dá *peak throughput* e ferramental de diagnóstico maduro (JFR, async-profiler); o native dá *startup* quase instantâneo e *footprint* baixo, ao custo de build lento, reflexão fechada por hints e profiling diferente. A decisão honesta está em [[03-Dominios/Tecnologia/Java/Cloud-native e produção/21 - Native vs JVM — a decisão honesta|Native vs JVM]] e o conceito em [[03-Dominios/Tecnologia/Java/Cloud-native e produção/08 - GraalVM Native Image — conceito e trade-offs|GraalVM Native Image — conceito]].
- **Quanto trace coletar?** *Head sampling* decide cedo (barato, mas pode descartar o trace de um erro raro); *tail sampling* decide depois de ver o trace inteiro no Collector (caro, mas pega os outliers). Ver [[03-Dominios/Tecnologia/Java/Cloud-native e produção/16 - OpenTelemetry Collector e sampling de produção|OpenTelemetry Collector e sampling]].

### O que produção exige (e dev não cobra)

Em dev, o serviço "funciona". Produção cobra contratos que dev nunca testa:

- **Morrer limpo.** Um pod é descartável; SIGTERM chega o tempo todo (rollout, autoscaling, drain de nó). Quem não drena conexões corta requisições no meio.
- **Caber no orçamento.** `limits` de memória + JVM container-aware: passou do limite, o kernel mata sem aviso (OOMKilled), sem stack trace.
- **Declarar saúde com honestidade.** Readiness que mente ("estou pronto" sem o banco conectado) faz o cluster mandar tráfego para um pod que vai falhar.
- **Ser observável sem `kubectl exec`.** Quando algo trava às 3h da manhã, você precisa de métricas, traces e logs já fluindo — não de abrir um shell no pod. Inclui **profiling sob carga** ([[03-Dominios/Tecnologia/Java/Cloud-native e produção/18 - Profiling e diagnóstico sob carga — produção|Profiling e diagnóstico sob carga]]) e **continuous profiling** ([[03-Dominios/Tecnologia/Java/Cloud-native e produção/19 - Continuous profiling no cluster — Pyroscope e async-profiler|Continuous profiling no cluster]]).

## Na prática

O diagrama do trajeto completo:

```text
                  ┌─────────────── BUILD ───────────────┐
   código  ──▶  mvn package  ──▶  order-service.jar (layered)
                                          │
              ┌───────────────────────────┴───────────────────────────┐
              ▼                            ▼                            ▼
        Dockerfile                    Buildpacks                      Jib
     (multi-stage)              mvn spring-boot:build-image     daemonless, em CI
              └───────────────────────────┬───────────────────────────┘
                                          ▼
                              imagem OCI (distroless, não-root, escaneada)
                                          │  docker push registry/order-service:sha
                                          ▼
   ┌──────────────────────────── KUBERNETES ────────────────────────────┐
   │  Deployment ──▶ Pod                                                 │
   │     ├─ JVM container-aware (MaxRAMPercentage lê o cgroup)           │
   │     ├─ env  ◀── ConfigMap + Secret                                  │
   │     ├─ readinessProbe  ──▶ /actuator/health/readiness              │
   │     ├─ livenessProbe   ──▶ /actuator/health/liveness               │
   │     └─ preStop + graceful shutdown (drena no SIGTERM)              │
   └────────────────────────────────┬───────────────────────────────────┘
                                     ▼
   ┌─────────────────────── OBSERVABILIDADE ────────────────────────────┐
   │  /actuator/prometheus ──▶ Prometheus ──▶ Grafana (dashboards/alertas)│
   │  OTLP traces ──▶ OpenTelemetry Collector ──▶ backend de tracing      │
   │  stdout (JSON) ──▶ coletor de logs ──▶ backend de logs               │
   └─────────────────────────────────────────────────────────────────────┘
                                     ▲
                                     │  tudo orquestrado por
                              ─── CI/CD pipeline ───
```

**Trecho 1 — Dockerfile multi-stage com layered jar** (estações 1-3):

```dockerfile
# --- stage de extração: quebra o jar em camadas ---
FROM eclipse-temurin:21-jdk AS builder
WORKDIR /app
COPY order-service.jar order-service.jar
RUN java -Djarmode=tools -jar order-service.jar extract --layers --destination extracted

# --- stage final: distroless, não-root ---
FROM gcr.io/distroless/java21-debian12:nonroot
WORKDIR /app
COPY --from=builder /app/extracted/dependencies/ ./
COPY --from=builder /app/extracted/spring-boot-loader/ ./
COPY --from=builder /app/extracted/snapshot-dependencies/ ./
COPY --from=builder /app/extracted/application/ ./
ENTRYPOINT ["java", "-XX:MaxRAMPercentage=75.0", "-jar", "order-service.jar"]
```

> [!note] `jarmode=tools` é o sucessor de `layertools`
> O Spring Boot 3.3+ promove `java -Djarmode=tools ... extract` como forma canônica. A sintaxe antiga `-Djarmode=layertools` ainda existe, mas a documentação atual mostra `tools`. Confirme a versão do seu Boot antes de copiar.

**Trecho 2 — `application.yml`: probes, prometheus e shutdown** (estações 4, 5, 7, 8):

```yaml
server:
  shutdown: graceful          # drena requisições em voo no SIGTERM
spring:
  lifecycle:
    timeout-per-shutdown-phase: 30s
management:
  endpoint:
    health:
      probes:
        enabled: true         # liga os grupos liveness/readiness
  health:
    livenessState:
      enabled: true
    readinessState:
      enabled: true
  endpoints:
    web:
      exposure:
        include: health,prometheus   # /actuator/prometheus exposto
```

**Trecho 3 — `Deployment` Kubernetes** (estações 4-7):

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-service
spec:
  replicas: 3
  strategy:
    type: RollingUpdate          # deploy sem downtime
    rollingUpdate:
      maxUnavailable: 0
      maxSurge: 1
  template:
    spec:
      terminationGracePeriodSeconds: 45   # > timeout-per-shutdown-phase
      containers:
        - name: order-service
          image: registry/order-service:sha-abc123
          resources:
            requests: { cpu: "500m", memory: "512Mi" }
            limits:   { memory: "768Mi" }     # casa com MaxRAMPercentage
          envFrom:
            - configMapRef: { name: order-service-config }
            - secretRef:    { name: order-service-secrets }
          readinessProbe:
            httpGet: { path: /actuator/health/readiness, port: 8080 }
            initialDelaySeconds: 10
            periodSeconds: 5
          livenessProbe:
            httpGet: { path: /actuator/health/liveness, port: 8080 }
            initialDelaySeconds: 30
            periodSeconds: 10
          lifecycle:
            preStop:
              exec:
                command: ["sh", "-c", "sleep 5"]   # janela p/ o endpoint sair do LB
```

## Tabela de decisão

**Como construir a imagem?**

| Critério | Dockerfile multi-stage | Buildpacks (`build-image`) | Jib |
|---|---|---|---|
| Controle sobre a imagem | Total (você escreve cada camada) | Baixo (opinativo) | Médio |
| Precisa de Docker daemon? | Sim | Sim (por padrão) | **Não** (daemonless) |
| Reprodutibilidade | Depende da disciplina | Alta | Alta |
| Esforço de manutenção | Maior (Dockerfile vive) | Mínimo (zero Dockerfile) | Mínimo |
| Bom para | Times com requisitos específicos de imagem | Quem quer convenção sobre configuração | CI sem Docker, builds rápidos |
| Detalhe | [[03-Dominios/Tecnologia/Java/Cloud-native e produção/04 - Dockerfile na prática — multi-stage e layered jar\|nota 04]] | [[03-Dominios/Tecnologia/Java/Cloud-native e produção/06 - Buildpacks — imagem sem Dockerfile\|nota 06]] | [[03-Dominios/Tecnologia/Java/Cloud-native e produção/07 - Jib — imagem daemonless\|nota 07]] |

**JVM ou native image?**

| Critério | JVM (HotSpot) | GraalVM Native Image |
|---|---|---|
| Startup | Segundos (warmup do JIT) | ~Milissegundos |
| Footprint de memória | Maior | Menor |
| Peak throughput | **Maior** (JIT otimiza em runtime) | Geralmente menor |
| Tempo de build | Rápido | **Lento** (minutos) |
| Reflexão/proxies dinâmicos | Livres | Exigem *hints* (Spring AOT) |
| Diagnóstico | JFR, async-profiler maduros | Ferramental diferente/limitado |
| Bom para | Serviços de longa duração, alto tráfego | Serverless, escala-a-zero, CLI |
| Detalhe | [[03-Dominios/Tecnologia/Java/Cloud-native e produção/21 - Native vs JVM — a decisão honesta\|nota 21]] | [[03-Dominios/Tecnologia/Java/Cloud-native e produção/09 - Native Image com Spring — Spring AOT na prática\|nota 09]] |

**Head vs tail sampling de traces?**

| Critério | Head sampling | Tail sampling |
|---|---|---|
| Quando decide | No início do trace (na app) | Depois do trace completo (no Collector) |
| Custo | Baixo (descarta cedo) | Alto (bufferiza o trace todo) |
| Pega erros raros? | Não garantido | **Sim** (decide vendo o resultado) |
| Onde mora a lógica | Na aplicação / SDK | No OpenTelemetry Collector |
| Bom para | Volume alto, orçamento apertado | Quando outliers/erros são o que importa |
| Detalhe | [[03-Dominios/Tecnologia/Java/Cloud-native e produção/16 - OpenTelemetry Collector e sampling de produção\|nota 16]] | idem |

## Armadilhas

### (1) "Production-ready é só adicionar o Actuator"

O raciocínio falho: *"adicionei `spring-boot-starter-actuator`, expus `/actuator/health`, pronto — está production-ready."* O Actuator **expõe** os contratos, mas não os **cumpre** sozinho. Liveness e readiness vêm desligados como grupos até você ligar `management.endpoint.health.probes.enabled`. O readiness padrão não sabe que seu banco caiu se você não plugar o indicador. Graceful shutdown não acontece sem `server.shutdown: graceful` **e** um `terminationGracePeriodSeconds` compatível no pod. O Actuator é o **painel de instrumentos** — instalar o painel não conserta o motor.

### (2) "Tudo deve ser native"

O raciocínio falho: *"native tem startup instantâneo e usa menos RAM, então é objetivamente melhor — migre tudo."* Native image é um **trade-off de plataforma, não um upgrade**. Você troca *peak throughput* (o JIT da JVM otimiza com base no que vê em runtime — o native compila uma vez, fechado) e troca **ferramental de diagnóstico** (perde JFR maduro) por *startup* e *footprint*. Para um serviço de longa duração e alto tráfego, o native pode ser **mais lento no regime permanente**. Native brilha onde o *startup* domina o custo: *serverless*, escala-a-zero, *jobs* curtos, CLIs. Para o `order-service` rodando 24/7 com três réplicas quentes, a JVM provavelmente vence. A decisão é por **perfil de carga**, não por moda.

### (3) "Observabilidade é só ligar o Prometheus"

O raciocínio falho: *"expus `/actuator/prometheus`, o Prometheus raspa, tenho observabilidade."* Métrica é **um** dos três sinais e responde *"o quê?"* ("a latência p99 subiu"). Ela não responde *"por quê?"* nem *"onde, naquela requisição específica?"* — isso é **trace**. E não te dá o contexto do evento exato — isso é **log estruturado**. Sem os três *seams* e sem **correlação** entre eles (o `traceId` no log, o trace ligado à métrica), você tem um gráfico bonito subindo e nenhuma forma de descer até a causa. Observabilidade é a **tríade correlacionada**, não um endpoint raspado.

## Em entrevista

### Frase pronta (inglês)

> "Taking a Spring Boot service to production isn't a single step — it's a chain of contracts. I start from a layered jar, build an OCI image (Dockerfile, Buildpacks, or Jib depending on how much control I need), and make sure the JVM is container-aware so it sizes the heap from the cgroup, not the host. In the cluster, I wire liveness and readiness as separate contracts, enable graceful shutdown so SIGTERM drains in-flight requests, and externalize config through ConfigMaps and Secrets. For observability I treat metrics, traces, and logs as three correlated seams — Micrometer to Prometheus, OpenTelemetry to a Collector, and structured JSON logs to stdout. The whole thing is driven by a CI/CD pipeline, never by hand. The judgment calls I always flag are JVM versus native — a platform trade-off, not an upgrade — and head versus tail sampling, depending on whether I'm optimizing for cost or for catching rare errors."

### Vocabulário

| Termo (EN) | Significado |
|---|---|
| layered jar | jar dividido em camadas por ritmo de mudança, para cache eficiente de imagem |
| container-aware JVM | JVM que lê os limites do cgroup e dimensiona heap por `MaxRAMPercentage` |
| liveness vs readiness | "estou vivo, não reinicie" vs "posso receber tráfego agora?" |
| graceful shutdown | drenar requisições em voo no SIGTERM antes de encerrar |
| chain of contracts | a sequência de acordos (build, JVM, orquestrador, coletor) que torna o app production-ready |
| three seams (signals) | métricas, traces e logs como sinais correlacionados de observabilidade |
| head vs tail sampling | decidir amostrar o trace no início (barato) vs após vê-lo inteiro (pega outliers) |
| native image trade-off | trocar peak throughput e diagnóstico por startup e footprint |

## Cheatsheet nota→problema

| Problema em produção | Nota que resolve |
|---|---|
| "O que significa estar pronto pra produção?" | [[03-Dominios/Tecnologia/Java/Cloud-native e produção/01 - Production-ready e cloud-native — a tese honesta\|01 - Production-ready e cloud-native — a tese honesta]] |
| "O pod é morto por OOM mesmo com pouca carga" | [[03-Dominios/Tecnologia/Java/Cloud-native e produção/02 - A JVM dentro de um container\|02 - A JVM dentro de um container]] |
| "Qual é o panorama de empacotar em imagem?" | [[03-Dominios/Tecnologia/Java/Cloud-native e produção/03 - Empacotando o app numa imagem — o panorama\|03 - Empacotando o app numa imagem — o panorama]] |
| "Como escrevo um Dockerfile eficiente?" | [[03-Dominios/Tecnologia/Java/Cloud-native e produção/04 - Dockerfile na prática — multi-stage e layered jar\|04 - Dockerfile na prática — multi-stage e layered jar]] |
| "Minha imagem é gorda e cheia de CVE" | [[03-Dominios/Tecnologia/Java/Cloud-native e produção/05 - Imagem enxuta e segura — distroless e scanning\|05 - Imagem enxuta e segura — distroless e scanning]] |
| "Quero imagem sem manter Dockerfile" | [[03-Dominios/Tecnologia/Java/Cloud-native e produção/06 - Buildpacks — imagem sem Dockerfile\|06 - Buildpacks — imagem sem Dockerfile]] |
| "Meu CI não tem Docker daemon" | [[03-Dominios/Tecnologia/Java/Cloud-native e produção/07 - Jib — imagem daemonless\|07 - Jib — imagem daemonless]] |
| "O que é native image e quais os trade-offs?" | [[03-Dominios/Tecnologia/Java/Cloud-native e produção/08 - GraalVM Native Image — conceito e trade-offs\|08 - GraalVM Native Image — conceito e trade-offs]] |
| "Como faço Spring rodar como native?" | [[03-Dominios/Tecnologia/Java/Cloud-native e produção/09 - Native Image com Spring — Spring AOT na prática\|09 - Native Image com Spring — Spring AOT na prática]] |
| "O cluster reinicia meu pod sem motivo" | [[03-Dominios/Tecnologia/Java/Cloud-native e produção/10 - Health e probes — o contrato com o orquestrador\|10 - Health e probes — o contrato com o orquestrador]] |
| "Como injeto config e dimensiono recursos?" | [[03-Dominios/Tecnologia/Java/Cloud-native e produção/11 - Config e recursos no Kubernetes\|11 - Config e recursos no Kubernetes]] |
| "O deploy corta requisições no meio" | [[03-Dominios/Tecnologia/Java/Cloud-native e produção/12 - Graceful shutdown e deploy sem downtime\|12 - Graceful shutdown e deploy sem downtime]] |
| "Por onde começo a observar o serviço?" | [[03-Dominios/Tecnologia/Java/Cloud-native e produção/13 - Observabilidade de operação — o panorama e os 3 seams\|13 - Observabilidade de operação — o panorama e os 3 seams]] |
| "Como exponho métricas pro Prometheus?" | [[03-Dominios/Tecnologia/Java/Cloud-native e produção/14 - Métricas em produção — Micrometer e Prometheus\|14 - Métricas em produção — Micrometer e Prometheus]] |
| "Preciso de dashboards e alertas" | [[03-Dominios/Tecnologia/Java/Cloud-native e produção/15 - Dashboards e alertas — Grafana\|15 - Dashboards e alertas — Grafana]] |
| "Quanto trace coletar sem estourar custo?" | [[03-Dominios/Tecnologia/Java/Cloud-native e produção/16 - OpenTelemetry Collector e sampling de produção\|16 - OpenTelemetry Collector e sampling de produção]] |
| "Meus logs são texto solto, sem correlação" | [[03-Dominios/Tecnologia/Java/Cloud-native e produção/17 - Logs estruturados em produção\|17 - Logs estruturados em produção]] |
| "A latência subiu sob carga — onde está o gargalo?" | [[03-Dominios/Tecnologia/Java/Cloud-native e produção/18 - Profiling e diagnóstico sob carga — produção\|18 - Profiling e diagnóstico sob carga — produção]] |
| "Quero perfilar continuamente no cluster" | [[03-Dominios/Tecnologia/Java/Cloud-native e produção/19 - Continuous profiling no cluster — Pyroscope e async-profiler\|19 - Continuous profiling no cluster — Pyroscope e async-profiler]] |
| "Como automatizo o caminho até produção?" | [[03-Dominios/Tecnologia/Java/Cloud-native e produção/20 - CI-CD e o caminho até produção\|20 - CI-CD e o caminho até produção]] |
| "JVM ou native — qual escolho de verdade?" | [[03-Dominios/Tecnologia/Java/Cloud-native e produção/21 - Native vs JVM — a decisão honesta\|21 - Native vs JVM — a decisão honesta]] |
| "Quero ver o fluxo inteiro montado" | [[03-Dominios/Tecnologia/Java/Cloud-native e produção/22 - Capstone — do jar ao cluster\|22 - Capstone — do jar ao cluster]] (você está aqui) |

## Veja também

- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/01 - Production-ready e cloud-native — a tese honesta|Production-ready e cloud-native (a tese)]]
- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/04 - Dockerfile na prática — multi-stage e layered jar|Dockerfile na prática (empacotamento)]]
- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/10 - Health e probes — o contrato com o orquestrador|Health e probes (contrato com o orquestrador)]]
- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/13 - Observabilidade de operação — o panorama e os 3 seams|Observabilidade — os 3 seams]]
- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/20 - CI-CD e o caminho até produção|CI-CD e o caminho até produção]]
- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/21 - Native vs JVM — a decisão honesta|Native vs JVM (a decisão honesta)]]
- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/index|Cloud-native e produção (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]

## Referências

- [Spring Boot — Reference Documentation](https://docs.spring.io/spring-boot/reference/) — sintaxe canônica de probes (`management.endpoint.health.probes.enabled`), graceful shutdown (`server.shutdown`, `spring.lifecycle.timeout-per-shutdown-phase`), Prometheus (`/actuator/prometheus`) e empacotamento.
- [Spring Boot — Container Images / Layered Jars](https://docs.spring.io/spring-boot/reference/packaging/container-images/index.html) — `java -Djarmode=tools ... extract` e Buildpacks (`spring-boot:build-image`).
- [Spring Boot — GraalVM Native Image](https://docs.spring.io/spring-boot/reference/packaging/native-image/index.html) — Spring AOT e `native:compile`.
- [The Twelve-Factor App](https://12factor.net/) — os contratos de build/release/run, config, disposability e logs.
- [Kubernetes — Configure Liveness, Readiness and Startup Probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/) — semântica dos probes do lado do orquestrador.
- [OpenTelemetry — Sampling](https://opentelemetry.io/docs/concepts/sampling/) — head vs tail sampling.
