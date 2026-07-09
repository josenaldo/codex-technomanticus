---
title: "Design Spec — Trilha Comunicação entre Sistemas"
created: 2026-07-09
type: meta
publish: false
tags:
  - meta
  - spec
  - comunicacao-entre-sistemas
---

# Design Spec — Trilha Comunicação entre Sistemas

> Item 10 da Onda C do [[00-Meta/Roadmap]] — a camada de **contrato**: como sistemas conversam (síncrono e assíncrono), o panorama histórico/comparativo dos protocolos, e confiabilidade da comunicação. Terceira trilha do trio [[project_trilha_system_design|System Design]] (desenha) → [[project_trilha_operacao|Operação]] (opera) → Comunicação (contrata).

## Ponto de vista (travado com o usuário 2026-07-09)

Trilha **comparativa e decisória, não tutorial**. O leitor já conhece as ferramentas (REST, gRPC, Kafka, etc. como conceito) e já viu implementação em pelo menos uma stack — o que falta é o mapa: **por que existem tantas formas de comunicação, quando cada uma vale, o que é legado vs o que é hype, e como a mesma decisão aparece em Java/TS/Python/Go** (menção comparativa curta, nunca tutorial completo — ver fronteiras abaixo).

Consequências desse POV:
- Cada nota resolve uma **decisão** ("REST ou gRPC aqui?", "fila ou stream?"), não ensina sintaxe.
- Comparação entre linguagens é **citação/tabela curta**, não implementação passo a passo — quem quer o tutorial vai pra trilha da linguagem.
- Amplitude deliberada: cobre não só REST/API (viés do rascunho inicial, corrigido pelo usuário) mas RPC legado, mensageria, tempo real, e o que está emergindo.

## Pesquisa prévia — Full Cycle (2026-07-09)

Curadoria de mercado antes do desenho, por pedido do usuário:

- **Full Cycle 3.0** tem um módulo chamado literalmente *"Comunicação entre Sistemas"*: REST (Richardson Maturity Model, HATEOAS, **HAL**, content/method negotiation), gRPC (Protobuf, HTTP/2, os 4 tipos de streaming — unary/server/client/bidirectional), GraphQL (schema, types, queries, mutations, resolvers). Confirma que **Maturity Model e HAL faltavam** no rascunho inicial — incorporados abaixo.
- **Full Cycle 4.0** expandiu: módulo "APIs" (REST+maturity+gRPC+API Gateway+versionamento+depreciação+paginação+padrões de proteção), módulos dedicados a **RabbitMQ** e **Kafka**, módulo "DDD e arquitetura orientada a eventos" (Domain Events, CQRS, Event Sourcing, Unit of Work, Event Storming — tratado como **fora de escopo aqui**, é DDD, não comunicação — ver fronteiras), módulo "Microsserviços" (coreografia vs orquestração, ACL, Strangler, BFF — já coberto por [[03-Dominios/Engenharia/Arquitetura/System Design/index|System Design]] e Java Microservices).

## Contexto: o que já existe

`03-Dominios/Engenharia/Comunicação entre Sistemas/` já é domínio (Engenharia — correto, "disciplina neutra de stack"). Conteúdo hoje = 2 monólitos:

- `API Design.md` (1325 ln) — REST/recursos, status codes, RFC 9457, paginação, filtering, versionamento, auth, idempotência, rate limiting, caching HTTP, webhooks, bulk, upload, async ops, REST vs GraphQL vs gRPC, OpenAPI, testes. Contém seção **"Na prática (da minha experiência)" do usuário — preservar verbatim**.
- `Mensageria/` — cluster de ferramenta: `Mensageria.md` (panorama, 776 ln), `Kafka.md` (918), `RabbitMQ.md` (930), `BullMQ.md` (786), `Event Streaming.md` (638), `index.md`.

Implementação por linguagem já existe (profunda, em outras trilhas — **não duplicar**):
- **Java:** `Java/Web e APIs REST` (16 notas: Spring MVC, RFC 9457, versionamento, OpenAPI, HATEOAS), `Java/Mensageria` (29 notas: Kafka, RabbitMQ, idempotência, Outbox, Saga, Event Sourcing/CQRS, Protobuf, gRPC), `Java/Microservices` (comunicação síncrona/assíncrona, API Gateway, resiliência).
- **Node/TS:** `Node/Integrações` (gRPC via grpc-js, GraphQL via Apollo/Mercurius, WebSockets, Kafka via kafkajs, clientes HTTP, resiliência).
- **Go/Python:** só stubs rasos (`Go Backend.md`, `Python Backend.md`) — sem trilha profunda. Menção conceitual aqui é aceitável; **não é escopo desta trilha construir a trilha de Go/Python**.

## Estrutura de pastas

```
Engenharia/Comunicação entre Sistemas/
├── index.md                          (MOC do galho-pai, já existe — atualizar)
├── roadmap.md                        (roadmap recursivo, novo)
├── API Design.md                     (vira tronco podado)
├── Mensageria/                       (permanece — referência de ferramenta)
├── 1 - Panorama e decisão/            (Iniciado)
├── 2 - Comunicação síncrona/          (Adepto)
├── 3 - Confiabilidade do contrato/    (Adepto→Magus)
└── 4 - Comunicação assíncrona/        (Adepto→Magus)
+ capstone no galho-pai (Magus)
```

## Roster de notas

### Sub-galho 1 — Panorama e decisão (Iniciado, ~5 notas)

> O mapa antes do território: por que tantas formas de comunicação existem, o eixo síncrono/assíncrono, e como decidir.

| # | Nota | Escopo | Fronteira / cross-link |
|---|------|--------|------------------------|
| 01 | O que é o contrato de comunicação | Producer/consumer, acoplamento, o contrato como abstração central; sync vs async como primeiro eixo de decisão. | enquadra a trilha |
| 02 | RPC clássico e por que caiu | CORBA, DCOM, XML-RPC, SOAP/WSDL — o que resolviam, por que foram substituídos, **onde ainda sobrevivem** (EDI em saúde/bancos, integrações legadas B2B). | histórico, sem tutorial |
| 03 | A era REST, GraphQL, gRPC | Por que REST venceu como default, por que GraphQL e gRPC surgiram como resposta a problemas específicos (over-fetching, performance interna). | prepara SG2 |
| 04 | Comunicação em tempo real | WebSocket, Server-Sent Events, WebTransport — quando cada um, o que substituiu polling. | linka [[Redes e Protocolos]] |
| 05 | O que está emergindo e framework de decisão | tRPC, Connect (Buf), AsyncAPI, CloudEvents, e o cruzamento com IA (MCP) — panorama do que é hype vs o que fica. Fecha com árvore de decisão "qual estilo pra qual problema", com nota comparativa curta por linguagem (Go: gRPC nativo; Python: FastAPI+strawberry; TS: peculiaridade do tRPC). | fecha o sub-galho |

### Sub-galho 2 — Comunicação síncrona: REST, GraphQL, gRPC (Adepto, ~6 notas)

> A decisão técnica de como desenhar o contrato síncrono.

| # | Nota | Escopo | Fronteira / cross-link |
|---|------|--------|------------------------|
| 01 | REST: modelagem de recursos e maturidade | Recursos como substantivos, verbos HTTP, nested vs flat, **Richardson Maturity Model** (níveis 0-3), **HATEOAS/HAL** na prática. | reforço de `API Design.md` (migra) |
| 02 | REST: o contrato de resposta | Status codes com significado, RFC 9457 Problem Details, content negotiation. | reforço de `API Design.md` |
| 03 | Paginação, filtros e autenticação em REST | Offset vs cursor, filtering/sorting, panorama de métodos de auth (API key/JWT/OAuth/mTLS) — decisão, não implementação (JWT deep-dive já é Node/Segurança, Java/Segurança). | linka Node/Segurança, Java/Segurança |
| 04 | GraphQL — schema, resolvers e quando vale | Types, queries, mutations, resolvers, N+1/DataLoader, quando escolher e quando é overkill. | linka Node/Integrações (Apollo/Mercurius) |
| 05 | gRPC — Protobuf, HTTP/2 e streaming | Motivação, Protocol Buffers, HTTP/2 multiplexing, os 4 tipos de streaming (unary/server/client/bidi). | linka Java/Mensageria 27-28 (Protobuf/gRPC Java), Node/Integrações 05 |
| 06 | REST vs GraphQL vs gRPC — decisão | Comparação final, documentação como contrato (OpenAPI vs .proto vs SDL), contract testing (Pact/Prism). | fecha o sub-galho |

### Sub-galho 3 — Confiabilidade do contrato (Adepto→Magus, ~5 notas)

> O contrato promete — como garantir que ele se sustenta sob falha, retry e o tempo.

| # | Nota | Escopo | Fronteira / cross-link |
|---|------|--------|------------------------|
| 01 | Idempotência | Por que POST não é idempotente, Idempotency-Key pattern (Stripe), armazenamento atômico. | reforço de `API Design.md`; linka Java/Mensageria 20 |
| 02 | Versionamento e evolução de contrato | URL/header/query versioning, regras de evolução segura (adicionar é seguro, remover não), deprecation (RFC 8594). | reforço de `API Design.md` |
| 03 | Caching HTTP e requisições condicionais | Cache-Control, ETag, If-None-Match, optimistic locking com If-Match. | reforço de `API Design.md` |
| 04 | Rate limiting como contrato | Headers de resposta, 429 + Retry-After, tiers. **Algoritmo (token bucket etc.) é [[04 - Rate Limiting|System Design SG3-04]]** — aqui só o que a API expõe. | reforço leve; fronteira explícita com SG |
| 05 | Webhooks e operações assíncronas | 202 Accepted + polling, webhooks (assinatura HMAC, retry, dedup), bulk operations. | reforço de `API Design.md`; linka sub-galho 4 (mensageria invertida) |

### Sub-galho 4 — Comunicação assíncrona e mensageria (conceitual) (Adepto→Magus, ~6 notas)

> Desacoplar no tempo. Panorama e decisão — ferramenta específica (Kafka/RabbitMQ/BullMQ) já tem casa em `Mensageria/*.md`.

| # | Nota | Escopo | Fronteira / cross-link |
|---|------|--------|------------------------|
| 01 | Síncrono vs assíncrono — quando desacoplar | Aprofunda o eixo do SG1-01: latência vs throughput, acoplamento temporal, o custo de complexidade da assincronia. | reforço de `Mensageria.md` |
| 02 | Message queue vs event streaming | Fila de tarefa vs log de eventos, panorama comparativo de brokers (Kafka/RabbitMQ/SQS/NATS/Pulsar/BullMQ) — tabela de decisão, ferramenta individual fica nas páginas existentes. | referência: `Mensageria/*.md` |
| 03 | Garantias de entrega e ordenação | At-most/at-least/exactly-once, idempotência no consumer, ordenação por partição/fila/FIFO. | reforço de `Mensageria.md` |
| 04 | Outbox e Saga | Transações distribuídas por eventos, o padrão Outbox, coreografia vs orquestração de Saga. | linka Java/Mensageria 21-22; **não** SG (Pub/Sub é lá, Saga/Outbox não existem lá) |
| 05 | Legado e padrões enterprise | JMS, IBM MQ, ESB (Enterprise Service Bus) — o que resolviam, por que a indústria migrou pra brokers modernos, onde ainda aparecem (bancos, seguradoras). | histórico, sem tutorial |
| 06 | O que está emergindo em mensageria | CloudEvents (envelope padrão), AsyncAPI (o "OpenAPI dos eventos"), webhooks como mensageria invertida (fecha o loop com SG3-05). | fecha o sub-galho |

### Capstone (Magus, galho-pai)

**"Desenhando a comunicação de um sistema do zero"** — walkthrough único que percorre um cenário concreto (ex.: e-commerce com checkout + pagamento assíncrono + notificação) decidindo, ponto a ponto: REST vs gRPC vs GraphQL na borda, fila vs stream internamente, onde idempotência é obrigatória, onde webhook entra. Costura os 4 sub-galhos num arco. Puxar experiência real do usuário só se ele fornecer (nunca fabricar — [[feedback_no_fabrication]]).

**Total planejado:** ~22 notas (5+6+5+6) + 1 capstone = **~23 notas**.

## Fronteiras anti-duplicação

| Tópico | Papel aqui | Mora em | Regra |
|--------|-----------|---------|-------|
| Pub/Sub em escala, message queues como building block de infra, API Gateway, CQRS, Event Sourcing, Circuit Breaker, Rate limiting (algoritmo) | — | [[03-Dominios/Engenharia/Arquitetura/System Design/index\|System Design]] SG2/SG3 | referência: linkar, não reescrever |
| Implementação REST/gRPC/mensageria em **Java** | — | `Java/Web e APIs REST`, `Java/Mensageria`, `Java/Microservices` | reforço + cross-link, sem tutorial aqui |
| Implementação gRPC/GraphQL/WebSocket em **Node/TS** | — | `Node/Integrações` | reforço + cross-link |
| Implementação em **Go/Python** | menção conceitual curta apenas | não existe trilha profunda ainda | **não** criar tutorial completo aqui; sinalizar lacuna, não preencher |
| Auth detalhada (JWT impl, OAuth flows, RBAC/ABAC) | panorama de decisão | `Node/Segurança`, `Java/Segurança` | linkar, sem reimplementar |
| Domain Events, CQRS/DDD, Event Storming, Unit of Work | fora de escopo | futuro domínio DDD (não existe ainda) | **não** entrar — é DDD, não comunicação |
| Ferramenta de broker (Kafka/RabbitMQ/BullMQ deep-dive) | referência | `Mensageria/*.md` (existente) | ganha callout apontando pra cá |
| Service Discovery/Consul | fora de escopo desta trilha | candidato a System Design building block (não coberto ainda) | não entrar; anotar como lacuna futura de SG, não desta trilha |

## Padrão de escrita (cravado, herdado de System Design/Operação)

Nota = **capítulo de livro** ([[feedback_padrao_capitulo_livro]]): TL;DR `[!abstract]`, abertura problema-first, divulgação progressiva, exemplo trabalhado. Densidade-alvo **~440-540 linhas** ([[feedback_notas_profundas_diagramas]]). `fase:` no frontmatter. ≥1 Mermaid (paleta azul `#4A90D9` / âmbar `#F5A623` / vermelho `#D0021B`). Callouts `[!question]-`/`[!warning]`. Seção "Em entrevista" + "How to explain in English" (tabela PT↔EN). "O que vem a seguir". `## Fontes` datadas. **Comparação por linguagem = tabela/menção curta, nunca subseção de tutorial completo** (regra nova desta trilha, por pedido explícito do usuário). Barra de densidade explícita no prompt de cada subagente (5-7k palavras / 15-25 buscas / exemplo concreto).

## Fontes canônicas da trilha

- **Livros:** *API Design Patterns* (JJ Geewax); *Designing Web APIs* (Jin/Sahni/Shevat); *RESTful Web APIs* (Richardson/Amundsen); *Enterprise Integration Patterns* (Hohpe/Woolf — mensageria clássica); *Designing Data-Intensive Applications* (Kleppmann — streams e garantias de entrega).
- **Cursos/mercado:** Full Cycle 3.0 (módulo "Comunicação entre Sistemas") e Full Cycle 4.0 (módulos APIs/RabbitMQ/Kafka) — usados como curadoria de escopo, não fonte de conteúdo copiado.
- **Guidelines:** Google Cloud API Design Guide, Microsoft REST API Guidelines, Zalando RESTful Guidelines, AsyncAPI spec, CloudEvents spec (CNCF).
- **RFCs:** 9457 (Problem Details), 7396/6902 (JSON Patch), 8594 (Sunset).

## Plano de execução (ritmo B, igual System Design/Operação)

1. Criar `roadmap.md` do galho-pai; atualizar `index.md` existente.
2. Semear sub-galho a sub-galho, ordem 1→2→3→4. Cada subpasta: `index.md` + `roadmap.md` + notas via subagente-por-nota (**≤3/onda**, Sonnet, cada um lê o EXEMPLAR do System Design + este spec, WebSearch inline, barra de densidade explícita).
3. Ao fechar cada sub-galho: roadmap-folha + roadmap-pai + commit (paths explícitos, sem Co-Authored-By, push manual).
4. Fechamento: capstone; podar `API Design.md` pro que não migrou (preservar "Na prática" verbatim); callout em `Mensageria/*.md` apontando pra casa canônica; atualizar [[00-Meta/Roadmap]] item 10 ⬜→🟢; atualizar memória.

## Pontos em aberto (decidir durante a execução)

- **EXEMPLAR:** usar a nota 01 do System Design como referência de estrutura até a 1ª nota desta trilha virar o exemplar próprio.
- **Renumeração/contagem** por sub-galho pode ajustar no seeding (mesma tolerância das trilhas anteriores).
- **Destino final de `API Design.md`:** tronco podado (como System Design) — confirmar no fechamento se sobra conteúdo suficiente pra justificar manter o arquivo ou se vira redirect fino.
