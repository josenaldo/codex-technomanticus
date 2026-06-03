---
title: "O modelo de eventos"
created: 2026-06-03
updated: 2026-06-03
type: concept
progress: backlog
status: seedling
publish: true
fase: iniciado
tags:
  - java
  - swing
  - iniciado
  - eventos
  - listeners
aliases:
  - Modelo de eventos
  - ActionListener
  - Listener
---

# O modelo de eventos

> [!abstract] TL;DR
> O Swing usa o **delegation event model**: componentes (fontes) disparam objetos de evento; objetos **listener** registrados nessa fonte recebem a notificação via callback. Interfaces com um único método (`ActionListener`) são diretamente substituíveis por lambda; interfaces com múltiplos métodos (`MouseListener`, `WindowListener`) têm **adapter classes** (`MouseAdapter`, `WindowAdapter`) com implementações vazias, permitindo sobrescrever só o que interessa. Todo o processamento de evento ocorre na **EDT** — trabalho pesado dentro de um listener congela a UI.

## O que é

O **delegation event model** (modelo de eventos por delegação) é o mecanismo pelo qual o Swing conecta a interação do usuário ao código da aplicação. O modelo define três papéis:

- **Source (fonte)** — o componente ou objeto que detecta a interação e dispara o evento; exemplos: `JButton`, `JTextField`, `JSlider`.
- **Event (evento)** — um objeto **criado pelo framework** que descreve o que aconteceu (qual componente, coordenadas, tecla etc.); carrega informações como a fonte (`getSource()`), timestamp e dados específicos do evento. Exemplos: `ActionEvent`, `MouseEvent`, `KeyEvent`.
- **Listener (ouvinte)** — objeto registrado na fonte que implementa uma interface de callback; quando o evento ocorre, a fonte itera sobre todos os listeners registrados e invoca o método correspondente.

A mesma fonte pode ter múltiplos listeners; o mesmo listener pode estar registrado em múltiplas fontes. A separação entre quem gera o evento (componente) e quem o trata (listener) é a essência do padrão: o componente não precisa conhecer a lógica da aplicação.

## Como funciona

### Source, event e listener (o triângulo)

O fluxo completo de um evento segue sempre o mesmo caminho:

```text
Ação do usuário
   → Componente (source) cria um objeto de evento
      → Componente notifica cada listener registrado (chama o método de callback)
         → Listener executa o código da aplicação
```

O componente mantém internamente uma lista de listeners. Ao chamar `addActionListener(listener)`, o componente adiciona o objeto à lista. Quando o evento ocorre, ele percorre a lista e invoca o callback em cada entrada — tudo na **Event Dispatch Thread (EDT)**.

### Listeners comuns (`ActionListener`, `MouseListener`, `KeyListener`, `FocusListener`, `WindowListener`)

| Interface | Método(s) | Quando é disparado |
|-----------|-----------|-------------------|
| `ActionListener` | `actionPerformed(ActionEvent)` | Clique em botão, Enter em campo de texto, seleção de menu |
| `MouseListener` | `mouseClicked`, `mousePressed`, `mouseReleased`, `mouseEntered`, `mouseExited` | Cliques e entrada/saída do cursor no componente |
| `MouseMotionListener` | `mouseMoved`, `mouseDragged` | Movimento do mouse sobre o componente |
| `KeyListener` | `keyPressed`, `keyTyped`, `keyReleased` | Teclas pressionadas (componente com foco) |
| `FocusListener` | `focusGained(FocusEvent)`, `focusLost(FocusEvent)` | Componente ganha ou perde o foco de teclado |
| `WindowListener` | `windowOpened`, `windowClosing`, `windowClosed`, `windowIconified`, `windowDeiconified`, `windowActivated`, `windowDeactivated` | Eventos de ciclo de vida da janela |
| `ItemListener` | `itemStateChanged(ItemEvent)` | Mudança de estado em `JCheckBox`, `JComboBox` |
| `ChangeListener` | `stateChanged(ChangeEvent)` | Mudança de valor em `JSlider`, `JTabbedPane`, `JSpinner` |

`ActionListener` é o listener mais usado no dia a dia. Por ter apenas **um método abstrato**, é uma **interface funcional** — pode ser substituída por uma lambda expression (conexão direta com o Galho 1 de linguagem: interfaces funcionais e lambdas).

### Event objects (`ActionEvent`, `MouseEvent`)

Os objetos de evento carregam contexto sobre o que aconteceu:

**`ActionEvent`** (pacote `java.awt.event`):
- `getSource()` — retorna o componente que disparou o evento.
- `getActionCommand()` — retorna o "comando" associado: por padrão, o texto do botão ou item de menu; pode ser customizado com `setActionCommand("meu-comando")`.
- `getModifiers()` — máscara com teclas modificadoras (Shift, Ctrl, Alt) pressionadas durante a ação.

**`MouseEvent`** (pacote `java.awt.event`):
- `getX()` / `getY()` — coordenadas relativas ao componente.
- `getPoint()` — conveniência: retorna um `Point`.
- `getClickCount()` — número de cliques consecutivos (útil para detectar duplo-clique).
- `getButton()` — qual botão do mouse: `BUTTON1` (esquerdo), `BUTTON2` (meio), `BUTTON3` (direito).
- `isPopupTrigger()` — indica se o evento deve abrir um menu de contexto; deve ser verificado tanto em `mousePressed` quanto em `mouseReleased` (a convenção varia por plataforma).

### Lambda vs classe anônima vs adapter (`MouseAdapter`)

Há três formas de fornecer um listener. A escolha depende da quantidade de métodos que a interface exige:

**Lambda — para interfaces funcionais (1 método abstrato):**

```java
JButton btn = new JButton("Enviar");
btn.addActionListener(e -> processarFormulario());
```

`ActionListener` tem um único método (`actionPerformed`), portanto é uma interface funcional. A lambda é a forma idiomática desde o Java 8.

**Classe anônima — quando há contexto local a capturar mas a interface tem poucos métodos:**

```java
btn.addActionListener(new ActionListener() {
    @Override
    public void actionPerformed(ActionEvent e) {
        processarFormulario();
    }
});
```

Na prática, lambdas (para listeners de método único) ou adapter classes cobrem quase todos os casos; classes anônimas são mais legado/verbosas.

**Adapter class — para interfaces com múltiplos métodos:**

Interfaces como `MouseListener` (5 métodos) e `WindowListener` (7 métodos) obrigam implementar todos os métodos, mesmo os que ficam vazios. As **adapter classes** resolvem isso: são classes abstratas com implementações vazias de todos os métodos da interface. O desenvolvedor estende o adapter e sobrescreve apenas o que precisa.

```java
panel.addMouseListener(new MouseAdapter() {
    @Override
    public void mouseClicked(MouseEvent e) {
        System.out.println("Clicou em (" + e.getX() + ", " + e.getY() + ")");
    }
    // mousePressed, mouseReleased, mouseEntered, mouseExited → herdados como vazio
});
```

`MouseAdapter` implementa `MouseListener`, `MouseMotionListener` e `MouseWheelListener`. Existe um adapter correspondente para cada interface multi-método: `WindowAdapter`, `FocusAdapter`, `KeyAdapter`, `ComponentAdapter`, etc.

### Registrar e remover listeners

Cada tipo de evento tem o par `addXxxListener` / `removeXxxListener`:

```java
ActionListener al = e -> processarFormulario();

// Registrar
btn.addActionListener(al);

// Remover (a mesma referência deve ser usada)
btn.removeActionListener(al);
```

Guardar a referência do listener é necessário para removê-lo depois. Listeners registrados mas nunca removidos em componentes de longa duração causam memory leaks — o componente mantém uma referência forte ao listener, impedindo o GC de coletar o objeto ouvinte.

## Na prática

**Botão com `ActionListener` via lambda:**

```java
import javax.swing.*;
import java.awt.*;

public class FormularioSimples {

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            JFrame frame = new JFrame("Login");
            frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

            JPanel panel = new JPanel(new FlowLayout());
            JTextField campoUsuario = new JTextField(15);
            JButton btnEntrar = new JButton("Entrar");
            JLabel status = new JLabel(" ");

            // ActionListener via lambda: ActionListener é interface funcional
            btnEntrar.addActionListener(e -> {
                String usuario = campoUsuario.getText().trim();
                status.setText(usuario.isEmpty() ? "Informe o usuário." : "Olá, " + usuario + "!");
            });

            panel.add(campoUsuario);
            panel.add(btnEntrar);
            panel.add(status);

            frame.add(panel);
            frame.pack();
            frame.setVisible(true);
        });
    }
}
```

**`MouseAdapter` para tratar apenas `mouseClicked`:**

```java
JPanel canvas = new JPanel();

// Implementar a interface MouseListener inteira exigiria 5 métodos.
// MouseAdapter fornece implementações vazias; sobrescrevemos só o necessário.
canvas.addMouseListener(new MouseAdapter() {
    @Override
    public void mouseClicked(MouseEvent e) {
        if (e.getClickCount() == 2) {
            System.out.println("Duplo-clique em (" + e.getX() + ", " + e.getY() + ")");
        }
    }
});
```

## Armadilhas

### (1) Trabalho pesado ou I/O dentro do listener (congela a UI)

O callback do listener é invocado **na EDT**. A EDT é a única thread que pode atualizar componentes Swing — e é também a thread responsável por redesenhar a tela. Qualquer operação longa dentro do listener (consulta a banco, chamada de rede, processamento de arquivo) bloqueia a EDT, fazendo a UI parecer travada ou "morta" durante toda a execução.

```java
// ERRADO: chamada de rede dentro do listener → EDT fica bloqueada
btnBuscar.addActionListener(e -> {
    String resultado = servicoHttp.buscar(campoPesquisa.getText()); // pode levar segundos
    labelResultado.setText(resultado);
});
```

**Fix:** mover o trabalho pesado para uma thread de background e atualizar a UI via `SwingUtilities.invokeLater` — ou usar `SwingWorker`, que foi criado exatamente para esse padrão. Ver [[03-Dominios/Java/Swing/05 - A Event Dispatch Thread|A Event Dispatch Thread (EDT)]].

```java
btnBuscar.addActionListener(e -> {
    new SwingWorker<String, Void>() { // <String = resultado de doInBackground, Void = sem resultados intermediários via publish/process>
        @Override
        protected String doInBackground() {
            return servicoHttp.buscar(campoPesquisa.getText()); // fora da EDT
        }

        @Override
        protected void done() {
            try {
                labelResultado.setText(get()); // de volta à EDT
            } catch (Exception ex) {
                labelResultado.setText("Erro: " + ex.getMessage());
            }
        }
    }.execute();
});
```

---

### (2) Implementar `MouseListener` inteira só para um método (cinco métodos vazios)

Ao implementar `MouseListener` diretamente, todos os cinco métodos tornam-se obrigatórios em tempo de compilação. Implementar quatro deles como corpos vazios gera ruído que obscurece a intenção real do código.

```java
// PROBLEMÁTICO: quatro métodos vazios não comunicam nada
panel.addMouseListener(new MouseListener() {
    @Override public void mouseClicked(MouseEvent e) { abrirMenu(e); }
    @Override public void mousePressed(MouseEvent e) { }   // vazio
    @Override public void mouseReleased(MouseEvent e) { }  // vazio
    @Override public void mouseEntered(MouseEvent e) { }   // vazio
    @Override public void mouseExited(MouseEvent e) { }    // vazio
});
```

**Fix:** usar `MouseAdapter`, que fornece implementações vazias de fábrica e deixa explícito que só `mouseClicked` tem relevância neste ponto.

```java
panel.addMouseListener(new MouseAdapter() {
    @Override
    public void mouseClicked(MouseEvent e) { abrirMenu(e); }
});
```

---

### (3) `KeyListener` para detectar atalhos de teclado (problema de foco)

`KeyListener` só recebe eventos do componente que tem o **foco de teclado** no momento. Em janelas com muitos componentes, o componente alvo pode não ter o foco, fazendo o atalho não funcionar silenciosamente — um bug difícil de rastrear.

```java
// FRÁGIL: só funciona se 'panel' tiver foco
panel.addKeyListener(new KeyAdapter() {
    @Override
    public void keyPressed(KeyEvent e) {
        if (e.getKeyCode() == KeyEvent.VK_DELETE) deletarItem();
    }
});
```

**Fix:** usar `InputMap` / `ActionMap` (mecanismo de key bindings do `JComponent`), que permite associar atalhos a um escopo de foco controlado (`WHEN_IN_FOCUSED_WINDOW`). Esse mecanismo é abordado em [[03-Dominios/Java/Swing/11 - Action API, key bindings e performance|Action API, key bindings e performance]].

## Em entrevista

### Frase pronta (inglês)

> "Swing follows the delegation event model: a component — the event source — fires an event object when the user interacts with it, and every registered listener is notified via a callback method. Listener interfaces with a single abstract method, like `ActionListener`, are functional interfaces and can be replaced by a lambda expression, which is the idiomatic approach since Java 8. For multi-method interfaces such as `MouseListener` or `WindowListener`, the AWT provides adapter classes — `MouseAdapter`, `WindowAdapter` — that supply empty implementations of every method so you only override what you need. The golden rule is that listener callbacks execute on the Event Dispatch Thread, so any blocking I/O or heavy computation inside a listener must be offloaded to a background thread, typically via `SwingWorker`, to keep the UI responsive."

### Vocabulário

| Termo PT | Termo EN |
|----------|----------|
| modelo de eventos por delegação | delegation event model |
| fonte de evento | event source |
| objeto de evento | event object |
| ouvinte / escutador | event listener |
| classe adaptadora | adapter class |
| registrar um listener | register a listener / add a listener |
| remover um listener | remove a listener / deregister a listener |
| interface funcional | functional interface |
| callback | callback / callback method |
| comando de ação | action command |
| evento semântico | semantic event |
| evento de baixo nível | low-level event |

## Veja também

- [[03-Dominios/Java/Swing/01 - O modelo do Swing|O modelo do Swing]]
- [[03-Dominios/Java/Swing/05 - A Event Dispatch Thread|A Event Dispatch Thread (EDT)]]
- [[03-Dominios/Java/Swing/11 - Action API, key bindings e performance|Action API, key bindings e performance]]
- [[03-Dominios/Java/Swing/index|Swing (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Linguagem e sintaxe moderna/index|Linguagem e sintaxe moderna]]
- [[03-Dominios/Java/Dicionário de Java#delegation event model|delegation event model]]
- [[03-Dominios/Java/Dicionário de Java#listener (event listener)|listener]]
- [[03-Dominios/Java/Dicionário de Java#adapter (event adapter)|adapter]]

## Referências

- [Writing Event Listeners — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/uiswing/events/index.html)
- [Introduction to Event Listeners — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/uiswing/events/intro.html)
- [General Information about Writing Event Listeners — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/uiswing/events/generalrules.html)
- [How to Write a Mouse Listener — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/uiswing/events/mouselistener.html)
- [ActionListener — Javadoc Java 21 (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.desktop/java/awt/event/ActionListener.html)
- [MouseAdapter — Javadoc Java 21 (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.desktop/java/awt/event/MouseAdapter.html)
- [ActionEvent — Javadoc Java 21 (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.desktop/java/awt/event/ActionEvent.html)
- [MouseEvent — Javadoc Java 21 (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.desktop/java/awt/event/MouseEvent.html)
