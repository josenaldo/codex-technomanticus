---
title: "JVM por dentro"
created: 2026-06-05
updated: 2026-06-05
type: moc
status: growing
publish: true
tags:
  - java
  - jvm
  - moc
aliases:
  - "JVM"
  - "Galho 3 - JVM por dentro"
---

# JVM por dentro

> [!abstract] TL;DR
> Galho 3 da trilha Java Senior; cobre memória de runtime, Garbage Collection (conceito → coletores → logs → tuning), JIT, classloading, bytecode, JPMS, diagnóstico (jcmd/heap dumps/JFR) e performance; 14 notas em 3 fases.

## Sobre este galho

Este galho cobre o **runtime da JVM de ponta a ponta**: o mapa de memória (heap, Metaspace, stack, code cache), o ciclo de vida do Garbage Collection com seus coletores do HotSpot, a compilação JIT com tiered compilation, o classloading e o delegation model, o bytecode e sua anatomia, o sistema de módulos JPMS, configuração de flags e ergonomics em containers, leitura de GC logs, tuning de GC com metodologia, diagnóstico forense (heap dumps, thread dumps, jcmd) e observabilidade contínua com JFR/JMC.

**Audiência primária:** dev senior em preparação para entrevista internacional — cada nota expõe o "porquê" das decisões e as perguntas mais cobradas, com vocabulário preciso em inglês. O mesmo dev que opera JVM em produção e precisa ir além do `-Xmx` quando o pod OOMKilla ou a latência explode. **Audiência secundária:** o mesmo dev no dia a dia de decisões de arquitetura e tuning — qual coletor escolher, como ler o GC log, quando o problema é de warmup e não de GC.

Este galho é um **refator do tronco** [[Java Fundamentals]]: a seção JVM foi extraída do monolito original, aprofundada e reorganizada em notas atômicas por fase — é a última grande seção do tronco a ser podada.

**Fronteira importante:** este galho cobre o *Java Memory Model* de **runtime** — layout de heap e stack, alocação de objetos, ciclo de vida do GC. O *Java Memory Model* de **concorrência** — happens-before, volatile, visibilidade entre threads — é do Galho 4: [[03-Dominios/Java/Concorrência e paralelismo/11 - Java Memory Model em profundidade|Java Memory Model em profundidade]].

## Iniciado

1. [[01 - A JVM — o que é e o pipeline de execução]] — o que é a JVM, a distinção JVM/JRE/JDK e o pipeline completo de execução: interpretação → profiling → compilação JIT para código nativo.
2. [[02 - Áreas de memória de runtime]] — o mapa das áreas de memória (heap, Metaspace, stack por thread, PC register, code cache) e o que cada `OutOfMemoryError` diz sobre qual área estourou.
3. [[03 - Garbage Collection — o conceito]] — reachability, GC roots, weak generational hypothesis, minor/major GC, stop-the-world e os vocabulários-base para ler logs e discutir tuning.
4. [[04 - Bytecode por dentro — anatomia e javap]] — o instruction set portátil da JVM, a estrutura do `.class` (magic number, constant pool, atributos) e `javap -c -v` como lupa do compilador.
5. [[05 - Classloading e o delegation model]] — as três fases loading → linking → initialization, o parent delegation model e por que a identidade de uma classe é o par nome + classloader que a definiu.

## Adepto

6. [[06 - Os coletores do HotSpot]] — catálogo dos coletores (G1, ZGC, Parallel, Serial) com o trade-off pausa × throughput × footprint de cada um e critérios de escolha atualizados (CMS removido no Java 14, ZGC generational-only no Java 24).
7. [[07 - JIT — C1, C2 e tiered compilation]] — interpretador, C1 e C2 como estágios da tiered compilation, warmup, deoptimização e por que benchmark ingênuo mente sobre performance Java.
8. [[08 - JPMS — o sistema de módulos]] — módulos como unidade de encapsulamento acima de pacotes (`requires`/`exports`), convivência com o classpath e por que `--add-opens` existe no ecossistema de frameworks.
9. [[09 - Flags, ergonomics e a JVM em containers]] — flags `-X`/`-XX`, ergonomics a partir de cgroups via `UseContainerSupport`, o erro clássico do `-Xmx` colado no limite do pod e `PrintFlagsFinal` como fonte da verdade.
10. [[10 - GC logs — unified logging e leitura]] — `-Xlog` unificado (Java 9, JEP 158), o que observar no log (pausas em percentis, frequência, taxa de promoção, humongous allocations, Full GC como sinal de problema).

## Magus

11. [[11 - Tuning de GC — metodologia e prática]] — o triângulo latência × throughput × footprint, a metodologia baseline → meta mensurável → uma mudança por vez → medir sob carga real, e quando a resposta certa é trocar de coletor ou consertar o código.
12. [[12 - Diagnóstico — heap dumps, thread dumps e jcmd]] — kit forense da JVM: jcmd como canivete central, heap dump para OOM, thread dump para deadlock, NMT para quando o RSS do processo cresce além do heap Java configurado.
13. [[13 - JFR e JMC — observabilidade de produção]] — JFR como gravador contínuo de eventos em produção (GC, alocação, locks, I/O) com overhead baixo, e JMC como analisador dos arquivos `.jfr` — o filme antes do sinistro vs. a foto depois.
14. [[14 - Performance da JVM — síntese]] — capstone do galho: árvore de decisão de coletor, mapa do eixo temporal startup → warmup → peak e checklist de troubleshooting que aponta de cada sintoma para a nota que o resolve.

## Rotas alternativas

### Completa

01 → 02 → 03 → 04 → 05 → 06 → 07 → 08 → 09 → 10 → 11 → 12 → 13 → 14. Percurso linear do básico ao avançado.

### Entrevista internacional

01 → 02 → 03 → 06 → 07 → 14. Pipeline de execução, mapa de memória, GC como conceito, coletores com trade-offs, JIT e síntese — o que mais cai em entrevistas de nível senior.

### Sobrevivência em produção

09 → 10 → 12 → 13 → 11. Flags e containers antes de qualquer tuning, leitura de GC log, forense com heap/thread dump e jcmd, observabilidade contínua com JFR e tuning com metodologia — o mínimo para operar JVM em produção sem adivinhação.

### Por dentro do runtime

04 → 05 → 07 → 08. Bytecode e anatomia do `.class`, classloading e delegation model, JIT com tiered compilation, e JPMS — a cadeia completa de como código Java vira execução.

### Tuning de memória e GC

02 → 03 → 06 → 10 → 11. Mapa de memória, GC como conceito, coletores do HotSpot, leitura de GC log e tuning com metodologia — trilha focada em memória e coleta de lixo do conceito ao ajuste fino.

## Todas as notas

```dataview
TABLE fase, status, updated
FROM "03-Dominios/Java/JVM"
WHERE type = "concept"
SORT file.name ASC
```

## Veja também

- [[03-Dominios/Java/index|Java (MOC central)]]
- [[03-Dominios/Java/Linguagem e sintaxe moderna/index|Linguagem e sintaxe moderna (Galho 1)]]
- [[03-Dominios/Java/Collections e Streams/index|Collections, Streams e Programação Funcional (Galho 2)]]
- [[03-Dominios/Java/Concorrência e paralelismo/index|Concorrência e paralelismo (Galho 4)]]
- [[03-Dominios/Java/Dicionário de Java|Dicionário de Java]]
- [[Java Fundamentals]] (tronco em transição)
