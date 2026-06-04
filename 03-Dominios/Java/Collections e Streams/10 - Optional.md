---
title: "Optional"
created: 2026-06-04
updated: 2026-06-04
type: concept
progress: backlog
status: seedling
publish: true
fase: adepto
tags:
  - java
  - collections
  - adepto
  - optional
  - funcional
aliases:
  - "Optional"
  - "Optional Java"
---

# Optional

> [!abstract] TL;DR
> `Optional<T>` é um container que pode conter ou não um valor — a presença ou ausência do valor **faz parte do tipo**. O objetivo central é comunicar, no contrato do método, que o resultado pode não existir, sem recorrer a `null`. Use-o como **tipo de retorno** apenas; nunca como campo de classe ou parâmetro de método. O estilo idiomático combina `map`, `flatMap` e `orElse`/`orElseThrow` em cadeia, sem nunca chamar `get()` cru. `orElse(expr)` sempre avalia `expr`; prefira `orElseGet(() -> expr)` quando `expr` for custoso.

## O que é

`Optional<T>` (pacote `java.util`, desde Java 8) é um objeto container que encapsula zero ou um valor de tipo `T`. Em vez de retornar `null` quando um resultado não existe, um método retorna `Optional.empty()` — e o chamador é obrigado pelo compilador a tratar essa possibilidade de forma explícita.

A classe é **valor-based** (*value-based class*): duas instâncias com o mesmo conteúdo são consideradas iguais via `equals`, mas não se deve comparar com `==` nem usar instâncias como monitor de sincronização.

```java
// Retorno que comunica ausência de forma explícita
Optional<Order> findById(long id);         // pode não encontrar
Order           findByIdOrFail(long id);   // sempre retorna ou lança
```

A assinatura já documenta a semântica: o chamador de `findById` sabe que o pedido pode não existir; o de `findByIdOrFail` sabe que receberá um pedido ou uma exceção.

## Por que importa

**Elimina NPE silenciosa.** Retornar `null` é legal em Java, mas o compilador não exige que o chamador verifique — o NPE aparece em tempo de execução, longe do ponto de origem. `Optional` torna a ausência impossível de ignorar.

**Documenta o contrato.** O tipo de retorno `Optional<T>` é documentação viva: "este método pode não produzir resultado". Sem `Optional`, essa semântica fica escondida em Javadoc ou convenção de equipe.

**Composição funcional.** O encadeamento `map → filter → orElse` substitui blocos aninhados de `if (x != null)`, tornando o fluxo de transformação linear e legível.

**Cobrado em entrevista.** Avaliadores esperam que o candidato:
- explique a diferença entre `orElse` e `orElseGet` (avaliação eager vs lazy);
- identifique anti-patterns (`get()` cru, `Optional` como campo, `Optional` como parâmetro);
- demonstre uso correto com `map` e `flatMap` em vez de `isPresent()` + `get()`.

## Como funciona

### Criação (`of` / `ofNullable` / `empty`)

```java
// of — valor garantidamente não-nulo; lança NPE se null
Optional<String> presente = Optional.of("Java 21");

// ofNullable — aceita null; retorna empty se o argumento for null
String valorNulo = null;
Optional<String> seguro = Optional.ofNullable(valorNulo);  // Optional.empty()

// empty — ausência explícita; uso típico em retornos
Optional<Order> naoEncontrado = Optional.empty();
```

Regra simples: use `of` quando você tem certeza que o valor não é `null`; use `ofNullable` ao integrar com APIs legadas que podem retornar `null`.

### Transformação (`map` / `flatMap` / `filter`)

`map` aplica uma função ao valor, se presente, e retorna um novo `Optional` com o resultado. Se o valor estiver ausente — ou se o mapeador retornar `null` — retorna `Optional.empty()`.

```java
Optional<String> codigo = findById(42L)
    .map(Order::getCode);   // Optional<String>; vazio se pedido não existe
```

`flatMap` é usado quando o próprio mapeador retorna um `Optional`. Sem `flatMap`, você obteria `Optional<Optional<T>>` — o que raramente é desejado.

```java
// getDiscount() retorna Optional<Discount>
Optional<Discount> desconto = findById(42L)
    .flatMap(Order::getDiscount);
```

`filter` mantém o valor apenas se o predicado for verdadeiro; caso contrário, retorna `Optional.empty()`.

```java
Optional<Order> pedidoPendente = findById(42L)
    .filter(o -> o.getStatus() == Status.PENDING);
```

### Consumo (`orElse` / `orElseGet` / `orElseThrow` / `ifPresent` / `ifPresentOrElse`)

```java
// orElse — retorna o valor ou o default fornecido (SEMPRE avaliado)
BigDecimal total = findById(id).map(Order::getTotal).orElse(BigDecimal.ZERO);

// orElseGet — retorna o valor ou invoca o Supplier (avaliado só se necessário)
String codigo = findById(id)
    .map(Order::getCode)
    .orElseGet(() -> generateTemporaryCode());

// orElseThrow sem argumento — lança NoSuchElementException (Java 10+)
Order pedido = findById(id).orElseThrow();

// orElseThrow com Supplier — lança exceção customizada
Order pedido = findById(id)
    .orElseThrow(() -> new OrderNotFoundException(id));

// ifPresent — executa ação somente se valor presente
findById(id).ifPresent(o -> notifyShipping(o));

// ifPresentOrElse — ramificação explícita (Java 9+)
findById(id).ifPresentOrElse(
    o  -> log.info("Pedido encontrado: {}", o.getCode()),
    () -> log.warn("Pedido {} não encontrado", id)
);
```

### `Optional` em streams (`stream()` / `flatMap`)

O método `stream()` (Java 9) converte um `Optional` em um `Stream` de zero ou um elemento. É especialmente útil para filtrar listas de opcionais sem `filter(Optional::isPresent).map(Optional::get)`.

```java
List<Long> ids = List.of(1L, 2L, 99L, 3L);

// Sem stream() — verboso
List<Order> pedidos = ids.stream()
    .map(repository::findById)          // Stream<Optional<Order>>
    .filter(Optional::isPresent)
    .map(Optional::get)
    .toList();

// Com stream() + flatMap — idiomático
List<Order> pedidos = ids.stream()
    .map(repository::findById)          // Stream<Optional<Order>>
    .flatMap(Optional::stream)          // Stream<Order> — vazio para ausentes
    .toList();
```

Analogamente, ao processar um `Stream<Optional<T>>` em qualquer contexto, `flatMap(Optional::stream)` é o padrão canônico desde Java 9.

### `orElse` vs `orElseGet` (eager vs lazy)

Esta é a diferença mais cobrada em entrevistas:

| Método | Argumento | Quando avalia |
|---|---|---|
| `orElse(T other)` | valor direto | **sempre**, mesmo se o Optional estiver presente |
| `orElseGet(Supplier<T>)` | função | **somente** se o Optional estiver vazio |

```java
// orElse — buildDefault() é chamado mesmo quando o pedido existe!
Order o1 = findById(id).orElse(buildDefault());

// orElseGet — buildDefault() só é chamado quando necessário
Order o2 = findById(id).orElseGet(() -> buildDefault());
```

Se o valor default é uma constante ou objeto leve (como `BigDecimal.ZERO`, `"N/A"`), `orElse` é aceitável. Se envolve I/O, consulta ao banco ou qualquer operação custosa, **sempre** use `orElseGet`.

## Na prática

Padrão mais comum — cadeia de transformação com fallback:

```java
// Calcula total de um pedido; retorna zero se não encontrado
BigDecimal total = findById(id)
    .map(Order::getTotal)
    .orElse(BigDecimal.ZERO);
```

Lançando exceção de domínio quando a ausência é erro:

```java
Order pedido = findById(id)
    .orElseThrow(() -> new OrderNotFoundException(id));
```

Combinando `filter` + `map` + `orElseGet`:

```java
// Retorna o código do pedido se ele estiver pendente; gera código temporário caso contrário
String codigo = findById(id)
    .filter(o -> o.getStatus() == Status.PENDING)
    .map(Order::getCode)
    .orElseGet(() -> generateTemporaryCode());
```

`flatMap` para encadear dois retornos opcionais:

```java
// Desconto do pedido, se o pedido existir e tiver desconto
Optional<Discount> desconto = findById(id)
    .flatMap(Order::getDiscount);
```

## Armadilhas

**1. `Optional` como campo de classe ou parâmetro de método (anti-pattern)**

O Javadoc oficial diz explicitamente: `Optional` foi concebido como **tipo de retorno** de métodos. Usá-lo como campo torna a serialização problemática (`Optional` não implementa `Serializable`), aumenta o footprint do objeto e gera confusão sobre se o campo pode ser `null` ou apenas `Optional.empty()`. Usá-lo como parâmetro obriga o chamador a empacotar valores em `Optional.of(x)` desnecessariamente — basta sobrecarregar o método ou aceitar `null` com `@Nullable`.

```java
// ❌ Anti-pattern: Optional como campo
class OrderSummary {
    private Optional<Discount> discount;   // errado
}

// ✅ Correto: campo simples; null ou default no construtor
class OrderSummary {
    private Discount discount;   // null = sem desconto
}
```

**2. `get()` cru ou `isPresent()` + `get()` — use `map`/`orElse`**

`get()` foi marcado como "não recomendado" na documentação oficial em favor de `orElseThrow()`. O padrão `isPresent()` + `get()` é equivalente a `if (x != null)` — derrota o propósito do Optional.

```java
// ❌ Equivalente a checar null na mão
if (opt.isPresent()) {
    process(opt.get());
}

// ✅ Idiomático — cadeia funcional
opt.ifPresent(this::process);

// ❌ get() sem verificação → NoSuchElementException em runtime
String s = opt.get();

// ✅ Explícito e seguro
String s = opt.orElseThrow();
```

**3. `orElse(expensive())` sempre avalia `expensive()` — use `orElseGet`**

Mesmo quando o `Optional` contém um valor, `orElse` avalia completamente seu argumento antes de retornar. Isso pode causar consultas desnecessárias ao banco, chamadas de rede ou outros efeitos colaterais.

```java
// ❌ loadFallbackFromDatabase() é chamado sempre
Order o = findById(id).orElse(loadFallbackFromDatabase(id));

// ✅ loadFallbackFromDatabase() só é chamado quando necessário
Order o = findById(id).orElseGet(() -> loadFallbackFromDatabase(id));
```

**4. `Optional.of(null)` lança NPE — use `ofNullable`**

`Optional.of` exige um valor não-nulo. Se a origem do valor é incerta (API legada, resultado de reflexão, dado externo), use sempre `ofNullable`.

```java
String valor = legacyApi.getValue();  // pode retornar null

// ❌ Lança NullPointerException
Optional<String> opt = Optional.of(valor);

// ✅ Retorna Optional.empty() se valor for null
Optional<String> opt = Optional.ofNullable(valor);
```

## Em entrevista

### Frase pronta (inglês)

"`Optional<T>` is a container type introduced in Java 8 whose primary purpose is to be used as a method return type when there is a clear need to represent 'no result' — it makes absence explicit at the type level, rather than relying on null conventions. The idiomatic approach chains `map`, `flatMap`, and `filter` to transform the contained value without ever extracting it imperatively, and then materializes the result with `orElse`, `orElseGet`, or `orElseThrow`. One important subtlety is the eager evaluation of `orElse`: the argument is always computed, even when the Optional is present, so any expensive or side-effecting computation should be wrapped in `orElseGet` with a lambda. Anti-patterns include using Optional as a field type — which breaks serialization and adds unnecessary wrapping — using it as a method parameter — which forces callers to box values pointlessly — and calling `get()` or `isPresent()` + `get()` directly, which is semantically identical to a null check and defeats the purpose of the API."

### Vocabulário

| Termo | Definição |
|---|---|
| **container type** | tipo que encapsula zero ou um valor de outro tipo |
| **absence** | ausência de valor; representada por `Optional.empty()` |
| **eager evaluation** | avaliação imediata do argumento, independente do contexto |
| **lazy evaluation** | avaliação postergada; o `Supplier` só é invocado se necessário |
| **value-based class** | classe cujas instâncias iguais são intercambiáveis; sem identidade de referência significativa |
| **anti-pattern** | prática que parece razoável mas produz efeitos indesejados |
| **fluent chain** | encadeamento de chamadas que retornam o mesmo tipo (ou similar), formando um pipeline legível |
| **NPE** | `NullPointerException` — exceção lançada ao acessar referência nula |

## Veja também

- [[04 - Lambdas e interfaces funcionais]]
- [[07 - Operações de Stream — intermediárias e terminais]]
- [[13 - Composição funcional e funções de alta ordem]]
- [[03-Dominios/Java/Collections e Streams/index|Collections e Streams (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Dicionário de Java#Optional|Optional]]

## Referências

- Oracle. *Class Optional\<T\>*. Java SE 21 API Specification. Disponível em: <https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/Optional.html>. Acesso em: 2026-06-04.
- Oracle. *The Java Tutorials — Optional*. dev.java. Disponível em: <https://dev.java/learn/api/optional/>. Acesso em: 2026-06-04.
