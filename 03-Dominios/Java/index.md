---
title: "Java"
type: moc
publish: true
created: 2026-05-21
updated: 2026-06-07
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
8. Spring Core e Boot *(planejado)* — IoC/DI, AOP, auto-configuration, profiles, Actuator
9. Web e APIs REST *(planejado)* — Spring MVC, REST, exception handling, validation, OpenAPI
10. Persistência de dados *(planejado)* — JPA/Hibernate, Spring Data, fetch/N+1, transações, migrations
11. Programação Reativa *(planejado)* — Reactor, WebFlux, backpressure, R2DBC
12. Segurança *(planejado)* — Spring Security, JWT, OAuth2/OIDC, CSRF/CORS
13. Testes *(planejado)* — JUnit 5, Mockito, AssertJ, Spring Boot Test, Testcontainers

### Plataforma distribuída e produção

14. Mensageria e eventos *(planejado)* — Kafka, RabbitMQ, Spring events, event-driven, gRPC
15. Build, tooling e ecossistema *(planejado)* — Maven, Gradle, BOM, multi-module, JDK distributions
16. Microservices e sistemas distribuídos *(planejado)* — Spring Cloud, gateway, resilience, sagas, tracing
17. Cloud-native e produção *(planejado)* — containers, GraalVM native, Micrometer/OpenTelemetry, profiling

### Certificação

18. Certificação Java OCP *(planejado)* — guia da prova OCP Java SE 21, mapeado aos galhos de linguagem

## Referência

- [[03-Dominios/Java/Dicionário de Java|Dicionário de Java]] — glossário de termos da trilha
- [[Java Fundamentals]] — tronco original da linguagem (em transição; sendo podado conforme galhos fecham)
- [[03-Dominios/Java/Core/Helsinki MOOC - Guia de Revisão|Helsinki MOOC]] — guia de revisão para iniciantes
- [[03-Dominios/Java/Core/Certificação Java OCP|Certificação OCP]] — guia da prova (vira Galho 18)

## Veja também

- [[03-Dominios/JavaScript/index|JavaScript]]
