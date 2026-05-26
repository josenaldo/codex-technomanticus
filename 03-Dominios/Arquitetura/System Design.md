---
title: "System Design"
created: 2026-04-01
updated: 2026-04-10
type: concept
status: evergreen
tags:
  - arquitetura
  - entrevista
publish: false
---

# System Design

A habilidade de projetar sistemas escaláveis, confiáveis e manuteníveis — e a skill mais avaliada em entrevistas de senior/staff. Não é sobre decorar arquiteturas, é sobre **demonstrar julgamento de engenharia**: saber fazer trade-offs, comunicar decisões, e adaptar o design a requisitos específicos.

## O que é

System Design é o processo de definir a **arquitetura**, **componentes**, **interfaces** e **fluxo de dados** de um sistema para atender requisitos funcionais e não-funcionais. Em entrevistas, é uma conversa de 45-60 minutos onde você projeta um sistema do zero.

O que diferencia um senior em system design:

1. **Começar pelos requisitos** — não pela solução. Dois sistemas de "chat" podem ter arquiteturas completamente diferentes dependendo da escala e dos requisitos.
2. **Fazer trade-offs explícitos** — toda decisão tem custo. Dizer "eu escolho X porque..." é o que demonstra senioridade.
3. **Conhecer os building blocks** — caching, sharding, message queues, load balancing — e saber quando cada um se aplica.
4. **Comunicar com clareza** — system design é uma conversa, não um monólogo. Validar premissas com o entrevistador é parte do processo.
5. **Dimensionar** — back-of-envelope math para justificar decisões de escala com números, não intuição.

---

## Framework de entrevista

### Fase 1 — Clarificar requisitos (5 min)

O erro mais comum é pular essa fase. Sem saber a escala, você pode over-engineer ou under-engineer.

**Requisitos funcionais** — o que o sistema faz:
- Quais são os core use cases? (máximo 3-4 para uma entrevista de 45 min)
- Quem são os atores? (usuário, admin, sistema externo)
- Quais operações são mais frequentes? (read-heavy? write-heavy? ambos?)

**Requisitos não-funcionais** — como o sistema se comporta:
- **Escala:** quantos usuários? quantos DAU (daily active users)?
- **Latência:** tempo de resposta aceitável? (< 200ms para API, < 1s para feed)
- **Disponibilidade:** 99.9%? 99.99%? (diferença: 8.7h vs 52min de downtime/ano)
- **Consistência:** strong consistency obrigatória? ou eventual consistency é aceitável?
- **Durabilidade:** perder dados é aceitável? (mensagens de chat vs analytics)

**Perguntas-chave para fazer ao entrevistador:**
- "Quantos usuários ativos por dia estamos esperando?"
- "Qual a proporção read/write?"
- "Precisamos de real-time ou near-real-time é suficiente?"
- "Quais são os requisitos de retenção de dados?"
- "O sistema precisa funcionar globalmente ou em uma região?"

### Fase 2 — Estimativas de escala (5 min)

Back-of-envelope math. Não precisa ser exato — precisa ser razoável e justificar decisões.

**Fórmulas práticas:**

```
QPS (queries per second):
  DAU × requests_por_dia / 86400 (segundos no dia)
  Peak QPS ≈ 2-5× média

Storage:
  tamanho_médio_por_registro × registros_por_dia × dias_de_retenção

Bandwidth:
  QPS × tamanho_médio_da_resposta

Memória para cache (regra 80/20):
  20% dos dados quentes × tamanho = memória necessária
```

**Exemplo — URL Shortener:**

```
100M URLs criadas/dia → ~1200 writes/s
Read:Write ratio 100:1 → ~120K reads/s

Storage por URL: ~500 bytes (short + long + metadata)
100M × 500B × 365 dias × 5 anos = ~91 TB

Cache: 20% das URLs geram 80% do tráfego
  20% × 100M = 20M URLs quentes × 500B ≈ 10 GB (cabe em RAM)
```

**Números de referência úteis:**

| Métrica | Valor |
| --- | --- |
| 1 dia | 86.400 segundos (~100K) |
| 1 mês | ~2.5M segundos |
| 1 ano | ~31.5M segundos |
| QPS → DAU | QPS × 86400 / requests_por_user |
| 1 char UTF-8 | 1-4 bytes |
| 1 tweet (140 chars) | ~300 bytes (com metadata) |
| 1 imagem (thumbnail) | ~30 KB |
| 1 imagem (HD) | ~500 KB |
| 1 minuto de vídeo (HD) | ~50 MB |

### Fase 3 — API Design (5 min)

Definir os endpoints principais. Mostra que você pensa em contrato antes de implementação.

```
POST /api/v1/urls
  Request:  { "long_url": "https://...", "custom_alias": "abc" }
  Response: { "short_url": "https://short.ly/abc", "expires_at": "..." }
  → 201 Created

GET /api/v1/{short_code}
  Response: 301 Redirect → long_url
  → 301 / 404

GET /api/v1/urls/{short_code}/stats
  Response: { "clicks": 1234, "created_at": "...", "top_countries": [...] }
  → 200 OK
```

**Pontos a mencionar:**
- Autenticação (API key, OAuth)
- Rate limiting (por user, por IP)
- Paginação para listagens
- Versionamento (path vs header)

→ Para aprofundar: [[API Design]]

### Fase 4 — Diagrama de alto nível (10 min)

O coração da entrevista. Desenhe a arquitetura com os componentes principais.

```
Clients (Web/Mobile)
    ↓
   DNS → CDN (assets estáticos)
    ↓
Load Balancer (L7)
    ↓
API Gateway (auth, rate limiting, routing)
    ↓
┌─────────────┬──────────────┐
│ Write Path  │  Read Path   │
│             │              │
│ App Server  │  App Server  │
│     ↓       │      ↓       │
│  Database   │    Cache     │
│  (primary)  │   (Redis)    │
│             │      ↓       │
│             │  Database    │
│             │  (replica)   │
└─────────────┴──────────────┘
        ↓
  Message Queue (async processing)
        ↓
  Workers (analytics, notifications, etc.)
```

**Regras práticas:**
- Separe read path de write path quando a proporção read/write for > 10:1
- Coloque cache no read path, não no write path (cache-aside é o padrão)
- Message queue para tudo que não precisa ser síncrono
- CDN para conteúdo estático e respostas cacheáveis

### Fase 5 — Deep dive (15-20 min)

Onde o entrevistador testa profundidade. Escolha 2-3 componentes mais complexos e aprofunde.

**Tópicos comuns de deep dive:**
- Database schema e indexação
- Caching strategy e invalidação
- Particionamento / sharding
- Consistência e resolução de conflitos
- Algoritmo de ranking / feed generation
- Real-time delivery (WebSocket, SSE, polling)
- Search indexing (Elasticsearch)
- File storage e upload handling

### Fase 6 — Trade-offs e evolução (5 min)

Demonstre que o design não é estático. Discuta:
- **Bottlenecks identificados** e como escalar
- **Single points of failure** e como eliminar
- **Monitoramento** — quais métricas acompanhar
- **Evolução** — como o design muda se a escala 10x

---

## Building blocks

Resumo dos componentes fundamentais. Cada um tem profundidade nas notas especializadas — aqui o foco é **quando usar** e **como combinar**.

### Escalabilidade

| Tipo | Como | Quando | Trade-off |
| --- | --- | --- | --- |
| Vertical (scale up) | Mais CPU/RAM na mesma máquina | Banco de dados, cache, quick wins | Tem teto; downtime para upgrade |
| Horizontal (scale out) | Mais máquinas | Stateless services, web servers | Requer load balancing; complexidade |

**Regra prática:** escale verticalmente primeiro (é mais simples), escale horizontalmente quando atingir o limite.

### Caching

Reduz latência e carga no backend armazenando dados frequentemente acessados em memória.

**Onde cachear:**

| Camada | Exemplo | Latência | Invalidação |
| --- | --- | --- | --- |
| Client-side | Browser cache, CDN | ~0ms | Cache-Control headers |
| Application | Redis, Memcached | ~1-5ms | TTL, event-based |
| Database | Query cache, materialized views | ~10ms | Automática (write invalida) |

**Estratégias:**

- **Cache-aside (lazy loading)** — app verifica cache → miss → lê do DB → popula cache. Mais comum.
- **Write-through** — app escreve no cache E no DB simultaneamente. Consistência forte, mas write mais lento.
- **Write-behind** — app escreve no cache → cache escreve no DB assincronamente. Rápido, mas risco de perda.
- **Read-through** — cache carrega do DB automaticamente no miss. Simplifica o código da app.

**Invalidação** (o problema mais difícil):
- **TTL** — simples, mas dados podem ficar stale
- **Event-based** — publish evento no write → consumer invalida cache. Consistente, mas complexo.
- **Versioned keys** — `user:42:v3` → nova versão = nova key. Sem delete, mas consome memória.

→ Para aprofundar caching HTTP: [[Redes e Protocolos]]

### Database choices

| Tipo | Exemplo | Quando usar |
| --- | --- | --- |
| SQL relacional | PostgreSQL, MySQL | Transações ACID, queries complexas, dados estruturados |
| Document store | MongoDB, DynamoDB | Schema flexível, dados hierárquicos, escala horizontal |
| Key-Value | Redis, Memcached | Cache, sessões, contadores, dados efêmeros |
| Wide-column | Cassandra, HBase | Write-heavy, time-series, escala massiva |
| Graph | Neo4j, Amazon Neptune | Relacionamentos complexos (social graphs, recomendações) |
| Search engine | Elasticsearch, Solr | Full-text search, analytics, logs |
| Time-series | InfluxDB, TimescaleDB | Métricas, IoT, dados temporais |

**Decisões comuns em entrevista:**
- **SQL vs NoSQL:** se precisa de transações ACID e queries JOIN → SQL. Se precisa de escala horizontal e schema flexível → NoSQL.
- **Sharding:** por hash (distribuição uniforme) ou por range (queries de range). Escolha a shard key com cuidado — redistribuir depois é doloroso.
- **Replication:** primary-replica para separar reads de writes. Multi-primary para escrita distribuída (mais complexo, risco de conflitos).

→ Para aprofundar: [[Banco de dados]]

### Message queues e processamento assíncrono

Desacoplam produtores de consumidores. Fundamentais para resiliência e escalabilidade.

**Quando usar:**
- Processamento que não precisa de resposta imediata (emails, notificações, analytics)
- Absorver picos de tráfego (buffer entre API e workers)
- Desacoplar serviços (serviço A não precisa conhecer serviço B)
- Garantir que trabalho não se perde (persistência da fila)

**Escolha:**

| Ferramenta | Quando |
| --- | --- |
| Kafka | Alto throughput, event streaming, replay, ordering por partição |
| RabbitMQ | Routing flexível, filas com prioridade, task queues |
| SQS | Managed, simples, integrado com AWS |
| BullMQ | Node.js, job queues com retry, cron jobs |

→ Para aprofundar: [[03-Dominios/Arquitetura/Mensageria/Kafka]], [[RabbitMQ]], [[BullMQ]]

### Consistência e CAP Theorem

**CAP:** em um sistema distribuído com partição de rede (P é inevitável), escolha:
- **CP** — consistência forte, aceita indisponibilidade durante partições (ex.: ZooKeeper, bancos tradicionais)
- **AP** — disponibilidade total, aceita inconsistência temporária (ex.: Cassandra, DynamoDB)

**Na prática:**
- Operações financeiras, agendamentos, inventário → **strong consistency** (não pode vender o mesmo item duas vezes)
- Feeds, likes, analytics, notificações → **eventual consistency** (OK se o like aparecer 2 segundos depois)

**Padrões de consistência:**
- **Read-your-writes** — após escrever, o mesmo usuário vê o dado atualizado (read do primary)
- **Monotonic reads** — uma vez que o usuário viu versão N, nunca vê versão < N
- **Quorum** — W + R > N garante overlap entre quem escreveu e quem lê (Dynamo-style)

→ Para aprofundar: [[Banco de dados]] (ACID, isolamento)

---

## Padrões arquiteturais recorrentes

Patterns que aparecem em múltiplos system designs. Reconhecê-los acelera a entrevista.

### Pub/Sub (Publish-Subscribe)

Produtores publicam eventos em tópicos; consumidores se inscrevem nos tópicos que interessam. Nenhum lado conhece o outro.

```
Service A → Topic "order.created" → Service B (notification)
                                  → Service C (analytics)
                                  → Service D (inventory)
```

**Quando usar:** notificações, event-driven architecture, fan-out de eventos.
**Ferramentas:** Kafka, Redis Pub/Sub, AWS SNS, Google Pub/Sub.

### CQRS (Command Query Responsibility Segregation)

Separa modelo de escrita (commands) do modelo de leitura (queries). Cada um pode ter schema, banco, e escala diferentes.

```
Write → Command Model (normalizado, SQL) → Event publicado
                                              ↓
Read  ← Query Model (desnormalizado, Redis/Elasticsearch) ← Consumer atualiza
```

**Quando usar:** read:write ratio muito alta; queries complexas que não performam no modelo normalizado; diferentes views dos mesmos dados.

**Trade-off:** complexidade de manter dois modelos sincronizados. Eventual consistency entre write e read model.

### Event Sourcing

Ao invés de salvar o estado atual, salva **todos os eventos** que levaram ao estado. O estado é derivado reproduzindo os eventos.

```
Eventos: [AccountCreated, Deposited(100), Withdrawn(30), Deposited(50)]
Estado atual: balance = 120
```

**Quando usar:** auditoria obrigatória, undo/redo, debug de "como chegou nesse estado", sistemas financeiros.

**Trade-off:** complexidade alta, replay pode ficar lento (snapshots ajudam), difícil de consultar diretamente (precisa de projeção/CQRS).

→ Para aprofundar: [[Event Storming]]

### Sharding strategies

**Hash-based:** `shard = hash(key) % num_shards`. Distribuição uniforme, mas perde queries de range.

**Range-based:** `shard_1: A-M, shard_2: N-Z`. Queries de range funcionam, mas hotspots se a distribuição não for uniforme.

**Directory-based:** lookup table que mapeia key → shard. Flexível, mas o diretório é SPOF e bottleneck.

**Consistent hashing:** ring de hash onde cada servidor ocupa um arco. Adicionar/remover servidor redistribui mínimo de dados. Usado por Cassandra, DynamoDB, memcached.

### Rate Limiting

Protege o sistema contra abuse e garante fairness.

**Algoritmos:**

| Algoritmo | Como funciona | Prós | Contras |
| --- | --- | --- | --- |
| Token Bucket | Tokens regeneram a taxa fixa; cada request consome 1 | Permite bursts controlados | Mais complexo de implementar distribuído |
| Sliding Window Log | Log de timestamps; conta requests na janela | Preciso | Memória alta (guarda cada timestamp) |
| Sliding Window Counter | Combina fixed window com peso proporcional | Bom balanço memória/precisão | Aproximação, não exato |
| Fixed Window | Conta por janela fixa (ex.: 100 req/min) | Simples | Burst na fronteira de janelas |

**Implementação distribuída:** Redis (`INCR` + `EXPIRE`), ou API Gateway (Kong, AWS API Gateway).

→ Para aprofundar: [[Redes e Protocolos]] (rate limiting, retries, circuit breaker)

### Circuit Breaker

Quando um serviço downstream falha, parar de chamá-lo temporariamente para:
1. Não sobrecarregar o serviço que já está com problemas
2. Não consumir threads/conexões esperando timeout
3. Falhar rápido e dar uma resposta degradada

```
CLOSED (normal) → falhas > threshold → OPEN (rejeita tudo)
                                          ↓ (após cooldown)
                                       HALF-OPEN (testa uma)
                                          ↓ (sucesso)
                                       CLOSED
```

**Ferramentas:** Resilience4j (Java), Polly (.NET), opossum (Node.js), custom com Redis.

### API Gateway

Ponto de entrada único para clientes. Centraliza cross-cutting concerns:

- **Autenticação/autorização** — valida token antes de chegar ao service
- **Rate limiting** — por user, por API key, por IP
- **Routing** — direciona para o microserviço correto
- **Request/response transformation** — adapta formato
- **Caching** — cacheia respostas de endpoints idempotentes
- **Load balancing** — distribui entre instâncias
- **Observabilidade** — logging, tracing, métricas centralizados

**Ferramentas:** Kong, AWS API Gateway, Nginx, Envoy, Spring Cloud Gateway.

→ Para aprofundar: [[API Design]], [[Arquitetura de Software]]

---

## Walkthroughs: sistemas clássicos de entrevista

Cada walkthrough segue o framework: requisitos → estimativas → API → diagrama → deep dive → trade-offs.

### 1. URL Shortener (ex.: bit.ly)

**Requisitos:**
- Criar short URL a partir de long URL
- Redirecionar short URL → long URL
- Analytics opcionais (clicks, geolocation)
- URLs expiram (TTL configurável)
- Scale: 100M URLs/dia, read:write 100:1

**Estimativas:**
- Write: ~1200/s, Read: ~120K/s
- Storage (5 anos): ~91 TB
- Cache: 10 GB (20% quentes)

**Arquitetura:**

```
Client → LB → API Server → Cache (Redis)
                    ↓              ↓ miss
              URL Generator    Database (key-value)
                    ↓
            Base62 Encoder
```

**Deep dive — geração de short code:**

| Abordagem | Prós | Contras |
| --- | --- | --- |
| Hash (MD5/SHA) + truncar | Sem coordenação | Colisão possível; precisa verificar |
| Counter + Base62 | Sem colisão, previsível | Sequencial (previsível = security concern); counter é SPOF |
| Pre-generated IDs (range) | Sem colisão, distribuído | Complexidade de gerenciar ranges; desperdício |
| Snowflake-style | Distribuído, ordenado, único | 64-bit → short code mais longo |

**Decisão recomendada:** counter distribuído (Zookeeper ou Redis INCR) + Base62. Cada server pega um range (ex.: 1M IDs por vez) e gera localmente. Sem colisão, sem coordenação por request.

**Redirect: 301 vs 302:**
- **301 (Moved Permanently)** — browser cacheia, menos carga no servidor, mas perde analytics
- **302 (Found)** — browser não cacheia, toda request passa pelo servidor, permite analytics

**Trade-offs finais:**
- Custom alias: verificar unicidade → DB lookup + cache
- Expiração: cron job para cleanup ou lazy deletion (verifica TTL no read)
- Analytics: async via Kafka → analytics worker (não bloqueia redirect)

---

### 2. News Feed / Timeline (ex.: Twitter, Instagram)

**Requisitos:**
- Postar conteúdo (texto, imagens)
- Ver feed personalizado (posts de quem você segue)
- Scale: 500M DAU, 10 posts/dia por user, feed de 200 posts

**O problema central: Fan-out**

Quando um user posta, como entregar para todos os seguidores?

| Estratégia | Como funciona | Prós | Contras |
| --- | --- | --- | --- |
| Fan-out on Write (push) | No momento do post, escreve na timeline cache de cada follower | Read rápido (feed pré-computado) | Write lento para celebridades (milhões de followers); desperdício se follower não abre o app |
| Fan-out on Read (pull) | No momento do read, consulta posts de todos que o user segue | Write rápido, sem desperdício | Read lento (merge de N fontes); latência alta |
| Híbrido | Push para users normais; pull para celebridades | Melhor de ambos | Complexidade |

**Decisão recomendada:** híbrido. A maioria dos users tem < 1000 followers → fan-out on write. Celebridades (> 10K followers) → fan-out on read, mesclado no momento da leitura.

**Arquitetura:**

```
Post Service → Fanout Service → Timeline Cache (Redis, por user)
     ↓                                    ↑
  Post DB (append-only)          Feed Service → merge com celebridades
     ↓                                    ↓
  Media Service (S3)              Client (paginado, cursor-based)
     ↓
  Notification Service (async)
```

**Deep dive — ranking:**
- Cronológico é simples mas não engajador
- ML-based: score = f(relevância, recência, engagement, relação com autor)
- Feature store para features de ranking em tempo real
- A/B testing para calibrar o modelo

**Trade-offs:**
- Timeline cache tem tamanho fixo (últimos 800 posts) — scroll infinito busca de histórico
- Eventual consistency: post pode levar segundos para aparecer no feed dos followers
- Delete/edit: precisa propagar para todos os caches (fan-out reverso)

---

### 3. Chat System (ex.: WhatsApp, Slack)

**Requisitos:**
- Mensagens 1:1 e em grupo
- Indicador de online/offline (presence)
- Confirmação de entrega/leitura
- Histórico de mensagens
- Scale: 50M DAU, 40 mensagens/dia por user

**Protocolo de comunicação:**

- **WebSocket** — conexão bidirecional persistente. Ideal para chat.
- **HTTP long polling** — fallback quando WebSocket não é possível.
- Cada user mantém uma conexão WebSocket com um Chat Server.

**Arquitetura:**

```
Client A ↔ WebSocket ↔ Chat Server 1 → Message Queue → Chat Server 2 ↔ WebSocket ↔ Client B
                            ↓                                ↓
                       Message DB (Cassandra)          Push Notification
                            ↓                          (se offline)
                       Message ID Generator
                       (Snowflake)
```

**Deep dive — ordenação de mensagens:**

Problema: em sistema distribuído, relógio de máquinas diferentes divergem. `timestamp` não garante ordem global.

Soluções:
- **Snowflake ID** — timestamp de 41 bits + machine ID + sequence. Ordenável, monotônico dentro de um servidor.
- **Lamport timestamp** — relógio lógico que garante causalidade.
- **Na prática:** Snowflake por conversa é suficiente (mensagens numa conversa passam pelo mesmo partition).

**Deep dive — presence (online/offline):**
- Heartbeat a cada 30s do client para o Presence Service
- Sem heartbeat por 90s → marcar offline
- Fan-out de status para contatos (pub/sub com Redis)
- Para grupos grandes: lazy check (consulta status só quando o user abre a conversa)

**Escolha de banco:**
- **Cassandra** ou **HBase** — write-heavy, append-only, partition por `(conversation_id)`, clustering por `(message_id DESC)`
- Não SQL relacional — escala de writes e modelo de dados (time-series) favorece wide-column

**Trade-offs:**
- End-to-end encryption: servidor não lê o conteúdo → não pode fazer search server-side
- Grupo grande (1000+ membros): fan-out de mensagem fica caro → message queue + async delivery
- Media (imagens, vídeo): upload para object storage (S3) → envia URL na mensagem

---

### 4. Rate Limiter

**Requisitos:**
- Limitar requests por user/IP/API key
- Configurável por endpoint (ex.: 100/min para search, 1000/min para feed)
- Distribuído (múltiplos servidores compartilham contagem)
- Baixa latência (< 1ms overhead)
- Resposta clara quando limitado (429 + Retry-After header)

**Onde colocar:**

| Local | Prós | Contras |
| --- | --- | --- |
| API Gateway | Centralizado, fácil de configurar | Menos flexível por endpoint |
| Middleware na app | Granular, contexto do request | Cada serviço implementa |
| Sidecar (service mesh) | Transparente para a app | Infraestrutura mais complexa |

**Algoritmo recomendado: Sliding Window Counter**

```
window_key = "rate:{user_id}:{endpoint}:{current_minute}"
count = Redis.INCR(window_key)
Redis.EXPIRE(window_key, 60)

# Peso proporcional da janela anterior
prev_count = Redis.GET(prev_window_key) || 0
weighted = prev_count * (1 - elapsed/60) + count

if weighted > limit:
  return 429 + Retry-After header
```

**Headers de resposta:**
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 23
X-RateLimit-Reset: 1618884474
Retry-After: 37
```

**Arquitetura distribuída:**
- Redis cluster como armazenamento central de contadores
- Cada API server consulta Redis antes de processar
- Race condition: `INCR` é atômico no Redis → sem problema
- Se Redis estiver indisponível: fail-open (permitir) é mais seguro que fail-closed (bloquear tudo)

**Trade-offs:**
- Rate limiting por IP não funciona bem com NAT (muitos users atrás do mesmo IP)
- Per-user requer autenticação antes do rate limiting
- Rate limiting global (todo o cluster) vs local (por instância): global é mais preciso, local é mais rápido

---

### 5. Notification System

**Requisitos:**
- Multi-canal: push notification, SMS, email
- Templates com variáveis
- Prioridade (urgente vs batch)
- Rate limiting por user (não spam)
- Tracking de delivery e open rate
- Scale: 10M notificações/dia

**Arquitetura:**

```
Trigger Service → Notification Service → Priority Queue (Kafka/RabbitMQ)
                        ↓                        ↓
                  Template Engine          ┌──────┼──────┐
                        ↓                  ↓      ↓      ↓
                  User Preferences    Push    SMS    Email
                  (opt-in/out)        (FCM/   (Twilio) (SES/
                                     APNs)            SendGrid)
                                          ↓
                                    Delivery Tracker
                                    (status, retry, analytics)
```

**Deep dive — reliability:**
- **Retry com backoff** — cada provider pode falhar. Retry 3x com exponential backoff.
- **Dead letter queue** — após N retries, mover para DLQ para investigação manual.
- **Idempotency** — notification_id garante que não envia duplicado no retry.
- **Rate limiting por user** — máximo N notificações por dia. Agrupar se necessário (digest).

**Deep dive — prioridade:**
- Fila separada por prioridade: `urgent` (processada imediatamente) vs `normal` (batch a cada minuto) vs `digest` (agrupada diariamente).
- Workers dedicados por prioridade para garantir que batch não bloqueia urgent.

**Trade-offs:**
- Push notification de terceiros (FCM/APNs) não garante entrega — fallback para outro canal
- Email em massa: warm up de IP, SPF/DKIM/DMARC, bounce handling
- Timezone-aware: notificação de marketing às 3am é opt-out automático

---

### 6. Distributed File Storage (ex.: Google Drive, Dropbox)

**Requisitos:**
- Upload/download de arquivos (até 10 GB)
- Sincronização entre dispositivos
- Versionamento (histórico de versões)
- Compartilhamento com permissões
- Scale: 50M users, 2 GB média por user

**Arquitetura:**

```
Client (Desktop/Mobile/Web)
    ↓
Block Service → divide arquivo em chunks (4 MB)
    ↓               ↓
Metadata DB    Object Storage (S3)
(PostgreSQL)   (chunks com content-hash)
    ↓
Sync Service → WebSocket/long-poll → notifica outros devices
    ↓
Notification Service
```

**Deep dive — chunking e deduplication:**
- Arquivo dividido em blocos de 4 MB
- Cada bloco: `hash = SHA256(content)` → usado como key no storage
- **Deduplication:** se dois users uploadam o mesmo arquivo, os chunks são idênticos → armazena uma vez
- **Delta sync:** ao modificar um arquivo, só os chunks alterados são re-uploadados (como rsync)

**Deep dive — conflitos:**
- Dois dispositivos editam o mesmo arquivo offline → conflito no sync
- Estratégias: last-write-wins (simples, perde dados) vs merge (complexo) vs fork (salvar ambas versões, user resolve)
- Dropbox approach: mantém ambas versões com sufixo "(conflicted copy)"

**Escolha de storage:**
- **Metadata:** SQL (PostgreSQL) — precisa de transações, queries complexas (permissões, versões)
- **Chunks:** Object storage (S3) — barato, durável (99.999999999%), escala infinita
- **Cache:** Redis para metadata quente (quem tem acesso, versão atual)

**Trade-offs:**
- Upload de arquivo grande: multipart upload com resume capability
- Bandwidth: compressão antes do upload economiza banda mas custa CPU no client
- Encryption: at-rest (server-side) vs end-to-end (client-side) — E2E impede dedup server-side

---

### 7. Web Crawler (ex.: Googlebot)

**Requisitos:**
- Crawliar bilhões de páginas
- Respeitar robots.txt e politeness (não sobrecarregar sites)
- Detectar conteúdo duplicado
- Priorizar páginas importantes
- Scale: 1B páginas/mês (~400 páginas/segundo)

**Arquitetura:**

```
Seed URLs → URL Frontier (priority queue)
                ↓
           DNS Resolver (cache local)
                ↓
           Fetcher (respeita robots.txt, rate limit por domínio)
                ↓
           Content Parser (extrai texto, links, metadata)
                ↓
        ┌───────┼───────┐
        ↓       ↓       ↓
   Duplicate   URL      Content
   Detector   Filter    Store
   (SimHash)  (Bloom    (S3 + Elasticsearch)
              Filter)
                ↓
           URL Frontier (novos URLs)
```

**Deep dive — URL Frontier:**
- Não é uma fila simples — é uma **priority queue com politeness**
- **Prioridade:** PageRank, freshness, mudança frequente → crawl mais seguido
- **Politeness:** no máximo 1 request por segundo por domínio → fila separada por domínio
- Implementação: front queue (prioridade) → back queue (por domínio, com delay)

**Deep dive — deduplication:**
- **URL dedup:** Bloom Filter — probabilístico, mas usa pouca memória. 1B URLs × 10 bits ≈ 1.2 GB
- **Content dedup:** SimHash — fingerprint que permite comparação fuzzy (detecta páginas quase idênticas)
- URLs diferentes podem ter conteúdo idêntico (www vs non-www, trailing slash, query params)

**Trade-offs:**
- BFS vs DFS: BFS é mais justo (não fica preso em um site), DFS é melhor para descobrir site inteiro
- Politeness vs velocidade: ser educado = crawl mais lento, mas evita ser bloqueado
- Freshness: recrawl frequency baseada em rate of change (homepage = frequente, about page = rara)
- Trap detection: sites infinitos (calendários, session IDs na URL) → limitar profundidade e URLs por domínio

---

### 8. Key-Value Store distribuído (ex.: DynamoDB, Redis Cluster)

**Requisitos:**
- put(key, value) / get(key)
- Alta disponibilidade (AP do CAP)
- Escalável horizontalmente
- Latência < 10ms (p99)
- Tuneable consistency

**Arquitetura — estilo Dynamo:**

```
Client → Coordinator Node (qualquer nó pode coordenar)
              ↓
         Consistent Hash Ring → identifica N nós responsáveis
              ↓
         Replication: escreve em N nós (W = quorum de escrita)
              ↓
         Read: lê de R nós (R = quorum de leitura)

         W + R > N → strong consistency
         W=1, R=1  → eventual consistency (rápido)
```

**Deep dive — consistent hashing:**
- Ring de hash (0 a 2^128)
- Cada nó mapeia para múltiplos pontos no ring (virtual nodes)
- Key é hasheada → percorre ring clockwise → primeiros N nós são responsáveis
- Adicionar nó: redistribui ~1/N dos dados (não todos)

**Deep dive — conflict resolution:**
- Writes concorrentes ao mesmo key em nós diferentes → conflito
- **Vector clocks** — detecta causalidade (A happened-before B vs concurrent)
- **Last-write-wins (LWW)** — simples, mas perde dados
- **Application-level merge** — DynamoDB retorna todos os valores conflitantes, app decide (ex.: union de sets)

**Deep dive — failure detection:**
- **Gossip protocol** — nós trocam informações periodicamente sobre o estado do cluster
- Nó que não responde gossip por N rounds → marcado como suspeito → depois morto
- **Hinted handoff** — se nó responsável está down, outro nó temporariamente assume e entrega quando o nó volta

**Trade-offs:**
- Consistency vs latency: quorum mais alto = mais consistente, mais lento
- Replication factor: N=3 é padrão (tolera 1 falha com quorum). N=5 para dados críticos.
- Compaction: LSM-tree (write-optimized) vs B-tree (read-optimized)

---

## Problemas comuns em produção (cross-stack)

Em entrevistas, é frequente o entrevistador perguntar: "você já enfrentou esse problema em produção? como resolveu?" A tabela abaixo mapeia problemas recorrentes e as ferramentas/abordagens por stack. Cada stack tem uma nota dedicada com detalhes.

### Mapeamento problema → solução por stack

| Problema | Java / Spring Boot | Node.js / Express | Python / Django | Go |
| --- | --- | --- | --- | --- |
| **Connection pool exausto** | HikariCP config (max pool, leak detection) | knex/TypeORM pool config; `pg-pool` | Django `CONN_MAX_AGE`; `django-db-connection-pool` | `sql.DB` SetMaxOpenConns, SetMaxIdleConns |
| **N+1 queries** | JPA `@EntityGraph`, `JOIN FETCH`, Hibernate batch fetch | DataLoader pattern; eager loading no ORM | `select_related()`, `prefetch_related()` | sqlc/GORM `Preload()`, query manual com JOIN |
| **Slow queries** | `EXPLAIN ANALYZE`, Spring Data `@Query` nativa, índices | `EXPLAIN` + query raw; knex query builder | Django Debug Toolbar, `raw()`, índices | `EXPLAIN` + sqlc, pgx para queries otimizadas |
| **Memory leak** | Heap dump + MAT/VisualVM; G1GC tuning | `--inspect` + Chrome DevTools; heapdump | tracemalloc, objgraph, memory_profiler | pprof (`go tool pprof`) |
| **Thread/goroutine exhaustion** | Thread pool config, `@Async` + virtual threads (Java 21+) | Event loop blocking → worker threads, clustering | Gunicorn workers, `asyncio`, Celery para background | Goroutine leak detection com pprof; context cancelation |
| **API timeout cascading** | Resilience4j (circuit breaker, bulkhead, retry) | opossum circuit breaker; `axios` timeout + retry | django-circuitbreaker; requests timeout | `context.WithTimeout`, custom circuit breaker |
| **Cache stampede** | Cache lock (Redisson), probabilistic early expiration | Redlock, `cache-manager` stale-while-revalidate | django-cacheops, cache lock pattern | singleflight (`golang.org/x/sync/singleflight`) |
| **Distributed tracing** | Spring Cloud Sleuth / Micrometer + Zipkin/Jaeger | OpenTelemetry SDK, `cls-hooked` para context | django-opentelemetry, ddtrace | OpenTelemetry Go SDK, native context propagation |
| **Graceful shutdown** | Spring Boot lifecycle hooks, `@PreDestroy` | `process.on('SIGTERM')`, drain connections | Gunicorn graceful worker restart, Django signals | `signal.Notify` + `http.Server.Shutdown()` |
| **Database migration** | Flyway, Liquibase | knex migrations, Prisma migrate | Django migrations (built-in) | golang-migrate, goose |

→ Para deep dive em Java/Spring Boot: [[Spring Boot]] (seção Troubleshooting)
→ Para deep dive em Node.js: [[Node.js]]

---

## Armadilhas comuns

- **Pular clarificação de requisitos** — sem saber a escala, você pode projetar um sistema de chat para 1000 users como se fosse o WhatsApp. Sempre pergunte.
- **Projetar para Google-scale imediatamente** — a maioria dos sistemas não precisa de sharding no dia 1. Comece com um banco, escale quando necessário. O entrevistador quer ver que você sabe **quando** escalar, não que você escala tudo por default.
- **Não falar sobre trade-offs** — todo design tem compromissos. "Eu escolho Redis porque é rápido" não é suficiente. "Eu escolho Redis para cache porque nosso read:write ratio é 100:1 e os dados cabe em memória, mas o trade-off é que perdemos dados se o cluster reiniciar, então mantemos o banco como source of truth" — isso é senioridade.
- **Ignorar requisitos não-funcionais** — disponibilidade, latência, consistência são tão importantes quanto features. Um chat que é 99.9% available mas perde mensagens é pior que um que é 99% available mas nunca perde.
- **Monólogo** — system design é uma conversa. Pergunte ao entrevistador, valide premissas, peça feedback. "Estou pensando em usar Cassandra aqui por causa do volume de writes. O que você acha?" mostra colaboração.
- **Ficar no abstrato** — "eu usaria um cache" não impressiona. "Eu usaria Redis com cache-aside, TTL de 5 minutos, e invalidação event-based via Kafka quando o dado muda" — isso impressiona.
- **Não fazer back-of-envelope math** — números justificam decisões. "Precisamos de sharding" vs "temos 120K QPS, um PostgreSQL aguenta ~10K QPS com esse schema, então precisamos de ~12 shards" — o segundo mostra capacidade analítica.
- **Esquecer de monitoramento e observabilidade** — mencionar métricas, alertas, dashboards mostra que você pensa em operar o sistema, não só projetar. "Eu monitoraria p99 latency, cache hit ratio, e queue depth."

---

## Na prática (da minha experiência)

> No MedEspecialista, projetei a evolução de um monolito para uma arquitetura orientada a serviços. Algumas decisões de design que ilustram os conceitos desta nota:
>
> **Separação read/write no agendamento:** O core de agendamentos usa PostgreSQL com **strong consistency** — não pode haver double-booking. Mas a listagem de horários disponíveis (read-heavy, tolerante a dados de segundos atrás) usa um **cache Redis com TTL de 5 minutos** populado por eventos Kafka. Quando um agendamento é confirmado, o serviço publica um evento que invalida o cache. CQRS na prática.
>
> **Fan-out de notificações:** Quando um médico confirma uma consulta, o sistema precisa notificar o paciente (push + SMS), atualizar o dashboard admin (SSE), e registrar para faturamento. Isso é um caso clássico de pub/sub: o Agendamento Service publica `consulta.confirmada`, e cada consumer (Notification, Dashboard, Billing) processa de forma independente. Se o serviço de SMS estiver fora, as outras notificações continuam funcionando.
>
> **Rate limiting na API pública:** A API que os parceiros (planos de saúde) consomem tem rate limiting por API key (1000 req/min) implementado no API Gateway (Kong). Isso protege o sistema contra integrations com bugs que bombardeiam a API, sem afetar o app mobile dos pacientes.
>
> **A lição principal:** o design perfeito no quadro branco nunca sobrevive ao contato com produção. O que importa é que a arquitetura seja **adaptável** — que você consiga mudar componentes sem reescrever tudo. Bounded contexts claros e comunicação assíncrona entre serviços tornam isso possível.

---

## How to explain in English

> "In system design interviews, I follow a structured approach that I've refined through both interviews and real production experience. I start by clarifying requirements — both functional and non-functional — because the scale and constraints drive every subsequent decision. I always do back-of-envelope math to justify my choices with numbers rather than intuition.
>
> For example, if asked to design a URL shortener, I'd first establish the scale: 100 million URLs per day means roughly 1,200 writes per second, and with a 100:1 read-to-write ratio, that's 120,000 reads per second. That tells me I definitely need caching for reads, but a single well-configured database can handle the writes. I'd use consistent hashing for the short code generation to avoid coordination between servers.
>
> What I focus on most is trade-offs. Every decision has a cost: choosing eventual consistency for a feed means faster reads but users might see stale data for a few seconds. Choosing strong consistency for a booking system means slightly higher latency but no double-bookings. The ability to articulate these trade-offs and choose appropriately for the context is what separates a senior engineer from someone who just memorized architectures.
>
> In my experience building production systems, I've learned three things: first, start simple and scale incrementally — a well-designed monolith with clear boundaries handles surprising scale. Second, separate your read and write paths early, because they almost always need to scale differently. Third, make everything async that doesn't need an immediate response — message queues are the most underrated tool in system design."

### Frases úteis em entrevista

- "Let me start by clarifying the requirements and establishing the scale we're designing for."
- "With 120K reads per second, we definitely need a caching layer — let me walk through the caching strategy."
- "The trade-off here is consistency versus availability. For this use case, I'd choose eventual consistency because..."
- "I'd separate the read path from the write path since the ratio is heavily read-dominant."
- "This is a great candidate for async processing via a message queue — the user doesn't need an immediate response."
- "Let me do some quick math: 100M daily active users, 10 requests per day, that's roughly 12,000 QPS at steady state, maybe 30-40K at peak."
- "I'd use consistent hashing here so we can add nodes without redistributing all the data."
- "For the database, I'd start with PostgreSQL. It can handle 10K QPS with proper indexing, and we can shard later if needed."
- "We need a circuit breaker on this downstream call to prevent cascading failures."
- "I'd monitor three key metrics: p99 latency, cache hit ratio, and queue depth."

### Key vocabulary

- projeto de sistema → system design
- escalabilidade horizontal → horizontal scaling / scale out
- balanceamento de carga → load balancing
- fragmentação de dados → sharding / data partitioning
- replicação → replication
- consistência eventual → eventual consistency
- consistência forte → strong consistency
- taxa de requisições → requests per second (RPS) / queries per second (QPS)
- ponto único de falha → single point of failure (SPOF)
- tolerância a falhas → fault tolerance
- throughput → throughput (volume processado por unidade de tempo)
- latência → latency (tempo de resposta)
- fanout → fan-out (distribuição para múltiplos destinatários)
- fila de mensagens → message queue
- disjuntor → circuit breaker
- cache distribuído → distributed cache
- particionamento consistente → consistent hashing
- conta de guardanapo → back-of-envelope calculation
- requisitos não-funcionais → non-functional requirements (NFRs)
- acordo de nível de serviço → service level agreement (SLA)
- observabilidade → observability
- rastreamento distribuído → distributed tracing

---

## Recursos

### Livros

- *Designing Data-Intensive Applications* — Martin Kleppmann (o livro essencial; cobre tudo de replicação a consistência)
- *System Design Interview Vol. 1 & 2* — Alex Xu (walkthroughs práticos, excelente para entrevistas)
- *Building Microservices* — Sam Newman (patterns de decomposição e comunicação)
- *Database Internals* — Alex Petrov (para quem quer entender o "como" por trás de bancos distribuídos)

### Online

- [System Design Primer (GitHub)](https://github.com/donnemartin/system-design-primer) — referência completa e gratuita
- [ByteByteGo](https://bytebytego.com/) — Alex Xu, diagramas visuais excelentes
- [Martin Fowler's blog](https://martinfowler.com/) — CQRS, Event Sourcing, microservices patterns
- [Architectural Katas](https://www.architecturalkatas.com/) — exercícios práticos de design
- [High Scalability](http://highscalability.com/) — case studies de arquiteturas reais

### Vídeos

> [!info] SYSTEM DESIGN: ALÉM DA ENTREVISTA
> [https://www.youtube.com/live/-8tdjn30SSw?si=kcvd_nTLIYMNIrM6](https://www.youtube.com/live/-8tdjn30SSw?si=kcvd_nTLIYMNIrM6)

> [!info] 18 System Design Concepts Every Engineer Must Know
> [https://www.designgurus.io/blog/system-design-interview-fundamentals](https://www.designgurus.io/blog/system-design-interview-fundamentals)

---

## Veja também

- [[API Design]] — design de APIs REST, GraphQL, gRPC
- [[Banco de dados]] — SQL, NoSQL, ACID, indexação, replicação, sharding
- [[Redes e Protocolos]] — TCP/UDP, DNS, HTTP, WebSocket, load balancing, CDN, caching HTTP
- [[03-Dominios/Arquitetura/Mensageria/Kafka]] — event streaming, partições, consumers
- [[RabbitMQ]] — message queuing, routing, dead letter queues
- [[Arquitetura de Software]] — patterns arquiteturais, microserviços, monolito
- [[Event Storming]] — event sourcing, domain events
- [[Spring Boot]] — troubleshooting Java em produção
- [[System Design Practice]] — exercícios práticos
