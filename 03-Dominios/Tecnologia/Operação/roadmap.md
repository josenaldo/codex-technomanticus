---
title: "Roadmap — Operação"
created: 2026-07-08
type: meta
publish: false
tags:
  - meta
  - roadmap
  - operacao
---

# Roadmap — Operação (galho-pai)

Roadmap do galho `03-Dominios/Tecnologia/Operação`. Galho-**pai**: mapeia o estado dos sub-galhos. Cada sub-galho tem seu próprio `roadmap.md` (folha). Spec de origem: [[00-Meta/specs/2026-07-08-operacao-devops-trilha-design]].

## Estado dos sub-galhos

| # | Sub-galho | Fase | Notas planejadas | Estado |
|---|-----------|------|------------------|--------|
| 1 | O ofício de operar | Iniciado→Adepto | 4 | ✅ 4/4 (2026-07-08) |
| 2 | Entrega e release | Adepto | 6 | ✅ 6/6 (2026-07-08) |
| 3 | Rodar em produção | Adepto→Magus | 6 | ✅ 6/6 (2026-07-08) |
| 4 | Observar e responder | Magus | 6 | ✅ 6/6 (2026-07-08) |
| ★ | Capstone — Anatomia de um incidente | Magus | 1 | ⬜ pendente |

**Total planejado:** ~22 notas de conteúdo + 1 capstone (~23) + scaffolding por sub-galho.

## Ordem de execução (ritmo B)

Sub-galho a sub-galho, 1 → 2 → 3 → 4 → capstone. Subagente-por-nota (≤3/onda), Sonnet, barra de densidade explícita no prompt. Commit por sub-galho (paths explícitos, sem Co-Authored-By, push manual). Ao fechar cada sub-galho, atualizar o roadmap-folha dele e esta tabela.

## Rollup para o domínio (ao fechar a trilha)

- Adicionar callouts nos monólitos duplicados ([[Kubernetes]] deployment strategies, [[CI-CD]] deployment strategies/GitOps, [[Observabilidade]] SLO) apontando pra casa canônica nesta trilha.
- Marcar [[00-Meta/Roadmap]] item 9 (Onda C) ⬜ → 🟢.
- Atualizar memória do projeto.

## Pendências transversais

- IaC (SG2-05): conceitual agora; Terraform vira broto/galho futuro se necessário.
- Capstone: decidir ao fechar o SG4 se puxa experiência real do usuário (só se ele fornecer — nunca fabricar).
