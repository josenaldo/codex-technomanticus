---
title: "A Event Dispatch Thread (EDT)"
created: 2026-06-03
updated: 2026-06-03
type: concept
progress: backlog
status: seedling
publish: true
fase: Adepto
tags:
  - java
  - swing
  - adepto
  - edt
  - threading
aliases:
  - EDT
  - Event Dispatch Thread
  - invokeLater
---

# A Event Dispatch Thread (EDT)

> [!abstract] TL;DR
> A **Event Dispatch Thread (EDT)** é a thread especial onde o Swing despacha eventos e pinta componentes. O modelo é **single-threaded por design**: salvo pouquíssimas exceções thread-safe, todo acesso a componentes Swing deve ocorrer na EDT. Disso saem as **duas regras de ouro**: (1) nunca toque um componente fora da EDT — o sintoma é corrupção **não-determinística e intermitente**, que funciona na maioria das execuções e falha de forma difícil de reproduzir; (2) nunca bloqueie a EDT com trabalho longo — enquanto ela está ocupada, eventos e repaints empilham e a UI "congela". Para entrar na EDT a partir de outra thread, use `SwingUtilities.invokeLater` (assíncrono) ou `invokeAndWait` (síncrono). Para tarefas de background, a ferramenta de alto nível é [[03-Dominios/Tecnologia/Java/Swing/06 - SwingWorker e tarefas em background|SwingWorker]].

## O que é

A **Event Dispatch Thread (EDT)** é uma thread única, criada e gerenciada pelo runtime AWT/Swing, responsável por dois trabalhos:

1. **Event handling** — disparar os listeners registrados (`ActionListener.actionPerformed`, `MouseListener`, etc.) em resposta a eventos de input e de sistema.
2. **Painting** — executar o ciclo de pintura dos componentes (`paintComponent` e correlatos).

O tutorial oficial é explícito: *"Swing event handling code runs on a special thread known as the event dispatch thread. Most code that invokes Swing methods also runs on this thread."*

Essa é a **single-thread rule** do Swing. A formulação canônica da Oracle:

> "All other Swing component methods must be invoked from the event dispatch thread. Programs that ignore this rule may function correctly most of the time, but are subject to unpredictable errors that are difficult to reproduce."

Em palavras: o Swing **não é thread-safe**. Métodos como `setText`, `setEnabled`, `add`, `repaint` ou `revalidate` só podem ser chamados pela EDT. As exceções — métodos documentados como thread-safe, p. ex. `repaint()` e `revalidate()` (que engloba a invalidação e agenda a repintura de forma segura), além dos próprios `invokeLater`/`invokeAndWait` — são a minoria explícita; tudo o mais é EDT-only.

A EDT é uma das **três categorias de thread** que um programa Swing manipula, segundo o tutorial:

| Categoria | Papel |
|-----------|-------|
| **Initial threads** | Executam o código de inicialização (tipicamente a `main`, que agenda a construção da UI na EDT). |
| **Event Dispatch Thread** | Despacha eventos e pinta — onde quase todo código Swing roda. |
| **Worker / background threads** | Executam trabalho demorado fora da EDT (normalmente via [[03-Dominios/Tecnologia/Java/Swing/06 - SwingWorker e tarefas em background|SwingWorker]]). |

O programador **não cria** a EDT explicitamente; o framework a provê. O que o programador controla é *quando seu código entra* nela.

## Por que importa

Quase todo bug "feio" de UI Swing tem origem na EDT:

- **UI congelada.** Um listener que faz I/O (consulta a banco, chamada HTTP, leitura de arquivo grande) **bloqueia a EDT**. Enquanto ela está presa, nenhum evento é despachado e nenhum repaint acontece — a janela trava, não responde a cliques e pode nem se redesenhar ao ser arrastada. O tutorial é direto: *"Tasks on the event dispatch thread must finish quickly; if they don't, unhandled events back up and the user interface becomes unresponsive."*
- **Corrupção intermitente.** Tocar um componente de uma thread de background produz *"unpredictable errors that are difficult to reproduce"* — o tipo de bug que passa em todos os testes locais e quebra em produção sob timing específico.

Em **entrevista**, esse é o coração da pergunta sobre Swing. O entrevistador raramente quer o catálogo de componentes; ele quer ouvir *"por que `invokeLater`?"* e *"o que acontece se você chamar `setText` de outra thread?"*. Quem sabe distinguir as duas regras de ouro — não bloquear vs não tocar fora da EDT — demonstra o modelo mental correto. Esta é a nota que ancora essa resposta; os primitivos de concorrência por trás (threads, executors, `interrupt`) vivem no galho [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Concorrência e paralelismo]] e não são re-explicados aqui.

## Como funciona

### A single-thread rule (por que a GUI é single-threaded)

O motivo imediato, segundo a Oracle: *"Most Swing object methods are not 'thread safe': invoking them from multiple threads risks thread interference or memory consistency errors."* Sincronizar cada componente seria caro e propenso a erro.

O motivo histórico, mais profundo, é a **ordem de aquisição de locks** (lock-ordering). Toolkits de GUI multi-thread anteriores tentaram proteger cada componente com locks. O problema: a árvore de componentes é percorrida ora de cima para baixo (eventos descem do top-level container até o filho), ora de baixo para cima (um repaint de um filho sobe pedindo validação ao pai). Threads diferentes adquirindo locks de pai e filho em ordens opostas produzem **deadlock clássico de lock-ordering**. A decisão de projeto do Swing foi eliminar a classe inteira de bugs: existe **uma só thread** que toca a árvore, então não há dois adquirentes de lock e não há deadlock por ordenação. O custo dessa simplicidade é transferido para o desenvolvedor — a responsabilidade de não bloquear a EDT.

> [!info] Single-thread, não thread-confined-por-lock
> O Swing não serializa o acesso com locks; ele **confina** o acesso a uma thread. Não há `synchronized` protegendo `JLabel`. A "proteção" é a disciplina de só tocar componentes na EDT. Quebrar essa disciplina não dá erro de compilação nem (geralmente) exceção imediata — dá corrupção silenciosa.

### O que roda na EDT (dispatch de eventos + painting)

A EDT consome uma fila de tarefas. Há essencialmente dois tipos:

- **Event-handling tasks** — *"Most tasks are invocations of event-handling methods, such as `ActionListener.actionPerformed`."* Quando o usuário clica num botão, o AWT enfileira um evento; a EDT o retira e invoca os listeners.
- **Painting tasks** — o ciclo de pintura (`paintComponent`) roda na EDT. Por isso bloquear a EDT também congela o redesenho: o pedido de repaint fica na fila atrás do trabalho que está prendendo a thread.
- **Scheduled tasks** — *"Other tasks can be scheduled by application code, using `invokeLater` or `invokeAndWait`."* É assim que código de outra thread "entra" na EDT.

```text
[input do usuário] → fila de eventos do AWT
                          │
                          ▼
                  Event Dispatch Thread  (uma só)
                          │
          ┌───────────────┼───────────────┐
          ▼               ▼               ▼
   event handling     painting      Runnables agendados
   (actionPerformed)  (paintComponent)  (invokeLater/invokeAndWait)
```

Como a fila é processada **sequencialmente por uma única thread**, qualquer tarefa lenta atrasa todas as seguintes — daí a exigência de que tudo na EDT termine rápido.

### A regra de ouro (não bloquear; não tocar componentes fora da EDT)

As duas obrigações são duais e ambas precisam valer:

1. **Não tocar componentes fora da EDT.** Ler ou mutar estado de componente (`setText`, `getText`, `add`, `setEnabled`) de uma thread de background viola a single-thread rule → corrupção não-determinística.
2. **Não bloquear a EDT.** Rodar trabalho demorado (I/O, cálculo pesado, `Thread.sleep`) *dentro* de um listener prende a única thread que pinta e despacha → UI congelada.

A solução combina as duas: o trabalho pesado vai para uma **thread de background**; quando ele termina e precisa atualizar a tela, **reentra na EDT** via `invokeLater`. Os primitivos de background — criar a thread, usar um `ExecutorService` — pertencem ao galho [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Concorrência e paralelismo]] (veja [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/02 - Threads e seu ciclo de vida|Threads e seu ciclo de vida]]). A EDT é só o ponto de **entrega** do resultado.

### `SwingUtilities.invokeLater` vs `invokeAndWait`

Ambos recebem um `Runnable` e o executam **na EDT**. A diferença é bloqueio e retorno.

```java
public static void invokeLater(Runnable doRun)
public static void invokeAndWait(Runnable doRun)
        throws InterruptedException, InvocationTargetException
```

- **`invokeLater`** — *"Causes `doRun.run()` to be executed asynchronously on the AWT event dispatching thread. This will happen after all pending AWT events have been processed."* Não bloqueia o chamador; só enfileira. É a escolha padrão para "atualize a UI quando der".
- **`invokeAndWait`** — *"Causes `doRun.run()` to be executed synchronously on the AWT event dispatching thread. This call blocks until all pending AWT events have been processed and (then) `doRun.run()` returns."* Use quando a thread de background **precisa do resultado** ou da garantia de que a atualização já ocorreu antes de prosseguir.

| | `invokeLater` | `invokeAndWait` |
|---|---|---|
| Execução | na EDT | na EDT |
| Bloqueia o chamador? | Não (assíncrono) | Sim (síncrono) |
| Exceções declaradas | nenhuma | `InterruptedException`, `InvocationTargetException` |
| Chamar a partir da própria EDT? | OK (reenfileira — o `Runnable` só executa após o evento atual terminar) | **Proibido** (lança `Error`) |
| Uso típico | atualizar UI a partir de background | esperar a UI atualizar antes de continuar |

Sobre exceções dentro do `Runnable` no `invokeAndWait`: *"if the `Runnable.run` method throws an uncaught exception (on the event dispatching thread) it's caught and rethrown, as an `InvocationTargetException`, on the caller's thread."* — ou seja, o erro da tarefa chega ao chamador embrulhado; recupere a causa real com `getCause()`.

> [!warning] `invokeAndWait` a partir da EDT
> O Javadoc adverte: *"It shouldn't be called from the event dispatching thread."* Na prática, a implementação lança `java.lang.Error` ("Cannot call invokeAndWait from the event dispatcher thread") — uma thread esperando por si mesma é deadlock por construção. Sempre proteja com `isEventDispatchThread()`.

Há ainda uma diferença sutil de **ordenação** entre os dois. `invokeLater` enfileira o `Runnable` *no fim* da fila de eventos: ele só roda *"after all pending AWT events have been processed"*. Logo, se você agenda uma atualização e em seguida o usuário ainda gera eventos, a sua tarefa não "fura a fila". Para encadear duas atualizações na ordem exata, agende ambas com `invokeLater` em sequência — a fila FIFO preserva a ordem de submissão a partir da mesma thread.

```java
SwingUtilities.invokeLater(() -> label.setText("passo 1"));
SwingUtilities.invokeLater(() -> label.setText("passo 2")); // roda depois do passo 1
```

### `isEventDispatchThread`

Para saber em qual thread o código corre, use o predicado estático:

```java
public static boolean isEventDispatchThread()  // true se a thread atual é a EDT
```

Casos de uso comuns:

- **Guard de `invokeAndWait`** — evitar o `Error` quando o método pode ser chamado de qualquer thread.
- **Assertions de invariante** — em código que *deve* rodar na EDT, falhar cedo e alto.

```java
void atualizarStatus(String texto) {
    assert SwingUtilities.isEventDispatchThread()
        : "atualizarStatus chamado fora da EDT";
    statusLabel.setText(texto);
}
```

```java
void executarNaEdt(Runnable acao) {
    if (SwingUtilities.isEventDispatchThread()) {
        acao.run();                       // já estamos na EDT: roda direto
    } else {
        SwingUtilities.invokeLater(acao); // outra thread: agenda
    }
}
```

## Na prática

### Iniciar a UI na EDT

O ponto de entrada (`main`) roda numa *initial thread*, não na EDT. A construção da janela é, ela própria, acesso a componentes Swing — então deve ser agendada na EDT:

```java
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.SwingUtilities;

public class App {

    private static void criarUi() {
        JFrame frame = new JFrame("Demo EDT");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.add(new JLabel("Pronto"));
        frame.pack();
        frame.setVisible(true);
    }

    public static void main(String[] args) {
        // 'main' roda numa initial thread; entrega a construção à EDT.
        SwingUtilities.invokeLater(App::criarUi);
    }
}
```

### Atualizar um `JLabel` a partir de uma thread de background

O padrão correto: o trabalho lento roda **fora** da EDT; o resultado é entregue **dentro** dela via `invokeLater`.

```java
JLabel statusLabel = new JLabel("Ocioso");

// Listener: dispara na EDT. NÃO faça o trabalho aqui — apenas inicie o background.
botao.addActionListener(e -> {
    statusLabel.setText("Carregando...");      // EDT: OK

    new Thread(() -> {                          // thread de background
        String resultado = consultarServico();  // I/O lento — fora da EDT, OK

        // Reentra na EDT só para tocar o componente:
        SwingUtilities.invokeLater(() -> statusLabel.setText(resultado));
    }, "background-consulta").start();
});
```

```text
// Fluxo:
// EDT     : setText("Carregando...")  → retorna rápido, UI continua responsiva
// bg      : consultarServico()        → demora, mas não trava a UI
// EDT     : setText(resultado)        → atualização final, agendada via invokeLater
```

### Ler estado da UI a partir do background com `invokeAndWait`

Quando a thread de background precisa **ler** um valor que vive na EDT (o texto de um campo, o item selecionado de uma lista) antes de prosseguir, `invokeLater` não serve — ele não devolve resultado. Use `invokeAndWait`, mas trafegue o valor por uma referência efetivamente final (a lambda não pode retornar diretamente):

```java
import java.util.concurrent.atomic.AtomicReference;

// roda numa thread de background
AtomicReference<String> filtro = new AtomicReference<>();
try {
    SwingUtilities.invokeAndWait(() -> filtro.set(campoBusca.getText())); // lê na EDT
} catch (InterruptedException e) {
    Thread.currentThread().interrupt();        // restaura o flag de interrupt
    return;
} catch (java.lang.reflect.InvocationTargetException e) {
    throw new RuntimeException(e.getCause());   // erro real veio embrulhado
}
String termo = filtro.get();                    // já disponível na thread de background
List<Registro> resultados = consultar(termo);   // segue o trabalho fora da EDT
```

O tratamento das duas exceções checadas é parte do contrato: `InterruptedException` exige restaurar o flag de interrupt (assunto do galho [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/02 - Threads e seu ciclo de vida|Threads e seu ciclo de vida]]), e `InvocationTargetException` embrulha a exceção real lançada dentro do `Runnable` — recupere a causa com `getCause()`.

> [!tip] Prefira `SwingWorker` na vida real
> Criar `Thread` na mão e costurar `invokeLater`/`invokeAndWait` funciona, mas é verboso e fácil de errar (tratamento de exceção, cancelamento, progresso). A forma idiomática de alto nível para "trabalho de background + atualização de UI" é [[03-Dominios/Tecnologia/Java/Swing/06 - SwingWorker e tarefas em background|SwingWorker]], que encapsula esse padrão (`doInBackground` fora da EDT, `done`/`process` na EDT). Os exemplos com `Thread` aqui isolam o mecanismo da EDT; em produção, use `SwingWorker`.

## Armadilhas

### (1) Atualizar um componente a partir de uma thread de background

**Descrição.** Mutar um componente Swing direto de uma thread de background viola a single-thread rule. Não há `synchronized` protegendo o componente, então o resultado é **não-determinístico e intermitente**: na maioria das execuções parece funcionar, e ocasionalmente — sob certo timing de scheduling — produz renderização corrompida, estado inconsistente, `NullPointerException` internos ou repaints perdidos. O bug *"may function correctly most of the time"* e some quando você liga o debugger.

```java
// RUIM — toca o JLabel fora da EDT
new Thread(() -> {
    String r = consultarServico();
    statusLabel.setText(r);   // violação: setText fora da EDT → corrupção intermitente
}).start();
```

**Fix (1 linha):** embrulhe o toque ao componente em `SwingUtilities.invokeLater(() -> statusLabel.setText(r));`.

---

### (2) `invokeAndWait` chamado a partir da própria EDT

**Descrição.** `invokeAndWait` bloqueia o chamador até a EDT processar o `Runnable`. Se o chamador *já é* a EDT, ela passaria a esperar por si mesma — deadlock por construção. A implementação detecta o caso e lança `java.lang.Error` ("Cannot call invokeAndWait from the event dispatcher thread"); o Javadoc avisa que o método *"shouldn't be called from the event dispatching thread."* Acontece em código compartilhado, chamado ora de background, ora de um listener.

```java
// RUIM — se este método for chamado de dentro de um listener, já estamos na EDT
void atualizarSincrono() throws Exception {
    SwingUtilities.invokeAndWait(() -> label.setText("ok")); // lança Error na EDT
}
```

**Fix (1 linha):** proteja com `if (SwingUtilities.isEventDispatchThread()) acao.run(); else SwingUtilities.invokeAndWait(acao);`.

---

### (3) Operação longa ou I/O direto dentro de um listener

**Descrição.** Um listener roda **na EDT**. Fazer I/O (HTTP, banco, arquivo), `Thread.sleep` ou cálculo pesado dentro dele prende a única thread que despacha eventos e pinta. A UI **congela**: não responde a cliques e não se redesenha, porque o repaint fica na fila atrás do trabalho que segura a thread. *"Tasks on the event dispatch thread must finish quickly; if they don't, ... the user interface becomes unresponsive."*

```java
// RUIM — I/O síncrono dentro do listener bloqueia a EDT por segundos
botao.addActionListener(e -> {
    byte[] dados = baixarArquivoGrande();  // bloqueia a EDT → janela congela
    label.setText("Baixado: " + dados.length + " bytes");
});
```

**Fix (1 linha):** mova o trabalho para background — idealmente um [[03-Dominios/Tecnologia/Java/Swing/06 - SwingWorker e tarefas em background|SwingWorker]] (`doInBackground` faz o I/O, `done` atualiza o `JLabel` na EDT).

## Em entrevista

### Frase pronta (inglês)

> "Swing is single-threaded by design: there's one special thread, the Event Dispatch Thread, that both dispatches events and paints components, and almost every Swing method has to be called on it. That design choice buys you a lot of simplicity — there are no locks on the component tree, so you never get the lock-ordering deadlocks that early multi-threaded GUI toolkits suffered from — but it pushes a responsibility onto the developer: you must never block the EDT, and you must never touch a component from another thread. If you run I/O inside a listener, the UI freezes because the one thread that paints is busy; if you mutate a component from a background thread, you get non-deterministic corruption that works most of the time and is painful to reproduce. So the pattern is: do the heavy work on a worker thread, then re-enter the EDT with `SwingUtilities.invokeLater` — or, in real code, use `SwingWorker`, which packages that whole pattern. The one caveat I'd add is `invokeAndWait`: it's the synchronous version, but you must never call it from the EDT itself, because the thread would end up waiting on itself — I guard it with `isEventDispatchThread`."

### Vocabulário

| Termo PT | Termo EN |
|----------|----------|
| thread de despacho de eventos | Event Dispatch Thread (EDT) |
| regra de thread única | single-thread rule |
| despacho de eventos | event dispatching |
| ciclo de pintura | painting cycle / paint cycle |
| thread de background | worker thread / background thread |
| bloquear a interface | freeze / block the UI |
| agendar na EDT | schedule on the EDT |
| reentrar na EDT | re-enter the EDT |
| não-determinístico / intermitente | non-deterministic / intermittent |
| ordenação de locks | lock ordering |
| não thread-safe | not thread-safe |

## Veja também

- [[03-Dominios/Tecnologia/Java/Swing/04 - O modelo de eventos|O modelo de eventos]]
- [[03-Dominios/Tecnologia/Java/Swing/06 - SwingWorker e tarefas em background|SwingWorker e tarefas em background]]
- [[03-Dominios/Tecnologia/Java/Swing/11 - Action API, key bindings e performance|Action API, key bindings e performance]]
- [[03-Dominios/Tecnologia/Java/Swing/index|Swing (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Concorrência e paralelismo]]
- [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/02 - Threads e seu ciclo de vida|Threads e seu ciclo de vida]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#EDT (Event Dispatch Thread)|EDT]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#invokeLater / invokeAndWait|invokeLater / invokeAndWait]]

## Referências

- [Concurrency in Swing — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/uiswing/concurrency/index.html)
- [The Event Dispatch Thread — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/uiswing/concurrency/dispatch.html)
- [SwingUtilities — Javadoc Java 21 (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.desktop/javax/swing/SwingUtilities.html)
