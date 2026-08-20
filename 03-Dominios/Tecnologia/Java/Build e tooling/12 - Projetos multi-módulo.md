---
title: "Projetos multi-módulo"
created: 2026-06-11
updated: 2026-06-11
type: concept
status: seedling
publish: true
fase: Adepto
tags:
  - java
  - build
  - adepto
  - multi-module
aliases:
  - "reactor"
  - "multi-project"
---

# Projetos multi-módulo

> [!abstract] TL;DR
> Um projeto multi-módulo é **um único build** decomposto em vários módulos com fronteiras de responsabilidade claras. No Maven, um **parent POM** com `<packaging>pom</packaging>` e `<modules>` agrega os filhos, e o **reactor** ordena a compilação topologicamente pelas dependências entre módulos. No Gradle, o `settings.gradle.kts` declara os subprojetos com `include(...)`, e um módulo depende de outro via `implementation(project(":core"))`. Divida em módulos quando há fronteiras nítidas, build/test isolável e reuso; **não** divida só por estética — módulos demais viram overhead. Isto é estrutura de UM projeto/build, não topologia de repositórios de microservices.

## O que é

Um **projeto multi-módulo** (Maven) ou **multi-project build** (Gradle) é um único build que se desdobra em vários módulos coesos. Em vez de um único artefato monolítico, você tem um módulo agregador no topo e módulos-filho — tipicamente algo como `app`, `core` e `domain` — cada um com seu próprio descritor de build, mas todos construídos em conjunto por um único comando.

A ideia central: **separar responsabilidades em unidades de build independentes**, mantendo-as no mesmo repositório e no mesmo ciclo de build. Cada módulo produz seu próprio artefato (JAR), pode declarar suas próprias dependências e pode depender de outros módulos do mesmo projeto.

Não confunda com o **monólito modular**: este último pode viver dentro de **um único módulo** de build, separado apenas por pacotes e fronteiras lógicas. Multi-módulo é o passo seguinte — quando essas fronteiras lógicas ganham fronteiras físicas de build (módulos separados, com artefatos próprios).

## Por que importa

- **Fronteiras explícitas.** Um módulo `domain` que não pode importar nada de `app` força, no nível do build, a direção das dependências. O compilador vira guardião da arquitetura.
- **Build e teste isoláveis.** Você compila e testa `core` sem arrastar `app` junto. Ferramentas conseguem reconstruir só o que mudou.
- **Reuso real.** Um módulo `domain` ou `core` pode ser publicado e consumido por outros projetos, sem o peso da camada de aplicação.
- **Ordem correta e automática.** Tanto o reactor do Maven quanto o Gradle resolvem a ordem de build a partir das dependências declaradas — você não precisa orquestrar manualmente quem compila antes de quem.

O custo é real: mais arquivos de build, mais cerimônia, e o risco de fragmentar demais. Por isso a decisão de **quando** dividir importa tanto quanto o **como**.

## Como funciona

### Reactor do Maven

O **reactor** é o mecanismo do Maven para builds multi-módulo. Segundo a documentação, ele faz três coisas: coleta os módulos disponíveis, ordena os projetos na ordem correta de build, e os constrói nessa ordem.

A estrutura parte de um **parent POM** (também chamado de aggregator POM) com:

- `<packaging>pom</packaging>` — sinaliza que este POM não gera um JAR, e sim agrega/herda.
- `<modules>` com um `<module>` por filho — a **agregação**: lista os módulos que devem ser construídos em conjunto.

Há dois conceitos distintos, frequentemente combinados no mesmo parent:

- **Herança** (inheritance): o filho declara `<parent>` e herda propriedades, `<dependencyManagement>`, `<pluginManagement>`, configurações de plugin. É vertical (parent → filho).
- **Agregação** (aggregation): o parent declara `<modules>` para que um único `mvn` no topo construa todos. É horizontal (build em conjunto).

A **ordem de build é topológica**: o reactor ordena os módulos pelas relações entre eles. A documentação lista as relações honradas na ordenação, em ordem de precedência: dependência de projeto sobre outro módulo do build, declaração de plugin que é outro módulo, dependência de plugin sobre outro módulo, declaração de build extension sobre outro módulo, e — só se nenhuma outra regra se aplicar — a ordem declarada no `<modules>`.

Detalhe importante da doc: apenas referências "instanciadas" contam. `dependencyManagement` e `pluginManagement` **não** alteram a ordem do reactor — só dependências reais é que mudam a topologia.

### Multi-project do Gradle

No Gradle, um build multi-project consiste em um **root project** e um ou mais **subprojetos**, todos definidos num único `settings.gradle(.kts)`. É lá que você declara o que entra no build:

```kotlin
rootProject.name = "minha-aplicacao"
include("app", "core", "domain")
```

Os caminhos de projeto usam dois-pontos para aninhamento (ex.: `services:person-service` mapeia para o diretório `./services/person-service`).

Quando um módulo depende de outro, isso é uma **project dependency**, declarada com `project(":nome")`:

```kotlin
dependencies {
    implementation(project(":core"))
}
```

A doc é explícita: uma project dependency afeta tanto a ordem de build quanto o classpath — o projeto requerido é construído primeiro. Ou seja, o Gradle também resolve a ordem topologicamente a partir das dependências declaradas.

Para **compartilhar configuração** entre módulos sem repetição, o caminho idiomático são os **convention plugins**: pequenos plugins que encapsulam convenções (versão de Java, plugins comuns, repositórios) e são aplicados em cada módulo. Eles vivem em `buildSrc/` ou num build incluído chamado `build-logic` (composite build via `includeBuild`). Assim, em vez de copiar blocos de configuração em cada `build.gradle.kts`, cada módulo só aplica o convention plugin.

### Quando dividir (e quando não)

Divida em módulos quando:

- há **fronteiras de responsabilidade claras** que você quer impor no nível do build (ex.: `domain` puro, sem dependência de framework);
- você quer **build/test isolável** de uma parte sem reconstruir o resto;
- há **reuso** previsto — um módulo será consumido por mais de um lugar.

**Não** divida quando:

- um **monólito modular de um único módulo** já basta (pacotes + disciplina resolvem);
- a divisão é só estética e cada "módulo" sempre muda junto com os outros;
- o número de módulos cresce a ponto de o **overhead** de manter N arquivos de build superar o ganho de fronteira.

> [!info] Fronteira de escopo
> Multi-módulo aqui é estrutura de **UM** projeto/build. A topologia de **repositórios** de microservices (monorepo vs multi-repo, vários serviços deployáveis) é assunto de organização de código e deploy, tratada no galho [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/02 - Monorepo vs multi-repo|Microservices e sistemas distribuídos]]. Não confunda os dois eixos.

## Na prática

Árvore de um projeto multi-módulo típico (parent agregador + três filhos):

```text
minha-aplicacao/
├── pom.xml                 # parent / aggregator (packaging pom)
├── settings.gradle.kts     # (alternativa Gradle, no lugar do parent POM)
├── app/                    # camada de aplicação / entrypoint
│   ├── pom.xml
│   └── src/main/java/com/example/app/...
├── core/                   # serviços, casos de uso, regras
│   ├── pom.xml
│   └── src/main/java/com/example/core/...
└── domain/                 # entidades e contratos puros
    ├── pom.xml
    └── src/main/java/com/example/domain/...
```

Parent POM (Maven) com `<modules>` — note `<packaging>pom</packaging>`:

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>

  <groupId>com.example</groupId>
  <artifactId>minha-aplicacao</artifactId>
  <version>1.0.0-SNAPSHOT</version>
  <packaging>pom</packaging>

  <modules>
    <module>domain</module>
    <module>core</module>
    <module>app</module>
  </modules>

  <properties>
    <maven.compiler.release>21</maven.compiler.release>
  </properties>

  <dependencyManagement>
    <dependencies>
      <!-- versões centralizadas, herdadas pelos filhos -->
    </dependencies>
  </dependencyManagement>
</project>
```

O filho `core` declara o parent e depende de `domain` — o reactor coloca `domain` antes de `core`:

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>

  <parent>
    <groupId>com.example</groupId>
    <artifactId>minha-aplicacao</artifactId>
    <version>1.0.0-SNAPSHOT</version>
  </parent>

  <artifactId>core</artifactId>

  <dependencies>
    <dependency>
      <groupId>com.example</groupId>
      <artifactId>domain</artifactId>
      <version>1.0.0-SNAPSHOT</version>
    </dependency>
  </dependencies>
</project>
```

Equivalente no Gradle — `settings.gradle.kts` com `include`, e `app` dependendo de `core`:

```kotlin
// settings.gradle.kts
rootProject.name = "minha-aplicacao"
include("app", "core", "domain")

// app/build.gradle.kts
dependencies {
    implementation(project(":core"))
}

// core/build.gradle.kts
dependencies {
    implementation(project(":domain"))
}
```

## Armadilhas

### (1) Módulos demais → overhead

Fragmentar um projeto pequeno em dez módulos não traz fronteiras melhores — traz dez arquivos de build para manter, dez declarações de dependência para sincronizar e builds mais lentos por cerimônia. Se dois "módulos" sempre mudam juntos e nunca são consumidos separadamente, eles deviam ser um só. Comece com um módulo (ou poucos) e divida quando a dor de **não** dividir aparecer, não antes.

### (2) Dependência circular entre módulos

Se `core` depende de `domain` e `domain` passa a depender de `core`, você cria um ciclo. O reactor do Maven e o Gradle ordenam topologicamente — e um grafo com ciclo **não tem ordem topológica**, então o build falha. O sintoma é claro, mas a causa costuma ser uma fronteira mal desenhada: alguma classe está no módulo errado. A correção é arquitetural (mover o tipo, extrair uma abstração), não um truque de configuração.

### (3) Confundir multi-módulo com multi-repo de microservices

Multi-módulo é **um** projeto, **um** build, **um** repositório, com vários artefatos internos compilados juntos. Microservices são **vários serviços deployáveis independentemente**, cada um com seu ciclo de release — possivelmente em repositórios separados (multi-repo) ou num monorepo. São eixos diferentes: um é organização de **build**, o outro é organização de **deploy/repositório**. Tratar módulos internos como se fossem serviços (ou vice-versa) leva a decisões de fronteira erradas. (A topologia de repositórios é o galho [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/02 - Monorepo vs multi-repo|Microservices e sistemas distribuídos]].)

## Em entrevista

### Frase pronta (inglês)

A multi-module project is a single build split into cohesive modules with clear responsibility boundaries — for example, `domain`, `core`, and `app`. In Maven, a parent POM with `pom` packaging aggregates the children through the `modules` element, while the reactor sorts the build order topologically from the inter-module dependencies; in Gradle, the `settings.gradle.kts` declares subprojects with `include`, and a module depends on another via `implementation(project(":core"))`. I reach for modules when there are genuine boundaries worth enforcing at build time, when parts must be built and tested in isolation, or when there is real reuse — otherwise a single-module modular monolith is enough, since too many modules just add overhead. And I keep this distinct from microservice repository topology, which is a deploy-and-repo concern, not a build concern.

### Vocabulário

| Termo PT | Termo EN |
| --- | --- |
| Projeto multi-módulo | Multi-module project |
| Reactor (ordenação de build) | Reactor (build sorting) |
| POM-pai / agregador | Parent / aggregator POM |
| Herança vs agregação | Inheritance vs aggregation |
| Ordem de build topológica | Topological build order |
| Subprojeto | Subproject |
| Dependência de projeto | Project dependency |
| Convention plugin | Convention plugin |
| Dependência circular | Circular dependency |

## Veja também

- [[03-Dominios/Tecnologia/Java/Build e tooling/02 - Maven — POM, coordenadas e lifecycle|Maven — o modelo]]
- [[03-Dominios/Tecnologia/Java/Build e tooling/05 - Gradle — build script, tasks e configurations|Gradle — o modelo]]
- [[03-Dominios/Tecnologia/Java/Build e tooling/11 - BOM e dependency management|BOM e dependency management]]
- [[03-Dominios/Tecnologia/Java/Build e tooling/index|Build, tooling e ecossistema (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]

## Referências

- Apache Maven — Guide to Working with Multiple Modules (reactor, `modules`, sort order): https://maven.apache.org/guides/mini/guide-multiple-modules.html
- Gradle User Guide — Structuring Projects with Gradle / Multi-Project Builds (`settings.gradle.kts`, `include`, `project(...)`): https://docs.gradle.org/current/userguide/multi_project_builds.html
- Gradle User Guide — Sharing Build Logic with Convention Plugins (`buildSrc` / `build-logic`): https://docs.gradle.org/current/userguide/sharing_build_logic_between_subprojects.html
