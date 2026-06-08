---
title: "Self-invocation e os limites do proxy"
created_at: 2026-06-08
updated_at: 2026-06-08
type: concept
progress: backlog
status: seedling
publish: true
fase: adepto
tags:
  - java
  - spring
  - adepto
  - aop
  - proxy
aliases:
  - "self-invocation"
---

# Self-invocation e os limites do proxy

> [!tip] TL;DR
> Toda a mágica de `@Transactional`, `@Async`, `@Cacheable` e afins depende de um proxy que intercepta a chamada antes de ela chegar ao objeto real. Quando um método chama outro método *do mesmo objeto* com `this.metodo()`, o proxy é ignorado completamente — a chamada vai direto para a instância, sem passar pelas instruções do aspecto. Além disso, métodos `private` e `final` nunca são interceptados pelo proxy CGLIB. A solução mais limpa é extrair o método para outro bean; self-injection e `AopContext.currentProxy()` existem, mas cada um traz um custo.

## O que é

**Self-invocation** (auto-invocação) é quando um método de um bean Spring chama outro método *do mesmo objeto* usando a referência `this` — explícita ou implícita:

```java
public void metodoA() {
    this.metodoB();   // self-invocation explícita
}

public void metodoA() {
    metodoB();        // self-invocation implícita (Java resolve como this.metodoB())
}
```

O problema é que esse padrão quebra silenciosamente qualquer anotação AOP (`@Transactional`, `@Async`, `@Cacheable`, `@Retryable`, etc.) presente em `metodoB`. Nenhuma exceção é lançada; o código compila e roda — só o comportamento esperado (transação, cache, execução assíncrona) não acontece.

## Por que importa

Comportamentos declarativos do Spring — iniciar uma transação, executar em thread separada, armazenar resultado em cache — são implementados como **adendos (advice)** que o proxy executa *antes* de delegar para o objeto real. Se o proxy nunca vê a chamada, o adendo nunca roda.

Esse é o tipo de bug mais traiçoeiro no ecossistema Spring: o código parece correto, os testes unitários passam (porque geralmente testam a classe sem proxy), mas em produção a transação simplesmente não abre, o cache não é consultado, ou o método roda na thread principal ao invés de uma pool assíncrona.

Compreender self-invocation é pré-requisito para usar com confiança qualquer anotação AOP do Spring.

## Como funciona

### Por que a chamada interna bypassa o proxy

O Spring não modifica o bytecode do seu bean. Em vez disso, ele cria um objeto separado — o **proxy** — que envolve o bean real. O contêiner injeta o proxy nos pontos de dependência, não o objeto diretamente.

Quando código externo chama `proxy.metodoA()`, o proxy intercepta, executa os adendos relevantes e só então delega para o objeto real. Mas quando `metodoA()` chama `this.metodoB()`, a referência `this` aponta para o *objeto real*, não para o proxy. O proxy nem sabe que `metodoB` foi chamado.

```
Código externo → proxy.metodoA()   ← proxy intercepta ✓
                     ↓
              objeto.metodoA()
                     ↓
              this.metodoB()        ← proxy ignorado ✗
                     ↓
              objeto.metodoB()      ← @Transactional não aplicada
```

A documentação oficial do Spring resume: *"once the call has finally reached the target object, any method calls that it may make on itself, such as `this.bar()` or `this.foo()`, are going to be invoked against the `this` reference, and not the proxy."*

### private/final: AOP silenciosamente ignorado (CGLIB não intercepta/sobrescreve)

O proxy CGLIB funciona gerando uma subclasse do bean em tempo de execução e sobrescrevendo (*override*) os métodos públicos para injetar os adendos. Por isso:

- **Métodos `private`** não podem ser sobrescritos por subclasses — o CGLIB simplesmente não os intercepta.
- **Métodos `final`** também não podem ser sobrescritos — o CGLIB os ignora da mesma forma.
- **Classes `final`** não podem ser estendidas — o CGLIB não consegue nem criar o proxy (falha em startup).

Colocar `@Transactional` em um método `private` ou `final` não causa erro de compilação nem de startup (em muitas configurações). A anotação é silenciosamente ignorada. O Spring não avisa — é responsabilidade do desenvolvedor saber dessa limitação.

> [!warning] Armadilha silenciosa
> `@Transactional private void processarPagamento()` compila e roda sem erro. A transação simplesmente nunca abre.

### Soluções

**1. Extrair para outro bean — a solução mais limpa**

Mover o método anotado para um bean separado elimina o problema pela raiz: a chamada agora sai de um objeto e chega em outro, passando obrigatoriamente pelo proxy.

```java
@Service
public class NotificacaoService {

    @Transactional
    public void enviarConfirmacao(Long pedidoId) {
        // lógica transacional aqui
    }
}

@Service
public class PedidoService {

    private final NotificacaoService notificacaoService;

    public PedidoService(NotificacaoService notificacaoService) {
        this.notificacaoService = notificacaoService;
    }

    public void criarPedido(Long pedidoId) {
        // ...
        notificacaoService.enviarConfirmacao(pedidoId); // passa pelo proxy ✓
    }
}
```

Vantagem: sem acoplamento ao Spring AOP; testável de forma independente; deixa as responsabilidades claras.

**2. Self-injection com `@Autowired` (ou `@Lazy`)**

O bean injeta uma referência a si mesmo pelo contêiner — que entrega o proxy, não `this`:

```java
@Service
public class PedidoService {

    @Autowired
    private PedidoService self; // Spring injeta o proxy

    public void criarPedido(Long pedidoId) {
        // ...
        self.enviarConfirmacao(pedidoId); // passa pelo proxy ✓
    }

    @Transactional
    public void enviarConfirmacao(Long pedidoId) {
        // lógica transacional aqui
    }
}
```

> [!caution] Cuidado com dependência circular
> Dependendo da versão do Spring Boot e da configuração, self-injection pode disparar aviso de dependência circular. Use `@Lazy` no campo se necessário: `@Autowired @Lazy private PedidoService self;`

**3. Anotar o método de entrada público (quando aplicável)**

Se a transação (ou outro comportamento) puder abranger o método de entrada inteiro, a solução mais simples é mover a anotação para o método chamado externamente:

```java
@Service
public class PedidoService {

    @Transactional // transação cobre criarPedido E a lógica interna
    public void criarPedido(Long pedidoId) {
        // ...
        enviarConfirmacao(pedidoId); // self-invocation, mas já está na mesma transação
    }

    private void enviarConfirmacao(Long pedidoId) {
        // lógica aqui — não precisa de @Transactional própria
    }
}
```

Limitação: funciona apenas quando a propagação padrão (`REQUIRED`) é suficiente. Se `enviarConfirmacao` precisasse de `REQUIRES_NEW` (nova transação independente), essa abordagem não serve.

## Na prática

O cenário mais comum em código Spring: `criarPedido` é chamado externamente (proxy intercepta, transação abre), mas internamente chama `this.enviarConfirmacao()` que também tem `@Transactional`. A anotação do método interno é ignorada.

```java
@Service
public class PedidoService {

    @Transactional
    public void criarPedido(Long pedidoId) {
        // persiste o pedido...
        this.enviarConfirmacao(pedidoId); // ← PROXY IGNORADO
    }

    @Transactional // ← NUNCA EXECUTADA quando chamada via this
    public void enviarConfirmacao(Long pedidoId) {
        // se criarPedido lançar exceção após este ponto,
        // qualquer lógica de rollback específica de enviarConfirmacao é ignorada
    }
}
```

**Fix 1 — extrair para outro bean:**

```java
@Service
public class ConfirmacaoService {

    @Transactional
    public void enviarConfirmacao(Long pedidoId) { ... }
}

@Service
public class PedidoService {

    private final ConfirmacaoService confirmacaoService;

    public PedidoService(ConfirmacaoService confirmacaoService) {
        this.confirmacaoService = confirmacaoService;
    }

    @Transactional
    public void criarPedido(Long pedidoId) {
        // ...
        confirmacaoService.enviarConfirmacao(pedidoId); // proxy ativo ✓
    }
}
```

**Fix 2 — self-injection:**

```java
@Service
public class PedidoService {

    @Autowired
    @Lazy
    private PedidoService self;

    @Transactional
    public void criarPedido(Long pedidoId) {
        // ...
        self.enviarConfirmacao(pedidoId); // proxy ativo ✓
    }

    @Transactional
    public void enviarConfirmacao(Long pedidoId) { ... }
}
```

**Fix 3 — anotação no método de entrada (propagação REQUIRED é suficiente):**

```java
@Service
public class PedidoService {

    @Transactional // cobre tudo abaixo
    public void criarPedido(Long pedidoId) {
        // ...
        enviarConfirmacao(pedidoId); // dentro da mesma transação — ok
    }

    private void enviarConfirmacao(Long pedidoId) { ... }
}
```

## Armadilhas

- **Refatorar "puxando lógica pra dentro" quebra `@Transactional`:** ao mover um método de uma classe auxiliar para dentro do próprio serviço (por parecer mais simples), a chamada deixa de passar pelo proxy. O comportamento muda silenciosamente em produção.

- **Método `@Async private`:** colocar `@Async` em um método `private` não gera erro, mas o método sempre roda na thread atual. O comportamento assíncrono nunca acontece.

- **Achar self-injection elegante:** self-injection resolve o problema técnico, mas sinaliza que a classe provavelmente acumula responsabilidades demais. Em revisão de código, é um indicador de que uma extração de bean seria mais adequada.

- **Assumir que AspectJ tem o mesmo limite:** AspectJ compile-time weaving e load-time weaving *não* têm esse problema — eles tecem o adendo diretamente no bytecode, sem proxy. O limite é específico do modelo de proxy do Spring AOP.

## Em entrevista

### Frase pronta (inglês)

- *"Spring AOP is proxy-based: when you call `this.method()` inside the same bean, you bypass the proxy entirely, so annotations like `@Transactional` or `@Async` on the called method are silently ignored."*

- *"The cleanest fix is to extract the annotated method into a separate bean — that way the call always goes through the proxy. Self-injection works too, but it's a code smell that usually means the class has too many responsibilities."*

- *"Private and final methods can't be intercepted by CGLIB because it generates a subclass at runtime and overrides methods — it simply can't override what's private or final."*

- *"Unlike AspectJ weaving, which modifies the bytecode directly, Spring AOP proxies only intercept calls that cross the bean boundary."*

### Vocabulário

| Termo PT | Termo EN |
|---|---|
| auto-invocação / chamada interna | self-invocation |
| adendo | advice |
| aspecto | aspect |
| proxy baseado em subclasse | CGLIB proxy |
| proxy baseado em interface | JDK dynamic proxy |
| tecelagem em tempo de compilação | compile-time weaving |
| limite do proxy | proxy boundary |
| injeção circular | circular dependency injection |
| extração de bean | bean extraction / extract-to-bean refactor |

## Veja também

- [[03-Dominios/Java/Spring Core e Boot/09 - AOP e proxies no Spring|AOP e proxies no Spring]] — o mecanismo de proxy em detalhe; self-invocation é sua consequência mais importante
- [[03-Dominios/Java/Jakarta EE/05 - CDI — escopos e contextos|CDI — escopos e contextos]] — o client proxy do CDI tem o mesmo limite de self-invocation: chamadas internas via `this` também ignoram o proxy contextual do CDI
- [[03-Dominios/Java/Spring Core e Boot/index|Spring Core e Boot (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Dicionário de Java#self-invocation|self-invocation]]

## Referências

- [Spring Framework Reference — Understanding AOP Proxies](https://docs.spring.io/spring-framework/reference/core/aop/proxying.html)
