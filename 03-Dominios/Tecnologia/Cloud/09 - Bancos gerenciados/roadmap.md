---
title: "Roadmap — Bancos gerenciados"
created: 2026-07-23
updated: 2026-07-23
type: meta
publish: false
tags:
  - meta
  - roadmap
  - cloud
---

# Roadmap — Bancos gerenciados (galho 9)

Roadmap-folha do galho `Cloud/09 - Bancos gerenciados`. Bloco 2 (Os primitivos). Spec: [[00-Meta/specs/2026-07-20-trilha-cloud-design]].

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 6 |
| ⬜ pendente | 0 |
| ✅ feita | 6 |
| 🔄 em andamento | 0 |
| % concluído | 100% ✅ |
| M1 (mídia) | pendente — enriquecimento futuro |

---

## Notas

#### 01 - Por que um banco gerenciado
- **Estado:** ✅ feita · fase: Iniciado · 264 linhas
- **Escopo:** managed vs self-hosted, divisão de responsabilidade (provedor: patch/failover/backup; você: schema/queries/índices/pooling), trade-off custo/controle, cenário de migração EC2→RDS, TCO ilustrativo (managed vence quando o tempo da equipe vale mais que o preço/hora); RDS ↔ DO Managed DB (catálogo 6 engines).

#### 02 - RDS e Managed Databases a fundo
- **Estado:** ✅ feita · fase: Adepto · 408 linhas
- **Escopo:** anatomia da DB instance (engine PostgreSQL/MySQL/MariaDB/Oracle/SQL Server/Db2/Aurora, classe db.*, storage gp3/io1-io2 = EBS por baixo, parameter group estático vs dinâmico), banco em subnet privada + DB subnet group + security group (callout fronteira galho 7), endpoint/conexão, publicly-accessible=false; RDS ↔ DO (PgBouncer embutido).

#### 03 - Alta disponibilidade e réplicas
- **Estado:** ✅ feita · fase: Adepto · 390 linhas
- **Escopo:** distinção-chave Multi-AZ (standby síncrono, não serve tráfego, failover ~1-2min via CNAME) vs read replica (assíncrona, serve leitura, sem failover automático, promovível, cross-region), Multi-AZ DB cluster (2 standbys legíveis), replication lag, Aurora até 15 réplicas; DO standby nodes (até 2) + read-only nodes.

#### 04 - Backups, PITR e manutenção
- **Estado:** ✅ feita · fase: Adepto · 380 linhas
- **Escopo:** HA≠backup (standby replica o DROP fielmente), backups automáticos (retention 0-35d, retention=0 desliga), point-in-time recovery (~5min RPO, restaura pra NOVA instância), snapshots manuais (não expiram, cross-region/account), maintenance window + patching minor/major (Multi-AZ aplica no standby primeiro), restore testado; snapshots→object storage (fronteira galho 8); DO fork + 7d PITR.

#### 05 - NoSQL gerenciado (DynamoDB)
- **Estado:** ✅ feita · fase: Adepto · 392 linhas
- **Escopo:** modelo tabela/item/atributos, partition key (hash) + sort key (range), hot partition (design da chave é tudo), capacity modes (on-demand vs provisioned RCU/WCU), GSI vs LSI, eventual vs strong consistency, Streams/TTL/transações/global tables, contraste com relacional (sem JOIN, modela pela query); DO SEM DynamoDB-like (só MongoDB/Valkey), Cosmos DB/Bigtable são os análogos.

#### 06 - Cache gerenciado e a grande escolha
- **Estado:** ✅ feita · fase: Magus · 430 linhas · **FECHA o galho**
- **Escopo:** ElastiCache Redis/Valkey vs Memcached, cluster mode, MemoryDB (Redis durável), cache-aside/write-through/TTL/eviction, transição Redis→Valkey (licença 2024); a grande escolha — árvore de decisão relacional vs NoSQL vs cache vs object storage, cenário polyglot da loja end-to-end, tabela-síntese requisito→tipo→serviço→armadilha; ponte→galho 10 (DNS/CDN). Capstone.

---

## Pendências

- **M1 (mídia):** enriquecimento de vídeos/podcasts ainda não rodado neste galho — pendente para sessão futura.

## Notas de execução

- Escrito em 2 ondas de 3 agentes (01-03, depois 04-06); orquestrador commitou serialmente (`d944835`, `73df051`). 0 wikilinks quebrados no gate.
- Nota 01 (abertura/porquê, Iniciado) reaberta 1x (215→264) SEM padding: seções "cenário de migração EC2→RDS" + "TCO real". Topou 264 <300 — aceito como nota-abertura/síntese.
- Nota 02: orquestrador adicionou callout de fronteira linkado ao galho 7 (VPC) na seção do endpoint — o agente citava a subnet privada em prosa sem wikilink.
- Notas de mecânica (02, 04, 05) com 10-16 blocos de código; notas de HA/síntese topam ~380-392 com densidade estrutural (aceito, contraste mecânica-vs-critério reconfirmado).
- Capstone (06) fechou 430 — dentro da banda 430-500.
- Honestidade de paridade DO capturada: DO tem 6 engines gerenciados (PostgreSQL, MySQL, Kafka, MongoDB, Valkey, OpenSearch), SEM DynamoDB-like (nota 05); standby nodes até 2 (nota 03); fork + 7d PITR (nota 04); Managed Caching for Valkey (aposentou "Managed Redis", nota 06).
- Fatos datados marcados com [!info]: Redis→Valkey (licença 2024, ElastiCache Valkey 8.0-9.0, DO aposentou Managed Redis, Azure aposentando SKUs Cache for Redis→Managed Redis, GCP Memorystore for Memcached deprecado); RDS PITR ~5min; retention 0-35d.
- Fronteiras: modelagem/SQL-vs-NoSQL → Dados; padrões de cache + escolha de storage → System Design; backup/DR como disciplina → Operação; galho 10 (DNS/CDN) → prosa (não existe).
