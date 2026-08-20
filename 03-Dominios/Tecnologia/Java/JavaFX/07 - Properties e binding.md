---
title: "Properties e binding"
created: 2026-06-06
updated: 2026-06-06
type: concept
progress: backlog
status: seedling
publish: true
fase: Adepto
tags:
  - java
  - javafx
  - adepto
  - binding
aliases:
  - "Properties JavaFX"
  - "Binding"
  - "SimpleStringProperty"
---

# Properties e binding

> [!abstract] TL;DR
> Uma **property** JavaFX é um valor *observável* e *bindável*: todo control expõe um `xxxProperty()` (`textProperty()`, `valueProperty()`, `disableProperty()`...) que outros objetos podem observar ou ao qual podem se ligar. **`bind`** cria uma dependência reativa unidirecional — o alvo passa a espelhar a fonte e vira *read-only* (setá-lo lança `RuntimeException`). **`bindBidirectional`** mantém dois valores independentes em sincronia. A avaliação é **lazy**: um *invalidation listener* só marca o valor como sujo, sem recalcular; um *change listener* força o recálculo (eager). Properties são **o** diferencial do JavaFX sobre o Swing e a base reativa do MVVM.

## O que é

Uma property é a peça que faz a UI do JavaFX *reagir* a dados sem que você escreva um listener manual em cada ponto. O modelo tem duas camadas de abstração que vale separar com clareza:

- **`ObservableValue<T>`** — algo que *tem* um valor e cujo valor pode ser *observado*. É o contrato mínimo: você pode pedir o valor (`getValue()`) e registrar listeners. É só-leitura do ponto de vista do observador.
- **`Property<T>`** — um `ObservableValue` que também é *mutável* (você pode `setValue()`) e *bindável* (você pode `bind()`/`bindBidirectional()`). É a peça concreta que você declara nos seus modelos.

Toda a árvore de controls do JavaFX é construída sobre properties. Um `TextField` não guarda uma `String` num campo privado qualquer — ele guarda uma `StringProperty`, exposta por `textProperty()`. É por isso que você consegue ligar o texto de um `Label` ao conteúdo de um `TextField` com uma única linha, sem nenhum callback explícito: o binding *é* o callback, gerenciado pelo framework.

## Por que importa

O Swing não tem equivalente nativo. Em Swing, sincronizar um label com um campo de texto exige um `DocumentListener` escrito à mão, que lê o valor e chama `setText` no label — código imperativo, repetido, propenso a esquecer um caso. JavaFX troca isso por uma declaração de *intenção*: "este label sempre reflete aquele campo". O framework cuida da propagação.

Esse modelo reativo é a fundação de duas peças centrais do galho:

- **`Task` / `Service`** ([[10 - A JavaFX Application Thread — Task, Service e Platform.runLater]]) expõem `progressProperty()`, `messageProperty()` e `valueProperty()` justamente para que a UI se ligue ao progresso de um trabalho em background via binding, sem tocar na thread de UI manualmente.
- **MVVM** ([[11 - Arquitetura — MVC, MVVM e injeção de dependência]]) vive de properties: o ViewModel expõe estado como properties observáveis e a View se liga a elas. Sem property/binding, não há ViewModel.

Em entrevista, dois assuntos rendem: a distinção **invalidation vs change** (revela se você entende lazy evaluation) e os **pitfalls de leak** com listeners fortes (revela se você já manteve uma app JavaFX viva por horas). Os dois aparecem mais adiante.

## Como funciona

### A hierarquia (ObservableValue → ReadOnlyProperty → Property)

A espinha dorsal é uma cadeia de interfaces, do contrato mais fraco ao mais forte:

```text
Observable                      // pode notificar invalidação
   └─ ObservableValue<T>        // + tem um valor observável (getValue)
        └─ ReadOnlyProperty<T>  // + sabe seu bean e seu name
             └─ Property<T>      // + mutável (setValue) e bindável (bind/bindBidirectional)
```

- **`Observable`** é o piso: define `addListener(InvalidationListener)` / `removeListener`. Só sabe avisar "algo mudou".
- **`ObservableValue<T>`** acrescenta o *valor*: `getValue()` e `addListener(ChangeListener)`. Estende `Observable`.
- **`ReadOnlyProperty<T>`** acrescenta identidade: `getBean()` (o objeto dono) e `getName()` (o nome da property). É o que você expõe quando quer dar leitura mas não escrita.
- **`Property<T>`** acrescenta mutação e binding: `setValue()`, `bind()`, `unbind()`, `isBound()`, `bindBidirectional()`, `unbindBidirectional()`.

As **especializações por tipo** existem por dois motivos — *performance* e *API fluente de binding*:

| Implementação | Tipo | Observação |
|---|---|---|
| `SimpleStringProperty` | `String` | property de texto, a mais comum em forms |
| `SimpleIntegerProperty` | `int` (primitivo) | evita autoboxing no caminho quente |
| `SimpleDoubleProperty` | `double` (primitivo) | idem; aritmética de binding sem boxing |
| `SimpleBooleanProperty` | `boolean` (primitivo) | liga `disableProperty`, `visibleProperty` etc. |
| `SimpleObjectProperty<T>` | qualquer `T` | enums, datas, objetos de domínio |

As variantes numéricas (`Integer`/`Double`/`Long`/`Float`) trabalham com primitivos e por isso oferecem operadores de binding aritmético — `.add()`, `.multiply()`, `.subtract()` — que retornam novos bindings observáveis sem boxing intermediário. Para qualquer outro tipo, use `SimpleObjectProperty<T>`. Há ainda `SimpleListProperty`, `SimpleMapProperty` e `SimpleSetProperty` para coleções observáveis.

### O padrão de property em modelos

Há um padrão canônico, repetido em praticamente todo modelo JavaFX, que vale memorizar. Para cada atributo observável você escreve **três membros**: o campo `private final`, o par getter/setter de conveniência, e o *accessor da property*.

```java
public class Customer {

    private final StringProperty name =
        new SimpleStringProperty(this, "name", "");

    // getter de conveniência — lê o valor atual
    public final String getName() {
        return name.get();
    }

    // setter de conveniência — escreve o valor (cuidado se a property estiver bound)
    public final void setName(String value) {
        name.set(value);
    }

    // accessor da property — expõe o objeto observável para binding/listeners
    public StringProperty nameProperty() {
        return name;
    }
}
```

Três detalhes importam:

- O construtor `new SimpleStringProperty(this, "name", "")` recebe **bean** (`this`), **name** (`"name"`) e **valor inicial** (`""`). O bean e o name não são decorativos: alimentam `getBean()`/`getName()`, úteis em debugging, validação e bibliotecas como TableView que inspecionam a property por reflexão (`PropertyValueFactory`).
- O campo é `final` — você nunca troca o *objeto* property, só o valor dentro dele. Trocar a referência quebraria todos os bindings já estabelecidos.
- A convenção de nomes (`xxxProperty()` para o accessor, `getXxx()`/`setXxx()` para conveniência) é a que o JavaFX e ferramentas esperam. Seguir essa convenção é o que faz `PropertyValueFactory("name")` encontrar `nameProperty()`.

### Binding unidirecional e bidirecional

**Unidirecional (`bind`):** o alvo passa a *espelhar* a fonte. A cada mudança da fonte, o alvo é atualizado.

```java
label.textProperty().bind(customer.nameProperty());
```

A consequência crucial: **o alvo vira read-only**. Enquanto estiver bound, chamar `set()`/`setValue()` no alvo lança `RuntimeException`. A direção é única — fonte → alvo, nunca o contrário. `unbind()` desfaz a ligação e devolve a escrita ao alvo.

**Bidirecional (`bindBidirectional`):** os dois valores permanecem *independentes* (cada um continua mutável), mas qualquer escrita em um propaga ao outro. É o que você usa para ligar um `TextField` editável a uma property de modelo: o usuário digita → o modelo atualiza; o modelo muda por outra via → o campo atualiza.

```java
nameField.textProperty().bindBidirectional(customer.nameProperty());
```

A diferença mental: `bind` é "A *é* B" (A perde autonomia); `bindBidirectional` é "A e B andam juntos" (ambos mantêm autonomia, mas espelhados). `unbindBidirectional(other)` quebra o par.

### Invalidation vs change listener

Esta é a distinção que mais aparece em entrevista, e ela só faz sentido à luz da **lazy evaluation**. O Javadoc de `ObservableValue` é explícito: *"the value is not immediately recomputed after changes, but lazily the next time the value is requested"*. Todas as properties e bindings da biblioteca JavaFX suportam avaliação lazy.

- **`InvalidationListener`** — disparado quando o valor *deixa de ser válido* (fica "sujo"). Ele **não recalcula** o valor. Para um binding lazy, isso é tudo o que precisa acontecer: marcar sujo e seguir em frente. O Javadoc reforça que *"for a lazily evaluated value one does not know if an invalid value really has changed until it is recomputed"* — ou seja, o invalidation nem garante que o valor de fato *mudou*, só que está desatualizado.
- **`ChangeListener`** — recebe `(observable, oldValue, newValue)` e, por precisar comparar antigo e novo, **força a avaliação eager**. O Javadoc é direto: *"attaching a ChangeListener enforces eager computation even if the implementation of the ObservableValue supports lazy evaluation."*

Quando usar cada um:

- **InvalidationListener** quando você só precisa saber que *algo mudou* e vai reagir recalculando sob demanda (ou quando performance importa e o valor é caro). Mais barato.
- **ChangeListener** quando você precisa do valor novo (e/ou do antigo) imediatamente — validação de campo, atualização de outro estado a partir do valor. Conveniente, mas paga o custo da avaliação eager a cada mudança.

### Computed bindings

Além de ligar uma property a outra, você pode *derivar* um valor observável a partir de várias fontes. A classe utilitária `Bindings` é a porta de entrada (*"a helper class with a lot of utility functions to create simple bindings"*).

**`Bindings.createStringBinding(Callable, Observable...)`** — o caso geral. Você fornece a função que produz o valor e **declara explicitamente as dependências** no varargs. O binding recalcula quando *qualquer* dependência invalida:

```java
StringBinding label = Bindings.createStringBinding(
    () -> customer.getName() + " (" + order.getQuantity() + " itens)",
    customer.nameProperty(), order.quantityProperty()   // dependências explícitas
);
```

**`Bindings.concat(Object...)`** — concatena valores (observáveis ou literais) num `StringExpression`, recalculando quando qualquer parte observável muda:

```java
StringExpression resumo = Bindings.concat("Pedido de ", customer.nameProperty());
```

**`Bindings.when(condição).then(a).otherwise(b)`** — um ternário reativo. Resolve para `a` ou `b` conforme uma `ObservableBooleanValue`:

```java
StringBinding selo = Bindings.when(order.quantityProperty().greaterThan(100))
                             .then("ATACADO")
                             .otherwise("VAREJO");
```

**`asString(...)`** — converte um valor observável (tipicamente numérico) num `StringExpression`, com suporte a formato estilo `String.format`:

```java
label.textProperty().bind(order.totalProperty().asString("R$ %.2f"));
```

### Weak listeners e o leak clássico

O leak nasce de *quem referencia quem*. Quando você registra um `ChangeListener` numa property, **a property guarda uma referência forte ao listener**. Se esse listener (tipicamente uma lambda ou classe anônima) capturar `this` ou outro objeto pesado, e a property viver mais que o objeto observador, o GC nunca coleta o observador — porque a property o mantém vivo pela cadeia listener → captura.

Cenário típico: um controller registra um listener numa property de um modelo *longevo* (singleton, cache global). O usuário fecha a tela; o controller deveria morrer; mas o modelo global ainda segura o listener, que segura o controller, que segura a Scene inteira. A app vaza uma tela a cada navegação.

Duas saídas:

- **`WeakChangeListener` / `WeakInvalidationListener`** — envelopam seu listener numa referência fraca. O Javadoc recomenda: *"either unregister a listener by calling removeListener after use or to use an instance of WeakChangeListener"*. Você precisa, ainda assim, manter uma referência *forte* ao listener original em algum lugar com o ciclo de vida certo, senão ele é coletado cedo demais.
- **`removeListener` no dispose** — quando a tela tem um ponto claro de desligamento, remover explicitamente é o mais previsível. (Os próprios `bind` internos do JavaFX já usam weak listeners; o problema é com listeners *seus*.)

### Quando binding clareia vs quando vira teia

Regra prática, fruto de cicatriz:

- **Clareia** quando as cadeias são *rasas* e a direção é *única*. `label ← total ← (quantity × unitPrice)` é trivial de ler: cada seta aponta para uma fonte de verdade, e você acompanha o fluxo num relance.
- **Vira teia** quando há *grafos bidirecionais profundos*. Vários `bindBidirectional` encadeados criam um grafo onde uma escrita em qualquer nó propaga em múltiplas direções. Rastrear "por que esse campo mudou?" vira *debugging hell* — não há uma fonte única de verdade, e a ordem de propagação não é óbvia.

Heurística: use `bind` (unidirecional) sempre que puder; reserve `bindBidirectional` para a fronteira View↔ViewModel de campos editáveis; e nunca encadeie bidirecionais em cadeia (A↔B↔C). Se precisar disso, provavelmente quer um único *source of truth* observável e múltiplos `bind` unidirecionais saindo dele.

## Na prática

Um modelo de domínio neutro com properties no padrão canônico, e a UI ligada por binding.

```java
package com.example;

import javafx.beans.property.*;

public class Order {

    private final StringProperty  id        = new SimpleStringProperty(this, "id", "");
    private final StringProperty  customer  = new SimpleStringProperty(this, "customer", "");
    private final IntegerProperty quantity  = new SimpleIntegerProperty(this, "quantity", 0);
    private final DoubleProperty  unitPrice = new SimpleDoubleProperty(this, "unitPrice", 0.0);

    // --- id ---
    public final String getId()            { return id.get(); }
    public final void setId(String v)      { id.set(v); }
    public StringProperty idProperty()     { return id; }

    // --- customer ---
    public final String getCustomer()         { return customer.get(); }
    public final void setCustomer(String v)   { customer.set(v); }
    public StringProperty customerProperty()  { return customer; }

    // --- quantity ---
    public final int getQuantity()             { return quantity.get(); }
    public final void setQuantity(int v)       { quantity.set(v); }
    public IntegerProperty quantityProperty()  { return quantity; }

    // --- unitPrice ---
    public final double getUnitPrice()         { return unitPrice.get(); }
    public final void setUnitPrice(double v)   { unitPrice.set(v); }
    public DoubleProperty unitPriceProperty()  { return unitPrice; }
}
```

**Binding aritmético + `asString`.** O total é derivado de `quantity × unitPrice` e o label se liga a ele formatado:

```java
Order order = new Order();
order.setQuantity(3);
order.setUnitPrice(49.90);

// total observável derivado das duas properties (sem boxing — variantes numéricas)
NumberBinding total = order.quantityProperty().multiply(order.unitPriceProperty());

Label totalLabel = new Label();
totalLabel.textProperty().bind(total.asString("R$ %.2f"));
// totalLabel agora mostra "R$ 149.70" e atualiza sozinho se quantity ou unitPrice mudar
```

**Bidirecional com conversão.** Um `TextField` editável ligado a uma property numérica precisa de conversão `String ↔ Number`. `Bindings.bindBidirectional` aceita um `StringConverter`:

```java
import javafx.util.converter.NumberStringConverter;

TextField quantityField = new TextField();
Bindings.bindBidirectional(
    quantityField.textProperty(),
    order.quantityProperty(),
    new NumberStringConverter()
);
// usuário digita "10" -> order.quantity vira 10; setQuantity(5) por outra via -> campo mostra "5"
```

**Computed binding com `createStringBinding`.** Um resumo que depende de três properties — todas declaradas como dependências:

```java
StringBinding summary = Bindings.createStringBinding(
    () -> String.format("%s — %d × R$ %.2f",
            order.getCustomer(), order.getQuantity(), order.getUnitPrice()),
    order.customerProperty(),       // dependência 1
    order.quantityProperty(),       // dependência 2
    order.unitPriceProperty()       // dependência 3
);

Label summaryLabel = new Label();
summaryLabel.textProperty().bind(summary);
```

**A `RuntimeException` ao setar uma property bound.** Depois de `bind`, o alvo é read-only:

```java
totalLabel.textProperty().bind(total.asString("R$ %.2f"));
totalLabel.setText("manual");   // BOOM
```

```text
java.lang.RuntimeException: A bound value cannot be set.
```

O conserto é não setar quem está bound — ou `unbind()` antes, se você realmente precisa retomar o controle manual:

```java
totalLabel.textProperty().unbind();
totalLabel.setText("manual");   // ok agora — não está mais bound
```

## Armadilhas

### (1) Setar uma property que está bound

**Problema:** depois de `bind`, o alvo é read-only. Qualquer `set`/`setValue` lança `RuntimeException` em runtime — não é erro de compilação, então passa despercebido até a linha executar.

```java
slider.valueProperty().bindBidirectional(order.unitPriceProperty());
order.unitPriceProperty().bind(catalog.basePriceProperty()); // PROBLEMA
order.setUnitPrice(10.0);  // RuntimeException: A bound value cannot be set.
```

```text
java.lang.RuntimeException: A bound value cannot be set.
```

**Fix:** quem binda não seta. Decida qual property é a fonte de verdade e só escreva *nela*. Se precisar retomar a escrita do alvo, chame `unbind()` antes:

```java
order.unitPriceProperty().unbind();
order.setUnitPrice(10.0);  // ok
```

---

### (2) Change listener anônimo segurando um objeto grande (leak)

**Problema:** a property guarda referência *forte* ao listener. Um listener anônimo que captura `this` (ou um cache pesado, uma Scene inteira) mantém esse objeto vivo enquanto a property viver — e properties de modelos globais vivem muito.

```java
// controller registra-se numa property de um modelo SINGLETON longevo
AppState.INSTANCE.themeProperty().addListener((obs, old, val) -> {
    this.repaintEverything();   // captura 'this' -> o controller nunca morre
});
```

**Fix:** use `WeakChangeListener` (mantendo uma referência forte ao listener real com o ciclo de vida certo) ou remova explicitamente no dispose da tela:

```java
ChangeListener<String> themeListener = (obs, old, val) -> repaintEverything();
AppState.INSTANCE.themeProperty().addListener(new WeakChangeListener<>(themeListener));
// ... ou, no desligamento da tela:
AppState.INSTANCE.themeProperty().removeListener(themeListener);
```

---

### (3) Ciclo bidirecional

**Problema:** encadear `bindBidirectional` num ciclo (A↔B, B↔C, C↔A) cria um grafo de propagação sem fonte única de verdade. O comportamento fica errático — atualizações em loop, ordem de propagação imprevisível, e em casos patológicos `StackOverflowError`.

```java
Bindings.bindBidirectional(a.valueProperty(), b.valueProperty());
Bindings.bindBidirectional(b.valueProperty(), c.valueProperty());
Bindings.bindBidirectional(c.valueProperty(), a.valueProperty()); // fecha o ciclo
```

**Fix:** desenhe o grafo no papel e quebre o ciclo. Eleja *uma* property como fonte de verdade e faça as outras se ligarem a ela com `bind` unidirecional. Bidirecional só na fronteira View↔ViewModel, nunca em cadeia.

---

### (4) `createStringBinding` esquecendo de declarar uma dependência

**Problema:** o binding só recalcula quando uma de suas *dependências declaradas* invalida. Se a função lê uma property que você esqueceu de listar no varargs, o binding não atualiza quando ela muda — e o bug é silencioso (o valor fica "congelado" no primeiro cálculo).

```java
StringBinding label = Bindings.createStringBinding(
    () -> order.getCustomer() + ": " + order.getQuantity(),
    order.customerProperty()   // PROBLEMA: quantity é lida mas NÃO declarada
);
// mudar a quantity não atualiza o label
```

**Fix:** liste **todas** as properties lidas dentro da função como dependências no varargs.

```java
StringBinding label = Bindings.createStringBinding(
    () -> order.getCustomer() + ": " + order.getQuantity(),
    order.customerProperty(), order.quantityProperty()  // todas as dependências
);
```

## Em entrevista

### Frase pronta (inglês)

> "A JavaFX property is an observable, bindable value — every control exposes one through accessors like `textProperty()` or `valueProperty()`. With `bind`, the target mirrors a source and becomes read-only, so trying to set it throws a RuntimeException; with `bindBidirectional`, two properties stay independent but synchronized, which is what you use between a TextField and a model field. The key subtlety is lazy evaluation: an invalidation listener just marks the value dirty without recomputing it, while a change listener forces eager evaluation because it needs the old and new values — so attaching change listeners is more expensive. The classic memory leak comes from a property holding a strong reference to your listener; the fix is a WeakChangeListener or removing the listener on dispose. All of this is what makes properties the reactive backbone of MVVM, something Swing never had natively."

### Vocabulário

| Termo PT | Termo EN |
|---|---|
| valor observável | observable value |
| ligação (binding) | binding |
| ligação bidirecional | bidirectional binding |
| avaliação preguiçosa | lazy evaluation |
| ouvinte de invalidação | invalidation listener |
| ouvinte de mudança | change listener |
| ligação computada/derivada | computed / derived binding |
| referência fraca | weak reference |
| fonte única de verdade | single source of truth |

## Veja também

- [[04 - Controls essenciais]]
- [[06 - FXML e Scene Builder]]
- [[08 - TableView, cell factories e dados observáveis]]
- [[10 - A JavaFX Application Thread — Task, Service e Platform.runLater]]
- [[11 - Arquitetura — MVC, MVVM e injeção de dependência]]
- [[03-Dominios/Tecnologia/Java/JavaFX/index|JavaFX (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#Property (JavaFX)|Property (Dicionário)]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#binding (JavaFX)|binding (Dicionário)]]

## Referências

- [javafx.beans.property — OpenJFX 21 Javadoc](https://openjfx.io/javadoc/21/javafx.base/javafx/beans/property/package-summary.html) — implementações `Simple*Property` (String/Integer/Double/Boolean/Object e coleções) como "full implementation of a Property wrapping" cada tipo
- [ObservableValue — OpenJFX 21 Javadoc](https://openjfx.io/javadoc/21/javafx.base/javafx/beans/value/ObservableValue.html) — lazy evaluation ("not immediately recomputed... but lazily the next time the value is requested"); change listener força avaliação eager; recomendação de `WeakChangeListener` / `removeListener` contra leak
- [Property — OpenJFX 21 Javadoc](https://openjfx.io/javadoc/21/javafx.base/javafx/beans/property/Property.html) — assinaturas `bind`/`unbind`/`isBound`/`bindBidirectional`/`unbindBidirectional`
- [Bindings — OpenJFX 21 Javadoc](https://openjfx.io/javadoc/21/javafx.base/javafx/beans/binding/Bindings.html) — fábricas `createStringBinding`/`createIntegerBinding`/`createDoubleBinding`, `concat`, `format`, `when().then().otherwise()`, `asString`
