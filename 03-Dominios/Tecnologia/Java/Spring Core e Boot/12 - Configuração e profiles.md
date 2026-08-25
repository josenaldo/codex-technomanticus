---
title: "Configuração e profiles"
created: 2026-06-08
updated: 2026-08-25
type: concept
progress: backlog
status: seedling
publish: true
fase: adepto
tags:
  - java
  - spring
  - adepto
  - config
  - profiles
aliases:
  - "@ConfigurationProperties"
  - profiles
---

# Configuração e profiles

> [!abstract] TL;DR
> Spring Boot lê propriedades de múltiplas fontes numa hierarquia fixa — args de linha de comando vencem tudo. Profiles recortam configurações por ambiente (`application-{profile}.yml`). `@ConfigurationProperties` entrega binding tipado, validado e imutável (records), substituindo `@Value` espalhado em todo o código.

## O que é

Configuração externalizada (_externalized configuration_) é o mecanismo pelo qual o Spring Boot injeta valores de fora do artefato — arquivos `.yml`/`.properties`, variáveis de ambiente, argumentos de linha de comando — no comportamento da aplicação sem recompilação.

**Profiles** são rótulos que ativam ou desativam beans e fatias de configuração de acordo com o ambiente em execução (`dev`, `staging`, `prod`, etc.).

**`@ConfigurationProperties`** é a annotation que amarra um prefixo de propriedades a uma classe Java (ou record), entregando binding tipado, validação via Bean Validation e suporte a IDE.

## Por que importa

- **Portabilidade de ambiente**: o mesmo JAR roda em dev e prod com configuração diferente, sem alterar o código.
- **Segurança operacional**: segredos nunca precisam entrar no código-fonte — chegam via variável de ambiente ou cofre (Vault, AWS Secrets Manager).
- **Manutenibilidade**: propriedades agrupadas em um record anotado com `@ConfigurationProperties` são fáceis de testar, documentar e validar; `@Value` espalhado por dezenas de beans é o oposto disso.
- **Pergunta frequente em entrevista**: a hierarquia de precedência e a diferença entre `@ConfigurationProperties` e `@Value` aparecem constantemente em processos seletivos para posições sênior.

## Como funciona

### Hierarquia/precedência de fontes (args > env > application-{profile} > application > defaults)

Spring Boot avalia propriedades em ordem estrita; a fonte de **maior prioridade vence**. Simplificando para o dia a dia (da menor para a maior precedência):

1. **Defaults** definidos via `SpringApplication.setDefaultProperties()`
2. **`@PropertySource`** em classes `@Configuration` (não suporta YAML)
3. **`application.properties` / `application.yml`** no classpath
4. **`application-{profile}.properties` / `application-{profile}.yml`** no classpath
5. **`application.properties` / `application.yml`** externos (fora do JAR)
6. **`application-{profile}.properties` / `application-{profile}.yml`** externos
7. **Variáveis de ambiente do SO** (ex.: `SERVER_PORT=9000`)
8. **System properties Java** (`-Dserver.port=9000`)
9. **`SPRING_APPLICATION_JSON`** (JSON em variável de ambiente ou system property)
10. **Argumentos de linha de comando** (`--server.port=9000`) — **prioridade máxima em produção**

> [!note] Regra prática
> Arquivo de profile externo > arquivo default externo > arquivo de profile no classpath > arquivo default no classpath. Quanto "mais tarde" a fonte é lida, mais ela sobrescreve o que veio antes.

Dentro da categoria "config data" (itens 3–6), arquivos de profile específico sempre sobrepõem o arquivo genérico. Isso significa que `application-prod.yml` pode sobrescrever qualquer chave definida em `application.yml`.

### Profiles (application-{profile}.yml, @Profile, ativação via env/arg/código)

Um profile é ativado informando seu nome para `spring.profiles.active`. Múltiplos profiles podem estar ativos ao mesmo tempo.

**Ativação via `application.yml`** (padrão de dev local):

```yaml
spring:
  profiles:
    active: "dev"
```

**Ativação via variável de ambiente** (recomendado em produção):

```bash
SPRING_PROFILES_ACTIVE=prod java -jar order-service.jar
```

**Ativação via argumento de linha de comando**:

```bash
java -jar order-service.jar --spring.profiles.active=prod,metrics
```

**Ativação programática** (raramente necessária, útil em testes):

```java
SpringApplication app = new SpringApplication(OrderServiceApplication.class);
app.setAdditionalProfiles("dev", "h2");
app.run(args);
```

**Arquivo de configuração específico de profile**:

```yaml
# application-prod.yml
spring:
  datasource:
    url: jdbc:postgresql://db.internal:5432/orders
    username: svc_orders
    password: ${DB_PASSWORD}   # vem de variável de ambiente
```

**`@Profile` em beans** — o bean só é registrado no container quando o profile indicado está ativo:

```java
@Configuration
@Profile("dev")
public class DevDataSourceConfig {
    @Bean
    public DataSource dataSource() {
        return new EmbeddedDatabaseBuilder()
            .setType(EmbeddedDatabaseType.H2)
            .build();
    }
}
```

> [!warning] Atenção
> `spring.profiles.active` e `spring.profiles.default` **não podem** ser definidos dentro de arquivos de profile específicos (ex.: dentro do próprio `application-prod.yml`). Essa restrição evita loops de auto-ativação.

**Profile groups** permitem ativar vários profiles com um único rótulo lógico:

```yaml
spring:
  profiles:
    group:
      production:
        - "proddb"
        - "prodmq"
```

Ativando `production`, os profiles `proddb` e `prodmq` são ativados juntos.

### @ConfigurationProperties (binding tipado, record, @Validated, relaxed binding) vs @Value/SpEL

`@ConfigurationProperties` vincula um prefixo de propriedades a uma classe Java ou record, realizando binding automático de tipos (incluindo listas, mapas e objetos aninhados).

**Relaxed binding**: o Spring aceita diferentes convenções de nomenclatura para a mesma propriedade. Para um campo `maxRetries`:

| Formato no arquivo / env | Exemplo |
|---|---|
| kebab-case (recomendado) | `order.max-retries` |
| camelCase | `order.maxRetries` |
| underscore | `order.max_retries` |
| UPPER\_SNAKE\_CASE (variável de ambiente) | `ORDER_MAX_RETRIES` |

`@Value("${order.maxRetries}")` **não** aplica relaxed binding — precisa do nome exato. `@ConfigurationProperties` aceita todos os formatos acima.

**`@Validated`** aciona a especificação Bean Validation sobre os campos vinculados: se alguma constraint falhar, a aplicação não sobe. Veja [[03-Dominios/Tecnologia/Java/Jakarta EE/08 - Bean Validation|Bean Validation]] (Galho 7) para a spec completa — aqui basta saber que `@Validated` é a ponte entre Spring e essa especificação.

**`@Value` / SpEL** serve para casos pontuais: uma única propriedade, lógica de default inline, ou expressões SpEL complexas. Quando há múltiplas propriedades relacionadas, `@ConfigurationProperties` é sempre a escolha mais limpa.

## Na prática

Exemplo completo com record (Boot 3.x / Java 16+) e YAML:

```java
// src/main/java/com/example/order/config/OrderProperties.java
package com.example.order.config;

import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import java.time.Duration;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.validation.annotation.Validated;

@ConfigurationProperties("order")
@Validated
public record OrderProperties(
    @NotBlank String serviceUrl,
    @Min(1) @Max(10) int maxRetries,
    Duration retryDelay
) {}
```

```yaml
# src/main/resources/application.yml
order:
  service-url: "https://api.internal/orders"
  max-retries: 3
  retry-delay: "PT2S"   # ISO-8601: 2 segundos
```

```java
// src/main/java/com/example/order/OrderServiceApplication.java
@SpringBootApplication
@ConfigurationPropertiesScan   // registra todos os @ConfigurationProperties do pacote
public class OrderServiceApplication {
    public static void main(String[] args) {
        SpringApplication.run(OrderServiceApplication.class, args);
    }
}
```

```java
// Uso no serviço — injeção normal por construtor
@Service
public class OrderClient {
    private final OrderProperties props;
    private final RestClient restClient;

    public OrderClient(OrderProperties props, RestClient.Builder builder) {
        this.props = props;
        this.restClient = builder.baseUrl(props.serviceUrl()).build();
    }
}
```

Para override em produção via variável de ambiente:

```bash
ORDER_SERVICE_URL=https://api.prod/orders \
ORDER_MAX_RETRIES=5 \
java -jar order-service.jar
```

> [!tip] Assista: ConfigurationProperties explained
> **Canal:** Java Brains | **Duração:** ~12min | **Idioma:** EN
>
> Dois ganhos sobre o que esta nota já cobre. O primeiro é a **segurança de tipo demonstrada ao vivo**: ele troca o valor da porta por `foo` e a aplicação simplesmente **recusa subir**, com a mensagem apontando a propriedade culpada. Um erro de configuração deixa de ser incidente em produção e vira falha de inicialização — que é o momento mais barato possível para descobri-lo. O segundo é o endpoint `/actuator/configprops`, que lista toda propriedade configurável da aplicação **incluindo as centenas que o próprio Spring Boot expõe**, cada uma com o valor atualmente em vigor. É a forma de descobrir o que dá para configurar sem caçar na documentação.
> Trecho de destaque [5:06]: *"you essentially get type safety in your configuration... you catch that during application startup time and not some time when the application runs"*
>
> 🎬 [Assistir no YouTube](https://www.youtube.com/watch?v=z8kfFbfGGME)

## Armadilhas

**1. Segredo hardcoded em `application.yml`** Colocar senhas, tokens ou chaves de API diretamente no arquivo commitado no repositório expõe credenciais em todo o histórico git. Sempre use referência a variável de ambiente (`${DB_PASSWORD}`) ou integre com um cofre de segredos.

**2. `@Value` espalhado onde cabia binding tipado** Quando um serviço tem cinco ou mais `@Value("${order.*}")` em campos diferentes, a manutenção se torna caótica: não há validação centralizada, o IDE não autocompleta, e testes unitários precisam mockar cada propriedade manualmente. Agrupe em um `@ConfigurationProperties`.

**3. Relaxed binding mal-entendido: `max-retries` ↔ `maxRetries`** Desenvolvedores frequentemente esperam que `@Value("${order.maxRetries}")` leia `order.max-retries` do YAML por relaxed binding — mas `@Value` **não faz isso**. A forma canônica no arquivo deve bater exatamente com o nome na annotation. Relaxed binding é exclusivo de `@ConfigurationProperties`.

**4. `@Profile` na classe errada com `@EnableConfigurationProperties`** Quando se usa `@EnableConfigurationProperties(MyProps.class)`, colocar `@Profile("prod")` na classe `MyProps` não funciona; o profile deve estar na classe `@Configuration` que registra o bean.

**5. `@PropertySource` com YAML** A annotation `@PropertySource` **não suporta arquivos `.yml`**. Para carregar um YAML customizado, use `spring.config.import` ou o mecanismo padrão de `application-{profile}.yml`.

## Em entrevista

### Frase pronta (inglês)

- "Spring Boot resolves configuration through a strict precedence chain — command-line arguments override everything, then environment variables, then profile-specific files, and finally the base `application.yml`. This lets you ship one artifact and configure it differently per environment without recompiling."
- "I prefer `@ConfigurationProperties` over scattered `@Value` fields because it gives me a single, validated, type-safe object that's easy to test and document. I annotate it with `@Validated` to catch misconfigured deployments at startup, not at runtime."
- "Profiles in Spring Boot are just labels: `application-prod.yml` is loaded automatically when the `prod` profile is active, and `@Profile("prod")` gates beans to that context. In CI/CD, I activate profiles through the `SPRING_PROFILES_ACTIVE` environment variable so the configuration stays out of the artifact."

### Vocabulário

| Termo PT | Termo EN |
|---|---|
| Configuração externalizada | Externalized configuration |
| Fonte de propriedades | Property source |
| Hierarquia de precedência | Precedence hierarchy / property source order |
| Binding tipado | Type-safe binding |
| Vinculação relaxada | Relaxed binding |
| Perfil ativo | Active profile |
| Grupo de profiles | Profile group |
| Propriedade de ambiente | Environment variable |
| Argumento de linha de comando | Command-line argument |
| Validação na inicialização | Startup validation / fail-fast validation |

## Veja também

- [[03-Dominios/Tecnologia/Java/Spring Core e Boot/08 - Qualificação de beans — @Qualifier, @Primary, @Profile|Qualificação de beans]] — `@Profile` na perspectiva de qualificação de beans
- [[03-Dominios/Tecnologia/Java/Jakarta EE/08 - Bean Validation|Bean Validation]] — `@Validated` aciona a spec Bean Validation do Galho 7; esta nota não re-explica a spec, apenas a consome
- [[03-Dominios/Tecnologia/Java/Spring Core e Boot/index|Spring Core e Boot (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#@ConfigurationProperties|@ConfigurationProperties]] (verbete)
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#@Value|@Value]] (verbete)

## Referências

- [Spring Boot Reference — Externalized Configuration](https://docs.spring.io/spring-boot/reference/features/external-config.html)
- [Spring Boot Reference — Profiles](https://docs.spring.io/spring-boot/reference/features/profiles.html)
