---
title: "Atômicos e operações lock-free"
created: 2026-06-03
updated: 2026-06-03
type: concept
progress: backlog
status: seedling
publish: true
fase: adepto
tags:
  - java
  - concorrencia
  - adepto
  - atomics
  - lock-free
aliases:
  - Atomic
  - CAS
  - lock-free
---

# Atômicos e operações lock-free

> [!abstract] TL;DR
> O pacote `java.util.concurrent.atomic` oferece variáveis que podem ser lidas e escritas atomicamente **sem locks**, usando a instrução de hardware **CAS (compare-and-swap)**. `AtomicInteger`, `AtomicLong` e `AtomicReference` são os tipos mais usados; `getAndUpdate` / `updateAndGet` / `accumulateAndGet` permitem transformações arbitrárias em loop CAS. Sob **alta contenção**, `LongAdder` e `DoubleAdder` escalam melhor que `AtomicLong` porque distribuem os incrementos em células (*striping*) e somam sob demanda — mas `sum()` não é um snapshot atômico. `AtomicStampedReference` anexa um inteiro de versão ao valor para contornar o clássico **problema ABA**, onde CAS aceita indevidamente um valor porque ele voltou ao estado original após ser modificado.

## O que é

**Operações atômicas** são operações indivisíveis do ponto de vista de outras threads: ou todo o efeito é visível, ou nenhum é. Em Java, o mecanismo primitivo para isso, abaixo dos `synchronized`/`Lock`, é a instrução de CPU chamada **compare-and-swap (CAS)**: em uma única operação de hardware, o processador lê um valor, compara com um esperado e, somente se forem iguais, substitui pelo novo valor — tudo sem que outra thread possa intervir no meio.

O pacote `java.util.concurrent.atomic` (introduzido no Java 5) expõe esse mecanismo com uma API de alto nível. As classes não usam bloqueio de sistema operacional; por isso chamamos essas estruturas de **lock-free** — threads não se bloqueiam mutuamente, apenas repetem a tentativa até que o CAS tenha sucesso.

A distinção prática em relação a `volatile`:

| Propriedade | `volatile` | `AtomicLong` |
|---|---|---|
| Visibilidade | Sim | Sim |
| Ordenação | Sim | Sim |
| Atomicidade de operações compostas | **Não** | **Sim** |

`volatile int counter; counter++;` envolve três operações separadas (leitura, incremento, escrita) — não é atômico. `AtomicInteger.incrementAndGet()` é uma única operação CAS.

## Por que importa

Contadores, geradores de sequência, flags e referências compartilhadas são onipresentes em código concorrente. Protegê-los com `synchronized` funciona, mas introduz contenção: threads bloqueiam, aguardam o lock ser liberado e sofrem trocas de contexto de sistema operacional. Sob carga alta, isso se torna gargalo mensurável.

Atômicos permitem um trade-off diferente: threads nunca bloqueiam, apenas **repetem a tentativa** (loop CAS) quando há conflito. Para operações de curta duração como incremento de contador, o custo de uma segunda tentativa é ordens de grandeza menor que um context-switch. O resultado prático:

- **Contadores de métricas**: substituir `synchronized int` por `AtomicLong` ou `LongAdder` pode reduzir latência de p99 em aplicações de alto throughput.
- **Geradores de ID sequencial**: CAS garante unicidade sem lock global.
- **Algoritmos lock-free**: estruturas como `ConcurrentLinkedQueue` e partes internas de `ConcurrentHashMap` são construídas sobre CAS.

Em entrevistas sênior, conhecer atômicos demonstra domínio da camada entre `synchronized` e código puramente reativo — e a capacidade de escolher a ferramenta certa para o nível de contenção esperado.

## Como funciona

### `AtomicInteger` / `AtomicLong` / `AtomicReference`

As classes fundamentais do pacote para tipos primitivos e referências de objetos:

```java
AtomicInteger ai = new AtomicInteger(0);

int old = ai.getAndIncrement();   // retorna valor anterior, depois incrementa
int now = ai.incrementAndGet();   // incrementa, depois retorna novo valor
int prev = ai.getAndAdd(5);       // retorna anterior e soma 5

// Leitura / escrita diretas (semântica volatile)
int val = ai.get();
ai.set(42);
ai.lazySet(42);  // sem barreira total — mais rápido, adequado quando não há leituras imediatas

AtomicLong al = new AtomicLong(0L);
al.incrementAndGet();  // idêntico ao AtomicInteger, mas para long

AtomicReference<String> ref = new AtomicReference<>("inicial");
String anterior = ref.getAndSet("novo");  // troca e retorna o anterior
```

`AtomicReference` permite que qualquer referência de objeto seja trocada atomicamente, o que é útil para substituir snapshots imutáveis de estruturas de dados sem lock.

### CAS (compare-and-swap) e `compareAndSet`

`compareAndSet` é a operação central de todo o pacote:

```java
AtomicInteger ai = new AtomicInteger(10);

// Troca 10 → 20 somente se o valor atual for 10
boolean sucesso = ai.compareAndSet(10, 20);  // retorna true
boolean falha   = ai.compareAndSet(10, 30);  // retorna false (valor já é 20)
```

Internamente, `compareAndSet` mapeia para a instrução `CMPXCHG` (x86) ou equivalente em outras arquiteturas — uma única instrução que executa leitura, comparação e escrita de forma atômica no nível de hardware, garantindo que nenhum outro core interrompa a operação no meio.

A semântica de memória é a de `volatile`: a escrita CAS é uma *release* e a leitura CAS é uma *acquire*, garantindo que efeitos anteriores na thread escritora sejam visíveis para threads que leem o novo valor.

**Padrão de loop CAS** para operações arbitrárias:

```java
AtomicLong ref = new AtomicLong(0);

// "Dobra o valor atual atomicamente" — operação que pode falhar e precisar de retry
long prev, updated;
do {
    prev    = ref.get();
    updated = prev * 2;
} while (!ref.compareAndSet(prev, updated));
// Resultado: não determinístico quanto ao número de tentativas sob contenção,
// mas sempre correto — nunca aplica o dobro ao valor errado.
```

Esse padrão é seguro: o loop garante que, se outra thread modificou o valor entre o `get()` e o `compareAndSet()`, a tentativa falha e recomeça com o valor atual.

### `getAndUpdate` / `updateAndGet` / `accumulateAndGet`

Os métodos funcionais encapsulam o loop CAS, tornando o código mais expressivo:

```java
AtomicInteger counter = new AtomicInteger(5);

// updateAndGet: aplica função e retorna novo valor
int novo  = counter.updateAndGet(x -> x * 2);         // 10

// getAndUpdate: aplica função e retorna valor anterior
int antes = counter.getAndUpdate(x -> x + 1);         // 10 (retorna antes de somar)

// accumulateAndGet: combina valor atual com um delta usando função binária
int total = counter.accumulateAndGet(3, Integer::sum); // atual + 3

// Equivalente com AtomicLong
AtomicLong al = new AtomicLong(100L);
long resultado = al.updateAndGet(v -> v > 0 ? v - 1 : 0);  // decremento com chão em 0
```

A função passada deve ser **sem efeitos colaterais** (*side-effect-free*) porque pode ser re-executada múltiplas vezes se o CAS falhar sob contenção. Não use lambdas que façam I/O, modifiquem estado externo ou dependam de ordem de execução.

### `LongAdder` / `DoubleAdder` (striping sob alta contenção)

`LongAdder` e `DoubleAdder`, introduzidos no Java 8, resolvem um problema específico: quando muitas threads incrementam simultaneamente um único `AtomicLong`, todas competem pelo mesmo valor, aumentando as falhas de CAS e degradando o throughput.

A solução é **striping**: internamente, `LongAdder` mantém uma célula base e um array de células adicionais. Sob contenção, cada thread tende a atualizar sua própria célula; `sum()` percorre todas as células e soma:

```java
LongAdder contador = new LongAdder();

// Threads incrementando em paralelo — cada uma provavelmente acessa célula diferente
contador.increment();          // equivale a add(1)
contador.decrement();          // equivale a add(-1)
contador.add(5L);

long total = contador.sum();   // soma todas as células internas
// ATENÇÃO: sum() não é um snapshot atômico — veja Armadilhas

contador.reset();              // zera todas as células — RISCO: apenas em quiescência
long totalEReset = contador.sumThenReset();  // sum + reset — também racy
```

**Quando usar `LongAdder` vs `AtomicLong`:**

| Cenário | Recomendação |
|---|---|
| Contador de métricas, muitas threads escrevendo, leituras ocasionais | `LongAdder` |
| Gerador de sequência único (cada valor importa) | `AtomicLong` |
| Baixa contenção (poucas threads) | Indiferente; `AtomicLong` é mais simples |
| Precisa de `compareAndSet` | Somente `AtomicLong` — `LongAdder` não expõe CAS |

`DoubleAdder` é o equivalente para `double`, com as mesmas garantias (e as mesmas ressalvas de `sum()`).

### `AtomicStampedReference` e o problema ABA

O **problema ABA** ocorre quando uma thread lê o valor `A`, é preemptada, e outra thread modifica o valor para `B` e depois volta para `A`. Quando a primeira thread executa o CAS, ele enxerga `A` e tem sucesso — mas o valor passou por uma modificação intermediária que pode deixar o sistema em estado inválido.

Exemplo clássico em estruturas de dados:

```java
// Thread 1: lê nó A no topo da pilha lock-free
// Thread 2: remove A, insere B, remove B, reusa o objeto A e o recoloca
// Thread 1: CAS de A → C tem sucesso, mas o estado da pilha está errado
```

`AtomicStampedReference` resolve anexando um **inteiro de versão (stamp)** ao valor. O CAS só tem sucesso se tanto o valor quanto o stamp conferem:

```java
// Estado inicial: referência "nó-A", stamp 0
AtomicStampedReference<String> asr = new AtomicStampedReference<>("nó-A", 0);

// Leitura segura: pegar referência e stamp juntos
int[] stampHolder = new int[1];
String atual = asr.get(stampHolder);  // atual = "nó-A", stampHolder[0] = 0

// CAS que requer tanto referência quanto stamp corretos
boolean ok = asr.compareAndSet(
    "nó-A", "nó-C",    // referência esperada → nova
    0,      1           // stamp esperado → novo
);
// Se outra thread já incrementou o stamp (mesmo que voltou para "nó-A"),
// este CAS falha — o ABA é detectado.
```

`AtomicMarkableReference` é uma variação que usa um `boolean` em vez de um inteiro, adequada quando só é preciso distinguir "original" de "modificado uma vez".

## Na prática

### Contador lock-free com `AtomicLong`

O caso mais direto: substituir um campo `int/long` sincronizado por `AtomicLong`:

```java
public class PageViewCounter {

    private final AtomicLong views = new AtomicLong(0L);

    // Chamado por múltiplas threads ao mesmo tempo
    public void record() {
        views.incrementAndGet();
    }

    public long total() {
        return views.get();
    }

    // Snapshot periódico para métricas — zera e retorna
    public long drainAndReset() {
        return views.getAndSet(0L);
    }
}
```

`drainAndReset` é atômico: mesmo que outra thread incremente entre `getAndSet` e a próxima chamada, nenhum incremento é perdido — apenas pode cair no próximo período de coleta.

### Gerador de sequência com loop CAS

Quando a semântica exige controle sobre o valor gerado (por exemplo, garantir que IDs nunca regridam, mesmo sob concorrência):

```java
public class StrictSequenceGenerator {

    private final AtomicLong current = new AtomicLong(0L);

    /**
     * Retorna o próximo valor maior que o atual.
     * Garante monotonia estrita mesmo com múltiplas threads.
     * Não determinístico quanto ao número de tentativas — pode fazer retry sob contenção.
     */
    public long next(long minimum) {
        long prev, next;
        do {
            prev = current.get();
            next = Math.max(prev + 1, minimum);
        } while (!current.compareAndSet(prev, next));
        return next;
    }
}
```

O loop não tem limite fixo de tentativas — sob contenção extrema pode iterar mais vezes. Para casos onde isso é inaceitável, considere um lock com timeout (ver [[05 - Locks explícitos]]).

### Métrica de alto volume com `LongAdder`

Em sistemas de telemetria onde dezenas de threads reportam eventos por segundo:

```java
public class RequestMetrics {

    private final LongAdder totalRequests  = new LongAdder();
    private final LongAdder totalErrors    = new LongAdder();
    private final LongAdder totalLatencyMs = new LongAdder();

    public void record(long latencyMs, boolean error) {
        totalRequests.increment();
        totalLatencyMs.add(latencyMs);
        if (error) totalErrors.increment();
    }

    // Chamado periodicamente pelo coletor de métricas — não durante pico de escrita
    public Snapshot snapshot() {
        return new Snapshot(
            totalRequests.sum(),
            totalErrors.sum(),
            totalLatencyMs.sum()
        );
        // Nota: os três sum() não são lidos atomicamente como grupo.
        // Para snapshots totalmente consistentes, prefira LongAccumulator com lock externo.
    }
}
```

`LongAdder` aqui escala sob carga porque cada thread que chega em colisão recebe uma célula diferente — o gargalo de CAS é distribuído horizontalmente.

## Armadilhas

### (1) Loop CAS sem progressão garantida sob contenção extrema

**O problema:** `updateAndGet` e qualquer loop CAS manual podem repetir indefinidamente quando muitas threads competem pelo mesmo valor. Tecnicamente não é deadlock (threads não se bloqueiam), mas na prática o comportamento se assemelha a *livelock*: threads consomem CPU sem progredir.

```java
// RUIM para contenção muito alta: todas as threads repetem o CAS em loop
AtomicLong shared = new AtomicLong(0L);

// 1000 threads fazendo isso ao mesmo tempo → CAS falha constantemente
long resultado = shared.updateAndGet(x -> compute(x));
```

```java
// FIX 1: se só precisa de contagem, use LongAdder — sem CAS conflitante
LongAdder adder = new LongAdder();
adder.add(delta);  // nenhum retry; células absorvem a contenção

// FIX 2: se precisa de CAS por semântica, introduza backoff com jitter
long prev, next;
int retries = 0;
do {
    prev = shared.get();
    next = computeNext(prev);
    if (retries++ > 10) {
        LockSupport.parkNanos(ThreadLocalRandom.current().nextLong(1_000, 10_000));
    }
} while (!shared.compareAndSet(prev, next));
```

A escolha entre atômicos e `ReentrantLock` depende do perfil de contenção: baixa-média contenção favorece atômicos; alta contenção sustentada pode favorecer um lock com fila de espera.

### (2) Problema ABA com `AtomicReference` simples

**O problema:** usar `AtomicReference.compareAndSet` em estruturas de dados com reuso de objetos (como pools de nós em pilhas lock-free) pode aceitar um CAS indevidamente porque o valor voltou para a referência original.

```java
// RUIM: AtomicReference não detecta ciclos A→B→A
AtomicReference<Node> top = new AtomicReference<>(nodeA);

// Thread 2, enquanto Thread 1 estava preemptada:
// top: A → B → A (com nodeA reusado do pool)

// Thread 1 executa o CAS com expectedRef = nodeA → SUCESSO indevido
// Resultado: estrutura da pilha corrompida, nó B "perdido"
top.compareAndSet(nodeA, nodeC);  // passa, mas não deveria
```

```java
// FIX: AtomicStampedReference com versão incremental
AtomicStampedReference<Node> top = new AtomicStampedReference<>(nodeA, 0);

int[] stamp = new int[1];
Node current = top.get(stamp);

// CAS agora exige que o stamp também corresponda
top.compareAndSet(current, nodeC, stamp[0], stamp[0] + 1);
// Se Thread 2 incrementou o stamp (mesmo que restaurou a referência),
// este CAS falha corretamente.
```

Na prática, algoritmos lock-free corretos para pilhas e filas (como os de Maged Michael e Michael Scott) sempre incorporam proteção ABA — ou via stamp, ou via garbage collection (em Java, GC impede reuso exato do mesmo endereço de memória na maioria dos casos, reduzindo o risco, mas não eliminando-o em sistemas com pool de objetos).

### (3) Assumir que `LongAdder.sum()` é consistente durante updates

**O problema:** `sum()` percorre células internas somando-as uma por uma. Durante essa travessia, outras threads podem estar modificando células já visitadas ou ainda não visitadas. O Javadoc do Oracle é explícito: o valor retornado **não é um snapshot atômico**; atualizações concorrentes em andamento podem não ser refletidas.

```java
// RUIM: assumir que sum() captura estado exato de um instante
LongAdder requests = new LongAdder();

// Thread de monitoramento:
long total = requests.sum();  // pode estar "desatualizado" por alguns nanos
log.info("Requests exatos agora: {}", total);  // premissa falsa
```

```java
// FIX 1: aceite a semântica aproximada — para métricas de observabilidade é suficiente
// "~N requests no último período" é tão útil quanto "exatamente N"

// FIX 2: se precisar de consistência exata entre múltiplas variáveis,
// use um lock externo para o snapshot:
synchronized (metricsLock) {
    long r = requests.sum();
    long e = errors.sum();
    long l = latencySum.sum();
    return new Snapshot(r, e, l);
}

// FIX 3: zerar e ler são operações separadas — reset() é racy se há threads ativas
// NUNCA:
long snapshot = counter.sum();
counter.reset();  // threads podem incrementar entre sum() e reset(), perdendo eventos

// USE sumThenReset() com cautela — mesmo ela não é atômica com o resto do sistema,
// mas pelo menos reduz a janela de inconsistência entre soma e zera
```

## Em entrevista

### Frase pronta (inglês)

> "Atomic classes in `java.util.concurrent.atomic` provide lock-free thread safety by leveraging hardware CAS — compare-and-swap — instructions, which atomically read, compare, and conditionally write a value in a single CPU operation, without acquiring an OS-level lock." "For simple counters and references, `AtomicLong` and `AtomicReference` are the go-to tools; `compareAndSet` is the primitive, and `updateAndGet` / `accumulateAndGet` wrap the CAS loop for you — but the function you pass must be side-effect-free because it may run multiple times under contention." "When thread density is high and most operations are plain increments — think metrics collection or hit counters — `LongAdder` outperforms `AtomicLong` because it uses striping: each thread updates its own cell, and `sum()` aggregates them on demand; the trade-off is that `sum()` is not an atomic snapshot, which is fine for approximate instrumentation but wrong for sequence generators or anything requiring strict consistency."

### Vocabulário

| Termo PT | Termo EN |
|---|---|
| operação atômica | atomic operation |
| comparação e troca | compare-and-swap (CAS) |
| sem bloqueio | lock-free |
| problema ABA | ABA problem |
| referência estampada | stamped reference |
| distribuição de células | cell striping |
| snapshot atômico | atomic snapshot |
| laço de retry | CAS retry loop |
| memória volátil | volatile memory semantics |
| contenção de threads | thread contention |
| gerador de sequência | sequence generator |
| versão de carimbo | version stamp |

## Veja também

- [[05 - Locks explícitos]]
- [[07 - Concurrent collections]]
- [[11 - Java Memory Model em profundidade]]
- [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|MOC do galho]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[Java Concurrency]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#Atomic (variável atômica)|atomic]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#CAS (compare-and-swap)|CAS]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#ABA problem|ABA problem]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#Lock-free|lock-free]]

## Referências

- [java.util.concurrent.atomic — Package Summary, Java 21 (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/atomic/package-summary.html)
- [AtomicInteger — Java 21 API (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/atomic/AtomicInteger.html)
- [AtomicLong — Java 21 API (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/atomic/AtomicLong.html)
- [LongAdder — Java 21 API (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/atomic/LongAdder.html)
- [AtomicStampedReference — Java 21 API (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/atomic/AtomicStampedReference.html)
- Brian Goetz et al. *Java Concurrency in Practice*. Addison-Wesley, 2006. Cap. 15 — "Atomic Variables and Nonblocking Synchronization".
