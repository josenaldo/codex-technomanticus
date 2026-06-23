---
title: "Toolchains — buildar com um JDK, mirar outro"
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
  - toolchains
  - jdk
aliases:
  - "toolchains"
---

# Toolchains — buildar com um JDK, mirar outro

> [!abstract] TL;DR
> O JDK que **roda** o seu build (Maven ou Gradle) não precisa ser o mesmo que você quer **mirar** ao compilar. *Toolchains* desacoplam os dois: você pode rodar o build num JDK 21 moderno e ainda compilar bytecode compatível com Java 17 (ou 11, ou 8) usando um JDK específico instalado na máquina. No Maven isso é o `maven-toolchains-plugin` + `~/.m2/toolchains.xml`; no Gradle é o bloco `java { toolchain { ... } }` com auto-detecção e auto-provisionamento. Em ambos, o flag `release` é quem garante que você não usou API mais nova que o alvo.

## O que é

Uma **toolchain** é uma declaração de "qual JDK usar para uma tarefa específica do build" (compilar, rodar testes, gerar javadoc) — separada de "qual JDK está executando a ferramenta de build agora".

Sem toolchains, o JDK ativo (o que está no `PATH` / `JAVA_HOME`) faz tudo: ele roda o Maven/Gradle **e** compila o seu código. Isso amarra a versão do seu artefato à versão do JDK da máquina, o que é frágil — em CI, na máquina do colega, no seu laptop, o JDK ativo varia.

Toolchains quebram esse acoplamento. Você diz "compile mirando o JDK X" de forma declarativa, e a ferramenta de build localiza o JDK X (já instalado ou baixando) sem depender de qual JDK iniciou o processo. A noção de *qual versão de bytecode* sai do alvo é assunto do Galho 3 — veja [[03-Dominios/Tecnologia/Java/JVM/01 - A JVM — o que é e o pipeline de execução|A JVM (Galho 3)]]; aqui o foco é a **mecânica de build** que seleciona o JDK.

## Por que importa

- **Reprodutibilidade**: o artefato compilado não muda só porque o JDK ativo da máquina mudou. A versão-alvo está cravada no `pom.xml` / `build.gradle.kts`, não no ambiente.
- **Migração gradual**: você adota recursos novos da ferramenta de build e do JDK que roda o build (mais rápido, mais seguro) sem ser obrigado a subir a versão-alvo dos seus consumidores.
- **Suporte a múltiplos alvos**: bibliotecas que precisam rodar em Java 8 *e* Java 21 podem compilar módulos diferentes mirando JDKs diferentes na mesma build.
- **CI honesto**: o pipeline declara explicitamente o JDK-alvo, em vez de "funciona porque a imagem do runner por acaso tem o JDK certo".

## Como funciona

### O problema: JDK que roda o build vs. JDK-alvo

Há dois JDKs em jogo, e confundi-los é a fonte de quase todo bug nesta área:

1. **O JDK que roda o build** — a JVM que iniciou o processo do Maven ou do Gradle. Pode ser o mais novo que você tiver; ele só precisa ser velho o bastante para a ferramenta funcionar.
2. **O JDK-alvo (toolchain)** — o JDK usado para *compilar* o seu código e, idealmente, *rodar os testes*. É a versão para a qual o bytecode é gerado e contra cujas APIs você compila.

O perigo: se você compilar com um JDK novo mas pedir bytecode antigo via `source`/`target`, o compilador rebaixa a *versão do classfile*, mas ainda enxerga a **biblioteca padrão do JDK novo**. Você pode chamar um método que só existe no JDK 21 e mesmo assim gerar um classfile "Java 17" — que vai estourar `NoSuchMethodError` em runtime no alvo real.

A solução de duas pontas:

- **Toolchain** para garantir que a *compilação roda no JDK certo* (com a stdlib certa).
- **`release N`** (`--release` do `javac`, exposto como `<release>` no Maven e `release.set(N)` no Gradle) para garantir, mesmo num JDK novo, que só a **API documentada da versão N** fica visível. O `release` valida contra os símbolos da versão-alvo; `source`/`target` não fazem essa validação de API.

A combinação ideal: toolchain mirando o JDK-alvo **e** `release` na versão-alvo — cinto e suspensório.

### Maven toolchains

No Maven, a engrenagem tem três peças:

1. **`~/.m2/toolchains.xml`** — um catálogo, por máquina, dos JDKs disponíveis. Cada `<toolchain>` tem `<type>jdk</type>`, um bloco `<provides>` (com `<version>` e `<vendor>`) e a `<configuration>` apontando o `<jdkHome>`. É aqui que mora o mapeamento "versão lógica → caminho no disco".
2. **`maven-toolchains-plugin`** no `pom.xml` — declara, via `<toolchains><jdk>`, qual versão/vendor o projeto exige. No goal `toolchain`, o plugin casa o requisito contra o `toolchains.xml` e seleciona o JDK.
3. **Plugins toolchain-aware** — uma vez selecionado, o `maven-compiler-plugin`, o `maven-surefire-plugin` etc. passam a usar aquele JDK em vez do que roda o Maven.

O Maven **não baixa JDK**: o `toolchains.xml` só referencia JDKs já instalados. Se nenhum casar com o requisito, o build falha.

### Gradle toolchains

No Gradle (Kotlin DSL) a declaração é mais enxuta e fica num único bloco:

```kotlin
java { toolchain { languageVersion = JavaLanguageVersion.of(21) } }
```

A partir daí, `compileJava`, `test`, `javadoc` etc. herdam essa toolchain. Diferenças em relação ao Maven:

- **Auto-detecção**: o Gradle descobre JDKs instalados em locais convencionais e via gerenciadores (SDKMAN!, Asdf, Jabba) e variáveis de ambiente. Dá pra desligar com `org.gradle.java.installations.auto-detect=false`.
- **Auto-provisionamento**: se nenhum JDK local casar, o Gradle pode **baixar** um — mas só se você tiver um *toolchain resolver*. O convencional é o plugin Foojay no `settings.gradle.kts` (`org.gradle.toolchains.foojay-resolver-convention`).
- **Vendor e implementação**: dá pra refinar com `vendor = JvmVendorSpec.ADOPTIUM`, `implementation = JvmImplementation.J9`, ou `nativeImageCapable = true`.
- **Override por tarefa**: via o serviço `javaToolchains`, você compila numa versão e roda testes em outra na mesma build.

> [!note] JPMS e módulos
> Quando o projeto usa o sistema de módulos, a versão-alvo também influencia o que o `module-info` enxerga; veja [[03-Dominios/Tecnologia/Java/JVM/08 - JPMS — o sistema de módulos|JPMS (Galho 3)]] para o lado da linguagem/runtime. Toolchain só decide *qual JDK* compila — não muda as regras de módulos.

## Na prática

**Maven** — catálogo de JDKs em `~/.m2/toolchains.xml` e o `pom.xml` exigindo o alvo com `release`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!-- ~/.m2/toolchains.xml: JDKs disponíveis NESTA máquina -->
<toolchains>
  <toolchain>
    <type>jdk</type>
    <provides>
      <version>17</version>
      <vendor>temurin</vendor>
    </provides>
    <configuration>
      <jdkHome>/opt/jdks/temurin-17</jdkHome>
    </configuration>
  </toolchain>
  <toolchain>
    <type>jdk</type>
    <provides>
      <version>21</version>
      <vendor>temurin</vendor>
    </provides>
    <configuration>
      <jdkHome>/opt/jdks/temurin-21</jdkHome>
    </configuration>
  </toolchain>
</toolchains>
```

```xml
<!-- pom.xml: exige o JDK 17 e compila MIRANDO a API do 17 -->
<build>
  <plugins>
    <plugin>
      <groupId>org.apache.maven.plugins</groupId>
      <artifactId>maven-toolchains-plugin</artifactId>
      <version>3.2.0</version>
      <executions>
        <execution>
          <goals>
            <goal>toolchain</goal>
          </goals>
        </execution>
      </executions>
      <configuration>
        <toolchains>
          <jdk>
            <version>17</version>
            <vendor>temurin</vendor>
          </jdk>
        </toolchains>
      </configuration>
    </plugin>
    <plugin>
      <groupId>org.apache.maven.plugins</groupId>
      <artifactId>maven-compiler-plugin</artifactId>
      <version>3.13.0</version>
      <configuration>
        <!-- release valida que SÓ a API do Java 17 está visível -->
        <release>17</release>
      </configuration>
    </plugin>
  </plugins>
</build>
```

**Gradle** (Kotlin DSL) — o resolver Foojay no `settings.gradle.kts` e a toolchain no `build.gradle.kts`:

```kotlin
// settings.gradle.kts — habilita auto-provisionamento (download)
plugins {
    id("org.gradle.toolchains.foojay-resolver-convention") version "1.0.0"
}
```

```kotlin
// build.gradle.kts — toolchain mira o JDK 21; release crava a API-alvo
plugins {
    java
}

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(21)
        vendor = JvmVendorSpec.ADOPTIUM
    }
}

tasks.withType<JavaCompile>().configureEach {
    // equivalente ao --release: não vaza API mais nova que o alvo
    options.release = 21
}
```

## Armadilhas

### (1) Buildar com o JDK errado sem notar

O sintoma clássico: o build "passa" na sua máquina e quebra no CI (ou vice-versa), porque o JDK ativo era outro. Sem toolchain declarada, o artefato fica refém de qual `JAVA_HOME`/`PATH` estava ativo. **Mitigação**: declare a toolchain explicitamente (Maven `toolchains.xml` + plugin; Gradle bloco `java { toolchain }`) para que a versão de compilação não dependa do ambiente. No Gradle, rode com `--info` para confirmar qual JDK a toolchain selecionou.

### (2) Usar `source`/`target` em vez de `release` (vaza API mais nova que o alvo)

`source`/`target` só rebaixam a *versão do classfile* — o compilador continua enxergando a biblioteca padrão do JDK que está compilando. Você consegue chamar um método que só existe no JDK novo e ainda gerar um classfile "antigo", que então estoura `NoSuchMethodError`/`NoSuchFieldError` no runtime-alvo. **Mitigação**: use `release N` (Maven `<release>`, Gradle `options.release`), que valida contra os símbolos *documentados* da versão N e barra o uso de API mais nova em tempo de compilação.

### (3) Assumir que o toolchain baixa/acha qualquer JDK automaticamente

No **Maven**, toolchain **nunca baixa nada**: o `toolchains.xml` só aponta JDKs já instalados; se nenhum casar com `<version>`/`<vendor>`, o build falha. No **Gradle**, auto-provisionamento **só funciona se houver um resolver** configurado (ex.: Foojay no `settings.gradle.kts`) — sem ele, o Gradle só usa o que a auto-detecção achar localmente, e falha se nada casar. **Mitigação**: no Maven, garanta que cada JDK-alvo está no catálogo; no Gradle, adicione o resolver se quiser download automático, e lembre que isso exige rede no ambiente de build.

## Em entrevista

### Frase pronta (inglês)

"Toolchains decouple the JDK that *runs* the build from the JDK I'm *targeting*. In Maven I register the available JDKs in `~/.m2/toolchains.xml` and select one with the `maven-toolchains-plugin`, while in Gradle I just declare `java { toolchain { languageVersion = JavaLanguageVersion.of(21) } }` and let auto-detection — or Foojay-based auto-provisioning — find or download it. Crucially, I pair the toolchain with the `--release` flag instead of the old `source`/`target` pair: `release` validates that I'm not using any API newer than the target version, so I can't accidentally ship a class file that throws `NoSuchMethodError` at runtime on an older JDK."

### Vocabulário

| Termo PT | Termo EN |
| --- | --- |
| JDK que roda o build | build-time JDK / runtime that runs the build |
| JDK-alvo | target JDK |
| flag de versão-alvo | release flag (`--release`) |
| auto-detecção (de JDKs) | toolchain auto-detection |
| auto-provisionamento (download) | toolchain auto-provisioning |
| fornecedor / distribuição | vendor / distribution |
| catálogo de JDKs (Maven) | toolchains registry (`toolchains.xml`) |
| versão do classfile | class file version |

## Veja também

- [[03-Dominios/Tecnologia/Java/Build e tooling/09 - Distribuições do JDK e o ecossistema|Distribuições do JDK]]
- [[03-Dominios/Tecnologia/Java/JVM/01 - A JVM — o que é e o pipeline de execução|A JVM (Galho 3)]]
- [[03-Dominios/Tecnologia/Java/JVM/08 - JPMS — o sistema de módulos|JPMS (Galho 3)]]
- [[03-Dominios/Tecnologia/Java/Build e tooling/index|Build, tooling e ecossistema (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]

## Referências

- Apache Maven — *Guide to Using Toolchains*. https://maven.apache.org/guides/mini/guide-using-toolchains.html
- Gradle — *Toolchains for JVM projects*. https://docs.gradle.org/current/userguide/toolchains.html
- Foojay Toolchains Resolver (Gradle plugin). https://github.com/gradle/foojay-toolchains
