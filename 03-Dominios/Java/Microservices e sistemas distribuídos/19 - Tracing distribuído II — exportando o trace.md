---
title: "Tracing distribuído II — exportando o trace"
created: 2026-06-12
updated: 2026-06-12
type: concept
status: seedling
publish: true
fase: adepto
tags:
  - java
  - microservices
  - adepto
  - tracing
  - observability
aliases:
  - "OpenTelemetry"
  - "OTLP"
  - "Exportando traces"
---

# Tracing distribuído II — exportando o trace

> [!abstract] TL;DR
> A [[03-Dominios/Java/Microservices e sistemas distribuídos/18 - Tracing distribuído I — correlação no código|nota anterior]] mostrou como o `traceId`/`spanId` nascem e se propagam no código. Mas um span que só existe em memória não serve pra nada: ele precisa ser **exportado** pra um backend onde você possa visualizá-lo. No mundo Spring Boot, a instrumentação é o **Micrometer Tracing**, uma fachada neutra; quem fala com o backend é um **bridge**. São dois caminhos mutuamente exclusivos: `micrometer-tracing-bridge-otel` exporta via **OpenTelemetry/OTLP** (pra um coletor OTLP, Jaeger, etc.) e `micrometer-tracing-bridge-brave` exporta no formato **Brave/Zipkin**. **OpenTelemetry** é o projeto **CNCF vendor-neutral** que padroniza tudo isso: a *spec*, os *SDKs*, as *semantic conventions* e o **OTLP** (o protocolo de wire). Você configura o endpoint de export e o **sampling** (`management.tracing.sampling.probability`) e lê o resultado como uma **cascata (waterfall)** no Jaeger ou Zipkin. **Esta nota para na borda do app**: instrumentar e exportar. *Operar* o coletor, os dashboards e a estratégia de sampling de produção é outro galho.

## O que é

**Exportar o trace** é pegar os spans que o app produziu em memória — cada um com seu `traceId`, `spanId`, timestamps e tags — e **enviá-los por rede** a um sistema externo que os armazena, indexa e desenha. Sem export, o trace morre no processo que o gerou.

No ecossistema Spring Boot 3.x a peça de instrumentação é o **Micrometer Tracing**. Ele não é, por si só, um tracer: é uma **fachada** (uma extensão do `ObservationHandler` do Micrometer) que delega o trabalho de verdade a um **tracer backend**. A ponte entre a fachada e o tracer concreto é o que se chama de **bridge**.

Há duas pontes possíveis, e você escolhe **uma**:

- **`micrometer-tracing-bridge-otel`** — liga o Micrometer ao SDK do **OpenTelemetry**. Os spans saem no protocolo **OTLP**.
- **`micrometer-tracing-bridge-brave`** — liga o Micrometer ao **Brave** (o tracer da OpenZipkin). Os spans saem no formato do **Zipkin**.

Por baixo dos dois está a mesma ideia que esta nota explora: **OpenTelemetry**, o padrão CNCF que define *como* a telemetria é descrita e transmitida, e a leitura do resultado como uma **waterfall** num visualizador.

> [!info] Onde esta nota para
> Aqui tratamos do **ângulo de código/config do app**: quais dependências adicionar, qual endpoint apontar, qual taxa de amostragem declarar. *Rodar* o backend que recebe esses dados é assunto de operação (ver o callout de seam mais abaixo).

## Por que importa

A nota 18 deu a você o trace *correlacionado* dentro de um serviço. Mas o valor de tracing distribuído só aparece quando você **junta os spans de vários serviços** numa visão única — e isso exige que cada serviço **exporte** seus spans pra um lugar comum.

A decisão de **qual bridge** usar é arquitetural, não cosmética. Ela define o **formato de wire**, o **backend compatível** e o **vocabulário** (semantic conventions) dos seus dados. Trocar de bridge depois que a frota inteira está instrumentada é caro. Então entender a diferença `otel` vs `brave` — e por que o mundo convergiu pra **OpenTelemetry** — é o tipo de decisão que um entrevistador sênior espera que você saiba justificar.

Pense numa analogia postal. O Micrometer Tracing é o **funcionário que prepara a encomenda** (empacota o span). O bridge é a **transportadora** que você contrata. OTLP e Zipkin são **formatos de etiqueta** diferentes: a encomenda é a mesma, mas a etiqueta dita quem consegue lê-la no destino. E o backend (Jaeger, Zipkin) é o **centro de distribuição** que recebe tudo e te mostra o mapa da entrega. Se você colar a etiqueta errada, a encomenda chega mas ninguém a entende.

A segunda razão é **custo**. Tracing não é grátis: cada span é dado que viaja pela rede e ocupa armazenamento no backend. A taxa de **sampling** é a alavanca que decide *quanto* disso você de fato exporta — e errar essa alavanca em produção é uma das armadilhas clássicas (ver abaixo).

## Como funciona

### Os dois bridges: `otel` vs `brave`

O Micrometer Tracing sozinho não exporta nada. Você precisa acoplar **um** bridge ao classpath, e ele decide o tracer concreto e o formato de saída.

**`micrometer-tracing-bridge-otel`** acopla o **SDK do OpenTelemetry** por baixo do Micrometer. Toda `Observation` que você cria no código vira um span do OTel, e esse span é exportado via **OTLP** — o protocolo nativo do OpenTelemetry. É o caminho recomendado hoje, porque te conecta ao ecossistema CNCF inteiro: coletor OTLP, Jaeger (que recebe OTLP nativamente nas versões modernas), e praticamente qualquer backend comercial.

**`micrometer-tracing-bridge-brave`** acopla o **Brave**, o tracer da família OpenZipkin. Os spans saem no **formato Zipkin** e vão pra um servidor Zipkin (tipicamente em `/api/v2/spans`). É o caminho histórico — quem vem do Spring Cloud Sleuth clássico já conhece o Brave —, ainda perfeitamente válido se a sua infra de observabilidade é Zipkin.

A regra de ouro: **um bridge por vez**. Os dois no mesmo classpath produzem configuração ambígua (ver Armadilhas). A escolha do bridge é a escolha do backend.

> [!tip] O que muda e o que não muda
> Trocar de bridge **não muda o seu código de instrumentação** — você continua usando `Observation`/`@Observed` do Micrometer exatamente igual. Muda só a dependência e o formato exportado. Essa é justamente a graça da fachada neutra: o código de negócio não sabe (nem deveria saber) se o destino é OTLP ou Zipkin.

### O que é OpenTelemetry (e o que é OTLP)

**OpenTelemetry** (frequentemente abreviado **OTel**) é um **projeto da CNCF** (Cloud Native Computing Foundation), nascido da fusão do **OpenTracing** com o **OpenCensus**. É um *framework de observabilidade* **vendor-neutral**: ele não te prende a nenhum fornecedor de backend.

OpenTelemetry **não é** um backend de observabilidade. Ele **gera e exporta** telemetria (traces, métricas e logs), mas o **armazenamento e a visualização** ficam por conta de outras ferramentas (Jaeger, Prometheus, ou produtos comerciais). Confundir os dois papéis é uma armadilha recorrente (ver abaixo).

O que o OpenTelemetry de fato entrega é um conjunto de padrões e artefatos:

- **Especificação (spec)** — o contrato formal de o que é um span, um trace, um contexto.
- **SDKs** — implementações por linguagem da spec (é o que o bridge `otel` traz pro seu app Java).
- **Semantic conventions** — nomes padronizados pros atributos comuns (ex.: `http.request.method`, `db.system`). Isso é o que faz dois serviços de equipes diferentes "falarem a mesma língua" no trace.
- **OTLP (OpenTelemetry Protocol)** — o **protocolo de wire**: define *como* a telemetria é estruturada e transmitida pela rede. É o formato que o bridge `otel` usa pra exportar.
- **O Collector** — um proxy que recebe, processa e reexporta telemetria. (Operá-lo é outro galho — ver o seam.)

A síntese mental: **OpenTelemetry = a linguagem comum**; **OTLP = o envelope em que essa linguagem viaja**; **Jaeger/Zipkin = quem lê as cartas e desenha o mapa**.

### Configuração de export e sampling

Com o bridge no lugar, faltam duas decisões de config: **pra onde** exportar e **quanto** exportar.

**Endpoint de export.** No caminho OTLP, você aponta o endpoint do receptor OTLP (um coletor, ou um Jaeger que recebe OTLP). A porta convencional do OTLP é a **4317** (gRPC) ou **4318** (HTTP). No caminho Zipkin/Brave, você aponta o endpoint do servidor Zipkin (tipicamente `http://host:9411/api/v2/spans`).

> [!warning] Nome da propriedade do endpoint OTLP variou entre versões
> A propriedade exata que aponta o endpoint OTLP **mudou de nome ao longo das versões do Spring Boot** (historicamente `management.otlp.tracing.endpoint`; releases mais recentes reorganizaram esse namespace de export). **Confira a doc da sua versão exata** antes de copiar a chave — o exemplo na seção "Na prática" usa a forma histórica estável e marca isso explicitamente.

**Sampling.** A propriedade canônica é **`management.tracing.sampling.probability`** — um número entre `0.0` e `1.0` que diz a **fração** de traces que serão amostrados (e portanto exportados). O default do Spring Boot é conservador (`0.1`, ou seja, 10%). Você sobe pra `1.0` (100%) só em **dev/local**, pra ver tudo enquanto depura.

A decisão de sampling é o nó górdio do tracing: amostrar de menos e você perde a transação problemática justamente quando precisa dela; amostrar de mais e você afoga o backend em dado e estoura o custo. Em produção, isso vira uma estratégia inteira (head-based, tail-based, adaptativo) — e *essa* estratégia é território de operação, não do código do app (ver o seam).

> [!example] Feynman: o que "probability 0.1" quer dizer
> Imagine que cada requisição que entra no seu serviço joga um dado de 10 faces. Se cair 1, o trace dela é gravado e exportado por inteiro; se cair 2 a 10, ele é descartado silenciosamente. A decisão é tomada **uma vez por trace** (na raiz) e **propagada** pra todos os serviços da cadeia — ou o trace inteiro é amostrado, ou nenhum pedaço dele é. É isso que evita "meio trace" espalhado pela frota.

### Lendo o waterfall

O resultado, no Jaeger ou no Zipkin, é uma visualização em **cascata (waterfall)**: cada span é uma **barra horizontal**, posicionada no tempo (eixo X) e indentada conforme a relação **pai/filho**. A largura da barra é a **duração** do span; o deslocamento mostra **quando** ele começou em relação ao trace inteiro.

Lendo de cima pra baixo você reconstrói a jornada da requisição: o span raiz (o gateway, digamos) é a barra mais larga no topo; abaixo dele, indentados, os spans dos serviços que ele chamou; abaixo desses, as chamadas a banco ou a outros serviços. **Gaps** entre barras (tempo em que nenhum span filho está ativo) denunciam latência "perdida"; uma barra anormalmente **larga** aponta o gargalo. É exatamente o "mapa de entrega da encomenda" da analogia — só que com régua de tempo.

## Na prática

Domínios neutros (`example.com`, portas convencionais). Primeiro, o **caminho OTLP** — as dependências (Maven). Note que é a fachada (`micrometer-tracing`) **mais um** bridge:

```xml
<!-- Fachada de instrumentação (neutra) -->
<dependency>
  <groupId>io.micrometer</groupId>
  <artifactId>micrometer-tracing</artifactId>
</dependency>

<!-- Bridge OTel: spans viram OpenTelemetry e saem via OTLP -->
<dependency>
  <groupId>io.micrometer</groupId>
  <artifactId>micrometer-tracing-bridge-otel</artifactId>
</dependency>

<!-- Exportador OTLP propriamente dito -->
<dependency>
  <groupId>io.opentelemetry</groupId>
  <artifactId>opentelemetry-exporter-otlp</artifactId>
</dependency>
```

Se em vez disso você fosse pelo **caminho Zipkin**, trocaria o bloco do meio por `micrometer-tracing-bridge-brave` + o reporter Zipkin — **nunca os dois bridges juntos**.

Configuração (`application.yml`) — endpoint OTLP e taxa de amostragem:

```yaml
management:
  tracing:
    sampling:
      # 1.0 = 100% APENAS em dev/local; em produção isso é decisão de operação (ver seam)
      probability: 1.0
  otlp:
    tracing:
      # Forma HISTÓRICA da chave (Spring Boot reorganizou esse namespace entre versões;
      # confira a doc da SUA versão). 4317 = porta OTLP/gRPC convencional.
      endpoint: http://otel-collector.example.com:4317
```

E como o **waterfall** aparece no visualizador (representação textual de um trace de três serviços):

```text
Trace 4bf92f3577b34da6...                                    total: 142ms
│
├─ GET /orders                 [api-gateway]        ▇▇▇▇▇▇▇▇▇▇▇▇▇▇  142ms
│   └─ GET /orders/{id}        [order-service]        ▇▇▇▇▇▇▇▇▇▇▇   118ms
│       ├─ SELECT orders       [order-service→db]       ▇▇          22ms
│       └─ GET /catalog/{sku}  [catalog-service]          ▇▇▇▇▇▇    71ms
│           └─ SELECT product  [catalog-service→db]         ▇▇      18ms

(indentação = relação pai/filho; largura da barra = duração;
 deslocamento horizontal = início no tempo)
```

> [!tip] Como interpretar este waterfall
> O `catalog-service` (71ms) é o trecho mais caro dentro dos 118ms do `order-service`, e a maior parte *dele* não é o banco (18ms) — sobra latência "no meio", candidata a investigação. É esse tipo de leitura que transforma tracing de "log bonito" em diagnóstico de gargalo.

## Armadilhas

### (1) Sampling a 100% em produção

`management.tracing.sampling.probability: 1.0` é o default mental de quem testou só em local — e é uma **armadilha de custo e volume** em produção. Amostrar 100% do tráfego significa que cada requisição gera spans que viajam pela rede e ocupam armazenamento no backend; numa frota de alto volume, isso vira gigabytes de telemetria, pressão sobre o coletor e conta cheia. O valor de produção é tipicamente **muito menor** (o próprio Spring Boot default é `0.1`), e a estratégia de *quanto* e *como* amostrar é decisão deliberada de operação — não um `1.0` esquecido no `application.yml`. Em dev, amostre tudo; em produção, amostre com intenção.

### (2) Confundir a instrumentação (Micrometer/OTel) com o backend (Jaeger/coletor)

É comum ouvir "vamos usar Jaeger pra tracing" como se Jaeger *fosse* o tracing. Não é. A **instrumentação** (Micrometer Tracing + bridge + SDK do OpenTelemetry) é o que **gera e exporta** os spans, dentro do seu app. O **backend** (Jaeger, Zipkin, o Collector) é o que **recebe, armazena e visualiza**. OpenTelemetry, aliás, **explicitamente não é** um backend. Confundir os papéis leva a erros de arquitetura — como achar que basta "subir um Jaeger" sem instrumentar o app, ou achar que trocar de backend exige reescrever a instrumentação (não exige, se você está na fachada neutra). Instrumentação produz; backend consome. São camadas distintas.

### (3) Dois bridges no classpath ao mesmo tempo

Colocar `micrometer-tracing-bridge-otel` **e** `micrometer-tracing-bridge-brave` no mesmo classpath é um erro silencioso e frustrante. Você acaba com **dois tracers concorrentes** tentando processar as mesmas observações, configuração ambígua e, no melhor caso, comportamento imprevisível de qual formato realmente sai. A regra é dura: **exatamente um bridge**. Isso costuma acontecer por herança transitiva (um starter puxa um bridge, você adiciona outro à mão) — então, ao migrar de Zipkin pra OTLP (ou vice-versa), **remova o bridge antigo** explicitamente, não apenas adicione o novo.

## Em entrevista

### Frase pronta (inglês)

> In Spring Boot, the instrumentation layer is Micrometer Tracing, which is a vendor-neutral facade — your code only ever creates `Observation`s, and it doesn't know where the spans go. What decides the wire format is the bridge: `micrometer-tracing-bridge-otel` sends spans over OTLP to the OpenTelemetry ecosystem, while `micrometer-tracing-bridge-brave` exports in the Zipkin format, and you pick exactly one. OpenTelemetry itself is the CNCF, vendor-neutral standard behind this — it defines the spec, the SDKs, the semantic conventions, and OTLP, which is the protocol the data travels on; crucially, OpenTelemetry is not a backend, it only generates and exports, so Jaeger or Zipkin do the storage and the waterfall visualization. On the config side I set the export endpoint and the sampling rate via `management.tracing.sampling.probability` — full sampling in dev, a much lower fraction in production, because tracing has a real cost in network and storage. Reading the result, I walk the waterfall: each span is a bar positioned in time and indented by parent-child, so the widest bar with no child activity underneath it is usually my bottleneck.

### Vocabulário

| Português | Inglês |
|---|---|
| ponte | bridge |
| neutro de fornecedor | vendor-neutral |
| amostragem | sampling |
| exportador | exporter |
| coletor | collector |
| cascata | waterfall |
| protocolo de wire | wire protocol |
| convenções semânticas | semantic conventions |

## Veja também

- [[03-Dominios/Java/Microservices e sistemas distribuídos/18 - Tracing distribuído I — correlação no código|Correlação no código]]
- [[03-Dominios/Java/Microservices e sistemas distribuídos/index|Microservices e sistemas distribuídos (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]

> [!warning] Seam com o Galho 17 — onde esta nota para
> Esta nota cobre **instrumentar e exportar** do ângulo do **código/config do app**: adicionar o bridge, apontar o endpoint, declarar a taxa de sampling. Tudo o que vem **depois da borda do app** é Galho 17: *operar* o **[[03-Dominios/Java/Cloud-native e produção/16 - OpenTelemetry Collector e sampling de produção|coletor]]** (OpenTelemetry Collector) e seus pipelines, montar e manter **[[03-Dominios/Java/Cloud-native e produção/15 - Dashboards e alertas — Grafana|dashboards]]**, **[[03-Dominios/Java/Cloud-native e produção/19 - Continuous profiling no cluster — Pyroscope e async-profiler|profiling contínuo]]**, e a **[[03-Dominios/Java/Cloud-native e produção/16 - OpenTelemetry Collector e sampling de produção|estratégia de sampling de produção]]** (head-based vs tail-based, adaptativo, budget de cardinalidade). Aqui você instrumenta e manda o dado pra fora; *governar* esse dado em produção é o outro galho.

> [!note] Galhos seguintes
> [[03-Dominios/Java/Cloud-native e produção/index|Observabilidade operacional (galho 17)]] já está pronta; segurança em sistemas distribuídos (galho 18) ainda está **(planejado)**.

## Referências

- OpenTelemetry — What is OpenTelemetry? (CNCF, vendor-neutral; spec, SDK, semantic conventions, OTLP, Collector): https://opentelemetry.io/docs/what-is-opentelemetry/
- Micrometer Tracing — referência (fachada `ObservationHandler`; bridges `micrometer-tracing-bridge-otel` e `micrometer-tracing-bridge-brave`): https://docs.micrometer.io/tracing/reference/index.html
- Spring Boot — Actuator Tracing (config de export e `management.tracing.sampling.probability`): https://docs.spring.io/spring-boot/reference/actuator/tracing.html
