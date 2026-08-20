---
title: "Composição funcional e funções de alta ordem"
created: 2026-06-04
updated: 2026-06-04
type: concept
progress: backlog
status: seedling
publish: true
fase: Magus
tags:
  - java
  - collections
  - magus
  - funcional
  - composicao
aliases:
  - Composição de funções
  - Funções de alta ordem
  - compose andThen
---

# Composição funcional e funções de alta ordem

> [!abstract] TL;DR
> **Composição funcional** é montar comportamento grande a partir de funções pequenas, encadeando-as como um pipeline. As quatro interfaces de `java.util.function` trazem operadores de composição como métodos `default`: `Function` tem `andThen` (executa `this` primeiro, depois o argumento) e `compose` (executa o argumento primeiro, depois `this`) — **a ordem é o ponto que mais confunde e mais cai em entrevista**. `Predicate` compõe lógica booleana com `and`/`or`/`negate` (curto-circuito) e tem o estático `isEqual`. `Consumer` encadeia efeitos colaterais em sequência com `andThen`. **Função de alta ordem** (*higher-order function*) é uma função que recebe ou retorna outra função — em Java, um método que aceita ou devolve uma `Function`/`Predicate`/etc. O estilo é poderoso para reuso e legibilidade declarativa, mas tem custo real: composição inline profunda produz stack traces opacos e debug difícil. A decisão sênior é saber **quando aplicar e quando recuar para código nomeado**.

## O que é

**Composição funcional** é a técnica de construir uma função complexa combinando funções menores, cada uma com responsabilidade única. Em vez de um método monolítico que faz cinco transformações, você define cinco funções e as encadeia — o resultado é um pipeline em que a saída de uma etapa vira a entrada da seguinte.

Java expõe isso diretamente nas interfaces de `java.util.function`, que declaram operadores de composição como métodos `default`:

- `Function<T,R>`: `andThen`, `compose`, e o estático `identity`.
- `Predicate<T>`: `and`, `or`, `negate`, e o estático `isEqual`.
- `Consumer<T>`: `andThen`.

**Função de alta ordem** (*higher-order function*, HOF) é o conceito complementar: uma função que **recebe outra função como parâmetro** ou **retorna uma função como resultado** (ou ambos). Java não tem funções soltas, então uma HOF aqui é um método cuja assinatura tem `Function`/`Predicate`/`Consumer`/`Supplier` como parâmetro ou tipo de retorno. `Stream.map(Function)` é uma HOF; um método `Function<Order,Order> descontoPara(Config)` que devolve uma função também é.

A mecânica das interfaces funcionais em si (SAM, `@FunctionalInterface`, lambdas, method references) é pré-requisito desta nota — veja [[04 - Lambdas e interfaces funcionais]]. Aqui o foco é **compor** essas funções e tratá-las como valores de primeira classe.

## Por que importa

Composição funcional é a base do estilo declarativo do Java moderno — todo pipeline de Stream é, no fundo, composição de `Function` e `Predicate`. Saber compor explicitamente desbloqueia três ganhos:

- **Reuso granular**: funções pequenas e nomeadas (`normalizarEmail`, `aplicarImposto`) viram blocos reaproveitáveis em vários pipelines, em vez de lógica duplicada inline.
- **Legibilidade declarativa**: `valido.and(emEstoque).and(naoExpirado)` lê-se quase como a regra de negócio em linguagem natural.
- **Testabilidade**: cada função isolada é testável sozinha, sem montar o pipeline inteiro.

Mas há um custo que separa o uso ingênuo do uso sênior. Composição **não é gratuita**:

- **Stack traces opacos**: quando algo estoura no meio de `f.andThen(g).andThen(h)`, o stack trace mostra lambdas sintéticas (`Lambda$1234`) sem nome de método de domínio. Rastrear qual etapa falhou é mais difícil que num bloco imperativo.
- **Debug difícil**: colocar breakpoint dentro de uma composição inline é desconfortável; inspecionar o valor intermediário entre `andThen`s exige quebrar a cadeia.
- **Abstração que esconde custo**: cada `andThen` cria um novo objeto função; composição profunda em hot path tem overhead de alocação e indireção.

A decisão de senior não é "usar composição sempre" nem "nunca" — é **calibrar**: aplicar onde o ganho de clareza/reuso supera o custo de debug, e recuar para código imperativo nomeado onde a composição vira charada.

## Como funciona

### `Function.compose` vs `andThen` (a ordem importa)

Estes dois métodos compõem duas `Function`, mas **em ordens opostas**. Confundi-los inverte o resultado — é o erro número um.

Direto do Javadoc do Java 21:

- `andThen(after)`: *"Returns a composed function that first applies **this** function to its input, and then applies the `after` function to the result."*
- `compose(before)`: *"Returns a composed function that first applies the `before` function to its input, and then applies **this** function to the result."*

Traduzindo para a regra prática:

| Expressão | O que roda primeiro | Depois | Leitura |
|---|---|---|---|
| `f.andThen(g)` | `f` | `g` | esquerda → direita (como method chaining) |
| `f.compose(g)` | `g` | `f` | direita → esquerda (como composição matemática `f∘g`) |

```java
Function<Integer, Integer> dobrar    = x -> x * 2;
Function<Integer, Integer> somarTres = x -> x + 3;

// andThen: dobrar PRIMEIRO, depois somarTres
Function<Integer, Integer> a = dobrar.andThen(somarTres);
a.apply(5);   // dobrar(5)=10 → somarTres(10)=13  → 13

// compose: somarTres PRIMEIRO, depois dobrar
Function<Integer, Integer> b = dobrar.compose(somarTres);
b.apply(5);   // somarTres(5)=8 → dobrar(8)=16     → 16
```

Note que `dobrar.andThen(somarTres)` e `somarTres.compose(dobrar)` produzem **o mesmo pipeline** (dobrar então somar). São duas formas de escrever a mesma composição — escolha pela que lê melhor no contexto.

O estático `Function.identity()` retorna uma função que devolve o próprio argumento (`x -> x`). É útil como elemento neutro em reduções/composições e como valor de mapeamento "não transforme" — por exemplo, `Collectors.toMap(Order::id, Function.identity())` mapeia cada chave para o próprio objeto.

### `Predicate.and` / `or` / `negate` / `isEqual`

`Predicate` compõe lógica booleana. Os dois conectores são **curto-circuitantes**, exatamente como `&&` e `||`:

- `and(other)`: *"short-circuiting logical AND"* — se `this` retorna `false`, `other` **não é avaliado**.
- `or(other)`: *"short-circuiting logical OR"* — se `this` retorna `true`, `other` **não é avaliado**.
- `negate()`: retorna a negação lógica de `this`.
- `isEqual(targetRef)` (estático): retorna um `Predicate` que testa igualdade via `Objects.equals(input, targetRef)` — null-safe, aceita `targetRef` nulo.

```java
Predicate<String> naoVazio = s -> !s.isBlank();
Predicate<String> curto    = s -> s.length() < 20;

Predicate<String> valido       = naoVazio.and(curto);    // ambos
Predicate<String> qualquerCoisa = naoVazio.or(curto);    // pelo menos um
Predicate<String> vazio        = naoVazio.negate();      // inverso

// isEqual — predicado de igualdade null-safe
Predicate<String> ehAdmin = Predicate.isEqual("admin");
ehAdmin.test("admin");   // true
```

O curto-circuito tem consequência prática: se `other` faz I/O ou é caro, **coloque o predicado barato e mais seletivo à esquerda** para que o caro seja pulado com frequência. Exceções lançadas em qualquer um dos predicados são repassadas ao chamador; se `this` lança, `other` não é avaliado.

### `Consumer.andThen`

`Consumer` representa efeito colateral (`void accept(T)`), então não há "transformar e passar adiante" — só executar em sequência. `andThen` encadeia dois consumidores **na ordem em que aparecem**:

Javadoc: *"Returns a composed `Consumer` that performs, in sequence, this operation followed by the `after` operation. If performing this operation throws an exception, the `after` operation will not be performed."*

```java
Consumer<Order> logar    = o -> log.info("Processando {}", o.id());
Consumer<Order> persistir = o -> repository.save(o);
Consumer<Order> notificar = o -> mailer.confirmar(o);

Consumer<Order> pipeline = logar.andThen(persistir).andThen(notificar);
pipeline.accept(order);   // logar → persistir → notificar, nessa ordem
```

Ponto crítico: se `persistir` lançar, `notificar` **não roda** — a exceção sobe imediatamente. Composição de `Consumer` não tem semântica transacional; se você precisa de "tudo ou nada", isso é responsabilidade do código de domínio, não do `andThen`.

### Funções de alta ordem (receber e retornar `Function`)

Em Java, uma HOF é só um método que tem uma interface funcional na assinatura. Dois sabores:

**Receber uma função como parâmetro** — o padrão de toda a Stream API e de métodos genéricos de processamento:

```java
// recebe a regra de transformação como Function — agnóstico ao domínio
static <T, R> List<R> mapear(List<T> itens, Function<T, R> regra) {
    return itens.stream().map(regra).toList();
}
```

**Retornar uma função** — uma *fábrica de funções* (factory), onde parâmetros de configuração viram uma função especializada:

```java
// retorna uma Function parametrizada pela taxa — uma "função que faz funções"
static Function<Order, Order> aplicarTaxa(double taxa) {
    return order -> order.comTotal(order.total() * (1 + taxa));
}

Function<Order, Order> imposto = aplicarTaxa(0.18);   // especializa
Order comImposto = imposto.apply(order);
```

A fábrica é onde **closures** aparecem em Java: a `Function` retornada captura `taxa` do escopo do método. Isso leva ao próximo ponto.

### Captura e `effectively final`; closures em Java

Quando um lambda ou method reference usa uma variável local do método envolvente, ele **captura** essa variável. Java só permite capturar variáveis `final` ou *effectively final* — declaradas uma vez e nunca reatribuídas. Tentar capturar uma variável reatribuída é erro de compilação: *"Variable used in lambda expression should be final or effectively final"*.

```java
static Function<Order, Order> aplicarTaxa(double taxa) {
    // 'taxa' é parâmetro nunca reatribuído → effectively final → capturável
    return order -> order.comTotal(order.total() * (1 + taxa));
}
```

O lambda retornado é um **closure**: ele "fecha sobre" o valor de `taxa` no momento da criação e carrega esse valor mesmo depois de o método `aplicarTaxa` ter retornado. Como Java captura o **valor** (para primitivos) ou a **referência** (para objetos) e exige `effectively final`, não existe o problema clássico de closures sobre variável de laço mutável que outras linguagens têm. A restrição parece limitante, mas é o que torna o valor capturado estável e previsível.

A consequência prática: para acumular estado dentro de um lambda você **não** reatribui uma variável local (não compila); usa um objeto mutável capturado por referência (`AtomicInteger`, um array de um elemento) — o que normalmente é sinal de que você deveria usar `reduce`/`collect` em vez de um efeito colateral.

### Quando o estilo funcional **ajuda** vs **atrapalha**

| Cenário | Estilo funcional **ajuda** | Estilo funcional **atrapalha** |
|---|---|---|
| Transformação de dados | Pipeline `map`/`filter` declarativo, sem laço manual | — |
| Reuso de regra | Função nomeada reaproveitada em N pipelines | — |
| Composição rasa (2-3 etapas nomeadas) | Lê como a regra de negócio | — |
| Debugging | — | Breakpoint dentro de composição inline é desconfortável |
| Stack traces | — | Lambdas sintéticas (`Lambda$…`) escondem a etapa que falhou |
| Estado mutável | — | Efeito colateral em lambda quebra a clareza; força `AtomicX`/arrays |
| Composição profunda inline | — | `f.andThen(g).andThen(h).compose(i)…` vira charada ilegível |

A heurística sênior: **funcional brilha em transformação declarativa e reuso de regras puras**; **recua diante de debugging intensivo, estado mutável e cadeias profundas inline**. Quando a composição passa de ~3 etapas ou mistura efeitos colaterais, extraia para funções nomeadas ou volte ao imperativo — legibilidade vence elegância.

## Na prática

Cenário: um sistema de pedidos com `record Order(String id, String customerName, String status, double total)` que oferece um "wither" `comTotal(double)`. Vamos montar um pipeline de transformação, um predicado composto e uma fábrica de funções.

```java
import java.util.List;
import java.util.function.*;

record Order(String id, String customerName, String status, double total) {
    Order comTotal(double novoTotal) {
        return new Order(id, customerName, status, novoTotal);
    }
}

public class OrderPipeline {

    // --- Função composta: pipeline de transformação com andThen ---
    static final Function<Order, Order> aplicarImposto =
        o -> o.comTotal(o.total() * 1.18);

    static final Function<Order, Order> arredondar =
        o -> o.comTotal(Math.round(o.total() * 100.0) / 100.0);

    // andThen: imposto PRIMEIRO, depois arredonda — esquerda → direita
    static final Function<Order, Order> precificar =
        aplicarImposto.andThen(arredondar);

    // --- Predicate composto: regra de negócio declarativa ---
    static final Predicate<Order> pendente   = o -> "PENDING".equals(o.status());
    static final Predicate<Order> acimaDeCem = o -> o.total() > 100.0;

    // pendente E acima de cem (ou, alternativamente, urgente)
    static final Predicate<Order> elegivel = pendente.and(acimaDeCem);

    // --- Função de alta ordem: fábrica que RETORNA uma Function ---
    static Function<Order, Function<Order, Order>> nada = o -> Function.identity();

    // fábrica parametrizada: Function<Config, Function<Order,Order>>
    record Config(double desconto) {}

    static Function<Config, Function<Order, Order>> descontoFactory =
        config -> order -> order.comTotal(order.total() * (1 - config.desconto()));

    public static void main(String[] args) {
        List<Order> orders = List.of(
            new Order("A1", "Alice", "PENDING", 150.0),
            new Order("B2", "Bob",   "PAID",    320.0),
            new Order("C3", "Carol", "PENDING",  80.0)
        );

        // especializa a fábrica → Function<Order,Order>
        Function<Order, Order> aplicar10pct = descontoFactory.apply(new Config(0.10));

        // pipeline completo: filtra elegíveis, precifica, aplica desconto
        List<Order> processados = orders.stream()
            .filter(elegivel)
            .map(precificar.andThen(aplicar10pct))
            .toList();

        processados.forEach(o ->
            System.out.printf("%s: %.2f%n", o.id(), o.total()));
        // Só A1 passa no filtro (PENDING e > 100): imposto → arredonda → -10%
    }
}
```

Pontos do exemplo:
- `precificar = aplicarImposto.andThen(arredondar)` deixa explícita a ordem (imposto primeiro). Trocar por `compose` inverteria — arredondaria antes de aplicar imposto, resultado errado.
- `elegivel = pendente.and(acimaDeCem)` aproveita curto-circuito: pedidos `PAID` nem chegam a checar o total.
- `descontoFactory` é a HOF mais densa: tipo `Function<Config, Function<Order,Order>>` — recebe config e **retorna** uma função especializada, que captura `config` como closure.

## Armadilhas

### (1) Inverter `compose` e `andThen` — ordem trocada, resultado errado

**O problema:** os dois métodos lêem parecido, mas executam em ordens opostas. Trocar um pelo outro não dá erro de compilação — só um resultado silenciosamente errado.

```java
Function<Order, Order> imposto    = o -> o.comTotal(o.total() * 1.18);
Function<Order, Order> arredondar = o -> o.comTotal(Math.round(o.total() * 100.0) / 100.0);

// ERRADO — compose roda o argumento PRIMEIRO: arredonda ANTES do imposto
Function<Order, Order> errado = imposto.compose(arredondar);
// arredondar(o) → imposto(...) : centavos do imposto não são arredondados
```

**Fix:** lembre da regra — `f.andThen(g)` roda `f` primeiro (esquerda → direita); `g.compose(f)` também roda `f` primeiro. **Escolha pela ordem desejada, não pelo nome que soa melhor.** Para "imposto e depois arredonda", use `andThen`:

```java
// CORRETO — andThen roda 'this' primeiro: imposto, depois arredonda
Function<Order, Order> certo = imposto.andThen(arredondar);
```

Mnemônico: `andThen` = "e **depois**" (este, e depois aquele); `compose` = composição matemática `f∘g` (aplica `g` por dentro primeiro).

---

### (2) Pipeline funcional ilegível — composição profunda inline

**O problema:** encadear muitas etapas inline, com lambdas anônimas, produz uma expressão que ninguém consegue ler nem revisar.

```java
// ILEGÍVEL — composição profunda com lambdas inline
var resultado = orders.stream()
    .map(((Function<Order, Order>) o -> o.comTotal(o.total() * 1.18))
        .andThen(o -> o.comTotal(Math.round(o.total() * 100.0) / 100.0))
        .andThen(o -> o.comTotal(o.total() * 0.9))
        .compose(o -> o.comTotal(Math.max(o.total(), 0))))
    .toList();
```

**Fix:** extraia cada etapa para uma `Function` nomeada e componha em um passo declarativo. O nome de cada função documenta a intenção e os stack traces ficam rastreáveis.

```java
// LEGÍVEL — etapas nomeadas, composição explícita
Function<Order, Order> naoNegativo = o -> o.comTotal(Math.max(o.total(), 0));
Function<Order, Order> imposto     = o -> o.comTotal(o.total() * 1.18);
Function<Order, Order> arredondar  = o -> o.comTotal(Math.round(o.total() * 100.0) / 100.0);
Function<Order, Order> desconto    = o -> o.comTotal(o.total() * 0.9);

Function<Order, Order> precificar =
    naoNegativo.andThen(imposto).andThen(arredondar).andThen(desconto);

var resultado = orders.stream().map(precificar).toList();
```

---

### (3) Stack trace inútil em lambda aninhada

**O problema:** quando uma exceção estoura no meio de uma composição inline, o stack trace mostra frames sintéticos como `OrderPipeline.lambda$main$3` — sem nome de domínio, é difícil saber qual etapa falhou, ainda mais com várias lambdas anônimas idênticas em estrutura.

```java
// Difícil de diagnosticar — lambda anônima inline no andThen
Function<Order, Order> pipe =
    ((Function<Order, Order>) o -> o.comTotal(o.total() / divisor))   // divisor pode ser 0
        .andThen(o -> o.comTotal(o.total() * 1.18));
// ArithmeticException → stack trace aponta para "lambda$pipe$0", sem pista de qual etapa
```

**Fix:** nomeie as funções (extraia para método ou variável com nome de domínio) e/ou quebre a cadeia em variáveis intermediárias durante o debug. Métodos nomeados aparecem com nome real no stack trace; method references (`OrderPricer::aplicarImposto`) preservam o nome do método.

```java
static Order aplicarTaxa(Order o)  { return o.comTotal(o.total() / divisor); }
static Order comImposto(Order o)   { return o.comTotal(o.total() * 1.18); }

// method references → stack trace mostra "OrderPricer.aplicarTaxa"
Function<Order, Order> pipe =
    ((Function<Order, Order>) OrderPricer::aplicarTaxa).andThen(OrderPricer::comImposto);
```

## Em entrevista

### Frase pronta (inglês)

> "Functional composition in Java is built into the `java.util.function` interfaces as default methods. The trickiest part is the order: `Function.andThen` applies `this` first and then the argument — left to right, like method chaining — while `compose` applies the argument first and then `this` — right to left, like mathematical composition `f∘g`. So `f.andThen(g)` and `g.compose(f)` produce the exact same pipeline, just written differently."
>
> "`Predicate` composes boolean logic with `and`, `or`, and `negate`, all short-circuiting like `&&` and `||`, plus a static `isEqual` for null-safe equality. `Consumer.andThen` chains side effects in sequence, but with no transactional semantics — if the first consumer throws, the second one never runs."
>
> "A higher-order function is one that takes or returns another function. In Java that's any method with a `Function`, `Predicate`, or similar in its signature — `Stream.map` takes one, and a factory that returns a parameterized `Function` is one that returns one. Those factories rely on closures capturing effectively-final variables. The senior judgment is knowing when composition helps — declarative transformation and reuse — versus when it hurts: deep inline chains give you opaque stack traces with synthetic lambda frames, so you extract named functions or drop back to imperative code."

### Vocabulário

| Termo PT | Termo EN |
|---|---|
| composição funcional | functional composition |
| função de alta ordem | higher-order function (HOF) |
| encadeamento (esquerda → direita) | chaining / left-to-right |
| composição matemática (direita → esquerda) | mathematical composition / right-to-left |
| curto-circuito | short-circuiting |
| efetivamente final | effectively final |
| fechamento / closure | closure |
| captura de variável | variable capture |
| fábrica de funções | function factory |
| stack trace opaco | opaque stack trace |
| frame de lambda sintético | synthetic lambda frame |

## Veja também

- [[04 - Lambdas e interfaces funcionais]]
- [[07 - Operações de Stream — intermediárias e terminais]]
- [[10 - Optional]]
- [[03-Dominios/Tecnologia/Java/Collections e Streams/index|Collections e Streams (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/08 - Interfaces e classes abstratas|Interfaces]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#effectively final|effectively final]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#Function / Predicate / Consumer / Supplier|Function / Predicate / Consumer / Supplier]]

## Referências

- [Function — Java 21 API (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/function/Function.html)
- [Predicate — Java 21 API (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/function/Predicate.html)
- [Consumer — Java 21 API (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/function/Consumer.html)
- [java.util.function — package summary (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/function/package-summary.html)
</content>
</invoke>
