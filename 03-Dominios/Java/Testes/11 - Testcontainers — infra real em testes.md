---
title: "Testcontainers — infra real em testes"
created: 2026-06-11
updated: 2026-06-11
type: concept
progress: backlog
status: seedling
publish: true
fase: adepto
tags:
  - java
  - testes
  - adepto
  - testcontainers
aliases:
  - "Testcontainers"
  - "@ServiceConnection"
---

# Testcontainers — infra real em testes

> [!abstract] TL;DR
> **Testcontainers** sobe containers Docker **reais** (Postgres, Kafka, Redis) durante o teste e os derruba ao final, eliminando o falso-positivo do H2 in-memory — cujo dialeto SQL diverge do banco de produção (JSONB, funções, tipos). A partir do **Spring Boot 3.1**, `@ServiceConnection` auto-configura a conexão (datasource, broker, cache) a partir do container, sem `@DynamicPropertySource` manual. O **singleton pattern** (container `static` iniciado uma vez) e o **reuse** (`withReuse(true)`, só dev local) aceleram o ciclo de feedback. Você testa contra a coisa real, não contra um simulacro.

## O que é

Testcontainers é uma biblioteca que controla containers Docker a partir do código de teste. Em vez de mockar a infraestrutura ou trocá-la por um substituto leve (como o H2 no lugar do Postgres), você sobe a infraestrutura **de verdade**, efêmera, isolada e descartável — um Postgres 16, um Kafka, um Redis — pelo tempo que o teste durar.

O fluxo é simples: ao iniciar a suíte, Testcontainers fala com o daemon Docker, baixa a imagem (se necessário), sobe o container numa porta aleatória, espera ele ficar saudável (`waitingFor`), e expõe host/porta/credenciais ao teste. Ao final, derruba e limpa. Um container auxiliar (o **Ryuk**) garante a limpeza mesmo se a JVM morrer no meio.

A integração com JUnit 5 usa duas anotações: `@Testcontainers` na classe (liga a extensão) e `@Container` no campo do container (gerencia o ciclo de vida). Com Spring Boot 3.1+, `@ServiceConnection` fecha a ponte entre o container e a auto-configuração do Spring.

> [!info] Pré-requisito: um daemon Docker
> Testcontainers não emula nada em-processo: ele **delega ao Docker**. Para rodar, precisa de um daemon Docker (ou compatível — Podman, Colima, Testcontainers Cloud) acessível pela máquina. Sem isso, a biblioteca falha logo no startup. Esse pré-requisito tem consequências no CI (ver Armadilhas).

## Por que importa

O H2 in-memory mente. Ele é rápido e zero-config, mas fala um **dialeto SQL diferente** do banco de produção. Uma query com `JSONB`, `ON CONFLICT`, window functions específicas do Postgres, ou um tipo `array` passa no H2 (ou nem compila) e **quebra em produção** — ou pior: passa nos dois, mas com semântica sutilmente diferente. O teste fica verde e te dá uma falsa sensação de segurança. Esse é o **falso-positivo** clássico.

Testcontainers remove a variável "o banco de teste é outro". Você testa migrations Flyway/Liquibase contra o Postgres real, valida que aquele índice parcial existe, que a constraint dispara, que o `ON CONFLICT DO UPDATE` se comporta como esperado. O mesmo vale para Kafka (rebalance, partições, offsets reais) e Redis (TTL, eviction, comandos específicos).

Em entrevista, isso aparece como a diferença entre "test infidelity" e "test fidelity": quanto mais o ambiente de teste se parece com produção, mais os bugs aparecem cedo. Testcontainers é o padrão de mercado para integração com infra desde ~2020.

## Como funciona

### Por que Testcontainers > H2 (dialeto SQL/JSONB diverge → falso-positivo)

O H2 oferece um "modo de compatibilidade" (`MODE=PostgreSQL`), mas é uma aproximação, não emulação. Funções nativas, tipos (`JSONB`, `tsvector`, arrays), sintaxe de `UPSERT`, comportamento de transações e nível de isolamento divergem. Resultado:

- Query que usa `JSONB ->> 'campo'` não roda no H2 → você reescreve o teste ou pula a feature.
- `ON CONFLICT` do Postgres vira `MERGE` no H2 → semântica diferente.
- Migrations específicas do Postgres falham no H2 → você mantém um schema de teste paralelo, que **desincroniza** do real.

Com Testcontainers, o banco do teste **é** o banco de produção (mesma major version). Não há tradução, não há schema paralelo. O teste vê exatamente o que produção vê.

Uma regra prática: o H2 é defensável para um slice rápido de persistência onde você só exercita query methods triviais e quer feedback instantâneo. No momento em que o schema usa qualquer recurso específico do banco — tipos, migrations versionadas, índices, triggers — o H2 vira um risco, e Testcontainers passa a ser a escolha correta. A pergunta-guia é: "se este teste passa no H2, eu confio que passa em produção?". Quando a resposta é "não tenho certeza", troque por infra real.

### @Testcontainers + @Container + @ServiceConnection (Boot 3.1+)

Sem Spring, o trio JUnit funciona assim:

- `@Testcontainers` — registra a extensão JUnit 5 que gerencia o ciclo dos containers.
- `@Container` — marca o campo. Se for **de instância**, sobe/derruba por método; se for **`static`**, sobe uma vez por classe (singleton de classe).

A dor histórica era ligar esse container ao Spring: você precisava de `@DynamicPropertySource` para empurrar `host`, `porta` e credenciais para as properties do Spring na mão. A partir do **Spring Boot 3.1**, `@ServiceConnection` faz isso automaticamente: o Spring **detecta o tipo do container** (`PostgreSQLContainer` → `JdbcConnectionDetails`; `KafkaContainer` → `KafkaConnectionDetails`; `RedisContainer` → `DataRedisConnectionDetails`) e cria os beans de `ConnectionDetails`, sobrescrevendo as properties de conexão. Zero fiação manual.

> [!tip] @ServiceConnection vs @DynamicPropertySource
> Prefira `@ServiceConnection` para containers padrão. Caia em `@DynamicPropertySource` só quando precisar de controle fino (propriedade custom, `GenericContainer` com imagem exótica, ou múltiplos containers do mesmo tipo).

Por baixo dos panos, `@ServiceConnection` cria um bean de `ConnectionDetails` (`JdbcConnectionDetails`, `KafkaConnectionDetails`, etc.) que **sobrescreve** as properties de conexão antes da auto-configuração do datasource rodar. Um detalhe importante: um único `PostgreSQLContainer` pode gerar **mais de um** `ConnectionDetails` (JDBC e R2DBC), de modo que tanto o stack bloqueante quanto o reativo se conectam ao mesmo container sem configuração extra. Você restringe isso com o atributo `type` da anotação, se quiser só uma das pontes.

### Singleton pattern e reuse (acelerar o ciclo local)

Subir e derrubar um Postgres a cada classe de teste custa segundos que se acumulam. Dois mecanismos cortam esse custo:

**Singleton pattern** — declare o container `static` numa classe-base (ou holder) e **não chame `stop()`**. O container sobe na primeira vez que a classe é carregada e vive pelo resto da JVM; o Ryuk limpa no fim do processo. Todas as classes de teste que estendem a base compartilham o mesmo container.

**Reuse** (`withReuse(true)`) — vai além do singleton: o container **sobrevive entre execuções** da suíte. Você roda os testes, o container fica de pé, roda de novo e ele é reaproveitado (sem subir do zero). Exige opt-in explícito no `~/.testcontainers.properties` com `testcontainers.reuse.enable=true`. É um recurso **exclusivo de dev local** — nunca no CI (ver Armadilhas).

A diferença mental entre os dois: o singleton resolve o desperdício **dentro** de uma execução (uma classe-base, um container para todas as classes); o reuse resolve o desperdício **entre** execuções (você fica rodando a mesma suíte enquanto desenvolve, e não paga o startup toda vez). Em projetos grandes, o singleton já costuma bastar — ative reuse só se o startup ainda incomodar no seu loop de feedback.

### Módulos prontos (Postgres, Kafka, Redis, LocalStack)

Testcontainers traz módulos especializados que encapsulam a configuração de cada serviço: `PostgreSQLContainer`, `MySQLContainer`, `MongoDBContainer`, `KafkaContainer`, `RedisContainer` (e `GenericContainer` para qualquer imagem). Cada um expõe helpers do domínio — `getJdbcUrl()`, `getBootstrapServers()` — e tem dependência Maven/Gradle própria.

O **LocalStack** merece destaque: emula serviços AWS (S3, SQS, DynamoDB) num container, deixando você testar integração com a nuvem sem credenciais nem custo. Kafka aprofundado (rebalance, exactly-once, schemas) é assunto do **Galho 14**; aqui basta saber que o módulo existe e que `@ServiceConnection` o auto-configura.

Para imagens sem módulo dedicado, há o `GenericContainer`, que aceita qualquer imagem Docker e expõe `getHost()` / `getMappedPort(porta)`. Com ele, você precisa dizer ao Spring qual conexão o container representa — via `@ServiceConnection(name = "redis")` num `@Bean` de configuração de teste, ou via `@DynamicPropertySource` na mão. Os módulos prontos existem justamente para te poupar dessa fiação no caso comum.

## Na prática

Container Postgres `static` com `@ServiceConnection` — o caminho mais limpo no Spring Boot 3.1+:

```java
@SpringBootTest
@Testcontainers
class OrderRepositoryIntegrationTest {

    @Container
    @ServiceConnection
    static PostgreSQLContainer<?> postgres =
            new PostgreSQLContainer<>("postgres:16-alpine");

    @Autowired
    OrderRepository orderRepository;

    @Test
    void persistsAndReadsBackAgainstRealPostgres() {
        Order saved = orderRepository.save(new Order("CUST-42", 250.00));

        Optional<Order> found = orderRepository.findById(saved.getId());

        assertThat(found).isPresent();
        assertThat(found.get().getCustomerId()).isEqualTo("CUST-42");
    }
}
```

Não há `@DynamicPropertySource`: `@ServiceConnection` detecta o `PostgreSQLContainer` e configura o datasource sozinho. O `static` aplica o singleton de classe — um Postgres por classe de teste.

Singleton pattern numa classe-base compartilhada (container sobe **uma vez** para toda a suíte, sem `stop()`):

```java
@SpringBootTest
@Testcontainers
abstract class AbstractIntegrationTest {

    // static + sem stop() => sobe na primeira carga, vive pela JVM inteira.
    // O Ryuk limpa quando o processo morre.
    @Container
    @ServiceConnection
    static final PostgreSQLContainer<?> POSTGRES =
            new PostgreSQLContainer<>("postgres:16-alpine");
}

// Todas as classes abaixo reusam o MESMO container:
class OrderRepositoryTest extends AbstractIntegrationTest { /* ... */ }
class CustomerRepositoryTest extends AbstractIntegrationTest { /* ... */ }
```

Os repositories testados aqui (JpaRepository, query methods derivados) vêm do Galho 10 e da trilha de persistência — não os reexplico, ver [[03-Dominios/Java/Testes/10 - @DataJpaTest — testando repositories|@DataJpaTest]] e [[03-Dominios/Java/Persistência de dados/04 - Spring Data repositories — JpaRepository e query methods derivados|Spring Data repositories]]. A diferença é que o `@DataJpaTest` por padrão usa banco embarcado; com Testcontainers você o aponta para o Postgres real (`@AutoConfigureTestDatabase(replace = NONE)` + `@ServiceConnection`).

Para um serviço sem `JdbcDatabaseContainer` direto (Redis via `GenericContainer`), declare o container como `@Bean` numa `@TestConfiguration` e nomeie a conexão:

```java
@TestConfiguration(proxyBeanMethods = false)
class RedisTestConfig {

    @Bean
    @ServiceConnection(name = "redis")
    GenericContainer<?> redis() {
        return new GenericContainer<>(DockerImageName.parse("redis:7-alpine"))
                .withExposedPorts(6379);
    }
}
```

O `name = "redis"` diz ao Spring qual fábrica de `ConnectionDetails` aplicar a esse `GenericContainer` genérico — sem isso, o Spring não sabe que a imagem é um Redis. Para módulos prontos (`PostgreSQLContainer`, `KafkaContainer`), o tipo já carrega essa informação e o `name` é dispensável.

Ativando o reuse — **só na sua máquina**, no `~/.testcontainers.properties`:

```properties
testcontainers.reuse.enable=true
```

Com isso ligado e `withReuse(true)` no container, o Postgres sobrevive entre execuções da suíte, cortando o tempo de startup repetido. Note que reuse e singleton são ortogonais: você pode ter um, o outro, ou ambos.

## Armadilhas

### (1) Container por método de teste (sobe/derruba a cada teste — lento)

Declarar o container como campo **de instância** (sem `static`) faz a extensão subir e derrubar um Postgres novo a **cada método** `@Test`. Numa classe com 15 testes, são 15 startups de banco.

```java
@Testcontainers
class SlowTest {
    @Container // de instância: NOVO container por método -> lentíssimo
    PostgreSQLContainer<?> pg = new PostgreSQLContainer<>("postgres:16");
}
```

**Fix:** torne o container `static` (singleton de classe) ou suba-o numa classe-base compartilhada (singleton de suíte). Um container, muitos testes.

### (2) Esquecer que o CI precisa de Docker disponível

Testcontainers depende de um daemon Docker acessível. Se o runner do CI não tem Docker (ou o socket não está montado), **todos** os testes de integração quebram com `Could not find a valid Docker environment`, mesmo passando localmente.

```yaml
# Pipeline sem Docker disponível:
test:
  script: ./mvnw verify   # estoura: nenhum Docker daemon
```

**Fix:** garanta Docker no runner — `services: docker:dind` (GitLab), runner com Docker (GitHub Actions já traz), ou Testcontainers Cloud. Documente o pré-requisito no README do projeto.

### (3) `withReuse(true)` no CI (reuse é só pra dev local)

O reuse mantém containers vivos **entre execuções** propositalmente. No CI — ambiente efêmero, paralelo e descartável — isso gera **containers órfãos** que não são limpos, vazam recursos e podem causar testes não-determinísticos (estado vazando de um job para outro).

```java
// Em código que roda no CI:
static PostgreSQLContainer<?> pg =
        new PostgreSQLContainer<>("postgres:16").withReuse(true); // lixo no CI
```

**Fix:** mantenha o reuse condicionado ao ambiente. O `testcontainers.reuse.enable` fica só no `~/.testcontainers.properties` da máquina do dev; no CI, ele não existe e o flag vira no-op — mas o ideal é nem setar `withReuse(true)` quando `CI=true`. Deixe o CI sempre subir limpo.

> [!summary] Em uma linha
> Testcontainers troca o H2 mentiroso por infra real e efêmera; `@ServiceConnection` (Boot 3.1+) faz a fiação sozinho; singleton e reuse mantêm a suíte rápida — reuse só no seu laptop, nunca no CI.

## Em entrevista

### Frase pronta (inglês)

> We use Testcontainers for our integration tests instead of an in-memory H2 database. The problem with H2 is test infidelity: its SQL dialect diverges from Postgres, so queries using JSONB or `ON CONFLICT` either fail or behave differently, which gives false positives. Testcontainers spins up a real Postgres container for the test run, and since Spring Boot 3.1 the `@ServiceConnection` annotation auto-configures the datasource from the container, so there's no manual property wiring. To keep the suite fast, we declare the container as a static singleton and reuse it across test classes, and we enable container reuse only on local dev machines — never in CI, where containers must stay ephemeral.

### Vocabulário

| Termo (EN) | PT-BR | Uso |
| --- | --- | --- |
| test fidelity | fidelidade do teste | quão perto o teste está de produção |
| false positive | falso-positivo | teste verde que esconde bug real |
| in-memory database | banco em memória | H2/HSQLDB; rápido mas infiel |
| SQL dialect | dialeto SQL | sintaxe/semântica específica do banco |
| ephemeral container | container efêmero | sobe e some no fim do teste |
| singleton container | container singleton | `static`, um por suíte |
| service connection | conexão de serviço | bean que liga container ao Spring |
| container reuse | reaproveitamento de container | sobrevive entre execuções (dev only) |

## Veja também

- [[03-Dominios/Java/Testes/10 - @DataJpaTest — testando repositories|@DataJpaTest]]
- [[03-Dominios/Java/Testes/12 - Testes de integração ponta a ponta|Testes de integração ponta a ponta]]
- [[03-Dominios/Java/Persistência de dados/04 - Spring Data repositories — JpaRepository e query methods derivados|Spring Data repositories]]
- [[03-Dominios/Java/Testes/index|Testes (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Dicionário de Java]]

## Referências

- Testcontainers for Java — documentação oficial: https://java.testcontainers.org/
- Spring Boot Reference — Testcontainers e `@ServiceConnection`: https://docs.spring.io/spring-boot/reference/testing/testcontainers.html
