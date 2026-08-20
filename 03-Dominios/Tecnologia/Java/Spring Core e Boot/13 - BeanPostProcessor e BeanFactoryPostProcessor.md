---
title: "BeanPostProcessor e BeanFactoryPostProcessor"
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
  - ioc
aliases:
  - "BeanPostProcessor"
  - "BeanFactoryPostProcessor"
---

# BeanPostProcessor e BeanFactoryPostProcessor

> [!abstract] TL;DR
> O Spring expõe dois pontos de extensão do container: `BeanFactoryPostProcessor` (BFPP) atua nas **definições** de bean antes de qualquer instância ser criada, e `BeanPostProcessor` (BPP) atua nas **instâncias** logo após serem criadas. É no BPP — especificamente em `postProcessAfterInitialization` — que o mecanismo de AOP do Spring envolve beans em proxies. Ambos respeitam `Ordered`/`PriorityOrdered` e são instanciados cedo, antes dos beans comuns.

## O que é

`BeanFactoryPostProcessor` e `BeanPostProcessor` são interfaces de extensão do IoC container do Spring, introduzidas no Spring Framework e mantidas sem alteração de contrato no Spring Boot 3.x.

**`BeanFactoryPostProcessor`** permite ler e modificar **metadados de configuração** (as `BeanDefinition`s) antes que qualquer bean de aplicação seja instanciado. O método central é:

```java
public interface BeanFactoryPostProcessor {
    void postProcessBeanFactory(ConfigurableListableBeanFactory beanFactory);
}
```

**`BeanPostProcessor`** permite interceptar e modificar **instâncias** de bean antes e depois dos callbacks de inicialização (`@PostConstruct`, `InitializingBean`):

```java
public interface BeanPostProcessor {
    Object postProcessBeforeInitialization(Object bean, String beanName);
    Object postProcessAfterInitialization(Object bean, String beanName);
}
```

## Por que importa

Esses dois contratos são a base sobre a qual toda a magia do Spring é construída. `PropertySourcesPlaceholderConfigurer` é um BFPP: ele resolve `${...}` nas definições de bean antes que qualquer datasource ou serviço seja criado. `AnnotationAwareAspectJAutoProxyCreator` é um BPP: ele inspeciona cada instância e a substitui por um proxy CGLIB ou JDK Proxy quando necessário para aplicar aspectos — sem isso, `@Transactional`, `@Cacheable` e `@Async` simplesmente não funcionam.

Entender a distinção permite diagnosticar falhas de ciclo de vida, implementar instrumentação personalizada e compreender por que certos beans "escapam" do proxy.

## Como funciona

### BeanFactoryPostProcessor: modificar bean definitions antes da instanciação

O BFPP recebe acesso direto ao `ConfigurableListableBeanFactory` — o registro interno de `BeanDefinition`s. Nesse ponto o container já leu todas as fontes de configuração (`@Configuration`, XML, `@ComponentScan`) mas ainda não criou nenhuma instância de bean de aplicação.

Um BFPP pode:
- Alterar propriedades de uma `BeanDefinition` (escopo, classe, valores de propriedades)
- Substituir placeholders por valores externos (papel do `PropertySourcesPlaceholderConfigurer`)
- Sobrescrever valores via arquivo externo (papel do `PropertyOverrideConfigurer`)

> [!warning] Não chame `getBean()` dentro de um BFPP
> Chamar `beanFactory.getBean("algumBean")` dentro de `postProcessBeanFactory` força a instanciação prematura daquele bean, antes que outros BFPPs tenham agido sobre sua definição. Isso viola o ciclo de vida e pode produzir beans sem processamento completo.

Para registrar um BFPP via `@Configuration`, o método **deve ser `static`**:

```java
@Configuration
public class AppConfig {
    @Bean
    public static PropertySourcesPlaceholderConfigurer placeholderConfigurer() {
        return new PropertySourcesPlaceholderConfigurer();
    }
}
```

Sem `static`, o Spring precisa instanciar a classe `@Configuration` para invocar o método, o que aciona proxies CGLIB prematuramente e dispara um aviso de falha de processamento de anotações (`@Autowired`, `@PostConstruct` etc.).

### BeanPostProcessor: envolver instâncias depois (onde nascem os proxies AOP)

O BPP opera **por instância**, recebendo o bean já construído e com dependências injetadas. Os dois hooks formam um "antes/depois" ao redor dos callbacks de inicialização:

```
instanciação → injeção de dependências
  → postProcessBeforeInitialization   ← aqui: @PostConstruct ainda não rodou
  → @PostConstruct / afterPropertiesSet
  → postProcessAfterInitialization    ← aqui: AOP cria o proxy e o substitui
```

O retorno de cada método **pode ser um objeto diferente** — é exatamente aí que o proxy AOP substitui o bean original no contexto. `AnnotationAwareAspectJAutoProxyCreator` verifica se o bean possui pointcuts correspondentes e, em caso positivo, retorna um proxy em `postProcessAfterInitialization`.

Da mesma forma que o BFPP, BPPs registrados via `@Bean` devem usar métodos `static` para evitar instanciação antecipada da classe de configuração.

### Ordem (Ordered/PriorityOrdered) e por que BPPs são instanciados cedo

Quando existem múltiplos BFPPs ou BPPs, a ordem de execução é controlada pelas interfaces `Ordered` e `PriorityOrdered`:

- **`PriorityOrdered`**: executado primeiro (fase anterior), mesmo em relação a outros `Ordered`
- **`Ordered`**: executado na segunda fase, em ordem crescente de `getOrder()`
- **Sem ordenação**: executado por último, em ordem de registro

```java
@Component
public class MeuBPP implements BeanPostProcessor, PriorityOrdered {
    @Override
    public int getOrder() { return Ordered.HIGHEST_PRECEDENCE; }

    @Override
    public Object postProcessBeforeInitialization(Object bean, String beanName) {
        return bean;
    }

    @Override
    public Object postProcessAfterInitialization(Object bean, String beanName) {
        return bean;
    }
}
```

BPPs registrados **programaticamente** (via `beanFactory.addBeanPostProcessor(...)`) não respeitam `Ordered` — a ordem de chamada é a ordem de registro.

**Por que BPPs são instanciados cedo:** o container precisa ter todos os BPPs prontos antes de criar o primeiro bean comum, para que nenhuma instância escape do processamento. Por isso, BPPs e seus beans de dependência direta são instanciados na fase de startup, antes dos beans de aplicação. Consequência: os próprios BPPs **não são elegíveis para auto-proxying** — aspectos AOP não são tecidos neles, e um aviso de log indica isso:

```
Bean 'meuBPP' of type [...] is not eligible for getting processed
by all BeanPostProcessors (for example: not eligible for auto-proxying).
```

## Na prática

BPP simples que loga a criação de cada bean e envolve `Service`s anotados com `@LogExecution` em um proxy dinâmico de logging:

```java
@Component
public class LoggingBeanPostProcessor implements BeanPostProcessor, Ordered {

    @Override
    public int getOrder() { return Ordered.LOWEST_PRECEDENCE - 1; }

    @Override
    public Object postProcessBeforeInitialization(Object bean, String beanName) {
        // Antes de @PostConstruct: apenas observa
        return bean;
    }

    @Override
    public Object postProcessAfterInitialization(Object bean, String beanName) {
        if (!bean.getClass().isAnnotationPresent(LogExecution.class)) {
            return bean; // Sem modificação
        }
        // Substitui o bean por um proxy JDK que loga chamadas
        return Proxy.newProxyInstance(
            bean.getClass().getClassLoader(),
            bean.getClass().getInterfaces(),
            (proxy, method, args) -> {
                System.out.printf("Chamando %s#%s%n",
                    beanName, method.getName());
                return method.invoke(bean, args);
            }
        );
    }
}
```

Registrado como `@Component`, este BPP aplica logging transparente sem modificar as classes de serviço — o mesmo padrão que o Spring usa internamente para `@Transactional`.

## Armadilhas

### 1. Injetar dependências complexas num BPP via `@Autowired` de campo

Um BPP é instanciado antes dos beans comuns. Se ele declarar `@Autowired` em um bean que depende de outros beans ainda não criados, o container pode falhar silenciosamente ou instanciar o bean de destino prematuramente — sem passar por outros BPPs.

```java
// PROBLEMÁTICO
@Component
public class MeuBPP implements BeanPostProcessor {
    @Autowired
    private ServicoComplexo servico; // ServicoComplexo depende de JPA, DataSource...
}
```

**Fix:** prefira dependências simples, use `ApplicationContext` via `ApplicationContextAware` ou injete via `ObjectProvider` para adiamento lazy:

```java
@Component
public class MeuBPP implements BeanPostProcessor {
    @Autowired
    private ObjectProvider<ServicoComplexo> servicoProvider;

    @Override
    public Object postProcessAfterInitialization(Object bean, String beanName) {
        ServicoComplexo servico = servicoProvider.getIfAvailable();
        // ... usa servico somente se disponível
        return bean;
    }
}
```

### 2. Quebrar a ordem do contexto ao registrar BPPs programaticamente

Adicionar um BPP via `beanFactory.addBeanPostProcessor(...)` dentro de outro BPP ou depois do refresh do contexto não garante que ele processará os beans já criados — eles já passaram pelo ciclo de vida.

```java
// PROBLEMA: beans criados antes deste ponto NÃO passarão pelo novoBPP
context.getBeanFactory().addBeanPostProcessor(novoBPP);
// Se o contexto já foi refreshed, a janela de processamento fechou
```

**Fix:** declare o BPP como `@Component` ou `@Bean static` para que o container o registre na fase correta, antes do primeiro bean de aplicação ser criado.

### 3. Confundir BFPP com BPP ao tentar modificar instâncias

Um equívoco comum é implementar `BeanFactoryPostProcessor` esperando receber instâncias configuradas. Dentro de `postProcessBeanFactory`, **não existem instâncias** — apenas `BeanDefinition`s. Tentar obter um bean via `getBean()` força instanciação prematura.

```java
// ERRADO: tenta modificar instância dentro de BFPP
public void postProcessBeanFactory(ConfigurableListableBeanFactory bf) {
    MeuBean bean = bf.getBean(MeuBean.class); // Instanciação prematura!
    bean.setConfig("valor");
}
```

**Fix:** use `BeanPostProcessor` para modificar instâncias; use `BeanFactoryPostProcessor` apenas para alterar `BeanDefinition`s (escopo, classe, propriedades de configuração).

```java
// CORRETO: modificar instância via BPP
public Object postProcessAfterInitialization(Object bean, String beanName) {
    if (bean instanceof MeuBean b) {
        b.setConfig("valor");
    }
    return bean;
}
```

## Em entrevista

### Frase pronta (inglês)

`BeanFactoryPostProcessor` and `BeanPostProcessor` are the two main extension points of the Spring IoC container. A `BeanFactoryPostProcessor` intercepts bean *definitions* before any instance is created — `PropertySourcesPlaceholderConfigurer` is the canonical example, resolving `${...}` placeholders at definition time. A `BeanPostProcessor`, on the other hand, intercepts bean *instances* after construction, wrapping them in proxies if needed; that is precisely how Spring AOP works — `AnnotationAwareAspectJAutoProxyCreator` is a BPP that replaces eligible beans with CGLIB or JDK proxies in `postProcessAfterInitialization`. Because BPPs must be ready before any regular bean is created, they are instantiated eagerly and therefore cannot themselves be auto-proxied.

### Vocabulário

| Termo PT | Termo EN |
|---|---|
| Definição de bean | Bean definition |
| Instância de bean | Bean instance |
| Pós-processador de bean | Bean post-processor |
| Pós-processador de fábrica | Bean factory post-processor |
| Instanciação antecipada | Premature instantiation / Eager instantiation |
| Proxy AOP | AOP proxy |
| Resolução de placeholder | Placeholder resolution |
| Ciclo de vida do container | Container lifecycle |
| Tecido de aspecto | Aspect weaving |
| Fábrica de beans configurável | Configurable listable bean factory |

## Veja também

- [[03-Dominios/Tecnologia/Java/Spring Core e Boot/09 - AOP e proxies no Spring|AOP e proxies no Spring]] — como o proxy CGLIB/JDK é criado pelo BPP de auto-proxy
- [[03-Dominios/Tecnologia/Java/Spring Core e Boot/15 - Auto-configuration e starters|Auto-configuration e starters]] — (planejado)
- [[03-Dominios/Tecnologia/Java/Jakarta EE/13 - CDI avançado — interceptors, decorators e extensões|CDI avançado — interceptors, decorators e extensões]] — as portable/build-compatible extensions do CDI são o ponto de extensão equivalente da spec; não reexplicado aqui
- [[03-Dominios/Tecnologia/Java/Spring Core e Boot/index|Spring Core e Boot (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- Verbetes: [[03-Dominios/Tecnologia/Java/Dicionário de Java#BeanPostProcessor|BeanPostProcessor]], [[03-Dominios/Tecnologia/Java/Dicionário de Java#BeanFactoryPostProcessor|BeanFactoryPostProcessor]]

## Referências

- [Spring Framework Reference — Container Extension Points](https://docs.spring.io/spring-framework/reference/core/beans/factory-extension.html)
- [Javadoc: BeanPostProcessor](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/beans/factory/config/BeanPostProcessor.html)
- [Javadoc: BeanFactoryPostProcessor](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/beans/factory/config/BeanFactoryPostProcessor.html)
- [Javadoc: PropertySourcesPlaceholderConfigurer](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/context/support/PropertySourcesPlaceholderConfigurer.html)
