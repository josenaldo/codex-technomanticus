---
title: "Auto-configuration e starters"
created: 2026-06-08
updated: 2026-06-08
type: concept
progress: backlog
status: seedling
publish: true
fase: Magus
tags:
  - java
  - spring
  - magus
  - auto-config
  - boot
aliases:
  - "auto-configuration"
  - "starters"
  - "@EnableAutoConfiguration"
---

# Auto-configuration e starters

> [!abstract] TL;DR
> A auto-configuration é o coração do Spring Boot: ela olha o que está no classpath e configura beans sensatos por padrão, mas sempre **cede o lugar** para qualquer bean que você definir (`@ConditionalOnMissingBean`). O gatilho é `@EnableAutoConfiguration` (embutido em `@SpringBootApplication`). No Boot 3.x o catálogo de classes auto-configuradas vive num único arquivo: `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports` — o velho `spring.factories` não vale mais para isso. Um **starter** não é código: é um POM agregador que puxa o conjunto coerente de dependências (`spring-boot-starter-web`, etc.), e quem traz o código de configuração é o módulo `*-autoconfigure`.

## O que é

**Auto-configuration** é o mecanismo pelo qual o Spring Boot configura automaticamente a aplicação **com base nas dependências (jars) presentes no classpath**. Se há um driver de banco e nenhuma `DataSource` definida por você, o Boot cria uma; se há `spring-webmvc` no classpath, ele sobe um `DispatcherServlet`, um servidor embutido, conversores de mensagem JSON e por aí vai.

A ideia central é **convention over configuration** com escape hatch: o Boot oferece um padrão razoável para cada peça, mas todo padrão pode ser sobrescrito definindo o seu próprio bean. A documentação chama isso de comportamento **não-invasivo** (_non-invasive_) — você nunca fica preso ao que o Boot decidiu.

Duas peças andam juntas mas são coisas diferentes:

- **Auto-configuration**: as classes `@AutoConfiguration` que efetivamente criam beans condicionalmente. É código.
- **Starter**: um POM (Maven) ou descritor de dependências que **agrega** um conjunto coerente de bibliotecas. É só dependência, sem lógica.

Você adiciona o starter; o starter traz (transitivamente) o módulo de auto-configuration; a auto-configuration roda na inicialização e monta os beans.

## Por que importa

Antes do Boot, subir uma aplicação Spring significava dezenas de linhas de XML ou de `@Configuration` manual: declarar `DispatcherServlet`, `ViewResolver`, `DataSource`, `EntityManagerFactory`, `TransactionManager`, conversores, validadores. A auto-configuration apaga a maior parte desse boilerplate — você declara a intenção (`spring-boot-starter-data-jpa`) e o resto aparece pronto.

Para o nível **magus**, o que importa não é usar a auto-configuration (todo mundo usa), e sim **entendê-la por dentro**:

- Saber **por que** um bean apareceu (ou **por que não** apareceu) sem ficar adivinhando.
- Saber **sobrescrever** um padrão sem brigar com o framework.
- Saber **escrever a sua própria** auto-configuration quando você publica uma biblioteca interna que outras equipes vão consumir — esse é o teste de domínio de verdade.

É também o ponto onde mais gente se enrola em entrevista: confundir starter com auto-config, achar que precisa escrever código no starter, ou citar `spring.factories` (mecanismo aposentado no Boot 3).

## Como funciona

### `@EnableAutoConfiguration` / `@SpringBootApplication`

A auto-configuration é ligada por **uma** anotação na classe de configuração primária:

- **`@EnableAutoConfiguration`** — liga explicitamente a auto-configuration.
- **`@SpringBootApplication`** — meta-anotação que é a forma idiomática e já inclui `@EnableAutoConfiguration`.

`@SpringBootApplication` é açúcar para a composição de três anotações:

| Anotação embutida | Papel |
| --- | --- |
| `@SpringBootConfiguration` | Marca a classe como fonte de configuração (variante de `@Configuration` específica do Boot). |
| `@EnableAutoConfiguration` | Liga o motor de auto-configuration. |
| `@ComponentScan` | Varre o pacote da classe e subpacotes em busca de `@Component`/`@Service`/etc. |

> [!warning] Uma anotação só
> Adicione `@EnableAutoConfiguration` (ou `@SpringBootApplication`) em **uma única** classe — em geral a classe principal. Espalhar a anotação por várias classes leva a comportamento confuso.

O pacote da classe anotada também define o **pacote de auto-configuration** padrão: é a partir dele que recursos auto-configurados (entidades JPA, repositórios Spring Data) fazem o scan por padrão.

### O registro via `AutoConfiguration.imports` (substituiu `spring.factories` — Boot 2.7+/3.x)

Como o Boot sabe **quais** classes são candidatas a auto-configuration? Ele lê um arquivo de texto plano dentro de cada jar:

```text
META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports
```

Cada linha é o nome totalmente qualificado de uma classe `@AutoConfiguration`, uma por linha. A documentação é literal sobre isso:

> Spring Boot checks for the presence of a `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports` file within your published jar. The file should list your configuration classes, with one class name per line.

> [!important] `spring.factories` aposentado para auto-config
> Até o Boot 2.6, as auto-configurations eram registradas em `META-INF/spring.factories` sob a chave `org.springframework.boot.autoconfigure.EnableAutoConfiguration`. A partir do **Boot 2.7** isso foi depreciado em favor do arquivo `.imports`, e no **Boot 3.x** o `.imports` é o **único** mecanismo aceito para auto-configuration — o `spring.factories` deixou de ser lido para esse propósito. (O `spring.factories` ainda existe para outros tipos de registro, como `ApplicationListener`/`EnvironmentPostProcessor`, mas não para auto-config.)

Em entrevista, citar `spring.factories` como o lugar das auto-configurations num projeto Boot 3 é uma bandeira vermelha de "parou de estudar em 2021".

### Como auto-config usa `@Conditional` e cede pro usuário (`@ConditionalOnMissingBean`); ordem

Toda classe `@AutoConfiguration` é, no fundo, uma `@Configuration` comum — `@AutoConfiguration` é meta-anotada com `@Configuration`. O que a torna "auto" é (1) estar listada no `.imports` e (2) ser fortemente guardada por **condições**.

As condições mais usadas (todas detalhadas em [[03-Dominios/Tecnologia/Java/Spring Core e Boot/14 - Conditional beans — @Conditional e os @ConditionalOn|Conditional beans]]):

- **`@ConditionalOnClass`** — só ativa a configuração se uma classe específica estiver no classpath. É assim que o Boot "detecta a tecnologia": `@ConditionalOnClass(DataSource.class)`.
- **`@ConditionalOnMissingBean`** — o coração da gentileza: o bean padrão **só** é criado se você **não** definiu um do mesmo tipo. É o que faz a auto-configuration **ceder o lugar** ao usuário.
- **`@ConditionalOnProperty`**, **`@ConditionalOnMissingClass`**, **`@ConditionalOnWebApplication`** — variantes para ligar/desligar por propriedade, ausência de classe ou tipo de aplicação.

A documentação coloca isso como regra de ouro do autor de auto-config:

> The `@ConditionalOnMissingBean` annotation is one common example that is used to allow developers to override auto-configuration if they are not happy with your defaults.

**Ordem.** Auto-configurations às vezes precisam rodar antes ou depois de outras (ex.: uma config web que depende da `WebMvcAutoConfiguration` já ter rodado). Para isso:

- Atributos **`before` / `beforeName` / `after` / `afterName`** na própria `@AutoConfiguration`.
- Ou as anotações dedicadas **`@AutoConfigureBefore`** e **`@AutoConfigureAfter`**.
- Para ordenar duas auto-configs que não se conhecem, **`@AutoConfigureOrder`** (mesma semântica de `@Order`, mas dedicada a auto-config).

> [!note] Ordem de definição ≠ ordem de criação
> A doc é explícita: a ordem entre auto-configs só afeta **a ordem em que os beans são *definidos***. A ordem em que os beans são efetivamente **criados** continua sendo ditada pelas dependências entre eles e por `@DependsOn`. Ou seja: `@AutoConfigureAfter` não garante que o bean da outra config já exista quando o seu for instanciado — garante apenas que a definição dela foi processada antes.

### Starters: o que são (POM agregador, não código)

Um **starter** é, nas palavras da doc, *"a set of convenient dependency descriptors"*: um POM que reúne, num único `<dependency>`, todo o conjunto coerente de bibliotecas que você precisaria caçar e colar manualmente.

Pontos centrais:

- **Não tem código.** O starter `spring-boot-starter-web` é só um `pom.xml` que declara dependências: Spring MVC, Jackson, Tomcat embutido, o starter base, etc. A lógica de auto-configuration mora no módulo `spring-boot-autoconfigure` (e seus equivalentes por tecnologia), que o starter traz transitivamente.
- **Convenção de nome:** starters **oficiais** seguem `spring-boot-starter-*` (ex.: `spring-boot-starter-web`, `spring-boot-starter-data-jpa`, `spring-boot-starter-security`, `spring-boot-starter-actuator`). O prefixo `spring-boot` é reservado para artefatos oficiais.
- Starters de **terceiros** seguem o padrão invertido `*-spring-boot-starter` (ex.: um projeto `acme` publicaria `acme-spring-boot-starter`).

| Starter | Traz |
| --- | --- |
| `spring-boot-starter` | núcleo: auto-config, logging, YAML, `SpringApplication`. |
| `spring-boot-starter-web` | Spring MVC + servidor embutido (Tomcat). |
| `spring-boot-starter-data-jpa` | Spring Data JPA + Hibernate. |
| `spring-boot-starter-security` | Spring Security. |
| `spring-boot-starter-test` | JUnit, Mockito, AssertJ, Spring Test. |

A divisão idiomática numa biblioteca própria é dois módulos: um `acme-spring-boot-autoconfigure` (com as classes `@AutoConfiguration` e o `.imports`) e um `acme-spring-boot-starter` (POM que só depende do autoconfigure + as libs de runtime). Quem consome adiciona o starter.

### Debug e AOT (`--debug`, ConditionEvaluationReport, `/actuator/conditions`; AOT/build-time)

Quando um bean "deveria estar lá e não está" (ou o oposto), você não adivinha — você lê o **relatório de avaliação de condições**.

- **`--debug`**: subir a aplicação com `java -jar app.jar --debug` (ou `debug=true` nas propriedades) imprime no console o **Conditions Evaluation Report**, listando o que foi **Positive matches** (auto-config aplicada) e **Negative matches** (não aplicada) — e o **motivo** de cada decisão.
- **`/actuator/conditions`**: com o `spring-boot-starter-actuator` presente e o endpoint exposto, o mesmo relatório fica disponível em JSON via HTTP. Útil em ambientes onde você não tem o console de boot à mão.

Esse relatório é a ferramenta número um para depurar auto-configuration: ele responde "por que esse bean não apareceu?" com algo como *"did not find class 'jakarta.persistence.EntityManager'"* em vez de te deixar no escuro.

**AOT / build-time (texto, sem aprofundar).** A partir do Boot 3, parte do trabalho da auto-configuration pode ser resolvida em **tempo de build** via processamento **AOT** (ahead-of-time): as condições são avaliadas e o grafo de beans é "congelado" durante a compilação, reduzindo o trabalho em runtime. Isso é a base para a **imagem nativa** (GraalVM), onde quase toda decisão precisa acontecer em build-time porque não há reflexão livre em runtime. O detalhamento de native image, AOT e packaging fica para o galho de empacotamento e deploy *(planejado)* — aqui basta o mapa mental: a auto-configuration foi reprojetada para ser amigável a build-time.

## Na prática

Esqueleto de uma auto-configuration própria — uma biblioteca que entrega um `OrderFormatter` por padrão, mas cede se a aplicação consumidora definir o seu:

```java
package com.acme.order.autoconfigure;

import org.springframework.boot.autoconfigure.AutoConfiguration;
import org.springframework.boot.autoconfigure.condition.ConditionalOnClass;
import org.springframework.boot.autoconfigure.condition.ConditionalOnMissingBean;
import org.springframework.context.annotation.Bean;

@AutoConfiguration
@ConditionalOnClass(OrderFormatter.class) // só ativa se a lib estiver no classpath
public class OrderAutoConfiguration {

    @Bean
    @ConditionalOnMissingBean // cede o lugar se o consumidor já tiver um OrderFormatter
    public OrderFormatter orderFormatter(OrderProperties properties) {
        return new OrderFormatter(properties.getPattern());
    }
}
```

O registro que torna a classe acima descoberta pelo Boot — um arquivo de texto, uma linha por classe:

```text
# src/main/resources/META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports
com.acme.order.autoconfigure.OrderAutoConfiguration
```

Do lado de quem consome, sobrescrever o padrão é só declarar o próprio bean — o `@ConditionalOnMissingBean` desativa o da lib:

```java
@Configuration
public class CustomerOrderConfig {

    @Bean
    public OrderFormatter orderFormatter() {
        return new OrderFormatter("CUSTOM-####"); // este vence; o auto-configurado recua
    }
}
```

E desativar uma auto-configuration inteira (sua ou de terceiro), quando ela atrapalha:

```java
@SpringBootApplication(exclude = { OrderAutoConfiguration.class })
public class Application { }
```

```text
# ou via propriedade (equivalente, útil quando a classe não está no classpath de compilação)
spring.autoconfigure.exclude=com.acme.order.autoconfigure.OrderAutoConfiguration
```

## Armadilhas

### Criar um starter achando que ele precisa de código

**Descrição.** Times montam um "starter interno" e despejam classes `@AutoConfiguration`, `@Bean` e o `.imports` dentro do módulo cujo `pom.xml` tem `<packaging>pom</packaging>` ou cujo nome é `*-starter` — misturando o agregador de dependências com o código de configuração.

**Exemplo.** Um módulo único `acme-spring-boot-starter` que contém `OrderAutoConfiguration.java` **e** declara dependências de runtime. Funciona, mas viola a convenção: o starter deveria ser só POM.

**Fix.** Separe em dois módulos: `acme-spring-boot-autoconfigure` (todo o código + `.imports` + `@ConfigurationProperties`) e `acme-spring-boot-starter` (POM que apenas depende do autoconfigure e das libs de runtime). Quem consome adiciona só o starter. É o mesmo padrão que o próprio Boot usa internamente.

### Auto-config não dispara — faltou `@ConditionalOnClass`

**Descrição.** Você publica a auto-config, adiciona ao `.imports`, mas o bean nunca aparece — ou pior, aparece e explode com `NoClassDefFoundError` em ambientes onde a lib opcional não está presente.

**Exemplo.** Uma `OrderAutoConfiguration` que cria um bean dependente de uma biblioteca opcional (digamos, um cliente HTTP) **sem** guardar a classe com `@ConditionalOnClass(HttpClient.class)`. Em projetos sem essa lib, o carregamento da `@Configuration` falha ao resolver os tipos.

**Fix.** Guarde toda auto-config com `@ConditionalOnClass` sobre as classes que ela usa. Assim a config inteira é silenciosamente ignorada quando a dependência não está no classpath — que é exatamente o comportamento "detecta a tecnologia". Para diagnosticar por que não disparou, suba com `--debug` e leia os **Negative matches** do Conditions Evaluation Report.

### Sobrescrever sem entender `@ConditionalOnMissingBean`

**Descrição.** Você define um bean para "sobrescrever" o padrão do Boot, mas ele não substitui nada — ou você acaba com dois beans e uma `NoUniqueBeanDefinitionException`. Quase sempre é confusão sobre **o tipo** que o `@ConditionalOnMissingBean` observa.

**Exemplo.** A auto-config tem `@ConditionalOnMissingBean(OrderFormatter.class)`. Você declara um bean de uma **subclasse** `FancyOrderFormatter` mas tipa o método como `FancyOrderFormatter`, não como `OrderFormatter` — dependendo da versão e da configuração, o `@ConditionalOnMissingBean` pode não reconhecer o seu como "o mesmo tipo" e cria o padrão também.

**Fix.** Declare o bean com o **mesmo tipo** que a auto-config observa (o tipo da interface/classe base). Em caso de dúvida sobre qual tipo é checado, leia o `@ConditionalOnMissingBean` da auto-config (e lembre que ele tem atributos `value`/`type`/`name` para ajustar). Use `/actuator/conditions` ou `--debug` para confirmar que o bean do Boot recuou (`@ConditionalOnMissingBean ... found beans of type 'OrderFormatter'`).

## Em entrevista

### Frase pronta (inglês)

> Auto-configuration is the engine of Spring Boot: it inspects the classpath and wires up sensible default beans, but it always backs off when you define your own — that's the role of `@ConditionalOnMissingBean`. The set of candidate auto-configuration classes is declared, in Boot 3, in a single file, `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports`; this replaced the old `spring.factories` registration. A starter, by contrast, is not code at all — it's a POM that aggregates a coherent set of dependencies, like `spring-boot-starter-web`. The actual configuration logic lives in a separate `*-autoconfigure` module that the starter pulls in transitively, and you debug what got applied with `--debug` or the `/actuator/conditions` endpoint.

### Vocabulário

| Termo PT | Termo EN |
| --- | --- |
| auto-configuração | auto-configuration |
| arquivo de registro de imports | imports file (`AutoConfiguration.imports`) |
| starter (agregador de dependências) | dependency starter |
| ceder o lugar / recuar | back off |
| relatório de avaliação de condições | conditions evaluation report |
| ordem de definição vs. de criação | definition order vs. creation order |
| não-invasivo | non-invasive |
| tempo de build / antecipado | ahead-of-time (AOT) / build-time |

## Veja também

- [[03-Dominios/Tecnologia/Java/Spring Core e Boot/14 - Conditional beans — @Conditional e os @ConditionalOn|Conditional beans]] — o vocabulário de condições (`@ConditionalOnClass`, `@ConditionalOnMissingBean`) que faz a auto-config funcionar.
- [[03-Dominios/Tecnologia/Java/Spring Core e Boot/16 - SpringApplication e o embedded server|SpringApplication e o embedded server]] — o que acontece no `run()` depois que a auto-config monta os beans.
- [[03-Dominios/Tecnologia/Java/Jakarta EE/13 - CDI avançado — interceptors, decorators e extensões|CDI avançado — interceptors, decorators e extensões]] — no mundo Jakarta EE, **CDI Lite / build compatible extensions** são o caminho build-time equivalente: runtimes que resolvem o grafo de beans em tempo de build em vez de runtime, mesma motivação por trás do AOT do Boot.
- [[03-Dominios/Tecnologia/Java/Spring Core e Boot/index|Spring Core e Boot (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- Verbetes: [[03-Dominios/Tecnologia/Java/Dicionário de Java#auto-configuration|auto-configuration]], [[03-Dominios/Tecnologia/Java/Dicionário de Java#starter (Spring Boot)|starter (Spring Boot)]], [[03-Dominios/Tecnologia/Java/Dicionário de Java#@EnableAutoConfiguration|@EnableAutoConfiguration]]

## Referências

- Spring Boot Reference — Using Spring Boot: Auto-configuration. https://docs.spring.io/spring-boot/reference/using/auto-configuration.html
- Spring Boot Reference — Features: Creating Your Own Auto-configuration. https://docs.spring.io/spring-boot/reference/features/developing-auto-configuration.html
- Spring Boot Reference — Using Spring Boot: Build Systems (Starters). https://docs.spring.io/spring-boot/reference/using/build-systems.html
