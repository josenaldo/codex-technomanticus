---
title: "Mockito — verify, ArgumentCaptor e quando NÃO mockar"
created: 2026-06-11
updated: 2026-06-11
type: concept
progress: backlog
status: seedling
publish: true
fase: adepto
tags:
  - java
  - testes
  - adepto
  - mockito
aliases:
  - "Mockito verify"
  - "ArgumentCaptor"
---

# Mockito — verify, ArgumentCaptor e quando NÃO mockar

> [!abstract] TL;DR
> `verify` confere que um mock foi chamado como esperado — `times(n)`, `never()`, `atLeast(n)`, `atMost(n)`, em ordem com `InOrder`, e sem sobras com `verifyNoMoreInteractions`. `ArgumentCaptor` captura o argumento que passou pelo mock pra você asserir os detalhes dele depois. E vem a regra de ouro: mocke colaboradores (que fazem I/O, rede, banco), **não** mocke value objects simples — e prefira escrever código testável (injetar um `Clock`) a recorrer a static mocking.

## O que é

Um mock tem dois lados. No lado da **entrada** você faz stubbing: "quando chamarem isto, devolva aquilo" (`when(...).thenReturn(...)`). No lado da **saída** você faz verificação: "confirme que este método foi chamado, com estes argumentos, esta quantidade de vezes". Esse segundo lado é o território do `verify`.

`verify(mock)` é uma asserção de **interação**. Diferente de um `assertEquals` (que olha um valor de retorno), ele olha o *comportamento*: o objeto sob teste conversou com seus colaboradores do jeito esperado? O `ArgumentCaptor` é o complemento natural: ele intercepta o argumento real que foi passado pro mock, guardando uma referência pra você inspecionar campo a campo.

O **static mocking** (`mockStatic`) é uma capacidade mais recente — a partir do Mockito 3.4 e plenamente parte do Mockito 5 — que permite fingir o retorno de métodos estáticos (como `Instant.now()`) dentro de um escopo controlado, dispensando o antigo PowerMock.

## Por que importa

Verificação de interação é o que torna um **mock** diferente de um **stub**: o stub só responde, o mock também *cobra*. Quando o efeito do método sob teste é "chamar outra coisa" — salvar no repositório, publicar um evento, enviar uma notificação — não há valor de retorno pra asserir. O `verify` é o único jeito de provar que aquilo aconteceu.

O `ArgumentCaptor` resolve um problema que matchers inline não resolvem bem: asserir o **conteúdo** de um objeto complexo construído dentro do método sob teste. Em vez de escrever um matcher gigante e ilegível, você captura o objeto e usa as asserções normais da sua biblioteca de testes.

E a parte mais valiosa pra um pleno/sênior é o discernimento de *quando não usar nada disso*. Excesso de `verify` produz testes frágeis que quebram a cada refatoração interna. Mockar value objects produz testes que testam o próprio mock. Saber a fronteira é o que separa um teste que protege de um teste que atrapalha.

## Como funciona

### verify: times / never / atLeast + InOrder + verifyNoMoreInteractions

A forma básica `verify(mock).metodo(args)` verifica exatamente **uma** chamada. Pra outras cardinalidades, passa-se um `VerificationMode` como segundo argumento:

| Modo | Significado |
| --- | --- |
| `times(n)` | exatamente `n` chamadas (default é `times(1)`) |
| `never()` | nenhuma chamada (atalho pra `times(0)`) |
| `atLeastOnce()` | uma ou mais |
| `atLeast(n)` | no mínimo `n` |
| `atMost(n)` | no máximo `n` |

```java
verify(repository, times(2)).save(any());
verify(notifier, never()).send(any());
verify(repository, atLeast(1)).findById(anyLong());
```

Quando a **ordem** entre chamadas importa, use `InOrder`:

```java
InOrder inOrder = inOrder(repository, eventBus);
inOrder.verify(repository).save(order);
inOrder.verify(eventBus).publish(any(OrderCreated.class));
```

E `verifyNoMoreInteractions(mock)` falha se houver qualquer chamada ao mock que você ainda não verificou — útil pra garantir que *nada além* do esperado aconteceu. Há ainda `verifyNoInteractions(mock)`, que afirma que o mock nunca foi tocado.

### ArgumentCaptor: capturar e asserir o argumento passado

Quando o método sob teste **constrói** o argumento internamente, você não tem como compará-lo por igualdade na chamada — ele nasce dentro da caixa-preta. O `ArgumentCaptor` resolve isso: ele entra no lugar do matcher na chamada `verify` e *segura* o objeto real.

O fluxo tem três passos:

1. `ArgumentCaptor<Order> captor = ArgumentCaptor.forClass(Order.class);`
2. usar `captor.capture()` dentro do `verify`: `verify(repository).save(captor.capture());`
3. recuperar com `captor.getValue()` (último valor) ou `captor.getAllValues()` (lista, quando houve várias chamadas).

A partir daí você assere o objeto capturado com as asserções normais. Importante: `capture()` é chamado **dentro** do `verify`, nunca no `when`.

### Static mocking sem PowerMock (mockStatic, Mockito 5+)

Métodos estáticos como `Instant.now()` ou `UUID.randomUUID()` não passam por uma instância, então não dá pra injetá-los como mock comum. Historicamente isso exigia PowerMock (lento, frágil, acoplado a versões). Desde o Mockito 3.4, e consolidado no Mockito 5, existe `mockStatic(Classe.class)`, que devolve um `MockedStatic<>` — um recurso **escopado** que deve viver dentro de um `try-with-resources`:

```java
try (MockedStatic<Instant> mockedInstant = mockStatic(Instant.class)) {
    Instant fixed = Instant.parse("2026-01-01T00:00:00Z");
    mockedInstant.when(Instant::now).thenReturn(fixed);
    // ... aqui dentro, Instant.now() devolve fixed
}
// fora do bloco, Instant.now() volta ao normal
```

O `try-with-resources` é essencial: o `close()` automático desfaz o mock estático. Sem ele, o mock vaza pra outros testes que rodem na mesma thread/JVM. Ainda assim, static mocking é a última opção — a próxima seção mostra a alternativa preferível.

### Quando NÃO mockar: value objects e código testável (injetar Clock/Supplier)

A heurística: **mocke colaboradores, não dados.** Colaboradores são objetos com comportamento e dependências externas — `OrderRepository`, um cliente HTTP, um gateway de pagamento. Value objects são estruturas de dados simples — um `Order`, um `Money`, um `CustomerId`. Mockar um value object é testar o mock, não o código.

Para tempo e aleatoriedade, a saída elegante não é `mockStatic` — é tornar a dependência **explícita**. Em vez de chamar `Instant.now()` diretamente, injete um `java.time.Clock` no construtor. No teste, passe um `Clock.fixed(...)` e o tempo vira determinístico sem nenhum mock. O mesmo vale pra aleatoriedade via um `Supplier<UUID>` injetado.

```java
class OrderService {
    private final Clock clock;
    OrderService(OrderRepository repo, Clock clock) { /* ... */ }
    // usa clock.instant() em vez de Instant.now()
}
```

Isso é design dirigido por testabilidade: o código fica mais limpo *e* mais fácil de testar ao mesmo tempo.

## Na prática

```java
import static org.mockito.Mockito.*;
import static org.assertj.core.api.Assertions.assertThat;
import org.mockito.ArgumentCaptor;
import org.mockito.MockedStatic;
import java.time.*;

class OrderServiceTest {

    OrderRepository repository = mock(OrderRepository.class);

    // 1) ArgumentCaptor: capturar e asserir o que foi salvo
    @Test
    void salvaPedidoComStatusInicial() {
        Clock clock = Clock.fixed(Instant.parse("2026-01-01T00:00:00Z"), ZoneOffset.UTC);
        OrderService service = new OrderService(repository, clock);

        service.place(new Customer("c-1"), 3);

        ArgumentCaptor<Order> captor = ArgumentCaptor.forClass(Order.class);
        verify(repository).save(captor.capture());

        Order saved = captor.getValue();
        assertThat(saved.status()).isEqualTo(OrderStatus.PLACED);
        assertThat(saved.createdAt()).isEqualTo(Instant.parse("2026-01-01T00:00:00Z"));
    }

    // 2) Clock injetado: tempo determinístico SEM static mock (preferível)
    @Test
    void usaRelogioInjetado() {
        Clock clock = Clock.fixed(Instant.parse("2026-06-11T12:00:00Z"), ZoneOffset.UTC);
        OrderService service = new OrderService(repository, clock);

        assertThat(service.timestamp()).isEqualTo(Instant.parse("2026-06-11T12:00:00Z"));
    }

    // 3) Static mocking escopado: só quando NÃO der pra injetar
    @Test
    void mockaInstantQuandoNaoHaInjecao() {
        Instant fixed = Instant.parse("2026-06-11T12:00:00Z");
        try (MockedStatic<Instant> mocked = mockStatic(Instant.class)) {
            mocked.when(Instant::now).thenReturn(fixed);
            assertThat(Instant.now()).isEqualTo(fixed);
        }
        // fora do try, Instant.now() volta ao real
    }
}
```

## Armadilhas

### (1) Verificar contagem acoplada à implementação

`verify(repository, times(3)).save(any())` amarra o teste a *como* o código faz o trabalho, não a *o que* ele entrega. Se uma refatoração trocar três `save` por um `saveAll`, o teste quebra sem que nenhum comportamento observável tenha mudado — é um falso positivo de regressão.

```java
// FRÁGIL: conta chamadas de implementação
verify(repository, times(3)).save(any());
```

**Fix**: verifique o **efeito observável**, não a mecânica. Se o que importa é que três pedidos foram persistidos, capture e assere os pedidos; se a quantidade não é a regra de negócio, não a verifique. Reserve contagens exatas para casos onde a cardinalidade *é* o requisito (ex.: "envie exatamente um e-mail").

```java
ArgumentCaptor<Order> captor = ArgumentCaptor.forClass(Order.class);
verify(repository, atLeastOnce()).save(captor.capture());
assertThat(captor.getAllValues()).hasSize(3);
```

### (2) Mockar um value object

`mock(Order.class)` para um objeto que é só dados (campos, alguns getters, sem dependências externas) cria um mock que devolve `null`/zero por padrão e exige stubbing de cada getter. Você acaba testando o mock que você mesmo configurou, não o código real.

```java
// ERRADO: Order é simples, mockar só esconde bugs reais
Order order = mock(Order.class);
when(order.total()).thenReturn(BigDecimal.TEN);
```

**Fix**: use uma instância real. Value objects são baratos de construir e seu comportamento real é exatamente o que você quer exercitar.

```java
Order order = new Order(new Customer("c-1"), 3); // real
```

### (3) mockStatic sem try-with-resources

Se você abrir `mockStatic(Instant.class)` e guardar o `MockedStatic` num campo (ou esquecer de fechá-lo), o mock estático permanece ativo após o teste. Como o registro é por thread na JVM, o próximo teste que chamar `Instant.now()` recebe o valor falso — produzindo falhas intermitentes difíceis de rastrear, dependentes da ordem de execução.

```java
// VAZA: nunca fecha, contamina os próximos testes
MockedStatic<Instant> mocked = mockStatic(Instant.class);
mocked.when(Instant::now).thenReturn(fixed);
// ...sem close()
```

**Fix**: sempre use `try-with-resources`, que garante o `close()` (e o desregistro) mesmo se uma asserção falhar no meio do bloco.

```java
try (MockedStatic<Instant> mocked = mockStatic(Instant.class)) {
    mocked.when(Instant::now).thenReturn(fixed);
    // ...
}
```

## Em entrevista

### Frase pronta (inglês)

> I use `verify` to assert interactions with collaborators — that a repository's `save` or an event bus's `publish` was actually called — and I lean on `ArgumentCaptor` when the method builds the argument internally and I need to inspect its fields. My rule of thumb is to mock collaborators, never value objects: mocking a plain data object just tests the mock I configured. For time and randomness I prefer injecting a `Clock` or a `Supplier` over `mockStatic`, because that makes the code testable by design; `mockStatic` is a last resort, and when I use it I always scope it inside a try-with-resources so the static mock doesn't leak into other tests.

### Vocabulário

| Termo (EN) | Tradução / nota |
| --- | --- |
| interaction verification | verificação de interação (`verify`) |
| collaborator | colaborador (objeto com comportamento/dependência externa) |
| value object | objeto de valor (dados simples, não mockar) |
| argument captor | captor de argumento (`ArgumentCaptor`) |
| static mocking | mock de método estático (`mockStatic`) |
| to leak (a mock) | vazar (um mock) pra outros testes |
| try-with-resources | bloco com fechamento automático (escopo do mock estático) |
| testable by design | testável por design (ex.: injetar `Clock`) |

## Veja também

- [[03-Dominios/Tecnologia/Java/Testes/06 - Mockito — mocks, stubbing e matchers|Mockito: mocks e stubbing]]
- [[03-Dominios/Tecnologia/Java/Testes/14 - Testando código assíncrono — Awaitility|Testando código assíncrono]]
- [[03-Dominios/Tecnologia/Java/Testes/index|Testes (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java]] (verbetes verify (Mockito) / ArgumentCaptor)

## Referências

- Mockito — javadoc da classe `Mockito` (verify, VerificationMode, InOrder, verifyNoMoreInteractions/verifyNoInteractions, ArgumentCaptor, mockStatic): https://site.mockito.org/javadoc/current/org/mockito/Mockito.html
