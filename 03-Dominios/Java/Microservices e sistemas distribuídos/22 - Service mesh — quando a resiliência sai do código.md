---
title: "Service mesh — quando a resiliência sai do código"
created: 2026-06-12
updated: 2026-06-12
type: concept
status: seedling
publish: true
fase: magus
tags:
  - java
  - microservices
  - magus
  - service-mesh
aliases:
  - "Service mesh"
  - "Istio"
  - "Linkerd"
  - "Sidecar"
---

# Service mesh — quando a resiliência sai do código

> [!abstract] TL;DR
> **Service mesh** é uma camada de infraestrutura que assume a comunicação serviço-a-serviço, tirando do *código da aplicação* responsabilidades como **mTLS**, **retries**, **circuit breaking**, **traffic shaping** e **observabilidade**. Ela é feita de duas partes: um **data plane** (proxies que interceptam todo o tráfego — o clássico *sidecar* Envoy "de carona" ao lado de cada serviço) e um **control plane** (o cérebro que distribui política e certificados). **Istio** oferece dois modos — *sidecar* (Envoy por pod) e *ambient* (ztunnel L4 por nó + waypoint L7 opcional, pronto para produção single-cluster desde a versão **1.22**). **Linkerd** usa um *micro-proxy* próprio escrito em **Rust** (não Envoy). A tese desta nota: quando o mesh entrega retry e circuit breaking na malha, parte do que o **Resilience4j** faz no código vira **redundante** — e duplicar essas políticas é uma armadilha real.

## O que é

Imagine que cada um dos seus serviços, em vez de falar direto com os outros pela rede, sempre fala primeiro com um **porteiro pessoal** que mora ao lado dele. Esse porteiro intercepta tudo que entra e tudo que sai, cuida da criptografia, decide se vale a pena repetir uma chamada que falhou, mede o tempo de cada requisição e reporta métricas. Todos os porteiros recebem ordens de um **escritório central**. Esse conjunto — porteiros + escritório central — é o **service mesh** (malha de serviço).

Em termos técnicos:

- O **data plane** ("plano de dados") é o exército de **proxies** que fica no caminho de cada chamada. No modelo clássico, cada proxy é um **sidecar** ("carro lateral") — um contêiner extra rodando ao lado do contêiner da aplicação, dentro do mesmo pod. O proxy mais usado nesse papel é o **Envoy**.
- O **control plane** ("plano de controle") é o cérebro: ele não fica no caminho das requisições, mas configura os proxies, distribui certificados, propaga políticas de roteamento e resiliência, e agrega telemetria.

A ideia-chave é **mover a lógica de comunicação para fora do código de negócio**. Em vez de cada serviço Java importar uma biblioteca de retry, configurar TLS na mão e instrumentar tracing, o mesh faz isso de forma transparente, na infraestrutura, sem o serviço "saber".

## Por que importa

Para alguém vindo do mundo Spring Boot, a primeira reação é: "mas eu já faço retry com Resilience4j, já tenho mTLS configurado, já tenho Micrometer exportando métricas — por que preciso de um mesh?".

A resposta tem três camadas:

1. **Consistência poliglota.** Resilência *no código* só vale para *aquela* linguagem e *aquela* biblioteca. Se metade da sua frota é Java/Spring e a outra metade é Go ou Python, você acaba reimplementando retry, timeout e circuit breaker N vezes, com comportamentos sutilmente diferentes. O mesh aplica a *mesma* política, do *mesmo jeito*, para *todos* os serviços, independente da stack.
2. **Separação de responsabilidades.** Quem decide a política de timeout entre o serviço de pagamento e o de fraude? O time de plataforma/SRE muitas vezes quer ajustar isso *sem* redeploy do código de negócio. O mesh torna resiliência e segurança **configuração de infra**, não release de aplicação.
3. **Observabilidade uniforme.** Como o proxy vê *todo* o tráfego L7, ele gera métricas douradas (latência, taxa de erro, throughput) e contexto de trace **sem instrumentação manual** em cada serviço.

> [!info] Onde isto entra na trilha
> Esta nota é **conceitual**: o que o mesh é e qual problema resolve. **Instalar e operar Istio ou Linkerd em produção** — perfis de injeção, gateways, políticas YAML, upgrade do control plane — **fica fora do escopo desta trilha**.

## Como funciona

### Data plane (sidecar) e control plane

O coração do mesh é a divisão entre **quem está no caminho do pacote** e **quem manda**.

O **data plane** é composto pelos **proxies**. No modo sidecar, o padrão de injeção funciona assim: quando seu pod sobe, um *admission controller* injeta automaticamente um contêiner-proxy ao lado do seu contêiner de aplicação. O tráfego do app é redirecionado (via `iptables` ou eBPF) para passar pelo proxy *antes* de sair para a rede e *depois* de chegar. O app continua achando que abriu uma conexão TCP normal — o proxy é **transparente**.

O **control plane** observa o cluster (quais serviços existem, onde estão, quais políticas valem) e empurra essa configuração para cada proxy. Ele também é a **autoridade certificadora** que emite e rotaciona as identidades usadas no mTLS. Como ele *não* está no caminho das requisições, uma queda momentânea do control plane não derruba o tráfego em andamento — os proxies seguem com a última config que receberam.

> [!tip] Por que "sidecar" e não "biblioteca"?
> Uma biblioteca (como o Resilience4j) roda **dentro** do seu processo: compartilha JVM, heap e ciclo de release. Um sidecar roda **ao lado**, em outro processo/contêiner: upgrade do proxy não recompila seu código, e a política é a mesma para qualquer linguagem. O custo é um *hop* de rede local extra e mais memória por pod.

### O que o mesh entrega

Movendo lógica do código para a malha, um mesh maduro tipicamente oferece:

- **mTLS (TLS mútuo):** criptografia *e* autenticação bidirecional entre serviços, automática. Cada proxy apresenta um certificado de identidade; o control plane os emite e rotaciona. O serviço Java não toca em keystore nenhum.
- **Retries:** o proxy reenvia chamadas que falham por causas idempotentes/transientes, segundo uma política central.
- **Circuit breaking:** o proxy corta tráfego para um *backend* que está respondendo mal (ejeção de outliers, limites de conexões/requisições pendentes), protegendo o sistema de cascata.
- **Traffic shaping:** roteamento ponderado para *canary*, *blue-green* e *A/B* — mandar 5% do tráfego para a nova versão é configuração, não código.
- **Observabilidade:** métricas douradas, logs de acesso e propagação de contexto de trace, geradas no proxy.

> [!example] Feynman: a malha é uma "alfândega" da rede interna
> Pense no mesh como uma alfândega instalada em cada fronteira da sua rede interna. Todo pacote passa por um agente (proxy) que confere documentos (mTLS), decide se um pacote perdido deve ser reenviado (retry), barra remessas para um destino congestionado (circuit breaking), desvia uma fração da carga para uma rota de teste (traffic shaping) e anota tudo num livro de registros (observabilidade). O exportador (seu serviço) não precisa conhecer nada dessas regras — a alfândega aplica.

### Istio (sidecar vs ambient) e Linkerd (micro-proxy em Rust)

Os dois meshes mais conhecidos fazem escolhas diferentes de **data plane**.

**Istio** historicamente usa o **Envoy** como sidecar (um Envoy por pod) e, desde 2022, introduziu um segundo modo, o **ambient** ("sem sidecar" / *sidecar-less*), que divide o data plane em duas peças:

- **ztunnel** — um proxy **L4 por nó** (um por máquina, não por pod), responsável por mTLS e pelo transporte seguro de todo o tráfego daquele nó. É leve e cuida só de camada 4.
- **waypoint** — um proxy **L7 opcional** (um Envoy compartilhado, tipicamente por *namespace*) que você habilita **só onde precisa** de recursos de camada 7 (retries HTTP, roteamento por header, *traffic shaping* avançado).

Segundo a documentação oficial (Istio, linha ~1.30.x em 2026), o modo **ambient é considerado pronto para produção em cenário *single-cluster* desde a versão 1.22**. A motivação do ambient é reduzir o custo de recursos: em vez de um Envoy completo em *cada* pod, você tem um L4 por nó e L7 só onde justifica.

**Linkerd** faz uma aposta diferente: em vez do Envoy, usa um **micro-proxy próprio escrito em Rust** (o `linkerd2-proxy`), projetado especificamente para o caso de uso de mesh — bem menor e mais simples que um Envoy de propósito geral. A documentação oficial ("Why Linkerd doesn't use Envoy") confirma que a escolha de *não* usar Envoy é deliberada. Em versão recente (Linkerd 2.19, 2026), ele entrega mTLS automático, *retries*/timeouts de HTTP e gRPC, *circuit breaking*, *traffic splitting* e métricas automáticas.

> [!note] A tese desta nota: o mesh pode tornar o Resilience4j redundante
> Se o **mesh** já aplica **retries** e **circuit breaking** na malha, *parte* do papel do **Resilience4j** (ver [[03-Dominios/Java/Microservices e sistemas distribuídos/13 - Resiliência I — a falha distribuída e o Circuit Breaker|Circuit Breaker (resiliência no código)]]) passa a ser **redundante** para chamadas *serviço-a-serviço*. A tensão **in-app vs malha** é real: não se deve **duplicar** a mesma política nos dois lugares, sob pena de o comportamento combinado ficar imprevisível (ver Armadilhas). Em geral, sobra para o código a resiliência que o mesh *não* enxerga: chamadas a recursos *fora* da malha (bancos, brokers, APIs de terceiros), *bulkheads* de thread pool dentro do processo, *fallbacks* com lógica de negócio.

## Na prática

O diagrama abaixo mostra o modelo sidecar e a separação data plane / control plane usando domínios neutros (um serviço de **pedidos** chamando um de **catálogo**). Note que toda chamada entra e sai pelo proxy local — o app nunca fala "na rede crua".

```text
                         CONTROL PLANE
                  (config, certificados, política)
                 ┌──────────────────────────────┐
                 │   distribui config + certs    │
                 └───────┬───────────────┬───────┘
                         │  (xDS / config) │
            ┌────────────▼───────┐  ┌──────▼─────────────┐
            │  POD: pedidos      │  │  POD: catalogo     │
            │ ┌────────┐ ┌─────┐ │  │ ┌─────┐ ┌────────┐ │
   req ───▶ │ │  app   │▶│proxy│─┼──┼▶│proxy│▶│  app   │ │
            │ │(Spring)│ │ ◀── sidecar ──▶ │ │(Spring)│ │
            │ └────────┘ └─────┘ │  │ └─────┘ └────────┘ │
            └────────────────────┘  └────────────────────┘
                   DATA PLANE              DATA PLANE
        (mTLS, retry, circuit breaking, métricas — no proxy)
```

E o modo **ambient** do Istio, que troca o sidecar-por-pod por um ztunnel-por-nó (L4) e um waypoint opcional (L7):

```text
                    CONTROL PLANE
                         │
       NÓ (máquina) ─────┼─────────────────────────
       ┌──────────────┐  │   ┌────────────────────┐
       │ pod: pedidos │  │   │ waypoint (L7, OPT)  │
       │   (app)      │  │   │  Envoy compartilhado│
       └──────┬───────┘  │   │  retry/route HTTP   │
              │          │   └─────────▲──────────┘
              ▼          │             │ (só quando precisa de L7)
       ┌──────────────────────────────┴───────┐
       │   ztunnel  (L4 por nó — mTLS/transporte)│
       └────────────────────────────────────────┘
```

> [!warning] Decisão de design, não receita de instalação
> Os diagramas acima são conceituais. **Habilitar injeção de sidecar, ligar ambient, criar waypoints, escrever políticas YAML** e operar upgrades **fica fora do escopo desta trilha**. Aqui o objetivo é entender *onde* a resiliência passa a morar.

## Armadilhas

### (1) Resiliência DUPLICADA: app + mesh multiplicando retries

A armadilha mais perigosa. Se o **Resilience4j** no serviço de pedidos tenta 3 vezes, e o **proxy do mesh** *também* tenta 3 vezes cada uma dessas tentativas, você não tem 3 retries — tem **3 × 3 = 9** chamadas ao serviço de destino. Num pico de falha transiente, isso vira um **retry storm** que *amplifica* a sobrecarga exatamente quando o sistema está mais frágil. Regra prática: **escolha um único lugar** para retry/circuit breaking por tipo de chamada. Para tráfego serviço-a-serviço *dentro* da malha, prefira o mesh e *desligue* a política equivalente no código (ou vice-versa) — mas **nunca os dois ativos para o mesmo salto**.

### (2) Adotar o mesh sem necessidade real

Um service mesh é uma peça de infraestrutura com **custo operacional alto**: você ganha um control plane para versionar, monitorar e atualizar; proxies que consomem CPU/memória e somam um *hop* de latência; e uma nova superfície de depuração ("o pacote sumiu — foi o app, a rede ou o proxy?"). Para um punhado de serviços homogêneos (digamos, tudo em Java/Spring), bibliotecas in-app como Resilience4j + tracing nativo podem entregar 90% do valor com **uma fração da complexidade**. O mesh começa a se pagar com **escala** (muitos serviços), **heterogeneidade** (várias linguagens) e **necessidade de política central** (segurança/SRE separados do desenvolvimento). Adotar "porque é moderno" é trocar um problema conhecido por uma plataforma inteira para operar.

### (3) Achar que o mesh dispensa *pensar* resiliência

O mesh fornece os **mecanismos** (retry, circuit breaker, timeout), mas **não decide os valores** por você. Quantos retries? Com qual *backoff*? Qual o **budget de retry** (o teto de tentativas extras por janela, para o retry não virar amplificador)? Qual timeout para a chamada de catálogo vs a de pagamento? Essas continuam sendo **decisões de engenharia** que dependem do contrato e da criticidade de cada serviço. Pior: mesh esconde tão bem a rede que dá a *ilusão* de que "está tratado". Timeout mal calibrado e ausência de retry budget causam incidentes **com ou sem** mesh — a malha só muda *onde* você configura, não *se* você precisa pensar (ver [[03-Dominios/Java/Microservices e sistemas distribuídos/21 - Os padrões de falha distribuída|Os padrões de falha distribuída]]).

## Em entrevista

### Frase pronta (inglês)

> A service mesh moves cross-cutting communication concerns — mutual TLS, retries, circuit breaking, traffic shaping and observability — out of the application code and into the infrastructure. It does this with a data plane of proxies, classically an Envoy sidecar running alongside each service, coordinated by a control plane that distributes policy and certificates. Istio supports both the sidecar model and an ambient, sidecar-less mode with a per-node L4 ztunnel and an optional L7 waypoint, while Linkerd ships a purpose-built micro-proxy written in Rust instead of Envoy. The architectural trade-off I always raise is that once the mesh handles retries and circuit breaking, library-level resilience like Resilience4j becomes redundant for in-mesh calls — so I make sure those policies live in exactly one place to avoid multiplying retries.

### Vocabulário

| Português | Inglês |
| --- | --- |
| malha de serviço | service mesh |
| plano de dados | data plane |
| plano de controle | control plane |
| carro lateral | sidecar |
| mesh sem sidecar (ambient) | sidecar-less ambient |
| TLS mútuo | mutual TLS |
| limitação de circuito | circuit breaking |
| modelagem de tráfego | traffic shaping |
| orçamento de retentativas | retry budget |

## Veja também

- [[03-Dominios/Java/Microservices e sistemas distribuídos/13 - Resiliência I — a falha distribuída e o Circuit Breaker|Circuit Breaker (resiliência no código)]]
- [[03-Dominios/Java/Microservices e sistemas distribuídos/17 - Segurança entre serviços|Segurança entre serviços (mTLS)]]
- [[03-Dominios/Java/Microservices e sistemas distribuídos/21 - Os padrões de falha distribuída|Os padrões de falha distribuída]]
- [[03-Dominios/Java/Microservices e sistemas distribuídos/index|Microservices e sistemas distribuídos (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]

## Referências

- Istio — *Data Plane Modes* (sidecar vs ambient; ztunnel L4 por nó, waypoint L7 opcional; ambient production-ready single-cluster desde 1.22). Documentação Istio (linha ~1.30.x). https://istio.io/latest/docs/overview/dataplane-modes/ — acesso em 2026-06-12.
- Linkerd — *Features* (mTLS automático, retries/timeouts HTTP e gRPC, traffic splitting, observabilidade). Linkerd 2.19. https://linkerd.io/2-edge/features/ — acesso em 2026-06-12.
- Linkerd — *Architecture* (micro-proxy `linkerd2-proxy` escrito em Rust, não baseado em Envoy; suporte a circuit breaking). https://linkerd.io/2-edge/reference/architecture/ — acesso em 2026-06-12.
