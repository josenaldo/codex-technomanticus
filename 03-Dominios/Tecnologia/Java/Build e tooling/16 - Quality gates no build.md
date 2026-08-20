---
title: "Quality gates no build"
created: 2026-06-11
updated: 2026-06-11
type: concept
status: seedling
publish: true
fase: magus
tags:
  - java
  - build
  - magus
  - quality
aliases:
  - "quality gates"
  - "JaCoCo"
---

# Quality gates no build

> [!abstract] TL;DR
> Um *quality gate* é uma regra que o **build** verifica e que, se violada, **falha** (`BUILD FAILURE`) — não apenas gera um relatório bonito que ninguém lê. Em Java/Maven, os quatro suspeitos de sempre se plugam no lifecycle: **JaCoCo** mede cobertura e o goal `check` reprova abaixo do `<minimum>`; **Checkstyle** verifica estilo/convenção e reprova com `failOnViolation`; **PMD** faz análise estática do código-fonte (e **CPD** caça copy-paste); **SpotBugs** analisa o bytecode atrás de *bug patterns*. Todos têm um goal `check` que se amarra a `verify` (no Gradle, à task `check`). A decisão de engenharia não é "qual ferramenta", é **quando o gate é hard (quebra o build) vs soft (só reporta)** e como usar *ratchet/baseline* pra introduzir gates em código legado sem parar o time.

## O que é

Quality gate é um limiar objetivo que o build aplica de forma automática: cobertura mínima, zero violações de estilo de severidade `error`, nenhum *bug pattern* de alta prioridade. O ponto não é o relatório — é o **veredito binário** que o gate emite e a capacidade de **falhar o build** quando o veredito é negativo.

Isso é fundamentalmente uma questão de **build**, não de teste. As ferramentas aqui não rodam testes nem decidem *o que* testar — elas **inspecionam** o resultado de uma compilação ou de uma execução de testes e bloqueiam o pipeline se algo estiver fora do contrato. Os runners de teste em si (Surefire/Failsafe), a teoria de cobertura e o mutation testing pertencem ao Galho 13 (ver [[03-Dominios/Tecnologia/Java/Testes/01 - O que é testar em Java — a pirâmide e o stack moderno|A pirâmide de testes (Galho 13)]] e [[03-Dominios/Tecnologia/Java/Testes/17 - Mutation testing — PIT e cobertura honesta|Mutation testing e cobertura honesta (Galho 13)]]). Aqui o foco é mecânico: **como plugar a ferramenta no lifecycle e fazê-la falhar o build**.

## Por que importa

Sem gate, qualidade é opinião: vira comentário de PR, depende de quem revisou, erode com o prazo. Com gate, qualidade é **contrato verificável** — o CI reprova antes de qualquer humano olhar, e o feedback é igual pra todo mundo.

A armadilha simétrica também importa: gate mal calibrado vira **teatro** (cobre o trivial e ignora a lógica) ou **ruído** (centenas de avisos não-triados que o time aprende a ignorar). Um gate bom é aquele que falha **pouco** e **por bons motivos** — quando ele acende vermelho, o time confia que há um problema real. Calibrar esse equilíbrio é trabalho de engenharia sênior, não de copiar um `pom.xml` da internet.

## Como funciona

O padrão é sempre o mesmo: a ferramenta tem um goal de **relatório** (gera HTML/XML, nunca falha) e um goal de **check** (aplica o limiar e **falha o build**). No Maven, amarra-se o `check` a uma fase tardia (`verify`, ou `check`/`test`); no Gradle, as tasks de verificação penduram na task agregadora `check`, que por sua vez é dependência de `build`.

### Cobertura — JaCoCo

O `jacoco-maven-plugin` opera em três goals encadeados:

1. **`prepare-agent`** — registra o agente de instrumentação na JVM dos testes (via `argLine`), pra que a execução do Surefire/Failsafe seja medida.
2. **`report`** — transforma os dados de execução (`jacoco.exec`) em relatório legível. **Nunca falha o build.**
3. **`check`** — avalia `<rules>` e **falha o build** se a cobertura ficar abaixo de algum `<limit>`/`<minimum>`.

A regra (`<rule>`) define o escopo (`element`: `BUNDLE`, `PACKAGE`, `CLASS`...) e um ou mais `<limit>` com `counter` (`LINE`, `BRANCH`, `INSTRUCTION`...), `value` (`COVEREDRATIO`, `MISSEDCOUNT`...) e `<minimum>`. É o `check` que transforma o número em veredito. Não há "porcentagem ideal" universal — o threshold é **trade-off**: alto demais e o time persegue cobertura de coisas triviais; baixo demais e o gate não protege nada. A questão de *que cobertura significa qualidade de verdade* é do Galho 13.

### Estilo e convenção — Checkstyle

O `maven-checkstyle-plugin` valida o **código-fonte** contra um conjunto de regras de formatação e convenção (nomes, imports, layout, design de classe). Dois pontos de execução:

- O goal **`checkstyle`** gera relatório (não falha).
- O goal **`check`** aplica `failOnViolation` (default `true`) e o `violationSeverity` (ex.: `error`): se houver violação no nível configurado, **`BUILD FAILURE`**.

Estilo é o gate mais barato de adotar (não exige nem rodar testes) e o mais fácil de virar bikeshed — por isso costuma-se herdar um padrão estabelecido (Google Java Style, Sun Conventions) em vez de inventar o próprio.

### Bugs e código problemático — PMD + SpotBugs

São complementares por **onde olham**:

- **PMD** (`maven-pmd-plugin`) faz análise estática sobre o **código-fonte** (AST): variáveis não usadas, `catch` vazio, criação desnecessária de objetos, complexidade excessiva. Inclui o **CPD** (Copy-Paste Detector), que detecta blocos duplicados. O goal **`check`** falha o build em violações; o **`cpd-check`** falha em duplicação acima de um limite de tokens.
- **SpotBugs** (`spotbugs-maven-plugin`) analisa o **bytecode** compilado atrás de *bug patterns* conhecidos (NPE prováveis, comparação de strings com `==`, recursos não fechados, concorrência suspeita). O goal **`check`** falha o build conforme `threshold`/`effort` e prioridade.

Como olham para artefatos diferentes (fonte vs bytecode), pegam classes de problema diferentes e é comum rodar os dois. O complemento `find-sec-bugs` adiciona regras de segurança ao SpotBugs.

## Na prática

JaCoCo no Maven, com o goal `check` ligado ao lifecycle e um gate hard de 80% de linhas por bundle. Domínio neutro (um módulo de pedidos):

```xml
<plugin>
  <groupId>org.jacoco</groupId>
  <artifactId>jacoco-maven-plugin</artifactId>
  <version>0.8.12</version>
  <executions>
    <!-- 1) instrumenta a JVM de teste -->
    <execution>
      <id>prepare-agent</id>
      <goals>
        <goal>prepare-agent</goal>
      </goals>
    </execution>

    <!-- 2) gera o relatório (não falha) -->
    <execution>
      <id>report</id>
      <phase>test</phase>
      <goals>
        <goal>report</goal>
      </goals>
    </execution>

    <!-- 3) o GATE: falha o build abaixo do minimum -->
    <execution>
      <id>coverage-gate</id>
      <phase>verify</phase>
      <goals>
        <goal>check</goal>
      </goals>
      <configuration>
        <rules>
          <rule>
            <element>BUNDLE</element>
            <limits>
              <limit>
                <counter>LINE</counter>
                <value>COVEREDRATIO</value>
                <minimum>0.80</minimum>
              </limit>
              <limit>
                <counter>BRANCH</counter>
                <value>COVEREDRATIO</value>
                <minimum>0.70</minimum>
              </limit>
            </limits>
            <!-- não cobrar cobertura de código gerado -->
            <excludes>
              <exclude>com.exemplo.pedidos.generated.*</exclude>
            </excludes>
          </rule>
        </rules>
      </configuration>
    </execution>
  </executions>
</plugin>
```

Mesmo gate no Gradle (Kotlin DSL) — `jacocoTestCoverageVerification` pendura na task `check`:

```kotlin
plugins {
    java
    jacoco
}

tasks.jacocoTestCoverageVerification {
    violationRules {
        rule {
            element = "BUNDLE"
            limit {
                counter = "LINE"
                value = "COVEREDRATIO"
                minimum = "0.80".toBigDecimal()
            }
            limit {
                counter = "BRANCH"
                value = "COVEREDRATIO"
                minimum = "0.70".toBigDecimal()
            }
            excludes = listOf("com.exemplo.pedidos.generated.*")
        }
    }
}

// torna o gate parte de `check` — e portanto de `build`
tasks.check {
    dependsOn(tasks.jacocoTestCoverageVerification)
}
```

Rodando o gate. No Maven, `verify` executa os checks plugados nessa fase; no Gradle, `check` agrega todas as verificações:

```bash
# Maven: roda testes, gera relatório e aplica o gate de cobertura
mvn clean verify

# se a cobertura cair abaixo do minimum:
#   [ERROR] Rule violated for bundle pedidos: lines covered ratio is 0.74, but expected minimum is 0.80
#   [INFO] BUILD FAILURE

# Gradle: a task check dispara o verification (e Checkstyle/PMD/SpotBugs se plugados)
./gradlew check
```

Checkstyle, PMD e SpotBugs seguem o mesmo padrão: cada um expõe um goal `check` (`mvn checkstyle:check`, `mvn pmd:check`, `mvn spotbugs:check`) que se amarra a `verify`. Plugados, um único `mvn verify` aplica todos os gates de uma vez.

## Armadilhas

### (1) Threshold de cobertura como teatro

Um `<minimum>0.80</minimum>` aplicado ao projeto inteiro é facilmente satisfeito **cobrindo o trivial**: getters/setters, DTOs, `toString`, `equals`, mappers gerados. O número fica verde enquanto a lógica de negócio crítica continua sem teste de comportamento. O gate vira **teatro de qualidade** — protege a métrica, não o software. Mitigação no nível do build: `excludes` para código gerado/DTOs e regras por pacote (cobrar mais do pacote `domain` que do `dto`). O problema mais profundo — *cobertura não prova que o teste verifica algo* — é exatamente o que mutation testing ataca; ver [[03-Dominios/Tecnologia/Java/Testes/17 - Mutation testing — PIT e cobertura honesta|Mutation testing (Galho 13)]].

### (2) Gate que ninguém olha (ou está desligado no CI)

Clássico: o `pom.xml` tem o plugin configurado, mas o goal `check` nunca é executado no CI (o pipeline roda `mvn test`, não `mvn verify`), ou alguém adicionou `-Djacoco.skip=true` / `<failOnViolation>false</failOnViolation>` "temporariamente" há dois anos. Um gate soft (só relatório) que ninguém abre é equivalente a não ter gate. Verifique que o pipeline executa a **fase** que dispara o `check` e que `skip`/`failOnViolation` não foram silenciados. Gate de verdade **quebra o build vermelho**; relatório é complemento, não substituto.

### (3) SpotBugs/PMD com ruído não-triado afogando o sinal

Ligar SpotBugs ou PMD com o ruleset cheio num codebase legado produz centenas a milhares de findings de uma vez. Se você falhar o build em todos imediatamente, o time não consegue mergear nada e o gate é desabilitado na primeira sexta-feira. Pior: avisos não-triados ensinam o time a ignorar a ferramenta inteira (*alert fatigue*). A saída é o **ratchet/baseline**: registrar os findings existentes como linha de base aceita (ex.: `excludeFilterFile` no SpotBugs, baseline no Gradle/SonarQube) e falhar o build apenas em **novos** problemas — "não pode piorar". A dívida existente é paga incrementalmente, sem travar o fluxo. Hard gate em código novo, soft/baseline no legado.

## Em entrevista

### Frase pronta (inglês)

> A quality gate is only a gate if it can fail the build — otherwise it's just a report nobody reads. In Maven I bind JaCoCo's `check` goal, plus Checkstyle, PMD and SpotBugs `check` goals, to the `verify` phase; in Gradle they all hang off the `check` task. The hard part isn't wiring the plugins, it's calibration: I set a coverage minimum as a trade-off rather than chasing a magic number, I exclude generated code and DTOs so the gate measures real logic instead of getters, and for legacy code I introduce static-analysis gates with a ratchet baseline so the build only fails on new violations. That keeps the signal high — when the gate goes red, the team trusts there's a genuine problem, instead of learning to ignore the noise.

### Vocabulário

| Termo PT | Termo EN |
| --- | --- |
| portão de qualidade (limiar que falha o build) | quality gate |
| falhar o build | fail the build |
| limiar / cobertura mínima | threshold / minimum coverage |
| análise estática | static analysis |
| padrão de bug (no bytecode) | bug pattern |
| linha de base / catraca (gate incremental) | baseline / ratchet |
| fadiga de alertas (ruído não-triado) | alert fatigue |
| teatro de cobertura (cobre o trivial) | coverage theater / gaming the metric |

## Veja também

- [[03-Dominios/Tecnologia/Java/Build e tooling/17 - Reprodutibilidade e reproducible builds|Reprodutibilidade]]
- [[03-Dominios/Tecnologia/Java/Testes/17 - Mutation testing — PIT e cobertura honesta|Mutation testing (Galho 13)]]
- [[03-Dominios/Tecnologia/Java/Testes/01 - O que é testar em Java — a pirâmide e o stack moderno|A pirâmide de testes (Galho 13)]]
- [[03-Dominios/Tecnologia/Java/Build e tooling/index|Build, tooling e ecossistema (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]

## Referências

- JaCoCo — Maven Plugin (goals `prepare-agent`, `report`, `check`): https://www.jacoco.org/jacoco/trunk/doc/maven.html
- Checkstyle: https://checkstyle.org/
- maven-checkstyle-plugin (`check`, `failOnViolation`): https://maven.apache.org/plugins/maven-checkstyle-plugin/
- PMD (análise estática) e CPD (copy-paste detector): https://pmd.github.io/
- maven-pmd-plugin (`check`, `cpd-check`): https://maven.apache.org/plugins/maven-pmd-plugin/
- SpotBugs: https://spotbugs.github.io/
- spotbugs-maven-plugin (`check`): https://spotbugs.readthedocs.io/en/latest/maven.html
