---
title: "Roadmap — Anatomia de um provedor"
created: 2026-07-20
updated: 2026-07-23
type: meta
publish: false
tags:
  - meta
  - roadmap
  - cloud
---

# Roadmap — Anatomia de um provedor (galho 2)

Roadmap-folha do galho `Cloud/02 - Anatomia de um provedor`. Bloco 1 (Modelo mental e fundamentos). Spec: [[00-Meta/specs/2026-07-20-trilha-cloud-design]].

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

#### 01 - A conta e a organização
- **Estado:** ✅ feita · fase: Iniciado
- **Escopo:** a conta como unidade de isolamento/cobrança, root user, blast radius, AWS Organizations vs DigitalOcean Teams/Organizations.

#### 02 - Geografia da nuvem — regions, zonas e edge
- **Estado:** ✅ feita · fase: Iniciado
- **Escopo:** region (preço/catálogo), availability zone (unidade de falha isolada), edge location (cache perto do usuário).

#### 03 - Plano de controle e plano de dados
- **Estado:** ✅ feita · fase: Adepto
- **Escopo:** control plane (orquestração, consistência) vs data plane (tráfego, disponibilidade), rate limit do plano de controle.

#### 04 - As quatro portas — console, CLI, SDK e API
- **Estado:** ✅ feita · fase: Iniciado
- **Escopo:** console, CLI, SDK e API como quatro clientes da mesma API HTTP; ponte para infraestrutura como código.

#### 05 - O modelo de responsabilidade compartilhada
- **Estado:** ✅ feita · fase: Adepto
- **Escopo:** segurança "da" nuvem (provedor) vs "na" nuvem (cliente); a fatia fixa (dados, IAM, config) que nunca se move.

#### 06 - Limites, cotas e o contrato do provedor
- **Estado:** ✅ feita · fase: Magus · **FECHA o galho**
- **Escopo:** cotas ajustáveis mas não instantâneas, rate limit e recuo exponencial, SLA como crédito na fatura, status pages.

---

## Pendências

- **M1 (mídia):** enriquecimento de vídeos/podcasts ainda não rodado neste galho — pendente para sessão futura de enriquecimento.
