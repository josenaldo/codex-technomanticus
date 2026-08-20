---
title: "Scene graph — stage, scene e nodes"
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
  - scene-graph
aliases:
  - "Scene graph"
  - "Stage Scene Node"
---

# Scene graph — stage, scene e nodes

> [!abstract] TL;DR
> A UI do JavaFX é uma árvore de `Node`s — o **scene graph** — pendurada na cadeia `Stage → Scene → root Node`. O desenvolvedor **descreve** a cena (adiciona nós, muda propriedades) e o framework decide quando e o que re-renderizar: isso é **retained mode**, o oposto do modelo de painting manual do Swing onde `paintComponent` era invocado explicitamente pelo sistema. Entender essa distinção é o primeiro salto mental de quem chega do Swing para o JavaFX.

## O que é

O **scene graph** é a estrutura de dados central do JavaFX: uma árvore onde cada elemento visual é um `Node`. A cadeia de contenção é fixa:

```text
Stage  (a janela — uma Window concreta)
 └── Scene  (o conteúdo — carrega o root e define dimensões)
      └── root Node  (geralmente um Pane de layout)
           ├── Node filho
           │    └── Node neto
           └── Node filho
```

- **Stage** — representa a janela do sistema operacional. O `primaryStage` é fornecido pelo framework no método `start(Stage)`. Stages adicionais podem ser criados com `new Stage()` para janelas secundárias.
- **Scene** — carrega o root do scene graph e define largura e altura. Um `Stage` exibe uma `Scene` por vez; a `Scene` conhece o `Stage` que a contém via `getWindow()`.
- **Node** — classe abstrata raiz de todos os elementos visuais. Cada `Node` tem **exatamente um pai** (ou nenhum, se for o root ou ainda não estiver na cena).

## Por que importa

O scene graph é o **modelo mental central** do JavaFX — tudo passa por ele: layout, eventos, CSS, animações, hit testing. Quem não internaliza a estrutura de árvore tende a escrever código imperativo reposicionando nós na mão, quando o correto é escolher o `Pane` de layout adequado e deixar o framework calcular as posições.

O contraste retained vs. immediate mode é **pergunta clássica de migração Swing → JavaFX**. Em entrevista de sênior, a resposta esperada vai além de "em JavaFX você usa scene graph" — ela inclui o mecanismo (o framework rastreia estado dos nós e agenda redraw), as implicações (thread safety, propriedades observáveis) e o ponto de contato com Swing (onde `paintComponent` entrava no fluxo).

## Como funciona

### Stage → Scene → root (a espinha; múltiplos Stages)

O `Stage` é um `Window` concreto — a janela do SO. Após criar a `Scene` com um nó raiz e dimensões, associa-se ao `Stage` com `setScene()` e exibe com `show()`:

```java
Stage stage = new Stage();          // stage adicional; primaryStage vem do framework
stage.setTitle("Exemplo");
Scene scene = new Scene(root, 800, 600);
stage.setScene(scene);
stage.show();
```

Restrições do `primaryStage`: não aceita `showAndWait()` nem mudança de modalidade (lança `IllegalStateException`). Stages adicionais aceitam `showAndWait()`, útil para diálogos bloqueantes.

### Node, Parent, Group e Region (a taxonomia — quem tem filhos, quem faz layout)

| Tipo | Tem filhos? | Faz layout? | Exemplos |
|------|-------------|-------------|---------|
| `Node` (abstract) | não | não | base de tudo |
| `Parent` (abstract) | sim | não diretamente | base de branch nodes |
| `Group` | sim | **não** — posição absoluta | agrupamento lógico, transformações compartilhadas |
| `Region` | sim | **sim** | `Pane`, `HBox`, `VBox`, `BorderPane`, `GridPane` |
| `Control` (extends Region) | sim | sim | `Button`, `Label`, `TextField` |

`Group` é frequentemente confundido com um container de layout — não é. Ele posiciona filhos nas coordenadas que eles declaram (ou em `0,0` se nenhuma for dada). Para layout automático, usa-se sempre uma subclasse de `Region` — detalhes em [[03 - Layout panes]].

A lista de filhos é acessada via `getChildren()` em qualquer `Parent`:

```java
group.getChildren().addAll(label, button);
vbox.getChildren().add(label);
```

### Coordenadas e transformações (local vs parent vs scene; translate/scale/rotate; bounds)

Cada `Node` vive em três espaços de coordenadas simultâneos:

| Espaço | Referência | Quando usar |
|--------|-----------|------------|
| **local** | o próprio nó (`(0,0)` = canto superior esquerdo do nó) | geometria interna, hit testing |
| **parent** | o nó pai | posicionamento relativo ao container |
| **scene** | a `Scene` inteira | coordenadas globais, drag-and-drop cross-node |

Conversões: `localToParent()`, `localToScene()`, `parentToLocal()`, `sceneToLocal()`.

Transformações são aplicadas na ordem: `layoutX/layoutY` → `translateX/Y/Z` → `rotate` → `scaleX/Y/Z` → transforms customizados (lista invertida).

```java
node.setTranslateX(50);    // desloca 50px no eixo X
node.setRotate(45);         // rotaciona 45° em torno do centro
node.setScaleX(1.5);        // escala 1.5× horizontal
```

Três tipos de bounds cobrem casos distintos:

- **`boundsInLocal`** — geometria sem transformar; inclui stroke, clip, effect.
- **`boundsInParent`** — geometria após todas as transformações; representa a extensão visual no espaço do pai.
- **`layoutBounds`** — referência usada pelo sistema de layout; exclui effects e transforms para a maioria dos nós.

### Retained vs immediate mode (retained: você muda o node, o framework redesenha)

Em **immediate mode** (modelo do Swing), a aplicação é responsável por chamar o método de painting quando a UI precisa ser atualizada. O sistema pergunta "o que desenhar aqui?" e o código de `paintComponent` executa naquele instante — sem memória de frame anterior. O mecanismo completo está em [[03-Dominios/Tecnologia/Java/Swing/10 - Custom painting e componentes customizados|Custom painting (Swing)]]; aqui só importa o contraste.

Em **retained mode** (JavaFX), o framework mantém o scene graph em memória entre frames. Ao mudar uma propriedade de um `Node` (posição, cor, texto), o framework marca aquela subárvore como "suja" e decide por conta própria quando re-renderizar — geralmente no próximo pulse do animation timer (60 fps por padrão). A aplicação nunca chama `repaint()` nem `update()`.

```
Immediate mode (Swing):  app → "preciso redesenhar" → paintComponent() → pixels
Retained mode  (JavaFX): app → muda propriedade do Node → framework → pixels
```

Consequência prática: propriedades de `Node` são **observáveis** (`DoubleProperty`, `StringProperty`) — o sistema de binding e as animações funcionam porque o framework é notificado de qualquer mudança via invalidation.

## Na prática

Montar uma cena por código, aplicar transformações e consultar nós por CSS selector:

```java
import javafx.application.Application;
import javafx.scene.Node;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.layout.VBox;
import javafx.stage.Stage;

public class SceneGraphDemo extends Application {

    @Override
    public void start(Stage stage) {
        Label titulo = new Label("Scene Graph Demo");
        titulo.setId("titulo");            // id para CSS lookup

        Button btn = new Button("Clique");

        VBox root = new VBox(10, titulo, btn);   // spacing = 10px

        // Transformações no botão — sem repaint manual
        btn.setRotate(15);
        btn.setTranslateX(20);

        Scene scene = new Scene(root, 400, 300);
        stage.setTitle("Demo");
        stage.setScene(scene);
        stage.show();

        // Lookup por CSS selector — teaser de [[09 - CSS em JavaFX]]
        Node encontrado = scene.lookup("#titulo");
        System.out.println(encontrado);    // imprime o Label
    }

    public static void main(String[] args) { launch(); }
}
```

Pontos a observar:

- `VBox.getChildren()` recebe os nós via construtor conveniente — não é necessário chamar `add` separadamente.
- `setRotate(15)` e `setTranslateX(20)` produzem efeito visual imediatamente; o framework agenda o redraw. Nenhum `repaint()` foi invocado.
- `scene.lookup("#titulo")` busca qualquer nó com `id = "titulo"` — o mesmo mecanismo que seletores CSS usam. CSS completo: [[09 - CSS em JavaFX]].

## Armadilhas

### (1) Adicionar o mesmo Node em dois parents (IllegalArgumentException: duplicate children)

**O problema:** cada `Node` pode ter no máximo um pai. Tentar adicioná-lo a um segundo container sem removê-lo do primeiro lança exceção em runtime.

```java
Label label = new Label("Olá");
hbox.getChildren().add(label);
vbox.getChildren().add(label);   // IllegalArgumentException: duplicate children added
```

**Fix:** um node deve ser reparentado explicitamente — removê-lo do container atual antes de adicioná-lo ao novo. Reparentar é a operação correta; duplicar não é suportada por design (o scene graph é uma árvore, não um DAG).

```java
hbox.getChildren().remove(label);
vbox.getChildren().add(label);   // ok
```

---

### (2) Mutar a cena de outra thread (IllegalStateException)

**O problema:** assim que uma `Scene` é associada a um `Stage` visível, qualquer modificação nos seus `Node`s **deve ocorrer na JavaFX Application Thread**. Atualizações vindas de uma `CompletableFuture`, `Thread`, ou executor pool causam `IllegalStateException` em runtime (às vezes silenciosamente, com comportamento visual incorreto dependendo da JVM).

```java
// ERRADO — executando em pool thread
CompletableFuture.supplyAsync(() -> buscarDados())
    .thenAccept(dados -> label.setText(dados));  // IllegalStateException
```

**Fix:** envolver a atualização em `Platform.runLater()` para agendar na JavaFX Application Thread. O mecanismo completo — `Task`, `Service` e regras de threading — está em [[10 - A JavaFX Application Thread — Task, Service e Platform.runLater]].

```java
CompletableFuture.supplyAsync(() -> buscarDados())
    .thenAccept(dados -> Platform.runLater(() -> label.setText(dados)));  // ok
```

---

### (3) Usar Group esperando que ele posicione os filhos automaticamente

**O problema:** `Group` não implementa nenhum algoritmo de layout. Filhos sem posição explícita aparecem empilhados em `(0,0)`. Desenvolvedores que esperam comportamento de `HBox` ou `VBox` ficam com todos os nós sobrepostos.

```java
Group g = new Group();
g.getChildren().addAll(new Label("A"), new Label("B"));
// Ambos os Labels aparecem em (0,0) — sobrepostos
```

**Fix:** substituir por um `Pane` de layout adequado (`VBox`, `HBox`, `BorderPane`, etc.) — ver [[03 - Layout panes]]. Reservar `Group` para agrupamentos lógicos onde se quer aplicar uma transformação a um conjunto de nós sem layout automático.

## Em entrevista

### Frase pronta (inglês)

> "In JavaFX, the UI is modeled as a scene graph — a tree of Node objects hanging from a Stage, which is the OS window, through a Scene that holds the root node. The key mental shift from Swing is the rendering model: JavaFX uses retained mode, meaning you describe the scene by setting properties on nodes, and the framework decides when to repaint. In Swing you had immediate mode — `paintComponent` was called by the system and you issued drawing commands on a Graphics context on demand, with no persistent scene representation. The practical consequence in JavaFX is that node properties are observable; the binding system and animations work because the framework is notified of every change via property invalidation. A common thread-safety pitfall is that once a Scene is attached to a visible Stage, all node mutations must happen on the JavaFX Application Thread — violations throw `IllegalStateException` at runtime."

### Vocabulário

| Termo PT | Termo EN |
|----------|----------|
| grafo de cena | scene graph |
| nó | Node |
| nó raiz | root node |
| modo retido | retained mode |
| modo imediato | immediate mode |
| espaço de coordenadas local | local coordinate space |
| espaço de coordenadas da cena | scene coordinate space |
| limites no pai | bounds in parent |
| limites locais | bounds in local |
| thread da aplicação JavaFX | JavaFX Application Thread |
| propriedade observável | observable property |
| redesenho agendado | scheduled redraw / pulse |

## Veja também

- [[01 - JavaFX — o que é e como chega ao projeto]]
- [[03 - Layout panes]]
- [[09 - CSS em JavaFX]]
- [[10 - A JavaFX Application Thread — Task, Service e Platform.runLater]]
- [[12 - Custom controls, Canvas e charts]]
- [[03-Dominios/Tecnologia/Java/Swing/10 - Custom painting e componentes customizados|Custom painting (Swing)]]
- [[03-Dominios/Tecnologia/Java/JavaFX/index|JavaFX (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#scene graph|scene graph (Dicionário)]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#retained mode / immediate mode|retained mode (Dicionário)]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#Stage / Scene|Stage / Scene (Dicionário)]]

## Referências

- [JavaFX 21 Javadoc — Node](https://openjfx.io/javadoc/21/javafx.graphics/javafx/scene/Node.html) — hierarquia Node/Parent/Group/Region, sistemas de coordenadas (local/parent/scene), transformações (translate/scale/rotate), tipos de bounds (boundsInLocal, boundsInParent, layoutBounds), retained mode
- [JavaFX 21 Javadoc — Scene](https://openjfx.io/javadoc/21/javafx.graphics/javafx/scene/Scene.html) — construtores, relação com Stage e root Node, método lookup, regra de threading após attach
- [JavaFX 21 Javadoc — Stage](https://openjfx.io/javadoc/21/javafx.graphics/javafx/stage/Stage.html) — Stage como Window concreto, múltiplos Stages, restrições do primaryStage (sem showAndWait, sem modality change)
