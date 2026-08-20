---
title: "MVC em Swing e os models"
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
  - mvc
  - model
aliases:
  - MVC em Swing
  - TableModel
  - Separable model
---

# MVC em Swing e os models

> [!abstract] TL;DR
> O Swing não implementa um MVC clássico de três objetos separados; usa uma **separable model architecture**: cada componente tem um **model** que guarda os dados, enquanto **view e controller ficam fundidos** num único objeto — o *UI delegate* (a classe `*UI` do look-and-feel). Você troca e customiza o model livremente; raramente toca na view+controller. Os models centrais são `TableModel` (para `JTable`), `ListModel`/`ComboBoxModel` (para `JList`/`JComboBox`), `Document` (texto) e `TreeModel` (`JTree`). A regra de ouro: o componente *"does not contain or cache data; it is simply a view of your data"* — então a view só repinta quando o model **dispara o evento certo** (`fireTableRowsInserted`, `fireTableDataChanged`, etc.). Mutar a `List` interna sem disparar o evento deixa a tela dessincronizada. Em uso real, prefira um `AbstractTableModel` tipado a um `DefaultTableModel` cru de `Object[][]`.

## O que é

"MVC em Swing" é uma expressão imprecisa, e numa entrevista vale corrigir o termo: o Swing usa uma variação chamada **separable model architecture** (arquitetura de model separável). No MVC clássico há **três** objetos distintos — Model, View, Controller. O Swing fundiu dois deles:

- **Model** — objeto separado, que guarda os **dados** (e o estado de seleção). É o que você customiza no dia a dia.
- **View + Controller** — fundidos num único objeto, o **UI delegate** (a classe terminada em `UI`, ex.: `BasicTableUI`), fornecido pelo look-and-feel. Ele desenha o componente **e** interpreta a entrada do usuário.

A razão da fusão é pragmática: separar pintura de tratamento de input rendia pouco e acoplava muito (ambos precisam de acesso íntimo ao mesmo estado de baixo nível). Separar o **model**, ao contrário, rende muito — é o eixo que permite plugar seus próprios dados num `JTable` ou `JList` sem reescrever a renderização.

O ponto-chave, na formulação da Oracle para `JTable`: *"JTable does not contain or cache data; it is simply a view of your data."* O componente é uma janela sobre o model; quem detém a verdade dos dados é o model. Disso decorre tudo o mais nesta nota.

## Como funciona

### Separable model (por que separar dados de apresentação; um model por componente)

A separação dados/apresentação é o que dá ao Swing flexibilidade real:

- **Seus dados, sua estrutura.** O tutorial é explícito: *"Your model might hold its data in an array, vector, or hash map, or it might get the data from an outside source such as a database. It might even generate the data at execution time."* O componente não impõe um formato de armazenamento.
- **Troca de view sem tocar nos dados.** O mesmo `TableModel` pode alimentar um `JTable` com qualquer look-and-feel; o model não sabe como é pintado.
- **Notificação por eventos.** Como o componente não cacheia dados, ele depende do model para avisar quando algo muda — via eventos. É a espinha dorsal da reatividade da view (detalhada adiante).

Cada componente orientado a dados tem **seu próprio tipo de model**, com uma interface, uma classe abstrata de conveniência e uma implementação default:

| Componente | Interface do model | Classe de conveniência | Default pronto |
|------------|--------------------|------------------------|----------------|
| `JTable` | `TableModel` | `AbstractTableModel` | `DefaultTableModel` |
| `JList` | `ListModel` | `AbstractListModel` | `DefaultListModel` |
| `JComboBox` | `ComboBoxModel` | (estende `ListModel`) | `DefaultComboBoxModel` |
| `JTree` | `TreeModel` | — | `DefaultTreeModel` |
| `JTextArea`/`JTextField` | `Document` | `AbstractDocument` | `PlainDocument` |

> [!info] Models de UI vs models de seleção
> Cada componente tem na verdade **dois** models: o de **dados** (ex.: `TableModel`) e o de **seleção** (ex.: `ListSelectionModel`). Esta nota cobre os dois — a seleção aparece na seção de selection models.

### `TableModel` / `AbstractTableModel` / `DefaultTableModel`

A interface `TableModel` *"specifies the methods the `JTable` will use to interrogate a tabular data model."* Os métodos essenciais:

```java
int     getRowCount();                              // quantas linhas
int     getColumnCount();                           // quantas colunas
String  getColumnName(int columnIndex);             // título da coluna
Class<?> getColumnClass(int columnIndex);           // tipo da coluna (renderer/editor default)
boolean isCellEditable(int rowIndex, int columnIndex);
Object  getValueAt(int rowIndex, int columnIndex);  // valor de uma célula
void    setValueAt(Object aValue, int rowIndex, int columnIndex);
void    addTableModelListener(TableModelListener l);
void    removeTableModelListener(TableModelListener l);
```

`getColumnClass` merece destaque: ele *"is used by the `JTable` to set up a default renderer and editor for the column"* — devolver `Boolean.class` faz a coluna virar checkboxes; `Integer.class`/`Number` alinha à direita. (Como a view escolhe o renderer a partir desse tipo é o tema de [[03-Dominios/Tecnologia/Java/Swing/08 - Renderers e editors|Renderers e editors]].)

Os três níveis de implementação:

- **`TableModel` (interface)** — você implementa **tudo**, inclusive a gestão de listeners. Raro.
- **`AbstractTableModel`** — *"provides default implementations for most of the methods... It takes care of the management of listeners and provides some conveniences for generating `TableModelEvents`."* Você só precisa fornecer `getRowCount()`, `getColumnCount()` e `getValueAt(...)`. **É a escolha idiomática** para models customizados. Para uma tabela **editável**, é preciso também sobrescrever `isCellEditable` (que por padrão retorna `false`) e `setValueAt`.
- **`DefaultTableModel`** — armazenamento pronto baseado em `Vector`/`Object[][]`. Conveniente para protótipos, mas perde type-safety (tudo é `Object`) e não modela um domínio.

### `ListModel` / `AbstractListModel` / `DefaultListModel` e `ComboBoxModel`

O `JList` segue o mesmo padrão de três níveis. O tutorial descreve as opções:

1. **`DefaultListModel`** — *"everything is pretty much taken care of for you."* Mutável: `addElement`, `remove`, `insertElementAt`.
2. **`AbstractListModel`** — *"you manage the data and invoke the 'fire' methods... you must subclass `AbstractListModel` and implement the `getSize` and `getElementAt` methods inherited from the `ListModel` interface."*
3. **`ListModel`** — *"you manage everything."*

Uma armadilha sutil na construção: *"If you initialize a list with an array or vector, the constructor implicitly creates a default list model. The default list model is **immutable** — you cannot add, remove, or replace items in the list."* Ou seja, `new JList<>(new String[]{...})` gera um model que você não pode mutar depois.

O `ComboBoxModel` **estende** `ListModel`, acrescentando o conceito de **item selecionado** (`getSelectedItem` / `setSelectedItem`). O default é `DefaultComboBoxModel`.

### `Document` (modelo de texto) e `TreeModel` (menção)

Nem todo model é uma lista de linhas:

- **`Document`** — é o model dos componentes de texto (`JTextField`, `JTextArea`, `JEditorPane`). Modela o conteúdo textual como uma sequência de caracteres com atributos e estrutura (elementos), não como uma `String` simples. Por isso edições de texto disparam `DocumentEvent`, e validação/máscara de entrada se faz no `Document` (via `DocumentFilter`), não no componente.
- **`TreeModel`** — model do `JTree`, que expõe dados **hierárquicos** (um nó-raiz, e para cada nó seus filhos). O `DefaultTreeModel` com `DefaultMutableTreeNode` cobre a maioria dos casos. Mencionado aqui para completar o mapa; o foco desta nota é `TableModel`/`ListModel`.

### Model listeners (`TableModelListener`) e como a view atualiza via eventos

Como o componente *não cacheia dados*, ele se registra como **listener do model**. Quando o model muda, ele dispara um evento; a view o recebe e repinta a região afetada. O tutorial: *"Whenever items are added to, removed from, or modified in a list, the list model fires list data events."*

Para tabelas, `AbstractTableModel` oferece métodos `fire*` que constroem e despacham o `TableModelEvent` certo:

| Método | Quando usar |
|--------|-------------|
| `fireTableRowsInserted(firstRow, lastRow)` | linhas `[firstRow, lastRow]` inseridas |
| `fireTableRowsDeleted(firstRow, lastRow)` | linhas `[firstRow, lastRow]` removidas |
| `fireTableCellUpdated(row, column)` | uma célula mudou |
| `fireTableRowsUpdated(firstRow, lastRow)` | valores de linhas mudaram |
| `fireTableDataChanged()` | todos os dados podem ter mudado (estrutura igual) |
| `fireTableStructureChanged()` | colunas mudaram (recria os column headers) |

A precisão importa: `fireTableRowsInserted(2, 2)` informa à view *exatamente* qual linha apareceu, permitindo repaint incremental. `fireTableDataChanged()` é o martelo grande — repinta tudo e **perde a seleção/posição**. Use o evento mais específico que descreve a mudança.

```java
// dentro do model: ao editar uma célula, notifique
@Override
public void setValueAt(Object value, int row, int col) {
    data.get(row).update(col, value);
    fireTableCellUpdated(row, col);   // a view repinta só essa célula
}
```

Para **ouvir** mudanças do model (ex.: recalcular um total ao editar), registre um `TableModelListener`:

```java
table.getModel().addTableModelListener(e -> {
    int row = e.getFirstRow();
    int col = e.getColumn();
    // reagir à mudança (e.getType() é INSERT, UPDATE ou DELETE)
});
```

### Selection models (`ListSelectionModel`)

A **seleção** é um model à parte, compartilhado por `JList` e `JTable`: o `ListSelectionModel`. *"A list uses an instance of `ListSelectionModel` to manage its selection."* Os três modos:

| Modo | Comportamento |
|------|---------------|
| `SINGLE_SELECTION` | um item por vez; selecionar um deseleciona o anterior |
| `SINGLE_INTERVAL_SELECTION` | um intervalo contíguo |
| `MULTIPLE_INTERVAL_SELECTION` | **default** — qualquer combinação de itens |

```java
list.setSelectionMode(ListSelectionModel.SINGLE_SELECTION);
```

Mudanças de seleção disparam `ListSelectionEvent`, ouvido por um `ListSelectionListener`. O detalhe que pega quem não conhece: *"Many list selection events can be generated from a single user action such as a mouse click. The `getValueIsAdjusting` method returns `true` if the user is still manipulating the selection."* Processe apenas o evento final:

```java
list.addListSelectionListener(e -> {
    if (!e.getValueIsAdjusting()) {           // ignora eventos intermediários
        int idx = list.getSelectedIndex();
        // reagir à seleção definitiva
    }
});
```

## Na prática

Em uso real, modele o domínio: um `AbstractTableModel` tipado sobre uma `List<Order>` é muito melhor que um `DefaultTableModel` de `Object[][]`. Ele dá **type-safety** (cada coluna conhece seu tipo), expõe os objetos de domínio diretamente (sem copiar para um array) e deixa explícito o que cada coluna significa.

```java
import javax.swing.table.AbstractTableModel;
import java.util.ArrayList;
import java.util.List;

public class OrderTableModel extends AbstractTableModel {

    private static final String[] COLUMNS = { "ID", "Customer", "Total", "Paid" };

    private final List<Order> orders = new ArrayList<>();

    public OrderTableModel(List<Order> initial) {
        orders.addAll(initial);
    }

    @Override
    public int getRowCount() {
        return orders.size();
    }

    @Override
    public int getColumnCount() {
        return COLUMNS.length;
    }

    @Override
    public String getColumnName(int column) {
        return COLUMNS[column];
    }

    @Override
    public Class<?> getColumnClass(int column) {
        // dirige renderer/editor default: Boolean -> checkbox, etc.
        return switch (column) {
            case 0 -> Integer.class;
            case 2 -> java.math.BigDecimal.class;
            case 3 -> Boolean.class;
            default -> String.class;
        };
    }

    @Override
    public Object getValueAt(int row, int column) {
        Order o = orders.get(row);
        return switch (column) {
            case 0 -> o.id();
            case 1 -> o.customer();
            case 2 -> o.total();        // BigDecimal cru — formatação fica no renderer
            case 3 -> o.paid();
            default -> null;
        };
    }

    // Mutação que MANTÉM a view em sincronia: muda os dados e dispara o evento certo.
    public void addOrder(Order order) {
        int newRow = orders.size();
        orders.add(order);
        fireTableRowsInserted(newRow, newRow);   // view repinta só a linha nova
    }
}
```

```text
// Uso:
//   OrderTableModel model = new OrderTableModel(carregarPedidos());
//   JTable table = new JTable(model);
//   panel.add(new JScrollPane(table));   // cabeçalhos só aparecem dentro do JScrollPane
//
//   model.addOrder(novoPedido);   // a tabela ganha a linha automaticamente
```

Por que isso supera o `DefaultTableModel` com `Object[][]`:

- **Type-safety e clareza** — `getColumnClass` devolve tipos reais; `getValueAt` lê de um `Order`, não de uma célula `Object` sem nome.
- **Fonte única de verdade** — os dados continuam na `List<Order>` do domínio; a tabela é só uma view sobre ela.
- **Eventos corretos de graça** — `fireTableRowsInserted` vem de `AbstractTableModel`; você só dispara no ponto certo.

## Armadilhas

### (1) Mutar a `List` interna sem disparar `fireTable...` — a view fica dessincronizada

**Descrição.** Como o componente *não cacheia dados*, ele só sabe que algo mudou quando o model **dispara o evento**. Se você muta a `List` interna e esquece o `fire*`, a tela continua mostrando o estado antigo até um repaint acidental (redimensionar a janela, trocar de aba). O bug parece intermitente: "às vezes a linha nova aparece".

```java
// RUIM — adiciona o dado mas não notifica a view
public void addOrder(Order order) {
    orders.add(order);   // a JTable não repinta: nenhum evento foi disparado
}
```

**Fix (1 linha):** dispare o evento que descreve a mudança — `fireTableRowsInserted(newRow, newRow);` após o `add` (ou `fireTableRowsDeleted` após remover).

---

### (2) Usar `DefaultTableModel` com `Object[][]`/`Vector` cru onde um `AbstractTableModel` tipado serviria melhor

**Descrição.** `new DefaultTableModel(Object[][] data, Object[] cols)` é tentador, mas tudo vira `Object`: sem `getColumnClass` decente, números viram texto alinhado à esquerda, booleanos não viram checkbox, e a lógica de domínio fica espalhada em índices mágicos de array. Numa entrevista, sinaliza desconhecimento da separable model.

```java
// RUIM — dados crus, sem tipos, sem domínio
Object[][] rows = { { 1, "Acme", "199.90", false } };
JTable table = new JTable(new DefaultTableModel(rows, COLUMNS));
// coluna "Total" é String; coluna "Paid" não vira checkbox
```

**Fix (1 linha):** modele o domínio com um `AbstractTableModel` tipado sobre `List<Order>` (como em *Na prática*), com `getColumnClass` retornando os tipos reais.

---

### (3) Colocar formatação/lógica de negócio no model (`getValueAt`) em vez de no renderer

**Descrição.** É tentador formatar moeda, data ou status dentro de `getValueAt` (devolver `"R$ 199,90"` em vez de `BigDecimal`). Isso quebra a separação: o model passa a guardar `String` de apresentação, perde-se a ordenação numérica correta, e o `getColumnClass` deixa de fazer sentido. Apresentação é trabalho da **view**, não do model.

```java
// RUIM — formatação dentro do model
@Override
public Object getValueAt(int row, int col) {
    if (col == 2) {
        return "R$ " + orders.get(row).total();  // String formatada no model
    }
    // ...
}
```

**Fix (1 linha):** devolva o valor cru (`BigDecimal total`) e formate na view com um `TableCellRenderer` — ver [[03-Dominios/Tecnologia/Java/Swing/08 - Renderers e editors|Renderers e editors]].

## Em entrevista

### Frase pronta (inglês)

> "People often say Swing follows MVC, but it's more precise to call it a *separable model architecture*. Classic MVC has three separate objects — model, view, and controller — whereas Swing merges the view and the controller into a single UI delegate provided by the look-and-feel, and keeps only the *model* as the separable, pluggable piece. That's a deliberate trade-off: separating painting from input handling wasn't worth the coupling, but separating the data model is hugely valuable, because it lets you back a `JTable` or `JList` with your own data — an array, a list of domain objects, or even a database query — without touching how it's painted. The crucial consequence is that the component, in Oracle's words, *does not contain or cache data; it is simply a view of your data*, so the view only repaints when the model fires the right event — `fireTableRowsInserted`, `fireTableDataChanged`, and so on. In real code I extend `AbstractTableModel` over a typed `List<Order>` rather than using a raw `DefaultTableModel` of `Object[][]`, because that gives me type-safety through `getColumnClass` and keeps formatting in the renderer instead of the model."

### Vocabulário

| Termo PT | Termo EN |
|----------|----------|
| arquitetura de model separável | separable model architecture |
| model separado / plugável | separable / pluggable model |
| view e controller fundidos | merged view and controller |
| delegate de interface | UI delegate |
| disparar um evento do model | fire a model event |
| ouvinte do model | model listener (`TableModelListener`) |
| model de seleção | selection model (`ListSelectionModel`) |
| repintar incrementalmente | repaint incrementally |
| segurança de tipo | type-safety |
| fonte única de verdade | single source of truth |

## Veja também

- [[03-Dominios/Tecnologia/Java/Swing/02 - Componentes e containers|Componentes e containers]]
- [[03-Dominios/Tecnologia/Java/Swing/08 - Renderers e editors|Renderers e editors]]
- [[03-Dominios/Tecnologia/Java/Swing/05 - A Event Dispatch Thread|A Event Dispatch Thread (EDT)]]
- [[03-Dominios/Tecnologia/Java/Swing/index|Swing (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#separable model (MVC do Swing)|separable model]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#TableModel / ListModel|TableModel / ListModel]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#Document (modelo de texto)|Document]]

## Referências

- [How to Use Tables — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/uiswing/components/table.html)
- [How to Use Lists — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/uiswing/components/list.html)
- [TableModel — Javadoc Java 21 (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.desktop/javax/swing/table/TableModel.html)
- [AbstractTableModel — Javadoc Java 21 (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.desktop/javax/swing/table/AbstractTableModel.html)
