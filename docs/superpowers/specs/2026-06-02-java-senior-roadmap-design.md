---
title: "Spec — Roadmap Java Senior (Tronco e Galhos)"
date: 2026-06-02
author: Josenaldo
status: draft
type: spec
publish: false
---

# Spec — Roadmap Java Senior

## 1. Contexto e motivação

O Codex Technomanticus tem em `03-Dominios/Tecnologia/Java/` um conjunto de **troncos densos** acumulados — notas monolíticas, em sua maioria `publish: false`/`status: evergreen`, que cobrem grandes áreas da plataforma Java com profundidade real mas formato saturado:

| Tronco | Linhas | Cobertura |
|---|---|---|
| `Core/Helsinki MOOC — Guia de Revisão.md` | 2371 | Curso de iniciantes (Universidade de Helsinki) |
| `Backend/Spring Boot.md` | 1848 | IoC, AOP, MVC, Actuator, Cloud |
| `Core/Java Fundamentals.md` | 1660 | Linguagem 8→25 + JVM + Collections/Streams |
| `Core/Java Concurrency.md` | 1579 | Memory Model, locks, CompletableFuture, Virtual Threads |
| `Backend/Spring Data JPA.md` | 1312 | JPA, Hibernate, fetch, N+1, transações |
| `Backend/Spring Security.md` | 1116 | Auth, JWT, OAuth2, CSRF, CORS |
| `Core/Certificação Java OCP.md` | 877 | Guia da prova OCP Java SE 21 |
| `Backend/Testes em Java.md` | — | JUnit 5, Mockito, AssertJ, Testcontainers |
| `Backend/Kafka/` | ~20 notas | Galho já estruturado (Kafka Concepts) |
| `Frontend/JavaFX.md` | 161 | GUI desktop (stub) |

Em paralelo, a estrutura atual usa um agrupamento intermediário `Core/Backend/Frontend` com MOCs genéricos (`Java/index.md`, `Java/Java.md`).

A tensão é a mesma que originou a trilha Node: o conteúdo precisa **florescer**. Conceitos que merecem nota própria estão amassados em uma seção de um monolito; vocabulário de entrevista internacional não tem onde morar; a profundidade de cada tema é limitada pelo formato.

**Metáfora orientadora:** cada monolito é um **tronco**. Esta trilha **enriquece os troncos até eles darem galhos**. Cada galho é uma sub-trilha temática, organizada em 3 fases de aprendizado (Iniciado/Adepto/Magus). Cada nota atômica é uma folha. À medida que um galho amadurece, a seção correspondente do tronco é podada — substituída por um callout com wikilink. A decisão final sobre o destino de cada tronco emerge depois de alguns galhos fecharem.

**Diferença em relação ao roadmap Node:** Java é uma plataforma de superfície muito maior (linguagem + JVM + Jakarta EE + Spring + desktop + build + cloud), então a trilha tem **18 galhos** (vs 6 do Node) e adota o esquema de **3 fases por galho** (Iniciado/Adepto/Magus), padrão estabelecido em 2026-05-18 com a trilha Terminal e ausente no Node legado.

## 2. Objetivo

Definir o roadmap de **18 sub-trilhas temáticas (galhos)** que progressivamente enriquecem e substituem os troncos monolíticos, estabelecendo:

- **Topologia** flat sob `03-Dominios/Tecnologia/Java/` (abandonando `Core/Backend/Frontend`), consistente com Node e IA
- **Padrões editoriais comuns** herdados por todos os galhos (frontmatter, estrutura de nota, 3 fases, idioma, audiência, restrições)
- **Escopo de blocos** de cada galho (sem nomear notas individuais — isso fica pro spec específico de cada galho)
- **Dependências** entre galhos e **ordem sugerida**
- **Política de poda** dos troncos à medida que galhos fecham
- **Artefatos transversais** (Dicionário de Java, MOC central)
- **Critério de "galho fechado"**

Este roadmap **não detalha** o nota-a-nota dos galhos. Cada galho ganha seu próprio spec quando for o momento de executá-lo. A única exceção é o **Galho 1 (Linguagem e sintaxe moderna)**, que tem spec completo coexistindo: `2026-06-02-java-galho-01-linguagem-design.md`.

## 3. Escopo

### Em escopo

- 18 sub-trilhas (galhos) progressivamente publicadas em `03-Dominios/Tecnologia/Java/<Nome do Galho>/`
- Reorganização da topologia para flat temático (migração de `Core/Backend/Frontend` para galhos)
- Padrões editoriais comuns + esquema de 3 fases que todo galho herda
- Política de poda dos troncos à medida que galhos fecham
- Artefato transversal **Dicionário de Java** (`type: glossary`), semeado pelo Galho 1
- MOC central `Java/index.md` reescrito no estilo Node, agregando galhos à medida que fecham
- Critérios de aceitação aplicáveis a qualquer galho

### Fora de escopo

- **Detalhamento nota-a-nota** dos galhos 2-18 — cada um ganha seu spec quando começar
- **Refactor estrutural dos troncos** antes do galho correspondente fechar — a decisão sobre o destino de cada tronco emerge da experiência de podar
- **Versão em inglês** das notas — derivação futura, projeto separado
- **Migração do Kafka existente** para formato 3-fases — o galho de Mensageria (12) decide se reaproveita as ~20 notas como estão ou refatora; não antecipar
- **Reformar `Java.md`** (o MOC duplicado) — será deprecado/fundido no `Java/index.md` reescrito; decidir quando o MOC central for atualizado
- **Helsinki MOOC** como galho — permanece como nota de referência/revisão para iniciantes (não vira galho); recebe wikilinks dos galhos relevantes

## 4. Audiência e barra de qualidade

**Audiência primária:** dev senior em preparação para entrevista internacional. Já programa em Java há anos, conhece OOP e sintaxe, mas precisa **dominar fluentemente** o vocabulário moderno (records, sealed, virtual threads, pattern matching), explicar mecânicas da JVM e do Spring em inglês, e reconhecer patterns idiomáticos e armadilhas em code review. Cada nota tem seção "Em entrevista" obrigatória.

**Audiência secundária:** o mesmo dev em produção, tomando decisões de arquitetura e debugando comportamentos de produção (N+1, leaks, GC pauses, contention, falhas de resiliência). Cada galho tem rotas alternativas no MOC priorizando produção/troubleshooting.

**Barra de qualidade:** ao terminar um galho, o leitor deve conseguir:

1. Explicar em inglês o conceito central com vocabulário preciso
2. Identificar armadilhas concretas que o galho cobre
3. Decidir e justificar escolhas de design relacionadas ao tema (não "implementar from scratch" — essa régua é exagerada; a barra é "decidir, justificar, reconhecer patterns e armadilhas em code review")
4. Diagnosticar problemas relacionados ao tema em produção

## 5. Topologia e os 18 galhos

Estrutura **flat** sob `03-Dominios/Tecnologia/Java/` — cada galho é uma pasta com numeração local e MOC homônimo (`index.md`). O agrupamento `Core/Backend/Frontend` é abandonado; os MOCs antigos `Core/index.md`, `Backend/index.md`, `Frontend/index.md` são absorvidos pelo MOC central reescrito.

Ordem **didática** (= ordem de leitura recomendada). A ordem de **execução** (qual galho construir primeiro) é decisão separada — ver §6.

### Núcleo da linguagem (galhos 1-4)

#### Galho 1 — Linguagem e sintaxe moderna
**Escopo.** Tipos e operadores, controle de fluxo, strings/text blocks, arrays, OOP (classes, herança, polimorfismo, interfaces/abstratas, enums), exceções, annotations, generics, e as features modernas que definem o Java atual (records, sealed classes, pattern matching, switch expressions). Evolução da linguagem Java 8→25 (LTS, preview).
**Dependências:** nenhuma. Base de todos os outros galhos.
**Tronco a podar:** `Core/Java Fundamentals.md` (seções de linguagem; JVM, Collections, Streams e Concorrência saem pra galhos 3/2/4).
**Spec próprio:** `2026-06-02-java-galho-01-linguagem-design.md`.

#### Galho 2 — Collections, Streams e Programação Funcional
**Escopo.** Collections Framework (hierarquia, escolha de estrutura, `Comparable`/`Comparator`), Stream API (pipeline, intermediárias/terminais, collectors, streams primitivos, paralelos), lambdas e interfaces funcionais, `Optional`, composição de funções, Date/Time API, I/O moderno (`java.nio.file`, try-with-resources).
**Dependências:** Galho 1 (genéricos, interfaces).
**Tronco a podar:** seções correspondentes de `Core/Java Fundamentals.md`.

#### Galho 3 — JVM por dentro
**Escopo.** Memory model (heap/stack/metaspace), Garbage Collection (G1, ZGC, Shenandoah, escolha e tuning), JIT (C1/C2, warmup, tiered), classloading, bytecode, sistema de módulos (JPMS), diagnóstico (heap dump, GC logs, JFR), performance da JVM.
**Dependências:** Galho 1.
**Tronco a podar:** seção JVM de `Core/Java Fundamentals.md`.

#### Galho 4 — Concorrência e paralelismo
**Escopo.** Java Memory Model (happens-before, volatile), threads e lifecycle, `synchronized`/locks/`java.util.concurrent`, executors e thread pools, `CompletableFuture`, **Virtual Threads / Project Loom**, structured concurrency, parallel streams, armadilhas de contention e deadlock.
**Dependências:** Galho 1; Galho 3 (memory model) ajuda.
**Tronco a podar:** `Core/Java Concurrency.md`.

### Interfaces desktop (galhos 5-6)

#### Galho 5 — Swing
**Escopo.** Componentes, containers e layout managers, modelo de eventos, Event Dispatch Thread (EDT) e `SwingWorker`, MVC em Swing, Look & Feel, **estado atual de adoção/manutenção** da API (modo de manutenção, papel hoje). Posicionado após Concorrência por causa do EDT.
**Dependências:** Galho 1, Galho 4 (EDT/threading).
**Tronco a podar:** nenhum (galho novo).

#### Galho 6 — JavaFX
**Escopo.** Scene graph, FXML e Scene Builder, properties e binding, CSS, controls, `Task`/`Service` e threading (`Platform.runLater`), **estado atual do projeto** (OpenJFX, governança pós-Oracle, releases). Comparação Swing vs JavaFX.
**Dependências:** Galho 1, Galho 4, Galho 5 (comparação).
**Tronco a podar:** `Frontend/JavaFX.md`.

### Fundamentos enterprise e Spring (galhos 7-13)

#### Galho 7 — Jakarta EE
**Escopo.** A plataforma que o Spring abstrai. CDI (injeção, escopos, qualifiers), Servlet API, JAX-RS (REST), Bean Validation, JPA spec, JTA (transações), e o legado EJB. Transição Java EE → Jakarta EE (namespace `javax` → `jakarta`).
**Dependências:** Galhos 1-2.
**Tronco a podar:** nenhum (galho novo).

#### Galho 8 — Spring Core e Boot
**Escopo.** IoC/DI, ciclo de vida de beans, AOP, configuração e profiles, auto-configuration, starters, properties/`@ConfigurationProperties`, eventos do contexto, fundamentos do Boot.
**Dependências:** Galhos 1, 7 (Spring implementa specs Jakarta).
**Tronco a podar:** `Backend/Spring Boot.md` (parte core).

#### Galho 9 — Web e APIs REST
**Escopo.** Spring MVC, REST controllers, content negotiation, exception handling (`@ControllerAdvice`, Problem Details), validation, OpenAPI/Swagger, HATEOAS, versionamento de API, `RestClient`/`WebClient`.
**Dependências:** Galho 8.
**Tronco a podar:** `Backend/Spring Boot.md` (parte MVC/web).

#### Galho 10 — Persistência de dados
**Escopo.** JPA/Hibernate, Spring Data JPA, mapeamento e relacionamentos, fetch strategies e o problema N+1, transações (`@Transactional`, propagação, isolamento), caching (1º/2º nível), paginação, query methods/JPQL/Criteria, migrations (Flyway/Liquibase).
**Dependências:** Galhos 7, 8.
**Tronco a podar:** `Backend/Spring Data JPA.md`.

#### Galho 11 — Programação Reativa
**Escopo.** Project Reactor (`Mono`/`Flux`, operadores), backpressure, Spring WebFlux, R2DBC, comparação imperativo vs reativo, quando (não) usar reativo.
**Dependências:** Galhos 4, 8, 9.
**Tronco a podar:** nenhum (galho novo).

#### Galho 12 — Segurança
**Escopo.** Spring Security (filter chain, authn/authz), JWT, OAuth2/OIDC, method security, CSRF/CORS, password encoding, RBAC, OWASP no contexto Java.
**Dependências:** Galhos 8, 9.
**Tronco a podar:** `Backend/Spring Security.md`.

#### Galho 13 — Testes
**Escopo.** JUnit 5 (lifecycle, parametrização, extensions), Mockito, AssertJ, Spring Boot Test e test slices (`@WebMvcTest`, `@DataJpaTest`), Testcontainers, integração, contract testing, estratégias e pirâmide de testes.
**Dependências:** Galhos 1, 8 (slices precisam de Spring).
**Tronco a podar:** `Backend/Testes em Java.md`.

### Plataforma distribuída e produção (galhos 14-17)

#### Galho 14 — Mensageria e eventos
**Escopo.** Apache Kafka (reaproveitando/refatorando o galho Kafka existente), RabbitMQ, Spring events e `@EventListener`, padrões event-driven, idempotência, outbox. Inclui gRPC (migra a nota `Backend/gRPC e Go.md`).
**Dependências:** Galhos 4, 8.
**Tronco a podar:** integra `Backend/Kafka/` e `Backend/gRPC e Go.md`.

#### Galho 15 — Build, tooling e ecossistema
**Escopo.** Maven (lifecycle, dependency management, BOM, multi-module), Gradle (DSL, build cache), gestão de dependências e conflitos, plugins essenciais, formatação/linting, JDK distributions (Temurin, GraalVM) e gestão de versões (SDKMAN).
**Dependências:** Galho 1.
**Tronco a podar:** nenhum (galho novo).

#### Galho 16 — Microservices e sistemas distribuídos
**Escopo.** Arquitetura de microservices, Spring Cloud (config, gateway, service discovery), resilience (circuit breaker, retry, bulkhead — Resilience4j), saga pattern, distributed tracing, comunicação inter-serviços.
**Dependências:** Galhos 8, 9, 12, 14.
**Tronco a podar:** nenhum (galho novo).

#### Galho 17 — Cloud-native e produção
**Escopo.** Containerização (Docker, buildpacks, layered jars), **GraalVM native image** (AOT, reflection config, trade-offs), observability (Actuator, Micrometer, OpenTelemetry), profiling e performance em produção, graceful shutdown, health checks, deploy.
**Dependências:** Galhos 3, 8, 16.
**Tronco a podar:** nenhum (galho novo).

### Certificação (galho 18)

#### Galho 18 — Certificação Java OCP
**Escopo.** Guia da prova OCP Java SE 21 (1Z0-830): tópicos cobrados, formato, armadilhas de prova, mapeamento dos tópicos da prova para os galhos 1-4 (a maior parte do conteúdo já existe nos galhos de linguagem). Notas focadas em "o que a prova cobra e como ela tenta te pegar", não re-explicar a linguagem.
**Dependências:** Galhos 1-4 (a prova é sobre a linguagem/JVM).
**Tronco a podar:** `Core/Certificação Java OCP.md`.

### Fora dos galhos (referência)

- `Core/Helsinki MOOC — Guia de Revisão.md` — permanece como nota de referência para iniciantes; recebe wikilinks do Galho 1.

## 6. Ordem de execução sugerida

A ordem **didática** (§5) não é a ordem de **execução**. Sugestão de execução, puxada pelo valor de entrevista e pela disponibilidade de tronco rico pra refatorar:

1. **Galho 1 (Linguagem e sintaxe moderna)** — agora; base de tudo, tronco rico, valida o padrão. Spec próprio nesta rodada.
2. **Galho 4 (Concorrência)** ou **Galho 8 (Spring Core e Boot)** — temas de altíssimo valor de entrevista, troncos ricos.
3. **Galho 2 (Collections/Streams)** e **Galho 3 (JVM)** — completam o núcleo da linguagem.
4. **Galhos 9-10-12-13 (Web, Persistência, Segurança, Testes)** — o miolo backend Spring.
5. **Galhos 5-6 (Swing/JavaFX)**, **7 (Jakarta EE)**, **11 (Reativa)**, **14-17 (mensageria/build/microservices/cloud)** — conforme necessidade real puxar.
6. **Galho 18 (OCP)** — por último; depende dos galhos de linguagem estarem maduros (mapeia pra eles).

A ordem é sugestão, não compromisso. Galhos podem ser reordenados quando a necessidade real (entrevista marcada, projeto, certificação agendada) puxar um pra frente. Cada galho ganha spec próprio quando começar, com revalidação de dependências.

## 7. Padrões editoriais herdados

Todo galho herda os padrões abaixo. Desvios são justificados no spec do galho. Padrões consolidados nas trilhas Node (tronco/galhos) e Terminal (3 fases).

### 7.1. Localização e nomenclatura

- Pasta `03-Dominios/Tecnologia/Java/<Nome do Galho>/`, flat (sem subpastas por fase — fase é organização lógica)
- Numeração local global por galho (`01 - <título>.md`, `02 - ...`), **não reinicia por fase**
- MOC do galho em `index.md` na raiz da pasta, `type: moc`
- MOC central `03-Dominios/Tecnologia/Java/index.md` atualizado a cada galho que fecha

### 7.2. As 3 fases de aprendizado

Cada galho organiza suas notas em 3 fases progressivas (ver [[project_trilhas_fases_aprendizado]]):

| Fase | Nível | Profundidade | Objetivo |
|---|---|---|---|
| **Iniciado** | júnior | visão geral | Vocabulário, modelo mental, sintaxe suficiente pra começar |
| **Adepto** | pleno | moderada | Domínio operacional — usar com confiança |
| **Magus** | senior | profunda | Maestria — técnicas avançadas, decisões de arquitetura |

- Frontmatter de nota: campo obrigatório `fase: iniciado | adepto | magus` + a fase no array de `tags`
- MOC do galho agrupa wikilinks em 3 subseções (`## Iniciado` / `## Adepto` / `## Magus`)
- Distribuição de referência: Iniciado ~35%, Adepto ~37%, Magus ~28% (sem regra rígida; Magus pode crescer em galhos complexos como Concorrência, JVM, Reativa)
- Iteração **vertical por galho**: cada galho fecha as 3 fases na mesma sessão de execução

### 7.3. Frontmatter padrão por nota

```yaml
---
title: "<título sem prefixo numérico>"
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
type: concept
status: seedling
publish: true
fase: iniciado | adepto | magus
tags:
  - java
  - <galho-tag: linguagem, collections, jvm, concorrencia, swing, javafx, jakarta-ee, spring, web, persistencia, reativa, seguranca, testes, mensageria, build, microservices, cloud-native, ocp>
  - <fase>
  - <conceito-tag: 1-3 específicas>
aliases:
  - <opcional>
---
```

MOCs usam `type: moc`.

### 7.4. Estrutura padrão por nota

```markdown
# <Título>

> [!abstract] TL;DR
> <2-4 linhas. Conceito central + regra prática + por que importa.>

## O que é

## Por que importa

## Como funciona

## Na prática

## Armadilhas

## Em entrevista

## Veja também
```

Variações permitidas quando o conteúdo pedir (nota de fechamento pode ter "Cheatsheet"). Esqueleto é referência, não gabarito rígido. **Tamanho típico:** 200-500 linhas; até 700 quando o tema pedir (concorrência baixo nível, decision trees) — não impor limite artificial.

### 7.5. Idioma e tom

- **PT-BR exclusivo** nesta fase
- Termos técnicos mantidos em inglês (garbage collection, virtual threads, backpressure, bean, etc.) — não traduzir o que o ecossistema não traduz
- Seção "Em entrevista" tem **frase pronta em inglês com 3+ sentenças** (trade-off + decisão + caveat — NÃO one-liner) + **vocabulário-chave** com 6+ termos PT→EN traduzidos
- Tom técnico mas acessível; TL;DR sempre presente; pedagógico em Iniciado, sobe até Magus

### 7.6. Versões assumidas

- **Java 21 LTS** (baseline) e **Java 25 LTS** (2025) como referências de "moderno"
- Menções a Java 17 LTS quando relevante (ainda comum em produção)
- Spring Boot 3.x / Spring 6.x (Jakarta namespace), Spring Framework atual
- Versões declaradas no frontmatter ou no corpo quando o tema for version-specific (ex: primitive patterns Java 23+, structured concurrency)
- Preferir hedge ("Java 21+; verifique a feature na sua versão") a pins que envelhecem mal em features preview

### 7.7. Code samples

- Java moderno (records, var, switch expressions, text blocks) onde idiomático
- Mínimo de 3-5 code samples por nota conceitual (notas panorâmicas podem ter menos)
- Comentários em PT-BR onde didáticos
- Compiláveis/testáveis quando possível (jshell, JBang, scripts standalone)
- Code fences corretos: ` ```java `, ` ```xml ` (Maven/config), ` ```properties `/` ```yaml ` (config Spring), ` ```text ` (output/bytecode). Sempre fechadas.

### 7.8. Wikilinks

- Densidade alta. Sempre que possível linkar pra:
  - O tronco correspondente (ex: `[[Java Fundamentals]]`) enquanto ele existir
  - Outras notas do mesmo galho
  - Notas de outros galhos quando o conceito conectar (ex: pattern matching ↔ sealed classes)
  - Verbetes do **Dicionário de Java**
  - `[[03-Dominios/Tecnologia/Java/index|Java (MOC central)]]`

### 7.9. Restrição absoluta de fabricação

A memória [Nunca inventar dados sobre o usuário](/home/josenaldo/.claude/projects/-home-josenaldo-repos-personal-codex-technomanticus/memory/feedback_no_fabrication.md) é regra inegociável.

**Nenhuma nota pode atribuir ao autor experiências profissionais, projetos, clientes, métricas ou casos não-vividos.** Atenção especial: vários troncos atuais têm seções tipo `## Na prática (da minha experiência)` (ex: `Java Fundamentals.md` linha ~1614) — esse conteúdo deve ser **higienizado** na poda, reescrito como padrão neutro/hipotético explícito. A seção "Na prática" das notas novas usa:

- "Padrão observado no ecossistema (Spring, Hibernate, JDK)"
- "Caso típico em serviço enterprise"
- "Armadilha comum reportada na comunidade"
- Citações com fonte verificável (docs oficiais, JEPs, talks identificadas, repos públicos)
- Hipotéticos explícitos ("Imagine um serviço que processa pedidos...")

Quando faltar contexto factual, **PERGUNTAR antes de escrever** — nunca preencher com plausibilidade.

### 7.10. Higiene de commits

- Sem `Co-Authored-By: Claude` (ver [[feedback_commits]])
- Sem `--no-verify`
- Stage explícito por arquivo (`git add <path>` nominal; nunca `git add -A`)
- 1 commit por nota (não bundled) quando executado por agente — preserva rastreabilidade

## 8. Artefatos transversais

### 8.1. Dicionário de Java (novo)

`03-Dominios/Tecnologia/Java/Dicionário de Java.md`, `type: glossary`, no padrão dos outros domínios (`Dicionário de IA`, `Dicionário do Terminal`, `Dicionário de React`). **Criado e semeado pelo Galho 1**, expandido por cada galho subsequente com seus verbetes. Cada verbete tem `Veja também:` apontando pras notas canônicas. Inserção em ordem alfabética case-insensitive.

### 8.2. MOC central reescrito

`03-Dominios/Tecnologia/Java/index.md` reescrito no estilo `Node/index.md`: TL;DR descrevendo a trilha de 18 galhos, lista de galhos com descrição (agregada à medida que fecham), "Veja também" (JavaScript, TypeScript). O `Java/Java.md` duplicado é deprecado/fundido nessa reescrita; os MOCs `Core/Backend/Frontend/index.md` são absorvidos.

## 9. Política de poda dos troncos

Cada galho, ao fechar, executa uma **task de poda** do(s) tronco(s) correspondente(s):

1. **Ler o tronco primeiro** pra confirmar níveis reais de heading (podem divergir do spec)
2. **Identificar** seções do tronco no escopo do galho
3. **Substituir** cada seção por callout com resumo + wikilinks:

```markdown
> [!nota] Migrado para galho próprio
> Conceito X foi expandido em [[Nome do galho]]. Veja em particular [[01 - ...]], [[02 - ...]].
```

4. **Higienizar fabricação** ao podar (seções "da minha experiência")
5. **Atualizar** o "Veja também" do tronco linkando o MOC do galho + `updated:` no frontmatter
6. **Não apagar** histórico Git — mudança via commit, sempre reversível

Troncos como `Java Fundamentals` alimentam **múltiplos galhos** (1, 2, 3, 4) — cada galho poda só a parte que migrou; o tronco só vira candidato a MOC enxuto/deprecação quando todos os galhos que o consomem fecharem. A decisão sobre o destino final de cada tronco emerge **depois** — não antecipar.

## 10. Critérios de "galho fechado"

Um galho está fechado quando:

1. Todas as notas existem em `03-Dominios/Tecnologia/Java/<Nome do Galho>/` com frontmatter completo (incluindo `fase:`) e `publish: true`
2. MOC do galho tem todas as notas linkadas em 3 subseções de fase + 4-5 rotas alternativas + dataview
3. Cada nota satisfaz a rubrica:
   - TL;DR compreensível em <30s
   - 2+ wikilinks pra outras notas + 1+ wikilink pro tronco/fundamento + verbetes do Dicionário
   - 3-5 code samples quando aplicável
   - "Em entrevista": frase pronta em inglês com 3+ sentenças (trade-off + decisão + caveat) + 6+ termos PT→EN
   - "Armadilhas": 2+ concretas, cada uma com descrição + exemplo curto + fix
   - Frontmatter completo; versões declaradas se relevante
   - PT-BR natural; termos técnicos em inglês
   - **Zero atribuição de experiência pessoal ao autor**
   - Nenhuma alegação técnica não-trivial sem fonte ou code sample
4. Dicionário de Java atualizado com os verbetes do galho
5. Tronco(s) podado(s): seções migradas substituídas por callouts + wikilinks + fabricação higienizada
6. MOC central `Java/index.md` atualizado linkando o novo galho
7. Quartz publica sem erros

## 11. Riscos e mitigações

| Risco | Mitigação |
|---|---|
| 18 galhos é muito e a trilha nunca "fecha" | Trilha é incremental por design; cada galho fecha e entrega valor sozinho. Não há obrigação de fechar todos. Ordem por necessidade real. |
| Tronco `Java Fundamentals` alimenta 4 galhos e poda parcial deixa retalho | Poda incremental por galho; tronco só vira candidato a MOC enxuto quando galhos 1-4 fecharem. Aceitar tronco "em transição" no meio. |
| Sobreposição entre galhos (ex: transações em Persistência e em Jakarta EE; virtual threads em Concorrência e Reativa) | Cada galho tem dono claro do conceito; outros linkam, não re-explicam. Definir dono no spec do galho. |
| Fabricação herdada dos troncos ("da minha experiência") vazar pras notas | Poda obrigatoriamente higieniza; rubrica de aceitação exige zero atribuição pessoal. |
| Esquema de 3 fases inflar nº de notas por galho | Distribuição de referência (35/37/28) + nº de notas fixado no spec de cada galho; se inflar, dividir nota (não galho). |
| Topologia flat quebrar wikilinks existentes pra `Core/`, `Backend/`, `Frontend/` | Auditar wikilinks ao migrar cada tronco (skill `verificar-wikilinks`); manter aliases. |
| Kafka existente (~20 notas) não casar com 3-fases | Galho 14 decide reaproveitar como está vs refatorar — não antecipar; documentar a decisão no spec do galho 14. |
| Versões envelhecerem (preview features, GraalVM, Loom) | Versões hedged; revisar `updated` periodicamente; declarar version-specificity no corpo. |

## 12. Próximos passos

1. **Aprovação deste roadmap** + spec do Galho 1 (`2026-06-02-java-galho-01-linguagem-design.md`)
2. **Plano de execução do Galho 1** via skill `superpowers:writing-plans`
3. **Execução do Galho 1** via `superpowers:subagent-driven-development` ou `superpowers:executing-plans`
4. **Poda parcial** de `Java Fundamentals` correspondente ao Galho 1 + criação do Dicionário de Java + reescrita do MOC central
5. **Revisão do roadmap** com aprendizados do Galho 1 antes de iniciar o próximo

## 13. Documentos relacionados

- `2026-06-02-java-galho-01-linguagem-design.md` — spec detalhado do Galho 1
- Plano de execução (criado depois): `docs/superpowers/plans/2026-06-02-java-galho-01-linguagem-execution.md`
- Troncos a podar: `03-Dominios/Tecnologia/Java/Core/*.md`, `03-Dominios/Tecnologia/Java/Backend/*.md`, `03-Dominios/Tecnologia/Java/Frontend/JavaFX.md`
- MOC central: `03-Dominios/Tecnologia/Java/index.md`
- Specs de referência (formato análogo): `2026-05-07-node-roadmap-design.md` (tronco/galhos), `2026-05-18-trilha-terminal-design.md` (3 fases)
- Memórias: [[project_tronco_galhos_pattern]], [[project_trilhas_fases_aprendizado]], [[feedback_no_fabrication]]
