---
title: "Arquitetura de Software"
created: 2026-04-01
updated: 2026-04-10
type: concept
status: evergreen
tags:
  - arquitetura
  - entrevista
publish: false
---

# Arquitetura de Software

Decisões estruturais de alto nível sobre como um sistema é organizado — estilos, padrões, princípios, documentação e evolução. Enquanto [[System Design]] foca em **construir sistemas para atender requisitos de escala**, arquitetura de software foca em **como organizar o código e os times** para que o sistema sobreviva anos de evolução, mudanças de requisitos e rotação de pessoas.

## O que é

Arquitetura de software é o conjunto de decisões de alto nível que são **caras de mudar depois** — a forma como o sistema é decomposto, como os componentes se comunicam, e os princípios que guiam a evolução. Ralph Johnson disse: "Architecture is the decisions that you wish you could get right early, because they're painful to change later."

Em entrevistas, o que diferencia um senior:

1. **Saber quando NÃO arquitetar** — a arquitetura deve ser proporcional à complexidade do problema. Clean Architecture pura num CRUD de 3 endpoints é over-engineering.
2. **Conhecer os trade-offs** — toda decisão arquitetural tem custo. Saber articular isso é senioridade.
3. **Evolução sobre perfeição** — a arquitetura "ideal" raramente sobrevive ao contato com produção. Projetar para **mudar** é mais importante que projetar para estar certo.
4. **Pensar em times** — Conway's Law é real. A estrutura do software reflete a estrutura da comunicação do time.
5. **Documentar decisões** — ADRs, C4, diagramas de sequência. O "porquê" importa mais que o "como".

---

## Estilos arquiteturais

A escolha do estilo arquitetural define a forma do sistema. Os estilos a seguir não são mutuamente exclusivos — projetos reais combinam elementos de vários.

### Layered Architecture (N-tier)

O estilo mais tradicional. Camadas horizontais: Presentation → Application → Domain → Infrastructure.

```
┌─────────────────────┐
│   Presentation      │  Controllers, Views
├─────────────────────┤
│   Application       │  Services, Use Cases
├─────────────────────┤
│   Domain            │  Entities, Business Rules
├─────────────────────┤
│   Infrastructure    │  Database, External APIs
└─────────────────────┘
```

**Regra:** camada N só conhece a camada N-1 (ou N+1 dependendo da direção).

**Prós:** familiar, fácil de entender, bom ponto de partida.

**Contras:** tende a virar "anemic domain model" — as entities viram estruturas de dados sem comportamento, e toda lógica vai para services. A infraestrutura frequentemente vaza para as camadas de cima.

**Quando usar:** CRUD, projetos simples, equipes iniciantes. É o default razoável quando você não tem certeza do que escolher.

### Hexagonal Architecture (Ports & Adapters)

Proposta por Alistair Cockburn (2005). O core da aplicação é isolado do mundo externo por meio de **Ports** (interfaces) e **Adapters** (implementações).

```
                 ┌─────── Driving Adapters (entrada) ───────┐
                 │                                           │
    HTTP Adapter ────→ Port ─────┐                          │
    CLI Adapter  ────→ Port ─────┤                          │
    Event Adapter────→ Port ─────┤                          │
                                 ↓                          │
                            ┌──────────┐                    │
                            │  Domain  │                    │
                            │  Logic   │                    │
                            └────┬─────┘                    │
                                 ↑                          │
    DB Adapter   ←──── Port ─────┤                          │
    Email Adapter←──── Port ─────┤                          │
    Payment API  ←──── Port ─────┘                          │
                 │                                           │
                 └──── Driven Adapters (saída) ──────────────┘
```

- **Driving Ports (entrada, "primary"):** interfaces que o mundo externo usa para acionar a aplicação. Ex.: `CreateOrderUseCase`.
- **Driven Ports (saída, "secondary"):** interfaces que a aplicação usa para acessar recursos externos. Ex.: `OrderRepository`, `EmailSender`.
- **Adapters:** implementações concretas. `HttpOrderController` (driving) e `JpaOrderRepository` (driven).

**Na prática (Spring Boot):**

```java
// Port (driven) — interface no domínio
public interface PatientRepository {
    Optional<Patient> findById(PatientId id);
    void save(Patient patient);
}

// Adapter — implementação na infraestrutura
@Repository
public class JpaPatientRepository implements PatientRepository {
    private final PatientJpaEntityRepository jpaRepo;

    @Override
    public Optional<Patient> findById(PatientId id) {
        return jpaRepo.findById(id.value())
            .map(this::toDomain);
    }
    // ...
}

// Use case (core) — não sabe que JPA existe
@Service
public class ScheduleAppointmentUseCase {
    private final PatientRepository patients;  // depende da interface
    private final NotificationPort notifier;

    public ScheduleAppointmentUseCase(PatientRepository patients,
                                      NotificationPort notifier) {
        this.patients = patients;
        this.notifier = notifier;
    }
}
```

**Prós:** isolamento total do domínio; testável sem infraestrutura; fácil trocar implementações (banco, provedor de email).

**Contras:** mais classes e interfaces; aprendizado inicial maior; pode ser over-engineering para CRUD.

### Onion Architecture

Proposta por Jeffrey Palermo (2008). Similar ao Hexagonal, mas com camadas concêntricas explícitas:

```
            ┌─────────────────────┐
            │  Infrastructure     │
            │  ┌───────────────┐  │
            │  │ Application   │  │
            │  │  Services     │  │
            │  │ ┌───────────┐ │  │
            │  │ │  Domain   │ │  │
            │  │ │ Services  │ │  │
            │  │ │┌─────────┐│ │  │
            │  │ ││ Domain  ││ │  │
            │  │ ││ Model   ││ │  │
            │  │ │└─────────┘│ │  │
            │  │ └───────────┘ │  │
            │  └───────────────┘  │
            └─────────────────────┘
```

**Regra fundamental:** dependências apontam sempre para dentro. O domínio (core) não conhece nada fora dele.

### Clean Architecture

Proposta por Uncle Bob (2012). Síntese de Hexagonal, Onion e outras. Define 4 camadas:

```
       ┌──────────────────────────────┐
       │ Frameworks & Drivers         │  UI, DB, Web, Devices
       │  ┌────────────────────────┐  │
       │  │ Interface Adapters     │  │  Controllers, Gateways,
       │  │  ┌──────────────────┐  │  │  Presenters
       │  │  │ Use Cases        │  │  │  Application Business Rules
       │  │  │  ┌────────────┐  │  │  │
       │  │  │  │ Entities   │  │  │  │  Enterprise Business Rules
       │  │  │  └────────────┘  │  │  │
       │  │  └──────────────────┘  │  │
       │  └────────────────────────┘  │
       └──────────────────────────────┘
```

**Dependency Rule:** nomes de fora podem ser referenciados por código de dentro, nunca o contrário. `Entities` não sabem que `Use Cases` existem; `Use Cases` não sabem que `Controllers` existem.

**Entities vs Use Cases (distinção sutil):**
- **Entities** — regras de negócio que existem independentemente da aplicação. "Um pedido com valor negativo é inválido" vale para qualquer sistema.
- **Use Cases** — regras específicas desta aplicação. "Ao criar um pedido, enviar email de confirmação" é específico deste sistema.

### Clean/Hexagonal/Onion: convergência

Herberto Graça mostrou que esses três estilos convergem para a mesma ideia: **isolar o domínio da infraestrutura via inversão de dependência**. As diferenças são em grande parte terminológicas.

| Aspecto | Layered | Hexagonal | Onion | Clean |
| --- | --- | --- | --- | --- |
| Proposto por | — (clássico) | Cockburn | Palermo | Uncle Bob |
| Ano | anos 70 | 2005 | 2008 | 2012 |
| Ênfase | camadas horizontais | ports/adapters | camadas concêntricas | regras de dependência |
| Domínio isolado? | não necessariamente | sim | sim | sim |
| Testável sem infra? | difícil | sim | sim | sim |
| Curva de aprendizado | baixa | média | média | alta |

**Recomendação prática:** aprenda Hexagonal primeiro. É o conceito mais puro e os outros são elaborações dele.

### Tomato Architecture (pragmatismo)

Abordagem pragmática proposta por Siva Prasad Reddy. Reconhece que Clean/Hexagonal estrita pode ser over-engineering e propõe:

- **Package by feature**, não por camada (`/orders`, `/patients`) em vez de (`/controllers`, `/services`)
- **Business logic pura** dentro do pacote, separada de infraestrutura
- **Sem cerimônia de interfaces** para tudo — só onde faz sentido (ex.: para mockar em testes)
- **Refatore para Hexagonal** quando a complexidade justificar

**Quando usar:** projetos médios, equipes pequenas, prazo curto. É o ponto intermediário entre "jogar tudo no controller" e "Clean Architecture pura".

### Event-Driven Architecture

Componentes se comunicam publicando e consumindo eventos, em vez de chamadas diretas.

```
Order Service → [OrderCreated event] → Message Broker → ┬─→ Inventory Service
                                                          ├─→ Notification Service
                                                          └─→ Analytics Service
```

**Vantagens:**
- **Desacoplamento temporal** — publisher não espera consumer responder
- **Desacoplamento espacial** — publisher não precisa saber quem são os consumers
- **Escalabilidade** — cada consumer escala independentemente
- **Resiliência** — se um consumer cai, eventos ficam na fila

**Desafios:**
- Debugging mais difícil (fluxo assíncrono entre serviços)
- Eventual consistency (não é imediato)
- Schema evolution (mudanças em eventos afetam todos os consumers)
- Duplicação e ordenação de eventos (consumers devem ser idempotentes)

→ Para aprofundar: [[Mensageria]], [[Event Streaming]], [[Event Storming]]

### Serverless / FaaS

Functions-as-a-Service: o código roda em resposta a eventos, sem gerenciamento de servidor.

**Exemplos:** AWS Lambda, Google Cloud Functions, Azure Functions, Cloudflare Workers.

**Prós:** paga só pelo uso, escala automaticamente até zero, sem ops de servidor.

**Contras:** cold start, vendor lock-in, limitações de execução (tempo máximo), estado precisa ir para fora (DynamoDB, S3), debugging complexo.

**Quando usar:** workloads esporádicos, event processing, endpoints com tráfego variável, background jobs, edge computing.

---

## Monolito vs Microserviços

A decisão mais discutida (e mal compreendida) em arquitetura moderna.

### O espectro

```
   Monolito                Modular                 Microserviços
   tradicional             Monolith
   ────────────────────────────────────────────────────────────→
   "big ball of mud"   "well-bounded modules"  "independently deployable"
        ↑                      ↑                         ↑
  acoplamento alto      acoplamento baixo          cada serviço tem
  1 único deploy        1 único deploy            deploy independente
                        módulos isolados
```

### Modular Monolith

O ponto intermediário frequentemente esquecido. Um único processo/deploy, mas organizado em módulos com fronteiras bem definidas.

**Princípios:**
- Módulos por domínio (não por camada técnica)
- Comunicação entre módulos via interfaces públicas, não acesso direto a tabelas
- Cada módulo tem seu próprio schema no banco (mesmo que no mesmo banco físico)
- Proibir import cruzado entre módulos via ArchUnit ou Java Modules

**Vantagens:**
- **Simplicidade operacional** do monolito (1 deploy, 1 log, 1 banco)
- **Evolução gradual** — um módulo pode virar microserviço quando justificar
- **Refactoring fácil** — mover código entre módulos é trivial comparado a microserviços
- **Performance** — chamadas in-process em vez de rede

**Quando escolher:** **quase sempre**, como ponto de partida. Martin Fowler e Sam Newman defendem "monolith first" — só migre para microserviços quando o monolito modular virar um gargalo real.

### Quando migrar para microserviços

Justifique cada uma com uma dor concreta antes de migrar:

1. **Escala heterogênea** — parte do sistema precisa escalar 10x mais que o resto
2. **Time cresceu demais para 1 deploy** — múltiplos times pisando no pé uns dos outros
3. **Domínios com tecnologias diferentes** — um módulo precisa de ML Python, outro de Go para performance
4. **Isolamento de falhas crítico** — você não pode deixar o módulo X derrubar o sistema todo
5. **Deploy velocity** — times precisam fazer deploys independentes e frequentes

**Sinais de que você NÃO deveria migrar:**
- "É a tendência do mercado"
- "Currículo fica melhor"
- "O time quer aprender Kubernetes"
- "Netflix faz assim"

### Custos dos microserviços

| Custo | Impacto |
| --- | --- |
| Complexidade operacional | Observabilidade, service mesh, deploy coordenado |
| Latência de rede | Cada chamada cross-service adiciona ms |
| Consistência distribuída | Sagas, eventual consistency, compensating transactions |
| Debugging | Distributed tracing obrigatório |
| Testing | Integration tests cross-service são frágeis |
| Versionamento de APIs | Breaking changes afetam múltiplos consumers |
| Custo de infraestrutura | Múltiplos processos, cada um com overhead fixo |

**Regra de ouro (Sam Newman):** se você está tendo dificuldade com um monolito bem projetado, terá muito mais dificuldade com microserviços.

### Padrões de migração

**Strangler Fig Pattern (Martin Fowler):** migrar gradualmente, roteando tráfego do monolito para novos serviços aos poucos, até o monolito "morrer".

```
Fase 1: [Monolith]
Fase 2: [Monolith] ← Proxy → [New Service (parte do trabalho)]
Fase 3: [Monolith (diminuindo)] ← Proxy → [Services (crescendo)]
Fase 4: [Services (tudo migrado)]
```

**Quando NÃO fazer big-bang rewrite:**
- Você perde features durante a migração
- Enquanto o novo está sendo construído, o antigo continua mudando
- Risco alto, validação só no final
- Joel Spolsky: "the single worst strategic mistake"

### Padrões essenciais de microserviços

| Padrão | O que resolve |
| --- | --- |
| API Gateway | Ponto de entrada único, routing, auth, rate limiting |
| Service Discovery | Encontrar serviços dinamicamente (Consul, Eureka) |
| Circuit Breaker | Evitar cascata de falhas (Resilience4j) |
| Saga | Transações distribuídas sem 2PC (orquestração ou coreografia) |
| Strangler Fig | Migração gradual de monolito |
| Sidecar | Cross-cutting concerns via proxy (service mesh: Istio, Linkerd) |
| Backends for Frontends (BFF) | API específica por tipo de cliente (web, mobile) |
| Outbox Pattern | Garantir publicação de evento junto com transação de banco |
| CQRS | Separar modelo de escrita do modelo de leitura |
| Event Sourcing | Estado derivado de eventos imutáveis |

→ Para deep dive em alguns deles: [[System Design]]

### Anti-patterns

- **Distributed Monolith** — serviços que precisam ser deployados juntos para funcionar. Pior que um monolito (tem os custos de ambos sem os benefícios).
- **Shared Database** — múltiplos serviços lendo/escrevendo nas mesmas tabelas. Acopla via schema, mudanças viram coordenação complexa.
- **Chatty Services** — um request do cliente vira 50 chamadas internas. Latência e acoplamento alto.
- **God Service** — um serviço que conhece todos os outros. Gargalo arquitetural.
- **Versioning Hell** — breaking changes sem coordenação. Consumers ficam presos em versões antigas.

---

## Domain-Driven Design (DDD)

Abordagem proposta por Eric Evans (2003) para lidar com a complexidade de domínios de negócio. Coloca o modelo de domínio no centro do design, e a linguagem do negócio no centro do código.

### Por que DDD importa

A maior fonte de bugs em software enterprise não é técnica — é **entender o domínio errado**. DDD força uma colaboração profunda entre devs e especialistas de negócio para construir um modelo compartilhado.

**Quando DDD vale a pena:**
- Domínios complexos com regras de negócio ricas (financeiro, saúde, logística, seguros)
- Sistemas que evoluem por anos
- Equipes onde há especialistas de negócio disponíveis

**Quando DDD é overkill:**
- CRUD simples
- MVPs e prototipagem
- Aplicações com pouca lógica de negócio (content management, dashboards)

### Conceitos estratégicos (big picture)

**Ubiquitous Language (Linguagem Ubíqua):**
A mesma terminologia entre devs, POs, negócio, documentação e código. Se o negócio chama de "consulta", o código tem `class Consulta`, não `class Appointment`. Se há ambiguidade ("cliente" significa paciente pro médico e empresa pro financeiro), isso é um sinal de bounded contexts diferentes.

**Bounded Context:**
Fronteira onde um modelo de domínio é consistente. O mesmo conceito ("cliente", "produto", "pedido") pode ter significados diferentes em contextos diferentes.

```
Contexto de Vendas:          Contexto de Faturamento:
  Cliente                       Cliente
  - nome                        - razão social
  - email                       - CNPJ
  - histórico de compras        - endereço fiscal
  - preferências                - regime tributário
```

Mesma palavra, modelos diferentes. Cada bounded context idealmente tem seu próprio modelo, seu próprio código, e pode virar seu próprio microserviço (ou módulo num monolito modular).

**Context Map:**
Diagrama de como os bounded contexts se relacionam. Relacionamentos possíveis:

| Relacionamento | Descrição |
| --- | --- |
| Shared Kernel | Pedaço de modelo compartilhado (frágil — evitar) |
| Customer/Supplier | Upstream define, downstream consome (negociação) |
| Conformist | Downstream se conforma ao upstream sem influência |
| Anti-Corruption Layer | Tradução para isolar o modelo local de um externo ruim |
| Open Host Service | Upstream publica API genérica para múltiplos consumers |
| Published Language | Schema público bem definido (ex.: eventos em Kafka) |
| Separate Ways | Contextos completamente independentes |

**Core Domain vs Supporting vs Generic:**
- **Core Domain** — o que é único e estratégico para o negócio. Invista o melhor time aqui.
- **Supporting Subdomain** — importante mas não diferenciador (ex.: billing, gestão de usuários). Pode ter solução mais simples.
- **Generic Subdomain** — comoditizado (ex.: autenticação, email). Use off-the-shelf (Auth0, SendGrid).

**Erro comum:** tratar tudo como core. O resultado é over-engineering onde não importa e subinvestimento onde importa.

### Conceitos táticos (como modelar)

**Entity:**
Objeto com identidade que persiste ao longo do tempo. Duas entities são iguais se têm o mesmo ID, mesmo que outros atributos mudem.

```java
public class Patient {
    private final PatientId id;  // identidade imutável
    private Name name;
    private Email email;
    private LocalDate birthDate;

    public void changeEmail(Email newEmail) {
        // regra de negócio: email não pode ser o mesmo
        if (this.email.equals(newEmail)) {
            throw new SameEmailException();
        }
        this.email = newEmail;
        // publicar domain event
    }
}
```

**Value Object:**
Definido pelos atributos, sem identidade. Dois value objects são iguais se todos os atributos forem iguais. Devem ser **imutáveis**.

```java
public record Money(BigDecimal amount, Currency currency) {
    public Money add(Money other) {
        if (!this.currency.equals(other.currency)) {
            throw new CurrencyMismatchException();
        }
        return new Money(this.amount.add(other.amount), this.currency);
    }
}
```

**Aggregate:**
Cluster de entities e value objects que mudam juntos. Tem uma **Aggregate Root** — a única forma de acessar os membros internos.

```java
public class Order {  // Aggregate Root
    private final OrderId id;
    private final List<OrderItem> items;  // entities internas
    private Money total;
    private OrderStatus status;

    // acesso aos items só via métodos da root
    public void addItem(Product product, int quantity) {
        if (status != OrderStatus.DRAFT) {
            throw new CannotModifyConfirmedOrderException();
        }
        items.add(new OrderItem(product, quantity));
        recalculateTotal();
    }
}
```

**Regras de aggregate:**
1. Uma transação = uma aggregate. Não modifique múltiplas aggregates atomicamente.
2. Comunicação entre aggregates via **eventual consistency** (domain events).
3. Mantenha aggregates **pequenas** — só o que precisa de consistência imediata.
4. Referencie outras aggregates por ID, não por referência direta.

**Repository:**
Abstração para persistir e recuperar aggregates. Retorna aggregates completas.

```java
public interface OrderRepository {
    Optional<Order> findById(OrderId id);
    void save(Order order);
    List<Order> findByCustomerId(CustomerId customerId);
}
```

**Domain Service:**
Lógica que não pertence naturalmente a nenhuma entity ou value object. Use com parcimônia — se tudo está virando service, seu modelo está anemic.

```java
// Transferência de dinheiro envolve 2 contas — não pertence a uma só
public class MoneyTransferService {
    public void transfer(Account from, Account to, Money amount) {
        from.withdraw(amount);
        to.deposit(amount);
    }
}
```

**Domain Event:**
Fato que aconteceu no domínio, relevante para o negócio. Passado, imutável, linguagem de negócio.

```java
public record OrderPlaced(
    OrderId orderId,
    CustomerId customerId,
    Money total,
    Instant occurredOn
) implements DomainEvent {}
```

Events são o mecanismo para comunicação entre aggregates (e entre bounded contexts) sem acoplamento.

### Anemic Domain Model (anti-pattern)

Modelo onde as entities são só getters/setters sem comportamento, e toda lógica fica nos services. Martin Fowler chama isso de anti-pattern porque perde o ponto principal de OOP: encapsulamento.

```java
// RUIM — anemic
public class Order {
    private BigDecimal total;
    public void setTotal(BigDecimal t) { this.total = t; }
    public BigDecimal getTotal() { return total; }
}

public class OrderService {
    public void addItem(Order order, Product p, int qty) {
        BigDecimal newTotal = order.getTotal().add(p.getPrice().multiply(BigDecimal.valueOf(qty)));
        order.setTotal(newTotal);  // lógica no service, não no objeto
    }
}

// BOM — rico
public class Order {
    private Money total;

    public void addItem(Product product, int quantity) {
        // lógica e validação no próprio objeto
        if (status != DRAFT) throw new ...
        items.add(new OrderItem(product, quantity));
        this.total = calculateTotal();
    }
}
```

→ Para aprofundar: [[Event Storming]]

---

## SOLID aplicado à arquitetura

Os princípios SOLID são normalmente discutidos em nível de classe, mas Uncle Bob mostrou que eles se aplicam em nível de **componentes/módulos** também.

| Princípio | Nível de classe | Nível arquitetural |
| --- | --- | --- |
| **SRP** — Single Responsibility | Uma classe, uma razão para mudar | Um módulo, um motivo de deploy |
| **OCP** — Open/Closed | Extender sem modificar | Adicionar features criando novos módulos, não mudando existentes |
| **LSP** — Liskov Substitution | Subtipos substituíveis | Versões de API devem ser compatíveis |
| **ISP** — Interface Segregation | Interfaces focadas | Microserviços não dependem de métodos que não usam |
| **DIP** — Dependency Inversion | Depender de abstrações | Core depende de interfaces; infra implementa |

→ Para deep dive em SOLID: [[Design Patterns]], [[Orientação a Objetos]]

### Dependency Inversion Principle em detalhe

O princípio mais importante para arquitetura. Define a direção das dependências.

```
// RUIM — domain depende de infrastructure
[Domain] → [Database (Postgres specific)]

// BOM — ambos dependem de abstração, e a abstração é propriedade do domain
[Domain] → [IRepository interface] ← [PostgresRepository]
            (no domain package)        (no infra package)
```

Isso é o que permite:
- Trocar o banco sem mexer no domain
- Testar o domain sem banco real
- Domain compilar sem depender de driver do Postgres

---

## Conway's Law e Team Topologies

> "Organizations which design systems are constrained to produce designs which are copies of the communication structures of these organizations." — Melvin Conway, 1967

**Consequência prática:** a arquitetura do software reflete a estrutura de comunicação dos times. Se você tem 3 times, você provavelmente vai acabar com 3 sistemas (mesmo que você queira 2 ou 4).

### Inverse Conway Maneuver

Se Conway's Law é inevitável, use-a **proativamente**: desenhe os times conforme a arquitetura que você quer. Quer 5 microserviços? Forme 5 times autônomos alinhados aos serviços.

### Team Topologies (Skelton & Pais)

Framework moderno que define 4 tipos de times e 3 modos de interação:

**Tipos de times:**

| Tipo | Papel |
| --- | --- |
| Stream-aligned | Time end-to-end por fluxo de valor (ex.: time de Agendamentos) |
| Enabling | Ajuda stream-aligned a adotar novas práticas (ex.: DevOps enablers) |
| Complicated Subsystem | Especialistas em áreas complexas (ex.: ML, criptografia) |
| Platform | Fornece plataforma interna (CI/CD, observabilidade, bancos) para stream-aligned |

**Modos de interação:**
- **Collaboration** — times trabalham juntos em um problema novo (alto custo, curto prazo)
- **X-as-a-Service** — um time consome o serviço do outro via API (baixo custo, longo prazo)
- **Facilitating** — um time ajuda o outro a aprender algo

**Na prática:** um microserviço deve ser "propriedade" de um único time stream-aligned. Se dois times precisam mudar o mesmo serviço, é um sinal de que as fronteiras estão erradas.

---

## Evolutionary Architecture

Proposta por Ford, Parsons, Kua (2017). Reconhece que a arquitetura **muda** — o desafio não é acertar no dia 1, mas suportar mudanças ao longo do tempo.

### Fitness Functions

Testes automatizados para propriedades arquiteturais (não funcionais). Roda no CI para impedir regressões arquiteturais.

**Exemplos:**

```java
// ArchUnit — garante que controllers não acessam repositories diretamente
@ArchTest
static ArchRule controllers_should_not_depend_on_repositories =
    noClasses().that().resideInAPackage("..controllers..")
        .should().dependOnClassesThat().resideInAPackage("..repositories..");

// Métrica de performance — testa que endpoint responde < 200ms p95
@Test
void searchEndpointP95ShouldBeBelow200ms() {
    var result = runLoadTest("/search?q=cardio", 1000);
    assertThat(result.p95()).isLessThan(Duration.ofMillis(200));
}

// Acoplamento — um módulo não pode importar de outro sem passar pela API pública
@ArchTest
static ArchRule modules_communicate_only_via_public_api =
    slices().matching("com.app.(*)..")
        .should().notDependOnEachOther()
        .ignoreDependency(resideInAPackage("..api.."), alwaysTrue());
```

**Tipos de fitness functions:**
- **Atomic** — testa uma dimensão (latência, acoplamento)
- **Holistic** — testa combinação (latência + segurança, etc.)
- **Triggered** — roda no CI
- **Continual** — roda em produção (observability)

### Princípios de evolução

- **Last Responsible Moment** — adie decisões arquiteturais até ter informação suficiente
- **Reversibility** — prefira decisões reversíveis a irreversíveis
- **Incremental change** — mude em pequenos passos, valide, continue
- **Architectural characteristics** como first-class citizens — performance, scalability, security são testáveis como features

---

## Documentação de arquitetura

Código se explica (em boa parte). Arquitetura precisa de documentação explícita, porque captura o **"por quê"** que o código não mostra.

### C4 Model

Abordagem hierárquica de diagramação em 4 níveis (Simon Brown):

**1. System Context Diagram** — o sistema no centro, usuários e sistemas externos ao redor. **Audiência:** stakeholders não-técnicos.

```
[Paciente] ──→ [MedEspecialista] ──→ [Gateway de Pagamento]
                      ↓
                      ↓ ──→ [Sistema de Clínicas Parceiras]
                [Médico]
```

**2. Container Diagram** — os containers (apps, bancos, filas) que compõem o sistema. **Audiência:** arquitetos, devs senior.

```
[Web App (React)] → [API (Spring Boot)] → [PostgreSQL]
                          ↓
                    [Kafka] → [Notification Worker]
                          ↓
                     [Redis Cache]
```

**3. Component Diagram** — a estrutura interna de cada container. **Audiência:** devs do time.

```
Dentro da API:
[AuthController] → [AuthService] → [JwtService]
                        ↓
                  [UserRepository] → [PostgreSQL]
```

**4. Code Diagram** — classes, funções (opcional, raramente necessário). **Audiência:** devs mexendo naquele código.

**Regra:** comece no nível mais alto (context) e desça conforme necessário. A maioria das discussões arquiteturais mora no nível 2 (container).

**Ferramentas:** Structurizr (oficial), Mermaid C4, PlantUML, draw.io.

### ADRs (Architectural Decision Records)

Documento curto que captura uma decisão arquitetural significativa: **contexto, decisão, consequências, status**. Vive no repositório (versionado) junto ao código.

```markdown
# ADR-007: Usar Kafka como event broker principal

## Status
Accepted (2026-02-15)

## Contexto
Precisamos de mecanismo de comunicação assíncrona entre microserviços
para suportar event-driven architecture. Requisitos:
- Retenção de eventos para replay (auditoria + recuperação)
- Throughput alto (prevemos 100K eventos/s em 2 anos)
- Ordenação por chave (events de uma mesma consulta na ordem)
- Consumer groups para paralelizar processamento

Alternativas consideradas:
1. RabbitMQ — maduro, mas modelo de queue dificulta replay e throughput
2. AWS SQS + SNS — managed, mas sem retenção longa nem ordenação forte
3. Kafka — alto throughput, retenção, ordenação por partition

## Decisão
Usar Apache Kafka (via Confluent Cloud) como broker de eventos.
Todos os serviços publicam domain events em tópicos e consomem via
consumer groups nomeados por serviço.

## Consequências

Positivas:
+ Suporta os requisitos de throughput e retenção
+ Permite replay para novos consumers ou recuperação
+ Ecossistema maduro (Schema Registry, Kafka Connect, ksqlDB)

Negativas:
- Curva de aprendizado maior que RabbitMQ para o time
- Custo operacional (vamos com Confluent Cloud para mitigar)
- Não serve bem para filas de tarefas tradicionais (RPC-like) —
  mantemos RabbitMQ para isso em serviços específicos

## Referências
- [[Kafka]]
- [Designing Event-Driven Systems (Stopford)](https://...)
```

**Regras:**
- Curto (1-2 páginas)
- Escrito no momento da decisão, não depois
- Status: Proposed → Accepted → Deprecated → Superseded
- Nunca edite ADRs aceitos — crie um novo que substitui

---

## Observabilidade

Os 3 pilares para entender o que acontece em produção:

### 1. Logs

Eventos discretos com contexto. **Structured logging** (JSON) é mandatório — permite query e análise.

```json
{
  "timestamp": "2026-04-10T14:23:11Z",
  "level": "ERROR",
  "service": "appointment-service",
  "traceId": "abc123",
  "userId": "user-42",
  "message": "Failed to create appointment",
  "error": "Doctor not available at requested time",
  "doctorId": "doc-7",
  "requestedTime": "2026-04-11T10:00Z"
}
```

**Boas práticas:**
- Nunca logar dados sensíveis (senhas, tokens, dados pessoais não mascarados)
- Sempre incluir `traceId` para correlacionar entre serviços
- Níveis: DEBUG (dev), INFO (eventos importantes), WARN (situação anômala), ERROR (falha), FATAL (sistema caiu)
- Agregação: ELK (Elasticsearch + Logstash + Kibana), Loki + Grafana, Datadog

### 2. Metrics

Números agregados ao longo do tempo. Responder: "qual é a taxa?", "qual é a distribuição?".

**RED method (para serviços):**
- **R**ate — requests por segundo
- **E**rrors — taxa de erros
- **D**uration — latência (p50, p95, p99)

**USE method (para recursos):**
- **U**tilization — % de uso
- **S**aturation — trabalho em fila
- **E**rrors — erros do recurso

**Ferramentas:** Prometheus + Grafana, Datadog, New Relic, CloudWatch.

**Na prática Spring Boot:**

```java
// Actuator + Micrometer exportam métricas automaticamente
management.endpoints.web.exposure.include=health,metrics,prometheus
management.metrics.export.prometheus.enabled=true

// Métricas customizadas
@Component
public class AppointmentMetrics {
    private final Counter appointmentsCreated;

    public AppointmentMetrics(MeterRegistry registry) {
        this.appointmentsCreated = Counter.builder("appointments.created")
            .tag("service", "appointment")
            .register(registry);
    }

    public void recordAppointmentCreated(String specialty) {
        appointmentsCreated.tag("specialty", specialty).increment();
    }
}
```

### 3. Traces

O caminho de uma única request através de múltiplos serviços. Essencial em microserviços.

```
[Client] → API Gateway (2ms) → Order Service (50ms)
                                    ↓
                              Payment Service (200ms) ← gargalo!
                                    ↓
                              Email Service (15ms)
```

Cada "span" é uma operação. Trace ID é propagado via headers HTTP e logs estruturados, permitindo reconstruir o fluxo completo.

**Ferramentas:** OpenTelemetry (padrão), Jaeger, Zipkin, Datadog APM.

### Princípios

- **Observability ≠ monitoring.** Monitoring = "eu sei quais perguntas fazer" (dashboards de métricas conhecidas). Observability = "eu posso responder perguntas novas" (drill down em logs e traces).
- **Alertas baseados em SLOs, não em CPU.** Alerte quando o usuário está sendo afetado, não quando uma máquina está em 80% de CPU.
- **Dashboards acionáveis.** Todo gráfico deve responder "e daí? o que eu faço?".

---

## Armadilhas comuns

- **Astronaut Architecture** — abstrações demais, código de menos. Interfaces para tudo "caso mude um dia". Ship first, refactor when needed.
- **Resume-Driven Development** — escolher tecnologia para enfeitar currículo, não para resolver o problema. "Vamos usar Kubernetes porque é o que tá no mercado" não é um argumento arquitetural.
- **Premature Distribution** — migrar para microserviços antes de ter um monolito modular funcionando. "We're Netflix" — you're not.
- **Ignore the Context** — aplicar a "melhor prática" sem entender o contexto. Clean Architecture num script de 200 linhas é over-engineering. Monolito num sistema com 50 times é under-engineering.
- **Anemic Domain Model** — entities sem comportamento. Resultado: toda lógica vai para services, modelo não representa o domínio, negócio fica difícil de entender.
- **Shared Database entre microserviços** — destrói o isolamento. Mudar uma tabela vira coordenação entre times. Se você vai compartilhar banco, provavelmente devia ser um monolito modular.
- **Transactional boundaries erradas** — tentar atomicidade cross-service com 2PC em vez de saga. O sistema fica lento e frágil.
- **Documentação que envelhece** — ADRs escritos meses após a decisão são ficção. C4 diagrams desatualizados são mentira.
- **Refatoração de big-bang** — reescrever o sistema do zero em vez de migrar gradualmente. Quase sempre falha (ver Joel Spolsky, Netscape 6).
- **Fitness functions ausentes** — sem testes automatizados de propriedades arquiteturais, a arquitetura erode naturalmente. Cada PR traz um pouquinho de dívida.
- **Tooling sobre princípios** — discutir "Spring vs Quarkus" antes de discutir bounded contexts é colocar a carroça na frente dos bois.

---

## Na prática (da minha experiência)

> **Muvz — migração de monolito para microserviços (Java EJB → Spring Boot):**
> Apliquei Hexagonal Architecture com DDD. Começamos com **Event Storming** com o pessoal de negócio para mapear bounded contexts — acabamos com 5 contextos bem definidos, que viraram 5 microserviços Spring Boot. Kafka como event broker principal (ADR documentando o porquê). Strangler Fig para migrar gradualmente, colocando o Kong como proxy roteando tráfego entre o monolito EJB legado e os novos serviços. A migração durou ~8 meses, sem big-bang, sem downtime significativo.
>
> **O que deu certo:** começar pela descoberta de domínio (Event Storming) antes de discutir tecnologia. Os bounded contexts ficaram estáveis e os serviços hoje ainda refletem essas fronteiras.
>
> **O que eu faria diferente:** Investiria mais cedo em observabilidade (tracing distribuído). Durante os primeiros meses, debuggar fluxos cross-service era doloroso. Hoje, OpenTelemetry é o primeiro a entrar no projeto.
>
> **MedEspecialista — decisão consciente de ficar em monolito modular:**
> O backend Spring Boot é um **modular monolith**, não microserviços. Cada bounded context é um módulo com seu próprio pacote Java (verificado por ArchUnit que impede imports cruzados). Uma única base de dados PostgreSQL, mas com schemas separados por módulo. Se precisarmos extrair um serviço no futuro, o módulo já está isolado — é uma refatoração, não uma reescrita.
>
> **Por que não microserviços?** A equipe tem 5 pessoas. A escala atual (~10K DAU) cabe folgada num monolito bem projetado. O custo operacional de microserviços (observabilidade, deploys coordenados, consistência distribuída) não seria justificado. O ADR-003 documenta essa decisão e revalidaremos em 2027 ou quando a escala/equipe justificar.
>
> **ADRs como memória institucional:** Todo PR com mudança arquitetural significativa tem um ADR associado. Isso evita o problema clássico de "por que isso está assim?" 2 anos depois. Quando alguém novo entra no time, eu aponto para a pasta `docs/adr/` — é a história das decisões em ordem cronológica.
>
> **A lição principal:** a melhor arquitetura é a que permite **mudar de ideia** depois. Bounded contexts claros, fitness functions automatizadas, ADRs documentando o "por quê". O código vai mudar. As fronteiras são o que importa.

---

## How to explain in English

> "My approach to software architecture is pragmatic and evolutionary. I don't believe in choosing 'the perfect architecture' upfront — I believe in starting simple, making the boundaries right, and evolving as the system grows.
>
> For most projects, I start with a modular monolith using Hexagonal Architecture principles: the domain logic depends on interfaces (ports), and infrastructure provides the implementations (adapters). This gives me the testability and isolation benefits of Clean Architecture without the overhead of microservices. I use tools like ArchUnit to enforce module boundaries automatically — fitness functions that fail the build if someone imports across modules incorrectly.
>
> When it comes to Domain-Driven Design, I focus on the strategic concepts first: identifying bounded contexts through Event Storming workshops with business stakeholders, defining the ubiquitous language, and mapping how contexts relate. The tactical patterns — entities, aggregates, value objects — come naturally once you have the strategic foundation right.
>
> I'm cautious about microservices. I've migrated a monolith to microservices at one company and consciously chose to stay with a modular monolith at another, because the scale and team size didn't justify the operational cost. The Strangler Fig pattern is my preferred migration strategy when microservices are needed — gradual, reversible, with continuous delivery the whole way through.
>
> For documentation, I use the C4 model to communicate at the right level of abstraction, and ADRs to capture architectural decisions with their context. ADRs are the institutional memory of why the system is shaped the way it is. When a new engineer joins, the ADR folder tells the story of every significant decision, in chronological order."

### Frases úteis em entrevista

- "I'd start with a modular monolith and extract services only when the monolith becomes the bottleneck."
- "The most important thing in DDD is getting the bounded contexts right — the tactical patterns flow from there."
- "I use Event Storming to map bounded contexts collaboratively with business stakeholders."
- "I follow the Strangler Fig pattern for migrations — gradual is safer than big-bang."
- "Fitness functions let me encode architectural rules as tests — ArchUnit is great for this on the JVM."
- "Conway's Law is real. If you want a certain architecture, you need the team structure to match."
- "The best architecture is the one that allows you to change your mind later."
- "ADRs are my institutional memory — they capture the why, not just the what."
- "Observability is a first-class architectural concern, not an afterthought."

### Key vocabulary

- estilo arquitetural → architectural style
- monolito modular → modular monolith
- arquitetura hexagonal → hexagonal architecture / ports and adapters
- contexto delimitado → bounded context (DDD)
- linguagem ubíqua → ubiquitous language
- mapeamento de contextos → context mapping
- agregação / raiz de agregação → aggregate / aggregate root
- objeto de valor → value object
- evento de domínio → domain event
- registro de decisão arquitetural → architectural decision record (ADR)
- inversão de dependência → dependency inversion
- camada anticorrupção → anti-corruption layer
- padrão estrangulador → strangler fig pattern
- função de fitness → fitness function
- topologia de equipes → team topologies
- lei de Conway → Conway's law
- arquitetura evolutiva → evolutionary architecture
- observabilidade → observability
- rastreamento distribuído → distributed tracing

---

## Recursos

### Livros essenciais

- *Domain-Driven Design* — Eric Evans (o livro original; denso mas fundamental)
- *Implementing Domain-Driven Design* — Vaughn Vernon (mais prático que o Evans)
- *Clean Architecture* — Robert C. Martin (síntese de Hexagonal/Onion)
- *Building Evolutionary Architectures* — Ford, Parsons, Kua (fitness functions, arquitetura que muda)
- *Team Topologies* — Skelton & Pais (como organizar times para suportar arquitetura)
- *Monolith to Microservices* — Sam Newman (guia de migração, Strangler Fig)
- *Fundamentals of Software Architecture* — Mark Richards & Neal Ford (visão panorâmica)
- *Software Architecture: The Hard Parts* — Richards & Ford (trade-offs difíceis em arquitetura distribuída)

### Online

- [Martin Fowler's blog](https://martinfowler.com/) — CQRS, DDD, microservices, refactoring
- [Herberto Graça — Software Architecture Chronicles](https://herbertograca.com/2017/07/03/the-software-architecture-chronicles/) — história e síntese dos estilos
- [C4 Model](https://c4model.com/) — site oficial de Simon Brown
- [ADR GitHub Organization](https://adr.github.io/) — templates e exemplos
- [Microservices.io](https://microservices.io/) — linguagem de padrões por Chris Richardson
- [arc42](https://arc42.org/) — template de documentação de arquitetura
- [ArchUnit](https://www.archunit.org/) — fitness functions para Java

### Vídeos e playlists

> [!info] Fundamentos de Arquitetura de Software
> [https://www.youtube.com/playlist?list=PLkpjQs-GfEMPzOzinFrqfkkfZy2DpwpBh](https://www.youtube.com/playlist?list=PLkpjQs-GfEMPzOzinFrqfkkfZy2DpwpBh)

> [!info] Arquitetura de Software - Primeira Temporada
> [https://www.youtube.com/playlist?list=PLkpjQs-GfEMNcWDlIck2I5TGBSSRCK39L](https://www.youtube.com/playlist?list=PLkpjQs-GfEMNcWDlIck2I5TGBSSRCK39L)

> [!info] Padrões Arquiteturais
> [https://www.youtube.com/playlist?list=PLkpjQs-GfEMMoh78fnnHtrhK1iWe-ZSJ5](https://www.youtube.com/playlist?list=PLkpjQs-GfEMMoh78fnnHtrhK1iWe-ZSJ5)

> [!info] DDD do jeito certo
> [https://www.youtube.com/playlist?list=PLkpjQs-GfEMN8CHp7tIQqg6JFowrIX9ve](https://www.youtube.com/playlist?list=PLkpjQs-GfEMN8CHp7tIQqg6JFowrIX9ve)

### Artigos específicos

- [The Clean Architecture — Uncle Bob](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Hexagonal Architecture — Alistair Cockburn](https://alistair.cockburn.us/hexagonal-architecture/)
- [Microservices — Martin Fowler](https://martinfowler.com/articles/microservices.html)
- [Strangler Fig Application — Martin Fowler](https://martinfowler.com/bliki/StranglerFigApplication.html)
- [What do you mean by "Event-Driven"? — Fowler](https://martinfowler.com/articles/201701-event-driven.html)
- [Tomato Architecture — Siva Prasad Reddy](https://www.sivalabs.in/tomato-architecture-pragmatic-approach-to-software-design/)
- [Package by Feature — Philipp Hauer](https://phauer.com/2020/package-by-feature/)
- [Architecture Antipatterns](https://architecture-antipatterns.tech/)

---

## Veja também

- [[System Design]] — building blocks, walkthroughs, escala e performance
- [[Design Patterns]] — SOLID, GoF, patterns de código
- [[API Design]] — contratos entre serviços, REST/GraphQL/gRPC
- [[Orientação a Objetos]] — fundamentos OOP que sustentam DDD
- [[Event Storming]] — workshop para descobrir bounded contexts
- [[Mensageria]] — comunicação assíncrona
- [[Event Streaming]] — eventos como fonte de verdade
- [[03-Dominios/Arquitetura/Mensageria/Kafka]] — event broker mais usado
- [[RabbitMQ]] — message queuing tradicional
- [[Banco de dados]] — persistência, transações, consistência
- [[Redes e Protocolos]] — comunicação entre serviços
- [[Spring Boot]] — implementação prática na stack Java
