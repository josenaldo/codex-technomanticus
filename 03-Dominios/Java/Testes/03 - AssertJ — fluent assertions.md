---
title: "AssertJ — fluent assertions"
created: 2026-06-11
updated: 2026-06-11
type: concept
progress: backlog
status: seedling
publish: true
fase: iniciado
tags:
  - java
  - testes
  - iniciado
  - assertj
aliases:
  - "AssertJ"
  - "fluent assertions"
---

# AssertJ — fluent assertions

> [!abstract] TL;DR
> O AssertJ entrega asserções _fluent_ — você encadeia checagens num único `assertThat(x).isNotNull().hasSize(3).contains(...)` que se lê quase como uma frase em inglês. É muito mais legível que o `assertEquals` built-in do JUnit ou os matchers do Hamcrest, e produz mensagens de erro detalhadas (mostra o esperado, o obtido e a diferença) em vez do clássico "expected true but was false". Hoje é o padrão moderno de asserção em Java: o `spring-boot-starter-test` já traz o AssertJ no classpath, então você não precisa adicionar nada para começar.

## O que é

O **AssertJ** é uma biblioteca de asserções para testes Java. Ela não substitui o JUnit nem o Mockito: ela substitui a _camada de verificação_ do teste — a parte em que, depois de exercer o código, você confere se o resultado bateu com o esperado.

O ponto de entrada é sempre o método estático `assertThat(...)`, importado de `org.assertj.core.api.Assertions`. A partir dele, o AssertJ devolve um objeto de asserção **especializado pelo tipo** do argumento: passou uma `String`, você ganha métodos como `startsWith` e `isEqualToIgnoringCase`; passou uma `List`, você ganha `hasSize` e `contains`. Cada método de asserção devolve o próprio objeto, o que permite **encadear** quantas checagens quiser.

```java
import static org.assertj.core.api.Assertions.*;
```

Esse import estático com `*` é a forma idiomática: ele traz `assertThat`, `assertThatThrownBy`, `catchThrowable`, `tuple` e companhia para o escopo do arquivo de teste.

## Por que importa

Três motivos práticos:

1. **Legibilidade.** `assertThat(orders).hasSize(2).extracting(Order::total).contains(...)` descreve a intenção do teste numa linha. O equivalente em JUnit puro exige várias linhas de `assertEquals` espalhadas, perdendo a narrativa.
2. **Mensagens de erro úteis.** Quando uma asserção fluent falha, o AssertJ diz exatamente o que esperava e o que recebeu — inclusive a posição do elemento divergente numa coleção ou o campo divergente num objeto. Isso encurta o tempo de diagnóstico.
3. **Descoberta por autocomplete.** Como cada tipo expõe métodos específicos, o IDE te mostra "o que dá pra asserir sobre uma `Optional`" assim que você digita o ponto. Você aprende a API navegando.

Para um candidato sênior, dominar AssertJ é tabuleiro de entrada: praticamente toda base Java moderna usa, e demonstrar fluência nas asserções de coleção e exceção sinaliza que você escreve testes de verdade, não `assertTrue` decorativo.

## Como funciona

### assertThat encadeado: String, Number, Collection, Map, Optional

O mesmo `assertThat` muda de personalidade conforme o tipo do argumento. Cada chamada na cadeia opera sobre o mesmo valor e devolve o objeto de asserção de volta, então a ordem é livre.

```java
// String
assertThat(customer.getName()).startsWith("Ali")
                              .endsWith("ce")
                              .isEqualToIgnoringCase("alice");

// Number
assertThat(order.total()).isGreaterThan(10)
                         .isLessThanOrEqualTo(100);

// Collection
assertThat(orders).hasSize(3)
                  .contains(firstOrder)
                  .doesNotContain(cancelledOrder);

// Map
assertThat(pricesByRegion).containsEntry("BR", 99)
                          .hasSize(2);

// Optional
assertThat(repository.findById(42L)).isPresent()
                                    .hasValue(expectedCustomer);
```

### extracting: projetar campos antes de asserir

Muitas vezes você não quer comparar objetos inteiros, só um campo deles. O `extracting` **projeta** — transforma a coleção de objetos numa coleção dos valores extraídos — e aí você aplica as asserções de coleção sobre a projeção.

```java
// extrai um único campo via method reference
assertThat(orders).extracting(Order::total)
                  .contains(50, 120);

// extrai vários campos como tuplas
assertThat(customers).extracting("name", "country")
                     .contains(tuple("Alice", "BR"),
                               tuple("Bob", "PT"));
```

A vantagem: você confere só o que importa para aquele teste, sem precisar montar objetos `Order` completos para comparar.

### Exception assertions: assertThatThrownBy / catchThrowable

AssertJ trata exceções como cidadãs de primeira classe. A forma mais comum é `assertThatThrownBy`, que recebe um lambda, captura o que ele lançar e devolve uma asserção sobre o throwable:

```java
assertThatThrownBy(() -> service.checkout(emptyCart))
    .isInstanceOf(IllegalStateException.class)
    .hasMessageContaining("empty cart");
```

Variações úteis:

```java
// estilo BDD: captura primeiro, asserta depois
Throwable thrown = catchThrowable(() -> service.checkout(emptyCart));
assertThat(thrown).isInstanceOf(IllegalStateException.class)
                  .hasMessageContaining("empty");

// foco no tipo da exceção
assertThatExceptionOfType(IllegalStateException.class)
    .isThrownBy(() -> service.checkout(emptyCart))
    .withMessageContaining("empty");

// garante que NADA é lançado
assertThatNoException().isThrownBy(() -> service.checkout(validCart));
```

### Soft assertions: acumular falhas em vez de parar na primeira

Por padrão, a primeira asserção que falha aborta o teste — você só descobre o próximo problema depois de corrigir esse e rodar de novo. As **soft assertions** acumulam todas as falhas e as reportam juntas no fim do bloco:

```java
assertSoftly(softly -> {
    softly.assertThat(order.total()).isEqualTo(120);
    softly.assertThat(order.status()).isEqualTo(Status.PAID);
    softly.assertThat(order.items()).hasSize(3);
    // todas executam; falhas saem num relatório único
});
```

Use quando as asserções são **independentes** e você quer enxergar todos os defeitos de uma vez (típico ao verificar vários campos de um mesmo objeto de resposta).

### usingRecursiveComparison: comparar objetos campo a campo (ignorando id/timestamps)

Comparar dois objetos com `isEqualTo` depende do `equals()` deles — que muitas vezes não existe ou compara por identidade. O `usingRecursiveComparison()` ignora o `equals()` e compara **campo a campo, recursivamente**, descendo em objetos aninhados. Combine com `ignoringFields(...)` para descartar campos voláteis como `id` gerado pelo banco ou `createdAt`:

```java
assertThat(savedOrder).usingRecursiveComparison()
                      .ignoringFields("id", "createdAt")
                      .isEqualTo(expectedOrder);
```

Isso é o que torna viável comparar uma entidade persistida (com `id` e timestamp preenchidos pelo banco) contra um objeto esperado montado à mão no teste.

## Na prática

```java
import static org.assertj.core.api.Assertions.*;

import java.util.List;
import org.junit.jupiter.api.Test;

class OrderServiceTest {

    @Test
    void projeta_e_verifica_totais_dos_pedidos() {
        List<Order> orders = orderService.findByCustomer(customerId);

        assertThat(orders).hasSize(2)
                          .extracting(Order::total)
                          .contains(50, 120);
    }

    @Test
    void checkout_de_carrinho_vazio_falha() {
        assertThatThrownBy(() -> orderService.checkout(emptyCart))
            .isInstanceOf(IllegalStateException.class)
            .hasMessageContaining("empty cart");
    }

    @Test
    void verifica_varios_campos_de_uma_vez() {
        Order order = orderService.place(validCart);

        assertSoftly(softly -> {
            softly.assertThat(order.total()).isEqualTo(120);
            softly.assertThat(order.status()).isEqualTo(Status.PAID);
            softly.assertThat(order.items()).hasSize(3);
        });
    }

    @Test
    void pedido_persistido_bate_com_o_esperado() {
        Order saved = orderRepository.save(newOrder);

        Order expected = new Order(customer, List.of(item), 120, Status.PAID);

        assertThat(saved).usingRecursiveComparison()
                         .ignoringFields("id", "createdAt")
                         .isEqualTo(expected);
    }
}
```

## Armadilhas

### (1) Embrulhar `equals` num `assertTrue` em vez de usar `isEqualTo`

É tentador escrever `assertThat(x.equals(y)).isTrue()` (ou o velho `assertTrue(x.equals(y))` do JUnit). O problema: você jogou fora toda a informação. Quando falha, a mensagem é o inútil **"expected true but was false"** — você não sabe qual era o `x`, qual era o `y`, nem onde diferem.

```java
// RUIM — falha vira "expected: true but was: false"
assertThat(order.equals(expected)).isTrue();
```

**Fix:** passe os objetos para o `assertThat` e deixe o AssertJ comparar. A mensagem de erro passa a mostrar esperado, obtido e a diferença.

```java
// BOM — falha mostra os dois objetos e o campo divergente
assertThat(order).isEqualTo(expected);
```

### (2) Asserções independentes que param na primeira falha

Quando você verifica vários campos de um mesmo resultado com `assertThat` comum, a primeira falha aborta o teste. Você corrige aquele campo, roda de novo, e só então descobre que o segundo campo também estava errado — um ciclo de correção lento e frustrante.

```java
// RUIM — se o total falha, você nunca vê que status e size também estão errados
assertThat(order.total()).isEqualTo(120);
assertThat(order.status()).isEqualTo(Status.PAID);   // não chega aqui
assertThat(order.items()).hasSize(3);                 // nem aqui
```

**Fix:** quando as asserções são independentes (verificam aspectos diferentes do mesmo objeto), agrupe num `assertSoftly`. Todas rodam e as falhas saem juntas num único relatório.

```java
// BOM — todas executam, relatório único com todas as falhas
assertSoftly(softly -> {
    softly.assertThat(order.total()).isEqualTo(120);
    softly.assertThat(order.status()).isEqualTo(Status.PAID);
    softly.assertThat(order.items()).hasSize(3);
});
```

## Em entrevista

### Frase pronta (inglês)

> "I default to AssertJ for the verification phase of my tests because the fluent API reads almost like a sentence and the failure messages are far more informative than JUnit's built-in assertions or Hamcrest. Instead of `assertTrue(a.equals(b))`, which fails with a useless 'expected true but was false', I write `assertThat(a).isEqualTo(b)` and get the actual diff. For collections I lean on `extracting` to project just the fields I care about, I use `assertThatThrownBy` to assert on exceptions, and `usingRecursiveComparison().ignoringFields(...)` to compare persisted entities against expected objects while ignoring generated ids and timestamps. When I'm checking several independent fields of one result, I wrap them in soft assertions so a single run surfaces every failure at once."

### Vocabulário

| Termo (inglês)              | Tradução / sentido                                                        |
| --------------------------- | ------------------------------------------------------------------------- |
| fluent assertion            | asserção encadeável que se lê como uma frase                              |
| chaining                    | encadeamento de chamadas sobre o mesmo objeto de asserção                 |
| extracting / projection     | projetar (extrair) campos de objetos antes de asserir                     |
| soft assertions             | acumular todas as falhas e reportá-las juntas no fim                      |
| recursive comparison        | comparação campo a campo, recursiva, ignorando `equals()`                 |
| failure message             | mensagem de erro que mostra esperado, obtido e a diferença                |

## Veja também

- [[03-Dominios/Java/Testes/02 - JUnit 5 — anatomia, lifecycle e o padrão AAA|JUnit 5]]
- [[03-Dominios/Java/Testes/06 - Mockito — mocks, stubbing e matchers|Mockito]]
- [[03-Dominios/Java/Testes/index|Testes (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Dicionário de Java]]

## Referências

- AssertJ Core — Documentação oficial: https://assertj.github.io/doc/#assertj-core
