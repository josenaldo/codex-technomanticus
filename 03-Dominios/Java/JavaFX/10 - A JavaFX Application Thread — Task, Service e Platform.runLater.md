---
title: "A JavaFX Application Thread — Task, Service e Platform.runLater"
created: 2026-06-06
updated: 2026-06-06
type: concept
progress: backlog
status: seedling
publish: true
fase: adepto
tags:
  - java
  - javafx
  - adepto
  - threading
aliases:
  - "JavaFX Application Thread"
  - "Task Service"
  - "Platform.runLater"
---

# A JavaFX Application Thread — Task, Service e Platform.runLater

> [!abstract] TL;DR
> O scene graph do JavaFX só pode ser tocado pela **JavaFX Application Thread** (a "FX thread") — a mesma regra single-thread do EDT do Swing, com outro nome. Trabalho pesado (I/O, cálculo) vai para um **`Task<V>`**, cujo `call()` roda em background. A vantagem estrutural sobre o `SwingWorker` é que o `Task` expõe `progressProperty()`, `messageProperty()` e `valueProperty()` **bindáveis** — você liga a barra de progresso e o label de status à Task com uma linha de `bind`, sem callback manual. Os métodos `updateProgress`/`updateMessage`/`updateValue` são seguros de chamar de qualquer thread e **coalescem** atualizações na FX thread. **`Platform.runLater`** é a válvula para voltar à FX thread quando você não tem uma property bindável à mão; **`Service`** é o `Task` reusável (`restart`/`reset`/`setExecutor`); **`ScheduledService`** repete em período com backoff.

## O que é

O JavaFX é um toolkit **single-threaded**: existe uma única thread — a *JavaFX Application Thread* — que processa eventos de UI, executa os handlers e renderiza o scene graph. Tudo que toca a cena (criar ou alterar `Node`s já anexados, mexer no `Stage`, mudar propriedades visuais) tem que acontecer nela. O método `start(Stage)` da sua `Application` já é chamado nessa thread; daí em diante, todo handler de evento também roda nela.

Disso decorre uma tensão: a FX thread não pode bloquear (senão a UI congela), mas a maior parte do trabalho útil — ler um arquivo, chamar uma API, processar um lote — é demorada. A solução é mover esse trabalho para uma thread de background e devolver só o *resultado* à FX thread. A família **`javafx.concurrent`** (no módulo `javafx.graphics`) existe exatamente para coreografar essa ida-e-volta:

- **`Worker<V>`** — a interface base: algo que executa em background e expõe estado/progresso/valor observáveis.
- **`Task<V>`** — implementação one-shot de `Worker`. Você escreve o `call()`.
- **`Service<V>`** — um `Worker` reusável que fabrica `Task`s sob demanda.
- **`ScheduledService<V>`** — um `Service` que se reinicia periodicamente.

E, por baixo de tudo, **`Platform.runLater(Runnable)`** e **`Platform.isFxApplicationThread()`**, as primitivas que respectivamente *enfileiram* trabalho na FX thread e *perguntam* se você já está nela.

## Por que importa

Violar a regra é caro de duas formas. Na melhor das hipóteses, o JavaFX detecta o acesso fora da thread e lança `IllegalStateException: Not on FX application thread` — um crash ruidoso, mas honesto. Na pior, a alteração passa sem checagem e corrompe o estado interno do scene graph de forma silenciosa: glitches de renderização, nós que somem, travamentos intermitentes que não reproduzem. O bug que *crasha* é o sortudo.

O lado oposto também queima: se você roda I/O na FX thread, a aplicação **congela** — o cursor vira ampulheta, a janela para de repintar, nem o spinner que deveria indicar "carregando" anda, porque o loop de animação que move o spinner também é a FX thread, e ela está bloqueada esperando o I/O. "Por que minha UI trava enquanto carrega?" é *a* pergunta de threading em entrevista de desktop, e a resposta correta combina as duas metades: nunca toque a cena fora da FX thread, e nunca bloqueie a FX thread.

A **teoria de por que** UI toolkits são single-threaded — o modelo de affinity de thread, por que locks no scene graph seriam piores que a regra — já foi estabelecida no Galho 5, em [[03-Dominios/Java/Swing/05 - A Event Dispatch Thread|A Event Dispatch Thread]]. Esta nota assume essa teoria e aplica a regra ao vocabulário do JavaFX. A novidade aqui não é o *porquê* (idêntico ao Swing), e sim o *como*: o JavaFX expõe o trabalho em background como properties bindáveis, fechando o ciclo com o modelo reativo da nota [[07 - Properties e binding]].

## Como funciona

### A regra e a thread

A regra, na forma mais curta: **só a FX Application Thread pode tocar a cena**. "Tocar a cena" inclui mais do que parece à primeira vista:

- alterar propriedades de qualquer `Node` **já anexado** a uma `Scene` (texto de um `Label`, itens de um `TableView`, `disable`/`visible`);
- mexer no `Stage` ou na `Scene` (título, tamanho, `show()`/`hide()`);
- adicionar ou remover filhos de um container que já está na cena.

Construir nós *soltos* (ainda não anexados) em background é tecnicamente tolerável, mas a fronteira é escorregadia e não vale o risco — a regra prática é: **construa e altere UI sempre na FX thread**.

Para checar onde você está, o JavaFX dá `Platform.isFxApplicationThread()`, que retorna `true` se a thread chamadora é a FX thread. O Javadoc descreve o uso como *"ensure that a given task is being executed (or not being executed) on the JavaFX Application Thread"* — útil em asserts e em código de biblioteca que pode ser chamado de qualquer lado.

```java
assert Platform.isFxApplicationThread() : "deve rodar na FX thread";
label.setText("pronto");
```

### Platform.runLater

`Platform.runLater(Runnable)` **enfileira** o `Runnable` para rodar na FX thread *"at some unspecified time in the future"*. É a válvula universal: de qualquer thread de background, você empacota a atualização de UI num runnable e o agenda.

```java
new Thread(() -> {
    String resultado = servico.buscarBloqueante();   // background, ok bloquear
    Platform.runLater(() -> label.setText(resultado)); // volta à FX thread
}).start();
```

Use `runLater` quando você tem uma atualização **pontual** e não há uma property bindável envolvida. Quando **não** usar: rajadas em loop apertado. O próprio Javadoc avisa que *"applications should avoid flooding JavaFX with too many pending Runnables. Otherwise, the application may become unresponsive."* — a recomendação é agrupar várias operações em menos chamadas e deixar trabalho longo no background. Um loop que dispara `runLater` a cada iteração inunda a fila e engasga a UI. Para progresso contínuo, prefira as `updateXxx` do `Task`, que **coalescem** por você (próxima seção).

### Task&lt;V&gt;

`Task<V>` é a peça central. Você estende e implementa o método abstrato `call()`, que **roda na thread de background**:

```java
protected abstract V call() throws Exception;
```

O `Task` expõe um conjunto de properties **read-only e bindáveis**, herdadas de `Worker`:

| Property | Tipo | Para quê |
|---|---|---|
| `progressProperty()` | `ReadOnlyDoubleProperty` | 0.0–1.0 (ou -1 = indeterminado) |
| `messageProperty()` | `ReadOnlyStringProperty` | status textual |
| `valueProperty()` | `ReadOnlyObjectProperty<V>` | resultado, preenchido ao suceder |
| `stateProperty()` | `ReadOnlyObjectProperty<Worker.State>` | READY/SCHEDULED/RUNNING/SUCCEEDED/FAILED/CANCELLED |
| `exceptionProperty()` | `ReadOnlyObjectProperty<Throwable>` | a exceção, se falhou |
| `runningProperty()` | `ReadOnlyBooleanProperty` | conveniência para `disable`/spinner |
| `workDoneProperty()` / `totalWorkProperty()` | `ReadOnlyDoubleProperty` | progresso bruto |

Como são `ObservableValue`s, você **liga a UI a elas** — é aqui que o galho fecha com [[07 - Properties e binding]]:

```java
progressBar.progressProperty().bind(task.progressProperty());
statusLabel.textProperty().bind(task.messageProperty());
```

Para *publicar* progresso de dentro do `call()`, o `Task` oferece métodos protegidos: `updateProgress(workDone, max)`, `updateMessage(String)`, `updateValue(V)` e `updateTitle(String)`. Eles têm duas garantias que o Javadoc cravam e que matam dois problemas de uma vez:

1. **São seguros de chamar de qualquer thread.** Cada um é marcado *"This method is safe to be called from any thread."* — você os chama de dentro do `call()` (background) sem `runLater`.
2. **Coalescem.** O Javadoc: *"Calls to updateProgress are coalesced and run later on the FX application thread, and ... intermediate workDone values may be coalesced to save on event notifications."* A mesma linguagem vale para `updateMessage`/`updateValue`/`updateTitle`. Ou seja, mesmo que seu loop chame `updateProgress` um milhão de vezes, o JavaFX não dispara um milhão de notificações na FX thread — ele junta e atualiza a property o suficiente para a UI acompanhar. Isso é exatamente o que `Platform.runLater` em loop *não* faz, e por isso `updateXxx` é a forma correta de reportar progresso.

O Javadoc é restritivo sobre o que pode ser tocado dentro do `call()`: *"Only the updateProgress, updateMessage, updateValue and updateTitle methods of Task may be called from code within this method."* Nada de `label.setText(...)` lá dentro.

Para reagir ao fim, registre handlers de transição de estado — eles rodam **na FX thread**, então podem tocar a UI à vontade:

```java
task.setOnSucceeded(e -> tabela.setItems(task.getValue()));
task.setOnFailed(e -> mostrarErro(task.getException()));
```

Há ainda `setOnRunning`, `setOnScheduled` e `setOnCancelled`.

### Task vs SwingWorker

O `SwingWorker` (Galho 5, [[03-Dominios/Java/Swing/06 - SwingWorker e tarefas em background|SwingWorker e tarefas em background]]) resolve o mesmo problema com um modelo **imperativo**: você faz `publish(chunk)` de dentro do `doInBackground()`, e o framework chama `process(List<chunk>)` na EDT, onde você escreve o código que empurra os dados para os controls — e lê o resultado final no `done()` via `get()`. Funciona, mas você escreve a ponte à mão em cada caso.

O `Task` é **declarativo/reativo**: em vez de `publish`/`process`, você expõe properties e a UI se *liga* a elas. A diferença estrutural:

| | SwingWorker | Task |
|---|---|---|
| Progresso | `setProgress(int)` + `PropertyChangeListener` | `updateProgress` + `progressProperty().bind(...)` |
| Resultados parciais | `publish`/`process(List)` | `updateValue` + `valueProperty()` (último valor) |
| Resultado final | `done()` + `get()` | `setOnSucceeded` + `getValue()` |
| Erro | `get()` lança `ExecutionException` | `setOnFailed` + `getException()` |
| Ligação à UI | imperativa, escrita à mão | `bind`, uma linha |

O ganho do `Task` é que a UI e o trabalho ficam acoplados por *binding*, não por código de cola — menos linhas, menos lugares onde esquecer um caso. (`SwingWorker` não tem property bindável porque o Swing não tem properties; ver [[07 - Properties e binding]] para a base que falta lá.)

### Service&lt;V&gt;

Um `Task` é **one-shot**: o Javadoc é explícito — *"As with FutureTask, a Task is a one-shot class and cannot be reused."* Para trabalho que precisa rodar de novo (um botão "atualizar"), use `Service<V>`. Você implementa o método abstrato `createTask()`, que **fabrica um `Task` novo a cada execução** (e roda na FX thread):

```java
protected abstract Task<V> createTask();
```

O `Service` expõe as mesmas properties bindáveis do `Task` (progress/message/value/state/exception/running) e adiciona ciclo de vida reusável:

- **`start()`** — inicia (exige estado READY).
- **`restart()`** — *"Cancels any currently running Task, if any, and restarts this Service. The state will be reset to READY prior to execution."* É o método do dia-a-dia: clicou em "atualizar", chama `restart()`.
- **`reset()`** — *"May only be called while in one of the finish states ... SUCCEEDED, FAILED, or CANCELLED, or when READY."* Volta ao READY sem disparar.
- **`cancel()`** — cancela o `Task` corrente; estado vai para CANCELLED.
- **`setExecutor(Executor)`** — **onde você pluga seu pool**. Sem executor, o Javadoc diz que *"a new daemon thread will be created"* por um executor default. Com `setExecutor`, você roda as Tasks num `ThreadPoolExecutor` seu (com `ThreadFactory`, limites etc.).

### ScheduledService

`ScheduledService<V>` é um `Service` que **se reinicia sozinho** após cada execução bem-sucedida — feito para *polling* (pingar um servidor de tempos em tempos). As properties que governam o ritmo:

- **`period`** — *"the minimum amount of time to allow between the start of the last run and the start of the next run"*. Terminou antes? Espera o período. Demorou mais? Reinicia já.
- **`delay`** — espera inicial antes da primeira execução.
- **`restartOnFailure`** — se reinicia após falha (sujeito ao backoff e ao `maximumFailureCount`).
- **`maximumFailureCount`** — atingido o teto, o serviço vai a FAILED em definitivo.
- **`backoffStrategy`** — um `Callback` que, após cada falha, computa o novo `cumulativePeriod`: *"the result of calling backoffStrategy will become the new cumulativePeriod."* Há estratégias prontas (linear, logarítmica — a default — e exponencial).
- **`lastValue`** — guarda o último resultado bem-sucedido (o `value` "comum" reseta entre iterações).

Em uma linha: `ScheduledService` é polling com backoff embutido, sem você escrever um `Timer` + retry à mão.

### Cancelamento cooperativo

`cancel()` sinaliza o cancelamento, mas o JavaFX **não interrompe à força** o seu `call()` — o cancelamento é *cooperativo*. O corpo do `call()` precisa **checar `isCancelled()`** em pontos estratégicos e sair limpo:

```java
@Override
protected Integer call() {
    int soma = 0;
    for (int i = 0; i < total; i++) {
        if (isCancelled()) {
            break;            // respeita o pedido de cancelamento
        }
        soma += processar(i);
        updateProgress(i + 1, total);
    }
    return soma;
}
```

Se o `call()` faz uma chamada bloqueante interruptível, um `InterruptedException` pode chegar — capture-o e re-cheque `isCancelled()` em vez de engolir. Sem essas checagens, `cancel()` muda o *estado* para CANCELLED mas o trabalho continua rodando inutilmente no background.

### Virtual threads e JavaFX

Virtual threads (Galho 4, [[03-Dominios/Java/Concorrência e paralelismo/12 - Virtual Threads e Project Loom|Virtual Threads e Project Loom]]) mudam *onde* roda o `call()`, não a regra da FX thread. Para Tasks **I/O-bound** (muitas chamadas de rede simultâneas), rodá-las num executor de virtual threads dá escala barata sem amarrar threads de plataforma:

```java
Executor vthreads = Executors.newVirtualThreadPerTaskExecutor();
service.setExecutor(vthreads);   // as Tasks do Service rodam em virtual threads
// ou, para um Task avulso:
vthreads.execute(task);
```

O ponto crítico: **a regra da FX thread não muda**. A FX Application Thread continua sendo uma thread de plataforma única, e tocar a cena de dentro de uma virtual thread é tão ilegal quanto de qualquer outra. Virtual threads aceleram o *background*; a fronteira de volta à UI continua sendo `bind`/`updateXxx`/`runLater`. (Não re-explico Loom aqui — ver a nota do Galho 4.)

## Na prática

Um `Task` que carrega pedidos simulando I/O, com a UI ligada por binding e o resultado populando uma `TableView` (conecta com [[08 - TableView, cell factories e dados observáveis]]).

```java
package com.example;

import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.concurrent.Task;

public class LoadOrdersTask extends Task<ObservableList<Order>> {

    private final OrderRepository repo;

    public LoadOrdersTask(OrderRepository repo) {
        this.repo = repo;
    }

    @Override
    protected ObservableList<Order> call() throws Exception {
        ObservableList<Order> result = FXCollections.observableArrayList();
        int total = repo.count();

        updateMessage("Carregando pedidos...");
        for (int i = 0; i < total; i++) {
            if (isCancelled()) {
                updateMessage("Cancelado");
                break;
            }
            result.add(repo.fetchOne(i));   // simula I/O por item
            updateProgress(i + 1, total);   // coalescido na FX thread
        }
        updateMessage("Concluído: " + result.size() + " pedidos");
        return result;
    }
}
```

Ligando a Task à UI e disparando-a. As properties da Task vão direto para os controls; `setOnSucceeded` (que roda na FX thread) popula a tabela:

```java
LoadOrdersTask task = new LoadOrdersTask(repo);

// binding: a UI espelha a Task sem nenhum callback manual
progressBar.progressProperty().bind(task.progressProperty());
statusLabel.textProperty().bind(task.messageProperty());
loadButton.disableProperty().bind(task.runningProperty());

// handlers de transição rodam na FX thread -> podem tocar a cena
task.setOnSucceeded(e -> ordersTable.setItems(task.getValue()));
task.setOnFailed(e -> {
    statusLabel.textProperty().unbind();  // solta o bind antes de setar
    statusLabel.setText("Falha: " + task.getException().getMessage());
});

// dispara em background — virtual thread é idiomático para I/O-bound
Thread.ofVirtual().start(task);
```

> [!note] Sobre o disparo
> `Thread.ofVirtual().start(task)` é o idiomático para carga **I/O-bound** em Java 21+. Em código de produção com muitas tarefas, prefira um `Service` com `setExecutor(...)` apontando para um pool reusável — o `Service` evita recriar a infraestrutura a cada clique. O trecho acima é ilustrativo.

Um `Service` de refresh, com o pool plugado e `restart()` no botão:

```java
public class OrderRefreshService extends Service<ObservableList<Order>> {

    private final OrderRepository repo;

    public OrderRefreshService(OrderRepository repo) {
        this.repo = repo;
        // pluga um pool de virtual threads como executor das Tasks
        setExecutor(Executors.newVirtualThreadPerTaskExecutor());
    }

    @Override
    protected Task<ObservableList<Order>> createTask() {
        return new LoadOrdersTask(repo);   // Task NOVA a cada execução
    }
}

// uso:
OrderRefreshService service = new OrderRefreshService(repo);
ordersTable.itemsProperty().bind(service.valueProperty()); // itemsProperty é uma ObjectProperty bindável
refreshButton.setOnAction(e -> service.restart());         // reusa: cancela a corrente e roda de novo
```

O **contraexemplo** — tocar um `Label` de dentro do `call()`, fora da FX thread:

```java
@Override
protected Void call() {
    String dados = repo.fetchAll();
    statusLabel.setText(dados);   // ERRADO: setText fora da FX thread
    return null;
}
```

A exceção real, lançada no background:

```text
java.lang.IllegalStateException: Not on FX application thread; currentThread = pool-1-thread-1
    at javafx.graphics/com.sun.javafx.tk.Toolkit.checkFxUserThread(Toolkit.java:303)
    at javafx.graphics/javafx.scene.Scene.setRoot(Scene.java:1389)
    at javafx.controls/javafx.scene.control.Labeled.setText(Labeled.java:145)
```

O conserto é não tocar a UI no `call()`: publique via `updateMessage(dados)` e ligue `statusLabel.textProperty()` à `messageProperty()`; ou, se for atualização pontual, `Platform.runLater(() -> statusLabel.setText(dados))`.

## Armadilhas

### (1) Tocar a UI dentro de call()

**Problema:** qualquer `setText`/`setItems`/`getChildren().add(...)` em um `Node` anexado, executado dentro do `call()`, roda na thread de background e lança `IllegalStateException: Not on FX application thread` (ou, pior, corrompe a cena em silêncio).

```java
protected Void call() {
    var dados = repo.fetchAll();
    listView.getItems().setAll(dados);   // PROBLEMA: fora da FX thread
    return null;
}
```

**Fix:** publique o estado via property do Task e ligue a UI por binding; ou use os handlers de transição (que rodam na FX thread); ou, para algo pontual, `Platform.runLater`.

```java
protected ObservableList<String> call() {
    return FXCollections.observableArrayList(repo.fetchAll());
}
// fora:
task.setOnSucceeded(e -> listView.setItems(task.getValue()));
```

---

### (2) Bloquear a FX thread

**Problema:** rodar I/O ou cálculo pesado direto no handler de um botão bloqueia a FX thread. A UI congela inteira — nem o spinner que você mostrou para indicar "carregando" anda, porque a animação dele também é a FX thread.

```java
loadButton.setOnAction(e -> {
    spinner.setVisible(true);
    var dados = repo.fetchAllBlocking();  // PROBLEMA: bloqueia a FX thread
    table.setItems(dados);                // o spinner nunca chegou a animar
});
```

**Fix:** mova o trabalho para um `Task` em background; ligue o spinner a `runningProperty()`; popule no `setOnSucceeded`.

```java
LoadTask task = new LoadTask(repo);
spinner.visibleProperty().bind(task.runningProperty());
task.setOnSucceeded(e -> table.setItems(task.getValue()));
Thread.ofVirtual().start(task);
```

---

### (3) Platform.runLater em loop apertado

**Problema:** disparar `runLater` a cada iteração de um loop empilha milhares de runnables na fila da FX thread. O Javadoc avisa: *"avoid flooding JavaFX with too many pending Runnables. Otherwise, the application may become unresponsive."* A UI engasga.

```java
for (int i = 0; i < 1_000_000; i++) {
    int progresso = i;
    Platform.runLater(() -> bar.setProgress(progresso / 1_000_000.0)); // PROBLEMA: inunda a fila
}
```

**Fix:** dentro de um `Task`, use `updateProgress`/`updateMessage`, que **coalescem** automaticamente — milhares de chamadas viram poucas notificações na FX thread. Fora de um Task, acumule e atualize uma vez (ou em intervalos), não a cada iteração.

```java
for (int i = 0; i < 1_000_000; i++) {
    updateProgress(i + 1, 1_000_000);   // coalescido pelo Task
}
```

---

### (4) Esquecer setOnFailed

**Problema:** se o `call()` lança uma exceção e você só registrou `setOnSucceeded`, a falha morre **em silêncio** — o estado vai a FAILED, mas nada na UI reage, e a exceção fica presa em `exceptionProperty()` sem ninguém olhar. O usuário vê um spinner que some e nenhum dado.

```java
task.setOnSucceeded(e -> table.setItems(task.getValue()));
// nenhum setOnFailed: se call() lança, ninguém fica sabendo
```

**Fix:** sempre trate o caminho de falha — `setOnFailed` lendo `getException()`, ou um binding/listener em `exceptionProperty()`.

```java
task.setOnFailed(e -> {
    Throwable ex = task.getException();
    log.error("falha ao carregar", ex);
    statusLabel.setText("Erro: " + ex.getMessage());
});
```

---

### (5) Reusar uma Task

**Problema:** `Task` é one-shot. Tentar rodar a *mesma* instância de novo (segundo clique no botão "atualizar") não funciona — o Javadoc é explícito: *"a Task is a one-shot class and cannot be reused."* O estado já está em SUCCEEDED/FAILED e a Task não re-executa.

```java
LoadTask task = new LoadTask(repo);
Thread.ofVirtual().start(task);
// ... mais tarde, no clique de "atualizar":
Thread.ofVirtual().start(task);   // PROBLEMA: mesma Task, não roda de novo
```

**Fix:** para trabalho repetível, use `Service`, que fabrica um `Task` novo a cada `restart()`.

```java
Service<List<Order>> service = new OrderRefreshService(repo);
refreshButton.setOnAction(e -> service.restart());  // Task nova a cada clique
```

## Em entrevista

### Frase pronta (inglês)

> "JavaFX is single-threaded: the scene graph can only be touched on the JavaFX Application Thread, which is exactly the same constraint as Swing's EDT, just renamed. So long-running work — I/O, computation — goes on a background thread via a `Task`, whose `call()` method runs off the FX thread. What makes `Task` nicer than Swing's `SwingWorker` is that it exposes bindable read-only properties — `progressProperty`, `messageProperty`, `valueProperty` — so I bind the progress bar and status label straight to the task instead of writing publish/process glue by hand. Inside `call()` I report progress with `updateProgress` and `updateMessage`, which are safe to call from any thread and coalesce updates onto the FX thread; I never touch UI controls directly there. When I need a one-off jump back to the FX thread without a property, I use `Platform.runLater`, but I avoid flooding it in a tight loop. For repeatable work I use a `Service`, which creates a fresh `Task` on each `restart()` and lets me plug in my own executor — increasingly a virtual-thread executor for I/O-bound work, though that never changes the FX-thread rule."

### Vocabulário

| Termo PT | Termo EN |
|---|---|
| thread de UI / thread da aplicação | UI thread / application thread |
| grafo de cena | scene graph |
| trabalho em segundo plano | background work |
| ligação (binding) | binding |
| coalescer (agrupar atualizações) | to coalesce updates |
| cancelamento cooperativo | cooperative cancellation |
| handler de transição de estado | state-transition handler |
| tarefa de uso único / reusável | one-shot / reusable task |
| executor / pool de threads | executor / thread pool |
| enfileirar na thread de UI | marshal onto the UI thread |

## Veja também

- [[05 - Eventos — capturing, bubbling e handlers]]
- [[07 - Properties e binding]]
- [[08 - TableView, cell factories e dados observáveis]]
- [[03-Dominios/Java/Swing/05 - A Event Dispatch Thread|A Event Dispatch Thread (Swing)]]
- [[03-Dominios/Java/Swing/06 - SwingWorker e tarefas em background|SwingWorker (Swing)]]
- [[03-Dominios/Java/Concorrência e paralelismo/12 - Virtual Threads e Project Loom|Virtual Threads]]
- [[03-Dominios/Java/JavaFX/index|JavaFX (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Dicionário de Java#JavaFX Application Thread|JavaFX Application Thread (Dicionário)]]
- [[03-Dominios/Java/Dicionário de Java#Platform.runLater|Platform.runLater (Dicionário)]]
- [[03-Dominios/Java/Dicionário de Java#Task / Service (JavaFX)|Task / Service (Dicionário)]]

## Referências

- [Task — OpenJFX 21 Javadoc](https://openjfx.io/javadoc/21/javafx.graphics/javafx/concurrent/Task.html) — módulo `javafx.graphics`, pacote `javafx.concurrent`; properties bindáveis (progress/message/value/state/exception/running/workDone/totalWork); `updateProgress`/`updateMessage`/`updateValue`/`updateTitle` "safe to be called from any thread" e coalescência ("Calls to updateProgress are coalesced and run later on the FX application thread... intermediate workDone values may be coalesced"); `call()` em background e restrição de só chamar as `updateXxx` dentro dele; handlers `setOnSucceeded`/`setOnFailed`/etc.; cancelamento via `isCancelled()`; one-shot ("a Task is a one-shot class and cannot be reused")
- [Service — OpenJFX 21 Javadoc](https://openjfx.io/javadoc/21/javafx.graphics/javafx/concurrent/Service.html) — `createTask()` na FX thread; `restart()` ("Cancels any currently running Task... state will be reset to READY"); `reset()` (só nos estados finais ou READY); `setExecutor`/`getExecutor` (sem executor, "a new daemon thread will be created"); reusável
- [ScheduledService — OpenJFX 21 Javadoc](https://openjfx.io/javadoc/21/javafx.graphics/javafx/concurrent/ScheduledService.html) — `period` ("minimum amount of time to allow between the start of the last run and the start of the next run"), `delay`, `restartOnFailure`, `maximumFailureCount`, `backoffStrategy` ("the result of calling backoffStrategy will become the new cumulativePeriod"), `cumulativePeriod`, `lastValue`; estratégias linear/logarítmica/exponencial
- [Platform — OpenJFX 21 Javadoc](https://openjfx.io/javadoc/21/javafx.graphics/javafx/application/Platform.html) — `runLater(Runnable)` (executa na FX thread "at some unspecified time in the future"; "avoid flooding JavaFX with too many pending Runnables. Otherwise, the application may become unresponsive."); `isFxApplicationThread()`
