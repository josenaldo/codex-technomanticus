---
title: "Parallel streams e fork/join"
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
  - parallel-streams
  - fork-join
aliases:
  - Parallel streams
  - ForkJoinPool
  - fork/join
---

# Parallel streams e fork/join

> [!abstract] TL;DR
> **Fork/join** é um framework de divisão-e-conquista: o `ForkJoinPool` divide um problema em sub-tarefas (`fork`), executa cada parte em threads separadas e combina os resultados (`join`). A estratégia central é o **work-stealing**: cada worker tem sua própria deque de tarefas e, quando fica ocioso, "rouba" o trabalho da cauda da deque de outro worker. **Parallel streams** são a fachada de alto nível que usa o `ForkJoinPool.commonPool()` internamente — basta chamar `.parallel()` em qualquer stream. O ganho real só aparece em problemas **CPU-bound com dados grandes e fonte bem particionável** (ex.: `ArrayList`, arrays); em I/O, datasets pequenos ou fontes mal-dividíveis (ex.: `LinkedList`), o overhead supera o benefício. O common pool é **compartilhado** com `CompletableFuture` e com outros parallel streams — bloquear I/O nele impacta todo o processo.

## O que é

O framework **fork/join** foi introduzido no Java 7 (pacote `java.util.concurrent`) e é composto por:

- **`ForkJoinPool`** — um `ExecutorService` especializado que gerencia um conjunto de worker threads usando work-stealing. É a peça de infraestrutura.
- **`ForkJoinTask<V>`** — a unidade de trabalho abstrata. As duas subclasses concretas úteis são `RecursiveTask<V>` (retorna valor) e `RecursiveAction` (sem retorno, efeito colateral).
- **Common pool** — uma instância estática compartilhada (`ForkJoinPool.commonPool()`) usada automaticamente por parallel streams, `CompletableFuture` e qualquer `ForkJoinTask` submetida sem pool explícito.

**Parallel streams** são a abstração de alto nível sobre esse mesmo mecanismo. A transformação `.parallel()` ou `parallelStream()` instrui a Stream API a particionar a fonte usando um **spliterator** e delegar as operações ao common pool:

```java
// Stream sequencial — um só thread, na ordem de inserção
long somaSeq = lista.stream()
    .mapToLong(Item::getValor)
    .sum();

// Parallel stream — o common pool divide o spliterator e processa em paralelo
long somaPar = lista.parallelStream()
    .mapToLong(Item::getValor)
    .sum();
```

Esta nota cobre a camada de infraestrutura (fork/join) e a camada de alto nível (parallel streams). O pipeline de operações de stream em si — `map`, `filter`, `collect`, `reduce`, spliterators — é do Galho 2; consulte [[03-Dominios/Tecnologia/Java/Collections e Streams/05 - Introdução à Stream API|Stream API]] e [[03-Dominios/Tecnologia/Java/Collections e Streams/07 - Operações de Stream — intermediárias e terminais|Operações de Stream]] para essa base.

## Por que importa

### Quando o paralelismo ganha

O paralelismo via fork/join é uma aposta que vale a pena quando **todos** os fatores a seguir estão presentes:

| Fator | Condição favorável |
|-------|--------------------|
| **Natureza do trabalho** | CPU-bound (cálculo puro, sem I/O ou bloqueios) |
| **Tamanho do dataset** | Grande o suficiente para amortizar overhead de split+merge |
| **Fonte** | Spliterator balanceado: `ArrayList`, arrays, `IntStream.range` |
| **Ordering** | Sem dependência de ordem de encontro (`findFirst` em paralelo sofre) |
| **Lambdas** | Sem estado mutável compartilhado, sem side effects |

Exemplo canônico: somar um array de `long[]` com 10 milhões de elementos — o `RecursiveTask` dividindo recursivamente em blocos de ~1 000 pode explorar todos os cores disponíveis com overhead desprezível.

### Quando o paralelismo perde (comparação justa)

| Cenário | Por que perde |
|---------|---------------|
| **Dataset pequeno** (< ~10 000 elementos, dependendo da operação) | Overhead de split, fork e merge supera o ganho. Sequential é mais rápido. |
| **I/O-bound** (HTTP, banco, arquivo) | Threads do common pool bloqueiam esperando I/O; throughput colapsa. Use `CompletableFuture` + executor dedicado. |
| **Fonte mal-particionável** (`LinkedList`, `Iterator`, streams de arquivos) | Spliterator não consegue dividir em tamanhos equilibrados; um worker processa tudo enquanto outros ficam ociosos. |
| **Lambdas com estado / autoboxing pesado** | Sincronização de estado ou boxing/unboxing excessivo anulam o ganho. |
| **Ambiente com common pool compartilhado** (servidor de aplicação, container) | Outro componente pode estar usando o pool; saturar o common pool afeta toda a JVM. |
| **Operações com ordering forte** (`forEachOrdered`, `findFirst`) | Paralelo precisa reordenar ou sincronizar — pode ser mais lento que sequencial. |

> [!tip] Regra prática
> Meça antes de paralelizar. Em benchmarks com JMH, problemas com menos de ~100 µs de trabalho por elemento raramente se beneficiam de parallelStream em produção.

## Como funciona

### `ForkJoinPool` e work-stealing

O `ForkJoinPool` mantém um array de worker threads. Cada worker possui uma **deque** (double-ended queue) própria de tarefas. O fluxo normal é:

1. O worker empilha novas sub-tarefas no **topo** da sua deque (LIFO — melhor localidade de cache).
2. Quando o worker fica ocioso, ele tenta **roubar** uma tarefa da **cauda** (FIFO) da deque de outro worker.
3. Essa assimetria (topo vs cauda) minimiza contenção: o worker processa pelo topo enquanto o ladrão retira pela cauda.

```
Worker 0 deque:  [ T1, T2, T3 ] ← topo (worker processa daqui)
                              ↑
Worker 1 (ocioso) rouba T1   ─┘  ← cauda (ladrão pega daqui)
```

O resultado é **balanceamento de carga automático** sem um coordenador central. Se um worker concluir rápido e outro tiver fila grande, o trabalho migra organicamente.

**Criação:**

```java
// Pool com parallelism = número de CPUs disponíveis (padrão)
ForkJoinPool poolPadrao = new ForkJoinPool();

// Pool com paralelismo explícito (e.g., apenas 4 workers)
ForkJoinPool pool4 = new ForkJoinPool(4);

// Common pool — instância estática compartilhada
ForkJoinPool common = ForkJoinPool.commonPool();
int nivel = ForkJoinPool.commonPool().getParallelism();
// típico: Runtime.getRuntime().availableProcessors() - 1
```

---

### Common pool (compartilhado com parallel streams e CompletableFuture)

O common pool é a instância padrão usada quando nenhum pool explícito é fornecido. Três mecanismos distintos o utilizam de forma transparente:

```
parallel stream   ──┐
                    ├──▶  ForkJoinPool.commonPool()  ──▶  worker threads
CompletableFuture ──┘
(sem executor)    ──┘
```

**Características importantes:**
- Threads são criadas *on demand* e recuperadas lentamente em períodos ociosos.
- Não pode ser desligado via `shutdown()` — pertence à JVM.
- O paralelismo padrão é `availableProcessors() - 1` (reserva um core para o thread chamador).
- Configurável via propriedade de sistema antes do primeiro uso:

```bash
# Forçar common pool com 2 workers
-Djava.util.concurrent.ForkJoinPool.common.parallelism=2
```

> [!warning] Contenção no common pool
> Parallel streams de código diferente rodando ao mesmo tempo **competem pelo mesmo pool**. Em servidores web (ex.: Tomcat, Netty), o common pool pode estar parcialmente ocupado por outras requisições. Pool dedicado via `pool.submit(() -> stream.parallel()...)` é a solução quando isolamento importa.

---

### `RecursiveTask`/`RecursiveAction` (fork/join/compute)

O padrão de uso é sempre o mesmo: implementar `compute()` com uma **condição de base** (problema pequeno o suficiente para resolver diretamente) e uma **divisão recursiva** (fork + compute + join):

```java
class SomaTask extends RecursiveTask<Long> {
    private static final int LIMIAR = 1_000; // resolver diretamente abaixo disso
    private final long[] dados;
    private final int inicio, fim;

    SomaTask(long[] dados, int inicio, int fim) {
        this.dados = dados;
        this.inicio = inicio;
        this.fim = fim;
    }

    @Override
    protected Long compute() {
        int tamanho = fim - inicio;

        // Condição de base — resolve diretamente
        if (tamanho <= LIMIAR) {
            long soma = 0;
            for (int i = inicio; i < fim; i++) soma += dados[i];
            return soma;
        }

        // Divide ao meio
        int meio = inicio + tamanho / 2;
        SomaTask esquerda = new SomaTask(dados, inicio, meio);
        SomaTask direita  = new SomaTask(dados, meio,  fim);

        // fork() agenda a tarefa esquerda de forma assíncrona
        esquerda.fork();

        // compute() executa a direita NO MESMO THREAD (evita overhead extra de fork)
        long resultadoDireita = direita.compute();

        // join() bloqueia até a esquerda terminar e retorna o resultado
        long resultadoEsquerda = esquerda.join();

        return resultadoEsquerda + resultadoDireita;
    }
}
```

> [!note] Padrão recomendado: fork um lado, compute o outro
> `esquerda.fork(); direita.compute(); esquerda.join()` é mais eficiente do que `esquerda.fork(); direita.fork(); esquerda.join(); direita.join()`. O segundo cria duas tarefas agendadas; o primeiro reutiliza o thread atual para `direita.compute()`, economizando um hop de agendamento.

**`RecursiveAction`** segue o mesmo padrão, mas `compute()` retorna `void`. Útil para operações in-place (ex.: ordenar segmento de array, preencher estrutura).

---

### Parallel streams (`.parallel()`) e o spliterator

Quando `.parallelStream()` (ou `.parallel()` num stream existente) é chamado, a Stream API:

1. Usa o **spliterator** da fonte para dividir os dados em partes (`trySplit()`).
2. Cada parte vira uma sub-tarefa submetida ao common pool (internamente um `ForkJoinTask`).
3. As operações intermediárias (map, filter, etc.) são aplicadas em paralelo em cada partição.
4. As operações terminais (reduce, collect, sum) combinam os resultados parciais.

```java
// Soma paralela com IntStream — fonte primitiva, sem boxing
long soma = IntStream.range(0, 10_000_000)
    .parallel()
    .filter(n -> n % 2 == 0)
    .asLongStream()
    .sum();

// Collect thread-safe — o collector gerencia a combinação parcial
List<String> filtrados = nomes.parallelStream()
    .filter(s -> s.startsWith("A"))
    .collect(Collectors.toList());  // Collectors.toList() é thread-safe internamente

// Verificar se o stream é paralelo
boolean eParalelo = lista.parallelStream().isParallel(); // true
```

**Spliterator e particionabilidade:** fontes baseadas em `ArrayList` e arrays implementam `SIZED | SUBSIZED` — o spliterator sabe o tamanho e pode dividir ao meio em O(1). Já `LinkedList` só pode atravessar sequencialmente; o spliterator parte mal e a divisão é desequilibrada.

## Na prática

### Soma paralela com `RecursiveTask`

```java
import java.util.concurrent.ForkJoinPool;
import java.util.concurrent.RecursiveTask;

public class SomaParalela {

    static class SomaTask extends RecursiveTask<Long> {
        private static final int LIMIAR = 2_000;
        private final int[] dados;
        private final int inicio, fim;

        SomaTask(int[] dados, int inicio, int fim) {
            this.dados = dados;
            this.inicio = inicio;
            this.fim = fim;
        }

        @Override
        protected Long compute() {
            if (fim - inicio <= LIMIAR) {
                long soma = 0;
                for (int i = inicio; i < fim; i++) soma += dados[i];
                return soma;
            }
            int meio = inicio + (fim - inicio) / 2;
            SomaTask esquerda = new SomaTask(dados, inicio, meio);
            SomaTask direita  = new SomaTask(dados, meio,  fim);
            esquerda.fork();
            long r = direita.compute();
            return r + esquerda.join();
        }
    }

    public static void main(String[] args) {
        int N = 10_000_000;
        int[] dados = new int[N];
        for (int i = 0; i < N; i++) dados[i] = i + 1;

        ForkJoinPool pool = ForkJoinPool.commonPool();

        // Fork/join explícito
        long somaFJ = pool.invoke(new SomaTask(dados, 0, N));

        // Parallel stream equivalente — mesma resposta, muito menos código
        long somaPar = java.util.Arrays.stream(dados).parallel().asLongStream().sum();

        // Sequential para comparação
        long somaSeq = java.util.Arrays.stream(dados).asLongStream().sum();

        System.out.printf("Fork/join: %d%n",    somaFJ);
        System.out.printf("Parallel:  %d%n",    somaPar);
        System.out.printf("Sequential: %d%n",   somaSeq);
        // Todos retornam 50000005000000
    }
}
```

### Medindo parallel vs sequential (CPU-bound)

Para avaliar se o paralelismo vale, use JMH ou ao menos `System.nanoTime()` em warm-up adequado. Abaixo, uma estrutura básica de comparação sem dependências externas:

```java
// Estrutura simplificada — NÃO substitui JMH em produção
int[] dados = new int[10_000_000]; // preencher com valores relevantes

long t0 = System.nanoTime();
long somaSeq = java.util.Arrays.stream(dados).asLongStream().sum();
long dtSeq = System.nanoTime() - t0;

long t1 = System.nanoTime();
long somaPar = java.util.Arrays.stream(dados).parallel().asLongStream().sum();
long dtPar = System.nanoTime() - t1;

System.out.printf("Sequential: %.1f ms%n", dtSeq / 1e6);
System.out.printf("Parallel:   %.1f ms%n", dtPar / 1e6);
System.out.printf("Speedup:    %.1fx%n",   (double) dtSeq / dtPar);
```

> [!warning] Microbenchmark
> `System.nanoTime()` sem JVM warm-up (JIT, caches) produz resultados instáveis. Em avaliações sérias, use [JMH](https://github.com/openjdk/jmh) com pelo menos 5 iterações de warm-up e 5 de medição. Os resultados acima são apenas orientativos.

### Pool customizado para isolamento

```java
// Isola o parallel stream do common pool — útil em servidores
ForkJoinPool poolDedicado = new ForkJoinPool(4);

List<Resultado> resultados = poolDedicado.submit(() ->
    minhaLista.parallelStream()
        .map(item -> processarCpuBound(item))
        .collect(Collectors.toList())
).get();

poolDedicado.shutdown();
```

## Armadilhas

### (1) Estado mutável compartilhado em lambda de parallel stream

**O problema:** parallel streams executam lambdas em múltiplos threads simultaneamente. Acumular resultados em uma estrutura não-thread-safe causa corrida de dados, resultados corrompidos ou `ConcurrentModificationException` — sem nenhuma exceção clara sobre a causa.

```java
// ERRADO — ArrayList não é thread-safe; resultado é não-determinístico
List<String> resultado = new ArrayList<>();
nomes.parallelStream()
    .filter(s -> s.length() > 3)
    .forEach(resultado::add);  // várias threads chamam add() simultaneamente
// resultado pode ter elementos faltando, duplicados ou lançar exceção

// CORRETO — collect() gerencia internamente a combinação thread-safe
List<String> resultado = nomes.parallelStream()
    .filter(s -> s.length() > 3)
    .collect(Collectors.toList());

// CORRETO — toList() (Java 16+) também é seguro
List<String> resultado = nomes.parallelStream()
    .filter(s -> s.length() > 3)
    .toList();
```

**Regra:** nunca use `forEach` para acumular em coleção mutável num parallel stream. Prefira `collect`, `reduce` ou operações terminais que garantam combinação segura.

---

### (2) Bloquear I/O no common pool

**O problema:** as threads do common pool são uma **pool de threads de plataforma finita** (por padrão `nCPUs - 1` threads). Se uma lambda de parallel stream faz chamada de rede, leitura de disco ou acesso a banco de dados, as threads ficam bloqueadas em I/O. Com threads suficientes bloqueadas, **todos** os parallel streams e `CompletableFuture` do processo sofrem degradação — incluindo os que nada têm a ver com o I/O problemático.

```java
// ERRADO — bloqueia threads do common pool em I/O de rede
List<Produto> produtos = ids.parallelStream()
    .map(id -> httpClient.buscar(id))   // operação bloqueante de rede
    .collect(Collectors.toList());
// common pool saturado → outros parallel streams da JVM param de progredir

// CORRETO — use CompletableFuture com executor dedicado para I/O
ExecutorService ioExecutor = Executors.newVirtualThreadPerTaskExecutor(); // Java 21+
List<CompletableFuture<Produto>> futuros = ids.stream()
    .map(id -> CompletableFuture.supplyAsync(() -> httpClient.buscar(id), ioExecutor))
    .toList();
List<Produto> produtos = futuros.stream()
    .map(CompletableFuture::join)
    .toList();
ioExecutor.shutdown();
```

Veja [[10 - CompletableFuture e composição assíncrona]] para o padrão completo de I/O assíncrono.

---

### (3) `.parallel()` em dataset pequeno (overhead > ganho)

**O problema:** paralelizar tem custo: split do spliterator, agendamento de tarefas no pool, possível context switch de threads e merge dos resultados parciais. Para datasets pequenos, esse overhead é maior do que o tempo economizado.

```java
// ERRADO — paralelizar lista de 10 elementos é mais lento que sequential
List<String> poucosDados = List.of("a", "b", "c", "d", "e", "f", "g", "h", "i", "j");
String resultado = poucosDados.parallelStream()
    .filter(s -> !s.equals("e"))
    .collect(Collectors.joining(", "));
// overhead de fork/join > tempo de filtrar 10 strings

// CORRETO — sequencial é sempre mais rápido para poucos elementos
String resultado = poucosDados.stream()
    .filter(s -> !s.equals("e"))
    .collect(Collectors.joining(", "));
```

Não existe um limiar universal — depende do custo da operação por elemento e do hardware. Como orientação geral: se cada elemento leva menos de ~10 µs e o dataset tem menos de ~10 000 itens, sequencial tende a ser mais rápido. Meça com JMH.

---

### (4) Pool dedicado não fecha (resource leak)

**O problema:** `ForkJoinPool` criado manualmente não é fechado automaticamente. Threads de worker ficam vivas e consomem recursos até o GC finalizar o pool (não-determinístico).

```java
// ERRADO — pool nunca fechado
ForkJoinPool pool = new ForkJoinPool(4);
pool.invoke(minhaTask);
// pool.shutdown() faltando → threads ficam vivas

// CORRETO — usar try-with-resources (Java 19+, ForkJoinPool implementa AutoCloseable)
try (ForkJoinPool pool = new ForkJoinPool(4)) {
    Long resultado = pool.invoke(new SomaTask(dados, 0, dados.length));
    System.out.println("Resultado: " + resultado);
} // pool.close() chamado automaticamente
```

## Em entrevista

### Frase pronta (inglês)

> "The fork/join framework in Java is designed for divide-and-conquer parallelism: a `ForkJoinPool` manages worker threads that use work-stealing — each worker maintains its own deque and steals tasks from the tail of other workers' deques when it runs out of work, which provides automatic load balancing without a central coordinator."
>
> "Parallel streams are the high-level abstraction built on top of this: calling `.parallel()` instructs the stream pipeline to split the source using its spliterator and distribute the work across the common pool, which is a shared static `ForkJoinPool` instance also used by `CompletableFuture` async operations — so blocking I/O inside a parallel stream lambda can starve the entire common pool and degrade unrelated parts of the application."
>
> "The key trade-off is that parallelism only pays off for CPU-bound work on large, easily splittable sources like arrays or `ArrayList`; for I/O-bound tasks, small datasets, poorly splittable sources like `LinkedList`, or lambdas with shared mutable state, sequential execution or `CompletableFuture` with a dedicated executor is almost always the better choice."

### Vocabulário

| Termo PT | Termo EN |
|----------|----------|
| divisão e conquista | divide and conquer |
| roubo de trabalho | work-stealing |
| pool comum (estático) | common pool |
| tarefa recursiva com resultado | `RecursiveTask` |
| tarefa recursiva sem resultado | `RecursiveAction` |
| spliterador / divisor de fonte | spliterator |
| paralelismo de dados | data parallelism |
| saturar o pool | saturate / starve the pool |
| sobrecarga de agendamento | scheduling overhead |
| operação terminal combinável | combinable terminal operation |
| fonte bem-particionável | well-splittable source |
| nível de paralelismo | parallelism level |

## Veja também

- [[08 - Executors e thread pools]]
- [[10 - CompletableFuture e composição assíncrona]]
- [[16 - Padrões e diagnóstico de concorrência]]
- [[03-Dominios/Tecnologia/Java/Collections e Streams/07 - Operações de Stream — intermediárias e terminais|Operações de Stream]]
- [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|MOC do galho]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[Java Concurrency]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#Fork/join|fork/join]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#Work-stealing|work-stealing]]

## Referências

- [ForkJoinPool — Java SE 21 API Docs (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/ForkJoinPool.html)
- [RecursiveTask — Java SE 21 API Docs (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/RecursiveTask.html)
- [RecursiveAction — Java SE 21 API Docs (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/RecursiveAction.html)
- [Fork/Join — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/essential/concurrency/forkjoin.html)
- [Parallelism — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/collections/streams/parallelism.html)
