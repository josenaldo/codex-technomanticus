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
| 3 | Confiabilidade do contrato | Adepto→Magus | 5 | ⬜ pendente |
| 4 | Comunicação assíncrona | Adepto→Magus | 6 | ⬜ pendente |
| ★ | Capstone — Desenhando a comunicação de um sistema do zero | Magus | 1 | ⬜ pendente |

**Total planejado:** ~22 notas de conteúdo + 1 capstone (~23) + scaffolding por sub-galho.

## Ordem de execução (ritmo B)

Sub-galho a sub-galho, 1 → 2 → 3 → 4 → capstone. Subagente-por-nota (≤3/onda), Sonnet, barra de densidade explícita no prompt. Comparação entre linguagens = tabela/menção curta, nunca tutorial completo (regra desta trilha). Commit por sub-galho (paths explícitos, sem Co-Authored-By, push manual). Ao fechar cada sub-galho, atualizar o roadmap-folha dele e esta tabela.

## Rollup para o domínio (ao fechar a trilha)

- Podar `API Design.md` pro que não migrou, preservando "Na prática (da minha experiência)" verbatim.
- Adicionar callouts em `Mensageria/*.md` apontando pra casa canônica nesta trilha.
- Marcar [[00-Meta/Roadmap]] item 10 (Onda C) ⬜ → 🟢.
- Atualizar memória do projeto.

## Pendências transversais

- EXEMPLAR: usar a nota 01 do System Design até a 1ª nota desta trilha virar exemplar próprio.
- Destino final de `API Design.md` (tronco podado vs redirect fino): decidir no fechamento.
