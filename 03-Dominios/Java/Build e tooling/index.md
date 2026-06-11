---
title: "Build, tooling e ecossistema"
created: 2026-06-11
updated: 2026-06-11
type: moc
status: growing
publish: true
tags:
  - java
  - build
  - moc
aliases:
  - "Build, tooling e ecossistema"
  - "Build e tooling"
  - "Build Tools"
  - "Maven e Gradle"
  - "Galho 15 - Build"
---

# Build, tooling e ecossistema

> [!abstract] TL;DR
> O Galho 15 cobre como um projeto Java é construído, versionado, empacotado e publicado — Maven e Gradle (modelo, lifecycle/tasks, performance), gestão de dependências (resolução transitiva, conflitos, BOM), multi-módulo, distribuições do JDK e licenciamento, annotation processing (Lombok/MapStruct), empacotamento, quality gates no build e cadeia de suprimentos (reproducible builds, SBOM).
> A tese: **um build tool resolve o grafo de dependências e produz um artefato reprodutível — não "compila"; e Maven vs Gradle é convenção vs flexibilidade, não "melhor vs pior".**
> São **20 notas** em 3 fases.

## Sobre este galho

A audiência primária é o dev pleno/sênior em preparação pra entrevista internacional que precisa justificar escolhas de build, dependências e JDK com critério — não decorar comandos, mas entender por que um build tool existe, o que ele resolve e onde Maven e Gradle divergem. A audiência secundária é quem configura na prática o build de um projeto Java real: scopes, BOM, multi-módulo, packaging, quality gates.

Este é um **galho novo/de pesquisa**, com **poda reversa mínima** — Lombok, MapStruct e packaging foram migrados de notas Spring pra cá, onde pertencem conceitualmente. A **tese honesta** atravessa o galho inteiro: build = grafo de dependências + reprodutibilidade; o bytecode produzido é o mesmo OpenJDK, então a diferença entre distribuições é licença e suporte, não tecnologia; e supply chain deixou de ser opcional depois do Log4Shell.

A **fronteira-assinatura é quádrupla** — quatro temas pertencem a este galho só de relance, porque foram explicados em profundidade em outros galhos (aqui se linka, não se re-explica): módulos/jlink/GraalVM-AOT estão no Galho 3; jpackage está no Galho 6; starters e repackage estão no Galho 8; teoria de teste, cobertura e mutation testing estão no Galho 13.

## Iniciado

O terreno: por que build tools, Maven, Gradle, JDK.
1. [[03-Dominios/Java/Build e tooling/01 - Por que build tools existem|01 — Por que build tools existem]] — javac/jar manual não escala; grafo de deps + lifecycle + artefato reprodutível.
2. [[03-Dominios/Java/Build e tooling/02 - Maven — POM, coordenadas e lifecycle|02 — Maven (POM, coordenadas e lifecycle)]] — POM, GAV, lifecycle/phases/goals; Maven 3.9.x estável, Maven 4 ainda RC.
3. [[03-Dominios/Java/Build e tooling/03 - Maven — dependências, scopes e exclusions|03 — Maven (dependências, scopes e exclusions)]] — scopes (compile/provided/runtime/test/import), transitividade, exclusions.
4. [[03-Dominios/Java/Build e tooling/04 - Maven — plugins, profiles e o wrapper|04 — Maven (plugins, profiles e o wrapper)]] — plugins como unidade de trabalho, profiles, mvnw (não vem por padrão).
5. [[03-Dominios/Java/Build e tooling/05 - Gradle — build script, tasks e configurations|05 — Gradle (build script, tasks e configurations)]] — Groovy vs Kotlin DSL (default desde 8.0), tasks/DAG, configurations.
6. [[03-Dominios/Java/Build e tooling/06 - Gradle — dependências, Version Catalogs e o wrapper|06 — Gradle (dependências, Version Catalogs e o wrapper)]] — implementation vs api, libs.versions.toml, gradlew.
7. [[03-Dominios/Java/Build e tooling/07 - Gradle — performance, build cache e daemon|07 — Gradle (performance, build cache e daemon)]] — incremental build, build cache, configuration cache, daemon.
8. [[03-Dominios/Java/Build e tooling/08 - Maven vs Gradle — trade-offs honestos|08 — Maven vs Gradle (trade-offs honestos)]] — declarativo/convenção vs imperativo/flexível; quando cada um, sem dogma.
9. [[03-Dominios/Java/Build e tooling/09 - Distribuições do JDK e o ecossistema|09 — Distribuições do JDK e o ecossistema]] — OpenJDK vs distros, NFTC/licença pós-2019, LTS 17/21/25, SDKMAN.

## Adepto

Dependências sérias, multi-módulo, packaging.
10. [[03-Dominios/Java/Build e tooling/10 - Resolução de dependências e conflitos de versão|10 — Resolução de dependências e conflitos de versão]] — nearest-wins (Maven) vs resolution strategy (Gradle), dependency tree.
11. [[03-Dominios/Java/Build e tooling/11 - BOM e dependency management|11 — BOM e dependency management]] — dependencyManagement, BOM via import, spring-boot-dependencies como caso concreto.
12. [[03-Dominios/Java/Build e tooling/12 - Projetos multi-módulo|12 — Projetos multi-módulo]] — reactor Maven vs multi-project Gradle; quando dividir.
13. [[03-Dominios/Java/Build e tooling/13 - Toolchains — buildar com um JDK, mirar outro|13 — Toolchains (buildar com um JDK, mirar outro)]] — Maven/Gradle toolchains, o release flag.
14. [[03-Dominios/Java/Build e tooling/14 - Annotation processing — Lombok e MapStruct|14 — Annotation processing (Lombok e MapStruct)]] — APT, Lombok+MapStruct, lombok-mapstruct-binding.
15. [[03-Dominios/Java/Build e tooling/15 - Empacotamento — fat jar, thin jar e repackage|15 — Empacotamento (fat jar, thin jar e repackage)]] — Shade/Shadow, spring-boot repackage, layered jar; jlink/jpackage como fronteira.

## Magus

Qualidade, supply chain, publicação.
16. [[03-Dominios/Java/Build e tooling/16 - Quality gates no build|16 — Quality gates no build]] — JaCoCo/Checkstyle/PMD/SpotBugs no lifecycle; falhar o build no threshold.
17. [[03-Dominios/Java/Build e tooling/17 - Reprodutibilidade e reproducible builds|17 — Reprodutibilidade e reproducible builds]] — build determinístico, project.build.outputTimestamp, default no Maven 4.
18. [[03-Dominios/Java/Build e tooling/18 - Supply chain e SBOM|18 — Supply chain e SBOM]] — SBOM, CycloneDX, SLSA, dependency scanning; o pós-Log4Shell.
19. [[03-Dominios/Java/Build e tooling/19 - Publicação de artefatos|19 — Publicação de artefatos]] — Maven Central (Central Portal), Nexus/Artifactory, SNAPSHOT vs release.
20. [[03-Dominios/Java/Build e tooling/20 - Capstone — o mesmo projeto em Maven e Gradle|20 — Capstone (o mesmo projeto em Maven e Gradle)]] — comparativo lado a lado + tabela de decisão + cheatsheet.

## Rotas alternativas

- **Completa** — 01 → 20 em ordem.
- **Entrevista internacional** — 01 → 02 → 05 → 08 → 09 → 10 → 11 → 18 → 20 (modelo, Maven, Gradle, decisão, JDK/licença, conflitos, BOM, supply chain, capstone).
- **Maven na prática** — 02 → 03 → 04 → 10 → 11 → 12 → 15 → 19.
- **Gradle na prática** — 05 → 06 → 07 → 10 → 11 → 12.
- **Build production-grade / supply chain** — 09 → 16 → 17 → 18 → 19.

## Todas as notas

```dataview
TABLE fase AS "Fase", status AS "Status"
FROM "03-Dominios/Java/Build e tooling"
WHERE type = "concept"
SORT file.name ASC
```

## Veja também

- [[03-Dominios/Java/index|Trilha Java (MOC central)]]
- [[03-Dominios/Java/JVM/index|JVM por dentro]] — módulos/JPMS, jlink, GraalVM/AOT (Galho 3)
- [[03-Dominios/Java/JavaFX/index|JavaFX]] — jpackage e empacotamento nativo (Galho 6)
- [[03-Dominios/Java/Spring Core e Boot/index|Spring Core e Boot]] — starters, BOM, spring-boot-maven-plugin (Galho 8)
- [[03-Dominios/Java/Testes/index|Testes]] — Surefire/Failsafe, JaCoCo, PIT (Galho 13)
- [[03-Dominios/Java/Dicionário de Java|Dicionário de Java]]

*> Galhos 16 (Microservices), 17 (Cloud-native e produção) e 18 (Certificação OCP) — planejados.*
