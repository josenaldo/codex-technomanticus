---
title: "Spec — Galho 9 da trilha Java Senior (Web e APIs REST)"
date: 2026-06-08
author: Josenaldo
status: draft
type: spec
publish: false
---

# Spec — Galho 9 da trilha Java Senior (Web e APIs REST)

## 1. Contexto e motivação

Este é o **nono galho** da trilha Java Senior (roadmap em `docs/superpowers/specs/2026-06-02-java-senior-roadmap-design.md`, §5, bloco "Fundamentos enterprise e Spring"). Pressupõe leitura do roadmap, que estabelece topologia flat, esquema de 3 fases, padrões editoriais e política de poda. Os Galhos 1 (Linguagem), 2 (Collections/Streams), 3 (JVM), 4 (Concorrência), 5 (Swing), 6 (JavaFX), **7 (Jakarta EE)** e **8 (Spring Core e Boot)** já fecharam em `main` — seus artefatos são o **template de padrão e qualidade** deste galho. O **Galho 8 é a dependência direta** (este galho roda sobre o container) e o **Galho 7 é a dependência conceitual** (este galho implementa as specs HTTP da plataforma).

**Galho HÍBRIDO: REFATOR (poda parcial) + PESQUISA.** Como o Galho 8, tem duas naturezas:

- **Parte REFATOR (poda parcial):** o tronco `Backend/Spring Boot.md` (1090 linhas após o Galho 8, `publish: false`, `status: evergreen`) tem **uma única seção core deste galho** — `## Spring MVC pipeline` (linhas ~221-371: O pipeline, DispatcherServlet, HandlerMapping, HandlerAdapter, HttpMessageConverter, Interceptors vs Filters, Exception Handling). O Galho 8 a **deixou intacta de propósito**, esperando este galho. É matéria-prima a refinar e depois **podar** (callout + wikilinks). A seção contém fabricação (`PatientController`/`PatientNotFoundException`, linhas ~332-349) que **some com a poda** (absorvida pelo callout — contraexemplo, nunca copiar pras notas).
- **Parte PESQUISA:** o tronco é **mudo** sobre OpenAPI/Swagger, HATEOAS, versionamento de API, Problem Details como formato (só cita), content negotiation a fundo e **clientes HTTP** (`RestClient`/`WebClient`/`RestTemplate` **não aparecem no tronco** — grep vazio). Essas notas **nascem de docs oficiais** (`docs.spring.io/spring-framework/reference/web/`, `docs.spring.io/spring-boot/`, `springdoc.org`) verificadas via WebFetch.

**A fronteira-assinatura é DUPLA.** O Galho 7 plantou ganchos mostrando que o Spring MVC implementa as specs HTTP da plataforma; o Galho 8 plantou ganchos mostrando que a camada web roda sobre o container. Este galho **linka de volta aos dois**, sem re-explicar nenhum:

- **Galho 7 (specs que o Spring MVC implementa/abstrai):** o `DispatcherServlet` **é** um servlet → Servlet API ([[03-Dominios/Java/Jakarta EE/03 - Servlet API — o alicerce HTTP|Servlet API]]); `@RestController` é **o caminho do Spring** pro mesmo problema do JAX-RS ([[03-Dominios/Java/Jakarta EE/07 - JAX-RS — REST declarativo|JAX-RS]]); `@Valid` no controller aciona **a spec Bean Validation** ([[03-Dominios/Java/Jakarta EE/08 - Bean Validation|Bean Validation]]); `HandlerInterceptor` vs **Servlet Filter** (a spec).
- **Galho 8 (o container sob a camada web):** controllers e `@ControllerAdvice` **são beans** ([[03-Dominios/Java/Spring Core e Boot/03 - Beans e estereótipos — @Component, @Service, @Repository, @Controller|Beans e estereótipos]]); o `@RestControllerAdvice`/`@ExceptionHandler` usam **o mecanismo AOP/proxy** ([[03-Dominios/Java/Spring Core e Boot/09 - AOP e proxies no Spring|AOP e proxies]]); o `DispatcherServlet` sobe no `ApplicationContext` e o embedded server o registra ([[03-Dominios/Java/Spring Core e Boot/16 - SpringApplication e o embedded server|SpringApplication e o embedded server]]); `@Validated` é a porta da config ([[03-Dominios/Java/Spring Core e Boot/12 - Configuração e profiles|Configuração e profiles]]).

O Galho 7 e o Galho 8 deixaram **ganchos "Galho 9 (planejado)"** em texto esperando exatamente esses wikilinks (dívida reversa — §3.6). Este galho **quita** essa dívida.

Web e APIs REST é a **camada web sobre o container do Galho 8**: como um HTTP request vira uma resposta no Spring MVC (front controller, pipeline, content negotiation), como se escreve um REST controller (mapeamentos, binding de request, `ResponseEntity`, serialização JSON), como se valida na borda e se trata erro (Problem Details / RFC 9457), como se documenta (OpenAPI), versiona e consome (RestClient) uma API production-grade. Depende dos Galhos 8 (container) e 7 (specs).

## 2. Objetivo

Produzir, em uma sessão de execução dedicada, **16 notas atômicas + 1 MOC do galho + expansão do Dicionário de Java + ativação do MOC central + poda parcial do tronco (seção MVC) + quitação da dívida reversa**, em `03-Dominios/Java/Web e APIs REST/` e `03-Dominios/Java/`, todas `publish: true`, em PT-BR, distribuídas em 3 fases (**5 Iniciado + 7 Adepto + 4 Magus**).

Ao terminar o galho, o leitor deve conseguir:

- **Explicar em inglês** como um request HTTP atravessa o Spring MVC (filter → `DispatcherServlet` → `HandlerMapping`/`HandlerAdapter` → controller → `HttpMessageConverter`), o que é content negotiation, como `@Valid` produz 400 automático, e como `@RestControllerAdvice` + `ProblemDetail` padronizam erro.
- **Reconhecer o que o Spring MVC implementa do Galho 7**: dado o `DispatcherServlet`/`@RestController`/`@Valid`/`HandlerInterceptor`, apontar a spec Jakarta correspondente (Servlet API, JAX-RS, Bean Validation, Servlet Filter) e a diferença de modelo (o caminho do Spring vs a spec portável).
- **Reconhecer o que a camada web deve ao container do Galho 8**: controllers são beans, `@ControllerAdvice` usa AOP/proxy, o `DispatcherServlet` sobe no contexto e é registrado pelo embedded server.
- **Projetar uma REST API production-grade**: status codes corretos, DTOs vs entidades, validação na borda, erro padronizado (RFC 9457), documentação (OpenAPI), estratégia de versionamento, e consumo de outras APIs com `RestClient`.
- **Diagnosticar armadilhas clássicas**: vazar entidade JPA no JSON, `@Valid` esquecido, 200-para-tudo, `@ExceptionHandler` que engole a stack, `RestTemplate` novo a cada request, content negotiation mal configurada.

A barra é "explicar o pipeline, reconhecer as specs por baixo e projetar uma API com critério" — não "escrever um `HandlerMethodArgumentResolver` de produção".

## 3. Saídas concretas

### 3.1. Notas (`03-Dominios/Java/Web e APIs REST/`)

Pasta **nova**, flat. 16 notas + 1 MOC (`index.md`, obrigatório pro folder-link do Quartz). Numeração global por galho (não reinicia por fase).

#### Iniciado (5 notas — vocabulário + modelo mental)

| # | Nota | Escopo nuclear |
|---|------|----------------|
| 01 | O que é Spring MVC — a camada web sobre o container *(opus)* | O padrão front controller; o `DispatcherServlet` como porta única (visão geral, mecânica fica na 06); Spring MVC = camada web do Spring Framework sobre o Servlet container; o que é REST nesse contexto. **A nota-assinatura da dupla fronteira.** Linka Servlet API do Galho 7 ("o `DispatcherServlet` é um servlet — a spec por baixo"), IoC do Galho 8 (controllers são beans), e JAX-RS do Galho 7 ("o outro caminho pro mesmo problema"). |
| 02 | @RestController e os mapeamentos | `@Controller` vs `@RestController` (= `@Controller` + `@ResponseBody`); `@RequestMapping` e os atalhos `@GetMapping`/`@PostMapping`/`@PutMapping`/`@DeleteMapping`/`@PatchMapping`; path patterns, `path`/`method`/`produces`/`consumes`. Linka Galho 8 (controller é bean/estereótipo) e JAX-RS do Galho 7 (resource methods — a spec). |
| 03 | Recebendo dados da request | `@PathVariable`, `@RequestParam` (defaults, `required`), `@RequestBody` (desserialização JSON), `@RequestHeader`, `@RequestPart`; binding de tipos; `Optional`/defaults. Linka JAX-RS do Galho 7 (`@PathParam`/`@QueryParam` — os params tipados da spec). |
| 04 | ResponseEntity e status codes | Montar a resposta: `ResponseEntity<T>` (status + headers + body), `@ResponseStatus`, status codes corretos (200/201/204/400/404/409/422/500), `Location` no 201, `ResponseEntity.created()`. Por que "200 pra tudo" é erro. |
| 05 | Serialização JSON com Jackson | `@ResponseBody` e o `HttpMessageConverter` padrão (`MappingJackson2HttpMessageConverter`); `ObjectMapper`; **DTO vs entidade** (não vazar entidade JPA → Galho 10); anotações Jackson (`@JsonProperty`, `@JsonIgnore`, `@JsonInclude`); datas (`JavaTimeModule`). Linka Galho 10 (entidade/JPA é lá; aqui só o DTO da borda). |

#### Adepto (7 notas — domínio operacional)

| # | Nota | Escopo nuclear |
|---|------|----------------|
| 06 | O pipeline do DispatcherServlet *(opus)* | A mecânica completa: `HandlerMapping` (`RequestMappingHandlerMapping`) → `HandlerInterceptor.preHandle` → `HandlerAdapter` → `HandlerMethodArgumentResolver` (resolve `@RequestBody`/`@PathVariable`/...) → método do controller → `HandlerMethodReturnValueHandler` → `HttpMessageConverter` → `postHandle`/`afterCompletion`. **A nota mais densa do galho.** Linka Servlet API do Galho 7 ("o `DispatcherServlet` É um servlet, registrado pelo container") e o `ApplicationContext`/embedded server do Galho 8. |
| 07 | Content negotiation | Como o Spring escolhe o formato: `Accept` header, `produces`/`consumes`, `ContentNegotiationStrategy` (header vs param vs path-extension — esta última desativada por padrão por segurança), `HttpMessageConverter` a fundo, `406 Not Acceptable`/`415 Unsupported Media Type`. Liga à 05/06. |
| 08 | Validação na borda | `@Valid`/`@Validated` no controller (em `@RequestBody`, `@PathVariable`, `@RequestParam`); o que dispara o `MethodArgumentNotValidException` (body) e o `ConstraintViolationException` (params); o **400 automático**; `BindingResult`. Linka **Bean Validation do Galho 7** (a spec — `@NotBlank`/`@Email`/...) e `@Validated`/config do Galho 8 (nota 12). A spec NÃO é re-explicada. |
| 09 | Tratamento de exceções com @ControllerAdvice *(opus)* | `@ExceptionHandler` local vs `@RestControllerAdvice` global (padrão recomendado); mapear exceção → status; `ResponseEntityExceptionHandler` (handlers built-in do Spring); ordem/especificidade dos handlers; não engolir a stack. Linka **AOP/proxy do Galho 8** (nota 09 — é o mecanismo que intercepta) e a nota 10 (o formato da resposta). |
| 10 | Problem Details (RFC 9457) | `ProblemDetail` (Spring Framework 6+); o formato `application/problem+json` (campos `type`/`title`/`status`/`detail`/`instance` + extensões); RFC 9457 (que obsoletou a 7807 — **WebFetch obrigatório**); `ProblemDetail.forStatusAndDetail()`, `setProperty()`; integração com o `@RestControllerAdvice` da 09. Padrão de erro moderno. |
| 11 | Interceptors vs Filters | `HandlerInterceptor` (Spring MVC: `preHandle`/`postHandle`/`afterCompletion`, vê o handler method) vs **Servlet `Filter`** (nível container, antes do `DispatcherServlet`); quando usar cada; `WebMvcConfigurer.addInterceptors`; ordem. Linka **Servlet filters do Galho 7** (nota 03 — a spec) e cita CORS como config MVC (auth/segurança = Galho 12). |
| 12 | Documentando a API com OpenAPI/Swagger | A spec OpenAPI vs Swagger UI; **springdoc-openapi** (o mantido — **não** o springfox legado, morto); geração automática a partir dos controllers; anotações (`@Operation`, `@Schema`, `@ApiResponse`); o endpoint `/v3/api-docs` e a UI. **WebFetch obrigatório** (springdoc.org). |

#### Magus (4 notas — maestria + arquitetura)

| # | Nota | Escopo nuclear |
|---|------|----------------|
| 13 | Versionamento de API | Estratégias: URI path (`/v1/...`), request param (`?version=`), custom header, content-type/media-type (`Accept: application/vnd.api.v2+json`); trade-offs (visibilidade, cache, REST-purismo); deprecação e Sunset header; por que versionar (contrato com clientes). Sem dogma. |
| 14 | HATEOAS | Hypermedia as the engine of application state; **Richardson Maturity Model** (níveis 0-3); Spring HATEOAS (`EntityModel`, `Link`, `WebMvcLinkBuilder`); HAL (`application/hal+json`); o conceito, o custo, e **quando (não) usar** (poucos o usam na prática — mas é tema clássico de entrevista REST). |
| 15 | Clientes HTTP — RestClient, WebClient, RestTemplate *(opus)* | **`RestClient`** (Spring Framework 6.1+, síncrono, fluent — o default moderno — **WebFetch obrigatório**); **`RestTemplate`** (legado, em manutenção, ainda onipresente); **`WebClient`** (menção: reativo, do WebFlux — uso reativo = Galho 11); a história de migração `RestTemplate` → `RestClient`; timeouts/error handling no cliente. **Menção de fronteira:** o cliente declarativo `@FeignClient` (Spring Cloud OpenFeign), orientado a microservices com service discovery/load balancing, é do **Galho 16 (planejado)** — citar em texto, sem wikilink. |
| 16 | Capstone — Uma request HTTP de ponta a ponta no Spring MVC *(opus)* | Traçar uma request real: `Filter` → `DispatcherServlet` → `HandlerMapping` → interceptor → `HandlerAdapter` → argument resolver → `@Valid` → controller → service (delega, fora do escopo) → `ResponseEntity` → `HttpMessageConverter` → resposta; e o caminho de erro (exceção → `@RestControllerAdvice` → `ProblemDetail`). **Tabela "Spring MVC → spec Jakarta"** (`DispatcherServlet`↔Servlet, `@RestController`↔JAX-RS, `@Valid`↔Bean Validation, `HandlerInterceptor`↔Servlet Filter). Checklist de REST API production-grade. Munição de entrevista. Cheatsheet nota→problema. **WebFetch obrigatório.** |

**Notas opus (4):** 01 (assinatura/dupla fronteira), 06 (pipeline — a mais densa), 09 (arquitetura de erro), 15 (pesquisa pura, comparação 3-vias + migração), 16 (capstone síntese). As demais → sonnet. Notas de pesquisa (10/12/13/14/15/16) fazem WebFetch no Step 1 independentemente do modelo.

**Decisões de fronteira (escopo de outro dono — texto "(planejado)", sem wikilink):**
- **Servlet API / JAX-RS / Bean Validation (a spec)** → Galho 7 (COMPLETO). **Linkar de volta, nunca re-explicar a spec.** Primeira metade da fronteira-assinatura.
- **Container / IoC / AOP / beans / config / `@Validated` / Actuator / embedded server** → Galho 8 (COMPLETO). **Linkar de volta** (controllers são beans; `@ControllerAdvice` usa AOP; o `DispatcherServlet` sobe no contexto). Segunda metade da fronteira-assinatura.
- **`@Transactional` operacional / Spring Data / JPA-Hibernate / N+1 / persistência / entidade** → Galho 10. Aqui a entidade aparece só como contraponto ao DTO da borda (nota 05); persistência NÃO é deste galho.
- **WebFlux / Reactor / `Mono`/`Flux` / R2DBC / programação reativa** → Galho 11. `RestClient` (síncrono) é deste galho; **`WebClient` só menção** (reativo = Galho 11).
- **Spring Security / authn/authz / JWT / OAuth2 / CSRF** → Galho 12. **CORS** pode ser citado como config MVC (nota 11), mas auth é Galho 12.
- **`@SpringBootTest` / `@WebMvcTest` / `MockMvc` / slices de teste** → Galho 13.
- **Spring Cloud / Gateway / OpenFeign / service discovery / resilience** → Galho 16. `@FeignClient` só menção de fronteira na nota 15.
- **Observabilidade distribuída / deploy / native image** → Galho 17.
- **Mecânica de annotations/reflection** → Galho 1 nota 11 (linkar). **Threading/concorrência da camada web** → Galho 4 (linkar quando tocar em thread-per-request / virtual threads).

### 3.2. MOC do galho

`03-Dominios/Java/Web e APIs REST/index.md`:
- `type: moc`, `status: growing`
- Frontmatter padrão (`title: "Web e APIs REST"`, tags `java`/`web`/`moc`, aliases `["Web e APIs REST", "Spring MVC", "REST API", "Galho 9 - Web"]`)
- TL;DR callout (galho cobre a camada web sobre o container do Galho 8: Spring MVC e o pipeline do `DispatcherServlet`, REST controllers, content negotiation, validação na borda, tratamento de erro com Problem Details, OpenAPI, HATEOAS, versionamento e clientes HTTP)
- "Sobre este galho" + audiência primária/secundária + nota de que é galho híbrido (refator parcial da seção MVC do tronco `Spring Boot.md` + pesquisa pras partes finas) e de **dupla fronteira** (implementa specs do Galho 7, roda sobre o container do Galho 8)
- Conteúdo agrupado em 3 H2 (`## Iniciado` / `## Adepto` / `## Magus`) com wikilinks pras 16 notas (uma linha descritiva cada)
- **Rotas alternativas (5):**
  - **Completa** — 01 → 16 em ordem
  - **Entrevista internacional** — 01 → 06 → 08 → 09 → 10 → 13 → 16 (pipeline, validação, erro/Problem Details, versionamento, capstone — o que mais cai)
  - **O pipeline desmontado** — 01 → 06 → 07 → 11 → 16 (front controller, pipeline, content negotiation, interceptors/filters, capstone)
  - **Projetando uma REST API production-grade** — 02 → 04 → 05 → 08 → 09 → 10 → 12 → 13 (mapeamentos, status, DTO, validação, erro, Problem Details, OpenAPI, versionamento)
  - **Spring MVC sobre Jakarta EE** (a ponte com o Galho 7) — 01 → 06 → 02 → 08 → 11 + notas do Galho 7 (Servlet API, JAX-RS, Bean Validation)
- "Veja também": MOC central `[[03-Dominios/Java/index|Trilha Java]]`, **Galho 8** (Spring Core e Boot — o container sob a camada web), **Galho 7** (Jakarta EE — as specs HTTP que o Spring MVC implementa), Galho 1 (Annotations), Dicionário de Java; Galhos 10/11/12/13/16/17 como texto "(planejado)" sem wikilink
- Dataview "Todas as notas do galho"

### 3.3. Dicionário de Java (EXPANSÃO — não recriar)

`03-Dominios/Java/Dicionário de Java.md` já existe (**240 verbetes** após o Galho 8, `type: glossary`, `updated: 2026-06-08`, seção alfabética única `## A`…`## Z` com verbetes `### `). Este galho **expande** o arquivo existente inserindo os verbetes **em ordem alfabética case-insensitive (sem acento)** nas seções de letra apropriadas. **Nunca recriar o arquivo nem reordenar verbetes existentes.** Atualizar `updated` no frontmatter.

Verbetes a inserir (~30):

`@ControllerAdvice / @RestControllerAdvice`, `@ExceptionHandler`, `@GetMapping / @PostMapping (mapeamentos HTTP)`, `@PathVariable`, `@RequestBody`, `@RequestHeader`, `@RequestMapping`, `@RequestParam`, `@ResponseBody`, `@ResponseStatus`, `@RestController`, `API versioning`, `content negotiation`, `DispatcherServlet`, `front controller`, `HandlerAdapter`, `HandlerInterceptor`, `HandlerMapping`, `HATEOAS`, `HttpMessageConverter`, `Jackson`, `MethodArgumentNotValidException`, `OpenAPI`, `ProblemDetail (RFC 9457)`, `RestClient`, `RestTemplate`, `Richardson Maturity Model`, `Spring HATEOAS`, `Spring MVC`, `springdoc-openapi`, `Swagger UI`, `WebClient`.

Cada verbete: definição curta (1-3 linhas) em PT-BR + `Veja também:` apontando pra(s) nota(s) canônica(s) do galho. **Conferir com grep os verbetes já existentes** (ex.: `Bean Validation`, `@Validated`, `@Transactional (Spring)`, `@Component / estereótipos Spring`, `Servlet`/`Servlet API` do Galho 7) para **não duplicar** — quando um termo web tocar um já existente, **linkar entre si** (ex.: `@RestController` ↔ `@Component / estereótipos Spring`; `@Valid` web ↔ `Bean Validation (Jakarta Validation)`). **Conferir 1:1** que os headings dos verbetes batem EXATAMENTE com as âncoras usadas nas notas (extrair as âncoras de Dicionário das notas via grep e conferir, como nos Galhos 4-8).

### 3.4. MOC central (ativação do Galho 9)

`03-Dominios/Java/index.md` já existe. Task **mínima**: trocar a linha 39 (atualmente `9. Web e APIs REST *(planejado)* — Spring MVC, REST, exception handling, validation, OpenAPI`) por wikilink ativo no padrão dos galhos fechados:

```markdown
9. [[03-Dominios/Java/Web e APIs REST/index|Web e APIs REST]] — Spring MVC e o pipeline do DispatcherServlet, REST controllers, content negotiation, validação na borda, exception handling (@ControllerAdvice, Problem Details), OpenAPI, HATEOAS, versionamento, clientes HTTP
```

Atualizar `updated`. Não mexer no resto do MOC central.

### 3.5. Poda PARCIAL do tronco (`Backend/Spring Boot.md`)

**Poda mínima e cirúrgica — uma única seção.** O tronco (1090 linhas, `publish: false`) mistura galhos; o Galho 8 já podou as seções core dele (viraram callouts). Este galho poda **só a seção MVC** (deste galho), substituindo-a por callout `[!nota] Migrado para galho próprio` com resumo + wikilinks pras notas novas. Formato herdado dos Galhos 2/3/8:

```markdown
> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Java/Web e APIs REST/index|Web e APIs REST]]. Veja [[03-Dominios/Java/Web e APIs REST/06 - O pipeline do DispatcherServlet|O pipeline do DispatcherServlet]], [[03-Dominios/Java/Web e APIs REST/09 - Tratamento de exceções com @ControllerAdvice|Tratamento de exceções]].
```

**Seção a podar (core — deste galho):**

| Seção do tronco | Linhas (aprox.) | Substituir por callout → notas |
|---|---|---|
| `## Spring MVC pipeline` (O pipeline, DispatcherServlet, HandlerMapping, HandlerAdapter, HttpMessageConverter, Interceptors vs Filters, Exception Handling) | ~221-371 | Callout → notas 01, 02, 04, 06, 07, 09, 10, 11 |

A fabricação `PatientController`/`PatientNotFoundException` (linhas ~332-349) **some com a poda** (a seção inteira vira callout) — **não copiar pras notas** (contraexemplo; usar `Order`/`Customer`). Confirmar os números de linha na execução (lendo o tronco primeiro — política §9 do roadmap; podem ter deslocado).

**NÃO TOCAR (seções de outros galhos):**
- `## Gerenciamento de transações — @Transactional deep dive` → Galho 10
- `## Configuração e Profiles` / `## Actuator` / `## Spring IoC Container` / `## AOP e proxies` / `## O que é` → **já podadas pelo Galho 8** (são callouts; intactas).
- `## Spring WebFlux — visão geral` → Galho 11
- `## Spring Cloud — visão geral` (incl. `### OpenFeign` ~439 e `### Alternativa moderna` ~487 — esta é sobre Kubernetes/Envoy/Vault, **não** sobre RestClient) → Galho 16
- `## Camadas típicas de uma aplicação Spring Boot` (incl. `### Bean Validation` ~573, `### Spring Security` ~546, `### Persistência` ~528) → cross-cutting (galhos 10-13). **Decisão sobre o `### Bean Validation` sob Camadas típicas:** **deixar intacto.** É um "resumo rápido" da visão em camadas (cada subseção aponta pra um deep-dive), não a seção core deste galho; a validação-na-borda a fundo é a nota 08. Fragmentar a visão em camadas seria pior. (A fabricação `CreatePatientRequest`/`PatientController` ali permanece — não é a seção deste galho; o Galho 8 também a deixou.)
- `## Troubleshooting em produção` → galhos 10/16/17
- `## Quando usar` / `## Armadilhas comuns` / `## How to explain in English` / `## Recursos` / `## Veja também` → gerais; atualizar só o "Veja também" pra linkar o MOC do galho.

**Não tocar nos troncos `Backend/Spring Data JPA.md` (Galho 10) nem `Backend/Kafka/` (Galho 14).** O `Veja também` final do tronco recebe wikilink pro MOC do Galho 9.

### 3.6. Dívida reversa (ganchos "Galho 9 / planejado")

Pré-flight localizou **9 ponteiros** (em 8 arquivos) a quitar após as notas existirem. Todos viram wikilinks pras notas do Galho 9; o Spring MVC/Web deixa de ser texto "(planejado)" **nesses pontos específicos**:

| # | Arquivo:linha | Texto atual (resumo) | Vira wikilink pra |
|---|---|---|---|
| 1 | `Jakarta EE/03 - Servlet API — o alicerce HTTP.md:24` | "...incluindo o Spring MVC (Galho 9, planejado)..." | **nota 01** (o `DispatcherServlet` é um servlet) ou nota 06 |
| 2 | `Jakarta EE/07 - JAX-RS — REST declarativo.md:24` | "controllers do Spring são outro caminho ... (Galho 9, planejado)" | **nota 02** (`@RestController`) |
| 3 | `Jakarta EE/07 - JAX-RS — REST declarativo.md:44` | "comparar abordagens: JAX-RS ... Spring MVC (Galho 9, planejado)" | nota 02 ou MOC do galho |
| 4 | `Jakarta EE/08 - Bean Validation.md:24` | "O `@Valid` que você vê no Spring MVC é esta mesma spec (Galho 9, planejado)" | **nota 08** (validação na borda) |
| 5 | `Jakarta EE/index.md:30` | "Spring MVC e validação no Spring são do Galho 9 (planejado)" | MOC do galho (+ nota 08 pra validação) |
| 6 | `Spring Core e Boot/index.md:32` | "Spring MVC/Web (Galho 9) é planejado — endpoints, DispatcherServlet e a camada web ficam lá" | MOC do galho |
| 7 | `Spring Core e Boot/03 - Beans e estereótipos ...:39,47,110,112` | "@Controller / @RestController ... detalhado no Galho 9, planejado" (4 ocorrências) | **nota 02** (`@RestController`) e/ou nota 01 |
| 8 | `Spring Core e Boot/16 - SpringApplication ...:144` | "Tuning profundo de servidor ... Galho 9/17 (planejado)" | nota 06 (pipeline/`DispatcherServlet`) — **manter a parte "/17" como texto "(planejado)"** |
| — | `Linguagem e sintaxe moderna/10 - Exceções ...:361` | "@RestControllerAdvice é o gancho central ... Galho 9 (Web e APIs REST) da trilha. O formato ProblemDetail (RFC 9457)..." | **nota 09** (@ControllerAdvice) + **nota 10** (Problem Details) — já nomeia o galho; trocar por wikilinks |

Em todos, manter como texto "(planejado)" qualquer referência a galhos **ainda** inexistentes (10/11/12/13/16/17). Confirmar os números de linha na execução (podem ter deslocado) via grep `"Galho 9"`/`"planejado"`/`"@Controller"`.

## 4. Convenções por nota

Herda §7 do roadmap e §4 dos specs dos Galhos 7/8. Reforços específicos:

### 4.1. Frontmatter

```yaml
---
title: "<título>"
created: 2026-06-08
updated: 2026-06-08
type: concept
status: seedling
publish: true
fase: iniciado | adepto | magus
tags:
  - java
  - web
  - <fase>
  - <tags específicas: spring-mvc, rest, controller, json, validation, exception-handling, problem-details, openapi, hateoas, versioning, http-client, ...>
aliases:
  - <aliases opcionais>
---
```

H1 `# Título` após o frontmatter (padrão dos galhos publicados).

### 4.2. Estrutura H2 obrigatória

- `> [!abstract] TL;DR` (callout, NÃO H2) — 2-4 linhas: conceito + regra prática + por que importa
- `## O que é` / `## Por que importa` / `## Como funciona` (≥3 subseções H3 em notas Adepto/Magus)
- `## Na prática` — exemplos compiláveis; framing **neutro** (`Order`/`Customer`/`Product`/`OrderController`/`CustomerService`); "padrão observado em APIs Spring"; NUNCA `Patient`/`MedEspecialista`/"no meu projeto" (o tronco está cheio disso — **contraexemplo**)
- `## Armadilhas` — **≥2** (Iniciado) / **≥3** (Adepto/Magus), cada uma com descrição + exemplo curto de código demonstrando o problema + fix em 1 linha
- `## Em entrevista` — subheading `### Frase pronta (inglês)` com **3+ sentenças** (trade-off + decisão + caveat) + subheading `### Vocabulário` com tabela `| Termo PT | Termo EN |` de **6+ termos**
- `## Veja também` — wikilinks **SEM backticks**; sempre inclui notas relacionadas do galho + `[[03-Dominios/Java/Web e APIs REST/index|MOC do galho]]` + `[[03-Dominios/Java/index|Trilha Java]]` + (quando espelhar spec) a nota do **Galho 7** correspondente + (quando usar o container) a nota do **Galho 8** + Galho 1 (Annotations) quando tocar em anotações + verbetes do Dicionário. **Evitar âncoras same-file `[[#Heading]]`** (falso-positivo no checker).
- `## Referências` — docs oficiais (`docs.spring.io/spring-framework/reference/web/...`, `docs.spring.io/spring-boot/...`, `springdoc.org`, RFC 9457). Afirmações version-specific fundadas em fonte verificada via WebFetch.

### 4.3. Restrições absolutas

1. **Dupla fronteira-assinatura (linkar de volta aos Galhos 7 e 8)** — todo conceito que implementa uma spec HTTP aponta pra nota do **Galho 7** ("é a spec por baixo / o outro caminho", sem re-explicar); todo conceito que depende do container aponta pra nota do **Galho 8** ("controller é bean / `@ControllerAdvice` usa AOP / sobe no contexto"). Galhos 10-17 = texto "(planejado)", sem wikilink.
2. **Sem fabricação** de experiência pessoal. Exemplos neutros (`Order`, `Customer`, `Product`) — NUNCA `Patient`/`josenaldo`/`MedEspecialista`/1ª pessoa. **O tronco é matéria-prima a higienizar, jamais a copiar** (a seção MVC tem `PatientController`/`PatientNotFoundException` — contraexemplo). **Zero estatística de adoção inventada** (regra dos Galhos 5/6/7/8) — vale pra HATEOAS ("poucos usam") e pra capstone.
3. **Sem invenção** de APIs/comportamentos. WebFetch obrigatório no Step 1 das notas de pesquisa (Problem Details 10, OpenAPI 12, versionamento 13, HATEOAS 14, clientes HTTP 15, capstone 16) e pra **toda afirmação version-specific**. Pontos minados verificados via WebFetch: **`ProblemDetail` (Spring Framework 6+)** e **RFC 9457** (obsoletou a 7807); **`RestClient` (Spring Framework 6.1+)**; **springdoc-openapi** (mantido) vs **springfox** (legado, morto); Spring Boot 3.x baseline (namespace `jakarta.*`, Java 17). Fonte: `docs.spring.io`, `springdoc.org`, `datatracker.ietf.org` (RFC 9457).
4. **Code samples compiláveis** — Java moderno (records pra DTO, `var`, switch); imports `jakarta.*` quando tocar em specs (Boot 3 — `jakarta.servlet.*`, `jakarta.validation.*`); `properties`/`yaml`/`json` em fences corretas.
5. **Comparações justas** — `@Valid` vs `@Validated`, `ResponseEntity` vs `@ResponseStatus`, interceptor vs filter, `RestClient` vs `RestTemplate` vs `WebClient`, as 4 estratégias de versionamento: sempre "quando X" E "quando Y". A capstone (16) é o ápice (checklist production-grade, sem dogma).
6. **Wikilinks sem backticks** em "Veja também"; MOC do galho + MOC central obrigatórios. **Não linkar galhos inexistentes** (10-17) — texto "(planejado)".
7. **Code fences corretos:** ` ```java ` pra código, ` ```xml ` pra Maven, ` ```properties `/` ```yaml ` pra config, ` ```json ` pra payloads, ` ```text ` pra output/diagrama. Sempre fechadas.
8. **`fase:` no frontmatter + na tag** — obrigatório.
9. **Higiene de commits** — sem `Co-Authored-By: Claude`, sem `--no-verify`, `git add <path>` nominal (nunca `-A` — bot de backup Obsidian Git roda em timer), 1 commit por nota, controlador commita (subagents write-only).
10. **Tom pedagógico graduado** — Iniciado assume Galhos 1-2 + 7 (Servlet/JAX-RS/Bean Validation básicos) + 8 (container básico); Magus assume o galho inteiro + Galhos 7-8.

## 5. Conteúdo por nota (síntese)

Esboço do recorte. Notas de **refator** partem da seção MVC do tronco refinada e higienizada; notas de **pesquisa** fundam-se em doc oficial via WebFetch. Fontes-base: `docs.spring.io/spring-framework/reference/web/webmvc.html`, `docs.spring.io/spring-boot/`, `springdoc.org`, RFC 9457.

- **01 — O que é Spring MVC (refator, opus).** O padrão front controller; o `DispatcherServlet` como porta única (visão geral; mecânica → 06); Spring MVC = camada web do Spring Framework sobre o Servlet container do Galho 7; o que "REST" significa aqui (recursos, verbos HTTP, stateless). A dupla fronteira em uma frase: implementa specs do Galho 7, roda sobre o container do Galho 8. Armadilhas: confundir Spring MVC (servlet/imperativo) com WebFlux (reativo — Galho 11); achar que `@RestController` "é" JAX-RS. Fontes: docs.spring.io/spring-framework/reference/web/webmvc.html (DispatcherServlet).
- **02 — @RestController e os mapeamentos (refator).** `@Controller` vs `@RestController` (= `@Controller` + `@ResponseBody`); `@RequestMapping` (classe + método) e os atalhos `@GetMapping`/`@PostMapping`/`@PutMapping`/`@DeleteMapping`/`@PatchMapping`; `path`/`method`/`params`/`headers`/`produces`/`consumes`; path patterns. Linka Galho 8 (estereótipo/bean) e JAX-RS do Galho 7 (resource methods da spec). Armadilhas: esquecer `@ResponseBody` num `@Controller` (tenta resolver view); colidir mapeamentos; `@PostMapping` sem `consumes` aceitando qualquer coisa. Fontes: docs.spring.io (annotated controllers, request mapping).
- **03 — Recebendo dados da request (refator).** `@PathVariable` (template `{id}`), `@RequestParam` (`required`/`defaultValue`), `@RequestBody` (desserialização via converter), `@RequestHeader`, `@RequestPart` (multipart); binding e conversão de tipos; `Optional`. Linka JAX-RS do Galho 7 (`@PathParam`/`@QueryParam` — params tipados da spec). Armadilhas: `@RequestParam` obrigatório sem default quebrando com 400; nome do path variable ≠ nome do parâmetro; `@RequestBody` num GET. Fontes: docs.spring.io (method arguments, handler methods).
- **04 — ResponseEntity e status codes (refator).** `ResponseEntity<T>` (status + headers + body); `@ResponseStatus` (declarativo); o catálogo de status (200 OK, 201 Created + `Location`, 204 No Content, 400/404/409/422, 500); `ResponseEntity.created(uri)`/`noContent()`/`ok()`. Armadilhas: "200 pra tudo" (inclusive erro); 201 sem `Location`; devolver 200 num delete que devia ser 204; status code no body em vez do header. Fontes: docs.spring.io (ResponseEntity, response status); MDN HTTP status (conceito).
- **05 — Serialização JSON com Jackson (refator + research).** `@ResponseBody` e o `MappingJackson2HttpMessageConverter`; o `ObjectMapper`; **DTO vs entidade** (não expor entidade JPA → Galho 10: lazy/ciclos/over-exposure); anotações Jackson (`@JsonProperty`, `@JsonIgnore`, `@JsonInclude(NON_NULL)`, `@JsonFormat`); `JavaTimeModule` pra datas (registrado por padrão no Boot). Linka Galho 10 (entidade é lá). Armadilhas: serializar entidade JPA direto (LazyInitializationException, vazamento de campos, ciclos); data sem formato ISO; expor campos sensíveis. Fontes: docs.spring.io (message converters), Jackson docs.
- **06 — O pipeline do DispatcherServlet (refator, opus).** A mecânica completa do request: `DispatcherServlet.doDispatch` → `HandlerMapping` (`RequestMappingHandlerMapping`) resolve handler → `HandlerInterceptor.preHandle` → `HandlerAdapter` (`RequestMappingHandlerAdapter`) → `HandlerMethodArgumentResolver` monta os args → método do controller → `HandlerMethodReturnValueHandler` → `HttpMessageConverter` serializa → `postHandle` → `afterCompletion`; tratamento de exceção no pipeline (`HandlerExceptionResolver` — liga à 09). **O `DispatcherServlet` É um servlet** (Galho 7 nota 03), registrado pelo embedded server (Galho 8 nota 16), e é um bean do contexto (Galho 8). Armadilhas: achar que o controller é "chamado direto" (há a engrenagem toda no meio); confundir filter (antes do dispatcher) com interceptor (dentro); assumir uma instância por request (o servlet é singleton, multi-thread — Galho 7). Fontes: docs.spring.io (DispatcherServlet, special bean types, processing).
- **07 — Content negotiation (refator + research).** Como o Spring escolhe a representação: `Accept` header (padrão), `produces` no mapping, `ContentNegotiationStrategy` (header vs `?format=` vs path-extension — esta desativada por padrão por segurança desde Spring 5.3); a cadeia de `HttpMessageConverter`; `406 Not Acceptable` / `415 Unsupported Media Type`. Liga à 05/06. Armadilhas: depender de path-extension (`.json`) desativada; `produces` que não bate com o `Accept` do cliente (406); assumir JSON quando há XML no classpath. Fontes: docs.spring.io (content negotiation, message converters).
- **08 — Validação na borda (refator + research).** `@Valid` (Jakarta, cascata) e `@Validated` (Spring, groups) no controller — em `@RequestBody` (→ `MethodArgumentNotValidException`), em `@PathVariable`/`@RequestParam` com `@Validated` na classe (→ `ConstraintViolationException`); o **400 automático**; `BindingResult` (quando você quer tratar manualmente). Linka **Bean Validation do Galho 7 nota 08** (a spec — `@NotBlank`/`@Email`/`@Size`/...) e `@Validated`/config do Galho 8 nota 12. A spec NÃO é re-explicada; aqui é só a **integração no controller**. Armadilhas: esquecer `@Valid` (request inválido passa); validar e ignorar o `BindingResult`; `@Validated` na classe esquecido pra validar params; misturar validação de negócio (service — Galho 10) com validação de formato (borda). Fontes: docs.spring.io (validation, method validation), Galho 7 nota 08.
- **09 — Tratamento de exceções com @ControllerAdvice (refator, opus).** `@ExceptionHandler` local (só aquele controller) vs `@RestControllerAdvice` global (`@ControllerAdvice` + `@ResponseBody` — padrão recomendado); mapear exceção de domínio → status HTTP; `ResponseEntityExceptionHandler` (os handlers built-in do Spring pra `MethodArgumentNotValidException` etc.); ordem/especificidade; logar sem engolir. **O mecanismo é AOP/proxy** (Galho 8 nota 09 — linkar) e o advice é um bean. O formato da resposta → nota 10. Armadilhas: handler que devolve 200 com erro no body; `catch` que engole a stack (sem log); ordem ambígua de handlers; `@ExceptionHandler` espalhado em vez de centralizado. Fontes: docs.spring.io (error handling, exception handler, ResponseEntityExceptionHandler).
- **10 — Problem Details / RFC 9457 (research).** `ProblemDetail` (Spring Framework 6+): o formato `application/problem+json` (`type`/`title`/`status`/`detail`/`instance` + propriedades de extensão); **RFC 9457** (obsoletou a 7807 — confirmar via WebFetch); `ProblemDetail.forStatusAndDetail()`, `setType()`, `setProperty("errors", ...)`; `ErrorResponse`/`ErrorResponseException`; ligar ao `@RestControllerAdvice` da 09; `spring.mvc.problemdetails.enabled`. Armadilhas: formato de erro ad-hoc por endpoint (inconsistente); vazar stack trace/SQL no `detail`; ignorar o `type` URI; reinventar o que o `ProblemDetail` já dá. Fontes: docs.spring.io (problemdetails, error responses), RFC 9457 (datatracker.ietf.org).
- **11 — Interceptors vs Filters (refator).** `HandlerInterceptor` (Spring MVC: `preHandle`/`postHandle`/`afterCompletion`, tem o handler method, registrado via `WebMvcConfigurer.addInterceptors`) vs **Servlet `Filter`** (nível container, antes do `DispatcherServlet`, registrado via `FilterRegistrationBean`); quando cada um (filter pra cross-cutting de container — encoding, CORS, request logging cru; interceptor pra lógica que precisa do handler — auth de rota, MDC); ordem. Linka **Servlet filters do Galho 7 nota 03** (a spec). **CORS** citado como config MVC (`@CrossOrigin`/`CorsRegistry`); **auth/segurança = Galho 12 (planejado)**. Armadilhas: pôr lógica que precisa do handler num filter; interceptor pra coisa que devia ser filter (encoding); esquecer `afterCompletion` (limpeza de MDC vaza). Fontes: docs.spring.io (interceptors, filters, CORS).
- **12 — OpenAPI/Swagger (research).** OpenAPI (a spec do contrato) vs Swagger UI (a interface); **springdoc-openapi** (a lib mantida — **não** o springfox, legado/morto — confirmar via WebFetch); geração automática dos controllers; `springdoc-openapi-starter-webmvc-ui`; `/v3/api-docs` (JSON) e `/swagger-ui.html`; anotações (`@Operation`, `@Parameter`, `@Schema`, `@ApiResponse`) quando o automático não basta; doc como contrato/cliente gerado. Armadilhas: usar springfox (abandonado); achar que precisa anotar tudo (muito é inferido); expor o swagger-ui em produção sem pensar (→ Galho 12); doc desatualizada por ser escrita à mão em vez de gerada. Fontes: springdoc.org, swagger.io/specification (conceito OpenAPI).
- **13 — Versionamento de API (research).** Por que versionar (contrato com clientes que não atualizam juntos); estratégias: **URI path** (`/v1/orders` — visível, cacheável, "não-REST-puro"), **request param** (`?version=1`), **custom header** (`X-API-Version`), **media-type/content negotiation** (`Accept: application/vnd.company.v2+json` — REST-purista, menos visível); trade-offs de cada (visibilidade, cache, roteamento, complexidade); deprecação (`Deprecation`/`Sunset` headers). Sem dogma — cada um tem contexto. Armadilhas: nunca versionar e quebrar clientes; versionar cedo demais; misturar estratégias; "v2" que muda semântica sem avisar. Fontes: docs.spring.io (versioning, se houver), guias de API design (conceito; sem estatística inventada).
- **14 — HATEOAS (research).** Hypermedia as the Engine of Application State; **Richardson Maturity Model** (nível 0 RPC → 1 recursos → 2 verbos HTTP → 3 hypermedia); Spring HATEOAS (`EntityModel<T>`, `Link`, `WebMvcLinkBuilder.linkTo(methodOn(...))`, `RepresentationModelAssembler`); HAL (`application/hal+json`, `_links`); o conceito, o custo (acoplamento cliente-servidor reduzido vs complexidade), e **quando (não) usar** — honestamente, pouca API pública o adota, mas é tema clássico de entrevista REST e de maturidade de design. Armadilhas: confundir "REST" com "nível 2" (a maioria); adicionar links que ninguém consome (custo sem benefício); achar HATEOAS obrigatório pra ser REST. Fontes: docs.spring.io/spring-hateoas, Richardson Maturity Model (Fowler — conceito).
- **15 — Clientes HTTP: RestClient, WebClient, RestTemplate (research, opus).** **`RestClient`** (Spring Framework 6.1+ — síncrono, API fluent, o default moderno pra blocking — confirmar via WebFetch); **`RestTemplate`** (legado, em manutenção desde 5.0 mas ainda onipresente — `getForObject`/`exchange`); **`WebClient`** (menção: reativo, parte do WebFlux; uso reativo/streaming = **Galho 11 planejado**; pode ser usado bloqueante mas não é o ponto); a história de migração `RestTemplate` → `RestClient`; timeouts (`ClientHttpRequestFactory`), error handling (`onStatus`/`StatusHandler`), interceptors. **Menção de fronteira:** o cliente declarativo `@FeignClient` (Spring Cloud OpenFeign) — orientado a microservices com service discovery e client-side load balancing — é do **Galho 16 (planejado)**; citar em texto, sem wikilink. Armadilhas: `new RestTemplate()` a cada chamada (criar/reusar); sem timeout (thread presa pra sempre); ignorar status de erro do cliente; escolher `WebClient` "porque é novo" num stack imperativo (puxa Reactor sem necessidade — Galho 11). Fontes: docs.spring.io/spring-framework/reference/web/webmvc/mvc-controller/...rest-clients, docs do RestClient/RestTemplate.
- **16 — Capstone: uma request HTTP de ponta a ponta (research, opus).** Traçar uma request `POST /orders` válida e uma inválida: `Filter` (encoding/CORS) → `DispatcherServlet` → `HandlerMapping` → `preHandle` → `HandlerAdapter` → argument resolver desserializa `@RequestBody` → `@Valid` (sucesso ou `MethodArgumentNotValidException`) → controller chama service (delega — fora do escopo) → `ResponseEntity.created()` → `HttpMessageConverter` serializa → `afterCompletion`; e o caminho de erro: exceção → `HandlerExceptionResolver` → `@RestControllerAdvice` → `ProblemDetail` (`application/problem+json`). **Tabela "Spring MVC → spec Jakarta"** (`DispatcherServlet`↔Servlet API, `@RestController`↔JAX-RS, `@Valid`↔Bean Validation, `HandlerInterceptor`↔Servlet Filter — "o caminho do Spring vs a spec portável"). **Checklist REST API production-grade** (status corretos, DTO não-entidade, validação na borda, erro RFC 9457, OpenAPI, versionamento, timeouts no cliente). Munição de entrevista (frases sobre o pipeline, sobre Problem Details, sobre versionamento). Cheatsheet nota→problema. Armadilhas (de raciocínio): "o controller é chamado direto" (há o pipeline); "qualquer 2xx serve"; "validação é no service" (também na borda); decidir client/versão por hype. Fontes: docs.spring.io (web overview), RFC 9457.

## 6. Pré-flight: verificações feitas

Executado nesta fase de brainstorming (2026-06-08); itens version-specific re-confirmados na execução de cada nota via WebFetch:

1. **Tronco mapeado** — `Backend/Spring Boot.md` (1090 linhas após o Galho 8, `publish: false`, `status: evergreen`) lido na seção MVC; **uma única seção core deste galho**: `## Spring MVC pipeline` (~221-371). As seções core do Galho 8 (`## O que é`, IoC, AOP, Config, Actuator) já são callouts; `## Gerenciamento de transações` (Galho 10), `## Spring MVC pipeline` deixada intacta pelo 8 de propósito, WebFlux/Cloud/Camadas/Troubleshooting são de outros galhos.
2. **Fabricação confirmada** — `PatientController`/`PatientNotFoundException` (linhas 332-349) **dentro da seção MVC** → **some com a poda** (vira callout); não copiar pras notas. A fabricação sob `## Camadas típicas` (`CreatePatientRequest`/`PatientController` ~578-588) **permanece** (não é a seção deste galho — cross-cutting, o Galho 8 também deixou). Notas usam `Order`/`Customer`.
3. **HTTP clients ausentes no tronco** — grep `RestClient`/`RestTemplate`/`WebClient` no tronco = **vazio**. Nota 15 é **pesquisa pura**. O `### Alternativa moderna` (~487) é sobre Kubernetes/Envoy/Vault (Spring Cloud), **não** RestClient — não confundir; é do Galho 16, intacto.
4. **Dívida reversa localizada** — 9 ponteiros em 8 arquivos (§3.6): Servlet API 03:24, JAX-RS 07:24, JAX-RS 07:44, Bean Validation 08:24, Jakarta index:30, Spring Core index:32, Spring Core 03:39/47/110/112, Spring Core 16:144, Linguagem 10:361. Confirmar linhas na execução.
5. **Dicionário** — **240 verbetes** após o Galho 8; seção alfabética única `## A`…`## Z`; verbetes `### `; `updated: 2026-06-08`. Verbetes Spring core (do Galho 8) existem; web ainda não. Expansão alfabética, nunca recriar/reordenar; conferir dups (`Bean Validation`, `@Validated`, `Servlet`, `@Component / estereótipos`) e linkar entre si.
6. **MOC central** — `03-Dominios/Java/index.md:39` é a linha do Galho 9 (`*(planejado)*`); galhos ativos usam `N. [[path/index|Title]] — summary`; `updated: 2026-06-08`.
7. **Troncos intocáveis** — `Backend/Spring Data JPA.md` (Galho 10), `Backend/Kafka/` (Galho 14).
8. **Versões a cravar via WebFetch na execução** — `ProblemDetail` (Spring Framework 6+) e **RFC 9457** (obsoletou 7807); `RestClient` (Spring Framework 6.1+); **springdoc-openapi** (mantido) vs **springfox** (morto); Spring Boot 3.x baseline (Java 17, `jakarta.*`). Spring Boot 4.0.x / Framework 7.0.x já são as releases atuais — manter **3.x/6.x como baseline** (como o Galho 8), citando 4/7 como "mais recente" quando relevante. Fonte: `docs.spring.io`, `springdoc.org`, `datatracker.ietf.org`.

Nenhum número de adoção é inventado. Quando faltar fato verificável, **PERGUNTAR** antes de escrever.

## 7. Critérios de aceitação do galho

Além dos critérios gerais (§10 do roadmap):

1. 16 notas em `03-Dominios/Java/Web e APIs REST/`, frontmatter completo com `fase:`, `publish: true`, distribuídas 5/7/4.
2. MOC do galho com 3 subseções de fase + 5 rotas alternativas + dataview + folder-link resolve (`index.md` presente).
3. Dicionário de Java **expandido** (não recriado) com ~30 verbetes; verbetes dos Galhos 1-8 intactos; `updated` atualizado; dups conferidos e linkados (não duplicar `Bean Validation`/`@Validated`/`Servlet`/`@Component`); headings conferidos 1:1 com as âncoras usadas nas notas (via grep).
4. MOC central `Java/index.md` com Galho 9 ativado (linha 39 vira wikilink); resto intacto.
5. **Poda parcial executada**: a seção `## Spring MVC pipeline` substituída por callout `[!nota] Migrado para galho próprio` + wikilinks (a fabricação `PatientController` da seção some com a poda). **Seções de outros galhos intactas** (`## Gerenciamento de transações`, callouts do Galho 8, WebFlux/Cloud/Camadas/Troubleshooting; `### Bean Validation` sob Camadas típicas deixado intacto). `Spring Data JPA.md`/`Kafka/` intactos.
6. **Dívida reversa quitada**: os 9 ponteiros com wikilinks corretos (Servlet API 03:24→nota 01/06, JAX-RS 07:24→nota 02, Bean Validation 08:24→nota 08, Linguagem 10:361→notas 09/10, etc.); galhos ainda inexistentes (10-17) permanecem texto "(planejado)" — incl. a parte "/17" do gancho Spring Core 16:144.
7. Cada nota: TL;DR; code samples compiláveis (Java moderno, records pra DTO, `jakarta.*` quando spec, fences corretas); "Em entrevista" com `### Frase pronta (inglês)` 3+ sentenças + `### Vocabulário` tabela 6+ termos PT→EN; "Armadilhas" com exemplo+fix (≥2 Iniciado, ≥3 Adepto/Magus); wikilinks (galho + MOC central + Galho 7 quando espelhar spec + Galho 8 quando usar o container + Galho 1 quando anotações + Dicionário); "Referências" com docs oficiais verificadas.
8. **Dupla fronteira-assinatura respeitada**: cada conceito que implementa spec HTTP linka de volta ao Galho 7 sem re-explicar; cada conceito que usa o container linka ao Galho 8; galhos 10-17 só como texto "(planejado)"; nenhum wikilink pra galho inexistente.
9. **Fronteiras de escopo respeitadas**: entidade/JPA só como contraponto ao DTO (Galho 10); `WebClient` só menção (reativo = Galho 11); CORS como config mas auth = Galho 12; `MockMvc`/slices = Galho 13; `@FeignClient` só menção (Galho 16); zero conteúdo de Security/WebFlux/Test/Cloud profundo.
10. Zero fabricação de experiência pessoal; zero estatística de adoção inventada; afirmações version-specific citam a versão verificada via WebFetch.
11. 1 commit por nota; sem `Co-Authored-By: Claude`; sem `--no-verify`; stage nominal (nunca `-A`); subagents write-only, controlador commita.
12. `verificar-wikilinks` roda limpo na pasta do galho (as ~204 quebras legadas da árvore Java NÃO são deste galho; evitar âncoras same-file).

## 8. Riscos e mitigações

| Risco | Mitigação |
|---|---|
| **Re-explicar a spec Jakarta (Servlet/JAX-RS/Bean Validation)** em vez de linkar de volta (1ª metade da fronteira-assinatura) | Restrição 4.3.1; review por fase checa cada nota que espelha spec; capstone mapeia em tabela; cada conceito espelhado tem wikilink obrigatório pro Galho 7. |
| **Re-explicar o container (IoC/AOP/beans)** em vez de linkar ao Galho 8 (2ª metade) | Restrição 4.3.1; controllers/`@ControllerAdvice`/`DispatcherServlet` linkam Galho 8 (notas 03/09/16); review por fase. |
| **Invadir Galho 10 (persistência) ou 11 (reativo)** ao falar de entidade/`WebClient` | Fronteira dura (§3.1): entidade só como contraponto ao DTO; `WebClient` só menção; review por fase. |
| **Invadir Galho 12 (segurança)** ao falar de filters/CORS | CORS como config MVC; auth/CSRF/JWT = Galho 12 (texto "planejado"); review checa nota 11. |
| **Poda danificar seções de outros galhos** (tronco de 1090 linhas, multi-galho) | Ler o tronco primeiro (§9 roadmap); podar **só** `## Spring MVC pipeline`; `## Gerenciamento de transações` e callouts do Galho 8 explicitamente intocáveis; mudança via commit reversível. |
| **Copiar fabricação do tronco** (`PatientController`/MedEspecialista) pras notas | Tronco é contraexemplo (restrição 4.3.2); a seção MVC vira callout (a fabricação some); exemplos neutros `Order`/`Customer`; review por fase grep `Patient|MedEspecialista|minha`. |
| **Inventar API "de memória"** nas notas de pesquisa (Problem Details, OpenAPI, RestClient, versionamento, HATEOAS) | WebFetch no Step 1 dessas notas; `RestClient` (6.1+), `ProblemDetail`/RFC 9457, springdoc≠springfox são os pontos minados — verificar; Referências com fonte oficial. |
| Versões envelhecerem (Boot 3.x vs 4.x, RestClient, RFC) | Baseline 3.x/6.x (como Galho 8), citando 4/7 como "mais recente"; WebFetch por nota version-specific; declarar version-specificity no corpo. |
| Galho denso (16 notas) inflar nº de notas ou notas individuais | Distribuição 5/7/4 fixada; se uma nota passar de ~600 linhas, dividir nota (não galho); capstone com cheatsheet enxuto. |
| Dicionário: duplicar verbete já existente (`Bean Validation`, `@Validated`, `Servlet`, `@Component`) | Grep dos existentes antes de inserir; quando tocar um existente, **linkar** em vez de duplicar; inserção alfabética, nunca recriar; conferir âncoras 1:1. |
| Bot de backup (Obsidian Git) commitando no meio | Padrão dos Galhos 2/3/6/7/8: subagents write-only; controlador commita imediatamente após cada nota com `git add` nominal (nunca `-A`); guardar contra `.git/index.lock`. |

## 9. Próximos passos

1. **Aprovação deste spec**
2. **Plano de execução** via skill `superpowers:writing-plans` → `docs/superpowers/plans/2026-06-08-java-galho-09-web-rest-execution.md`
3. **Execução** via `superpowers:subagent-driven-development` **direto na `main`** (subagents write-only; sonnet por padrão, opus nas notas 01/06/09/15/16; review **por fase** + fix loop; push manual do usuário)
4. **Verificação** de wikilinks + conferência de âncoras do Dicionário
5. **Atualização da memória** `project_trilha_java` (Galho 9 completo) antes do próximo galho

## 10. Documentos relacionados

- `2026-06-02-java-senior-roadmap-design.md` — roadmap macro (18 galhos)
- `2026-06-08-java-galho-08-spring-core-design.md` / `...-execution.md` — Galho 8 (dependência direta; o container sob a camada web; molde mais recente de poda parcial + dupla natureza)
- `2026-06-07-java-galho-07-jakarta-ee-design.md` — Galho 7 (dependência conceitual; dono das specs HTTP que o Spring MVC implementa: Servlet API, JAX-RS, Bean Validation)
- `2026-06-04-java-galho-02-collections-streams-design.md`, `2026-06-05-java-galho-03-jvm-design.md` — templates de **poda parcial** de tronco monolítico
- Artefatos a atualizar: `03-Dominios/Java/Dicionário de Java.md`, `03-Dominios/Java/index.md`, `03-Dominios/Java/Backend/Spring Boot.md` (poda parcial — seção MVC), `Jakarta EE/03 - Servlet API`, `07 - JAX-RS`, `08 - Bean Validation`, `Jakarta EE/index.md`, `Spring Core e Boot/index.md`, `Spring Core e Boot/03 - Beans e estereótipos`, `Spring Core e Boot/16 - SpringApplication`, `Linguagem e sintaxe moderna/10 - Exceções e tratamento de erros.md` (dívida reversa)
- Fontes-base do galho: `docs.spring.io/spring-framework/reference/web/webmvc.html`, `docs.spring.io/spring-boot/`, `springdoc.org`, RFC 9457 (`datatracker.ietf.org`)
- Memórias: [[project_trilha_java]], [[project_trilhas_fases_aprendizado]], [[project_tronco_galhos_pattern]], [[feedback_galhos_direto_main]], [[feedback_no_fabrication]], [[feedback_quartz_index]], [[feedback_commits]], [[feedback_dataview_inline_code]]
