---
title: "Spec — Galho 10 da trilha Java Senior (Persistência de dados)"
date: 2026-06-09
author: Josenaldo
status: draft
type: spec
publish: false
---

# Spec — Galho 10 da trilha Java Senior (Persistência de dados)

## 1. Contexto e motivação

Este é o **décimo galho** da trilha Java Senior (roadmap em `docs/superpowers/specs/2026-06-02-java-senior-roadmap-design.md`, §5, bloco "Fundamentos enterprise e Spring", linha 143). Pressupõe leitura do roadmap, que estabelece topologia flat, esquema de 3 fases, padrões editoriais e política de poda. Os Galhos 1 (Linguagem), 2 (Collections/Streams), 3 (JVM), 4 (Concorrência), 5 (Swing), 6 (JavaFX), **7 (Jakarta EE)**, **8 (Spring Core e Boot)** e **9 (Web e APIs REST)** já fecharam em `main` — seus artefatos são o **template de padrão e qualidade** deste galho. As dependências diretas são os **Galhos 7 e 8** (linha 145 do roadmap): o Galho 7 é dono das **specs** que este galho operacionaliza (JPA, EntityManager, JTA); o Galho 8 é dono do **mecanismo** (o container, o proxy AOP que faz o `@Transactional` funcionar).

**Galho HÍBRIDO: REFATOR (poda em DOIS troncos) + PESQUISA.** Como os Galhos 8 e 9, tem dupla natureza, mas com a particularidade de podar **dois** troncos:

- **Parte REFATOR (poda integral + poda cirúrgica):**
  - `Backend/Spring Data JPA.md` (1313 linhas, `publish: false`, `status: evergreen`) é o **tronco dedicado deste galho**. Cobre **todo** o escopo (entidades, relacionamentos, fetch/N+1, repositories, queries, projections, transações, locking, caching, batch, Flyway, quando-não-usar-JPA), de forma densa e monolítica. **Poda INTEGRAL** (padrão JavaFX/Galho 6): o tronco encolhe a um hub de ~20 linhas — frontmatter (`publish: false`), H1, 1-2 frases de intro e um único callout `[!nota] Migrado para galho próprio` com wikilinks pro MOC do galho + notas representativas. **Toda a fabricação evapora** com a poda (o tronco tem `Patient`/`Doctor`/`Appointment`, a seção `## Na prática (da minha experiência)` com incidente fabricado do "MedEspecialista", e `## How to explain in English` em 1ª pessoa — **contraexemplo, jamais copiar pras notas**).
  - `Backend/Spring Boot.md` seção `## Gerenciamento de transações — @Transactional deep dive` (linhas ~67-219) — **deixada intacta de propósito** pelos Galhos 8/9, esperando este galho. Cobre O básico, Propagation, Isolation levels, Rollback rules, Read-only, Timeout e o padrão arquitetural (transações na camada Service). **Poda cirúrgica** → callout `[!nota] Migrado para galho próprio` + wikilinks pras notas de transação (12). Tem uma contaminação pontual (`Patient` na linha ~175; o resto é `Account`/`Order` neutro) que **some com a poda**.

- **Parte PESQUISA:** mesmo o tronco dedicado sendo rico, várias afirmações são **version-specific** e exigem confirmação via WebFetch (versão atual de Hibernate ORM e Spring Data JPA; `@GeneratedValue` strategies, incl. UUID na JPA 3.1; semântica de `@Transactional(readOnly)`; Flyway vs Liquibase atuais). E o **comparativo Flyway vs Liquibase** e os **detalhes de Criteria API** são tratados de forma rasa no tronco — nascem/se completam de doc oficial (`docs.spring.io/spring-data/jpa/`, `hibernate.org/orm/documentation`, `documentation.red-gate.com/fd` (Flyway), `docs.liquibase.com`).

**A fronteira-assinatura é TRIPLA.** Os Galhos 7, 8 e 9 plantaram ganchos esperando exatamente as notas deste galho. Este galho **linka de volta aos três**, sem re-explicar nenhum:

- **Galho 7 (as specs que este galho operacionaliza):** a **spec JPA** (`@Entity`, `@Id`, contrato de mapeamento) → [[03-Dominios/Tecnologia/Java/Jakarta EE/09 - JPA — a especificação de persistência|JPA]]; o **EntityManager / persistence context / ciclo de vida da entidade** (o conceito) → [[03-Dominios/Tecnologia/Java/Jakarta EE/10 - EntityManager e o ciclo de vida da entidade|EntityManager e o ciclo de vida da entidade]]; a **JTA / demarcação transacional** (o contrato) → [[03-Dominios/Tecnologia/Java/Jakarta EE/11 - JTA — transações na plataforma|JTA]]. Spring Data e Hibernate são a **implementação/abstração operacional** da spec — a spec não se re-explica.
- **Galho 8 (o mecanismo que faz o `@Transactional` funcionar):** o **proxy AOP** que intercepta o método anotado → [[03-Dominios/Tecnologia/Java/Spring Core e Boot/09 - AOP e proxies no Spring|AOP e proxies]]; os **limites do proxy** (self-invocation, método `private`/`final`) → [[03-Dominios/Tecnologia/Java/Spring Core e Boot/10 - Self-invocation e os limites do proxy|Self-invocation e os limites do proxy]]. Este galho cobre o **comportamento** transacional (propagação, isolamento, rollback, readOnly), **não o mecanismo** (que é o AOP do Galho 8).
- **Galho 9 (a borda que consome a persistência):** **DTO vs entidade**, não vazar a entidade JPA no JSON → [[03-Dominios/Tecnologia/Java/Web e APIs REST/05 - Serialização JSON com Jackson|Serialização JSON com Jackson]]; validação de **negócio** (service) vs validação de **formato** (borda) → [[03-Dominios/Tecnologia/Java/Web e APIs REST/08 - Validação na borda|Validação na borda]]. A entidade vive aqui; a borda recebe DTO.

Os Galhos 7, 8 e 9 deixaram **ganchos "Galho 10 (planejado)"** em texto esperando exatamente esses wikilinks (dívida reversa — §3.6). Este galho **quita** essa dívida.

Persistência de dados é a **camada de dados sobre a spec JPA do Galho 7**: como uma classe vira `@Entity` e atravessa estados (transient → managed → detached), como o persistence context é um cache de 1º nível com dirty checking, como se mapeiam relacionamentos sem cair no N+1, como o Spring Data elimina o boilerplate do repositório, como se consulta (derived/JPQL/native/Specifications), pagina e transaciona (`@Transactional` operacional), e como se evolui o schema com disciplina (Flyway/Liquibase). Depende dos Galhos 7 (specs) e 8 (mecanismo).

## 2. Objetivo

Produzir, em uma sessão de execução dedicada, **17 notas atômicas + 1 MOC do galho + expansão do Dicionário de Java + ativação do MOC central + poda de DOIS troncos (integral do `Spring Data JPA.md` + cirúrgica da seção de transações do `Spring Boot.md`) + quitação da dívida reversa**, em `03-Dominios/Tecnologia/Java/Persistência de dados/` e `03-Dominios/Tecnologia/Java/`, todas `publish: true`, em PT-BR, distribuídas em 3 fases (**5 Iniciado + 6 Adepto + 6 Magus**).

Ao terminar o galho, o leitor deve conseguir:

- **Explicar em inglês** a pilha de persistência (Spring Data → spec JPA → Hibernate → JDBC), o ciclo de vida da entidade, o que é o persistence context e o dirty checking, e por que o N+1 é o bug mais caro da JPA.
- **Reconhecer o que este galho operacionaliza do Galho 7**: dada a `@Entity`/o `EntityManager`/a demarcação transacional, apontar a spec Jakarta correspondente (JPA, EntityManager, JTA) e a diferença entre o **contrato** (spec) e a **operação** (Hibernate/Spring Data).
- **Reconhecer o que o `@Transactional` deve ao mecanismo do Galho 8**: o comportamento (propagação/isolamento/rollback) roda sobre o proxy AOP, e os limites do proxy (self-invocation, `private`/`final`) explicam por que ele às vezes "não funciona".
- **Projetar uma camada de persistência production-grade**: entidades com `equals/hashCode` corretos, relações sempre LAZY, fetch explícito (`@EntityGraph`/`JOIN FETCH`/projection), transações na camada Service com `readOnly` default, locking otimista onde há concorrência, e migrations com expand-and-contract.
- **Diagnosticar armadilhas clássicas**: N+1 silencioso, `@ManyToOne` EAGER, `LazyInitializationException`, OSIV escondendo bugs, `@Transactional` em self-invocation, checked exception que não faz rollback, `IDENTITY` matando o batch, `JOIN FETCH` + paginação carregando tudo em memória.

A barra é "explicar a pilha, reconhecer as specs e o mecanismo por baixo, e projetar a camada de dados com critério" — não "escrever um `Dialect` customizado do Hibernate".

## 3. Saídas concretas

### 3.1. Notas (`03-Dominios/Tecnologia/Java/Persistência de dados/`)

Pasta **nova**, flat. 17 notas + 1 MOC (`index.md`, obrigatório pro folder-link do Quartz). Numeração global por galho (não reinicia por fase).

#### Iniciado (5 notas — vocabulário + modelo mental)

| # | Nota | Escopo nuclear |
|---|------|----------------|
| 01 | O que é a camada de persistência — Spring Data, JPA e Hibernate *(opus)* | A pilha: seu código → Spring Data JPA (elimina boilerplate) → **spec JPA** (Galho 7) → **Hibernate** (a implementação) → JDBC → banco. O que cada camada faz e por que existe. **A nota-assinatura da TRIPLA fronteira:** operacionaliza a spec JPA do Galho 7, o `@Transactional` usa o mecanismo AOP do Galho 8, devolve DTO (não entidade) pra borda do Galho 9. Linka G7 nota 09 (spec), G8 nota 09 (AOP), G9 nota 05 (DTO). |
| 02 | A entidade JPA — @Entity, @Id e geração de chave | `@Entity`/`@Table`/`@Column`/`@Id`/`@GeneratedValue` (estratégias IDENTITY/SEQUENCE/TABLE/AUTO/UUID — **UUID na JPA 3.1**, WebFetch); construtor sem-arg obrigatório; por que **record não serve** como entidade; `equals`/`hashCode` por business key (nunca `@Data` do Lombok). Linka **G7 nota 09** (a spec define essas anotações; aqui é o uso operacional). |
| 03 | O persistence context e os estados da entidade | Os 4 estados (transient/managed/detached/removed) e as transições (persist/merge/remove/detach); o persistence context como **cache de 1º nível** (mesma query 2x = 1 SQL); **dirty checking** (não precisa de `save()`); `save` do Spring Data = persist (id null) ou merge (id existe); flush. Linka **G7 nota 10** (EntityManager/persistence context — o conceito; aqui o ângulo operacional Hibernate/Spring Data). Quita dívida Jakarta 10:160/331. |
| 04 | Spring Data repositories — JpaRepository e query methods derivados | A hierarquia (`Repository` → `CrudRepository` → `PagingAndSortingRepository` → `JpaRepository`); CRUD herdado; **derived queries** (`findByEmail`, keywords `And`/`Or`/`Between`/`GreaterThan`/`OrderBy`/...); quando a derived query fica ilegível e cede pro `@Query`. Linka **G8** (o repositório é um bean/proxy gerado — o mecanismo é AOP). |
| 05 | Relacionamentos — @ManyToOne, @OneToMany e o owning side | A relação mais comum; **owning side** (`@ManyToOne` tem a FK) vs **inverse side** (`mappedBy`); `@JoinColumn`; bidirecional + **helper methods** pra sincronizar os dois lados; a tabela de **defaults de fetch** (`@ManyToOne` EAGER — armadilha). Prepara a nota 07. |

#### Adepto (6 notas — domínio operacional)

| # | Nota | Escopo nuclear |
|---|------|----------------|
| 06 | @ManyToMany, @OneToOne, cascade e orphanRemoval | O resto do mapeamento: `@ManyToMany` (e por que preferir entidade associativa explícita); `@OneToOne` (e o problema do lazy sem `@MapsId`); `cascade` (PERSIST/MERGE/REMOVE/ALL) e `orphanRemoval` — a diferença e os perigos (`cascade = ALL` deletando filhos sem querer). |
| 07 | Fetch strategies — LAZY, EAGER e a LazyInitializationException | A decisão central da JPA; LAZY vs EAGER (proxy/coleção lazy); **regra prática: sempre LAZY**; a `LazyInitializationException` (acesso lazy fora da transação) e as soluções de borda; **Open Session In View** (Boot habilita por default — desabilite). Linka **G9 nota 05** (a entidade vaza no JSON → DTO). |
| 08 | O problema N+1 e suas soluções — @EntityGraph, JOIN FETCH, batch size *(opus)* | **O bug mais caro da JPA.** O que é (1 query pai + N filhos); como **detectar** (SQL logging, `generate_statistics`, contador de queries no teste); as soluções: **`@EntityGraph`** (declarativo, preferido), **`JOIN FETCH`** (JPQL, uma coleção por query — o cartesian product), **`@BatchSize`**, **DTO projection**; o cuidado **`JOIN FETCH` + paginação** (HHH000104, carrega tudo em memória). |
| 09 | Consultas com @Query — JPQL, native e @Modifying | **JPQL** (entidades/atributos, não tabelas/colunas) vs **SQL nativo** (`nativeQuery = true`); `@Param`; **`@Modifying`** pra UPDATE/DELETE em massa (e o `clearAutomatically`/`flushAutomatically`); bulk vs carregar-e-modificar. |
| 10 | Projections e DTOs — não vazar a entidade | **Interface projection** (proxy do Spring), **class-based/DTO projection** (`record` via `SELECT new ...`), **dynamic projection** (`<T> findBy...(Class<T>)`); quando usar projection (listagem read-only) vs entidade (modificar). **Não vazar a entidade na borda** — linka **G9 nota 05** (o DTO é o contrato da API). |
| 11 | Paginação e ordenação — Pageable, Page e Slice | `Pageable`/`PageRequest`; **`Page`** (traz o `count` total — query extra) vs **`Slice`** (só sabe se há próxima — sem count); `Sort`; o custo do count em tabelas grandes; cursor-based como menção de fronteira (API design). |

#### Magus (6 notas — maestria + arquitetura)

| # | Nota | Escopo nuclear |
|---|------|----------------|
| 12 | Transações operacionais — @Transactional: propagação, isolamento, rollback, readOnly *(opus)* | O **comportamento** (não o mecanismo): **propagação** (REQUIRED/REQUIRES_NEW/NESTED/...), **isolamento** (READ_COMMITTED/REPEATABLE_READ/SERIALIZABLE — liga a [[Banco de dados]]), **rollback rules** (só `RuntimeException`/`Error` por default — checked não faz rollback; `rollbackFor`), **readOnly** (desabilita dirty checking), timeout, transação na **camada Service**. **O mecanismo é o proxy AOP** → linka **G8 notas 09/10** (AOP + self-invocation); a demarcação é a **JTA** → linka **G7 nota 11**. Quita dívida Spring Boot:63 e JTA:35. |
| 13 | Locking — optimistic (@Version) e pessimistic | **Lost update** e como evitar; **optimistic** (`@Version`, `OptimisticLockException`, retry) vs **pessimistic** (`@Lock(PESSIMISTIC_WRITE)`, `SELECT ... FOR UPDATE`, deadlocks e ordem de aquisição); quando cada um. Liga a [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Concorrência]] (conflito de escrita). |
| 14 | Caching — 1º nível, 2º nível e Spring Cache *(opus)* | **L1** (persistence context — já visto na 03, recapitula a fronteira); **L2** (cache application-wide, `@Cacheable`/`@Cache`, estratégias READ_ONLY/READ_WRITE/..., quando usar — entidades de referência; quando NÃO — dados dinâmicos, multi-nó sem cache distribuído); **Spring Cache** (`@Cacheable`/`@CacheEvict`/`@CachePut` na camada Service — a camada acima da JPA). Distingue os três níveis. |
| 15 | Consultas dinâmicas e os limites da JPA — Specifications, Criteria e quando descer pro SQL | **Specifications** (`JpaSpecificationExecutor`, filtros dinâmicos componíveis — comum em APIs de busca) sobre a **Criteria API** (a query programática type-safe da spec JPA — Galho 7); **quando a JPA não basta** (queries analíticas, window functions, bulk, reporting) e o **escape hatch**: `JdbcClient`/`JdbcTemplate`, **jOOQ** (type-safe). Sem dogma — JPA pro domínio transacional, SQL pro analítico. |
| 16 | Migrations de schema — Flyway, Liquibase e expand-and-contract | Por que versionar schema (não confiar no `ddl-auto`); **Flyway** (SQL versionado, `V__`/`R__`) vs **Liquibase** (changelog XML/YAML/SQL, rollback declarativo) — **WebFetch** pra versões/diferenças atuais; regras de ouro (nunca editar migration aplicada, roll-forward); **expand-and-contract** pra mudança em tabela grande sem downtime; índice `CONCURRENTLY`. |
| 17 | Capstone — Uma query do repositório ao banco, sem cair no N+1 *(opus, híbrido trace + checklist)* | **Trace:** `repo.findAll(spec, pageable)` → proxy Spring Data → tradução pra JPQL/Criteria → Hibernate monta o SQL → persistence context (cache/identidade) → JDBC → `ResultSet` → entidades managed → projeção/DTO pra borda; e o caminho transacional (proxy AOP abre tx → dirty checking no commit). **Checklist de design production-grade:** sempre LAZY, fetch explícito (sem N+1), DTO não-entidade na borda, `readOnly` default no Service, `@Version` onde há concorrência, migration com expand-and-contract. **Tabela "Galho 10 → spec Jakarta (Galho 7)"** (`@Entity`↔JPA, persistence context↔EntityManager, `@Transactional`↔JTA + proxy AOP do Galho 8). Cheatsheet nota→problema. Munição de entrevista. **WebFetch.** |

**Notas opus (5):** 01 (assinatura/tripla fronteira), 08 (N+1 — a mais densa), 12 (transações — comportamento + tripla referência), 14 (caching — os três níveis), 17 (capstone síntese). As demais → sonnet. Notas com afirmação version-specific (02, 16, 17 e qualquer outra que cravar versão) fazem WebFetch no Step 1 independentemente do modelo.

**Decisões de fronteira (escopo de outro dono — texto "(planejado)", sem wikilink):**
- **Spec JPA / EntityManager / persistence context (o conceito) / JTA** → Galho 7 (COMPLETO). **Linkar de volta, nunca re-explicar a spec.** Primeira face da fronteira-assinatura.
- **Container / IoC / AOP / o proxy que faz o `@Transactional` / self-invocation** → Galho 8 (COMPLETO). **Linkar de volta** (comportamento ≠ mecanismo). Segunda face.
- **DTO vs entidade / serialização da entidade no controller / validação de negócio vs borda** → Galho 9 (COMPLETO). **Linkar de volta.** Terceira face.
- **R2DBC / persistência reativa / `Mono`/`Flux` sobre o banco** → Galho 11 (planejado). A persistência aqui é **bloqueante/imperativa**.
- **Segurança a nível de dados / row-level security / criptografia de campo / auditoria com Spring Security** → Galho 12 (planejado). Auditoria aqui só como `@CreatedDate`/`@LastModifiedDate` (mecânica JPA), sem o `AuditorAware` que puxa o `SecurityContext`.
- **`@DataJpaTest` / Testcontainers / `TestEntityManager` / slices de teste de repositório** → Galho 13 (planejado). As notas **citam** que se testa com banco real, sem ensinar a stack de teste.
- **Dados distribuídos / sharding / saga / event sourcing / CQRS / outbox** → Galho 16 (planejado).
- **Banco de dados (SQL, ACID, índices, isolamento — teoria)** → nota existente [[Banco de dados]] (linkar pra teoria de isolamento na nota 12). **Concorrência de baixo nível** → Galho 4 (linkar na nota 13). **Annotations (mecânica)** → Galho 1 nota 11 (linkar quando tocar em `@Entity` como anotação).

### 3.2. MOC do galho

`03-Dominios/Tecnologia/Java/Persistência de dados/index.md`:
- `type: moc`, `status: growing`
- Frontmatter padrão (`title: "Persistência de dados"`, tags `java`/`persistencia`/`moc`, aliases `["Persistência de dados", "JPA", "Hibernate", "Spring Data JPA", "Galho 10 - Persistência"]`)
- TL;DR callout (galho cobre a camada de dados sobre a spec JPA do Galho 7: entidades e o persistence context, mapeamento de relacionamentos, fetch strategies e o N+1, Spring Data repositories e consultas, paginação, transações operacionais, locking, caching e migrations)
- "Sobre este galho" + audiência primária/secundária + nota de que é galho híbrido (poda integral do tronco `Spring Data JPA.md` + poda cirúrgica da seção de transações do `Spring Boot.md` + pesquisa pras partes version-specific) e de **tripla fronteira** (operacionaliza specs do Galho 7, usa o mecanismo AOP do Galho 8, alimenta a borda do Galho 9)
- Conteúdo agrupado em 3 H2 (`## Iniciado` / `## Adepto` / `## Magus`) com wikilinks pras 17 notas (uma linha descritiva cada)
- **Rotas alternativas (5):**
  - **Completa** — 01 → 17 em ordem
  - **Entrevista internacional** — 01 → 03 → 05 → 07 → 08 → 12 → 17 (pilha, persistence context, relacionamentos, fetch, N+1, transações, capstone — o que mais cai)
  - **Caçando o N+1** — 05 → 07 → 08 → 10 → 17 (relacionamentos, fetch, N+1, projections, capstone)
  - **Projetando a camada de persistência** — 02 → 05 → 07 → 10 → 11 → 12 → 16 (entidade, relação, fetch, DTO, paginação, transação, migration)
  - **Persistência sobre Jakarta EE** (a ponte com o Galho 7) — 01 → 03 → 12 + notas do Galho 7 (JPA, EntityManager, JTA)
- "Veja também": MOC central `[[03-Dominios/Tecnologia/Java/index|Trilha Java]]`, **Galho 7** (Jakarta EE — as specs que este galho operacionaliza), **Galho 8** (Spring Core e Boot — o mecanismo AOP do `@Transactional`), **Galho 9** (Web e APIs REST — a borda que consome a persistência), nota existente [[Banco de dados]] (teoria SQL/ACID), Dicionário de Java; Galhos 11/12/13/16 como texto "(planejado)" sem wikilink
- Dataview "Todas as notas do galho"

### 3.3. Dicionário de Java (EXPANSÃO — não recriar)

`03-Dominios/Tecnologia/Java/Dicionário de Java.md` já existe (**272 verbetes** após o Galho 9, `type: glossary`, `updated: 2026-06-08`, seções alfabéticas únicas `## A`…`## Z` com verbetes `### `). Este galho **expande** o arquivo existente inserindo os verbetes **em ordem alfabética case-insensitive (sem acento)** nas seções de letra apropriadas. **Nunca recriar o arquivo nem reordenar verbetes existentes.** Atualizar `updated` no frontmatter para `2026-06-09`.

Verbetes a inserir (~30, conferir dups antes):

`@BatchSize`, `@Cacheable / Spring Cache`, `@EntityGraph`, `@GeneratedValue`, `@ManyToMany`, `@ManyToOne / @OneToMany`, `@Modifying`, `@OneToOne`, `@Query (JPQL/native)`, `@Transactional (propagação)`, `@Version (optimistic locking)`, `cascade / orphanRemoval`, `Criteria API`, `derived query method`, `dirty checking`, `expand-and-contract`, `fetch strategy (LAZY/EAGER)`, `Flyway`, `Hibernate`, `isolamento (isolation level)`, `JpaRepository`, `LazyInitializationException`, `Liquibase`, `N+1 (problema)`, `Open Session In View (OSIV)`, `owning side / inverse side`, `Pageable / Page / Slice`, `pessimistic locking`, `persistence context (1º nível)`, `projection (JPA)`, `propagação de transação`, `readOnly (transação)`, `rollback rules`, `Specification (Spring Data)`, `Spring Data JPA`, `second-level cache (2º nível)`.

Cada verbete: definição curta (1-3 linhas) em PT-BR + `Veja também:` apontando pra(s) nota(s) canônica(s) do galho. **Conferir com grep os verbetes já existentes** (vindos dos Galhos 7/8: `JPA`, `EntityManager`, `persistence context` (conceito), `entidade`, `JPQL`, `owning side`, `@Transactional` (Jakarta e/ou Spring), `JTA`, `mappedBy`, `dirty checking` se já houver) para **não duplicar** — quando um termo operacional tocar um já existente, **linkar entre si** em vez de criar segundo verbete (ex.: `persistence context (1º nível)` operacional ↔ `persistence context` conceitual do Galho 7; `@Transactional (propagação)` ↔ `@Transactional` do Galho 8). **Conferir 1:1** que os headings dos verbetes batem EXATAMENTE com as âncoras `[[Dicionário de Java#...]]` usadas nas notas (extrair as âncoras das notas via grep e conferir, como nos Galhos 4-9).

### 3.4. MOC central (ativação do Galho 10)

`03-Dominios/Tecnologia/Java/index.md` já existe. Task **mínima**: trocar a linha 40 (atualmente `10. Persistência de dados *(planejado)* — JPA/Hibernate, Spring Data, fetch/N+1, transações, migrations`) por wikilink ativo no padrão dos galhos fechados:

```markdown
10. [[03-Dominios/Tecnologia/Java/Persistência de dados/index|Persistência de dados]] — JPA/Hibernate, o persistence context, mapeamento e relacionamentos, fetch strategies e o N+1, Spring Data repositories e consultas, paginação, transações operacionais, locking, caching e migrations
```

Atualizar `updated` para `2026-06-09`. Não mexer no resto do MOC central.

### 3.5. Poda dos DOIS troncos

#### 3.5.1. Poda INTEGRAL — `Backend/Spring Data JPA.md`

O tronco dedicado deste galho (1313 linhas, `publish: false`). **Poda integral** (padrão JavaFX/Galho 6): substituir **todo o corpo** (da linha após o frontmatter até o fim) por:
- frontmatter preservado, com `publish: false` (mantém — é tronco de trabalho) e `updated: 2026-06-09`;
- H1 `# Spring Data JPA`;
- 1-2 frases de intro neutras (sem fabricação);
- um único callout `[!nota] Migrado para galho próprio` com wikilink pro MOC do galho + ~5-6 notas representativas (01, 03, 05, 08, 12, 16), formato herdado do JavaFX:

```markdown
> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Tecnologia/Java/Persistência de dados/index|Persistência de dados]]. Veja [[03-Dominios/Tecnologia/Java/Persistência de dados/01 - O que é a camada de persistência — Spring Data, JPA e Hibernate|O que é a camada de persistência]], [[03-Dominios/Tecnologia/Java/Persistência de dados/08 - O problema N+1 e suas soluções — @EntityGraph, JOIN FETCH, batch size|O problema N+1]], [[03-Dominios/Tecnologia/Java/Persistência de dados/12 - Transações operacionais — @Transactional: propagação, isolamento, rollback, readOnly|Transações operacionais]], [[03-Dominios/Tecnologia/Java/Persistência de dados/16 - Migrations de schema — Flyway, Liquibase e expand-and-contract|Migrations de schema]].
```

**Toda a fabricação some** (`Patient`/`Doctor`/`Appointment`, `## Na prática (da minha experiência)`, `## How to explain in English`, o "incidente memorável" do MedEspecialista). O nome de arquivo `Spring Data JPA.md` permanece (o wikilink `[[Spring Data JPA]]` de `Spring Boot.md:385` `### Persistência` continua resolvendo — vira ponteiro encadeado pro hub).

#### 3.5.2. Poda CIRÚRGICA — `Backend/Spring Boot.md` (seção de transações)

**Poda mínima — uma única seção.** Substituir `## Gerenciamento de transações — @Transactional deep dive` (linhas ~67-219: O básico, Propagation, Isolation levels, Rollback rules, Read-only, Timeout, Padrão arquitetural Service) por callout `[!nota] Migrado para galho próprio` + wikilinks pras notas de transação:

```markdown
## Gerenciamento de transações — @Transactional deep dive

> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Tecnologia/Java/Persistência de dados/index|Persistência de dados]]. Veja [[03-Dominios/Tecnologia/Java/Persistência de dados/12 - Transações operacionais — @Transactional: propagação, isolamento, rollback, readOnly|Transações operacionais (@Transactional)]] e [[03-Dominios/Tecnologia/Java/Persistência de dados/13 - Locking — optimistic (@Version) e pessimistic|Locking]]. O mecanismo (proxy AOP, self-invocation) é do galho [[03-Dominios/Tecnologia/Java/Spring Core e Boot/index|Spring Core e Boot]].
```

A contaminação `Patient` (linha ~175) **some com a poda**. Confirmar os números de linha na execução (lendo o tronco primeiro — política §9 do roadmap; podem ter deslocado).

**NÃO TOCAR no `Spring Boot.md` (seções de outros galhos):**
- `## O que é` / `## Spring IoC Container` / `## AOP e proxies` / `## Configuração e Profiles` / `## Actuator` → **já podadas pelo Galho 8** (callouts; intactas).
- `## Spring MVC pipeline` → **já podada pelo Galho 9** (callout; intacta).
- `## Spring WebFlux — visão geral` → Galho 11.
- `## Spring Cloud — visão geral` (incl. `### OpenFeign`, `### Alternativa moderna`) → Galho 16.
- `## Camadas típicas de uma aplicação Spring Boot` (incl. `### Persistência` ~383 e `### Bean Validation` ~428): **deixar intactas.** O `### Persistência` é um "resumo rápido" que aponta pro deep-dive `[[Spring Data JPA]]` (que vira o hub do §3.5.1 — ponteiro encadeado válido). É um resumo da visão em camadas, não a seção core deste galho; fragmentá-la seria pior. (A fabricação `PatientRepository`/`Patient` ali permanece — não é a seção deste galho; os Galhos 8/9 também a deixaram.)
- `## Troubleshooting em produção` → galhos 10/16/17.
- `## Quando usar` / `## Armadilhas comuns` / `## How to explain in English` / `## Recursos` / `## Veja também` → gerais; atualizar só o "Veja também" pra linkar o MOC do galho.

**Atualizar `updated` nos dois troncos.** Não tocar em `Backend/Kafka/` (Galho 14) nem `Backend/Spring Security.md` (Galho 12). O `## Veja também` de cada tronco podado recebe wikilink pro MOC do Galho 10.

### 3.6. Dívida reversa (ganchos "Galho 10 / planejado")

Pré-flight localizou **11 ponteiros inline + 3 parágrafos de fronteira** a quitar após as notas existirem. Todos viram wikilinks pras notas do Galho 10; a persistência deixa de ser texto "(planejado)" **nesses pontos específicos**:

| # | Arquivo:linha | Texto atual (resumo) | Vira wikilink pra |
|---|---|---|---|
| 1 | `index.md:40` (MOC central) | `10. Persistência de dados *(planejado)*` | ativação (§3.4) |
| 2 | `Backend/Spring Boot.md:63` (callout AOP) | "...fica para o Galho 10, planejado, na seção de transações abaixo." | **nota 12** (a "seção de transações abaixo" deixa de existir — vira callout) |
| 3 | `Jakarta EE/09 - JPA:57` | "O Galho 10 (planejado) constrói em cima..." | **nota 01** (a pilha) ou MOC |
| 4 | `Jakarta EE/09 - JPA:152` | tabela "Tudo que vai além do default — Galho 10 (planejado)" | **nota 07** (fetch strategies) |
| 5 | `Jakarta EE/09 - JPA:333` | comentário HTML "além do contrato é assunto do Galho 10 (planejado)." | **nota 07** ou MOC |
| 6 | `Jakarta EE/10 - EntityManager:160` | "**Como** o provider detecta as mudanças ... território do Galho 10 (planejado)" | **nota 03** (persistence context/dirty checking operacional) |
| 7 | `Jakarta EE/10 - EntityManager:331` | "As estratégias concretas de carregamento ... Galho 10 (planejado)" | **nota 07** (fetch strategies) |
| 8 | `Jakarta EE/11 - JTA:35` | "O `@Transactional` do Spring é assunto dos Galhos 8/10 (planejado)" | **Galho 8** (AOP — já existe) + **nota 12** (transações operacionais) |
| 9 | `Web e APIs REST/05 - Serialização JSON:133` | "(Galho 10 da trilha Java — persistência com JPA/Hibernate, planejado)" | **nota 10** (projections/DTO) ou 01 |
| 10 | `Web e APIs REST/05 - Serialização JSON:378` | "Persistência JPA/Hibernate ... → Galho 10 (planejado)." (Veja também) | **nota 01** ou MOC |
| 11 | `Web e APIs REST/08 - Validação na borda:236` | "regras de negócio ... camada de serviço (Galho 10 — planejado)" | **nota 12** (transações/service) ou MOC |
| P1 | `Jakarta EE/index.md:30` (parágrafo fronteira) | "JPA operacional (Hibernate, fetch/N+1, caching, Spring Data, migrations) é do Galho 10 (planejado)" | trecho do Galho 10 → wikilink pro **MOC do galho** |
| P2 | `Spring Core e Boot/index.md:32` (parágrafo fronteira) | "Persistência/transações operacionais ... (Galho 10) são planejados" | trecho do Galho 10 → wikilink pro **MOC do galho** |
| P3 | `Web e APIs REST/index.md:32` (parágrafo fronteira) | "Persistência/Spring Data (Galho 10)" | trecho do Galho 10 → wikilink pro **MOC do galho** |

**Não tocar nos horizonte-lists de uma linha** (`Spring Core e Boot/index.md:97`, `Web e APIs REST/index.md:95`) — são listas-resumo de galhos futuros que o Galho 9 deixou intactas (padrão estabelecido); 11/12/13/16/17 permanecem "(planejado)" lá. Em todos os pontos, manter como texto "(planejado)" qualquer referência a galhos **ainda** inexistentes (11/12/13/16/17). Confirmar os números de linha na execução (podem ter deslocado) via grep `"Galho 10"`/`"planejado"`.

## 4. Convenções por nota

Herda §7 do roadmap e §4 dos specs dos Galhos 7/8/9. Reforços específicos:

### 4.1. Frontmatter

```yaml
---
title: "<título>"
created: 2026-06-09
updated: 2026-06-09
type: concept
status: seedling
publish: true
fase: iniciado | adepto | magus
tags:
  - java
  - persistencia
  - <fase>
  - <tags específicas: jpa, hibernate, entidade, relacionamentos, fetch, n-mais-1, spring-data, jpql, projection, paginacao, transacao, locking, cache, migrations, ...>
aliases:
  - <aliases opcionais>
---
```

H1 `# Título` após o frontmatter (padrão dos galhos publicados).

### 4.2. Estrutura H2 obrigatória

- `> [!abstract] TL;DR` (callout, NÃO H2) — 2-4 linhas: conceito + regra prática + por que importa
- `## O que é` / `## Por que importa` / `## Como funciona` (≥3 subseções H3 em notas Adepto/Magus)
- `## Na prática` — exemplos compiláveis; framing **neutro** (`Order`/`Customer`/`Product`/`OrderRepository`/`CustomerService`); "padrão observado em apps Spring Data"; NUNCA `Patient`/`MedEspecialista`/"no meu projeto" (os dois troncos estão cheios disso — **contraexemplo**)
- `## Armadilhas` — **≥2** (Iniciado) / **≥3** (Adepto/Magus), cada uma com descrição + exemplo curto de código demonstrando o problema + fix em 1 linha
- `## Em entrevista` — subheading `### Frase pronta (inglês)` com **3+ sentenças** (trade-off + decisão + caveat) + subheading `### Vocabulário` com tabela `| Termo PT | Termo EN |` de **6+ termos**
- `## Veja também` — wikilinks **SEM backticks**; sempre inclui notas relacionadas do galho + `[[03-Dominios/Tecnologia/Java/Persistência de dados/index|MOC do galho]]` + `[[03-Dominios/Tecnologia/Java/index|Trilha Java]]` + (quando operacionalizar spec) a nota do **Galho 7** correspondente + (quando usar o mecanismo do `@Transactional`) a nota do **Galho 8** + (quando tocar DTO/borda) a nota do **Galho 9** + verbetes do Dicionário. **Evitar âncoras same-file `[[#Heading]]`** (falso-positivo no checker).
- `## Referências` — docs oficiais (`docs.spring.io/spring-data/jpa/reference/`, `hibernate.org/orm/documentation`, `jakarta.ee/specifications/persistence/`, `documentation.red-gate.com/fd` (Flyway), `docs.liquibase.com`). Afirmações version-specific fundadas em fonte verificada via WebFetch.

### 4.3. Restrições absolutas

1. **Tripla fronteira-assinatura (linkar de volta aos Galhos 7, 8 e 9)** — todo conceito que operacionaliza uma spec aponta pra nota do **Galho 7** ("é a spec por baixo", sem re-explicar); o `@Transactional` aponta pra nota do **Galho 8** ("o mecanismo é o proxy AOP"); o que toca a borda (entidade vs DTO) aponta pra nota do **Galho 9**. Galhos 11-16 = texto "(planejado)", sem wikilink.
2. **Sem fabricação** de experiência pessoal. Exemplos neutros (`Order`, `Customer`, `Product`) — NUNCA `Patient`/`josenaldo`/`MedEspecialista`/1ª pessoa. **Os dois troncos são matéria-prima a higienizar, jamais a copiar** (o `Spring Data JPA.md` tem o "incidente memorável" do MedEspecialista e `## Na prática (da minha experiência)` — contraexemplo). **Zero estatística de adoção inventada** (regra dos Galhos 5-9).
3. **Sem invenção** de APIs/comportamentos. WebFetch obrigatório no Step 1 das notas version-specific (02 `@GeneratedValue`/UUID JPA 3.1, 16 Flyway/Liquibase, 17 capstone) e pra **toda afirmação version-specific**. Pontos minados verificados via WebFetch: **versão atual do Hibernate ORM** e do **Spring Data JPA**; **Jakarta Persistence 3.2** (já é EE 11 — cravado no Galho 7); **`@GeneratedValue` strategies** (IDENTITY/SEQUENCE/TABLE/AUTO/UUID — **UUID na JPA 3.1**); semântica de **`@Transactional(readOnly)`**; **Flyway vs Liquibase** atuais. Spring Boot 3.x / Spring Data JPA / Hibernate ORM 6.x como **baseline** (`jakarta.persistence.*`, Java 17), citando 4.x/7.x como "mais recente" quando relevante. Fonte: `docs.spring.io`, `hibernate.org`, `jakarta.ee`, `documentation.red-gate.com`, `docs.liquibase.com`. Nada "de memória".
4. **Code samples compiláveis** — Java moderno (records pra DTO/projection, `var`, switch); imports `jakarta.persistence.*` (Boot 3); `properties`/`yaml`/`sql`/`json` em fences corretas.
5. **Comparações justas** — LAZY vs EAGER, `@EntityGraph` vs `JOIN FETCH` vs projection, `Page` vs `Slice`, optimistic vs pessimistic, `@OneToMany` vs entidade associativa, Flyway vs Liquibase, JPA vs jOOQ/JdbcClient: sempre "quando X" E "quando Y". A capstone (17) é o ápice (checklist production-grade, sem dogma).
6. **Wikilinks sem backticks** em "Veja também"; MOC do galho + MOC central obrigatórios. **Não linkar galhos inexistentes** (11-16) — texto "(planejado)".
7. **Code fences corretos:** ` ```java ` pra código, ` ```sql ` pra DDL/migration, ` ```properties `/` ```yaml ` pra config, ` ```json ` pra payloads, ` ```text ` pra diagrama/output. Sempre fechadas.
8. **`fase:` no frontmatter + na tag** — obrigatório.
9. **Higiene de commits** — sem `Co-Authored-By: Claude`, sem `--no-verify`, `git add <path>` nominal (nunca `-A` — bot de backup Obsidian Git roda em timer), 1 commit por nota, controlador commita (subagents write-only). Guardar contra `.git/index.lock`.
10. **Tom pedagógico graduado** — Iniciado assume Galhos 1-2 + 7 (spec JPA/EntityManager básicos) + 8 (container/`@Transactional` básico); Magus assume o galho inteiro + Galhos 7-9.

## 5. Conteúdo por nota (síntese)

Esboço do recorte. Notas de **refator** partem do tronco `Spring Data JPA.md` (e da seção de transações do `Spring Boot.md`) refinado e higienizado; afirmações version-specific re-fundadas em doc oficial via WebFetch. Fontes-base: `docs.spring.io/spring-data/jpa/reference/`, `hibernate.org/orm/documentation/current/userguide/`, `jakarta.ee/specifications/persistence/`, `documentation.red-gate.com/fd`, `docs.liquibase.com`.

- **01 — O que é a camada de persistência (refator, opus).** A pilha em camadas (seu código → Spring Data JPA → spec JPA do Galho 7 → Hibernate → JDBC → banco) e o que cada uma resolve; JPA = spec (Galho 7), Hibernate = implementação, Spring Data = elimina boilerplate. A **tripla fronteira numa frase**: operacionaliza a spec do Galho 7, o `@Transactional` usa o mecanismo do Galho 8, devolve DTO pra borda do Galho 9. Armadilhas: dizer "JPA é o Hibernate" (spec ≠ impl — linka G7); achar que Spring Data "é" a JPA. Fontes: docs.spring.io/spring-data/jpa, hibernate.org.
- **02 — A entidade JPA (refator + research).** `@Entity`/`@Table`/`@Column`/`@Id`/`@GeneratedValue`; estratégias de ID (IDENTITY não permite batch; SEQUENCE com `allocationSize`; UUID na JPA 3.1 — **WebFetch**); construtor sem-arg; record não serve como entidade; `equals`/`hashCode` por business key, nunca `@Data`. Linka G7 nota 09 (a spec define as anotações). Armadilhas: `@Data` do Lombok em entidade (quebra equals/toString com lazy); `equals` por id gerado (null antes do save); `IDENTITY` em workload write-heavy. Fontes: jakarta.ee/persistence, hibernate.org (identifiers).
- **03 — O persistence context e os estados da entidade (refator).** Os 4 estados e transições; persistence context = cache de 1º nível (identidade: mesma query 2x = 1 SQL, `p1 == p2`); dirty checking (sem `save()`); `save` do Spring Data = persist|merge; flush (commit / antes de query / explícito). Linka **G7 nota 10** (EntityManager/persistence context — o conceito; aqui o operacional). Armadilhas: `save()` redundante em entidade managed; acessar lazy detached (prenúncio da 07); modificar e esperar persistir sem tx. Fontes: hibernate.org (persistence context), docs.spring.io.
- **04 — Spring Data repositories (refator).** Hierarquia `Repository`→`CrudRepository`→`PagingAndSortingRepository`→`JpaRepository`; CRUD herdado; derived queries (keywords); o limite (derived ilegível → `@Query`). Linka **G8** (o repositório é um proxy/bean gerado pelo Spring). Armadilhas: derived query gigante e ilegível; `findById` quando bastava `existsById`; assumir que todo método derivado é eficiente. Fontes: docs.spring.io/spring-data/jpa (query methods).
- **05 — Relacionamentos: @ManyToOne, @OneToMany, owning side (refator).** Owning (`@ManyToOne` tem a FK) vs inverse (`mappedBy`); `@JoinColumn`; bidirecional + helper methods; defaults de fetch (`@ManyToOne` EAGER — armadilha que a 07 ataca). Linka G7 nota 09 (a spec define os defaults). Armadilhas: esquecer `mappedBy` (duas FKs / join table inesperada); não sincronizar os dois lados (estado inconsistente); confiar no default EAGER do `@ManyToOne`. Fontes: jakarta.ee/persistence, hibernate.org (associations).
- **06 — @ManyToMany, @OneToOne, cascade e orphanRemoval (refator).** `@ManyToMany` + `@JoinTable` (e por que preferir entidade associativa quando há atributos na relação); `@OneToOne` (lazy problemático sem `@MapsId`); `cascade` (PERSIST/MERGE/REMOVE/ALL) e `orphanRemoval` (a diferença). Armadilhas: `@ManyToMany` escondendo entidade que merecia existir; `cascade = ALL` deletando filhos sem querer; `@OneToOne` EAGER dobrando JOINs. Fontes: hibernate.org (associations, cascading).
- **07 — Fetch strategies e LazyInitializationException (refator).** LAZY vs EAGER (proxy / coleção lazy); regra prática **sempre LAZY**; `LazyInitializationException` (acesso lazy fora da tx) e soluções de borda (DTO/`@EntityGraph`); **OSIV** (Boot habilita por default — `open-in-view: false` em produção, e por quê). Linka **G9 nota 05** (a entidade vaza no JSON → DTO) e prepara a 08. Armadilhas: `@ManyToOne` EAGER; OSIV escondendo N+1; `@Transactional` no controller só pra evitar a exceção (acopla camadas). Fontes: hibernate.org (fetching), docs.spring.io (open-in-view).
- **08 — O problema N+1 e suas soluções (refator, opus).** O que é (1 + N queries ao iterar coleção lazy); detecção (`show-sql`, `generate_statistics`, contador de query no teste); soluções: **`@EntityGraph`** (declarativo, preferido), **`JOIN FETCH`** (uma coleção/query — cartesian product com 2+), **`@BatchSize`**, **DTO projection**; o cuidado `JOIN FETCH` + paginação (HHH000104 — pagina em memória). Armadilhas: N+1 silencioso escondido por OSIV; `JOIN FETCH` de duas coleções (produto cartesiano); paginar com fetch de coleção. Fontes: hibernate.org (fetching, batch), vladmihalcea.com (conceito — sem estatística inventada).
- **09 — Consultas com @Query (refator).** JPQL (entidades/atributos) vs SQL nativo (`nativeQuery=true`); `@Param`; `@Modifying` pra UPDATE/DELETE em massa (`clearAutomatically`/`flushAutomatically` — invalida L1); JPQL não é SQL. Armadilhas: `@Modifying` sem limpar o L1 (entidade stale na sessão); misturar JPQL e SQL sem perceber (nomes de entidade vs tabela); `LIKE '%x%'` sem índice. Fontes: docs.spring.io/spring-data/jpa (@Query), jakarta.ee (JPQL).
- **10 — Projections e DTOs (refator).** Interface projection (proxy Spring), class-based/DTO (`record` via `SELECT new`), dynamic (`Class<T>`); quando projection (listagem read-only) vs entidade (modificar). **Não vazar a entidade na borda** — linka **G9 nota 05** (DTO é o contrato). Armadilhas: carregar entidade inteira só pra ler 3 campos; projection com relação lazy (N+1 sutil); expor entidade direto no JSON. Fontes: docs.spring.io/spring-data/jpa (projections).
- **11 — Paginação e ordenação (refator + research).** `Pageable`/`PageRequest`; `Page` (count total — query extra) vs `Slice` (só há-próxima — sem count); `Sort`; o custo do count em tabela grande; cursor-based como menção de fronteira (→ [[API Design]]). Armadilhas: `Page` desnecessário (paga o count sem usar); `Sort` por campo não indexado; offset alto em tabela grande (deep pagination). Fontes: docs.spring.io/spring-data/jpa (paging and sorting).
- **12 — Transações operacionais (refator, opus).** O **comportamento**: propagação (REQUIRED default, REQUIRES_NEW pra auditoria que commita independente, NESTED/savepoint, MANDATORY/NEVER), isolamento (READ_COMMITTED default PG / REPEATABLE_READ default MySQL / SERIALIZABLE — teoria em [[Banco de dados]]), rollback rules (só unchecked + Error por default; `rollbackFor`; `setRollbackOnly`), readOnly (desabilita dirty checking), timeout, transação na camada Service. **O mecanismo é o proxy AOP** → linka **G8 notas 09/10**; a demarcação é a **JTA** → linka **G7 nota 11**. Armadilhas: checked exception não faz rollback (default); self-invocation (chamada interna não passa pelo proxy — G8); `@Transactional` em método `private`. Fontes: docs.spring.io/spring-framework (transaction management), Spring Boot.md (refinar/higienizar).
- **13 — Locking: optimistic e pessimistic (refator).** Lost update; optimistic (`@Version`, `OptimisticLockException`, retry — para conflito raro) vs pessimistic (`@Lock(PESSIMISTIC_WRITE)`, `SELECT ... FOR UPDATE`, deadlock e ordem de aquisição — para conflito frequente). Liga a [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Concorrência]]. Armadilhas: esquecer `@Version` em entidade editável concorrentemente (lost update silencioso); deadlock por ordem de lock inconsistente; pessimistic onde optimistic bastava (contenção). Fontes: hibernate.org (locking), jakarta.ee (LockModeType).
- **14 — Caching: 1º, 2º nível e Spring Cache (refator + research, opus).** L1 (persistence context — recapitula a fronteira da 03), L2 (`@Cacheable`/`@Cache`, READ_ONLY/NONSTRICT/READ_WRITE/TRANSACTIONAL, quando usar — entidade de referência lida-muito/mudada-pouco; quando NÃO — dinâmico, multi-nó sem cache distribuído), Spring Cache (`@Cacheable`/`@CacheEvict`/`@CachePut` na Service — camada acima da JPA, Caffeine/Redis). Distingue os três. Armadilhas: confundir L1 (por-tx) com L2 (app-wide); L2 em dado volátil (stale); `@Cacheable` sem `@CacheEvict` (cache nunca invalida). Fontes: hibernate.org (caching), docs.spring.io (cache abstraction).
- **15 — Consultas dinâmicas e os limites da JPA (refator).** Specifications (`JpaSpecificationExecutor`, `Specification` componível pra filtros de busca) sobre a Criteria API (a query programática type-safe da spec JPA — Galho 7); quando a JPA não basta (analítico, window functions, bulk, reporting) e o escape hatch (`JdbcClient`/`JdbcTemplate`, jOOQ type-safe). Sem dogma. Armadilhas: forçar JPQL onde SQL/jOOQ era melhor; Specification ilegível (lógica demais no predicado); achar que JPA serve pra tudo. Fontes: docs.spring.io/spring-data/jpa (specifications), jakarta.ee (Criteria), jooq.org (menção).
- **16 — Migrations de schema (refator + research).** Por que versionar (não confiar no `ddl-auto=update` em produção); Flyway (`V__`/`R__`, SQL) vs Liquibase (changelog XML/YAML/SQL, rollback declarativo) — **WebFetch** pras versões/diferenças atuais; regras de ouro (nunca editar migration aplicada, roll-forward, baseline); **expand-and-contract** (add nullable → backfill → not null, deploy sequencial) pra tabela grande sem downtime; índice `CONCURRENTLY` (Postgres). Armadilhas: `ddl-auto=update` em produção; editar migration já aplicada; `ALTER TABLE ADD COLUMN NOT NULL` travando tabela grande. Fontes: documentation.red-gate.com/fd (Flyway), docs.liquibase.com.
- **17 — Capstone: uma query do repositório ao banco, sem cair no N+1 (refator + research, opus, híbrido).** **Trace:** `repo.findAll(spec, pageable)` → proxy Spring Data → Criteria/JPQL → Hibernate monta o SQL → persistence context (identidade/cache) → JDBC → `ResultSet` → entidades managed → projeção/DTO pra borda; e o caminho transacional (proxy AOP abre tx → dirty checking → commit). **Checklist de design production-grade:** sempre LAZY, fetch explícito (sem N+1), DTO não-entidade na borda, `readOnly` default no Service, `@Version` onde há concorrência, migration expand-and-contract, OSIV desabilitado. **Tabela "Galho 10 → spec Jakarta (Galho 7)"** (`@Entity`↔JPA, persistence context↔EntityManager, `@Transactional`↔JTA + proxy AOP do Galho 8). Cheatsheet nota→problema. Munição de entrevista. Armadilhas de raciocínio: "o repositório vai direto no banco" (há a engrenagem toda); "JPA resolve tudo" (escape hatch); "EAGER é mais simples" (N+1). Fontes: docs.spring.io, hibernate.org.

## 6. Pré-flight: verificações feitas

Executado nesta fase de brainstorming (2026-06-09); itens version-specific re-confirmados na execução de cada nota via WebFetch:

1. **Tronco 1 mapeado** — `Backend/Spring Data JPA.md` (1313 linhas, `publish: false`, `status: evergreen`) lido **inteiro**. Cobre todo o escopo do galho de forma monolítica. **Poda integral** (padrão JavaFX). Seções: O que é, Entidades JPA, Relacionamentos, Fetch strategies (+N+1), Spring Data Repositories, EntityManager e Session, Transações, Caching, Batch operations, Testando JPA, Flyway, Quando NÃO usar JPA, Armadilhas, Na prática (fabricação), How to explain in English, Recursos, Veja também.
2. **Tronco 2 mapeado** — `Backend/Spring Boot.md` seção `## Gerenciamento de transações — @Transactional deep dive` (~67-219) lida; **deixada intacta pelos Galhos 8/9 de propósito**. Demais seções já são callouts (8/9) ou de outros galhos. **Poda cirúrgica** (uma seção).
3. **Fabricação confirmada** — `Spring Data JPA.md`: `Patient`/`Doctor`/`Appointment` em todo o corpo, `## Na prática (da minha experiência)` (incidente fabricado do MedEspecialista, linhas ~1180-1211), `## How to explain in English` 1ª pessoa. **Some toda com a poda integral.** `Spring Boot.md`: `Patient` na linha ~175 da seção de transações → some com a poda cirúrgica. A fabricação sob `## Camadas típicas / ### Persistência` (~390) **permanece** (não é seção deste galho). Notas usam `Order`/`Customer`/`Product`.
4. **Dívida reversa localizada** — 11 ponteiros inline + 3 parágrafos de fronteira (§3.6), em: MOC central :40, Spring Boot :63, Jakarta 09 :57/152/333, Jakarta 10 :160/331, Jakarta 11 (JTA) :35, Web 05 :133/378, Web 08 :236, e os parágrafos Jakarta index :30 / Spring Core index :32 / Web index :32. Horizonte-lists (Spring Core :97, Web :95) intactos. Confirmar linhas na execução.
5. **Dicionário** — **272 verbetes** após o Galho 9; seções alfabéticas únicas `## A`…`## Z`; verbetes `### `; `updated: 2026-06-08`. Verbetes de spec JPA/EntityManager/JTA (do Galho 7) e `@Transactional` (do Galho 8) podem já existir — conferir e linkar, nunca duplicar. Expansão alfabética (~30), nunca recriar/reordenar; conferir âncoras 1:1.
6. **MOC central** — `03-Dominios/Tecnologia/Java/index.md:40` é a linha do Galho 10 (`*(planejado)*`); galhos ativos usam `N. [[path/index|Title]] — summary`; `updated: 2026-06-08`.
7. **Troncos intocáveis** — `Backend/Spring Security.md` (Galho 12), `Backend/Kafka/` (Galho 14), `Backend/gRPC e Go.md` (Galho 14). `Backend/Testes em Java.md` (Galho 13).
8. **Versões a cravar via WebFetch na execução** — Hibernate ORM (versão atual da família 6.x/7.x — baseline **6.x**), Spring Data JPA (versão atual), Jakarta Persistence 3.2 (EE 11 — cravado no Galho 7), `@GeneratedValue` strategies (UUID na **JPA 3.1**), `@Transactional(readOnly)`, Flyway vs Liquibase atuais. Spring Boot 3.x / Hibernate 6.x baseline (`jakarta.persistence.*`, Java 17), citando 4.x/7.x como "mais recente". Fonte: `docs.spring.io`, `hibernate.org`, `jakarta.ee`, `documentation.red-gate.com`, `docs.liquibase.com`.

Nenhum número de adoção é inventado. Quando faltar fato verificável, **PERGUNTAR** antes de escrever.

## 7. Critérios de aceitação do galho

Além dos critérios gerais (§10 do roadmap):

1. 17 notas em `03-Dominios/Tecnologia/Java/Persistência de dados/`, frontmatter completo com `fase:`, `publish: true`, distribuídas 5/6/6.
2. MOC do galho com 3 subseções de fase + 5 rotas alternativas + dataview + folder-link resolve (`index.md` presente).
3. Dicionário de Java **expandido** (não recriado) com ~30 verbetes; verbetes dos Galhos 1-9 intactos; `updated: 2026-06-09`; dups conferidos e linkados (não duplicar `JPA`/`EntityManager`/`persistence context`/`@Transactional`/`JTA`/`owning side`/`JPQL` do Galho 7-8); headings conferidos 1:1 com as âncoras usadas nas notas (via grep).
4. MOC central `Java/index.md` com Galho 10 ativado (linha 40 vira wikilink); resto intacto.
5. **Poda dos dois troncos executada**: `Spring Data JPA.md` reduzido a hub (poda integral, fabricação do MedEspecialista some, `publish: false` mantido); `Spring Boot.md` seção `## Gerenciamento de transações` vira callout (poda cirúrgica). **Seções de outros galhos intactas** no `Spring Boot.md` (callouts dos Galhos 8/9; `### Persistência`/`### Bean Validation` sob Camadas típicas; WebFlux/Cloud/Troubleshooting). `Spring Security.md`/`Kafka/` intactos.
6. **Dívida reversa quitada**: os 11 ponteiros inline + 3 parágrafos de fronteira com wikilinks corretos (Jakarta 09 :57/152/333→notas 01/07, Jakarta 10 :160/331→notas 03/07, JTA :35→Galho 8 + nota 12, Web 05/08→notas 10/12, Spring Boot :63→nota 12, etc.); galhos ainda inexistentes (11-16) permanecem texto "(planejado)"; horizonte-lists intactos.
7. Cada nota: TL;DR; code samples compiláveis (Java moderno, records pra DTO/projection, `jakarta.persistence.*`, fences corretas — `java`/`sql`/`yaml`/`json`); "Em entrevista" com `### Frase pronta (inglês)` 3+ sentenças + `### Vocabulário` tabela 6+ termos PT→EN; "Armadilhas" com exemplo+fix (≥2 Iniciado, ≥3 Adepto/Magus); wikilinks (galho + MOC central + Galho 7 quando operacionalizar spec + Galho 8 quando usar o mecanismo do `@Transactional` + Galho 9 quando tocar DTO/borda + Dicionário); "Referências" com docs oficiais verificadas.
8. **Tripla fronteira-assinatura respeitada**: cada conceito que operacionaliza spec linka de volta ao Galho 7 sem re-explicar; o `@Transactional` linka o mecanismo do Galho 8; o que toca a borda linka o Galho 9; galhos 11-16 só como texto "(planejado)"; nenhum wikilink pra galho inexistente.
9. **Fronteiras de escopo respeitadas**: persistência **bloqueante** (R2DBC/reativo = Galho 11); auditoria só como mecânica JPA (`@CreatedDate`), segurança de dados = Galho 12; testes de repositório só citados (Testcontainers/`@DataJpaTest` = Galho 13); saga/CQRS/sharding = Galho 16; zero conteúdo profundo de Reativa/Security/Test/Distribuído.
10. Zero fabricação de experiência pessoal; zero estatística de adoção inventada; afirmações version-specific citam a versão verificada via WebFetch.
11. 1 commit por nota; sem `Co-Authored-By: Claude`; sem `--no-verify`; stage nominal (nunca `-A`); subagents write-only, controlador commita.
12. `verificar-wikilinks` roda limpo na pasta do galho (as ~204 quebras legadas da árvore Java NÃO são deste galho; evitar âncoras same-file).

## 8. Riscos e mitigações

| Risco | Mitigação |
|---|---|
| **Re-explicar a spec Jakarta (JPA/EntityManager/JTA)** em vez de linkar de volta (1ª face da fronteira) | Restrição 4.3.1; review por fase checa cada nota que operacionaliza spec; capstone mapeia em tabela; cada conceito espelhado tem wikilink obrigatório pro Galho 7. |
| **Re-explicar o mecanismo (AOP/proxy do `@Transactional`)** em vez de linkar ao Galho 8 (2ª face) | Restrição 4.3.1; a nota 12 cobre **comportamento**, linka o **mecanismo** (G8 notas 09/10); review por fase. |
| **Re-explicar DTO/serialização** em vez de linkar ao Galho 9 (3ª face) | Notas 07/10 linkam G9 nota 05; a entidade vive aqui, o DTO é a borda. |
| **Copiar fabricação dos troncos** (`Patient`/MedEspecialista/"incidente memorável") pras notas | Os dois troncos são contraexemplo (restrição 4.3.2); poda integral faz a fabricação sumir; exemplos neutros `Order`/`Customer`; review por fase grep `Patient|MedEspecialista|minha|Doctor|Appointment`. |
| **Poda integral perder conteúdo bom** do `Spring Data JPA.md` | O conteúdo bom **migra pras notas** (refinado/higienizado) ANTES da poda; a poda é o último passo; commit reversível. |
| **Poda cirúrgica danificar seções de outros galhos** no `Spring Boot.md` | Ler o tronco primeiro (§9 roadmap); podar **só** `## Gerenciamento de transações`; callouts dos Galhos 8/9 e `### Persistência`/`### Bean Validation` explicitamente intocáveis. |
| **Invadir Galho 11 (reativo)** ao falar de fetch/queries | Persistência bloqueante; R2DBC = texto "(planejado)"; review por fase. |
| **Invadir Galho 13 (testes)** ao falar de Testcontainers/`@DataJpaTest` | Citar que se testa com banco real, sem ensinar a stack; `@DataJpaTest`/Testcontainers = Galho 13 (texto). |
| **Inventar API/versão "de memória"** (Hibernate/Spring Data version, UUID JPA 3.1, Flyway vs Liquibase) | WebFetch no Step 1 das notas version-specific (02/16/17); baseline Boot 3.x/Hibernate 6.x; Referências com fonte oficial. |
| Versões envelhecerem (Boot 3.x vs 4.x, Hibernate 6.x vs 7.x, RFC/spec) | Baseline 3.x/6.x (como Galhos 8/9), citando 4/7 como "mais recente"; WebFetch por nota version-specific; declarar version-specificity no corpo. |
| Galho denso (17 notas) inflar nº de notas ou notas individuais (transações/N+1/caching) | Distribuição 5/6/6 fixada; se uma nota passar de ~600 linhas, dividir nota (não galho — Locking ficou separado de Transações justamente por isso); capstone com cheatsheet enxuto. |
| Dicionário: duplicar verbete já existente (`JPA`, `EntityManager`, `@Transactional`, `JTA`, `JPQL`, `owning side`) | Grep dos existentes antes de inserir; quando tocar um existente, **linkar** em vez de duplicar; inserção alfabética, nunca recriar; conferir âncoras 1:1. |
| Bot de backup (Obsidian Git) commitando no meio | Padrão dos Galhos 2-9: subagents write-only; controlador commita imediatamente após cada nota com `git add` nominal (nunca `-A`); guardar contra `.git/index.lock`. |

## 9. Próximos passos

1. **Aprovação deste spec**
2. **Plano de execução** via skill `superpowers:writing-plans` → `docs/superpowers/plans/2026-06-09-java-galho-10-persistencia-execution.md`
3. **Execução** via `superpowers:subagent-driven-development` **direto na `main`** (subagents write-only; sonnet por padrão, opus nas notas 01/08/12/14/17; review **por fase** + fix loop; push manual do usuário)
4. **Verificação** de wikilinks + conferência de âncoras do Dicionário
5. **Atualização da memória** `project_trilha_java` (Galho 10 completo) antes do próximo galho

## 10. Documentos relacionados

- `2026-06-02-java-senior-roadmap-design.md` — roadmap macro (18 galhos)
- `2026-06-08-java-galho-09-web-rest-design.md` / `...-execution.md` — Galho 9 (molde mais recente de poda parcial + dupla natureza + dívida reversa; este galho usa-o como template direto)
- `2026-06-08-java-galho-08-spring-core-design.md` — Galho 8 (dependência: o mecanismo AOP do `@Transactional`)
- `2026-06-07-java-galho-07-jakarta-ee-design.md` — Galho 7 (dependência conceitual: dono das specs JPA/EntityManager/JTA que este galho operacionaliza)
- Galho 6 (JavaFX) — template de **poda integral** de tronco monolítico (`Frontend/JavaFX.md` reduzido a hub)
- Artefatos a atualizar: `03-Dominios/Tecnologia/Java/Dicionário de Java.md`, `03-Dominios/Tecnologia/Java/index.md`, `03-Dominios/Tecnologia/Java/Backend/Spring Data JPA.md` (poda integral), `03-Dominios/Tecnologia/Java/Backend/Spring Boot.md` (poda cirúrgica — seção transações), `Jakarta EE/09 - JPA`, `Jakarta EE/10 - EntityManager`, `Jakarta EE/11 - JTA`, `Jakarta EE/index.md`, `Spring Core e Boot/index.md`, `Web e APIs REST/05 - Serialização JSON`, `Web e APIs REST/08 - Validação na borda`, `Web e APIs REST/index.md` (dívida reversa)
- Fontes-base do galho: `docs.spring.io/spring-data/jpa/reference/`, `hibernate.org/orm/documentation`, `jakarta.ee/specifications/persistence/`, `documentation.red-gate.com/fd` (Flyway), `docs.liquibase.com`
- Memórias: [[project_trilha_java]], [[project_trilhas_fases_aprendizado]], [[project_tronco_galhos_pattern]], [[feedback_galhos_direto_main]], [[feedback_no_fabrication]], [[feedback_quartz_index]], [[feedback_commits]], [[feedback_dataview_inline_code]], [[feedback_notas_atomicas]], [[feedback_enriquecimento_feynman]]
