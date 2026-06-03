---
title: "Concurrent collections"
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
  - collections
  - concurrent-collections
aliases:
  - ConcurrentHashMap
  - BlockingQueue
  - Concurrent collections
---

# Concurrent collections

> [!abstract] TL;DR
> **Concurrent collections** são estruturas de dados do pacote `java.util.concurrent` projetadas para uso seguro em ambientes multi-thread sem exigir lock externo. `ConcurrentHashMap` substitui `HashMap` com locking por bucket e operações atômicas compostas (`computeIfAbsent`, `merge`). `CopyOnWriteArrayList` e `CopyOnWriteArraySet` são ideais para listas lidas muito mais que escritas: cada escrita produz uma cópia do array. `BlockingQueue` (com implementações como `ArrayBlockingQueue` e `LinkedBlockingQueue`) é a base do padrão produtor-consumidor, bloqueando o produtor quando a fila está cheia e o consumidor quando está vazia. Para filas não-bloqueantes, `ConcurrentLinkedQueue` usa CAS. Para mapas e sets ordenados e thread-safe, `ConcurrentSkipListMap`/`Set` são a alternativa a `TreeMap`/`TreeSet`. A escolha correta depende do perfil de acesso: read-heavy vs write-heavy, bloqueante vs não-bloqueante, ordenado vs não-ordenado.

## O que é

**Concurrent collections** são implementações de coleções do Java prontas para uso concorrente. Elas fazem parte do pacote `java.util.concurrent` (introduzido no Java 5) e foram projetadas com granularidade de locking muito mais fina — ou sem locking algum — em comparação com as alternativas mais antigas baseadas em `Collections.synchronizedXxx(...)`.

O framework [[Java Fundamentals]] define as interfaces `Map`, `List`, `Queue` e `Set`. As concurrent collections implementam essas mesmas interfaces, de modo que substituem as versões não thread-safe sem alterar o código cliente.

> [!note] Escopo desta nota
> Esta nota cobre as concurrent collections do `java.util.concurrent`. Para os tipos atômicos (`AtomicInteger`, `LongAdder`), veja [[06 - Atômicos e operações lock-free]]. Para `ExecutorService` e filas de tasks, veja [[08 - Executors e thread pools]]. Para `CountDownLatch`, `Semaphore` e similares, veja [[09 - Sincronizadores]].

## Por que importa

`HashMap`, `ArrayList` e `HashSet` não são thread-safe. Acesso concorrente sem sincronização produz data races: resultados incorretos silenciosos, `ConcurrentModificationException` durante iteração ou, no pior caso (documentado antes do Java 8), um loop infinito por corrupção da estrutura de hash.

A alternativa histórica — `Collections.synchronizedMap(new HashMap<>())` — resolve a thread-safety, mas com custo alto: **um único lock global** para toda a operação. Em cenários com muitas threads lendo ou escrevendo, esse lock vira gargalo imediato.

As concurrent collections resolvem isso com:

- **Locking por bucket** (`ConcurrentHashMap`) — múltiplas threads podem escrever em buckets diferentes simultaneamente.
- **Separação de locks de leitura e escrita** — leituras sem lock, escritas com lock mínimo.
- **Algoritmos lock-free baseados em CAS** (`ConcurrentLinkedQueue`) — sem locks, sem espera por monitor.
- **Operações compostas atômicas** — elimina a necessidade de lock externo para padrões comuns como "get-or-compute".

## Como funciona

### `ConcurrentHashMap`

`ConcurrentHashMap` é um mapa thread-safe com alta concorrência para leituras e escritas. Reads são completamente sem lock. Escritas aplicam lock apenas no bucket afetado, não na estrutura inteira.

**Operações atômicas compostas** — essas são as operações mais importantes na prática:

```java
ConcurrentHashMap<String, List<String>> cache = new ConcurrentHashMap<>();

// computeIfAbsent: atômico. Se a chave ausente, computa e insere.
// A função é invocada exatamente uma vez se a chave está ausente.
List<String> list = cache.computeIfAbsent("grupo-a", k -> new ArrayList<>());

// compute: atômico. Recalcula o valor (pode ser null → cria, null → remove).
cache.compute("contador", (k, v) -> v == null ? 1 : v + 1);

// merge: atômico. Combina valor existente com o novo usando BiFunction.
cache.merge("contador", 1, Integer::sum);

// putIfAbsent: atômico. Adiciona só se chave ausente.
cache.putIfAbsent("config", "default");
```

> [!important] `computeIfAbsent` e `merge` são atômicos
> O Javadoc do Java 21 especifica: *"The entire method invocation is performed atomically."* para `computeIfAbsent` e `merge`. A função de mapeamento é invocada exatamente uma vez se a chave está ausente. Isso elimina a necessidade de lock externo para o padrão "get or compute".

**`size()` e concorrência** — o retorno de `size()` é exato em um instante, mas o Javadoc adverte que os resultados de `size()`, `isEmpty()` e `containsValue()` são *"typically useful only when a map is not undergoing concurrent updates in other threads."* Para mapas muito grandes, prefira `mappingCount()`, cujo retorno é explicitamente aproximado por ser `long` sem truncar em `Integer.MAX_VALUE`.

**Null não é permitido** — ao contrário de `HashMap`, `ConcurrentHashMap` lança `NullPointerException` para chaves ou valores nulos. A razão é que `null` é usado internamente como sentinela para indicar ausência de valor nos métodos que retornam valor especial.

**Iteração weakly consistent** — iteradores refletem o estado do mapa em algum ponto igual ou posterior à sua criação. Eles não lançam `ConcurrentModificationException`, mas podem ou não refletir modificações concorrentes feitas após a criação do iterador.

```java
ConcurrentHashMap<String, Integer> scores = new ConcurrentHashMap<>();
scores.put("alice", 10);
scores.put("bob", 20);

// forEach é thread-safe; iteração não lança ConcurrentModificationException
scores.forEach((k, v) -> System.out.println(k + " → " + v));

// Operações bulk paralelas (usa ForkJoinPool se acima do threshold)
int totalScore = scores.reduceValues(1000, Integer::sum);
```

---

### `CopyOnWriteArrayList` / `CopyOnWriteArraySet`

Toda operação de escrita (`add`, `set`, `remove`) cria uma cópia inteira do array interno, aplica a modificação na cópia e substitui a referência atomicamente. Leituras e iterações são completamente sem lock e operam sobre um snapshot imutável capturado no momento da criação do iterador.

```java
CopyOnWriteArrayList<String> listeners = new CopyOnWriteArrayList<>();

// Escrita: cria cópia do array — O(n)
listeners.add("listener-a");
listeners.add("listener-b");

// Leitura / iteração: sem lock, snapshot imutável
// O iterador não reflete adições ou remoções feitas depois de sua criação
for (String l : listeners) {
    dispatch(l);  // seguro mesmo que outra thread adicione durante a iteração
}
```

**Quando usar:** estruturas lidas com muito mais frequência do que escritas — listas de listeners de eventos, listas de handlers registrados, configurações imutáveis que são lidas em hot paths.

**Quando não usar:** qualquer cenário com escritas frequentes. Cada escrita é `O(n)` em tempo e requer o dobro de memória temporariamente. Em listas grandes com muitas mutações, o custo domina.

---

### `BlockingQueue`

`BlockingQueue` é uma interface que define uma fila thread-safe com semântica de bloqueio para inserções e remoções. É a base do padrão produtor-consumidor em Java.

O Javadoc define quatro grupos de operações, diferenciados pelo comportamento quando a operação não pode ser completada imediatamente:

| Operação | Lança exceção | Valor especial | Bloqueia | Com timeout |
|---|---|---|---|---|
| Inserir | `add(e)` | `offer(e)` | `put(e)` | `offer(e, t, unit)` |
| Remover | `remove()` | `poll()` | `take()` | `poll(t, unit)` |
| Examinar | `element()` | `peek()` | — | — |

**Garantia happens-before** — o Javadoc especifica: *"actions in a thread prior to placing an object into a BlockingQueue happen-before actions subsequent to the access or removal of that element from the BlockingQueue in another thread."* O produtor não precisa de sincronização adicional para que o consumidor veja o estado do objeto enfileirado.

**Null não é permitido** em nenhuma implementação de `BlockingQueue`. `null` é usado como valor sentinela pelo método `poll()` para indicar que a fila está vazia.

**Principais implementações:**

```java
// ArrayBlockingQueue: bounded, array circular, capacidade fixa
BlockingQueue<Task> bounded = new ArrayBlockingQueue<>(500);

// LinkedBlockingQueue: opcionalmente bounded, dois locks separados (put e take)
// → mais throughput que ArrayBlockingQueue em alta concorrência
BlockingQueue<Task> linked = new LinkedBlockingQueue<>(1000); // com limite
BlockingQueue<Task> unbounded = new LinkedBlockingQueue<>();   // sem limite — cuidado com OOM

// PriorityBlockingQueue: ordenada por prioridade, unbounded
BlockingQueue<Task> priority = new PriorityBlockingQueue<>();

// SynchronousQueue: capacidade zero, handoff direto produtor-consumidor
BlockingQueue<Task> sync = new SynchronousQueue<>();

// DelayQueue: elementos liberados após delay (Delayed interface)
BlockingQueue<ScheduledTask> delayed = new DelayQueue<>();
```

---

### `ConcurrentLinkedQueue`

Fila não-bloqueante (lock-free) baseada em algoritmo CAS. Nunca bloqueia o chamador — `offer()` retorna sempre `true` (fila ilimitada) e `poll()` retorna `null` se vazia. Adequada para cenários onde bloquear o produtor ou consumidor não é aceitável.

```java
ConcurrentLinkedQueue<Event> events = new ConcurrentLinkedQueue<>();

// Producer: nunca bloqueia
events.offer(new Event("login", userId));

// Consumer: retorna null se vazia (não bloqueia)
Event e = events.poll();
if (e != null) process(e);
```

**Quando preferir sobre `BlockingQueue`:** quando o produtor nunca deve bloquear e o consumidor pode fazer polling (ou usar busy-wait com backoff). Mais adequado para cenários de baixa latência onde blocking seria inaceitável.

---

### `ConcurrentSkipListMap` / `ConcurrentSkipListSet`

Alternativas concorrentes a `TreeMap` e `TreeSet`. Mantêm os elementos em ordem natural (ou por `Comparator`) e oferecem operações de navegação (`firstKey`, `floorKey`, `headMap`, etc.). Internamente implementadas com skip list (estrutura probabilística sem rebalanceamento de árvore).

```java
ConcurrentSkipListMap<String, Integer> ranking = new ConcurrentSkipListMap<>();
ranking.put("alice", 95);
ranking.put("bob", 87);
ranking.put("carol", 92);

// Operações de navegação são thread-safe
String top = ranking.firstKey();         // "alice"
Map<String, Integer> top2 = ranking.headMap("carol"); // alice, bob
```

**Quando usar:** quando você precisa de um mapa/set ordenado e thread-safe. Se a ordem não importa, prefira `ConcurrentHashMap` — é mais rápido.

## Na prática

### Cache concorrente com `computeIfAbsent`

Padrão clássico de cache thread-safe sem lock externo:

```java
ConcurrentHashMap<String, UserProfile> profileCache = new ConcurrentHashMap<>();

public UserProfile getProfile(String userId) {
    // computeIfAbsent: atômico — só carrega se ausente, só invoca a função uma vez
    return profileCache.computeIfAbsent(userId, id -> {
        // Esta função é invocada no máximo uma vez por chave ausente
        return userRepository.loadProfile(id);
    });
}

// Invalidar entrada
public void invalidate(String userId) {
    profileCache.remove(userId);
}

// Atualizar contagem de acessos de forma atômica
public void recordAccess(String userId) {
    accessCounts.merge(userId, 1, Integer::sum);
}
```

### Pipeline produtor-consumidor com `BlockingQueue`

```java
BlockingQueue<Task> queue = new ArrayBlockingQueue<>(200); // capacidade limitada = backpressure natural

// Producer thread
Thread producer = Thread.ofPlatform().name("producer").start(() -> {
    try {
        while (!Thread.currentThread().isInterrupted()) {
            Task task = generateNextTask();
            queue.put(task); // bloqueia se fila cheia — backpressure automático
        }
    } catch (InterruptedException e) {
        Thread.currentThread().interrupt();
    }
});

// Consumer threads (pool de N consumidores)
ExecutorService consumers = Executors.newFixedThreadPool(4);
for (int i = 0; i < 4; i++) {
    consumers.submit(() -> {
        try {
            while (!Thread.currentThread().isInterrupted()) {
                Task task = queue.take(); // bloqueia se fila vazia
                process(task);
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    });
}
```

### Árvore de decisão — qual concurrent collection escolher?

```text
Preciso de uma coleção thread-safe...

├── É um MAP?
│     ├── Precisa de ordem (sort)? → ConcurrentSkipListMap
│     └── Não precisa de ordem?   → ConcurrentHashMap (default)
│
├── É uma LIST ou SET?
│     ├── Leituras >> Escritas?   → CopyOnWriteArrayList / CopyOnWriteArraySet
│     └── Escritas frequentes?    → ConcurrentSkipListSet (set ordenado)
│                                   ou ConcurrentHashMap como set (keySet/newKeySet)
│
└── É uma QUEUE?
      ├── Precisa bloquear produtor/consumidor?
      │     ├── Capacidade fixa?        → ArrayBlockingQueue
      │     ├── Capacidade ajustável?   → LinkedBlockingQueue
      │     ├── Por prioridade?         → PriorityBlockingQueue
      │     └── Handoff direto?         → SynchronousQueue
      │
      └── Não pode bloquear (lock-free)?
            └── ConcurrentLinkedQueue / ConcurrentLinkedDeque
```

> [!tip] Regra geral
> Comece com `ConcurrentHashMap` para mapas e `LinkedBlockingQueue` para filas produtor-consumidor. Só substitua se o profiling indicar gargalo.

## Armadilhas

### (1) `Collections.synchronizedMap` + iteração não-atômica

**O problema:** `Collections.synchronizedMap` sincroniza cada método individualmente, mas a iteração exige lock externo explícito. Sem ele, outros threads podem modificar o mapa durante a iteração, causando `ConcurrentModificationException`.

```java
// RUIM — iteração não é atômica em synchronizedMap
Map<String, Integer> m = Collections.synchronizedMap(new HashMap<>());
// Outra thread pode modificar entre chamadas ao iterator!
for (Map.Entry<String, Integer> e : m.entrySet()) {  // ConcurrentModificationException
    process(e);
}
```

```java
// FIX 1 — lock externo explícito (verboso e propenso a esquecer)
synchronized (m) {
    for (Map.Entry<String, Integer> e : m.entrySet()) {
        process(e);
    }
}

// FIX 2 (melhor) — use ConcurrentHashMap, que não lança ConcurrentModificationException
ConcurrentHashMap<String, Integer> m = new ConcurrentHashMap<>();
m.forEach((k, v) -> process(k, v));  // iteração weakly consistent, sem exceção
```

---

### (2) Operação composta não-atômica em `ConcurrentHashMap` — use `compute`

**O problema:** separar um `get()` de um `put()` subsequente cria uma janela onde outra thread pode modificar a chave entre as duas chamadas. Mesmo usando `ConcurrentHashMap`, a sequência `get`→`put` **não é atômica**.

```java
// RUIM — check-then-act não é atômico
if (!cache.containsKey(key)) {           // thread B pode entrar aqui também
    cache.put(key, computeValue(key));   // ambas computam e inserem
}

// TAMBÉM RUIM — get/put separados
Integer v = cache.get("count");
cache.put("count", v == null ? 1 : v + 1);  // race condition entre get e put
```

```java
// FIX — use operações atômicas compostas
// computeIfAbsent: atômico, função invocada uma única vez
cache.computeIfAbsent(key, k -> computeValue(k));

// merge: atômico, combina valor existente com novo
cache.merge("count", 1, Integer::sum);

// compute: atômico, reformula o valor com lógica customizada
cache.compute("count", (k, v) -> v == null ? 1 : v + 1);
```

---

### (3) `CopyOnWriteArrayList` em cenário write-heavy

**O problema:** cada escrita no `CopyOnWriteArrayList` cria uma cópia do array inteiro. Em listas grandes com mutações frequentes, isso resulta em pressão de GC severa e degradação de performance.

```java
// RUIM — write-heavy com CopyOnWriteArrayList
CopyOnWriteArrayList<Integer> data = new CopyOnWriteArrayList<>();
// Loop com 10.000 adições = 10.000 cópias do array crescente = O(n²) total
for (int i = 0; i < 10_000; i++) {
    data.add(i);  // cada chamada copia o array inteiro até o momento
}
```

```java
// FIX — para write-heavy, use alternativas adequadas

// Opção 1: ConcurrentLinkedQueue (se ordem de inserção, sem acesso por índice)
ConcurrentLinkedQueue<Integer> queue = new ConcurrentLinkedQueue<>();

// Opção 2: Collections.synchronizedList para uso pontual
List<Integer> synced = Collections.synchronizedList(new ArrayList<>());

// Opção 3: adicionar em batch quando possível
List<Integer> batch = List.of(1, 2, 3, 4, 5);
data.addAll(batch);  // uma única cópia para o batch inteiro
```

**Regra de bolso:** se leituras são 10x ou mais frequentes que escritas, `CopyOnWriteArrayList` é adequado. Se escritas são frequentes, escolha outra estrutura.

## Em entrevista

### Frase pronta (inglês)

> "The concurrent collections in `java.util.concurrent` are specifically designed to avoid the global-lock bottleneck that `Collections.synchronizedMap` introduces. `ConcurrentHashMap`, for example, only locks at the bucket level during writes — reads are completely lock-free — and it provides atomic compound operations like `computeIfAbsent` and `merge` that eliminate the need for external locking on common get-or-compute patterns. The Javadoc specifies that the entire invocation of `computeIfAbsent` is performed atomically and the mapping function is called exactly once when the key is absent." "For producer-consumer pipelines, `BlockingQueue` is the canonical choice: `put` blocks the producer when the queue is full, giving you natural backpressure, and `take` blocks the consumer when empty — no polling, no busy-waiting, and the happens-before guarantee means the consumer always sees the correct state of the objects it receives." "The trap most developers fall into is mixing a `ConcurrentHashMap` with non-atomic compound operations: doing a `get` followed by a separate `put` is still a race condition — two threads can compute the same value simultaneously. The fix is always to use the atomic methods directly: `computeIfAbsent`, `merge`, or `compute`."

### Vocabulário

| Termo PT | Termo EN |
|---|---|
| coleção concorrente | concurrent collection |
| fila bloqueante | blocking queue |
| operação atômica composta | atomic compound operation |
| locking por bucket | bucket-level locking |
| iterador fracamente consistente | weakly consistent iterator |
| cópia na escrita | copy-on-write |
| produtor-consumidor | producer-consumer |
| contrapressão | backpressure |
| não-bloqueante (lock-free) | non-blocking / lock-free |
| mapa de skip list concorrente | concurrent skip-list map |

## Veja também

- [[06 - Atômicos e operações lock-free]]
- [[08 - Executors e thread pools]]
- [[09 - Sincronizadores]]
- [[Java Fundamentals]]
- [[03-Dominios/Java/Concorrência e paralelismo/index|MOC do galho]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[Java Concurrency]]
- [[03-Dominios/Java/Dicionário de Java#ConcurrentHashMap|ConcurrentHashMap]]
- [[03-Dominios/Java/Dicionário de Java#BlockingQueue|BlockingQueue]]

## Referências

- [ConcurrentHashMap — Java 21 API (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/ConcurrentHashMap.html)
- [CopyOnWriteArrayList — Java 21 API (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/CopyOnWriteArrayList.html)
- [BlockingQueue — Java 21 API (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/BlockingQueue.html)
- [ArrayBlockingQueue — Java 21 API (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/ArrayBlockingQueue.html)
- [LinkedBlockingQueue — Java 21 API (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/LinkedBlockingQueue.html)
- [ConcurrentLinkedQueue — Java 21 API (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/ConcurrentLinkedQueue.html)
- [ConcurrentSkipListMap — Java 21 API (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/ConcurrentSkipListMap.html)
- [java.util.concurrent package summary — Java 21 API (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/package-summary.html)
