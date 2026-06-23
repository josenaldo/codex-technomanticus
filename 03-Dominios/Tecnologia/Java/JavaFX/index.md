---
title: "JavaFX"
created: 2026-06-06
updated: 2026-06-06
type: moc
status: growing
publish: true
tags:
  - java
  - javafx
  - moc
aliases:
  - "Galho 6 - JavaFX"
  - "OpenJFX (galho)"
---

# JavaFX

> [!abstract] TL;DR
> Galho 6 da trilha Java Senior; cobre scene graph, FXML/Scene Builder, properties e binding, CSS, TableView, Task/Service e threading, MVVM, custom controls/Canvas, empacotamento (jlink/jpackage) e estado do projeto (OpenJFX/Gluon); 14 notas em 3 fases.

## Sobre este galho

Este galho cobre o **toolkit de UI desktop moderno do ecossistema Java de ponta a ponta**: o scene graph como modelo mental central (Stage → Scene → Nodes), layout com panes, controls essenciais e propagação de eventos, declaração de views com FXML e Scene Builder, o modelo reativo de properties e binding, componentes de dados com TableView e ObservableList, estilização com o dialeto CSS do JavaFX, threading com Task/Service e Platform.runLater, arquitetura com MVVM e injeção de dependência, custom controls e Canvas, e o ciclo completo de empacotamento com jlink e jpackage até o instalador nativo.

**Audiência primária:** dev senior em preparação para entrevista internacional — cada nota expõe o "porquê" das decisões e as perguntas mais cobradas, com vocabulário preciso em inglês. O mesmo dev que precisa construir ou manter uma aplicação desktop Java e quer dominar não apenas a API, mas os trade-offs arquiteturais (MVC vs. MVVM, compor vs. estender controls, Canvas vs. scene graph). **Audiência secundária:** o dev que conhece Swing e está avaliando ou migrando para JavaFX, ou que precisa decidir entre desktop e web com argumentos sólidos.

Este galho é um **refator com poda integral** do tronco [[JavaFX]] (`Frontend/JavaFX.md`): a seção JavaFX foi extraída, aprofundada e reorganizada em notas atômicas por fase. Fecha o **par desktop** da trilha Java junto com [[03-Dominios/Tecnologia/Java/Swing/index|Swing (Galho 5)]].

**Fronteiras importantes:** a teoria geral de UI thread — single-thread model, Event Dispatch Thread, deadlock AWT — está no Galho 5 ([[03-Dominios/Tecnologia/Java/Swing/05 - A Event Dispatch Thread|EDT]]); o sistema de módulos JPMS como conceito (requires/exports, classpath vs. module path) está no Galho 3 ([[03-Dominios/Tecnologia/Java/JVM/08 - JPMS — o sistema de módulos|JPMS]]); concorrência de baixo nível (locks, executors, Java Memory Model) está no Galho 4.

## Iniciado

1. [[01 - JavaFX — o que é e como chega ao projeto]] — o que é JavaFX, a linha do tempo honesta do desacoplamento (JDK 8 bundled → Java 11 OpenJFX externo), como incluir via Maven/Gradle e por que Swing não foi substituído.
2. [[02 - Scene graph — stage, scene e nodes]] — a árvore central Stage → Scene → root Node, retained mode como contraponto ao painting manual do Swing, e por que internalizar a hierarquia resolve a maioria dos problemas de layout e evento.
3. [[03 - Layout panes]] — pane como política de layout embutida (sem LayoutManager plugável), o catálogo de panes essenciais (HBox, VBox, BorderPane, GridPane, StackPane, AnchorPane) e quando usar cada um.
4. [[04 - Controls essenciais]] — os widgets de `javafx.scene.control` (Button, TextField, ComboBox, ListView, TableView, Dialog), a hierarquia sobre `Region` e `Control`, e como toda propriedade exposta é bindável via `xxxProperty()`.
5. [[05 - Eventos — capturing, bubbling e handlers]] — as duas fases de propagação no scene graph (capturing Stage → target e bubbling target → Stage), `addEventFilter` vs. `addEventHandler`, `consume()` e o contraste com o modelo de eventos do Swing.

## Adepto

6. [[06 - FXML e Scene Builder]] — FXML como view declarativa em XML, FXMLLoader como montador de objetos, o ciclo de inicialização garantido (construtor → injeção de `@FXML` → `initialize()`), e `setControllerFactory` como gancho de DI; Scene Builder como editor visual gratuito mantido pela Gluon.
7. [[07 - Properties e binding]] — property como valor observável e bindável, `bind` unidirecional (alvo vira read-only) vs. `bindBidirectional`, avaliação lazy (invalidation) vs. eager (change listener), e por que properties são o diferencial reativo do JavaFX sobre o Swing.
8. [[08 - TableView, cell factories e dados observáveis]] — `TableView<S>` sobre `ObservableList<S>`, o par `cellValueFactory`/`cellFactory`, reuso de células durante o scroll, e o pipeline `FilteredList → SortedList` para filtro e ordenação reativos sem tocar nos dados originais.
9. [[09 - CSS em JavaFX]] — o dialeto CSS 2.1 do JavaFX (propriedades `-fx-`, não CSS web), o tema padrão Modena como user-agent stylesheet, a ordem de precedência da cascata (`setStyle` inline > Parent > Scene > Modena) e o que CSS JavaFX *não* faz (layout).
10. [[10 - A JavaFX Application Thread — Task, Service e Platform.runLater]] — regra single-thread do scene graph (tudo que toca a cena precisa da FX thread), `Task<V>` com `call()` em background e properties bindáveis de progresso, `Platform.runLater` como válvula de retorno, e `Service`/`ScheduledService` como `Task` reusável.

## Magus

11. [[11 - Arquitetura — MVC, MVVM e injeção de dependência]] — o MVC natural do FXML que vira god class sem disciplina, MVVM com ViewModel de properties testável sem toolkit, a seta de dependência View → ViewModel → Model que nunca sobe, e `setControllerFactory` como ponto de encaixe de qualquer estratégia de DI.
12. [[12 - Custom controls, Canvas e charts]] — os três caminhos para UI fora do catálogo (COMPOR em Region, ESTENDER com Control+Skin, DESENHAR com Canvas em immediate mode), quando cada um se justifica, e os charts nativos (LineChart, BarChart, PieChart) para visualização de dados sem nenhum deles.
13. [[13 - Empacotamento — módulos, jlink e jpackage]] — JavaFX como conjunto de módulos JPMS externos ao JDK, `jlink` para montar um runtime image enxuto e `jpackage` (JEP 392) para gerar instalador nativo por plataforma (deb/rpm, msi/exe, dmg/pkg) com o runtime embarcado.
14. [[14 - JavaFX hoje — estado do projeto e Swing vs JavaFX]] — capstone do galho: estado real do OpenJFX (repositório ativo, releases semestrais alinhadas ao JDK, stewardship da Gluon), e o framework de decisão Swing vs. JavaFX vs. web por critérios de contexto — não de torcida.

## Rotas alternativas

### Completa

01 → 02 → 03 → 04 → 05 → 06 → 07 → 08 → 09 → 10 → 11 → 12 → 13 → 14. Percurso linear do básico ao avançado — recomendado para quem não tem experiência anterior com JavaFX.

### Entrevista internacional

01 → 02 → 07 → 10 → 14. Setup e desacoplamento do JDK, scene graph como modelo mental, properties e binding como diferencial reativo, threading com Task/Service, e o framework de decisão Swing vs. JavaFX — o que mais cai em entrevistas de nível senior.

### Vindo do Swing

01 → 02 → 05 → 10 → 14. Os quatro contrastes que mais desorientam quem chega do Galho 5: setup externo vs. core SE, retained mode vs. painting manual, fases de evento vs. listener direto, FX thread vs. EDT, e a decisão de quando migrar ou coexistir.

### App de dados

04 → 06 → 07 → 08 → 09. Controls essenciais como ponto de entrada, FXML para estruturar a view, properties e binding para reatividade, TableView com cell factories e dados observáveis, e CSS para tematizar a interface — a trilha de quem constrói uma tela de gestão de dados.

### Do código ao instalador

06 → 11 → 13. FXML como base de uma view bem estruturada, MVVM para separar ViewModel testável da View, e jlink/jpackage para empacotar e distribuir sem pedir "instale o Java" — o caminho mínimo de quem quer entregar uma app desktop real.

## Todas as notas

```dataview
TABLE fase, status, updated
FROM "03-Dominios/Tecnologia/Java/JavaFX"
WHERE type = "concept"
SORT file.name ASC
```

## Veja também

- [[03-Dominios/Tecnologia/Java/index|Java (MOC central)]]
- [[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/index|Linguagem e sintaxe moderna (Galho 1)]]
- [[03-Dominios/Tecnologia/Java/JVM/index|JVM por dentro (Galho 3)]]
- [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Concorrência e paralelismo (Galho 4)]]
- [[03-Dominios/Tecnologia/Java/Swing/index|Swing (Galho 5)]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java|Dicionário de Java]]
- [[JavaFX]] (tronco em transição)
