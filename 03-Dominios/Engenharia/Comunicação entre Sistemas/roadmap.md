---
title: "Roadmap — Comunicação entre Sistemas"
created: 2026-07-09
type: meta
publish: false
tags:
  - meta
  - roadmap
  - comunicacao-entre-sistemas
---

# Roadmap — Comunicação entre Sistemas (galho-pai)

Roadmap do galho `03-Dominios/Engenharia/Comunicação entre Sistemas`. Galho-**pai**: mapeia o estado dos sub-galhos. Cada sub-galho tem seu próprio `roadmap.md` (folha). Spec de origem: [[00-Meta/specs/2026-07-09-comunicacao-entre-sistemas-trilha-design]].

## Estado dos sub-galhos

| # | Sub-galho | Fase | Notas planejadas | Estado |
|---|-----------|------|------------------|--------|
| 1 | Panorama e decisão | Iniciado | 5 | ✅ 5/5 (2026-07-09) |
| 2 | Comunicação síncrona | Adepto | 6 | ✅ 6/6 (2026-07-09) |
| 3 | Confiabilidade do contrato | Adepto→Magus | 5 | ✅ 5/5 (2026-07-09) |
| 4 | Comunicação assíncrona | Adepto→Magus | 6 | ✅ 6/6 (2026-07-09) |
| ★ | Capstone — Desenhando a comunicação de um sistema do zero | Magus | 1 | ✅ feito (2026-07-09) |

**Total entregue:** 22 notas de conteúdo + 1 capstone = **23 notas**. Trilha 🟢 COMPLETA (2026-07-09).

## Ordem de execução (ritmo B)

Sub-galho a sub-galho, 1 → 2 → 3 → 4 → capstone. Subagente-por-nota (≤3/onda), Sonnet, barra de densidade explícita no prompt. Comparação entre linguagens = tabela/menção curta, nunca tutorial completo (regra desta trilha). Commit por sub-galho (paths explícitos, sem Co-Authored-By, push manual). Ao fechar cada sub-galho, atualizar o roadmap-folha dele e esta tabela.

## Rollup para o domínio (feito ao fechar a trilha, 2026-07-09)

- ✅ `API Design.md` podado — vira tronco com tabela de redirecionamento por tema, preserva "File upload" (único tema que não migrou) e "Na prática (da minha experiência)" verbatim.
- ✅ Callouts adicionados em `Mensageria.md`, `Kafka.md`, `RabbitMQ.md`, `BullMQ.md`, `Event Streaming.md` apontando pra casa canônica.
- ✅ [[00-Meta/Roadmap]] item 10 (Onda C) ⬜ → 🟢.
- ✅ Memória do projeto atualizada.

## Pendências transversais

- Nenhuma. Trilha fechada.
