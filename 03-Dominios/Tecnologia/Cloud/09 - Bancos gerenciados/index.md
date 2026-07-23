---
title: "Cloud — Bancos gerenciados"
created: 2026-07-23
updated: 2026-07-23
type: moc
status: growing
publish: true
tags:
  - cloud
  - moc
  - bancos
  - database
aliases:
  - "Bancos gerenciados"
  - "Galho 9 - Bancos gerenciados"
---

# Bancos gerenciados

> [!abstract] TL;DR
> Galho 9 da trilha Cloud, Bloco 2 (Os primitivos). Rodar um banco de dados você mesmo parece barato até a primeira falha às 3h da manhã — quem faz o failover, o patch, o restore? O **banco gerenciado** transfere ao provedor as tarefas operacionais não-diferenciadas e te entrega um endpoint. O galho abre pelo *porquê* (managed vs self-hosted, o TCO real), mergulha no relacional gerenciado (RDS/Managed DB por dentro, depois alta disponibilidade com Multi-AZ vs read replicas, depois backups/PITR/manutenção), atravessa para o NoSQL gerenciado (DynamoDB e o design de partition key), e fecha com o cache gerenciado (ElastiCache/Valkey) e a grande escolha — qual tipo de armazenamento de dados para qual necessidade, o padrão de *polyglot persistence*. 6 notas, 3 fases, lente dupla AWS ↔ DigitalOcean.

## Sobre este galho

Os galhos 5-8 deram à aplicação onde computar (compute), como escalar (elasticidade), onde viver (rede) e onde guardar bytes brutos (armazenamento). Falta a camada onde a maioria das aplicações realmente guarda seu *estado*: o banco de dados. Este galho não reensina bancos — ensina o que muda quando o provedor os opera por você, e como escolher entre os tipos gerenciados que ele oferece.

O fio condutor sobe do porquê ao como e volta à decisão. Primeiro o *porquê* — o que "gerenciado" transfere ao provedor, o trade-off honesto de custo e controle. Depois o *relacional* em três notas: a anatomia de uma instância RDS (engine, classe, storage, parameter group), a alta disponibilidade (a distinção crítica entre Multi-AZ para failover e read replicas para escalar leitura), e a proteção dos dados (backups automáticos, point-in-time recovery, manutenção). Depois o *NoSQL* — DynamoDB, onde o design da partition key é tudo e não existe JOIN. E por fim o *cache* — ElastiCache/Valkey à frente do banco — e a síntese: dado um requisito, qual banco, e por que uma arquitetura real usa vários ao mesmo tempo.

**Audiência primária:** quem sabe SQL mas nunca decidiu entre Multi-AZ e read replica, ou entre RDS e DynamoDB, com intenção. **Audiência secundária:** quem já usa banco gerenciado mas nunca formalizou por que HA não é backup, por que uma partition key ruim derruba o DynamoDB, ou quando um cache resolve o que mais storage não resolve.

> [!info] Fronteira
> **Modelagem de dados e a teoria de SQL vs NoSQL** vivem no domínio [[03-Dominios/Engenharia/Dados/index|Dados]]; a **escolha de armazenamento como decisão de arquitetura** e os padrões de cache (cache-aside, write-through) são [[03-Dominios/Engenharia/Arquitetura/index|System Design]]; **backup e DR como disciplina de operação** são [[03-Dominios/Engenharia/Operação/index|Operação]]. Este galho trata o banco como serviço gerenciado da nuvem — a encarnação concreta (RDS, DynamoDB, ElastiCache) dos conceitos que aqueles domínios explicam.

## Iniciado

1. [[03-Dominios/Tecnologia/Cloud/09 - Bancos gerenciados/01 - Por que um banco gerenciado|01 — Por que um banco gerenciado]] — managed vs self-hosted, o que o provedor assume (patch, failover, backup) e o que continua seu (schema, queries, índices), o TCO real, o cenário de migração EC2→RDS; RDS ↔ DO Managed Databases.

## Adepto

2. [[03-Dominios/Tecnologia/Cloud/09 - Bancos gerenciados/02 - RDS e Managed Databases a fundo|02 — RDS e Managed Databases a fundo]] — anatomia da DB instance (engine, classe, storage EBS, parameter group), o banco em subnet privada, endpoint e conexão; RDS ↔ DO Managed DB (connection pool embutido).
3. [[03-Dominios/Tecnologia/Cloud/09 - Bancos gerenciados/03 - Alta disponibilidade e réplicas|03 — Alta disponibilidade e réplicas]] — a distinção crítica Multi-AZ (standby síncrono, failover, não serve tráfego) vs read replica (assíncrona, escala leitura, sem failover automático), replication lag, failover na prática.
4. [[03-Dominios/Tecnologia/Cloud/09 - Bancos gerenciados/04 - Backups, PITR e manutenção|04 — Backups, PITR e manutenção]] — HA não é backup: backups automáticos, point-in-time recovery, snapshots manuais (cross-region), maintenance window e patching, restore testado; AWS ↔ DO.
5. [[03-Dominios/Tecnologia/Cloud/09 - Bancos gerenciados/05 - NoSQL gerenciado (DynamoDB)|05 — NoSQL gerenciado (DynamoDB)]] — o banco que não é relacional: modelo tabela/item/partition key, hot partition, capacity modes (on-demand vs provisioned), GSI/LSI, consistência; DO não tem DynamoDB-like (honestidade).

## Magus

6. [[03-Dominios/Tecnologia/Cloud/09 - Bancos gerenciados/06 - Cache gerenciado e a grande escolha|06 — Cache gerenciado e a grande escolha]] — ElastiCache Redis/Valkey vs Memcached, cache-aside, a transição Redis→Valkey, e a árvore de decisão consolidada: relacional vs NoSQL vs cache vs object storage (polyglot persistence). Capstone do galho e ponte para DNS/CDN/borda.

## Rotas alternativas

### Completa

01 → 02 → 03 → 04 → 05 → 06. Percurso linear — o porquê, o relacional em profundidade, o NoSQL, o cache, e a síntese decisória no fim.

### Já uso RDS, quero fechar as lacunas de fato

03 (a diferença exata Multi-AZ vs read replica que toda entrevista cobra) → 04 (por que HA não é backup, e o PITR na prática) → 06 (a árvore que separa relacional, NoSQL, cache e object sem hesitar).

## Todas as notas

```dataview
TABLE fase, status FROM "03-Dominios/Tecnologia/Cloud/09 - Bancos gerenciados" WHERE type = "concept" SORT file.name ASC
```

## Veja também

- [[03-Dominios/Tecnologia/Cloud/index|Cloud]] (MOC do domínio)
- [[03-Dominios/Tecnologia/Cloud/08 - Armazenamento (object, block e file)/index|Armazenamento (object, block e file)]] — Galho 8, os primitivos de storage (o RDS é EBS por baixo; imagens vão pra object storage)
- [[03-Dominios/Tecnologia/Cloud/07 - Rede na nuvem (VPC)/index|Rede na nuvem (VPC)]] — Galho 7, a subnet privada e o security group que protegem o banco
- [[03-Dominios/Tecnologia/Cloud/05 - Compute I — máquinas virtuais/index|Compute I — máquinas virtuais]] — Galho 5, a VM que é a instância de banco por baixo
- [[03-Dominios/Engenharia/Dados/index|Dados]] — a modelagem e a teoria de bancos que este galho encarna em serviços gerenciados
- [[03-Dominios/Engenharia/Arquitetura/index|System Design]] — a escolha de armazenamento e os padrões de cache como decisão de arquitetura
