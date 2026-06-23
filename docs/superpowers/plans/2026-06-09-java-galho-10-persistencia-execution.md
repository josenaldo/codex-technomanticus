# Galho 10 — Persistência de dados (Java Senior) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Criar o Galho 10 da trilha Java Senior — 17 notas atômicas (camada de persistência, entidade JPA, persistence context, Spring Data repositories, relacionamentos, fetch/N+1, queries JPQL/native, projections, paginação, transações operacionais, locking, caching, Specifications/Criteria, migrations, capstone) em 3 fases + MOC do galho + expansão do Dicionário + ativação do MOC central + **poda de DOIS troncos** (integral do `Backend/Spring Data JPA.md` + cirúrgica da seção de transações do `Backend/Spring Boot.md`) + **quitação de 11 ponteiros inline + 3 parágrafos de fronteira de dívida reversa**.

**Architecture:** Padrão galhos + 3 fases (Iniciado/Adepto/Magus). Pasta flat `03-Dominios/Tecnologia/Java/Persistência de dados/`, notas `publish: true` em PT-BR, numeração global 01-17 (5/6/6). **Galho HÍBRIDO:** REFATOR (o tronco `Spring Data JPA.md` inteiro é higienizado e migrado pras notas, depois podado integral; a seção `## Gerenciamento de transações` do `Spring Boot.md` é refinada e podada cirúrgica) + PESQUISA (afirmações version-specific — Hibernate/Spring Data version, UUID JPA 3.1, Flyway vs Liquibase — confirmadas via WebFetch). **TRIPLA fronteira-assinatura:** cada conceito que **operacionaliza uma spec** linka de volta ao **Galho 7** (JPA/EntityManager/JTA) sem re-explicar; o `@Transactional` linka o **mecanismo** do **Galho 8** (proxy AOP/self-invocation); o que toca a **borda** (entidade vs DTO) linka o **Galho 9** (serialização/validação). Galhos 11/12/13/16 = texto "(planejado)", sem wikilink. **Direto na `main`** ([[feedback_galhos_direto_main]]); push manual do usuário.

**Tech Stack:** Obsidian Flavored Markdown, frontmatter YAML, wikilinks, callouts, Dataview, Quartz v4. Verificação via WebFetch (`docs.spring.io/spring-data/jpa/`, `hibernate.org/orm/documentation`, `jakarta.ee/specifications/persistence/`, `documentation.red-gate.com/fd`, `docs.liquibase.com`).

---

## Convenções aplicadas a TODAS as notas (ler antes de qualquer task)

**Frontmatter** (ajustar `title`/`fase`/`tags`/`aliases` por nota; `created`/`updated: 2026-06-09`):

```yaml
---
title: "<título sem prefixo numérico>"
created: 2026-06-09
updated: 2026-06-09
type: concept
progress: backlog
status: seedling
publish: true
fase: iniciado | adepto | magus
tags:
  - java
  - persistencia
  - <fase>
  - <1-3 tags de conceito: jpa, hibernate, entidade, relacionamentos, fetch, n-mais-1, spring-data, jpql, projection, paginacao, transacao, locking, cache, migrations>
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
5. `## Na prática` — código compilável; framing neutro; **NUNCA** 1ª pessoa, `Patient`, `Doctor`, `Appointment`, `Josenaldo`, `MedEspecialista`. Domínios neutros: `Order`, `Customer`, `Product`, `OrderRepository`, `CustomerService`. Records pra DTO/projection. Imports `jakarta.persistence.*` (Boot 3).
6. `## Armadilhas` — ≥2 (Iniciado) / ≥3 (Adepto/Magus). Cada uma: `### (N) Título` + descrição + exemplo curto + fix em 1 linha.
7. `## Em entrevista` — `### Frase pronta (inglês)` com **3+ sentenças** (trade-off + decisão + caveat) + `### Vocabulário` **6+ termos** em tabela `| Termo PT | Termo EN |`.
8. `## Veja também` — wikilinks SEM backticks, SEM âncoras same-file `[[#...]]`. Sempre: notas do galho + `[[03-Dominios/Tecnologia/Java/Persistência de dados/index|Persistência de dados (MOC do galho)]]` + `[[03-Dominios/Tecnologia/Java/index|Trilha Java]]` + (quando operacionalizar spec) a nota do **Galho 7** + (quando usar o mecanismo do `@Transactional`) a nota do **Galho 8** + (quando tocar DTO/borda) a nota do **Galho 9** + verbetes do Dicionário.
9. `## Referências` — docs oficiais consultadas (`docs.spring.io/spring-data/jpa/...`, `hibernate.org/...`, `jakarta.ee/...`, Flyway/Liquibase docs).

**Tamanho:** 200-500 linhas (densas até 600 — limite de [[feedback_notas_atomicas]]).

**Restrições absolutas:**
- **TRIPLA fronteira-assinatura.** Mapeamento de link-back **Galho 7** (a spec, não re-explicar): `@Entity`/`@Id`/contrato de mapeamento → JPA 09; persistence context/EntityManager/ciclo de vida (conceito) → EntityManager 10; demarcação transacional/JTA → JTA 11. Mapeamento de link-back **Galho 8** (o mecanismo do `@Transactional`): o proxy que intercepta → AOP 09; os limites (self-invocation, `private`/`final`) → Self-invocation 10. Mapeamento de link-back **Galho 9** (a borda): entidade vaza no JSON → DTO → Serialização JSON 05; validação de negócio (service) vs formato (borda) → Validação na borda 08.
- **Galhos 11-16 só como texto "(planejado)", SEM wikilink.** Greps de review checam `\[\[[^]]*(Galho (11|12|13|16)|WebFlux|R2DBC|reativ|Spring Security|@DataJpaTest|Testcontainers|saga|CQRS|sharding)`.
- Sem fabricação ([[feedback_no_fabrication]]); **os dois troncos são contraexemplo** (`Patient`/`Doctor`/`Appointment`/"incidente memorável" do MedEspecialista/1ª pessoa — NUNCA copiar; usar `Order`/`Customer`/`Product`); **zero estatística de adoção inventada** (regra dos Galhos 5-9) — vale pra "Flyway vs Liquibase" e pra capstone.
- **Pesquisa pras partes version-specific:** notas 02/16/17 fundam-se em WebFetch (Step 1); qualquer outra que cravar versão também confirma. Toda afirmação version-specific verificada: **versão atual do Hibernate ORM** (baseline **6.x**) e do **Spring Data JPA**; **Jakarta Persistence 3.2** (EE 11 — cravado no Galho 7); **`@GeneratedValue` strategies** (IDENTITY/SEQUENCE/TABLE/AUTO/**UUID na JPA 3.1**); **`@Transactional(readOnly)`**; **Flyway vs Liquibase** atuais. Boot 4.x/Hibernate 7.x já são as releases atuais — **manter 3.x/6.x como baseline** (como os Galhos 8/9), citando 4/7 como "mais recente" quando relevante. Nada de memória.
- **Não re-explicar o que é de outro galho:** spec JPA/EntityManager/persistence context (conceito)/JTA → Galho 7 (linkar); o proxy AOP que faz o `@Transactional`/self-invocation → Galho 8 (linkar); DTO/serialização/validação na borda → Galho 9 (linkar); R2DBC/persistência reativa → Galho 11 (texto); segurança de dados/row-level → Galho 12 (texto); `@DataJpaTest`/Testcontainers/slices → Galho 13 (texto — citar que se testa com banco real, sem ensinar a stack); saga/CQRS/sharding/event sourcing → Galho 16 (texto). Teoria SQL/ACID/isolamento → [[Banco de dados]] (linkar). Concorrência de baixo nível → Galho 4 (linkar).
- Comparações justas (quando X E quando Y): LAZY vs EAGER, `@EntityGraph` vs `JOIN FETCH` vs projection, `Page` vs `Slice`, optimistic vs pessimistic, `@OneToMany` vs entidade associativa, Flyway vs Liquibase, JPA vs jOOQ/JdbcClient.
- Code fences: ` ```java `, ` ```sql ` (DDL/migration), ` ```properties `/` ```yaml ` (config), ` ```json ` (payloads), ` ```bash `, ` ```text `. Sempre fechadas.
- Commits: sem `Co-Authored-By: Claude`; sem `--no-verify`; `git add <path>` nominal (bot de backup roda em timer — NUNCA `-A`; guardar contra `.git/index.lock`); 1 commit por nota; direto na `main`; **sem push, sem deploy**. Subagents NÃO rodam git — o controlador commita.

**Modelo por nota:** sonnet por padrão; **opus** nas **01** (assinatura/tripla fronteira), **08** (N+1 — a mais densa), **12** (transações — comportamento + tripla referência), **14** (caching — os três níveis) e **17** (capstone).

**Fontes oficiais (base):**
- Spring Data JPA reference: `https://docs.spring.io/spring-data/jpa/reference/`
- Spring Data JPA — repositories/query methods: `https://docs.spring.io/spring-data/jpa/reference/repositories/query-methods-details.html`
- Spring Data JPA — `@Query`: `https://docs.spring.io/spring-data/jpa/reference/jpa/query-methods.html`
- Spring Data JPA — projections: `https://docs.spring.io/spring-data/jpa/reference/repositories/projections.html`
- Spring Data JPA — Specifications: `https://docs.spring.io/spring-data/jpa/reference/jpa/specifications.html`
- Spring Data JPA — paging: `https://docs.spring.io/spring-data/jpa/reference/repositories/core-concepts.html`
- Hibernate ORM User Guide: `https://docs.jboss.org/hibernate/orm/current/userguide/html_single/Hibernate_User_Guide.html`
- Jakarta Persistence spec: `https://jakarta.ee/specifications/persistence/`
- Spring transaction management: `https://docs.spring.io/spring-framework/reference/data-access/transaction/declarative.html`
- Spring cache abstraction: `https://docs.spring.io/spring-framework/reference/integration/cache.html`
- Flyway: `https://documentation.red-gate.com/fd`
- Liquibase: `https://docs.liquibase.com`

---

## Task 0: Pré-flight — pasta, terreno e baselines

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Persistência de dados/` (pasta)

- [ ] **Step 1: Confirmar `main`**

```bash
git branch --show-current
```
Expected: `main`. NÃO criar branch.

- [ ] **Step 2: Criar a pasta do galho**

```bash
mkdir -p "03-Dominios/Tecnologia/Java/Persistência de dados"
```

- [ ] **Step 3: Confirmar títulos exatos das notas dos Galhos 7/8/9 (linkadas de volta)**

```bash
ls "03-Dominios/Tecnologia/Java/Jakarta EE/" | grep -E "^(09|10|11) "
ls "03-Dominios/Tecnologia/Java/Spring Core e Boot/" | grep -E "^(09|10) "
ls "03-Dominios/Tecnologia/Java/Web e APIs REST/" | grep -E "^(05|08) "
```
Expected: G7 — `09 - JPA — a especificação de persistência`, `10 - EntityManager e o ciclo de vida da entidade`, `11 - JTA — transações na plataforma`; G8 — `09 - AOP e proxies no Spring`, `10 - Self-invocation e os limites do proxy`; G9 — `05 - Serialização JSON com Jackson`, `08 - Validação na borda`. Anotar divergências.

- [ ] **Step 4: Relocalizar a dívida reversa (11 ponteiros inline + 3 parágrafos — linhas podem ter mudado)**

```bash
grep -rn "Galho 10\|galho 10" "03-Dominios/Tecnologia/Java/Jakarta EE/09 - JPA — a especificação de persistência.md" "03-Dominios/Tecnologia/Java/Jakarta EE/10 - EntityManager e o ciclo de vida da entidade.md" "03-Dominios/Tecnologia/Java/Jakarta EE/11 - JTA — transações na plataforma.md" "03-Dominios/Tecnologia/Java/Jakarta EE/index.md" "03-Dominios/Tecnologia/Java/Spring Core e Boot/index.md" "03-Dominios/Tecnologia/Java/Web e APIs REST/05 - Serialização JSON com Jackson.md" "03-Dominios/Tecnologia/Java/Web e APIs REST/08 - Validação na borda.md" "03-Dominios/Tecnologia/Java/Web e APIs REST/index.md"
grep -n "Galho 10\|planejado" "03-Dominios/Tecnologia/Java/Backend/Spring Boot.md"
```
Expected (anotar linhas reais pra Task 23): Jakarta 09 :~57/152/333; Jakarta 10 :~160/331; JTA 11 :~35; Jakarta index :~30; Spring Core index :~32 (parágrafo) e :~97 (horizonte-list — NÃO tocar); Web 05 :~133/378; Web 08 :~236; Web index :~32 (parágrafo) e :~95 (horizonte-list — NÃO tocar); Spring Boot :~63 (callout AOP).

- [ ] **Step 5: Baseline do Dicionário**

```bash
grep -cE "^### " "03-Dominios/Tecnologia/Java/Dicionário de Java.md"
```
Expected: **272** (baseline pós-Galho 9). Anotar o número real.

- [ ] **Step 6: Mapear os DOIS troncos (pras Tasks 21/22) e confirmar a fabricação**

```bash
grep -nE "^#{2,3} " "03-Dominios/Tecnologia/Java/Backend/Spring Data JPA.md"
grep -nE "^#{2,3} " "03-Dominios/Tecnologia/Java/Backend/Spring Boot.md"
grep -niE "Patient|Doctor|Appointment|Josenaldo|MedEspecialista|minha experiência" "03-Dominios/Tecnologia/Java/Backend/Spring Data JPA.md" | head -30
grep -niE "Patient|Doctor|Appointment" "03-Dominios/Tecnologia/Java/Backend/Spring Boot.md"
```
Expected: `Spring Data JPA.md` (~1313 linhas) cobre **todo** o escopo do galho — **poda INTEGRAL** na Task 21 (vira hub). Confirmar fabricação espalhada (`Patient`/`Doctor`/`Appointment`, `## Na prática (da minha experiência)`, `## How to explain in English`, "incidente memorável") — **some toda com a poda**. No `Spring Boot.md`: confirmar `## Gerenciamento de transações — @Transactional deep dive` ~67-219 (a única seção core deste galho — subseções O básico/Propagation/Isolation/Rollback/Read-only/Timeout/Padrão Service) com `Patient` pontual ~175 (some com a poda cirúrgica na Task 22). INTOCÁVEIS no `Spring Boot.md`: callouts dos Galhos 8/9 (`## O que é`/IoC/AOP/Config/Actuator/`## Spring MVC pipeline`), `## Spring WebFlux`/`## Spring Cloud`/`## Camadas típicas` (incl. `### Persistência` ~383 e `### Bean Validation` ~428 — **deixar intactos**)/`## Troubleshooting`. Anotar ranges reais.

- [ ] **Step 7: Fixar fatos a verificar via WebFetch** — versão atual do Hibernate ORM (baseline 6.x) e do Spring Data JPA; Jakarta Persistence 3.2 (EE 11 — cravado no Galho 7); `@GeneratedValue` strategies (UUID na **JPA 3.1**); semântica de `@Transactional(readOnly)`; Flyway vs Liquibase atuais; Boot 3.x baseline (Java 17, `jakarta.persistence.*`). Nada de memória.

- [ ] **Step 8: Sem commit** (preparação).

---

## Fase INICIADO (notas 01-05)

### Task 1: Nota 01 — O que é a camada de persistência — Spring Data, JPA e Hibernate ⟦opus⟧

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Persistência de dados/01 - O que é a camada de persistência — Spring Data, JPA e Hibernate.md`

- [ ] **Step 1: Pesquisar** — WebFetch `https://docs.spring.io/spring-data/jpa/reference/` + `https://hibernate.org/orm/`. CONFIRMAR: a pilha (seu código → Spring Data JPA → spec JPA → Hibernate → JDBC → banco); JPA = spec (Galho 7), Hibernate = implementação, Spring Data = elimina boilerplate; versão atual do Hibernate ORM (baseline 6.x) e do Spring Data JPA. Refinar a abertura do tronco `Spring Data JPA.md` (`## O que é`), **higienizando**.

- [ ] **Step 2: Escrever** — `fase: iniciado`, tags `[java, persistencia, iniciado, jpa]`, aliases `["camada de persistência", "Spring Data JPA", "ORM em Java"]`. **Nota-assinatura da TRIPLA fronteira.** Conteúdo:
  - TL;DR: a persistência na stack Spring é uma pilha de camadas — Spring Data elimina o boilerplate do repositório sobre a spec JPA (Galho 7), que o Hibernate implementa; o `@Transactional` roda sobre o proxy AOP do Galho 8 e a borda recebe DTO (Galho 9), não a entidade.
  - `## O que é` — a pilha em camadas (diagrama ```text: seu código → Spring Data JPA → JPA spec → Hibernate → JDBC → banco) e o que cada uma resolve.
  - `## Por que importa` — é a camada de dados de quase todo backend Spring; entrevista cobra "spec vs implementação" e "o que o Spring Data esconde".
  - `## Como funciona` — H3s: "JPA: a especificação (Galho 7) — o contrato `@Entity`/`@Id`", "Hibernate: a implementação (o que você usa 99% do tempo quando diz 'JPA')", "Spring Data JPA: a camada que elimina o boilerplate do repositório", "A tripla fronteira: a spec (Galho 7), o mecanismo do `@Transactional` (Galho 8), a borda/DTO (Galho 9)".
  - `## Na prática` — um `OrderRepository extends JpaRepository<Order, Long>` mínimo + a entidade `Order` mínima (```java); `pom.xml` com `spring-boot-starter-data-jpa` (```xml).
  - `## Armadilhas` — ≥2: (1) dizer "JPA é o Hibernate" (spec ≠ implementação — linka G7 nota 09); (2) achar que "Spring Data É a JPA" (é uma camada acima).
  - `## Em entrevista` + `## Veja também` ([[03 - O persistence context e os estados da entidade]], [[04 - Spring Data repositories — JpaRepository e query methods derivados]], **[[03-Dominios/Tecnologia/Java/Jakarta EE/09 - JPA — a especificação de persistência|JPA (a spec)]]**, **[[03-Dominios/Tecnologia/Java/Spring Core e Boot/09 - AOP e proxies no Spring|AOP e proxies]]** (o mecanismo do `@Transactional`), **[[03-Dominios/Tecnologia/Java/Web e APIs REST/05 - Serialização JSON com Jackson|Serialização JSON (DTO na borda)]]**, MOC galho, MOC central, verbetes `Spring Data JPA`/`Hibernate`) + `## Referências`.

- [ ] **Step 3: Verificar**
```bash
grep -cE "^## (O que é|Por que importa|Como funciona|Na prática|Armadilhas|Em entrevista|Veja também|Referências)" "03-Dominios/Tecnologia/Java/Persistência de dados/01 - O que é a camada de persistência — Spring Data, JPA e Hibernate.md"
grep -riE "Patient|Doctor|Appointment|MedEspecialista|minha experiência" "03-Dominios/Tecnologia/Java/Persistência de dados/01 - O que é a camada de persistência — Spring Data, JPA e Hibernate.md"
grep -c "Jakarta EE/09 - JPA" "03-Dominios/Tecnologia/Java/Persistência de dados/01 - O que é a camada de persistência — Spring Data, JPA e Hibernate.md"
```
Expected: ≥7 seções; segundo grep **VAZIO**; terceiro ≥1 (link de volta ao Galho 7).

- [ ] **Step 4: Commit** — `git add "<path>"` && `git commit -m "feat(java): galho 10 nota 01 — O que é a camada de persistência (Spring Data, JPA, Hibernate)"`

### Task 2: Nota 02 — A entidade JPA — @Entity, @Id e geração de chave

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Persistência de dados/02 - A entidade JPA — @Entity, @Id e geração de chave.md`

- [ ] **Step 1: Pesquisar** — WebFetch `https://jakarta.ee/specifications/persistence/` + Hibernate User Guide (seção identifiers). CONFIRMAR: `@Entity`/`@Table`/`@Column`/`@Id`/`@GeneratedValue`; estratégias IDENTITY/SEQUENCE/TABLE/AUTO/**UUID (JPA 3.1)**; `@SequenceGenerator`/`allocationSize`; construtor sem-arg. **Version-specific (WebFetch obrigatório).**

- [ ] **Step 2: Escrever** — `fase: iniciado`, tags `[java, persistencia, iniciado, entidade, jpa]`. Conteúdo:
  - TL;DR: uma classe vira tabela com `@Entity`+`@Id`; `@GeneratedValue` define como a PK é gerada (SEQUENCE como default recomendado, IDENTITY impede batch); a entidade exige construtor sem-arg e `equals`/`hashCode` por business key.
  - H3s: "`@Entity`/`@Table`/`@Column`: o mapeamento básico", "`@Id` e `@GeneratedValue` (IDENTITY/SEQUENCE/TABLE/AUTO/UUID — quando usar cada; UUID na JPA 3.1)", "`equals`/`hashCode` por business key (nunca `@Data` do Lombok; id gerado é null antes do save)", "Por que record não serve como entidade".
  - `## Na prática` — entidade `Order` com `@Id @GeneratedValue(strategy = SEQUENCE)` + `equals`/`hashCode` por `externalId` UUID (```java).
  - `## Armadilhas` — ≥2: (1) `@Data` do Lombok em entidade (quebra equals/toString com lazy); (2) `equals` por id gerado (null antes do save → dois objetos diferentes dão `true`); (3) `IDENTITY` em workload write-heavy (impede batch — use SEQUENCE).
  - `## Veja também` — [[01 - O que é a camada de persistência — Spring Data, JPA e Hibernate]], [[03 - O persistence context e os estados da entidade]], **[[03-Dominios/Tecnologia/Java/Jakarta EE/09 - JPA — a especificação de persistência|JPA (a spec define as anotações)]]**, **[[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/11 - Annotations|Annotations]]** (a mecânica), verbetes `@GeneratedValue`.

- [ ] **Step 3: Verificar** — ≥7 seções; anti-fabricação VAZIO; link Galho 7 nota 09 presente; `grep -i "3.1"` ≥1 (UUID).

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 10 nota 02 — a entidade JPA (@Entity, @Id, @GeneratedValue)"`

### Task 3: Nota 03 — O persistence context e os estados da entidade

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Persistência de dados/03 - O persistence context e os estados da entidade.md`

- [ ] **Step 1: Pesquisar** — WebFetch Hibernate User Guide (persistence context / flushing / dirty checking) + `https://docs.spring.io/spring-data/jpa/reference/`. CONFIRMAR: os 4 estados (transient/managed/detached/removed); persistence context = cache de 1º nível (identidade); dirty checking; `save` do Spring Data = persist|merge; flush. Refinar do tronco `## EntityManager e Session` (Persistence Context, Flush, Dirty checking, save/merge), higienizando.

- [ ] **Step 2: Escrever** — `fase: iniciado`, tags `[java, persistencia, iniciado, jpa, hibernate]`. Conteúdo:
  - TL;DR: o persistence context é um cache de 1º nível por transação — entidades managed têm identidade (mesma query 2x = 1 SQL) e dirty checking (mudou um setter → UPDATE no commit, sem `save()`).
  - H3s: "Os 4 estados (transient → managed → detached → removed) e as transições", "Persistence context = cache de 1º nível (identidade: `p1 == p2`)", "Dirty checking: por que você não chama `save()` em entidade managed", "`save` do Spring Data = persist (id null) ou merge (id existe); flush (commit / antes de query / explícito)".
  - `## Na prática` — `@Transactional` carregando o mesmo `Order` 2x (1 SQL) + mudando um campo sem `save()` (dirty checking) (```java).
  - `## Armadilhas` — ≥2: (1) `save()` redundante em entidade managed (dirty checking já faz); (2) esperar persistir fora de transação (`TransactionRequiredException`); (3) acessar lazy em entidade detached (prenúncio da 07).
  - `## Veja também` — [[01 - O que é a camada de persistência — Spring Data, JPA e Hibernate]], [[07 - Fetch strategies — LAZY, EAGER e a LazyInitializationException]], **[[03-Dominios/Tecnologia/Java/Jakarta EE/10 - EntityManager e o ciclo de vida da entidade|EntityManager e o ciclo de vida da entidade]]** (o conceito, na spec), verbetes `persistence context (1º nível)`/`dirty checking`.

- [ ] **Step 3: Verificar** — ≥7 seções; anti-fabricação VAZIO; link Galho 7 nota 10 presente.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 10 nota 03 — o persistence context e os estados da entidade"`

### Task 4: Nota 04 — Spring Data repositories — JpaRepository e query methods derivados

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Persistência de dados/04 - Spring Data repositories — JpaRepository e query methods derivados.md`

- [ ] **Step 1: Pesquisar** — WebFetch `https://docs.spring.io/spring-data/jpa/reference/repositories/query-methods-details.html` + `.../repositories/core-concepts.html`. CONFIRMAR: hierarquia `Repository`→`CrudRepository`→`PagingAndSortingRepository`→`JpaRepository`; derived queries e keywords; o repositório é um proxy gerado.

- [ ] **Step 2: Escrever** — `fase: iniciado`, tags `[java, persistencia, iniciado, spring-data]`. Conteúdo:
  - TL;DR: você declara uma interface `extends JpaRepository<T, ID>` e o Spring Data gera a implementação (CRUD herdado + queries derivadas do nome do método).
  - H3s: "A hierarquia (`Repository`→`CrudRepository`→`PagingAndSortingRepository`→`JpaRepository`)", "CRUD herdado (`save`/`findById`/`findAll`/`delete`/`count`/`existsById`)", "Derived queries: o SQL gerado do nome do método (keywords `And`/`Or`/`Between`/`GreaterThan`/`OrderBy`/`In`/`Containing`)", "Quando a derived query fica ilegível → `@Query` (nota 09)".
  - `## Na prática` — `OrderRepository` com `findByCustomerEmail`, `findByStatusAndTotalGreaterThan`, `countByStatus`, `existsByExternalId` (```java).
  - `## Armadilhas` — ≥2: (1) derived query gigante e ilegível (`findByAAndBOrCOrderByD...` → use `@Query`); (2) `findById` quando bastava `existsById` (mais rápido); (3) assumir que todo método derivado é eficiente.
  - `## Veja também` — [[01 - O que é a camada de persistência — Spring Data, JPA e Hibernate]], [[09 - Consultas com @Query — JPQL, native e @Modifying]], **[[03-Dominios/Tecnologia/Java/Spring Core e Boot/09 - AOP e proxies no Spring|AOP e proxies]]** (o repositório é um proxy/bean gerado), verbetes `JpaRepository`/`derived query method`.

- [ ] **Step 3: Verificar** — ≥7 seções; anti-fabricação VAZIO; link Galho 8 presente.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 10 nota 04 — Spring Data repositories e query methods derivados"`

### Task 5: Nota 05 — Relacionamentos — @ManyToOne, @OneToMany e o owning side

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Persistência de dados/05 - Relacionamentos — @ManyToOne, @OneToMany e o owning side.md`

- [ ] **Step 1: Pesquisar** — WebFetch Hibernate User Guide (associations) + `https://jakarta.ee/specifications/persistence/`. CONFIRMAR: `@ManyToOne` (owning, tem a FK) vs `@OneToMany(mappedBy)` (inverse); `@JoinColumn`; defaults de fetch (`@ManyToOne`/`@OneToOne` EAGER, `@OneToMany`/`@ManyToMany` LAZY). Refinar do tronco `## Relacionamentos` (@OneToMany/@ManyToOne), higienizando (`Doctor`/`Appointment` → `Customer`/`Order`).

- [ ] **Step 2: Escrever** — `fase: iniciado`, tags `[java, persistencia, iniciado, relacionamentos]`. Conteúdo:
  - TL;DR: o par `@ManyToOne`/`@OneToMany` modela um-para-muitos; o **owning side** (`@ManyToOne`, com a FK) controla a relação, o inverse (`mappedBy`) só espelha; helper methods mantêm os dois lados sincronizados.
  - H3s: "Owning side (`@ManyToOne`, tem a FK) vs inverse side (`mappedBy`)", "`@JoinColumn` e o lado dono", "Bidirecional + helper methods (`addOrder`/`removeOrder`)", "Os defaults de fetch (`@ManyToOne` EAGER — a armadilha que a nota 07 ataca)".
  - `## Na prática` — `Customer` (`@OneToMany(mappedBy="customer")`) e `Order` (`@ManyToOne(fetch=LAZY) @JoinColumn`) + helper methods (```java).
  - `## Armadilhas` — ≥2: (1) esquecer `mappedBy` (duas FKs / join table inesperada); (2) não sincronizar os dois lados (estado inconsistente em memória); (3) confiar no default EAGER do `@ManyToOne`.
  - `## Veja também` — [[06 - @ManyToMany, @OneToOne, cascade e orphanRemoval]], [[07 - Fetch strategies — LAZY, EAGER e a LazyInitializationException]], **[[03-Dominios/Tecnologia/Java/Jakarta EE/09 - JPA — a especificação de persistência|JPA (os defaults de fetch são da spec)]]**, verbetes `@ManyToOne / @OneToMany`/`owning side / inverse side`.

- [ ] **Step 3: Verificar** — ≥7 seções; anti-fabricação VAZIO (sem `Doctor`/`Appointment`); link Galho 7 presente.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 10 nota 05 — relacionamentos (@ManyToOne, @OneToMany, owning side)"`

---

## Fase ADEPTO (notas 06-11)

### Task 6: Nota 06 — @ManyToMany, @OneToOne, cascade e orphanRemoval

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Persistência de dados/06 - @ManyToMany, @OneToOne, cascade e orphanRemoval.md`

- [ ] **Step 1: Pesquisar** — WebFetch Hibernate User Guide (associations, cascading). CONFIRMAR: `@ManyToMany` + `@JoinTable`; entidade associativa explícita; `@OneToOne` (lazy problemático sem `@MapsId`); tipos de `cascade` (PERSIST/MERGE/REMOVE/REFRESH/DETACH/ALL) e `orphanRemoval`. Refinar do tronco (`@ManyToMany`, `@OneToOne`), higienizando.

- [ ] **Step 2: Escrever** — `fase: adepto`, tags `[java, persistencia, adepto, relacionamentos]`. ≥3 H3s: "`@ManyToMany` + `@JoinTable` (e por que preferir entidade associativa quando a relação tem atributos)", "`@OneToOne` (e o lazy problemático sem `@MapsId`)", "`cascade` (PERSIST/MERGE/REMOVE/ALL): propagando operações pai→filho", "`orphanRemoval`: a diferença pra `cascade = REMOVE`". `## Na prática`: `@ManyToMany` Product↔Tag + a versão com entidade associativa `OrderItem` (```java). `## Armadilhas` ≥3: `@ManyToMany` escondendo entidade que merecia existir (quando precisa de quantidade/data); `cascade = ALL` deletando filhos sem querer; `@OneToOne` EAGER dobrando JOINs. `## Veja também` — [[05 - Relacionamentos — @ManyToOne, @OneToMany e o owning side]], [[07 - Fetch strategies — LAZY, EAGER e a LazyInitializationException]], verbetes `@ManyToMany`/`@OneToOne`/`cascade / orphanRemoval`.

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; anti-fabricação VAZIO.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 10 nota 06 — @ManyToMany, @OneToOne, cascade e orphanRemoval"`

### Task 7: Nota 07 — Fetch strategies — LAZY, EAGER e a LazyInitializationException

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Persistência de dados/07 - Fetch strategies — LAZY, EAGER e a LazyInitializationException.md`

- [ ] **Step 1: Pesquisar** — WebFetch Hibernate User Guide (fetching) + `https://docs.spring.io/spring-boot/` (open-in-view). CONFIRMAR: LAZY vs EAGER (proxy/coleção lazy); regra prática sempre LAZY; `LazyInitializationException` (acesso fora da tx); OSIV (`spring.jpa.open-in-view`, default `true` no Boot). Refinar do tronco `## Fetch strategies` (LAZY vs EAGER) + `### LazyInitializationException` + `### Open Session In View`, higienizando.

- [ ] **Step 2: Escrever** — `fase: adepto`, tags `[java, persistencia, adepto, fetch]`. ≥3 H3s: "LAZY vs EAGER (proxy / coleção lazy) e a tabela de defaults", "A regra prática: sempre LAZY (o `@ManyToOne` EAGER é o vilão escondido)", "`LazyInitializationException`: acesso lazy fora da transação (e as soluções de borda)", "Open Session In View: o Boot habilita por default — `open-in-view: false` em produção e por quê". **A entidade que vaza no JSON → DTO** linka **G9 nota 05**. `## Na prática`: `@ManyToOne(fetch=LAZY)` + a exceção ao acessar a coleção fora da tx + o fix (DTO/`@EntityGraph`) (```java). `## Armadilhas` ≥3: `@ManyToOne` EAGER (5 JOINs em toda query); OSIV escondendo N+1; `@Transactional` no controller só pra evitar a exceção (acopla camadas). `## Veja também` — [[05 - Relacionamentos — @ManyToOne, @OneToMany e o owning side]], [[08 - O problema N+1 e suas soluções — @EntityGraph, JOIN FETCH, batch size]], **[[03-Dominios/Tecnologia/Java/Web e APIs REST/05 - Serialização JSON com Jackson|Serialização JSON (DTO na borda)]]**, verbetes `fetch strategy (LAZY/EAGER)`/`LazyInitializationException`/`Open Session In View (OSIV)`.

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; link Galho 9 nota 05 presente; anti-fabricação VAZIO.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 10 nota 07 — fetch strategies (LAZY, EAGER, LazyInitializationException)"`

### Task 8: Nota 08 — O problema N+1 e suas soluções — @EntityGraph, JOIN FETCH, batch size ⟦opus⟧

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Persistência de dados/08 - O problema N+1 e suas soluções — @EntityGraph, JOIN FETCH, batch size.md`

- [ ] **Step 1: Pesquisar** — WebFetch Hibernate User Guide (fetching, batch fetching) + `https://docs.spring.io/spring-data/jpa/reference/jpa/entity-graph.html`. CONFIRMAR: o N+1 (1 + N queries); `@EntityGraph` (attributePaths / named); `JOIN FETCH` (uma coleção/query, cartesian product); `@BatchSize`; o warning `HHH000104` (fetch de coleção + paginação → memória). Refinar do tronco `### N+1: o bug mais caro` + `### Soluções para N+1`, higienizando.

- [ ] **Step 2: Escrever** — `fase: adepto`, tags `[java, persistencia, adepto, fetch, n-mais-1]`. **A nota mais densa do galho.** ≥3 H3s: "O que é o N+1 (1 query pai + N filhos ao iterar coleção lazy — exemplo)", "Detectar: SQL logging, `generate_statistics`, contador de query no teste", "Soluções: `@EntityGraph` (declarativo, preferido), `JOIN FETCH` (uma coleção/query — o cartesian product com 2+), `@BatchSize`, DTO projection", "O cuidado `JOIN FETCH` + paginação (`HHH000104` — pagina em memória; use DTO/subquery)". `## Na prática`: o loop que causa N+1 + as 3 soluções lado a lado (`@EntityGraph`, `JOIN FETCH`, projection) (```java) + config de SQL logging (```yaml). `## Armadilhas` ≥3: N+1 silencioso escondido por OSIV; `JOIN FETCH` de duas coleções (produto cartesiano); paginar com fetch de coleção (`HHH000104`). `## Veja também` — [[07 - Fetch strategies — LAZY, EAGER e a LazyInitializationException]], [[10 - Projections e DTOs — não vazar a entidade]], [[11 - Paginação e ordenação — Pageable, Page e Slice]], verbetes `N+1 (problema)`/`@EntityGraph`/`@BatchSize`. (Sem estatística de adoção inventada.)

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; `grep -i "HHH000104\|EntityGraph"` ≥1; anti-fabricação VAZIO.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 10 nota 08 — o problema N+1 e suas soluções"`

### Task 9: Nota 09 — Consultas com @Query — JPQL, native e @Modifying

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Persistência de dados/09 - Consultas com @Query — JPQL, native e @Modifying.md`

- [ ] **Step 1: Pesquisar** — WebFetch `https://docs.spring.io/spring-data/jpa/reference/jpa/query-methods.html`. CONFIRMAR: `@Query` JPQL vs `nativeQuery = true`; `@Param`; `@Modifying` (UPDATE/DELETE em massa, `clearAutomatically`/`flushAutomatically`). Refinar do tronco `### @Query — JPQL e native` + `### Modifying queries`, higienizando.

- [ ] **Step 2: Escrever** — `fase: adepto`, tags `[java, persistencia, adepto, spring-data, jpql]`. ≥3 H3s: "JPQL: consulta entidades/atributos, não tabelas/colunas", "SQL nativo (`nativeQuery = true`): quando o JPQL não basta", "`@Modifying`: UPDATE/DELETE em massa (e o `clearAutomatically`/`flushAutomatically` que invalida o L1)". `## Na prática`: `@Query("SELECT o FROM Order o WHERE ...")` + um native + um `@Modifying` UPDATE retornando linhas afetadas (```java). `## Armadilhas` ≥3: `@Modifying` sem limpar o L1 (entidade stale na sessão); misturar JPQL e SQL sem perceber (nome de entidade vs tabela); `LIKE '%x%'` sem índice (full scan). `## Veja também` — [[04 - Spring Data repositories — JpaRepository e query methods derivados]], [[10 - Projections e DTOs — não vazar a entidade]], [[15 - Consultas dinâmicas e os limites da JPA — Specifications, Criteria e SQL]], verbetes `@Query (JPQL/native)`/`@Modifying`.

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; anti-fabricação VAZIO.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 10 nota 09 — consultas com @Query (JPQL, native, @Modifying)"`

### Task 10: Nota 10 — Projections e DTOs — não vazar a entidade

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Persistência de dados/10 - Projections e DTOs — não vazar a entidade.md`

- [ ] **Step 1: Pesquisar** — WebFetch `https://docs.spring.io/spring-data/jpa/reference/repositories/projections.html`. CONFIRMAR: interface projection (proxy), class-based/DTO (`record` via `SELECT new`), dynamic projection (`<T> ...(Class<T>)`). 

- [ ] **Step 2: Escrever** — `fase: adepto`, tags `[java, persistencia, adepto, projection, spring-data]`. ≥3 H3s: "Interface projection (o proxy do Spring; closed vs open)", "Class-based / DTO projection (`record` via `SELECT new com.app.OrderDto(...)`)", "Dynamic projection (`<T> List<T> findBy...(Class<T>)`)", "Quando projection (listagem read-only) vs entidade (modificar)". **Não vazar a entidade na borda** linka **G9 nota 05** (o DTO é o contrato da API). `## Na prática`: a entidade `Order`, uma interface `OrderSummary`, um `record OrderDto` via JPQL `SELECT new` (```java). `## Armadilhas` ≥3: carregar a entidade inteira só pra ler 3 campos; projection com relação lazy (N+1 sutil); expor a entidade direto no JSON (→ borda é DTO, Galho 9). `## Veja também` — [[08 - O problema N+1 e suas soluções — @EntityGraph, JOIN FETCH, batch size]], [[09 - Consultas com @Query — JPQL, native e @Modifying]], **[[03-Dominios/Tecnologia/Java/Web e APIs REST/05 - Serialização JSON com Jackson|Serialização JSON (DTO na borda)]]**, verbete `projection (JPA)`.

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; link Galho 9 nota 05 presente; anti-fabricação VAZIO.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 10 nota 10 — projections e DTOs (não vazar a entidade)"`

### Task 11: Nota 11 — Paginação e ordenação — Pageable, Page e Slice

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Persistência de dados/11 - Paginação e ordenação — Pageable, Page e Slice.md`

- [ ] **Step 1: Pesquisar** — WebFetch `https://docs.spring.io/spring-data/jpa/reference/repositories/core-concepts.html` (paging and sorting). CONFIRMAR: `Pageable`/`PageRequest`; `Page` (count total — query extra) vs `Slice` (só há-próxima, sem count); `Sort`.

- [ ] **Step 2: Escrever** — `fase: adepto`, tags `[java, persistencia, adepto, paginacao, spring-data]`. ≥3 H3s: "`Pageable`/`PageRequest` e `Sort`", "`Page<T>`: traz o total (uma query `count` a mais)", "`Slice<T>`: só sabe se há próxima página (sem count — mais barato)", "O custo do count em tabela grande". `## Na prática`: `Page<OrderDto> findByStatus(Status s, Pageable p)` + `PageRequest.of(0, 20, Sort.by("createdAt").descending())` (```java). `## Armadilhas` ≥3: usar `Page` quando não precisa do total (paga o count à toa — use `Slice`); `Sort` por campo não indexado; offset alto em tabela grande (deep pagination — cursor-based é melhor, → [[API Design]]). `## Veja também` — [[08 - O problema N+1 e suas soluções — @EntityGraph, JOIN FETCH, batch size]], [[04 - Spring Data repositories — JpaRepository e query methods derivados]], [[API Design]] (cursor-based), verbete `Pageable / Page / Slice`.

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; anti-fabricação VAZIO.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 10 nota 11 — paginação e ordenação (Pageable, Page, Slice)"`

---

## Fase MAGUS (notas 12-17)

### Task 12: Nota 12 — Transações operacionais — @Transactional propagação, isolamento, rollback, readOnly ⟦opus⟧

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Persistência de dados/12 - Transações operacionais — @Transactional propagação, isolamento, rollback, readOnly.md`

- [ ] **Step 1: Pesquisar** — WebFetch `https://docs.spring.io/spring-framework/reference/data-access/transaction/declarative.html` (+ `.../transaction/declarative/annotations.html`). CONFIRMAR: propagação (REQUIRED/REQUIRES_NEW/NESTED/MANDATORY/SUPPORTS/NOT_SUPPORTED/NEVER); isolamento; rollback rules (só unchecked + Error por default; `rollbackFor`); `readOnly`; timeout. Refinar a seção `## Gerenciamento de transações` do `Spring Boot.md` (O básico/Propagation/Isolation/Rollback/Read-only/Timeout/Padrão Service), higienizando (`Patient` → `Order`).

- [ ] **Step 2: Escrever** — `fase: magus`, tags `[java, persistencia, magus, transacao]`. **Cobre o COMPORTAMENTO, não o mecanismo.** ≥3 H3s: "Propagação (REQUIRED default; REQUIRES_NEW pra auditoria que commita independente; NESTED/savepoint; MANDATORY/NEVER)", "Isolamento (READ_COMMITTED default PG / REPEATABLE_READ default MySQL / SERIALIZABLE — teoria em [[Banco de dados]])", "Rollback rules (só `RuntimeException`/`Error` por default — checked NÃO faz rollback; `rollbackFor`; `setRollbackOnly`)", "`readOnly` (desabilita dirty checking), timeout, transação na camada Service". **O mecanismo é o proxy AOP** → linka **G8 notas 09/10** (AOP + self-invocation); a demarcação é a **JTA** → linka **G7 nota 11**. `## Na prática`: `@Service @Transactional(readOnly=true)` na classe, método de escrita sobrescrevendo com `@Transactional` + `REQUIRES_NEW` pra auditoria (```java). `## Armadilhas` ≥3: checked exception não faz rollback (default — exemplo + `rollbackFor`); self-invocation (chamada interna não passa pelo proxy — linka G8 nota 10); `@Transactional` em método `private`. `## Veja também` — [[03 - O persistence context e os estados da entidade]], [[13 - Locking — optimistic (@Version) e pessimistic]], **[[03-Dominios/Tecnologia/Java/Spring Core e Boot/09 - AOP e proxies no Spring|AOP e proxies (o mecanismo)]]**, **[[03-Dominios/Tecnologia/Java/Spring Core e Boot/10 - Self-invocation e os limites do proxy|Self-invocation e os limites do proxy]]**, **[[03-Dominios/Tecnologia/Java/Jakarta EE/11 - JTA — transações na plataforma|JTA (a demarcação, na spec)]]**, [[Banco de dados]], verbetes `@Transactional (propagação)`/`propagação de transação`/`isolamento (isolation level)`/`rollback rules`/`readOnly (transação)`.

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; links Galho 8 (AOP 09 + Self-invocation 10) **e** Galho 7 (JTA 11) presentes; **grep `Patient` VAZIO** (higienizado); anti-fabricação VAZIO.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 10 nota 12 — transações operacionais (@Transactional)"`

### Task 13: Nota 13 — Locking — optimistic (@Version) e pessimistic

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Persistência de dados/13 - Locking — optimistic (@Version) e pessimistic.md`

- [ ] **Step 1: Pesquisar** — WebFetch Hibernate User Guide (locking) + `https://jakarta.ee/specifications/persistence/` (LockModeType). CONFIRMAR: `@Version` (optimistic, `OptimisticLockException`); `@Lock(PESSIMISTIC_WRITE)`/`SELECT ... FOR UPDATE`; deadlock e ordem de aquisição. Refinar do tronco `### Optimistic locking — @Version` + `### Pessimistic locking`, higienizando (`Account`/transferência é neutro — pode manter).

- [ ] **Step 2: Escrever** — `fase: magus`, tags `[java, persistencia, magus, locking, transacao]`. ≥3 H3s: "Lost update: o problema que o locking resolve", "Optimistic (`@Version`, `OptimisticLockException`, retry — pra conflito raro)", "Pessimistic (`@Lock(PESSIMISTIC_WRITE)`, `SELECT ... FOR UPDATE`, deadlock e ordem de aquisição — pra conflito frequente)", "Quando cada um". Liga a [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Concorrência]] (conflito de escrita). `## Na prática`: `@Version` numa entidade `Account` + o retry no `OptimisticLockException` + um `findByIdForUpdate` com `@Lock` (```java). `## Armadilhas` ≥3: esquecer `@Version` em entidade editável concorrentemente (lost update silencioso); deadlock por ordem de lock inconsistente (adquira por ordem crescente de id); pessimistic onde optimistic bastava (contenção desnecessária). `## Veja também` — [[12 - Transações operacionais — @Transactional propagação, isolamento, rollback, readOnly]], **[[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Concorrência e paralelismo]]**, [[Banco de dados]], verbetes `@Version (optimistic locking)`/`pessimistic locking`.

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; anti-fabricação VAZIO.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 10 nota 13 — locking (optimistic e pessimistic)"`

### Task 14: Nota 14 — Caching — 1º nível, 2º nível e Spring Cache ⟦opus⟧

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Persistência de dados/14 - Caching — 1º nível, 2º nível e Spring Cache.md`

- [ ] **Step 1: Pesquisar** — WebFetch Hibernate User Guide (caching) + `https://docs.spring.io/spring-framework/reference/integration/cache.html`. CONFIRMAR: L1 (persistence context, por-tx); L2 (`@Cacheable`/`@Cache`, estratégias READ_ONLY/NONSTRICT_READ_WRITE/READ_WRITE/TRANSACTIONAL, region factory); Spring Cache (`@Cacheable`/`@CacheEvict`/`@CachePut`, Caffeine/Redis). Refinar do tronco `## Caching` (1st/2nd level + Spring Cache), higienizando.

- [ ] **Step 2: Escrever** — `fase: magus`, tags `[java, persistencia, magus, cache]`. ≥3 H3s: "1º nível (persistence context — por transação; recapitula a nota 03)", "2º nível (application-wide, `@Cacheable`/`@Cache`, estratégias; quando usar — entidade de referência lida-muito/mudada-pouco; quando NÃO — dinâmico, multi-nó sem cache distribuído)", "Spring Cache (`@Cacheable`/`@CacheEvict`/`@CachePut` na camada Service — a camada acima da JPA)". Distingue os três níveis. `## Na prática`: `@Entity @Cacheable @Cache(usage = READ_WRITE)` numa `Country` de referência + `@Cacheable("countries")` num service (```java) + config (```yaml). `## Armadilhas` ≥3: confundir L1 (por-tx) com L2 (app-wide); L2 em dado volátil (stale reads); `@Cacheable` sem `@CacheEvict` (cache nunca invalida). `## Veja também` — [[03 - O persistence context e os estados da entidade]], [[12 - Transações operacionais — @Transactional propagação, isolamento, rollback, readOnly]], [[System Design]] (estratégias de cache), verbetes `second-level cache (2º nível)`/`@Cacheable / Spring Cache`.

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; anti-fabricação VAZIO.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 10 nota 14 — caching (1º nível, 2º nível, Spring Cache)"`

### Task 15: Nota 15 — Consultas dinâmicas e os limites da JPA — Specifications, Criteria e SQL

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Persistência de dados/15 - Consultas dinâmicas e os limites da JPA — Specifications, Criteria e SQL.md`

- [ ] **Step 1: Pesquisar** — WebFetch `https://docs.spring.io/spring-data/jpa/reference/jpa/specifications.html` + `https://jakarta.ee/specifications/persistence/` (Criteria) + `https://www.jooq.org/` (menção). CONFIRMAR: `JpaSpecificationExecutor`/`Specification`; Criteria API (query programática type-safe da spec); JdbcClient/JdbcTemplate/jOOQ como escape hatch. Refinar do tronco `### Specifications` + `## Quando NÃO usar JPA` + `### jOOQ` + `### JdbcTemplate / JdbcClient`, higienizando.

- [ ] **Step 2: Escrever** — `fase: magus`, tags `[java, persistencia, magus, spring-data, jpql]`. ≥3 H3s: "Specifications: filtros dinâmicos componíveis (`JpaSpecificationExecutor`, `where(...).and(...)`)", "Criteria API: a query programática type-safe da spec JPA (Galho 7) sob as Specifications", "Quando a JPA não basta (analítico, window functions, bulk, reporting)", "O escape hatch: `JdbcClient`/`JdbcTemplate`, jOOQ (type-safe)". Sem dogma — JPA pro domínio transacional, SQL pro analítico. `## Na prática`: `PatientSpecs`→`OrderSpecs` com `hasStatus`/`totalGreaterThan` compostos via `where().and()` + um `JdbcClient` simples (```java). `## Armadilhas` ≥3: forçar JPQL onde SQL/jOOQ era melhor (relatório com window function); Specification ilegível (lógica demais no predicado); achar que JPA serve pra tudo. `## Veja também` — [[09 - Consultas com @Query — JPQL, native e @Modifying]], [[11 - Paginação e ordenação — Pageable, Page e Slice]], **[[03-Dominios/Tecnologia/Java/Jakarta EE/09 - JPA — a especificação de persistência|JPA (a Criteria API é da spec)]]**, [[Banco de dados]], verbetes `Specification (Spring Data)`/`Criteria API`.

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; anti-fabricação VAZIO (sem `Patient`); link Galho 7 presente.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 10 nota 15 — consultas dinâmicas e os limites da JPA"`

### Task 16: Nota 16 — Migrations de schema — Flyway, Liquibase e expand-and-contract

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Persistência de dados/16 - Migrations de schema — Flyway, Liquibase e expand-and-contract.md`

- [ ] **Step 1: Pesquisar (CRÍTICO)** — WebFetch `https://documentation.red-gate.com/fd` (Flyway) + `https://docs.liquibase.com`. CONFIRMAR: Flyway (`V__`/`R__`, SQL versionado) vs Liquibase (changelog XML/YAML/JSON/SQL, rollback declarativo, `databasechangelog`); versões/integração atuais com Spring Boot; regras de ouro. **Version-specific (WebFetch obrigatório; sem estatística de adoção inventada).** Refinar do tronco `## Flyway: migrations seguras` (estrutura, regras de ouro, expand-and-contract), higienizando.

- [ ] **Step 2: Escrever** — `fase: magus`, tags `[java, persistencia, magus, migrations]`. ≥3 H3s: "Por que versionar o schema (não confiar no `ddl-auto=update` em produção)", "Flyway (`V__`/`R__`, SQL puro) vs Liquibase (changelog declarativo, rollback) — quando cada", "Regras de ouro (nunca editar migration aplicada, roll-forward, baseline)", "Expand-and-contract: mudança em tabela grande sem downtime (add nullable → backfill → not null, deploy sequencial); índice `CONCURRENTLY`". `## Na prática`: estrutura `db/migration/V1__...sql` (Flyway) + o trio expand/backfill/contract (```sql) + config (```yaml). `## Armadilhas` ≥3: `ddl-auto=update` em produção (drift de schema); editar migration já aplicada (checksum quebra); `ALTER TABLE ADD COLUMN NOT NULL` travando tabela grande (use expand-and-contract). `## Veja também` — [[02 - A entidade JPA — @Entity, @Id e geração de chave]], [[Banco de dados]], [[API Design]] (evolução com deprecation), verbetes `Flyway`/`Liquibase`/`expand-and-contract`.

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; `grep -i "flyway\|liquibase"` ≥2; anti-fabricação VAZIO; sem estatística inventada (revisar manualmente).

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 10 nota 16 — migrations de schema (Flyway, Liquibase, expand-and-contract)"`

### Task 17: Nota 17 — Capstone — Uma query do repositório ao banco, sem cair no N+1 ⟦opus⟧

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Persistência de dados/17 - Capstone — Uma query do repositório ao banco, sem cair no N+1.md`

- [ ] **Step 1: Pesquisar** — WebFetch `https://docs.spring.io/spring-data/jpa/reference/` (revisão) + Hibernate User Guide (revisão). Conferir a tabela "Galho 10 → spec Jakarta" com as notas dos Galhos 7/8 já escritas.

- [ ] **Step 2: Escrever** — `fase: magus`, tags `[java, persistencia, magus, spring-data, jpa]`, aliases `["Capstone Persistência", "Query do repositório ao banco"]`. **Híbrido: trace + checklist de design.** Conteúdo:
  - TL;DR: uma query atravessa repo (proxy Spring Data) → JPQL/Criteria → Hibernate monta o SQL → persistence context → JDBC → `ResultSet` → entidades managed → DTO; projetar a camada é dominar esse caminho sem cair no N+1.
  - `## O que é` / `## Por que importa`.
  - `## Como funciona` — H3s: "**Trace:** `repo.findAll(spec, pageable)` da chamada ao banco e de volta (diagrama ```text: proxy → JPQL/Criteria → SQL → persistence context → JDBC → ResultSet → entidades managed → DTO)", "O caminho transacional (proxy AOP abre tx → dirty checking → commit)", "**Galho 10 → spec Jakarta (Galho 7)** (tabela: `@Entity`↔JPA, persistence context↔EntityManager, `@Transactional`↔JTA + proxy AOP do Galho 8)".
  - `## Na prática` — `### Checklist de design production-grade` (sempre LAZY; fetch explícito sem N+1; DTO não-entidade na borda; `readOnly` default no Service; `@Version` onde há concorrência; migration expand-and-contract; OSIV desabilitado).
  - `## Armadilhas` (de raciocínio) ≥3: "o repositório vai direto no banco" (há a engrenagem toda no meio); "JPA resolve tudo" (escape hatch — nota 15); "EAGER é mais simples" (N+1).
  - `## Em entrevista` (munição: a pilha, o N+1, transações) + `### Cheatsheet` (nota→problema) + `## Veja também` (notas-chave do galho + **[[03-Dominios/Tecnologia/Java/Jakarta EE/09 - JPA — a especificação de persistência|JPA]]** + **[[03-Dominios/Tecnologia/Java/Jakarta EE/11 - JTA — transações na plataforma|JTA]]** + **[[03-Dominios/Tecnologia/Java/Spring Core e Boot/09 - AOP e proxies no Spring|AOP e proxies]]** + MOC galho/central) + `## Referências`.

- [ ] **Step 3: Verificar** — ≥7 seções; tabela "Galho 10 → spec Jakarta" presente (`grep -iE "JPA|EntityManager|JTA"`); links Galho 7 + Galho 8 presentes; anti-fabricação VAZIO; sem estatística inventada (revisar manualmente).

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 10 nota 17 — capstone (uma query do repositório ao banco)"`

---

## Task 18: MOC do galho

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Persistência de dados/index.md`

- [ ] **Step 1: Escrever** — modelar pelo `03-Dominios/Tecnologia/Java/Web e APIs REST/index.md`. Frontmatter: `type: moc`, `status: growing`, `publish: true`, `title: "Persistência de dados"`, tags `[java, persistencia, moc]`, aliases `["Persistência de dados", "JPA", "Hibernate", "Spring Data JPA", "Galho 10 - Persistência"]`, `created`/`updated: 2026-06-09`. Conteúdo:
  - TL;DR — Galho 10; a camada de dados sobre a spec JPA do Galho 7: entidades e o persistence context, mapeamento de relacionamentos, fetch e o N+1, Spring Data repositories e consultas, paginação, transações operacionais, locking, caching e migrations; 17 notas em 3 fases.
  - `## Sobre este galho` — escopo + audiência + **galho híbrido** (poda integral do tronco `Spring Data JPA.md` + poda cirúrgica da seção de transações do `Spring Boot.md` + pesquisa pras partes version-specific) + **tripla fronteira** (operacionaliza specs do Galho 7; usa o mecanismo AOP do `@Transactional` do Galho 8; alimenta a borda do Galho 9; Galhos 11/12/13/16 planejados, texto).
  - `## Iniciado` (01-05) / `## Adepto` (06-11) / `## Magus` (12-17) — wikilinks + 1 linha cada.
  - `## Rotas alternativas` — 5: **Completa** (01→17); **Entrevista internacional** (01→03→05→07→08→12→17); **Caçando o N+1** (05→07→08→10→17); **Projetando a camada de persistência** (02→05→07→10→11→12→16); **Persistência sobre Jakarta EE** (01→03→12 + Galho 7).
  - `## Todas as notas` — Dataview (`FROM "03-Dominios/Tecnologia/Java/Persistência de dados"`, `WHERE type = "concept"`).
  - `## Veja também` — MOC central, **[[03-Dominios/Tecnologia/Java/Jakarta EE/index|Jakarta EE]]** (as specs), **[[03-Dominios/Tecnologia/Java/Spring Core e Boot/index|Spring Core e Boot]]** (o mecanismo AOP), **[[03-Dominios/Tecnologia/Java/Web e APIs REST/index|Web e APIs REST]]** (a borda), [[Banco de dados]] (teoria SQL/ACID), Dicionário; Galhos 11/12/13/16 como texto "(planejado)" SEM wikilink.

- [ ] **Step 2: Verificar**
```bash
grep -cE "^## (Iniciado|Adepto|Magus|Rotas alternativas)" "03-Dominios/Tecnologia/Java/Persistência de dados/index.md"
grep -c "\[\[" "03-Dominios/Tecnologia/Java/Persistência de dados/index.md"
grep -E "\[\[[^]]*(Galho (11|12|13|16))" "03-Dominios/Tecnologia/Java/Persistência de dados/index.md"
```
Expected: 4 headings; ≥17 wikilinks; **último grep VAZIO**.

- [ ] **Step 3: Commit** — `git add "<path>"` && `git commit -m "feat(java): galho 10 MOC — Persistência de dados"`

---

## Task 19: Expandir o Dicionário de Java (NÃO recriar)

**Files:**
- Modify: `03-Dominios/Tecnologia/Java/Dicionário de Java.md`

- [ ] **Step 1: Extrair as âncoras realmente usadas pelas notas**
```bash
grep -rhoE "Dicionário de Java#[^]|]+" "03-Dominios/Tecnologia/Java/Persistência de dados/" | sort -u
```
A fonte da verdade é o que as notas usaram. Lista esperada (~30): `@BatchSize`, `@Cacheable / Spring Cache`, `@EntityGraph`, `@GeneratedValue`, `@ManyToMany`, `@ManyToOne / @OneToMany`, `@Modifying`, `@OneToOne`, `@Query (JPQL/native)`, `@Transactional (propagação)`, `@Version (optimistic locking)`, `cascade / orphanRemoval`, `Criteria API`, `derived query method`, `dirty checking`, `expand-and-contract`, `fetch strategy (LAZY/EAGER)`, `Flyway`, `Hibernate`, `isolamento (isolation level)`, `JpaRepository`, `LazyInitializationException`, `Liquibase`, `N+1 (problema)`, `Open Session In View (OSIV)`, `owning side / inverse side`, `Pageable / Page / Slice`, `pessimistic locking`, `persistence context (1º nível)`, `projection (JPA)`, `propagação de transação`, `readOnly (transação)`, `rollback rules`, `Specification (Spring Data)`, `Spring Data JPA`, `second-level cache (2º nível)`.

- [ ] **Step 2: Ler o Dicionário e conferir duplicatas** — formato `### Termo` + 1-3 linhas + `Veja também:`. **NÃO recriar/reordenar.** **Conferir verbetes já existentes (Galhos 7/8) pra NÃO duplicar** e **linkar entre si**: `persistence context (1º nível)` ↔ `persistence context` (conceito, Galho 7); `@Transactional (propagação)` ↔ `@Transactional` (Galho 8 e/ou Jakarta, Galho 7); `dirty checking` (se já existir do Galho 7) — **não duplicar, complementar/linkar**; `Hibernate`/`JPA`/`EntityManager`/`JTA`/`JPQL`/`owning side` (Galho 7). Conferir com:
```bash
grep -nE "^### (JPA|EntityManager|JTA|JPQL|persistence context|dirty checking|owning side|@Transactional|Hibernate|entidade)" "03-Dominios/Tecnologia/Java/Dicionário de Java.md"
```

- [ ] **Step 3: Inserir em ordem alfabética** (case-insensitive, sem acento; verbetes iniciados em `@` entram na seção da letra seguinte — conferir o padrão do arquivo). Cada verbete: heading EXATO da âncora + definição fiel às notas + `Veja também:` pra nota canônica (Spring Data JPA/Hibernate→01; `@GeneratedValue`→02; persistence context/dirty checking→03; JpaRepository/derived query→04; `@ManyToOne / @OneToMany`/owning side→05; `@ManyToMany`/`@OneToOne`/cascade→06; fetch strategy/LazyInitializationException/OSIV→07; N+1/`@EntityGraph`/`@BatchSize`→08; `@Query`/`@Modifying`→09; projection→10; `Pageable / Page / Slice`→11; `@Transactional`/propagação/isolamento/rollback/readOnly→12; `@Version`/pessimistic locking→13; second-level cache/`@Cacheable`→14; Specification/Criteria API→15; Flyway/Liquibase/expand-and-contract→16). Atualizar `updated: 2026-06-09`.

- [ ] **Step 4: Verificar**
```bash
grep -E "^### (Spring Data JPA|N\+1|@EntityGraph|Flyway|persistence context|@Transactional)" "03-Dominios/Tecnologia/Java/Dicionário de Java.md"
grep -cE "^### " "03-Dominios/Tecnologia/Java/Dicionário de Java.md"
```
Expected: novos presentes; contagem subiu ~30 vs baseline (272 → ~300).

- [ ] **Step 5: Commit** — `git add "<path>"` && `git commit -m "feat(java): expande Dicionário de Java com verbetes do galho 10 (Persistência de dados)"`

---

## Task 20: Ativar o Galho 10 no MOC central

**Files:**
- Modify: `03-Dominios/Tecnologia/Java/index.md`

- [ ] **Step 1: Trocar a linha do item 10** (localizar por conteúdo: `10. Persistência de dados *(planejado)* — JPA/Hibernate, Spring Data, fetch/N+1, transações, migrations`) por:
```markdown
10. [[03-Dominios/Tecnologia/Java/Persistência de dados/index|Persistência de dados]] — JPA/Hibernate, o persistence context, mapeamento e relacionamentos, fetch strategies e o N+1, Spring Data repositories e consultas, paginação, transações operacionais, locking, caching e migrations
```
Atualizar `updated: 2026-06-09`. Não mexer no resto.

- [ ] **Step 2: Verificar**
```bash
grep -E "Persistência de dados/index" "03-Dominios/Tecnologia/Java/index.md"
grep -c "planejado" "03-Dominios/Tecnologia/Java/index.md"
```
Expected: wikilink ativo; "planejado" caiu exatamente 1 vs baseline.

- [ ] **Step 3: Commit** — `git add "<path>"` && `git commit -m "feat(java): ativa Galho 10 (Persistência de dados) no MOC central"`

---

## Task 21: Poda INTEGRAL do tronco (`Backend/Spring Data JPA.md`)

**Files:**
- Modify: `03-Dominios/Tecnologia/Java/Backend/Spring Data JPA.md`

- [ ] **Step 1: Ler o tronco e confirmar que o conteúdo bom já migrou pras notas** (política §9 do roadmap — ler antes de podar). Conferir que entidade/relacionamentos/fetch/N+1/repositories/queries/projections/transações/locking/caching/migrations já estão cobertos nas notas 01-17. **Só podar depois das 17 notas existirem.**

- [ ] **Step 2: Podar INTEGRAL** — substituir TODO o corpo (da linha após o frontmatter até o fim) por um hub enxuto (padrão JavaFX/Galho 6). Manter o frontmatter com `publish: false` e `updated: 2026-06-09`. Corpo novo:
```markdown
# Spring Data JPA

Persistência na stack Spring — JPA/Hibernate, Spring Data repositories, mapeamento e relacionamentos, fetch strategies, o problema N+1, transações, caching e migrations.

> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Tecnologia/Java/Persistência de dados/index|Persistência de dados]]. Veja [[03-Dominios/Tecnologia/Java/Persistência de dados/01 - O que é a camada de persistência — Spring Data, JPA e Hibernate|O que é a camada de persistência]], [[03-Dominios/Tecnologia/Java/Persistência de dados/03 - O persistence context e os estados da entidade|O persistence context e os estados da entidade]], [[03-Dominios/Tecnologia/Java/Persistência de dados/05 - Relacionamentos — @ManyToOne, @OneToMany e o owning side|Relacionamentos]], [[03-Dominios/Tecnologia/Java/Persistência de dados/08 - O problema N+1 e suas soluções — @EntityGraph, JOIN FETCH, batch size|O problema N+1]], [[03-Dominios/Tecnologia/Java/Persistência de dados/12 - Transações operacionais — @Transactional propagação, isolamento, rollback, readOnly|Transações operacionais]] e [[03-Dominios/Tecnologia/Java/Persistência de dados/16 - Migrations de schema — Flyway, Liquibase e expand-and-contract|Migrations de schema]].

## Veja também

- [[03-Dominios/Tecnologia/Java/Persistência de dados/index|Persistência de dados (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[Banco de dados]]
```
**Toda a fabricação some** (`Patient`/`Doctor`/`Appointment`, `## Na prática (da minha experiência)`, `## How to explain in English`, "incidente memorável" do MedEspecialista).

- [ ] **Step 3: Verificar (poda integral — fabricação evaporada, hub presente)**
```bash
wc -l "03-Dominios/Tecnologia/Java/Backend/Spring Data JPA.md"
grep -niE "Patient|Doctor|Appointment|MedEspecialista|minha experiência|incidente" "03-Dominios/Tecnologia/Java/Backend/Spring Data JPA.md"
grep -c "Migrado para galho próprio" "03-Dominios/Tecnologia/Java/Backend/Spring Data JPA.md"
grep -E "^publish:" "03-Dominios/Tecnologia/Java/Backend/Spring Data JPA.md"
```
Expected: arquivo ~20-25 linhas; **segundo grep VAZIO** (fabricação some); 1 callout "Migrado"; `publish: false` mantido.

- [ ] **Step 4: Commit** — `git add "03-Dominios/Tecnologia/Java/Backend/Spring Data JPA.md"` && `git commit -m "refactor(java): poda integral do tronco Spring Data JPA — vira hub do galho 10"`

---

## Task 22: Poda CIRÚRGICA do tronco (`Backend/Spring Boot.md`) — só a seção de transações

**Files:**
- Modify: `03-Dominios/Tecnologia/Java/Backend/Spring Boot.md`

- [ ] **Step 1: Ler o tronco e confirmar o range** (política §9 — ler antes de podar)
```bash
grep -nE "^#{2,3} " "03-Dominios/Tecnologia/Java/Backend/Spring Boot.md"
```
Confirmar os limites reais de `## Gerenciamento de transações — @Transactional deep dive` (início ~67, fim = imediatamente antes da próxima `## ` — provavelmente `## Spring MVC pipeline` callout; **conferir na execução**). **Só esta seção é podada.**

- [ ] **Step 2: Podar `## Gerenciamento de transações`** — substituir TODO o bloco da seção (do heading até imediatamente antes da próxima `## `) por:
```markdown
## Gerenciamento de transações — @Transactional deep dive

> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Tecnologia/Java/Persistência de dados/index|Persistência de dados]]. Veja [[03-Dominios/Tecnologia/Java/Persistência de dados/12 - Transações operacionais — @Transactional propagação, isolamento, rollback, readOnly|Transações operacionais (@Transactional)]] e [[03-Dominios/Tecnologia/Java/Persistência de dados/13 - Locking — optimistic (@Version) e pessimistic|Locking]]. O mecanismo (proxy AOP, self-invocation) é do galho [[03-Dominios/Tecnologia/Java/Spring Core e Boot/index|Spring Core e Boot]].
```
A contaminação `Patient` (~175) **some** com a substituição (não copiar pras notas).

- [ ] **Step 3: Atualizar `## Veja também` + frontmatter** — adicionar wikilink `[[03-Dominios/Tecnologia/Java/Persistência de dados/index|Persistência de dados]]` no "Veja também" do tronco (se já não houver); `updated: 2026-06-09`.

- [ ] **Step 4: Verificar (poda cirúrgica — uma seção só; resto intacto)**
```bash
grep -nE "^## " "03-Dominios/Tecnologia/Java/Backend/Spring Boot.md"
grep -c "Persistência de dados/index" "03-Dominios/Tecnologia/Java/Backend/Spring Boot.md"
grep -nE "Propagation|Isolation levels|Rollback rules" "03-Dominios/Tecnologia/Java/Backend/Spring Boot.md"
grep -nE "^## (Spring MVC pipeline|Spring WebFlux|Spring Cloud|Camadas típicas)" "03-Dominios/Tecnologia/Java/Backend/Spring Boot.md"
grep -nE "^### (Persistência|Bean Validation)" "03-Dominios/Tecnologia/Java/Backend/Spring Boot.md"
```
Expected: o `## Gerenciamento de transações` agora é só callout (segundo grep ≥1 link); subseções de transação (`Propagation`/`Isolation`/`Rollback`) **sumiram** (terceiro grep VAZIO); callouts dos Galhos 8/9 (`## Spring MVC pipeline`) e seções de outros galhos (WebFlux/Cloud/Camadas típicas) **AINDA PRESENTES**; `### Persistência`/`### Bean Validation` sob Camadas típicas **intactos** (último grep ≥2).

- [ ] **Step 5: Commit** — `git add "03-Dominios/Tecnologia/Java/Backend/Spring Boot.md"` && `git commit -m "refactor(java): poda cirúrgica do tronco Spring Boot — seção de transações migra pro galho 10"`

---

## Task 23: Quitar a dívida reversa (11 ponteiros inline + 3 parágrafos → wikilinks)

**Files:**
- Modify: `03-Dominios/Tecnologia/Java/Jakarta EE/09 - JPA — a especificação de persistência.md`
- Modify: `03-Dominios/Tecnologia/Java/Jakarta EE/10 - EntityManager e o ciclo de vida da entidade.md`
- Modify: `03-Dominios/Tecnologia/Java/Jakarta EE/11 - JTA — transações na plataforma.md`
- Modify: `03-Dominios/Tecnologia/Java/Jakarta EE/index.md`
- Modify: `03-Dominios/Tecnologia/Java/Spring Core e Boot/index.md`
- Modify: `03-Dominios/Tecnologia/Java/Web e APIs REST/05 - Serialização JSON com Jackson.md`
- Modify: `03-Dominios/Tecnologia/Java/Web e APIs REST/08 - Validação na borda.md`
- Modify: `03-Dominios/Tecnologia/Java/Web e APIs REST/index.md`
- (O `Backend/Spring Boot.md:63` já foi quitado na Task 22 — o callout AOP "fica para o Galho 10... na seção de transações abaixo" deve ser ajustado lá; ver Step 2.)

- [ ] **Step 1: Relocalizar (por conteúdo — linhas podem ter mudado)**
```bash
grep -rn "Galho 10\|galho 10\|planejado" "03-Dominios/Tecnologia/Java/Jakarta EE/09 - JPA — a especificação de persistência.md" "03-Dominios/Tecnologia/Java/Jakarta EE/10 - EntityManager e o ciclo de vida da entidade.md" "03-Dominios/Tecnologia/Java/Jakarta EE/11 - JTA — transações na plataforma.md" "03-Dominios/Tecnologia/Java/Jakarta EE/index.md" "03-Dominios/Tecnologia/Java/Spring Core e Boot/index.md" "03-Dominios/Tecnologia/Java/Web e APIs REST/05 - Serialização JSON com Jackson.md" "03-Dominios/Tecnologia/Java/Web e APIs REST/08 - Validação na borda.md" "03-Dominios/Tecnologia/Java/Web e APIs REST/index.md"
```

- [ ] **Step 2: Aplicar os wikilinks** — em cada ponteiro, trocar o texto "Galho 10 (planejado)"/"Galho 10, planejado" pelo wikilink, **mantendo natural a frase** e atualizando `updated: 2026-06-09` no frontmatter de cada arquivo tocado:
  - **Jakarta EE/09 - JPA (~57):** "...O Galho 10 (planejado) constrói em cima..." → "...[[03-Dominios/Tecnologia/Java/Persistência de dados/01 - O que é a camada de persistência — Spring Data, JPA e Hibernate|o Galho 10]] constrói em cima..."
  - **Jakarta EE/09 - JPA (~152):** tabela "Tudo que vai além do default — Galho 10 (planejado)" → "...[[03-Dominios/Tecnologia/Java/Persistência de dados/07 - Fetch strategies — LAZY, EAGER e a LazyInitializationException|Galho 10]]"
  - **Jakarta EE/09 - JPA (~333):** comentário HTML "além do contrato é assunto do Galho 10 (planejado)." → wikilink pra nota 07 (ou MOC); **se estiver em comentário HTML `<!-- -->`, manter o comentário** mas trocar o texto pelo wikilink.
  - **Jakarta EE/10 - EntityManager (~160):** "...**Como** o provider detecta as mudanças ... território do Galho 10 (planejado)." → "...território do [[03-Dominios/Tecnologia/Java/Persistência de dados/03 - O persistence context e os estados da entidade|Galho 10]]."
  - **Jakarta EE/10 - EntityManager (~331):** "As estratégias concretas de carregamento ... Galho 10 (planejado)..." → "...são assunto do [[03-Dominios/Tecnologia/Java/Persistência de dados/07 - Fetch strategies — LAZY, EAGER e a LazyInitializationException|Galho 10]]..."
  - **Jakarta EE/11 - JTA (~35):** "O `@Transactional` do Spring é assunto dos Galhos 8/10 (planejado)..." → "...dos Galhos [[03-Dominios/Tecnologia/Java/Spring Core e Boot/09 - AOP e proxies no Spring|8 (o mecanismo AOP)]] e [[03-Dominios/Tecnologia/Java/Persistência de dados/12 - Transações operacionais — @Transactional propagação, isolamento, rollback, readOnly|10 (o comportamento)]]..." (Galho 8 já existe — quitar os dois.)
  - **Jakarta EE/index (~30):** "...JPA operacional (Hibernate, fetch/N+1, caching, Spring Data, migrations) é do Galho 10 (planejado)..." → "...é do galho [[03-Dominios/Tecnologia/Java/Persistência de dados/index|Persistência de dados]]..."
  - **Spring Core e Boot/index (~32, parágrafo de fronteira):** "...Persistência/transações operacionais com Spring Data, Hibernate, fetch/N+1 e migrations (Galho 10) são planejados..." → "...com Spring Data, Hibernate, fetch/N+1 e migrations é o galho [[03-Dominios/Tecnologia/Java/Persistência de dados/index|Persistência de dados]]..." **NÃO tocar o horizonte-list :97** (deixar 11/12/13/16 como planejados lá).
  - **Web e APIs REST/05 - Serialização JSON (~133):** "...A camada de persistência ... (Galho 10 da trilha Java — persistência com JPA/Hibernate, planejado)." → "...(o galho [[03-Dominios/Tecnologia/Java/Persistência de dados/10 - Projections e DTOs — não vazar a entidade|Persistência de dados]])."
  - **Web e APIs REST/05 - Serialização JSON (~378, Veja também):** "Persistência JPA/Hibernate ... → Galho 10 (planejado)." → wikilink pra `[[03-Dominios/Tecnologia/Java/Persistência de dados/index|Persistência de dados]]` (ou nota 01).
  - **Web e APIs REST/08 - Validação na borda (~236):** "...regras de negócio ... pertencem à camada de serviço (Galho 10 — planejado)." → "...pertencem à camada de serviço (ver o galho [[03-Dominios/Tecnologia/Java/Persistência de dados/12 - Transações operacionais — @Transactional propagação, isolamento, rollback, readOnly|Persistência de dados]])."
  - **Web e APIs REST/index (~32, parágrafo de fronteira):** "...Persistência/Spring Data (Galho 10) ... são planejados..." → "...Persistência/Spring Data é o galho [[03-Dominios/Tecnologia/Java/Persistência de dados/index|Persistência de dados]]..." **NÃO tocar o horizonte-list :95.**

- [ ] **Step 3: Verificar**
```bash
grep -rn "Galho 10\|galho 10" "03-Dominios/Tecnologia/Java/Jakarta EE/09 - JPA — a especificação de persistência.md" "03-Dominios/Tecnologia/Java/Jakarta EE/10 - EntityManager e o ciclo de vida da entidade.md" "03-Dominios/Tecnologia/Java/Jakarta EE/11 - JTA — transações na plataforma.md" "03-Dominios/Tecnologia/Java/Jakarta EE/index.md" "03-Dominios/Tecnologia/Java/Spring Core e Boot/index.md" "03-Dominios/Tecnologia/Java/Web e APIs REST/05 - Serialização JSON com Jackson.md" "03-Dominios/Tecnologia/Java/Web e APIs REST/08 - Validação na borda.md" "03-Dominios/Tecnologia/Java/Web e APIs REST/index.md" | grep -v "Persistência de dados" | grep -vE ":(95|97):" | grep -iE "planejado|10 \(plan"
```
Expected: **VAZIO** (nenhum "Galho 10 (planejado)" solto sobra fora dos horizonte-lists :95/:97; os "Galho 10" remanescentes devem vir acompanhados do wikilink "Persistência de dados"). Conferir manualmente que os horizonte-lists (Spring Core :97, Web :95) **permanecem** com 11/12/13/16 como "(planejado)".

- [ ] **Step 4: Commit** — `git add` nominal dos 8 arquivos && `git commit -m "refactor(java): quita dívida reversa do galho 10 — ponteiros de persistência viram wikilinks"`

---

## Task 24: Verificação final do galho

**Files:** (somente leitura/verificação)

- [ ] **Step 1: 17 notas + MOC**
```bash
ls "03-Dominios/Tecnologia/Java/Persistência de dados/" | sort
```
Expected: 01..17 + index.md (18 arquivos).

- [ ] **Step 2: Fases (5/6/6)**
```bash
for f in "03-Dominios/Tecnologia/Java/Persistência de dados/"[0-9]*.md; do grep -H "^fase:" "$f"; done
```
Expected: 01-05 `iniciado`, 06-11 `adepto`, 12-17 `magus`.

- [ ] **Step 3: Seções obrigatórias (3 por nota)**
```bash
for f in "03-Dominios/Tecnologia/Java/Persistência de dados/"[0-9]*.md; do echo "$f: $(grep -cE '^## (Em entrevista|Armadilhas|Veja também)' "$f")"; done
```
Expected: 3 em todas.

- [ ] **Step 4: Anti-fabricação + fronteiras (greps decisivos)**
```bash
grep -riE "minha experiência|no meu projeto|josenaldo|Patient|Doctor|Appointment|MedEspecialista|market share|% d[ao]s (dev|empresas|projetos)" "03-Dominios/Tecnologia/Java/Persistência de dados/"
grep -rE "\[\[[^]]*(Galho (11|12|13|16)|WebFlux|R2DBC|Spring Security|@DataJpaTest|Testcontainers|saga|CQRS|sharding)" "03-Dominios/Tecnologia/Java/Persistência de dados/"
grep -rn '\[\[#' "03-Dominios/Tecnologia/Java/Persistência de dados/"
```
Expected: **todos VAZIOS**.

- [ ] **Step 5: Tripla fronteira-assinatura (links de volta aos Galhos 7, 8 e 9 presentes)**
```bash
grep -rl "Jakarta EE/(09|10|11)" "03-Dominios/Tecnologia/Java/Persistência de dados/" | sort
grep -rl "Spring Core e Boot/(09|10)" "03-Dominios/Tecnologia/Java/Persistência de dados/" | sort
grep -rl "Web e APIs REST/05" "03-Dominios/Tecnologia/Java/Persistência de dados/" | sort
```
Expected: notas 01/02/03/05/15/17 linkam pra alguma nota do Galho 7 (JPA/EntityManager/JTA); notas 01/04/12 linkam pro Galho 8 (AOP/self-invocation); notas 07/10 linkam pro Galho 9 (Serialização JSON).

- [ ] **Step 6: Frase pronta (1 por nota)**
```bash
for f in "03-Dominios/Tecnologia/Java/Persistência de dados/"[0-9]*.md; do echo "$f: $(grep -c '### Frase pronta (inglês)' "$f")"; done
```
Expected: 1 em todas.

- [ ] **Step 7: Troncos — poda confirmada (integral + cirúrgica)**
```bash
wc -l "03-Dominios/Tecnologia/Java/Backend/Spring Data JPA.md"
grep -c "Migrado para galho próprio" "03-Dominios/Tecnologia/Java/Backend/Spring Data JPA.md"
grep -niE "Patient|Doctor|MedEspecialista" "03-Dominios/Tecnologia/Java/Backend/Spring Data JPA.md"
grep -c "Migrado para galho próprio" "03-Dominios/Tecnologia/Java/Backend/Spring Boot.md"
grep -nE "^## (Gerenciamento de transações|Spring MVC pipeline|Spring WebFlux)" "03-Dominios/Tecnologia/Java/Backend/Spring Boot.md"
git status --short "03-Dominios/Tecnologia/Java/Backend/Spring Security.md" "03-Dominios/Tecnologia/Java/Backend/Kafka/"
```
Expected: `Spring Data JPA.md` ~20-25 linhas, 1 callout "Migrado", **fabricação VAZIA**; `Spring Boot.md` com ≥7 callouts "Migrado" (5 Galho 8 + 1 Galho 9 + 1 novo de transações), `## Gerenciamento de transações`/`## Spring MVC pipeline`/WebFlux presentes (callouts/intocados); `Spring Security.md`/`Kafka/` **sem modificação**.

- [ ] **Step 8: Skill `verificar-wikilinks`** — rodar na pasta `03-Dominios/Tecnologia/Java/Persistência de dados/` + conferir os arquivos tocados fora (MOC central, Dicionário, os dois troncos, os 3 arquivos Jakarta EE + 1 Spring Core index + 3 Web da dívida reversa). Âncoras `Dicionário de Java#...` resolvem 1:1 (cross-check com o grep da Task 19 Step 1). As ~204 quebras legadas da árvore Java NÃO são deste galho — só corrigir o que este galho introduziu. Corrigir e commitar à parte se houver.

- [ ] **Step 9: Resumo de fechamento (sem commit)** — reportar: 17 notas (5/6/6), ~30 verbetes (272→~300), MOC galho + MOC central, **poda dos dois troncos** (integral do `Spring Data JPA.md` — fabricação do MedEspecialista evaporada; cirúrgica da seção de transações do `Spring Boot.md`), **dívida reversa quitada** (11 ponteiros inline + 3 parágrafos; horizonte-lists e galhos 11-16 preservados como "(planejado)"), troncos vizinhos intocados (mostrar o grep), wikilinks limpos. Commits locais na `main`; **push manual do usuário; sem deploy**. Atualizar memória [[project_trilha_java]] com Galho 10 completo + fatos cravados via WebFetch (versão Hibernate ORM/Spring Data, UUID JPA 3.1, Flyway vs Liquibase, baseline 3.x/6.x).

---

## Self-Review (preenchido na escrita do plano)

**Spec coverage:** Tasks 1-17 ↔ spec §3.1 (17 notas, escopos idênticos, opus 01/08/12/14/17, distribuição 5/6/6); Task 18 ↔ §3.2 (MOC, 5 rotas iguais); Task 19 ↔ §3.3 (~30 verbetes, âncoras 1:1 por grep, dups conferidos/linkados com Galhos 7/8); Task 20 ↔ §3.4 (linha 40); Task 21 ↔ §3.5.1 (poda integral `Spring Data JPA.md` → hub, fabricação evaporada, `publish: false` mantido); Task 22 ↔ §3.5.2 (poda cirúrgica — só `## Gerenciamento de transações`; `### Persistência`/`### Bean Validation` sob Camadas típicas intactos; callouts dos Galhos 8/9 intocados); Task 23 ↔ §3.6 (11 ponteiros inline + 3 parágrafos, mapeamento idêntico, horizonte-lists :95/:97 preservados, galhos 11-16 como texto); Task 0 ↔ §6 (pré-flight, baseline 272, ranges dos dois troncos); Task 24 ↔ §7. Tripla fronteira-assinatura (§4.3.1) garantida por links obrigatórios pros Galhos 7/8/9 nas Tasks 1/2/3/5/7/10/12/15/17 e pelo grep da Task 24 Step 5; fronteira galhos 11-16 pelo grep da Task 24 Step 4.

**Placeholder scan:** sem TBD/TODO; cada nota tem fonte WebFetch nomeada com URL, frontmatter concreto, H3s, armadilhas mínimas com conteúdo real, tamanho-alvo herdado das convenções. Pontos version-sensitive marcados com "verificar/confirmar" são instruções de verificação WebFetch (parte pesquisa do galho híbrido), não placeholders: versão Hibernate ORM/Spring Data (baseline 6.x), UUID na JPA 3.1, `@Transactional(readOnly)`, Flyway vs Liquibase, baseline Boot 3.x. A confirmação dos ranges/linhas dos troncos e da dívida reversa (Tasks 0/21/22/23) é resolução-na-execução por política §9 do roadmap (ler antes de podar/editar).

**Type/naming consistency:** numeração 01-17 idêntica entre tasks, MOC, Dicionário, dívida reversa, poda e cheatsheet da capstone; distribuição 5/6/6 consistente; opus 01/08/12/14/17 marcadas ⟦opus⟧; filenames com em dash (sem `:`/`/` — nota 12 usa "@Transactional propagação, isolamento, rollback, readOnly" sem dois-pontos; nota 15 usa "Specifications, Criteria e SQL"); mapeamento de link-back Galho 7→nota (09/10/11), Galho 8→nota (09/10), Galho 9→nota (05/08) consistente entre spec §3.1, convenções e Tasks; âncoras do Dicionário extraídas por grep antes de inserir (Task 19) e validadas na Task 24; verbetes adjacentes (`persistence context (1º nível)`↔`persistence context`, `@Transactional (propagação)`↔`@Transactional`) linkados, não duplicados.
