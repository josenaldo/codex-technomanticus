---
title: "Action API, key bindings e performance"
created: 2026-06-03
updated: 2026-06-03
type: concept
progress: backlog
status: seedling
publish: true
fase: magus
tags:
  - java
  - swing
  - magus
  - action
  - key-bindings
  - performance
aliases:
  - Action API
  - Key bindings
  - InputMap
---

# Action API, key bindings e performance

> [!abstract] TL;DR
> **Action API** (`javax.swing.Action` / `AbstractAction`) centraliza comportamento e estado num único objeto reutilizável: um `Action` conectado a um `JButton`, um `JMenuItem` e uma toolbar mantém texto, ícone e estado `enabled` sincronizados — um `setEnabled(false)` desabilita os três de uma vez. **Key bindings** (`InputMap` + `ActionMap`) são a forma idiomática de mapear atalhos de teclado em Swing; ao contrário de `KeyListener`, eles não dependem de foco no componente certo — especialmente com `WHEN_IN_FOCUSED_WINDOW`. **Performance e responsividade** dependem de manter a EDT livre (nunca bloquear), usar models lazy/virtuais para grandes volumes de dados e restringir `repaint` à região mínima necessária.

## O que é

Três técnicas de nível sênior para UIs Swing robustas e sustentáveis:

- **Action API** — o padrão de centralizar lógica e estado de UI num único objeto `Action`, eliminando a duplicação que surge quando o mesmo comportamento é acessível por múltiplos pontos de entrada (botão, item de menu, atalho de teclado, toolbar).
- **Key bindings** — o mecanismo nativo do Swing, baseado em `InputMap` e `ActionMap`, para associar `KeyStroke`s a ações de forma desacoplada do foco. Substitui `KeyListener` para qualquer atalho cujo escopo seja maior que o componente individual.
- **Performance e responsividade** — conjunto de práticas que mantém a UI fluida: EDT livre de trabalho pesado, models lazy/virtuais para listas e tabelas grandes, e `repaint` de região para custom painting.

As três se complementam: `Action` já carrega o `ACCELERATOR_KEY` (um `KeyStroke`), que os próprios menus lêem; registrar o mesmo `KeyStroke` via `InputMap`/`ActionMap` estende o atalho para o escopo de janela; e a EDT desocupada garante que a UI responda ao atalho sem jank.

## Como funciona

### Action API (`Action` / `AbstractAction`)

A interface `javax.swing.Action` estende `ActionListener` e adiciona:

- **Propriedades nomeadas** — armazenadas num mapa interno e acessadas via `putValue(String key, Object value)` / `getValue(String key)`. As constantes padrão são:

| Constante | Tipo | Uso típico |
|-----------|------|------------|
| `Action.NAME` | `String` | Rótulo do botão / item de menu |
| `Action.SHORT_DESCRIPTION` | `String` | Texto do tooltip |
| `Action.SMALL_ICON` | `Icon` | Ícone pequeno (menus e toolbars) |
| `Action.LARGE_ICON_KEY` | `Icon` | Ícone grande (botões de toolbar) |
| `Action.ACCELERATOR_KEY` | `KeyStroke` | Atalho de teclado exibido no menu |
| `Action.MNEMONIC_KEY` | `Integer` | Código `KeyEvent.VK_*` para mnemonic |
| `Action.SELECTED_KEY` | `Boolean` | Estado de seleção (toggle buttons) |
| `Action.ACTION_COMMAND_KEY` | `String` | Comando passado no `ActionEvent` |

- **Estado `enabled` centralizado** — `setEnabled(boolean)` / `isEnabled()` propagam para todos os componentes ligados via `PropertyChangeListener` interno.
- **Comportamento** — o método `actionPerformed(ActionEvent e)` define o que acontece quando qualquer componente associado é acionado.

`AbstractAction` é a implementação base fornecida pelo framework: gerencia o mapa de propriedades, dispara `PropertyChangeEvent` quando uma propriedade muda e implementa `addPropertyChangeListener` / `removePropertyChangeListener`. Na prática, sempre se estende `AbstractAction` em vez de implementar `Action` diretamente.

**O ponto central:** quando você chama `button.setAction(action)` ou `new JButton(action)`, o componente instala o `Action` como `ActionListener` e registra um `PropertyChangeListener` que mantém texto, ícone e estado `enabled` sincronizados. O mesmo vale para `JMenuItem` e `JToolBar`. Alterar o `Action` atualiza todos os componentes associados.

### Key bindings (`InputMap` + `ActionMap`)

Cada `JComponent` possui três `InputMap`s, selecionáveis pela condição de foco:

| Constante (`JComponent.*`) | Ativa quando... | Uso típico |
|----------------------------|-----------------|------------|
| `WHEN_FOCUSED` | o próprio componente tem foco | `Space` ativa um `JButton` focado |
| `WHEN_ANCESTOR_OF_FOCUSED_COMPONENT` | o componente contém o componente com foco | setas de navegação num `JTable` |
| `WHEN_IN_FOCUSED_WINDOW` | qualquer componente da janela tem foco | atalhos de aplicação como `Ctrl+S` |

O fluxo de resolução é:

```text
KeyStroke pressionado
  → InputMap (condição correta) → chave String
    → ActionMap → Action
      → Action.actionPerformed(e)
```

**Por que vence `KeyListener`:** `KeyListener` só recebe eventos se o componente exato ao qual foi adicionado tiver o foco de teclado no momento. Numa janela com dezenas de componentes, o foco pode estar em qualquer lugar. Com `InputMap(WHEN_IN_FOCUSED_WINDOW)`, o atalho funciona enquanto a janela tiver foco — independente de qual componente está ativo. Além disso, a `Action` associada pode ser desabilitada com `setEnabled(false)`, e o atalho pára de funcionar automaticamente; com `KeyListener` isso exige gerenciamento manual. Ver [[03-Dominios/Tecnologia/Java/Swing/04 - O modelo de eventos|O modelo de eventos]] para o contexto de `KeyListener` e suas limitações.

**Registrar um binding:**

```java
// Obter InputMap com escopo de janela e ActionMap do componente raiz
JRootPane root = frame.getRootPane();

root.getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
    .put(KeyStroke.getKeyStroke("ctrl S"), "salvar");

root.getActionMap()
    .put("salvar", salvarAction); // salvarAction é um AbstractAction
```

A chave intermediária (`"salvar"`) é apenas uma `String` arbitrária que desacopla o `InputMap` do `ActionMap`. Isso permite trocar a `Action` sem alterar o mapeamento de tecla, ou reutilizar a mesma `Action` com várias teclas.

**`KeyStroke.getKeyStroke(String)`** aceita expressões legíveis:

```java
KeyStroke.getKeyStroke("ctrl S")           // Ctrl+S
KeyStroke.getKeyStroke("ctrl shift Z")     // Ctrl+Shift+Z
KeyStroke.getKeyStroke("F5")               // F5
KeyStroke.getKeyStroke("DELETE")           // Delete
KeyStroke.getKeyStroke("released DELETE")  // Delete ao soltar
```

> As duas formas são equivalentes: `KeyStroke.getKeyStroke("ctrl S")` e `KeyStroke.getKeyStroke(KeyEvent.VK_S, InputEvent.CTRL_DOWN_MASK)` produzem o mesmo `KeyStroke` — a diferença é apenas legibilidade (string) vs. segurança de compilação (constantes).

### Performance e responsividade

Três eixos principais:

**1. Manter a EDT livre** A EDT (ver [[03-Dominios/Tecnologia/Java/Swing/05 - A Event Dispatch Thread|A Event Dispatch Thread (EDT)]]) é a única thread que pinta e despacha eventos. Qualquer I/O, consulta a banco ou cálculo pesado dentro de um listener bloqueia a EDT e congela a UI. A solução é delegar o trabalho a uma thread de background (ver [[03-Dominios/Tecnologia/Java/Swing/06 - SwingWorker e tarefas em background|SwingWorker e tarefas em background]]) e re-entrar na EDT via `invokeLater` para atualizar componentes.

**2. Models lazy/virtuais para grandes volumes de dados** `DefaultTableModel` e `DefaultListModel` carregam todos os dados em memória na inicialização. Com milhares de linhas, o tempo de construção trava a UI ao montar. A solução é um model customizado que carrega dados sob demanda (lazy) e, para `JTable`, combina com paginação ou virtualização. Ver [[03-Dominios/Tecnologia/Java/Swing/07 - MVC em Swing e os models|MVC em Swing e os models]].

**3. `repaint` de região em custom painting** Chamar `repaint()` sem argumentos solicita a repintura do componente inteiro. Em componentes grandes com custom painting (ver [[03-Dominios/Tecnologia/Java/Swing/10 - Custom painting e componentes customizados|Custom painting e componentes customizados]]), isso é desnecessariamente caro quando apenas uma área pequena mudou. A sobrecarga `repaint(int x, int y, int width, int height)` restringe o repaint à região mínima necessária, reduzindo o trabalho de pintura.

## Na prática

### `AbstractAction` "Salvar" reutilizado em `JButton` e `JMenuItem`

```java
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class ActionApiDemo {

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            // 1. Criar a Action uma única vez
            Action salvarAction = new AbstractAction("Salvar") {
                {
                    putValue(SHORT_DESCRIPTION, "Salva o documento atual");
                    putValue(MNEMONIC_KEY, KeyEvent.VK_S);
                    putValue(ACCELERATOR_KEY,
                        KeyStroke.getKeyStroke(KeyEvent.VK_S, InputEvent.CTRL_DOWN_MASK));
                }

                @Override
                public void actionPerformed(ActionEvent e) {
                    JOptionPane.showMessageDialog(null, "Salvando... (origem: " + e.getSource() + ")");
                }
            };

            // 2. Plugar o mesmo objeto em botão e item de menu
            JButton btnSalvar   = new JButton(salvarAction);
            JMenuItem miSalvar  = new JMenuItem(salvarAction);

            // 3. setEnabled(false) desabilita AMBOS — um único ponto de controle
            JCheckBox chkHabilitar = new JCheckBox("Habilitar Salvar", true);
            chkHabilitar.addActionListener(e ->
                salvarAction.setEnabled(chkHabilitar.isSelected())
            );

            JMenuBar menuBar = new JMenuBar();
            JMenu menuArquivo = new JMenu("Arquivo");
            menuArquivo.add(miSalvar);
            menuBar.add(menuArquivo);

            JPanel panel = new JPanel(new FlowLayout());
            panel.add(btnSalvar);
            panel.add(chkHabilitar);

            JFrame frame = new JFrame("Action API Demo");
            frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            frame.setJMenuBar(menuBar);
            frame.add(panel);
            frame.pack();
            frame.setVisible(true);
        });
    }
}
```

### Registrar `Ctrl+S` via `InputMap`/`ActionMap` com escopo de janela

```java
// Após criar o frame e a salvarAction acima:

JRootPane rootPane = frame.getRootPane();

// InputMap com WHEN_IN_FOCUSED_WINDOW: funciona independente de qual componente tem foco
rootPane.getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
        .put(KeyStroke.getKeyStroke("ctrl S"), "cmd.salvar");

// ActionMap aponta para a mesma Action já usada no botão e no menu
rootPane.getActionMap()
        .put("cmd.salvar", salvarAction);
```

Com esse registro, pressionar `Ctrl+S` enquanto a janela estiver em foco dispara `salvarAction.actionPerformed` — mesmo que o foco esteja num `JTextField`, num `JTable` ou em qualquer outro componente. E se `salvarAction.setEnabled(false)` for chamado, o atalho também é silenciado automaticamente.

## Armadilhas

### (1) Duplicar a lógica no listener do botão e no do item de menu (drift)

**Descrição.** É tentador adicionar um `ActionListener` inline no botão e um segundo `ActionListener` inline no item de menu. Com o tempo, as duas implementações divergem: uma recebe uma correção de bug, a outra não; uma ganha uma validação extra, a outra não. O comportamento fica inconsistente dependendo de como o usuário aciona a operação.

```java
// PROBLEMÁTICO: dois listeners com a mesma lógica, que vão divergir
btnSalvar.addActionListener(e -> {
    if (documento.isModificado()) salvar();
});
miSalvar.addActionListener(e -> {
    salvar(); // esqueceu a verificação isModificado()
});
```

**Fix:** extrair um único `AbstractAction` e plugar em ambos os componentes. A lógica existe num só lugar.

```java
// Fix: uma Action, zero drift
Action salvarAction = new AbstractAction("Salvar") {
    @Override
    public void actionPerformed(ActionEvent e) {
        if (documento.isModificado()) salvar();
    }
};
btnSalvar  = new JButton(salvarAction);
miSalvar   = new JMenuItem(salvarAction);
```

---

### (2) `KeyListener` para atalho de aplicação (problema de foco)

**Descrição.** `KeyListener` só recebe eventos do componente que tem o **foco de teclado** no instante do evento. Numa janela com `JTextField`, `JTable`, `JButton` e outros componentes, o usuário pode pressionar `Ctrl+S` enquanto um campo de texto está focado — mas o `KeyListener` registrado no painel não recebe o evento porque o painel não tem foco. O atalho silenciosamente não funciona, e o bug é difícil de reproduzir porque depende de onde o foco estava.

```java
// FRÁGIL: só dispara se 'panel' tiver foco exato
panel.addKeyListener(new KeyAdapter() {
    @Override
    public void keyPressed(KeyEvent e) {
        if (e.isControlDown() && e.getKeyCode() == KeyEvent.VK_S) salvar();
    }
});
```

**Fix:** usar `InputMap(WHEN_IN_FOCUSED_WINDOW)` no `rootPane`. O atalho funciona enquanto a janela tiver foco, independente do componente focado.

```java
// Fix: atalho de janela via InputMap/ActionMap
frame.getRootPane()
     .getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
     .put(KeyStroke.getKeyStroke("ctrl S"), "salvar");
frame.getRootPane()
     .getActionMap()
     .put("salvar", salvarAction);
```

---

### (3) Carregar tudo eager num `DefaultTableModel` com muitas linhas (UI trava ao montar)

**Descrição.** `DefaultTableModel` armazena todas as linhas como uma `Vector<Vector>` em memória. Inicializar um modelo com milhares de registros (resultado de uma query sem paginação, CSV grande) bloqueia a EDT durante a construção do modelo e a renderização inicial do `JTable`. A janela pode demorar vários segundos para aparecer, parecendo travada.

```java
// PROBLEMÁTICO: 50.000 linhas carregadas todas de uma vez na EDT
DefaultTableModel model = new DefaultTableModel(columns, 0);
for (Registro r : repositorio.listarTodos()) { // pode retornar 50k registros
    model.addRow(new Object[]{r.getId(), r.getNome(), r.getData()});
}
tabela.setModel(model);
```

**Fix:** implementar um `AbstractTableModel` que carrega dados por página (ou com limite), delegando o carregamento pesado a um `SwingWorker` e exibindo um indicador de progresso enquanto os dados chegam. Ver [[03-Dominios/Tecnologia/Java/Swing/07 - MVC em Swing e os models|MVC em Swing e os models]].

```java
// Fix: SwingWorker carrega em background; model atualizado aos poucos na EDT
new SwingWorker<List<Registro>, Registro>() {
    @Override
    protected List<Registro> doInBackground() {
        return repositorio.listarPagina(0, 200); // primeira página apenas
    }
    @Override
    protected void done() {
        try {
            modeloPaginado.setDados(get()); // atualiza na EDT
        } catch (Exception ex) { /* tratar */ }
    }
}.execute();
```

## Em entrevista

### Frase pronta (inglês)

> "For any operation accessible from multiple entry points — a toolbar button, a menu item, and a keyboard shortcut — I use an `AbstractAction`. The `Action` holds the label, icon, tooltip, and enabled state in one place; calling `setEnabled(false)` disables the button, the menu item, and the accelerator simultaneously, with no risk of drift between implementations. For keyboard shortcuts with application-wide scope, I register them via `InputMap` with `WHEN_IN_FOCUSED_WINDOW` on the root pane rather than with `KeyListener`, because `KeyListener` only fires when the exact component it is attached to has focus — which is fragile in any non-trivial window. Responsiveness comes down to keeping the EDT free: any I/O or heavy computation must run on a background thread via `SwingWorker`, results must re-enter the EDT through `invokeLater`, and large data sets must be loaded lazily through a custom `AbstractTableModel` rather than dumped into a `DefaultTableModel` all at once."

### Vocabulário

| Termo PT | Termo EN |
|----------|----------|
| ação centralizada | shared action / centralized action |
| estado habilitado | enabled state |
| atalho de teclado | keyboard shortcut / accelerator |
| vinculação de tecla | key binding |
| mapa de entrada | input map |
| mapa de ações | action map |
| escopo de foco | focus scope / focus condition |
| foco de janela | window focus / focused window |
| model preguiçoso | lazy model / virtual model |
| paginação de dados | data pagination |
| repintura de região | region repaint / dirty region repaint |
| drift de comportamento | behavior drift / implementation drift |

## Veja também

- [[03-Dominios/Tecnologia/Java/Swing/04 - O modelo de eventos|O modelo de eventos]]
- [[03-Dominios/Tecnologia/Java/Swing/05 - A Event Dispatch Thread|A Event Dispatch Thread (EDT)]]
- [[03-Dominios/Tecnologia/Java/Swing/06 - SwingWorker e tarefas em background|SwingWorker e tarefas em background]]
- [[03-Dominios/Tecnologia/Java/Swing/07 - MVC em Swing e os models|MVC em Swing e os models]]
- [[03-Dominios/Tecnologia/Java/Swing/10 - Custom painting e componentes customizados|Custom painting e componentes customizados]]
- [[03-Dominios/Tecnologia/Java/Swing/index|Swing (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#Action API|Action API]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#InputMap / ActionMap (key bindings)|InputMap / ActionMap]]

## Referências

- [How to Use Actions — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/uiswing/misc/action.html)
- [How to Use Key Bindings — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/uiswing/misc/keybinding.html)
- [Action — Javadoc Java 21 (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.desktop/javax/swing/Action.html)
- [AbstractAction — Javadoc Java 21 (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.desktop/javax/swing/AbstractAction.html)
- [InputMap — Javadoc Java 21 (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.desktop/javax/swing/InputMap.html)
- [ActionMap — Javadoc Java 21 (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.desktop/javax/swing/ActionMap.html)
