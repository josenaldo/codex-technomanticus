---
title: "Os padrões de falha distribuída"
created: 2026-06-12
updated: 2026-06-12
type: concept
status: seedling
publish: true
fase: magus
tags:
  - java
  - microservices
  - magus
  - resiliencia
aliases:
  - "Padrões de falha distribuída"
  - "Cascading failure"
---

# Os padrões de falha distribuída

> [!abstract] TL;DR
> As notas 13-16 deste galho te deram as **ferramentas** da resiliência (Circuit Breaker, Retry, Time Limiter, Bulkhead, Rate Limiter) e como configurá-las no Resilience4j. Esta nota sobe um nível: ela amarra essas peças numa **postura de arquitetura**. A tese é que, num sistema distribuído, falha não é exceção — é o **estado normal de operação**. Quatro princípios sustentam um sistema que sobrevive a isso: **(1) toda chamada remota tem timeout** (esperar para sempre é o pecado original); **(2) retries só em operações idempotentes e com backoff** (→ Galho 14), senão viram *retry storm*; **(3) o Circuit Breaker existe para quebrar a falha em cascata**, isolando o serviço doente antes que ele esgote os pools de quem o chama; **(4) sob saturação, o sistema degrada graciosamente** em vez de cair inteiro — e o limite de "quanto ele aguenta" é a **backpressure**, conceito que a [[03-Dominios/Tecnologia/Java/Programação Reativa/index|Programação Reativa]] modela no nível de stream. Resiliência madura não é "ligar todas as anotações"; é decidir **conscientemente** como cada falha se propaga — ou não.

## O que é

Os **padrões de falha distribuída** são o conjunto de decisões arquiteturais que governam o que acontece quando — não *se* — uma chamada remota falha. Eles não são uma biblioteca nem uma anotação; são uma **forma de pensar** o sistema, da qual o Resilience4j é apenas a implementação tática.

A intuição central foi cristalizada por Michael Nygard (*Release It!*) e popularizada por Martin Fowler: num sistema monolítico, chamar um componente é uma invocação de método, e ou ela funciona ou lança uma exceção na hora. Num sistema distribuído, a chamada atravessa a **rede**, e a rede tem um terceiro estado além de "sucesso" e "erro": o **silêncio**. O serviço-alvo pode não responder — nem com sucesso, nem com erro. Ele simplesmente *pendura* a sua chamada. E é esse terceiro estado, o pendurar, que destrói sistemas distribuídos.

Os quatro padrões desta nota — timeout, retry seguro, circuit breaker, graceful degradation — existem todos para domar esse terceiro estado. As notas [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/13 - Resiliência I — a falha distribuída e o Circuit Breaker|13]] a [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/16 - Resiliência IV — compondo os padrões|16]] ensinaram *como* cada um funciona no Resilience4j (versão estável **2.4.0**, baseline Java 17). Esta nota é a **síntese de arquitetura**: como eles se encaixam numa postura coerente.

> [!info] A pergunta que esta nota responde
> Não "como configuro um Circuit Breaker?" (isso é a nota 13), mas "**quando uma chamada remota falha, que sequência de defesas o meu sistema deveria ter, e por quê?**". É a diferença entre conhecer as peças e entender o jogo.

## Por que importa

A **falácia número um** da computação distribuída é "a rede é confiável". Toda arquitetura distribuída ingênua é construída, sem perceber, sobre essa mentira. O resultado é um sistema que funciona lindamente na demo — onde tudo está na mesma máquina e responde em microssegundos — e desmorona em produção no primeiro pico de latência de um serviço a jusante.

O custo de não pensar nisso não é "um erro 500 ocasional". É a **falha em cascata**: um único serviço lento que, através das chamadas síncronas que o atravessam, derruba serviços perfeitamente saudáveis um a um, até a aplicação inteira parar. Um incidente de produção típico não começa com "o banco caiu"; começa com "um serviço de recomendação ficou 2 segundos mais lento" — e termina com o checkout fora do ar, porque o caminho da falha não foi pensado.

Do ponto de vista de **senioridade** (esta é uma nota *magus*), o que separa um engenheiro pleno de um sênior aqui não é saber decorar um método com `@CircuitBreaker`. É olhar para um diagrama de arquitetura e conseguir apontar: *"esta chamada síncrona sem timeout é uma bomba-relógio; este retry sem idempotência vai duplicar pedidos sob estresse; e se este serviço saturar, o sistema inteiro cai em vez de degradar"*. Resiliência é uma propriedade do **desenho**, não das anotações.

## Como funciona

### Timeout em toda chamada remota — o princípio fundador

Se você só puder lembrar de **uma** regra de sistemas distribuídos, que seja esta: **nenhuma chamada remota pode esperar para sempre**. Toda chamada de rede — HTTP, gRPC, query a banco, leitura de fila — precisa de um **tempo limite** explícito. Não existe "sem timeout"; existe "timeout que você definiu" ou "timeout que o sistema operacional vai impor depois de minutos, tarde demais".

A razão é a economia de **threads**. Cada chamada síncrona pendente segura uma thread (ou uma conexão do pool) bloqueada, esperando. Threads são finitas. Se o serviço-alvo fica lento e suas chamadas não têm timeout, suas threads vão sendo consumidas uma a uma até o pool esgotar — e aí o **seu** serviço para de responder a *qualquer* requisição, inclusive as que nada têm a ver com o serviço lento. Foi assim que a doença do vizinho virou a sua.

> [!tip] A intuição contra-intuitiva (vale repetir)
> Um serviço **lento** é mais perigoso que um serviço **morto**. O morto te devolve um erro de conexão na hora — você falha rápido e libera a thread. O lento *segura* sua thread por 30 segundos, e é assim que ele te arrasta para o fundo. Por isso o timeout não é opcional: ele é o que **converte "lentidão" em "falha rápida e tratável"**.

No Resilience4j, esse papel é do **Time Limiter** (nota 14), que atua sobre chamadas assíncronas (`CompletableFuture`). Mas o princípio é maior que a biblioteca: o cliente HTTP tem timeout de conexão e de leitura; o driver do banco tem timeout de query; a chamada à fila tem timeout de poll. **Timeout é um requisito em cada camada**, não uma feature de uma delas.

### Cascading failure e o circuit breaker

A **falha em cascata** (cascading failure) é o modo de falha que mata sistemas distribuídos, e funciona em três tempos:

1. **Saturação local.** Um serviço B fica lento. O serviço A, que chama B de forma síncrona, acumula threads bloqueadas esperando B.
2. **Propagação.** O pool de A esgota. Agora A também está lento/indisponível — não porque A tem um bug, mas porque está todo *preso* esperando B.
3. **Contágio.** O serviço C, que chama A, repete o ciclo. A falha **sobe a árvore de dependências**, um nó de cada vez, até a borda do sistema.

O **Circuit Breaker** (nota 13) é a ferramenta que **quebra essa cadeia** no passo 1, antes que vire passo 2. Ele monitora a taxa de falha (e de chamadas lentas) de B e, quando ela estoura um limiar, **abre o circuito**: passa a rejeitar as chamadas a B *instantaneamente*, sem bloquear thread alguma. Dois efeitos simultâneos:

- **A se protege:** suas threads não ficam presas esperando B; A continua respondendo ao resto.
- **B ganha trégua:** em vez de receber uma enxurrada de chamadas (e retries) enquanto agoniza, B fica sem tráfego e tem chance de se recuperar. Periodicamente, o disjuntor entreabre (HALF_OPEN) e testa se B voltou.

O detalhe arquitetural fino: o circuit breaker **não conserta** a falha de B. Ele faz algo mais humilde e mais importante — ele **contém o raio de explosão**. A falha continua existindo em B, mas para de se espalhar. Esse é o coração da arquitetura resiliente: você não evita falhas (impossível), você **isola** cada uma para que não derrube o todo. É a **isolamento de falha** (fault isolation), o mesmo princípio que o Bulkhead (nota 15) aplica aos pools de recursos.

> [!note] Retry idempotente entra aqui — mas como arma de fogo amigo
> O Retry (nota 14) é a defesa contra falhas **transitórias** (um soluço de rede, um pod reiniciando). Mas, no nível de arquitetura, ele é também a **fonte mais comum de fogo amigo**: dois riscos. Primeiro, retry numa operação não-idempotente **duplica efeitos** (dois pagamentos) — por isso idempotência é pré-requisito, e o assunto é cravado no Galho 14: [[03-Dominios/Tecnologia/Java/Mensageria/20 - Idempotência — o pilar do at-least-once|Idempotência (Galho 14)]]. Segundo, retry sem backoff **amplifica** a sobrecarga: mil clientes repetindo em sincronia num serviço que cambaleia o derrubam de vez (*retry storm*). A composição importa: o Circuit Breaker deve ser o "freio" que corta o retry quando B está claramente caído, em vez de deixar o retry martelá-lo (ver a ordem dos aspectos na nota 16).

### Backpressure distribuído e graceful degradation

Timeout, circuit breaker e retry seguro lidam com o **alvo** falhando. Mas há o lado oposto: e quando é **você** que está recebendo mais do que aguenta? Esse é o domínio da **backpressure** (contrapressão) e da **graceful degradation** (degradação graciosa).

**Backpressure** é o mecanismo pelo qual um consumidor sobrecarregado **sinaliza ao produtor que diminua o ritmo**, em vez de aceitar tudo e estourar a memória. No nível de um stream — `request(n)`, estratégias `BUFFER`/`DROP`/`LATEST` — esse é exatamente o assunto do **Galho 11 (Programação Reativa)**, e eu **não vou re-explicar o modelo interno aqui**: veja [[03-Dominios/Tecnologia/Java/Programação Reativa/09 - Backpressure — request(n) e as estratégias BUFFER, DROP, LATEST|Backpressure (Galho 11)]]. O que importa nesta nota é a **leitura de arquitetura**: a backpressure de um stream reativo é a versão fina e local de um princípio distribuído maior — **um sistema saudável tem um limite explícito de quanto trabalho aceita, e rejeita/enfileira o excedente em vez de aceitar tudo e cair**.

> [!info] Da fronteira reativa à fronteira de sistema
> O Galho 11 modela backpressure **dentro de um processo**, entre um `Publisher` e um `Subscriber`. No nível **distribuído**, a mesma ideia reaparece com outros nomes: o **Rate Limiter** (nota 15) é backpressure no sentido "não aceito mais que N chamadas por segundo"; o **Bulkhead** é backpressure no sentido "não rodo mais que N chamadas concorrentes — o resto espera ou é rejeitado". São todos o mesmo princípio — *limitar a entrada para proteger o núcleo* — em escalas diferentes. É aqui que o gancho que a trilha Reativa deixou se fecha: backpressure não é um detalhe de Reactor; é uma **lei de arquitetura distribuída**.

**Graceful degradation** é a outra metade. Quando uma dependência falha (ou você precisa rejeitar carga), a pergunta não é "como evito o erro?" mas "**o que entrego no lugar?**". A resposta madura quase nunca é "propagar um 500". É:

- um **valor de cache** (possivelmente *stale*, marcado como tal);
- uma **resposta parcial** (a página carrega sem o bloco de recomendações);
- um **status honesto de contingência** ("pagamento pendente", "processaremos em instantes");
- um **enfileiramento assíncrono** (Fowler cita a autorização de cartão que vai para uma fila e é resolvida depois).

A regra de ouro: o fallback deve **degradar com integridade**, nunca **mentir**. Um fallback que devolve "pago" quando o serviço de pagamento está caído é pior que o erro — cria uma inconsistência silenciosa que só aparece na conciliação, dias depois (cravado na armadilha 3 da nota 16). Degradar é entregar *menos*, com honestidade; não é *fingir* que entregou tudo.

## Na prática

Não há código novo aqui — o código é o das notas 13-16. O que esta nota agrega é o **diagrama mental**. Primeiro, a anatomia de uma falha em cascata, e onde cada padrão a interrompe:

```text
SEM RESILIÊNCIA — a cascata
─────────────────────────────────────────────
  [checkout] ──> [order] ──> [payment]  ⚡ lento (2s+)
                                │
   payment fica lento ─────────┘
        │
        ▼  order acumula threads bloqueadas esperando payment
   [order] pool de threads ESGOTA → order para de responder
        │
        ▼  checkout acumula threads esperando order
   [checkout] pool ESGOTA → sistema inteiro fora do ar
        │
        ▼
   ☠  UM serviço lento derrubou TRÊS

COM RESILIÊNCIA — a cascata contida
─────────────────────────────────────────────
  [checkout] ──> [order] ──> [payment]  ⚡ lento
                    │
                    ├─ (1) TIMEOUT: corta a espera em 2s → falha rápida
                    │       (thread liberada, não fica presa)
                    │
                    ├─ (2) CIRCUIT BREAKER: detecta payment doente,
                    │       ABRE → rejeita em µs, sem tocar payment
                    │       (payment ganha trégua p/ se recuperar)
                    │
                    ├─ (3) RETRY: só se idempotente + backoff
                    │       (NUNCA martela payment caído → CB barra)
                    │
                    └─ (4) FALLBACK: "pagamento pendente"
                            → order responde, checkout responde
                    ▼
   ✓  payment falha SOZINHO; o resto degrada, mas vive
```

A leitura: a falha do `payment` **continua acontecendo** — a resiliência não a apaga. O que muda é que ela fica **confinada** ao `payment`, e os serviços acima dele entregam uma experiência degradada porém viva, em vez de morrerem junto.

Em configuração, essa postura aparece como **timeout em toda camada**, não só na anotação Resilience4j:

```yaml
# A disciplina de timeout NÃO mora num lugar só — ela permeia o stack
resilience4j:
  timelimiter:
    instances:
      paymentService:
        timeout-duration: 2s        # corte da chamada lógica (Time Limiter)

spring:
  cloud:
    openfeign:
      client:
        config:
          payment-service:
            connect-timeout: 1000   # ms — não pendurar abrindo conexão
            read-timeout: 2000      # ms — não pendurar esperando resposta
  datasource:
    hikari:
      connection-timeout: 3000      # ms — nem o pool do banco espera p/ sempre
```

> [!tip] O cheiro de código a caçar numa revisão de arquitetura
> Numa revisão sênior, o primeiro grep mental é por **chamadas remotas sem timeout**: um `RestClient`/`WebClient`/driver sem timeout configurado é uma bomba-relógio. O segundo é por **`@Retry` em mutações sem idempotência**. O terceiro é por **fallbacks que mentem** (devolvem sucesso falso). Esses três cobrem a maioria dos incidentes de cascata.

## Armadilhas

### (1) Chamada remota sem timeout — a thread presa para sempre

Esta é a **mãe de todas as armadilhas distribuídas**. Uma única chamada de rede sem timeout explícito é uma thread que pode ficar bloqueada indefinidamente. Sob um serviço lento, essas threads presas se acumulam até esgotar o pool — e então *seu* serviço para de responder a tudo, contaminado por um problema que era de outro. O erro é insidioso porque **não aparece em testes**: na demo o alvo responde rápido, e o timeout ausente nunca é exercitado. Só sob estresse de produção a bomba dispara. Regra absoluta: **toda** chamada remota — HTTP, gRPC, banco, fila, cache — tem timeout de conexão *e* de leitura. "Sem timeout" não é um default aceitável; é um bug latente.

### (2) Degradação que vira falha total por falta de fallback

Aplicar Circuit Breaker, Time Limiter e Bulkhead sem definir o **que entregar quando eles disparam** é meia resiliência. O disjuntor abre, o Resilience4j lança `CallNotPermittedException`, e — sem `fallbackMethod` — essa exceção **propaga para cima exatamente como o erro original propagaria**. Você gastou esforço protegendo o *recurso* (threads não ficam presas), mas o *usuário* continua recebendo um 500. Pior: a falha que deveria ficar contida num bloco da página (as recomendações sumirem) derruba a página inteira, porque ninguém definiu o caminho degradado. Resiliência sem graceful degradation é como um air bag que infla mas não amortece. Para **cada** ponto protegido, decida: cache stale? resposta parcial? status de contingência? fila assíncrona? A ausência dessa decisão é a decisão de cair.

### (3) Retry amplificando a sobrecarga — a retry storm

O retry é a defesa que mais facilmente vira ataque. Sob uma falha transitória, repetir ajuda. Sob uma **saturação real**, repetir é gasolina no incêndio: um serviço cambaleia, centenas de clientes começam a repetir — muitas vezes em sincronia, todos no mesmo intervalo fixo — e o pico de tráfego que o retry gera é **maior** que o tráfego normal que o serviço já não estava dando conta. Ele afunda de vez. É a *retry storm*, o remédio virando veneno. A defesa é tripla e **arquitetural**, não só de config: **backoff exponencial** (cada falha aumenta o intervalo, aliviando o alvo), **jitter** (aleatoriedade que dessincroniza os clientes) e — no nível de sistema — um **orçamento de tentativas** (retry budget): um teto global de quantas retentativas o sistema permite, para que o tráfego de retry nunca passe de uma fração pequena do tráfego total. E, acima de tudo, o **Circuit Breaker deve abortar o retry** quando o alvo está claramente caído: não adianta tentar de novo numa porta que comprovadamente não abre. Os detalhes de backoff/jitter estão na [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/14 - Resiliência II — Retry e Time Limiter|nota 14]].

## Em entrevista

### Frase pronta (inglês)

> My mental model for distributed systems is that failure is the normal operating state, not the exception — so I design for it rather than hope to avoid it. The foundational rule is that no remote call may wait forever: every network call gets an explicit timeout, because a slow downstream is more dangerous than a dead one — it holds your threads hostage until the pool exhausts and a cascading failure spreads up the dependency tree. The Circuit Breaker is what breaks that chain: it isolates the unhealthy service, rejects calls instantly instead of blocking, and gives the failing service room to recover — it doesn't fix the failure, it contains the blast radius. Retries are powerful but they're the most common source of friendly fire, so I only retry idempotent operations, always with exponential backoff and jitter, and I let the Circuit Breaker cut the retry off when the target is clearly down, otherwise I'm creating a retry storm. Finally, when a system is saturated it should degrade gracefully rather than collapse — serve stale cache, a partial response, or an honest "pending" status — and that limit on how much work a system accepts is backpressure, which the reactive stack models at the stream level but is really a law of distributed architecture.

### Vocabulário

| Português | Inglês |
| --- | --- |
| tempo limite | timeout |
| falha em cascata | cascading failure |
| contrapressão | backpressure |
| degradação graciosa | graceful degradation |
| orçamento de tentativas | retry budget |
| isolamento de falha | fault isolation |
| raio de explosão | blast radius |
| esgotamento do pool de threads | thread pool exhaustion |
| tempestade de retentativas | retry storm |

## Veja também

- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/13 - Resiliência I — a falha distribuída e o Circuit Breaker|Circuit Breaker]]
- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/16 - Resiliência IV — compondo os padrões|Compondo os padrões de resiliência]]
- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/20 - Consistência em sistemas distribuídos|Consistência distribuída]]
- [[03-Dominios/Tecnologia/Java/Programação Reativa/index|Programação Reativa (Galho 11)]]
- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/index|Microservices e sistemas distribuídos (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]

> [!note] Onde isto se encaixa
> Esta nota é a **síntese de arquitetura** da resiliência: ela amarra os padrões táticos das notas 13-16 numa postura coerente e fecha o gancho que a trilha **Reativa (Galho 11)** deixou na backpressure. Daqui, o galho segue para segurança entre serviços (nota 17) e tracing distribuído (notas 18-19) — porque resiliência sem **observabilidade** é cega: você não pode conter o que não consegue ver. Operar resiliência em escala envolve [[03-Dominios/Tecnologia/Java/Cloud-native e produção/16 - OpenTelemetry Collector e sampling de produção|coletores]] e [[03-Dominios/Tecnologia/Java/Cloud-native e produção/15 - Dashboards e alertas — Grafana|dashboards]] — assunto do **Galho 17**; já *chaos engineering* fica fora do escopo desta trilha.

## Referências

- Martin Fowler — [CircuitBreaker](https://martinfowler.com/bliki/CircuitBreaker.html) (timeouts, supervisão, fallback/graceful degradation, monitoramento e proteção de recursos; baseado em Michael Nygard, *Release It!*). Acesso em 2026-06-12.
- Resilience4j — [Documentação / Overview](https://resilience4j.readme.io/docs) (os cinco padrões compostos — Circuit Breaker, Retry, Bulkhead, Rate Limiter, Time Limiter — e a filosofia "pick what you need"; linha estável **2.x**, baseline Java 17). Acesso em 2026-06-12.
- Versões cravadas nas notas 13-16: Resilience4j **2.4.0** (mar/2025), baseline **Java 17**; não há linha 3.x estável lançada (verificado em 2026-06-12).
