---
title: "JavaFX"
created: 2026-04-01
updated: 2026-04-01
type: concept
status: seedling
tags:
  - java
  - frontend
  - entrevista
publish: false
---

# JavaFX

Framework Java para construção de aplicações desktop com interface gráfica rica.

## O que é

JavaFX é o toolkit oficial da Oracle para desenvolvimento de aplicações desktop em Java, substituindo o Swing. Usa FXML (XML declarativo) para layouts, CSS para estilização, e suporta gráficos 2D/3D, mídia e controles modernos de UI.

## Como funciona

### Arquitetura

```text
Stage (janela)
  └── Scene (cena)
       └── Scene Graph (árvore de nós)
            ├── Layout Panes (VBox, HBox, GridPane, BorderPane)
            ├── Controls (Button, TextField, TableView, ListView)
            └── Canvas / Charts / Media
```

- **Stage:** janela da aplicação
- **Scene:** container do conteúdo visual
- **Scene Graph:** hierarquia de nós (nodes) que compõem a UI
- **FXML:** definição declarativa de layouts, separando UI da lógica

### FXML + Controller

```xml
<!-- patient-view.fxml -->
<VBox xmlns:fx="http://javafx.com/fxml" fx:controller="com.app.PatientController">
    <TextField fx:id="nameField" promptText="Nome do paciente"/>
    <Button text="Salvar" onAction="#handleSave"/>
    <TableView fx:id="patientTable"/>
</VBox>
```

```java
public class PatientController {
    @FXML private TextField nameField;
    @FXML private TableView<Patient> patientTable;

    @FXML
    private void handleSave(ActionEvent event) {
        String name = nameField.getText();
        // lógica de salvamento
    }
}
```

### Binding e Properties

JavaFX usa properties observáveis para data binding reativo:

```java
StringProperty name = new SimpleStringProperty("Josenaldo");
IntegerProperty age = new SimpleIntegerProperty(40);

// Binding unidirecional
label.textProperty().bind(name);

// Binding bidirecional
textField.textProperty().bindBidirectional(name);

// Listener
name.addListener((obs, oldVal, newVal) -> {
    System.out.println("Nome mudou: " + newVal);
});
```

### Padrões comuns

- **MVC:** Model-View-Controller com FXML (View) + Controller + Model
- **MVVM:** Model-View-ViewModel usando bindings
- **CSS Styling:** `-fx-background-color`, `-fx-font-size` — similar ao CSS web mas com prefixo `-fx-`
- **Concorrência:** `Task<V>` e `Service<V>` para operações em background sem bloquear a UI thread

### Integração com Spring Boot

```java
@SpringBootApplication
public class App extends Application {
    private ConfigurableApplicationContext context;

    @Override
    public void init() {
        context = SpringApplication.run(App.class);
    }

    @Override
    public void start(Stage stage) {
        // Controllers injetados pelo Spring
        FXMLLoader loader = new FXMLLoader(getResource("main.fxml"));
        loader.setControllerFactory(context::getBean);
        stage.setScene(new Scene(loader.load()));
        stage.show();
    }
}
```

## Quando usar

- **Aplicações desktop Java:** ferramentas internas, dashboards, utilitários
- **Integração com sistemas Java existentes:** quando precisa de UI desktop para sistemas backend Java
- **Cross-platform desktop:** um único código roda em Windows, macOS, Linux
- **Prototipagem rápida:** SceneBuilder (editor visual) acelera a criação de telas

## Armadilhas comuns

- **Bloquear a UI thread:** operações longas (I/O, banco) devem rodar em `Task<V>` ou `Service<V>`, nunca na Application Thread
- **Atualizar UI fora da Application Thread:** usar `Platform.runLater()` para modificar a UI a partir de threads background
- **Não usar FXML:** misturar layout com lógica Java dificulta manutenção. FXML separa responsabilidades
- **Ignorar CSS:** estilizar via código Java em vez de CSS dificulta temas e manutenção

## Na prática (da minha experiência)

> Usei JavaFX em projetos que precisavam de interfaces desktop ricas integradas com sistemas Java existentes. A vantagem é manter toda a stack em Java — mesmos modelos de domínio, mesma lógica de negócio — com uma UI moderna. A integração com Spring Boot permite injeção de dependência nos controllers, mantendo a mesma arquitetura do backend.

## How to explain in English

"JavaFX is my choice for Java desktop applications. It provides a modern UI toolkit with FXML for declarative layouts, CSS for styling, and observable properties for reactive data binding — concepts that parallel what we see in web frameworks like React.

What I appreciate about JavaFX is the separation of concerns through FXML and Controllers, similar to how Spring MVC separates views from logic. When combined with Spring Boot, I get dependency injection in my UI controllers, which makes the code testable and well-structured.

The key challenge with JavaFX is threading — the UI must only be updated from the Application Thread, similar to how React only updates the DOM in the main thread. I use `Task<V>` for background operations and `Platform.runLater()` to push results back to the UI thread."

### Key vocabulary

- interface gráfica → graphical user interface (GUI)
- cena → scene: container visual
- nó → node: elemento na árvore de componentes
- vinculação de dados → data binding
- propriedade observável → observable property
- thread da aplicação → application thread / UI thread
- tarefa em segundo plano → background task

## Recursos

- [OpenJFX](https://openjfx.io/) — site oficial do JavaFX
- [JavaFX Documentation](https://openjfx.io/javadoc/21/) — API docs
- [SceneBuilder](https://gluonhq.com/products/scene-builder/) — editor visual de FXML

## Veja também

- [[Java Fundamentals]]
- [[Spring Boot]]
- [[Orientação a Objetos]]
