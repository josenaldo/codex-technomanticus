# Galho 9 — Web e APIs REST (Java Senior) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Criar o Galho 9 da trilha Java Senior — 16 notas atômicas (Spring MVC, REST controllers, binding de request, `ResponseEntity`/status, serialização JSON, pipeline do `DispatcherServlet`, content negotiation, validação na borda, `@ControllerAdvice`, Problem Details/RFC 9457, interceptors vs filters, OpenAPI, versionamento, HATEOAS, clientes HTTP, capstone) em 3 fases + MOC do galho + expansão do Dicionário + ativação do MOC central + **poda parcial** do tronco `Backend/Spring Boot.md` (só a seção MVC) + **quitação de 9 ponteiros de dívida reversa**.

**Architecture:** Padrão galhos + 3 fases (Iniciado/Adepto/Magus). Pasta flat `03-Dominios/Tecnologia/Java/Web e APIs REST/`, notas `publish: true` em PT-BR, numeração global 01-16 (5/7/4). **Galho HÍBRIDO:** REFATOR (a seção `## Spring MVC pipeline` do tronco é refinada e higienizada) + PESQUISA (Problem Details, content negotiation a fundo, OpenAPI, HATEOAS, versionamento, clientes HTTP nascem de `docs.spring.io`/`springdoc.org`/RFC via WebFetch). **DUPLA fronteira-assinatura:** cada conceito que implementa uma spec HTTP **linka de volta** ao **Galho 7** (Servlet/JAX-RS/Bean Validation) sem re-explicar a spec; cada conceito que usa o container **linka de volta** ao **Galho 8** (controllers são beans, `@ControllerAdvice` usa AOP, `DispatcherServlet` sobe no contexto). Galhos 10/11/12/13/16/17 = texto "(planejado)", sem wikilink. **Direto na `main`** ([[feedback_galhos_direto_main]]); push manual do usuário.

**Tech Stack:** Obsidian Flavored Markdown, frontmatter YAML, wikilinks, callouts, Dataview, Quartz v4. Verificação via WebFetch (`docs.spring.io/spring-framework/reference/web/`, `docs.spring.io/spring-boot/`, `springdoc.org`, `datatracker.ietf.org`).

---

## Convenções aplicadas a TODAS as notas (ler antes de qualquer task)

**Frontmatter** (ajustar `title`/`fase`/`tags`/`aliases` por nota; `created`/`updated: 2026-06-08`):

```yaml
---
title: "<título sem prefixo numérico>"
created: 2026-06-08
updated: 2026-06-08
type: concept
progress: backlog
status: seedling
publish: true
fase: iniciado | adepto | magus
tags:
  - java
  - web
  - <fase>
  - <1-3 tags de conceito: spring-mvc, rest, controller, json, validation, exception-handling, problem-details, openapi, hateoas, versioning, http-client>
aliases:
  - <aliases>
---
```

H1 `# Título` após o frontmatter (padrão dos galhos publicados).

**Estrutura H2 obrigatória** (nesta ordem):

1. `> [!abstract] TL;DR` — 2-4 linhas. Callout, NÃO H2.
2. `## O que é` — definição.
3. `## Por que importa` — relevância pra senior/entrevista. (Pode fundir com "O que é" em Iniciado curtas.)
4. `## Como funciona` — H3s; mínimo 3 em Adepto/Magus.
5. `## Na prática` — código compilável; framing neutro; **NUNCA** 1ª pessoa, `Patient`, `Josenaldo`, `MedEspecialista`. Domínios neutros: `Order`, `Customer`, `Product`, `OrderController`, `CustomerService`. Records pra DTO. Imports `jakarta.*` quando tocar em spec (Boot 3: `jakarta.servlet.*`, `jakarta.validation.*`).
6. `## Armadilhas` — ≥2 (Iniciado) / ≥3 (Adepto/Magus). Cada uma: `### (N) Título` + descrição + exemplo curto + fix em 1 linha.
7. `## Em entrevista` — `### Frase pronta (inglês)` com **3+ sentenças** (trade-off + decisão + caveat) + `### Vocabulário` **6+ termos** em tabela `| Termo PT | Termo EN |`.
8. `## Veja também` — wikilinks SEM backticks, SEM âncoras same-file `[[#...]]`. Sempre: notas do galho + `[[03-Dominios/Tecnologia/Java/Web e APIs REST/index|Web e APIs REST (MOC do galho)]]` + `[[03-Dominios/Tecnologia/Java/index|Trilha Java]]` + (quando espelhar spec) a nota do **Galho 7** correspondente + (quando usar o container) a nota do **Galho 8** + (quando tocar annotations) Galho 1 nota 11 + verbetes do Dicionário.
9. `## Referências` — docs oficiais consultadas (`docs.spring.io/...`, `springdoc.org`, RFC 9457).

**Tamanho:** 200-500 linhas (densas até 600 — limite de [[feedback_notas_atomicas]]).

**Restrições absolutas:**
- **DUPLA fronteira-assinatura.** Mapeamento de link-back **Galho 7** (a spec, não re-explicar): `DispatcherServlet`/pipeline → Servlet API 03; `@RestController`/mapeamentos → JAX-RS 07; binding de params → JAX-RS 07; `@Valid` no controller → Bean Validation 08; `HandlerInterceptor` vs Filter → Servlet API 03 (filters). Mapeamento de link-back **Galho 8** (o container): controllers são beans/estereótipos → Beans 03; `@ControllerAdvice`/`@ExceptionHandler` (mecanismo) → AOP 09; `DispatcherServlet` sobe no contexto/embedded server → SpringApplication 16; `@Validated`/config → Configuração 12.
- **Galhos 10-17 só como texto "(planejado)", SEM wikilink.** Greps de review checam `\[\[[^]]*(Galho (10|11|12|13|16|17)|WebFlux|Spring Security|Spring Data|Spring Cloud|OpenFeign|MockMvc|Testcontainers)`.
- Sem fabricação ([[feedback_no_fabrication]]); **o tronco é contraexemplo** (`PatientController`/`MedEspecialista`/1ª pessoa — NUNCA copiar; usar `Order`/`Customer`); **zero estatística de adoção inventada** — vale pra HATEOAS ("poucos usam") e capstone.
- **Pesquisa pras partes finas:** notas 10/12/13/14/15/16 fundam-se em WebFetch (Step 1); 05/07/08/09 também confirmam pontos via WebFetch. Toda afirmação version-specific verificada: **`ProblemDetail` (Spring Framework 6+)** e **RFC 9457** (obsoletou 7807); **`RestClient` (Spring Framework 6.1+)**; **springdoc-openapi** (mantido) vs **springfox** (legado/morto); Boot 3.x baseline (Java 17, `jakarta.*`). Boot 4.0.x/Framework 7.0.x já são as releases atuais — **manter 3.x/6.x como baseline** (como o Galho 8), citando 4/7 como "mais recente" quando relevante. Nada de memória.
- **Não re-explicar o que é de outro galho:** Servlet/JAX-RS/Bean Validation (a spec) → Galho 7 (linkar); IoC/AOP/beans/config/embedded server → Galho 8 (linkar); entidade/JPA/`@Transactional` operacional → Galho 10 (texto); `WebClient`/Reactor → Galho 11 (`WebClient` só menção); Security/auth/CSRF → Galho 12 (CORS pode ser citado como config MVC; auth não); `MockMvc`/`@WebMvcTest`/slices → Galho 13; OpenFeign/Gateway/service discovery → Galho 16 (`@FeignClient` só menção); native/deploy → Galho 17.
- Comparações justas (quando X E quando Y): `@Valid` vs `@Validated`, `ResponseEntity` vs `@ResponseStatus`, interceptor vs filter, `RestClient` vs `RestTemplate` vs `WebClient`, as 4 estratégias de versionamento.
- Code fences: ` ```java `, ` ```xml ` (Maven), ` ```properties `/` ```yaml ` (config), ` ```json ` (payloads), ` ```bash `, ` ```text `. Sempre fechadas.
- Commits: sem `Co-Authored-By: Claude`; sem `--no-verify`; `git add <path>` nominal (bot de backup roda em timer — NUNCA `-A`; guardar contra `.git/index.lock`); 1 commit por nota; direto na `main`; **sem push, sem deploy**. Subagents NÃO rodam git — o controlador commita.

**Modelo por nota:** sonnet por padrão; **opus** nas **01** (assinatura/dupla fronteira), **06** (pipeline), **09** (arquitetura de erro), **15** (clientes HTTP — pesquisa/comparação) e **16** (capstone).

**Fontes oficiais (base):**
- Spring MVC overview: `https://docs.spring.io/spring-framework/reference/web/webmvc.html`
- DispatcherServlet: `https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-servlet.html`
- Annotated controllers / request mapping: `https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-controller.html` · `.../mvc-controller/ann-requestmapping.html`
- Method arguments / responseentity: `.../mvc-controller/ann-methods/arguments.html` · `.../ann-methods/responseentity.html`
- Message converters / content negotiation: `.../mvc-controller/ann-methods/responsebody.html` · `https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-config/content-negotiation.html`
- Validation: `https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-controller/ann-validation.html`
- Exception handling / REST error responses: `.../mvc-controller/ann-exceptionhandler.html` · `https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-ann-rest-exceptions.html`
- Interceptors / CORS: `https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-config/interceptors.html` · `https://docs.spring.io/spring-framework/reference/web/webmvc-cors.html`
- REST clients (RestClient/RestTemplate): `https://docs.spring.io/spring-framework/reference/integration/rest-clients.html`
- springdoc-openapi: `https://springdoc.org/`
- Spring HATEOAS: `https://docs.spring.io/spring-hateoas/docs/current/reference/html/`
- RFC 9457 (Problem Details): `https://datatracker.ietf.org/doc/html/rfc9457`

---

## Task 0: Pré-flight — pasta, terreno e baselines

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Web e APIs REST/` (pasta)

- [ ] **Step 1: Confirmar `main`**

```bash
git branch --show-current
```
Expected: `main`. NÃO criar branch.

- [ ] **Step 2: Criar a pasta do galho**

```bash
mkdir -p "03-Dominios/Tecnologia/Java/Web e APIs REST"
```

- [ ] **Step 3: Confirmar títulos exatos das notas dos Galhos 7 e 8 (linkadas de volta)**

```bash
ls "03-Dominios/Tecnologia/Java/Jakarta EE/" | grep -E "^(03|07|08) "
ls "03-Dominios/Tecnologia/Java/Spring Core e Boot/" | grep -E "^(03|09|12|16) "
ls "03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/" | grep -E "^(10|11) "
```
Expected: Galho 7 — `03 - Servlet API — o alicerce HTTP`, `07 - JAX-RS — REST declarativo`, `08 - Bean Validation`; Galho 8 — `03 - Beans e estereótipos — @Component, @Service, @Repository, @Controller`, `09 - AOP e proxies no Spring`, `12 - Configuração e profiles`, `16 - SpringApplication e o embedded server`; Galho 1 — `10 - Exceções e tratamento de erros`, `11 - Annotations`. Anotar divergências.

- [ ] **Step 4: Relocalizar a dívida reversa (9 ponteiros, 8 arquivos — linhas podem ter mudado)**

```bash
grep -rn "Galho 9\|planejado" "03-Dominios/Tecnologia/Java/Jakarta EE/03 - Servlet API — o alicerce HTTP.md" "03-Dominios/Tecnologia/Java/Jakarta EE/07 - JAX-RS — REST declarativo.md" "03-Dominios/Tecnologia/Java/Jakarta EE/08 - Bean Validation.md" "03-Dominios/Tecnologia/Java/Jakarta EE/index.md" "03-Dominios/Tecnologia/Java/Spring Core e Boot/index.md" "03-Dominios/Tecnologia/Java/Spring Core e Boot/16 - SpringApplication e o embedded server.md" "03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/10 - Exceções e tratamento de erros.md"
grep -n "@Controller\|Galho 9" "03-Dominios/Tecnologia/Java/Spring Core e Boot/03 - Beans e estereótipos — @Component, @Service, @Repository, @Controller.md"
```
Expected: Servlet API 03:~24; JAX-RS 07:~24 e ~44; Bean Validation 08:~24; Jakarta index:~30; Spring index:~32; Spring 16:~144; Linguagem 10:~361; Spring 03:~39/47/110/112. Anotar linhas reais pra Task 21.

- [ ] **Step 5: Baseline do Dicionário**

```bash
grep -cE "^### " "03-Dominios/Tecnologia/Java/Dicionário de Java.md"
```
Expected: **240** (baseline pós-Galho 8). Anotar o número real.

- [ ] **Step 6: Mapear a seção MVC do tronco (pra Task 20 — poda parcial) e confirmar a fabricação**

```bash
grep -nE "^#{2,3} " "03-Dominios/Tecnologia/Java/Backend/Spring Boot.md"
grep -niE "Patient|Josenaldo|MedEspecialista|minha experiência" "03-Dominios/Tecnologia/Java/Backend/Spring Boot.md" | head -40
grep -niE "RestClient|RestTemplate|WebClient" "03-Dominios/Tecnologia/Java/Backend/Spring Boot.md"
```
Expected: confirmar **`## Spring MVC pipeline` ~221-371** (a única seção core deste galho — subseções: O pipeline, DispatcherServlet, HandlerMapping, HandlerAdapter, HttpMessageConverter, Interceptors vs Filters, Exception Handling). Confirmar fabricação `PatientController`/`PatientNotFoundException` ~332-349 **dentro** dessa seção (some com a poda). Confirmar INTOCÁVEIS: `## Gerenciamento de transações` (galho 10), os callouts do Galho 8 (`## O que é`/IoC/AOP/Config/Actuator), `## Spring WebFlux`/`## Spring Cloud`/`## Camadas típicas` (incl. `### Bean Validation` ~573 — **deixar intacto**)/`## Troubleshooting`. Terceiro grep **VAZIO** (clientes HTTP não estão no tronco — nota 15 é pesquisa pura). Anotar ranges reais pra Task 20.

- [ ] **Step 7: Fixar fatos a verificar via WebFetch** — `ProblemDetail` (Framework 6+) + RFC 9457 (obsoletou 7807); `RestClient` (Framework 6.1+); springdoc-openapi (mantido) vs springfox (morto); Boot 3.x baseline (Java 17, `jakarta.*`); versionamento de API (estratégias conceituais; o atributo `version` em `@RequestMapping` é Framework 7.0 — citar como "mais recente"). Nada de memória.

- [ ] **Step 8: Sem commit** (preparação).

---

## Fase INICIADO (notas 01-05)

### Task 1: Nota 01 — O que é Spring MVC — a camada web sobre o container ⟦opus⟧

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Web e APIs REST/01 - O que é Spring MVC — a camada web sobre o container.md`

- [ ] **Step 1: Pesquisar** — WebFetch `https://docs.spring.io/spring-framework/reference/web/webmvc.html` + `.../web/webmvc/mvc-servlet.html`. CONFIRMAR: Spring MVC = camada web servlet-based do Spring Framework; o padrão front controller; o `DispatcherServlet` como porta única; baseline Boot 3 (`jakarta.servlet.*`). Refinar a abertura da seção `## Spring MVC pipeline` do tronco, **higienizando**.

- [ ] **Step 2: Escrever** — `fase: iniciado`, tags `[java, web, iniciado, spring-mvc]`, aliases `["Spring MVC", "Spring Web MVC"]`. **Nota-assinatura da dupla fronteira.** Conteúdo:
  - TL;DR: Spring MVC é a camada web (servlet/imperativa) do Spring Framework; um front controller (`DispatcherServlet`) recebe todo request e delega a um controller; implementa as specs HTTP do Galho 7 e roda sobre o container do Galho 8.
  - `## O que é` — front controller; o `DispatcherServlet` como porta única (visão geral; mecânica → nota 06); MVC vs REST aqui (recursos, verbos HTTP, stateless).
  - `## Por que importa` — é como toda request HTTP vira resposta num backend Spring; entrevista cobra "o que acontece quando chega um request".
  - `## Como funciona` — H3s: "O padrão front controller e o `DispatcherServlet`", "Spring MVC sobre o Servlet container (o `DispatcherServlet` é um servlet — Galho 7)", "Controllers são beans do contexto (Galho 8)", "Spring MVC vs WebFlux (servlet/imperativo vs reativo — Galho 11, planejado)".
  - `## Na prática` — `@SpringBootApplication` + um `@RestController` mínimo `OrderController` com um `@GetMapping` (```java); `pom.xml` com `spring-boot-starter-web` (```xml).
  - `## Armadilhas` — ≥2: (1) confundir Spring MVC (imperativo) com WebFlux (reativo); (2) achar que `@RestController` "é" JAX-RS (é o caminho do Spring pro mesmo problema).
  - `## Em entrevista` + `## Veja também` ([[06 - O pipeline do DispatcherServlet]], [[02 - @RestController e os mapeamentos]], **[[03-Dominios/Tecnologia/Java/Jakarta EE/03 - Servlet API — o alicerce HTTP|Servlet API]]** (a spec por baixo), **[[03-Dominios/Tecnologia/Java/Jakarta EE/07 - JAX-RS — REST declarativo|JAX-RS]]** (o outro caminho), **[[03-Dominios/Tecnologia/Java/Spring Core e Boot/index|Spring Core e Boot]]** (o container), MOC galho, MOC central, verbetes `Spring MVC`/`DispatcherServlet`/`front controller`) + `## Referências`.

- [ ] **Step 3: Verificar**
```bash
grep -cE "^## (O que é|Por que importa|Como funciona|Na prática|Armadilhas|Em entrevista|Veja também|Referências)" "03-Dominios/Tecnologia/Java/Web e APIs REST/01 - O que é Spring MVC — a camada web sobre o container.md"
grep -riE "Patient|MedEspecialista|minha experiência" "03-Dominios/Tecnologia/Java/Web e APIs REST/01 - O que é Spring MVC — a camada web sobre o container.md"
grep -c "Jakarta EE/03 - Servlet API" "03-Dominios/Tecnologia/Java/Web e APIs REST/01 - O que é Spring MVC — a camada web sobre o container.md"
```
Expected: ≥7 seções; segundo grep **VAZIO**; terceiro ≥1 (link de volta ao Galho 7).

- [ ] **Step 4: Commit** — `git add "<path>"` && `git commit -m "feat(java): galho 9 nota 01 — O que é Spring MVC (a camada web sobre o container)"`

### Task 2: Nota 02 — @RestController e os mapeamentos

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Web e APIs REST/02 - @RestController e os mapeamentos.md`

- [ ] **Step 1: Pesquisar** — WebFetch `https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-controller/ann-requestmapping.html`. CONFIRMAR: `@RestController` = `@Controller` + `@ResponseBody`; `@RequestMapping` e os atalhos por verbo; atributos `path`/`method`/`params`/`headers`/`produces`/`consumes`.

- [ ] **Step 2: Escrever** — `fase: iniciado`, tags `[java, web, iniciado, controller, rest]`. Conteúdo:
  - TL;DR: `@RestController` marca a classe como handler REST (= `@Controller` + `@ResponseBody`); `@GetMapping`/`@PostMapping`/... mapeiam métodos a URLs+verbos.
  - H3s (≥3 não obrigatório em iniciado, mas usar): "`@Controller` vs `@RestController` (view vs body)", "`@RequestMapping` e os atalhos por verbo HTTP", "Atributos: `path`, `method`, `produces`/`consumes`, `params`/`headers`".
  - `## Na prática` — `@RestController @RequestMapping("/orders")` com `@GetMapping`/`@PostMapping` (```java).
  - `## Armadilhas` — ≥2: (1) esquecer `@ResponseBody` num `@Controller` puro (Spring tenta resolver uma view); (2) dois métodos com o mesmo mapeamento (ambiguidade); (3) `@PostMapping` sem `consumes` aceitando qualquer content-type.
  - `## Veja também` — [[01 - O que é Spring MVC — a camada web sobre o container]], [[03 - Recebendo dados da request]], **[[03-Dominios/Tecnologia/Java/Jakarta EE/07 - JAX-RS — REST declarativo|JAX-RS]]** (resource methods da spec), **[[03-Dominios/Tecnologia/Java/Spring Core e Boot/03 - Beans e estereótipos — @Component, @Service, @Repository, @Controller|Beans e estereótipos]]** (o controller é um estereótipo/bean), verbetes `@RestController`/`@RequestMapping`/`@GetMapping / @PostMapping (mapeamentos HTTP)`.

- [ ] **Step 3: Verificar** — ≥7 seções; anti-fabricação VAZIO; sem `[[` pra Galho 10-17; link JAX-RS + Galho 8 presentes.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 9 nota 02 — @RestController e os mapeamentos"`

### Task 3: Nota 03 — Recebendo dados da request

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Web e APIs REST/03 - Recebendo dados da request.md`

- [ ] **Step 1: Pesquisar** — WebFetch `https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-controller/ann-methods/arguments.html`. CONFIRMAR: `@PathVariable`, `@RequestParam` (`required`/`defaultValue`), `@RequestBody`, `@RequestHeader`, `@RequestPart`.

- [ ] **Step 2: Escrever** — `fase: iniciado`, tags `[java, web, iniciado, controller]`. Conteúdo:
  - TL;DR: o handler recebe dados da request por anotações — `@PathVariable` (segmento da URL), `@RequestParam` (query/form), `@RequestBody` (corpo JSON desserializado), `@RequestHeader`.
  - H3s: "Path e query: `@PathVariable` e `@RequestParam` (`required`/`defaultValue`)", "Corpo: `@RequestBody` (desserialização via converter)", "Headers e multipart: `@RequestHeader`, `@RequestPart`".
  - `## Na prática` — `GET /orders/{id}` com `@PathVariable` + `POST /orders` com `@RequestBody` record (```java).
  - `## Armadilhas` — ≥2: (1) `@RequestParam` obrigatório sem `defaultValue` → 400 quando ausente; (2) nome do `{id}` ≠ nome do parâmetro (precisa `@PathVariable("id")`); (3) `@RequestBody` num GET (sem corpo).
  - `## Veja também` — [[02 - @RestController e os mapeamentos]], [[05 - Serialização JSON com Jackson]], **[[03-Dominios/Tecnologia/Java/Jakarta EE/07 - JAX-RS — REST declarativo|JAX-RS]]** (`@PathParam`/`@QueryParam` — os params tipados da spec), verbetes `@PathVariable`/`@RequestParam`/`@RequestBody`/`@RequestHeader`.

- [ ] **Step 3: Verificar** — ≥7 seções; anti-fabricação VAZIO; link JAX-RS presente.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 9 nota 03 — recebendo dados da request"`

### Task 4: Nota 04 — ResponseEntity e status codes

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Web e APIs REST/04 - ResponseEntity e status codes.md`

- [ ] **Step 1: Pesquisar** — WebFetch `https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-controller/ann-methods/responseentity.html`. CONFIRMAR: `ResponseEntity<T>` (status+headers+body), `@ResponseStatus`, factory methods (`ok`/`created`/`noContent`).

- [ ] **Step 2: Escrever** — `fase: iniciado`, tags `[java, web, iniciado, rest]`. Conteúdo:
  - TL;DR: a resposta HTTP se monta com `ResponseEntity<T>` (status + headers + body) ou `@ResponseStatus`; usar o status code certo é parte do contrato REST (201 + `Location` no create, 204 no delete, 4xx pra erro de cliente).
  - H3s: "`ResponseEntity<T>`: status + headers + body", "`@ResponseStatus` (declarativo)", "O catálogo de status (200/201+`Location`/204/400/404/409/422/500)".
  - `## Na prática` — `ResponseEntity.created(uri).body(...)` no POST, `noContent()` no DELETE (```java).
  - `## Armadilhas` — ≥2: (1) "200 pra tudo" (inclusive erro); (2) 201 sem header `Location`; (3) 200 num delete que devia ser 204; (4) status code no corpo em vez do header.
  - `## Veja também` — [[02 - @RestController e os mapeamentos]], [[09 - Tratamento de exceções com @ControllerAdvice]] (status de erro), verbetes `@ResponseStatus`/`@ResponseBody`.

- [ ] **Step 3: Verificar** — ≥7 seções; anti-fabricação VAZIO.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 9 nota 04 — ResponseEntity e status codes"`

### Task 5: Nota 05 — Serialização JSON com Jackson

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Web e APIs REST/05 - Serialização JSON com Jackson.md`

- [ ] **Step 1: Pesquisar** — WebFetch `https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-controller/ann-methods/responsebody.html` (message converters). CONFIRMAR: `MappingJackson2HttpMessageConverter` como default; `JavaTimeModule` registrado por padrão no Boot; anotações Jackson principais.

- [ ] **Step 2: Escrever** — `fase: iniciado`, tags `[java, web, iniciado, json]`. Conteúdo:
  - TL;DR: o Spring serializa o retorno do handler em JSON via Jackson (`MappingJackson2HttpMessageConverter`); **exponha DTOs, não entidades JPA**.
  - H3s: "`@ResponseBody` e o converter Jackson padrão", "Anotações Jackson (`@JsonProperty`, `@JsonIgnore`, `@JsonInclude`, `@JsonFormat`)", "**DTO vs entidade**: por que não vazar a entidade JPA (lazy/ciclos/over-exposure — Galho 10, planejado)", "Datas: `JavaTimeModule` e ISO-8601".
  - `## Na prática` — entidade `Order` → record `OrderDto` serializado; `@JsonInclude(NON_NULL)` (```java).
  - `## Armadilhas` — ≥2: (1) serializar entidade JPA direto (`LazyInitializationException`, ciclos, vazamento de campos); (2) data sem formato ISO; (3) expor campo sensível por falta de DTO.
  - `## Veja também` — [[04 - ResponseEntity e status codes]], [[07 - Content negotiation]], verbetes `Jackson`/`HttpMessageConverter`. (Entidade/JPA → Galho 10, planejado — texto.)

- [ ] **Step 3: Verificar** — ≥7 seções; anti-fabricação VAZIO; sem `[[` pra Galho 10.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 9 nota 05 — serialização JSON com Jackson"`

---

## Fase ADEPTO (notas 06-12)

### Task 6: Nota 06 — O pipeline do DispatcherServlet ⟦opus⟧

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Web e APIs REST/06 - O pipeline do DispatcherServlet.md`

- [ ] **Step 1: Pesquisar** — WebFetch `https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-servlet.html` (+ `.../mvc-servlet/special-bean-types.html` e `.../mvc-servlet/handlermapping-interceptor.html`). CONFIRMAR a sequência: `HandlerMapping` → interceptor `preHandle` → `HandlerAdapter` → argument resolver → handler → return value handler → `HttpMessageConverter` → `postHandle`/`afterCompletion`; `HandlerExceptionResolver`. Refinar do tronco `### O pipeline`/`### DispatcherServlet`/`### HandlerMapping`/`### HandlerAdapter`/`### HttpMessageConverter`, higienizando.

- [ ] **Step 2: Escrever** — `fase: adepto`, tags `[java, web, adepto, spring-mvc]`. **A nota mais densa do galho.** ≥3 H3s: "O caminho do request (`doDispatch`): mapping → adapter → handler → converter (diagrama ```text)", "`HandlerMapping` (`RequestMappingHandlerMapping`) e `HandlerAdapter`", "`HandlerMethodArgumentResolver` e `ReturnValueHandler` (como `@RequestBody`/`@PathVariable` viram args)", "Tratamento de exceção no pipeline (`HandlerExceptionResolver` — liga à 09)". **O `DispatcherServlet` É um servlet** (Galho 7 nota 03), registrado pelo embedded server e bean do contexto (Galho 8 nota 16). `## Na prática`: um `HandlerInterceptor` simples mostrando os pontos do pipeline (```java). `## Armadilhas` ≥3: achar que o controller é "chamado direto" (há a engrenagem toda); confundir filter (antes do dispatcher) com interceptor (dentro); assumir uma instância por request (o servlet é singleton multi-thread — Galho 7). `## Veja também` — [[01 - O que é Spring MVC — a camada web sobre o container]], [[11 - Interceptors vs Filters]], **[[03-Dominios/Tecnologia/Java/Jakarta EE/03 - Servlet API — o alicerce HTTP|Servlet API]]** (a spec por baixo), **[[03-Dominios/Tecnologia/Java/Spring Core e Boot/16 - SpringApplication e o embedded server|SpringApplication e o embedded server]]** (quem registra o dispatcher), verbetes `DispatcherServlet`/`HandlerMapping`/`HandlerAdapter`/`front controller`.

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; link Servlet API 03 + Galho 8 16 presentes; anti-fabricação VAZIO.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 9 nota 06 — o pipeline do DispatcherServlet"`

### Task 7: Nota 07 — Content negotiation

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Web e APIs REST/07 - Content negotiation.md`

- [ ] **Step 1: Pesquisar** — WebFetch `https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-config/content-negotiation.html` + `.../mvc-controller/ann-methods/responsebody.html`. CONFIRMAR: `Accept` header como estratégia default; `ContentNegotiationStrategy`; path-extension **desativada por padrão** (segurança, desde 5.3); 406/415.

- [ ] **Step 2: Escrever** — `fase: adepto`, tags `[java, web, adepto, json]`. ≥3 H3s: "Como o Spring escolhe a representação (`Accept`, `produces`)", "`ContentNegotiationStrategy` (header vs param vs path-extension desativada)", "A cadeia de `HttpMessageConverter` e os erros 406/415". `## Na prática`: `produces` no mapping + cliente com `Accept` (```java/```bash). `## Armadilhas` ≥3: depender de path-extension (`.json`) desativada; `produces` que não bate com o `Accept` (406); assumir JSON com XML no classpath. `## Veja também` — [[05 - Serialização JSON com Jackson]], [[06 - O pipeline do DispatcherServlet]], verbetes `content negotiation`/`HttpMessageConverter`.

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; anti-fabricação VAZIO.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 9 nota 07 — content negotiation"`

### Task 8: Nota 08 — Validação na borda

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Web e APIs REST/08 - Validação na borda.md`

- [ ] **Step 1: Pesquisar** — WebFetch `https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-controller/ann-validation.html`. CONFIRMAR: `@Valid` (body → `MethodArgumentNotValidException`) e `@Validated` na classe (params → `ConstraintViolationException`); 400 automático; `BindingResult`.

- [ ] **Step 2: Escrever** — `fase: adepto`, tags `[java, web, adepto, validation]`. ≥3 H3s: "`@Valid` no `@RequestBody` (→ `MethodArgumentNotValidException`)", "`@Validated` na classe pra validar `@PathVariable`/`@RequestParam` (→ `ConstraintViolationException`)", "O 400 automático e o `BindingResult` (tratar manualmente)". **Linka a spec Bean Validation (Galho 7 nota 08 — `@NotBlank`/`@Email`/...) SEM re-explicar** e `@Validated`/config do Galho 8 nota 12. Aqui é só a **integração no controller**. `## Na prática`: record `CreateOrderRequest` com constraints + `@Valid` no controller (```java). `## Armadilhas` ≥3: esquecer `@Valid` (request inválido passa); validar e ignorar o `BindingResult`; `@Validated` na classe esquecido pra params; misturar validação de negócio (service — Galho 10, texto) com validação de formato (borda). `## Veja também` — [[03 - Recebendo dados da request]], [[09 - Tratamento de exceções com @ControllerAdvice]], **[[03-Dominios/Tecnologia/Java/Jakarta EE/08 - Bean Validation|Bean Validation]]** (a spec), **[[03-Dominios/Tecnologia/Java/Spring Core e Boot/12 - Configuração e profiles|Configuração e profiles]]** (`@Validated`), verbete `MethodArgumentNotValidException`.

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; link Bean Validation 08 + Galho 8 12 presentes; sem `[[` pra Galho 10; anti-fabricação VAZIO.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 9 nota 08 — validação na borda"`

### Task 9: Nota 09 — Tratamento de exceções com @ControllerAdvice ⟦opus⟧

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Web e APIs REST/09 - Tratamento de exceções com @ControllerAdvice.md`

- [ ] **Step 1: Pesquisar** — WebFetch `https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-controller/ann-exceptionhandler.html` + `https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-ann-rest-exceptions.html`. CONFIRMAR: `@ExceptionHandler` local vs `@RestControllerAdvice` global; `ResponseEntityExceptionHandler` (handlers built-in). Refinar do tronco `### Exception Handling` (~326-369), **higienizando `PatientController`/`PatientNotFoundException` → `OrderController`/`OrderNotFoundException`**.

- [ ] **Step 2: Escrever** — `fase: adepto`, tags `[java, web, adepto, exception-handling]`. ≥3 H3s: "`@ExceptionHandler` local vs `@RestControllerAdvice` global (padrão recomendado)", "Mapear exceção de domínio → status HTTP", "`ResponseEntityExceptionHandler` (os handlers built-in do Spring) e ordem/especificidade", "Logar sem engolir a stack". **O mecanismo é AOP/proxy** (Galho 8 nota 09 — linkar) e o advice é um bean. Formato da resposta → nota 10. `## Na prática`: `@RestControllerAdvice` com `@ExceptionHandler(OrderNotFoundException.class)` devolvendo `ProblemDetail` (teaser da 10) (```java). `## Armadilhas` ≥3: handler que devolve 200 com erro no body; `catch` que engole a stack (sem log); ordem ambígua de handlers; `@ExceptionHandler` espalhado em vez de centralizado. `## Veja também` — [[04 - ResponseEntity e status codes]], [[10 - Problem Details — RFC 9457]], [[06 - O pipeline do DispatcherServlet]], **[[03-Dominios/Tecnologia/Java/Spring Core e Boot/09 - AOP e proxies no Spring|AOP e proxies]]** (o mecanismo), verbetes `@ControllerAdvice / @RestControllerAdvice`/`@ExceptionHandler`.

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; link AOP 09 (Galho 8) presente; **grep `Patient` VAZIO** (higienizado); anti-fabricação VAZIO.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 9 nota 09 — tratamento de exceções com @ControllerAdvice"`

### Task 10: Nota 10 — Problem Details — RFC 9457

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Web e APIs REST/10 - Problem Details — RFC 9457.md`

- [ ] **Step 1: Pesquisar (CRÍTICO)** — WebFetch `https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-ann-rest-exceptions.html` + `https://datatracker.ietf.org/doc/html/rfc9457`. CONFIRMAR: `ProblemDetail` é Spring Framework 6+; **RFC 9457 obsoletou a 7807**; media type `application/problem+json`; campos `type`/`title`/`status`/`detail`/`instance` + extensões; `spring.mvc.problemdetails.enabled`. **Nota de pesquisa.**

- [ ] **Step 2: Escrever** — `fase: adepto`, tags `[java, web, adepto, problem-details, exception-handling]`. ≥3 H3s: "O formato `application/problem+json` (RFC 9457, que obsoletou a 7807)", "`ProblemDetail` no Spring (Framework 6+): `forStatusAndDetail`, `setType`, `setProperty`", "`ErrorResponse`/`ErrorResponseException` e integração com o `@RestControllerAdvice` (nota 09)". `## Na prática`: `@ExceptionHandler` devolvendo `ProblemDetail` com extensão `errors` (```java) + o JSON resultante (```json). `## Armadilhas` ≥3: formato de erro ad-hoc por endpoint (inconsistente); vazar stack trace/SQL no `detail`; ignorar o `type` URI; reinventar o que o `ProblemDetail` já dá. `## Veja também` — [[09 - Tratamento de exceções com @ControllerAdvice]], [[04 - ResponseEntity e status codes]], verbete `ProblemDetail (RFC 9457)`.

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; `grep -i "9457"` ≥1; anti-fabricação VAZIO.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 9 nota 10 — Problem Details (RFC 9457)"`

### Task 11: Nota 11 — Interceptors vs Filters

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Web e APIs REST/11 - Interceptors vs Filters.md`

- [ ] **Step 1: Pesquisar** — WebFetch `https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-config/interceptors.html` + `https://docs.spring.io/spring-framework/reference/web/webmvc-cors.html`. CONFIRMAR: `HandlerInterceptor` (`preHandle`/`postHandle`/`afterCompletion`) vs Servlet `Filter`/`FilterRegistrationBean`; CORS como config MVC. Refinar do tronco `### Interceptors vs Filters` (~292-324), higienizando.

- [ ] **Step 2: Escrever** — `fase: adepto`, tags `[java, web, adepto, spring-mvc]`. ≥3 H3s: "Servlet `Filter`: nível container, antes do `DispatcherServlet`", "`HandlerInterceptor`: dentro do Spring MVC, com o handler method (`preHandle`/`postHandle`/`afterCompletion`)", "Quando usar cada (filter pra encoding/CORS/log cru; interceptor pra lógica que precisa do handler) e ordem". **CORS** citado como config MVC (`@CrossOrigin`/`CorsRegistry`); **auth/segurança = Galho 12 (planejado, texto)**. Linka **Servlet filters do Galho 7 nota 03** (a spec). `## Na prática`: `HandlerInterceptor` (MDC/traceId) + registro via `WebMvcConfigurer` (```java). `## Armadilhas` ≥3: pôr lógica que precisa do handler num filter; interceptor pra coisa que devia ser filter (encoding); esquecer `afterCompletion` (limpeza de MDC vaza). `## Veja também` — [[06 - O pipeline do DispatcherServlet]], **[[03-Dominios/Tecnologia/Java/Jakarta EE/03 - Servlet API — o alicerce HTTP|Servlet API]]** (a spec dos filters), verbete `HandlerInterceptor`. (Auth/CSRF → Galho 12, planejado — texto.)

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; link Servlet API 03 presente; sem `[[` pra Galho 12; anti-fabricação VAZIO.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 9 nota 11 — interceptors vs filters"`

### Task 12: Nota 12 — Documentando a API com OpenAPI e Swagger

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Web e APIs REST/12 - Documentando a API com OpenAPI e Swagger.md`

- [ ] **Step 1: Pesquisar (CRÍTICO)** — WebFetch `https://springdoc.org/`. CONFIRMAR: **springdoc-openapi** é a lib mantida (Spring Boot 3 → `springdoc-openapi-starter-webmvc-ui`); **springfox está legado/morto**; geração automática dos controllers; `/v3/api-docs` e `/swagger-ui.html`; anotações `@Operation`/`@Schema`/`@ApiResponse`. **Nota de pesquisa.**

- [ ] **Step 2: Escrever** — `fase: adepto`, tags `[java, web, adepto, openapi]`. ≥3 H3s: "OpenAPI (a spec do contrato) vs Swagger UI (a interface)", "springdoc-openapi: o starter, `/v3/api-docs`, `/swagger-ui.html` (e por que **não** springfox)", "Anotando quando o automático não basta (`@Operation`, `@Parameter`, `@Schema`, `@ApiResponse`)". `## Na prática`: dependência `springdoc-openapi-starter-webmvc-ui` + `@Operation` num endpoint (```xml/```java). `## Armadilhas` ≥3: usar springfox (abandonado); achar que precisa anotar tudo (muito é inferido); expor o swagger-ui em produção sem pensar (→ Galho 12, texto); doc escrita à mão que desatualiza. `## Veja também` — [[02 - @RestController e os mapeamentos]], [[13 - Versionamento de API]], verbetes `OpenAPI`/`springdoc-openapi`/`Swagger UI`.

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; `grep -i "springdoc"` ≥1; anti-fabricação VAZIO.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 9 nota 12 — documentando a API com OpenAPI/Swagger"`

---

## Fase MAGUS (notas 13-16)

### Task 13: Nota 13 — Versionamento de API

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Web e APIs REST/13 - Versionamento de API.md`

- [ ] **Step 1: Pesquisar** — WebFetch `https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-controller/ann-requestmapping.html` (procurar `version`) + guias de API design. CONFIRMAR: as 4 estratégias (URI path, request param, custom header, media-type); o atributo `version` em `@RequestMapping` é **Framework 7.0** (citar como "mais recente", não baseline); headers `Deprecation`/`Sunset`. **Nota de pesquisa** (sem estatística inventada). **Nota:** se a doc não trouxer o tema diretamente no baseline 6.x, fundar em conceito de REST design citando a fonte; **não inventar**.

- [ ] **Step 2: Escrever** — `fase: magus`, tags `[java, web, magus, versioning]`. ≥3 H3s: "Por que versionar (contrato com clientes que não atualizam juntos)", "As 4 estratégias: URI path / request param / custom header / media-type (content negotiation)", "Trade-offs (visibilidade, cache, roteamento, REST-purismo) e deprecação (`Deprecation`/`Sunset`)". `## Na prática`: o mesmo recurso em `/v1/orders` e via `Accept: application/vnd.company.v2+json` (```java/```bash). `## Armadilhas` ≥3: nunca versionar e quebrar clientes; versionar cedo demais; misturar estratégias; "v2" que muda semântica sem avisar. `## Veja também` — [[02 - @RestController e os mapeamentos]], [[07 - Content negotiation]], [[12 - Documentando a API com OpenAPI e Swagger]], verbete `API versioning`.

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; anti-fabricação VAZIO; sem estatística inventada (revisar manualmente).

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 9 nota 13 — versionamento de API"`

### Task 14: Nota 14 — HATEOAS

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Web e APIs REST/14 - HATEOAS.md`

- [ ] **Step 1: Pesquisar** — WebFetch `https://docs.spring.io/spring-hateoas/docs/current/reference/html/` + Richardson Maturity Model (martinfowler.com). CONFIRMAR: `EntityModel`/`Link`/`WebMvcLinkBuilder`; HAL (`application/hal+json`); os 4 níveis (0-3). **Nota de pesquisa** (sem estatística inventada; honesto sobre adoção real).

- [ ] **Step 2: Escrever** — `fase: magus`, tags `[java, web, magus, hateoas, rest]`. ≥3 H3s: "Hypermedia as the engine of application state — a ideia", "Richardson Maturity Model (0 RPC → 1 recursos → 2 verbos → 3 hypermedia)", "Spring HATEOAS (`EntityModel`, `Link`, `WebMvcLinkBuilder`, HAL)", "Quando (não) usar — o custo vs o benefício (honesto)". `## Na prática`: `EntityModel<OrderDto>` com `linkTo(methodOn(...))` (```java) + JSON HAL (```json). `## Armadilhas` ≥3: confundir "REST" com nível 2 (a maioria); adicionar links que ninguém consome (custo sem benefício); achar HATEOAS obrigatório pra ser REST. `## Veja também` — [[04 - ResponseEntity e status codes]], [[13 - Versionamento de API]], verbetes `HATEOAS`/`Spring HATEOAS`/`Richardson Maturity Model`.

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; anti-fabricação VAZIO; sem estatística inventada.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 9 nota 14 — HATEOAS"`

### Task 15: Nota 15 — Clientes HTTP — RestClient, WebClient, RestTemplate ⟦opus⟧

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Web e APIs REST/15 - Clientes HTTP — RestClient, WebClient, RestTemplate.md`

- [ ] **Step 1: Pesquisar (CRÍTICO)** — WebFetch `https://docs.spring.io/spring-framework/reference/integration/rest-clients.html`. CONFIRMAR: **`RestClient` é Spring Framework 6.1+** (síncrono, API fluent, default moderno); `RestTemplate` em manutenção (legado, ainda onipresente); `WebClient` é reativo (WebFlux). Timeouts (`ClientHttpRequestFactory`), error handling (`onStatus`). **Nota de pesquisa** (tronco não cobre — grep vazio na Task 0).

- [ ] **Step 2: Escrever** — `fase: magus`, tags `[java, web, magus, http-client]`. ≥3 H3s: "`RestClient` (Framework 6.1+): o default síncrono moderno (API fluent)", "`RestTemplate`: o legado em manutenção (`getForObject`/`exchange`) e a migração pro `RestClient`", "`WebClient`: menção — reativo, do WebFlux (uso reativo/streaming = Galho 11, planejado)", "Timeouts e error handling no cliente (`onStatus`)". **Menção de fronteira:** o cliente declarativo `@FeignClient` (Spring Cloud OpenFeign) — orientado a microservices com service discovery e load balancing — é do **Galho 16 (planejado)**; citar em texto, **sem wikilink**. `## Na prática`: `RestClient.create().get()...retrieve().body(OrderDto.class)` com timeout e `onStatus` (```java). `## Armadilhas` ≥3: `new RestTemplate()` a cada chamada (criar/reusar); sem timeout (thread presa pra sempre); ignorar status de erro do cliente; escolher `WebClient` "porque é novo" num stack imperativo (puxa Reactor — Galho 11). `## Veja também` — [[02 - @RestController e os mapeamentos]], [[05 - Serialização JSON com Jackson]], verbetes `RestClient`/`RestTemplate`/`WebClient`. (WebFlux/Reactor → Galho 11; OpenFeign → Galho 16 — ambos texto, sem wikilink.)

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; `grep "6.1"` ≥1; **sem `[[` pra Galho 11/16** (OpenFeign/WebClient só texto); anti-fabricação VAZIO.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 9 nota 15 — clientes HTTP (RestClient, WebClient, RestTemplate)"`

### Task 16: Nota 16 — Capstone: uma request HTTP de ponta a ponta no Spring MVC ⟦opus⟧

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Web e APIs REST/16 - Capstone — Uma request HTTP de ponta a ponta no Spring MVC.md`

- [ ] **Step 1: Pesquisar** — WebFetch `https://docs.spring.io/spring-framework/reference/web/webmvc.html` (revisar) + `.../mvc-ann-rest-exceptions.html`. Conferir a tabela Spring MVC↔spec Jakarta com as notas dos Galhos 7/8 já escritas.

- [ ] **Step 2: Escrever** — `fase: magus`, tags `[java, web, magus, spring-mvc, rest]`, aliases `["Capstone Web", "Request HTTP de ponta a ponta"]`. Conteúdo:
  - TL;DR: uma request REST atravessa filter → `DispatcherServlet` → mapping → interceptor → adapter → argument resolver → `@Valid` → controller → `ResponseEntity` → converter; o erro vira `@RestControllerAdvice` → `ProblemDetail`. Projetar uma API é dominar esse caminho.
  - `## O que é` / `## Por que importa`.
  - `## Como funciona` — H3s: "Da request à resposta: o caminho completo (`POST /orders` válida — diagrama ```text)", "O caminho de erro (exceção → `HandlerExceptionResolver` → `@RestControllerAdvice` → `ProblemDetail`)", "**Spring MVC → spec Jakarta** (tabela: `DispatcherServlet`↔Servlet API, `@RestController`↔JAX-RS, `@Valid`↔Bean Validation, `HandlerInterceptor`↔Servlet Filter)".
  - `## Na prática` — `### Checklist REST API production-grade` (status corretos, DTO não-entidade, validação na borda, erro RFC 9457, OpenAPI, versionamento, timeouts no cliente).
  - `## Armadilhas` (de raciocínio) ≥3: "o controller é chamado direto" (há o pipeline); "qualquer 2xx serve"; "validação é só no service" (também na borda); decidir client/versão por hype.
  - `## Em entrevista` (munição: o pipeline, Problem Details, versionamento) + `### Cheatsheet` (nota→problema) + `## Veja também` (notas-chave do galho + **[[03-Dominios/Tecnologia/Java/Jakarta EE/07 - JAX-RS — REST declarativo|JAX-RS]]** + **[[03-Dominios/Tecnologia/Java/Spring Core e Boot/index|Spring Core e Boot]]** + MOC galho/central) + `## Referências`.

- [ ] **Step 3: Verificar** — ≥7 seções; tabela Spring↔Jakarta presente (`grep -iE "Servlet|JAX-RS|Bean Validation"`); link Galho 7 + Galho 8 presentes; anti-fabricação VAZIO; sem estatística inventada (revisar manualmente).

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 9 nota 16 — capstone (request HTTP de ponta a ponta)"`

---

## Task 17: MOC do galho

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Web e APIs REST/index.md`

- [ ] **Step 1: Escrever** — modelar pelo `03-Dominios/Tecnologia/Java/Spring Core e Boot/index.md`. Frontmatter: `type: moc`, `status: growing`, `publish: true`, `title: "Web e APIs REST"`, tags `[java, web, moc]`, aliases `["Web e APIs REST", "Spring MVC", "REST API", "Galho 9 - Web"]`, `created`/`updated: 2026-06-08`. Conteúdo:
  - TL;DR — Galho 9; a camada web sobre o container do Galho 8: Spring MVC e o pipeline do `DispatcherServlet`, REST controllers, content negotiation, validação na borda, erro com Problem Details, OpenAPI, HATEOAS, versionamento e clientes HTTP; 16 notas em 3 fases.
  - `## Sobre este galho` — escopo + audiência + **galho híbrido** (refator parcial da seção MVC do tronco `Spring Boot.md` + pesquisa) + **dupla fronteira** (implementa specs do Galho 7; roda sobre o container do Galho 8; Galhos 10/11/12/13/16/17 planejados, texto).
  - `## Iniciado` (01-05) / `## Adepto` (06-12) / `## Magus` (13-16) — wikilinks + 1 linha cada.
  - `## Rotas alternativas` — 5: **Completa** (01→16); **Entrevista internacional** (01→06→08→09→10→13→16); **O pipeline desmontado** (01→06→07→11→16); **Projetando uma REST API production-grade** (02→04→05→08→09→10→12→13); **Spring MVC sobre Jakarta EE** (01→06→02→08→11 + Galho 7).
  - `## Todas as notas` — Dataview (`FROM "03-Dominios/Tecnologia/Java/Web e APIs REST"`, `WHERE type = "concept"`).
  - `## Veja também` — MOC central, **[[03-Dominios/Tecnologia/Java/Spring Core e Boot/index|Spring Core e Boot]]** (o container), **[[03-Dominios/Tecnologia/Java/Jakarta EE/index|Jakarta EE]]** (as specs HTTP), Galho 1 (Annotations), Dicionário; Galhos 10-17 como texto "(planejado)" SEM wikilink.

- [ ] **Step 2: Verificar**
```bash
grep -cE "^## (Iniciado|Adepto|Magus|Rotas alternativas)" "03-Dominios/Tecnologia/Java/Web e APIs REST/index.md"
grep -c "\[\[" "03-Dominios/Tecnologia/Java/Web e APIs REST/index.md"
grep -E "\[\[[^]]*(Galho (10|11|12|13|16|17))" "03-Dominios/Tecnologia/Java/Web e APIs REST/index.md"
```
Expected: 4 headings; ≥16 wikilinks; **último grep VAZIO**.

- [ ] **Step 3: Commit** — `git add "<path>"` && `git commit -m "feat(java): galho 9 MOC — Web e APIs REST"`

---

## Task 18: Expandir o Dicionário de Java (NÃO recriar)

**Files:**
- Modify: `03-Dominios/Tecnologia/Java/Dicionário de Java.md`

- [ ] **Step 1: Extrair as âncoras realmente usadas pelas notas**
```bash
grep -rhoE "Dicionário de Java#[^]|]+" "03-Dominios/Tecnologia/Java/Web e APIs REST/" | sort -u
```
A fonte da verdade é o que as notas usaram. Lista esperada (~30): `@ControllerAdvice / @RestControllerAdvice`, `@ExceptionHandler`, `@GetMapping / @PostMapping (mapeamentos HTTP)`, `@PathVariable`, `@RequestBody`, `@RequestHeader`, `@RequestMapping`, `@RequestParam`, `@ResponseBody`, `@ResponseStatus`, `@RestController`, `API versioning`, `content negotiation`, `DispatcherServlet`, `front controller`, `HandlerAdapter`, `HandlerInterceptor`, `HandlerMapping`, `HATEOAS`, `HttpMessageConverter`, `Jackson`, `MethodArgumentNotValidException`, `OpenAPI`, `ProblemDetail (RFC 9457)`, `RestClient`, `RestTemplate`, `Richardson Maturity Model`, `Spring HATEOAS`, `Spring MVC`, `springdoc-openapi`, `Swagger UI`, `WebClient`.

- [ ] **Step 2: Ler o Dicionário e conferir duplicatas** — formato `### Termo` + 1-3 linhas + `Veja também:`. **NÃO recriar/reordenar.** **Conferir verbetes já existentes pra NÃO duplicar** e **linkar entre si** quando adjacentes: `@RestController` ↔ `@Component / estereótipos Spring` (Galho 8); `MethodArgumentNotValidException`/validação web ↔ `Bean Validation (Jakarta Validation)` e `@Validated` (Galhos 7/8); `DispatcherServlet`/`front controller` ↔ `Servlet`/`Servlet API` (Galho 7, se existir). Conferir com:
```bash
grep -nE "^### (Bean Validation|@Validated|Servlet|@Component|@ResponseBody|Jackson)" "03-Dominios/Tecnologia/Java/Dicionário de Java.md"
```

- [ ] **Step 3: Inserir em ordem alfabética** (case-insensitive, sem acento; verbetes iniciados em `@` entram na seção da letra seguinte — conferir o padrão do arquivo). Cada verbete: heading EXATO da âncora + definição fiel às notas + `Veja também:` pra nota canônica (Spring MVC/DispatcherServlet/front controller→01/06; `@RestController`/`@RequestMapping`/mapeamentos→02; `@PathVariable`/`@RequestParam`/`@RequestBody`/`@RequestHeader`→03; `@ResponseStatus`/`@ResponseBody`→04; Jackson/HttpMessageConverter→05; HandlerMapping/HandlerAdapter→06; content negotiation→07; MethodArgumentNotValidException→08; `@ControllerAdvice`/`@ExceptionHandler`→09; ProblemDetail→10; HandlerInterceptor→11; OpenAPI/springdoc/Swagger UI→12; API versioning→13; HATEOAS/Spring HATEOAS/Richardson→14; RestClient/RestTemplate/WebClient→15). Atualizar `updated: 2026-06-08`.

- [ ] **Step 4: Verificar**
```bash
grep -E "^### (Spring MVC|DispatcherServlet|ProblemDetail|RestClient|content negotiation|@RestController)" "03-Dominios/Tecnologia/Java/Dicionário de Java.md"
grep -cE "^### " "03-Dominios/Tecnologia/Java/Dicionário de Java.md"
```
Expected: novos presentes; contagem subiu ~30 vs baseline (240 → ~270).

- [ ] **Step 5: Commit** — `git add "<path>"` && `git commit -m "feat(java): expande Dicionário de Java com verbetes do galho 9 (Web e APIs REST)"`

---

## Task 19: Ativar o Galho 9 no MOC central

**Files:**
- Modify: `03-Dominios/Tecnologia/Java/index.md`

- [ ] **Step 1: Trocar a linha do item 9** (localizar por conteúdo: `9. Web e APIs REST *(planejado)* — Spring MVC, REST, exception handling, validation, OpenAPI`) por:
```markdown
9. [[03-Dominios/Tecnologia/Java/Web e APIs REST/index|Web e APIs REST]] — Spring MVC e o pipeline do DispatcherServlet, REST controllers, content negotiation, validação na borda, exception handling (@ControllerAdvice, Problem Details), OpenAPI, HATEOAS, versionamento, clientes HTTP
```
Atualizar `updated: 2026-06-08`. Não mexer no resto.

- [ ] **Step 2: Verificar**
```bash
grep -E "Web e APIs REST/index" "03-Dominios/Tecnologia/Java/index.md"
grep -c "planejado" "03-Dominios/Tecnologia/Java/index.md"
```
Expected: wikilink ativo; "planejado" caiu exatamente 1 vs baseline.

- [ ] **Step 3: Commit** — `git add "<path>"` && `git commit -m "feat(java): ativa Galho 9 (Web e APIs REST) no MOC central"`

---

## Task 20: Poda PARCIAL do tronco (`Backend/Spring Boot.md`) — só a seção MVC

**Files:**
- Modify: `03-Dominios/Tecnologia/Java/Backend/Spring Boot.md`

- [ ] **Step 1: Ler o tronco e confirmar o range** (política §9 do roadmap — ler antes de podar)
```bash
grep -nE "^#{2,3} " "03-Dominios/Tecnologia/Java/Backend/Spring Boot.md"
```
Confirmar os limites reais de `## Spring MVC pipeline` (início ~221, fim = imediatamente antes da próxima `## ` — provavelmente `## Configuração e Profiles` callout ou `## Gerenciamento de transações`; **conferir na execução**). **Só esta seção é podada.**

- [ ] **Step 2: Podar `## Spring MVC pipeline`** — substituir TODO o bloco da seção (do heading `## Spring MVC pipeline` até imediatamente antes da próxima `## `) por:
```markdown
## Spring MVC pipeline

> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Tecnologia/Java/Web e APIs REST/index|Web e APIs REST]]. Veja [[03-Dominios/Tecnologia/Java/Web e APIs REST/01 - O que é Spring MVC — a camada web sobre o container|O que é Spring MVC]], [[03-Dominios/Tecnologia/Java/Web e APIs REST/06 - O pipeline do DispatcherServlet|O pipeline do DispatcherServlet]], [[03-Dominios/Tecnologia/Java/Web e APIs REST/07 - Content negotiation|Content negotiation]], [[03-Dominios/Tecnologia/Java/Web e APIs REST/11 - Interceptors vs Filters|Interceptors vs Filters]] e [[03-Dominios/Tecnologia/Java/Web e APIs REST/09 - Tratamento de exceções com @ControllerAdvice|Tratamento de exceções com @ControllerAdvice]] (com [[03-Dominios/Tecnologia/Java/Web e APIs REST/10 - Problem Details — RFC 9457|Problem Details / RFC 9457]]).
```
A fabricação `PatientController`/`PatientNotFoundException` da seção **some** com a substituição (não copiar pras notas).

- [ ] **Step 3: Atualizar `## Veja também` + frontmatter** — adicionar wikilink `[[03-Dominios/Tecnologia/Java/Web e APIs REST/index|Web e APIs REST]]` no "Veja também" do tronco; `updated: 2026-06-08`.

- [ ] **Step 4: Verificar (poda cirúrgica — uma seção só; resto intacto)**
```bash
grep -nE "^## " "03-Dominios/Tecnologia/Java/Backend/Spring Boot.md"
grep -c "Web e APIs REST/index" "03-Dominios/Tecnologia/Java/Backend/Spring Boot.md"
grep -nE "PatientController|PatientNotFoundException" "03-Dominios/Tecnologia/Java/Backend/Spring Boot.md"
grep -nE "^## (Gerenciamento de transações|Spring WebFlux|Spring Cloud|Camadas típicas)" "03-Dominios/Tecnologia/Java/Backend/Spring Boot.md"
```
Expected: o `## Spring MVC pipeline` agora é só callout; ≥1 link "Web e APIs REST" (callout) + 1 no "Veja também"; `PatientController`/`PatientNotFoundException` **só sobram sob `## Camadas típicas`** (`### Bean Validation` ~578 — intacto, não é deste galho) — confirmar que **não** sobrou nenhum dentro do antigo bloco MVC; seções de galhos 10/11/16 **AINDA PRESENTES** (intocadas).

- [ ] **Step 5: Commit** — `git add "03-Dominios/Tecnologia/Java/Backend/Spring Boot.md"` && `git commit -m "refactor(java): poda parcial do tronco Spring Boot — seção MVC migra pro galho 9"`

---

## Task 21: Quitar a dívida reversa (9 ponteiros "Galho 9" → wikilinks)

**Files:**
- Modify: `03-Dominios/Tecnologia/Java/Jakarta EE/03 - Servlet API — o alicerce HTTP.md`
- Modify: `03-Dominios/Tecnologia/Java/Jakarta EE/07 - JAX-RS — REST declarativo.md`
- Modify: `03-Dominios/Tecnologia/Java/Jakarta EE/08 - Bean Validation.md`
- Modify: `03-Dominios/Tecnologia/Java/Jakarta EE/index.md`
- Modify: `03-Dominios/Tecnologia/Java/Spring Core e Boot/index.md`
- Modify: `03-Dominios/Tecnologia/Java/Spring Core e Boot/03 - Beans e estereótipos — @Component, @Service, @Repository, @Controller.md`
- Modify: `03-Dominios/Tecnologia/Java/Spring Core e Boot/16 - SpringApplication e o embedded server.md`
- Modify: `03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/10 - Exceções e tratamento de erros.md`

- [ ] **Step 1: Relocalizar (por conteúdo — linhas podem ter mudado)**
```bash
grep -rn "Galho 9\|planejado" "03-Dominios/Tecnologia/Java/Jakarta EE/03 - Servlet API — o alicerce HTTP.md" "03-Dominios/Tecnologia/Java/Jakarta EE/07 - JAX-RS — REST declarativo.md" "03-Dominios/Tecnologia/Java/Jakarta EE/08 - Bean Validation.md" "03-Dominios/Tecnologia/Java/Jakarta EE/index.md" "03-Dominios/Tecnologia/Java/Spring Core e Boot/index.md" "03-Dominios/Tecnologia/Java/Spring Core e Boot/16 - SpringApplication e o embedded server.md" "03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/10 - Exceções e tratamento de erros.md"
grep -n "Galho 9" "03-Dominios/Tecnologia/Java/Spring Core e Boot/03 - Beans e estereótipos — @Component, @Service, @Repository, @Controller.md"
```

- [ ] **Step 2: Aplicar os wikilinks** — em cada ponteiro, trocar o texto "Galho 9 (planejado)"/"Galho 9, planejado" pelo wikilink, **mantendo natural a frase** e atualizando `updated: 2026-06-08` no frontmatter de cada arquivo tocado:
  - **Servlet API 03 (~24):** `...incluindo o Spring MVC (Galho 9, planejado)...` → `...incluindo o Spring MVC ([[03-Dominios/Tecnologia/Java/Web e APIs REST/01 - O que é Spring MVC — a camada web sobre o container|o DispatcherServlet é um servlet]])...` (a simetria-assinatura: a spec por baixo).
  - **JAX-RS 07 (~24):** `...controllers do Spring são outro caminho... (Galho 9, planejado)` → `...controllers do Spring ([[03-Dominios/Tecnologia/Java/Web e APIs REST/02 - @RestController e os mapeamentos|@RestController]]) são outro caminho para o mesmo problema.`
  - **JAX-RS 07 (~44):** `...comparar abordagens: JAX-RS ... Spring MVC (Galho 9, planejado)...` → wikilink pra `[[03-Dominios/Tecnologia/Java/Web e APIs REST/02 - @RestController e os mapeamentos|Spring MVC]]` (ou MOC do galho).
  - **Bean Validation 08 (~24):** `...O `@Valid` que você vê no Spring MVC é esta mesma spec (Galho 9, planejado)...` → wikilink pra `[[03-Dominios/Tecnologia/Java/Web e APIs REST/08 - Validação na borda|validação na borda no Spring MVC]]`.
  - **Jakarta EE/index (~30):** `...Spring MVC e validação no Spring são do Galho 9 (planejado)...` → wikilink pra `[[03-Dominios/Tecnologia/Java/Web e APIs REST/index|Web e APIs REST]]` (e, pra validação, nota 08).
  - **Spring Core e Boot/index (~32):** `...Spring MVC/Web (Galho 9) é planejado — endpoints, DispatcherServlet e a camada web ficam lá...` → wikilink pra `[[03-Dominios/Tecnologia/Java/Web e APIs REST/index|Web e APIs REST]]`.
  - **Spring Core 03 (~39/47/110/112, 4 ocorrências):** `@Controller`/`@RestController` "detalhado no Galho 9, planejado" → wikilink pra `[[03-Dominios/Tecnologia/Java/Web e APIs REST/02 - @RestController e os mapeamentos|@RestController e os mapeamentos]]` (ou nota 01 pra a citação introdutória). Trocar as 4, mantendo a frase natural.
  - **Spring Core 16 (~144):** `...Tuning profundo de servidor ... Galho 9/17 (planejado)...` → wikilink pra `[[03-Dominios/Tecnologia/Java/Web e APIs REST/06 - O pipeline do DispatcherServlet|o pipeline do DispatcherServlet]]` **mantendo a parte "/17" como texto "(planejado)"** (Galho 17 ainda não existe).
  - **Linguagem 10 (~361):** `...@RestControllerAdvice é o gancho central ... Galho 9 (Web e APIs REST) da trilha. O formato ProblemDetail (RFC 9457)...` → wikilinks pra `[[03-Dominios/Tecnologia/Java/Web e APIs REST/09 - Tratamento de exceções com @ControllerAdvice|@ControllerAdvice]]` **e** `[[03-Dominios/Tecnologia/Java/Web e APIs REST/10 - Problem Details — RFC 9457|Problem Details / RFC 9457]]`.

- [ ] **Step 3: Verificar**
```bash
grep -rn "Galho 9" "03-Dominios/Tecnologia/Java/Jakarta EE/03 - Servlet API — o alicerce HTTP.md" "03-Dominios/Tecnologia/Java/Jakarta EE/07 - JAX-RS — REST declarativo.md" "03-Dominios/Tecnologia/Java/Jakarta EE/08 - Bean Validation.md" "03-Dominios/Tecnologia/Java/Jakarta EE/index.md" "03-Dominios/Tecnologia/Java/Spring Core e Boot/index.md" "03-Dominios/Tecnologia/Java/Spring Core e Boot/03 - Beans e estereótipos — @Component, @Service, @Repository, @Controller.md" "03-Dominios/Tecnologia/Java/Spring Core e Boot/16 - SpringApplication e o embedded server.md" "03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/10 - Exceções e tratamento de erros.md" | grep -v "Web e APIs REST"
```
Expected: **VAZIO** (nenhum "Galho 9 (planejado)" solto sobra; o único "Galho 9" remanescente aceitável é se vier acompanhado do wikilink "Web e APIs REST" — por isso o `grep -v`). Conferir que a parte "/17" do gancho Spring 16 permaneceu como "(planejado)".

- [ ] **Step 4: Commit** — `git add` nominal dos 8 arquivos && `git commit -m "refactor(java): quita dívida reversa do galho 9 — ponteiros Spring MVC viram wikilinks"`

---

## Task 22: Verificação final do galho

**Files:** (somente leitura/verificação)

- [ ] **Step 1: 16 notas + MOC**
```bash
ls "03-Dominios/Tecnologia/Java/Web e APIs REST/" | sort
```
Expected: 01..16 + index.md (17 arquivos).

- [ ] **Step 2: Fases (5/7/4)**
```bash
for f in "03-Dominios/Tecnologia/Java/Web e APIs REST/"[0-9]*.md; do grep -H "^fase:" "$f"; done
```
Expected: 01-05 `iniciado`, 06-12 `adepto`, 13-16 `magus`.

- [ ] **Step 3: Seções obrigatórias (3 por nota)**
```bash
for f in "03-Dominios/Tecnologia/Java/Web e APIs REST/"[0-9]*.md; do echo "$f: $(grep -cE '^## (Em entrevista|Armadilhas|Veja também)' "$f")"; done
```
Expected: 3 em todas.

- [ ] **Step 4: Anti-fabricação + fronteiras (greps decisivos)**
```bash
grep -riE "minha experiência|no meu projeto|josenaldo|Patient|MedEspecialista|market share|% d[ao]s (dev|empresas|projetos)" "03-Dominios/Tecnologia/Java/Web e APIs REST/"
grep -rE "\[\[[^]]*(Galho (10|11|12|13|16|17)|WebFlux|Spring Security|Spring Data|Spring Cloud|OpenFeign|MockMvc|Testcontainers)" "03-Dominios/Tecnologia/Java/Web e APIs REST/"
grep -rn '\[\[#' "03-Dominios/Tecnologia/Java/Web e APIs REST/"
```
Expected: **todos VAZIOS**.

- [ ] **Step 5: Dupla fronteira-assinatura (links de volta aos Galhos 7 e 8 presentes)**
```bash
grep -rl "Jakarta EE/0[378]" "03-Dominios/Tecnologia/Java/Web e APIs REST/" | sort
grep -rl "Spring Core e Boot/" "03-Dominios/Tecnologia/Java/Web e APIs REST/" | sort
```
Expected: notas 01/02/03/06/08/11/16 linkam pra alguma nota do Galho 7 (Servlet/JAX-RS/Bean Validation); notas 01/02/06/08/09 linkam pro Galho 8 (container/AOP/embedded server/config).

- [ ] **Step 6: Frase pronta (1 por nota)**
```bash
for f in "03-Dominios/Tecnologia/Java/Web e APIs REST/"[0-9]*.md; do echo "$f: $(grep -c '### Frase pronta (inglês)' "$f")"; done
```
Expected: 1 em todas.

- [ ] **Step 7: Tronco — poda cirúrgica confirmada**
```bash
grep -c "Migrado para galho próprio" "03-Dominios/Tecnologia/Java/Backend/Spring Boot.md"
grep -nE "^## (Gerenciamento de transações|Spring MVC pipeline|Spring WebFlux|Spring Cloud)" "03-Dominios/Tecnologia/Java/Backend/Spring Boot.md"
git status --short "03-Dominios/Tecnologia/Java/Backend/Spring Data JPA.md" "03-Dominios/Tecnologia/Java/Backend/Kafka/"
```
Expected: ≥6 callouts "Migrado" (5 do Galho 8 + 1 novo do MVC); `## Spring MVC pipeline` presente (agora callout), `## Gerenciamento de transações`/WebFlux/Cloud presentes (intocados); `Spring Data JPA.md`/`Kafka/` **sem modificação**.

- [ ] **Step 8: Skill `verificar-wikilinks`** — rodar na pasta `03-Dominios/Tecnologia/Java/Web e APIs REST/` + conferir os arquivos tocados fora (MOC central, Dicionário, tronco, os 3 arquivos Jakarta EE + 3 Spring Core da dívida reversa, Linguagem 10). Âncoras `Dicionário de Java#...` resolvem 1:1 (cross-check com o grep da Task 18 Step 1). As ~204 quebras legadas da árvore Java NÃO são deste galho — só corrigir o que este galho introduziu. Corrigir e commitar à parte se houver.

- [ ] **Step 9: Resumo de fechamento (sem commit)** — reportar: 16 notas (5/7/4), ~30 verbetes (240→~270), MOC galho + MOC central, **poda parcial cirúrgica** (1 seção MVC migrada, fabricação absorvida; transações/WebFlux/Cloud intactas), **dívida reversa quitada** (9 ponteiros, 8 arquivos), troncos vizinhos intocados (mostrar o grep), wikilinks limpos. Commits locais na `main`; **push manual do usuário; sem deploy**. Atualizar memória [[project_trilha_java]] com Galho 9 completo + fatos cravados (ProblemDetail/RFC 9457 Framework 6+, RestClient 6.1+, springdoc≠springfox, baseline 3.x/6.x).

---

## Self-Review (preenchido na escrita do plano)

**Spec coverage:** Tasks 1-16 ↔ spec §3.1 (16 notas, escopos idênticos, opus 01/06/09/15/16, distribuição 5/7/4); Task 17 ↔ §3.2 (MOC, 5 rotas iguais); Task 18 ↔ §3.3 (~30 verbetes, âncoras 1:1 por grep, dups conferidos/linkados); Task 19 ↔ §3.4 (linha 39); Task 20 ↔ §3.5 (poda parcial — só `## Spring MVC pipeline`; fabricação absorvida; `### Bean Validation` sob Camadas típicas intacto); Task 21 ↔ §3.6 (9 ponteiros, 8 arquivos, mapeamento idêntico, "/17" preservado como texto); Task 0 ↔ §6 (pré-flight, baseline 240, range MVC, clientes ausentes no tronco); Task 22 ↔ §7. Dupla fronteira-assinatura (§4.3.1) garantida por links obrigatórios pros Galhos 7 e 8 nas Tasks 1/2/3/6/8/9/11/16 e pelo grep da Task 22 Step 5; fronteira galhos 10-17 pelo grep da Task 22 Step 4.

**Placeholder scan:** sem TBD/TODO; cada nota tem fonte WebFetch nomeada com URL, frontmatter concreto, H3s, armadilhas mínimas com conteúdo real, tamanho-alvo herdado das convenções. Pontos version-sensitive marcados com "verificar/confirmar" são instruções de verificação WebFetch (parte pesquisa do galho híbrido), não placeholders: `ProblemDetail`/RFC 9457 (Framework 6+), `RestClient` (6.1+), springdoc≠springfox, baseline Boot 3.x/Framework 6.x, atributo `version` em `@RequestMapping` (Framework 7.0). A confirmação dos ranges/linhas do tronco e da dívida reversa (Tasks 0/20/21) é resolução-na-execução por política §9 do roadmap (ler antes de podar/editar).

**Type/naming consistency:** numeração 01-16 idêntica entre tasks, MOC, Dicionário, dívida reversa, poda e cheatsheet da capstone; distribuição 5/7/4 consistente; opus 01/06/09/15/16 marcadas ⟦opus⟧; filenames com em dash (sem `:`/`/` — nota 10 usa `— RFC 9457` e nota 12 usa `OpenAPI e Swagger` pra evitar `/`); mapeamento de link-back Galho 7→nota e Galho 8→nota consistente entre spec §3.1, convenções e Tasks; âncoras do Dicionário extraídas por grep antes de inserir (Task 18) e validadas na Task 22; verbetes adjacentes (`@RestController`↔`@Component`, validação web↔`Bean Validation`/`@Validated`) linkados, não duplicados.
