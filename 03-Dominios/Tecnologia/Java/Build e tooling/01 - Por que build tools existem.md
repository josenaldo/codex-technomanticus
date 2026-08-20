---
title: "Por que build tools existem"
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
aliases:
  - "Por que build tools existem"
---

# Por que build tools existem

> [!abstract] TL;DR
> Um **build tool** (Maven, Gradle) é um **gestor de build + dependências**: ele resolve o grafo de dependências (incluindo transitivas), automatiza o ciclo de vida (compilar, testar, empacotar) e produz um artefato reprodutível — coisas que `javac` + `jar` na mão não fazem em escala.
> Regra prática: build tool **não é compilador**; ele orquestra o `javac` e tudo ao redor. O bytecode que sai é o mesmo.
> Importa porque, em qualquer projeto Java real, é o build tool que define o que é "buildável", o que entra no classpath e o que o CI consegue reproduzir. Sem ele, o projeto não escala além de um punhado de classes.

## O que é

Segundo a documentação oficial, **Maven** é "uma ferramenta para construir e gerenciar qualquer projeto baseado em Java", que faz isso a partir de um **Project Object Model (POM)** e um conjunto de plugins, oferecendo "gestão superior de dependências, incluindo atualização automática e dependências transitivas". O **Gradle**, por sua vez, se define como "uma ferramenta de automação de build open-source, rápida, confiável e adaptável, com uma linguagem de build declarativa, elegante e extensível", e a documentação trata gestão de dependências como capacidade central, ao lado de execução de tarefas (`tasks`).

Em uma frase: **um build tool é um gestor de build + dependências.** Ele não é o compilador — ele é quem chama o compilador na hora certa, com o classpath certo, e empacota o resultado.

A pergunta natural de quem está começando é: "mas eu já consigo compilar com `javac` e empacotar com `jar` — por que preciso de mais alguma coisa?". A resposta é que `javac` e `jar` resolvem o caso de **uma ou duas classes sem dependências externas**. No momento em que você depende de uma biblioteca que depende de outras três, que por sua vez exigem versões específicas de uma quarta, montar o classpath na mão deixa de ser viável.

## Por que importa

Pense no `javac` como uma **furadeira**: uma ferramenta excelente para um furo. O build tool é a **linha de montagem** ao redor dela — define a ordem das etapas, alimenta as peças certas (dependências), aciona a furadeira (compilação), testa o produto e o embala em uma caixa padronizada (o artefato). Você não monta um carro com uma furadeira solta na mão; você monta numa linha.

Quatro problemas concretos que aparecem quando se tenta buildar Java "na mão" e que o build tool resolve:

1. **Classpath manual.** Cada `.jar` de dependência precisa estar listado no `-cp`. Com 5 bibliotecas vira tedioso; com 50, vira impossível de manter à mão.
2. **Dependências transitivas.** A biblioteca A precisa da B, que precisa da C. Você só declarou A — quem traz B e C? O build tool calcula esse fechamento (closure) automaticamente.
3. **Ordem de compilação e ciclo de vida.** Compilar, rodar testes, empacotar, instalar — nessa ordem, e só prosseguindo se a etapa anterior passou. Isso é o **lifecycle** (Maven) ou o grafo de **tasks** (Gradle).
4. **Reprodutibilidade.** O build da sua máquina precisa dar o mesmo resultado no CI e na máquina do colega. Versões fixas + repositório central + cache local garantem isso.

> [!tip] O repositório local como "cache de bibliotecas"
> Tanto Maven quanto Gradle baixam as dependências de repositórios remotos (como o Maven Central) **uma vez** e guardam num diretório local na sua máquina (`~/.m2/repository` no Maven, `~/.gradle/caches` no Gradle). Da segunda build em diante, elas saem do cache — não há novo download. É o mesmo princípio de um cache de navegador, só que para bibliotecas.

## Como funciona

Independente da ferramenta, o ciclo conceitual é o mesmo:

1. Você **declara** o que o projeto precisa (dependências, versões) e o que ele é (coordenadas, plugins).
2. O build tool **resolve o grafo de dependências**: lê suas declarações, segue as transitivas, decide quais versões usar e baixa o que falta para o cache local.
3. O build tool **executa o lifecycle / o grafo de tasks**: compila com `javac`, roda testes, empacota.
4. Sai um **artefato reprodutível** (um `.jar`, por exemplo) — o mesmo, dadas as mesmas entradas.

A diferença de filosofia entre as duas ferramentas aparece exatamente em *como* você declara as coisas — e essa é a **tese-assinatura deste galho**:

> [!important] A escolha não é sobre o bytecode
> Maven e Gradle produzem o **mesmo bytecode** — ambos chamam o mesmo `javac`. A escolha entre eles é sobre o **modelo de configuração**: Maven aposta em **convenção e declaração** (um POM XML que descreve *o que* o projeto é, com um lifecycle fixo); Gradle aposta em **flexibilidade e imperatividade** (um build script em Groovy/Kotlin onde você pode descrever *como* cada task se comporta). Convenção/declarativo (Maven) vs flexibilidade/imperativo (Gradle) — esse trade-off honesto é destrinchado em [[03-Dominios/Tecnologia/Java/Build e tooling/08 - Maven vs Gradle — trade-offs honestos|Maven vs Gradle]].

## Na prática

Imagine um projeto mínimo com duas classes no pacote `com.example`: `Order` e `Payment`, onde `Order` usa uma biblioteca de logging (que, por sua vez, traz uma dependência transitiva).

### O problema, compilando na mão

A árvore do problema quando você tenta fazer tudo manualmente:

```text
com.example.Order      -> usa biblioteca de logging (logging-api)
com.example.Payment    -> usa Order
                          |
logging-api            -> depende de logging-core (TRANSITIVA: você não declarou)
                          |
logging-core           -> precisa de uma versão específica
```

Para compilar e rodar "na mão", você precisaria baixar manualmente cada `.jar` (inclusive o `logging-core`, que ninguém te avisou que era necessário) e montar o classpath à mão:

```bash
# 1. Você mesmo encontra, baixa e versiona cada jar em libs/
#    (incluindo a transitiva logging-core, que descobriu na marra)
# 2. Compila apontando o classpath manualmente:
javac -cp "libs/logging-api.jar:libs/logging-core.jar" \
      -d out \
      src/com/example/Order.java src/com/example/Payment.java

# 3. Empacota na mão:
jar --create --file app.jar -C out .

# 4. Roda repetindo TODO o classpath:
java -cp "out:libs/logging-api.jar:libs/logging-core.jar" com.example.Payment
```

Funciona — para duas classes e duas dependências. Mas cada nova biblioteca exige editar o `-cp` à mão, descobrir suas transitivas no escuro e garantir que a versão bate em todas as máquinas. Não escala.

### A mesma coisa, com build tool

Com um build tool, você apenas **declara** a dependência direta (`logging-api`). A transitiva (`logging-core`) é resolvida e baixada para o cache local automaticamente, o classpath é montado pela ferramenta, e o empacotamento vira um comando único:

```bash
# Maven: resolve o grafo, compila, testa e empacota em out/target/*.jar
mvn package

# Gradle: equivalente, executando a task 'build'
gradle build
```

Você nunca escreveu um `-cp`. Nunca caçou a transitiva. E o resultado é reprodutível: o colega que clonar o repositório roda o mesmo comando e obtém o mesmo artefato.

> [!question] Onde está o `javac` aqui?
> Continua lá, escondido. `mvn package` e `gradle build`, em algum ponto do lifecycle, invocam o `javac` para você — com o classpath que a ferramenta montou a partir do grafo de dependências. O build tool não substituiu o compilador; ele o orquestrou.

## Armadilhas

### (1) Achar que "build tool é só pra compilar"

É o mal-entendido fundador. Como build tool e compilador andam juntos, é tentador tratá-los como sinônimos — e concluir que o build tool é "um `javac` mais chique".

Exemplo: alguém adiciona uma dependência no POM, roda só "compilar" mentalmente e se surpreende quando os testes que rodam no lifecycle quebram a build, ou quando o artefato empacotado não inclui o que deveria.

Fix: lembre que compilar é **uma fase** do lifecycle — resolver dependências, testar, empacotar e instalar também são; o build tool orquestra todas.

### (2) Ignorar o build até quebrar no CI

"Na minha máquina funciona" quase sempre é um problema de build não-reprodutível: versões não fixadas, dependência que existe só no cache local de quem escreveu, ou um passo manual que não está no POM/script.

Exemplo: a aplicação roda localmente porque um `.jar` antigo ficou no cache, mas a build limpa no CI baixa a versão declarada (diferente) e falha.

Fix: rode periodicamente uma build limpa (sem reaproveitar artefatos locais) e fixe versões; trate o que o CI faz como a fonte da verdade do que é "buildável".

### (3) Confundir a escolha da ferramenta com uma decisão técnica de bytecode

Achar que "Gradle gera código mais rápido" ou "Maven gera binário mais leve" — não geram; o bytecode é o mesmo, pois o compilador é o mesmo.

Exemplo: justificar a migração Maven→Gradle por "performance da aplicação" em vez do que de fato muda (modelo de build, performance *da build*, flexibilidade de configuração).

Fix: avalie Maven vs Gradle pelo **modelo de configuração e tooling**, não pelo artefato final — veja [[03-Dominios/Tecnologia/Java/Build e tooling/08 - Maven vs Gradle — trade-offs honestos|Maven vs Gradle]].

## Em entrevista

### Frase pronta (inglês)

> A build tool like Maven or Gradle is a build *and* dependency manager, not a compiler — it resolves the dependency graph, including transitive dependencies, drives the lifecycle from compilation to packaging, and produces a reproducible artifact. The trade-off between the two is mostly about the configuration model: Maven favors convention and a declarative POM, while Gradle favors flexibility and an imperative, scriptable build. One caveat worth stating up front: both invoke the same `javac` under the hood, so the choice doesn't change the bytecode — it changes how the build itself is described, cached, and evolved.

### Vocabulário

| Termo PT | Termo EN |
| --- | --- |
| Ferramenta de build | Build tool |
| Gestão de dependências | Dependency management |
| Dependência transitiva | Transitive dependency |
| Grafo de dependências | Dependency graph |
| Ciclo de vida (do build) | Build lifecycle |
| Artefato reprodutível | Reproducible artifact |
| Caminho de classes | Classpath |
| Empacotamento | Packaging |
| Repositório local (cache) | Local repository (cache) |

## A fronteira deste galho

Build é um tema com muitas fronteiras vizinhas. Para manter as notas atômicas, **este galho linka, não re-explica** os quatro temas abaixo — cada um vive no seu galho próprio:

- **Módulos (JPMS), `jlink` e AOT com GraalVM** — como o código é modularizado e como gerar imagens nativas/runtimes enxutos é assunto do **Galho 3** (plataforma e runtime). Aqui só importa que o build tool sabe acionar esses passos.
- **`jpackage`** (gerar instaladores/pacotes nativos da aplicação) — coberto no **Galho 6**.
- **Starters e `repackage`** (o fat-jar executável do Spring Boot e o ecossistema de starters) — coberto no **Galho 8**.
- **Quality gates e cobertura** (gates de qualidade, métricas de cobertura no pipeline) — coberto no **Galho 13**.

Quando alguma dessas peças aparecer numa nota deste galho, ela será citada como "(Galho N)" e o leitor é remetido ao galho correspondente — não duplicamos a explicação aqui.

## Veja também

- [[03-Dominios/Tecnologia/Java/Build e tooling/02 - Maven — POM, coordenadas e lifecycle|Maven — o modelo]]
- [[03-Dominios/Tecnologia/Java/Build e tooling/05 - Gradle — build script, tasks e configurations|Gradle — o modelo]]
- [[03-Dominios/Tecnologia/Java/Build e tooling/08 - Maven vs Gradle — trade-offs honestos|Maven vs Gradle]]
- [[03-Dominios/Tecnologia/Java/Build e tooling/index|Build, tooling e ecossistema (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]

## Referências

- Apache Maven — *What is Maven?* — https://maven.apache.org/what-is-maven.html
- Apache Maven — *Guides / Introduction* — https://maven.apache.org/guides/
- Gradle — *User Manual (What is Gradle?)* — https://docs.gradle.org/current/userguide/userguide.html
