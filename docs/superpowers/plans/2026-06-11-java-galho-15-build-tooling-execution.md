# Galho 15 — Build, tooling e ecossistema (Java Senior) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Criar o Galho 15 da trilha Java Senior — 20 notas atômicas (por que build tools, Maven modelo/deps/plugins, Gradle modelo/deps/performance, Maven vs Gradle, distribuições do JDK, resolução de conflitos, BOM, multi-módulo, toolchains, annotation processing, empacotamento, quality gates, reprodutibilidade, supply chain/SBOM, publicação, capstone comparativo) em 3 fases + MOC do galho + expansão do Dicionário + ativação do MOC central + **poda reversa conservadora** em `Backend/Spring Boot.md` + cross-links.

**Architecture:** Padrão galhos + 3 fases (Iniciado/Adepto/Magus). Pasta flat `03-Dominios/Tecnologia/Java/Build e tooling/` (sem vírgula no path; título "Build, tooling e ecossistema"), notas `publish: true` em PT-BR, numeração global 01-20 (9/6/5). **Galho NOVO/PESQUISA** (como 5/7/11/14 — sem tronco a podar) + **poda reversa mínima** (Lombok/MapStruct/layered-jar em `Spring Boot.md` → resumo + wikilink; a armadilha Lombok+JPA fica no contexto Spring). **Fronteira-assinatura quádrupla**: JPMS/jlink/GraalVM-AOT → G3; jpackage → G6; starters/repackage/auto-config → G8; teoria de teste/cobertura/mutation → G13. **Tese honesta**: build tool resolve grafo de dependências + reprodutibilidade (não "compila"); Maven vs Gradle = convenção vs flexibilidade; o bytecode é o mesmo OpenJDK (a diferença entre distros é licença/suporte). Galhos 16/17/18 = texto "(planejado)", sem wikilink. **Direto na `main`** ([[feedback_galhos_direto_main]]); push manual do usuário.

**Tech Stack:** Obsidian Flavored Markdown, frontmatter YAML, wikilinks, callouts, Dataview, Quartz v4. Verificação via WebFetch (maven.apache.org, docs.gradle.org/gradle.org, oracle.com/java, adoptium.net, projectlombok.org, mapstruct.org, cyclonedx.org, slsa.dev, central.sonatype.org, sdkman.io).

---

## Convenções aplicadas a TODAS as notas (ler antes de qualquer task)

**Frontmatter** (ajustar `title`/`fase`/`tags`/`aliases` por nota; `created`/`updated: 2026-06-11`):

```yaml
---
title: "<título sem prefixo numérico>"
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
  - <1-3 tags de conceito: maven, gradle, dependencias, bom, jdk, sdkman, lombok, mapstruct, packaging, supply-chain, sbom, multi-module, toolchains, quality>
aliases:
  - <aliases>
---
```

H1 `# Título` após o frontmatter.

**Estrutura H2 obrigatória** (nesta ordem):

1. `> [!abstract] TL;DR` — 2-4 linhas. Callout, NÃO H2.
2. `## O que é` — definição.
3. `## Por que importa` — relevância pra senior/entrevista.
4. `## Como funciona` — H3s; mínimo 3 em Adepto/Magus.
5. `## Na prática` — código/config **válido**; framing neutro; **NUNCA** 1ª pessoa, `MedEspecialista`, `josenaldo`, "da minha experiência", "no meu build", "incidente de produção". Domínios neutros: `com.example`, `Order`, `Customer`, `Payment`, `OrderService`, módulos `app`/`core`/`domain`.
6. `## Armadilhas` — ≥2 (Iniciado) / ≥3 (Adepto/Magus). Cada uma: `### (N) Título` + descrição + exemplo curto + fix em 1 linha (H3 numerado, NÃO callout `[!warning]`).
7. `## Em entrevista` — `### Frase pronta (inglês)` com **3+ sentenças** + `### Vocabulário` **6+ termos** em tabela `| Termo PT | Termo EN |`.
8. `## Veja também` — wikilinks SEM backticks, SEM âncoras same-file. Sempre: notas do galho + `[[03-Dominios/Tecnologia/Java/Build e tooling/index|Build, tooling e ecossistema (MOC do galho)]]` + `[[03-Dominios/Tecnologia/Java/index|Trilha Java]]` + (quando aplicável) a nota da fronteira + verbetes do Dicionário.
9. `## Referências` — docs oficiais consultadas.

**Tamanho:** 200-500 linhas (densas até 600 — limite de [[feedback_notas_atomicas]]).

**Registro Feynman** (de [[feedback_enriquecimento_feynman]]) onde couber: analogias (repositório local = "cache de bibliotecas"; BOM = "lista de preços com versões combinadas"; nearest-wins = "o parente mais próximo ganha a discussão"; daemon do Gradle = "JVM que fica quente entre builds"), perguntas retóricas, callouts. Sem inflar.

**Restrições absolutas:**
- **FRONTEIRA-ASSINATURA (linkar de volta, NUNCA re-explicar).** Mapeamento de link-back (paths confirmados na Task 0):
  - **G3 (JVM/JPMS):** módulos/`jlink`/GraalVM-AOT → `03-Dominios/Tecnologia/Java/JVM/08 - JPMS — o sistema de módulos` + `03-Dominios/Tecnologia/Java/JVM/01 - A JVM — o que é e o pipeline de execução` (distros/Temurin/Corretto no ângulo runtime). **GraalVM native image = G17 (texto "planejado")** — só conceito de AOT como fronteira.
  - **G6 (JavaFX):** `jpackage`/empacotamento nativo → `03-Dominios/Tecnologia/Java/JavaFX/13 - Empacotamento — módulos, jlink e jpackage`. **NÃO re-explicar jpackage.**
  - **G8 (Spring Boot):** starters/auto-config/`spring-boot-maven-plugin`/`repackage` → `03-Dominios/Tecnologia/Java/Spring Core e Boot/15 - Auto-configuration e starters` + `03-Dominios/Tecnologia/Java/Spring Core e Boot/16 - SpringApplication e o embedded server`.
  - **G13 (Testes):** Surefire/Failsafe/JaCoCo(métrica)/PIT → `03-Dominios/Tecnologia/Java/Testes/17 - Mutation testing — PIT e cobertura honesta` + `03-Dominios/Tecnologia/Java/Testes/01 - O que é testar em Java — a pirâmide e o stack moderno`.
- **Galhos 16/17/18 só como texto "(planejado)", SEM wikilink.** Greps de review checam `\[\[[^]]*(Galho (16|17|18)|microservi|Spring Cloud|native image|GraalVM native|Docker|Kubernetes)`.
- Sem fabricação ([[feedback_no_fabrication]]); domínios neutros. **Zero estatística de adoção/market-share inventada** (o pré-flight não achou fonte — **proibido citar "X% usa Maven/Gradle"**); números só com fonte verificável.
- **Pesquisa pras partes version-specific (quase todas as notas):** WebFetch no Step 1. **Fatos cravados no pré-flight (2026-06-11) — re-confirmar, são a base:**
  - **Maven 3.9.16** (GA 2026-05-13) é a linha estável; **Maven 4.0.0-rc-5** (2025-11-13) **NÃO é GA** → Maven 4 é "próxima major, ainda RC"; suas features (consumer/flattened POM, `<packaging>bom</packaging>` nativo, sintaxe CI-friendly, reproducible builds por padrão) citadas como **"vindo no Maven 4"**, não presente. **Maven Wrapper NÃO vem por padrão.**
  - **Gradle 9.5.1** (2026-05-12); **Gradle 9.0** (2025-07-31) exige **Java 17+**. **Kotlin DSL = default recomendado desde Gradle 8.0**; Groovy **não deprecado**. **Configuration cache** = "preferred mode" desde 9.0 mas **ainda opt-in**. **Version Catalogs** estáveis/recomendados.
  - **Lombok 1.18.46** (2026-04-22) — JDK 21 (desde 1.18.30), JDK 25 (desde 1.18.40), JDK 26. **`lombok-mapstruct-binding`** necessário p/ Lombok+MapStruct (desde Lombok 1.18.16). **MapStruct 1.6.3** (GA 2024-11-09); 1.7.0.Beta1 existe.
  - **Java LTS: 17, 21 (set/2023), 25 (16/09/2025)**; cadência LTS = **a cada 2 anos**; próxima LTS **Java 29 (set/2027)**. Non-LTS: 24 (mar/2025), **26 (17/03/2026)**. Release de 6 meses.
  - **Oracle JDK** sob **NFTC** v21+ (a confusão veio da licença comercial de 2019/Java 11, corrigida com NFTC em 2021). **OpenJDK = projeto/código**; Temurin/Corretto/Zulu/Liberica/MS = **GPLv2+Classpath Exception**; **GraalVM = GFTC**.
  - **Reproducible builds**: `project.build.outputTimestamp`; **default a partir do Maven 4**; validação `maven-artifact-plugin` (`check-buildplan`/`compare`).
  - **CycloneDX 1.6** = padrão **Ecma** (26/06/2024); `cyclonedx-maven-plugin`/`cyclonedx-gradle-plugin`; SPDX = alternativa. **SLSA** (L1-L3), **OWASP Dependency-Check** (SCA).
  - **Maven Central**: **OSSRH descontinuado 30/06/2025**; **Central Portal** (`central-publishing-maven-plugin`) é o caminho atual.
  - **SDKMAN** p/ instalar/trocar JDK/Maven/Gradle localmente.
- **Não re-explicar o que é de outro galho:** JPMS/jlink/GraalVM-AOT → G3 (linkar); jpackage → G6 (linkar); starters/auto-config/repackage-mecanismo → G8 (linkar); pirâmide/teoria de teste/cobertura → G13 (linkar). Containers/native image/deploy → G17 (texto); microservices/Spring Cloud → G16 (texto); CI/CD pipeline → G17 (texto); OCP → G18 (texto).
- Comparações justas (quando X E quando Y): Maven vs Gradle, XML vs DSL, declarativo vs imperativo, fat vs thin jar, nearest-wins vs highest-version, BOM vs Version Catalog, Oracle JDK vs Temurin, monolito modular vs multi-módulo.
- Code fences: ` ```xml ` (POM/config Maven), ` ```kotlin ` (build.gradle.kts) / ` ```groovy ` (build.gradle), ` ```toml ` (version catalog), ` ```properties `/` ```yaml `, ` ```bash ` (CLI mvn/gradle/sdk), ` ```text ` (árvore de arquivos/dependency tree/output), ` ```java ` (código). Sempre fechadas.
- Commits: sem `Co-Authored-By: Claude`; sem `--no-verify`; `git add <path>` nominal (bot de backup roda em timer — NUNCA `-A`; guardar contra `.git/index.lock`); 1 commit por nota/artefato; direto na `main`; **sem push, sem deploy**. Subagents NÃO rodam git — o controlador commita.

**Modelo por nota:** sonnet por padrão; **opus** nas **01** (assinatura), **08** (Maven vs Gradle), **09** (distros/licença, version-heavy), **10** (resolução/conflitos), **18** (supply chain/SBOM), **20** (capstone comparativo).

**Fontes oficiais (base):**
- Maven: `https://maven.apache.org/guides/` + `https://maven.apache.org/ref/current/`
- Gradle: `https://docs.gradle.org/current/userguide/userguide.html` + `https://gradle.org/releases/`
- JDK roadmap/licença: `https://www.oracle.com/java/technologies/java-se-support-roadmap.html` + `.../javase/jdk-faqs.html`
- Distros: `https://adoptium.net/`, `https://bell-sw.com/`, `https://www.azul.com/`
- Lombok: `https://projectlombok.org/` ; MapStruct: `https://mapstruct.org/`
- Supply chain: `https://cyclonedx.org/`, `https://slsa.dev/`, `https://owasp.org/www-project-dependency-check/`
- Publicação: `https://central.sonatype.org/` ; SDKMAN: `https://sdkman.io/`

---

## Task 0: Pré-flight — pasta, terreno e baselines

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Build e tooling/` (pasta)

- [ ] **Step 1:** Confirmar `main` limpa: `git status` e `git branch --show-current` (deve ser `main`).
- [ ] **Step 2:** Criar a pasta do galho: `mkdir -p "03-Dominios/Tecnologia/Java/Build e tooling"`.
- [ ] **Step 3:** Confirmar os paths EXATOS das notas-fronteira (devem existir; usar nos wikilinks):
```bash
ls "03-Dominios/Tecnologia/Java/JVM/08 - JPMS — o sistema de módulos.md" \
   "03-Dominios/Tecnologia/Java/JVM/01 - A JVM — o que é e o pipeline de execução.md" \
   "03-Dominios/Tecnologia/Java/JavaFX/13 - Empacotamento — módulos, jlink e jpackage.md" \
   "03-Dominios/Tecnologia/Java/Spring Core e Boot/15 - Auto-configuration e starters.md" \
   "03-Dominios/Tecnologia/Java/Spring Core e Boot/16 - SpringApplication e o embedded server.md" \
   "03-Dominios/Tecnologia/Java/Testes/17 - Mutation testing — PIT e cobertura honesta.md" \
   "03-Dominios/Tecnologia/Java/Testes/01 - O que é testar em Java — a pirâmide e o stack moderno.md"
```
- [ ] **Step 4:** Confirmar a linha do Galho 15 no MOC central e o estado do Dicionário:
```bash
grep -n "15\. Build" "03-Dominios/Tecnologia/Java/index.md"
grep -c "^### " "03-Dominios/Tecnologia/Java/Dicionário de Java.md"   # baseline ~437
grep -ni "updated:" "03-Dominios/Tecnologia/Java/Dicionário de Java.md" | head -1
```
- [ ] **Step 5:** Localizar os pontos de poda reversa (números de linha p/ a Task 27):
```bash
grep -n "Lombok\|MapStruct\|spring-boot-maven-plugin\|layered\|Galho 15" "03-Dominios/Tecnologia/Java/Backend/Spring Boot.md"
grep -n "layered\|Galho 15\|repackage" "03-Dominios/Tecnologia/Java/Spring Core e Boot/16 - SpringApplication e o embedded server.md"
```
- [ ] **Step 6:** Conferir possíveis verbetes duplicados no Dicionário (linkar, não duplicar): `grep -ni "^### \(auto-configuration\|starter\|JaCoCo\|Surefire\|mutation\|PIT\|GraalVM\|AOT\|jpackage\|JPMS\|módulos\)" "03-Dominios/Tecnologia/Java/Dicionário de Java.md"`. Anotar quais já existem.

> Nenhum commit nesta task (só pasta vazia — será preenchida nas tasks seguintes; o `git add` da pasta acontece no 1º commit de nota).

---

## Fase Iniciado (notas 01-09)

> Cada nota: dispatch de subagente write-only com o texto da task + o bloco de Convenções. WebFetch no Step 1. Controlador commita após cada nota.

### Task 1: Nota 01 — Por que build tools existem *(opus, assinatura)*

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Build e tooling/01 - Por que build tools existem.md`

- [ ] **Step 1 (WebFetch):** `maven.apache.org/guides/` (introduction/what is Maven) + `docs.gradle.org/current/userguide/userguide.html` (what is Gradle) — confirmar a definição de cada um como "gestor de build + dependências".
- [ ] **Step 2 (escrever):** fase `iniciado`. O problema: `javac`+`jar` na mão não escala (classpath manual, dependências transitivas, ordem de compilação, empacotamento, reprodutibilidade). O que um build tool resolve: **grafo de dependências + lifecycle + artefato reprodutível**. **A nota-assinatura:** build tool ≠ compilador; a escolha Maven vs Gradle é convenção vs flexibilidade (aponta nota 08); a **fronteira quádrupla** (G3 módulos/jlink, G6 jpackage, G8 starters/repackage, G13 quality). Armadilhas (≥2): "build tool é só pra compilar"; ignorar o build até quebrar em CI. "Em entrevista" + "Veja também" (notas 02/05/08, Trilha) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Build e tooling/01 - Por que build tools existem.md"
git commit -m "feat(java): galho 15 nota 01 — por que build tools existem"
```

### Task 2: Nota 02 — Maven, POM, coordenadas e lifecycle

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Build e tooling/02 - Maven — POM, coordenadas e lifecycle.md`

- [ ] **Step 1 (WebFetch):** `maven.apache.org/guides/introduction/introduction-to-the-pom.html` + `.../introduction-to-the-lifecycle.html` + `maven.apache.org/download.cgi` — confirmar phases, GAV e **Maven 3.9.x atual / Maven 4 RC**.
- [ ] **Step 2 (escrever):** fase `iniciado`. POM (`pom.xml`) declarativo; **coordenadas GAV** (`groupId:artifactId:version`, packaging, classifier); repositório local (`~/.m2`) e remotos (analogia "cache de bibliotecas"); **lifecycle e phases** (`validate`→`compile`→`test`→`package`→`verify`→`install`→`deploy`), a ligação phase→plugin goal. Citar **Maven 3.9.x estável; Maven 4 ainda RC** (features vindas: consumer POM, BOM nativo). ` ```xml ` (POM mínimo) + ` ```bash ` (`mvn package`). Armadilhas (≥2): confundir phase com goal; achar que `package` roda `install`/`deploy`. "Em entrevista" + "Veja também" (notas 03/04/08/10) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Build e tooling/02 - Maven — POM, coordenadas e lifecycle.md"
git commit -m "feat(java): galho 15 nota 02 — Maven (POM, coordenadas e lifecycle)"
```

### Task 3: Nota 03 — Maven, dependências, scopes e exclusions

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Build e tooling/03 - Maven — dependências, scopes e exclusions.md`

- [ ] **Step 1 (WebFetch):** `maven.apache.org/guides/introduction/introduction-to-dependency-mechanism.html` — confirmar scopes (`compile`/`provided`/`runtime`/`test`/`system`/`import`) e propagação transitiva.
- [ ] **Step 2 (escrever):** fase `iniciado`. Declarar dependências; **scopes** e como cada um propaga na transitividade; `<exclusions>` pra cortar transitiva indesejada; `<optional>`. ` ```xml `. Armadilhas (≥2): `provided` esperando estar no runtime; não excluir transitiva conflitante (aponta nota 10). "Em entrevista" + "Veja também" (notas 02/10/11) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Build e tooling/03 - Maven — dependências, scopes e exclusions.md"
git commit -m "feat(java): galho 15 nota 03 — Maven (dependências, scopes e exclusions)"
```

### Task 4: Nota 04 — Maven, plugins, profiles e o wrapper

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Build e tooling/04 - Maven — plugins, profiles e o wrapper.md`

- [ ] **Step 1 (WebFetch):** `maven.apache.org/plugins/` + `maven.apache.org/guides/introduction/introduction-to-profiles.html` + `maven.apache.org/tools/wrapper/` — confirmar plugins essenciais e que o **wrapper NÃO vem por padrão**.
- [ ] **Step 2 (escrever):** fase `iniciado`. Plugins como a unidade de trabalho (o lifecycle só orquestra goals); essenciais (compiler, surefire, jar, shade — aponta nota 15); **profiles** (ativação por env/property/OS) e o risco de abusar (build não-reprodutível, aponta nota 17); o **Maven Wrapper** (`mvnw`/`mvnw.cmd`, gerado via `wrapper:wrapper`) pra fixar a versão. ` ```xml ` + ` ```bash `. Armadilhas (≥2): profiles divergentes quebrando reprodutibilidade; commitar sem wrapper (build depende do Maven da máquina). "Em entrevista" + "Veja também" (notas 02/07/17) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Build e tooling/04 - Maven — plugins, profiles e o wrapper.md"
git commit -m "feat(java): galho 15 nota 04 — Maven (plugins, profiles e o wrapper)"
```

### Task 5: Nota 05 — Gradle, build script, tasks e configurations

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Build e tooling/05 - Gradle — build script, tasks e configurations.md`

- [ ] **Step 1 (WebFetch):** `docs.gradle.org/current/userguide/kotlin_dsl.html` + `.../more_about_tasks.html` + `.../declaring_dependencies.html` + `gradle.org/releases/` — confirmar **Kotlin DSL default desde 8.0**, tasks/DAG, configurations e **Gradle 9.x atual**.
- [ ] **Step 2 (escrever):** fase `iniciado`. `build.gradle` (Groovy) vs `build.gradle.kts` (**Kotlin DSL = default recomendado desde Gradle 8.0**; Groovy não deprecado); **tasks** e o **task graph** (DAG, `dependsOn`); **configurations** como buckets de dependência (`implementation`/`api`/`compileOnly`/`runtimeOnly`/`testImplementation` — aponta nota 06); `plugins {}`; `settings.gradle(.kts)`. Citar **Gradle 9.x (9.0 exige Java 17+)**. ` ```kotlin ` (+ ` ```groovy ` no contraste). Armadilhas (≥2): pensar em Gradle como "Maven em código"; task sem inputs/outputs declarados (quebra incremental — aponta nota 07). "Em entrevista" + "Veja também" (notas 06/07/08) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Build e tooling/05 - Gradle — build script, tasks e configurations.md"
git commit -m "feat(java): galho 15 nota 05 — Gradle (build script, tasks e configurations)"
```

### Task 6: Nota 06 — Gradle, dependências, Version Catalogs e o wrapper

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Build e tooling/06 - Gradle — dependências, Version Catalogs e o wrapper.md`

- [ ] **Step 1 (WebFetch):** `docs.gradle.org/current/userguide/java_library_plugin.html` (api vs implementation) + `.../platforms.html` (version catalogs) + `.../gradle_wrapper.html` — confirmar Version Catalogs estáveis e `libs.versions.toml`.
- [ ] **Step 2 (escrever):** fase `iniciado`. Declarar deps por configuration; **`implementation` vs `api`** (encapsulamento do classpath de compilação — o ganho-chave do Gradle); **Version Catalogs** (`gradle/libs.versions.toml`, accessors type-safe `libs.xxx`); o **Gradle Wrapper** (`gradlew`, sempre presente, fixa a versão). ` ```kotlin ` + ` ```toml `. Armadilhas (≥2): tudo `api` (vaza classpath transitivo); hardcode de versão espalhado em vez do catalog. "Em entrevista" + "Veja também" (notas 05/07/11) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Build e tooling/06 - Gradle — dependências, Version Catalogs e o wrapper.md"
git commit -m "feat(java): galho 15 nota 06 — Gradle (dependências, Version Catalogs e o wrapper)"
```

### Task 7: Nota 07 — Gradle, performance, build cache e daemon

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Build e tooling/07 - Gradle — performance, build cache e daemon.md`

- [ ] **Step 1 (WebFetch):** `docs.gradle.org/current/userguide/incremental_build.html` + `.../build_cache.html` + `.../configuration_cache.html` — confirmar **configuration cache = preferred mode desde 9.0, ainda opt-in**.
- [ ] **Step 2 (escrever):** fase `iniciado`. O argumento de venda do Gradle: **incremental build** (task inputs/outputs, up-to-date checking), **build cache** (local e remoto — reusar outputs entre máquinas/CI), **configuration cache** ("preferred mode" 9.0, opt-in), o **daemon** (JVM quente — analogia). Por que Maven não tem equivalente nativo. ` ```bash ` + ` ```kotlin `. Armadilhas (≥2): task não-cacheável por output não-declarado; desligar o daemon em dev (lentidão). "Em entrevista" + "Veja também" (notas 05/06/08) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Build e tooling/07 - Gradle — performance, build cache e daemon.md"
git commit -m "feat(java): galho 15 nota 07 — Gradle (performance, build cache e daemon)"
```

### Task 8: Nota 08 — Maven vs Gradle, trade-offs honestos *(opus)*

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Build e tooling/08 - Maven vs Gradle — trade-offs honestos.md`

- [ ] **Step 1 (WebFetch):** `maven.apache.org/` + `docs.gradle.org/current/userguide/migrating_from_maven.html` — confirmar o posicionamento de cada um (sem hype).
- [ ] **Step 2 (escrever):** fase `iniciado`. O framework de decisão com os dois na mão: **declarativo/convenção** (Maven: previsível, onboarding rápido, IDE/CI universal, XML verboso porém estável) vs **imperativo/flexível** (Gradle: performance incremental, builds heterogêneos/custom logic, DSL, curva maior). Tabela "quando Maven" / "quando Gradle". **Sem dogma** — bytecode idêntico, ambos resolvem o mesmo problema. ` ```text ` (tabela). Armadilhas (≥2): escolher por hype/CV; migrar Maven→Gradle sem ganho real. "Em entrevista" (3+ sentenças com trade-off) + "Veja também" (notas 02/05/20) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Build e tooling/08 - Maven vs Gradle — trade-offs honestos.md"
git commit -m "feat(java): galho 15 nota 08 — Maven vs Gradle (trade-offs honestos)"
```

### Task 9: Nota 09 — Distribuições do JDK e o ecossistema *(opus, version-heavy)*

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Build e tooling/09 - Distribuições do JDK e o ecossistema.md`

- [ ] **Step 1 (WebFetch):** `oracle.com/java/technologies/java-se-support-roadmap.html` + `.../javase/jdk-faqs.html` + `adoptium.net/` + `sdkman.io/` — confirmar **LTS 17/21/25 (cadência 2 anos, próxima 29/2027)**, non-LTS 24/26, **NFTC** e licenças das distros.
- [ ] **Step 2 (escrever):** fase `iniciado`. **OpenJDK = projeto/código; distribuição = binário com selo de suporte/licença** (o bytecode é o mesmo). Oracle JDK (**NFTC** v21+ — a confusão pós-2019/licença comercial do Java 11, corrigida em 2021), Eclipse **Temurin**/Adoptium, Amazon **Corretto**, Azul **Zulu**, BellSoft **Liberica**, Microsoft Build (GPLv2+CPE), **GraalVM** (GFTC). Calendário (release 6 meses, **LTS a cada 2 anos**: 17/21/**25**; próxima 29/2027; non-LTS 24/26). **SDKMAN** pra instalar/trocar versões locais. ` ```bash ` (`sdk install java ...`) + ` ```text ` (tabela de distros×licença). Armadilhas (≥2): achar que precisa pagar a Oracle pra usar Java; usar non-LTS em produção sem entender o suporte de 6 meses. "Em entrevista" + "Veja também" (G3 A JVM, notas 13/08) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Build e tooling/09 - Distribuições do JDK e o ecossistema.md"
git commit -m "feat(java): galho 15 nota 09 — distribuições do JDK e o ecossistema"
```

### Task 10: Review da fase Iniciado (01-09)

- [ ] **Step 1:** dispatch de subagente revisor (spec compliance + qualidade) lendo as 9 notas. Checa: frontmatter+`fase`; estrutura H2; **zero fabricação** (grep `MedEspecialista|josenaldo|minha experiência|meu build|incidente`); **zero estatística inventada** (grep `%`); **zero re-explicação de fronteira** (módulos/jpackage/auto-config/pirâmide devem LINKAR G3/G6/G8/G13); zero wikilink pra galho 16/17/18; versões cravadas corretas (Maven 4 = RC, não GA; Kotlin DSL default 8.0; LTS 25); "Em entrevista" 3+ sentenças + 6+ termos; tese honesta presente (01/08/09).
- [ ] **Step 2:** fix loop (implementador corrige) até aprovado. Se corrige, commit `fix(java): galho 15 — ajustes da fase Iniciado`.

---

## Fase Adepto (notas 10-15)

### Task 11: Nota 10 — Resolução de dependências e conflitos de versão *(opus)*

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Build e tooling/10 - Resolução de dependências e conflitos de versão.md`

- [ ] **Step 1 (WebFetch):** `maven.apache.org/guides/introduction/introduction-to-dependency-mechanism.html` (dependency mediation/nearest-wins) + `docs.gradle.org/current/userguide/dependency_resolution.html` (resolution strategy) — confirmar os dois algoritmos.
- [ ] **Step 2 (escrever):** fase `adepto`. Resolução **transitiva**; o **conflito de versão**; **Maven: nearest-wins** (a mais próxima na árvore vence — e o efeito-surpresa da ordem de declaração; analogia "parente mais próximo ganha"); **Gradle: highest-version-wins** + resolution strategy (`failOnVersionConflict`, `force`, constraints). Ler o **dependency tree** (`mvn dependency:tree` / `gradle dependencies`); diagnosticar `NoSuchMethodError`/`NoClassDefFoundError`. ` ```bash ` (dependency tree) + ` ```text ` (árvore com conflito) + ` ```kotlin `/` ```xml ` (resolver). Armadilhas (≥3): confiar na resolução implícita; `force` sem entender a causa; assumir que Maven e Gradle resolvem igual. "Em entrevista" + "Veja também" (notas 03/06/11) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Build e tooling/10 - Resolução de dependências e conflitos de versão.md"
git commit -m "feat(java): galho 15 nota 10 — resolução de dependências e conflitos de versão"
```

### Task 12: Nota 11 — BOM e dependency management

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Build e tooling/11 - BOM e dependency management.md`

- [ ] **Step 1 (WebFetch):** `maven.apache.org/guides/introduction/introduction-to-dependency-mechanism.html` (dependencyManagement/import) + `docs.gradle.org/current/userguide/platforms.html` (platform/BOM) — confirmar BOM `import` scope e `platform()`.
- [ ] **Step 2 (escrever):** fase `adepto`. `dependencyManagement` (declarar versão sem declarar a dep); **BOM** (Bill of Materials) como POM de `import` scope (analogia "lista de preços com versões combinadas"); o **`spring-boot-dependencies`/`spring-boot-starter-parent`** como BOM concreto que o leitor já usa (**fronteira G8 — linka, não re-explica starters** → `Spring Core e Boot/15 - Auto-configuration e starters`); Version Catalogs + `platform()` no Gradle. ` ```xml ` (import BOM) + ` ```kotlin ` (`platform()`). Armadilhas (≥3): declarar versão em cada módulo (drift); ignorar o BOM e divergir versões; sobrescrever uma versão gerenciada por engano. "Em entrevista" + "Veja também" (notas 03/10/12, G8 starters) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Build e tooling/11 - BOM e dependency management.md"
git commit -m "feat(java): galho 15 nota 11 — BOM e dependency management"
```

### Task 13: Nota 12 — Projetos multi-módulo

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Build e tooling/12 - Projetos multi-módulo.md`

- [ ] **Step 1 (WebFetch):** `maven.apache.org/guides/mini/guide-multiple-modules.html` + `docs.gradle.org/current/userguide/multi_project_builds.html` — confirmar reactor (parent/modules) e `include`/convention plugins.
- [ ] **Step 2 (escrever):** fase `adepto`. **Reactor do Maven** (parent POM `<packaging>pom</packaging>` + `<modules>`, herança vs agregação, build order topológico) vs **multi-project do Gradle** (`settings.gradle` `include`, convention plugins, project dependencies). Quando dividir em módulos (e quando o **monólito modular** basta — fronteira: topologia de repos de microservices é G16 "(planejado)"). ` ```xml ` + ` ```text ` (árvore de módulos) + ` ```kotlin `. Armadilhas (≥3): módulos demais (overhead); dependência circular entre módulos; confundir multi-módulo com multi-repo de microservices. "Em entrevista" + "Veja também" (notas 02/05/11) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Build e tooling/12 - Projetos multi-módulo.md"
git commit -m "feat(java): galho 15 nota 12 — projetos multi-módulo"
```

### Task 14: Nota 13 — Toolchains, buildar com um JDK, mirar outro

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Build e tooling/13 - Toolchains — buildar com um JDK, mirar outro.md`

- [ ] **Step 1 (WebFetch):** `maven.apache.org/guides/mini/guide-using-toolchains.html` + `docs.gradle.org/current/userguide/toolchains.html` — confirmar toolchains Maven (`toolchains.xml`) e Gradle (auto-provisioning).
- [ ] **Step 2 (escrever):** fase `adepto`. O problema: a JVM que roda o build ≠ o JDK-alvo do bytecode. **Maven toolchains** (`maven-toolchains-plugin`, `~/.m2/toolchains.xml`) + o `release` flag do compiler; **Gradle toolchains** (`java { toolchain { languageVersion = ... } }`, auto-download). **Liga G3** (a JVM/bytecode versionado → `JVM/01`/`JVM/08`). ` ```xml ` (toolchains.xml) + ` ```kotlin `. Armadilhas (≥3): buildar com JDK errado sem notar; usar `source/target` em vez de `release` (vaza API nova); assumir que o toolchain baixa qualquer JDK. "Em entrevista" + "Veja também" (nota 09, G3 A JVM) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Build e tooling/13 - Toolchains — buildar com um JDK, mirar outro.md"
git commit -m "feat(java): galho 15 nota 13 — toolchains (buildar com um JDK, mirar outro)"
```

### Task 15: Nota 14 — Annotation processing, Lombok e MapStruct

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Build e tooling/14 - Annotation processing — Lombok e MapStruct.md`

- [ ] **Step 1 (WebFetch):** `projectlombok.org/` (features/changelog) + `mapstruct.org/` (docs + Lombok FAQ) — confirmar **Lombok 1.18.46 (JDK 21/25/26)**, **MapStruct 1.6.3**, e **`lombok-mapstruct-binding`**.
- [ ] **Step 2 (escrever):** fase `adepto`. O que é annotation processing (APT, `javax.annotation.processing`, geração em compile-time); **Lombok** (manipula AST, não é APT padrão; `lombok.config`; JDK 21/25-ready); **MapStruct** (mapper gerado, `componentModel = "spring"`); **o atrito Lombok+MapStruct** → `lombok-mapstruct-binding` + a **ordem de processors** e `-parameters`. **Recebe a poda do Spring Boot.md** (o tratamento canônico de Lombok/MapStruct vive aqui). ` ```xml ` (compiler plugin + annotationProcessorPaths) + ` ```java ` (mapper) + ` ```properties ` (lombok.config). Armadilhas (≥3): Lombok+MapStruct sem o binding (mapper vazio/nulls); `-parameters` faltando; Lombok `@Data` em entidade JPA (aponta a armadilha que fica no contexto Spring/G8/G10). "Em entrevista" + "Veja também" (G8 Spring Boot.md, notas 02/05) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Build e tooling/14 - Annotation processing — Lombok e MapStruct.md"
git commit -m "feat(java): galho 15 nota 14 — annotation processing (Lombok e MapStruct)"
```

### Task 16: Nota 15 — Empacotamento, fat jar, thin jar e repackage

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Build e tooling/15 - Empacotamento — fat jar, thin jar e repackage.md`

- [ ] **Step 1 (WebFetch):** `maven.apache.org/plugins/maven-shade-plugin/` + `docs.gradle.org/current/userguide/application_plugin.html` + `docs.spring.io` (spring-boot maven plugin / repackage / layered) — confirmar Shade/Shadow e o executable jar do Boot.
- [ ] **Step 2 (escrever):** fase `adepto`. `jar` simples (sem deps); **fat/uber jar** (Maven Shade / Gradle Shadow — tudo num jar; o problema de **resource merging/relocation**); **thin jar**; o **`spring-boot:repackage`** (executable jar com nested jars + `JarLauncher`) e o **layered jar** (camadas pra cache de imagem — **fronteira G8/G17**). **`jlink`/`jpackage` são fronteira (G3/G6) — LINKA, não re-explica** (→ `JVM/08`, `JavaFX/13`). **Recebe a poda do layered jar** do `Spring Boot.md`/`Spring Core e Boot/16`. ` ```xml ` (shade) + ` ```text ` (estrutura do jar). Armadilhas (≥3): fat jar com resource merge quebrado (META-INF/services); relocation esquecida (classes duplicadas); layered jar sem necessidade. "Em entrevista" + "Veja também" (G8 SpringApplication, G3 JPMS/jlink, G6 jpackage, nota 04) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Build e tooling/15 - Empacotamento — fat jar, thin jar e repackage.md"
git commit -m "feat(java): galho 15 nota 15 — empacotamento (fat jar, thin jar e repackage)"
```

### Task 17: Review da fase Adepto (10-15)

- [ ] **Step 1:** dispatch de subagente revisor lendo as 6 notas. Checa: frontmatter+`fase`; estrutura H2 (≥3 H3 em Como funciona; ≥3 armadilhas); **fronteira respeitada** (nota 13 LINKA G3; nota 15 LINKA G3/G6 jpackage e G8 repackage — NÃO re-explica; nota 11 LINKA G8 starters); versões corretas (Lombok+binding, MapStruct 1.6.3); zero fabricação/estatística; zero wikilink galho 16/17/18; "Em entrevista" completo; code/config válido (XML/DSL bem-formado).
- [ ] **Step 2:** fix loop até aprovado. Se corrige, commit `fix(java): galho 15 — ajustes da fase Adepto`.

---

## Fase Magus (notas 16-20)

### Task 18: Nota 16 — Quality gates no build

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Build e tooling/16 - Quality gates no build.md`

- [ ] **Step 1 (WebFetch):** `jacoco.org/jacoco/trunk/doc/maven.html` + `checkstyle.org/` + `spotbugs.github.io/` + `pmd.github.io/` — confirmar os goals/tasks que falham o build no threshold.
- [ ] **Step 2 (escrever):** fase `magus`. Plugar a ferramenta no lifecycle e **falhar o build** no threshold: **JaCoCo** (`check` goal com `minimum`), **Checkstyle** (estilo), **PMD** e **SpotBugs** (análise estática). **Ângulo de build, NÃO teoria** — Surefire/Failsafe (runners), JaCoCo como métrica e PIT (mutation) são **fronteira G13 — LINKA** (→ `Testes/17`, `Testes/01`). Quando falhar o build vs só reportar. ` ```xml ` + ` ```kotlin `. Armadilhas (≥3): threshold de cobertura como teatro (cobre getters); gate que ninguém olha; SpotBugs/PMD com ruído não-triado. "Em entrevista" + "Veja também" (G13 Mutation testing/pirâmide, nota 17) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Build e tooling/16 - Quality gates no build.md"
git commit -m "feat(java): galho 15 nota 16 — quality gates no build"
```

### Task 19: Nota 17 — Reprodutibilidade e reproducible builds

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Build e tooling/17 - Reprodutibilidade e reproducible builds.md`

- [ ] **Step 1 (WebFetch):** `maven.apache.org/guides/mini/guide-reproducible-builds.html` + `maven.apache.org/plugins/maven-artifact-plugin/` — confirmar `project.build.outputTimestamp`, **default no Maven 4**, e `check-buildplan`/`compare`.
- [ ] **Step 2 (escrever):** fase `magus`. Build determinístico: mesma entrada → bit-a-bit o mesmo artefato. **`project.build.outputTimestamp`** (timestamps normalizados, ordem estável); **default ativo a partir do Maven 4**; validação (`maven-artifact-plugin` `check-buildplan`/`compare`); pin de versões (sem `LATEST`/ranges abertos — aponta nota 10). Por que importa (verificabilidade, cache, auditoria de supply chain → nota 18). ` ```xml ` + ` ```bash `. Armadilhas (≥3): timestamps/ordem não-determinística; `RANGE`/`LATEST` de versão; assumir reprodutível sem validar. "Em entrevista" + "Veja também" (notas 10/18, nota 04 profiles) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Build e tooling/17 - Reprodutibilidade e reproducible builds.md"
git commit -m "feat(java): galho 15 nota 17 — reprodutibilidade e reproducible builds"
```

### Task 20: Nota 18 — Supply chain e SBOM *(opus)*

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Build e tooling/18 - Supply chain e SBOM.md`

- [ ] **Step 1 (WebFetch):** `cyclonedx.org/specification/overview/` + `slsa.dev/` + `owasp.org/www-project-dependency-check/` — confirmar **CycloneDX 1.6 (Ecma)**, os plugins Maven/Gradle, e SLSA L1-L3.
- [ ] **Step 2 (escrever):** fase `magus`. O pós-Log4Shell: saber **o que** você embarca. **SBOM** (Software Bill of Materials); **CycloneDX** (padrão Ecma 1.6, `cyclonedx-maven-plugin`/`cyclonedx-gradle-plugin`) vs SPDX; **SLSA** (níveis de integridade de build), **dependency scanning/SCA** (OWASP Dependency-Check); proveniência/attestation. Por que CVE scanning sozinho não cobre typosquatting/backdoor. ` ```xml ` (cyclonedx plugin) + ` ```bash `. Armadilhas (≥3): SBOM gerado e nunca consumido; achar que CVE scan cobre typosquatting; confundir SBOM (inventário) com reprodutibilidade (determinismo — nota 17). "Em entrevista" + "Veja também" (notas 17/19, nota 10 resolução) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Build e tooling/18 - Supply chain e SBOM.md"
git commit -m "feat(java): galho 15 nota 18 — supply chain e SBOM"
```

### Task 21: Nota 19 — Publicação de artefatos

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Build e tooling/19 - Publicação de artefatos.md`

- [ ] **Step 1 (WebFetch):** `central.sonatype.org/publish/` + `docs.gradle.org/current/userguide/publishing_maven.html` — confirmar **OSSRH descontinuado (30/06/2025) → Central Portal** e `central-publishing-maven-plugin`.
- [ ] **Step 2 (escrever):** fase `magus`. Coordenadas + repositório; publicar **interno** (Nexus/Artifactory) vs **público** (**Maven Central**); o processo atual: **OSSRH morreu (30/06/2025), Central Portal é o caminho** (`central-publishing-maven-plugin`); requisitos do Central (GPG signing, sources/javadoc jars, POM metadata completa); `maven-publish`/`signing` no Gradle; **SNAPSHOT vs release**. ` ```xml ` + ` ```kotlin ` + ` ```bash `. Armadilhas (≥3): publicar SNAPSHOT como release; metadata incompleta rejeitada pelo Central; usar o `maven-deploy-plugin` legado contra OSSRH (não funciona mais). "Em entrevista" + "Veja também" (notas 02/11/18) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Build e tooling/19 - Publicação de artefatos.md"
git commit -m "feat(java): galho 15 nota 19 — publicação de artefatos"
```

### Task 22: Nota 20 — Capstone, o mesmo projeto em Maven e Gradle *(opus, comparativo)*

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Build e tooling/20 - Capstone — o mesmo projeto em Maven e Gradle.md`

- [ ] **Step 1 (WebFetch):** `maven.apache.org/` + `docs.gradle.org/current/userguide/userguide.html` — confirmar a sintaxe dos snippets do projeto comparativo (POM multi-módulo vs settings/build.gradle.kts + libs.versions.toml).
- [ ] **Step 2 (escrever):** fase `magus`. **O mesmo projeto multi-módulo construído nos dois build tools, lado a lado** (coluna Maven vs coluna Gradle): árvore de arquivos (`pom.xml` vs `build.gradle.kts` + `libs.versions.toml`), declarar deps + BOM, plugar JaCoCo/Checkstyle, gerar SBOM, empacotar, publicar. **Tabela de decisão** (Maven quando…, Gradle quando…; qual distribuição de JDK; quando BOM; quando multi-módulo). **Cheatsheet nota→problema** ("conflito de versão? → nota 10"; "alinhar versões? → nota 11"; etc. — usar os **títulos EXATOS** das 20 notas). Munição de entrevista. ` ```xml ` + ` ```kotlin ` + ` ```toml ` + ` ```text ` (árvore + tabela). Armadilhas de raciocínio (≥3): "Gradle é sempre mais rápido"; "preciso de multi-módulo"; "tenho que pagar pelo JDK". "Em entrevista" + "Veja também" (todas as fases + MOC) + Referências.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Build e tooling/20 - Capstone — o mesmo projeto em Maven e Gradle.md"
git commit -m "feat(java): galho 15 nota 20 — capstone (o mesmo projeto em Maven e Gradle)"
```

### Task 23: Review da fase Magus (16-20)

- [ ] **Step 1:** dispatch de subagente revisor lendo as 5 notas. Checa: frontmatter+`fase`; estrutura; **nota 16 LINKA G13** (não re-explica teoria de teste); **nota 18 ≠ nota 17** (inventário vs determinismo); versões (CycloneDX 1.6, Central Portal, OSSRH morto); **capstone usa títulos EXATOS das 20 notas** (sem inventar — lição G12); zero fabricação/estatística; zero wikilink galho 16/17/18; tabela de decisão sem dogma.
- [ ] **Step 2:** fix loop até aprovado. Se corrige, commit `fix(java): galho 15 — ajustes da fase Magus`.

---

## Task 24: MOC do galho (`index.md`)

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Build e tooling/index.md`

- [ ] **Step 1 (escrever):** `type: moc`, `status: growing`, `publish: true`, `created`/`updated: 2026-06-11`, `title: "Build, tooling e ecossistema"`, tags `java`/`build`/`moc`, aliases `["Build, tooling e ecossistema", "Build e tooling", "Build Tools", "Maven e Gradle", "Galho 15 - Build"]`. Conteúdo conforme spec §3.2:
  - `> [!abstract] TL;DR` (galho cobre construir/versionar/empacotar/publicar um projeto Java; tese: build = grafo de deps + reprodutibilidade; Maven vs Gradle = convenção vs flexibilidade; **20 notas em 3 fases**)
  - "Sobre este galho" + audiência + nota de galho NOVO/PESQUISA com poda reversa mínima + **fronteira-assinatura quádrupla** (G3/G6/G8/G13)
  - 3 H2 (`## Iniciado` / `## Adepto` / `## Magus`) com wikilinks pras 20 notas (1 linha descritiva cada — usar títulos EXATOS dos arquivos)
  - **5 rotas alternativas** (Completa 01→20; Entrevista internacional 01→02→05→08→09→10→11→18→20; Maven na prática 02→03→04→10→11→12→15→19; Gradle na prática 05→06→07→10→11→12; Build production-grade 09→16→17→18→19)
  - "Veja também" (Trilha central, G3 JVM/JPMS, G6 jpackage, G8 starters/repackage, G13 testes/JaCoCo/PIT, Dicionário; Galhos 16/17/18 = texto "(planejado)" SEM wikilink)
  - Dataview "Todas as notas" (TABLE fase/status; **inline code nunca começa com `=`** — [[feedback_dataview_inline_code]])
- [ ] **Step 2 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Build e tooling/index.md"
git commit -m "feat(java): galho 15 MOC — Build, tooling e ecossistema"
```

---

## Task 25: Expansão do Dicionário de Java

**Files:**
- Modify: `03-Dominios/Tecnologia/Java/Dicionário de Java.md`

- [ ] **Step 1 (conferir dups):** `grep -ni "^### " "03-Dominios/Tecnologia/Java/Dicionário de Java.md"` filtrando os candidatos a colisão (do Task 0 Step 6): `auto-configuration`, `starter`, `JaCoCo`, `Surefire`, `mutation testing`, `PIT`, `GraalVM`, `AOT`, `jpackage`, `JPMS`/`módulos`. Onde já existir, **linkar** (não duplicar).
- [ ] **Step 2 (inserir):** inserir ~32 verbetes em ordem alfabética (case-insensitive, sem acento, ignorando símbolos) nas seções `## A`…`## Z` existentes. Lista (spec §3.3): `artifact (artefato Maven)`, `BOM (Bill of Materials)`, `build cache (Gradle)`, `Central Portal`, `Checkstyle`, `configuration (Gradle)`, `configuration cache (Gradle)`, `coordenadas GAV`, `CycloneDX`, `dependencyManagement`, `dependency scope (Maven)`, `dependency tree`, `fat jar / uber jar`, `GraalVM (distribuição)`, `Gradle`, `incremental build`, `JDK distribution`, `jlink (no build)`, `Kotlin DSL (Gradle)`, `lifecycle (Maven)`, `Lombok`, `MapStruct`, `Maven`, `Maven Central`, `multi-module (reactor)`, `nearest-wins (mediation)`, `NFTC (No-Fee Terms and Conditions)`, `OpenJDK`, `phase (Maven)`, `POM`, `reproducible build`, `SBOM`, `SDKMAN`, `SLSA`, `Temurin (Adoptium)`, `thin jar`, `toolchain (build)`, `Version Catalog`, `wrapper (mvnw/gradlew)`. Cada verbete: definição curta (1-3 linhas) PT-BR + `Veja também:` apontando pra nota canônica do galho. **Manter `updated: 2026-06-11`; NÃO recriar/reordenar verbetes existentes.**
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Dicionário de Java.md"
git commit -m "feat(java): expande Dicionário de Java com verbetes do galho 15 (Build e tooling)"
```

---

## Task 26: Ativação do MOC central

**Files:**
- Modify: `03-Dominios/Tecnologia/Java/index.md`

- [ ] **Step 1:** Ler `03-Dominios/Tecnologia/Java/index.md` e localizar a linha do Galho 15 (Task 0 confirmou ~linha 48: `15. Build, tooling e ecossistema *(planejado)* — ...`).
- [ ] **Step 2:** Trocar por wikilink ativo (spec §3.4):
```markdown
15. [[03-Dominios/Tecnologia/Java/Build e tooling/index|Build, tooling e ecossistema]] — Maven e Gradle (modelo, lifecycle/tasks, performance), gestão de dependências (resolução transitiva, conflitos, BOM), multi-módulo, distribuições do JDK e licenciamento, annotation processing (Lombok/MapStruct), empacotamento, quality gates no build e cadeia de suprimentos (reproducible builds, SBOM, Maven Central)
```
Atualizar `updated: 2026-06-11`. **Não mexer no resto.** Galhos 16/17/18 permanecem `*(planejado)*`.
- [ ] **Step 3 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/index.md"
git commit -m "feat(java): ativa Galho 15 (Build e tooling) no MOC central"
```

---

## Task 27: Poda reversa em `Spring Boot.md` + cross-links

**Files:**
- Modify: `03-Dominios/Tecnologia/Java/Backend/Spring Boot.md`
- Modify: `03-Dominios/Tecnologia/Java/Spring Core e Boot/16 - SpringApplication e o embedded server.md`
- (opcional) Modify: notas-fronteira com "Veja também" existente (§3.6)

- [ ] **Step 1 (confirmar linhas):** rodar o grep do Task 0 Step 5 de novo (linhas podem ter mudado).
- [ ] **Step 2 (poda conservadora — `Spring Boot.md`):** conforme spec §3.5:
  - **Lombok** (~297-307): **manter o resumo curto da armadilha Lombok+JPA** (`@Data`/`equals`/`hashCode` — é relevante no contexto Spring/persistência); adicionar wikilink `[[03-Dominios/Tecnologia/Java/Build e tooling/14 - Annotation processing — Lombok e MapStruct|tratamento completo de Lombok no Galho 15]]`; remover só a explicação genérica de tooling que duplica a nota 14.
  - **MapStruct** (~297-305): reduzir a resumo + wikilink pra nota 14.
  - **`spring-boot-maven-plugin`/layered jar** (~313): o `repackage` como mecanismo Spring continua; trocar a referência "(planejado)" ao packaging por wikilink ativo `[[03-Dominios/Tecnologia/Java/Build e tooling/15 - Empacotamento — fat jar, thin jar e repackage|Empacotamento (Galho 15)]]`.
- [ ] **Step 3 (poda — `Spring Core e Boot/16`):** trocar o texto "coberto no Galho 15/17 (planejado)" por wikilink ativo pra **nota 15** (Galho 15); manter "(planejado)" só pro Galho 17 (containers/native).
- [ ] **Step 4 (cross-links opcionais, conservador):** só onde a nota-dona JÁ tem seção "Veja também" e o link agrega (§3.6): `JavaFX/13` → nota 15; `Spring Core e Boot/15` → nota 11; `Testes/17` → nota 16. **Não inflar notas fechadas; não forçar.**
- [ ] **Step 5 (commit):**
```bash
git add "03-Dominios/Tecnologia/Java/Backend/Spring Boot.md" "03-Dominios/Tecnologia/Java/Spring Core e Boot/16 - SpringApplication e o embedded server.md"
# + quaisquer notas-fronteira tocadas no Step 4 (git add nominal de cada)
git commit -m "refactor(java): poda reversa do galho 15 — Lombok/MapStruct/packaging viram wikilinks"
```

---

## Task 28: Verificação final (wikilinks + spec compliance)

- [ ] **Step 1 (verificar-wikilinks):** rodar a skill `verificar-wikilinks` na pasta `03-Dominios/Tecnologia/Java/Build e tooling/` + nos arquivos tocados (Dicionário, MOC central, Spring Boot.md, Spring Core e Boot/16). Corrigir quebrados. Atenção aos **títulos EXATOS** das notas-fronteira (em-dash `—`) e do Dicionário.
- [ ] **Step 2 (grep de sanidade):**
```bash
# zero wikilink pra galho inexistente
grep -rn "\[\[[^]]*\(Galho 1[678]\|Galho 18\|microservi\|Spring Cloud\|native image\|GraalVM native\)" "03-Dominios/Tecnologia/Java/Build e tooling/"
# zero fabricação
grep -rni "MedEspecialista\|josenaldo\|minha experiência\|meu build\|incidente de produção" "03-Dominios/Tecnologia/Java/Build e tooling/"
# zero percentual de adoção inventado
grep -rn "% \(dos\|das\|usa\|adota\)" "03-Dominios/Tecnologia/Java/Build e tooling/"
# 20 notas + index
ls "03-Dominios/Tecnologia/Java/Build e tooling/" | wc -l   # deve ser 21
```
- [ ] **Step 3 (review final):** dispatch de subagente revisor cross-galho — confere os 12 critérios de aceitação (spec §7): 20 notas 9/6/5, MOC com 5 rotas + dataview, Dicionário expandido (não recriado), MOC central ativado, poda conservadora (armadilha Lombok+JPA preservada), fronteira quádrupla respeitada, versões cravadas corretas, capstone com títulos exatos.
- [ ] **Step 4 (fix loop):** corrigir o que o review apontar; commit `fix(java): galho 15 — ajustes finais`.

---

## Task 29: Atualização da memória

**Files:**
- Modify: `/home/josenaldo/.claude/projects/-home-josenaldo-repos-personal-codex-technomanticus/memory/project_trilha_java.md`

- [ ] **Step 1:** Atualizar o registro `project_trilha_java`: Galho 15 (Build e tooling) **COMPLETO em main**; 20 notas (9/6/5) na pasta `Build e tooling/`; versões cravadas (Maven 3.9.16/Maven 4 RC, Gradle 9.5.1, Kotlin DSL default 8.0, config cache opt-in, Lombok 1.18.46+binding, MapStruct 1.6.3, LTS 17/21/25 cadência 2 anos, Oracle NFTC, CycloneDX 1.6, OSSRH morto→Central Portal, SDKMAN); poda reversa de Lombok/MapStruct/packaging no Spring Boot.md; fronteira quádrupla G3/G6/G8/G13; próximo sugerido: **Galho 16 (Microservices)** ou **17 (Cloud-native)**. Não duplicar — editar o arquivo existente.
- [ ] **Step 2:** (não commitar — a memória fica fora do repo do vault; o arquivo está no diretório de memória do Claude Code, não versionado no codex-technomanticus.)

---

## Resumo de tasks

| Task | Conteúdo | Modelo |
|------|----------|--------|
| 0 | Pré-flight (pasta, paths de fronteira, baselines, linhas de poda) | — |
| 1-9 | Notas 01-09 (Iniciado) | opus: 01/08/09; resto sonnet |
| 10 | Review Iniciado | sonnet |
| 11-16 | Notas 10-15 (Adepto) | opus: 10; resto sonnet |
| 17 | Review Adepto | sonnet |
| 18-22 | Notas 16-20 (Magus) | opus: 18/20; resto sonnet |
| 23 | Review Magus | sonnet |
| 24 | MOC do galho | sonnet |
| 25 | Expansão do Dicionário (~32 verbetes) | sonnet |
| 26 | Ativação do MOC central | sonnet |
| 27 | Poda reversa Spring Boot.md + cross-links | sonnet |
| 28 | Verificação final (wikilinks + compliance) | sonnet (review opus se necessário) |
| 29 | Atualização da memória | — |

**Total:** 20 notas + MOC + Dicionário + MOC central + poda + verificação. Opus em 01/08/09/10/18/20.
