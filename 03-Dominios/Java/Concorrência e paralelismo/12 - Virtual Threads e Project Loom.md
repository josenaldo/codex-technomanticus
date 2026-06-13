---
title: "Virtual Threads e Project Loom"
created: 2026-06-03
updated: 2026-06-10
type: concept
progress: backlog
status: seedling
publish: true
fase: magus
tags:
  - java
  - concorrencia
  - magus
  - virtual-threads
  - loom
aliases:
  - Virtual Threads
  - Project Loom
  - Virtual thread
---

# Virtual Threads e Project Loom

> [!abstract] TL;DR
> Uma **virtual thread** é uma thread leve gerenciada pela JVM, **não** mapeada 1:1 com uma thread do sistema operacional. Você pode ter milhões delas num único processo. Resultado do **Project Loom**, foram tornadas **GA (final) no Java 21** pela **JEP 444** (foram *preview* no Java 19 e 20). Elas ressuscitam o modelo **thread-per-request** imperativo e bloqueante, com a escalabilidade que antes só o código assíncrono/reativo entregava: você escreve código síncrono simples e a JVM multiplexa milhões de virtual threads sobre um punhado de **carrier threads** (platform threads de um `ForkJoinPool` interno). Quando uma virtual thread bloqueia em I/O, ela **desmonta** (*unmount*) do carrier e libera-o para outra. A grande armadilha é o **pinning**: dentro de um bloco `synchronized` ou de uma chamada nativa, a virtual thread **não consegue desmontar** e prende o carrier — a mitigação é trocar `synchronized` por `ReentrantLock`. Regra de ouro: **crie uma virtual thread por tarefa** (`Executors.newVirtualThreadPerTaskExecutor()`); **nunca faça pool** nem limite o número de virtual threads — pooling de virtual threads é anti-pattern. E lembre: elas escalam I/O-bound, **não aceleram CPU-bound**.

## O que é

Uma **virtual thread** é uma `java.lang.Thread` cujo ciclo de vida e agendamento são controlados pela **JVM**, em vez de delegados ao agendador do sistema operacional. Ela continua sendo uma `Thread` de verdade — implementa a mesma API, aparece em thread dumps, tem nome, pode ser interrompida — mas é **leve**: a JVM mantém sua pilha no heap e só a "monta" sobre uma thread do SO quando ela tem trabalho de CPU a fazer.

O contraste é com a **platform thread**, que é um invólucro fino sobre uma thread do SO (modelo **1:1**): cada platform thread consome uma thread do kernel pelo tempo todo de sua existência, com pilha grande (tipicamente na casa do megabyte) e custo de criação alto. Por isso uma JVM consegue sustentar, na prática, apenas alguns milhares de platform threads — enquanto pode sustentar **milhões** de virtual threads.

A motivação histórica é a **ressurreição do modelo thread-per-request**. Servidores tradicionais (Tomcat, Jetty no modelo clássico) dedicam uma thread por requisição: código simples, imperativo, fácil de depurar — mas a thread fica bloqueada esperando I/O (banco, HTTP, disco), desperdiçando uma thread cara do SO. Para escalar, a indústria migrou para pools fixos (`newFixedThreadPool(200)`) e depois para programação assíncrona/reativa, que escala mas torna o código "colorido", difícil de ler e de depurar.

Virtual threads desfazem esse trade-off: você **mantém o código síncrono e bloqueante** (thread-per-request), e a JVM cuida de não desperdiçar threads do SO durante o bloqueio. O modelo mental volta a ser linear, e ainda assim escala para centenas de milhares de requisições concorrentes.

```java
// Uma virtual thread é uma Thread — mesma API, peso radicalmente menor
Thread vt = Thread.ofVirtual().start(() -> {
    System.out.println("Rodando em: " + Thread.currentThread());
    // imprime algo como: VirtualThread[#23]/runnable@ForkJoinPool-1-worker-3
});
vt.join();

System.out.println(vt.isVirtual()); // true (API de Java 21)
```

## Por que importa

A pergunta central não é "virtual threads são melhores?", e sim **"melhores para quê?"**. A comparação justa exige separar dois eixos: o tipo de carga (I/O-bound vs CPU-bound) e o estilo de programação (imperativo vs reativo).

### Quando usar (e quando NÃO)

> [!success] Use virtual threads para
> - **I/O-bound** — clientes HTTP, consultas a banco, I/O de arquivo, sockets. Aqui a thread passa a maior parte do tempo **bloqueada esperando**, e é exatamente nesse bloqueio que a virtual thread desmonta e libera o carrier.
> - **Alta concorrência / alto fan-out** — agregar dados de muitos serviços, milhares ou milhões de tarefas concorrentes simultâneas.
> - **Modelo thread-per-request** — substituir pools fixos grandes (`newFixedThreadPool(500)`) por "uma virtual thread por requisição".

> [!failure] NÃO use virtual threads para
> - **CPU-bound** — trabalho que satura a CPU **não acelera** com virtual threads. Elas não executam código mais rápido; entregam **escala (throughput)**, não **velocidade (latência)**. Para CPU-bound, o limite continua sendo o número de núcleos, e platform threads (ou um pool dimensionado pelos núcleos) seguem sendo a ferramenta certa.
> - **Como recurso a ser *pooled***. Fazer pool ou limitar o número de virtual threads é **anti-pattern** (ver Armadilhas). Platform threads são escassas — por isso se faz pool delas. Virtual threads são abundantes — crie **uma por tarefa**.

> [!warning] Virtual threads NÃO são "threads mais rápidas"
> Elas não fazem nenhuma operação individual rodar mais rápido. O ganho aparece **apenas** quando há concorrência massiva de tarefas que passam tempo bloqueadas. A regra prática da Oracle é que o benefício se materializa na ordem de **milhares a dezenas de milhares** de tarefas concorrentes — abaixo disso, platform threads bastam.

### Virtual threads vs reactive

Programação reativa (Reactor, RxJava) foi a resposta da era pré-Loom para escalar I/O sem pagar o custo de uma thread do SO por requisição. Virtual threads tornam o reativo **menos necessário em muitos casos**, porque entregam escala parecida mantendo código imperativo e depurável.

Um esboço da comparação:

| Aspecto | Virtual threads | Reativo |
| --- | --- | --- |
| Modelo | Síncrono / imperativo | Assíncrono / declarativo |
| Legibilidade | Igual a código bloqueante | Cadeias de operadores |
| Debugging | Stack trace normal | Difícil (fragmentado) |
| Backpressure | Não nativo | Nativo |
| Libs bloqueantes | Compatíveis direto | Precisam de adaptador |

> [!note] A comparação aprofundada com reativo é assunto de outro galho
> Este card não ensina programação reativa. O confronto detalhado (backpressure, operadores, quando reativo ainda vence) pertence ao **Galho 11** — [[03-Dominios/Java/Programação Reativa/14 - Reativo vs Virtual Threads — o confronto honesto|Reativo vs Virtual Threads]]. Para o panorama de concorrência completo, ver o tronco [[Java Concurrency]].

## Como funciona

### Platform threads (= OS thread) vs virtual threads

| Aspecto | Platform thread | Virtual thread |
| --- | --- | --- |
| Mapeamento | **1:1** com thread do SO | M:N — multiplexada sobre poucas threads do SO |
| Gerenciada por | Agendador do **SO** | Agendador da **JVM** |
| Pilha | Grande, mantida pelo SO (~MB) | Rasa, no heap; cresce/encolhe sob demanda |
| Custo de criação | Alto (syscall) | Baixo (objeto na JVM) |
| Quantidade viável | Milhares | **Milhões** |
| Criação | `Thread.ofPlatform()` | `Thread.ofVirtual()` |
| Melhor para | CPU-bound | I/O-bound, alta concorrência |

A platform thread **captura** uma thread do SO por toda a sua vida. A virtual thread **não está presa** a nenhuma thread do SO específica: ela só ocupa uma enquanto efetivamente roda código.

### Carrier threads (ForkJoinPool) e mount/unmount

A JVM mantém um pool de platform threads chamadas **carrier threads** — concretamente, um `ForkJoinPool` dedicado (distinto do `commonPool()`), dimensionado por padrão pelo número de processadores disponíveis. Cada virtual threads "anda em cima" de um carrier para executar:

- **Mount (montar)** — a JVM atribui a virtual thread a um carrier e ela executa código nessa platform thread.
- **Run** — enquanto faz trabalho de CPU, a virtual thread permanece montada.
- **Unmount (desmontar)** — ao atingir uma operação **bloqueante** (I/O de rede, espera em lock compatível, `Thread.sleep`, etc.), a virtual thread **suspende e desmonta** do carrier. Sua continuação (pilha) é guardada no heap.
- **Carrier liberado** — o carrier fica livre para montar **outra** virtual thread. Quando a operação bloqueante termina, a virtual thread é remontada (possivelmente em outro carrier) e prossegue.

```text
Carriers (platform threads, ~Nº de núcleos):  [ C1 ]   [ C2 ]   [ C3 ]   [ C4 ]
                                                 │        │        │        │
                                                 ▼        ▼        ▼        ▼
Virtual threads (milhões):   VT-1   VT-2   VT-3   ...   VT-999998   VT-999999  VT-1000000
                              ▲                          ▲
                       montada: usando CPU         bloqueada em I/O →
                                                   desmontou e liberou o carrier
```

É essa multiplexação (**muitas** virtual threads sobre **poucos** carriers) que permite manter centenas de milhares de tarefas "vivas" enquanto a maioria está apenas esperando I/O.

> [!info] A maior parte do I/O bloqueante já foi adaptado
> Para que a desmontagem funcione, a JVM do Java 21 reimplementou as APIs de I/O bloqueante (sockets, `java.net.http.HttpClient`, etc.) para cooperar com o agendador de virtual threads. Bloquear num socket dentro de uma virtual thread **desmonta** corretamente, sem prender o carrier — desde que você não esteja num bloco que cause **pinning** (a seguir).

### Pinning (synchronized block / native call prendem o carrier — armadilha)

**Pinning** acontece quando uma virtual thread **não consegue desmontar** ao bloquear, ficando "pregada" (*pinned*) ao seu carrier. Enquanto pinned, a virtual thread monopoliza uma platform thread do SO durante o bloqueio — exatamente o desperdício que virtual threads vieram eliminar. No Java 21, há duas causas principais:

1. **Bloquear dentro de um bloco/método `synchronized`** — o monitor do objeto está amarrado ao carrier; a JVM não pode trocar de carrier sem violar a semântica do monitor.
2. **Bloquear dentro de um método nativo (JNI) ou de uma chamada *foreign function*** — a JVM não controla a pilha nativa para suspendê-la.

> [!warning] Pinning não é sempre catastrófico — mas é uma armadilha real
> Pinning **curto e raro** é tolerável. O problema é pinning **frequente ou longo** dentro de seções que bloqueiam: ele estrangula o pool de carriers e derruba o throughput. Por padrão, o evento JFR `jdk.VirtualThreadPinned` é gravado quando o pinning ultrapassa ~20 ms, justamente para sinalizar os casos que importam.

**Diagnóstico** — habilite o rastreamento de threads pinned:

```bash
# Stack trace completo de cada evento de pinning
java -Djdk.tracePinnedThreads=full -jar app.jar

# Só os frames problemáticos (saída mais enxuta)
java -Djdk.tracePinnedThreads=short -jar app.jar
```

Ou inspecione o evento JFR `jdk.VirtualThreadPinned` em uma gravação.

**Mitigação** — troque `synchronized` por `ReentrantLock` em seções críticas que bloqueiam (detalhado em Na prática e em Armadilhas). `ReentrantLock` é "ciente" de virtual threads e permite a desmontagem.

> [!note] O cenário de versões evolui
> Os fatos acima valem para o **Java 21 (JEP 444, GA)**. O `synchronized`-pinning é uma **limitação conhecida** desta versão; releases posteriores trabalharam para reduzi-lo. Verifique as notas da sua versão específica antes de afirmar que "synchronized não causa mais pinning" — neste card, assuma o comportamento do Java 21.

### Criação

Há duas formas idiomáticas de criar virtual threads no Java 21.

**1. Diretamente, via `Thread.ofVirtual()`** (a `Thread.Builder` de virtual threads):

```java
// Mais simples: cria e inicia uma virtual thread
Thread t = Thread.ofVirtual().start(() -> System.out.println("Olá da virtual thread"));
t.join();

// Com nome (útil em thread dumps)
Thread.Builder builder = Thread.ofVirtual().name("worker-", 0);
Thread t0 = builder.start(tarefa); // nome "worker-0"
Thread t1 = builder.start(tarefa); // nome "worker-1"

// Apenas construir (sem iniciar) — start() depois
Thread naoIniciada = Thread.ofVirtual().unstarted(tarefa);
naoIniciada.start();
```

**2. Via executor `newVirtualThreadPerTaskExecutor()`** — cria **uma virtual thread nova por tarefa submetida** (não há pool):

```java
// O executor é AutoCloseable — close() (no try-with-resources) espera todas as tarefas
try (ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor()) {
    Future<String> f = executor.submit(() -> {
        // código bloqueante simples — sem callbacks
        return chamarServico();
    });
    System.out.println(f.get());
} // close() aguarda o término de todas as tarefas submetidas
```

A diferença essencial em relação a `newFixedThreadPool(n)`: ali há **n** threads reutilizadas; aqui **não há reúso** — cada tarefa nasce numa virtual thread fresca e descartável. É exatamente o que se quer, porque virtual threads são baratas.

## Na prática

### Servidor thread-per-request com virtual threads

O caso de uso canônico: um servidor que atende cada requisição com uma virtual thread dedicada, escrevendo código **síncrono e bloqueante** — sem `CompletableFuture`, sem operadores reativos.

```java
// Servidor simples: uma virtual thread por conexão aceita
public class ServidorThreadPerRequest {

    public void servir(int porta) throws IOException {
        try (ServerSocket servidor = new ServerSocket(porta);
             // Uma virtual thread por requisição — nada de pool fixo
             ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor()) {

            while (true) {
                Socket conexao = servidor.accept();      // bloqueia esperando conexão
                executor.submit(() -> tratar(conexao));  // nova virtual thread por requisição
            }
        }
    }

    // Código 100% imperativo e bloqueante — fácil de ler e depurar
    private void tratar(Socket conexao) {
        try (conexao) {
            String requisicao = lerRequisicao(conexao);          // bloqueia → desmonta
            String dadosUsuario = consultarBanco(requisicao);    // bloqueia → desmonta
            String enriquecido = chamarServicoExterno(dadosUsuario); // bloqueia → desmonta
            escreverResposta(conexao, enriquecido);              // bloqueia → desmonta
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
    // métodos lerRequisicao/consultarBanco/... omitidos por brevidade
}
```

Cada `submit` cria uma virtual thread; em cada bloqueio de I/O ela desmonta e devolve o carrier. Com milhares de conexões simultâneas, ainda assim só há ~Nº-de-núcleos carriers ativos.

### Trocar `synchronized` por `ReentrantLock` em hot path (evitar pinning)

Se uma seção crítica que **bloqueia** estiver protegida por `synchronized`, ela causa pinning. Em um caminho quente (executado por muitas virtual threads), isso estrangula os carriers. A correção é usar `ReentrantLock`, que permite a desmontagem.

```java
// ❌ ANTES: synchronized + I/O bloqueante = pinning no hot path
public class CacheRemoto {
    private final Object lock = new Object();

    public String buscar(String chave) {
        synchronized (lock) {            // entra no monitor...
            return carregarDaRede(chave); // ...e bloqueia em I/O → PINNING
        }
    }
    // carregarDaRede faz I/O de rede (bloqueante)
}
```

```java
// ✅ DEPOIS: ReentrantLock é compatível com virtual threads (permite unmount)
public class CacheRemoto {
    private final ReentrantLock lock = new ReentrantLock();

    public String buscar(String chave) {
        lock.lock();
        try {
            return carregarDaRede(chave); // bloqueia em I/O → DESMONTA (sem pinning)
        } finally {
            lock.unlock();               // sempre liberar no finally
        }
    }
}
```

### Limitar acesso a um recurso escasso: `Semaphore`, não pool

Surge naturalmente a pergunta: "se eu não posso fazer pool, como limito o número de chamadas concorrentes a um serviço que aguenta, digamos, 10 simultâneas?". A resposta **não** é um pool de 10 threads — é um `Semaphore` de 10 permissões, mantendo uma virtual thread por tarefa.

```java
// Limitar concorrência a um recurso, SEM fazer pool de threads
public class ClienteLimitado {
    private final Semaphore limite = new Semaphore(10); // no máx. 10 chamadas simultâneas

    public Resultado chamar() throws InterruptedException {
        limite.acquire();      // bloqueia se 10 já estão em voo → desmonta
        try {
            return servicoLimitado(); // a tarefa segue em sua própria virtual thread
        } finally {
            limite.release();
        }
    }
}
```

O número de **virtual threads** continua igual ao número de tarefas; o `Semaphore` limita apenas o acesso concorrente ao recurso. Pool e limitação de taxa são problemas diferentes — use a ferramenta certa para cada um.

## Armadilhas

### (1) Fazer pool ou limitar o número de virtual threads (anti-pattern)

**O problema:** o instinto, herdado das platform threads, é "criar threads é caro, então reutilize via pool". Com virtual threads isso se inverte: elas são **baratas e descartáveis**, e fazer pool delas reintroduz exatamente o gargalo que elas vieram eliminar — um pool de N virtual threads volta a limitar a concorrência a N, esperando uma "vaga" liberar.

```java
// ❌ ANTI-PATTERN: pool fixo de virtual threads — limita concorrência sem motivo
ExecutorService poolErrado = Executors.newFixedThreadPool(
    200, Thread.ofVirtual().factory()); // 200 virtual threads reaproveitadas
// Com 1000 tarefas, 800 esperam por uma "vaga" — gargalo artificial
```

```java
// ✅ FIX: uma virtual thread por tarefa — sem teto artificial
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    for (var tarefa : tarefas) {
        executor.submit(tarefa); // cada tarefa em sua própria virtual thread
    }
}
```

**Regra:** o número de virtual threads deve igualar o número de tarefas concorrentes da aplicação. Se você *precisa* limitar acesso a um recurso escasso, use `Semaphore` (ver Na prática), **não** um pool.

### (2) `synchronized` em seção que bloqueia → pinning

**O problema:** bloquear dentro de um bloco/método `synchronized` causa **pinning** — a virtual thread não desmonta e prende o carrier durante todo o I/O. Num hot path, isso esgota os carriers e mata o throughput, frequentemente de forma silenciosa (a aplicação só "não escala", sem erro óbvio).

```java
// ❌ Bloqueio de I/O sob synchronized — pinning
public synchronized void salvar(Registro r) {
    repositorio.gravarNoBanco(r); // I/O bloqueante dentro do monitor → PINNING
}
```

**Fix:** substitua por `ReentrantLock`, que coopera com o agendador de virtual threads e permite a desmontagem:

```java
// ✅ ReentrantLock permite unmount durante o bloqueio
private final ReentrantLock lock = new ReentrantLock();

public void salvar(Registro r) {
    lock.lock();
    try {
        repositorio.gravarNoBanco(r); // desmonta normalmente — sem pinning
    } finally {
        lock.unlock();
    }
}
```

Detecte com `-Djdk.tracePinnedThreads=full` ou pelo evento JFR `jdk.VirtualThreadPinned`. (Cenário válido para Java 21; releases posteriores reduzem o pinning de `synchronized` — confira sua versão.)

### (3) `ThreadLocal` pesado com milhões de virtual threads (custo de memória)

**O problema:** cada virtual thread tem seus **próprios** `ThreadLocal`s. Com platform threads (poucas dezenas/centenas), guardar um objeto caro num `ThreadLocal` é uma otimização de cache aceitável. Com **milhões** de virtual threads, o mesmo padrão vira **milhões de cópias** desse objeto na memória — um vazamento de memória de fato.

```java
// ❌ Objeto mutável e caro cacheado em ThreadLocal — explode com milhões de VTs
static final ThreadLocal<SimpleDateFormat> FORMATTER =
    ThreadLocal.withInitial(() -> new SimpleDateFormat("yyyy-MM-dd"));
// 1.000.000 de virtual threads ⇒ 1.000.000 de SimpleDateFormat na memória
```

**Fix 1 — preferir um valor imutável e compartilhado** quando possível (resolve o caso do formatter):

```java
// ✅ Imutável e thread-safe: UMA instância compartilhada por todas as threads
static final DateTimeFormatter FORMATTER = DateTimeFormatter.ISO_LOCAL_DATE;
```

**Fix 2 — para propagação de contexto (ex.: id de transação, usuário), preferir scoped values.** Eles foram desenhados para ser uma alternativa imutável, mais barata e segura ao `ThreadLocal`, especialmente sob virtual threads — ver [[14 - Scoped values]].

> [!tip] Gancho para scoped values
> Sempre que pensar "preciso de `ThreadLocal` para carregar contexto pela chamada" sob virtual threads, considere **scoped values** primeiro. O ganho de memória e a imutabilidade compensam — detalhes na nota [[14 - Scoped values]].

## Em entrevista

### Frase pronta (inglês)

> "Virtual threads, made generally available in Java 21 by JEP 444, are lightweight threads scheduled by the JVM rather than the operating system, so a single process can run millions of them instead of just a few thousand platform threads."
>
> "The key trade-off is that virtual threads give you **scale, not speed**: they shine for I/O-bound, high-concurrency workloads — like a thread-per-request server — because a virtual thread *unmounts* from its carrier platform thread whenever it blocks on I/O, freeing that carrier for other work; but for CPU-bound work they bring no benefit, since you're still limited by the number of cores."
>
> "Two rules I always keep in mind: never pool or cap virtual threads — create one per task with `newVirtualThreadPerTaskExecutor` and use a `Semaphore` if you must limit access to a scarce resource; and watch out for **pinning**, where a virtual thread blocked inside a `synchronized` block or a native call can't unmount and holds its carrier hostage — the fix is to replace `synchronized` with a `ReentrantLock` on blocking hot paths."

### Vocabulário

| Termo PT | Termo EN |
| --- | --- |
| thread leve / virtual | virtual thread / lightweight thread |
| thread de plataforma | platform thread |
| thread carregadora (carrier) | carrier thread |
| montar / desmontar | mount / unmount |
| pregar (prender ao carrier) | pinning |
| uma thread por requisição | thread-per-request |
| pool de threads | thread pool |
| ligado a I/O / ligado a CPU | I/O-bound / CPU-bound |
| escala vs. velocidade | scale vs. speed (throughput vs. latency) |
| disponibilidade geral | generally available (GA) |
| propagação de contexto | context propagation |

## Veja também

- [[02 - Threads e seu ciclo de vida]]
- [[08 - Executors e thread pools]]
- [[10 - CompletableFuture e composição assíncrona]]
- [[13 - Structured concurrency]]
- [[14 - Scoped values]]
- [[11 - Java Memory Model em profundidade]]
- [[03-Dominios/Java/Concorrência e paralelismo/index|MOC do galho]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[Java Concurrency]]
- [[Java Fundamentals]]
- [[03-Dominios/Java/Dicionário de Java#Virtual thread|virtual thread]]
- [[03-Dominios/Java/Dicionário de Java#Carrier thread|carrier thread]]
- [[03-Dominios/Java/Dicionário de Java#Pinning|pinning]]
- [[03-Dominios/Java/Dicionário de Java#Thread pool|thread pool]]

## Referências

- [JEP 444: Virtual Threads](https://openjdk.org/jeps/444) — proposta que tornou virtual threads GA no Java 21.
- [Virtual Threads — Java Core Libraries (Oracle, Java 21)](https://docs.oracle.com/en/java/javase/21/core/virtual-threads.html) — guia oficial: mount/unmount, carriers, pinning, criação, thread-per-request, ThreadLocal e scoped values.
