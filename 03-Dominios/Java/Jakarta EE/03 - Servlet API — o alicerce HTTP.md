---
title: "Servlet API — o alicerce HTTP"
created: 2026-06-07
updated: 2026-06-07
type: concept
progress: backlog
status: seedling
publish: true
fase: iniciado
tags:
  - java
  - jakarta-ee
  - iniciado
  - servlet
aliases:
  - "Servlet"
  - "Servlet API"
  - "HttpServlet"
---

> [!abstract] TL;DR
> A Servlet API é o **contrato entre o código Java e o servidor HTTP** — o container cria **uma única instância** do servlet e a usa para atender **múltiplas threads concorrentes**. Tudo que processa HTTP no ecossistema Java — incluindo o Spring MVC (Galho 9, planejado) — roda sobre essa fundação. Entender o lifecycle e o modelo de threading é a chave para não introduzir bugs silenciosos em produção.

## O que é

A Servlet API (especificação **Jakarta Servlet 6.1**, parte do **Jakarta EE 11**) define um contrato de API que permite escrever componentes Java capazes de receber requisições HTTP e produzir respostas — sem depender de nenhum servidor específico.

O servidor de aplicações (Tomcat, WildFly, Payara, GlassFish) implementa esse contrato através do **servlet container**: uma camada de runtime que gerencia o ciclo de vida dos servlets, o pool de threads, o roteamento de URLs e as sessões HTTP.

A API central vive no pacote `jakarta.servlet` e `jakarta.servlet.http`. A versão 6.1 exige no mínimo **Java SE 17** e removeu todas as referências ao `SecurityManager`, que foi descontinuado na plataforma Java.

## Por que importa

Três razões práticas para todo desenvolvedor Java web conhecer a Servlet API:

1. **É o chão de toda aplicação web Java.** Frameworks como Spring MVC, Jakarta Faces e RESTEasy são construídos sobre servlets. Quando algo dá errado na camada de HTTP, a investigação invariavelmente desce até esse nível.

2. **"O que acontece quando uma requisição chega?"** é pergunta clássica em entrevistas de back-end sênior. A resposta correta passa pelo lifecycle do servlet, pelo modelo de threading e pelo papel do container.

3. **Filters são a origem da ideia de middleware.** Interceptar e modificar requisições antes de chegarem ao handler — logging, autenticação, compressão, encoding — é um padrão que reaparece em todos os frameworks. Entendê-lo na forma original torna trivial aprender qualquer variante.

## Como funciona

### Lifecycle (`init` → N × `service` → `destroy`)

O container gerencia o lifecycle completo do servlet:

```text
Implantação
    │
    ▼
  init(ServletConfig)          ← chamado UMA VEZ
    │                            (inicializa recursos: pool, cache, etc.)
    ▼
 service(request, response)    ← chamado N VEZES, em threads concorrentes
    │                            (roteia para doGet, doPost, etc.)
    ▼
destroy()                      ← chamado UMA VEZ na desimplantação
                                 (libera recursos)
```

**O ponto crítico:** o container cria **uma única instância** do servlet e a reutiliza para todas as requisições. Múltiplas threads executam `service()` simultaneamente nessa mesma instância. Isso define o modelo de memória que toda a programação de servlets pressupõe.

Para detalhes sobre sincronização e visibilidade entre threads, veja [[03-Dominios/Java/Concorrência e paralelismo/index|Concorrência (Galho 4)]] — o servlet não gerencia threads, mas o desenvolvedor precisa entender o que compartilha entre elas.

### `HttpServlet` (`doGet`, `doPost` e demais)

`HttpServlet` estende `GenericServlet` e fornece o método `service(HttpServletRequest, HttpServletResponse)` que roteia automaticamente para o método `doXxx` correto com base no verbo HTTP da requisição:

| Método HTTP | Método Java |
|-------------|-------------|
| GET | `doGet(req, resp)` |
| POST | `doPost(req, resp)` |
| PUT | `doPut(req, resp)` |
| DELETE | `doDelete(req, resp)` |
| PATCH | `doPatch(req, resp)` |
| HEAD | `doHead(req, resp)` |
| OPTIONS | `doOptions(req, resp)` |

A recomendação da spec é **nunca sobrescrever `service()`** — apenas os métodos `doXxx` específicos que a classe precisar atender.

**`HttpServletRequest`** expõe a requisição recebida:

- `getMethod()` — verbo HTTP ("GET", "POST", ...)
- `getRequestURI()` — path da URL
- `getParameter(name)` — parâmetro de query string ou form
- `getHeader(name)` — valor de um cabeçalho
- `getInputStream()` / `getReader()` — corpo da requisição
- `getCookies()` — cookies enviados pelo cliente
- `getSession()` / `getSession(boolean)` — gerenciamento de sessão

**`HttpServletResponse`** controla a resposta enviada:

- `setStatus(int)` — código HTTP (200, 404, 500...)
- `setContentType(String)` — MIME type ("application/json", "text/html")
- `setHeader(name, value)` — adiciona ou sobrescreve cabeçalho
- `getWriter()` — stream de texto para o corpo da resposta
- `getOutputStream()` — stream binário para o corpo da resposta

### Sessões (`HttpSession`, cookies e o trade-off de estado no servidor)

HTTP é stateless por natureza. `HttpSession` é o mecanismo da Servlet API para manter estado entre requisições do mesmo cliente:

```java
HttpSession session = request.getSession();          // cria se não existir
HttpSession session = request.getSession(false);     // retorna null se não existir

session.setAttribute("cart", cartObject);            // armazena objeto
Object cart = session.getAttribute("cart");          // recupera objeto
session.removeAttribute("cart");                     // remove
session.invalidate();                                // termina a sessão

session.setMaxInactiveInterval(1800);                // timeout em segundos (30 min)
int timeout = session.getMaxInactiveInterval();
String id = session.getId();                         // ID único da sessão
boolean isNew = session.isNew();                     // cliente ainda não reconheceu
```

Por padrão, o container rastreia a sessão via **cookie** (`JSESSIONID`). Quando o cliente não aceita cookies, o container pode usar URL rewriting (acrescentar o ID na URL), mas essa abordagem é rara em aplicações modernas.

**Trade-off:** a sessão vive na memória do servidor. Em ambientes com múltiplas instâncias (load balancer), é preciso sticky sessions ou um session store externo (Redis, banco). Guarde o mínimo necessário na sessão e configure sempre um timeout razoável.

### Filters e listeners

**Filters** interceptam requisições antes de chegarem ao servlet (e respostas antes de saírem). Implementam a interface `Filter`:

```java
public interface Filter {
    default void init(FilterConfig filterConfig) throws ServletException { }

    void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
        throws IOException, ServletException;

    default void destroy() { }
}
```

O padrão dentro de `doFilter`:
1. Examinar (e opcionalmente modificar) a requisição.
2. Chamar `chain.doFilter(request, response)` para passar ao próximo elo (outro filtro ou o servlet).
3. Após o retorno do `chain.doFilter`, examinar (e opcionalmente modificar) a resposta.

Casos de uso comuns: logging, autenticação/autorização, compressão GZIP, configuração de encoding, CORS headers.

**Listeners** reagem a eventos do container sem interceptar o fluxo de requisições:

| Interface | Quando é notificado |
|---|---|
| `ServletContextListener` | Aplicação iniciando (`contextInitialized`) ou parando (`contextDestroyed`) |
| `HttpSessionListener` | Sessão criada ou destruída |
| `HttpSessionAttributeListener` | Atributo adicionado, removido ou substituído na sessão |
| `ServletRequestListener` | Requisição entrando ou saindo do escopo do servlet |

`ServletContextListener` é o ponto canônico para inicializar recursos compartilhados (pool de conexões, caches, agendadores) na subida da aplicação e liberá-los no shutdown.

### Registro (`@WebServlet` vs `web.xml`) e async processing

**Via anotação** (abordagem moderna):

```java
@WebServlet(
    name        = "OrderServlet",
    urlPatterns = "/orders",
    asyncSupported = false
)
public class OrderServlet extends HttpServlet { ... }

@WebFilter(urlPatterns = "/*")
public class LoggingFilter implements Filter { ... }

@WebListener
public class AppStartupListener implements ServletContextListener { ... }
```

**Via `web.xml`** (deployment descriptor, ainda válido):

```xml
<servlet>
    <servlet-name>OrderServlet</servlet-name>
    <servlet-class>com.example.OrderServlet</servlet-class>
</servlet>
<servlet-mapping>
    <servlet-name>OrderServlet</servlet-name>
    <url-pattern>/orders</url-pattern>
</servlet-mapping>
```

**Quando usar cada um:**

- Use `@WebServlet` / `@WebFilter` / `@WebListener` em novos projetos: configuração co-localizada com o código, sem arquivos extras.
- Use `web.xml` quando precisar de configuração externalizada (deployments em ambientes diferentes sem recompilar), quando a ordem dos filtros precisar ser garantida de forma explícita, ou para sobrescrever anotações sem modificar o source.
- Ambas podem coexistir; o `web.xml` tem precedência quando conflita com anotações.

**Async processing:** a Servlet API suporta processamento assíncrono via `AsyncContext` (habilitado com `asyncSupported = true` na anotação ou `web.xml`). Ao chamar `request.startAsync()`, o container libera a thread do pool para outras requisições enquanto uma operação de longa duração (I/O, chamada externa) ocorre em segundo plano. Quando o processamento termina, `asyncContext.complete()` fecha a resposta. Essa funcionalidade existe mas é raramente usada diretamente — frameworks reativos e o Jakarta REST abstraem sobre ela.

## Na prática

### `OrderServlet` — lista e criação de pedidos

```java
package com.example.orders;

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.io.PrintWriter;

@WebServlet(name = "OrderServlet", urlPatterns = "/orders")
public class OrderServlet extends HttpServlet {

    // ATENÇÃO: campos de instância são compartilhados entre threads.
    // Aqui, apenas String imutável — seguro.
    private static final String CONTENT_TYPE = "application/json;charset=UTF-8";

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException {

        resp.setStatus(HttpServletResponse.SC_OK);
        resp.setContentType(CONTENT_TYPE);

        try (PrintWriter out = resp.getWriter()) {
            // Exemplo didático: JSON codificado à mão.
            // Em produção, use uma biblioteca (Jackson, Gson, etc.)
            out.println("[");
            out.println("  {\"id\": 1, \"product\": \"Notebook\", \"status\": \"PENDING\"},");
            out.println("  {\"id\": 2, \"product\": \"Mouse\",    \"status\": \"SHIPPED\"}");
            out.println("]");
        }
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException {

        // Lê parâmetros de form ou query string
        String product = req.getParameter("product");
        String quantity = req.getParameter("quantity");

        if (product == null || product.isBlank()) {
            resp.sendError(HttpServletResponse.SC_BAD_REQUEST, "product é obrigatório");
            return;
        }

        resp.setStatus(HttpServletResponse.SC_CREATED);
        resp.setContentType(CONTENT_TYPE);

        try (PrintWriter out = resp.getWriter()) {
            out.printf("{\"product\": \"%s\", \"quantity\": \"%s\", \"status\": \"CREATED\"}%n",
                product, quantity);
        }
    }
}
```

### `LoggingFilter` — registro de todas as requisições

```java
package com.example.filters;

import jakarta.servlet.Filter;
import jakarta.servlet.FilterChain;
import jakarta.servlet.FilterConfig;
import jakarta.servlet.ServletException;
import jakarta.servlet.ServletRequest;
import jakarta.servlet.ServletResponse;
import jakarta.servlet.annotation.WebFilter;
import jakarta.servlet.http.HttpServletRequest;
import java.io.IOException;

@WebFilter(urlPatterns = "/*")   // intercepta TUDO
public class LoggingFilter implements Filter {

    @Override
    public void init(FilterConfig filterConfig) throws ServletException {
        System.out.println("[LoggingFilter] inicializado");
    }

    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
            throws IOException, ServletException {

        HttpServletRequest httpReq = (HttpServletRequest) request;

        long inicio = System.currentTimeMillis();
        System.out.printf("[REQ]  %s %s%n", httpReq.getMethod(), httpReq.getRequestURI());

        chain.doFilter(request, response);   // <-- delegar é obrigatório

        long duracao = System.currentTimeMillis() - inicio;
        System.out.printf("[RESP] %s concluído em %d ms%n",
            httpReq.getRequestURI(), duracao);
    }

    @Override
    public void destroy() {
        System.out.println("[LoggingFilter] destruído");
    }
}
```

## Armadilhas

### (1) Estado mutável em campo de servlet — race condition silenciosa

**O problema:** como o container mantém uma única instância do servlet para múltiplas threads, qualquer campo de instância mutável é um recurso compartilhado. Modificá-lo sem sincronização causa race conditions que só aparecem sob carga.

```java
// ERRADO — campo mutável compartilhado entre todas as threads
@WebServlet("/orders")
public class OrderServlet extends HttpServlet {
    private int requestCount = 0;   // não é thread-safe!

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException {
        requestCount++;             // duas threads lendo e escrevendo ao mesmo tempo
        resp.getWriter().println("Requests: " + requestCount);
    }
}
```

**Fix:** use atributos de request ou de sessão para dados por-requisição; use tipos thread-safe (`AtomicInteger`, `ConcurrentHashMap`) para estado global; prefira imutabilidade.

```java
// CORRETO — contador thread-safe
private final AtomicInteger requestCount = new AtomicInteger(0);

requestCount.incrementAndGet();   // operação atômica
```

### (2) Filter sem `chain.doFilter` — requisição morre silenciosamente

**O problema:** se um filter não chamar `chain.doFilter()` e também não escrever uma resposta, o cliente fica esperando indefinidamente (ou recebe uma resposta vazia). Erros nessa linha são difíceis de diagnosticar porque não geram exceção — a requisição simplesmente desaparece.

```java
// ERRADO — filtro que "engole" a requisição
@Override
public void doFilter(ServletRequest req, ServletResponse resp, FilterChain chain)
        throws IOException, ServletException {
    HttpServletRequest httpReq = (HttpServletRequest) req;
    if (!isAuthorized(httpReq)) {
        // esqueceu de enviar 401 E não delegou — cliente fica pendurado
        return;
    }
    chain.doFilter(req, resp);
}
```

**Fix:** sempre faça uma das duas coisas: **delegar** (`chain.doFilter`) ou **responder** (`resp.sendError` / `resp.setStatus` + corpo). Nunca retorne sem fazer nenhuma das duas.

```java
// CORRETO
if (!isAuthorized(httpReq)) {
    ((HttpServletResponse) resp).sendError(HttpServletResponse.SC_UNAUTHORIZED);
    return;   // resposta enviada — ok não delegar
}
chain.doFilter(req, resp);
```

### (3) Objetos pesados na sessão sem timeout configurado — vazamento de memória

**O problema:** tudo armazenado em `HttpSession` vive na heap do servidor até a sessão expirar. Em aplicações de alto tráfego, sessões abandonadas (usuário fechou o browser sem fazer logout) acumulam objetos grandes e causam `OutOfMemoryError` silencioso.

```java
// ARRISCADO — produto completo (com imagens, histórico, etc.) na sessão
session.setAttribute("currentProduct", fatProductObject);   // pode ser MB por sessão
```

**Fix:** armazene apenas o mínimo na sessão (IDs, primitivos); configure timeout explícito no `web.xml` (`<session-timeout>30</session-timeout>` em minutos); use `session.invalidate()` no logout; considere session stores externos com eviction automática em arquiteturas escaláveis.

```java
// MELHOR — apenas o ID; busque o objeto quando precisar
session.setAttribute("currentProductId", productId);
```

## Em entrevista

### Frase pronta (inglês)

> "A servlet is a Java class managed by the servlet container — the container creates a single instance and dispatches every incoming HTTP request to that same instance on potentially many concurrent threads. That means any mutable instance field is a shared resource and must be thread-safe or avoided entirely. The lifecycle is straightforward: `init` runs once at deployment, `service` (routed to `doGet`, `doPost`, etc.) runs for every request, and `destroy` runs once at undeployment. Filters wrap around servlets to implement cross-cutting concerns like logging and authentication, and every filter must either call `chain.doFilter` to continue the chain or write a response — there is no middle ground."

### Vocabulário

| Termo PT | Termo EN |
|---|---|
| Contêiner de servlet | Servlet container |
| Ciclo de vida | Lifecycle |
| Instância única | Single instance |
| Cadeia de filtros | Filter chain |
| Sessão HTTP | HTTP session |
| Escuta de eventos | Event listener |
| Processamento assíncrono | Async processing |
| Descritor de implantação | Deployment descriptor |
| Encaminhamento de requisição | Request dispatch |
| Thread-safe | Thread-safe |

## Veja também

- [[01 - O modelo Jakarta EE — especificações e implementações]]
- [[07 - JAX-RS — REST declarativo]]
- [[03-Dominios/Java/Concorrência e paralelismo/index|Concorrência (Galho 4)]]
- [[03-Dominios/Java/Jakarta EE/index|Jakarta EE (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Dicionário de Java#servlet|servlet (Dicionário)]]
- [[03-Dominios/Java/Dicionário de Java#servlet container|servlet container (Dicionário)]]

## Referências

- Jakarta Servlet 6.1 Specification — <https://jakarta.ee/specifications/servlet/6.1/> — acesso 2026-06-07
- Jakarta Servlet 6.1 API Docs — <https://jakarta.ee/specifications/servlet/6.1/apidocs/> — acesso 2026-06-07
- `HttpServlet` Javadoc — <https://jakarta.ee/specifications/servlet/6.1/apidocs/jakarta.servlet/jakarta/servlet/http/httpservlet> — acesso 2026-06-07
- `HttpServletRequest` Javadoc — <https://jakarta.ee/specifications/servlet/6.1/apidocs/jakarta.servlet/jakarta/servlet/http/httpservletrequest> — acesso 2026-06-07
- `Filter` Javadoc — <https://jakarta.ee/specifications/servlet/6.1/apidocs/jakarta.servlet/jakarta/servlet/filter> — acesso 2026-06-07
- `AsyncContext` Javadoc — <https://jakarta.ee/specifications/servlet/6.1/apidocs/jakarta.servlet/jakarta/servlet/asynccontext> — acesso 2026-06-07
