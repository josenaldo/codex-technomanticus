---
title: "Structured concurrency"
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
  - structured-concurrency
  - loom
aliases:
  - Structured concurrency
  - StructuredTaskScope
---

# Structured concurrency

> [!abstract] TL;DR
> **Structured concurrency** trata um grupo de subtarefas concorrentes como uma unidade estruturada: todas nascem dentro de um escopo, o escopo só fecha quando todas terminam, e erros propagam automaticamente para o thread pai. `StructuredTaskScope` é a API central — cria-se com `StructuredTaskScope.open(joiner)`, dispara-se subtarefas com `scope.fork(callable)` (cada uma retorna um `Subtask`), e aguarda-se com `scope.join()`. O **Joiner** define a política de encerramento: todas-devem-suceder ou primeira-que-vencer. **Status de versão:** preview contínuo desde o Java 21; ainda **preview** no Java 25 — exige `--enable-preview`; a API pode mudar antes de virar GA.

## O que é

**Structured concurrency** é um modelo de programação concorrente onde subtarefas têm tempo de vida (*lifetime*) vinculado ao escopo que as criou — da mesma forma que chamadas de função são estruturadas em uma pilha de chamadas. O thread que abre o escopo é o "dono"; ele não avança além do escopo até que todas as subtarefas terminem.

O contraste com o modelo tradicional é direto. Com `ExecutorService`, subtarefas são **não estruturadas** — não há relação formal pai/filho:

```java
// Modelo tradicional — tasks órfãs, cancelamento manual
ExecutorService exec = Executors.newVirtualThreadPerTaskExecutor();

Future<User>        userFuture   = exec.submit(() -> fetchUser(userId));
Future<List<Order>> ordersFuture = exec.submit(() -> fetchOrders(userId));

// Se fetchUser() lançar exceção, fetchOrders() continua rodando inutilmente.
// O chamador precisa cancelar manualmente, tratar InterruptedException,
// lembrar de chamar future.cancel(true) no bloco catch — propenso a leak.
try {
    User        user   = userFuture.get();
    List<Order> orders = ordersFuture.get();
    return new UserDetails(user, orders);
} catch (Exception e) {
    userFuture.cancel(true);    // fácil esquecer
    ordersFuture.cancel(true);  // fácil esquecer
    throw new RuntimeException(e);
}
```

Com structured concurrency, o escopo é a unidade de trabalho: ao sair do bloco `try-with-resources` (seja por sucesso ou exceção), **todas** as subtarefas pendentes são canceladas automaticamente antes do fechamento.

## Por que importa

| Problema no modelo não estruturado | Solução com structured concurrency |
|------------------------------------|-------------------------------------|
| Tasks órfãs continuam após falha do pai | Cancelamento automático das irmãs |
| Vazamento de threads (leak) | Lifetime atrelado ao escopo — sem leak |
| Cancelamento manual tedioso e frágil | `close()` cancela tudo ao sair do `try` |
| Stack traces sem contexto pai/filho | Relação hierárquica visível em profilers |
| Tratamento de erro disperso | Joiner centraliza a política de encerramento |

Além da correção, a legibilidade melhora: o código estruturado expressa intenção (*"busca user e orders em paralelo, falha rápido se qualquer um falhar"*) em vez de mecânica (*"cancel, join, propagate"*).

## Como funciona

### `StructuredTaskScope` e `fork`/`join`

`StructuredTaskScope<T, R>` é uma classe genérica com dois type parameters:

- `T` — tipo de resultado que cada subtarefa (`Subtask`) pode produzir.
- `R` — tipo de resultado que `scope.join()` retorna (determinado pelo Joiner).

A API do **JDK 25** usa exclusivamente a factory estática `open()`:

```java
// Sem joiner explícito → usa awaitAllSuccessfulOrThrow internamente
// R = Void (join() retorna null, usado quando só se quer aguardar)
StructuredTaskScope<Object, Void> scope = StructuredTaskScope.open();

// Com joiner explícito (forma recomendada para políticas específicas)
StructuredTaskScope<String, String> scope =
    StructuredTaskScope.open(Joiner.anySuccessfulResultOrThrow());
```

Cada subtarefa é disparada com `fork()`, que retorna um `Subtask<U>`:

```java
// fork() aceita Callable<? extends U> ou Runnable
Subtask<User>        userTask   = scope.fork(() -> fetchUser(userId));
Subtask<List<Order>> ordersTask = scope.fork(() -> fetchOrders(userId));
```

`fork()` dispara a subtarefa imediatamente (em uma virtual thread, tipicamente). A chamada é não-bloqueante.

`scope.join()` bloqueia o thread dono até que **todas** as subtarefas completem (ou o escopo seja cancelado pela política do Joiner). Retorna o resultado do tipo `R`:

```java
R result = scope.join();   // bloqueia; retorna tipo definido pelo Joiner
```

Após `join()`, o estado de cada subtarefa pode ser inspecionado:

```java
subtask.state()      // Subtask.State: UNAVAILABLE, SUCCESS, FAILED
subtask.get()        // resultado se SUCCESS; lança IllegalStateException se não
subtask.exception()  // Throwable se FAILED
```

---

### Policies/Joiners (todas-ou-falha vs primeira-que-vence)

O `Joiner` é a estratégia de encerramento do escopo. Os joiners fornecidos pela API em JDK 25:

| Joiner | Comportamento |
|--------|---------------|
| `Joiner.awaitAllSuccessfulOrThrow()` | Aguarda todas; lança `FailedException` se qualquer uma falhar. `join()` retorna `Void`. |
| `Joiner.allSuccessfulOrThrow()` | Como o anterior, mas `join()` retorna `Stream<T>` com todos os resultados. |
| `Joiner.anySuccessfulResultOrThrow()` | Cancela as demais ao primeiro sucesso; `join()` retorna `T` (o primeiro resultado bem-sucedido). Lança se todas falharem. |

```java
// Todas-devem-suceder — join() retorna Void, resultados via subtask.get()
try (var scope = StructuredTaskScope.open(Joiner.awaitAllSuccessfulOrThrow())) {
    var uTask = scope.fork(() -> fetchUser(userId));
    var oTask = scope.fork(() -> fetchOrders(userId));
    scope.join();
    return new UserDetails(uTask.get(), oTask.get());
}

// Primeira-que-vence — join() retorna o primeiro resultado T
try (var scope = StructuredTaskScope.open(Joiner.anySuccessfulResultOrThrow())) {
    scope.fork(() -> queryReplica1(query));
    scope.fork(() -> queryReplica2(query));
    String fastest = scope.join();   // retorna String (tipo R = T = String)
}
```

É possível implementar `Joiner<T, R>` customizado para políticas mais complexas (ex.: tolerar N falhas, coletar resultados parciais).

---

### Propagação de erro e cancelamento automático

Quando o Joiner decide encerrar o escopo (por falha ou sucesso), ele chama internamente `scope.cancel()`. Isso interrompe (*interrupt*) todas as subtarefas em execução. Ao sair do bloco `try-with-resources`, `scope.close()` aguarda as subtarefas interrompidas terminarem antes de liberar o escopo — sem leaks.

```
Thread dono
    └─ StructuredTaskScope.open(...)
            ├─ fork(task A)  →  Virtual Thread A
            ├─ fork(task B)  →  Virtual Thread B  ← falha aqui
            └─ join()
                   Joiner detecta falha de B
                   → cancela A (interrupt)
                   → join() lança FailedException
            close() espera A encerrar
    └─ FailedException propaga para o chamador
```

---

### Escopo como unidade de trabalho (vs ExecutorService solto)

`ExecutorService` é um *pool* — um recurso compartilhado e reutilizado. `StructuredTaskScope` é um **escopo de trabalho** — criado para uma operação específica e descartado ao final. A distinção importa:

| Dimensão | `ExecutorService` | `StructuredTaskScope` |
|----------|-------------------|-----------------------|
| Lifetime | longo (pool global) | curto (operação específica) |
| Relação pai/filho | nenhuma | explícita |
| Cancelamento | manual | automático via Joiner |
| Resultado | `Future<T>` | `Subtask<T>` + retorno de `join()` |
| Observabilidade | stack trace plano | hierarquia visível em JFR/profiler |

Os dois não são excludentes: `StructuredTaskScope` usa virtual threads internamente (Project Loom) e pode ser combinado com `ExecutorService` no nível do sistema — mas dentro de uma operação, o escopo estruturado é preferível.

## Na prática

> [!warning] Feature em preview — exige `--enable-preview`
> `StructuredTaskScope` é **preview** no Java 25 (since Java 21). Para compilar e executar, passe:
> ```
> javac --enable-preview --release 25 MinhaClasse.java
> java  --enable-preview MinhaClasse
> ```
> A API pode mudar entre versões de preview. Não use em código de produção sem avaliar o risco de migração.

### Exemplo: buscar user e orders em paralelo, falhar rápido

```java
import java.util.concurrent.StructuredTaskScope;
import java.util.concurrent.StructuredTaskScope.Joiner;

// Requer --enable-preview (Java 25 preview)
record UserDetails(User user, List<Order> orders) {}

UserDetails fetchUserDetails(long userId) throws InterruptedException {
    try (var scope = StructuredTaskScope.open(Joiner.awaitAllSuccessfulOrThrow())) {

        // fork() dispara cada subtarefa em uma virtual thread — não-bloqueante
        StructuredTaskScope.Subtask<User>        userTask   =
            scope.fork(() -> fetchUser(userId));
        StructuredTaskScope.Subtask<List<Order>> ordersTask =
            scope.fork(() -> fetchOrders(userId));

        // join() bloqueia até todas completarem.
        // Se qualquer uma falhar, awaitAllSuccessfulOrThrow lança FailedException,
        // scope.close() cancela a outra e o try-with-resources sai limpo.
        scope.join();

        // Seguro acessar .get() somente após join() com sucesso
        return new UserDetails(userTask.get(), ordersTask.get());

    } // close() garante que não há subtarefas vazando ao sair
}
```

### Exemplo: primeira réplica a responder vence

```java
// Requer --enable-preview (Java 25 preview)
String queryFastest(String sql) throws InterruptedException {
    try (var scope = StructuredTaskScope.open(Joiner.anySuccessfulResultOrThrow())) {
        scope.fork(() -> queryReplica("db-primary", sql));
        scope.fork(() -> queryReplica("db-replica-1", sql));
        scope.fork(() -> queryReplica("db-replica-2", sql));

        // join() retorna o resultado da primeira subtarefa bem-sucedida;
        // as demais são canceladas automaticamente pelo Joiner
        return scope.join();
    }
}
```

> [!info] Equivalência com a API dos previews anteriores (JDK 21–24)
> A API foi reformulada ao longo dos previews. Nos JDKs 21–24 usava-se subclasses concretas e métodos de instância distintos:
> ```java
> // Forma antiga (JDK 21–24) — ShutdownOnFailure
> try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
>     var userTask   = scope.fork(() -> fetchUser(userId));
>     var ordersTask = scope.fork(() -> fetchOrders(userId));
>     scope.join();           // aguarda
>     scope.throwIfFailed();  // propaga exceção manualmente
>     return new UserDetails(userTask.get(), ordersTask.get());
> }
>
> // Forma antiga — ShutdownOnSuccess
> try (var scope = new StructuredTaskScope.ShutdownOnSuccess<String>()) {
>     scope.fork(() -> queryReplica1(sql));
>     scope.fork(() -> queryReplica2(sql));
>     scope.join();
>     return scope.result();  // retorna o primeiro sucesso
> }
> ```
> No JDK 25, `ShutdownOnFailure` e `ShutdownOnSuccess` foram substituídos pelo modelo `open(Joiner)`. Se você migra de código 21–24, substitua as subclasses pelos joiners equivalentes.

## Armadilhas

### (1) Usar resultado de subtarefa antes de `join()`

**O problema:** `Subtask.get()` só é válido após `scope.join()` completar com sucesso. Chamá-lo antes lança `IllegalStateException` (estado `UNAVAILABLE`). É um erro fácil de cometer em refatorações.

```java
// ERRADO — get() antes de join()
try (var scope = StructuredTaskScope.open(Joiner.awaitAllSuccessfulOrThrow())) {
    var userTask = scope.fork(() -> fetchUser(userId));
    User user = userTask.get();   // IllegalStateException: state is UNAVAILABLE
    scope.join();
}

// CORRETO — get() somente após join()
try (var scope = StructuredTaskScope.open(Joiner.awaitAllSuccessfulOrThrow())) {
    var userTask   = scope.fork(() -> fetchUser(userId));
    var ordersTask = scope.fork(() -> fetchOrders(userId));
    scope.join();                           // aguarda
    User user         = userTask.get();     // seguro
    List<Order> orders = ordersTask.get();  // seguro
}
```

**Fix:** disciplina de layout — sempre coloque `scope.join()` logo após todos os `fork()`s, antes de qualquer `subtask.get()`.

---

### (2) Não checar interrupção em subtarefas com loops longos

**O problema:** quando o Joiner cancela o escopo, ele interrompe as virtual threads das subtarefas (`Thread.interrupt()`). Uma subtarefa com loop longo que ignora interrupção continua executando, bloqueando o `close()` e criando latência indesejada.

```java
// PROBLEMÁTICO — loop ignora InterruptedException (engole a flag)
scope.fork(() -> {
    for (int i = 0; i < 1_000_000; i++) {
        try {
            process(items.get(i));
        } catch (InterruptedException e) {
            // ❌ engole a interrupção — a thread não vai parar
        }
    }
    return result;
});

// CORRETO — respeita interrupção, encerra rápido
scope.fork(() -> {
    for (int i = 0; i < 1_000_000; i++) {
        if (Thread.currentThread().isInterrupted()) break; // ✔ verifica
        try {
            process(items.get(i));
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt(); // ✔ restaura a flag
            break;
        }
    }
    return result;
});
```

**Fix:** em todo loop longo dentro de subtarefas, verifique `Thread.currentThread().isInterrupted()` e nunca engula `InterruptedException` sem restaurar a flag.

---

### (3) Misturar `ExecutorService` manual dentro do escopo estruturado

**O problema:** submeter tarefas a um `ExecutorService` externo dentro de um `StructuredTaskScope` cria tarefas fora da hierarquia do escopo. O scope não sabe da existência dessas tarefas, não as cancela, e o benefício estrutural se perde.

```java
// PROBLEMÁTICO — tarefa escapa da estrutura
ExecutorService pool = Executors.newCachedThreadPool();

try (var scope = StructuredTaskScope.open(Joiner.awaitAllSuccessfulOrThrow())) {
    var userTask = scope.fork(() -> fetchUser(userId));
    // ❌ Esta tarefa não está no escopo — não é cancelada com o scope
    Future<String> extra = pool.submit(() -> auditLog(userId));
    scope.join();
    // extra ainda pode estar rodando aqui!
}
```

**Fix:** qualquer tarefa que deva ser cancelada com o escopo deve ser disparada via `scope.fork()`. Se precisar de um pool customizado (ex.: thread platform para operações bloqueantes antigas), configure via `StructuredTaskScope.Configuration` — não use `ExecutorService` externo para lógica que pertence ao escopo.

---

### (extra) Tratar como GA e esquecer `--enable-preview`

**O problema:** a documentação do JDK 25 marca `StructuredTaskScope` como `[PREVIEW]`. Código compilado sem `--enable-preview` falha em compilação:

```
error: StructuredTaskScope is a preview API and is disabled by default.
  (use --enable-preview to enable preview APIs)
```

Em projetos Maven/Gradle, `--enable-preview` precisa ser passado tanto para o compilador quanto para a JVM de testes e produção. É fácil configurar só no compilador e esquecer no runtime — o programa falhará com `UnsupportedClassVersionError` em tempo de carga.

```xml
<!-- Maven — habilitar preview em compilação E em testes -->
<plugin>
    <artifactId>maven-compiler-plugin</artifactId>
    <configuration>
        <compilerArgs>
            <arg>--enable-preview</arg>
        </compilerArgs>
        <release>25</release>
    </configuration>
</plugin>
<plugin>
    <artifactId>maven-surefire-plugin</artifactId>
    <configuration>
        <argLine>--enable-preview</argLine>
    </configuration>
</plugin>
```

**Fix:** ao adotar qualquer API preview, configure `--enable-preview` em todos os estágios do build (compile, test, run) e adicione um comentário no código explicando que a feature é preview e em qual versão Java.

## Em entrevista

### Frase pronta (inglês)

> "Structured concurrency treats a group of concurrent subtasks as a single unit of work: all subtasks are forked within a scope, and the scope does not close until every subtask has finished — either successfully or by cancellation. This eliminates the most common bugs in traditional executor-based code: orphan threads that keep running after a parent failure, resource leaks from forgotten cancellation calls, and error-handling logic scattered across `Future.get()` catch blocks."
>
> "The API in JDK 25 centers on `StructuredTaskScope.open(joiner)`, where the `Joiner` defines the shutdown policy — `awaitAllSuccessfulOrThrow` to fail fast if any subtask fails, or `anySuccessfulResultOrThrow` to return the first successful result and cancel the rest. Each `fork()` call returns a typed `Subtask`, and results are only safe to read after `scope.join()` returns."
>
> "One important caveat: as of Java 25, `StructuredTaskScope` is still a preview API — it requires `--enable-preview` at both compile time and runtime, and the API has already evolved significantly from its first preview in Java 21, so production adoption requires careful evaluation of migration cost across future Java versions."

### Vocabulário

| Termo PT | Termo EN |
|----------|----------|
| concorrência estruturada | structured concurrency |
| escopo de tarefas | task scope |
| subtarefa | subtask |
| política de encerramento | shutdown policy / joiner policy |
| cancelamento automático | automatic cancellation |
| tarefa órfã | orphan task / leaked task |
| esperar todas completarem | await all / join all |
| primeira-que-vencer | race / short-circuit (first result wins) |
| propagação de erro estruturada | structured error propagation |
| feature em preview | preview feature |

## Veja também

- [[12 - Virtual Threads e Project Loom]]
- [[14 - Scoped values]]
- [[08 - Executors e thread pools]]
- [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|MOC do galho]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[Java Concurrency]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#Structured concurrency|structured concurrency]]

## Referências

- [StructuredTaskScope — Java SE 25 API (Oracle)](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/concurrent/StructuredTaskScope.html)
- [StructuredTaskScope.Joiner — Java SE 25 API (Oracle)](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/concurrent/StructuredTaskScope.Joiner.html)
- [JEP da série de previews de Structured Concurrency](https://openjdk.org/jeps/505) — JEP 505 (Java 25 preview); a série inclui JEPs anteriores desde o Java 21
- [Project Loom — OpenJDK](https://openjdk.org/projects/loom/)
