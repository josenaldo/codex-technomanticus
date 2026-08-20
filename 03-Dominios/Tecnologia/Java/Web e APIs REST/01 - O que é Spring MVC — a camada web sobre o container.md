---
title: "O que é Spring MVC — a camada web sobre o container"
created: 2026-06-08
updated: 2026-06-10
type: concept
progress: backlog
status: seedling
publish: true
fase: Iniciado
tags:
  - java
  - web
  - iniciado
  - spring-mvc
aliases:
  - "Spring MVC"
  - "Spring Web MVC"
---

# O que é Spring MVC — a camada web sobre o container

> [!abstract] TL;DR
> **Spring MVC** (formalmente *Spring Web MVC*, módulo `spring-webmvc`) é a camada web **servlet-based e imperativa** do Spring Framework. Ele segue o padrão **front controller**: um único servlet, o `DispatcherServlet`, recebe **todo** request HTTP e delega o trabalho real a componentes configuráveis — controllers, conversores, resolvedores. Por baixo, ele implementa as specs HTTP do Galho 7 (Servlet API) e roda sobre o container IoC do Galho 8 (os controllers são beans). É o caminho do Spring para transformar uma requisição HTTP em uma resposta.

## O que é

Spring MVC é o framework web original do Spring, construído **diretamente sobre a Servlet API** e presente no Spring Framework desde o início. O nome "MVC" vem de *Model-View-Controller*, mas hoje, em backends de API REST, o "View" raramente renderiza HTML — ele serializa JSON. O coração não é a sigla, é o padrão arquitetural que está por trás dela.

### Front controller: uma porta única

A documentação oficial é explícita:

> *"Spring MVC, as many other web frameworks, is designed around the front controller pattern where a central `Servlet`, the `DispatcherServlet`, provides a shared algorithm for request processing, while actual work is performed by configurable delegate components."*

Traduzindo a ideia: em vez de cada endpoint ter seu próprio servlet (como na era pré-frameworks), **um único servlet é a porta de entrada de toda a aplicação**. Esse servlet é o `DispatcherServlet`. Ele não contém regra de negócio — ele é um *despachante*: recebe o request, descobre quem deve tratá-lo (qual controller), invoca, pega o resultado e produz a resposta.

Pense num hotel grande. Você não bate na porta de cada quarto procurando o hóspede certo; você fala com a **recepção** (front controller), que sabe para onde encaminhar. O `DispatcherServlet` é essa recepção. A mecânica detalhada de como ele orquestra cada etapa — `HandlerMapping`, `HandlerAdapter`, conversores, resolvedores de exceção — fica para a [[03-Dominios/Tecnologia/Java/Web e APIs REST/06 - O pipeline do DispatcherServlet|nota 06]]. Aqui basta a visão geral: porta única, delegação para dentro.

### MVC vs REST

Vale separar dois conceitos que coexistem no mesmo framework:

| | Estilo MVC clássico | Estilo REST (APIs) |
|---|---|---|
| Resposta | View renderizada (HTML, Thymeleaf, JSP) | Representação serializada (JSON, XML) |
| Foco | Páginas | **Recursos** (`/orders`, `/orders/42`) |
| Verbos | `GET`/`POST` (formulários) | `GET`/`POST`/`PUT`/`PATCH`/`DELETE` (semântica HTTP completa) |
| Estado | Pode usar sessão | **Stateless** (cada request é autossuficiente) |
| Anotação típica | `@Controller` + view | `@RestController` (corpo serializado direto) |

REST não é um framework — é um **estilo arquitetural**: recursos endereçáveis por URI, manipulados pelos verbos HTTP, em interações sem estado de servidor. Spring MVC suporta os dois estilos com o mesmo `DispatcherServlet`; a diferença está em como o controller é anotado e em como a resposta é produzida.

## Por que importa

Spring MVC é, na prática, **como toda request HTTP vira resposta num backend Spring tradicional**. Se você sobe um serviço com `spring-boot-starter-web`, é o `DispatcherServlet` que está na frente recebendo cada chamada. Entender essa camada é entender o ponto onde o mundo externo (HTTP, JSON, status codes) encontra o seu código (beans, métodos, objetos de domínio).

Em entrevista, isso aparece como a pergunta clássica: **"o que acontece, do começo ao fim, quando chega um request na sua aplicação Spring?"**. Quem só sabe escrever `@GetMapping` trava; quem entende o front controller responde com clareza: o request chega no servidor embarcado (Tomcat), é entregue ao `DispatcherServlet`, que mapeia para um handler, invoca o controller (um bean do container), converte o retorno em JSON e escreve a resposta. Essa narrativa demonstra que você enxerga a arquitetura, não só a API.

## Como funciona

### O padrão front controller e o DispatcherServlet

O `DispatcherServlet` centraliza o **algoritmo compartilhado** de processamento de request e delega o trabalho específico. Segundo a doc, ele *"uses Spring configuration to discover the delegate components it needs for request mapping, view resolution, exception handling, and more"*.

Ou seja: o `DispatcherServlet` por si só não sabe que existe um `OrderController`. Ele descobre isso **consultando o contexto Spring** em tempo de inicialização, registrando os componentes de mapeamento. Quando um request chega, ele percorre seu algoritmo fixo (achar handler → invocar → converter resposta → tratar exceção) usando esses delegados configuráveis. O algoritmo é estável; os participantes são plugáveis. É isso que dá flexibilidade ao framework sem que você precise tocar no núcleo.

### Spring MVC sobre o Servlet container (o DispatcherServlet é um servlet — Galho 7)

Aqui está o elo com o [[03-Dominios/Tecnologia/Java/Jakarta EE/03 - Servlet API — o alicerce HTTP|Servlet API]]: **o `DispatcherServlet` é, literalmente, um `jakarta.servlet.http.HttpServlet`**. Toda a "mágica" do Spring MVC está, na base, sentada sobre o contrato Servlet definido na plataforma Jakarta EE.

Quem chama o `DispatcherServlet` é o **servlet container** (Tomcat, Jetty, Undertow). O container faz o trabalho de baixo nível — abrir o socket, fazer o parsing do HTTP, gerenciar o pool de threads — e entrega ao servlet um `HttpServletRequest` e um `HttpServletResponse`. Sem o Spring Boot, você declararia esse servlet manualmente via `WebApplicationInitializer`:

```java
public class MyWebApplicationInitializer implements WebApplicationInitializer {
    @Override
    public void onStartup(ServletContext servletContext) {
        var context = new AnnotationConfigWebApplicationContext();
        context.register(AppConfig.class);

        var servlet = new DispatcherServlet(context);
        ServletRegistration.Dynamic registration =
            servletContext.addServlet("app", servlet);
        registration.setLoadOnStartup(1);
        registration.addMapping("/app/*");
    }
}
```

Com Spring Boot 3.x, **nada disso é escrito à mão**: o starter web detecta o classpath, sobe um Tomcat embutido e registra o `DispatcherServlet` mapeado em `/` automaticamente. Mas é importante saber que essa camada existe — o servlet não desaparece, só fica configurado por convenção.

> [!info] Baseline
> A baseline desta nota é **Spring Boot 3.x / Spring Framework 6.x**, que exige **Java 17+** e usa o namespace **`jakarta.*`** (não `javax.*`). Versões mais recentes (Framework 7.x / Boot 4.x) já existem e elevam o baseline de runtime, mas o modelo do `DispatcherServlet` descrito aqui permanece o mesmo.

### Controllers são beans do contexto (Galho 8)

O `OrderController` não é instanciado por você com `new`. Ele é um **bean gerenciado pelo container IoC** — exatamente o mecanismo do [[03-Dominios/Tecnologia/Java/Spring Core e Boot/index|Spring Core e Boot]]. A anotação `@RestController` é um estereótipo: por baixo, ela é um `@Component`, então o component scan a detecta e registra como bean no `WebApplicationContext`.

A consequência prática é poderosa: como o controller é um bean, ele recebe **injeção de dependência** normalmente. Um `OrderController` pode declarar um `OrderService` no construtor e o container injeta a colaboração. O `DispatcherServlet`, ao descobrir os handlers, está apenas lendo o catálogo de beans web do contexto. Camada web e camada de container são o mesmo grafo de objetos.

### Spring MVC vs WebFlux (servlet/imperativo vs reativo)

Spring MVC é **imperativo e bloqueante por modelo**: cada request ocupa uma thread do pool do servlet container do início ao fim (*thread-per-request*). É simples de raciocinar e cobre a esmagadora maioria dos backends.

O Spring oferece uma alternativa reativa, o **WebFlux** ([[03-Dominios/Tecnologia/Java/Programação Reativa/10 - Spring WebFlux — o stack não-bloqueante sobre Netty e o DispatcherHandler|Galho 11]]), construído sobre Reactor e um modelo não-bloqueante, sem depender da Servlet API. WebFlux brilha em cenários de altíssima concorrência com I/O dominante (muitas conexões esperando), trocando simplicidade por escalabilidade de threads. Para esta trilha e para a maioria das APIs CRUD, **Spring MVC é o ponto de partida correto** — e os dois não se misturam no mesmo fluxo de request.

## Na prática

Uma aplicação Spring Boot mínima com um endpoint REST. O `@SpringBootApplication` é o ponto de entrada; o `@RestController` define o recurso.

```java
package com.example.shop;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class ShopApplication {
    public static void main(String[] args) {
        SpringApplication.run(ShopApplication.class, args);
    }
}
```

```java
package com.example.shop.web;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

record Order(Long id, String customer, int total) {}

@RestController
@RequestMapping("/orders")
public class OrderController {

    @GetMapping("/{id}")
    public Order findById(@PathVariable Long id) {
        // num serviço real, isto viria de um OrderService injetado
        return new Order(id, "ACME Ltda", 4200);
    }
}
```

Um `GET /orders/42` é recebido pelo Tomcat embutido, repassado ao `DispatcherServlet`, mapeado para `OrderController#findById`, e o `Order` retornado é serializado em JSON automaticamente (via Jackson, que vem no starter). Nenhuma linha de código de serialização ou de roteamento foi escrita.

O `pom.xml` precisa apenas do starter web — ele traz Spring MVC, Tomcat embutido e Jackson de uma vez:

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.3.0</version>
    </parent>

    <groupId>com.example</groupId>
    <artifactId>shop</artifactId>
    <version>0.0.1-SNAPSHOT</version>

    <properties>
        <java.version>17</java.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
    </dependencies>
</project>
```

## Armadilhas

### (1) Confundir Spring MVC imperativo com WebFlux reativo

São **dois stacks web distintos** que compartilham anotações parecidas (`@GetMapping`, `@RestController`), o que ilude. Misturar tipos reativos (`Mono`, `Flux`) em um controller servlet-based esperando que "fique não-bloqueante" não funciona como se imagina, e adicionar os dois starters cria conflitos de configuração.

```java
// MVC servlet-based — está OK retornar o objeto direto:
@GetMapping("/{id}")
public Order findById(@PathVariable Long id) { ... }

// WebFlux (Galho 11) usaria outro starter e Mono<Order>.
// Não basta trocar o tipo de retorno: o stack inteiro muda.
```

**Fix:** escolha um stack por aplicação. Para esta trilha, use `spring-boot-starter-web` (MVC) e mantenha controllers retornando objetos de domínio, não `Mono`/`Flux`.

### (2) Achar que `@RestController` "é" JAX-RS

`@RestController` (Spring) e [[03-Dominios/Tecnologia/Java/Jakarta EE/07 - JAX-RS — REST declarativo|JAX-RS]] (`@Path`, `@GET`, da plataforma Jakarta EE) resolvem **o mesmo problema** — expor recursos REST — mas são **APIs concorrentes e incompatíveis entre si**. As anotações têm nomes e pacotes diferentes e não são intercambiáveis.

```java
// Spring MVC:
@RestController
@RequestMapping("/orders")
class OrderController { @GetMapping("/{id}") Order get(...) {} }

// JAX-RS (Jakarta EE) — outra API, outros imports:
@Path("/orders")
class OrderResource { @GET @Path("/{id}") Order get(...) {} }
```

**Fix:** num projeto Spring, fique no modelo Spring MVC (`@RestController`); trate JAX-RS como o "outro caminho", relevante quando o ambiente é um servidor Jakarta EE puro.

## Em entrevista

### Frase pronta (inglês)

> Spring MVC is the servlet-based, imperative web layer of the Spring Framework: it follows the front controller pattern, where a single `DispatcherServlet` receives every HTTP request and delegates the actual work to controller beans from the application context. I usually default to it for REST APIs because the thread-per-request model is simple to reason about and integrates seamlessly with the IoC container — the controllers are just beans, so they get dependency injection for free. The trade-off is that it's blocking by design, so for workloads with extreme concurrency and I/O-bound waits I'd evaluate WebFlux, the reactive stack, instead — but I wouldn't reach for it by default, since it adds real cognitive cost.

### Vocabulário

| Termo PT | Termo EN |
|---|---|
| camada web | web layer |
| padrão front controller | front controller pattern |
| servlet despachante / porta única | dispatcher servlet / single entry point |
| container de servlet | servlet container |
| componente delegado | delegate component |
| mapeamento de handler | handler mapping |
| bloqueante / não-bloqueante | blocking / non-blocking |
| uma thread por requisição | thread-per-request |
| stack reativo | reactive stack |
| sem estado | stateless |

## Veja também

- [[03-Dominios/Tecnologia/Java/Web e APIs REST/06 - O pipeline do DispatcherServlet|O pipeline do DispatcherServlet]] — a mecânica etapa a etapa
- [[03-Dominios/Tecnologia/Java/Web e APIs REST/02 - @RestController e os mapeamentos|@RestController e os mapeamentos]] — como declarar os endpoints
- [[03-Dominios/Tecnologia/Java/Jakarta EE/03 - Servlet API — o alicerce HTTP|Servlet API]] — a spec por baixo: o DispatcherServlet é um servlet
- [[03-Dominios/Tecnologia/Java/Jakarta EE/07 - JAX-RS — REST declarativo|JAX-RS]] — o outro caminho pro mesmo problema
- [[03-Dominios/Tecnologia/Java/Spring Core e Boot/index|Spring Core e Boot]] — o container que gerencia os controllers
- [[03-Dominios/Tecnologia/Java/Web e APIs REST/index|Web e APIs REST]] — MOC do galho
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- Verbetes: [[03-Dominios/Tecnologia/Java/Dicionário de Java#Spring MVC|Spring MVC]], [[03-Dominios/Tecnologia/Java/Dicionário de Java#DispatcherServlet|DispatcherServlet]], [[03-Dominios/Tecnologia/Java/Dicionário de Java#front controller|front controller]]

## Referências

- Spring Framework Reference — Web on Servlet Stack (Spring Web MVC): https://docs.spring.io/spring-framework/reference/web/webmvc.html
- Spring Framework Reference — DispatcherServlet: https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-servlet.html
