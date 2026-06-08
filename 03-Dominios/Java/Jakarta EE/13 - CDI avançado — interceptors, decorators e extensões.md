---
title: "CDI avançado — interceptors, decorators e extensões"
created: 2026-06-07
updated: 2026-06-07
type: concept
progress: backlog
status: seedling
publish: true
fase: magus
tags:
  - java
  - jakarta-ee
  - magus
  - cdi
aliases:
  - "Interceptors CDI"
  - "Decorators CDI"
  - "CDI Lite"
---

# CDI avançado — interceptors, decorators e extensões

> [!abstract] TL;DR
> Interceptors são o AOP da plataforma — **é assim que `@Transactional` funciona por baixo** (veja [[11 - JTA — transações na plataforma]]): uma anotação customizada + uma classe interceptadora que envolve a invocação sem tocar no código de negócio. Decorators vão um passo além: conhecem o contrato que decoram e adicionam lógica de domínio a ele. Extensões conectam-se ao próprio container, seja em tempo de execução (portable extensions) ou em tempo de build (build compatible extensions — CDI Lite, Core Profile), habilitando a nova geração de runtimes de startup rápido.

## O que é

CDI oferece três mecanismos de meta-programação que operam em camadas diferentes:

- **Interceptors**: classes que envolvem invocações de métodos (ou construtores) de forma **opaca** — o interceptor não sabe nada sobre o contrato de negócio do alvo, apenas que uma chamada passou por ele. Usados para cross-cutting concerns: log, auditoria, métricas, transações.
- **Decorators**: classes que implementam a **mesma interface** do bean que decoram e recebem uma referência ao original via `@Delegate`. Conhecem o contrato e podem enriquecer a lógica de negócio.
- **Extensões**: mecanismos que permitem que código externo observe e modifique o próprio processo de bootstrap do container. Existem duas famílias: *portable extensions* (runtime, reflexão) e *build compatible extensions* (build-time, sem reflexão, CDI Lite).

Todas essas features existem em **CDI Full**. Interceptors e build compatible extensions também estão disponíveis em **CDI Lite** (Core Profile).

## Por que importa

Esses mecanismos desmistificam a "mágica" de frameworks inteiros. Quando você vê `@Transactional`, `@RolesAllowed` ou `@Retry` funcionando de forma declarativa, é um interceptor CDI (ou compatível) por baixo — um binding que associa uma anotação a uma classe que chama `proceed()` envolto em try/catch/finally. Dominar isso transforma o desenvolvedor de usuário de framework em autor de framework.

Em entrevista de nível sênior, a pergunta clássica é: *"Como você implementaria um `@Audited` que registra toda operação sensível?"* A resposta canônica passa por interceptor binding + `@AroundInvoke` + `InvocationContext`.

A distinção **CDI Lite vs CDI Full** explica por que a nova geração de runtimes (aqueles que fazem resolução em build-time para obter startup rápido e executáveis nativos — Galho 8, planejado) pode suportar CDI sem reflexão em runtime: build compatible extensions (introduzidas no CDI 4.0) permitem que extensões operem durante a compilação, antes do container subir.

## Como funciona

### Interceptor bindings: criando `@Audited`

Um interceptor binding é uma meta-anotação (`@InterceptorBinding`) que você coloca na sua própria anotação customizada. O trio é: **binding + interceptor + uso**.

**1. A anotação binding:**

```java
import jakarta.interceptor.InterceptorBinding;
import java.lang.annotation.ElementType;
import java.lang.annotation.Inherited;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

@InterceptorBinding
@Target({ElementType.TYPE, ElementType.METHOD})
@Retention(RetentionPolicy.RUNTIME)
@Inherited
public @interface Audited {}
```

**2. A classe interceptadora** (detalhada na seção seguinte).

**3. O uso no bean de negócio:**

```java
@Audited          // aplica o interceptor a todos os métodos da classe
@ApplicationScoped
public class OrderService {

    @Audited      // ou método a método
    public void placeOrder(Order order) { /* ... */ }
}
```

O container CDI conecta as pontas via proxy — quem chama `OrderService.placeOrder()` na verdade chama o proxy, que passa pelo interceptor antes de chegar ao método real.

### `@AroundInvoke` e `InvocationContext`

`@AroundInvoke` (pacote `jakarta.interceptor`) marca o método do interceptor que envolve a invocação de métodos de negócio. O parâmetro `InvocationContext` (mesmo pacote) expõe tudo sobre a chamada em curso:

| Método | O que retorna |
|---|---|
| `proceed()` | Avança para o próximo interceptor (ou o método alvo); retorna o valor de retorno |
| `getParameters()` | Array com os argumentos que serão passados ao método alvo |
| `setParameters(Object[])` | Substitui os argumentos antes de passar adiante |
| `getMethod()` | `java.lang.reflect.Method` do método interceptado |
| `getTarget()` | Instância do bean alvo |

`@AroundConstruct` funciona de forma análoga mas envolve o construtor do bean: nesse contexto, `getTarget()` retorna `null` antes de `proceed()` (o objeto ainda não existe).

```java
import jakarta.annotation.Priority;
import jakarta.interceptor.AroundInvoke;
import jakarta.interceptor.Interceptor;
import jakarta.interceptor.InvocationContext;
import java.util.logging.Logger;

@Audited
@Interceptor
@Priority(Interceptor.Priority.APPLICATION + 10)
public class AuditInterceptor {

    private static final Logger LOG = Logger.getLogger(AuditInterceptor.class.getName());

    @AroundInvoke
    public Object audit(InvocationContext ctx) throws Exception {
        String method = ctx.getMethod().getName();
        LOG.info("AUDIT → chamando " + method + " com " + ctx.getParameters().length + " arg(s)");
        try {
            Object result = ctx.proceed(); // avança na cadeia
            LOG.info("AUDIT → " + method + " concluído com sucesso");
            return result;
        } catch (Exception ex) {
            LOG.warning("AUDIT → " + method + " lançou " + ex.getClass().getSimpleName());
            throw ex;
        }
    }
}
```

### Ativação e ordem: `@Priority` vs `beans.xml`

Um interceptor **anotado com `@Interceptor` mas sem ativação simplesmente não roda** — essa é a armadilha mais comum. Há dois mecanismos de ativação:

**`@Priority`** (pacote `jakarta.annotation`) — ativa e ordena o interceptor globalmente (toda a aplicação):

```java
@Priority(Interceptor.Priority.APPLICATION + 10)
@Interceptor
@Audited
public class AuditInterceptor { /* ... */ }
```

`Interceptor.Priority` define constantes de faixa:
- `PLATFORM_BEFORE` (0) — interceptors de plataforma (início)
- `LIBRARY_BEFORE` (1000) — libs antes da lógica de aplicação
- `APPLICATION` (2000) — faixa recomendada para interceptors de aplicação
- `LIBRARY_AFTER` (3000) — libs após lógica de aplicação
- `PLATFORM_AFTER` (4000) — plataforma ao final

**`beans.xml`** — ativa e ordena interceptors por deployment (escopo do arquivo):

```xml
<beans xmlns="https://jakarta.ee/xml/ns/jakartaee"
       version="4.0">
    <interceptors>
        <class>com.example.AuditInterceptor</class>
        <class>com.example.SecurityInterceptor</class>
    </interceptors>
</beans>
```

A ordem declarada no `beans.xml` prevalece sobre `@Priority` para os interceptors listados nele. Quando ambos os mecanismos coexistem no mesmo deployment, os ativados via `@Priority` são ordenados entre si por valor numérico; os do `beans.xml` seguem a ordem de listagem.

### Decorators: `@Decorator` e `@Delegate`

Um decorator (pacote `jakarta.decorator`) implementa a mesma interface do bean que decora e recebe uma referência ao bean original via `@Delegate` (mesmo pacote). A diferença central em relação a interceptors:

- **Interceptor**: cego ao contrato de negócio — só sabe que houve uma chamada.
- **Decorator**: conhece o contrato — pode chamar métodos específicos do delegate, ler e transformar parâmetros de domínio, compor comportamento.

```java
import jakarta.decorator.Decorator;
import jakarta.decorator.Delegate;
import jakarta.enterprise.inject.Any;
import jakarta.inject.Inject;

@Decorator
public abstract class DiscountDecorator implements PriceCalculator {

    @Inject
    @Delegate
    @Any
    private PriceCalculator delegate;

    @Override
    public double calculate(Order order) {
        double base = delegate.calculate(order);           // chama o original
        return order.isVip() ? base * 0.9 : base;         // lógica de domínio
    }
}
```

O decorator é declarado `abstract` por convenção (métodos não decorados delegam automaticamente). O `@Any` no `@Delegate` é necessário para que o container o injete sem qualifiers adicionais.

**Quando usar cada um:**

| Situação | Mecanismo |
|---|---|
| Log, auditoria, métricas, retry, segurança | Interceptor |
| Lógica que depende de parâmetros de domínio (preço, desconto, validação de negócio) | Decorator |
| Precisa conhecer o tipo exato do contrato | Decorator |
| Deve aplicar a múltiplos contratos sem mudança | Interceptor |

Decorators também precisam ser ativados — preferencialmente via `@Priority` ou via `beans.xml` sob `<decorators>`.

### Portable extensions: panorama

Portable extensions (pacote `jakarta.enterprise.inject.spi`) são implementações da interface `Extension` que observam eventos do ciclo de vida do container em **tempo de execução**. Frameworks usam isso para registrar beans customizados, modificar metadados de tipos ou validar configurações na inicialização.

O evento mais usado é `ProcessAnnotatedType<T>`, que dispara para cada tipo descoberto pelo container — extensões podem vetar tipos, adicionar qualifiers ou substituir anotações inteiras. Outros eventos relevantes: `AfterBeanDiscovery` (para registrar beans sintetizados), `ProcessBean`, `ProcessInjectionPoint`.

Portable extensions dependem de reflexão e de acesso ao classloader em runtime, o que as torna incompatíveis com ambientes que exigem resolução estática em build-time. Por isso o CDI 4.0 introduziu as build compatible extensions.

### CDI Full vs CDI Lite e build compatible extensions

**CDI Lite** é o subconjunto introduzido no **CDI 4.0** que cobre beans, injeção, escopos básicos (`@RequestScoped`, `@ApplicationScoped`, `@Dependent`), interceptors e eventos. É a especificação que integra o **Jakarta EE Core Profile** — o perfil mínimo da plataforma, voltado a runtimes compactos.

**CDI Full** adiciona sobre o Lite: decorators, escopos de sessão/conversação, specialization e portable extensions.

**Build compatible extensions** (também CDI 4.0, pacote `jakarta.enterprise.inject.build.compatible.spi`) implementam a interface `BuildCompatibleExtension` e operam em **cinco fases de build-time** (`@Discovery`, `@Enhancement`, `@Registration`, `@Synthesis`, `@Validation`). Por serem sem reflexão (usam o Language Model API), funcionam em ambientes de compilação nativa e runtimes que fazem resolução estática — conectando esta nota à [[14 - Jakarta EE hoje — a plataforma sob o Spring]].

| Característica | CDI Lite | CDI Full |
|---|---|---|
| Beans, DI, qualifiers, producers | Sim | Sim |
| Interceptors | Sim | Sim |
| Build compatible extensions | Sim | Sim |
| Decorators | Não | Sim |
| Escopos de sessão/conversação | Não | Sim |
| Portable extensions | Não | Sim |
| Core Profile | Sim | Não |

## Na prática

### Trio completo: `@Audited`

```java
// 1. Binding
import jakarta.interceptor.InterceptorBinding;
import java.lang.annotation.*;

@InterceptorBinding
@Target({ElementType.TYPE, ElementType.METHOD})
@Retention(RetentionPolicy.RUNTIME)
@Inherited
public @interface Audited {}

// 2. Interceptor
import jakarta.annotation.Priority;
import jakarta.interceptor.AroundInvoke;
import jakarta.interceptor.Interceptor;
import jakarta.interceptor.InvocationContext;
import java.util.logging.Logger;

@Audited
@Interceptor
@Priority(Interceptor.Priority.APPLICATION)
public class AuditInterceptor {

    private static final Logger LOG = Logger.getLogger(AuditInterceptor.class.getName());

    @AroundInvoke
    public Object log(InvocationContext ctx) throws Exception {
        LOG.info("→ " + ctx.getMethod().getName());
        Object result = ctx.proceed();
        LOG.info("← ok");
        return result;
    }
}

// 3. Uso no bean
import jakarta.enterprise.context.ApplicationScoped;

@ApplicationScoped
public class OrderService {

    @Audited
    public void placeOrder(Order order) {
        // lógica de negócio — sem nenhuma referência a log/auditoria
    }
}
```

### Decorator de `PriceCalculator`

```java
import jakarta.decorator.Decorator;
import jakarta.decorator.Delegate;
import jakarta.enterprise.inject.Any;
import jakarta.inject.Inject;

@Decorator
public abstract class TaxDecorator implements PriceCalculator {

    @Inject
    @Delegate
    @Any
    private PriceCalculator delegate;

    @Override
    public double calculate(Order order) {
        double price = delegate.calculate(order);
        return price * 1.12; // adiciona 12% de imposto
    }
}
```

> [!warning] Self-invocation não é interceptada
> Se `OrderService.placeOrder()` chamar internamente `this.anotherMethod()` — e `anotherMethod()` for anotada com `@Audited` — o interceptor **não vai rodar**. A chamada via `this` não passa pelo proxy CDI. O mesmo vale para decorators. Veja [[04 - CDI — beans e injeção]] e [[11 - JTA — transações na plataforma]] para o padrão de solução (injetar o próprio bean ou redesenhar o fluxo).

## Armadilhas

### (1) Interceptor que "não roda"

**Sintoma:** você anotou o bean com `@Audited`, implementou o interceptor com `@Interceptor` e `@AroundInvoke`, mas nada acontece.

**Causa:** interceptors CDI não são ativados automaticamente — precisam de `@Priority` ou de declaração no `beans.xml`.

**Exemplo do problema:**

```java
@Audited
@Interceptor
// FALTOU @Priority — interceptor existe mas está desativado
public class AuditInterceptor {
    @AroundInvoke
    public Object log(InvocationContext ctx) throws Exception {
        return ctx.proceed(); // nunca chamado
    }
}
```

**Fix:**

```java
@Audited
@Interceptor
@Priority(Interceptor.Priority.APPLICATION) // ativa e define ordem
public class AuditInterceptor { /* ... */ }
```

Ou, alternativamente, adicionar ao `beans.xml`:

```xml
<interceptors>
    <class>com.example.AuditInterceptor</class>
</interceptors>
```

### (2) Self-invocation não é interceptada

**Sintoma:** `@Audited` funciona quando chamado de fora, mas métodos internos do mesmo bean passam em branco.

**Causa:** o proxy CDI só envolve chamadas externas ao bean. Chamadas via `this.metodo()` dentro da mesma instância vão diretamente ao objeto, sem passar pelo proxy.

```java
@ApplicationScoped
public class ReportService {

    @Audited
    public void generateReport() {
        prepare();          // ← @Audited em prepare() NÃO será ativado
    }

    @Audited
    public void prepare() { /* ... */ }
}
```

**Fix:** injete o próprio bean (via CDI) para que a chamada passe pelo proxy, ou reorganize para que `prepare()` seja chamado externamente quando necessário.

### (3) Lógica de negócio em interceptor

**Sintoma:** o interceptor começa a carregar regras de negócio ("se for VIP, aplica desconto") misturadas com infraestrutura ("loga, faz retry").

**Causa:** interceptors são para cross-cutting concerns — eles são **cegos ao domínio** intencionalmente. Colocar lógica de negócio neles esconde regras onde ninguém espera, dificulta testes e cria acoplamento implícito.

**Fix:** mova a lógica de domínio para o próprio serviço ou, se precisar variar o comportamento conhecendo o contrato, use um **decorator**. Interceptor = infraestrutura; Decorator = extensão de negócio.

### (4) Decorator onde interceptor bastaria

**Sintoma:** você cria um decorator só para logar chamadas de `PriceCalculator`, acoplando-se ao contrato sem necessidade.

**Causa:** decorators exigem que você implemente (ou herde) a interface do bean decorado. Se a lógica não usa nenhum método ou tipo específico do domínio, esse acoplamento não tem justificativa.

**Fix:** use interceptor com binding customizado. Decorator é justificado apenas quando a lógica **precisa** do contrato de domínio — por exemplo, ler os campos de `Order` para calcular desconto ou imposto.

## Em entrevista

### Frase pronta (inglês)

CDI interceptors implement Aspect-Oriented Programming at the platform level — they allow cross-cutting concerns like auditing, security, and transaction management to be applied declaratively through custom binding annotations, without touching the business code. The interceptor wraps the invocation through `InvocationContext.proceed()`, and activation is controlled by `@Priority` or `beans.xml`, so forgetting activation is the most common pitfall. Decorators, on the other hand, know the business contract they decorate and are the right tool when the extra behavior must reason about domain types — a distinction that separates infrastructure concerns from business enrichment.

### Vocabulário

| Termo PT | Termo EN |
|---|---|
| Interceptor binding | Interceptor binding |
| Ligação de interceptor | Interceptor binding type |
| Invocação interceptada | Intercepted invocation |
| Cadeia de interceptors | Interceptor chain |
| Decorator de contrato | Business decorator |
| Delegate injetado | Injected delegate |
| Extensão portável | Portable extension |
| Extensão compatível com build | Build compatible extension |
| Invocação direta / self-invocation | Self-invocation |
| Perfil mínimo (Jakarta EE) | Core Profile |

## Veja também

- [[04 - CDI — beans e injeção]]
- [[05 - CDI — escopos e contextos]]
- [[06 - CDI — qualifiers, producers e eventos]]
- [[11 - JTA — transações na plataforma]]
- [[14 - Jakarta EE hoje — a plataforma sob o Spring]]
- [[03-Dominios/Java/Jakarta EE/index|Jakarta EE (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Dicionário de Java#interceptor (CDI)|interceptor (Dicionário)]]
- [[03-Dominios/Java/Dicionário de Java#decorator (CDI)|decorator (Dicionário)]]
- [[03-Dominios/Java/Dicionário de Java#portable extension (CDI)|portable extension (Dicionário)]]

## Referências

- Jakarta CDI 4.1 Specification: <https://jakarta.ee/specifications/cdi/4.1/> — acesso 2026-06-07
- Jakarta CDI 4.0 Specification (introdução de CDI Lite e build compatible extensions): <https://jakarta.ee/specifications/cdi/4.0/> — acesso 2026-06-07
- Jakarta Interceptors 2.2 API Docs (`jakarta.interceptor`): <https://jakarta.ee/specifications/interceptors/2.2/apidocs/jakarta.interceptor/jakarta/interceptor/package-summary.html> — acesso 2026-06-07
- Jakarta Annotations API (`jakarta.annotation.Priority`): <https://jakarta.ee/specifications/annotations/2.1/apidocs/jakarta.annotation/jakarta/annotation/Priority.html> — acesso 2026-06-07
- CDI 4.1 Javadoc (pacotes `jakarta.decorator`, `jakarta.enterprise.inject.build.compatible.spi`): <https://jakarta.ee/specifications/cdi/4.1/apidocs/> — acesso 2026-06-07
