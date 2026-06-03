---
title: "Componentes e containers"
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
  - componentes
aliases:
  - Componentes Swing
  - JButton
  - JTable
---

# Componentes e containers

> [!abstract] TL;DR
> Swing oferece um catálogo rico de widgets dividido em dois grupos: **componentes** (controles que o usuário interage ou que exibem dados — `JButton`, `JLabel`, `JTable`, etc.) e **containers intermediários** (agrupam e organizam outros componentes — `JPanel`, `JScrollPane`, `JTabbedPane`). Todos herdam de `JComponent` e são lightweight. Saber quando usar cada widget — e quais precisam de um `JScrollPane` envolvendo-os ou de um model dedicado — é a base de qualquer formulário ou painel Swing funcional.

## O que é

O catálogo de componentes Swing pode ser visto como uma caixa de ferramentas de widgets, todos pertencentes ao pacote `javax.swing`. A divisão fundamental é:

- **Componentes (controles e exibidores):** widgets folha que o usuário vê ou manipula diretamente — botões, campos de texto, rótulos, listas, tabelas. Não contêm outros componentes Swing de forma significativa.
- **Containers intermediários:** classes que agrupam e dispõem componentes filhos, adicionando comportamentos como rolagem (`JScrollPane`), abas (`JTabbedPane`) ou divisão redimensionável (`JSplitPane`). Diferem dos **top-level containers** (`JFrame`, `JDialog`) — cobertos na nota 01 — porque não têm existência autônoma de janela: precisam estar dentro de um top-level container para aparecer na tela.

Todos os widgets — tanto componentes quanto containers intermediários — herdam de `javax.swing.JComponent`, que por sua vez herda de `java.awt.Container`. A hierarquia completa foi detalhada em [[03-Dominios/Java/Swing/01 - O modelo do Swing|O modelo do Swing]].

## Como funciona

### Controles básicos (`JButton`, `JLabel`, `JTextField`, `JTextArea`, `JPasswordField`)

Os controles mais usados em formulários comuns:

| Classe | Papel |
|--------|-------|
| `JButton` | Botão de ação; dispara `ActionEvent` quando clicado. |
| `JLabel` | Rótulo estático de texto ou ícone; não é focável por padrão. |
| `JTextField` | Campo de texto de linha única; ideal para entradas curtas. |
| `JTextArea` | Área de texto multi-linha; não tem scroll próprio — requer `JScrollPane`. |
| `JPasswordField` | Subclasse de `JTextField` que mascara a entrada; use `getPassword()` (retorna `char[]`) em vez de `getText()`. |

`JLabel` aceita HTML simples como conteúdo (ex.: `new JLabel("<html><b>Nome:</b></html>")`) — útil para formatação leve, mas pode impactar performance se usado em excesso em listas ou tabelas.

### Seleção (`JCheckBox`/`JRadioButton` + `ButtonGroup`, `JComboBox`, `JList`)

Controles de escolha entre opções:

**`JCheckBox`** — caixa de marcação independente; cada instância tem seu próprio estado booleano (`isSelected()`). Adequado para múltiplas seleções independentes.

**`JRadioButton` + `ButtonGroup`** — botões de escolha mutuamente exclusivos. A exclusividade não é automática: é necessário adicionar todos os `JRadioButton` relacionados a um `ButtonGroup`. O grupo não é um componente visual — não precisa ser adicionado ao painel.

```java
ButtonGroup group = new ButtonGroup();
JRadioButton rbActive   = new JRadioButton("Ativo");
JRadioButton rbInactive = new JRadioButton("Inativo");
group.add(rbActive);
group.add(rbInactive);
// apenas rbActive e rbInactive são adicionados ao painel, não o group
panel.add(rbActive);
panel.add(rbInactive);
```

**`JComboBox<E>`** — lista suspensa (dropdown). No modo padrão, permite selecionar um item; com `setEditable(true)`, também aceita digitação livre. Internamente usa um `ComboBoxModel`.

**`JList<E>`** — lista de itens com seleção simples ou múltipla. **Não possui rolagem própria** — deve ser embrulhada em `JScrollPane` na quase totalidade dos usos reais. O model (`ListModel`) é detalhado em outra nota do galho.

### Componentes orientados a dados (`JTable`, `JTree`)

Componentes para exibir estruturas de dados mais complexas:

**`JTable`** — exibe dados em grade de linhas e colunas. É o componente mais poderoso e ao mesmo tempo o mais exigente do catálogo: funciona bem com poucos dados hardcoded, mas em uso real necessita de um `TableModel` adequado para lidar com tipos, edição e notificação de mudanças. Como `JList`, **não tem scroll próprio** — deve ser adicionado via `new JScrollPane(table)`. Os cabeçalhos de coluna só aparecem quando o `JTable` está dentro de um `JScrollPane`.

**`JTree`** — exibe dados hierárquicos (árvore). Requer um `TreeModel` para dados reais; o `DefaultTreeModel` com `DefaultMutableTreeNode` cobre a maioria dos casos simples. Também necessita de `JScrollPane` para conteúdos extensos.

> [!note] Models em detalhe
> A arquitetura MVC dos componentes orientados a dados (`JTable`, `JTree`, `JList`) — incluindo `TableModel`, `TreeModel`, `ListModel` e como dispará eventos de atualização corretamente — é o tema de [[03-Dominios/Java/Swing/07 - MVC em Swing e os models|MVC em Swing e os models]].

### Containers intermediários (`JPanel`, `JScrollPane`, `JTabbedPane`, `JSplitPane`)

Containers que organizam componentes dentro de uma janela:

**`JPanel`** — container genérico e mais usado. Aceita qualquer `LayoutManager`; o padrão é `FlowLayout`. Pode ser aninhado livremente para compor layouts complexos.

**`JScrollPane`** — adiciona barras de rolagem (horizontal e/ou vertical) ao componente que envolve. A maioria dos componentes scrolláveis (`JTextArea`, `JList`, `JTable`, `JTree`) deve ser passada ao construtor do `JScrollPane`, não adicionada diretamente ao painel pai:

```java
JTextArea textArea = new JTextArea(10, 40);
JScrollPane scrollPane = new JScrollPane(textArea);
panel.add(scrollPane);  // adiciona o scroll, não o textArea
```

**`JTabbedPane`** — painel com abas navegáveis. Cada aba pode conter um componente arbitrário (tipicamente um `JPanel`). Abas podem ser posicionadas em cima, baixo, esquerda ou direita via `setTabPlacement`.

```java
JTabbedPane tabbedPane = new JTabbedPane();
tabbedPane.addTab("Geral", generalPanel);
tabbedPane.addTab("Avançado", advancedPanel);
```

**`JSplitPane`** — divide o espaço em dois painéis com um divisor arrastável. Pode ser horizontal (`HORIZONTAL_SPLIT`) ou vertical (`VERTICAL_SPLIT`). Útil para layouts mestre-detalhe.

```java
JSplitPane split = new JSplitPane(JSplitPane.HORIZONTAL_SPLIT, listPanel, detailPanel);
split.setDividerLocation(200);  // posição inicial em pixels
```

### Menus, toolbars e diálogos (`JMenuBar`/`JMenu`/`JMenuItem`, `JToolBar`, `JDialog`/`JOptionPane`)

**Sistema de menus:** a barra de menus (`JMenuBar`) é adicionada ao frame via `frame.setJMenuBar(menuBar)` — fora do content pane. Cada `JMenu` dentro dela pode conter `JMenuItem`, `JCheckBoxMenuItem`, `JRadioButtonMenuItem` e submenus (`JMenu` aninhado).

```java
JMenuBar menuBar = new JMenuBar();
JMenu fileMenu = new JMenu("Arquivo");
fileMenu.add(new JMenuItem("Abrir"));
fileMenu.add(new JMenuItem("Salvar"));
fileMenu.addSeparator();
fileMenu.add(new JMenuItem("Sair"));
menuBar.add(fileMenu);
frame.setJMenuBar(menuBar);
```

**`JToolBar`** — barra de ferramentas com botões e outros controles. Por padrão é flutuante (pode ser destacada pelo usuário); esse comportamento é controlado por `setFloatable(false)`.

**`JDialog`** — janela de diálogo customizável. Pode ser modal (bloqueia interação com a janela pai enquanto aberta) ou não-modal.

**`JOptionPane`** — fornece diálogos padrão prontos para uso imediato (confirmação, mensagem, input, seleção de opção) sem precisar construir um `JDialog` do zero:

```java
JOptionPane.showMessageDialog(frame, "Operação concluída.", "Info", JOptionPane.INFORMATION_MESSAGE);
int choice = JOptionPane.showConfirmDialog(frame, "Deseja continuar?", "Confirmar", JOptionPane.YES_NO_OPTION);
```

## Na prática

Formulário simples: dois campos de texto com rótulos, um botão de confirmação e um `JOptionPane` de feedback.

```java
import javax.swing.*;
import java.awt.*;

public class CustomerForm {

    private static void buildAndShow() {
        JFrame frame = new JFrame("Cadastro");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        JPanel form = new JPanel(new GridLayout(3, 2, 6, 6));

        JLabel nameLabel  = new JLabel("Nome:");
        JTextField nameField = new JTextField(20);

        JLabel emailLabel = new JLabel("E-mail:");
        JTextField emailField = new JTextField(20);

        JButton saveBtn = new JButton("Salvar");
        saveBtn.addActionListener(e ->
            JOptionPane.showMessageDialog(
                frame,
                "Salvo: " + nameField.getText(),
                "Sucesso",
                JOptionPane.INFORMATION_MESSAGE
            )
        );

        form.add(nameLabel);  form.add(nameField);
        form.add(emailLabel); form.add(emailField);
        form.add(new JLabel());  // célula vazia
        form.add(saveBtn);

        frame.add(form, BorderLayout.CENTER);
        frame.pack();
        frame.setLocationRelativeTo(null);  // centraliza na tela
        frame.setVisible(true);
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(CustomerForm::buildAndShow);
    }
}
```

```text
// Resultado: janela com dois campos rotulados e botão "Salvar".
// Ao clicar, exibe diálogo: "Salvo: <texto digitado>".
```

Pontos relevantes:
- `GridLayout(3, 2, 6, 6)` organiza rótulo + campo em pares de colunas, com gaps horizontal/vertical de 6 px.
- O `ActionListener` é adicionado inline via lambda — padrão moderno em vez de classe anônima.
- `setLocationRelativeTo(null)` centraliza a janela na tela; deve ser chamado depois de `pack()`.

## Armadilhas

### (1) `JTextArea` e `JList` sem `JScrollPane` — conteúdo cortado, sem rolagem

**O problema:** `JTextArea` e `JList` não têm scrollbar incorporado. Adicioná-los diretamente a um painel faz o conteúdo ser cortado quando ultrapassa o espaço visível — sem nenhuma barra de rolagem para navegar.

```java
// hipotético — errado: JTextArea sem scroll
JTextArea log = new JTextArea(10, 40);
panel.add(log);  // conteúdo além das 10 linhas fica inacessível
```

**Fix:** sempre embrulhar em `JScrollPane` antes de adicionar ao container pai.

```java
panel.add(new JScrollPane(log));
```

O mesmo vale para `JList` e `JTable`.

---

### (2) `JList`/`JTable` populados com dados crus sem model adequado

**O problema:** construir um `JList<String>` com array estático ou preencher um `DefaultTableModel` acrescentando linhas manualmente funciona para protótipos, mas não notifica a view quando os dados mudam programaticamente, não separa dados de apresentação e dificulta sorting/filtering. Em uma entrevista, usar apenas `JList(new String[]{"a","b"})` sinaliza desconhecimento de MVC.

```java
// hipotético — aceitável só para demos estáticos
JList<String> list = new JList<>(new String[]{"Opção A", "Opção B"});
```

**Fix:** usar `DefaultListModel<E>` (para `JList`) ou um `DefaultTableModel` / `AbstractTableModel` customizado (para `JTable`), que disparam os eventos corretos de `ListDataEvent`/`TableModelEvent` ao inserir, remover ou modificar dados. O assunto é detalhado em [[03-Dominios/Java/Swing/07 - MVC em Swing e os models|MVC em Swing e os models]].

```java
DefaultListModel<String> model = new DefaultListModel<>();
model.addElement("Opção A");
model.addElement("Opção B");
JList<String> list = new JList<>(model);
// model.addElement("Opção C") → view atualiza automaticamente
```

---

### (3) `JOptionPane` ou construção de `JDialog` chamados fora da EDT

**O problema:** `JOptionPane.showMessageDialog` e a construção de qualquer componente Swing são operações de UI — devem rodar na EDT. Chamá-los de uma thread de trabalho (callback de rede, `ExecutorService`, etc.) viola o contrato single-threaded do Swing e pode produzir deadlocks ou diálogos que nunca fecham corretamente.

```java
// hipotético — errado: diálogo fora da EDT
executor.submit(() -> {
    String result = fetchFromNetwork();
    JOptionPane.showMessageDialog(frame, result);  // fora da EDT
});
```

**Fix:** agendar via `SwingUtilities.invokeLater` dentro do callback.

```java
executor.submit(() -> {
    String result = fetchFromNetwork();
    SwingUtilities.invokeLater(() ->
        JOptionPane.showMessageDialog(frame, result)
    );
});
```

## Em entrevista

### Frase pronta (inglês)

> "Swing ships a rich widget catalog divided into two broad categories: leaf components — controls like `JButton`, `JTextField`, `JTable`, and `JList` that the user interacts with directly — and intermediate containers like `JPanel`, `JScrollPane`, `JTabbedPane`, and `JSplitPane` that organize and decorate other components. A common mistake is adding scrollable components like `JTextArea`, `JList`, or `JTable` directly to a panel instead of wrapping them in a `JScrollPane`; without it, content simply gets clipped. For data-heavy components such as `JTable` and `JList`, proper use requires understanding the model layer — `TableModel` and `ListModel` — because the view only updates when the model fires the right events; populating them with static arrays works for demos but breaks as soon as data needs to change at runtime."

### Vocabulário

| Termo PT | Termo EN |
|----------|----------|
| componente folha / controle | leaf component / control |
| container intermediário | intermediate container |
| caixa de seleção | check box (`JCheckBox`) |
| lista suspensa | combo box / drop-down list (`JComboBox`) |
| painel com abas | tabbed pane (`JTabbedPane`) |
| painel com divisor | split pane (`JSplitPane`) |
| painel de rolagem | scroll pane (`JScrollPane`) |
| barra de menus | menu bar (`JMenuBar`) |
| diálogo de opção | option pane (`JOptionPane`) |
| model da lista | list model (`ListModel`) |

## Veja também

- [[03-Dominios/Java/Swing/01 - O modelo do Swing|O modelo do Swing]]
- [[03-Dominios/Java/Swing/03 - Layout managers|Layout managers]]
- [[03-Dominios/Java/Swing/07 - MVC em Swing e os models|MVC em Swing e os models]]
- [[03-Dominios/Java/Swing/index|Swing (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Dicionário de Java#JComponent|JComponent]]

## Referências

- [A Visual Guide to Swing Components — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/uiswing/components/componentlist.html)
- [Using Swing Components — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/uiswing/components/index.html)
- [javax.swing — Javadoc Java 21 (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.desktop/javax/swing/package-summary.html)
- [JComponent — Javadoc Java 21 (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.desktop/javax/swing/JComponent.html)
