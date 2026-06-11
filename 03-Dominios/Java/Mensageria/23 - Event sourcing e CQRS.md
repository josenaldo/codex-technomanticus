---
title: "Event sourcing e CQRS"
fase: magus
tags:
  - java
  - mensageria
  - magus
  - event-sourcing
  - cqrs
created: 2026-06-11
updated: 2026-06-11
type: concept
status: seedling
publish: true
aliases:
  - "Event sourcing"
  - "CQRS"
---

# Event sourcing e CQRS

> [!abstract] TL;DR
> Event Sourcing armazena o histórico de mudanças como uma sequência de eventos imutáveis — o estado atual é derivado do replay. CQRS separa o modelo de escrita do(s) modelo(s) de leitura. Ambos são padrões legítimos e poderosos em contextos específicos; fora desses contextos, adicionam complexidade desproporcional. O default continua sendo CRUD.

## O que é

**Event Sourcing** é um padrão de persistência no qual nenhuma linha é sobrescrita. Em vez disso, cada mudança de estado é registrada como um evento imutável num log append-only. O estado atual de qualquer entidade é obtido fazendo o replay de todos os eventos que a afetam desde o início.

**CQRS** (Command Query Responsibility Segregation) é um padrão arquitetural que separa o caminho de escrita (commands) do caminho de leitura (queries). O write model pode ser um agregado rico, otimizado para invariantes de negócio; os read models (projections) são estruturas desnormalizadas, otimizadas para consulta.

Os dois padrões são frequentemente mencionados juntos porque se complementam bem: o log de eventos do Event Sourcing alimenta naturalmente as projections do CQRS. Mas são independentes — você pode aplicar CQRS sem Event Sourcing e vice-versa.

## Por que importa

Em domínios onde **o log de alterações é o requisito em si** — auditoria financeira, prontuário médico, rastreabilidade de pedidos — Event Sourcing entrega isso de graça. A trilha de auditoria não é uma feature acrescentada depois; ela é a estrutura de dados fundamental.

CQRS aparece quando o write model e o read model têm formas tão diferentes que manter um único modelo ORM começa a gerar código contorcido: joins forçados, DTOs que mimetizam o modelo relacional, projeções SQL ad-hoc espalhadas pelo repositório.

O risco real é aplicar os dois padrões por moda ou por simetria ("o projeto usa Kafka, então vamos fazer Event Sourcing"). Fowler é direto: CQRS pode "levar um sistema a dificuldades sérias" quando aplicado onde o modelo CRUD teria sido suficiente.

## Como funciona

### Event Sourcing — o evento como fonte da verdade

O evento é a unidade de persistência. Um `PedidoConfirmado`, um `EstoqueReservado`, um `PagamentoAprovado` são gravados em ordem no event store. Ninguém sobrescreve o evento; versões posteriores apenas acrescentam novos eventos.

O estado atual do agregado é reconstruído via replay:

```java
// pseudo-código: agregado reconstrói estado a partir do stream de eventos
public class Pedido {
    private UUID id;
    private StatusPedido status;
    private List<ItemPedido> itens;

    public static Pedido reconstituir(List<EventoPedido> eventos) {
        Pedido pedido = new Pedido();
        for (EventoPedido evento : eventos) {
            pedido.aplicar(evento);   // cada evento muta o estado interno
        }
        return pedido;
    }

    private void aplicar(PedidoConfirmado evento) {
        this.id = evento.pedidoId();
        this.status = StatusPedido.CONFIRMADO;
        this.itens = evento.itens();
    }

    private void aplicar(PagamentoAprovado evento) {
        this.status = StatusPedido.PAGO;
    }
    // ... demais handlers
}
```

Para evitar replay completo toda vez, o sistema pode tirar **snapshots** periódicos — um estado serializado num ponto do tempo — e fazer replay só dos eventos posteriores ao snapshot.

### CQRS — separar write model de read models/projections

O write side processa commands e persiste eventos (ou entidades CRUD, dependendo da escolha). O read side consome esses eventos e mantém projeções desnormalizadas, prontas para ser servidas sem joins:

```java
// Projection: ouvinte que mantém a leitura atualizada
@Component
public class PedidoResumoProjection {

    private final PedidoResumoRepository repo;

    @EventHandler
    public void on(PedidoConfirmado evento) {
        PedidoResumo resumo = new PedidoResumo(
            evento.pedidoId(),
            evento.clienteId(),
            evento.total(),
            StatusPedido.CONFIRMADO
        );
        repo.save(resumo);
    }

    @EventHandler
    public void on(PagamentoAprovado evento) {
        repo.atualizarStatus(evento.pedidoId(), StatusPedido.PAGO);
    }
}

// Query side: lê da projeção, não do agregado
@Service
public class PedidoQueryService {

    private final PedidoResumoRepository repo;

    public List<PedidoResumoDTO> listarPorCliente(UUID clienteId) {
        return repo.findByClienteId(clienteId)
                   .stream()
                   .map(PedidoResumoDTO::from)
                   .toList();
    }
}
```

A projeção é eventual — ela será consistente com o write side após a propagação do evento, não instantaneamente.

### Quando NÃO usar

Essa seção é tão importante quanto as anteriores.

**Event Sourcing aumenta a carga operacional** de formas que costumam surpreender:

- **Versionamento de eventos**: quando o schema de `PedidoConfirmado` muda, todos os eventos antigos ainda existem na forma antiga. É preciso upcasters, migrações ou múltiplas versões do evento coexistindo no código.
- **Replay em produção**: se um bug afetou a lógica de um handler, corrigir e fazer replay pode levar horas num volume real de eventos; o sistema fica indisponível ou inconsistente nesse intervalo.
- **Consistência eventual é real**: o read side não reflete imediatamente o write side. Em fluxos onde o usuário escreve e logo lê o que acabou de escrever, isso exige cuidado (leitura do próprio agregado, ou sincronização explícita).
- **Curva de aprendizado**: a equipe toda precisa internalizar o modelo mental; migrações de esquema relacionais viram migrações de schema de evento; debug requer ferramentas específicas.

**CQRS sem um read model que justifique a separação** gera duplicação sem benefício. Se as queries e os commands operam sobre as mesmas entidades com o mesmo shape, um repositório JPA comum é mais simples e mais correto.

O ponto de partida sempre deve ser CRUD. Event Sourcing e CQRS são upgrades cirúrgicos para quando os requisitos exigirem.

## Na prática

Frameworks Java que suportam o modelo:

- **Axon Framework**: framework dedicado a Event Sourcing + CQRS + DDD no ecossistema Spring; event store embutido, suporte a snapshots e sagas.
- **Spring Modulith**: desde a versão GA (Boot 3.2+), oferece eventos de domínio persistidos com suporte a replay dentro de um monólito modular — uma opção mais leve antes de ir para Axon.
- **Kafka como event store improvisado**: funciona para cenários onde a retenção é suficiente, mas Kafka não foi projetado como event store (sem busca por ID de agregado, compactação de tópico não é replay seletivo). Use com consciência das limitações.

Em produção, o padrão costuma aparecer em **bounded contexts específicos** — não no sistema inteiro. O checkout de um e-commerce pode ser event-sourced enquanto o cadastro de produtos usa CRUD normal.

## Armadilhas

### (1) Event Sourcing por moda — complexidade desnecessária

O argumento mais comum para adotar Event Sourcing é "teremos auditoria grátis". Mas se auditoria é o único requisito, uma tabela de histórico (shadow table, trigger, `@SQLInsert` com colunas `created_at`/`updated_by`) resolve com zero overhead arquitetural. Event Sourcing faz sentido quando o **replay em si** tem valor de negócio — não quando o log é apenas um subproduto desejável.

### (2) CQRS sem read model que justifique a separação

Adicionar CQRS num CRUD comum produz dois repositórios, dois serviços, eventos de sincronização e consistência eventual para resolver um problema que uma query JPA com projeção resolveria em dez linhas. O padrão só paga o custo quando as formas do write model e do read model divergem significativamente — domínios com regras de negócio ricas no comando e dashboards agregados complexos na leitura.

### (3) Assumir consistência forte entre write e read

Esse é o erro mais silencioso. Após um command ser aceito, o read model **ainda não reflete a mudança** — a projection é atualizada de forma assíncrona. Se o código assume que um `GET` imediatamente após um `POST` verá o novo estado, o sistema se comporta de forma não determinística sob carga. A solução é ou aceitar a eventual consistency explicitamente na UX, ou ler do próprio agregado (write side) quando consistência imediata for obrigatória.

## Em entrevista

### Frase pronta (inglês)

"Event Sourcing and CQRS are powerful patterns, but I apply them surgically — only in bounded contexts where the audit log or the read/write shape divergence genuinely justifies the overhead. Use it where the audit log *is* the requirement, not by default. The version management of events, the eventual consistency between write and read sides, and the replay infrastructure add costs that a plain CRUD architecture simply doesn't have. My default is always CRUD first, then evolve toward these patterns if the domain demands it."

### Vocabulário

| Termo | Definição rápida |
|---|---|
| Event store | Repositório append-only de eventos imutáveis; unidade fundamental do Event Sourcing |
| Replay | Reprocessar todos os eventos de um agregado para reconstruir seu estado atual |
| Snapshot | Estado serializado num ponto do tempo; evita replay completo a cada leitura |
| Projection (read model) | Visão desnormalizada e otimizada para leitura, mantida por handlers de eventos |
| Upcaster | Componente que transforma eventos de versões antigas para o schema atual durante o replay |
| Eventual consistency | Garantia de que o read model convergirá para o estado correto, mas não instantaneamente após o write |
| Command | Intenção de mudança de estado (write side no CQRS); pode ser rejeitado pelas invariantes do agregado |
| Bounded context | Limite explícito dentro do qual um modelo de domínio é coerente; Event Sourcing/CQRS são aplicados por contexto, não globalmente |

## Veja também

- [[03-Dominios/Java/Mensageria/index|Mensageria (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Mensageria/22 - Saga — transações distribuídas por eventos|Saga]]
- [[03-Dominios/Java/Mensageria/24 - Versionamento e evolução de eventos|Versionamento e evolução de eventos]]
- [[03-Dominios/Java/Dicionário de Java|Dicionário de Java]]

## Referências

- Fowler, Martin. *Event Sourcing*. martinfowler.com/eaaDev/EventSourcing.html (acesso 2026-06-11)
- Fowler, Martin. *CQRS*. martinfowler.com/bliki/CQRS.html (acesso 2026-06-11)
- Axon Framework Documentation. docs.axoniq.io
- Spring Modulith Reference. docs.spring.io/spring-modulith
