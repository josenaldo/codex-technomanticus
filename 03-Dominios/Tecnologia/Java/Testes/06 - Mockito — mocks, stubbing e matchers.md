---
title: "Mockito — mocks, stubbing e matchers"
created: 2026-06-11
updated: 2026-06-11
type: concept
progress: backlog
status: seedling
publish: true
fase: Adepto
tags:
  - java
  - testes
  - adepto
  - mockito
aliases:
  - "Mockito"
  - "mocks e stubbing"
---

# Mockito — mocks, stubbing e matchers

> [!abstract] TL;DR
> Mockito cria dublês de teste (mocks) que você programa com `when().thenReturn()` e depois verifica. As anotações `@Mock` e `@InjectMocks` montam o objeto sob teste já com colaboradores falsos injetados, sem `new` manual. Argument matchers (`any`, `eq`, `anyString`) descrevem quais argumentos um stub aceita — mas há uma regra de ouro: se um argumento usa matcher, **todos** têm que usar.

## O que é

Mockito é a biblioteca de mocking mais usada do ecossistema Java. Ela fabrica, em tempo de execução, objetos falsos (dublês de teste) que implementam uma interface ou estendem uma classe sem você escrever uma linha de implementação. Esses dublês servem para **isolar a unidade sob teste** dos seus colaboradores: em vez de chamar o banco de verdade, um serviço HTTP real ou um relógio do sistema, você troca tudo por mocks programáveis.

O fluxo canônico tem três tempos:

1. **Stubbing** — você ensina o mock a responder: `when(repository.findById(1L)).thenReturn(Optional.of(order))`.
2. **Exercício** — você chama o método de produção que usa esse mock.
3. **Verificação** — você confere que o mock foi (ou não foi) chamado como esperado (assunto da [[03-Dominios/Tecnologia/Java/Testes/07 - Mockito — verify, ArgumentCaptor e quando NÃO mockar|próxima nota]]).

A versão atual é **Mockito 5.x** (5.23.0, março de 2026), que exige Java 11+ e usa o `mockito-inline` como engine padrão — ou seja, dá pra mockar classes `final` e métodos `static` sem dependência extra, coisa que no Mockito 3 era um adendo opcional.

## Por que importa

Sem mocks, todo teste de uma camada de serviço vira teste de integração: você precisa subir banco, fila, rede. Isso é lento, frágil e mistura "a lógica de negócio está certa?" com "a infra está de pé?". Mockito permite responder **só a primeira pergunta**.

Para uma entrevista sênior, o domínio de Mockito sinaliza três coisas: você entende **isolamento de unidade**, sabe a **diferença entre os tipos de dublê** (e portanto quando não usar mock nenhum), e conhece as **armadilhas** — mocking de spy com side effect, mistura de matcher e literal, strict stubbing. Quem só decora `when().thenReturn()` trava na primeira pergunta de acompanhamento.

A contrapartida: mock em excesso acopla o teste à implementação. Um teste que mocka demais quebra a cada refactor, mesmo quando o comportamento externo não mudou. Saber **onde parar** é metade da habilidade.

## Como funciona

### Mock vs spy vs fake vs stub (e qual usar)

Os quatro termos descrevem dublês de teste diferentes (taxonomia de Gerard Meszaros / Martin Fowler):

| Dublê | O que faz | Quando usar |
| --- | --- | --- |
| **Stub** | Retorna respostas pré-programadas, sem lógica | Quando você só precisa que o colaborador "devolva algo" |
| **Mock** | Stub + registra interações para verificação | Quando você quer **verificar** que uma chamada ocorreu |
| **Spy** | Embrulha um objeto real; chama o método real por padrão, mas pode stubar partes | Quando 90% do objeto real serve e você quer sobrescrever só um método |
| **Fake** | Implementação leve e funcional de verdade (ex.: repositório em `HashMap`) | Quando o comportamento real importa mas a infra é cara |

No Mockito, `mock(Order.class)` cria um **mock** (todos os métodos retornam `null`/`0`/coleção vazia até serem stubados). `spy(realObject)` cria um **spy** (métodos reais rodam até você stubar). Fakes você escreve à mão — não é função do Mockito. A regra prática: **prefira mock para colaboradores que você controla via interface; prefira fake quando a lógica do colaborador é parte do que você testa; use spy com parcimônia** (ver Armadilha 1).

### @Mock / @InjectMocks / MockitoExtension

A forma idiomática no JUnit 5 usa a extensão do Mockito para inicializar as anotações:

```java
@ExtendWith(MockitoExtension.class)
class OrderServiceTest {

    @Mock
    OrderRepository repository;

    @Mock
    NotificationSender notifier;

    @InjectMocks
    OrderService service;
}
```

- `@ExtendWith(MockitoExtension.class)` registra a extensão; ela cria os mocks antes de cada teste e valida o strict stubbing no fim.
- `@Mock` declara um campo que será substituído por um mock.
- `@InjectMocks` cria a instância real de `OrderService` e injeta os mocks declarados acima — por construtor (preferido), setter ou campo, nessa ordem de tentativa.

Sem a extensão, você precisaria de `MockitoAnnotations.openMocks(this)` num `@BeforeEach`. A extensão elimina esse boilerplate e ainda ativa o strict stubbing (ver Armadilha 3).

### Stubbing: when().thenReturn / thenThrow / thenAnswer e doX().when() pra void

O stubbing "normal" usa `when(...)`:

```java
when(repository.findById(1L)).thenReturn(Optional.of(order)); // valor fixo
when(repository.findById(99L)).thenThrow(new NotFoundException()); // exceção
when(repository.save(any())).thenAnswer(inv -> inv.getArgument(0)); // resposta dinâmica
```

- `thenReturn(x)` devolve `x`. Pode encadear (`thenReturn(a).thenReturn(b)`) para chamadas sucessivas.
- `thenThrow(ex)` lança a exceção quando o método é chamado.
- `thenAnswer(lambda)` computa a resposta a partir dos argumentos recebidos (via `InvocationOnMock`). Útil quando o retorno depende da entrada.

O problema: `when(mock.metodoVoid())` **não compila** — `void` não é uma expressão. Para métodos `void` (e para spies, ver Armadilha 1), use a forma `doX().when()`:

```java
doNothing().when(notifier).send(any());           // não faz nada (já é o default, mas explicita)
doThrow(new MailException()).when(notifier).send(any()); // lança ao enviar
doAnswer(inv -> { log(inv.getArgument(0)); return null; }).when(notifier).send(any());
```

A inversão da ordem (`do...` antes de `.when()`) existe porque o Mockito precisa configurar o comportamento **sem** invocar o método de verdade.

### Argument matchers e a regra "todos ou nenhum"

Matchers descrevem **quais argumentos** um stub aceita, em vez de exigir igualdade exata:

```java
when(repository.findByStatus(anyString())).thenReturn(List.of());
when(repository.findByStatusAndCustomer(eq("PAID"), any(Customer.class))).thenReturn(List.of());
when(repository.findByPriority(intThat(p -> p > 5))).thenReturn(List.of());
```

Principais matchers (de `ArgumentMatchers`, herdados estaticamente por `Mockito`):

- `any()` — qualquer objeto, **inclusive `null`**.
- `any(Type.class)` / `anyString()` / `anyInt()` — qualquer valor **não-nulo** daquele tipo.
- `eq(valor)` — igualdade exata (use quando precisa fixar um argumento no meio de outros matchers).
- `argThat(predicate)` / `intThat(predicate)` — matcher customizado por predicado.

A **regra de ouro**: *se você usa um matcher para um argumento, todos os argumentos daquela chamada têm que ser matchers*. Isso é uma limitação técnica — matchers funcionam empilhando valores numa fila interna, e misturar literal com matcher desalinha essa fila. Para passar um valor literal junto com matchers, embrulhe-o em `eq(...)` (ver Armadilha 2).

## Na prática

```java
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;
import static org.assertj.core.api.Assertions.assertThat;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class OrderServiceTest {

    @Mock
    OrderRepository repository;

    @Mock
    NotificationSender notifier;

    @InjectMocks
    OrderService service;

    @Test
    void placeOrder_persistsAndReturnsWithGeneratedId() {
        Order incoming = new Order(null, "alice@example.com", 250);

        // thenAnswer: simula o banco atribuindo um id no save
        when(repository.save(any(Order.class)))
            .thenAnswer(invocation -> {
                Order toSave = invocation.getArgument(0);
                return new Order(42L, toSave.email(), toSave.total());
            });

        Order placed = service.placeOrder(incoming);

        assertThat(placed.id()).isEqualTo(42L);
        assertThat(placed.email()).isEqualTo("alice@example.com");
    }

    @Test
    void placeOrder_belowMinimum_isRejected() {
        Order tiny = new Order(null, "bob@example.com", 5);

        // eq + any: matcher literal embrulhado pra cumprir a regra "todos ou nenhum"
        when(repository.existsByEmailAndStatus(eq("bob@example.com"), any()))
            .thenReturn(false);

        assertThatThrownBy(() -> service.placeOrder(tiny))
            .isInstanceOf(IllegalArgumentException.class);
    }
}
```

O `thenAnswer` brilha quando o retorno depende da entrada: aqui ele copia o e-mail e o total recebidos e devolve um `Order` com id gerado, imitando o comportamento de um `save` real sem tocar no banco. Note o uso de [[03-Dominios/Tecnologia/Java/Testes/03 - AssertJ — fluent assertions|AssertJ]] para as asserções.

## Armadilhas

### (1) Stubar spy com `when(spy.foo())` dispara o método real

Em um spy, `when(spy.foo())` **chama `foo()` de verdade** antes de stubar — porque o argumento de `when` é avaliado primeiro. Se `foo()` tem efeito colateral (lança exceção, escreve em disco), o teste quebra na hora do setup.

```java
List<String> spy = spy(new ArrayList<>());
when(spy.get(0)).thenReturn("a"); // IndexOutOfBoundsException: a lista real está vazia!
```

**Fix**: use a forma `doReturn().when()`, que não invoca o método real:

```java
doReturn("a").when(spy).get(0); // ok, não toca no objeto real
```

### (2) Misturar matcher e literal na mesma chamada

Se um argumento é matcher, todos têm que ser. Misturar literal e matcher lança `InvalidUseOfMatchersException`:

```java
// ERRO: 1 é literal, any() é matcher
when(repository.find(1, any())).thenReturn(result);
// InvalidUseOfMatchersException: 2 matchers expected, 1 recorded
```

**Fix**: embrulhe o literal em `eq(...)`:

```java
when(repository.find(eq(1), any())).thenReturn(result); // ok
```

### (3) Stub não usado dispara `UnnecessaryStubbingException`

Com `MockitoExtension` (strict stubbing, default no Mockito 5), um stub configurado mas nunca exercido faz o teste **falhar** com `UnnecessaryStubbingException`. Isso é proposital: stub morto costuma ser sinal de teste desatualizado.

```java
when(notifier.isEnabled()).thenReturn(true); // se o teste nunca chama isEnabled()...
// → UnnecessaryStubbingException
```

**Fix**: remova o stub que não é usado. Se ele é compartilhado e só *alguns* testes o exercem, marque-o como lenient:

```java
lenient().when(notifier.isEnabled()).thenReturn(true); // não cobrado pelo strict stubbing
```

## Em entrevista

### Frase pronta (inglês)

> Mockito lets me isolate the unit under test by replacing its collaborators with programmable test doubles. I configure behavior with `when(...).thenReturn(...)` — or `doThrow().when(...)` for void methods and spies — and I use argument matchers like `any()` and `eq()` to describe which calls a stub should match. The key rule is that if one argument uses a matcher, all of them must, otherwise Mockito throws. With the `MockitoExtension` and strict stubbing, unused stubs fail the test, which keeps my tests honest. I also distinguish mock, spy, fake and stub, and I reach for a fake instead of a mock when the collaborator's own logic is part of what I'm verifying.

### Vocabulário

| Termo | Significado |
| --- | --- |
| test double | termo guarda-chuva para mock, spy, fake e stub |
| stubbing | programar a resposta de um mock para uma chamada |
| argument matcher | descritor de argumento (`any`, `eq`) em vez de valor exato |
| strict stubbing | modo que falha o teste se um stub não for usado |
| spy | dublê que embrulha um objeto real e chama métodos reais por padrão |
| to inject | injetar mocks no objeto sob teste (`@InjectMocks`) |
| lenient stub | stub isento da checagem de strict stubbing |

## Veja também

- [[03-Dominios/Tecnologia/Java/Testes/07 - Mockito — verify, ArgumentCaptor e quando NÃO mockar|Mockito: verify e ArgumentCaptor]]
- [[03-Dominios/Tecnologia/Java/Testes/03 - AssertJ — fluent assertions|AssertJ]]
- [[03-Dominios/Tecnologia/Java/Testes/index|Testes (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java]]

## Referências

- Site oficial do Mockito — https://site.mockito.org/
- Javadoc do mockito-core — https://javadoc.io/doc/org.mockito/mockito-core/latest/index.html
- Releases do Mockito (versão 5.23.0, mar/2026) — https://github.com/mockito/mockito/releases
