---
title: "AOP e proxies no Spring"
created: 2026-06-08
updated: 2026-06-08
type: concept
progress: backlog
status: seedling
publish: true
fase: Adepto
tags:
  - java
  - spring
  - adepto
  - aop
  - proxy
aliases:
  - "Spring AOP"
  - "proxies"
---

# AOP e proxies no Spring

> [!abstract] TL;DR
> AOP (*Aspect-Oriented Programming*) modulariza *cross-cutting concerns* — logging, métricas, transação, segurança, cache — que cortam horizontalmente várias classes. No Spring, o mecanismo é **proxy em runtime**: o container embrulha o bean num objeto-proxy que intercepta as chamadas de método e injeta o *advice* (código do aspecto) antes, depois ou em volta da execução real. Há dois tipos de proxy: **JDK dynamic proxy** (quando o bean implementa interface) e **CGLIB** (subclasse gerada em runtime, quando não há interface). O Spring Boot força CGLIB por padrão. Você escreve um aspecto com `@Aspect` + `@Component`, declara um *pointcut* (expressão que casa os pontos de interseção) e anota o método com um *advice type* (`@Before`, `@After`, `@AfterReturning`, `@AfterThrowing`, `@Around`). AOP é o motor por baixo de `@Transactional`, `@Async`, `@Cacheable` e `@PreAuthorize`.

## O que é

**AOP** é um paradigma que complementa a orientação a objetos. A OO modulariza *concerns* verticalmente: cada classe encapsula uma responsabilidade de domínio (`OrderService`, `CustomerRepository`, `ProductCatalog`). Mas certas preocupações não se encaixam nessa decomposição — elas atravessam todas essas classes. Logar a entrada e saída de cada método, medir tempo de execução, abrir e commitar uma transação, checar permissão antes de executar: isso é o mesmo código repetido em dezenas de lugares. São os **cross-cutting concerns** (preocupações transversais).

A AOP extrai esse código repetido para um módulo separado — o **aspecto** (*aspect*) — e deixa o framework "tecer" (*weave*) esse código de volta nos pontos certos, sem que as classes de domínio saibam que estão sendo interceptadas. O `OrderService` continua puro, só com lógica de pedido; o aspecto de logging vive isolado e se aplica a ele por uma regra declarativa.

O vocabulário canônico da AOP:

- **Aspect** (aspecto): o módulo que encapsula uma preocupação transversal. No Spring, uma classe anotada com `@Aspect`.
- **Join point** (ponto de junção): um ponto na execução do programa onde um aspecto pode ser aplicado. **No Spring AOP, o join point é sempre a execução de um método** — é a única granularidade suportada pelo modelo de proxy.
- **Pointcut**: uma expressão que seleciona *quais* join points recebem o advice. É o filtro.
- **Advice**: o código que roda no join point casado. O "o quê" e o "quando".
- **Weaving** (tecelagem): o processo de aplicar os aspectos ao objeto-alvo, criando o proxy. No Spring AOP, isso acontece em **runtime**, na criação do bean.

## Por que importa

Sem AOP, um *concern* transversal apodrece o código de domínio. Imagine que toda operação de `OrderService` precisa medir o tempo de execução e logar exceções. A versão ingênua é colar um `try/finally` com `System.nanoTime()` em cada método — código de instrumentação misturado com regra de negócio, duplicado, fácil de esquecer num método novo, infernal de mudar (trocar de logger = editar cinquenta arquivos).

A AOP inverte isso: a instrumentação vira **um** aspecto, declarado uma vez, aplicado por uma expressão que casa "todos os métodos de `OrderService`". Adicionar um método novo já o cobre automaticamente. Trocar o logger mexe num único lugar.

Mas o motivo mais importante de entender AOP no Spring não é escrever aspectos próprios — é que **AOP é o mecanismo por baixo de quase toda a mágica declarativa do framework**:

- `@Transactional` → implementado com um advice do tipo **`@Around`**: um `TransactionInterceptor` envolve o método, abre/obtém a transação antes de `proceed()` e commita ou faz rollback depois.
- `@Async` → um aspecto desvia a execução para outra thread.
- `@Cacheable` → um aspecto checa o cache antes de chamar o método e guarda o retorno depois.
- `@PreAuthorize` / `@Secured` → um aspecto valida a autorização antes de deixar a chamada passar.

Quando você entende que tudo isso é "um proxy interceptando a chamada", os comportamentos estranhos desses recursos param de ser mágica e viram consequência lógica do modelo de proxy. (O comportamento transacional e o de segurança em si pertencem a outros galhos da trilha — galhos 10 e 12, planejados — aqui interessa só o *mecanismo* que os habilita.)

## Como funciona

### Cross-cutting concerns e como o proxy intercepta (diagrama)

O Spring não modifica o bytecode da sua classe nem usa um compilador especial. Ele cria, em runtime, um **objeto-proxy** que tem a mesma "cara" do bean original (mesma interface ou mesma classe-pai) e o coloca no lugar do bean real no contexto. Quem injeta `OrderService` recebe, na verdade, o proxy. O proxy guarda uma referência ao objeto-alvo (*target*) real e a uma cadeia de *advices*.

Quando um cliente chama um método no proxy, este intercepta a chamada, executa os advices na ordem certa e, em algum ponto, delega para o método real do alvo:

```text
 Cliente
    │  orderService.place(order)
    ▼
┌───────────────────────────────────────────┐
│  PROXY  (criado pelo Spring em runtime)    │
│                                            │
│   1. roda @Before  ─────────────┐          │
│   2. pjp.proceed() ─────────────┼──┐       │
│   3. roda @AfterReturning  ◄────┼──┼─┐     │
│      ou @AfterThrowing          │  │ │     │
│   4. roda @After (sempre)       │  │ │     │
└─────────────────────────────────┼──┼─┼─────┘
                                   │  │ │
                                   ▼  │ │
                          ┌─────────────────┐
                          │  TARGET (real)  │
                          │  OrderService   │
                          │  .place(order)  │ ──┘
                          └─────────────────┘
```

O ponto crucial: **a interceptação só acontece quando a chamada passa pelo proxy**. Como o proxy é um objeto distinto do alvo, uma chamada que o alvo faz a si mesmo (`this.outroMetodo()`) **não** atravessa o proxy — é uma invocação direta dentro do mesmo objeto. Esse é o limite fundamental do modelo, a *self-invocation*, detalhada na nota seguinte.

### JDK dynamic proxy vs CGLIB (interface vs subclasse; default no Boot)

O Spring tem duas estratégias para fabricar o proxy:

**JDK dynamic proxy** — usa o `java.lang.reflect.Proxy` embutido na JDK. Gera, em runtime, uma classe que **implementa as mesmas interfaces** do bean. É a estratégia escolhida quando o alvo implementa pelo menos uma interface (no Spring Framework "puro"). Consequência: o proxy é do tipo *da interface*, não da classe concreta. Se você injetar pela classe concreta em vez da interface, pode levar um `ClassCastException` ou falha de injeção — com JDK proxy, programe contra a interface.

**CGLIB** — gera, em runtime, uma **subclasse** do bean, sobrescrevendo os métodos para inserir a interceptação. Não precisa de interface nenhuma. É a estratégia quando o alvo não implementa interface, ou quando você força proxying por classe. A biblioteca CGLIB vem repackaged dentro do `spring-core`.

| Aspecto | JDK dynamic proxy | CGLIB |
|---|---|---|
| Como proxia | implementa as interfaces | gera subclasse |
| Requisito | alvo tem ≥1 interface | nenhum |
| Proxy é do tipo | da interface | da classe (subclasse dela) |
| Limitações | só métodos da interface são interceptados | não proxia `final` (classe/método), nem `private` |

> [!warning] Default no Spring Boot
> O **Spring Framework** sozinho prefere **JDK dynamic proxy** quando há interface. Mas o **Spring Boot** inverte isso: desde a versão 2.x ele configura `proxyTargetClass = true` por padrão, ou seja, **usa CGLIB para todos os proxies, mesmo quando há interface**. A motivação foi evitar surpresas de injeção (poder injetar pela classe concreta) e tornar o comportamento uniforme. Logo, num projeto Boot 3.x típico, espere CGLIB — e lembre que CGLIB **não** proxia classes/métodos `final` nem métodos `private`.

Limitações do CGLIB que viram bug silencioso: um método `final` não pode ser sobrescrito, então o advice **não roda** nele (sem erro, só não intercepta). Idem para classe `final` (não pode ser estendida) e métodos `private`/`static`. Como o Boot usa CGLIB por padrão, evite `final` em beans que dependem de AOP (transação, cache etc.).

### Advice types (@Before/@After/@AfterReturning/@AfterThrowing/@Around)

O *advice type* declara **quando** o código do aspecto roda em relação ao método interceptado:

- **`@Before`** — roda **antes** do método. Não pode impedir a execução (a não ser lançando exceção) nem alterar o retorno. Recebe um `JoinPoint` para inspecionar assinatura e argumentos. Uso típico: validação, log de entrada.
- **`@AfterReturning`** — roda **depois** do método retornar **com sucesso**. Pode capturar o valor de retorno via `returning = "result"`. Não roda se o método lançou exceção. Uso: log do resultado, auditoria de sucesso.
- **`@AfterThrowing`** — roda **somente se** o método lançou exceção. Captura a exceção via `throwing = "ex"`. Não a engole (a exceção continua propagando). Uso: log de erro, alertas.
- **`@After`** — roda **sempre**, depois do método, com sucesso ou exceção (semântica de `finally`). Uso: liberar recurso, log de "método finalizado".
- **`@Around`** — o mais poderoso. **Envolve** a execução inteira. Recebe um `ProceedingJoinPoint` e decide *se* e *quando* chama `pjp.proceed()` (a execução real). Pode: medir tempo (antes/depois do `proceed`), alterar argumentos, alterar o retorno, suprimir/transformar exceções, ou nem chamar o método. É o único que pode fazer timing de ponta a ponta e o que `@Transactional` usa por baixo.

Ordem de execução numa chamada bem-sucedida: `@Around` (parte de antes) → `@Before` → método → `@Around` (parte de depois) → `@AfterReturning` → `@After`. Numa exceção, troque `@AfterReturning` por `@AfterThrowing`.

> [!info] Regra prática
> Use o advice mais fraco que resolve o problema. `@Around` dá controle total mas obriga você a chamar `proceed()` e a tratar `Throwable` manualmente — esquecer o `proceed()` faz o método nunca executar. Para puro log de entrada/saída, `@Before`/`@AfterReturning` são mais seguros; para timing ou modificação de fluxo, `@Around` é necessário.

### Pointcut expressions e @Aspect

A classe do aspecto é marcada com **`@Aspect`** (do AspectJ) **e** com `@Component` (para o Spring registrá-la como bean — sem isso, o aspecto não existe no contexto e é ignorado). O suporte a `@Aspect` precisa estar ligado por `@EnableAspectJAutoProxy` — no Boot 3.x isso já vem habilitado por autoconfiguração quando o AspectJ está no classpath (via `spring-boot-starter-aop`).

O **pointcut** é a expressão que casa os join points. As mais usadas:

- **`execution(...)`** — a mais comum. Casa pela assinatura do método. Sintaxe: `execution(modificadores? tipo-retorno pacote.classe.metodo(args) throws?)`. Exemplos:
  - `execution(* com.example.order.OrderService.*(..))` — qualquer método de `OrderService`, qualquer retorno (`*`), quaisquer argumentos (`..`).
  - `execution(public * com.example..*Service.*(..))` — todo método público de qualquer classe `*Service` em `com.example` e subpacotes.
- **`@annotation(...)`** — casa métodos que carregam uma anotação específica. `@annotation(com.example.Audited)` casa todo método anotado com `@Audited`. É exatamente assim que `@Transactional`/`@Cacheable` funcionam: um pointcut `@annotation` aponta para a anotação.
- **`within(...)`** — casa por tipo/pacote, mais grosso que `execution`. `within(com.example.order..*)` casa qualquer método de qualquer classe no pacote `order` e subpacotes.

Pointcuts podem ser combinados com `&&`, `||`, `!`, e nomeados num método `@Pointcut` reutilizável para não repetir a expressão.

## Na prática

Um aspecto único que faz logging e timing de toda chamada ao `OrderService`, usando `@Around`:

```java
package com.example.order.aop;

import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Pointcut;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;

@Aspect       // marca como aspecto AspectJ
@Component    // registra como bean — SEM isto, o aspecto é ignorado
public class OrderServiceTimingAspect {

    private static final Logger log =
            LoggerFactory.getLogger(OrderServiceTimingAspect.class);

    // Pointcut nomeado e reutilizável: todo método público de OrderService
    @Pointcut("execution(public * com.example.order.OrderService.*(..))")
    public void orderServiceMethods() { }

    @Around("orderServiceMethods()")
    public Object logAndTime(ProceedingJoinPoint pjp) throws Throwable {
        String method = pjp.getSignature().toShortString();
        long start = System.nanoTime();
        log.info("→ entrando em {} args={}", method, pjp.getArgs());
        try {
            Object result = pjp.proceed();           // executa o método real
            long ms = (System.nanoTime() - start) / 1_000_000;
            log.info("← {} concluído em {} ms", method, ms);
            return result;
        } catch (Throwable ex) {
            long ms = (System.nanoTime() - start) / 1_000_000;
            log.error("✗ {} falhou após {} ms: {}", method, ms, ex.toString());
            throw ex;                                 // re-propaga: não engole
        }
    }
}
```

Aqui, qualquer chamada a `OrderService.place(...)`, `OrderService.cancel(...)` etc. passa pelo proxy, dispara o `@Around`, mede o tempo e loga — e o `OrderService` permanece sem uma linha de logging. Adicionar `OrderService.refund(...)` amanhã já vem instrumentado, porque o pointcut casa por padrão de assinatura, não por método nomeado.

Versão alternativa dirigida por anotação, para aplicar timing só onde você quiser: crie `@Timed`, troque o pointcut por `@annotation(com.example.order.aop.Timed)`, e anote os métodos de interesse. É o mesmo modelo de `@Cacheable` e companhia.

## Armadilhas

> [!danger] 1. Esperar AOP em chamada interna (self-invocation)
> Se um método do `OrderService` chama outro método **do mesmo objeto** via `this.outroMetodo()`, a chamada **não passa pelo proxy** — vai direto ao alvo. O advice (e portanto `@Transactional`, `@Cacheable` etc. no método interno) **não roda**. Esse é o erro de AOP mais comum e mais traiçoeiro do Spring, porque não há erro nem aviso: simplesmente nada acontece. É o tema inteiro da próxima nota — [[03-Dominios/Tecnologia/Java/Spring Core e Boot/10 - Self-invocation e os limites do proxy|Self-invocation e os limites do proxy]].

> [!danger] 2. `@Aspect` sem `@Component`
> `@Aspect` só diz "esta classe é um aspecto AspectJ". Quem coloca a classe no contexto do Spring é o `@Component` (ou um `@Bean` numa `@Configuration`). Sem o registro como bean, o auto-proxy creator nunca vê o aspecto e ele é **silenciosamente ignorado** — nenhum advice roda e nenhum erro aparece. Sempre `@Aspect` **e** `@Component` juntos.

> [!danger] 3. Pointcut largo demais com overhead
> Um pointcut como `execution(* com.example..*.*(..))` casa **todo método de todo bean** da aplicação. Cada chamada passa a atravessar a cadeia de advice, o que adiciona overhead de interceptação a getters/setters triviais e a hot paths. Mantenha pointcuts cirúrgicos (por pacote de serviço, por anotação) em vez de varrer a aplicação inteira. Pointcuts amplos também tornam o comportamento imprevisível: fica difícil saber o que está sendo interceptado.

> [!warning] 4. CGLIB e `final` (consequência do default do Boot)
> Como o Boot usa CGLIB por padrão, métodos ou classes `final` **não** são proxiados — o advice não roda neles, sem erro. Evite `final` em beans que dependem de AOP.

## Em entrevista

### Frase pronta (inglês)

> Spring AOP modularizes cross-cutting concerns — like logging, transactions, or security — by wrapping each bean in a runtime proxy that intercepts method calls and runs advice around them. Under the hood, Spring uses a JDK dynamic proxy when the bean implements an interface, and CGLIB — a runtime-generated subclass — when it doesn't; Spring Boot actually defaults to CGLIB for everything via `proxyTargetClass`. The key consequence of the proxy model is that interception only happens when the call goes through the proxy, so a self-invocation through `this` bypasses the advice entirely — which is exactly why `@Transactional` or `@Cacheable` silently fail to apply on internal method calls.

### Vocabulário

| Termo PT | Termo EN |
|---|---|
| preocupação transversal | cross-cutting concern |
| aspecto | aspect |
| ponto de junção | join point |
| corte / filtro de pontos | pointcut |
| conselho / interceptação | advice |
| tecelagem | weaving |
| proxy em runtime | runtime proxy |
| proxy por subclasse | subclass-based / CGLIB proxy |
| autoinvocação | self-invocation |
| objeto-alvo | target object |

## Veja também

- [[03-Dominios/Tecnologia/Java/Spring Core e Boot/10 - Self-invocation e os limites do proxy|Self-invocation e os limites do proxy]] — por que a chamada interna via `this` fura o proxy, e como contornar.
- [[03-Dominios/Tecnologia/Java/Jakarta EE/13 - CDI avançado — interceptors, decorators e extensões|CDI avançado — interceptors, decorators e extensões]] — o AOP da plataforma Jakarta é **interceptor-based** (o container intercepta via metadata de interceptor binding); o Spring é **proxy-based** (embrulha o bean num objeto-proxy). Mesma meta — modularizar *concerns* transversais — mecanismo diferente.
- [[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/11 - Annotations|Annotations]] — a mecânica de annotations que sustenta `@Aspect`, `@Around` e os pointcuts `@annotation`.
- [[03-Dominios/Tecnologia/Java/Spring Core e Boot/index|Spring Core e Boot (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- Verbetes: [[03-Dominios/Tecnologia/Java/Dicionário de Java#Spring AOP|Spring AOP]] · [[03-Dominios/Tecnologia/Java/Dicionário de Java#advice (Spring AOP)|advice (Spring AOP)]] · [[03-Dominios/Tecnologia/Java/Dicionário de Java#pointcut|pointcut]]

## Referências

- Spring Framework Reference — *Aspect Oriented Programming with Spring*: https://docs.spring.io/spring-framework/reference/core/aop.html
- Spring Framework Reference — *Proxying Mechanisms*: https://docs.spring.io/spring-framework/reference/core/aop/proxying.html
