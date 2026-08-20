---
title: "Tracing distribuído I — correlação no código"
created: 2026-06-12
updated: 2026-06-12
type: concept
status: seedling
publish: true
fase: Adepto
tags:
  - java
  - microservices
  - adepto
  - tracing
  - observability
aliases:
  - "Micrometer Tracing"
  - "Correlação distribuída"
  - "traceId spanId"
---

# Tracing distribuído I — correlação no código

> [!abstract] TL;DR
> Numa arquitetura de microsserviços, uma única request do usuário atravessa N serviços antes de virar resposta. Quando algo falha ou fica lento, você precisa saber **por onde a request passou** e **onde travou** — e um log solto por serviço não te conta essa história. O **tracing distribuído** costura tudo: cada request ganha um **traceId** (o fio da meada, igual no caminho inteiro) e cada salto ganha um **spanId** (um trecho do caminho). No mundo Spring/Java moderno, você instrumenta o código **uma vez** com a **Micrometer Observation API** ("instrument once") e ganha métricas, traces e logs do mesmo ponto. O motor de tracing é o **Micrometer Tracing**, que **substituiu o Spring Cloud Sleuth** (Sleuth foi pro `spring-attic`, está arquivado e **não roda em Boot 3.x**). A propagação entre serviços usa o padrão **W3C Trace Context** (headers HTTP), e o traceId/spanId entra no **MDC** pra aparecer em todo log. Esta nota é a **parte código**: instrumentar e correlacionar. **Exportar o trace** pra um coletor é a [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/19 - Tracing distribuído II — exportando o trace|nota 19]].

## O que é

**Tracing distribuído** é a técnica de seguir uma request de ponta a ponta enquanto ela cruza vários serviços. Pense numa encomenda dos correios: o **código de rastreamento** é único e te deixa ver a encomenda em cada centro de distribuição por onde ela passou. O **traceId** é exatamente esse código de rastreamento — nasce na borda do sistema (geralmente no gateway ou no primeiro serviço) e é o **mesmo** em todos os serviços que a request tocar. Já o **spanId** identifica **um trecho específico** do percurso: a passagem por um serviço, uma chamada HTTP de saída, uma query no banco. Um trace é, então, uma árvore de spans amarrados pelo mesmo traceId.

A peça que faz isso no ecossistema atual é a **Micrometer Observation API**, com sua bandeira de **"instrument once"**: você descreve uma operação como uma `Observation` **uma única vez** no código, e o framework deriva dela **três sinais** ao mesmo tempo — métricas (quanto tempo levou, quantas vezes rodou), traces (o span correspondente) e logs (eventos correlacionados). Antes da Observation API, você instrumentava métricas de um jeito e tracing de outro, duplicando esforço; a ideia central é unificar isso num ponto só.

O **Micrometer Tracing** é a extensão que transforma cada `Observation` num **span**. Ele é uma fachada (facade) sobre tracers populares — você programa contra a API neutra do Micrometer e por baixo um tracer concreto (Brave ou OpenTelemetry) faz o trabalho. Foi ele que **assumiu o lugar do Spring Cloud Sleuth**, que está descontinuado.

## Por que importa

Sem tracing, depurar uma falha distribuída vira arqueologia. O sintoma chega na borda — "o checkout está lento" — mas a causa pode estar três saltos adentro, num serviço que você nem lembrava que participava daquela request. Você abre o log de cada serviço, vê milhares de linhas intercaladas de **outras** requests simultâneas, e não tem como dizer **quais linhas pertencem à request que falhou**. É o problema da correlação: o sistema fala alto, mas em vozes que você não consegue separar.

O traceId resolve isso. Com ele injetado em cada linha de log de cada serviço, "depurar a request X" vira um `grep` por um único valor: você filtra pelo traceId e reconstrói a jornada inteira, na ordem, atravessando processos e máquinas. E como a Observation API entrega também métricas e o span, você consegue ver **onde** o tempo foi gasto — não só **que** foi lento.

Há ainda a razão histórica, que cai em entrevista: quem aprendeu Spring antes de 2022 conhece o **Sleuth**. Saber que ele foi para o `spring-attic`, está arquivado e **não funciona em Boot 3.x** — e que a substituição é Micrometer Tracing desde o **Boot 3.0** — é o tipo de detalhe que separa quem acompanhou a evolução de quem parou no tempo.

## Como funciona

### A Observation API e o "instrument once"

O ponto de partida é uma `ObservationRegistry`, o registro central que coordena todas as observações da aplicação. No Spring Boot 3.x ele já vem autoconfigurado — você o injeta e usa. Você descreve uma operação criando uma `Observation` com um nome e a executa dentro de um bloco. A partir desse **único** ponto de instrumentação, os *handlers* registrados derivam os sinais: um handler de métricas mede a duração, e o handler de tracing (vindo do Micrometer Tracing) abre e fecha o **span** correspondente.

O ganho do "instrument once" é não repetir a si mesmo. Você não escreve um cronômetro pra métrica e, ao lado, um `startSpan()/endSpan()` pra trace. Descreve a operação **uma vez** como observação; quem multiplica isso em métrica + trace + log é a infraestrutura. Boa parte do framework (controllers, `RestClient`, `@Scheduled`, etc.) já vem instrumentada com Observation, então o grosso do tracing acontece **sem você escrever nada** — você só instrumenta manualmente trechos de negócio que queira destacar.

### traceId, spanId e a propagação W3C entre serviços

Dentro de um processo, o tracer mantém o **span atual** (o contexto de trace ativo). O desafio do distribuído é **atravessar a fronteira do processo**: quando o serviço A chama o serviço B por HTTP, o contexto precisa viajar junto. É aí que entra a **propagação**.

O padrão default do Micrometer Tracing é o **W3C Trace Context**, um formato padronizado de carregar a identidade do trace em **headers HTTP**. O principal é o header `traceparent`, que codifica numa string o traceId (o mesmo no trace inteiro) e o spanId do chamador (o "pai" do próximo span). O serviço A **injeta** esse header na request de saída; o serviço B **extrai** o header na entrada, vê que já existe um trace em andamento, reusa o **mesmo traceId** e abre um **novo spanId** filho. Assim a árvore de spans se forma atravessando serviços, sem que ninguém combine nada manualmente — desde que ambos os lados falem W3C, o que é o default. (Brave também entende o formato legado `B3`; W3C é o padrão moderno e interoperável.)

> [!info] Por que "W3C" e não um formato proprietário?
> Porque trace cruza fronteiras de **tecnologia**, não só de processo. Seu serviço Java pode chamar um serviço Node ou Go; se todos falam o padrão W3C nos headers, o trace continua íntegro atravessando linguagens. Padrão aberto é o que torna o tracing **interoperável** entre stacks diferentes.

### MDC e a propagação de contexto entre threads

Saber o traceId no tracer é metade do problema; a outra metade é **fazê-lo aparecer no log**. A ponte é o **MDC** (Mapped Diagnostic Context) — um mapa de chave/valor que o framework de logging (Logback, Log4j2) anexa a cada linha. O Micrometer Tracing coloca `traceId` e `spanId` no MDC do span ativo, e você inclui esses campos no padrão de log. Resultado: **toda** linha de log já sai carimbada com o traceId, e a correlação fica de graça.

A armadilha mora num detalhe: tanto o span ativo quanto o MDC vivem em **`ThreadLocal`** — são amarrados à **thread** que está executando. No fluxo síncrono de uma request, isso funciona porque a mesma thread roda do começo ao fim. Mas no instante em que você **troca de thread** — submete um `Runnable` a um pool, usa `@Async`, encadeia um `CompletableFuture`, ou entra num fluxo reativo — a nova thread **não herda** o ThreadLocal da original. O contexto se perde: o span "evapora" e os logs daquela thread saem **sem traceId**, órfãos.

A solução é a **propagação de contexto** (*context propagation*): a biblioteca `context-propagation` do Micrometer captura o contexto na thread de origem e o restaura na thread de destino antes do trabalho rodar. Na prática, você instrumenta o executor (envolvendo-o com o suporte de propagação) ou, no mundo reativo, habilita o hook de propagação automática — e o traceId atravessa a troca de thread junto com a tarefa. É um daqueles pontos onde "funciona na minha máquina" engana: no caminho feliz síncrono tudo correlaciona; o buraco só aparece quando o código vira assíncrono.

## Na prática

Instrumentação manual de um trecho de negócio com a Observation API (o framework já instrumenta controllers e clients HTTP sozinho; aqui você destaca uma operação interna):

```java
import io.micrometer.observation.Observation;
import io.micrometer.observation.ObservationRegistry;
import org.springframework.stereotype.Service;

@Service
public class CalculadoraDePreco {

    private final ObservationRegistry registry;

    public CalculadoraDePreco(ObservationRegistry registry) {
        this.registry = registry;
    }

    public Preco calcular(Pedido pedido) {
        // "instrument once": esta única observação vira métrica + span + log
        return Observation.createNotStarted("preco.calcular", registry)
                .lowCardinalityKeyValue("tipo", pedido.tipo())  // vira tag/atributo
                .observe(() -> {
                    // dentro deste bloco existe um span ativo;
                    // chamadas a outros serviços herdam o traceId
                    return aplicarRegras(pedido);
                });
    }
}
```

Configuração mínima no `application.yml`. O `sampling.probability: 1.0` significa "rastrear 100% das requests" — ótimo em dev, mas em produção você reduz a amostragem (assunto da [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/19 - Tracing distribuído II — exportando o trace|nota 19]]):

```yaml
management:
  tracing:
    enabled: true
    sampling:
      probability: 1.0            # 100% em dev; reduzir em prod
    propagation:
      type: w3c                   # padrão default: W3C Trace Context
```

Padrão de log que carimba o traceId/spanId em cada linha (lendo do MDC). Uma linha correlacionada fica assim:

```text
2026-06-12 14:03:21.118  INFO [a1b2c3d4e5f60718,9f8e7d6c5b4a3210] CalculadoraDePreco : preço calculado para pedido 4471
                              └──── traceId ────┘└──── spanId ────┘
```

O primeiro valor entre colchetes é o **traceId** (idêntico em todos os serviços que essa request tocar); o segundo é o **spanId** deste trecho. Filtrar todos os logs de todos os serviços por `a1b2c3d4e5f60718` reconstrói a jornada inteira da request.

## Armadilhas

### (1) Log sem traceId = impossível correlacionar

O erro mais caro é instrumentar o tracing mas **esquecer de injetar o traceId no padrão de log**. O tracing fica funcionando "por dentro" — os spans existem —, mas seus logs continuam mudos: linhas soltas, sem o fio que as costura à request. Quando o incidente chega, você tem traces num lugar e logs noutro, sem ponte entre eles. O traceId **no MDC e no `logging.pattern`** é o que transforma log em algo correlacionável. Sem ele, você tem observabilidade pela metade.

### (2) Perder o contexto ao trocar de thread

O span ativo e o MDC vivem em **`ThreadLocal`**. No momento em que o código pula pra outra thread — pool de executores, `@Async`, `CompletableFuture`, fluxo reativo — a thread nova **não herda** esse contexto, e o traceId some dos logs dali pra frente. O trace fica truncado e as linhas viram órfãs. A correção é a **propagação de contexto** (`context-propagation` do Micrometer): capturar na origem e restaurar no destino, instrumentando o executor ou habilitando o hook reativo. É um bug silencioso: o caminho síncrono correlaciona perfeitamente, e o buraco só aparece quando alguém torna aquele trecho assíncrono.

### (3) Achar que ainda se usa Sleuth no Boot 3

O **Spring Cloud Sleuth está descontinuado**: foi movido para o `spring-attic`, está **arquivado** e seu último major suportou apenas **Boot 2.x** — ele **não roda em Boot 3.x**. Tentar adicionar a dependência do Sleuth num projeto Boot 3 leva a incompatibilidade e frustração. Desde o **Boot 3.0**, o motor de tracing é o **Micrometer Tracing**, e a instrumentação é via **Micrometer Observation API**. Tutoriais antigos que mandam adicionar `spring-cloud-starter-sleuth` estão desatualizados — esse é um ponto frequente de confusão pra quem migra de Boot 2 pra 3.

## Em entrevista

### Frase pronta (inglês)

> In a microservices architecture, a single request fans out across several services, so a per-service log line alone can't tell you where it went or where it broke. We solve this with distributed tracing: each request carries a **trace id** that stays the same across every hop, while each segment gets its own **span id**. In the modern Spring stack we instrument once with the **Micrometer Observation API** — a single observation yields metrics, traces, and logs — and **Micrometer Tracing** turns each observation into a span. It replaced **Spring Cloud Sleuth**, which was archived and doesn't run on Boot 3.x. Context propagates between services as **W3C Trace Context** headers, and we push the trace id into the **MDC** so every log line is correlated; we just have to remember to restore that context when work hops to another thread.

### Vocabulário

| Português | Inglês |
| --- | --- |
| rastreamento distribuído | distributed tracing |
| id de rastro | trace id |
| span (trecho do trace) | span |
| propagação de contexto | context propagation |
| correlação de logs | log correlation |
| instrumentar uma vez | instrument once |

## Veja também

- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/19 - Tracing distribuído II — exportando o trace|Exportando o trace]]
- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/04 - Panorama do Spring Cloud — e o que morreu|Panorama do Spring Cloud]]
- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/index|Microservices e sistemas distribuídos (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]

> [!note] Fronteira com o Galho 17
> Operar o **[[03-Dominios/Tecnologia/Java/Cloud-native e produção/16 - OpenTelemetry Collector e sampling de produção|coletor]]** e os **[[03-Dominios/Tecnologia/Java/Cloud-native e produção/15 - Dashboards e alertas — Grafana|dashboards]]** de produção (Tempo, Jaeger, Grafana, a parte de SRE/operação) é assunto do **Galho 17 — Observabilidade e operação**. Aqui, no Galho 16, o escopo é só a **correlação no código**: instrumentar com Observation, propagar o traceId e carimbá-lo nos logs.

## Referências

- [Micrometer Observation API — documentação oficial](https://docs.micrometer.io/micrometer/reference/observation.html) — o conceito "instrument once" e a `ObservationRegistry`.
- [Micrometer Tracing — documentação oficial](https://docs.micrometer.io/tracing/reference/index.html) — extensão de tracing sobre o `ObservationHandler`; bridges Brave e OpenTelemetry.
- [Spring Cloud Sleuth (spring-attic, arquivado)](https://github.com/spring-attic/spring-cloud-sleuth) — confirma a descontinuação: não funciona em Boot 3.x; core migrado para Micrometer Tracing.
