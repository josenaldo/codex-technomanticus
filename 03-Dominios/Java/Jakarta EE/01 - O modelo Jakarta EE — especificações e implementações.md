---
title: "O modelo Jakarta EE — especificações e implementações"
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
  - "Jakarta EE"
  - "Especificações Jakarta"
  - "Java EE"
---

> [!abstract] TL;DR
> Jakarta EE não é um produto — é um **conjunto de especificações** (contratos de API) mantido pela Eclipse Foundation, com múltiplas implementações certificadas por um kit de testes chamado TCK. Quando você usa Spring, boa parte do que acontece por baixo — persistência, transações, injeção de dependências — segue esses mesmos contratos. Entender o modelo desbloqueia todo o restante do galho.

## O que é

Jakarta EE é uma **plataforma de especificações** para desenvolvimento Java enterprise, mantida pela Eclipse Foundation sob um modelo de governança neutro onde todos os membros têm igual poder de voto.

O ponto central para entender Jakarta EE é distinguir **especificação** de **implementação**. Cada tecnologia da plataforma é definida por um trio inseparável:

| Componente | O que é | Exemplo (JPA) |
|---|---|---|
| **API jar** | Interfaces, anotações e contratos compiláveis | `jakarta.persistence.*` |
| **Spec document** | Documento em linguagem natural que define o comportamento exato | Jakarta Persistence 3.2 Specification |
| **TCK** | Test Compatibility Kit — suíte de testes que qualquer implementação precisa passar para ser certificada | Jakarta Persistence TCK |

> [!tip] A analogia do contrato
> Uma especificação Jakarta é como um contrato assinado: define o que deve acontecer, mas não como. A implementação é quem assina e executa o contrato.

**JPA não é o Hibernate**: JPA (Jakarta Persistence API) é o contrato. Hibernate é uma implementação desse contrato. EclipseLink é outra. Seu código compila contra a API; qual implementação roda em produção é decisão do servidor ou do `pom.xml`.

Esse modelo garante portabilidade: uma aplicação escrita contra os contratos Jakarta EE pode, em teoria, rodar em qualquer servidor certificado sem alteração de código.

## Por que importa

Antes de mergulhar em CDI, JPA, REST e as outras specs, é essencial ter esse modelo mental claro — porque ele reaparece em cada galho.

Entrevistas internacionais testam exatamente essa distinção:

- "Qual a diferença entre JPA e Hibernate?"
- "Por que minha aplicação rodava no GlassFish mas quebrou no Tomcat?"
- "O que é um container Jakarta EE?"

Todas essas perguntas têm a mesma raiz: **spec vs. implementação vs. perfil**.

E mais: quando você usa `@Transactional` ou `@Autowired` no Spring, o que acontece por baixo envolve exatamente esses contratos Jakarta EE. A nota [[14 - Jakarta EE hoje — a plataforma sob o Spring]] explora esse elo com profundidade.

## Como funciona

### Anatomia de uma spec (API, documento, TCK, implementação ratificadora)

O ciclo de vida de uma especificação Jakarta EE segue o Jakarta EE Specification Process (JESP):

1. Uma equipe de especialistas propõe e redige a spec
2. A spec define a API (interfaces/anotações) e o comportamento esperado
3. O TCK é escrito em paralelo — é o árbitro objetivo da conformidade
4. Uma **implementação ratificadora** passa o TCK completo antes da spec ser finalizada (para Jakarta EE 11, foi o Eclipse GlassFish)
5. Outras implementações podem se certificar depois, passando o mesmo TCK

Qualquer produto que queira se chamar de "implementação certificada Jakarta EE" precisa passar o TCK da versão correspondente. Não há exceção.

### Os 3 perfis (Platform / Web Profile / Core Profile)

Jakarta EE não é monolítico: existe em três perfis com escopos diferentes.

```text
┌─────────────────────────────────────────────────────┐
│               Jakarta EE Platform                   │  ← tudo
│  ┌──────────────────────────────────────────────┐   │
│  │           Jakarta EE Web Profile             │   │  ← web + data
│  │  ┌───────────────────────────────────────┐   │   │
│  │  │      Jakarta EE Core Profile          │   │   │  ← cloud-native mínimo
│  │  └───────────────────────────────────────┘   │   │
│  └──────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

**Core Profile** — o menor subconjunto, voltado para runtimes cloud-native e microserviços. Contém:
- CDI Lite 4.1 (subconjunto de CDI sem decorators, portable extensions, specialization e escopos de sessão/conversação — pensado pra resolução em build-time)
- RESTful Web Services 4.0
- JSON Processing 2.1
- JSON Binding 3.0
- Annotations 3.0
- Interceptors 2.2
- Dependency Injection 2.0

**Web Profile** — inclui tudo do Core Profile mais as tecnologias web completas:
- Servlet 6.1, Pages 4.0, Faces 4.1
- CDI 4.1 completo, Validation 3.1
- Persistence 3.2, Transactions 2.0
- Concurrency 3.1, Security 4.0, WebSocket 2.2
- Enterprise Beans Lite 4.0

**Platform (completa)** — inclui tudo do Web Profile mais tecnologias enterprise avançadas:
- Enterprise Beans 4.0 (EJB completo)
- Batch 2.1, Messaging 3.1, Connectors 2.1
- Mail 2.1, Activation 2.1

> [!question] Qual perfil preciso?
> Para APIs REST e microsserviços simples: Core Profile. Para aplicações web com banco de dados: Web Profile. Para sistemas enterprise com filas, batch e conectores: Platform.

### Onde roda

Nem todo servidor Java é igual. O perfil que um servidor implementa determina o que está disponível:

| Tipo de runtime | Exemplos | O que implementa |
|---|---|---|
| **App server completo** | WildFly, Payara Server, GlassFish, Open Liberty, WebSphere Liberty | Platform ou Web Profile certificados |
| **Servlet container** | Tomcat, Jetty | Apenas Servlet + JSP — **sem CDI, JPA ou EJB nativos** |
| **Runtime cloud-native** | Open Liberty (modo Core), WildFly (modo slim) | Core Profile |

Tomcat é amplamente usado com Spring, mas **Tomcat não é um servidor Jakarta EE**. Ele implementa apenas as specs Servlet/JSP. CDI, JPA e transações no Tomcat chegam via Spring ou outras libs externas — não nativamente.

### As specs deste galho no EE 11

A tabela abaixo lista as especificações cobertas neste Galho 7, todas na versão do Jakarta EE 11 (lançado em 2025):

| Especificação | Versão no EE 11 | Perfil mínimo | Notas do galho |
|---|---|---|---|
| CDI (Contexts and Dependency Injection) | 4.1 | Core (Lite) / Web (completo) | Galho: notas 04-06/13 |
| Servlet | 6.1 | Web Profile | Galho: nota 03 |
| RESTful Web Services (JAX-RS) | 4.0 | Core Profile | Galho: nota 07 |
| Bean Validation | 3.1 | Web Profile | Galho: nota 08 |
| Persistence (JPA) | 3.2 | Web Profile | Galho: nota 09 |
| Transactions (JTA) | 2.0 | Web Profile | Galho: nota 11 |
| Enterprise Beans (EJB) | 4.0 | Platform | Galho: nota 12 |

> [!info] Fonte
> Versões confirmadas em [jakarta.ee/specifications](https://jakarta.ee/specifications/) em 2026-06-07. Jakarta EE 12 está em desenvolvimento no mesmo período.

## Na prática

O ponto de entrada mais comum em projetos Maven é declarar a API da plataforma como dependência com escopo `provided` — o servidor vai fornecer a implementação em runtime:

```xml
<dependencies>
    <!-- Jakarta EE 11 Platform API — compile-time apenas -->
    <!-- A implementação é provida pelo servidor de aplicação -->
    <dependency>
        <groupId>jakarta.platform</groupId>
        <artifactId>jakarta.jakartaee-api</artifactId>
        <version>11.0.0</version>
        <scope>provided</scope>
    </dependency>
</dependencies>
```

Com isso, seu código compila contra os contratos oficiais:

```java
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.GeneratedValue;
import jakarta.inject.Inject;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.Path;

@Entity
public class Order {

    @Id
    @GeneratedValue
    private Long id;

    private String customer;

    // getters e setters...
}

@Path("/orders")
public class OrderResource {

    @Inject
    private OrderRepository repository;

    @GET
    public List<Order> listAll() {
        return repository.findAll();
    }
}
```

Note que o código não importa nenhuma classe do Hibernate, do WildFly ou do GlassFish. Tudo é `jakarta.*`. Qual implementação executa isso é decisão do servidor — e é exatamente isso que garante portabilidade.

> [!tip] scope=provided é obrigatório
> Sem `provided`, o API jar vai parar dentro do WAR junto com a implementação do servidor, causando conflitos de classes. O servidor já carrega as implementações; o API jar é apenas para compilar.

## Armadilhas

### (1) Confundir a spec com a implementação

**Problema:** "Preciso instalar o JPA no servidor" ou "minha versão do JPA é 6.x" (confundindo com a versão do Hibernate).

**Como acontece:**

```xml
<!-- ERRADO: adicionando impl no compile sem provided -->
<dependency>
    <groupId>org.hibernate.orm</groupId>
    <artifactId>hibernate-core</artifactId>
    <version>6.5.0.Final</version>
    <!-- sem <scope>provided</scope> -->
</dependency>
```

O código funciona, mas agora você depende explicitamente do Hibernate, perde portabilidade e provavelmente enfrenta conflito de classes em servidores que já trazem Hibernate embutido.

**Fix:** dependa da API com `provided`, deixe a impl para o servidor:

```xml
<dependency>
    <groupId>jakarta.platform</groupId>
    <artifactId>jakarta.jakartaee-api</artifactId>
    <version>11.0.0</version>
    <scope>provided</scope>
</dependency>
```

### (2) Assumir que todo runtime implementa a Platform completa

**Problema:** Configurar CDI, JPA e `@Transactional` num projeto deployado em Tomcat e não entender por que nada injeta ou persiste.

**Como acontece:** Tomcat implementa apenas Servlet + JSP. Não tem contêiner CDI, não tem provedor JPA, não tem gerenciador de transações JTA nativos. Rodar nele sem Spring (ou Weld + Hibernate + Narayana manuais) resulta em `NullPointerException` nos pontos de injeção e entidades não gerenciadas.

**Fix:** Antes de escolher o runtime, verifique qual perfil Jakarta EE ele implementa (ou se é apenas um servlet container). Consulte [jakarta.ee/compatibility](https://jakarta.ee/compatibility/) para a lista de certificados.

### (3) Misturar versões de API e servidor incompatíveis

**Problema:** Compilar com `jakarta.jakartaee-api:11.0.0` e fazer deploy num servidor que implementa Jakarta EE 10 (ou Java EE 8).

**Como acontece:** Jakarta EE 11 usa `jakarta.*`. Jakarta EE 8 e anteriores usavam `javax.*`. Mesmo dentro de `jakarta.*`, versões de API diferentes têm assinaturas de métodos diferentes. Um WAR compilado contra EE 11 **não roda** num servidor EE 10 sem recompilação.

**Fix:** Identifique qual versão de Jakarta EE o servidor alvo implementa (documentação do servidor ou a página de certificações) e compile contra a mesma versão de API. Use a mesma versão de ponta a ponta:

```text
Servidor: WildFly 34 → Jakarta EE 11
API: jakarta.jakartaee-api:11.0.0 ✓

Servidor: WildFly 27 → Jakarta EE 10
API: jakarta.jakartaee-api:10.0.0 ✓

Mismatch: WildFly 27 + jakarta.jakartaee-api:11.0.0 ✗
```

## Em entrevista

### Frase pronta (inglês)

"Jakarta EE is a set of specifications — not a product — where each spec defines an API contract, a written specification document, and a TCK that any implementation must pass to be certified. This separation between spec and implementation means you can write your code against the `jakarta.persistence` API and switch between Hibernate and EclipseLink without touching a single line of business logic. The trade-off is that you're dependent on a compliant runtime, so dropping to a plain servlet container like Tomcat means losing CDI, JPA, and JTA unless you wire those implementations in yourself."

### Vocabulário

| Termo PT | Termo EN |
|---|---|
| Especificação | Specification |
| Implementação certificada | Certified compatible implementation |
| Kit de compatibilidade de testes | Technology Compatibility Kit (TCK) |
| Perfil | Profile |
| Contêiner | Container |
| Escopo de dependência | Dependency scope |
| Portabilidade | Portability |
| Servidor de aplicação | Application server |
| Perfil Web | Web Profile |
| Perfil Núcleo | Core Profile |

## Veja também

- [[02 - De Java EE a Jakarta EE]]
- [[04 - CDI — beans e injeção]]
- [[14 - Jakarta EE hoje — a plataforma sob o Spring]]
- [[03-Dominios/Java/Jakarta EE/index|Jakarta EE (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Dicionário de Java#Jakarta EE|Jakarta EE (Dicionário)]]
- [[03-Dominios/Java/Dicionário de Java#Web Profile|Web Profile (Dicionário)]]
- [[03-Dominios/Java/Dicionário de Java#Core Profile|Core Profile (Dicionário)]]

## Referências

- Jakarta EE — About. Eclipse Foundation. Disponível em: <https://jakarta.ee/about/>. Acesso em: 2026-06-07.
- Jakarta EE Specifications. Eclipse Foundation. Disponível em: <https://jakarta.ee/specifications/>. Acesso em: 2026-06-07.
- Jakarta EE 11 Platform Specification. Eclipse Foundation. Disponível em: <https://jakarta.ee/specifications/platform/11/>. Acesso em: 2026-06-07.
- Jakarta EE Compatibility — Certified Products. Eclipse Foundation. Disponível em: <https://jakarta.ee/compatibility/>. Acesso em: 2026-06-07.
- Jakarta EE 11 Certification Results. Eclipse Foundation. Disponível em: <https://jakarta.ee/compatibility/certification/11/>. Acesso em: 2026-06-07.
