---
title: "Performance da JVM — síntese"
created: 2026-06-05
updated: 2026-06-05
type: concept
progress: backlog
status: seedling
publish: true
fase: Magus
tags:
  - java
  - jvm
  - magus
  - sintese
  - performance
aliases:
  - "Performance da JVM"
  - "Decision tree de GC"
  - "Troubleshooting JVM"
---

# Performance da JVM — síntese

> [!abstract] TL;DR
> Performance de JVM não é flag mágica — é **escolher o coletor para o perfil de carga**, **medir antes de mexer** e **saber em que fase do ciclo de vida o problema mora**: startup (classloading), warmup (JIT) ou peak (GC e alocação). Esta nota é a capstone do galho: consolida os critérios de decisão das 13 notas anteriores em uma árvore de escolha de coletor, um mapa do eixo temporal startup→warmup→peak (com CDS/AppCDS e o AOT do Project Leyden) e um checklist de troubleshooting que aponta de cada sintoma para a nota que o resolve. O fio condutor de tudo: **baseline antes, uma mudança por vez, medição depois** — sem isso, qualquer "tuning" é superstição.

## O que é

Esta é a nota de síntese do Galho 3 — JVM por dentro. As 13 notas anteriores construíram as peças: o pipeline de execução, o mapa de memória, o GC como conceito e como catálogo, o JIT, os módulos, as flags em containers, os logs, o tuning, o forense e a observabilidade contínua. Esta nota monta as peças num **modo de raciocinar de ponta a ponta**.

O raciocínio integrado tem três movimentos:

1. **Localizar o problema no tempo.** A JVM tem três regimes de performance distintos — startup, warmup e peak — e cada um tem causas, ferramentas e soluções próprias. Otimizar GC num problema de warmup é gastar esforço no regime errado.
2. **Localizar o problema no espaço.** O processo JVM é um mapa de áreas ([[02 - Áreas de memória de runtime]]) e de subsistemas (classloader, JIT, GC, code cache). Cada sintoma — OOM, latência, CPU — tem assinaturas diferentes conforme a área de origem.
3. **Decidir com evidência.** Toda decisão deste galho começa igual: capturar a evidência (GC log, JFR, dump), formar hipótese, mudar UMA coisa, medir de novo. A metodologia de [[11 - Tuning de GC — metodologia e prática]] não é só de GC — é o método do galho inteiro.

O que esta nota **não** faz: re-explicar os mecanismos. Para isso existem as notas — e o cheatsheet no fim desta página mapeia cada problema para a nota certa.

## Por que importa

**Entrevista de senior fecha com "como você decidiria".** As perguntas factuais ("qual o GC default?", "o que é deoptimization?") filtram pleno de senior; a pergunta que decide a vaga é integradora: *"sua API está com p99 estourado — me conta como você investiga"*. A resposta boa não lista flags: percorre um raciocínio — em que regime o problema acontece? que evidência eu capturo primeiro? o que distingue GC de contenção de warmup? Quem só tem fatos soltos trava nessa pergunta; quem tem o mapa atravessa.

**Produção cobra o raciocínio integrado, não fatos soltos.** O incidente real nunca chega rotulado: chega como "está lento" ou "o pod morreu". Saber que o ZGC tem pausas sub-ms não ajuda se você não consegue determinar se o problema sequer é GC. O valor do galho está em transformar "está lento" em uma pergunta respondível — e o caminho dessa transformação é exatamente a síntese desta nota.

**O custo de errar a fase é alto e silencioso.** Time gasta semanas tunando G1 num serviço cujo problema era warmup pós-deploy; outro adota native image para "performance" num serviço de longa duração cujo gargalo era alocação em loop quente. Ambos os erros nascem do mesmo lugar: tratar "performance de JVM" como um problema único, quando são pelo menos três problemas diferentes com soluções diferentes.

## Como funciona

### Decision tree de coletor

Consolidando [[06 - Os coletores do HotSpot]], [[10 - GC logs — unified logging e leitura]] e [[11 - Tuning de GC — metodologia e prática]] — as perguntas, na ordem em que valem a pena ser feitas:

```text
1. Existe requisito MEDIDO que o G1 default não atende?
   ├─ NÃO → G1 (default desde o Java 9). Fim. Não troque por palpite.
   └─ SIM → continue.

2. O requisito é LATÊNCIA (p99/p999 com orçamento apertado)
   ou o heap é muito grande (dezenas de GB a TB)?
   ├─ SIM → ZGC (pausas < 1ms, independentes do heap; generational
   │        por default desde o 23, modo único desde o 24).
   │        Pré-condições: CPU com folga para as fases concorrentes
   │        e heap com headroom — senão, allocation stalls.
   │        (Shenandoah é alternativa equivalente em builds
   │        OpenJDK não-Oracle: Temurin, Corretto, Red Hat.)
   └─ NÃO → continue.

3. O perfil é BATCH/ETL — ninguém espera resposta, a métrica
   é trabalho total por hora?
   ├─ SIM → Parallel. Pausas longas são irrelevantes; throughput
   │        máximo por core, sem pagar o overhead de controle
   │        de pausa do G1.
   └─ NÃO → continue.

4. Heap minúsculo (< ~100 MB), 1 vCPU, sidecar/CLI?
   ├─ SIM → Serial. Menor footprint e custo fixo; as estruturas
   │        auxiliares do G1 pesam proporcionalmente demais aqui.
   └─ NÃO → volte ao G1 e tune DENTRO do envelope dele (nota 11).

Em TODOS os ramos: validar com GC log sob carga real,
antes e depois — nos três eixos (latência, throughput, footprint).
```

O porquê de cada ramo, em uma linha:

- **G1 por default** porque é o meio-termo calibrado: pausas previsíveis (~target de 200ms), throughput bom, escala de GB a centenas de GB — e porque trocar sem requisito medido só adiciona variáveis.
- **ZGC quando latência manda** porque ele desloca o trabalho para fases concorrentes — e cobra em CPU e headroom de heap. Pagar esse preço sem SLA que o exija é desperdício (a armadilha 2 da nota 06).
- **Parallel quando throughput manda** porque o controle de pausa do G1 tem custo, e num batch ninguém está medindo pausa — só a hora em que o job termina.
- **Serial quando o footprint manda** porque em heap minúsculo o custo fixo dos coletores sofisticados domina.

A árvore decide o **ponto de partida** — nunca o veredito. O veredito vem do GC log.

Um lembrete de comparação justa, herdado da nota 06: cada coletor vence **na métrica para a qual foi desenhado**. "ZGC é melhor que G1" sem dizer a métrica é afirmação vazia — o G1 vence em throughput por core e footprint em heaps moderados; o ZGC vence quando o p99 ou o tamanho do heap estouram o envelope do G1. A pergunta correta nunca é "qual é o melhor?", e sim "melhor **para qual eixo, no meu workload, medido como**?".

### Startup vs warmup vs peak

O eixo temporal é a peça que falta em quase toda discussão de "performance de Java". O mesmo processo passa por três regimes, com gargalos e remédios diferentes:

| Regime | O que domina | Onde dói | Ferramentas/remédios |
|---|---|---|---|
| **Startup** | Classloading + linking ([[05 - Classloading e o delegation model]]), inicialização de frameworks | Serverless, scale-to-zero, CLIs, rolling deploys | CDS/AppCDS, AOT cache (Leyden), native image (radical) |
| **Warmup** | JIT subindo a escada interpretador → C1 → C2 ([[07 - JIT — C1, C2 e tiered compilation]]) | p99 dos primeiros minutos pós-deploy; autoscaling que cria pods frios sob pico | Readiness probe + aquecimento dirigido; AOT method profiling (JEP 515); load test que descarta o warmup |
| **Peak** | GC e taxa de alocação; contenção; code cache | SLA contínuo, conta de cloud | Escolha de coletor (acima), tuning com log ([[11 - Tuning de GC — metodologia e prática]]), JFR ([[13 - JFR e JMC — observabilidade de produção]]) |

**CDS e AppCDS — atacando o startup.** Class Data Sharing é um archive de classes **pré-processadas**: segundo a documentação da Oracle (Java 21), o archive é mapeado em memória quando a JVM sobe, "e como acessar o archive compartilhado é mais rápido do que carregar as classes, o tempo de startup é reduzido" — com o bônus de os metadados read-only serem compartilhados entre processos JVM na mesma máquina (menos footprint agregado). O JDK já embarca um archive default com classes core (em `lib/server/classes.jsa`); o **AppCDS** estende o mecanismo para classes **da aplicação** — incluindo as carregadas pelo system/platform classloader e até custom classloaders. A criação ficou simples nos JDKs modernos: um dynamic archive pode ser gerado automaticamente na saída do processo (`-XX:+AutoCreateSharedArchive -XX:SharedArchiveFile=app.jsa`) — primeira execução grava, as seguintes consomem.

**Project Leyden — startup E warmup via AOT.** A linha evolutiva do OpenJDK para "engarrafar" o trabalho de uma execução e reaproveitá-lo nas seguintes:

- **JEP 483 — Ahead-of-Time Class Loading & Linking (Java 24, entregue).** Classes da aplicação ficam disponíveis **já carregadas e linkadas** quando a JVM sobe, a partir de um **AOT cache** criado observando uma execução de treino. Funciona com aplicações existentes sem mudança de código; no Java 24 o fluxo tinha três passos (treino com `-XX:AOTMode=record`, criação do cache, execução com `-XX:AOTCache=app.aot`).
- **JEP 514 — AOT Command-Line Ergonomics (Java 25).** Colapsa treino+criação em um comando só: `-XX:AOTCacheOutput=app.aot` grava as observações e monta o cache no shutdown. O fluxo vira dois passos: treinar uma vez, fazer deploy com o cache.
- **JEP 515 — AOT Method Profiling (Java 25).** O cache passa a incluir **perfis de método** coletados no treino — em produção, o JIT começa a compilar os métodos quentes desde o boot, em vez de esperar acumular perfil próprio. É AOT atacando o **warmup**, não só o startup: encurta a escada do C2 sem abrir mão do modelo JIT.

(Hedge honesto: os números de ganho variam por workload e framework — trate qualquer percentual de melhora de startup como dependente do caso, não como propriedade da feature.)

Os comandos, lado a lado — o espectro em forma de shell:

```bash
# AppCDS dinâmico (JDKs modernos): a 1ª execução treina e grava,
# as seguintes consomem o archive automaticamente
java -XX:+AutoCreateSharedArchive -XX:SharedArchiveFile=app.jsa \
     -jar app.jar

# AOT cache — Java 24 (JEP 483): três passos
java -XX:AOTMode=record -XX:AOTConfiguration=app.aotconf -jar app.jar  # treino
java -XX:AOTMode=create -XX:AOTConfiguration=app.aotconf \
     -XX:AOTCache=app.aot -jar app.jar                                  # criação
java -XX:AOTCache=app.aot -jar app.jar                                  # produção

# AOT cache — Java 25 (JEP 514): dois passos
java -XX:AOTCacheOutput=app.aot -jar app.jar   # treino grava e monta no shutdown
java -XX:AOTCache=app.aot -jar app.jar         # produção
# (JEP 515: perfis de método entram no cache automaticamente no treino)
```

Duas regras de uso que evitam o cache trabalhar contra você: o **treino precisa ser representativo** — o cache acelera o que foi observado; treinar com um "hello world" e servir tráfego real desperdiça o mecanismo; e o cache é **acoplado ao ambiente** (versão de JDK, classpath) — recriá-lo faz parte do pipeline de build, não é artefato eterno.

**GraalVM native image — a alternativa radical.** Compilar tudo ahead-of-time para um binário nativo: startup de milissegundos, sem warmup — em troca de abrir mão do JIT especulativo (e do pico que ele entrega), com restrições ao dinamismo (reflection exige configuração). É um trade-off de arquitetura para cenários onde o startup domina tudo; tratamento completo fica para o [[03-Dominios/Tecnologia/Java/Cloud-native e produção/08 - GraalVM Native Image — conceito e trade-offs|Galho 17 (GraalVM Native Image)]].

A leitura senior do eixo: **CDS → AOT cache → native image é um espectro de quanto trabalho você move do runtime para antes dele** — e quanto de flexibilidade (e pico de JIT) você troca por isso.

### Checklist de troubleshooting

Do sintoma para a hipótese, e da hipótese para a nota:

| Sintoma | Primeira pergunta | Hipóteses e onde resolver |
|---|---|---|
| **OOM** | *Qual área?* (a mensagem do erro diz) | `Java heap space` → live-set vs leak: heap dump e dominators ([[02 - Áreas de memória de runtime]], [[12 - Diagnóstico — heap dumps, thread dumps e jcmd]]); `Metaspace` → classes vazando via classloader (02/05); pod morto com exit 137 → OOMKill do kernel, não é OOM da JVM ([[09 - Flags, ergonomics e a JVM em containers]]) |
| **Latência alta** | *Em que regime, e o GC log mostra pausa coincidindo?* | Pausas de GC batendo com o p99 → ler o log ([[10 - GC logs — unified logging e leitura]]) e tunar ou trocar coletor ([[11 - Tuning de GC — metodologia e prática]]); sem pausa de GC no horário → lock/contention: thread dump (12) + JFR de monitor (13), modelo de concorrência no [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Galho 4]]; só nos primeiros minutos → warmup ([[07 - JIT — C1, C2 e tiered compilation]]) |
| **CPU alta** | *Quem está queimando — GC, JIT ou a aplicação?* | Threads de GC concorrente (ZGC/G1 marcação) → dimensionamento de CPU/heap ([[06 - Os coletores do HotSpot]]); threads de compilação logo após deploy → warmup normal, passa (07); aplicação mesmo → method profiling com JFR ([[13 - JFR e JMC — observabilidade de produção]]) |
| **Lentidão que se instala e não regride** | *O code cache encheu?* | `CodeCache is full. Compiler has been disabled.` no log → métodos novos presos no interpretador para sempre (07) |
| **RSS cresce, heap não explica** | *Memória nativa?* | NMT e a anatomia do processo (02/12) |

A disciplina transversal: **a evidência vem antes da hipótese**. GC log e JFR ligados *antes* do incidente ([[13 - JFR e JMC — observabilidade de produção]]) transformam cada linha desta tabela de "reproduzir e torcer" em "abrir a gravação e ver".

### Virtual Threads e a JVM

As virtual threads mudam o perfil de pressão sobre a JVM sem mudar o modelo de performance: as stacks viram **continuations armazenadas no heap** (não mais stacks nativas de tamanho fixo), montadas e desmontadas sobre um pool pequeno de **carrier threads** — o que permite escalar workloads **I/O-bound** para milhões de tarefas concorrentes.

Para este galho, duas consequências:

- **O GC entra na conta da concorrência massiva**: stacks como objetos no heap significam que escalar tarefas concorrentes também escala pressão de alocação — mais um motivo para o GC log acompanhar a adoção.
- **"Uma thread por request" deixa de ser limite de capacidade** — o gargalo migra de threads nativas para os recursos reais (I/O downstream, heap, CPU).

O modelo completo — pinning, structured concurrency, quando NÃO usar — é assunto de [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/12 - Virtual Threads e Project Loom|Virtual Threads]], não desta nota.

## Na prática

Três cenários hipotéticos, cada um escolhendo a **postura completa** — coletor, observabilidade e plano de ciclo de vida — a partir dos critérios do galho.

### Cenário A — API latency-sensitive

```text
// hipotético: OrderService — API síncrona de pedidos, Java 21,
// SLA: p99 < 80ms ponta a ponta. Heap 24 GB, picos de 3.000 req/s.
// Baseline com G1: pausas mixed de 120-180ms batendo direto no p99.
```

A postura, decidida pela árvore:

- **Coletor: ZGC** — o orçamento de pausa dentro de um p99 de 80ms está abaixo do envelope do G1 nesse heap; o log da baseline comprova que a pausa É a causa (sem essa prova, a troca seria hype). Pré-condições verificadas antes: CPU com folga nos picos e headroom de heap — senão a latência volta como allocation stall.
- **Observabilidade: JFR always-on** desde o dia 1 (profile default, overhead mínimo) + GC log contínuo. Quando o incidente vier, o filme já existe.
- **Ciclo de vida: plano de warmup** — readiness probe que segura tráfego até os endpoints quentes terem sido exercitados por tráfego sintético; rollout gradual para nunca ter a frota inteira fria. O p99 do primeiro minuto pós-deploy também é p99.
- **Medição de aceite**: mesmas 24h de perfil de carga da baseline, comparando p99 da API, pausas no log, CPU e RSS — os três eixos.

### Cenário B — batch noturno

```text
// hipotético: CustomerReportJob — consolidação noturna, Java 21,
// processa ~80M de registros em janela de 4h. Ninguém espera resposta;
// a métrica é terminar dentro da janela com o menor custo de máquina.
```

A postura:

- **Coletor: Parallel** (`-XX:+UseParallelGC`) — pausas de centenas de ms são invisíveis para o negócio; o que importa é trabalho por hora de CPU, e nesse jogo o Parallel vence. Manter G1 aqui seria pagar overhead de controle de pausa que ninguém mede; ZGC seria pagar duas vezes.
- **Meta declarada em throughput**, não em pausa: % máximo do tempo total em GC (o eixo que o `GCTimeRatio` formaliza).
- **Observabilidade proporcional**: GC log ligado (custo desprezível) e JFR sob demanda se a janela começar a estourar — a primeira suspeita num batch que alarga é taxa de alocação, e o fix costuma ser código, não flag.

### Cenário C — serverless / scale-to-zero

```text
// hipotético: CustomerLookupFunction — função que escala a zero,
// invocações de 200-800ms, instâncias vivem segundos a poucos minutos.
// O gargalo NÃO é GC: é o custo de subir a JVM e nunca sair do C1.
```

A postura — aqui o eixo temporal manda, não a árvore de coletor:

- **Startup primeiro**: AppCDS como ganho barato e imediato (archive dinâmico gerado numa execução de treino); em Java 24+, **AOT cache do Leyden** (JEP 483; em Java 25, fluxo de dois passos via JEP 514 e perfis de método via JEP 515 — que ataca também o warmup que uma instância efêmera nunca completaria).
- **Coletor: irrelevante de tunar** — com heap pequeno e vida curta, o default (ou Serial, se o container tem 1 vCPU) resolve; qualquer minuto gasto em flag de GC aqui é minuto roubado do problema real.
- **Decisão de arquitetura no horizonte**: se mesmo com AOT cache o cold start dominar o SLA, a conversa muda de tuning para plataforma — native image ([[03-Dominios/Tecnologia/Java/Cloud-native e produção/21 - Native vs JVM — a decisão honesta|Galho 17 — native vs JVM]]), com seus próprios trade-offs.

Os três cenários usam o mesmo método e chegam a posturas opostas — é exatamente isso que "performance de JVM" significa: **não existe configuração boa, existe configuração boa para um perfil de carga medido**.

Duas observações de quem opera isso:

- **A postura é um pacote, não uma flag.** Note que nenhum cenário acima se resolve com uma decisão só: o coletor vem junto com a observabilidade, que vem junto com o plano de ciclo de vida. Quem responde "ZGC" para o cenário A acertou um terço da resposta — o JFR always-on e o plano de warmup são o que transforma a escolha em operação sustentável.
- **O cenário muda, o método não.** A baseline do cenário A é um GC log de 24h; a do C é uma medição de cold start. As evidências são diferentes, mas a sequência — medir, declarar meta, mudar uma coisa, medir de novo — é idêntica. É por isso que a metodologia da nota 11 é a nota mais transferível do galho: ela sobrevive a qualquer troca de coletor, de JDK e de plataforma.

## Armadilhas

As armadilhas desta nota são de **raciocínio** — os erros de modelo mental que sobrevivem mesmo sabendo todos os fatos das notas anteriores.

### (1) Otimizar sem medir

**O problema:** começar pela solução — "vamos trocar pro ZGC", "vamos aumentar o heap" — sem baseline. Toda decisão deste galho começa com evidência: GC log sob carga real, JFR, dump. Sem o "antes", o "depois" é ininterpretável: melhora vira coincidência não comprovada, piora vira mistério, e a flag entra para o `JAVA_OPTS` protegida pelo medo de remover. O cargo cult de produção nasce exatamente aqui.

**O raciocínio correto:** a primeira ação de qualquer trabalho de performance é capturar a baseline e declarar a meta numérica (percentil + unidade). Se a baseline já cumpre a meta, o trabalho acabou antes de começar — e esse é o desfecho mais comum e mais subestimado. Só então: uma mudança, mesma carga, comparação nos três eixos.

---

### (2) Escolher coletor por hype, não por SLA medido

**O problema:** "ZGC tem pausa sub-milissegundo" vira "ZGC em tudo". Mas pausa curta não é grátis — é trabalho deslocado para CPU concorrente mais headroom de heap. Num serviço com SLA folgado, a troca **piora** os dois eixos que ninguém olhou (throughput e footprint) para melhorar um que já estava bom. O simétrico também existe: manter G1 num batch por inércia, pagando controle de pausa que o workload não usa.

**O raciocínio correto:** coletor se escolhe de trás para frente — do **requisito medido** para a árvore de decisão, nunca da reputação para o requisito. A pergunta não é "qual o melhor GC?" (não existe); é "qual eixo do triângulo latência×throughput×footprint o meu SLA torna inegociável — e o log confirma que o coletor atual falha nele?".

---

### (3) Tratar a JVM como caixa preta até o incidente

**O problema:** observabilidade ligada só depois que o problema aparece. Aí o OOM morreu sem heap dump, o pico de latência passou sem gravação, e o diagnóstico vira arqueologia de métricas agregadas — ou pior, tentativa de reproduzir em staging o que só acontece em produção. A evidência mais valiosa é sempre a do momento do incidente, e ela não é capturável retroativamente.

**O raciocínio correto:** observabilidade se liga **antes**, como parte do deploy padrão: GC log contínuo (custo desprezível), JFR always-on (profile default, overhead mínimo), `-XX:+HeapDumpOnOutOfMemoryError` com path em volume persistente. O custo é quase zero; o retorno é transformar cada linha do checklist de troubleshooting de "adivinhar" em "abrir a gravação". Caixa-preta de avião se instala antes do voo.

---

### (4) Ignorar startup/warmup em workload elástico

**O problema:** medir e otimizar só o estado estacionário, num sistema cujo perfil real é elástico — autoscaling, rolling deploys frequentes, scale-to-zero. Cada pod novo nasce frio: classloading no startup, escada do JIT no warmup. Se o autoscaler cria pods justamente nos picos de tráfego, os requests do pico caem nos pods mais lentos da frota — e o p99 medido "em laboratório" nunca acontece em produção. O p99 do primeiro minuto também é p99.

**O raciocínio correto:** perguntar **quanto tempo da vida útil de uma instância é gasto fora do regime de pico**. Se a resposta for "quase nada" (monolito de uptime longo), startup/warmup são nota de rodapé. Se for "uma fração relevante" (elástico/efêmero), eles entram no orçamento de performance com prioridade — readiness com aquecimento, rollout gradual, CDS/AOT cache — e o load test passa a medir também o transitório, de propósito.

## Em entrevista

### Frase pronta (inglês)

> "I treat JVM performance as measurement-driven engineering across three regimes — startup, warmup, and peak — because each one has different bottlenecks and different tools. At peak, the conversation is collector choice and allocation rate: I keep G1 unless a measured requirement pushes me off it — ZGC when a tight latency SLA or a very large heap demands sub-millisecond pauses, Parallel when it's a batch job where only total throughput matters."

> "For startup and warmup, the levers are different: CDS and AppCDS map pre-processed class archives to cut class loading cost, and Project Leyden's AOT cache — class loading and linking in Java 24, with simpler ergonomics and AOT method profiling in Java 25 — lets the JVM reuse training-run work so the JIT starts compiling hot methods from boot. In elastic or scale-to-zero workloads that transient phase is a first-class part of the latency budget, not a footnote."

> "And the discipline that ties it together: baseline first, one change per iteration, re-measure on all three axes — latency, throughput, footprint. Observability gets turned on before the incident, not after: continuous GC logs, always-on JFR, and a heap dump on OOM configured from day one. Most of what looks like a GC problem turns out to be allocation in the code, a leak, or warmup — and the evidence is what tells them apart."

### Vocabulário

| Termo PT | Termo EN |
|----------|----------|
| engenharia orientada a medição | measurement-driven engineering |
| linha de base | baseline |
| regime transitório vs estacionário | transient vs steady state |
| partida a frio | cold start |
| aquecimento (da JVM) | (JVM) warmup |
| compartilhamento de dados de classe | class data sharing (CDS) |
| cache AOT (carga e linking antecipados) | AOT cache (ahead-of-time class loading & linking) |
| execução de treino | training run |
| árvore de decisão (de coletor) | (collector) decision tree |
| orçamento de latência | latency budget |
| carga elástica / escala a zero | elastic workload / scale-to-zero |
| postura de observabilidade | observability posture |
| imagem nativa | native image |
| triângulo latência × throughput × footprint | latency × throughput × footprint trade-off |
| uma mudança por rodada | one change per iteration |

## Cheatsheet do galho

Qual nota para qual problema — o índice reverso do galho:

| Problema / pergunta | Nota |
|---|---|
| Como a JVM executa código — o pipeline inteiro | [[01 - A JVM — o que é e o pipeline de execução]] |
| OOM — qual área de memória, o que cada erro significa | [[02 - Áreas de memória de runtime]] |
| GC — o conceito: reachability, gerações, STW | [[03 - Garbage Collection — o conceito]] |
| O que o `javac` gerou — bytecode e `javap` | [[04 - Bytecode por dentro — anatomia e javap]] |
| `ClassNotFoundException`, delegation, identidade de classe | [[05 - Classloading e o delegation model]] |
| Escolher coletor — o catálogo e os trade-offs | [[06 - Os coletores do HotSpot]] |
| Warmup, deoptimization, benchmark honesto | [[07 - JIT — C1, C2 e tiered compilation]] |
| `--add-opens`, encapsulamento, módulos | [[08 - JPMS — o sistema de módulos]] |
| Flags, ergonomics, JVM em container/K8s, exit 137 | [[09 - Flags, ergonomics e a JVM em containers]] |
| Ler GC logs — `-Xlog`, o que observar | [[10 - GC logs — unified logging e leitura]] |
| Tunar GC — metodologia, diais, quando trocar | [[11 - Tuning de GC — metodologia e prática]] |
| Forense — heap dump, thread dump, jcmd, NMT | [[12 - Diagnóstico — heap dumps, thread dumps e jcmd]] |
| Observabilidade contínua — JFR always-on, JMC | [[13 - JFR e JMC — observabilidade de produção]] |

## Veja também

- [[01 - A JVM — o que é e o pipeline de execução]]
- [[06 - Os coletores do HotSpot]]
- [[07 - JIT — C1, C2 e tiered compilation]]
- [[09 - Flags, ergonomics e a JVM em containers]]
- [[10 - GC logs — unified logging e leitura]]
- [[11 - Tuning de GC — metodologia e prática]]
- [[12 - Diagnóstico — heap dumps, thread dumps e jcmd]]
- [[13 - JFR e JMC — observabilidade de produção]]
- [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/12 - Virtual Threads e Project Loom|Virtual Threads]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#G1 GC|G1 GC (Dicionário)]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#ZGC (generational)|ZGC (Dicionário)]]
- [[03-Dominios/Tecnologia/Java/JVM/index|JVM por dentro (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]

## Referências

- [Class Data Sharing — Oracle JVM Guide (Java 21)](https://docs.oracle.com/en/java/javase/21/vm/class-data-sharing.html) — CDS reduz startup e footprint; archive mapeado em memória; AppCDS estende a classes da aplicação (system/platform/custom classloaders); archive default do JDK; `-XX:SharedArchiveFile`, `-XX:+AutoCreateSharedArchive`, `-Xshare`
- [JEP 483: Ahead-of-Time Class Loading & Linking](https://openjdk.org/jeps/483) — entregue no **Java 24**: classes carregadas e linkadas disponíveis no boot via AOT cache criado a partir de execução de treino; sem mudança de código
- [What's New in Project Leyden — JEP 514 and JEP 515 Explained (SoftwareMill)](https://softwaremill.com/whats-new-in-project-leyden-jep-514-and-jep-515-explained/) — **Java 25**: JEP 514 (AOT Command-Line Ergonomics) colapsa treino+criação via `-XX:AOTCacheOutput`; JEP 515 (AOT Method Profiling) inclui perfis de método no cache para o JIT compilar desde o boot
- [Project Leyden — OpenJDK](https://openjdk.org/projects/leyden/) — objetivo do projeto: reduzir startup e warmup da JVM
- [Run Into the New Year with Java's Ahead-of-Time Cache Optimizations — inside.java](https://inside.java/2026/01/09/run-aot-cache/) — uso do AOT cache nos JDKs 24/25
- Documentação dos coletores e do tuning citada nas notas [[06 - Os coletores do HotSpot]] e [[11 - Tuning de GC — metodologia e prática]] (Oracle GC Tuning Guide, Java 21/24; JEPs 248, 377, 439, 474, 490, 521)
