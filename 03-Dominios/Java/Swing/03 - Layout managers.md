---
title: "Layout managers"
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
  - layout
aliases:
  - Layout managers
  - BorderLayout
  - GridBagLayout
---

# Layout managers

> [!abstract] TL;DR
> **Layout managers** são objetos que calculam automaticamente posição e tamanho dos componentes dentro de um container. Eles tornam a UI responsiva a resize, mudanças de DPI e diferentes look-and-feels — coisas que o posicionamento absoluto (`null` layout) quebra silenciosamente. O **`BorderLayout`** e o **`FlowLayout`** são os padrões (content pane e `JPanel`, respectivamente). Para formulários e UIs complexas feitas à mão, o **`GridBagLayout`** é o mais poderoso; para UIs geradas por GUI builders, o **`GroupLayout`**. Aninhar `JPanel`s com layouts diferentes é a técnica principal para composição.

## O que é

Um **layout manager** é um objeto que implementa a interface `java.awt.LayoutManager` (ou sua extensão `LayoutManager2`) e é associado a um `Container`. Toda vez que o container precisa se posicionar — ao ser exibido, redimensionado ou após `revalidate()` — ele delega para o layout manager o cálculo de onde cada filho vai ficar e qual tamanho vai ter.

Esse modelo resolve problemas reais:

- **Resize automático:** quando o usuário arrasta a borda da janela, o layout recalcula; com posicionamento absoluto, os componentes ficam presos onde foram colocados.
- **DPI e fonte variável:** em telas de alta resolução ou com fontes maiores (acessibilidade), as dimensões preferidas dos componentes aumentam; o layout manager absorve essa variação.
- **Look-and-feel diferente:** um `JButton` no Nimbus pode ser ligeiramente mais largo do que no Metal; o recálculo de layout é automático.

A API de configuração é direta:

```java
// via construtor do panel
JPanel panel = new JPanel(new BorderLayout());

// via setLayout (útil para content pane)
frame.getContentPane().setLayout(new FlowLayout());
```

## Como funciona

### `BorderLayout` / `FlowLayout` / `GridLayout` (os básicos)

**`BorderLayout`** (padrão do content pane de `JFrame`/`JDialog`) divide o container em cinco zonas constantes: `NORTH`, `SOUTH`, `EAST`, `WEST` e `CENTER`. Todo espaço restante após alocar as bordas vai para `CENTER`. Ideal para a estrutura principal de uma janela: toolbar no `NORTH`, status bar no `SOUTH`, navegação lateral no `WEST`, conteúdo principal no `CENTER`.

```java
JPanel main = new JPanel(new BorderLayout());
main.add(new JToolBar(), BorderLayout.NORTH);
main.add(new JScrollPane(table), BorderLayout.CENTER);
main.add(statusLabel, BorderLayout.SOUTH);
```

**`FlowLayout`** (padrão de `JPanel`) posiciona componentes em linha, da esquerda para a direita, quebrando para a próxima linha quando o espaço horizontal se esgota. Respeita o tamanho preferido de cada componente mas não estica nenhum deles. Bom para grupos de botões compactos; ruim para qualquer coisa que precise se expandir.

```java
JPanel buttons = new JPanel(new FlowLayout(FlowLayout.RIGHT, 8, 4));
buttons.add(cancelButton);
buttons.add(okButton);
```

**`GridLayout`** divide o container em células de tamanho uniforme — todos os filhos recebem exatamente o mesmo espaço, independentemente do tamanho preferido deles. Número de linhas e colunas são definidos no construtor (usar 0 em um dos eixos deixa crescer livremente). Ideal para matrizes de botões, teclados numéricos, grades de ícones onde a uniformidade é desejada — e problemático quando os componentes têm tamanhos naturalmente diferentes.

```java
JPanel numpad = new JPanel(new GridLayout(4, 3, 2, 2)); // 4 linhas, 3 colunas, gaps
for (String digit : new String[]{"7","8","9","4","5","6","1","2","3","*","0","#"}) {
    numpad.add(new JButton(digit));
}
```

### `BoxLayout` e `CardLayout`

**`BoxLayout`** arranja componentes em uma única linha (`X_AXIS`) ou coluna (`Y_AXIS`). Ao contrário do `GridLayout`, ele respeita o tamanho preferido e máximo de cada filho — componentes não crescem além do `getMaximumSize()`. É o layout recomendado para colunas de formulário simples e barras de ferramentas verticais. `Box.createVerticalGlue()` e `Box.createRigidArea()` servem para espaçamento flexível e fixo, respectivamente.

```java
JPanel sidebar = new JPanel();
sidebar.setLayout(new BoxLayout(sidebar, BoxLayout.Y_AXIS));
sidebar.add(navButton1);
sidebar.add(navButton2);
sidebar.add(Box.createVerticalGlue()); // empurra o restante para baixo
sidebar.add(settingsButton);
```

**`CardLayout`** empilha componentes como um baralho: apenas um "card" (painel) é visível por vez. A troca é feita por `show(container, name)`, `next()` ou `previous()`. É a base natural para wizards e para painéis que alternam conteúdo dependendo de seleção em combo box. A alternativa mais rica é `JTabbedPane`, que oferece navegação visual integrada.

```java
CardLayout cards = new CardLayout();
JPanel deck = new JPanel(cards);
deck.add(stepOnePanel, "step1");
deck.add(stepTwoPanel, "step2");

// para avançar:
cards.show(deck, "step2");
```

### `GridBagLayout` (o power tool, com `GridBagConstraints`)

**`GridBagLayout`** é o layout manager mais flexível do Swing. Divide o container em um grid onde células podem ter alturas e larguras diferentes, e componentes podem ocupar múltiplas células (`gridwidth`/`gridheight`). Cada componente recebe um objeto `GridBagConstraints` com as regras de posicionamento.

Os campos essenciais de `GridBagConstraints`:

| Campo | Descrição |
|-------|-----------|
| `gridx`, `gridy` | Coluna e linha da célula inicial (`GridBagConstraints.RELATIVE` para automático) |
| `gridwidth`, `gridheight` | Quantas colunas/linhas o componente ocupa |
| `weightx`, `weighty` | Proporção de espaço extra que essa coluna/linha absorve (0.0 = não estica; 1.0 = absorve todo o espaço) |
| `fill` | Como o componente preenche o espaço da célula: `NONE`, `HORIZONTAL`, `VERTICAL`, `BOTH` |
| `anchor` | Alinhamento quando o componente não preenche a célula: `CENTER`, `WEST`, `NORTHWEST`, etc. |
| `insets` | Margem externa (`Insets(top, left, bottom, right)`) |
| `ipadx`, `ipady` | Padding interno (adiciona ao tamanho mínimo) |

Padrão canônico: criar uma instância de `GridBagConstraints`, ajustar campos e chamar `add(component, constraints)`:

```java
JPanel form = new JPanel(new GridBagLayout());
GridBagConstraints gbc = new GridBagConstraints();
gbc.insets = new Insets(4, 4, 4, 4);

// Linha 0 — label na col 0, field na col 1 expandindo horizontalmente
gbc.gridx = 0; gbc.gridy = 0;
gbc.anchor = GridBagConstraints.WEST;
gbc.fill = GridBagConstraints.NONE;
gbc.weightx = 0.0;
form.add(new JLabel("Nome:"), gbc);

gbc.gridx = 1;
gbc.fill = GridBagConstraints.HORIZONTAL;
gbc.weightx = 1.0;  // campo de texto expande
form.add(new JTextField(20), gbc);

// Linha 1 — text area ocupando 2 colunas e expandindo em ambas as direções
gbc.gridx = 0; gbc.gridy = 1;
gbc.gridwidth = 2;
gbc.fill = GridBagConstraints.BOTH;
gbc.weightx = 1.0; gbc.weighty = 1.0;  // expande vertical
form.add(new JScrollPane(new JTextArea()), gbc);
```

### `GroupLayout` (gerado por GUI builders)

**`GroupLayout`** trabalha com dois eixos independentes: para cada componente é preciso declarar onde ele fica tanto na hierarquia horizontal quanto na vertical. Isso dá controle total sobre alinhamento entre grupos de componentes, mas torna o código manual prolixo e difícil de manter. O `GroupLayout` é o layout que ferramentas como o NetBeans GUI Builder geram automaticamente; para código escrito à mão, `GridBagLayout` ou composição de `BorderLayout` + `BoxLayout` são mais práticos.

### Aninhar painéis para layouts complexos

Nenhum layout manager sozinho cobre todos os casos. A técnica padrão é compor vários `JPanel`s com layouts simples para atingir o resultado desejado. Um `BorderLayout` no nível externo + painéis internos com `BoxLayout` ou `GridBagLayout` cobre a maioria dos casos reais sem a complexidade de um `GridBagLayout` único para toda a tela.

### Sizing (`preferred` / `minimum` / `maximum`)

Todo `Component` expõe três hints de tamanho que os layout managers consultam:

- **`getPreferredSize()`** — tamanho ideal. A maioria dos layouts tenta honrá-lo.
- **`getMinimumSize()`** — menor tamanho aceitável. Respeitado por `BorderLayout`, `GridBagLayout` e `BoxLayout`.
- **`getMaximumSize()`** — tamanho máximo. Respeitado principalmente por `BoxLayout`; outros layouts geralmente ignoram.

Há duas formas de definir esses valores: chamar os setters (`setPreferredSize(new Dimension(200, 30))`) ou sobrescrever os getters em uma subclasse. A segunda abordagem é preferível para componentes customizados, pois os hints acompanham a lógica do componente e não dependem de quem instancia.

```java
// setter — adequado para componentes existentes em código de aplicação
textField.setPreferredSize(new Dimension(200, 28));

// override — adequado para componentes customizados
class GraphPanel extends JPanel {
    @Override
    public Dimension getPreferredSize() { return new Dimension(400, 300); }
    @Override
    public Dimension getMinimumSize()   { return new Dimension(100,  75); }
}
```

## Na prática

### Tela mestre-detalhe com `BorderLayout` + painel aninhado

Um padrão clássico: lista de itens à esquerda, formulário de detalhes à direita, barra de botões de ação na base.

```java
import javax.swing.*;
import java.awt.*;

public class MasterDetailPanel extends JPanel {

    public MasterDetailPanel() {
        super(new BorderLayout(8, 0));

        // --- Lado esquerdo: lista mestre ---
        JList<String> masterList = new JList<>(new String[]{"Item A", "Item B", "Item C"});
        masterList.setPreferredSize(new Dimension(160, 0));
        add(new JScrollPane(masterList), BorderLayout.WEST);

        // --- Centro: formulário de detalhes (GridBagLayout) ---
        JPanel detailPanel = buildDetailForm();
        add(detailPanel, BorderLayout.CENTER);

        // --- Sul: barra de ações ---
        JPanel actionBar = new JPanel(new FlowLayout(FlowLayout.RIGHT, 6, 4));
        actionBar.add(new JButton("Cancelar"));
        actionBar.add(new JButton("Salvar"));
        add(actionBar, BorderLayout.SOUTH);
    }

    private JPanel buildDetailForm() {
        JPanel panel = new JPanel(new GridBagLayout());
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.insets = new Insets(4, 6, 4, 6);
        gbc.anchor = GridBagConstraints.WEST;

        // Linha 0: label + campo de texto (expande horizontalmente)
        gbc.gridx = 0; gbc.gridy = 0;
        gbc.fill = GridBagConstraints.NONE; gbc.weightx = 0.0;
        panel.add(new JLabel("Nome:"), gbc);

        gbc.gridx = 1;
        gbc.fill = GridBagConstraints.HORIZONTAL; gbc.weightx = 1.0;
        panel.add(new JTextField(20), gbc);

        // Linha 1: label + combo
        gbc.gridx = 0; gbc.gridy = 1;
        gbc.fill = GridBagConstraints.NONE; gbc.weightx = 0.0;
        panel.add(new JLabel("Status:"), gbc);

        gbc.gridx = 1;
        gbc.fill = GridBagConstraints.HORIZONTAL; gbc.weightx = 1.0;
        panel.add(new JComboBox<>(new String[]{"Ativo", "Inativo"}), gbc);

        // Linha 2: text area ocupando 2 colunas, expande vertical
        gbc.gridx = 0; gbc.gridy = 2;
        gbc.gridwidth = 2;
        gbc.fill = GridBagConstraints.BOTH;
        gbc.weightx = 1.0; gbc.weighty = 1.0;
        panel.add(new JScrollPane(new JTextArea()), gbc);

        return panel;
    }
}
```

```text
// Resultado: painel com lista fixa à esquerda, formulário expansível ao centro
// (nome + status + área de texto), botões alinhados à direita na base.
// Ao redimensionar, somente CENTER e a text area crescem.
```

## Armadilhas

### (1) `null` layout / posicionamento absoluto (`setBounds`)

**O problema:** desativar o layout manager com `container.setLayout(null)` e posicionar componentes via `component.setBounds(x, y, w, h)` produz uma UI que parece funcionar no ambiente de desenvolvimento, mas quebra em produção: componentes ficam sobrepostos ou cortados ao redimensionar a janela, ficam minúsculos em telas de alta resolução (HiDPI), e comportam-se de forma errada com fontes maiores (configurações de acessibilidade) ou com um L&F diferente do que foi usado no design.

```java
// hipotético: posicionamento absoluto — não faça isso
JPanel panel = new JPanel();
panel.setLayout(null);
JLabel label = new JLabel("Nome:");
label.setBounds(10, 10, 60, 25);  // posição hardcoded
panel.add(label);
JTextField field = new JTextField();
field.setBounds(80, 10, 200, 25); // tamanho hardcoded
panel.add(field);
```

**Fix:** use sempre um layout manager. Para formulários simples, `GridBagLayout` ou `BoxLayout` + `JPanel` aninhados resolvem. Se a tela tem design muito preciso, `GroupLayout` (gerado por um GUI builder) é a alternativa correta.

---

### (2) Usar `GridBagLayout` onde `BoxLayout`/`BorderLayout` resolveriam

**O problema:** `GridBagLayout` tem curva de aprendizado alta e constraints verbosas. Usá-lo para tudo — mesmo para um simples par label + campo ou uma coluna de botões — produz código de difícil manutenção sem nenhum benefício funcional.

```java
// hipotético: GridBagLayout desnecessário para coluna de botões
JPanel buttonCol = new JPanel(new GridBagLayout());
GridBagConstraints gbc = new GridBagConstraints();
gbc.gridx = 0; gbc.gridy = 0; gbc.fill = GridBagConstraints.HORIZONTAL;
buttonCol.add(new JButton("Novo"), gbc);
gbc.gridy = 1;
buttonCol.add(new JButton("Editar"), gbc);
gbc.gridy = 2;
buttonCol.add(new JButton("Excluir"), gbc);
```

**Fix:** usar o layout mais simples que resolve o problema.

```java
// fix: BoxLayout para coluna de botões
JPanel buttonCol = new JPanel();
buttonCol.setLayout(new BoxLayout(buttonCol, BoxLayout.Y_AXIS));
buttonCol.add(new JButton("Novo"));
buttonCol.add(new JButton("Editar"));
buttonCol.add(new JButton("Excluir"));
```

---

### (3) Ignorar `getPreferredSize` em componente customizado (vira 0×0)

**O problema:** ao criar um `JPanel` com `paintComponent` sobrescrito para desenho customizado, sem sobrescrever `getPreferredSize()`, o componente retorna `(0, 0)` como tamanho preferido. Layout managers como `BorderLayout` (zona `CENTER`) até esticam o componente — mas `FlowLayout` e `BoxLayout` deixam o componente invisível, e `pack()` no frame resulta em janela mínima que não exibe nada.

```java
// hipotético: painel de gráfico sem preferredSize
class GraphPanel extends JPanel {
    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        // desenha o gráfico... mas o painel tem tamanho (0, 0)
    }
    // sem getPreferredSize() → layout manager não sabe quanto espaço alocar
}
```

**Fix:** sobrescrever `getPreferredSize()` (e idealmente `getMinimumSize()`) no componente customizado.

```java
@Override
public Dimension getPreferredSize() { return new Dimension(400, 300); }
```

## Em entrevista

### Frase pronta (inglês)

> "In Swing, a layout manager is an object that implements `LayoutManager` and is responsible for computing the size and position of every child component inside a container whenever the container is laid out. This means the UI automatically adapts to resize events, different DPI settings, and varying look-and-feels without any hardcoded coordinates. The default layout for a content pane is `BorderLayout` — five named zones, with `CENTER` absorbing extra space — and the default for `JPanel` is `FlowLayout`. For hand-coded complex UIs, `GridBagLayout` is the most flexible option: it uses a grid where cells can span multiple columns and rows and each component gets a `GridBagConstraints` object specifying position, weight, fill, anchor, and insets. The recommended approach for production is to compose multiple nested `JPanel`s with simpler layouts — like `BorderLayout` for the outer shell and `BoxLayout` or `GridBagLayout` for inner forms — rather than fighting a single layout manager for the entire screen. Using a null layout and `setBounds` is an anti-pattern: it breaks on resize, HiDPI displays, and non-default fonts, so it should never appear in production Swing code."

### Vocabulário

| Termo PT | Termo EN |
|----------|----------|
| gerenciador de layout | layout manager |
| posicionamento absoluto | absolute positioning / null layout |
| tamanho preferido | preferred size |
| tamanho mínimo | minimum size |
| tamanho máximo | maximum size |
| restrições de grid | grid bag constraints |
| peso de distribuição | weight (weightx / weighty) |
| preenchimento de célula | fill (HORIZONTAL / VERTICAL / BOTH) |
| âncora de alinhamento | anchor |
| aninhar painéis | nesting panels |
| espaçamento flexível | glue (Box.createVerticalGlue) |
| validar layout | revalidate |

## Veja também

- [[03-Dominios/Java/Swing/01 - O modelo do Swing|O modelo do Swing]]
- [[03-Dominios/Java/Swing/02 - Componentes e containers|Componentes e containers]]
- [[03-Dominios/Java/Swing/10 - Custom painting e componentes customizados|Custom painting e componentes customizados]]
- [[03-Dominios/Java/Swing/index|Swing (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Dicionário de Java#layout manager|layout manager]]
- [[03-Dominios/Java/Dicionário de Java#GridBagLayout|GridBagLayout]]

## Referências

- [A Visual Guide to Layout Managers — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/uiswing/layout/visual.html)
- [Laying Out Components Within a Container — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/uiswing/layout/using.html)
- [BorderLayout — Javadoc Java 21 (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.desktop/java/awt/BorderLayout.html)
- [GridBagLayout — Javadoc Java 21 (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.desktop/java/awt/GridBagLayout.html)
- [GridBagConstraints — Javadoc Java 21 (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.desktop/java/awt/GridBagConstraints.html)
- [BoxLayout — Javadoc Java 21 (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.desktop/javax/swing/BoxLayout.html)
- [CardLayout — Javadoc Java 21 (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.desktop/java/awt/CardLayout.html)
- [GroupLayout — Javadoc Java 21 (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.desktop/javax/swing/GroupLayout.html)
