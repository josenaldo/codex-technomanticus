---
title: "Roadmap — System Design"
created: 2026-07-06
type: meta
publish: false
tags:
  - meta
  - roadmap
  - system-design
---

# Roadmap — System Design (galho-pai)

Roadmap do galho `03-Dominios/Engenharia/Arquitetura/System Design`. Galho-**pai**: mapeia o estado dos sub-galhos. Cada sub-galho tem seu próprio `roadmap.md` (folha). Spec de origem: [[00-Meta/specs/2026-07-06-system-design-trilha-design]].

## Estado dos sub-galhos

| # | Sub-galho | Fase | Notas planejadas | Estado |
|---|-----------|------|------------------|--------|
| 1 | Framework de entrevista | Iniciado | 5 | ✅ 5/5 (2026-07-06) |
| 2 | Building blocks | Adepto | 7 | ✅ 7/7 (2026-07-07) |
| 3 | Padrões recorrentes | Adepto | 6 | ✅ 6/6 (2026-07-07) |
| 4 | Walkthroughs | Magus | 8 | ✅ 8/8 (2026-07-07) |
| ★ | Capstone — Conduzindo a entrevista completa | Magus | 1 | ✅ (2026-07-07) |

**Total:** 26 notas de conteúdo + 1 capstone (27) + scaffolding (index/roadmap por sub-galho). **TRILHA COMPLETA.**

## Ordem de execução (ritmo B)

Sub-galho a sub-galho, ponta a ponta: 1 → 2 → 3 → 4. Commit por sub-galho (paths explícitos, sem Co-Authored-By, push manual). Ao fechar cada sub-galho, atualizar o roadmap-folha dele e esta tabela.

## Rollup para o domínio — FEITO (2026-07-07)

- ✅ **Tronco podado:** o monólito `System Design.md` (921 ln) foi **removido**; seu conteúdo já estava nos 4 sub-galhos, e o meta-conteúdo órfão (armadilhas, experiência de produção do MedEspecialista, inglês consolidado, cross-stack) migrou pro capstone [[Conduzindo a entrevista completa]]; Recursos + Veja também migraram pro `index.md`. `[[System Design]]` agora resolve pra este galho via folder-rule do Quartz.
- ✅ **Item 8 do [[00-Meta/Roadmap]]** (Onda C) marcado 🟡 → 🟢.

## Pendências transversais

- ~~CDN (SG2-07): nota dedicada vs dobrar em Caching~~ — **resolvido:** nota dedicada 07 (2026-07-07).
- ~~Capstone do galho-pai~~ — **feito:** [[Conduzindo a entrevista completa]] (2026-07-07).
