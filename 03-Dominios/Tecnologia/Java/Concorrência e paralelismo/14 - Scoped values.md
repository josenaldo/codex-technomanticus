---
title: "Scoped values"
created: 2026-06-03
updated: 2026-06-03
type: concept
progress: backlog
status: seedling
publish: true
fase: Magus
tags:
  - java
  - concorrencia
  - magus
  - scoped-values
  - threadlocal
aliases:
  - "Scoped values"
  - "ScopedValue"
---

# Scoped values

> [!abstract] TL;DR
> **`ScopedValue`** (Java 25, API **final**) é a alternativa moderna ao `ThreadLocal`: imutável dentro do escopo, com lifetime delimitado pelo bloco `where().run()` e custo zero de herança em forks de structured concurrency. Em sistemas com milhões de virtual threads, substitui `ThreadLocal` sem o vazamento de memória causado por cópias por thread. A leitura fora do escopo lança exceção; a mutação é substituída por *rebinding* — abrir um novo escopo aninhado com o valor novo.

## O que é

`ScopedValue` é uma variável cujo valor é vinculado a um escopo dinâmico delimitado, imutável dentro desse escopo, e automaticamente desvinculado ao término do bloco. Sua motivação central é escalar o padrão de "dado que acompanha a execução" — como um request-id ou um usuário autenticado — para ambientes com milhões de [[12 - Virtual Threads e Project Loom|virtual threads]], onde o custo e os riscos de `ThreadLocal` se tornam proibitivos.

A API é `public final class ScopedValue<T>` em `java.lang`, disponível como API **estável e permanente desde o Java 25** (Since: 25, sem preview).

## Por que importa

Com a chegada das virtual threads (Java 21+), o padrão de propagar contexto por `ThreadLocal` ganhou dois problemas novos em escala:

- **Custo de memória:** cada virtual thread carrega sua própria tabela de `ThreadLocal`. Um sistema com 1 milhão de virtual threads simultâneas pode manter 1 milhão de cópias de cada `ThreadLocal` vivo — mesmo que a maioria nunca o acesse.
- **Herança cara:** o construtor de `Thread` copia a tabela de `InheritableThreadLocal` do pai. Ao criar threads filho em forks massivos, esse custo se multiplica.

`ScopedValue` elimina ambos: não existe cópia por thread, e a herança em forks de structured concurrency é feita pelo escopo, não pela thread.

## Como funciona

### Problemas do `ThreadLocal`

`ThreadLocal` tem três características que o tornam problemático em escala de virtual threads:

1. **Mutável**: qualquer código no ciclo de vida da thread pode chamar `set()` e alterar o valor, criando acoplamento implícito.
2. **Lifetime ilimitado**: o valor persiste enquanto a thread existir. Em pools de threads (platform threads reutilizadas), esquecer `remove()` vaza o valor para requests seguintes.
3. **Herança cara**: `InheritableThreadLocal` copia toda a tabela de contexto para cada thread filha criada — em forks com milhões de virtual threads, isso é proibitivo.

```java
// ThreadLocal — mutável, lifetime ilimitado, fácil de vazar
private static final ThreadLocal<String> REQUEST_ID = new ThreadLocal<>();

REQUEST_ID.set("abc-123");
try {
    processRequest();   // lê REQUEST_ID.get()
} finally {
    REQUEST_ID.remove(); // se esquecer → vaza para o próximo request na mesma thread
}
```

### `ScopedValue` e `where().run()`

`ScopedValue` não tem `set()`. O único modo de vincular um valor é criando um escopo delimitado com `ScopedValue.where(key, value).run(op)` (ou `.call(op)` para obter retorno). Fora do bloco, a variável volta ao estado anterior (desvinculada, ou o valor externo se havia rebinding).

```java
// Declaração — por convenção, constante estática final
private static final ScopedValue<String> REQUEST_ID = ScopedValue.newInstance();

// Vincula e executa — automaticamente limpo ao sair do bloco
ScopedValue.where(REQUEST_ID, "abc-123").run(() -> {
    processRequest();           // pode chamar REQUEST_ID.get() em qualquer profundidade
});
// Aqui REQUEST_ID está desvinculado novamente
```

Para obter retorno do escopo:

```java
String resultado = ScopedValue.where(REQUEST_ID, "abc-123")
    .call(() -> processAndReturn());
```

Leitura dentro do escopo:

```java
String id = REQUEST_ID.get();           // retorna o valor vinculado
boolean bound = REQUEST_ID.isBound();   // true se vinculado no escopo atual
String idOuDefault = REQUEST_ID.orElse("sem-id"); // fallback se desvinculado
```

### Rebinding

Para "alterar" um valor em escopo aninhado, usa-se rebinding: abrir um novo escopo com `where()` dentro do escopo externo. O valor interno prevalece apenas dentro do bloco aninhado; ao sair, o escopo externo retoma o valor anterior.

```java
ScopedValue.where(REQUEST_ID, "externo").run(() -> {
    System.out.println(REQUEST_ID.get()); // "externo"

    ScopedValue.where(REQUEST_ID, "interno").run(() -> {
        System.out.println(REQUEST_ID.get()); // "interno"
    });

    System.out.println(REQUEST_ID.get()); // "externo" — reverteu
});
```

Também é possível vincular múltiplos valores num único carrier encadeando `where()`:

```java
ScopedValue.where(REQUEST_ID, "abc-123")
           .where(TENANT_ID, "tenant-42")
           .run(() -> processRequest());
```

### Herança em forks de structured concurrency

Quando um escopo de `ScopedValue` está ativo e se abre um `StructuredTaskScope`, as threads filhas criadas com `fork()` **herdam automaticamente** todas as vinculações do escopo pai — sem custo de cópia de tabela.

```java
private static final ScopedValue<String> REQUEST_ID = ScopedValue.newInstance();

ScopedValue.where(REQUEST_ID, "abc-123").run(() -> {
    try (var scope = StructuredTaskScope.open()) {
        var t1 = scope.fork(() -> serviço1());   // herda REQUEST_ID = "abc-123"
        var t2 = scope.fork(() -> serviço2());   // herda REQUEST_ID = "abc-123"
        scope.join();
        return combinar(t1.get(), t2.get());
    }
});
```

## Na prática

**Caso de uso canônico:** propagar um `requestId` por toda a cadeia de chamadas de um request HTTP sem passar o valor por parâmetro.

```java
// Declaração — um único ponto de verdade por contexto
public final class RequestContext {
    public static final ScopedValue<String> REQUEST_ID = ScopedValue.newInstance();
    public static final ScopedValue<String> TENANT_ID  = ScopedValue.newInstance();

    private RequestContext() {}
}

// Filtro HTTP — estabelece o escopo para todo o request
public class RequestContextFilter implements Filter {

    @Override
    public void doFilter(ServletRequest req, ServletResponse res, FilterChain chain)
            throws IOException, ServletException {

        String requestId = UUID.randomUUID().toString();
        String tenantId  = extractTenantId(req);

        ScopedValue.where(RequestContext.REQUEST_ID, requestId)
                   .where(RequestContext.TENANT_ID,  tenantId)
                   .run(() -> chain.doFilter(req, res));
        // Ao sair do run(), os valores são automaticamente desvinculados
    }
}

// Qualquer serviço na cadeia lê diretamente, sem receber por parâmetro
public class AuditService {

    public void registrarAuditoria(String operacao) {
        String reqId    = RequestContext.REQUEST_ID.get();
        String tenantId = RequestContext.TENANT_ID.get();
        log.info("[{}][{}] {}", tenantId, reqId, operacao);
    }
}
```

**`ThreadLocal` vs `ScopedValue`**

| Aspecto | `ThreadLocal` | `ScopedValue` |
|---|---|---|
| Mutabilidade | Mutável (`set()` a qualquer momento) | Imutável dentro do escopo (rebinding cria novo escopo) |
| Lifetime | Dura enquanto a thread existir | Delimitado pelo bloco `where().run()` |
| Custo por thread | Cópia por thread (cara com milhões de VTs) | Sem cópia — escopo compartilhado por leitura |
| Herança em forks | `InheritableThreadLocal` copia toda tabela | Herança automática e gratuita via `StructuredTaskScope` |
| Risco de vazamento | Alto — fácil esquecer `remove()` | Nenhum — desvincula ao sair do bloco automaticamente |

> [!info] Status no Java 25
> `ScopedValue` foi preview em versões anteriores. No **Java 25**, passou a API **final e permanente** (`java.lang.ScopedValue`, `@since 25`). Não requer flags de preview. `StructuredTaskScope` (nota 13), por outro lado, ainda é preview no Java 25.

## Armadilhas

### (1) Tentar mutar um `ScopedValue` — ele é imutável

**O problema:** desenvolvedores acostumados com `ThreadLocal` tentam alterar o valor em mid-flight chamando algo equivalente a `set()`. `ScopedValue` não tem `set()` — qualquer tentativa de "mudar" o valor exige abrir um novo escopo aninhado.

```java
private static final ScopedValue<String> LOCALE = ScopedValue.newInstance();

ScopedValue.where(LOCALE, "pt-BR").run(() -> {
    // ERRO de compilação: ScopedValue não tem set()
    // LOCALE.set("en-US");  // ❌ não existe

    // FIX: rebinding — novo escopo aninhado
    ScopedValue.where(LOCALE, "en-US").run(() -> {
        System.out.println(LOCALE.get()); // "en-US"
    });
    System.out.println(LOCALE.get()); // "pt-BR" — reverteu
});
```

O rebinding não altera o escopo externo. Se o código precisar que a mudança seja "permanente" para o restante do fluxo, o escopo deve ser iniciado no nível correto.

---

### (2) Ler fora do escopo `run()` — lança `NoSuchElementException`

**O problema:** chamar `get()` quando o `ScopedValue` não está vinculado lança `NoSuchElementException`. Isso acontece se o código que lê o valor for chamado antes do `where().run()`, ou após o bloco ter encerrado.

```java
private static final ScopedValue<String> USER = ScopedValue.newInstance();

// FORA do escopo — lança NoSuchElementException
String nome = USER.get();  // ❌ NoSuchElementException: ScopedValue not bound

// FIX 1: checar antes de ler
if (USER.isBound()) {
    String n = USER.get();
}

// FIX 2: usar orElse para valor padrão
String n = USER.orElse("anônimo");

// FIX 3: garantir que toda chamada a get() esteja dentro do escopo run()
ScopedValue.where(USER, "joao").run(() -> {
    String n2 = USER.get(); // ✅ "joao"
});
```

---

### (3) Assumir herança automática sem `StructuredTaskScope`

**O problema:** `ScopedValue` **não** propaga automaticamente para threads criadas com `new Thread()`, `ExecutorService.submit()` ou `CompletableFuture.runAsync()`. A herança automática ocorre **somente** via `StructuredTaskScope.fork()`. Código legado que dispara threads manualmente não herdará o escopo.

```java
private static final ScopedValue<String> REQUEST_ID = ScopedValue.newInstance();

ScopedValue.where(REQUEST_ID, "abc-123").run(() -> {

    // ❌ Thread avulsa — NÃO herda o escopo
    new Thread(() -> {
        System.out.println(REQUEST_ID.isBound()); // false — não herdou!
    }).start();

    // ❌ ExecutorService — NÃO herda automaticamente
    executor.submit(() -> {
        System.out.println(REQUEST_ID.isBound()); // false
    });

    // ✅ StructuredTaskScope.fork() — herda o escopo corretamente
    try (var scope = StructuredTaskScope.open()) {
        scope.fork(() -> {
            System.out.println(REQUEST_ID.get()); // "abc-123" — herdou!
            return null;
        });
        scope.join();
    }
});
```

**Fix:** ao precisar propagar contexto para threads independentes, capture o valor antes e passe explicitamente, ou refatore para usar `StructuredTaskScope`.

## Em entrevista

### Frase pronta (inglês)

> "`ScopedValue`, finalized in Java 25, is the modern replacement for `ThreadLocal` in high-scale systems. Unlike `ThreadLocal`, a `ScopedValue` is immutable within its dynamic scope — you bind a value with `ScopedValue.where(key, value).run(op)`, and it is automatically unbound when the block exits, with no risk of leaking state across requests. The key motivation is Virtual Threads: with potentially millions of virtual threads active at once, the per-thread copy cost of `ThreadLocal` becomes prohibitive, whereas `ScopedValue` shares the bound value across the call stack without copying."
>
> "Mutation is replaced by rebinding: you open a nested scope with a new value, and the outer scope is transparently restored when the inner block finishes. This composability makes it safe to use in frameworks and libraries without fear of cross-cutting side effects."
>
> "Inheritance into child tasks works automatically when using `StructuredTaskScope.fork()`, but does not propagate to threads created with plain `new Thread()` or `ExecutorService.submit()`. That asymmetry is intentional — structured concurrency is the recommended model when you need both scoped context and safe task management."

### Vocabulário

| Termo PT | Termo EN |
|---|---|
| valor com escopo | scoped value |
| escopo dinâmico | dynamic scope |
| revinculação / rebinding | rebinding |
| desvinculado | unbound |
| lifetime delimitado | bounded lifetime |
| herança de escopo em forks | scope inheritance in forks |
| propagação de contexto | context propagation |
| vazamento de estado por thread | per-thread state leak |
| alternativa ao ThreadLocal | `ThreadLocal` replacement / alternative |
| cópia por thread | per-thread copy |

## Veja também

- [[12 - Virtual Threads e Project Loom]]
- [[13 - Structured concurrency]]
- [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|MOC do galho]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[Java Concurrency]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#Scoped value|scoped value]]

## Referências

- [ScopedValue — Oracle JavaSE 25 API](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/lang/ScopedValue.html) — especificação final, Since: 25
- [ScopedValue.Carrier — Oracle JavaSE 25 API](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/lang/ScopedValue.Carrier.html) — métodos `run()` e `call()`
- [JEP 506: Scoped Values](https://openjdk.org/jeps/506) — proposta de finalização no Java 25
