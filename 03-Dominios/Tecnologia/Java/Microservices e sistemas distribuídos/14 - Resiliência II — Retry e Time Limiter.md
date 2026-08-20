---
title: "Resiliência II — Retry e Time Limiter"
created: 2026-06-12
updated: 2026-06-12
type: concept
status: seedling
publish: true
fase: adepto
tags:
  - java
  - microservices
  - adepto
  - resiliencia
  - resilience4j
aliases:
  - "Retry"
  - "Time Limiter"
---

# Resiliência II — Retry e Time Limiter

> [!abstract] TL;DR
> **Retry** reenvia uma chamada que falhou, esperando um intervalo entre tentativas. Em sistemas distribuídos, falhas costumam ser **transitórias** (um pico de latência, um pod reiniciando), e tentar de novo dá certo. Mas há duas armadilhas: (1) só é seguro repetir operações **idempotentes** — repetir um `POST /pagamentos` pode cobrar duas vezes; (2) sem **backoff exponencial + jitter**, mil clientes repetindo ao mesmo tempo viram uma *retry storm* que derruba o serviço que estava só cambaleando. O **TimeLimiter** corta uma chamada **assíncrona** (`CompletableFuture`) que demora demais, transformando "esperar para sempre" numa falha rápida e previsível. No Resilience4j, são duas anotações: `@Retry` e `@TimeLimiter`.

## O que é

São dois padrões de resiliência complementares ao [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/13 - Resiliência I — a falha distribuída e o Circuit Breaker|Circuit Breaker]], implementados no Resilience4j (versão de referência: **2.4.0**, sobre Java 17 — não existe linha 3.x estável).

- **Retry** é a política de **tentar de novo**. Quando uma chamada remota falha, em vez de propagar o erro imediatamente, o Retry aguarda um intervalo e repete, até um número máximo de tentativas. A ideia é absorver falhas **transitórias** sem incomodar quem chamou.
- **TimeLimiter** é a política de **desistir no tempo certo**. Ele impõe um teto de duração a uma chamada assíncrona: se passar do limite, a operação é cancelada e vira uma exceção de timeout, em vez de travar a thread (ou o cliente) esperando indefinidamente.

A diferença de papel é importante: o Retry lida com *falhas que talvez sumam se eu insistir*; o TimeLimiter lida com *chamadas que nunca respondem*. Uma chamada lenta demais, aliás, é justamente o tipo de coisa que o TimeLimiter transforma numa falha — que o Retry pode então decidir repetir.

## Por que importa

Numa rede, a falha é o estado normal de fundo, não a exceção. Pacotes se perdem, GCs pausam a JVM por centenas de milissegundos, um nó faz failover, um balanceador rota para um pod que ainda não terminou de subir. A maioria dessas falhas é **transitória**: some sozinha em milissegundos ou segundos.

O Retry existe para que essas falhas transitórias **não vazem para o usuário**. Sem ele, o primeiro soluço da rede vira um erro 500 na cara de quem clicou. Com ele, a segunda tentativa quase sempre passa, e o usuário nem percebe.

O TimeLimiter existe porque, em sistemas distribuídos, **uma chamada lenta é pior que uma chamada que falha**. Um erro rápido você trata. Mas uma chamada que pendura por 30 segundos segura uma thread, esgota o pool, propaga a lentidão para cima e contamina serviços inteiros — o efeito dominó clássico que o Circuit Breaker tenta conter. O TimeLimiter ataca a raiz: nenhuma chamada deveria poder demorar para sempre. Ele converte "espera indefinida" em "falha previsível em N segundos", e falha previsível é coisa que arquitetura sabe tratar.

Juntos, os dois fecham um ciclo virtuoso com o Circuit Breaker: TimeLimiter garante que a falha apareça rápido, Retry absorve o que é transitório, e o Circuit Breaker abre quando o Retry para de adiantar.

## Como funciona

### Retry com backoff e jitter

A configuração de Retry no Resilience4j gira em torno de poucos parâmetros centrais:

- **`maxAttempts`** — número máximo de tentativas, **incluindo a primeira chamada**. O padrão é `3` (ou seja, a chamada original + 2 retentativas).
- **`waitDuration`** — pausa fixa entre tentativas. Padrão `500ms`.
- **`intervalFunction`** — substitui a pausa fixa por uma função do número da tentativa. É aqui que entram **backoff exponencial** (`IntervalFunction.ofExponentialBackoff()`, fator multiplicador padrão `2.0`) e **jitter** (`IntervalFunction.ofRandomized()`).
- **`retryExceptions`** — lista de exceções que **disparam** retry. Por padrão é vazia (e o predicado padrão considera toda exceção como retentável); na prática, você restringe a falhas que fazem sentido repetir.
- **`ignoreExceptions`** — lista de exceções que **nunca** disparam retry, mesmo que caiam na lista anterior. Use para erros que repetir não resolve: um `400 Bad Request`, uma validação que falhou.
- **`failAfterMaxAttempts`** — se `true`, lança `MaxRetriesExceededException` quando esgota as tentativas. Padrão `false`.

O **backoff exponencial** é o que separa um retry ingênuo de um retry educado. Em vez de bater na porta a cada 500ms, você espera 500ms, depois 1s, depois 2s, depois 4s. Cada falha consecutiva dá mais ar ao serviço do outro lado. A intuição: se ele falhou agora, provavelmente está sobrecarregado — insistir mais rápido só piora.

O **jitter** é o tempero que evita o efeito-manada. Imagine que um serviço caiu por 2 segundos e mil clientes estavam todos esperando. Quando ele volta, se todos usarem exatamente o mesmo backoff, todos repetem **no mesmo instante** — e o serviço recém-recuperado leva mil requisições simultâneas na cara e cai de novo. O jitter adiciona uma aleatoriedade ao intervalo (cada cliente espera, digamos, entre 1,5s e 2,5s), **espalhando** as retentativas no tempo. É a diferença entre uma fila ordenada e um estouro de boiada.

### Retry exige idempotência

Aqui está a regra que separa quem usa Retry de quem se machuca com ele: **só repita o que é seguro repetir.**

Repetir uma leitura (`GET`) é inofensivo — você só lê de novo. Mas repetir uma operação que **muda estado** sem garantia de idempotência é perigoso: a primeira tentativa pode ter **funcionado** no servidor, e só a *resposta* se perdeu na volta. Você acha que falhou, repete, e a operação acontece duas vezes. Dois pagamentos. Dois pedidos. Dois e-mails.

O conceito que torna o Retry seguro — uma operação que, executada N vezes, produz o mesmo efeito de tê-la executado uma vez — é a **idempotência**, e ele é o assunto do Galho 14 (Mensageria), onde o `at-least-once` força exatamente esse cuidado. Não vou re-explicar aqui: veja [[03-Dominios/Tecnologia/Java/Mensageria/20 - Idempotência — o pilar do at-least-once|Idempotência (Galho 14)]]. A ponte conceitual é direta: **retry é uma fonte de duplicação, e idempotência é a defesa contra duplicação.** Quem ativa retry numa operação que muta estado e *não* a tornou idempotente está, sem perceber, programando bugs de duplicação.

Regra de bolso: ative `@Retry` livremente em leituras e em operações que você protegeu com chave de idempotência; restrinja com `retryExceptions`/`ignoreExceptions` para nunca repetir o que não deve (um `409 Conflict`, por exemplo, raramente merece retry).

### TimeLimiter para chamadas assíncronas

O TimeLimiter decora uma chamada **assíncrona** e impõe um teto de tempo. Os parâmetros são dois:

- **`timeoutDuration`** — quanto tempo a operação pode rodar antes de estourar timeout.
- **`cancelRunningFuture`** — se `true`, cancela o `Future` em execução quando o timeout dispara (em vez de só desistir de esperar e deixar a tarefa rodando solta).

O ponto crucial — e a fonte da armadilha mais comum — é que o TimeLimiter opera sobre **`CompletionStage`/`Future`**, ou seja, sobre código **assíncrono**. Com a anotação `@TimeLimiter`, o método precisa retornar `CompletableFuture<T>`. A razão é mecânica: para *interromper* uma chamada que demora, o TimeLimiter precisa que ela esteja rodando em **outra thread** que ele possa cancelar. Um método síncrono e bloqueante executa na própria thread chamadora; não há para onde o TimeLimiter "voltar" para cortar a espera. Por isso, anotar com `@TimeLimiter` um método que retorna um tipo síncrono não tem o efeito esperado — o timeout precisa de assincronia para existir.

## Na prática

Configuração declarativa no `application.yml` (domínios neutros — `servicoExterno`):

```yaml
resilience4j:
  retry:
    instances:
      servicoExterno:
        max-attempts: 4
        wait-duration: 500ms
        enable-exponential-backoff: true
        exponential-backoff-multiplier: 2
        enable-randomized-wait: true          # jitter: espalha as retentativas
        randomized-wait-factor: 0.5
        retry-exceptions:
          - java.io.IOException
          - org.springframework.web.client.HttpServerErrorException
        ignore-exceptions:
          - com.exemplo.ErroDeValidacao        # repetir não resolve
  timelimiter:
    instances:
      servicoExterno:
        timeout-duration: 2s
        cancel-running-future: true
```

Uso com anotações. Note que `@TimeLimiter` força o retorno `CompletableFuture` — e que ele combina naturalmente com `@Retry` no mesmo método assíncrono:

```java
@Service
public class CatalogoClient {

    private final WebClient webClient;

    public CatalogoClient(WebClient webClient) {
        this.webClient = webClient;
    }

    // Leitura: idempotente por natureza, seguro repetir.
    // @TimeLimiter exige retorno assíncrono (CompletableFuture).
    @Retry(name = "servicoExterno")
    @TimeLimiter(name = "servicoExterno")
    public CompletableFuture<Produto> buscarProduto(String id) {
        return webClient.get()
                .uri("/produtos/{id}", id)
                .retrieve()
                .bodyToMono(Produto.class)
                .toFuture();   // Mono -> CompletableFuture
    }
}
```

Para um Retry imperativo sem WebFlux, o método de negócio pode lançar e o Resilience4j cuida da repetição:

```java
@Retry(name = "servicoExterno")
public CompletableFuture<Recibo> registrarEvento(EventoIdempotente evento) {
    // 'evento' carrega uma chave de idempotência: repetir é seguro.
    return CompletableFuture.supplyAsync(() -> gateway.enviar(evento));
}
```

## Armadilhas

### (1) Retry sem idempotência: efeito colateral duplicado

A armadilha mais cara. Você anota `@Retry` num endpoint que cria um pedido. A primeira tentativa **chega ao servidor e executa**, mas a resposta se perde no caminho de volta (timeout de rede, conexão derrubada). Do lado do cliente, parece falha — então o Retry repete. Resultado: **dois pedidos**, um cliente irritado, e um bug que só aparece sob estresse de rede, o pior tipo de bug para reproduzir. Antes de ligar retry em qualquer operação que muda estado, garanta idempotência (chave de idempotência, *deduplication*). Veja [[03-Dominios/Tecnologia/Java/Mensageria/20 - Idempotência — o pilar do at-least-once|Idempotência (Galho 14)]]. Na dúvida, restrinja com `ignoreExceptions` para não repetir mutações.

### (2) Retry storm sem backoff/jitter

Retry com `waitDuration` fixa e pequena, multiplicado por muitos clientes, **amplifica** a falha que deveria curar. Um serviço dá um soluço; centenas de clientes começam a repetir a cada 200ms, todos sincronizados; o serviço que ia se recuperar agora leva um pico de tráfego muito maior que o normal e **afunda de vez**. É a *retry storm* — o remédio virando veneno. A defesa é dupla: **backoff exponencial** (cada falha aumenta o intervalo, aliviando o alvo) e **jitter** (aleatoriedade que dessincroniza os clientes, evitando o pico simultâneo). Nunca rode retry de alto volume sem os dois.

### (3) TimeLimiter em chamada bloqueante: precisa ser assíncrono

Você anota `@TimeLimiter` num método síncrono que retorna `Produto` e espera que ele estoure timeout em 2s. Não estoura. O TimeLimiter precisa de uma chamada **assíncrona** — `CompletableFuture`/`CompletionStage` — porque só consegue cortar uma operação que roda em outra thread, cancelável. Um método bloqueante executa na própria thread chamadora; não há nada para o TimeLimiter interromper. O sintoma é silencioso e traiçoeiro: a anotação está lá, parece configurada, mas o timeout nunca acontece. Regra: `@TimeLimiter` só faz sentido em métodos que retornam `CompletableFuture<T>`.

## Em entrevista

### Frase pronta (inglês)

> Retry handles transient failures by re-issuing a request, but it's only safe on idempotent operations — retrying a non-idempotent write can duplicate side effects, like charging a customer twice. To use it responsibly, I pair it with exponential backoff and jitter, which prevents a retry storm where many clients hammer a recovering service in sync. For slow calls, I add a Time Limiter, which caps the duration of an asynchronous call and turns "waiting forever" into a fast, predictable failure — and it only works on async returns like CompletableFuture, because it needs a cancellable task on another thread.

### Vocabulário

| Português | Inglês |
| --- | --- |
| nova tentativa / retentativa | retry |
| recuo exponencial | exponential backoff |
| jitter (aleatoriedade no intervalo) | jitter |
| idempotência | idempotency |
| limitador de tempo | time limiter |
| tempestade de retentativas | retry storm |
| falha transitória | transient failure |
| chave de idempotência | idempotency key |

## Veja também

- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/13 - Resiliência I — a falha distribuída e o Circuit Breaker|Circuit Breaker]]
- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/15 - Resiliência III — Bulkhead e Rate Limiter|Bulkhead e Rate Limiter]]
- [[03-Dominios/Tecnologia/Java/Mensageria/20 - Idempotência — o pilar do at-least-once|Idempotência (Galho 14)]]
- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/index|Microservices e sistemas distribuídos (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]

## Referências

- Resilience4j — Retry: https://resilience4j.readme.io/docs/retry
- Resilience4j — TimeLimiter: https://resilience4j.readme.io/docs/timeout
- Resilience4j — Getting Started (Spring Boot): https://resilience4j.readme.io/docs/getting-started-3
- Versão de referência: Resilience4j 2.4.0 (Java 17). Não há linha 3.x estável.
