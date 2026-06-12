---
title: "Java"
type: moc
publish: true
created: 2026-05-21
updated: 2026-06-12
status: growing
tags:
  - moc
  - java
aliases:
  - Estante Java
---
# Java

> [!abstract] TL;DR
> Trilha Java Senior organizada em **18 galhos** progressivos, de fundamentos da linguagem até produção cloud-native — passando por JVM, concorrência, desktop (Swing/JavaFX), Jakarta EE, Spring, persistência, segurança, testes, mensageria, microservices e certificação OCP. Cada galho é um conjunto de notas atômicas em 3 fases de aprendizado (Iniciado/Adepto/Magus), com seção "Em entrevista" em inglês. A trilha cresce um galho por vez; só os galhos publicados têm link ativo abaixo.

A estante de Java cobre tudo o que um desenvolvedor senior precisa dominar no ecossistema — linguagem e JVM, frameworks de backend (Jakarta EE, Spring), interfaces desktop, plataforma distribuída e produção. O material está sendo refatorado dos troncos monolíticos originais (`Java Fundamentals`, `Java Concurrency`, `Spring Boot`, `Spring Data JPA`, `Spring Security`, etc.) para galhos temáticos de notas atômicas, no mesmo padrão das trilhas [[03-Dominios/Node/index|Node]] e [[03-Dominios/IA/index|IA]].

## Galhos da trilha

### Núcleo da linguagem

1. [[03-Dominios/Java/Linguagem e sintaxe moderna/index|Linguagem e sintaxe moderna]] — tipos, OOP, exceções, generics, records, sealed classes, pattern matching, evolução Java 8→25
2. [[03-Dominios/Java/Collections e Streams/index|Collections, Streams e Programação Funcional]] — Collections Framework, Stream API, lambdas e interfaces funcionais, Optional, Date/Time (java.time), I/O moderno (java.nio.file)
3. [[03-Dominios/Java/JVM/index|JVM por dentro]] — memória de runtime, GC (G1/ZGC/Shenandoah), JIT e tiered compilation, classloading, bytecode, módulos (JPMS), diagnóstico (JFR/jcmd) e tuning
4. [[03-Dominios/Java/Concorrência e paralelismo/index|Concorrência e paralelismo]] — Memory Model, locks, atomics, executors, CompletableFuture, Virtual Threads/Loom, structured concurrency

### Interfaces desktop

5. [[03-Dominios/Java/Swing/index|Swing]] — componentes e containers, layout managers, modelo de eventos, EDT/SwingWorker, MVC/models, Look & Feel, custom painting, estado atual da API
6. [[03-Dominios/Java/JavaFX/index|JavaFX]] — scene graph, FXML/Scene Builder, properties e binding, CSS, Task/Service e threading, MVVM, jlink/jpackage, estado do projeto (OpenJFX/Gluon)

### Fundamentos enterprise e Spring

7. [[03-Dominios/Java/Jakarta EE/index|Jakarta EE]] — spec vs implementação, transição javax→jakarta, Servlet, CDI, JAX-RS, Bean Validation, JPA spec, JTA, legado EJB, estado atual da plataforma
8. [[03-Dominios/Java/Spring Core e Boot/index|Spring Core e Boot]] — IoC/DI, beans e escopos, AOP/proxies, configuração e profiles, conditional/auto-configuration, eventos do contexto, fundamentos do Boot, Actuator
9. [[03-Dominios/Java/Web e APIs REST/index|Web e APIs REST]] — Spring MVC e o pipeline do DispatcherServlet, REST controllers, content negotiation, validação na borda, exception handling (@ControllerAdvice, Problem Details), OpenAPI, HATEOAS, versionamento, clientes HTTP
10. [[03-Dominios/Java/Persistência de dados/index|Persistência de dados]] — JPA/Hibernate, o persistence context, mapeamento e relacionamentos, fetch strategies e o N+1, Spring Data repositories e consultas, paginação, transações operacionais, locking, caching e migrations
11. [[03-Dominios/Java/Programação Reativa/index|Programação Reativa]] — o modelo reativo na JVM: Reactive Streams, Project Reactor (Mono/Flux e operadores), schedulers e backpressure, Spring WebFlux e WebClient, R2DBC, e o confronto honesto reativo vs Virtual Threads
12. [[03-Dominios/Java/Segurança/index|Segurança]] — Spring Security e o filter chain, autenticação e password encoding, autorização URL-based e method-level, JWT, OAuth2/OIDC, CSRF/CORS, session management, security headers e OWASP no contexto Java
13. [[03-Dominios/Java/Testes/index|Testes]] — a pirâmide e o stack moderno, JUnit 5/AssertJ/Mockito, os slices do Spring Boot, Testcontainers e integração, testes de segurança/async/reativo, mutation testing, performance, fitness functions e contract testing

### Plataforma distribuída e produção

14. [[03-Dominios/Java/Mensageria/index|Mensageria e eventos]] — o modelo de mensageria e as garantias de entrega, Spring Kafka e RabbitMQ, eventos in-process, padrões de confiabilidade (idempotência, outbox, DLQ, exactly-once), arquitetura event-driven (saga, event sourcing, CQRS), mensageria reativa, observabilidade e o contraste com gRPC
15. [[03-Dominios/Java/Build e tooling/index|Build, tooling e ecossistema]] — Maven e Gradle (modelo, lifecycle/tasks, performance), gestão de dependências (resolução transitiva, conflitos, BOM), multi-módulo, distribuições do JDK e licenciamento, annotation processing (Lombok/MapStruct), empacotamento, quality gates no build e cadeia de suprimentos (reproducible builds, SBOM, Maven Central)
16. [[03-Dominios/Java/Microservices e sistemas distribuídos/index|Microservices e sistemas distribuídos]] — o modelo e a tese honesta (microservices vs monólito modular), Spring Cloud (service discovery, gateway, config centralizado), resiliência com Resilience4j (circuit breaker, retry, bulkhead, rate limiter, time limiter), comunicação síncrona (OpenFeign/@HttpExchange), segurança entre serviços, tracing distribuído (Micrometer Tracing/OpenTelemetry), consistência (CAP/PACELC) e service mesh
17. [[03-Dominios/Java/Cloud-native e produção/index|Cloud-native e produção]] — levar o jar a produção num cluster: empacotamento em imagem (Dockerfile multi-stage/layered jar, distroless, Buildpacks, Jib), a JVM ciente do container (cgroup, MaxRAMPercentage), GraalVM Native Image e Spring AOT, o contrato com o Kubernetes (probes, config, graceful shutdown), observabilidade de operação (Micrometer/Prometheus/Grafana, OpenTelemetry Collector e sampling, logs estruturados), profiling sob carga e continuous profiling, CI/CD e a decisão native vs JVM

### Certificação

18. Certificação Java OCP *(planejado)* — guia da prova OCP Java SE 21, mapeado aos galhos de linguagem

## Referência

- [[03-Dominios/Java/Dicionário de Java|Dicionário de Java]] — glossário de termos da trilha
- [[Java Fundamentals]] — tronco original da linguagem (em transição; sendo podado conforme galhos fecham)
- [[03-Dominios/Java/Core/Helsinki MOOC - Guia de Revisão|Helsinki MOOC]] — guia de revisão para iniciantes
- [[03-Dominios/Java/Core/Certificação Java OCP|Certificação OCP]] — guia da prova (vira Galho 18)

## Veja também

- [[03-Dominios/JavaScript/index|JavaScript]]
