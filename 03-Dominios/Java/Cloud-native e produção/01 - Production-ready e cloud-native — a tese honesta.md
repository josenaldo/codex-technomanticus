---
title: "Production-ready e cloud-native — a tese honesta"
created: 2026-06-12
updated: 2026-06-12
type: concept
status: seedling
publish: true
fase: iniciado
tags:
  - java
  - cloud-native
  - iniciado
aliases:
  - "Production-ready"
  - "Cloud-native"
---

# Production-ready e cloud-native — a tese honesta

> [!abstract] TL;DR
> **Production-ready não é uma feature que se "liga".** É uma **postura** — um conjunto de contratos que a aplicação cumpre: ser **observável** (expõe métricas, health, logs estruturados), **descartável** (sobe rápido, morre limpo), **configurável de fora** (config no ambiente, não no jar) e ter **saúde declarada** (o orquestrador sabe se você está vivo). "Cloud-native", neste galho, é o nível de **deploy e operação** — botar esse contrato pra rodar num cluster. A **arquitetura distribuída** (microservices, Spring Cloud) é assunto do **Galho 16**, não daqui. Este galho responde à pergunta operacional: *como eu observo e opero esse jar lá em cima?* A nota-assinatura disso são os **3 seams de observabilidade** (G3, G16, G17) e a tese final: **native image é trade-off de plataforma, não upgrade.**

## O que é

Quando alguém diz que uma aplicação está "pronta para produção", a tentação é imaginar um botão — um `production: true` no `application.yml`. Não existe esse botão. **Production-ready é um conjunto de contratos que a aplicação assume com a plataforma que vai operá-la.**

O vocabulário canônico desses contratos vem dos [12 fatores](https://12factor.net/). Quatro deles formam o núcleo "operacional" que interessa a este galho:

- **Build, release, run (Fator V)** — "Strictly separate build and run stages". O artefato que você compila não é o que você executa: entre eles há um *release* (artefato + config). Você constrói uma vez, faz deploy do mesmo binário em vários ambientes, e cada ambiente injeta sua própria configuração.
- **Config (Fator III)** — "Store config in the environment". Senhas, URLs de banco, feature flags: tudo vem de fora (variáveis de ambiente, ConfigMaps, Secrets), nunca cravado no jar. O mesmo artefato roda em dev, staging e prod.
- **Processes / stateless (Fator VI)** — "Execute the app as one or more stateless processes". A aplicação não guarda estado de sessão em memória local; qualquer estado que precise sobreviver vai pra um backing service (banco, cache). É isso que permite escalar horizontalmente.
- **Disposability (Fator IX)** — "Maximize robustness with fast startup and graceful shutdown". A aplicação sobe rápido e, ao receber o sinal de término (SIGTERM), drena conexões e morre limpa. Pods nascem e morrem o tempo todo num cluster; quem não morre limpo deixa rastro.
- **Logs (Fator XI)** — "Treat logs as event streams". A aplicação não gerencia arquivos de log nem faz rotação; ela escreve no `stdout` como um fluxo contínuo de eventos, e o **ambiente de execução** (o cluster, o coletor) decide o que fazer com isso.

> [!info] A parte de arquitetura dos 12 fatores fica no Galho 16
> Os 12 fatores também têm um lado **arquitetural** — como compor serviços, tratar backing services como recursos anexados, portar concorrência via modelo de processos. Esse lado conversa com [[03-Dominios/Java/Microservices e sistemas distribuídos/index|Microservices (Galho 16)]]. Aqui ficamos com o lado **build/release/run + disposability + logs-as-event-streams**: a operação do artefato, não o desenho do sistema.

Do lado do framework, o [Spring Boot Actuator](https://docs.spring.io/spring-boot/reference/actuator/index.html) é a materialização desses contratos em Java. A documentação descreve: *"Spring Boot includes a number of additional features to help you monitor and manage your application when you push it to production."* Ele entrega **health**, **métricas**, **info** e **endpoints de gestão** (via HTTP ou JMX) — os ganchos pelos quais a plataforma observa e gerencia o processo.

## Por que importa

A confusão mais cara da carreira de quem chega à nuvem é tratar "production-ready" como uma **checklist de bibliotecas**: adicionar Actuator, adicionar Micrometer, adicionar um logger JSON, marcar as caixinhas, declarar vitória.

Mas adicionar a dependência não cumpre o contrato. Você pode ter o Actuator no classpath e ainda assim:

- expor um `/health` que retorna `UP` enquanto o banco está fora (health **mentiroso**);
- escrever logs em arquivo (violando logs-as-event-streams) porque copiou uma config de 2014;
- guardar sessão em memória local (violando stateless), o que faz a segunda réplica perder o login do usuário;
- ignorar o SIGTERM e ser morto à força após o timeout, derrubando requisições no meio.

**A diferença entre "ter Actuator" e "estar production-ready" é a diferença entre ter um estetoscópio e saber auscultar.** O contrato é comportamental, não declarativo. É por isso que este galho começa por aqui: sem entender que production-ready é **postura**, todo o resto (containers, métricas, tracing, deploy) vira culto à carga — gestos copiados sem o entendimento do porquê.

## Como funciona

### Production-ready como postura, não como feature

Pense num contrato de aluguel. Você não "liga" um inquilino bom; um inquilino bom é aquele que **cumpre cláusulas**: paga em dia, avisa antes de sair, não deixa o imóvel destruído. Production-ready é o mesmo: a aplicação cumpre cláusulas que a plataforma espera.

As quatro cláusulas centrais:

1. **Observável** — a aplicação **se deixa medir**. Expõe métricas (latência, throughput, erros), expõe saúde, e emite logs estruturados que um coletor consegue parsear. Sem isso, operar é dirigir vendado.
2. **Descartável (disposable)** — sobe rápido e morre limpo. Num cluster, o orquestrador mata e recria pods o tempo todo (deploy, autoscaling, falha de nó). Quem demora pra subir atrasa o deploy; quem não trata o SIGTERM corrompe requisições.
3. **Configurável de fora** — o mesmo artefato roda em qualquer ambiente porque toda a variação vem de injeção externa. Isso é o que torna o pipeline *build → release → run* honesto: você constrói uma vez e promove o mesmo binário.
4. **Saúde declarada** — a aplicação responde a perguntas padronizadas: "você está vivo?" (liveness) e "você consegue receber tráfego?" (readiness). O orquestrador toma decisões com base nessas respostas; um health que sempre diz `UP` engana o orquestrador.

Nenhuma dessas cláusulas é uma biblioteca. Bibliotecas (Actuator, Micrometer) são **ferramentas para cumprir** o contrato — não o contrato em si.

### Cloud-native: nível de operação, não nível de arquitetura

Aqui mora a ambiguidade que mais confunde. "Cloud-native" significa coisas diferentes em camadas diferentes:

- **Cloud-native como arquitetura** — desenhar o sistema como serviços independentes, comunicação resiliente, service discovery, circuit breakers. Isso é **microservices e Spring Cloud**, e é assunto do **[[03-Dominios/Java/Microservices e sistemas distribuídos/index|Galho 16]]**. Não vamos re-explicar microservices aqui.
- **Cloud-native como operação** — empacotar a aplicação num container, declarar seus recursos, expor seus health probes, mandar métricas e logs pra um stack de observabilidade, fazer deploy num orquestrador. **Isto é o Galho 17.**

A distinção importa porque você pode ser cloud-native-operação **sem** ser cloud-native-arquitetura. Um monólito Spring Boot bem comportado — containerizado, com Actuator, logs estruturados, graceful shutdown, métricas Prometheus — é **perfeitamente cloud-native na camada de operação**, mesmo sem ser um sistema distribuído. A nuvem opera monólitos felizes o tempo todo.

> [!tip] Regra de bolso
> Se a pergunta é *"como divido isso em serviços?"* → Galho 16 (arquitetura). Se a pergunta é *"como observo e opero esse processo no cluster?"* → Galho 17 (operação). Este galho fica do lado direito.

### Os 3 seams de observabilidade

Observabilidade aparece em três galhos diferentes da trilha, e a fonte de confusão é achar que é tudo a mesma coisa. Não é. Há **três costuras (seams)** distintas, cada uma operando numa camada:

| Seam | Galho | Camada | Pergunta que responde |
| --- | --- | --- | --- |
| **Interna da JVM** | G3 (JVM) | Dentro do processo | "Como está o heap, o GC, as threads desta JVM?" |
| **Correlação de trace** | G16 (Microservices) | Entre serviços, no código | "Por onde passou esta requisição que cruzou 5 serviços?" |
| **Operação no cluster** | **G17 (este galho)** | No cluster, fora do código | "Como está a saúde do stack inteiro? Quais métricas e logs estão chegando?" |

Detalhando cada seam:

- **G3 — observabilidade INTERNA da JVM.** Ferramentas como JFR (Java Flight Recorder) e JMC, inspeção de heap, comportamento do garbage collector. É introspecção da própria máquina virtual, e **já está coberta no Galho 3**. Não repetimos aqui.
- **G16 — correlação de trace NO CÓDIGO.** Quando uma requisição atravessa vários serviços, você precisa de um `traceId` que costure os saltos. Isso é instrumentação **dentro do código** (Micrometer Tracing propagando o contexto), e pertence ao mundo distribuído do **Galho 16**.
- **G17 — OPERAR o stack no cluster.** Aqui não estamos *dentro* da JVM nem *dentro* do código de negócio. Estamos no plano de operação: expor métricas no formato Prometheus e visualizá-las no Grafana, rodar um OTel Collector que recebe métricas/traces/logs, configurar **sampling** (você não guarda 100% dos traces — seria caro demais), e emitir **logs estruturados** (JSON) que um agregador consegue indexar.

Esses três seams **não competem** — eles se empilham. A JVM se observa por dentro (G3), o código correlaciona requisições (G16), e o cluster coleta e opera tudo isso (G17). Este galho mora na terceira camada.

> [!info] A tese sobre native image
> Compilar a aplicação para **native image** (GraalVM) entrega startup quase instantâneo e baixo consumo de memória — atraente para disposability e para cenários serverless. Mas é um **trade-off de plataforma**, não um upgrade gratuito: você troca o JIT e o tooling maduro da JVM (incluindo boa parte da observabilidade interna de G3, como JFR) por restrições de reflexão, builds longos e um ecossistema de diagnóstico mais novo. Native image é uma **escolha de plataforma** com custos próprios — não um "modo turbo" que se ativa sem consequências.

## Na prática

Imagine um serviço neutro, `order-service`, que precisa ir de "roda na minha máquina" a "opera no cluster".

O percurso production-ready, em ordem de contrato:

1. **Configurável de fora** — a URL do banco e as credenciais saem do `application.yml` cravado e passam a vir de variáveis de ambiente / Secrets. O `order-service` agora roda idêntico em dev e prod; só muda a injeção.
2. **Saúde declarada** — o `order-service` expõe `/actuator/health` com checagens de liveness (o processo respira?) e readiness (o banco está acessível, dá pra receber tráfego?). Um health honesto retorna `DOWN` quando a dependência crítica caiu, em vez de mentir `UP`.
3. **Descartável** — habilita-se graceful shutdown: ao receber SIGTERM, o `order-service` para de aceitar novas requisições, drena as em andamento e encerra. Nenhum pedido morre no meio durante um deploy.
4. **Observável (métricas)** — expõe métricas no formato Prometheus (`/actuator/prometheus`): taxa de pedidos, latência, erros. Um Prometheus raspa esse endpoint; um Grafana desenha os gráficos.
5. **Observável (logs)** — em vez de escrever num arquivo, o `order-service` emite logs estruturados em JSON no `stdout`. O cluster captura o fluxo e um agregador indexa. Logs viram eventos pesquisáveis, não arquivos a girar.
6. **Coleta unificada** — um **OTel Collector** recebe métricas, traces e logs do `order-service`, aplica **sampling** nos traces (guarda uma fração representativa) e encaminha pro backend de observabilidade.

Note o que **não** aparece nessa lista: nada sobre dividir o `order-service` em sub-serviços, service discovery ou circuit breakers. Isso seria reprojetar a arquitetura — território do Galho 16. Aqui o `order-service` continua sendo o mesmo serviço; o que muda é como ele **se deixa operar**.

## Armadilhas

### (1) Tratar production-ready como uma checklist de features

A armadilha mais comum: "adicionei Actuator, Micrometer e um logger JSON, logo estou production-ready". **Falso.** Production-ready é comportamental. Você pode ter todas as dependências e ainda violar todos os contratos — health que mente, logs em arquivo, sessão em memória, SIGTERM ignorado. A pergunta certa nunca é *"quais bibliotecas eu adicionei?"*, mas *"a aplicação cumpre os contratos de observabilidade, descartabilidade, configuração externa e saúde?"*. Ferramenta é meio; contrato é fim.

### (2) Confundir cloud-native-arquitetura (G16) com cloud-native-operação (este galho)

Quando alguém diz "vamos ficar cloud-native", pergunte **qual camada**. Se a resposta for "quebrar o monólito em microservices", isso é **arquitetura** — Galho 16, decisão cara e com trade-offs de complexidade distribuída. Se a resposta for "containerizar, expor health probes, mandar métricas pro Grafana", isso é **operação** — este galho, e você não precisa de microservices pra fazer. Tratar as duas como sinônimo leva ao erro caríssimo de **fragmentar um monólito que só precisava ser bem operado**. Um monólito containerizado e observável já é cloud-native na camada que importa pra operação.

### (3) Achar que native image é upgrade, não trade-off

Migrar pra native image porque "é mais rápido" sem pesar os custos — perda de tooling de diagnóstico da JVM, restrições de reflexão, builds longos — é confundir trade-off com upgrade. Native image resolve problemas específicos (cold start, footprint de memória) ao preço de outros. É decisão de plataforma, não otimização universal.

## Em entrevista

### Frase pronta (inglês)

> "Being *production-ready* isn't a feature you toggle on — it's a posture, a set of contracts the application honors with its platform: it has to be **observable**, **disposable**, **externally configurable**, and expose a **declared health**. In this context I separate *cloud-native as architecture* — splitting into microservices, which is a distributed-systems concern — from *cloud-native as operation* — containerizing, exposing health probes, and shipping metrics and structured logs to an observability stack. A well-behaved monolith can be perfectly cloud-native at the operational level. And I treat native image as a **platform trade-off**, not a free upgrade: it buys fast startup at the cost of mature JVM tooling and reflection constraints."

### Vocabulário

| Termo PT | Termo EN |
| --- | --- |
| pronto pra produção | production-ready |
| nativo de nuvem | cloud-native |
| descartabilidade | disposability |
| observabilidade | observability |
| contrato | contract |
| plano de controle | control plane |
| desligamento gracioso | graceful shutdown |
| saúde declarada | declared health |
| logs estruturados | structured logs |
| imagem nativa | native image |
| amostragem | sampling |

## Veja também

- [[03-Dominios/Java/Cloud-native e produção/02 - A JVM dentro de um container|A JVM dentro de um container]]
- [[03-Dominios/Java/Cloud-native e produção/13 - Observabilidade de operação — o panorama e os 3 seams|Observabilidade de operação]]
- [[03-Dominios/Java/Cloud-native e produção/22 - Capstone — do jar ao cluster|Capstone — do jar ao cluster]]
- [[03-Dominios/Java/Microservices e sistemas distribuídos/index|Microservices e sistemas distribuídos (Galho 16)]] ← fronteira de arquitetura distribuída
- [[03-Dominios/Java/Cloud-native e produção/index|Cloud-native e produção (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]

> [!note] O que vem depois
> Este galho 17 é onde a plataforma de produção é tratada. O **Galho 18 (Certificação Java OCP)** fecha a trilha, mapeando a prova aos galhos de linguagem — é texto "(planejado)".

## Referências

- *The Twelve-Factor App* — 12factor.net (fatores III Config, V Build/release/run, VI Processes, IX Disposability, XI Logs). Acesso 2026-06-12.
- *Spring Boot Actuator — Production-ready Features*. docs.spring.io/spring-boot/reference/actuator. Acesso 2026-06-12.

## Referências

- [The Twelve-Factor App](https://12factor.net/) — fatores III (Config), V (Build/release/run), VI (Processes/stateless), IX (Disposability), XI (Logs as event streams).
- [Spring Boot Actuator — Production-ready Features](https://docs.spring.io/spring-boot/reference/actuator/index.html) — health, métricas, info e endpoints de gestão via HTTP/JMX.
