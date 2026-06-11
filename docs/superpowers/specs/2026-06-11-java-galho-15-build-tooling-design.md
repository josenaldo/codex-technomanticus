---
title: "Spec — Galho 15 da trilha Java Senior (Build, tooling e ecossistema)"
date: 2026-06-11
author: Josenaldo
status: draft
type: spec
publish: false
---

# Spec — Galho 15 da trilha Java Senior (Build, tooling e ecossistema)

## 1. Contexto e motivação

Este é o **décimo quinto galho** da trilha Java Senior (roadmap em `docs/superpowers/specs/2026-06-02-java-senior-roadmap-design.md`, §5, Galho 15). Pressupõe leitura do roadmap, que estabelece topologia flat, esquema de 3 fases (Iniciado/Adepto/Magus), padrões editoriais e política de poda. Os Galhos 1 a 14 já fecharam em `main` — seus artefatos são o **template de padrão e qualidade** deste galho. É o **primeiro galho do bloco "Plataforma distribuída e produção"** depois de o miolo backend Spring (8-13) e a mensageria (14) terem fechado.

**Galho NOVO/PESQUISA** (como os Galhos 5/7/11/14 — roadmap: "tronco a podar: nenhum") **+ poda reversa pequena e localizada**:

- **Parte PESQUISA (a maior):** o galho cobre **como um projeto Java é construído, versionado, empacotado e publicado** — Maven e Gradle (modelo, lifecycle/tasks, dependências, performance), a gestão séria de dependências (resolução transitiva, conflito de versão, BOM), projetos multi-módulo, as distribuições do JDK e o licenciamento pós-2019, annotation processing (Lombok/MapStruct), empacotamento (fat/thin jar, repackage), quality gates no build (JaCoCo/Checkstyle/SpotBugs/PMD) e a cadeia de suprimentos (reproducible builds, SBOM/CycloneDX, publicação no Maven Central). Quase tudo nasce de doc oficial via WebFetch (ZERO memória): `maven.apache.org`, `docs.gradle.org`/`gradle.org`, `oracle.com/java` (roadmap de suporte/licença), `adoptium.net`, `projectlombok.org`, `mapstruct.org`, `cyclonedx.org`, `central.sonatype.org`.

- **Parte PODA REVERSA (pequena e localizada):** o pré-flight (2026-06-11) confirmou que **NÃO existe tronco de build disperso** — só **menções pontuais** em `Backend/Spring Boot.md` (Lombok, MapStruct, `spring-boot-maven-plugin`/layered jar) e um auto-reconhecimento em `Spring Core e Boot/16 - SpringApplication e o embedded server.md` ("coberto no Galho 15/17 (planejado)"). A poda é **mínima e conservadora** (§3.5): a explicação canônica de Lombok/MapStruct e de packaging passa a viver no galho; nos arquivos do Spring fica um **resumo curto + wikilink** (Lombok no contexto de JPA é pedagogicamente relevante lá — não se apaga, linka-se).

**A fronteira-assinatura é QUÁDRUPLA.** O build é a camada que monta o que outros galhos já explicaram. Cada nota linka de volta sem re-explicar:

- **Galho 3 (JVM/JPMS):** módulos (JPMS), `jlink` (runtime customizado), GraalVM/AOT/native image → `[[03-Dominios/Java/JVM/08 - JPMS — o sistema de módulos|JPMS]]` e `[[03-Dominios/Java/JVM/01 - A JVM — o que é e o pipeline de execução|A JVM]]` (distribuições/Temurin/Corretto no ângulo de runtime). A nota 13 (toolchains) e a 15 (empacotamento) apontam pra cá. **GraalVM native image é Galho 17 (planejado)** — o galho 15 só menciona o conceito de AOT como fronteira.
- **Galho 6 (JavaFX):** `jpackage` (empacotamento nativo/instaladores) **já está coberto lá** → `[[03-Dominios/Java/JavaFX/13 - Empacotamento — módulos, jlink e jpackage|Empacotamento (JavaFX)]]`. A nota 15 linka, **não re-explica jpackage**.
- **Galho 8 (Spring Boot):** starters, auto-configuration, `spring-boot-maven-plugin`/`repackage` → `[[03-Dominios/Java/Spring Core e Boot/15 - Auto-configuration e starters|Auto-configuration e starters]]` e `[[03-Dominios/Java/Spring Core e Boot/16 - SpringApplication e o embedded server|SpringApplication]]`. O `spring-boot-dependencies`/`starter-parent` é a **fronteira de BOM** (nota 11): o galho explica o **mecanismo de BOM**, e linka o Boot como o BOM concreto que o leitor já conhece.
- **Galho 13 (Testes):** Surefire/Failsafe (os runners), JaCoCo (cobertura), PIT (mutation testing) → `[[03-Dominios/Java/Testes/17 - Mutation testing — PIT e cobertura honesta|Mutation testing — PIT]]` e `[[03-Dominios/Java/Testes/01 - O que é testar em Java — a pirâmide e o stack moderno|A pirâmide de testes]]`. A nota 16 (quality gates) cobre o **ângulo de build** (plugar a ferramenta no lifecycle, falhar o build no threshold), **não a teoria de teste/cobertura** — isso é o Galho 13.

**A tese honesta do galho:** um build tool não "compila" — ele resolve o **grafo de dependências** e produz um artefato **reprodutível**. A escolha **Maven vs Gradle** é **convenção/declarativo vs flexibilidade/imperativo**, não "melhor vs pior": Maven vence em projetos convencionais e onboarding; Gradle vence em builds grandes/heterogêneos pela performance incremental. E o "ecossistema do JDK" pós-2019 é uma **questão de licença e suporte**, não de tecnologia: o bytecode é o mesmo — Temurin, Corretto, Zulu e Oracle JDK são o mesmo OpenJDK com selos de suporte/licença diferentes. A cadeia de suprimentos (reproducible builds, SBOM) deixou de ser opcional pós-Log4Shell.

**Os Galhos 16/17/18 ainda não existem** — toda referência a microservices/Spring Cloud (Galho 16), containers/GraalVM native/deploy/produção (Galho 17) e OCP (Galho 18) permanece como texto "(planejado)", sem wikilink.

## 2. Objetivo

Produzir, em uma sessão de execução dedicada, **20 notas atômicas + 1 MOC do galho + expansão do Dicionário de Java + ativação do MOC central (Galho 15) + poda reversa conservadora em `Backend/Spring Boot.md` + cross-links**, em `03-Dominios/Java/Build e tooling/` e `03-Dominios/Java/`, todas `publish: true`, em PT-BR, distribuídas em 3 fases (**9 Iniciado + 6 Adepto + 5 Magus**).

Ao terminar o galho, o leitor deve conseguir:

- **Explicar em inglês** o que um build tool resolve (grafo de dependências + lifecycle + empacotamento reprodutível), o modelo do Maven (POM, coordenadas, lifecycle/phases) e do Gradle (build script, tasks, configurations), e **justificar a escolha** entre os dois com trade-offs honestos (convenção vs flexibilidade; performance incremental).
- **Gerir dependências com critério**: ler um dependency tree, diagnosticar e resolver um conflito de versão (entender **nearest-wins** do Maven vs a **resolution strategy** do Gradle), e usar um **BOM**/`dependencyManagement` (incluindo o `spring-boot-dependencies` como caso concreto) pra alinhar versões.
- **Estruturar um projeto multi-módulo** (reactor Maven / multi-project Gradle) e configurar **toolchains** pra buildar com um JDK e mirar outro.
- **Escolher uma distribuição do JDK** sabendo o que muda entre OpenJDK, Oracle JDK (NFTC), Temurin, Corretto, Zulu, Liberica e GraalVM, e a história de licença pós-2019; navegar o calendário de releases e LTS (21/25) e gerir versões locais com SDKMAN.
- **Empacotar** (fat/uber jar vs thin jar, `spring-boot:repackage`, layered jar), sabendo que `jlink`/`jpackage` são fronteira (Galhos 3/6), e configurar **annotation processing** (Lombok + MapStruct, o `lombok-mapstruct-binding`, o atrito de ordem de processors).
- **Endurecer o build**: plugar quality gates (JaCoCo/Checkstyle/SpotBugs/PMD) no lifecycle, produzir **builds reprodutíveis** (`project.build.outputTimestamp`), gerar um **SBOM** (CycloneDX) e publicar um artefato (Maven Central via Central Portal, ou Nexus/Artifactory).

A barra é "projetar, justificar e endurecer o build de um projeto Java production-grade, escolhendo build tool, distribuição de JDK e estratégia de dependências com critério" — não "decorar comandos de CLI". O foco é o **modelo mental + a decisão de engenharia**, com snippets corretos como apoio.

## 3. Saídas concretas

### 3.1. Notas (`03-Dominios/Java/Build e tooling/`)

Pasta **nova**, flat. 20 notas + 1 MOC (`index.md`, obrigatório pro folder-link do Quartz). Numeração global por galho (não reinicia por fase). **Nome da pasta no disco: `Build e tooling`** (decisão do brainstorming — sem vírgula, casa com o padrão "X e Y" das pastas-irmãs como "Collections e Streams"/"Spring Core e Boot"). O **título** no frontmatter/MOC/aliases continua "Build, tooling e ecossistema" (espelha o roadmap).

#### Iniciado (9 notas — o terreno: por que build tools, Maven, Gradle, JDK)

| # | Nota | Escopo nuclear |
|---|------|----------------|
| 01 | Por que build tools existem *(opus, assinatura)* | O problema: `javac` + `jar` na mão não escala (classpath, dependências transitivas, ordem de compilação, empacotamento, reprodutibilidade). O que um build tool resolve: **grafo de dependências + lifecycle + artefato reprodutível**. **A nota-assinatura:** build tool ≠ "compilador"; a escolha Maven vs Gradle é convenção vs flexibilidade; a fronteira quádrupla (G3/G6/G8/G13). |
| 02 | Maven — o modelo: POM, coordenadas e lifecycle | POM (`pom.xml`) como descritor declarativo; **coordenadas GAV** (`groupId:artifactId:version`, packaging, classifier); o **repositório local** (`~/.m2`) e os remotos; **lifecycle e phases** (`validate`→`compile`→`test`→`package`→`verify`→`install`→`deploy`), goals e a ligação phase→plugin goal. Versão atual: **Maven 3.9.x** (WebFetch); Maven 4 como "próxima major" (WebFetch — status atual). |
| 03 | Maven — dependências, scopes e exclusions | Declarar dependências; **scopes** (`compile`/`provided`/`runtime`/`test`/`system`/`import`); transitividade e como o scope propaga; `<exclusions>` pra cortar transitiva indesejada; `optional`. Armadilha: `provided` vs `runtime`. |
| 04 | Maven — plugins, profiles e o wrapper (mvnw) | Plugins como a unidade de trabalho (o lifecycle só orquestra goals de plugin); plugins essenciais (compiler, surefire, jar, shade); **profiles** (ativação por env/property/OS) e quando NÃO abusar; o **Maven Wrapper** (`mvnw`/`mvnw.cmd`) — fixar a versão do Maven por projeto (WebFetch: não vem por padrão, gerado via plugin). |
| 05 | Gradle — o modelo: build script, tasks e configurations | `build.gradle` (Groovy) vs `build.gradle.kts` (**Kotlin DSL — default recomendado desde Gradle 8.0**, WebFetch); **tasks** e o **task graph** (DAG, `dependsOn`); **configurations** como buckets de dependência (`implementation`/`api`/`compileOnly`/`runtimeOnly`/`testImplementation`); plugins (`plugins {}` block); `settings.gradle(.kts)`. Versão atual: **Gradle 9.x** (WebFetch). |
| 06 | Gradle — dependências, Version Catalogs e o wrapper | Declarar dependências por configuration; **`implementation` vs `api`** (encapsulamento do classpath de compilação — o grande ganho do Gradle); **Version Catalogs** (`gradle/libs.versions.toml`, `libs.xxx` type-safe accessors — estável e recomendado, WebFetch); o **Gradle Wrapper** (`gradlew`, sempre presente, fixa a versão). |
| 07 | Gradle — performance: incremental build, build cache e daemon | O argumento de venda do Gradle: **incremental build** (task inputs/outputs, up-to-date checking), **build cache** (local e remoto — reusar outputs entre máquinas/CI), **configuration cache** ("preferred mode" desde Gradle 9.0, WebFetch — ainda opt-in), o **daemon** (JVM quente). Por que Maven não tem equivalente nativo. |
| 08 | Maven vs Gradle — trade-offs honestos *(opus)* | O framework de decisão com os dois já na mão: **declarativo/convenção** (Maven: previsível, onboarding rápido, IDE/CI universal) vs **imperativo/flexível** (Gradle: performance incremental, builds heterogêneos, custom logic); XML vs DSL; curva de aprendizado; o ecossistema de plugins; quando cada um. **Sem dogma** — "quando X" E "quando Y". |
| 09 | Distribuições do JDK e o ecossistema *(opus, version-heavy)* | **OpenJDK** = o projeto/código; **distribuição** = binário com selo de suporte/licença. Oracle JDK (**NFTC** desde 2021 — a confusão pós-2019/OTN), Eclipse **Temurin**/Adoptium, Amazon **Corretto**, Azul **Zulu**, BellSoft **Liberica**, Microsoft Build of OpenJDK (todos GPLv2+CPE), **GraalVM** (GFTC). Calendário de releases (6 meses), **LTS a cada 2 anos** (17/21/**25**; próxima 29 em 2027), non-LTS (24/26). **SDKMAN** pra instalar/trocar versões localmente. Tudo WebFetch. |

#### Adepto (6 notas — dependências sérias, multi-módulo, packaging, annotation processing)

| # | Nota | Escopo nuclear |
|---|------|----------------|
| 10 | Resolução de dependências e conflitos de versão *(opus)* | Resolução **transitiva**; o **conflito de versão** (duas transitivas pedem versões diferentes); **Maven: nearest-wins** (a mais próxima na árvore vence — e o efeito surpresa da ordem de declaração); **Gradle: resolution strategy** (highest-version-wins por padrão, `failOnVersionConflict`, `force`, constraints). Ler o **dependency tree** (`mvn dependency:tree` / `gradle dependencies`); diagnosticar `NoSuchMethodError`/`NoClassDefFoundError` de classpath. |
| 11 | BOM e dependency management | `dependencyManagement` (Maven) — declarar versão sem declarar dependência; **BOM** (Bill of Materials) como POM de `import` scope; o **`spring-boot-dependencies`/`spring-boot-starter-parent`** como BOM concreto que o leitor já usa (**fronteira p/ Galho 8** — linka, não re-explica starters); Version Catalogs + `platform()` no Gradle como equivalente. Por que alinhar versões num só lugar. |
| 12 | Projetos multi-módulo | **Reactor do Maven** (parent POM `<packaging>pom</packaging>` + `<modules>`, herança vs agregação, build order topológico) vs **multi-project do Gradle** (`settings.gradle` `include`, `subprojects`/convention plugins, project dependencies). Quando dividir em módulos (e quando não — o monólito modular basta). |
| 13 | Toolchains — buildar com um JDK, mirar outro | O problema: a JVM que roda o build ≠ o JDK-alvo do bytecode. **Maven toolchains** (`maven-toolchains-plugin`, `~/.m2/toolchains.xml`) e o `release` flag do compiler; **Gradle toolchains** (`java { toolchain { languageVersion = ... } }`, auto-download/provisioning). Liga **G3** (a JVM/bytecode versionado). |
| 14 | Annotation processing — Lombok e MapStruct | O que é annotation processing (APT, `javax.annotation.processing`, geração de código em compile-time); **Lombok** (versão atual JDK 21/25-ready, WebFetch) e o atrito (não é APT padrão — manipula AST; `lombok.config`); **MapStruct** (mapper gerado, `componentModel = "spring"`); **o atrito Lombok+MapStruct** → `lombok-mapstruct-binding` (WebFetch) e a **ordem de processors**. **Recebe a poda do Spring Boot.md** (§3.5). |
| 15 | Empacotamento — fat jar, thin jar e repackage | `jar` simples (sem deps no classpath); **fat/uber jar** (Maven Shade / Gradle Shadow — tudo num jar, e o problema de resource merging/relocation); **thin jar**; o **`spring-boot:repackage`** (executable jar com nested jars + `JarLauncher`) e o **layered jar** (camadas pra cache de imagem — **fronteira p/ Galho 8/17**). **`jlink`/`jpackage` são fronteira (Galhos 3/6) — linka, não re-explica.** **Recebe a poda do layered jar do Spring Boot.md / Spring Core e Boot/16.** |

#### Magus (5 notas — qualidade, supply chain, publicação, capstone)

| # | Nota | Escopo nuclear |
|---|------|----------------|
| 16 | Quality gates no build — cobertura, estilo e bugs | Plugar a ferramenta no lifecycle e **falhar o build** no threshold: **JaCoCo** (cobertura, `check` goal com `minimum`), **Checkstyle** (estilo), **PMD** e **SpotBugs** (análise estática de bugs). **Ângulo de build, não teoria** — Surefire/Failsafe (runners), JaCoCo (cobertura como métrica) e PIT (mutation) são **fronteira p/ Galho 13** (linka). Quando falhar o build vs só reportar. |
| 17 | Reprodutibilidade — reproducible builds | Build determinístico: mesma entrada → bit-a-bit o mesmo artefato. **`project.build.outputTimestamp`** (Maven), timestamps normalizados, ordem estável de entradas; **default ativo no Maven 4** (WebFetch); validação (`maven-artifact-plugin` `check-buildplan`/`compare`); por que importa (verificabilidade, cache, auditoria de supply chain). Pin de versões (sem `LATEST`/ranges abertos). |
| 18 | Supply chain e SBOM *(opus)* | O pós-Log4Shell: saber **o que** você embarca. **SBOM** (Software Bill of Materials), **CycloneDX** (padrão Ecma desde 1.6, `cyclonedx-maven-plugin`/`cyclonedx-gradle-plugin`, WebFetch) vs SPDX; **SLSA** (níveis de integridade de build), **dependency scanning/SCA** (OWASP Dependency-Check); proveniência e attestation. Por que CVE scanning sozinho não cobre typosquatting/backdoor. |
| 19 | Publicação de artefatos | Coordenadas + repositório; publicar **interno** (Nexus/Artifactory) vs **público** (**Maven Central**); o processo atual: **OSSRH foi descontinuado (30/06/2025), Central Portal é o caminho** (`central-publishing-maven-plugin`, WebFetch); requisitos do Central (GPG signing, sources/javadoc jars, POM metadata); `maven-publish`/`signing` no Gradle; SNAPSHOT vs release. |
| 20 | Capstone — o mesmo projeto, Maven ⇄ Gradle *(opus, comparativo + síntese)* | **O mesmo projeto multi-módulo construído nos dois build tools, lado a lado**: a árvore de arquivos (`pom.xml` vs `build.gradle.kts` + `libs.versions.toml`), declarar deps + BOM, plugar JaCoCo/Checkstyle, gerar SBOM, empacotar e publicar — coluna Maven vs coluna Gradle. **Tabela de decisão** (Maven quando…, Gradle quando…; qual distribuição de JDK; quando BOM; quando multi-módulo). Cheatsheet nota→problema; munição de entrevista. |

**Notas opus (6):** 01 (assinatura/modelo), 08 (Maven vs Gradle — decisão), 09 (distribuições/licença — denso e version-heavy), 10 (resolução de conflitos — o algoritmo mais escorregadio), 18 (supply chain/SBOM — nuançado), 20 (capstone comparativo). As demais → sonnet. **Quase todas as notas são version-specific** e fazem WebFetch no Step 1 (ver §4.3.3 e §6).

**Decisões de fronteira (escopo de outro dono — link-back ou texto "(planejado)"):**
- **JPMS / módulos / `jlink` / GraalVM AOT (mecanismo)** → Galho 3. Notas 13/15 linkam. GraalVM **native image** (build nativo de produção) é **Galho 17 (planejado)** — só menção conceitual.
- **`jpackage` / empacotamento nativo (instaladores desktop)** → Galho 6 (JavaFX/13). Nota 15 linka, **não re-explica**.
- **Starters / auto-configuration / `spring-boot-maven-plugin` (mecanismo Spring)** → Galho 8. Notas 11/15 linkam o BOM/repackage como casos concretos; o mecanismo é lá.
- **Teoria de teste/cobertura/mutation (Surefire/Failsafe/JaCoCo como métrica/PIT)** → Galho 13. Nota 16 cobre o **ângulo de build** (plugar e falhar), não a teoria.
- **Containers/Docker/buildpacks/GraalVM native/deploy/observabilidade de produção** → Galho 17 (planejado).
- **Monorepo vs multi-repo de microservices / Spring Cloud** → Galho 16 (planejado). A nota 12 (multi-módulo) é **estrutura de build de UM projeto**, não topologia de repositórios de microservices.
- **CI/CD propriamente (pipelines, GitHub Actions, etc.)** → Galho 17 (planejado). O galho 15 cobre o build **localmente reprodutível e CI-friendly** (wrapper, cache, version pinning), não a esteira.

### 3.2. MOC do galho

`03-Dominios/Java/Build e tooling/index.md`:
- `type: moc`, `status: growing`, `publish: true`, `created`/`updated: 2026-06-11`
- Frontmatter padrão (`title: "Build, tooling e ecossistema"`, tags `java`/`build`/`moc`, aliases `["Build, tooling e ecossistema", "Build e tooling", "Build Tools", "Maven e Gradle", "Galho 15 - Build"]`)
- `> [!abstract] TL;DR` callout — 2-4 linhas: galho cobre como um projeto Java é construído/versionado/empacotado/publicado (Maven, Gradle, dependências/BOM, multi-módulo, JDK distributions, annotation processing, packaging, quality gates, supply chain); a tese (build tool resolve grafo de deps + reprodutibilidade; Maven vs Gradle = convenção vs flexibilidade); **20 notas em 3 fases**
- "Sobre este galho" + audiência primária/secundária + nota de que é galho **NOVO/PESQUISA** com **poda reversa mínima** (Spring Boot.md) + a **fronteira-assinatura quádrupla** (G3/G6/G8/G13)
- Conteúdo em 3 H2 (`## Iniciado` / `## Adepto` / `## Magus`) com wikilinks pras 20 notas (uma linha descritiva cada)
- **Rotas alternativas (5):**
  - **Completa** — 01 → 20 em ordem
  - **Entrevista internacional** — 01 → 02 → 05 → 08 → 09 → 10 → 11 → 18 → 20 (modelo, Maven, Gradle, decisão, JDK/licença, conflitos, BOM, supply chain, capstone — o que mais cai)
  - **Maven na prática** — 02 → 03 → 04 → 10 → 11 → 12 → 15 → 19 (modelo, deps/scopes, plugins, conflitos, BOM, multi-módulo, packaging, publicar)
  - **Gradle na prática** — 05 → 06 → 07 → 10 → 11 → 12 (modelo, deps/catalogs, performance, conflitos, platform/BOM, multi-project)
  - **Build production-grade / supply chain** — 09 → 16 → 17 → 18 → 19 (JDK, quality gates, reprodutibilidade, SBOM, publicação)
- "Veja também": MOC central `[[03-Dominios/Java/index|Trilha Java]]`, **G3** (JVM/JPMS/jlink), **G6** (jpackage), **G8** (starters/repackage), **G13** (testes/JaCoCo/PIT), Dicionário de Java; Galhos 16/17/18 como texto "(planejado)" sem wikilink
- Dataview "Todas as notas do galho" (TABLE fase/status; **inline code nunca começa com `=`** — lição da memória)

### 3.3. Dicionário de Java (EXPANSÃO — não recriar)

`03-Dominios/Java/Dicionário de Java.md` já existe (**437 verbetes** após o Galho 14, `type: glossary`, `updated: 2026-06-11`, seções alfabéticas únicas `## A`…`## Z` com verbetes `### `). Este galho **expande** o arquivo inserindo os verbetes **em ordem alfabética case-insensitive (sem acento, ignorando símbolos iniciais)** nas seções de letra apropriadas. **Nunca recriar o arquivo nem reordenar verbetes existentes.** Manter `updated: 2026-06-11`.

Verbetes a inserir (~32, conferir dups antes via grep):

`artifact (artefato Maven)`, `BOM (Bill of Materials)`, `build cache (Gradle)`, `Central Portal`, `Checkstyle`, `configuration (Gradle)`, `configuration cache (Gradle)`, `coordenadas GAV`, `CycloneDX`, `dependencyManagement`, `dependency scope (Maven)`, `dependency tree`, `fat jar / uber jar`, `GraalVM (distribuição)`, `Gradle`, `incremental build`, `JDK distribution`, `jlink (no build)`, `Kotlin DSL (Gradle)`, `lifecycle (Maven)`, `Lombok`, `MapStruct`, `Maven`, `Maven Central`, `multi-module (reactor)`, `nearest-wins (mediation)`, `NFTC (No-Fee Terms and Conditions)`, `OpenJDK`, `phase (Maven)`, `POM`, `reproducible build`, `SBOM`, `SDKMAN`, `SLSA`, `Temurin (Adoptium)`, `thin jar`, `toolchain (build)`, `Version Catalog`, `wrapper (mvnw/gradlew)`.

Cada verbete: definição curta (1-3 linhas) em PT-BR + `Veja também:` apontando pra(s) nota(s) canônica(s) do galho. **Conferir com grep os verbetes já existentes** para **não duplicar** — possíveis colisões: `auto-configuration`/`starter` (Galho 8 — linkar, não duplicar); `JaCoCo`/`Surefire`/`mutation testing`/`PIT` (Galho 13 — se existirem, linkar do ângulo de build); `GraalVM`/`AOT`/`módulos (JPMS)`/`jpackage` (Galho 3/6 — se existirem, linkar). Quando um termo tocar um já existente, **linkar entre si** em vez de criar segundo verbete. **Conferir 1:1** que os headings batem com âncoras `[[Dicionário de Java#...]]` usadas nas notas.

### 3.4. MOC central (ativação do Galho 15)

`03-Dominios/Java/index.md` já existe. Task **mínima**: trocar a linha do Galho 15 (atualmente `15. Build, tooling e ecossistema *(planejado)* — Maven, Gradle, BOM, multi-module, JDK distributions`) por wikilink ativo no padrão dos galhos fechados:

```markdown
15. [[03-Dominios/Java/Build e tooling/index|Build, tooling e ecossistema]] — Maven e Gradle (modelo, lifecycle/tasks, performance), gestão de dependências (resolução transitiva, conflitos, BOM), multi-módulo, distribuições do JDK e licenciamento, annotation processing (Lombok/MapStruct), empacotamento, quality gates no build e cadeia de suprimentos (reproducible builds, SBOM, Maven Central)
```

Atualizar `updated` para `2026-06-11`. Não mexer no resto do MOC central. **Confirmar o número da linha na execução** (lendo o arquivo primeiro — hoje é a linha 48).

### 3.5. Poda reversa em `Backend/Spring Boot.md` (conservadora)

O pré-flight confirmou **dívida reversa pequena e localizada**, toda em `Backend/Spring Boot.md` (+ um auto-reconhecimento em `Spring Core e Boot/16`). Política: **conservadora** — a explicação **canônica** passa a viver no galho 15; nos arquivos do Spring fica um **resumo curto + wikilink** quando a menção for pedagogicamente relevante ao contexto Spring; poda integral só onde o conteúdo é puramente de build.

| # | Arquivo:linha (aprox., confirmar via grep) | Conteúdo | Ação |
|---|---|---|---|
| 1 | `Backend/Spring Boot.md` ~297-307 | **Lombok** (`@Data` vs `@Getter/@Setter`, armadilha com JPA/`equals/hashCode`) | A armadilha Lombok+JPA é **relevante no contexto Spring** → **manter um resumo curto**, mover o tratamento canônico de Lombok pra **nota 14** e adicionar wikilink `[[.../14 - Annotation processing|...]]`. **Não apagar a armadilha JPA** (é Spring/persistência). |
| 2 | `Backend/Spring Boot.md` ~297-305 | **MapStruct** (compile-time mapping, `componentModel = "spring"`) | Tratamento canônico → **nota 14**; em Spring Boot.md, resumo curto + wikilink. |
| 3 | `Backend/Spring Boot.md` ~313 / `Spring Core e Boot/16` | **`spring-boot-maven-plugin`/repackage/layered jar** (já diz "coberto no Galho 15/17 (planejado)") | Trocar o texto "(planejado)" por **wikilink ativo** pra **nota 15** (empacotamento). O `repackage` como mecanismo Spring continua em G8; o **layered jar/packaging genérico** passa a apontar pro galho 15. |

**NÃO TOCAR** em `Backend/Spring Data JPA.md`, `Backend/Spring Security.md`, `Backend/Testes em Java.md`, `Backend/Kafka/**`, nem em qualquer nota dos Galhos 1-14 além dos cross-links abaixo. **Confirmar todos os números de linha via grep na execução** (`Lombok`, `MapStruct`, `spring-boot-maven-plugin`, `layered`, `Galho 15`).

### 3.6. Cross-links (após as notas existirem)

| # | Arquivo | Ação |
|---|---|---|
| 1 | `03-Dominios/Java/index.md` | ativação do Galho 15 (§3.4) |
| 2 | `JVM/08 - JPMS — o sistema de módulos.md` (se houver gancho/"Veja também") | cross-link pra **nota 13/15** (toolchains/empacotamento) — **só se já houver seção "Veja também"**; não forçar |
| 3 | `JavaFX/13 - Empacotamento — módulos, jlink e jpackage.md` | cross-link pra **nota 15** (empacotamento, ângulo build) no "Veja também", se existir |
| 4 | `Spring Core e Boot/15 - Auto-configuration e starters.md` | cross-link pra **nota 11** (BOM) se houver "Veja também"; menção do `spring-boot-dependencies` como BOM |
| 5 | `Testes/17 - Mutation testing — PIT e cobertura honesta.md` | cross-link pra **nota 16** (quality gates) se houver "Veja também" |

**Conservador:** cross-links de volta só onde a nota-dona já tem seção "Veja também" e o link agrega; **não inflar** notas fechadas. O grosso da ligação é **das notas novas → notas-fronteira** (sempre), não o contrário.

**NÃO quitar (permanece "(planejado)"):** horizonte-lists de uma linha nos índices dos galhos que listam "15, 16, 17 — planejados"; Galhos 16/17/18 permanecem texto "(planejado)" em todo lugar. Quitar só a linha do Galho 15 no MOC central (§3.4) e os 3 pontos de poda (§3.5).

## 4. Convenções por nota

Herda §7 do roadmap e §4 dos specs dos galhos de pesquisa (5/7/11/14). Reforços específicos:

### 4.1. Frontmatter

```yaml
---
title: "<título>"
created: 2026-06-11
updated: 2026-06-11
type: concept
status: seedling
publish: true
fase: iniciado | adepto | magus
tags:
  - java
  - build
  - <fase>
  - <tags específicas: maven, gradle, dependencias, bom, jdk, sdkman, lombok, mapstruct, packaging, supply-chain, sbom, multi-module, toolchains, quality, ...>
aliases:
  - <aliases opcionais>
---
```

H1 `# Título` após o frontmatter.

### 4.2. Estrutura H2 obrigatória

- `> [!abstract] TL;DR` (callout, NÃO H2) — 2-4 linhas: conceito + regra prática + por que importa
- `## O que é` / `## Por que importa` / `## Como funciona` (≥3 subseções H3 em notas Adepto/Magus)
- `## Na prática` — exemplos compiláveis; framing **neutro** (`com.example`, `Order`/`Payment`/`OrderService`, módulos `app`/`core`/`domain`); "padrão observado em projetos Java"; NUNCA `MedEspecialista`/"da minha experiência"/"no meu projeto"/"quando configurei o build"
- `## Armadilhas` — **≥2** (Iniciado) / **≥3** (Adepto/Magus), cada uma com `### (N) Título` (H3 numerado, NÃO callout `[!warning]`) + descrição + exemplo curto + fix em 1 linha
- `## Em entrevista` — `### Frase pronta (inglês)` com **3+ sentenças** (trade-off + decisão + caveat) + `### Vocabulário` com tabela `| Termo PT | Termo EN |` de **6+ termos**
- `## Veja também` — wikilinks **SEM backticks**, **SEM âncoras same-file**; sempre inclui notas relacionadas do galho + `[[03-Dominios/Java/Build e tooling/index|MOC do galho]]` + `[[03-Dominios/Java/index|Trilha Java]]` + (quando aplicável) a nota da fronteira (G3 JPMS/jlink, G6 jpackage, G8 starters/repackage, G13 testes) + verbetes do Dicionário
- `## Referências` — docs oficiais (`maven.apache.org`, `docs.gradle.org`, `oracle.com/java`, `adoptium.net`, `projectlombok.org`, `mapstruct.org`, `cyclonedx.org`, `central.sonatype.org`)

### 4.3. Restrições absolutas

1. **Fronteira-assinatura (linkar de volta, não re-explicar)** — JPMS/jlink/GraalVM-AOT → G3; jpackage → G6; starters/repackage/auto-config → G8; teoria de teste/cobertura/mutation → G13. **Nunca re-explicar** o sistema de módulos, jpackage, o mecanismo de auto-configuration, ou a pirâmide de testes — apontar. Galhos 16/17/18 = texto "(planejado)", sem wikilink.
2. **Sem fabricação** de experiência pessoal. Exemplos neutros (`com.example`, `Order`, `Payment`, módulos `app`/`core`) — NUNCA `MedEspecialista`/`josenaldo`/1ª pessoa/"no meu build"/"incidente de dependência em produção". **Zero estatística de adoção inventada** (ex.: "X% dos projetos usam Maven"); números só com fonte verificável (e o pré-flight não achou nenhuma fonte de market-share — então **não citar percentuais de adoção**).
3. **Sem invenção** de versões/APIs/comportamentos. WebFetch obrigatório no Step 1 das notas version-specific e pra **toda afirmação version-specific**. **Versões cravadas no pré-flight (2026-06-11) — re-confirmar na execução, mas estes são os fatos-base:**
   - **Maven 3.9.16** (GA, 2026-05-13) é a linha estável; **Maven 4.0.0-rc-5** (2025-11-13) **NÃO é GA** em jun/2026 — tratar Maven 4 como "próxima major, ainda RC", citando suas mudanças (consumer/flattened POM, `<packaging>bom</packaging>` nativo, sintaxe de versão CI-friendly, reproducible builds por padrão) como **"vindo no Maven 4"**, não como presente. O **Maven Wrapper NÃO vem por padrão** (gerado via `wrapper:wrapper`).
   - **Gradle 9.5.1** (2026-05-12) é a versão estável; **Gradle 9.0** (2025-07-31) exige **Java 17+**. **Kotlin DSL é o default recomendado desde Gradle 8.0**; Groovy DSL **não está deprecado**. **Configuration cache** é o "preferred mode" desde 9.0 mas **ainda opt-in** (não default). **Version Catalogs** são estáveis e recomendados.
   - **Lombok 1.18.46** (2026-04-22) — suporta JDK 21 (desde 1.18.30), JDK 25 (desde 1.18.40), JDK 26. **`lombok-mapstruct-binding`** é necessário pra Lombok+MapStruct juntos (desde Lombok 1.18.16). **MapStruct 1.6.3** (GA, 2024-11-09); 1.7.0.Beta1 (2026-02-01) existe como beta.
   - **Java LTS: 17, 21 (set/2023), 25 (16/09/2025)**; cadência LTS mudou pra **a cada 2 anos**; próxima LTS **Java 29 (set/2027)**. Non-LTS recentes: Java 24 (mar/2025), **Java 26 (17/03/2026)**. Modelo de release de 6 meses.
   - **Oracle JDK** sob **NFTC** (No-Fee Terms and Conditions) pra v21+ (uso de produção/redistribuição sem taxa); a confusão veio da licença comercial de 2019 (Java 11), corrigida com a NFTC em 2021. **OpenJDK = projeto/código**; Temurin/Corretto/Zulu/Liberica/MS = builds **GPLv2+Classpath Exception**; **GraalVM = GFTC**.
   - **Reproducible builds**: `project.build.outputTimestamp`; **default ativo a partir do Maven 4** (4.0.0-beta-5+, MNG-8258); validação via `maven-artifact-plugin` (`check-buildplan`/`compare`).
   - **CycloneDX 1.6** é padrão **Ecma International** (desde 26/06/2024); `cyclonedx-maven-plugin`/`cyclonedx-gradle-plugin` existem; SPDX é alternativa menos adotada em Java. **SLSA** (níveis L1-L3), **OWASP Dependency-Check** (SCA).
   - **Maven Central**: **OSSRH descontinuado em 30/06/2025**; **Central Portal** (`central-publishing-maven-plugin`) é o caminho atual; o `maven-deploy-plugin` legado contra OSSRH não funciona mais.
   - **SDKMAN** pra instalar/trocar versões de JDK (e Maven/Gradle) localmente.
4. **Code samples compiláveis/válidos** — `pom.xml` (XML válido, coordenadas reais), `build.gradle.kts` (Kotlin DSL como default; mostrar Groovy quando o contraste importar), `libs.versions.toml`, `toolchains.xml`, CLI (`mvn`/`gradle`/`sdk`). Fences corretas: ` ```xml ` (POM/config Maven), ` ```kotlin ` (build.gradle.kts) ou ` ```groovy ` (build.gradle), ` ```toml ` (version catalog), ` ```properties `/` ```yaml `, ` ```bash ` (CLI), ` ```text ` (árvores de arquivo/dependency tree/output), ` ```java ` (quando houver código). Sempre fechadas.
5. **Comparações justas** — Maven vs Gradle, XML vs DSL, declarativo vs imperativo, fat jar vs thin jar, nearest-wins vs highest-version, BOM vs Version Catalog, Oracle JDK vs Temurin, monolito modular vs multi-módulo: sempre "quando X" E "quando Y". O capstone (20) é o ápice (o comparativo lado a lado + mapa de decisão, sem dogma).
6. **Wikilinks sem backticks** em "Veja também"; MOC do galho + MOC central obrigatórios. **Não linkar galhos inexistentes** (16/17/18) — texto "(planejado)". Wikilinks pras notas-fronteira usam **path completo** e o **título EXATO** do arquivo (conferir 1:1 — lição do Galho 12: a nota inventou títulos; os paths de fronteira têm nomes longos com em-dash `—`).
7. **`fase:` no frontmatter + na tag** — obrigatório.
8. **Higiene de commits** — sem `Co-Authored-By: Claude`, sem `--no-verify`, `git add <path>` nominal (nunca `-A` — bot de backup Obsidian Git roda em timer), 1 commit por nota/artefato, controlador commita (subagents write-only). Guardar contra `.git/index.lock`.
9. **Tom pedagógico graduado** — Iniciado assume Galhos 1-2 (linguagem) e que o leitor já compilou algo; Adepto assume que já produziu um jar e usou Spring (G8); Magus assume o stack inteiro + a tese honesta (build é grafo de deps + reprodutibilidade; a escolha é trade-off, não dogma).
10. **Registro Feynman onde couber** (memória `feedback_enriquecimento_feynman`): analogias pro que é abstrato (o repositório local como "cache de bibliotecas", o BOM como "lista de preços com versões combinadas", nearest-wins como "o parente mais próximo ganha a discussão"), perguntas retóricas, callouts. Sem inflar — registro didático, não enchimento.

## 5. Conteúdo por nota (síntese)

Notas de pesquisa fundadas em doc oficial via WebFetch. Fontes-base: `maven.apache.org/guides` + `maven.apache.org/ref/current`, `docs.gradle.org/current/userguide`, `gradle.org/releases`, `oracle.com/java/technologies/java-se-support-roadmap.html` + `jdk-faqs`, `adoptium.net`, `bell-sw.com`/`azul.com` (comparativos de distro), `projectlombok.org`, `mapstruct.org`, `cyclonedx.org`, `slsa.dev`, `central.sonatype.org`, `sdkman.io`.

- **01 — Por que build tools existem (pesquisa, opus, assinatura).** `javac`/`jar` manual não escala; o que Maven/Gradle resolvem; build tool ≠ compilador; a fronteira quádrupla. Armadilhas: "build tool é só pra compilar"; ignorar o build até quebrar. Fontes: maven.apache.org, docs.gradle.org.
- **02 — Maven, o modelo (pesquisa).** POM, GAV, repositório local/remoto, lifecycle/phases/goals. **Maven 3.9.x atual; Maven 4 RC (WebFetch).** Armadilhas: confundir phase com goal; achar que `package` roda `install`. Fontes: maven.apache.org.
- **03 — Maven deps e scopes (pesquisa).** Scopes, transitividade, exclusions, optional. Armadilhas: `provided` esperando runtime; não excluir transitiva conflitante. Fontes: maven.apache.org (dependency mechanism).
- **04 — Maven plugins/profiles/wrapper (pesquisa).** Plugins essenciais, profiles, `mvnw` (não vem por padrão — WebFetch). Armadilhas: abusar de profiles (build não-reprodutível); commitar sem wrapper. Fontes: maven.apache.org (plugins, wrapper).
- **05 — Gradle, o modelo (pesquisa).** Groovy vs Kotlin DSL (**KTS default desde 8.0**, WebFetch), tasks/DAG, configurations, plugins. Armadilhas: pensar em Gradle como "Maven em código"; task sem inputs/outputs (quebra incremental). Fontes: docs.gradle.org.
- **06 — Gradle deps/Version Catalogs/wrapper (pesquisa).** `implementation` vs `api`, Version Catalogs (`libs.versions.toml`, WebFetch), `gradlew`. Armadilhas: tudo `api` (vaza classpath); hardcode de versão em vez de catalog. Fontes: docs.gradle.org (java library plugin, platforms).
- **07 — Gradle performance (pesquisa).** Incremental build, build cache (local/remoto), configuration cache (preferred 9.0, opt-in — WebFetch), daemon. Armadilhas: task não-cacheável por output não-declarado; desligar o daemon em dev. Fontes: docs.gradle.org (build cache, configuration cache, incremental).
- **08 — Maven vs Gradle (pesquisa, opus).** Declarativo/convenção vs imperativo/flexível; XML vs DSL; performance; ecossistema. Sem dogma. Armadilhas: escolher por hype; migrar sem motivo. Fontes: maven.apache.org, docs.gradle.org (migrating guides).
- **09 — Distribuições do JDK (pesquisa, opus, version-heavy).** OpenJDK vs distribuição; Oracle NFTC e a confusão pós-2019; Temurin/Corretto/Zulu/Liberica/MS/GraalVM e licenças; LTS 17/21/25 (cadência 2 anos), non-LTS 24/26; SDKMAN. **Tudo WebFetch.** Armadilhas: achar que precisa pagar Oracle; misturar versão de build e de runtime. Fontes: oracle.com (roadmap/faqs), adoptium.net, bell-sw.com, sdkman.io.
- **10 — Resolução e conflitos (pesquisa, opus).** Transitiva; **nearest-wins (Maven)** vs **highest-version/resolution strategy (Gradle)**; dependency tree; diagnosticar `NoSuchMethodError`. Armadilhas: confiar na resolução implícita; resolver conflito com `force` sem entender. Fontes: maven.apache.org (mediation), docs.gradle.org (dependency resolution).
- **11 — BOM e dependency management (pesquisa).** `dependencyManagement`, BOM `import`, `spring-boot-dependencies` (fronteira G8), `platform()` no Gradle. Armadilhas: declarar versão em cada módulo; ignorar o BOM e ter versões divergentes. Fontes: maven.apache.org, docs.gradle.org (platforms), docs.spring.io (link).
- **12 — Multi-módulo (pesquisa).** Reactor Maven (parent/modules, herança vs agregação, build order) vs multi-project Gradle (`include`, convention plugins). Quando dividir. Armadilhas: módulos demais (overhead); dependência circular entre módulos. Fontes: maven.apache.org, docs.gradle.org (structuring builds).
- **13 — Toolchains (pesquisa).** Maven toolchains + `release`; Gradle toolchains (auto-provisioning). Liga G3. Armadilhas: buildar com JDK errado e não notar; `source/target` em vez de `release`. Fontes: maven.apache.org (toolchains), docs.gradle.org (toolchains).
- **14 — Annotation processing (pesquisa).** APT; Lombok (AST, JDK 21/25-ready, WebFetch); MapStruct (`componentModel=spring`); **lombok-mapstruct-binding** + ordem de processors. **Recebe poda do Spring Boot.md.** Armadilhas: Lombok+MapStruct sem o binding (mapper vazio); `-parameters` faltando. Fontes: projectlombok.org, mapstruct.org.
- **15 — Empacotamento (pesquisa).** Jar simples vs fat/uber (Shade/Shadow, relocation) vs thin; `spring-boot:repackage`/layered jar (fronteira G8/17); **jlink/jpackage = fronteira G3/G6 (linka).** **Recebe poda do layered jar.** Armadilhas: fat jar com resource merge quebrado; layered sem necessidade. Fontes: maven.apache.org (shade), docs.gradle.org (shadow/application), docs.spring.io (link).
- **16 — Quality gates (pesquisa).** JaCoCo (`check`/minimum), Checkstyle, PMD, SpotBugs no lifecycle; falhar build vs reportar. Fronteira G13 (Surefire/Failsafe/PIT). Armadilhas: threshold de cobertura como teatro; gate que ninguém olha. Fontes: jacoco.org, checkstyle docs, spotbugs/pmd docs, maven/gradle plugin docs.
- **17 — Reprodutibilidade (pesquisa).** `project.build.outputTimestamp`; default no Maven 4 (WebFetch); `maven-artifact-plugin` compare; version pinning. Armadilhas: timestamps/ordem não-determinística; `RANGE`/`LATEST` de versão. Fontes: maven.apache.org (reproducible builds guide).
- **18 — Supply chain e SBOM (pesquisa, opus).** SBOM; CycloneDX 1.6 (Ecma, WebFetch) vs SPDX; SLSA; SCA/OWASP Dependency-Check; proveniência. Pós-Log4Shell. Armadilhas: SBOM gerado e nunca consumido; achar que CVE scan cobre typosquatting. Fontes: cyclonedx.org, slsa.dev, owasp.org (dependency-check).
- **19 — Publicação (pesquisa).** Nexus/Artifactory (interno) vs Maven Central; **OSSRH descontinuado, Central Portal** (WebFetch); GPG/sources/javadoc; `maven-publish`/`signing` Gradle; SNAPSHOT vs release. Armadilhas: publicar SNAPSHOT como release; metadata incompleta rejeitada pelo Central. Fontes: central.sonatype.org, docs.gradle.org (publishing).
- **20 — Capstone (pesquisa, opus, comparativo).** O mesmo projeto multi-módulo Maven ⇄ Gradle lado a lado (árvore, deps+BOM, JaCoCo/Checkstyle, SBOM, empacotar, publicar); **tabela de decisão**; cheatsheet nota→problema; munição de entrevista. Armadilhas de raciocínio: "Gradle é sempre mais rápido"; "preciso de multi-módulo"; "tenho que pagar pelo JDK". Fontes: maven.apache.org, docs.gradle.org.

## 6. Pré-flight: verificações feitas

Executado nesta fase de brainstorming (2026-06-11); itens version-specific re-confirmados na execução de cada nota via WebFetch:

1. **Estrutura da trilha confirmada** — MOC central é `03-Dominios/Java/index.md` (`Java.md` é legado); Galho 15 listado como `*(planejado)*` na linha 48. Padrão de nota `type: concept`/`fase`/`publish: true`; template de MOC e de nota = Galho 14 (Mensageria).
2. **Galho NOVO/PESQUISA confirmado** — pré-flight não achou tronco de build disperso. Só menções pontuais em `Backend/Spring Boot.md` (Lombok ~297-307, MapStruct ~297-305, `spring-boot-maven-plugin`/layered jar ~313) e auto-reconhecimento em `Spring Core e Boot/16` ("coberto no Galho 15/17 (planejado)"). **Poda reversa conservadora** (§3.5).
3. **Fronteira-assinatura quádrupla confirmada (paths exatos):**
   - G3 → `JVM/08 - JPMS — o sistema de módulos.md`, `JVM/01 - A JVM — o que é e o pipeline de execução.md`
   - G6 → `JavaFX/13 - Empacotamento — módulos, jlink e jpackage.md` (jpackage **já coberto**)
   - G8 → `Spring Core e Boot/15 - Auto-configuration e starters.md`, `Spring Core e Boot/16 - SpringApplication e o embedded server.md`
   - G13 → `Testes/17 - Mutation testing — PIT e cobertura honesta.md`, `Testes/01 - O que é testar em Java — a pirâmide e o stack moderno.md`
4. **Dicionário** — **437 verbetes** após o Galho 14; seções `## A`…`## Z`; verbetes `### `; `updated: 2026-06-11`. Possíveis dups a linkar (não duplicar): `auto-configuration`/`starter` (G8), `JaCoCo`/`Surefire`/`mutation testing`/`PIT` (G13), `GraalVM`/`AOT`/`módulos (JPMS)`/`jpackage` (G3/6). Expansão alfabética (~32), nunca recriar/reordenar.
5. **MOC central** — linha 48 (`15. Build, tooling e ecossistema *(planejado)*`); galhos ativos usam `N. [[path/index|Title]] — summary`; `updated: 2026-06-11`. Confirmar a linha na execução.
6. **Versões CRAVADAS via WebFetch (2026-06-11)** — Maven 3.9.16 GA / Maven 4.0.0-rc-5 (não GA); Gradle 9.5.1 (9.0 exige Java 17+); Kotlin DSL default desde 8.0 (Groovy não deprecado); config cache preferred 9.0 mas opt-in; Version Catalogs estáveis; Lombok 1.18.46 (JDK 21/25/26 ok) + `lombok-mapstruct-binding`; MapStruct 1.6.3 GA; Java LTS 17/21/25 (cadência 2 anos, próxima 29/2027), non-LTS 24/26; Oracle NFTC v21+; OpenJDK=projeto, distros=builds; CycloneDX 1.6 (Ecma); reproducible builds default no Maven 4; OSSRH descontinuado 30/06/2025 → Central Portal; SDKMAN. (Detalhes em §4.3.3.) **Re-confirmar na execução.**
7. **Troncos/arquivos intocáveis** — todos os artefatos dos Galhos 1-14 exceto: ativação do MOC central (§3.4), poda conservadora em `Backend/Spring Boot.md` + `Spring Core e Boot/16` (§3.5), e cross-links opcionais (§3.6). Pasta `Build e tooling/` ainda **não existe**.

Nenhum número de adoção/market-share é inventado (o pré-flight não achou fonte — **não citar percentuais**). Quando faltar fato verificável, **PERGUNTAR** antes de escrever.

## 7. Critérios de aceitação do galho

Além dos critérios gerais (§10 do roadmap):

1. 20 notas em `03-Dominios/Java/Build e tooling/`, frontmatter completo com `fase:`, `publish: true`, distribuídas 9/6/5.
2. MOC do galho com 3 subseções de fase + 5 rotas alternativas + dataview (inline code nunca inicia com `=`) + folder-link resolve (`index.md` presente).
3. Dicionário de Java **expandido** (não recriado) com ~32 verbetes; verbetes dos Galhos 1-14 intactos; `updated: 2026-06-11`; dups conferidos e linkados (não duplicar `auto-configuration`/`starter`/`JaCoCo`/`PIT`/`GraalVM`/`jpackage`).
4. MOC central `Java/index.md` com Galho 15 ativado (linha 48 vira wikilink); resto intacto; `updated: 2026-06-11`.
5. **Poda reversa executada e conservadora**: Lombok/MapStruct/layered-jar em `Backend/Spring Boot.md` (+ `Spring Core e Boot/16`) reduzidos a resumo + wikilink pras notas 14/15; a armadilha Lombok+JPA **mantida** no contexto Spring; "(planejado)" do packaging vira wikilink ativo. **Outros troncos intactos.**
6. **Cross-links**: das notas novas → fronteiras (sempre); de volta só onde a nota-dona já tem "Veja também" (conservador). Galhos 16/17/18 permanecem texto "(planejado)" em todo lugar; horizonte-lists intactos.
7. Cada nota: TL;DR; code samples válidos (POM XML / build.gradle.kts / toml / CLI; fences `xml`/`kotlin`/`groovy`/`toml`/`properties`/`yaml`/`bash`/`text`/`java`); "Em entrevista" com `### Frase pronta (inglês)` 3+ sentenças + `### Vocabulário` tabela 6+ termos PT→EN; "Armadilhas" com `### (N) Título` numerado + exemplo + fix (≥2 Iniciado, ≥3 Adepto/Magus); wikilinks (galho + MOC central + fronteira quando aplicável + Dicionário); "Referências" com docs oficiais verificadas.
8. **Fronteira-assinatura respeitada**: JPMS/jlink/GraalVM-AOT → G3; jpackage → G6; starters/repackage → G8; teoria de teste/cobertura/mutation → G13; nada re-explicado; galhos 16/17/18 só texto "(planejado)".
9. **Fronteiras de escopo respeitadas**: containers/GraalVM native/deploy/produção = Galho 17; microservices/Spring Cloud = Galho 16; CI/CD = Galho 17; OCP = Galho 18; teoria de teste = Galho 13. Zero conteúdo de operação/deploy.
10. Zero fabricação de experiência pessoal; zero estatística de adoção inventada; afirmações version-specific citam a versão verificada via WebFetch (Maven/Gradle/Lombok/MapStruct/JDK/CycloneDX/Central Portal).
11. 1 commit por nota/artefato; sem `Co-Authored-By: Claude`; sem `--no-verify`; stage nominal (nunca `-A`); subagents write-only, controlador commita.
12. `verificar-wikilinks` roda limpo na pasta do galho (evitar âncoras same-file; conferir os títulos EXATOS das notas-fronteira — nomes longos com em-dash; lição do Galho 12).

## 8. Riscos e mitigações

| Risco | Mitigação |
|---|---|
| **Inventar versão "de memória"** (Maven 4 GA, Gradle, Lombok, JDK LTS, Central Portal) | Versões cravadas no pré-flight (§4.3.3); WebFetch no Step 1; Referências oficiais. Pontos minados: **Maven 4 ainda é RC** (não GA); **OSSRH morreu (30/06/2025)** → Central Portal; **Kotlin DSL default desde 8.0**; **config cache opt-in**; **LTS a cada 2 anos**. |
| **Re-explicar fronteiras** (JPMS, jpackage, auto-configuration, pirâmide de testes) | Restrição 4.3.1; notas 13/15/16 explicitamente "linka, não re-explica"; review por fase confere link-back. |
| **Inventar estatística de adoção** ("X% usa Maven/Gradle") | Pré-flight não achou fonte → **proibido citar percentuais**; comparações qualitativas; números só com fonte verificável. |
| **Hype/dogma** ("Gradle é melhor", "Maven é legado", "tem que pagar o Oracle JDK") | A tese honesta (build = grafo+reprodutibilidade; escolha = trade-off; bytecode é o mesmo OpenJDK) fixada em 01/08/09/20; "quando X E quando Y" obrigatório; review por fase. |
| **Invadir Galho 17** (containers, GraalVM native, deploy, observabilidade de produção) | GraalVM native image = texto "(planejado)" (G17); o galho cobre AOT só como conceito de fronteira; layered jar é mencionado mas Docker/imagem é G17; review por fase. |
| **Invadir Galho 16** (microservices/Spring Cloud) ao falar de multi-módulo | Multi-módulo (nota 12) = **estrutura de build de UM projeto**; topologia de repos de microservices = texto "(planejado)" G16; review confere. |
| **Poda reversa agressiva demais** (apagar a armadilha Lombok+JPA que é relevante no Spring) | Política conservadora (§3.5): resumo + wikilink, não deleção; a armadilha JPA fica no contexto Spring; confirmar linhas via grep; review confere que Spring Boot.md não perdeu conteúdo pedagógico. |
| **Code samples inválidos** (POM/XML/Gradle DSL errados) | Snippets compiláveis/válidos; coordenadas reais; KTS como default + Groovy no contraste; fences corretas; review confere XML/DSL bem-formado. |
| **gRPC/Go-style cross-contamination** ou exemplos de domínio sensível | Framing neutro (`com.example`, `Order`/`Payment`, módulos `app`/`core`); NUNCA MedEspecialista/1ª pessoa; review por fase. |
| **Sobreposição entre notas** (02-04 Maven, 05-07 Gradle muito parecidas) | Foco distinto por nota (02 modelo, 03 deps, 04 plugins; 05 modelo, 06 deps, 07 performance); review por fase checa sobreposição. |
| **Cheatsheet/capstone inventar títulos de nota** (lição Galho 12) | Passar aos subagentes os títulos EXATOS das 20 notas + das notas-fronteira (em-dash); `verificar-wikilinks` ao fim; review do capstone confere 1:1. |
| Galho denso (20 notas) inflar notas individuais | Distribuição 9/6/5 fixada; se uma nota passar de ~600 linhas, dividir nota (não galho); capstone com cheatsheet enxuto. |
| Dicionário: duplicar verbete existente (`JaCoCo`, `GraalVM`, `jpackage`) | Grep dos existentes antes de inserir; tocar existente → **linkar**, não duplicar; inserção alfabética, nunca recriar. |
| Bot de backup (Obsidian Git) commitando no meio | Padrão dos Galhos 2-14: subagents write-only; controlador commita após cada nota com `git add` nominal (nunca `-A`); guardar contra `.git/index.lock`. |

## 9. Próximos passos

1. **Aprovação deste spec**
2. **Plano de execução** via skill `superpowers:writing-plans` → `docs/superpowers/plans/2026-06-11-java-galho-15-build-tooling-execution.md`
3. **Execução** via `superpowers:subagent-driven-development` **direto na `main`** (subagents write-only; sonnet por padrão, opus nas notas 01/08/09/10/18/20; review **por fase** + fix loop; push manual do usuário)
4. **Verificação** de wikilinks (incluindo os paths longos das notas-fronteira) + conferência de âncoras do Dicionário
5. **Atualização da memória** `project_trilha_java` (Galho 15 completo; próximo sugerido: 16 Microservices ou 17 Cloud-native) antes do próximo galho

## 10. Documentos relacionados

- `2026-06-02-java-senior-roadmap-design.md` — roadmap macro (18 galhos); Galho 15 em §5
- `2026-06-11-java-galho-14-mensageria-design.md` / `...-execution.md` — Galho 14 (galho anterior; molde de galho de pesquisa + MOC + Dicionário + ativação)
- `2026-06-11-java-galho-13-testes-design.md` — Galho 13 (dono de Surefire/Failsafe/JaCoCo/PIT — fronteira da nota 16)
- `2026-06-08-java-galho-08-spring-core-design.md` — Galho 8 (dono de starters/auto-config/spring-boot-maven-plugin — fronteira das notas 11/15; alvo da poda reversa em Spring Boot.md)
- `2026-06-05-java-galho-03-jvm-design.md` — Galho 3 (dono de JPMS/jlink/GraalVM — fronteira das notas 13/15)
- Galho 6 (JavaFX) — dono de jpackage (fronteira da nota 15)
- Galhos 5/7/11/14 — template de **galho de pesquisa** (sem tronco a podar)
- Artefatos a criar/atualizar: `03-Dominios/Java/Build e tooling/**` (20 notas + MOC), `03-Dominios/Java/Dicionário de Java.md`, `03-Dominios/Java/index.md`, `03-Dominios/Java/Backend/Spring Boot.md` (poda conservadora), `03-Dominios/Java/Spring Core e Boot/16 - SpringApplication e o embedded server.md` (wikilink), cross-links opcionais (§3.6)
- Fontes-base do galho: `maven.apache.org`, `docs.gradle.org`/`gradle.org`, `oracle.com/java` (roadmap/faqs), `adoptium.net`, `bell-sw.com`/`azul.com`, `projectlombok.org`, `mapstruct.org`, `cyclonedx.org`, `slsa.dev`, `central.sonatype.org`, `sdkman.io`
- Memórias: [[project_trilha_java]], [[project_trilhas_fases_aprendizado]], [[project_tronco_galhos_pattern]], [[feedback_galhos_direto_main]], [[feedback_no_fabrication]], [[feedback_quartz_index]], [[feedback_commits]], [[feedback_dataview_inline_code]], [[feedback_notas_atomicas]], [[feedback_enriquecimento_feynman]]
