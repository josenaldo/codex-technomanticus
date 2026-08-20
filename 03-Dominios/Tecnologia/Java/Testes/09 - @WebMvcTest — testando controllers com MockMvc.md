---
title: "@WebMvcTest — testando controllers com MockMvc"
created: 2026-06-11
updated: 2026-06-11
type: concept
progress: backlog
status: seedling
publish: true
fase: Adepto
tags:
  - java
  - testes
  - adepto
  - spring-test
  - webmvctest
aliases:
  - "@WebMvcTest"
  - "MockMvc"
---

# @WebMvcTest — testando controllers com MockMvc

> [!abstract] TL;DR
> `@WebMvcTest` carrega **só a camada web** (controllers, `@ControllerAdvice`, converters, filters) e mocka o resto da aplicação. O `MockMvc` dispara requests **sem subir servidor** — direto no `DispatcherServlet`, em memória — e assere status HTTP e corpo JSON via `jsonPath`. É o *slice* certo pra testar controllers isoladamente: rápido, focado, sem banco nem rede.

## O que é

`@WebMvcTest` é um **slice de teste** do Spring Boot que auto-configura apenas a infraestrutura do Spring MVC. Em vez de subir o `ApplicationContext` inteiro (como faria `@SpringBootTest`), ele monta um contexto mínimo contendo só os beans da camada web — o suficiente pra que um controller responda a um request.

Junto com ele vem o `MockMvc`, já `@Autowired`-ável: um cliente que simula requisições HTTP **sem container servlet real**. O request entra pelo `DispatcherServlet` em memória, percorre o pipeline MVC normal (handler mapping, validação, serialização) e devolve a resposta — tudo sem abrir porta TCP.

A forma típica é declarar o controller sob teste explicitamente:

```java
@WebMvcTest(OrderController.class)
```

Isso restringe o slice a esse controller (mais os componentes web globais), tornando o teste rápido e previsível.

> [!info] O pipeline MVC em si é território do Galho 9
> O *como* o `DispatcherServlet` resolve handlers, despacha exceções e serializa o corpo está descrito em [[03-Dominios/Tecnologia/Java/Web e APIs REST/06 - O pipeline do DispatcherServlet|O pipeline do DispatcherServlet]]. Aqui o foco é **testar** esse pipeline, não reexplicá-lo.

## Por que importa

Testar controller subindo a aplicação inteira é caro e frágil: você acopla o teste ao banco, à segurança, a serviços externos. Um bug num repository derruba o teste do controller, e você perde a localização da falha.

`@WebMvcTest` corta isso. Ele isola a **responsabilidade do controller**: receber um request, validar a entrada, delegar pra um service (mockado) e traduzir o resultado em status HTTP + corpo. É exatamente o contrato que o controller deve cumprir — nem mais, nem menos.

O ganho prático é triplo:

- **Velocidade** — contexto mínimo, sem JPA, sem datasource, sem auto-config pesada. Testes de controller rodam em milissegundos.
- **Foco** — quando o teste falha, o problema está no controller (ou no advice/converter), não em camadas abaixo.
- **Cobertura do contrato HTTP** — você assere os códigos de status (200, 404, 422) e o shape do JSON, que é o que o cliente da API enxerga.

## Como funciona

### `@WebMvcTest` carrega só a web layer (e o que NÃO carrega)

O slice escaneia e instancia **apenas** os componentes da camada web:

- `@Controller` / `@RestController`
- `@ControllerAdvice` (o tratamento de exceções global)
- `Converter` e `GenericConverter`
- `Filter` e `HandlerInterceptor`
- `WebMvcConfigurer` e `HandlerMethodArgumentResolver`
- componentes Jackson de (de)serialização

E **não** carrega o resto da aplicação:

- `@Service`
- `@Repository`
- `@Component` comuns
- `@ConfigurationProperties` (a menos que incluído explicitamente)

Ou seja: o controller existe, mas as dependências dele (services) **não estão no contexto**. Se você não mockar, o contexto falha em subir por bean faltante. Esse é o ponto-chave do slice — ele força você a isolar.

### MockMvc: perform + andExpect (status / jsonPath)

O `MockMvc` processa o request em memória e expõe uma API fluente de asserção:

```java
mockMvc.perform(get("/orders/1"))
    .andExpect(status().isOk())
    .andExpect(jsonPath("$.id").value(1))
    .andExpect(jsonPath("$.status").value("CONFIRMED"));
```

- `perform(...)` dispara o request (`get`, `post`, `put`, `delete` vêm de `MockMvcRequestBuilders`).
- `andExpect(status().isOk())` assere o código HTTP (`isNotFound()` → 404, `isUnprocessableEntity()` → 422, `isCreated()` → 201).
- `andExpect(jsonPath("$.campo").value(...))` navega o JSON da resposta e compara valores. `$` é a raiz; `$.items[0].id` desce em listas.

Como não há servidor real, não há latência de rede nem porta aberta — o request atravessa o `DispatcherServlet` direto.

### Mockar o service com `@MockitoBean`

A dependência do controller entra no contexto como **mock do Mockito**, via `@MockitoBean` (a anotação do Spring Framework que substituiu `@MockBean`):

```java
@MockitoBean
OrderService orderService;
```

O Spring registra esse mock no contexto de teste no lugar do bean real. Você programa o comportamento com a API normal do Mockito:

```java
given(orderService.findById(1L))
    .willReturn(new Order(1L, "CONFIRMED"));
```

Assim o controller recebe respostas determinísticas do service, e o teste fica responsável só pelo que o controller faz com elas.

### Testar 200 / 404 / 422 / validação

Os quatro cenários que um teste de controller costuma cobrir:

- **200 OK** — caminho feliz: service devolve a entidade, controller serializa, status 200.
- **404 Not Found** — service lança `OrderNotFoundException`; o `@ControllerAdvice` (que o slice carrega) traduz pra 404.
- **422 Unprocessable Entity** — corpo da requisição viola `@Valid`; o advice traduz a `MethodArgumentNotValidException` em 422 com a lista de erros.
- **Validação** — assere que um body inválido **não** chega ao service (verificável com `verifyNoInteractions(orderService)`).

Note que 404 e 422 só funcionam porque o `@ControllerAdvice` está no slice. É por isso que `@WebMvcTest` o carrega: o tratamento de exceção faz parte do contrato HTTP do controller.

## Na prática

```java
import static org.mockito.BDDMockito.given;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@WebMvcTest(OrderController.class)
class OrderControllerTest {

    @Autowired
    MockMvc mockMvc;

    @MockitoBean
    OrderService orderService;

    @Test
    void getReturns200AndBody() throws Exception {
        given(orderService.findById(1L))
            .willReturn(new Order(1L, "CONFIRMED"));

        mockMvc.perform(get("/orders/1"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.id").value(1))
            .andExpect(jsonPath("$.status").value("CONFIRMED"));
    }

    @Test
    void getUnknownReturns404() throws Exception {
        given(orderService.findById(99L))
            .willThrow(new OrderNotFoundException(99L));

        mockMvc.perform(get("/orders/99"))
            .andExpect(status().isNotFound());
    }

    @Test
    void postInvalidBodyReturns422() throws Exception {
        String invalidBody = """
            { "customer": "" }
            """;

        mockMvc.perform(post("/orders")
                .contentType(MediaType.APPLICATION_JSON)
                .content(invalidBody))
            .andExpect(status().isUnprocessableEntity());

        verifyNoInteractions(orderService);
    }
}
```

O teste descreve só o contrato HTTP: dado o que o service retorna (ou lança), qual status e qual JSON o controller produz. Nada de banco, nada de servidor.

> [!tip] De onde vêm `OrderController` e `OrderService`
> O `@RestController` e seus mapeamentos (`@GetMapping`, `@PostMapping`, `@PathVariable`, `@RequestBody @Valid`) são do Galho 9 — veja [[03-Dominios/Tecnologia/Java/Web e APIs REST/02 - @RestController e os mapeamentos|@RestController e os mapeamentos]]. O `@WebMvcTest` apenas **exercita** esses mapeamentos.

## Armadilhas

### (1) Esperar que o service/repository reais carreguem

O erro mais comum: declarar `@WebMvcTest(OrderController.class)` e supor que o `OrderService` real (com seu `OrderRepository`, datasource etc.) vai estar disponível. Ele não vai — o slice **não carrega** `@Service` nem `@Repository`.

```java
@WebMvcTest(OrderController.class)
class OrderControllerTest {
    @Autowired MockMvc mockMvc;
    // sem mock do OrderService → contexto falha:
    // "No qualifying bean of type OrderService"
}
```

**Fix:** declare a dependência como mock e programe-a:

```java
@MockitoBean
OrderService orderService;
// given(orderService.findById(1L)).willReturn(...);
```

### (2) Testar serialização JSON complexa aqui em vez de `@JsonTest`

Tentar validar todas as regras de (de)serialização — formatos de data, campos ignorados, polimorfismo Jackson — dentro do `@WebMvcTest`. Isso mistura responsabilidades: o foco do slice web é o **controller** (roteamento, status, validação), não o motor de serialização.

```java
// Anti-padrão: dezenas de jsonPath assertando cada nuance do mapeamento JSON
.andExpect(jsonPath("$.createdAt").value("2026-06-11T00:00:00Z"))
.andExpect(jsonPath("$.internalNote").doesNotExist())
// ... 20 linhas validando o serializer, não o controller
```

**Fix:** valide o **shape essencial** no `@WebMvcTest` (1-2 campos-chave) e mova os testes finos do serializer pra um slice dedicado de JSON (`@JsonTest`), que carrega só o `ObjectMapper` configurado.

### (3) Confundir `MockMvc` com teste de integração com servidor (porta)

`MockMvc` **não sobe servidor** — não há porta, não há cliente HTTP real, não há `RestTemplate`/`WebTestClient` batendo na rede. Tratar um teste de `@WebMvcTest` como se fosse end-to-end leva a expectativas erradas (ex.: achar que filtros de container, TLS ou o connector estão no caminho).

```java
// Errado: isto NÃO é o que @WebMvcTest faz —
// não existe servidor real escutando numa porta aqui.
```

**Fix:** quando o objetivo for testar a stack **real** com servidor de verdade, use `@SpringBootTest(webEnvironment = RANDOM_PORT)` com `WebTestClient`/`TestRestTemplate` — veja [[03-Dominios/Tecnologia/Java/Testes/12 - Testes de integração ponta a ponta|Testes de integração ponta a ponta]]. `@WebMvcTest` + `MockMvc` é deliberadamente **in-memory**.

## Em entrevista

### Frase pronta (inglês)

> `@WebMvcTest` is a Spring Boot test slice that loads only the web layer — controllers, `@ControllerAdvice`, converters and filters — while leaving services and repositories out of the context. I autowire a `MockMvc` instance to drive requests straight through the `DispatcherServlet` in memory, with no servlet container or open port, and mock the controller's service dependency with `@MockitoBean`. From there I assert the HTTP contract: `status().isOk()` for the happy path, `isNotFound()` and `isUnprocessableEntity()` for error cases handled by the advice, and `jsonPath` matchers for the response body. It keeps controller tests fast and focused, so when one fails I know the bug is in the web layer rather than somewhere underneath.

### Vocabulário

| Termo (EN) | Significado |
| --- | --- |
| test slice | fatia de contexto que carrega só parte da aplicação |
| web layer | camada web: controllers, advice, converters, filters |
| in-memory request | request processado sem container/porta, direto no dispatcher |
| mock bean | dependência substituída por mock no contexto (`@MockitoBean`) |
| status matcher | asserção sobre o código HTTP (`status().isOk()`) |
| JSON path assertion | asserção que navega o corpo JSON (`jsonPath(...)`) |
| controller advice | tratamento global de exceções (`@ControllerAdvice`) |
| HTTP contract | o acordo de status/corpo que a API expõe ao cliente |

## Veja também

- [[03-Dominios/Tecnologia/Java/Testes/08 - Spring Boot Test e os slices — o contexto de teste|Spring Boot Test e os slices]]
- [[03-Dominios/Tecnologia/Java/Testes/12 - Testes de integração ponta a ponta|Testes de integração ponta a ponta]]
- [[03-Dominios/Tecnologia/Java/Testes/13 - Testando a segurança|Testando a segurança]]
- [[03-Dominios/Tecnologia/Java/Web e APIs REST/02 - @RestController e os mapeamentos|@RestController e os mapeamentos]]
- [[03-Dominios/Tecnologia/Java/Web e APIs REST/06 - O pipeline do DispatcherServlet|O pipeline do DispatcherServlet]]
- [[03-Dominios/Tecnologia/Java/Web e APIs REST/09 - Tratamento de exceções com @ControllerAdvice|Tratamento de exceções com @ControllerAdvice]]
- [[03-Dominios/Tecnologia/Java/Testes/index|Testes (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java]]

## Referências

- Spring Boot Reference — Testing: Spring Boot Applications (`@WebMvcTest`): https://docs.spring.io/spring-boot/reference/testing/spring-boot-applications.html
- Spring Framework Reference — MockMvc: https://docs.spring.io/spring-framework/reference/testing/mockmvc/
