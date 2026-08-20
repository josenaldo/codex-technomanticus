---
title: "Os coletores do HotSpot"
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
aliases:
  - "Coletores de GC"
  - "G1"
  - "ZGC"
  - "Shenandoah"
---

# Os coletores do HotSpot

> [!abstract] TL;DR
> O HotSpot oferece múltiplos coletores porque não existe GC ótimo para todos os cenários — cada um ocupa um ponto diferente no trade-off **pausa × throughput × footprint × tamanho de heap**. **G1 é o default desde o Java 9** (JEP 248) e cobre bem a maioria dos serviços; **ZGC** entrega pausas sub-milissegundo para latência crítica e heaps enormes; **Parallel** maximiza throughput em batch; **Serial** serve heaps minúsculos. A tabela mental precisa estar atualizada: **CMS foi removido no Java 14** (JEP 363) e **ZGC é generational-only desde o Java 24** (JEP 490) — citar CMS como opção viva ou ZGC como single-generation denuncia conhecimento de 2019.

## O que é

Esta nota é o catálogo dos coletores do HotSpot — quem são, como funcionam por dentro e quando escolher cada um. Os conceitos compartilhados por todos (reachability, gerações, STW, safepoints) estão em [[03 - Garbage Collection — o conceito]]; aqui o assunto é a **decisão**.

Escolher coletor não é detalhe de configuração — é **decisão de arquitetura com efeitos observáveis**:

- **p99/p999 de latência**: pausas STW aparecem direto no tail latency dos requests.
- **Custo de CPU**: coletores concorrentes (ZGC, Shenandoah) trocam pausa por ciclos de CPU rodando em paralelo com a aplicação.
- **Custo de RAM**: low-pause exige folga de heap e estruturas auxiliares — o mesmo workload pode precisar de mais memória sob ZGC do que sob G1.
- **Comportamento sob pico**: cada coletor degrada de um jeito diferente quando a taxa de alocação excede a capacidade de coleta.

O catálogo atual (Java 21+) tem cinco coletores em produção ou suporte — Serial, Parallel, G1, ZGC e Shenandoah — mais o Epsilon (experimental, no-op) e um fantasma que ainda assombra blogs: o CMS, removido no Java 14.

## Por que importa

Dois motivos, um de produção e um de carreira:

**Em produção, escolha errada custa dinheiro ou SLA.** Um serviço de pagamentos com SLA de p99 < 50ms rodando Parallel GC vai estourar o SLA a cada major GC. No sentido inverso, um job batch noturno rodando ZGC paga overhead de CPU concorrente para obter pausas curtas que ninguém está medindo — throughput menor, job mais longo, mais horas de máquina. A escolha do coletor é uma das poucas decisões de JVM com impacto direto e mensurável na conta de cloud.

**Em entrevista, o catálogo cobrado é o ATUAL.** As perguntas clássicas — "qual o GC default?", "quando você usaria ZGC?", "o que aconteceu com o CMS?" — têm respostas que mudaram nos últimos anos:

- CMS está **morto** desde o Java 14. Mencioná-lo como opção atual data o conhecimento do candidato.
- ZGC deixou de ser experimental no Java 15 e virou **generational** (a evolução mais importante do GC recente): opt-in no 21, default no 23, modo único no 24.
- G1 é default desde o Java 9 — quem responde "Parallel" parou no Java 8.

Material desatualizado domina os resultados de busca sobre GC. Um senior precisa saber filtrar.

## Como funciona

### Serial e Parallel (geracionais clássicos, throughput-first)

Os dois coletores mais antigos do HotSpot são **totalmente stop-the-world**: quando coletam, a aplicação para até o fim da coleta. Ambos são geracionais no modelo clássico (Eden + Survivors + Old) e **compactam** a Old Generation, evitando fragmentação.

**Serial** (`-XX:+UseSerialGC`) usa **uma única thread** para todo o trabalho de GC. Sem coordenação entre threads, o overhead por ciclo é o menor possível — mas a pausa cresce linearmente com o heap. A documentação da Oracle o recomenda para heaps de até ~100 MB ou máquinas de um único processador. Em 2026, isso significa: **sidecars, containers com 1 vCPU, CLIs e funções serverless de heap pequeno**. Nesses ambientes, o Serial costuma vencer o G1 em footprint (sem estruturas auxiliares de região, sem threads de GC ociosas).

**Parallel** (`-XX:+UseParallelGC`), também chamado de *throughput collector*, paraleliza o trabalho de coleta entre múltiplas threads. As pausas continuam sendo STW completas, mas terminam mais rápido. Foi o **default até o Java 8**. Continua sendo a melhor escolha quando:

- O objetivo é **maximizar throughput total** (trabalho útil por hora de CPU).
- Pausas de centenas de ms — ou até segundos — são aceitáveis.
- O perfil é **batch**: ETL, processamento de filas offline, jobs noturnos, builds.

Num job que processa 50 milhões de registros sem ninguém esperando resposta, uma pausa de 800ms é irrelevante; o que importa é terminar o job no menor tempo total — e nesse jogo o Parallel ainda é difícil de bater.

### G1 — o default (regions, pause target, mixed collections, humongous)

O **Garbage-First (G1)** é o default do HotSpot **desde o Java 9 (JEP 248)**, substituindo o Parallel. Seu objetivo de design: pausas **previsíveis e configuráveis** em heaps de médios a grandes, sem sacrificar muito throughput.

A inovação estrutural do G1 é abandonar o heap contíguo dividido em gerações fixas. O heap vira um conjunto de **regiões** de tamanho uniforme:

- Tamanho calculado ergonomicamente visando **~2.048 regiões**, sempre potência de 2 — na prática, entre **1 e 32 MB** por padrão (configurável até 512 MB via `-XX:G1HeapRegionSize`).
- Cada região assume um papel dinâmico: Eden, Survivor ou Old. As "gerações" são conjuntos lógicos de regiões, não áreas físicas fixas.

Os mecanismos centrais:

- **Pause time target**: `-XX:MaxGCPauseMillis` (default **200ms**) define a meta de pausa. O G1 ajusta quantas regiões evacua por ciclo para tentar cumprir a meta — é heurística com alta probabilidade de acerto, não garantia.
- **Garbage first**: na fase de space-reclamation, o G1 prioriza as regiões com **mais lixo** (melhor retorno por ms de pausa) — daí o nome.
- **Mixed collections**: depois de um ciclo de marcação concorrente (algoritmo **SATB** — snapshot-at-the-beginning), o G1 executa coletas que evacuam a Young **mais um subconjunto de regiões da Old** selecionadas pelo custo-benefício. É assim que a Old é limpa incrementalmente, sem Full GC.
- **Humongous objects**: objetos com tamanho **≥ metade de uma região** são alocados em regiões contíguas dedicadas direto na Old. São caros de gerenciar — geralmente só reclamados ao fim da marcação ou em Full GC — e alocação frequente deles pode disparar coletas prematuras.

O plano B do G1 também importa: se uma evacuação falha por falta de regiões livres (*evacuation failure*) ou a alocação supera a capacidade de coleta, o G1 recorre a uma **Full GC** — stop-the-world sobre o heap inteiro, a pausa longa que ele existe para evitar. Full GC frequente em G1 não é "comportamento normal": é sintoma de heap subdimensionado, excesso de humongous ou meta de pausa impossível.

O G1 é o "meio-termo bem calibrado": pausas na casa de dezenas a ~200ms, throughput bom, funciona de poucos GB a centenas de GB. Para a maioria dos serviços web e APIs, **é a resposta certa por default** — só vale trocar com requisito medido.

### ZGC — low-latency (concurrent, pausas sub-ms, generational)

O **Z Garbage Collector** é o coletor de baixa latência do HotSpot: projetado para que **nenhuma pausa STW exceda 1 milissegundo**, com pausas **independentes do tamanho do heap** — de algumas centenas de MB até **16 TB**, segundo a documentação da Oracle.

Como isso é possível: praticamente todo o trabalho — marcação, relocação de objetos, processamento de referências — acontece **de forma concorrente**, com as threads da aplicação rodando. As fases STW restantes são curtíssimas e de duração constante. A mágica fica nos **colored pointers** (metadados de estado do GC embutidos nos próprios ponteiros de 64 bits) e nos **load barriers** (verificações injetadas pelo JIT em cada leitura de referência, que corrigem ponteiros para objetos realocados on-the-fly).

A linha do tempo de versões — onde mais se cai em entrevista:

| Marco | JEP | Versão |
|-------|-----|--------|
| ZGC experimental | JEP 333 | Java 11 |
| ZGC **produção** | JEP 377 | **Java 15** |
| ZGC **generational** (opt-in: `-XX:+ZGenerational`) | JEP 439 | **Java 21** |
| Generational vira **default**; modo single-gen deprecado | JEP 474 | Java 23 |
| Modo non-generational **removido**; flag `ZGenerational` obsoleta | JEP 490 | **Java 24** |

O ZGC original era **single-generation**: coletava o heap inteiro a cada ciclo, abrindo mão da hipótese geracional. Funcionava, mas exigia mais CPU e mais headroom de heap para acompanhar taxas de alocação altas. O **Generational ZGC** (JEP 439) reintroduziu Young/Old dentro do design concorrente — coleta a Young com frequência e a Old raramente, mantendo as pausas sub-ms. Resultado: o mesmo workload roda com **menos heap e menos CPU**. No Java 24, a documentação da Oracle é explícita: *"As of JDK 24 ZGC is a generational garbage collector. The `ZGenerational` option has been removed."* Em 2026, dizer "ZGC não é geracional" é informação de três gerações de JDK atrás.

O custo do ZGC: o trabalho concorrente **compete por CPU** com a aplicação, e os load barriers adicionam overhead por leitura de referência. Throughput total tende a ser um pouco menor que G1/Parallel no mesmo hardware. É o preço da latência — e ele deve ser pago só quando latência é o requisito.

### Shenandoah (perfil similar ao ZGC, história Red Hat)

O **Shenandoah** é o "primo" do ZGC: também low-pause, também faz **evacuação concorrente** (realoca objetos com a aplicação rodando), com pausas curtas e pouco sensíveis ao tamanho do heap. Foi desenvolvido pela **Red Hat** e contribuído ao OpenJDK.

Linha do tempo verificada:

- **Produção: JEP 379, Java 15** — mesmo release em que o ZGC saiu do experimental.
- **Generational Shenandoah: JEP 404, Java 24** — entrou como **experimental** (havia sido proposto para o 21 e adiado por risco/tempo de revisão).
- **JEP 521, Java 25** — o modo generational virou **product feature** (sem `-XX:+UnlockExperimentalVMOptions`), mas **não é o default do Shenandoah**: por padrão ele continua single-generation, e o modo geracional é opt-in via `-XX:ShenandoahGCMode=generational`.

Diferença prática mais relevante: **disponibilidade nos builds**. O Shenandoah faz parte do OpenJDK, mas **não é incluído nos builds da Oracle** — por isso ele não aparece no GC Tuning Guide oficial. Está disponível em Red Hat builds, Eclipse Temurin, Amazon Corretto e na maioria das demais distribuições OpenJDK. Se a infraestrutura é Red Hat/OpenShift, o Shenandoah é cidadão de primeira classe; se o time usa Oracle JDK, ele simplesmente não existe como opção.

Na escolha ZGC vs Shenandoah, o empate técnico é comum — ambos entregam pausas de poucos ms ou menos. Os critérios de desempate costumam ser o build de JDK em uso, a versão (o ZGC generational amadureceu um release antes) e benchmarks com o workload real.

### Epsilon (no-op — benchmark e testes)

O **Epsilon** (`-XX:+UseEpsilonGC`, JEP 318, **Java 11**, experimental — exige `-XX:+UnlockExperimentalVMOptions`) é um anti-coletor proposital: **gerencia alocação, mas nunca coleta nada**. Quando o heap enche, a JVM morre com `OutOfMemoryError`.

Parece piada, mas tem usos legítimos:

- **Benchmarks**: medir performance de código sem nenhuma interferência de GC — isola o custo do GC por comparação.
- **Testes de pressão de alocação**: descobrir exatamente quanto um workload aloca (o heap consumido é a alocação total).
- **Jobs efêmeros**: processos que alocam menos que o heap disponível e morrem antes de precisar de coleta — zero overhead de GC.
- **Latência extrema**: sistemas que pré-alocam tudo e não geram lixo no caminho quente.

Epsilon nunca é resposta para um serviço de longa duração — é ferramenta de medição e nicho.

### CMS — nota histórica (removido, mas ainda assombra)

O **Concurrent Mark Sweep** foi por mais de uma década o coletor low-pause do HotSpot: marcação concorrente da Old Generation, pausas menores que as do Parallel. Mas não compactava a Old — sofria de **fragmentação**, que eventualmente forçava uma Full GC serial catastrófica — e seu código complicava a manutenção do GC inteiro.

Destino selado em duas etapas: **deprecado no Java 9 (JEP 291)** e **REMOVIDO no Java 14 (JEP 363)**. O código foi deletado do HotSpot; o G1 sempre foi seu sucessor designado, e ZGC/Shenandoah cobriram o caso low-pause.

Consequência prática que ainda morde em 2026: uma quantidade enorme de blogs, respostas de Stack Overflow e configs herdadas recomenda `-XX:+UseConcMarkSweepGC` e suas dezenas de flags satélites (`CMSInitiatingOccupancyFraction` e cia.). Num JDK ≥ 14, essas flags não são ignoradas com warning — **a JVM se recusa a subir** (`Unrecognized VM option`). CMS hoje é resposta de entrevista ("o que aconteceu com ele e por quê"), nunca de produção.

### Tabela comparativa

| Coletor | Desde | Pausas | Throughput | Heap ideal | Uso ideal |
|---------|-------|--------|------------|------------|-----------|
| **Serial** | JDKs 1.x (origens do HotSpot) | Longas (STW total, 1 thread) | Baixo em heap grande; ótimo custo fixo em heap mínimo | < ~100 MB | Sidecars, containers 1 vCPU, CLIs |
| **Parallel** | Era o default até o Java 8 | Longas, mas paralelizadas (centenas de ms+) | **Máximo** | Médio a grande | Batch, ETL, jobs sem SLA de latência |
| **G1** | **Default desde Java 9** (JEP 248) | Previsíveis (~target de 200ms, ajustável) | Bom | Alguns GB a centenas de GB | Serviços de propósito geral — o ponto de partida |
| **ZGC** | Produção Java 15 (JEP 377); generational-only desde Java 24 (JEP 490) | **< 1ms**, independentes do heap | Bom, com custo de CPU concorrente e load barriers | Centenas de MB a **16 TB** | p99/p999 crítico, heaps muito grandes |
| **Shenandoah** | Produção Java 15 (JEP 379); generational product no Java 25 (JEP 521, opt-in) | Poucos ms ou menos | Similar ao ZGC | Médio a muito grande | Latência crítica em builds OpenJDK (Red Hat, Temurin, Corretto) |
| **Epsilon** | Java 11 (JEP 318), experimental | Nenhuma (nunca coleta — OOM no limite) | Máximo possível, até o heap acabar | Qualquer, efêmero | Benchmarks, testes de alocação |
| ~~CMS~~ | Deprecado Java 9 (JEP 291), **removido Java 14 (JEP 363)** | — | — | — | Nota histórica; flag derruba a JVM em JDK ≥ 14 |

## Na prática

### Flags de seleção

```bash
# G1 — o default; a flag explícita só documenta a intenção
java -XX:+UseG1GC -Xmx4g -jar app.jar

# G1 com meta de pausa mais agressiva que os 200ms default
java -XX:+UseG1GC -XX:MaxGCPauseMillis=100 -Xmx8g -jar app.jar

# ZGC — low-latency (generational por padrão no 23+; modo único no 24+)
java -XX:+UseZGC -Xmx32g -jar app.jar

# ZGC generational no Java 21 (onde ainda era opt-in via JEP 439)
java -XX:+UseZGC -XX:+ZGenerational -Xmx32g -jar app.jar   # NÃO usar em 24+: flag obsoleta

# Parallel — throughput máximo para batch
java -XX:+UseParallelGC -Xmx16g -jar batch-job.jar

# Serial — heap pequeno, container de 1 vCPU
java -XX:+UseSerialGC -Xmx256m -jar sidecar.jar

# Epsilon — benchmark/teste (experimental: exige unlock)
java -XX:+UnlockExperimentalVMOptions -XX:+UseEpsilonGC -Xmx8g -jar benchmark.jar

# Shenandoah — em builds que o incluem (Temurin, Corretto, Red Hat)
java -XX:+UseShenandoahGC -Xmx16g -jar app.jar
```

### Decisão de primeira ordem

```bash
# Árvore de decisão — ponto de partida, não veredito final:
#
# 1. Sem requisito específico medido?
#    → fique no G1 (default). Não troque GC por palpite.
#
# 2. p99/p999 de latência é requisito de negócio, ou heap > dezenas de GB?
#    → ZGC. Pausas sub-ms, escala até 16 TB.
#      (em builds OpenJDK não-Oracle, Shenandoah é alternativa equivalente)
#
# 3. Batch/ETL sem ninguém esperando resposta, throughput é o que importa?
#    → Parallel. Pausas longas são irrelevantes; trabalho total por hora vence.
#
# 4. Heap minúsculo (< ~100 MB), 1 vCPU, sidecar/CLI?
#    → Serial. Menor footprint, menor custo fixo.
#
# Em TODOS os casos: valide com carga real e GC logs antes e depois.
```

### Conferindo qual coletor está ativo

Não confie no que o Dockerfile diz — pergunte à JVM. A seleção ergonômica varia com hardware, e uma flag mal digitada pode estar sendo a causa de outro coletor estar rodando:

```bash
# Qual coletor a JVM selecionou nesta máquina/configuração?
java -XX:+PrintFlagsFinal -version | grep -E 'Use\w+GC.*true'
#   bool UseG1GC = true        ← G1 ativo (ergonomic ou via flag)

# Em runtime, a primeira linha do GC log identifica o coletor:
java -Xlog:gc -jar app.jar
# [0.004s][info][gc] Using G1
# [0.003s][info][gc] Using The Z Garbage Collector   ← se ZGC

# Num processo já em execução:
jcmd <pid> VM.flags | tr ' ' '\n' | grep GC
```

Esse check de 10 segundos evita a situação clássica: o time "ativou o ZGC" num `JAVA_OPTS` que outro layer da imagem sobrescreve, e passa semanas analisando logs do G1 achando que são do ZGC.

Duas observações de quem opera isso:

- **A comparação precisa ser justa.** O G1 vence o ZGC em throughput por core e em footprint em heaps moderados com SLA folgado; o ZGC vence o G1 quando o p99 é apertado ou o heap é tão grande que as pausas do G1 escalam. Não existe "ZGC é melhor" — existe "melhor para qual métrica".
- **A flag é só o começo.** A validação vem dos GC logs ([[10 - GC logs — unified logging e leitura]]) e de uma metodologia de medição ([[11 - Tuning de GC — metodologia e prática]]). Em containers, a ergonomia de seleção automática tem pegadinhas próprias — [[09 - Flags, ergonomics e a JVM em containers]].

## Armadilhas

### (1) Copiar flags de blog antigo — a JVM nem sobe

**O problema:** tutoriais de tuning escritos na era Java 8 recomendam CMS e suas flags. Em qualquer JDK ≥ 14, flags de coletores removidos não são ignoradas — são **erro fatal de inicialização**. O deploy falha com a aplicação nem chegando a subir:

```bash
$ java -XX:+UseConcMarkSweepGC -jar app.jar
Unrecognized VM option 'UseConcMarkSweepGC'
Error: Could not create the Java Virtual Machine.
Error: A fatal exception has occurred. Program will exit.
```

O mesmo vale para flags satélites do CMS (`CMSInitiatingOccupancyFraction`, `UseCMSInitiatingOccupancyOnly`) e, desde o Java 24, para `-XX:+ZGenerational` (obsoleta pelo JEP 490). Pior variação do problema: a flag morta está enterrada num `JAVA_OPTS` de Dockerfile herdado, e o erro só aparece no upgrade de JDK.

**Fix:** ao migrar de versão, **audite todas as flags de JVM contra as release notes** da versão de destino. `java -XX:+PrintFlagsFinal -version` lista as flags que o JDK atual reconhece. Trate qualquer flag de GC copiada da internet como suspeita até confirmar que existe — e que faz o que o blog dizia — na SUA versão de JDK.

---

### (2) Ligar ZGC em heap pequeno esperando milagre

**O problema:** "ZGC tem pausas sub-milissegundo" vira "ZGC é o melhor GC, vou usar em tudo". Num serviço com heap de 512 MB e p99 confortável, trocar G1 por ZGC tende a **piorar** o quadro: o ZGC consome mais CPU em trabalho concorrente, adiciona overhead de load barrier em cada leitura de referência e precisa de mais headroom de heap para operar com folga. O serviço fica com throughput menor e footprint maior — pagando o preço da latência ultra-baixa sem precisar dela.

```bash
# Cheiro de decisão por hype, não por medição:
java -XX:+UseZGC -Xmx512m -jar api-pequena.jar
# Heap pequeno + SLA folgado: o G1 default provavelmente entrega
# p99 equivalente com menos CPU e menos memória.
```

**Fix:** decida por **medição, não por reputação**. Capture GC logs com o G1 sob carga real; se as pausas observadas já cabem no SLA, não há problema a resolver. Se o p99 estoura por pausa de GC comprovada nos logs, aí sim teste o ZGC — com benchmark do workload real comparando p99, throughput e consumo de CPU/RAM antes e depois.

---

### (3) Achar que "pausa < 1ms" significa "GC de graça"

**O problema:** pausas sub-milissegundo medem só o tempo **stop-the-world** — não o custo total do GC. Coletores concorrentes não eliminam o trabalho de coleta; eles o **deslocam** para threads que rodam em paralelo com a aplicação, competindo pelos mesmos cores. Numa máquina de 4 vCPUs com CPU já saturada, ligar ZGC pode degradar o throughput da aplicação ou, pior, deixar o coletor sem CPU para acompanhar a taxa de alocação — forçando *allocation stalls*, em que threads da aplicação param esperando o GC liberar memória. A "pausa invisível" volta por outra porta.

**Fix:** dimensione **CPU junto com o GC**. Coletores concorrentes pedem folga de cores além do que a aplicação usa em pico. Monitore, além do tempo de pausa: utilização de CPU das threads de GC, tempo total gasto em GC por minuto e ocorrência de allocation stalls nos logs. Se a aplicação satura a CPU sozinha, resolva a capacidade antes de trocar de coletor — GC concorrente em CPU saturada só muda o formato do problema.

---

### (4) Levar flags geracionais da era Parallel para o G1

**O problema:** receitas antigas de tuning fixam o tamanho da Young Generation com `-Xmn` ou `-XX:NewRatio` — prática comum no Parallel/CMS. No G1, essas flags **funcionam**, mas sabotam o mecanismo central do coletor: o G1 cumpre o `MaxGCPauseMillis` justamente **redimensionando a Young dinamicamente** a cada ciclo. Fixar a Young tira do G1 sua principal alavanca de controle de pausa — a meta vira letra morta e as pausas ficam erráticas.

```bash
# Config herdada da era Java 8 rodando em G1 moderno:
java -XX:+UseG1GC -Xmn2g -XX:MaxGCPauseMillis=100 -jar app.jar
# -Xmn fixa a Young em 2 GB → o G1 perde a capacidade de encolhê-la
# para cumprir os 100ms; o pause target vira decorativo.
```

**Fix:** ao adotar (ou herdar) G1, comece **limpando o tuning antigo**, não acumulando flags por cima. O ponto de partida saudável do G1 é mínimo: `-Xmx` (e `-Xms`) + `MaxGCPauseMillis` se o default de 200ms não servir. Só adicione flags adicionais com hipótese formada a partir dos GC logs — a metodologia está em [[11 - Tuning de GC — metodologia e prática]].

## Em entrevista

### Frase pronta (inglês)

> "HotSpot ships several collectors because GC is a trade-off space — pause time, throughput, footprint, and heap size pull in different directions. G1 has been the default since Java 9: it splits the heap into regions, targets a configurable pause goal of 200 milliseconds by default, and reclaims the old generation incrementally through mixed collections, which makes it a solid general-purpose choice."

> "When I have a strict latency requirement or a very large heap, I reach for ZGC: it does almost all of its work concurrently, keeps pauses under a millisecond regardless of heap size, and since it became generational — opt-in in Java 21, the default in 23, and the only mode from Java 24 onwards — it handles high allocation rates with much less CPU and memory headroom than the original design. The trade-off versus G1 is that ZGC's concurrent work and load barriers cost CPU and some throughput, so for a typical service with a comfortable SLA, G1 is usually the better deal — I only switch after GC logs prove that pauses are actually breaking the SLA."

> "It's also worth keeping the mental table current: CMS was removed in Java 14, so its flags won't even let the JVM start on a modern JDK; Parallel is still the right answer for pure throughput batch workloads; and Shenandoah offers a ZGC-like low-pause profile in OpenJDK builds — its generational mode became a product feature in Java 25, though it's still opt-in."

### Vocabulário

| Termo PT | Termo EN |
|----------|----------|
| coletor de lixo | garbage collector |
| pausa stop-the-world | stop-the-world pause |
| meta de tempo de pausa | pause time target / pause time goal |
| coletor de throughput | throughput collector |
| coleta concorrente | concurrent collection |
| evacuação concorrente | concurrent evacuation |
| região (de heap) | (heap) region |
| coleta mista | mixed collection |
| objeto humongous | humongous object |
| barreira de leitura | load barrier |
| ponteiros coloridos | colored pointers |
| ZGC geracional | Generational ZGC |
| latência de cauda | tail latency (p99/p999) |

## Veja também

- [[03 - Garbage Collection — o conceito]]
- [[09 - Flags, ergonomics e a JVM em containers]]
- [[10 - GC logs — unified logging e leitura]]
- [[11 - Tuning de GC — metodologia e prática]]
- [[14 - Performance da JVM — síntese]]
- [[03-Dominios/Tecnologia/Java/JVM/index|JVM por dentro (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#G1 GC|G1 GC (Dicionário)]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#ZGC (generational)|ZGC (Dicionário)]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#Shenandoah|Shenandoah (Dicionário)]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#Epsilon GC|Epsilon GC (Dicionário)]]

## Referências

- [Available Collectors — Oracle GC Tuning Guide (Java 21)](https://docs.oracle.com/en/java/javase/21/gctuning/available-collectors.html)
- [Garbage-First (G1) Garbage Collector — Oracle GC Tuning Guide (Java 21)](https://docs.oracle.com/en/java/javase/21/gctuning/garbage-first-g1-garbage-collector1.html)
- [The Z Garbage Collector — Oracle GC Tuning Guide (Java 21)](https://docs.oracle.com/en/java/javase/21/gctuning/z-garbage-collector.html)
- [The Z Garbage Collector — Oracle GC Tuning Guide (Java 24)](https://docs.oracle.com/en/java/javase/24/gctuning/z-garbage-collector.html) — confirma: "As of JDK 24 ZGC is a generational garbage collector. The `ZGenerational` option has been removed."
- JEP 248: Make G1 the Default Garbage Collector (Java 9)
- JEP 291: Deprecate the Concurrent Mark Sweep (CMS) Garbage Collector (Java 9)
- JEP 318: Epsilon: A No-Op Garbage Collector — Experimental (Java 11)
- JEP 333: ZGC: A Scalable Low-Latency Garbage Collector — Experimental (Java 11)
- JEP 363: Remove the Concurrent Mark Sweep (CMS) Garbage Collector (Java 14)
- JEP 377: ZGC: A Scalable Low-Latency Garbage Collector — Production (Java 15)
- JEP 379: Shenandoah: A Low-Pause-Time Garbage Collector — Production (Java 15)
- JEP 439: Generational ZGC (Java 21)
- JEP 474: ZGC: Generational Mode by Default (Java 23)
- JEP 490: ZGC: Remove the Non-Generational Mode (Java 24)
- JEP 404: Generational Shenandoah — Experimental (Java 24)
- JEP 521: Generational Shenandoah — product feature, opt-in (Java 25)
