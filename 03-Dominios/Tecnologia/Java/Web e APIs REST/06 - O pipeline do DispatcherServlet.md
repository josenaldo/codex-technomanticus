---
title: "O pipeline do DispatcherServlet"
created: 2026-06-08
updated: 2026-06-08
type: concept
progress: backlog
status: seedling
publish: true
fase: adepto
tags:
  - java
  - web
  - adepto
  - spring-mvc
aliases:
  - "DispatcherServlet pipeline"
---

# O pipeline do DispatcherServlet

> [!abstract] TL;DR
> Toda request HTTP que chega numa aplicação Spring MVC passa pelo **DispatcherServlet** — um único servlet que age como *front controller* e orquestra a engrenagem: `HandlerMapping` descobre qual método do controller responde, o `HandlerAdapter` invoca esse método, `HandlerMethodArgumentResolver` constrói os argumentos, e o `HttpMessageConverter` serializa o retorno pro corpo da resposta. Entender essa engrenagem é o que separa "eu uso `@GetMapping`" de "eu sei exatamente o que acontece quando o request chega". É também onde se encaixam interceptors, conversão de exceção e a regra de que o servlet é *singleton* multi-thread.

## O que é

O `DispatcherServlet` é a peça central do Spring MVC. Ele é um servlet de verdade — implementa a `jakarta.servlet.http.HttpServlet` — registrado no container web (Tomcat embarcado, no Boot) tipicamente mapeado para `/`. A partir do momento em que o container entrega um request a ele, o DispatcherServlet assume e executa um algoritmo fixo de despacho, delegando cada etapa para *beans especiais* descobertos no `ApplicationContext`.

A esse padrão dá-se o nome de **front controller**: em vez de cada recurso ter seu próprio servlet, um único ponto de entrada centraliza a lógica compartilhada (resolução de handler, conversão de dados, tratamento de erro, internacionalização) e delega o que é específico de cada rota. O coração do despacho vive no método `doDispatch(...)` da classe `DispatcherServlet`.

Os beans especiais que ele consulta, na ordem de relevância para o caminho de uma API REST, são:

- **`HandlerMapping`** — descobre qual handler responde à URL/método (impl. padrão: `RequestMappingHandlerMapping`).
- **`HandlerAdapter`** — sabe *como* invocar aquele handler (impl. padrão: `RequestMappingHandlerAdapter`).
- **`HandlerExceptionResolver`** — converte exceções lançadas durante o despacho em respostas.
- **`ViewResolver`** — resolve nomes lógicos de view (irrelevante para `@RestController`, que serializa direto).
- **`LocaleResolver`**, **`MultipartResolver`**, **`FlashMapManager`** — locale, upload multipart e flash attributes em redirects.

## Por que importa

No dia a dia você anota `@GetMapping("/orders/{id}")`, devolve um `Order`, e mágica: vira JSON. Essa abstração é ótima — até o dia em que algo dá errado e você precisa saber *onde* no pipeline o problema mora.

- O JSON saiu vazio? Provavelmente é o `HttpMessageConverter` (getters faltando, módulo Jackson ausente).
- O `@PathVariable` veio `null`? É um `HandlerMethodArgumentResolver` que não conseguiu fazer o binding.
- O 404 veio antes de chegar no controller? O `HandlerMapping` não encontrou rota.
- O header que você setou num interceptor não apareceu? `postHandle` rodou **tarde demais** para respostas `@ResponseBody`.

Saber a sequência transforma debugging por tentativa-e-erro em diagnóstico dirigido. Em entrevista, é a diferença entre "uso Spring" e "entendo Spring". E quando você precisar de um *cross-cutting concern* (auditoria, métricas, correlação de logs), saber a diferença entre **filter** (antes do dispatcher) e **interceptor** (dentro do pipeline) decide onde o código vai morar.

## Como funciona

### O caminho do request (doDispatch): mapping → adapter → handler → converter

Quando o container chama o DispatcherServlet, o `doDispatch` executa, em ordem:

1. **HandlerMapping** resolve o request num `HandlerExecutionChain` — o handler (o método do controller) mais a lista de interceptors aplicáveis.
2. **`preHandle`** de cada interceptor é chamado, na ordem de registro. Se algum retornar `false`, o despacho para ali e o handler nunca é invocado.
3. **HandlerAdapter** é selecionado e invoca o handler. Aqui, antes do método rodar, os `HandlerMethodArgumentResolver` constroem cada argumento (`@PathVariable`, `@RequestBody`, etc.).
4. **O método do controller** roda e devolve um valor.
5. **HandlerMethodReturnValueHandler** processa o retorno. Para `@ResponseBody`/`ResponseEntity`, um `HttpMessageConverter` serializa o objeto e **escreve o corpo da resposta**.
6. **`postHandle`** de cada interceptor é chamado, em ordem inversa.
7. **Renderização da view** (só quando há view a renderizar — não é o caso de API REST com `@ResponseBody`).
8. **`afterCompletion`** de cada interceptor é chamado, em ordem inversa, *sempre* — inclusive quando houve exceção.

Se qualquer etapa lançar exceção, o controle desvia para o `HandlerExceptionResolver` (ver mais abaixo).

```text
                    container web (Tomcat)
                            │  request HTTP
                            ▼
                ┌───────────────────────────┐
                │      DispatcherServlet      │
                │        (doDispatch)         │
                └───────────────────────────┘
                            │
      (1) HandlerMapping ───┤  resolve URL+método → HandlerExecutionChain
                            │     (handler + interceptors)
                            ▼
      (2) interceptor.preHandle() ── false ──► para aqui, resposta já decidida
                            │ true
                            ▼
      (3) HandlerAdapter ───┤  vai invocar o método
                            │
            ArgumentResolvers: monta args (@PathVariable, @RequestBody…)
                            │
                            ▼
      (4)            método do @Controller
                            │ devolve objeto / ResponseEntity
                            ▼
      (5) ReturnValueHandler → HttpMessageConverter (objeto → JSON no corpo)
                            │
                            ▼
      (6) interceptor.postHandle()   (ordem inversa)
                            │
                            ▼
      (7) renderização de view  (só MVC clássico; API REST pula)
                            │
                            ▼
      (8) interceptor.afterCompletion()  (sempre, mesmo com erro)
                            │
                            ▼
                      resposta HTTP

   * exceção em qualquer ponto ► HandlerExceptionResolver
```

### HandlerMapping (RequestMappingHandlerMapping) e HandlerAdapter

São as duas peças que respondem à pergunta "qual código roda, e como?".

O **`HandlerMapping`** responde *qual*. Sua implementação padrão num app Boot é a **`RequestMappingHandlerMapping`**, que na inicialização varre todos os beans `@Controller`/`@RestController`, lê as anotações `@RequestMapping` (e derivadas como `@GetMapping`) e monta uma tabela de `RequestMappingInfo` → método. Em runtime, ela casa o request (path, método HTTP, headers, `Accept`/`Content-Type`) contra essa tabela e devolve um `HandlerExecutionChain`. Não achou rota? Vira 404 (`NoHandlerFoundException` / resposta padrão).

O **`HandlerAdapter`** responde *como invocar*. Existe porque "handler" no Spring é um conceito genérico — poderia ser um método anotado, um `Controller` antigo baseado em interface, uma function. Cada tipo de handler tem um adapter que sabe chamá-lo, blindando o DispatcherServlet desses detalhes. Para métodos anotados, o adapter é a **`RequestMappingHandlerAdapter`**, que orquestra os argument resolvers, invoca o método via reflection e despacha o retorno aos return value handlers.

> [!info] Por que dois beans e não um só?
> Separar *descobrir* (mapping) de *invocar* (adapter) é uma aplicação do princípio de responsabilidade única. Permite, por exemplo, ter mapeamentos por URL explícita (`SimpleUrlHandlerMapping`) e por anotação convivendo, cada um com a estratégia de invocação adequada.

### HandlerMethodArgumentResolver e ReturnValueHandler (como @RequestBody/@PathVariable viram args)

Quando a `RequestMappingHandlerAdapter` vai invocar `createOrder(@PathVariable Long id, @RequestBody OrderRequest body)`, ela precisa produzir os dois argumentos *antes* de chamar o método. É aí que entram os **`HandlerMethodArgumentResolver`**.

Cada resolver declara, via `supportsParameter(...)`, que tipo de parâmetro ele sabe construir. O adapter percorre os parâmetros do método e, para cada um, pergunta a cada resolver "você cuida deste?". Exemplos:

- `PathVariableMethodArgumentResolver` → lê `@PathVariable` da URI template, converte a string para o tipo do parâmetro.
- `RequestResponseBodyMethodProcessor` → lê `@RequestBody`, escolhe um `HttpMessageConverter` compatível com o `Content-Type` do request e **desserializa** o corpo no objeto.
- `RequestParamMethodArgumentResolver` → `@RequestParam`.
- Resolvers para `HttpServletRequest`, `Model`, `@RequestHeader`, etc.

Simetricamente, depois que o método retorna, os **`HandlerMethodReturnValueHandler`** processam o valor de retorno. O `RequestResponseBodyMethodProcessor` também atua aqui: para um retorno anotado com `@ResponseBody` (implícito em `@RestController`), ele escolhe um `HttpMessageConverter` com base no `Accept` do cliente e **serializa** o objeto no corpo da resposta.

Ou seja: `@RequestBody` e `@ResponseBody` são os dois lados da mesma moeda — desserialização e serialização —, ambos delegados a `HttpMessageConverter` (tipicamente `MappingJackson2HttpMessageConverter` para JSON). O argument resolver/return handler é o *encaixe* desse conversor no pipeline.

### Tratamento de exceção no pipeline (HandlerExceptionResolver — liga à nota 09)

Se o handler (ou qualquer etapa do despacho) lança uma exceção, o `doDispatch` não a deixa vazar crua pro container. Em vez disso, consulta a cadeia de **`HandlerExceptionResolver`** registrados, perguntando a cada um se sabe converter aquela exceção numa resposta.

Num app Boot, o resolver mais importante é o `ExceptionHandlerExceptionResolver`, que é o motor por trás de `@ExceptionHandler` e `@ControllerAdvice`. Ele localiza um método tratador compatível com o tipo da exceção e o invoca — passando o retorno (muitas vezes um `ResponseEntity`) de volta pelo mesmo mecanismo de return value handler / message converter.

Outros resolvers da cadeia: `ResponseStatusExceptionResolver` (para `@ResponseStatus` e `ResponseStatusException`) e `DefaultHandlerExceptionResolver` (mapeia exceções padrão do Spring MVC para status HTTP, p.ex. `MethodArgumentNotValidException` → 400).

Detalhe importante do fluxo: mesmo no caminho de erro, o `afterCompletion` de cada interceptor é chamado — recebendo a exceção como argumento. O tratamento aprofundado (`@ControllerAdvice`, `ProblemDetail`/RFC 9457, `@ResponseStatus`) é o tema da nota 09 deste galho.

## Na prática

Um `HandlerInterceptor` simples deixa visível *onde* cada hook entra no pipeline. Os três métodos vivem em `org.springframework.web.servlet.HandlerInterceptor` e marcam pontos distintos do `doDispatch`:

```java
package com.example.web;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.lang.Nullable;
import org.springframework.web.servlet.HandlerInterceptor;
import org.springframework.web.servlet.ModelAndView;

public class TimingInterceptor implements HandlerInterceptor {

    private static final String START_ATTR = "requestStartNanos";

    // (2) ANTES do handler. Retornar false aborta o despacho:
    // o método do controller NUNCA é chamado.
    @Override
    public boolean preHandle(HttpServletRequest request,
                             HttpServletResponse response,
                             Object handler) {
        request.setAttribute(START_ATTR, System.nanoTime());
        return true; // segue o pipeline
    }

    // (6) DEPOIS do handler, ANTES de renderizar a view.
    // ATENÇÃO: para respostas @ResponseBody/ResponseEntity, o corpo já foi
    // escrito e a resposta possivelmente já commitada pelo HandlerAdapter —
    // setar header aqui pode não ter efeito. Use ResponseBodyAdvice nesse caso.
    @Override
    public void postHandle(HttpServletRequest request,
                           HttpServletResponse response,
                           Object handler,
                           @Nullable ModelAndView modelAndView) {
        // Em API REST, modelAndView costuma ser null (não há view).
    }

    // (8) SEMPRE roda no fim — inclusive quando houve exceção (vem em 'ex').
    // Lugar certo para cleanup, métricas e logging de duração.
    @Override
    public void afterCompletion(HttpServletRequest request,
                                HttpServletResponse response,
                                Object handler,
                                @Nullable Exception ex) {
        Long start = (Long) request.getAttribute(START_ATTR);
        if (start != null) {
            long elapsedMs = (System.nanoTime() - start) / 1_000_000;
            // log.info("{} {} levou {} ms (erro={})",
            //          request.getMethod(), request.getRequestURI(), elapsedMs, ex != null);
        }
    }
}
```

Registro via `WebMvcConfigurer` (a forma recomendada):

```java
package com.example.web;

import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class WebConfig implements WebMvcConfigurer {

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(new TimingInterceptor())
                .addPathPatterns("/api/**");
    }
}
```

A numeração nos comentários `(2)`, `(6)`, `(8)` casa com o diagrama do `doDispatch` lá em cima — útil para fixar onde cada hook dispara.

## Armadilhas

### (1) Achar que o controller é "chamado direto"

A anotação `@GetMapping` cria a ilusão de que o container "chama seu método". Na verdade, há a engrenagem inteira no meio: o request bate no DispatcherServlet, que consulta o HandlerMapping, escolhe um HandlerAdapter, monta argumentos via resolvers e só então invoca o método por reflection.

Por que dói: quando o JSON sai errado ou o binding falha, quem pensa "é só meu método" fica perdido — o defeito quase sempre está numa peça do pipeline, não no corpo do método.

```text
ILUSÃO:   request ──────────────► seu @GetMapping
REALIDADE: request ► DispatcherServlet ► HandlerMapping ► HandlerAdapter
                   ► ArgumentResolvers ► seu método ► ReturnValueHandler
                   ► HttpMessageConverter ► resposta
```

Fix: ao depurar, pergunte *em qual etapa* o problema mora. Status 404 antes de logar nada no controller → HandlerMapping. `@RequestBody` nulo ou exceção de parse → argument resolver + message converter. JSON vazio → message converter (getters/Jackson). Esse mapa torna o debugging dirigido.

### (2) Confundir filter (antes do dispatcher) com interceptor (dentro do pipeline)

`jakarta.servlet.Filter` e `HandlerInterceptor` parecem fazer a mesma coisa, mas vivem em camadas diferentes. O **filter** é da Servlet API — roda no container, *antes* de o request chegar ao DispatcherServlet, e envolve a chamada inteira (incluindo a escolha de handler). O **interceptor** é do Spring MVC — roda *dentro* do `doDispatch`, *depois* que o handler já foi resolvido, então tem acesso ao `handler` (o método do controller).

Por que dói: você tenta, num interceptor, fazer algo que exige interceptar requests que nem chegam a virar um handler (p.ex. CORS preflight, segurança de borda), e não funciona — porque nesse ponto o handler já foi (ou não) resolvido.

```text
container ─► [ Filter chain ] ─► DispatcherServlet ─► [ Interceptor chain ] ─► handler
            └ Servlet API ┘                          └────── Spring MVC ──────┘
            (sem saber qual                          (já sabe o handler;
             handler responde)                        tem ModelAndView no postHandle)
```

Fix: precisa atuar sobre *toda* request bruta, antes de qualquer resolução de rota (segurança, CORS, troca de wrapper de request/response, cache de body)? Use **Filter**. Precisa de lógica acoplada ao handler escolhido, com acesso ao `Object handler` e ao `ModelAndView` (logging de controller, métricas por rota)? Use **Interceptor**. A nota 11 detalha o contraste.

### (3) Assumir uma instância de controller por request (o servlet é singleton multi-thread)

O DispatcherServlet é instanciado uma vez. Os beans `@Controller` também são singletons por padrão. Múltiplas threads do pool do Tomcat atravessam o *mesmo* objeto controller simultaneamente. Logo, **campo de instância mutável em controller é estado compartilhado entre requests** — receita para race condition.

Por que dói: o bug some em teste single-thread e aparece só sob carga, com dados de um request vazando para outro de forma intermitente — o pior tipo de defeito para reproduzir.

```java
// ERRADO: campo mutável compartilhado entre todas as threads/requests
@RestController
public class OrderController {
    private Long lastOrderId; // estado de instância — corrompido sob concorrência

    @PostMapping("/orders")
    public OrderResponse create(@RequestBody OrderRequest req) {
        this.lastOrderId = persist(req); // duas threads sobrescrevem uma à outra
        return new OrderResponse(this.lastOrderId); // pode devolver o id de OUTRO request
    }
}
```

Fix: mantenha controllers *stateless*. Tudo que é específico do request vive em variáveis locais (que são por-thread, na pilha) ou nos parâmetros do método. Dependências (services, repositories) são injetadas como campos `final` — imutáveis e seguros para compartilhar.

```java
// CERTO: sem estado mutável; só dependências final e variáveis locais
@RestController
public class OrderController {
    private final OrderService orderService; // imutável, thread-safe

    public OrderController(OrderService orderService) {
        this.orderService = orderService;
    }

    @PostMapping("/orders")
    public OrderResponse create(@RequestBody OrderRequest req) {
        Long id = orderService.create(req); // variável local: isolada por thread
        return new OrderResponse(id);
    }
}
```

## Em entrevista

### Frase pronta (inglês)

> Spring MVC is built around the DispatcherServlet, which acts as a front controller: every HTTP request goes through this single servlet, and it orchestrates a fixed dispatch algorithm. First a HandlerMapping — typically RequestMappingHandlerMapping — resolves the request to a controller method and its interceptor chain; then a HandlerAdapter, usually RequestMappingHandlerAdapter, invokes that method, using argument resolvers to build parameters like @PathVariable and @RequestBody, and return-value handlers plus HttpMessageConverters to serialize the result into the response body. Because the DispatcherServlet and the controllers are singletons shared across the thread pool, I keep controllers stateless and put any request-specific state in local variables; and I'm careful to distinguish servlet filters, which run before the dispatcher, from Spring interceptors, which run inside the pipeline once the handler is known.

### Vocabulário

| Termo PT | Termo EN |
| --- | --- |
| front controller (controlador frontal) | front controller |
| despacho de requisição | request dispatch |
| mapeamento de handler | handler mapping |
| adaptador de handler | handler adapter |
| resolvedor de argumentos | argument resolver |
| conversor de mensagem HTTP | HTTP message converter |
| interceptador | interceptor |
| filtro (Servlet) | servlet filter |
| singleton multi-thread | multi-threaded singleton |
| resolvedor de exceção | exception resolver |

## Veja também

- [[03-Dominios/Tecnologia/Java/Web e APIs REST/01 - O que é Spring MVC — a camada web sobre o container|O que é Spring MVC]]
- [[03-Dominios/Tecnologia/Java/Web e APIs REST/11 - Interceptors vs Filters|Interceptors vs Filters]]
- [[03-Dominios/Tecnologia/Java/Jakarta EE/03 - Servlet API — o alicerce HTTP|Servlet API]] (a spec por baixo — o DispatcherServlet É um servlet, singleton multi-thread)
- [[03-Dominios/Tecnologia/Java/Spring Core e Boot/16 - SpringApplication e o embedded server|SpringApplication e o embedded server]] (quem registra o DispatcherServlet)
- [[03-Dominios/Tecnologia/Java/Web e APIs REST/index|Web e APIs REST]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- Verbetes: [[03-Dominios/Tecnologia/Java/Dicionário de Java#DispatcherServlet|DispatcherServlet]], [[03-Dominios/Tecnologia/Java/Dicionário de Java#HandlerMapping|HandlerMapping]], [[03-Dominios/Tecnologia/Java/Dicionário de Java#HandlerAdapter|HandlerAdapter]], [[03-Dominios/Tecnologia/Java/Dicionário de Java#front controller|front controller]]

## Referências

- Spring Framework Reference — Web on Servlet Stack, DispatcherServlet: https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-servlet.html
- Spring Framework Reference — Special Bean Types: https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-servlet/special-bean-types.html
- Spring Framework Reference — Interception (HandlerInterceptor): https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-servlet/handlermapping-interceptor.html
- Spring Framework Reference — Exceptions / HandlerExceptionResolver: https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-servlet/exceptionhandlers.html
