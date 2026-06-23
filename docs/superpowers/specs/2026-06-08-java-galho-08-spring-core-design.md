---
title: "Spec — Galho 8 da trilha Java Senior (Spring Core e Boot)"
date: 2026-06-08
author: Josenaldo
status: draft
type: spec
publish: false
---

# Spec — Galho 8 da trilha Java Senior (Spring Core e Boot)

## 1. Contexto e motivação

Este é o **oitavo galho** da trilha Java Senior (roadmap em `docs/superpowers/specs/2026-06-02-java-senior-roadmap-design.md`, §5, bloco "Fundamentos enterprise e Spring"). Pressupõe leitura do roadmap, que estabelece topologia flat, esquema de 3 fases, padrões editoriais e política de poda. Os Galhos 1 (Linguagem), 2 (Collections/Streams), 3 (JVM), 4 (Concorrência), 5 (Swing), 6 (JavaFX) e **7 (Jakarta EE)** já fecharam em `main` — seus artefatos são o **template de padrão e qualidade** deste galho, e o Galho 7 é a sua **dependência direta**.

**Galho HÍBRIDO: REFATOR (poda parcial) + PESQUISA.** Diferente do Galho 7 (pesquisa pura, sem tronco), este galho tem duas naturezas:

- **Parte REFATOR (poda parcial):** existe o tronco `Backend/Spring Boot.md` (1848 linhas, `publish: false`, `status: evergreen`) com conteúdo core rico — `## Spring IoC Container`, `## AOP e proxies`, `## Configuração e Profiles`, `## Actuator`. Essas seções são **matéria-prima a refinar** e depois **podar** (callout + wikilinks). O tronco está **cheio de fabricação** (33 ocorrências de `Patient`/`MedEspecialista`/1ª pessoa) — é **contraexemplo a higienizar, nunca copiar**.
- **Parte PESQUISA:** o tronco é **fino** em auto-configuration (só menciona em `## O que é` e na subseção `### Conditional beans`), starters, eventos do `ApplicationContext`, `SpringApplication`/bootstrap e AOT. Essas notas **nascem de docs oficiais** (`docs.spring.io`, `spring.io/projects/...`) verificadas via WebFetch — atenção redobrada à fabricação.

**A fronteira-assinatura, invertida em relação ao Galho 7.** No Galho 7 o Spring era **proibido** (só motivação, sem wikilink). Aqui o Spring **é o assunto** — mas a regra agora é **LINKAR DE VOLTA ao Galho 7** mostrando como o Spring implementa/abstrai cada spec, **sem re-explicar a spec**. Ex.: a nota de IoC/DI explica o container do Spring e linka `[[03-Dominios/Tecnologia/Java/Jakarta EE/04 - CDI — beans e injeção|CDI]]` ("é a mesma ideia da spec CDI, com container próprio — é isso que o `@Autowired` esconde"); AOP linka interceptors do CDI; eventos linkam `@Observes`; post-processors linkam portable extensions. O Galho 7 plantou **9 ganchos "Galho 8 (planejado)"** esperando exatamente esses wikilinks (dívida reversa — §3.6). Este galho **quita** essa dívida.

Spring Core e Boot é o **container que implementa as ideias do Galho 7**: IoC/DI no Spring, ciclo de vida e escopos de beans, AOP e proxies (o mecanismo sob `@Transactional`/`@Async`), configuração e profiles, auto-configuration e starters (o coração do Boot), `@ConfigurationProperties`, eventos do contexto e os fundamentos do Boot. Depende dos Galhos 1 (annotations/reflection) e 7 (specs Jakarta).

## 2. Objetivo

Produzir, em uma sessão de execução dedicada, **18 notas atômicas + 1 MOC do galho + expansão do Dicionário de Java + ativação do MOC central + poda parcial do tronco + quitação da dívida reversa**, em `03-Dominios/Tecnologia/Java/Spring Core e Boot/` e `03-Dominios/Tecnologia/Java/`, todas `publish: true`, em PT-BR, distribuídas em 3 fases (**5 Iniciado + 7 Adepto + 6 Magus**).

Ao terminar o galho, o leitor deve conseguir:

- **Explicar em inglês** o modelo IoC/DI do Spring, o ciclo de vida e os escopos de beans, como AOP via proxy implementa `@Transactional`/`@Async`, e como a auto-configuration do Boot decide o que configurar.
- **Reconhecer o que o Spring implementa do Galho 7**: dado `@Autowired`/`@Transactional`/`@Valid`/um stereotype, apontar a spec Jakarta correspondente (CDI, JTA, Bean Validation) e a diferença de mecanismo (proxy-based vs interceptor-based, container próprio vs CDI).
- **Diagnosticar armadilhas clássicas**: self-invocation que ignora o proxy, `@Transactional` em método `private`/`final`, prototype injetado em singleton, dependência circular, ambiguidade de bean, auto-config que não dispara (`ConditionEvaluationReport`).
- **Decidir e defender** escolhas de configuração (`@ConfigurationProperties` vs `@Value`, profiles, conditional beans, `@Bean` vs component scanning) e situar o Spring honestamente em relação à plataforma Jakarta.

A barra é "explicar o mecanismo, reconhecer a spec por baixo e decidir com critério" — não "escrever um `BeanPostProcessor` de produção".

## 3. Saídas concretas

### 3.1. Notas (`03-Dominios/Tecnologia/Java/Spring Core e Boot/`)

Pasta **nova**, flat. 18 notas + 1 MOC (`index.md`, obrigatório pro folder-link do Quartz). Numeração global por galho (não reinicia por fase).

#### Iniciado (5 notas — vocabulário + modelo mental)

| # | Nota | Escopo nuclear |
|---|------|----------------|
| 01 | O que é Spring — Framework, Boot e o ecossistema | Spring Framework vs Spring Boot vs projetos (Data/Security/Cloud); o stack (Boot → Framework → projetos); "opinionated"/convention-over-configuration; Boot 3.x baseline Java 17, namespace `jakarta.*` (migrou de `javax` no Boot 3). Porta de entrada. Linka Jakarta EE (a plataforma que o Spring implementa). |
| 02 | IoC e injeção de dependência no Spring *(opus)* | IoC como princípio (o framework controla criação/wiring), DI como implementação, o container; por que inverter controle (acoplamento, testabilidade). **A nota-assinatura do galho.** Linka CDI 04 ("mesma ideia da spec CDI; container próprio — é isso que o `@Autowired` esconde"). Quita ganchos Annotations:309, EJB 12:65, JavaFX 11:35/110, CDI 04:24. |
| 03 | Beans e estereótipos — @Component, @Service, @Repository, @Controller | O que é um bean Spring; component scanning (`@ComponentScan`, `@SpringBootApplication`); os 4 estereótipos e o que cada um adiciona (`@Repository` = tradução de exceções pra `DataAccessException`; `@Controller`/`@RestController` = Galho 9, mencionar sem explicar). Linka CDI 04 (bean discovery). |
| 04 | Tipos de injeção — constructor, setter, field | Constructor injection (recomendado: `final`, fail-fast, testável, sem reflection); setter (dependências opcionais); field (`@Autowired` em campo — evite, e por quê); dependências circulares proibidas por default no Boot 2.6+. Linka CDI 04 (`@Inject` em campo/construtor/método). |
| 05 | @Configuration e @Bean — definição explícita de beans | Classes `@Configuration`, métodos `@Bean`; quando usar (libs externas não-anotáveis, construção complexa, overrides) vs component scanning; `@Import`; full vs lite mode (`proxyBeanMethods=false`). Linka CDI 06 (`@Produces` — fabricar o que não é bean anotável: mesma necessidade, mecanismo próprio). |

#### Adepto (7 notas — domínio operacional; AOP densa → opus)

| # | Nota | Escopo nuclear |
|---|------|----------------|
| 06 | ApplicationContext — o container e seu ciclo | `BeanFactory` vs `ApplicationContext` (o que o segundo adiciona: eventos, i18n, resource loading, environment); tipos concretos (`AnnotationConfig...`, servlet, reactive); `refresh()`; interfaces `*Aware`. Injetar o contexto (raro). Linka CDI 04 (o container da spec). |
| 07 | Ciclo de vida e escopos de beans | Lifecycle (instanciação → populate → `*Aware` → BPP before → init → BPP after → pronto → destroy); `@PostConstruct`/`@PreDestroy`; escopos (singleton/prototype/request/session/application/websocket); a armadilha prototype-em-singleton e as saídas (`ObjectProvider`, `@Lookup`, scoped proxy). Linka CDI 05 (escopos + client proxies — mesma tensão de escopo, mecanismo próprio). Quita gancho CDI 05:48. |
| 08 | Qualificação de beans — @Qualifier, @Primary, @Profile | Ambiguidade de tipo (2 beans do mesmo tipo); `@Qualifier` (custom e por nome); `@Primary`; `@Profile` como condicional de bean; injeção de coleções (`List<T>`, `Map<String,T>`); `@Order`. Linka CDI 06 (qualifiers — `@Qualifier`/`@Default`/`@Any`). |
| 09 | AOP e proxies no Spring *(opus)* | Cross-cutting concerns; como o proxy intercepta (advice antes/depois do método real); **JDK dynamic proxy vs CGLIB** (interface vs subclasse); advice types (`@Before`/`@After`/`@AfterReturning`/`@AfterThrowing`/`@Around`); pointcut expressions; `@Aspect`. AOP é o mecanismo sob `@Transactional`/`@Async`/`@Cacheable` (citar, comportamento transacional = Galho 10). Linka CDI 13 (interceptors — **Spring é proxy-based, CDI é interceptor-based**: mesma meta, mecanismo diferente). |
| 10 | Self-invocation e os limites do proxy | A armadilha clássica: chamada interna (`this.metodo()`) **bypassa o proxy** e ignora o advice; `@Transactional`/`@Async` em método `private` ou `final` são silenciosamente ignorados; por quê (o proxy só intercepta chamadas externas / CGLIB não sobrescreve `final`/`private`); soluções (extrair pra outro bean, self-injection, anotar o método de entrada público). Linka CDI 05/13 (self-invocation no client proxy — a spec tem o mesmo limite). |
| 11 | Eventos do ApplicationContext | `ApplicationEvent`/POJO events, `ApplicationEventPublisher`, `@EventListener`; síncrono por default; `@Async` events; `@TransactionalEventListener` (menção — comportamento transacional = Galho 10); eventos built-in do contexto (`ContextRefreshedEvent` etc.). Pub/sub in-process desacoplado. Linka CDI 06 (eventos `@Observes`/`Event<T>` — a versão da spec). Quita gancho CDI 06:42. |
| 12 | Configuração e profiles | Hierarquia de fontes (precedência: args > env > `application-{profile}` > `application.yml` > defaults); profiles (`application-{profile}.yml`, `@Profile` em beans, ativação via env/arg/código); **`@ConfigurationProperties`** (binding tipado, records, `@Validated`, relaxed binding, `@ConfigurationPropertiesScan`) vs **`@Value`**/SpEL (casos pontuais). Linka Bean Validation 08 (`@Validated` aciona Bean Validation — a spec do Galho 7). |

#### Magus (6 notas — Boot internals + maestria; auto-config e capstone → opus)

| # | Nota | Escopo nuclear |
|---|------|----------------|
| 13 | BeanPostProcessor e BeanFactoryPostProcessor | Os hooks de extensão do container; **BFPP** (modifica *bean definitions* antes da instanciação — ex: resolução de placeholders) vs **BPP** (envolve *instâncias* depois — é onde nascem os proxies AOP/`@Async`); ordem (`@Priority`/`Ordered`); por que entender isso explica "a mágica" do Spring. Linka CDI 13 (portable extensions / build compatible extensions — o ponto de extensão da spec). |
| 14 | Conditional beans — @Conditional e os @ConditionalOn* | O SPI `@Conditional` + `Condition`; os condicionais do Boot: `@ConditionalOnClass`/`OnMissingClass`, `@ConditionalOnBean`/`OnMissingBean`, `@ConditionalOnProperty`, `@ConditionalOnWebApplication`, etc.; ordem de avaliação; é o mecanismo que a auto-configuration usa. Pré-requisito da nota 15. |
| 15 | Auto-configuration e starters *(opus)* | `@EnableAutoConfiguration`/`@SpringBootApplication`; **`META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports`** (substituiu `spring.factories` no Boot 2.7+; só `.imports` no Boot 3 — **WebFetch obrigatório**); como classes de auto-config usam `@Conditional` (liga à 14) e cedem pro user (`@ConditionalOnMissingBean`); o que é um **starter** (BOM de dependências, não código); ordem (`@AutoConfiguration(before/after)`); AOT/build-time (menção — native image = Galho 17); debug (`--debug` → `ConditionEvaluationReport`, `/actuator/conditions`). Linka CDI 13 (build-time resolution / CDI Lite — runtimes que resolvem em build-time). Quita gancho CDI 13:42. |
| 16 | SpringApplication e o embedded server | O bootstrap: `SpringApplication.run()` (cria o contexto, dispara auto-config, sobe o servidor); fases e listeners (`ApplicationRunner`/`CommandLineRunner`, `SpringApplicationRunListener` — panorama); **embedded server** como conceito (Tomcat/Jetty/Undertow embutidos — escolha por starter; deep tuning = Galho 9/17); fat/executable jar e layered jar (conceito — packaging deep = Galho 15/17); banner/exit codes (menção). Linka Servlet 03 (o embedded server roda o Servlet container da spec). Quita gancho EJB 12:203. |
| 17 | Actuator e observabilidade | `spring-boot-starter-actuator`; endpoints (`/health`, `/info`, `/metrics`, `/loggers`, `/conditions`, `/beans`...); exposição e segurança dos endpoints (menção — auth = Galho 12); health groups e liveness/readiness probes; custom `HealthIndicator`; **Micrometer** como fachada de métricas (conceito). **Fronteira:** OpenTelemetry/tracing/observabilidade distribuída profunda = Galho 17 (texto "(planejado)"). |
| 18 | Capstone — Spring sob o capô *(opus)* | "O que a auto-configuration esconde": traçar uma request do `run()` ao bean pronto, passando por scanning, conditional, post-processor, proxy. **Tabela Spring → Jakarta EE** (IoC↔CDI, AOP↔interceptors, `@Transactional` Spring↔JTA, `@Validated`↔Bean Validation, eventos↔`@Observes`) — "dois caminhos pro mesmo problema". Decisão honesta Spring vs plataforma pura (sem dogma, sem estatística inventada). Munição de entrevista. Cheatsheet nota→problema. **WebFetch obrigatório.** |

**Decisões de fronteira (escopo de outro dono — texto "(planejado)", sem wikilink):**
- **Spring MVC / REST controllers / `@ControllerAdvice` / content negotiation / validation no controller** → Galho 9. Aqui `@Controller`/`@RestController` só são citados como stereotypes (nota 03).
- **`@Transactional` operacional (propagation/isolation/rollback) / Spring Data / JPA-Hibernate / N+1 / caching** → Galho 10. Aqui **só o AOP que torna `@Transactional` possível** (notas 09/10); o comportamento transacional NÃO é deste galho.
- **WebFlux / Reactor / R2DBC** → Galho 11. **Spring Security** → Galho 12. **Spring Boot Test / `@SpringBootTest` / slices** → Galho 13. **Spring Cloud** → Galho 16. **GraalVM native image / OpenTelemetry / packaging deep / deploy** → Galho 17.
- **Specs Jakarta (CDI, JTA, Bean Validation, JPA, Servlet)** → Galho 7 (COMPLETO). **Linkar de volta, nunca re-explicar a spec.** Fronteira-assinatura do galho.
- **Mecânica de annotations/reflection** → Galho 1 nota 11 (linkar). **Generics/records** → Galho 1; **threading/`@Async` por baixo** → Galho 4 (linkar quando tocar em concorrência).

### 3.2. MOC do galho

`03-Dominios/Tecnologia/Java/Spring Core e Boot/index.md`:
- `type: moc`, `status: growing`
- Frontmatter padrão (`title: "Spring Core e Boot"`, tags `java`/`spring`/`moc`, aliases `["Spring Core e Boot", "Spring", "Spring Framework", "Spring Boot", "Galho 8 - Spring"]`)
- TL;DR callout (galho cobre o container que implementa as specs do Galho 7: IoC/DI, beans e escopos, AOP/proxies, configuração e profiles, conditional/auto-configuration, eventos, fundamentos do Boot e Actuator)
- "Sobre este galho" + audiência primária/secundária + nota de que é galho híbrido (refator parcial do tronco `Spring Boot.md` + pesquisa pras partes finas)
- Conteúdo agrupado em 3 H2 (`## Iniciado` / `## Adepto` / `## Magus`) com wikilinks pras 18 notas (uma linha descritiva cada)
- **Rotas alternativas (5):**
  - **Completa** — 01 → 18 em ordem
  - **Entrevista internacional** — 02 → 04 → 07 → 09 → 10 → 11 → 15 → 18 (IoC/DI, injeção, escopos, AOP, self-invocation, eventos, auto-config, capstone — o que mais cai)
  - **O que o Spring esconde** — 02 → 05 → 09 → 13 → 15 → 18 (DI, `@Configuration`, AOP, post-processors, auto-config, capstone — a mágica desmontada)
  - **Boot sob o capô** — 14 → 15 → 16 → 17 → 13 → 18 (conditional, auto-config, bootstrap, Actuator, post-processors, capstone)
  - **Spring vs Jakarta EE** (a ponte com o Galho 7) — 02 → 07 → 09 → 11 → 18 + notas do Galho 7 (CDI, interceptors, eventos)
- "Veja também": MOC central `[[03-Dominios/Tecnologia/Java/index|Trilha Java]]`, Galho 7 (Jakarta EE — a plataforma sob o Spring), Galho 1 (Annotations), Galho 4 (Concorrência — `@Async`/threads), Dicionário de Java; Galhos 9/10/11/12/13/16/17 como texto "(planejado)" sem wikilink
- Dataview "Todas as notas do galho"

### 3.3. Dicionário de Java (EXPANSÃO — não recriar)

`03-Dominios/Tecnologia/Java/Dicionário de Java.md` já existe (**202 verbetes** após o Galho 7, `type: glossary`, seção alfabética única `## A`…`## Z` com verbetes `### `). Este galho **expande** o arquivo existente inserindo os verbetes **em ordem alfabética case-insensitive (sem acento)** nas seções de letra apropriadas. **Nunca recriar o arquivo nem reordenar verbetes existentes.** Atualizar `updated` no frontmatter. Nenhum verbete Spring existe ainda (só `client proxy (CDI)` é adjacente — é do Galho 7, intacto).

Verbetes a inserir (~37):

`@Autowired`, `@Bean`, `@Component / estereótipos Spring`, `@Conditional / @ConditionalOnX`, `@Configuration`, `@ConfigurationProperties`, `@EnableAutoConfiguration`, `@EventListener`, `@Primary`, `@Profile (Spring)`, `@Qualifier (Spring)`, `@Transactional (Spring)`, `@Value`, `advice (Spring AOP)`, `ApplicationContext`, `aspect`, `auto-configuration`, `BeanFactory`, `BeanFactoryPostProcessor`, `BeanPostProcessor`, `bean scope (Spring)`, `CGLIB`, `component scanning`, `constructor injection`, `convention over configuration`, `embedded server`, `executable jar / fat jar`, `IoC / inversão de controle (Spring)`, `JDK dynamic proxy`, `pointcut`, `self-invocation`, `Spring Actuator`, `Spring AOP`, `Spring AOT`, `Spring Boot`, `Spring Framework`, `SpringApplication`, `starter (Spring Boot)`.

Cada verbete: definição curta (1-3 linhas) em PT-BR + `Veja também:` apontando pra(s) nota(s) canônica(s) do galho. **Desambiguar `@Transactional (Spring)` do `@Transactional (Jakarta)`** já existente (linkar entre si). **Conferir 1:1** que os headings dos verbetes batem EXATAMENTE com as âncoras usadas nas notas (extrair as âncoras de Dicionário das notas via grep e conferir, como nos Galhos 4-7).

### 3.4. MOC central (ativação do Galho 8)

`03-Dominios/Tecnologia/Java/index.md` já existe. Task **mínima**: trocar a linha 38 (atualmente `8. Spring Core e Boot *(planejado)* — IoC/DI, AOP, auto-configuration, profiles, Actuator`) por wikilink ativo no padrão dos galhos fechados:

```markdown
8. [[03-Dominios/Tecnologia/Java/Spring Core e Boot/index|Spring Core e Boot]] — IoC/DI, beans e escopos, AOP/proxies, configuração e profiles, conditional/auto-configuration, eventos do contexto, fundamentos do Boot, Actuator
```

Atualizar `updated`. Não mexer no resto do MOC central.

### 3.5. Poda PARCIAL do tronco (`Backend/Spring Boot.md`)

**Poda parcial e delicada.** O tronco (1848 linhas, `publish: false`) mistura três galhos. Podar **só as seções core** (deste galho), substituindo cada uma por callout `[!nota] Migrado para galho próprio` com resumo + wikilinks pras notas novas. Formato herdado dos Galhos 2/3:

```markdown
> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Tecnologia/Java/Spring Core e Boot/index|Spring Core e Boot]]. Veja [[01 - ...]], [[02 - ...]].
```

**Seções a podar (core — deste galho):**

| Seção do tronco | Linhas (aprox.) | Substituir por callout → notas |
|---|---|---|
| `## O que é` | 19-49 | Callout no topo → nota 01 (manter o resto? ver nota abaixo) |
| `## Spring IoC Container — deep dive` (todo o bloco: BeanFactory/ApplicationContext, IoC/DI, Tipos de injeção, Bean lifecycle, Bean scopes, BeanPostProcessor, estereótipos, `@Configuration`/`@Bean`, Conditional beans) | 50-313 | Callout → notas 02, 03, 04, 05, 06, 07, 13, 14 |
| `## AOP e proxies — a mágica por baixo` (proxies, JDK/CGLIB, self-invocation, `@Transactional` private/final, advice types, pointcut) | 315-512 | Callout → notas 09, 10 |
| `## Configuração e Profiles — deep dive` (hierarquia, profiles, `@ConfigurationProperties`, `@Value`) | 822-983 | Callout → nota 12 |
| `## Actuator — production-ready features` | 984-1146 | Callout → nota 17 |
| `## Na prática (da minha experiência)` (fabricação órfã MedEspecialista) | 1799-1801 | **Higienizar** (remover/neutralizar — decisão do brainstorming; nenhum galho futuro é dono) |

**Observação sobre `## O que é`:** a seção tem um stack diagram + checklist de senior que referencia MVC/transações (galhos 9/10). Podar o conteúdo introdutório de Spring (→ nota 01) via callout no topo, **preservando** a checklist multi-galho como índice de transição enquanto o tronco existir, OU podar a seção inteira se o callout cobrir a função. **Decisão final na execução, lendo o tronco** (política §9 do roadmap: ler o tronco primeiro). Conservador: callout + manter o que aponta pra galhos ainda abertos.

**NÃO TOCAR (seções de outros galhos):**
- `## Gerenciamento de transações — @Transactional deep dive` (516-669) → Galho 10
- `## Spring MVC pipeline` (670-821) → Galho 9
- `## Spring WebFlux — visão geral` (1147) → Galho 11
- `## Spring Cloud — visão geral` (1183) → Galho 16
- `## Camadas típicas de uma aplicação Spring Boot` (1260) → cross-cutting (persistência/segurança/validation/testing — galhos 9-13)
- `## Troubleshooting em produção` (1435) → galhos 10/16/17
- `## Quando usar` / `## Armadilhas comuns` / `## How to explain in English` / `## Recursos` / `## Veja também` → gerais; atualizar só o "Veja também" pra linkar o MOC do galho.

**Não tocar nos troncos `Backend/Spring Data JPA.md` (Galho 10) nem `Backend/Kafka/` (Galho 14).** O `Veja também` final do tronco recebe wikilink pro MOC do Galho 8.

### 3.6. Dívida reversa (ganchos "Galho 8 / planejado")

Pré-flight localizou **9 ponteiros** (em 6 arquivos) a quitar após as notas existirem. Todos viram wikilinks pras notas do Galho 8; Spring deixa de ser texto "(planejado)" **nesses pontos específicos**:

| # | Arquivo:linha | Texto atual (resumo) | Vira wikilink pra |
|---|---|---|---|
| 1 | `Linguagem e sintaxe moderna/11 - Annotations.md:309` | "...e com o Galho 8 (Spring, planejado)." | nota 02 (IoC/DI) + MOC do galho |
| 2 | `Jakarta EE/index.md:30` | "o Spring ... é do Galho 8 (planejado)" | MOC do galho |
| 3 | `Jakarta EE/04 - CDI — beans e injeção.md:24` | "É isso que o `@Autowired` esconde ... Spring (Galho 8, planejado)" | **nota 02** (simetria-assinatura) |
| 4 | `Jakarta EE/05 - CDI — escopos e contextos.md:48` | "frameworks ... (Galho 8, planejado) reaproveitam o mesmo raciocínio" | nota 07 (ciclo de vida e escopos) |
| 5 | `Jakarta EE/06 - CDI — qualifiers, producers e eventos.md:42` | "frameworks de aplicação (Galho 8, planejado)" [eventos/pub-sub] | **nota 11** (eventos do ApplicationContext) |
| 6 | `Jakarta EE/12 - EJB ...:65` | "frameworks mais leves ... Galho 8 ... POJOs gerenciados por contêiner leve" | nota 02 (IoC) ou nota 01 |
| 7 | `Jakarta EE/12 - EJB ...:203` | "scheduler do servidor/framework do Galho 8" | nota 16 ou MOC do galho |
| 8 | `Jakarta EE/13 - CDI avançado ...:42` | "build-time resolution ... native ... Galho 8, planejado" | **nota 15** (auto-config/AOT) |
| 9 | `JavaFX/11 - Arquitetura ...:35,110` | "o Spring fica para o Galho 8 (planejado)" [DI em UI] | nota 02 (IoC/DI) |

Em todos, manter como texto "(planejado)" qualquer referência a galhos **ainda** inexistentes (9/10/11/12/13/16/17). Confirmar os números de linha na execução (podem ter deslocado).

## 4. Convenções por nota

Herda §7 do roadmap e §4 do spec do Galho 7. Reforços específicos:

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
  - spring
  - <fase>
  - <tags específicas: ioc, di, beans, aop, proxy, config, profiles, eventos, auto-config, boot, actuator, ...>
aliases:
  - <aliases opcionais>
---
```

H1 `# Título` após o frontmatter (padrão dos galhos publicados; o Galho 7 corrigiu isso retroativo).

### 4.2. Estrutura H2 obrigatória

- `> [!abstract] TL;DR` (callout, NÃO H2) — 2-4 linhas: conceito + regra prática + por que importa
- `## O que é` / `## Por que importa` / `## Como funciona` (≥3 subseções H3 em notas Adepto/Magus)
- `## Na prática` — exemplos compiláveis; framing **neutro** (`Order`/`Customer`/`Product`/`OrderService`/`CustomerRepository`); "padrão observado em aplicações Spring"; NUNCA `Patient`/`MedEspecialista`/"no meu projeto" (o tronco está cheio disso — **contraexemplo**)
- `## Armadilhas` — **≥2** (Iniciado) / **≥3** (Adepto/Magus), cada uma com descrição + exemplo curto de código demonstrando o problema + fix em 1 linha
- `## Em entrevista` — subheading `### Frase pronta (inglês)` com **3+ sentenças** (trade-off + decisão + caveat) + subheading `### Vocabulário` com tabela `| Termo PT | Termo EN |` de **6+ termos**
- `## Veja também` — wikilinks **SEM backticks**; sempre inclui notas relacionadas do galho + `[[03-Dominios/Tecnologia/Java/Spring Core e Boot/index|MOC do galho]]` + `[[03-Dominios/Tecnologia/Java/index|Trilha Java]]` + (quando espelhar spec) a nota do **Galho 7** correspondente + Galho 1 (Annotations) quando tocar em anotações + verbetes do Dicionário. **Evitar âncoras same-file `[[#Heading]]`** (falso-positivo no checker).
- `## Referências` — docs oficiais (`docs.spring.io/spring-boot/...`, `docs.spring.io/spring-framework/reference/...`, `spring.io/projects/...`). Afirmações version-specific fundadas em fonte verificada via WebFetch.

### 4.3. Restrições absolutas

1. **Fronteira-assinatura (linkar de volta ao Galho 7)** — todo conceito do Spring que espelha uma spec Jakarta aponta pra nota do Galho 7 ("mesma ideia da spec, implementação própria") **sem re-explicar a spec**. Galhos 9-17 = texto "(planejado)", sem wikilink.
2. **Sem fabricação** de experiência pessoal. Exemplos neutros (`Order`, `Customer`, `Product`) — NUNCA `Patient`/`josenaldo`/`MedEspecialista`/1ª pessoa. **O tronco é matéria-prima a higienizar, jamais a copiar.** **Zero estatística de adoção inventada** (regra dos Galhos 5/6/7) — vale pra capstone e pra nota 01.
3. **Sem invenção** de APIs/comportamentos. WebFetch obrigatório no Step 1 das notas de pesquisa (auto-config 15, starters, eventos 11, SpringApplication 16, AOT, capstone 18) e pra **toda afirmação version-specific**. Pontos minados verificados via WebFetch: `spring.factories` → `META-INF/spring/...AutoConfiguration.imports` (Boot 2.7+/3.x); Boot 3 baseline Java 17 e migração `javax`→`jakarta`; dependências circulares proibidas por default Boot 2.6+; versão atual do Spring Boot 3.x / Spring Framework 6.x. Fonte: `docs.spring.io` / `spring.io/projects/...` (sem o 403 do openjdk).
4. **Code samples compiláveis** — Java moderno (records, `var`, switch); imports `jakarta.*` quando tocar em specs (Boot 3); `properties`/`yaml` em fences corretas.
5. **Comparações justas** — `@ConfigurationProperties` vs `@Value`, `@Bean` vs scanning, JDK proxy vs CGLIB, Spring vs Jakarta: sempre "quando X" E "quando Y". A capstone (18) é o ápice (sem dogma, sem panfleto).
6. **Wikilinks sem backticks** em "Veja também"; MOC do galho + MOC central obrigatórios. **Não linkar galhos inexistentes** (9-17) — texto "(planejado)".
7. **Code fences corretos:** ` ```java ` pra código, ` ```xml ` pra Maven/descritores, ` ```properties `/` ```yaml ` pra config, ` ```text ` pra output/diagrama. Sempre fechadas.
8. **`fase:` no frontmatter + na tag** — obrigatório.
9. **Higiene de commits** — sem `Co-Authored-By: Claude`, sem `--no-verify`, `git add <path>` nominal (nunca `-A` — bot de backup Obsidian Git roda em timer), 1 commit por nota, controlador commita (subagents write-only).
10. **Tom pedagógico graduado** — Iniciado assume Galhos 1-2 + 7 (CDI básico); Magus assume o galho inteiro + Galhos 1-4-7.

## 5. Conteúdo por nota (síntese)

Esboço do recorte. Notas de **refator** partem do tronco refinado e higienizado; notas de **pesquisa** fundam-se em doc oficial via WebFetch. Fontes-base: `docs.spring.io/spring-boot/reference/`, `docs.spring.io/spring-framework/reference/core/` (IoC/AOP), `spring.io/projects/spring-boot`, `spring.io/projects/spring-framework`.

- **01 — O que é Spring (refator).** Spring Framework (o núcleo: IoC, AOP, MVC, tx) vs Spring Boot (auto-config, starters, embedded server, Actuator) vs projetos (Data/Security/Cloud) — o stack em camadas. "Opinionated"/convention-over-configuration; `start.spring.io`; `java -jar`. Boot 3.x: baseline Java 17, namespace `jakarta.*`. Armadilhas: confundir "Spring" com "Spring Boot"; achar que Boot é um framework separado do Framework. Fontes: spring.io/projects/spring-boot, docs.spring.io/spring-boot/.
- **02 — IoC e DI no Spring (refator, opus).** IoC: o framework controla criação e wiring; DI: a forma de implementar (o container injeta). Antes/depois (acoplamento → `final` injetado). O container como peça central. Comparação honesta com CDI (Galho 7): mesma ideia, container próprio do Spring, não uma impl de CDI. Armadilhas: `new` manual que ignora o container; field injection escondendo dependências (teaser da 04); achar que Spring "é" CDI. Fontes: docs.spring.io/spring-framework/reference/core/beans.
- **03 — Beans e estereótipos (refator).** Bean = objeto gerenciado pelo container; component scanning e `@ComponentScan`/`@SpringBootApplication`; `@Component` genérico; `@Service` (semântica); `@Repository` (+ tradução de exceções `DataAccessException`); `@Controller`/`@RestController` (citar, Galho 9). Armadilhas: classe fora do pacote escaneado (bean não encontrado); usar `@Component` onde a semântica pedia `@Repository` (perde tradução de exceção). Fontes: docs.spring.io (stereotype annotations, classpath scanning).
- **04 — Tipos de injeção (refator).** Constructor (recomendado: imutável `final`, fail-fast, testável sem Spring, sem reflection); setter (opcional); field `@Autowired` (evite: difícil testar, esconde deps, sem `final`, permite ciclos). Boot 2.6+ proíbe deps circulares por default. Armadilhas: field injection em código testável; `@Autowired` em construtor único (redundante desde Spring 4.3); dependência circular mascarada. Fontes: docs.spring.io (dependency injection).
- **05 — @Configuration e @Bean (refator).** Declarar beans explicitamente; quando (libs externas não-anotáveis, construção complexa, override condicional) vs scanning; `@Import`; `@Bean` + `@ConditionalOnMissingBean` (teaser da 14/15); full vs lite (`proxyBeanMethods`). Comparar com `@Produces` do CDI (Galho 7). Armadilhas: chamar método `@Bean` direto esperando o singleton (em lite mode não intercepta); esquecer que `@Bean` em `@Component` ≠ em `@Configuration`. Fontes: docs.spring.io (Java-based configuration, `@Bean`).
- **06 — ApplicationContext (refator).** `BeanFactory` (básico, lazy) vs `ApplicationContext` (enterprise: eventos, i18n, resource loading, environment) — o que você usa. Tipos concretos (servlet/reactive/standalone); `refresh()` (conceito); `*Aware` interfaces. Injetar o contexto (raro, code smell). Armadilhas: usar `getBean()` em vez de injeção (service locator anti-pattern); assumir lazy onde o contexto é eager. Fontes: docs.spring.io (`ApplicationContext`, `BeanFactory`).
- **07 — Ciclo de vida e escopos (refator).** Lifecycle completo (instanciação → populate → `*Aware` → BPP before → `@PostConstruct`/init → BPP after [proxies] → pronto → `@PreDestroy`/destroy); escopos (singleton default, prototype, request/session/application/websocket). Prototype-em-singleton: o singleton recebe **uma** instância; saídas (`ObjectProvider`, `@Lookup`, scoped proxy). Comparar com CDI escopos + client proxies (Galho 7 nota 05). Armadilhas: estado mutável em singleton (thread-safety — linka Galho 4); prototype injetado ingenuamente; lógica pesada em construtor vs `@PostConstruct`. Fontes: docs.spring.io (bean scopes, lifecycle callbacks).
- **08 — Qualificação de beans (refator + research).** Ambiguidade (2 beans do mesmo tipo → `NoUniqueBeanDefinitionException`); `@Qualifier` (custom annotation e por nome); `@Primary`; `@Profile` como condicional; injeção de `List<T>`/`Map<String,T>` (todos os beans do tipo); `@Order`. Comparar com qualifiers do CDI (Galho 7 nota 06). Armadilhas: dois `@Primary`; `@Qualifier` com nome errado (falha silenciosa vira erro de contexto); esquecer que `List<T>` injeta todos. Fontes: docs.spring.io (`@Qualifier`, `@Primary`, autowiring).
- **09 — AOP e proxies (refator, opus).** Cross-cutting concerns; o proxy intercepta a chamada externa e roda o advice; **JDK dynamic proxy** (interface) **vs CGLIB** (subclasse — default no Boot pra classes sem interface); advice types (`@Before`/`@After`/`@AfterReturning`/`@AfterThrowing`/`@Around`); pointcut expressions (`execution`, `@annotation`, `within`); `@Aspect`. É o mecanismo sob `@Transactional`/`@Async`/`@Cacheable`/`@PreAuthorize` (citar; comportamento = galhos 10/12). Comparar com interceptors do CDI (Galho 7 nota 13): **proxy-based vs interceptor-based**. Armadilhas: esperar AOP em chamada interna (teaser da 10); `@Aspect` sem `@Component`; pointcut largo demais (overhead). Fontes: docs.spring.io/spring-framework/reference/core/aop.
- **10 — Self-invocation e limites do proxy (refator).** A chamada interna (`this.metodo()`) não passa pelo proxy → advice ignorado; `@Transactional`/`@Async` em método `private` (CGLIB não intercepta) ou `final` (CGLIB não sobrescreve) silenciosamente ignorados. Por quê (o proxy só vê chamadas externas). Soluções: extrair pra outro bean (mais limpa), self-injection, anotar só o método de entrada público. Liga à 09 e ao limite equivalente do client proxy CDI (Galho 7 nota 05/13). Armadilhas: refatorar "puxando pra dentro" e quebrar `@Transactional`; método `@Async` `private`; achar que self-injection é elegante. Fontes: docs.spring.io (AOP proxying, understanding AOP proxies).
- **11 — Eventos do ApplicationContext (research).** `ApplicationEventPublisher.publishEvent`; eventos como POJO (desde Spring 4.2) ou `ApplicationEvent`; `@EventListener`; síncrono por default (no mesmo thread/transação); `@Async` events (linka Galho 4); `@TransactionalEventListener` (menção — comportamento tx = Galho 10); eventos built-in (`ContextRefreshedEvent`, `ApplicationReadyEvent`). Pub/sub in-process desacoplado. Comparar com eventos CDI `@Observes`/`Event<T>` (Galho 7 nota 06). Armadilhas: listener síncrono lento bloqueando o publisher; assumir transação no listener async; vazar evento entre contextos. Fontes: docs.spring.io (standard and custom events, `@EventListener`).
- **12 — Configuração e profiles (refator).** Hierarquia/precedência de fontes (args > env > system props > `application-{profile}` > `application` > defaults); profiles (`application-{profile}.yml`, `@Profile` em beans, ativação via `SPRING_PROFILES_ACTIVE`/arg/código); **`@ConfigurationProperties`** (binding tipado em record, `@Validated` → Bean Validation do Galho 7, relaxed binding, `@ConfigurationPropertiesScan`) vs **`@Value`**/SpEL. Armadilhas: secret hardcoded em `application.yml` (use env); `@Value` espalhado onde cabia binding tipado; profile errado em produção; relaxed binding mal-entendido (`max-retries` ↔ `maxRetries`). Fontes: docs.spring.io (externalized configuration, profiles, type-safe configuration properties).
- **13 — BeanPostProcessor e BeanFactoryPostProcessor (refator + research).** Os hooks de extensão: **BFPP** age nas *bean definitions* antes da instanciação (ex: `PropertySourcesPlaceholderConfigurer`); **BPP** age nas *instâncias* (`postProcessBeforeInitialization`/`AfterInitialization` — onde o `AbstractAutoProxyCreator` envolve beans em proxies AOP). Ordem (`Ordered`/`@Priority`). Por que BPPs são instanciados cedo (não podem ser proxiados por AOP). Comparar com portable/build-compatible extensions do CDI (Galho 7 nota 13). Armadilhas: injetar deps complexas num BPP (instanciado cedo demais); BPP que quebra a ordem do contexto. Fontes: docs.spring.io (`BeanPostProcessor`, `BeanFactoryPostProcessor`, container extension points).
- **14 — Conditional beans (refator + research).** `@Conditional` + interface `Condition`; os condicionais do Boot: `@ConditionalOnClass`/`OnMissingClass`, `@ConditionalOnBean`/`OnMissingBean`, `@ConditionalOnProperty` (+ `matchIfMissing`), `@ConditionalOnWebApplication`, `@ConditionalOnExpression`; ordem de avaliação e por que `@ConditionalOnMissingBean` cede pro usuário. É o tijolo da auto-config (liga à 15). Armadilhas: `@ConditionalOnMissingBean` por tipo errado; ordem de avaliação assumida; condicional em bean que outro condicional depende. Fontes: docs.spring.io (`@Conditional`, condition annotations).
- **15 — Auto-configuration e starters (research, opus).** `@SpringBootApplication` = `@EnableAutoConfiguration` + `@ComponentScan` + `@Configuration`; o registro via **`META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports`** (substituiu `spring.factories` no Boot 2.7+; **no Boot 3 só `.imports`** — WebFetch obrigatório); classes `@AutoConfiguration` usam `@Conditional` (liga à 14) e cedem pro usuário (`@ConditionalOnMissingBean`); ordem (`@AutoConfiguration(before/after)`); o que é um **starter** (POM agregador de dependências, *não* código); AOT/build-time (menção — native = Galho 17); debug (`--debug` → `ConditionEvaluationReport`, `/actuator/conditions`). Comparar com CDI Lite/build-time (Galho 7 nota 13). Armadilhas: criar starter achando que precisa de código; auto-config que não dispara (faltou `@ConditionalOnClass`); ordem de auto-config assumida; sobrescrever sem entender `@ConditionalOnMissingBean`. Fontes: docs.spring.io (auto-configuration, creating your own starter, `@SpringBootApplication`).
- **16 — SpringApplication e embedded server (research).** `SpringApplication.run()`: cria o `ApplicationContext`, dispara a auto-config, sobe o embedded server, roda `ApplicationRunner`/`CommandLineRunner`; fases e `SpringApplicationRunListener` (panorama); **embedded server** (Tomcat default; Jetty/Undertow via starter — escolha; tuning deep = Galho 9/17); fat/executable jar e layered jar (conceito — packaging deep = Galho 15/17); banner/exit codes (menção). O embedded server roda o Servlet container (Galho 7 nota 03). Armadilhas: lógica pesada no `main` em vez de runner/bean; assumir servidor externo (WAR) por hábito; bloquear o startup num runner. Fontes: docs.spring.io (`SpringApplication`, embedded web servers, executable jar).
- **17 — Actuator e observabilidade (refator + research).** `spring-boot-starter-actuator`; endpoints (`/health`, `/info`, `/metrics`, `/loggers`, `/conditions`, `/beans`, `/env`, `/mappings`); exposição (`management.endpoints.web.exposure`) e segurança (menção — auth = Galho 12); health groups + liveness/readiness (Kubernetes); custom `HealthIndicator`; **Micrometer** como fachada de métricas (conceito; Prometheus como exemplo). **Fronteira:** OpenTelemetry/distributed tracing/observabilidade profunda = Galho 17 (texto "(planejado)"). Armadilhas: expor todos os endpoints sem auth; health check pesado; confundir liveness com readiness. Fontes: docs.spring.io (Actuator, endpoints, health, Micrometer/metrics).
- **18 — Capstone: Spring sob o capô (research, opus).** Traçar o caminho do `SpringApplication.run()` ao bean pronto: scanning → bean definitions → BFPP → instanciação → DI → BPP → proxies AOP → `@PostConstruct` → contexto pronto; onde a auto-config entra. **Tabela Spring → Jakarta EE** (IoC↔CDI container, `@Autowired`↔`@Inject`, AOP proxy↔interceptors, `@Transactional` Spring↔JTA, `@Validated`↔Bean Validation, eventos↔`@Observes`, `@ConfigurationProperties`↔(sem equivalente direto)) — "dois caminhos pro mesmo problema". Decisão honesta Spring vs plataforma pura (Galho 7): quando cada um (sem dogma, **zero estatística inventada**). Munição de entrevista (frases sobre IoC, AOP, auto-config). Cheatsheet nota→problema. Armadilhas (de raciocínio): "auto-config é mágica" (é `@Conditional` + `.imports`); "Spring substituiu Jakarta" (implementa/consome várias specs); decidir framework por hype. Fontes: docs.spring.io (overview, the IoC container), spring.io/projects.

## 6. Pré-flight: verificações feitas

Executado nesta fase de brainstorming (2026-06-08); itens version-specific re-confirmados na execução de cada nota via WebFetch:

1. **Tronco mapeado** — `Backend/Spring Boot.md` (1848 linhas, `publish: false`, `status: evergreen`, `updated: 2026-04-11`) lido; seções core (deste galho) vs MVC (galho 9) vs transações (galho 10) vs cross-cutting (galhos 9-17) classificadas (§3.5).
2. **Fabricação confirmada** — 33 ocorrências de `Patient`/`Josenaldo`/`MedEspecialista`/1ª pessoa (grep). Pior bloco: `## Na prática (da minha experiência)` (linha 1799, MedEspecialista 1ª pessoa). **Decisão do brainstorming: higienizar agora** (bloco órfão, sem dono em galho futuro). Demais ocorrências em seções core somem com a poda (substituídas por callout); as em seções de galhos 9/10 ficam pra eles.
3. **Dívida reversa localizada** — 9 ganchos em 6 arquivos (§3.6); confirmar linhas na execução.
4. **Dicionário** — **202 verbetes** (não 166); seção alfabética única `## A`…`## Z`; verbetes `### `; `updated: 2026-06-07`; nenhum verbete Spring (`client proxy (CDI)` é do Galho 7, intacto). Expansão alfabética, nunca recriar/reordenar.
5. **MOC central** — `03-Dominios/Tecnologia/Java/index.md:38` é a linha do Galho 8 (`*(planejado)*`); galhos ativos usam `N. [[path/index|Title]] — summary`; `updated: 2026-06-07`.
6. **Troncos intocáveis** — `Backend/Spring Data JPA.md` (Galho 10), `Backend/Kafka/` (Galho 14).
7. **Versões a cravar via WebFetch na execução** — Spring Boot 3.x atual e Spring Framework 6.x (baseline Java 17, namespace `jakarta.*`); `AutoConfiguration.imports` vs `spring.factories` (Boot 2.7+/3.x); deps circulares proibidas por default Boot 2.6+. Fonte: `docs.spring.io` / `spring.io/projects/...`.

Nenhum número de adoção é inventado. Quando faltar fato verificável, **PERGUNTAR** antes de escrever.

## 7. Critérios de aceitação do galho

Além dos critérios gerais (§10 do roadmap):

1. 18 notas em `03-Dominios/Tecnologia/Java/Spring Core e Boot/`, frontmatter completo com `fase:`, `publish: true`, distribuídas 5/7/6.
2. MOC do galho com 3 subseções de fase + 5 rotas alternativas + dataview + folder-link resolve (`index.md` presente).
3. Dicionário de Java **expandido** (não recriado) com ~37 verbetes; verbetes dos Galhos 1-7 intactos; `updated` atualizado; `@Transactional (Spring)` desambiguado do `@Transactional (Jakarta)`; headings conferidos 1:1 com as âncoras usadas nas notas (via grep).
4. MOC central `Java/index.md` com Galho 8 ativado (linha 38 vira wikilink); resto intacto.
5. **Poda parcial executada**: seções core (`## O que é`, `## Spring IoC Container`, `## AOP e proxies`, `## Configuração e Profiles`, `## Actuator`) substituídas por callouts `[!nota] Migrado para galho próprio` + wikilinks; `## Na prática (da minha experiência)` higienizada. **Seções de galhos 9/10/11/16/17 intactas** (`## Gerenciamento de transações`, `## Spring MVC pipeline`, WebFlux/Cloud/Camadas/Troubleshooting). `Spring Data JPA.md`/`Kafka/` intactos.
6. **Dívida reversa quitada**: os 9 ganchos com wikilinks corretos (CDI 04:24→nota 02, CDI 06:42→nota 11, CDI 13:42→nota 15, etc.); galhos ainda inexistentes (9-17) permanecem texto "(planejado)".
7. Cada nota: TL;DR; code samples compiláveis (Java moderno, `jakarta.*` quando spec, fences corretas); "Em entrevista" com `### Frase pronta (inglês)` 3+ sentenças + `### Vocabulário` tabela 6+ termos PT→EN; "Armadilhas" com exemplo+fix (≥2 Iniciado, ≥3 Adepto/Magus); wikilinks (galho + MOC central + Galho 7 quando espelhar spec + Galho 1/4 quando conectar + Dicionário); "Referências" com docs oficiais verificadas.
8. **Fronteira-assinatura respeitada**: cada conceito que espelha spec Jakarta linka de volta ao Galho 7 sem re-explicar a spec; galhos 9-17 só como texto "(planejado)"; nenhum wikilink pra galho inexistente.
9. **Fronteiras de escopo respeitadas**: `@Transactional` aqui só como mecanismo AOP (comportamento = Galho 10); `@Controller`/REST só citado (Galho 9); zero conteúdo de Security/WebFlux/Test/Cloud/native.
10. Zero fabricação de experiência pessoal; zero estatística de adoção inventada; afirmações version-specific citam a versão verificada via WebFetch.
11. 1 commit por nota; sem `Co-Authored-By: Claude`; sem `--no-verify`; stage nominal (nunca `-A`); subagents write-only, controlador commita.
12. `verificar-wikilinks` roda limpo na pasta do galho (as ~204 quebras legadas da árvore Java NÃO são deste galho; evitar âncoras same-file).

## 8. Riscos e mitigações

| Risco | Mitigação |
|---|---|
| **Re-explicar a spec Jakarta** em vez de linkar de volta (fronteira-assinatura invertida) | Restrição 4.3.1; review por fase checa cada nota que espelha spec; capstone mapeia em tabela; cada conceito espelhado tem wikilink obrigatório pro Galho 7. |
| **Invadir Galho 9 (MVC) ou 10 (transações)** ao falar de `@Transactional`/controllers | Fronteira dura declarada (§3.1, §3.5): AOP só como mecanismo; `@Controller` só citado; review por fase. Poda NÃO toca `## Spring MVC pipeline` nem `## Gerenciamento de transações`. |
| **Poda parcial danificar seções de outros galhos** (tronco de 1848 linhas) | Ler o tronco primeiro (§9 roadmap); podar só as 5 seções core listadas; tabela de linhas em §3.5; seções 9/10/11/16/17 explicitamente intocáveis; mudança via commit reversível. |
| **Copiar fabricação do tronco** (`Patient`/MedEspecialista) pras notas novas | Tronco é contraexemplo (restrição 4.3.2); exemplos neutros `Order`/`Customer`; review por fase grep `Patient|MedEspecialista|minha`. |
| **Inventar API "de memória"** nas notas de pesquisa (auto-config, eventos, SpringApplication, AOT) | WebFetch no Step 1 dessas notas; `spring.factories`→`.imports` é o ponto mais minado (Boot 2.7+/3.x) — verificar; Referências com fonte oficial. |
| Versões envelhecerem (Boot 3.x, AOT, namespace) | Versões hedged; WebFetch por nota version-specific; declarar version-specificity no corpo. |
| Galho denso (18 notas) inflar nº de notas ou notas individuais | Distribuição 5/7/6 fixada; se uma nota passar de ~600 linhas, dividir nota (não galho); capstone com cheatsheet enxuto. |
| Dicionário: duplicar `@Transactional` ou reordenar verbetes | `@Transactional (Spring)` ≠ `@Transactional (Jakarta)` — verbetes separados que se linkam; inserção alfabética, nunca recriar; conferir âncoras 1:1. |
| Bot de backup (Obsidian Git) commitando no meio | Padrão dos Galhos 2/3/6/7: subagents write-only; controlador commita imediatamente após cada nota com `git add` nominal (nunca `-A`). |
| openjdk.org 403 no WebFetch | Não se aplica — fontes são `docs.spring.io`/`spring.io` (sem esse problema). Pra Jakarta usar `jakarta.ee` (Galho 7). |

## 9. Próximos passos

1. **Aprovação deste spec**
2. **Plano de execução** via skill `superpowers:writing-plans` → `docs/superpowers/plans/2026-06-08-java-galho-08-spring-core-execution.md`
3. **Execução** via `superpowers:subagent-driven-development` **direto na `main`** (subagents write-only; sonnet por padrão, opus nas notas 02/09/15/18; review **por fase** + fix loop; push manual do usuário)
4. **Verificação** de wikilinks + conferência de âncoras do Dicionário
5. **Atualização da memória** `project_trilha_java` (Galho 8 completo) antes do próximo galho

## 10. Documentos relacionados

- `2026-06-02-java-senior-roadmap-design.md` — roadmap macro (18 galhos)
- `2026-06-07-java-galho-07-jakarta-ee-design.md` / `...-execution.md` — Galho 7 (dependência direta; template mais recente; dono das specs que o Spring implementa)
- `2026-06-04-java-galho-02-collections-streams-design.md`, `2026-06-05-java-galho-03-jvm-design.md` — templates de **poda parcial** de tronco monolítico
- Artefatos a atualizar: `03-Dominios/Tecnologia/Java/Dicionário de Java.md`, `03-Dominios/Tecnologia/Java/index.md`, `03-Dominios/Tecnologia/Java/Backend/Spring Boot.md` (poda parcial + higiene), `Linguagem e sintaxe moderna/11 - Annotations.md`, `Jakarta EE/index.md`, `Jakarta EE/04`, `05`, `06`, `12`, `13`, `JavaFX/11 - Arquitetura — MVC, MVVM e injeção de dependência.md` (dívida reversa)
- Fontes-base do galho: `docs.spring.io/spring-boot/reference/`, `docs.spring.io/spring-framework/reference/core/`, `spring.io/projects/spring-boot`, `spring.io/projects/spring-framework`
- Memórias: [[project_trilha_java]], [[project_trilhas_fases_aprendizado]], [[project_tronco_galhos_pattern]], [[feedback_galhos_direto_main]], [[feedback_no_fabrication]], [[feedback_quartz_index]], [[feedback_commits]]
