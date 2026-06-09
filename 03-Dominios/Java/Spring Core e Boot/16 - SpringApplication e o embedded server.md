---
title: "SpringApplication e o embedded server"
created: 2026-06-08
updated: 2026-06-08
type: concept
progress: backlog
status: seedling
publish: true
fase: magus
tags:
  - java
  - spring
  - magus
  - boot
aliases:
  - "SpringApplication"
  - "embedded server"
---

# SpringApplication e o embedded server

> [!abstract] TL;DR
> `SpringApplication.run()` faz três coisas de uma vez: cria o `ApplicationContext` correto para o tipo de aplicação, dispara o ciclo de auto-configuration e sobe o servidor embutido. O servidor padrão é Tomcat; trocar por Jetty ou Undertow é uma questão de mover starters no POM. O resultado é um **fat jar** — um único artefato autocontido que roda com `java -jar` sem precisar de servidor externo. `CommandLineRunner` e `ApplicationRunner` são os ganchos canônicos para executar código logo após o contexto estar pronto, antes de o servidor aceitar tráfego.

## O que é

`SpringApplication` é a classe de entrada do Spring Boot. Seu método estático `run()` orquestra toda a inicialização: detecta o tipo de aplicação (web Servlet, Reactive ou standalone), instancia o `ApplicationContext` adequado, ativa a auto-configuration e levanta o servidor embutido configurado.

O **embedded server** (servidor embutido) é um servidor HTTP que reside dentro do fat jar — não é necessário instalar nem gerenciar um contêiner externo. Tomcat, Jetty e Undertow são as opções suportadas pelo Spring Boot 3.x, com Tomcat como padrão via `spring-boot-starter-web`.

## Por que importa

O modelo de servidor embutido muda o paradigma de deploy: a aplicação não é mais um WAR implantado num servidor externo, mas um **processo autossuficiente**. Isso alinha com arquitetura de microsserviços e containers Docker — cada serviço carrega sua própria versão do servidor, elimina conflitos de classpath entre aplicações num mesmo contêiner e simplifica pipelines de CI/CD.

Para entrevistas de nível sênior, o entrevistador espera que o candidato compreenda não só "como funciona" mas também os trade-offs: startup mais lento com lazy-initialization desligada, risco de lógica pesada travar o boot, e quando faz sentido permanecer no modelo WAR.

## Como funciona

### SpringApplication.run(): cria o contexto, dispara auto-config, sobe o servidor

O ponto de entrada mínimo de uma aplicação Boot é:

```java
@SpringBootApplication
public class MyApplication {
    public static void main(String[] args) {
        SpringApplication.run(MyApplication.class, args);
    }
}
```

Internamente, `run()` executa a seguinte sequência:

1. Publica `ApplicationStartingEvent` (listeners registrados antes do contexto recebem).
2. Prepara o `Environment` (carrega `application.properties`, perfis) → `ApplicationEnvironmentPreparedEvent`.
3. Determina o tipo de contexto: `AnnotationConfigServletWebServerApplicationContext` para Servlet, `AnnotationConfigReactiveWebServerApplicationContext` para Reactive, `AnnotationConfigApplicationContext` para standalone.
4. Executa os `ApplicationContextInitializer` → `ApplicationContextInitializedEvent`.
5. Carrega definições de beans; aplica auto-configuration → `ApplicationPreparedEvent`.
6. Chama `context.refresh()` — aqui o servidor embutido é instanciado e inicia a escuta.
7. Publica `ApplicationStartedEvent` + `AvailabilityChangeEvent(LivenessState.CORRECT)`.
8. Executa `ApplicationRunner`s e `CommandLineRunner`s.
9. Publica `ApplicationReadyEvent` + `AvailabilityChangeEvent(ReadinessState.ACCEPTING_TRAFFIC)`.

Se qualquer etapa falhar, o Boot publica `ApplicationFailedEvent` e exibe uma mensagem diagnóstica de `FailureAnalyzer` — por exemplo, "Port 8080 was already in use" com sugestão de ação.

A personalização do `SpringApplication` pode ser feita programaticamente antes de chamar `run()`:

```java
SpringApplication app = new SpringApplication(MyApplication.class);
app.setBannerMode(Banner.Mode.OFF);
app.setLazyInitialization(true);
app.run(args);
```

Ou via `application.properties`:

```properties
spring.main.lazy-initialization=true
spring.main.banner-mode=off
```

### ApplicationRunner/CommandLineRunner e listeners do startup

`CommandLineRunner` e `ApplicationRunner` são interfaces funcionais executadas **depois** que o contexto foi totalmente inicializado e o servidor está no ar, mas **antes** de `ApplicationReadyEvent` ser publicado. São beans Spring normais — use `@Order` para sequenciar múltiplos runners.

```java
@Component
@Order(1)
public class CargaDadosRunner implements ApplicationRunner {
    @Override
    public void run(ApplicationArguments args) {
        boolean debug = args.containsOption("debug");
        List<String> arquivos = args.getNonOptionArgs();
        // inicialização após o boot
    }
}

@Component
@Order(2)
public class VerificacaoRunner implements CommandLineRunner {
    @Override
    public void run(String... args) {
        // recebe args raw como String[]
    }
}
```

A diferença prática: `ApplicationRunner` recebe `ApplicationArguments`, que parse `--chave=valor` estruturado; `CommandLineRunner` recebe `String[]` direto do `main`.

Para lógica que precisa reagir a eventos **antes** do contexto existir (ex.: ajustar `Environment`), o caminho é `ApplicationListener<ApplicationEnvironmentPreparedEvent>` registrado via `META-INF/spring.factories` ou via `SpringApplication.addListeners()`.

### Embedded server (Tomcat default; Jetty/Undertow via starter)

Ao detectar `spring-boot-starter-web` no classpath, a auto-configuration instancia um `TomcatServletWebServerFactory` e sobe o Tomcat embutido na porta `8080`.

Para trocar para **Jetty**:

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
    <exclusions>
        <exclusion>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-tomcat</artifactId>
        </exclusion>
    </exclusions>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-jetty</artifactId>
</dependency>
```

O mesmo padrão vale para **Undertow** — substitua `spring-boot-starter-jetty` por `spring-boot-starter-undertow`. A auto-configuration detecta qual factory está disponível e usa.

Configuração básica via `application.properties`:

```properties
server.port=8080
server.servlet.context-path=/api
```

Customizações avançadas (thread pool, timeouts, connectors) são feitas via `WebServerFactoryCustomizer<TomcatServletWebServerFactory>`. O pipeline web sobre esse servidor é o galho [[03-Dominios/Java/Web e APIs REST/06 - O pipeline do DispatcherServlet|Web e APIs REST]]; tuning profundo de servidor e configurações de produção ficam para o Galho 17 (planejado).

> [!note] O servidor embutido roda o Servlet container
> O embedded server implementa o contêiner de Servlets que a Servlet API (Jakarta EE) define. O Spring MVC usa `DispatcherServlet` como front controller, que é registrado nesse contêiner. Para entender a spec que o embedded Tomcat implementa, veja [[03-Dominios/Java/Jakarta EE/03 - Servlet API — o alicerce HTTP|Servlet API — o alicerce HTTP]].

### Fat/executable jar e layered jar (conceito)

Um **fat jar** (ou executable jar) é um único arquivo `.jar` que contém:
- O bytecode da aplicação
- Todas as dependências (jars dentro do jar)
- O servidor embutido
- O Spring Boot Launcher, que sabe como carregar classes de JARs aninhados

Para executar:

```bash
java -jar minha-aplicacao-1.0.0.jar --server.port=9090
```

O Maven Plugin do Spring Boot cuida do empacotamento:

```xml
<plugin>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-maven-plugin</artifactId>
</plugin>
```

O **layered jar** é uma variante que organiza o conteúdo em camadas (`dependencies`, `spring-boot-loader`, `snapshot-dependencies`, `application`) para otimizar cache de layers em imagens Docker — a camada de dependências externas raramente muda; só a camada `application` é reconstruída no pipeline. O detalhamento de packaging, layered jars e imagens nativas é coberto no Galho 15/17 (planejado).

## Na prática

Exemplo completo de `main` com um `CommandLineRunner` para aquecimento:

```java
@SpringBootApplication
public class CatalogoApplication {

    public static void main(String[] args) {
        SpringApplication.run(CatalogoApplication.class, args);
    }

    // Runner como bean inline (alternativa ao @Component separado)
    @Bean
    public CommandLineRunner aquecimento(CatalogoService service) {
        return args -> {
            System.out.println("Servidor no ar. Aquecendo cache...");
            service.precarregarCatalogo();
        };
    }
}
```

Usar `@Bean CommandLineRunner` com injeção de parâmetro é idiomático quando o runner precisa de um colaborador — evita `@Autowired` num `@Component`.

## Armadilhas

**1. Lógica pesada diretamente no `main`**

```java
// Errado — bloqueia o bootstrap antes do contexto existir
public static void main(String[] args) {
    SpringApplication.run(App.class, args);
    carregarDados(); // nunca chega aqui; mesmo que chegue, contexto pode já estar fechando
}
```

```java
// Correto — delega para runner que roda com o contexto pronto
@Bean
public ApplicationRunner inicializacao(DataService service) {
    return args -> service.carregarDados();
}
```

**2. Assumir modelo WAR/servidor externo por hábito**

```xml
<!-- Errado — empacotar como WAR e depender de servidor externo num projeto novo -->
<packaging>war</packaging>
```

```java
// Errado — extends SpringBootServletInitializer sem necessidade real
public class App extends SpringBootServletInitializer { ... }
```

O modelo padrão do Spring Boot é fat jar + servidor embutido. Herdar `SpringBootServletInitializer` e empacotar como WAR só faz sentido quando o deploy é obrigatoriamente num servidor externo legado (ex.: WebSphere corporativo). Em projetos greenfield, use fat jar.

**3. Bloquear o startup num runner**

```java
// Errado — operação bloqueante longa impede ApplicationReadyEvent
@Component
public class SyncRunner implements CommandLineRunner {
    @Override
    public void run(String... args) throws Exception {
        sincronizarBaseDados(); // leva 5 minutos; saúde/readiness nunca é reportada
    }
}
```

```java
// Correto — disparar assíncrono ou limitar o trabalho síncrono a operações rápidas
@Component
public class SyncRunner implements CommandLineRunner {
    private final TaskExecutor executor;

    @Override
    public void run(String... args) {
        executor.execute(this::sincronizarBaseDados);
    }
}
```

Runners síncronos que demoram impedem `ReadinessState.ACCEPTING_TRAFFIC` — o load balancer considera a instância não pronta e pode desregistrá-la.

## Em entrevista

### Frase pronta (inglês)

- "When you call `SpringApplication.run()`, Spring Boot determines the correct application context type, triggers auto-configuration based on the classpath, and starts the embedded server — all before control returns to your code."
- "`CommandLineRunner` and `ApplicationRunner` run after the context is fully refreshed but before the application signals readiness, making them the right place for post-startup initialization — as long as they don't block for too long."
- "A fat jar bundles the application code, all dependencies, and an embedded servlet container into a single executable artifact. You just `java -jar` it — no external application server required."
- "Switching the embedded server from Tomcat to Jetty is purely a dependency swap: exclude `spring-boot-starter-tomcat`, include `spring-boot-starter-jetty` — Spring Boot's auto-configuration picks it up automatically."

### Vocabulário

| Termo PT | Termo EN |
|---|---|
| servidor embutido | embedded server |
| jar gordo / jar executável | fat jar / executable jar |
| jar em camadas | layered jar |
| inicialização preguiçosa | lazy initialization |
| runner de inicialização | startup runner |
| evento de disponibilidade | availability change event |
| fábrica de servidor web | web server factory |
| analisador de falha | failure analyzer |

## Veja também

- [[03-Dominios/Java/Spring Core e Boot/15 - Auto-configuration e starters|Auto-configuration e starters]]
- [[03-Dominios/Java/Spring Core e Boot/17 - Actuator e observabilidade|Actuator e observabilidade]]
- [[03-Dominios/Java/Jakarta EE/03 - Servlet API — o alicerce HTTP|Servlet API — o alicerce HTTP]] — o embedded server roda o Servlet container que a spec define; esta nota não repete a spec, apenas usa o contrato
- [[03-Dominios/Java/Spring Core e Boot/index|Spring Core e Boot (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Dicionário de Java#SpringApplication|SpringApplication]]
- [[03-Dominios/Java/Dicionário de Java#embedded server|embedded server]]
- [[03-Dominios/Java/Dicionário de Java#executable jar / fat jar|executable jar / fat jar]]

## Referências

- [Spring Boot Reference — SpringApplication](https://docs.spring.io/spring-boot/reference/features/spring-application.html)
- [Spring Boot Reference — Embedded Servlet Containers](https://docs.spring.io/spring-boot/reference/web/servlet.html)
