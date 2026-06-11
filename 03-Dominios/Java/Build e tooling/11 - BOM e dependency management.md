---
title: "BOM e dependency management"
created: 2026-06-11
updated: 2026-06-11
type: concept
status: seedling
publish: true
fase: adepto
tags:
  - java
  - build
  - adepto
  - dependencias
  - bom
aliases:
  - "BOM"
  - "Bill of Materials"
  - "dependencyManagement"
---

# BOM e dependency management

> [!abstract] TL;DR
> `dependencyManagement` (Maven) é onde você declara a **versão** de uma dependência sem necessariamente declarar a dependência em si. Módulos filhos passam a herdar essa versão sem repetir o `<version>`. Um **BOM** (Bill of Materials) é um POM que existe só pra carregar um bloco de `dependencyManagement`: você o importa via `<scope>import</scope>` e ganha de graça um conjunto de versões já combinadas e testadas juntas. Pense numa "lista de preços" com versões pré-acordadas. No Gradle o equivalente é `platform()` / `enforcedPlatform()`, que importa o mesmo BOM como restrições de versão.

## O que é

Quando um projeto cresce em módulos e dependências, a pergunta "qual versão de cada biblioteca?" vira um problema de coordenação. Declarar versões soltas em cada `pom.xml` ou `build.gradle` espalha decisões que precisam ser consistentes, e basta um módulo divergir pra você ter duas versões da mesma lib no mesmo build.

`dependencyManagement` é a resposta do Maven pra esse problema. É uma seção do POM onde você diz **qual versão usar** de um artefato — sem, necessariamente, adicionar esse artefato ao classpath. A inclusão de verdade continua acontecendo em `<dependencies>`; só que lá, no módulo que usa a lib, você omite o `<version>` e deixa o `dependencyManagement` resolver.

Um **BOM** (Bill of Materials) leva essa ideia um passo adiante: é um POM cujo único propósito é conter um `dependencyManagement` grande, descrevendo um conjunto coerente de artefatos e suas versões. Em vez de copiar dezenas de versões manualmente, você **importa** o BOM e herda o bloco inteiro de uma vez.

## Por que importa

- **Single source of truth de versões.** Uma decisão de versão fica num lugar só. Subir a versão de uma lib no parent ou no BOM propaga pra todos os consumidores sem editar cada módulo.
- **Combinações testadas juntas.** Um BOM publicado por um framework (Spring, JUnit, AWS SDK) não é uma lista aleatória: são versões que os mantenedores validaram em conjunto. Importar o BOM significa "use o conjunto que sabemos que funciona", evitando incompatibilidades entre componentes do mesmo ecossistema.
- **POMs filhos mais limpos.** Dependências sem `<version>` ficam mais legíveis e expressam intenção ("quero a lib X") sem ruído de versão.
- **Menos drift.** Sem gestão central, módulos divergem ao longo do tempo. O BOM e o `dependencyManagement` ancoram todo mundo no mesmo ponto.

## Como funciona

### dependencyManagement: declarar versão sem declarar a dependência

A seção `<dependencyManagement>` do Maven **centraliza informação de versão**. Quando um conjunto de projetos herda de um parent comum, dá pra colocar toda a informação da dependência no POM comum e deixar os filhos com referências simples — sem repetir versão.

A regra-chave: o que está em `dependencyManagement` **não** entra no classpath por si só. Ele só dita a versão (e outras configurações, como `scope` e `exclusions`) que será aplicada **se e quando** aquela dependência for de fato declarada em `<dependencies>` — no próprio POM ou num filho. É declaração de política de versão, não de uso.

No filho, você declara a dependência sem `<version>`; o Maven preenche a versão a partir do `dependencyManagement` herdado.

### BOM via import scope

O `import` é um escopo especial, suportado **apenas** em dependências do tipo `pom` dentro de `<dependencyManagement>`. Ele indica que aquela dependência deve ser **substituída pela lista efetiva de dependências da seção `<dependencyManagement>` do POM apontado**. Na prática: o bloco de versões do BOM é mesclado no seu próprio `dependencyManagement`.

Isso resolve uma limitação importante: um POM só pode ter **um** parent (herança única). Mas você pode **importar vários BOMs** via `scope=import`, combinando conjuntos de versões de ecossistemas diferentes sem precisar herdar de nenhum deles.

Regra de precedência: se uma versão é declarada tanto no POM que importa quanto no BOM importado, **a declaração do POM que importa vence**. É por isso que sobrescrever uma versão gerenciada é tecnicamente possível — e perigoso (ver Armadilhas).

### O equivalente Gradle: platform()

No Gradle, você importa um BOM (ou uma plataforma Gradle nativa) com a função `platform()`. Ela marca o componente com a categoria `platform` e, por padrão, aplica o comportamento de endossar as versões estritas definidas na plataforma. As entradas do BOM viram **constraints** (restrições): dependências declaradas sem versão recebem a versão da plataforma automaticamente.

Existe também `enforcedPlatform()`, uma variante mais agressiva que **força** as versões do BOM, sobrescrevendo o que aparecer no grafo de dependências. A documentação alerta que essa imposição é transitiva e afeta o grafo dos seus consumidores — então use com cuidado em bibliotecas publicadas. Resumindo: `platform()` recomenda versões (permite override), `enforcedPlatform()` impõe.

No Gradle, o catálogo de versões (Version Catalogs) cobre o lado de **aliases e centralização declarativa** de coordenadas/versões — veja [[03-Dominios/Java/Build e tooling/06 - Gradle — tasks, plugins e configuration cache|Version Catalogs (nota 06)]]. `platform()` e os catálogos são complementares: um importa conjuntos testados de terceiros, o outro centraliza as suas próprias coordenadas.

## Na prática

Maven — importar um BOM e declarar uma dependência sem versão:

```xml
<dependencyManagement>
  <dependencies>
    <dependency>
      <groupId>com.exemplo.plataforma</groupId>
      <artifactId>plataforma-bom</artifactId>
      <version>2.4.0</version>
      <type>pom</type>
      <scope>import</scope>
    </dependency>
  </dependencies>
</dependencyManagement>

<dependencies>
  <!-- versão omitida: vem do BOM importado acima -->
  <dependency>
    <groupId>com.exemplo.plataforma</groupId>
    <artifactId>plataforma-core</artifactId>
  </dependency>
</dependencies>
```

Gradle (Kotlin DSL) — importar o mesmo BOM como plataforma:

```kotlin
dependencies {
    // platform() importa o BOM como conjunto de constraints
    implementation(platform("com.exemplo.plataforma:plataforma-bom:2.4.0"))

    // sem versão: o platform() supre a partir do BOM
    implementation("com.exemplo.plataforma:plataforma-core")
}
```

### O caso concreto que você já usa: spring-boot-dependencies

Se você herda do `spring-boot-starter-parent` ou importa o `spring-boot-dependencies`, está usando um BOM concreto sem perceber. O `spring-boot-starter-parent` traz, via `dependencyManagement`, o BOM `spring-boot-dependencies`, que **alinha as versões** de centenas de bibliotecas que o Boot integra. É por isso que você adiciona um starter e não precisa cravar versão de Jackson, Tomcat embarcado ou Logback: o BOM já decidiu o conjunto testado junto.

Aqui é a fronteira com o Galho 8 — os *starters* e a *auto-configuration* são outro assunto (eles é que decidem **quais** dependências e beans entram). Esta nota só cobre o lado de **versões**: o `starter-parent` traz o BOM que alinha versões. Pra entender o que o starter realmente faz, veja [[03-Dominios/Java/Spring Core e Boot/15 - Auto-configuration e starters|starters (Galho 8)]].

## Armadilhas

### (1) Declarar versão em cada módulo → drift

Sem `dependencyManagement` ou BOM, cada módulo crava sua própria versão. Com o tempo, atualizações chegam em ritmos diferentes e o projeto acaba com dois ou mais módulos pedindo versões distintas da mesma lib. O resultado é *version drift*: builds inconsistentes, bugs que só aparecem em um módulo e atualizações que viram caça ao tesouro por todos os POMs. Centralize a versão num lugar só.

### (2) Ignorar o BOM e divergir versões do ecossistema

Quando um framework publica um BOM, ele garante que seus componentes foram testados naquela combinação. Adicionar manualmente as dependências do ecossistema com versões escolhidas a dedo — ignorando o BOM — convida incompatibilidades sutis entre peças que deveriam casar. Se existe um BOM oficial pro conjunto que você usa, importe-o em vez de versionar peça por peça.

### (3) Sobrescrever uma versão gerenciada do BOM por engano

Como a versão declarada no seu POM **vence** a do BOM importado, é fácil fixar uma versão localmente (às vezes só pra "resolver" um aviso) e, sem querer, quebrar a combinação testada que o BOM garantia. Aí um componente fica numa versão que nunca foi validada contra os outros do mesmo conjunto, e surgem incompatibilidades de runtime difíceis de rastrear. Override de versão gerenciada deve ser decisão consciente e documentada, não acidente.

## Em entrevista

### Frase pronta (inglês)

In Maven, `dependencyManagement` lets me declare versions in one place so child modules inherit them without repeating the `<version>` tag. A BOM is just a POM whose only job is to carry a `dependencyManagement` block, and I import it with `scope=import`, which merges its managed versions into mine — that's how I pull in a set of versions that were tested together, like Spring Boot's `spring-boot-dependencies`. In Gradle the equivalent is `implementation(platform("..."))`, which imports the same BOM as version constraints, with `enforcedPlatform()` as the stricter variant that overrides versions in the graph. The main thing I watch for is accidentally overriding a managed version, because the importing POM wins and you can silently break the tested combination.

### Vocabulário

| Termo PT | Termo EN |
| --- | --- |
| Lista de materiais / BOM | Bill of Materials (BOM) |
| Gerência de dependências | dependency management |
| Versão gerenciada | managed version |
| Escopo de importação | import scope |
| Restrição de versão | version constraint |
| Divergência de versões | version drift |
| Herança única (de parent) | single inheritance |
| Combinação testada junta | tested-together combination |

## Veja também

- [[03-Dominios/Java/Build e tooling/03 - Maven — dependências, scopes e exclusions|Maven — scopes]]
- [[03-Dominios/Java/Build e tooling/10 - Resolução de dependências e conflitos de versão|Resolução de conflitos]]
- [[03-Dominios/Java/Build e tooling/12 - Projetos multi-módulo|Projetos multi-módulo]]
- [[03-Dominios/Java/Spring Core e Boot/15 - Auto-configuration e starters|Starters e auto-configuration (Galho 8)]]
- [[03-Dominios/Java/Build e tooling/index|Build, tooling e ecossistema (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]

## Referências

- Maven — Introduction to the Dependency Mechanism (dependencyManagement, import scope, BOM): https://maven.apache.org/guides/introduction/introduction-to-dependency-mechanism.html
- Gradle — Sharing dependency versions between projects / Platforms (`platform()`, `enforcedPlatform()`, importing a Maven BOM): https://docs.gradle.org/current/userguide/platforms.html
