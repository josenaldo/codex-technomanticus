---
title: "Roadmap — Building blocks"
created: 2026-07-07
type: meta
publish: false
tags:
  - meta
  - roadmap
  - system-design
---

# Roadmap — Building blocks (sub-galho 2)

Roadmap-folha do sub-galho `System Design/2 - Building blocks`. Fase **Adepto** (piso ≥400 linhas; alvo de densidade ~440-540). Spec: [[00-Meta/specs/2026-07-06-system-design-trilha-design]]. EXEMPLAR do galho: [[1 - Framework de entrevista/01 - O que é System Design e o que a entrevista avalia]].

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 7 |
| ⬜ pendente | 0 |
| ✅ feita | 7 |
| 🔄 em andamento | 0 |
| % concluído | 100% ✅ |

---

## Notas

#### 01 - Escalabilidade e load balancing   [substantivo]
- **Estado:** ✅ feita (2026-07-07) · fase: Adepto
- **Escopo:** vertical vs horizontal, stateless, L4 vs L7, health checks, sticky sessions, algoritmos de balanceamento (round-robin/least-conn/hashing).
- **Fronteira:** linka [[Redes e Protocolos]]; não duplica o detalhe de TCP/HTTP.
- **Fontes:** AWS ELB docs (ALB/NLB); Alex Xu Vol.1 cap.2; Hello Interview; System Design Primer.
- **Resultado:** 283 linhas / 5087 palavras; 3 Mermaid, 2 [!warning], 3 [!question]-. Consistent hashing só citado (aponta →04). Verificado: [[Redes e Protocolos]] resolve via index; links-irmãos ok; URLs datadas "consultado em 2026-07".

#### 02 - Caching   [substantivo]
- **Estado:** ✅ feita (2026-07-07) · fase: Adepto
- **Escopo:** cache-aside / write-through / write-back / read-through, TTL, eviction (LRU/LFU/maxmemory-policy), cache stampede e mitigação (lock, early/probabilistic expiration, coalescing), invalidação, hit ratio, hot keys.
- **Fronteira:** linka Redis; usa como bloco, não reescreve o detalhe de Redis. CDN aponta →07.
- **Fontes:** redis.io/docs; antirez.com (stampede); AWS whitepaper; Alex Xu Vol.1; System Design Primer.
- **Resultado:** 421 linhas / 7487 palavras; 6 Mermaid, 4 [!warning], 5 [!question]-. Ressalva checada: Redis OSS default `noeviction`, mas ElastiCache sobrescreve p/ `volatile-lru`. Verificado: links-irmãos e URLs ok.

#### 03 - Bancos de dados em escala - SQL vs NoSQL e replicação   [substantivo]
- **Estado:** ✅ feita (2026-07-07) · fase: Adepto
- **Escopo:** modelos de dado (relacional/KV/doc/coluna/grafo), SQL vs NoSQL por padrão de acesso, normalização/desnormalização, leader-follower, read replicas, lag e leituras stale, sync vs async, failover/split-brain.
- **Fronteira:** reforço de [[03-Dominios/Ciência/Banco de Dados/index|Banco de Dados]] sob ótica SD; não duplica ACID/índices. Sharding →04, quórum/CAP →06.
- **Fontes:** Kleppmann DDIA cap.5; PostgreSQL docs (streaming replication, v18); MongoDB read-preference; Alex Xu.
- **Resultado:** 424 linhas / ~7600 palavras; 4 Mermaid (inc. sequenceDiagram + split-brain), 6 [!warning], 5 [!question]-. Verificado: links-irmãos e reforço de BD ok; URLs datadas.

#### 04 - Sharding e Consistent Hashing   [substantivo]
- **Estado:** ✅ feita (2026-07-07) · fase: Adepto
- **Escopo:** sharding≠replicação, estratégias de partição (range/hash/geo/entity), shard key e hot spots, `hash % N` vs consistent hashing (anel, virtual nodes, K/N chaves movem), resharding, fan-out cross-shard.
- **Fronteira:** tópico top-pedido; reforça, não duplica BD. Replicação →03, quórum/CAP →06.
- **Fontes:** Karger et al. 1997 (STOC); Amazon Dynamo 2007 (SOSP); Kleppmann DDIA cap.6; Hello Interview; Cassandra vnode default (256→16).
- **Resultado:** 376 linhas / 7120 palavras; 4 Mermaid (anel, hierarquia, virtual-nodes, resharding sequenceDiagram), 3 [!warning], 6 [!question]-. Verificado: links-irmãos ok; URLs (Karger dblp, Dynamo PDF) datadas.

#### 05 - Message queues e processamento assíncrono   [substantivo]
- **Estado:** ✅ feita (2026-07-07) · fase: Adepto
- **Escopo:** por que assíncrono (desacoplar/absorver pico/resiliência/latência), fila vs log (consumo destrutivo vs offset+replay), backpressure (buffer/throttle/drop/scale-out), at-most/at-least/exactly-once + idempotência, ordering só por partição, DLQ + retry backoff, quando NÃO usar fila.
- **Fronteira:** usa [[03-Dominios/Engenharia/Comunicação entre Sistemas/Mensageria/Kafka|Kafka]]/[[RabbitMQ]] como bloco; linka o detalhe interno. Pub/Sub em escala é nota do SG3 (só citada).
- **Fontes:** Kleppmann DDIA cap.11; Alex Xu Vol.2; Confluent (exactly-once/delivery-semantics); RabbitMQ docs (DLX).
- **Resultado:** 296 linhas / 5478 palavras; 3 Mermaid (sync vs async, fila vs log, árvore de garantias), 4 [!warning], 4 [!question]-. Kafka/RabbitMQ confirmados existentes no vault. Verificado: URLs reais datadas.

#### 06 - CAP, consistência e consenso   [substantivo]
- **Estado:** ✅ feita (2026-07-07) · fase: Adepto
- **Escopo:** CAP com precisão (P não é escolha), CP vs AP em sistemas reais (etcd/ZooKeeper vs Cassandra/Dynamo, MongoDB por operação, Spanner+TrueTime), PACELC, espectro de consistência (linearizável→sequencial→causal→eventual, read-your-writes/monotonic reads), quorum R+W>N (+ sloppy quorum/hinted handoff/vetores de versão), consenso (Raft vs Paxos, 2PC), exemplo trabalhado (checkout: estoque CP vs carrinho AP).
- **Fronteira:** reforça CAP do monólito; conceito teórico profundo mora em [[03-Dominios/Ciência/Banco de Dados/12 - Replicação, sharding e CAP|Replicação, sharding e CAP]] (não existe pasta `03-Dominios/Fundamentos` — foi absorvida em Ciência na reorg de camadas). Não duplica replicação mecânica (nota 03) nem sharding (nota 04).
- **Fontes:** Brewer "CAP Twelve Years Later" (IEEE Computer 2012); Abadi PACELC paper (IEEE Computer 2012); Kleppmann DDIA cap.9; Ongaro & Ousterhout Raft paper (USENIX ATC 2014); Gilbert & Lynch (prova formal do CAP, 2002).
- **Resultado:** 378 linhas / 6618 palavras; 6 Mermaid, 5 [!warning], 5 [!question]-. Verificado: links-irmãos ok (03 e 07 existem; 05 é forward-link intencional pois está "em andamento" em paralelo; walkthrough do KV store citado só em prosa pois sub-galho 4 ainda não existe). URLs verificados via WebSearch.

#### 07 - CDN e entrega na borda   [substantivo]
- **Estado:** ✅ feita (2026-07-07) · fase: Adepto · **FECHA o sub-galho**
- **Escopo:** latência geográfica (velocidade da luz), PoPs/edge locations + roteamento (anycast/geo-DNS), cache hit ratio na borda, estático vs dinâmico, push vs pull, invalidação/purge (URL/surrogate key/cache busting por hash), TTL/Cache-Control, TLS termination na borda, edge compute (citado).
- **Fronteira:** nota dedicada (decisão travada — não dobrou em Caching); referencia [[02 - Caching]] p/ políticas gerais e [[01 - Escalabilidade e load balancing]] p/ anycast/geo-LB.
- **Fontes:** Cloudflare/Fastly/AWS CloudFront docs (2025-2026); MDN; System Design Primer. Dados datados: 750+ PoPs / 1140+ embedded, purge ~150-250ms, TLS 1.3 no origin (Nov 2025).
- **Resultado:** 363 linhas / 6491 palavras; 4 Mermaid (inc. user→PoP→origin hit/miss), 4 [!warning], 4 [!question]-. Verificado: links-irmãos e anchors de heading pra 02 conferidos; forward-link [[3 - Padrões recorrentes/index]] intencional (SG3 não criado). URLs reais.
