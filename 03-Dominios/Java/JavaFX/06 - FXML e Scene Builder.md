---
title: "FXML e Scene Builder"
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
  - fxml
aliases:
  - "FXML"
  - "Scene Builder"
  - "FXMLLoader"
---

# FXML e Scene Builder

> [!abstract] TL;DR
> **FXML** é a view em XML declarativo do JavaFX: você descreve a hierarquia de nós no arquivo `.fxml` e o `FXMLLoader` instancia, injeta e liga tudo a um **controller** Java. A ligação ocorre por `fx:id` (no XML) + `@FXML` (no campo Java), e o ciclo de inicialização segue uma ordem garantida — construtor → injeção → `initialize()`. O **Scene Builder** (mantido pela Gluon) edita FXML visualmente com drag-and-drop. FXML versus código puro é um trade-off de separação/ferramental contra type-safety/refactoring — não há resposta dogmática.

## O que é

FXML é uma linguagem de marcação baseada em XML que permite construir gráficos de objetos JavaFX de forma declarativa. A hierarquia de elementos no arquivo `.fxml` corresponde diretamente à hierarquia de nós do scene graph: um elemento `<VBox>` aninhado dentro de `<BorderPane>` produz exatamente esse containment em tempo de execução.

O papel central do FXML é **separar a descrição da view da lógica de apresentação**: o arquivo `.fxml` descreve o que aparece; a classe controller em Java decide o que acontece. Essa divisão permite que designers editem o layout sem tocar em Java, e que programadores refinem comportamentos sem mexer no XML.

O **Scene Builder** é o editor visual oficial para arquivos FXML. É open source, gratuito e mantido pela Gluon (versão 26.0.0 em 2026). Ele oferece drag-and-drop de controls, inspeção de propriedades em painel lateral e geração automática do atributo `fx:id`. O arquivo `.fxml` editado pelo Scene Builder é o mesmo carregado pelo `FXMLLoader` — não há formato intermediário.

## Por que importa

O ciclo `FXMLLoader → controller → @FXML → initialize()` é cobrado em entrevistas de posições sênior porque revela se o candidato entende quando os campos injetados estão disponíveis — uma das fontes mais comuns de `NullPointerException` em JavaFX. Saber a ordem de inicialização e o papel de `setControllerFactory` como gancho de DI são diferenciadores claros.

FXML também é a linguagem de fato dos times maiores: frameworks como o MVVM do Gluon e ferramentas de análise de acessibilidade consomem FXML estruturado. Entender o formato é pré-requisito para ler código legado e contribuir em projetos open source JavaFX.

## Como funciona

### Anatomia de um FXML

Todo arquivo FXML começa com processing instructions e imports que declaram as classes disponíveis no documento:

```xml
<?xml version="1.0" encoding="UTF-8"?>

<?import javafx.scene.control.Button?>
<?import javafx.scene.control.Label?>
<?import javafx.scene.control.TextField?>
<?import javafx.scene.layout.VBox?>
```

O elemento raiz é o nó que será retornado pelo `FXMLLoader.load()`. Ele carrega o namespace JavaFX e, opcionalmente, declara o controller:

```xml
<VBox xmlns="http://javafx.com/javafx/21"
      xmlns:fx="http://javafx.com/fxml/1"
      fx:controller="com.example.OrderController"
      spacing="8">
```

Dentro do elemento raiz, atributos XML correspondem a propriedades JavaFX. O atributo especial **`fx:id`** nomeia o nó no namespace do documento e instrui o `FXMLLoader` a injetá-lo no campo de mesmo nome do controller:

```xml
    <Label text="Customer:" />
    <TextField fx:id="customerField" promptText="Enter customer name" />
    <Button text="Save" onAction="#handleSave" />
</VBox>
```

`onAction="#handleSave"` é uma **referência de método**: o `#` indica que `handleSave` é um método no controller, não um valor literal.

### O controller

O controller é uma classe Java comum — não precisa estender nada. O atributo `fx:controller` no FXML indica qual classe instanciar.

```java
public class OrderController {

    @FXML
    private TextField customerField;   // nome deve bater com fx:id="customerField"

    @FXML
    private void handleSave() {
        String customer = customerField.getText();
        // lógica de salvar pedido
    }

    @FXML
    private void initialize() {
        // executado APÓS a injeção de todos os @FXML
        customerField.setPromptText("Type customer name here");
    }
}
```

**A ordem de inicialização é garantida:**

1. **Construtor** da classe controller — `@FXML` ainda são `null` aqui.
2. **Injeção dos campos `@FXML`** — o loader percorre o document e preenche cada campo anotado pelo `fx:id` correspondente.
3. **Chamada a `initialize()`** — todos os `@FXML` já estão disponíveis; configure bindings, listeners e estado inicial aqui.

`initialize()` pode ser `private` — o `FXMLLoader` o acessa via reflexão. Campos `@FXML` também podem ser `private`, pelo mesmo motivo.

### FXMLLoader

O `FXMLLoader` é quem transforma o arquivo `.fxml` em um grafo de objetos vivos. Há duas formas de uso:

**Load estático** — conveniente, mas não permite acessar o controller depois:

```java
Parent root = FXMLLoader.load(
    getClass().getResource("/com/example/order-view.fxml")
);
```

**Load por instância** — permite `getController()` e `setControllerFactory()`:

```java
FXMLLoader loader = new FXMLLoader(
    getClass().getResource("/com/example/order-view.fxml")
);
Parent root = loader.load();
OrderController controller = loader.getController();
```

**`getController()`** só pode ser chamado *após* `load()` — antes disso retorna `null`.

**`setControllerFactory()`** é o gancho para injeção de dependências: em vez de deixar o loader instanciar o controller com `new`, você fornece um `Callback<Class<?>, Object>` que pode delegar para um container de DI (Guice, Spring, Weld etc.). Os detalhes de arquitetura estão em [[11 - Arquitetura — MVC, MVVM e injeção de dependência]].

```java
FXMLLoader loader = new FXMLLoader(
    getClass().getResource("/com/example/order-view.fxml")
);
loader.setControllerFactory(clazz -> injector.getInstance(clazz));
Parent root = loader.load();
```

### Resources e i18n

O `FXMLLoader` suporta internacionalização nativa via `ResourceBundle`. No FXML, qualquer atributo prefixado com `%` é substituído pelo valor da chave correspondente no bundle:

```xml
<Label text="%label.customer" />
<Button text="%button.save" onAction="#handleSave" />
```

No arquivo de recursos (`messages_pt.properties`):

```text
label.customer=Cliente:
button.save=Salvar
```

O bundle é passado no construtor do `FXMLLoader`:

```java
ResourceBundle bundle = ResourceBundle.getBundle(
    "com.example.messages", Locale.getDefault()
);
FXMLLoader loader = new FXMLLoader(
    getClass().getResource("/com/example/order-view.fxml"),
    bundle
);
```

### Scene Builder

O Scene Builder é um editor WYSIWYG para arquivos FXML. O fluxo de trabalho é bidirecional:

- **IDE → Scene Builder:** abra o `.fxml` no Scene Builder a partir da IDE (IntelliJ e VS Code têm integração direta).
- **Scene Builder → IDE:** salve no Scene Builder; o arquivo `.fxml` atualizado é recarregado pelo `FXMLLoader` no próximo build sem nenhum passo extra.

O Scene Builder atribui `fx:id` automaticamente ao arrastar controls, gera o bloco `fx:controller` e permite inspecionar o CSS de cada nó. É mantido pela Gluon (open source, gratuito; v26.0.0 em 2026), distribuído como instalador nativo para Windows, macOS e Linux.

### FXML vs código puro

Nem FXML nem código puro é a escolha correta para todos os casos. A decisão é um trade-off:

| Dimensão | FXML + Scene Builder | Código puro |
|---|---|---|
| Separação view/lógica | explícita (dois arquivos) | implícita (disciplina) |
| Tooling visual | Scene Builder, editores com preview | nenhum |
| Colaboração com designer | possível (sem Java) | improvável |
| Type-safety | nenhuma no XML | total em Java |
| Refactoring | renomear fx:id quebra silenciosamente | IDE propaga tudo |
| Magia/indireção | `@FXML`, reflexão, ordem de init | zero — tudo explícito |
| Geração dinâmica de UI | difícil (templates + factory) | natural (loops, condicionais) |

Use FXML quando a view é relativamente estável, o time tem designers ou a separação arquitetural é um requisito. Use código quando a UI é gerada dinamicamente, quando a base precisa de refactoring agressivo ou quando você quer eliminar uma dependência de runtime.

## Na prática

### O par completo: FXML + controller

**`order-view.fxml`:**

```xml
<?xml version="1.0" encoding="UTF-8"?>

<?import javafx.scene.control.Button?>
<?import javafx.scene.control.Label?>
<?import javafx.scene.control.TextField?>
<?import javafx.scene.layout.VBox?>

<VBox xmlns="http://javafx.com/javafx/21"
      xmlns:fx="http://javafx.com/fxml/1"
      fx:controller="com.example.OrderController"
      spacing="12"
      style="-fx-padding: 16;">

    <Label text="Customer:" />
    <TextField fx:id="customerField" promptText="Enter customer name"
               maxWidth="Infinity" />

    <Label text="Product:" />
    <TextField fx:id="productField" promptText="Enter product name"
               maxWidth="Infinity" />

    <Button text="Save Order" onAction="#handleSave" />
</VBox>
```

**`OrderController.java`:**

```java
package com.example;

import javafx.fxml.FXML;
import javafx.scene.control.TextField;

public class OrderController {

    @FXML
    private TextField customerField;

    @FXML
    private TextField productField;

    @FXML
    private void initialize() {
        // campos já injetados aqui — seguro para configurar
        customerField.textProperty().addListener((obs, old, val) ->
            System.out.println("Customer changed: " + val)
        );
    }

    @FXML
    private void handleSave() {
        String customer = customerField.getText().trim();
        String product  = productField.getText().trim();
        if (customer.isEmpty() || product.isEmpty()) {
            System.err.println("Fields must not be empty.");
            return;
        }
        System.out.printf("Saving order — customer=%s, product=%s%n",
            customer, product);
    }
}
```

### Carregando no `start()`

```java
@Override
public void start(Stage stage) throws Exception {
    FXMLLoader loader = new FXMLLoader(
        getClass().getResource("/com/example/order-view.fxml")
    );
    Parent root = loader.load();

    OrderController controller = loader.getController();
    // controller disponível para configuração adicional se necessário

    stage.setScene(new Scene(root, 400, 260));
    stage.setTitle("Order Entry");
    stage.show();
}
```

O caminho `/com/example/order-view.fxml` é **absoluto a partir do classpath** (barra inicial obrigatória). Ver Armadilha (3).

## Armadilhas

### (1) Acessar campo `@FXML` no construtor

**Problema:** o construtor é chamado *antes* da injeção dos campos. Qualquer acesso a um campo `@FXML` dentro do construtor resulta em `NullPointerException`.

```java
public class OrderController {

    @FXML
    private TextField customerField;

    public OrderController() {
        // PROBLEMA: customerField ainda é null aqui
        customerField.setText("Default");  // NullPointerException
    }
}
```

**Fix:** mova toda lógica de configuração pós-injeção para `initialize()`. O construtor serve apenas para injetar dependências externas (via `setControllerFactory`), não para acessar componentes da view.

```java
@FXML
private void initialize() {
    customerField.setText("Default");  // seguro — já foi injetado
}
```

---

### (2) `fx:id` diferente do nome do campo

**Problema:** o `FXMLLoader` emparelha `fx:id` com o nome do campo Java por string. Uma discrepância pode resultar em campo `null` silencioso (sem exceção) — ou, dependendo da versão do JavaFX e das configurações de acesso, em `LoadException`. O bug costuma aparecer só em runtime, quando o handler é invocado.

```xml
<!-- FXML: fx:id="customerField" -->
<TextField fx:id="customerField" />
```

```java
@FXML
private TextField custField;  // PROBLEMA: nome diferente — fica null
```

**Fix:** mantenha os nomes idênticos. Use o Scene Builder para gerar os `fx:id` — ele também pode gerar o esqueleto do controller com os nomes corretos.

```java
@FXML
private TextField customerField;  // bate com fx:id="customerField"
```

---

### (3) Path do `getResource` errado

**Problema:** `getResource` retorna `null` quando o path não é encontrado. O `FXMLLoader` recebe uma `URL null` e lança `NullPointerException` ou `LoadException` com mensagem pouco informativa.

```java
// PROBLEMA: path relativo depende da localização da classe chamadora
FXMLLoader loader = new FXMLLoader(
    getClass().getResource("order-view.fxml")  // pode não resolver
);
```

**Fix:** use sempre o path **absoluto** a partir da raiz do classpath, com barra inicial:

```java
FXMLLoader loader = new FXMLLoader(
    getClass().getResource("/com/example/order-view.fxml")
);
if (loader.getLocation() == null) {
    throw new IllegalStateException("FXML not found on classpath");
}
```

Confirme que o `.fxml` está dentro do source set de resources no build (Maven: `src/main/resources`).

---

### (4) Lógica de negócio crescendo no controller (god class)

**Problema:** controllers FXML tendem a acumular validação, acesso a dados, regras de negócio e manipulação de UI no mesmo lugar. O resultado é uma classe difícil de testar (depende de nós JavaFX) e difícil de reutilizar.

```java
@FXML
private void handleSave() {
    // PROBLEMA: validação + SQL + formatação + UI, tudo aqui
    if (customerField.getText().isEmpty()) { /* ... */ }
    String sql = "INSERT INTO orders ...";
    Connection conn = DriverManager.getConnection(...);
    // ... 80 linhas misturadas
}
```

**Fix:** o controller deve ser apenas o adaptador UI → ViewModel (ou Presenter). Regras de negócio ficam em serviços e o ViewModel expõe propriedades observáveis que o controller apenas vincula via binding. Veja [[11 - Arquitetura — MVC, MVVM e injeção de dependência]].

## Em entrevista

### Frase pronta (inglês)

> "In JavaFX, FXML lets you describe the view declaratively in XML while keeping all logic in a Java controller. The FXMLLoader wires them together: it instantiates the controller, injects fields annotated with `@FXML` that match `fx:id` attributes in the XML, and only then calls `initialize()` — so `initialize()` is the safe place to set up bindings or listeners, not the constructor. For dependency injection, `setControllerFactory` lets you hand controller instantiation to a DI container like Guice or Spring. Scene Builder, maintained by Gluon, gives you a visual drag-and-drop editor that writes the same FXML the loader reads, no extra format involved."

### Vocabulário

| Termo PT | Termo EN |
|---|---|
| arquivo de marcação | markup file / FXML file |
| injeção de campo | field injection |
| referência de método | method reference (handler) |
| fábrica de controller | controller factory |
| inicialização pós-injeção | post-injection initialization |
| chave de recurso (i18n) | resource key |
| instrução de processamento | processing instruction |
| editor visual | visual / WYSIWYG editor |

## Veja também

- [[01 - JavaFX — o que é e como chega ao projeto]]
- [[04 - Controls essenciais]]
- [[07 - Properties e binding]]
- [[11 - Arquitetura — MVC, MVVM e injeção de dependência]]
- [[03-Dominios/Java/JavaFX/index|JavaFX (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Dicionário de Java#FXML|FXML (Dicionário)]]
- [[03-Dominios/Java/Dicionário de Java#fx:id / @FXML|fx:id (Dicionário)]]
- [[03-Dominios/Java/Dicionário de Java#FXMLLoader|FXMLLoader (Dicionário)]]
- [[03-Dominios/Java/Dicionário de Java#Scene Builder|Scene Builder (Dicionário)]]

## Referências

- [Introduction to FXML — OpenJFX 21 Javadoc](https://openjfx.io/javadoc/21/javafx.fxml/javafx/fxml/doc-files/introduction_to_fxml.html) — fonte canônica: fx:controller, fx:id, @FXML, initialize(), FXMLLoader, setControllerFactory, %key + ResourceBundle
- [Scene Builder — Gluon](https://gluonhq.com/products/scene-builder/) — editor visual FXML mantido pela Gluon; open source; v26.0.0 (2026)
