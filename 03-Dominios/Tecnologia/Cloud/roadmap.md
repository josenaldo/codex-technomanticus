---
title: "Roadmap — Cloud"
created: 2026-07-20
updated: 2026-07-24
type: meta
publish: false
tags:
  - meta
  - roadmap
  - cloud
---
# Roadmap — Cloud

Roadmap-**raiz** da trilha `03-Dominios/Tecnologia/Cloud`. Mapeia o estado dos **24 galhos** (agrupados em 5 blocos) + capstone. Cada galho terá o próprio `roadmap.md` (Modo A) mapeando suas notas quando for construído.

**Design:** [[00-Meta/specs/2026-07-20-trilha-cloud-design|Design — Trilha Cloud]] · **Plano:** [[00-Meta/specs/2026-07-20-trilha-cloud-plano|Plano de Execução]]

**Nível:** raiz de domínio (contém galhos)

**Legenda de estado:** ✅ completo (0 ⬜) · 📋 diagnosticado, escrita pendente · 🔶 parcial · ⬜ não iniciado · ⚪ especial/fora do fluxo · `%` = (✅ + ➖) / total.

## Notas diretas (logo abaixo desta pasta)

| Nota | Tipo | Estado |
|------|------|--------|
| `index.md` | MOC da trilha | ➖ não precisa |
| `roadmap.md` | este roadmap | ➖ não precisa |
| `Dicionário.md` | glossário do domínio | ➖ não precisa (semeado na Task 0) |
| `Biblioteca.md` | recursos externos | ➖ não precisa (semeado na Task 0) |

## Galhos

### Bloco 1 — Modelo mental e fundamentos

| # | Galho | Notas | Estado | roadmap |
|--:|-------|------:|--------|---------|
| 1 | O que é a nuvem, de verdade | 6 | ✅ completo | [[03-Dominios/Tecnologia/Cloud/01 - O que é a nuvem, de verdade/roadmap|roadmap]] |
| 2 | Anatomia de um provedor | 6 | ✅ completo | [[03-Dominios/Tecnologia/Cloud/02 - Anatomia de um provedor/roadmap|roadmap]] |
| 3 | Well-Architected Framework | 7 | ✅ completo | [[03-Dominios/Tecnologia/Cloud/03 - Well-Architected Framework/roadmap|roadmap]] |
| 4 | Identidade e acesso (IAM) | 6 | ✅ completo | [[03-Dominios/Tecnologia/Cloud/04 - Identidade e acesso (IAM)/roadmap|roadmap]] |

### Bloco 2 — Os primitivos

| # | Galho | Notas | Estado | roadmap |
|--:|-------|------:|--------|---------|
| 5 | Compute I — máquinas virtuais | 6 | ✅ completo | [[03-Dominios/Tecnologia/Cloud/05 - Compute I — máquinas virtuais/roadmap|roadmap]] |
| 6 | Compute II — elasticidade e balanceamento | 6 | ✅ completo | [[03-Dominios/Tecnologia/Cloud/06 - Compute II — elasticidade e balanceamento/roadmap|roadmap]] |
| 7 | Rede na nuvem (VPC) | 6 | ✅ completo | [[03-Dominios/Tecnologia/Cloud/07 - Rede na nuvem (VPC)/roadmap|roadmap]] |
| 8 | Armazenamento — object, block e file | 6 | ✅ completo | [[03-Dominios/Tecnologia/Cloud/08 - Armazenamento (object, block e file)/roadmap|roadmap]] |
| 9 | Bancos gerenciados | 6 | ✅ completo | [[03-Dominios/Tecnologia/Cloud/09 - Bancos gerenciados/roadmap|roadmap]] |
| 10 | DNS, CDN e borda | 6 | ✅ completo | [[03-Dominios/Tecnologia/Cloud/10 - DNS, CDN e borda/roadmap|roadmap]] |

### Bloco 3 — Serverless e arquiteturas modernas

| # | Galho | Notas | Estado | roadmap |
|--:|-------|------:|--------|---------|
| 11 | Serverless e FaaS — Lambda a fundo | 6 | ✅ completo | [[03-Dominios/Tecnologia/Cloud/11 - Serverless e FaaS — Lambda a fundo/roadmap|roadmap]] |
| 12 | Containers gerenciados | 6 | ✅ completo | [[03-Dominios/Tecnologia/Cloud/12 - Containers gerenciados/roadmap|roadmap]] |
| 13 | Mensageria e eventos gerenciados | 6 | ✅ completo | [[03-Dominios/Tecnologia/Cloud/13 - Mensageria e eventos gerenciados/roadmap|roadmap]] |
| 14 | API Gateway e edge de aplicação | — | ⬜ não iniciado | a criar |
| 15 | Arquiteturas serverless e event-driven | — | ⬜ não iniciado | a criar |

### Bloco 4 — Operar, sustentar, governar

| # | Galho | Notas | Estado | roadmap |
|--:|-------|------:|--------|---------|
| 16 | Infrastructure as Code | — | ⬜ não iniciado | a criar |
| 17 | Observabilidade na cloud | — | ⬜ não iniciado | a criar |
| 18 | Segurança na cloud a fundo | — | ⬜ não iniciado | a criar |
| 19 | FinOps — a economia da cloud | — | ⬜ não iniciado | a criar |
| 20 | Resiliência e continuidade | — | ⬜ não iniciado | a criar |

### Bloco 5 — Provedores e maestria

| # | Galho | Notas | Estado | roadmap |
|--:|-------|------:|--------|---------|
| 21 | AWS a fundo — consolidação | — | ⬜ não iniciado | a criar |
| 22 | DigitalOcean a fundo — consolidação | — | ⬜ não iniciado | a criar |
| 23 | Panorama multi-cloud e portabilidade | — | ⬜ não iniciado | a criar |
| 24 | Certificação — AWS Solutions Architect Associate | — | ⬜ não iniciado | a criar |

### Capstone

| # | Galho | Notas | Estado | roadmap |
|--:|-------|------:|--------|---------|
| — | Arquitetar um SaaS na cloud do zero | — | ⬜ não iniciado | — |

## Tabela-resumo (agregado)

| Métrica | Valor |
|---------|-------|
| Galhos | 13/24 escritos |
| ✅ completos | 13 (Blocos 1-2 inteiros + galhos 11-13 do Bloco 3) |
| 🔶 parciais | 0 |
| ⬜ não iniciados | 11 + capstone |
| Notas escritas | 79 |
| M1 (mídia) pendente | galhos 1-13 (79 notas) + resto do domínio |

---

## Próximos passos

1. **Task 0:** ✅ andaime do domínio — `index.md`, `roadmap.md`, `Dicionário.md`, `Biblioteca.md`, `Senda Cloud.md` reescrita.
2. **Bloco 1 (galhos 1-4):** ✅ completo — 25 notas + index.md/roadmap.md de cada galho.
3. **Bloco 2 — galhos 5-10 (Compute I, Compute II, Rede/VPC, Armazenamento, Bancos gerenciados, DNS/CDN/borda):** ✅ **completo** — 36 notas + index.md/roadmap.md de cada. Galho 10 fechou o bloco em 2026-07-24.
4. **Bloco 3 (galhos 11-15, Serverless e arquiteturas modernas):** em curso — galhos 11 (Serverless/FaaS) e 12 (Containers gerenciados) ✅ fechados 2026-07-24. Próximo: galho 13 (Mensageria e eventos gerenciados — SQS/SNS/EventBridge; ponte→Comunicação).
5. **Pendência registrada:** enriquecimento de mídia (M1) — Bloco 1 já elegível, ainda não rodado; demais blocos entram na fila conforme forem escritos.
