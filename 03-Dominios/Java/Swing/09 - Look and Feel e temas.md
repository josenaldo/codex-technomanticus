---
title: "Look and Feel e temas"
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
  - look-and-feel
  - ui
aliases:
  - Look and Feel
  - Nimbus
  - FlatLaf
---

# Look and Feel e temas

> [!abstract] TL;DR
> **Look and Feel (L&F)** é o mecanismo do Swing que desacopla a aparência visual dos componentes da sua lógica. O `UIManager` gerencia o L&F ativo; trocar exige `setLookAndFeel` + `SwingUtilities.updateComponentTreeUI`. O JDK vem com quatro L&Fs bundled: **Metal** (padrão cross-platform), **Nimbus** (moderno, vetorial), **system/native** e **Motif** (legado). Para UIs com estética contemporânea (flat, dark mode), a comunidade usa **FlatLaf** — projeto **third-party, open-source** da FormDev, não parte do JDK Oracle.

## O que é

A **aparência plugável (pluggable look-and-feel)** é uma das propriedades arquiteturais centrais do Swing. Ela separa *o que* um componente faz (lógica, modelo) de *como* ele é pintado na tela. Cada componente Swing (`JButton`, `JTable`, `JLabel`…) delega toda a sua renderização a um objeto **`ComponentUI`** — o *UI delegate* —, que pode ser trocado em tempo de execução sem alterar uma linha da lógica da aplicação.

Na prática, um **Look and Feel** é um conjunto coeso de `ComponentUI` para todos os componentes Swing, empacotado em uma subclasse de `LookAndFeel`. Trocar o L&F ativo atualiza esses delegates em todos os componentes, resultando em uma aparência radicalmente diferente — fontes, bordas, paletas de cor, animações — com zero alteração no código de negócio.

Esse desacoplamento é o que torna possível, por exemplo, que o IntelliJ IDEA ofereça temas como IntelliJ Light, Darcula (escuro) e High Contrast mantendo a mesma base de código Swing.

## Como funciona

### L&Fs bundled no JDK

O JDK inclui quatro Look and Feels sem dependências externas:

| L&F | Classe | Quando usar |
|-----|--------|-------------|
| **Metal** | `javax.swing.plaf.metal.MetalLookAndFeel` | Padrão cross-platform; garantido em todos os SOs; tema Ocean por padrão |
| **Nimbus** | `javax.swing.plaf.nimbus.NimbusLookAndFeel` | Vetor-based, escalável; introduzido no JDK 7; mais moderno que o Metal |
| **System/nativo** | `UIManager.getSystemLookAndFeelClassName()` | Aparência do SO: Windows, macOS Aqua ou GTK+ no Linux |
| **Motif** | `com.sun.java.swing.plaf.motif.MotifLookAndFeel` | Legado (Unix/CDE); evitar em código novo |

O **Metal** é o L&F cross-platform padrão — retornado por `UIManager.getCrossPlatformLookAndFeelClassName()`. O **Nimbus** se destaca por usar formas vetoriais (não bitmaps), o que o torna o L&F bundled mais escalável em displays HiDPI; entretanto, alguns detalhes de layout diferem do Metal e podem causar surpresas em código que assume dimensões fixas.

### `UIManager`: a fachada do sistema de L&F

`javax.swing.UIManager` é o ponto central de controle do look-and-feel. Principais métodos:

```java
// Trocar L&F (por nome de classe)
UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");

// Trocar L&F (por instância)
UIManager.setLookAndFeel(new javax.swing.plaf.nimbus.NimbusLookAndFeel());

// Obter o nome da classe do L&F nativo do SO atual
String systemLnF = UIManager.getSystemLookAndFeelClassName();

// Obter o nome da classe do L&F cross-platform (Metal)
String crossLnF = UIManager.getCrossPlatformLookAndFeelClassName();

// Ler um token do UIDefaults
Color bg = UIManager.getColor("Panel.background");
Font font = UIManager.getFont("Button.font");

// Sobrescrever um token (developer defaults)
UIManager.put("Button.font", new Font("Segoe UI", Font.PLAIN, 13));

// Obter todos os defaults do L&F atual
javax.swing.UIDefaults defaults = UIManager.getLookAndFeelDefaults();
```

O `UIManager` mantém três camadas de defaults empilhadas: *system defaults* (JVM), *L&F defaults* e *developer defaults* (via `put`). A resolução de uma chave sempre percorre as camadas do topo para baixo, então um `UIManager.put` sobrescreve o valor do L&F sem alterar o próprio L&F.

### Trocar L&F em runtime

Trocar o L&F depois que a UI já está visível exige duas etapas: setar o novo L&F e propagar a mudança para cada top-level container da aplicação.

```java
try {
    UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
    // Propaga para todas as janelas abertas
    for (Window window : Window.getWindows()) {
        SwingUtilities.updateComponentTreeUI(window);
        window.pack(); // reajusta tamanhos que podem mudar entre L&Fs
    }
} catch (ClassNotFoundException
       | InstantiationException
       | IllegalAccessException
       | UnsupportedLookAndFeelException e) {
    // Tratar ou logar; não silenciar
    e.printStackTrace();
}
```

`SwingUtilities.updateComponentTreeUI(component)` percorre recursivamente toda a hierarquia de componentes a partir do componente informado e reinicia o `ComponentUI` de cada um para o L&F ativo. Sem essa chamada, componentes criados antes da troca continuam usando o `ComponentUI` antigo.

### Ecossistema moderno: FlatLaf (third-party, open-source)

> [!warning] FlatLaf é uma dependência externa — não faz parte do JDK
> **FlatLaf** é um projeto **third-party, open-source** da **FormDev Software GmbH**, licenciado sob Apache 2.0, hospedado em [github.com/JFormDesigner/FlatLaf](https://github.com/JFormDesigner/FlatLaf). Ele **não é produzido nem endossado pela Oracle** e **não está incluído no JDK**. Para usá-lo, a aplicação precisa declarar uma dependência externa e gerenciar essa adição ao classpath.

Para projetos que precisam de aparência flat/moderna com suporte a dark mode, **FlatLaf** é amplamente usado na comunidade Swing. Ele oferece os temas FlatLight, FlatDark, FlatIntelliJ e FlatDarcula, suporte a HiDPI e é a base visual usada pelo próprio IntelliJ IDEA.

**Adicionando ao projeto (Maven — exemplo):**

```xml
<dependency>
    <groupId>com.formdev</groupId>
    <artifactId>flatlaf</artifactId>
    <version>3.4</version> <!-- verifique a versão atual no Maven Central -->
</dependency>
```

**Configuração mínima — deve ocorrer antes de criar qualquer componente:**

```java
// Opção 1: método estático de conveniência (recomendado pelo FlatLaf)
FlatLightLaf.setup();

// Opção 2: via UIManager (equivalente)
try {
    UIManager.setLookAndFeel(new FlatLightLaf());
} catch (UnsupportedLookAndFeelException e) {
    e.printStackTrace();
}

// Após setar o L&F, construir a UI normalmente:
SwingUtilities.invokeLater(() -> {
    JFrame frame = new JFrame("App com FlatLaf");
    // ...
});
```

Para dark mode, substitua `FlatLightLaf` por `FlatDarkLaf`. Ambas as classes estão no pacote `com.formdev.flatlaf`.

### Customização leve sem trocar de L&F

É possível ajustar pontos específicos da aparência sem trocar o L&F inteiro:

```java
// Fonte global de botões
UIManager.put("Button.font", new Font("Segoe UI", Font.PLAIN, 13));

// Borda customizada para um componente específico
JPanel panel = new JPanel();
panel.setBorder(BorderFactory.createLineBorder(Color.GRAY, 1));

// Cor de seleção de tabela
UIManager.put("Table.selectionBackground", new Color(0x0078D7));
```

As chaves disponíveis (como `"Button.font"`, `"Panel.background"`, `"Table.selectionBackground"`) variam por L&F. Uma forma de descobrir todas as chaves ativas é iterar `UIManager.getLookAndFeelDefaults()`.

## Na prática

### Setar o L&F correto na inicialização da aplicação

O padrão canônico é setar o L&F na primeira linha do `main`, *antes* de qualquer código Swing — inclusive antes do `invokeLater`:

```java
public static void main(String[] args) {
    // 1. Setar L&F ANTES de criar qualquer componente
    try {
        UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
    } catch (ClassNotFoundException
           | InstantiationException
           | IllegalAccessException
           | UnsupportedLookAndFeelException e) {
        // System L&F indisponível; Metal será usado como fallback automático
        System.err.println("L&F não disponível: " + e.getMessage());
    }

    // 2. Construir a UI na EDT
    SwingUtilities.invokeLater(() -> {
        JFrame frame = new JFrame("Minha App");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.add(new JLabel("Olá, mundo!", JLabel.CENTER));
        frame.pack();
        frame.setVisible(true);
    });
}
```

Pontos de atenção:
- As quatro exceções checked (`ClassNotFoundException`, `InstantiationException`, `IllegalAccessException`, `UnsupportedLookAndFeelException`) **devem** ser tratadas — não use `catch (Exception e)` apenas para silenciar.
- Se `getSystemLookAndFeelClassName()` falhar (L&F nativo ausente), o Swing usa Metal como fallback — isso não é erro fatal, mas vale logar.
- Chamar `pack()` e `setVisible` após trocar o L&F garante que o layout seja recalculado para as dimensões do novo L&F.

### Exemplo com FlatLaf (dependência externa)

O fluxo com FlatLaf é idêntico, mas requer a dependência adicionada ao build:

```java
// Requer: com.formdev:flatlaf no classpath (Maven/Gradle — NÃO bundled no JDK)
public static void main(String[] args) {
    FlatDarkLaf.setup(); // tema escuro; setar antes de qualquer Swing

    SwingUtilities.invokeLater(() -> {
        JFrame frame = new JFrame("App Escura");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(640, 480);
        frame.add(new JLabel("FlatDark theme (FlatLaf - FormDev, Apache 2.0)", JLabel.CENTER));
        frame.setVisible(true);
    });
}
```

## Armadilhas

### (1) Trocar L&F depois de exibir componentes sem chamar `updateComponentTreeUI`

**Problema:** chamar `UIManager.setLookAndFeel(...)` atualiza qual L&F será usado para *novos* componentes, mas os componentes já criados continuam com o `ComponentUI` antigo. O resultado é uma UI híbrida: botões criados antes da troca têm aparência Metal enquanto botões criados depois têm aparência Nimbus, produzindo inconsistência visual difícil de diagnosticar.

```java
// Hipotético — problema
UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
// frame já existe e está visível — componentes NÃO foram atualizados
```

**Fix:** após `setLookAndFeel`, chamar `SwingUtilities.updateComponentTreeUI(window)` para cada top-level container aberto. Se apenas uma janela existir:

```java
SwingUtilities.updateComponentTreeUI(frame);
frame.pack();
```

---

### (2) Assumir que o system L&F tem aparência/tamanhos consistentes entre SOs

**Problema:** `UIManager.getSystemLookAndFeelClassName()` retorna L&Fs radicalmente diferentes — Windows, macOS Aqua, GTK+ no Linux. Cada um usa fontes, métricas e dimensões distintas. Hard-codar dimensões como `setPreferredSize(new Dimension(200, 30))` produz UIs que parecem corretas no Windows e ficam cortadas ou com espaçamento errado no Linux/GTK ou macOS.

```java
// Hipotético — frágil
JButton btn = new JButton("Confirmar");
btn.setPreferredSize(new Dimension(100, 25)); // pode ser grande demais no macOS, pequeno no GTK
```

**Fix:** deixar o layout manager calcular as dimensões com base no `getPreferredSize` do componente (que considera a fonte e métricas do L&F ativo). Usar `pack()` no frame em vez de `setSize`. Testar em múltiplas plataformas antes de fixar dimensões:

```java
// Melhor: não forçar tamanho; confiar no layout manager
JButton btn = new JButton("Confirmar");
// sem setPreferredSize — tamanho calculado pelo L&F e layout manager
```

---

### (3) Usar cores hard-coded que quebram em dark mode ou L&F escuro

**Problema:** usar `setBackground(Color.WHITE)` ou `setForeground(Color.BLACK)` diretamente em componentes anula o sistema de temas. Quando o L&F é trocado para um tema escuro (FlatDark, Darcula), esses componentes mantêm suas cores fixas, resultando em texto branco sobre fundo branco (invisível) ou contrastes inaceitáveis.

```java
// Hipotético — problemático
JPanel panel = new JPanel();
panel.setBackground(Color.WHITE);   // fixo — quebra em dark mode
JLabel label = new JLabel("Texto");
label.setForeground(Color.BLACK);   // fixo — pode ficar invisível em temas escuros
```

**Fix:** usar as chaves do `UIManager` para obter as cores do tema ativo:

```java
JPanel panel = new JPanel();
panel.setBackground(UIManager.getColor("Panel.background"));  // respeita o L&F

JLabel label = new JLabel("Texto");
label.setForeground(UIManager.getColor("Label.foreground")); // respeita o L&F
```

Se precisar de uma cor customizada que funcione em ambos os modos, derivar a partir das cores do `UIManager` ou usar `UIManager.put` para registrar sua própria chave com variantes clara/escura.

## Em entrevista

### Frase pronta (inglês)

> "Swing's pluggable look-and-feel system decouples a component's visual rendering from its behavior by delegating all painting to a `ComponentUI` UI delegate that can be swapped at runtime via `UIManager.setLookAndFeel`. The JDK ships four bundled L&Fs: Metal (the default cross-platform), Nimbus (vector-based, HiDPI-friendly), the system/native wrapper, and the legacy Motif; after changing the L&F on an already-running UI you must call `SwingUtilities.updateComponentTreeUI` on every top-level container to repaint existing components with the new delegate, otherwise you end up with a mixed UI where old components keep their original appearance. For modern flat and dark-mode styling the community commonly uses FlatLaf, a third-party open-source library from FormDev (Apache 2.0, not part of the JDK), which is the visual foundation used by IntelliJ IDEA's own UI."

### Vocabulário

| Termo PT | Termo EN |
|----------|----------|
| aparência plugável | pluggable look-and-feel (L&F) |
| delegado de UI | UI delegate (`ComponentUI`) |
| gerenciador de aparência | `UIManager` |
| trocar aparência em tempo de execução | swap L&F at runtime |
| aparência nativa do sistema | system/native look-and-feel |
| atualizar árvore de componentes | `updateComponentTreeUI` |
| defaults do L&F | look-and-feel defaults (`UIDefaults`) |
| tema escuro | dark theme / dark mode |
| biblioteca terceira | third-party library |
| chave de UI | UI key (e.g. `"Panel.background"`) |

## Veja também

- [[03-Dominios/Java/Swing/01 - O modelo do Swing|O modelo do Swing]]
- [[03-Dominios/Java/Swing/10 - Custom painting e componentes customizados|Custom painting e componentes customizados]]
- [[03-Dominios/Java/Swing/index|Swing (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Dicionário de Java#look and feel (L&F)|look and feel]]
- [[03-Dominios/Java/Dicionário de Java#pluggable look-and-feel|pluggable look-and-feel]]
- [[03-Dominios/Java/Dicionário de Java#UIManager|UIManager]]
- [[03-Dominios/Java/Dicionário de Java#Nimbus|Nimbus]]
- [[03-Dominios/Java/Dicionário de Java#FlatLaf|FlatLaf]]

## Referências

- [How to Set the Look and Feel — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/uiswing/lookandfeel/index.html)
- [Modifying the Look and Feel — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/uiswing/lookandfeel/plaf.html)
- [UIManager — Javadoc Java 21 (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.desktop/javax/swing/UIManager.html)
- [FlatLaf — FormDev Software GmbH](https://www.formdev.com/flatlaf/) — projeto **third-party open-source** (Apache 2.0), não afiliado à Oracle; código em [github.com/JFormDesigner/FlatLaf](https://github.com/JFormDesigner/FlatLaf)
