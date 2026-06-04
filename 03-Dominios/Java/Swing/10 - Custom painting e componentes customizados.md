---
title: "Custom painting e componentes customizados"
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
  - painting
  - custom-component
aliases:
  - Custom painting
  - paintComponent
  - Componente customizado
---

# Custom painting e componentes customizados

> [!abstract] TL;DR
> Quando os componentes prontos do Swing não bastam, você estende `JComponent` ou `JPanel` e sobrescreve `paintComponent(Graphics g)` — **nunca** `paint(g)`. O Swing chama `paint`, que delega para `paintComponent` → `paintBorder` → `paintChildren` nessa ordem; sobrescrever `paint` quebra borders, filhos e o double buffering automático. Dentro de `paintComponent`, chame `super.paintComponent(g)` primeiro (limpa o fundo e deixa o UI delegate pintar), faça cast para `Graphics2D` e use `RenderingHints` para antialiasing. Para redimensionar o conteúdo, sobrescreva também `getPreferredSize()`. Para invalidar apenas o que mudou, prefira `repaint(Rectangle)` a `repaint()` completo; quando o tamanho do componente mudar, chame `revalidate()` para recalcular o layout.

## O que é

Custom painting é a técnica de **desenhar diretamente sobre a superfície de um componente** usando a API de 2D do Java (`Graphics`/`Graphics2D`), em vez de compor componentes existentes do Swing.

Os casos de uso típicos são:

- **Gráficos e visualizações** — gráficos de barras, de linhas, mapas de calor, indicadores de status.
- **Controles visuais únicos** — knobs, sliders circulares, barras de progresso com forma customizada.
- **Jogos e animações** — qualquer superfície de renderização que atualiza em loop.
- **Decoração avançada** — fundos com gradiente, bordas com forma, overlays de seleção.

A base do mecanismo é simples: estenda `JComponent` (ou `JPanel` se quiser suporte a filhos) e sobrescreva `paintComponent(Graphics g)`. O Swing chama esse método automaticamente sempre que o componente precisa ser (re)pintado — seja por exposição da janela, resize, ou chamada explícita de `repaint()`.

> *"Many programs will get by just fine without writing their own painting code; they will simply use the standard GUI components that are already available in the Swing API. But if you need specific control over how your graphics are drawn, then this lesson is for you."*
> — The Java Tutorials, Performing Custom Painting

## Como funciona

### A paint chain (`paint` → `paintComponent` / `paintBorder` / `paintChildren`)

O método público de entrada é `paint(Graphics g)`, definido originalmente em `java.awt.Component` e sobrescrito em `JComponent`. O Javadoc é explícito:

> *"This method actually delegates the work of painting to three protected methods: `paintComponent`, `paintBorder`, and `paintChildren`. They're called in the order listed to ensure that children appear on top of component itself."*

A cadeia completa:

```text
JComponent.paint(g)
  ├── paintComponent(g)   ← conteúdo visual do componente
  ├── paintBorder(g)      ← borda (se houver)
  └── paintChildren(g)    ← filhos (se houver)
```

Por que sobrescrever `paintComponent` e **não** `paint`? O Javadoc responde:

> *"A subclass that just wants to specialize the UI (look and feel) delegate's paint method should just override `paintComponent`."*

Sobrescrever `paint` exige reimplementar a delegação para `paintBorder` e `paintChildren` manualmente — qualquer esquecimento faz borders e filhos desaparecerem. Além disso, o double buffering do Swing é coordenado a partir de `paint`; sobrescrevê-lo sem chamar `super.paint(g)` corretamente desliga essa proteção.

Dentro de `paintComponent`, há uma sub-cadeia para componentes padrão (que têm UI delegate):

1. `paintComponent` invoca `ui.update()`.
2. Se o componente é opaco, `ui.update()` preenche o fundo com `background color`.
3. `ui.paint()` renderiza o conteúdo visual do componente.

Para componentes customizados que não têm UI delegate, essa sub-cadeia não existe — você pinta diretamente.

### `paintComponent(Graphics g)` e `Graphics2D` (cast, shapes, `RenderingHints` para antialiasing)

O parâmetro recebido em `paintComponent` é um `Graphics`, mas na prática é sempre uma instância de `Graphics2D` — a API de 2D moderna do Java. O cast é simples e seguro:

```java
@Override
protected void paintComponent(Graphics g) {
    super.paintComponent(g);
    Graphics2D g2 = (Graphics2D) g;
    // ... uso de Graphics2D
}
```

O Javadoc do `paintComponent` avisa: *"We pass the delegate a copy of the `Graphics` object to protect the rest of the paint code from irrevocable changes (for example, `Graphics.translate`)."* Portanto, o objeto recebido já é uma cópia — você pode usá-lo livremente sem criar outra cópia (mas não guarde a referência além do método).

`Graphics2D` adiciona sobre `Graphics`:

- **Shapes geométricas** — `draw(Shape)` e `fill(Shape)` aceitam `Rectangle2D`, `Ellipse2D`, `Arc2D`, `Path2D`, etc.
- **`RenderingHints`** — controlam qualidade de renderização vs. performance.
- **Transforms** — `rotate`, `scale`, `translate` aplicados ao contexto.
- **Compositing** — `setComposite(AlphaComposite...)` para transparência.

O `RenderingHint` mais importante para componentes customizados é o antialiasing, que elimina os degraus (jaggies) em linhas diagonais e curvas:

```java
g2.setRenderingHint(
    RenderingHints.KEY_ANTIALIASING,
    RenderingHints.VALUE_ANTIALIAS_ON
);
g2.setRenderingHint(
    RenderingHints.KEY_TEXT_ANTIALIASING,
    RenderingHints.VALUE_TEXT_ANTIALIAS_ON
);
```

### Double buffering (ligado por padrão no Swing — reduz flicker)

O Swing ativa o double buffering automaticamente em todos os `JComponent`s. O mecanismo: antes de pintar, o Swing aloca um buffer de imagem fora-de-tela (`off-screen buffer`), deixa todo o ciclo `paint` (incluindo `paintComponent` → `paintBorder` → `paintChildren`) acontecer nesse buffer, e só então copia o resultado pronto para a tela em uma única operação.

O efeito visível: **ausência de flickering**. Sem double buffering, cada etapa da paint chain seria visível individualmente — o fundo aparecia, depois o conteúdo, depois a borda — produzindo piscadas perceptíveis. Com o buffer, o usuário sempre vê o frame completo.

O Javadoc de `JComponent` menciona `setDoubleBuffered(boolean)` para controlar esse comportamento, mas na prática não há motivo para desativá-lo. `isDoubleBuffered()` confirma se está ativo.

> [!info] Não confundir com buffers explícitos de animação
> O double buffering automático do Swing é gerenciado pelo `RepaintManager`. Para animações de alta frequência (jogos, visualizações que atualizam > 30 fps), pode ser necessário usar `BufferStrategy` (API do AWT de mais baixo nível) em vez do ciclo de repaint do Swing.

### `repaint(Rectangle)` vs `revalidate()`

Estas duas chamadas têm propósitos distintos e são frequentemente confundidas.

**`repaint()`** — agenda uma repintura do componente. O Swing marca a região como "suja" (`dirty`) e, o mais breve possível, chama `paint`. Existe em várias sobrecargas:

- `repaint()` — agenda repintura de todo o componente.
- `repaint(int x, int y, int width, int height)` — apenas a sub-região especificada.
- `repaint(Rectangle r)` — idem, com objeto `Rectangle`.

Quando apenas o **visual** muda (cores, valores, posições internas de desenho), mas o **tamanho do componente** permanece o mesmo, use `repaint()` ou `repaint(Rectangle)`. A versão com `Rectangle` é preferível se você sabe exatamente qual área mudou — o Swing otimiza o ciclo de pintura para pintar apenas as regiões sujas.

**`revalidate()`** — invalida a hierarquia de layout e agenda um `validate()`. Deve ser chamado quando o **tamanho preferido** do componente muda (por exemplo, o conteúdo cresceu, a fonte foi trocada) e o layout manager precisa recalcular posições e tamanhos. O Javadoc descreve: *"Supports deferred automatic layout. Invalidates the component hierarchy up to the nearest validate root and schedules a request to re-layout the hierarchy."*

A sequência idiomática quando tamanho e visual mudam juntos:

```java
// alguma propriedade interna do componente mudou,
// afetando tanto o visual quanto o tamanho:
this.valor = novoValor;
revalidate();   // recalcula o layout
repaint();      // agenda a repintura com o novo visual
```

### Criar componente reutilizável (estender `JComponent`/`JPanel`, sobrescrever `paintComponent` + `getPreferredSize`)

A estrutura mínima de um componente customizado reutilizável:

1. **Estender `JComponent`** (sem filhos) ou **`JPanel`** (com filhos ou que precise de suporte a `LayoutManager`).
2. **Sobrescrever `paintComponent(Graphics g)`** — toda lógica de desenho fica aqui.
3. **Sobrescrever `getPreferredSize()`** — diz ao layout manager quanto espaço o componente precisa. Sem isso, o tamanho preferido é `(0, 0)` e o componente pode se tornar invisível com `FlowLayout` ou `BoxLayout` (ver Armadilha 3 da nota [[03-Dominios/Java/Swing/03 - Layout managers|Layout managers]]).
4. **Expor a lógica via setters** — quando propriedades mudam, chame `repaint()` (e `revalidate()` se o tamanho mudar).

```java
public class StatusIndicator extends JComponent {

    private Color cor = Color.GRAY;

    public void setCor(Color cor) {
        this.cor = cor;
        repaint(); // agenda repintura — não desenha diretamente aqui
    }

    @Override
    public Dimension getPreferredSize() {
        return new Dimension(24, 24);
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);                   // limpa o fundo
        Graphics2D g2 = (Graphics2D) g;
        g2.setRenderingHint(
            RenderingHints.KEY_ANTIALIASING,
            RenderingHints.VALUE_ANTIALIAS_ON);
        g2.setColor(cor);
        g2.fillOval(2, 2, getWidth() - 4, getHeight() - 4);
    }
}
```

## Na prática

O exemplo a seguir implementa um `BadgeComponent` — um indicador circular que exibe um número (como um badge de notificações), com antialiasing e tamanho dinâmico baseado no valor exibido.

```java
import javax.swing.*;
import java.awt.*;
import java.awt.geom.Ellipse2D;

/**
 * Indicador de badge circular (ex: contador de notificações).
 * Componente reutilizável que estende JComponent e sobrescreve
 * paintComponent + getPreferredSize.
 */
public class BadgeComponent extends JComponent {

    private int valor;
    private Color corFundo  = new Color(220, 53, 69);   // vermelho
    private Color corTexto  = Color.WHITE;
    private Font  fonte     = new Font(Font.SANS_SERIF, Font.BOLD, 11);

    public BadgeComponent(int valor) {
        this.valor = valor;
        setOpaque(false); // fundo transparente (o badge é oval, não retangular)
    }

    public void setValor(int valor) {
        this.valor = valor;
        revalidate(); // tamanho pode mudar (ex: 9 → 10 é mais largo)
        repaint();
    }

    @Override
    public Dimension getPreferredSize() {
        // Calcula largura mínima baseada no texto; mínimo é um círculo de 20px
        FontMetrics fm = getFontMetrics(fonte);
        String texto = String.valueOf(valor);
        int largura = Math.max(20, fm.stringWidth(texto) + 10);
        return new Dimension(largura, 20);
    }

    @Override
    public Dimension getMinimumSize() {
        return getPreferredSize();
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g); // ① limpa fundo e deixa UI delegate agir primeiro

        Graphics2D g2 = (Graphics2D) g; // ② cast seguro: Swing sempre passa Graphics2D

        // ③ antialiasing para curvas suaves
        g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING,
                            RenderingHints.VALUE_ANTIALIAS_ON);
        g2.setRenderingHint(RenderingHints.KEY_TEXT_ANTIALIASING,
                            RenderingHints.VALUE_TEXT_ANTIALIAS_ON);

        int w = getWidth();
        int h = getHeight();

        // ④ preenche o oval com a cor de fundo do badge
        g2.setColor(corFundo);
        g2.fill(new Ellipse2D.Float(0, 0, w, h));

        // ⑤ texto centralizado
        g2.setColor(corTexto);
        g2.setFont(fonte);
        FontMetrics fm = g2.getFontMetrics();
        String texto = String.valueOf(valor);
        int xTexto = (w - fm.stringWidth(texto)) / 2;
        int yTexto = (h - fm.getHeight()) / 2 + fm.getAscent();
        g2.drawString(texto, xTexto, yTexto);
    }
}
```

```text
// Uso:
// BadgeComponent badge = new BadgeComponent(3);
// panel.add(badge); // tamanho preferido calculado automaticamente
//
// Para atualizar:
// badge.setValor(12); // revalidate() + repaint() chamados internamente
//
// Resultado visual: oval vermelho com número branco em negrito,
// centralizado, com antialiasing nas bordas.
```

O componente funciona corretamente com qualquer layout manager porque `getPreferredSize()` retorna um tamanho significativo. Quando o valor muda de um para dois dígitos, `revalidate()` dispara o recálculo do layout para acomodar a largura extra.

## Armadilhas

### (1) Sobrescrever `paint(g)` em vez de `paintComponent(g)`

**Descrição.** Sobrescrever o método `paint(Graphics g)` em vez de `paintComponent(Graphics g)` parece funcionar para o caso simples — o conteúdo aparece — mas silenciosamente quebra três mecanismos:

- **Borders** — `paintBorder` não é chamado porque ele depende de `paint` chamar sua sub-cadeia; ao sobrescrever `paint` sem propagar, a borda some.
- **Filhos** — `paintChildren` idem; componentes filho adicionados ao painel deixam de ser pintados.
- **Double buffering** — o `RepaintManager` do Swing coordina o buffer fora-de-tela a partir de `paint`; sobrescrevê-lo sem chamar `super.paint(g)` pode desativar o buffer e introduzir flickering.

```java
// RUIM — sobrescrever paint em vez de paintComponent
public class GraficoPanel extends JPanel {
    @Override
    public void paint(Graphics g) {
        // ausência de super.paint(g) → borders e filhos não pintam,
        // double buffering possivelmente desativado
        g.setColor(Color.BLUE);
        g.fillRect(0, 0, getWidth(), getHeight());
    }
}
```

**Fix:** sobrescreva `paintComponent`, nunca `paint`.

```java
@Override
protected void paintComponent(Graphics g) {
    super.paintComponent(g);
    g.setColor(Color.BLUE);
    g.fillRect(0, 0, getWidth(), getHeight());
}
```

---

### (2) Não chamar `super.paintComponent(g)` no início

**Descrição.** Omitir a chamada a `super.paintComponent(g)` faz com que o fundo do componente não seja limpo antes de cada ciclo de pintura. O resultado são **artefatos visuais**: pixels de ciclos anteriores ficam visíveis sob o novo desenho, especialmente quando o componente move ou anima objetos que não cobrem toda a área. O Javadoc é explícito: *"if you do not invoke super's implementation you must honor the opaque property, that is if this component is opaque, you must completely fill in the background in an opaque color. If you do not honor the opaque property you will likely see visual artifacts."*

```java
// RUIM — sem super.paintComponent(g): resíduos de frames anteriores ficam visíveis
@Override
protected void paintComponent(Graphics g) {
    // super.paintComponent(g) ausente!
    Graphics2D g2 = (Graphics2D) g;
    g2.setColor(Color.RED);
    // se o círculo mover, o rastro da posição anterior permanece visível
    g2.fillOval(xAtual, yAtual, 20, 20);
}
```

**Fix:** sempre a primeira linha é `super.paintComponent(g)`.

```java
@Override
protected void paintComponent(Graphics g) {
    super.paintComponent(g); // limpa o fundo (ou deixa o L&F fazer)
    Graphics2D g2 = (Graphics2D) g;
    g2.setColor(Color.RED);
    g2.fillOval(xAtual, yAtual, 20, 20);
}
```

---

### (3) Desenhar fora do `paintComponent` — guardar o objeto `Graphics` ou pintar de outra thread

**Descrição.** O objeto `Graphics` (ou `Graphics2D`) recebido em `paintComponent` é válido **apenas durante aquela invocação**. Guardar a referência em um campo e usá-la depois (por exemplo, em um `ActionListener` ou em uma thread de background) produz comportamento indefinido: `NullPointerException`, gráficos corrompidos, ou simplesmente nada desenhado. Da mesma forma, tentar obter um contexto gráfico chamando `component.getGraphics()` de fora do `paintComponent` é explicitamente desencorajado — o contexto retornado é descartado após o próximo repaint e o desenho feito nele some.

Além disso, pintar de uma thread que não seja a EDT viola a single-thread rule do Swing (ver [[03-Dominios/Java/Swing/05 - A Event Dispatch Thread|A Event Dispatch Thread]]) — o Swing não sincroniza o acesso à superfície de pintura.

```java
// RUIM — guarda Graphics fora do paintComponent
public class AnimacaoPanel extends JPanel {
    private Graphics graficoSalvo; // NUNCA faça isso

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        graficoSalvo = g; // referência inválida após este método retornar
    }

    void atualizar() {
        if (graficoSalvo != null) {
            graficoSalvo.drawLine(0, 0, 100, 100); // comportamento indefinido
        }
    }
}
```

**Fix:** todo desenho vai dentro de `paintComponent`; para atualizar o visual, mude o estado interno e chame `repaint()`.

```java
public class AnimacaoPanel extends JPanel {
    private int progresso = 0;

    void setProgresso(int p) {
        this.progresso = p;
        repaint(); // agenda: Swing chamará paintComponent na EDT
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        g.setColor(Color.GREEN);
        g.fillRect(0, 0, progresso, getHeight()); // usa estado, não referência externa
    }
}
```

## Em entrevista

### Frase pronta (inglês)

> "In Swing, custom painting means extending `JComponent` or `JPanel` and overriding `paintComponent(Graphics g)` — not `paint`. The reason is that `paint` is the orchestrator: it calls `paintComponent`, then `paintBorder`, then `paintChildren` in that order, so overriding `paint` directly breaks borders, child components, and the automatic double buffering that `RepaintManager` coordinates at that level. Inside `paintComponent`, the first line is always `super.paintComponent(g)` to let the UI delegate clear the background; after that I cast `Graphics` to `Graphics2D` — it's always a `Graphics2D` at runtime — and set `RenderingHints` for antialiasing before drawing shapes. For a reusable component I also override `getPreferredSize()` so layout managers know how much space to allocate. When the visual changes but the size stays the same, I call `repaint()` — or `repaint(Rectangle)` for a specific dirty region. When the size itself changes, I call `revalidate()` followed by `repaint()` so the layout manager recalculates positions before the next paint cycle. One thing I'm careful about: never hold a reference to the `Graphics` object outside of `paintComponent`, and never paint from a background thread — both lead to undefined behavior."

### Vocabulário

| Termo PT | Termo EN |
|----------|----------|
| pintura customizada | custom painting |
| cadeia de pintura | paint chain |
| buffer fora-de-tela | off-screen buffer / double buffer |
| artefatos visuais | visual artifacts / painting artifacts |
| delegado de UI | UI delegate (`ComponentUI`) |
| dicas de renderização | rendering hints |
| suavização de bordas | antialiasing |
| região suja | dirty region |
| invalidar layout | invalidate / revalidate |
| tamanho preferido | preferred size |
| componente opaco | opaque component |

## Veja também

- [[03-Dominios/Java/Swing/03 - Layout managers|Layout managers]]
- [[03-Dominios/Java/Swing/08 - Renderers e editors|Renderers e editors]]
- [[03-Dominios/Java/Swing/09 - Look and Feel e temas|Look and Feel e temas]]
- [[03-Dominios/Java/Swing/11 - Action API, key bindings e performance|Action API, key bindings e performance]]
- [[03-Dominios/Java/Swing/index|Swing (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Dicionário de Java#paintComponent / custom painting|paintComponent / custom painting]]
- [[03-Dominios/Java/Dicionário de Java#double buffering|double buffering]]

## Referências

- [Performing Custom Painting — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/uiswing/painting/index.html)
- [A Closer Look at the Paint Mechanism — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/uiswing/painting/closer.html)
- [Solving Common Painting Problems — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/uiswing/painting/problems.html)
- [JComponent — Javadoc Java 21 (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.desktop/javax/swing/JComponent.html)
