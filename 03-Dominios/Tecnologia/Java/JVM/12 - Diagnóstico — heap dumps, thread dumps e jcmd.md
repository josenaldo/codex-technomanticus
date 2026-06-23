---
title: "Diagnóstico — heap dumps, thread dumps e jcmd"
created: 2026-06-05
updated: 2026-06-05
type: concept
progress: backlog
status: seedling
publish: true
fase: magus
tags:
  - java
  - jvm
  - magus
  - diagnostico
aliases:
  - "Heap dump"
  - "Thread dump"
  - "jcmd"
  - "Eclipse MAT"
---

# Diagnóstico — heap dumps, thread dumps e jcmd

> [!abstract] TL;DR
> O kit forense da JVM tem quatro peças: **jcmd** (canivete moderno que centraliza diagnósticos sem precisar de ferramentas separadas), **heap dump** (fotografia de todos os objetos na memória num instante — a evidência do OOM), **thread dump** (fotografia do estado de cada thread e seus locks — a evidência do deadlock ou do thread preso), e **NMT** (Native Memory Tracking — o raio-X da memória nativa quando o RSS do processo cresce mas o heap Java não explica o crescimento). A diferença entre incidente resolvido e adivinhação é ter a evidência. E a diferença entre ter e não ter a evidência do OOM é uma flag ligada antes do incidente: `-XX:+HeapDumpOnOutOfMemoryError` com `-XX:HeapDumpPath` apontando para um volume persistente garante que o processo morra com o .hprof em disco — não apenas com uma linha de log.

## O que é

Diagnóstico de JVM é o conjunto de técnicas e ferramentas para capturar **evidência forense** de uma JVM em dificuldade — memória exaustada, thread travada, processo consumindo mais RAM do que o heap Java explicaria. As três categorias de evidência:

**Heap dump** — um arquivo HPROF contendo a fotografia completa de todos os objetos alocados no heap Java no momento da captura: instâncias, classes, referências entre objetos, tamanho retido por cada grafo de objetos. É a matéria-prima para análise de memory leak e investigação de OOM.

**Thread dump** — um snapshot textual de todas as threads em execução no momento da captura: nome, estado (`RUNNABLE`, `BLOCKED`, `WAITING`, `TIMED_WAITING`), stack trace completo e, quando disponível, o lock que a thread segura e quem está esperando por ele. É a matéria-prima para investigação de deadlock, thread pool esgotado e processamento travado.

**NMT (Native Memory Tracking)** — relatório da memória nativa consumida por subsistemas da JVM (heap Java, metaspace, código JIT, threads, GC, class loading). Disponível via `jcmd VM.native_memory` após habilitar com `-XX:NativeMemoryTracking=summary` (ou `detail`). Indispensável quando o RSS do processo no SO é muito maior do que o heap Java configurado.

As **ferramentas** que capturam essas evidências:

| Ferramenta | Categoria | Papel principal |
|---|---|---|
| `jcmd` | moderna (Java 7+) | canivete: captura heap dump, thread dump, flags, NMT, muito mais |
| `jmap` | legada | heap dump; ainda aparece em scripts antigos e documentação |
| `jstack` | legada | thread dump; ainda presente em tutoriais e runbooks |
| `jstat` | legada | séries temporais de GC sem heap dump |
| Eclipse MAT | análise offline | lê o .hprof, calcula dominator tree, identifica leak suspects |

## Por que importa

Quando o OOM acontece às 3 da manhã e o pod K8s reinicia sozinho, a evidência some junto com o processo — a menos que ela tenha sido gravada antes da morte. Quando um serviço trava sem mensagem de erro, a causa está nos stacks das threads — mas só se alguém tirar o snapshot. **Ou você tem a evidência, ou tem adivinhação.**

Do ponto de vista de carreira, esse é um dos territórios que mais distingue senioridade real de sênior-no-título. Resolver um OOM em produção com heap dump + MAT — encontrar o `OrderCache` estático sem TTL que foi crescendo por 14 horas até consumir 7 GB — é o tipo de história técnica concreta que fecha entrevistas de staff/principal. Não é teoria: é processo forense reproduzível.

A outra razão é que o custo de **não** ter as flags certas é pago no pior momento. Ligar `HeapDumpOnOutOfMemoryError` depois do OOM é impossível. Configurar o `HeapDumpPath` para um diretório que não persiste entre reinicializações é o mesmo que não configurar. Esses são erros de preparação que se pagam em incidentes futuros — e que um engenheiro sênior já cometeu, aprendeu, e agora previne em toda nova aplicação.

## Como funciona

### jcmd — o canivete (GC.heap_dump, Thread.print, VM.flags, GC.heap_info, VM.native_memory, help)

`jcmd` é a ferramenta canônica para diagnóstico ao vivo desde o Java 7. Um único binário substitui `jmap`, `jstack`, `jinfo` e outros, com interface mais consistente e subcomandos descobríveis.

**Sintaxe geral:**

```bash
jcmd <pid>            # lista os subcomandos disponíveis para o processo
jcmd <pid> help       # idem, explícito
jcmd <pid> help GC.heap_dump   # ajuda de um subcomando específico
jcmd -l               # lista todos os processos Java em execução com seus PIDs
```

**Subcomandos essenciais (confirmados na man page do Java 21):**

`GC.heap_dump` — gera um arquivo HPROF do heap Java. Impacto: **alto** (solicita um GC full, exceto com `-all`). Aceita os flags `-all` (incluir objetos inalcançáveis), `-gz=<1-9>` (compressão gzip) e `-overwrite`.

```bash
jcmd <pid> GC.heap_dump /tmp/app.hprof
jcmd <pid> GC.heap_dump -overwrite -gz=9 /tmp/app.hprof.gz
```

`Thread.print` — imprime todas as threads com stack traces. Impacto: **médio**. Com `-e` imprime informações estendidas; com `-l` inclui locks `java.util.concurrent`.

```bash
jcmd <pid> Thread.print
jcmd <pid> Thread.print -e -l
```

`VM.flags` — imprime as flags da JVM e seus valores correntes. Impacto: **baixo**. Com `-all` mostra todas as flags suportadas pela VM (centenas).

```bash
jcmd <pid> VM.flags
jcmd <pid> VM.flags -all
```

`GC.heap_info` — informação genérica do heap Java (regiões, occupancy). Impacto: **médio**. Mais leve que `GC.heap_dump`; útil para checar o estado do heap sem gerar um arquivo grande.

```bash
jcmd <pid> GC.heap_info
```

`VM.native_memory` — imprime o uso de memória nativa por subsistema (requer `-XX:NativeMemoryTracking=summary|detail` no startup da JVM). Aceita `summary`, `detail`, `baseline`, `summary.diff`, `detail.diff` e `scale=KB|MB|GB`.

```bash
jcmd <pid> VM.native_memory summary scale=MB
jcmd <pid> VM.native_memory baseline          # tira uma baseline
# ... deixar o processo rodar ...
jcmd <pid> VM.native_memory summary.diff scale=MB   # compara com a baseline
```

`help` — o ponto de entrada para descobrir o resto. Cada JVM expõe um conjunto diferente de subcomandos dependendo dos agentes carregados (JFR, JVMTI, etc.); `jcmd <pid> help -all` lista tudo disponível naquele processo específico.

```bash
jcmd <pid> help -all   # descobrir todos os subcomandos disponíveis
```

### As ferramentas legadas vivas (jstat para séries temporais, jmap/jstack — onde ainda aparecem)

**`jstat -gcutil`** é o único caso em que uma ferramenta legada ainda tem vantagem sobre `jcmd`: ela produz **séries temporais** de ocupação de GC a intervalos regulares, o que é útil para ver o live-set crescendo ao longo do tempo sem gerar um dump pesado.

```bash
jstat -gcutil <pid> 5000    # amostra a cada 5 segundos
# saída: S0, S1, E (eden), O (old), M (metaspace), CCS (compressed class space), YGC, YGCT, FGC, FGCT, CGC, CGCT, GCT
```

**`jmap -dump`** e **`jstack <pid>`** ainda aparecem extensivamente em runbooks antigos, documentação de ferramentas externas e tutoriais. Funcionam, mas `jcmd` é o substituto moderno recomendado — mais seguro (não usa API de attach interna depreciada) e com interface mais consistente. Em ambientes containerizados com binários mínimos, às vezes só `jcmd` está disponível.

```bash
# legado — equivalente ao jcmd GC.heap_dump
jmap -dump:format=b,file=/tmp/app.hprof <pid>

# legado — equivalente ao jcmd Thread.print
jstack <pid>
```

### Heap dump (capturar e analisar no Eclipse MAT)

**Captura via jcmd (ao vivo):**

```bash
jcmd <pid> GC.heap_dump -overwrite /tmp/heap.hprof
```

**Captura automática no OOM (a flag mais importante de preparação):**

Confirmadas na man page do `java` para Java 21:

- `-XX:+HeapDumpOnOutOfMemoryError` — habilita a gravação automática de um heap dump HPROF quando um `OutOfMemoryError` é lançado. **Desligada por default.** Deve ser ligada em toda aplicação de produção.
- `-XX:HeapDumpPath=<path>` — define o caminho do arquivo. Default: `java_pid<pid>.hprof` no diretório corrente. Em containers: apontar para um volume persistente. Aceita `%p` como placeholder do PID.

```bash
java \
  -XX:+HeapDumpOnOutOfMemoryError \
  -XX:HeapDumpPath=/mnt/dumps/heap-%p.hprof \
  -jar app.jar
```

**Análise no Eclipse MAT:**

MAT é um analisador offline de arquivos HPROF. Ele abre dumps com centenas de milhões de objetos e oferece três visões principais:

- **Histogram** — lista todas as classes com o número de instâncias e o shallow size total (tamanho direto de cada objeto, sem o grafo que ele retém) por default. Retained size é calculado sob demanda e pode ser aproximado para conjuntos grandes. Ponto de partida: quais classes dominam em número de instâncias ou em tamanho?
- **Dominator tree** — para cada objeto, mostra quem é o "dominador" (quem segura a referência que impede o GC de coletar o grafo inteiro). É a visão que responde "quem está segurando tudo isso?". Uma entrada com retenção de vários GB no topo da dominator tree é o leak.
- **Leak Suspects** — relatório automático gerado pelo MAT que identifica os candidatos mais prováveis de leak com base na dominator tree. Bom ponto de entrada em dumps desconhecidos.

**Anatomia do leak típico:**

Os padrões mais comuns encontrados em dominator trees:

- **Cache estático sem bound ou TTL** — um `Map` ou `List` em campo `static` que cresce indefinidamente. Exemplo: cache de sessão que nunca expira.
- **Listener não removido** — objeto registrado em evento/observer que mantém a referência viva muito depois de sua vida útil esperada. Comum em frameworks de UI e em código que usa `EventBus`.
- **ThreadLocal em thread pool** — valor armazenado em `ThreadLocal` em threads de um pool nunca é coletado automaticamente (a thread não morre, o valor fica). Requer `remove()` explícito.

### Thread dump (estados, locks e como ler em série)

Um thread dump é um snapshot textual. Cada entrada contém:

```text
"http-nio-8080-exec-1" #42 daemon prio=5 os_prio=0 cpu=1234.56ms elapsed=3600.00s tid=0x00007f... nid=0x... waiting on condition [0x...]
   java.lang.Thread.State: WAITING (parking)
        at sun.misc.Unsafe.park(Native Method)
        - parking to wait for <0x0000000700012345> (a java.util.concurrent.locks.ReentrantLock$NonfairSync)
        at java.util.concurrent.locks.LockSupport.park(LockSupport.java:211)
        ...
```

Os estados relevantes para triagem:

| Estado | Significado |
|---|---|
| `RUNNABLE` | executando em CPU ou aguardando I/O (no SO, não na JVM) |
| `BLOCKED` | esperando por um monitor (`synchronized`) que outra thread segura |
| `WAITING` | esperando indefinidamente (`Object.wait()`, `LockSupport.park()`) |
| `TIMED_WAITING` | esperando com timeout (`Thread.sleep()`, `wait(timeout)`) |

**Deadlock detection automática:** o `jcmd Thread.print` (e o `jstack`) detecta deadlocks automaticamente e os lista no final do dump com as threads envolvidas e os locks que cada uma segura e aguarda.

**Leitura em série — o ponto mais ignorado:** um único thread dump é um snapshot que pode ser enganoso. Uma thread aparecendo como `WAITING` pode estar apenas em pausa momentânea num processamento saudável. A técnica correta é **capturar 3+ dumps espaçados de ~10 segundos** e comparar:

- Thread `BLOCKED` em todos os dumps com o mesmo lock owner → deadlock ou contenção grave.
- Thread `RUNNABLE` em todos os dumps com o mesmo stack frame no topo → loop infinito ou hot spot.
- Thread mudando de estado entre dumps → processamento normal, não é o problema.

```bash
for i in 1 2 3; do
  jcmd <pid> Thread.print > /tmp/tdump-$i.txt
  sleep 10
done
```

### NMT (-XX:NativeMemoryTracking=summary + jcmd VM.native_memory)

O heap Java configurado com `-Xmx` não representa toda a memória consumida pelo processo. O RSS real do processo inclui também: metaspace, buffers JIT, memória de threads (stack nativa de cada thread), overhead de GC, buffers de I/O nativos (NIO direct buffers), e memória alocada por bibliotecas nativas. Quando o RSS cresce e o heap Java está estável, o NMT é a ferramenta.

Confirmado na man page do `java` para Java 21:

- `-XX:NativeMemoryTracking=off` — default; sem rastreamento.
- `-XX:NativeMemoryTracking=summary` — rastreia por subsistema JVM.
- `-XX:NativeMemoryTracking=detail` — rastreia por callsite (overhead de CPU maior; para investigação pontual).

**Fluxo de uso:**

```bash
# 1. Iniciar a JVM com NMT (deve estar no startup — não pode ser ligado ao vivo)
java -XX:NativeMemoryTracking=summary -jar app.jar

# 2. Ver o estado corrente
jcmd <pid> VM.native_memory summary scale=MB

# 3. Tomar uma baseline
jcmd <pid> VM.native_memory baseline

# 4. Após um período (horas, dias), comparar
jcmd <pid> VM.native_memory summary.diff scale=MB
```

A saída de `summary.diff` mostra quais subsistemas cresceram e quanto desde a baseline — o caminho mais direto para identificar se o crescimento de RSS vem de metaspace, de thread stacks, de buffers de código JIT, ou de alocação nativa.

## Na prática

### Cenário completo — OOM num pod K8s

```text
// hipotético: serviço de catálogo (CatalogService), Java 21, G1 default,
// -Xmx2g, rodando em pod K8s com 2.5 GB de limite de memória.
// Sintoma: pod reinicia com OOM killer às ~4h de funcionamento; logs mostram
// apenas a reinicialização — sem stack trace de OutOfMemoryError gravada.
// Evidência: zero. Investigação: adivinhação.
```

**Fase 0 — preparação (antes do próximo incidente).**

A primeira constatação é que o pod não tinha `HeapDumpOnOutOfMemoryError` ligada. O caminho correto é adicionar as flags e garantir o volume:

```bash
# hipotético: trecho do Dockerfile / entrypoint após o diagnóstico da ausência
java \
  -Xmx2g \
  -XX:+HeapDumpOnOutOfMemoryError \
  -XX:HeapDumpPath=/mnt/dumps/heap-%p.hprof \
  -XX:NativeMemoryTracking=summary \
  -Xlog:gc*:file=/mnt/logs/gc.log:time,uptime,level,tags:filecount=5,filesize=20m \
  -jar catalog-service.jar
```

```yaml
# hipotético: trecho do manifesto K8s — volume persistente para os dumps
volumeMounts:
  - name: dump-volume
    mountPath: /mnt/dumps
volumes:
  - name: dump-volume
    persistentVolumeClaim:
      claimName: jvm-dumps-pvc
```

**Fase 1 — próximo OOM acontece. Dump gravado automaticamente.**

```bash
# hipotético: verificar o dump gerado no volume
ls -lh /mnt/dumps/
# -rw-r--r-- 1 app app 1.9G Jun 05 04:17 heap-42.hprof
```

**Fase 2 — copiar o dump para fora do pod (MAT não roda no pod).**

```bash
# hipotético: copiar para estação de análise
kubectl cp catalog-pod:/mnt/dumps/heap-42.hprof ./heap-42.hprof
```

**Fase 3 — abrir no Eclipse MAT e consultar a dominator tree.**

```text
// hipotético: saída resumida da dominator tree no MAT
Dominator Tree (top 5 retainers):
  1.  com.example.catalog.OrderCache   1.74 GB  91.6%
      └── java.util.HashMap$Node[]     1.74 GB
          └── [16 843 211 entries]
  2.  ...
```

A dominator tree aponta `OrderCache` como retentor de 1,74 GB — 91,6% do heap. O histogram confirma: mais de 16 milhões de entradas num `HashMap`.

**Fase 4 — inspeção no código.**

```java
// hipotético: classe encontrada via MAT
public class OrderCache {
    // cache estático sem bound, sem TTL — cresce até o OOM
    private static final Map<String, Order> CACHE = new HashMap<>();

    public static void put(String orderId, Order order) {
        CACHE.put(orderId, order);   // nunca remove
    }
}
```

**Fase 5 — fix.**

```java
// hipotético: fix com Caffeine (bound + TTL)
import com.github.benmanes.caffeine.cache.Cache;
import com.github.benmanes.caffeine.cache.Caffeine;
import java.util.concurrent.TimeUnit;

public class OrderCache {
    private static final Cache<String, Order> CACHE = Caffeine.newBuilder()
        .maximumSize(50_000)
        .expireAfterWrite(30, TimeUnit.MINUTES)
        .build();

    public static void put(String orderId, Order order) {
        CACHE.put(orderId, order);
    }
}
```

Após o deploy, `jstat -gcutil` confirma o live-set estável: a coluna `O` (Old) oscila em torno de 41% sem crescimento contínuo — o leak está resolvido.

## Armadilhas

### (1) Heap dump em produção sem saber o custo

**O problema:** `GC.heap_dump` (e `jmap -dump`) solicita um GC full (stop-the-world) e em seguida percorre **todo o heap** para serializar os objetos. Num heap de 4 GB, a pausa pode durar de segundos a minutos — suficiente para derrubar o SLA da aplicação. Adicionalmente, o arquivo gerado tem aproximadamente o mesmo tamanho do heap em uso: 4 GB de heap ocupado gera um .hprof de ~4 GB. Se o diretório alvo não tiver espaço, o dump é corrompido ou falha.

```bash
# hipotético: conferir espaço ANTES de disparar o dump em produção
df -h /tmp
# Filesystem      Size  Used Avail Use% Mounted on
# /dev/sda1        10G   9.2G  0.8G  92% /tmp   ← 0.8 GB livres para um heap de 4 GB = problema
```

**Fix:** escolher uma janela de baixo tráfego, confirmar o espaço disponível (pelo menos 110% do heap em uso), e em produção crítica preferir deixar `HeapDumpOnOutOfMemoryError` fazer o trabalho — o OOM já parou a aplicação, o custo da pausa do dump não importa mais.

---

### (2) Analisar o dump na máquina de produção

**O problema:** Eclipse MAT para analisar um dump de 4 GB precisa de pelo menos 4–8 GB de heap disponível para a própria análise — sem contar as estruturas internas que o MAT constrói (índices, dominator tree). Rodar o MAT no servidor de produção compete diretamente com a aplicação que já está em dificuldade, além de tornar a análise lenta e instável.

**Fix:** copiar o .hprof para uma estação de análise (via `kubectl cp`, `scp`, ou download de bucket de object storage) antes de abrir no MAT. O dump é somente leitura — não precisa ficar no servidor. Em emergências com dumps muito grandes, o MAT tem uma opção de linha de comando para gerar o relatório de leak suspects sem GUI, que pode rodar numa máquina dedicada de análise.

```bash
# hipotético: copiar de pod K8s
kubectl cp <namespace>/<pod>:/mnt/dumps/heap-42.hprof ./heap-42.hprof

# hipotético: copiar de servidor remoto
scp prod-server:/tmp/heap-42.hprof ./heap-42.hprof
```

---

### (3) Esquecer HeapDumpOnOutOfMemoryError (evidência morre com o pod)

**O problema:** sem `-XX:+HeapDumpOnOutOfMemoryError`, quando o OOM ocorre a JVM lança o erro, a stack trace vai para o log (se houver handler), e o processo morre. Em K8s, o pod reinicia e toda a memória some. O único dado disponível é a mensagem de erro — sem saber quais objetos encheram o heap, a investigação começa do zero: code review sem evidência, que é outra forma de adivinhação.

**Fix:** a flag é barata (zero overhead quando não há OOM) e deve ser ligada em toda aplicação de produção. Combinada com `HeapDumpPath` apontando para um volume persistente, garante que mesmo após reinicialização do pod o dump está disponível para análise.

```bash
# hipotético: configuração mínima de segurança para qualquer aplicação de produção
-XX:+HeapDumpOnOutOfMemoryError
-XX:HeapDumpPath=/mnt/dumps/heap-%p.hprof
```

---

### (4) Concluir de um único thread dump ("está travado!")

**O problema:** um único thread dump é um snapshot de um instante. Uma thread aparecendo como `WAITING` pode estar num wait legítimo entre tasks de um executor. Uma thread com um `synchronized` no stack pode ter acabado de entrar e sair na fração de segundo seguinte. Concluir "o serviço está em deadlock" a partir de um único dump é comum e frequentemente errado — e leva a reinicializações desnecessárias que não resolvem a causa raiz.

```text
// hipotético: snapshot infeliz — thread parece travada mas só estava em pausa momentânea
"worker-pool-1" State: WAITING
    at java.lang.Object.wait(...)
    - waiting on <0x...> (a java.util.LinkedList)
// Um único dump não diz se ela ficará assim ou se já continuou
```

**Fix:** coletar uma série de 3 ou mais dumps com intervalo de aproximadamente 10 segundos. Se a thread está no mesmo estado com o mesmo stack frame em todos os dumps, é evidência de travamento real. Se mudou, é processamento normal.

```bash
# hipotético: série de 3 dumps para comparação
for i in 1 2 3; do
  echo "=== dump $i ===" > /tmp/tdump-$i.txt
  jcmd <pid> Thread.print -l >> /tmp/tdump-$i.txt
  sleep 10
done
# comparar os três arquivos: threads imutáveis = problema real
```

## Em entrevista

### Frase pronta (inglês)

> "When I'm dealing with an OOM or suspected memory leak, I always start with the evidence — a heap dump. If the application is still running, I use `jcmd GC.heap_dump` to capture it; if it already died, I check whether `HeapDumpOnOutOfMemoryError` was enabled. That flag is the difference between having the crime scene preserved and having nothing. I then copy the HPROF file off the production machine — never analyze it there — and open it in Eclipse MAT, where the dominator tree tells me which object graph is retaining the most memory and why it's not being collected."

> "For thread issues — deadlock, thread pool exhaustion, a request that never returns — I collect a series of at least three thread dumps spaced about ten seconds apart using `jcmd Thread.print -l`. A single dump is just a snapshot and can be misleading; the pattern across a series is the evidence. If a thread is `BLOCKED` on the same lock owner across all three dumps, that's a real contention or deadlock, not a coincidence."

> "When the process RSS is growing but the Java heap isn't explaining it, I turn to NMT: start the JVM with `-XX:NativeMemoryTracking=summary`, take a baseline with `jcmd VM.native_memory baseline`, let it run, then do `jcmd VM.native_memory summary.diff` to see which subsystem — metaspace, code cache, thread stacks — is growing. That's how you find native memory growth that GC logs and heap dumps don't show."

### Vocabulário

| Termo PT | Termo EN |
|---|---|
| despejo de heap | heap dump |
| despejo de threads | thread dump |
| árvore de dominadores | dominator tree |
| candidatos a vazamento | leak suspects |
| rastreamento de memória nativa | native memory tracking (NMT) |
| tamanho retido | retained size |
| cache sem limite/expiração | unbounded / TTL-less cache |
| thread bloqueada | blocked thread |
| dono do lock | lock owner |
| objeto alcançável | reachable object / live object |
| volume persistente | persistent volume |
| erro de falta de memória | OutOfMemoryError (OOM) |

## Veja também

- [[02 - Áreas de memória de runtime]]
- [[09 - Flags, ergonomics e a JVM em containers]]
- [[10 - GC logs — unified logging e leitura]]
- [[11 - Tuning de GC — metodologia e prática]]
- [[13 - JFR e JMC — observabilidade de produção]]
- [[03-Dominios/Tecnologia/Java/JVM/index|JVM por dentro (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#heap dump|heap dump (Dicionário)]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#jcmd|jcmd (Dicionário)]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#NMT (Native Memory Tracking)|NMT (Dicionário)]]

## Referências

- [jcmd — Java 21 man page (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/specs/man/jcmd.html) — subcomandos confirmados: `GC.heap_dump` (flags `-all`, `-gz`, `-overwrite`; impacto alto), `Thread.print` (flags `-e`, `-l`; impacto médio), `VM.flags` (flag `-all`; impacto baixo), `GC.heap_info` (impacto médio), `VM.native_memory` (opções `summary`, `detail`, `baseline`, `summary.diff`, `detail.diff`, `scale`; impacto médio), `help`
- [java — Java 21 man page (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/specs/man/java.html) — flags confirmadas: `-XX:+HeapDumpOnOutOfMemoryError` (default: desligada), `-XX:HeapDumpPath=<path>` (default: `java_pid<pid>.hprof` no diretório corrente; suporta `%p`), `-XX:NativeMemoryTracking=off|summary|detail`
- [Eclipse Memory Analyzer (MAT)](https://eclipse.dev/mat/) — analisador de heap dumps HPROF; dominator tree, leak suspects, histogram
- [Java Platform, SE 21 Troubleshooting Guide (Oracle)](https://docs.oracle.com/en/java/javase/21/troubleshoot/) — guia geral de troubleshooting Java SE 21
