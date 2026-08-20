---
title: "Fitness functions — ArchUnit (testes de arquitetura)"
created: 2026-06-11
updated: 2026-06-11
type: concept
progress: backlog
status: seedling
publish: true
fase: magus
tags:
  - java
  - testes
  - magus
  - archunit
aliases:
  - "ArchUnit"
  - "fitness functions"
  - "testes de arquitetura"
---

# Fitness functions — ArchUnit (testes de arquitetura)

> [!abstract] TL;DR
> ArchUnit expressa regras de arquitetura como testes JUnit que falham o build quando alguém viola uma camada, introduz um ciclo ou foge de uma convenção; são **fitness functions** — um guardrail automático contra o *drift* arquitetural. Em vez de confiar em revisão humana ou num diagrama de wiki que ninguém lê, você codifica a regra ("controller não chama repository direto") e o CI a defende a cada commit.

## O que é

ArchUnit é uma biblioteca Java que analisa o **bytecode** das suas classes e permite afirmar propriedades estruturais sobre o código como testes comuns. Você escreve uma `ArchRule` numa DSL fluente, aponta para os pacotes que quer inspecionar, e a regra ou passa ou estoura uma `AssertionError` com a lista de violações.

O conceito por trás disso é o de **fitness function**, emprestado de *Building Evolutionary Architectures*: uma função objetiva, automatizada e executável que mede o quão perto a arquitetura está das características que você decidiu preservar. Uma fitness function não desenha a arquitetura — ela a *protege*. ArchUnit é a encarnação mais comum dessa ideia no ecossistema Java.

Diferente de um *linter* de estilo, ArchUnit opera no nível de **dependências entre tipos e pacotes**: quem importa quem, qual classe está em qual camada, se há ciclos, se uma convenção de nome ou anotação foi respeitada.

## Por que importa

Toda arquitetura tende a apodrecer. O diagrama de camadas que o time desenhou no kickoff sobrevive umas semanas; depois alguém, sob prazo, injeta um `JdbcTemplate` direto no controller "só dessa vez", e a fronteira começa a vazar. Esse vazamento é silencioso — compila, passa nos testes funcionais, e ninguém nota até a base estar acoplada demais para refatorar.

Fitness functions transformam decisões arquiteturais em **código executável e versionado**. A regra deixa de ser folclore oral ("a gente não chama repository do controller") e vira um teste que falha o build de quem violar. Isso muda o custo do erro: o atalho é barrado no `mvn test` / `gradle test`, não três meses depois numa auditoria.

Para um nível sênior, o valor não é "rodar ArchUnit"; é **escolher quais invariantes merecem virar guardrail** e mantê-las legíveis o suficiente para que a falha eduque em vez de irritar. Uma boa suíte de ArchUnit é documentação viva da arquitetura.

## Como funciona

### Fitness function: regra de arquitetura como teste que falha o build

A unidade básica é a `ArchRule`. Você declara uma classe de teste anotada com `@AnalyzeClasses`, apontando os pacotes a inspecionar, e expõe regras como campos `static final ArchRule` anotados com `@ArchTest`. O runner do JUnit avalia cada campo contra o conjunto de classes importadas.

```java
@AnalyzeClasses(packages = "com.example.app")
class ArchitectureTest {

    @ArchTest
    static final ArchRule controllers_should_be_annotated =
        classes().that().resideInAPackage("..controller..")
            .should().beAnnotatedWith(RestController.class);
}
```

Por trabalhar no bytecode, a importação é barata e independe de rodar a aplicação. O resultado é binário: a regra passa, ou estoura com uma mensagem listando cada classe que a violou.

### Dependências entre camadas (noClasses / layeredArchitecture)

Há dois jeitos de defender camadas. O primeiro é uma proibição pontual com `noClasses()`:

```java
@ArchTest
static final ArchRule controllers_must_not_touch_repositories =
    noClasses().that().resideInAPackage("..controller..")
        .should().dependOnClassesThat().resideInAPackage("..repository..");
```

O segundo descreve a arquitetura inteira de uma vez com `layeredArchitecture()`. Você nomeia as camadas, diz que pacotes as definem, e declara quem pode acessar quem. O `consideringAllDependencies()` garante que campos, parâmetros, retornos e anotações entrem na análise, não só chamadas de método:

```java
@ArchTest
static final ArchRule layers_respected =
    layeredArchitecture().consideringAllDependencies()
        .layer("Controller").definedBy("..controller..")
        .layer("Service").definedBy("..service..")
        .layer("Repository").definedBy("..repository..")
        .whereLayer("Controller").mayNotBeAccessedByAnyLayer()
        .whereLayer("Service").mayOnlyBeAccessedByLayers("Controller")
        .whereLayer("Repository").mayOnlyBeAccessedByLayers("Service");
```

A regra de camadas é mais expressiva — uma única `ArchRule` cobre o grafo inteiro de permissões e a mensagem de falha aponta exatamente qual acesso indevido ocorreu.

### Sem ciclos entre pacotes (slices().beFreeOfCycles())

Ciclos de dependência entre módulos são veneno: impedem testar, evoluir ou extrair um pacote isoladamente. ArchUnit detecta isso com `slices()`, que fatia o código por um padrão de pacote e verifica se as fatias formam um grafo acíclico:

```java
@ArchTest
static final ArchRule no_cycles =
    slices().matching("com.example.app.(*)..")
        .should().beFreeOfCycles();
```

O `(*)` captura o primeiro segmento abaixo de `com.example.app` como nome da fatia (ex.: `order`, `billing`, `user`). Se `order` depende de `billing` e `billing` depende de volta de `order`, a regra falha e descreve o ciclo. É um dos testes de maior retorno por linha escrita.

### Convenções: nome de classe, anotação obrigatória

Além de dependências, ArchUnit defende **convenções estruturais**. Classes num pacote devem terminar com certo sufixo, residir em certo lugar, ou carregar certa anotação:

```java
@ArchTest
static final ArchRule services_naming =
    classes().that().resideInAPackage("..service..")
        .should().haveSimpleNameEndingWith("Service")
        .andShould().beAnnotatedWith(Service.class);
```

Convenções como essas mantêm o código previsível: qualquer dev sabe que `..service..` contém classes `*Service` anotadas com `@Service`, e o build garante que ninguém escapou disso.

## Na prática

Uma suíte enxuta que junta as quatro famílias de regra. Pacotes neutros, sem framework específico além das anotações ilustrativas:

```java
import com.tngtech.archunit.junit.AnalyzeClasses;
import com.tngtech.archunit.junit.ArchTest;
import com.tngtech.archunit.lang.ArchRule;

import static com.tngtech.archunit.lang.syntax.ArchRuleDefinition.classes;
import static com.tngtech.archunit.lang.syntax.ArchRuleDefinition.noClasses;
import static com.tngtech.archunit.library.Architectures.layeredArchitecture;
import static com.tngtech.archunit.library.dependencies.SlicesRuleDefinition.slices;

@AnalyzeClasses(packages = "com.example.app")
class ArchitectureTest {

    // 1. Camadas como contrato declarativo
    @ArchTest
    static final ArchRule layered = layeredArchitecture()
            .consideringAllDependencies()
            .layer("Controller").definedBy("..controller..")
            .layer("Service").definedBy("..service..")
            .layer("Repository").definedBy("..repository..")
            .whereLayer("Controller").mayNotBeAccessedByAnyLayer()
            .whereLayer("Service").mayOnlyBeAccessedByLayers("Controller")
            .whereLayer("Repository").mayOnlyBeAccessedByLayers("Service")
            .because("a camada de apresentacao nunca deve falar direto com persistencia");

    // 2. Proibição pontual e explícita (reforça a regra de camadas)
    @ArchTest
    static final ArchRule controllers_keep_off_repositories =
            noClasses().that().resideInAPackage("..controller..")
                    .should().dependOnClassesThat().resideInAPackage("..repository..")
                    .because("controllers devem delegar a services, nao acessar dados direto");

    // 3. Sem ciclos entre os módulos de topo
    @ArchTest
    static final ArchRule no_cycles =
            slices().matching("com.example.app.(*)..")
                    .should().beFreeOfCycles();

    // 4. Convenção: services bem nomeados e anotados
    @ArchTest
    static final ArchRule services_well_formed =
            classes().that().resideInAPackage("..service..")
                    .should().haveSimpleNameEndingWith("Service")
                    .because("nomeacao consistente torna a camada de servico descobrivel");
}
```

Quando alguém abre um *pull request* que viola qualquer uma delas, o build do CI fica vermelho com uma mensagem do tipo *"Class com.example.app.web.OrderController depends on com.example.app.data.OrderRepository"* — antes do merge, não depois.

## Armadilhas

### (1) Regra acoplada a nome de pacote literal frágil

Amarrar a regra a um caminho literal completo a torna refém da estrutura de pastas. Um simples renomear de pacote, sem nenhuma mudança arquitetural real, quebra a regra e gera ruído.

```java
// Frágil: qualquer reorganização de pacotes derruba isso sem motivo arquitetural
noClasses().that().resideInAPackage("com.example.app.web.controller")
    .should().dependOnClassesThat().resideInAPackage("com.example.app.persistence.jpa.repository");
```

**Fix:** use *wildcards* `..` que casam por convenção, não por caminho exato. `..controller..` casa qualquer pacote que contenha `controller` em algum nível, sobrevivendo a reorganizações que não mudam o papel das classes:

```java
noClasses().that().resideInAPackage("..controller..")
    .should().dependOnClassesThat().resideInAPackage("..repository..");
```

### (2) ArchUnit escrito mas que não roda no CI

A pior armadilha: a suíte existe, está bonita no repositório, mas mora fora do conjunto de testes que o build executa — num `sourceSet` ignorado, num perfil Maven desligado, ou marcada com um `@Disabled` esquecido. Vira decoração. As regras envelhecem, as violações se acumulam, e quando alguém finalmente roda há centenas de erros impossíveis de triar.

**Fix:** garanta que `ArchitectureTest` esteja na mesma suíte que `mvn test` / `gradle test` roda por padrão, e que o pipeline de CI falhe o build em violação. Trate a fitness function como teste de primeira classe — se ela não pode reprovar um PR, ela não existe.

### (3) Regra críptica sem mensagem clara

Quando uma regra falha sem contexto, o dev que tropeçou nela não entende *por quê* a arquitetura proíbe aquilo — só vê uma barreira arbitrária e fica tentado a apagar o teste.

```java
// Quando falha, a mensagem é genérica e não educa
noClasses().that().resideInAPackage("..service..")
    .should().dependOnClassesThat().resideInAPackage("..controller..");
```

**Fix:** anexe `.because(...)` explicando a intenção. A frase vira parte da mensagem de erro e transforma a falha num momento de aprendizado em vez de irritação:

```java
noClasses().that().resideInAPackage("..service..")
    .should().dependOnClassesThat().resideInAPackage("..controller..")
    .because("a camada de servico nao deve conhecer a de apresentacao — inverte a dependencia");
```

## Em entrevista

### Frase pronta (inglês)

> I treat architecture rules as fitness functions: ArchUnit lets me encode invariants — like "controllers may not depend on repositories" or "no package cycles" — as JUnit tests that analyze the bytecode and fail the build when someone drifts. The point isn't running the tool; it's choosing which invariants are worth a guardrail and keeping the failure messages clear with `.because(...)`, so a broken rule teaches instead of annoying. I always make sure these tests run in the default CI suite, otherwise they're just decoration that rots silently.

### Vocabulário

| Termo (EN) | Significado |
|---|---|
| fitness function | função automatizada que mede e protege uma característica arquitetural |
| architectural drift | erosão silenciosa da arquitetura ao longo do tempo |
| guardrail | barreira automática que impede uma violação antes do merge |
| layered architecture | arquitetura em camadas com regras de quem pode acessar quem |
| package cycle | dependência circular entre pacotes/módulos |
| slice | fatia de código agrupada por um padrão de pacote |
| bytecode analysis | inspeção das classes compiladas, sem rodar a aplicação |
| invariant | propriedade que deve permanecer verdadeira em todo o código |

## Veja também

- [[03-Dominios/Tecnologia/Java/Testes/20 - Contract testing — Pact|Contract testing — Pact]]
- [[03-Dominios/Tecnologia/Java/Testes/21 - Capstone — a estratégia de testes de uma app Spring production-grade|Capstone de testes]]
- [[03-Dominios/Tecnologia/Java/Spring Core e Boot/06 - ApplicationContext — o container e seu ciclo|ApplicationContext]]
- [[03-Dominios/Tecnologia/Java/Testes/index|Testes (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java]]

## Referências

- ArchUnit User Guide — https://www.archunit.org/userguide/html/000_Index.html
