---
title: "Gradle — performance, build cache e daemon"
created: 2026-06-11
updated: 2026-06-11
type: concept
status: seedling
publish: true
fase: Iniciado
tags:
  - java
  - build
  - iniciado
  - gradle
aliases:
  - "build cache"
  - "Gradle daemon"
---

# Gradle — performance, build cache e daemon

> [!abstract] TL;DR
> A reputação de "Gradle é rápido" não é magia: é a soma de quatro mecanismos que **evitam refazer trabalho**. O **incremental build** pula tasks cujos inputs não mudaram (`UP-TO-DATE`). O **build cache** vai além e reusa *outputs* de tasks de builds anteriores — local ou remoto, até entre máquinas e CI (`FROM-CACHE`). A **configuration cache** cacheia a própria fase de configuração (o task graph) — é o "preferred mode of execution" desde o **Gradle 9.0**, mas ainda é **opt-in, não default**. E o **daemon** mantém uma JVM "quente" viva entre builds, eliminando o custo de startup. O Maven não tem equivalente nativo a esses dois últimos por causa do seu modelo de execução diferente.

## O que é

Esses quatro mecanismos são as **otimizações de performance** que o Gradle aplica para que cada build faça o mínimo de trabalho possível. A ideia central é simples e se repete em camadas: **se nada relevante mudou, não refaça**.

- **Incremental build** — granularidade de *task*: pula a execução de uma task individual se suas entradas e saídas estão idênticas à última vez.
- **Build cache** — granularidade de *output*: em vez de só pular, *recupera* o resultado já computado de um cache (mesmo de outra máquina).
- **Configuration cache** — granularidade da *fase de configuração*: cacheia o resultado de montar o task graph, pulando a configuração inteira.
- **Daemon** — granularidade do *processo*: mantém a JVM viva entre builds para não pagar startup e JIT toda hora.

Cada um ataca uma fonte diferente de lentidão. Juntos, fazem o build incremental do dia a dia ser muito mais barato que um build do zero.

## Por que importa

Build lento é imposto que você paga em **cada commit, cada PR, cada rodada de CI**. Em projetos grandes, o ciclo de feedback (editar → compilar → testar) domina o tempo do desenvolvedor. Esses mecanismos são o principal argumento de venda do Gradle frente ao Maven.

Numa entrevista de Java senior, a pergunta não é "o Gradle é rápido?" — é "**por que** ele é rápido, e quando isso quebra?". Saber distinguir incremental build de build cache, e entender que a configuration cache ainda é opt-in, mostra que você conhece a ferramenta de verdade, não só de ouvir falar. E saber as **armadilhas** (task que não cacheia, daemon desligado) mostra que você já apanhou em produção.

## Como funciona

### Incremental build e up-to-date checking

Toda task declara seus **inputs** e **outputs** — via anotações em tasks customizadas (`@Input`, `@InputFiles`, `@OutputDirectory`, `@OutputFile`...) ou via API de runtime (`task.inputs` / `task.outputs`).

Antes de executar, o Gradle gera um **fingerprint** dos inputs (caminhos de arquivo + hashes de conteúdo) e dos outputs. Na execução seguinte, ele recalcula o fingerprint e compara com o anterior:

- Se os fingerprints são **iguais**, o Gradle assume que os outputs estão atualizados e **pula a task** — ela aparece como `UP-TO-DATE` no console.
- Se algo mudou (um arquivo de input, o código da própria task), a task roda de novo.

O Gradle rastreia até mudanças na implementação da task. Anotações especializadas como `@Classpath` ignoram ruído irrelevante (timestamps e metadados de JAR), evitando re-execução desnecessária.

> [!info] Pré-requisito: declarar outputs
> Incremental build exige **pelo menos um output declarado**. Sem output, o Gradle não tem o que comparar e roda a task sempre.

### Build cache (local e remoto)

O incremental build só pula uma task quando os outputs **daquela árvore de trabalho** ainda estão lá. O **build cache** é mais poderoso: armazena os outputs de tasks indexados por uma **chave de hash dos inputs**, permitindo *recuperar* um resultado já computado — mesmo que você nunca o tenha gerado nesta máquina.

A chave de cache combina, entre outras coisas: o tipo da task, o classpath, os nomes das propriedades de input/output e os **valores dos inputs**. Detalhe importante: **o caminho da task não entra na chave** — então tasks idênticas em locais diferentes compartilham a mesma entrada de cache.

Há dois níveis:

- **Local** — um diretório (por padrão dentro do Gradle User Home) que guarda outputs entre builds na mesma máquina.
- **Remoto** — tipicamente um cache HTTP compartilhado. O Gradle tenta primeiro o cache local; se não acha, tenta o remoto; se acha lá, também grava no local.

A doc oficial afirma que, com um cache compartilhado, o reuso de outputs **funciona até entre máquinas de desenvolvedores e agentes de build (CI)**. O padrão recomendado: o servidor de CI *popula* o cache a partir de builds limpos, e os desenvolvedores apenas *leem* dele.

Uma task que aparece `FROM-CACHE` no console teve seu output baixado do cache em vez de recomputado.

### Configuration cache e o daemon

Todo build do Gradle tem duas fases: **configuração** (avaliar os scripts, montar o *task graph*) e **execução** (rodar as tasks). O incremental build e o build cache otimizam a *execução*. A **configuration cache** otimiza a *configuração*.

Ela armazena o resultado da fase de configuração — captura o task graph já montado para um dado conjunto de tasks. Em builds seguintes com os mesmos inputs de configuração, o Gradle **pula a configuração inteira** e vai direto para a execução, além de permitir mais paralelismo.

> [!important] Estado oficial (re-confirmado nesta nota)
> Desde o **Gradle 9.0.0**, a configuration cache é o **"preferred mode of execution"**. Mas ela **não é habilitada por default** — continua **opt-in**. A doc avisa que nem todos os plugins core e features são suportados ainda, e que seu build pode precisar de ajustes para ser compatível.

O **daemon** é uma peça à parte: um processo JVM de longa duração que fica vivo *entre* builds. Em vez de subir uma JVM nova a cada `gradle build` (e pagar startup + aquecimento do JIT), o Gradle reaproveita um daemon já quente.

> [!tip] Analogia: o forno que fica ligado
> Sem daemon, cada build é como **acender o forno do zero** toda vez que você vai assar um pão: você espera ele esquentar antes de qualquer coisa útil acontecer. O daemon é **deixar o forno ligado em fogo baixo** entre uma fornada e outra — quando chega a próxima massa, ele já está na temperatura. A JVM "quente" do daemon já tem classes carregadas e código compilado pelo JIT.

E o Maven? O modelo de execução do Maven é diferente: ele sobe uma JVM por invocação e não mantém um grafo de tasks configurável da mesma forma. Não há daemon nativo nem configuration cache equivalente no Maven padrão — por isso o `mvn` paga o custo de startup a cada chamada.

## Na prática

Rodar duas vezes seguidas deixa os mecanismos visíveis no console. Primeira vez, tudo executa:

```bash
$ gradle build
> Task :app:compileJava
> Task :app:processResources
> Task :app:classes
> Task :app:jar
> Task :app:test
> Task :app:build

BUILD SUCCESSFUL in 8s
```

Segunda vez, sem mudar nada — incremental build entra em ação:

```bash
$ gradle build
> Task :app:compileJava UP-TO-DATE
> Task :app:processResources UP-TO-DATE
> Task :app:classes UP-TO-DATE
> Task :app:jar UP-TO-DATE
> Task :app:test UP-TO-DATE
> Task :app:build UP-TO-DATE

BUILD SUCCESSFUL in 1s
```

Com o build cache ligado, num clone novo ou em CI, os outputs vêm do cache em vez de serem recomputados:

```bash
$ gradle build --build-cache
> Task :app:compileJava FROM-CACHE
> Task :app:test FROM-CACHE
> Task :app:build

BUILD SUCCESSFUL in 2s
```

Para ligar de forma permanente (em vez da flag por build), use o `gradle.properties` na raiz do projeto:

```properties
# gradle.properties

# build cache: reusa outputs de tasks entre builds e máquinas
org.gradle.caching=true

# configuration cache: cacheia o task graph (preferred mode desde 9.0, opt-in)
org.gradle.configuration-cache=true

# daemon: mantém a JVM quente entre builds (ligado por padrão; explícito aqui)
org.gradle.daemon=true
```

Cache remoto é configurado no `settings.gradle(.kts)` apontando para um cache HTTP compartilhado — útil para o time inteiro e o CI dividirem outputs.

## Armadilhas

### (1) Task não-cacheável por output não-declarado

Se uma task **não declara nenhum output** (ou declara inputs/outputs incompletos), o Gradle não consegue fazer up-to-date checking nem cachear: ela **roda toda vez**. Pior: tasks com *validation warnings* (propriedade sem anotação, getter não anotado) são executadas **sem nenhuma otimização** — sem cache, sem paralelismo.

O sintoma é uma task customizada que nunca aparece `UP-TO-DATE` por mais que você não mude nada. A correção é declarar corretamente os inputs e outputs (anotações `@Input`/`@OutputFile`/... ou a API `inputs`/`outputs`). Se a task realmente não tem outputs em arquivo e gerencia o próprio estado, há `@UntrackedTask` / `doNotTrackState()` — mas isso é exceção, não a regra.

### (2) Desligar o daemon em dev (a lentidão silenciosa)

Vez ou outra alguém roda `--no-daemon` ou seta `org.gradle.daemon=false` no `gradle.properties` "para resolver um problema estranho" — e esquece de reverter. O efeito: **toda** invocação passa a pagar o custo de subir uma JVM nova e aquecer o JIT do zero, build após build. O ciclo de feedback fica visivelmente mais lento sem causa aparente.

A regra prática: **em dev, deixe o daemon ligado** (é o padrão). `--no-daemon` faz sentido pontual em CI efêmero (onde cada job é uma máquina descartável e o daemon não seria reaproveitado mesmo), mas é a escolha errada para o loop de desenvolvimento local.

## Em entrevista

### Frase pronta (inglês)

> Gradle's performance story rests on avoiding redundant work at several levels. Incremental build skips a task when its declared inputs and outputs are unchanged, marking it `UP-TO-DATE`, while the build cache goes further and restores task outputs by an input-hash key — even across machines and CI when you use a shared remote cache. On top of that, the configuration cache caches the configuration phase itself, capturing the task graph; it has been the preferred mode of execution since Gradle 9.0, though it's still opt-in rather than the default. Finally, the daemon keeps a warm JVM alive between builds so you don't pay startup and JIT cost every time, which is something Maven's execution model doesn't offer natively.

### Vocabulário

| Termo PT | Termo EN |
| --- | --- |
| pular tasks cujos inputs/outputs não mudaram (`UP-TO-DATE`) | Incremental build |
| comparar fingerprints de inputs/outputs para decidir se a task roda | Up-to-date checking |
| reusar *outputs* de tasks indexados por hash dos inputs (`FROM-CACHE`); local ou remoto | Build cache |
| cachear a fase de configuração / o task graph; preferred mode desde 9.0, opt-in | Configuration cache |
| processo JVM persistente que fica "quente" entre builds, evitando custo de startup | Daemon |
| propriedades declaradas (anotações ou API) que alimentam fingerprint e chave de cache | Task inputs/outputs |
| hash derivado de tipo da task, classpath e valores dos inputs (o caminho da task *não* entra) | Cache key |
| montar o task graph vs rodar as tasks; cada cache otimiza uma fase | Configuration phase vs execution phase |

## Veja também

- [[03-Dominios/Tecnologia/Java/Build e tooling/05 - Gradle — build script, tasks e configurations|Gradle — o modelo]]
- [[03-Dominios/Tecnologia/Java/Build e tooling/06 - Gradle — dependências, Version Catalogs e o wrapper|Gradle — dependências]]
- [[03-Dominios/Tecnologia/Java/Build e tooling/08 - Maven vs Gradle — trade-offs honestos|Maven vs Gradle]]
- [[03-Dominios/Tecnologia/Java/Build e tooling/index|Build, tooling e ecossistema (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]

## Referências

- Gradle User Guide — Incremental Build. https://docs.gradle.org/current/userguide/incremental_build.html
- Gradle User Guide — Build Cache. https://docs.gradle.org/current/userguide/build_cache.html
- Gradle User Guide — Configuration Cache. https://docs.gradle.org/current/userguide/configuration_cache.html
