---
title: "GC logs — unified logging e leitura"
created: 2026-06-05
updated: 2026-06-05
type: concept
progress: backlog
status: seedling
publish: true
fase: adepto
tags:
  - java
  - jvm
  - adepto
  - gc
  - diagnostico
aliases:
  - "GC logs"
  - "Unified logging"
  - "-Xlog"
---

# GC logs — unified logging e leitura

> [!abstract] TL;DR
> `-Xlog` (introduzido no Java 9, JEP 158) unificou todos os logs da JVM em um único framework — GC incluso. Habilitar o GC log tem custo desprezível e é a **caixa-preta do coletor**: sem ele, qualquer diagnóstico ou tuning é adivinhação. O que observar: **pausas** (percentis e pior caso, não média), **frequência** das coletas, **taxa de promoção** para a Old, **humongous allocations** e, acima de tudo, **Full GC** — que no G1/ZGC é sinal de problema, não comportamento normal.

## O que é

Antes do Java 9, cada subsistema da JVM tinha sua própria forma de logar: `-XX:+PrintGCDetails`, `-Xloggc:arquivo`, `-XX:+PrintGCDateStamps`, `-XX:+PrintGCApplicationStoppedTime` e dezenas de flags satélites formavam um zoológico incoerente. Os campos variavam por coletor, o formato era inconsistente e não havia como correlacionar eventos de GC com outros subsistemas da JVM.

O **JVM Unified Logging Framework** (JEP 158, Java 9) colapsou tudo isso em um único mecanismo: `-Xlog`. Todos os subsistemas — GC, classloading, compilação JIT, threads — passaram a usar a mesma infraestrutura com sintaxe uniforme, decoradores padronizados e saídas configuráveis.

O **GC log** é o produto mais importante desse framework para diagnóstico de produção. Ele registra cada coleta com suas fases, heap antes e depois, duração de pausa e metadados de contexto — tudo que é preciso para entender o que o coletor está fazendo e por quê.

## Por que importa

Sem GC log não há tuning honesto. A nota [[11 - Tuning de GC — metodologia e prática]] pressupõe que existe um log para analisar — tentar ajustar flags sem baseline de log é cargo cult.

Dois motivos práticos:

**Em produção:** incidentes de latência com frequência têm GC como causa ou agravante. Uma pausa de 2 segundos num G1 com heap apertado não aparece no APM como "GC" — aparece como request com latência de 2s, timeout, ou "lentidão inexplicável às 3h". O GC log é a evidência.

**Em entrevista:** saber ler um log do G1 ou do ZGC é hard skill de nível senior. Entrevistadores que trabalham com sistemas de alta performance pedem isso explicitamente — "qual o tail latency do seu GC?", "como você detectou o problema de to-space exhausted?" são perguntas que só têm resposta se o candidato já abriu um GC log de verdade.

O custo de habilitar é desprezível. A Oracle documenta o overhead como estatisticamente insignificante para cargas normais — a preocupação com "overhead do log de GC" é mito operacional. O custo real é o de **não ter o log** quando o incidente acontece.

## Como funciona

### A sintaxe do -Xlog

A sintaxe completa, conforme a documentação da Oracle para o Java 21:

```text
-Xlog[:<seletores>][:<output>][:<decoradores>][:<opções-de-output>]
```

Todos os componentes são opcionais e separados por `:`. Na prática:

```bash
-Xlog:gc*:file=gc.log:time,uptime,level,tags:filecount=5,filesize=20m
#      ^^^  ^^^^^^^^^^^  ^^^^^^^^^^^^^^^^^^^^ ^^^^^^^^^^^^^^^^^^^^^^^^
#    seletor   saída        decoradores            opções de rotação
```

**Seletores (tags + níveis):** combinam uma ou mais tags com um nível de detalhe.

```text
gc               # tag "gc", nível default (info)
gc=debug         # tag "gc", nível debug
gc*              # tag "gc" e quaisquer subtags (gc+heap, gc+phases...)
gc*=info         # todas as subtags de GC no nível info
gc+heap=trace    # interseção gc E heap, nível trace
```

Tags relevantes para GC:

| Tag | O que mostra |
|-----|-------------|
| `gc` | eventos de alto nível — início/fim de cada coleta |
| `gc+heap` | tamanho do heap antes/depois, humongous regions |
| `gc+phases` | fases internas de cada coleta (Minor, Major, Concurrent) |
| `gc+cpu` | tempo de CPU por categoria (User/Sys/Real) |
| `gc+ergo` | decisões ergonômicas do coletor (por que coletou, quanto) |
| `gc+remset` | remembered set (G1) |
| `gc*` | tudo acima + subtags menores — bom ponto de partida para diagnóstico |

Níveis em ordem crescente de detalhe: `off` → `error` → `warning` → `info` → `debug` → `trace`.

**Output:**

| Valor | Descrição |
|-------|-----------|
| `stdout` | saída padrão |
| `stderr` | saída de erro padrão |
| `file=<caminho>` | arquivo em disco |

**Decoradores** — campos que precedem cada linha de log:

| Decorador | Exemplo | O que mostra |
|-----------|---------|-------------|
| `time` | `2026-06-05T14:23:01.234+0000` | data/hora wall-clock |
| `uptime` | `12.345s` | tempo desde o início da JVM |
| `timemillis` | `1749130981234` | epoch em ms |
| `uptimemillis` | `12345` | uptime em ms |
| `level` | `info` | nível do log |
| `tags` | `[gc,heap]` | tags ativas da linha |
| `pid` | `1234` | PID do processo |
| `tid` | `5678` | ID da thread |
| `hostname` | `pod-abc123` | hostname — útil em containers |

**Opções de rotação de arquivo:**

| Opção | Significado |
|-------|-------------|
| `filecount=N` | mantém N arquivos rotacionados (0 = sem rotação) |
| `filesize=Xm` | rotaciona ao atingir X megabytes (k/m/g para unidade) |

### Anatomia de um log do G1

> [!note] Logs ilustrativos
> Os trechos abaixo são plausíveis e representativos do formato real do G1 com `-Xlog:gc*`, mas são ilustrativos — não extraídos de uma execução específica. O formato real pode variar ligeiramente entre versões do JDK.

**Pause Young (Normal)** — coleta young rotineira:

```text
[14.233s][info][gc] GC(42) Pause Young (Normal) (G1 Evacuation Pause) 512M->487M(2048M) 18.234ms
#         ^^^         ^^^   ^^^^^^^^^^^^^^^^^^^^  ^^^^^^^^^^^^^^^^^^^^^^ ^^^^^^^^^^^^^^^^^ ^^^^^^^^^
#       uptime      nível   tipo de pausa          motivo da coleta      heap antes→depois  duração
```

- `GC(42)` — sequência da coleta (facilita correlação com outras linhas do mesmo evento)
- `Pause Young (Normal)` — coleta da Young Generation, sem marcação concorrente
- `512M->487M(2048M)` — heap antes: 512M; heap depois: 487M; heap total: 2048M
- `18.234ms` — duração total da pausa STW

**Concurrent Start** — coleta Young que dispara o ciclo de marcação concorrente:

```text
[22.891s][info][gc] GC(67) Pause Young (Concurrent Start) (G1 Humongous Allocation) 1024M->998M(2048M) 24.107ms
[22.892s][info][gc] GC(68) Concurrent Mark Cycle
[23.105s][info][gc] GC(68) Concurrent Mark Cycle 213.445ms
```

- `Concurrent Start` — o G1 percebeu que precisa marcar a Old; inicia o ciclo concorrente
- Motivo entre parênteses pode ser `Humongous Allocation`, `G1 Evacuation Pause`, `Metadata GC Threshold` etc.
- O `Concurrent Mark Cycle` (GC 68) roda em paralelo com a aplicação — sem pausa adicional

**Mixed Collection** — após a marcação, o G1 evacua Young + parte da Old:

```text
[23.441s][info][gc] GC(71) Pause Young (Mixed) (G1 Evacuation Pause) 1536M->1024M(2048M) 45.321ms
```

- `Mixed` — Young + regiões selecionadas da Old sendo evacuadas
- Heap cai de forma mais expressiva que em coletas Young normais
- Bom sinal: o G1 está reclamando Old Generation antes de encher

**To-space exhausted** — sinal de alarme:

```text
[25.002s][info][gc] GC(79) Pause Young (Normal) (G1 Evacuation Pause) 1980M->1975M(2048M) 312.455ms
[25.002s][info][gc] GC(79) To-space exhausted
```

- O G1 tentou evacuar objetos mas não encontrou regiões livres suficientes para copiar
- A pausa fica anormalmente longa; o heap quase não encolhe
- Precursor imediato de Full GC se a situação continuar

**Full GC** — coleta stop-the-world completa, o que o G1 existe para evitar:

```text
[25.344s][info][gc] GC(80) Pause Full (G1 Compaction Pause) 2044M->312M(2048M) 4211.003ms
```

- `Pause Full` — toda aplicação parada; compactação completa do heap
- Pausa na casa dos segundos (aqui 4,2s) — estoura qualquer SLA razoável
- Heap esvazia muito (de 2044M para 312M) porque coletou tudo
- Causa raiz: heap subdimensionado, taxa de promoção alta demais, excesso de humongous allocations

### Anatomia de um log do ZGC

> [!note] Logs ilustrativos
> Trechos representativos do ZGC generational (Java 21+). Formato real pode variar.

O ZGC generational (default a partir do Java 21) separa coletas em **Major** (heap todo) e **Minor** (young generation). As pausas STW são mínimas e de duração constante; as fases longas rodam concorrentemente:

```text
[5.002s][info][gc] GC(2) Minor Collection (Allocation Rate)
[5.003s][info][gc] GC(2) Y: Pause Mark Start 0.012ms
[5.104s][info][gc] GC(2) Y: Concurrent Mark 101.234ms
[5.105s][info][gc] GC(2) Y: Pause Mark End 0.009ms
[5.106s][info][gc] GC(2) Y: Concurrent Process Non-Strong References 0.987ms
[5.107s][info][gc] GC(2) Y: Pause Relocate Start 0.011ms
[5.189s][info][gc] GC(2) Y: Concurrent Relocate 81.443ms
[5.189s][info][gc] GC(2) Y: Young Generation 187.234ms 512M->128M(8192M)

[12.441s][info][gc] GC(7) Major Collection (Warmup)
[12.442s][info][gc] GC(7) O: Pause Mark Start 0.018ms
[12.751s][info][gc] GC(7) O: Concurrent Mark 308.912ms
[12.752s][info][gc] GC(7) O: Pause Mark End 0.014ms
[12.754s][info][gc] GC(7) O: Concurrent Process Non-Strong References 1.102ms
[12.755s][info][gc] GC(7) O: Pause Relocate Start 0.021ms
[12.891s][info][gc] GC(7) O: Concurrent Relocate 135.678ms
[12.891s][info][gc] GC(7) O: Old Generation 446.891ms 4096M->1024M(8192M)
```

O que observar:

- **Prefixo `Y:`** — fase da young generation; **prefixo `O:`** — fase da old generation
- **`Minor Collection` / `Major Collection`** — tipo do ciclo; o motivo entre parênteses (`Allocation Rate`, `Warmup`, `Proactive`, etc.) indica o gatilho
- **Pause Mark Start / Pause Mark End / Pause Relocate Start** — as três pausas STW; todas sub-milissegundo em operação normal
- **Concurrent Mark / Concurrent Relocate** — fases longas, mas correm com a aplicação — sem pausa
- `4096M->1024M(8192M)` — heap antes, depois, total — aparece no resumo final do ciclo
- Pausas sub-ms constantes são o comportamento esperado; qualquer pausa na casa de dezenas de ms no ZGC é anômala e merece investigação

### O que olhar primeiro

Ao abrir um GC log, o roteiro inicial:

1. **Frequência das coletas Young** — coletas a cada poucos segundos indicam alocação agressiva; pode ser normal dependendo da carga, mas é o contexto.

2. **Duração das pausas** — não olhe a média. Olhe **p99 e pior caso**. Uma pausa de 1,2s que acontece uma vez por hora passa despercebida na média (que fica em 45ms) mas explode SLAs e timeout de health checks.

3. **Taxa de promoção** — observe o delta entre heap antes e depois das coletas Young. Se o heap não cai muito, muita coisa está sobrevivendo e sendo promovida para a Old. Old crescendo rápido → marcação concorrente mais frequente → Mixed collections → risco de Full GC.

4. **Humongous allocations** — procure `Humongous Allocation` como motivo de Concurrent Start e use `-Xlog:gc+heap=info` para ver `Humongous regions: X->Y`. Humongous frequente é sinal de alocações grandes (≥ metade do tamanho da região do G1) sendo feitas no caminho quente.

5. **Full GC e to-space exhausted** — `grep "Pause Full\|to-space exhausted"` no log. Qualquer ocorrência é red flag no G1 e ZGC. Merece investigação imediata — não normalizar.

### Da era antiga para cá

Antes do Java 9, as flags de GC log eram:

| Flag antiga | Equivalente em -Xlog |
|-------------|---------------------|
| `-Xloggc:<arquivo>` | `-Xlog:gc:file=<arquivo>` |
| `-XX:+PrintGCDetails` | `-Xlog:gc*` |
| `-XX:+PrintGCDateStamps` | decorador `time` no `-Xlog` |
| `-XX:+PrintGCApplicationStoppedTime` | `-Xlog:safepoint` |

> [!warning] Hedge
> A documentação do Java 21 tem uma seção "Convert GC Logging Flags to Xlog" que lista esses mapeamentos; os acima são os principais, mas consulte a doc oficial para a lista completa. O comportamento exato (alias vs. remoção) pode variar por flag e versão do JDK — confirme no `java -Xlog:help` ou nas release notes da sua versão.

Em JDKs modernos (9+), as flags antigas são tratadas como aliases para seus equivalentes `-Xlog` ou geram warning de deprecação — diferente do CMS, que faz a JVM não subir. Mas depender de flags legadas é dívida técnica: migre para `-Xlog` ao atualizar o JDK.

## Na prática

### Linha recomendada de produção

```bash
# Linha de produção — GC log completo com rotação
java \
  -Xlog:gc*:file=/var/log/app/gc.log:time,uptime,level,tags:filecount=5,filesize=20m \
  -jar app.jar
```

- `gc*` — captura gc + todas as subtags em nível info (suficiente para diagnóstico; suba para `gc*=debug` para investigação ativa)
- `file=/var/log/app/gc.log` — persiste em disco (não confie em stdout de container que pode rolar)
- `time,uptime,level,tags` — decoradores: timestamp absoluto para correlação, uptime para sequência, nível e tags para filtro
- `filecount=5,filesize=20m` — rotação automática: 5 arquivos de 20 MB = até 100 MB de histórico

> [!note] Confirmar sintaxe
> A sintaxe acima foi construída a partir da documentação oficial do Java 21 (`-Xlog` man page). Confirme com `java -Xlog:help` na sua versão de JDK — o comportamento de rotação (`filecount`/`filesize`) está confirmado na doc; o separador de unidade (`m` para megabytes) também.

Para investigação ativa de um problema, escale o detalhe:

```bash
# Investigação: mais detalhe de fases e ergonomia do G1
java \
  -Xlog:gc*=debug,gc+phases=debug,gc+heap=info,gc+cpu=info:file=gc-debug.log:time,uptime,level,tags:filecount=3,filesize=50m \
  -jar app.jar
```

### Trecho de log G1 anotado linha a linha

> [!note] Ilustrativo
> Trecho sintético representativo; campos e valores são plausíveis para G1 em Java 21.

```text
[0.003s][info][gc] Using G1
# A JVM confirma o coletor ativo — sempre procure esta linha primeiro

[8.421s][info][gc] GC(23) Pause Young (Normal) (G1 Evacuation Pause) 768M->702M(2048M) 22.341ms
# ^^^^^^  ^^^^ ^^  ^^^^^^  ^^^^^^^^^^^^^^^^^^^^^  ^^^^^^^^^^^^^^^^^^^^ ^^^^^^^^^^^^^^^^ ^^^^^^^^^
# uptime  nível tags sequência tipo de pausa       motivo              heap antes→depois  duração STW

[8.421s][info][gc,cpu] GC(23) User=0.18s Sys=0.00s Real=0.02s
# Breakdown de CPU: User = CPU total das threads de GC; Real = tempo real (parede)
# Real << User → GC usou múltiplas threads em paralelo (bom)
# Real ≈ User → GC rodou em single thread (suspeito em heap grande)

[14.992s][info][gc] GC(41) Pause Young (Concurrent Start) (G1 Humongous Allocation) 1536M->1509M(2048M) 31.045ms
# "Concurrent Start" = esta coleta Young dispara o ciclo de marcação concorrente
# Motivo: "Humongous Allocation" — alocação grande acelerou a decisão

[14.993s][info][gc] GC(42) Concurrent Mark Cycle
# Marcação concorrente iniciada — roda junto com a aplicação, sem pausa adicional

[15.267s][info][gc] GC(42) Concurrent Mark Cycle 274.002ms
# Ciclo concorrente concluído em 274ms (sem pausa para a aplicação)

[15.891s][info][gc] GC(44) Pause Young (Mixed) (G1 Evacuation Pause) 1509M->948M(2048M) 53.782ms
# "Mixed" = Young + subconjunto da Old sendo coletados
# Heap caiu 561M: o G1 está reclamando a Old de forma incremental

[18.334s][info][gc] GC(51) Pause Young (Normal) (G1 Evacuation Pause) 1987M->1984M(2048M) 287.441ms
[18.334s][info][gc] GC(51) To-space exhausted
# ALERTA: heap quase não encolheu (só 3M), pausa muito longa (287ms)
# O G1 não encontrou regiões livres para evacuar — evacuation failure
# Próximo ciclo provavelmente termina em Full GC

[18.891s][info][gc] GC(52) Pause Full (G1 Compaction Pause) 2044M->278M(2048M) 3847.221ms
# RED FLAG: Full GC — pausa de 3,8 segundos
# Heap esvaziou de 2044M para 278M (compactação completa)
# Causa raiz a investigar: heap muito pequeno, promoção alta, humongous excessivo
```

### Trecho com to-space exhausted — o que significa

`To-space exhausted` ocorre quando o G1 não encontra regiões livres suficientes para copiar objetos durante a evacuação. A coleta não consegue mover todos os objetos para o "to-space" (regiões destino) — alguns objetos permanecem no lugar, apenas com referências ajustadas. É um **evacuation failure**.

Consequências imediatas:
- Pausa muito mais longa que o esperado
- Heap mal compactado, fragmentado
- Old Generation com objetos que deveriam ter sido coletados
- Alta probabilidade de Full GC no próximo ciclo

Causas típicas: heap subdimensionado para a carga; taxa de promoção alta demais; excesso de humongous objects ocupando regiões; meta de pausa muito agressiva forçando coleções antes do heap ter espaço livre suficiente.

## Armadilhas

### (1) Rodar produção sem GC log

**O problema:** o argumento mais comum é "overhead". Na prática, o overhead do GC log com rotação de arquivo é estatisticamente negligenciável em cargas normais. O problema real é o oposto: sem GC log, quando um incidente de latência acontece às 3h da manhã — pausa longa, Full GC, to-space exhausted — não há evidência. O on-call passa horas adivinhando. O post-mortem fica especulativo. O tuning da semana seguinte é baseado em palpite.

```bash
# Sem evidência — o incidente de latência de 8 segundos ficou sem causa raiz:
java -Xmx4g -jar app.jar
# Logs da aplicação: "slow response detected (8234ms)" — nada mais

# Com evidência — diagnóstico imediato:
java -Xmx4g -Xlog:gc*:file=gc.log:time,uptime,level,tags:filecount=5,filesize=20m -jar app.jar
# GC log: Pause Full (G1 Compaction Pause) 3987M->312M(4096M) 8121.004ms
# Causa: Full GC. Próximo passo: investigar por que o G1 chegou a Full GC.
```

**Fix:** ative GC log em todos os ambientes — dev, staging e produção — com rotação configurada. O custo de disco (100 MB de histórico com `filecount=5,filesize=20m`) é trivial; o custo de não ter o log durante um incidente é alto.

---

### (2) Olhar pausa média e ignorar cauda e Full GC

**O problema:** "nossa média de pausa do GC é de 45ms — está ótimo". Enquanto isso, o p99.9 é 2,3 segundos porque acontece um Full GC a cada 4 horas. A média esconde completamente a cauda — e é exatamente na cauda que os SLAs estouram e os health checks falham.

```bash
# Análise ingênua — só olha a média:
grep "Pause Young" gc.log | awk -F'ms' '{print $1}' | awk '{sum+=$NF; n++} END{print "média:", sum/n "ms"}'
# resultado: "média: 43.2ms" — parece ótimo

# Análise honesta — procura o que dói:
grep -E "Pause Full|to-space exhausted|To-space" gc.log
# resultado: 3 ocorrências de "Pause Full" nas últimas 12h — problema real

# As 5 piores pausas (distribuição real, não média):
grep -oE '[0-9]+\.[0-9]+ms' gc.log | sort -n | tail -5
# observa a cauda — onde os SLAs estouram
```

**Fix:** ao analisar GC logs, sempre: (a) `grep "Pause Full\|to-space exhausted"` primeiro — qualquer hit é prioridade; (b) analise distribuição de pausas (sort + percentis), não só média; (c) observe frequência absoluta de coletas — muita coleta Young rápida pode ser tão problemático quanto pouca coleta lenta.

---

### (3) Usar -XX:+PrintGCDetails em JVM moderna sem entender o que acontece

**O problema:** receitas antigas, Dockerfiles herdados e documentações desatualizadas ainda usam `-XX:+PrintGCDetails`, `-Xloggc:gc.log` e `-XX:+PrintGCDateStamps`. Em JDKs modernos (9+) essas flags são mapeadas para equivalentes em `-Xlog` ou geram warning — o comportamento depende da versão e da flag específica. O log resultante pode ter formato diferente do esperado, campos faltando ou, pior, a flag simplesmente não ter efeito sem um aviso claro.

```bash
# Flag legada — comportamento imprevisível em JDK 17+:
java -XX:+PrintGCDetails -XX:+PrintGCDateStamps -Xloggc:gc.log -jar app.jar
# Em alguns JDKs: warning "Ignoring option PrintGCDetails; support was removed in 9.0"
# Em outros: mapeado silenciosamente; formato do log pode diferir do esperado
```

**Fix:** migre explicitamente para `-Xlog`. A tradução é direta (tabela na seção "Como funciona"), o formato é previsível e documentado, e você ganha controle fino sobre tags, decoradores e rotação. Ao atualizar o JDK de qualquer aplicação, audite as flags de GC no startup e substitua as legadas.

## Em entrevista

### Frase pronta (inglês)

> "Java 9 introduced the JVM Unified Logging Framework — JEP 158 — which replaced the zoo of PrintGCDetails, Xloggc, and related flags with a single -Xlog syntax. For production, I always enable GC logging with rotation: something like `-Xlog:gc*:file=gc.log:time,uptime,level,tags:filecount=5,filesize=20m`. The overhead is negligible, and without it any latency incident becomes guesswork."

> "When I read a G1 log, I start with two greps: one for 'Pause Full' and one for 'to-space exhausted'. Those are red flags — the G1 is designed to avoid Full GC, so if it's happening, something is wrong: heap too small, promotion rate too high, or too many humongous allocations. Only after ruling those out do I look at Young pause percentiles — not the mean, because the mean hides the tail. A p99 of 1.2 seconds caused by Full GC every few hours will look like a p50 of 40ms."

> "For ZGC, the read is different: the STW pauses should be sub-millisecond regardless of heap size, so if I see a Pause Mark Start taking 50ms something is wrong with the environment — GC threads starved of CPU, perhaps. The bulk of ZGC's work shows up as Concurrent Mark and Concurrent Relocate, which run alongside the application and don't block requests."

### Vocabulário

| Termo PT | Termo EN |
|----------|----------|
| log unificado da JVM | JVM unified logging |
| decorador de log | log decorator |
| seletor de tags | tag selector |
| pausa young normal | young normal pause |
| coleta mista | mixed collection |
| falha de evacuação | evacuation failure |
| to-space exaurido | to-space exhausted |
| objeto humongous | humongous object |
| latência de cauda | tail latency (p99 / p999) |
| coleta full de GC | full garbage collection |
| rotação de arquivo de log | log file rotation |
| marcação concorrente | concurrent marking |

## Veja também

- [[03 - Garbage Collection — o conceito]]
- [[06 - Os coletores do HotSpot]]
- [[09 - Flags, ergonomics e a JVM em containers]]
- [[11 - Tuning de GC — metodologia e prática]]
- [[12 - Diagnóstico — heap dumps, thread dumps e jcmd]]
- [[13 - JFR e JMC — observabilidade de produção]]
- [[03-Dominios/Java/JVM/index|JVM por dentro (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Dicionário de Java#unified logging (-Xlog)|unified logging (Dicionário)]]

## Referências

- [Enable Logging with the JVM Unified Logging Framework — java(1) man page, Java 21](https://docs.oracle.com/en/java/javase/21/docs/specs/man/java.html#enable-logging-with-the-jvm-unified-logging-framework) — fonte primária para sintaxe do `-Xlog`, tags, decoradores, opções de rotação
- [Garbage-First Garbage Collector Tuning — Oracle GC Tuning Guide, Java 21](https://docs.oracle.com/en/java/javase/21/gctuning/garbage-first-garbage-collector-tuning.html) — recomendações de `-Xlog:gc*=debug`, `gc+heap=info`, `gc+cpu=info`; descrição de evacuation failure e Full GC
- [Garbage-First (G1) Garbage Collector — Oracle GC Tuning Guide, Java 21](https://docs.oracle.com/en/java/javase/21/gctuning/garbage-first-g1-garbage-collector1.html) — arquitetura interna do G1, fases de coleta
- [The Z Garbage Collector — Oracle GC Tuning Guide, Java 21](https://docs.oracle.com/en/java/javase/21/gctuning/z-garbage-collector.html) — configuração e comportamento do ZGC
- JEP 158: Unified JVM Logging (Java 9) — introdução do framework; disponível em [openjdk.org/jeps/158](https://openjdk.org/jeps/158)
