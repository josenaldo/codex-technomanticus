---
title: "Gradle — dependências, Version Catalogs e o wrapper"
created: 2026-06-11
updated: 2026-06-11
type: concept
status: seedling
publish: true
fase: iniciado
tags:
  - java
  - build
  - iniciado
  - gradle
  - dependencias
aliases:
  - "Version Catalog"
  - "libs.versions.toml"
---

# Gradle — dependências, Version Catalogs e o wrapper

> [!abstract] TL;DR
> No Gradle, cada dependência é declarada numa **configuration**. A escolha mais importante é entre **`implementation`** e **`api`**: `implementation` mantém a dependência interna ao módulo e ela **não vaza** no classpath de compilação dos consumidores; `api` expõe a dependência transitivamente — use só quando o tipo aparece na API pública do seu módulo. Os **Version Catalogs** (`gradle/libs.versions.toml`) centralizam versões e geram accessors type-safe (`libs.xxx`). O **Gradle Wrapper** (`gradlew`/`gradlew.bat` + `gradle/wrapper/`) fixa a versão do Gradle e vem por padrão — diferente do Maven, onde o wrapper é opcional.

## O que é

Declarar uma dependência no Gradle é dizer **a quê** o módulo se liga e **em que escopo**. Esse escopo é a *configuration*: um balde nomeado onde você joga a dependência (`implementation`, `api`, `testImplementation`, `runtimeOnly`, etc.). A configuration escolhida decide se a dependência fica visível na compilação, em runtime, nos testes, e — crucialmente — se ela é repassada para quem consome o seu módulo.

Em cima disso, duas peças do ecossistema Gradle organizam o gerenciamento de dependências:

- **Version Catalog** — um arquivo TOML único (`gradle/libs.versions.toml`) que concentra as coordenadas e versões de todas as bibliotecas do projeto.
- **Gradle Wrapper** — scripts versionados no repositório que fixam qual versão do Gradle constrói o projeto.

## Por que importa

A separação `implementation`/`api` é o ganho de design que distingue o Gradle do Maven, que tem um único `compile` que sempre vaza transitivamente. Ao manter dependências internas fora do classpath de compilação dos consumidores, o Gradle reduz o tamanho do classpath, acelera a compilação e evita recompilações desnecessárias quando uma dependência interna muda.

O Version Catalog elimina o problema clássico de versões espalhadas e divergentes entre módulos: uma versão definida num lugar só, accessors com autocompletar na IDE e erro de digitação pego em tempo de build. E o Wrapper garante que todo mundo — sua máquina, o colega, o CI — roda exatamente a mesma versão do Gradle, tornando o build reprodutível sem instalação manual.

## Como funciona

### `implementation` vs `api`

Ambas colocam a dependência no classpath de compilação **do próprio módulo**. A diferença está no que acontece com os **consumidores** do módulo:

- **`implementation`** — a dependência é interna ao componente. Ela **não é exposta aos consumidores** e, portanto, **não vaza no classpath de compilação** deles. Use quando o tipo da dependência aparece só em corpos de método, membros privados ou classes internas.
- **`api`** — a dependência é exportada pela API da biblioteca e fica **transitivamente exposta aos consumidores**. Use quando um tipo da dependência aparece na superfície pública (ABI) do módulo: superclasses, parâmetros ou retornos de métodos públicos, campos públicos, tipos de anotação.

Regra prática: comece sempre com `implementation`. Só promova para `api` quando o compilador (ou o consumidor) reclamar de um tipo que vaza pela sua API pública. Tanto `api` quanto `implementation` exigem o plugin `java-library` (o plugin `java` puro só oferece `implementation`).

### Version Catalogs

Por convenção, o catálogo vive em `gradle/libs.versions.toml` e o Gradle o importa automaticamente. O TOML tem quatro seções:

- **`[versions]`** — identificadores de versão reutilizáveis (`spring = "6.2.0"`).
- **`[libraries]`** — apelidos mapeados para coordenadas GAV (group:artifact:version), podendo referenciar uma versão via `version.ref`.
- **`[bundles]`** — grupos de bibliotecas declaradas juntas com um único accessor.
- **`[plugins]`** — plugins com id e versão, usados via `alias(libs.plugins.xxx)`.

O Gradle gera **accessors type-safe** a partir dos apelidos: traços (`-`) viram pontos no accessor (`groovy-core` → `libs.groovy.core`), criando grupos aninhados. Bundles aparecem em `libs.bundles.xxx` e plugins em `libs.plugins.xxx`. Version Catalogs são um recurso **estável e recomendado** nas versões atuais do Gradle.

### O wrapper

O Gradle Wrapper é a forma recomendada de executar qualquer build. Ele é composto por quatro arquivos, todos versionados no repositório:

- **`gradlew`** — script shell para Unix/macOS/Linux.
- **`gradlew.bat`** — script batch para Windows.
- **`gradle/wrapper/gradle-wrapper.jar`** — código que baixa a distribuição do Gradle.
- **`gradle/wrapper/gradle-wrapper.properties`** — configura o wrapper; é onde a versão é fixada via `distributionUrl`.

Ao rodar `./gradlew build` em vez de `gradle build`, o wrapper baixa (se necessário) e usa exatamente a versão declarada no `distributionUrl`. Isso padroniza a versão do Gradle para builds confiáveis e reprodutíveis em IDEs e servidores de CI. Contraste com o Maven: lá o equivalente (Maven Wrapper, `mvnw`) **não vem por padrão** e precisa ser adicionado explicitamente — no Gradle, o wrapper é parte do esqueleto gerado por `gradle init`.

## Na prática

Catálogo completo em `gradle/libs.versions.toml`:

```toml
[versions]
spring-boot = "3.4.0"
jackson = "2.18.0"
junit = "5.11.0"

[libraries]
spring-boot-starter-web = { module = "org.springframework.boot:spring-boot-starter-web", version.ref = "spring-boot" }
jackson-databind = { module = "com.fasterxml.jackson.core:jackson-databind", version.ref = "jackson" }
commons-lang3 = { group = "org.apache.commons", name = "commons-lang3", version = "3.17.0" }
junit-jupiter = { module = "org.junit.jupiter:junit-jupiter", version.ref = "junit" }

[bundles]
jackson = ["jackson-databind"]

[plugins]
spring-boot = { id = "org.springframework.boot", version.ref = "spring-boot" }
```

Build script (`build.gradle.kts`) consumindo o catálogo:

```kotlin
plugins {
    `java-library`
    alias(libs.plugins.spring.boot)
}

dependencies {
    // vaza na API pública: aparece em assinaturas de métodos públicos
    api(libs.jackson.databind)

    // interno ao módulo: não vaza no classpath dos consumidores
    implementation(libs.spring.boot.starter.web)
    implementation(libs.commons.lang3)

    // bundle: várias libs num accessor só
    testImplementation(libs.junit.jupiter)
}
```

Rodando o build pelo wrapper:

```bash
./gradlew build
```

## Armadilhas

### (1) Marcar tudo como `api` e vazar o classpath transitivo

É tentador usar `api` para tudo "para garantir que funciona". O custo aparece depois: toda dependência `api` é repassada transitivamente ao classpath de compilação de quem consome o módulo. Isso incha o classpath dos consumidores, deixa a compilação mais lenta, força recompilações quando uma dependência puramente interna muda e acopla os consumidores a detalhes que não deviam enxergar. Mantenha `implementation` como padrão e reserve `api` para os tipos que realmente aparecem na sua API pública.

### (2) Hardcode de versão espalhado em vez do catalog

Declarar `implementation("com.fasterxml.jackson.core:jackson-databind:2.18.0")` em cada `build.gradle.kts` parece inofensivo no primeiro módulo. Em projetos multi-módulo, vira divergência: um módulo em `2.18.0`, outro em `2.16.0`, conflitos de resolução silenciosos e atualizações que exigem caçar a string em N arquivos. Centralize tudo no `libs.versions.toml`: uma versão num lugar só, accessor type-safe e erro de digitação pego no build.

## Em entrevista

### Frase pronta (inglês)

In Gradle, the most important dependency choice is between the `implementation` and `api` configurations. I default to `implementation` because it keeps the dependency internal to the module — it doesn't leak into the compile classpath of consumers, which keeps their classpaths small and avoids unnecessary recompilations. I only promote a dependency to `api` when one of its types actually appears in my module's public API, such as a public method parameter or return type. On top of that, I centralize all coordinates and versions in a Version Catalog (`gradle/libs.versions.toml`) so versions are defined once with type-safe accessors, and I always commit the Gradle Wrapper so every developer and the CI run the exact same Gradle version.

### Vocabulário

| Termo PT | Termo EN |
| --- | --- |
| escopo nomeado onde uma dependência é declarada (`implementation`, `api`, etc.) | configuration |
| conjunto de dependências visíveis na compilação; o que `implementation` impede de vazar aos consumidores | compile classpath |
| dependência herdada de outra dependência; `api` as expõe, `implementation` não | transitive dependency |
| superfície pública do módulo (assinaturas, tipos expostos) que decide se algo é `api` | ABI (Application Binary Interface) |
| `libs.versions.toml`, centraliza versões e gera accessors `libs.xxx` | Version Catalog |
| referência gerada (`libs.spring.boot.starter.web`) com autocompletar e checagem em build | type-safe accessor |
| `gradlew`/`gradlew.bat` que fixa e provisiona a versão do Gradle | Gradle Wrapper |

## Veja também

- [[03-Dominios/Tecnologia/Java/Build e tooling/05 - Gradle — build script, tasks e configurations|Gradle — o modelo]]
- [[03-Dominios/Tecnologia/Java/Build e tooling/07 - Gradle — performance, build cache e daemon|Gradle — performance]]
- [[03-Dominios/Tecnologia/Java/Build e tooling/11 - BOM e dependency management|BOM e dependency management]]
- [[03-Dominios/Tecnologia/Java/Build e tooling/index|Build, tooling e ecossistema (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]

## Referências

- [Gradle Userguide — The Java Library Plugin (`api` vs `implementation`)](https://docs.gradle.org/current/userguide/java_library_plugin.html)
- [Gradle Userguide — Sharing dependency versions with version catalogs](https://docs.gradle.org/current/userguide/version_catalogs.html)
- [Gradle Userguide — The Gradle Wrapper](https://docs.gradle.org/current/userguide/gradle_wrapper.html)
