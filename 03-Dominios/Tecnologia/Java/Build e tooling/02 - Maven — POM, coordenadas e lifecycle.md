---
title: "Maven — POM, coordenadas e lifecycle"
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
  - "Maven — o modelo"
  - "POM"
---

# Maven — POM, coordenadas e lifecycle

> [!abstract] TL;DR
> Maven é uma ferramenta de build **declarativa**: você descreve *o que* o projeto é num arquivo `pom.xml` (o **POM**, Project Object Model), e o Maven decide *como* construí-lo seguindo convenções. Todo artefato é identificado por **coordenadas GAV** (`groupId:artifactId:version`), e o build percorre um **lifecycle** de phases ordenadas (`validate` → `compile` → `test` → `package` → `verify` → `install` → `deploy`). A phase em si não faz nada: ela apenas dispara os **goals de plugin** que foram ligados a ela. A linha estável é o **Maven 3.9.x** (3.9.16, GA em maio de 2026); o **Maven 4** ainda é **release candidate** (4.0.0-rc-5) e não deve ir pra produção.

## O que é

Maven é uma ferramenta de build e gerenciamento de projetos Java mantida pela Apache. A ideia central é **convenção sobre configuração**: em vez de escrever um script imperativo dizendo "compile estes arquivos, depois copie aqueles, depois empacote", você descreve o projeto de forma **declarativa** num único arquivo XML — o `pom.xml` — e o Maven aplica um modelo padrão de diretórios e etapas.

Esse modelo declarativo apoia-se em três pilares:

- **POM** (`pom.xml`): o descritor do projeto. Diz quem o projeto é, do que ele depende, e como deve ser construído.
- **Coordenadas GAV**: o "endereço" único de qualquer artefato no ecossistema Maven (`groupId:artifactId:version`).
- **Lifecycle**: a sequência fixa de etapas (phases) que o Maven percorre para construir o projeto, executando goals de plugins ligados a cada etapa.

Se você não especifica algo, o Maven usa um valor padrão herdado do **Super POM** (o POM-raiz implícito de todo projeto). Por isso um POM mínimo tem só cinco linhas úteis e mesmo assim compila, testa e empacota.

## Por que importa

Antes do Maven, builds Java eram scripts Ant — imperativos, longos, e diferentes em cada projeto. Cada repositório reinventava sua própria estrutura de pastas e suas próprias tarefas. Entrar num projeto novo significava aprender o build do zero.

O Maven padronizou isso. Como a convenção é a mesma em qualquer projeto Maven, `mvn package` faz a mesma coisa em qualquer lugar: compila `src/main/java`, roda os testes de `src/test/java`, e gera o `.jar` em `target/`. Você troca de projeto e o build já é familiar.

Para uma entrevista de nível pleno/sênior, dominar o modelo do Maven importa porque:

- É o vocabulário comum de quase todo backend Java corporativo (Spring Boot inclusive).
- As perguntas favoritas — "qual a diferença entre `package` e `install`?", "o que é uma phase?", "o que são as coordenadas GAV?" — testam se você entende o **modelo**, não se decorou comandos.
- Confundir phase com goal é um erro clássico que revela falta de base.

## Como funciona

### POM e coordenadas GAV

O `pom.xml` é o coração de um projeto Maven. Os campos mínimos obrigatórios são:

- `<modelVersion>`: a versão do modelo do POM, sempre `4.0.0` (no Maven 3 e 4).
- `<groupId>`: o grupo/organização dona do projeto, normalmente um domínio reverso (`com.example`).
- `<artifactId>`: o nome do artefato (`order-service`).
- `<version>`: a versão do artefato (`1.0.0-SNAPSHOT`).

Esses três últimos formam as **coordenadas GAV** — o nome plenamente qualificado do artefato:

```
groupId:artifactId:version
com.example:order-service:1.0.0-SNAPSHOT
```

Duas peças opcionais completam o endereçamento:

- **`packaging`**: o tipo de saída do build. Padrão é `jar`; outros valores comuns são `war`, `pom` (para projetos pai/agregadores) e `ear`. Se você não declara, o Maven assume `jar`.
- **`classifier`**: um sufixo opcional que distingue variantes do *mesmo* GAV — por exemplo `sources` (jar com o código-fonte) ou `javadoc`. O artefato `com.example:order-service:1.0.0:jar:sources` é a variante de fontes do mesmo GAV.

O sufixo `-SNAPSHOT` na versão marca uma build em desenvolvimento (mutável); uma versão sem `-SNAPSHOT` é uma **release** imutável.

### Repositórios local e remotos

Maven não baixa cada dependência toda vez. Ele usa um **repositório local** — uma pasta-cache na sua máquina, por padrão `~/.m2/repository`. Pense nela como um **cache de bibliotecas**: cada artefato baixado fica guardado lá, organizado pelas coordenadas GAV.

Quando o build precisa de uma dependência:

1. Maven procura no **repositório local** (`~/.m2/repository`). Se já está lá, usa.
2. Se não está, busca nos **repositórios remotos** — por padrão o **Maven Central** (`https://repo.maven.apache.org/maven2`), herdado do Super POM. Empresas frequentemente colocam um proxy/mirror (Nexus, Artifactory) no meio.
3. O artefato baixado é gravado no repositório local, então a próxima build não baixa de novo.

É por isso que a primeira build de um projeto novo é lenta (baixa tudo) e as seguintes são rápidas (cache quente).

### Lifecycle, phases e goals

O Maven define três lifecycles built-in: `clean` (limpa o `target/`), `default` (constrói o projeto) e `site` (gera documentação). O importante para o dia a dia é o **default lifecycle**, uma sequência **ordenada** de phases. As principais, na ordem:

`validate` → `compile` → `test` → `package` → `verify` → `install` → `deploy`

(Entre elas existem phases intermediárias como `process-resources`, `test-compile` e `integration-test`, mas essas sete são o esqueleto que importa decorar.)

O ponto-chave, que separa quem entende Maven de quem decora comandos:

> **Uma phase não faz nada sozinha.** Ela é só um marco na sequência. O trabalho real é feito por **goals de plugin** que foram **ligados (bound)** àquela phase.

Um **plugin** é um artefato que fornece **goals** (tarefas concretas, no formato `plugin:goal`). Quando uma phase executa, o Maven roda todos os goals ligados a ela. As ligações padrão para `packaging` = `jar` são:

| Phase | Goal ligado (plugin:goal) |
| --- | --- |
| `process-resources` | `resources:resources` |
| `compile` | `compiler:compile` |
| `test` | `surefire:test` |
| `package` | `jar:jar` |
| `install` | `install:install` |
| `deploy` | `deploy:deploy` |

E há mais uma regra que confunde iniciantes: as phases são **cumulativas**. Quando você pede `mvn package`, o Maven executa **todas as phases anteriores na ordem** (`validate`, `compile`, `test`...) e só então `package`. Você nunca roda `package` "puro" — ele arrasta tudo que vem antes.

Você também pode invocar um goal diretamente, fora do lifecycle, no formato `plugin:goal` — por exemplo `dependency:tree`. Esse goal não está ligado a nenhuma phase do default lifecycle; você o chama de propósito.

### Versão: 3.9.x estável, Maven 4 ainda RC

A linha **estável** atual é o **Maven 3.9.x** — a release mais recente é a **3.9.16** (GA em maio de 2026), que roda em JDK 8+. É o que você usa em produção.

O **Maven 4** ainda está em **release candidate** (4.0.0-rc-5 no momento) e **não é GA** — a própria página de download avisa que não é seguro para produção. Ele exige JDK 17+ e traz mudanças no modelo (consumer/flattened POM, `<packaging>bom</packaging>` nativo, sintaxe de versão CI-friendly, reproducible builds por padrão), mas trate isso tudo como **"vindo no Maven 4"**, não como algo presente no seu dia a dia.

## Na prática

POM mínimo válido de um serviço hipotético:

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
                             https://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>

  <groupId>com.example</groupId>
  <artifactId>order-service</artifactId>
  <version>1.0.0-SNAPSHOT</version>
  <packaging>jar</packaging>

  <properties>
    <maven.compiler.release>21</maven.compiler.release>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
  </properties>
</project>
```

As coordenadas GAV desse projeto são `com.example:order-service:1.0.0-SNAPSHOT`.

Comandos do dia a dia:

```bash
# Constrói o projeto até a phase package: valida, compila, testa e gera o jar em target/
mvn package

# Mostra a árvore de dependências resolvidas (goal direto, fora do lifecycle)
mvn dependency:tree

# Limpa o target/ e instala o artefato no repositório local (~/.m2/repository)
mvn clean install
```

## Armadilhas

### (1) Confundir phase com goal

Phase e goal não são a mesma coisa. **Phase** é um marco no lifecycle (`compile`, `test`, `package`) — um ponto na linha do tempo do build, que por si só não executa nada. **Goal** é uma tarefa concreta fornecida por um plugin (`compiler:compile`, `surefire:test`, `jar:jar`). A phase só "funciona" porque tem goals **ligados** a ela.

Sintoma do mal-entendido: tentar rodar `mvn compiler:compile` achando que é o mesmo que `mvn compile`. São parecidos no caso default, mas conceitualmente diferentes — `mvn compile` executa a *phase* (e tudo antes dela), enquanto `mvn compiler:compile` executa só aquele *goal* isolado.

### (2) Achar que `package` roda `install` ou `deploy`

Como as phases são cumulativas **para trás**, é tentador achar que rodar `package` também instala e publica o artefato. Não roda. `mvn package` executa as phases **até** `package` (inclusive), e **para ali**. O jar fica em `target/`, mas não vai para o `~/.m2/repository` (isso é `install`) nem para o repositório remoto (isso é `deploy`).

A ordem é `package` → `verify` → `install` → `deploy`. Se você precisa que outro projeto local consuma seu artefato, rode `mvn install`. Se precisa publicá-lo num repositório remoto compartilhado, rode `mvn deploy` (que, sendo a última phase, arrasta `install` junto).

## Em entrevista

### Frase pronta (inglês)

Maven is a declarative build tool: instead of scripting how to build the project, you describe what the project is in a `pom.xml`, and Maven applies a standard model based on convention over configuration. Every artifact is identified by its GAV coordinates — groupId, artifactId and version — and dependencies are resolved from a local repository cache under `~/.m2`, falling back to remote repositories like Maven Central. The build runs through an ordered lifecycle of phases such as `validate`, `compile`, `test`, `package` and `install`; a phase itself does nothing — it simply triggers the plugin goals bound to it, which is why running `package` also runs every phase before it but stops short of `install` and `deploy`.

### Vocabulário

| Português | Inglês |
| --- | --- |
| ferramenta de build | build tool |
| descritor declarativo | declarative descriptor |
| coordenadas (GAV) | (GAV) coordinates |
| repositório local | local repository |
| ciclo de vida / etapa | lifecycle / phase |
| meta de plugin (ligada) | (bound) plugin goal |
| convenção sobre configuração | convention over configuration |
| árvore de dependências | dependency tree |

## Veja também

- [[03-Dominios/Tecnologia/Java/Build e tooling/03 - Maven — dependências, scopes e exclusions|Maven — dependências e scopes]]
- [[03-Dominios/Tecnologia/Java/Build e tooling/04 - Maven — plugins, profiles e o wrapper|Maven — plugins e profiles]]
- [[03-Dominios/Tecnologia/Java/Build e tooling/08 - Maven vs Gradle — trade-offs honestos|Maven vs Gradle]]
- [[03-Dominios/Tecnologia/Java/Build e tooling/10 - Resolução de dependências e conflitos de versão|Resolução de dependências]]
- [[03-Dominios/Tecnologia/Java/Build e tooling/index|Build, tooling e ecossistema (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]

## Referências

- Introduction to the POM — https://maven.apache.org/guides/introduction/introduction-to-the-pom.html
- Introduction to the Build Lifecycle — https://maven.apache.org/guides/introduction/introduction-to-the-lifecycle.html
- Apache Maven — Download (versões 3.9.16 estável / 4.0.0-rc-5) — https://maven.apache.org/download.cgi
