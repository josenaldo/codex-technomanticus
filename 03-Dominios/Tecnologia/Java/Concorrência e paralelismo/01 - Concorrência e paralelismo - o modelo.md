---
title: "Concorrência e paralelismo: o modelo"
created: 2026-06-03
updated: 2026-06-03
type: concept
progress: backlog
status: seedling
publish: true
fase: Iniciado
tags:
  - java
  - concorrencia
  - iniciado
  - threads
  - fundamentos
aliases:
  - Concorrência
  - Paralelismo
---

# Concorrência e paralelismo: o modelo

> [!abstract] TL;DR
> **Concorrência** é a capacidade de lidar com muitas tarefas ao mesmo tempo — estruturar o programa para que múltiplas coisas possam progredir. **Paralelismo** é executá-las literalmente ao mesmo tempo em múltiplos núcleos. Java usa um modelo de **memória compartilhada** entre threads: eficiente, mas essa facilidade de comunicação é exatamente a fonte dos bugs mais difíceis de rastrear em produção.

## O que é

### Concorrência vs Paralelismo

Os termos são frequentemente confundidos, mas descrevem conceitos distintos:

- **Concorrência** é sobre **estrutura**: o programa é organizado de forma que múltiplas tarefas possam estar em progresso ao mesmo tempo — intercalando execução, fazendo progresso mesmo que não literalmente simultâneas. Exemplo: um servidor web que aceita novos pedidos enquanto ainda processa o anterior.
- **Paralelismo** é sobre **execução**: tarefas rodam ao mesmo tempo em hardware paralelo (múltiplos núcleos ou CPUs). Exemplo: um algoritmo de ordenação que divide o array em metades e ordena cada metade em um núcleo diferente.

Uma analogia útil: **concorrência** é um cozinheiro que prepara três pratos ao mesmo tempo — alterna entre eles conforme cada etapa termina. **Paralelismo** é três cozinheiros, cada um preparando um prato simultaneamente.

A distinção prática: é possível ter concorrência sem paralelismo (um único núcleo intercalando threads) e é possível ter paralelismo sem concorrência bem estruturada (o que causa bugs).

### Processos vs Threads

A JVM opera, na maior parte das implementações, como um único **processo** do sistema operacional. Um processo possui:

- Seu próprio espaço de memória, isolado dos demais processos
- Recursos privados (descritores de arquivo, sockets, etc.)
- Comunicação com outros processos via IPC (pipes, sockets)

Dentro de um processo existem **threads** — às vezes chamadas de "processos leves" (lightweight processes). Threads:

- Existem **dentro** de um processo; cada processo tem ao menos uma
- **Compartilham** a memória e os recursos abertos do processo
- Custam muito menos para criar do que processos
- Se comunicam com eficiência — mas essa comunicação compartilhada é a raiz dos problemas de concorrência

Em Java, toda aplicação começa com ao menos uma thread: a **main thread**. Ela pode criar novas threads para trabalho concorrente.

## Por que importa

Para quem almeja o nível sênior, concorrência não é um nicho — é inevitável:

- A maioria dos sistemas reais (APIs, filas de eventos, processamento em batch) executa trabalho concorrente. Bugs de concorrência são notoriamente difíceis de reproduzir: aparecem em produção sob carga, desaparecem no debugger, e podem corromper dados silenciosamente.
- **Race conditions**, **deadlocks** e erros de visibilidade de memória são listados consistentemente entre as categorias de bugs mais caros de diagnosticar e corrigir.
- Em entrevistas para posições sênior, a pergunta sobre concorrência é quase certa. O que diferencia o candidato sênior não é decorar APIs, mas **entender o modelo mental**: por que um contador compartilhado sem sincronização produz resultados errados, e qual é a forma correta de corrigi-lo.

## Como funciona

### Processos vs Threads (resumo técnico)

| Aspecto           | Processo                          | Thread                                  |
|-------------------|-----------------------------------|-----------------------------------------|
| Memória           | Espaço próprio e isolado          | Compartilhada com demais threads        |
| Custo de criação  | Alto (fork, alocação de recursos) | Baixo (estruturas dentro do processo)   |
| Comunicação       | IPC (pipes, sockets, sinais)      | Variáveis compartilhadas (direto)       |
| Isolamento de falhas | Crash isola o processo          | Crash pode derrubar toda a aplicação    |

### Modelo de memória compartilhada

Java adota o modelo de **memória compartilhada** (*shared memory*), em oposição ao modelo de **passagem de mensagens** (*message-passing*, usado por Go e Erlang/Elixir, por exemplo).

No modelo compartilhado:
- Threads dentro da mesma JVM enxergam o mesmo heap
- Comunicação é feita por leitura/escrita em variáveis compartilhadas
- É eficiente e natural em Java — mas exige que o programador **garanta a correção** dessas leituras e escritas

No modelo de passagem de mensagens:
- Cada ator/goroutine possui sua própria memória
- Comunicação é explícita via canais/mensagens
- Mais difícil de ter race conditions, mas requer estruturar o código de forma diferente

O modelo compartilhado torna Java poderoso para concorrência de baixa latência, mas coloca a responsabilidade de correção no desenvolvedor.

### Os três problemas: atomicidade, visibilidade, ordenação

Estes são os três eixos ao longo dos quais a concorrência pode falhar. (O deep dive técnico de cada um vai para [[11 - Java Memory Model em profundidade]].)

**Atomicidade** — uma operação composta que parece única mas não é. O exemplo clássico é `counter++`: envolve três passos (ler, incrementar, escrever) que podem ser interrompidos por outra thread no meio.

**Visibilidade** — uma thread pode não ver as escritas feitas por outra. CPUs modernas têm caches por núcleo; sem instruções de barreira de memória, um valor escrito por uma thread pode ficar no cache e nunca ser "flushed" para a memória principal visível às demais.

**Ordenação** — compiladores e CPUs reordenam instruções para performance. Em single-thread, a reordenação é indetectável. Em multi-thread, pode fazer com que uma thread observe operações numa ordem diferente da que o programador escreveu.

Esses três problemas são o *por quê* de `synchronized`, `volatile`, e das classes atômicas existirem.

### O landscape moderno: platform vs virtual threads

Historicamente, toda thread Java mapeava 1:1 para uma thread do sistema operacional (**platform thread**). Criar dezenas de milhares delas era inviável: cada uma consome ~1 MB de stack e estruturas no kernel.

O **Project Loom**, com as **Virtual Threads** tornadas definitivas no Java 21 (JEP 444), muda esse quadro:

- Virtual threads são gerenciadas pela JVM, não pelo OS
- Muitas virtual threads podem multiplicar sobre poucas platform threads
- Quando uma virtual thread bloqueia (em I/O, por exemplo), ela é "desmontada" da platform thread, que passa a executar outra virtual thread
- Permitem escrever código bloqueante simples com escalabilidade de código assíncrono

A distinção concorrência vs paralelismo fica nítida aqui: virtual threads ampliam a **concorrência** (mais tarefas em andamento ao mesmo tempo); para **paralelismo** CPU-bound, ainda se usam streams paralelas ou fork-join. O deep dive vai para [[12 - Virtual Threads e Project Loom]].

## Na prática

O exemplo abaixo mostra duas threads incrementando um contador compartilhado sem nenhuma sincronização. O resultado é não-determinístico: cada execução pode produzir um valor diferente, e raramente será 2000.

```java
public class ContadorCompartilhado {

    static int contador = 0;  // campo compartilhado — sem sincronização

    public static void main(String[] args) throws InterruptedException {
        Runnable tarefa = () -> {
            for (int i = 0; i < 1000; i++) {
                contador++;  // lê, incrementa, escreve — três passos não-atômicos
            }
        };

        Thread t1 = new Thread(tarefa, "thread-1");
        Thread t2 = new Thread(tarefa, "thread-2");

        t1.start();
        t2.start();

        t1.join();  // espera t1 terminar
        t2.join();  // espera t2 terminar

        System.out.println("Contador final: " + contador);
    }
}
```

```text
// Saída — NÃO-DETERMINÍSTICA. Exemplos de execuções possíveis:
Contador final: 1872
Contador final: 1435
Contador final: 2000  // ocorre, mas não é garantido
```

O resultado esperado seria 2000 (1000 incrementos por thread). Mas `counter++` não é atômico — outra thread pode ler o valor antes que a primeira termine de escrever, e um dos incrementos se perde. Esse é um **race condition** clássico.

A correção correta pode usar `synchronized`, `AtomicInteger`, ou outras primitivas — temas das notas seguintes.

## Armadilhas

### (1) Confundir concorrência com paralelismo

**O problema:** assumir que "usar threads" automaticamente produz paralelismo. Em sistemas com um único núcleo disponível (ou com scheduler do OS que não aloca múltiplos núcleos), threads concorrem pelo mesmo núcleo. O programa ganha estrutura (concorrência), mas não necessariamente velocidade (paralelismo). Pior: adicionar threads pode tornar o programa mais lento pelo overhead de context switch.

```java
// hipotético: código CPU-bound em duas threads num sistema de 1 núcleo
// Resultado: pode ser mais lento que single-thread pelo overhead de context switch
ExecutorService pool = Executors.newFixedThreadPool(2);
pool.submit(() -> calcularPiAté(1_000_000));
pool.submit(() -> calcularPiAté(1_000_000));
```

**Fix:** para trabalho CPU-bound, o número ideal de threads é próximo do número de núcleos disponíveis (`Runtime.getRuntime().availableProcessors()`). Para trabalho I/O-bound, virtual threads (Java 21+) são a abordagem moderna.

---

### (2) "Mais threads = mais rápido" (contention e context switch)

**O problema:** aumentar o pool de threads além de um certo ponto degrada a performance em vez de melhorá-la. Dois mecanismos explicam isso:

- **Contention** (contenção): múltiplas threads competindo pelo mesmo lock fazem a maioria esperar, anulando o ganho de paralelismo.
- **Context switch**: o OS tem custo para salvar e restaurar o estado de cada thread. Com muitas threads, o sistema gasta mais tempo trocando de thread do que executando trabalho real.

```java
// hipotético: pool excessivo para tarefa CPU-bound com lock compartilhado
ExecutorService pool = Executors.newFixedThreadPool(200);  // 200 threads para 4 núcleos
// Cada thread vai competir pelo mesmo recurso → contention extrema
```

**Fix:** calibrar o tamanho do pool pelo tipo de carga. Ferramentas como profilers e thread dumps (via `jstack`) revelam contention: muitas threads em estado `BLOCKED` no mesmo monitor é sinal claro de pool superdimensionado ou lock muito largo.

## Em entrevista

### Frase pronta (inglês)

> "Concurrency and parallelism are related but distinct concepts. Concurrency is about structure — designing a program so that multiple tasks can make progress, potentially interleaved on a single core. Parallelism is about execution — multiple tasks running literally at the same time on multiple CPU cores. In Java, the shared-memory model means threads communicate by reading and writing the same heap, which is efficient but places correctness responsibilities on the developer: without proper synchronization, you get race conditions, visibility failures, or reordering bugs. The trade-off matters in practice: for I/O-bound workloads, more concurrency helps throughput, and Java 21 virtual threads make this cheap; for CPU-bound workloads, parallelism through fork-join or parallel streams is the right tool, bounded by the number of available cores. The caveat is that adding threads doesn't automatically add speed — contention on shared locks and context-switch overhead can make a heavily-threaded design slower than a simpler single-threaded one."

Use essa resposta para perguntas como *"What is the difference between concurrency and parallelism?"*, *"How does Java's threading model work?"* ou *"When would you use virtual threads vs platform threads?"*.

### Vocabulário

| Termo PT                          | Termo EN                                        |
|-----------------------------------|-------------------------------------------------|
| concorrência                      | concurrency                                     |
| paralelismo                       | parallelism                                     |
| thread de plataforma              | platform thread                                 |
| thread virtual                    | virtual thread                                  |
| memória compartilhada             | shared memory                                   |
| passagem de mensagens             | message passing                                 |
| condição de corrida               | race condition                                  |
| exclusão mútua                    | mutual exclusion                                |
| contenção                         | contention                                      |
| troca de contexto                 | context switch                                  |
| atomicidade                       | atomicity                                       |
| visibilidade                      | visibility                                      |
| ordenação / reordenação           | ordering / reordering                           |
| barreira de memória               | memory barrier / memory fence                   |

## Veja também

- [[02 - Threads e seu ciclo de vida]]
- [[03 - Exclusão mútua com synchronized]]
- [[04 - As armadilhas - race, deadlock e companhia]]
- [[11 - Java Memory Model em profundidade]]
- [[12 - Virtual Threads e Project Loom]]
- [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|MOC do galho]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[Java Concurrency]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#Mutual exclusion (exclusão mútua)|mutual exclusion]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#Contention|contention]]

## Referências

- [Concurrency — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/essential/concurrency/)
- [Processes and Threads — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/essential/concurrency/procthread.html)
- [Virtual Threads — dev.java](https://dev.java/learn/new-features/virtual-threads/)
- [JEP 444: Virtual Threads (Java 21) — openjdk.org](https://openjdk.org/jeps/444)
- Goetz, Brian et al. *Java Concurrency in Practice*. Addison-Wesley, 2006. — referência canônica sobre o modelo de memória compartilhada, atomicidade, visibilidade e padrões corretos de sincronização em Java.
