---
title: "Maven — dependências, scopes e exclusions"
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
  - dependencias
aliases:
  - "Maven — scopes"
---

# Maven — dependências, scopes e exclusions

> [!abstract] TL;DR
> Toda dependência no POM tem um **scope** que decide em quais classpaths ela aparece (compile, runtime, test) e se ela **propaga transitivamente** para quem depende do seu projeto. `compile` (default) vale em tudo e propaga; `provided` existe no compile mas o container/JDK fornece em runtime e não propaga; `runtime` entra só em runtime/test; `test` fica preso aos testes; `system` é o último recurso (evite); `import` só existe em `<dependencyManagement>` para puxar um BOM. Para cortar uma transitiva indesejada use `<exclusions>`; para não empurrar uma dependência sua aos consumidores use `<optional>true</optional>`.

## O que é

Uma **dependência** é uma biblioteca externa que seu projeto precisa, declarada por coordenadas (`groupId`, `artifactId`, `version`) dentro de `<dependencies>` no `pom.xml`. O Maven baixa cada dependência do repositório, monta os classpaths apropriados e resolve as **dependências transitivas** (as dependências das suas dependências) automaticamente.

O **scope** é o atributo que governa esse processo. Ele responde a duas perguntas: (1) em qual classpath a dependência fica disponível — compilação, execução, testes; e (2) se ela é repassada aos projetos que dependem do seu (propagação transitiva). Sem entender scope, é fácil empacotar bibliotecas que não deveriam ir para o artefato final, ou ter um `NoClassDefFoundError` em produção porque algo que estava no compile-time sumiu no runtime.

## Por que importa

Em projetos reais o classpath não é um saco único: o que você precisa para **compilar** não é o mesmo que precisa para **rodar**, que por sua vez difere do que precisa para **testar**. Misturar tudo gera artefatos inchados, conflitos de versão e bugs que só aparecem em produção.

Saber declarar scopes corretamente é também questão de higiene de API: ao expor uma biblioteca, você não quer forçar todos os consumidores a herdar dependências de implementação que poderiam escolher diferente. É aí que entram `provided`, `optional` e `exclusions`. Esses mecanismos são o vocabulário do dia a dia de qualquer dev backend Java — e tema recorrente em entrevista quando se fala de empacotamento e de "por que essa classe não foi encontrada".

## Como funciona

### Declarar dependências no POM

Cada dependência fica em um bloco `<dependency>` dentro de `<dependencies>`. As coordenadas mínimas são `groupId`, `artifactId` e `version`; o `<scope>` é opcional e, quando omitido, vale `compile`.

```xml
<dependency>
  <groupId>com.example</groupId>
  <artifactId>biblioteca-core</artifactId>
  <version>1.4.0</version>
  <!-- scope omitido => compile -->
</dependency>
```

A `version` pode ser herdada de um `<dependencyManagement>` (próprio ou de um BOM importado), e nesse caso é omitida aqui — veja a nota de BOM no fim.

### Os scopes e o que cada um significa

O Maven define seis scopes. A tabela abaixo resume em quais classpaths cada um aparece e se **propaga transitivamente** (se quem depende do seu projeto também herda a dependência):

| Scope | Compile | Runtime | Test | Transitivo? | Exemplo típico |
|-------|---------|---------|------|-------------|----------------|
| `compile` (default) | sim | sim | sim | sim | biblioteca de uso geral |
| `provided` | sim | **não** | sim | **não** | `servlet-api`, Lombok |
| `runtime` | **não** | sim | sim | sim | driver JDBC |
| `test` | **não** | **não** | sim | **não** | JUnit, Mockito |
| `system` | sim | sim | sim | **não** | jar local (evitar) |
| `import` | — | — | — | **não** | só em `dependencyManagement` (BOM) |

Em detalhe:

- **`compile`** — o default. Disponível em todos os classpaths e propagado para os consumidores. Use para o que seu código importa e precisa em runtime.
- **`provided`** — disponível em compile-time e testes, mas **não é empacotado** nem aparece no runtime classpath, porque você espera que o ambiente (container, servidor de aplicação, JDK) já o forneça. Exemplos clássicos: a `servlet-api` num WAR (o Tomcat fornece) e o Lombok (só age durante a compilação). Não propaga.
- **`runtime`** — **não** está disponível no compile-time, só em runtime e testes. Use quando seu código não referencia a classe diretamente, mas a biblioteca precisa estar presente para executar — o caso canônico é o **driver JDBC**, carregado por reflexão/SPI. Propaga.
- **`test`** — disponível apenas na compilação e execução dos testes. JUnit, Mockito, AssertJ vivem aqui. Não vaza para o artefato nem para os consumidores. Não propaga.
- **`system`** — como `provided`, mas você aponta o jar por caminho absoluto no disco via `<systemPath>`, em vez de resolver no repositório. **Evite**: amarra o build à máquina e quebra portabilidade/CI. Existe quase só por compatibilidade legada.
- **`import`** — caso especial, válido **somente** dentro de `<dependencyManagement>` e apenas em dependências do tipo `pom`. Substitui a dependência pela lista efetiva de `<dependencyManagement>` do POM apontado. É o mecanismo de **BOM** (Bill of Materials) — ver [[03-Dominios/Tecnologia/Java/Build e tooling/11 - BOM e dependency management|BOM e dependency management]].

### Transitividade e exclusions

Quando uma dependência arrasta outras, o scope da transitiva no seu projeto é o cruzamento entre o scope que você declarou e o scope original dela. A regra prática: uma dependência `compile` que traz uma transitiva `runtime` chega no seu projeto como `runtime`; uma `provided` que traz `compile` chega como `provided`; e dependências `test` ou `provided` **não propagam** suas transitivas para consumidores. Por isso `provided` e `test` são "barreiras" naturais na árvore.

Para **cortar** uma transitiva específica que veio junto e você não quer (versão conflitante, biblioteca redundante, dependência pesada), use `<exclusions>`. O bloco `<exclusion>` exige só `groupId` e `artifactId` — sem versão:

```xml
<dependency>
  <groupId>com.example</groupId>
  <artifactId>biblioteca-x</artifactId>
  <version>2.0.0</version>
  <exclusions>
    <exclusion>
      <groupId>com.example.legacy</groupId>
      <artifactId>modulo-indesejado</artifactId>
    </exclusion>
  </exclusions>
</dependency>
```

Para o lado oposto — você **depende** de algo mas não quer empurrá-lo aos seus consumidores — marque `<optional>true</optional>`. Pense em opcional como "excluído por padrão": você usa em casa, mas quem depender de você precisa redeclarar explicitamente se quiser.

```xml
<dependency>
  <groupId>com.example</groupId>
  <artifactId>integracao-opcional</artifactId>
  <version>1.1.0</version>
  <optional>true</optional>
</dependency>
```

## Na prática

POM mostrando vários scopes e uma exclusão de transitiva:

```xml
<dependencies>

  <!-- compile (default): usado e empacotado, propaga -->
  <dependency>
    <groupId>com.example</groupId>
    <artifactId>app-core</artifactId>
    <version>1.4.0</version>
  </dependency>

  <!-- provided: o container fornece em runtime, não empacota -->
  <dependency>
    <groupId>com.example</groupId>
    <artifactId>servlet-api</artifactId>
    <version>5.0.0</version>
    <scope>provided</scope>
  </dependency>

  <!-- runtime: driver JDBC, ausente no compile, presente ao rodar -->
  <dependency>
    <groupId>com.example</groupId>
    <artifactId>jdbc-driver</artifactId>
    <version>42.7.0</version>
    <scope>runtime</scope>
  </dependency>

  <!-- test: só na compilação e execução dos testes -->
  <dependency>
    <groupId>com.example</groupId>
    <artifactId>test-framework</artifactId>
    <version>5.10.0</version>
    <scope>test</scope>
  </dependency>

  <!-- compile com exclusão de transitiva conflitante -->
  <dependency>
    <groupId>com.example</groupId>
    <artifactId>biblioteca-x</artifactId>
    <version>2.0.0</version>
    <exclusions>
      <exclusion>
        <groupId>com.example.legacy</groupId>
        <artifactId>modulo-indesejado</artifactId>
      </exclusion>
    </exclusions>
  </dependency>

</dependencies>
```

## Armadilhas

### (1) `provided` esperando estar no runtime (NoClassDefFoundError)

Marcar como `provided` algo que o ambiente *não* fornece compila sem erro — porque `provided` está no compile-time — mas a classe some do artefato final e estoura `NoClassDefFoundError`/`ClassNotFoundException` ao executar. A regra: só use `provided` quando o container/JDK comprovadamente entrega aquela classe (servlet-api num WAR servido pelo Tomcat, Lombok que age só na compilação). Se a sua aplicação carrega e executa a classe por conta própria, o scope é `compile` (ou `runtime`).

### (2) Não excluir uma transitiva conflitante

Quando duas dependências arrastam versões diferentes da mesma biblioteca, o Maven escolhe uma pela árvore — e a perdedora pode quebrar em runtime (`NoSuchMethodError`, incompatibilidade binária). Inspecionar a árvore (`mvn dependency:tree`) e cortar a versão errante com `<exclusions>` resolve o sintoma; a forma estrutural de fixar versão é gerenciar em `dependencyManagement`/BOM. Os detalhes de resolução e mediação de versão estão em [[03-Dominios/Tecnologia/Java/Build e tooling/10 - Resolução de dependências e conflitos de versão|Resolução de conflitos]].

## Em entrevista

### Frase pronta (inglês)

In Maven, every dependency has a scope that determines which classpaths it appears on and whether it propagates transitively to downstream consumers. The default `compile` scope is available everywhere and is propagated, while `provided` is available at compile time but is not packaged because the runtime environment supplies it, and `runtime` is the opposite — absent at compile time but present at execution, which is exactly how JDBC drivers are wired. When a transitive dependency causes a version conflict, I inspect the tree with `mvn dependency:tree` and either exclude the unwanted artifact with an `<exclusions>` block or pin the version through dependency management.

### Vocabulário

| Termo PT | Termo EN |
| --- | --- |
| escopo da dependência (em quais classpaths ela vale) | dependency scope |
| dependência transitiva (a dependência da sua dependência) | transitive dependency |
| fornecida pelo ambiente em runtime, não empacotada | provided scope |
| caminho de classes usado na execução | runtime classpath |
| corte de uma transitiva indesejada | exclusion |
| opcional; não propaga ao consumidor ("excluded by default") | optional dependency |
| POM importado para alinhar versões | bill of materials (BOM) |

## Veja também

- [[03-Dominios/Tecnologia/Java/Build e tooling/02 - Maven — POM, coordenadas e lifecycle|Maven — o modelo]]
- [[03-Dominios/Tecnologia/Java/Build e tooling/10 - Resolução de dependências e conflitos de versão|Resolução de conflitos]]
- [[03-Dominios/Tecnologia/Java/Build e tooling/11 - BOM e dependency management|BOM e dependency management]]
- [[03-Dominios/Tecnologia/Java/Build e tooling/index|Build, tooling e ecossistema (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]

## Referências

- Apache Maven — *Introduction to the Dependency Mechanism*. https://maven.apache.org/guides/introduction/introduction-to-dependency-mechanism.html
