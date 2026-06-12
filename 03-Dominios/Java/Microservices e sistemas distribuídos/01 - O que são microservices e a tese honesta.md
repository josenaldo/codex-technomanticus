---
title: "O que são microservices e a tese honesta"
created: 2026-06-12
updated: 2026-06-12
type: concept
status: seedling
publish: true
fase: iniciado
tags:
  - java
  - microservices
  - iniciado
  - arquitetura
aliases:
  - "O que são microservices"
  - "Microservices vs monólito"
---

# O que são microservices e a tese honesta

> [!abstract] TL;DR
> Microservices é o estilo arquitetural que decompõe uma aplicação em serviços pequenos, **deployáveis independentemente**, cada um com **seu próprio banco** (database-per-service) e dono de uma capacidade de negócio. A tese honesta deste galho: microservices é **trade-off organizacional e de escala, não default técnico** — você paga o *microservice premium* (Fowler) antes de colher qualquer benefício. Importa porque a resposta madura de senior quase nunca é "vamos de microservices", e sim "qual problema isso resolve que um **monólito modular** não resolveria?".

## O que é

Microservices é uma forma de construir uma única aplicação como um **conjunto de serviços pequenos**, cada um rodando no seu próprio processo e se comunicando por mecanismos leves (HTTP/REST, mensageria). A definição canônica de Martin Fowler e James Lewis: *"an approach to developing a single application as a suite of small services, each running in its own process and communicating with lightweight mechanisms."*

As características que definem o estilo (segundo Fowler/Lewis):

- **Componentização por serviços.** A unidade de componente é o serviço — algo *fora do processo*, deployável de forma independente —, não uma biblioteca linkada no mesmo processo. Num monólito, *"a change to any single component results in having to redeploy the entire application"*. Em microservices, você redeploya só o serviço que mudou.
- **Organização por capacidade de negócio.** Times se alinham a funções de negócio (pagamentos, catálogo, pedidos), não a camadas técnicas (time de UI, time de backend, time de DBA). Cada time é cross-funcional e dono da fatia inteira: UI, lógica, persistência.
- **Dados descentralizados — database-per-service.** Cada serviço gerencia o próprio banco. Fowler chama isso de *Polyglot Persistence*: cada serviço escolhe a tecnologia de dados que faz sentido para ele. Não há um schema central compartilhado entre serviços.
- **Smart endpoints, dumb pipes.** A inteligência mora nos serviços; a infraestrutura de comunicação é deliberadamente simples (REST, mensageria leve), sem orquestradores centrais pesados.
- **Produtos, não projetos.** *"You build it, you run it"* — o time carrega a responsabilidade de produção do serviço, não entrega e some.
- **Design for failure e design evolutivo.** Como serviços falham pela rede, o sistema é projetado para tolerar falha (timeouts, circuit breakers), e cada serviço é pensado para ser substituível.

Repare no que **não** está na lista: "é mais moderno", "todo mundo usa", "escala melhor por default". Nada disso é uma característica do estilo — são justificativas de marketing.

## Por que importa

Para um senior — e numa entrevista — o valor não está em *saber descrever* microservices (júnior também sabe). Está em **saber quando NÃO usar** e por quê. É exatamente aí que a conversa separa quem leu a documentação de quem entende o trade-off.

A tese-assinatura deste galho, direto do próprio Fowler:

> [!quote] Martin Fowler — MicroservicePremium
> *"if you can keep your system simple enough to avoid the need for microservices: do."*

Microservices **não é um upgrade técnico gratuito**. É uma resposta a um problema **organizacional e de escala**: muitos times grandes que precisam deployar de forma independente, partes do sistema com cargas e ritmos de evolução muito diferentes, sistema complexo demais para um único monólito comportar. Se você não tem esse problema, microservices só adiciona custo.

A pergunta certa de senior não é *"como eu quebro isso em microservices?"*. É *"esse sistema tem o problema que microservices resolve?"*. Na maioria dos casos, a resposta honesta é: ainda não — e um **monólito modular** (Sam Newman) resolve melhor agora.

## Como funciona

### O modelo: deploy independente e database-per-service

O coração do estilo são dois acoplamentos que você **corta**:

1. **Acoplamento de deploy.** Cada serviço é uma unidade deployável sozinha. O `payment-service` sobe sem precisar redeployar o `catalog-service`. Isso permite que times trabalhem e entreguem em ritmos diferentes.
2. **Acoplamento de dados.** Cada serviço é dono exclusivo do seu banco. Nenhum outro serviço lê ou escreve diretamente naquele schema — só através da API do dono.

```text
   ┌──────────────────┐      ┌──────────────────┐      ┌──────────────────┐
   │  order-service   │      │ payment-service  │      │ inventory-service│
   │  ┌────────────┐  │      │  ┌────────────┐  │      │  ┌────────────┐  │
   │  │  orders DB │  │      │  │ payments DB│  │      │  │  stock DB  │  │
   │  └────────────┘  │      │  └────────────┘  │      │  └────────────┘  │
   └────────┬─────────┘      └────────┬─────────┘      └────────┬─────────┘
            │                         │                         │
            └──────────── REST / mensageria leve ───────────────┘
              (cada serviço fala só com a API do outro, nunca com o banco do outro)
```

O preço escondido dessa figura bonita: assim que os dados deixam de morar num banco só, você perde transações ACID atravessando serviços. A coordenação passa a ser feita por **eventos e consistência eventual** — território de saga/eventos, que é assunto do **Galho 14 (Mensageria)**, não desta nota. Aqui basta gravar: *database-per-service troca consistência forte por autonomia*.

### O custo: o microservice premium, Conway e bounded contexts

Antes de qualquer benefício, microservices cobra um **premium** — um custo fixo de entrada. Fowler:

> *"you have to work on automated deployment, monitoring, dealing with failure, eventual consistency, and other factors that a distributed system introduces."*

Ou seja: deploy automatizado, observabilidade distribuída, tratamento de falha de rede, consistência eventual — tudo isso vira obrigatório no dia um, mesmo que o sistema ainda seja pequeno. É um pedágio que você paga **antes** de colher escala.

Some a isso duas dificuldades estruturais:

- **Lei de Conway.** *"Any organization that designs a system will produce a design whose structure is a copy of the organization's communication structure."* Os limites entre serviços tendem a espelhar os limites entre **times**. Se a sua organização não está dividida em times autônomos por capacidade de negócio, seus microservices vão sair tortos — ou você vai estar lutando contra a estrutura da empresa o tempo todo.
- **Bounded contexts difíceis de acertar cedo.** As fronteiras certas entre serviços (os *bounded contexts* do DDD) raramente são óbvias no começo. E Fowler é taxativo: *"any refactoring of functionality between services is much harder than it is in a monolith."* Mover uma responsabilidade entre dois serviços envolve migração de dados, versionamento de API, deploy coordenado. Errar a fronteira cedo é caríssimo.

### A alternativa quase sempre suficiente: monólito modular

Por que começar com um monólito? Fowler defende explicitamente o **MonolithFirst**: no início de uma aplicação você não sabe se ela vai dar certo, as fronteiras ainda não estão claras, e *"the premium of microservices is a drag you should do without"* nessa fase.

A confusão comum é achar que "monólito" significa "bola de lama". Não significa. O **monólito modular** (termo popularizado por Sam Newman) é um único deployável com **fronteiras internas bem definidas** — módulos com APIs claras, baixo acoplamento, alta coesão — mas que ainda sobe como uma coisa só. Você ganha a organização do código sem pagar o pedágio distribuído.

> [!tip] A regra prática
> Comece monólito modular. Mantenha as fronteiras internas limpas. Quando (e *se*) uma fronteira provar que precisa de deploy/escala independente, extraia *aquele* pedaço para um serviço. Fowler chama isso de extrair microservices "nas bordas" conforme as fronteiras estabilizam.

Pergunta retórica para fechar: se as fronteiras certas só ficam claras com o uso real, por que congelá-las em serviços separados *antes* de ter esse uso? O monólito modular te dá o luxo de descobrir as fronteiras barato, refatorando dentro do mesmo processo, antes de cravá-las em rede.

## Na prática

Considere um e-commerce com três capacidades: **pedidos**, **pagamentos** e **estoque**. O domínio tem entidades como `Order`, `Payment` e `InventoryItem`.

A decisão arquitetural — e não o código — é o ponto:

**Opção A — Monólito modular.** Um único deployável `com.example.shop` com três pacotes/módulos bem isolados:

```text
com.example.shop
├── orders/      (Order, OrderService — API pública do módulo)
├── payments/    (Payment, PaymentService)
└── inventory/   (InventoryItem, InventoryService)
```

Os módulos conversam por chamadas de método em memória, dentro de uma transação. Um `OrderService` que precisa reservar estoque chama `InventoryService` direto — consistência forte, transação única, refatoração trivial.

**Opção B — Microservices.** Três deployáveis: `order-service`, `payment-service`, `inventory-service`, cada um com seu banco. Agora "criar um pedido e reservar estoque" deixa de ser uma transação local: vira uma coordenação por rede entre serviços, com consistência eventual e tratamento de falha. Útil **se** pedidos, pagamentos e estoque têm times distintos, cargas muito diferentes e precisam deployar sem se bloquear.

Como decidir? A pergunta não é "qual é mais elegante". É: **há times separados? Há escala/ritmo divergente real? As fronteiras já provaram ser estáveis?** Se a resposta for "não" ou "ainda não sei", a Opção A é a escolha de senior. A Opção B passa a fazer sentido quando o monólito vira gargalo organizacional — não antes.

(O empacotamento e a produção desses serviços — containers, orquestração — são assunto do **Galho 17 (planejado)**. Aqui a decisão é de fronteira, não de infra.)

## Armadilhas

### (1) Microservices como default técnico

Tratar microservices como "o jeito moderno e certo de fazer" e começar todo projeto novo já quebrado em serviços. O resultado é pagar o *premium* (deploy automatizado, observabilidade distribuída, consistência eventual) num sistema que ainda cabia tranquilo num único deployável — com a desvantagem extra de fronteiras erradas que serão caríssimas de corrigir depois.

*Exemplo:* uma startup de 4 devs sobe 8 microservices no MVP; metade do tempo de engenharia vai para encanamento distribuído em vez de funcionalidade, e o produto ainda nem validou mercado.

*Fix:* comece monólito modular; só extraia um serviço quando uma fronteira provar que precisa de deploy ou escala independente.

### (2) Dividir por camada técnica em vez de capacidade de negócio

Recortar os serviços por camada — `ui-service`, `business-logic-service`, `data-access-service` — em vez de por **bounded context / capacidade de negócio**. Isso ignora a Lei de Conway e produz serviços fortemente acoplados: qualquer feature de negócio precisa de deploy coordenado das três camadas, anulando a independência que justificava microservices.

*Exemplo:* adicionar um campo a "pedido" exige mudar e redeployar o serviço de UI, o de regras e o de dados juntos — você tem os custos do distribuído sem nenhum dos benefícios.

*Fix:* alinhe cada serviço a uma capacidade de negócio inteira (vertical: `order-service` com sua UI, lógica e dados), não a uma camada horizontal.

## Em entrevista

### Frase pronta (inglês)

> Microservices is an organizational and scaling trade-off, not a technical default — you pay the "microservice premium" (automated deployment, distributed monitoring, eventual consistency) up front, before you get any benefit. My default is a modular monolith with clean internal boundaries, because service boundaries are genuinely hard to get right early and refactoring across services is far more expensive than refactoring inside one process. I'd extract a microservice only when a specific bounded context proves it needs independent deployment or scaling — typically driven by team structure, per Conway's Law — rather than splitting everything up front.

### Vocabulário

| Termo PT | Termo EN |
| --- | --- |
| microsserviço | microservice |
| monólito modular | modular monolith |
| contexto delimitado | bounded context |
| consistência eventual | eventual consistency |
| prêmio dos microsserviços | microservice premium |
| lei de Conway | Conway's Law |
| capacidade de negócio | business capability |
| banco por serviço | database-per-service |
| deploy independente | independent deployment |

## Veja também

- [[03-Dominios/Java/Microservices e sistemas distribuídos/02 - Monorepo vs multi-repo|Monorepo vs multi-repo]]
- [[03-Dominios/Java/Microservices e sistemas distribuídos/05 - Comunicação inter-serviços — síncrono vs assíncrono|Comunicação inter-serviços]]
- [[03-Dominios/Java/Microservices e sistemas distribuídos/23 - Quando NÃO fazer microservices|Quando NÃO fazer microservices]]
- [[03-Dominios/Java/Microservices e sistemas distribuídos/index|Microservices e sistemas distribuídos (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]

## Referências

- Martin Fowler & James Lewis — *Microservices*: https://martinfowler.com/articles/microservices.html
- Martin Fowler — *MonolithFirst*: https://martinfowler.com/bliki/MonolithFirst.html
- Martin Fowler — *MicroservicePremium*: https://martinfowler.com/bliki/MicroservicePremium.html
