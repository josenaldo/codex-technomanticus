# Galho 7 — Jakarta EE (Java Senior) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Criar o Galho 7 da trilha Java Senior — 14 notas atômicas (modelo spec vs impl, transição javax→jakarta, Servlet, CDI ×4, JAX-RS, Bean Validation, JPA spec ×2, JTA, EJB, capstone) em 3 fases + MOC do galho + expansão do Dicionário + ativação do MOC central + **quitação da dívida reversa** (incluindo a correção de atribuição CDI→Galho 8 no JavaFX/11).

**Architecture:** Padrão galhos + 3 fases (Iniciado/Adepto/Magus). Pasta flat `03-Dominios/Java/Jakarta EE/`, notas `publish: true` em PT-BR, numeração global 01-14 (4/6/4). **Galho de PESQUISA, como o Galho 5** (roadmap: "Tronco a podar: nenhum") — toda nota nasce de doc oficial (jakarta.ee, spec documents, Javadoc Jakarta) verificada via WebFetch; **sem task de poda**. **Fronteira mais sensível:** Spring implementa/abstrai estas specs (Galho 8, planejado) — citar como motivação ("é isso que o `@Autowired` esconde") **SEM wikilink e SEM explicar o framework**; o galho explica a SPEC. JPA operacional (Hibernate/fetch/N+1/Spring Data) → Galho 10 (texto); Spring MVC/validation-no-Spring → Galho 9 (texto); mecânica de annotations → Galho 1 nota 11 (linkar); concorrência → Galho 4; JPMS → Galho 3 nota 08; `Backend/Kafka/` é do Galho 14 — não tocar. Troncos `Backend/Spring Boot.md` e `Backend/Spring Data JPA.md` **intocáveis**. **Direto na `main`** ([[feedback_galhos_direto_main]]); push manual do usuário.

**Tech Stack:** Obsidian Flavored Markdown, frontmatter YAML, wikilinks, callouts, Dataview, Quartz v4. Verificação via WebFetch (jakarta.ee, Javadoc das specs; openjdk.org dá 403 → fallback Oracle/dev.java).

---

## Convenções aplicadas a TODAS as notas (ler antes de qualquer task)

**Frontmatter** (ajustar `title`/`fase`/`tags`/`aliases` por nota; `created`/`updated: 2026-06-07`):

```yaml
---
title: "<título sem prefixo numérico>"
created: 2026-06-07
updated: 2026-06-07
type: concept
progress: backlog
status: seedling
publish: true
fase: iniciado | adepto | magus
tags:
  - java
  - jakarta-ee
  - <fase>
  - <1-3 tags de conceito: especificacao, cdi, servlet, jax-rs, validation, jpa, jta, ejb>
aliases:
  - <aliases>
---
```

**Estrutura H2 obrigatória** (nesta ordem):

1. `> [!abstract] TL;DR` — 2-4 linhas. Callout, NÃO H2.
2. `## O que é` — definição.
3. `## Por que importa` — relevância pra senior/entrevista. (Pode fundir com "O que é" em Iniciado curtas.)
4. `## Como funciona` — H3s; mínimo 3 em Adepto/Magus.
5. `## Na prática` — código compilável com **imports `jakarta.*`** (NUNCA `javax.*`, exceto nota 02 ao explicar a transição, com contexto explícito); framing neutro; **NUNCA** 1ª pessoa, `Patient`, `Josenaldo`. Domínios neutros: `Order`, `Customer`, `Product`.
6. `## Armadilhas` — ≥2 (Iniciado) / ≥3 (Adepto/Magus). Cada uma: `### (N) Título` + descrição + exemplo curto + fix em 1 linha.
7. `## Em entrevista` — `### Frase pronta (inglês)` com **3+ sentenças** (trade-off + decisão + caveat) + "Vocabulário" **6+ termos** em tabela `| Termo PT | Termo EN |`.
8. `## Veja também` — wikilinks SEM backticks, SEM âncoras same-file `[[#...]]`. Sempre: notas do galho + `[[03-Dominios/Java/Jakarta EE/index|Jakarta EE (MOC do galho)]]` + `[[03-Dominios/Java/index|Trilha Java]]` + (quando conectar) Galhos 1/2/3/4 + verbetes do Dicionário.
9. `## Referências` — docs oficiais consultadas (jakarta.ee, spec documents, Javadoc).

**Tamanho:** 200-500 linhas (densas até 600 — limite de [[feedback_notas_atomicas]]).

**Restrições absolutas:**
- **Fronteira Spring (a mais sensível):** Spring só como motivação em texto, sem wikilink, sem explicar o framework. Greps de review checam `\[\[[^]]*Spring`.
- Sem fabricação ([[feedback_no_fabrication]]); **zero estatística de adoção inventada** (regra dos Galhos 5/6) — vale pra capstone (14) E pra nota de EJB (12).
- **Campo minado de versões:** toda afirmação version-specific cita a versão da spec no EE 11 (CDI 4.1, Servlet 6.1, REST 4.0, Validation 3.1, Persistence 3.2, Transactions 2.0, EJB 4.0 — cravadas no spec §6, re-verificar via WebFetch nota a nota). Nada de memória.
- **Não re-explicar o que é de outro galho:** annotations → Galho 1 (nota 11); lambdas → Galho 2 (nota 04); JPMS → Galho 3 (nota 08); threads → Galho 4. Spring → "Galho 8 (planejado)", Spring MVC/validation → "Galho 9 (planejado)", JPA operacional/Hibernate → "Galho 10 (planejado)", texto puro SEM wikilink.
- Comparações justas (spec vs impl, plataforma vs framework, CMT vs BMT, EJB vs CDI: quando X E quando Y).
- Code fences: ` ```java `, ` ```xml ` (descritores/persistence.xml), ` ```bash `, ` ```text `. Sempre fechadas.
- Commits: sem `Co-Authored-By: Claude`; sem `--no-verify`; `git add <path>` nominal (bot de backup roda em timer — NUNCA `-A`); 1 commit por nota; direto na `main`; **sem push, sem deploy**. Subagents NÃO rodam git — o controlador commita.

**Modelo por nota:** sonnet por padrão; **opus** nas **05** (CDI escopos), **09** (JPA spec), **10** (EntityManager), **11** (JTA) e **14** (capstone).

**Fontes oficiais (base):**
- Hub de specs: `https://jakarta.ee/specifications/` (navegar pro path exato de cada spec a partir daqui)
- Plataforma EE 11: `https://jakarta.ee/specifications/platform/11/` · releases: `https://jakarta.ee/release/`
- CDI 4.1: `https://jakarta.ee/specifications/cdi/4.1/` (spec document + apidocs)
- Servlet 6.1: `https://jakarta.ee/specifications/servlet/6.1/`
- RESTful Web Services 4.0: `https://jakarta.ee/specifications/restful-ws/4.0/`
- Validation 3.1: navegar de `https://jakarta.ee/specifications/` (path `bean-validation` ou `validation` — conferir)
- Persistence 3.2: `https://jakarta.ee/specifications/persistence/3.2/`
- Transactions 2.0: `https://jakarta.ee/specifications/transactions/2.0/`
- Enterprise Beans 4.0: `https://jakarta.ee/specifications/enterprise-beans/4.0/`
- História/transição: `https://jakarta.ee/about/` + blog Eclipse Foundation (buscar a partir de jakarta.ee)
- Versões cravadas no pré-flight do spec (2026-06-07): **EE 11 (26/jun/2025) atual; EE 12 em desenvolvimento**.

---

## Task 0: Pré-flight — pasta e confirmação do terreno

**Files:**
- Create: `03-Dominios/Java/Jakarta EE/` (pasta)

- [ ] **Step 1: Confirmar `main`**

```bash
git branch --show-current
```
Expected: `main`. NÃO criar branch.

- [ ] **Step 2: Criar a pasta do galho**

```bash
mkdir -p "03-Dominios/Java/Jakarta EE"
```

- [ ] **Step 3: Confirmar que não há conteúdo Jakarta preexistente (galho novo)**

```bash
ls "03-Dominios/Java/"
grep -rli "jakarta" "03-Dominios/Java/" --include="*.md" | grep -viE "Backend/|index.md|Annotations|O modelo da linguagem|A evolução do Java|Certificação|Records"
```
Expected: nenhuma pasta `Jakarta EE` prévia além da recém-criada; segundo grep vazio ou só menções de passagem conhecidas. NÃO tocar em `Backend/Spring Boot.md`, `Backend/Spring Data JPA.md`, `Backend/Kafka/`.

- [ ] **Step 4: Confirmar títulos exatos das notas vizinhas linkadas**

```bash
ls "03-Dominios/Java/Linguagem e sintaxe moderna/" | grep -E "^11 "
ls "03-Dominios/Java/Collections e Streams/" | grep -E "^04 "
ls "03-Dominios/Java/JVM/" | grep -E "^08 "
ls "03-Dominios/Java/Concorrência e paralelismo/" | grep -E "^(02|08) "
```
Expected: confirmar filenames exatos (o plano assume `11 - Annotations`, `04 - Lambdas e interfaces funcionais`, `08 - JPMS — o sistema de módulos`, `02 - Threads...`, `08 - Executors...`). Anotar divergências.

- [ ] **Step 5: Relocalizar a dívida reversa**

```bash
grep -n "planejado" "03-Dominios/Java/index.md" | grep -i "jakarta"
grep -n "Galhos 7 e 8" "03-Dominios/Java/Linguagem e sintaxe moderna/11 - Annotations.md"
grep -n "Galho 8" "03-Dominios/Java/JavaFX/11 - Arquitetura — MVC, MVVM e injeção de dependência.md"
```
Expected: MOC central linha ~37; Annotations linha ~309; JavaFX/11 linhas ~35 e ~110 (estas duas com **atribuição incorreta** — apontam CDI/Weld pro Galho 8; CDI é DESTE galho). Anotar linhas reais pra Task 18.

- [ ] **Step 6: Baseline do Dicionário**

```bash
grep -cE "^### " "03-Dominios/Java/Dicionário de Java.md"
```
Expected: **166** (baseline pós-Galho 6). Anotar o número real.

- [ ] **Step 7: Fixar fatos a verificar (WebFetch nota a nota)**

Versões EE 11 (cravadas no spec §6, re-confirmar): CDI 4.1, Servlet 6.1, REST 4.0, Validation 3.1, Persistence 3.2, Transactions 2.0, EJB 4.0. Linha do tempo: doação anunciada 2017; Jakarta EE 8 (10/set/2019, `javax`); EE 9 (08/dez/2020, rename big-bang); EE 9.1 (25/mai/2021); EE 10 (22/set/2022, Core Profile); EE 11 (26/jun/2025); EE 12 em desenvolvimento. Nada de memória.

- [ ] **Step 8: Sem commit** (preparação).

---

## Fase INICIADO (notas 01-04)

### Task 1: Nota 01 — O modelo Jakarta EE — especificações e implementações

**Files:**
- Create: `03-Dominios/Java/Jakarta EE/01 - O modelo Jakarta EE — especificações e implementações.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch `https://jakarta.ee/about/` + `https://jakarta.ee/specifications/` + `https://jakarta.ee/compatibility/` (produtos compatíveis). CONFIRMAR: o que é uma especificação Jakarta (API + spec document + TCK), os 3 perfis (Platform / Web Profile / Core Profile) e o que o Core Profile contém (CDI Lite etc. — conferir), exemplos de implementações certificadas (GlassFish, WildFly, Payara, Open Liberty), papel do TCK.

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: iniciado`, tags `[java, jakarta-ee, iniciado, especificacao]`, aliases `["Jakarta EE", "Especificações Jakarta", "Java EE"]`.

Conteúdo:
- TL;DR: Jakarta EE não é um produto — é um **conjunto de especificações** (contratos de API) com múltiplas implementações certificadas por TCK; o Spring implementa/abstrai boa parte delas por baixo (motivação, sem explicar).
- `## O que é` — plataforma de specs enterprise; o trio API jar + spec document + TCK; spec vs implementação ("JPA não é o Hibernate: JPA é o contrato, Hibernate é uma implementação").
- `## Por que importa` — o modelo mental que destrava o bloco enterprise inteiro da trilha; entrevista cobra "qual a diferença entre JPA e Hibernate?"; é esse contrato que o `@Autowired`/`@Transactional` escondem (texto, Galho 8 planejado).
- `## Como funciona` — H3s: "Anatomia de uma spec (API, documento, TCK, implementação ratificadora)", "Os 3 perfis (Platform completa / Web Profile / Core Profile pra runtimes cloud-native)", "Onde roda (app server completo: WildFly/Payara/GlassFish; servlet container: Tomcat/Jetty — só Servlet+; runtimes modernos: Open Liberty)", "As specs deste galho no EE 11 (tabela: CDI 4.1, Servlet 6.1, REST 4.0, Validation 3.1, Persistence 3.2, Transactions 2.0, EJB 4.0)".
- `## Na prática` — `pom.xml` com BOM/API da plataforma (`jakarta.platform:jakarta.jakartaee-api` — conferir coordenada via WebFetch) em ```xml; mostrar que o código compila contra a API e roda na impl do servidor.
- `## Armadilhas` — ≥2: (1) confundir spec com impl ("instalei o JPA") → API no compile, impl no runtime; (2) assumir que todo runtime implementa a Platform inteira (Tomcat não tem CDI/JPA nativos) → conferir o perfil; (3) misturar versões de API e de servidor incompatíveis → alinhar com a versão EE do servidor.
- `## Em entrevista` + `## Veja também` ([[02 - De Java EE a Jakarta EE]], [[04 - CDI — beans e injeção]], [[14 - Jakarta EE hoje — a plataforma sob o Spring]], MOC galho, MOC central, [[03-Dominios/Java/Dicionário de Java#Jakarta EE|Jakarta EE (Dicionário)]], [[03-Dominios/Java/Dicionário de Java#Web Profile|Web Profile (Dicionário)]], [[03-Dominios/Java/Dicionário de Java#Core Profile|Core Profile (Dicionário)]]) + `## Referências`.

Tamanho: 220-340 linhas.

- [ ] **Step 3: Verificar**

```bash
grep -cE "^## (O que é|Por que importa|Como funciona|Na prática|Armadilhas|Em entrevista|Veja também|Referências)" "03-Dominios/Java/Jakarta EE/01 - O modelo Jakarta EE — especificações e implementações.md"
grep -E "TCK|Web Profile|Core Profile|implementação|WildFly|Open Liberty" "03-Dominios/Java/Jakarta EE/01 - O modelo Jakarta EE — especificações e implementações.md" | head
grep -E "\[\[[^]]*Spring" "03-Dominios/Java/Jakarta EE/01 - O modelo Jakarta EE — especificações e implementações.md"
```
Expected: ≥7 seções; conceitos cobertos; **último grep VAZIO**.

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Java/Jakarta EE/01 - O modelo Jakarta EE — especificações e implementações.md"
git commit -m "feat(java): galho 7 nota 01 — o modelo Jakarta EE (especificações e implementações)"
```

---

### Task 2: Nota 02 — De Java EE a Jakarta EE

**Files:**
- Create: `03-Dominios/Java/Jakarta EE/02 - De Java EE a Jakarta EE.md`

- [ ] **Step 1: Pesquisar fonte — VERIFICAÇÃO DE LINHA DO TEMPO OBRIGATÓRIA**

WebFetch `https://jakarta.ee/release/` (datas oficiais) + `https://jakarta.ee/about/` + página de release do EE 9 (`https://jakarta.ee/release/9/` se existir — navegar) pra confirmar o big-bang rename e a justificativa (trademark). CONFIRMAR: J2EE→Java EE (rebrand 2006, Java EE 5), doação à Eclipse anunciada em 2017, Jakarta EE 8 = 10/set/2019 (ainda `javax`), EE 9 = 08/dez/2020 (rename `javax`→`jakarta`), EE 9.1 = 25/mai/2021 (Java 11), EE 10 = 22/set/2022 (Core Profile novo), EE 11 = 26/jun/2025, EE 12 em desenvolvimento. Eclipse Transformer como tooling de migração (confirmar existência via busca em jakarta.ee/eclipse.org; hedge se não confirmar).

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: iniciado`, tags `[java, jakarta-ee, iniciado, especificacao]`, aliases `["javax para jakarta", "Transição Java EE Jakarta EE", "Jakarta EE 9"]`.

Conteúdo:
- TL;DR: Java EE virou Jakarta EE quando a Oracle doou a plataforma à Eclipse Foundation (2017), mas reteve a trademark "Java" — daí o **rename big-bang `javax.*` → `jakarta.*` no EE 9 (2020)**, que partiu o ecossistema em dois mundos de namespace.
- `## O que é` — a transição de governança (Sun → Oracle → Eclipse Foundation) e de namespace.
- `## Por que importa` — TODO projeto enterprise vivo cruzou ou vai cruzar essa fronteira; "por que meus imports quebraram?" é a pergunta prática; entrevista cobra a história e o porquê do rename.
- `## Como funciona` — H3s: "Linha do tempo (J2EE 1999 → Java EE 5-8 → doação 2017 → Jakarta EE 8 set/2019 → EE 9 dez/2020 → 9.1 → 10 → 11 jun/2025 → 12 em dev)" com tabela de datas verificadas; "Por que o rename (trademark: Oracle reteve `javax`/'Java'; Jakarta EE 8 foi a transição de governança SEM rename; EE 9 foi o rename SEM features novas — a estratégia big-bang)"; "O impacto prático (imports, dependências em dois mundos, servidores; bibliotecas que suportam ambos; bytecode transformation — Eclipse Transformer)"; "Como identificar o mundo de um projeto (imports, versões de dependência, versão do servidor)".
- `## Na prática` — diff de import em ```java (`import javax.persistence.Entity` → `import jakarta.persistence.Entity` — ÚNICO lugar do galho onde `javax.*` aparece, com contexto explícito); tabela spec → artefato pré/pós-rename; checklist hipotético de migração (explícito como hipotético).
- `## Armadilhas` — ≥2: (1) misturar `javax.*` e `jakarta.*` no mesmo classpath (ClassNotFound/NoSuchMethod em runtime) → alinhar TODAS as dependências num mundo só; (2) achar que Jakarta EE 8 já usa `jakarta.*` (não — rename foi no 9) → conferir a versão; (3) subir app `javax` em servidor `jakarta` (ou vice-versa) sem transformer → versão do servidor compatível ou migrar.
- `## Em entrevista` + `## Veja também` (01, 14, MOC galho, MOC central, [[03-Dominios/Java/Dicionário de Java#javax → jakarta (rename)|javax → jakarta (Dicionário)]], [[03-Dominios/Java/Dicionário de Java#Jakarta EE|Jakarta EE (Dicionário)]]) + `## Referências`.

Tamanho: 220-340 linhas.

- [ ] **Step 3: Verificar**

```bash
grep -E "2017|2019|2020|2022|2025|trademark|big-bang|Eclipse Foundation" "03-Dominios/Java/Jakarta EE/02 - De Java EE a Jakarta EE.md" | head
grep -c "javax" "03-Dominios/Java/Jakarta EE/02 - De Java EE a Jakarta EE.md"
```
Expected: linha do tempo + trademark cobertos; `javax` presente (esta é a ÚNICA nota onde é esperado em volume).

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Java/Jakarta EE/02 - De Java EE a Jakarta EE.md"
git commit -m "feat(java): galho 7 nota 02 — de Java EE a Jakarta EE"
```

---

### Task 3: Nota 03 — Servlet API — o alicerce HTTP

**Files:**
- Create: `03-Dominios/Java/Jakarta EE/03 - Servlet API — o alicerce HTTP.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch `https://jakarta.ee/specifications/servlet/6.1/` (spec document/apidocs). CONFIRMAR: lifecycle (`init`/`service`/`destroy`), `HttpServlet` e os `doXxx`, `HttpServletRequest`/`HttpServletResponse`, `HttpSession`, `Filter`/`FilterChain`, listeners (`ServletContextListener` etc.), `@WebServlet`/`@WebFilter`/`@WebListener` vs `web.xml`, async processing (existência e forma — menção honesta).

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: iniciado`, tags `[java, jakarta-ee, iniciado, servlet]`, aliases `["Servlet", "Servlet API", "HttpServlet"]`.

Conteúdo:
- TL;DR: a Servlet API é o contrato entre o código Java e o servidor HTTP — **uma instância, muitas threads**; tudo que atende HTTP no ecossistema (incluindo o Spring MVC, texto sem explicar — Galho 9 planejado) roda sobre ela.
- `## O que é` — o contrato servlet (Servlet 6.1 no EE 11); container gerencia lifecycle e threading.
- `## Por que importa` — é o chão de TODA aplicação web Java; "o que acontece quando uma request chega?" é pergunta clássica; filters são a origem da ideia de middleware.
- `## Como funciona` — H3s: "Lifecycle (`init` → N×`service` → `destroy`; 1 instância, N threads — linka Galho 4 sem re-explicar threads)", "`HttpServlet` (`doGet`/`doPost`; request/response; status, headers, body)", "Sessões (`HttpSession`, cookies, o trade-off de estado no servidor)", "Filters e listeners (chain, casos: logging/auth/encoding; listeners de contexto e sessão)", "Registro (`@WebServlet` vs `web.xml` — quando cada um) e async processing (menção)".
- `## Na prática` — `OrderServlet` completo em ```java (`@WebServlet("/orders")`, `doGet` escrevendo JSON simples, `doPost` lendo parâmetros); um `Filter` de logging com `chain.doFilter`.
- `## Armadilhas` — ≥2: (1) estado mutável em campo de servlet (race — 1 instância, N threads) → atributos de request/session ou imutabilidade; (2) filter sem `chain.doFilter` (request morre silenciosa) → sempre delegar ou responder explicitamente; (3) guardar objetos pesados na session sem expiração (memória) → minimizar e configurar timeout.
- `## Em entrevista` + `## Veja também` (01, 07, [[03-Dominios/Java/Concorrência e paralelismo/index|Concorrência (Galho 4)]], MOC galho, MOC central, [[03-Dominios/Java/Dicionário de Java#servlet|servlet (Dicionário)]], [[03-Dominios/Java/Dicionário de Java#servlet container|servlet container (Dicionário)]]) + `## Referências`.

Tamanho: 240-380 linhas.

- [ ] **Step 3: Verificar**

```bash
grep -E "HttpServlet|doGet|FilterChain|HttpSession|@WebServlet|init|destroy" "03-Dominios/Java/Jakarta EE/03 - Servlet API — o alicerce HTTP.md" | head
grep -E "import javax" "03-Dominios/Java/Jakarta EE/03 - Servlet API — o alicerce HTTP.md"
```
Expected: contrato coberto; **segundo grep VAZIO** (só `jakarta.servlet`).

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Java/Jakarta EE/03 - Servlet API — o alicerce HTTP.md"
git commit -m "feat(java): galho 7 nota 03 — Servlet API, o alicerce HTTP"
```

---

### Task 4: Nota 04 — CDI — beans e injeção

**Files:**
- Create: `03-Dominios/Java/Jakarta EE/04 - CDI — beans e injeção.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch `https://jakarta.ee/specifications/cdi/4.1/` (spec document — capítulos de beans/injection/bean discovery). CONFIRMAR: o que torna uma classe um bean (managed bean), `@Inject` em campo/construtor/método, bean discovery modes (`annotated` default vs `all`; papel do `beans.xml` no CDI 4), typesafe resolution, Weld como implementação de referência (rotular como impl).

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: iniciado`, tags `[java, jakarta-ee, iniciado, cdi]`, aliases `["CDI", "Injeção de dependência Jakarta", "@Inject"]`.

Conteúdo:
- TL;DR: CDI é a spec de injeção de dependência e contextos da plataforma — o container constrói o grafo de objetos por você. **É isso que o `@Autowired` esconde** (Spring → Galho 8 planejado, texto).
- `## O que é` — Contexts and Dependency Injection (CDI 4.1 no EE 11); inversão de controle; o container como dono do ciclo de vida.
- `## Por que importa` — é o coração da plataforma (quase toda spec moderna integra com CDI); o modelo mental de DI é pré-requisito do bloco enterprise inteiro; entrevista: "como o container sabe o que injetar?".
- `## Como funciona` — H3s: "O que é um bean (requisitos de managed bean; o que o container instancia)", "`@Inject` (campo vs construtor vs método — construtor preferido: testabilidade e imutabilidade)", "Bean discovery (`annotated` vs `all`; o `beans.xml` no CDI 4)", "Resolução typesafe (por tipo; ambiguidade → teaser qualifiers, nota 06)", "Annotations por baixo (linka [[03-Dominios/Java/Linguagem e sintaxe moderna/11 - Annotations|Annotations (Galho 1)]] — RUNTIME retention + reflection, sem re-explicar)".
- `## Na prática` — `OrderService` + `OrderRepository` (interface + impl) com `@Inject` por construtor em ```java; bootstrap num runtime CDI (citar Weld como impl de referência, rotulada); contraexemplo: `new OrderService(...)` manual ignorando o container (funciona mas perde escopo/interceptors — teaser 05/13).
- `## Armadilhas` — ≥2: (1) injetar por campo e sofrer pra testar (mock exige reflection) → construtor; (2) ambiguidade com 2 impls do mesmo tipo (`AmbiguousResolutionException`) → qualifier (nota 06); (3) `new` manual em classe gerenciada (sem interceptors/escopo) → deixar o container instanciar.
- `## Em entrevista` + `## Veja também` (01, 05, 06, 13, [[03-Dominios/Java/Linguagem e sintaxe moderna/11 - Annotations|Annotations (Galho 1)]], MOC galho, MOC central, [[03-Dominios/Java/Dicionário de Java#CDI (Contexts and Dependency Injection)|CDI (Dicionário)]], [[03-Dominios/Java/Dicionário de Java#bean (CDI)|bean (Dicionário)]], [[03-Dominios/Java/Dicionário de Java#@Inject|@Inject (Dicionário)]], [[03-Dominios/Java/Dicionário de Java#bean discovery / beans.xml|bean discovery (Dicionário)]]) + `## Referências`.

Tamanho: 240-380 linhas.

- [ ] **Step 3: Verificar**

```bash
grep -E "@Inject|bean discovery|beans.xml|managed bean|Weld|typesafe" "03-Dominios/Java/Jakarta EE/04 - CDI — beans e injeção.md" | head
grep -E "\[\[[^]]*Spring" "03-Dominios/Java/Jakarta EE/04 - CDI — beans e injeção.md"
```
Expected: básico de CDI coberto; **segundo grep VAZIO** (Spring só texto).

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Java/Jakarta EE/04 - CDI — beans e injeção.md"
git commit -m "feat(java): galho 7 nota 04 — CDI, beans e injeção"
```

---

## Fase ADEPTO (notas 05-10)

### Task 5: Nota 05 — CDI — escopos e contextos  ⟦opus⟧

**Files:**
- Create: `03-Dominios/Java/Jakarta EE/05 - CDI — escopos e contextos.md`

- [ ] **Step 1: Pesquisar fonte (usar modelo opus)**

WebFetch `https://jakarta.ee/specifications/cdi/4.1/` (capítulos scopes & contexts) + apidocs `jakarta.enterprise.context`. CONFIRMAR: escopos normais (`@ApplicationScoped`/`@RequestScoped`/`@SessionScoped`/`@ConversationScoped`) vs pseudo-escopo `@Dependent`; client proxy (por que escopos normais exigem proxy; restrições: classe não-final, construtor acessível); lazy instantiation; `@PostConstruct`/`@PreDestroy`.

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: adepto`, tags `[java, jakarta-ee, adepto, cdi]`, aliases `["Escopos CDI", "Client proxy", "@ApplicationScoped"]`.

Conteúdo:
- TL;DR: escopo define QUANDO o container cria e descarta um bean; escopos normais são entregues via **client proxy** — você nunca segura a instância real, e isso tem consequências (final proibido, self-invocation, lazy init).
- `## O que é` — contexts: o ciclo de vida gerenciado; cada escopo = um contexto.
- `## Por que importa` — escopo errado = bug sutil (estado vazando entre requests, ou N instâncias onde se esperava 1); client proxy explica meia dúzia de comportamentos "mágicos" (inclusive do Spring, texto); entrevista adora "por que injetar request-scoped em application-scoped funciona?".
- `## Como funciona` — H3s: "Os escopos normais (`@ApplicationScoped`, `@RequestScoped`, `@SessionScoped`, `@ConversationScoped` — quando cada um)", "`@Dependent` (pseudo-escopo: a instância acompanha quem injetou; sem proxy)", "Client proxy (o mecanismo: o proxy resolve o contexto ativo a cada chamada; por isso request-scoped dentro de application-scoped funciona; restrições — classe não-final, lazy)", "Ciclo de vida (`@PostConstruct`/`@PreDestroy` — quando rodam; construtor NÃO é o lugar de inicialização pesada)", "Escopo ativo e `ContextNotActiveException` (request-scoped fora de request)".
- `## Na prática` — `CartService` `@SessionScoped` injetado em `@ApplicationScoped` (funciona — proxy) em ```java; demonstrar lazy init (`@PostConstruct` só na primeira chamada real); contraexemplo `final class` com escopo normal (deployment error — mostrar a categoria de erro em ```text, conferida na spec/Weld).
- `## Armadilhas` — ≥3: (1) `@Dependent` achando que é singleton (N instâncias, estado "some") → `@ApplicationScoped`; (2) inicialização pesada no construtor (roda na criação do proxy? não — mas roda fora de controle; e proxy ≠ instância) → `@PostConstruct`; (3) `@SessionScoped` sem `Serializable` (passivação pode falhar — conferir exigência na spec) → implementar; (4) acessar bean request-scoped de thread própria (`ContextNotActiveException`) → propagação de contexto não é automática (linka Galho 4 sem re-explicar).
- `## Em entrevista` + `## Veja também` (04, 06, 13, [[03-Dominios/Java/Concorrência e paralelismo/index|Concorrência (Galho 4)]], MOC galho, MOC central, [[03-Dominios/Java/Dicionário de Java#escopo (CDI)|escopo (Dicionário)]], [[03-Dominios/Java/Dicionário de Java#client proxy (CDI)|client proxy (Dicionário)]]) + `## Referências`.

Tamanho: 320-500 linhas (densa; opus).

- [ ] **Step 3: Verificar**

```bash
grep -E "@ApplicationScoped|@RequestScoped|@Dependent|client proxy|@PostConstruct|ContextNotActive" "03-Dominios/Java/Jakarta EE/05 - CDI — escopos e contextos.md" | head
```

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Java/Jakarta EE/05 - CDI — escopos e contextos.md"
git commit -m "feat(java): galho 7 nota 05 — CDI, escopos e contextos"
```

---

### Task 6: Nota 06 — CDI — qualifiers, producers e eventos

**Files:**
- Create: `03-Dominios/Java/Jakarta EE/06 - CDI — qualifiers, producers e eventos.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch `https://jakarta.ee/specifications/cdi/4.1/` (capítulos qualifiers/producers/events) + apidocs `jakarta.enterprise.inject` e `jakarta.enterprise.event`. CONFIRMAR: `@Qualifier` custom + built-in (`@Default`/`@Any`/`@Named`), `@Produces`/`@Disposes`, `Event<T>.fire`/`fireAsync`, `@Observes`/`@ObservesAsync`, transactional observer phases (menção), `@Alternative` (+ `@Priority`), `Instance<T>`.

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: adepto`, tags `[java, jakarta-ee, adepto, cdi]`, aliases `["Qualifiers CDI", "@Produces", "Eventos CDI"]`.

Conteúdo:
- TL;DR: qualifiers desambiguam ("qual dos dois `PaymentGateway`?"); producers fabricam o que o container não cria sozinho (third-party, config); eventos desacoplam emissor de ouvintes — o pub/sub embutido do container.
- `## O que é` — os 3 mecanismos de flexibilidade do CDI sobre a resolução por tipo.
- `## Por que importa` — todo sistema real tem 2+ implementações do mesmo contrato; integrar libs de terceiros é o dia-a-dia; o padrão de eventos é a versão spec do que frameworks oferecem (texto). **Atenção: o `@Produces` do CDI NÃO é o `@Produces` do JAX-RS** (homônimos — desambiguar aqui e na nota 07).
- `## Como funciona` — H3s: "Qualifiers (`@Qualifier` custom; `@Default`/`@Any`; por que `@Named` é pra EL, não pra injeção típica)", "Producers (`@Produces` em método/campo; `@Disposes` pro cleanup; escopo do producer)", "Eventos síncronos (`Event<T>.fire` + `@Observes`; observers ordenados — `@Priority`)", "Eventos assíncronos (`fireAsync` + `@ObservesAsync`; threading — linka Galho 4 sem re-explicar; transactional observers em menção)", "`@Alternative` e `Instance<T>` (trocar impl por configuração; resolução programática/lazy)".
- `## Na prática` — 2 impls de `PaymentGateway` com qualifiers `@Pix`/`@CreditCard` em ```java; producer de objeto de config third-party com disposer; evento `OrderPlaced` com 2 observers (email + auditoria), um síncrono e um async.
- `## Armadilhas` — ≥3: (1) `@Named("x")` como qualifier de injeção (string-based, frágil — é pra EL) → qualifier tipado; (2) producer de recurso caro sem `@Disposes` (leak) → par produce/dispose; (3) observer síncrono lento bloqueando o `fire` (request trava) → `@ObservesAsync` ou trabalho mínimo; (4) confundir os dois `@Produces` (CDI `jakarta.enterprise.inject` × JAX-RS `jakarta.ws.rs`) → conferir o import.
- `## Em entrevista` + `## Veja também` (04, 05, 07 (o outro `@Produces`), 13, MOC galho, MOC central, [[03-Dominios/Java/Dicionário de Java#qualifier (CDI)|qualifier (Dicionário)]], [[03-Dominios/Java/Dicionário de Java#@Produces (producer CDI)|@Produces (Dicionário)]], [[03-Dominios/Java/Dicionário de Java#@Observes / eventos CDI|@Observes (Dicionário)]]) + `## Referências`.

Tamanho: 280-440 linhas.

- [ ] **Step 3: Verificar**

```bash
grep -E "@Qualifier|@Produces|@Disposes|@Observes|fireAsync|@Alternative|Instance<" "03-Dominios/Java/Jakarta EE/06 - CDI — qualifiers, producers e eventos.md" | head
grep -c "JAX-RS" "03-Dominios/Java/Jakarta EE/06 - CDI — qualifiers, producers e eventos.md"
```
Expected: mecanismos cobertos; desambiguação do `@Produces` presente (contagem ≥1).

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Java/Jakarta EE/06 - CDI — qualifiers, producers e eventos.md"
git commit -m "feat(java): galho 7 nota 06 — CDI, qualifiers, producers e eventos"
```

---

### Task 7: Nota 07 — JAX-RS — REST declarativo

**Files:**
- Create: `03-Dominios/Java/Jakarta EE/07 - JAX-RS — REST declarativo.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch `https://jakarta.ee/specifications/restful-ws/4.0/` (spec document/apidocs `jakarta.ws.rs`). CONFIRMAR: `@Path` com templates, verbos (`@GET`/`@POST`/`@PUT`/`@DELETE`), params (`@PathParam`/`@QueryParam`/`@HeaderParam`/`@FormParam`), `@Produces`/`@Consumes` (media types), `Response` builder, `Application`/`@ApplicationPath`, providers (`MessageBodyReader/Writer`, `ExceptionMapper`), Client API (`ClientBuilder`), papel de JSON-B/JSON-P; Jersey (impl de referência) e RESTEasy citadas como impls.

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: adepto`, tags `[java, jakarta-ee, adepto, jax-rs]`, aliases `["JAX-RS", "REST Jakarta", "Jakarta RESTful Web Services"]`.

Conteúdo:
- TL;DR: JAX-RS mapeia HTTP pra métodos Java por annotations — resource classes, params tipados, content negotiation e providers. Sobre a Servlet API por baixo (nota 03); controllers do Spring são outro caminho pro mesmo problema (texto, Galho 9 planejado).
- `## O que é` — a spec REST da plataforma (RESTful Web Services 4.0 no EE 11).
- `## Por que importa` — REST declarativo é o padrão da indústria; o modelo de providers explica "como o JSON vira objeto"; entrevista compara abordagens (spec vs framework — saber a spec é o diferencial).
- `## Como funciona` — H3s: "Resources (`@Path` em classe/método; templates `/orders/{id}`; verbos)", "Params (`@PathParam`/`@QueryParam`/`@HeaderParam` — conversão de tipos)", "Content negotiation (`@Produces`/`@Consumes` com media types — **ATENÇÃO: homônimo do `@Produces` do CDI**, import `jakarta.ws.rs` vs `jakarta.enterprise.inject`; desambiguar com a nota 06)", "Respostas (`Response` builder: status, headers, entity; vs retorno direto)", "Providers (`MessageBodyReader/Writer` — a ponte objeto↔representação; `ExceptionMapper` — exceção→status; JSON-B/JSON-P)", "Bootstrap e Client API (`Application`/`@ApplicationPath`; `ClientBuilder` pra consumir)".
- `## Na prática` — `OrderResource` completo em ```java (GET lista, GET por id com 404 via `ExceptionMapper`, POST com 201 + Location); um `ExceptionMapper<OrderNotFoundException>`; chamada com Client API.
- `## Armadilhas` — ≥3: (1) esquecer `Application`/`@ApplicationPath` (nada responde) → declarar; (2) `ExceptionMapper` que engole a exceção sem log (500 mudo) → logar antes de mapear; (3) import errado do `@Produces` (CDI no lugar do JAX-RS — comportamento silenciosamente errado) → conferir `jakarta.ws.rs.Produces`; (4) retornar entidade JPA crua (acoplamento + lazy issues — nível conceito, sem entrar em fetch) → DTO.
- `## Em entrevista` + `## Veja também` (03, 06, 08, 09, MOC galho, MOC central, [[03-Dominios/Java/Dicionário de Java#JAX-RS (Jakarta RESTful Web Services)|JAX-RS (Dicionário)]], [[03-Dominios/Java/Dicionário de Java#ExceptionMapper|ExceptionMapper (Dicionário)]]) + `## Referências`.

Tamanho: 280-440 linhas.

- [ ] **Step 3: Verificar**

```bash
grep -E "@Path|@GET|@PathParam|@QueryParam|MessageBodyReader|ExceptionMapper|ClientBuilder|@ApplicationPath" "03-Dominios/Java/Jakarta EE/07 - JAX-RS — REST declarativo.md" | head
grep -E "jakarta.ws.rs|jakarta.enterprise.inject" "03-Dominios/Java/Jakarta EE/07 - JAX-RS — REST declarativo.md" | head -5
```
Expected: spec coberta; desambiguação de imports presente.

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Java/Jakarta EE/07 - JAX-RS — REST declarativo.md"
git commit -m "feat(java): galho 7 nota 07 — JAX-RS, REST declarativo"
```

---

### Task 8: Nota 08 — Bean Validation

**Files:**
- Create: `03-Dominios/Java/Jakarta EE/08 - Bean Validation.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch a partir de `https://jakarta.ee/specifications/` → Validation 3.1 (conferir path exato; spec document + apidocs `jakarta.validation`). CONFIRMAR: constraints built-in (lista), onde anotar (campo/getter/parâmetro/retorno; **suporte a record components na 3.1 — verificar**), `@Valid` cascata, custom constraint (`@Constraint(validatedBy=...)` + `ConstraintValidator`), groups, method validation (mecanismo executável — verificar nome exato), comportamento integrado com JAX-RS/CDI, Hibernate Validator como impl de referência (rotular).

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: adepto`, tags `[java, jakarta-ee, adepto, validation]`, aliases `["Bean Validation", "Jakarta Validation", "@Valid"]`.

Conteúdo:
- TL;DR: Bean Validation declara restrições no modelo (annotations) e valida em um ponto só — standalone ou integrada (JAX-RS valida request automaticamente). O `@Valid` do Spring é ESTA spec por baixo (texto, Galho 9 planejado).
- `## O que é` — a spec de validação declarativa (Validation 3.1 no EE 11); Hibernate Validator = impl de referência (rotulada).
- `## Por que importa` — validação espalhada por `if` é o anti-pattern mais comum; declarar no modelo centraliza; entrevista: "onde validar?" e groups.
- `## Como funciona` — H3s: "Constraints built-in (`@NotNull`/`@NotBlank`/`@NotEmpty` — as diferenças; `@Size`/`@Pattern`/`@Min`/`@Max`/`@Email`...)", "Onde anotar (campo/getter/parâmetro/retorno; records — conforme verificado na 3.1)", "Cascata (`@Valid` em campo/elemento de coleção)", "Custom constraints (`@Constraint` + `ConstraintValidator<A, T>`; mensagens e interpolação — menção)", "Groups e sequências (validações por contexto: criação vs atualização)", "Validação standalone vs integrada (`Validator` programático e o `Set<ConstraintViolation>`; method validation com CDI; JAX-RS → 400 automático — conforme verificado)".
- `## Na prática` — `Order` com constraints + `@Valid` em `List<OrderItem>` em ```java; custom constraint `@ValidSku` com validator; uso programático (`Validation.buildDefaultValidatorFactory()` — conferir API) imprimindo violações; resource JAX-RS com `@Valid` no parâmetro (conecta nota 07).
- `## Armadilhas` — ≥3: (1) chamar `validator.validate()` e ignorar o retorno (NÃO lança sozinho fora do container) → checar o Set/lançar; (2) `@NotNull` onde queria `@NotBlank` (string vazia passa) → constraint certa pro tipo; (3) esquecer `@Valid` no aninhado (filhos não validados) → cascata explícita; (4) lógica pesada/IO em `ConstraintValidator` (roda a cada validação) → validador leve, regra de negócio em serviço.
- `## Em entrevista` + `## Veja também` (04, 07, 09, [[03-Dominios/Java/Linguagem e sintaxe moderna/11 - Annotations|Annotations (Galho 1)]], MOC galho, MOC central, [[03-Dominios/Java/Dicionário de Java#Bean Validation (Jakarta Validation)|Bean Validation (Dicionário)]]) + `## Referências`.

Tamanho: 260-400 linhas.

- [ ] **Step 3: Verificar**

```bash
grep -E "@NotNull|@NotBlank|@Valid|ConstraintValidator|ConstraintViolation|groups" "03-Dominios/Java/Jakarta EE/08 - Bean Validation.md" | head
```

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Java/Jakarta EE/08 - Bean Validation.md"
git commit -m "feat(java): galho 7 nota 08 — Bean Validation"
```

---

### Task 9: Nota 09 — JPA — a especificação de persistência  ⟦opus⟧

**Files:**
- Create: `03-Dominios/Java/Jakarta EE/09 - JPA — a especificação de persistência.md`

- [ ] **Step 1: Pesquisar fonte (usar modelo opus)**

WebFetch `https://jakarta.ee/specifications/persistence/3.2/` (spec document + apidocs `jakarta.persistence`). CONFIRMAR: requisitos de `@Entity` (construtor no-args, não-final — conferir exigências exatas na spec 3.2), `@Id`/`@GeneratedValue` (estratégias), `@Column`/`@Table`/`@Transient`, relacionamentos como contrato (`@OneToMany`/`@ManyToOne`/`@ManyToMany`/`@OneToOne`, owning side, `mappedBy`), persistence unit/`persistence.xml`, novidades relevantes da 3.2 (menção honesta — verificar o que mudou).

**FRONTEIRA DURA:** esta nota é o CONTRATO. Fetch strategies/tuning/N+1/caching/Hibernate específico/Spring Data → Galho 10 (planejado, texto). `FetchType` pode ser APRESENTADO como atributo da spec (existe no contrato), sem tuning nem N+1.

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: adepto`, tags `[java, jakarta-ee, adepto, jpa]`, aliases `["JPA", "Jakarta Persistence", "@Entity"]`.

Conteúdo:
- TL;DR: JPA é a SPEC de ORM da plataforma (Persistence 3.2 no EE 11) — define o contrato (`@Entity`, EntityManager, JPQL) que Hibernate e EclipseLink implementam. "JPA não é o Hibernate" é a primeira frase da nota.
- `## O que é` — a especificação; spec vs provider (retoma a nota 01 com o caso concreto mais famoso).
- `## Por que importa` — a confusão JPA×Hibernate é a mais comum do ecossistema; conhecer o contrato te deixa portável e te dá o vocabulário do Galho 10 (planejado, texto); entrevista: "o que é JPA?" é filtro de senioridade.
- `## Como funciona` — H3s: "`@Entity` (requisitos da classe conforme a spec; identidade — `@Id`, `@GeneratedValue` e estratégias como contrato)", "Mapeamento básico (`@Column`/`@Table`/`@Transient`/`@Enumerated`/`@Temporal`-ou-java.time conforme 3.2 — verificar)", "Relacionamentos como vocabulário da spec (`@ManyToOne`/`@OneToMany`(`mappedBy`)/`@ManyToMany`/`@OneToOne`; owning side — quem escreve a FK; `FetchType` como atributo do contrato, SEM tuning — Galho 10)", "Persistence unit (`persistence.xml`: unit, provider, datasource; resource-local vs JTA — teaser 10/11)", "Spec vs provider na prática (o que é portável vs o que é extensão — Hibernate/EclipseLink citadas, não explicadas)".
- `## Na prática` — `Order`/`OrderItem`/`Customer` mapeadas em ```java (entity completa, `@ManyToOne` com owning side comentado); `persistence.xml` mínimo em ```xml; comentário explícito: "o provider (Hibernate/EclipseLink) entra aqui — comportamento além do contrato é assunto do Galho 10 (planejado)".
- `## Armadilhas` — ≥3: (1) entidade sem construtor no-args (provider não instancia) → garantir o construtor; (2) `equals`/`hashCode` com id gerado/campos mutáveis (quebra em Set antes do persist — apresentar o dilema honestamente, sem dogma) → estratégia consciente (id natural, ou identidade só pós-persist); (3) esquecer `mappedBy` (duas tabelas de junção/FK duplicada) → owning side explícito; (4) anotar `@Entity` e esperar que "funcione" sem persistence unit → declarar no `persistence.xml`.
- `## Em entrevista` + `## Veja também` (01, 10, 11, [[03-Dominios/Java/Linguagem e sintaxe moderna/11 - Annotations|Annotations (Galho 1)]], MOC galho, MOC central, [[03-Dominios/Java/Dicionário de Java#JPA (Jakarta Persistence)|JPA (Dicionário)]], [[03-Dominios/Java/Dicionário de Java#entity (JPA)|entity (Dicionário)]], [[03-Dominios/Java/Dicionário de Java#persistence unit / persistence.xml|persistence unit (Dicionário)]]) + `## Referências`.

Tamanho: 320-500 linhas (densa; opus).

- [ ] **Step 3: Verificar**

```bash
grep -E "@Entity|@GeneratedValue|mappedBy|owning side|persistence.xml|provider|EclipseLink" "03-Dominios/Java/Jakarta EE/09 - JPA — a especificação de persistência.md" | head
grep -iE "N\+1|fetch join|cache de segundo nível|Spring Data" "03-Dominios/Java/Jakarta EE/09 - JPA — a especificação de persistência.md"
```
Expected: contrato coberto; **segundo grep VAZIO ou só menção "Galho 10 (planejado)"** (fronteira respeitada).

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Java/Jakarta EE/09 - JPA — a especificação de persistência.md"
git commit -m "feat(java): galho 7 nota 09 — JPA, a especificação de persistência"
```

---

### Task 10: Nota 10 — EntityManager e o ciclo de vida da entidade  ⟦opus⟧

**Files:**
- Create: `03-Dominios/Java/Jakarta EE/10 - EntityManager e o ciclo de vida da entidade.md`

- [ ] **Step 1: Pesquisar fonte (usar modelo opus)**

WebFetch `https://jakarta.ee/specifications/persistence/3.2/` (capítulos EntityManager/entity lifecycle) + apidocs `jakarta.persistence.EntityManager`. CONFIRMAR: persistence context (identidade + unit of work), estados (new/managed/detached/removed) e transições exatas (`persist`/`merge`/`remove`/`find`/`detach`/`refresh`), semântica do `merge` (retorna a managed; o argumento NÃO vira managed), flush (`FlushModeType.AUTO`/`COMMIT`), dirty checking como contrato, JPQL/`TypedQuery` básico, `EntityTransaction` vs JTA, container-managed vs application-managed EntityManager.

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: adepto`, tags `[java, jakarta-ee, adepto, jpa]`, aliases `["EntityManager", "Persistence context", "Ciclo de vida da entidade"]`.

Conteúdo:
- TL;DR: o EntityManager opera um **persistence context** — cache de identidade + unit of work; entidades têm estados (new/managed/detached/removed) e quem entende as transições entende 80% dos "bugs de JPA".
- `## O que é` — a interface central da spec; o persistence context como o conceito por trás.
- `## Por que importa` — `merge` vs `persist`, "por que meu UPDATE não rodou", detached em serialização — todo bug clássico de JPA é transição de estado mal entendida; entrevista cobra o diagrama de estados.
- `## Como funciona` — H3s: "O persistence context (identidade — mesmo id, mesma instância; unit of work — acumula mudanças)", "Os 4 estados e as transições (`persist`/`find`/`merge`/`remove`/`detach`/`refresh` — diagrama ```text)", "A semântica do `merge` (copia estado pra uma managed e a RETORNA; o argumento segue detached)", "Flush e dirty checking (quando o SQL acontece: flush no commit/query/explícito; `FlushModeType`; dirty checking como contrato — o COMO é do provider, Galho 10 planejado)", "JPQL e `TypedQuery` (intro: sintaxe orientada a entidade, parâmetros nomeados; Criteria em menção)", "Quem gerencia o EntityManager (container-managed `@PersistenceContext` vs application-managed; `EntityTransaction` resource-local vs JTA — gancho nota 11)".
- `## Na prática` — sequência completa em ```java: `persist` (managed), mutação sem `update` explícito (dirty checking no commit), `find` + `detach` + mutação (nada acontece — demonstra detached), `merge` usando o RETORNO; JPQL `TypedQuery<Order>` com parâmetro nomeado.
- `## Armadilhas` — ≥3: (1) mutar o argumento do `merge` e descartar o retorno (mudanças no limbo) → usar a entidade retornada; (2) esperar UPDATE sem transação ativa (dirty checking só flusha em transação) → demarcar transação; (3) `LazyInitializationException` conceitual — acessar associação lazy com a entidade detached/contexto fechado (explicar via estados, SEM entrar em fetch tuning — Galho 10 planejado) → acessar dentro do contexto; (4) persistence context inflando em lote (memória + flush caro) → `flush`+`clear` periódicos (nível spec).
- `## Em entrevista` + `## Veja também` (09, 11, MOC galho, MOC central, [[03-Dominios/Java/Dicionário de Java#EntityManager|EntityManager (Dicionário)]], [[03-Dominios/Java/Dicionário de Java#persistence context|persistence context (Dicionário)]], [[03-Dominios/Java/Dicionário de Java#dirty checking|dirty checking (Dicionário)]], [[03-Dominios/Java/Dicionário de Java#JPQL|JPQL (Dicionário)]]) + `## Referências`.

Tamanho: 320-500 linhas (densa; opus).

- [ ] **Step 3: Verificar**

```bash
grep -E "persistence context|managed|detached|merge|flush|dirty checking|TypedQuery" "03-Dominios/Java/Jakarta EE/10 - EntityManager e o ciclo de vida da entidade.md" | head
grep -iE "fetch join|N\+1|Spring Data|Hibernate Session" "03-Dominios/Java/Jakarta EE/10 - EntityManager e o ciclo de vida da entidade.md"
```
Expected: ciclo de vida coberto; **segundo grep VAZIO ou só "Galho 10 (planejado)"**.

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Java/Jakarta EE/10 - EntityManager e o ciclo de vida da entidade.md"
git commit -m "feat(java): galho 7 nota 10 — EntityManager e o ciclo de vida da entidade"
```

---

## Fase MAGUS (notas 11-14)

### Task 11: Nota 11 — JTA — transações na plataforma  ⟦opus⟧

**Files:**
- Create: `03-Dominios/Java/Jakarta EE/11 - JTA — transações na plataforma.md`

- [ ] **Step 1: Pesquisar fonte (usar modelo opus)**

WebFetch `https://jakarta.ee/specifications/transactions/2.0/` (spec document + apidocs `jakarta.transaction`). CONFIRMAR: `UserTransaction` (begin/commit/rollback), `@Transactional` do `jakarta.transaction` (valores de `TxType`: `REQUIRED`/`REQUIRES_NEW`/`MANDATORY`/`SUPPORTS`/`NOT_SUPPORTED`/`NEVER`), regra de rollback (runtime vs checked — `rollbackOn`/`dontRollbackOn`; conferir default exato na spec), `@TransactionScoped`, papel do transaction manager, relação com XA/2PC (conceito; a spec JTA mapeia pra X/Open XA — confirmar framing honesto).

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: magus`, tags `[java, jakarta-ee, magus, jta]`, aliases `["JTA", "Jakarta Transactions", "@Transactional Jakarta"]`.

Conteúdo:
- TL;DR: JTA é a spec que coordena transações na plataforma — declarativa (`@Transactional`, via interceptor CDI) ou programática (`UserTransaction`); pra múltiplos recursos entra XA/two-phase commit. O `@Transactional` do Spring é outra annotation pro mesmo problema (texto, Galhos 8/10 planejados).
- `## O que é` — a spec de demarcação e coordenação de transações (Transactions 2.0 no EE 11). **Desambiguação imediata:** `jakarta.transaction.Transactional` ≠ `org.springframework...Transactional` (texto).
- `## Por que importa` — transação é onde bug vira prejuízo; o modelo CMT/BMT explica o que TODO framework declarativo faz por baixo; XA/2PC é pergunta de system design.
- `## Como funciona` — H3s: "O problema (atomicidade entre operações; quem coordena: o container)", "Programático — BMT (`UserTransaction`: begin/commit/rollback; quando o controle manual vale)", "Declarativo — CMT (`@Transactional` + `TxType` — semântica de cada um; implementado como interceptor CDI → gancho nota 13)", "Rollback (a regra da spec pra unchecked vs checked — conforme verificado; `rollbackOn`/`dontRollbackOn`; `setRollbackOnly`)", "`@TransactionScoped` (bean vivo durante a transação)", "XA e two-phase commit (2 recursos: prepare → commit; o coordinator; o custo — latência/bloqueio; quando 2PC vs padrões alternativos — menção honesta, sem aprofundar mensageria → Galho 14 planejado)".
- `## Na prática` — serviço com `@Transactional(REQUIRED)` chamando repositório JPA em ```java; um `REQUIRES_NEW` pra auditoria que sobrevive a rollback; BMT com `UserTransaction` em bloco try/catch completo; demonstrar self-invocation não passando pelo interceptor (conecta 05/13).
- `## Armadilhas` — ≥3: (1) self-invocation de método `@Transactional` (interceptor não roda — proxy!) → chamar via referência injetada/repensar o desenho; (2) assumir rollback automático em checked exception (default da spec — conforme verificado) → `rollbackOn` explícito; (3) misturar BMT e CMT no mesmo componente (comportamento indefinido/confuso) → um modelo por componente; (4) `REQUIRES_NEW` em cascata sem perceber (transações aninhadas independentes — commit parcial inesperado) → mapear os limites.
- `## Em entrevista` + `## Veja também` (05, 10, 13, [[03-Dominios/Java/Concorrência e paralelismo/index|Concorrência (Galho 4)]], MOC galho, MOC central, [[03-Dominios/Java/Dicionário de Java#JTA (Jakarta Transactions)|JTA (Dicionário)]], [[03-Dominios/Java/Dicionário de Java#@Transactional (Jakarta)|@Transactional (Dicionário)]], [[03-Dominios/Java/Dicionário de Java#CMT / BMT|CMT / BMT (Dicionário)]], [[03-Dominios/Java/Dicionário de Java#two-phase commit (2PC / XA)|two-phase commit (Dicionário)]]) + `## Referências`.

Tamanho: 300-460 linhas (densa; opus).

- [ ] **Step 3: Verificar**

```bash
grep -E "UserTransaction|@Transactional|REQUIRES_NEW|rollback|two-phase|XA|TransactionScoped" "03-Dominios/Java/Jakarta EE/11 - JTA — transações na plataforma.md" | head
grep -E "\[\[[^]]*Spring" "03-Dominios/Java/Jakarta EE/11 - JTA — transações na plataforma.md"
```
Expected: spec coberta; **segundo grep VAZIO**.

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Java/Jakarta EE/11 - JTA — transações na plataforma.md"
git commit -m "feat(java): galho 7 nota 11 — JTA, transações na plataforma"
```

---

### Task 12: Nota 12 — EJB — o legado que moldou a plataforma

**Files:**
- Create: `03-Dominios/Java/Jakarta EE/12 - EJB — o legado que moldou a plataforma.md`

- [ ] **Step 1: Pesquisar fonte — VERIFICAÇÃO DE STATUS OBRIGATÓRIA**

WebFetch `https://jakarta.ee/specifications/enterprise-beans/4.0/`. CONFIRMAR: o que a spec 4.0 contém (session beans, MDB, timer service; o que foi removido/podado no Jakarta — entity beans/CMP? conferir), status real (4.0 atual, 4.1 "under development" — sinais verificáveis, sem editorializar além da fonte), relação com CDI (o que migrou conceitualmente). **Mesma regra da capstone do Galho 5: separar status oficial de consenso de-facto da comunidade, com fonte; ZERO estatística de adoção.**

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: magus`, tags `[java, jakarta-ee, magus, ejb]`, aliases `["EJB", "Enterprise JavaBeans", "Session beans"]`.

Conteúdo:
- TL;DR: EJB foi O modelo de componente enterprise por uma década — transações, segurança e remoting declarativos quando nada mais oferecia; o peso do EJB 2.x gerou a reação (Spring, e depois a própria simplificação no EJB 3); hoje a spec é estável (4.0), o CDI absorveu o papel central, e você encontra EJB em legados.
- `## O que é` — o modelo de componentes server-side da plataforma; visão histórica honesta.
- `## Por que importa` — legados corporativos EXISTEM (manutenção e migração são trabalho real de senior); a história explica POR QUE CDI/Spring são como são; entrevista: "EJB vs CDI?" testa maturidade histórica.
- `## Como funciona` — H3s: "Ascensão (J2EE: o que o EJB resolvia — transações/segurança/pooling/remoting declarativos)", "O peso do 2.x (home interfaces, descritores XML, entity beans/CMP — por que doía; a reação da comunidade, Spring citado como contexto histórico em texto)", "A simplificação do 3.x (annotations, POJOs — convergência com a ideia que virou CDI)", "Os tipos hoje (stateless/stateful/singleton session beans; MDB — menção, mensageria é Galho 14 planejado; timer service)", "EJB × CDI (o que o CDI absorveu — DI/escopos/interceptors; o que ainda é exclusivo de EJB conforme a spec 4.0 verificada; status: 4.0 estável, sinais verificáveis sem editorializar)".
- `## Na prática` — `@Stateless` com `@Schedule` (timer) em ```java como exemplo do que se encontra em legado; o equivalente moderno em CDI (+`@Transactional`) lado a lado — comparação justa: o que se ganha, o que se perde.
- `## Armadilhas` (de raciocínio) — ≥3: (1) tratar EJB como sinônimo de "Java enterprise moderno" (currículo/fala desatualizados) → vocabulário atual (CDI/specs); (2) reescrever EJB estável sem business case (custo/risco sem payoff) → migrar com motivo concreto; (3) confundir entity beans (CMP, mortos) com JPA entities (vivíssimas) → são histórias diferentes; (4) descartar conhecimento de EJB em entrevista pra vaga com legado (é diferencial) → honestidade sobre o stack.
- `## Em entrevista` + `## Veja também` (04, 11, 13, 14, MOC galho, MOC central, [[03-Dominios/Java/Dicionário de Java#EJB (Enterprise JavaBeans)|EJB (Dicionário)]], [[03-Dominios/Java/Dicionário de Java#session bean|session bean (Dicionário)]], [[03-Dominios/Java/Dicionário de Java#MDB (message-driven bean)|MDB (Dicionário)]]) + `## Referências`.

Tamanho: 260-400 linhas.

- [ ] **Step 3: Verificar**

```bash
grep -E "stateless|stateful|singleton|MDB|timer|home interface|entity bean" "03-Dominios/Java/Jakarta EE/12 - EJB — o legado que moldou a plataforma.md" | head
grep -riE "% d[ao]s|market share|maioria das empresas" "03-Dominios/Java/Jakarta EE/12 - EJB — o legado que moldou a plataforma.md"
```
Expected: história + tipos cobertos; **segundo grep VAZIO** (zero estatística).

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Java/Jakarta EE/12 - EJB — o legado que moldou a plataforma.md"
git commit -m "feat(java): galho 7 nota 12 — EJB, o legado que moldou a plataforma"
```

---

### Task 13: Nota 13 — CDI avançado — interceptors, decorators e extensões

**Files:**
- Create: `03-Dominios/Java/Jakarta EE/13 - CDI avançado — interceptors, decorators e extensões.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch `https://jakarta.ee/specifications/cdi/4.1/` (capítulos interceptors/decorators/SPI; seção CDI Full vs CDI Lite) + apidocs `jakarta.interceptor`/`jakarta.decorator`. CONFIRMAR: `@InterceptorBinding` custom, `@Interceptor` + `@AroundInvoke` + `InvocationContext`, ativação (`@Priority` vs `beans.xml`), `@Decorator`/`@Delegate`, portable extensions (eventos de container — `ProcessAnnotatedType` etc., panorama), build compatible extensions (CDI Lite/Core Profile — o motivo build-time; em qual versão entraram — conferir: CDI 4.0?).

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: magus`, tags `[java, jakarta-ee, magus, cdi]`, aliases `["Interceptors CDI", "Decorators CDI", "CDI Lite"]`.

Conteúdo:
- TL;DR: interceptors são o AOP da plataforma — **é assim que `@Transactional` funciona por baixo** (nota 11); decorators decoram contratos de negócio; extensões plugam no próprio container. CDI Lite (Core Profile) move isso pra build-time.
- `## O que é` — os mecanismos de meta-programação do CDI.
- `## Por que importa` — desmistifica a "mágica" dos frameworks (cross-cutting declarativo = interceptor + binding); entrevista de senior: "como você implementaria um `@Audited`?"; Lite vs Full explica a nova geração de runtimes (texto, sem explicar Quarkus).
- `## Como funciona` — H3s: "Interceptor bindings (`@InterceptorBinding` custom — ex.: `@Audited`; o trio binding + interceptor + uso)", "`@AroundInvoke` e `InvocationContext` (proceed, metadados, alterar argumentos/retorno; `@AroundConstruct` em menção)", "Ativação e ordem (`@Priority` vs `beans.xml`; a armadilha clássica do interceptor que 'não roda')", "Decorators (`@Decorator` + `@Delegate` — decora um contrato de NEGÓCIO conhecendo-o; vs interceptor, que é cego ao contrato; quando cada um)", "Portable extensions (panorama: observar eventos de container — `ProcessAnnotatedType`...; o que frameworks fazem com isso; NÃO é tutorial de SPI)", "CDI Full vs CDI Lite (build compatible extensions; por que build-time — startup/native; Core Profile — conecta notas 01 e 14)".
- `## Na prática` — trio completo `@Audited` em ```java (binding + interceptor com `@AroundInvoke` logando + serviço anotado); um decorator de `PriceCalculator` aplicando desconto; lembrar self-invocation (conecta 05/11).
- `## Armadilhas` — ≥3: (1) interceptor sem ativação (`@Priority`/`beans.xml` — anotou e "não roda") → ativar e conferir; (2) self-invocation não interceptada (proxy de novo — 05/11) → desenho; (3) lógica de negócio em interceptor (esconde regra em infraestrutura) → interceptor pra cross-cutting, negócio em serviço/decorator; (4) decorator onde interceptor bastava (acopla ao contrato sem necessidade) → decorator só quando a lógica PRECISA do domínio.
- `## Em entrevista` + `## Veja também` (04, 05, 06, 11, 14, MOC galho, MOC central, [[03-Dominios/Java/Dicionário de Java#interceptor (CDI)|interceptor (Dicionário)]], [[03-Dominios/Java/Dicionário de Java#decorator (CDI)|decorator (Dicionário)]], [[03-Dominios/Java/Dicionário de Java#portable extension (CDI)|portable extension (Dicionário)]]) + `## Referências`.

Tamanho: 280-440 linhas.

- [ ] **Step 3: Verificar**

```bash
grep -E "@InterceptorBinding|@AroundInvoke|InvocationContext|@Priority|@Decorator|@Delegate|Lite" "03-Dominios/Java/Jakarta EE/13 - CDI avançado — interceptors, decorators e extensões.md" | head
```

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Java/Jakarta EE/13 - CDI avançado — interceptors, decorators e extensões.md"
git commit -m "feat(java): galho 7 nota 13 — CDI avançado (interceptors, decorators e extensões)"
```

---

### Task 14: Nota 14 — Jakarta EE hoje — a plataforma sob o Spring  ⟦opus⟧ (capstone)

**Files:**
- Create: `03-Dominios/Java/Jakarta EE/14 - Jakarta EE hoje — a plataforma sob o Spring.md`

- [ ] **Step 1: Pesquisar fonte — VERIFICAÇÃO OBRIGATÓRIA (estado/governança)**

WebFetch `https://jakarta.ee/release/` + `https://jakarta.ee/specifications/platform/11/` + `https://jakarta.ee/about/` (working group/EFSP — navegar se preciso). CONFIRMAR no dia da execução: EE 11 segue atual (26/jun/2025) e EE 12 em desenvolvimento; o que o Core Profile contém; processo (Jakarta EE Working Group, EFSP, TCK); runtimes que consomem as specs (Quarkus/Open Liberty/Helidon — confirmar a relação com Core Profile/CDI Lite via fontes navegáveis; 1 linha cada, sem explicar nenhum); MicroProfile (relação com Jakarta EE — governança Eclipse, complemento cloud-native; menção). **ZERO estatística de adoção** — sinais verificáveis (releases, specs ativas, runtimes certificados), não market share.

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: magus`, tags `[java, jakarta-ee, magus, sintese, especificacao]`, aliases `["Jakarta EE hoje", "Jakarta EE vs Spring", "Estado do Jakarta EE"]`.

Conteúdo (capstone — fecha a tese do galho):
- TL;DR: Jakarta EE está ativo (EE 11/2025, EE 12 em dev, cadência Eclipse) e é a FUNDAÇÃO invisível do ecossistema — o Spring implementa/consome/abstrai as specs, e a nova geração (via Core Profile) as usa direto. Saber a spec é entender o que TODO framework esconde.
- `## O que é` — o estado da plataforma + o framework de decisão.
- `## Por que importa` — "Jakarta EE morreu?" é meia-verdade de blog antigo; a resposta com datas e specs é diferencial de entrevista; a tabela spec→Spring é o mapa mental do bloco enterprise da trilha (Galhos 8-10, planejados).
- `## Como funciona` — H3s:
  - "Governança e cadência (Eclipse Foundation, Working Group, EFSP, TCK; EE 11 em jun/2025; EE 12 em desenvolvimento — verificado)" com datas/fontes.
  - "Os 3 perfis e o papel estratégico do Core Profile (specs mínimas — CDI Lite, REST...; a ponte pra runtimes cloud-native: Quarkus/Open Liberty/Helidon em 1 linha cada, citados sem explicar)".
  - "MicroProfile (1 parágrafo: complemento cloud-native sob a Eclipse, governança própria; menção honesta)".
  - "A tese do galho: o que o Spring esconde (tabela spec → feature Spring: CDI→DI/`@Autowired`; Servlet→o chão do Spring MVC; JAX-RS→alternativa aos controllers REST; Bean Validation→`@Valid`; JPA→base do Spring Data JPA; JTA→`@Transactional` — **lado Spring SÓ nomes**, Galhos 8/9/10 planejados, sem wikilink)".
  - "Plataforma pura vs framework (quando Jakarta puro faz sentido: padronização/portabilidade/app server existente; quando framework: ecossistema/produtividade/contratação — comparação justa, sem dogma)".
  - "O que o senior responde (frame de decisão, não torcida)".
- `## Na prática` — 2-3 cenários hipotéticos explícitos: manter sistema WildFly/Jakarta existente (ficar e modernizar dentro da plataforma); serviço novo em time Spring (framework — e saber as specs por baixo te faz melhor nele); produto cloud-native enxuto (runtime moderno sobre Core Profile).
- `## Armadilhas` (de raciocínio) — ≥3: (1) "Jakarta EE morreu" (EE 11 é de 2025; as specs fundam o ecossistema inteiro) → checar releases; (2) "Spring substituiu as specs" (ele as implementa/consome em várias áreas — saber a spec é vantagem, não arqueologia) → tabela da tese; (3) decidir plataforma por ideologia (specs "puras" vs framework "prático") em vez de requisito → contexto decide; (4) citar estatística de adoção de blog → sinais verificáveis.
- `## Em entrevista` + `### Cheatsheet do galho` — tabela "qual nota pra qual problema" (spec vs impl→01, migração javax→02, HTTP base→03, DI→04, escopos→05, qualifiers/eventos→06, REST→07, validação→08, ORM contrato→09, estados da entidade→10, transações→11, legado→12, AOP/extensões→13) com wikilinks.
- `## Veja também` — (01, 02, 04, 13, [[03-Dominios/Java/index|Trilha Java]], MOC galho, [[03-Dominios/Java/Dicionário de Java#Jakarta EE|Jakarta EE (Dicionário)]], [[03-Dominios/Java/Dicionário de Java#Core Profile|Core Profile (Dicionário)]]) + `## Referências`.

Tamanho: 320-500 linhas (fechamento; opus).

- [ ] **Step 3: Verificar**

```bash
grep -iE "EE 11|EE 12|Core Profile|MicroProfile|cheatsheet|TCK" "03-Dominios/Java/Jakarta EE/14 - Jakarta EE hoje — a plataforma sob o Spring.md" | head
grep -riE "minha experiência|no meu projeto|josenaldo|Patient|% d[ao]s|market share" "03-Dominios/Java/Jakarta EE/14 - Jakarta EE hoje — a plataforma sob o Spring.md"
grep -E "\[\[[^]]*(Spring|Quarkus|Hibernate)" "03-Dominios/Java/Jakarta EE/14 - Jakarta EE hoje — a plataforma sob o Spring.md"
```
Expected: estado + tese cobertos; **segundo e terceiro greps VAZIOS**.

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Java/Jakarta EE/14 - Jakarta EE hoje — a plataforma sob o Spring.md"
git commit -m "feat(java): galho 7 nota 14 — Jakarta EE hoje (capstone)"
```

---

## Task 15: MOC do galho

**Files:**
- Create: `03-Dominios/Java/Jakarta EE/index.md`

- [ ] **Step 1: Escrever o MOC**

Frontmatter: `type: moc`, `status: growing`, `publish: true`, `title: "Jakarta EE"`, tags `[java, jakarta-ee, moc]`, aliases `["Galho 7 - Jakarta EE", "Java EE (galho)"]`, `created`/`updated: 2026-06-07`. (Alias "Jakarta EE" NÃO — colide com o verbete do Dicionário e o title já cobre; conferir padrão dos MOCs 5/6.)

Conteúdo (modelar pelo `03-Dominios/Java/JavaFX/index.md`):
- TL;DR — Galho 7; a plataforma de specs enterprise que o Spring abstrai: spec vs impl, transição javax→jakarta, Servlet, CDI (4 notas), JAX-RS, Bean Validation, JPA spec, JTA, EJB, estado atual; 14 notas em 3 fases.
- `## Sobre este galho` — escopo + audiência + **galho de pesquisa** (sem tronco; notas nascidas de jakarta.ee/spec documents) + fronteiras (Spring → Galho 8/9/10 planejados, texto; JPA operacional → Galho 10; annotations → Galho 1; concorrência → Galho 4).
- `## Iniciado` (01-04) / `## Adepto` (05-10) / `## Magus` (11-14) — wikilinks + 1 linha cada.
- `## Rotas alternativas` — 5:
  - **Completa** — 01 → 14.
  - **Entrevista internacional** — 01 → 02 → 04 → 09 → 10 → 11 → 14.
  - **O que o Spring esconde** — 04 → 05 → 06 → 13 → 14.
  - **REST do zero na plataforma** — 03 → 04 → 07 → 08.
  - **Persistência e transações** — 09 → 10 → 11.
- `## Todas as notas` — Dataview (`FROM "03-Dominios/Java/Jakarta EE"`, `WHERE type = "concept"`).
- `## Veja também` — MOC central, Galhos 1/2/3/4 (index), Dicionário; Galhos 8/9/10 como texto "(planejado)" SEM wikilink.

- [ ] **Step 2: Verificar**

```bash
grep -cE "^## (Iniciado|Adepto|Magus|Rotas alternativas)" "03-Dominios/Java/Jakarta EE/index.md"
grep -c "\[\[" "03-Dominios/Java/Jakarta EE/index.md"
grep -E "\[\[[^]]*Spring" "03-Dominios/Java/Jakarta EE/index.md"
```
Expected: 4 headings; ≥14 wikilinks; **último grep VAZIO**.

- [ ] **Step 3: Commit**

```bash
git add "03-Dominios/Java/Jakarta EE/index.md"
git commit -m "feat(java): galho 7 MOC — Jakarta EE"
```

---

## Task 16: Expandir o Dicionário de Java (NÃO recriar)

**Files:**
- Modify: `03-Dominios/Java/Dicionário de Java.md`

- [ ] **Step 1: Extrair as âncoras realmente usadas**

```bash
grep -rhoE "Dicionário de Java#[^]|]+" "03-Dominios/Java/Jakarta EE/" | sort -u
```
Lista esperada (~35; ajustar AO GREP — a fonte da verdade é o que as notas usaram): `@Inject`, `@Observes / eventos CDI`, `@Produces (producer CDI)`, `@Transactional (Jakarta)`, `bean (CDI)`, `bean discovery / beans.xml`, `Bean Validation (Jakarta Validation)`, `CDI (Contexts and Dependency Injection)`, `client proxy (CDI)`, `CMT / BMT`, `Core Profile`, `decorator (CDI)`, `dirty checking`, `EJB (Enterprise JavaBeans)`, `entity (JPA)`, `EntityManager`, `escopo (CDI)`, `ExceptionMapper`, `interceptor (CDI)`, `Jakarta EE`, `JAX-RS (Jakarta RESTful Web Services)`, `javax → jakarta (rename)`, `JPA (Jakarta Persistence)`, `JPQL`, `JTA (Jakarta Transactions)`, `MDB (message-driven bean)`, `persistence context`, `persistence unit / persistence.xml`, `portable extension (CDI)`, `qualifier (CDI)`, `servlet`, `servlet container`, `session bean`, `two-phase commit (2PC / XA)`, `Web Profile`.

- [ ] **Step 2: Ler o Dicionário inteiro e conferir duplicatas**

Formato `### Termo` + 1-3 linhas + `Veja também:`. **NÃO recriar/reordenar.** Conferir colisões com verbetes dos Galhos 1-6 (ex.: termos de annotations são do Galho 1; se algum verbete Jakarta já existir por engano, atualizar em vez de duplicar).

- [ ] **Step 3: Inserir em ordem alfabética** (case-insensitive, sem acento; verbetes iniciados em `@` entram na seção da letra seguinte — conferir o padrão usado no arquivo; criar seções se preciso). Cada verbete: heading EXATO da âncora + definição fiel às notas + `Veja também:` pra nota canônica (CDI básico→04; escopos/client proxy→05; qualifier/@Produces/@Observes→06; JAX-RS/ExceptionMapper→07; Bean Validation→08; JPA/entity/persistence unit→09; EntityManager/persistence context/dirty checking/JPQL→10; JTA/@Transactional/CMT-BMT/2PC→11; EJB/session bean/MDB→12; interceptor/decorator/portable extension→13; Jakarta EE/perfis→01; javax→jakarta→02; servlet/container→03). Atualizar `updated: 2026-06-07`.

- [ ] **Step 4: Verificar**

```bash
grep -E "^### (Jakarta EE|CDI \(Contexts and Dependency Injection\)|EntityManager|JPQL|servlet|Web Profile)" "03-Dominios/Java/Dicionário de Java.md"
grep -cE "^### " "03-Dominios/Java/Dicionário de Java.md"
```
Expected: novos presentes; contagem subiu ~35 vs baseline da Task 0 Step 6 (166 → ~201).

- [ ] **Step 5: Commit**

```bash
git add "03-Dominios/Java/Dicionário de Java.md"
git commit -m "feat(java): expande Dicionário de Java com verbetes do galho 7 (Jakarta EE)"
```

---

## Task 17: Ativar o Galho 7 no MOC central

**Files:**
- Modify: `03-Dominios/Java/index.md`

- [ ] **Step 1: Trocar a linha do item 7** (localizar por conteúdo: `7. Jakarta EE *(planejado)* — CDI, Servlet, JAX-RS, Bean Validation, JPA spec, JTA`) por:

```markdown
7. [[03-Dominios/Java/Jakarta EE/index|Jakarta EE]] — spec vs implementação, transição javax→jakarta, Servlet, CDI, JAX-RS, Bean Validation, JPA spec, JTA, legado EJB, estado atual da plataforma
```

Atualizar `updated: 2026-06-07`. Não mexer no resto.

- [ ] **Step 2: Verificar**

```bash
grep -E "Jakarta EE/index" "03-Dominios/Java/index.md"
grep -c "planejado" "03-Dominios/Java/index.md"
```
Expected: wikilink ativo; "planejado" caiu exatamente 1 vs baseline.

- [ ] **Step 3: Commit**

```bash
git add "03-Dominios/Java/index.md"
git commit -m "feat(java): ativa Galho 7 (Jakarta EE) no MOC central"
```

---

## Task 18: Quitar a dívida reversa (ponteiros "Galho 7" → wikilinks; corrigir atribuição CDI)

**Files:**
- Modify: `03-Dominios/Java/Linguagem e sintaxe moderna/11 - Annotations.md`
- Modify: `03-Dominios/Java/JavaFX/11 - Arquitetura — MVC, MVVM e injeção de dependência.md`

- [ ] **Step 1: Relocalizar (por conteúdo — linhas podem ter mudado)**

```bash
grep -n "Galhos 7 e 8" "03-Dominios/Java/Linguagem e sintaxe moderna/11 - Annotations.md"
grep -n "Galho 8" "03-Dominios/Java/JavaFX/11 - Arquitetura — MVC, MVVM e injeção de dependência.md"
grep -n "Bean Validation" "03-Dominios/Java/Linguagem e sintaxe moderna/11 - Annotations.md"
```

- [ ] **Step 2: Annotations.md (~linha 309)** — trocar o trecho `Este é o ponto de conexão com os **Galhos 7 e 8** (Spring e Jakarta EE).` por:

```markdown
Este é o ponto de conexão com o galho [[03-Dominios/Java/Jakarta EE/index|Jakarta EE]] (CDI, JPA, Bean Validation — specs construídas sobre annotations RUNTIME) e com o Galho 8 (Spring, planejado).
```

Opcional, se natural: na linha ~383 (menção a Bean Validation), linkar `[[03-Dominios/Java/Jakarta EE/08 - Bean Validation|Bean Validation]]`. Atualizar `updated: 2026-06-07` no frontmatter.

- [ ] **Step 3: JavaFX/11 (~linhas 35 e 110)** — **corrigir a atribuição** (CDI é do Galho 7, não do 8):
- Linha ~35: trocar `(Guice, Weld, ou frameworks de terceiros como mvvmFX; Spring/CDI ficam para o Galho 8, planejado)` por `(Guice, Weld, ou frameworks de terceiros como mvvmFX; [[03-Dominios/Java/Jakarta EE/04 - CDI — beans e injeção|CDI]] tem galho próprio; Spring fica para o Galho 8, planejado)`.
- Linha ~110: trocar `Weld/CDI e outros containers ficam para o Galho 8 (planejado)` por `Weld/[[03-Dominios/Java/Jakarta EE/04 - CDI — beans e injeção|CDI]] têm galho próprio; Spring fica para o Galho 8 (planejado)`.
- Ajustar o fraseado mínimo necessário pra frase continuar natural; atualizar `updated: 2026-06-07`.

- [ ] **Step 4: Verificar**

```bash
grep -n "Galhos 7 e 8" "03-Dominios/Java/Linguagem e sintaxe moderna/11 - Annotations.md"
grep -n "CDI ficam para o Galho 8\|CDI e outros containers ficam" "03-Dominios/Java/JavaFX/11 - Arquitetura — MVC, MVVM e injeção de dependência.md"
grep -c "Jakarta EE" "03-Dominios/Java/JavaFX/11 - Arquitetura — MVC, MVVM e injeção de dependência.md"
```
Expected: dois primeiros greps **VAZIOS** (ponteiros antigos eliminados); terceiro ≥1 (wikilinks novos).

- [ ] **Step 5: Commit**

```bash
git add "03-Dominios/Java/Linguagem e sintaxe moderna/11 - Annotations.md" "03-Dominios/Java/JavaFX/11 - Arquitetura — MVC, MVVM e injeção de dependência.md"
git commit -m "refactor(java): quita dívida reversa do galho 7 — ponteiros Jakarta/CDI viram wikilinks"
```

---

## Task 19: Verificação final do galho

**Files:** (somente leitura/verificação)

- [ ] **Step 1: 14 notas + MOC**

```bash
ls "03-Dominios/Java/Jakarta EE/" | sort
```
Expected: 01..14 + index.md (15 arquivos).

- [ ] **Step 2: Fases (4/6/4)**

```bash
for f in "03-Dominios/Java/Jakarta EE/"[0-9]*.md; do grep -H "^fase:" "$f"; done
```
Expected: 01-04 `iniciado`, 05-10 `adepto`, 11-14 `magus`.

- [ ] **Step 3: Seções obrigatórias (3 por nota)**

```bash
for f in "03-Dominios/Java/Jakarta EE/"[0-9]*.md; do echo "$f: $(grep -cE '^## (Em entrevista|Armadilhas|Veja também)' "$f")"; done
```
Expected: 3 em todas.

- [ ] **Step 4: Anti-fabricação + fronteiras (greps decisivos)**

```bash
grep -riE "minha experiência|no meu projeto|josenaldo|Patient|getSpecialty|market share|% d[ao]s" "03-Dominios/Java/Jakarta EE/"
grep -rE "\[\[[^]]*(Spring|Hibernate|Quarkus|EclipseLink|Kafka|Galho (8|9|10|14))" "03-Dominios/Java/Jakarta EE/"
grep -rn '\[\[#' "03-Dominios/Java/Jakarta EE/"
grep -rn "import javax" "03-Dominios/Java/Jakarta EE/" | grep -v "02 - De Java EE a Jakarta EE"
```
Expected: **todos VAZIOS** (o 4º tolera `javax` SÓ na nota 02).

- [ ] **Step 5: Frase pronta (1 por nota)**

```bash
for f in "03-Dominios/Java/Jakarta EE/"[0-9]*.md; do echo "$f: $(grep -c '### Frase pronta (inglês)' "$f")"; done
```

- [ ] **Step 6: Troncos intocados**

```bash
git log --oneline -5 -- "03-Dominios/Java/Backend/"
git status --short "03-Dominios/Java/Backend/"
```
Expected: nenhum commit novo deste galho em `Backend/`; working tree limpa ali.

- [ ] **Step 7: Skill `verificar-wikilinks`**

Rodar na pasta `03-Dominios/Java/Jakarta EE/` + conferir os arquivos tocados fora (MOC central, Dicionário, Annotations.md, JavaFX/11). Âncoras `Dicionário de Java#...` resolvem 1:1 (cross-check com o grep da Task 16 Step 1). As ~204 quebras legadas da árvore Java NÃO são deste galho — só corrigir o que este galho introduziu. Corrigir e commitar à parte se houver.

- [ ] **Step 8: Resumo de fechamento (sem commit)** — reportar: 14 notas (4/6/4), ~35 verbetes, MOC + MOC central, dívida reversa quitada (incluindo a correção CDI no JavaFX/11), troncos intocados (mostrar o grep), wikilinks limpos. Commits locais na `main`; **push manual do usuário; sem deploy**. Atualizar memória [[project_trilha_java]] com status e fatos cravados (EE 11 jun/2025, versões das specs).

---

## Self-Review (preenchido na escrita do plano)

**Spec coverage:** Tasks 1-14 ↔ spec §3.1 (14 notas, escopos idênticos, opus 05/09/10/11/14); Task 15 ↔ §3.2 (MOC, 5 rotas iguais); Task 16 ↔ §3.3 (~35 verbetes, âncoras 1:1 por grep); Task 17 ↔ §3.4 (linha 37); **sem task de poda** ↔ §3.5 (galho de pesquisa; Task 19 Step 6 garante troncos intocados); Task 18 ↔ §3.6 (incluindo a correção de atribuição CDI no JavaFX/11); Task 0 ↔ §6 (pré-flight, baseline 166, versões cravadas); Task 19 ↔ §7. Fronteira Spring (§4.3.1) garantida por greps nas Tasks 1/4/11/14/15 e no grep global da Task 19 Step 4.

**Placeholder scan:** sem TBD/TODO; cada nota tem fonte nomeada com URL, frontmatter concreto, H3s, armadilhas mínimas com conteúdo real, tamanho-alvo. Pontos version-sensitive marcados com "verificar/conferir" são instruções de verificação WebFetch (galho de pesquisa), não placeholders: path da spec Validation, suporte a records na 3.1, default de rollback na JTA, conteúdo exato do Core Profile, o que a EJB 4.0 removeu, versão de entrada das build compatible extensions.

**Type/naming consistency:** numeração 01-14 idêntica entre tasks, MOC, Dicionário, dívida reversa e cheatsheet da capstone; distribuição 4/6/4 consistente; opus 05/09/10/11/14 marcadas ⟦opus⟧; filenames com em dash (sem `:`/`/`); títulos vizinhos (Linguagem 11, Collections 04, JVM 08, Concorrência 02/08) reconfirmados na Task 0 Step 4; âncoras do Dicionário extraídas por grep antes de inserir (Task 16) e validadas na Task 19; homônimo `@Produces` desambiguado com verbetes distintos (`@Produces (producer CDI)` vs nota 07 usando o contexto JAX-RS sem verbete próprio de mesmo nome).
