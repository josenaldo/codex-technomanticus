---
title: "Consistência em sistemas distribuídos"
created: 2026-06-12
updated: 2026-06-12
type: concept
status: seedling
publish: true
fase: Magus
tags:
  - java
  - microservices
  - magus
  - consistencia
aliases:
  - "CAP theorem"
  - "PACELC"
  - "Consistência eventual"
---

# Consistência em sistemas distribuídos

> [!abstract] TL;DR
> Quando você espalha dados por várias máquinas (ou vários serviços), **consistência deixa de ser grátis**. O **teorema CAP** (Brewer, 2000; provado por Gilbert & Lynch, 2002) diz: durante uma **partição de rede**, você escolhe entre **consistência** e **disponibilidade** — não dá pra ter as duas. A crítica **PACELC** (Abadi, 2010/2012) vai além: **mesmo sem partição**, há um trade-off permanente entre **latência** e **consistência**. Em microsserviços, o padrão **database-per-service** garante que a consistência entre serviços será **eventual** — todo mundo concorda, só não ao mesmo tempo. *Como* reconciliar (saga, outbox, idempotência) é assunto do Galho 14 (Mensageria) — aqui a gente explica *por que* a inconsistência é inevitável.

## O que é

**Consistência** num sistema distribuído é a garantia de que diferentes leitores enxergam o mesmo dado ao mesmo tempo. Quando há um único banco e um único processo, isso é trivial: você escreve, você lê de volta o que escreveu. Quando o dado está replicado em várias máquinas — ou particionado entre vários serviços, cada um com seu próprio banco — manter essa garantia passa a custar **tempo, disponibilidade ou ambos**.

Dois resultados teóricos definem a fronteira do que é possível:

- **CAP** — não dá pra ter consistência forte E disponibilidade total durante uma falha de rede.
- **PACELC** — mesmo quando a rede está saudável, consistência forte custa latência.

E uma decisão arquitetural cotidiana torna isso concreto em microsserviços: o **database-per-service**, que recusa o banco compartilhado e, com isso, abre mão de transações globais. A consequência direta é que, **entre serviços**, a consistência é **eventual** por construção.

> [!note] Feynman
> Imagine que cada serviço tem um caderno de anotações próprio. Quando o `order-service` rabisca "pedido #42 criado", o `inventory-service` ainda não sabe — a notícia precisa *viajar* até ele. Por um instante, os dois cadernos discordam. **Consistência eventual** é a promessa de que, dado tempo suficiente sem novas escritas, os dois cadernos vão dizer a mesma coisa. *Todo mundo concorda — só não ao mesmo tempo.*

## Por que importa

Numa entrevista de nível sênior, "como você garante consistência entre microsserviços?" é uma pergunta-armadilha. A resposta ingênua — "eu uso uma transação distribuída pra tudo ficar atômico" — sinaliza que o candidato **não entendeu CAP**. O ponto que diferencia um sênior é reconhecer que:

1. **A partição não é negociável.** Em qualquer sistema distribuído real, a rede *vai* falhar — pacotes se perdem, links caem, GCs travam um nó por segundos. O "P" do CAP não é uma escolha de design: é uma condição que a realidade impõe. A escolha de verdade é só entre **C** e **A**.
2. **O trade-off existe o tempo todo, não só na falha.** É aqui que o PACELC corrige o CAP. Mesmo com a rede impecável, garantir que toda réplica confirme uma escrita antes de responder ao cliente **adiciona latência**. Consistência forte é um imposto contínuo, não uma fatura que só chega quando algo quebra.
3. **"Eventual" tem prazo, não é "nunca".** Tratar consistência eventual como sinônimo de "tanto faz" é como confundir um cheque pré-datado com um calote.

Quem decide a arquitetura de um sistema de microsserviços está, a cada escolha de comunicação e armazenamento, posicionando o sistema em algum ponto desse espaço de trade-offs — explicitamente ou não.

## Como funciona

### CAP e o que ele realmente diz

Eric Brewer apresentou o **teorema CAP** como conjectura no **PODC 2000** (Symposium on Principles of Distributed Computing); Seth Gilbert e Nancy Lynch, do **MIT**, deram a **prova formal em 2002**, transformando a conjectura em teorema. As três propriedades:

- **Consistency (C)** — toda leitura recebe a escrita mais recente, ou um erro. Todos os clientes veem o mesmo dado, não importa em qual nó se conectem.
- **Availability (A)** — todo nó não-falho responde a toda requisição (a resposta pode não ser a mais recente, mas vem).
- **Partition tolerance (P)** — o sistema continua operando mesmo que mensagens entre nós sejam perdidas ou atrasadas.

O enunciado que importa: **sob uma partição de rede (P), você é forçado a escolher entre C e A**. Se o nó A não consegue falar com o nó B e mesmo assim aceita uma escrita, ele fica **disponível** mas pode divergir de B (sacrifica C). Se ele se recusa a responder enquanto não tem certeza de estar sincronizado, mantém **consistência** mas fica indisponível (sacrifica A).

> [!warning] O "dois de três" é um mito
> Em 2012 o próprio Brewer esclareceu que a leitura popular "escolha 2 das 3 letras" é **enganosa**. A restrição vale **especificamente durante a partição**. Em operação normal, um sistema pode entregar consistência forte E disponibilidade ao mesmo tempo — técnicas de recuperação de partição reconciliam o estado quando a rede volta. P não é uma letra que você "abre mão de ter": em sistemas distribuídos reais, P é dado de fábrica.

### PACELC e a crítica

**Daniel Abadi** (Yale) introduziu o **PACELC** num **blog em 2010**, formalizado num **paper de 2012** (prova formal em 2018). A crítica central, nas palavras dele: *ignorar o trade-off consistência/latência dos sistemas replicados é uma grande omissão do CAP* — porque esse trade-off opera **continuamente**, enquanto partições são **raras**.

O acrônimo se lê assim:

- **PAC** — se há **P**artição, escolha entre **A**vailability e **C**onsistency (isso é o CAP).
- **ELC** — **E**lse (sem partição, o caso comum), escolha entre **L**atency e **C**onsistency.

A genialidade do PACELC é mostrar que o CAP só fala do **caso excepcional** (a falha de rede), enquanto o que de fato domina a experiência do sistema no dia a dia é o **caso normal** — e nesse caso a tensão é **latência vs consistência**. Querer que toda réplica confirme antes de responder = mais consistência, mais latência. Aceitar responder a partir de uma réplica possivelmente defasada = menos latência, menos consistência.

Os quatro perfis resultantes (combinando a escolha sob partição com a escolha em operação normal):

| Perfil | Sob partição | Em operação normal | Exemplos típicos |
|--------|-------------|--------------------|------------------|
| **PA/EL** | prioriza disponibilidade | prioriza latência | Cassandra, Riak, Dynamo inicial |
| **PC/EC** | prioriza consistência | prioriza consistência | PostgreSQL, MySQL Cluster (ACID) |
| **PA/EC** | disponibilidade | consistência | MongoDB, Hazelcast (raro fora de in-memory) |
| **PC/EL** | consistência | latência | PNUTS (o mais difícil de raciocinar) |

> [!tip] A pergunta que o PACELC obriga você a fazer
> Não é só "o que acontece quando a rede cai?". É também: "no dia normal, eu prefiro respostas **rápidas** ou respostas **certas**?". Os dois eixos são independentes — daí o sistema ter *duas* letras (ex.: PA/EL).

### Strong vs eventual consistency e o database-per-service

**Consistência forte (strong consistency)**: depois que uma escrita é confirmada, **toda** leitura subsequente — de qualquer nó — enxerga aquele valor. É o modelo mental de um banco ACID monolítico. O preço é latência (PACELC: o "C" do "EC") e/ou disponibilidade reduzida sob partição (CAP: o "C" do "PC").

**Consistência eventual (eventual consistency)**: na ausência de novas escritas, **dado tempo suficiente**, todas as réplicas convergem para o mesmo valor. Não há garantia de *quando* — só de que converge. É o modelo de sistemas PA/EL, que aceitam divergência temporária em troca de disponibilidade e baixa latência.

O ponto onde isso encontra microsserviços é o **database-per-service**. Martin Fowler descreve o **gerenciamento descentralizado de dados** como um princípio central de microsserviços: cada serviço **dono do seu próprio banco** — instâncias diferentes da mesma tecnologia, ou tecnologias inteiramente distintas — em vez de um banco lógico compartilhado.

A consequência é direta. Sem banco compartilhado, **não existe transação ACID que abrace dois serviços**. Tentar usar transações distribuídas (2PC) entre serviços, nas palavras do próprio Fowler, cria *acoplamento temporal significativo*, que é problemático entre serviços, além de ser *notoriamente difícil de implementar*. Por isso a indústria escolheu o caminho oposto:

> Times de microsserviços preferem **coordenação sem transação entre serviços, com reconhecimento explícito de que a consistência pode ser apenas eventual**, e problemas são tratados por **operações compensatórias**. — Fowler, *Microservices*

Ou seja: o database-per-service **não permite** consistência forte entre serviços. Ele **força** a consistência eventual. Isso não é um bug do estilo arquitetural — é a condição de existência dele. A pergunta deixa de ser "como manter tudo forte e atômico" e passa a ser "como **reconciliar** estados que vão divergir temporariamente".

> [!important] Fronteira de galho — Galho 14 (Mensageria)
> **Como** se reconcilia a consistência entre serviços — o padrão **Saga** (transações distribuídas por eventos), o padrão **Outbox** (publicação confiável de eventos) e **idempotência** (reprocessar sem duplicar efeito) — é território do **Galho 14 (Mensageria)**. Esta nota explica *por que* a inconsistência é inevitável e *qual* é o trade-off; os mecanismos de resolução têm notas próprias. Veja [[03-Dominios/Tecnologia/Java/Mensageria/22 - Saga — transações distribuídas por eventos|Saga (Galho 14)]] e [[03-Dominios/Tecnologia/Java/Mensageria/21 - O padrão Outbox|Outbox (Galho 14)]]. Aqui a gente **linka, não re-deriva**.

## Na prática

### O mapa CAP / PACELC

```text
                    Há partição de rede?
                            |
              +-------------+-------------+
              |                           |
            SIM (P)                    NÃO (Else)
        -- caso raro --            -- caso comum --
              |                           |
        Escolha CAP:               Escolha PACELC:
              |                           |
      +-------+-------+           +--------+--------+
      |               |          |                 |
  CONSISTENCY    AVAILABILITY  LATENCY         CONSISTENCY
  (nó recusa     (nó responde  (responde       (confirma em
   se não tem     mesmo sem     da réplica       todas as
   certeza)       sincronizar)  mais próxima)    réplicas antes)
      |               |          |                 |
     PC              PA         EL                EC

  Perfil do sistema = (escolha sob P) + (escolha no Else)
  ex.: PA/EL = disponível na falha, rápido no normal (Cassandra)
       PC/EC = consistente sempre, ao custo de latência (Postgres)
```

### Dois serviços convergindo

Cenário neutro: criação de um pedido que precisa reservar estoque.

```text
1) Cliente -> order-service:  POST /orders {item: X, qty: 2}
              order-service grava no SEU banco (orders):
                  pedido #42 = PENDING
              responde 201 ao cliente IMEDIATAMENTE
                  (disponibilidade + baixa latência: PA/EL)

   >>> NESTE INSTANTE os dois bancos DISCORDAM <<<
       orders:    pedido #42 existe (PENDING)
       inventory: nada sabe sobre #42

2) order-service emite evento OrderCreated(#42, item X, qty 2)
       (COMO emitir de forma confiável = Outbox, Galho 14)

3) inventory-service consome o evento (assíncrono):
       grava no SEU banco (inventory):
           item X: disponível 100 -> 98 (reservado p/ #42)
       emit StockReserved(#42)

   >>> CONVERGÊNCIA: agora os dois bancos concordam <<<
       orders:    pedido #42 (será confirmado ao receber StockReserved)
       inventory: 2 unidades de X reservadas p/ #42

   Se faltar estoque -> StockReservationFailed(#42)
       -> order-service compensa: pedido #42 = CANCELLED
       (a coreografia/orquestração disso = Saga, Galho 14)
```

A janela entre os passos 1 e 3 é a **inconsistência temporária** — inevitável, porque os bancos são separados (database-per-service) e a notícia viaja por mensagem assíncrona. O sistema é **eventualmente consistente**: dado que o evento será entregue e processado, os dois serviços convergem. O que *garante* essa entrega e essa convergência (idempotência no consumo, reconciliação por saga, publicação atômica via outbox) é o **Galho 14** — não se re-deriva aqui.

## Armadilhas

### (1) Esperar strong consistency entre serviços

A armadilha mais comum: projetar como se o `order-service` pudesse ler o estado do `inventory-service` e ter certeza de que é o estado mais atual, **no mesmo instante**, de forma atômica. Com database-per-service isso é **impossível por construção** — não há transação que abrace os dois bancos. Quem insiste nisso acaba reintroduzindo um banco compartilhado disfarçado (acoplamento de dados) ou um 2PC frágil que reacende o acoplamento temporal que os microsserviços existem para evitar. A postura sênior é **projetar para a divergência temporária**, não tentar aboli-la.

### (2) Ignorar o trade-off latency/consistency do PACELC

Muita gente "conhece o CAP" e acha que terminou a análise — como se o trade-off só existisse durante falhas de rede (que são raras). É exatamente a omissão que Abadi apontou. No **dia normal**, escolher "ler sempre do líder pra garantir o valor mais recente" custa **latência e capacidade**; escolher "ler de qualquer réplica" devolve latência baixa mas pode entregar dado defasado. Ignorar o **ELC** leva a sistemas que parecem corretos no quadro-branco e ficam lentos (ou inconsistentes de forma surpreendente) em produção, **mesmo sem nenhuma partição acontecendo**.

### (3) Usar "eventual" como desculpa pra inconsistência permanente

"É eventualmente consistente" não pode virar carta branca para *nunca* reconciliar. Consistência eventual promete **convergência**: na ausência de novas escritas, o sistema *chega* a um estado único. Se não há mecanismo de reconciliação — sem reprocessamento idempotente, sem retry, sem dead-letter, sem compensação — então não é consistência eventual: é **inconsistência permanente** com nome bonito. "Eventual" tem prazo. Um estado que diverge e nunca converge é um bug, não um modelo de consistência. (Os mecanismos que garantem a convergência são o **Galho 14** — esta nota só te obriga a exigir que eles existam.)

## Em entrevista

### Frase pronta (inglês)

> The CAP theorem tells us that, during a network partition, a distributed system must choose between consistency and availability — partition tolerance isn't optional in any real distributed system, so the genuine choice is only between C and A. But PACELC adds the part most people miss: even with no partition, there's a permanent trade-off between latency and consistency, and that's the one you pay for every single day. In a microservices architecture, the database-per-service pattern means there's no global transaction across services, so consistency between services is eventual by design. My job isn't to eliminate that temporary divergence — it's to make sure the services reliably converge.

### Vocabulário

| Português | Inglês |
|-----------|--------|
| consistência forte | strong consistency |
| consistência eventual | eventual consistency |
| tolerância a partição | partition tolerance |
| disponibilidade | availability |
| banco por serviço | database-per-service |
| latência | latency |
| operação compensatória | compensating operation |
| convergência (de réplicas) | (replica) convergence |

## Veja também

- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/05 - Comunicação inter-serviços — síncrono vs assíncrono|Comunicação inter-serviços]]
- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/21 - Os padrões de falha distribuída|Os padrões de falha distribuída]]
- [[03-Dominios/Tecnologia/Java/Mensageria/22 - Saga — transações distribuídas por eventos|Saga (Galho 14)]]
- [[03-Dominios/Tecnologia/Java/Mensageria/21 - O padrão Outbox|Outbox (Galho 14)]]
- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/index|Microservices e sistemas distribuídos (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]

## Referências

- Wikipedia — *CAP theorem*. <https://en.wikipedia.org/wiki/CAP_theorem> (Brewer, conjectura PODC 2000; prova formal Gilbert & Lynch, MIT, 2002; esclarecimento de Brewer sobre o "dois de três", 2012).
- Wikipedia — *PACELC design principle*. <https://en.wikipedia.org/wiki/PACELC_design_principle> (Daniel Abadi, blog 2010 / paper 2012; prova formal 2018; perfis PA/EL, PC/EC, PA/EC, PC/EL).
- Fowler, Martin & Lewis, James — *Microservices*. <https://martinfowler.com/articles/microservices.html> (gerenciamento descentralizado de dados / database-per-service; consistência eventual e operações compensatórias entre serviços).
