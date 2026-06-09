---
title: "Spec — Galho 7 da trilha Java Senior (Jakarta EE)"
date: 2026-06-07
author: Josenaldo
status: draft
type: spec
publish: false
---

# Spec — Galho 7 da trilha Java Senior (Jakarta EE)

## 1. Contexto e motivação

Este é o **sétimo galho** da trilha Java Senior (roadmap em `docs/superpowers/specs/2026-06-02-java-senior-roadmap-design.md`, §5, bloco "Fundamentos enterprise e Spring"). Pressupõe leitura do roadmap, que estabelece topologia flat, esquema de 3 fases, padrões editoriais e política de poda. Os Galhos 1 (Linguagem), 2 (Collections/Streams), 3 (JVM), 4 (Concorrência), 5 (Swing) e 6 (JavaFX) já fecharam em `main` — seus artefatos são o **template de padrão e qualidade** deste galho.

**Galho de PESQUISA, como o Galho 5 (Swing).** O roadmap confirma: **"Tronco a podar: nenhum (galho novo)."** Não existe `Jakarta EE.md` para refatorar. As notas **nascem de docs oficiais** (`jakarta.ee`, Javadoc Jakarta, eclipse.org) verificadas via WebFetch. Consequências:

- **Sem seção de poda.**
- Pré-flight = confirmar ausência de conteúdo preexistente (feito — §6), localizar dívida reversa (feito — §3.6) e **cravar as versões atuais das specs via jakarta.ee** (feito — §6).
- A matéria-prima é a documentação oficial, não texto pré-existente do autor — atenção redobrada à fabricação (todo exemplo é neutro ou hipotético explícito).

Jakarta EE abre o bloco enterprise da trilha: é **a plataforma que o Spring abstrai**. CDI, Servlet, JAX-RS, Bean Validation, JPA (como especificação), JTA, o legado EJB e a transição Java EE → Jakarta EE. Este galho é o **dono dos conceitos de especificação enterprise** da trilha. Depende dos Galhos 1-2.

**A fronteira mais sensível do galho:** Spring implementa/abstrai essas specs (Galho 8, planejado). As notas citam o Spring como **motivação** ("é isso que o `@Autowired` esconde") **SEM wikilink e SEM explicar o framework**. O Galho 7 explica a SPEC, nunca o framework.

## 2. Objetivo

Produzir, em uma sessão de execução dedicada, **14 notas atômicas + 1 MOC do galho + expansão do Dicionário de Java + ativação do MOC central + quitação da dívida reversa**, em `03-Dominios/Java/Jakarta EE/` e `03-Dominios/Java/`, todas `publish: true`, em PT-BR, distribuídas em 3 fases (4 Iniciado + 6 Adepto + 4 Magus). **Sem poda** (galho novo).

Ao terminar o galho, o leitor deve conseguir:

- **Explicar em inglês** o modelo spec vs implementação da plataforma, a transição Java EE → Jakarta EE (incluindo o rename `javax` → `jakarta` no EE 9 e o porquê), e o papel de cada spec central (CDI, Servlet, JAX-RS, Validation, JPA, JTA).
- **Reconhecer o que o Spring esconde**: dado um `@Autowired`/`@Transactional`/`@Valid`/controller REST, apontar a spec Jakarta correspondente e o mecanismo por baixo (CDI, JTA, Bean Validation, Servlet).
- **Dominar o CDI operacionalmente**: escopos e client proxies, qualifiers, producers, eventos, interceptors — e o ciclo de vida da entidade JPA em nível de spec (persistence context, estados, flush).
- **Decidir e defender honestamente** quando a plataforma Jakarta pura faz sentido vs frameworks, com o estado atual verificado (EE 11, Core Profile, cadência Eclipse) na ponta da língua.

A barra é "explicar a spec, reconhecer o mecanismo por baixo do framework e decidir com critério" — não "administrar um application server".

## 3. Saídas concretas

### 3.1. Notas (`03-Dominios/Java/Jakarta EE/`)

Pasta **nova**, flat. 14 notas + 1 MOC (`index.md`, obrigatório pro folder-link do Quartz). Numeração global por galho (não reinicia por fase).

#### Iniciado (4 notas — vocabulário + modelo mental)

| # | Nota | Escopo nuclear |
|---|------|----------------|
| 01 | O modelo Jakarta EE — especificações e implementações | A ideia central da plataforma: **spec vs implementação** (API jar + impls: Weld, Jersey, Hibernate Validator, EclipseLink); perfis (Platform / Web Profile / Core Profile); app servers vs runtimes (WildFly, Payara, Open Liberty, GlassFish como implementação ratificadora). Porta de entrada — "é esse contrato que o Spring implementa por baixo" (texto, sem explicar Spring). |
| 02 | De Java EE a Jakarta EE | História honesta: J2EE → Java EE 8 → doação à Eclipse Foundation (anunciada em 2017) → Jakarta EE 8 (set/2019, ainda `javax`) → **EE 9 (dez/2020): big-bang rename `javax`→`jakarta`** (e por quê: trademark "Java" é da Oracle) → EE 9.1 (mai/2021) → EE 10 (set/2022) → EE 11 (jun/2025) → EE 12 em desenvolvimento. Impacto prático do rename (migração de imports, ferramentas de bytecode transform, ecossistema partido em dois mundos). **WebFetch pesado.** |
| 03 | Servlet API — o alicerce HTTP | Lifecycle do servlet (`init`/`service`/`destroy`), `HttpServlet`, request/response, sessions/cookies, filters e listeners (panorama), `@WebServlet` vs `web.xml`, servlet containers (Tomcat/Jetty) vs app servers. "É isso que roda embaixo de todo controller" (texto, sem explicar Spring MVC — Galho 9). |
| 04 | CDI — beans e injeção | O básico do coração da plataforma: o que é um bean CDI, `@Inject` (em campo/construtor/método), bean discovery (`beans.xml`, modos `annotated`/`all`), o container e por que inversão de controle. Linka Galho 1 (11 - Annotations) pra mecânica de annotations. "É isso que o `@Autowired` esconde" — motivação, sem explicar Spring. |

#### Adepto (6 notas — domínio operacional; 3 densas → opus)

| # | Nota | Escopo nuclear |
|---|------|----------------|
| 05 | CDI — escopos e contextos *(opus)* | `@ApplicationScoped`/`@RequestScoped`/`@SessionScoped`/`@Dependent`/`@ConversationScoped`; **client proxies** (por que o container injeta proxy, não a instância — e as consequências: chamada self não interceptada, `final` proibido); ciclo de vida (`@PostConstruct`/`@PreDestroy`); lazy instantiation via proxy. |
| 06 | CDI — qualifiers, producers e eventos | `@Qualifier` (resolver ambiguidade de tipo), `@Produces`/`@Disposes` (fabricar o que não é bean: third-party, configuração), eventos (`Event<T>`, `@Observes`, síncrono vs `@ObservesAsync`, transactional observers — menção), `@Alternative`/`@Specializes`, `Instance<T>` (resolução programática). |
| 07 | JAX-RS — REST declarativo | Resources (`@Path`/`@GET`/`@POST`/`@DELETE`...), params (`@PathParam`/`@QueryParam`/`@HeaderParam`...), content negotiation (`@Produces`/`@Consumes` — **homônimos do CDI, desambiguar explicitamente**), providers (`MessageBodyReader/Writer`, `ExceptionMapper`), JSON-B/JSON-P (papel na serialização), Client API. Implementações: Jersey, RESTEasy (citar). Spring MVC/REST → Galho 9 (texto, sem wikilink). |
| 08 | Bean Validation | Constraints built-in (`@NotNull`/`@NotBlank`/`@Size`/`@Pattern`...), `@Valid` e validação em cascata, custom constraints (`@Constraint` + `ConstraintValidator`), validation groups, method validation e integração com CDI/JAX-RS. Implementação de referência: Hibernate Validator (citar como impl, não explicar). Validação no Spring → Galho 9 (texto). Linka Galho 1 (11 - Annotations). |
| 09 | JPA — a especificação de persistência *(opus)* | JPA **nível spec**: `@Entity`/`@Id`/`@GeneratedValue`, mapeamento básico (`@Column`, `@Table`, relacionamentos como contrato da spec — `@OneToMany`/`@ManyToOne` apresentados, SEM fetch tuning), persistence unit (`persistence.xml`), spec vs provider (Hibernate/EclipseLink como impls — citar, não explicar). **Fronteira dura:** fetch strategies/N+1/caching/Spring Data/migrations → Galho 10 (texto, sem wikilink). |
| 10 | EntityManager e o ciclo de vida da entidade *(opus)* | Persistence context, estados da entidade (new/managed/detached/removed), `persist`/`merge`/`remove`/`find`, flush e dirty checking (nível spec), JPQL intro (sintaxe básica, typed queries), `EntityTransaction` (resource-local) vs JTA (gancho pra 11). Fronteira: tuning de performance → Galho 10 (texto). |

#### Magus (4 notas — maestria + decisão de arquitetura; 2 → opus)

| # | Nota | Escopo nuclear |
|---|------|----------------|
| 11 | JTA — transações na plataforma *(opus)* | O problema da transação na plataforma; `UserTransaction` (BMT) vs container-managed (CMT); `@Transactional` (**o do `jakarta.transaction` — desambiguar do Spring por texto**) e `@TransactionScoped`; XA e two-phase commit (conceito); o transaction manager do container. `@Transactional` do Spring → Galhos 8/10 (texto). Linka Galho 4 quando tocar em threads. |
| 12 | EJB — o legado que moldou a plataforma | Visão histórica honesta: session beans (stateless/stateful/singleton), MDB, timer service; por que EJB dominou (transações/segurança/remoting declarativos quando nada mais oferecia) e por que caiu (complexidade, peso, testabilidade); o que o CDI absorveu; EJB 4.0 no Jakarta (estável, sem evolução ativa — verificar); quando você ainda encontra EJB (legados corporativos). Nem obituário nem nostalgia. |
| 13 | CDI avançado — interceptors, decorators e extensões | `@Interceptor`/`@InterceptorBinding`/`@AroundInvoke` (o AOP da plataforma — "é assim que `@Transactional` funciona por baixo", ligando à 11), decorators (`@Decorator`/`@Delegate`), portable extensions (SPI, eventos de container), build compatible extensions (CDI 4 Lite / Core Profile — o caminho build-time). |
| 14 | **Capstone:** Jakarta EE hoje — a plataforma sob o Spring *(opus)* | Estado atual verificado: EE 11 (jun/2025), EE 12 em desenvolvimento, cadência e processo Eclipse (EFSP/specification committee); Core Profile e a nova geração de runtimes (Quarkus/Open Liberty/Helidon usam as specs — citar, não explicar); a relação honesta com o Spring (implementa/abstrai as specs; tabela spec → equivalente Spring como *mapa*, sem explicar o lado Spring); MicroProfile (menção: specs cloud-native complementares); quando plataforma pura vs framework; munição de entrevista. Cheatsheet de fechamento (qual nota pra qual problema). **WebFetch obrigatório, zero estatística de adoção inventada** (regra dos Galhos 5/6). |

**Decisões de fronteira (escopo de outro dono):**
- **Spring (todas as menções)** → Galho 8/9/10 (planejados). Citar como motivação ("é isso que o `@Autowired` esconde") **sem wikilink, sem explicar o framework**. Nenhuma nota deste galho ensina Spring. Não tocar nos troncos `Backend/Spring Boot.md` e `Backend/Spring Data JPA.md`.
- **JPA operacional** (Hibernate, fetch/N+1, caching, Spring Data, migrations) → Galho 10. Aqui só o nível spec: entidade, EntityManager, ciclo de vida, JPQL intro.
- **Spring MVC / REST no Spring / validation no Spring** → Galho 9. Aqui Servlet e JAX-RS como specs.
- **Mecânica de annotations** (retention, meta-annotations) → Galho 1, nota 11 — CDI/JPA/Validation usam pesado: **linkar, não re-explicar**.
- **Generics/records** → Galho 1; **threading/concorrência** → Galho 4; **JPMS** → Galho 3 (nota 08) se tocar em módulos.
- **Kafka** (`Backend/Kafka/`) → Galho 14. Não tocar.

### 3.2. MOC do galho

`03-Dominios/Java/Jakarta EE/index.md`:
- `type: moc`, `status: growing`
- Frontmatter padrão (`title: "Jakarta EE"`, tags `java`/`jakarta-ee`/`moc`, aliases `["Jakarta EE", "Galho 7 - Jakarta EE", "Java EE"]`)
- TL;DR callout (galho cobre a plataforma de especificações enterprise: spec vs impl, transição Java EE → Jakarta EE, Servlet, CDI, JAX-RS, Bean Validation, JPA spec, JTA, legado EJB e estado atual)
- "Sobre este galho" + audiência primária/secundária + nota de que é galho construído por pesquisa (sem tronco)
- Conteúdo agrupado em 3 H2 (`## Iniciado` / `## Adepto` / `## Magus`) com wikilinks pras 14 notas (uma linha descritiva cada)
- **Rotas alternativas (5):**
  - **Completa** — 01 → 14 em ordem
  - **Entrevista internacional** — 01 → 02 → 04 → 09 → 10 → 11 → 14 (modelo da plataforma, transição, CDI, JPA, transações, estado atual — o que mais cai)
  - **O que o Spring esconde** — 04 → 05 → 06 → 13 → 14 (a trilha CDI completa + capstone — o mecanismo por baixo do `@Autowired`/`@Transactional`)
  - **REST do zero na plataforma** — 03 → 04 → 07 → 08 (Servlet, beans, JAX-RS, validação — uma API REST só com specs)
  - **Persistência e transações** — 09 → 10 → 11 (JPA spec, EntityManager, JTA — o contrato antes do Hibernate)
- "Veja também": MOC central `[[03-Dominios/Java/index|Trilha Java]]`, Galho 1 (Linguagem — Annotations), Galho 4 (Concorrência), Dicionário de Java; Galhos 8/9/10 como texto "(planejado)" sem wikilink
- Dataview "Todas as notas do galho"

### 3.3. Dicionário de Java (EXPANSÃO — não recriar)

`03-Dominios/Java/Dicionário de Java.md` já existe (**166 verbetes** após o Galho 6, `type: glossary`, seções alfabéticas). Este galho **expande** o arquivo existente inserindo os verbetes **em ordem alfabética case-insensitive (sem acento)** nas seções apropriadas, criando seções novas quando necessário. **Nunca recriar o arquivo nem reordenar verbetes existentes.** Atualizar `updated` no frontmatter.

Verbetes a inserir (~35):

`@Inject`, `@Observes / eventos CDI`, `@Produces (producer CDI)`, `@Transactional (Jakarta)`, `bean (CDI)`, `bean discovery / beans.xml`, `Bean Validation (Jakarta Validation)`, `CDI (Contexts and Dependency Injection)`, `client proxy (CDI)`, `CMT / BMT (transações container- vs bean-managed)`, `Core Profile`, `decorator (CDI)`, `dirty checking`, `EJB (Enterprise JavaBeans)`, `entity (JPA)`, `EntityManager`, `ExceptionMapper`, `interceptor (CDI)`, `Jakarta EE`, `JAX-RS (Jakarta RESTful Web Services)`, `JPA (Jakarta Persistence)`, `JPQL`, `JTA (Jakarta Transactions)`, `MDB (message-driven bean)`, `persistence context`, `persistence unit / persistence.xml`, `portable extension (CDI)`, `qualifier (CDI)`, `escopo (CDI)`, `servlet`, `servlet container`, `session bean`, `two-phase commit (2PC / XA)`, `Web Profile`, `javax → jakarta (rename de namespace)`.

Cada verbete: definição curta (1-3 linhas) em PT-BR + `Veja também:` apontando pra(s) nota(s) canônica(s) do galho. **Conferir 1:1** que os headings dos verbetes batem EXATAMENTE com as âncoras usadas nas notas (extrair as âncoras de Dicionário das notas via grep e conferir, como nos Galhos 4/5/6).

### 3.4. MOC central (ativação do Galho 7)

`03-Dominios/Java/index.md` já existe. Task **mínima**: trocar a linha 37 (atualmente `7. Jakarta EE *(planejado)* — CDI, Servlet, JAX-RS, Bean Validation, JPA spec, JTA`) por wikilink ativo no padrão dos galhos fechados:

```markdown
7. [[03-Dominios/Java/Jakarta EE/index|Jakarta EE]] — spec vs implementação, transição javax→jakarta, Servlet, CDI, JAX-RS, Bean Validation, JPA spec, JTA, legado EJB, estado atual da plataforma
```

Atualizar `updated`. Não mexer no resto do MOC central.

### 3.5. Sem poda

**Galho novo, sem tronco.** Não há `Jakarta EE.md` a podar. Os troncos `Backend/Spring Boot.md` (Galhos 8/9) e `Backend/Spring Data JPA.md` (Galho 10) **não são deste galho — não tocar**.

### 3.6. Dívida reversa (ganchos "Galho 7 / planejado")

Pré-flight localizou **3 arquivos** com ponteiros a quitar após as notas existirem:

1. `03-Dominios/Java/index.md:37` — linha do galho no MOC central (já coberta pela task 3.4).
2. `Linguagem e sintaxe moderna/11 - Annotations.md:309` — "Este é o ponto de conexão com os **Galhos 7 e 8** (Spring e Jakarta EE)." → vira wikilink pro MOC do galho (Jakarta EE) mantendo o Galho 8 como texto "(planejado)". Opcional, se natural: linha 383 (Bean Validation) ganha wikilink pra nota 08.
3. `JavaFX/11 - Arquitetura — MVC, MVVM e injeção de dependência.md:35,110` — **atribuição incorreta a corrigir**: o texto aponta CDI/Weld pro "Galho 8 (planejado)", mas CDI é deste galho. Fix: CDI/Weld → wikilink pra nota 04 (CDI — beans e injeção); Spring continua texto "Galho 8 (planejado)".

Opcional (menção de passagem, linkar só se natural): `JVM/05 - Classloading.md:44` cita CDI entre frameworks de DI.

## 4. Convenções por nota

Herda §7 do roadmap e §4 dos specs dos Galhos 5/6. Reforços específicos:

### 4.1. Frontmatter

```yaml
---
title: "<título>"
created: 2026-06-07
updated: 2026-06-07
type: concept
status: seedling
publish: true
fase: iniciado | adepto | magus
tags:
  - java
  - jakarta-ee
  - <fase>
  - <tags específicas: cdi, servlet, jax-rs, validation, jpa, jta, ejb, especificacao>
aliases:
  - <aliases opcionais>
---
```

### 4.2. Estrutura H2 obrigatória

- `> [!abstract] TL;DR` (callout, NÃO H2)
- `## O que é` / `## Por que importa` / `## Como funciona` (≥3 subseções H3 em notas Adepto/Magus)
- `## Na prática` — exemplos compiláveis; framing neutro (`Order`/`Customer`/`Product`, "padrão observado em aplicações Jakarta EE"); NUNCA "no meu projeto"
- `## Armadilhas` — **≥2** (Iniciado) / **≥3** (Adepto/Magus), cada uma com descrição + exemplo curto de código demonstrando o problema + fix em 1 linha
- `## Em entrevista` — subheading `### Frase pronta (inglês)` com **3+ sentenças** (trade-off + decisão + caveat) + vocabulário **6+ termos** em tabela `| Termo PT | Termo EN |`
- `## Veja também` — wikilinks **SEM backticks**; sempre inclui notas relacionadas do galho + `[[03-Dominios/Java/Jakarta EE/index|MOC do galho]]` + `[[03-Dominios/Java/index|Trilha Java]]` + (quando conectar) Galho 1 (Annotations) / Galho 4 + verbetes do Dicionário. **Evitar âncoras same-file `[[#Heading]]`** (falso-positivo no checker).
- `## Referências` — docs oficiais (jakarta.ee/specifications/..., Javadoc Jakarta, eclipse.org). **Toda nota é fundada em fonte oficial verificada via WebFetch** (galho de pesquisa). openjdk.org costuma dar 403 no WebFetch — para JEPs usar fallback Oracle/dev.java.

### 4.3. Restrições absolutas

1. **Fronteira Spring (a mais sensível do galho)** — Spring aparece só como motivação em texto ("é isso que o `@Autowired` esconde"), **sem wikilink, sem explicar o framework**. A capstone pode mapear spec → equivalente Spring em tabela, mas o lado Spring é só o nome da feature.
2. **Sem fabricação** de experiência pessoal. Exemplos neutros (`Order`, `Customer`, `OrderResource`, `CustomerRepository` hipotético explícito) — NUNCA `Patient`/`josenaldo`/1ª pessoa. **Zero estatística de adoção inventada** (regra dos Galhos 5/6) — vale pra capstone E pra nota 12 (EJB).
3. **Sem invenção** de APIs/comportamentos. WebFetch obrigatório no Step 1 de cada nota; **Jakarta é campo minado de versões** — toda afirmação version-specific cita a versão da spec (CDI 4.1, Servlet 6.1, REST 4.0, Validation 3.1, Persistence 3.2, Transactions 2.0, EJB 4.0 — EE 11) verificada em jakarta.ee.
4. **Code samples compiláveis** — imports `jakarta.*` (nunca `javax.*`, exceto na nota 02 ao explicar a transição, com contexto explícito).
5. **Comparações justas** — spec vs impl, plataforma vs framework, CMT vs BMT, EJB vs CDI: sempre "quando X" E "quando Y". A capstone e a nota 12 (EJB) são o ápice (nem obituário nem panfleto).
6. **Wikilinks sem backticks** em "Veja também"; MOC do galho + MOC central obrigatórios. **Não linkar galhos inexistentes** (8/9/10/14) — texto "(planejado)".
7. **Code fences corretos:** ` ```java ` pra código, ` ```xml ` pra descritores, ` ```text ` pra output. Sempre fechadas.
8. **`fase:` no frontmatter + na tag** — obrigatório.
9. **Higiene de commits** — sem `Co-Authored-By: Claude`, sem `--no-verify`, `git add <path>` nominal (nunca `-A` — bot de backup roda em timer), 1 commit por nota, controlador commita (subagents write-only).
10. **Tom pedagógico graduado** — Iniciado assume só Galhos 1-2; Magus assume o galho inteiro + Galhos 1-4.

## 5. Conteúdo por nota (síntese)

Esboço do recorte. **Toda nota funda-se em doc oficial verificada via WebFetch.** Fontes-base: `jakarta.ee/specifications/<spec>/<versão>/` (spec documents + Javadoc), `jakarta.ee` (release pages, blog da transição), `eclipse.org` (Eclipse Foundation, EFSP).

- **01 — O modelo Jakarta EE.** Spec vs implementação (a API como contrato, TCK como verificador, impls certificadas); perfis Platform/Web Profile/Core Profile (o que cada um inclui, por que o Core Profile nasceu — runtimes cloud-native); app server (WildFly, Payara, GlassFish) vs servlet container (Tomcat) vs runtime moderno (Open Liberty). Armadilhas: confundir spec com impl ("JPA é o Hibernate"); assumir que todo runtime implementa a Platform inteira. Fontes: jakarta.ee/about/, jakarta.ee/specifications/, jakarta.ee/compatibility/.
- **02 — De Java EE a Jakarta EE.** Linha do tempo verificada: J2EE (1999) → Java EE 5/6/7/8 (Sun→Oracle) → doação à Eclipse Foundation (anúncio 2017) → Jakarta EE 8 (set/2019, `javax` intacto) → EE 9 (dez/2020, big-bang rename) → EE 9.1 (mai/2021, Java 11) → EE 10 (set/2022, Core Profile) → EE 11 (jun/2025) → EE 12 (em desenvolvimento). Por que o rename (Oracle reteve a trademark `javax`/"Java"); estratégia big-bang vs incremental; impacto: imports, bibliotecas em dois mundos, Eclipse Transformer/bytecode tools. Armadilhas: misturar `javax.*` e `jakarta.*` no classpath; assumir que Jakarta EE 8 já usa `jakarta.*`. Fontes: jakarta.ee (release pages), blog Eclipse Foundation.
- **03 — Servlet API.** O contrato servlet (Servlet 6.1 no EE 11): lifecycle, `HttpServlet` e os `doGet`/`doPost`, `HttpServletRequest`/`Response`, sessions (`HttpSession`, cookies, URL rewriting — menção), filters (`Filter`, chain) e listeners (`ServletContextListener` etc.) em panorama, registro via `@WebServlet`/`@WebFilter` vs `web.xml`, async processing (menção honesta). Armadilhas: estado mutável em campo de servlet (1 instância, N threads — linka Galho 4); esquecer thread-safety da session; filter sem `chain.doFilter`. Fontes: jakarta.ee/specifications/servlet/6.1/, Javadoc.
- **04 — CDI: beans e injeção.** O que torna uma classe um bean; `@Inject` em campo/construtor/método (construtor preferido — testabilidade); bean discovery (`beans.xml`, `annotated` vs `all`); tipos de bean (managed beans, producer-made); resolução por tipo. Motivação Spring em 1 parágrafo (texto). Armadilhas: classe sem construtor no-args adequado/`final` (proxy — teaser da 05); ambiguidade de tipo sem qualifier (teaser da 06); `new` manual que ignora o container. Fontes: jakarta.ee/specifications/cdi/4.1/, Weld docs (impl de referência, rotulada).
- **05 — CDI: escopos e contextos (opus).** Cada escopo normal (`@ApplicationScoped`/`@RequestScoped`/`@SessionScoped`/`@ConversationScoped`) + pseudo-escopo `@Dependent`; client proxy: por quê (escopo mais curto injetado em mais longo), consequências (classe não-final, chamada self não passa pelo proxy, lazy init); `@PostConstruct`/`@PreDestroy`. Armadilhas: `@Dependent` onde se espera singleton (N instâncias); injetar `@RequestScoped` em `@ApplicationScoped` e estranhar o proxy; lógica pesada em construtor (proxy instancia lazy — use `@PostConstruct`). Fontes: spec CDI 4.1 (capítulos de scopes/contexts), Javadoc `jakarta.enterprise.context`.
- **06 — CDI: qualifiers, producers e eventos.** `@Qualifier` custom + built-in (`@Default`/`@Any`/`@Named`); `@Produces` (third-party, valores de config, decisão em runtime) + `@Disposes`; eventos: `Event<T>.fire`, `@Observes`, `fireAsync`/`@ObservesAsync`, qualificar eventos; `@Alternative` (+ ativação), `Instance<T>`. Armadilhas: `@Named` como qualifier de injeção (é pra EL); producer sem disposer vazando recurso; observer síncrono lento bloqueando o fire. Fontes: spec CDI 4.1, Javadoc `jakarta.enterprise.inject`/`jakarta.enterprise.event`.
- **07 — JAX-RS.** Resource classes e métodos (REST 4.0 no EE 11); `@Path` com templates, verbos, params; `@Produces`/`@Consumes` (media types — **desambiguar do `@Produces` do CDI explicitamente**); `Response` builder vs retorno direto; providers: `MessageBodyReader/Writer`, `ExceptionMapper`, `ContextResolver` (menção); JSON-B/JSON-P; Client API (`ClientBuilder`). Jersey/RESTEasy citadas como impls. Armadilhas: esquecer `@ApplicationPath`/`Application`; `ExceptionMapper` engolindo exceção sem log; confundir os dois `@Produces`. Fontes: jakarta.ee/specifications/restful-ws/4.0/, Javadoc `jakarta.ws.rs`.
- **08 — Bean Validation.** Constraints built-in (Validation 3.1 no EE 11); onde anotar (campo/getter/parâmetro/retorno/record component — verificar suporte a records na 3.1); `@Valid` cascata; custom constraint (`@Constraint(validatedBy=...)` + `ConstraintValidator`); groups e sequência; method validation (`@Executable...` — verificar) e integração CDI/JAX-RS (400 automático — verificar comportamento na spec). Hibernate Validator = impl de referência (rotulada). Armadilhas: validar e ignorar o `Set<ConstraintViolation>` (não lança sozinho fora do container); constraint em tipo errado (`@Size` em número); esquecer `@Valid` no objeto aninhado. Fontes: jakarta.ee/specifications/ (Validation 3.1), Javadoc `jakarta.validation`.
- **09 — JPA: a especificação (opus).** O contrato (Persistence 3.2 no EE 11): `@Entity` (requisitos da classe), `@Id`/`@GeneratedValue` (estratégias como contrato), `@Column`/`@Table`/`@Transient`, relacionamentos apresentados como vocabulário da spec (`@OneToMany`/`@ManyToOne`/`@ManyToMany` + owning side) **sem fetch tuning** (Galho 10); persistence unit e `persistence.xml`; spec vs provider (Hibernate/EclipseLink citadas). Armadilhas: entidade sem construtor no-args; `equals`/`hashCode` com campos mutáveis/id gerado (apresentar o dilema honestamente); esquecer o owning side em bidirectional. Fontes: jakarta.ee/specifications/persistence/3.2/, Javadoc `jakarta.persistence`.
- **10 — EntityManager e ciclo de vida (opus).** Persistence context (cache de identidade + unit of work — nível spec); estados new/managed/detached/removed e as transições (`persist`/`merge`/`remove`/`find`/`detach`); flush (quando acontece, `FlushModeType`) e dirty checking como contrato; JPQL intro (`TypedQuery`, parâmetros nomeados); `EntityTransaction` (resource-local) vs JTA-managed (gancho 11). Armadilhas: usar a entidade retornada errada após `merge` (merge retorna a managed); esperar UPDATE sem transação ativa; `LazyInitializationException` conceitual — entidade detached fora do contexto (sem entrar em fetch tuning — Galho 10). Fontes: spec Persistence 3.2 (capítulos EntityManager/lifecycle), Javadoc.
- **11 — JTA (opus).** Por que transações são problema da plataforma (recursos múltiplos, container coordena); BMT com `UserTransaction` vs CMT declarativo; `@Transactional` do `jakarta.transaction` (tipos `REQUIRED`/`REQUIRES_NEW`... como contrato; **desambiguar do Spring por texto**); `@TransactionScoped`; XA/two-phase commit em conceito (coordinator, prepare/commit, o custo); onde o JTA aparece (JPA, JMS — menção). Armadilhas: misturar BMT e CMT; chamada self que não passa pelo interceptor (liga à 05/13); assumir rollback automático em checked exception (regra de rollback da spec — verificar). Fontes: jakarta.ee/specifications/transactions/2.0/, Javadoc `jakarta.transaction`.
- **12 — EJB: o legado.** O que foi o EJB (2.x: entity beans, home interfaces, XML — o peso; 3.x: a simplificação por annotations); session beans stateless/stateful/singleton + pooling; MDB; timer service; o que o CDI absorveu e o que restou exclusivo (verificar na spec 4.0: timers, MDB, pooling); status atual (EJB 4.0 estável no EE 11, evolução parada — verificar); onde ainda se encontra (legados corporativos, migrações). Armadilhas (de raciocínio): tratar EJB como sinônimo de Java enterprise atual; reescrever EJB estável sem business case; confundir entity beans (mortos) com JPA entities. Fontes: jakarta.ee/specifications/enterprise-beans/4.0/, história em jakarta.ee/eclipse.org.
- **13 — CDI avançado.** Interceptors: `@InterceptorBinding` custom, `@Interceptor` + `@AroundInvoke`, ativação/ordem (`@Priority`), "é assim que `@Transactional` funciona" (liga à 11); decorators (`@Decorator`/`@Delegate` — quando decorar vs interceptar); portable extensions (eventos de container `ProcessAnnotatedType` etc. — panorama, não tutorial de SPI); build compatible extensions (CDI 4 Lite, Core Profile, build-time — por quê: runtimes modernos/native image, citar sem explicar Quarkus). Armadilhas: interceptor não ativado (falta `@Priority`/`beans.xml`); self-invocation; lógica de negócio em interceptor. Fontes: spec CDI 4.1 (Full vs Lite), Javadoc `jakarta.interceptor`/`jakarta.decorator`.
- **14 — Capstone: Jakarta EE hoje (opus).** Estado verificado com data: EE 11 (26/jun/2025), EE 12 em desenvolvimento, processo Eclipse (working group, EFSP, TCK); os 3 perfis e o papel estratégico do Core Profile (specs mínimas pra runtimes cloud-native — Quarkus/Open Liberty/Helidon citados como consumidores das specs, 1 linha cada); MicroProfile em 1 parágrafo (complemento cloud-native, governança própria — menção); a tese do galho fechada: tabela spec Jakarta → o que o Spring oferece por cima (só nomes do lado Spring, Galho 8 planejado); decisão honesta plataforma pura vs framework ("quando X / quando Y", sem dogma e sem estatística); munição de entrevista; cheatsheet nota → problema. **WebFetch obrigatório em jakarta.ee no dia da execução.** Armadilhas (de raciocínio): "Jakarta EE morreu" (EE 11 é de 2025; specs são a fundação dos runtimes modernos); "Spring substituiu as specs" (Spring as implementa/consome em várias áreas); decidir plataforma por ideologia em vez de requisito. Fontes: jakarta.ee, blog Eclipse Foundation, página EE 11.

## 6. Pré-flight (substitui a poda): verificações feitas

Executado nesta fase de brainstorming (2026-06-07); itens version-specific re-confirmados na execução de cada nota:

1. **Sem conteúdo Jakarta preexistente** — grep por "Jakarta", "javax", "JAX-RS", "CDI" em `03-Dominios/Java/`: só menções de passagem (Annotations, troncos Spring dos Galhos 8/10, `javax.swing` do Galho 5). Nenhuma pasta/nota Jakarta EE. Pasta `Jakarta EE/` é nova.
2. **Versões cravadas via WebFetch em jakarta.ee (2026-06-07):** plataforma atual **Jakarta EE 11 (26/jun/2025)**, EE 12 em desenvolvimento. Specs no EE 11: **CDI 4.1, Servlet 6.1, RESTful Web Services 4.0, Validation 3.1, Persistence 3.2, Transactions 2.0, Enterprise Beans 4.0** (todas com sucessoras "under development"). Releases históricas: EE 8 (10/set/2019), EE 9 (08/dez/2020 — rename), EE 9.1 (25/mai/2021), EE 10 (22/set/2022), EE 11 (26/jun/2025).
3. **Dívida reversa localizada** (§3.6): MOC central linha 37; Annotations.md:309; JavaFX/11:35,110 (com atribuição CDI→Galho 8 a corrigir).
4. **Dicionário**: 166 verbetes; expansão alfabética, nunca recriar.
5. **Troncos intocáveis**: `Backend/Spring Boot.md`, `Backend/Spring Data JPA.md`, `Backend/Kafka/`.

Nenhum número de adoção é inventado. Quando faltar fato verificável, **PERGUNTAR** antes de escrever.

## 7. Critérios de aceitação do galho

Além dos critérios gerais (§10 do roadmap):

1. 14 notas em `03-Dominios/Java/Jakarta EE/`, frontmatter completo com `fase:`, `publish: true`, distribuídas 4/6/4.
2. MOC do galho com 3 subseções de fase + 5 rotas alternativas + dataview + folder-link resolve (`index.md` presente).
3. Dicionário de Java **expandido** (não recriado) com ~35 verbetes; verbetes dos Galhos 1-6 intactos; `updated` atualizado; headings conferidos 1:1 com as âncoras usadas nas notas (via grep).
4. MOC central `Java/index.md` com Galho 7 ativado (linha 37 vira wikilink); resto intacto.
5. **Dívida reversa quitada**: Annotations.md:309 e JavaFX/11:35,110 com wikilinks corretos (CDI atribuído ao Galho 7; Spring permanece texto "Galho 8 planejado").
6. **Sem poda** — nenhum tronco modificado (`Spring Boot.md`/`Spring Data JPA.md`/`Kafka/` intactos).
7. Cada nota: TL;DR; code samples compiláveis com imports `jakarta.*`; "Em entrevista" com `### Frase pronta (inglês)` 3+ sentenças + tabela 6+ termos PT→EN; "Armadilhas" com exemplo+fix (≥2 Iniciado, ≥3 Adepto/Magus); wikilinks (galho + MOC central + Galho 1/4 quando conectar + Dicionário); "Referências" com docs oficiais verificadas.
8. **Fronteira Spring respeitada**: zero wikilink pra conteúdo Spring; zero explicação de framework; menções só como motivação/mapa.
9. Zero fabricação de experiência pessoal; zero estatística de adoção inventada (capstone E nota 12); afirmações version-specific citam a versão da spec.
10. 1 commit por nota; sem `Co-Authored-By: Claude`; sem `--no-verify`; stage nominal (nunca `-A`); subagents write-only, controlador commita.
11. `verificar-wikilinks` roda limpo na pasta do galho (as ~204 quebras legadas da árvore Java NÃO são deste galho; evitar âncoras same-file).

## 8. Riscos e mitigações

| Risco | Mitigação |
|---|---|
| **Explicar Spring em vez da spec** (a fronteira mais sensível) | Restrição 4.3.1; Spring só como motivação em texto; review por fase checa explicitamente; capstone mapeia em tabela sem explicar o lado Spring. |
| Campo minado de versões (afirmar coisa de CDI 5/EE 12 como atual, ou de Java EE como Jakarta) | Versões cravadas no §6; WebFetch obrigatório por nota; toda afirmação version-specific cita a versão; nota 02 é a dona da linha do tempo. |
| JPA invadir o Galho 10 (fetch, N+1, Hibernate) | Notas 09/10 são nível spec (contrato, ciclo de vida); fronteira dura declarada; review por fase checa. |
| Galho de pesquisa: inventar API "de memória" | WebFetch no Step 1 de cada nota; Referências com fonte oficial; nada sem conferir no spec document/Javadoc. |
| Nota 12 (EJB) virar obituário ou nostalgia | Mesma regra da capstone do Galho 5: separar status oficial (EJB 4.0 estável no EE 11) de consenso de-facto; "quando ainda se encontra" honesto; zero estatística. |
| `@Produces` homônimo (CDI vs JAX-RS) confundir o leitor | Notas 06 e 07 desambiguam explicitamente; verbetes separados no Dicionário. |
| Capstone inflar (estado atual + perfis + Spring map + MicroProfile) | Cheatsheet enxuto; MicroProfile em 1 parágrafo; runtimes em 1 linha cada; se passar de ~600 linhas, dividir (regra de notas atômicas). |
| openjdk.org 403 no WebFetch | Fallback Oracle/dev.java (cravado nos galhos anteriores); pra specs Jakarta o site é jakarta.ee (sem esse problema). |
| Bot de backup (Obsidian Git) commitando no meio | Padrão dos Galhos 2/3/6: subagents write-only; controlador commita imediatamente após cada nota com `git add` nominal. |
| Magus crescer demais | Distribuição 4/6/4 fixada; se uma nota inflar, dividir nota, não galho. |

## 9. Próximos passos

1. **Aprovação deste spec**
2. **Plano de execução** via skill `superpowers:writing-plans` → `docs/superpowers/plans/2026-06-07-java-galho-07-jakarta-ee-execution.md`
3. **Execução** via `superpowers:subagent-driven-development` **direto na `main`** (subagents write-only; sonnet, opus pras notas 05/09/10/11/14; review **por fase** + fix loop; push manual do usuário)
4. **Verificação** de wikilinks + conferência de âncoras do Dicionário
5. **Revisão do roadmap** com aprendizados antes do próximo galho

## 10. Documentos relacionados

- `2026-06-02-java-senior-roadmap-design.md` — roadmap macro (18 galhos)
- `2026-06-03-java-galho-05-swing-design.md` / `...-execution.md` — Galho 5 (template de galho de PESQUISA)
- `2026-06-06-java-galho-06-javafx-design.md` / `...-execution.md` — Galho 6 (template mais recente)
- Artefatos a atualizar: `03-Dominios/Java/Dicionário de Java.md`, `03-Dominios/Java/index.md`, `Linguagem e sintaxe moderna/11 - Annotations.md`, `JavaFX/11 - Arquitetura — MVC, MVVM e injeção de dependência.md`
- Fontes-base do galho: `jakarta.ee/specifications/...` (spec documents + Javadoc), `jakarta.ee` (releases, blog), `eclipse.org`
- Memórias: [[project_trilha_java]], [[project_trilhas_fases_aprendizado]], [[feedback_galhos_direto_main]], [[feedback_no_fabrication]], [[feedback_quartz_index]], [[feedback_commits]]
