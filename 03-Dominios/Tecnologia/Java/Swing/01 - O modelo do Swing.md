---
title: "O modelo do Swing"
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
  - fundamentos
aliases:
  - Swing
  - Modelo do Swing
---

# O modelo do Swing

> [!abstract] TL;DR
> **Swing** é o toolkit de GUI desktop do Java, parte do JFC (Java Foundation Classes). Seus componentes são **lightweight** — pintados inteiramente em Java, sem peers nativos do SO — o que garante consistência visual entre plataformas. A arquitetura de **pluggable look-and-feel** permite trocar a aparência em tempo de execução. Todo acesso a componentes Swing deve ocorrer na **Event Dispatch Thread (EDT)**; violar essa regra produz falhas intermitentes difíceis de rastrear.

## O que é

**Swing** é o framework de GUI incluído no JDK como parte do **JFC (Java Foundation Classes)** — o conjunto de funcionalidades para construção de interfaces gráficas em Java. O JFC engloba cinco grandes áreas: os componentes Swing, o suporte a pluggable look-and-feel, a API de Acessibilidade, a Java 2D API e suporte a internacionalização. A trilha Swing concentra-se nos componentes `J*` que formam o toolkit propriamente dito.

### Lightweight vs heavyweight

A distinção fundamental entre Swing e seu predecessor, o **AWT (Abstract Window Toolkit)**, está no modelo de componentes:

- **Componentes heavyweight (AWT)** possuem um *peer* nativo: para cada `Button` AWT existe um botão real do SO subjacente. O SO é responsável por pintar e responder a eventos. Isso torna o comportamento dependente de plataforma e limita a customização visual.
- **Componentes lightweight (Swing)** não têm peer nativo equivalente. São pintados inteiramente pelo Java 2D sobre uma janela nativa mínima. O JDK controla toda a renderização, o que garante aparência consistente entre plataformas e permite o sistema de pluggable look-and-feel.

Os componentes Swing seguem a convenção de prefixo `J`: `JButton`, `JLabel`, `JTable`, etc. — o `J` diferencia da contraparte AWT (`Button`, `Label`). As classes AWT (`java.awt.*`) ainda existem e formam a base da hierarquia; Swing estende AWT, não o substitui integralmente.

### Por que Swing nasceu

O AWT, lançado com o Java 1.0, dependia de peers nativos para cada componente. Isso criava o problema do "menor denominador comum": só era possível usar features presentes em todos os SOs suportados. Componentes tinham aparência e comportamento levemente diferentes em cada plataforma, e a customização visual era extremamente limitada. O Swing foi introduzido no Java 1.2 para resolver essas limitações: componentes 100% Java com aparência programável, hierarquia rica e model-view-controller integrado.

## Por que importa

Para um desenvolvedor sênior, Swing aparece em dois contextos principais:

1. **Ferramentas e IDEs**: IntelliJ IDEA, NetBeans e muitas ferramentas internas corporativas são construídas em Swing. Entender o modelo é pré-requisito para trabalhar nesses codebases ou depurar problemas de UI em ferramentas próprias.
2. **Entrevistas**: a pergunta sobre Swing testa compreensão de **por que o modelo é single-threaded** (a EDT) e **o que distingue lightweight de heavyweight**. Candidatos que apenas sabem "criar uma janela" ficam presos quando o entrevistador pergunta "por que `invokeLater`?" ou "o que acontece se você chamar `setText` de outra thread?". O modelo conceitual — não o catálogo de componentes — é o que diferencia.

## Como funciona

### Hierarquia `Component` → `Container` → `JComponent`

Toda GUI Swing é construída sobre a hierarquia de classes do `java.awt`:

```text
java.lang.Object
  └── java.awt.Component          // pintável, tem posição/tamanho, recebe eventos
      └── java.awt.Container      // pode conter outros Component
          └── javax.swing.JComponent  // base de quase todos os componentes Swing
                  ├── JLabel, JButton, JTextField, JTable, JTree …
                  └── JPanel (container genérico)
```

`JComponent` adiciona sobre o AWT: o mecanismo de pluggable look-and-feel (via `ComponentUI`), double buffering para reduzir flickering, suporte a borders, tool tips e key bindings. Os **top-level containers** (`JFrame`, `JDialog`, `JWindow`) são exceção: eles herdam diretamente de contrapartes AWT heavyweight, pois precisam de uma janela nativa real como âncora de renderização.

### Top-level containers (`JFrame`, `JDialog`, `JWindow`) e o content pane

Toda hierarquia de componentes Swing precisa de um **top-level container** como raiz. Os três principais são:

- **`JFrame`** — janela principal de uma aplicação desktop. Possui barra de título, bordas e controles do SO.
- **`JDialog`** — janela secundária, modal ou não-modal, dependente de um frame pai.
- **`JWindow`** — janela sem decoração (sem título, sem bordas do SO); usada para splash screens ou popups customizados.

Internamente, cada top-level container possui um **root pane** (`JRootPane`) que organiza quatro camadas:

```text
JFrame
  └── JRootPane
      ├── Glass Pane      (intercepta eventos; pintado sobre tudo)
      ├── Layered Pane    (suporta z-ordering entre filhos)
      │   ├── Menu Bar    (opcional, fora do content pane)
      │   └── Content Pane ← onde os componentes da aplicação ficam
```

O **content pane** é o container onde se adicionam os componentes visíveis da aplicação. Desde o Java 5, os métodos `add()`, `remove()` e `setLayout()` do `JFrame` redirecionam automaticamente para o content pane:

```java
frame.add(panel);  // equivalente a frame.getContentPane().add(panel)
```

O content pane padrão usa `BorderLayout` como gerenciador de layout.

### Ciclo de vida de uma janela (`pack` / `setVisible` / `setDefaultCloseOperation`)

O padrão canônico para criar e exibir uma janela Swing envolve três chamadas:

| Método | O que faz |
|--------|-----------|
| `pack()` | Calcula o tamanho preferido do frame com base nos componentes e seus layout managers. Deve ser chamado depois de adicionar todos os componentes. |
| `setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE)` | Define o que acontece quando o usuário fecha a janela. `EXIT_ON_CLOSE` termina a JVM; `DISPOSE_ON_CLOSE` destrói a janela mas mantém a JVM viva. |
| `setVisible(true)` | Torna a janela visível e dispara o primeiro repaint. Deve ser a última chamada, sempre na EDT. |

### Pluggable look-and-feel (introdução)

Swing implementa uma arquitetura **Model-View-Controller** onde a renderização visual é delegada a um objeto `ComponentUI` por componente. Isso permite trocar o "tema" de toda a aplicação em tempo de execução sem recompilar:

```java
UIManager.setLookAndFeel("javax.swing.plaf.metal.MetalLookAndFeel"); // lança exceções checked (UnsupportedLookAndFeelException etc.) — trate com try/catch em código real
SwingUtilities.updateComponentTreeUI(frame);  // propaga a mudança para todos os filhos
```

O JDK inclui os L&Fs Metal (padrão Java), Nimbus, e wrappers para aparência nativa de Windows e GTK+. O mecanismo completo — incluindo como customizar tokens de cor e criar L&Fs próprios — é tema de outra nota do galho.

## Na prática

O padrão observado em aplicações Swing e em ferramentas do JDK é construir e exibir toda a UI dentro de um `Runnable` agendado via `SwingUtilities.invokeLater`, garantindo que a construção ocorra na EDT.

```java
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.SwingUtilities;
import java.awt.BorderLayout;

public class HelloSwing {

    private static void buildAndShow() {
        JFrame frame = new JFrame("Hello Swing");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        JPanel panel = new JPanel(new BorderLayout());
        JLabel label = new JLabel("Olá, Swing!", JLabel.CENTER);
        panel.add(label, BorderLayout.CENTER);

        frame.add(panel);   // adiciona ao content pane via conveniência
        frame.pack();
        frame.setVisible(true);
    }

    public static void main(String[] args) {
        // Garante que a UI seja construída na EDT
        SwingUtilities.invokeLater(HelloSwing::buildAndShow);
    }
}
```

```text
// Resultado: janela com título "Hello Swing" exibindo "Olá, Swing!" centralizado.
```

Pontos de atenção no exemplo:
- `invokeLater` agenda a execução na EDT sem bloquear a thread chamadora (aqui, a `main`).
- `pack()` antes de `setVisible(true)` é a ordem correta; inverter causa layout incorreto.
- `EXIT_ON_CLOSE` é adequado para aplicações standalone; em ferramentas embedded, prefere-se `DISPOSE_ON_CLOSE`.

## Armadilhas

### (1) Misturar componentes AWT e Swing (problemas de z-order e repaint)

**O problema:** usar componentes AWT heavyweight (como `java.awt.Button` ou `java.awt.Canvas`) dentro de containers Swing lightweight cria conflitos de z-order. Como componentes heavyweight sempre ficam "acima" dos lightweight no sistema de pintagem, menus Swing podem ficar escondidos atrás de um canvas AWT, e repaints ficam inconsistentes.

```java
// hipotético: mistura incorreta
JFrame frame = new JFrame();
java.awt.Button awtButton = new java.awt.Button("AWT");  // heavyweight
JPanel panel = new JPanel();
panel.add(awtButton);   // AWT dentro de Swing → conflito de z-order
frame.add(panel);
```

**Fix:** use exclusivamente componentes Swing (`J*`) dentro de hierarquias Swing. Se precisar de um canvas para renderização customizada, use `JPanel` com `paintComponent` sobrescrito. A única exceção aceita são os próprios top-level containers (`JFrame`/`JDialog`), que são necessariamente heavyweight.

---

### (2) Construir ou modificar a UI fora da EDT

**O problema:** Swing não é thread-safe. Criar componentes, modificar seu estado (`setText`, `setEnabled`, `repaint`) ou chamar `setVisible` a partir de qualquer thread que não seja a EDT viola o contrato do framework. O sintoma é **não-determinístico e intermitente**: a aplicação pode funcionar corretamente na maioria das execuções e produzir renderizações corrompidas, exceções `NullPointerException` ou deadlocks sob determinadas condições de scheduling.

```java
// hipotético: violação da EDT
new Thread(() -> {
    JLabel label = new JLabel("Carregando...");
    frame.add(label);         // fora da EDT — comportamento indefinido
    frame.revalidate();
}).start();
```

**Fix:** qualquer acesso a componentes Swing que não esteja na EDT deve ser agendado via `SwingUtilities.invokeLater` (assíncrono) ou `SwingUtilities.invokeAndWait` (síncrono, quando o resultado é necessário imediatamente):

```java
SwingUtilities.invokeLater(() -> {
    label.setText("Concluído");
    frame.revalidate();
});
```

## Em entrevista

### Frase pronta (inglês)

> "Swing is Java's desktop GUI toolkit, part of the Java Foundation Classes. The key architectural decision is that Swing components are *lightweight* — they have no native OS peer and are painted entirely by Java's 2D rendering engine, which means the same component looks and behaves consistently across platforms, unlike AWT's heavyweight peer model where each widget delegated to the native OS. This also enables the *pluggable look-and-feel* system: the rendering of every component is delegated to a `ComponentUI` object that can be swapped at runtime, so you can switch between Metal, Nimbus, or a native-themed L&F without recompiling. The trade-off is that Swing is single-threaded by design — all component creation and mutation must happen on the Event Dispatch Thread; violating this produces non-deterministic corruption that's notoriously hard to reproduce in a debugger. The caveat in modern Java is that Swing is mature and stable but no longer receiving new features; for greenfield desktop apps the community increasingly looks at JavaFX or web-based UIs, though Swing remains the foundation of major IDEs and internal tooling built on the JDK."

### Vocabulário

| Termo PT | Termo EN |
|----------|----------|
| componente lightweight | lightweight component |
| componente heavyweight | heavyweight component |
| peer nativo | native peer |
| aparência plugável | pluggable look-and-feel (L&F) |
| hierarquia de contenção | containment hierarchy |
| painel de conteúdo | content pane |
| thread de despacho de eventos | Event Dispatch Thread (EDT) |
| delegado de UI | UI delegate (`ComponentUI`) |
| janela de nível superior | top-level container |
| double buffering | double buffering |

## Veja também

- [[03-Dominios/Tecnologia/Java/Swing/02 - Componentes e containers|Componentes e containers]]
- [[03-Dominios/Tecnologia/Java/Swing/03 - Layout managers|Layout managers]]
- [[03-Dominios/Tecnologia/Java/Swing/04 - O modelo de eventos|O modelo de eventos]]
- [[03-Dominios/Tecnologia/Java/Swing/05 - A Event Dispatch Thread|A Event Dispatch Thread (EDT)]]
- [[03-Dominios/Tecnologia/Java/Swing/12 - Swing hoje - estado atual|Swing hoje: estado atual]]
- [[03-Dominios/Tecnologia/Java/Swing/index|Swing (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/index|Linguagem e sintaxe moderna]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#AWT (Abstract Window Toolkit)|AWT]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#componente lightweight / heavyweight|lightweight vs heavyweight]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#content pane|content pane]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#JComponent|JComponent]]

## Referências

- [About the JFC and Swing — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/uiswing/start/about.html)
- [Using Top-Level Containers — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/uiswing/components/toplevel.html)
- [javax.swing — Javadoc Java 21 (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.desktop/javax/swing/package-summary.html)
- [JComponent — Javadoc Java 21 (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.desktop/javax/swing/JComponent.html)
- [Creating a GUI With Swing — dev.java](https://dev.java/learn/creating-gui-apps-with-swing/)
