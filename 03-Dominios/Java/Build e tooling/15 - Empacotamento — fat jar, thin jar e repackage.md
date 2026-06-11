---
title: "Empacotamento — fat jar, thin jar e repackage"
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
  - packaging
aliases:
  - "fat jar"
  - "uber jar"
  - "repackage"
---

# Empacotamento — fat jar, thin jar e repackage

> [!abstract] TL;DR
> Um `jar` simples só carrega **suas** classes — sem as dependências no classpath, ele não roda sozinho. Para distribuir uma aplicação você escolhe uma estratégia: o **fat jar** (uber jar) funde tudo num único arquivo via **Shade** (Maven) ou **Shadow** (Gradle), ao custo de ter que resolver **resource merging** (`META-INF/services`, `MANIFEST`) e **relocation** de pacotes; o **thin jar** mantém as deps separadas ao lado do jar fino; e o **`spring-boot:repackage`** produz um *executable jar* com **nested jars** intactos sob `BOOT-INF/lib/` e um `JarLauncher` — não é um fat jar padrão. O **layered jar** reorganiza esse executable jar em camadas para cache eficiente de imagem de container.

## O que é

Empacotar é transformar suas classes compiladas (`.class`) e os recursos do projeto em um artefato distribuível e, idealmente, executável. O formato base no ecossistema Java é o **jar** — um ZIP com um `META-INF/MANIFEST.MF` que descreve o conteúdo (e, opcionalmente, o `Main-Class`).

O problema é que um jar de aplicação típico **não inclui suas dependências**. As bibliotecas que você usa em runtime ficam fora dele. Rodar `java -jar app.jar` sem um classpath que aponte para essas libs resulta em `NoClassDefFoundError` na primeira classe de terceiros que o código toca.

As três grandes respostas a esse problema são: enfiar tudo num único jar (**fat jar**), distribuir o jar magro junto de uma pasta de libs (**thin jar**), ou usar o formato proprietário do Spring Boot que mantém os jars de deps inteiros aninhados dentro do artefato (**executable jar** via `repackage`).

## Por que importa

Empacotamento é o ponto onde "compila na minha máquina" vira "roda em produção". A escolha do formato afeta:

- **Portabilidade**: um único arquivo executável é trivial de mover; um thin jar exige carregar a pasta de libs junto.
- **Tamanho e build**: fat jars são grandes e reconstruídos por inteiro a cada mudança; layered jars permitem cache por camada.
- **Conflitos de classpath**: quando duas deps trazem a mesma classe ou o mesmo recurso (`META-INF/services`), fundir tudo num jar só pode quebrar silenciosamente sem **resource merging** e **relocation** corretos.
- **Containerização**: o layered jar existe justamente para que a camada de aplicação (que muda toda hora) fique separada da camada de dependências (que muda raramente), maximizando o reuso de camadas de imagem.

Numa entrevista de backend Java, saber distinguir um fat jar de Shade do executable jar do Boot é um marcador claro de quem já fez deploy de verdade.

## Como funciona

### jar simples, fat jar e thin jar

O `jar` produzido pelo `maven-jar-plugin` (ou pela task `jar` do Gradle) contém **apenas** as classes e recursos do seu módulo. Para rodá-lo você precisaria montar o classpath manualmente com todas as deps — inviável na prática para aplicações reais.

O **fat jar** (ou **uber jar**) resolve isso fundindo, num único jar, suas classes **mais o conteúdo descompactado de todas as dependências**. As classes de terceiros são extraídas e gravadas lado a lado com as suas, numa estrutura plana. O resultado roda com um `java -jar` limpo e um `URLClassLoader` padrão.

O **thin jar** vai pelo caminho oposto: mantém o jar magro com só as suas classes e distribui as dependências **separadas**, tipicamente numa pasta `libs/` ao lado, referenciada pelo `Class-Path` do manifesto ou por um script de inicialização. É o que a estratégia de *distribution* do **Gradle application plugin** faz: gera um ZIP/TAR com as classes, **todas as deps de runtime** como jars separados, e scripts de start específicos por SO (Unix e Windows).

### Shade / Shadow: resource merging e relocation

Fat jars não são produzidos pelo plugin de jar padrão. Em Maven, usa-se o **`maven-shade-plugin`** (goal `shade:shade`, atado à fase `package`); em Gradle, o **Shadow plugin** (task `shadowJar`).

Fundir várias deps num jar plano cria dois problemas que esses plugins endereçam:

- **Resource merging**: vários jars podem trazer o **mesmo caminho de recurso**. O caso clássico é `META-INF/services/<interface>`, usado pelo `ServiceLoader`. Se dois providers declaram o mesmo arquivo de serviço e você só copia "o último que ganhou", os outros providers somem. Os **resource transformers** do Shade resolvem isso: o `ServicesResourceTransformer` **concatena** as entradas de `META-INF/services`, e o `ManifestResourceTransformer` cuida do `MANIFEST.MF` (inclusive definindo o `Main-Class`).
- **Relocation**: duas deps podem trazer versões diferentes da **mesma classe** no mesmo pacote (ex.: dois `org.apache.commons.*`). Como um jar plano só tem um lugar para `org/apache/commons/Foo.class`, uma versão sobrescreve a outra — *version clash*. A **relocation** renomeia o pacote de uma das deps (ex.: `org.apache.commons` → `com.minhaapp.shaded.org.apache.commons`) reescrevendo o bytecode, de modo que as duas convivam isoladas.

### spring-boot:repackage e layered jar

O **`spring-boot:repackage`** (do Spring Boot Maven/Gradle plugin) **não** produz um fat jar padrão. Ele toma o jar magro já produzido e o reembala num **executable jar** com um layout proprietário:

- `BOOT-INF/classes/` — suas classes de aplicação;
- `BOOT-INF/lib/` — as dependências mantidas como **nested jars** (jars inteiros, **não** descompactados);
- `org/springframework/boot/loader/...` — as classes do **loader**, incluindo o **`JarLauncher`**, que é o `Main-Class` real no manifesto.

Ao rodar `java -jar app.jar`, o `JarLauncher` sobe primeiro, instala um *class loader* customizado capaz de ler classes de dentro dos jars aninhados (via `NestedJarFile`, **sem extrair** nada para disco) e só então invoca a sua `Main-Class` de aplicação. Manter os jars de deps inteiros (em vez de fundi-los) preserva as fronteiras de cada biblioteca e evita boa parte dos conflitos de resource/relocation que o fat jar enfrenta. O mecanismo de boot da aplicação em si (auto-config, starters, embedded server) é assunto do Galho 8 — ver [[03-Dominios/Java/Spring Core e Boot/16 - SpringApplication e o embedded server|SpringApplication e executable jar (Galho 8)]].

O **layered jar** é uma variação do executable jar voltada a **cache de imagem de container**. Ele organiza o conteúdo em **camadas** (tipicamente dependências, dependências de snapshot e aplicação) descritas por um índice **`layers.idx`**. A ideia: como as deps mudam raramente e suas classes mudam a cada build, separá-las em camadas distintas permite que uma ferramenta de build de imagem reaproveite as camadas estáveis e só reconstrua a de aplicação. O uso concreto em imagem/Docker é do Galho 17 *(planejado)*.

`jlink` e `jpackage` são empacotamento de outra natureza e ficam fora deste galho: ver [[03-Dominios/Java/JVM/08 - JPMS — o sistema de módulos|JPMS e jlink (Galho 3)]] (runtime customizado, depende de módulos JPMS) e [[03-Dominios/Java/JavaFX/13 - Empacotamento — módulos, jlink e jpackage|jpackage e empacotamento nativo (Galho 6)]] (instalador nativo).

## Na prática

Configuração mínima do **`maven-shade-plugin`** com resource merging e relocation:

```xml
<plugin>
  <groupId>org.apache.maven.plugins</groupId>
  <artifactId>maven-shade-plugin</artifactId>
  <executions>
    <execution>
      <phase>package</phase>
      <goals>
        <goal>shade</goal>
      </goals>
      <configuration>
        <transformers>
          <!-- concatena META-INF/services em vez de sobrescrever -->
          <transformer
            implementation="org.apache.maven.plugins.shade.resource.ServicesResourceTransformer"/>
          <!-- define o Main-Class no MANIFEST do uber jar -->
          <transformer
            implementation="org.apache.maven.plugins.shade.resource.ManifestResourceTransformer">
            <mainClass>com.exemplo.app.Main</mainClass>
          </transformer>
        </transformers>
        <relocations>
          <relocation>
            <pattern>org.apache.commons</pattern>
            <shadedPattern>com.exemplo.shaded.org.apache.commons</shadedPattern>
          </relocation>
        </relocations>
      </configuration>
    </execution>
  </executions>
</plugin>
```

Estrutura interna de um **fat jar** (Shade) versus o **executable jar** do Boot:

```text
# fat jar (Shade/Shadow) — tudo plano, classes de deps EXTRAÍDAS
app-uber.jar
├── META-INF/
│   ├── MANIFEST.MF              (Main-Class: com.exemplo.app.Main)
│   └── services/...             (mesclado pelo ServicesResourceTransformer)
├── com/exemplo/app/...          (suas classes)
├── org/apache/commons/...       (classes da dep, extraídas/relocadas)
└── ...

# executable jar do Boot (repackage) — deps como NESTED JARS
app.jar
├── META-INF/
│   └── MANIFEST.MF              (Main-Class: org.springframework.boot.loader.launch.JarLauncher)
├── org/springframework/boot/loader/...   (JarLauncher + loader)
└── BOOT-INF/
    ├── classes/com/exemplo/app/...        (suas classes)
    ├── lib/spring-core-x.y.z.jar          (deps inteiras, NÃO extraídas)
    ├── lib/...
    └── layers.idx                         (só em layered jar)
```

Em ambos os casos, a execução é a mesma do ponto de vista do operador:

```bash
java -jar app.jar
```

## Armadilhas

### (1) Fat jar com resource merge quebrado

Sem um resource transformer adequado, quando duas deps trazem o mesmo `META-INF/services/<interface>`, o Shade copia só um dos arquivos e o outro some. Resultado: o `ServiceLoader` deixa de enxergar providers que existiam separadamente, e funcionalidades que dependiam de descoberta via `META-INF/services` falham em runtime — muitas vezes de forma silenciosa, só quebrando quando aquele provider específico é requisitado. Sempre inclua o `ServicesResourceTransformer` (e cuide do `MANIFEST` com o `ManifestResourceTransformer`).

### (2) Relocation esquecida

Quando duas dependências trazem versões diferentes da mesma classe no mesmo pacote e você não relocou nenhuma, o fat jar fica com **uma** versão arbitrária da classe (a última gravada vence). Isso é *version clash*: o código compilou contra uma API mas em runtime carrega outra, produzindo `NoSuchMethodError`/`ClassNotFoundException` difíceis de diagnosticar. A relocation isola os pacotes conflitantes renomeando-os no bytecode.

### (3) Usar layered jar sem necessidade

O layered jar só compensa quando você constrói **imagens de container** e quer aproveitar cache de camadas. Para uma aplicação distribuída como jar solto, rodada com `java -jar` direto, habilitar camadas adiciona complexidade (índice `layers.idx`, ferramentas de extração de camadas) sem nenhum ganho. Não ligue camadas por reflexo — ligue quando o pipeline de imagem realmente usar as camadas.

## Em entrevista

### Frase pronta (inglês)

A plain jar contains only my own classes, so it can't run on its own without a classpath pointing to every dependency. To ship a runnable artifact I either build a fat jar — with Maven Shade or the Gradle Shadow plugin, which flattens all dependencies into one jar and needs resource transformers to merge things like `META-INF/services` and relocation to avoid package clashes — or I use Spring Boot's `repackage`, which is **not** a standard fat jar: it keeps the dependency jars intact as nested jars under `BOOT-INF/lib/` and boots through a `JarLauncher`. When I'm building container images, I enable layered jars so the rarely-changing dependency layers stay cached and only the application layer is rebuilt.

### Vocabulário

| Termo PT | Termo EN |
| --- | --- |
| jar gordo / uber jar | fat jar / uber jar |
| jar magro | thin jar |
| fusão de recursos | resource merging |
| transformador de recursos | resource transformer |
| relocação de pacotes | package relocation |
| conflito de versão | version clash |
| jar aninhado | nested jar |
| jar executável | executable jar |
| jar em camadas | layered jar |
| carregador de classes | class loader |

## Veja também

- [[03-Dominios/Java/Build e tooling/04 - Maven — plugins, profiles e o wrapper|Maven — plugins]]
- [[03-Dominios/Java/Spring Core e Boot/16 - SpringApplication e o embedded server|SpringApplication e executable jar (Galho 8)]]
- [[03-Dominios/Java/JVM/08 - JPMS — o sistema de módulos|JPMS e jlink (Galho 3)]]
- [[03-Dominios/Java/JavaFX/13 - Empacotamento — módulos, jlink e jpackage|jpackage (Galho 6)]]
- [[03-Dominios/Java/Build e tooling/index|Build, tooling e ecossistema (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]

## Referências

- Apache Maven Shade Plugin — https://maven.apache.org/plugins/maven-shade-plugin/
- Gradle Application Plugin — https://docs.gradle.org/current/userguide/application_plugin.html
- Spring Boot Maven Plugin — https://docs.spring.io/spring-boot/maven-plugin/
- Spring Boot — The Executable Jar Format — https://docs.spring.io/spring-boot/specification/executable-jar/index.html
