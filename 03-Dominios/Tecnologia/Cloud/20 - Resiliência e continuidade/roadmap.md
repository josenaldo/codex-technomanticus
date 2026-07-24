---
title: "Roadmap — Resiliência e continuidade"
created: 2026-07-24
updated: 2026-07-24
type: meta
publish: false
tags:
  - meta
  - roadmap
  - cloud
---

# Roadmap — Resiliência e continuidade (galho 20)

Roadmap-folha do galho `Cloud/20 - Resiliência e continuidade`. Bloco 4 (Operar em produção) — **galho que fecha o bloco**. Spec: [[00-Meta/specs/2026-07-20-trilha-cloud-design]].

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

#### 01 - Por que resiliência
- **Estado:** ✅ feita · fase: Iniciado · 202 linhas
- **Escopo:** "everything fails, all the time" (Werner Vogels, 2008) como princípio de design; blast radius como conceito central (o raio de impacto de uma falha); os níveis de redundância em escada (instância única → multi-instância mesma AZ → multi-AZ → multi-region → multi-cloud) com custo crescente por degrau; fronteira com System Design (padrão abstrato vs encarnação concreta); disponibilidade como escala de noves (99%→99.999%) com tabela de downtime/ano-mês-semana e SLA real de EC2 (single 99.5% vs Multi-AZ 99.99%); a conta em dinheiro do downtime (e-commerce R$600k/h); failure modes (instância/AZ/região/dependência/rede) com fronteira para Operação (SRE); caso prático Black Friday com AZ caindo passo a passo; comandos CLI de descoberta de topologia (describe-availability-zones / doctl region list); AWS 39 regiões/123 AZs ↔ DigitalOcean 15 datacenters/12 regiões sem conceito de AZ de primeira classe.

#### 02 - Alta disponibilidade
- **Estado:** ✅ feita · fase: Adepto · 343 linhas · nota mais longa do galho (9 blocos de código/config)
- **Escopo:** HA como o reflexo automático dentro de uma região (segundos a poucos minutos, sem decisão humana), distinguida de DR; zona de disponibilidade como unidade de isolamento; SPOF e redundância N+1 com tabela de SPOFs comuns e escondidos (compute, rede de saída, banco, DNS/borda); health checks + Auto Scaling + Route 53 failover em três granularidades (sequence diagram); stateless design (o teste mental de matar a instância no meio de uma sessão) com exemplo de sessão externalizada em Redis; graceful degradation — circuit breaker (código ilustrativo com estados closed/open/half-open), retry com backoff+jitter, timeout, idempotência, bulkhead — cada um com fronteira para System Design/Comunicação; lente dupla AWS (CLI+Terraform de ASG multi-AZ, RDS Multi-AZ) vs DigitalOcean (sem AZ de primeira classe, standby nodes como paridade parcial, LB com health check); tabela de tradução Azure/GCP; testar failover antes do incidente com fronteira para chaos engineering (Operação); o preço da redundância (tensão com FinOps); 3 casos práticos + 6 armadilhas.

#### 03 - RTO, RPO e estratégias de DR
- **Estado:** ✅ feita · fase: Adepto · 263 linhas
- **Escopo:** quando o failover automático (Multi-AZ) não dispara — evento de correlação regional; RTO e RPO definidos com precisão e diagrama; tabela de tiers de criticidade (0-3) com RTO/RPO/estratégia típica; as quatro estratégias canônicas do whitepaper AWS (Backup & Restore, Pilot Light, Warm Standby, Multi-Site Active/Active) com RTO/RPO/custo por estratégia e tabela-síntese; custo multiplicativo por região (não linear); caso prático de uma empresa com quatro workloads em quatro tiers/estratégias diferentes; tabela AWS→serviço gerenciado por estratégia; distinção data plane (Route 53 health check, ARC) vs control plane no failover; Aurora Global Database <1min de promoção; comandos de failover de read replica + Route 53; AWS Resilience Hub para validar o plano; lente DigitalOcean (backup no mesmo datacenter, sem Pilot Light/Warm Standby/Active-Active de prateleira); tabela de tradução Azure/GCP; 4 armadilhas.

#### 04 - Multi-region a fundo
- **Estado:** ✅ feita · fase: Adepto · 292 linhas
- **Escopo:** quando a região inteira é o SPOF (analogia da cidade com bairros/AZs); por que replicação cross-region é sempre assíncrona (velocidade da luz, latência São Paulo↔N.Virgínia); S3 Cross-Region Replication (padrão vs RTC com SLA de 15min, versionamento obrigatório); DynamoDB Global Tables (multi-master, MREC/MRSC, last-writer-wins, RTO~zero); Aurora Global Database (switchover vs failover, write forwarding, latência sub-segundo); tabela comparativa dos três mecanismos (RPO/RTO/resolução de conflito); roteamento (Route 53 failover routing com TTL/FailureThreshold, latency-based, Global Accelerator) com exemplo de health check + registro de recurso; active-passive vs active-active; caso prático de e-commerce decidindo por domínio de dado (catálogo/carrinho→Global Tables, pedidos/pagamento→active-passive Aurora); compliance e residência de dados (GDPR/LGPD) como motor não-DR; lente DigitalOcean honesta sobre a lacuna (sem Global Tables/Aurora Global/S3 CRR, rclone manual para Spaces); quando multi-region é a escolha errada (over-engineering); tabela de tradução Azure/GCP; 5 armadilhas.

#### 05 - Backup, continuidade e teste
- **Estado:** ✅ feita · fase: Adepto · 279 linhas
- **Escopo:** o backup que existia mas não voltava (caso de abertura com 3 falhas: estratégia, imutabilidade, teste); regra 3-2-1 e isolamento de conta/credencial; AWS Backup como orquestrador central (backup plans, tags, lifecycle, cross-region/cross-account fan-in/fan-out) com exemplo de CLI e tabela sem/com AWS Backup; Vault Lock (Governance vs Compliance, grace time mínimo 72h, imutabilidade que nem o root reverte); Business Continuity Plan além da infraestrutura (fronteira para gestão de risco corporativo); testar o DR — restore test e game day (sequence diagram); chaos engineering via AWS Fault Injection Service (actions/targets/stop conditions, exemplo de failover forçado de RDS) com fronteira forte para Operação/SRE; lente dupla DigitalOcean honesta (backup diário/semanal + snapshot sob demanda, sem orquestrador central, sem Vault Lock, sem FIS — chaos exige ferramenta própria tipo Chaos Mesh/Litmus); tabela de tradução Azure/GCP; 3 casos práticos + 5 armadilhas.

#### 06 - Resiliência da arquitetura de referência (capstone do Bloco 4)
- **Estado:** ✅ feita · fase: Magus · 177 linhas · **FECHA o galho e o Bloco 4**
- **Escopo:** o diagrama bonito com um SPOF escondido (arquitetura serverless de referência do Bloco 3 revisitada); o que já vem de graça sem configuração extra (Lambda/S3 11 noves/DynamoDB/API Gateway/EventBridge multi-AZ nativo dentro da região) vs o que é SPOF regional sem config extra (evento de correlação, DynamoDB sem Global Tables, delete/corrupção que replica em ms); árvore de decisão RTO/RPO → estratégia de DR aplicada camada por camada à arquitetura de referência (tabela com 6 componentes: API Gateway+Lambda, Step Functions, DynamoDB, S3, EventBridge, Fargate — cada um com criticidade/RTO-RPO/estratégia/justificativa); o triângulo resiliência × custo × complexidade; armadilha do "já que estamos migrando, vamos fazer active-active em tudo"; lente dupla AWS (kit completo: Global Tables/Aurora Global/S3 CRR/Route 53/IaC redeployável) vs DigitalOcean (HA sólida dentro da região, zero primitiva nativa de replicação multi-região, DR cross-region é construído pela equipe) com tabela de necessidades de DR; tabela de tradução Azure/GCP; síntese do Bloco 4 inteiro (IaC+Observabilidade+Segurança+FinOps+Resiliência como interseção, não soma); ponte para o Bloco 5 (consolidação AWS/DO, multi-cloud, certificação AWS SAA).

---

## Pendências

- **M1 (mídia):** enriquecimento de vídeos/podcasts ainda não rodado neste galho — pendente para sessão futura.

## Notas de execução

- Diagnóstico feito por leitura direta das 6 notas já escritas (galho recebido pronto, sem escrita nesta sessão) — roadmap gerado a posteriori para fechar o rastreio da árvore.
- Fecha o Bloco 4 (Operar em produção) da trilha Cloud: IaC (galho 16) → Observabilidade (galho 17) → Segurança (galho 18) → FinOps (galho 19) → **Resiliência (galho 20)**. O capstone (nota 06) amarra explicitamente as cinco disciplinas na síntese do bloco.
- Fronteiras nomeadas de forma consistente através das 6 notas: System Design/Arquitetura (padrão abstrato de replicação geográfica), Operação/SRE (error budgets, alerting, runbooks, chaos engineering como programa contínuo — não só a ferramenta FIS pontual), Comunicação entre Sistemas (idempotência a fundo), Bancos gerenciados galho 9 (Multi-AZ e réplicas de banco, reciclado sob lente de resiliência, não reexplicado), FinOps galho 19 (tensão custo×redundância citada em quase toda nota).
- Honestidade de paridade DO consistente e reforçada nota a nota: sem AZ de primeira classe (nota 01-02), sem Pilot Light/Warm Standby/Active-Active de prateleira (nota 03), sem Global Tables/Aurora Global/S3 CRR — rclone manual (nota 04), sem orquestrador central de backup nem Vault Lock nem FIS (nota 05), síntese explícita no capstone (nota 06: "isso não é a DO perdendo a comparação — é a DO sendo honesta sobre o que ela é").
- Nenhuma nota do galho ficou abaixo da banda esperada por fase apesar de contagens moderadas (177-343 linhas): densidade de Mermaid (blast radius, escada de redundância, failure modes, SPOF/N+1, health-check sequence, RTO/RPO, quadrantChart de criticidade, árvore de decisão de DR, replicação assíncrona, active-passive/active-active, 3-2-1, AWS Backup plan, game day sequence, arquitetura de referência com SPOF) e tabelas comparativas AWS/DO/Azure/GCP compensam a extensão em linhas — nenhuma nota parece com padding.
- Wikilinks internos ao galho (01↔02↔03↔04↔05↔06) e cruzados (galho 9, galho 15 do Bloco 3, galho 16/17/18/19, System Design/Circuit Breaker, Comunicação/Idempotência, Operação/index e nota de chaos engineering, Armazenamento/Versioning) todos referenciados nas notas — não verificados exaustivamente nesta sessão de roadmap (fora do escopo: só o Veja também do index foi confirmado via `ls`).
