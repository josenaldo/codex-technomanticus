---
title: "Jakarta EE"
created: 2026-06-07
updated: 2026-06-09
type: moc
status: growing
publish: true
tags:
  - java
  - jakarta-ee
  - moc
aliases:
  - "Galho 7 - Jakarta EE"
  - "Java EE (galho)"
---

# Jakarta EE

> [!abstract] TL;DR
> Galho 7 da trilha Java Senior; cobre a plataforma de especificações enterprise que o Spring abstrai: spec vs. implementação, a transição Java EE → Jakarta EE (rename `javax` → `jakarta`), Servlet, CDI (injeção, escopos, qualifiers/eventos, interceptors/decorators), JAX-RS, Bean Validation, JPA como especificação, JTA, o legado EJB e o estado atual da plataforma; 14 notas em 3 fases.

## Sobre este galho

Este galho cobre **a plataforma de especificações enterprise do Java de ponta a ponta** — não um framework, mas o conjunto de contratos que os frameworks implementam por baixo. Começa pelo modelo mental que destrava tudo (especificação vs. implementação, os perfis, o TCK) e pela transição histórica de Java EE para Jakarta EE com o rename de namespace. Avança pelo alicerce HTTP (Servlet), pelo coração da plataforma (CDI: injeção, escopos e client proxies, qualifiers/producers/eventos, interceptors/decorators/extensões), pela camada REST (JAX-RS), pela validação declarativa (Bean Validation), pela persistência como contrato (JPA spec, EntityManager e o ciclo de vida da entidade) e pela coordenação de transações (JTA). Fecha com o legado que moldou tudo (EJB) e uma síntese honesta do estado atual da plataforma.

**Audiência primária:** dev senior em preparação para entrevista internacional — cada nota expõe o "porquê" das decisões da plataforma e a pergunta que mais cai, com vocabulário preciso em inglês, e treina o reflexo de reconhecer **qual spec Jakarta está por baixo** de cada conveniência de framework. **Audiência secundária:** o dev que já usa Spring e quer entender o que o `@Autowired`/`@Transactional`/`@Valid` escondem, e o dev que mantém ou migra sistemas Jakarta EE / Java EE corporativos.

Este é um **galho de pesquisa** (sem tronco a podar): cada nota nasceu da documentação oficial (`jakarta.ee`, spec documents e Javadoc das specs) verificada fonte a fonte. É o **dono dos conceitos de especificação enterprise** da trilha.

**Fronteiras importantes:** o Spring (que implementa/abstrai estas specs) é do galho [[03-Dominios/Tecnologia/Java/Spring Core e Boot/index|Spring Core e Boot]] — aqui ele aparece só como motivação, nunca explicado; Spring MVC e validação no Spring são do galho [[03-Dominios/Tecnologia/Java/Web e APIs REST/index|Web e APIs REST]]; JPA operacional (Hibernate, fetch/N+1, caching, Spring Data, migrations) é do galho [[03-Dominios/Tecnologia/Java/Persistência de dados/index|Persistência de dados]] — aqui a JPA é tratada **só como especificação** (entidade, EntityManager, ciclo de vida); a mecânica de annotations está no Galho 1 ([[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/11 - Annotations|Annotations]]); concorrência de baixo nível está no Galho 4 ([[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Concorrência e paralelismo]]).

## Iniciado

1. [[01 - O modelo Jakarta EE — especificações e implementações]] — a ideia que destrava o bloco enterprise inteiro: especificação (API + spec document + TCK) vs. implementação certificada, os três perfis (Platform/Web/Core) e onde cada spec roda (app server, servlet container, runtime moderno).
2. [[02 - De Java EE a Jakarta EE]] — a transição de governança (Sun → Oracle → Eclipse Foundation, 2017) e o rename big-bang `javax.*` → `jakarta.*` no EE 9 (2020), por que aconteceu (trademark) e o impacto prático de um ecossistema partido em dois namespaces.
3. [[03 - Servlet API — o alicerce HTTP]] — o contrato entre código Java e servidor HTTP (lifecycle, `HttpServlet`, sessões, filters), o modelo de uma instância para muitas threads, e por que tudo que atende HTTP no ecossistema roda sobre ele.
4. [[04 - CDI — beans e injeção]] — o coração da plataforma: o que torna uma classe um bean, `@Inject` por construtor, bean discovery e a resolução typesafe; o modelo de inversão de controle que `@Autowired` esconde.

## Adepto

5. [[05 - CDI — escopos e contextos]] — escopo como ciclo de vida gerenciado (`@ApplicationScoped`/`@RequestScoped`/`@SessionScoped`/`@Dependent`) e o **client proxy** que explica os comportamentos "mágicos": classe não-final, lazy init e por que um bean request-scoped vive dentro de um application-scoped.
6. [[06 - CDI — qualifiers, producers e eventos]] — os três mecanismos de flexibilidade sobre a resolução por tipo: qualifiers para desambiguar implementações, producers para fabricar o que o container não cria, e eventos como pub/sub embutido (síncrono e assíncrono).
7. [[07 - JAX-RS — REST declarativo]] — REST mapeado para métodos Java por annotations: resources e params tipados, content negotiation, e o modelo de providers (`MessageBodyReader/Writer`, `ExceptionMapper`) que explica como o JSON vira objeto.
8. [[08 - Bean Validation]] — restrições declaradas no modelo (`@NotNull`/`@Size`/custom constraints) e validadas em um ponto só, standalone ou integradas a CDI/JAX-RS; a spec que está por baixo do `@Valid` que se vê nos frameworks.
9. [[09 - JPA — a especificação de persistência]] — JPA como **contrato** (`@Entity`, identidade, mapeamento, relacionamentos e owning side, persistence unit): o que é portável da spec vs. o que é extensão do provider — "JPA não é o Hibernate".
10. [[10 - EntityManager e o ciclo de vida da entidade]] — o persistence context (identity map + unit of work), os quatro estados da entidade (new/managed/detached/removed) e suas transições, a semântica do `merge`, flush/dirty checking e JPQL — a origem da maioria dos "bugs de JPA".

## Magus

11. [[11 - JTA — transações na plataforma]] — coordenação de transações declarativa (`@Transactional` via interceptor CDI) e programática (`UserTransaction`), a regra de rollback (unchecked sim, checked não), os tipos de propagação e XA/two-phase commit para múltiplos recursos.
12. [[12 - EJB — o legado que moldou a plataforma]] — visão histórica honesta: o que o EJB resolvia quando nada mais oferecia, o peso do 2.x e a reação que levou ao CDI, os tipos que sobrevivem (session beans, MDB, timer) e quando você ainda encontra EJB em legado.
13. [[13 - CDI avançado — interceptors, decorators e extensões]] — o AOP da plataforma: interceptors (cegos ao contrato — o mecanismo por baixo de `@Transactional`), decorators (que conhecem o contrato de negócio) e as extensões de container, incluindo o caminho build-time do CDI Lite / Core Profile.
14. [[14 - Jakarta EE hoje — a plataforma sob o Spring]] — capstone do galho: estado real da plataforma (EE 11/2025, EE 12 em desenvolvimento, cadência Eclipse), o papel do Core Profile na nova geração de runtimes, e a tese central mapeada — o que cada framework esconde, com o frame de decisão plataforma pura vs. framework.

## Rotas alternativas

### Completa

01 → 02 → 03 → 04 → 05 → 06 → 07 → 08 → 09 → 10 → 11 → 12 → 13 → 14. Percurso linear do modelo mental ao estado atual — recomendado para quem está construindo a base enterprise do zero.

### Entrevista internacional

01 → 02 → 04 → 09 → 10 → 11 → 14. Spec vs. implementação, a transição de namespace, CDI como coração da plataforma, JPA como contrato, o ciclo de vida da entidade, transações, e a síntese plataforma vs. framework — o que mais cai em entrevista de nível senior.

### O que o Spring esconde

04 → 05 → 06 → 13 → 14. A trilha completa do CDI (injeção, escopos e client proxy, qualifiers/producers/eventos, interceptors/decorators) mais a capstone — o mecanismo real por baixo de `@Autowired` e `@Transactional`.

### REST do zero na plataforma

03 → 04 → 07 → 08. Servlet como alicerce, CDI para montar o grafo de objetos, JAX-RS para os endpoints e Bean Validation para a entrada — uma API REST construída só com especificações.

### Persistência e transações

09 → 10 → 11. JPA como contrato, o EntityManager e os estados da entidade, e a JTA coordenando o commit — o contrato de persistência antes de qualquer Hibernate ou Spring Data.

## Todas as notas

```dataview
TABLE fase, status, updated
FROM "03-Dominios/Tecnologia/Java/Jakarta EE"
WHERE type = "concept"
SORT file.name ASC
```

## Veja também

- [[03-Dominios/Tecnologia/Java/index|Java (MOC central)]]
- [[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/index|Linguagem e sintaxe moderna (Galho 1)]]
- [[03-Dominios/Tecnologia/Java/Collections e Streams/index|Collections e Streams (Galho 2)]]
- [[03-Dominios/Tecnologia/Java/JVM/index|JVM por dentro (Galho 3)]]
- [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Concorrência e paralelismo (Galho 4)]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java|Dicionário de Java]]

> Galhos 8 (Spring Core e Boot), 9 (Web e APIs REST) e 10 (Persistência de dados) — planejados.
