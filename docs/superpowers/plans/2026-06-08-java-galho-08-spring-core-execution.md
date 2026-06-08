# Galho 8 — Spring Core e Boot (Java Senior) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Criar o Galho 8 da trilha Java Senior — 18 notas atômicas (Spring/Boot, IoC/DI, beans/estereótipos, injeção, `@Configuration`, ApplicationContext, lifecycle/escopos, qualificação, AOP, self-invocation, eventos, config/profiles, post-processors, conditional, auto-config, SpringApplication, Actuator, capstone) em 3 fases + MOC do galho + expansão do Dicionário + ativação do MOC central + **poda parcial** do tronco `Backend/Spring Boot.md` + **quitação de 9 ganchos de dívida reversa**.

**Architecture:** Padrão galhos + 3 fases (Iniciado/Adepto/Magus). Pasta flat `03-Dominios/Java/Spring Core e Boot/`, notas `publish: true` em PT-BR, numeração global 01-18 (5/7/6). **Galho HÍBRIDO:** REFATOR (notas core partem do tronco rico, refinadas e higienizadas) + PESQUISA (auto-config/starters/eventos/SpringApplication/AOT nascem de `docs.spring.io` via WebFetch). **Fronteira-assinatura INVERTIDA vs Galho 7:** aqui o Spring É o assunto; cada conceito que espelha uma spec Jakarta **linka de volta** ao Galho 7 (CDI/interceptors/eventos/portable extensions) **sem re-explicar a spec**. Galhos 9/10/11/12/13/16/17 = texto "(planejado)", sem wikilink. **Direto na `main`** ([[feedback_galhos_direto_main]]); push manual do usuário.

**Tech Stack:** Obsidian Flavored Markdown, frontmatter YAML, wikilinks, callouts, Dataview, Quartz v4. Verificação via WebFetch (`docs.spring.io`, `spring.io/projects/...` — sem o 403 do openjdk).

---

## Convenções aplicadas a TODAS as notas (ler antes de qualquer task)

**Frontmatter** (ajustar `title`/`fase`/`tags`/`aliases` por nota; `created`/`updated: 2026-06-08`):

```yaml
---
title: "<título sem prefixo numérico>"
created: 2026-06-08
updated: 2026-06-08
type: concept
progress: backlog
status: seedling
publish: true
fase: iniciado | adepto | magus
tags:
  - java
  - spring
  - <fase>
  - <1-3 tags de conceito: ioc, di, beans, aop, proxy, config, profiles, eventos, auto-config, boot, actuator>
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
5. `## Na prática` — código compilável; framing neutro; **NUNCA** 1ª pessoa, `Patient`, `Josenaldo`, `MedEspecialista`. Domínios neutros: `Order`, `Customer`, `Product`, `OrderService`, `CustomerRepository`. Imports `jakarta.*` quando tocar em spec (Boot 3).
6. `## Armadilhas` — ≥2 (Iniciado) / ≥3 (Adepto/Magus). Cada uma: `### (N) Título` + descrição + exemplo curto + fix em 1 linha.
7. `## Em entrevista` — `### Frase pronta (inglês)` com **3+ sentenças** (trade-off + decisão + caveat) + `### Vocabulário` **6+ termos** em tabela `| Termo PT | Termo EN |`.
8. `## Veja também` — wikilinks SEM backticks, SEM âncoras same-file `[[#...]]`. Sempre: notas do galho + `[[03-Dominios/Java/Spring Core e Boot/index|Spring Core e Boot (MOC do galho)]]` + `[[03-Dominios/Java/index|Trilha Java]]` + (quando espelhar spec) a nota do **Galho 7** correspondente + (quando tocar annotations/threads) Galhos 1/4 + verbetes do Dicionário.
9. `## Referências` — docs oficiais consultadas (`docs.spring.io/...`, `spring.io/projects/...`).

**Tamanho:** 200-500 linhas (densas até 600 — limite de [[feedback_notas_atomicas]]).

**Restrições absolutas:**
- **Fronteira-assinatura (linkar de volta ao Galho 7):** todo conceito que espelha spec Jakarta linka pra nota do Galho 7 ("mesma ideia da spec, mecanismo próprio") SEM re-explicar a spec. Mapeamento: IoC/DI/container → CDI 04; escopos/proxies de escopo → CDI 05; qualifiers → CDI 06; `@Configuration`/`@Bean` → CDI 06 (`@Produces`); AOP/interceptors → CDI 13; eventos → CDI 06 (`@Observes`); post-processors → CDI 13 (portable extensions); auto-config/build-time → CDI 13 (CDI Lite); `@Validated` → Bean Validation 08; embedded server → Servlet 03; `@Transactional` (mecanismo) → JTA 11.
- **Galhos 9-17 só como texto "(planejado)", SEM wikilink.** Greps de review checam `\[\[[^]]*(Galho (9|10|11|12|13|16|17)|WebFlux|Spring Security|Spring Data|Spring Cloud)`.
- Sem fabricação ([[feedback_no_fabrication]]); **o tronco é contraexemplo** (`Patient`/`MedEspecialista`/1ª pessoa — NUNCA copiar); **zero estatística de adoção inventada** — vale pra capstone (18) e nota 01.
- **Pesquisa pras partes finas:** notas 11/13/14/15/16/17/18 fundam-se em WebFetch (Step 1). Toda afirmação version-specific verificada: Boot 3.x baseline Java 17 + namespace `jakarta.*`; **`spring.factories` → `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports`** (Boot 2.7+; só `.imports` no Boot 3); deps circulares proibidas por default Boot 2.6+. Nada de memória.
- **Não re-explicar o que é de outro galho:** annotations/reflection → Galho 1 (nota 11); `@Async`/threads por baixo → Galho 4; `@Transactional` operacional/Spring Data/N+1 → Galho 10; `@Controller`/REST/MVC → Galho 9; Security → Galho 12; WebFlux → Galho 11; testes → Galho 13; native/OpenTelemetry/packaging → Galho 17. Specs Jakarta → Galho 7 (linkar, não re-explicar).
- Comparações justas (quando X E quando Y): `@ConfigurationProperties` vs `@Value`, `@Bean` vs scanning, JDK proxy vs CGLIB, Spring vs Jakarta.
- Code fences: ` ```java `, ` ```xml ` (Maven), ` ```properties `/` ```yaml ` (config), ` ```bash `, ` ```text `. Sempre fechadas.
- Commits: sem `Co-Authored-By: Claude`; sem `--no-verify`; `git add <path>` nominal (bot de backup roda em timer — NUNCA `-A`); 1 commit por nota; direto na `main`; **sem push, sem deploy**. Subagents NÃO rodam git — o controlador commita.

**Modelo por nota:** sonnet por padrão; **opus** nas **02** (IoC/DI), **09** (AOP/proxies), **15** (auto-config) e **18** (capstone).

**Fontes oficiais (base):**
- Spring Boot project: `https://spring.io/projects/spring-boot` · docs: `https://docs.spring.io/spring-boot/`
- Spring Framework project: `https://spring.io/projects/spring-framework` · reference core (IoC/AOP): `https://docs.spring.io/spring-framework/reference/core.html`
- IoC container: `https://docs.spring.io/spring-framework/reference/core/beans.html`
- AOP: `https://docs.spring.io/spring-framework/reference/core/aop.html`
- Auto-configuration: `https://docs.spring.io/spring-boot/reference/using/auto-configuration.html` · criar starter: `https://docs.spring.io/spring-boot/reference/features/developing-auto-configuration.html`
- Externalized config: `https://docs.spring.io/spring-boot/reference/features/external-config.html`
- Actuator: `https://docs.spring.io/spring-boot/reference/actuator/`
- SpringApplication/embedded: `https://docs.spring.io/spring-boot/reference/features/spring-application.html` · `https://docs.spring.io/spring-boot/reference/web/servlet.html#web.servlet.embedded-container`

---

## Task 0: Pré-flight — pasta, terreno e baselines

**Files:**
- Create: `03-Dominios/Java/Spring Core e Boot/` (pasta)

- [ ] **Step 1: Confirmar `main`**

```bash
git branch --show-current
```
Expected: `main`. NÃO criar branch.

- [ ] **Step 2: Criar a pasta do galho**

```bash
mkdir -p "03-Dominios/Java/Spring Core e Boot"
```

- [ ] **Step 3: Confirmar títulos exatos das notas do Galho 7 (linkadas de volta) e vizinhas**

```bash
ls "03-Dominios/Java/Jakarta EE/" | grep -E "^(03|04|05|06|08|11|13) "
ls "03-Dominios/Java/Linguagem e sintaxe moderna/" | grep -E "^11 "
ls "03-Dominios/Java/Concorrência e paralelismo/" | grep -E "^(02|08) "
```
Expected: confirmar filenames exatos do Galho 7 (`03 - Servlet API — o alicerce HTTP`, `04 - CDI — beans e injeção`, `05 - CDI — escopos e contextos`, `06 - CDI — qualifiers, producers e eventos`, `08 - Bean Validation`, `11 - JTA — transações na plataforma`, `13 - CDI avançado — interceptors, decorators e extensões`) + Annotations 11 + Concorrência. Anotar divergências.

- [ ] **Step 4: Relocalizar a dívida reversa (9 ganchos — linhas podem ter mudado)**

```bash
grep -rn "Galho 8" "03-Dominios/Java/Linguagem e sintaxe moderna/11 - Annotations.md" "03-Dominios/Java/Jakarta EE/" "03-Dominios/Java/JavaFX/11 - Arquitetura — MVC, MVVM e injeção de dependência.md"
grep -n "planejado" "03-Dominios/Java/index.md" | grep -iE "spring core"
```
Expected: Annotations:~309; Jakarta EE/index:~30; CDI 04:~24; CDI 05:~48; CDI 06:~42; EJB 12:~65 e ~203; CDI 13:~42; JavaFX/11:~35 e ~110; MOC central:38. Anotar linhas reais pra Task 23.

- [ ] **Step 5: Baseline do Dicionário**

```bash
grep -cE "^### " "03-Dominios/Java/Dicionário de Java.md"
```
Expected: **202** (baseline pós-Galho 7). Anotar o número real.

- [ ] **Step 6: Mapear as seções core do tronco (pra Task 22 — poda parcial)**

```bash
grep -nE "^#{2,3} " "03-Dominios/Java/Backend/Spring Boot.md"
grep -niE "Patient|Josenaldo|MedEspecialista|minha experiência" "03-Dominios/Java/Backend/Spring Boot.md" | head -40
```
Expected: confirmar as 5 seções core (`## O que é` ~19; `## Spring IoC Container` ~50; `## AOP e proxies` ~315; `## Configuração e Profiles` ~822; `## Actuator` ~984) e as seções INTOCÁVEIS (`## Gerenciamento de transações` ~516 → galho 10; `## Spring MVC pipeline` ~670 → galho 9; WebFlux/Cloud/Camadas/Troubleshooting). Localizar `## Na prática (da minha experiência)` ~1799 (higienizar). Anotar ranges reais pra Task 22.

- [ ] **Step 7: Fixar fatos a verificar via WebFetch** — Boot 3.x atual + Spring Framework 6.x (baseline Java 17, namespace `jakarta.*`); `AutoConfiguration.imports` vs `spring.factories`; deps circulares proibidas por default Boot 2.6+. Nada de memória.

- [ ] **Step 8: Sem commit** (preparação).

---

## Fase INICIADO (notas 01-05)

### Task 1: Nota 01 — O que é Spring — Framework, Boot e o ecossistema

**Files:**
- Create: `03-Dominios/Java/Spring Core e Boot/01 - O que é Spring — Framework, Boot e o ecossistema.md`

- [ ] **Step 1: Pesquisar** — WebFetch `https://spring.io/projects/spring-boot` + `https://spring.io/projects/spring-framework`. CONFIRMAR: versão atual do Boot 3.x e do Framework 6.x; baseline Java 17; namespace `jakarta.*` (migração de `javax` no Boot 3); o que cada camada faz.

- [ ] **Step 2: Escrever** — `fase: iniciado`, tags `[java, spring, iniciado, boot]`, aliases `["Spring", "Spring Boot", "Spring Framework"]`. Conteúdo:
  - TL;DR: Spring é um ecossistema em camadas — Framework (núcleo IoC/AOP/MVC/tx), Boot (auto-config + starters + embedded server + Actuator por cima) e projetos (Data/Security/Cloud); é a plataforma que implementa boa parte das specs Jakarta (Galho 7).
  - `## O que é` — Framework vs Boot vs projetos; o stack em camadas (diagrama ```text); "opinionated"/convention-over-configuration; `start.spring.io`; `java -jar`.
  - `## Por que importa` — framework de-facto pra backend Java; entrevista cobra "diferença entre Spring e Spring Boot".
  - `## Como funciona` — H3s: "Spring Framework: o núcleo (IoC, AOP, tx, MVC)", "Spring Boot: o que ele adiciona (auto-config, starters, embedded server, Actuator)", "Os projetos do portfólio (Data/Security/Cloud — citar, galhos próprios planejados)", "Boot 3.x: Java 17+ e o namespace `jakarta.*`".
  - `## Na prática` — `pom.xml` mínimo com `spring-boot-starter` + classe `@SpringBootApplication` com `main` (```java).
  - `## Armadilhas` — ≥2: (1) confundir "Spring" com "Spring Boot"; (2) achar que Boot substitui o Framework; (3) misturar deps `javax.*` num projeto Boot 3 (é `jakarta.*`).
  - `## Em entrevista` + `## Veja também` ([[02 - IoC e injeção de dependência no Spring]], [[15 - Auto-configuration e starters]], [[03-Dominios/Java/Jakarta EE/index|Jakarta EE]] (a plataforma sob o Spring), MOC galho, MOC central, verbetes `Spring Framework`/`Spring Boot`/`convention over configuration`) + `## Referências`.

- [ ] **Step 3: Verificar**
```bash
grep -cE "^## (O que é|Por que importa|Como funciona|Na prática|Armadilhas|Em entrevista|Veja também|Referências)" "03-Dominios/Java/Spring Core e Boot/01 - O que é Spring — Framework, Boot e o ecossistema.md"
grep -riE "Patient|MedEspecialista|minha experiência" "03-Dominios/Java/Spring Core e Boot/01 - O que é Spring — Framework, Boot e o ecossistema.md"
```
Expected: ≥7 seções; segundo grep **VAZIO**.

- [ ] **Step 4: Commit** — `git add "<path>"` && `git commit -m "feat(java): galho 8 nota 01 — O que é Spring (Framework, Boot e ecossistema)"`

### Task 2: Nota 02 — IoC e injeção de dependência no Spring ⟦opus⟧

**Files:**
- Create: `03-Dominios/Java/Spring Core e Boot/02 - IoC e injeção de dependência no Spring.md`

- [ ] **Step 1: Pesquisar** — WebFetch `https://docs.spring.io/spring-framework/reference/core/beans.html` (Introduction to the IoC Container). Refinar a partir do tronco `## Spring IoC Container` (linhas 84-110), **higienizando** `Patient`→`Customer`.

- [ ] **Step 2: Escrever** — `fase: iniciado`, tags `[java, spring, iniciado, ioc, di]`, aliases `["IoC no Spring", "DI no Spring", "Inversão de controle"]`. **Nota-assinatura do galho.** Conteúdo:
  - TL;DR: IoC = o framework controla criação e wiring dos objetos; DI = a forma de implementar (o container injeta dependências). É a mesma ideia da spec CDI (Galho 7), com container próprio do Spring — é isso que o `@Autowired` esconde.
  - `## O que é` — IoC (princípio) e DI (implementação); o container Spring.
  - `## Por que importa` — desacoplamento, testabilidade; base de todo o galho.
  - `## Como funciona` — H3s: "Antes e depois (acoplamento com `new` vs `final` injetado)", "O container: quem cria e conecta os beans", "Spring vs CDI: mesma ideia, container próprio (não é uma impl de CDI)".
  - `## Na prática` — `OrderService` recebendo `CustomerRepository` por construtor; o container resolvendo (```java).
  - `## Armadilhas` — ≥2: (1) `new` manual ignorando o container; (2) field injection escondendo deps (teaser da 04); (3) achar que Spring "é" CDI.
  - `## Em entrevista` + `## Veja também` ([[03 - Beans e estereótipos — @Component, @Service, @Repository, @Controller]], [[04 - Tipos de injeção — constructor, setter, field]], [[06 - ApplicationContext — o container e seu ciclo]], **[[03-Dominios/Java/Jakarta EE/04 - CDI — beans e injeção|CDI — beans e injeção]]** (a spec equivalente), MOC galho, MOC central, verbetes `IoC / inversão de controle (Spring)`/`@Autowired`) + `## Referências`.

- [ ] **Step 3: Verificar** — ≥7 seções; grep anti-fabricação VAZIO; `grep "Jakarta EE/04 - CDI"` ≥1 (link de volta presente).

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 8 nota 02 — IoC e injeção de dependência no Spring"`

### Task 3: Nota 03 — Beans e estereótipos — @Component, @Service, @Repository, @Controller

**Files:**
- Create: `03-Dominios/Java/Spring Core e Boot/03 - Beans e estereótipos — @Component, @Service, @Repository, @Controller.md`

- [ ] **Step 1: Pesquisar** — WebFetch `https://docs.spring.io/spring-framework/reference/core/beans/classpath-scanning.html`. Refinar do tronco `### @Component vs @Service vs @Repository vs @Controller` (246-256), higienizando.

- [ ] **Step 2: Escrever** — `fase: iniciado`, tags `[java, spring, iniciado, beans]`. Conteúdo:
  - TL;DR: bean = objeto gerenciado pelo container; estereótipos (`@Component`/`@Service`/`@Repository`/`@Controller`) registram a classe via component scanning; tecnicamente equivalentes, semanticamente distintos (`@Repository` adiciona tradução de exceções).
  - `## O que é` / `## Por que importa` / `## Como funciona` (H3s: "Component scanning e `@ComponentScan`/`@SpringBootApplication`", "Os 4 estereótipos e o que cada um adiciona (`@Repository` → `DataAccessException`)", "`@Controller`/`@RestController` (citar — Galho 9, planejado)").
  - `## Na prática` — `@Service OrderService`, `@Repository CustomerRepository` (```java).
  - `## Armadilhas` — ≥2: (1) classe fora do pacote escaneado → bean não registrado; (2) `@Component` onde cabia `@Repository` → perde tradução de exceção.
  - `## Em entrevista` + `## Veja também` ([[02 - ...]], [[04 - ...]], [[03-Dominios/Java/Jakarta EE/04 - CDI — beans e injeção|CDI — beans e injeção]] (bean discovery), MOC galho/central, verbetes `@Component / estereótipos Spring`/`component scanning`) + `## Referências`.

- [ ] **Step 3: Verificar** — ≥7 seções; anti-fabricação VAZIO; sem `[[` pra Galho 9.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 8 nota 03 — beans e estereótipos"`

### Task 4: Nota 04 — Tipos de injeção — constructor, setter, field

**Files:**
- Create: `03-Dominios/Java/Spring Core e Boot/04 - Tipos de injeção — constructor, setter, field.md`

- [ ] **Step 1: Pesquisar** — WebFetch `https://docs.spring.io/spring-framework/reference/core/beans/dependencies/factory-collaborators.html` (constructor vs setter). Refinar do tronco `### Tipos de injeção` (111-159), higienizando `Patient`→`Customer`.

- [ ] **Step 2: Escrever** — `fase: iniciado`, tags `[java, spring, iniciado, di]`. Conteúdo:
  - TL;DR: prefira constructor injection (`final`, imutável, fail-fast, testável sem Spring); setter pra opcional; evite field injection.
  - H3s: "Constructor injection (recomendado e por quê)", "Setter injection (dependências opcionais)", "Field injection (`@Autowired` em campo — por que evitar)", "Dependências circulares proibidas por default no Boot 2.6+ (verificar via WebFetch)".
  - `## Na prática` — as 3 formas lado a lado (```java).
  - `## Armadilhas` — ≥2: (1) field injection em código que precisa de teste; (2) `@Autowired` redundante em construtor único (desde Spring 4.3); (3) ciclo mascarado.
  - `## Veja também` — [[02 - ...]], [[03 - ...]], [[03-Dominios/Java/Jakarta EE/04 - CDI — beans e injeção|CDI — beans e injeção]] (`@Inject` em campo/construtor/método), MOC galho/central, verbete `constructor injection`.

- [ ] **Step 3: Verificar** — ≥7 seções; anti-fabricação VAZIO.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 8 nota 04 — tipos de injeção"`

### Task 5: Nota 05 — @Configuration e @Bean — definição explícita de beans

**Files:**
- Create: `03-Dominios/Java/Spring Core e Boot/05 - @Configuration e @Bean — definição explícita de beans.md`

- [ ] **Step 1: Pesquisar** — WebFetch `https://docs.spring.io/spring-framework/reference/core/beans/java.html` (Java-based config, `@Bean`, `@Configuration` full vs lite). Refinar do tronco `### Configuração com @Configuration e @Bean` (257-285), higienizando.

- [ ] **Step 2: Escrever** — `fase: iniciado`, tags `[java, spring, iniciado, beans]`. Conteúdo:
  - TL;DR: além de scanning, você declara beans com métodos `@Bean` em classes `@Configuration` — útil pra libs externas não-anotáveis e construção complexa.
  - H3s: "`@Configuration` + `@Bean`: declarar explicitamente", "Quando usar (libs externas, construção complexa, override) vs component scanning", "`@Import` e composição de configs", "Full vs lite mode (`proxyBeanMethods`)".
  - `## Na prática` — `@Bean` pra um `RestClient`/`ObjectMapper` (lib externa) (```java).
  - `## Armadilhas` — ≥2: (1) chamar método `@Bean` direto esperando o singleton (lite mode não intercepta); (2) `@Bean` em `@Component` ≠ em `@Configuration`.
  - `## Veja também` — [[02 - ...]], **[[03-Dominios/Java/Jakarta EE/06 - CDI — qualifiers, producers e eventos|CDI — producers]]** (`@Produces`: fabricar o que não é bean anotável — mesma necessidade), [[14 - Conditional beans — @Conditional e os @ConditionalOn]] (teaser), MOC galho/central, verbetes `@Configuration`/`@Bean`.

- [ ] **Step 3: Verificar** — ≥7 seções; anti-fabricação VAZIO; link CDI 06 presente.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 8 nota 05 — @Configuration e @Bean"`

---

## Fase ADEPTO (notas 06-12)

### Task 6: Nota 06 — ApplicationContext — o container e seu ciclo

**Files:**
- Create: `03-Dominios/Java/Spring Core e Boot/06 - ApplicationContext — o container e seu ciclo.md`

- [ ] **Step 1: Pesquisar** — WebFetch `https://docs.spring.io/spring-framework/reference/core/beans/context-introduction.html` (`ApplicationContext` vs `BeanFactory`). Refinar do tronco `### BeanFactory vs ApplicationContext` (54-82), higienizando.

- [ ] **Step 2: Escrever** — `fase: adepto`, tags `[java, spring, adepto, ioc]`. ≥3 H3s: "`BeanFactory` vs `ApplicationContext` (o que o segundo adiciona)", "Tipos concretos (standalone, servlet, reactive)", "`refresh()` e o ciclo do container", "Interfaces `*Aware` (injetar infraestrutura)". `## Na prática`: injetar `ApplicationContext` (raro, com ressalva). `## Armadilhas` ≥3: service-locator anti-pattern (`getBean()` em vez de injeção); assumir lazy onde é eager; segurar referência ao contexto. `## Veja também` — [[02 - ...]], [[07 - Ciclo de vida e escopos de beans]], [[03-Dominios/Java/Jakarta EE/04 - CDI — beans e injeção|CDI]] (o container da spec), verbetes `ApplicationContext`/`BeanFactory`.

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; anti-fabricação VAZIO.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 8 nota 06 — ApplicationContext e o container"`

### Task 7: Nota 07 — Ciclo de vida e escopos de beans

**Files:**
- Create: `03-Dominios/Java/Spring Core e Boot/07 - Ciclo de vida e escopos de beans.md`

- [ ] **Step 1: Pesquisar** — WebFetch `https://docs.spring.io/spring-framework/reference/core/beans/factory-scopes.html` + `.../factory-nature.html` (lifecycle callbacks). Refinar do tronco `### Bean lifecycle` (161-193) + `### Bean scopes` (195-223), higienizando.

- [ ] **Step 2: Escrever** — `fase: adepto`, tags `[java, spring, adepto, beans]`. ≥3 H3s: "O ciclo de vida (instanciação → populate → `*Aware` → BPP → `@PostConstruct`/init → BPP → pronto → `@PreDestroy`/destroy)", "Escopos (singleton default, prototype, request/session/application/websocket)", "Prototype em singleton: o problema e as saídas (`ObjectProvider`, `@Lookup`, scoped proxy)". `## Na prática`: `@PostConstruct`/`@PreDestroy` + `ObjectProvider`. `## Armadilhas` ≥3: estado mutável em singleton (thread-safety — linka [[03-Dominios/Java/Concorrência e paralelismo/index|Galho 4]]); prototype injetado ingenuamente; lógica pesada no construtor vs `@PostConstruct`. `## Veja também` — **[[03-Dominios/Java/Jakarta EE/05 - CDI — escopos e contextos|CDI — escopos e contextos]]** (escopos + client proxies da spec), verbetes `bean scope (Spring)`.

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; link CDI 05 presente; anti-fabricação VAZIO.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 8 nota 07 — ciclo de vida e escopos de beans"`

### Task 8: Nota 08 — Qualificação de beans — @Qualifier, @Primary, @Profile

**Files:**
- Create: `03-Dominios/Java/Spring Core e Boot/08 - Qualificação de beans — @Qualifier, @Primary, @Profile.md`

- [ ] **Step 1: Pesquisar** — WebFetch `https://docs.spring.io/spring-framework/reference/core/beans/annotation-config/autowired-qualifiers.html`. Refinar das menções do tronco (`@Primary`/`@Profile` espalhados em 277-309, 896-910).

- [ ] **Step 2: Escrever** — `fase: adepto`, tags `[java, spring, adepto, beans]`. ≥3 H3s: "Ambiguidade de tipo (`NoUniqueBeanDefinitionException`)", "`@Qualifier` (custom e por nome)", "`@Primary` e `@Profile` como condicionais", "Injeção de coleções (`List<T>`, `Map<String,T>`) e `@Order`". `## Armadilhas` ≥3: dois `@Primary`; `@Qualifier` com nome errado; esquecer que `List<T>` injeta todos. `## Veja também` — **[[03-Dominios/Java/Jakarta EE/06 - CDI — qualifiers, producers e eventos|CDI — qualifiers]]**, [[12 - Configuração e profiles]] (`@Profile` em detalhe), verbetes `@Qualifier (Spring)`/`@Primary`.

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; link CDI 06 presente; anti-fabricação VAZIO.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 8 nota 08 — qualificação de beans"`

### Task 9: Nota 09 — AOP e proxies no Spring ⟦opus⟧

**Files:**
- Create: `03-Dominios/Java/Spring Core e Boot/09 - AOP e proxies no Spring.md`

- [ ] **Step 1: Pesquisar** — WebFetch `https://docs.spring.io/spring-framework/reference/core/aop.html` + `.../aop/proxying.html` (JDK vs CGLIB). Refinar do tronco `## AOP e proxies` (315-373, 446-512), higienizando `PatientService`→`OrderService`.

- [ ] **Step 2: Escrever** — `fase: adepto`, tags `[java, spring, adepto, aop, proxy]`. ≥3 H3s: "Cross-cutting concerns e como o proxy intercepta", "JDK dynamic proxy vs CGLIB (interface vs subclasse; default no Boot)", "Advice types (`@Before`/`@After`/`@AfterReturning`/`@AfterThrowing`/`@Around`)", "Pointcut expressions e `@Aspect`". AOP é o mecanismo sob `@Transactional`/`@Async`/`@Cacheable` (citar; comportamento → galhos 10/12 texto). `## Na prática`: `@Aspect` de logging com `@Around` (```java). `## Armadilhas` ≥3: esperar AOP em chamada interna (teaser da 10); `@Aspect` sem `@Component`; pointcut largo demais. `## Veja também` — **[[03-Dominios/Java/Jakarta EE/13 - CDI avançado — interceptors, decorators e extensões|CDI — interceptors]]** (proxy-based vs interceptor-based), [[10 - Self-invocation e os limites do proxy]], [[03-Dominios/Java/Linguagem e sintaxe moderna/11 - Annotations|Annotations]] (Galho 1), verbetes `Spring AOP`/`proxy`/`advice`/`pointcut`.

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; link CDI 13 presente; sem `[[` pra Galho 10/12; anti-fabricação VAZIO.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 8 nota 09 — AOP e proxies no Spring"`

### Task 10: Nota 10 — Self-invocation e os limites do proxy

**Files:**
- Create: `03-Dominios/Java/Spring Core e Boot/10 - Self-invocation e os limites do proxy.md`

- [ ] **Step 1: Pesquisar** — WebFetch `https://docs.spring.io/spring-framework/reference/core/aop/proxying.html` (understanding AOP proxies / self-invocation). Refinar do tronco `### Self-invocation` (375-437) + `### @Transactional em métodos private ou final` (439-444).

- [ ] **Step 2: Escrever** — `fase: adepto`, tags `[java, spring, adepto, aop, proxy]`. ≥3 H3s: "Por que a chamada interna bypassa o proxy", "`private`/`final`: AOP silenciosamente ignorado (CGLIB não intercepta/sobrescreve)", "Soluções (extrair pra outro bean; self-injection; anotar o método de entrada público)". É o mecanismo por baixo de `@Transactional`/`@Async` (sem o comportamento transacional → Galho 10 texto). `## Na prática`: `OrderService.createOrder` chamando `this.sendConfirmation()` `@Transactional` ignorado + fix (```java). `## Armadilhas` ≥3: refatorar "puxando pra dentro" e quebrar `@Transactional`; método `@Async` `private`; achar self-injection elegante. `## Veja também` — [[09 - AOP e proxies no Spring]], **[[03-Dominios/Java/Jakarta EE/05 - CDI — escopos e contextos|CDI — escopos e contextos]]** (mesmo limite no client proxy), verbete `self-invocation`.

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; link CDI 05 presente; sem `[[` pra Galho 10; anti-fabricação VAZIO.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 8 nota 10 — self-invocation e os limites do proxy"`

### Task 11: Nota 11 — Eventos do ApplicationContext

**Files:**
- Create: `03-Dominios/Java/Spring Core e Boot/11 - Eventos do ApplicationContext.md`

- [ ] **Step 1: Pesquisar** — WebFetch `https://docs.spring.io/spring-framework/reference/core/beans/context-introduction.html#context-functionality-events` (standard/custom events, `@EventListener`). **Nota de pesquisa** (tronco não cobre).

- [ ] **Step 2: Escrever** — `fase: adepto`, tags `[java, spring, adepto, eventos]`. ≥3 H3s: "Publicar e ouvir (`ApplicationEventPublisher`, POJO events, `@EventListener`)", "Síncrono por default vs `@Async` events (linka [[03-Dominios/Java/Concorrência e paralelismo/index|Galho 4]])", "Eventos built-in do contexto (`ContextRefreshedEvent`, `ApplicationReadyEvent`)". `@TransactionalEventListener` só menção (comportamento tx → Galho 10 texto). `## Na prática`: publicar `OrderPlacedEvent` e ouvir com `@EventListener` (```java). `## Armadilhas` ≥3: listener síncrono lento bloqueando o publisher; assumir transação em listener async; vazar evento entre contextos. `## Veja também` — **[[03-Dominios/Java/Jakarta EE/06 - CDI — qualifiers, producers e eventos|CDI — eventos]]** (`@Observes`/`Event<T>` da spec), verbete `@EventListener`.

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; link CDI 06 presente; anti-fabricação VAZIO.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 8 nota 11 — eventos do ApplicationContext"`

### Task 12: Nota 12 — Configuração e profiles

**Files:**
- Create: `03-Dominios/Java/Spring Core e Boot/12 - Configuração e profiles.md`

- [ ] **Step 1: Pesquisar** — WebFetch `https://docs.spring.io/spring-boot/reference/features/external-config.html` + `.../profiles.html`. Refinar do tronco `## Configuração e Profiles` (822-980), higienizando `medespecialista`→`order-service`.

- [ ] **Step 2: Escrever** — `fase: adepto`, tags `[java, spring, adepto, config, profiles]`. ≥3 H3s: "Hierarquia/precedência de fontes (args > env > `application-{profile}` > `application` > defaults)", "Profiles (`application-{profile}.yml`, `@Profile`, ativação)", "`@ConfigurationProperties` (binding tipado, record, `@Validated`, relaxed binding) vs `@Value`/SpEL". `## Na prática`: `@ConfigurationProperties` record + YAML (```java/```yaml). `## Armadilhas` ≥3: secret hardcoded em `application.yml`; `@Value` espalhado onde cabia binding tipado; relaxed binding mal-entendido (`max-retries`↔`maxRetries`). `## Veja também` — [[08 - Qualificação de beans — @Qualifier, @Primary, @Profile]], **[[03-Dominios/Java/Jakarta EE/08 - Bean Validation|Bean Validation]]** (`@Validated` aciona a spec), verbetes `@ConfigurationProperties`/`@Value`/`@Profile (Spring)`.

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; link Bean Validation 08 presente; anti-fabricação VAZIO (grep `medespecialista` também).

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 8 nota 12 — configuração e profiles"`

---

## Fase MAGUS (notas 13-18)

### Task 13: Nota 13 — BeanPostProcessor e BeanFactoryPostProcessor

**Files:**
- Create: `03-Dominios/Java/Spring Core e Boot/13 - BeanPostProcessor e BeanFactoryPostProcessor.md`

- [ ] **Step 1: Pesquisar** — WebFetch `https://docs.spring.io/spring-framework/reference/core/beans/factory-extension.html` (container extension points). Refinar do tronco `### BeanPostProcessor` (225-244).

- [ ] **Step 2: Escrever** — `fase: magus`, tags `[java, spring, magus, ioc]`. ≥3 H3s: "BFPP: modificar bean *definitions* antes da instanciação", "BPP: envolver *instâncias* depois (onde nascem os proxies AOP)", "Ordem (`Ordered`/`@Priority`) e por que BPPs são instanciados cedo". `## Na prática`: um BPP simples que loga/embrulha (```java). `## Armadilhas` ≥3: injetar deps complexas num BPP (instanciado cedo demais — não é proxiável); quebrar a ordem do contexto; confundir BFPP com BPP. `## Veja também` — [[09 - AOP e proxies no Spring]], **[[03-Dominios/Java/Jakarta EE/13 - CDI avançado — interceptors, decorators e extensões|CDI avançado — portable extensions]]** (o ponto de extensão da spec), [[15 - Auto-configuration e starters]], verbetes `BeanPostProcessor`/`BeanFactoryPostProcessor`.

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; link CDI 13 presente; anti-fabricação VAZIO.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 8 nota 13 — BeanPostProcessor e BeanFactoryPostProcessor"`

### Task 14: Nota 14 — Conditional beans — @Conditional e os @ConditionalOn*

**Files:**
- Create: `03-Dominios/Java/Spring Core e Boot/14 - Conditional beans — @Conditional e os @ConditionalOn.md`

- [ ] **Step 1: Pesquisar** — WebFetch `https://docs.spring.io/spring-boot/reference/features/developing-auto-configuration.html#features.developing-auto-configuration.condition-annotations` + Javadoc `org.springframework.boot.autoconfigure.condition`. Refinar do tronco `### Conditional beans` (287-311).

- [ ] **Step 2: Escrever** — `fase: magus`, tags `[java, spring, magus, auto-config]`. ≥3 H3s: "O SPI `@Conditional` + `Condition`", "Os condicionais do Boot (`@ConditionalOnClass`/`OnMissingClass`/`OnBean`/`OnMissingBean`/`OnProperty`/`OnWebApplication`/`OnExpression`)", "Ordem de avaliação e por que `@ConditionalOnMissingBean` cede pro usuário". Pré-requisito da 15. `## Na prática`: `@Bean @ConditionalOnProperty` escolhendo impl (```java). `## Armadilhas` ≥3: `@ConditionalOnMissingBean` por tipo errado; ordem assumida; condicional dependente de outro condicional. `## Veja também` — [[05 - @Configuration e @Bean — definição explícita de beans]], [[15 - Auto-configuration e starters]], verbete `@Conditional / @ConditionalOnX`.

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; anti-fabricação VAZIO.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 8 nota 14 — conditional beans"`

### Task 15: Nota 15 — Auto-configuration e starters ⟦opus⟧

**Files:**
- Create: `03-Dominios/Java/Spring Core e Boot/15 - Auto-configuration e starters.md`

- [ ] **Step 1: Pesquisar (CRÍTICO)** — WebFetch `https://docs.spring.io/spring-boot/reference/using/auto-configuration.html` + `.../features/developing-auto-configuration.html` + `.../using/build-systems.html#using.build-systems.starters`. **CONFIRMAR o ponto minado:** o registro de auto-config é `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports` (substituiu `spring.factories`; no Boot 3 só `.imports`). Confirmar `@AutoConfiguration(before/after)`, `@SpringBootApplication = @EnableAutoConfiguration + @ComponentScan + @Configuration`, o que é um starter (POM agregador, não código). **Nota de pesquisa.**

- [ ] **Step 2: Escrever** — `fase: magus`, tags `[java, spring, magus, auto-config, boot]`. ≥3 H3s: "`@EnableAutoConfiguration`/`@SpringBootApplication`", "O registro via `AutoConfiguration.imports` (substituiu `spring.factories` — Boot 2.7+/3.x)", "Como auto-config usa `@Conditional` e cede pro usuário (`@ConditionalOnMissingBean`); ordem", "Starters: o que são (POM agregador, não código)", "Debug (`--debug` → `ConditionEvaluationReport`, `/actuator/conditions`); AOT/build-time (menção — native → Galho 17 texto)". `## Na prática`: esqueleto de uma auto-config class + `.imports` (```java/```text). `## Armadilhas` ≥3: criar starter achando que precisa de código; auto-config não dispara (faltou `@ConditionalOnClass`); sobrescrever sem entender `@ConditionalOnMissingBean`. `## Veja também` — [[14 - Conditional beans — @Conditional e os @ConditionalOn]], [[16 - SpringApplication e o embedded server]], **[[03-Dominios/Java/Jakarta EE/13 - CDI avançado — interceptors, decorators e extensões|CDI avançado]]** (build-time/CDI Lite), verbetes `auto-configuration`/`starter (Spring Boot)`/`@EnableAutoConfiguration`.

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; `grep "AutoConfiguration.imports"` ≥1; link CDI 13 presente; anti-fabricação VAZIO.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 8 nota 15 — auto-configuration e starters"`

### Task 16: Nota 16 — SpringApplication e o embedded server

**Files:**
- Create: `03-Dominios/Java/Spring Core e Boot/16 - SpringApplication e o embedded server.md`

- [ ] **Step 1: Pesquisar** — WebFetch `https://docs.spring.io/spring-boot/reference/features/spring-application.html` + `.../web/servlet.html` (embedded container) + `.../specification/executable-jar/` (packaging — conceito). **Nota de pesquisa.**

- [ ] **Step 2: Escrever** — `fase: magus`, tags `[java, spring, magus, boot]`. ≥3 H3s: "`SpringApplication.run()`: cria o contexto, dispara auto-config, sobe o servidor", "`ApplicationRunner`/`CommandLineRunner` e listeners do startup", "Embedded server (Tomcat default; Jetty/Undertow via starter — tuning deep → Galho 9/17 texto)", "Fat/executable jar e layered jar (conceito — packaging deep → Galho 15/17 texto)". `## Na prática`: `main` + `CommandLineRunner` (```java). `## Armadilhas` ≥3: lógica pesada no `main` vs runner/bean; assumir WAR/servidor externo por hábito; bloquear o startup num runner. `## Veja também` — [[15 - Auto-configuration e starters]], [[17 - Actuator e observabilidade]], **[[03-Dominios/Java/Jakarta EE/03 - Servlet API — o alicerce HTTP|Servlet API]]** (o embedded server roda o Servlet container), verbetes `SpringApplication`/`embedded server`/`executable jar / fat jar`.

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; link Servlet 03 presente; sem `[[` pra Galho 9/15/17; anti-fabricação VAZIO.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 8 nota 16 — SpringApplication e embedded server"`

### Task 17: Nota 17 — Actuator e observabilidade

**Files:**
- Create: `03-Dominios/Java/Spring Core e Boot/17 - Actuator e observabilidade.md`

- [ ] **Step 1: Pesquisar** — WebFetch `https://docs.spring.io/spring-boot/reference/actuator/` (endpoints, health, metrics/Micrometer). Refinar do tronco `## Actuator` (984-1146), higienizando `/patients`→`/orders`.

- [ ] **Step 2: Escrever** — `fase: magus`, tags `[java, spring, magus, actuator, boot]`. ≥3 H3s: "Endpoints (`/health`, `/info`, `/metrics`, `/loggers`, `/conditions`, `/beans`...)", "Exposição e segurança dos endpoints (auth → Galho 12 texto)", "Health groups + liveness/readiness (Kubernetes); custom `HealthIndicator`", "Micrometer como fachada de métricas (conceito; Prometheus de exemplo)". **Fronteira:** OpenTelemetry/distributed tracing/observabilidade profunda → Galho 17 (texto "(planejado)"). `## Na prática`: custom `HealthIndicator` + `management.endpoints.web.exposure` (```java/```yaml). `## Armadilhas` ≥3: expor todos os endpoints sem auth; health check pesado; confundir liveness com readiness. `## Veja também` — [[16 - SpringApplication e o embedded server]], [[14 - Conditional beans — @Conditional e os @ConditionalOn]], verbetes `Spring Actuator`.

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; sem `[[` pra Galho 12/17; anti-fabricação VAZIO (grep `patients` também).

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 8 nota 17 — Actuator e observabilidade"`

### Task 18: Nota 18 — Capstone: Spring sob o capô ⟦opus⟧

**Files:**
- Create: `03-Dominios/Java/Spring Core e Boot/18 - Capstone — Spring sob o capô.md`

- [ ] **Step 1: Pesquisar** — WebFetch `https://docs.spring.io/spring-framework/reference/overview.html` + `https://docs.spring.io/spring-boot/reference/using/auto-configuration.html` (revisar). Conferir a tabela Spring↔Jakarta com as notas do Galho 7 já escritas.

- [ ] **Step 2: Escrever** — `fase: magus`, tags `[java, spring, magus, boot]`, aliases `["Capstone Spring", "Spring sob o capô"]`. Conteúdo:
  - TL;DR: a "mágica" do Spring é mecanismo — `run()` → scanning → bean definitions → BFPP → instanciação → DI → BPP/proxies → `@PostConstruct` → contexto pronto; a auto-config é `@Conditional` + `.imports`.
  - `## O que é` / `## Por que importa`.
  - `## Como funciona` — H3s: "Da `run()` ao bean pronto: o caminho completo (diagrama ```text)", "Onde a auto-config entra", "**Spring → Jakarta EE: dois caminhos pro mesmo problema** (tabela: IoC↔CDI, `@Autowired`↔`@Inject`, AOP proxy↔interceptors, `@Transactional` Spring↔JTA, `@Validated`↔Bean Validation, eventos↔`@Observes`)".
  - `## Na prática` — decisão honesta Spring vs plataforma pura (quando cada um; **sem dogma, zero estatística inventada**).
  - `## Armadilhas` (de raciocínio) ≥3: "auto-config é mágica" (é `@Conditional` + `.imports`); "Spring substituiu Jakarta" (implementa/consome várias specs); decidir framework por hype.
  - `## Em entrevista` (munição: IoC, AOP, auto-config) + `### Cheatsheet` (nota→problema) + `## Veja também` (todas as notas-chave do galho + **[[03-Dominios/Java/Jakarta EE/14 - Jakarta EE hoje — a plataforma sob o Spring|Jakarta EE hoje]]** + MOC galho/central) + `## Referências`.

- [ ] **Step 3: Verificar** — ≥7 seções; tabela Spring↔Jakarta presente (`grep -i "CDI\|JTA\|Bean Validation"`); link capstone Galho 7 presente; anti-fabricação VAZIO; sem estatística inventada (revisar manualmente).

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 8 nota 18 — capstone (Spring sob o capô)"`

---

## Task 19: MOC do galho

**Files:**
- Create: `03-Dominios/Java/Spring Core e Boot/index.md`

- [ ] **Step 1: Escrever** — modelar pelo `03-Dominios/Java/Jakarta EE/index.md`. Frontmatter: `type: moc`, `status: growing`, `publish: true`, `title: "Spring Core e Boot"`, tags `[java, spring, moc]`, aliases `["Spring", "Spring Framework", "Spring Boot", "Galho 8 - Spring"]`, `created`/`updated: 2026-06-08`. Conteúdo:
  - TL;DR — Galho 8; o container que implementa as specs do Galho 7: IoC/DI, beans e escopos, AOP/proxies, config/profiles, conditional/auto-config, eventos, fundamentos do Boot e Actuator; 18 notas em 3 fases.
  - `## Sobre este galho` — escopo + audiência + **galho híbrido** (refator parcial do tronco `Spring Boot.md` + pesquisa) + fronteiras (Jakarta EE → Galho 7 linkado; Galhos 9/10/11/12/13/16/17 planejados, texto).
  - `## Iniciado` (01-05) / `## Adepto` (06-12) / `## Magus` (13-18) — wikilinks + 1 linha cada.
  - `## Rotas alternativas` — 5: **Completa** (01→18); **Entrevista internacional** (02→04→07→09→10→11→15→18); **O que o Spring esconde** (02→05→09→13→15→18); **Boot sob o capô** (14→15→16→17→13→18); **Spring vs Jakarta EE** (02→07→09→11→18 + Galho 7).
  - `## Todas as notas` — Dataview (`FROM "03-Dominios/Java/Spring Core e Boot"`, `WHERE type = "concept"`).
  - `## Veja também` — MOC central, [[03-Dominios/Java/Jakarta EE/index|Jakarta EE]], Galhos 1/4 (index), Dicionário; Galhos 9-17 como texto "(planejado)" SEM wikilink.

- [ ] **Step 2: Verificar**
```bash
grep -cE "^## (Iniciado|Adepto|Magus|Rotas alternativas)" "03-Dominios/Java/Spring Core e Boot/index.md"
grep -c "\[\[" "03-Dominios/Java/Spring Core e Boot/index.md"
grep -E "\[\[[^]]*(Galho (9|10|11|12|13|16|17))" "03-Dominios/Java/Spring Core e Boot/index.md"
```
Expected: 4 headings; ≥18 wikilinks; **último grep VAZIO**.

- [ ] **Step 3: Commit** — `git add "<path>"` && `git commit -m "feat(java): galho 8 MOC — Spring Core e Boot"`

---

## Task 20: Expandir o Dicionário de Java (NÃO recriar)

**Files:**
- Modify: `03-Dominios/Java/Dicionário de Java.md`

- [ ] **Step 1: Extrair as âncoras realmente usadas pelas notas**
```bash
grep -rhoE "Dicionário de Java#[^]|]+" "03-Dominios/Java/Spring Core e Boot/" | sort -u
```
A fonte da verdade é o que as notas usaram. Lista esperada (~37): `@Autowired`, `@Bean`, `@Component / estereótipos Spring`, `@Conditional / @ConditionalOnX`, `@Configuration`, `@ConfigurationProperties`, `@EnableAutoConfiguration`, `@EventListener`, `@Primary`, `@Profile (Spring)`, `@Qualifier (Spring)`, `@Transactional (Spring)`, `@Value`, `advice (Spring AOP)`, `ApplicationContext`, `aspect`, `auto-configuration`, `BeanFactory`, `BeanFactoryPostProcessor`, `BeanPostProcessor`, `bean scope (Spring)`, `CGLIB`, `component scanning`, `constructor injection`, `convention over configuration`, `embedded server`, `executable jar / fat jar`, `IoC / inversão de controle (Spring)`, `JDK dynamic proxy`, `pointcut`, `self-invocation`, `Spring Actuator`, `Spring AOP`, `Spring AOT`, `Spring Boot`, `Spring Framework`, `SpringApplication`, `starter (Spring Boot)`.

- [ ] **Step 2: Ler o Dicionário e conferir duplicatas** — formato `### Termo` + 1-3 linhas + `Veja também:`. **NÃO recriar/reordenar.** **Desambiguar `@Transactional (Spring)` do `@Transactional (Jakarta)` já existente** — verbetes distintos que se linkam mutuamente. Nenhum verbete Spring existe ainda (Task 0 Step 5 confirma 202; só `client proxy (CDI)` é adjacente, do Galho 7 — intacto).

- [ ] **Step 3: Inserir em ordem alfabética** (case-insensitive, sem acento; verbetes iniciados em `@` entram na seção da letra seguinte — conferir o padrão do arquivo). Cada verbete: heading EXATO da âncora + definição fiel às notas + `Veja também:` pra nota canônica (IoC/DI→02; estereótipos/scanning→03; injeção→04; `@Configuration`/`@Bean`→05; `ApplicationContext`/`BeanFactory`→06; escopos→07; `@Qualifier`/`@Primary`→08; AOP/proxy/advice/pointcut/CGLIB/JDK→09; self-invocation→10; `@EventListener`→11; `@ConfigurationProperties`/`@Value`/`@Profile`→12; post-processors→13; `@Conditional`→14; auto-config/starter/`@EnableAutoConfiguration`/AOT→15; `SpringApplication`/embedded/fat jar→16; Actuator→17; Spring Framework/Boot/convention→01). Atualizar `updated: 2026-06-08`.

- [ ] **Step 4: Verificar**
```bash
grep -E "^### (Spring Boot|ApplicationContext|auto-configuration|Spring AOP|@ConfigurationProperties|SpringApplication)" "03-Dominios/Java/Dicionário de Java.md"
grep -cE "^### " "03-Dominios/Java/Dicionário de Java.md"
grep -E "^### @Transactional" "03-Dominios/Java/Dicionário de Java.md"
```
Expected: novos presentes; contagem subiu ~37 vs baseline (202 → ~239); **dois** `@Transactional` (Jakarta + Spring).

- [ ] **Step 5: Commit** — `git add "<path>"` && `git commit -m "feat(java): expande Dicionário de Java com verbetes do galho 8 (Spring Core e Boot)"`

---

## Task 21: Ativar o Galho 8 no MOC central

**Files:**
- Modify: `03-Dominios/Java/index.md`

- [ ] **Step 1: Trocar a linha do item 8** (localizar por conteúdo: `8. Spring Core e Boot *(planejado)* — IoC/DI, AOP, auto-configuration, profiles, Actuator`) por:
```markdown
8. [[03-Dominios/Java/Spring Core e Boot/index|Spring Core e Boot]] — IoC/DI, beans e escopos, AOP/proxies, configuração e profiles, conditional/auto-configuration, eventos do contexto, fundamentos do Boot, Actuator
```
Atualizar `updated: 2026-06-08`. Não mexer no resto.

- [ ] **Step 2: Verificar**
```bash
grep -E "Spring Core e Boot/index" "03-Dominios/Java/index.md"
grep -c "planejado" "03-Dominios/Java/index.md"
```
Expected: wikilink ativo; "planejado" caiu exatamente 1 vs baseline.

- [ ] **Step 3: Commit** — `git add "<path>"` && `git commit -m "feat(java): ativa Galho 8 (Spring Core e Boot) no MOC central"`

---

## Task 22: Poda PARCIAL do tronco (`Backend/Spring Boot.md`) + higiene

**Files:**
- Modify: `03-Dominios/Java/Backend/Spring Boot.md`

- [ ] **Step 1: Ler o tronco e confirmar ranges** (política §9 do roadmap — ler antes de podar)
```bash
grep -nE "^#{2,3} " "03-Dominios/Java/Backend/Spring Boot.md"
```
Confirmar os limites reais das 5 seções core e das seções intocáveis (podem ter deslocado). **Só as seções core são podadas.**

- [ ] **Step 2: Podar `## O que é`** (decisão da execução) — inserir callout no topo da seção, **preservando** a checklist de senior multi-galho (referencia MVC/transações — galhos 9/10 ainda abertos):
```markdown
> [!nota] Migrado para galho próprio
> Os fundamentos de Spring (Framework vs Boot, o stack, convention-over-configuration) foram expandidos no galho [[03-Dominios/Java/Spring Core e Boot/index|Spring Core e Boot]]. Veja [[01 - O que é Spring — Framework, Boot e o ecossistema]].
```

- [ ] **Step 3: Podar `## Spring IoC Container — deep dive`** — substituir TODO o bloco da seção (de `## Spring IoC Container` até imediatamente antes de `## AOP e proxies`) por:
```markdown
## Spring IoC Container — deep dive

> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Java/Spring Core e Boot/index|Spring Core e Boot]]. Veja [[02 - IoC e injeção de dependência no Spring]], [[03 - Beans e estereótipos — @Component, @Service, @Repository, @Controller]], [[04 - Tipos de injeção — constructor, setter, field]], [[05 - @Configuration e @Bean — definição explícita de beans]], [[06 - ApplicationContext — o container e seu ciclo]], [[07 - Ciclo de vida e escopos de beans]], [[13 - BeanPostProcessor e BeanFactoryPostProcessor]], [[14 - Conditional beans — @Conditional e os @ConditionalOn]].
```

- [ ] **Step 4: Podar `## AOP e proxies — a mágica por baixo`** — substituir TODO o bloco (até antes de `## Gerenciamento de transações`) por:
```markdown
## AOP e proxies — a mágica por baixo

> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Java/Spring Core e Boot/index|Spring Core e Boot]]. Veja [[09 - AOP e proxies no Spring]] e [[10 - Self-invocation e os limites do proxy]]. (O comportamento transacional do `@Transactional` — propagation/isolation/rollback — fica para o Galho 10, planejado, na seção de transações abaixo.)
```

- [ ] **Step 5: Podar `## Configuração e Profiles — deep dive`** — substituir TODO o bloco (até antes de `## Actuator`) por:
```markdown
## Configuração e Profiles — deep dive

> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Java/Spring Core e Boot/index|Spring Core e Boot]]. Veja [[12 - Configuração e profiles]].
```

- [ ] **Step 6: Podar `## Actuator — production-ready features`** — substituir TODO o bloco (até antes de `## Spring WebFlux — visão geral`) por:
```markdown
## Actuator — production-ready features

> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Java/Spring Core e Boot/index|Spring Core e Boot]]. Veja [[17 - Actuator e observabilidade]]. (Observabilidade distribuída — OpenTelemetry, tracing — fica para o Galho 17, planejado.)
```

- [ ] **Step 7: Higienizar `## Na prática (da minha experiência)`** (decisão do brainstorming) — substituir a seção (heading + parágrafo MedEspecialista em 1ª pessoa) por uma versão neutra:
```markdown
## Na prática

> [!exemplo] Stack típico de um serviço Spring Boot
> Um backend Spring Boot 3 sobre Java 17+ costuma combinar Spring Data JPA (persistência), Spring Security (autenticação/JWT) e Actuator + Micrometer (métricas), com testes de integração via Testcontainers. Cada uma dessas peças tem (ou terá) galho próprio na trilha — veja [[03-Dominios/Java/Spring Core e Boot/index|Spring Core e Boot]] para o núcleo.
```

- [ ] **Step 8: Atualizar `## Veja também` + frontmatter** — adicionar wikilink `[[03-Dominios/Java/Spring Core e Boot/index|Spring Core e Boot]]` no "Veja também" do tronco; `updated: 2026-06-08`.

- [ ] **Step 9: Verificar (poda cirúrgica — seções de outros galhos intactas)**
```bash
grep -nE "^## " "03-Dominios/Java/Backend/Spring Boot.md"
grep -c "Migrado para galho próprio" "03-Dominios/Java/Backend/Spring Boot.md"
grep -niE "minha experiência|MedEspecialista" "03-Dominios/Java/Backend/Spring Boot.md"
grep -nE "^## (Gerenciamento de transações|Spring MVC pipeline)" "03-Dominios/Java/Backend/Spring Boot.md"
```
Expected: 5 callouts "Migrado"; grep fabricação **VAZIO**; `## Gerenciamento de transações` e `## Spring MVC pipeline` **AINDA PRESENTES** (intocados — galhos 10/9).

- [ ] **Step 10: Commit** — `git add "03-Dominios/Java/Backend/Spring Boot.md"` && `git commit -m "refactor(java): poda parcial do tronco Spring Boot — seções core migram pro galho 8 + higiene de fabricação"`

---

## Task 23: Quitar a dívida reversa (9 ganchos "Galho 8" → wikilinks)

**Files:**
- Modify: `03-Dominios/Java/Linguagem e sintaxe moderna/11 - Annotations.md`
- Modify: `03-Dominios/Java/Jakarta EE/index.md`
- Modify: `03-Dominios/Java/Jakarta EE/04 - CDI — beans e injeção.md`
- Modify: `03-Dominios/Java/Jakarta EE/05 - CDI — escopos e contextos.md`
- Modify: `03-Dominios/Java/Jakarta EE/06 - CDI — qualifiers, producers e eventos.md`
- Modify: `03-Dominios/Java/Jakarta EE/12 - EJB — o legado que moldou a plataforma.md`
- Modify: `03-Dominios/Java/Jakarta EE/13 - CDI avançado — interceptors, decorators e extensões.md`
- Modify: `03-Dominios/Java/JavaFX/11 - Arquitetura — MVC, MVVM e injeção de dependência.md`

- [ ] **Step 1: Relocalizar (por conteúdo — linhas podem ter mudado)**
```bash
grep -rn "Galho 8" "03-Dominios/Java/Linguagem e sintaxe moderna/11 - Annotations.md" "03-Dominios/Java/Jakarta EE/" "03-Dominios/Java/JavaFX/11 - Arquitetura — MVC, MVVM e injeção de dependência.md"
```

- [ ] **Step 2: Aplicar os wikilinks** — em cada ponteiro, trocar o texto "Galho 8 (planejado)"/"Galho 8 (Spring, planejado)" pelo wikilink, **mantendo natural a frase** e atualizando `updated: 2026-06-08` no frontmatter de cada arquivo tocado:
  - **Annotations.md (~309):** `...e com o Galho 8 (Spring, planejado).` → `...e com o galho [[03-Dominios/Java/Spring Core e Boot/index|Spring Core e Boot]] (que implementa esse modelo num container próprio — veja [[03-Dominios/Java/Spring Core e Boot/02 - IoC e injeção de dependência no Spring|IoC e DI no Spring]]).`
  - **Jakarta EE/index.md (~30):** `...é do Galho 8 (planejado)...` → wikilink pra `[[03-Dominios/Java/Spring Core e Boot/index|Spring Core e Boot]]`.
  - **CDI 04 (~24):** `...Spring (Galho 8, planejado) implementa um container próprio...` → `...o Spring ([[03-Dominios/Java/Spring Core e Boot/02 - IoC e injeção de dependência no Spring|IoC e DI no Spring]]) implementa um container próprio...` (simetria-assinatura).
  - **CDI 05 (~48):** `...frameworks construídos sobre essas ideias (Galho 8, planejado) reaproveitam...` → wikilink pra `[[03-Dominios/Java/Spring Core e Boot/07 - Ciclo de vida e escopos de beans|escopos no Spring]]`.
  - **CDI 06 (~42):** `...frameworks de aplicação (Galho 8, planejado)...` [eventos] → wikilink pra `[[03-Dominios/Java/Spring Core e Boot/11 - Eventos do ApplicationContext|eventos do Spring]]`.
  - **EJB 12 (~65):** `...Galho 8 (planejado)...POJOs gerenciados por um contêiner leve...` → wikilink pra `[[03-Dominios/Java/Spring Core e Boot/02 - IoC e injeção de dependência no Spring|Spring]]` (ou nota 01).
  - **EJB 12 (~203):** `...scheduler do servidor/framework do Galho 8...` → wikilink pra `[[03-Dominios/Java/Spring Core e Boot/index|Spring Core e Boot]]` (sem nota dedicada a scheduling — `@Scheduled` é feature AOP citada na 09/16).
  - **CDI 13 (~42):** `...build-time...native...Galho 8, planejado...` → wikilink pra `[[03-Dominios/Java/Spring Core e Boot/15 - Auto-configuration e starters|auto-configuration e AOT]]`.
  - **JavaFX/11 (~35 e ~110):** `...o Spring fica para o Galho 8 (planejado).` → `...o Spring fica para o galho [[03-Dominios/Java/Spring Core e Boot/02 - IoC e injeção de dependência no Spring|Spring Core e Boot]].`

- [ ] **Step 3: Verificar**
```bash
grep -rn "Galho 8" "03-Dominios/Java/Linguagem e sintaxe moderna/11 - Annotations.md" "03-Dominios/Java/Jakarta EE/" "03-Dominios/Java/JavaFX/11 - Arquitetura — MVC, MVVM e injeção de dependência.md" | grep -v "Spring Core e Boot"
grep -rc "Spring Core e Boot" "03-Dominios/Java/Jakarta EE/index.md" "03-Dominios/Java/Jakarta EE/04 - CDI — beans e injeção.md"
```
Expected: primeiro grep **VAZIO** (nenhum "Galho 8 (planejado)" solto sobra); segundo ≥1 cada (wikilinks novos).

- [ ] **Step 4: Commit** — `git add` nominal dos 8 arquivos && `git commit -m "refactor(java): quita dívida reversa do galho 8 — ponteiros Spring viram wikilinks"`

---

## Task 24: Verificação final do galho

**Files:** (somente leitura/verificação)

- [ ] **Step 1: 18 notas + MOC**
```bash
ls "03-Dominios/Java/Spring Core e Boot/" | sort
```
Expected: 01..18 + index.md (19 arquivos).

- [ ] **Step 2: Fases (5/7/6)**
```bash
for f in "03-Dominios/Java/Spring Core e Boot/"[0-9]*.md; do grep -H "^fase:" "$f"; done
```
Expected: 01-05 `iniciado`, 06-12 `adepto`, 13-18 `magus`.

- [ ] **Step 3: Seções obrigatórias (3 por nota)**
```bash
for f in "03-Dominios/Java/Spring Core e Boot/"[0-9]*.md; do echo "$f: $(grep -cE '^## (Em entrevista|Armadilhas|Veja também)' "$f")"; done
```
Expected: 3 em todas.

- [ ] **Step 4: Anti-fabricação + fronteiras (greps decisivos)**
```bash
grep -riE "minha experiência|no meu projeto|josenaldo|Patient|MedEspecialista|market share|% d[ao]s (dev|empresas|projetos)" "03-Dominios/Java/Spring Core e Boot/"
grep -rE "\[\[[^]]*(Galho (9|10|11|12|13|16|17)|WebFlux|Spring Security|Spring Data|Spring Cloud|Hibernate)" "03-Dominios/Java/Spring Core e Boot/"
grep -rn '\[\[#' "03-Dominios/Java/Spring Core e Boot/"
```
Expected: **todos VAZIOS**.

- [ ] **Step 5: Fronteira-assinatura (links de volta ao Galho 7 presentes)**
```bash
grep -rl "Jakarta EE/0[3-8]\|Jakarta EE/1[34]" "03-Dominios/Java/Spring Core e Boot/" | sort
```
Expected: notas 02, 05, 07, 08, 09, 10, 11, 12, 13, 15, 16, 18 linkam pra alguma nota do Galho 7 (conferir as obrigatórias do mapeamento).

- [ ] **Step 6: Frase pronta (1 por nota)**
```bash
for f in "03-Dominios/Java/Spring Core e Boot/"[0-9]*.md; do echo "$f: $(grep -c '### Frase pronta (inglês)' "$f")"; done
```
Expected: 1 em todas.

- [ ] **Step 7: Tronco — poda cirúrgica confirmada**
```bash
grep -c "Migrado para galho próprio" "03-Dominios/Java/Backend/Spring Boot.md"
grep -nE "^## (Gerenciamento de transações|Spring MVC pipeline|Spring WebFlux|Spring Cloud)" "03-Dominios/Java/Backend/Spring Boot.md"
git status --short "03-Dominios/Java/Backend/Spring Data JPA.md" "03-Dominios/Java/Backend/Kafka/"
```
Expected: 5 callouts; seções de galhos 9/10/11/16 presentes; `Spring Data JPA.md`/`Kafka/` **sem modificação** (working tree limpa ali).

- [ ] **Step 8: Skill `verificar-wikilinks`** — rodar na pasta `03-Dominios/Java/Spring Core e Boot/` + conferir os arquivos tocados fora (MOC central, Dicionário, tronco, Annotations.md, os 5 arquivos Jakarta EE da dívida reversa, JavaFX/11). Âncoras `Dicionário de Java#...` resolvem 1:1 (cross-check com o grep da Task 20 Step 1). As ~204 quebras legadas da árvore Java NÃO são deste galho — só corrigir o que este galho introduziu. Corrigir e commitar à parte se houver.

- [ ] **Step 9: Resumo de fechamento (sem commit)** — reportar: 18 notas (5/7/6), ~37 verbetes (202→~239), MOC galho + MOC central, **poda parcial cirúrgica** (5 seções core migradas, transações/MVC intactas, fabricação higienizada), **dívida reversa quitada** (9 ganchos), troncos vizinhos intocados (mostrar o grep), wikilinks limpos. Commits locais na `main`; **push manual do usuário; sem deploy**. Atualizar memória [[project_trilha_java]] com Galho 8 completo + fatos cravados (Boot 3.x/Framework 6.x, `AutoConfiguration.imports`, baseline Java 17/`jakarta.*`).

---

## Self-Review (preenchido na escrita do plano)

**Spec coverage:** Tasks 1-18 ↔ spec §3.1 (18 notas, escopos idênticos, opus 02/09/15/18, distribuição 5/7/6); Task 19 ↔ §3.2 (MOC, 5 rotas iguais); Task 20 ↔ §3.3 (~37 verbetes, âncoras 1:1 por grep, `@Transactional` desambiguado); Task 21 ↔ §3.4 (linha 38); Task 22 ↔ §3.5 (poda parcial das 5 seções core + higiene da seção órfã; transações/MVC intactas); Task 23 ↔ §3.6 (9 ganchos, mapeamento idêntico); Task 0 ↔ §6 (pré-flight, baseline 202, ranges do tronco); Task 24 ↔ §7. Fronteira-assinatura (§4.3.1) garantida por links obrigatórios pro Galho 7 nas Tasks 2/5/7/8/9/10/11/12/13/15/16/18 e pelo grep da Task 24 Step 5; fronteira galhos 9-17 pelo grep da Task 24 Step 4.

**Placeholder scan:** sem TBD/TODO; cada nota tem fonte WebFetch nomeada com URL, frontmatter concreto, H3s, armadilhas mínimas com conteúdo real, tamanho-alvo herdado das convenções. Pontos version-sensitive marcados com "verificar/confirmar" são instruções de verificação WebFetch (parte pesquisa do galho híbrido), não placeholders: versão atual Boot 3.x/Framework 6.x, `AutoConfiguration.imports` vs `spring.factories`, default de deps circulares Boot 2.6+, coordenada exata de starters. A decisão de poda do `## O que é` (Task 22 Step 2) é resolução-na-execução por política §9 do roadmap (ler o tronco primeiro), com default conservador explícito.

**Type/naming consistency:** numeração 01-18 idêntica entre tasks, MOC, Dicionário, dívida reversa, poda e cheatsheet da capstone; distribuição 5/7/6 consistente; opus 02/09/15/18 marcadas ⟦opus⟧; filenames com em dash (sem `:`/`/` — nota 14 usa `@ConditionalOn` sem `*` no filename pra evitar glob); mapeamento de links Galho 7→nota consistente entre spec §3.1, convenções e Tasks; âncoras do Dicionário extraídas por grep antes de inserir (Task 20) e validadas na Task 24; `@Transactional (Spring)` vs `@Transactional (Jakarta)` desambiguados (verbetes distintos que se linkam).
