---
title: "Layout panes"
created: 2026-06-06
updated: 2026-06-06
type: concept
progress: backlog
status: seedling
publish: true
fase: Iniciado
tags:
  - java
  - javafx
  - iniciado
  - layout
aliases:
  - "Layout panes"
  - "VBox HBox"
  - "GridPane"
---

# Layout panes

> [!abstract] TL;DR
> Em JavaFX, **pane = layout**: cada classe de pane carrega embutida sua própria política de posicionamento dos filhos. Não há manager plugável — escolhe-se o pane correto e ele cuida do resto. Esse é o contraste central com o Swing, onde `Container` e `LayoutManager` são objetos separados (ver [[03-Dominios/Tecnologia/Java/Swing/03 - Layout managers|Layout managers (Swing)]]). Dominar dois pilares — **qual pane usar** e **como expressar growth via constraints estáticos** — resolve 90% dos problemas de layout.

## O que é

A hierarquia de contenção relevante para layout é:

```text
Node  (abstrato — todo elemento visual)
 └── Parent  (abstrato — pode ter filhos)
      └── Region  (tem filhos + calcula layout + CSS de fundo/borda)
           └── Pane  (expõe getChildren() como lista pública)
                ├── HBox
                ├── VBox
                ├── BorderPane
                ├── GridPane
                ├── StackPane
                ├── FlowPane
                ├── TilePane
                └── AnchorPane
```

`Region` é o ponto onde o layout entra em cena: ela conhece seu tamanho, calcula `prefWidth`/`prefHeight` dos filhos e os posiciona. `Pane` simplesmente torna `getChildren()` público para que subclasses e código cliente possam adicionar nós diretamente. Cada subclasse concreta implementa o algoritmo de posicionamento específico à sua política.

`Group` — mencionado na nota anterior [[02 - Scene graph — stage, scene e nodes]] — **não é um pane de layout**: ele não calcula posições, é apenas agrupamento lógico.

## Por que importa

Layout quebrado em resize é o bug visual nº 1 de interfaces JavaFX. Quando um `TextField` não estica ao redimensionar a janela, quando colunas de formulário não alinham, ou quando um painel de sobreposição não centraliza — quase sempre a causa é escolha errada de pane ou ausência de constraint de growth.

Em entrevista de migração Swing → JavaFX, a comparação entre os modelos de layout é pergunta frequente. A resposta esperada articula a diferença estrutural (pane vs. container + manager) e demonstra conhecimento prático de pelo menos GridPane, BorderPane e HBox/VBox.

## Como funciona

### Os lineares — VBox e HBox

`VBox` empilha filhos em coluna; `HBox` enfileira em linha. Ambos compartilham os mesmos parâmetros estruturais:

| Propriedade | O que controla |
|---|---|
| `spacing` | espaço entre filhos consecutivos (px) |
| `padding` | espaço interno ao redor de todos os filhos |
| `alignment` | alinhamento do bloco de filhos dentro do pane |
| `fillWidth` / `fillHeight` | se os filhos devem preencher a largura/altura perpendicular |

```java
VBox coluna = new VBox(8);              // spacing = 8px
coluna.setPadding(new Insets(12));
coluna.setAlignment(Pos.TOP_LEFT);

HBox linha = new HBox(4, btn1, btn2);  // spacing + filhos no construtor
linha.setAlignment(Pos.CENTER_RIGHT);
```

### BorderPane e StackPane

**`BorderPane`** divide o espaço em cinco regiões fixas: `top`, `bottom`, `left`, `right` e `center`. O `center` recebe todo o espaço restante — ideal para estrutura de janela de aplicação (toolbar no topo, tabela/editor no centro, barra de status no rodapé).

```java
BorderPane frame = new BorderPane();
frame.setTop(toolbar);
frame.setCenter(tableView);
frame.setBottom(statusBar);
```

Cada região aceita um único nó (que pode ser, ele mesmo, um pane com múltiplos filhos).

**`StackPane`** empilha todos os filhos de trás para frente, centralizando-os por padrão. Casos de uso: sobrepor um indicador de loading sobre um formulário, badge sobre ícone, watermark sobre conteúdo.

```java
StackPane overlay = new StackPane(conteudo, loadingIndicator);
// loadingIndicator aparece na frente, centralizado
```

### GridPane — células, span e ColumnConstraints

`GridPane` organiza filhos em grade com linhas e colunas independentes. O posicionamento usa o método `add(node, colIndex, rowIndex)` — e as variantes com colspan/rowspan:

```java
GridPane grid = new GridPane();
grid.setHgap(8);    // espaço horizontal entre colunas
grid.setVgap(6);    // espaço vertical entre linhas

grid.add(labelNome,   0, 0);          // col 0, row 0
grid.add(fieldNome,   1, 0);          // col 1, row 0
grid.add(labelEmail,  0, 1);
grid.add(fieldEmail,  1, 1);
// botão ocupa 2 colunas: add(node, col, row, colspan, rowspan)
grid.add(btnSalvar,   0, 2, 2, 1);
```

**`ColumnConstraints`** controla como cada coluna se comporta no resize:

```java
ColumnConstraints col0 = new ColumnConstraints();
col0.setPercentWidth(30);             // label: 30% da largura

ColumnConstraints col1 = new ColumnConstraints();
col1.setPercentWidth(70);             // campo: 70%
col1.setHgrow(Priority.ALWAYS);      // estica com a janela

grid.getColumnConstraints().addAll(col0, col1);
```

`RowConstraints` funciona de forma análoga para controle de altura por linha.

### FlowPane, TilePane e AnchorPane

**`FlowPane`** distribui filhos em fluxo que quebra linha (ou coluna) ao atingir o limite do container — comportamento próximo ao `FlowLayout` do Swing, mas com controle de orientação, `hgap` e `vgap`. Útil para conjuntos de tags, botões de filtro, galerias de thumbnails onde a quantidade de itens varia.

**`TilePane`** também quebra em grade, mas força todas as células ao mesmo tamanho (o maior item define o tile). Indicado para galerias com itens uniformes — ícones de aplicativos, avatares.

**`AnchorPane`** ancora as bordas de cada filho a offsets fixos das bordas do pane:

```java
AnchorPane.setTopAnchor(btn, 8.0);
AnchorPane.setRightAnchor(btn, 8.0);
```

Parece conveniente, mas resulta em **layout absoluto disfarçado** — ver Armadilhas.

### Growth e constraints estáticos

Constraints em JavaFX são métodos estáticos no pane que os honra — não propriedades do nó filho. Isso permite que o mesmo nó se comporte diferente conforme o container onde é inserido.

```java
// Dentro de um HBox: campo de busca estica horizontalmente
TextField busca = new TextField();
HBox.setHgrow(busca, Priority.ALWAYS);
busca.setMaxWidth(Double.MAX_VALUE);   // sem isso, o campo não estica mesmo com ALWAYS

// Margem externa ao redor de um botão
HBox.setMargin(btnBuscar, new Insets(0, 0, 0, 4));

// Dentro de um VBox: área de conteúdo estica verticalmente
VBox.setVgrow(scrollPane, Priority.ALWAYS);
scrollPane.setMaxHeight(Double.MAX_VALUE);
```

`Priority` tem três valores: `ALWAYS` (estica sempre que há espaço sobrando), `SOMETIMES` (estica apenas se não houver nó com `ALWAYS`), `NEVER` (tamanho preferido fixo).

### Pane = layout vs. container + manager

No Swing, layout é bipartido: `Container` guarda os filhos; `LayoutManager` (plugável, trocável em runtime) calcula posições. O mesmo `JPanel` pode usar `FlowLayout`, `BorderLayout` ou `GridBagLayout` conforme o manager atribuído.

Em JavaFX, a política de layout é **parte da classe do pane** — não há manager separado. Trocar a política significa trocar o pane. Isso simplifica o modelo mental e elimina a indireção do manager, mas exige escolher o pane correto desde o início.

Detalhes do modelo Swing estão em [[03-Dominios/Tecnologia/Java/Swing/03 - Layout managers|Layout managers (Swing)]] — esta nota não os re-explica.

## Na prática

### Formulário com GridPane

```java
GridPane form = new GridPane();
form.setHgap(8);
form.setVgap(6);
form.setPadding(new Insets(16));

// Coluna de labels (30%) e coluna de campos (70%)
ColumnConstraints c0 = new ColumnConstraints();
c0.setPercentWidth(30);
ColumnConstraints c1 = new ColumnConstraints();
c1.setPercentWidth(70);
c1.setHgrow(Priority.ALWAYS);
form.getColumnConstraints().addAll(c0, c1);

TextField fieldCustomer = new TextField();
fieldCustomer.setMaxWidth(Double.MAX_VALUE);   // permite esticar

TextField fieldOrder = new TextField();
fieldOrder.setMaxWidth(Double.MAX_VALUE);

form.add(new Label("Customer:"), 0, 0);
form.add(fieldCustomer,          1, 0);
form.add(new Label("Order #:"),  0, 1);
form.add(fieldOrder,             1, 1);

Button btnSave = new Button("Save");
form.add(btnSave, 0, 2, 2, 1);   // span 2 colunas
GridPane.setHalignment(btnSave, HPos.RIGHT);
```

### Janela de aplicação com BorderPane

```java
ToolBar toolbar = new ToolBar(new Button("New"), new Button("Open"));
TableView<Order> table = new TableView<>();
Label status = new Label("Ready");

BorderPane root = new BorderPane();
root.setTop(toolbar);
root.setCenter(table);
root.setBottom(status);
BorderPane.setMargin(status, new Insets(4, 8, 4, 8));
```

### TextField que estica em HBox

```java
TextField search = new TextField();
search.setPromptText("Filter orders…");
search.setMaxWidth(Double.MAX_VALUE);
HBox.setHgrow(search, Priority.ALWAYS);

Button btnGo = new Button("Search");
HBox bar = new HBox(8, search, btnGo);
bar.setPadding(new Insets(8));
bar.setAlignment(Pos.CENTER_LEFT);
```

## Armadilhas

### (1) AnchorPane para tudo — layout absoluto disfarçado

**O problema:** anchorar todos os componentes parece dar controle preciso, mas produz layout absoluto: ao redimensionar a janela ou mudar o tamanho de fonte do sistema, os componentes não se redistribuem — aparecem sobrepostos ou cortados. `AnchorPane` não redistribui o espaço disponível entre os filhos.

```java
// PROBLEMA: botões se sobrepõem se a janela encolher
AnchorPane.setLeftAnchor(btn1, 10.0);
AnchorPane.setLeftAnchor(btn2, 10.0);   // mesmo âncora — btn2 fica sobre btn1
AnchorPane.setTopAnchor(btn1, 10.0);
AnchorPane.setTopAnchor(btn2, 10.0);
```

**Fix:** usar um pane com política de distribuição (`HBox`, `VBox`, `GridPane`) como container dos filhos. Reservar `AnchorPane` para o caso específico e legítimo de "fixar um nó à borda do container" — por exemplo, um botão flutuante sempre no canto inferior direito.

---

### (2) Esquecer `setMaxWidth(Double.MAX_VALUE)` com `setHgrow(Priority.ALWAYS)`

**O problema:** o constraint `HBox.setHgrow(node, Priority.ALWAYS)` instrui o HBox a **oferecer** espaço extra ao nó, mas o nó só o aceita se seu `maxWidth` permitir. O `maxWidth` padrão de `TextField`, `Button` e outros controls é `USE_PREF_SIZE` — o campo continua com seu tamanho preferido mesmo que haja espaço sobrando.

```java
// PROBLEMA: busca não estica — maxWidth está travado em USE_PREF_SIZE
TextField busca = new TextField();
HBox.setHgrow(busca, Priority.ALWAYS);   // sem efeito visível
```

**Fix:** setar `setMaxWidth(Double.MAX_VALUE)` (ou `setMaxHeight` para crescimento vertical) explicitamente após o constraint:

```java
busca.setMaxWidth(Double.MAX_VALUE);
HBox.setHgrow(busca, Priority.ALWAYS);   // agora funciona
```

---

### (3) Aninhamento profundo de panes para simular grade

**O problema:** para criar um formulário de 2 colunas, é tentador aninhar vários `HBox` dentro de um `VBox`. Além do custo extra no layout pass (cada container faz sua própria passagem de medição), o FXML resultante fica ilegível e as colunas não alinham — cada `HBox` calcula a largura da coluna de labels independentemente.

```java
// PROBLEMA: labels da coluna esquerda têm larguras diferentes por linha
VBox form = new VBox(6,
    new HBox(8, new Label("Customer:"), new TextField()),
    new HBox(8, new Label("Order number:"), new TextField())
);
```

**Fix:** usar um único `GridPane`. Ele resolve grades completas sem aninhamento, alinha colunas automaticamente e aceita `ColumnConstraints` por coluna:

```java
// CORRETO: coluna 0 sempre com a mesma largura em todas as linhas
GridPane form = new GridPane();
form.setHgap(8);
form.add(new Label("Customer:"),     0, 0);
form.add(new TextField(),            1, 0);
form.add(new Label("Order number:"), 0, 1);
form.add(new TextField(),            1, 1);
```

## Em entrevista

### Frase pronta (inglês)

> "In JavaFX, the layout policy is baked into the pane class itself — you pick VBox for vertical stacking, GridPane for a form grid, BorderPane for the application frame. There's no pluggable LayoutManager like in Swing: swapping the policy means swapping the pane. The most common layout bug I see is a field that doesn't stretch on resize — it almost always means the developer set HBox.setHgrow with Priority.ALWAYS but forgot to also call setMaxWidth(Double.MAX_VALUE), because the control's default maxWidth is USE_PREF_SIZE and won't accept extra space. For complex forms, GridPane with ColumnConstraints and percentWidth is the right tool — nesting HBoxes inside a VBox produces misaligned columns and extra layout passes."

### Vocabulário

| Termo PT | Termo EN |
|---|---|
| pane de layout | layout pane |
| constraint de crescimento | growth constraint |
| esticar / crescer | grow / stretch |
| prioridade de crescimento | grow priority |
| largura percentual | percent width |
| restrição de coluna | column constraint |
| span de coluna | column span |
| espaçamento interno | padding |
| espaçamento entre filhos | spacing / gap |
| ancorar borda | anchor edge |

## Veja também

- [[02 - Scene graph — stage, scene e nodes]]
- [[04 - Controls essenciais]]
- [[06 - FXML e Scene Builder]]
- [[09 - CSS em JavaFX]]
- [[03-Dominios/Tecnologia/Java/Swing/03 - Layout managers|Layout managers (Swing)]]
- [[03-Dominios/Tecnologia/Java/JavaFX/index|JavaFX (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#layout pane|layout pane (Dicionário)]]

## Referências

- [JavaFX 21 Javadoc — layout package summary](https://openjfx.io/javadoc/21/javafx.graphics/javafx/scene/layout/package-summary.html) — lista completa dos panes, hierarquia Region/Pane, static constraints (setHgrow, setVgrow, setMargin), Priority, ColumnConstraints/RowConstraints
- [JavaFX 21 Javadoc — GridPane](https://openjfx.io/javadoc/21/javafx.graphics/javafx/scene/layout/GridPane.html) — add() com col/row/colspan/rowspan, ColumnConstraints.percentWidth, setHgap/setVgap
- [JavaFX 21 Javadoc — HBox](https://openjfx.io/javadoc/21/javafx.graphics/javafx/scene/layout/HBox.html) — spacing, alignment, fillHeight, setHgrow estático, Priority
- [JavaFX 21 Javadoc — BorderPane](https://openjfx.io/javadoc/21/javafx.graphics/javafx/scene/layout/BorderPane.html) — regiões top/bottom/left/right/center, setMargin estático
