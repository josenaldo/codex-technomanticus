---
title: "SwingWorker e tarefas em background"
created: 2026-06-03
updated: 2026-06-03
type: concept
progress: backlog
status: seedling
publish: true
fase: adepto
tags:
  - java
  - swing
  - adepto
  - swingworker
  - threading
aliases:
  - SwingWorker
  - Tarefas em background
---

# SwingWorker e tarefas em background

> [!abstract] TL;DR
> `SwingWorker<T,V>` é a forma idiomática de alto nível de fazer trabalho de background numa app Swing sem violar a [[03-Dominios/Java/Swing/05 - A Event Dispatch Thread|EDT]]. Ele encapsula o padrão "trabalho pesado fora da EDT, atualização da UI dentro da EDT": você implementa `doInBackground`, que **roda numa worker thread** (onde o I/O lento mora), e os métodos `process` e `done` **rodam na EDT** (onde você toca os componentes com segurança). O parâmetro **`T` é o tipo do resultado final** (devolvido por `doInBackground` e `get`); **`V` é o tipo dos resultados intermediários** que você emite com `publish` e recebe em `process`. Progresso vai pela bound property `progress` (`setProgress`/`getProgress`/`PropertyChangeListener`); cancelamento por `cancel`/`isCancelled`. A regra de ouro de uso: **leia o resultado em `done()` com `get()` dentro de um `try/catch`** — nunca chame `get()` direto na EDT (bloqueia tudo) e nunca toque um componente dentro de `doInBackground`. Os pools de threads por baixo são os [[03-Dominios/Java/Concorrência e paralelismo/08 - Executors e thread pools|executors]] do galho de concorrência.

## O que é

`SwingWorker<T,V>` é uma classe abstrata que serve de **ponte entre uma worker thread e a EDT**. Ela existe para resolver, de forma encapsulada, a tensão central do [[03-Dominios/Java/Swing/05 - A Event Dispatch Thread|modelo single-threaded do Swing]]: o trabalho demorado não pode rodar na EDT (congela a UI), mas a atualização dos componentes só pode acontecer na EDT (tocar componente fora dela é corrupção intermitente). `SwingWorker` costura as duas pontas.

A assinatura da classe é parametrizada por dois tipos:

```java
public abstract class SwingWorker<T,V> implements RunnableFuture<T>
```

- **`T`** — *"the result type returned by this `SwingWorker`'s `doInBackground` and `get` methods"*. É o tipo do **resultado final** da tarefa.
- **`V`** — *"the type used for carrying out intermediate results by this `SwingWorker`'s `publish` and `process` methods"*. É o tipo dos **resultados intermediários** (cada "chunk" publicado durante o processamento).

Quando a tarefa não devolve resultado, usa-se `Void` para `T`; quando ela não publica nada incremental, usa-se `Void` para `V`. Um worker que carrega uma `List<Registro>` publicando o progresso por linha seria `SwingWorker<List<Registro>, Registro>`.

Como `SwingWorker` implementa `java.util.concurrent.Future`, o resultado de background fica acessível por `get()` — o mesmo contrato de qualquer `Future`. A diferença é que `SwingWorker` cuida do *handoff* de volta para a EDT: o tutorial resume que *"The background task can provide intermediate results by invoking `SwingWorker.publish`, causing `SwingWorker.process` to be invoked from the event dispatch thread."*

## Como funciona

### O ciclo: `doInBackground` roda no worker; `done` e `process` rodam na EDT

A divisão de threads é o coração do `SwingWorker` e a parte que mais cai em entrevista. Há **uma fronteira clara**:

| Método | Assinatura | Onde roda |
|--------|-----------|-----------|
| `doInBackground` | `protected abstract T doInBackground() throws Exception` | **worker thread** |
| `publish` | `protected final void publish(V... chunks)` | worker thread (chamado de dentro de `doInBackground`) |
| `process` | `protected void process(List<V> chunks)` | **EDT** |
| `done` | `protected void done()` | **EDT** |

O Javadoc é explícito sobre cada um:

- `doInBackground` — *"Computes a result, or throws an exception if unable to do so. Note that this method is executed only once."* Roda fora da EDT; é aqui que vai todo o I/O e cálculo pesado. **Nunca** toque componentes Swing daqui.
- `done` — *"Executed on the Event Dispatch Thread after the `doInBackground` method is finished."* É o ponto seguro para ler o resultado e atualizar a UI ao final.
- `process` — *"Receives data chunks from the `publish` method asynchronously on the Event Dispatch Thread."* É o ponto seguro para atualizar a UI **durante** o processamento.

Você dispara o worker com `execute()`:

```java
public final void execute()  // agenda este SwingWorker numa worker thread
```

O Javadoc: *"Schedules this `SwingWorker` for execution on a worker thread. There are a number of worker threads available. In the event all worker threads are busy handling other `SwingWorkers` this `SwingWorker` is placed in a waiting queue."* Esse pool de worker threads é exatamente um [[03-Dominios/Java/Concorrência e paralelismo/08 - Executors e thread pools|executor / thread pool]] gerenciado pelo Swing — os primitivos por baixo (filas de tarefas, número de threads, enfileiramento) são os do galho [[03-Dominios/Java/Concorrência e paralelismo/index|Concorrência e paralelismo]]; aqui só importa que o trabalho cai em *alguma* thread que não é a EDT.

> [!warning] Um `SwingWorker` é descartável
> *"`SwingWorker` is only designed to be executed once."* Não dá para reutilizar a mesma instância para uma segunda tarefa — crie um novo `SwingWorker` a cada execução.

```text
EDT      :  worker.execute()  ──┐
                                ▼
worker   :  doInBackground() ── publish(chunk) ──┐  ... segue computando ...  return T
                                                 ▼
EDT      :              process(List<chunk>) (1+ vezes durante)
EDT      :                                                       done()  ← lê get() aqui
```

### Resultados intermediários (`publish`/`process`) e progresso (`setProgress`/`getProgress`/`PropertyChangeListener`)

Para uma tarefa que produz resultados aos poucos (linhas de um arquivo, registros de uma consulta paginada), o par `publish`/`process` faz o *streaming* de dados de volta para a EDT:

- De dentro de `doInBackground`, chame `publish(V... chunks)` — *"This method is to be used from inside the `doInBackground` method to deliver intermediate results for processing on the Event Dispatch Thread inside the `process` method."*
- O Swing coalesce os chunks e invoca `process(List<V> chunks)` na EDT. *"Results from multiple invocations of `publish` are often accumulated for a single invocation of `process`."* Ou seja, vários `publish` podem virar **uma só** chamada de `process` com a lista acumulada — não conte com uma chamada por publish.

Para **progresso** (0–100), há um canal separado, baseado na bound property `progress`:

```java
protected final void setProgress(int progress)  // 0..100, chamado no worker
public final int getProgress()                  // lê a property
```

`setProgress` *"Sets the `progress` bound property. The value should be from 0 to 100."* Como `progress` é uma **bound property**, mudanças disparam um `PropertyChangeEvent`. Você registra um ouvinte com `addPropertyChangeListener(PropertyChangeListener listener)` e reage na EDT — o tutorial: *"The background task can define bound properties. Changes to these properties trigger events, causing event-handling methods to be invoked on the event dispatch thread."* O padrão idiomático é ligar isso a uma `JProgressBar`:

```java
worker.addPropertyChangeListener(evt -> {
    if ("progress".equals(evt.getPropertyName())) {
        progressBar.setValue((Integer) evt.getNewValue()); // roda na EDT — OK
    }
});
```

A distinção mental: **`publish`/`process` carregam dados** (de tipo `V`); **`setProgress`/`PropertyChangeListener` carregam só um inteiro de progresso**. Use o primeiro para resultado incremental, o segundo para a barra de progresso.

### Cancelamento (`cancel`/`isCancelled`)

`SwingWorker` herda o cancelamento de `Future`:

```java
public final boolean cancel(boolean mayInterruptIfRunning)
public final boolean isCancelled()
```

`cancel` *"Attempts to cancel execution of this task. This method has no effect if the task is already completed or cancelled, or could not be cancelled for some other reason."* O cancelamento é **cooperativo**: passar `mayInterruptIfRunning = true` interrompe a worker thread (seta o flag de interrupt), mas `doInBackground` precisa **checar** `isCancelled()` (ou `Thread.interrupted()`) em pontos de parada e abortar por conta própria. Cancelar não mata a thread à força.

```java
@Override
protected List<Registro> doInBackground() {
    List<Registro> acc = new ArrayList<>();
    for (int i = 0; i < total; i++) {
        if (isCancelled()) {
            break;                 // sai cedo: o cancelamento é cooperativo
        }
        acc.add(carregarLinha(i)); // i/o por linha
    }
    return acc;
}
```

### Obter o resultado (`get` — bloqueante)

`SwingWorker` é um `Future<T>`, então o resultado sai por `get()`:

```java
public final T get() throws InterruptedException, ExecutionException
public final T get(long timeout, TimeUnit unit)
        throws InterruptedException, ExecutionException, TimeoutException
```

`get` *"Waits if necessary for the computation to complete, and then retrieves its result."* O ponto crítico está no próprio Javadoc: *"calling `get` on the Event Dispatch Thread blocks all events, including repaints, from being processed until this `SwingWorker` is complete."* Logo, o lugar certo de chamar `get()` é **dentro de `done()`** — quando `done` roda, a tarefa já terminou, então `get()` retorna imediatamente sem bloquear. E `get()` é também onde a **exceção** lançada em `doInBackground` reaparece, embrulhada num `ExecutionException` (recupere a causa com `getCause()`). Atenção: se o worker foi cancelado via `cancel(true)`, `done()` ainda é invocado, mas `get()` lança `CancellationException` — não `ExecutionException` —, portanto o `done()` idiomático trata os três casos: `InterruptedException`, `ExecutionException` e `CancellationException`.

### `javax.swing.Timer` (callbacks na EDT) vs `java.util.Timer` (thread própria)

Para trabalho **periódico** (não um job único de background), a escolha do timer importa para a EDT:

| | `javax.swing.Timer` | `java.util.Timer` |
|---|---|---|
| Onde o callback roda | **na EDT** | numa **thread própria** do timer |
| Seguro para tocar componentes? | Sim (já está na EDT) | Não (precisa de `invokeLater`) |
| Uso típico | animação, atualização de UI a cada N ms | tarefa de fundo agendada, sem UI |

`javax.swing.Timer` dispara seu `ActionListener` **na EDT** — por isso pode atualizar componentes direto, e por isso o callback precisa ser rápido (vale a mesma regra de não bloquear a EDT). `java.util.Timer` roda numa thread separada — ótimo para background puro, mas qualquer toque em componente Swing de dentro dele precisa reentrar na EDT via `SwingUtilities.invokeLater`. Regra prática: **se o tique atualiza a UI, use `javax.swing.Timer`**.

## Na prática

Carregar dados de uma fonte lenta publicando progresso numa `JProgressBar`, e ler o resultado em `done()`. O `SwingWorker<List<Registro>, Integer>` devolve a lista (`T`) e publica o índice processado (`V`) para alimentar a barra; o progresso 0–100 vai pela bound property.

```java
import javax.swing.*;
import java.util.*;
import java.util.concurrent.ExecutionException;

class CargaWorker extends SwingWorker<List<Registro>, Integer> {

    private final JProgressBar progressBar;
    private final JLabel statusLabel;

    CargaWorker(JProgressBar progressBar, JLabel statusLabel) {
        this.progressBar = progressBar;
        this.statusLabel = statusLabel;
    }

    @Override
    protected List<Registro> doInBackground() throws Exception {
        // worker thread: I/O lento mora aqui. NÃO tocar componentes daqui.
        List<Registro> resultado = new ArrayList<>();
        int total = contarRegistros();          // hipotético: fonte lenta
        for (int i = 0; i < total; i++) {
            if (isCancelled()) {
                break;                           // cancelamento cooperativo
            }
            resultado.add(carregarRegistro(i));  // hipotético: lê 1 registro
            publish(i + 1);                      // chunk intermediário (V = Integer)
            setProgress((i + 1) * 100 / total);  // bound property 'progress' (0..100)
        }
        return resultado;                        // T = List<Registro>
    }

    @Override
    protected void process(List<Integer> processados) {
        // EDT: seguro tocar componentes. 'process' pode coalescer vários publish.
        int ultimo = processados.get(processados.size() - 1);
        statusLabel.setText("Carregados: " + ultimo);
    }

    @Override
    protected void done() {
        // EDT: a tarefa já terminou, então get() não bloqueia.
        try {
            List<Registro> dados = get();        // resultado final (ou relança erro)
            statusLabel.setText("Concluído: " + dados.size() + " registros");
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();  // restaura o flag de interrupt
        } catch (ExecutionException e) {
            // exceção lançada em doInBackground reaparece aqui, embrulhada
            statusLabel.setText("Falha: " + e.getCause().getMessage());
        } catch (java.util.concurrent.CancellationException e) {
            statusLabel.setText("Cancelado");
        }
    }
}
```

Ligando o worker à UI e à barra de progresso (tudo na EDT, num listener):

```java
botaoCarregar.addActionListener(e -> {
    progressBar.setValue(0);
    CargaWorker worker = new CargaWorker(progressBar, statusLabel);
    // a bound property 'progress' alimenta a JProgressBar
    worker.addPropertyChangeListener(evt -> {
        if ("progress".equals(evt.getPropertyName())) {
            progressBar.setValue((Integer) evt.getNewValue()); // EDT — OK
        }
    });
    worker.execute(); // agenda numa worker thread; retorna já
});
```

```text
// Fluxo:
// EDT     : execute() agenda e retorna  → UI continua responsiva
// worker  : doInBackground() lê registros, publish()/setProgress() a cada um
// EDT     : process() atualiza o label; PropertyChangeListener move a barra
// EDT     : done() lê get() e exibe o resultado final (ou o erro)
```

## Armadilhas

### (1) Chamar `get()` na EDT antes de a tarefa terminar

**Descrição.** `get()` é bloqueante: espera a tarefa concluir. Se você chama `get()` na EDT **antes** de `done()` (por exemplo, logo depois de `execute()`, no mesmo listener), a EDT trava esperando o background — e o próprio Javadoc avisa que *"calling `get` on the Event Dispatch Thread blocks all events, including repaints, from being processed until this `SwingWorker` is complete."* Resultado: a UI congela exatamente como se o trabalho rodasse na EDT. Você anulou todo o benefício do `SwingWorker`.

```java
// RUIM — get() na EDT, logo após execute(), bloqueia a UI até o fim do background
worker.execute();
List<Registro> dados = worker.get(); // EDT presa: nenhum repaint até terminar
statusLabel.setText("ok: " + dados.size());
```

**Fix (1 linha):** leia o resultado **dentro de `done()`**, onde a tarefa já terminou e `get()` retorna na hora.

---

### (2) Tocar componentes Swing dentro de `doInBackground`

**Descrição.** `doInBackground` *"is executed only once"* numa **worker thread**, fora da EDT. Mutar ou ler um componente Swing dali (`setText`, `getText`, `add`, `setValue`) viola a single-thread rule do Swing → corrupção **não-determinística e intermitente**, do tipo que funciona na maioria das execuções e quebra em produção sob certo timing. O compilador não acusa; em geral nem há exceção.

```java
// RUIM — atualiza a barra direto de doInBackground (fora da EDT)
@Override
protected Void doInBackground() {
    for (int i = 0; i <= 100; i++) {
        progressBar.setValue(i);  // toca componente fora da EDT → corrupção intermitente
        trabalhar();
    }
    return null;
}
```

**Fix (1 linha):** emita dados com `publish(...)` (recebidos em `process`, na EDT) ou progresso com `setProgress(...)` (lido por `PropertyChangeListener`, na EDT) — nunca toque o componente direto.

---

### (3) Exceção lançada em `doInBackground` engolida silenciosamente

**Descrição.** Se `doInBackground` lança uma exceção, ela **não** aparece no console nem para nenhum lugar: fica retida e só é relançada quando alguém chama `get()`, embrulhada num `ExecutionException`. Se você nunca chama `get()`, o erro **some** — a tarefa "termina", a UI não atualiza, e não há rastro de por quê. É uma das fontes mais comuns de "o SwingWorker não fez nada e não deu erro".

```java
// RUIM — done() não chama get(); a exceção de doInBackground desaparece
@Override
protected void done() {
    statusLabel.setText("Concluído"); // mente: pode ter falhado e ninguém viu
}
```

**Fix (1 linha):** **sempre** chame `get()` dentro de `done()` num `try/catch (ExecutionException e)` e trate `e.getCause()` (a exceção real).

## Em entrevista

### Frase pronta (inglês)

> "`SwingWorker` is the idiomatic way to do background work in Swing without breaking the single-thread rule. You subclass it and implement `doInBackground`, which runs on a worker thread — that's where the slow I/O or computation lives — and the result is typed as `T`, the first type parameter. The methods that touch the UI run on the Event Dispatch Thread: `done` is called once the task finishes, and `process` is called when you `publish` interim results of type `V`, the second type parameter. The two mistakes I always watch for are calling `get()` on the EDT before the task is done — that blocks every event and repaint, so I read the result inside `done()` where it returns immediately — and swallowing exceptions, because anything `doInBackground` throws is only rethrown when you call `get()`, wrapped in an `ExecutionException`, so I always call `get()` in `done()` inside a try/catch. For a progress bar I use the `progress` bound property via `setProgress` and a `PropertyChangeListener`, and for cancellation `cancel` plus a cooperative `isCancelled()` check in the loop."

### Vocabulário

| Termo PT | Termo EN |
|----------|----------|
| trabalho em background | background work / background task |
| thread de trabalho | worker thread |
| resultado final | final result |
| resultados intermediários | interim / intermediate results |
| publicar (chunks) | publish (chunks) |
| barra de progresso | progress bar |
| propriedade vinculada | bound property |
| ouvinte de mudança de propriedade | property change listener |
| cancelamento cooperativo | cooperative cancellation |
| bloquear a thread | block the thread |
| engolir a exceção | swallow the exception |
| relançar embrulhada | rethrow wrapped |

## Veja também

- [[03-Dominios/Java/Swing/05 - A Event Dispatch Thread|A Event Dispatch Thread (EDT)]]
- [[03-Dominios/Java/Swing/11 - Action API, key bindings e performance|Action API, key bindings e performance]]
- [[03-Dominios/Java/Swing/index|Swing (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Concorrência e paralelismo/index|Concorrência e paralelismo]]
- [[03-Dominios/Java/Concorrência e paralelismo/08 - Executors e thread pools|Executors e thread pools]]
- [[03-Dominios/Java/Dicionário de Java#SwingWorker|SwingWorker]]

## Referências

- [Worker Threads and SwingWorker — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/uiswing/concurrency/worker.html)
- [Tasks that Have Interim Results — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/uiswing/concurrency/interim.html)
- [SwingWorker — Javadoc Java 21 (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.desktop/javax/swing/SwingWorker.html)
