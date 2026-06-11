---
title: "Spring Core e Boot"
created: 2026-06-08
updated: 2026-06-11
type: moc
status: growing
publish: true
tags:
  - java
  - spring
  - moc
aliases:
  - "Spring"
  - "Spring Framework"
  - "Spring Boot"
  - "Galho 8 - Spring"
---

# Spring Core e Boot

> [!abstract] TL;DR
> Galho 8 da trilha Java Senior; cobre o container que implementa as specs do Galho 7: IoC/DI, beans e escopos, AOP/proxies, configuração e profiles, conditional/auto-configuration, eventos do contexto, fundamentos do Boot e Actuator; 18 notas em 3 fases.

## Sobre este galho

Este galho cobre **o Spring como container e plataforma** — não as APIs de borda (Web, Dados, Segurança), mas o núcleo que faz tudo funcionar por baixo. Começa pelo modelo mental (o que é Spring, o que é Boot, por que o ecossistema é tão grande), avança pelo mecanismo central (IoC/DI, beans, escopos, ApplicationContext), aprofunda em AOP e proxies (o mecanismo real por baixo de `@Transactional` e `@Cacheable`), percorre configuração e profiles, eventos do contexto e os hooks de extensão do container, e finaliza com os fundamentos do Boot: conditional/auto-configuration, starters, o servidor embedded e o Actuator.

**Audiência primária:** dev senior em preparação para entrevista internacional — cada nota expõe o "porquê" das decisões de design do Spring e a pergunta que mais cai, com vocabulário preciso em inglês, e treina o reflexo de reconhecer **qual mecanismo do container está em jogo** em cada comportamento "mágico". **Audiência secundária:** o dev que já usa Spring no dia a dia e quer finalmente entender o que o `@Autowired`/`@Transactional`/`@SpringBootApplication` escondem.

Este é um **galho híbrido**: parte refatora o tronco existente `Spring Boot.md` (que cobria os temas de forma densa e monolítica), parte expande com pesquisa aprofundada nas partes que o tronco tratava de forma rasa (AOP, proxies, BeanPostProcessor, auto-configuration interna). A divisão em notas atômicas garante que cada conceito possa ser estudado e revisado de forma independente.

**Fronteiras importantes:** [[03-Dominios/Java/Jakarta EE/index|Jakarta EE (Galho 7)]] é a plataforma de especificações que o Spring implementa e abstrai — o ponto de partida conceitual para entender o que o Spring esconde. Spring MVC/Web é o galho [[03-Dominios/Java/Web e APIs REST/index|Web e APIs REST]] — endpoints, DispatcherServlet e a camada web ficam lá. Persistência/transações operacionais com Spring Data, Hibernate, fetch/N+1 e migrations é o galho [[03-Dominios/Java/Persistência de dados/index|Persistência de dados]] — aqui a persistência aparece só quando explica comportamento do proxy (`@Transactional`). Spring Reativa com WebFlux é o galho [[03-Dominios/Java/Programação Reativa/index|Programação Reativa]]; Spring Security é o galho [[03-Dominios/Java/Segurança/index|Segurança]]; Testes no ecossistema Spring é o galho [[03-Dominios/Java/Testes/index|Testes]]; Microservices/Cloud com Spring Cloud (Galhos 16 e 17) são planejados, sem cobertura neste galho.

## Iniciado

1. [[03-Dominios/Java/Spring Core e Boot/01 - O que é Spring — Framework, Boot e o ecossistema|O que é Spring — Framework, Boot e o ecossistema]] — visão panorâmica do ecossistema: o que é o Framework, o que é o Boot, o que é o Spring Portfolio, e por que tantos projetos; o modelo mental que orienta todo o resto do galho.
2. [[03-Dominios/Java/Spring Core e Boot/02 - IoC e injeção de dependência no Spring|IoC e injeção de dependência no Spring]] — inversão de controle como princípio e injeção de dependência como implementação; o container como dono do grafo de objetos e o que isso muda no design de código.
3. [[03-Dominios/Java/Spring Core e Boot/03 - Beans e estereótipos — @Component, @Service, @Repository, @Controller|Beans e estereótipos — @Component, @Service, @Repository, @Controller]] — o que torna uma classe um bean Spring, component scanning, e o papel semântico (e técnico) de cada estereótipo.
4. [[03-Dominios/Java/Spring Core e Boot/04 - Tipos de injeção — constructor, setter, field|Tipos de injeção — constructor, setter, field]] — as três formas de injetar dependências, o consenso atual (constructor-injection), e os casos em que setter ou field injection fazem sentido ou causam problemas.
5. [[03-Dominios/Java/Spring Core e Boot/05 - @Configuration e @Bean — definição explícita de beans|@Configuration e @Bean — definição explícita de beans]] — configuração programática de beans: quando usar `@Bean` em vez de anotações, full vs. lite `@Configuration`, e como o CGLIB proxy garante a semântica de singleton.

## Adepto

6. [[03-Dominios/Java/Spring Core e Boot/06 - ApplicationContext — o container e seu ciclo|ApplicationContext — o container e seu ciclo]] — o container central: hierarquia de contextos, as fases de inicialização (load → refresh → ready), e o que acontece quando o contexto sobe e desce.
7. [[03-Dominios/Java/Spring Core e Boot/07 - Ciclo de vida e escopos de beans|Ciclo de vida e escopos de beans]] — escopos built-in (singleton, prototype, request, session, application), o ciclo de vida de um bean (instantiation → injection → init → use → destroy), e as armadilhas de injetar um bean de escopo curto em um de escopo longo.
8. [[03-Dominios/Java/Spring Core e Boot/08 - Qualificação de beans — @Qualifier, @Primary, @Profile|Qualificação de beans — @Qualifier, @Primary, @Profile]] — os mecanismos para resolver ambiguidade quando há múltiplas implementações: `@Primary` como padrão, `@Qualifier` para seleção precisa, e `@Profile` para variações de ambiente.
9. [[03-Dominios/Java/Spring Core e Boot/09 - AOP e proxies no Spring|AOP e proxies no Spring]] — Aspect-Oriented Programming no Spring: pointcuts, advices, os dois mecanismos de proxy (JDK dynamic proxy vs. CGLIB), e como o container intercepta chamadas para entregar cross-cutting concerns.
10. [[03-Dominios/Java/Spring Core e Boot/10 - Self-invocation e os limites do proxy|Self-invocation e os limites do proxy]] — por que `this.metodo()` dentro da mesma classe ignora o proxy, as três saídas (refatorar, `AopContext`, injetar a si mesmo), e o que esse comportamento revela sobre a arquitetura de proxies do Spring.
11. [[03-Dominios/Java/Spring Core e Boot/11 - Eventos do ApplicationContext|Eventos do ApplicationContext]] — o sistema de eventos built-in: `ApplicationEvent`, `@EventListener`, publicação síncrona e assíncrona, eventos transacionais com `@TransactionalEventListener`, e quando usar eventos vs. chamadas diretas.
12. [[03-Dominios/Java/Spring Core e Boot/12 - Configuração e profiles|Configuração e profiles]] — `Environment`, `@Value`, `@ConfigurationProperties`, precedência de fontes de configuração, e profiles como mecanismo de variação de comportamento entre ambientes.

## Magus

13. [[03-Dominios/Java/Spring Core e Boot/13 - BeanPostProcessor e BeanFactoryPostProcessor|BeanPostProcessor e BeanFactoryPostProcessor]] — os dois hooks de extensão do container: `BeanFactoryPostProcessor` modifica a definição de beans antes da instanciação; `BeanPostProcessor` envolve cada bean depois — é aqui que o container instala proxies AOP e processa annotations customizadas.
14. [[03-Dominios/Java/Spring Core e Boot/14 - Conditional beans — @Conditional e os @ConditionalOn|Conditional beans — @Conditional e os @ConditionalOn]] — o mecanismo que permite registrar beans condicionalmente: `@Conditional` como contrato, e as variantes do Boot (`@ConditionalOnClass`, `@ConditionalOnMissingBean`, `@ConditionalOnProperty` etc.) que são a engrenagem central da auto-configuration.
15. [[03-Dominios/Java/Spring Core e Boot/15 - Auto-configuration e starters|Auto-configuration e starters]] — como o Boot descobre e aplica configurações automaticamente (META-INF/spring.factories / AutoConfiguration.imports), o papel dos starters como dependências curadas, e como escrever sua própria auto-configuration.
16. [[03-Dominios/Java/Spring Core e Boot/16 - SpringApplication e o embedded server|SpringApplication e o embedded server]] — o bootstrap do Boot: o que `SpringApplication.run()` faz, como o servidor embedded (Tomcat, Jetty, Undertow) é configurado e iniciado, e os eventos do ciclo de vida da aplicação.
17. [[03-Dominios/Java/Spring Core e Boot/17 - Actuator e observabilidade|Actuator e observabilidade]] — os endpoints de produção do Boot: health, info, metrics, env, beans; integração com Micrometer; customização de endpoints e segurança — o que os SREs e entrevistadores esperam que você saiba.
18. [[03-Dominios/Java/Spring Core e Boot/18 - Capstone — Spring sob o capô|Capstone — Spring sob o capô]] — capstone do galho: o mapa completo do container desde o bootstrap até a requisição, as decisões de design que moldaram o Spring (por que proxy em vez de bytecode puro, por que convention over configuration no Boot), e o frame de decisão Spring puro vs. Spring Boot vs. Jakarta EE nativo.

## Rotas alternativas

### Completa

01 → 02 → 03 → 04 → 05 → 06 → 07 → 08 → 09 → 10 → 11 → 12 → 13 → 14 → 15 → 16 → 17 → 18. Percurso linear do modelo mental à capstone — recomendado para quem está construindo a base Spring do zero ou quer a cobertura total para entrevista.

### Entrevista internacional

02 → 04 → 07 → 09 → 10 → 11 → 15 → 18. IoC/DI como fundamento, tipos de injeção (o que o entrevistador testa primeiro), escopos e armadilhas, AOP e proxies (o tema mais cobrado em senior), self-invocation (a pegadinha clássica), eventos, auto-configuration (o diferencial Boot) e a capstone integradora.

### O que o Spring esconde

02 → 05 → 09 → 13 → 15 → 18. A trilha dos mecanismos internos: IoC como princípio, `@Configuration` com CGLIB, AOP e a mecânica de proxy, os hooks de extensão do container, a auto-configuration desmontada, e a síntese final — o percurso para quem quer entender o que está por baixo das anotações.

### Boot sob o capô

14 → 15 → 16 → 17 → 13 → 18. A trilha inversa do Boot: começa pelos conditionals (o building block), sobe para auto-configuration e starters, passa pelo bootstrap da aplicação e pelo servidor embedded, examina o Actuator, desce aos hooks de extensão do container, e termina na capstone.

### Spring vs Jakarta EE

02 → 07 → 09 → 11 → 18 + notas do Galho 7 (CDI, interceptors, eventos). IoC no Spring vs. CDI, escopos e proxies comparados, AOP no Spring vs. interceptors CDI, eventos do ApplicationContext vs. eventos CDI, e a capstone com o frame de decisão — o percurso para quem vem do Galho 7 e quer mapear um mundo no outro.

## Todas as notas

```dataview
TABLE fase, status FROM "03-Dominios/Java/Spring Core e Boot" WHERE type = "concept" SORT file.name ASC
```

## Veja também

- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Jakarta EE/index|Jakarta EE]] — a plataforma de especificações que o Spring implementa
- [[03-Dominios/Java/Linguagem e sintaxe moderna/index|Linguagem e sintaxe moderna]]
- [[03-Dominios/Java/Concorrência e paralelismo/index|Concorrência e paralelismo]]
- [[03-Dominios/Java/Dicionário de Java|Dicionário de Java]]

> Galhos 9 (Spring MVC/Web), 10 (Persistência/Spring Data), 11 (Spring Reativa/WebFlux), 12 (Spring Security), 13 (Testes no ecossistema Spring), 16 (Microservices) e 17 (Spring Cloud) — planejados.
