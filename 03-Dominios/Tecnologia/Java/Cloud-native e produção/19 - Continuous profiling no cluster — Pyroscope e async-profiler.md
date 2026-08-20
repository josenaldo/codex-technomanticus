---
title: "Continuous profiling no cluster — Pyroscope e async-profiler"
created: 2026-06-12
updated: 2026-06-12
type: concept
status: seedling
publish: true
fase: Magus
tags:
  - java
  - cloud-native
  - magus
  - profiling
aliases:
  - "Continuous profiling"
  - "Pyroscope"
  - "async-profiler"
---

# Continuous profiling no cluster — Pyroscope e async-profiler

> [!abstract] TL;DR
> **Continuous profiling** é o 4º sinal de observabilidade emergente: em vez de perfilar **uma** JVM **uma** vez (o JFR pontual do [[03-Dominios/Tecnologia/Java/JVM/13 - JFR e JMC — observabilidade de produção|Galho 3]]), você liga um agente leve em **toda a frota** e ele coleta perfis de CPU/alocação/lock **o tempo todo**, com baixo overhead, agregando tudo numa plataforma central. O **Grafana Pyroscope** (linha 2.x) é o sistema de agregação **multi-tenant** dessa categoria; para Java ele usa o **async-profiler** por baixo (saída em formato **JFR**). O ganho de verdade é a **correlação**: do span lento no trace você salta direto para o **flamegraph** daquele intervalo, fechando o ciclo métrica↔log↔trace↔perfil. A analogia: uma **caixa-preta sempre ligada**, gravando a frota inteira, pronta para o pós-mortem.

## O que é

**Continuous profiling** ("perfilamento contínuo") é a prática de coletar perfis de execução — onde a CPU está gastando ciclos, onde a memória está sendo alocada, onde threads bloqueiam em locks — de forma **permanente e distribuída**, e não como um evento manual de diagnóstico.

A diferença com o profiling clássico é de **modo**, não de técnica:

- **Profiling pontual/local** (o que você já viu no [[03-Dominios/Tecnologia/Java/JVM/13 - JFR e JMC — observabilidade de produção|JFR e JMC, Galho 3]]): você suspeita de um problema, abre o JMC, grava uma sessão JFR de N minutos numa instância específica, analisa o `.jfr` e fecha. É reativo, focado, e produz um artefato local.
- **Continuous profiling**: o agente fica **sempre coletando**, em **todas** as instâncias, e envia amostras compactadas para um backend que as **agrega por serviço, por versão, por janela de tempo**. É proativo e sistêmico — quando o incidente acontece, o perfil **já existe**.

O **Grafana Pyroscope** é o representante open source dessa categoria: a doc o descreve como "a multi-tenant, continuous profiling aggregation system" — um sistema de **agregação** de perfis, multi-inquilino, com arquitetura comparável aos outros componentes da stack Grafana (Loki para logs, Tempo para traces, Mimir para métricas).

> [!info] Pyroscope usa async-profiler para Java
> O SDK Java do Pyroscope não reinventa a coleta: ele usa o **async-profiler** por baixo e suporta o **formato JFR** justamente para carregar múltiplos tipos de evento (CPU, alocação, lock) num único fluxo. É o mesmo motor de baixo overhead que você usaria avulso — só que pilotado por um agente que faz upload contínuo.

## Por que importa

Para um sistema senior em produção, o gargalo raramente é "qual instância está lenta agora" — é **"o que mudou e onde está o custo"** ao longo do tempo e da frota inteira. Continuous profiling responde perguntas que o profiling pontual não alcança:

- **Regressão entre versões**: o flamegraph do deploy de hoje ficou 30% mais gordo num método específico? Você compara janelas de tempo (antes/depois do release) sem ter de reproduzir nada.
- **Custo agregado**: qual método consome mais CPU **somando todas as réplicas**? Otimizar 2% num hot path que roda em 200 pods é dinheiro real de cloud.
- **O incidente que já passou**: o pico de latência das 3h da manhã sumiu antes de você logar. Com perfil contínuo, o flamegraph daquela janela **ainda está lá**.

E o diferencial estratégico é tratá-lo como o **4º sinal** ao lado de métricas, logs e traces — todos correlacionáveis na mesma plataforma. É a peça que faltava para sair do "**o quê**" (métrica diz: latência subiu) e do "**onde no fluxo**" (trace diz: o span do serviço X está lento) e chegar no "**em qual linha de código**" (perfil diz: 60% do tempo desse span está em `parseEntity`).

Isso conecta direto com [[03-Dominios/Tecnologia/Java/Cloud-native e produção/18 - Profiling e diagnóstico sob carga — produção|diagnóstico sob carga]] (que trata da técnica de perfilar sob pressão) e com [[03-Dominios/Tecnologia/Java/Cloud-native e produção/13 - Observabilidade de operação — o panorama e os 3 seams|o panorama de observabilidade]] (que situa os sinais e os seams de instrumentação).

## Como funciona

### Continuous profiling: o que é e por que difere do pontual

A ideia central é **amostragem de baixo overhead, sempre ligada**. Em vez de instrumentar cada chamada (overhead alto, distorce o que mede), o profiler **amostra** a pilha de chamadas em intervalos curtos: a cada ~10ms ele pergunta "onde a CPU está agora?" e registra o stack. Estatisticamente, os caminhos que mais aparecem nas amostras são os que mais custam.

O que torna isso viável **em produção contínua**:

1. **Overhead baixo** — amostragem por sinal/perf events (o que o async-profiler faz) custa uma fração do que instrumentação completa custaria.
2. **Compressão e agregação no backend** — o agente envia amostras compactas; a agregação por símbolo/serviço/tempo acontece no Pyroscope, não na app.
3. **Multi-tenant** — um único backend serve vários times/serviços com isolamento, exatamente como Loki/Tempo/Mimir.

A distinção com o [[03-Dominios/Tecnologia/Java/JVM/13 - JFR e JMC — observabilidade de produção|JFR local do Galho 3]] precisa ficar nítida: **mesma família de técnica** (amostragem de stacks, saída JFR), **modos opostos de uso**. JFR/JMC = sessão local, manual, focada, artefato `.jfr` que você abre na sua máquina. Pyroscope = coleta contínua, automática, da frota, agregada numa plataforma central. Um é a lanterna que você acende quando entra no porão; o outro é a câmera de segurança que nunca desliga.

### Pyroscope + async-profiler: o agente Java

No mundo Java, o Pyroscope **delega a coleta ao async-profiler**. O SDK suporta o **formato JFR** para transportar múltiplos tipos de evento de uma vez. Os tipos principais:

- **CPU sampling** (amostragem de CPU): via eventos `itimer`, `cpu` ou `wall` — quem está gastando ciclos.
- **Allocation profiling** (perfil de alocação): por threshold configurável — quem está pressionando o heap.
- **Lock contention** (contenção de lock): por threshold configurável — quem está bloqueando em monitores.

O agente pode ser iniciado de dois jeitos: **programaticamente** (`PyroscopeAgent.start()` com um `Config.Builder`) ou por **variáveis de ambiente / `pyroscope.properties`** — o caminho idiomático em containers, onde você não quer recompilar para mudar config. Parâmetros típicos: nome da aplicação, evento de profiling, formato (JFR), endereço do servidor, intervalo de amostragem (default ~10ms) e intervalo de upload (default ~10s).

### Correlação profile ↔ métrica ↔ trace

O valor multiplicador é a **correlação**, não o flamegraph isolado. A doc do Pyroscope frisa a integração total com o Grafana, "allowing you to correlate with other observability signals, like metrics, logs, and traces".

O fluxo de ouro do diagnóstico fica assim:

1. **Métrica** dispara: P99 de latência do serviço de checkout subiu.
2. **Trace** localiza: o span do checkout passa 800ms num único trecho.
3. **Profile** explica: o flamegraph daquela janela mostra que 70% do tempo está numa serialização ingênua.

O salto técnico que torna isso possível é a **propagação de contexto**: amarrando IDs de span/trace às amostras de perfil, a plataforma consegue mostrar o **flamegraph daquele span específico** — não o perfil médio do serviço, mas o do request lento. É o que fecha de verdade o ciclo dos quatro sinais.

## Na prática

Configuração de agente Pyroscope por variáveis de ambiente (caminho idiomático em container, domínio neutro):

```yaml
# Trecho de Deployment Kubernetes — app Java com agente Pyroscope
apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-service
spec:
  template:
    spec:
      containers:
        - name: order-service
          image: registry.example.com/order-service:1.4.2
          # async-profiler precisa de perf events do kernel
          securityContext:
            capabilities:
              add: ["SYS_ADMIN"]   # ou ajuste perf_event_paranoid no host
          env:
            - name: JAVA_TOOL_OPTIONS
              value: "-javaagent:/opt/pyroscope/pyroscope.jar"
            - name: PYROSCOPE_APPLICATION_NAME
              value: "order-service"
            - name: PYROSCOPE_SERVER_ADDRESS
              value: "http://pyroscope.observability.svc:4040"
            - name: PYROSCOPE_FORMAT
              value: "jfr"           # transporta múltiplos eventos via JFR
            - name: PYROSCOPE_PROFILER_EVENT
              value: "itimer"        # CPU sampling
            - name: PYROSCOPE_PROFILER_ALLOC
              value: "512k"          # threshold de allocation profiling
            - name: PYROSCOPE_PROFILER_LOCK
              value: "10ms"          # threshold de lock contention
            - name: PYROSCOPE_UPLOAD_INTERVAL
              value: "10s"
            # labels para correlação por versão/ambiente
            - name: PYROSCOPE_LABELS
              value: "region=eu-west,version=1.4.2"
```

Leitura conceitual de um flamegraph (o eixo X é **tempo de CPU somado**, não ordem cronológica; a largura de cada caixa = fração das amostras naquele frame):

```text
Flamegraph — order-service, janela 03:00–03:15 (pico noturno)

[================ root (100%) ================]
[===== handleRequest (78%) =====][== background (22%) ==]
[== parseEntity (61%) ==][ persist ]
[ jsonDecode (54%) ]                  <- caixa larga = hot path
[ allocBuffer (40%) ]                 <- alocação dentro do decode
   ^
   |
   '-- 54% do tempo de CPU do serviço está em jsonDecode.
       Largura = custo. Profundidade = pilha de chamadas.
       Aqui mora a otimização (trocar o parser, reusar buffer).
```

A leitura: caixa **larga** = caminho **caro**; profundidade = pilha de chamadas. Você procura a caixa mais larga que **você controla** e ataca ali. Como o perfil é contínuo, dá para sobrepor a janela do pico com uma janela "normal" e ver exatamente qual caixa engordou.

## Armadilhas

### (1) Confundir continuous profiling com o JFR pontual do Galho 3

A técnica de coleta é parente — ambos amostram stacks e o Pyroscope até emite **JFR** —, mas o **modo de operação é o oposto**. Se você descreve Pyroscope como "JFR melhorado" numa conversa de arquitetura, perde o ponto: o diferencial não é a coleta, é a **agregação distribuída, contínua e multi-tenant** com **correlação** entre sinais. O JFR/JMC ([[03-Dominios/Tecnologia/Java/JVM/13 - JFR e JMC — observabilidade de produção|Galho 3]]) é a sessão local e manual de uma instância; o continuous profiling é a câmera sempre ligada da frota inteira. Saber dizer **qual usar quando** é o que separa o senior: JFR para um deep-dive cirúrgico numa instância; Pyroscope para regressões, custo agregado e o incidente que já passou.

### (2) Overhead de profiling agressivo em produção

"Baixo overhead" é uma **propriedade da configuração**, não uma garantia incondicional. Amostragem de CPU a ~10ms é barata; mas se você liga **allocation profiling com threshold muito baixo** (capturando cada alocação minúscula), ou wall-clock profiling em milhares de threads, o custo sobe e pode distorcer o que você está medindo (efeito observador). Em produção, prefira CPU sampling como padrão, suba o threshold de alocação/lock, e **valide o overhead** num ambiente de carga antes de ligar na frota toda. Profiling que muda o comportamento do sistema mede o profiler, não o sistema.

### (3) Profile sem correlação — o flamegraph órfão

Coletar perfis e parar aí entrega só metade do valor. Um flamegraph **isolado** (sem contexto de span/trace, sem labels de versão/ambiente) responde "onde a CPU vai **em média**" — útil, mas não te leva do **incidente** ao **código** num salto. Sem **propagação de contexto** (IDs de trace amarrados às amostras) e sem **labels** consistentes (serviço, versão, região), você não consegue dizer "o flamegraph **daquele span lento**" nem comparar "antes/depois do release". O perfil vira um número solto. O retorno do continuous profiling está justamente na **correlação** — projete os labels e a propagação desde o início, não como reflexão tardia.

## Em entrevista

### Frase pronta (inglês)

> Continuous profiling is the fourth observability signal: instead of capturing a one-off JFR session on a single instance, an agent like Grafana Pyroscope keeps sampling CPU, allocation and lock profiles across the **whole fleet**, with low overhead, and aggregates them in a multi-tenant backend. On the JVM it uses **async-profiler** under the hood and ships data in **JFR** format. The real payoff is correlation — I can jump straight from a slow span in a trace to the flamegraph for that exact time window, closing the loop between metrics, logs, traces and profiles. That's distinct from the local JFR/JMC workflow, which is a manual, focused deep-dive on one instance rather than always-on, fleet-wide aggregation.

### Vocabulário

| Português | Inglês |
| --- | --- |
| perfilamento contínuo | continuous profiling |
| gráfico de chama | flamegraph |
| multi-inquilino | multi-tenant |
| sobrecarga | overhead |
| frota | fleet |
| amostragem de CPU | CPU sampling |
| perfil de alocação | allocation profiling |
| contenção de lock | lock contention |
| propagação de contexto | context propagation |

## Veja também

- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/18 - Profiling e diagnóstico sob carga — produção|Profiling e diagnóstico sob carga]]
- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/13 - Observabilidade de operação — o panorama e os 3 seams|Observabilidade de operação]]
- [[03-Dominios/Tecnologia/Java/JVM/13 - JFR e JMC — observabilidade de produção|JFR e JMC (Galho 3)]]
- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/index|Cloud-native e produção (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]

## Referências

- Grafana Pyroscope — documentação oficial: https://grafana.com/docs/pyroscope/latest/ (sistema de agregação de continuous profiling, multi-tenant, correlação com métricas/logs/traces)
- Grafana Pyroscope — Java SDK: https://grafana.com/docs/pyroscope/latest/configure-client/language-sdks/java/ (usa async-profiler por baixo; formato JFR para múltiplos eventos; CPU/allocation/lock; config programática ou por env vars/properties)
- async-profiler — projeto upstream usado pelo SDK Java do Pyroscope: https://github.com/async-profiler/async-profiler
