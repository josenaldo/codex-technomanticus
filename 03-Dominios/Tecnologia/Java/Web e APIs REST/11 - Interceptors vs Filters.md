---
title: "Interceptors vs Filters"
created: 2026-06-08
updated: 2026-06-10
type: concept
progress: backlog
status: seedling
publish: true
fase: Adepto
tags:
  - java
  - web
  - adepto
  - spring-mvc
aliases:
  - "HandlerInterceptor vs Filter"
---

# Interceptors vs Filters

> [!abstract] TL;DR
> Filter é nível container — actua **antes do DispatcherServlet**, intercepta qualquer requisição HTTP e não sabe nada sobre o handler que vai processar. `HandlerInterceptor` vive **dentro do Spring MVC**, enxerga o handler method e o `ModelAndView`. A regra de escolha é simples: use Filter quando a lógica precisa atuar na camada de servlet (encoding, CORS cru, log bruto); use Interceptor quando precisa de contexto MVC (saber qual controller/método vai responder, manipular o modelo).

## O que é

**Servlet Filter** é uma interface da Servlet API (`jakarta.servlet.Filter`) que permite interceptar requisições e respostas HTTP no nível do container — ou seja, antes que o `DispatcherServlet` do Spring sequer receba a requisição. Filters formam uma cadeia (`FilterChain`) e podem encurtar ou transformar o fluxo em qualquer ponto.

**`HandlerInterceptor`** é uma interface do Spring MVC (`org.springframework.web.servlet.HandlerInterceptor`) que age **depois** que o `DispatcherServlet` já mapeou a requisição para um handler. Tem acesso ao objeto handler (normalmente um `HandlerMethod` que representa o método do controller) e ao `ModelAndView` resultante.

Os dois mecanismos coexistem, mas atuam em camadas distintas do pipeline:

```text
Requisição HTTP
    ↓
[ Servlet Container ]
    → Filter 1 → Filter 2 → ... → FilterChain
                                       ↓
                               [ DispatcherServlet ]
                                   → HandlerMapping
                                   → HandlerInterceptor.preHandle()
                                   → Handler (Controller)
                                   → HandlerInterceptor.postHandle()
                                   → ViewResolver / Response write
                                   → HandlerInterceptor.afterCompletion()
```

## Por que importa

Em entrevistas e no dia-a-dia, a confusão entre os dois é comum — e colocar lógica na camada errada cria bugs difíceis de diagnosticar:

- Um Filter **não tem acesso ao handler method**: não dá para saber que método do controller vai executar, portanto não dá para fazer decisões baseadas em anotações do método.
- Um `HandlerInterceptor` **só executa se a requisição passou pelo DispatcherServlet**: requisições para recursos estáticos servidos directamente pelo container podem não passar pelos interceptors.
- A ordem de execução importa: Filters rodam antes dos interceptors; se um Filter encerrar a cadeia, nenhum interceptor é invocado.

Entender a fronteira das camadas evita:
- Lógica de autenticação/autorização em interceptors (onde path matching pode divergir — a própria doc do Spring recomenda Spring Security ou Filters para segurança);
- Encoding ou log bruto em interceptors, perdendo requisições que não chegam ao DispatcherServlet;
- Vazamentos de recursos (ex.: MDC do logging) por não limpar no `afterCompletion`.

## Como funciona

### Servlet Filter: nível container, antes do DispatcherServlet (FilterRegistrationBean)

Um Filter implementa `jakarta.servlet.Filter` e é registrado no container. No Spring Boot, a forma recomendada é via `FilterRegistrationBean`:

```java
import jakarta.servlet.Filter;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.ServletRequest;
import jakarta.servlet.ServletResponse;
import jakarta.servlet.http.HttpServletRequest;
import java.io.IOException;
import org.springframework.boot.web.servlet.FilterRegistrationBean;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class FilterConfig {

    @Bean
    public FilterRegistrationBean<RequestIdFilter> requestIdFilter() {
        FilterRegistrationBean<RequestIdFilter> registration = new FilterRegistrationBean<>();
        registration.setFilter(new RequestIdFilter());
        registration.addUrlPatterns("/*");
        registration.setOrder(1);
        return registration;
    }
}

public class RequestIdFilter implements Filter {

    @Override
    public void doFilter(ServletRequest request, ServletResponse response,
                         FilterChain chain) throws IOException, ServletException {
        HttpServletRequest httpRequest = (HttpServletRequest) request;
        // actua ANTES do DispatcherServlet — sem acesso ao handler
        String requestId = httpRequest.getHeader("X-Request-Id");
        // ... propaga requestId
        chain.doFilter(request, response); // passa adiante
    }
}
```

Alternativa para filtros com ciclo de vida Spring: estender `OncePerRequestFilter` (garante execução única por request, mesmo em forwards/includes).

### HandlerInterceptor: dentro do Spring MVC, com o handler method (preHandle/postHandle/afterCompletion)

`HandlerInterceptor` tem três métodos:

| Método | Quando executa | Parâmetros notáveis | Retorno |
|---|---|---|---|
| `preHandle` | Antes do handler | `Object handler` (normalmente `HandlerMethod`) | `boolean` — `false` aborta a cadeia |
| `postHandle` | Após o handler, antes do render | `ModelAndView modelAndView` (pode ser null) | `void` |
| `afterCompletion` | Após o render (ou após erro) | `Exception ex` (null se sem erro) | `void` |

> [!warning] Atenção com `@ResponseBody` / `ResponseEntity`
> Para métodos que escrevem a resposta directamente (REST APIs), a resposta já está **commitada** quando `postHandle` é chamado — não dá para adicionar headers. Use `ResponseBodyAdvice` nesses casos.

```java
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.web.method.HandlerMethod;
import org.springframework.web.servlet.HandlerInterceptor;
import org.springframework.web.servlet.ModelAndView;

public class TraceInterceptor implements HandlerInterceptor {

    @Override
    public boolean preHandle(HttpServletRequest request,
                             HttpServletResponse response,
                             Object handler) throws Exception {
        if (handler instanceof HandlerMethod hm) {
            // acesso ao método e controller — impossível num Filter
            String controllerName = hm.getBeanType().getSimpleName();
            String methodName = hm.getMethod().getName();
            System.out.println("Handling: " + controllerName + "#" + methodName);
        }
        return true; // continua a cadeia
    }

    @Override
    public void afterCompletion(HttpServletRequest request,
                                HttpServletResponse response,
                                Object handler,
                                Exception ex) throws Exception {
        // limpeza garantida mesmo em caso de excepção
    }
}
```

### Quando usar cada um — e a ordem de execução

| Situação | Ferramenta certa | Motivo |
|---|---|---|
| Forçar character encoding | `Filter` | Precisa actuar antes de qualquer leitura do body |
| Log bruto de request/response | `Filter` | Captura tudo, incluindo erros antes do DispatcherServlet |
| CORS (sem Spring Security) | `CorsFilter` ou config MVC | Filter para granularidade máxima; `CorsRegistry` para simplicidade |
| MDC / traceId no logging | `HandlerInterceptor` | Quer associar o trace ao handler name |
| Verificar anotação no método | `HandlerInterceptor` | Só o interceptor tem `HandlerMethod` |
| Lógica de segurança/autenticação | Filter (Spring Security) | Path matching mais confiável; Doc Spring recomenda explicitamente |

**Ordem de execução (múltiplos interceptors):** `preHandle` na ordem de registro; `postHandle` e `afterCompletion` na **ordem inversa**. Isso espelha o padrão de pilha — o último a entrar é o primeiro a sair na limpeza.

## Na prática

Caso comum: propagar `traceId` de um header HTTP para o MDC do SLF4J, de forma que todos os logs do request apareçam identificados.

```java
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.slf4j.MDC;
import org.springframework.stereotype.Component;
import org.springframework.web.servlet.HandlerInterceptor;

@Component
public class MdcTraceInterceptor implements HandlerInterceptor {

    private static final String TRACE_KEY = "traceId";

    @Override
    public boolean preHandle(HttpServletRequest request,
                             HttpServletResponse response,
                             Object handler) {
        String traceId = request.getHeader("X-Trace-Id");
        if (traceId == null || traceId.isBlank()) {
            traceId = java.util.UUID.randomUUID().toString();
        }
        MDC.put(TRACE_KEY, traceId);
        response.setHeader("X-Trace-Id", traceId);
        return true;
    }

    @Override
    public void afterCompletion(HttpServletRequest request,
                                HttpServletResponse response,
                                Object handler,
                                Exception ex) {
        MDC.remove(TRACE_KEY); // OBRIGATÓRIO — threads são reutilizadas
    }
}
```

Registro do interceptor via `WebMvcConfigurer`:

```java
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class WebMvcConfig implements WebMvcConfigurer {

    private final MdcTraceInterceptor mdcTraceInterceptor;

    public WebMvcConfig(MdcTraceInterceptor mdcTraceInterceptor) {
        this.mdcTraceInterceptor = mdcTraceInterceptor;
    }

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(mdcTraceInterceptor)
                .addPathPatterns("/**")
                .excludePathPatterns("/actuator/**", "/health");
    }
}
```

> [!tip] Path patterns no interceptor
> `addPathPatterns` e `excludePathPatterns` usam a sintaxe AntPathMatcher (`/**`, `/api/orders/*`). Sem `addPathPatterns`, o interceptor se aplica a todos os paths mapeados pelo DispatcherServlet.

## Armadilhas

### (1) Colocar lógica que depende do handler num Filter

**Problema:** Filters não recebem o `Object handler` — não há como inspecionar anotações do método controller (ex.: `@RequiresRole`, `@Cacheable`) ou saber o nome do controller.

**Exemplo do erro:**

```java
// ❌ ERRADO: Filter tentando ler anotação do controller
public class AnnotationReadingFilter implements Filter {
    @Override
    public void doFilter(ServletRequest request, ServletResponse response,
                         FilterChain chain) throws IOException, ServletException {
        // IMPOSSÍVEL obter o HandlerMethod aqui — não existe essa info no Filter
        // qualquer workaround vira gambiarra frágil
        chain.doFilter(request, response);
    }
}
```

**Fix:** Migrar para `HandlerInterceptor.preHandle` e usar cast para `HandlerMethod`:

```java
// ✅ CORRETO
@Override
public boolean preHandle(HttpServletRequest request,
                         HttpServletResponse response,
                         Object handler) {
    if (handler instanceof HandlerMethod hm) {
        MyAnnotation ann = hm.getMethodAnnotation(MyAnnotation.class);
        if (ann != null) { /* lógica */ }
    }
    return true;
}
```

### (2) Usar interceptor para o que deveria ser Filter (ex.: character encoding)

**Problema:** Se o body for lido antes do interceptor (o que pode acontecer dependendo de outros filters na cadeia), a tentativa de forçar encoding no interceptor chega tarde demais. Além disso, requisições que não chegam ao DispatcherServlet (ex.: recursos estáticos servidos directamente) não passam pelos interceptors.

**Exemplo do erro:**

```java
// ❌ ERRADO: tentar forçar UTF-8 num interceptor
@Override
public boolean preHandle(HttpServletRequest request, ...) {
    request.setCharacterEncoding("UTF-8"); // pode lançar excepção se o body já foi lido
    return true;
}
```

**Fix:** Usar `CharacterEncodingFilter` do Spring (que é um Filter) registrado antes de outros filters:

```java
// ✅ CORRETO — via FilterRegistrationBean com ordem baixa (executa primeiro)
@Bean
public FilterRegistrationBean<CharacterEncodingFilter> encodingFilter() {
    FilterRegistrationBean<CharacterEncodingFilter> bean = new FilterRegistrationBean<>();
    bean.setFilter(new CharacterEncodingFilter("UTF-8", true));
    bean.setOrder(Ordered.HIGHEST_PRECEDENCE);
    return bean;
}
```

### (3) Esquecer de limpar o MDC no afterCompletion (vaza entre requests)

**Problema:** Servidores web (Tomcat, Jetty) usam thread pools — a mesma thread atende requisições diferentes. Se `MDC.put(...)` em `preHandle` não for limpo em `afterCompletion`, o valor vaza para a próxima requisição da thread, poluindo logs com dados errados.

**Exemplo do erro:**

```java
// ❌ ERRADO: sem limpeza do MDC
@Override
public boolean preHandle(HttpServletRequest request, ...) {
    MDC.put("orderId", request.getHeader("X-Order-Id")); // ← vaza se não limpar
    return true;
}
// afterCompletion não implementado
```

**Fix:** Sempre limpar em `afterCompletion` (chamado mesmo em caso de excepção):

```java
// ✅ CORRETO
@Override
public void afterCompletion(HttpServletRequest request,
                            HttpServletResponse response,
                            Object handler, Exception ex) {
    MDC.remove("orderId"); // garante limpeza independente de erro
}
```

> [!warning] Regra de ouro
> Tudo que foi colocado no MDC, ThreadLocal, ou qualquer estado ligado à thread em `preHandle` **deve** ser removido em `afterCompletion`. Nunca depender de `postHandle` para isso — ele não é chamado em caso de excepção.

## Em entrevista

### Frase pronta (inglês)

"In Spring MVC, a Servlet Filter operates at the container level, intercepting requests before they even reach the DispatcherServlet — it's ideal for concerns like character encoding, raw logging, or CORS that need to apply regardless of which handler will respond. A HandlerInterceptor, on the other hand, lives inside the Spring MVC pipeline and has access to the resolved handler object, so you can inspect controller annotations or correlate logs with a specific method. The key question is: does your cross-cutting logic need to know *which* handler will run? If yes, use an interceptor; otherwise, prefer a filter for broader, earlier interception."

### Vocabulário

| PT | EN |
|---|---|
| Filtro de servlet | Servlet Filter |
| Interceptor de handler | Handler Interceptor |
| Cadeia de filtros | Filter chain |
| Método handler | Handler method |
| Antes do processamento | Pre-handle / preHandle |
| Após a conclusão | After completion / afterCompletion |
| Registro de interceptor | Interceptor registration |
| Padrão de caminho | Path pattern |
| Contexto de diagnóstico mapeado | Mapped Diagnostic Context (MDC) |
| Vazamento de contexto de thread | Thread context leak |

## Veja também

- [[03-Dominios/Tecnologia/Java/Web e APIs REST/06 - O pipeline do DispatcherServlet|O pipeline do DispatcherServlet]]
- [[03-Dominios/Tecnologia/Java/Jakarta EE/03 - Servlet API — o alicerce HTTP|Servlet API]] (a spec dos filters)
- [[03-Dominios/Tecnologia/Java/Web e APIs REST/index|Web e APIs REST]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- Verbete: [[03-Dominios/Tecnologia/Java/Dicionário de Java#HandlerInterceptor|HandlerInterceptor]]

Autenticação, CSRF e autorização pertencem ao galho [[03-Dominios/Tecnologia/Java/Segurança/06 - A arquitetura do filter chain em profundidade|Segurança]], que explora a camada de filtros do Spring Security em profundidade.

## Referências

- [Spring Framework — MVC Config: Interceptors](https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-config/interceptors.html)
- [Spring Framework — HandlerInterceptor (Interception)](https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-servlet/handlermapping-interceptor.html)
- [Spring Framework — Filters](https://docs.spring.io/spring-framework/reference/web/webmvc/filters.html)
- [Spring Framework — CORS](https://docs.spring.io/spring-framework/reference/web/webmvc-cors.html)
