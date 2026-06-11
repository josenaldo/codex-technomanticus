---
title: "Maven vs Gradle — trade-offs honestos"
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
  - maven
  - gradle
aliases:
  - "Maven vs Gradle"
---

# Maven vs Gradle — trade-offs honestos

> [!abstract] TL;DR
> Maven e Gradle resolvem o **mesmo problema** — grafo de dependências, ciclo de vida e empacotamento — e produzem **o mesmo bytecode**. Maven é **declarativo e convencional**: previsível, onboarding rápido, ferramental universal, ao custo de XML verboso e lógica custom dolorida. Gradle é **imperativo e flexível**: build cache e builds incrementais (nota 07), DSL programável, lógica custom fácil, ao custo de mais curva e mais "magia". Não é "melhor vs pior" — é **contexto**. Maven não é legado; Gradle não é sempre melhor.

## O que é

Você já viu os dois modelos nas notas anteriores: o [[03-Dominios/Java/Build e tooling/02 - Maven — POM, coordenadas e lifecycle|POM e o lifecycle do Maven]] e o [[03-Dominios/Java/Build e tooling/05 - Gradle — build script, tasks e configurations|build script, tasks e configurations do Gradle]]. Esta nota não reapresenta nenhum dos dois — ela junta os dois numa **moldura de decisão honesta**.

A pergunta "Maven ou Gradle?" aparece em todo projeto Java novo e em quase toda entrevista de backend. A resposta ruim é dogmática ("Gradle é moderno, Maven é coisa de legado" ou "Maven é padrão, Gradle é firula"). A resposta boa começa reconhecendo um fato incômodo: **os dois fazem a mesma coisa**.

Ambos são ferramentas de build que:

- resolvem um **grafo de dependências** (transitive deps, versões, conflitos);
- orquestram um **ciclo de vida** (compilar → testar → empacotar → publicar);
- produzem o **mesmo artefato** (um `.jar`/`.war` com o mesmo bytecode dentro).

A documentação oficial confirma esse posicionamento sóbrio. O Maven se descreve como "uma ferramenta de build para projetos Java" que, "usando um project object model (POM), gerencia compilação, testes e documentação". O guia de migração do Gradle, por sua vez, vende performance ("2-10x mais rápido que o Maven na maioria dos projetos") e um modelo de build flexível baseado em grafo de tasks — mas o mesmo guia admite curva de aprendizado e custo de reescrever plugins custom.

> [!info] A diferença não está no *o quê*, está no *como*
> Maven e Gradle divergem no **modelo de configuração** (declarativo vs imperativo) e no **ferramental de performance** (incremental + cache), não no resultado final. Essa é a chave da escolha.

## Por que importa

Build é **infraestrutura**: você convive com ela todo dia, em toda máquina de dev e em toda pipeline de CI. A escolha tem consequências reais que não aparecem na primeira semana:

- **Custo de onboarding.** Quanto tempo um dev novo leva para entender o build e fazer uma alteração com segurança?
- **Custo de manutenção.** Quem mexe no build quando ele precisa de lógica custom? Toda a equipe consegue, ou vira propriedade de uma pessoa?
- **Custo de tempo.** Em projeto grande, build lento queima horas de dev e minutos de CI por commit. Cache e incremental viram dinheiro.
- **Custo de risco.** Mais flexibilidade = mais formas de errar. Menos flexibilidade = mais previsibilidade.

Escolher errado não quebra o projeto, mas adiciona atrito permanente. Por isso a decisão merece ser tomada **pelo contexto do projeto**, não pela moda do momento nem pela linha do currículo que você quer engordar.

## Como funciona

### O eixo declarativo vs imperativo

Esse é o eixo central. Tudo o mais decorre dele.

**Maven é declarativo.** Você descreve *o que* o projeto é (suas coordenadas, dependências, plugins) e o Maven aplica um lifecycle fixo e conhecido por cima. "Convention over configuration": se você seguir as convenções (código em `src/main/java`, testes em `src/test/java`), quase nada precisa ser configurado. O POM é dados, não programa — duas pessoas leem o mesmo POM e entendem a mesma coisa.

**Gradle é imperativo (com fachada declarativa).** O build script é **código de verdade** (Kotlin ou Groovy), que monta um grafo de tasks. Você não está limitado a um lifecycle fixo: pode declarar tasks novas, condicionar comportamento, programar lógica. Isso é poder — e poder pede responsabilidade. Um build script pode esconder lógica que não é óbvia ao ler.

O trade-off em uma frase: **Maven te dá previsibilidade por restrição; Gradle te dá poder por liberdade.**

### Performance e ferramental

Aqui o Gradle tem vantagem técnica concreta, já detalhada na nota [[03-Dominios/Java/Build e tooling/07 - Gradle — performance, build cache e daemon|Gradle — performance, build cache e daemon]]:

- **builds incrementais** — só recompila o que mudou;
- **build cache** — reaproveita outputs entre builds (e entre máquinas, com cache remoto);
- **daemon** — processo de longa duração que evita o custo de subir a JVM a cada build.

O guia oficial de migração do Gradle reivindica "2-10x mais rápido que o Maven na maioria dos projetos". É uma afirmação **deles**, e o ganho real depende do projeto: em build pequeno e rápido, a diferença é irrelevante; em monorepo grande, pode ser transformadora.

O Maven, em contrapartida, ganha no **ferramental universal e maduro**: IDEs e servidores de CI tratam o POM como cidadão de primeira classe há mais de uma década, e a previsibilidade do lifecycle facilita ferramentas que inspecionam o build sem executá-lo.

### Ecossistema e curva de aprendizado

**Maven** tem o ecossistema mais maduro e estável de plugins, com comportamento documentado e previsível. A curva é curta: aprender o lifecycle e os scopes resolve a maioria dos casos. O custo aparece quando você precisa de lógica que **não cabe** no modelo declarativo — aí o XML vira ginástica, e você acaba escrevendo (ou caçando) um plugin.

**Gradle** tem uma curva mais longa: você precisa entender as fases (initialization, configuration, execution), a diferença entre `api` e `implementation`, e o modelo de tasks. Em compensação, lógica custom é natural — é só código. O custo é a **"magia"**: convenções implícitas e comportamento que depende de quando o script roda, o que dificulta debugar build quebrado se você não domina o modelo.

> [!tip] Regra prática
> Se a maior parte do seu build é "convenção pura" (compilar, testar, empacotar um jar), o Maven entrega isso com menos cerimônia. Se o build tem **lógica de verdade** (geração de código, múltiplas variantes, integração poliglota), o Gradle paga a curva.

## Na prática

A decisão não é ideológica. É um casamento entre o **perfil do projeto** e o **perfil do time**.

```text
DECISÃO — QUANDO MAVEN, QUANDO GRADLE

┌────────────────────────────┬────────────────────────────────────┐
│ ESCOLHA MAVEN QUANDO...     │ ESCOLHA GRADLE QUANDO...            │
├────────────────────────────┼────────────────────────────────────┤
│ Projeto convencional        │ Build grande/lento que se beneficia │
│ (jar/war padrão, sem        │ de build cache e incremental        │
│ lógica de build exótica)    │                                     │
├────────────────────────────┼────────────────────────────────────┤
│ Time júnior ou rotativo;    │ Monorepo poliglota (vários módulos, │
│ onboarding rápido importa   │ linguagens, builds heterogêneos)    │
├────────────────────────────┼────────────────────────────────────┤
│ Previsibilidade > poder;    │ Lógica de build custom recorrente   │
│ build estável e "chato"     │ (geração de código, variantes)      │
├────────────────────────────┼────────────────────────────────────┤
│ Quer ferramental e CI       │ Android (Gradle é o build oficial)  │
│ universal, sem surpresas    │                                     │
├────────────────────────────┼────────────────────────────────────┤
│ Ninguém no time quer ser    │ Há alguém que domina (e quer manter)│
│ "dono" do build             │ o build como código                 │
└────────────────────────────┴────────────────────────────────────┘

Empate? Fique com a CONVENÇÃO DO ECOSSISTEMA do seu time.
Build não é onde você inova — é onde você quer tédio confiável.
```

Para sentir a diferença de verbosidade, o **mesmo trecho** — declarar uma dependência e fixar a versão do Java — nos dois modelos:

```xml
<!-- pom.xml — Maven (declarativo) -->
<project>
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.exemplo</groupId>
  <artifactId>servico-pedidos</artifactId>
  <version>1.0.0</version>

  <properties>
    <maven.compiler.release>21</maven.compiler.release>
  </properties>

  <dependencies>
    <dependency>
      <groupId>com.exemplo</groupId>
      <artifactId>biblioteca-comum</artifactId>
      <version>2.3.0</version>
    </dependency>
  </dependencies>
</project>
```

```kotlin
// build.gradle.kts — Gradle (DSL programável)
plugins {
    `java`
}

group = "com.exemplo"
version = "1.0.0"

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(21)
    }
}

dependencies {
    implementation("com.exemplo:biblioteca-comum:2.3.0")
}
```

Repare: o Gradle é **mais conciso** no caso simples (a coordenada cabe numa linha). Mas o ponto não é "menos linhas = melhor". O POM é **dados puros** — qualquer ferramenta lê sem executar nada. O `build.gradle.kts` é **código** — mais expressivo, e por isso pode esconder comportamento que só aparece ao rodar. Concisão e previsibilidade são eixos diferentes; cada ferramenta otimiza um.

## Armadilhas

### (1) Escolher por hype ou por currículo (CV-driven development)

A armadilha mais comum: escolher Gradle porque "é moderno" ou porque você quer a linha no currículo, sem que o projeto precise de nada que o Gradle oferece a mais. Ou o oposto — recusar Gradle por preconceito ("é complicado demais") num monorepo que sofre com build lento e que ganharia muito com cache.

Decisão de build é **engenharia, não estética**. Pergunte: *que problema concreto deste projeto esta ferramenta resolve melhor?* Se a resposta honesta é "nenhum, mas eu queria aprender", aprenda em projeto pessoal — não imponha o custo de manutenção à equipe.

### (2) Migrar Maven → Gradle (ou vice-versa) sem ganho real

Migração de build tem custo alto e invisível: reescrever a configuração, reaprender o ferramental, retreinar a equipe, ajustar a CI, caçar diferenças sutis de comportamento. O próprio guia de migração do Gradle avisa que plugins custom do Maven costumam exigir **reescrita**, não tradução literal.

Esse custo só se paga se há um **ganho mensurável** do outro lado: build dramaticamente mais rápido, lógica que o modelo atual não comporta, ou alinhamento com o resto do ecossistema (ex.: adotar Android). "O outro é melhor no geral" **não** é justificativa — lembre que o resultado final é o mesmo bytecode. Migre por um número, não por uma sensação.

## Em entrevista

### Frase pronta (inglês)

> "Maven and Gradle solve the same problem and produce the same bytecode, so I treat the choice as context-driven rather than a question of which tool is 'better'. Maven's declarative, convention-over-configuration model gives me predictability and fast onboarding, which I prefer for conventional projects and rotating teams; Gradle's programmable DSL plus incremental builds and build caching pay off on large or polyglot codebases where build performance and custom logic actually matter. The caveat I always add is that migrating between them carries a real maintenance cost, so I'd only switch when there's a measurable gain — not because one is trendier than the other."

Por que funciona: mostra que você entende **o que é igual** (mesmo bytecode, mesmo problema), apresenta os dois lados com seus custos, ancora a decisão no **contexto**, e fecha com um caveat maduro (migração custa) — sem tomar partido.

### Vocabulário

| Termo PT | Termo EN |
| --- | --- |
| defaults sensatos no lugar de configuração explícita; o pilar do Maven | Convention over configuration |
| você descreve *o quê*; a ferramenta decide *como* (POM do Maven) | Declarative build |
| você escreve *como*, com lógica (build script do Gradle) | Imperative / programmable build |
| só refaz o trabalho cujas entradas mudaram desde o último build | Incremental build |
| reaproveita outputs já calculados, local ou remotamente entre máquinas | Build cache |
| escolher tecnologia pelo currículo, não pela necessidade do projeto | CV-driven development |

## Veja também

- [[03-Dominios/Java/Build e tooling/02 - Maven — POM, coordenadas e lifecycle|Maven — o modelo]]
- [[03-Dominios/Java/Build e tooling/05 - Gradle — build script, tasks e configurations|Gradle — o modelo]]
- [[03-Dominios/Java/Build e tooling/07 - Gradle — performance, build cache e daemon|Gradle — performance]]
- [[03-Dominios/Java/Build e tooling/20 - Capstone — o mesmo projeto em Maven e Gradle|Capstone comparativo]]
- [[03-Dominios/Java/Build e tooling/index|Build, tooling e ecossistema (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]

## Referências

- Apache Maven — site oficial e posicionamento: <https://maven.apache.org/>
- Gradle — Migrating from Maven (User Guide): <https://docs.gradle.org/current/userguide/migrating_from_maven.html>
- Gradle — Build Cache: <https://docs.gradle.org/current/userguide/build_cache.html>
