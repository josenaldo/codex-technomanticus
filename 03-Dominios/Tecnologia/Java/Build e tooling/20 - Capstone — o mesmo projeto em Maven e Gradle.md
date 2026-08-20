---
title: "Capstone — o mesmo projeto em Maven e Gradle"
created: 2026-06-11
updated: 2026-06-11
type: concept
status: seedling
publish: true
fase: Magus
tags:
  - java
  - build
  - magus
  - maven
  - gradle
aliases:
  - "Capstone Build e tooling"
  - "Maven vs Gradle lado a lado"
---

# Capstone — o mesmo projeto em Maven e Gradle

> [!abstract] TL;DR
> Pegamos **um único projeto multi-módulo** (uma lib `core` + um app `api`) e o construímos **duas vezes**: uma em Maven, outra em Gradle (Kotlin DSL + Version Catalog). Mesmas tarefas, lado a lado — declarar deps, importar um BOM, plugar JaCoCo e Checkstyle, gerar SBOM CycloneDX, empacotar e publicar. A conclusão honesta: **os dois resolvem o problema**. Maven vence em convenção e previsibilidade; Gradle vence em performance (cache, incremental) e flexibilidade. A escolha é de contexto, não de fé. JDK? **Temurin por padrão** — e a licença NFTC da Oracle desfaz o medo antigo de "pagar pelo Java". BOM e multi-módulo são ferramentas que você puxa quando a dor aparece, não cargo cult.

## O que é

Esta nota fecha o galho **Build, tooling e ecossistema**. Em vez de mais teoria, ela faz **a mesma coisa nos dois build tools**, coluna a coluna, para você ver onde divergem e onde convergem.

O projeto-exemplo é deliberadamente realista, mas mínimo:

```text
meu-projeto/
├── core/      → biblioteca (java-library): regras de domínio, sem framework
└── api/       → aplicação que depende de core e empacota um artefato executável
```

As tarefas que vamos espelhar:

1. **Estrutura** — o parent/raiz e os dois módulos.
2. **Dependências + BOM** — importar um conjunto coeso de versões via Bill of Materials.
3. **Quality gates + SBOM + empacotar** — JaCoCo, Checkstyle, CycloneDX, e o jar final.
4. **Publicar** — subir o artefato num repositório.

Em todo lugar usamos as mesmas coordenadas (`group:artifact:version`) — esse vocabulário é compartilhado, vem do mundo Maven e sobrevive intacto no Gradle. Ver [[03-Dominios/Tecnologia/Java/Build e tooling/01 - Por que build tools existem|01 — Por que build tools existem]].

## O projeto lado a lado

### Estrutura e árvore de arquivos

O Maven concentra tudo em `pom.xml`: um parent que lista os `<modules>` e um POM por módulo. O Gradle separa **o que faz parte do build** (`settings.gradle.kts`) de **como cada peça é construída** (`build.gradle.kts`), e centraliza versões num catálogo TOML.

```text
# Maven                          # Gradle
meu-projeto/                     meu-projeto/
├── pom.xml      (parent)        ├── settings.gradle.kts
├── core/                        ├── build.gradle.kts      (raiz, opcional)
│   └── pom.xml                  ├── gradle/
└── api/                         │   └── libs.versions.toml
    └── pom.xml                  ├── core/
                                 │   └── build.gradle.kts
                                 └── api/
                                     └── build.gradle.kts
```

**Maven — `pom.xml` parent:**

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.exemplo</groupId>
  <artifactId>meu-projeto-parent</artifactId>
  <version>1.0.0-SNAPSHOT</version>
  <packaging>pom</packaging>

  <modules>
    <module>core</module>
    <module>api</module>
  </modules>

  <properties>
    <maven.compiler.release>21</maven.compiler.release>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
  </properties>
</project>
```

**Gradle — `settings.gradle.kts`:**

```kotlin
rootProject.name = "meu-projeto"

include("core", "api")
```

O `packaging=pom` do parent (não produz jar, só agrega) é o análogo do projeto raiz do Gradle, que normalmente não gera artefato — só amarra os subprojetos. Detalhes do parent e do agregador em [[03-Dominios/Tecnologia/Java/Build e tooling/12 - Projetos multi-módulo|12 — Projetos multi-módulo]].

### Dependências e importação de BOM

Um **BOM** (Bill of Materials) é um POM só com `dependencyManagement`: você importa o conjunto e omite versões individuais — elas vêm alinhadas. Ver [[03-Dominios/Tecnologia/Java/Build e tooling/11 - BOM e dependency management|11 — BOM e dependency management]].

**Maven — BOM via `<dependencyManagement>` com `scope=import`:**

```xml
<dependencyManagement>
  <dependencies>
    <dependency>
      <groupId>com.fasterxml.jackson</groupId>
      <artifactId>jackson-bom</artifactId>
      <version>2.18.2</version>
      <type>pom</type>
      <scope>import</scope>
    </dependency>
  </dependencies>
</dependencyManagement>

<dependencies>
  <dependency>
    <groupId>com.fasterxml.jackson.core</groupId>
    <artifactId>jackson-databind</artifactId>
    <!-- versão herdada do BOM -->
  </dependency>
  <dependency>
    <groupId>org.junit.jupiter</groupId>
    <artifactId>junit-jupiter</artifactId>
    <scope>test</scope>
  </dependency>
</dependencies>
```

**Gradle — `gradle/libs.versions.toml` (o Version Catalog):**

```toml
[versions]
junit = "5.11.4"

[libraries]
jackson-bom = { module = "com.fasterxml.jackson:jackson-bom", version = "2.18.2" }
jackson-databind = { module = "com.fasterxml.jackson.core:jackson-databind" }
junit-jupiter = { module = "org.junit.jupiter:junit-jupiter", version.ref = "junit" }
```

**Gradle — `api/build.gradle.kts` importando o BOM com `platform()`:**

```kotlin
dependencies {
    implementation(project(":core"))
    implementation(platform(libs.jackson.bom))   // BOM → alinha versões
    implementation(libs.jackson.databind)        // sem versão: vem do platform
    testImplementation(libs.junit.jupiter)
}
```

Note o casamento conceitual: `<scope>import</scope>` do Maven ≡ `platform(...)` do Gradle. E `<scope>test</scope>` ≡ `testImplementation`. A dependência entre módulos: `<dependency>` apontando o `artifactId` do `core` no Maven ≡ `project(":core")` no Gradle. Scopes/configurations em detalhe: [[03-Dominios/Tecnologia/Java/Build e tooling/03 - Maven — dependências, scopes e exclusions|03 — Maven (deps, scopes, exclusions)]] e [[03-Dominios/Tecnologia/Java/Build e tooling/06 - Gradle — dependências, Version Catalogs e o wrapper|06 — Gradle (deps, Version Catalogs, wrapper)]].

> [!tip] Por que o catálogo é uma vitória pequena e real
> No Maven, versões compartilhadas vivem em `<properties>` e são referenciadas por `${...}` — funciona, mas é texto solto. O `libs.versions.toml` dá **autocomplete tipado** (`libs.jackson.databind`) e um único arquivo como fonte da verdade para todo o monorepo. É o tipo de ergonomia onde o Gradle se destaca sem precisar de mágica.

### Quality gates, SBOM e empacotamento

As três tarefas que mais separam "compila na minha máquina" de "pronto pra produção": cobertura/estilo, inventário de dependências (SBOM), e o pacote final.

**Maven — JaCoCo + Checkstyle + CycloneDX no `<build><plugins>`:**

```xml
<build>
  <plugins>
    <plugin>
      <groupId>org.jacoco</groupId>
      <artifactId>jacoco-maven-plugin</artifactId>
      <version>0.8.12</version>
      <executions>
        <execution><goals><goal>prepare-agent</goal></goals></execution>
        <execution><id>report</id><phase>test</phase>
          <goals><goal>report</goal></goals></execution>
      </executions>
    </plugin>
    <plugin>
      <groupId>org.apache.maven.plugins</groupId>
      <artifactId>maven-checkstyle-plugin</artifactId>
      <version>3.6.0</version>
      <executions>
        <execution><phase>verify</phase>
          <goals><goal>check</goal></goals></execution>
      </executions>
    </plugin>
    <plugin>
      <groupId>org.cyclonedx</groupId>
      <artifactId>cyclonedx-maven-plugin</artifactId>
      <version>2.9.1</version>
      <executions>
        <execution><goals><goal>makeAggregateBom</goal></goals></execution>
      </executions>
    </plugin>
  </plugins>
</build>
```

**Gradle — plugins declarativos no `api/build.gradle.kts`:**

```kotlin
plugins {
    id("java-library")
    id("jacoco")
    id("checkstyle")
    id("org.cyclonedx.bom") version "2.2.0"
    id("maven-publish")
}

tasks.test { finalizedBy(tasks.jacocoTestReport) }

tasks.jacocoTestReport {
    dependsOn(tasks.test)
}
```

Diferença de filosofia visível aqui: no Maven cada plugin **se amarra a uma fase do lifecycle** (`prepare-agent`, `verify`, etc.) — o ciclo é fixo e você pendura goals nele. No Gradle você **declara um grafo de tasks** e expressa relações (`finalizedBy`, `dependsOn`). Lifecycle vs grafo de tasks é a divisão mental central do galho: [[03-Dominios/Tecnologia/Java/Build e tooling/02 - Maven — POM, coordenadas e lifecycle|02 — Maven (POM, coordenadas, lifecycle)]] vs [[03-Dominios/Tecnologia/Java/Build e tooling/05 - Gradle — build script, tasks e configurations|05 — Gradle (build script, tasks, configurations)]].

**Empacotar** — o jar simples sai de graça nos dois (`mvn package` / `gradle build`). Para um **fat jar executável** (todas as deps embutidas), Maven usa o `maven-shade-plugin` ou o Spring Boot repackage; Gradle usa o plugin `application`/`shadow` ou o `bootJar`. Os trade-offs (fat vs thin, classpath vs nesting) estão em [[03-Dominios/Tecnologia/Java/Build e tooling/15 - Empacotamento — fat jar, thin jar e repackage|15 — Empacotamento]].

**Publicar** — subir o artefato para um repositório (Nexus, Artifactory, Maven Central):

```xml
<!-- Maven: distributionManagement no pom -->
<distributionManagement>
  <repository>
    <id>releases</id>
    <url>https://repo.exemplo.com/releases</url>
  </repository>
</distributionManagement>
<!-- publica com: mvn deploy -->
```

```kotlin
// Gradle: plugin maven-publish
publishing {
    publications {
        create<MavenPublication>("lib") {
            from(components["java"])
        }
    }
    repositories {
        maven { url = uri("https://repo.exemplo.com/releases") }
    }
}
// publica com: gradle publish
```

Mesmo formato de saída nos dois: um artefato Maven (POM + jar) num layout de repositório padrão. O consumidor não sabe (nem precisa saber) qual build tool gerou. Assinatura, staging e Central em [[03-Dominios/Tecnologia/Java/Build e tooling/19 - Publicação de artefatos|19 — Publicação de artefatos]] e o SBOM em [[03-Dominios/Tecnologia/Java/Build e tooling/18 - Supply chain e SBOM|18 — Supply chain e SBOM]].

## Tabela de decisão

```text
ESCOLHA O BUILD TOOL
─────────────────────────────────────────────────────────────────
Maven quando…                      Gradle quando…
─────────────────────────────────────────────────────────────────
• Projeto convencional, segue a    • Build grande/lento: build cache
  estrutura padrão sem brigar        e compilação incremental pagam
• Onboarding rápido: dev novo lê   • Monorepo poliglota (JVM + outras
  o pom e entende em minutos         linguagens/ferramentas)
• Build estável, declarativo,      • Precisa de lógica customizada no
  pouca lógica condicional           build (tasks, plugins próprios)
• Time prefere convenção forte e   • Time aceita curva de Kotlin DSL em
  previsibilidade sobre velocidade   troca de flexibilidade + perf
─────────────────────────────────────────────────────────────────
QUAL DISTRIBUIÇÃO DE JDK
─────────────────────────────────────────────────────────────────
• Default sensato: Eclipse Temurin (Adoptium) — TCK-certificado,
  gratuito, sem amarras.
• Oracle JDK: a licença NFTC (No-Fee Terms and Conditions, desde o
  JDK 17) permite uso gratuito inclusive em produção → o medo antigo
  de "pagar pela Oracle" não se aplica à versão atual.
• Variantes: GraalVM (native-image/AOT), Azul Zulu, Amazon Corretto,
  Liberica — todas builds do OpenJDK; escolha por suporte/LTS.
─────────────────────────────────────────────────────────────────
QUANDO USAR BOM
─────────────────────────────────────────────────────────────────
• Quando você consome um "stack" coeso (Spring, Jackson, AWS SDK,
  testcontainers): o BOM alinha todas as versões transitivamente.
• Quando múltiplos módulos precisam das MESMAS versões — o BOM vira
  fonte única da verdade e elimina drift entre módulos.
─────────────────────────────────────────────────────────────────
QUANDO USAR MULTI-MÓDULO
─────────────────────────────────────────────────────────────────
• Quando há fronteiras de compilação reais (lib publicável separada,
  ou limites de dependência que você quer impor pelo build).
• NÃO use só para "organizar pastas" — um monólito modular com
  pacotes bem definidos costuma bastar (ver Armadilha 2).
─────────────────────────────────────────────────────────────────
```

## Cheatsheet — problema → nota

| Problema / dúvida | Nota do galho |
|---|---|
| Por que não basta `javac`? | [[03-Dominios/Tecnologia/Java/Build e tooling/01 - Por que build tools existem\|01 — Por que build tools existem]] |
| Estrutura do POM, coordenadas, fases do lifecycle | [[03-Dominios/Tecnologia/Java/Build e tooling/02 - Maven — POM, coordenadas e lifecycle\|02 — Maven (POM, coordenadas, lifecycle)]] |
| Scopes (compile/test/provided), exclusions transitivas | [[03-Dominios/Tecnologia/Java/Build e tooling/03 - Maven — dependências, scopes e exclusions\|03 — Maven (deps, scopes, exclusions)]] |
| Plugins, profiles, `mvnw` (wrapper) | [[03-Dominios/Tecnologia/Java/Build e tooling/04 - Maven — plugins, profiles e o wrapper\|04 — Maven (plugins, profiles, wrapper)]] |
| Build script Kotlin, tasks, configurations | [[03-Dominios/Tecnologia/Java/Build e tooling/05 - Gradle — build script, tasks e configurations\|05 — Gradle (build script, tasks, configurations)]] |
| `implementation` vs `api`, Version Catalog, `gradlew` | [[03-Dominios/Tecnologia/Java/Build e tooling/06 - Gradle — dependências, Version Catalogs e o wrapper\|06 — Gradle (deps, Version Catalogs, wrapper)]] |
| Build lento: cache, daemon, incremental | [[03-Dominios/Tecnologia/Java/Build e tooling/07 - Gradle — performance, build cache e daemon\|07 — Gradle (performance, build cache, daemon)]] |
| "Maven ou Gradle?" — trade-offs sem dogma | [[03-Dominios/Tecnologia/Java/Build e tooling/08 - Maven vs Gradle — trade-offs honestos\|08 — Maven vs Gradle]] |
| Qual JDK instalar? Oracle cobra? | [[03-Dominios/Tecnologia/Java/Build e tooling/09 - Distribuições do JDK e o ecossistema\|09 — Distribuições do JDK]] |
| Duas versões da mesma lib brigando | [[03-Dominios/Tecnologia/Java/Build e tooling/10 - Resolução de dependências e conflitos de versão\|10 — Resolução de conflitos]] |
| Alinhar versões de um stack inteiro | [[03-Dominios/Tecnologia/Java/Build e tooling/11 - BOM e dependency management\|11 — BOM e dependency management]] |
| Quebrar o projeto em módulos | [[03-Dominios/Tecnologia/Java/Build e tooling/12 - Projetos multi-módulo\|12 — Projetos multi-módulo]] |
| Buildar com um JDK, mirar outra versão | [[03-Dominios/Tecnologia/Java/Build e tooling/13 - Toolchains — buildar com um JDK, mirar outro\|13 — Toolchains]] |
| Lombok/MapStruct não geram código | [[03-Dominios/Tecnologia/Java/Build e tooling/14 - Annotation processing — Lombok e MapStruct\|14 — Annotation processing (Lombok/MapStruct)]] |
| Fat jar vs thin jar, repackage | [[03-Dominios/Tecnologia/Java/Build e tooling/15 - Empacotamento — fat jar, thin jar e repackage\|15 — Empacotamento]] |
| Falhar o build por cobertura/estilo | [[03-Dominios/Tecnologia/Java/Build e tooling/16 - Quality gates no build\|16 — Quality gates]] |
| Mesmo input → mesmo binário (byte a byte) | [[03-Dominios/Tecnologia/Java/Build e tooling/17 - Reprodutibilidade e reproducible builds\|17 — Reprodutibilidade]] |
| Inventário de deps, CVEs, SBOM | [[03-Dominios/Tecnologia/Java/Build e tooling/18 - Supply chain e SBOM\|18 — Supply chain e SBOM]] |
| Publicar artefato (Nexus/Central) | [[03-Dominios/Tecnologia/Java/Build e tooling/19 - Publicação de artefatos\|19 — Publicação de artefatos]] |

## Armadilhas de raciocínio

### (1) "Gradle é sempre mais rápido"

O ganho do Gradle vem de **cache, daemon e incremental** — coisas que rendem em builds **grandes e repetidos** (CI quente, monorepo, recompilações parciais). Num projeto pequeno, num clean build frio em CI, ou na primeira execução (JVM e daemon ainda esfriando), a vantagem some — e o Gradle pode até ficar atrás de um Maven enxuto. Velocidade depende de **carga + cache quente**, não da etiqueta da ferramenta. O honesto é medir o seu build, não importar o benchmark de outro. Ver [[03-Dominios/Tecnologia/Java/Build e tooling/07 - Gradle — performance, build cache e daemon|07 — Gradle (performance, build cache, daemon)]].

### (2) "Preciso de multi-módulo"

Multi-módulo resolve **fronteiras de compilação e dependência reais**: uma lib publicável separadamente, ou limites que você quer que o build force. Não é ferramenta de organização de pastas. Para a maioria dos serviços, um **monólito modular** — um módulo só, com pacotes bem desenhados e disciplina de dependências — entrega a mesma clareza sem o custo de orquestrar N POMs/build scripts, resolver builds entre módulos e lidar com ordem de build. Quebre quando a dor de acoplamento aparecer, não preventivamente. Ver [[03-Dominios/Tecnologia/Java/Build e tooling/12 - Projetos multi-módulo|12 — Projetos multi-módulo]].

### (3) "Tenho que pagar pelo JDK"

Resquício do trauma de 2019, quando a Oracle mudou o licenciamento do Oracle JDK 8/11 para uso comercial pago. Desde o **JDK 17**, a Oracle publica o binário sob **NFTC (No-Fee Terms and Conditions)** — gratuito inclusive em produção, dentro dos termos. E o **OpenJDK** sempre foi e segue sendo livre: Temurin, Corretto, Zulu, Liberica são builds dele, TCK-certificadas e sem custo. O default seguro hoje é **Temurin**; ninguém precisa de licença paga para rodar Java moderno. Ver [[03-Dominios/Tecnologia/Java/Build e tooling/09 - Distribuições do JDK e o ecossistema|09 — Distribuições do JDK]].

## Em entrevista

### Frase pronta (inglês)

> Maven and Gradle solve the same problem — they turn source plus declared dependencies into a published artifact — so I treat the choice as contextual, not religious. I reach for Maven when the project is conventional and I value predictability and fast onboarding, since the POM is declarative and any new developer can read it. I reach for Gradle when the build is large or slow, where its build cache, daemon, and incremental compilation pay off, or when I need a polyglot monorepo or custom build logic, accepting the Kotlin DSL learning curve as the cost. Either way, I default to a TCK-certified OpenJDK build like Temurin, lock dependency versions with a BOM or version catalog, generate a CycloneDX SBOM for supply-chain visibility, and enforce coverage and style as quality gates so the artifact is reproducible and audit-ready before it ships.

### Vocabulário

| Termo PT | Termo EN |
|---|---|
| Build tool / ferramenta de build | build tool |
| Coordenadas (groupId:artifactId:version) | coordinates / GAV |
| Ciclo de vida (fases) | lifecycle (phases) |
| Grafo de tasks | task graph |
| Dependência transitiva | transitive dependency |
| Gerenciamento de dependências (BOM) | dependency management (BOM) |
| Catálogo de versões | version catalog |
| Projeto multi-módulo | multi-module project |
| Portões de qualidade (cobertura/estilo) | quality gates (coverage/style) |
| Inventário de software (SBOM) | Software Bill of Materials (SBOM) |
| Build reproduzível | reproducible build |
| Cache de build / daemon | build cache / daemon |
| Distribuição do JDK | JDK distribution / vendor |
| Empacotamento (fat/thin jar) | packaging (fat/thin jar) |

## Veja também

- [[03-Dominios/Tecnologia/Java/Build e tooling/index|Build, tooling e ecossistema (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Build e tooling/08 - Maven vs Gradle — trade-offs honestos|08 — Maven vs Gradle]]
- [[03-Dominios/Tecnologia/Java/Build e tooling/09 - Distribuições do JDK e o ecossistema|09 — Distribuições do JDK]]
- [[03-Dominios/Tecnologia/Java/Build e tooling/10 - Resolução de dependências e conflitos de versão|10 — Resolução de conflitos]]
- [[03-Dominios/Tecnologia/Java/Build e tooling/18 - Supply chain e SBOM|18 — Supply chain e SBOM]]

## Referências

- Apache Maven — documentação oficial: https://maven.apache.org/
- Gradle User Manual (current): https://docs.gradle.org/current/userguide/userguide.html
- Gradle — Sharing dependency versions (Version Catalogs): https://docs.gradle.org/current/userguide/platforms.html
- Eclipse Adoptium / Temurin: https://adoptium.net/
- Oracle — No-Fee Terms and Conditions (NFTC): https://www.oracle.com/downloads/licenses/no-fee-license.html
- CycloneDX — SBOM standard: https://cyclonedx.org/
- CycloneDX Maven Plugin: https://github.com/CycloneDX/cyclonedx-maven-plugin
- CycloneDX Gradle Plugin: https://github.com/CycloneDX/cyclonedx-gradle-plugin
