---
title: "Web e APIs REST"
created: 2026-06-08
updated: 2026-06-11
type: moc
status: growing
publish: true
tags:
  - java
  - web
  - moc
aliases:
  - "Web e APIs REST"
  - "Spring MVC"
  - "REST API"
  - "Galho 9 - Web"
---

# Web e APIs REST

> [!abstract] TL;DR
> Galho 9 da trilha Java Senior: a camada web sobre o container do Galho 8 — Spring MVC e o pipeline do DispatcherServlet, REST controllers, content negotiation, validação na borda, erro com Problem Details, OpenAPI, HATEOAS, versionamento e clientes HTTP; 16 notas em 3 fases.

## Sobre este galho

Este galho cobre **a camada web do Spring** — não o container (Galho 8) nem as specs de baixo nível (Galho 7), mas a superfície onde a aplicação fala HTTP: como o Spring MVC recebe uma requisição, a roteia para o controller certo, serializa a resposta, valida a entrada e comunica erros de forma padronizada. Começa pelo modelo mental (o que é Spring MVC e onde ele se encaixa no container), avança pelos controllers e mapeamentos de endpoint, aprofunda no pipeline interno do DispatcherServlet, percorre validação, tratamento de exceções e Problem Details, e finaliza com os temas de design de API que separam uma implementação ingênua de uma production-grade: OpenAPI, HATEOAS, versionamento e clientes HTTP.

**Audiência primária:** dev senior em preparação para entrevista backend Java internacional — cada nota expõe o "porquê" das decisões de design do Spring MVC, a pergunta que mais cai, e treina o reflexo de reconhecer qual peça do pipeline está em jogo quando algo não funciona como esperado. **Audiência secundária:** o dev que já usa Spring MVC no dia a dia e quer entender o que o `@RestController`/`@RequestMapping`/`@ExceptionHandler` escondem.

Este é um **galho híbrido**: parte refatora o tronco existente `Spring Boot.md` (que cobria os temas de MVC de forma densa e monolítica), parte expande com pesquisa aprofundada nas partes que o tronco tratava de forma rasa (pipeline do DispatcherServlet, content negotiation, Problem Details, HATEOAS). A divisão em notas atômicas garante que cada conceito possa ser estudado e revisado de forma independente.

**Dupla fronteira:** este galho **implementa as specs HTTP do Galho 7** ([[03-Dominios/Java/Jakarta EE/index|Jakarta EE]]) — Servlet API, JAX-RS e Bean Validation — e **roda sobre o container do Galho 8** ([[03-Dominios/Java/Spring Core e Boot/index|Spring Core e Boot]]) — IoC/DI, AOP, auto-configuration. As notas aqui assumem familiaridade com os dois. Persistência/Spring Data ([[03-Dominios/Java/Persistência de dados/index|Persistência de dados]]) e Spring Reativa/WebFlux ([[03-Dominios/Java/Programação Reativa/index|Programação Reativa]]) já estão cobertos; Spring Security é o galho [[03-Dominios/Java/Segurança/index|Segurança]]; Testes no ecossistema Spring é o galho [[03-Dominios/Java/Testes/index|Testes]]; Microservices e Spring Cloud são o galho [[03-Dominios/Java/Microservices e sistemas distribuídos/index|Microservices e sistemas distribuídos]]; cloud-native e produção são o galho [[03-Dominios/Java/Cloud-native e produção/index|Cloud-native e produção (Galho 17)]], sem cobertura neste galho.

## Iniciado

1. [[03-Dominios/Java/Web e APIs REST/01 - O que é Spring MVC — a camada web sobre o container|01 — O que é Spring MVC]] — visão panorâmica: o que é Spring MVC, como ele se posiciona sobre o container do Galho 8 e sob as specs do Galho 7, e o modelo mental que orienta todo o resto do galho.
2. [[03-Dominios/Java/Web e APIs REST/02 - @RestController e os mapeamentos|02 — @RestController e os mapeamentos]] — a anatomia de um controller REST: `@RestController` como composição de `@Controller` + `@ResponseBody`, os mapeamentos de método (`@GetMapping`, `@PostMapping` etc.) e as variantes de `@RequestMapping`.
3. [[03-Dominios/Java/Web e APIs REST/03 - Recebendo dados da request|03 — Recebendo dados da request]] — as formas de extrair dados de uma requisição HTTP: `@PathVariable`, `@RequestParam`, `@RequestHeader`, `@CookieValue` e `@RequestBody`, com os conversores e binders por trás.
4. [[03-Dominios/Java/Web e APIs REST/04 - ResponseEntity e status codes|04 — ResponseEntity e status codes]] — como controlar a resposta HTTP com precisão: `ResponseEntity`, `@ResponseStatus`, status codes semânticos e os padrões REST que entrevistadores esperam que você saiba justificar.
5. [[03-Dominios/Java/Web e APIs REST/05 - Serialização JSON com Jackson|05 — Serialização JSON com Jackson]] — o papel do Jackson na serialização/desserialização de JSON: `ObjectMapper`, anotações fundamentais (`@JsonProperty`, `@JsonIgnore`, `@JsonFormat`), customização de conversores e as armadilhas mais comuns.

## Adepto

6. [[03-Dominios/Java/Web e APIs REST/06 - O pipeline do DispatcherServlet|06 — O pipeline do DispatcherServlet]] — o coração do Spring MVC: como o `DispatcherServlet` coordena `HandlerMapping`, `HandlerAdapter`, `MessageConverter` e `ViewResolver` do recebimento da request até a escrita da response.
7. [[03-Dominios/Java/Web e APIs REST/07 - Content negotiation|07 — Content negotiation]] — como o Spring MVC escolhe o formato da resposta: o algoritmo de negociação, `Accept` header, sufixos de URL, `HttpMessageConverter`, e as decisões de design que levaram ao deprecamento de path extensions.
8. [[03-Dominios/Java/Web e APIs REST/08 - Validação na borda|08 — Validação na borda]] — Bean Validation (Jakarta) integrado ao Spring MVC: `@Valid` vs `@Validated`, as anotações de constraint, grupos de validação, `BindingResult` e como expor erros de validação de forma consistente.
9. [[03-Dominios/Java/Web e APIs REST/09 - Tratamento de exceções com @ControllerAdvice|09 — Tratamento de exceções com @ControllerAdvice]] — o modelo centralizado de tratamento de exceções: `@ControllerAdvice`, `@ExceptionHandler`, `ResponseEntityExceptionHandler`, e a hierarquia de resolução de handlers de exceção.
10. [[03-Dominios/Java/Web e APIs REST/10 - Problem Details — RFC 9457|10 — Problem Details (RFC 9457)]] — o padrão de resposta de erro estruturado: a spec RFC 9457, o suporte nativo do Spring 6 (`ProblemDetail`, `ErrorResponse`), e como ele se integra com o `@ControllerAdvice` para respostas de erro padronizadas.
11. [[03-Dominios/Java/Web e APIs REST/11 - Interceptors vs Filters|11 — Interceptors vs Filters]] — os dois mecanismos de cross-cutting na camada web: `Filter` (Servlet API, fora do contexto Spring) vs. `HandlerInterceptor` (Spring MVC, dentro do contexto), quando usar cada um e as implicações de ciclo de vida.
12. [[03-Dominios/Java/Web e APIs REST/12 - Documentando a API com OpenAPI e Swagger|12 — Documentando a API com OpenAPI e Swagger]] — geração e curadoria de documentação de API: springdoc-openapi, anotações OpenAPI 3, Swagger UI, e as boas práticas que separam uma documentação que ajuda de uma que atrapalha.

## Magus

13. [[03-Dominios/Java/Web e APIs REST/13 - Versionamento de API|13 — Versionamento de API]] — as estratégias de versionamento (URI, header, content type, query param), seus trade-offs, e o que arquitetos sênior esperam que você saiba defender em entrevista ou design review.
14. [[03-Dominios/Java/Web e APIs REST/14 - HATEOAS|14 — HATEOAS]] — Hypermedia as the Engine of Application State: o princípio, a implementação com Spring HATEOAS (`Link`, `EntityModel`, `CollectionModel`), HAL e quando o HATEOAS vale o custo de complexidade.
15. [[03-Dominios/Java/Web e APIs REST/15 - Clientes HTTP — RestClient, WebClient, RestTemplate|15 — Clientes HTTP (RestClient, WebClient, RestTemplate)]] — os três clientes HTTP do ecossistema Spring: `RestTemplate` (legado), `WebClient` (reativo, bloqueável) e `RestClient` (novo, fluente, Spring 6.1+), com critérios de escolha e os padrões de resiliência que os acompanham.
16. [[03-Dominios/Java/Web e APIs REST/16 - Capstone — Uma request HTTP de ponta a ponta no Spring MVC|16 — Capstone: request HTTP de ponta a ponta]] — capstone do galho: o percurso completo de uma requisição HTTP desde o socket TCP até o JSON na response, passando por Filters, DispatcherServlet, HandlerMapping, conversão de dados, validação, execução do controller, tratamento de exceções e serialização — o mapa integrado de tudo que o galho cobriu.

## Rotas alternativas

### Completa

01 → 02 → 03 → 04 → 05 → 06 → 07 → 08 → 09 → 10 → 11 → 12 → 13 → 14 → 15 → 16. Percurso linear do modelo mental à capstone — recomendado para quem está construindo a base Spring MVC do zero ou quer cobertura total para entrevista.

### Entrevista internacional

01 → 06 → 08 → 09 → 10 → 13 → 16. Modelo mental, pipeline interno (o que o entrevistador testa em senior), validação (onipresente em qualquer API), tratamento de exceções, Problem Details (diferencial de senioridade), versionamento (design de API) e a capstone integradora.

### O pipeline desmontado

01 → 06 → 07 → 11 → 16. A trilha dos mecanismos internos: modelo mental do Spring MVC, o pipeline do DispatcherServlet em detalhe, content negotiation, a diferença entre Filters e Interceptors, e a capstone que amarra tudo — o percurso para quem quer entender o que está por baixo das anotações.

### Projetando uma REST API production-grade

02 → 04 → 05 → 08 → 09 → 10 → 12 → 13. A trilha de design: controllers e mapeamentos, controle preciso da response, serialização JSON, validação na borda, tratamento centralizado de exceções, Problem Details, documentação OpenAPI e estratégias de versionamento — tudo que uma API madura precisa ter.

### Spring MVC sobre Jakarta EE (a ponte com o Galho 7)

01 → 06 → 02 → 08 → 11 + notas do Galho 7 (Servlet API, JAX-RS, Bean Validation). O percurso para quem vem do Galho 7 e quer mapear Jakarta EE no Spring MVC: onde o `DispatcherServlet` se encaixa no modelo Servlet, como os `@RequestMapping` se relacionam com JAX-RS, como Bean Validation é integrado, e onde Filters (Servlet) terminam e Interceptors (Spring) começam.

## Todas as notas

```dataview
TABLE fase, status FROM "03-Dominios/Java/Web e APIs REST" WHERE type = "concept" SORT file.name ASC
```

## Veja também

- [[03-Dominios/Java/index|Trilha Java]] (MOC central)
- [[03-Dominios/Java/Spring Core e Boot/index|Spring Core e Boot]] — o container — Galho 8
- [[03-Dominios/Java/Jakarta EE/index|Jakarta EE]] — as specs HTTP — Galho 7
- [[03-Dominios/Java/Linguagem e sintaxe moderna/11 - Annotations|Annotations]] — Galho 1
- [[03-Dominios/Java/Dicionário de Java|Dicionário de Java]]

> Galhos 10 (Persistência/Spring Data), 11 (Spring Reativa/WebFlux), 12 (Spring Security), 13 (Testes no ecossistema Spring), 16 (Microservices) e 17 (Spring Cloud) — planejados.
