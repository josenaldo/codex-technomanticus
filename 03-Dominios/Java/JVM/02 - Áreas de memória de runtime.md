---
title: "Áreas de memória de runtime"
created: 2026-06-05
updated: 2026-06-05
type: concept
progress: backlog
status: seedling
publish: true
fase: iniciado
tags:
  - java
  - jvm
  - iniciado
  - memoria
  - heap
aliases:
  - "Heap e Metaspace"
  - "Memória da JVM"
  - "Áreas de memória"
---

# Áreas de memória de runtime

> [!abstract] TL;DR
> O processo JVM é composto de várias áreas de memória distintas: heap (objetos, compartilhada entre threads), Metaspace (metadados de classes, fora do heap), stack por thread, PC register, native method stack e code cache. Cada `OutOfMemoryError` aponta para uma área específica — saber o mapa acelera muito o diagnóstico. `-Xmx` limita apenas o heap; o processo JVM como um todo consome significativamente mais memória do que o heap configurado.

## O que é

A JVM divide a memória de runtime em áreas com propósitos distintos. Conhecer esse mapa é pré-requisito para interpretar erros de memória, ajustar flags e responder perguntas de entrevista sobre diferenças entre heap, stack e Metaspace.

| Área | Escopo | O que armazena |
|------|--------|---------------|
| **Heap** | Compartilhada entre todas as threads | Instâncias de objetos e arrays |
| **Metaspace** | Compartilhada entre todas as threads | Metadados de classes (bytecode, estrutura de métodos) |
| **Stack (por thread)** | Exclusiva de cada thread | Frames de método: variáveis locais e pilha de operandos |
| **PC Register** | Exclusivo de cada thread | Endereço da instrução de bytecode em execução |
| **Native Method Stack** | Exclusiva de cada thread | Frames de métodos nativos (JNI) |
| **Code Cache** | Compartilhada | Código nativo compilado pelo JIT |

## Por que importa

- **Diagnóstico de OOM mais rápido**: a mensagem do `OutOfMemoryError` indica a área afetada. Sem o mapa, o diagnóstico começa no lugar errado.
- **Entrevistas de sênior**: três perguntas recorrentes — diferença entre heap e stack; o que é Metaspace e por que substituiu PermGen; por que `-Xmx` não limita a memória total do processo.
- **Sizing de containers**: o RSS (Resident Set Size) do processo JVM inclui heap + Metaspace + stacks + code cache + buffers nativos. Dimensionar pod/container apenas pelo `-Xmx` causa OOM no nível do SO.

## Como funciona

### Heap: Young (Eden + Survivor S0/S1) e Old/Tenured (+ humongous no G1)

O heap é a área compartilhada onde todos os objetos Java são alocados. O GC geracional divide o heap em **Young Generation** e **Old Generation** com base na *Weak Generational Hypothesis*: a maioria dos objetos morre jovem, portanto coletar a geração jovem com frequência é mais eficiente do que coletar o heap inteiro.

**Young Generation** contém três regiões:

- **Eden**: onde os novos objetos são alocados. Quando Eden enche, ocorre uma *minor GC*.
- **Survivor S0 e S1**: dois espaços, um sempre vazio. Durante a minor GC, objetos vivos de Eden e do survivor ocupado são copiados para o survivor vazio. Os dois espaços alternam de papel a cada coleta.

Objetos que sobrevivem a um número configurável de coletas (*tenuring threshold*) são **promovidos** para a **Old Generation** (também chamada *Tenured*). A Old armazena objetos de vida longa e é coletada em *major GCs*, que são mais longas.

No **G1GC** (padrão desde Java 9), o heap é dividido em regiões de tamanho fixo (~1–32 MB) que assumem dinamicamente o papel de Eden, Survivor ou Old. Objetos maiores que metade do tamanho de uma região são alocados diretamente em **humongous regions** — regiões contíguas na Old Generation. Objetos humongous são coletados durante minor GCs (desde Java 8u60), mas alocações frequentes de objetos grandes podem fragmentar o heap.

```text
┌─────────────────────────────────────────────────┐
│  Java Heap (-Xms / -Xmx)                        │
│                                                 │
│  Young Generation                               │
│  ┌──────────────┬───────────┬───────────┐       │
│  │    Eden      │   S0      │   S1      │       │
│  └──────────────┴───────────┴───────────┘       │
│                      ↓ promoção                  │
│  Old / Tenured Generation                        │
│  ┌────────────────────────────────────┐          │
│  │  objetos de longa duração          │          │
│  │  humongous objects (G1)            │          │
│  └────────────────────────────────────┘          │
└─────────────────────────────────────────────────┘
```

O heap é compartilhada entre todas as threads — qualquer thread pode ler ou escrever em qualquer objeto no heap. Isso levanta a questão de visibilidade de escritas entre threads: esse assunto pertence ao [[03-Dominios/Java/Concorrência e paralelismo/11 - Java Memory Model em profundidade|Java Memory Model]] (happens-before, volatile, sincronização) e está fora do escopo desta nota.

### Metaspace (Java 8+; por que PermGen morreu)

O **Metaspace** armazena os metadados de classes carregadas: estrutura de métodos, bytecode, tabelas de constantes, anotações e informações de tipos. Ao contrário do heap, ele reside na **memória nativa do SO**, fora do heap Java.

Antes do Java 8, essa área se chamava **PermGen** (*Permanent Generation*) e ficava dentro do heap, com tamanho fixo controlado por `-XX:PermSize` e `-XX:MaxPermSize`. O problema era duplo: o tamanho fixo causava `OutOfMemoryError: PermGen space` em aplicações com muitas classes (servidores de aplicação com múltiplos deploys), e o ajuste era difícil de acertar.

**Java 8 substituiu PermGen pelo Metaspace:**

| Aspecto | PermGen (até Java 7) | Metaspace (Java 8+) |
|---------|----------------------|---------------------|
| Localização | Java Heap | Memória nativa do SO |
| Tamanho padrão | Fixo e pequeno | Dinâmico (cresce até a RAM disponível) |
| Controle | `-XX:PermSize` / `-XX:MaxPermSize` | `-XX:MetaspaceSize` / `-XX:MaxMetaspaceSize` |
| OOM | `PermGen space` | `Metaspace` |

Por padrão, o Metaspace não tem limite máximo — ele cresce conforme classes são carregadas. Definir `-XX:MaxMetaspaceSize` é recomendado em produção para evitar que um leak de classloader consuma toda a memória do host.

### Stack por thread (frames, variáveis locais, operandos; `-Xss`)

Cada thread Java tem sua própria **stack** (pilha de execução). A stack é composta de **frames**: quando um método é invocado, um novo frame é empilhado; quando o método retorna, o frame é desempilhado.

Cada frame contém:
- **Variáveis locais**: incluindo os parâmetros do método e variáveis primitivas declaradas no corpo. Referências a objetos também ficam aqui (o objeto em si fica no heap).
- **Pilha de operandos**: área de trabalho para as instruções de bytecode (operações aritméticas, invocações etc.).
- **Referência ao pool de constantes** da classe.

O tamanho de cada stack de thread é controlado por `-Xss` (padrão: 512 KB–1 MB dependendo da plataforma). Recursão muito profunda esgota a stack e causa `StackOverflowError` — não `OutOfMemoryError`.

### PC Register e Native Method Stack

Cada thread mantém um **PC Register** (*Program Counter*): um ponteiro para a instrução de bytecode que está sendo executada naquele momento. Para métodos nativos, o valor é indefinido (a CPU tem seu próprio registrador de instrução).

A **Native Method Stack** é o equivalente da stack Java para métodos nativos (JNI). Em HotSpot, a native method stack e a stack Java são geralmente a mesma estrutura.

### Code Cache (onde o JIT guarda código nativo)

O **Code Cache** é a área de memória onde o compilador JIT armazena o código nativo compilado — tanto código gerado por C1 quanto por C2. Fica fora do heap.

Quando o code cache enche, o JIT para de compilar novos métodos e a aplicação passa a rodar apenas em modo interpretado, com queda significativa de throughput. O aviso `CodeCache is full. Compiler has been disabled.` nos logs indica esse estado.

Controlado por `-XX:ReservedCodeCacheSize` (padrão: ~240–256 MB no Java 21).

```text
Visão geral: processo JVM (RSS)
┌────────────────────────────────────────────────────────────┐
│                                                            │
│  Java Heap (-Xms / -Xmx)                                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Young (Eden + S0 + S1)  │  Old/Tenured              │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                            │
│  Metaspace (memória nativa, fora do heap)                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  metadados de classes, bytecode, pool de constantes  │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                            │
│  Code Cache  │  Por thread: Stack + PC Register + NMS      │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

## Na prática

### Mapa de erros

| Erro | Área afetada | Causa típica | Primeira reação |
|------|--------------|--------------|-----------------|
| `OutOfMemoryError: Java heap space` | Heap | Leak de objetos, heap subdimensionado | Heap dump + analisar com Eclipse MAT ou VisualVM |
| `OutOfMemoryError: Metaspace` | Metaspace | Leak de classloader, redeploys em quente | Heap dump + analisar classloaders carregados |
| `OutOfMemoryError: unable to create native thread` | Memória nativa (stacks) | Muitas threads criadas, memória nativa esgotada | Verificar thread count com `jstack`; reduzir `-Xss` ou número de threads |
| `OutOfMemoryError: GC overhead limit exceeded` | Heap | GC gasta >98% do tempo recuperando <2% | Aumentar heap ou investigar leak |
| `StackOverflowError` | Stack (por thread) | Recursão profunda ou infinita | Revisar lógica de recursão; considerar versão iterativa |

### Flags de dimensionamento

```bash
# Exemplo de linha de comando para aplicação de processamento de pedidos
java \
  -Xms512m \                        # heap inicial (evita resize no startup)
  -Xmx2g \                          # heap máximo
  -Xss512k \                        # stack por thread
  -XX:MetaspaceSize=128m \           # tamanho inicial do Metaspace
  -XX:MaxMetaspaceSize=256m \        # limite máximo do Metaspace
  -XX:ReservedCodeCacheSize=256m \   # code cache para o JIT
  -jar order-processor.jar
```

| Flag | O que controla | Padrão (Java 21) |
|------|---------------|-----------------|
| `-Xms` | Heap inicial | ~1/64 da RAM |
| `-Xmx` | Heap máximo | ~1/4 da RAM |
| `-Xss` | Stack por thread | 512 KB–1 MB |
| `-XX:MetaspaceSize` | Tamanho inicial do Metaspace | ~21 MB |
| `-XX:MaxMetaspaceSize` | Limite máximo do Metaspace | ilimitado (padrão) |
| `-XX:ReservedCodeCacheSize` | Tamanho do code cache | ~240 MB |

## Armadilhas

### (1) Achar que `-Xmx` limita a memória total do processo

**O problema:** `-Xmx` limita apenas o heap Java. O processo JVM consome adicionalmente: Metaspace, stacks de todas as threads (N threads × `-Xss`), code cache, JVM internals, buffers nativos (NIO, direct ByteBuffer). Em produção, o RSS de um processo com `-Xmx2g` pode facilmente chegar a 3–4 GB.

```bash
# Ver consumo real do processo JVM (Linux)
ps -o pid,rss,vsz -p <PID>

# Ou com Native Memory Tracking
java -XX:NativeMemoryTracking=summary -jar app.jar
jcmd <PID> VM.native_memory summary
```

**Fix:** dimensionar o pod ou host com base no RSS esperado. Uma heurística conservadora: RSS ≈ `-Xmx` + ~500 MB para overhead JVM (Metaspace + stacks + code cache). Em containers Kubernetes, definir `resources.limits.memory` com margem acima do `-Xmx`.

---

### (2) `OutOfMemoryError: Metaspace` por leak de classloader em redeploy

**O problema:** em servidores de aplicação (Tomcat, WildFly) ou ambientes com hot-reload (Spring DevTools), cada redeploy cria um novo `ClassLoader`. Se o classloader antigo mantiver referências estáticas acessíveis via GC roots, as classes carregadas por ele não podem ser descarregadas — o Metaspace cresce indefinidamente a cada redeploy.

```java
// Exemplo clássico de leak: cache estático segurando referência à classe do deploy anterior
public class OrderRegistry {
    // Se este Map nunca for limpo, as classes do deploy anterior ficam no Metaspace
    private static final Map<String, Class<?>> cache = new HashMap<>();
}
```

**Fix:** gerar heap dump (`jcmd <PID> GC.heap_dump arquivo.hprof`) e analisar no Eclipse MAT com o relatório *Leak Suspects*. Buscar classloaders duplicados na view *OQL*: `select cl from java.lang.ClassLoader cl`. A nota [[05 - Classloading e o delegation model]] detalha o ciclo de vida de classloaders e como evitar esse padrão.

---

### (3) Recursão profunda leva a `StackOverflowError` — quando ajustar `-Xss` vs. reescrever

**O problema:** cada frame na stack ocupa memória. Recursão com centenas de níveis pode estourar a stack, especialmente com `-Xss` pequeno ou frames grandes (muitas variáveis locais).

```java
// Recursão ingênua — estoura stack para n grande
public long factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1); // cada chamada empilha um frame
}
```

**Fix — dois caminhos:**
1. **Aumentar `-Xss`**: apenas se a profundidade é justificada pelo problema (ex: travessia de árvores profundas). Aumentar stack aumenta o consumo de memória nativa por thread — com 200 threads e `-Xss2m`, são 400 MB só de stacks.
2. **Reescrever iterativo**: solução preferida para algoritmos que naturalmente não precisam de recursão profunda (Fibonacci, factorial, travessias de listas). Evita o problema na raiz.

```java
// Versão iterativa — sem risco de StackOverflowError
public long factorial(int n) {
    long result = 1;
    for (int i = 2; i <= n; i++) result *= i;
    return result;
}
```

## Em entrevista

### Frase pronta (inglês)

> "The JVM runtime memory is divided into several distinct areas. The heap is the shared area where all object instances live, and it's split generationally into Young — with Eden and two Survivor spaces — and Old, or Tenured. Metaspace, introduced in Java 8 to replace PermGen, stores class metadata in native memory outside the heap, which means it can grow dynamically and isn't bound by `-Xmx`. Each thread has its own stack holding method frames with local variables and operands, a PC register pointing to the current bytecode instruction, and a native method stack for JNI. The code cache holds JIT-compiled native code and is also separate from the heap."

> "A critical point for production sizing is that `-Xmx` only caps the heap. The actual RSS of the JVM process includes Metaspace, thread stacks — which are N-threads times `-Xss` — code cache, and JVM internals. In containerized environments, this means you must set your pod memory limit well above `-Xmx`, typically adding 500 MB or more for overhead."

> "Each `OutOfMemoryError` message points to a specific area: `Java heap space` means the heap is exhausted, `Metaspace` usually indicates a classloader leak in a hot-deploy scenario, and `unable to create native thread` means native memory for thread stacks ran out. `StackOverflowError` is not an `OutOfMemoryError` at all — it means a single thread's stack depth was exceeded, typically from unbounded recursion."

### Vocabulário

| Termo PT | Termo EN |
|----------|----------|
| heap / área do heap | heap / heap memory |
| geração jovem | young generation |
| geração antiga / tenured | old generation / tenured generation |
| espaço Eden | Eden space |
| espaços sobreviventes | survivor spaces |
| objetos humongous | humongous objects |
| Metaspace | Metaspace |
| geração permanente | permanent generation (PermGen) |
| pilha por thread | per-thread stack |
| frame de pilha | stack frame |
| variáveis locais | local variables |
| cache de código | code cache |
| memória nativa | native memory |
| conjunto residente | resident set size (RSS) |
| promoção de objetos | object promotion |
| estouro de pilha | stack overflow |

## Veja também

- [[01 - A JVM — o que é e o pipeline de execução]]
- [[03 - Garbage Collection — o conceito]]
- [[05 - Classloading e o delegation model]]
- [[09 - Flags, ergonomics e a JVM em containers]]
- [[12 - Diagnóstico — heap dumps, thread dumps e jcmd]]
- [[03-Dominios/Java/Concorrência e paralelismo/11 - Java Memory Model em profundidade|Java Memory Model]]
- [[03-Dominios/Java/JVM/index|JVM por dentro (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Dicionário de Java#heap|heap (Dicionário)]]
- [[03-Dominios/Java/Dicionário de Java#Metaspace|Metaspace (Dicionário)]]
- [[03-Dominios/Java/Dicionário de Java#stack frame|stack frame (Dicionário)]]

## Referências

- [Garbage Collector Implementation — Oracle GC Tuning Guide (Java 21)](https://docs.oracle.com/en/java/javase/21/gctuning/garbage-collector-implementation.html)
- [Troubleshooting Memory Leaks — Oracle Troubleshooting Guide (Java 21)](https://docs.oracle.com/en/java/javase/21/troubleshoot/troubleshooting-memory-leaks.html)
- [Java Virtual Machine Specification — Run-Time Data Areas](https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-2.html#jvms-2.5)
