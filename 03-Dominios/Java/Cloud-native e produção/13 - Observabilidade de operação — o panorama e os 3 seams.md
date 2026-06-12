---
title: "Observabilidade de operação — o panorama e os 3 seams"
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
aliases:
  - "Observabilidade de operação"
  - "Os 3 pilares"
  - "Os 3 seams"
---

# Observabilidade de operação — o panorama e os 3 seams

> [!abstract] TL;DR
> **Observabilidade** é a capacidade de inferir o que acontece *dentro* de um sistema a partir do que ele *emite*. Ela se sustenta sobre **três pilares**: **métricas** (números agregados ao longo do tempo), **logs** (eventos discretos e datados) e **traces** (o caminho de uma requisição atravessando serviços).
> Esta nota é o **mapa** do galho. O assunto "observabilidade" cruza a trilha Java em **três costuras** (*seams*) distintas, e confundi-las é a fonte número um de retrabalho:
> - **G3 (JVM)** — olhar *para dentro da JVM* (JFR, JMC, heap, GC). Isso é diagnóstico de runtime, não de operação de cluster.
> - **G16 (Microservices)** — *correlacionar* um trace **no código** (Micrometer Tracing, propagar o `traceId`).
> - **G17 (este galho)** — **operar** o stack de observabilidade no cluster: Prometheus/Grafana, OTel Collector, sampling, logs estruturados.
> O **Spring Boot Actuator** é a **ponte** que liga seu app às ferramentas — ele *expõe* `/actuator/prometheus`, `/actuator/health`, `/actuator/metrics`. O *mecanismo* do Actuator é tema do **G8**; aqui ele é só a tomada na parede.
> Esta nota **emoldura**. As notas 14–18 detalham cada parte.

## O que é

Imagine que você administra um prédio que você não pode entrar. A única coisa que você tem são os instrumentos do lado de fora: um medidor de consumo de energia, um livro de registro do porteiro e uma câmera que segue uma pessoa do portão até a sala dela. Com esses três instrumentos, você consegue responder perguntas que nunca te contaram diretamente: "o prédio está mais cheio que ontem?", "o que aconteceu às 3h da manhã?", "por que a entrega do apartamento 502 demorou?".

Isso é **observabilidade**: a propriedade de um sistema que permite **inferir seu estado interno** a partir dos sinais que ele **emite para fora**. Não é sobre adicionar `System.out.println` quando algo quebra — é sobre o sistema *já emitir* sinais suficientes para que perguntas **novas** (que você não anteviu) possam ser respondidas *sem* mexer no código e fazer deploy de novo.

Os instrumentos do prédio são, exatamente, os **três pilares**:

- **Métricas** — o medidor de energia. Números agregados, baratos de armazenar, ótimos para tendências e alertas ("requisições por segundo", "uso de heap", "latência p99").
- **Logs** — o livro do porteiro. Eventos discretos, datados, ricos em detalhe ("usuário X falhou no login às 14:02 com erro Y").
- **Traces** — a câmera que segue a pessoa. O caminho completo de **uma** requisição, mostrando por quais serviços ela passou e quanto tempo gastou em cada um.

> [!info] Observabilidade ≠ monitoramento
> **Monitoramento** responde perguntas que você **já sabia** que ia fazer (dashboards e alertas pré-definidos). **Observabilidade** te permite fazer perguntas que você **ainda não sabe** que vai precisar fazer. Monitoramento é um *subconjunto* do que a observabilidade habilita.

## Por que importa

Em um monólito numa máquina só, "depurar" muitas vezes era *anexar um debugger* e olhar. Em produção distribuída — vários pods, autoescalando, efêmeros, atrás de um load balancer — **não existe "a máquina" para anexar**. O pod que processou a requisição que falhou pode já ter sido destruído. A única realidade que sobra é **o que o sistema emitiu** *enquanto* rodava.

Por isso a observabilidade deixou de ser "nice to have" e virou requisito de operação. Mas o assunto é **enorme**, e é aqui que a maioria das pessoas se perde: elas tratam "observabilidade" como **um tema só** quando, na trilha Java, ele aparece em **três lugares diferentes que resolvem problemas diferentes**. Estudar os três como se fossem um leva a re-explicar conceito, duplicar instrumentação e — pior — implementar no app coisas que a infraestrutura já faz de graça.

O valor desta nota não é te ensinar Prometheus. É te dar o **mapa** para você nunca confundir as três costuras.

## Como funciona

### Os 3 pilares: métricas, logs, traces

Os três pilares são **complementares**, não substitutos. Cada um responde a uma pergunta diferente, e a resposta completa quase sempre exige os três trabalhando juntos.

| Pilar | Pergunta que responde | Forma do dado | Custo de armazenar | Exemplo |
|---|---|---|---|---|
| **Métricas** | "Está acontecendo *quanto*? A tendência piorou?" | Números agregados em séries temporais | Baixo (agregado) | `http_requests_total`, `jvm_memory_used`, latência p99 |
| **Logs** | "O que *exatamente* aconteceu naquele instante?" | Eventos discretos e datados | Alto (cada evento) | "Pagamento recusado para pedido 9981, gateway timeout" |
| **Traces** | "*Onde* o tempo foi gasto nesta requisição?" | Grafo de spans de uma requisição | Médio/alto (com sampling) | requisição → API → serviço de pedidos → banco |

O fluxo típico de investigação atravessa os três: uma **métrica** dispara um alerta ("p99 subiu"); um **trace** mostra *qual serviço* da cadeia está lento; os **logs** *daquele span específico* explicam o *porquê*. Sem os três, você tem peças soltas.

> [!tip] O elo que costura os três: o `traceId`
> Quando um `traceId` aparece tanto no **trace** quanto nos **logs** de cada serviço, você consegue pular da câmera para o livro do porteiro instantaneamente. Fazer esse `traceId` existir e se propagar é, precisamente, o trabalho do **G16** — e é por isso que ele é uma costura separada.

### O seam de 3 pontas: G3 vs G16 vs G17

Esta é **a razão de ser** desta nota. A palavra "observabilidade" se decompõe em **três costuras** (*seams*) ao longo da trilha. São fronteiras de conhecimento, não sinônimos.

| Eixo | **G3 — JVM** | **G16 — Microservices** | **G17 — Cloud-native (este galho)** |
|---|---|---|---|
| **Pergunta central** | "O que a *JVM* está fazendo por dentro?" | "Como *correlaciono* uma requisição entre serviços?" | "Como *opero* o stack de observabilidade no cluster?" |
| **Unidade de observação** | Um processo JVM | Uma requisição distribuída | A frota inteira em produção |
| **Ferramentas** | JFR, JMC, heap dumps, GC logs | Micrometer Tracing, propagação de `traceId` | Prometheus, Grafana, OTel Collector, logs estruturados |
| **Onde mora** | *Dentro* do runtime | *No código* da aplicação | *Na infraestrutura* ao redor do app |
| **Nota canônica** | [[03-Dominios/Java/JVM/13 - JFR e JMC — observabilidade de produção\|JFR e JMC (G3)]] | [[03-Dominios/Java/Microservices e sistemas distribuídos/18 - Tracing distribuído I — correlação no código\|Tracing distribuído (G16)]] | notas 14–18 deste galho |

A regra de ouro para não embaralhar:

- **G3 olha para DENTRO da JVM.** Heap, garbage collector, threads, alocação. É diagnóstico de *runtime* de um processo. Esta nota **não re-explica** JFR/JMC — ela **linka** o G3.
- **G16 acontece NO CÓDIGO.** É a instrumentação que cria o span e propaga o `traceId` de um serviço para o próximo (via headers HTTP, por exemplo). Esta nota **não re-explica** correlação de trace — ela **linka** o G16.
- **G17 acontece NO CLUSTER.** É *operar*: configurar o Prometheus para raspar os endpoints, montar painéis no Grafana, rodar um OTel Collector para receber/processar/exportar telemetria, decidir a política de sampling, padronizar os logs em JSON. Isso é o que as **notas 14–18** detalham.

> [!warning] G18 NÃO é observabilidade
> O **Galho 18 é exclusivamente Certificação Java OCP**. Ele não tem nenhuma relação com observabilidade ou operação de produção. Se você está pensando em "produção", o galho é o **17**, nunca o 18.

### O Actuator como ponte (mecanismo é G8)

Como as ferramentas do G17 conseguem ler os sinais que o app produz? Por uma **tomada na parede**: o **Spring Boot Actuator**.

O Actuator é o componente do Spring Boot que **expõe endpoints de produção** — `/actuator/health`, `/actuator/metrics`, `/actuator/prometheus`, `/actuator/loggers`, entre outros. Ele é a **fronteira** entre o seu app e o mundo de ferramentas lá fora:

- O Prometheus (nota 14/15) **raspa** o endpoint `/actuator/prometheus`.
- O Kubernetes consulta `/actuator/health` para liveness/readiness probes.
- Por baixo, o Actuator delega ao **Micrometer**, que é o *facade vendor-neutral de métricas* — "Think SLF4J, but for observability", nas palavras da própria doc. Você instrumenta com uma interface neutra e escolhe o backend (Prometheus, etc.) como último passo.

Mas atenção à fronteira: **o *mecanismo* do Actuator — como os endpoints funcionam, como configurá-los, como expô-los com segurança — é tema do G8**. Esta nota **não re-explica** o Actuator; ela só o posiciona como *a ponte* app↔ferramentas. Para o mecanismo, **linka** o [[03-Dominios/Java/Spring Core e Boot/17 - Actuator e observabilidade\|Actuator (G8)]].

> [!info] A ponte é vendor-neutral por design
> Tanto o **Micrometer** (métricas) quanto o **OpenTelemetry** (os três sinais) são *facades vendor-neutral*: você instrumenta uma vez e decide o backend depois. O OTel Collector é, nas palavras da doc, "a vendor-agnostic way to receive, process and export telemetry data". Isso é o que permite trocar Grafana por outra coisa sem reescrever a aplicação — assunto da nota 16.

## Na prática

O diagrama abaixo mostra como as três costuras e os três pilares se encaixam. Domínios neutros, sem números inventados.

```text
                        ┌──────────────────────────────────────────────┐
                        │              APLICAÇÃO JAVA (pod)             │
                        │                                              │
   G3 (JVM) ───────────┤  [ JVM por dentro: JFR / JMC / heap / GC ]    │
   olha p/ DENTRO       │         ▲ diagnóstico de runtime             │
                        │         │                                    │
   G16 (Microservices)─┤  [ código instrumentado: cria span,          │
   correlação NO CÓDIGO │    propaga traceId p/ o próximo serviço ]    │
                        │         │                                    │
                        │   ┌─────┴───────────────────────────────┐    │
                        │   │  ACTUATOR  (a ponte — mecanismo G8) │    │
                        │   │  /prometheus  /health  /metrics     │    │
                        │   └─────┬───────────┬───────────┬───────┘    │
                        └─────────┼───────────┼───────────┼────────────┘
                                  │           │           │
              ╔═══════════════════╪═══════════╪═══════════╪══════════════════╗
              ║   G17 (ESTE GALHO): operar o stack NO CLUSTER                 ║
              ║                   │           │           │                  ║
              ║   MÉTRICAS    ◄───┘     TRACES│      LOGS │                  ║
              ║   Prometheus            OTel Collector    logs estruturados  ║
              ║   + Grafana             (recebe/processa/  (JSON, com        ║
              ║   (notas 14/15)          exporta; sampling) traceId embutido)║
              ║                          (nota 16)         (nota 17)         ║
              ╚══════════════════════════════════════════════════════════════╝

   Os 3 PILARES:  [MÉTRICAS] números agregados · [LOGS] eventos datados ·
                  [TRACES] caminho de UMA requisição
   O elo:         o mesmo traceId aparece no trace E nos logs → você pula entre eles
```

Leitura do diagrama, da esquerda para a direita do *seam*: o **G3** mergulha na JVM (runtime), o **G16** instrumenta o **código** (correlação), e o **G17** — onde você está — fica **do lado de fora**, no cluster, *operando* as ferramentas que consomem o que o Actuator expõe.

## Armadilhas

### (1) Instrumentar sem coletar — o dado que ninguém vê

A armadilha mais comum e mais frustrante: você adiciona métricas e traces lindos no código (`@Timed`, spans, contadores)... e **nada** os coleta. O endpoint `/actuator/prometheus` existe, mas **nenhum Prometheus o raspa**. O OTel SDK gera spans, mas **nenhum Collector os recebe**. O resultado é trabalho de instrumentação 100% invisível — pior que não ter, porque dá *falsa sensação* de observabilidade. Instrumentar (código) e coletar (cluster) são **as duas pontas** que precisam se encontrar; é por isso que a nota 14 em diante existe.

### (2) Re-fazer no app o que o coletor faz — ou confundir os 3 seams

Sintomas clássicos de costuras embaralhadas: tentar **agregar/amostrar métricas dentro da aplicação** (o **OTel Collector** já faz isso — nota 16); escrever **código de retry/batching de exportação** que o SDK e o Collector já oferecem; ou re-explicar/re-implementar **leitura de heap e GC** (isso é **G3**, runtime, não operação). A regra: se o problema é "olhar para dentro da JVM", é G3; se é "correlacionar requisição", é G16; se é "operar o pipeline no cluster", é G17. Misturar leva a duplicar esforço e a discussões intermináveis sobre "onde isso deveria estar".

### (3) Métricas sem cardinalidade controlada

Uma métrica em Prometheus é identificada pelo nome **mais o conjunto de labels (tags)**. Cada combinação distinta de labels vira uma **série temporal própria**. Colocar como label algo de **alta cardinalidade** — `userId`, `requestId`, `email`, `traceId` — faz o número de séries **explodir**, podendo derrubar o backend de métricas por consumo de memória. A confusão de fundo é *de seam*: identificadores únicos por requisição pertencem a **traces e logs** (G16/G17), **não a métricas**. Métricas são para o **agregado**; reserve labels para dimensões de **baixa cardinalidade** (status HTTP, nome do endpoint, região).

## Em entrevista

### Frase pronta (inglês)

> Observability rests on three pillars — metrics, logs, and traces — and they answer different questions: metrics tell you *how much* and surface trends, logs tell you *what exactly* happened at a point in time, and traces tell you *where* the time went across a distributed request. In the Java world this concern shows up as three distinct seams that I'm careful not to conflate: the JVM-internal view with JFR and JMC, the in-code trace correlation with Micrometer Tracing propagating a traceId, and the operational layer where I run Prometheus, Grafana, an OpenTelemetry Collector, and structured logging in the cluster. The bridge between the application and those tools is Spring Boot Actuator, which exposes endpoints like `/actuator/prometheus` and `/actuator/health`, backed by Micrometer as a vendor-neutral metrics facade — "think SLF4J, but for observability". A trap I always call out is uncontrolled metric cardinality: per-request identifiers belong in traces and logs, never as metric labels.

### Vocabulário

| Português | Inglês |
|---|---|
| observabilidade | observability |
| os três pilares | the three pillars |
| métrica | metric |
| traço | trace |
| costura | seam |
| ponte | bridge |
| coletor | collector |
| amostragem | sampling |
| cardinalidade | cardinality |
| log estruturado | structured logging |

## Veja também

- [[03-Dominios/Java/Cloud-native e produção/14 - Métricas em produção — Micrometer e Prometheus|Métricas em produção]]
- [[03-Dominios/Java/Cloud-native e produção/16 - OpenTelemetry Collector e sampling de produção|OpenTelemetry Collector e sampling]]
- [[03-Dominios/Java/Cloud-native e produção/18 - Profiling e diagnóstico sob carga — produção|Profiling e diagnóstico sob carga]]
- [[03-Dominios/Java/JVM/13 - JFR e JMC — observabilidade de produção|JFR e JMC (Galho 3)]]
- [[03-Dominios/Java/Microservices e sistemas distribuídos/18 - Tracing distribuído I — correlação no código|Tracing distribuído (Galho 16)]]
- [[03-Dominios/Java/Spring Core e Boot/17 - Actuator e observabilidade|Actuator (Galho 8)]]
- [[03-Dominios/Java/Cloud-native e produção/index|Cloud-native e produção (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]

## Referências

- Micrometer — *Reference Documentation* (vendor-neutral application observability facade; "Think SLF4J, but for observability"). https://docs.micrometer.io/micrometer/reference/
- OpenTelemetry — *Documentation* (traces, metrics e logs como sinais; OTel Collector como "vendor-agnostic way to receive, process and export telemetry data"). https://opentelemetry.io/docs/
- Spring Boot — *Production-ready Features (Actuator)* (endpoints `/actuator/health`, `/actuator/metrics`, `/actuator/prometheus`; Micrometer como projeto foundational). https://docs.spring.io/spring-boot/reference/actuator/index.html
