---
title: "OpenTelemetry Collector e sampling de produção"
created: 2026-06-12
updated: 2026-06-12
type: concept
status: seedling
publish: true
fase: Adepto
tags:
  - java
  - cloud-native
  - adepto
  - observabilidade
  - opentelemetry
aliases:
  - "OpenTelemetry Collector"
  - "Sampling de produção"
  - "Tail-based sampling"
---

# OpenTelemetry Collector e sampling de produção

> [!abstract] TL;DR
> O **OTel Collector** é um serviço **separado do seu app**: ele *recebe*, *processa* e *exporta* telemetria através de um pipeline de **receivers → processors → exporters** (OTLP entrando e saindo). Ele existe para que cada aplicação não precise saber falar com cada backend de observabilidade — o app manda tudo pro Collector e o Collector decide o destino. Sobre **sampling**: **head-based** decide cedo, no SDK/app (por trace-id e porcentagem, antes de saber o que aconteceu); **tail-based** decide tarde, no Collector *stateful*, **depois do trace completo** — por isso consegue guardar os traces com erro ou lentidão, mas precisa bufferizar todos os spans até o trace fechar. Esta nota **recebe o seam do Galho 16**: lá você *instrumenta e exporta* o trace no código; aqui você *opera o coletor* e escolhe a *estratégia de sampling de produção*.

## O que é

O **OpenTelemetry Collector** é um componente de infraestrutura que fica **fora do processo da sua aplicação**. Diferente das bibliotecas de instrumentação (o OTel SDK, o Micrometer) que vivem *dentro* do app e *geram* o dado de telemetria, o Collector é um **serviço autônomo** que apenas *recebe*, *transforma* e *encaminha* esse dado.

A documentação oficial o descreve como uma forma *vendor-agnostic* de receber, processar e exportar telemetria. Ele introduz uma camada intermediária entre os seus serviços e os backends de observabilidade (Jaeger, Tempo, Prometheus, um SaaS qualquer). O app conversa **só com o Collector**, falando **OTLP** (OpenTelemetry Protocol); o Collector é quem conhece os destinos finais.

Internamente, o Collector é organizado em **pipelines**, cada um composto por três estágios:

- **Receivers** — pontos de entrada. Aceitam telemetria em vários formatos (OTLP, Jaeger, Prometheus, etc.).
- **Processors** — transformam o fluxo no meio do caminho (batching, retry, filtragem, e — relevante aqui — *tail sampling*).
- **Exporters** — pontos de saída. Mandam o dado já processado para um ou vários backends.

O Collector está na **linha 0.x atual** (seus componentes têm níveis de estabilidade mistos e a versão maior ainda não chegou a 1.0 para todos eles).

## Por que importa

Sem o Collector, você cairia no problema do **N×M**: cada um dos seus *N* serviços precisaria carregar a biblioteca de exportação de cada um dos *M* backends, e qualquer troca de backend obrigaria a recompilar e reimplantar **todos** os serviços. O Collector centraliza essa complexidade: o app só precisa saber exportar OTLP para um único endereço, e a decisão de *para onde* mandar vira configuração de infraestrutura.

Em produção, isso desacopla o ciclo de vida do código do ciclo de vida da observabilidade. Trocar de vendor, adicionar um segundo destino, aplicar retry e backpressure, ou mudar a estratégia de amostragem — tudo isso acontece no Collector, sem tocar no app.

E é exatamente no Collector que mora a estratégia de **sampling de produção** mais poderosa, o *tail-based*, que só é possível porque há um componente *stateful* fora do app capaz de ver o trace inteiro antes de decidir.

## Como funciona

### Collector: receivers, processors e exporters (e por que é separado do app)

O Collector funciona como um **encanamento configurável**. Você declara um ou mais *pipelines* e, em cada um, encaixa peças:

1. Um **receiver** abre uma porta e fica escutando telemetria. O receiver OTLP é o caso mais comum — é por ele que os seus apps entram.
2. Os dados atravessam uma cadeia de **processors**. Aqui acontece o `batch` (agrupar spans para enviar em lote), o `memory_limiter` (proteção contra estouro de memória) e processadores especializados como o `tail_sampling`.
3. No fim, um ou mais **exporters** despacham o resultado para os backends.

O ponto conceitual central: o Collector é **separado do app**. Ele não instrumenta nada, não gera span nenhum — ele **recebe e roteia**. Você pode reiniciá-lo, escalá-lo, trocar seus exporters sem nunca mexer no serviço que produz a telemetria.

### Instrumentação no app (G16) vs Collector (esta nota)

Esta é a fronteira que a presente nota guarda. São dois mundos distintos:

- **Instrumentação no app** — é onde o dado **nasce**. O OTel SDK ou o Micrometer, dentro do processo, criam os spans, propagam contexto e *exportam* via OTLP. Isso é assunto do **Galho 16** — veja [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/19 - Tracing distribuído II — exportando o trace|Tracing distribuído II (Galho 16)]], que cobre *gerar e mandar* o trace do código.
- **Collector** — é onde o dado **chega de fora**. Ele *recebe* o que o app exportou e *roteia* para os destinos. É infraestrutura de produção, não código de aplicação.

> [!info] Quem faz o quê
> O app **GERA e EXPORTA** (G16). O Collector **RECEBE e ROTEIA** (G17). Esta nota **recebe o seam do G16**: lá o foco é instrumentar/exportar no código; aqui o foco é operar o coletor e a estratégia de sampling de produção.

Não re-explicamos aqui como se instrumenta um trace — isso é o G16. Aqui assumimos que o trace já está sendo exportado e cuidamos do que acontece *depois que ele sai do app*.

### Head-based vs tail-based sampling

**Amostrar** (sampling) é decidir **quais traces guardar**. Em volume de produção, guardar 100% é caro demais; você fica com uma fração. A pergunta é *quando* e *onde* essa decisão é tomada.

- **Head-based sampling** — a decisão é tomada **cedo**, logo no início, normalmente no **SDK/app**. Olha apenas o **trace-id** e uma **porcentagem** (ex.: guardar 5% deterministicamente). É simples, barato e eficiente. A documentação nota que pode ocorrer em qualquer ponto do pipeline, mas a forma mais comum é probabilística no próprio app. O problema: como a decisão acontece *antes* de o trace terminar, você **não sabe ainda** se aquele trace teve erro ou lentidão — pode jogar fora justamente o trace interessante.

- **Tail-based sampling** — a decisão é tomada **tarde**, **no Collector**, **depois que o trace inteiro completou**. Isso permite estratégias ricas: *sempre guardar traces que contêm erro*, ou *guardar traces acima de um certo limiar de latência*. O custo é estrutural: o componente que faz tail sampling precisa ser **stateful** — ele tem que **bufferizar todos os spans** de cada trace até o trace fechar, para só então avaliar o conjunto e decidir. A doc oficial diz que esses componentes "precisam ser sistemas stateful capazes de aceitar e armazenar grande quantidade de dados", podendo exigir "dezenas ou centenas de nós de computação".

> [!example] Analogia Feynman — tail-based é decidir gravar depois do fim do jogo
> Head-based é como ligar a câmera no início de uma partida sem saber se o jogo vai ser bom — você decide gravar **antes** de qualquer coisa acontecer. Tail-based é assistir à partida inteira, ver que terminou em virada épica (ou em pênalti no último minuto), e **só então** decidir guardar a gravação. Para fazer isso você precisou **segurar** a partida toda na memória até o fim — esse é o preço do estado.

## Na prática

Configuração mínima de um Collector com pipeline de traces, incluindo o processor de tail sampling (domínio neutro):

```yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

processors:
  batch: {}
  tail_sampling:
    decision_wait: 10s        # quanto esperar pra considerar o trace "completo"
    policies:
      - name: erros
        type: status_code
        status_code: { status_codes: [ERROR] }   # sempre guarda traces com erro
      - name: lentos
        type: latency
        latency: { threshold_ms: 500 }            # guarda traces lentos
      - name: amostra-base
        type: probabilistic
        probabilistic: { sampling_percentage: 5 } # 5% do resto

exporters:
  otlp:
    endpoint: backend-de-traces:4317

service:
  pipelines:
    traces:
      receivers:  [otlp]
      processors: [tail_sampling, batch]
      exporters:  [otlp]
```

Onde cada decisão de sampling acontece:

```text
HEAD-BASED (cedo, no app)
  [App + OTel SDK]
     |  decide JÁ AQUI: trace-id % 5 == 0 ?  guarda 5%
     |  (não sabe ainda se vai dar erro)
     v
  [Collector] --> [Backend]

TAIL-BASED (tarde, no Collector)
  [App + OTel SDK]
     |  exporta TODOS os spans (sem decidir)
     v
  [Collector  (stateful, bufferiza o trace inteiro)]
     |  espera o trace COMPLETAR
     |  trace teve erro?      -> guarda
     |  trace foi lento?      -> guarda
     |  caso contrário        -> guarda 5% e descarta o resto
     v
  [Backend]
```

## Armadilhas

### (1) Querer tail-based sem o Collector — é impossível por construção

Tail-based sampling **exige** um componente *stateful* que veja o trace inteiro. Esse componente é o Collector (ou um agregador equivalente). Tentar fazer "tail sampling no app" não faz sentido: cada instância do app só enxerga seus próprios spans daquele trace, nunca o trace completo distribuído entre vários serviços. Sem o Collector centralizando os spans, não há onde avaliar o trace fechado. Se você quer "sempre guardar traces com erro", precisa do Collector — ponto final.

### (2) Head 100% em produção — explode custo e volume

É tentador deixar `sampling_percentage: 100` ("guarda tudo") para nunca perder um trace. Em produção real, isso significa exportar, transportar, processar e armazenar **todo** o tráfego de telemetria — custo de rede, de armazenamento e de processamento que cresce com o volume de requisições. Head-based existe justamente para reduzir esse volume na origem. Manter 100% costuma ser sustentável só em dev/staging; em produção, ou se reduz a porcentagem head-based, ou se troca a estratégia para tail-based (que guarda o que importa em vez de guardar tudo).

### (3) Rodar o Collector como sidecar sem entender o trade-off de estado

Subir um Collector *sidecar* (um por pod/instância do app) é comum e válido — mas perigoso se você pretende fazer **tail sampling** ali. Tail sampling precisa ver **todos os spans de um mesmo trace**, e num sistema distribuído esses spans podem nascer em instâncias diferentes, cada uma com seu sidecar. Um sidecar isolado só vê um pedaço do trace, então a decisão de tail sampling fica errada ou impossível. Para tail sampling, normalmente se usa uma **camada de Collector centralizada (gateway)**, com roteamento que garante que todos os spans de um trace caiam no mesmo nó stateful. Rodar sidecar "porque é mais simples" sem perceber esse trade-off de estado leva a traces incompletos e amostragem furada.

## Em entrevista

### Frase pronta (inglês)

> The OpenTelemetry Collector is a separate service from the application: it receives, processes, and exports telemetry through a pipeline of receivers, processors, and exporters, all over OTLP. This decouples each app from every backend — instead of every service knowing how to talk to every observability vendor, the app just sends OTLP to the Collector, and the Collector routes it. For production sampling, head-based sampling decides early in the SDK or app, looking only at the trace ID and a percentage, while tail-based sampling decides later, inside the stateful Collector, after the whole trace has completed — which is what lets you always keep traces that contain errors or high latency, at the cost of buffering every span until the trace closes.

### Vocabulário

| Português | Inglês |
| --- | --- |
| coletor | collector |
| receptor | receiver |
| processador | processor |
| exportador | exporter |
| amostragem na cabeça | head-based sampling |
| amostragem na cauda | tail-based sampling |
| pipeline de telemetria | telemetry pipeline |
| stateful (com estado) | stateful |

## Veja também

- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/13 - Observabilidade de operação — o panorama e os 3 seams|Observabilidade de operação]]
- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/17 - Logs estruturados em produção|Logs estruturados em produção]]
- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/19 - Tracing distribuído II — exportando o trace|Tracing distribuído II (Galho 16)]]
- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/index|Cloud-native e produção (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]

## Referências

- OpenTelemetry — *Collector* — https://opentelemetry.io/docs/collector/
- OpenTelemetry — *Sampling* — https://opentelemetry.io/docs/concepts/sampling/
