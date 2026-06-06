---
title: "Controls essenciais"
created: 2026-06-06
updated: 2026-06-06
type: concept
progress: backlog
status: seedling
publish: true
fase: iniciado
tags:
  - java
  - javafx
  - iniciado
  - controls
aliases:
  - "Controls JavaFX"
  - "TextField Button"
  - "ComboBox"
---

# Controls essenciais

> [!abstract] TL;DR
> `javafx.scene.control` reúne os **widgets prontos** construídos sobre o scene graph: botões, campos de texto, listas, diálogos. Quase toda propriedade neles — texto, valor selecionado, estado de desabilitado — é uma **Property bindável** (gancho da nota [[07 - Properties e binding]]). Listas e tabelas montam sobre `ObservableList`: quando a lista muda, a UI atualiza sozinha, sem chamada manual de refresh.

## O que é

`javafx.scene.control` é a biblioteca de widgets de alto nível do JavaFX. A hierarquia começa em `Node`, passa por `Region` (que lida com CSS de fundo/borda e cálculo de layout) e chega em `Control`:

```text
Node
 └── Parent
      └── Region
           └── Control          ← propriedades bindáveis, tooltip, skin
                ├── Labeled     ← Label, Button, CheckBox, RadioButton
                ├── TextInputControl  ← TextField, TextArea, PasswordField
                ├── ComboBoxBase      ← ComboBox, ChoiceBox
                ├── ListView<T>
                ├── TableView<S>
                └── Dialog<R>   ← Alert extends Dialog<ButtonType>
```

`Control` separa **estado** (suas Properties) de **renderização** (a `Skin` plugável). A `Skin` é quem desenha o controle; trocá-la significa mudar o visual sem tocar na lógica — base de estilização (CSS, [[09 - CSS em JavaFX]]) e de controls customizados ([[12 - Custom controls, Canvas e charts]]).

## Por que importa

O vocabulário de controls é o pré-requisito para qualquer tela real. Saber quais widgets existem prontos evita reinventar (e manter) código de renderização que o framework já oferece. Em entrevista de senioridade Java, errar a diferença entre `ComboBox` e `ChoiceBox`, ou não saber por que `setVisible(false)` às vezes quebra o layout, sinaliza lacuna de prática com UI.

## Como funciona

### Texto e ação

| Control | Uso típico |
|---|---|
| `Label` | texto estático, não editável |
| `Button` | ação disparada por clique ou tecla |
| `TextField` | entrada de texto de linha única |
| `TextArea` | entrada multilinha |
| `PasswordField` | texto mascarado (herda `TextField`) |

Todos os `TextInputControl` expõem `textProperty()` — uma `StringProperty` bindável. `TextField` e `TextArea` têm `promptText` (texto cinza exibido quando vazio) e `tooltip` (balão ao passar o mouse):

```java
TextField fieldEmail = new TextField();
fieldEmail.setPromptText("email@exemplo.com");
fieldEmail.setTooltip(new Tooltip("Informe o e-mail do cliente"));

Button btnSalvar = new Button("Salvar");
btnSalvar.setOnAction(e -> System.out.println(fieldEmail.getText()));
```

### Escolha

**`CheckBox`** representa seleção independente (booleana). Expõe `selectedProperty()`.

**`RadioButton`** representa seleção exclusiva dentro de um grupo. Sem `ToggleGroup`, todos os `RadioButton` da tela ficam independentes — cada um selecionável ao mesmo tempo (ver Armadilhas). Com `ToggleGroup`, desmarcar o anterior é automático:

```java
ToggleGroup grupo = new ToggleGroup();
RadioButton rbAtivo   = new RadioButton("Ativo");
RadioButton rbInativo = new RadioButton("Inativo");
rbAtivo.setToggleGroup(grupo);
rbInativo.setToggleGroup(grupo);
rbAtivo.setSelected(true);
```

**`ComboBox<T>`** vs **`ChoiceBox<T>`**: ambos mostram uma lista suspensa, mas `ComboBox` é editável (campo de texto embutido), aceita `CellFactory` para renderização customizada e escala melhor para listas longas. `ChoiceBox` é mais simples e leve — adequado para listas curtas e fixas de strings.

### Listas e tabelas — visão geral

`ListView<T>` e `TableView<S>` recebem seus dados via `ObservableList`. A ligação é automática: qualquer modificação na lista (add, remove, set) reflete na UI sem chamada de refresh:

```java
ObservableList<String> itens = FXCollections.observableArrayList("A", "B", "C");
ListView<String> lista = new ListView<>(itens);

itens.add("D");   // aparece na ListView imediatamente
```

Para `TableView`, cada `TableColumn<S, T>` mapeia um campo do objeto via `setCellValueFactory`. A profundidade — cell factories customizadas, `FilteredList`, `SortedList`, edição inline — está em [[08 - TableView, cell factories e dados observáveis]].

### Diálogos

**`Alert`** é a subclasse mais usada de `Dialog<ButtonType>`. O `AlertType` pré-configura título, ícone e botões:

| AlertType | Uso |
|---|---|
| `INFORMATION` | mensagem informativa (botão OK) |
| `WARNING` | aviso (botão OK) |
| `ERROR` | erro crítico (botão OK) |
| `CONFIRMATION` | pergunta (botões OK / Cancel) |
| `NONE` | configuração manual completa |

`showAndWait()` bloqueia a thread JavaFX (na prática, entra em loop de eventos aninhado) e retorna `Optional<ButtonType>`:

```java
Alert confirm = new Alert(Alert.AlertType.CONFIRMATION);
confirm.setHeaderText("Remover cliente?");
confirm.setContentText("Esta ação não pode ser desfeita.");
Optional<ButtonType> resultado = confirm.showAndWait();
// resultado.isPresent() && resultado.get() == ButtonType.OK
```

**`FileChooser`** (em `javafx.stage`, não em `javafx.scene.control`) abre o seletor de arquivos nativo do SO via `showOpenDialog(stage)` ou `showSaveDialog(stage)`.

### Estado — disable vs visible vs managed

Três propriedades controlam a presença de um nó na tela, e a diferença importa:

| Propriedade | Efeito visual | Ocupa espaço? |
|---|---|---|
| `setDisable(true)` | renderiza acinzentado, não recebe eventos | sim |
| `setVisible(false)` | invisível | **sim** (managed = true por padrão) |
| `setManaged(false)` | excluído do cálculo de layout | não |

Para esconder um nó **e** liberar o espaço que ele ocupava, é necessário setar ambos (ver Armadilhas).

## Na prática

### Formulário de cadastro com Alert de confirmação

```java
// --- controles ---
TextField fieldNome  = new TextField();
fieldNome.setPromptText("Nome completo");

TextField fieldEmail = new TextField();
fieldEmail.setPromptText("E-mail");

ComboBox<String> cbCategoria = new ComboBox<>();
cbCategoria.getItems().addAll("Bronze", "Prata", "Ouro");
cbCategoria.setPromptText("Categoria");

CheckBox chkAtivo = new CheckBox("Cliente ativo");
chkAtivo.setSelected(true);

Button btnCadastrar = new Button("Cadastrar");
btnCadastrar.setOnAction(e -> {
    String nome      = fieldNome.getText().trim();
    String email     = fieldEmail.getText().trim();
    String categoria = cbCategoria.getValue();
    boolean ativo    = chkAtivo.isSelected();

    if (nome.isEmpty() || email.isEmpty() || categoria == null) {
        Alert err = new Alert(Alert.AlertType.WARNING);
        err.setHeaderText("Campos obrigatórios");
        err.setContentText("Preencha nome, e-mail e categoria.");
        err.showAndWait();
        return;
    }

    Alert confirm = new Alert(Alert.AlertType.CONFIRMATION);
    confirm.setHeaderText("Confirmar cadastro?");
    confirm.setContentText("Nome: " + nome + "\nCategoria: " + categoria);

    Optional<ButtonType> res = confirm.showAndWait();
    if (res.isPresent() && res.get() == ButtonType.OK) {
        // prossegue com a persistência
        System.out.printf("Cadastrando: %s | %s | %s | ativo=%b%n",
                nome, email, categoria, ativo);
    }
});

// --- layout ---
VBox form = new VBox(8,
        new Label("Nome:"),   fieldNome,
        new Label("E-mail:"), fieldEmail,
        new Label("Categoria:"), cbCategoria,
        chkAtivo,
        btnCadastrar);
form.setPadding(new Insets(16));
```

> O tratamento de `Optional<ButtonType>` retornado por `showAndWait()` usa o mesmo padrão de `Optional` explorado em [[03-Dominios/Java/Collections e Streams/10 - Optional|Optional (Galho 2)]].

## Armadilhas

### (1) `setVisible(false)` sem `setManaged(false)` — espaço fantasma

**Problema:** `setVisible(false)` torna o nó transparente, mas o pane de layout ainda o considera ao calcular posições e tamanhos. O espaço que ele ocuparia permanece reservado, gerando um "buraco" visível no formulário.

```java
// PROBLEMA: botão some, mas o espaço continua lá
btnOpcional.setVisible(false);
```

**Fix:** desativar o gerenciamento também.

```java
btnOpcional.setVisible(false);
btnOpcional.setManaged(false);   // remove do cálculo de layout
```

Para religar, setar ambos como `true` na ordem inversa: `setManaged(true)` antes de `setVisible(true)`.

---

### (2) `RadioButton` sem `ToggleGroup` — seleção múltipla acidental

**Problema:** sem `ToggleGroup`, cada `RadioButton` se comporta como um `CheckBox` independente — todos ficam selecionáveis simultaneamente. A exclusividade não é automática; ela exige agrupamento explícito.

```java
// PROBLEMA: todos podem ser marcados ao mesmo tempo
RadioButton rbA = new RadioButton("Opção A");
RadioButton rbB = new RadioButton("Opção B");
```

**Fix:** criar um `ToggleGroup` e atribuir a todos os `RadioButton` do mesmo grupo.

```java
ToggleGroup grupo = new ToggleGroup();
RadioButton rbA = new RadioButton("Opção A");
RadioButton rbB = new RadioButton("Opção B");
rbA.setToggleGroup(grupo);
rbB.setToggleGroup(grupo);
```

---

### (3) Confiar no texto cru de `TextField` sem validar

**Problema:** `TextField` retorna `String` pura — não há validação automática de tipo ou formato. Tentar parsear diretamente sem tratar exceção quebra em runtime.

```java
// PROBLEMA: lança NumberFormatException se o campo estiver vazio ou com letras
int quantidade = Integer.parseInt(fieldQtd.getText());
```

**Fix:** validar no handler (com try/catch ou `.matches()`) ou, melhor, usar binding com converter para expressar a restrição declarativamente (detalhado em [[07 - Properties e binding]]).

```java
String raw = fieldQtd.getText().trim();
if (!raw.matches("\\d+")) {
    // exibir Alert de WARNING e retornar
    return;
}
int quantidade = Integer.parseInt(raw);
```

## Em entrevista

### Frase pronta (inglês)

> "JavaFX ships a rich set of ready-made controls in `javafx.scene.control`, all built on the scene graph and exposing their state as bindable Properties. The key architectural detail is the separation between Control — which holds state — and Skin, which handles rendering; swapping the skin changes the look without touching logic. For data-heavy UIs, ListView and TableView are backed by ObservableList, so any mutation to the list is reflected in the UI automatically with no manual refresh. One subtle trap is visibility: `setVisible(false)` hides the node but keeps it in the layout pass — you need `setManaged(false)` as well to reclaim the space. Another classic mistake is adding RadioButtons without a ToggleGroup, which makes all of them independently selectable instead of mutually exclusive."

### Vocabulário

| Termo PT | Termo EN |
|---|---|
| controle / widget | control / widget |
| campo de texto | text field |
| lista suspensa | drop-down / combo box |
| seleção exclusiva | mutually exclusive selection |
| grupo de alternância | toggle group |
| diálogo modal | modal dialog |
| tipo de alerta | alert type |
| propriedade bindável | bindable property |
| skin / tema visual | skin / visual theme |
| gerenciamento de layout | layout management (managed property) |

## Veja também

- [[03 - Layout panes]]
- [[05 - Eventos — capturing, bubbling e handlers]]
- [[06 - FXML e Scene Builder]]
- [[07 - Properties e binding]]
- [[08 - TableView, cell factories e dados observáveis]]
- [[03-Dominios/Java/JavaFX/index|JavaFX (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Dicionário de Java#ObservableList|ObservableList (Dicionário)]]

## Referências

- [JavaFX 21 Javadoc — javafx.scene.control package summary](https://openjfx.io/javadoc/21/javafx.controls/javafx/scene/control/package-summary.html) — lista completa dos controls, arquitetura Control/Skin, tooltips, CSS
- [JavaFX 21 Javadoc — ListView](https://openjfx.io/javadoc/21/javafx.controls/javafx/scene/control/ListView.html) — constructor `ListView(ObservableList<T>)`, items property, sincronização automática, cell factories
- [JavaFX 21 Javadoc — Alert](https://openjfx.io/javadoc/21/javafx.controls/javafx/scene/control/Alert.html) — AlertType (CONFIRMATION, ERROR, INFORMATION, WARNING, NONE), `showAndWait()` retornando `Optional<ButtonType>`, relação com `Dialog<ButtonType>`
