---
title: "Publicação de artefatos"
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
  - packaging
aliases:
  - "Maven Central"
  - "Central Portal"
---

# Publicação de artefatos

> [!abstract] TL;DR
> Publicar um artefato é empurrá-lo para um repositório onde outros builds o resolvam por coordenadas (`groupId:artifactId:version`). Há dois destinos: **interno** (Nexus/Artifactory — repos corporativos privados, com proxy/cache de Central) e **público** (Maven Central). Para Central, o caminho legado via **OSSRH foi desligado em 30/06/2025**: hoje publica-se pelo **Central Portal** (`central.sonatype.com`) usando o `central-publishing-maven-plugin`. O Central exige **assinatura GPG**, jars de **sources** e **javadoc**, POM com metadata completa (licença, SCM, developers) e **namespace verificado** — e **não aceita SNAPSHOT**.

## O que é

Publicar é a etapa final do ciclo de vida do build: depois de compilar, testar e empacotar, você envia o artefato para um **repositório remoto** onde outros projetos podem resolvê-lo como dependência. A identidade do artefato são suas **coordenadas** — `groupId`, `artifactId` e `version` —, e o destino é declarado no `distributionManagement` (Maven) ou no bloco `repositories` do `publishing` (Gradle).

O comando `mvn deploy` (ou as tasks `publish*` do Gradle) faz o upload. O que muda entre cenários é **para onde** você publica e **quais requisitos** o repositório de destino impõe.

## Por que importa

Sem publicação, um artefato vive só na sua máquina (`~/.m2/repository`, via `mvn install`) — invisível para CI, colegas e o mundo. Publicar é o que transforma código em **dependência reutilizável**.

Mas os dois destinos têm contratos muito diferentes. Um repositório **interno** é permissivo: aceita SNAPSHOT, não exige assinatura, serve para deps privadas da empresa. O **Maven Central**, por ser público e imutável, é rigoroso: metadata completa, assinatura criptográfica, namespace verificado. Confundir os dois contratos — ou usar o fluxo OSSRH legado, já desligado — é a fonte número um de deploys rejeitados.

## Como funciona

### Interno (Nexus/Artifactory) vs público (Maven Central)

Um **repositório interno** (Sonatype Nexus ou JFrog Artifactory rodando na empresa) serve três papéis:

- **Hospedar deps privadas**: bibliotecas internas que não podem ir para Central.
- **Proxy/cache de Central**: o build resolve dependências externas através do Nexus, que faz cache local — acelera e protege contra indisponibilidade do upstream.
- **Repositório de releases e snapshots corporativos**: com controle de acesso e retenção próprios.

O contrato é flexível: aceita SNAPSHOT, normalmente não exige assinatura GPG, e a autenticação é por credenciais no `settings.xml` (Maven) ou nas credenciais do `repositories` (Gradle).

O **Maven Central** é o repositório público padrão do ecossistema Java. Por ser global e **imutável** (uma vez publicada, uma versão nunca muda nem some), impõe requisitos estritos de qualidade e procedência. É para onde vão bibliotecas open source consumidas por qualquer um.

### Maven Central hoje: OSSRH morreu, o caminho é o Central Portal

O fluxo histórico usava o **OSSRH** (OSS Repository Hosting), baseado no Sonatype **Nexus 2**, com o `maven-deploy-plugin` apontando para `oss.sonatype.org` e um passo manual de "close/release" no staging. **Esse fluxo foi descontinuado em 30/06/2025.** O `maven-deploy-plugin` legado contra OSSRH **não funciona mais**.

O caminho atual é o **Central Portal** (`central.sonatype.com`). Em Maven, usa-se o **`central-publishing-maven-plugin`**, que faz o upload diretamente para o Portal. Requisitos do Central:

- **Namespace verificado**: você prova controle do `groupId` (ex.: domínio próprio ou conta GitHub) antes de poder publicar nele.
- **Assinatura GPG**: todo artefato vai assinado com chave PGP publicada em um keyserver (`maven-gpg-plugin`).
- **Jar de sources e jar de javadoc**: obrigatórios além do jar principal.
- **POM com metadata completa**: `name`, `description`, `url`, `licenses`, `scm` e `developers`.

Falhar qualquer um destes faz o Portal **rejeitar** a publicação.

### SNAPSHOT vs release

Uma versão **SNAPSHOT** (ex.: `1.4.0-SNAPSHOT`) é **mutável**: representa "trabalho em andamento" e pode ser republicada sobre si mesma. Vive em um **repositório de snapshots** separado e é resolvida com o sufixo de timestamp.

Uma versão **release** (ex.: `1.4.0`) é **imutável**: publicada uma vez, congelada para sempre. É o que builds reprodutíveis dependem.

Ponto crítico: o **Maven Central não aceita SNAPSHOT** — só releases imutáveis. SNAPSHOTs ficam em repositórios internos ou no endpoint de snapshots do Portal, nunca no Central de releases.

## Na prática

POM com `central-publishing-maven-plugin`, `maven-gpg-plugin` e metadata completa:

```xml
<project>
  <groupId>com.example</groupId>
  <artifactId>minha-lib</artifactId>
  <version>1.4.0</version>

  <name>Minha Lib</name>
  <description>Biblioteca de exemplo.</description>
  <url>https://github.com/example/minha-lib</url>

  <licenses>
    <license>
      <name>Apache License 2.0</name>
      <url>https://www.apache.org/licenses/LICENSE-2.0.txt</url>
    </license>
  </licenses>
  <developers>
    <developer>
      <id>fulano</id>
      <name>Fulano de Tal</name>
      <email>fulano@example.com</email>
    </developer>
  </developers>
  <scm>
    <connection>scm:git:https://github.com/example/minha-lib.git</connection>
    <developerConnection>scm:git:ssh://git@github.com/example/minha-lib.git</developerConnection>
    <url>https://github.com/example/minha-lib</url>
  </scm>

  <build>
    <plugins>
      <!-- jars de sources e javadoc -->
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-source-plugin</artifactId>
        <executions>
          <execution>
            <id>attach-sources</id>
            <goals><goal>jar-no-fork</goal></goals>
          </execution>
        </executions>
      </plugin>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-javadoc-plugin</artifactId>
        <executions>
          <execution>
            <id>attach-javadocs</id>
            <goals><goal>jar</goal></goals>
          </execution>
        </executions>
      </plugin>
      <!-- assinatura GPG -->
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-gpg-plugin</artifactId>
        <executions>
          <execution>
            <id>sign-artifacts</id>
            <phase>verify</phase>
            <goals><goal>sign</goal></goals>
          </execution>
        </executions>
      </plugin>
      <!-- upload para o Central Portal -->
      <plugin>
        <groupId>org.sonatype.central</groupId>
        <artifactId>central-publishing-maven-plugin</artifactId>
        <extensions>true</extensions>
        <configuration>
          <publishingServerId>central</publishingServerId>
        </configuration>
      </plugin>
    </plugins>
  </build>
</project>
```

Para um repositório **interno**, basta declarar o destino em `distributionManagement` e rodar `mvn deploy`:

```xml
<distributionManagement>
  <repository>
    <id>nexus-releases</id>
    <url>https://nexus.example.com/repository/maven-releases/</url>
  </repository>
  <snapshotRepository>
    <id>nexus-snapshots</id>
    <url>https://nexus.example.com/repository/maven-snapshots/</url>
  </snapshotRepository>
</distributionManagement>
```

Gradle, com `maven-publish` + `signing`:

```kotlin
plugins {
    `maven-publish`
    signing
    `java-library`
}

java {
    withSourcesJar()
    withJavadocJar()
}

publishing {
    publications {
        create<MavenPublication>("mavenJava") {
            from(components["java"])
            groupId = "com.example"
            artifactId = "minha-lib"
            version = "1.4.0"
            pom {
                name = "Minha Lib"
                description = "Biblioteca de exemplo."
                url = "https://github.com/example/minha-lib"
                licenses {
                    license {
                        name = "Apache License 2.0"
                        url = "https://www.apache.org/licenses/LICENSE-2.0.txt"
                    }
                }
                developers {
                    developer {
                        id = "fulano"
                        name = "Fulano de Tal"
                    }
                }
                scm {
                    connection = "scm:git:https://github.com/example/minha-lib.git"
                    url = "https://github.com/example/minha-lib"
                }
            }
        }
    }
    repositories {
        maven {
            name = "nexusInterno"
            url = uri("https://nexus.example.com/repository/maven-releases/")
        }
    }
}

signing {
    sign(publishing.publications["mavenJava"])
}
```

Comandos:

```bash
# instala no repo local (~/.m2), sem publicar
mvn install

# publica no destino do distributionManagement (interno) ou no Central Portal
mvn deploy

# Gradle: publica em todas as publicações/repositórios configurados
./gradlew publish
```

## Armadilhas

### (1) Publicar SNAPSHOT como release (ou esperar SNAPSHOT no Central)

Marcar a versão como `-SNAPSHOT` e tentar publicar como release imutável — ou pior, esperar resolver um SNAPSHOT a partir do Maven Central. O Central **só aceita releases imutáveis**; SNAPSHOTs vivem em repos internos ou no endpoint de snapshots do Portal. Remova o sufixo `-SNAPSHOT` para releases.

### (2) Metadata, sources, javadoc ou GPG incompletos → rejeitado pelo Central

O Central recusa o upload se faltar **assinatura GPG**, jar de **sources**, jar de **javadoc**, ou se o POM não tiver `licenses`, `scm` e `developers`. É um contrato tudo-ou-nada: um campo ausente derruba a publicação inteira. Configure os plugins de source, javadoc e gpg antes de tentar.

### (3) Usar o fluxo OSSRH legado / `maven-deploy-plugin` antigo

Copiar configs antigas apontando para `oss.sonatype.org` com `maven-deploy-plugin` e o passo de staging do Nexus 2. **Isso não funciona desde 30/06/2025** — o OSSRH foi desligado. Migre para o **Central Portal** com o `central-publishing-maven-plugin`.

## Em entrevista

### Frase pronta (inglês)

Publishing an artifact means pushing it to a repository where other builds resolve it by its `groupId:artifactId:version` coordinates. There are two destinations with very different contracts: an **internal** repository like Nexus or Artifactory — for private dependencies, and as a proxy/cache for Central — which is permissive and accepts SNAPSHOTs; and **Maven Central**, which is public, immutable, and strict. For Central, the legacy OSSRH path was shut down on June 30th, 2025, so today you publish through the **Central Portal** using the `central-publishing-maven-plugin`, which requires GPG-signed artifacts, sources and javadoc jars, complete POM metadata, a verified namespace, and release versions only — no SNAPSHOTs.

### Vocabulário

| Termo PT | Termo EN |
| --- | --- |
| Publicação de artefato | Artifact publishing / deployment |
| Coordenadas | Coordinates (groupId:artifactId:version) |
| Repositório interno | Internal / private repository |
| Assinatura GPG | GPG signing |
| Namespace verificado | Verified namespace |
| Versão imutável | Immutable version (release) |

## Veja também

- [[03-Dominios/Tecnologia/Java/Build e tooling/02 - Maven — POM, coordenadas e lifecycle|Maven — coordenadas e lifecycle]]
- [[03-Dominios/Tecnologia/Java/Build e tooling/11 - BOM e dependency management|BOM e dependency management]]
- [[03-Dominios/Tecnologia/Java/Build e tooling/18 - Supply chain e SBOM|Supply chain e SBOM]]
- [[03-Dominios/Tecnologia/Java/Build e tooling/index|Build, tooling e ecossistema (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]

## Referências

- Sonatype Central — Publish Guide: https://central.sonatype.org/publish/
- Sonatype Central — Central Portal registration: https://central.sonatype.org/register/central-portal/
- Sonatype — OSSRH Sunset / migration para o Central Portal: https://central.sonatype.org/news/20250326_ossrh_sunset/
- Gradle — Maven Publish Plugin: https://docs.gradle.org/current/userguide/publishing_maven.html
- Gradle — Signing Plugin: https://docs.gradle.org/current/userguide/signing_plugin.html
