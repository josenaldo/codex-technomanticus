---
title: "Renderers e editors"
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
  - renderer
  - table
aliases:
  - Cell renderer
  - TableCellRenderer
  - Cell editor
---

# Renderers e editors

> [!abstract] TL;DR
> No Swing, **renderer** e **editor** são os dois lados de uma célula: o renderer define *como ela é pintada* (display permanente), o editor define *como ela é modificada* (componente temporário ativo durante edição). Ambos interagem com os models da nota 07 — o model fornece o dado cru; o renderer o formata visualmente; o editor o grava de volta via `setValueAt`. O ponto central de performance é o **rubber-stamp pattern**: um único componente renderer é reusado para pintar *todas* as células do mesmo tipo a cada repaint — não há um componente separado por célula. Por isso, o renderer deve ser **stateless por chamada**: nunca registre listeners nele e nunca crie um `new JLabel()` a cada invocação de `getTableCellRendererComponent`. O ponto central de corretude do editor é sempre confirmar a edição via `stopCellEditing` / `fireEditingStopped`; sem isso, o valor digitado pelo usuário se perde silenciosamente.

## O que é

No Swing, toda célula de `JTable` ou item de `JList` tem dois objetos responsáveis por sua apresentação e modificação:

- **Renderer** (`TableCellRenderer` / `ListCellRenderer`) — define **como** a célula é *desenhada* no estado de leitura. É ativado a cada repaint de qualquer célula visível. Ele não faz parte da hierarquia de componentes da janela: é um "carimbo" configurável que a `JTable` usa para pintar cada célula e descarta em seguida.
- **Editor** (`TableCellEditor`) — define **como** a célula é *editada* quando o usuário clica para modificar seu valor. Ao contrário do renderer, o componente do editor *é* inserido temporariamente na hierarquia da `JTable` durante a edição e removido assim que a edição termina.

Os dois papéis se complementam e **pairam sobre os models** da [[03-Dominios/Java/Swing/07 - MVC em Swing e os models|nota 07]]: o model (`TableModel`) guarda os dados; o renderer os apresenta formatados; o editor os modifica e os grava de volta via `setValueAt`. Separar apresentação do model é exatamente a armadilha (3) da nota 07 — devolver `"R$ 199,90"` de `getValueAt` quebra a separação; o lugar certo para formatar é o renderer.

## Como funciona

### `TableCellRenderer` / `ListCellRenderer` e o rubber-stamp pattern

A interface central é `TableCellRenderer`:

```java
Component getTableCellRendererComponent(
    JTable table,
    Object value,
    boolean isSelected,
    boolean hasFocus,
    int row,
    int column
)
```

O Javadoc do `ListCellRenderer` (Java 21) usa explicitamente o termo: a interface *"identifies components that can be used as 'rubber stamps' to paint the cells in a JList"*. O `TableCellRenderer` segue o mesmo padrão de reuso descrito nos tutoriais da Oracle, mas o Javadoc do `TableCellRenderer` em si não emprega o termo "rubber stamp". Em ambos os casos, um **único** componente renderer é reconfigurado e reusado para pintar *cada* célula visível a cada repaint — não existe um componente separado por célula.

O que acontece internamente:

1. Para cada célula visível, a `JTable` chama `getTableCellRendererComponent(...)`.
2. O método configura o componente (cor de fundo, texto, borda etc.) e o *retorna*.
3. A `JTable` chama `paint()` nesse componente para renderizar a célula.
4. O mesmo componente é reconfigurado para a próxima célula.

Consequência direta: o renderer **não pode guardar estado entre chamadas** — ele é compartilhado. Listeners registrados no renderer se propagam para todas as células; estado mutável de uma célula "vaza" para a próxima. A regra é: configure tudo dentro de `getTableCellRendererComponent` e retorne `this`.

Para `ListCellRenderer<E>`, o método análogo é:

```java
Component getListCellRendererComponent(
    JList<? extends E> list,
    E value,
    int index,
    boolean isSelected,
    boolean cellHasFocus
)
```

### `DefaultTableCellRenderer` — estender vs implementar do zero

`DefaultTableCellRenderer` é a implementação padrão de `TableCellRenderer`. Detalhe importante: **ela estende `JLabel`**. Por isso, estender `DefaultTableCellRenderer` é a forma idiomática de criar renderers customizados — você ganha pintura de texto, borda de foco, cores de seleção e herança de look-and-feel de graça, e só sobrescreve o que precisa mudar.

Dois pontos de extensão comuns:

- **Sobrescrever `setValue(Object value)`** — chamado internamente antes do repaint; ideal para formatar o texto exibido sem reescrever a lógica de seleção/foco.
- **Sobrescrever `getTableCellRendererComponent(...)`** — necessário quando a customização vai além do texto (cores de fundo, bordas condicionais, outros componentes).

```java
// Estendendo DefaultTableCellRenderer — acesso a getTableCellRendererComponent completo
public class StatusCellRenderer extends DefaultTableCellRenderer {

    @Override
    public Component getTableCellRendererComponent(
            JTable table, Object value,
            boolean isSelected, boolean hasFocus,
            int row, int column) {

        // deixa a lógica padrão (seleção, borda de foco) rodar primeiro
        super.getTableCellRendererComponent(
                table, value, isSelected, hasFocus, row, column);

        // só customiza o que importa — aqui, a cor de fundo por status
        if (!isSelected) {
            String status = (value != null) ? value.toString() : "";
            setBackground(switch (status) {
                case "PAID"    -> new Color(200, 240, 200);
                case "PENDING" -> new Color(255, 245, 180);
                case "OVERDUE" -> new Color(255, 200, 200);
                default        -> table.getBackground();
            });
        }

        return this;
    }
}
```

Implementar `TableCellRenderer` do zero (sem estender `DefaultTableCellRenderer`) faz sentido quando o componente visual não é um `JLabel` — por exemplo, um `JProgressBar` ou um painel composto.

### Cell editors — `TableCellEditor`, `DefaultCellEditor` com `JTextField` / `JComboBox` / `JCheckBox`

A interface `TableCellEditor` estende `CellEditor` e exige um método principal:

```java
Component getTableCellEditorComponent(
    JTable table,
    Object value,
    boolean isSelected,
    int row,
    int column
)
```

O componente retornado é *inserido* na `JTable` durante a edição e *removido* quando ela termina (confirmada ou cancelada).

`DefaultCellEditor` é a implementação padrão e aceita três tipos de componente no construtor:

| Construtor | Componente usado | Tipo de dado típico |
|---|---|---|
| `new DefaultCellEditor(new JTextField())` | `JTextField` | `String`, texto livre |
| `new DefaultCellEditor(new JCheckBox())` | `JCheckBox` | `Boolean` |
| `new DefaultCellEditor(new JComboBox<>(...))` | `JComboBox` | enumeração, lista fixa |

Os métodos herdados de `CellEditor` mais relevantes:

- `stopCellEditing()` — confirma a edição; a tabela chama `getCellEditorValue()` e grava via `setValueAt`. Retorna `false` se a validação falhar e a edição deve continuar.
- `cancelCellEditing()` — cancela sem gravar; dispara `fireEditingCancelled()`.
- `getCellEditorValue()` — devolve o valor editado.

### Renderer vs editor — display permanente vs componente temporário durante edição

| Aspecto | Renderer | Editor |
|---|---|---|
| Quando ativo | em todo repaint de toda célula visível | só durante a edição de uma célula específica |
| Componente na hierarquia | não — é um carimbo, nunca adicionado ao container | sim — inserido temporariamente na `JTable` |
| Stateless? | obrigatoriamente (compartilhado entre todas as células) | não — pode guardar estado entre o início e o fim da edição |
| Confirma mudança | não altera dados | via `stopCellEditing()` → `getCellEditorValue()` → `setValueAt` |
| Interface base | `TableCellRenderer` / `ListCellRenderer` | `TableCellEditor` (estende `CellEditor`) |

## Na prática

### Renderer: colorir fundo da coluna de status conforme o valor

O exemplo abaixo colore o fundo de uma coluna `"Status"` de `Order` (dado cru `String` — formatação é responsabilidade do renderer, não do model):

```java
public class OrderStatusRenderer extends DefaultTableCellRenderer {

    @Override
    public Component getTableCellRendererComponent(
            JTable table, Object value,
            boolean isSelected, boolean hasFocus,
            int row, int column) {

        // configura texto, borda de foco e cores padrão de seleção
        super.getTableCellRendererComponent(
                table, value, isSelected, hasFocus, row, column);

        if (!isSelected) {
            String status = (value != null) ? value.toString() : "";
            Color bg = switch (status) {
                case "PAID"      -> new Color(198, 239, 206);
                case "PENDING"   -> new Color(255, 235, 156);
                case "OVERDUE"   -> new Color(255, 199, 206);
                default          -> table.getBackground();
            };
            setBackground(bg);
        }

        return this;   // retorna THIS — o carimbo rubber-stamp
    }
}
```

Registro na coluna correta:

```java
int statusCol = 2;   // índice da coluna "Status" no model
table.getColumnModel().getColumn(statusCol)
     .setCellRenderer(new OrderStatusRenderer());
```

Para registrar por tipo (toda coluna cujo `getColumnClass` devolva aquela classe):

```java
table.setDefaultRenderer(OrderStatus.class, new OrderStatusRenderer());
```

### Editor: `JComboBox` numa coluna de status

Quando o status é uma enumeração, um `JComboBox` como editor impede valores inválidos:

```java
JComboBox<String> statusCombo = new JComboBox<>(
        new String[]{"PAID", "PENDING", "OVERDUE"});

TableColumn statusColumn = table.getColumnModel().getColumn(2);
statusColumn.setCellEditor(new DefaultCellEditor(statusCombo));
```

Ao confirmar a seleção, `DefaultCellEditor` chama automaticamente `stopCellEditing()`, que dispara `getCellEditorValue()` e a `JTable` grava o valor via `model.setValueAt(...)`.

## Armadilhas

### (1) Criar `new JLabel()` (ou outro componente) a cada chamada de `getTableCellRendererComponent`

**Descrição.** O método é chamado a cada repaint de cada célula visível. Com centenas de linhas e scroll, isso acontece dezenas de vezes por segundo. Criar uma nova instância de componente a cada invocação despeja objetos na heap contínuamente — GC frequente, jank visual, performance degrada com o tamanho da tabela.

```java
// RUIM — instancia um novo JLabel a cada célula pintada
public Component getTableCellRendererComponent(...) {
    JLabel label = new JLabel(value.toString());   // novo objeto sempre!
    label.setBackground(computeColor(value));
    return label;
}
```

**Fix (1 linha):** configure `this` (o próprio renderer, que é o carimbo) e retorne `this` — o rubber-stamp pattern.

```java
setText(value.toString());   // configura this
setBackground(computeColor(value));
return this;                 // retorna o carimbo reusado
```

---

### (2) Guardar estado mutável ou registrar listener no renderer

**Descrição.** O renderer é uma única instância compartilhada entre *todas* as células. Se você registrar um `ActionListener` nele no construtor (ou pior, em cada chamada), ele dispara múltiplas vezes — uma para cada célula que o reusou. Se guardar estado mutável entre chamadas (ex.: um flag `lastRow`), esse estado "vaza" de uma célula para outra, produzindo renderização incorreta de forma difícil de reproduzir.

```java
// RUIM — listener acumulado e estado compartilhado
public MyRenderer() {
    addActionListener(e -> handleClick());   // registrado uma vez, mas compartilhado
}
```

**Fix (1 linha):** o renderer deve ser **stateless por chamada** — toda configuração acontece dentro de `getTableCellRendererComponent`, baseada apenas nos parâmetros recebidos; nunca acumule listeners.

---

### (3) Editor que não confirma o valor — valor digitado se perde silenciosamente

**Descrição.** Se um editor customizado (especialmente um baseado em `AbstractCellEditor`) não chama `stopCellEditing()` / `fireEditingStopped()` ao término da interação, a `JTable` nunca coleta `getCellEditorValue()` e nunca chama `setValueAt`. O usuário digita algo, clica fora, e o valor volta ao original sem nenhuma mensagem de erro — o bug mais silencioso do Swing.

```java
// RUIM — editor de diálogo que fecha o dialog mas não sinaliza o fim da edição
button.addActionListener(e -> {
    dialog.setVisible(true);
    // esqueceu de chamar fireEditingStopped()!
});
```

**Fix (1 linha):** chame `fireEditingStopped()` ao confirmar a edição para que a `JTable` colete o valor e o renderer reapareça.

```java
fireEditingStopped();   // sinaliza fim da edição; JTable chama getCellEditorValue()
```

## Em entrevista

### Frase pronta (inglês)

> "In Swing, `TableCellRenderer` and `TableCellEditor` are the two sides of a cell: the renderer is responsible for *displaying* a cell's value at all times, while the editor is a temporary component that takes over *only while the user is actively editing*. The key insight for the renderer is the rubber-stamp pattern — a single renderer instance is reused and reconfigured to paint every visible cell on every repaint, so it must never hold mutable state between calls and must never register listeners, since it's shared across all cells. The editor, on the other hand, is inserted into the table's component hierarchy only during editing and is removed when `stopCellEditing` is called; forgetting that call is the classic footgun — the user's input is silently discarded because the table never invokes `getCellEditorValue` and `setValueAt`."

### Vocabulário

| Termo PT | Termo EN |
|---|---|
| renderizador de célula | cell renderer (`TableCellRenderer`) |
| editor de célula | cell editor (`TableCellEditor`) |
| padrão carimbo de borracha | rubber-stamp pattern |
| componente reusado entre células | shared / reused renderer component |
| confirmar edição | stop cell editing (`stopCellEditing`) |
| disparar fim de edição | fire editing stopped (`fireEditingStopped`) |
| sem estado entre chamadas | stateless per call |
| registrar renderer por tipo | set default renderer by type (`setDefaultRenderer`) |

## Veja também

- [[03-Dominios/Java/Swing/02 - Componentes e containers|Componentes e containers]]
- [[03-Dominios/Java/Swing/07 - MVC em Swing e os models|MVC em Swing e os models]]
- [[03-Dominios/Java/Swing/index|Swing (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Dicionário de Java#cell renderer|cell renderer]]
- [[03-Dominios/Java/Dicionário de Java#cell editor|cell editor]]

## Referências

- [How to Use Tables — Using Custom Renderers (The Java Tutorials, Oracle)](https://docs.oracle.com/javase/tutorial/uiswing/components/table.html)
- [How to Use Tables — Using Other Editors (The Java Tutorials, Oracle)](https://docs.oracle.com/javase/tutorial/uiswing/components/table.html)
- [TableCellRenderer — Javadoc Java 21 (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.desktop/javax/swing/table/TableCellRenderer.html)
- [ListCellRenderer — Javadoc Java 21 (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.desktop/javax/swing/ListCellRenderer.html)
- [TableCellEditor — Javadoc Java 21 (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.desktop/javax/swing/table/TableCellEditor.html)
