---
title: "Dicionário de Java"
created: 2026-06-02
updated: 2026-06-12
type: glossary
status: growing
publish: true
tags:
  - java
  - glossary
  - moc
aliases:
  - Glossário de Java
---

# Dicionário de Java

> Glossário do domínio Java: termos de linguagem, plataforma e ecossistema. Semeado com o Galho 1 — Linguagem e sintaxe moderna; cresce a cada galho incorporado.

<!--
Como usar este glossário:

- Cada verbete é um `###` dentro de uma `##` temática (seção alfabética).
- Verbetes em ordem alfabética dentro de cada seção; ordenação case-insensitive, sem considerar acento.
- Linkar de outra nota: wikilink para este arquivo com âncora `#` + nome do termo.
- Customizar o texto exibido: adicionar o pipe `|` após a âncora, seguido do texto.
- A skill /verbete adiciona termos automaticamente em ordem alfabética.
- Cada verbete tem (i) 1-3 frases de definição em PT-BR e (ii) "Veja também:" com wikilinks para a(s) nota(s) que aprofundam.
-->

## A

### AAA (Arrange-Act-Assert)
Estrutura de um teste em três blocos: **Arrange** (prepara o cenário/given), **Act** (executa a ação/when), **Assert** (verifica o resultado/then). Torna o teste legível em segundos.

Veja também: [[03-Dominios/Java/Testes/02 - JUnit 5 — anatomia, lifecycle e o padrão AAA|JUnit 5]].

### ABA problem
Anomalia em algoritmos lock-free onde um valor lido como A é alterado para B e de volta para A antes do CAS ser executado, fazendo o CAS ter sucesso incorretamente. A thread acredita que nada mudou, mas o estado intermediário pode ter corrompido invariantes. Solucionado com estampilhas de versão (ex: `AtomicStampedReference`).

Veja também: [[06 - Atômicos e operações lock-free]].

### ABAC (attribute-based)
Modelo de autorização que decide o acesso por **atributos** (do usuário, do recurso, do contexto) em vez de papéis fixos; no Spring Security expressa-se via SpEL. Mais flexível que o RBAC, porém mais difícil de auditar.

Veja também: [[03-Dominios/Java/Segurança/14 - Autorização avançada — AuthorizationManager, RBAC vs ABAC|Autorização avançada]].

### ack mode (Spring Kafka)
Controla quando o offset de uma mensagem consumida é confirmado (committed) de volta ao broker. Os modos principais são `RECORD` (após cada registro), `BATCH` (após o lote inteiro), `MANUAL` e `MANUAL_IMMEDIATE` (o código chama `Acknowledgment.acknowledge()` explicitamente). O modo adequado influencia a semântica de entrega e o comportamento em caso de falha.

Veja também: [[03-Dominios/Java/Mensageria/10 Ack modes e commit de offset|Ack modes e commit de offset]].

### Action API
`Action`/`AbstractAction` encapsulam um comportamento e seu estado (`enabled`, texto, ícone, accelerator key) em um único objeto reutilizável. O mesmo objeto pode ser plugado em botão, item de menu e toolbar, mantendo todos sincronizados automaticamente.

Veja também: [[03-Dominios/Java/Swing/11 - Action API, key bindings e performance|Action API]].

### adapter (event adapter)
Classe abstrata (ex.: `MouseAdapter`) que implementa um listener com métodos vazios, permitindo sobrescrever apenas os eventos de interesse, sem ter que implementar todos os métodos da interface.

Veja também: [[03-Dominios/Java/Swing/04 - O modelo de eventos|Modelo de eventos]].

### advice (Spring AOP)
A ação que um aspecto executa, associada a um pointcut: define *o quê* fazer e *quando* (`@Before`, `@After`, `@AfterReturning`, `@AfterThrowing`, `@Around`). O `@Around` é o mais poderoso — recebe um `ProceedingJoinPoint` e decide se e quando chama o método interceptado.

Veja também: [[03-Dominios/Java/Spring Core e Boot/09 - AOP e proxies no Spring|AOP e proxies no Spring]].

### alg: none (ataque JWT)
Ataque em que o header do token traz `"alg":"none"`, pedindo que o servidor aceite um JWT **sem assinatura**; uma biblioteca ingênua valida e o atacante forja qualquer claim. Defesa: whitelist explícita de algoritmos.

Veja também: [[03-Dominios/Java/Segurança/08 - JWT — estrutura, assinatura e validação|JWT]].

### ambient mesh
Modo do Istio que dispensa o sidecar por pod: um `ztunnel` por nó cuida do tráfego L4 (mTLS, identidade) e um `waypoint` opcional aplica políticas L7. Reduz o overhead de recursos e a complexidade de injeção de sidecar.

Veja também: [[03-Dominios/Java/Microservices e sistemas distribuídos/22 - Service mesh — quando a resiliência sai do código|Service mesh]].

### AMQP
Advanced Message Queuing Protocol: protocolo aberto de mensageria orientado a filas, com suporte a exchanges, bindings e filas. O RabbitMQ é a implementação de referência na JVM; o Spring AMQP abstrai a API de baixo nível do cliente Java (rabbitmq-client) com template e listener container.

Veja também: [[03-Dominios/Java/Mensageria/15 Spring AMQP e RabbitMQ|Spring AMQP e RabbitMQ]].

### API Gateway
Porta única de entrada de um sistema de microservices: roteia requisições para os serviços internos e centraliza preocupações transversais (autenticação, rate limiting, CORS, agregação). Esconde a topologia interna do cliente.

Veja também: [[03-Dominios/Java/Microservices e sistemas distribuídos/10 - API Gateway — papel, roteamento, predicates e filters|API Gateway]].

### API versioning
Estratégias para evoluir uma API sem quebrar clientes existentes: versão na URI (`/v1/...`), em header customizado, via content negotiation (media type versionado) ou query param. Cada abordagem tem trade-offs de visibilidade, cacheabilidade e aderência ao REST; o Spring MVC suporta todas via atributos de `@RequestMapping` (path, headers, params, produces).

Veja também: [[03-Dominios/Java/Web e APIs REST/13 - Versionamento de API|Versionamento de API]].

### ApplicationContext
A interface central do container Spring: estende `BeanFactory` e adiciona resolução de mensagens i18n, publicação de eventos, carregamento de recursos e integração com a hierarquia de contextos. É o objeto que instancia, configura e gerencia o ciclo de vida de todos os beans da aplicação.

Veja também: [[03-Dominios/Java/Spring Core e Boot/06 - ApplicationContext — o container e seu ciclo|ApplicationContext — o container e seu ciclo]].

### ArchUnit
Biblioteca que expressa regras de arquitetura como testes JUnit (dependências entre camadas, ausência de ciclos, convenções) — fitness functions que falham o build no drift arquitetural.

Veja também: [[03-Dominios/Java/Testes/19 - Fitness functions — ArchUnit (testes de arquitetura)|Fitness functions — ArchUnit]].

### ArgumentCaptor
Recurso do Mockito que captura o argumento passado a um mock (`captor.capture()`/`getValue()`), permitindo asserções detalhadas sobre o que o código sob teste enviou.

Veja também: [[03-Dominios/Java/Testes/07 - Mockito — verify, ArgumentCaptor e quando NÃO mockar|Mockito: verify e ArgumentCaptor]].

### artifact (artefato Maven)
A unidade que um build produz ou consome — tipicamente um `jar`, `war` ou o próprio `pom` — identificada de forma única por suas coordenadas GAV (groupId:artifactId:version) no repositório.

Veja também: [[03-Dominios/Java/Build e tooling/02 - Maven — POM, coordenadas e lifecycle|Maven — coordenadas]].

### aspect
Módulo que encapsula uma preocupação transversal (cross-cutting concern) no AOP, combinando pointcuts (onde) e advices (o quê). No Spring, declarado com `@Aspect` sobre um bean; agrupa a lógica de logging, segurança ou transações que de outra forma se espalharia por todo o código.

Veja também: [[03-Dominios/Java/Spring Core e Boot/09 - AOP e proxies no Spring|AOP e proxies no Spring]].

### assembly time / subscription time
As duas fases de um pipeline reativo: montar a cadeia de operadores (*assembly time*) não executa nada; só o `subscribe` (*subscription time*) dispara o fluxo. Erros de montagem aparecem cedo; o trabalho real só acontece na subscription.

Veja também: [[03-Dominios/Java/Programação Reativa/04 - Nada acontece até o subscribe — lazy, assembly vs subscription, cold vs hot|Nada acontece até o subscribe]].

### AssertJ
Biblioteca de asserções fluent (`assertThat(x).isNotNull().hasSize(3)`) com mensagens de erro claras; o padrão moderno, mais legível que o JUnit built-in/Hamcrest.

Veja também: [[03-Dominios/Java/Testes/03 - AssertJ — fluent assertions|AssertJ]].

### async-profiler
Profiler de baixo overhead para a JVM que amostra via `perf_events` do kernel Linux, produzindo saída em flamegraph ou JFR. Captura stacks de CPU, alocação e contenção de locks sem o viés de safepoint dos profilers tradicionais.

Veja também: [[03-Dominios/Java/Cloud-native e produção/19 - Continuous profiling no cluster — Pyroscope e async-profiler|Continuous profiling no cluster]].

### at-least-once
Garantia de entrega em que uma mensagem é processada **uma ou mais vezes**: o broker retransmite em caso de falha ou falta de ACK, podendo gerar duplicatas. É a garantia mais comum em sistemas de mensageria; exige que o consumidor seja **idempotente** para lidar com reprocessamento.

Veja também: [[03-Dominios/Java/Mensageria/03 Garantias de entrega — e a falácia do exactly-once|Garantias de entrega]].

### at-most-once
Garantia de entrega em que uma mensagem é processada **no máximo uma vez**: o broker não retransmite em caso de falha, podendo haver perda de mensagens. Oferece a menor latência e overhead, sendo adequada para dados onde perda ocasional é tolerável (logs, métricas em alta frequência).

Veja também: [[03-Dominios/Java/Mensageria/03 Garantias de entrega — e a falácia do exactly-once|Garantias de entrega]].

### Atomic (variável atômica)
Variável que suporta operações de leitura, escrita e atualização compostas sem necessidade de `synchronized`, usando instruções CAS do hardware. O pacote `java.util.concurrent.atomic` oferece `AtomicInteger`, `AtomicLong`, `AtomicReference` e variantes. Garante atomicidade sem bloquear threads.

Veja também: [[06 - Atômicos e operações lock-free]].

### AuthenticationManager
Ponto central da autenticação no Spring Security: recebe um `Authentication` não-autenticado e devolve um autenticado (ou lança exceção); a implementação padrão `ProviderManager` delega a uma cadeia de `AuthenticationProvider`.

Veja também: [[03-Dominios/Java/Segurança/03 - Autenticação — UserDetailsService, AuthenticationManager, Form e Basic|Autenticação]].

### @AuthenticationPrincipal
Anotação que injeta o principal autenticado (`UserDetails`, `Jwt` ou `OidcUser`) direto num parâmetro do controller.

Veja também: [[03-Dominios/Java/Segurança/02 - SecurityContext, Authentication e Principal — o usuário atual|SecurityContext, Authentication e Principal]].

### AuthenticationProvider
Estratégia que sabe autenticar um tipo específico de credencial; o `DaoAuthenticationProvider` usa um `UserDetailsService` + `PasswordEncoder`.

Veja também: [[03-Dominios/Java/Segurança/03 - Autenticação — UserDetailsService, AuthenticationManager, Form e Basic|Autenticação]].

### AuthorizationManager
Interface (Spring Security 6) que decide uma autorização de forma programática; usada com `.access(...)` para lógica custom além de `hasRole`/SpEL.

Veja também: [[03-Dominios/Java/Segurança/14 - Autorização avançada — AuthorizationManager, RBAC vs ABAC|Autorização avançada]].

### authorizeHttpRequests
DSL atual (Spring Security 6) para autorização baseada em URL; substituiu `authorizeRequests`. Casa requests com `requestMatchers` e exige `permitAll`/`authenticated`/`hasRole`/`hasAuthority`.

Veja também: [[03-Dominios/Java/Segurança/05 - Autorização baseada em URL — authorizeHttpRequests, roles vs authorities|Autorização baseada em URL]].

### Autoboxing
Conversão automática entre tipos primitivos (ex: `int`) e seus wrappers (`Integer`) feita pelo compilador Java. O processo inverso — de wrapper para primitivo — chama-se *unboxing*. Pode causar `NullPointerException` e overhead de alocação se usado em laços intensivos.

Veja também: [[02 - Tipos, variáveis e operadores]].

### auto-configuration
Mecanismo do Spring Boot que configura beans automaticamente com base no que está no classpath e nas propriedades definidas, aplicando *convention over configuration*. Classes de auto-configuração (anotadas com `@AutoConfiguration` + `@ConditionalOnX`) entram em ação só quando suas condições são satisfeitas, e cedem lugar a beans definidos pelo usuário.

Veja também: [[03-Dominios/Java/Spring Core e Boot/15 - Auto-configuration e starters|Auto-configuration e starters]].

### @Autowired
Annotation do Spring (`org.springframework.beans.factory.annotation.Autowired`) que marca um ponto de injeção — construtor, campo ou método. O container resolve a dependência por tipo (e desambigua com `@Qualifier`/`@Primary`). Desde o Spring 4.3 é opcional em construtores únicos. Alfabetiza como "Autowired".

Veja também: [[03-Dominios/Java/Spring Core e Boot/02 - IoC e injeção de dependência no Spring|IoC e injeção de dependência no Spring]].

### Awaitility
Biblioteca para testar condições eventuais/assíncronas com polling declarativo (`await().atMost(...).untilAsserted(...)`), substituindo o `Thread.sleep` que causa flakiness.

Veja também: [[03-Dominios/Java/Testes/14 - Testando código assíncrono — Awaitility|Testando código assíncrono]].

### AWT (Abstract Window Toolkit)
Toolkit de GUI original do Java, com componentes heavyweight que têm peers nativos do sistema operacional. O Swing é construído sobre o AWT e o estende com componentes lightweight de renderização puramente Java.

Veja também: [[03-Dominios/Java/Swing/01 - O modelo do Swing|Modelo do Swing]].

### Avro
Formato de serialização binária criado pela Apache, amplamente usado com Kafka. Define schemas em JSON que descrevem a estrutura dos dados; ao contrário do JSON/XML, os dados em Avro são binários e compactos. A separação schema/dado permite evolução compatível e integração com o Schema Registry.

Veja também: [[03-Dominios/Java/Mensageria/14 Schema e contratos — Avro e Schema Registry|Schema e contratos — Avro e Schema Registry]].

## B

### backpressure
Mecanismo do Reactive Streams em que o consumidor controla a demanda (`request(n)`), impedindo o produtor de empurrar mais elementos do que ele consegue processar. É o que torna o modelo reativo seguro sob carga, em contraste com o push cego.

Veja também: [[03-Dominios/Java/Programação Reativa/09 - Backpressure — request(n) e as estratégias BUFFER, DROP, LATEST|Backpressure]]. Para o controle de fluxo entre serviços, veja [[#backpressure distribuído|backpressure distribuído]].

### backpressure distribuído
Controle de fluxo entre serviços: impedir que um produtor sobrecarregue um consumidor mais lento ao longo da rede, propagando a pressão para trás. Diferente do backpressure intra-processo do Reactive Streams, depende de filas, rate limiting e padrões de resiliência para não derrubar a cadeia.

Veja também: [[03-Dominios/Java/Microservices e sistemas distribuídos/21 - Os padrões de falha distribuída|Os padrões de falha distribuída]], [[#backpressure|backpressure (Reactive Streams)]].

### Barrier (CyclicBarrier)
Ponto de sincronização onde um número fixo de threads deve se encontrar antes que qualquer uma prossiga. Ao contrário do `CountDownLatch`, o `CyclicBarrier` pode ser reutilizado após cada ciclo. Útil em algoritmos paralelos com fases distintas.

Veja também: [[09 - Sincronizadores]].

### BCryptPasswordEncoder
Implementação de `PasswordEncoder` baseada no algoritmo BCrypt: hash adaptativo com work factor ajustável, slow-by-design contra força bruta. Default razoável no Spring Security.

Veja também: [[03-Dominios/Java/Segurança/04 - Password encoding — BCrypt, Argon2 e o DelegatingPasswordEncoder|Password encoding]].

### @Bean
Annotation do Spring (`org.springframework.context.annotation.Bean`) aplicada a um método dentro de uma classe `@Configuration`: o valor retornado pelo método é registrado como bean no container. É a definição *explícita e programática* de beans — alternativa ao component scanning, útil para configurar objetos de bibliotecas de terceiros. Alfabetiza como "Bean".

Veja também: [[03-Dominios/Java/Spring Core e Boot/05 - @Configuration e @Bean — definição explícita de beans|@Configuration e @Bean]].

### bean (CDI)
No CDI, qualquer classe Java que o container consegue instanciar e gerenciar — descoberta por bean discovery, com ciclo de vida e injeção controlados pelo container. Inclui managed beans (classes concretas com construtor adequado) e objetos fabricados por `@Produces`.

Veja também: [[03-Dominios/Java/Jakarta EE/04 - CDI — beans e injeção|CDI — beans e injeção]].

### bean discovery / beans.xml
Processo pelo qual o container CDI varre o classpath e decide quais classes viram beans. No CDI 4 o modo padrão é `annotated` (só classes com bean defining annotation); `all` descobre todas. O arquivo `beans.xml` (opcional) ajusta o modo e ativa alternatives/interceptors.

Veja também: [[03-Dominios/Java/Jakarta EE/04 - CDI — beans e injeção|CDI — beans e injeção]].

### bean scope (Spring)
Define quantas instâncias de um bean o container cria e por quanto tempo vivem. O padrão é `singleton` (uma instância por container); `prototype` cria uma nova a cada injeção/lookup. Escopos web (`request`, `session`, `application`, `websocket`) ligam a vida do bean ao ciclo HTTP. Configurado com `@Scope`.

Veja também: [[03-Dominios/Java/Spring Core e Boot/07 - Ciclo de vida e escopos de beans|Ciclo de vida e escopos de beans]].

### Bean Validation (Jakarta Validation)
Especificação de validação declarativa (Jakarta Validation 3.1 no EE 11): restrições como `@NotNull`/`@Size`/`@Pattern` anotadas no modelo e checadas por um `Validator`. Integra-se a CDI e JAX-RS; a implementação de referência é o Hibernate Validator.

Veja também: [[03-Dominios/Java/Jakarta EE/08 - Bean Validation|Bean Validation]].

### BeanFactory
A interface raiz do container Spring (`org.springframework.beans.factory.BeanFactory`): define o contrato mínimo de IoC — instanciar, configurar e fornecer beans sob demanda (lazy). O `ApplicationContext` é um superset que adiciona recursos enterprise. Raramente usado diretamente; é a base sobre a qual o container completo é construído.

Veja também: [[03-Dominios/Java/Spring Core e Boot/06 - ApplicationContext — o container e seu ciclo|ApplicationContext — o container e seu ciclo]].

### BeanFactoryPostProcessor
Hook de extensão do container que opera sobre as *definições* de bean (metadados) antes que qualquer bean seja instanciado. Permite modificar a configuração programaticamente — o exemplo clássico é o `PropertySourcesPlaceholderConfigurer`, que resolve placeholders `${...}`. Atua antes do `BeanPostProcessor`.

Veja também: [[03-Dominios/Java/Spring Core e Boot/13 - BeanPostProcessor e BeanFactoryPostProcessor|BeanPostProcessor e BeanFactoryPostProcessor]].

### BeanPostProcessor
Hook de extensão que intercepta cada bean *já instanciado*, antes e depois da inicialização (`postProcessBeforeInitialization`/`postProcessAfterInitialization`). É o mecanismo por baixo de boa parte da mágica do Spring — `@Autowired`, `@Async` e os proxies de `@Transactional` são aplicados por BeanPostProcessors.

Veja também: [[03-Dominios/Java/Spring Core e Boot/13 - BeanPostProcessor e BeanFactoryPostProcessor|BeanPostProcessor e BeanFactoryPostProcessor]].

### BearerTokenAuthenticationFilter
Filtro do Resource Server que extrai o token do header `Authorization: Bearer ...`, valida e popula o `SecurityContext`; é o ponto de entrada de uma request autenticada por JWT.

Veja também: [[03-Dominios/Java/Segurança/09 - OAuth2 Resource Server — validando JWT na API|OAuth2 Resource Server]].

### binding (JavaFX)
Mecanismo de sincronização declarativa entre `Property` observáveis: `propA.bind(propB)` faz com que `propA` se atualize automaticamente sempre que `propB` mudar. Bindings unidirecionais (`bind`) e bidirecionais (`bindBidirectional`) eliminam listeners manuais; bindings podem ser compostos com `Bindings.*` para expressar expressões aritméticas ou booleanas.

Veja também: [[07 - Properties e binding]].

### BlockingQueue
Interface de fila thread-safe que bloqueia o produtor quando a fila está cheia e o consumidor quando está vazia, sem necessidade de `wait/notify` manuais. Implementações incluem `ArrayBlockingQueue`, `LinkedBlockingQueue` e `SynchronousQueue`. Pedra angular do padrão produtor-consumidor.

Veja também: [[07 - Concurrent collections]].

### BOM (Bill of Materials)
POM especial que contém apenas uma seção `dependencyManagement` e é importado com `<scope>import</scope>`, alinhando as versões de um conjunto coeso de bibliotecas sem declará-las como dependências diretas.

Veja também: [[03-Dominios/Java/Build e tooling/11 - BOM e dependency management|BOM e dependency management]].

### bounded context
Conceito do DDD: uma fronteira explícita dentro da qual um modelo de domínio é coeso e consistente. É o critério natural para dividir um sistema em microservices — cada serviço deve possuir um bounded context, não uma entidade isolada.

Veja também: [[03-Dominios/Java/Microservices e sistemas distribuídos/01 - O que são microservices e a tese honesta|O que são microservices]], [[03-Dominios/Java/Microservices e sistemas distribuídos/23 - Quando NÃO fazer microservices|Quando NÃO fazer microservices]].

### boundedElastic (Scheduler)
`Scheduler` do Reactor com pool elástico mas limitado, destinado a isolar chamadas BLOQUEANTES (JDBC, I/O legado) para que não travem o event loop. Cada tarefa bloqueante roda numa thread dedicada e descartável, em vez de prender um worker do event loop.

Veja também: [[03-Dominios/Java/Programação Reativa/08 - Schedulers — subscribeOn, publishOn e em qual thread o código roda|Schedulers]].

### Brave (tracer)
Tracer da família OpenZipkin usado pelo Micrometer Tracing através do bridge `micrometer-tracing-bridge-brave`. Instrumenta a propagação de contexto (traceId/spanId) e exporta spans para o Zipkin ou compatíveis.

Veja também: [[03-Dominios/Java/Microservices e sistemas distribuídos/19 - Tracing distribuído II — exportando o trace|Tracing distribuído II — exportando o trace]].

### broker (mensageria)
Servidor intermediário que recebe mensagens de produtores, as armazena em filas ou tópicos e as entrega a consumidores. Desacopla produtores de consumidores no tempo e no espaço. Exemplos de brokers JVM-friendly: Apache Kafka (log distribuído), RabbitMQ (AMQP), ActiveMQ (JMS).

Veja também: [[03-Dominios/Java/Mensageria/04 O ecossistema de brokers na JVM|O ecossistema de brokers na JVM]].

### boxing / unboxing
Conversão automática entre tipos primitivos (`int`, `long`, `double`…) e seus wrappers (`Integer`, `Long`, `Double`…): *boxing* empacota o primitivo num objeto; *unboxing* extrai o primitivo do wrapper. Feita implicitamente pelo compilador (autoboxing), mas introduz overhead de alocação e risco de `NullPointerException` em unboxing de referência `null`. Relevante em streams primitivos (`IntStream`), que evitam esse custo.

Veja também: [[03-Dominios/Java/Collections e Streams/09 - Streams primitivos|Streams primitivos]].

### build cache (Gradle)
Cache que reusa os outputs de tasks já executadas — entre builds, máquinas e até no CI — chaveado por um hash dos inputs da task. Diferente do build incremental (local à máquina), pode ser remoto e compartilhado pelo time.

Veja também: [[03-Dominios/Java/Build e tooling/07 - Gradle — performance, build cache e daemon|Gradle — performance e build cache]].

### Buildpacks (Cloud Native Buildpacks)
Especificação que transforma código-fonte diretamente em imagem OCI, sem Dockerfile, detectando a stack e aplicando camadas otimizadas. O Paketo é a implementação usada pelo Spring Boot via `spring-boot:build-image`.

Veja também: [[03-Dominios/Java/Cloud-native e produção/06 - Buildpacks — imagem sem Dockerfile|Buildpacks — imagem sem Dockerfile]].

### bulkhead
Padrão de resiliência (anteparo) que isola recursos — pools de threads ou semáforos — por dependência, de modo que a saturação de uma chamada lenta não consuma toda a capacidade do serviço e derrube as demais. Inspirado nos compartimentos estanques de um navio.

Veja também: [[03-Dominios/Java/Microservices e sistemas distribuídos/15 - Resiliência III — Bulkhead e Rate Limiter|Resiliência III — Bulkhead e Rate Limiter]].

### Bytecode
Representação intermediária compilada pelo `javac` a partir do código-fonte `.java`, gravada em arquivos `.class`. Não é código de máquina nativo: é executado (ou JIT-compilado) pela JVM, o que viabiliza o princípio WORA.

Veja também: [[01 - O modelo da linguagem Java]], [[04 - Bytecode por dentro — anatomia e javap]].

## C

### @Cacheable / Spring Cache
Abstração de cache do Spring aplicada em métodos (`@Cacheable`, `@CacheEvict`, `@CachePut`), na camada de serviço, acima da JPA — com providers como Caffeine, Redis ou Hazelcast. Diferente do cache de 2º nível do Hibernate (que cacheia entidades). Veja também: [[03-Dominios/Java/Persistência de dados/14 - Caching — 1º nível, 2º nível e Spring Cache|Caching]].

### Canvas (JavaFX)
Nó de modo imediato do JavaFX que expõe uma API de desenho 2D (via `GraphicsContext`) semelhante ao HTML5 Canvas. Todo o conteúdo é rasterizado em um bitmap; não há grafo de cena interno — o desenvolvedor é responsável por redesenhar a área afetada. Indicado para gráficos dinâmicos de alta frequência (simulações, jogos simples).

Veja também: [[12 - Custom controls, Canvas e charts]].

### CAP theorem
Teorema de Brewer: em um sistema distribuído, sob uma partição de rede (P) é impossível garantir simultaneamente consistência (C) e disponibilidade (A) — é preciso escolher entre CP e AP. Orienta decisões de design em sistemas distribuídos.

Veja também: [[03-Dominios/Java/Microservices e sistemas distribuídos/20 - Consistência em sistemas distribuídos|Consistência em sistemas distribuídos]].

### Carrier thread
Thread da plataforma (OS thread) que executa uma virtual thread no modelo de virtual threads do Java. Uma virtual thread é montada sobre um carrier thread durante sua execução e desmontada ao bloquear, liberando o carrier para executar outra virtual thread.

Veja também: [[12 - Virtual Threads e Project Loom]].

### CAS (compare-and-swap)
Instrução atômica de hardware que compara o valor atual de uma posição de memória com um valor esperado e, somente se forem iguais, substitui pelo novo valor — tudo em uma única operação indivisível. Base de todos os algoritmos lock-free em Java. Exposto pela API `Unsafe` e pelas classes `Atomic*`.

Veja também: [[06 - Atômicos e operações lock-free]].

### cascade / orphanRemoval
`cascade` propaga operações (PERSIST, MERGE, REMOVE, ALL) do lado pai para o filho de uma associação. `orphanRemoval = true` apaga o filho quando ele é removido da coleção do pai — vai além do `cascade = REMOVE`. Veja também: [[03-Dominios/Java/Persistência de dados/06 - @ManyToMany, @OneToOne, cascade e orphanRemoval|@ManyToMany, @OneToOne, cascade e orphanRemoval]].

### cascading failure
Falha em cascata: uma falha (ou lentidão) em um serviço se propaga pelas chamadas encadeadas, esgotando threads e recursos dos chamadores até derrubar boa parte do sistema. É a falha distribuída que circuit breaker, timeout e bulkhead existem para conter.

Veja também: [[03-Dominios/Java/Microservices e sistemas distribuídos/21 - Os padrões de falha distribuída|Os padrões de falha distribuída]].

### CDC (Change Data Capture)
Técnica que captura eventos de mudança de dados diretamente do log de transações do banco (ex.: binlog do MySQL, WAL do Postgres) e os publica como mensagens em um tópico. Permite sincronizar sistemas sem polling e sem acoplar o banco ao código da aplicação. O Debezium é o conector CDC de referência na JVM.

Veja também: [[03-Dominios/Java/Mensageria/21 O padrão Outbox|O padrão Outbox]].

### CDI (Contexts and Dependency Injection)
Especificação de injeção de dependência e gerenciamento de contextos da plataforma Jakarta (CDI 4.1 no EE 11). O container resolve e injeta dependências por tipo + qualifiers, gerencia escopos e habilita interceptors, decorators e eventos. É a spec que o `@Autowired` de frameworks esconde.

Veja também: [[03-Dominios/Java/Jakarta EE/04 - CDI — beans e injeção|CDI — beans e injeção]].

### cell editor
Componente temporário que entra em ação quando o usuário edita uma célula de `JTable`. Implementa `TableCellEditor` (ex.: `DefaultCellEditor` com `JComboBox`); confirma o valor editado via `stopCellEditing` e o devolve ao model.

Veja também: [[03-Dominios/Java/Swing/08 - Renderers e editors|Renderers e editors]].

### cell factory / cell value factory
Em `TableColumn` do JavaFX, `cellValueFactory` extrai o valor a exibir de cada item de linha (retorna uma `ObservableValue`), e `cellFactory` cria o nó visual que renderiza esse valor. A célula (`TableCell`) é **reutilizada** pela `ListView`/`TableView` — deve-se sobrescrever `updateItem` para evitar artefatos de reuso.

Veja também: [[08 - TableView, cell factories e dados observáveis]].

### cell renderer
Objeto responsável por desenhar o conteúdo de cada célula ou item de `JTable`/`JList`, implementando `TableCellRenderer` ou `ListCellRenderer`. Reutilizado para pintar todas as células (rubber-stamp), por isso deve ser stateless.

Veja também: [[03-Dominios/Java/Swing/08 - Renderers e editors|Renderers e editors]].

### Central Portal
Serviço atual da Sonatype para publicar artefatos no Maven Central, que substituiu o OSSRH (legacy) em 2025. Centraliza namespace verification, upload e release dos componentes.

Veja também: [[03-Dominios/Java/Build e tooling/19 - Publicação de artefatos|Publicação de artefatos]].

### CGLIB
Biblioteca de geração de bytecode que o Spring usa para criar proxies via *subclasse* quando o bean-alvo não implementa interface alguma. Diferente do JDK dynamic proxy (baseado em interface), o proxy CGLIB estende a classe concreta — por isso a classe e os métodos não podem ser `final`. É a estratégia padrão para classes `@Configuration` e beans sem interface.

Veja também: [[03-Dominios/Java/Spring Core e Boot/09 - AOP e proxies no Spring|AOP e proxies no Spring]].

### cgroup (control group)
Recurso do kernel Linux que impõe e contabiliza limites de CPU e memória sobre um conjunto de processos; é o que o container engine usa para confinar um container. A JVM container-aware lê esses limites para dimensionar heap e pools.

Veja também: [[03-Dominios/Java/Cloud-native e produção/02 - A JVM dentro de um container|A JVM dentro de um container]].

### Checked exception
Exceção que o compilador obriga o desenvolvedor a declarar (`throws`) ou capturar (`try/catch`). Estende `Exception` (excluindo `RuntimeException`). Exemplos: `IOException`, `SQLException`. Usada quando o chamador pode se recuperar do erro.

Veja também: [[10 - Exceções e tratamento de erros]].

### Checkstyle
Ferramenta de análise estática que verifica estilo e convenções de código (formatação, nomes, imports, javadoc) contra um conjunto de regras configurável. Plugável no build (Maven/Gradle) como quality gate que falha o build no desvio.

Veja também: [[03-Dominios/Java/Build e tooling/16 - Quality gates no build|Quality gates no build]].

### CI/CD
Integração contínua e entrega/deploy contínuos: o pipeline automatizado que constrói, testa e leva o código até produção sem humano no terminal. Cada commit dispara build, testes e gates de qualidade; passando, o artefato segue para deploy.

Veja também: [[03-Dominios/Java/Cloud-native e produção/20 - CI-CD e o caminho até produção|CI-CD e o caminho até produção]].

### circuit breaker
Disjuntor: padrão de resiliência que monitora a taxa de falha de uma chamada remota e, ao ultrapassar um limiar, "abre" — passa a falhar rápido sem chamar o serviço degradado, dando-lhe tempo para se recuperar. Tem três estados: fechado, aberto e meio-aberto. No Java, implementado pelo Resilience4j.

Veja também: [[03-Dominios/Java/Microservices e sistemas distribuídos/13 - Resiliência I — a falha distribuída e o Circuit Breaker|Resiliência I — Circuit Breaker]].

### classloader (parent delegation)
Componente da JVM responsável por carregar classes sob demanda a partir do classpath ou modulepath. O modelo de delegação hierárquica (parent delegation) determina que cada classloader consulta seu pai antes de tentar carregar a classe ele mesmo, garantindo que classes do JDK nunca sejam substituídas por versões do usuário.

Veja também: [[05 - Classloading e o delegation model]].

### client credentials (grant)
Fluxo OAuth2 server-to-server, sem usuário: o cliente troca `client_id`+`client_secret` por um access token. Para integrações de backend, não para login de pessoa.

Veja também: [[03-Dominios/Java/Segurança/12 - OAuth2 e OIDC Client e os grant types|OAuth2 e OIDC Client]].

### client proxy (CDI)
Objeto intermediário que o container injeta no lugar da instância real de um bean de escopo normal. A cada chamada de método o proxy resolve a instância do contexto ativo — o que permite injetar um bean de escopo curto (request) em um de escopo longo (application). Exige classe não-final (unproxyable types geram erro de deployment).

Veja também: [[03-Dominios/Java/Jakarta EE/05 - CDI — escopos e contextos|CDI — escopos e contextos]].

### client-side discovery
Padrão de service discovery em que o próprio cliente consulta o service registry, obtém a lista de instâncias disponíveis e escolhe uma (geralmente com load balancing). Contrasta com server-side discovery, onde um intermediário (load balancer) faz a escolha.

Veja também: [[03-Dominios/Java/Microservices e sistemas distribuídos/06 - Service discovery — o conceito e o Eureka|Service discovery — o conceito e o Eureka]].

### client-side load balancing
Balanceamento de carga feito no cliente: a partir da lista de instâncias obtida do registry, o cliente decide para qual instância enviar cada requisição (round-robin, random etc.). No Spring, implementado pelo Spring Cloud LoadBalancer.

Veja também: [[03-Dominios/Java/Microservices e sistemas distribuídos/08 - Client-side load balancing — Spring Cloud LoadBalancer|Client-side load balancing]].

### closed-world assumption
Premissa do GraalVM Native Image: tudo que o programa pode executar precisa ser conhecido em tempo de build, pois o que não for alcançado pela análise estática não entra no binário. Reflexão, proxies dinâmicos e carregamento dinâmico de classes exigem hints de configuração.

Veja também: [[03-Dominios/Java/Cloud-native e produção/08 - GraalVM Native Image — conceito e trade-offs|GraalVM Native Image — conceito e trade-offs]].

### CMT / BMT
Container-Managed Transactions vs. Bean-Managed Transactions: os dois modelos de demarcação da JTA. Em CMT o container abre/comita a transação de forma declarativa (`@Transactional`); em BMT o código controla manualmente via `UserTransaction`.

Veja também: [[03-Dominios/Java/Jakarta EE/11 - JTA — transações na plataforma|JTA — transações na plataforma]].

### comando vs evento
Distinção fundamental em arquiteturas orientadas a mensagens: um **comando** é uma instrução imperativa direcionada a um destinatário específico (ex.: `ProcessarPedidoCommand`), enquanto um **evento** é um fato ocorrido no passado publicado para quem quiser reagir (ex.: `PedidoProcessadoEvent`). Comandos implicam intenção; eventos implicam notificação.

Veja também: [[03-Dominios/Java/Mensageria/01 O que é mensageria e arquitetura orientada a eventos|O que é mensageria e arquitetura orientada a eventos]].

### code cache
Região de memória nativa onde a JVM armazena o código nativo gerado pelo compilador JIT. Quando fica cheia, a JVM para de compilar novos métodos e reverte à interpretação, degradando a performance. Monitorável com `-XX:+PrintCodeCache` e configurável com `-XX:ReservedCodeCacheSize`.

Veja também: [[07 - JIT — C1, C2 e tiered compilation]].

### cold publisher / hot publisher
Um *cold publisher* refaz a fonte para cada subscriber — cada subscription recomeça o fluxo do zero. Um *hot publisher* compartilha uma única fonte entre subscribers, e late subscribers só recebem o que for emitido depois que entraram (`share()`/`publish()`).

Veja também: [[03-Dominios/Java/Programação Reativa/04 - Nada acontece até o subscribe — lazy, assembly vs subscription, cold vs hot|Nada acontece até o subscribe]].

### Collector (coletor)
Objeto que encapsula uma estratégia de redução mutável para a operação terminal `collect` de uma `Stream`. Combina quatro funções: supplier (cria o container), accumulator (adiciona elemento), combiner (mescla containers paralelos) e finisher (transforma o resultado final). A fábrica `Collectors` fornece implementações prontas como `toList`, `groupingBy` e `joining`.

Veja também: [[03-Dominios/Java/Collections e Streams/08 - Collectors e agrupamento|Collectors]].

### Collections Framework
Arquitetura unificada do Java para representar e manipular grupos de objetos, composta por interfaces (`Collection`, `List`, `Set`, `Queue`, `Map`), implementações concretas (`ArrayList`, `HashSet`, `HashMap`…) e algoritmos utilitários (`Collections.sort`). Introduzida no Java 2 e continuamente ampliada.

Veja também: [[03-Dominios/Java/Collections e Streams/01 - O Collections Framework|Collections Framework]].

### Compact constructor
Construtor especial de records que omite a lista de parâmetros (não repete a assinatura) e executa antes da atribuição automática dos campos. Ideal para validação e normalização de dados sem boilerplate.

Veja também: [[13 - Records e record patterns]].

### Comparable
Interface `java.lang.Comparable<T>` com método `compareTo(T o)` que define a *ordenação natural* de uma classe. Implementada pela própria classe cujos objetos serão ordenados. Usada implicitamente por `Collections.sort`, `TreeSet` e `TreeMap`.

Veja também: [[03-Dominios/Java/Collections e Streams/06 - Comparable e Comparator|Comparable e Comparator]].

### Comparator
Interface funcional `java.util.Comparator<T>` com método `compare(T o1, T o2)` que define uma *ordenação externa* — separada da classe comparada. Permite múltiplas ordens para o mesmo tipo e compõe cadeias com `thenComparing`, `reversed` e métodos estáticos de fábrica como `Comparator.comparing`.

Veja também: [[03-Dominios/Java/Collections e Streams/06 - Comparable e Comparator|Comparable e Comparator]].

### CompletableFuture
Implementação de `Future` e `CompletionStage` introduzida no Java 8 que permite compor operações assíncronas em pipelines fluentes (`thenApply`, `thenCompose`, `thenCombine`). Suporta execução em thread pools customizados, tratamento de erros e combinação de múltiplos estágios sem bloqueio.

Veja também: [[10 - CompletableFuture e composição assíncrona]].

### @Component / estereótipos Spring
`@Component` marca uma classe como bean candidato a ser detectado pelo component scanning. Os estereótipos `@Service`, `@Repository` e `@Controller` (e `@RestController`) são especializações semânticas de `@Component`: indicam o papel da classe na arquitetura e, em alguns casos, adicionam comportamento (ex.: `@Repository` traduz exceções de persistência). Alfabetiza como "Component".

Veja também: [[03-Dominios/Java/Spring Core e Boot/03 - Beans e estereótipos — @Component, @Service, @Repository, @Controller|Beans e estereótipos]].

### component scanning
Processo pelo qual o Spring varre os pacotes em busca de classes anotadas com `@Component` (ou estereótipos) e as registra como beans, sem definição explícita. Configurado por `@ComponentScan` (ou implicitamente por `@SpringBootApplication`, que escaneia o pacote da classe principal e seus subpacotes).

Veja também: [[03-Dominios/Java/Spring Core e Boot/03 - Beans e estereótipos — @Component, @Service, @Repository, @Controller|Beans e estereótipos]].

### componente lightweight / heavyweight
Componente lightweight (Swing) é pintado inteiramente em Java, sem peer nativo do SO; componente heavyweight (AWT) possui peer nativo. Lightweight possibilita aparência consistente cross-platform e suporte a pluggable look-and-feel.

Veja também: [[03-Dominios/Java/Swing/01 - O modelo do Swing|Modelo do Swing]].

### concatMap
Operador reativo como o `flatMap`, mas que preserva a ordem: assina o próximo inner publisher só depois que o anterior completar. Sacrifica a concorrência em troca de saída ordenada e determinística.

Veja também: [[03-Dominios/Java/Programação Reativa/05 - map e flatMap — transformando o fluxo|map e flatMap]].

### ConcurrentHashMap
Implementação de `Map` altamente concorrente que usa segmentação interna (striping) e CAS para permitir leituras sem bloqueio e escritas com granularidade fina. Substituiu `Hashtable` e `Collections.synchronizedMap` em cenários de alta concorrência. Não permite chaves ou valores `null`.

Veja também: [[07 - Concurrent collections]].

### Condição de corrida (race condition)
Defeito que ocorre quando o resultado de um programa depende da ordem de intercalação não-determinística de operações de múltiplas threads. Geralmente causada por acesso a estado compartilhado sem sincronização adequada. Difícil de reproduzir e depurar por ser sensível ao escalonamento do SO.

Veja também: [[04 - As armadilhas - race, deadlock e companhia]].

### @Conditional / @ConditionalOnX
`@Conditional` registra um bean apenas se uma `Condition` programática retornar `true`. O Spring Boot fornece variantes declarativas — `@ConditionalOnClass`, `@ConditionalOnMissingBean`, `@ConditionalOnProperty` etc. — que são a espinha dorsal da auto-configuration: cada bean automático só entra se as condições do ambiente forem satisfeitas. Alfabetiza como "Conditional".

Veja também: [[03-Dominios/Java/Spring Core e Boot/14 - Conditional beans — @Conditional e os @ConditionalOn|Conditional beans]].

### @Configuration
Annotation do Spring que marca uma classe como fonte de definições de bean via métodos `@Bean`. Por padrão é *full mode*: a classe é proxiada por CGLIB para que chamadas entre métodos `@Bean` retornem o singleton do container (não uma nova instância). Alfabetiza como "Configuration".

Veja também: [[03-Dominios/Java/Spring Core e Boot/05 - @Configuration e @Bean — definição explícita de beans|@Configuration e @Bean]].

### configuration cache (Gradle)
Cache da fase de configuração e do task graph: o Gradle serializa o resultado da configuração e o reusa quando nada relevante muda, pulando o trabalho de reconfigurar o build. É o modo preferido a partir do Gradle 9.0 (ainda opt-in).

Veja também: [[03-Dominios/Java/Build e tooling/07 - Gradle — performance, build cache e daemon|Gradle — performance e build cache]].

### configuration (Gradle)
Bucket nomeado de dependências no Gradle — `implementation`, `api`, `compileOnly`, `runtimeOnly`, `testImplementation` — que define em qual classpath cada dependência entra e como se propaga para os consumidores do módulo.

Veja também: [[03-Dominios/Java/Build e tooling/05 - Gradle — build script, tasks e configurations|Gradle — build script e configurations]].

### @ConfigurationProperties
Annotation do Spring Boot que faz binding de um grupo de propriedades externas (com prefixo comum) para os campos de um bean tipado, com validação opcional. Alternativa estruturada e type-safe ao `@Value` para conjuntos de configuração relacionados. Alfabetiza como "ConfigurationProperties".

Veja também: [[03-Dominios/Java/Spring Core e Boot/12 - Configuração e profiles|Configuração e profiles]].

### constructor injection
Forma de injeção de dependência em que o container fornece as dependências como argumentos do construtor. É a abordagem recomendada no Spring: torna as dependências obrigatórias e explícitas, permite campos `final` (imutabilidade) e facilita testes sem o container.

Veja também: [[03-Dominios/Java/Spring Core e Boot/04 - Tipos de injeção — constructor, setter, field|Tipos de injeção]].

### Consul
Ferramenta da HashiCorp para service discovery e configuração distribuída: oferece registro de serviços com health checks, resolução via HTTP e DNS e um key/value store. Alternativa ao Eureka, integrada ao Spring Cloud via `spring-cloud-consul`.

Veja também: [[03-Dominios/Java/Microservices e sistemas distribuídos/07 - Discovery — Consul e Kubernetes-native|Discovery — Consul e Kubernetes-native]].

### container-awareness
Capacidade da JVM (desde o Java 10) de detectar que roda dentro de um container e ler os limites do cgroup em vez dos recursos da máquina inteira. Sem isso, a JVM dimensionaria heap e pools pela CPU/memória do host, e estouraria o limite do container.

Veja também: [[03-Dominios/Java/Cloud-native e produção/02 - A JVM dentro de um container|A JVM dentro de um container]].

### content negotiation
Mecanismo pelo qual o servidor escolhe a representação da resposta (JSON, XML, etc.) com base no que o cliente aceita, geralmente pelo header `Accept`. No Spring MVC o `ContentNegotiationManager` casa o media type solicitado com os `HttpMessageConverter` disponíveis e com o `produces` do mapeamento, retornando 406 (Not Acceptable) quando não há representação compatível.

Veja também: [[03-Dominios/Java/Web e APIs REST/07 - Content negotiation|Content negotiation]].

### content pane
Container interno de um top-level container (`JFrame`, `JDialog`) onde se adicionam os componentes visíveis da aplicação. `frame.add(...)` delega a ele. Usa `BorderLayout` por padrão.

Veja também: [[03-Dominios/Java/Swing/01 - O modelo do Swing|Modelo do Swing]].

### consumer lag
Diferença entre o offset mais recente produzido num tópico/partição e o offset que o grupo de consumidores já confirmou. Um lag crescente indica que os consumidores não acompanham o ritmo de produção. Monitorado via `kafka-consumer-groups.sh`, JMX ou ferramentas de observabilidade como Burrow e Micrometer.

Veja também: [[03-Dominios/Java/Mensageria/26 Observabilidade em mensageria|Observabilidade em mensageria]].

### Contention
Situação em que múltiplas threads disputam o mesmo lock ou recurso simultaneamente, forçando algumas a esperar. Alta contention degrada performance e pode eliminar os ganhos do paralelismo. Mitigada por locks de granularidade fina, estruturas lock-free ou particionamento de estado.

Veja também: [[04 - As armadilhas - race, deadlock e companhia]].

### continuous profiling
Perfilar a frota inteira continuamente, com overhead baixo o bastante para rodar sempre em produção, agregando os dados numa plataforma central. Permite responder "por que este serviço gastou CPU às 3h da manhã na semana passada" sem reproduzir o incidente.

Veja também: [[03-Dominios/Java/Cloud-native e produção/19 - Continuous profiling no cluster — Pyroscope e async-profiler|Continuous profiling no cluster]].

### contract testing
Técnica em que o consumidor de uma API declara o contrato que espera e o provedor verifica que o cumpre no próprio build — pega quebras sem testes E2E frágeis entre serviços. Em Java, via Pact.

Veja também: [[03-Dominios/Java/Testes/20 - Contract testing — Pact|Contract testing — Pact]].

### control plane
Plano de controle de um service mesh: o componente que distribui configuração, políticas e certificados para os proxies (data plane), sem tocar no tráfego em si. No Istio, é o `istiod`.

Veja também: [[03-Dominios/Java/Microservices e sistemas distribuídos/22 - Service mesh — quando a resiliência sai do código|Service mesh]].

### @ControllerAdvice / @RestControllerAdvice
`@ControllerAdvice` marca uma classe cujos `@ExceptionHandler`, `@InitBinder` e `@ModelAttribute` valem globalmente, para todos os controllers (ou um subconjunto filtrado por pacote/anotação/tipo). `@RestControllerAdvice` é a variante que combina `@ControllerAdvice` com `@ResponseBody`, ideal para handlers de exceção de APIs REST que serializam o corpo de erro diretamente. Alfabetiza como "ControllerAdvice".

Veja também: [[03-Dominios/Java/Web e APIs REST/09 - Tratamento de exceções com @ControllerAdvice|Tratamento de exceções com @ControllerAdvice]].

### convention over configuration
Princípio de design (popularizado pelo Rails e abraçado pelo Spring Boot) em que o framework assume padrões sensatos para a maioria dos casos, reduzindo a configuração explícita ao mínimo. O desenvolvedor só configura aquilo que diverge da convenção — é a filosofia por trás da auto-configuration e dos starters.

Veja também: [[03-Dominios/Java/Spring Core e Boot/01 - O que é Spring — Framework, Boot e o ecossistema|O que é Spring]].

### Conway's Law
Lei de Conway: organizações tendem a produzir sistemas cuja arquitetura espelha a estrutura de comunicação da própria organização. Em microservices, implica que a divisão em serviços deve refletir (e às vezes redesenhar — *inverse Conway maneuver*) as fronteiras das equipes.

Veja também: [[03-Dominios/Java/Microservices e sistemas distribuídos/01 - O que são microservices e a tese honesta|O que são microservices]], [[03-Dominios/Java/Microservices e sistemas distribuídos/23 - Quando NÃO fazer microservices|Quando NÃO fazer microservices]].

### coordenadas GAV
O endereço único de um artefato no repositório: `groupId:artifactId:version`. O groupId identifica a organização/projeto, o artifactId o módulo, e a version a release específica — juntos, resolvem exatamente qual binário baixar.

Veja também: [[03-Dominios/Java/Build e tooling/02 - Maven — POM, coordenadas e lifecycle|Maven — coordenadas]].

### Core Profile
O menor dos três perfis do Jakarta EE (introduzido no EE 10): conjunto mínimo de specs (CDI Lite, RESTful Web Services, JSON, Annotations, Interceptors) voltado a runtimes cloud-native e resolução em build-time. Web Profile e Platform são supersets.

Veja também: [[03-Dominios/Java/Jakarta EE/01 - O modelo Jakarta EE — especificações e implementações|O modelo Jakarta EE]].

### coreografia vs orquestração
Dois estilos de coordenação em arquiteturas de microsserviços. Na **coreografia** cada serviço reage a eventos e age de forma autônoma, sem um coordenador central — acoplamento mínimo, complexidade distribuída. Na **orquestração** um serviço central (orquestrador/saga orchestrator) coordena explicitamente os passos, facilitando visibilidade mas introduzindo acoplamento.

Veja também: [[03-Dominios/Java/Mensageria/22 Saga — transações distribuídas por eventos|Saga — transações distribuídas por eventos]].

### correlation ID
Identificador único atribuído a uma requisição na borda do sistema e propagado por todas as chamadas downstream, permitindo correlacionar logs e traces de uma mesma transação espalhada por vários serviços. Base do tracing distribuído junto com traceId/spanId.

Veja também: [[03-Dominios/Java/Microservices e sistemas distribuídos/18 - Tracing distribuído I — correlação no código|Tracing distribuído I — correlação no código]].

### CORS (Cross-Origin Resource Sharing)
Mecanismo do **browser** que libera ou bloqueia requests entre origens diferentes; não é segurança do servidor (`curl` ignora). Configurado por origens/métodos/headers explícitos.

Veja também: [[03-Dominios/Java/Segurança/11 - CORS — a borda, o preflight e a config de segurança|CORS]].

### CQRS
Command Query Responsibility Segregation: padrão arquitetural que separa o modelo de escrita (comandos que alteram estado) do modelo de leitura (queries). Permite otimizar cada lado independentemente — escritas transacionais com consistência forte; leituras com projeções desnormalizadas e alta performance. Frequentemente combinado com event sourcing.

Veja também: [[03-Dominios/Java/Mensageria/23 Event sourcing e CQRS|Event sourcing e CQRS]].

### Criteria API
API programática e type-safe da spec Jakarta Persistence para construir queries em Java (`CriteriaBuilder`, `CriteriaQuery`, `Root`) em vez de strings JPQL. As Specifications do Spring Data são uma camada sobre ela. Veja também: [[03-Dominios/Java/Persistência de dados/15 - Consultas dinâmicas e os limites da JPA — Specifications, Criteria e SQL|Consultas dinâmicas e os limites da JPA]], [[03-Dominios/Java/Jakarta EE/09 - JPA — a especificação de persistência|JPA]].

### CSRF (Cross-Site Request Forgery)
Ataque em que um site malicioso induz o browser a enviar uma request autenticada via cookie; o Spring Security protege por default com token sincronizado. Desliga-se em APIs stateless com JWT no header.

Veja também: [[03-Dominios/Java/Segurança/10 - CSRF — por que ligado por default e quando desligar|CSRF]].

### CsrfFilter
Filtro da cadeia que valida o token CSRF em requests mutating (POST/PUT/DELETE/PATCH).

Veja também: [[03-Dominios/Java/Segurança/10 - CSRF — por que ligado por default e quando desligar|CSRF]].

### CSS do JavaFX (-fx-)
Sistema de estilização do JavaFX baseado em um subconjunto de CSS 2.1 estendido com propriedades prefixadas `-fx-` (ex.: `-fx-background-color`, `-fx-font-size`). O user-agent stylesheet padrão é o Modena; folhas customizadas são aplicadas via `scene.getStylesheets().add(...)` ou `node.setStyle(...)`. Cada controle expõe pseudo-classes de estado (`:hover`, `:focused`, `:disabled`).

Veja também: [[09 - CSS em JavaFX]].

### CycloneDX
Padrão de SBOM focado em segurança, ratificado como especificação Ecma. Descreve componentes, dependências e suas vulnerabilidades em um formato legível por máquina; plugins Maven e Gradle geram o BOM CycloneDX no build.

Veja também: [[03-Dominios/Java/Build e tooling/18 - Supply chain e SBOM|Supply chain e SBOM]].

## D

### DatabaseClient (R2DBC)
Cliente de baixo nível do Spring para acesso reativo a banco relacional via R2DBC, sem repositório nem ORM. Expõe uma API fluente (`sql(...).bind(...).fetch()`) que devolve `Mono`/`Flux`, útil quando se quer controle direto sobre o SQL.

Veja também: [[03-Dominios/Java/Programação Reativa/13 - R2DBC — persistência reativa sem EntityManager|R2DBC]].

### database-per-service
Princípio de microservices em que cada serviço é dono exclusivo do seu banco de dados; nenhum outro serviço o acessa diretamente, só via API. Garante baixo acoplamento e autonomia, ao custo de consistência eventual e transações distribuídas (saga) entre serviços.

Veja também: [[03-Dominios/Java/Microservices e sistemas distribuídos/20 - Consistência em sistemas distribuídos|Consistência em sistemas distribuídos]].

### @DataJpaTest
Slice de teste do Spring Boot que carrega só a camada JPA (repositories, `EntityManager`); cada teste roda em transação com rollback automático. Use `Replace.NONE` + Testcontainers pra banco real.

Veja também: [[03-Dominios/Java/Testes/10 - @DataJpaTest — testando repositories|@DataJpaTest]].

### data plane
Plano de dados de um service mesh: o conjunto de proxies sidecar que interceptam e roteiam o tráfego real entre serviços, aplicando mTLS, retry e telemetria conforme a configuração recebida do control plane.

Veja também: [[03-Dominios/Java/Microservices e sistemas distribuídos/22 - Service mesh — quando a resiliência sai do código|Service mesh]].

### dead letter queue (DLQ)
Fila (ou tópico) de destino para mensagens que não puderam ser processadas com sucesso após N tentativas. Em vez de descartar ou bloquear o consumidor, a mensagem é encaminhada para a DLQ para análise e reprocessamento manual. No Spring Kafka o padrão equivalente chama-se Dead Letter Topic (DLT).

Veja também: [[03-Dominios/Java/Mensageria/12 Dead Letter Topic — o padrão DLQ|Dead Letter Topic — o padrão DLQ]].

### Deadlock
Estado em que duas ou mais threads se bloqueiam mutuamente, cada uma esperando um lock que a outra segura — criando uma espera circular sem saída. Nenhuma das threads progride indefinidamente. Prevenido por ordenação consistente de locks, uso de `tryLock` com timeout ou eliminação de lock aninhado.

Veja também: [[04 - As armadilhas - race, deadlock e companhia]].

### Debezium
Plataforma open-source de Change Data Capture baseada em Kafka Connect que captura eventos de mudança do log transacional de bancos (Postgres WAL, MySQL binlog, MongoDB oplog) e os publica como mensagens Kafka. É a implementação de CDC mais adotada na JVM e viabiliza o padrão Outbox sem polling no banco.

Veja também: [[03-Dominios/Java/Mensageria/21 O padrão Outbox|O padrão Outbox]].

### decorator (CDI)
Bean que envolve outro implementando o MESMO contrato de negócio, com acesso à instância decorada via `@Delegate`. Ao contrário do interceptor (cego ao contrato), o decorator conhece e pode usar os métodos do tipo decorado — ideal quando a lógica transversal depende do domínio.

Veja também: [[03-Dominios/Java/Jakarta EE/13 - CDI avançado — interceptors, decorators e extensões|CDI avançado]].

### Default method
Método com implementação definido em uma interface (palavra-chave `default`), introduzido no Java 8. Permite adicionar comportamento a interfaces sem quebrar classes que as implementam, viabilizando evolução retrocompatível de APIs.

Veja também: [[08 - Interfaces e classes abstratas]].

### DefaultErrorHandler
Componente do Spring Kafka (substituto do `SeekToCurrentErrorHandler` a partir do 2.8) que trata falhas no processamento de mensagens: tenta novamente N vezes (com backoff configurável) e, ao esgotar as tentativas, encaminha a mensagem para o Dead Letter Topic ou a descarta.

Veja também: [[03-Dominios/Java/Mensageria/11 Tratamento de erro no consumo|Tratamento de erro no consumo]].

### DelegatingPasswordEncoder
`PasswordEncoder` que prefixa o hash com o id do algoritmo (`{bcrypt}$...`), permitindo conviver com vários algoritmos e migrar gradualmente. Default do `PasswordEncoderFactories`.

Veja também: [[03-Dominios/Java/Segurança/04 - Password encoding — BCrypt, Argon2 e o DelegatingPasswordEncoder|Password encoding]].

### delegation event model
Modelo de eventos do AWT/Swing: a fonte (componente) notifica os listeners registrados quando um evento ocorre, despachando um objeto de evento. Separa a produção do evento do seu tratamento, favorecendo extensibilidade.

Veja também: [[03-Dominios/Java/Swing/04 - O modelo de eventos|Modelo de eventos]].

### deoptimization
Processo pelo qual a JVM descarta código nativo gerado pelo JIT e volta a interpretar (ou recompilar com menos agressividade) um método, tipicamente quando uma suposição feita em tempo de compilação (ex.: classe monormórfica) é invalidada em runtime. Pode ser observado nos GC logs com `-XX:+PrintCompilation`.

Veja também: [[07 - JIT — C1, C2 e tiered compilation]].

### dependencyManagement
Seção do POM que fixa as versões (e opcionalmente scope/exclusions) de dependências sem declará-las de fato no módulo. Os módulos filhos herdam a versão ao declarar a dependência sem `<version>`. É a base sobre a qual um BOM é construído.

Veja também: [[03-Dominios/Java/Build e tooling/11 - BOM e dependency management|BOM e dependency management]].

### dependency scope (Maven)
O escopo de uma dependência no Maven — `compile`, `provided`, `runtime`, `test`, `system` ou `import` — que controla em quais classpaths (compilação, runtime, teste) ela aparece e se é transitiva para os consumidores.

Veja também: [[03-Dominios/Java/Build e tooling/03 - Maven — dependências, scopes e exclusions|Maven — dependências e scopes]].

### dependency tree
A árvore das dependências efetivamente resolvidas, incluindo as transitivas. Inspecionada com `mvn dependency:tree` ou `gradle dependencies` para diagnosticar conflitos de versão, dependências duplicadas ou indesejadas.

Veja também: [[03-Dominios/Java/Build e tooling/10 - Resolução de dependências e conflitos de versão|Resolução de dependências e conflitos]].

### Deque
Interface `java.util.Deque<E>` (double-ended queue) que permite inserção e remoção em ambas as extremidades. Estende `Queue` e é implementada por `ArrayDeque` (preferível a `Stack` e `LinkedList` para pilhas e filas). Métodos principais: `addFirst`/`addLast`, `pollFirst`/`pollLast`, `peekFirst`/`peekLast`.

Veja também: [[03-Dominios/Java/Collections e Streams/02 - Listas, conjuntos e filas|Listas, conjuntos e filas]].

### dirty checking
Mecanismo da JPA pelo qual o provider detecta, no flush, quais entidades managed mudaram desde que entraram no persistence context e gera o SQL de UPDATE automaticamente — sem chamada explícita de "save". O contrato é da spec; a estratégia de detecção é do provider.

Veja também: [[03-Dominios/Java/Jakarta EE/10 - EntityManager e o ciclo de vida da entidade|EntityManager e o ciclo de vida da entidade]].

### DispatcherHandler
O *front controller* reativo do Spring WebFlux: o equivalente não-bloqueante do `DispatcherServlet` do Spring MVC. Recebe todas as requisições, resolve o handler via `HandlerMapping` e devolve um `Mono<Void>`, orquestrando o pipeline sobre o event loop.

Veja também: [[03-Dominios/Java/Programação Reativa/10 - Spring WebFlux — o stack não-bloqueante sobre Netty e o DispatcherHandler|Spring WebFlux]].

### DispatcherServlet
O *front controller* do Spring MVC: um único `Servlet` que recebe todas as requisições e orquestra o pipeline — consulta os `HandlerMapping` para achar o handler, invoca o `HandlerAdapter` para executá-lo, aplica `HandlerInterceptor`, resolve a view (ou serializa via `HttpMessageConverter`) e despacha a resposta. Centraliza o fluxo de processamento web.

Veja também: [[03-Dominios/Java/Web e APIs REST/06 - O pipeline do DispatcherServlet|O pipeline do DispatcherServlet]].

### distroless
Imagens base de container sem shell nem gerenciador de pacotes — só o runtime e as dependências estritamente necessárias para rodar o app. Reduzem drasticamente a superfície de ataque e o ruído do scanning de vulnerabilidades, ao custo de dificultar o debug interativo dentro do container.

Veja também: [[03-Dominios/Java/Cloud-native e produção/05 - Imagem enxuta e segura — distroless e scanning|Imagem enxuta e segura — distroless e scanning]].

### Document (modelo de texto)
Model dos componentes de texto (`JTextField`, `JTextArea`): representa o conteúdo como sequência de caracteres com atributos, não como `String`. Edições disparam `DocumentEvent` e podem ser interceptadas via `DocumentListener` ou `DocumentFilter`.

Veja também: [[03-Dominios/Java/Swing/07 - MVC em Swing e os models|MVC em Swing]].

### double buffering
Técnica em que o desenho é feito num buffer fora da tela e copiado de uma vez para o display, eliminando flicker. Ativo por padrão em todos os componentes Swing, gerenciado automaticamente pelo `RepaintManager`.

Veja também: [[03-Dominios/Java/Swing/10 - Custom painting e componentes customizados|Custom painting]].

### Duration / Period
Classes imutáveis do pacote `java.time` que representam quantidades de tempo. `Duration` mede intervalos baseados em segundos e nanossegundos (horas, minutos, segundos) e é adequada para tempo de máquina. `Period` mede intervalos em anos, meses e dias e é adequada para tempo humano/calendário. Ambas são criadas por métodos de fábrica e suportam aritmética de datas.

Veja também: [[03-Dominios/Java/Collections e Streams/11 - java.time — Date e Time API|java.time]].

## E

### EDT (Event Dispatch Thread)
Thread única onde o Swing processa todos os eventos e repinta a tela. A single-thread rule exige que todo acesso a componentes ocorra na EDT; operações longas nela travam a interface. Use `SwingUtilities.invokeLater` para delegar à EDT a partir de outras threads.

Veja também: [[03-Dominios/Java/Swing/05 - A Event Dispatch Thread|EDT]].

### EJB (Enterprise JavaBeans)
Modelo de componentes server-side da plataforma (Enterprise Beans 4.0 no EE 11): session beans (stateless/stateful/singleton), message-driven beans e timer service, com transações e segurança declarativas. Dominou o Java enterprise nos anos 2000; hoje grande parte de seu papel foi absorvida pelo CDI.

Veja também: [[03-Dominios/Java/Jakarta EE/12 - EJB — o legado que moldou a plataforma|EJB — o legado que moldou a plataforma]].

### effectively final
Variável local (ou parâmetro) que nunca é reatribuída após a inicialização, mesmo sem o modificador `final` explícito. Lambdas e classes anônimas só podem capturar variáveis `final` ou *effectively final*; reatribuir a variável depois da captura é erro de compilação. Garante que o valor capturado seja estável e evita closures sobre estado mutável.

Veja também: [[03-Dominios/Java/Collections e Streams/04 - Lambdas e interfaces funcionais|Lambdas e interfaces funcionais]], [[03-Dominios/Java/Collections e Streams/13 - Composição funcional e funções de alta ordem|Composição funcional]].

### embedded server
Servidor web (Tomcat, Jetty ou Undertow) embutido dentro do próprio jar da aplicação Spring Boot, em vez de a aplicação ser empacotada como WAR e implantada num servidor externo. Inverte o modelo tradicional: o `main()` sobe o servidor. Permite executar a aplicação com `java -jar`, simplificando deploy e containerização.

Veja também: [[03-Dominios/Java/Spring Core e Boot/16 - SpringApplication e o embedded server|SpringApplication e o embedded server]].

### @EnableAutoConfiguration
Annotation que ativa o mecanismo de auto-configuration do Spring Boot: instrui o container a aplicar as classes de auto-configuração registradas no classpath, conforme suas condições. Está embutida em `@SpringBootApplication`. Alfabetiza como "EnableAutoConfiguration".

Veja também: [[03-Dominios/Java/Spring Core e Boot/15 - Auto-configuration e starters|Auto-configuration e starters]].

### @EnableMethodSecurity
Anotação que liga a segurança no nível de método (`@PreAuthorize`/`@PostAuthorize`); substituiu `@EnableGlobalMethodSecurity`. Sem ela, as anotações são ignoradas silenciosamente.

Veja também: [[03-Dominios/Java/Segurança/07 - Method security — @PreAuthorize, @PostAuthorize e SpEL|Method security]].

### Enhanced for
Laço `for-each` — forma simplificada do `for` que itera diretamente sobre arrays ou qualquer objeto `Iterable`, sem índice explícito. Sintaxe: `for (Tipo var : coleção) { }`. Introduzido no Java 5.

Veja também: [[03 - Estruturas de controle e fluxo]].

### entity (JPA)
Classe Java anotada com `@Entity` que a JPA mapeia para uma tabela: tem identidade (`@Id`), construtor no-args e estado persistente. É o contrato da spec; o provider (Hibernate, EclipseLink) faz o ORM real.

Veja também: [[03-Dominios/Java/Jakarta EE/09 - JPA — a especificação de persistência|JPA — a especificação de persistência]].

### @EntityGraph
Anotação do Spring Data que define declarativamente quais associações carregar junto numa query (`attributePaths`) — a solução preferida para o problema N+1, sem o `JOIN FETCH` manual. Veja também: [[03-Dominios/Java/Persistência de dados/08 - O problema N+1 e suas soluções — @EntityGraph, JOIN FETCH, batch size|O problema N+1]].

### EntityManager
Interface central da JPA que gerencia o persistence context e expõe as operações de ciclo de vida (`persist`/`merge`/`remove`/`find`) e consultas (JPQL/Criteria). É a porta pela qual as entidades transitam entre os estados managed/detached.

Veja também: [[03-Dominios/Java/Jakarta EE/10 - EntityManager e o ciclo de vida da entidade|EntityManager e o ciclo de vida da entidade]].

### Enum
Tipo especial de classe cujas instâncias são um conjunto fechado e nomeado de constantes. Em Java, enums são objetos de pleno direito: podem ter campos, construtores, métodos e implementar interfaces. Garantem type-safety e eliminam "magic numbers".

Veja também: [[09 - Enums]].

### Epsilon GC
Coletor de lixo *no-op* experimental (JEP 318, Java 11): aloca objetos mas nunca os coleta. Útil para benchmarks de alocação, testes de desempenho sem interferência de GC e aplicações de vida curtíssima. Quando o heap é esgotado, a JVM termina com `OutOfMemoryError`. Ativado com `-XX:+UseEpsilonGC`.

Veja também: [[06 - Os coletores do HotSpot]].

### escopo (CDI)
Define o ciclo de vida e a visibilidade de um bean: quando o container o cria e descarta, e quem compartilha a instância. Escopos normais (`@ApplicationScoped`/`@RequestScoped`/`@SessionScoped`/`@ConversationScoped`) usam client proxy; `@Dependent` é pseudo-escopo (sem proxy, acompanha quem injeta).

Veja também: [[03-Dominios/Java/Jakarta EE/05 - CDI — escopos e contextos|CDI — escopos e contextos]].

### ergonomics (JVM)
Capacidade da JVM de ajustar automaticamente seus parâmetros de comportamento (tamanho de heap, número de GC threads, coletor padrão) com base nos recursos detectados no ambiente de execução, como número de CPUs e memória disponível. Fundamental para ajuste correto em containers, onde os recursos visíveis ao processo podem diferir dos da máquina física.

Veja também: [[09 - Flags, ergonomics e a JVM em containers]].

### escape analysis
Análise estática realizada pelo JIT para determinar se um objeto criado em um método pode ser referenciado fora dele (escapa). Se o objeto não escapa, o JIT pode eliminá-lo por inteiro (*scalar replacement*), substituindo seus campos por variáveis locais e evitando a alocação no heap — não por alocação na stack.

Veja também: [[07 - JIT — C1, C2 e tiered compilation]].

### Eureka
Service registry da Netflix, ainda mantido e integrado ao Spring Cloud via `spring-cloud-netflix-eureka`. As instâncias se registram e enviam heartbeats; os clientes consultam o registry para descobrir instâncias. Modelo AP (prioriza disponibilidade sobre consistência).

Veja também: [[03-Dominios/Java/Microservices e sistemas distribuídos/06 - Service discovery — o conceito e o Eureka|Service discovery — o conceito e o Eureka]].

### event dispatch chain (capturing / bubbling)
Rota percorrida por um evento JavaFX desde a raiz do grafo de cena até o nó-alvo (fase de *capturing*) e de volta à raiz (fase de *bubbling*). `EventFilter`s são ativados durante capturing; `EventHandler`s durante bubbling. Chamar `event.consume()` interrompe a propagação.

Veja também: [[05 - Eventos — capturing, bubbling e handlers]].

### EventFilter / EventHandler
Interfaces de tratamento de eventos do JavaFX. `EventHandler` (bubbling) é registrado com `node.addEventHandler(tipo, handler)` ou pela propriedade de conveniência `setOnAction`. `EventFilter` (capturing) é registrado com `node.addEventFilter(tipo, filter)` e intercepta o evento antes que chegue ao nó-alvo, permitindo controle centralizado ou cancelamento.

Veja também: [[05 - Eventos — capturing, bubbling e handlers]].

### Exaustividade
Propriedade de um `switch` (expressão ou statement) que garante que todos os casos possíveis são cobertos. O compilador Java exige exaustividade em switch expressions e em switches sobre sealed classes e enums. Violação gera erro em tempo de compilação.

Veja também: [[14 - Sealed classes e pattern matching]].

### @EventListener
Annotation do Spring que marca um método como ouvinte de eventos do `ApplicationContext`: o método é invocado quando um evento do tipo declarado é publicado (via `ApplicationEventPublisher`). Substitui a interface `ApplicationListener` por uma abordagem declarativa; suporta filtragem por condição SpEL e execução assíncrona com `@Async`. Alfabetiza como "EventListener".

Veja também: [[03-Dominios/Java/Spring Core e Boot/11 - Eventos do ApplicationContext|Eventos do ApplicationContext]].

### event-driven architecture
Estilo arquitetural em que os componentes se comunicam por meio de eventos assíncronos em vez de chamadas síncronas diretas. O produtor publica um evento e não conhece os consumidores; cada consumidor reage de forma independente, promovendo baixo acoplamento, alta escalabilidade e resiliência.

Veja também: [[03-Dominios/Java/Mensageria/01 O que é mensageria e arquitetura orientada a eventos|O que é mensageria e arquitetura orientada a eventos]].

### event loop
Modelo de execução do WebFlux/Netty em que poucos threads processam muitas conexões de forma não-bloqueante. Como cada thread atende várias requisições, bloquear um deles (ex.: JDBC ou `sleep`) paralisa todas as conexões que ele estava servindo — daí a regra de nunca bloquear o event loop.

Veja também: [[03-Dominios/Java/Programação Reativa/10 - Spring WebFlux — o stack não-bloqueante sobre Netty e o DispatcherHandler|Spring WebFlux]].

### event sourcing
Padrão em que o estado de uma entidade é derivado de uma sequência de eventos imutáveis armazenados em ordem temporal, em vez de persistir o estado atual diretamente. O estado presente é reconstituído reproduzindo os eventos. Facilita auditoria completa, projeções (read models) e integração com CQRS.

Veja também: [[03-Dominios/Java/Mensageria/23 Event sourcing e CQRS|Event sourcing e CQRS]].

### eventual consistency
Consistência eventual: modelo em que réplicas ou serviços diferentes podem divergir temporariamente, mas convergem para o mesmo estado se não houver novas escritas. É o trade-off típico de sistemas AP e do database-per-service, onde a consistência forte cede lugar à disponibilidade.

Veja também: [[03-Dominios/Java/Microservices e sistemas distribuídos/20 - Consistência em sistemas distribuídos|Consistência em sistemas distribuídos]].

### exactly-once semantics (EOS)
Garantia de que uma mensagem é processada **exatamente uma vez**, sem perdas nem duplicatas. Na prática é a mais difícil de alcançar: requer transações idempotentes no produtor Kafka (enable.idempotence), transações no consumidor/produtor e um processamento transacional end-to-end. O Spring Kafka oferece suporte via `KafkaTransactionManager`.

Veja também: [[03-Dominios/Java/Mensageria/13 Transações e exactly-once no Spring Kafka|Transações e exactly-once no Spring Kafka]].

### @ExceptionHandler
Annotation do Spring MVC que marca um método como tratador de uma ou mais exceções: quando um controller (ou handler) lança o tipo declarado, o método anotado é invocado para produzir a resposta. Funciona local ao controller ou globalmente dentro de uma classe `@ControllerAdvice`; o método pode retornar `ResponseEntity`, `ProblemDetail` ou um corpo serializado. Alfabetiza como "ExceptionHandler".

Veja também: [[03-Dominios/Java/Web e APIs REST/09 - Tratamento de exceções com @ControllerAdvice|Tratamento de exceções com @ControllerAdvice]].

### ExceptionMapper
Provider JAX-RS que converte uma exceção lançada por um resource em uma `Response` HTTP (ex.: `OrderNotFoundException` → 404). Centraliza o tratamento de erros fora dos métodos de recurso.

Veja também: [[03-Dominios/Java/Jakarta EE/07 - JAX-RS — REST declarativo|JAX-RS — REST declarativo]].

### ExceptionTranslationFilter
Filtro que traduz exceções de segurança em respostas HTTP: 401 (não-autenticado) dispara o entry point de autenticação, 403 (não-autorizado) vira acesso negado.

Veja também: [[03-Dominios/Java/Segurança/06 - A arquitetura do filter chain em profundidade|A arquitetura do filter chain]].

### executable jar / fat jar
Jar autocontido do Spring Boot que empacota a aplicação, todas as dependências e um servidor embarcado, executável com `java -jar`. Usa um layout aninhado próprio (dependências sob `BOOT-INF/lib`) e um launcher do Boot, em vez de um uber-jar plano. Também chamado de fat jar.

Veja também: [[03-Dominios/Java/Spring Core e Boot/16 - SpringApplication e o embedded server|SpringApplication e o embedded server]].

### Executor / ExecutorService
Abstração do `java.util.concurrent` que desacopla a submissão de tarefas (`Runnable` ou `Callable`) de sua execução. `ExecutorService` estende `Executor` adicionando ciclo de vida (`shutdown`, `awaitTermination`) e suporte a `Future`. Preferido ao gerenciamento manual de threads.

Veja também: [[08 - Executors e thread pools]].

### expand-and-contract
Padrão de migração de schema em três passos para mudar tabelas grandes sem downtime: expand (coluna nullable), backfill (em lotes), contract (aplica a constraint, ex.: NOT NULL) — cada passo numa migration separada, deployada em sequência. Veja também: [[03-Dominios/Java/Persistência de dados/16 - Migrations de schema — Flyway, Liquibase e expand-and-contract|Migrations de schema]].

## F

### fat jar / uber jar
Jar que embute, além das classes da aplicação, todas as suas dependências, virando um único artefato executável e autossuficiente. Produzido pelo Maven Shade Plugin ou pelo Gradle Shadow; o Spring Boot usa uma variante com layout próprio (executable jar).

Veja também: [[03-Dominios/Java/Build e tooling/15 - Empacotamento — fat jar, thin jar e repackage|Empacotamento — fat jar e thin jar]].

### Feign / OpenFeign
Cliente HTTP declarativo: descreve-se a chamada remota como uma interface Java anotada (`@FeignClient`) e o framework gera a implementação. Hoje em modo *feature-complete* (sem novos recursos), com o `@HttpExchange` do Spring como alternativa nativa.

Veja também: [[03-Dominios/Java/Microservices e sistemas distribuídos/09 - Comunicação síncrona — OpenFeign e HTTP Interface|Comunicação síncrona — OpenFeign e HTTP Interface]].

### fetch strategy (LAZY/EAGER)
Decide quando o Hibernate carrega uma associação: LAZY (sob demanda, via proxy) ou EAGER (junto com o pai). A regra prática é sempre LAZY — o default EAGER de `@ManyToOne`/`@OneToOne` é fonte oculta de problemas de performance. Veja também: [[03-Dominios/Java/Persistência de dados/07 - Fetch strategies — LAZY, EAGER e a LazyInitializationException|Fetch strategies]].

### FilterChainProxy
O `Filter` único (registrado via `DelegatingFilterProxy`) que delega para a lista ordenada de `SecurityFilterChain`; o coração da arquitetura do Spring Security.

Veja também: [[03-Dominios/Java/Segurança/06 - A arquitetura do filter chain em profundidade|A arquitetura do filter chain]].

### fitness function
Teste automatizado que valida uma característica arquitetural (camadas, ciclos, convenções) e falha o build quando ela é violada; em Java, expressas com ArchUnit.

Veja também: [[03-Dominios/Java/Testes/19 - Fitness functions — ArchUnit (testes de arquitetura)|Fitness functions — ArchUnit]].

### FlatLaf
Look and Feel moderno (flat, com suporte a dark mode) desenvolvido pela FormDev, disponível como biblioteca open-source third-party — não faz parte do JDK. Mantém aplicações Swing com aparência atual em diferentes sistemas operacionais.

Veja também: [[03-Dominios/Java/Swing/09 - Look and Feel e temas|Look and Feel]].

### flatMap (reativo)
Operador que transforma cada elemento em outro publisher e achata o resultado (`T → Publisher<R>`), usado para encadear chamadas assíncronas (ex.: buscar o usuário e, para cada um, buscar seus pedidos). Não garante ordem — os inner publishers são assinados em paralelo e intercalados conforme respondem.

Veja também: [[03-Dominios/Java/Programação Reativa/05 - map e flatMap — transformando o fluxo|map e flatMap]].

### Flow (java.util.concurrent)
As interfaces de Reactive Streams absorvidas no JDK no Java 9: `Flow.Publisher`, `Flow.Subscriber`, `Flow.Subscription` e `Flow.Processor`. São idênticas em contrato à spec Reactive Streams, mas vivem no `java.util.concurrent`, dando ao JDK um vocabulário comum sem depender de bibliotecas externas.

Veja também: [[03-Dominios/Java/Programação Reativa/02 - Reactive Streams — a spec das 4 interfaces e o Flow do Java 9|Reactive Streams]].

### Flux
Publisher do Project Reactor que representa uma sequência assíncrona de 0-N elementos (`Flux<T>`). É o tipo usado quando o fluxo pode emitir vários valores antes de completar (ou falhar); complementa o `Mono` (0-1).

Veja também: [[03-Dominios/Java/Programação Reativa/03 - Mono e Flux — os publishers do Project Reactor|Mono e Flux]].

### Flyway
Ferramenta de migração de schema baseada em SQL versionado (`V<versão>__<descrição>.sql`) e repeatable (`R__`), com a tabela de controle `flyway_schema_history` e enforcement de checksum. Veja também: [[03-Dominios/Java/Persistência de dados/16 - Migrations de schema — Flyway, Liquibase e expand-and-contract|Migrations de schema]].

### Fork/join
Framework introduzido no Java 7 (`ForkJoinPool`, `RecursiveTask`, `RecursiveAction`) que divide um problema em subproblemas menores (fork), resolve-os em paralelo e combina os resultados (join). Usa work-stealing para maximizar a utilização dos núcleos. Base dos parallel streams e do `CompletableFuture`.

Veja também: [[15 - Parallel streams e fork-join]].

### front controller
Padrão de arquitetura web em que um único ponto de entrada recebe todas as requisições e centraliza o despacho para os handlers apropriados, concentrando preocupações transversais (roteamento, segurança, logging) num só lugar. No Spring MVC, o `DispatcherServlet` é a encarnação desse padrão.

Veja também: [[03-Dominios/Java/Web e APIs REST/01 - O que é Spring MVC — a camada web sobre o container|O que é Spring MVC]].

### Function / Predicate / Consumer / Supplier
As quatro interfaces funcionais centrais de `java.util.function`. `Function<T,R>` transforma um T em R (`apply`); `Predicate<T>` testa uma condição booleana sobre T (`test`); `Consumer<T>` executa uma ação sobre T sem retorno (`accept`); `Supplier<T>` fornece um T sem receber argumento (`get`). Cada uma traz métodos `default` de composição — `andThen`/`compose` (`Function`), `and`/`or`/`negate` (`Predicate`), `andThen` (`Consumer`) — base da composição funcional e das operações de Stream.

Veja também: [[03-Dominios/Java/Collections e Streams/04 - Lambdas e interfaces funcionais|Lambdas e interfaces funcionais]], [[03-Dominios/Java/Collections e Streams/13 - Composição funcional e funções de alta ordem|Composição funcional]].

### functional endpoint (RouterFunction)
Modelo do Spring WebFlux em que o roteamento é código explícito (`RouterFunction`) em vez de controllers anotados, e cada rota é uma `HandlerFunction` (`ServerRequest → Mono<ServerResponse>`). Torna o fluxo de uma request um valor de primeira classe, componível e testável sem o container web.

Veja também: [[03-Dominios/Java/Programação Reativa/12 - Functional endpoints — RouterFunction e HandlerFunction|Functional endpoints]].

### Future
Interface que representa o resultado de uma operação assíncrona ainda em execução. Permite verificar se concluiu (`isDone`), cancelar (`cancel`) ou obter o resultado bloqueando (`get`). Limitada por não suportar composição; `CompletableFuture` supera essas limitações.

Veja também: [[08 - Executors e thread pools]].

### fx:id / @FXML
`fx:id` é o atributo XML de um elemento FXML que serve como identificador do nó dentro do documento. A anotação `@FXML` em um campo ou método do controller permite que o `FXMLLoader` injete o nó correspondente ao carregar o arquivo, eliminando lookups manuais via `scene.lookup`.

Veja também: [[06 - FXML e Scene Builder]].

### FXML
Formato XML do JavaFX para declarar a hierarquia de nós da UI de forma separada da lógica de negócio. Cada elemento XML corresponde a uma classe JavaFX instanciada pelo `FXMLLoader`; atributos mapeiam para propriedades via reflection. Suporta referência a controller, importações de classes, recursos i18n e inclusão de outros arquivos FXML.

Veja também: [[06 - FXML e Scene Builder]].

### FXMLLoader
Classe responsável por parsear um arquivo FXML e instanciar o grafo de cena correspondente. Associa o controller (anotado com `@FXML`) ao grafo carregado, injeta os nós com `fx:id` e registra os handlers declarados nos atributos `onAction`. Uso típico: `FXMLLoader.load(getClass().getResource("view.fxml"))`.

Veja também: [[06 - FXML e Scene Builder]].

## G

### G1 GC
Coletor de lixo de baixa latência padrão desde o Java 9, projetado para heaps grandes (> 4 GB). Divide o heap em regiões de tamanho fixo (1–32 MB) em vez de gerations físicas contíguas, selecionando as regiões com maior quantidade de lixo para coletar primeiro (*garbage-first*). Usa pausas incrementais e previsíveis, com meta de pause-time configurável via `-XX:MaxGCPauseMillis`.

Veja também: [[06 - Os coletores do HotSpot]].

### Gatherer (Stream Gatherers)
API introduzida no Java 24 (JEP 485) que permite criar operações intermediárias customizadas para `Stream`, além das oferecidas nativamente. Um `Gatherer` define como acumular, transformar ou filtrar elementos com estado próprio, integrando-se ao pipeline de stream com o método `gather(gatherer)`.

Veja também: [[03-Dominios/Java/Collections e Streams/15 - Collectors customizados e Gatherers|Gatherers]].

### GC roots / reachability
Conjunto de referências sempre consideradas vivas pelo garbage collector: referências em stack frames ativos, variáveis estáticas, referências JNI e objetos de sistema. Um objeto é alcançável (*reachable*) se existe algum caminho de referências a partir de qualquer GC root; objetos inalcançáveis são elegíveis para coleta.

Veja também: [[03 - Garbage Collection — o conceito]].

### @GeneratedValue
Anotação JPA que define a estratégia de geração da chave primária: IDENTITY (auto-increment, impede batch), SEQUENCE (recomendado, permite batch via `allocationSize`), TABLE, AUTO e UUID (adicionada na JPA 3.1). Veja também: [[03-Dominios/Java/Persistência de dados/02 - A entidade JPA — @Entity, @Id e geração de chave|A entidade JPA]].

### Generics
Mecanismo de parametrização de tipos que permite escrever classes, interfaces e métodos que operam sobre um tipo definido pelo chamador, com checagem em tempo de compilação. Elimina casts explícitos e detecta erros de tipo cedo. Ex: `List<String>`.

Veja também: [[12 - Generics em profundidade]].

### @GetMapping / @PostMapping (mapeamentos HTTP)
Atalhos do Spring MVC para `@RequestMapping` restritos a um método HTTP: `@GetMapping`, `@PostMapping`, `@PutMapping`, `@DeleteMapping` e `@PatchMapping`. Aplicados a métodos de um `@RestController`/`@Controller`, mapeiam um path + verbo para o handler, deixando a intenção explícita e o código mais legível que o `@RequestMapping(method = ...)`. Alfabetiza como "GetMapping".

Veja também: [[03-Dominios/Java/Web e APIs REST/02 - @RestController e os mapeamentos|@RestController e os mapeamentos]].

### Gluon
Empresa e projeto open-source que mantém o port do JavaFX para dispositivos móveis (iOS e Android) por meio do Gluon Mobile e das ferramentas GraalVM native-image. Principal mantenedor comercial do OpenJFX; fornece também o Gluon CloudLink e plugins para integração com Maven/Gradle.

Veja também: [[14 - JavaFX hoje — estado do projeto e Swing vs JavaFX]].

### GraalVM
Distribuição de JDK de alto desempenho que inclui um compilador AOT capaz de gerar um native image — um executável nativo do app, sem JVM em runtime. Também oferece um JIT alternativo e suporte a linguagens poliglotas.

Veja também: [[03-Dominios/Java/Cloud-native e produção/08 - GraalVM Native Image — conceito e trade-offs|GraalVM Native Image — conceito e trade-offs]].

### graceful shutdown
Encerramento ordenado em que, ao receber o `SIGTERM`, a aplicação para de aceitar novas requisições mas drena as que estão em voo antes de terminar. É o que evita erros 5xx para o usuário durante deploys e rescheduling de pods.

Veja também: [[03-Dominios/Java/Cloud-native e produção/12 - Graceful shutdown e deploy sem downtime|Graceful shutdown e deploy sem downtime]].

### Gradle
Build tool imperativo e flexível baseado em DSL (Groovy ou Kotlin), com build incremental, daemon e cache para acelerar builds. Modela o build como um grafo de tasks, em contraste com o lifecycle fixo do Maven.

Veja também: [[03-Dominios/Java/Build e tooling/05 - Gradle — build script, tasks e configurations|Gradle — build script, tasks e configurations]].

### Grafana
Plataforma de dashboards e alertas que visualiza métricas (do Prometheus) e outros sinais de observabilidade. Painéis exibem séries temporais e regras de alerta disparam notificações quando um limiar é cruzado.

Veja também: [[03-Dominios/Java/Cloud-native e produção/15 - Dashboards e alertas — Grafana|Dashboards e alertas — Grafana]].

### GrantedAuthority
Representa uma permissão concedida ao principal (uma role `ROLE_*`, um scope `SCOPE_*` ou uma authority custom); é o que `hasRole`/`hasAuthority` consultam.

Veja também: [[03-Dominios/Java/Segurança/02 - SecurityContext, Authentication e Principal — o usuário atual|SecurityContext, Authentication e Principal]].

### GridBagLayout
Layout manager mais flexível do Swing: posiciona componentes numa grade configurável via `GridBagConstraints` (gridx, gridy, weightx, weighty, fill, anchor). Poderoso para layouts complexos, mas verboso em comparação com alternativas como `MigLayout`.

Veja também: [[03-Dominios/Java/Swing/03 - Layout managers|Layout managers]].

### groupingBy
Collector de `java.util.stream.Collectors` que agrupa os elementos de uma stream por uma função classificadora, produzindo um `Map<K, List<V>>`. Variantes `groupingBy(f, downstream)` permitem aplicar um segundo collector aos elementos de cada grupo (ex.: contar, somar, transformar).

Veja também: [[03-Dominios/Java/Collections e Streams/08 - Collectors e agrupamento|Collectors]].

### gRPC
Framework de RPC (Remote Procedure Call) de alto desempenho criado pelo Google, que usa HTTP/2 como transporte e Protocol Buffers como serialização. Permite definir serviços e mensagens em `.proto` e gerar stubs Java tipados. Suporta streaming unidirecional e bidirecional. Alternativa eficiente ao REST para comunicação interna entre microsserviços.

Veja também: [[03-Dominios/Java/Mensageria/28 gRPC em Java — RPC síncrono sobre HTTP_2|gRPC em Java — RPC síncrono sobre HTTP/2]].

### Guard
Condição booleana adicional (`when`) que refina um case de pattern matching. Permite combinar a verificação de tipo/estrutura com uma expressão lógica no mesmo braço do switch. Ex: `case Integer i when i > 0 -> ...`.

Veja também: [[14 - Sealed classes e pattern matching]].

## H

### H2 (vs Testcontainers)
Banco em memória usado historicamente em testes; rápido, mas seu dialeto SQL diverge do banco de produção (Postgres/MySQL) e gera falso-positivo. Em produção-grade, prefira Testcontainers com o banco real.

Veja também: [[03-Dominios/Java/Testes/11 - Testcontainers — infra real em testes|Testcontainers]].

### HandlerAdapter
Componente do Spring MVC que sabe *como invocar* um handler de um determinado tipo. O `DispatcherServlet` não chama o handler diretamente: delega ao `HandlerAdapter` apropriado (ex.: `RequestMappingHandlerAdapter` para métodos `@RequestMapping`), que resolve argumentos, executa o método e adapta o retorno. Desacopla o despachante das várias formas de handler.

Veja também: [[03-Dominios/Java/Web e APIs REST/06 - O pipeline do DispatcherServlet|O pipeline do DispatcherServlet]].

### HandlerInterceptor
Interface do Spring MVC com os ganchos `preHandle`, `postHandle` e `afterCompletion`, executados em torno da invocação do handler (dentro do `DispatcherServlet`, com acesso ao contexto Spring). Diferente do `Filter` da spec Servlet (que opera antes de chegar ao `DispatcherServlet`), o interceptor enxerga qual handler será executado e pode abortar a cadeia retornando `false` no `preHandle`.

Veja também: [[03-Dominios/Java/Web e APIs REST/11 - Interceptors vs Filters|Interceptors vs Filters]].

### HandlerMapping
Componente do Spring MVC que, dada uma requisição, decide *qual handler* deve tratá-la. O `RequestMappingHandlerMapping` casa URL + método HTTP + headers/params contra os mapeamentos declarados (`@RequestMapping` e atalhos) e devolve um `HandlerExecutionChain` (handler + interceptors) ao `DispatcherServlet`.

Veja também: [[03-Dominios/Java/Web e APIs REST/06 - O pipeline do DispatcherServlet|O pipeline do DispatcherServlet]].

### Happens-before
Relação de ordenação definida pelo Java Memory Model (JMM) que garante que ações de uma thread sejam visíveis e ordenadas corretamente para outra thread. Não é ordem temporal: duas ações podem ocorrer em qualquer tempo, mas se A happens-before B, o efeito de A é garantidamente visível quando B ocorre. Estabelecida por `synchronized`, `volatile`, start/join de threads, entre outros.

Veja também: [[11 - Java Memory Model em profundidade]].

### hashCode / equals (contrato)
Contrato Java que exige consistência entre os dois métodos: objetos iguais (`equals` retorna `true`) devem ter o mesmo `hashCode`. A violação corrompeu estruturas baseadas em hash (`HashMap`, `HashSet`): o objeto pode ser inserido mas nunca encontrado. O inverso não é obrigado — dois objetos com mesmo `hashCode` podem ser desiguais (colisão normal).

Veja também: [[03-Dominios/Java/Collections e Streams/03 - Mapas|Mapas]].

### hasRole vs hasAuthority
`hasRole("ADMIN")` consulta a authority `ROLE_ADMIN` (adiciona o prefixo `ROLE_` automaticamente); `hasAuthority("ROLE_ADMIN")` exige o nome exato. Não duplicar o prefixo.

Veja também: [[03-Dominios/Java/Segurança/05 - Autorização baseada em URL — authorizeHttpRequests, roles vs authorities|Autorização baseada em URL]].

### HATEOAS
Hypermedia As The Engine Of Application State: restrição do REST em que a resposta carrega *links* que indicam ao cliente as transições de estado possíveis a partir do recurso atual, em vez de o cliente conhecer URLs de antemão. Corresponde ao nível 3 do Richardson Maturity Model; no Spring é suportado pela biblioteca Spring HATEOAS (`EntityModel`, `Link`, `WebMvcLinkBuilder`).

Veja também: [[03-Dominios/Java/Web e APIs REST/14 - HATEOAS|HATEOAS]].

### head sampling
Estratégia de amostragem de traces em que a decisão de amostrar (ou descartar) é tomada no início, na própria aplicação, antes de o trace existir por inteiro. É barata e simples, mas pode descartar justamente o trace de um erro raro, por decidir às cegas.

Veja também: [[03-Dominios/Java/Cloud-native e produção/16 - OpenTelemetry Collector e sampling de produção|OpenTelemetry Collector e sampling de produção]].

### heap
Área de memória principal da JVM onde todos os objetos e arrays são alocados. Dividida em gerações (young/eden, survivor, old) pelos coletores generacionais. O tamanho é configurável com `-Xms` (inicial) e `-Xmx` (máximo); esgotar o heap causa `OutOfMemoryError`.

Veja também: [[02 - Áreas de memória de runtime]].

### heap dump
Snapshot do conteúdo do heap da JVM em um dado instante, gravado em formato HPROF. Contém todos os objetos vivos, seus tipos, tamanhos e referências entre eles. Usado para diagnosticar vazamentos de memória com ferramentas como JMC, Eclipse MAT ou VisualVM.

Veja também: [[12 - Diagnóstico — heap dumps, thread dumps e jcmd]].

### Hibernate
A implementação mais usada da especificação JPA (Jakarta Persistence) — o provider que faz o ORM, com recursos além da spec (natural IDs, `@BatchSize`, query cache). É o que se usa em 99% dos casos quando se diz "JPA". Veja também: [[03-Dominios/Java/Persistência de dados/01 - O que é a camada de persistência — Spring Data, JPA e Hibernate|O que é a camada de persistência]].

### @HttpExchange (HTTP Interface)
Cliente HTTP declarativo nativo do Spring Framework (6.1+): uma interface anotada com `@HttpExchange`/`@GetExchange` é transformada em proxy por um `HttpServiceProxyFactory` sobre `RestClient` ou `WebClient`. Alternativa do próprio Spring ao OpenFeign.

Veja também: [[03-Dominios/Java/Microservices e sistemas distribuídos/09 - Comunicação síncrona — OpenFeign e HTTP Interface|Comunicação síncrona — OpenFeign e HTTP Interface]].

### HttpMessageConverter
Estratégia do Spring MVC que converte entre o corpo HTTP (bytes) e objetos Java: na leitura, desserializa o `@RequestBody`; na escrita, serializa o retorno marcado com `@ResponseBody`. Cada converter declara os media types que suporta (ex.: `MappingJackson2HttpMessageConverter` para JSON); a content negotiation escolhe qual usar conforme o `Accept`/`Content-Type`.

Veja também: [[03-Dominios/Java/Web e APIs REST/05 - Serialização JSON com Jackson|Serialização JSON com Jackson]].

## I

### idempotência (consumidor idempotente)
Propriedade de uma operação que produz o mesmo resultado independentemente de ser executada uma ou múltiplas vezes. Em mensageria com semântica at-least-once, o consumidor **deve** ser idempotente para lidar com reentregas sem efeitos colaterais duplicados — por exemplo, usando uma tabela de IDs processados ou uma chave de idempotência na operação de negócio.

Veja também: [[03-Dominios/Java/Mensageria/20 Idempotência — o pilar do at-least-once|Idempotência — o pilar do at-least-once]].

### Imutabilidade
Propriedade de um objeto cujo estado não pode ser alterado após a criação. Em Java, alcançada declarando campos `final`, não expondo mutadores e retornando cópias defensivas. Facilita raciocínio sobre o código e é segura para uso concorrente.

Veja também: [[06 - Classes, objetos e encapsulamento]].

### incremental build
Otimização do build tool que pula tasks cujos inputs e outputs não mudaram desde a última execução (up-to-date checking). É local à máquina; complementa o build cache, que compartilha outputs entre builds e máquinas.

Veja também: [[03-Dominios/Java/Build e tooling/07 - Gradle — performance, build cache e daemon|Gradle — performance e build cache]].

### Inferência de tipo
Capacidade do compilador de deduzir o tipo de uma variável local a partir da expressão à direita, sem que o programador o declare explicitamente. Em Java (a partir do Java 10): `var nome = "Alice";`. Só se aplica a variáveis locais com inicializador.

Veja também: [[02 - Tipos, variáveis e operadores]].

### @Inject
Annotation do CDI (`jakarta.inject.Inject`) que marca um ponto de injeção — campo, construtor ou método. O container resolve o bean por tipo + qualifiers e o fornece. Injeção por construtor é a preferida (testabilidade e imutabilidade). Alfabetiza como "Inject".

Veja também: [[03-Dominios/Java/Jakarta EE/04 - CDI — beans e injeção|CDI — beans e injeção]].

### InjectMocks
Anotação do Mockito (`@InjectMocks`) que cria o objeto sob teste e injeta nele os colaboradores `@Mock` declarados na classe de teste.

Veja também: [[03-Dominios/Java/Testes/06 - Mockito — mocks, stubbing e matchers|Mockito]].

### inlining (JIT)
Otimização do compilador JIT que substitui uma chamada de método pelo corpo do método chamado diretamente no ponto de chamada, eliminando o overhead de invocação e abrindo espaço para otimizações adicionais no contexto inlined. Métodos pequenos e frequentemente chamados são candidatos prioritários.

Veja também: [[07 - JIT — C1, C2 e tiered compilation]].

### InputMap / ActionMap (key bindings)
Mecanismo de atalhos de teclado do Swing: `InputMap` mapeia `KeyStroke` para uma chave string, e `ActionMap` mapeia a chave para uma `Action`. Supera `KeyListener` por suportar escopos de foco (`WHEN_IN_FOCUSED_WINDOW`) independentemente de qual componente está focado.

Veja também: [[03-Dominios/Java/Swing/11 - Action API, key bindings e performance|Action API]].

### Instant
Ponto no tempo com precisão de nanossegundos representado pelo número de segundos desde a época Unix (1970-01-01T00:00:00Z). Pertence ao pacote `java.time`. Imutável e compatível com `java.util.Date` via métodos de conversão. Ideal para timestamps de sistema independentes de fuso horário.

Veja também: [[03-Dominios/Java/Collections e Streams/11 - java.time — Date e Time API|java.time]].

### interceptor (CDI)
Bean transversal (`@Interceptor` + `@InterceptorBinding`) que envolve chamadas de método via `@AroundInvoke`/`InvocationContext`, sem conhecer o contrato de negócio do alvo. É o AOP da plataforma — o mecanismo por baixo de `@Transactional`. Ativado por `@Priority` ou `beans.xml`.

Veja também: [[03-Dominios/Java/Jakarta EE/13 - CDI avançado — interceptors, decorators e extensões|CDI avançado]].

### interface funcional
Interface com exatamente um método abstrato (SAM — Single Abstract Method), anotada opcionalmente com `@FunctionalInterface`. Permite que lambdas e method references sejam usados onde a interface é esperada. Exemplos: `Runnable`, `Comparator`, `Function`, `Predicate`, `Consumer`, `Supplier`.

Veja também: [[03-Dominios/Java/Collections e Streams/04 - Lambdas e interfaces funcionais|Lambdas e interfaces funcionais]].

### invokeLater / invokeAndWait
`SwingUtilities.invokeLater` agenda um `Runnable` para execução na EDT de forma assíncrona; `SwingUtilities.invokeAndWait` faz o mesmo de forma síncrona, bloqueando até a conclusão. `invokeAndWait` não pode ser chamado a partir da própria EDT.

Veja também: [[03-Dominios/Java/Swing/05 - A Event Dispatch Thread|EDT]].

### IoC / inversão de controle (Spring)
Princípio em que o controle da criação e da ligação de objetos é transferido do código da aplicação para o container: em vez de a classe instanciar suas dependências, o framework as injeta. A injeção de dependência é a forma concreta de IoC no Spring — "não nos chame, nós o chamaremos". Alfabetiza como "IoC".

Veja também: [[03-Dominios/Java/Spring Core e Boot/02 - IoC e injeção de dependência no Spring|IoC e injeção de dependência no Spring]].

### Istio
Service mesh mais popular: injeta proxies Envoy como sidecar (ou, no modo ambient, usa ztunnel + waypoint) para entregar mTLS, roteamento, retry e observabilidade sem tocar no código do serviço. Composto por data plane (proxies) e control plane (`istiod`).

Veja também: [[03-Dominios/Java/Microservices e sistemas distribuídos/22 - Service mesh — quando a resiliência sai do código|Service mesh]].

## J

### Jackson
Biblioteca de serialização/desserialização JSON padrão do ecossistema Spring. O `ObjectMapper` é o objeto central; anotações como `@JsonProperty`, `@JsonIgnore`, `@JsonInclude` e `@JsonFormat` controlam o mapeamento entre objetos Java e JSON. No Spring MVC, o `MappingJackson2HttpMessageConverter` o usa para converter `@RequestBody`/`@ResponseBody`.

Veja também: [[03-Dominios/Java/Web e APIs REST/05 - Serialização JSON com Jackson|Serialização JSON com Jackson]].

### Jakarta EE
Conjunto de especificações enterprise para Java (sucessor do Java EE, sob a Eclipse Foundation desde 2017). Define contratos de API (CDI, Servlet, JAX-RS, JPA, JTA...) implementados por servidores e runtimes certificados via TCK. Release atual: Jakarta EE 11 (jun/2025).

Veja também: [[03-Dominios/Java/Jakarta EE/01 - O modelo Jakarta EE — especificações e implementações|O modelo Jakarta EE]].

### javax → jakarta (rename)
Mudança de namespace ocorrida no Jakarta EE 9 (dez/2020): os pacotes `javax.*` da plataforma passaram a `jakarta.*` porque a Oracle reteve a trademark "Java". Foi big-bang (sem features novas) e partiu o ecossistema em dois mundos de namespace.

Veja também: [[03-Dominios/Java/Jakarta EE/02 - De Java EE a Jakarta EE|De Java EE a Jakarta EE]].

### java.nio.file (Path / Files)
API moderna de I/O de arquivos introduzida no Java 7, que substitui `java.io.File`. `Path` representa um caminho no sistema de arquivos de forma imutável e portável; `Files` oferece métodos utilitários estáticos para leitura, escrita, cópia, movimentação, walk e observação de diretórios com suporte a streams e nio channels.

Veja também: [[03-Dominios/Java/Collections e Streams/12 - I-O moderno com java.nio.file|I/O moderno]].

### JavaFX Application Thread
Thread única dedicada à atualização do grafo de cena e ao processamento de eventos de UI no JavaFX, análoga à EDT do Swing. Todo acesso a nós visíveis deve ocorrer nessa thread; operações longas devem ser delegadas a `Task` ou `Service` e o resultado devolvido via `Platform.runLater`.

Veja também: [[10 - A JavaFX Application Thread — Task, Service e Platform.runLater]].

### JAX-RS (Jakarta RESTful Web Services)
Especificação para construir APIs REST com annotations (RESTful Web Services 4.0 no EE 11): `@Path`/`@GET`/`@PathParam`, content negotiation (`@Produces`/`@Consumes`) e providers (`MessageBodyReader/Writer`, `ExceptionMapper`). Implementações: Jersey (RI), RESTEasy.

Veja também: [[03-Dominios/Java/Jakarta EE/07 - JAX-RS — REST declarativo|JAX-RS — REST declarativo]].

### jcmd
Ferramenta de linha de comando do JDK que envia comandos de diagnóstico a uma JVM em execução, como listar threads (`Thread.print`), gerar heap dump (`GC.heap_dump`), iniciar e despejar JFR (`JFR.start`, `JFR.dump`) e exibir flags de VM (`VM.flags`). Substitui `jmap`, `jstack` e `jinfo` como interface unificada de diagnóstico.

Veja também: [[12 - Diagnóstico — heap dumps, thread dumps e jcmd]].

### JComponent
Classe-base da maioria dos componentes Swing (`J*`), que estende `Container` do AWT. Adiciona suporte a pluggable look-and-feel, double buffering, borders, tooltips, key bindings e painting otimizado.

Veja também: [[03-Dominios/Java/Swing/01 - O modelo do Swing|Modelo do Swing]].

### JDK distribution
Um binário concreto do OpenJDK empacotado por um vendor com seu próprio selo de suporte, licença e cadência — Temurin (Adoptium), Corretto (AWS), Zulu (Azul), Liberica (BellSoft), Oracle JDK e GraalVM. Todas partem da mesma base OpenJDK.

Veja também: [[03-Dominios/Java/Build e tooling/09 - Distribuições do JDK e o ecossistema|Distribuições do JDK]].

### JDK dynamic proxy
Mecanismo do JDK (`java.lang.reflect.Proxy`) que cria, em runtime, um proxy implementando uma ou mais *interfaces*. É a estratégia padrão do Spring AOP quando o bean-alvo implementa interface — o proxy só pode interceptar métodos declarados na interface. Quando não há interface, o Spring recorre ao CGLIB.

Veja também: [[03-Dominios/Java/Spring Core e Boot/09 - AOP e proxies no Spring|AOP e proxies no Spring]].

### JFR (Java Flight Recorder)
Mecanismo de profiling e diagnóstico de baixíssimo overhead integrado à JVM HotSpot (GA no OpenJDK desde o Java 11) que coleta continuamente eventos de GC, alocações, I/O, threads, locks e código JIT em um buffer circular. Os dados são despejados em arquivo `.jfr` e analisados com JMC ou ferramentas compatíveis.

Veja também: [[13 - JFR e JMC — observabilidade de produção]].

### Jib
Plugin Maven/Gradle (do Google) que constrói uma imagem OCI do app sem precisar de Docker daemon nem Dockerfile — é daemonless. Monta a imagem em camadas otimizadas (dependências, recursos, classes) direto a partir do build, e pode publicá-la diretamente num registry.

Veja também: [[03-Dominios/Java/Cloud-native e produção/07 - Jib — imagem daemonless|Jib — imagem daemonless]].

### JIT (C1 / C2)
Compiladores Just-In-Time da JVM HotSpot que traduzem bytecode para código nativo em tempo de execução. C1 (client compiler) é rápido e aplica otimizações simples; C2 (server compiler) é mais lento mas produz código altamente otimizado via especulação e análise de perfil. Em tiered compilation (padrão desde o Java 8), ambos são usados em sequência conforme a "temperatura" do método.

Veja também: [[07 - JIT — C1, C2 e tiered compilation]].

### jlink
Ferramenta do JDK (introduzida no Java 9) que gera uma imagem de runtime customizada contendo apenas os módulos JPMS necessários para a aplicação. Reduz drasticamente o tamanho do JRE distribuído (de centenas de MB para dezenas), viabilizando distribuições self-contained de aplicações JavaFX.

Veja também: [[13 - Empacotamento — módulos, jlink e jpackage]].

### jlink (no build)
No contexto de empacotamento, o `jlink` cria um runtime Java mínimo e customizado a partir dos módulos JPMS necessários, reduzindo o tamanho da imagem distribuída. O detalhe da ferramenta em si está no Galho 3 (JPMS).

Veja também: [[03-Dominios/Java/Build e tooling/15 - Empacotamento — fat jar, thin jar e repackage|Empacotamento]], [[03-Dominios/Java/JVM/08 - JPMS — o sistema de módulos|JPMS]].

### JMC (JDK Mission Control)
IDE de análise de performance que lê arquivos `.jfr` gerados pelo JFR e os apresenta em visões gráficas de eventos, alocações, CPU, GC e latências. Distribuído separadamente do JDK; suporta análise offline e conexão em tempo real via JMX.

Veja também: [[13 - JFR e JMC — observabilidade de produção]].

### JMH (microbenchmark)
Java Microbenchmark Harness — o harness oficial do OpenJDK pra medir performance de código corretamente, lidando com warmup, JIT, fork e dead-code elimination (que enganam um `System.nanoTime()` num `@Test`).

Veja também: [[03-Dominios/Java/Testes/18 - Performance — JMH e microbenchmarks|Performance — JMH]].

### JMS
Java Message Service: API padrão do Jakarta EE (Jakarta Messaging 3.1) para comunicação assíncrona baseada em mensagens. Define `Queue` (point-to-point) e `Topic` (publish-subscribe) como destinos, e usa `JMSProducer`/`JMSConsumer` para envio e recepção. Implementações: ActiveMQ, IBM MQ, Oracle AQ.

Veja também: [[03-Dominios/Java/Mensageria/02 Os modelos de mensageria — queue vs topic|Os modelos de mensageria — queue vs topic]].

### jpackage
Ferramenta do JDK (JEP 392, GA no Java 16) que empacota uma aplicação Java e sua imagem de runtime (`jlink`) em um instalador nativo para a plataforma-alvo: `.msi`/`.exe` (Windows), `.dmg`/`.pkg` (macOS) ou `.deb`/`.rpm` (Linux). Elimina a necessidade de JRE instalado previamente no sistema do usuário.

Veja também: [[13 - Empacotamento — módulos, jlink e jpackage]].

### JPA (Jakarta Persistence)
Especificação de ORM da plataforma (Jakarta Persistence 3.2 no EE 11): define `@Entity`, EntityManager, persistence unit e JPQL. É o contrato — Hibernate e EclipseLink são implementações. "JPA não é o Hibernate."

Veja também: [[03-Dominios/Java/Jakarta EE/09 - JPA — a especificação de persistência|JPA — a especificação de persistência]].

### JpaRepository
Interface topo da hierarquia de repositórios do Spring Data JPA (`Repository` → `CrudRepository` → `PagingAndSortingRepository` → `JpaRepository`); o Spring gera a implementação (um proxy) em runtime, com CRUD, paginação e queries derivadas. Veja também: [[03-Dominios/Java/Persistência de dados/04 - Spring Data repositories — JpaRepository e query methods derivados|Spring Data repositories]].

### JPQL
Jakarta Persistence Query Language: linguagem de consulta orientada a entidades (não a tabelas) da JPA. Sintaxe parecida com SQL, mas opera sobre entidades e seus relacionamentos; executada via `TypedQuery` com parâmetros nomeados.

Veja também: [[03-Dominios/Java/Jakarta EE/10 - EntityManager e o ciclo de vida da entidade|EntityManager e o ciclo de vida da entidade]].

### JPMS (module-info)
Java Platform Module System (introduzido no Java 9, JEP 261): sistema de módulos que adiciona uma camada de encapsulamento forte acima dos pacotes. Cada módulo declara suas dependências (`requires`) e o que exporta (`exports`) em um arquivo `module-info.java`. Permite criar imagens de runtime mínimas com `jlink` e elimina o classpath hell.

Veja também: [[08 - JPMS — o sistema de módulos]].

### JTA (Jakarta Transactions)
Especificação de demarcação e coordenação de transações da plataforma (Transactions 2.0 no EE 11): `UserTransaction` (programática), `@Transactional` (declarativa via interceptor CDI) e integração com XA/two-phase commit para múltiplos recursos.

Veja também: [[03-Dominios/Java/Jakarta EE/11 - JTA — transações na plataforma|JTA — transações na plataforma]].

### JUnit 5 (Jupiter)
Framework de testes moderno do Java (Platform + Jupiter + Vintage); a API Jupiter (`@Test`/`@BeforeEach`/`@ParameterizedTest`) substituiu o modelo do JUnit 4.

Veja também: [[03-Dominios/Java/Testes/02 - JUnit 5 — anatomia, lifecycle e o padrão AAA|JUnit 5]].

### JWKS (JSON Web Key Set)
Endpoint que publica as chaves públicas do emissor (`jwk-set-uri`); o Resource Server busca a chave por ele para validar a assinatura do JWT, permitindo rotação sem downtime.

Veja também: [[03-Dominios/Java/Segurança/09 - OAuth2 Resource Server — validando JWT na API|OAuth2 Resource Server]].

### JWT (JSON Web Token)
Token de três partes (header.payload.signature em base64url) que carrega claims assinadas; é **legível, não criptografado**. Stateless; valide sempre `iss`/`aud`/`exp` e a whitelist de `alg`.

Veja também: [[03-Dominios/Java/Segurança/08 - JWT — estrutura, assinatura e validação|JWT]].

### JwtAuthenticationConverter
Componente que converte as claims de um JWT (ex.: `scope`/`roles`) em `GrantedAuthority` no Resource Server; sem ele, as authorities saem vazias.

Veja também: [[03-Dominios/Java/Segurança/09 - OAuth2 Resource Server — validando JWT na API|OAuth2 Resource Server]].

## K

### @KafkaListener
Annotation do Spring Kafka aplicada a um método que o torna um consumidor Kafka: o Spring cria um listener container que faz o poll, deserializa os registros e invoca o método para cada mensagem (ou lote). Configurável com group id, tópicos, partições e concorrência diretamente na anotação. Alfabetiza como "KafkaListener".

Veja também: [[03-Dominios/Java/Mensageria/08 @KafkaListener — consumindo mensagens|@KafkaListener — consumindo mensagens]].

### KafkaTemplate
Componente central do Spring Kafka para produção de mensagens: abstrai o `KafkaProducer` do cliente Java com uma API fluente (`send(topic, key, value)`) que devolve um `CompletableFuture`. Lida com serialização e, opcionalmente, com transações Kafka.

Veja também: [[03-Dominios/Java/Mensageria/07 KafkaTemplate — produzindo mensagens|KafkaTemplate — produzindo mensagens]].

### Kotlin DSL (Gradle)
Forma de escrever build scripts do Gradle em Kotlin (`build.gradle.kts`), com tipagem estática e autocompletar no IDE, em contraste com a DSL Groovy dinâmica. É o default recomendado desde o Gradle 8.0.

Veja também: [[03-Dominios/Java/Build e tooling/05 - Gradle — build script, tasks e configurations|Gradle — build script, tasks e configurations]].

### KRaft
Modo de operação do Apache Kafka (disponível como padrão a partir do Kafka 3.3, substituindo o ZooKeeper completamente no 4.0) em que o próprio cluster Kafka gerencia seus metadados via protocolo Raft, eliminando a dependência do ZooKeeper. Simplifica o deployment e operação do cluster.

Veja também: [[03-Dominios/Java/Mensageria/05 Kafka numa página para o dev de aplicação|Kafka numa página para o dev de aplicação]].

## L

### lambda
Expressão anônima que implementa uma interface funcional na forma `(parâmetros) -> corpo`. Introduzida no Java 8, elimina a verbosidade de classes anônimas e habilita programação funcional — passagem de comportamento como argumento. Captura variáveis `final` ou *effectively final* do escopo externo.

Veja também: [[03-Dominios/Java/Collections e Streams/04 - Lambdas e interfaces funcionais|Lambdas e interfaces funcionais]].

### Latch (CountDownLatch)
Sincronizador de uso único que permite que uma ou mais threads aguardem até que um contador chegue a zero. O contador é decrementado por `countDown()` e a espera é feita com `await()`. Ideal para aguardar a conclusão de um conjunto de tarefas ou o início de um evento comum. Não pode ser reutilizado.

Veja também: [[09 - Sincronizadores]].

### layered jar
Modo de empacotamento do Spring Boot que divide o jar executável em camadas organizadas por ritmo de mudança (dependências, snapshots, recursos, classes da aplicação). Como as camadas de baixo ritmo mudam raramente, a imagem de container reaproveita seu cache entre builds, reconstruindo só o que mudou.

Veja também: [[03-Dominios/Java/Cloud-native e produção/04 - Dockerfile na prática — multi-stage e layered jar|Dockerfile na prática — multi-stage e layered jar]].

### layout manager
Objeto que posiciona e dimensiona automaticamente os componentes de um container, respondendo a resize, look-and-feel e DPI. Exemplos: `BorderLayout`, `FlowLayout`, `BoxLayout`, `GridBagLayout`. Evita coordenadas absolutas e torna o layout adaptável.

Veja também: [[03-Dominios/Java/Swing/03 - Layout managers|Layout managers]].

### layout pane
Container do JavaFX que posiciona e dimensiona seus filhos segundo uma estratégia específica. Principais opções: `HBox`/`VBox` (linha/coluna), `BorderPane` (5 regiões), `GridPane` (grade), `StackPane` (sobreposição), `AnchorPane` (ancorado nas bordas) e `FlowPane` (fluxo). Substituem os layout managers do Swing no modelo de retained mode.

Veja também: [[03 - Layout panes]].

### lifecycle (Maven)
A sequência ordenada de phases que o Maven executa: `validate` → `compile` → `test` → `package` → `verify` → `install` → `deploy`. Rodar uma phase executa todas as anteriores e dispara os goals de plugin ligados a cada uma.

Veja também: [[03-Dominios/Java/Build e tooling/02 - Maven — POM, coordenadas e lifecycle|Maven — lifecycle]].

### Linkerd
Service mesh leve, focado em simplicidade: usa um micro-proxy escrito em Rust (em vez do Envoy) como sidecar, com menor consumo de recursos. Projeto graduado da CNCF, alternativa mais enxuta ao Istio.

Veja também: [[03-Dominios/Java/Microservices e sistemas distribuídos/22 - Service mesh — quando a resiliência sai do código|Service mesh]].

### Liquibase
Ferramenta de migração de schema baseada em changelog declarativo (changesets em XML/YAML/JSON/SQL), com rollback declarativo e a tabela de controle `DATABASECHANGELOG` (com MD5SUM). Alternativa ao Flyway. Veja também: [[03-Dominios/Java/Persistência de dados/16 - Migrations de schema — Flyway, Liquibase e expand-and-contract|Migrations de schema]].

### listener (event listener)
Objeto registrado em um componente (fonte) para ser notificado quando eventos específicos ocorrem, via callback (ex.: `ActionListener.actionPerformed`). Os callbacks são invocados na EDT.

Veja também: [[03-Dominios/Java/Swing/04 - O modelo de eventos|Modelo de eventos]].

### Livelock
Situação em que duas ou mais threads continuam executando (não bloqueadas) mas não progridem, pois cada uma reage à ação da outra em loop infinito — como duas pessoas que se desviam na mesma direção no corredor. Diferente do deadlock, as threads estão ativas mas inutilmente.

Veja também: [[04 - As armadilhas - race, deadlock e companhia]].

### liveness probe
Sonda do Kubernetes que pergunta "este pod ainda está vivo?"; se falhar repetidamente, o orquestrador reinicia o container. Deve checar apenas se o processo travou de forma irrecuperável — não dependências externas, sob pena de reinícios em cascata.

Veja também: [[03-Dominios/Java/Cloud-native e produção/10 - Health e probes — o contrato com o orquestrador|Health e probes — o contrato com o orquestrador]].

### LocalDate / LocalDateTime
Classes imutáveis de `java.time` que representam, respectivamente, uma data (ano-mês-dia) e uma combinação de data e hora, ambas sem informação de fuso horário. `LocalDate` é adequada para datas de calendário (aniversários, vencimentos); `LocalDateTime` para timestamps locais. Criadas por `LocalDate.now()`, `LocalDate.of(...)` e similares.

Veja também: [[03-Dominios/Java/Collections e Streams/11 - java.time — Date e Time API|java.time]].

### Lock-free
Propriedade de um algoritmo ou estrutura de dados que garante progresso global mesmo se threads individuais forem preemptadas indefinidamente — ao menos uma thread sempre avança. Implementado com CAS e loops de retry sem `synchronized`. Reduz contention e risco de deadlock ao custo de maior complexidade.

Veja também: [[06 - Atômicos e operações lock-free]].

### Lombok
Biblioteca que gera boilerplate (getters, setters, construtores, `equals`/`hashCode`, builders) em compile-time, manipulando a AST via annotation processing — `@Getter`, `@Data`, `@Builder`. Reduz código repetitivo, ao custo de acoplar o build ao processor.

Veja também: [[03-Dominios/Java/Build e tooling/14 - Annotation processing — Lombok e MapStruct|Annotation processing — Lombok e MapStruct]].

### look and feel (L&F)
Conjunto plugável que define a aparência visual e o comportamento interativo de todos os componentes Swing. Trocável em runtime via `UIManager.setLookAndFeel`; inclui opções como Metal, Nimbus, System L&F e bibliotecas third-party como FlatLaf.

Veja também: [[03-Dominios/Java/Swing/09 - Look and Feel e temas|Look and Feel]].

### LTS
Long-Term Support — versão do Java que recebe atualizações de segurança e correções por um período estendido (vários anos). Recomendada para produção. As principais versões LTS modernas são Java 8, 11, 17, 21 e 25.

Veja também: [[01 - O modelo da linguagem Java]], [[15 - A evolução do Java (8 a 25)]].

## M

### @ManyToMany
Associação muitos-para-muitos, mapeada por uma tabela de junção (`@JoinTable`). Quando a relação tem atributos próprios (quantidade, data), prefira uma entidade associativa explícita. Veja também: [[03-Dominios/Java/Persistência de dados/06 - @ManyToMany, @OneToOne, cascade e orphanRemoval|@ManyToMany, @OneToOne, cascade e orphanRemoval]].

### @ManyToOne / @OneToMany
O par que modela uma associação um-para-muitos. O `@ManyToOne` é o owning side (tem a foreign key); o `@OneToMany(mappedBy = ...)` é o inverse side (só espelha). Veja também: [[03-Dominios/Java/Persistência de dados/05 - Relacionamentos — @ManyToOne, @OneToMany e o owning side|Relacionamentos]].

### map (reativo)
Operador que transforma cada elemento de um publisher de forma síncrona e 1:1 (`T → R`), sem achatar publishers. É o equivalente reativo do `map` de `Stream`/`Optional`; quando a transformação produz outro publisher, usa-se `flatMap` no lugar.

Veja também: [[03-Dominios/Java/Programação Reativa/05 - map e flatMap — transformando o fluxo|map e flatMap]].

### MapStruct
Gerador de mappers entre Entity e DTO em compile-time via annotation processing: a partir de uma interface anotada com `@Mapper`, gera a implementação que copia os campos, sem reflection em runtime. Type-safe e rápido.

Veja também: [[03-Dominios/Java/Build e tooling/14 - Annotation processing — Lombok e MapStruct|Annotation processing — Lombok e MapStruct]].

### marble diagram
Diagrama visual que representa um fluxo reativo no tempo — os elementos emitidos, o sinal de conclusão e o de erro — e o efeito de um operador sobre esse fluxo. É a notação padrão da documentação do Reactor/RxJava para explicar operadores.

Veja também: [[03-Dominios/Java/Programação Reativa/03 - Mono e Flux — os publishers do Project Reactor|Mono e Flux]].

### Maven
Build tool declarativo baseado em convenção e no descritor `pom.xml`. Modela o build como um lifecycle de phases fixas e resolve dependências por coordenadas GAV a partir de repositórios. Privilegia convenção sobre configuração.

Veja também: [[03-Dominios/Java/Build e tooling/02 - Maven — POM, coordenadas e lifecycle|Maven — POM, coordenadas e lifecycle]].

### Maven Central
O repositório público padrão de artefatos do ecossistema Java/JVM, de onde Maven e Gradle baixam dependências por default. A publicação atual passa pelo Central Portal da Sonatype.

Veja também: [[03-Dominios/Java/Build e tooling/19 - Publicação de artefatos|Publicação de artefatos]].

### MaxRAMPercentage
Flag da JVM que dimensiona o heap máximo como uma porcentagem da memória disponível ao container, em vez de um valor absoluto fixo (`-Xmx`). É a forma idiomática de configurar memória num container: o heap acompanha o limite do cgroup mesmo quando este muda.

Veja também: [[03-Dominios/Java/Cloud-native e produção/02 - A JVM dentro de um container|A JVM dentro de um container]].

### MDB (message-driven bean)
Tipo de Enterprise Bean que consome mensagens de forma assíncrona (tipicamente de uma fila/tópico), processando-as fora do fluxo request/response. É o ponto de integração do EJB com mensageria.

Veja também: [[03-Dominios/Java/Jakarta EE/12 - EJB — o legado que moldou a plataforma|EJB — o legado que moldou a plataforma]].

### merge / concat / zip
Operadores de combinação de publishers no Reactor: `merge` intercala os elementos conforme chegam (sem ordem garantida entre fontes), `concat` concatena ordenado (esgota uma fonte antes da próxima) e `zip` combina elemento-a-elemento, esperando que todos os lados emitam.

Veja também: [[03-Dominios/Java/Programação Reativa/06 - Combinando publishers — zip, merge, concat, filter|Combinando publishers]].

### method reference
Atalho sintático para lambdas que apenas delegam a um método existente, na forma `Classe::método` ou `objeto::método`. Quatro variantes: referência a método estático (`Integer::parseInt`), a método de instância via tipo (`String::toUpperCase`), a método de instância via objeto específico (`this::process`) e a construtor (`ArrayList::new`).

Veja também: [[03-Dominios/Java/Collections e Streams/04 - Lambdas e interfaces funcionais|Lambdas e interfaces funcionais]].

### MethodArgumentNotValidException
Exceção que o Spring MVC lança quando um argumento de handler anotado com `@Valid`/`@Validated` falha na Bean Validation: agrega os erros num `BindingResult`. Por padrão resulta em 400 (Bad Request); pode ser capturada num `@ExceptionHandler`/`@ControllerAdvice` para transformar as violações num corpo de erro estruturado (ex.: `ProblemDetail`).

Veja também: [[03-Dominios/Java/Web e APIs REST/08 - Validação na borda|Validação na borda]], [[Dicionário de Java#Bean Validation (Jakarta Validation)|Bean Validation]].

### Metaspace
Área de memória nativa (fora do heap Java) introduzida no Java 8 para substituir o PermGen, onde a JVM armazena metadados de classes carregadas (estruturas internas, bytecode, pool de constantes). Cresce sob demanda sem limite fixo por padrão; configurável com `-XX:MaxMetaspaceSize`. Não confundir com `MetaspaceSize`, que é o tamanho inicial a partir do qual o GC começa a limpar classes não utilizadas.

Veja também: [[02 - Áreas de memória de runtime]].

### Micrometer Observation API
API do Micrometer que unifica a instrumentação: marca-se uma operação como uma `Observation` uma única vez e dela derivam métricas, traces e logs correlacionados. Evita instrumentar três vezes a mesma fronteira.

Veja também: [[03-Dominios/Java/Microservices e sistemas distribuídos/18 - Tracing distribuído I — correlação no código|Tracing distribuído I — correlação no código]].

### Micrometer Tracing
Biblioteca de tracing distribuído do projeto Micrometer, sucessora do Spring Cloud Sleuth (descontinuado). Gera e propaga traceId/spanId e faz bridge para tracers como Brave (Zipkin) ou OpenTelemetry.

Veja também: [[03-Dominios/Java/Microservices e sistemas distribuídos/18 - Tracing distribuído I — correlação no código|Tracing distribuído I — correlação no código]].

### microservices
Estilo arquitetural em que a aplicação é dividida em serviços pequenos, independentes e deployáveis em separado, cada um dono de um bounded context e do seu próprio banco. Troca a simplicidade do monólito por autonomia de equipes e escala — ao custo de complexidade distribuída.

Veja também: [[03-Dominios/Java/Microservices e sistemas distribuídos/01 - O que são microservices e a tese honesta|O que são microservices e a tese honesta]].

### mock vs spy vs fake vs stub
Os test doubles: **mock** (dublê controlado e verificável), **spy** (wrapper sobre objeto real com stubs pontuais), **fake** (implementação simples alternativa, ex.: repositório em `HashMap`), **stub** (retorna respostas fixas).

Veja também: [[03-Dominios/Java/Testes/06 - Mockito — mocks, stubbing e matchers|Mockito]].

### Mockito
Framework de mocks de facto do Java: cria dublês programáveis (`when().thenReturn()`) e verificáveis (`verify()`); integra via `MockitoExtension`.

Veja também: [[03-Dominios/Java/Testes/06 - Mockito — mocks, stubbing e matchers|Mockito]].

### @MockitoBean
Anotação do Spring Boot (3.4+) que substitui um bean do contexto de teste por um mock do Mockito; substituiu o `@MockBean` (deprecated).

Veja também: [[03-Dominios/Java/Testes/08 - Spring Boot Test e os slices — o contexto de teste|Spring Boot Test e os slices]].

### MockMvc
Cliente de teste do Spring que dispara requests contra a camada web sem subir um servidor (`perform(...).andExpect(status()/jsonPath())`); o coração do `@WebMvcTest`.

Veja também: [[03-Dominios/Java/Testes/09 - @WebMvcTest — testando controllers com MockMvc|@WebMvcTest]].

### MockRestServiceServer
Servidor de mock do Spring Test pra `RestClient`/`RestTemplate` (`@RestClientTest`): casa requests esperados e devolve respostas stub, sem HTTP real.

Veja também: [[03-Dominios/Java/Testes/16 - Mockando HTTP externo — WireMock e MockRestServiceServer|Mockando HTTP externo]].

### Modena
User-agent stylesheet padrão do JavaFX desde a versão 8, que define a aparência base de todos os controles. É um arquivo CSS interno que pode ser consultado e sobrescrito pelas folhas da aplicação. Substitui o Caspian (padrão no JavaFX 2) e serve como ponto de partida para temas customizados.

Veja também: [[09 - CSS em JavaFX]].

### @Modifying
Anotação do Spring Data que marca uma `@Query` como UPDATE/DELETE em massa; use `@Modifying(clearAutomatically = true, flushAutomatically = true)` porque o persistence context (1º nível) não é invalidado automaticamente. Veja também: [[03-Dominios/Java/Persistência de dados/09 - Consultas com @Query — JPQL, native e @Modifying|Consultas com @Query]].

### modular monolith (monólito modular)
Arquitetura de um único processo (deploy único) internamente dividido em módulos bem isolados, com fronteiras explícitas e baixo acoplamento. Captura boa parte dos benefícios organizacionais dos microservices sem a complexidade distribuída — frequentemente o ponto de partida e o destino recomendado antes de fragmentar.

Veja também: [[03-Dominios/Java/Microservices e sistemas distribuídos/23 - Quando NÃO fazer microservices|Quando NÃO fazer microservices]].

### Monitor (intrinsic lock)
Mecanismo de sincronização intrínseco de todo objeto Java que combina exclusão mútua e comunicação via `wait/notify/notifyAll`. Cada objeto tem um lock implícito adquirido com `synchronized`. Ao entrar em um bloco `synchronized`, a thread adquire o monitor; ao sair, libera-o automaticamente.

Veja também: [[03 - Exclusão mútua com synchronized]].

### Mono
Publisher do Project Reactor que representa 0-1 elemento assíncrono (`Mono<T>`). É o tipo usado quando a operação produz no máximo um valor — uma busca por id, um POST, um `count`; complementa o `Flux` (0-N).

Veja também: [[03-Dominios/Java/Programação Reativa/03 - Mono e Flux — os publishers do Project Reactor|Mono e Flux]].

### monorepo
Estratégia de versionamento em que vários serviços (ou todos) convivem num único repositório. Facilita refatorações atômicas cross-serviço e compartilhamento de código, ao custo de tooling de build mais sofisticado e acoplamento de CI.

Veja também: [[03-Dominios/Java/Microservices e sistemas distribuídos/02 - Monorepo vs multi-repo|Monorepo vs multi-repo]].

### mTLS (TLS mútuo)
TLS mútuo: ambas as pontas de uma conexão se autenticam por certificado, não só o servidor. Em microservices, garante que apenas serviços de identidade conhecida conversem entre si; normalmente entregue de forma transparente pelo service mesh.

Veja também: [[03-Dominios/Java/Microservices e sistemas distribuídos/22 - Service mesh — quando a resiliência sai do código|Service mesh]], [[03-Dominios/Java/Microservices e sistemas distribuídos/17 - Segurança entre serviços|Segurança entre serviços]].

### multi-module (reactor)
Projeto Maven composto de vários módulos sob um parent POM. O reactor analisa as dependências entre os módulos e os ordena topologicamente, buildando-os na ordem correta em uma única invocação.

Veja também: [[03-Dominios/Java/Build e tooling/12 - Projetos multi-módulo|Projetos multi-módulo]].

### multi-repo
Estratégia de versionamento com um repositório por serviço. Reforça a autonomia e o deploy independente de cada equipe, ao custo de coordenar mudanças que atravessam serviços e duplicar configuração de build/CI.

Veja também: [[03-Dominios/Java/Microservices e sistemas distribuídos/02 - Monorepo vs multi-repo|Monorepo vs multi-repo]].

### multi-stage build
Dockerfile com mais de um estágio `FROM`: estágios iniciais compilam/empacotam o app com todo o toolchain, e o estágio final copia apenas o artefato pronto para uma imagem base mínima. O resultado é uma imagem enxuta, sem compilador nem dependências de build.

Veja também: [[03-Dominios/Java/Cloud-native e produção/04 - Dockerfile na prática — multi-stage e layered jar|Dockerfile na prática — multi-stage e layered jar]].

### mutation testing
Técnica que mede a qualidade dos testes mutando o bytecode (ex.: `>`→`>=`) e checando se os testes pegam o mutante; mutation coverage é métrica mais honesta que line coverage. Em Java, PIT.

Veja também: [[03-Dominios/Java/Testes/17 - Mutation testing — PIT e cobertura honesta|Mutation testing — PIT]].

### Mutual exclusion (exclusão mútua)
Propriedade que garante que apenas uma thread por vez execute uma seção crítica de código que acessa estado compartilhado. Implementada em Java por `synchronized`, `ReentrantLock` ou semáforos com 1 permissão. Previne condições de corrida ao serializar o acesso.

Veja também: [[03 - Exclusão mútua com synchronized]].

### MVVM
Padrão arquitetural (Model-View-ViewModel) adaptado para JavaFX: o ViewModel expõe `Property` observáveis que a View conecta via binding bidirecional, sem referência direta ao Model. Permite testar a lógica de apresentação sem instanciar nós de UI, e mantém o controller FXML como cola mínima entre View e ViewModel.

Veja também: [[11 - Arquitetura — MVC, MVVM e injeção de dependência]].

## N

### N+1 (problema)
O bug de performance mais comum da JPA: ao carregar N entidades pai e acessar uma associação lazy de cada uma, geram-se 1 (pai) + N (filhos) queries. Resolve-se com `@EntityGraph`, `JOIN FETCH`, `@BatchSize` ou DTO projection. Veja também: [[03-Dominios/Java/Persistência de dados/08 - O problema N+1 e suas soluções — @EntityGraph, JOIN FETCH, batch size|O problema N+1]].

### native image
Executável nativo compilado ahead-of-time pelo GraalVM, que embute o app e um runtime mínimo num único binário, sem JVM em runtime. Startup quase instantâneo e footprint de memória baixo, ao custo de build mais lento, ausência de JIT e a closed-world assumption.

Veja também: [[03-Dominios/Java/Cloud-native e produção/08 - GraalVM Native Image — conceito e trade-offs|GraalVM Native Image — conceito e trade-offs]].

### nearest-wins (mediation)
Estratégia de dependency mediation do Maven: quando a árvore traz a mesma dependência em versões diferentes, vence a declaração mais próxima da raiz (menor profundidade), não a versão mais nova. O Gradle, por contraste, escolhe a versão mais alta.

Veja também: [[03-Dominios/Java/Build e tooling/10 - Resolução de dependências e conflitos de versão|Resolução de dependências e conflitos]].

### @Nested
Anotação do JUnit 5 que agrupa testes relacionados numa classe interna não-estática, dando estrutura e nomes de cenário (`@Nested @DisplayName "when order is pending"`).

Veja também: [[03-Dominios/Java/Testes/04 - Testes parametrizados e organização|Testes parametrizados e organização]].

### NFTC (No-Fee Terms and Conditions)
Licença da Oracle, vigente desde 2021, sob a qual o Oracle JDK é gratuito para uso em produção a partir da versão 17 — incluindo uso comercial, durante o período de release + um ano. Distinta da licença comercial paga das versões anteriores.

Veja também: [[03-Dominios/Java/Build e tooling/09 - Distribuições do JDK e o ecossistema|Distribuições do JDK]].

### Nimbus
Look and Feel vetorial bundled no JDK desde o Java 7, alternativa ao Metal padrão. Renderiza os componentes com formas suaves e escala melhor em diferentes resoluções de tela. Configurável via `UIManager.put` para ajustes de cores e fontes.

Veja também: [[03-Dominios/Java/Swing/09 - Look and Feel e temas|Look and Feel]].

### NMT (Native Memory Tracking)
Funcionalidade do HotSpot que rastreia o uso de memória nativa da JVM categorizado por subsistema (heap, metaspace, code cache, threads, GC, compiler…). Ativada com `-XX:NativeMemoryTracking=summary|detail`; consultada com `jcmd <pid> VM.native_memory`. Essencial para diagnosticar crescimento de memória fora do heap.

Veja também: [[12 - Diagnóstico — heap dumps, thread dumps e jcmd]].

### non-blocking I/O
Modelo de I/O em que a thread não fica parada esperando a resposta: ela é liberada e retomada por callback quando o dado chega. É a base do modelo reativo e do WebFlux — permite que poucos threads sustentem muitas conexões concorrentes, ao contrário do I/O bloqueante thread-por-request.

Veja também: [[03-Dominios/Java/Programação Reativa/01 - O que é programação reativa — o modelo push, assíncrono e não-bloqueante|O que é programação reativa]].

## O

### OAuth2 Client
Lado do Spring Security em que a app **consome** um provedor OAuth2/OIDC (login social): `oauth2Login`, `OidcUser`/`OAuth2User`. Contrasta com o Resource Server, que valida tokens.

Veja também: [[03-Dominios/Java/Segurança/12 - OAuth2 e OIDC Client e os grant types|OAuth2 e OIDC Client]].

### OAuth2 Resource Server
Configuração em que a API **valida** JWTs emitidos por um IdP (`issuer-uri`/`jwk-set-uri`); o cenário mais comum de API stateless.

Veja também: [[03-Dominios/Java/Segurança/09 - OAuth2 Resource Server — validando JWT na API|OAuth2 Resource Server]].

### ObservableList
Implementação de `List` do JavaFX (`javafx.collections.ObservableList`) que dispara notificações de mudança (`ListChangeListener`) sempre que elementos são adicionados, removidos ou substituídos. É a coleção-base de controles como `ListView` e `TableView`, garantindo que a UI reflita automaticamente alterações nos dados.

Veja também: [[08 - TableView, cell factories e dados observáveis]].

### @Observes / eventos CDI
Mecanismo de pub/sub embutido no CDI: um bean dispara um evento (`Event<T>.fire`/`fireAsync`) e métodos observadores marcados com `@Observes`/`@ObservesAsync` reagem — desacoplando emissor e ouvintes sem dependência direta. Alfabetiza como "Observes".

Veja também: [[03-Dominios/Java/Jakarta EE/06 - CDI — qualifiers, producers e eventos|CDI — qualifiers, producers e eventos]].

### OCI image
Formato padrão de imagem de container especificado pela Open Container Initiative, independente do Docker. Define como as camadas, o manifesto e a configuração de uma imagem são empacotados, de modo que qualquer runtime compatível (Docker, containerd, Podman) a execute.

Veja também: [[03-Dominios/Java/Cloud-native e produção/03 - Empacotando o app numa imagem — o panorama|Empacotando o app numa imagem — o panorama]].

### OIDC (OpenID Connect)
Camada de **identidade** sobre o OAuth2: adiciona o `id_token` (um JWT que identifica o usuário). OAuth2 delega acesso; OIDC autentica.

Veja também: [[03-Dominios/Java/Segurança/12 - OAuth2 e OIDC Client e os grant types|OAuth2 e OIDC Client]].

### onBackpressureBuffer / Drop / Latest
Estratégias de overflow do Reactor para quando o produtor é mais rápido que o consumidor: `onBackpressureBuffer` enfileira o excedente (com risco de OOM), `onBackpressureDrop` descarta o que não cabe, e `onBackpressureLatest` mantém apenas o elemento mais recente.

Veja também: [[03-Dominios/Java/Programação Reativa/09 - Backpressure — request(n) e as estratégias BUFFER, DROP, LATEST|Backpressure]].

### onErrorResume / onErrorReturn
Operadores de recuperação reativa: `onErrorResume` substitui o erro por um publisher de fallback (ex.: buscar de um cache), enquanto `onErrorReturn` substitui por um valor fixo. Ambos transformam um sinal de erro num caminho alternativo de sucesso.

Veja também: [[03-Dominios/Java/Programação Reativa/07 - Error handling reativo — onErrorResume, onErrorReturn, retry|Error handling reativo]].

### OOM-kill (OOMKilled)
Quando o kernel Linux mata um processo que ultrapassou o limite de memória do cgroup do container; no Kubernetes o pod aparece como `OOMKilled`. Não há `OutOfMemoryError` nem stack trace Java — o processo simplesmente recebe um `SIGKILL`, daí a importância de dimensionar o heap dentro do limite.

Veja também: [[03-Dominios/Java/Cloud-native e produção/02 - A JVM dentro de um container|A JVM dentro de um container]].

### OpenAPI
Especificação aberta (antiga Swagger Specification) para descrever APIs REST de forma legível por máquina — endpoints, parâmetros, schemas, respostas e segurança — em JSON ou YAML. Serve de contrato e alimenta ferramentas de documentação (Swagger UI), geração de clientes e testes. No Spring Boot é gerada automaticamente pelo springdoc-openapi.

Veja também: [[03-Dominios/Java/Web e APIs REST/12 - Documentando a API com OpenAPI e Swagger|Documentando a API com OpenAPI e Swagger]].

### OpenJDK
A implementação de referência open-source do Java SE, sob licença GPLv2+CPE. É a base de código a partir da qual todas as distribuições do JDK (Temurin, Corretto, Oracle JDK, etc.) são construídas.

Veja também: [[03-Dominios/Java/Build e tooling/09 - Distribuições do JDK e o ecossistema|Distribuições do JDK]].

### OpenJFX
Projeto open-source que abriga o código-fonte do JavaFX desde que foi desacoplado do JDK no Java 11. Mantido pela comunidade com contribuições da Gluon, Oracle e outros, disponibilizado em [openjfx.io](https://openjfx.io). Distribuído como módulos separados adicionados ao projeto via Maven/Gradle.

Veja também: [[14 - JavaFX hoje — estado do projeto e Swing vs JavaFX]].

### OpenTelemetry
Padrão vendor-neutral da CNCF para telemetria (traces, métricas, logs): define APIs, SDKs e o protocolo de transporte OTLP, desacoplando a instrumentação do backend de observabilidade (Jaeger, Tempo, Datadog etc.). No Java, integra-se ao Micrometer Tracing via bridge.

Veja também: [[03-Dominios/Java/Microservices e sistemas distribuídos/19 - Tracing distribuído II — exportando o trace|Tracing distribuído II — exportando o trace]].

### OpenTelemetry Collector
Processo intermediário, fora da aplicação, que recebe telemetria via OTLP, a processa (filtragem, enriquecimento, tail sampling) e a exporta para um ou mais backends. Centraliza a política de sampling e desacopla as apps dos destinos de observabilidade.

Veja também: [[03-Dominios/Java/Cloud-native e produção/16 - OpenTelemetry Collector e sampling de produção|OpenTelemetry Collector e sampling de produção]].

### operação intermediária / terminal
Classificação das operações de uma `Stream`. Operações *intermediárias* (ex.: `filter`, `map`, `sorted`) retornam uma nova stream e são *lazy* — não processam elementos até que uma operação terminal seja chamada. Operações *terminais* (ex.: `collect`, `forEach`, `count`, `reduce`) desencadeiam o processamento do pipeline e consomem a stream, que não pode ser reutilizada.

Veja também: [[03-Dominios/Java/Collections e Streams/05 - Introdução à Stream API|Stream API]].

### Optional
Container que pode ou não conter um valor não-nulo, introduzido no Java 8. Evita `NullPointerException` ao forçar o tratamento explícito da ausência de valor. Métodos principais: `isPresent`, `get`, `orElse`, `orElseGet`, `orElseThrow`, `map`, `flatMap`, `ifPresent`. Deve ser usado como tipo de retorno, nunca como campo ou parâmetro.

Veja também: [[03-Dominios/Java/Collections e Streams/10 - Optional|Optional]].

### OTLP
OpenTelemetry Protocol: o formato e o transporte padrão (sobre gRPC ou HTTP) pelo qual dados de telemetria do OpenTelemetry são exportados de uma aplicação para um collector ou backend de observabilidade.

Veja também: [[03-Dominios/Java/Microservices e sistemas distribuídos/19 - Tracing distribuído II — exportando o trace|Tracing distribuído II — exportando o trace]].

### outbox pattern
Padrão para garantir consistência entre persistência e publicação de mensagens: em vez de chamar o broker diretamente após salvar, o código persiste o evento em uma tabela `outbox` dentro da mesma transação de banco. Um processo separado (poller ou Debezium CDC) lê a tabela e publica as mensagens, assegurando que "ou salva e publica, ou não faz nenhum dos dois".

Veja também: [[03-Dominios/Java/Mensageria/21 O padrão Outbox|O padrão Outbox]].

### Overloading
Definição de múltiplos métodos com o mesmo nome mas assinaturas diferentes (quantidade ou tipos de parâmetros) em uma mesma classe. A resolução acontece em tempo de compilação com base nos tipos dos argumentos. Não deve ser confundido com overriding.

Veja também: [[07 - Herança e polimorfismo]].

### Overriding
Redefinição de um método herdado em uma subclasse, mantendo a mesma assinatura. Anotado com `@Override` para verificação do compilador. É o mecanismo base do polimorfismo dinâmico em Java — a JVM escolhe a implementação em tempo de execução pelo tipo real do objeto.

Veja também: [[07 - Herança e polimorfismo]].

### OWASP Top 10
Lista de referência das dez categorias de risco mais críticas em aplicações web (edição 2025: A01 Broken Access Control, A02 Security Misconfiguration, ...); guia de conscientização, não checklist exaustivo.

Veja também: [[03-Dominios/Java/Segurança/16 - OWASP Top 10 no contexto Java|OWASP Top 10 no contexto Java]].

## P

### PACELC
Extensão do teorema CAP: além do trade-off C/A sob partição (P), considera o caso sem partição (Else) — em que a escolha passa a ser entre menor latência (L) e maior consistência (C). Captura que o trade-off latência×consistência existe mesmo quando a rede está saudável.

Veja também: [[03-Dominios/Java/Microservices e sistemas distribuídos/20 - Consistência em sistemas distribuídos|Consistência em sistemas distribuídos]].

### Pact
Ferramenta de contract testing consumer-driven pra JVM: o consumer gera o pact, o producer verifica (`@Provider`/`@State`); a quebra falha no build sem E2E.

Veja também: [[03-Dominios/Java/Testes/20 - Contract testing — Pact|Contract testing — Pact]].

### Pageable / Page / Slice
Abstrações de paginação do Spring Data: `Pageable`/`PageRequest` definem página+tamanho+ordenação; `Page<T>` traz o total (query `count` extra); `Slice<T>` só sabe se há próxima página (sem count, mais barato). Veja também: [[03-Dominios/Java/Persistência de dados/11 - Paginação e ordenação — Pageable, Page e Slice|Paginação e ordenação]].

### paintComponent / custom painting
Método a sobrescrever (em vez de `paint`) para desenhar conteúdo customizado em um componente Swing. Deve chamar `super.paintComponent(g)` antes de desenhar e fazer cast de `Graphics` para `Graphics2D` para acessar a API completa de renderização Java2D.

Veja também: [[03-Dominios/Java/Swing/10 - Custom painting e componentes customizados|Custom painting]].

### Paketo Buildpacks
Implementação de Cloud Native Buildpacks mantida pela comunidade, usada por padrão pelo `spring-boot:build-image` para gerar a imagem de container do app sem Dockerfile. Detecta a stack JVM e monta camadas otimizadas automaticamente.

Veja também: [[03-Dominios/Java/Cloud-native e produção/06 - Buildpacks — imagem sem Dockerfile|Buildpacks — imagem sem Dockerfile]].

### @ParameterizedTest
Anotação do JUnit 5 que roda o mesmo teste com vários inputs vindos de uma source (`@ValueSource`/`@CsvSource`/`@MethodSource`/`@EnumSource`).

Veja também: [[03-Dominios/Java/Testes/04 - Testes parametrizados e organização|Testes parametrizados e organização]].

### PasswordEncoder
Interface do Spring Security para hash de senha: `encode` (gera) e `matches` (confere). Nunca há decode — hash é one-way.

Veja também: [[03-Dominios/Java/Segurança/04 - Password encoding — BCrypt, Argon2 e o DelegatingPasswordEncoder|Password encoding]].

### @PathVariable
Annotation do Spring MVC que vincula um segmento variável do path da URL a um parâmetro do método handler. Declarado no mapeamento como `{id}` (ex.: `@GetMapping("/users/{id}")`) e capturado com `@PathVariable Long id`. Usado para identificar o recurso na própria URL, no estilo REST.

Veja também: [[03-Dominios/Java/Web e APIs REST/03 - Recebendo dados da request|Recebendo dados da request]].

### Pattern matching
Mecanismo que combina teste de tipo, extração de componentes e (opcionalmente) uma guarda em uma única expressão coesa. A partir do Java 16 (`instanceof`) e Java 21 (switch patterns), elimina casts manuais e torna o código mais legível e seguro.

Veja também: [[14 - Sealed classes e pattern matching]].

### PECS
Producer Extends, Consumer Super — regra mnemônica para uso de wildcards em Generics. Use `? extends T` quando a coleção é fonte de dados (apenas leitura); use `? super T` quando a coleção é destino (apenas escrita). Define qual operação é type-safe em cada contexto.

Veja também: [[12 - Generics em profundidade]].

### persistence context
Conjunto de entidades managed que o EntityManager rastreia: funciona como identity map (um id ↔ uma instância) e unit of work (acumula mudanças até o flush). Entender suas transições explica a maioria dos "bugs de JPA".

Veja também: [[03-Dominios/Java/Jakarta EE/10 - EntityManager e o ciclo de vida da entidade|EntityManager e o ciclo de vida da entidade]].

### persistence context (1º nível)
O ângulo operacional do persistence context: atua como cache de 1º nível por transação — entidades managed têm identidade (mesma query 2x = 1 SQL) e dirty checking (mudança gera UPDATE no flush, sem `save()`). Complementa o conceito da spec (verbete `persistence context`). Veja também: [[03-Dominios/Java/Persistência de dados/03 - O persistence context e os estados da entidade|O persistence context e os estados da entidade]].

### persistence unit / persistence.xml
Unidade de configuração da JPA (declarada em `persistence.xml` ou, na 3.2, via `PersistenceConfiguration` programática): define o provider, o datasource, as entidades e o tipo de transação (JTA ou resource-local). É o que liga `@Entity` a um provider real.

Veja também: [[03-Dominios/Java/Jakarta EE/09 - JPA — a especificação de persistência|JPA — a especificação de persistência]].

### pessimistic locking
Bloqueio explícito no banco (`@Lock(LockModeType.PESSIMISTIC_WRITE)` → `SELECT ... FOR UPDATE`) que segura o lock até o commit; usado quando conflitos de escrita são frequentes. Cuidado com deadlocks (adquira locks em ordem consistente). Veja também: [[03-Dominios/Java/Persistência de dados/13 - Locking — optimistic (@Version) e pessimistic|Locking]].

### phase (Maven)
Uma etapa do lifecycle do Maven (ex.: `compile`, `test`, `package`). Cada phase dispara os goals dos plugins ligados a ela; invocar uma phase executa, em cadeia, todas as phases anteriores do mesmo lifecycle.

Veja também: [[03-Dominios/Java/Build e tooling/02 - Maven — POM, coordenadas e lifecycle|Maven — lifecycle]].

### PKCE / authorization code
Authorization Code é o fluxo OAuth2 recomendado (redirect → code → token); o PKCE (Proof Key for Code Exchange) o protege em clientes públicos (SPA/mobile) dispensando o client secret.

Veja também: [[03-Dominios/Java/Segurança/12 - OAuth2 e OIDC Client e os grant types|OAuth2 e OIDC Client]].

### Pinning
Fenômeno em que uma virtual thread fica "presa" ao seu carrier thread durante um bloco `synchronized` ou chamada nativa, impedindo que o carrier execute outras virtual threads enquanto aguarda. Reduz a escalabilidade de virtual threads; mitigado substituindo `synchronized` por `ReentrantLock` ou eliminando bloqueios em seções críticas.

Veja também: [[12 - Virtual Threads e Project Loom]].

### PIT (Pitest)
Ferramenta de mutation testing pra Java (`pitest-maven` + `pitest-junit5-plugin`): muta o bytecode e reporta a mutation coverage; lento, roda no nightly.

Veja também: [[03-Dominios/Java/Testes/17 - Mutation testing — PIT e cobertura honesta|Mutation testing — PIT]].

### Platform.runLater
Método estático do JavaFX (`Platform.runLater(Runnable)`) que agenda a execução de um `Runnable` na JavaFX Application Thread de forma assíncrona. Deve ser usado sempre que código de uma background thread precisar atualizar nós do grafo de cena; análogo ao `SwingUtilities.invokeLater` do Swing.

Veja também: [[10 - A JavaFX Application Thread — Task, Service e Platform.runLater]].

### pluggable look-and-feel
Arquitetura do Swing em que a renderização de cada componente é delegada a um UI delegate (`ComponentUI`), separando o modelo/lógica da apresentação visual. Permite trocar toda a aparência da aplicação via `UIManager.setLookAndFeel` sem alterar o código da aplicação.

Veja também: [[03-Dominios/Java/Swing/09 - Look and Feel e temas|Look and Feel]].

### pointcut
Expressão que seleciona *onde* um advice deve ser aplicado — quais join points (no Spring AOP, execuções de método) são interceptados. Escrito na linguagem de pointcut do AspectJ (ex.: `execution(* com.app.service.*.*(..))`), pode ser nomeado com `@Pointcut` e reutilizado por vários advices.

Veja também: [[03-Dominios/Java/Spring Core e Boot/09 - AOP e proxies no Spring|AOP e proxies no Spring]].

### point-to-point (queue)
Modelo de mensageria em que cada mensagem é entregue a **um único consumidor**: o primeiro que consome a mensagem do canal a remove da fila. Garante processamento exclusivo e distribui carga entre consumidores competidores. Equivale ao conceito de `Queue` no JMS e às partições Kafka com um único consumer group.

Veja também: [[03-Dominios/Java/Mensageria/02 Os modelos de mensageria — queue vs topic|Os modelos de mensageria — queue vs topic]].

### Polimorfismo
Capacidade de um mesmo método ou referência se comportar de maneiras diferentes conforme o tipo real do objeto em tempo de execução. Em Java, é realizado principalmente por overriding + herança/interface. Permite escrever código genérico que opera sobre famílias de tipos.

Veja também: [[07 - Herança e polimorfismo]].

### POM (Project Object Model)
O `pom.xml`: o descritor declarativo de um projeto Maven. Define coordenadas GAV, dependências, plugins, propriedades e herança de parent — a fonte única da configuração do build.

Veja também: [[03-Dominios/Java/Build e tooling/02 - Maven — POM, coordenadas e lifecycle|Maven — POM, coordenadas e lifecycle]].

### portable extension (CDI)
Ponto de extensão do container CDI (SPI `Extension`): um bean observa eventos do bootstrap (`ProcessAnnotatedType` etc.) para adicionar/modificar beans programaticamente — é como frameworks se integram ao CDI. No CDI Lite, o equivalente build-time é a build compatible extension.

Veja também: [[03-Dominios/Java/Jakarta EE/13 - CDI avançado — interceptors, decorators e extensões|CDI avançado]].

### @PreAuthorize / @PostAuthorize
Anotações de method security que avaliam uma expressão SpEL antes (`@PreAuthorize`) ou depois (`@PostAuthorize`) da execução do método; rodam sobre o proxy AOP, logo só funcionam em método `public` chamado de fora.

Veja também: [[03-Dominios/Java/Segurança/07 - Method security — @PreAuthorize, @PostAuthorize e SpEL|Method security]].

### Preview feature
Funcionalidade completa de linguagem ou JVM incluída em uma versão do Java para coleta de feedback, mas não finalizada. Precisa ser habilitada explicitamente com `--enable-preview` em compilação e execução. Pode mudar ou ser removida antes de tornar-se permanente.

Veja também: [[15 - A evolução do Java (8 a 25)]].

### @Primary
Annotation do Spring que marca um bean como a escolha preferencial quando há múltiplos candidatos do mesmo tipo e nenhum `@Qualifier` desambigua. Define o "padrão" da injeção; um `@Qualifier` explícito ainda pode sobrepor a preferência. Alfabetiza como "Primary".

Veja também: [[03-Dominios/Java/Spring Core e Boot/08 - Qualificação de beans — @Qualifier, @Primary, @Profile|Qualificação de beans]].

### PriorityQueue
Fila (`java.util.PriorityQueue<E>`) que entrega elementos na ordem definida pelo `Comparator` fornecido ou pela ordenação natural (`Comparable`). Internamente implementada como heap binário. Não garante ordem de iteração, apenas que `poll()` retorna sempre o menor (ou maior) elemento segundo o critério configurado.

Veja também: [[03-Dominios/Java/Collections e Streams/02 - Listas, conjuntos e filas|Listas, conjuntos e filas]].

### probe (Kubernetes)
Sonda que o Kubernetes usa para inspecionar a saúde de um pod e decidir o que fazer com ele. Há três tipos: liveness (reiniciar se travou), readiness (mandar ou não tráfego) e startup (esperar a inicialização lenta antes das outras sondas valerem).

Veja também: [[03-Dominios/Java/Cloud-native e produção/10 - Health e probes — o contrato com o orquestrador|Health e probes — o contrato com o orquestrador]].

### ProblemDetail (RFC 9457)
Formato padronizado de corpo de erro HTTP definido pela RFC 9457 (antiga RFC 7807): um objeto com campos `type`, `title`, `status`, `detail` e `instance`, servido como `application/problem+json`. O Spring 6 traz a classe `ProblemDetail` e suporte nativo (`ResponseEntityExceptionHandler`) para devolver erros nesse formato, padronizando as respostas de falha da API.

Veja também: [[03-Dominios/Java/Web e APIs REST/10 - Problem Details — RFC 9457|Problem Details — RFC 9457]].

### Processor (Reactive Streams)
Interface que é `Publisher` e `Subscriber` ao mesmo tempo — um estágio intermediário que consome um fluxo e reemite outro. Raramente usada diretamente no código de aplicação; operadores e `Sinks` cobrem a maioria dos casos. Alfabetiza como "Processor".

Veja também: [[03-Dominios/Java/Programação Reativa/02 - Reactive Streams — a spec das 4 interfaces e o Flow do Java 9|Reactive Streams]].

### @Produces (producer CDI)
Method/field producer do CDI (`jakarta.enterprise.inject.Produces`) que fabrica um objeto que o container não criaria sozinho (libs de terceiros, valores de config); `@Disposes` faz o cleanup. NÃO confundir com o `@Produces` do JAX-RS (`jakarta.ws.rs.Produces`), que declara media types. Alfabetiza como "Produces".

Veja também: [[03-Dominios/Java/Jakarta EE/06 - CDI — qualifiers, producers e eventos|CDI — qualifiers, producers e eventos]].

### @Profile (Spring)
Annotation do Spring que condiciona o registro de um bean (ou de uma classe `@Configuration`) à ativação de um ou mais profiles. Profiles (`dev`, `prod`, `test`...) são ativados via `spring.profiles.active` e permitem variar a configuração por ambiente. Alfabetiza como "Profile".

Veja também: [[03-Dominios/Java/Spring Core e Boot/12 - Configuração e profiles|Configuração e profiles]].

### Project Reactor
Biblioteca reativa da Pivotal/VMware que implementa a spec Reactive Streams e fornece os tipos `Mono` e `Flux` com um vasto conjunto de operadores. É a base sobre a qual o Spring WebFlux é construído. Alfabetiza como "Project".

Veja também: [[03-Dominios/Java/Programação Reativa/01 - O que é programação reativa — o modelo push, assíncrono e não-bloqueante|O que é programação reativa]].

### projection (JPA)
Trazer só um subconjunto de campos em vez da entidade inteira, via interface projection (proxy do Spring), class-based/DTO (`record` com `SELECT new`) ou dynamic (`Class<T>`). Ideal para listagens read-only. Veja também: [[03-Dominios/Java/Persistência de dados/10 - Projections e DTOs — não vazar a entidade|Projections e DTOs]].

### Prometheus
Banco de séries temporais e sistema de monitoramento que coleta métricas por scraping: faz pull periódico do endpoint `/actuator/prometheus` da aplicação. Armazena as séries e oferece a linguagem de consulta PromQL, consumida por dashboards (Grafana) e regras de alerta.

Veja também: [[03-Dominios/Java/Cloud-native e produção/14 - Métricas em produção — Micrometer e Prometheus|Métricas em produção — Micrometer e Prometheus]].

### Property (JavaFX)
Abstração central do sistema de binding do JavaFX (`javafx.beans.property`). Uma `Property<T>` é ao mesmo tempo um `ObservableValue` (notifica listeners de invalidação de forma *lazy* ou de mudança de valor de forma *eager*) e um `WritableValue`. Subclasses concretas (`SimpleStringProperty`, `IntegerProperty`…) são usadas em beans de ViewModel para habilitar binding declarativo.

Veja também: [[07 - Properties e binding]].

### Protocol Buffers (protobuf)
Formato de serialização binária e IDL (Interface Definition Language) criado pelo Google, definido em arquivos `.proto`. Gera stubs fortemente tipados em várias linguagens. É compacto, eficiente e versionável; usado como formato de serialização padrão do gRPC e como alternativa ao Avro em ecossistemas multi-linguagem.

Veja também: [[03-Dominios/Java/Mensageria/27 Protocol Buffers — a IDL e a serialização binária|Protocol Buffers — a IDL e a serialização binária]].

### Publisher / Subscriber / Subscription
As três interfaces centrais do Reactive Streams: o `Publisher` é a fonte de dados, o `Subscriber` é o consumidor, e a `Subscription` é a ligação entre eles que carrega a demanda (`request(n)`) e o cancelamento (`cancel`). É por essa tríade que o backpressure flui.

Veja também: [[03-Dominios/Java/Programação Reativa/02 - Reactive Streams — a spec das 4 interfaces e o Flow do Java 9|Reactive Streams]].

### publishOn / subscribeOn
Operadores de troca de thread no Reactor. `subscribeOn` afeta a origem da cadeia — em qual `Scheduler` a subscription e a fonte rodam — independentemente de onde aparece no pipeline. `publishOn` troca a thread daquele ponto para baixo, afetando os operadores subsequentes.

Veja também: [[03-Dominios/Java/Programação Reativa/08 - Schedulers — subscribeOn, publishOn e em qual thread o código roda|Schedulers]].

### publish-subscribe (topic)
Modelo de mensageria em que uma mensagem publicada num canal (tópico) é entregue a **todos os assinantes** interessados. Cada consumidor (ou consumer group) recebe sua própria cópia. Promove fanout e desacoplamento; é o modelo base do Kafka (via tópico + consumer groups) e do RabbitMQ com exchanges do tipo fanout/topic.

Veja também: [[03-Dominios/Java/Mensageria/02 Os modelos de mensageria — queue vs topic|Os modelos de mensageria — queue vs topic]].

### Pyroscope (Grafana Pyroscope)
Plataforma de continuous profiling multi-tenant que coleta, armazena e visualiza perfis de toda a frota ao longo do tempo. Para aplicações Java, a coleta usa o async-profiler; os flamegraphs ficam consultáveis por serviço, período e dimensão.

Veja também: [[03-Dominios/Java/Cloud-native e produção/19 - Continuous profiling no cluster — Pyroscope e async-profiler|Continuous profiling no cluster]].

## Q

### qualifier (CDI)
Annotation (`@Qualifier`) que desambigua qual implementação injetar quando há mais de um bean do mesmo tipo (ex.: `@Pix` vs. `@CreditCard`). `@Default` e `@Any` são built-in; `@Named` é para EL, não para injeção típica.

Veja também: [[03-Dominios/Java/Jakarta EE/06 - CDI — qualifiers, producers e eventos|CDI — qualifiers, producers e eventos]].

### @Qualifier (Spring)
Annotation do Spring que desambigua qual bean injetar quando há vários candidatos do mesmo tipo, casando pelo nome/qualificador declarado. É o equivalente Spring do `@Qualifier` do CDI. Combina com `@Primary` (preferência padrão) e pode ser usado como meta-annotation para criar qualificadores customizados. Alfabetiza como "Qualifier".

Veja também: [[03-Dominios/Java/Spring Core e Boot/08 - Qualificação de beans — @Qualifier, @Primary, @Profile|Qualificação de beans]].

### @Query (JPQL/native)
Anotação do Spring Data para escrever a query explicitamente — em JPQL (sobre entidades/atributos) ou SQL nativo (`nativeQuery = true`, sobre tabelas/colunas) — quando a derived query não basta. Veja também: [[03-Dominios/Java/Persistência de dados/09 - Consultas com @Query — JPQL, native e @Modifying|Consultas com @Query]].

## R

### R2DBC
Reactive Relational Database Connectivity: a API/driver não-bloqueante para banco relacional, alternativa reativa ao JDBC. Permite acesso a banco sem segurar a thread esperando o resultado, fechando o gap entre o stack reativo e a persistência relacional.

Veja também: [[03-Dominios/Java/Programação Reativa/13 - R2DBC — persistência reativa sem EntityManager|R2DBC]].

### R2dbcRepository
Repositório do Spring Data R2DBC cujos métodos devolvem `Mono`/`Flux`; é o equivalente reativo do `JpaRepository`, mas sem ORM nem persistence context — não há dirty checking nem lazy loading, e o mapeamento é direto linha→objeto.

Veja também: [[03-Dominios/Java/Programação Reativa/13 - R2DBC — persistência reativa sem EntityManager|R2DBC]].

### @RabbitListener
Annotation do Spring AMQP aplicada a um método que o torna um consumidor de mensagens de uma fila RabbitMQ. O listener container gerencia a conexão, o thread pool e o ACK automático ou manual. Equivalente funcional do `@KafkaListener` para o ecossistema AMQP. Alfabetiza como "RabbitListener".

Veja também: [[03-Dominios/Java/Mensageria/15 Spring AMQP e RabbitMQ|Spring AMQP e RabbitMQ]].

### RabbitMQ
Message broker open-source que implementa o protocolo AMQP, com suporte adicional a MQTT e STOMP. Usa o modelo de exchanges → bindings → queues para roteamento flexível de mensagens. Amplamente adotado em microsserviços que precisam de roteamento sofisticado, confirmação de entrega e filas duráveis.

Veja também: [[03-Dominios/Java/Mensageria/15 Spring AMQP e RabbitMQ|Spring AMQP e RabbitMQ]].

### rate limiter
Padrão de resiliência que limita o número de chamadas permitidas por janela de tempo, protegendo um serviço de ser sobrecarregado e impondo cotas de uso. No Java, oferecido pelo Resilience4j (`RateLimiter`).

Veja também: [[03-Dominios/Java/Microservices e sistemas distribuídos/15 - Resiliência III — Bulkhead e Rate Limiter|Resiliência III — Bulkhead e Rate Limiter]].

### RBAC (role-based)
Controle de acesso por **papéis**: o usuário tem roles, as roles concedem permissões. Simples e cobre a maioria dos casos; o modelo default do Spring Security.

Veja também: [[03-Dominios/Java/Segurança/05 - Autorização baseada em URL — authorizeHttpRequests, roles vs authorities|Autorização baseada em URL]].

### Reactive Streams
Especificação de streams assíncronos com backpressure não-bloqueante: padroniza o contrato entre publishers e subscribers (as quatro interfaces `Publisher`/`Subscriber`/`Subscription`/`Processor`). Foi absorvida no `java.util.concurrent.Flow` no Java 9 e é implementada pelo Reactor, RxJava e Akka Streams.

Veja também: [[03-Dominios/Java/Programação Reativa/02 - Reactive Streams — a spec das 4 interfaces e o Flow do Java 9|Reactive Streams]].

### Reactor Kafka
Biblioteca da família Reactor (desenvolvida pela Confluent) que expõe a API do produtor e consumidor Kafka como `KafkaSender` e `KafkaReceiver`, devolvendo `Flux`/`Mono`. Permite integrar Kafka num pipeline reativo sem bloquear threads, aproveitando backpressure e composição de operadores.

Veja também: [[03-Dominios/Java/Mensageria/25 Mensageria reativa — Reactor Kafka|Mensageria reativa — Reactor Kafka]].

### readiness probe
Sonda do Kubernetes que pergunta "este pod pode receber tráfego agora?". Quando falha, o pod é retirado do balanceamento de carga sem ser reiniciado — útil enquanto a app aquece ou perde temporariamente uma dependência. É separada da liveness probe justamente para não reiniciar um pod que só está temporariamente indisponível.

Veja também: [[03-Dominios/Java/Cloud-native e produção/10 - Health e probes — o contrato com o orquestrador|Health e probes — o contrato com o orquestrador]].

### Record
Classe de dados imutável declarada com `record NomeClasse(Tipo campo, ...)`. O compilador gera automaticamente construtor canônico, acessores, `equals`, `hashCode` e `toString`. Ideal para portadores de dados sem lógica de negócio.

Veja também: [[13 - Records e record patterns]].

### Record pattern
Extensão de pattern matching que desconstói um record diretamente no `instanceof` ou `switch`, ligando seus componentes a variáveis locais. Permite navegação estrutural em hierarquias de dados sem getters explícitos.

Veja também: [[13 - Records e record patterns]], [[14 - Sealed classes e pattern matching]].

### refresh token
Token de longa duração (idealmente opaco e server-side) usado para obter novos access tokens curtos sem novo login; permite revogação imediata e rotação a cada uso.

Veja também: [[03-Dominios/Java/Segurança/13 - Refresh tokens e revogação de token|Refresh tokens e revogação de token]].

### reproducible build
Build determinístico: a mesma entrada (fontes + dependências + toolchain) produz bit-a-bit o mesmo artefato, independentemente de quando ou onde rodou. No Maven, exige fixar `project.build.outputTimestamp` e zerar fontes de variação (timestamps, ordem de arquivos). Permite verificar a integridade da cadeia de build.

Veja também: [[03-Dominios/Java/Build e tooling/17 - Reprodutibilidade e reproducible builds|Reprodutibilidade e reproducible builds]].

### request(n) (demanda)
O sinal pelo qual o `Subscriber` pede `n` elementos ao `Publisher` através da `Subscription`. É o mecanismo concreto do backpressure: o produtor só pode emitir até o total já demandado, e nunca além — o consumidor dita o ritmo.

Veja também: [[03-Dominios/Java/Programação Reativa/09 - Backpressure — request(n) e as estratégias BUFFER, DROP, LATEST|Backpressure]].

### @RequestBody
Annotation do Spring MVC que vincula o corpo da requisição HTTP a um parâmetro do método, desserializando-o (via `HttpMessageConverter`/Jackson) para um objeto Java. Usado em POST/PUT/PATCH para receber payloads JSON; combina com `@Valid` para disparar a Bean Validation sobre o objeto recebido. Alfabetiza como "RequestBody".

Veja também: [[03-Dominios/Java/Web e APIs REST/03 - Recebendo dados da request|Recebendo dados da request]].

### @RequestHeader
Annotation do Spring MVC que vincula o valor de um header HTTP a um parâmetro do método handler (ex.: `@RequestHeader("User-Agent") String ua`). Suporta valor default e marcação de obrigatoriedade. Alfabetiza como "RequestHeader".

Veja também: [[03-Dominios/Java/Web e APIs REST/03 - Recebendo dados da request|Recebendo dados da request]].

### @RequestMapping
Annotation base do Spring MVC que mapeia requisições HTTP para classes e métodos handler, combinando path, método HTTP, headers, params e media types (`consumes`/`produces`). Aplicada na classe define um prefixo comum; nos métodos, os atalhos `@GetMapping`/`@PostMapping` etc. são especializações por verbo. Alfabetiza como "RequestMapping".

Veja também: [[03-Dominios/Java/Web e APIs REST/02 - @RestController e os mapeamentos|@RestController e os mapeamentos]].

### @RequestParam
Annotation do Spring MVC que vincula um parâmetro de query string (ou de formulário) a um parâmetro do método (ex.: `?page=2` → `@RequestParam int page`). Suporta valor default, obrigatoriedade e binding para coleções/`Map`. Alfabetiza como "RequestParam".

Veja também: [[03-Dominios/Java/Web e APIs REST/03 - Recebendo dados da request|Recebendo dados da request]].

### Resilience4j
Biblioteca leve e modular de tolerância a falhas para Java, sucessora do Hystrix (em manutenção). Oferece Circuit Breaker, Retry, Rate Limiter, Bulkhead e Time Limiter como decorators componíveis, com integração Spring Boot. Versão atual 2.4.0.

Veja também: [[03-Dominios/Java/Microservices e sistemas distribuídos/13 - Resiliência I — a falha distribuída e o Circuit Breaker|Resiliência I — Circuit Breaker]], [[03-Dominios/Java/Microservices e sistemas distribuídos/16 - Resiliência IV — compondo os padrões|Resiliência IV — compondo os padrões]].

### @ResponseBody
Annotation do Spring MVC que indica que o retorno do método deve ser serializado direto no corpo da resposta (via `HttpMessageConverter`), em vez de ser interpretado como nome de view. É implícita em `@RestController`. Alfabetiza como "ResponseBody".

Veja também: [[03-Dominios/Java/Web e APIs REST/04 - ResponseEntity e status codes|ResponseEntity e status codes]].

### @ResponseStatus
Annotation do Spring MVC que define o status code HTTP da resposta de forma declarativa, aplicada a um método handler ou a uma classe de exceção (ex.: `@ResponseStatus(HttpStatus.NOT_FOUND)`). Alternativa estática ao `ResponseEntity` quando o status é fixo. Alfabetiza como "ResponseStatus".

Veja também: [[03-Dominios/Java/Web e APIs REST/04 - ResponseEntity e status codes|ResponseEntity e status codes]].

### RestClient
Cliente HTTP síncrono e fluente introduzido no Spring 6.1, com API moderna (`get().uri(...).retrieve()...`) que substitui o `RestTemplate` em código novo síncrono. Reusa a infraestrutura de `HttpMessageConverter` do Spring. Alfabetiza como "RestClient".

Veja também: [[03-Dominios/Java/Web e APIs REST/15 - Clientes HTTP — RestClient, WebClient, RestTemplate|Clientes HTTP — RestClient, WebClient, RestTemplate]].

### @RestController
Estereótipo do Spring que combina `@Controller` com `@ResponseBody`: marca a classe como controller web cujos métodos retornam o corpo da resposta serializado (tipicamente JSON), sem resolução de view. É o ponto de entrada padrão de uma API REST no Spring MVC. Alfabetiza como "RestController".

Veja também: [[03-Dominios/Java/Web e APIs REST/02 - @RestController e os mapeamentos|@RestController e os mapeamentos]], [[Dicionário de Java#@Component / estereótipos Spring|@Component / estereótipos Spring]].

### RestTemplate
Cliente HTTP síncrono clássico do Spring, dominante por anos para consumir APIs REST. Em modo de manutenção desde o Spring 5: ainda suportado, mas o time recomenda `RestClient` (síncrono) ou `WebClient` (reativo) para código novo. Alfabetiza como "RestTemplate".

Veja também: [[03-Dominios/Java/Web e APIs REST/15 - Clientes HTTP — RestClient, WebClient, RestTemplate|Clientes HTTP — RestClient, WebClient, RestTemplate]].

### retained mode / immediate mode
Dois paradigmas de renderização de UI. No **retained mode** (JavaFX, Swing), o framework mantém uma representação interna do estado da cena (o grafo de cena) e sabe o que redesenhar; o desenvolvedor modifica o modelo e o framework atualiza a tela. No **immediate mode** (Canvas JavaFX, OpenGL), o desenvolvedor emite comandos de desenho diretamente a cada frame, sem estado persistente gerenciado pelo framework.

Veja também: [[02 - Scene graph — stage, scene e nodes]].

### @RetryableTopic
Annotation do Spring Kafka que configura reprocessamento automático com retentativas em tópicos separados (retry topics) e, após esgotar as tentativas, encaminha a mensagem para o Dead Letter Topic (DLT). Elimina a necessidade de lógica manual de retry e DLQ, com suporte a backoff configurável. Alfabetiza como "RetryableTopic".

Veja também: [[03-Dominios/Java/Mensageria/12 Dead Letter Topic — o padrão DLQ|Dead Letter Topic — o padrão DLQ]].

### retry / retryWhen
Operadores reativos que re-subscrevem a fonte após um erro, refazendo o trabalho do zero. `retry(n)` tenta n vezes; `retryWhen(Retry.backoff(...))` adiciona espera exponencial (com jitter) entre as tentativas, evitando martelar um serviço que está se recuperando.

Veja também: [[03-Dominios/Java/Programação Reativa/07 - Error handling reativo — onErrorResume, onErrorReturn, retry|Error handling reativo]].

### Richardson Maturity Model
Modelo de Leonard Richardson que mede o quão "RESTful" é uma API em quatro níveis: nível 0 (um único endpoint, RPC sobre HTTP), nível 1 (recursos identificados por URLs), nível 2 (uso correto dos verbos HTTP e status codes) e nível 3 (HATEOAS — hipermídia guiando o cliente). Serve de régua para avaliar maturidade de design de APIs.

Veja também: [[03-Dominios/Java/Web e APIs REST/14 - HATEOAS|HATEOAS]].

### RoleHierarchy
Configuração que faz uma role herdar outra (ex.: `ROLE_ADMIN > ROLE_USER`), evitando listar todas as roles em cada regra.

Veja também: [[03-Dominios/Java/Segurança/14 - Autorização avançada — AuthorizationManager, RBAC vs ABAC|Autorização avançada]].

### rolling update
Estratégia de deploy do Kubernetes que substitui os pods da versão antiga pela nova gradualmente, alguns por vez, mantendo o serviço disponível durante a transição. Combinada com readiness probes e graceful shutdown, permite atualizar a aplicação sem downtime.

Veja também: [[03-Dominios/Java/Cloud-native e produção/12 - Graceful shutdown e deploy sem downtime|Graceful shutdown e deploy sem downtime]].

## S

### Safe publication (publicação segura)
Conjunto de técnicas que garantem que um objeto construído por uma thread seja corretamente visível por outras threads sem objetos parcialmente inicializados. Alcançada via campos `final`, `volatile`, referências em coleções thread-safe ou blocos `synchronized`. Sem safe publication, outra thread pode ver o objeto em estado incompleto.

Veja também: [[11 - Java Memory Model em profundidade]].

### safepoint
Estado global da JVM em que todas as threads Java estão em pontos de execução seguros — tipicamente paradas ou em código nativo inspecionável — permitindo que a VM execute operações que requerem visibilidade consistente do heap, como pausas de GC, recompilação JIT e deoptimização. A JVM insere verificações de safepoint em loops e chamadas; o tempo de chegada ao safepoint (*time to safepoint*, TTSP) é visível com `-Xlog:safepoint`.

Veja também: [[03 - Garbage Collection — o conceito]].

### saga
Padrão para gerenciar transações longas distribuídas por múltiplos microsserviços sem two-phase commit: a saga é uma sequência de transações locais, cada uma seguida de um evento; em caso de falha, eventos compensatórios desfazem as etapas anteriores. Pode ser implementada por coreografia (eventos reativos) ou orquestração (saga orchestrator central).

Veja também: [[03-Dominios/Java/Mensageria/22 Saga — transações distribuídas por eventos|Saga — transações distribuídas por eventos]].

### SBOM (Software Bill of Materials)
Inventário formal e legível por máquina de todos os componentes e dependências (diretas e transitivas) que compõem um artefato. Base da segurança de supply chain — permite cruzar componentes com bases de vulnerabilidades. Formatos comuns: CycloneDX e SPDX.

Veja também: [[03-Dominios/Java/Build e tooling/18 - Supply chain e SBOM|Supply chain e SBOM]].

### Scene Builder
Ferramenta visual de arrastar-e-soltar (distribuída pela Gluon) para criar arquivos FXML sem escrever XML manualmente. Permite inspecionar a hierarquia de nós, configurar propriedades e CSS, e associar controllers; gera o FXML que o `FXMLLoader` carrega em tempo de execução.

Veja também: [[06 - FXML e Scene Builder]].

### scene graph
Estrutura de dados em árvore do JavaFX que representa todos os nós visuais de uma `Scene`. Cada nó é uma instância de `Node` (shapes, controles, containers, grupos); o framework percorre o grafo para layout, renderização e hit-testing. Opera em retained mode — o desenvolvedor modifica a árvore e o runtime decide o que redesenhar.

Veja também: [[02 - Scene graph — stage, scene e nodes]].

### Scheduler (Reactor)
Abstração do Reactor para controlar em qual thread/pool um trecho do pipeline roda. As fábricas de `Schedulers` oferecem `parallel` (CPU-bound), `boundedElastic` (I/O bloqueante isolado), `single` e `immediate`. Combina-se com `publishOn`/`subscribeOn` para mover o trabalho entre threads.

Veja também: [[03-Dominios/Java/Programação Reativa/08 - Schedulers — subscribeOn, publishOn e em qual thread o código roda|Schedulers]].

### schema registry
Serviço centralizado que armazena e versiona schemas (Avro, Protobuf, JSON Schema) usados por produtores e consumidores Kafka. Garante compatibilidade de evolução (backward, forward, full) no momento do registro, evitando que uma mudança de schema quebre consumidores em produção. A implementação de referência é o Confluent Schema Registry.

Veja também: [[03-Dominios/Java/Mensageria/14 Schema e contratos — Avro e Schema Registry|Schema e contratos — Avro e Schema Registry]].

### Scoped value
Mecanismo final (permanente) do Java 25 para compartilhar dados imutáveis com threads descendentes sem passar parâmetros explicitamente, como alternativa segura e eficiente ao `ThreadLocal`. O valor é acessível apenas dentro de um escopo delimitado e não pode ser alterado após a ligação.

Veja também: [[14 - Scoped values]].

### SDKMAN
Gerenciador de versões de SDKs no ambiente local (JDK, Maven, Gradle, etc.): instala, lista e alterna distribuições por linha de comando, definindo o JDK ativo por shell ou por projeto (`.sdkmanrc`).

Veja também: [[03-Dominios/Java/Build e tooling/09 - Distribuições do JDK e o ecossistema|Distribuições do JDK]].

### Sealed class
Classe (ou interface) que restringe explicitamente quais subclasses (ou subinterfaces) podem estendê-la, usando a palavra-chave `sealed` e a cláusula `permits`. Permite ao compilador verificar exaustividade em switches e torna hierarquias fechadas e explicitamente documentadas.

Veja também: [[14 - Sealed classes e pattern matching]].

### second-level cache (2º nível)
Cache de entidades compartilhado entre transações/sessões (application-wide), opt-in no Hibernate (`@Cacheable` + `@Cache(usage = ...)`, com estratégias READ_ONLY/NONSTRICT_READ_WRITE/READ_WRITE/TRANSACTIONAL). Indicado para dados de referência lidos muito e mudados pouco. Veja também: [[03-Dominios/Java/Persistência de dados/14 - Caching — 1º nível, 2º nível e Spring Cache|Caching]].

### SecurityContextHolder
Onde o `Authentication` do usuário atual vive durante o request (um `ThreadLocal` por default); acessível via `SecurityContextHolder.getContext().getAuthentication()`.

Veja também: [[03-Dominios/Java/Segurança/02 - SecurityContext, Authentication e Principal — o usuário atual|SecurityContext, Authentication e Principal]].

### SecurityFilterChain
A cadeia ordenada de filtros de segurança aplicada a um conjunto de requests; em Spring Security 6 é um **bean** declarado com lambda DSL (substituiu o `WebSecurityConfigurerAdapter`).

Veja também: [[03-Dominios/Java/Segurança/01 - O que é Spring Security — authn, authz e o filter chain|O que é Spring Security]].

### self-invocation
Chamada de um método do próprio bean a partir de outro método dele (`this.metodo()`), que *não passa pelo proxy* — porque o proxy só intercepta chamadas externas. É a armadilha clássica do Spring AOP: `@Transactional`, `@Cacheable` ou `@Async` em um método invocado internamente são silenciosamente ignorados.

Veja também: [[03-Dominios/Java/Spring Core e Boot/10 - Self-invocation e os limites do proxy|Self-invocation e os limites do proxy]].

### Semaphore (semáforo)
Sincronizador que controla o acesso a um recurso com um número limitado de permissões. Threads adquirem permissões com `acquire()` e as devolvem com `release()`; quando todas as permissões estão em uso, novos `acquire()` bloqueiam. Útil para limitar concorrência em pools de recursos ou seções com capacidade máxima.

Veja também: [[09 - Sincronizadores]].

### separable model (MVC do Swing)
Variação do MVC adotada pelo Swing: o model (dados) é separado do componente, enquanto view e controller são fundidos no UI delegate. O desenvolvedor customiza o model (ex.: `TableModel`); raramente precisa alterar view ou controller.

Veja também: [[03-Dominios/Java/Swing/07 - MVC em Swing e os models|MVC em Swing]].

### SequencedCollection / SequencedMap
Interfaces introduzidas no Java 21 (`java.util.SequencedCollection`, `java.util.SequencedMap`) que adicionam semântica de *ordem de encontro* garantida a coleções. Fornecem métodos uniformes `getFirst`, `getLast`, `addFirst`, `addLast`, `removeFirst`, `removeLast` e `reversed()`. Implementadas por `List`, `Deque`, `LinkedHashSet`, `LinkedHashMap` e `SortedSet`/`SortedMap`.

Veja também: [[03-Dominios/Java/Collections e Streams/14 - SequencedCollection e SequencedMap|SequencedCollection]].

### @ServiceConnection
Anotação do Spring Boot (3.1+) que auto-configura a conexão (datasource, Kafka, Redis) a partir de um container Testcontainers, dispensando o `@DynamicPropertySource` manual.

Veja também: [[03-Dominios/Java/Testes/11 - Testcontainers — infra real em testes|Testcontainers]].

### service discovery
Mecanismo que permite a um serviço localizar, em tempo de execução, as instâncias (host:porta) de outro serviço, cujos endereços são dinâmicos. Resolve o problema de hardcodar endpoints num ambiente onde instâncias sobem, caem e migram.

Veja também: [[03-Dominios/Java/Microservices e sistemas distribuídos/06 - Service discovery — o conceito e o Eureka|Service discovery — o conceito e o Eureka]].

### service mesh
Malha de serviço: infraestrutura que move resiliência, mTLS, roteamento e observabilidade para fora do código da aplicação, delegando-os a proxies sidecar (data plane) coordenados por um control plane. Implementações: Istio, Linkerd.

Veja também: [[03-Dominios/Java/Microservices e sistemas distribuídos/22 - Service mesh — quando a resiliência sai do código|Service mesh — quando a resiliência sai do código]].

### service registry
Registro central das instâncias de serviço disponíveis: cada instância se cadastra (e renova via heartbeat) e os clientes o consultam para descobrir endereços. É a peça que viabiliza o service discovery. Exemplos: Eureka, Consul.

Veja também: [[03-Dominios/Java/Microservices e sistemas distribuídos/06 - Service discovery — o conceito e o Eureka|Service discovery — o conceito e o Eureka]].

### servlet
Componente Java que processa requisições HTTP dentro de um container (Servlet 6.1 no EE 11). `HttpServlet` expõe `doGet`/`doPost`...; uma única instância atende múltiplas threads concorrentes, então estado mutável de instância é perigoso. É o alicerce sobre o qual frameworks web rodam.

Veja também: [[03-Dominios/Java/Jakarta EE/03 - Servlet API — o alicerce HTTP|Servlet API — o alicerce HTTP]].

### servlet container
Runtime que gerencia o ciclo de vida de servlets e a infraestrutura HTTP (threads, sessões, mapeamento de URLs) — ex.: Tomcat, Jetty. Implementa a Servlet API mas não necessariamente a plataforma Jakarta EE completa (sem CDI/JPA nativos).

Veja também: [[03-Dominios/Java/Jakarta EE/03 - Servlet API — o alicerce HTTP|Servlet API — o alicerce HTTP]].

### session bean
Tipo de Enterprise Bean que encapsula lógica de negócio: stateless (sem estado entre chamadas, pooled), stateful (mantém estado conversacional por cliente) ou singleton (uma instância por aplicação).

Veja também: [[03-Dominios/Java/Jakarta EE/12 - EJB — o legado que moldou a plataforma|EJB — o legado que moldou a plataforma]].

### session fixation
Ataque em que o atacante fixa um session id antes do login para sequestrá-lo depois; o Spring previne migrando a sessão no login (`migrateSession`, default).

Veja também: [[03-Dominios/Java/Segurança/15 - Session management e security headers|Session management e security headers]].

### SessionCreationPolicy (STATELESS)
Política de criação de sessão; `STATELESS` (típica de APIs JWT) não cria nem usa `HttpSession` — a identidade vem no token a cada request.

Veja também: [[03-Dominios/Java/Segurança/15 - Session management e security headers|Session management e security headers]].

### Shenandoah
Coletor de lixo de pausa ultra-baixa desenvolvido pela Red Hat, disponível no OpenJDK. Realiza a fase de compactação (evacuation) concorrentemente com a aplicação, reduzindo as pausas STW a trabalho de curtíssima duração independentemente do tamanho do heap. Ativado com `-XX:+UseShenandoahGC`.

Veja também: [[06 - Os coletores do HotSpot]].

### sidecar
Proxy implantado ao lado de cada instância de serviço (no mesmo pod), que intercepta todo o tráfego de entrada e saída. É o data plane de um service mesh: aplica mTLS, retry, telemetria e roteamento sem que o serviço saiba. O Envoy é o sidecar mais comum.

Veja também: [[03-Dominios/Java/Microservices e sistemas distribuídos/22 - Service mesh — quando a resiliência sai do código|Service mesh]].

### skin (Control)
Implementação plugável da aparência e do comportamento visual de um `Control` do JavaFX. Cada controle delega layout e renderização ao seu `Skin` (ex.: `ButtonSkin`); criar um skin customizado permite reimplementar completamente a aparência sem alterar o modelo do controle. O mecanismo é análogo ao UI delegate do Swing.

Veja também: [[12 - Custom controls, Canvas e charts]].

### SLSA
Framework de níveis de integridade da cadeia de suprimentos de software (Supply-chain Levels for Software Artifacts). Define níveis crescentes de garantia sobre como um artefato foi produzido, baseados em proveniência (provenance) e attestation verificáveis.

Veja também: [[03-Dominios/Java/Build e tooling/18 - Supply chain e SBOM|Supply chain e SBOM]].

### soft assertions
Asserções que acumulam todas as falhas em vez de parar na primeira (`SoftAssertions.assertSoftly`), reportando tudo de uma vez.

Veja também: [[03-Dominios/Java/Testes/03 - AssertJ — fluent assertions|AssertJ]].

### Specification (Spring Data)
Predicado componível (`Specification<T>`) sobre a Criteria API, usado com `JpaSpecificationExecutor` para construir filtros dinâmicos (`where(...).and(...).or(...)`) — comum em APIs de busca. Veja também: [[03-Dominios/Java/Persistência de dados/15 - Consultas dinâmicas e os limites da JPA — Specifications, Criteria e SQL|Consultas dinâmicas e os limites da JPA]].

### Spring Actuator
Módulo do Spring Boot que expõe endpoints de produção (`/actuator/health`, `/metrics`, `/info`, `/env`, `/conditions`...) para monitorar e inspecionar a aplicação em runtime. Integra-se ao Micrometer para métricas e a sistemas de observabilidade; os endpoints são habilitados e protegidos seletivamente.

Veja também: [[03-Dominios/Java/Spring Core e Boot/17 - Actuator e observabilidade|Actuator e observabilidade]].

### Spring AMQP
Módulo do ecossistema Spring que abstrai a comunicação com brokers AMQP (principalmente RabbitMQ): fornece `RabbitTemplate` para envio, `@RabbitListener` para consumo e o listener container para gerenciamento de threads e conexões. Segue o mesmo padrão de abstração do Spring Kafka.

Veja também: [[03-Dominios/Java/Mensageria/15 Spring AMQP e RabbitMQ|Spring AMQP e RabbitMQ]].

### Spring AOP
Implementação de programação orientada a aspectos do Spring, baseada em *proxies* em runtime (JDK dynamic proxy ou CGLIB) — não em weaving de bytecode como o AspectJ completo. Intercepta apenas execuções de método de beans gerenciados; é o mecanismo por baixo de `@Transactional`, `@Cacheable` e `@Async`.

Veja também: [[03-Dominios/Java/Spring Core e Boot/09 - AOP e proxies no Spring|AOP e proxies no Spring]].

### Spring AOT
Processamento ahead-of-time do Spring (build-time) que "congela" o grafo de beans e avalia as condições durante a compilação, gerando código e metadados que substituem parte do trabalho reflexivo de runtime. É o que viabiliza imagens nativas com GraalVM e reduz tempo de startup e footprint de memória.

Veja também: [[03-Dominios/Java/Spring Core e Boot/15 - Auto-configuration e starters|Auto-configuration e starters]], [[03-Dominios/Java/Cloud-native e produção/09 - Native Image com Spring — Spring AOT na prática|Native Image com Spring — Spring AOT na prática]].

### Spring Boot
Camada sobre o Spring Framework que aplica *convention over configuration*: auto-configuration, starters, servidor embarcado e jars executáveis para que uma aplicação Spring suba com configuração mínima e `java -jar`. Não substitui o Spring Framework — o orquestra para reduzir boilerplate.

Veja também: [[03-Dominios/Java/Spring Core e Boot/01 - O que é Spring — Framework, Boot e o ecossistema|O que é Spring]].

### @SpringBootTest
Anotação que carrega o `ApplicationContext` completo num teste (integração); combinada com Testcontainers e `WebEnvironment`, testa o fluxo inteiro. Mais pesada que os slices.

Veja também: [[03-Dominios/Java/Testes/12 - Testes de integração ponta a ponta|Testes de integração ponta a ponta]].

### Spring Cloud
Conjunto de projetos do ecossistema Spring para construir sistemas distribuídos: service discovery, config centralizado, gateway, resiliência e tracing. Versionado por um *release train* alinhado ao Spring Boot. Vários módulos da era Netflix (Ribbon, Hystrix, Zuul) foram aposentados e substituídos.

Veja também: [[03-Dominios/Java/Microservices e sistemas distribuídos/04 - Panorama do Spring Cloud — e o que morreu|Panorama do Spring Cloud — e o que morreu]].

### Spring Cloud Config
Solução de configuração externalizada e centralizada do Spring Cloud: um Config Server serve propriedades (de Git, Vault etc.) e os Config Clients as consomem no boot, com suporte a refresh dinâmico. Realiza o fator "config" dos 12 fatores.

Veja também: [[03-Dominios/Java/Microservices e sistemas distribuídos/12 - Config centralizado — Spring Cloud Config|Config centralizado — Spring Cloud Config]].

### Spring Cloud Gateway
API Gateway do ecossistema Spring, baseado em rotas com *predicates* (condições de match) e *filters* (transformações). Existe em duas variantes: a reativa (sobre WebFlux/Netty) e a Spring Cloud Gateway MVC (sobre o stack servlet bloqueante).

Veja também: [[03-Dominios/Java/Microservices e sistemas distribuídos/10 - API Gateway — papel, roteamento, predicates e filters|API Gateway]], [[03-Dominios/Java/Microservices e sistemas distribuídos/11 - Gateway reativo vs MVC — as duas variantes|Gateway reativo vs MVC]].

### Spring Cloud LoadBalancer
Componente de client-side load balancing do Spring Cloud, que substituiu o Netflix Ribbon (aposentado). Distribui as requisições entre as instâncias descobertas via service discovery, com estratégias plugáveis (round-robin por padrão).

Veja também: [[03-Dominios/Java/Microservices e sistemas distribuídos/08 - Client-side load balancing — Spring Cloud LoadBalancer|Client-side load balancing]].

### Spring Cloud Stream
Framework do ecossistema Spring Cloud que abstrai a integração com brokers de mensagens (Kafka, RabbitMQ) por meio de *binders* e *bindings* declarativos. O código da aplicação trabalha com `Supplier`, `Function` e `Consumer` Java; o binder cuida da conexão com o broker específico. Facilita a troca de broker sem alterar a lógica de negócio.

Veja também: [[03-Dominios/Java/Mensageria/17 Spring Cloud Stream — a abstração de binders|Spring Cloud Stream — a abstração de binders]].

### Spring Data JPA
Camada do Spring sobre a JPA/Hibernate que elimina o boilerplate do repositório: interfaces `JpaRepository`, queries derivadas, paginação, projections e Specifications. Veja também: [[03-Dominios/Java/Persistência de dados/01 - O que é a camada de persistência — Spring Data, JPA e Hibernate|O que é a camada de persistência]].

### Spring Framework
O núcleo do ecossistema Spring: container IoC/DI, AOP, abstração de transações, suporte a MVC web e muito mais. É a base sobre a qual Spring Boot, Spring Data, Spring Security e os demais projetos são construídos. Lançado em 2003 como alternativa leve ao peso do EJB da época.

Veja também: [[03-Dominios/Java/Spring Core e Boot/01 - O que é Spring — Framework, Boot e o ecossistema|O que é Spring]].

### Spring HATEOAS
Biblioteca do ecossistema Spring que facilita construir representações hipermídia (nível 3 do Richardson Maturity Model): fornece `EntityModel`/`CollectionModel` para envolver recursos com links, `Link` para representá-los e `WebMvcLinkBuilder` para gerar URLs de forma type-safe a partir dos controllers.

Veja também: [[03-Dominios/Java/Web e APIs REST/14 - HATEOAS|HATEOAS]].

### Spring Kafka
Módulo do Spring para integração com Apache Kafka: fornece `KafkaTemplate` para produção, `@KafkaListener` e listener containers para consumo, suporte a transações via `KafkaTransactionManager`, `DefaultErrorHandler` para tratamento de erros e `@RetryableTopic` para retry automático. É a camada de abstração principal para Kafka no ecossistema Spring.

Veja também: [[03-Dominios/Java/Mensageria/07 KafkaTemplate — produzindo mensagens|KafkaTemplate — produzindo mensagens]].

### Spring MVC
O framework web do Spring baseado no padrão front controller: um `DispatcherServlet` recebe as requisições e orquestra `HandlerMapping`, `HandlerAdapter`, interceptors e `HttpMessageConverter` para produzir a resposta. Roda sobre a Servlet API e é a base para construir aplicações web e APIs REST com `@Controller`/`@RestController`.

Veja também: [[03-Dominios/Java/Web e APIs REST/01 - O que é Spring MVC — a camada web sobre o container|O que é Spring MVC]].

### Spring Security
Framework de segurança do ecossistema Spring: autenticação, autorização e proteção contra ataques comuns, construído sobre um filter chain na frente do `DispatcherServlet`.

Veja também: [[03-Dominios/Java/Segurança/01 - O que é Spring Security — authn, authz e o filter chain|O que é Spring Security]].

### Spring WebFlux
O stack web não-bloqueante do Spring, construído sobre o Project Reactor e tipicamente servido por Netty. É a alternativa reativa ao Spring MVC: usa o `DispatcherHandler` em vez do `DispatcherServlet`, handlers que devolvem `Mono`/`Flux`, e roda sobre um event loop em vez de thread-por-request.

Veja também: [[03-Dominios/Java/Programação Reativa/10 - Spring WebFlux — o stack não-bloqueante sobre Netty e o DispatcherHandler|Spring WebFlux]].

### SpringApplication
Classe que faz o bootstrap de uma aplicação Spring Boot (`SpringApplication.run(App.class, args)`): cria o `ApplicationContext` apropriado, aplica auto-configuration, sobe o servidor embarcado, dispara listeners e banners. Customizável via `SpringApplicationBuilder` ou propriedades. Alfabetiza como "SpringApplication".

Veja também: [[03-Dominios/Java/Spring Core e Boot/16 - SpringApplication e o embedded server|SpringApplication e o embedded server]].

### springdoc-openapi
Biblioteca que integra OpenAPI ao Spring Boot: inspeciona os controllers em runtime e gera automaticamente o documento OpenAPI da API, além de servir a interface Swagger UI. Adicionada via starter (`springdoc-openapi-starter-webmvc-ui`), expõe a spec em `/v3/api-docs` e a UI em `/swagger-ui.html`.

Veja também: [[03-Dominios/Java/Web e APIs REST/12 - Documentando a API com OpenAPI e Swagger|Documentando a API com OpenAPI e Swagger]].

### stack frame
Estrutura de dados criada na pilha de cada thread para cada invocação de método ativa, armazenando variáveis locais, operandos, referência ao pool de constantes e o endereço de retorno. O conjunto de stack frames de uma thread forma a call stack. O estouro da pilha causa `StackOverflowError`.

Veja também: [[02 - Áreas de memória de runtime]].

### Stage / Scene
As duas classes de container de mais alto nível do JavaFX. `Stage` representa uma janela do SO (a janela primária é passada ao método `start(Stage)`); cada Stage pode exibir uma `Scene`. `Scene` é o container do grafo de cena, define largura/altura e a folha de estilos aplicada aos nós filhos. Um Stage pode trocar de Scene em runtime.

Veja também: [[02 - Scene graph — stage, scene e nodes]].

### starter (Spring Boot)
Dependência "guarda-chuva" do Spring Boot (ex.: `spring-boot-starter-web`) que agrega um conjunto coeso de bibliotecas para uma capacidade, com versões já harmonizadas pelo BOM do Boot. Adicionar um starter ao build traz, de uma vez, tudo o que aquela funcionalidade precisa — e ativa as auto-configurations correspondentes.

Veja também: [[03-Dominios/Java/Spring Core e Boot/15 - Auto-configuration e starters|Auto-configuration e starters]].

### Starvation
Situação em que uma thread nunca obtém acesso a um recurso porque outras threads de maior prioridade ou mais agressivas o monopolizam indefinidamente. A thread não está bloqueada em deadlock — continua elegível para execução — mas jamais é escalonada. Mitigada com políticas de lock fair (ex: `new ReentrantLock(true)`).

Veja também: [[04 - As armadilhas - race, deadlock e companhia]].

### StepVerifier
Utilitário do `reactor-test` pra testar `Mono`/`Flux`: assina o publisher e verifica os sinais passo a passo (`expectNext`/`expectError`/`verifyComplete`), com `withVirtualTime` pra delays.

Veja também: [[03-Dominios/Java/Testes/15 - Testando código reativo — StepVerifier e @WebFluxTest|Testando código reativo]].

### stop-the-world
Pausa em que a JVM suspende todas as threads da aplicação para executar uma fase do GC que exige visão consistente do heap, como a marcação inicial ou a cópia de objetos young. A duração das pausas STW é o principal indicador de latência do GC e varia conforme o coletor: G1 as minimiza incrementalmente; ZGC e Shenandoah as tornam sub-milissegundos.

Veja também: [[03 - Garbage Collection — o conceito]].

### strangler fig
Padrão de migração incremental (Martin Fowler): em vez de reescrever um monólito de uma vez, novas funcionalidades e fatias migradas são interceptadas por uma fachada e roteadas para serviços novos, enquanto o monólito é "estrangulado" aos poucos até ser desligado. Reduz o risco do big-bang.

Veja também: [[03-Dominios/Java/Microservices e sistemas distribuídos/23 - Quando NÃO fazer microservices|Quando NÃO fazer microservices]].

### Stream
Sequência de elementos que suporta operações de agregação em pipeline, introduzida no Java 8 (`java.util.stream.Stream<T>`). Não armazena dados — processa elementos sob demanda a partir de uma fonte (coleção, array, I/O). Operações intermediárias são lazy; apenas uma operação terminal dispara a execução. Uma stream não pode ser reutilizada após consumida.

Veja também: [[03-Dominios/Java/Collections e Streams/05 - Introdução à Stream API|Stream API]].

### stream lazy (avaliação preguiçosa)
Característica das operações intermediárias de uma `Stream`: elas não processam elementos imediatamente ao serem declaradas, mas apenas quando uma operação terminal é chamada. Isso permite otimizações como *short-circuit* (ex.: `findFirst` interrompe o pipeline ao encontrar o primeiro resultado) e fusão de operações (loop fusion).

Veja também: [[03-Dominios/Java/Collections e Streams/05 - Introdução à Stream API|Stream API]].

### stream primitivo (IntStream)
Especializações de `Stream` para tipos primitivos (`IntStream`, `LongStream`, `DoubleStream`) que evitam boxing/unboxing. Oferecem operações adicionais como `sum`, `average`, `min`, `max` e `summaryStatistics`. Obtidos via `mapToInt`, `mapToLong`, `mapToDouble` ou diretamente de `IntStream.range`, `Arrays.stream(int[])`.

Veja também: [[03-Dominios/Java/Collections e Streams/09 - Streams primitivos|Streams primitivos]].

### String pool
Área de memória (no heap, a partir do Java 7) onde a JVM armazena strings literais de forma deduplicada. Dois literais idênticos referenciam o mesmo objeto, economizando memória. Strings criadas com `new String(...)` não entram no pool automaticamente; `intern()` força a entrada.

Veja também: [[04 - Strings e text blocks]].

### Structured concurrency
API de concorrência estruturada em preview no Java 25 (exige `--enable-preview`), que trata um conjunto de tarefas concorrentes como uma unidade coesa com ciclo de vida delimitado por um `StructuredTaskScope`. Garante que subtarefas são concluídas (ou canceladas) antes que o escopo seja fechado, simplificando o tratamento de erros e cancelamento.

Veja também: [[13 - Structured concurrency]].

### structured logging (log estruturado)
Logar em formato estruturado e legível por máquina (tipicamente JSON) no `stdout`, com campos nomeados em vez de texto livre. Carregar o `traceId` em cada linha permite correlacionar os logs de uma requisição com seu trace e filtrar/agregar os eventos numa plataforma central.

Veja também: [[03-Dominios/Java/Cloud-native e produção/17 - Logs estruturados em produção|Logs estruturados em produção]].

### Swagger UI
Interface web interativa que renderiza um documento OpenAPI como documentação navegável e executável: lista endpoints, schemas e exemplos, e permite disparar requisições de teste direto do navegador. No Spring Boot é servida automaticamente pelo springdoc-openapi.

Veja também: [[03-Dominios/Java/Web e APIs REST/12 - Documentando a API com OpenAPI e Swagger|Documentando a API com OpenAPI e Swagger]].

### SwingWorker
Classe utilitária para executar trabalho demorado em uma background thread (`doInBackground`) e devolver resultados e progresso à EDT (`process`/`done`), sem congelar a interface. Cada instância é de uso único — não pode ser reiniciada.

Veja também: [[03-Dominios/Java/Swing/06 - SwingWorker e tarefas em background|SwingWorker]].

### Switch expression
Forma moderna do `switch` (Java 14+) que é uma expressão — produz um valor — e usa a sintaxe de seta (`case X -> valor`). Elimina fall-through acidental, exige exaustividade e pode ser atribuído diretamente a uma variável.

Veja também: [[03 - Estruturas de controle e fluxo]].

### Synchronized
Modificador Java que garante exclusão mútua e visibilidade de memória. Pode ser aplicado a métodos (bloqueia no objeto `this` ou na classe) ou a blocos (`synchronized(lock) { }`) que bloqueiam em um objeto arbitrário. A thread adquire o monitor ao entrar e o libera ao sair, mesmo em caso de exceção.

Veja também: [[03 - Exclusão mútua com synchronized]].

## T

### TableModel / ListModel
Interfaces de model para `JTable` (`TableModel`) e `JList` (`ListModel`): guardam os dados que o componente apenas exibe. `AbstractTableModel` e `AbstractListModel` facilitam implementações customizadas, exigindo apenas os métodos essenciais.

Veja também: [[03-Dominios/Java/Swing/07 - MVC em Swing e os models|MVC em Swing]].

### tail sampling
Estratégia de amostragem de traces em que a decisão é tomada depois de o trace estar completo, no OpenTelemetry Collector, que enxerga o trace inteiro. Permite reter justamente os outliers (traces com erro ou alta latência), ao custo de buffer e processamento — mais caro que o head sampling.

Veja também: [[03-Dominios/Java/Cloud-native e produção/16 - OpenTelemetry Collector e sampling de produção|OpenTelemetry Collector e sampling de produção]].

### Task / Service (JavaFX)
Classes do JavaFX para executar trabalho demorado fora da JavaFX Application Thread. `Task<V>` é de uso único (como `FutureTask`): define `call()`, expõe propriedades `value`, `progress` e `message` observáveis na JAT. `Service<V>` encapsula e reutiliza um `Task`, podendo ser reiniciado (`restart()`); adequado para operações repetíveis como buscas ou polling.

Veja também: [[10 - A JavaFX Application Thread — Task, Service e Platform.runLater]].

### Temurin (Adoptium)
Distribuição do OpenJDK vendor-neutral mantida pela Eclipse Foundation (projeto Adoptium), sob licença GPLv2+CPE. É a escolha gratuita e neutra mais comum quando não há requisito de um vendor específico.

Veja também: [[03-Dominios/Java/Build e tooling/09 - Distribuições do JDK e o ecossistema|Distribuições do JDK]].

### test data builder
Padrão que constrói objetos de teste com defaults sensatos + overrides fluentes (`anOrder().asPaid().build()`), evitando construtores enormes e setup duplicado.

Veja também: [[03-Dominios/Java/Testes/05 - Test data builders e fixtures|Test data builders e fixtures]].

### test pyramid (pirâmide de testes)
Heurística de distribuição: muitos testes de unidade (rápidos), uma camada de integração e poucos E2E (lentos/frágeis). Inverter a pirâmide deixa a suíte lenta.

Veja também: [[03-Dominios/Java/Testes/01 - O que é testar em Java — a pirâmide e o stack moderno|O que é testar em Java]].

### test slice (Spring Boot)
Anotação que carrega só parte do contexto pra testar uma camada isolada (`@WebMvcTest`/`@DataJpaTest`/`@JsonTest`/`@RestClientTest`), mais rápida que `@SpringBootTest`.

Veja também: [[03-Dominios/Java/Testes/08 - Spring Boot Test e os slices — o contexto de teste|Spring Boot Test e os slices]].

### Testcontainers
Biblioteca que sobe containers Docker reais (Postgres, Kafka, Redis) durante o teste, eliminando o falso-positivo do H2; `@ServiceConnection` (Boot 3.1+) auto-configura a conexão.

Veja também: [[03-Dominios/Java/Testes/11 - Testcontainers — infra real em testes|Testcontainers]].

### TestEntityManager
Alternativa de teste ao `EntityManager` no `@DataJpaTest` (`persist`/`flush`/`find`), pra preparar o estado do banco sem passar pelo repositório sob teste.

Veja também: [[03-Dominios/Java/Testes/10 - @DataJpaTest — testando repositories|@DataJpaTest]].

### Text block
Literal de string multilinha delimitado por `"""` (Java 15+). Preserva a indentação relativa, suporta interpolação futura e elimina concatenações e escapes desnecessários em strings longas como SQL, JSON ou HTML embutido.

Veja também: [[04 - Strings e text blocks]].

### thin jar
Jar que contém apenas as classes da aplicação, mantendo as dependências externas (no classpath ou em um diretório `lib/`). Mais leve que o fat jar e melhor para camadas de cache de imagem Docker, ao custo de exigir o classpath montado na execução.

Veja também: [[03-Dominios/Java/Build e tooling/15 - Empacotamento — fat jar, thin jar e repackage|Empacotamento — fat jar e thin jar]].

### Thread pool
Conjunto de threads pré-criadas e reutilizáveis que executam tarefas submetidas a uma fila, evitando o custo de criar e destruir threads para cada tarefa. Em Java, provido por `ExecutorService` com implementações como `ThreadPoolExecutor`, `FixedThreadPool` e `ForkJoinPool`. Fundamental para escalabilidade de aplicações concorrentes.

Veja também: [[08 - Executors e thread pools]].

### tiered compilation
Estratégia de compilação JIT padrão desde o Java 8 que combina C1 e C2 em cinco níveis (0=interpretado, 1–3=C1 com crescente profundidade de instrumentação, 4=C2 totalmente otimizado). Métodos sobem de nível conforme a frequência de invocação, balanceando tempo de warmup e pico de throughput.

Veja também: [[07 - JIT — C1, C2 e tiered compilation]].

### time limiter
Padrão de resiliência que impõe um timeout a chamadas assíncronas (`Future`/`CompletableFuture`), cancelando a operação e liberando recursos se ela exceder o tempo limite. No Java, oferecido pelo Resilience4j (`TimeLimiter`).

Veja também: [[03-Dominios/Java/Microservices e sistemas distribuídos/14 - Resiliência II — Retry e Time Limiter|Resiliência II — Retry e Time Limiter]].

### token relay
Padrão em que um serviço (tipicamente o gateway) repassa o token de acesso do usuário para os serviços downstream, propagando a identidade e as permissões ao longo da cadeia de chamadas em vez de reautenticar.

Veja também: [[03-Dominios/Java/Microservices e sistemas distribuídos/17 - Segurança entre serviços|Segurança entre serviços]].

### toolchain (build)
Mecanismo do Maven e do Gradle que desacopla o JDK que roda o build do JDK usado para compilar e mirar o código. Permite, por exemplo, rodar o build com Java 21 e produzir bytecode compatível com Java 17, sem depender do JDK do `PATH`.

Veja também: [[03-Dominios/Java/Build e tooling/13 - Toolchains — buildar com um JDK, mirar outro|Toolchains]].

### traceId / spanId
Identificadores do tracing distribuído: o **traceId** identifica uma requisição inteira ao atravessar vários serviços; cada unidade de trabalho dentro dela recebe um **spanId** próprio, formando uma árvore. Propagados via headers (ex.: W3C `traceparent`) para reconstituir o caminho ponta a ponta.

Veja também: [[03-Dominios/Java/Microservices e sistemas distribuídos/18 - Tracing distribuído I — correlação no código|Tracing distribuído I — correlação no código]].

### @Transactional (Jakarta)
Annotation da JTA (`jakarta.transaction.Transactional`) que demarca transações de forma declarativa via interceptor CDI. O atributo `TxType` (REQUIRED/REQUIRES_NEW/...) define a propagação; por padrão faz rollback em exceções unchecked, não em checked. Homônima — mas distinta — da annotation de mesmo nome em frameworks. Alfabetiza como "Transactional".

Veja também: [[03-Dominios/Java/Jakarta EE/11 - JTA — transações na plataforma|JTA — transações na plataforma]]; ver também o homônimo do Spring em [[#@Transactional (Spring)]].

### @Transactional (propagação)
O comportamento transacional do `@Transactional` do Spring: propagação (REQUIRED, REQUIRES_NEW, NESTED...), isolamento, rollback rules (só `RuntimeException`/`Error` por default — checked não reverte) e `readOnly`. O mecanismo (proxy AOP) é o do verbete `@Transactional (Spring)`. Veja também: [[03-Dominios/Java/Persistência de dados/12 - Transações operacionais — @Transactional propagação, isolamento, rollback, readOnly|Transações operacionais]].

### @Transactional (Spring)
Annotation do Spring (`org.springframework.transaction.annotation.Transactional`) que demarca transações de forma declarativa via proxy AOP. O atributo `propagation` (REQUIRED/REQUIRES_NEW/...) controla a propagação e `isolation` o nível; por padrão faz rollback só em exceções unchecked (`rollbackFor` ajusta isso). Sofre da armadilha de self-invocation. Distinta — mas homônima — da annotation da JTA. Alfabetiza como "Transactional".

Veja também: [[03-Dominios/Java/Spring Core e Boot/09 - AOP e proxies no Spring|AOP e proxies no Spring]]; ver também o homônimo da plataforma em [[#@Transactional (Jakarta)]].

### treeification
Otimização interna do `HashMap` (e `LinkedHashMap`) introduzida no Java 8: quando um bucket acumula muitas entradas por colisões de `hashCode` (padrão: ≥ 8), a lista encadeada do bucket é convertida em uma árvore vermelho-preta, reduzindo o pior caso de buscas de O(n) para O(log n). O bucket é convertido de volta para lista se encolher abaixo do limiar.

Veja também: [[03-Dominios/Java/Collections e Streams/03 - Mapas|Mapas]].

### Try-with-resources
Construção `try (Recurso r = ...)` que garante o fechamento automático de qualquer objeto `AutoCloseable` ao fim do bloco, mesmo em caso de exceção. Elimina o padrão `finally { r.close(); }` e torna o gerenciamento de recursos mais seguro e legível.

Veja também: [[10 - Exceções e tratamento de erros]].

### twelve-factor (12-factor)
Metodologia (Heroku) de doze práticas para construir aplicações cloud-native — config no ambiente, processos stateless, build/release/run separados, paridade dev/prod, logs como streams etc. Serve de checklist para serviços bem-comportados em containers e orquestradores.

Veja também: [[03-Dominios/Java/Microservices e sistemas distribuídos/03 - Os 12 fatores e o serviço cloud-native|Os 12 fatores e o serviço cloud-native]].

### two-phase commit (2PC / XA)
Protocolo que garante atomicidade de uma transação que abrange múltiplos recursos (ex.: banco + fila): uma fase de prepare seguida de uma de commit, coordenadas por um transaction manager via a interface X/Open XA. Robusto, mas caro em latência e bloqueio.

Veja também: [[03-Dominios/Java/Jakarta EE/11 - JTA — transações na plataforma|JTA — transações na plataforma]].

### Type erasure
Processo pelo qual o compilador Java remove as informações de tipo genérico em tempo de compilação, substituindo parâmetros de tipo por `Object` (ou pelo bound superior). Em tempo de execução, `List<String>` e `List<Integer>` são indistinguíveis, o que limita certas reflexões e casts.

Veja também: [[12 - Generics em profundidade]].

## U

### UIManager
Classe que gerencia o look and feel ativo e os defaults de UI de todos os componentes Swing. Métodos principais: `setLookAndFeel`, `getSystemLookAndFeelClassName`, `getLookAndFeelDefaults`. Permite sobrescrever cores, fontes e bordas via `UIManager.put(chave, valor)`.

Veja também: [[03-Dominios/Java/Swing/09 - Look and Feel e temas|Look and Feel]].

### Unchecked exception
Exceção que não precisa ser declarada nem capturada obrigatoriamente. Estende `RuntimeException` ou `Error`. Exemplos: `NullPointerException`, `IllegalArgumentException`. Geralmente indica bugs ou estados inesperados que o chamador não tem como recuperar programaticamente.

Veja também: [[10 - Exceções e tratamento de erros]].

### unified logging (-Xlog)
Framework de logging unificado da JVM introduzido no Java 9 (JEP 158) que unifica todos os logs internos (GC, JIT, classloading, safepoints…) em uma única infraestrutura configurável via `-Xlog:<tags>:<output>:<decorators>`. Substitui flags fragmentadas como `-XX:+PrintGCDetails`. Permite filtrar por subsistema, nível e redirecionar para arquivo com rotação.

Veja também: [[10 - GC logs — unified logging e leitura]].

### UseContainerSupport
Flag da JVM, ligada por padrão desde o Java 10, que faz a VM detectar que roda dentro de um container e ler os limites do cgroup em vez dos recursos do host. É o interruptor por trás da container-awareness; desligá-la faz a JVM voltar a enxergar a máquina inteira.

Veja também: [[03-Dominios/Java/Cloud-native e produção/02 - A JVM dentro de um container|A JVM dentro de um container]].

### UserDetailsService
Interface cujo `loadUserByUsername` carrega o usuário (e suas authorities) de onde estiver (banco, LDAP); auto-detectada como bean e usada pelo `DaoAuthenticationProvider`.

Veja também: [[03-Dominios/Java/Segurança/03 - Autenticação — UserDetailsService, AuthenticationManager, Form e Basic|Autenticação]].

### usingRecursiveComparison
Recurso do AssertJ que compara dois objetos campo a campo recursivamente (`.ignoringFields("id", "createdAt")`), sem depender de `equals`.

Veja também: [[03-Dominios/Java/Testes/03 - AssertJ — fluent assertions|AssertJ]].

## V

### @Value
Annotation do Spring que injeta um valor — literal, propriedade externa (`@Value("${app.timeout}")`) ou expressão SpEL (`@Value("#{...}")`) — em um campo, parâmetro ou método. É a forma pontual de ler configuração; para grupos de propriedades relacionadas, prefira `@ConfigurationProperties`. Alfabetiza como "Value".

Veja também: [[03-Dominios/Java/Spring Core e Boot/12 - Configuração e profiles|Configuração e profiles]].

### Varargs
Mecanismo que permite declarar um método com número variável de argumentos do mesmo tipo (`Tipo... nomes`). O compilador converte os argumentos em um array. Deve ser o último parâmetro da assinatura e gera um aviso se usado junto com generics por ambiguidade de heap pollution.

Veja também: [[05 - Arrays e varargs]].

### verify (Mockito)
Confere que um mock foi chamado como esperado (`verify(mock, times(n))`, `never()`, `InOrder`); verifique o comportamento observável, não a contagem acoplada à implementação.

Veja também: [[03-Dominios/Java/Testes/07 - Mockito — verify, ArgumentCaptor e quando NÃO mockar|Mockito: verify e ArgumentCaptor]].

### Version Catalog
Mecanismo do Gradle (`gradle/libs.versions.toml`) que centraliza, de forma type-safe, as versões e coordenadas das dependências num único arquivo TOML. Os módulos referenciam as libs pelo alias (`libs.spring.boot`), evitando versões duplicadas e divergentes.

Veja também: [[03-Dominios/Java/Build e tooling/06 - Gradle — dependências, Version Catalogs e o wrapper|Gradle — dependências e Version Catalogs]].

### @Version (optimistic locking)
Campo de versão numa entidade que habilita o optimistic locking: o Hibernate adiciona `WHERE version = ?` no UPDATE e incrementa a versão; se 0 linhas forem afetadas, lança `OptimisticLockException`. Veja também: [[03-Dominios/Java/Persistência de dados/13 - Locking — optimistic (@Version) e pessimistic|Locking]].

### Virtual thread
Thread leve gerenciada pela JVM (não mapeada 1:1 com OS threads), GA no Java 21 (JEP 444). Permite criar milhões de threads com baixo overhead de memória, tornando o modelo thread-per-request viável em servidores de alta concorrência. Criadas via `Thread.ofVirtual()` ou `Executors.newVirtualThreadPerTaskExecutor()`.

Veja também: [[12 - Virtual Threads e Project Loom]].

### Volatile
Modificador de campo que garante visibilidade imediata de escritas a todas as threads e proíbe reordenação de instruções ao redor da variável. Garante visibilidade e ordering, mas NÃO garante atomicidade composta: `volatile int i; i++` ainda é uma race condition pois envolve leitura-modificação-escrita não-atômica.

Veja também: [[11 - Java Memory Model em profundidade]].

## W

### weak generational hypothesis
Hipótese empírica que embasa os coletores generacionais: a maioria dos objetos morre jovem. Com base nisso, o heap é dividido em geração jovem (young/eden + survivor) e geração velha (old/tenured), e a coleta foca na geração jovem — onde o retorno de objetos coletados por unidade de trabalho é máximo — reduzindo o custo total do GC.

Veja também: [[03 - Garbage Collection — o conceito]].

### Web Profile
Perfil intermediário do Jakarta EE: inclui as specs típicas de aplicações web (Servlet, CDI, JAX-RS, JPA, JTA, Bean Validation...) sem o conjunto completo da Platform. Maior que o Core Profile, menor que a Platform.

Veja também: [[03-Dominios/Java/Jakarta EE/01 - O modelo Jakarta EE — especificações e implementações|O modelo Jakarta EE]].

### WebClient
Cliente HTTP reativo e não-bloqueante do Spring WebFlux, com API fluente (`get().uri(...).retrieve().bodyToMono(...)`). Suporta streaming e composição reativa via Project Reactor (`Mono`/`Flux`); é a escolha para cenários assíncronos/reativos ou alta concorrência, complementando o `RestClient` síncrono. Sob o capô, libera a thread chamadora enquanto a resposta não chega, integrando-se ao event loop do Netty — por isso uma única conexão pode multiplexar muitas requests sem inflar o pool de threads. Alfabetiza como "WebClient".

Veja também: [[03-Dominios/Java/Web e APIs REST/15 - Clientes HTTP — RestClient, WebClient, RestTemplate|Clientes HTTP — RestClient, WebClient, RestTemplate]], [[03-Dominios/Java/Programação Reativa/11 - WebClient — o cliente HTTP reativo a fundo|WebClient a fundo]].

### @WebFluxTest
Slice de teste do Spring Boot pra reactive controllers (WebFlux); auto-configura o `WebTestClient`.

Veja também: [[03-Dominios/Java/Testes/15 - Testando código reativo — StepVerifier e @WebFluxTest|Testando código reativo]].

### @WebMvcTest
Slice de teste do Spring Boot que carrega só a web layer (controllers, `@ControllerAdvice`, converters) e mocka o resto; testado com `MockMvc`.

Veja também: [[03-Dominios/Java/Testes/09 - @WebMvcTest — testando controllers com MockMvc|@WebMvcTest]].

### WebTestClient
Cliente de teste reativo do Spring (não-bloqueante) pra exercitar endpoints WebFlux ou servidores reais; usado em `@WebFluxTest` e `@SpringBootTest`.

Veja também: [[03-Dominios/Java/Testes/15 - Testando código reativo — StepVerifier e @WebFluxTest|Testando código reativo]].

### Wildcard
Argumento de tipo genérico desconhecido, representado por `?`. Pode ser não-limitado (`?`), com limite superior (`? extends T`) ou com limite inferior (`? super T`). Aumenta a flexibilidade das APIs genéricas ao custo de restringir as operações permitidas sobre a coleção.

Veja também: [[12 - Generics em profundidade]].

### WireMock
Servidor de mock HTTP pra testar integrações com APIs externas sem depender delas (`stubFor`/`verify`, cenários de retry); aponta-se o client via `@DynamicPropertySource`.

Veja também: [[03-Dominios/Java/Testes/16 - Mockando HTTP externo — WireMock e MockRestServiceServer|Mockando HTTP externo]].

### @WithMockUser
Anotação de teste do Spring Security que injeta um usuário autenticado no `SecurityContext` para testar regras de autorização; a stack de teste é tema do galho de Testes.

Veja também: [[03-Dominios/Java/Segurança/18 - Capstone — projetando a segurança de uma API Spring production-grade|Capstone de segurança]]. [[03-Dominios/Java/Testes/13 - Testando a segurança|Testando a segurança]].

### WORA
Write Once, Run Anywhere — princípio central do Java: o bytecode compilado roda em qualquer plataforma que possua uma JVM compatível, sem recompilação. Viabilizado pela camada de abstração da JVM entre o código e o hardware/SO.

Veja também: [[01 - O modelo da linguagem Java]].

### Work-stealing
Estratégia de escalonamento do `ForkJoinPool` onde threads ociosas "roubam" tarefas da fila de outras threads sobrecarregadas. Reduz ociosidade e melhora o balanceamento dinâmico de carga em workloads irregulares. Cada worker mantém uma deque (fila dupla) de tarefas; o roubo ocorre pela extremidade oposta.

Veja também: [[15 - Parallel streams e fork-join]].

### wrapper (mvnw/gradlew)
Script versionado no próprio projeto (`mvnw`/`mvnw.cmd`, `gradlew`/`gradlew.bat`) que baixa e usa uma versão fixa do build tool, garantindo builds reprodutíveis sem depender da instalação local. O Gradle Wrapper vem por padrão (`gradle wrapper`); o Maven Wrapper precisa ser adicionado explicitamente.

Veja também: [[03-Dominios/Java/Build e tooling/04 - Maven — plugins, profiles e o wrapper|Maven — wrapper]], [[03-Dominios/Java/Build e tooling/06 - Gradle — dependências, Version Catalogs e o wrapper|Gradle — wrapper]].

## Y

### Yield
Palavra-chave usada dentro de um bloco de switch expression (`case X -> { ... yield valor; }`) para retornar o valor produzido pelo bloco. Necessário quando o braço do switch contém mais de uma instrução; na sintaxe de seta simples, o valor é retornado diretamente sem `yield`.

Veja também: [[03 - Estruturas de controle e fluxo]].

## Z

### ZGC (generational)
Coletor de lixo de latência ultra-baixa (sub-milissegundos), com arquitetura generacional adotada como padrão no Java 23 (JEP 439, final no Java 21). Realiza marcação, realocação e compactação concorrentemente com a aplicação usando load barriers e colored pointers, mantendo as pausas STW praticamente constantes independentemente do tamanho do heap. Ativado explicitamente com `-XX:+UseZGC`.

Veja também: [[06 - Os coletores do HotSpot]].

### Zuul
API Gateway legado da Netflix, integrado ao Spring Cloud Netflix. Foi descontinuado e removido — o Spring Cloud Gateway é seu substituto recomendado, com modelo reativo e melhor desempenho.

Veja também: [[03-Dominios/Java/Microservices e sistemas distribuídos/04 - Panorama do Spring Cloud — e o que morreu|Panorama do Spring Cloud — e o que morreu]].
