---
title: "O que é Spring — Framework, Boot e o ecossistema"
created: 2026-06-08
updated: 2026-06-08
type: concept
progress: backlog
status: seedling
publish: true
fase: iniciado
tags:
  - java
  - spring
  - iniciado
  - boot
aliases:
  - "Spring"
  - "Spring Boot"
  - "Spring Framework"
---

# O que é Spring — Framework, Boot e o ecossistema

> [!abstract] TL;DR
> Spring é um ecossistema em camadas: o **Spring Framework** fornece o núcleo (IoC/DI, AOP, gerenciamento de transações, Spring MVC/WebFlux); o **Spring Boot** adiciona auto-configuração, starters, servidor embarcado e Actuator por cima desse núcleo; e os **projetos do portfólio** (Spring Data, Security, Cloud, entre outros) estendem esse stack para casos específicos. Boot 3.x exige Java 17+ e migrou todos os namespaces de `javax.*` para `jakarta.*`, alinhando-se à plataforma Jakarta EE 9+ que o Galho 7 descreve.

## O que é

O nome "Spring" abrange três coisas distintas que costumam ser confundidas:

| Camada | O que é | Exemplo de uso |
|---|---|---|
| **Spring Framework** | Biblioteca Java de propósito geral: IoC, AOP, MVC, acesso a dados, tx | `@Component`, `@Transactional`, `DispatcherServlet` |
| **Spring Boot** | Camada de conveniência sobre o Framework: auto-config, starters, servidor embarcado | `@SpringBootApplication`, `spring-boot-starter-web` |
| **Projetos do portfólio** | Módulos independentes para problemas específicos | Spring Data, Spring Security, Spring Cloud (planejado) |

O diagrama abaixo ilustra a relação de camadas:

```text
┌─────────────────────────────────────────────────┐
│          Projetos do portfólio                  │
│  (Spring Data / Security / Cloud — planejado)   │
├─────────────────────────────────────────────────┤
│                 Spring Boot                     │
│  auto-config · starters · embedded server       │
│  Actuator · DevTools · CLI                      │
├─────────────────────────────────────────────────┤
│              Spring Framework                   │
│  IoC/DI · AOP · Tx · MVC · WebFlux · Testing   │
├─────────────────────────────────────────────────┤
│           Plataforma Jakarta EE (specs)          │
│  Servlet · JPA · CDI · Bean Validation · JTA    │
└─────────────────────────────────────────────────┘
```

**Spring Boot** é "opinionated": ele aplica convenções sensatas por padrão (convention-over-configuration). Quando `spring-boot-starter-web` está no classpath, Boot configura automaticamente um `DispatcherServlet`, um `Tomcat` embutido na porta 8080 e uma série de beans de suporte — sem nenhum XML. Quer uma configuração diferente? Você sobrescreve apenas o que precisa.

O ponto de partida recomendado para novos projetos é o **Spring Initializr** (`start.spring.io`): seleciona linguagem, versão do Boot, dependências (starters) e gera um projeto Maven ou Gradle pronto para importar na IDE.

O artefato final é um **fat JAR** autocontido: `java -jar pedido-service.jar` sobe toda a aplicação, incluindo o servidor Tomcat/Jetty/Undertow, sem precisar de um servidor de aplicação externo.

## Por que importa

Spring Boot é o framework de facto para desenvolvimento backend em Java moderno. Serviços REST, microsserviços, batch jobs e aplicações web corporativas — a esmagadora maioria dos projetos Java novos usa Boot como ponto de partida.

Em entrevistas técnicas para posições pleno/sênior, a distinção entre **Spring Framework** e **Spring Boot** é cobrada com frequência. Respostas vagas como "Spring Boot é o Spring mais fácil" demonstram lacuna conceitual; a resposta precisa é sobre *o que cada camada adiciona* e *quais problemas cada uma resolve*.

Entender o modelo de camadas também é pré-requisito para as notas seguintes: IoC e DI fazem parte do **Framework**; auto-configuração e starters são mecanismos do **Boot**; Spring Data e Security são **projetos separados** que apenas se integram ao ecossistema.

## Como funciona

### Spring Framework: o núcleo (IoC, AOP, transações, MVC)

O Spring Framework resolve o problema central de como os objetos de uma aplicação obtêm suas dependências. Em vez de cada classe instanciar seus colaboradores com `new`, o **IoC Container** (ApplicationContext) cria, conecta e gerencia o ciclo de vida dos beans.

Principais módulos:

- **Core (IoC/DI)** — ApplicationContext, BeanFactory, `@Component`, `@Autowired`
- **AOP** — interceptação declarativa de chamadas de método; base para `@Transactional` e `@Cacheable`
- **Data Access / Transactions** — abstração sobre JDBC, JPA e gerenciadores de transação; `@Transactional`
- **Spring MVC** — framework web baseado no padrão Front Controller (`DispatcherServlet`); `@RestController`, `@GetMapping`
- **Spring WebFlux** — stack reativo não-bloqueante, alternativa ao MVC para cargas de alta concorrência

O Framework **não é** um servidor de aplicação e **não substitui** as specs Jakarta: ele as *implementa* ou *delega* para elas. `@Transactional` usa JTA ou um `PlatformTransactionManager` que, por baixo, pode chamar a implementação JPA configurada.

### Spring Boot: o que ele adiciona (auto-config, starters, embedded server, Actuator)

Boot não reescreve o Framework — ele o configura automaticamente. Os mecanismos centrais são:

**Auto-configuração**: Boot inspeciona o classpath e o `application.properties` (ou `application.yml`) e cria os beans necessários sem declaração explícita. Se `spring-boot-starter-data-jpa` está presente e há um `DataSource` configurado, Boot registra automaticamente um `EntityManagerFactory`, um `TransactionManager` e os repositórios Spring Data.

**Starters**: dependências agrupadas por função. `spring-boot-starter-web` puxa Spring MVC, Tomcat embutido, Jackson e outros. O desenvolvedor declara *o que quer fazer*, não *quais jars precisa*.

**Servidor embutido**: Tomcat é o padrão; Jetty e Undertow são alternativas configuráveis. O fat JAR é autocontido e iniciável com `java -jar`.

**Actuator**: endpoints HTTP prontos para produção — `/actuator/health`, `/actuator/metrics`, `/actuator/info` — sem código adicional. Integra com Prometheus, Micrometer e sistemas de APM.

**DevTools**: reinicialização automática em desenvolvimento ao detectar mudanças no classpath.

### Os projetos do portfólio (Data, Security, Cloud)

O ecossistema Spring inclui projetos independentes que se integram ao núcleo:

- **Spring Data** (planejado) — repositórios genéricos para JPA, MongoDB, Redis, Elasticsearch e outros; abstrai queries com convenções de nome de método
- **Spring Security** (planejado) — autenticação e autorização; integra com OAuth 2, JWT, LDAP, form login
- **Spring Cloud** (planejado) — padrões para microsserviços distribuídos: discovery, circuit breaker, config centralizado, gateway

Esses projetos têm versionamento próprio e releases independentes, mas seguem o ciclo do Boot para garantir compatibilidade.

### Boot 3.x: Java 17+ e o namespace jakarta.*

Spring Boot 3.x (lançado em novembro de 2022) introduziu duas mudanças de baseline com impacto direto no código:

**Java 17 como mínimo obrigatório.** Boot 2.x suportava Java 8+. Boot 3.x requer Java 17, aproveitando records, sealed classes, text blocks e o pattern matching disponíveis desde essa versão.

**Migração de `javax.*` para `jakarta.*`.** Boot 3 é baseado em Spring Framework 6, que adota Jakarta EE 9+ como baseline. Todas as especificações Jakarta que antes usavam o namespace `javax.*` passaram a usar `jakarta.*`:

| Antes (Boot 2 / Framework 5) | Depois (Boot 3 / Framework 6+) |
|---|---|
| `javax.servlet.http.HttpServletRequest` | `jakarta.servlet.http.HttpServletRequest` |
| `javax.persistence.Entity` | `jakarta.persistence.Entity` |
| `javax.validation.constraints.NotNull` | `jakarta.validation.constraints.NotNull` |
| `javax.transaction.Transactional` | `jakarta.transaction.Transactional` |

Projetos migrando de Boot 2 para Boot 3 precisam atualizar todos os imports afetados — o IntelliJ IDEA e a ferramenta `spring-boot-migrator` automatizam grande parte desse processo.

Spring Framework 7.x (mais recente) eleva o baseline para Jakarta EE 11-12 e recomenda JDK 25 para produção, mantendo compatibilidade com JDK 17 e 21 (LTS).

## Na prática

Um projeto Spring Boot mínimo com Maven tem este `pom.xml`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.example</groupId>
    <artifactId>order-service</artifactId>
    <version>1.0.0</version>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.5.0</version>
        <relativePath/>
    </parent>

    <properties>
        <java.version>17</java.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>
</project>
```

O `spring-boot-starter-parent` gerencia versões de dependências; o `spring-boot-maven-plugin` empacota o fat JAR. A classe principal:

```java
package com.example.orderservice;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.PathVariable;

@SpringBootApplication
public class OrderServiceApplication {

    public static void main(String[] args) {
        SpringApplication.run(OrderServiceApplication.class, args);
    }
}

@RestController
class OrderController {

    @GetMapping("/orders/{id}")
    String findOrder(@PathVariable Long id) {
        return "Order #" + id;
    }
}
```

`@SpringBootApplication` é uma meta-anotação que combina `@Configuration`, `@EnableAutoConfiguration` e `@ComponentScan`. Ao chamar `SpringApplication.run(...)`, Boot inicializa o ApplicationContext, dispara a auto-configuração e sobe o Tomcat embutido.

Iniciar: `mvn spring-boot:run` ou `java -jar target/order-service-1.0.0.jar`.

## Armadilhas

### (1) Confundir "Spring" com "Spring Boot"

**Problema:** dizer "estou usando Spring" sem especificar qual camada. Em entrevista, o entrevistador pode entender "apenas o Framework", enquanto o candidato usa Boot com Data e Security.

**Exemplo impreciso:**
> "O projeto usa Spring para persistência e autenticação."

**Fix em 1 linha:** seja específico — "usa Spring Boot 3, Spring Data JPA e Spring Security."

### (2) Achar que Boot substitui o Framework

**Problema:** acreditar que Boot é um produto independente. Na prática, Boot sem Framework não existe — todo bean gerenciado, toda injeção de dependência, todo `@Transactional` é processado pelos módulos core do Spring Framework.

**Consequência:** ao debugar um problema de IoC ou AOP, a documentação relevante está no Spring Framework, não no Spring Boot.

**Fix em 1 linha:** lembre-se que Boot é uma *camada de conveniência*, não um substituto — pesquise na documentação do Framework quando o problema é IoC, AOP ou MVC.

### (3) Misturar imports `javax.*` em projeto Boot 3

**Problema:** copiar código de projeto Boot 2 (ou tutorial antigo) que usa `javax.servlet.*`, `javax.persistence.*` ou `javax.validation.*` num projeto Boot 3.

**Exemplo com erro:**
```java
// Boot 3 — isso NÃO compila
import javax.servlet.http.HttpServletRequest;
import javax.persistence.Entity;
```

**Fix em 1 linha:** substitua todos os imports `javax.*` por `jakarta.*` — use busca global na IDE (Ctrl+Shift+R no IntelliJ).

## Em entrevista

### Frase pronta (inglês)

> "Spring Framework provides the foundational IoC container, AOP infrastructure, and MVC framework that all Spring-based applications rely on. Spring Boot sits on top of that and adds opinionated auto-configuration, curated starter dependencies, and an embedded server, so teams can reach production without boilerplate setup. The trade-off is that Boot's magic can obscure what's actually happening under the hood — which is why understanding the Framework layer is still essential for debugging and for overriding defaults effectively."

### Vocabulário

| Termo PT | Termo EN |
|---|---|
| Inversão de controle | Inversion of Control (IoC) |
| Injeção de dependência | Dependency Injection (DI) |
| Auto-configuração | Auto-configuration |
| Convenção sobre configuração | Convention over configuration |
| Servidor embutido | Embedded server |
| Módulo iniciador | Starter dependency |
| Contêiner de beans | Bean container / ApplicationContext |
| Monitoramento em produção | Actuator / production-ready features |

## Veja também

- [[03-Dominios/Java/Spring Core e Boot/02 - IoC e injeção de dependência no Spring|IoC e injeção de dependência no Spring]]
- [[03-Dominios/Java/Spring Core e Boot/15 - Auto-configuration e starters|Auto-configuration e starters]]
- [[03-Dominios/Java/Jakarta EE/14 - Jakarta EE hoje — a plataforma sob o Spring|Jakarta EE hoje — a plataforma sob o Spring]]
- [[03-Dominios/Java/Spring Core e Boot/index|Spring Core e Boot (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Dicionário de Java#Spring Framework|Spring Framework]]
- [[03-Dominios/Java/Dicionário de Java#Spring Boot|Spring Boot]]
- [[03-Dominios/Java/Dicionário de Java#convention over configuration|convention over configuration]]

## Referências

- Spring Boot — página oficial do projeto: <https://spring.io/projects/spring-boot>
- Spring Framework — página oficial do projeto: <https://spring.io/projects/spring-framework>
- Spring Framework — versões e baselines JDK/Jakarta: <https://github.com/spring-projects/spring-framework/wiki/Spring-Framework-Versions>
- Spring Boot Reference Documentation (getting started): <https://docs.spring.io/spring-boot/docs/current/reference/html/getting-started.html>
- Spring Initializr: <https://start.spring.io>
