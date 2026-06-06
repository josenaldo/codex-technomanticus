---
title: "Spec — Galho 3 da trilha Java Senior (JVM por dentro)"
date: 2026-06-05
author: Josenaldo
status: draft
type: spec
publish: false
---

# Spec — Galho 3 da trilha Java Senior (JVM por dentro)

## 1. Contexto e motivação

Este é o **terceiro galho** da trilha Java Senior (roadmap em `docs/superpowers/specs/2026-06-02-java-senior-roadmap-design.md`). Pressupõe leitura do roadmap, que estabelece topologia flat, esquema de 3 fases, padrões editoriais e política de poda. Os Galhos 1 (Linguagem, 15 notas), 2 (Collections/Streams, 16 notas), 4 (Concorrência, 16 notas) e 5 (Swing, 12 notas) já fecharam e estão em `main` — seus artefatos são o **template de padrão e qualidade** deste galho.

**Como o Galho 2, este é um galho de REFATOR DE TRONCO.** Tem tronco a podar: a seção `## JVM (Java Virtual Machine)` de `Core/Java Fundamentals.md` (linhas ~33-225), marcada `[!info] Migra em galho futuro (Galho 3)`. Consequências:

- **Pré-flight de leitura de tronco executado** (§6): headings reais da seção JVM confirmados; podas dos Galhos 1 e 2 verificadas; a seção JVM é a **última grande seção cheia** do tronco — depois dela, só resta `## Concorrência (visão geral)`, dívida residual do Galho 4 (**não podar aqui**).
- **Há task de poda** (§3.5): a seção JVM vira callout com wikilinks pras notas novas.
- **Higienização:** a seção JVM está limpa de fabricação em 1ª pessoa (diferente da cauda que o Galho 2 higienizou) — a poda absorve o corpo todo, incluindo a sub `### Project Loom e Virtual Threads`, que já só aponta pro Galho 4.
- **Decisão sobre o destino do tronco** (§3.6): com a seção JVM podada, o tronco fica reduzido a intro + callouts + dívida do Galho 4 + cauda. Decisão registrada: conversão em nota-resumo enxuta é **diferida** pro fechamento da dívida do Galho 4.
- **Conteúdo do tronco é matéria-prima desatualizada:** a tabela de GC cita CMS sem nota de remoção, data ZGC como "Java 15" (production-ready), ignora ZGC generational (Java 21+) e Shenandoah generational — as notas **expandem e modernizam via WebFetch**, não copiam.

Galho 3 é o **dono dos conceitos de runtime/JVM** da trilha: memória de runtime, GC, JIT, classloading, bytecode, JPMS, diagnóstico e performance. Depende do Galho 1. Denso e técnico por natureza — **14 notas**, na faixa dos Galhos 1 (15), 2 (16) e 4 (16).

**Distinção de fronteira nuclear deste galho:** *memory model de runtime* (layout heap/stack/metaspace, alocação, GC — dono: Galho 3) ≠ *Java Memory Model* (happens-before, volatile, visibilidade entre threads — dono: Galho 4, nota 11). As notas deste galho linkam o JMM quando tocarem visibilidade, **sem re-explicar**.

## 2. Objetivo

Produzir, em uma sessão de execução dedicada **direto na `main`** (sem branch dedicada — ver [[feedback_galhos_direto_main]]), **14 notas atômicas + 1 MOC do galho + expansão do Dicionário de Java + ativação do MOC central + poda da seção JVM do tronco**, em `03-Dominios/Java/JVM/` e `03-Dominios/Java/`, todas `publish: true`, em PT-BR, distribuídas em 3 fases (5 Iniciado + 5 Adepto + 4 Magus).

Ao terminar o galho, o leitor deve conseguir:

- **Explicar em inglês** o pipeline de execução da JVM (bytecode → interpretação → JIT), o layout de memória de runtime, o funcionamento geracional do GC e o papel do classloading com parent delegation.
- **Escolher e justificar** um coletor de GC (G1 vs ZGC vs Parallel vs Serial) para um perfil de carga dado, com trade-offs de latência/throughput/footprint na ponta da língua.
- **Diagnosticar** problemas reais de produção: ler GC logs, capturar e analisar heap dumps e thread dumps, usar `jcmd`/JFR/JMC, reconhecer OOM por área de memória.
- **Decidir e defender** estratégias de tuning (quando tunar, quando trocar de coletor, quando o problema não é GC) sem cargo cult de flags.

A barra é "operar, diagnosticar e decidir sobre a JVM em produção e defender em entrevista" — não "implementar um GC ou um JIT from scratch".

## 3. Saídas concretas

### 3.1. Notas (`03-Dominios/Java/JVM/`)

Pasta **nova**, flat. 14 notas + 1 MOC (`index.md`, obrigatório — Quartz folder-link). Numeração global por galho (não reinicia por fase). Tag de galho: `jvm`.

#### Iniciado (5 notas — vocabulário + modelo mental)

| # | Nota | Escopo nuclear |
|---|------|----------------|
| 01 | A JVM — o que é e o pipeline de execução | JVM vs JRE vs JDK; "write once, run anywhere"; pipeline `javac` → bytecode → classload → verify → interpret → JIT; HotSpot como implementação de referência; outras implementações (OpenJ9, GraalVM — menção). Porta de entrada do galho. |
| 02 | Áreas de memória de runtime | Heap (Young: Eden/S0/S1; Old/Tenured; humongous objects no G1), Metaspace (Java 8+, vs PermGen), stack por thread (frames, variáveis locais, operandos), PC register, native method stack, code cache. Mapa de erros por área: variantes de `OutOfMemoryError` (heap, metaspace, native) vs `StackOverflowError`. **Fronteira:** visibilidade entre threads → linka [[03-Dominios/Java/Concorrência e paralelismo/11 - Java Memory Model em profundidade\|Java Memory Model]], sem re-explicar happens-before. |
| 03 | Garbage Collection — o conceito | O que é coleta de lixo (reachability, GC roots), weak generational hypothesis, minor/major/mixed collections, stop-the-world e safepoints, por que não chamar `System.gc()`; soft/weak/phantom references em visão geral. Conceito **sem** catálogo de coletores (vai na 06). |
| 04 | Bytecode por dentro — anatomia e javap | Anatomia do `.class` (magic number, constant pool, métodos, atributos), JVM stack-based vs register-based, instruções principais (`iload`/`istore`/`iadd`/`invokevirtual`/`invokestatic`/`invokedynamic`), inspeção com `javap -c -v`. `invokedynamic` cita lambdas → linka Galho 2 ([[04 - Lambdas e interfaces funcionais]]), sem re-explicar. |
| 05 | Classloading e o delegation model | Fases: loading → linking (verification, preparation, resolution) → initialization; hierarquia Bootstrap → Platform → Application; parent delegation e por que existe (proteger classes core); custom classloaders (app servers, plugins, hot reload); `ClassNotFoundException` vs `NoClassDefFoundError`. |

#### Adepto (5 notas — domínio operacional; 2 densas → opus)

| # | Nota | Escopo nuclear |
|---|------|----------------|
| 06 | Os coletores do HotSpot *(opus)* | Catálogo honesto e atualizado: Serial, Parallel, G1 (default desde Java 9 — JEP 248; regions, pause time target, mixed collections), ZGC **generational** (JEP 439, Java 21; modo non-generational deprecado/removido — confirmar JEP 490), Shenandoah (+ modo generational — confirmar JEP 404 e status), Epsilon (no-op, JEP 318). CMS: removido (JEP 363) — nota histórica. Tabela comparativa + escolha de primeira ordem (default G1; latência → ZGC; throughput batch → Parallel; heap mínimo → Serial). **Campo minado de versões — tudo via WebFetch.** |
| 07 | JIT — C1, C2 e tiered compilation *(opus)* | Interpretação vs compilação; C1 (client) e C2 (server); tiered compilation (níveis 0-4), profiling/invocation counters; otimizações do C2 (inlining, escape analysis, lock elision, dead code elimination, loop unrolling); **deoptimization** (e por que especulação compensa); warmup; por que benchmarks ingênuos mentem → JMH; code cache. Escape analysis toca alocação/boxing → linka Galho 2 ([[09 - Streams primitivos]]). |
| 08 | JPMS — o sistema de módulos | `module-info.java`; `requires`/`requires transitive`/`exports`/`exports...to`/`opens`; services (`uses`/`provides...with`); unnamed module e automatic modules (migração); strong encapsulation (saga `--illegal-access` até o default deny, `--add-opens`/`--add-exports`); `jlink` (menção como payoff). JPMS = Java 9 (JEP 261). |
| 09 | Flags, ergonomics e a JVM em containers | Categorias de flag (`-X` vs `-XX`, boolean vs valor); `-Xms`/`-Xmx`, `MetaspaceSize`/`MaxMetaspaceSize`; ergonomics (defaults derivados do hardware); **container awareness** (cgroups, `UseContainerSupport`, `MaxRAMPercentage` vs `-Xmx` em K8s/Docker); `-XX:+PrintFlagsFinal` pra descobrir o efetivo. Operação cotidiana de JVM containerizada. |
| 10 | GC logs — unified logging e leitura | Unified logging (`-Xlog`, JEP 158, Java 9 — sintaxe seletores:decoradores:output); anatomia de um log do G1 (pause young, mixed, to-space exhausted) e do ZGC; o que olhar: frequência, duração de pausa, taxa de promoção, humongous allocations, **Full GC como red flag**. Pré-requisito da nota 11. |

#### Magus (4 notas — maestria + decisão; 2 → opus)

| # | Nota | Escopo nuclear |
|---|------|----------------|
| 11 | Tuning de GC — metodologia e prática *(opus)* | O triângulo latency/throughput/footprint (escolha 2); metodologia disciplinada (baseline → meta explícita → mudar UMA flag → medir → repetir); tuning de G1 (`MaxGCPauseMillis`, `G1HeapRegionSize`, `InitiatingHeapOccupancyPercent`); tuning de ZGC (heap, `SoftMaxHeapSize`); quando **trocar** de coletor em vez de tunar; quando o problema **não é** GC (alocação excessiva, leak); anti-patterns (cargo cult flags copiadas de blog, tunar sem baseline, otimizar pausa que ninguém sente). |
| 12 | Diagnóstico — heap dumps, thread dumps e jcmd | `jcmd` como ferramenta canônica (`GC.heap_dump`, `Thread.print`, `VM.flags`, `GC.heap_info`, `VM.native_memory`); `jstat`/`jmap`/`jstack` (legado vivo); heap dump (`-XX:+HeapDumpOnOutOfMemoryError`, análise com Eclipse MAT: dominator tree, leak suspects, anatomia de um memory leak típico — cache sem bound, listener não removido); thread dumps (estados, deadlock detection); NMT (Native Memory Tracking). |
| 13 | JFR e JMC — observabilidade de produção | Java Flight Recorder: arquitetura de events, overhead baixo (~1%) que permite sempre-ligado em produção; OSS desde Java 11 (JEP 328 — confirmar); gravação via flags e `jcmd JFR.start/dump/stop`; análise no JDK Mission Control (JMC — projeto separado); JFR Event Streaming (JEP 349, Java 14); custom events (API `jdk.jfr`). Posicionamento vs profilers e vs APM. |
| 14 | Performance da JVM — síntese *(capstone, opus)* | Decision tree de coletor (consolidando 06/10/11); o eixo startup vs warmup vs peak performance; CDS/AppCDS e o caminho AOT (Project Leyden — JEP 483 Java 24, e JEPs subsequentes — confirmar status atual via WebFetch, hedge no que for preview); checklist de troubleshooting (OOM por área, latência alta, CPU alto); cheatsheet "qual nota pra qual problema". Cita o impacto de Virtual Threads na JVM (stacks no heap, carrier threads) → **linka** [[03-Dominios/Java/Concorrência e paralelismo/12 - Virtual Threads e Project Loom\|Virtual Threads]], não re-explica Loom. Liga o galho inteiro. |

**Decisões de fronteira (escopo NÃO coberto aqui ou de outro dono):**

- **Java Memory Model (happens-before, volatile, visibilidade, publicação segura)** → **Galho 4 é dono** (nota 11). Galho 3 é dono do *memory model de runtime* (layout de memória, alocação, GC). Notas 02/03 linkam `[[03-Dominios/Java/Concorrência e paralelismo/11 - Java Memory Model em profundidade|Java Memory Model]]` ao tocar visibilidade — **sem re-explicar**.
- **Virtual Threads / carrier threads / pinning / structured concurrency** → **Galho 4 é dono** (nota 12). Galho 3 pode citar impacto na JVM (nota 14); **linka, não re-explica**. A sub `### Project Loom e Virtual Threads` do tronco morre na poda (já era só um ponteiro).
- **Lambdas e `invokedynamic` como API** → Galho 2 (nota 04). A nota 04 deste galho explica a *instrução* `invokedynamic` e linka pra lá no uso em lambdas.
- **Boxing/alocação em streams** → Galho 2 (nota 09). A nota 07 (escape analysis) linka.
- **Generics/erasure, records, sealed** → Galho 1. Linkar quando exemplos usarem.
- **JMH como ferramenta de benchmark** → citado na nota 07 (por que existe), sem nota dedicada — profiling fino e benchmark de aplicação são do Galho 17 (Cloud-native e produção, futuro). Citação textual "Galho 17 (planejado)" **sem wikilink**.
- **GraalVM native image** → menção na 01/14 como existência; dono é o Galho 17 (futuro). Texto sem wikilink.
- **Galho 18 (OCP)** mapeará pros galhos 1-4 — não antecipar.

### 3.2. MOC do galho

`03-Dominios/Java/JVM/index.md`:
- `type: moc`, `status: growing`
- Frontmatter padrão (`title: "JVM por dentro"`, tags `java`/`jvm`/`moc`, aliases `["JVM", "Galho 3 - JVM por dentro"]`)
- TL;DR callout (galho cobre memória de runtime, GC, JIT, classloading, bytecode, JPMS, diagnóstico/JFR e performance)
- "Sobre este galho" + audiência primária/secundária + nota de que é galho de refator do tronco `Java Fundamentals` (poda da seção JVM)
- Conteúdo agrupado em 3 H2 (`## Iniciado` / `## Adepto` / `## Magus`) com wikilinks pras 14 notas (uma linha descritiva cada, no padrão dos MOCs dos Galhos 1/2/4/5)
- **Rotas alternativas (5):**
  - **Completa** — 01 → 14 em ordem
  - **Entrevista internacional** — 01 → 02 → 03 → 06 → 07 → 14 (pipeline, memória, GC conceito, coletores, JIT, síntese — o que mais cai)
  - **Sobrevivência em produção** — 09 → 10 → 12 → 13 → 11 (flags/containers, ler logs, diagnosticar, JFR, tunar)
  - **Por dentro do runtime** — 04 → 05 → 07 → 08 (bytecode, classloading, JIT, módulos)
  - **Tuning de memória e GC** — 02 → 03 → 06 → 10 → 11 (áreas, conceito, coletores, logs, tuning)
- "Veja também": MOC central `[[03-Dominios/Java/index|Trilha Java]]`, Galho 1 (Linguagem), Galho 2 (Collections/Streams), Galho 4 (Concorrência), Dicionário de Java, tronco `[[Java Fundamentals]]` (em transição)
- Dataview "Todas as notas do galho"

### 3.3. Dicionário de Java (EXPANSÃO — não recriar)

`03-Dominios/Java/Dicionário de Java.md` já existe (criado no Galho 1, expandido nos Galhos 2/4/5, `type: glossary`, seções alfabéticas). Este galho **expande** o arquivo inserindo os verbetes de JVM/GC/JIT/JPMS **em ordem alfabética case-insensitive (sem acento)** nas seções apropriadas, criando seções novas se necessário. **Nunca recriar o arquivo nem reordenar verbetes existentes.** Atualizar `updated:`.

Verbetes a inserir (~24-28, lista de referência — ajustar na execução conforme as âncoras reais das notas):

`bytecode`, `classloader (parent delegation)`, `code cache`, `deoptimization`, `Eden / Survivor spaces`, `Epsilon GC`, `ergonomics (JVM)`, `escape analysis`, `G1 GC`, `GC roots / reachability`, `geração (Young / Old)`, `heap`, `heap dump`, `inlining (JIT)`, `JFR (Java Flight Recorder)`, `jcmd`, `JIT (C1 / C2)`, `JMC (JDK Mission Control)`, `JPMS (module-info)`, `Metaspace`, `NMT (Native Memory Tracking)`, `safepoint`, `Shenandoah`, `stack frame`, `stop-the-world`, `tiered compilation`, `unified logging (-Xlog)`, `weak generational hypothesis`, `ZGC (generational)`.

Cada verbete: definição curta (1-3 linhas) em PT-BR + `Veja também:` apontando pra(s) nota(s) canônica(s). **Conferir 1:1** que os headings dos verbetes batem EXATAMENTE com as âncoras usadas nas notas (extrair as âncoras de Dicionário das notas e conferir, como nos galhos anteriores). Alguns termos podem já existir (ex: termos de threads são do Galho 4) — conferir antes de inserir pra não duplicar.

### 3.4. MOC central (ativação do Galho 3)

`03-Dominios/Java/index.md` já existe. Task **mínima**: trocar a **linha 27** (atualmente `3. JVM por dentro *(planejado)* — memory model, GC (G1/ZGC), JIT, classloading, bytecode, módulos (JPMS), tuning`) por um wikilink ativo no padrão das linhas 25/26/28/32:

```markdown
3. [[03-Dominios/Java/JVM/index|JVM por dentro]] — memória de runtime, GC (G1/ZGC/Shenandoah), JIT e tiered compilation, classloading, bytecode, módulos (JPMS), diagnóstico (JFR/jcmd) e tuning
```

Atualizar `updated:`. Não mexer no resto do MOC central. (Reconfirmar o número da linha na execução — editar por conteúdo.)

### 3.5. Poda da seção JVM do tronco

`Core/Java Fundamentals.md`. O pré-flight (§6) confirmou que a seção `## JVM (Java Virtual Machine)` (linhas ~33-225) está marcada `[!info] Migra em galho futuro (Galho 3)` e é exatamente o escopo deste galho. Vira callout no padrão de poda do roadmap (§9):

```markdown
## JVM (Java Virtual Machine)

> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Java/JVM/index|JVM por dentro]]. Veja [[01 - A JVM — o que é e o pipeline de execução]], [[02 - Áreas de memória de runtime]], [[03 - Garbage Collection — o conceito]], [[06 - Os coletores do HotSpot]], [[07 - JIT — C1, C2 e tiered compilation]].
```

A poda absorve **todas** as subseções (`### Pipeline de compilação e execução`, `### Bytecode — uma olhada`, `### Memory areas`, `### Garbage Collection`, `### Como escolher GC`, `### JIT Compiler`, `### Classloader`, `### Project Loom e Virtual Threads` — esta última já era só ponteiro pro Galho 4 e morre sem substituição própria).

**NÃO podar:**
- `## Concorrência (visão geral)` → dívida de poda do **Galho 4** (marcada `[!info] Migra em galho futuro (Galho 4)`). **Não é escopo deste galho.** Deixar como está.
- As seções `[!nota] Migrado` dos Galhos 1 e 2 — já podadas.
- A cauda (`## Armadilhas comuns`, `## Na prática`, `## Como explicar em inglês`, `## Recursos`, `## Veja também`) — já higienizada pelo Galho 2; conferir que a poda não a afeta.

**Higienização:** a seção JVM está limpa de 1ª pessoa e de exemplos com sabor de cliente (pré-flight §6) — a poda absorve o corpo inteiro, nada adicional a higienizar. Se a execução encontrar fabricação residual em outro ponto do tronco, higienizar conforme [[feedback_no_fabrication]].

**Atualizar** `updated:` do tronco e conferir o "Veja também" (adicionar link pro galho novo). Não apagar histórico Git.

### 3.6. Destino do tronco `Java Fundamentals` (decisão registrada, execução diferida)

Após a poda deste galho, o tronco fica: intro + ~17 callouts de migração + `## Concorrência (visão geral)` (dívida do Galho 4) + cauda. **Decisão apresentada e aprovada no brainstorming:**

- **Neste galho:** apenas a poda da seção JVM. O tronco **não** vira MOC ainda — a dívida do Galho 4 ainda mora nele.
- **Depois (fora deste galho):** quando a dívida do Galho 4 for quitada (tarefa própria de fechamento), converter `Java Fundamentals` em **nota-resumo enxuta** — intro + mapa de callouts apontando pros galhos + Recursos —, `status: evergreen`, **sem deletar o arquivo** (wikilinks externos apontam pra ele; histórico preservado).

### 3.7. Reciprocidade de links (Galho 3 ↔ vizinhos)

As notas do Galho 3 que tocam fronteira linkam os donos (mão dupla; os galhos vizinhos já fecharam, então não há dívida de linkback a quitar — só links de ida):
- Notas 02, 03 → `[[03-Dominios/Java/Concorrência e paralelismo/11 - Java Memory Model em profundidade|Java Memory Model]]`.
- Nota 14 → `[[03-Dominios/Java/Concorrência e paralelismo/12 - Virtual Threads e Project Loom|Virtual Threads]]` (confirmar título exato da nota na execução).
- Nota 04 → `[[03-Dominios/Java/Collections e Streams/04 - Lambdas e interfaces funcionais|Lambdas]]` (invokedynamic).
- Nota 07 → `[[03-Dominios/Java/Collections e Streams/09 - Streams primitivos|Streams primitivos]]` (boxing/alocação).

Dívida de linkback REVERSA a verificar na execução: os Galhos 1/2/4 podem ter texto "Galho 3 (JVM), planejado" esperando virar wikilink (o Galho 2 cravou esse padrão em §3.1 do spec dele). **Grep por "Galho 3" nas pastas dos galhos fechados** e quitar o que for ponteiro textual → wikilink pra nota real correspondente.

## 4. Convenções por nota

Herda §7 do roadmap e §4 dos specs dos Galhos 1/2/4/5. Reforços específicos:

### 4.1. Frontmatter

```yaml
---
title: "<título>"
created: 2026-06-05
updated: 2026-06-05
type: concept
progress: backlog
status: seedling
publish: true
fase: iniciado | adepto | magus
tags:
  - java
  - jvm
  - <fase>
  - <tags específicas: gc, jit, bytecode, classloading, jpms, tuning, diagnostico, jfr, memoria>
aliases:
  - <aliases opcionais>
---
```

### 4.2. Estrutura H2 obrigatória

- `> [!abstract] TL;DR` (callout, NÃO H2)
- `## O que é` / `## Por que importa` / `## Como funciona` (≥3 subseções em notas Adepto/Magus)
- `## Na prática` — exemplos compiláveis/executáveis (código Java, comandos `java`/`jcmd`/`javap` com output realista em ` ```text `); framing neutro ("padrão observado em serviços enterprise", "caso típico de JVM containerizada"); NUNCA "no meu projeto"
- `## Armadilhas` — **≥2** (Iniciado) / **≥3** (Adepto/Magus), cada uma com descrição + exemplo curto demonstrando o problema + fix em 1 linha
- `## Em entrevista` — subheading `### Frase pronta (inglês)` com frase de **3+ sentenças** (trade-off + decisão + caveat) + vocabulário **6+ termos PT→EN**
- `## Veja também` — wikilinks **SEM backticks**; sempre inclui notas relacionadas do galho + `[[03-Dominios/Java/JVM/index|MOC do galho]]` + `[[03-Dominios/Java/index|Trilha Java]]` + (quando o conceito conectar) Galhos 1/2/4 + verbetes do Dicionário. **Evitar âncoras same-file `[[#Heading]]`** (falso-positivo no checker).
- `## Referências` — docs oficiais (Oracle JVM Guide/GC Tuning Guide, Javadoc, dev.java), JEPs quando relevantes (openjdk.org costuma dar 403 no WebFetch — citar como referência é ok, verificar conteúdo via fallback Oracle/dev.java).

### 4.3. Restrições absolutas

1. **Sem fabricação** de experiência pessoal. Exemplos neutros (`Order`, `Customer`, `Product`, serviço hipotético explícito `// hipotético:`). **NUNCA** `Patient`/`getSpecialty`, `josenaldo`, nem casos vividos.
2. **GC é campo minado de versões — WebFetch obrigatório** pra toda alegação version-specific antes de afirmar: G1 default (JEP 248, Java 9), ZGC production (JEP 377, Java 15), **ZGC generational (JEP 439, Java 21)**, ZGC non-generational deprecado (JEP 490 — confirmar versão), Shenandoah (JEP 379) + generational (JEP 404 — confirmar status), CMS removido (JEP 363, Java 14), Epsilon (JEP 318, Java 11), JPMS (JEP 261, Java 9), JFR OSS (JEP 328, Java 11), JFR streaming (JEP 349, Java 14), unified logging (JEP 158, Java 9), CDS/AppCDS e Project Leyden (JEP 483+ — confirmar status atual e hedge no que for preview). Nada de "de memória". Fontes: docs.oracle.com (JVM Guide, GC Tuning Guide), dev.java, Javadoc; JEPs no openjdk.org dão 403 no WebFetch — usar fallbacks.
3. **Conteúdo herdado do tronco é matéria-prima, não cópia** — o esqueleto está correto mas a tabela de GC está desatualizada (CMS sem nota de remoção, ZGC sem generational). As notas expandem e modernizam.
4. **Code samples e comandos verificáveis** — Java moderno onde houver código; comandos de CLI (`java -XX:...`, `jcmd`, `javap`, `jstat`) com flags reais conferidas; outputs ilustrativos marcados como ` ```text `. Code fences sempre fechadas.
5. **Comparações justas** — ao comparar (G1 vs ZGC, JIT vs AOT, jcmd vs ferramentas legadas), incluir "quando X" E "quando Y". A capstone (14) é o ápice dessa exigência.
6. **Wikilinks sem backticks** em "Veja também"; MOC do galho + MOC central obrigatórios. **Não linkar galhos inexistentes** (6, 17...) — usar texto "planejado".
7. **`fase:` no frontmatter + na tag** — obrigatório.
8. **Higiene de commits** — sem `Co-Authored-By: Claude` ([[feedback_commits]]), sem `--no-verify`, `git add <path>` nominal (nunca `-A` — bot de backup do vault roda em timer), **1 commit por nota**, controlador commita (subagents write-only). **Direto na `main`** ([[feedback_galhos_direto_main]]); **push é manual do usuário** — não pushar. Não fazer deploy.
9. **Tom pedagógico graduado** — Iniciado assume pouco; Magus assume domínio dos anteriores e dos Galhos 1/2.

## 5. Conteúdo por nota (síntese)

Esboço do recorte. Fontes-base: Oracle JVM Guide + GC Tuning Guide (docs.oracle.com), dev.java, Javadoc (`java.lang.instrument`, `jdk.jfr`), The Java Tutorials, JEPs (248, 261, 318, 328, 349, 363, 377, 379, 404, 439, 483, 490 — verificar via fallback).

- **01 — A JVM — o que é e o pipeline de execução.** JVM/JRE/JDK, WORA, pipeline completo, HotSpot, menção a OpenJ9/GraalVM. Armadilhas: confundir bytecode com código nativo ("Java é interpretado" — meia-verdade); assumir mesma JVM = mesmo comportamento entre vendors/versões. Fonte: dev.java, Oracle JVM Guide.
- **02 — Áreas de memória de runtime.** Heap (Eden/S0/S1/Old, humongous), Metaspace vs PermGen, stacks, PC, native, code cache; mapa de OOM por área. Linka JMM (Galho 4) pra visibilidade. Armadilhas: achar que `-Xmx` limita toda a memória do processo (native/metaspace ficam fora); `OutOfMemoryError: Metaspace` por leak de classloader; recursão profunda → `StackOverflowError` (e `-Xss`). Fonte: Oracle JVM Guide, GC Tuning Guide (generations).
- **03 — Garbage Collection — o conceito.** Reachability/GC roots, generational hypothesis, minor/major/mixed, STW/safepoints, `System.gc()`, references API em visão geral. Armadilhas: chamar `System.gc()` em produção; segurar referências em cache estático (leak "na frente do GC"); confundir GC com gerenciamento de recursos nativos (use try-with-resources → linka Galho 1). Fonte: GC Tuning Guide.
- **04 — Bytecode por dentro — anatomia e javap.** `.class`, constant pool, stack-based, instruções, `javap -c -v`, `invokedynamic` (lambdas → Galho 2). Armadilhas: otimizar "lendo bytecode" sem medir (JIT transforma tudo — linka 07); confundir versão de bytecode com versão da linguagem (`--release`); assumir 1 linha de código = 1 instrução. Fonte: javap docs, JVM Spec (visão geral).
- **05 — Classloading e o delegation model.** Load/link/init, hierarquia, parent delegation, custom classloaders, `ClassNotFoundException` vs `NoClassDefFoundError`. Armadilhas: mesma classe carregada por 2 classloaders ≠ mesma classe (`ClassCastException` "impossível"); leak de classloader em redeploy (metaspace OOM — linka 02); depender de ordem de inicialização estática. Fonte: Oracle docs, dev.java.
- **06 — Os coletores do HotSpot (opus).** Catálogo completo atualizado + tabela + escolha de primeira ordem. **WebFetch pesado** (JEPs 248/318/363/377/379/404/439/490). Armadilhas: copiar escolha de coletor de blog de 2015 (CMS!); ativar ZGC esperando milagre em heap minúsculo; ignorar que low-pause cobra em CPU/footprint; tabela do tronco como contraexemplo do que atualizar. Fonte: GC Tuning Guide, JEPs.
- **07 — JIT — C1, C2 e tiered compilation (opus).** Tiered (níveis), profiling, otimizações C2, deoptimization, warmup, JMH, code cache. Armadilhas: microbenchmark sem JMH (dead code elimination mente); medir performance no warmup; `synchronized` "lento" sem considerar lock elision; flag `-Xcomp`/`-Xint` em produção. Fonte: Oracle JVM Guide, dev.java, JMH docs.
- **08 — JPMS — o sistema de módulos.** module-info, requires/exports/opens, services, unnamed/automatic, strong encapsulation, jlink. Armadilhas: `opens` esquecido pra framework de reflection (Hibernate/Jackson quebram); automatic module name instável (sem `Automatic-Module-Name` no manifest); split packages; achar que classpath morreu (unnamed module convive). Fonte: JEP 261 (fallback), dev.java, Oracle docs.
- **09 — Flags, ergonomics e a JVM em containers.** -X/-XX, heap/metaspace flags, ergonomics, container awareness, MaxRAMPercentage, PrintFlagsFinal. Armadilhas: `-Xmx` fixo em pod com limite de memória menor (OOMKilled pelo kernel, não OOM da JVM); confiar no default de `MaxRAMPercentage` (25%) em container dedicado; flag copiada sem conferir se existe na versão (`PrintFlagsFinal` pra checar). Fonte: Oracle docs (java command reference), container support docs.
- **10 — GC logs — unified logging e leitura.** `-Xlog` (JEP 158), anatomia de log G1/ZGC, sinais (frequência, pausas, promoção, humongous, Full GC). Armadilhas: rodar produção sem GC log (overhead ~zero, informação impagável); ler só a pausa média e ignorar percentis/Full GC; sintaxe antiga (`-XX:+PrintGCDetails`) em Java 9+ (removida/aliased). Fonte: JEP 158 (fallback), Oracle docs.
- **11 — Tuning de GC — metodologia e prática (opus).** Triângulo, metodologia 1-flag-por-vez, tuning G1/ZGC, quando trocar de coletor, quando não é GC. Armadilhas: cargo cult flags; tunar sem baseline/meta; `MaxGCPauseMillis` agressivo demais (throughput despenca); "resolver" leak com heap maior (adia o OOM). Fonte: GC Tuning Guide (capítulos G1/ZGC).
- **12 — Diagnóstico — heap dumps, thread dumps e jcmd.** jcmd canônico, jstat/jmap/jstack, heap dump + MAT (dominator tree, leak suspects), thread dumps, NMT. Armadilhas: heap dump em produção sem avisar (STW + arquivo gigante — saber o custo antes); analisar dump na máquina de produção (copiar pra fora); esquecer `HeapDumpOnOutOfMemoryError` (o OOM acontece e a evidência morre com o pod); ler thread dump único (precisa de série). Fonte: Oracle troubleshooting guide, jcmd docs.
- **13 — JFR e JMC — observabilidade de produção.** JFR events, overhead ~1%, sempre-ligado, jcmd JFR.*, JMC, streaming (JEP 349), custom events. Armadilhas: confundir JFR (coleta) com JMC (análise — projeto separado, download próprio); gravação `maxage`/`maxsize` sem limite (disco); achar que JFR substitui APM/tracing distribuído (complementa). Fonte: JEP 328/349 (fallback), Oracle JFR docs, jdk.jfr Javadoc.
- **14 — Performance da JVM — síntese (capstone, opus).** Decision tree de coletor; startup vs warmup vs peak; CDS/AppCDS, Project Leyden/AOT (status via WebFetch, hedge se preview); checklist de troubleshooting; cheatsheet do galho. Virtual Threads: impacto citado, link Galho 4. Armadilhas (de raciocínio): otimizar sem medir; escolher coletor por hype; tratar JVM como caixa preta até o incidente; ignorar startup/warmup em workload serverless. Fonte: síntese + docs Leyden/CDS.

## 6. Pré-flight (executado nesta fase de brainstorming)

1. **Headings reais confirmados** em `Core/Java Fundamentals.md`: seção `## JVM (Java Virtual Machine)` (linhas ~33-225) com subseções `### Pipeline de compilação e execução`, `### Bytecode — uma olhada`, `### Memory areas`, `### Garbage Collection`, `### Como escolher GC`, `### JIT Compiler`, `### Classloader`, `### Project Loom e Virtual Threads`. Marcada `[!info] Migra em galho futuro (Galho 3)`.
2. **Podas anteriores confirmadas:** todas as seções dos Galhos 1 e 2 já são callouts `[!nota] Migrado`. Após a poda deste galho, resta apenas `## Concorrência (visão geral)` (dívida do Galho 4) como seção cheia.
3. **`## Concorrência (visão geral)` NÃO é deste galho** — dívida do Galho 4; intocada.
4. **Fabricação:** seção JVM limpa (sem 1ª pessoa, sem `Patient`); cauda do tronco já higienizada pelo Galho 2. Nada adicional identificado.
5. **Tronco desatualizado como matéria-prima:** tabela de GC cita CMS sem remoção, ZGC "Java 15" sem generational, sem Shenandoah generational — reescrever com WebFetch, não copiar.
6. **Verificações version-specific a fazer na execução (WebFetch):** ver §4.3.2 (lista de JEPs). Pontos cravados em [[project_trilha_java]] que valem aqui: ZGC generational = Java 21 (JEP 439).
7. **Dívida reversa a verificar:** grep "Galho 3" nos galhos fechados (1/2/4/5) — ponteiros textuais "Galho 3 (JVM), planejado" viram wikilinks pras notas novas (§3.7).

Quando faltar fato verificável, **PERGUNTAR** antes de escrever.

## 7. Critérios de aceitação do galho

Além dos critérios gerais (§10 do roadmap):

1. 14 notas em `03-Dominios/Java/JVM/`, frontmatter completo com `fase:`, `publish: true`, distribuídas 5/5/4.
2. MOC do galho com 3 subseções de fase + 5 rotas alternativas + dataview + folder-link resolve (`index.md` presente).
3. Dicionário de Java **expandido** (não recriado) com ~24-28 verbetes em ordem alfabética; verbetes dos Galhos 1/2/4/5 intactos; `updated` atualizado; headings dos verbetes conferidos 1:1 com as âncoras usadas nas notas; sem duplicar verbetes pré-existentes.
4. MOC central `Java/index.md` com Galho 3 ativado (linha do item 3 vira wikilink); resto intacto.
5. **Poda executada:** a seção `## JVM (Java Virtual Machine)` do tronco vira callout com wikilinks; `## Concorrência (visão geral)` intacta; cauda intacta; `updated` do tronco atualizado.
6. **Dívida reversa quitada:** ponteiros textuais "Galho 3 (planejado)" nos galhos 1/2/4/5 viram wikilinks (os que existirem no grep).
7. Cada nota: TL;DR; 3-5 code samples/comandos; "Em entrevista" com `### Frase pronta (inglês)` 3+ sentenças + 6+ termos PT→EN; "Armadilhas" com exemplo+fix (≥2 Iniciado, ≥3 Adepto/Magus); wikilinks (galho + MOC central + Galhos 1/2/4 quando conectar + Dicionário); "Referências" com docs oficiais.
8. Zero fabricação de experiência pessoal; exemplos neutros; alegações version-specific verificadas via WebFetch (nada de API/flag/JEP "de memória").
9. 1 commit por nota; sem `Co-Authored-By: Claude`; sem `--no-verify`; stage nominal por arquivo; **direto na `main`, sem push, sem deploy**.
10. `verificar-wikilinks` roda limpo na pasta do galho e nos arquivos editados fora dela (tronco, MOC central, Dicionário, notas com dívida reversa); sem âncoras same-file; Quartz publica sem erros.

## 8. Riscos e mitigações

| Risco | Mitigação |
|---|---|
| Versões/status de GC errados (ZGC generational, Shenandoah, CMS, Leyden) | WebFetch obrigatório por alegação (§4.3.2); hedge explícito no que for preview/experimental; openjdk.org 403 → fallback Oracle/dev.java. |
| Copiar a tabela de GC desatualizada do tronco | Tronco declarado matéria-prima desatualizada (§3.5, pré-flight 5); nota 06 reconstrói do zero com fontes. |
| Invadir o JMM (Galho 4) ao falar de memória | Fronteira nuclear cravada (§1, §3.1): runtime memory ≠ JMM; notas 02/03 linkam, não explicam happens-before. |
| Re-explicar Virtual Threads na nota 14 | Fronteira: citar impacto + wikilink Galho 4 (12); critério 7. |
| Podar `## Concorrência` por engano | Pré-flight fixou: só a seção JVM é podada; Concorrência é dívida do Galho 4, explicitamente intocada (§3.5). |
| Comandos/flags inventados (jcmd, -Xlog, MAT) | Flags conferidas em docs oficiais via WebFetch; outputs marcados como ilustrativos (` ```text `). |
| Galho denso inflar notas individuais | Tópicos pesados distribuídos (GC em 03/06/10/11; JIT isolado em 07; diagnóstico em 12/13); se inflar, dividir nota, não galho ([[feedback_notas_atomicas]]). |
| Race com bot de backup do vault (index.lock, commits alheios) | Padrão do Galho 2: subagents write-only; controlador commita logo após cada nota com `git add <path>` nominal; nunca `-A`. |
| Quebrar wikilinks ao podar | Tronco continua existindo (poda = callout); `verificar-wikilinks` roda ao fim em tudo que foi tocado. |
| Duplicar verbete no Dicionário | Conferir cada verbete contra o arquivo antes de inserir; nunca reordenar/recriar. |

## 9. Próximos passos

1. **Aprovação deste spec** ✅ (mapa aprovado no brainstorming em 2026-06-05)
2. **Plano de execução** via skill `superpowers:writing-plans` → `docs/superpowers/plans/2026-06-05-java-galho-03-jvm-execution.md`
3. **Execução** via `superpowers:subagent-driven-development` **direto na `main`** (1 subagente write-only por nota; sonnet, opus pras notas 06/07/11/14; review **por fase** + fix loop; controlador commita)
4. **Poda** da seção JVM do tronco + **quitação da dívida reversa** (grep "Galho 3")
5. **Verificação** de wikilinks + conferência de âncoras do Dicionário
6. **Revisão do roadmap** com aprendizados antes do próximo galho

## 10. Documentos relacionados

- `2026-06-02-java-senior-roadmap-design.md` — roadmap macro (18 galhos)
- `2026-06-02-java-galho-01-linguagem-design.md` / `...-execution.md` — Galho 1
- `2026-06-04-java-galho-02-collections-streams-design.md` / `...-execution.md` — Galho 2 (refator de tronco — template direto deste)
- `2026-06-03-java-galho-04-concorrencia-design.md` / `...-execution.md` — Galho 4 (dono do JMM e de Virtual Threads)
- `2026-06-03-java-galho-05-swing-design.md` / `...-execution.md` — Galho 5
- Tronco a podar: `03-Dominios/Java/Core/Java Fundamentals.md` (seção JVM)
- Artefatos a atualizar: `03-Dominios/Java/Dicionário de Java.md`, `03-Dominios/Java/index.md`, notas dos galhos 1/2/4/5 com ponteiro textual "Galho 3"
- Fontes-base: Oracle JVM Guide + GC Tuning Guide, dev.java, Javadoc (`jdk.jfr`), JEPs 158, 248, 261, 318, 328, 349, 363, 377, 379, 404, 439, 483, 490 (openjdk.org 403 → fallback)
- Memórias: [[project_trilha_java]], [[project_trilhas_fases_aprendizado]], [[project_tronco_galhos_pattern]], [[feedback_no_fabrication]], [[feedback_quartz_index]], [[feedback_commits]], [[feedback_galhos_direto_main]], [[feedback_notas_atomicas]]
