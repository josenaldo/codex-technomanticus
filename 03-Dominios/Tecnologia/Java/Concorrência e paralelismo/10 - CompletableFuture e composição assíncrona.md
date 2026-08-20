---
title: "CompletableFuture e composição assíncrona"
created: 2026-06-03
updated: 2026-06-03
type: concept
progress: backlog
status: seedling
publish: true
fase: Adepto
tags:
  - java
  - concorrencia
  - adepto
  - completablefuture
  - async
aliases:
  - CompletableFuture
  - Composição assíncrona
---

# CompletableFuture e composição assíncrona

> [!abstract] TL;DR
> **`CompletableFuture<T>`** é a API de composição assíncrona do Java desde a versão 8. Ao contrário do `Future` clássico, ele não exige `get()` bloqueante — as operações são encadeadas como um pipeline: `thenApply` (map), `thenCompose` (flatMap), `thenCombine` (zip), `allOf` (fan-in). Para tratamento de erro existem `exceptionally`, `handle` e `whenComplete`. Java 9 adicionou `orTimeout` e `completeOnTimeout` para timeouts sem bloquear. O executor padrão de todos os métodos `Async` sem argumento é o `ForkJoinPool.commonPool()` — em código de produção que faz I/O, passe sempre um executor próprio para não saturar o pool compartilhado.

## O que é

`CompletableFuture<T>` é uma implementação de `CompletionStage<T>` introduzida no Java 8 que representa um cálculo assíncrono cujo resultado pode ser composto, transformado e combinado com outros cálculos sem bloquear a thread chamadora.

O predecessor, `Future<T>` (Java 5), era unidimensional: ou você chamava `get()` e bloqueava, ou checava `isDone()` em polling. Não havia como encadear operações. `CompletableFuture` resolve isso modelando o fluxo como um **grafo de continuações** — cada passo é registrado como um callback que executa assim que o passo anterior concluir.

```java
// Future clássico — forçado a bloquear
Future<User> f = executor.submit(() -> buscarUsuario(id));
User user = f.get();  // bloqueia aqui até o resultado chegar

// CompletableFuture — pipeline sem bloqueio
CompletableFuture.supplyAsync(() -> buscarUsuario(id))
    .thenApply(User::getNome)
    .thenAccept(nome -> log.info("Usuário: {}", nome));
// a thread atual segue imediatamente; os passos rodam em outra thread
```

## Por que importa

Em aplicações que fazem chamadas a serviços externos (banco, API REST, cache), o padrão "uma thread por requisição" desperdiça recursos: a thread fica parada esperando I/O na maior parte do tempo. `CompletableFuture` permite:

- **Paralelismo fácil**: disparar N chamadas ao mesmo tempo com `allOf` e combinar os resultados.
- **Composição expressiva**: encadear transformações sem callbacks aninhados ("callback hell").
- **Resiliência**: tratar erros na cadeia com `exceptionally`/`handle`, ou definir valores de fallback com `completeOnTimeout`.
- **Integração**: é a abstração de baixo nível que frameworks como Spring WebFlux, gRPC Java e Vert.x expõem ou geram internamente.

Em entrevistas, `CompletableFuture` aparece nos temas de *async programming*, *reactive systems* e design de serviços de alta disponibilidade.

## Como funciona

### Criação (`supplyAsync` / `runAsync`)

```java
// supplyAsync — computa e retorna um valor
CompletableFuture<String> cfStr =
    CompletableFuture.supplyAsync(() -> buscarDados());

// supplyAsync com executor explícito — recomendado em produção
ExecutorService ioPool = Executors.newFixedThreadPool(10);
CompletableFuture<String> cfIO =
    CompletableFuture.supplyAsync(() -> buscarDados(), ioPool);

// runAsync — executa sem retorno (Void)
CompletableFuture<Void> cfRun =
    CompletableFuture.runAsync(() -> enviarEmail(usuario));

// Valor já conhecido (útil em testes / short-circuit)
CompletableFuture<String> pronto =
    CompletableFuture.completedFuture("valor fixo");

// Já completado com exceção (útil em testes) — failedFuture é Java 9+
CompletableFuture<String> falhou =
    CompletableFuture.failedFuture(new RuntimeException("erro"));
```

---

### Transformação (`thenApply` / `thenAccept` / `thenRun`)

Esses três métodos representam os três casos de uso de uma continuação:

| Método | Recebe resultado? | Retorna valor? | Análogo |
|---|---|---|---|
| `thenApply(fn)` | sim | sim | `Stream.map` |
| `thenAccept(consumer)` | sim | não (`Void`) | side effect |
| `thenRun(runnable)` | não | não (`Void`) | callback puro |

```java
CompletableFuture.supplyAsync(() -> 42)
    .thenApply(n -> n * 2)            // 84
    .thenAccept(n -> log.info("{}", n)) // loga 84, retorna Void
    .thenRun(() -> metricas.incrementar()); // sem acesso ao valor
```

---

### Encadeamento: `thenCompose` (flatMap) vs `thenApply` (map)

Esta é a distinção mais cobrada em entrevistas sobre `CompletableFuture`.

**`thenApply`** aplica uma função `T → U` e devolve `CompletableFuture<U>`. Se a função retornar um `CompletableFuture<U>`, o resultado seria `CompletableFuture<CompletableFuture<U>>` — aninhamento inútil.

**`thenCompose`** aplica uma função `T → CompletionStage<U>` e **achata** (flatten) o resultado para `CompletableFuture<U>`. É o equivalente de `flatMap` do `Stream` ou `Optional`.

```java
// thenApply com função que retorna CF → aninhamento indesejado
CompletableFuture<CompletableFuture<Pedido>> errado =
    buscarUsuario(id).thenApply(user -> buscarPedidos(user.getId()));

// thenCompose → achata para CF<Pedido>
CompletableFuture<List<Pedido>> certo =
    buscarUsuario(id).thenCompose(user -> buscarPedidos(user.getId()));

// Encadeamento de múltiplos passos dependentes
CompletableFuture<BigDecimal> total =
    buscarUsuario(id)
        .thenCompose(user -> buscarPedidos(user.getId()))
        .thenCompose(pedidos -> calcularTotal(pedidos));
```

**Regra prática:** se a função que você passa ao `thenApply` retorna um `CompletableFuture`, troque por `thenCompose`.

---

### Combinação (`thenCombine` / `allOf` / `anyOf`)

**`thenCombine`** — combina o resultado de dois futuros independentes com uma `BiFunction`:

```java
CompletableFuture<Usuario> cfUsuario = buscarUsuario(id);
CompletableFuture<Endereco> cfEndereco = buscarEndereco(id);

CompletableFuture<UsuarioCompleto> cfCombinado =
    cfUsuario.thenCombine(cfEndereco,
        (usuario, endereco) -> new UsuarioCompleto(usuario, endereco));
// dispara as duas buscas em paralelo; combina quando ambas concluírem
```

**`allOf`** — fan-in: conclui quando **todos** os futuros passados concluírem. Retorna `CompletableFuture<Void>` — os resultados individuais precisam ser coletados manualmente:

```java
List<CompletableFuture<Produto>> futures = ids.stream()
    .map(id -> CompletableFuture.supplyAsync(() -> buscarProduto(id), ioPool))
    .toList();

CompletableFuture<List<Produto>> todos =
    CompletableFuture.allOf(futures.toArray(new CompletableFuture[0]))
        .thenApply(v -> futures.stream()
            .map(CompletableFuture::join)  // join() aqui é seguro: todos já completaram
            .toList());
```

**`anyOf`** — retorna o resultado do **primeiro** futuro a concluir (tipo `Object`; requer cast):

```java
CompletableFuture<Object> primeiro =
    CompletableFuture.anyOf(replica1, replica2, replica3);
// útil para hedged requests: dispara para 3 réplicas, usa quem responder primeiro
```

---

### Error handling (`exceptionally` / `handle` / `whenComplete`)

Os três métodos diferem em quando são chamados e se podem transformar o resultado:

| Método | Chamado quando | Transforma resultado? | Tipo retornado |
|---|---|---|---|
| `exceptionally(fn)` | só se houve exceção | sim (recovery value) | `CompletableFuture<T>` |
| `handle(biFunction)` | sempre (OK ou erro) | sim (novo valor U) | `CompletableFuture<U>` |
| `whenComplete(biConsumer)` | sempre (OK ou erro) | não (side effect) | `CompletableFuture<T>` |

```java
// exceptionally — fornece valor de fallback em caso de erro
buscarDados()
    .thenApply(Dados::processar)
    .exceptionally(ex -> {
        log.error("Falha no pipeline", ex);
        return Dados.vazio();  // valor de recuperação
    });

// handle — acesso a resultado E exceção; sempre executa
buscarDados().handle((dados, ex) -> {
    if (ex != null) {
        log.error("Erro: {}", ex.getMessage());
        return Dados.vazio();
    }
    return dados.processar();
});

// whenComplete — side effect (log, métricas) sem alterar o resultado
buscarDados().whenComplete((dados, ex) -> {
    if (ex != null) metricas.incrementarErros();
    else metricas.incrementarSucessos();
});
// o future resultante mantém o mesmo resultado/exceção original
```

---

### Timeout (`orTimeout` / `completeOnTimeout`, Java 9+)

Antes do Java 9, implementar timeout em um `CompletableFuture` exigia um `ScheduledExecutorService` manual. O Java 9 adicionou dois métodos de conveniência:

```java
// orTimeout — completa excepcionalmente com TimeoutException após o prazo
CompletableFuture<Dados> cf = buscarDados()
    .orTimeout(3, TimeUnit.SECONDS);
// se não concluir em 3s → cf.isCompletedExceptionally() == true

// completeOnTimeout — completa com valor padrão após o prazo
CompletableFuture<Dados> cfComFallback = buscarDados()
    .completeOnTimeout(Dados.vazio(), 3, TimeUnit.SECONDS);
// se não concluir em 3s → cf.join() == Dados.vazio()
```

Ambos retornam o próprio `CompletableFuture<T>` para encadeamento. O timer é gerenciado por uma thread daemon interna da JVM — não é necessário nenhum executor adicional.

---

### Async vs sync variants e qual executor (common pool default)

Todo método de continuação existe em três versões. Usando `thenApply` como exemplo:

| Variante | Onde executa |
|---|---|
| `thenApply(fn)` | na thread que completou o future anterior (ou na thread chamadora, se já concluído) |
| `thenApplyAsync(fn)` | no `ForkJoinPool.commonPool()` |
| `thenApplyAsync(fn, executor)` | no executor fornecido |

O mesmo padrão vale para `thenAccept`, `thenRun`, `thenCompose`, `thenCombine`, `handle`, `whenComplete` e `exceptionally` (que tem `exceptionallyAsync` desde Java 12).

**Por que o executor padrão importa:** o `ForkJoinPool.commonPool()` é um pool **compartilhado pela JVM inteira** — é o mesmo pool usado por `Streams` paralelos e outras operações. Se suas operações fazem I/O bloqueante (JDBC, HTTP), o pool se esgota e degrada toda a aplicação. A versão com executor explícito é mandatória em código de produção para I/O.

```java
// Ruim para I/O — usa o common pool, que é otimizado para CPU
CompletableFuture.supplyAsync(() -> jdbcRepository.buscar(id))

// Correto — pool dedicado para I/O
ExecutorService ioPool = Executors.newVirtualThreadPerTaskExecutor(); // Java 21
CompletableFuture.supplyAsync(() -> jdbcRepository.buscar(id), ioPool)
```

## Na prática

### Orquestrar duas chamadas paralelas e combinar

O padrão mais comum: duas buscas independentes disparadas em paralelo, resultado combinado quando ambas terminam.

```java
public PerfilCompleto montarPerfil(Long usuarioId) {
    ExecutorService ioPool = Executors.newFixedThreadPool(10);

    CompletableFuture<Usuario> cfUsuario =
        CompletableFuture.supplyAsync(() -> usuarioService.buscar(usuarioId), ioPool);

    CompletableFuture<List<Pedido>> cfPedidos =
        CompletableFuture.supplyAsync(() -> pedidoService.listar(usuarioId), ioPool);

    return cfUsuario
        .thenCombine(cfPedidos, PerfilCompleto::new)
        .orTimeout(5, TimeUnit.SECONDS)           // Java 9+
        .exceptionally(ex -> PerfilCompleto.parcial(usuarioId))
        .join();  // bloqueia apenas no ponto de coleta — OK em borda de serviço síncrono
}
```

As duas buscas rodam em paralelo. `thenCombine` junta os resultados quando ambas concluírem. `orTimeout` evita espera indefinida. `exceptionally` devolve um perfil parcial em caso de falha.

---

### Fan-out / fan-in com `allOf`

Quando o número de futuros é dinâmico (ex: buscar N produtos de uma lista de IDs):

```java
public List<Produto> buscarProdutos(List<Long> ids) {
    ExecutorService ioPool = Executors.newFixedThreadPool(20);

    List<CompletableFuture<Produto>> futures = ids.stream()
        .map(id -> CompletableFuture.supplyAsync(
            () -> catalogoService.buscar(id), ioPool))
        .toList();

    // allOf espera todos; thenApply coleta os resultados
    return CompletableFuture
        .allOf(futures.toArray(new CompletableFuture[0]))
        .thenApply(v -> futures.stream()
            .map(CompletableFuture::join)  // seguro: allOf garantiu que todos concluíram
            .toList())
        .orTimeout(10, TimeUnit.SECONDS)
        .join();
}
```

**Por que `join()` e não `get()`:** `join()` lança `CompletionException` (unchecked) em vez de `ExecutionException` (checked) — mais compatível com lambdas e streams.

## Armadilhas

### (1) Bloquear I/O no common pool — satura o pool compartilhado

**O problema:** ao usar `supplyAsync` sem executor explícito, a operação roda no `ForkJoinPool.commonPool()`. Esse pool tem número de threads igual ao número de CPUs disponíveis e é otimizado para trabalho CPU-bound sem bloqueio. Operações I/O bloqueantes (JDBC, chamadas HTTP síncronas) mantêm as threads presas esperando, esgotam o pool e degradam **toda** a aplicação — incluindo streams paralelos e outros futuros que não têm nada a ver com o seu código.

```java
// RUIM — I/O no common pool (compartilhado com streams paralelos, etc.)
List<CompletableFuture<Dado>> futures = ids.stream()
    .map(id -> CompletableFuture.supplyAsync(
        () -> jdbcRepo.buscar(id)))  // bloqueia thread do common pool
    .toList();
```

```java
// FIX — executor dedicado para I/O
ExecutorService ioPool = Executors.newFixedThreadPool(
    Runtime.getRuntime().availableProcessors() * 10);

List<CompletableFuture<Dado>> futures = ids.stream()
    .map(id -> CompletableFuture.supplyAsync(
        () -> jdbcRepo.buscar(id), ioPool))  // pool isolado
    .toList();

// Melhor ainda em Java 21: virtual threads são ideais para I/O bloqueante
ExecutorService vPool = Executors.newVirtualThreadPerTaskExecutor();
```

**Regra:** common pool = CPU-bound / não bloqueante. I/O = executor separado (ou virtual threads no Java 21+).

---

### (2) Chamar `get()` sem timeout — trava indefinidamente

**O problema:** `future.get()` sem timeout bloqueia a thread **para sempre** se a operação travar ou o serviço remoto parar de responder. Em produção isso significa thread leak e, dependendo do framework, exaustão do pool de threads da aplicação.

```java
// RUIM — pode bloquear para sempre
try {
    Dados resultado = future.get();  // sem timeout!
} catch (InterruptedException | ExecutionException e) {
    tratarErro(e);
}
```

```java
// FIX opção A — get() com timeout
try {
    Dados resultado = future.get(5, TimeUnit.SECONDS);
} catch (TimeoutException e) {
    future.cancel(true);
    return Dados.vazio();
} catch (InterruptedException | ExecutionException e) {
    tratarErro(e);
}

// FIX opção B — orTimeout antes de qualquer join/get (Java 9+, mais idiomático)
Dados resultado = future
    .orTimeout(5, TimeUnit.SECONDS)
    .exceptionally(ex -> Dados.vazio())
    .join();
```

**Prefira `join()` a `get()`** no pipeline de `CompletableFuture`: `join()` lança `CompletionException` (unchecked), que compõe melhor com lambdas. Use `get()` quando precisar distinguir `InterruptedException` de `ExecutionException`.

---

### (3) Perder exceção sem `handle` / `exceptionally` — falha silenciosa

**O problema:** `CompletableFuture` **não propaga exceções automaticamente** para nenhum lugar. Se um futuro completar excepcionalmente e ninguém chamar `get()`, `join()` ou anexar um handler de erro, a exceção desaparece sem rastro. Isso é especialmente traiçoeiro em pipelines do tipo "dispara e esquece" (`thenRun` / `thenAccept` sem retorno observável).

```java
// RUIM — exceção silenciada: ninguém observa o futuro
CompletableFuture.supplyAsync(() -> {
    throw new RuntimeException("falha na tarefa");
}).thenAccept(resultado -> processar(resultado));
// RuntimeException jogada fora; a aplicação continua sem saber
```

```java
// FIX A — handle no final do pipeline
CompletableFuture.supplyAsync(() -> buscarDados())
    .thenApply(Dados::processar)
    .handle((resultado, ex) -> {
        if (ex != null) {
            log.error("Erro no pipeline de dados", ex);
            alertas.enviar("pipeline-dados", ex);
            return null;
        }
        return resultado;
    });

// FIX B — whenComplete para log/métricas sem alterar resultado
CompletableFuture.supplyAsync(() -> buscarDados())
    .thenApply(Dados::processar)
    .whenComplete((resultado, ex) -> {
        if (ex != null) log.error("Falha", ex);
        else metricas.sucesso();
    });

// FIX C — se alguém vai chamar join(), o try/catch captura
try {
    future.join();
} catch (CompletionException e) {
    log.error("Exceção na tarefa assíncrona", e.getCause());
}
```

**Regra:** todo pipeline `CompletableFuture` de produção deve ter ao menos um `handle`, `exceptionally` ou `whenComplete` para observabilidade de erros — ou ser observado via `join()` / `get()` em um ponto de coleta.

## Em entrevista

### Frase pronta (inglês)

> "The core distinction between `thenApply` and `thenCompose` mirrors `map` versus `flatMap` in streams: `thenApply` takes a regular function and wraps the result in a new `CompletableFuture`, while `thenCompose` takes a function that itself returns a `CompletionStage` and flattens it — so you avoid `CompletableFuture<CompletableFuture<T>>` nesting when chaining dependent async calls."
>
> "For fan-out/fan-in patterns, `allOf` lets you fire N independent futures in parallel and collect results when all complete — but since it returns `CompletableFuture<Void>`, you still need to call `join()` on each individual future inside the `thenApply` callback; `anyOf` is useful for hedged requests where you want the fastest replica to win."
>
> "A common production mistake is using the default async executor — `ForkJoinPool.commonPool()` — for I/O-bound work like JDBC queries or HTTP calls. That pool is shared JVM-wide, sized to the number of CPUs, and optimized for non-blocking CPU work. Saturating it with blocking I/O degrades parallel streams and other unrelated parts of the application. The fix is always to pass an explicit `ExecutorService` — or in Java 21, a virtual-thread executor — to every `supplyAsync` that does I/O."

### Vocabulário

| Termo PT | Termo EN |
|---|---|
| composição assíncrona | async composition / async pipeline |
| futuro encadeado | chained future / completion stage |
| achatamento de futuro aninhado | flattening nested futures |
| fan-out / fan-in | fan-out / fan-in (mesmo em PT-BR técnico) |
| pool de threads compartilhado | shared thread pool / common pool |
| exceção silenciosa | silent exception / swallowed exception |
| timeout sem bloqueio | non-blocking timeout |
| variante assíncrona | async variant |
| executor dedicado | dedicated executor |
| continuação | continuation / callback stage |

## Veja também

- [[08 - Executors e thread pools]]
- [[12 - Virtual Threads e Project Loom]]
- [[15 - Parallel streams e fork-join]]
- [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|MOC do galho]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[Java Concurrency]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#CompletableFuture|CompletableFuture]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#Future|Future]]

## Referências

- [CompletableFuture — Java 21 API (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/CompletableFuture.html)
- [CompletionStage — Java 21 API (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/CompletionStage.html)
- [ForkJoinPool.commonPool — Java 21 API (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/ForkJoinPool.html#commonPool())
- [Concurrency — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/essential/concurrency/)
