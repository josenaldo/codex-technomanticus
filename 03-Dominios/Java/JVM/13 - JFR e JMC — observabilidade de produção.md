---
title: "JFR e JMC — observabilidade de produção"
created: 2026-06-05
updated: 2026-06-05
type: concept
progress: backlog
status: seedling
publish: true
fase: magus
tags:
  - java
  - jvm
  - magus
  - jfr
  - diagnostico
aliases:
  - "JFR"
  - "Java Flight Recorder"
  - "JMC"
  - "Mission Control"
---

# JFR e JMC — observabilidade de produção

> [!abstract] TL;DR
> **JFR (Java Flight Recorder)** é um gravador de eventos embutido na JVM — GC, alocação, locks/monitor, I/O, CPU — que pode ficar ligado o tempo todo em produção porque seu overhead é baixo o suficiente para uso contínuo (o profile `default.jfc` tem impacto mínimo de performance, conforme a documentação oficial). **JMC (JDK Mission Control)** é a ferramenta de análise dos arquivos `.jfr`: projeto separado, download independente do JDK, interface visual com automated analysis, method profiling e visões de latência. A metáfora é a caixa-preta de avião: quando o incidente acontece — CPU explodindo, latência de lock oculta, alocação excessiva antes do GC — a gravação já existia. O forense reativo (nota 12: heap dump, thread dump) captura a foto depois do sinistro; o JFR grava o filme antes.

## O que é

**JFR (Java Flight Recorder)** é um subsistema de coleta de eventos embutido no HotSpot JVM, disponível no JDK desde o Java 11 como software open source (JEP 328, integrado ao OpenJDK). Não é um agente externo nem um profiler de attach: é parte da JVM, o que explica o overhead estruturalmente baixo.

O JFR registra eventos em buffers em memória, organizados em chunks escritos periodicamente em disco quando `disk=true`. Cada evento tem timestamp, duração (para eventos de duração) e campos de payload tipados. O resultado final é um arquivo `.jfr` — um formato binário eficiente que os analisadores leem sem precisar do processo original.

**JMC (JDK Mission Control)** é a ferramenta de análise desses arquivos. Desde o Java 11 também é open source (projeto Eclipse Mission Control), mas é **distribuído separadamente do JDK** — precisa de download independente (disponível em `jdk.java.net/jmc/` ou via empacotadores como Adoptium/Azul/Red Hat). A versão estável mais recente é a 9.x (2025). Não há JMC incluído no `jdk` ou `jre` instalado.

| Ferramenta | Papel | Onde vive |
|---|---|---|
| JFR | Coleta eventos na JVM em execução | Embutido no JDK (Java 11+) |
| JMC | Analisa arquivos `.jfr` offline | Download separado |
| `jcmd JFR.*` | Controla gravações ao vivo | Embutido no JDK |
| `-XX:StartFlightRecording` | Liga JFR no startup | Flag da JVM |

## Por que importa

O JFR é um dos recursos mais subutilizados do ecossistema Java. A maioria dos engenheiros só o descobre quando precisa — ou seja, quando o incidente já aconteceu e não havia gravação. O problema é que **o JFR resolve exatamente a classe de problemas que um dump pontual não pega**: o que aconteceu nos 30 minutos antes do spike de CPU? Qual lock estava gerando contenção durante o horário de pico de ontem à noite? Quais objetos eram alocados em excesso antes do GC full às 3h?

Heap dump e thread dump (nota 12) são forense reativo: capturam uma fotografia de um instante, e só depois do sintoma aparecer. JFR é always-on: a gravação existe antes do incidente, e pode ser extraída retroativamente com `jcmd JFR.dump`.

Do ponto de vista de carreira, saber configurar JFR para gravação contínua em produção e interpretar um `.jfr` no JMC é um marcador claro de senioridade real — especialmente em entrevistas focadas em sistemas de alta disponibilidade e diagnóstico de performance.

## Como funciona

### Arquitetura de eventos (categorias, buffers, por que o overhead é baixo)

O JFR organiza seus eventos em categorias funcionais:

- **GC** — coletas (tipo, duração, pausa, fases do G1/ZGC/Shenandoah), alocações que falharam no TLAB, referências
- **Alocação** — alocações amostradas — em novo TLAB e fora do TLAB (`jdk.ObjectAllocationInNewTLAB`, `jdk.ObjectAllocationOutsideTLAB`), live objects
- **Locks / monitor** — contenção em `synchronized` (`jdk.JavaMonitorWait`, `jdk.JavaMonitorEnter`), threads park/unpark
- **I/O** — leituras e escritas em socket e arquivo com duração acima de threshold configurável
- **CPU / método** — amostras de CPU com stack trace (method profiling), tempo de execução de métodos

O overhead é baixo porque o JFR **não intercepta cada operação em tempo real**: ele usa buffers locais por thread (thread-local buffers) que são escritos assincronamente, evita sincronização no caminho crítico, e coleta a maioria dos dados aproveitando pontos de instrumentação já existentes na JVM (GC hooks, safepoints). A documentação Oracle descreve o `default.jfc` como tendo "low overhead" com "minimal performance impact" — o suficiente para uso contínuo em produção. O profile `profile.jfc` coleta mais dados (stack traces mais frequentes, thresholds mais baixos) com overhead maior, indicado apenas para sessões curtas de diagnóstico.

> [!warning] Overhead — ausência de número oficial
> A documentação Oracle do Java 21 (`java` man page, Troubleshooting Guide, jcmd man page) **não publica um percentual específico** de overhead para o JFR com `default.jfc`. O que está documentado é a qualificação "low overhead" / "minimal performance impact" para uso contínuo. A cifra de "~1-2%" frequentemente citada em blogs e apresentações vem de benchmarks comunitários, não de uma garantia da especificação. Use o hedging correto: overhead baixo o suficiente para produção com `default.jfc`; meça no seu workload específico antes de assegurar um número.

### Ligando — `-XX:StartFlightRecording` e `jcmd JFR.*`

**Via flag de startup (gravação contínua — o padrão para produção):**

Opções confirmadas na `java` man page do Java 21:

```bash
java \
  -XX:StartFlightRecording=disk=true,maxage=12h,maxsize=512m,dumponexit=true,filename=/tmp/app-%p-%t.jfr,settings=default \
  -jar app.jar
```

| Opção | Default | Descrição |
|---|---|---|
| `disk` | `true` | Escreve dados em disco durante a gravação (necessário para ring buffer) |
| `maxage` | `0s` (ilimitado) | Tempo máximo de dados retidos em disco; `0s` = sem limite |
| `maxsize` | `0` (ilimitado) | Tamanho máximo em disco; `0` = sem limite |
| `dumponexit` | `false` | Salva o arquivo quando a JVM encerra |
| `filename` | auto-gerado | Caminho do arquivo; suporta `%p` (PID) e `%t` (timestamp) |
| `settings` | `default.jfc` | Profile: `default` (always-on) ou `profile` (diagnóstico curto) |
| `delay` | `0s` | Aguarda antes de iniciar a gravação |
| `duration` | `0s` (ilimitado) | Duração da gravação; `0s` = para sempre |
| `name` | auto-gerado | Nome da gravação (usado nos comandos `jcmd`) |
| `path-to-gc-roots` | `false` | Coleta caminho até raízes GC ao final (útil para leak, custoso) |

**Via `jcmd` ao vivo (confirmado na `jcmd` man page do Java 21):**

```bash
# Iniciar uma gravação nomeada
jcmd <pid> JFR.start name=prod-recording disk=true maxage=6h maxsize=256m settings=default

# Verificar gravações em andamento
jcmd <pid> JFR.check

# Extrair snapshot sem parar a gravação (the killer feature)
jcmd <pid> JFR.dump name=prod-recording filename=/tmp/incident.jfr

# Parar e salvar
jcmd <pid> JFR.stop name=prod-recording filename=/tmp/final.jfr
```

> [!tip] `JFR.dump` não interrompe a gravação
> Ao contrário do heap dump (que para o mundo enquanto percorre o heap), `JFR.dump` extrai os dados acumulados no ring buffer para um arquivo sem pausar a JVM e sem encerrar a gravação. É o equivalente a "tirar uma cópia da caixa-preta sem pousar o avião".

### Analisando no JMC

O JMC abre arquivos `.jfr` e oferece:

- **Automated Analysis** — relatório automático que destaca os problemas mais relevantes na gravação: GC pressure, thread contention, allocation hot spots, I/O lento. Ponto de entrada obrigatório antes de mergulhar nos dados brutos.
- **Method Profiling** — visão de flame graph / call tree dos stack traces amostrados. Mostra onde a CPU foi gasta. Permite filtrar por thread, por período, por pacote.
- **Allocation view** — mostra quais tipos de objetos foram alocados com maior frequência e quais stack traces originaram as alocações. Complementa o heap dump: o dump diz o que está na memória agora; o JFR diz o que foi alocado ao longo do tempo.
- **Lock / Monitor view** — threads que esperaram mais tempo por monitors, com stack trace de quem segurava o lock. Diagnóstico de contenção que nem heap dump nem thread dump isolados revelam bem.
- **I/O view** — operações de socket e arquivo com latência acima do threshold, agrupadas por host/endpoint.

### JFR Event Streaming — consumindo eventos em tempo real (JEP 349, Java 14)

Antes do Java 14, a única forma de consumir dados do JFR era abrir um arquivo `.jfr` offline. O JEP 349 (Java 14) introduziu o **JFR Event Streaming**: a capacidade de consumir eventos do JFR em tempo real, enquanto a JVM está rodando, via `RecordingStream` (pacote `jdk.jfr.consumer`).

```java
// hipotético: monitoring de CPU e GC em tempo real
// RecordingStream como campo de instância — mantido vivo enquanto o serviço roda;
// fechado no shutdown hook para liberar o stream com segurança.
import jdk.jfr.consumer.RecordingStream;
import java.time.Duration;

// Em código real: campo de instância, não try-with-resources local
// (try-with-resources fecha o stream ao sair do bloco, encerrando o consumo)
var rs = new RecordingStream();
rs.enable("jdk.CPULoad").withPeriod(Duration.ofSeconds(5));
rs.enable("jdk.GarbageCollection");
rs.onEvent("jdk.CPULoad", event -> {
    double jvmUser = event.getDouble("jvmUser");
    if (jvmUser > 0.80) {
        System.out.printf("ALERTA: CPU JVM em %.0f%%%n", jvmUser * 100);
    }
});
rs.onEvent("jdk.GarbageCollection", event -> {
    System.out.printf("GC %s — duração: %s%n",
        event.getString("cause"), event.getDuration("duration"));
});
rs.startAsync();   // processa em thread separada — a aplicação continua rodando

// fechar no shutdown da aplicação:
// Runtime.getRuntime().addShutdownHook(new Thread(rs::close));
```

`RecordingStream` implementa `AutoCloseable` e `EventStream`. Métodos principais:
- `onEvent(String nome, Consumer<RecordedEvent>)` — registra handler por nome de evento
- `startAsync()` — inicia o consumo em thread separada (a JVM não bloqueia)
- `start()` — inicia no thread corrente (bloqueia até o stream ser fechado)
- `enable(String nome).withPeriod(Duration)` — ativa evento periódico com intervalo
- `stop()` / `close()` — encerra o stream

Casos de uso: dashboards internos de saúde, alertas customizados sem agente externo, testes de integração que verificam alocações ou uso de socket.

### Custom events — instrumentando o domínio da aplicação

O JFR permite criar eventos de domínio próprio estendendo `jdk.jfr.Event`. O framework os trata exatamente como eventos nativos: aparecem no JMC, podem ser filtrados, têm timestamp e duração automáticos.

```java
// hipotético: evento de processamento de pedido
import jdk.jfr.Category;
import jdk.jfr.Description;
import jdk.jfr.Event;
import jdk.jfr.Label;
import jdk.jfr.Name;

@Name("com.example.OrderProcessed")
@Label("Order Processed")
@Description("Registra a conclusão do processamento de um pedido")
@Category({"Application", "Orders"})
public class OrderProcessedEvent extends Event {

    @Label("Order ID")
    public String orderId;

    @Label("Total Items")
    public int totalItems;

    @Label("Success")
    public boolean success;
}

// uso no código de produção:
var event = new OrderProcessedEvent();
event.begin();
try {
    // processamento real aqui
    event.orderId = order.getId();
    event.totalItems = order.getItems().size();
    event.success = true;
} finally {
    event.commit();   // grava o evento com duração calculada automaticamente
}
```

O `event.shouldCommit()` — verificar antes de coletar dados caros:

```java
var event = new OrderProcessedEvent();
event.begin();
// ... processamento ...
if (event.shouldCommit()) {
    event.orderId = collectExpensiveMetadata(); // só executa se o evento for gravado
    event.commit();
}
```

### Posicionamento — JFR vs profiler de attach vs APM

| Ferramenta | Escopo | Overhead | Use case principal |
|---|---|---|---|
| JFR (`default.jfc`) | Uma JVM, always-on | Baixo | Gravação contínua em produção |
| JFR (`profile.jfc`) | Uma JVM, sessão curta | Médio-alto | Diagnóstico de CPU/alocação pontual |
| Profiler de attach (async-profiler, YourKit) | Uma JVM, sessão curta | Variável | Flame graph detalhado, análise local |
| APM (Datadog, New Relic, Dynatrace) | Sistema distribuído | Baixo-médio | Rastreamento distribuído, negócio, alertas |

JFR e APM são **complementares, não substitutos**: o JFR enxerga o interior de uma única JVM com altíssimo detalhe; o APM enxerga o fluxo entre serviços, SLAs de negócio, e correlação de traces distribuídos. O JFR não tem context propagation entre serviços.

## Na prática

**Configuração de produção — ring buffer contínuo:**

```bash
java \
  -XX:StartFlightRecording=disk=true,maxage=12h,maxsize=512m,dumponexit=true,settings=default \
  -jar app.jar
```

Com essa configuração: os últimas 12 horas de dados são mantidos em disco (ring buffer — os dados mais antigos são descartados conforme o limite é atingido); no shutdown, o arquivo é salvo automaticamente.

**Dump sob demanda após incidente:**

```bash
# extrair os dados do ring buffer sem parar a gravação
jcmd <pid> JFR.dump filename=/tmp/incident-$(date +%Y%m%d-%H%M%S).jfr

# verificar o que está gravando
jcmd <pid> JFR.check verbose=true
```

**Custom event completo — `OrderProcessedEvent`:**

```java
// hipotético: evento de domínio para rastrear processamento de pedidos no JFR
import jdk.jfr.Category;
import jdk.jfr.Description;
import jdk.jfr.Event;
import jdk.jfr.Label;
import jdk.jfr.Name;

@Name("com.example.order.OrderProcessed")
@Label("Order Processed")
@Description("Duração e resultado do processamento de um pedido")
@Category({"Application", "Orders"})
public class OrderProcessedEvent extends Event {

    @Label("Order ID")
    public String orderId;

    @Label("Item Count")
    public int itemCount;

    @Label("Success")
    public boolean success;

    @Label("Failure Reason")
    public String failureReason;
}

// uso:
public void processOrder(Order order) {
    var event = new OrderProcessedEvent();
    event.begin();
    try {
        doProcess(order);
        event.success = true;
    } catch (Exception e) {
        event.success = false;
        event.failureReason = e.getClass().getSimpleName();
        throw e;
    } finally {
        event.orderId = order.getId();
        event.itemCount = order.getItems().size();
        event.commit();
    }
}
```

## Armadilhas

### (1) Confundir JFR (coleta) com JMC (análise) — e tentar instalar o JMC pelo JDK

**O problema:** JFR vem embutido no JDK 11+, sem necessidade de instalação adicional. JMC **não** faz parte do JDK — não existe `jmc` no `$JAVA_HOME/bin` de uma instalação padrão. Tentar usar JMC sem instalá-lo separadamente resulta em "command not found" ou na confusão de abrir arquivos `.jfr` sem ferramenta disponível.

```bash
# hipotético: erro comum — procurar jmc no JAVA_HOME
ls $JAVA_HOME/bin/jmc
# ls: /usr/lib/jvm/java-21-openjdk/bin/jmc: No such file or directory
```

**Fix:** baixar o JMC separadamente em `jdk.java.net/jmc/` (projeto Eclipse Mission Control) ou via empacotadores. No JDK só existem as ferramentas de **coleta** (`jcmd JFR.*`, `-XX:StartFlightRecording`); a **análise** requer o download à parte.

---

### (2) Gravar sem `maxage` nem `maxsize` — o disco enche silenciosamente

**O problema:** com `disk=true` e `maxage=0s,maxsize=0` (ambos os defaults), o JFR escreve dados em disco indefinidamente. Em aplicações de longa duração (dias, semanas), isso significa que o volume de gravação cresce até encher o disco disponível — o que pode causar falha de escrita de logs, falha de criação de heap dump, ou até queda da aplicação.

```bash
# hipotético: verificar o espaço após semanas sem configurar limites
du -sh /tmp/*.jfr
# 47G    /tmp/app-47-1234567890.jfr
```

**Fix:** sempre configurar pelo menos um dos dois limites. Para gravação contínua em produção, `maxage` é o mais intuitivo:

```bash
-XX:StartFlightRecording=disk=true,maxage=12h,maxsize=512m,settings=default
```

O JFR usa os dois limites simultaneamente: o dado é descartado quando excede `maxage` **ou** `maxsize`, o que ocorrer primeiro — comportamento de ring buffer.

---

### (3) Tratar JFR como substituto de APM ou tracing distribuído

**O problema:** JFR enxerga o interior de **uma única JVM**. Ele não tem nenhum conceito de trace distribuído, correlation ID entre serviços, ou visibilidade de latência de rede entre microsserviços. Usar JFR como ferramenta principal de observabilidade em arquitetura de microsserviços resulta em pontos cegos: a latência da chamada HTTP entre serviço A e serviço B não aparece no JFR do serviço A como um evento identificável — aparece apenas como tempo de I/O de socket.

**Fix:** JFR e APM são complementares. O APM (Datadog, New Relic, OpenTelemetry) cuida de tracing distribuído, SLAs de negócio, correlação entre serviços. O JFR cuida do detalhe interno da JVM: alocações, GC, contenção de lock, CPU por método. Em produção, use os dois.

---

### (4) Usar `settings=profile` como gravação contínua achando que é o default

**O problema:** o profile `profile.jfc` coleta stack traces com muito mais frequência, habilita eventos com thresholds mais baixos (I/O, locks), e pode ter overhead significativamente maior que o `default.jfc`. A documentação Oracle descreve o `profile.jfc` como indicado para "short periods" — não para uso contínuo. Confundir os dois e deixar `settings=profile` em produção pode degradar a performance da aplicação de forma perceptível.

```bash
# ERRADO para always-on — profile é para sessões curtas de diagnóstico
-XX:StartFlightRecording=disk=true,maxage=12h,settings=profile

# CORRETO para always-on
-XX:StartFlightRecording=disk=true,maxage=12h,maxsize=512m,settings=default
```

**Fix:** `default.jfc` para gravação contínua em produção. `profile.jfc` apenas para sessões curtas de diagnóstico de CPU ou alocação — e com `duration` limitado.

## Em entrevista

### Frase pronta (inglês)

> "My default for production services is running JFR in continuous mode — `disk=true`, `maxage=12h`, `maxsize=512m`, `settings=default`. The overhead with the default profile is low enough that Oracle documents it for continuous production use. When an incident happens — CPU spike, latency degradation, GC pressure — I dump the ring buffer with `jcmd JFR.dump` without stopping the recording, open the file in JMC, and let the Automated Analysis surface the top issues. From there I drill into Method Profiling for CPU, the Allocation view for memory pressure, and the Lock view for thread contention — all of which happened before the incident, not just at the moment I took the snapshot."

> "The key difference from reactive diagnostics is timing. A heap dump or thread dump tells you what the JVM looks like right now. JFR tells you what happened over the last 12 hours. If the OOM or the CPU spike is a symptom of something that built up over time — a growing allocation rate, increasing lock contention, a GC that started taking longer — the JFR recording has the evidence; the point-in-time snapshot doesn't."

> "JFR and APM are complementary, not alternatives. JFR gives deep visibility into a single JVM — object allocation, GC phases, monitor contention, method-level CPU usage. APM gives distributed tracing, cross-service latency, and business SLAs. In a microservices system you need both: JFR to understand what's happening inside each JVM, and your APM to understand what's happening between services."

### Vocabulário

| Termo PT | Termo EN |
|---|---|
| gravador de voo Java | Java Flight Recorder (JFR) |
| controle de missão JDK | JDK Mission Control (JMC) |
| análise automatizada | automated analysis |
| perfil / profile de coleta | recording profile / configuration (`default.jfc`, `profile.jfc`) |
| buffer circular / anel | ring buffer |
| extração sob demanda | on-demand dump (`JFR.dump`) |
| streaming de eventos | event streaming (`RecordingStream`) |
| evento de domínio customizado | custom domain event (`extends Event`) |
| contenção de monitor | monitor contention / lock contention |
| overhead de produção | production overhead |

## Veja também

- [[10 - GC logs — unified logging e leitura]]
- [[12 - Diagnóstico — heap dumps, thread dumps e jcmd]]
- [[14 - Performance da JVM — síntese]]
- [[03-Dominios/Java/JVM/index|JVM por dentro (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Dicionário de Java#JFR (Java Flight Recorder)|JFR (Dicionário)]]
- [[03-Dominios/Java/Dicionário de Java#JMC (JDK Mission Control)|JMC (Dicionário)]]

## Referências

- [JDK jcmd man page — Java 21 (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/specs/man/jcmd.html) — JFR.start (parâmetros `disk`, `maxage`, `maxsize`, `dumponexit`, `filename`, `name`, `settings`, `delay`, `duration`, `path-to-gc-roots`), JFR.dump, JFR.stop, JFR.check — todos os parâmetros confirmados nessa fonte
- [java man page — Java 21 (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/specs/man/java.html) — `-XX:StartFlightRecording` com subopções `disk`, `maxage`, `maxsize`, `dumponexit`, `filename`, `settings`, `delay`, `duration`, `name`, `path-to-gc-roots` — confirmadas; `default.jfc` descrito como "low overhead, minimal performance impact"; `profile.jfc` descrito como "more data, more overhead, short periods"
- [jdk.jfr package-summary — Java 21 Javadoc (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/jdk.jfr/jdk/jfr/package-summary.html) — classes confirmadas: `Event`, `FlightRecorder`, `Recording`, `RecordingState`, `EventFactory`, `Configuration`; anotações: `@Label`, `@Description`, `@Category`, `@Enabled`, `@StackTrace`, `@Threshold`, `@Period`; métodos `begin()`, `commit()`, `shouldCommit()`
- [RecordingStream — Java 21 Javadoc (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/jdk.jfr/jdk/jfr/consumer/RecordingStream.html) — confirmado "Since: 14" (Java 14); métodos `onEvent`, `startAsync`, `start`, `stop`, `close`, `enable`, `setMaxAge`, `dump`
- [Java Platform SE Troubleshooting Guide — Java 21 (Oracle)](https://docs.oracle.com/en/java/javase/21/troubleshoot/diagnostic-tools.html) — overhead descrito como "very small performance overhead, so it can be used in production environments"; "can record a large amount of data on production systems while keeping the overhead of the recording process low" — sem percentual específico publicado
- [Flight Recorder API Programmer's Guide — Java 21 (Oracle)](https://docs.oracle.com/en/java/javase/21/jfapi/) — guia oficial da API JFR
- [Eclipse Mission Control (Adoptium)](https://adoptium.net/jmc) — JMC como download separado; versão estável 9.1.2 (2025); disponível para Windows/macOS/Linux x86_64 e aarch64
- JEP 328 — *Flight Recorder* (Java 11) — JFR open source integrado ao OpenJDK; fonte: especificação oficial do JEP
- JEP 349 — *JFR Event Streaming* (Java 14) — `RecordingStream` para consumo de eventos em tempo real; fonte: especificação oficial do JEP
