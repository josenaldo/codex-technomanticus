---
title: "Saga — transações distribuídas por eventos"
fase: magus
tags:
  - java
  - mensageria
  - magus
  - saga
created: 2026-06-11
updated: 2026-06-11
type: concept
status: seedling
publish: true
aliases:
  - "Saga"
---

# Saga — transações distribuídas por eventos

> [!abstract] TL;DR
> Quando uma operação de negócio atravessa vários serviços — cada um com seu próprio banco — não dá pra abrir uma transação ACID distribuída barata. A **saga** resolve isso quebrando a operação numa sequência de **transações locais**: cada serviço faz a sua parte, persiste no próprio banco e emite um **evento** que dispara o próximo passo. Se algum passo falha, a saga não faz `ROLLBACK` — ela executa **transações de compensação** que desfazem semanticamente o que já tinha acontecido (estornar um pagamento, liberar um estoque reservado). A coordenação pode ser **coreografada** (serviços reagem a eventos, sem maestro) ou **orquestrada** (um coordenador central comanda os passos). O preço é abrir mão do isolamento: a saga é eventualmente consistente, não atomicamente isolada.

## O que é

Uma **saga** é um padrão de gerenciamento de dados para manter consistência entre serviços **sem** usar uma transação distribuída. Em vez de um único `BEGIN ... COMMIT` que abrange todos os bancos, a saga é uma **sequência de transações locais**. Cada transação local atualiza o banco de **um** serviço e, ao terminar, publica uma mensagem ou evento que aciona a próxima transação local da sequência.

A diferença crucial em relação a uma transação tradicional está no caminho de erro. Numa transação ACID, se algo dá errado o banco desfaz tudo automaticamente. Numa saga não existe esse rollback global: se um passo falha por violar uma regra de negócio, a saga precisa executar **transações de compensação** que desfazem, uma a uma, as transações locais que já tinham sido confirmadas. Esse "desfazer" não é técnico (não é um rollback de banco) — é **semântico**, expresso na linguagem do domínio.

Saga é o padrão irmão do [[03-Dominios/Tecnologia/Java/Mensageria/21 - O padrão Outbox|O padrão Outbox]]: cada passo da saga precisa atualizar o banco **e** publicar um evento de forma confiável, e é exatamente esse problema de atomicidade local que o Outbox resolve.

## Por que importa

Arquiteturas baseadas em mensageria empurram o sistema na direção de **um banco por serviço**. Isso é ótimo para acoplamento e escala, mas mata a transação distribuída como ferramenta padrão: você não pode mais envolver "reservar estoque", "cobrar o cartão" e "agendar a entrega" numa única transação que ou acontece inteira ou não acontece, porque essas operações vivem em bancos diferentes, possivelmente em serviços diferentes.

A saga é a resposta canônica a essa restrição. Sem ela, as alternativas são piores: ou você volta a um banco monolítico compartilhado (perdendo a autonomia dos serviços), ou tenta colar tudo com 2PC (que não escala e cria pontos de falha). A saga aceita o trade-off honestamente — abre mão da consistência forte imediata em troca de consistência **eventual** — e dá um vocabulário claro (passos + compensações) para raciocinar sobre o que acontece quando algo falha no meio de uma operação multi-serviço.

Em entrevista, dominar saga sinaliza que você entende o custo real de quebrar um monólito: não é só "dividir o código", é repensar transações.

## Como funciona

### Por que não há ACID entre serviços

Numa arquitetura de microsserviços bem feita, **cada serviço tem seu próprio banco de dados** e ninguém de fora acessa esse banco diretamente. Essa é justamente a fronteira que dá autonomia ao serviço. Mas ela também elimina a transação ACID como recurso entre serviços: não existe um `BEGIN` que abranja o banco do `Order`, o do `Payment` e o do `Shipment` ao mesmo tempo.

A saída teórica seria uma transação distribuída via **2PC (two-phase commit)**, em que um coordenador pergunta a todos os participantes se podem confirmar e só então manda confirmar. O problema é prático: 2PC **não escala** bem e introduz acoplamento temporal forte — durante a fase de preparação, recursos ficam travados esperando o coordenador, e se o coordenador cai no meio, os participantes ficam em dúvida. Por isso, no mundo de microsserviços, **2PC não é uma opção** no caminho padrão. A saga existe exatamente para preencher esse vácuo.

> [!info] Isolamento é o que se perde
> A saga mantém **atomicidade** (via compensação) e consistência eventual, mas abre mão do **I** de ACID — o **isolamento**. Como os passos confirmam um a um, um observador externo pode ver estados intermediários (um pedido já criado mas ainda não pago). Mitigar isso exige contramedidas explícitas de design, não vem de graça.

### Saga = transações locais + eventos

A unidade de trabalho da saga é a **transação local**: uma operação que toca **um único** banco e, portanto, pode ser ACID de verdade dentro daquele serviço. A saga encadeia essas unidades.

O mecanismo de encadeamento é mensageria: ao confirmar sua transação local, o serviço **emite um evento**, e esse evento é o gatilho do próximo passo. Order cria o pedido e emite `OrderCreated`; quem escuta `OrderCreated` faz a sua transação local e emite o próximo evento; e assim por diante. Não há um `COMMIT` global — há uma cadeia de commits locais costurados por eventos.

É aqui que a saga encosta no Outbox: para que "atualizar o banco" e "publicar o evento" não fiquem dessincronizados (banco salvo mas evento perdido, ou vice-versa), cada passo deve escrever evento e estado **atomicamente**. Sem isso, a saga trava ou duplica.

### Coreografia vs orquestração

Há dois estilos de coordenar quem dispara o quê.

Na **coreografia**, não existe maestro. Cada serviço **reage a eventos** e publica os seus, e a saga "acontece" como efeito emergente dessas reações. É descentralizado e tira pontos centrais do caminho — mas a lógica do fluxo fica **espalhada** entre os serviços, e ninguém detém uma visão única de "em que passo a saga está".

Na **orquestração**, existe um **orquestrador** central: um componente que conhece o fluxo inteiro, comanda cada passo ("`Payment`, cobre isso") e recebe as respostas, decidindo aprovar ou compensar. A lógica fica **centralizada e visível** num só lugar — ao custo de introduzir esse coordenador como peça adicional, que precisa ser cuidada para não virar gargalo nem ponto único de falha.

| Eixo | Coreografia | Orquestração |
|---|---|---|
| Controle do fluxo | Distribuído entre serviços | Centralizado no orquestrador |
| Acoplamento | Baixo entre serviços, alto via eventos | Serviços acoplados ao orquestrador |
| Visibilidade do estado | Difícil — ninguém tem o todo | Fácil — o orquestrador sabe |
| Risco | Vira "spaghetti" de eventos | Orquestrador vira ponto crítico |

Não há vencedor universal: coreografia brilha em sagas curtas e simples; orquestração paga seu custo quando o fluxo é longo, condicional ou precisa de auditoria.

### Compensação

Quando um passo falha por uma regra de negócio (estoque insuficiente, cartão recusado), a saga precisa desfazer os passos anteriores que já confirmaram. Como esses passos foram **commits locais reais**, não dá pra "dar rollback" neles. A saga executa, então, **transações de compensação**: novas transações locais que produzem o efeito **inverso** do ponto de vista do negócio.

O ponto-chave é que a compensação é um **undo semântico**, não um rollback técnico. Estornar um pagamento não apaga o registro da cobrança — cria um **estorno**. Liberar estoque reservado não desfaz a reserva no log — emite uma **liberação**. O desenvolvedor precisa **projetar explicitamente** cada compensação; ela não vem de graça do banco como o `ROLLBACK` viria. Passos que não têm como ser compensados (já enviou o produto físico, por exemplo) precisam ser ordenados o mais tarde possível na saga, ou tratados como pontos de não-retorno.

## Na prática

Considere uma saga de **criação de pedido** com três passos e suas compensações. Domínios neutros: `Order`, `Payment`, `Shipment`.

Fluxo feliz e caminho de compensação:

```text
Saga: Criar Pedido (coreografada)

  [Order]            [Inventory]          [Payment]           [Shipment]
    |                    |                    |                   |
 cria pedido             |                    |                   |
 (PENDING) ──OrderCreated──>                  |                   |
    |               reserva estoque           |                   |
    |               ──StockReserved──────────>                    |
    |                    |               cobra cartão             |
    |                    |               ──PaymentDone──────────> |
    |                    |                    |              agenda entrega
    |                    |                    |              ──Shipped──> [Order: CONFIRMED]

Caminho de falha (cartão recusado no passo de Payment):

   PaymentFailed
        │
        ▼
  compensação: liberar estoque (StockReleased)  →  Order: CANCELLED
        │
        └─ NÃO há cobrança a estornar (o passo falhou antes de cobrar)
```

Esboço em Java (coreografia via listeners de eventos; baseline Spring Boot 3.x):

```java
// Passo 1 — Order Service: transação local + evento
@Service
public class OrderSaga {

    @Transactional
    public void criarPedido(NovoPedido cmd) {
        Order order = orderRepo.save(Order.pendente(cmd));
        // publicado via Outbox para garantir atomicidade banco+evento
        eventPublisher.publish(new OrderCreated(order.id(), order.itens()));
    }

    // Passo 1 reage ao fim da cadeia
    @EventListener
    @Transactional
    public void onShipped(Shipped ev) {
        orderRepo.confirmar(ev.orderId());
    }

    // Compensação: alguém falhou lá na frente
    @EventListener
    @Transactional
    public void onSagaFailed(OrderSagaFailed ev) {
        orderRepo.cancelar(ev.orderId(), ev.motivo()); // undo semântico
    }
}

// Passo 2 — Inventory Service
@Service
public class InventorySaga {

    @EventListener
    @Transactional
    public void onOrderCreated(OrderCreated ev) {
        try {
            inventoryRepo.reservar(ev.orderId(), ev.itens());
            eventPublisher.publish(new StockReserved(ev.orderId()));
        } catch (EstoqueInsuficiente e) {
            // dispara a compensação rio acima
            eventPublisher.publish(new OrderSagaFailed(ev.orderId(), "sem estoque"));
        }
    }

    // Compensação deste passo, acionada se um passo POSTERIOR falhar
    @EventListener
    @Transactional
    public void onPaymentFailed(PaymentFailed ev) {
        inventoryRepo.liberar(ev.orderId()); // StockReleased: undo semântico
    }
}
```

Repare que cada listener é uma **transação local** própria e que cada publicação de evento deveria sair por um Outbox — não por um `publish` direto que pode se perder se o serviço cair logo após o `COMMIT`.

## Armadilhas

### (1) Saga sem compensação

Implementar só o caminho feliz e esquecer as transações de compensação deixa o sistema num **estado inconsistente permanente** quando algo falha no meio: estoque reservado para um pedido que nunca será pago, pagamento feito para uma entrega que nunca sairá. Como não existe rollback automático entre serviços, **toda** transação local que possa precisar ser desfeita exige uma compensação correspondente, projetada à mão. A saga só está completa quando o caminho de erro está completo.

### (2) Coreografia virando spaghetti de eventos

A coreografia é sedutora porque "não precisa de coordenador", mas em fluxos longos ela espalha a lógica do processo por todos os serviços. Sem um lugar único que descreva a saga, ninguém consegue responder "em que passo este pedido está?" nem "por que ele travou?". O resultado é um **emaranhado de eventos sem visibilidade**, difícil de depurar e de evoluir. Quando o número de passos e ramificações cresce, esse é o sinal de que a orquestração passou a valer seu custo.

### (3) Orquestrador como ponto único de falha

A orquestração resolve a visibilidade, mas concentra poder. Se o orquestrador for mal projetado, ele vira **ponto único de falha** (caiu o orquestrador, nenhuma saga progride) e fonte de **acoplamento** (todo serviço passa a depender de ser comandado por ele). O orquestrador precisa ser tão resiliente quanto qualquer serviço crítico: persistir o estado da saga, ser capaz de retomar de onde parou e não guardar estado só em memória.

## Em entrevista

### Frase pronta (inglês)

A saga is a way to keep data consistent across services without using a distributed transaction, because in a microservices architecture each service owns its database and two-phase commit doesn't scale. Instead of one global commit, a saga is a sequence of local transactions, and each transaction publishes an event that triggers the next step. If a step fails, there is no automatic rollback — the saga runs compensating transactions that semantically undo the previous steps, like issuing a refund instead of deleting a charge. You can coordinate it by choreography, where services just react to each other's events, or by orchestration, where a central coordinator drives the steps; the trade-off is decentralization and low coupling versus visibility and explicit control.

### Vocabulário

| Termo (EN) | Tradução / sentido |
|---|---|
| local transaction | transação local; toca um único banco, é ACID dentro do serviço |
| compensating transaction | transação de compensação; desfaz semanticamente um passo já confirmado |
| choreography | coreografia; serviços reagem a eventos, sem coordenador central |
| orchestration | orquestração; um coordenador central comanda os passos |
| eventual consistency | consistência eventual; estados intermediários são observáveis |
| lack of isolation | ausência de isolamento; o "I" de ACID que a saga abre mão |

## Veja também

- [[03-Dominios/Tecnologia/Java/Mensageria/index|Mensageria (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Mensageria/21 - O padrão Outbox|O padrão Outbox]]
- [[03-Dominios/Tecnologia/Java/Mensageria/23 - Event sourcing e CQRS|Event sourcing e CQRS]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java|Dicionário de Java]]
- Microsserviços e Spring Cloud — o galho [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/index|Microservices e sistemas distribuídos]] trata a coordenação de sagas no contexto da plataforma de microsserviços.

## Referências

- Richardson, Chris. *Pattern: Saga*. microservices.io — https://microservices.io/patterns/data/saga.html
