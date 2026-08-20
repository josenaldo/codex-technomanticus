---
title: "Maven — plugins, profiles e o wrapper"
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
  - maven
aliases:
  - "Maven Wrapper"
  - "mvnw"
---

# Maven — plugins, profiles e o wrapper

> [!abstract] TL;DR
> No Maven, quem faz o trabalho de verdade são os **plugins**: o lifecycle (`compile`, `test`, `package`...) só **orquestra** os *goals* dos plugins ligados a cada fase. Os essenciais são `maven-compiler-plugin` (compila), `maven-surefire-plugin` (roda testes), `maven-jar-plugin` (monta o JAR) e `maven-shade-plugin` (uber-JAR). **Profiles** permitem variar a build por ambiente (ativados por `-P`, propriedade, env, OS ou JDK), mas abusar deles gera builds divergentes e não-reprodutíveis. O **Maven Wrapper** (`mvnw`) fixa a versão do Maven por projeto — e **não vem por padrão**: você o gera com `mvn wrapper:wrapper`.

## O que é

O Maven é movido a **plugins**. Cada operação concreta — compilar, testar, empacotar — é um *goal* fornecido por um plugin. O **lifecycle** (a sequência de fases) não executa nada por si: ele apenas amarra goals de plugins a fases, e rodar `mvn package` significa "execute, em ordem, todos os goals ligados às fases até `package`".

Em cima disso, dois mecanismos dão flexibilidade e portabilidade à build:

- **Profiles**: blocos de configuração que só entram em vigor sob certas condições (uma flag, uma propriedade, um sistema operacional, uma versão de JDK). Servem para variar a build entre ambientes (`dev`, `prod`).
- **Maven Wrapper** (`mvnw`): um par de scripts versionados no repositório que baixam e usam uma versão fixa do Maven, garantindo que todo mundo (e o CI) rode a build com o mesmo Maven.

## Por que importa

Entender que **o trabalho mora nos plugins** muda como você lê um `pom.xml`: quando algo não compila com a versão certa de Java, ou um teste não roda, o ajuste é na configuração de um plugin — não numa "mágica" do Maven.

Profiles e wrapper, por sua vez, são onde a build encontra a realidade do mundo: ambientes diferentes, máquinas diferentes, versões de Maven diferentes. Usados com disciplina, dão portabilidade. Usados sem critério, são a fonte clássica do "na minha máquina funciona" — exatamente o tipo de fragilidade que [[03-Dominios/Tecnologia/Java/Build e tooling/17 - Reprodutibilidade e reproducible builds|reprodutibilidade]] combate.

## Como funciona

### Plugins e goals — a unidade de trabalho

Cada plugin expõe um ou mais **goals**, e o lifecycle só os coordena. Os essenciais do dia a dia:

- **`maven-compiler-plugin`** — compila os fontes Java. É aqui que se define o nível da linguagem (`<release>`).
- **`maven-surefire-plugin`** — roda os **testes unitários** num classloader isolado, na fase `test`. Build quebra se um teste falha.
- **`maven-jar-plugin`** — monta o JAR principal do projeto (o artefato `package` padrão para `jar`).
- **`maven-shade-plugin`** — gera um **uber-JAR** (fat JAR), embutindo as dependências num único arquivo executável. Os detalhes de empacotamento e fat JAR ficam em [[03-Dominios/Tecnologia/Java/Build e tooling/15 - Empacotamento — fat jar, thin jar e repackage|empacotamento]].

Você declara um plugin em `<build><plugins>`, fixando versão e configuração.

### Profiles — variando a build por contexto

Um profile é um subconjunto de elementos do POM que só "liga" sob ativação. Formas de ativar:

- **Por flag**: `-Pprod` (lista separada por vírgula; `!prod` desativa).
- **Por propriedade**: `-Denvironment=test` casa com `<activation><property>`.
- **Por variável de ambiente**: ex. `env.CI`.
- **Por sistema operacional**: `<os><family>Windows</family></os>`.
- **Por versão de JDK**: `<jdk>[17,)</jdk>` (prefixo ou range).
- **Por padrão**: `<activeByDefault>true</activeByDefault>`.

O risco: como a doc do Maven alerta, profiles "facilmente levam a resultados de build divergentes entre membros do time". Se a configuração crítica vive fora do POM versionado (em `~/.m2/settings.xml`, por exemplo), quem não tiver aquele settings não consegue buildar.

### Maven Wrapper — fixando a versão do Maven

O wrapper resolve uma pergunta incômoda: *qual Maven o time está usando?* Ele consiste em:

- **`mvnw`** (script shell, Linux/macOS) e **`mvnw.cmd`** (batch, Windows);
- a pasta **`.mvn/wrapper/`**, com `maven-wrapper.properties` apontando a versão e a URL de download.

Rodando `./mvnw package`, o script baixa (na primeira vez) e usa exatamente a versão fixada, sem depender de Maven instalado na máquina. Crucial: **o wrapper NÃO vem por padrão** com o Maven — você o gera no projeto com `mvn wrapper:wrapper` (que invoca o `maven-wrapper-plugin`). É o mesmo espírito do wrapper do [[03-Dominios/Tecnologia/Java/Build e tooling/07 - Gradle — performance, build cache e daemon|Gradle]].

## Na prática

Declarando um plugin e um profile no `pom.xml`:

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.example</groupId>
  <artifactId>app</artifactId>
  <version>1.0.0</version>

  <build>
    <plugins>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-compiler-plugin</artifactId>
        <version>3.15.0</version>
        <configuration>
          <release>17</release>
        </configuration>
      </plugin>
    </plugins>
  </build>

  <profiles>
    <profile>
      <id>prod</id>
      <properties>
        <app.endpoint>https://api.example.com</app.endpoint>
      </properties>
    </profile>
  </profiles>
</project>
```

Empacotando com o profile `prod` e gerando o wrapper:

```bash
# Empacota ativando o profile prod
mvn -Pprod package

# Gera o Maven Wrapper no projeto (mvnw, mvnw.cmd, .mvn/wrapper/)
mvn wrapper:wrapper

# A partir daí, a build usa a versão fixada — sem Maven instalado
./mvnw -Pprod package
```

## Armadilhas

### (1) Profiles divergentes quebram a reprodutibilidade

Cada profile é uma bifurcação possível da build. Quando configuração essencial mora em profiles ativados por condições de ambiente — ou pior, em propriedades definidas fora do POM (no `settings.xml` de cada um) — a build deixa de ser determinística: o mesmo comando produz artefatos diferentes em máquinas diferentes, e quem não tem o profile/propriedade certo simplesmente não consegue buildar. Mantenha a configuração no POM versionado, cubra o conjunto completo de ambientes-alvo e trate profiles como exceção controlada, não como atalho. Veja [[03-Dominios/Tecnologia/Java/Build e tooling/17 - Reprodutibilidade e reproducible builds|reprodutibilidade]].

### (2) Commitar sem o wrapper deixa a build refém do Maven da máquina

Sem `mvnw`/`mvnw.cmd` e `.mvn/wrapper/` versionados, cada dev e cada runner de CI usa a versão de Maven que tiver instalada. Basta uma diferença de versão para uma build passar na sua máquina e falhar no CI (ou vice-versa). Gere o wrapper com `mvn wrapper:wrapper`, **commite** os arquivos gerados, e padronize o time a invocar `./mvnw` em vez de `mvn`.

## Em entrevista

### Frase pronta (inglês)

In Maven, plugins are where the actual work happens — the lifecycle phases like `compile`, `test`, and `package` simply orchestrate the goals bound to them. The essentials are the compiler plugin, the Surefire plugin for unit tests, the JAR plugin for the main artifact, and the Shade plugin when I need an uber-JAR. Profiles let me vary the build per environment, activated by the `-P` flag, a property, an environment variable, the OS, or the JDK version, but I keep them disciplined because they easily lead to non-reproducible builds. I always commit the Maven Wrapper — `mvnw` plus `.mvn/wrapper/` — so the whole team and the CI run the exact same Maven version; it doesn't ship by default, so I generate it with `mvn wrapper:wrapper`.

### Vocabulário

| Termo PT | Termo EN |
| --- | --- |
| plugin / objetivo (a unidade de trabalho executável) | plugin / goal |
| fase do ciclo de vida (orquestra goals) | lifecycle phase |
| plugin de execução de testes unitários | Surefire |
| JAR com dependências embutidas (Shade plugin) | uber-JAR / fat JAR |
| perfil de build, ativado por condição | build profile |
| ativação de profile (`-P`, property, env, OS, JDK) | profile activation |
| wrapper que fixa a versão do Maven por projeto | Maven Wrapper (`mvnw`) |
| build reprodutível / determinística | reproducible build |

## Veja também

- [[03-Dominios/Tecnologia/Java/Build e tooling/02 - Maven — POM, coordenadas e lifecycle|Maven — o modelo]]
- [[03-Dominios/Tecnologia/Java/Build e tooling/07 - Gradle — performance, build cache e daemon|Gradle — wrapper e performance]]
- [[03-Dominios/Tecnologia/Java/Build e tooling/17 - Reprodutibilidade e reproducible builds|Reprodutibilidade]]
- [[03-Dominios/Tecnologia/Java/Build e tooling/index|Build, tooling e ecossistema (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]

## Referências

- Maven — Available Plugins: https://maven.apache.org/plugins/
- Maven — Introduction to Build Profiles: https://maven.apache.org/guides/introduction/introduction-to-profiles.html
- Maven Wrapper: https://maven.apache.org/tools/wrapper/
