---
title: "De Java EE a Jakarta EE"
created: 2026-06-07
updated: 2026-06-07
type: concept
progress: backlog
status: seedling
publish: true
fase: iniciado
tags:
  - java
  - jakarta-ee
  - iniciado
  - especificacao
aliases:
  - "javax para jakarta"
  - "Transição Java EE Jakarta EE"
  - "Jakarta EE 9"
---

> [!abstract] TL;DR
> Java EE virou Jakarta EE quando a Oracle doou a plataforma à Eclipse Foundation (2017), mas reteve a trademark "Java" — daí o **rename big-bang `javax.*` → `jakarta.*` no EE 9 (2020)**, que partiu o ecossistema em dois mundos de namespace. Jakarta EE 8 foi a transição de governança *sem* rename; EE 9 foi o rename *sem* features novas; EE 10 em diante é onde a plataforma voltou a evoluir de verdade.

## O que é

A história de Jakarta EE é uma história de governança: quem controla a plataforma enterprise Java e quem decide seu futuro.

A plataforma nasceu como **J2EE** (Java 2 Platform, Enterprise Edition) na Sun Microsystems em 1999. Com o Java EE 5 (2006), o nome foi simplificado para **Java EE** — o "2" caiu, mas o controle continuou na Sun e depois na Oracle. Em 2010, a Oracle adquiriu a Sun e se tornou a guardiã da plataforma.

Em **setembro de 2017**, a Oracle doou o projeto à **Eclipse Foundation**. Essa decisão foi recebida com entusiasmo pela comunidade, que esperava um ritmo de desenvolvimento mais ágil sob governança neutra. Porém, a transição veio com uma restrição crítica: a Oracle reteve as marcas registradas do nome "Java" e do prefixo de pacote `javax.*`.

O resultado prático foi um rename obrigatório: todo código novo da plataforma precisaria usar o namespace `jakarta.*` em vez de `javax.*`. Esse rename aconteceu no **Jakarta EE 9** (dezembro de 2020) e é o evento central desta nota.

## Por que importa

Qualquer desenvolvedor Java enterprise que trabalha com bases de código reais vai se deparar com esta fronteira. As perguntas aparecem em várias formas:

- "Por que meus imports `javax.persistence.*` quebraram ao trocar de servidor?"
- "Qual versão de Hibernate eu uso com Jakarta EE 10?"
- "Por que essa lib de terceiros só funciona com a versão antiga?"

A resposta para todas é a mesma: o **mundo `javax` e o mundo `jakarta` são incompatíveis no classpath**. Entender o porquê histórico e técnico do rename é o que permite diagnosticar e resolver esses problemas com clareza.

Em entrevistas internacionais, a pergunta sobre a diferença entre Java EE e Jakarta EE é frequente — especialmente a parte do *por que* o rename aconteceu e *quando* ele efetivamente mudou o namespace.

## Como funciona

### Linha do tempo: de J2EE até hoje

| Versão | Data | Namespace | Marco |
|---|---|---|---|
| J2EE 1.2 | Dez/1999 | `javax.*` | Lançamento original (Sun) |
| J2EE 1.4 | Nov/2003 | `javax.*` | Web services integrados |
| Java EE 5 | Mai/2006 | `javax.*` | Rename: J2EE → Java EE; anotações introduzidas |
| Java EE 6 | Dez/2009 | `javax.*` | CDI, Bean Validation, JAX-RS |
| Java EE 7 | Jun/2013 | `javax.*` | WebSocket, JSON-P, Batch |
| Java EE 8 | Set/2017 | `javax.*` | Última versão sob Oracle |
| **Jakarta EE 8** | **10/set/2019** | **`javax.*`** | **Primeira versão Eclipse Foundation — sem rename** |
| **Jakarta EE 9** | **08/dez/2020** | **`jakarta.*`** | **Big-bang rename — sem features novas** |
| **Jakarta EE 9.1** | **25/mai/2021** | `jakarta.*` | Adiciona suporte a Java SE 11 |
| **Jakarta EE 10** | **22/set/2022** | `jakarta.*` | Core Profile novo; evolução das specs |
| **Jakarta EE 11** | **26/jun/2025** | `jakarta.*` | Jakarta Data; suporte a Java 21 |
| Jakarta EE 12 | Em desenvolvimento | `jakarta.*` | WIP na data desta nota (2026-06-07) |

> [!info] Fontes das datas
> Datas verificadas em [jakarta.ee/release/](https://jakarta.ee/release/) em 2026-06-07. A transição J2EE→Java EE no Java EE 5 é amplamente documentada; a data exata de cada versão antiga foi confirmada via documentação histórica Oracle/Sun.

### Por que o rename (a questão da trademark)

O nó da questão é a propriedade intelectual. Quando a Oracle doou a plataforma à Eclipse Foundation, a doação não incluiu as marcas registradas do nome "Java" nem do prefixo de pacote `javax.*`.

O resultado ficou documentado em comunicado oficial da Eclipse Foundation (maio de 2019):

> *"o namespace `javax` não pode ser evoluído pela comunidade Jakarta EE. Da mesma forma, marcas Java como os nomes existentes de especificações não podem ser usadas."*

Em termos práticos: a Eclipse Foundation podia usar `javax.*` **como estava**, mas **não podia adicionar nada novo** a esse namespace. Qualquer nova API, qualquer evolução de spec existente, teria que usar o novo namespace `jakarta.*`.

A comunidade debateu duas estratégias:

1. **Migração gradual**: novas specs usariam `jakarta.*`; specs antigas continuariam em `javax.*` por um período de convivência.
2. **Big-bang rename**: todas as specs, antigas e novas, migram de uma vez para `jakarta.*` numa única versão.

A estratégia escolhida foi o **big-bang rename no Jakarta EE 9**. O racional: uma migração gradual criaria um período indefinido com dois namespaces misturados, tornando o ecossistema de ferramentas, servidores e bibliotecas muito mais difícil de gerenciar. Melhor uma ruptura limpa e única.

Por isso, o Jakarta EE 9 **não trouxe nenhuma feature nova**: seu único propósito foi fazer o rename de todas as APIs existentes de `javax.*` para `jakarta.*`. Foi uma versão de transição técnica pura.

### O impacto prático: dois mundos de namespace

O rename criou uma linha divisória no ecossistema:

**Mundo `javax` (Java EE / Jakarta EE 8 e anteriores):**
- Servidores: JBoss/WildFly ≤ 26, Payara ≤ 5, GlassFish ≤ 5, WebSphere Liberty ≤ 21.x (modo legado), Tomcat ≤ 9 (para Servlet)
- Hibernate ORM ≤ 5.x
- Spring Boot ≤ 2.x (internamente usa `javax.*`)

**Mundo `jakarta` (Jakarta EE 9+ ):**
- Servidores: WildFly ≥ 27, Payara ≥ 6, GlassFish ≥ 6 (dez/2020, EE 9), Open Liberty ≥ 22.x, Tomcat ≥ 10 (para Servlet)
- Hibernate ORM ≥ 6.x
- Spring Boot ≥ 3.x (migrou para `jakarta.*`)

Esses dois mundos são **binariamente incompatíveis**: você não pode misturar uma biblioteca compilada contra `javax.persistence` com um servidor que só entende `jakarta.persistence` sem transformação de bytecode.

**Eclipse Transformer** — para projetos que precisam cruzar essa fronteira sem recompilar, existe o Eclipse Transformer (projeto confirmado em [projects.eclipse.org/projects/technology.transformer](https://projects.eclipse.org/projects/technology.transformer)). É uma ferramenta que reescreve referências de tipo em class files e archives (JAR, WAR) em tempo de transformação ou até em tempo de carregamento de classe. Seu propósito inicial foi exatamente a migração `javax.*` → `jakarta.*`. Útil para adaptar bibliotecas de terceiros sem acesso ao código-fonte.

### Como identificar o "mundo" de um projeto

Três sinais claros para diagnosticar em qual namespace um projeto está:

**1. Os imports do código Java:**

```java
// Mundo javax (Java EE / Jakarta EE 8-)
import javax.persistence.Entity;
import javax.inject.Inject;
import javax.ws.rs.GET;

// Mundo jakarta (Jakarta EE 9+)
import jakarta.persistence.Entity;
import jakarta.inject.Inject;
import jakarta.ws.rs.GET;
```

**2. As versões das dependências Maven:**

```xml
<!-- Mundo javax -->
<dependency>
    <groupId>javax</groupId>
    <artifactId>javaee-api</artifactId>
    <version>8.0</version>
</dependency>

<!-- Mundo jakarta -->
<dependency>
    <groupId>jakarta.platform</groupId>
    <artifactId>jakarta.jakartaee-api</artifactId>
    <version>11.0.0</version>
    <scope>provided</scope>
</dependency>
```

**3. A versão do servidor de aplicação** e sua página de certificação Jakarta EE em [jakarta.ee/compatibility/](https://jakarta.ee/compatibility/).

## Na prática

### O diff que tudo resume

Esta é a mudança central do Jakarta EE 9. Nenhuma lógica de negócio muda — apenas o prefixo do pacote:

```java
// Antes (Java EE / Jakarta EE 8) — mundo javax
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.GeneratedValue;
import javax.inject.Inject;
import javax.ws.rs.GET;
import javax.ws.rs.Path;

@Entity
public class Product {
    @Id
    @GeneratedValue
    private Long id;
    private String name;
}
```

```java
// Depois (Jakarta EE 9+) — mundo jakarta
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.GeneratedValue;
import jakarta.inject.Inject;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.Path;

@Entity
public class Product {
    @Id
    @GeneratedValue
    private Long id;
    private String name;
}
```

> [!warning] Contexto desta nota
> Os imports `javax.*` acima aparecem **exclusivamente** para ilustrar a transição histórica. Em qualquer código novo, use sempre `jakarta.*`. Esta é a única nota do galho onde `javax.*` aparece com essa finalidade explícita.

### Tabela spec → artefato pré e pós-rename

| Especificação | Artefato pré-EE 9 (javax) | Artefato pós-EE 9 (jakarta) |
|---|---|---|
| Persistence (JPA) | `javax.persistence:javax.persistence-api` | `jakarta.persistence:jakarta.persistence-api` |
| CDI | `javax.enterprise:cdi-api` | `jakarta.enterprise:jakarta.enterprise.cdi-api` |
| RESTful Web Services | `javax.ws.rs:javax.ws.rs-api` | `jakarta.ws.rs:jakarta.ws.rs-api` |
| Servlet | `javax.servlet:javax.servlet-api` | `jakarta.servlet:jakarta.servlet-api` |
| Bean Validation | `javax.validation:validation-api` | `jakarta.validation:jakarta.validation-api` |
| Platform completa | `javax:javaee-api` | `jakarta.platform:jakarta.jakartaee-api` |

### Checklist de migração (hipotético)

> [!warning] Hipotético
> Este checklist é ilustrativo. Projetos reais têm variações; avalie sempre o contexto específico antes de executar qualquer migração.

- [ ] Identificar versão atual do servidor e a versão Jakarta EE que ele implementa
- [ ] Decidir o namespace-alvo (manter em `javax` ou migrar para `jakarta`)
- [ ] Atualizar versão da dependência de API (`javaee-api` → `jakarta.jakartaee-api`)
- [ ] Atualizar versão do servidor para uma certificada no namespace-alvo
- [ ] Fazer replace global `javax.` → `jakarta.` nos imports do código-fonte
- [ ] Atualizar dependências de libs de terceiros para versões que suportam o namespace-alvo
- [ ] Checar arquivos de configuração XML (persistence.xml, web.xml, beans.xml) — o namespace também muda em alguns
- [ ] Rodar testes de integração contra o novo servidor antes de promover

## Armadilhas

### (1) Misturar `javax.*` e `jakarta.*` no mesmo classpath

**Problema:** A aplicação compila, mas falha em runtime com `ClassNotFoundException`, `NoSuchMethodError` ou comportamento silenciosamente errado.

**Como acontece:** Uma biblioteca de persistência compilada contra `javax.persistence.Entity` e um servidor que carrega `jakarta.persistence.Entity` enxergam tipos completamente diferentes. A JVM não os identifica como o mesmo tipo — o rename é uma ruptura binária real.

```xml
<!-- CONFLITO: lib do mundo javax num projeto do mundo jakarta -->
<dependency>
    <groupId>com.alguma-lib</groupId>
    <artifactId>alguma-lib</artifactId>
    <version>2.3.0</version> <!-- compilada contra javax.* -->
</dependency>
<!-- servidor rodando Jakarta EE 10 (jakarta.*) -->
```

**Fix:** Alinhe TODAS as dependências num único mundo. Para libs sem versão `jakarta.*`, avalie o Eclipse Transformer ou busque um fork compatível.

### (2) Assumir que Jakarta EE 8 já usa `jakarta.*`

**Problema:** O nome "Jakarta EE 8" sugere que é a primeira versão Jakarta — e é. Mas o namespace ainda é `javax.*`.

**Como acontece:** Jakarta EE 8 foi a **transição de governança** (de Oracle para Eclipse Foundation), não a transição de namespace. Ela foi lançada em setembro de 2019 como uma versão funcionalmente idêntica ao Java EE 8, apenas sob nova gestão. O rename só veio no **Jakarta EE 9** (dezembro de 2020).

```java
// Jakarta EE 8: ainda javax! Não é jakarta.*
import javax.persistence.Entity; // ← isso é Jakarta EE 8, não Java EE antigo
```

**Fix:** Ao identificar o mundo de um projeto, verifique a **versão** do Jakarta EE — não apenas o prefixo do nome. Jakarta EE 8 = `javax.*`; Jakarta EE 9+ = `jakarta.*`.

### (3) Fazer deploy de app `javax` em servidor `jakarta` (ou vice-versa) sem transformer

**Problema:** O deploy aparentemente funciona (sem erro de deploy), mas a aplicação falha em runtime com erros de classe não encontrada ou injeção nula.

**Como acontece:** Um servidor Jakarta EE 10 carrega `jakarta.persistence.EntityManager`. Se sua aplicação procura `javax.persistence.EntityManager`, a JVM não encontra nenhum bean ou componente injetado — são tipos diferentes do ponto de vista do classloader.

```text
Erro típico:
WELD-001408: Unsatisfied dependencies for type EntityManager
              with qualifiers @Default
→ causa raiz: servidor fala jakarta.*, app fala javax.*
```

**Fix:** Ou migre a aplicação para o namespace do servidor, ou use o Eclipse Transformer para reescrever o bytecode da aplicação antes do deploy, ou use um servidor que implemente o namespace compatível com o código.

## Em entrevista

### Frase pronta (inglês)

"Oracle donated the platform to the Eclipse Foundation in 2017, and the first Jakarta EE release shipped in 2019, but Oracle retained the 'Java' trademark and the `javax` package namespace, which meant the community couldn't evolve any existing API under `javax.*`. To resolve this cleanly, Jakarta EE 9 in December 2020 did a big-bang rename of all APIs from `javax.*` to `jakarta.*` with no new features — it was a pure namespace migration release. The practical implication is that libraries and servers compiled against `javax` and those compiled against `jakarta` are binary-incompatible, so migrating a project means aligning every dependency and the runtime to the same namespace world."

### Vocabulário

| Termo PT | Termo EN |
|---|---|
| Rename big-bang | Big-bang rename |
| Marca registrada / trademark | Trademark |
| Namespace de pacote | Package namespace |
| Transição de governança | Governance transition |
| Incompatibilidade binária | Binary incompatibility |
| Transformação de bytecode | Bytecode transformation |
| Prefixo de pacote | Package prefix |
| Fundação Eclipse | Eclipse Foundation |
| Doação de projeto | Project donation |
| Versão de transição | Transition release |

## Veja também

- [[01 - O modelo Jakarta EE — especificações e implementações]]
- [[14 - Jakarta EE hoje — a plataforma sob o Spring]]
- [[03-Dominios/Java/Jakarta EE/index|Jakarta EE (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Dicionário de Java#javax → jakarta (rename)|javax → jakarta (Dicionário)]]
- [[03-Dominios/Java/Dicionário de Java#Jakarta EE|Jakarta EE (Dicionário)]]

## Referências

- Jakarta EE — Releases. Eclipse Foundation. Disponível em: <https://jakarta.ee/release/>. Acesso em: 2026-06-07.
- Jakarta EE 9 Release. Eclipse Foundation. Disponível em: <https://jakarta.ee/release/9/>. Acesso em: 2026-06-07.
- Jakarta EE 10 Release. Eclipse Foundation. Disponível em: <https://jakarta.ee/release/10/>. Acesso em: 2026-06-07.
- Jakarta EE 11 Release. Eclipse Foundation. Disponível em: <https://jakarta.ee/release/11/>. Acesso em: 2026-06-07.
- Milinkovich, Mike. Jakarta EE and the Java Trademarks. Eclipse Foundation Blog, mai/2019. Disponível em: <https://eclipse-foundation.blog/2019/05/03/jakarta-ee-java-trademarks/>. Acesso em: 2026-06-07.
- Eclipse Transformer — Eclipse Technology Project. Disponível em: <https://projects.eclipse.org/projects/technology.transformer>. Acesso em: 2026-06-07.
