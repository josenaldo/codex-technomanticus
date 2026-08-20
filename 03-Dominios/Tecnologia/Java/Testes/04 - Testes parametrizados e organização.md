---
title: "Testes parametrizados e organização"
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
  - junit
  - parametrizados
aliases:
  - "testes parametrizados"
  - "@ParameterizedTest"
---

# Testes parametrizados e organização

> [!abstract] TL;DR
> `@ParameterizedTest` roda o mesmo corpo de teste com vários inputs, vindos de `@ValueSource`, `@CsvSource` ou `@MethodSource`. `@Nested` agrupa cenários relacionados em classes internas, dando hierarquia e legibilidade ao relatório. `@Tag` rotula testes para execução seletiva no CI (rodar só `unit`, pular `slow`). E `@ExtendWith` é o ponto de extensão que pluga comportamento extra no ciclo de vida do JUnit 5.

## O que é

Três eixos diferentes, mas que aparecem juntos no dia a dia de quem escreve testes em JUnit 5:

- **Parametrização**: em vez de copiar e colar um teste cinco vezes mudando só o input, você escreve uma vez e o JUnit injeta cada conjunto de argumentos como uma invocação separada. A anotação é `@ParameterizedTest` (no lugar de `@Test`), alimentada por um *argument source*.
- **Organização**: `@Nested` permite escrever classes internas que agrupam testes de um mesmo contexto ("quando o pedido está pendente", "quando o pedido foi pago"). O relatório fica em árvore, refletindo a estrutura.
- **Seletividade**: `@Tag` carimba um rótulo no teste. O build então decide quais rótulos rodar.

> Parametrização precisa de uma dependência a mais: `junit-jupiter-params`, além do `junit-jupiter-api`.

## Por que importa

Sem parametrização, validar uma regra de classificação de faixas (0–18, 19–64, 65+) vira três métodos quase idênticos. Multiplique isso por dezenas de regras e o arquivo de teste fica maior e mais frágil que a própria regra. `@ParameterizedTest` colapsa esse ruído: uma intenção, vários dados.

`@Nested` resolve o problema oposto — quando a suíte cresce e vira uma lista plana de 40 métodos sem hierarquia. Agrupar por cenário transforma o relatório de teste em documentação viva do comportamento.

`@Tag` é o que mantém o CI rápido: testes unitários (milissegundos) rodam a cada push; testes lentos de integração (que sobem banco, container) rodam num estágio separado. Sem rótulos, ou você roda tudo sempre (lento) ou nada (arriscado).

## Como funciona

### @ParameterizedTest + sources (ValueSource / CsvSource / MethodSource / EnumSource)

`@ParameterizedTest` substitui `@Test` e exige pelo menos uma fonte de argumentos:

- `@ValueSource` — uma lista simples de literais de um único tipo (`ints`, `strings`, `longs`...). Cada valor vira uma invocação. Bom para "este input não pode lançar exceção".
- `@CsvSource` — linhas de CSV inline, cada linha mapeada para os parâmetros do método na ordem. Bom para pares input/output (`"19, ADULT"`).
- `@MethodSource` — aponta para um método fábrica que retorna `Stream`, `Collection` ou array de argumentos. Bom quando os dados são construídos em código (objetos, não literais).
- `@EnumSource` — injeta as constantes de um enum como argumentos. Bom para "este teste deve valer para todo `OrderStatus`".
- `@CsvFileSource` — igual ao `@CsvSource`, mas lê as linhas de um arquivo `.csv` no classpath. Bom para grandes massas de dados.

### @Nested: agrupar cenários relacionados

`@Nested` marca uma classe interna **não-estática** como um grupo de testes. Cada classe interna pode ter seu próprio `@BeforeEach`, montando o contexto daquele cenário uma vez. Combinada com `@DisplayName`, produz um relatório legível em árvore:

```
OrderTest
└─ when order is pending
   ├─ allows cancellation
   └─ rejects shipment
```

A não-estaticidade é proposital: a classe interna tem acesso ao estado da classe externa, então o setup compartilhado flui de fora para dentro.

### @Tag e execução seletiva (unit vs slow vs integration)

`@Tag("unit")` carimba um rótulo (texto livre) na classe ou no método. O rótulo só ganha efeito quando o *runner* filtra por ele. No Maven Surefire:

- `groups` — roda **somente** os testes com os rótulos listados.
- `excludedGroups` — roda tudo **menos** os rótulos listados.

Esses parâmetros podem vir da linha de comando (`-Dgroups=...`) ou da configuração do plugin no `pom.xml`. Assim o mesmo código de teste serve a vários pipelines: o rápido roda `unit`, o noturno roda tudo.

### @ExtendWith: o ponto de extensão do JUnit 5

`@ExtendWith` registra uma *extension* de forma declarativa — é o gancho que pluga comportamento no ciclo de vida (antes/depois de cada teste, resolução de parâmetros, callbacks). É como bibliotecas como Mockito (`@ExtendWith(MockitoExtension.class)`) ou Spring (`@ExtendWith(SpringExtension.class)`) se integram ao JUnit. A anotação é **herdada**, então aplicá-la numa classe base propaga a extension às filhas. Por enquanto, basta saber que ela existe e é o mecanismo de plugin do framework.

## Na prática

```java
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import org.junit.jupiter.params.provider.MethodSource;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;
import java.util.stream.Stream;
import static org.junit.jupiter.api.Assertions.*;

class OrderTest {

    enum AgeBracket { MINOR, ADULT, SENIOR }

    AgeBracket classify(int age) {
        if (age < 19) return AgeBracket.MINOR;
        if (age < 65) return AgeBracket.ADULT;
        return AgeBracket.SENIOR;
    }

    // (1) @CsvSource: pares input/output inline
    @ParameterizedTest
    @CsvSource({
        "5,  MINOR",
        "18, MINOR",
        "19, ADULT",
        "64, ADULT",
        "65, SENIOR"
    })
    void classifiesAgeIntoBracket(int age, AgeBracket expected) {
        assertEquals(expected, classify(age));
    }

    // (2) @MethodSource: dados construídos em código
    @ParameterizedTest
    @MethodSource("validCustomerNames")
    void acceptsNonBlankCustomerName(String name) {
        assertFalse(name.isBlank());
    }

    static Stream<String> validCustomerNames() {
        return Stream.of("Acme Corp", "Globex", "Initech");
    }

    // (3) @Nested: agrupando um cenário
    @Nested
    @DisplayName("when order is pending")
    class WhenPending {

        @Test
        void allowsCancellation() {
            OrderStatus status = OrderStatus.PENDING;
            assertTrue(status.canBeCancelled());
        }

        @Test
        void rejectsShipment() {
            OrderStatus status = OrderStatus.PENDING;
            assertFalse(status.canBeShipped());
        }
    }
}

enum OrderStatus {
    PENDING, PAID, SHIPPED;

    boolean canBeCancelled() { return this == PENDING; }
    boolean canBeShipped()   { return this == PAID; }
}
```

```bash
# roda só os testes marcados com @Tag("unit")
mvn test -Dgroups="unit"

# roda tudo, menos os marcados com @Tag("slow")
mvn test -DexcludedGroups="slow"
```

## Armadilhas

### (1) @MethodSource apontando para método de instância sem PER_CLASS

`@MethodSource` espera, por padrão, um método fábrica **estático**. Se você apontar para um método de instância sem ajustar o ciclo de vida, o JUnit não consegue invocá-lo (a instância de teste ainda não existe quando os argumentos são resolvidos) e o teste falha na coleta de argumentos.

```java
// QUEBRA: método de instância, mas classe usa o lifecycle padrão (PER_METHOD)
class OrderTest {
    @ParameterizedTest
    @MethodSource("names")
    void t(String n) { /* ... */ }

    Stream<String> names() { return Stream.of("Acme", "Globex"); } // não-static
}
```

**Fix:** ou torne o método fábrica `static`, ou anote a classe com `@TestInstance(TestInstance.Lifecycle.PER_CLASS)` — aí o JUnit cria uma única instância por classe e consegue chamar o método de instância.

```java
@TestInstance(TestInstance.Lifecycle.PER_CLASS)
class OrderTest {
    @ParameterizedTest
    @MethodSource("names")
    void t(String n) { /* ... */ }

    Stream<String> names() { return Stream.of("Acme", "Globex"); } // agora OK
}
```

### (2) Parametrizar quando os cenários mereciam testes nomeados distintos

Parametrização é para **mesmo comportamento, dado diferente**. Quando os "casos" na verdade exercitam lógicas distintas, empacotá-los num único `@ParameterizedTest` esconde a intenção: um nome genérico cobre comportamentos que mereciam nomes próprios, e quando um caso quebra fica difícil entender o que ele garantia.

```java
// CHEIRO: a "tabela" mistura regras conceitualmente diferentes
@ParameterizedTest
@CsvSource({
    "PENDING, true",   // pode cancelar
    "PAID,    true",   // pode enviar (!! outra regra, outro verbo)
    "SHIPPED, false"   // já enviado
})
void orderRule(OrderStatus status, boolean expected) { /* qual regra? */ }
```

**Fix:** quando o que muda não é só o dado mas a regra, separe em testes nomeados (idealmente sob um `@Nested` por cenário). Use parametrização apenas para a faixa de dados que exercita **a mesma** asserção.

```java
@Nested class Cancellation {
    @ParameterizedTest
    @EnumSource(value = OrderStatus.class, names = "PENDING")
    void onlyPendingCanBeCancelled(OrderStatus s) { assertTrue(s.canBeCancelled()); }
}
```

## Em entrevista

### Frase pronta (inglês)

> I reach for `@ParameterizedTest` when I have the same assertion across a range of inputs — it removes copy-paste and makes the test table read like a spec. For inline pairs I use `@CsvSource`; when the arguments are objects built in code I use `@MethodSource`, keeping the factory method `static` unless the class is on the `PER_CLASS` lifecycle. To keep suites readable I group related scenarios with `@Nested` and `@DisplayName`, and I tag tests with `@Tag` so the CI can run fast unit tests on every push and defer the slow integration ones with Surefire's `groups` and `excludedGroups`.

### Vocabulário

| Termo (EN) | Significado |
| --- | --- |
| parameterized test | teste rodado várias vezes com inputs diferentes |
| argument source | fonte de dados que alimenta o teste (`@ValueSource`, `@CsvSource`...) |
| factory method | método que produz os argumentos (usado por `@MethodSource`) |
| nested test class | classe interna que agrupa cenários (`@Nested`) |
| tag / tagging | rótulo para filtrar execução (`@Tag`) |
| selective execution | rodar só um subconjunto de testes (groups/excludedGroups) |
| extension point | gancho de plugin do framework (`@ExtendWith`) |
| test lifecycle | quando a instância de teste é criada (PER_METHOD / PER_CLASS) |

## Veja também

- [[03-Dominios/Tecnologia/Java/Testes/02 - JUnit 5 — anatomia, lifecycle e o padrão AAA|JUnit 5]]
- [[03-Dominios/Tecnologia/Java/Testes/05 - Test data builders e fixtures|Test data builders e fixtures]]
- [[03-Dominios/Tecnologia/Java/Testes/index|Testes (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java]] (verbetes @ParameterizedTest / @Nested)

## Referências

- JUnit 5 User Guide — Writing Tests (Parameterized Tests, Tagging and Filtering, Nested Tests, Extensions): https://docs.junit.org/current/user-guide/
