---
title: "JUnit 5 — anatomia, lifecycle e o padrão AAA"
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
aliases:
  - "JUnit 5"
  - "JUnit Jupiter"
---

# JUnit 5 — anatomia, lifecycle e o padrão AAA

> [!abstract] TL;DR
> JUnit 5 (Jupiter) é o framework de testes moderno do ecossistema Java. Cada teste é um método anotado com `@Test` dentro de uma classe comum, com hooks de lifecycle (`@BeforeEach`, `@AfterEach`, `@BeforeAll`, `@AfterAll`) para preparar e limpar o ambiente. O corpo do teste segue o padrão **AAA** (Arrange-Act-Assert, ou given/when/then): monta o cenário, executa a ação, verifica o resultado. `@DisplayName` dá nomes legíveis com espaços e acentos. Por padrão, uma **nova instância da classe é criada por método de teste**, isolando estado.

## O que é

JUnit 5 é a versão atual do framework de testes mais usado em Java. Diferente das versões anteriores (que eram um único `.jar`), o JUnit 5 é composto por **três subprojetos** que trabalham juntos. A baseline mínima é Java 8, mas o ecossistema moderno (Spring Boot 3, records, etc.) opera sobre **Java 17+**.

Na prática, escrever um teste com JUnit 5 significa: criar uma classe de teste (sem herança nem interface obrigatória), declarar métodos anotados com `@Test`, e usar **asserções** para afirmar que o código sob teste se comporta como esperado. O framework descobre, instancia e executa esses métodos automaticamente.

## Por que importa

Testar à mão (rodar o programa e olhar a saída) não escala e não documenta. Um teste de JUnit é **executável, repetível e versionado**: roda no CI a cada commit, falha de forma visível quando uma regressão entra, e serve de documentação viva do comportamento esperado.

Conhecer a **anatomia** (as três partes), o **lifecycle** (quando cada hook roda) e o **padrão AAA** (como estruturar o corpo) é o vocabulário básico para ler e escrever qualquer suíte de testes Java. Em entrevista, é o piso: espera-se que a pessoa saiba a diferença entre `@BeforeEach` e `@BeforeAll`, e por que o framework cria uma instância nova por teste.

## Como funciona

### Platform / Jupiter / Vintage: as três partes

Conforme a documentação oficial, **JUnit 5 = JUnit Platform + JUnit Jupiter + JUnit Vintage**. Cada parte tem um papel:

- **JUnit Platform** — a fundação. Define a API `TestEngine` para descobrir e rodar testes, e fornece o `Launcher` que ferramentas de build (Gradle, Maven) e IDEs usam para disparar a execução. É a camada que faz testes rodarem na JVM.
- **JUnit Jupiter** — o modelo de programação **novo**. É onde vivem `@Test`, `@BeforeEach`, `@DisplayName` e as asserções. Quando se diz "escrever testes em JUnit 5", quase sempre se está usando Jupiter. Inclui também o `JupiterTestEngine` que roda esses testes na Platform.
- **JUnit Vintage** — uma ponte de **retrocompatibilidade**. Fornece um `TestEngine` que roda testes legados de JUnit 3 e JUnit 4 na Platform, permitindo migração gradual sem reescrever tudo de uma vez.

Resumindo: a Platform é o motor, o Jupiter é a API moderna, o Vintage é o adaptador para o passado.

### O lifecycle: @BeforeAll / @BeforeEach / @AfterEach / @AfterAll

O lifecycle controla **quando** o código de preparação e limpeza roda em relação aos métodos de teste:

| Anotação | Quando roda | Static por default? |
| --- | --- | --- |
| `@BeforeAll` | **Uma vez**, antes de todos os testes da classe | Sim |
| `@BeforeEach` | Antes de **cada** método de teste | Não |
| `@Test` | É o método de teste em si | — |
| `@AfterEach` | Depois de **cada** método de teste | Não |
| `@AfterAll` | **Uma vez**, depois de todos os testes da classe | Sim |

A ordem de execução para uma classe com dois testes é: `@BeforeAll` → (`@BeforeEach` → teste 1 → `@AfterEach`) → (`@BeforeEach` → teste 2 → `@AfterEach`) → `@AfterAll`.

A documentação é explícita: métodos `@BeforeAll` e `@AfterAll` **devem ser `static`** a não ser que o lifecycle "per-class" seja usado (mais sobre isso abaixo). Use `@BeforeEach`/`@AfterEach` para setup/teardown que precisa de estado fresco por teste; use `@BeforeAll`/`@AfterAll` para recursos caros e compartilhados (abrir/fechar uma conexão, subir um container).

### AAA (Arrange-Act-Assert) e convenções de nome

O padrão **AAA** estrutura o corpo de um teste em três blocos visuais:

1. **Arrange** (given) — monta o cenário: cria objetos, configura dependências, prepara os dados de entrada.
2. **Act** (when) — executa **a única ação** sob teste, geralmente uma chamada de método.
3. **Assert** (then) — verifica o resultado com asserções: o retorno é o esperado? O estado mudou? A exceção certa foi lançada?

A versão "given/when/then" (vinda do BDD) é o mesmo esqueleto com outro vocabulário. A regra de ouro: **um teste, uma asserção lógica de comportamento** — não embuta cinco cenários diferentes num método só.

Sobre nomes: nomes de método em Java não têm espaços, então testes ganham nomes como `returnsTotalWhenOrderHasItems`. Para legibilidade, `@DisplayName("retorna o total quando o pedido tem itens")` permite **nomes legíveis com espaços e acentos**, exibidos no relatório do IDE e do CI. Convenções comuns de nome de método: `metodo_condicao_resultado` ou `should_<resultado>_when_<condicao>`.

### Per-method vs per-class (@TestInstance) e por que o default isola estado

Por padrão (`Lifecycle.PER_METHOD`), o JUnit **cria uma nova instância da classe de teste antes de executar cada método de teste**. A documentação justifica: isso permite que cada teste rode em **isolamento** e evita efeitos colaterais de estado mutável compartilhado entre testes. Um campo de instância modificado no teste A não vaza para o teste B — porque o teste B roda num objeto novo.

`@TestInstance(Lifecycle.PER_CLASS)` muda isso: o JUnit usa **uma única instância para todos os métodos** da classe. Nesse modo, segundo a documentação, torna-se possível declarar `@BeforeAll` e `@AfterAll` em **métodos não-static** (e em `default` methods de interface), e o estado de instância é **compartilhado** entre os testes.

`PER_CLASS` é útil para evitar reconstruir setup caro a cada teste, mas tem um custo: como o estado é compartilhado, **um teste pode contaminar o outro** se não houver reset cuidadoso. Por isso o default `PER_METHOD` é o caminho seguro para a maioria dos casos.

Anotações de controle de execução que complementam o lifecycle:

- `@Disabled("motivo")` — desabilita uma classe ou método de teste (pula a execução).
- `@Timeout` — falha o teste se a execução exceder uma duração dada.
- `@DisabledOnOs` / `@EnabledOnJre` — execução condicional por sistema operacional ou por versão da JRE.

## Na prática

Uma classe de teste neutra exercitando o lifecycle completo, `@DisplayName` e o padrão AAA:

```java
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

@DisplayName("OrderService")
class OrderServiceTest {

    private OrderService service;

    @BeforeAll
    static void setUpClass() {
        // Roda uma vez antes de todos os testes (precisa ser static no default).
        // Bom lugar para recursos caros e compartilhados.
    }

    @BeforeEach
    void setUp() {
        // Roda antes de CADA teste: estado fresco, sem vazamento entre testes.
        service = new OrderService();
    }

    @Test
    @DisplayName("calcula o total somando os itens do pedido")
    void calculatesTotalFromItems() {
        // Arrange (given): monta o cenário
        Order order = new Order();
        order.addItem(new Item("Book", 30.00));
        order.addItem(new Item("Pen", 5.00));

        // Act (when): a única ação sob teste
        double total = service.total(order);

        // Assert (then): verifica o resultado
        assertEquals(35.00, total);
    }

    @Test
    @DisplayName("considera um pedido sem itens como vazio")
    void treatsEmptyOrderAsEmpty() {
        Order order = new Order();

        boolean empty = service.isEmpty(order);

        assertTrue(empty);
    }

    @AfterEach
    void tearDown() {
        // Roda depois de cada teste: limpeza por teste.
        service = null;
    }

    @AfterAll
    static void tearDownClass() {
        // Roda uma vez depois de todos os testes (static no default).
    }
}
```

## Armadilhas

### (1) Estado compartilhado entre testes com PER_CLASS sem reset

Com `@TestInstance(Lifecycle.PER_CLASS)`, todos os testes rodam na **mesma instância**. Se um teste muta um campo e o próximo não o reseta, a ordem de execução passa a importar — um teste contamina o outro, e a suíte fica "verde por acidente" ou falha de forma intermitente.

```java
@TestInstance(TestInstance.Lifecycle.PER_CLASS)
class CartTest {

    private final Cart cart = new Cart(); // compartilhado entre todos os testes!

    @Test
    void addsItem() {
        cart.add(new Item("Book", 30.00));
        assertEquals(1, cart.size());
    }

    @Test
    void startsEmpty() {
        // FALHA se addsItem() rodou antes: cart já tem 1 item.
        assertEquals(0, cart.size());
    }
}
```

**Fix:** prefira o default `PER_METHOD` (instância nova por teste), ou, se `PER_CLASS` for necessário, **resete o estado em `@BeforeEach`**:

```java
@BeforeEach
void reset() {
    cart.clear(); // garante estado limpo antes de cada teste
}
```

### (2) @BeforeAll não-static sem PER_CLASS

No lifecycle default (`PER_METHOD`), `@BeforeAll` e `@AfterAll` **precisam ser `static`**. Declarar um `@BeforeAll` de instância (não-static) sem ativar `PER_CLASS` resulta em erro de configuração — o método não roda como esperado e o JUnit reporta falha.

```java
class ReportServiceTest {

    @BeforeAll
    void loadFixtures() { // ERRO: não-static no lifecycle PER_METHOD
        // ...
    }
}
```

**Fix:** ou torne o método `static`...

```java
@BeforeAll
static void loadFixtures() {
    // ...
}
```

...ou ative o lifecycle per-class para permitir `@BeforeAll` não-static:

```java
@TestInstance(TestInstance.Lifecycle.PER_CLASS)
class ReportServiceTest {

    @BeforeAll
    void loadFixtures() { // OK com PER_CLASS
        // ...
    }
}
```

## Em entrevista

### Frase pronta (inglês)

> JUnit 5 is split into three parts: the **Platform** is the engine that launches tests on the JVM, **Jupiter** is the modern programming model where `@Test`, the lifecycle hooks, and assertions live, and **Vintage** bridges legacy JUnit 3 and 4 tests. Each test method runs in a **fresh instance of the test class by default** — that's the `PER_METHOD` lifecycle — which isolates state and avoids side effects bleeding between tests. I structure the body with **Arrange-Act-Assert**: set up the scenario, invoke the single action under test, then assert the outcome, and I use `@DisplayName` for readable, human-friendly test names in the reports.

### Vocabulário

| Termo | Significado |
| --- | --- |
| **Test fixture** | O ambiente fixo (objetos, dados) montado antes do teste; preparado nos hooks `@BeforeEach`/`@BeforeAll` |
| **Lifecycle hook** | Método de setup/teardown (`@BeforeEach`, `@AfterAll`, etc.) que roda em torno dos testes |
| **Test instance lifecycle** | Política de quando o JUnit instancia a classe de teste: per-method (default) ou per-class |
| **Arrange-Act-Assert (AAA)** | Padrão de estruturar o corpo do teste em três blocos: cenário, ação, verificação |
| **Assertion** | Afirmação que faz o teste falhar se a condição esperada não for verdadeira |
| **Test isolation** | Garantia de que um teste não afeta o resultado de outro; vem da instância nova por método |
| **Setup / Teardown** | Preparação antes e limpeza depois de um teste, nos hooks de lifecycle |

## Veja também

- [[03-Dominios/Java/Testes/01 - O que é testar em Java — a pirâmide e o stack moderno|O que é testar em Java]]
- [[03-Dominios/Java/Testes/03 - AssertJ — fluent assertions|AssertJ]]
- [[03-Dominios/Java/Testes/04 - Testes parametrizados e organização|Testes parametrizados e organização]]
- [[03-Dominios/Java/Testes/index|Testes (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Dicionário de Java]] (verbetes JUnit 5 (Jupiter) / AAA (Arrange-Act-Assert))

## Referências

- JUnit 5 User Guide — Writing Tests: https://docs.junit.org/current/user-guide/ (seções Annotations, Test Instance Lifecycle, Display Names; consultado em 2026-06-11)
