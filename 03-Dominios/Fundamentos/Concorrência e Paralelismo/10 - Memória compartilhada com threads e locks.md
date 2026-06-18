---
title: "Memória compartilhada com threads e locks"
created: 2026-06-18
updated: 2026-06-18
type: concept
fase: magus
status: evergreen
publish: false
tags:
  - fundamentos
  - concorrencia
  - modelos
  - entrevista
---

# Memória compartilhada com threads e locks

> [!abstract] Resumo em uma linha
> O modelo mais antigo e mais difícil da concorrência: várias threads dividem o mesmo heap e cabe ao programador coordenar cada acesso com locks e atômicos — poder máximo, responsabilidade máxima.

Você já passou pela fase Adepto inteira preparando este momento. Aprendeu o que dá errado quando duas threads tocam o mesmo dado `[[03 - Estado compartilhado e race conditions]]`, aprendeu a serializar o acesso com `[[05 - Exclusão mútua - locks, mutexes e monitores]]`, a coordenar com `[[06 - Semáforos e coordenação]]`, a evitar o lock de vez com `[[08 - Operações atômicas e lock-free]]`, e a temer os patológicos `[[07 - Deadlock, livelock e starvation]]`. Agora a pergunta muda de nível.

Não é mais "como faço um lock funcionar?". É: **isto tudo é UM modelo de concorrência** — uma família de respostas para uma única pergunta de fundo. E existem outros modelos que respondem à mesma pergunta de um jeito radicalmente diferente. Este é o primeiro deles, o dominante, o padrão de fábrica da indústria.

## A cozinha com uma geladeira só

Imagine uma cozinha de restaurante movimentado. Vários cozinheiros (as threads). Uma geladeira só (o heap). Todos podem abrir a geladeira, pegar ingredientes, mexer, devolver. É rápido e flexível — ninguém precisa pedir comida a um garçom intermediário, cada um vai lá e serve-se.

Mas há um problema. Se dois cozinheiros abrem a geladeira ao mesmo tempo para pegar o último ovo, um deles sai de mãos vazias — ou pior, os dois acham que pegaram e a receita quebra lá na frente. Se um cozinheiro está reorganizando uma prateleira enquanto outro lê dela, o segundo vê meia-prateleira. E se dois precisam, cada um, de dois utensílios que o outro já segurou, ninguém solta e a cozinha trava `[[07 - Deadlock, livelock e starvation]]`.

A solução do modelo de memória compartilhada é colocar **cadeados nas prateleiras**. Quem quer mexer numa prateleira pega o cadeado antes, mexe sozinho, e devolve o cadeado depois. É exatamente isso que um `lock` faz. A geladeira continua compartilhada — só o *acesso* a cada região vira exclusivo enquanto durar a operação.

```mermaid
flowchart TB
    subgraph HEAP["Heap compartilhado (uma geladeira)"]
        R1["Região A&lt;br/&gt;protegida por Lock A"]
        R2["Região B&lt;br/&gt;protegida por Lock B"]
        R3["Região C&lt;br/&gt;sem proteção = perigo"]
    end
    T1["Thread 1"] --> R1
    T2["Thread 2"] --> R1
    T3["Thread 3"] --> R2
    T1 -.acesso direto.-> R3
    T2 -.acesso direto.-> R3
    style R3 fill:#5a1a1a,color:#fff
    style HEAP fill:#1a2a3a,color:#fff
```

Lead-in: as setas cheias passam por um lock; as pontilhadas tocam a região C direto.

Leitura do diagrama: três threads dividem um mesmo heap. As regiões A e B têm cadeados — duas threads podem querer A, mas o lock garante que só uma mexe por vez. A região C (vermelha) não tem proteção: qualquer thread toca direto, a qualquer momento. **É ali que mora a race condition.** O modelo não impede o acesso desprotegido — ele só te dá as ferramentas. A disciplina é sua.

> [!tip] O contrato do modelo em uma frase
> Threads compartilham memória mutável; a corretude depende inteiramente de o programador colocar a sincronização certa em cada ponto certo. Nada é protegido por padrão.

## Por que este modelo "venceu" historicamente

Antes de comparar com os outros, vale entender por que este modelo virou o padrão de fábrica — não por mérito de design, mas por uma confluência de hardware, padronização e inércia.

**O hardware era memória compartilhada.** Nos anos 1990 chegaram as máquinas **SMP** (*symmetric multiprocessing*): vários processadores idênticos, sem hierarquia mestre-escravo, todos com acesso igual à mesma RAM. O modelo de software que espelha isso de forma mais barata é justamente threads sobre um heap comum. A abstração não mente sobre a máquina — ela *é* a máquina.

**A padronização criou um vocabulário comum.** O **POSIX threads** (pthreads) foi padronizado pela IEEE (POSIX 1003.1c, raízes em 1988, consolidado em meados dos anos 1990) como uma API em C de tipos e procedimentos para criar e coordenar threads de forma portável e *SMP-aware*. De repente, "criar uma thread", "pegar um mutex", "sinalizar uma variável de condição" tinham nomes iguais em todo Unix. Quem aprendia o modelo numa máquina o levava para qualquer outra.

**As linguagens que herdaram C herdaram o modelo.** Java (1995), C# (2000), C++ com threads padronizadas (C++11) — todas nasceram ou cresceram sobre sistemas operacionais cujo primitivo de concorrência era a thread de SO no estilo pthreads. A escolha já vinha feita pela plataforma. Modelos alternativos (atores, CSP) existiam na academia desde os anos 1970, mas remavam contra a corrente do hardware e do SO.

**A inércia de ecossistema fechou o ciclo.** Uma vez que milhões de linhas, bibliotecas, profilers e desenvolvedores treinados se acumularam sobre threads-e-locks, mudar de modelo virou caro. A maioria das linguagens *nasceu aqui* e a maioria dos programadores aprende concorrência aqui primeiro. Não porque seja o mais seguro — você já viu que é o mais difícil — mas porque foi o caminho que o hardware abriu.

> [!note] "Venceu" entre aspas
> Dominância não é superioridade. Este modelo venceu pela proximidade do silício e pela padronização, não por ser o mais fácil de acertar. Guardar essa distinção é o que separa "uso threads porque é o jeito certo" de "uso threads porque é o jeito padrão — e sei quando trocar".

## Por que este modelo domina (hoje)

Vencida a história, ficam quatro razões técnicas que ainda sustentam a escolha. Não é por acaso que Java, C++, C#, Rust e Kotlin mantêm este modelo no centro.

**Mapeia direto no hardware.** Uma máquina multicore *é* memória compartilhada de verdade — vários núcleos, uma RAM, caches que precisam de coerência. Threads sobre memória compartilhada são o reflexo de software dessa realidade física. Nenhuma camada de abstração mente sobre o que a máquina faz.

**Performance.** Compartilhar um ponteiro custa zero. Não há cópia de mensagem, não há serialização, não há fila intermediária. Para paralelismo CPU-bound de alto desempenho — processar uma matriz gigante dividida entre núcleos — esse é o caminho mais curto entre o dado e o trabalho.

**Controle fino.** Você decide a granularidade do lock, escolhe entre `synchronized` e `ReentrantLock`, troca um lock por um atômico, faz lock-free quando a contenção dói. Nenhum outro modelo te dá essa régua de ajuste.

**Ecossistema maduro.** Décadas de bibliotecas, ferramentas de profiling, detectores de race, padrões de projeto consolidados. `java.util.concurrent` sozinho é uma enciclopédia.

```mermaid
flowchart TB
    APP["Seu código&lt;br/&gt;(quer paralelismo)"]
    THREADS["Threads&lt;br/&gt;(unidade de execução)"]
    SYNC["Sincronização&lt;br/&gt;locks · atômicos · barreiras"]
    MEM["Memória compartilhada&lt;br/&gt;(o heap)"]
    HW["Hardware multicore&lt;br/&gt;(cores + caches + RAM)"]
    APP --> THREADS
    THREADS --> SYNC
    SYNC --> MEM
    MEM --> HW
    style APP fill:#1a3a5a,color:#fff
    style HW fill:#2a4a2a,color:#fff
```

Lead-in: a pilha do modelo, do seu código até o silício.

Leitura do diagrama: seu código pede paralelismo; as threads o executam; a sincronização disciplina o acesso à memória compartilhada; a memória descansa sobre o hardware multicore real. O ponto da figura é que cada camada é fina — quase não há tradução. É por isso que o modelo é rápido. E é por isso, veremos já, que ele é perigoso: nada esconde o estado compartilhado de você.

## Por que é o mais difícil de acertar

A mesma proximidade do hardware que dá performance cobra um preço cruel: **o programador é responsável por TODA a sincronização**. O compilador não te avisa que faltou um lock. O runtime não recusa um acesso desprotegido. O código compila, roda, passa nos testes — e quebra em produção sob carga, num núcleo ARM, uma vez a cada dez milhões de requisições.

Há um consenso na literatura que vale gravar: *shared mutable state is the root of most concurrency bugs*. Os três fantasmas:

- **Race conditions** — a ordem de execução muda o resultado `[[03 - Estado compartilhado e race conditions]]`.
- **Deadlocks** — duas threads esperam para sempre uma pela outra `[[07 - Deadlock, livelock e starvation]]`.
- **Erros de visibilidade** — uma thread escreve, outra nunca enxerga a escrita, porque o valor ficou num cache de núcleo. Este é o mais sorrateiro: não há corrida temporal, há *invisibilidade* de memória.

> [!warning] O bug que esconde o bug
> No x86 a JVM costuma ser mais estrita do que o spec exige, mascarando erros de visibilidade que só apareceriam no ARM. Seu código "funciona" no laptop e morre no servidor. Por isso o modelo de memória `[[11 - Modelos de memória e consistência]]` é o assunto que separa o pleno do sênior.

Note a assimetria com os outros perigos. Uma race tem ao menos a chance de aparecer num teste de estresse. Um erro de visibilidade pode estar correto em 100% dos seus testes e errado na natureza, porque depende do modelo de memória do *processador*, não da sua lógica.

## Showcase: como Java materializa o modelo

Java é o exemplar canônico deste modelo, e o galho dedicado tem toda a mecânica: `[[03-Dominios/Java/Concorrência e paralelismo/index|Concorrência (Java)]]` e `[[Java Concurrency]]`. Aqui o objetivo é outro — mostrar como o *modelo abstrato* vira *concreto* na linguagem, sem repetir o detalhe.

**A unidade de execução: `Thread` e `Runnable`.** O cozinheiro do nosso exemplo. Você descreve o trabalho num `Runnable` e o entrega a uma thread.

```java
Runnable tarefa = () -> processar(lote);
Thread t = new Thread(tarefa);
t.start();   // agora há dois cozinheiros na cozinha
```

**O lock embutido: `synchronized`.** Todo objeto Java carrega um *monitor* intrínseco `[[05 - Exclusão mútua - locks, mutexes e monitores]]`. A palavra `synchronized` pega esse monitor na entrada e solta na saída — o cadeado da prateleira, gratuito em cada objeto.

```java
private int contador = 0;

public synchronized void incrementa() {
    contador++;          // exclusão mútua: um cozinheiro por vez
}
```

**O contrato invisível: o Java Memory Model.** Aqui está o coração da dificuldade. O JMM define quando uma escrita de uma thread fica *visível* para a leitura de outra, via a relação **happens-before**. Sem um elo happens-before entre a escrita e a leitura do mesmo dado, você tem um *data race* — e o resultado é indefinido, não apenas "atrasado". `synchronized`, `volatile` e os atômicos existem tanto para excluir mutuamente quanto para *estabelecer* esses elos. A nota `[[11 - Modelos de memória e consistência]]` trata disso a fundo; basta reter: **o lock não serve só para travar — serve para tornar a escrita visível.**

```java
private volatile boolean pronto = false;
// uma escrita volatile "happens-before" a leitura volatile seguinte:
// a thread leitora enxerga TUDO que a escritora fez antes de pronto = true
```

**A caixa de ferramentas industrial: `java.util.concurrent`.** Quando `synchronized` é grosso demais, o pacote `j.u.c` entrega locks explícitos (`ReentrantLock`, `ReadWriteLock`), atômicos sem lock (`AtomicInteger`, `LongAdder`) `[[08 - Operações atômicas e lock-free]]`, coleções concorrentes (`ConcurrentHashMap`) e *executors* — pools de threads que separam "que trabalho fazer" de "em qual thread fazer", para você não criar threads na mão.

```java
ExecutorService pool = Executors.newFixedThreadPool(8);
pool.submit(() -> processar(lote));   // o pool gerencia os cozinheiros
```

### A virada do Project Loom

Por anos, o calcanhar do modelo Java foi o custo da thread. Uma thread de plataforma é uma thread do SO — pesada, megabytes de pilha, cara de criar. Então a indústria inteira aprendeu a *evitar* threads: pools, callbacks, programação assíncrona reativa `[[14 - Loop de eventos e assincronia]]` — código contorcido só para não pagar o preço da thread.

O **Project Loom**, finalizado no Java 21, mudou o jogo com as **virtual threads**. Uma virtual thread é gerenciada pela JVM, não pelo SO. Consome kilobytes, não megabytes. Quando bloqueia (I/O, lock, sleep), a JVM captura sua continuação, *desmonta* a virtual thread da carrier thread (uma thread de SO real, que nunca bloqueia) e monta outra no lugar. Resultado: você pode ter *milhões* de virtual threads.

> [!important] O que Loom NÃO muda
> Virtual threads continuam no modelo de memória compartilhada. Elas ainda dividem o heap, ainda exigem locks, ainda sofrem race conditions e erros de visibilidade. Loom não troca o modelo — torna barato o estilo "uma thread por tarefa", que o custo das threads de plataforma havia proibido. A dificuldade da sincronização permanece intacta.

```mermaid
sequenceDiagram
    participant Req as Requisição
    participant VT as Virtual thread
    participant CT as Carrier thread (SO)
    participant IO as I/O (rede/disco)
    Req->>VT: chega, cria 1 virtual thread
    VT->>CT: monta na carrier
    VT->>IO: chama operação bloqueante
    Note over VT,CT: JVM desmonta a VT da carrier
    CT->>CT: carrier atende OUTRA virtual thread
    IO-->>VT: I/O completa
    VT->>CT: remonta numa carrier livre
    VT-->>Req: responde
```

Lead-in: o ciclo de uma virtual thread numa requisição que bloqueia em I/O.

Leitura do diagrama: cada requisição ganha sua própria virtual thread — código sequencial, fácil de ler. Quando ela bloqueia em I/O, a JVM a desmonta e libera a carrier (thread de SO real) para atender outra virtual thread. A thread de SO nunca fica parada esperando. Você escreve código simples e bloqueante; a JVM colhe a escalabilidade que antes só o estilo assíncrono dava.

> [!caution] Pinning
> Há um porém: se uma virtual thread bloqueia *dentro* de um bloco `synchronized`, ela fica **pinned** — não pode ser desmontada, e prende a carrier. Em código pesado de virtual threads, prefira `ReentrantLock` a `synchronized` nesses pontos. Mais um detalhe que o modelo de memória compartilhada deixa por sua conta.

## O espectro de abstração dentro do modelo

Aqui está um equívoco caro de iniciante: achar que "memória compartilhada" significa "escrever locks à mão". Não significa. O modelo tem um *espectro de abstração* — da manipulação crua de mutexes até estruturas que escondem toda a sincronização. A regra de ouro do engenheiro experiente é simples: **suba o nível sempre que puder.** Você só desce ao lock manual quando os níveis acima não dão a granularidade ou a performance que o problema exige.

Pense numa escada. Quanto mais alto o degrau, menos sincronização você escreve à mão — e menos chance de errar. Cada degrau ainda está no modelo de memória compartilhada (tudo continua dividindo o heap), mas a coordenação foi *delegada* para código de biblioteca testado por milhões de execuções.

```mermaid
flowchart TB
    L5["Mais ALTO: paralelismo declarativo&lt;br/&gt;parallel streams · fork/join&lt;br/&gt;você diz O QUÊ, não COMO"]
    L4["Tarefas e executors&lt;br/&gt;ExecutorService · Task/TPL · CompletableFuture&lt;br/&gt;trabalho desacoplado da thread"]
    L3["Coleções concorrentes&lt;br/&gt;ConcurrentHashMap · BlockingQueue&lt;br/&gt;sincronização embutida na estrutura"]
    L2["Atômicos e lock-free&lt;br/&gt;AtomicInteger · CAS · std::atomic&lt;br/&gt;sem lock, mas você raciocina sobre ordenação"]
    L1["Mais BAIXO: locks manuais&lt;br/&gt;synchronized · ReentrantLock · pthread_mutex&lt;br/&gt;você pega e solta cada cadeado"]
    L5 --> L4 --> L3 --> L2 --> L1
    style L5 fill:#1a4a2a,color:#fff
    style L1 fill:#5a2a1a,color:#fff
```

Lead-in: a escada de abstração; o topo (verde) esconde a sincronização, a base (vermelha) a expõe.

Leitura do diagrama: no degrau mais baixo você escreve cada `lock`/`unlock` na mão — poder total, risco total. Subindo, os atômicos eliminam o lock mas ainda exigem que você pense em visibilidade `[[04 - Atomicidade, visibilidade e ordenação]]`. Mais acima, as coleções concorrentes embutem a sincronização na própria estrutura: um `ConcurrentHashMap` faz *lock striping* (trava por bucket, não pela tabela inteira) e leitura sem lock, e você nunca toca num mutex. No topo, o paralelismo declarativo (`parallelStream`, fork/join) deixa você dizer *o quê* paralelizar enquanto o runtime decide *como*. Você desce a escada apenas quando precisa — não por padrão.

| Nível | Ferramenta (exemplos) | Você escreve... | Quando descer até aqui |
|---|---|---|---|
| Declarativo | parallel streams, fork/join | "processe esta coleção em paralelo" | quase nunca precisa descer; comece aqui |
| Tarefas/executors | `ExecutorService`, `CompletableFuture`, TPL `Task` | "execute este trabalho num pool" | quando precisa controlar o pool ou compor assíncrono |
| Coleções concorrentes | `ConcurrentHashMap`, `BlockingQueue` | "use esta estrutura thread-safe" | quando o estado compartilhado é uma estrutura de dados |
| Atômicos / lock-free | `AtomicInteger`, CAS, `std::atomic` | "atualize este contador sem lock" | quando a contenção num lock dói e a operação é simples |
| Locks manuais | `synchronized`, `ReentrantLock`, `pthread_mutex` | "pegue e solte este cadeado" | quando precisa de invariantes entre múltiplas variáveis |

> [!tip] A heurística
> Se você está escrevendo um lock à mão, pare e pergunte: existe uma coleção concorrente, um atômico ou um executor que já faz isso? Na maioria dos casos de aplicação, sim. Locks manuais são para quando você protege um *invariante composto* (várias variáveis que precisam mudar juntas), não para proteger uma estrutura que a biblioteca já protege melhor.

## Showcase comparativo: o modelo em quatro linguagens

Java é o exemplar canônico, mas o modelo de memória compartilhada atravessa toda a família de linguagens de sistemas. Comparar como cada uma o materializa revela uma escala de *quanto* a linguagem te protege — culminando no caso que muda o jogo, Rust.

**C++ — o mais cru.** `std::thread` cria a thread, `std::mutex` com `std::lock_guard` (RAII: trava ao construir, destrava ao sair do escopo) faz a exclusão mútua, e `std::atomic` dá operações sem lock. O diferencial perigoso de C++ é o `std::memory_order` explícito: você escolhe à mão o nível de garantia de ordenação (`relaxed`, `acquire`, `release`, `seq_cst`) `[[04 - Atomicidade, visibilidade e ordenação]]`. Poder máximo, zero rede de proteção — um data race em C++ é *undefined behavior* puro.

```cpp
std::mutex m;
int contador = 0;
{
    std::lock_guard<std::mutex> lk(m);  // trava ao construir
    contador++;                          // destrava ao sair do escopo (RAII)
}
```

**C# — o mais ergonômico do .NET.** A palavra `lock(obj)` é açúcar sobre `Monitor.Enter/Exit` — o irmão do `synchronized` de Java. Mas o idioma moderno raramente usa `lock` direto: a **TPL** (*Task Parallel Library*) com `Task`, `Parallel.For` e `async/await` empurra o programador escada acima, para o nível de tarefas e declarativo. Mesmo modelo de memória compartilhada por baixo, abstração alta por cima.

```csharp
lock (trava) { contador++; }          // baixo nível
await Task.Run(() => Processar(lote)); // alto nível (TPL)
```

**Rust — o que muda o jogo.** Aqui está o destaque. Rust oferece o *mesmo* modelo de memória compartilhada (`std::thread`, `Mutex<T>`, `Arc<T>` para compartilhar posse entre threads), mas com uma diferença radical: **o compilador barra data races em tempo de compilação.** É a chamada *fearless concurrency* — concorrência sem medo.

O mecanismo são duas marcas (*marker traits*) que o compilador rastreia automaticamente:

- **`Send`** — um tipo é `Send` se é seguro *transferir a posse* de um valor dele de uma thread para outra.
- **`Sync`** — um tipo é `Sync` se é seguro *compartilhar uma referência* (`&T`) a ele entre threads.

Some isso à regra de *ownership* do Rust — você pode ter *ou* uma referência mutável *ou* várias referências imutáveis a um dado, **nunca as duas ao mesmo tempo** — e o resultado é que a condição básica de um data race (duas threads, uma escrevendo, sem sincronização) simplesmente não compila. O exemplo clássico: `Rc<T>` (contador de referências não-atômico) **não é `Send`**; se você tentar movê-lo para outra thread, o compilador recusa, porque duas threads incrementando o contador concorrentemente seriam um data race. A correção é `Arc<T>` (*atomic* reference count), que é `Send`. Para mutação compartilhada, o padrão idiomático é `Arc<Mutex<T>>`: o `Arc` compartilha a posse entre threads, o `Mutex` serializa o acesso — e o sistema de tipos *te obriga* a pegar o lock antes de tocar no dado, porque o dado só é acessível através do guard do mutex.

```rust
use std::sync::{Arc, Mutex};
use std::thread;

let dado = Arc::new(Mutex::new(0));        // posse compartilhável + lock
let d = Arc::clone(&dado);
thread::spawn(move || {
    let mut n = d.lock().unwrap();         // só acesso o dado VIA o lock
    *n += 1;                                // impossível esquecer de travar
});
```

```mermaid
flowchart TB
    CODE["Código tenta compartilhar&lt;br/&gt;um dado entre threads"]
    CHECK{"O tipo é&lt;br/&gt;Send / Sync?"}
    OK["Compila&lt;br/&gt;(data race impossível)"]
    FAIL["ERRO DE COMPILAÇÃO&lt;br/&gt;'Rc&lt;T&gt; cannot be sent&lt;br/&gt;between threads safely'"]
    FIX["Programador troca por&lt;br/&gt;Arc&lt;Mutex&lt;T&gt;&gt;"]
    CODE --> CHECK
    CHECK -->|"sim"| OK
    CHECK -->|"não"| FAIL
    FAIL --> FIX
    FIX --> CHECK
    style OK fill:#1a4a2a,color:#fff
    style FAIL fill:#5a1a1a,color:#fff
```

Lead-in: o caminho de uma tentativa de compartilhamento pelo verificador de tipos do Rust.

Leitura do diagrama: o compilador intercepta *antes de o programa rodar*. Se o tipo não é `Send`/`Sync`, o build falha com uma mensagem que explica o problema — não há binário com data race para depois caçar em produção. Compare com o modelo de Java: lá, o mesmo erro compila feliz e só talvez apareça sob carga, num núcleo ARM, uma vez a cada dez milhões de requisições `[[04 - Atomicidade, visibilidade e ordenação]]`. Rust move a detecção da madrugada de produção para a tela do editor. É a mesma família de modelo — memória compartilhada com locks — mas com o sistema de tipos como rede de segurança.

> [!important] O que Rust NÃO resolve
> *Fearless concurrency* elimina data races (acesso desprotegido), não *deadlocks* nem *race conditions* lógicas `[[07 - Deadlock, livelock e starvation]]`. Você ainda pode travar dois mutexes em ordens opostas e travar o programa. O compilador garante que todo acesso é sincronizado — não que sua *lógica* de sincronização está certa. É uma rede embaixo de um dos três fantasmas, não dos três.

## Este modelo × os outros quatro

Aqui está a virada de chave conceitual da fase Magus. Memória compartilhada não é "a concorrência" — é *uma resposta* a um problema. E o problema é justamente o estado compartilhado mutável. Os outros modelos são respostas diferentes à *mesma* pergunta: como evitar, esconder ou domar esse estado?

```mermaid
flowchart TB
    PROB["Problema comum:&lt;br/&gt;estado compartilhado mutável&lt;br/&gt;é a raiz dos bugs"]
    PROB --> M1["Memória compartilhada&lt;br/&gt;ABRAÇA o estado,&lt;br/&gt;protege com locks"]
    PROB --> M2["CSP&lt;br/&gt;EVITA: troca dados&lt;br/&gt;por canais"]
    PROB --> M3["Atores&lt;br/&gt;ISOLA: cada ator&lt;br/&gt;tem seu estado"]
    PROB --> M4["Event loop&lt;br/&gt;SERIALIZA: uma thread,&lt;br/&gt;sem disputa"]
    style PROB fill:#5a3a1a,color:#fff
    style M1 fill:#1a3a5a,color:#fff
```

Lead-in: um problema, quatro estratégias.

Leitura do diagrama: todos partem do mesmo mal — estado compartilhado mutável. **Memória compartilhada** o abraça e o protege com sincronização explícita (este é o modelo desta nota). **CSP** `[[12 - Troca de mensagens e CSP]]` diz "não comunique compartilhando memória; compartilhe memória comunicando" — os dados andam por canais. **Atores** `[[13 - O modelo de atores]]` dá a cada ator seu estado privado e só permite mensagens entre eles. **Event loop** `[[14 - Loop de eventos e assincronia]]` simplesmente roda tudo numa thread só, eliminando a disputa pela base. São filosofias distintas; o capstone `[[18 - Concorrência em entrevista]]` compara todas lado a lado.

> [!note] A diferença essencial
> Memória compartilhada é o único modelo que *expõe* o estado compartilhado e te dá ferramentas para protegê-lo. Os outros três o *escondem* atrás de uma abstração — canais, mensagens, ou uma thread única. Por isso são mais seguros por construção, e por isso pagam em performance ou flexibilidade. Não há almoço grátis.

## O custo de coordenação é o limite

Há uma ironia no coração deste modelo. Você usa threads para ganhar paralelismo — mas todo lock que você coloca *desfaz* parte desse paralelismo, porque dentro da seção crítica só uma thread roda por vez. **A trava é, por definição, um gargalo.** Ela serializa o que era paralelo.

Isso conecta direto às leis da escala `[[16 - As leis da escala - Amdahl e Gustafson]]`. A **Lei de Amdahl** diz que o ganho de paralelizar é limitado pela fração *serial* do programa. Cada seção crítica é, exatamente, fração serial: enquanto uma thread segura o lock, os outros núcleos esperam. Adicione núcleos à vontade — a parte serializada pela trava não acelera. Locks grossos (lock da tabela inteira) têm muita fração serial; locks finos (lock striping, um por bucket) têm pouca. É por isso que `ConcurrentHashMap` escala e um `Hashtable` synchronized não.

Dois efeitos pioram isso na prática:

- **Contention (contenção).** Quando muitas threads disputam o mesmo lock, elas passam mais tempo *esperando o lock* do que *trabalhando*. A partir de certo ponto, adicionar threads *piora* o desempenho — você só aumentou a fila na porta do cadeado.
- **False sharing (falso compartilhamento).** Dois dados independentes que por azar caem na mesma linha de cache fazem os núcleos invalidarem o cache um do outro a cada escrita, mesmo sem lock nenhum. É contenção de *hardware*, invisível no código `[[04 - Atomicidade, visibilidade e ordenação]]`.

> [!warning] O paradoxo do lock
> Quanto mais você protege com locks, mais serial fica o programa — e mais Amdahl te pune. O objetivo não é "travar tudo com segurança"; é travar o *mínimo* necessário pela *menor* janela possível. Seção crítica gorda é desempenho jogado fora. Por isso a escada de abstração importa: subir de nível (atômicos, coleções concorrentes) costuma reduzir a fração serial sem você precisar pensar nela.

A consequência estratégica: quando a coordenação domina o tempo de execução — quando as threads passam mais tempo se sincronizando do que trabalhando — o modelo de memória compartilhada parou de te servir. O custo da trava engoliu o ganho do paralelismo.

## Onde brilha × onde evitar

**Brilha quando:**

- O trabalho é **CPU-bound de alto desempenho** — dividir um cálculo pesado entre núcleos, sem o custo de copiar dados entre eles.
- Você precisa de **controle fino** sobre granularidade de lock, layout de memória, estratégias lock-free.
- O ecossistema importa: libs maduras, profilers, padrões consolidados (todo o `java.util.concurrent`).

**Evite quando:**

- **A coordenação domina o trabalho.** Se as threads passam mais tempo disputando locks do que computando, Amdahl já te derrotou `[[16 - As leis da escala - Amdahl e Gustafson]]`. O modelo certo passa a ser o que *elimina* a disputa — confinamento, imutabilidade ou troca de mensagens.
- A complexidade de sincronização **não compensa** o ganho. Se você está lutando contra deadlocks num CRUD, está no modelo errado.
- Você pode usar **confinamento ou imutabilidade** em vez de locks `[[08 - Imutabilidade e estado]]` — dado que vive numa thread só (confinado) ou que nunca muda (imutável) é compartilhável sem sincronização nenhuma, e o JMM até garante *initialization safety* para campos `final` de objetos bem construídos. Estado que não é compartilhado ou que não muda não tem como ter race.
- O problema é I/O-bound ou orientado a coordenação e cabe melhor num **modelo de mais alto nível** — um event loop `[[14 - Loop de eventos e assincronia]]`, atores `[[13 - O modelo de atores]]`, ou CSP `[[12 - Troca de mensagens e CSP]]`, onde a segurança vem de graça com a estrutura porque o estado compartilhado mutável simplesmente não existe.

> [!tip] A regra de ouro
> O melhor estado compartilhado é o que não existe. A segunda melhor opção é o imutável. Lock é a terceira — poderosa, necessária, mas a que mais cobra disciplina. Comece pelo topo da lista.

## Em entrevista

Frame it as a *model* among several, not as "concurrency itself". Say: shared-memory threading is the default model in Java, C++, C#, and Rust because it maps directly onto multicore hardware and gives the finest control and best raw performance. Then name its cost crisply: the programmer is responsible for all synchronization, and *shared mutable state is the root of most concurrency bugs* — races, deadlocks, and silent visibility errors. If asked about Java specifically, connect the dots: `synchronized` and the monitor, the Java Memory Model with its happens-before relationship for visibility, and `java.util.concurrent` for explicit locks and atomics. Mention Project Loom / virtual threads (Java 21) as the recent shift — it keeps the shared-memory model but makes one-thread-per-task cheap, so you write simple blocking code at scale. Add a maturity signal: you rarely hand-write locks — the model is a *spectrum of abstraction*, so you climb to concurrent collections, executors, and parallel streams first and only drop to manual mutexes when you need a composite invariant. Name Rust as the standout: *Send* and *Sync* plus ownership let the compiler reject data races at compile time — "fearless concurrency" — moving the bug from a 3am production incident to your editor, though it still won't save you from deadlocks. And flag the ceiling: every lock serializes, so coordination cost is an Amdahl limit — the lock is a bottleneck, and when coordination dominates work you are in the wrong model. Close by contrasting it with CSP, actors, and the event loop as *different answers to the same problem* of taming shared state. That last move signals senior-level understanding.

### Vocabulário

- memória compartilhada → shared memory
- estado mutável compartilhado → shared mutable state
- threads → threads
- lock / cadeado → lock
- visibilidade → visibility
- relação acontece-antes → happens-before relationship
- modelo de memória → memory model
- thread virtual → virtual thread
- thread portadora → carrier thread
- corrida de dados → data race
- fixação (de thread) → pinning
- pool de threads → thread pool
- concorrência sem medo → fearless concurrency
- marcas Send / Sync → the Send / Sync (marker) traits
- posse / propriedade → ownership
- espectro de abstração → spectrum of abstraction
- divisão de locks (por região) → lock striping
- contenção → contention
- falso compartilhamento → false sharing
- custo de coordenação → coordination cost

> [!info] Lastro
> - Oracle — *Memory Consistency Errors* (Java Tutorials): a relação happens-before como garantia de visibilidade de escritas entre threads. https://docs.oracle.com/javase/tutorial/essential/concurrency/memconsist.html
> - Oracle Java Magazine — *Virtual threads in Java*: virtual threads mantêm o modelo de memória compartilhada do Java; thread-safety e races continuam aplicáveis. https://blogs.oracle.com/javamagazine/java-virtual-threads/
> - Java Code Geeks (2026) — *Java's Memory Model Is Not What You Think*: erros de visibilidade mascarados no x86 que afloram no ARM; o sentido de data race no JMM. https://www.javacodegeeks.com/2026/04/javas-memory-model-is-not-what-you-think-the-gap-between-the-jmm-spec-and-the-jits-actual-guarantees.html
> - Okta Developer — *What the Heck Is Project Loom for Java?*: o modelo de estado compartilhado como padrão do Java e o papel das virtual threads. https://developer.okta.com/blog/2022/08/26/state-of-java-project-loom
> - The Rust Programming Language — *Fearless Concurrency* (cap. 16): `Send`/`Sync` e o sistema de posse transformam erros de concorrência em erros de compilação; `Arc<Mutex<T>>` como padrão de mutação compartilhada. https://doc.rust-lang.org/book/ch16-00-concurrency.html
> - University of Illinois at Chicago — *POSIX Threads and OpenMP (Shared Memory Paradigm)*: pthreads como API SMP-aware padronizada pela IEEE; o modelo de memória compartilhada sobre máquinas SMP. https://www.cs.uic.edu/~ajayk/c566/Presentation_POSIX_OpenMP.pdf
> - Software Patterns Lexicon — *Concurrent Collections in Java*: coleções concorrentes oferecem nível de abstração mais alto que sincronização manual; `ConcurrentHashMap` usa lock striping e leitura sem lock. https://softwarepatternslexicon.com/java/concurrency-and-parallelism-in-java/concurrent-collections/

## Veja também

- `[[01 - Concorrência e paralelismo - o que é e por que é difícil]]` — a pergunta de fundo que todo modelo responde
- `[[03 - Estado compartilhado e race conditions]]` — o perigo central deste modelo
- `[[11 - Modelos de memória e consistência]]` — happens-before e visibilidade a fundo
- `[[12 - Troca de mensagens e CSP]]` — a resposta "evite compartilhar"
- `[[13 - O modelo de atores]]` — a resposta "isole o estado"
- `[[14 - Loop de eventos e assincronia]]` — a resposta "serialize numa thread"
- `[[18 - Concorrência em entrevista]]` — os modelos comparados lado a lado
- `[[03-Dominios/Java/Concorrência e paralelismo/index|Concorrência (Java)]]` — a mecânica completa no exemplar canônico
- `[[03-Dominios/Fundamentos/Concorrência e Paralelismo/index|Concorrência e Paralelismo]]`
