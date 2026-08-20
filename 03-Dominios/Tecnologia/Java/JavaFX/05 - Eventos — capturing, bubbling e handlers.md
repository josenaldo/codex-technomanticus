---
title: "Eventos — capturing, bubbling e handlers"
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
  - eventos
aliases:
  - "Eventos JavaFX"
  - "EventFilter EventHandler"
  - "Bubbling"
---

# Eventos — capturing, bubbling e handlers

> [!abstract] TL;DR
> Eventos no JavaFX percorrem o **scene graph** em duas fases distintas: **capturing** (Stage → target, descendo a árvore) e **bubbling** (target → Stage, subindo a árvore). `addEventFilter` registra um listener na fase de capturing; `addEventHandler` registra na fase de bubbling. `consume()` interrompe a propagação onde for chamado. Isso é diferente do modelo do Swing — descrito em [[03-Dominios/Tecnologia/Java/Swing/04 - O modelo de eventos|O modelo de eventos (Swing)]] — onde listeners são registrados diretamente no componente sem fases explícitas de propagação.

## O que é

O sistema de eventos do JavaFX é construído sobre o **scene graph** descrito em [[02 - Scene graph — stage, scene e nodes]]. Cada `Node` (e também `Scene` e `Stage`) implementa `EventTarget`, o que significa que pode participar da **event dispatch chain** — a rota completa que um evento percorre desde a raiz da árvore até o nó alvo e de volta.

Quando o usuário clica em um `Button` dentro de um `VBox` dentro de uma `Scene` dentro de um `Stage`, o JavaFX não entrega o evento diretamente ao botão. Ele constrói a rota completa, percorre essa rota de cima a baixo (capturing), passa pelo target, e percorre de baixo a cima (bubbling). Filtros e handlers registrados em qualquer ponto da rota podem processar ou suprimir o evento.

## Por que importa

Entender as fases de propagação é indispensável para implementar comportamentos que atuam em **múltiplos nós ao mesmo tempo**:

- **Atalhos globais** — interceptar `KeyEvent` num container pai antes que o foco chegue ao campo de texto filho.
- **Validação centralizada** — um `VBox` de formulário pode filtrar eventos antes de deixá-los alcançar os `TextField`s individuais.
- **Modal behavior** — bloquear todos os eventos de mouse numa região enquanto um painel de loading está visível.
- **Logging e diagnóstico** — registrar eventos em qualquer ponto da árvore sem modificar os nós filhos.

Para quem vem do Swing, a pergunta "como intercepto um evento antes que o componente o processe?" é frequente em migrações — e a resposta exige conhecer capturing.

## Como funciona

### A dispatch chain (rota da Stage ao target e de volta)

Quando um evento é disparado, o JavaFX executa os seguintes passos:

1. **Determina o target** — o nó mais específico que recebeu a interação (ex.: o `Button` que foi clicado, detectado via hit testing).
2. **Constrói a dispatch chain** — a lista ordenada de todos os `EventTarget`s entre a raiz e o target: `Stage → Scene → root Node → ... → target`.
3. **Fase de capturing (descida)** — percorre a chain do topo ao target, executando os **EventFilters** registrados em cada nó para aquele tipo de evento.
4. **Fase de target** — os handlers e filtros do próprio target são executados.
5. **Fase de bubbling (subida)** — percorre a chain do target até o topo, executando os **EventHandlers** registrados em cada nó.

```text
          capturing (descida)       bubbling (subida)
                  ↓                        ↑
  Stage ──────── filter? ────────── handler?
    │                                      │
  Scene ──────── filter? ────────── handler?
    │                                      │
  VBox  ──────── filter? ────────── handler?
    │                                      │
  Button ─────── filter? + handler? ───────┘
                   (target)
```

### EventFilter (capturing) vs EventHandler (bubbling) — addEventFilter / addEventHandler

```java
// EventFilter: executa na DESCIDA (antes de chegar ao target)
vbox.addEventFilter(MouseEvent.MOUSE_CLICKED, event -> {
    System.out.println("VBox filter — fase capturing");
});

// EventHandler: executa na SUBIDA (após o target processar)
vbox.addEventHandler(MouseEvent.MOUSE_CLICKED, event -> {
    System.out.println("VBox handler — fase bubbling");
});

// Ordem de execução ao clicar no Button dentro do VBox:
// 1. VBox filter  (capturing — desce)
// 2. Button filter (capturing — no target)
// 3. Button handler (bubbling — no target)
// 4. VBox handler (bubbling — sobe)
```

Para remover, use `removeEventFilter` e `removeEventHandler` com a mesma referência ao handler — por isso, ao registrar lambdas que precisam ser removidas, armazene a referência em variável.

```java
EventHandler<MouseEvent> bloqueador = Event::consume;
vbox.addEventFilter(MouseEvent.MOUSE_CLICKED, bloqueador);
// ... depois:
vbox.removeEventFilter(MouseEvent.MOUSE_CLICKED, bloqueador);
```

### consume() — parar a propagação (e onde ela para)

`consume()` marca o evento como consumido e interrompe a propagação **a partir do ponto onde é chamado**. O evento não é entregue a nenhum nó seguinte na chain.

- Chamado num **filter** (capturing): o evento não desce mais — nenhum filter ou handler abaixo na árvore recebe o evento.
- Chamado num **handler** (bubbling): o evento não sobe mais — nenhum handler acima na árvore recebe o evento.

```java
// Bloquear o evento inteiramente no VBox antes de chegar ao Button:
vbox.addEventFilter(MouseEvent.MOUSE_CLICKED, event -> {
    System.out.println("Bloqueado no VBox — Button não saberá do clique");
    event.consume();
});
```

### Convenience methods — setOnAction / setOnMouseClicked / setOnKeyPressed

O JavaFX oferece métodos `setOn*` em `Node`, `Scene` e `Stage` como atalhos para registrar **um único EventHandler** na fase de bubbling. Internamente são propriedades `ObjectProperty<EventHandler<T>>`:

```java
Button btn = new Button("Salvar");

// Equivalente a btn.addEventHandler(ActionEvent.ACTION, e -> ...)
// Lambda — ver [[03-Dominios/Tecnologia/Java/Collections e Streams/04 - Lambdas e interfaces funcionais|Lambdas e interfaces funcionais]]
btn.setOnAction(e -> System.out.println("Botão clicado"));

// Equivalente a node.addEventHandler(MouseEvent.MOUSE_CLICKED, e -> ...)
btn.setOnMouseClicked(e -> System.out.println("Mouse clicado em " + e.getX()));

// Equivalente a node.addEventHandler(KeyEvent.KEY_PRESSED, e -> ...)
scene.setOnKeyPressed(e -> System.out.println("Tecla: " + e.getCode()));
```

Limitação importante: só pode haver **um** handler registrado via `setOn*` por nó. Chamar `setOnAction` duas vezes substitui o handler anterior. Para múltiplos listeners no mesmo evento, use `addEventHandler`.

### EventType e a hierarquia (Event.ANY → MouseEvent.ANY → MOUSE_CLICKED)

Os tipos de evento formam uma hierarquia com `Event.ANY` (ROOT) no topo. Registrar um handler num tipo mais genérico o faz receber todos os eventos dos subtipos:

```text
Event.ANY
├── InputEvent.ANY
│   ├── MouseEvent.ANY
│   │   ├── MouseEvent.MOUSE_CLICKED
│   │   ├── MouseEvent.MOUSE_PRESSED
│   │   ├── MouseEvent.MOUSE_RELEASED
│   │   └── MouseEvent.MOUSE_MOVED  (+ outros)
│   └── KeyEvent.ANY
│       ├── KeyEvent.KEY_PRESSED
│       ├── KeyEvent.KEY_RELEASED
│       └── KeyEvent.KEY_TYPED
└── ActionEvent.ANY
    └── ActionEvent.ACTION
```

```java
// Handler registrado em MouseEvent.ANY recebe MOUSE_CLICKED, MOUSE_PRESSED, etc.
node.addEventHandler(MouseEvent.ANY, e -> System.out.println("Qualquer mouse: " + e.getEventType()));

// Handler registrado em MOUSE_CLICKED recebe APENAS cliques
node.addEventHandler(MouseEvent.MOUSE_CLICKED, e -> System.out.println("Apenas clique"));
```

Registrar no tipo mais específico possível evita processamento desnecessário.

## Na prática

**Caso 1: Button com setOnAction (caso mais comum)**

```java
Button salvar = new Button("Salvar");
// setOnAction é convenience method para ActionEvent — handler de bubbling
salvar.setOnAction(e -> System.out.println("Salvando..."));
```

**Caso 2: EventFilter num VBox interceptando MOUSE_CLICKED antes dos filhos**

```java
VBox painel = new VBox(10);
Button btn1 = new Button("A");
Button btn2 = new Button("B");
painel.getChildren().addAll(btn1, btn2);

// O VBox intercepta TODOS os cliques de mouse antes de qualquer filho
painel.addEventFilter(MouseEvent.MOUSE_CLICKED, event -> {
    System.out.println("Clique interceptado pelo VBox em: "
        + event.getTarget().getClass().getSimpleName());
    // Sem consume() — o evento continua para o filho que foi clicado
});
```

**Caso 3: consume() bloqueando teclas inválidas num TextField (somente dígitos)**

```java
TextField campoNumerico = new TextField();

// Filter na fase de capturing — bloqueia a tecla antes de chegar ao TextField
campoNumerico.addEventFilter(KeyEvent.KEY_TYPED, event -> {
    String caractere = event.getCharacter();
    if (!caractere.matches("[0-9]")) {
        event.consume(); // Tecla não-dígito: descartada, não aparece no campo
    }
});
```

## Armadilhas

### (1) Esperar que o handler no pai execute antes do filho (pai executa depois no bubbling)

**O problema:** Ao registrar `addEventHandler` num container pai, o handler executa na fase de bubbling — **depois** que o filho já processou o evento. Quem vem do Swing (onde a ordem de notificação é linear e previsível) costuma se surpreender.

```java
// INTENÇÃO: VBox valida antes do Button processar
// PROBLEMA: addEventHandler no VBox executa DEPOIS do Button
vbox.addEventHandler(MouseEvent.MOUSE_CLICKED, e -> {
    System.out.println("Pai — mas executa DEPOIS do filho no bubbling");
});
btn.addEventHandler(MouseEvent.MOUSE_CLICKED, e -> {
    System.out.println("Filho — executa ANTES do pai");
});
// Saída: "Filho..." → "Pai..."
```

**Fix:** trocar `addEventHandler` por `addEventFilter` no pai. Filters executam na fase de capturing — antes de qualquer filho.

```java
vbox.addEventFilter(MouseEvent.MOUSE_CLICKED, e -> {
    System.out.println("Pai — agora executa ANTES do filho (capturing)");
});
```

---

### (2) consume() esquecido — evento "vaza" e dispara dois comportamentos

**O problema:** Ao processar um evento em um handler, esquecer `consume()` permite que o evento continue propagando. O resultado é que dois (ou mais) handlers distintos reagem ao mesmo evento, causando efeito duplicado.

```java
// Dois handlers para o mesmo botão — sem consume(), ambos executam
btn.addEventHandler(MouseEvent.MOUSE_CLICKED, e -> {
    abrirDialog();          // intenção: tratar aqui e parar
    // esqueceu e.consume()
});
scene.addEventHandler(MouseEvent.MOUSE_CLICKED, e -> {
    logClique();            // executa também, mesmo sem intenção
});
```

**Fix:** chamar `event.consume()` no handler que tratou o evento de forma definitiva.

---

### (3) Lógica pesada ou bloqueante dentro do handler (congela a UI)

**O problema:** Todos os EventHandlers e EventFilters executam na **JavaFX Application Thread** — a mesma thread que renderiza a UI. Operações de I/O, consultas a banco ou qualquer código que bloqueie essa thread congelam a interface durante a execução.

```java
btn.setOnAction(e -> {
    List<Dado> dados = bancoDeDados.buscarTodos(); // BLOQUEIA a UI thread
    tabela.setItems(FXCollections.observableArrayList(dados));
});
```

**Fix:** mover o trabalho pesado para uma thread de background e retornar à Application Thread apenas para atualizar os nós. O mecanismo completo — `Task`, `Service` e `Platform.runLater` — está em [[10 - A JavaFX Application Thread — Task, Service e Platform.runLater]].

## Em entrevista

### Frase pronta (inglês)

> "JavaFX uses a two-phase event dispatch model built on top of the scene graph. When an event is triggered, the framework builds the dispatch chain from the Stage down to the target node. In the first phase — capturing — the event travels down the tree, invoking any EventFilters registered along the way via `addEventFilter`. After reaching the target, the event bubbles back up, invoking EventHandlers registered via `addEventHandler`. Calling `consume()` at any point stops further propagation immediately. The `setOn*` convenience methods — like `setOnAction` or `setOnMouseClicked` — are shorthand for registering a single bubbling-phase handler. This is fundamentally different from Swing, where listeners are registered directly on the component with no explicit propagation phases; to intercept an event before a child processes it in JavaFX, you use a filter on the parent, not a handler."

### Vocabulário

| Termo PT | Termo EN |
|----------|----------|
| cadeia de despacho | event dispatch chain |
| fase de captura | capturing phase |
| fase de borbulhamento | bubbling phase |
| filtro de evento | EventFilter |
| manipulador de evento | EventHandler |
| consumir evento | consume an event |
| tipo de evento | EventType |
| métodos de conveniência | convenience methods |
| nó alvo | event target / target node |
| propagação | event propagation |

## Veja também

- [[02 - Scene graph — stage, scene e nodes]]
- [[04 - Controls essenciais]]
- [[10 - A JavaFX Application Thread — Task, Service e Platform.runLater]]
- [[03-Dominios/Tecnologia/Java/Swing/04 - O modelo de eventos|O modelo de eventos (Swing)]]
- [[03-Dominios/Tecnologia/Java/Collections e Streams/04 - Lambdas e interfaces funcionais|Lambdas e interfaces funcionais]]
- [[03-Dominios/Tecnologia/Java/JavaFX/index|JavaFX (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#event dispatch chain (capturing / bubbling)|event dispatch chain (Dicionário)]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#EventFilter / EventHandler|EventFilter / EventHandler (Dicionário)]]

## Referências

- [JavaFX 21 Javadoc — Event](https://openjfx.io/javadoc/21/javafx.base/javafx/event/Event.html) — classe base de todos os eventos; `consume()`, hierarquia via `EventType`, `Event.ANY` como ROOT
- [JavaFX 21 Javadoc — EventTarget](https://openjfx.io/javadoc/21/javafx.base/javafx/event/EventTarget.html) — `buildEventDispatchChain()`, fases de capturing e bubbling, papéis de EventFilter e EventHandler
- [JavaFX 21 Javadoc — EventType](https://openjfx.io/javadoc/21/javafx.base/javafx/event/EventType.html) — hierarquia de tipos (`ROOT == Event.ANY`), herança de subtipos, registro em supertipo para receber subtipos
- [JavaFX 21 Javadoc — Node](https://openjfx.io/javadoc/21/javafx.graphics/javafx/scene/Node.html) — `addEventFilter`, `addEventHandler`, `removeEventFilter`, `removeEventHandler`, `setOnMouseClicked`, `setOnKeyPressed` e demais convenience methods
