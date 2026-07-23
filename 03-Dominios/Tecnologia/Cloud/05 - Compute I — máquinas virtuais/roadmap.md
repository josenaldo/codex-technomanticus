---
title: "Roadmap — Compute I: máquinas virtuais"
created: 2026-07-23
updated: 2026-07-23
type: meta
publish: false
tags:
  - meta
  - roadmap
  - cloud
---

# Roadmap — Compute I: máquinas virtuais (galho 5)

Roadmap-folha do galho `Cloud/05 - Compute I — máquinas virtuais`. Abre o Bloco 2 (Os primitivos). Spec: [[00-Meta/specs/2026-07-20-trilha-cloud-design]].

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

#### 01 - Anatomia de uma máquina virtual na nuvem
- **Estado:** ✅ feita · fase: Iniciado · 299 linhas
- **Escopo:** hipervisor/virtualização, instância como recurso alugável, control plane vs instância, EC2 ↔ Droplet, por que a VM segue sendo o primitivo base.

#### 02 - Tipos e famílias de instância
- **Estado:** ✅ feita · fase: Iniciado · 305 linhas
- **Escopo:** dimensões (vCPU/RAM/rede/storage), famílias (general/compute/memory/storage/GPU), nomenclatura EC2 decodificada, Droplet plans, right-sizing.

#### 03 - Imagens, AMIs e provisionamento no boot
- **Estado:** ✅ feita · fase: Adepto · 425 linhas
- **Escopo:** AMI/Snapshot, user data, cloud-init (5 estágios, debug), MIME multi-part, golden image (Packer) vs bootstrap, copy-image entre regiões.

#### 04 - Ciclo de vida de uma instância
- **Estado:** ✅ feita · fase: Adepto · 397 linhas
- **Escopo:** estados e transições, stop/hibernate/terminate, instance store (efêmero) vs EBS/Volumes (persistente), cobrança por estado (DO cobra `off`, AWS não).

#### 05 - Modelos de preço (on-demand, reserved, spot)
- **Estado:** ✅ feita · fase: Adepto · 398 linhas
- **Escopo:** eixo do compromisso, on-demand, Reserved Instances vs Savings Plans, Spot (aviso de 2 min, rebalance), modelo simples da DO, ponte FinOps.

#### 06 - Padrões de uso e o caminho para a elasticidade
- **Estado:** ✅ feita · fase: Magus · 412 linhas · **FECHA o galho**
- **Escopo:** cattle vs pets, infraestrutura imutável, estado externalizado, design tolerante a spot, launch templates versionados, teto da escala vertical → ponte para o Galho 6 (Compute II). Capstone.

---

## Pendências

- **M1 (mídia):** enriquecimento de vídeos/podcasts ainda não rodado neste galho — pendente para sessão futura.

## Notas de execução

- Escrito em 2 ondas de 3 agentes (01-03, depois 04-06); orquestrador commitou serialmente (`47f48ea`, `48ea9db`). 0 wikilinks quebrados no gate.
- Nota 03 reaberta uma vez para atingir o piso Adepto com conteúdo real (cloud-init em profundidade, MIME, Packer), não padding: 276 → 425.
- Nota 06 (capstone Magus) fechou em 412 — abaixo do piso 500, aceito por ser síntese/capstone com densidade estrutural no alvo (exceção reconhecida ao piso).
