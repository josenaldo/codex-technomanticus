---
title: "CSS em JavaFX"
created: 2026-06-06
updated: 2026-06-06
type: concept
progress: backlog
status: seedling
publish: true
fase: adepto
tags:
  - java
  - javafx
  - adepto
  - css
aliases:
  - "CSS JavaFX"
  - "-fx-"
  - "Modena"
---

# CSS em JavaFX

> [!abstract] TL;DR
> O JavaFX tem seu próprio sistema de estilo baseado em CSS 2.1 — mas é um **dialeto**, não CSS web. A sintaxe de seletores é familiar (`.classe`, `#id`, pseudo-classes, descendente); o vocabulário de propriedades é diferente: tudo começa com `-fx-` (`-fx-background-color`, `-fx-text-fill`, `-fx-padding`). **Layout não é CSS**: margens e posicionamento são responsabilidade dos panes, não de folhas de estilo. O tema padrão se chama **Modena** e funciona como a user-agent stylesheet. A precedência é: `setStyle` inline > stylesheets do Parent > stylesheets da Scene > user-agent/Modena.

## O que é

O JavaFX possui um mecanismo de estilo próprio, especificado no **JavaFX CSS Reference Guide**. Ele se baseia no CSS 2.1 da W3C com algumas adições de funcionalidades do CSS 3 — o que significa que a estrutura é reconhecível para quem conhece CSS web, mas o vocabulário de propriedades é inteiramente diferente.

A distinção central: **propriedades de estilo visual** (cor de fundo, borda, fonte, preenchimento interno) são controladas por CSS; **propriedades de layout** (margem entre filhos, alinhamento, posição absoluta) pertencem à API dos panes (`HBox.setMargin`, `GridPane.setConstraints`, etc.) e **não existem** em CSS JavaFX. Não há `margin`, `flex` ou `display` — essas propriedades são silenciosamente ignoradas se escritas.

Cada nó do scene graph carrega uma lista de **style classes** (equivalente ao `class` do HTML) e opcionalmente um `id`. A engine de CSS do JavaFX processa os seletores das folhas de estilo e aplica os valores calculados ao renderizar o nó.

O tema padrão é o **Modena**, introduzido no JavaFX 8 para substituir o antigo Caspian. Modena funciona como a user-agent stylesheet do navegador: define a aparência base de todos os controls. Qualquer folha de estilo de aplicação sobrescreve Modena.

## Por que importa

CSS no JavaFX resolve o problema que o Look and Feel do Swing nunca resolveu de forma simples: **mudar o visual sem recompilar**. Enquanto no Swing trocar de tema significava implementar uma subclasse de `LookAndFeel` e lidar com defaults globais via `UIManager` — veja [[03-Dominios/Java/Swing/09 - Look and Feel e temas|Look and Feel (Swing)]] para o contraste — no JavaFX basta trocar a URL da stylesheet em runtime e o scene graph inteiro se atualiza automaticamente.

Do ponto de vista de entrevistas sênior, o candidato é avaliado em dois pontos concretos: saber que CSS JavaFX é um **dialeto** (não CSS web) e conhecer a **ordem de precedência** da cascata. Confundir os dois é sinal de que o desenvolvedor copiou CSS web sem ler a documentação — o que é exatamente o tipo de bug silencioso que aparece em produção.

## Como funciona

### Seletores (.style-class, #id, descendente, pseudo-classes)

O Reference Guide documenta os seguintes tipos de seletores:

- **`.style-class`** — nós com aquela string na lista `getStyleClass()`
- **`#id`** — nó cujo `getId()` retorna a string correspondente
- **Descendente** — `HBox .label` (espaço entre seletores): qualquer `.label` que seja descendente de `HBox`
- **Pseudo-classes** — `:hover`, `:focused`, `:disabled`, `:pressed`, `:selected`, `:armed`, `:indeterminate`, `:empty`, `:filled`, `:editable`, `:even`, `:odd`, entre outros

Pseudo-classes refletem **estado do nó**; não é preciso escrever código para `:hover` ou `:focused` — o JavaFX os aplica automaticamente quando o estado muda.

```css
/* Exemplo de seletores */
.primary-button { -fx-background-color: #1976D2; }
.primary-button:hover { -fx-background-color: #1565C0; }
#main-title { -fx-font-size: 24px; }
.table-view .overdue { -fx-text-fill: #D32F2F; }
```

### Propriedades -fx-* (famílias principais)

Todas as propriedades JavaFX CSS carregam o prefixo `-fx-`. As famílias mais usadas, com exemplos reais do Reference Guide:

| Família | Propriedades |
|---|---|
| Background | `-fx-background-color`, `-fx-background-image`, `-fx-background-radius`, `-fx-background-insets` |
| Border | `-fx-border-color`, `-fx-border-width`, `-fx-border-style`, `-fx-border-radius` |
| Fonte/Texto | `-fx-font`, `-fx-font-family`, `-fx-font-size`, `-fx-font-weight`, `-fx-text-fill` |
| Padding/Espaçamento | `-fx-padding`, `-fx-spacing`, `-fx-hgap`, `-fx-vgap` |

> [!warning] Consulte sempre o Reference Guide
> Não existe `-fx-margin`. Não existe `-fx-display`. Se uma propriedade não constar no Reference Guide, ela não existe e será ignorada silenciosamente. O Reference Guide é o único dicionário válido: <https://openjfx.io/javadoc/21/javafx.graphics/javafx/scene/doc-files/cssref.html>

### Onde pendurar estilos

Há três pontos de aplicação, com granularidade diferente:

**Inline via `setStyle`** — aplicado diretamente no nó; maior precedência; dificulta temas:

```java
button.setStyle("-fx-background-color: #1976D2; -fx-text-fill: white;");
```

**Style class via `getStyleClass().add`** — a forma recomendada; o nó passa a ser estilizado por qualquer stylesheet que defina aquela classe:

```java
button.getStyleClass().add("primary-button");
```

**Stylesheet da Scene** — carregada uma vez, vale para todos os nós da cena:

```java
scene.getStylesheets().add(
    getClass().getResource("/app.css").toExternalForm()
);
```

**Stylesheet do Parent** — disponível desde JavaFX 2.1; vale apenas para os descendentes daquele nó:

```java
myPane.getStylesheets().add(
    getClass().getResource("/module-theme.css").toExternalForm()
);
```

### Precedência (cascata)

Do menor para o maior peso na cascata:

```text
user-agent (Modena)
    ↑
Scene stylesheets
    ↑
Parent stylesheets
    ↑
setStyle inline  ← vence sempre
```

A consequência prática: `setStyle` é difícil de sobrescrever por tema e torna o nó resistente a mudanças globais de aparência. Use-o apenas para overrides temporários ou calculados em runtime; prefira style classes para estilo declarativo.

Parent stylesheets permitem criar sub-temas dentro de uma mesma cena — útil para toolbars ou painéis com identidade visual própria.

### Custom pseudo-classes (PseudoClass API)

Desde o JavaFX 8, é possível criar pseudo-classes de domínio com a `PseudoClass` API e aplicá-las em CSS exatamente como `:hover` ou `:disabled`. O fluxo é:

1. Declarar a pseudo-classe como constante estática.
2. Chamar `pseudoClassStateChanged` quando o estado mudar.
3. Usar `:nome-da-pseudo-classe` no CSS normalmente.

```java
import javafx.css.PseudoClass;
import javafx.scene.control.TableRow;

public class ItemRow<T extends Item> extends TableRow<T> {

    private static final PseudoClass OVERDUE =
        PseudoClass.getPseudoClass("overdue");

    public ItemRow() {
        itemProperty().addListener((obs, oldItem, newItem) -> {
            boolean isOverdue = newItem != null && newItem.isOverdue();
            pseudoClassStateChanged(OVERDUE, isOverdue);
        });
    }
}
```

```css
.table-row-cell:overdue {
    -fx-text-fill: #B71C1C;
    -fx-font-weight: bold;
}
```

Pseudo-classes de domínio mantêm lógica de estado em Java e aparência em CSS — separação limpa sem acoplamento.

### Temas (trocar stylesheet em runtime)

Trocar o tema é simplesmente substituir a URL na lista de stylesheets da cena:

```java
private void applyTheme(Scene scene, String themePath) {
    scene.getStylesheets().clear();
    scene.getStylesheets().add(
        getClass().getResource(themePath).toExternalForm()
    );
}

// Alternância claro/escuro
applyTheme(scene, isDark ? "/theme-dark.css" : "/theme-light.css");
```

O scene graph inteiro re-estiliza imediatamente, sem nenhum rebuild. Modena pode ser usada como base importando-a explicitamente ou simplesmente não a removendo da lista.

## Na prática

O cenário a seguir conecta os conceitos: um `app.css` com botão primário e pseudo-classe de domínio para linhas vencidas (retomando o `TableView` da nota 08).

**`/src/main/resources/app.css`:**

```css
/* Botão primário com feedback de hover */
.primary-button {
    -fx-background-color: #1976D2;
    -fx-text-fill: white;
    -fx-font-weight: bold;
    -fx-padding: 8 16 8 16;
    -fx-background-radius: 4;
    -fx-cursor: hand;
}

.primary-button:hover {
    -fx-background-color: #1565C0;
}

.primary-button:pressed {
    -fx-background-color: #0D47A1;
}

/* Linha de tabela com prazo vencido */
.table-row-cell:overdue {
    -fx-text-fill: #B71C1C;
    -fx-font-weight: bold;
}

/* Tema escuro (arquivo separado: theme-dark.css) */
```

**Aplicar no `start()`:**

```java
@Override
public void start(Stage stage) {
    // ... construir scene graph ...

    scene.getStylesheets().add(
        getClass().getResource("/app.css").toExternalForm()
    );

    Button saveBtn = new Button("Salvar");
    saveBtn.getStyleClass().add("primary-button");

    stage.setScene(scene);
    stage.show();
}
```

**Row factory com pseudo-classe `overdue`:**

```java
tableView.setRowFactory(tv -> new TableRow<Task>() {

    private static final PseudoClass OVERDUE =
        PseudoClass.getPseudoClass("overdue");

    {
        itemProperty().addListener((obs, oldTask, newTask) -> {
            boolean late = newTask != null && newTask.isOverdue();
            pseudoClassStateChanged(OVERDUE, late);
        });
    }
});
```

**Alternância de tema claro/escuro:**

```java
CheckBox darkModeToggle = new CheckBox("Modo escuro");
darkModeToggle.selectedProperty().addListener((obs, wasOn, isOn) -> {
    scene.getStylesheets().clear();
    scene.getStylesheets().add(
        getClass().getResource(isOn ? "/theme-dark.css" : "/app.css")
                  .toExternalForm()
    );
});
```

## Armadilhas

### (1) Copiar CSS web — propriedades ignoradas silenciosamente

**Problema:** propriedades web como `background-color`, `margin`, `padding` (sem prefixo `-fx-`), `flex`, `display`, `border` não existem no dialeto JavaFX CSS. O JavaFX simplesmente as ignora — sem erro, sem aviso no console — e o nó permanece com o estilo do Modena.

```css
/* PROBLEMA: CSS web válido, mas inútil em JavaFX */
.card {
    background-color: #fff;   /* ignorado */
    margin: 8px;              /* ignorado — não existe */
    padding: 16px;            /* ignorado — sem -fx- */
    border-radius: 4px;       /* ignorado */
}
```

**Fix:** consulte o Reference Guide para cada propriedade. O equivalente correto:

```css
.card {
    -fx-background-color: white;
    -fx-padding: 16;           /* sem px — JavaFX aceita número */
    -fx-background-radius: 4;
    /* margin → use HBox.setMargin / VBox.setMargin na API Java */
}
```

---

### (2) `setStyle` inline espalhado no código

**Problema:** `setStyle` tem a maior precedência na cascata — vence qualquer stylesheet. Quando espalhado em vários pontos do código Java, torna o estilo imune a temas e difícil de manter: trocar a stylesheet da cena não terá efeito nos nós com `setStyle`.

```java
// PROBLEMA: estilo fixado no código, imune a qualquer tema
button.setStyle("-fx-background-color: blue; -fx-text-fill: white;");
label.setStyle("-fx-font-size: 14px;");
pane.setStyle("-fx-padding: 12;");
```

**Fix:** use style classes e centralize em arquivos `.css`. Reserve `setStyle` para valores calculados dinamicamente em runtime (ex.: cor gerada a partir de um dado).

```java
button.getStyleClass().add("primary-button");
label.getStyleClass().add("section-label");
// Os valores ficam no .css — um lugar só para mudar
```

---

### (3) Depender de seletores internos de skin

**Problema:** internamente, controls como `TextField` são compostos por sub-nós com style classes como `.text-field > .text`. Esses seletores de estrutura interna **mudam entre versões do JavaFX** sem aviso, quebrando folhas de estilo que dependem deles.

```css
/* PROBLEMA: estrutura interna — pode mudar na próxima versão */
.text-field > .text {
    -fx-fill: #333;
}
```

**Fix:** aplique o estilo no próprio nó via sua style class pública, ou crie um custom control com style class própria:

```css
/* Fix: style class no nó público */
.search-field {
    -fx-text-fill: #333;
    -fx-font-size: 14px;
}
```

```java
searchField.getStyleClass().add("search-field");
```

---

### (4) Esquecer `toExternalForm()` ao adicionar stylesheet

**Problema:** `getResource()` retorna um objeto `URL` Java. A lista `getStylesheets()` espera uma `String` com a URL em formato externo (ex.: `file:/...` ou `jar:file:/...`). Passar `.toString()` diretamente ou passar a URL errada resulta em stylesheet ignorada silenciosamente — sem exceção, sem aviso visível.

```java
// PROBLEMA: .toString() pode não produzir o formato esperado
scene.getStylesheets().add(
    getClass().getResource("/app.css").toString()   // pode falhar em jar
);
```

**Fix:** use sempre `.toExternalForm()`:

```java
scene.getStylesheets().add(
    getClass().getResource("/app.css").toExternalForm()
);
```

Se `getResource()` retornar `null` (path errado ou arquivo ausente do classpath), o código lança `NullPointerException`. Verifique que o `.css` está em `src/main/resources` e que o path começa com `/`.

## Em entrevista

### Frase pronta (inglês)

> "JavaFX has its own CSS dialect based on CSS 2.1 — the selector syntax is familiar, but all property names are prefixed with `-fx-`, like `-fx-background-color` or `-fx-text-fill`. There is no `-fx-margin` and no flexbox: layout is handled by the pane API, not by stylesheets. The cascade priority goes from lowest to highest: Modena (the user-agent theme), then Scene stylesheets, then Parent stylesheets, then inline `setStyle` — which always wins and should be used sparingly. For dynamic state, you can create custom pseudo-classes with the `PseudoClass` API and drive them from Java, so domain state like 'overdue' becomes a CSS pseudo-class just like `:hover` or `:disabled`."

### Vocabulário

| Termo PT | Termo EN |
|---|---|
| dialeto de CSS | CSS dialect |
| folha de estilo | stylesheet |
| classe de estilo | style class |
| tema padrão / user-agent | default theme / user-agent stylesheet |
| precedência da cascata | cascade order |
| pseudo-classe de domínio | custom pseudo-class |
| estilo inline | inline style (`setStyle`) |
| prefixo de propriedade | property prefix (`-fx-`) |

## Veja também

- [[02 - Scene graph — stage, scene e nodes]]
- [[03 - Layout panes]]
- [[08 - TableView, cell factories e dados observáveis]]
- [[12 - Custom controls, Canvas e charts]]
- [[03-Dominios/Java/Swing/09 - Look and Feel e temas|Look and Feel (Swing)]]
- [[03-Dominios/Java/JavaFX/index|JavaFX (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Dicionário de Java#CSS do JavaFX (-fx-)|CSS do JavaFX (Dicionário)]]
- [[03-Dominios/Java/Dicionário de Java#Modena|Modena (Dicionário)]]

## Referências

- [JavaFX CSS Reference Guide — OpenJFX 21](https://openjfx.io/javadoc/21/javafx.graphics/javafx/scene/doc-files/cssref.html) — fonte canônica: CSS 2.1 + extensões CSS 3; seletores; pseudo-classes; propriedades -fx-*; PseudoClass API; precedência da cascata; `getStylesheets()`; `setStyle()`
