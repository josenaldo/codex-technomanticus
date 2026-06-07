---
title: "Arquitetura — MVC, MVVM e injeção de dependência"
created: 2026-06-06
updated: 2026-06-06
type: concept
progress: backlog
status: seedling
publish: true
fase: magus
tags:
  - java
  - javafx
  - magus
  - mvvm
  - arquitetura
aliases:
  - "MVVM JavaFX"
  - "Arquitetura JavaFX"
  - "controllerFactory"
---

# Arquitetura — MVC, MVVM e injeção de dependência

> [!abstract] TL;DR
> O controller FXML é MVC na sua forma mais simples — view declarativa em XML, controller como cola entre UI e modelo —, mas acumula estado, lógica e formatação rápido e vira uma **god class** impossível de testar sem subir o toolkit. O caso arquitetural forte do JavaFX é **MVVM**: o **ViewModel** expõe estado como properties e comandos observáveis; a View (controller) apenas binda, sem guardar lógica; o fluxo de dados segue **View → ViewModel → Model, nunca o contrário**. O ViewModel não conhece nenhum nó da UI e por isso é testável com JUnit puro, sem FX thread. O gancho que conecta DI ao ciclo de vida do loader é `FXMLLoader.setControllerFactory(Callback<Class<?>, Object>)` — é ali que um container se pluga ou que uma factory manual entrega instâncias pré-montadas.

## O que é

Três arranjos arquiteturais dominam aplicações JavaFX, e entendê-los em conjunto é o que distingue um desenvolvedor pleno de um sênior:

**MVC à la FXML** — o modelo mais natural quando se parte do zero com FXML. A view é o arquivo `.fxml` (hierarquia de nós), o controller é a classe Java anotada com `@FXML`, e o model é o domínio de negócio puro. O FXMLLoader faz a costura: instancia o controller, injeta os campos anotados e chama `initialize()`. É simples e funciona — até o controller começar a acumular validação, acesso a serviços, formatação de exibição e estado de sessão. Esse acúmulo é inevitável sem disciplina arquitetural explícita.

**MVVM com properties** — o arranjo que explora a proposta central do JavaFX. O **ViewModel** é uma classe pura Java que expõe o estado da tela como properties observáveis (`StringProperty`, `BooleanProperty`, `ReadOnlyDoubleProperty`…) e operações como métodos simples. A View (o controller fino) recebe o ViewModel, binda cada control a uma property correspondente e delega ações ao ViewModel — sem guardar estado próprio, sem chamar serviços diretamente. O Model (repositórios, serviços de domínio) é chamado pelo ViewModel, não pela View. A seta de dependência nunca sobe: Model não conhece ViewModel, ViewModel não conhece View.

**Injeção de dependência nos controllers** — FXML por padrão instancia o controller com `new` via reflexão. `setControllerFactory` substitui essa instanciação: você fornece um `Callback<Class<?>, Object>` e o loader o invoca para cada classe de controller encontrada no documento, antes de injetar os campos `@FXML`. É o ponto de encaixe de qualquer estratégia de DI — de uma factory manual com mapa de suppliers até um container completo (Guice, Weld, ou frameworks de terceiros como mvvmFX; Spring/CDI ficam para o Galho 8, planejado).

## Por que importa

**Testabilidade sem toolkit** é o argumento de nível sênior. Um controller que mistura `customerField.getText()` com lógica de negócio só pode ser testado subindo o JavaFX Application Thread — testes lentos, frágeis, dependentes de ambiente gráfico. Um ViewModel que expõe `StringProperty customer` é testável com JUnit puro: `new OrderViewModel(fakeRepo)`, `setCustomer("Alice")`, `assertEquals(...)`. Nenhum toolkit envolvido.

**Binding nativo como diferencial** — properties e binding são primitivos da plataforma. Isso habilita MVVM sem código de cola imperativo: o ViewModel declara o estado, a View declara as ligações, a propagação é automática. Em Swing, isso exige plumbing manual a cada ponto — e é a resposta técnica para "por que JavaFX em vez de Swing numa app nova?".

**Entrevista de arquitetura** — "como você organizaria uma tela complexa em JavaFX?" separa quem usou JavaFX de quem o entende. A resposta esperada cobre: controller fino como adaptador, ViewModel com properties testáveis, serviços separados via DI, `setControllerFactory` como ponto de extensão.

## Como funciona

### MVC à la FXML (e onde rateia)

O ciclo canônico é o descrito em [[06 - FXML e Scene Builder]]: FXMLLoader instancia o controller declarado em `fx:controller`, injeta campos `@FXML` e chama `initialize()`. O controller é o **glue layer** — recebe eventos da View e atualiza o Model.

O ponto de ruptura é a concentração: como o controller tem referência direta a todos os nós e é o único receptor de eventos, a gravidade o leva a acumular estado de sessão, validação, lógica de negócio, acesso a infraestrutura e formatação — numa classe de 300–500 linhas que só pode ser exercitada abrindo a tela.

### MVVM com properties

O MVVM reorganiza as responsabilidades com uma regra única: **o ViewModel não pode referenciar nenhum nó da UI**.

O **ViewModel** é uma classe Java pura. Ele expõe:

- **Properties observáveis** para cada dado que a View precisa exibir ou editar.
- **ReadOnlyProperty** para dados derivados ou que a View não deve alterar diretamente (totais calculados, flags de estado).
- **Métodos de comando** para ações (`save()`, `cancel()`, `loadData()`).

O **controller** (a View no vocabulário MVVM) recebe o ViewModel — via construtor ou DI — e no `initialize()` apenas binda cada control a uma property correspondente. Não há `if`s, não há acesso direto a serviços, não há estado local. Cada ação delega para o ViewModel (`viewModel.save()`). O exemplo completo está em [[#Na prática]].

A **direção das dependências** é a invariante central:

```
View (controller) ──binda──► ViewModel ──chama──► Model (repositórios, serviços)
       ▲                          ▲
   não conhece                não conhece
    ViewModel                    View
```

Nenhuma seta sobe. O ViewModel não sabe que existe uma `Label`; o Model não sabe que existe um ViewModel.

### O ViewModel testável

O JavaFX separa properties em dois módulos: `javafx.base` (properties, observables, bindings) e `javafx.graphics` (nodes, scene, stage). O módulo `javafx.base` **não exige FX Application Thread** — um ViewModel construído só sobre `javafx.beans.property.*` pode ser instanciado, manipulado e assertado em JUnit puro, sem nenhuma infraestrutura de UI. O exemplo completo está em [[#Na prática]].

### DI nos controllers

A assinatura de `setControllerFactory` (OpenJFX 21 Javadoc):

```java
public void setControllerFactory(Callback<Class<?>, Object> controllerFactory)
```

O `Callback<Class<?>, Object>` é uma interface funcional do JavaFX com método `call(Class<?> type)`. O loader a invoca com o `Class` do controller que encontrou no `fx:controller`, esperando receber de volta a instância pronta. É o loader quem ainda faz a injeção dos campos `@FXML` e chama `initialize()` — a factory só substitui o `new`.

**Factory manual com mapa de suppliers:**

```java
Map<Class<?>, Supplier<Object>> registry = new HashMap<>();
registry.put(OrderController.class,
    () -> new OrderController(new OrderRepositoryImpl()));

FXMLLoader loader = new FXMLLoader(
    getClass().getResource("/com/example/order-view.fxml")
);
loader.setControllerFactory(type -> {
    Supplier<Object> supplier = registry.get(type);
    if (supplier == null) {
        throw new IllegalStateException("No factory for " + type.getName());
    }
    return supplier.get();
});
Parent root = loader.load();
```

Essa abordagem é suficiente para projetos sem container. Para projetos maiores, frameworks de DI se plugam exatamente neste ponto — por exemplo, Guice: `injector.getInstance(type)`; Weld/CDI e outros containers ficam para o Galho 8 (planejado). Frameworks de terceiros como mvvmFX existem para reduzir o boilerplate de binding MVVM; basta saber que existem — verifique o repositório corrente antes de adotar.

### Quando MVC basta vs quando MVVM compensa

| Critério | MVC (controller direto) | MVVM (ViewModel + binding) |
|---|---|---|
| Complexidade da tela | Formulário simples, ação única | Múltiplos campos, estado derivado, ações condicionais |
| Ciclo de vida | Tela descartável | App de longa vida, múltiplas telas |
| Necessidade de teste | Baixa (smoke test basta) | Alta (lógica de negócio relevante) |

Regra prática: se você precisa mockar um `TextField` para testar lógica do controller, é hora de extrair um ViewModel.

## Na prática

### OrderViewModel — ViewModel completo

```java
package com.example;

import javafx.beans.binding.BooleanBinding;
import javafx.beans.property.*;

public class OrderViewModel {

    // Estado editável (a View binda bidirecionalmente)
    private final StringProperty  customer = new SimpleStringProperty(this, "customer", "");
    private final IntegerProperty quantity = new SimpleIntegerProperty(this, "quantity", 0);
    private final DoubleProperty  unitPrice = new SimpleDoubleProperty(this, "unitPrice", 0.0);

    // Estado derivado (ReadOnly — a View só lê)
    private final ReadOnlyDoubleWrapper  total;
    private final ReadOnlyBooleanWrapper saveDisabled;

    private final OrderRepository repository;

    public OrderViewModel(OrderRepository repository) {
        this.repository = repository;

        // total = quantity × unitPrice, recalculado automaticamente
        total = new ReadOnlyDoubleWrapper(this, "total", 0.0);
        total.bind(quantity.multiply(unitPrice));

        // saveDisabled = customer vazio OU quantity <= 0
        BooleanBinding invalid = customer.isEmpty()
                .or(quantity.lessThanOrEqualTo(0));
        saveDisabled = new ReadOnlyBooleanWrapper(this, "saveDisabled", true);
        saveDisabled.bind(invalid);
    }

    // --- customer ---
    public StringProperty customerProperty()     { return customer; }
    public String getCustomer()                  { return customer.get(); }
    public void setCustomer(String v)            { customer.set(v); }

    // --- quantity ---
    public IntegerProperty quantityProperty()    { return quantity; }
    public int getQuantity()                     { return quantity.get(); }
    public void setQuantity(int v)               { quantity.set(v); }

    // --- unitPrice ---
    public DoubleProperty unitPriceProperty()    { return unitPrice; }
    public double getUnitPrice()                 { return unitPrice.get(); }
    public void setUnitPrice(double v)           { unitPrice.set(v); }

    // --- total (read-only) ---
    public ReadOnlyDoubleProperty totalProperty()       { return total.getReadOnlyProperty(); }
    public double getTotal()                            { return total.get(); }

    // --- saveDisabled (read-only) ---
    public ReadOnlyBooleanProperty saveDisabledProperty() { return saveDisabled.getReadOnlyProperty(); }
    public boolean isSaveDisabled()                       { return saveDisabled.get(); }

    // --- comando ---
    public void save() {
        if (isSaveDisabled()) return;
        repository.save(getCustomer(), getQuantity(), getUnitPrice());
    }
}
```

### Controller fino — apenas binding

```java
package com.example;

import javafx.fxml.FXML;
import javafx.scene.control.*;
import javafx.util.converter.NumberStringConverter;

public class OrderController {

    @FXML private TextField  customerField;
    @FXML private TextField  quantityField;
    @FXML private TextField  unitPriceField;
    @FXML private Label      totalLabel;
    @FXML private Button     saveButton;

    private final OrderViewModel viewModel;

    // DI via construtor — setControllerFactory entrega o ViewModel
    public OrderController(OrderViewModel viewModel) {
        this.viewModel = viewModel;
    }

    @FXML
    private void initialize() {
        // bindings bidirecionais para campos editáveis
        customerField.textProperty()
            .bindBidirectional(viewModel.customerProperty());
        quantityField.textProperty()
            .bindBidirectional(viewModel.quantityProperty(),
                               new NumberStringConverter("##0"));
        unitPriceField.textProperty()
            .bindBidirectional(viewModel.unitPriceProperty(),
                               new NumberStringConverter("#,##0.00"));

        // bindings unidirecionais para saídas derivadas
        totalLabel.textProperty()
            .bind(viewModel.totalProperty().asString("R$ %.2f"));
        saveButton.disableProperty()
            .bind(viewModel.saveDisabledProperty());
    }

    @FXML
    private void handleSave() {
        viewModel.save();   // delega; controller não sabe o que "save" faz
    }
}
```

### Teste JUnit do ViewModel — sem toolkit

```java
package com.example;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class OrderViewModelTest {

    @Test
    void totalEhQuantidadeVezesPreco() {
        OrderViewModel vm = new OrderViewModel(new FakeOrderRepository());
        vm.setCustomer("Alice");
        vm.setQuantity(3);
        vm.setUnitPrice(49.90);

        assertEquals(149.70, vm.getTotal(), 0.001);
        assertFalse(vm.isSaveDisabled());
    }

    @Test
    void saveDesativadoQuandoCustomerVazio() {
        OrderViewModel vm = new OrderViewModel(new FakeOrderRepository());
        vm.setQuantity(1);
        vm.setUnitPrice(10.0);
        // customer permanece ""

        assertTrue(vm.isSaveDisabled());
    }

    // Fake sem Mockito — POJO puro, sem dependência de test framework pesado
    static class FakeOrderRepository implements OrderRepository {
        String savedCustomer;
        @Override
        public void save(String customer, int qty, double price) {
            this.savedCustomer = customer;
        }
    }
}
```

### setControllerFactory com factory manual

```java
// Na inicialização da aplicação (antes de criar qualquer tela)
OrderRepository repo = new OrderRepositoryImpl();
Map<Class<?>, Supplier<Object>> registry = new HashMap<>();
registry.put(OrderController.class,
    () -> new OrderController(new OrderViewModel(repo)));

Callback<Class<?>, Object> factory = type -> {
    Supplier<Object> s = registry.get(type);
    if (s != null) return s.get();
    // classes não registradas caem no construtor padrão (conveniência)
    try { return type.getDeclaredConstructor().newInstance(); }
    catch (Exception e) { throw new RuntimeException("Cannot instantiate " + type, e); }
};

FXMLLoader loader = new FXMLLoader(
    getClass().getResource("/com/example/order-view.fxml")
);
loader.setControllerFactory(factory);
Parent root = loader.load();
```

## Armadilhas

### (1) Lógica de negócio no controller FXML

**Problema:** o controller FXML tem acesso direto a todos os nós da UI e é o receptor natural de eventos. A gravidade arquitetural o leva a acumular validação, cálculo, acesso a serviços — e o resultado é uma classe intestável sem subir o JavaFX Application Thread.

```java
@FXML
private void handleSave() {
    // PROBLEMA: validação + cálculo + persistência + formatação — tudo no controller
    if (customerField.getText().isEmpty()) {
        errorLabel.setText("Informe o cliente.");
        return;
    }
    double total = Integer.parseInt(quantityField.getText())
                 * Double.parseDouble(priceField.getText());
    totalLabel.setText(String.format("R$ %.2f", total));
    db.insert(customerField.getText(), total);  // acesso direto ao banco
}
```

**Fix:** mova toda lógica para o ViewModel. O controller chama `viewModel.save()` e binda `totalLabel` a `viewModel.totalProperty()`. O ViewModel pode ser testado com JUnit puro; o controller vira uma casca que só binda e delega.

---

### (2) ViewModel referenciando Node ou Label

**Problema:** ao tentar "facilitar" a atualização da UI, o ViewModel passa a guardar referências a nós JavaFX (`Label`, `Button`, `Node`). Isso inverte a seta arquitetural — o ViewModel passa a depender da View, tornando-se um controller disfarçado. Testes do ViewModel voltam a exigir o toolkit.

```java
public class OrderViewModel {
    private Label totalLabel;  // PROBLEMA: ViewModel conhece a View

    public void setTotalLabel(Label l) { this.totalLabel = l; }

    public void recalculate() {
        double total = getQuantity() * getUnitPrice();
        totalLabel.setText(String.format("R$ %.2f", total)); // dependência de nó
    }
}
```

**Fix:** o ViewModel expõe `ReadOnlyDoubleProperty totalProperty()`. É a View que binda `totalLabel.textProperty()` a essa property. O ViewModel nunca sabe que existe um `Label`.

---

### (3) `bindBidirectional` para tudo

**Problema:** usar `bindBidirectional` em todas as ligações — inclusive em campos de saída (totais, status, flags) — cria um grafo de propagação em múltiplas direções. Rastrear "por que esse campo mudou?" vira depuração por tentativa e erro: não há fonte única de verdade, e a ordem de atualização não é determinística para grafos não triviais.

```java
// PROBLEMA: total é derivado, não deveria ser bidirecional
totalField.textProperty().bindBidirectional(viewModel.totalProperty(), converter);
// Agora o usuário pode editar o "total" — comportamento indefinido
```

**Fix:** use `bind` (unidirecional) para tudo que é saída ou derivado. Reserve `bindBidirectional` para a fronteira View↔ViewModel de campos que o usuário edita. Campos de saída sempre via `bind` unidirecional, preferencialmente a uma `ReadOnlyProperty`.

---

### (4) Instanciar serviços com `new` dentro do controller

**Problema:** quando o controller instancia seus próprios colaboradores com `new` (repositório, serviço HTTP, logger estruturado), o acoplamento é máximo e não há como substituir por um fake em teste sem alterar o código de produção.

```java
public class OrderController {
    // PROBLEMA: seam de teste inexistente — OrderRepositoryImpl está cravado
    private final OrderRepository repo = new OrderRepositoryImpl();

    @FXML
    private void handleSave() {
        repo.save(customerField.getText(), ...);
    }
}
```

**Fix:** receba os colaboradores via construtor (ou via setter, se necessário). Use `setControllerFactory` para que o loader entregue o controller já montado com suas dependências. Em teste, passe um fake pelo construtor — sem alterar uma linha de produção.

```java
public class OrderController {
    private final OrderViewModel viewModel; // ViewModel já contém o repo

    public OrderController(OrderViewModel viewModel) {
        this.viewModel = viewModel;
    }
}
```

## Em entrevista

### Frase pronta (inglês)

> "In JavaFX, the natural MVC pattern pairs an FXML view with a controller that acts as glue — but controllers tend to accumulate business logic, state, and formatting, making them untestable without spinning up the UI toolkit. The architectural sweet spot for JavaFX is MVVM: the ViewModel exposes state as observable properties and commands, the controller just binds and delegates, and the data flow is strictly one-directional — View to ViewModel to Model, never back up. Because JavaFX properties live in the `javafx.base` module, which has no dependency on the graphics toolkit, you can instantiate a ViewModel, set its properties, and assert on computed values in plain JUnit — no FX Application Thread, no headless setup. The integration point for dependency injection is `FXMLLoader.setControllerFactory(Callback<Class<?>, Object>)`: the loader calls your factory with the controller class and you return a fully-wired instance. Any DI container plugs in there; for simple projects a manual registry of suppliers is enough."

### Vocabulário

| Termo PT | Termo EN |
|---|---|
| modelo de apresentação | view model |
| ligação de dados | data binding |
| ligação unidirecional | one-way binding / unidirectional binding |
| fábrica de controller | controller factory |
| god class / classe-deus | god class |
| seam de teste | test seam |
| inversão de dependência | dependency inversion |
| injeção por construtor | constructor injection |
| propriedade somente-leitura derivada | computed read-only property |
| camada de apresentação | presentation layer |

## Veja também

- [[06 - FXML e Scene Builder]]
- [[07 - Properties e binding]]
- [[10 - A JavaFX Application Thread — Task, Service e Platform.runLater]]
- [[14 - JavaFX hoje — estado do projeto e Swing vs JavaFX]]
- [[03-Dominios/Java/JavaFX/index|JavaFX (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Dicionário de Java#MVVM|MVVM (Dicionário)]]

## Referências

- [FXMLLoader — OpenJFX 21 Javadoc](https://openjfx.io/javadoc/21/javafx.fxml/javafx/fxml/FXMLLoader.html) — `setControllerFactory(Callback<Class<?>, Object>)`: o loader invoca o callback com o `Class` do controller declarado em `fx:controller` e espera receber a instância pronta; os campos `@FXML` e `initialize()` são processados pelo loader após a factory entregar o objeto.
- [Introduction to FXML — OpenJFX 21](https://openjfx.io/javadoc/21/javafx.fxml/javafx/fxml/doc-files/introduction_to_fxml.html) — ciclo de inicialização (construtor → injeção → initialize()), fx:controller, @FXML, referências de método.
- [javafx.beans.property — OpenJFX 21 Javadoc](https://openjfx.io/javadoc/21/javafx.base/javafx/beans/property/package-summary.html) — `SimpleStringProperty`, `ReadOnlyDoubleWrapper`, `ReadOnlyBooleanWrapper`, padrão bean com três membros por atributo.
- [ObservableValue — OpenJFX 21 Javadoc](https://openjfx.io/javadoc/21/javafx.base/javafx/beans/value/ObservableValue.html) — lazy evaluation; `ChangeListener` força avaliação eager; `WeakChangeListener`.
