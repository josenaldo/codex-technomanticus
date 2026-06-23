---
title: "Native Image com Spring — Spring AOT na prática"
created: 2026-06-12
updated: 2026-06-12
type: concept
status: seedling
publish: true
fase: adepto
tags:
  - java
  - cloud-native
  - adepto
  - native-image
  - graalvm
aliases:
  - "Spring AOT"
  - "native-build-tools"
---

# Native Image com Spring — Spring AOT na prática

> [!abstract] TL;DR
> Native image fecha o mundo em build-time, mas o Spring é todo dinâmico em runtime (beans criados por reflection, proxies CGLIB, condicionais por property). O **Spring AOT** (desde Spring Boot 3.0, nov/2022) resolve a tensão: em build-time ele transforma a configuração dinâmica em **artefatos estáticos** — `*__BeanDefinitions` em Java, hints JSON sob `META-INF/native-image/` (reflect/resource/proxy-config) e proxies pré-compilados. Quando o AOT não consegue inferir um uso de reflection, você registra à mão com `RuntimeHintsRegistrar` ou `@RegisterReflectionForBinding`. Pra compilar há dois caminhos: **native-build-tools** (`native:compile`/`nativeCompile`, exige GraalVM local) ou **Buildpacks** com `BP_NATIVE_IMAGE=true` (GraalVM mora no container). Condicionais avaliadas em runtime, como `@ConditionalOnProperty`, **não funcionam** — o classpath e as decisões ficam congelados no build.

## O que é

O **Spring AOT** (*Ahead-of-Time processing*) é um motor que roda durante o build e converte a configuração dinâmica do Spring em código e metadados estáticos que o GraalVM consegue analisar. É o que torna uma aplicação Spring Boot compilável para [[03-Dominios/Tecnologia/Java/Cloud-native e produção/08 - GraalVM Native Image — conceito e trade-offs|native image]] sem que você precise escrever metadados de reflection na unha pra cada bean.

Pensa assim: o GraalVM exige um *mundo fechado* — tudo o que será usado precisa ser conhecido em build-time. Mas o Spring, por design, monta o `ApplicationContext` em runtime, descobrindo beans por scan, criando proxies sob demanda e decidindo o que instanciar a partir de properties. Esses dois mundos são incompatíveis por natureza. O Spring AOT é o **tradutor**: ele "roda" a montagem do contexto antecipadamente e materializa o resultado em arquivos estáticos.

Está disponível desde o **Spring Boot 3.0** e é a peça que faltava pra que o ecossistema Spring suportasse native image como cidadão de primeira classe (antes disso, era território do projeto experimental Spring Native).

## Por que importa

Sem o Spring AOT, compilar Spring para native image seria praticamente inviável: você teria que mapear manualmente cada classe acessada por reflection, cada recurso carregado, cada proxy dinâmico. Numa aplicação real com dezenas de starters, isso são milhares de entradas.

O AOT automatiza 90% desse trabalho. Ele te dá os benefícios do native image — startup em milissegundos, footprint de memória menor, ideal para serverless e escala horizontal agressiva — sem te obrigar a virar especialista nos internals do GraalVM. Pro time, isso significa que migrar um serviço pra native vira uma questão de configurar o build e tratar as poucas exceções que o AOT não cobre, em vez de um projeto de pesquisa.

E importa saber **onde estão os limites**: o que o AOT cobre sozinho, o que exige hint manual, e quais padrões Spring (como `@ConditionalOnProperty`) simplesmente deixam de funcionar. Numa entrevista de plataforma ou numa decisão de arquitetura, é essa fronteira que separa quem leu o título de quem realmente operou native em produção.

## Como funciona

### O Spring AOT engine em build-time

Quando o build AOT roda (`process-aot`), o Spring constrói o `ApplicationContext` em modo de análise e emite três famílias de artefato:

1. **`*__BeanDefinitions` em código Java.** Cada `@Configuration` vira uma classe gerada com a definição explícita dos beans. Um `MyConfiguration` com um `@Bean myBean()` vira:

   ```java
   public class MyConfiguration__BeanDefinitions {
       public static BeanDefinition getMyBeanBeanDefinition() {
           RootBeanDefinition beanDefinition = new RootBeanDefinition(MyBean.class);
           beanDefinition.setInstanceSupplier(getMyBeanInstanceSupplier());
           return beanDefinition;
       }
   }
   ```

   Não há mais scan nem `@Bean` interpretado em runtime: a fábrica de beans já vem pronta. (Maven: `target/spring-aot/main/sources`.)

2. **Hints / reachability metadata** — arquivos JSON sob `META-INF/native-image/{groupId}/{artifactId}/` que o GraalVM lê automaticamente: `reflect-config.json` (classes/métodos via reflection), `resource-config.json` (recursos a embarcar), `proxy-config.json` (interfaces de proxy dinâmico), além de `serialization-config.json` e `jni-config.json`.

3. **Proxies CGLIB pré-compilados.** Os proxies que o Spring normalmente geraria em runtime (bytecode na hora) são gerados como `.class` já no build (`target/spring-aot/main/classes`), porque native image não permite geração dinâmica de bytecode.

O resultado: o GraalVM enxerga um Spring "achatado", todo estático, e consegue fazer a análise de alcançabilidade dele.

### Hints, `RuntimeHintsRegistrar` e `@RegisterReflectionForBinding`

O AOT infere muita coisa, mas **não tudo**. Se o seu código (ou uma lib) acessa uma classe por reflection de um jeito que o AOT não consegue rastrear — por exemplo, carregando um nome de classe vindo de string —, o GraalVM removerá essa classe como "inalcançável" e você toma um `ClassNotFoundException` em runtime. A solução é registrar o hint **explicitamente**.

Há duas portas de entrada:

- **`RuntimeHintsRegistrar`**: uma interface com o método `registerHints(RuntimeHints hints, ClassLoader classLoader)` onde você declara, programaticamente, o que precisa de reflection, recurso ou proxy. Registra-se via `@ImportRuntimeHints`. É a forma de baixo nível e mais poderosa.
- **`@RegisterReflectionForBinding`**: um atalho declarativo. Você anota apontando para uma classe (tipicamente um DTO usado em (de)serialização) e o Spring registra todos os membros necessários pra binding por reflection. Ideal para o caso comum de "esse POJO é lido/escrito por uma lib via reflection".

A regra mental: **o AOT é otimista sobre o que consegue ver; você cobre o que ele não vê.**

### Os dois caminhos de build

Materializar o native image em si tem dois caminhos, e a escolha depende de onde o GraalVM vive:

- **native-build-tools** (`org.graalvm.buildtools`, versão **1.1.2**): plugins oficiais do GraalVM para Maven e Gradle. No Maven, o goal é `native:compile`; no Gradle, a task é `nativeCompile`. Esse caminho **exige uma distribuição GraalVM instalada localmente** (na máquina de dev ou no runner de CI) — é a ferramenta que de fato invoca o `native-image`.
- **Buildpacks** com `BP_NATIVE_IMAGE=true`: o build acontece dentro de um container que **já traz o GraalVM embutido**. Você não instala nada localmente; basta `./mvnw spring-boot:build-image` com a variável setada. Esse caminho está detalhado na nota de [[03-Dominios/Tecnologia/Java/Cloud-native e produção/06 - Buildpacks — imagem sem Dockerfile|Buildpacks]].

Em ambos os caminhos, o Spring AOT roda **antes** da compilação nativa — ele é pré-requisito comum, não alternativa.

## Na prática

Um `RuntimeHintsRegistrar` registrando reflection e recurso que o AOT não pegou sozinho:

```java
import org.springframework.aot.hint.RuntimeHints;
import org.springframework.aot.hint.RuntimeHintsRegistrar;
import org.springframework.aot.hint.MemberCategory;
import org.springframework.context.annotation.ImportRuntimeHints;

@ImportRuntimeHints(CatalogRuntimeHints.class)
public class CatalogConfig {

    static class CatalogRuntimeHints implements RuntimeHintsRegistrar {
        @Override
        public void registerHints(RuntimeHints hints, ClassLoader classLoader) {
            // Classe acessada por reflection numa lib sem metadata própria
            hints.reflection().registerType(LegacyParser.class,
                MemberCategory.INVOKE_PUBLIC_CONSTRUCTORS,
                MemberCategory.INVOKE_PUBLIC_METHODS);

            // Recurso lido em runtime via classpath
            hints.resources().registerPattern("templates/*.mustache");
        }
    }
}
```

O atalho declarativo para um DTO de binding:

```java
import org.springframework.aot.hint.annotation.RegisterReflectionForBinding;

@RegisterReflectionForBinding(InvoicePayload.class)
public class InvoiceModule { }
```

Compilando com native-build-tools (exige GraalVM local). O perfil `native` é ativado pelo `spring-boot-starter-parent`:

```bash
# Gera o executável nativo em target/
./mvnw -Pnative native:compile
```

O plugin no `pom.xml` (gerenciado pelo parent; aqui explícito pra deixar o goal visível):

```xml
<plugin>
    <groupId>org.graalvm.buildtools</groupId>
    <artifactId>native-maven-plugin</artifactId>
    <version>1.1.2</version>
    <executions>
        <execution>
            <id>build-native</id>
            <goals>
                <goal>compile-no-fork</goal>
            </goals>
            <phase>package</phase>
        </execution>
    </executions>
</plugin>
```

## Armadilhas

### (1) Reflection numa lib sem metadata → precisa de hint manual

O AOT cobre o seu código e as libs do ecossistema Spring, mas uma dependência transitiva qualquer que faz reflection "criativa" pode não trazer metadados. O sintoma clássico: tudo compila, o build nativo passa, e em runtime você toma `ClassNotFoundException` ou `NoSuchMethodException` numa classe que existe no jar mas foi podada como inalcançável. A correção é registrar o hint via `RuntimeHintsRegistrar`. Dica de diagnóstico: o Maven `native:list-libraries-missing-metadata` (ou o `listLibrariesMissingMetadata` no Gradle) lista exatamente as dependências sem metadata.

### (2) `@ConditionalOnProperty` que não funciona em native

Esta é a pegadinha que mais surpreende quem vem do mundo JVM. No native image, **o classpath e as decisões de criação de bean são congelados em build-time**. A documentação é explícita: *"Properties that change if a bean is created are not supported (for example, `@ConditionalOnProperty`)"*. Se você liga/desliga um bean por property em produção, no native essa decisão foi tomada na hora do build — mudar a property em runtime não tem efeito. O mesmo vale parcialmente para `@Profile`: perfis são avaliados quando o AOT roda, não quando o app sobe. Conclusão prática: o que você quer variar em runtime precisa virar configuração *de valor* (lida normalmente), não *de existência de bean*.

### (3) Build de CI lento sem cache

Compilar native image é caro — a análise de alcançabilidade percorre todo o grafo de classes e a compilação AOT do GraalVM pode levar muitos minutos, contra segundos de um `package` JVM. Sem cachear o toolchain do GraalVM e os artefatos intermediários, cada pipeline paga o custo cheio, e o tempo de feedback do CI despenca. Vale também não rodar o build nativo em todo commit: muitos times mantêm o build JVM rápido como gate padrão e disparam o nativo só em branches de release ou sob demanda.

## Em entrevista

### Frase pronta (inglês)

> Spring AOT is the bridge between Spring's dynamic runtime model and GraalVM's closed-world requirement. Since Spring Boot 3.0, it runs at build time and turns dynamic configuration into static artifacts — generated `__BeanDefinitions`, reachability hints under `META-INF/native-image`, and pre-built CGLIB proxies — so the native-image analysis can see a fully static application. When the AOT engine can't infer a reflective access, I register it explicitly with a `RuntimeHintsRegistrar` or `@RegisterReflectionForBinding`. For the actual compilation I use either native-build-tools, which needs a local GraalVM, or Buildpacks with `BP_NATIVE_IMAGE=true`, which ships GraalVM inside the container. The big mental shift for the team is that anything evaluated at runtime — like `@ConditionalOnProperty` — is frozen at build time and simply won't switch beans on and off in production.

### Vocabulário

| Português | Inglês |
| --- | --- |
| processamento AOT | AOT processing |
| dica de runtime | runtime hint |
| registrador de dicas | hints registrar |
| definição de bean | bean definition |
| ferramentas de build nativo | native build tools |
| perfil | profile |
| metadados de alcançabilidade | reachability metadata |

## Veja também

- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/08 - GraalVM Native Image — conceito e trade-offs|GraalVM Native Image (conceito)]]
- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/06 - Buildpacks — imagem sem Dockerfile|Buildpacks]]
- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/21 - Native vs JVM — a decisão honesta|Native vs JVM (a decisão honesta)]]
- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/index|Cloud-native e produção (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]

## Referências

- Spring Boot Reference — Introducing GraalVM Native Images: https://docs.spring.io/spring-boot/reference/packaging/native-image/introducing-graalvm-native-images.html
- Spring Boot Reference — GraalVM Native Images (index): https://docs.spring.io/spring-boot/reference/packaging/native-image/index.html
- GraalVM Native Build Tools (1.1.2): https://graalvm.github.io/native-build-tools/latest/
