---
title: "TableView, cell factories e dados observáveis"
created: 2026-06-06
updated: 2026-06-06
type: concept
progress: backlog
status: seedling
publish: true
fase: Adepto
tags:
  - java
  - javafx
  - adepto
  - tableview
aliases:
  - "TableView"
  - "Cell factory"
  - "FilteredList SortedList"
---

# TableView, cell factories e dados observáveis

> [!abstract] TL;DR
> `TableView<S>` exibe uma `ObservableList<S>` em formato de grade. O par de fábricas define tudo: **`cellValueFactory`** diz *o quê* mostrar (extrai um `ObservableValue<T>` do modelo), **`cellFactory`** diz *como* (cria e atualiza a célula visual). Células são **reusadas** durante o scroll — todo `updateItem` deve chamar `super.updateItem`, tratar o caso `empty/null` e nunca criar `Node`s dentro do método. O pipeline **`FilteredList` → `SortedList`** dá filtro e ordenação reativos sem tocar nos dados originais; o único fio condutor é `sortedList.comparatorProperty().bind(table.comparatorProperty())`.

## O que é

`TableView<S>` é o workhorse de dados tabulares do JavaFX. A assinatura da classe é `public class TableView<S> extends Control`, onde `S` é o tipo dos objetos da lista — o Javadoc chama isso de *"the type of the objects contained within the TableView items list"*.

Três tipos cooperam sempre:

- **`TableView<S>`** — o container que gerencia layout, seleção, ordenação e edição.
- **`TableColumn<S, T>`** — uma coluna que sabe extrair um valor `T` de cada linha `S`. Você adiciona colunas via `table.getColumns().setAll(col1, col2, ...)`.
- **`ObservableList<S>`** — a lista viva que alimenta a tabela; qualquer adição, remoção ou troca de elemento propaga-se automaticamente para a UI sem `repaint` manual.

O contrato básico:

```java
ObservableList<Order> data = FXCollections.observableArrayList();
TableView<Order> table = new TableView<>(data);
```

## Por que importa

Toda aplicação de negócio tem pelo menos uma grade. A arquitetura de duas fábricas do `TableView` separa *quem entende dos dados* (o modelo, via `cellValueFactory`) de *quem sabe renderizá-los* (a célula, via `cellFactory`). Quem entende a separação escreve tabelas que podem ser testadas, trocadas e estendidas sem reescrever a lógica de domínio.

O paralelo com o Swing é direto: `TableCellRenderer` e `TableCellEditor` fazem papel semelhante no Swing — mas usam o mecanismo de *stamp* (renderizador retorna um componente genérico que é pintado sobre a célula). JavaFX vai além: a `TableCell` é um `Node` real da cena, com CSS, binding e ciclo de vida próprios. Mais detalhes sobre renderers e editors do Swing em [[03-Dominios/Tecnologia/Java/Swing/08 - Renderers e editors|Renderers e editors (Swing)]].

## Como funciona

### ObservableList e FXCollections (a lista que avisa)

`FXCollections.observableArrayList(...)` cria uma `ObservableList<S>` — uma lista que notifica seus observadores a cada mutação estrutural (add, remove, set). A tabela se registra como observadora: ao adicionar um elemento à lista, a linha aparece na UI sem nenhum código extra.

**`setAll` vs trocar a lista:** mutar a lista existente com `setAll(novaLista)` preserva o pipeline — os wrappers `FilteredList` e `SortedList` que encapsulam essa lista continuam funcionando. Chamar `table.setItems(outraListaAbsoluta)` substitui a referência subjacente, quebrando qualquer pipeline de transformação que foi construído em cima da lista original (veja Armadilha 3).

### cellValueFactory — os DADOS

`cellValueFactory` é um `Callback<CellDataFeatures<S,T>, ObservableValue<T>>` que recebe metadados da célula e retorna um `ObservableValue<T>` para exibir.

A forma moderna e type-safe usa uma **lambda com properties do modelo** (conforme [[07 - Properties e binding]]):

```java
TableColumn<Order, String> customerCol = new TableColumn<>("Cliente");
customerCol.setCellValueFactory(
    cellData -> cellData.getValue().customerProperty()
);

TableColumn<Order, Integer> quantityCol = new TableColumn<>("Qtd");
quantityCol.setCellValueFactory(
    cellData -> cellData.getValue().quantityProperty().asObject()
);
```

O `asObject()` converte `IntegerProperty` em `ObjectProperty<Integer>`, necessário porque `TableColumn<S, T>` espera um `ObservableValue<T>` (referência), não um primitivo.

**`PropertyValueFactory` — o atalho legado:** é uma implementação pronta que usa *reflection* para localizar a property pelo nome:

```java
customerCol.setCellValueFactory(new PropertyValueFactory<>("customer"));
// equivale a: cellData -> cellData.getValue().customerProperty()
// encontrado por reflection procurando o método customerProperty()
```

Os riscos do atalho: o nome é uma `String` sem verificação em tempo de compilação; se você renomear o método do modelo, a coluna fica vazia silenciosamente em runtime. Para código novo, prefira a lambda — é type-safe e inspecionável pelo compilador.

### cellFactory — o RENDER

`cellFactory` é um `Callback<TableColumn<S,T>, TableCell<S,T>>` que *cria* (e depois *atualiza*) a célula visual. O Javadoc é explícito: *"Avoid creating new Nodes in the updateItem method"* — crie os `Node`s uma única vez, no construtor ou bloco inicializador, e apenas os configure em `updateItem`.

As três regras de `updateItem`:

1. **Sempre chamar `super.updateItem(item, empty)`** — o Javadoc diz: *"it is important that you also ensure that you call the super method"*. A super-chamada atualiza estado interno da célula (selected, focused, etc.).
2. **Tratar o caso `empty` ou `null`** — células no final da tabela (linhas vazias de preenchimento) chegam com `empty == true`; o item pode ser `null`. Ignorar isso produz "células fantasma" com conteúdo de uma linha anterior (veja Armadilha 1).
3. **Não criar `Node`s dentro do método** — a célula é reusada ao rolar: `updateItem` é chamado repetidamente. Criar um `new Rectangle()` a cada chamada desperdiça memória e CPU.

Exemplo de coluna de status com cor:

```java
TableColumn<Order, String> statusCol = new TableColumn<>("Status");
statusCol.setCellValueFactory(cellData -> cellData.getValue().statusProperty());
statusCol.setCellFactory(col -> new TableCell<>() {
    private final Label badge = new Label();  // criado uma vez

    @Override
    protected void updateItem(String status, boolean empty) {
        super.updateItem(status, empty);       // regra 1
        if (empty || status == null) {         // regra 2
            setText(null);
            setGraphic(null);
            return;
        }
        badge.setText(status);
        badge.setStyle(switch (status) {
            case "APROVADO"  -> "-fx-background-color: #c8f7c5; -fx-text-fill: #1e7e34;";
            case "PENDENTE"  -> "-fx-background-color: #fef3cd; -fx-text-fill: #856404;";
            case "REJEITADO" -> "-fx-background-color: #fde8e8; -fx-text-fill: #9b1c1c;";
            default          -> "-fx-background-color: transparent;";
        });
        setGraphic(badge);                     // regra 3 — reutiliza o Node
    }
});
```

### Seleção (selectionModel)

O Javadoc declara: *"the default SelectionModel used when instantiating a TableView is an implementation of the MultipleSelectionModel, however the default value is SelectionMode.SINGLE"*. Na prática, só uma linha é selecionável até você mudar:

```java
// múltipla seleção (Ctrl+Click, Shift+Click)
table.getSelectionModel().setSelectionMode(SelectionMode.MULTIPLE);

// binding reativo ao item selecionado
ObjectProperty<Order> selected = new SimpleObjectProperty<>();
selected.bind(table.getSelectionModel().selectedItemProperty());
```

`selectedItemProperty()` é um `ReadOnlyObjectProperty<S>` — você pode ligar um detalhe de formulário ou botão de ação diretamente a ele com `bind` ou um `ChangeListener`.

### Edição (setEditable, TextFieldTableCell, onEditCommit)

Para edição inline, três condições devem ser verdadeiras ao mesmo tempo: a tabela, a coluna e a célula precisam ser editáveis.

```java
table.setEditable(true);
customerCol.setEditable(true);
customerCol.setCellFactory(TextFieldTableCell.forTableColumn());
```

O Javadoc alerta: *"unless you then handle the writeback to the property (or the relevant data source), nothing will happen"* — o commit não escreve no modelo automaticamente quando você usa `PropertyValueFactory`. Com lambda e properties, o `onEditCommit` padrão já faz o writeback:

```java
customerCol.setOnEditCommit(event ->
    event.getRowValue().setCustomer(event.getNewValue())
);
```

### Sorting e filtering — o pipeline reativo

O pipeline canônico para filtro + ordenação reativos:

```
ObservableList<S>   (dados reais, nunca altere a referência)
    ↓
FilteredList<S>     (oculta itens; mudanças na fonte propagam imediatamente)
    ↓
SortedList<S>       (reordena; segue o comparador da tabela)
    ↓
TableView<S>        (exibe o resultado final)
```

```java
ObservableList<Order> source   = FXCollections.observableArrayList();
FilteredList<Order>  filtered  = new FilteredList<>(source, p -> true);
SortedList<Order>    sorted    = new SortedList<>(filtered);

// Liga o comparador da tabela ao da SortedList (fundamental — veja Armadilha 2)
sorted.comparatorProperty().bind(table.comparatorProperty());
table.setItems(sorted);
```

**Filtro reativo com TextField** (versão declarativa com `Bindings.createObjectBinding`):

```java
filtered.predicateProperty().bind(Bindings.createObjectBinding(
    () -> {
        String lower = searchField.getText() == null
            ? "" : searchField.getText().toLowerCase();
        return lower.isEmpty() ? (Order o) -> true
            : (Order o) -> o.getCustomer().toLowerCase().contains(lower)
                       || o.getStatus().toLowerCase().contains(lower);
    },
    searchField.textProperty()
));
```

### Contraste com Swing

O `TableCellRenderer` do Swing usa *stamp*: o renderer retorna um componente pintado sobre a célula, que não é um `Node` real da hierarquia. A `TableCell` do JavaFX é um `Node` real — participa de CSS, layout e eventos individualmente. Mais detalhes em [[03-Dominios/Tecnologia/Java/Swing/08 - Renderers e editors|Renderers e editors (Swing)]].

## Na prática

O modelo `Order` segue o padrão canônico de [[07 - Properties e binding]] — campos `private final StringProperty/IntegerProperty/DoubleProperty` com trio `getId()`/`setId()`/`idProperty()` para cada atributo. A montagem da tabela com pipeline completo:
```java
package com.example;

import javafx.application.Application;
import javafx.beans.binding.Bindings;
import javafx.collections.*;
import javafx.collections.transformation.*;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.control.cell.TextFieldTableCell;
import javafx.scene.layout.VBox;
import javafx.stage.Stage;

public class OrderTableApp extends Application {

    @Override
    public void start(Stage stage) {
        // 1. Dados reais
        ObservableList<Order> source = FXCollections.observableArrayList(
            buildOrder("ORD-001", "Acme Corp",   10, 1500.00, "APROVADO"),
            buildOrder("ORD-002", "Beta Ltda",    3,  450.00, "PENDENTE"),
            buildOrder("ORD-003", "Gamma SA",    25, 3200.00, "APROVADO"),
            buildOrder("ORD-004", "Delta Eireli",  1,   89.90, "REJEITADO")
        );

        // 2. Pipeline filtro → ordenação
        FilteredList<Order> filtered = new FilteredList<>(source, p -> true);
        SortedList<Order>   sorted   = new SortedList<>(filtered);

        TableView<Order> table = new TableView<>(sorted);
        table.setEditable(true);
        sorted.comparatorProperty().bind(table.comparatorProperty());  // essencial

        // 3. Colunas com cellValueFactory via lambda (type-safe)
        TableColumn<Order, String> idCol = new TableColumn<>("ID");
        idCol.setCellValueFactory(c -> c.getValue().idProperty());

        TableColumn<Order, String> customerCol = new TableColumn<>("Cliente");
        customerCol.setCellValueFactory(c -> c.getValue().customerProperty());
        customerCol.setCellFactory(TextFieldTableCell.forTableColumn());
        customerCol.setOnEditCommit(e -> e.getRowValue().setCustomer(e.getNewValue()));

        TableColumn<Order, Integer> qtyCol = new TableColumn<>("Qtd");
        qtyCol.setCellValueFactory(c -> c.getValue().quantityProperty().asObject());

        TableColumn<Order, Double> totalCol = new TableColumn<>("Total (R$)");
        totalCol.setCellValueFactory(c -> c.getValue().totalProperty().asObject());

        // 4. Coluna de status com cellFactory custom (badge colorido)
        TableColumn<Order, String> statusCol = new TableColumn<>("Status");
        statusCol.setCellValueFactory(c -> c.getValue().statusProperty());
        statusCol.setCellFactory(col -> new TableCell<>() {
            private final Label badge = new Label();
            @Override
            protected void updateItem(String status, boolean empty) {
                super.updateItem(status, empty);
                if (empty || status == null) { setGraphic(null); return; }
                badge.setText(status);
                badge.setStyle(switch (status) {
                    case "APROVADO"  -> "-fx-background-color: #c8f7c5;";
                    case "PENDENTE"  -> "-fx-background-color: #fef3cd;";
                    case "REJEITADO" -> "-fx-background-color: #fde8e8;";
                    default          -> "";
                });
                setGraphic(badge);
            }
        });

        table.getColumns().setAll(idCol, customerCol, qtyCol, totalCol, statusCol);

        // 5. Campo de busca com filtro reativo (declarativo via Bindings)
        TextField searchField = new TextField();
        searchField.setPromptText("Buscar por cliente ou status...");
        filtered.predicateProperty().bind(Bindings.createObjectBinding(
            () -> {
                String lower = searchField.getText() == null
                    ? "" : searchField.getText().toLowerCase();
                return lower.isEmpty() ? (Order o) -> true
                    : (Order o) -> o.getCustomer().toLowerCase().contains(lower)
                               || o.getStatus().toLowerCase().contains(lower);
            },
            searchField.textProperty()
        ));

        VBox root = new VBox(8, searchField, table);
        stage.setScene(new Scene(root, 700, 400));
        stage.setTitle("Pedidos");
        stage.show();
    }

    private Order buildOrder(String id, String customer, int qty, double total, String status) {
        Order o = new Order();
        o.setId(id); o.setCustomer(customer);
        o.setQuantity(qty); o.setTotal(total); o.setStatus(status);
        return o;
    }

    public static void main(String[] args) { launch(args); }
}
```

## Armadilhas

### (1) `updateItem` sem tratar `empty` — células fantasma

**Problema:** o `TableView` cria mais células do que há dados para preencher o espaço visual. Células excedentes chegam com `empty == true` e `item == null`. Se `updateItem` não verificar, a célula exibe o conteúdo da última linha que ocupou aquele slot de reuso — conteúdo "fantasma" que aparece e some conforme o usuário rola.

```java
// ERRADO — não trata empty
@Override
protected void updateItem(String value, boolean empty) {
    super.updateItem(value, empty);
    setText(value.toUpperCase());  // NullPointerException ou conteúdo fantasma
}
```

**Fix:** sempre verificar antes de usar o item:

```java
@Override
protected void updateItem(String value, boolean empty) {
    super.updateItem(value, empty);
    if (empty || value == null) {
        setText(null);
        setGraphic(null);
        return;
    }
    setText(value.toUpperCase());
}
```

---

### (2) `SortedList` sem `comparatorProperty().bind(...)` — header clicável que não faz nada

**Problema:** clicar no cabeçalho de uma coluna altera o `comparatorProperty()` da tabela, mas a `SortedList` não sabe disso — ela tem seu próprio comparador, que está nulo. O resultado é que as setas de ordenação aparecem no header, mas a ordem das linhas não muda.

```java
SortedList<Order> sorted = new SortedList<>(filtered);
table.setItems(sorted);
// esqueceu o bind — header clicável, mas inerte
```

**Fix:** ligar os dois comparadores imediatamente após criar a `SortedList`:

```java
sorted.comparatorProperty().bind(table.comparatorProperty());
```

---

### (3) Trocar a lista inteira com `setItems` quebra o pipeline

**Problema:** ao buscar dados novos do servidor, é tentador fazer `table.setItems(FXCollections.observableArrayList(novosResultados))`. Isso substitui os itens da tabela por uma lista completamente nova — mas os wrappers `FilteredList` e `SortedList` continuam apontando para a lista *antiga*. O pipeline se torna um zumbi: filtros e ordenação param de funcionar, e mudanças nos dados novos não propagam.

```java
// ERRADO
table.setItems(FXCollections.observableArrayList(novosResultados));
// FilteredList e SortedList agora ignoram a nova lista
```

**Fix:** manter a referência da lista base e mutar seu conteúdo com `setAll`:

```java
source.setAll(novosResultados);  // propaga pelo pipeline intacto
```

---

### (4) Lógica pesada em `updateItem` — travamento no scroll

**Problema:** `updateItem` é chamado a cada célula visível reexibida — potencialmente dezenas de vezes por segundo durante o scroll. Consultas ao banco de dados, formatações caras ou cálculos de layout dentro do método tornam o scroll visivelmente lento.

```java
// ERRADO — operação cara a cada scroll
@Override
protected void updateItem(Order order, boolean empty) {
    super.updateItem(order, empty);
    if (empty || order == null) { setText(null); return; }
    // NUNCA faça I/O ou cálculos pesados aqui
    String badge = service.calcularCategoria(order);  // chamada de rede/DB
    setText(badge);
}
```

**Fix:** pré-computar no modelo (como property derivada com `Bindings`) e usar o resultado diretamente em `updateItem`:

```java
// No modelo Order — property derivada, computada uma vez e cacheada
public StringBinding categoriaBinding() {
    return Bindings.createStringBinding(
        () -> total.get() > 5000 ? "ENTERPRISE" : "SMB",
        total
    );
}
```

---

### (5) `PropertyValueFactory` com nome errado — coluna vazia silenciosa

**Problema:** `PropertyValueFactory("customerr")` com um typo não lança exceção — apenas retorna uma coluna em branco. O erro de compilação que salvaria o debug não existe porque o nome é uma `String`. Encontrar a causa exige inspecionar o nome manualmente.

```java
// ERRADO — typo silencioso; coluna em branco, sem aviso
customerCol.setCellValueFactory(new PropertyValueFactory<>("customerr"));
```

**Fix:** usar lambda — o compilador verifica o nome do método:

```java
// CORRETO — erro de compilação se customerProperty() não existir
customerCol.setCellValueFactory(c -> c.getValue().customerProperty());
```

## Em entrevista

### Frase pronta (inglês)

> "In JavaFX, `TableView<S>` is backed by an `ObservableList<S>`, so any structural change to the list — add, remove, set — immediately reflects in the UI without any manual repaint. Each `TableColumn` has two factories: `cellValueFactory` extracts an `ObservableValue<T>` from the row object — I always use a lambda pointing to a JavaFX property rather than `PropertyValueFactory`, because that reflection-based shortcut silently produces an empty column if the property name doesn't match. `cellFactory` controls rendering: you get a `TableCell` that is *reused* as the user scrolls, so `updateItem` must call `super`, guard against the `empty` flag, and never instantiate new `Node`s inside the method — only update pre-built ones."

> "For filtering and sorting without mutating the source, I chain `ObservableList → FilteredList → SortedList` and pass the `SortedList` to the table. The critical step is binding `sortedList.comparatorProperty()` to `table.comparatorProperty()` — otherwise clicking a column header shows the sort arrows but doesn't reorder the rows. To update data, I call `source.setAll(newData)` rather than `setItems`, which would bypass the pipeline entirely."

> "The contrast with Swing's renderer/editor pattern is meaningful: Swing uses a stamp model where the renderer is painted onto the cell but isn't a real component in the hierarchy. JavaFX `TableCell` is a real scene `Node`, so it participates in CSS, layout, and event handling independently — which is both more powerful and more demanding, since you must be disciplined about `updateItem` performance."

### Vocabulário

| Termo PT | Termo EN |
|---|---|
| fábrica de valor de célula | cell value factory |
| fábrica de célula | cell factory |
| lista observável | observable list |
| lista filtrada | filtered list |
| lista ordenada | sorted list |
| modelo de seleção | selection model |
| confirmação de edição | edit commit |
| célula reusada | reused cell / cell recycling |
| item vazio | empty item |
| encadeamento de transformação | transformation pipeline |

## Veja também

- [[04 - Controls essenciais]]
- [[07 - Properties e binding]]
- [[09 - CSS em JavaFX]]
- [[10 - A JavaFX Application Thread — Task, Service e Platform.runLater]]
- [[03-Dominios/Tecnologia/Java/Swing/08 - Renderers e editors|Renderers e editors (Swing)]]
- [[03-Dominios/Tecnologia/Java/JavaFX/index|JavaFX (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#cell factory / cell value factory|cell factory (Dicionário)]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#ObservableList|ObservableList (Dicionário)]]

## Referências

- [TableView — OpenJFX 21 Javadoc](https://openjfx.io/javadoc/21/javafx.controls/javafx/scene/control/TableView.html) — assinatura `TableView<S> extends Control`, cellValueFactory/cellFactory, regras de `updateItem`, selectionModel, edição com `TextFieldTableCell`, binding de `SortedList`
- [FilteredList — OpenJFX 21 Javadoc](https://openjfx.io/javadoc/21/javafx.base/javafx/collections/transformation/FilteredList.html) — *"Wraps an ObservableList and filters its content using the provided Predicate. All changes in the ObservableList are propagated immediately"*; predicado nulo = sempre verdadeiro
- [SortedList — OpenJFX 21 Javadoc](https://openjfx.io/javadoc/21/javafx.base/javafx/collections/transformation/SortedList.html) — *"Wraps an ObservableList and sorts its content"*; `comparatorProperty()` como `ObjectProperty<Comparator<? super E>>`
