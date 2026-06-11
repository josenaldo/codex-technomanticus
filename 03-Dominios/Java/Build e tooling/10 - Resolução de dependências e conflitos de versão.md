---
title: "Resolução de dependências e conflitos de versão"
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
aliases:
  - "nearest-wins"
  - "conflito de versão"
---

# Resolução de dependências e conflitos de versão

> [!abstract] TL;DR
> Quando você declara uma dependência, ela arrasta as dela junto (resolução **transitiva**). Cedo ou tarde, duas dessas transitivas pedem versões diferentes da mesma lib — é o **conflito de versão**. Maven resolve por **nearest-wins** (a versão mais próxima da raiz na árvore vence; empate de profundidade → a primeira declarada vence). Gradle resolve por **highest-version-wins** (a versão mais alta vence), e você ajusta isso com **resolution strategy** (`failOnVersionConflict()`, `force`, constraints, `strictly`). Os dois algoritmos são **diferentes**, e isso é a causa raiz de `NoSuchMethodError` que só aparece em runtime.

## O que é

Você nunca depende só do que declara. Ao adicionar uma única dependência, o build importa também tudo de que **ela** depende, e tudo de que **essas** dependem, recursivamente. Isso é a **resolução transitiva**: a árvore inteira abaixo de cada dependência direta entra no seu classpath sem você pedir nome por nome.

O problema nasce quando dois ramos diferentes dessa árvore pedem a **mesma biblioteca em versões diferentes**. Só pode haver uma versão de cada artefato no classpath final, então o build precisa de uma regra para **escolher uma e descartar a outra**. Essa regra é o algoritmo de resolução de conflitos, e ele é diferente entre Maven e Gradle.

## Por que importa

Porque a escolha errada não dá erro de compilação — ela dá erro **em runtime**, geralmente longe da causa. O build "resolve" o conflito silenciosamente, compila, empacota, e só em produção (ou no teste de integração) explode com `NoSuchMethodError` ou `NoClassDefFoundError`: a versão que ganhou não tem o método que outra parte do código esperava.

E o detalhe que pega gente sênior desprevenida: **Maven e Gradle resolvem o mesmo conflito de formas diferentes**. Migrar um projeto de um para o outro, ou raciocinar sobre um sem saber qual ferramenta está embaixo, leva a conclusões erradas. Saber ler a árvore de dependências e saber qual algoritmo está agindo é a diferença entre adivinhar e diagnosticar.

## Como funciona

### Resolução transitiva: você ganha C sem pedir

Considere `A → B → C`: seu projeto `A` declara `B`, e `B` declara `C`. Você nunca escreveu `C` no seu build, mas `C` está no seu classpath. É herança de dependências, e é o que torna o ecossistema produtivo — e também o que torna conflitos inevitáveis, porque cada dependência direta arrasta uma subárvore inteira que você não controla.

A unidade do conflito é o par `groupId:artifactId` (Maven) ou o módulo (Gradle). Quando dois caminhos diferentes da árvore chegam ao **mesmo** par com versões diferentes, há conflito.

Vale separar dois fenômenos que muita gente confunde:

- **Dependência direta** — a que você escreve, com nome e (em geral) versão.
- **Dependência transitiva** — a que entra de carona, herdada de uma direta. Você não a nomeia, mas ela está no classpath e pode quebrar você.

Quanto mais dependências diretas, maior a subárvore transitiva e maior a chance de dois ramos colidirem na mesma lib. Por isso projetos grandes vivem mais conflitos: não é azar, é combinatória.

### Nearest-wins do Maven (dependency mediation)

Maven usa o que a doc chama de **"nearest definition"** — a versão escolhida é a da dependência **mais próxima do seu projeto na árvore**. A analogia: numa discussão de família, o **parente mais próximo ganha**. Profundidade na árvore, não número de versão.

Exemplo da própria documentação:

```text
A
├── B
│   └── C
│       └── D 2.0
└── E
    └── D 1.0
```

Aqui **D 1.0 vence**, porque o caminho `A → E → D` (profundidade 2) é mais curto que `A → B → C → D` (profundidade 3). Repare: a versão **mais antiga** ganhou, simplesmente porque está mais perto da raiz. Nearest-wins não liga para qual versão é maior.

E o **efeito-surpresa da ordem**: quando duas versões empatam em profundidade, a doc é explícita — *"if two dependency versions are at the same depth in the dependency tree, the first declaration wins"*. A **ordem em que você declara** as dependências no POM passa a determinar o resultado. Trocar duas linhas de lugar pode mudar a versão resolvida.

Há ainda um caminho de fuga dentro do próprio POM: se você **declarar `D` diretamente** no seu projeto, essa declaração fica à profundidade 1 — mais perto que qualquer transitivo — e portanto vence pela mesma regra do nearest-wins. É o truque mais simples para "subir" uma versão transitiva: trazê-la para perto da raiz declarando-a você mesmo.

Para sobrepor a mediação sem precisar declarar a dependência de fato, Maven oferece `dependencyManagement`, que **tem precedência sobre** o nearest-wins: a versão fixada ali vale para qualquer aparição transitiva daquele artefato, em qualquer profundidade. (Ver [[03-Dominios/Java/Build e tooling/11 - BOM e dependency management|BOM e dependency management]].)

> [!warning] O perigo silencioso do nearest-wins
> Como a profundidade manda, **subir a versão de uma dependência direta pode rebaixar um transitivo sem aviso**. Se você atualiza `service-a` e a nova versão passa a puxar `lib-core` por um caminho mais curto, a versão resolvida muda — e nada no seu código denuncia isso até o runtime. Releia a árvore a cada upgrade.

### Resolution strategy do Gradle (highest-version-wins)

Gradle **não faz nearest-wins**. Por padrão, *"it will select the highest one out of these versions"* — a versão **mais alta** entre todas as pedidas vence, não importa a profundidade na árvore. Se um ramo pede `guava:20.0` e outro pede `guava:25.1`, Gradle escolhe `25.1`, mesmo que `20.0` esteja mais perto da raiz.

Por cima disso, Gradle expõe uma **resolution strategy** explícita para você assumir o controle:

- **`failOnVersionConflict()`** — desliga a resolução automática e faz o build **falhar** ao detectar qualquer conflito, forçando você a resolver manualmente. Útil para times que querem zero versão escolhida "no escuro".
- **`force`** — fixa uma versão e ignora as demais. Martelo: resolve o sintoma, mas não exige que você entenda a causa.
- **Dependency constraints** — declaram a versão preferida sem criar uma dependência direta: *"if any version of `org.apache.commons:commons-lang3` is requested in the dependency graph (either directly or transitively), Gradle will pick version `3.12.0`"*. É a forma idiomática e recomendada.
- **`strictly`** — versão **estrita**: declara que aquela versão (ou faixa) é a única aceitável, e o build **falha** se um transitivo exigir algo incompatível, em vez de silenciosamente subir para a versão mais alta.

Resumo da diferença essencial: **Maven olha a posição na árvore; Gradle olha o número da versão.** O mesmo conflito pode resolver para versões diferentes dependendo da ferramenta.

> [!note] Por que Gradle escolheu highest-wins
> A aposta de design do Gradle é que versões de uma biblioteca tendem a ser **retrocompatíveis** — a mais nova geralmente contém tudo o que a antiga tinha, mais coisas. Logo, subir para a mais alta costuma satisfazer todos os ramos de uma vez. Quando essa premissa falha (a nova versão removeu ou mudou um método), aí entram `strictly` e `failOnVersionConflict()` para te avisar em vez de quebrar em runtime. Maven não faz essa aposta: ele prioriza o que **você** colocou mais perto, deixando a previsibilidade da ordem nas suas mãos.

## Na prática

Uma árvore com conflito. Dois ramos pedem `com.example:lib-core` em versões diferentes:

```text
com.example:app:1.0.0
├── com.example:service-a:2.3.0
│   └── com.example:lib-core:1.4.0
└── com.example:service-b:1.1.0
    └── com.example:internal:0.9.0
        └── com.example:lib-core:1.2.0
```

Resolução do mesmo conflito, lado a lado:

- **Maven (nearest-wins):** `lib-core:1.4.0` vence — está a 2 saltos (`app → service-a → lib-core`), contra 3 saltos no outro ramo.
- **Gradle (highest-version-wins):** `lib-core:1.4.0` também vence aqui, mas por outro motivo (é a versão mais alta). Inverta os números — coloque `1.2.0` no ramo raso e `1.4.0` no profundo — e os dois **divergem**: Maven escolhe `1.2.0` (mais perto), Gradle escolhe `1.4.0` (mais alta).

Inspecionar a árvore real, em cada ferramenta:

```bash
# Maven: árvore completa, ou filtrada por um artefato
mvn dependency:tree
mvn dependency:tree -Dincludes=com.example:lib-core

# Gradle: árvore de uma configuração, ou por que uma versão foi escolhida
./gradlew dependencies --configuration runtimeClasspath
./gradlew dependencyInsight --dependency com.example:lib-core --configuration runtimeClasspath
```

`dependencyInsight` é o que explica **por que** Gradle escolheu aquela versão (quem pediu o quê) — o equivalente a abrir a caixa-preta da resolução.

Forçando a versão certa quando o build escolheu errado.

Maven — excluir o transitivo problemático no ramo que o arrasta:

```xml
<dependency>
  <groupId>com.example</groupId>
  <artifactId>service-b</artifactId>
  <version>1.1.0</version>
  <exclusions>
    <exclusion>
      <groupId>com.example</groupId>
      <artifactId>lib-core</artifactId>
    </exclusion>
  </exclusions>
</dependency>
```

Gradle — `force` (martelo) ou constraint (idiomático):

```kotlin
dependencies {
    // Opção martelo: força e ignora o resto. Resolve o sintoma.
    implementation("com.example:service-b:1.1.0") {
        version { strictly("1.1.0") }
    }

    // Opção idiomática: constraint declara a versão preferida sem criar dependência direta.
    constraints {
        implementation("com.example:lib-core:1.4.0") {
            because("alinha as duas transitivas na versão com o método que app usa")
        }
    }
}

// Endurecer o build: falhar em vez de resolver no escuro.
configurations.all {
    resolutionStrategy {
        failOnVersionConflict()
        force("com.example:lib-core:1.4.0")
    }
}
```

Diagnosticando o sintoma clássico. Quando o build compila mas a JVM lança em runtime:

```text
java.lang.NoSuchMethodError: com.example.LibCore.novoMetodo(...)
java.lang.NoClassDefFoundError: com/example/LibCore$NovaClasse
```

A leitura é quase sempre a mesma: **o conflito foi resolvido para a versão errada**. Seu código (ou um transitivo) foi compilado contra `lib-core:1.4.0`, que tem `novoMetodo`, mas a resolução colocou `lib-core:1.2.0` no classpath, que não tem. Rode `mvn dependency:tree` / `./gradlew dependencyInsight`, ache quem está puxando a versão antiga, e exclua ou fixe.

Roteiro de diagnóstico, em ordem:

1. **Identifique o artefato culpado** — o nome da classe ou método no stack trace (`com.example.LibCore`) aponta a lib.
2. **Liste as versões em jogo** — `mvn dependency:tree -Dincludes=com.example:lib-core` ou `./gradlew dependencyInsight --dependency com.example:lib-core`. Veja quais versões aparecem e qual foi a vencedora.
3. **Ache o ramo que pediu a errada** — `dependencyInsight` mostra a cadeia (quem → quem → lib-core). No Maven, leia a indentação da árvore.
4. **Decida a correção** — se as versões são compatíveis, fixe a boa (constraint / `dependencyManagement`). Se uma é incompatível, exclua o ramo que a arrasta. Se você não sabe, pare e investigue antes de forçar (ver Armadilha 2).
5. **Confirme** — rode a árvore de novo e veja a versão certa vencendo, e o teste de integração passar.

## Armadilhas

### (1) Confiar na resolução implícita

Deixar o build escolher sozinho e nunca olhar a árvore é a armadilha-mãe. A resolução implícita não é "errada" — ela é **invisível**. Funciona até o dia em que um upgrade de uma dependência muda a versão resolvida de um transitivo e o classpath silenciosamente troca de versão. Você só descobre quando o `NoSuchMethodError` aparece. Rode `dependency:tree` / `dependencyInsight` ao adicionar ou subir dependências, e fixe versões críticas via `dependencyManagement` (Maven) ou constraints/BOM (Gradle), em vez de torcer.

### (2) Usar `force` (ou exclusion) sem entender a causa raiz

`force`, `strictly` e `<exclusions>` são bisturis, não curativos. Cravar uma versão à força silencia o conflito, mas se a causa real é que duas libs são genuinamente incompatíveis, você só empurrou o `NoSuchMethodError` para outro ponto — agora a lib que precisava da versão excluída quebra. Antes de forçar, use `dependencyInsight` para entender **por que** as versões divergem e se elas são compatíveis. Force só depois de saber o que está sacrificando, e documente o porquê (no Gradle, `because(...)`).

### (3) Assumir que Maven e Gradle resolvem igual

O erro de raciocínio mais caro do galho. "A versão mais perto / a versão mais nova vai ganhar" depende **inteiramente** de qual ferramenta está embaixo. Maven faz nearest-wins (posição na árvore, com a primeira-declarada como desempate); Gradle faz highest-version-wins (número da versão). Migrar de Maven para Gradle pode **mudar versões resolvidas** sem você tocar em nenhum número de dependência, e introduzir bugs de runtime que não existiam. Sempre confirme qual algoritmo está agindo antes de prever um resultado.

### (4) Tratar o conflito como ruído e silenciá-lo

A tentação de fazer o warning sumir — um `force` global, um `<exclusions>` no primeiro ramo que aparecer — é como desligar o alarme de incêndio em vez de apagar o fogo. O conflito é **informação**: ele diz que duas partes do seu sistema esperam contratos diferentes da mesma lib. Silenciá-lo sem entender significa que uma das duas vai rodar contra uma API que não conhece. Trate cada conflito como um diagnóstico a fazer, não como um aviso a calar — e prefira fixar a versão num único lugar central (BOM, `dependencyManagement`, constraints) a espalhar `force` e exclusões pelo build.

## Em entrevista

### Frase pronta (inglês)

> Transitive resolution means every direct dependency drags its own dependency tree onto your classpath, so version conflicts are inevitable: two transitive paths request the same library in different versions, and the build must pick one. The critical thing to know is that Maven and Gradle resolve this differently — Maven uses nearest-wins, where the version closest to the root of the tree wins and ties are broken by declaration order, while Gradle by default uses highest-version-wins and lets you override it with a resolution strategy like constraints, strict versions, or failOnVersionConflict. When I see a NoSuchMethodError or NoClassDefFoundError at runtime on a build that compiled fine, my first move is to read the dependency tree with mvn dependency:tree or gradle dependencyInsight, find which path pulled the wrong version, and fix the root cause with an exclusion or a constraint rather than blindly forcing a version.

### Vocabulário

| Termo PT | Termo EN |
| --- | --- |
| resolução transitiva | transitive resolution |
| conflito de versão | version conflict |
| a versão mais próxima vence | nearest-wins |
| a versão mais alta vence | highest-version-wins |
| mediação de dependências | dependency mediation |
| estratégia de resolução | resolution strategy |
| árvore de dependências | dependency tree |
| exclusão (de transitivo) | exclusion |
| versão estrita | strict version |
| causa raiz | root cause |

## Veja também

- [[03-Dominios/Java/Build e tooling/03 - Maven — dependências, scopes e exclusions|Maven — dependências e scopes]]
- [[03-Dominios/Java/Build e tooling/06 - Gradle — dependências, Version Catalogs e o wrapper|Gradle — dependências]]
- [[03-Dominios/Java/Build e tooling/11 - BOM e dependency management|BOM e dependency management]]
- [[03-Dominios/Java/Build e tooling/index|Build, tooling e ecossistema (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]

## Referências

- Apache Maven — Introduction to the Dependency Mechanism (dependency mediation / nearest definition, dependencyManagement, exclusions): https://maven.apache.org/guides/introduction/introduction-to-dependency-mechanism.html
- Gradle User Guide — Dependency Resolution: https://docs.gradle.org/current/userguide/dependency_resolution.html
- Gradle User Guide — Handling Version Conflicts / Dependency Constraints (highest-version-wins, constraints): https://docs.gradle.org/current/userguide/dependency_constraints_conflicts.html
