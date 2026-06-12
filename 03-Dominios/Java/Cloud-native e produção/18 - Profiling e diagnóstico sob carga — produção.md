---
title: "Profiling e diagnóstico sob carga — produção"
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
  - profiling
aliases:
  - "Profiling em produção"
  - "Diagnóstico sob carga"
---

# Profiling e diagnóstico sob carga — produção

> [!abstract] TL;DR
> Profiling de produção não é uma ferramenta — é um **workflow de incidente**: do **sintoma** (CPU alta, latência, OOM), você escolhe o **sinal** certo (thread dump, GC log, heap dump, JFR) e a **ferramenta** que o captura. A mecânica de cada ferramenta é do [[03-Dominios/Java/JVM/index|Galho 3 (JVM)]] — aqui você **linka, não re-explica**. O valor sênior está em três coisas: capturar o sinal **sem derrubar o pod**, **correlacionar** esse sinal com métricas e traces do stack de observabilidade (notas 13-17), e saber que isso é **diferente de microbenchmark** ([[03-Dominios/Java/Testes/18 - Performance — JMH e microbenchmarks|JMH, Galho 13]]).

## O que é

**Profiling e diagnóstico sob carga** é a disciplina de capturar, ler e correlacionar sinais de runtime de uma JVM **enquanto ela atende tráfego real**, para explicar um comportamento anômalo (lentidão, consumo de recursos, travamento) e direcionar a correção.

A palavra-chave é **sob carga**. Um perfil tirado numa máquina ociosa, com dados sintéticos, responde uma pergunta diferente da que o incidente faz. Produção tem concorrência real, dados reais, latência de rede real, GC pressionado por alocação real. O sintoma só existe — e só se reproduz — nesse contexto. Por isso o profiling de produção é um **ato operacional**, não um experimento de laboratório.

> [!info] Fronteira com o Galho 3
> As **ferramentas** — heap dump, thread dump, `jcmd`, GC logs, JFR, JMC — e como **lê-las** são todas do [[03-Dominios/Java/JVM/index|Galho 3]]. Esta nota assume que você sabe operar cada uma. O que ela adiciona é o **ângulo de cluster**: quando disparar cada sinal, como capturá-lo num pod sem causar um segundo incidente, e como cruzá-lo com o resto da observabilidade.

## Por que importa

Em produção, ninguém te entrega um stack trace bonito. Você recebe um **sintoma vago** — "o checkout está lento", "o pod reinicia sozinho", "a CPU está em 90%" — e um relógio correndo. A diferença entre um dev pleno e um sênior é o **caminho mental** do sintoma até a causa:

- O pleno abre o profiler favorito e fica olhando gráficos esperando que algo salte aos olhos.
- O sênior parte do sintoma, **decide qual sinal vai falar mais alto** sobre aquele sintoma, captura **só esse sinal**, e o **correlaciona** com o que as métricas e os traces já estavam dizendo.

Esse caminho é o que esta nota cataloga. Ele é transferível: vale para qualquer JVM, em qualquer orquestrador, sob qualquer stack de observabilidade. A ferramenta muda; o workflow não.

## Como funciona

### O workflow de incidente: sintoma → sinal → ferramenta

O coração da nota. Você nunca começa pela ferramenta. Você começa pelo **sintoma**, deriva o **sinal** que melhor o explica, e só então escolhe a **ferramenta** que captura aquele sinal.

| Sintoma observado | Sinal que fala mais alto | Ferramenta (mecânica no G3) |
| --- | --- | --- |
| CPU alta, threads ocupadas | Onde a CPU está sendo gasta; quais threads estão RUNNABLE | JFR / async-profiler (perfil de CPU); thread dump |
| Latência alta, throughput caindo | Pausas de GC; threads bloqueadas/em I/O | GC log; thread dump (repetido) |
| Travamento / deadlock | Estado das threads, locks contidos | Thread dump (vários, em sequência) |
| Memória subindo, OOM iminente | Distribuição do heap, dominadores, vazamentos | Heap dump (com cuidado — ver Armadilhas) |
| Comportamento intermitente | Linha do tempo de eventos JVM (GC, alocação, locks, I/O) | JFR contínuo |

A leitura: **o sintoma seleciona o sinal**. "CPU alta" não pede heap dump — pede um perfil de CPU. "OOM" não pede thread dump — pede heap dump (e mesmo assim, com ressalva). Trocar o sinal pelo sintoma é o erro nº 1 do diagnóstico apressado.

> [!tip] Feynman
> Pense num médico no pronto-socorro. O paciente chega com "dor no peito" (sintoma). O médico não sai pedindo todos os exames do hospital. Ele decide: isso pede um **ECG** (sinal elétrico), não uma ressonância. O sintoma seleciona o exame. Profiling de produção é a mesma triagem: o sintoma seleciona o sinal, e o sinal seleciona a ferramenta.

### Os sinais e onde cada um mora (tudo no Galho 3)

Cada sinal tem uma nota dedicada no Galho 3 com a **mecânica completa** — como capturar, como ler, o que cada campo significa. Aqui você só vê o mapa de **quando** alcançar cada um:

- **Heap dump** — fotografia do heap inteiro, para caçar vazamentos e ver quem domina a memória. Captura e leitura: [[03-Dominios/Java/JVM/12 - Diagnóstico — heap dumps, thread dumps e jcmd|Diagnóstico — heap dumps, thread dumps e jcmd (Galho 3)]].
- **Thread dump** — estado de todas as threads num instante: o que pede deadlock, contenção de lock, threads presas em I/O. Mesma nota do G3: [[03-Dominios/Java/JVM/12 - Diagnóstico — heap dumps, thread dumps e jcmd|Diagnóstico — heap dumps, thread dumps e jcmd (Galho 3)]].
- **GC log** — a linha do tempo das pausas e da pressão de coletor; o primeiro lugar para olhar latência irregular. Leitura: [[03-Dominios/Java/JVM/10 - GC logs — unified logging e leitura|GC logs — unified logging e leitura (Galho 3)]]. Quando o GC **é** a causa e você precisa ajustar: [[03-Dominios/Java/JVM/11 - Tuning de GC — metodologia e prática|Tuning de GC — metodologia e prática (Galho 3)]].
- **JFR / JMC** — o gravador de voo contínuo da JVM: CPU, alocação, locks, I/O, eventos de GC, tudo numa timeline de baixo overhead. A ferramenta de eleição para perfilar **sob carga** sem parar a aplicação. Mecânica: [[03-Dominios/Java/JVM/13 - JFR e JMC — observabilidade de produção|JFR e JMC — observabilidade de produção (Galho 3)]].

> [!warning] Repetindo o limite desta nota
> Nenhum desses bullets explica **como** ler um heap dump ou interpretar um GC log. Isso é o Galho 3. Se você quer a mecânica, siga o link. Esta nota só decide **qual** sinal e **quando**.

### A correlação com o stack de observabilidade (notas 13-17)

Um sinal de JVM isolado é meia história. O salto sênior é **cruzar** o sinal com o que a observabilidade já registrava:

- A **métrica** (nota [[03-Dominios/Java/Cloud-native e produção/15 - Métricas — Micrometer e Prometheus|Métricas — Micrometer e Prometheus]]) te dá o **quando** e o **quanto**: o pico de latência começou às 14h03, a CPU subiu junto, o uso de heap fez serra. A métrica é o **gatilho** do diagnóstico.
- O **trace** (nota [[03-Dominios/Java/Cloud-native e produção/16 - Tracing distribuído — OpenTelemetry|Tracing distribuído — OpenTelemetry]]) te dá o **onde** no fluxo distribuído: qual span estourou, qual chamada downstream segurou a thread.
- O **log** (nota [[03-Dominios/Java/Cloud-native e produção/14 - Logging estruturado e correlação|Logging estruturado e correlação]]) te dá o **o quê** textual: a exceção, o ID de correlação que liga tudo.
- O **panorama** dos três seams está em [[03-Dominios/Java/Cloud-native e produção/13 - Observabilidade de operação — o panorama e os 3 seams|Observabilidade de operação — o panorama e os 3 seams]].

O profiling **completa** essa tríade: quando métrica + trace + log dizem "a thread X ficou presa", o **thread dump** mostra *em quê*; quando dizem "o heap cresceu sem voltar", o **heap dump** mostra *o quê* estava vazando. Profiling sem correlação é olhar um sinal solto no escuro; correlação sem profiling é saber *que* dói sem saber *onde*.

> [!info] Onde isso entra no Actuator
> Em apps Spring Boot, alguns sinais já têm porta de entrada via [Actuator](https://docs.spring.io/spring-boot/reference/actuator/index.html): o endpoint `threaddump` devolve o dump de threads, `heapdump` baixa o dump de heap, `metrics`/`prometheus` expõem as métricas que servem de gatilho, e `loggers` permite subir o nível de log em runtime durante o incidente. O Actuator é uma **fachada de captura** — a leitura do que ele te entrega continua sendo a mecânica do Galho 3.

## Na prática

A árvore de decisão que você carrega na cabeça quando o pager toca:

```text
INCIDENTE
│
├─ CPU alta (pod com CPU saturada, threads em RUNNABLE)
│   ├─ 1º: olhar métricas — pico desde quando? correlaciona com deploy/tráfego?
│   ├─ 2º: perfil de CPU sob carga → JFR (ou async-profiler) ── G3: JVM/13
│   └─ 3º: thread dump pra ver O QUE roda ───────────────────── G3: JVM/12
│
├─ Latência alta / throughput caindo (resposta lenta, p99 ruim)
│   ├─ 1º: trace — qual span estoura? downstream ou local? ──── nota 16
│   ├─ 2º: GC log — pausas explicam a serra de latência? ────── G3: JVM/10
│   ├─ 3º: thread dump x2 (intervalo) — threads presas em I/O? ─ G3: JVM/12
│   └─ se GC É a causa → tuning ────────────────────────────── G3: JVM/11
│
├─ OOM / memória subindo (heap cresce e não volta, pod reinicia)
│   ├─ 1º: métrica de heap — vazamento (sobe sempre) ou pico? ─ nota 15
│   ├─ 2º: heap dump — MAS NÃO no pod sob OOM (ver Armadilhas) ─ G3: JVM/12
│   └─ 3º: dominadores / suspeitos de vazamento no dump ─────── G3: JVM/12
│
└─ Travamento / deadlock (requests param, sem erro)
    └─ thread dumps em sequência → locks contidos, ciclo ────── G3: JVM/12
```

Disparar a captura de um sinal num pod, via `jcmd` (mecânica no Galho 3 — aqui só o gatilho):

```bash
# 1) Achar o PID da JVM dentro do container
jcmd -l

# 2) Thread dump — barato, seguro sob carga
jcmd <PID> Thread.print

# 3) Iniciar uma gravação JFR limitada no tempo (perfil sob carga)
#    Leitura do .jfr resultante: ver JFR e JMC (Galho 3)
jcmd <PID> JFR.start name=incident duration=120s filename=/tmp/incident.jfr

# 4) Heap dump — CARO. Pausa a JVM. Pesar antes (ver Armadilhas)
jcmd <PID> GC.heap_dump /tmp/heap.hprof
```

(Domínios e PIDs acima são genéricos — substitua pelo seu container. O **uso** de cada subcomando e a **interpretação** da saída estão nas notas do Galho 3.)

## Armadilhas

### (1) Tirar heap dump num pod já sob OOM e derrubá-lo de vez

Heap dump é a captura **mais cara** que existe: ela pausa a JVM (stop-the-world) e escreve um arquivo do tamanho do heap inteiro em disco. Num pod que já está raspando o limite de memória, o ato de dumpar pode estourar o limite, fazer o orquestrador matar o pod no meio da escrita, e te deixar com um dump **truncado e inútil** — além de causar um segundo incidente. Em produção: prefira `-XX:+HeapDumpOnOutOfMemoryError` (a JVM dumpa **antes** de morrer, automaticamente), garanta volume com espaço, e nunca dispare um heap dump manual num pod já agonizando. A mecânica está no Galho 3; o **julgamento de quando NÃO disparar** é o que esta nota cobra.

### (2) Confundir microbenchmark (JMH / Galho 13) com profiling de produção

São perguntas diferentes. **JMH** ([[03-Dominios/Java/Testes/18 - Performance — JMH e microbenchmarks|Performance — JMH e microbenchmarks, Galho 13]]) mede um **trecho de código isolado**, em ambiente controlado, com warmup e múltiplas iterações, para responder "este método é mais rápido que aquele?". **Profiling de produção** observa o **sistema inteiro sob tráfego real** para responder "por que ESTE incidente está acontecendo agora?". JMH não tem a concorrência, os dados e a latência de rede reais; profiling não tem o isolamento nem a repetibilidade de um benchmark. Otimizar com base num número de JMH que não se reproduz sob carga é otimizar o lugar errado. Use JMH para **escolher** um algoritmo; use profiling para **diagnosticar** um sintoma.

### (3) Perfilar sem correlacionar com métricas e traces

Abrir o JFR e ficar caçando gargalo no escuro é desperdício. O sinal de profiling só tem sentido **ancorado** no que a observabilidade já marcou: a janela de tempo do pico (métrica), o span que estourou (trace), o ID de correlação do request lento (log). Sem essa âncora, você não sabe nem **qual** janela do gravador de voo olhar, e corre o risco de "achar" um gargalo que não tem nada a ver com o incidente. Sempre comece pela métrica/trace que **gatilhou** o alerta, e use o profiling para **explicar** aquele ponto específico — não para vasculhar às cegas.

## Em entrevista

### Frase pronta (inglês)

> Production profiling, for me, is a workflow, not a tool. I start from the **symptom** — high CPU, latency, or an OOM — and let it pick the **signal**: a thread dump, a GC log, a heap dump, or a continuous JFR recording. The discipline is capturing that signal **under load without taking the pod down** — a manual heap dump on a pod that's already out of memory will just kill it and hand you a truncated dump. Then I **correlate** the signal with the metrics and traces we already collect, so the JVM-level evidence lines up with the request that actually failed. That's also why I keep it separate from JMH: a microbenchmark answers "is this code path faster?" in isolation, while profiling answers "why is *this* incident happening right now?" under real traffic.

### Vocabulário

| Português | Inglês | Nota de uso |
| --- | --- | --- |
| perfilamento | profiling | "production profiling", "CPU profiling" |
| despejo de heap | heap dump | "take/capture a heap dump"; caro, pausa a JVM |
| despejo de threads | thread dump | "grab a thread dump"; barato, seguro sob carga |
| sob carga | under load | "profile under load", "under real traffic" |
| gravador de voo | flight recorder | JFR = Java Flight Recorder; "a continuous JFR recording" |
| correlação | correlation | "correlate the signal with metrics and traces" |
| análise de causa raiz | root cause analysis | o objetivo do workflow; "drive RCA" |
| vazamento de memória | memory leak | o que o heap dump caça; "hunt down a leak" |

## Veja também

- [[03-Dominios/Java/Cloud-native e produção/19 - Continuous profiling no cluster — Pyroscope e async-profiler|Continuous profiling no cluster]]
- [[03-Dominios/Java/Cloud-native e produção/13 - Observabilidade de operação — o panorama e os 3 seams|Observabilidade de operação]]
- [[03-Dominios/Java/JVM/13 - JFR e JMC — observabilidade de produção|JFR e JMC (Galho 3)]]
- [[03-Dominios/Java/JVM/12 - Diagnóstico — heap dumps, thread dumps e jcmd|Diagnóstico (Galho 3)]]
- [[03-Dominios/Java/Testes/18 - Performance — JMH e microbenchmarks|JMH (Galho 13)]]
- [[03-Dominios/Java/Cloud-native e produção/index|Cloud-native e produção (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]

## Referências

- Spring Boot — Actuator (endpoints de diagnóstico: `heapdump`, `threaddump`, `metrics`, `prometheus`, `loggers`): https://docs.spring.io/spring-boot/reference/actuator/index.html
- A mecânica de cada ferramenta de diagnóstico (heap/thread dump, `jcmd`, GC logs, JFR/JMC, tuning de GC) vive nas notas 10-13 do Galho 3 (JVM) — ver os links em "Veja também".
- A correlação operacional (métricas, traces, logs) vive nas notas 13-17 deste galho (Cloud-native e produção).
