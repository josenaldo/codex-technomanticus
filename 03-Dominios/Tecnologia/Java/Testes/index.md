---
title: "Testes"
created: 2026-06-11
updated: 2026-06-11
type: moc
status: growing
publish: true
tags:
  - java
  - testes
  - moc
aliases:
  - "Testes"
  - "Testes em Java"
  - "Testing"
  - "Galho 13 - Testes"
---

# Testes

> [!abstract] TL;DR
> O **Galho 13** é a disciplina que testa os Galhos 1-12: **JUnit 5**, **AssertJ** e **Mockito** como o tripé do teste unitário, os **slices do Spring** (`@WebMvcTest`, `@DataJpaTest`) e os **Testcontainers** para integração com infra real, testes de **segurança**, **assíncrono** e **reativo**, e o que vem depois do verde — **mutation testing**, **performance**, **fitness functions** e **contratos**. São **21 notas** em 3 fases (Iniciado, Adepto, Magus).

## Sobre este galho

Testar é a engenharia de provar que o código faz o que diz — e de proteger essa prova contra a próxima mudança. Este galho parte da **pirâmide de testes** e do stack moderno, percorre o tripé unitário (JUnit 5, AssertJ, Mockito), sobe pros **slices do Spring** que carregam só a fatia do contexto que cada teste precisa, integra com infra real via **Testcontainers**, cobre as fronteiras difíceis (segurança, código assíncrono, reativo, HTTP externo) e fecha indo **além do verde**: testes que questionam a qualidade da própria suíte (mutation testing), a performance (JMH), a arquitetura (ArchUnit) e os contratos entre serviços (Pact), com um capstone de estratégia de testes production-grade.

**Audiência primária:** dev pleno/sênior que vai encarar **entrevista internacional de backend Java/Spring** e precisa explicar a pirâmide, os slices e o que mockar (e o que não mockar) com critério. **Secundária:** quem desenha a estratégia de testes de uma app Spring e precisa decidir entre unitário e integração, mock e infra real, cobertura de linha e cobertura honesta.

É um **galho híbrido**: combina a **poda integral do tronco** `Testes em Java.md` (a nota monolítica antiga, agora dissolvida em notas atômicas) com **pesquisa version-specific** nas docs do JUnit 5, Mockito, AssertJ, Spring Boot Test e Testcontainers.

E é um galho de **convergência**: ele testa o que os Galhos 1-12 construíram. Cada técnica linka de volta ao galho dono — a web testada vem do Galho 9, a persistência do Galho 10, o reativo do Galho 11, a segurança do Galho 12. Esse retorno paga **três dívidas** deixadas pra trás: o `@DataJpaTest` prometido no Galho 10, o `StepVerifier` adiado no Galho 11 e o `@WithMockUser` apontado no Galho 12 — todos quitados aqui.

Galhos 14 (Mensageria), 16 (Microservices) e 17 (Cloud) são planejados e ficam fora do escopo deste galho.

## Iniciado

O modelo mental — a pirâmide, o tripé unitário e a organização da suíte.

- [[03-Dominios/Tecnologia/Java/Testes/01 - O que é testar em Java — a pirâmide e o stack moderno|01 — O que é testar em Java]] — a pirâmide de testes e o stack moderno (JUnit 5, AssertJ, Mockito, Spring Boot Test).
- [[03-Dominios/Tecnologia/Java/Testes/02 - JUnit 5 — anatomia, lifecycle e o padrão AAA|02 — JUnit 5]] — anatomia de um teste, o lifecycle (`@BeforeEach`/`@AfterEach`) e o padrão Arrange-Act-Assert.
- [[03-Dominios/Tecnologia/Java/Testes/03 - AssertJ — fluent assertions|03 — AssertJ]] — asserções fluentes legíveis que dizem o que falhou e por quê.
- [[03-Dominios/Tecnologia/Java/Testes/04 - Testes parametrizados e organização|04 — Testes parametrizados e organização]] — `@ParameterizedTest`, `@Nested`, `@DisplayName` e a organização da suíte.
- [[03-Dominios/Tecnologia/Java/Testes/05 - Test data builders e fixtures|05 — Test data builders e fixtures]] — builders e fixtures pra montar dados de teste sem ruído.

## Adepto

O mock a fundo e os slices do Spring até a integração.

- [[03-Dominios/Tecnologia/Java/Testes/06 - Mockito — mocks, stubbing e matchers|06 — Mockito]] — criar mocks, fazer stubbing com `when`/`thenReturn` e os argument matchers.
- [[03-Dominios/Tecnologia/Java/Testes/07 - Mockito — verify, ArgumentCaptor e quando NÃO mockar|07 — Mockito — verify e quando NÃO mockar]] — `verify`, `ArgumentCaptor` e a disciplina de não mockar o que você não possui.
- [[03-Dominios/Tecnologia/Java/Testes/08 - Spring Boot Test e os slices — o contexto de teste|08 — Spring Boot Test e os slices]] — o `ApplicationContext` de teste e os slices que carregam só a fatia necessária.
- [[03-Dominios/Tecnologia/Java/Testes/09 - @WebMvcTest — testando controllers com MockMvc|09 — @WebMvcTest]] — testando controllers isolados com `MockMvc`, sem subir o servidor.
- [[03-Dominios/Tecnologia/Java/Testes/10 - @DataJpaTest — testando repositories|10 — @DataJpaTest]] — testando repositories e queries com o slice de persistência (a dívida do Galho 10, quitada).
- [[03-Dominios/Tecnologia/Java/Testes/11 - Testcontainers — infra real em testes|11 — Testcontainers]] — banco, broker e infra real em containers Docker no lugar de mocks e H2.
- [[03-Dominios/Tecnologia/Java/Testes/12 - Testes de integração ponta a ponta|12 — Testes de integração ponta a ponta]] — `@SpringBootTest` com o contexto completo, do request ao banco.

## Magus

As fronteiras difíceis e o que vem depois do verde.

- [[03-Dominios/Tecnologia/Java/Testes/13 - Testando a segurança|13 — Testando a segurança]] — `@WithMockUser`, `spring-security-test` e a verificação de authz (a dívida do Galho 12, quitada).
- [[03-Dominios/Tecnologia/Java/Testes/14 - Testando código assíncrono — Awaitility|14 — Testando código assíncrono]] — testando código assíncrono com Awaitility, sem `Thread.sleep` frágil.
- [[03-Dominios/Tecnologia/Java/Testes/15 - Testando código reativo — StepVerifier e @WebFluxTest|15 — Testando código reativo]] — `StepVerifier` e `@WebFluxTest` pra `Mono`/`Flux` (a dívida do Galho 11, quitada).
- [[03-Dominios/Tecnologia/Java/Testes/16 - Mockando HTTP externo — WireMock e MockRestServiceServer|16 — Mockando HTTP externo]] — WireMock e `MockRestServiceServer` pra simular APIs externas sem dependência de rede.
- [[03-Dominios/Tecnologia/Java/Testes/17 - Mutation testing — PIT e cobertura honesta|17 — Mutation testing]] — PIT e a pergunta que a cobertura de linha não responde: seus testes realmente pegam o bug?
- [[03-Dominios/Tecnologia/Java/Testes/18 - Performance — JMH e microbenchmarks|18 — Performance e microbenchmarks]] — JMH e a arte de medir performance sem cair nas armadilhas do JIT.
- [[03-Dominios/Tecnologia/Java/Testes/19 - Fitness functions — ArchUnit (testes de arquitetura)|19 — Fitness functions com ArchUnit]] — ArchUnit pra cravar regras de arquitetura como testes que falham na violação.
- [[03-Dominios/Tecnologia/Java/Testes/20 - Contract testing — Pact|20 — Contract testing com Pact]] — Pact e os contratos consumer-driven que protegem a fronteira entre serviços.
- [[03-Dominios/Tecnologia/Java/Testes/21 - Capstone — a estratégia de testes de uma app Spring production-grade|21 — Capstone]] — projetando a estratégia de testes de uma app Spring production-grade de ponta a ponta.

## Rotas alternativas

- **Completa** — 01 → 21 em ordem (da pirâmide ao capstone).
- **Entrevista internacional** — 01 → 02 → 03 → 06 → 09 → 10 → 12 → 21 (pirâmide, JUnit 5, AssertJ, Mockito, os slices web e JPA, integração e a estratégia — o que mais cai).
- **Os slices do Spring** — 08 → 09 → 10 → 11 → 12 → 13 (o contexto de teste, `@WebMvcTest`, `@DataJpaTest`, Testcontainers, integração e segurança).
- **Indo além do verde** — 17 → 18 → 19 → 20 (mutation testing, performance, fitness functions e contratos — o que a cobertura não conta).
- **Testando o stack reativo** — 01 → 08 → 15 + Galho 11 (Spring WebFlux/`WebClient` — o reativo que o `StepVerifier` verifica).

## Todas as notas

```dataview
TABLE fase, status
FROM "03-Dominios/Tecnologia/Java/Testes"
WHERE type = "concept"
SORT file.name ASC
```

## Veja também

- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Spring Core e Boot/index|Spring Core e Boot]] — o container que os slices carregam (Galho 8)
- [[03-Dominios/Tecnologia/Java/Web e APIs REST/index|Web e APIs REST]] — a web testada (Galho 9)
- [[03-Dominios/Tecnologia/Java/Persistência de dados/index|Persistência de dados]] — a persistência testada (Galho 10)
- [[03-Dominios/Tecnologia/Java/Programação Reativa/index|Programação Reativa]] — o reativo testado (Galho 11)
- [[03-Dominios/Tecnologia/Java/Segurança/index|Segurança]] — a segurança testada (Galho 12)
- [[03-Dominios/Tecnologia/Java/Dicionário de Java]] — glossário de termos da trilha

> Galhos 14 (Mensageria), 16 (Microservices) e 17 (Cloud) — planejados.
