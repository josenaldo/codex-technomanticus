---
title: "Caching — 1º nível, 2º nível e Spring Cache"
created: 2026-06-09
updated: 2026-06-09
type: concept
progress: backlog
status: seedling
publish: true
fase: Magus
tags:
  - java
  - persistencia
  - magus
  - cache
aliases:
  - "second-level cache"
  - "Spring Cache"
  - "cache JPA"
---

# Caching — 1º nível, 2º nível e Spring Cache

> [!abstract] TL;DR
> Existem **três níveis de cache** em jogo numa aplicação JPA + Spring, e confundi-los é fonte garantida de bug:
> - **1º nível (L1)** — o *persistence context*. Vive **por transação**, é **automático e sempre ativo**, não dá pra desligar. Garante identidade de entidade dentro de uma sessão.
> - **2º nível (L2)** — cache de entidade **application-wide**, **opt-in**. Liga-se com `@Cacheable` + `@Cache(usage = ...)` na entidade. Serve pra **dados de referência** (lidos muito, mudados pouco).
> - **Spring Cache** — abstração que cacheia **valores de retorno de métodos** na camada **Service**, *acima* da JPA, com `@Cacheable`/`@CacheEvict`/`@CachePut`. Providers: Caffeine, Redis, Hazelcast.
>
> Não são a mesma coisa, não vivem na mesma camada e não resolvem o mesmo problema.

## O que é

Cache, no contexto de persistência, é qualquer camada que evita ir ao banco quando o dado já está disponível em memória. O ponto delicado é que numa stack Java moderna existem **três caches distintos**, em três camadas diferentes, com ciclos de vida que não conversam entre si:

1. O **cache de primeiro nível** é parte intrínseca do `EntityManager`/`Session` — é o próprio *persistence context*. Toda operação JPA passa por ele, querendo você ou não.
2. O **cache de segundo nível** é uma camada do `EntityManagerFactory`/`SessionFactory`, compartilhada por todas as transações da aplicação. É opcional e precisa ser configurado explicitamente.
3. O **Spring Cache** nem sabe que existe JPA. É uma abstração genérica que intercepta chamadas de método e guarda o retorno, indexado pelos argumentos.

A confusão clássica de entrevista (e de produção) é tratar os três como se fossem o mesmo botão de "ligar cache".

## Por que importa

- **L1** é a razão de a mesma `Order` carregada duas vezes na mesma transação ser **o mesmo objeto** (`==`). Entender isso explica por que `flush`/`dirty checking` funcionam.
- **L2** é a diferença entre martelar o banco a cada request por uma tabela de `Country` que muda uma vez por ano, ou servir isso da memória. Mal usado, vira **stale read** — usuário vê dado velho.
- **Spring Cache** resolve o caso em que o gargalo não é uma entidade, mas o resultado de um cálculo ou de uma chamada de serviço caro. É a ferramenta certa quando você quer cachear *na fronteira do Service*, não *no ORM*.

Saber **qual nível** atacar é o que separa "liguei cache e ficou pior" de uma decisão de arquitetura defensável.

## Como funciona

### 1º nível (persistence context — por transação)

O cache de primeiro nível **é** o persistence context (detalhado na [[03-Dominios/Tecnologia/Java/Persistência de dados/03 - O persistence context e os estados da entidade|nota 03]]). Recapitulando o essencial:

- Vive enquanto a `Session`/`EntityManager` viver — tipicamente o escopo de **uma transação**.
- É **sempre ativo** e **não pode ser desligado**.
- Garante **identidade**: dentro da mesma sessão, `find(Order.class, 1L)` chamado duas vezes retorna **a mesma instância** em memória, sem segundo `SELECT`.
- É o que viabiliza o *dirty checking*: o contexto guarda o estado das entidades gerenciadas e detecta mudanças no `flush`.

Importante: L1 **não** é compartilhado entre transações. Fechou a sessão, esvaziou o cache. Por isso ele não resolve o problema de "duas requests diferentes lendo a mesma tabela de referência" — esse é trabalho do L2.

### 2º nível (application-wide — `@Cacheable`/`@Cache`)

O cache de segundo nível vive no `EntityManagerFactory`/`SessionFactory` e é **compartilhado por toda a aplicação**, atravessando transações. É **opt-in** em três frentes:

1. Habilitar via propriedades de configuração:

```properties
hibernate.cache.use_second_level_cache=true
hibernate.cache.region.factory_class=org.hibernate.cache.jcache.JCacheRegionFactory
hibernate.cache.default_cache_concurrency_strategy=read-write
```

A `region.factory_class` aponta o provider (JCache/JSR-107, Ehcache, Infinispan).

2. Marcar a entidade como cacheável com a anotação **JPA-padrão** `@Cacheable` e, opcionalmente, a **Hibernate-específica** `@Cache`, que escolhe a *concurrency strategy*:

```java
@Entity
@Cacheable
@Cache(usage = CacheConcurrencyStrategy.READ_WRITE)
public class Country { /* ... */ }
```

3. Escolher a `CacheConcurrencyStrategy` correta:

| Estratégia | Quando usar | Garantia |
| --- | --- | --- |
| `READ_ONLY` | Dado **imutável** (nunca atualiza) | Mais rápida; escrita lança erro |
| `NONSTRICT_READ_WRITE` | Update raro, tolera janela de inconsistência | Locking mínimo; pode servir stale por instantes |
| `READ_WRITE` | Update concorrente com consistência forte | *Soft locks*, consistência sólida |
| `TRANSACTIONAL` | Ambiente JTA com cache transacional | Isolamento dentro da transação |

**Quando usar L2:** entidade de **referência** — lida muitíssimo, mudada raramente. Tabelas de `Country`, `Currency`, `Category`, status codes.

**Quando NÃO usar L2:** dado **dinâmico** (carrinho, saldo, estoque em tempo real) — vira stale na hora. E em ambiente **multi-nó sem cache distribuído**: cada instância tem seu L2 local, então uma escrita num nó não invalida o L2 dos outros — você precisa de um provider distribuído (Infinispan/Hazelcast) ou desliga.

### Spring Cache (`@Cacheable`/`@CacheEvict`/`@CachePut` na camada Service)

O Spring Cache é uma **abstração genérica de caching**, ligada com `@EnableCaching`, que opera **no nível de método**: cacheia o **valor de retorno**, indexado pelos **argumentos** do método. Ele não tem nenhum conhecimento de JPA — é a **camada acima da JPA**, vivendo tipicamente na camada **Service**.

- `@Cacheable("countries")` — na **primeira** chamada executa o método e guarda o retorno; nas seguintes com os mesmos argumentos, retorna do cache **sem executar o método**.
- `@CacheEvict("countries")` — remove entradas (uma chave, ou `allEntries = true` pra limpar a região inteira). É o **gatilho de invalidação**.
- `@CachePut("countries")` — **sempre** executa o método e atualiza o cache com o retorno (não usar junto de `@Cacheable` no mesmo método).

A chave default é derivada dos parâmetros via `SimpleKeyGenerator` (ou SpEL com `key="#id"`). Os providers plugáveis incluem **Caffeine** (in-process), **Redis** e **Hazelcast** (distribuídos), e qualquer **JCache** (JSR-107).

A diferença mental: L2 cacheia **entidades dentro do ORM**; Spring Cache cacheia **o que o seu método de Service retorna** (DTOs, listas, resultados de cálculo) — não necessariamente entidades.

### Os três níveis lado a lado

| Aspecto | 1º nível (L1) | 2º nível (L2) | Spring Cache |
| --- | --- | --- | --- |
| Camada | Persistence context | `EntityManagerFactory` | Service (proxy AOP) |
| Escopo | Por transação | Application-wide | Application-wide |
| Ativação | **Sempre ativo** | Opt-in | Opt-in (`@EnableCaching`) |
| O que cacheia | Entidades gerenciadas | Entidades / coleções | Retorno de método |
| Conhece JPA? | É a JPA | É a JPA | **Não** |
| Anotação | (nenhuma) | `@Cacheable` + `@Cache` | `@Cacheable`/`@CacheEvict` |
| Invalidação | Fecha a sessão | Provider + estratégia | `@CacheEvict` |
| Caso de uso | Identidade, dirty check | Dados de referência | Cálculos/DTOs caros |

## Na prática

Entidade de **referência** `Country` (muda raramente), elegível pra L2 com estratégia `READ_WRITE`:

```java
import jakarta.persistence.Cacheable;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import org.hibernate.annotations.Cache;
import org.hibernate.annotations.CacheConcurrencyStrategy;

@Entity
@Cacheable
@Cache(usage = CacheConcurrencyStrategy.READ_WRITE, region = "countries")
public class Country {

    @Id
    private String isoCode;   // "BR", "US", ...

    private String name;

    // getters/setters
}
```

Configuração do **2º nível** (Spring Boot + provider JCache):

```yaml
spring:
  jpa:
    properties:
      hibernate:
        cache:
          use_second_level_cache: true
          use_query_cache: true
          region:
            factory_class: org.hibernate.cache.jcache.JCacheRegionFactory
          default_cache_concurrency_strategy: read-write
```

E um **`CountryService`** usando o **Spring Cache** (camada acima da JPA) pra cachear o resultado da busca e invalidá-lo na escrita:

```java
import org.springframework.cache.annotation.Cacheable;
import org.springframework.cache.annotation.CacheEvict;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class CountryService {

    private final CountryRepository repository;

    public CountryService(CountryRepository repository) {
        this.repository = repository;
    }

    // 1ª chamada vai ao banco; demais vêm do cache "countries"
    @Cacheable("countries")
    @Transactional(readOnly = true)
    public Country findByCode(String isoCode) {
        return repository.findById(isoCode).orElseThrow();
    }

    // toda escrita LIMPA o cache — sem isto, o dado fica obsoleto pra sempre
    @CacheEvict(value = "countries", allEntries = true)
    @Transactional
    public Country save(Country country) {
        return repository.save(country);
    }
}
```

Note os **três níveis convivendo**: dentro de `findByCode`, o `EntityManager` usa L1; a entidade `Country` pode estar no L2 do Hibernate; e o retorno do método de Service é guardado pelo Spring Cache. Cada um numa camada.

## Armadilhas

### (1) Confundir L1 (por-transação) com L2 (application-wide)

O erro mais comum: esperar que o cache de primeiro nível "lembre" de uma entidade entre requests diferentes. Não lembra — **L1 morre com a transação**. Se duas requisições distintas precisam do mesmo dado em cache, isso é trabalho do **L2** (ou do Spring Cache). Inversamente, achar que ligar o L2 vai dar identidade `==` dentro da transação também é equívoco: identidade é L1. São camadas distintas com responsabilidades distintas.

### (2) L2 em dado volátil (stale reads)

Marcar uma entidade dinâmica — saldo, estoque, posição de pedido — como `@Cacheable` no segundo nível é receita de **dado obsoleto**. O usuário lê do L2 um valor que o banco já mudou (possivelmente por outro nó). L2 é pra **dados de referência** (`Country`, `Currency`): lidos muito, mudados quase nunca. Para dado volátil, ou não cacheia, ou usa TTL curtíssimo com cache distribuído — e mesmo assim com olhos abertos.

### (3) `@Cacheable` sem `@CacheEvict` correspondente

Colocar `@Cacheable` num `findByCode` e **esquecer** o `@CacheEvict` no `save`/`update` é o bug silencioso por excelência: o cache popula na primeira leitura e **nunca mais invalida**. Toda escrita posterior atualiza o banco, mas o Service continua servindo o valor velho — **dado obsoleto pra sempre**, até a aplicação reiniciar. Para todo método de escrita que afeta uma região cacheada, tem que haver um `@CacheEvict` (ou `@CachePut`) correspondente.

## Em entrevista

### Frase pronta (inglês)

> Java persistence involves three distinct caches, and it's critical not to conflate them. The first-level cache is the persistence context — it's transaction-scoped, always on, and gives entity identity within a session. The second-level cache is an opt-in, application-wide entity cache, configured per entity with a concurrency strategy; I reserve it for reference data that is read heavily and changed rarely, like country or currency tables. The Spring Cache abstraction sits above JPA at the service layer, caching method return values, and I always pair `@Cacheable` reads with `@CacheEvict` on writes so the cache never serves stale data.

### Vocabulário

| Português | Inglês |
| --- | --- |
| cache de primeiro nível | first-level cache |
| cache de segundo nível | second-level cache |
| região de cache | cache region |
| invalidação | eviction |
| dados de referência | reference data |
| dados obsoletos | stale data |
| estratégia de concorrência | concurrency strategy |
| cache distribuído | distributed cache |

## Veja também

- [[03-Dominios/Tecnologia/Java/Persistência de dados/03 - O persistence context e os estados da entidade|O persistence context e os estados da entidade]]
- [[03-Dominios/Tecnologia/Java/Persistência de dados/12 - Transações operacionais — @Transactional propagação, isolamento, rollback, readOnly|Transações operacionais]]
- [[03-Dominios/Engenharia/Arquitetura/System Design|System Design]]
- [[03-Dominios/Tecnologia/Java/Persistência de dados/index|Persistência de dados (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#second-level cache (2º nível)|second-level cache (2º nível)]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#@Cacheable / Spring Cache|@Cacheable / Spring Cache]]

## Referências

- Hibernate ORM User Guide — Caching (first/second-level cache, `@Cache`, `CacheConcurrencyStrategy`, region factory): https://docs.hibernate.org/orm/current/userguide/html_single/Hibernate_User_Guide.html
- Spring Framework Reference — Cache Abstraction: https://docs.spring.io/spring-framework/reference/integration/cache.html
- Spring Framework Reference — Declarative Annotation-based Caching (`@Cacheable`, `@CacheEvict`, `@CachePut`, `@EnableCaching`): https://docs.spring.io/spring-framework/reference/integration/cache/annotations.html
