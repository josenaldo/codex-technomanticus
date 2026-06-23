---
title: "Capstone — Spring sob o capô"
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
  - "Capstone Spring"
  - "Spring sob o capô"
---

# Capstone — Spring sob o capô

> [!abstract] TL;DR
> A "mágica" do Spring é, na verdade, um **mecanismo previsível** que você pode rastrear passo a passo. Quando `run()` dispara, o container faz: **scanning** do classpath → cria **bean definitions** (metadados, não objetos) → aplica os **`BeanFactoryPostProcessor`** (que ainda mexem nas definitions) → **instancia** os beans → resolve a **DI** → passa cada bean pelos **`BeanPostProcessor`** (aqui nascem os **proxies** de AOP/transação) → chama **`@PostConstruct`** → e só então o **contexto está pronto**. Em cima desse motor, o Boot acrescenta a **auto-configuration**, que não é mágica nenhuma: é `@Conditional` (olha o classpath e os beans já existentes) somando-se a um catálogo de classes listadas no arquivo `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports`. Esta nota fecha o galho amarrando todo esse caminho — e mostra que cada conveniência do Spring tem uma **spec Jakarta EE** equivalente por baixo ou ao lado.

## O que é

Esta é a capstone do galho de **Spring Core e Boot**. Ela tem duas funções.

A primeira é **integradora**: as 16 notas anteriores dissecaram peças isoladas — IoC, beans, estereótipos, tipos de injeção, `@Configuration`/`@Bean`, `ApplicationContext`, ciclo de vida, qualificação, AOP, self-invocation, eventos, profiles, `BeanPostProcessor`/`BeanFactoryPostProcessor`, conditional beans, auto-configuration e starters. Cada uma respondeu "o que é esta peça". Esta nota responde a pergunta que **junta tudo**: quando você chama `SpringApplication.run(...)`, **o que acontece, em ordem, da chamada até o contexto pronto** — e onde, exatamente, nesse caminho, cada peça que você estudou se encaixa.

A segunda é **estratégica**: situar o Spring no mapa maior do Java enterprise. O Spring não nasceu no vácuo. Ele resolve os mesmos problemas que o **Jakarta EE** (galho 7) resolve com especificações — IoC, interceptação, transação, validação, eventos — só que com uma API própria, frequentemente **implementando ou consumindo as próprias specs Jakarta** por baixo. Saber traçar essa correspondência é o que separa "sei usar `@Autowired`" de "entendo o modelo de container que `@Autowired` instancia".

O frame central: **Spring é mecanismo, não mágica.** Tudo que parece automático tem um ponto de extensão nomeado, uma ordem definida e um ponto exato no ciclo de vida onde acontece. Esta nota é o mapa desse mecanismo.

## Por que importa

Em entrevista sênior, a diferença entre júnior e magus não é saber **que** o Spring injeta dependências — é saber **quando** e **como**. "Por que `@Transactional` não funciona quando um método chama outro método transacional da mesma classe?" só tem resposta se você souber que a transação é um **proxy criado por um `BeanPostProcessor`**, e que a auto-invocação não passa pelo proxy (galho 8, nota 10). "Por que meu `@Value` está nulo no construtor mas preenchido depois?" só tem resposta se você souber a ordem instanciação → DI → `@PostConstruct`.

Há também um motivo arquitetural. Quando você entende que a auto-configuration é só `@Conditional` + um arquivo de imports, você para de ter medo do Boot. Você sabe rodar com `--debug`, ler o **conditions report**, descobrir **por que** um bean foi (ou não foi) criado, e sobrescrever qualquer padrão definindo o seu próprio bean. O Boot deixa de ser uma caixa-preta e vira uma camada de conveniência **auditável**.

E há o motivo que conecta este galho ao 7: o entrevistador internacional frequentemente pergunta "Spring or Jakarta EE?". A resposta sênior **não é uma estatística de adoção** nem um torcedor de framework — é um **critério técnico** ("depende do runtime, do time, do grau de portabilidade que você precisa") somado à percepção de que **os dois resolvem os mesmos problemas** e o Spring **consome várias specs Jakarta** internamente. Esta nota arma você para essa conversa.

## Como funciona

### Da run() ao bean pronto: o caminho completo

A sequência abaixo é o coração desta capstone. Cada etapa corresponde a uma ou mais notas do galho. Baseline **Spring Boot 3.x**.

```text
SpringApplication.run(App.class, args)
        │
        ▼
┌─────────────────────────────────────────────────────────────┐
│ 1. CRIA o ApplicationContext                                 │  nota 06
│    (decide Servlet/Reactive/None pelo classpath)            │
└─────────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. COMPONENT SCANNING                                        │  notas 03, 05
│    varre o classpath em busca de @Component/@Service/        │
│    @Repository/@Controller/@Configuration                   │
└─────────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. BEAN DEFINITIONS                                          │  notas 05, 06
│    registra METADADOS de cada bean (classe, escopo,         │
│    dependências). Ainda NÃO há objetos instanciados.        │
└─────────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. BeanFactoryPostProcessor (BFPP)                          │  nota 13
│    pode AINDA alterar as bean definitions antes da           │
│    instanciação (ex.: resolver placeholders ${...},          │
│    é aqui que a AUTO-CONFIGURATION entra de fato)            │  nota 15
└─────────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. INSTANCIAÇÃO                                              │  notas 04, 07
│    o container chama o construtor de cada bean singleton     │
│    (injeção por construtor acontece AQUI)                    │
└─────────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────────┐
│ 6. POPULAÇÃO / DEPENDENCY INJECTION                         │  notas 02, 04, 08
│    resolve @Autowired de setter/field; aplica @Qualifier,   │
│    @Primary, @Profile para escolher candidatos               │
└─────────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────────┐
│ 7. BeanPostProcessor (BPP) — postProcessBeforeInitialization│  nota 13
│    ganchos ANTES da init: callbacks *Aware, etc.            │
│    (Ainda NÃO é aqui que os proxies AOP nascem.)            │
└─────────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────────┐
│ 8. @PostConstruct / InitializingBean / init-method          │  nota 07
│    callbacks de inicialização do bean (já com deps prontas) │
└─────────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────────┐
│ 8b. BeanPostProcessor — postProcessAfterInitialization      │  notas 09, 13
│     AQUI NASCEM OS PROXIES: AOP, @Transactional, @Async,    │
│     @Cacheable. O bean é ENVOLVIDO/SUBSTITUÍDO por um proxy │
│     que intercepta as chamadas.                             │
└─────────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────────┐
│ 9. CONTEXTO PRONTO                                           │  notas 06, 11
│    dispara ContextRefreshed/ApplicationReadyEvent;           │
│    sobe o servidor embutido (se web). App no ar.            │
└─────────────────────────────────────────────────────────────┘
```

Três observações que costumam aparecer em entrevista:

- **BFPP age sobre definitions; BPP age sobre instâncias.** O `BeanFactoryPostProcessor` (etapa 4) mexe nos **metadados** antes de qualquer objeto existir. O `BeanPostProcessor` (etapas 7 e 8b) recebe o **objeto já instanciado** e pode devolvê-lo envolvido num substituto — o proxy AOP nasce no gancho *after-initialization* (8b), **depois** do `@PostConstruct`. Confundir BFPP com BPP é erro clássico.
- **Injeção por construtor acontece na instanciação (5); por setter/field, na população (6).** Por isso a injeção por construtor garante o bean já nascer completo e imutável — o motivo técnico de ela ser a recomendada (nota 04).
- **O proxy é um wrapper.** Quando há AOP/transação, o bean que os outros recebem injetado **não é a instância original** — é o proxy. Isso explica a self-invocation (nota 10): uma chamada `this.metodo()` interna pula o proxy e, portanto, pula a transação.

### Onde a auto-configuration entra

A auto-configuration (notas 14 e 15) não é uma fase paralela mágica — ela se encaixa **dentro** do caminho acima, na fase de processamento de configuração (etapa 4, via os mecanismos de `@Configuration`/import que rodam antes da instanciação).

O mecanismo, no Boot 3.x:

1. `@SpringBootApplication` embute `@EnableAutoConfiguration`.
2. O Boot lê o catálogo de classes de auto-config no arquivo `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports` (o antigo `META-INF/spring.factories` **não vale mais** para isto desde o Boot 2.7/3.0).
3. Cada classe `@AutoConfiguration` listada é avaliada contra suas anotações **`@Conditional`** (nota 14): `@ConditionalOnClass` (a lib está no classpath?), `@ConditionalOnMissingBean` (você ainda não definiu este bean?), `@ConditionalOnProperty`, `@ConditionalOnWebApplication`, etc.
4. Só os beans cujas condições batem são registrados como bean definitions — e seguem o caminho normal a partir daí.

A consequência prática mais importante: **`@ConditionalOnMissingBean` é o que torna o Boot não-invasivo.** Se você definir sua própria `DataSource`, a auto-config recua. Você nunca fica preso ao padrão. E rodando com `--debug`, o **conditions report** lista o que foi aplicado e **por quê cada coisa foi ou não criada** — a prova de que não há mágica, só decisão condicional auditável.

### **Spring → Jakarta EE: dois caminhos pro mesmo problema**

O Spring e o Jakarta EE (galho 7) resolvem o mesmo conjunto de problemas enterprise. O Spring frequentemente **consome ou implementa** as próprias specs Jakarta por baixo (Servlet, Bean Validation, JPA, JMS via `jakarta.*` no baseline 6.x/Boot 3.x). A tabela abaixo cita apenas o **nome** da feature equivalente do lado Jakarta — a spec em si está explicada no galho 7.

| Problema | Spring | Jakarta EE (Galho 7) |
| --- | --- | --- |
| Container IoC / DI | IoC container (`ApplicationContext`, bean definitions) | CDI |
| Declarar injeção de dependência | `@Autowired` | `@Inject` |
| Interceptação / cross-cutting | AOP via proxy (`@Aspect`, `BeanPostProcessor`) | interceptors CDI (`@Interceptor` / `@AroundInvoke`) |
| Transação declarativa | `@Transactional` (abstração própria do Spring) | JTA |
| Validação declarativa | `@Validated` / `@Valid` | Bean Validation |
| Eventos no container | `@EventListener` (nota 11) | `@Observes` (eventos CDI) |
| Binding de configuração tipado | `@ConfigurationProperties` | (sem equivalente direto — o Spring vai além aqui) |

Duas leituras dessa tabela:

- **Onde há equivalência direta** (DI, injeção, interceptação, eventos), o Spring oferece uma API mais ergonômica para o mesmo conceito — e em vários pontos roda **sobre** as specs Jakarta (ele usa `jakarta.inject.@Inject` e `jakarta.annotation.@PostConstruct` como cidadãos de primeira classe).
- **Onde o Spring vai além** (`@ConfigurationProperties`, sua própria abstração de transação que não exige um gerenciador JTA completo), ele entrega conveniência que a plataforma pura não padroniza. Isso é parte do que explica sua adoção — não um número, mas uma **ergonomia**.

## Na prática

A pergunta "Spring ou Jakarta EE puro?" é de **critério técnico**, não de torcida nem de estatística. Quando cada um faz sentido:

**Inclina para o Spring (Boot) quando:**

- o time já domina o ecossistema e você quer **time-to-market** (starters, auto-config, `start.spring.io`);
- você precisa do ecossistema amplo (Data, Security, Cloud, Batch) integrado de fábrica;
- o runtime é flexível e um JAR executável com servidor embutido (Tomcat/Jetty/Netty) atende — o modelo padrão do Boot;
- você quer a abstração de transação leve (`@Transactional` sem precisar de um app server com JTA completo).

**Inclina para uma plataforma Jakarta EE pura (ou runtime cloud-native que a implementa direto) quando:**

- **portabilidade entre vendors** é um requisito real (você quer programar contra contratos do TCK, não contra a API de um único projeto);
- há mandato corporativo/regulatório por um app server certificado (WildFly, Open Liberty, Payara);
- o time já tem profundo investimento em CDI/JTA/JPA puros e migrar não agrega;
- você quer um runtime com **startup/footprint** otimizados que consome o Core Profile diretamente (Quarkus, Helidon) sem a camada do framework.

O ponto sênior: **não é um duelo de soma zero.** O Spring 6/Boot 3 roda **sobre** o namespace `jakarta.*`. Saber Jakarta (galho 7) é saber o que o Spring esconde; saber Spring é saber a camada de conveniência. A decisão real raramente é "um ou outro de forma absoluta" — é "qual camada de abstração o **requisito** (portabilidade, runtime, time, regulação) pede".

## Armadilhas

Três armadilhas **de raciocínio** — não de sintaxe. São os erros mentais que separam quem decorou de quem entendeu.

1. **"Auto-config é mágica / ela adivinha o que eu quero."**
   *Por que erra:* não há adivinhação. A auto-config é determinística: um catálogo de classes no arquivo `...AutoConfiguration.imports` avaliado contra `@Conditional` (classpath, beans existentes, properties). Quem trata como mágica não sabe **depurar**: não roda `--debug`, não lê o conditions report, e fica perdido quando um bean esperado não aparece. Quem entende o mecanismo sabe exatamente onde olhar.

2. **"O Spring substituiu / matou o Jakarta EE."**
   *Por que erra:* é uma meia-verdade datada. O que acabou foi a hegemonia do app server monolítico pesado como escolha-padrão — não as especificações. O Spring 6/Boot 3 **implementa e consome** várias specs Jakarta (`jakarta.servlet`, `jakarta.validation`, `jakarta.persistence`, `jakarta.inject`, `jakarta.annotation`). Dizer que ele substituiu o Jakarta é como dizer que um carro substituiu o motor: ele tem um motor de specs por dentro.

3. **Escolher framework por hype em vez de por requisito.**
   *Por que erra:* "todo mundo usa X" não é um critério de arquitetura — é apelo à popularidade. A escolha correta deriva de requisitos concretos: portabilidade entre vendors, runtime alvo, footprint/startup, expertise do time, mandatos regulatórios. Trocar requisito por hype é como escolher banco de dados pela quantidade de estrelas no GitHub. O sênior justifica a escolha com **trade-offs técnicos**, não com tendência.

## Em entrevista

### Frase pronta (inglês)

> Spring's "magic" is really just a well-defined mechanism. When the application starts, the IoC container scans the classpath, builds bean definitions, runs the `BeanFactoryPostProcessor`s over those definitions, instantiates the beans, injects dependencies, and then passes each bean through the `BeanPostProcessor`s — which is exactly where AOP and transactional proxies are created, before `@PostConstruct` runs and the context is ready. Spring Boot's auto-configuration sits on top of that: it's not magic, it's a list of `@AutoConfiguration` classes declared in the `AutoConfiguration.imports` file, each gated by `@Conditional` checks against the classpath and the beans you've already defined — which is why defining your own bean transparently overrides the default through `@ConditionalOnMissingBean`. And under the hood, Spring 6 runs on top of the Jakarta EE namespace, so it implements and consumes specs like Servlet, Bean Validation and `jakarta.inject` rather than replacing them.

### Vocabulário

| Termo PT | Termo EN |
| --- | --- |
| Inversão de controle | Inversion of Control (IoC) |
| Injeção de dependência | Dependency Injection (DI) |
| Definição de bean | Bean definition |
| Pós-processador de fábrica de beans | BeanFactoryPostProcessor |
| Pós-processador de bean | BeanPostProcessor |
| Proxy de interceptação | interception proxy |
| Auto-configuração | auto-configuration |
| Avaliação condicional | conditional evaluation |
| Programação orientada a aspectos | Aspect-Oriented Programming (AOP) |
| Auto-invocação | self-invocation |
| Contexto da aplicação | application context |

### Cheatsheet

Mapa **dúvida → nota** do galho (qual nota resolve qual pergunta):

| Se a dúvida é... | A nota é |
| --- | --- |
| "o que é Spring vs Boot vs ecossistema?" | [[03-Dominios/Tecnologia/Java/Spring Core e Boot/01 - O que é Spring — Framework, Boot e o ecossistema\|01]] |
| "como o container injeta dependências?" | [[03-Dominios/Tecnologia/Java/Spring Core e Boot/02 - IoC e injeção de dependência no Spring\|02]] |
| "quando uso @Service vs @Component?" | [[03-Dominios/Tecnologia/Java/Spring Core e Boot/03 - Beans e estereótipos — @Component, @Service, @Repository, @Controller\|03]] |
| "construtor, setter ou field injection?" | [[03-Dominios/Tecnologia/Java/Spring Core e Boot/04 - Tipos de injeção — constructor, setter, field\|04]] |
| "como definir um bean explicitamente?" | [[03-Dominios/Tecnologia/Java/Spring Core e Boot/05 - @Configuration e @Bean — definição explícita de beans\|05]] |
| "o que é o ApplicationContext e seu ciclo?" | [[03-Dominios/Tecnologia/Java/Spring Core e Boot/06 - ApplicationContext — o container e seu ciclo\|06]] |
| "ordem do ciclo de vida e escopos?" | [[03-Dominios/Tecnologia/Java/Spring Core e Boot/07 - Ciclo de vida e escopos de beans\|07]] |
| "dois candidatos, qual o Spring escolhe?" | [[03-Dominios/Tecnologia/Java/Spring Core e Boot/08 - Qualificação de beans — @Qualifier, @Primary, @Profile\|08]] |
| "como o AOP/proxy funciona?" | [[03-Dominios/Tecnologia/Java/Spring Core e Boot/09 - AOP e proxies no Spring\|09]] |
| "por que @Transactional não pegou nesta chamada?" | [[03-Dominios/Tecnologia/Java/Spring Core e Boot/10 - Self-invocation e os limites do proxy\|10]] |
| "como reagir a eventos do contexto?" | [[03-Dominios/Tecnologia/Java/Spring Core e Boot/11 - Eventos do ApplicationContext\|11]] |
| "como separar config por ambiente?" | [[03-Dominios/Tecnologia/Java/Spring Core e Boot/12 - Configuração e profiles\|12]] |
| "onde a auto-config mexe nas definitions?" | [[03-Dominios/Tecnologia/Java/Spring Core e Boot/13 - BeanPostProcessor e BeanFactoryPostProcessor\|13]] |
| "como condicionar um bean ao classpath?" | [[03-Dominios/Tecnologia/Java/Spring Core e Boot/14 - Conditional beans — @Conditional e os @ConditionalOn\|14]] |
| "como o Boot configura tudo sozinho?" | [[03-Dominios/Tecnologia/Java/Spring Core e Boot/15 - Auto-configuration e starters\|15]] |

## Veja também

- [[03-Dominios/Tecnologia/Java/Spring Core e Boot/02 - IoC e injeção de dependência no Spring|IoC e injeção de dependência no Spring]] — o motor de DI que esta capstone rastreia
- [[03-Dominios/Tecnologia/Java/Spring Core e Boot/09 - AOP e proxies no Spring|AOP e proxies no Spring]] — onde os proxies da etapa 7 nascem
- [[03-Dominios/Tecnologia/Java/Spring Core e Boot/13 - BeanPostProcessor e BeanFactoryPostProcessor|BeanPostProcessor e BeanFactoryPostProcessor]] — os dois pontos de extensão centrais do ciclo
- [[03-Dominios/Tecnologia/Java/Spring Core e Boot/15 - Auto-configuration e starters|Auto-configuration e starters]] — o detalhe completo da camada do Boot
- [[03-Dominios/Tecnologia/Java/Jakarta EE/14 - Jakarta EE hoje — a plataforma sob o Spring|Jakarta EE hoje — a plataforma sob o Spring]] — a capstone contraparte do Galho 7
- [[03-Dominios/Tecnologia/Java/Jakarta EE/index|Jakarta EE]]
- [[03-Dominios/Tecnologia/Java/Spring Core e Boot/index|Spring Core e Boot (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]

## Referências

- Spring Framework — Overview: https://docs.spring.io/spring-framework/reference/overview.html
- Spring Boot — Auto-configuration: https://docs.spring.io/spring-boot/reference/using/auto-configuration.html
- Spring Boot — Creating Your Own Auto-configuration (mecanismo `.imports`): https://docs.spring.io/spring-boot/reference/features/developing-auto-configuration.html
