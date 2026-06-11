---
title: "Testando código assíncrono — Awaitility"
created: 2026-06-11
updated: 2026-06-11
type: concept
progress: backlog
status: seedling
publish: true
fase: magus
tags:
  - java
  - testes
  - magus
  - awaitility
aliases:
  - "Awaitility"
  - "testando assíncrono"
---

# Testando código assíncrono — Awaitility

> [!abstract] TL;DR
> Quando o efeito de uma ação acontece **"depois"** — um processamento assíncrono que roda em outra thread, um evento que será consumido mais tarde, uma escrita que só se reflete no repositório passados alguns milissegundos —, o teste não pode simplesmente ler o estado na linha seguinte: ele ainda não chegou. O **Awaitility** resolve isso com *polling declarativo*: `await().atMost(5, SECONDS).untilAsserted(...)` fica re-executando a sua asserção até ela passar **ou** até estourar o timeout. É o substituto direto do `Thread.sleep`, que é fonte garantida de *flakiness* — lento quando o efeito chega rápido, falho quando o CI está sobrecarregado.

## O que é

Awaitility é uma biblioteca pequena de DSL para **esperar por condições eventuais** em testes de código assíncrono. Em vez de pausar a thread de teste por um tempo fixo e torcer para o efeito já ter acontecido, você descreve *o que* precisa ficar verdadeiro e *por quanto tempo no máximo* você está disposto a esperar. A biblioteca cuida do laço de *polling*.

O coração da API é um *builder* iniciado por `await()`:

- `atMost(long, TimeUnit)` — o teto de tempo. Se a condição não ficar verdadeira dentro dele, dispara `ConditionTimeoutException` e o teste falha.
- `untilAsserted(ThrowingRunnable)` — recebe um bloco de asserções (AssertJ, JUnit, Hamcrest). A cada *poll*, o bloco é executado; se ele lança `AssertionError`, o Awaitility engole o erro e tenta de novo no próximo *poll*. A última falha vira a mensagem de erro se o timeout estourar.
- `until(Callable<Boolean>)` — a forma mais simples: re-avalia um *predicate* até ele retornar `true`.
- `pollInterval(...)` — de quanto em quanto tempo re-checar.

Os imports estáticos canônicos deixam o código fluente:

```java
import static org.awaitility.Awaitility.await;
import static java.util.concurrent.TimeUnit.SECONDS;
import static org.assertj.core.api.Assertions.assertThat;
```

## Por que importa

Código de produção sério é cheio de assincronia: `@Async`, `CompletableFuture`, *executors*, *listeners* de mensageria, *event handlers*, *schedulers*. O efeito observável (uma linha gravada, um status mudado, um *callback* invocado) chega **fora** da thread que disparou a ação. Um teste ingênuo lê o estado cedo demais e falha de forma intermitente.

A reação errada mais comum é jogar um `Thread.sleep(2000)` no meio do teste. Isso é o pior dos dois mundos: **lento** (você paga 2 segundos mesmo quando o efeito chega em 50 ms) e **frágil** (2 segundos podem não bastar num CI carregado). Testes assim são desligados, ignorados ou viram a razão pela qual ninguém confia na *suite*. Awaitility troca a aposta cega por uma espera adaptativa: termina assim que a condição é satisfeita e só consome o tempo necessário.

## Como funciona

### Consistência eventual: o efeito acontece "depois" (async)

Em código síncrono, causa e efeito são a mesma thread: você chama, ele retorna, você lê. Em código assíncrono há um *gap* temporal — a chamada **agenda** o trabalho e retorna; o efeito materializa depois, em outra thread, em outro instante. Esse é o regime de **consistência eventual**: o sistema *vai* convergir para o estado correto, mas você não sabe *quando*.

O detalhe de *como* esse trabalho roda (pool de threads, `CompletableFuture`, modelo de memória, *happens-before*) é assunto do galho de concorrência — veja [[03-Dominios/Java/Concorrência e paralelismo/index|Concorrência e paralelismo]]. Aqui o ponto é o teste: precisamos de uma forma de **esperar a convergência** sem fixar um tempo arbitrário.

### await().atMost().untilAsserted: polling declarativo

A combinação canônica:

```java
await()
    .atMost(5, SECONDS)
    .untilAsserted(() -> assertThat(repo.findById(id)).isPresent());
```

Leitura: "espere no máximo 5 segundos; a cada *poll*, rode esta asserção; pare assim que ela passar". O `untilAsserted` é declarativo porque você escreve a **condição final desejada** como se fosse uma asserção normal de teste — o laço de retry é invisível.

A forma `until(Callable<Boolean>)` é o irmão mais cru, útil quando o que você quer é apenas um *predicate*:

```java
await().atMost(5, SECONDS).until(() -> repo.count() == 1);
```

A diferença prática: `untilAsserted` carrega o **estado final esperado** (e a mensagem rica do AssertJ quando falha); `until` carrega só um booleano. Prefira `untilAsserted` quando houver uma asserção de verdade a fazer — a mensagem de timeout fica muito mais útil para depurar.

### Nunca Thread.sleep (flakiness garantida)

`Thread.sleep` é a anti-solução. Ele não observa nada — apenas pausa. Você está apostando que o efeito chega dentro do tempo escolhido, e essa aposta tem dois jeitos de dar errado:

1. O efeito chega antes — você desperdiça o resto do *sleep*, deixando a *suite* lenta.
2. O efeito chega depois (CI lento, *garbage collector* mordendo, máquina compartilhada) — o teste falha sem nenhum bug real.

`await()` elimina os dois: termina no instante em que a condição é satisfeita e tolera variação de tempo até o teto. Regra prática de galho magus: **se você digitou `Thread.sleep` num teste, troque por Awaitility**.

### Configurar pollInterval e timeout para o CI

Dois botões calibram o comportamento:

- `pollInterval(Duration)` — de quanto em quanto re-checar. Curto (50–100 ms) reage rápido, mas re-executa a asserção mais vezes (custo se ela for cara). Padrão razoável: `Duration.ofMillis(100)`.
- `atMost(...)` — o teto. Curto demais é a causa nº 1 de *flakiness* em CI: na sua máquina o efeito chega em 200 ms, mas o *runner* compartilhado leva 3 s. Calibre o `atMost` para o **pior caso do ambiente mais lento**, não para a sua máquina.

```java
await()
    .atMost(5, SECONDS)
    .pollInterval(Duration.ofMillis(100))
    .untilAsserted(() -> assertThat(repo.findById(id)).isPresent());
```

Há ainda `pollDelay` (espera inicial antes do primeiro *poll*, default 100 ms) e `with().pollInterval(...)` como açúcar sintático — mas `atMost` + `pollInterval` já cobrem a esmagadora maioria dos casos.

## Na prática

Um serviço que processa pedidos de forma assíncrona: `submit` agenda o trabalho e retorna na hora; algum tempo depois o `Order` aparece no repositório com status `PROCESSED`. O teste dispara e **espera a convergência** com Awaitility.

```java
import static org.awaitility.Awaitility.await;
import static java.util.concurrent.TimeUnit.SECONDS;
import static org.assertj.core.api.Assertions.assertThat;

import java.time.Duration;
import org.junit.jupiter.api.Test;

class OrderProcessingTest {

    OrderService orderService = new OrderService();          // dispara o processamento async
    OrderRepository orderRepository = orderService.repository();

    @Test
    void processaPedidoDeFormaAssincrona() {
        Customer customer = new Customer("ACME Ltda");
        Order order = new Order(customer, /* total */ 1299_00);

        // submit() agenda o processamento em outra thread e retorna imediatamente
        String id = orderService.submit(order);

        // o efeito (status PROCESSED) só aparece "depois" — esperamos a convergência
        await()
            .atMost(5, SECONDS)
            .pollInterval(Duration.ofMillis(100))
            .untilAsserted(() ->
                assertThat(orderRepository.findById(id))
                    .get()
                    .extracting(Order::status)
                    .isEqualTo(OrderStatus.PROCESSED));
    }
}
```

O bloco dentro de `untilAsserted` é uma asserção AssertJ comum — nada nele "sabe" que está num laço de retry. O Awaitility re-executa a *lambda* a cada 100 ms; se `findById` ainda devolve vazio ou o status ainda é `PENDING`, a asserção lança `AssertionError`, o Awaitility ignora e tenta de novo. Assim que o processamento converge, a asserção passa e o teste segue. Se passar 5 segundos sem convergir, vem `ConditionTimeoutException` carregando a última falha do AssertJ — mensagem muito mais rica do que um `assertEquals` solto que rodou cedo demais.

O *como* esse `submit` roda em outra thread (pool, `CompletableFuture`, visibilidade de memória) é território do [[03-Dominios/Java/Concorrência e paralelismo/index|galho de concorrência]] — aqui só nos importa que o efeito é **eventual** e que o teste precisa esperá-lo de forma adaptativa.

## Armadilhas

### (1) Trocar a espera adaptativa por Thread.sleep(2000)

O reflexo de "o teste falha às vezes, vou dar um sleep maior" é exatamente o caminho da *flakiness*.

```java
// ANTIPADRÃO
orderService.submit(order);
Thread.sleep(2000);                 // aposta cega
assertThat(orderRepository.findById(id)).isPresent();
```

Quando o efeito chega em 50 ms, você desperdiça 1.95 s por teste — multiplicado por dezenas de testes, a *suite* fica insuportável. Quando o CI está sobrecarregado e o efeito leva 2.5 s, o teste falha sem bug nenhum.

**Fix:** `await().atMost(5, SECONDS).untilAsserted(...)`. Termina no instante da convergência e tolera variação até o teto.

### (2) Timeout (atMost) curto demais para o CI carregado

Calibrar o `atMost` pela velocidade da sua máquina é flaky garantido: o *runner* compartilhado é mais lento, divide CPU com outros jobs e sofre pausas de GC.

```java
// frágil: 200 ms basta no laptop, mas o CI leva 1,5 s
await().atMost(200, MILLISECONDS).untilAsserted(...);
```

**Fix:** calibre o teto para o **pior caso do ambiente mais lento**, com folga. Um `atMost` generoso (3–5 s) **não** deixa o teste lento quando ele passa rápido — `untilAsserted` retorna na convergência, não no teto. O teto só protege contra o cenário patológico.

### (3) until() com booleano que não asserta o estado final

`until(Callable<Boolean>)` checa um *predicate*; se o *predicate* é frouxo, o teste pode passar **cedo demais**, antes de o estado realmente desejado existir.

```java
// passa assim que QUALQUER pedido existe — não garante status PROCESSED
await().atMost(5, SECONDS).until(() -> orderRepository.count() > 0);
```

O pedido pode estar lá com status `PENDING` e o teste verde — falso positivo. Além disso, quando estoura o timeout, a mensagem é só "condição não satisfeita", sem dizer *qual* estado faltava.

**Fix:** prefira `untilAsserted` com a asserção do **estado final completo**. Ela é mais específica (status `PROCESSED`, não "existe algo") e produz mensagem de erro rica no timeout.

## Em entrevista

### Frase pronta (inglês)

> When the effect of an action happens asynchronously, the test can't read the state on the next line — it isn't there yet. I avoid `Thread.sleep`, which is the textbook source of flakiness: too slow when the effect arrives quickly, and a false failure when the CI runner is loaded. Instead I use Awaitility's declarative polling: `await().atMost(5, SECONDS).pollInterval(ofMillis(100)).untilAsserted(...)` re-runs my assertion until it passes or the timeout fires. I prefer `untilAsserted` over the raw `until(Callable<Boolean>)` because it carries the final expected state and gives a rich failure message, and I calibrate `atMost` for the slowest environment rather than my laptop so the test stays green under load while still returning the instant the condition converges.

### Vocabulário

| Termo (EN) | Significado |
| --- | --- |
| eventual condition | condição que fica verdadeira algum tempo depois da ação (efeito assíncrono) |
| polling | re-checar uma condição em intervalos até ela passar ou estourar o teto |
| flaky test | teste que passa ou falha de forma intermitente sem mudança de código |
| timeout (atMost) | tempo máximo de espera antes de declarar falha (`ConditionTimeoutException`) |
| poll interval | intervalo entre re-checagens da condição |
| assert eventually | asserir que algo se torna verdadeiro com o tempo, não imediatamente |

## Veja também

- [[03-Dominios/Java/Testes/15 - Testando código reativo — StepVerifier e @WebFluxTest|Testando código reativo]]
- [[03-Dominios/Java/Testes/07 - Mockito — verify, ArgumentCaptor e quando NÃO mockar|Mockito: verify e ArgumentCaptor]]
- [[03-Dominios/Java/Concorrência e paralelismo/index|Concorrência e paralelismo]]
- [[03-Dominios/Java/Testes/index|Testes (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Dicionário de Java]]

## Referências

- Awaitility Wiki — Usage: https://github.com/awaitility/awaitility/wiki/Usage
