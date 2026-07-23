---
title: "Roadmap — Compute II: elasticidade e balanceamento"
created: 2026-07-23
updated: 2026-07-23
type: meta
publish: false
tags:
  - meta
  - roadmap
  - cloud
---

# Roadmap — Compute II: elasticidade e balanceamento (galho 6)

Roadmap-folha do galho `Cloud/06 - Compute II — elasticidade e balanceamento`. Bloco 2 (Os primitivos). Spec: [[00-Meta/specs/2026-07-20-trilha-cloud-design]].

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

#### 01 - Por que uma instância não basta
- **Estado:** ✅ feita · fase: Iniciado · 300 linhas
- **Escopo:** escala horizontal vs vertical, teto e ponto único de falha, o balanceador como porta de entrada, pré-requisito de statelessness, elasticidade vs réplicas fixas.

#### 02 - Balanceamento de carga na nuvem
- **Estado:** ✅ feita · fase: Adepto · 401 linhas
- **Escopo:** ALB (L7) vs NLB (L4), DO Load Balancer, target groups/listeners/regras, algoritmos, sticky sessions, terminação TLS, preservação de IP do cliente.

#### 03 - Health checks
- **Estado:** ✅ feita · fase: Adepto · 392 linhas
- **Escopo:** interval/timeout/healthy+unhealthy threshold, health check do LB vs do ASG, TCP vs HTTP, deregistration delay/draining, liveness vs readiness.

#### 04 - Auto Scaling Groups
- **Estado:** ✅ feita · fase: Adepto · 408 linhas
- **Escopo:** desired/min/max, self-healing, launch template, distribuição multi-AZ, integração ASG↔LB, instance refresh; DO Droplet Autoscale Pools (com lacunas honestas).

#### 05 - Políticas de escala
- **Estado:** ✅ feita · fase: Adepto · 404 linhas
- **Escopo:** target tracking / step / simple (legado) / scheduled, predictive de passagem, escolha de métrica (ALBRequestCountPerTarget), cooldown/warmup, flapping.

#### 06 - Arquitetura elástica de ponta a ponta
- **Estado:** ✅ feita · fase: Magus · 375 linhas · **FECHA o galho**
- **Escopo:** arquitetura de referência DNS→LB→ASG→instâncias stateless→estado externalizado, alta disponibilidade multi-AZ, custo vs resiliência, cenário de queda de AZ, síntese das 6 notas → ponte para o Galho 7 (Rede/VPC). Capstone.

---

## Pendências

- **M1 (mídia):** enriquecimento de vídeos/podcasts ainda não rodado neste galho — pendente para sessão futura.

## Notas de execução

- Escrito em 2 ondas de 3 agentes (01-03, depois 04-06); orquestrador commitou serialmente (`c1c89a5`, `a2337ed`). 0 wikilinks quebrados no gate.
- Fronteira forte com System Design: o conceito de LB mora lá; este galho é a encarnação gerenciada (ELB/DO LB) — linkado, não reexplicado.
- Honestidade de paridade DO: Droplet Autoscale Pools existe (2024) mas é single-datacenter, sem instance refresh, integração com LB via tagging; sem step/scheduled/predictive scaling. Reportado sem inventar paridade.
- Capstone (nota 06) fechou 375 — abaixo do piso Magus 500, aceito por ser síntese/capstone com densidade estrutural no alvo (exceção reconhecida ao piso).
