---
title: "Design Spec — Trilha System Design (Onda C, item 8)"
created: 2026-07-06
type: meta
publish: false
tags:
  - meta
  - spec
  - system-design
---

# Design Spec — Trilha System Design

> Refator de monólito (tronco→galhos), **não greenfield**. Alvo: item 8 da Onda C do [[00-Meta/Roadmap]] — "escalar de 7 notas para trilha de entrevista sênior (CAP, sharding, caching, filas, consistência, design exercises)".

## Contexto

A pasta `03-Dominios/Engenharia/Arquitetura/` guarda dois monólitos que ensinam habilidades diferentes:

- **`System Design.md`** (921 linhas) — a habilidade de *whiteboard* de entrevista. **É o alvo desta trilha.**
- **`Arquitetura de Software.md`** (992 linhas) — o ofício de arquitetura (estilos, DDD, SOLID, Conway, C4/ADR, observabilidade). **Fora do escopo desta sessão** — vira trilha própria no futuro.

Mais o galho **Event Storming** (existente) e o stub **Gateway de Pagamento**.

## Decisões travadas (com o usuário, 2026-07-06)

1. **Sub-galhos**, não galho único flat.
2. Os **8 walkthroughs viram 8 notas Magus densas** (aplicação ponta-a-ponta) — é o coração da trilha.
3. É **System Design (sistemas distribuídos)**, não design system de UI.
4. Tópicos que moram em outros galhos **podem ser revisitados aqui sob a ótica de system design** — redundância como reforço, sempre com cross-link.

## Estrutura de pastas

```
Engenharia/Arquitetura/
├── System Design.md            ← vira TRONCO PODADO (overview + porta de entrada)
├── System Design/              ← galho-pai (novo)
│   ├── index.md                (MOC do galho-pai)
│   ├── roadmap.md              (roadmap recursivo, galho-pai)
│   ├── 1 - Framework de entrevista/   (sub-galho, fase Iniciado)
│   ├── 2 - Building blocks/            (sub-galho, fase Adepto)
│   ├── 3 - Padrões recorrentes/        (sub-galho, fase Adepto)
│   └── 4 - Walkthroughs/               (sub-galho, fase Magus)
├── Arquitetura de Software.md  ← NÃO tocar nesta sessão
└── Event Storming/             ← existente; linkar, não reescrever
```

Cada subpasta de sub-galho recebe `index.md` (MOC) + `roadmap.md` (folha) + notas numeradas reiniciando em 01.

## Roster de notas

### Sub-galho 1 — Framework de entrevista (Iniciado, ~5 notas)

> Como conduzir os 45-60 min do whiteboard sem travar. É a fase Iniciado: dá o processo antes do conteúdo.

| # | Nota | Escopo | Fontes-âncora |
|---|------|--------|---------------|
| 01 | O que é System Design (e o que a entrevista avalia) | Sinal buscado pelo entrevistador: estruturação, trade-offs, comunicação — não "a resposta certa". Rubrica de senioridade. | Alex Xu Vol.1 cap.1; Hello Interview "Delivery" |
| 02 | Clarificar requisitos: funcionais, não-funcionais, restrições | Perguntas de escopo; separar RF de RNF (latência, disponibilidade, consistência); fechar o escopo antes de desenhar. | System Design Primer; Alex Xu |
| 03 | Estimativas de escala (back-of-envelope) | QPS = usuários×ações/86.400; peak factor 3-5; storage/bandwidth; **latency numbers** (jboner); powers of two. | jboner gist; ByteByteGo estimation; Hello Interview "Numbers to Know" |
| 04 | API design & data model na entrevista | Esboçar endpoints/contratos e o modelo de dados de forma enxuta; quando SQL vs NoSQL entra cedo. | Alex Xu; [[API Design]] |
| 05 | Diagrama de alto nível → deep dive → trade-offs | Sequência dos 45 min: desenho macro, aprofundar 1-2 componentes, fechar com trade-offs e evolução. | Alex Xu framework; designgurus "First 10 minutes" |

### Sub-galho 2 — Building blocks (Adepto, ~7 notas)

> O vocabulário de escala. Cada bloco é uma peça que reaparece nos walkthroughs.

| # | Nota | Escopo | Fronteira / cross-link |
|---|------|--------|------------------------|
| 01 | Escalabilidade & load balancing | Vertical vs horizontal, stateless, L4 vs L7, health checks, sticky sessions. | linka [[Redes e Protocolos]] |
| 02 | Caching | cache-aside / write-through / write-back, TTL, eviction (LRU/LFU), **cache stampede** e mitigação. | linka Redis |
| 03 | Bancos de dados em escala: SQL vs NoSQL & replicação | Modelos de dado, leader-follower, read replicas, quando desnormalizar. | reforço de [[03-Dominios/Ciência/Banco de Dados/index\|Banco de Dados]] sob ótica SD |
| 04 | Sharding & Consistent Hashing | Estratégias de partição (range/hash/geo), hot spots, **consistent hashing** (anel, virtual nodes) e rebalanceamento. | tópico top-pedido; reforça, não duplica BD |
| 05 | Message queues & processamento assíncrono | Fila vs log, backpressure, at-least/exactly-once sob ótica de design; desacoplar produtor/consumidor. | usa [[03-Dominios/Engenharia/Comunicação entre Sistemas/Mensageria/Kafka\|Kafka]]/[[RabbitMQ]] como bloco; linka o detalhe |
| 06 | CAP, consistência e consenso | CAP e PACELC, consistência eventual/forte, quorum (R+W>N), leader election (intuição de Raft/Paxos). | reforça CAP do monólito; conceito em [[03-Dominios/Fundamentos]] |
| 07 | CDN & entrega na borda | PoPs, cache hit ratio, invalidação/purge, push vs pull, TLS termination na borda. | da pesquisa 2025; linka caching (02) |

### Sub-galho 3 — Padrões recorrentes (Adepto, ~6 notas)

> Padrões que aparecem em quase todo design não-trivial. Vistos aqui pela lente "como usar em escala", não "como modelar o domínio".

| # | Nota | Escopo | Fronteira / cross-link |
|---|------|--------|------------------------|
| 01 | Pub/Sub & event-driven em escala | Broker, tópicos, fan-out, ordering, entrega; quando event-driven vence request-response. | linka [[Arquitetura de Software]] (EDA) |
| 02 | CQRS sob a ótica de system design | Separar read/write models por razão de escala/latência; read replicas materializadas. | **reforço** de [[Event Storming]]/[[Arquitetura de Software]] + cross-link explícito |
| 03 | Event Sourcing sob a ótica de system design | Log de eventos como fonte da verdade; replay, snapshots, projeções; custo operacional. | **reforço** de [[Event Storming]] + cross-link |
| 04 | Rate Limiting | Token bucket / leaky bucket / sliding window; **distribuído com Redis + Lua** (atômico), header 429. | aprofundado no walkthrough 4 |
| 05 | Circuit Breaker & resiliência | Timeout, retry (backoff+jitter), bulkhead, fallback; estados closed/open/half-open. | reforça Resilience4j de [[Spring Boot]] sob ótica de design |
| 06 | API Gateway & BFF | Roteamento, auth, rate-limit, agregação; Backend-for-Frontend; onde o gateway vira gargalo. | linka [[API Design]] / Comunicação entre Sistemas |

### Sub-galho 4 — Walkthroughs (Magus, 8 notas densas)

> Cada nota conduz um design completo aplicando os building blocks e padrões. Estrutura fixa por nota: requisitos → estimativas → API → diagrama macro → deep dives → gargalos & trade-offs → variações de follow-up.

| # | Sistema | Peças-chave que a nota exercita |
|---|---------|----------------------------------|
| 01 | **URL Shortener** (bit.ly) | hashing/base62, colisões, read-heavy, cache, analytics assíncrono |
| 02 | **News Feed / Timeline** (Twitter/Instagram) | fan-out on-write vs on-read, celebridades, feed cache, ranking |
| 03 | **Chat System** (WhatsApp/Slack) | WebSocket, presence, entrega/ordering, grupos, fila offline |
| 04 | **Distributed Rate Limiter** | aprofunda o padrão (SG3-04) em sistema completo: Redis, sincronização entre nós |
| 05 | **Notification System** | fan-out multi-canal (push/SMS/email), templates, dedup, retry, prioridade |
| 06 | **Distributed File Storage** (Drive/Dropbox) | chunking, metadata service, dedup, sync, consistência |
| 07 | **Web Crawler** (Googlebot) | BFS distribuído, politeness, dedup de URL, armadilhas de spider |
| 08 | **Distributed Key-Value Store** (DynamoDB/Cassandra) | consistent hashing, quorum, replicação, gossip, vector clocks |

**Capstone (opcional, no galho-pai):** "Conduzindo a entrevista completa" — um walkthrough integral comentado meta-nível (gestão de tempo, sinais, recuperação de travadas). Decidir ao fechar o SG4.

## Fronteiras anti-duplicação

| Tópico | Papel aqui | Mora em | Regra |
|--------|-----------|---------|-------|
| DDD estratégico/tático, Event Storming | — | Arquitetura de Software.md, [[Event Storming]] | linkar |
| Estilos (Hexagonal/Clean/Onion) | — | Arquitetura de Software.md | linkar |
| SOLID, design de código | — | Design de Software | linkar |
| APIs REST/GraphQL/gRPC (detalhe) | building block | [[API Design]], Comunicação entre Sistemas | usar + linkar |
| Kafka/RabbitMQ internals | bloco de fila | Comunicação/Mensageria | usar + linkar |
| CQRS / Event Sourcing | ótica de escala | Event Storming | **reforço** + cross-link |
| ACID, índices, replicação SQL | usa | Ciência/Banco de Dados | reforço + linkar |
| Observabilidade (craft logs/metrics/traces) | usa p/ operar o design | Arquitetura de Software.md | linkar |

## Padrão de escrita (cravado)

Nota = **capítulo de livro** ([[feedback_padrao_capitulo_livro]]): TL;DR `[!abstract]`, abertura-problema concreta, divulgação progressiva, exemplo trabalhado. Densidade-alvo **~440-540 linhas** ([[feedback_notas_profundas_diagramas]]) — mirar mais alto que a sessão de Web Performance/Testes JS. `fase:` no frontmatter (Iniciado/Adepto/Magus). ≥1 diagrama Mermaid (paleta azul `#4A90D9` / âmbar `#F5A623` / vermelho `#D0021B`). Callouts `[!question]-` (dúvidas) e `[!warning]` (armadilhas). Seção "Em entrevista" + "How to explain in English" com tabela PT↔EN. "O que vem a seguir". `## Fontes` com URL e dado sempre cravado com data/versão (caducidade). Pesquisa web inline por nota (via `escrever-nota`). **Gravar direto**, sem gate de rascunho.

## Fontes canônicas da trilha

- **Livros:** *Designing Data-Intensive Applications* (Kleppmann); *System Design Interview Vol.1 & 2* (Alex Xu); *Building Microservices* (Newman); *Database Internals* (Petrov).
- **Online:** [System Design Primer](https://github.com/donnemartin/system-design-primer); [ByteByteGo](https://bytebytego.com/); [Hello Interview — System Design in a Hurry](https://www.hellointerview.com/learn/system-design/in-a-hurry/introduction) (novo, 2024-2026); [Latency Numbers Every Programmer Should Know](https://gist.github.com/jboner/2841832); [High Scalability](http://highscalability.com/); Martin Fowler (CQRS/ES).

## Plano de execução (ritmo B)

1. Criar `System Design/index.md` + `System Design/roadmap.md` (galho-pai).
2. Semear sub-galho a sub-galho, ponta a ponta, na ordem 1→2→3→4 (fases Iniciado→Adepto→Magus). Cada subpasta ganha `index.md` + `roadmap.md` + notas via `escrever-nota`.
3. Ao fechar cada sub-galho: atualizar seu `roadmap.md` e o do galho-pai; commit por sub-galho (paths explícitos, `git diff --cached`, **sem Co-Authored-By**, push manual).
4. Podar `System Design.md` → overview com callouts apontando pros sub-galhos (padrão tronco→galho).
5. Atualizar [[00-Meta/Roadmap]] item 8 (🟡→🟢 ao fechar) e a memória.

## Pontos em aberto

- CDN (SG2-07): nota dedicada (proposto) ou dobrar em Caching? — decisão ao chegar no SG2.
- Capstone do galho-pai: escrever ou não ao fechar o SG4.
- Renumeração/ordem exata dentro de cada sub-galho pode ajustar durante o seeding.
