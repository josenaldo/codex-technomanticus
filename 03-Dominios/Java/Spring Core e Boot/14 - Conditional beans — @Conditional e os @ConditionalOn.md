---
title: "Conditional beans — @Conditional e os @ConditionalOn"
created: 2026-06-08
updated: 2026-06-08
type: concept
progress: backlog
status: seedling
publish: true
fase: magus
tags:
  - java
  - spring
  - magus
  - auto-config
aliases:
  - "@Conditional"
  - "conditional beans"
---

# Conditional beans — @Conditional e os @ConditionalOn

> [!abstract] TL;DR
> `@Conditional` é o SPI do Spring que permite registrar um bean somente quando uma condição é satisfeita em tempo de startup. O Spring Boot amplia esse mecanismo com uma família de `@ConditionalOn*` prontas para uso: `@ConditionalOnClass`, `@ConditionalOnMissingBean`, `@ConditionalOnProperty`, entre outras. Toda auto-configuration é construída sobre essas condições — o princípio fundamental é que **auto-config nunca deve sobrepor uma decisão explícita do desenvolvedor**.

## O que é

**Conditional beans** são beans cujo registro no `ApplicationContext` depende da avaliação de uma ou mais condições em tempo de bootstrap. O mecanismo central é o par anotação/interface:

- `@Conditional(MinhaCondicao.class)` — anotação aplicada a um `@Bean`, `@Configuration` ou `@Component`.
- `Condition` — interface funcional com um único método `matches(ConditionContext, AnnotatedTypeMetadata)`, que retorna `true` (registra) ou `false` (pula).

O Spring Boot adiciona a classe-base `SpringBootCondition` (que formata mensagens de diagnóstico para `--debug`) e toda a família `@ConditionalOn*`, que encapsula condições de uso frequente sem exigir implementação manual.

## Por que importa

Auto-configuration é o coração do "mágico" do Spring Boot: ao colocar `spring-boot-starter-data-jpa` no classpath, um `DataSource` e um `EntityManagerFactory` aparecem prontos. Esses beans só aparecem porque:

1. `@ConditionalOnClass` detecta que o driver JDBC está no classpath.
2. `@ConditionalOnMissingBean` verifica que o desenvolvedor ainda não definiu o seu próprio `DataSource`.

Sem esse mecanismo, duas implementações de `CacheManager` ou dois `DataSource` entrariam em conflito na inicialização. Com ele, a auto-config **cede espaço** ao código explícito e **fornece defaults** apenas quando necessário.

Para entrevistas de nível sênior, dominar `@Conditional` sinaliza compreensão de como o Boot funciona por dentro — não apenas como usá-lo.

## Como funciona

### O SPI @Conditional + Condition

```java
// Condição manual: só registra se a propriedade "feature.cache" existir
public class CachePropertyCondition implements Condition {
    @Override
    public boolean matches(ConditionContext context, AnnotatedTypeMetadata metadata) {
        return context.getEnvironment()
                      .containsProperty("feature.cache");
    }
}

@Bean
@Conditional(CachePropertyCondition.class)
public CacheManager localCacheManager() {
    return new ConcurrentMapCacheManager();
}
```

`ConditionContext` expõe o `Environment`, o `BeanFactory`, o `ClassLoader` e o `ResourceLoader` — tudo que é necessário para inspecionar o estado do contexto naquele momento. A avaliação ocorre **antes** da instanciação do bean, durante a fase de definição (`BeanDefinition` registration).

### Os condicionais do Boot (@ConditionalOnClass/OnMissingClass/OnBean/OnMissingBean/OnProperty/OnWebApplication/OnExpression)

O Boot fornece condicionais de alto nível para os casos mais comuns:

| Anotação | Registra quando… |
|---|---|
| `@ConditionalOnClass` | a classe indicada está no classpath |
| `@ConditionalOnMissingClass` | a classe indicada **não** está no classpath |
| `@ConditionalOnBean` | já existe um bean do tipo/nome especificado no `BeanFactory` |
| `@ConditionalOnMissingBean` | **não** existe bean do tipo/nome especificado |
| `@ConditionalOnProperty` | a propriedade existe e tem o valor esperado |
| `@ConditionalOnWebApplication` | a aplicação é um contexto web (Servlet ou Reactive) |
| `@ConditionalOnNotWebApplication` | a aplicação **não** é um contexto web |
| `@ConditionalOnExpression` | a expressão SpEL avalia como `true` |
| `@ConditionalOnSingleCandidate` | existe exatamente um bean candidato do tipo |
| `@ConditionalOnJava` | a JVM está em uma versão específica |
| `@ConditionalOnResource` | um resource (arquivo, classpath entry) está presente |

> [!tip] @ConditionalOnClass usa ASM
> A verificação de presença de classe **não carrega a classe em runtime** — usa leitura de bytecode via ASM. Por isso é seguro referenciar classes opcionais pelo atributo `name` (String) em vez de `value` quando a classe pode não existir.

```java
@Configuration(proxyBeanMethods = false)
@ConditionalOnClass(name = "com.hazelcast.core.HazelcastInstance")
public class HazelcastAutoConfiguration {

    @Bean
    @ConditionalOnMissingBean
    public CacheManager hazelcastCacheManager(HazelcastInstance instance) {
        return new HazelcastCacheManager(instance);
    }
}
```

### Ordem de avaliação e por que @ConditionalOnMissingBean cede pro usuário

As condições são avaliadas no momento em que o Spring processa cada `BeanDefinition`. A sequência importa:

1. **Beans do desenvolvedor** são registrados primeiro — via `@ComponentScan` e classes `@Configuration` explícitas no `ApplicationContext`.
2. **Auto-configurations** são registradas depois, carregadas a partir do SPI `AutoConfiguration.imports` (Boot 3.x) ou `spring.factories` (Boot 2.x).

```
startup
  │
  ├─ Scan + @Configuration do desenvolvedor  →  DataSource definida pelo dev
  │
  └─ Auto-configurations (após)              →  @ConditionalOnMissingBean(DataSource.class)
                                                 → já existe? SKIP. Não existe? CRIA.
```

Quando uma auto-configuration usa `@ConditionalOnMissingBean`, no momento da avaliação o bean do desenvolvedor já está registrado. A condição retorna `false` e o bean padrão é descartado — **sem conflito, sem exceção**.

A ordem entre auto-configurations é controlada pelos atributos `before`/`after` de `@AutoConfiguration` ou as anotações `@AutoConfigureBefore`/`@AutoConfigureAfter`.

> [!warning] Ordem não é criação
> `@ConditionalOnBean` detecta **registro** de `BeanDefinition`, não instanciação. Usar `@ConditionalOnBean` em beans do desenvolvedor (não em auto-configs) pode gerar resultados imprevisíveis dependendo da ordem de scan.

## Na prática

Cenário: a aplicação pode usar dois `CacheManager` diferentes, escolhido por propriedade.

```java
@Configuration
public class CacheConfig {

    @Bean
    @ConditionalOnProperty(prefix = "app.cache", name = "provider", havingValue = "redis")
    public CacheManager redisCacheManager(RedisConnectionFactory factory) {
        return RedisCacheManager.builder(factory)
                                .cacheDefaults(RedisCacheConfiguration.defaultCacheConfig())
                                .build();
    }

    @Bean
    @ConditionalOnProperty(
        prefix = "app.cache",
        name = "provider",
        havingValue = "local",
        matchIfMissing = true   // padrão quando a propriedade não está definida
    )
    public CacheManager localCacheManager() {
        return new ConcurrentMapCacheManager("products", "sessions");
    }
}
```

`application.properties`:
```properties
# Redis ativo:
app.cache.provider=redis

# Local (ou omitir a propriedade — matchIfMissing=true garante o fallback):
app.cache.provider=local
```

O atributo `matchIfMissing = true` é crucial: sem ele, omitir a propriedade significa que **nenhum** `CacheManager` seria registrado.

## Armadilhas

### 1. @ConditionalOnMissingBean pelo tipo errado

Quando o tipo não é especificado explicitamente, o Boot infere pelo tipo de retorno do método `@Bean`. Se a assinatura retorna a implementação concreta em vez da interface, a condição pode não detectar um bean registrado com o tipo da interface.

```java
// PROBLEMA: retorna ConcurrentMapCacheManager, não CacheManager
@Bean
@ConditionalOnMissingBean   // checa ConcurrentMapCacheManager, não CacheManager
public ConcurrentMapCacheManager cacheManager() { ... }

// FIX: declarar o tipo alvo explicitamente
@Bean
@ConditionalOnMissingBean(CacheManager.class)
public CacheManager cacheManager() { ... }
```

### 2. Assumir ordem de avaliação entre beans do desenvolvedor

Dois beans em classes `@Configuration` diferentes, ambos com `@ConditionalOnMissingBean` de um terceiro tipo, podem se comportar de forma imprevisível — depende de qual `@Configuration` é processada primeiro.

```java
// ConfigA.java
@Bean
@ConditionalOnMissingBean(DataSource.class)
public DataSource dataSourceA() { ... }  // pode ou não registrar

// ConfigB.java — processada antes de ConfigA?
@Bean
@ConditionalOnMissingBean(DataSource.class)
public DataSource dataSourceB() { ... }  // quem ganha?
```

**Fix:** usar `@ConditionalOnMissingBean` apenas em auto-configurations, onde a ordem é garantida pelo SPI. Para código de aplicação, preferir `@Primary` ou `@Profile`.

### 3. Condicional dependente de outro condicional (@ConditionalOnBean em cadeia)

Encadear `@ConditionalOnBean` entre beans do desenvolvedor é frágil. Se o bean dependente ainda não foi registrado no momento da avaliação (porque está em outra `@Configuration` que ainda não foi processada), a condição retorna `false` mesmo que o bean venha a existir depois.

```java
// PROBLEMA: SecurityService pode não estar registrado ainda
@Bean
@ConditionalOnBean(SecurityService.class)
public AuditService auditService(SecurityService sec) { ... }

// FIX: use @DependsOn para garantir ordem de registro,
//      ou reestruture para auto-configuration explícita
@Bean
@DependsOn("securityService")
public AuditService auditService(SecurityService sec) { ... }
```

> [!note] `@DependsOn` controla **criação**, não **registro**. Para condicionais, o que importa é o registro da `BeanDefinition`. A solução mais robusta é mover para auto-configuration com `@AutoConfigureAfter`.

## Em entrevista

### Frase pronta (inglês)

- "Spring's `@Conditional` is the SPI that gates bean registration based on a `Condition` implementation evaluated at startup, before any bean is instantiated."
- "Spring Boot's `@ConditionalOnMissingBean` is the cornerstone of the 'back-off' pattern: auto-configuration provides a sensible default only when the developer hasn't explicitly defined one, because auto-configs are always loaded after the application's own beans."
- "The key to understanding conditional evaluation order is that auto-configurations are registered last via the `AutoConfiguration.imports` SPI, so by the time `@ConditionalOnMissingBean` runs, any user-defined bean of that type is already visible in the `BeanFactory`."
- "One subtle pitfall is that `@ConditionalOnMissingBean` infers the target type from the `@Bean` method's return type — if you return the concrete class instead of the interface, it may not detect a bean registered under the interface type."

### Vocabulário

| Termo PT | Termo EN |
|---|---|
| Condicional de bean | Conditional bean |
| Avaliação de condição | Condition evaluation |
| Auto-configuração | Auto-configuration |
| Ceder espaço / recuar | Back off |
| Definição de bean | Bean definition |
| Infraestrutura de classpath | Classpath condition |
| Expressão SpEL | SpEL expression |
| Ordem de registro | Registration order |

## Veja também

- [[03-Dominios/Java/Spring Core e Boot/05 - @Configuration e @Bean — definição explícita de beans|@Configuration e @Bean]]
- [[03-Dominios/Java/Spring Core e Boot/15 - Auto-configuration e starters|Auto-configuration e starters]]
- [[03-Dominios/Java/Spring Core e Boot/index|Spring Core e Boot (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Dicionário de Java#@Conditional / @ConditionalOnX|@Conditional / @ConditionalOnX]]

## Referências

- [Spring Boot Reference — Condition Annotations](https://docs.spring.io/spring-boot/reference/features/developing-auto-configuration.html#features.developing-auto-configuration.condition-annotations)
- [Javadoc: org.springframework.boot.autoconfigure.condition](https://docs.spring.io/spring-boot/docs/current/api/org/springframework/boot/autoconfigure/condition/package-summary.html)
- [Spring Framework Javadoc: @Conditional](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/context/annotation/Conditional.html)
