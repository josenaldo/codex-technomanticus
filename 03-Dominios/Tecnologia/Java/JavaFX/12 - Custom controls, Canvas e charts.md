---
title: "Custom controls, Canvas e charts"
created: 2026-06-06
updated: 2026-06-06
type: concept
progress: backlog
status: seedling
publish: true
fase: magus
tags:
  - java
  - javafx
  - magus
  - canvas
  - custom-controls
aliases:
  - "Custom controls JavaFX"
  - "Canvas"
  - "Charts JavaFX"
---

# Custom controls, Canvas e charts

> [!abstract] TL;DR
> Três caminhos para UI que não existe pronta no catálogo JavaFX: **COMPOR** (`Region` com filhos + properties próprias — cobre 90% dos casos sem custo de infraestrutura), **ESTENDER** (`Control` + `Skin` — separa estado/propriedades do visual, habilita tematização real via CSS, custo que se paga em controles de biblioteca), **DESENHAR** (`Canvas` + `GraphicsContext` — immediate mode dentro do scene graph retained; você redesenha explicitamente porque o toolkit não redesenha por você). Charts nativos (`LineChart`/`BarChart`/`PieChart`/`AreaChart`/`ScatterChart` sobre `XYChart.Series`) cobrem o básico de visualização de dados sem nenhum desses três caminhos.

## O que é

A grande maioria das telas JavaFX é montada combinando controles existentes (`Button`, `TableView`, `TextField`). Quando o design exige algo que o catálogo não oferece, três estratégias se abrem — e escolher a errada tem custo real:

**COMPOR** — criar uma subclasse de `Region` (ou de um `Pane` concreto como `HBox`/`VBox`) que empacota controles filhos e expõe `Property` próprias. O Scene Graph continua gerenciando layout, hit-testing e CSS de todos os filhos. É o caminho default porque o custo é baixo e os benefícios do scene graph são mantidos integralmente.

**ESTENDER** — criar uma subclasse de `Control` com `Skin` separada. `Control` guarda o estado e as `Property` públicas; `Skin` constrói e gerencia os nós visuais. O framework cria o `Skin` via `createDefaultSkin()` ou via CSS (`-fx-skin`). O custo é maior (duas classes mínimas, contrato rígido), mas a separação permite trocar o visual sem alterar o contrato e é o que controles de biblioteca reutilizável demandam.

**DESENHAR** — usar `Canvas`, um nó do scene graph que expõe uma superfície de desenho via `GraphicsContext`. O modelo é immediate mode: você emite comandos de desenho (`fillRect`, `strokePolyline`, `drawImage`…) e o resultado aparece; não há objetos persistentes por forma desenhada. Quando o `Canvas` é redimensionado, a área nova fica em branco — redesenhar é responsabilidade sua.

## Por que importa

**A escolha do caminho é maturidade.** Desenvolvedores que chegaram do Swing tendem a cair direto no `Canvas` porque em Swing há essencialmente um único caminho: sobrescrever `paintComponent`. Em JavaFX, `paintComponent` não existe — ver [[03-Dominios/Tecnologia/Java/Swing/10 - Custom painting e componentes customizados|Custom painting (Swing)]] para o modelo Swing, que não se replica aqui.

**Canvas para tudo é o erro clássico.** Quando você desenha no `Canvas`, o scene graph não sabe o que está lá dentro: nenhum nó filho, nenhuma caixa de bounding por elemento, nenhuma acessibilidade, nenhum hit-testing automático por objeto desenhado. Clicar em um elemento "desenhado" exige calcular manualmente se a coordenada do clique cai dentro da área esperada. Scroll, foco, tab order, leitor de tela — tudo vira responsabilidade sua. Para um botão customizado isso é regressão pura; para um plot com 50 000 pontos, é a solução correta.

**O custo de Control+Skin se justifica em contextos específicos.** Para um controle interno de uma tela só, COMPOR é suficiente. Control+Skin paga seu custo quando o controle vai ser reutilizado em múltiplos projetos, precisa responder a temas CSS diferentes ou deve compor uma biblioteca com API pública estável.

## Como funciona

### Compor (Region/Pane com filhos)

O caminho mais direto: estenda `Region` (ou `HBox`, `VBox`, `StackPane`…), instancie os filhos no construtor, adicione-os via `getChildren().add(...)`, e exponha `Property` próprias que os filhos consomem via binding. Adicione uma style class própria no construtor (`getStyleClass().add("status-badge")`) para que o CSS externo possa estilizá-lo — ver [[09 - CSS em JavaFX]]. Use `PseudoClass` para estados dinâmicos (`active`, `error`, `disabled-custom`).

As `Property` expostas funcionam exatamente como nas [[07 - Properties e binding|properties nativas do JavaFX]]: binding bidirecional, listeners, `ReadOnlyProperty` para dados derivados. O scene graph cuida de layout, clipping, hit-testing e CSS dos filhos automaticamente.

**Quando usar:** quase sempre. Empacotamento de label + ícone, badge de status, card com múltiplos dados, campos com validação inline.

### Estender (Control + Skin)

`Control` estende `Region` e implementa `Skinnable`. O contrato é:

- **Control** guarda estado e expõe `Property` públicas. Não constrói nós visuais diretamente. Sobrescreve `createDefaultSkin()` retornando uma instância do Skin padrão.
- **Skin** recebe o `Control` no construtor via `getSkinnable()`, constrói a hierarquia de nós e escuta as properties do Control para atualizar o visual. Não armazena estado de negócio — só estado de renderização.

```java
// Contrato mínimo do Control
@Override
protected Skin<?> createDefaultSkin() {
    return new RatingControlSkin(this);
}
```

O Skin pode ser substituído via CSS:

```css
.rating-control {
    -fx-skin: "com.example.RatingControlDarkSkin";
}
```

`Control.getCssMetaData()` agrega as propriedades CSS do Control e do Skin (se o Skin estender `SkinBase`), permitindo propriedades CSS customizadas — ver [[09 - CSS em JavaFX]].

**Invariante crítica:** o Skin não deve acessar internals do Control por cast — só as `Property` públicas. Quebrar isso acopla o Skin à implementação e invalida a substituição via CSS.

**Quando usar:** controles de biblioteca reutilizável; controles que precisam de temas CSS radicalmente diferentes; APIs públicas com contrato de propriedades estável.

### Desenhar (Canvas + GraphicsContext)

`Canvas` é um `Node` do scene graph que encapsula uma superfície de pixels. Você obtém o contexto de desenho via `getGraphicsContext2D()` e emite comandos:

```java
GraphicsContext gc = canvas.getGraphicsContext2D();
gc.setFill(Color.STEELBLUE);
gc.fillRect(10, 10, 100, 50);
gc.setStroke(Color.DARKBLUE);
gc.setLineWidth(2.0);
gc.strokePolyline(xPoints, yPoints, n);
gc.clearRect(0, 0, canvas.getWidth(), canvas.getHeight()); // limpa tudo
```

API completa do `GraphicsContext`: formas (`fillRect`, `strokeOval`, `fillPolygon`, `strokePolyline`), paths (`beginPath`, `moveTo`, `lineTo`, `closePath`, `fill`, `stroke`), texto (`fillText`), imagem (`drawImage`), transformações (`translate`, `scale`, `rotate`), estado (`save`/`restore`).

**Immediate mode dentro do retained:** o scene graph sabe que existe um `Canvas` como nó (posição, tamanho, transformações, opacidade, clipping da cena) — isso é retained. O que está desenhado dentro é immediate: não há objetos por forma, o toolkit não redesenha automaticamente, e redimensionar o nó limpa a área expandida.

**Redesenho explícito obrigatório em resize:**

```java
canvas.widthProperty().addListener((obs, o, n) -> redraw());
canvas.heightProperty().addListener((obs, o, n) -> redraw());
```

**Quando usar:** visualizações com muitos elementos onde criar um Node por ponto tornaria o scene graph custoso (plots densos, espectrogramas, mapas de calor, sparklines com centenas de pontos, jogos 2D).

### Charts nativos

JavaFX inclui um conjunto de charts prontos, todos extensíveis via CSS:

| Classe | Uso típico |
|---|---|
| `LineChart<X,Y>` | Tendência ao longo do tempo |
| `AreaChart<X,Y>` | Tendência com área preenchida sob a linha |
| `BarChart<X,Y>` | Comparação entre categorias |
| `StackedBarChart<X,Y>` | Comparação com composição interna |
| `ScatterChart<X,Y>` | Distribuição / correlação |
| `BubbleChart<X,Y>` | Três dimensões em 2D (x, y, raio) |
| `PieChart` | Proporções de um todo |

Os charts XY operam sobre `XYChart.Series<X,Y>`, que contém `XYChart.Data<X,Y>` — cada `Data` é um ponto. O eixo pode ser `NumberAxis` ou `CategoryAxis`. Estilização via CSS puro — ver [[09 - CSS em JavaFX]].

**Quando usar:** visualizações de dados sem requisito de interatividade avançada ou renderização massiva. Para milhares de pontos com atualização em tempo real, considere `Canvas`.

### O critério de escolha

```
Novo elemento visual necessário
        │
        ▼
Compor Region + filhos resolve? ──── SIM ───► COMPOR (default)
        │
       NÃO
        │
        ▼
Controle reutilizável / temável? ─── SIM ───► Control + Skin
        │
       NÃO
        │
        ▼
Muitos elementos / plot denso? ───── SIM ───► Canvas
        │
       NÃO
        │
        ▼
                                            COMPOR (ainda)
```

## Na prática

### Control composto: StatusBadge

```java
import javafx.beans.property.StringProperty;
import javafx.beans.property.SimpleStringProperty;
import javafx.css.PseudoClass;
import javafx.scene.control.Label;
import javafx.scene.layout.HBox;

public class StatusBadge extends HBox {

    private static final PseudoClass ERROR   = PseudoClass.getPseudoClass("error");
    private static final PseudoClass SUCCESS = PseudoClass.getPseudoClass("success");

    private final Label label = new Label();
    private final StringProperty status = new SimpleStringProperty(this, "status", "");

    public StatusBadge() {
        getStyleClass().add("status-badge");
        getChildren().add(label);
        label.textProperty().bind(status);
        status.addListener((obs, old, val) -> updatePseudoClasses(val));
    }

    private void updatePseudoClasses(String val) {
        pseudoClassStateChanged(ERROR,   "error".equalsIgnoreCase(val));
        pseudoClassStateChanged(SUCCESS, "success".equalsIgnoreCase(val));
    }

    public StringProperty statusProperty() { return status; }
    public String getStatus()              { return status.get(); }
    public void setStatus(String v)        { status.set(v); }
}
```

CSS correspondente:

```css
.status-badge { -fx-padding: 4 8; -fx-background-radius: 4; -fx-background-color: #ccc; }
.status-badge:error   { -fx-background-color: #f44336; -fx-text-fill: white; }
.status-badge:success { -fx-background-color: #4caf50; -fx-text-fill: white; }
```

### Canvas: sparkline com redesenho em resize

```java
import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.paint.Color;
import java.util.List;

public class SparklineCanvas extends Canvas {

    private List<Double> data = List.of();

    public SparklineCanvas(double width, double height) {
        super(width, height);
        widthProperty().addListener((obs, o, n) -> redraw());
        heightProperty().addListener((obs, o, n) -> redraw());
    }

    public void setData(List<Double> values) {
        this.data = List.copyOf(values);
        redraw();
    }

    private void redraw() {
        double w = getWidth(), h = getHeight();
        GraphicsContext gc = getGraphicsContext2D();
        gc.clearRect(0, 0, w, h);
        if (data == null || data.size() < 2) return;

        double min = data.stream().mapToDouble(Double::doubleValue).min().orElse(0);
        double max = data.stream().mapToDouble(Double::doubleValue).max().orElse(1);
        double range = (max - min) == 0 ? 1 : max - min;
        int n = data.size();

        double[] xs = new double[n];
        double[] ys = new double[n];
        for (int i = 0; i < n; i++) {
            xs[i] = i * (w / (n - 1));
            ys[i] = h - ((data.get(i) - min) / range) * h;
        }

        gc.setStroke(Color.STEELBLUE);
        gc.setLineWidth(1.5);
        gc.strokePolyline(xs, ys, n);
    }

    // Necessário para que o Canvas expanda com o pai
    @Override public boolean isResizable() { return true; }
    @Override public double prefWidth(double h)  { return getWidth(); }
    @Override public double prefHeight(double w) { return getHeight(); }
}
```

### LineChart: pedidos por dia

```java
import javafx.scene.chart.*;

NumberAxis xAxis = new NumberAxis(1, 30, 1);
NumberAxis yAxis = new NumberAxis();
xAxis.setLabel("Dia");
yAxis.setLabel("Pedidos");

LineChart<Number, Number> chart = new LineChart<>(xAxis, yAxis);
chart.setTitle("Pedidos por dia");

XYChart.Series<Number, Number> series = new XYChart.Series<>();
series.setName("Junho");
series.getData().add(new XYChart.Data<>(1, 42));
series.getData().add(new XYChart.Data<>(2, 58));
series.getData().add(new XYChart.Data<>(3, 37));
series.getData().add(new XYChart.Data<>(4, 91));

chart.getData().add(series);
```

## Armadilhas

### (1) Canvas para tudo

**Problema:** usar `Canvas` como superfície universal porque "é mais simples desenhar do que compor". O scene graph não enxerga o que está desenhado: hit-testing por elemento desenhado é manual (calcular se a coordenada do clique cai dentro de cada "objeto"), não há acessibilidade (leitor de tela não sabe o que existe), não há CSS por elemento, não há foco/tab order automático por forma.

```java
// Problema: botão "desenhado" — clique, foco e acessibilidade são manuais
canvas.setOnMouseClicked(e -> {
    if (e.getX() > 10 && e.getX() < 110 && e.getY() > 10 && e.getY() < 40) {
        handleClick(); // acerta na mão o que o scene graph faria de graça
    }
});
```

**Fix:** componha com `Region` + filhos para qualquer elemento que precise de interatividade. Reserve `Canvas` para densidades onde um `Node` por elemento é custo real.

---

### (2) Canvas não redesenha sozinho em resize

**Problema:** colocar um `Canvas` num layout e esperar que o conteúdo se ajuste ao redimensionamento. Quando o `Canvas` cresce, a área nova fica transparente (em branco). O conteúdo anterior não é escalado nem repetido.

```java
// Problema: canvas cresce com a janela mas o desenho não
Canvas canvas = new Canvas();
AnchorPane.setTopAnchor(canvas, 0.0);
AnchorPane.setBottomAnchor(canvas, 0.0);
// ... janela redimensiona → área nova em branco
```

**Fix:** adicione listeners nas propriedades de tamanho e redesenhe explicitamente:

```java
canvas.widthProperty().addListener((obs, o, n) -> redraw());
canvas.heightProperty().addListener((obs, o, n) -> redraw());
```

Lembre-se de chamar `gc.clearRect(0, 0, w, h)` antes de redesenhar para não acumular o desenho anterior.

---

### (3) Skin acessando internals do Control por cast

**Problema:** o `Skin` faz cast do `getSkinnable()` para a implementação concreta e acessa campos ou métodos internos (não parte da API pública de `Property`). Isso quebra o contrato do Control+Skin: a pele passa a depender de detalhes de implementação, impossibilitando troca de Skin via CSS.

```java
// Problema: Skin acessa campo interno por cast
public class RatingSkin extends SkinBase<RatingControl> {
    public RatingSkin(RatingControl control) {
        super(control);
        // ERRADO: acessa campo interno diretamente
        int v = ((RatingControl) getSkinnable()).internalRawValue; // campo package-private
    }
}
```

**Fix:** o Control expõe toda informação relevante como `Property` pública. O Skin acessa exclusivamente via `getSkinnable().valueProperty()`, `getSkinnable().maxProperty()`, etc.

---

### (4) Milhares de nodes no scene graph onde Canvas resolvia

**Problema:** criar um `Node` por ponto de dados em um gráfico com dezenas de milhares de pontos. O scene graph precisa calcular layout, transformações e pick (hit-testing) para cada nó — a UI para.

```java
// Problema: 50 000 circles no scene graph
for (DataPoint p : largeDataset) {
    Circle c = new Circle(p.x(), p.y(), 2, Color.STEELBLUE);
    plotPane.getChildren().add(c); // 50 000 nodes → layout/pick custosos
}
```

**Fix:** meça primeiro (`VisualVM`, `FPS counter`). Se o scene graph engasgar, mova a renderização para um `Canvas`: desenhe todos os pontos com `gc.fillOval(...)` em um loop. O scene graph gerencia um único nó; você gerencia o que está dentro.

## Em entrevista

### Frase pronta (inglês)

> "In JavaFX you have three paths for custom UI: composing a Region subclass with children — which preserves the full scene graph contract including CSS and hit-testing and covers most cases — extending Control with a separate Skin, which decouples state from visual rendering and enables CSS-driven theming, and drawing on a Canvas using a GraphicsContext in immediate mode, where you issue draw calls and the toolkit does not redraw for you. The key distinction from Swing is that JavaFX has multiple strategies rather than a single paintComponent override, and choosing the wrong one has real costs: using Canvas for everything means you lose automatic hit-testing, accessibility, and CSS per element, while flooding the scene graph with thousands of nodes when Canvas would suffice causes layout and pick overhead that stalls the UI. The Control-plus-Skin contract is specifically designed so the Skin sees the Control only through its public Property API — never through internals — which is what makes CSS skin substitution work."

### Vocabulário

| Termo PT | Termo EN |
|---|---|
| controle composto | composite control |
| pele (de controle) | skin |
| modo imediato | immediate mode |
| grafo de cena retido | retained scene graph |
| redesenho explícito | explicit redraw |
| hit-testing | hit-testing |
| série de dados | data series |
| classe de pseudo-estado | pseudo-class |

## Veja também

- [[02 - Scene graph — stage, scene e nodes]]
- [[07 - Properties e binding]]
- [[09 - CSS em JavaFX]]
- [[03-Dominios/Tecnologia/Java/Swing/10 - Custom painting e componentes customizados|Custom painting (Swing)]]
- [[03-Dominios/Tecnologia/Java/JavaFX/index|JavaFX (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#Canvas (JavaFX)|Canvas (Dicionário)]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#skin (Control)|skin (Dicionário)]]

## Referências

- [Canvas — OpenJFX 21 Javadoc](https://openjfx.io/javadoc/21/javafx.graphics/javafx/scene/canvas/Canvas.html) — Canvas é um `Node` que aceita comandos de desenho via `GraphicsContext`; immediate mode; dimensões fixas por construção; `getGraphicsContext2D()` retorna o contexto; resize não redesenha.
- [GraphicsContext — OpenJFX 21 Javadoc](https://openjfx.io/javadoc/21/javafx.graphics/javafx/scene/canvas/GraphicsContext.html) — API completa de desenho: formas, paths, texto, imagem, transformações, estado (`save`/`restore`); coordenadas transformadas no momento em que são adicionadas ao path.
- [Control — OpenJFX 21 Javadoc](https://openjfx.io/javadoc/21/javafx.controls/javafx/scene/control/Control.html) — contrato Control+Skin; `createDefaultSkin()`; Skin como caixa preta do ponto de vista do Control; CSS via `-fx-skin`; `getCssMetaData()` agrega Control e Skin.
- [javafx.scene.chart — OpenJFX 21 Javadoc](https://openjfx.io/javadoc/21/javafx.controls/javafx/scene/chart/package-summary.html) — `LineChart`, `AreaChart`, `BarChart`, `StackedBarChart`, `ScatterChart`, `BubbleChart`, `PieChart`; `XYChart.Series` e `XYChart.Data`; `NumberAxis` e `CategoryAxis`.
