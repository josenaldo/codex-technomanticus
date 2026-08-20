---
title: "Resiliência III — Bulkhead e Rate Limiter"
created: 2026-06-12
updated: 2026-06-12
type: concept
status: seedling
publish: true
fase: Adepto
tags:
  - java
  - microservices
  - adepto
  - resiliencia
  - resilience4j
aliases:
  - "Bulkhead"
  - "Rate Limiter"
---

# Resiliência III — Bulkhead e Rate Limiter

> [!abstract] TL;DR
> O **Bulkhead** (anteparo) isola recursos para que a falha — ou a lentidão — de um serviço não esgote todas as threads da aplicação e derrube tudo junto. No Resilience4j **2.4.0** ele tem duas formas: **SemaphoreBulkhead**, que limita a concorrência na própria thread chamadora com um semáforo (`maxConcurrentCalls`), e **ThreadPoolBulkhead**, que dá ao serviço um pool de threads dedicado mais uma fila limitada (`coreThreadPoolSize`, `maxThreadPoolSize`, `queueCapacity`), executando de forma assíncrona. O **RateLimiter** ataca outra dimensão: limita **quantas chamadas** podem passar por janela de tempo (`limitForPeriod` permissões a cada `limitRefreshPeriod`), recusando ou esperando (`timeoutDuration`) o excedente. Bulkhead protege contra esgotamento de concorrência; RateLimiter protege contra excesso de volume. São padrões complementares, não substitutos.

## O que é

Um navio bem projetado não afunda quando um casco fura. Ele é dividido em **compartimentos estanques** — os *bulkheads* — de modo que a água que entra por uma brecha fica confinada a um compartimento, e o resto do navio segue flutuando. O padrão Bulkhead em software pega exatamente essa ideia: **particionar recursos** para que uma falha localizada não se espalhe.

O recurso mais precioso e mais fácil de esgotar numa aplicação é o **pool de threads**. Imagine um serviço que chama três dependências: pagamentos, estoque e notificações. Se todas as chamadas compartilham o mesmo pool e o serviço de pagamentos fica lento, as requisições para pagamentos começam a empilhar, **segurando threads** enquanto esperam. Em pouco tempo, todas as threads estão presas esperando pagamentos — e as chamadas a estoque e notificações, que estavam saudáveis, **também travam por falta de thread**. Uma falha em um lugar virou uma falha em todos. O Bulkhead evita isso isolando cada dependência num compartimento de concorrência próprio.

O Resilience4j **2.4.0** (Java 17) implementa o Bulkhead de duas maneiras distintas:

- **SemaphoreBulkhead** — limita a concorrência **na thread chamadora**, usando um semáforo. A chamada executa de forma síncrona; o semáforo só controla *quantas* podem estar em voo ao mesmo tempo.
- **ThreadPoolBulkhead** — dá ao compartimento um **pool de threads dedicado** com uma **fila limitada**. A chamada roda de forma **assíncrona**, numa thread do pool, não na thread chamadora.

O **RateLimiter** resolve um problema vizinho mas diferente: em vez de limitar *quantas chamadas simultâneas*, ele limita *quantas chamadas por unidade de tempo*. É o limitador de taxa — o "no máximo N requisições por segundo" — que protege uma dependência de ser inundada.

## Por que importa

Numa arquitetura de microservices, um serviço quase nunca falha sozinho de forma limpa. O modo de falha mais traiçoeiro é a **lentidão**: a dependência não cai, ela só responde devagar. Sem isolamento, essa lentidão se traduz em threads presas, e threads presas se traduzem em **esgotamento de recursos** que contamina chamadas saudáveis. É a "falha distribuída" se propagando — o tema central desta sub-trilha de resiliência.

O Bulkhead te dá **contenção de raio de dano**: o pior caso de um serviço lento fica limitado ao seu próprio compartimento. As outras dependências continuam respondendo porque têm suas próprias threads (ThreadPoolBulkhead) ou suas próprias permissões de concorrência (SemaphoreBulkhead). É a diferença entre "o serviço de pagamentos está degradado" e "a aplicação inteira caiu".

O RateLimiter te dá **controle de vazão**. Ele serve para:

- **Proteger uma dependência frágil** que não aguenta mais que X chamadas por segundo (um sistema legado, uma API de terceiro com cota).
- **Respeitar contratos de cota** — APIs externas frequentemente cobram ou bloqueiam por excesso de requisições; o RateLimiter te mantém dentro do limite.
- **Garantir justiça** entre consumidores, evitando que um cliente abusivo monopolize a capacidade.

Os dois padrões se encaixam no mesmo objetivo — **degradar com graça em vez de colapsar** — mas em eixos diferentes: Bulkhead no eixo da *concorrência simultânea*, RateLimiter no eixo do *volume ao longo do tempo*.

## Como funciona

### SemaphoreBulkhead

O SemaphoreBulkhead é o modo padrão e mais leve. Ele mantém um **semáforo** com um número fixo de permissões. Antes de executar, a chamada tenta adquirir uma permissão; ao terminar, devolve. Se não há permissão livre, a chamada espera por até `maxWaitDuration` e, se ainda assim não conseguir, é **recusada** com `BulkheadFullException`.

Parâmetros (com os defaults da 2.4.0):

- **`maxConcurrentCalls`** (default `25`) — o número máximo de execuções paralelas que o bulkhead permite. É o tamanho do semáforo.
- **`maxWaitDuration`** (default `0`) — quanto tempo uma thread espera bloqueada tentando entrar num bulkhead saturado antes de desistir. `0` significa "rejeite na hora se estiver cheio".

O ponto-chave: a chamada roda **na thread chamadora**. O semáforo não troca de thread, só conta. Isso o torna barato e compatível com vários modelos de I/O, mas significa que a thread original **fica presa** durante a chamada lenta — o isolamento é de *contagem de concorrência*, não de *thread física*.

### ThreadPoolBulkhead

O ThreadPoolBulkhead leva o isolamento mais longe: ele dá ao compartimento um **pool de threads fixo** mais uma **fila limitada**. Quando uma chamada chega, ela é submetida ao pool; se houver thread livre, executa nela; se todas estiverem ocupadas, vai para a fila; se a fila estiver cheia, é **rejeitada**. A execução é **assíncrona** — retorna um `CompletableFuture`.

Parâmetros (com os defaults da 2.4.0):

- **`coreThreadPoolSize`** (default `núcleos disponíveis − 1`) — o número de threads mantidas vivas no pool.
- **`maxThreadPoolSize`** (default `núcleos disponíveis`) — o teto de threads que o pool pode criar sob carga.
- **`queueCapacity`** (default `100`) — quantas chamadas podem aguardar na fila quando todas as threads estão ocupadas.
- **`keepAliveDuration`** (default `20ms`) — quanto tempo as threads excedentes (acima do core) ficam ociosas antes de serem encerradas.

A vantagem sobre o semáforo: a chamada lenta segura uma **thread do pool dedicado**, não a thread chamadora. Mesmo que o serviço de pagamentos sature seu próprio pool, a thread que originou a requisição é liberada e o resto da aplicação não sente. O isolamento aqui é de *thread física*, e é mais forte.

> [!question] Por que então não usar sempre ThreadPoolBulkhead, que isola mais?
> Porque a troca de thread tem custo e — mais importante — **perde o contexto da thread original**. Tudo que vive em `ThreadLocal` (e padrões construídos sobre ele, como o `SecurityContext` ou o contexto de uma transação) não atravessa para a thread do pool, a menos que você propague explicitamente. Voltaremos a isso nas armadilhas. O SemaphoreBulkhead, por executar na thread chamadora, preserva esse contexto de graça.

### RateLimiter

O RateLimiter divide o tempo em **ciclos** de duração `limitRefreshPeriod`. No início de cada ciclo, o contador de permissões é reabastecido para `limitForPeriod`. Cada chamada consome uma permissão. Quando as permissões do ciclo acabam, as chamadas seguintes **esperam** por uma permissão pelo tempo de `timeoutDuration`; se o próximo ciclo chegar dentro desse prazo, a chamada passa; senão, é **recusada** com `RequestNotPermitted`.

Parâmetros (com os defaults da 2.4.0):

- **`limitForPeriod`** (default `50`) — o número de permissões disponíveis durante um período de refresh. É o "quantas chamadas por janela".
- **`limitRefreshPeriod`** (default `500 ns`) — a duração da janela; ao fim de cada uma, as permissões voltam a `limitForPeriod`.
- **`timeoutDuration`** (default `5s`) — quanto tempo uma thread espera por uma permissão antes de falhar.

Na prática, `limitForPeriod = 100` com `limitRefreshPeriod = 1s` configura "no máximo 100 chamadas por segundo". O `timeoutDuration` decide o comportamento sob saturação: alto, e os chamadores **esperam educadamente** a próxima janela (suavizando picos); baixo (ou zero), e o excedente **falha rápido**, devolvendo erro em vez de enfileirar.

## Na prática

Configuração declarativa no `application.yml` — um bulkhead por dependência, mais um rate limiter:

```yaml
resilience4j:
  bulkhead:
    instances:
      servicoPagamentos:
        max-concurrent-calls: 10
        max-wait-duration: 50ms
  thread-pool-bulkhead:
    instances:
      servicoRelatorios:
        core-thread-pool-size: 4
        max-thread-pool-size: 8
        queue-capacity: 50
  ratelimiter:
    instances:
      apiParceiro:
        limit-for-period: 100
        limit-refresh-period: 1s
        timeout-duration: 0
```

Uso com as anotações `@Bulkhead` e `@RateLimiter`. O `@Bulkhead` usa `type = SEMAPHORE` por padrão; para o pool dedicado, declara-se `type = THREADPOOL` e o método retorna `CompletableFuture`:

```java
@Service
public class ConsultaService {

    // SemaphoreBulkhead (default): roda na thread chamadora
    @Bulkhead(name = "servicoPagamentos")
    public Recibo consultarPagamento(String id) {
        return clientePagamentos.buscar(id);
    }

    // ThreadPoolBulkhead: assíncrono, em pool dedicado
    @Bulkhead(name = "servicoRelatorios", type = Bulkhead.Type.THREADPOOL)
    public CompletableFuture<Relatorio> gerarRelatorio(String periodo) {
        return CompletableFuture.completedFuture(
            geradorRelatorios.montar(periodo));
    }

    // RateLimiter: no máximo limit-for-period chamadas por janela
    @RateLimiter(name = "apiParceiro")
    public Cotacao consultarParceiro(String simbolo) {
        return clienteParceiro.cotar(simbolo);
    }
}
```

Tanto `@Bulkhead` quanto `@RateLimiter` aceitam `fallbackMethod`, para devolver uma resposta de degradação em vez de propagar `BulkheadFullException` ou `RequestNotPermitted`. Os padrões compõem entre si — combiná-los com Circuit Breaker, Retry e Timeout, e a ordem em que eles se aninham, é o assunto da próxima nota.

## Armadilhas

### (1) Um único pool compartilhado para tudo

A armadilha que o Bulkhead existe para resolver, e que reaparece quando o padrão é mal aplicado: usar **um só pool de threads para todas as dependências**. Basta um serviço lento para que suas chamadas empilhem, segurem todas as threads e **estrangulem as chamadas saudáveis** às outras dependências. O sintoma é cruel: o painel mostra pagamentos degradado, mas o usuário relata que *o sistema inteiro* parou. A correção é dar a cada dependência seu próprio compartimento — um bulkhead por dependência — para que o esgotamento de uma não vire o esgotamento de todas.

### (2) Rate limit no lugar errado — no cliente em vez da borda

Colocar o RateLimiter **dentro de cada instância do serviço cliente** parece proteger a dependência, mas falha em escala. Se o limite é "100 por segundo" e você tem dez réplicas, cada uma achando que pode mandar 100, a dependência recebe **1000 por segundo** — dez vezes o pretendido. Limites de taxa que precisam valer para *o sistema todo* pertencem a um ponto de coordenação: a **borda** (API Gateway) ou um rate limiter distribuído com estado compartilhado. O RateLimiter do Resilience4j é **por instância, em memória** — excelente para proteger a própria instância de saturar uma dependência, mas não substitui um limite global na borda.

### (3) ThreadPoolBulkhead com chamada que depende do contexto da thread

Por executar numa thread do pool dedicado, o ThreadPoolBulkhead **não carrega o contexto da thread chamadora**. Tudo que mora em `ThreadLocal` — o `SecurityContext` do Spring Security, o contexto de uma transação, dados de tracing/MDC do log — **não atravessa** para a thread do pool. O resultado é insidioso: a chamada executa "sem usuário autenticado", ou fora da transação, ou perde a correlação dos logs, e o bug só aparece em produção sob certas rotas. Se a chamada precisa desse contexto, ou você o propaga explicitamente para o pool, ou usa o **SemaphoreBulkhead**, que roda na thread chamadora e preserva o contexto naturalmente. Isolamento de thread não é grátis: o que ele isola, ele também desconecta.

## Em entrevista

### Frase pronta (inglês)

> The Bulkhead pattern partitions resources so a single slow dependency can't exhaust all the threads and take the whole application down — like the watertight compartments of a ship. In Resilience4j I have two flavors: a SemaphoreBulkhead, which caps concurrency on the calling thread with a semaphore via `maxConcurrentCalls`, and a ThreadPoolBulkhead, which gives the dependency a dedicated thread pool and a bounded queue, running asynchronously. The Rate Limiter solves a different axis: instead of limiting simultaneous calls, it limits how many calls pass per time window, with `limitForPeriod` permits refilled every `limitRefreshPeriod`. One caveat I always flag: the ThreadPoolBulkhead doesn't carry thread-local context like the SecurityContext across to the pool thread, so if the call needs it, I either propagate it explicitly or fall back to the semaphore variant.

### Vocabulário

| Português | Inglês |
| --- | --- |
| anteparo | bulkhead |
| semáforo | semaphore |
| pool de threads | thread pool |
| isolamento | isolation |
| limitador de taxa | rate limiter |
| contexto de thread | thread context |
| esgotamento de recursos | resource exhaustion |
| fila limitada | bounded queue |

## Veja também

- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/13 - Resiliência I — a falha distribuída e o Circuit Breaker|Circuit Breaker]]
- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/16 - Resiliência IV — compondo os padrões|Compondo os padrões de resiliência]]
- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/21 - Os padrões de falha distribuída|Os padrões de falha distribuída]]
- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/index|Microservices e sistemas distribuídos (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]

## Referências

- Resilience4j — Bulkhead. https://resilience4j.readme.io/docs/bulkhead (SemaphoreBulkhead vs ThreadPoolBulkhead; `maxConcurrentCalls`/`maxWaitDuration`; `coreThreadPoolSize`/`maxThreadPoolSize`/`queueCapacity`/`keepAliveDuration` e seus defaults)
- Resilience4j — RateLimiter. https://resilience4j.readme.io/docs/ratelimiter (`limitForPeriod`/`limitRefreshPeriod`/`timeoutDuration`, modelo de ciclos e permissões, defaults)
- Resilience4j — versão 2.4.0, Java 17 (linha de base cravada para os módulos Bulkhead e RateLimiter desta nota)
