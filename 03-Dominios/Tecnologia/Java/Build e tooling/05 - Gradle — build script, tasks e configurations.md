---
title: "Gradle — build script, tasks e configurations"
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
  - "Gradle — o modelo"
  - "Kotlin DSL"
---

# Gradle — build script, tasks e configurations

> [!abstract] TL;DR
> Gradle descreve o build como um **programa**, não como um documento. O `build.gradle.kts` (Kotlin DSL — o **default recomendado desde Gradle 8.0**) é um script real, com autocomplete e checagem de tipos na IDE; o `build.gradle` em Groovy continua válido e **não está deprecado**. Esse script declara **tasks** (unidades de trabalho) que Gradle organiza num **grafo acíclico dirigido (DAG)** via `dependsOn`, executando dependências antes do alvo. Cada task declara **inputs e outputs**, e é isso que permite a Gradle pular trabalho que já está atualizado (incremental, ver nota 07). Dependências entram em **configurations** — baldes por escopo, como `implementation`, `api`, `compileOnly`, `runtimeOnly` e `testImplementation`. Versão estável atual: **Gradle 9.5.1** (Gradle 9.0 exige **Java 17+**).

## O que é

Gradle é uma **ferramenta de build de propósito geral** que modela o processo de construção como código executável, não como configuração declarativa pura. Onde o Maven descreve o projeto num XML fixo e segue um ciclo de vida pré-definido, Gradle te dá uma **linguagem** (Kotlin ou Groovy) para descrever *o que* construir e *como*.

Três conceitos sustentam o modelo:

- **Build script** — o arquivo `build.gradle.kts` (ou `build.gradle`) que descreve o projeto: plugins aplicados, repositórios, dependências e tasks customizadas.
- **Task** — a unidade atômica de trabalho (compilar, empacotar, rodar testes). Tasks se conectam num grafo de dependências.
- **Configuration** — um balde nomeado que agrupa dependências por escopo (compilação, runtime, teste).

Há ainda o `settings.gradle.kts`, que define o nome do build e quais subprojetos compõem um build multi-módulo — ele é avaliado **antes** de qualquer `build.gradle.kts`.

> [!info] Onde isso se encaixa no galho
> Esta é a nota de **modelo mental** do Gradle. A mecânica de dependências (api vs implementation, Version Catalogs, wrapper) está na nota 06; performance, build cache e daemon na nota 07; a comparação honesta com Maven na nota 08.

## Por que importa

Quem vem do Maven costuma tratar o `build.gradle.kts` como "um `pom.xml` com outra sintaxe". Esse modelo mental quebra rápido: como o build é um **programa**, você pode declarar variáveis, condicionais, funções e tasks customizadas direto no script — flexibilidade que o XML não oferece, mas que também abre espaço para builds bagunçados.

Para uma entrevista de backend Java, três pontos rendem:

1. **Saber ler um `build.gradle.kts`** e explicar o que cada bloco faz (`plugins`, `repositories`, `dependencies`).
2. **Entender o grafo de tasks** — por que `gradle build` dispara `compileJava`, `test` e `jar` na ordem certa sem você pedir.
3. **Escolher a configuration correta** ao declarar uma dependência, porque isso afeta o que vaza para quem consome seu módulo (detalhe na nota 06).

## Como funciona

### Build script: Groovy DSL vs Kotlin DSL

Gradle aceita duas linguagens para o build script, e ambas produzem o mesmo modelo de build por baixo:

- **Kotlin DSL** (`build.gradle.kts`) — o **default recomendado desde Gradle 8.0**. Por ser Kotlin estaticamente tipado, a IDE entrega **autocomplete, navegação, refatoração e erros em tempo de compilação** (em vez de só descobrir o erro ao rodar o build). Gradle gera *type-safe accessors* para os elementos contribuídos por plugins, então `implementation(...)` aparece com tipo conhecido.
- **Groovy DSL** (`build.gradle`) — a sintaxe original, dinâmica. Continua **totalmente suportada e NÃO está deprecada**. É mais concisa em alguns pontos e tem histórico maior na web, mas resolve muita coisa só em runtime, o que enfraquece o suporte da IDE.

Os dois podem **coexistir no mesmo build** (um módulo em Kotlin, outro em Groovy). O custo conhecido do Kotlin DSL é ser mais lento no *primeiro* uso, por causa da compilação do script — algo geralmente irrelevante depois que o build aquece.

> [!tip] Regra prática
> Projeto novo → comece em Kotlin DSL. O ganho de autocomplete e de pegar erro antes do build compensa quase sempre.

### Tasks e o task graph (DAG)

Uma **task** é a unidade de trabalho de Gradle. Tasks declaram dependências entre si com `dependsOn`, e Gradle as organiza num **grafo acíclico dirigido** (DAG — *directed acyclic graph*). "Acíclico" porque não pode haver ciclo: se A depende de B, B não pode depender de A.

Quando você roda `gradle build`, Gradle:

1. Monta o grafo completo de tasks a partir do que `build` exige.
2. Faz a **ordenação topológica** — descobre uma ordem em que toda dependência roda antes do seu dependente.
3. Executa as tasks nessa ordem (e pode paralelizar ramos independentes do grafo).

Por isso você nunca chama `compileJava` na mão: pedir `build` já arrasta `compileJava`, depois `test`, depois `jar`, na sequência correta.

O ponto central para entrevista: **toda task declara `inputs` e `outputs`**. Antes de executar, Gradle compara os inputs e outputs atuais com os da última execução. Se nada mudou, a task fica marcada como `UP-TO-DATE` e é **pulada**. É esse contrato de inputs/outputs que torna o build **incremental** — a base de toda a performance que a nota 07 detalha.

```kotlin
// Task customizada que declara input e output (esqueleto)
tasks.register("gerarVersao") {
    val arquivoFonte = layout.projectDirectory.file("version.txt")
    val arquivoSaida = layout.buildDirectory.file("generated/version.properties")

    inputs.file(arquivoFonte)        // se version.txt não mudou...
    outputs.file(arquivoSaida)       // ...e a saída existe → UP-TO-DATE, pula

    doLast {
        // lógica de geração aqui
    }
}
```

### Configurations: baldes de dependência por escopo

Uma **configuration** é um balde nomeado de dependências, definido por *escopo*: em que momento aquela dependência é necessária — compilação, runtime ou teste. Você declara uma dependência colocando-a na configuration certa dentro do bloco `dependencies`:

- **`implementation`** — disponível na compilação e no runtime do seu módulo; é o escopo padrão da maioria das libs.
- **`api`** — como `implementation`, mas a dependência **vaza para quem consome** seu módulo (faz parte do contrato público). O contraste fino `api` vs `implementation` é o tema da nota 06.
- **`compileOnly`** — presente só na compilação, ausente no runtime (ex.: anotações de processador, APIs fornecidas pelo container).
- **`runtimeOnly`** — presente só no runtime, ausente na compilação (ex.: driver JDBC, implementação de logging).
- **`testImplementation`** — disponível apenas para o código de teste.

A escolha da configuration controla o **classpath** em cada fase e o que é exposto a consumidores. Errar aqui infla o classpath ou vaza detalhe de implementação como se fosse API.

## Na prática

Um `build.gradle.kts` mínimo de uma aplicação Java, com `plugins`, `repositories` e `dependencies` usando várias configurations:

```kotlin
plugins {
    java
    application
}

repositories {
    mavenCentral()
}

dependencies {
    implementation("com.example:lib-core:1.4.0")        // compila + runtime
    api("com.example:lib-api:2.1.0")                     // vaza pro consumidor
    compileOnly("org.example:annotations:0.9.0")         // só na compilação
    runtimeOnly("com.example:driver-impl:3.0.0")         // só no runtime
    testImplementation("org.example:test-kit:5.2.0")     // só nos testes
}

application {
    mainClass.set("com.example.app.Main")
}
```

O `settings.gradle.kts` que acompanha:

```kotlin
rootProject.name = "minha-aplicacao"
```

O **mesmo build em Groovy DSL**, para contraste (note as aspas simples e a ausência de parênteses/`=`):

```groovy
plugins {
    id 'java'
    id 'application'
}

repositories {
    mavenCentral()
}

dependencies {
    implementation 'com.example:lib-core:1.4.0'
    testImplementation 'org.example:test-kit:5.2.0'
}
```

Comandos do dia a dia:

```bash
# Constrói o projeto: dispara o grafo de tasks (compileJava, test, jar...)
gradle build

# Lista as tasks disponíveis, agrupadas por categoria
gradle tasks

# Roda uma task específica (e suas dependências)
gradle test
```

## Armadilhas

### (1) Pensar em Gradle como "Maven em código"

A tentação é ler o `build.gradle.kts` como um `pom.xml` traduzido. Mas o build é um **programa que constrói um modelo de objetos**, avaliado em fases (configuração e execução). Quem trata o script como documento estático escreve lógica imperativa no lugar errado — por exemplo, código que roda em *toda* invocação durante a fase de configuração, em vez de dentro de uma task. O resultado é build lento e imprevisível. A regra mental certa não é "que tag eu coloco?", e sim "que task produz isso, e quais são seus inputs/outputs?".

### (2) Task sem inputs/outputs declarados quebra o incremental

Se você escreve uma task customizada (ou um `doLast`) que lê/escreve arquivos mas **não declara** `inputs`/`outputs`, Gradle não tem como saber se o trabalho já está atualizado. A task **roda toda vez**, nunca fica `UP-TO-DATE`, nunca é cacheável — e ainda pode forçar a re-execução de tasks downstream. Declarar `inputs.file(...)` e `outputs.file(...)` (ou `dir`/`property`) é o que liga essa task ao motor incremental. Esquecer disso é a causa nº 1 de build "que sempre faz tudo de novo". Aprofundamento na nota 07.

## Em entrevista

### Frase pronta (inglês)

> Gradle models the build as a program rather than static configuration: the build script declares tasks, and Gradle wires them into a directed acyclic graph, running each task's dependencies first. What makes it incremental is that every task declares its inputs and outputs, so Gradle can mark a task UP-TO-DATE and skip it when nothing changed. Dependencies go into scope-based configurations — implementation, api, compileOnly, runtimeOnly, testImplementation — and I default to the Kotlin DSL because the static typing gives me real IDE autocomplete and compile-time errors instead of failures only at build time.

### Vocabulário

| Termo PT | Termo EN |
| --- | --- |
| o `build.gradle(.kts)` que descreve o projeto | Build script |
| unidade de trabalho do build (compilar, testar, empacotar) | Task |
| grafo de tasks ordenado por `dependsOn`, sem ciclos | DAG (directed acyclic graph) |
| o que uma task consome e produz; base do `UP-TO-DATE` e do incremental | Inputs/outputs |
| balde de dependências por escopo (`implementation`, `api`, etc.) | Configuration |
| DSL tipada (`.kts`), default recomendado desde Gradle 8.0; Groovy DSL não é deprecado | Kotlin DSL |
| define nome do build e subprojetos; avaliado antes dos build scripts | `settings.gradle(.kts)` |

## Veja também

- [[03-Dominios/Tecnologia/Java/Build e tooling/06 - Gradle — dependências, Version Catalogs e o wrapper|Gradle — dependências e Version Catalogs]]
- [[03-Dominios/Tecnologia/Java/Build e tooling/07 - Gradle — performance, build cache e daemon|Gradle — performance]]
- [[03-Dominios/Tecnologia/Java/Build e tooling/08 - Maven vs Gradle — trade-offs honestos|Maven vs Gradle]]
- [[03-Dominios/Tecnologia/Java/Build e tooling/index|Build, tooling e ecossistema (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]

## Referências

- Gradle User Guide — [Kotlin DSL Primer](https://docs.gradle.org/current/userguide/kotlin_dsl.html)
- Gradle User Guide — [More about Tasks](https://docs.gradle.org/current/userguide/more_about_tasks.html)
- Gradle User Guide — [Declaring Dependencies](https://docs.gradle.org/current/userguide/declaring_dependencies.html)
- [Gradle Releases](https://gradle.org/releases/) — versão estável atual 9.5.1 (maio de 2026); Gradle 9.0.0 (2025-07-31) exige Java 17+.
