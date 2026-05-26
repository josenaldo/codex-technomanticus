---
title: "Event Storming"
created: 2026-04-01
updated: 2026-04-10
type: concept
status: evergreen
tags:
  - arquitetura
  - ddd
  - entrevista
publish: false
---

# Event Storming

Workshop colaborativo criado por **Alberto Brandolini** para descobrir e mapear domínios complexos usando **eventos de negócio** como unidade fundamental. É a ponte entre especialistas de negócio e desenvolvedores, e a técnica mais eficaz para descobrir bounded contexts em DDD. Enquanto [[Event Streaming]] cobre a implementação técnica de eventos, esta nota foca no **processo de descoberta** que acontece antes de qualquer linha de código.

## O que é

Event Storming é um workshop colaborativo onde desenvolvedores, especialistas de domínio, product owners e stakeholders se reúnem em torno de uma parede (ou board virtual) e mapeiam o sistema através de **eventos de domínio** — fatos significativos que acontecem no negócio — escritos em post-its coloridos.

**Por que funciona:**
- **Baixa barreira de entrada** — qualquer pessoa sabe escrever em um post-it
- **Elimina silos** — negócio e tech pensam juntos
- **Foca em comportamento**, não em dados ou UI
- **Descobre inconsistências rapidamente** — pontos quentes (hot spots) emergem naturalmente
- **Resultado tangível** — modelo visual compartilhado em horas, não semanas

Em entrevistas, o que diferencia um senior que conhece Event Storming:

1. **Saber explicar os 3 níveis** — Big Picture, Process Modelling, Software Design — cada um serve a um propósito
2. **Dominar as cores padrão** — a convenção de post-its não é decoração, é linguagem
3. **Reconhecer quando Event Storming se aplica** — é valioso para domínios complexos, overkill para CRUDs
4. **Conectar a DDD** — como descobre bounded contexts, aggregates, e ubiquitous language
5. **Facilitar um workshop** — a técnica é simples, facilitação é difícil

---

## A origem e a filosofia

Criado por **Alberto Brandolini** em 2013 na Itália, inspirado pela frustração de que UML e BPMN eram ferramentas de **documentação**, não de **descoberta**. Brandolini queria uma técnica onde o **processo** fosse mais valioso que o **artefato** — onde a conversa que acontece durante o workshop fosse mais importante que o diagrama resultante.

**Citação famosa:**
> "The first rule of Event Storming is: talk to the people who know about the problem."  
> — Alberto Brandolini

**Princípios fundamentais:**

1. **Eventos são a lingua franca** — todo mundo entende "o pedido foi confirmado"
2. **Parede infinita** — espaço físico ilimitado (ou board virtual gigante) força pensar em escala
3. **Sem hierarquia** — CTO e dev júnior têm a mesma voz durante o workshop
4. **Ordem cronológica** — eventos são colocados da esquerda para direita no tempo
5. **Suspender julgamento** — anote tudo, discuta depois
6. **Hot spots são valiosos** — pontos de conflito ou incerteza são onde está o aprendizado

---

## Os 3 níveis de Event Storming

Event Storming não é uma técnica única. Brandolini a descreve em **3 níveis de zoom** — cada um serve a um propósito diferente.

### 1. Big Picture Event Storming

**Propósito:** alinhar entendimento de alto nível do domínio inteiro. Descobrir bounded contexts. Identificar as áreas mais valiosas e problemáticas.

**Audiência:** stakeholders seniors, product managers, arquitetos, tech leads.

**Duração:** 2-4 horas (exploratório) a 1-2 dias (mais profundo).

**Output:** mapa de alto nível do domínio, descoberta de bounded contexts candidatos, identificação de hot spots e knowledge gaps.

**Como fazer:**

1. **Post-its laranjas** (eventos de domínio) na parede, em ordem cronológica
2. Começar com o que todo mundo sabe — os eventos óbvios
3. Explorar "o que acontece antes?" e "o que acontece depois?"
4. Identificar gaps — "e quando o pagamento é recusado? nunca pensei nisso"
5. **Hot spots** (post-its roxos/rosas) — onde há conflito, incerteza, ou regra difícil
6. Agrupar eventos em **áreas temáticas** — esses agrupamentos são candidatos a bounded contexts
7. Identificar **pivotal events** — eventos que mudam o fluxo significativamente

**Exemplo visual:**

```
CLIENTE                       PAGAMENTO                    LOGÍSTICA
───────                       ─────────                    ─────────

[Pedido       [Carrinho    [Pagamento   [Pagamento    [Pedido       [Pedido
Iniciado] →   Confirmado] → Iniciado] → Aprovado]  →  Despachado] → Entregue]
                                    ↓
                             [Pagamento
                              Recusado] 🔥 (hot spot)
                                    ↓
                             ???
```

### 2. Process Modelling

**Propósito:** modelar processos de negócio específicos em detalhe. Entender quem faz o quê, quando, e por quê.

**Audiência:** product owners, especialistas de domínio, devs, UX.

**Duração:** 4 horas a 1 dia por processo.

**Output:** modelo detalhado de um processo, com atores, comandos, políticas, eventos, e sistemas externos.

**Como fazer:**

1. Parte do output do Big Picture — escolhe um processo
2. Adiciona **Actors** (post-its amarelos) — quem dispara os eventos (usuário, admin, sistema)
3. Adiciona **Commands** (post-its azuis) — as ações que os actors querem tomar
4. Adiciona **Policies** (post-its lilases) — regras automáticas: "quando X acontece, faça Y"
5. Adiciona **Read Models** (post-its verdes) — informações que os actors precisam ver para decidir
6. Adiciona **External Systems** (post-its rosas) — integrações (Stripe, Correios, etc.)

**Estrutura de um fluxo:**

```
Actor → Command → Event → Policy → Command → Event ...
                          (auto)     (trigger)
```

### 3. Software Design (ou Design-Level) Event Storming

**Propósito:** modelar a implementação. Identificar aggregates, value objects, entities. Ponte entre o negócio e o código.

**Audiência:** principalmente devs e arquitetos (com domínio disponível para consulta).

**Duração:** dias a semanas, iterativo.

**Output:** modelo pronto para implementação — aggregates claros, eventos bem definidos, limites de consistência.

**Como fazer:**

1. Parte do Process Modelling
2. Identifica **Aggregates** (post-its amarelos grandes) — clusters de comandos e eventos que precisam de consistência
3. Nomeia os aggregates usando a ubiquitous language
4. Define invariantes de cada aggregate
5. Valida com casos reais ("o que acontece se dois users tentam fazer X ao mesmo tempo?")

---

## O alfabeto: post-its e suas cores

A convenção de cores de Brandolini não é arbitrária. Cada cor tem um significado específico e evoluiu através de centenas de workshops.

### Cores canônicas

| Cor | Conceito | O que representa | Escrito no passado? |
| --- | --- | --- | --- |
| 🟧 **Laranja** | **Domain Event** | Fato que aconteceu no domínio | **Sim** ("Pedido Confirmado") |
| 🟦 **Azul claro** | **Command** | Ação/intenção de um actor | Não, imperativo ("Confirmar Pedido") |
| 🟨 **Amarelo** | **Actor** | Pessoa ou sistema que dispara comando | Substantivo ("Cliente", "Admin") |
| 🟨 **Amarelo grande** | **Aggregate** | Cluster de consistência | Substantivo ("Pedido", "Paciente") |
| 🟩 **Verde** | **Read Model** | Informação que o actor vê para decidir | Substantivo ("Lista de Médicos Disponíveis") |
| 🟪 **Lilás** | **Policy** | Regra automática ("quando X, então Y") | "Quando pedido confirmado, cobrar cartão" |
| 🌸 **Rosa** | **External System** | Integração com sistema externo | Nome ("Stripe", "Correios", "SMS Gateway") |
| 🟥 **Rosa/Vermelho** | **Hot Spot** | Problema, conflito, dúvida, risco | Pergunta ou observação |
| ⬜ **Branco** | **Explanation** | Nota explicativa, comentário | Texto livre |

### Hot spots: a cor mais valiosa

**Rosa/vermelho** marca pontos de dor ou descoberta:

- "E se o médico cancelar depois do pagamento?"
- "Não sabemos como funciona o reembolso"
- "Tem um caso que o legal pediu no email e nunca documentamos"
- "Isso aqui é um bug ou feature?"

**Regra de Brandolini:** hot spots são **ouro**. Eles indicam onde o aprendizado está. Nunca esconda ou apague hot spots — destaque-os.

### Pivotal events

Eventos críticos que **mudam a natureza** do que acontece. Ex.: "Pedido Pago" é pivotal porque depois disso o mundo é diferente — agora tem faturamento, logística, etc. Marque-os com uma linha vertical na parede para separar fases.

---

## Como conduzir um workshop

### Preparação

**Pessoas:**
- **Facilitator** — quem conduz (idealmente alguém que conhece a técnica, não necessariamente o líder)
- **Domain experts** — pessoas que SABEM como o negócio funciona (não gerentes de gerentes)
- **Developers** — quem vai implementar
- **Stakeholders relevantes** — product, UX, ops se aplicável
- **Tamanho ideal:** 5-10 pessoas. Mais que isso, quebra em grupos.

**Espaço:**
- **Físico:** parede LONGA (8+ metros), post-its em quantidade (MUITOS laranjas), canetas grossas, fita
- **Virtual:** Miro, Mural, Figjam. Templates prontos para Event Storming.

**Regras do workshop:**
- Sem laptops/celulares (exceto para notas)
- Sem hierarquia — todo mundo tem voz igual
- Anote primeiro, discuta depois
- Post-it é barato — erre à vontade

### Passo a passo (Big Picture)

**Fase 1 — Caos Caótico (Chaotic Exploration):**
1. Facilitator explica: "vamos escrever nos post-its laranjas os eventos de negócio, no passado, em ordem cronológica na parede"
2. **Todo mundo escreve em paralelo** — sem filtro, sem discussão
3. Cole na parede, mais ou menos em ordem
4. 20-30 minutos de caos criativo

**Fase 2 — Ordenação Cronológica (Enforce the Timeline):**
1. Grupo reorganiza eventos em ordem temporal
2. Conflitos emergem: "espera, isso acontece antes ou depois daquilo?"
3. Duplicatas são consolidadas
4. Eventos faltantes são descobertos

**Fase 3 — Gaps e Hot Spots:**
1. Procure gaps: "o que acontece entre esses dois eventos?"
2. Marque hot spots: "isso aqui ninguém sabe direito"
3. Identifique **pivotal events**
4. Discuta casos alternativos: "e se der errado?"

**Fase 4 — Bounded Contexts (para Big Picture):**
1. Agrupe eventos por áreas temáticas
2. Cada grupo é um candidato a bounded context
3. Marque linhas de separação entre contextos
4. Discuta: "isso aqui é o mesmo conceito ou é diferente em cada contexto?"

**Fase 5 — Próximos Passos:**
1. Priorize hot spots a resolver
2. Identifique áreas para aprofundar em Process Modelling
3. Documente decisões e aprendizados

---

## Como Event Storming conecta com DDD

Event Storming é a **porta de entrada para DDD**. Os conceitos se mapeiam diretamente:

### Descoberta de Bounded Contexts

No Big Picture, agrupamentos naturais de eventos são **bounded contexts candidatos**. Quando um conceito muda de significado entre áreas (ex.: "cliente" no Pagamento vs "paciente" no Agendamento), isso é um sinal forte de fronteira de contexto.

### Ubiquitous Language

O workshop naturalmente gera a linguagem ubíqua. Os nomes dos post-its **são** a linguagem do negócio. Se um dev escreve "Order Placed" e o negócio escreve "Pedido Registrado", vocês têm que negociar qual é o termo canônico.

### Aggregates

No Software Design Event Storming, aggregates emergem como clusters de comandos e eventos que compartilham **invariantes**. Se um comando afeta dados de múltiplos aggregates, é sinal de que um evento + eventual consistency é melhor.

### Domain Events

Os próprios post-its laranjas são a lista inicial de domain events do sistema. Eles vão virar classes Java/código no final.

### Commands e Policies

Commands viram casos de uso. Policies viram event handlers ou process managers.

→ Para aprofundar: [[Arquitetura de Software]] (DDD estratégico e tático)

---

## Variantes e extensões

### Example Mapping

Técnica complementar criada por Matt Wynne. Depois de Event Storming, você pega um evento/regra específica e mapeia **exemplos concretos** para descobrir as regras de negócio.

```
Regra: "Desconto para clientes VIP"
├── Exemplo 1: Cliente VIP compra 100 reais → desconto de 10
├── Exemplo 2: Cliente VIP compra 50 reais → sem desconto (mín 100)
├── Exemplo 3: Cliente normal compra 100 reais → sem desconto
└── Questão: "E se o VIP expirou ontem?" (hot spot)
```

Excelente para preparar cenários BDD e testes de aceitação.

### User Story Mapping (complementar, não substitui)

Jeff Patton. Mapeia **jornada do usuário** em horizontal. Event Storming mapeia **comportamento do sistema** em horizontal. Os dois se complementam — User Story Mapping para UX, Event Storming para lógica de negócio.

### Domain Storytelling

Stefan Hofer. Mais estruturado, usa pictogramas para actors, work objects, e activities. Captura **histórias específicas** do negócio. Menos eventos, mais narrativa.

### Remote Event Storming

COVID acelerou ferramentas virtuais. Miro e Mural têm templates prontos. Desafios:
- Energia é menor que presencial (compensar com pausas, breakouts)
- Discussões laterais acontecem no chat (perde contexto)
- Grupos grandes viram caos (dividir em breakout rooms)

Brandolini tem um guia específico de Remote Event Storming.

---

## Quando usar (e quando NÃO)

### Use Event Storming quando:

- **Domínio complexo** com muitas regras de negócio não triviais
- **Começando um projeto novo** e precisa descobrir o domínio
- **Modernizando sistema legado** — mapear o que existe antes de refazer
- **Conflitos entre negócio e tech** — workshop alinha expectativas
- **Migrando para microserviços** — descobrir bounded contexts para separar serviços
- **Onboarding de nova equipe** em domínio complexo
- **Process discovery** antes de automação

### NÃO use Event Storming quando:

- **CRUD simples** — não tem processo suficiente para mapear
- **Domínio trivial e conhecido** — todo mundo já sabe como funciona
- **Não há domain experts disponíveis** — o workshop falha sem eles
- **Equipe não compra a ideia** — workshop só funciona com engajamento
- **Só você está "interessado"** — Event Storming é coletivo por definição

---

## Armadilhas comuns

- **Facilitator inexperiente** — sem facilitação boa, vira discussão técnica sobre nada
- **Sem domain experts** — o workshop vira invenção. Precisa de quem SABE como o negócio funciona
- **Discutir tecnologia durante Big Picture** — "vai ser um microserviço?" "usamos Kafka?" — não é hora. Foque em negócio.
- **Eventos no presente ou futuro** — "Confirmar Pedido" é comando, não evento. "Pedido Confirmado" é evento.
- **Eventos técnicos, não de negócio** — "Request Received", "Cache Invalidated" — isso é implementação, não domínio.
- **Pular Big Picture e ir direto para Software Design** — vira modelagem no vácuo, sem entender o todo
- **Ignorar hot spots** — hot spots são onde mora o aprendizado
- **Muita gente na sala** — 15+ pessoas = caos. Divida em grupos.
- **Hierarquia dominando** — se o CTO fala e ninguém discorda, você tem teatro, não descoberta
- **Workshop sem próximos passos** — sem follow-up, o valor se perde
- **Não documentar o resultado** — fotografe, transcreva, preserve o aprendizado
- **Querer mapear tudo em um único workshop** — grandes domínios exigem múltiplas sessões
- **Laptops na sala** — mata a energia e o engajamento

---

## Na prática (da minha experiência)

> **Muvz — Event Storming para migração de monolito:**
> Na Muvz, usamos Event Storming para descobrir bounded contexts antes de decidir como quebrar o monolito EJB em microserviços. Fizemos um **Big Picture Event Storming** de dois dias com product owners, especialistas do negócio, tech leads e devs. A parede tinha mais de 8 metros de post-its laranja.
>
> **O que aprendemos:**
>
> **1. A realidade era mais complexa que a documentação.** A documentação oficial tinha 3 fluxos. O workshop revelou 11 fluxos, incluindo vários que só o pessoal de suporte conhecia ("quando acontece X, eu vou no banco e faço Y manualmente...").
>
> **2. Bounded contexts não eram o que pensávamos.** Tinhamos 3 bounded contexts "óbvios" na cabeça. O workshop revelou 5. Dois deles eram coisas que sempre tratamos juntas mas tinham linguagens e regras totalmente diferentes (eram o mesmo conceito só em superfície).
>
> **3. Hot spots estavam em todo lugar.** Marcamos dezenas de pontos com rosa — áreas onde ninguém sabia a regra, onde havia discordância, ou onde a implementação atual era workaround. Isso virou nosso backlog de descoberta.
>
> **4. Ubiquitous language emergiu naturalmente.** Durante o workshop, negociamos termos: "contrato" vs "apólice" vs "assinatura" — coisas que no código eram misturadas. Depois do workshop, o glossário compartilhado eliminou uma categoria inteira de bugs de comunicação.
>
> **5. Os microserviços finais refletiram o resultado do workshop.** Os 5 microserviços que acabamos construindo respeitaram os 5 bounded contexts descobertos. Sem o workshop, teríamos feito os 3 óbvios errados, e descoberto a dor depois.
>
> **MedEspecialista — Process Modelling para feature nova:**
> Quando precisei desenhar o fluxo de reagendamento de consultas (que parecia simples mas envolvia regras complexas de cancellation, reembolso, notificação ao médico, slot de volta na disponibilidade, etc.), fizemos um Process Modelling Event Storming em 3 horas. Descobrimos 6 casos alternativos que ninguém tinha mapeado, incluindo um que tinha implicações financeiras.
>
> **Lição chave: o valor está no workshop, não no artefato.** Os post-its acabaram sendo fotografados e arquivados. O que ficou foi o **entendimento compartilhado**. Um mês depois, quando implementamos, ninguém olhou para as fotos — mas todo mundo lembrava das decisões. O workshop é a forma de aprender coletivamente, não de documentar.
>
> **Dica de facilitação:** comece a sessão com um exemplo famoso (ex.: "vamos fazer um Event Storming do processo de comprar um livro na Amazon") por 15 min. Isso quebra o gelo e ensina a técnica na prática. Depois vá para o domínio real.

---

## How to explain in English

> "Event Storming is a collaborative workshop technique created by Alberto Brandolini for discovering complex domains through business events. It's my go-to technique when starting a new project, modernizing a legacy system, or identifying bounded contexts for a migration to microservices.
>
> The core idea is simple: you gather developers, domain experts, and stakeholders around a wall covered with sticky notes, and you write down everything that happens in the business as events in past tense — like 'Order Placed', 'Payment Confirmed', 'Shipment Delivered'. The wall becomes a shared model that everyone contributes to and understands.
>
> There are three levels. Big Picture Event Storming maps the entire domain at a high level to discover bounded contexts and hotspots — areas of confusion or complexity. Process Modelling zooms into specific processes, adding actors, commands, policies, and external systems. Software Design Event Storming is the bridge to implementation, identifying aggregates and invariants.
>
> At Muvz, I used Big Picture Event Storming to guide a monolith-to-microservices migration. The workshop revealed five bounded contexts instead of the three we thought we had, and the resulting microservices structure was directly informed by that discovery. Without the workshop, we would have drawn the wrong lines and paid for it later.
>
> What I value most is not the artifact — the wall of sticky notes — but the shared understanding it creates. The conversation during the workshop is where the learning happens. A month later, people remember the decisions without looking at the photos, because they lived the discovery process."

### Frases úteis em entrevista

- "Event Storming is a collaborative workshop to discover complex domains through business events."
- "The three levels — Big Picture, Process Modelling, Software Design — serve different purposes."
- "I use Big Picture Event Storming to discover bounded contexts before committing to a microservices split."
- "Hot spots — areas of confusion or disagreement — are where the most learning happens."
- "The workshop's value is the shared understanding, not the artifact."
- "Events are written in past tense — they're facts that happened, not intentions."
- "Event Storming is my go-to technique for building ubiquitous language with business experts."
- "Without domain experts in the room, Event Storming becomes invention rather than discovery."

### Key vocabulary

- tempestade de eventos → event storming
- evento de domínio → domain event
- comando → command
- política → policy
- ator → actor
- agregado → aggregate
- modelo de leitura → read model
- sistema externo → external system
- ponto quente → hot spot
- evento crítico → pivotal event
- contexto delimitado → bounded context
- linguagem ubíqua → ubiquitous language
- facilitador → facilitator
- especialista de domínio → domain expert
- descoberta colaborativa → collaborative discovery
- nível panorâmico → big picture level
- modelagem de processos → process modelling
- design no nível de software → software design level

---

## Recursos

### Livros

- **[Introducing EventStorming](https://www.eventstorming.com/book/)** — Alberto Brandolini (o livro oficial, em progresso há anos, versões intermediárias disponíveis no LeanPub)

### Artigos canônicos

- [Introducing EventStorming — Alberto Brandolini](http://ziobrando.blogspot.com/2013/11/introducing-event-storming.html) — o artigo original
- [How to explain Design Level Event Storming to your mother](https://www.eventstormingjournal.com/software%20design/how-to-explain-design-level-event-storming-to-your-mother/)
- [Remote EventStorming](https://blog.avanscoperta.it/2020/03/26/remote-eventstorming/) — Brandolini sobre workshops remotos
- [Collaborative Process Modelling with EventStorming](https://medium.com/@ziobrando/collaborative-process-modelling-with-eventstorming-17ed363650c0) — Brandolini
- [EventStorming — going beyond the superficial](https://www.eventstore.com/blog/event-storming-going-beyond-the-superficial)
- [Event Storming and Spring with a splash of DDD](https://spring.io/blog/2018/04/11/event-storming-and-spring-with-a-splash-of-ddd) — Jakub Pilimon (Pivotal)
- [An introduction to EventStorming, the easy way to do DDD](https://techbeacon.com/introduction-event-storming-easy-way-achieve-domain-driven-design) — Stephen A. Lowe
- [Facilitating EventStorming](http://verraes.net/2013/08/facilitating-event-storming/) — Mathias Verraes
- [Event Storming — guia básico (pt-br)](https://medium.com/@jonesroberto/event-storming-guia-básico-216498f5dd2d)

### Cheat sheets e recursos

- [Event Storming Cheat Sheet (Weave IT)](https://weave-it.org/blog/eventstorming-cheat-sheet/)
- [DDD Crew — EventStorming Glossary & Cheat Sheet](https://github.com/ddd-crew/eventstorming-glossary-cheat-sheet)
- [Event Storming Workshop Cheat Sheet](https://github.com/wwerner/event-storming-cheatsheet)
- [Awesome Event Storming — Mariusz Gil](https://github.com/mariuszgil/awesome-eventstorming) — coleção completa
- [Event Storming Journal](https://www.eventstormingjournal.com/) — casos práticos

### Vídeos essenciais

> [!info] 50,000 Orange Stickies Later — Alberto Brandolini @ ExploreDDD 2017
> [https://www.youtube.com/watch?v=1i6QYvYhlYQ](https://www.youtube.com/watch?v=1i6QYvYhlYQ)
> Provavelmente a melhor visão geral dos diferentes formatos de Event Storming.

> [!info] Extreme Modelling Patterns — Alberto Brandolini @ DDD Europe 2023
> [https://www.youtube.com/watch?v=jv1-ohCWbE0](https://www.youtube.com/watch?v=jv1-ohCWbE0)

> [!info] Domain-Driven Design in ProductLand — Alberto Brandolini @ DDD Europe 2022
> [https://youtu.be/ufdcfe8VmHM](https://youtu.be/ufdcfe8VmHM)

> [!info] EVENT STORMING — DDD, EVENT SOURCING E CQRS (pt-br)
> [https://www.youtube.com/watch?v=s8cvn2TUXoM](https://www.youtube.com/watch?v=s8cvn2TUXoM)

> [!info] DOMINE O EVENT STORMING! (pt-br)
> [https://www.youtube.com/watch?v=Y31kprvAfIE](https://www.youtube.com/watch?v=Y31kprvAfIE)

> [!info] Event Storming — what it is and why you should use it with DDD
> [https://www.youtube.com/watch?v=7LFxWgfJEeI](https://www.youtube.com/watch?v=7LFxWgfJEeI)

### Outros vídeos de Brandolini

- [No, you don't need to access my data](https://www.youtube.com/watch?v=gU-p90-EYSY) — DDD Europe 2021
- [Extreme Domain-Driven Design Modelling](https://youtu.be/uJ4mPU1i6E0) — Nexten webinar
- [100,000 Orange Stickies Later](https://youtu.be/fGm62ra_mQ8) — Øredev 2019
- [The Gordian Knot](https://blog.avanscoperta.it/it/2019/06/05/alberto-brandolini-the-gordian-knot-mucon-london-2019-skills-matter/) — muCon 2019
- [Joys and Pitfalls of Collaborative Modelling](https://blog.avanscoperta.it/it/2018/05/02/alberto-brandolinis-keynote-at-ddd-exchange-2018-skills-matter-london/) — DDDX London 2018
- [Transactions Redefined](https://www.youtube.com/watch?v=NqKNqIsB8_k) — DDD Europe 2017
- [The Precision Blade](https://www.youtube.com/watch?v=lG46Yo_9DPc) — DDD Europe 2016
- [Introducing EventStorming](https://vimeo.com/130202708) — NCrafts Paris 2015

### Outros autores

- [EventStorming for fun and profit](https://speakerdeck.com/tastapod/event-storming-for-fun-and-profit) — Dan North, DDDX 2017
- [EventStorming — collaborative learning for complex domains](https://www.youtube.com/watch?v=vf6x0i2d9VE) — Paul Rayner
- [EventStorming the perfect wedding](https://baasie.com/2018/08/17/eventstorming-the-perfect-wedding/) — Kenny Baas
- [From Big Picture to Software Design](https://www.agilepartner.net/eventstorming-from-big-picture-to-software-design/) — Cédric Pontet
- [A step by step guide to Event Storming](https://www.boldare.com/blog/event-storming-guide/) — Natalia Kolińska (Boldare)

### Exemplos

- [[Exemplos]] — casos práticos anotados

---

## Veja também

- [[Arquitetura de Software]] — DDD (estratégico e tático), bounded contexts
- [[Event Streaming]] — implementação técnica de eventos de domínio
- [[03-Dominios/Java/Backend/Kafka/Kafka]] — onde os eventos de domínio viram mensagens
- [[System Design]] — como os bounded contexts viram microserviços
- [[API Design]] — como os commands descobertos viram endpoints
- [[Mensageria]] — como os eventos fluem entre serviços
