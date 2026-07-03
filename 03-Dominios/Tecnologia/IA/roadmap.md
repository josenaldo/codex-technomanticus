---
title: "Roadmap — IA (raiz do domínio)"
created: 2026-07-02
type: meta
publish: false
tags:
  - meta
  - roadmap
---

# Roadmap — IA (raiz do domínio)

Roadmap **raiz do domínio**: mapeia o **estado de cada galho** (não as notas dos galhos) e as **notas soltas** logo abaixo de `IA/`. Cada galho tem o próprio `roadmap.md` mapeando suas notas (e, se for galho-pai, seus sub-galhos).

**Domínio:** `03-Dominios/Tecnologia/IA`
**Nível:** raiz (contém galhos)
**Rastreio multi-nível:** raiz → galho → (sub-galho) → nota. Cada nível mapeia só o nível imediatamente abaixo.

> [!note] Auditoria de reconciliação — 2026-07-03. Cruzamento de contagem de notas, mapeamento entrada-do-roadmap↔arquivo e git (último commit de nota por galho) confirmou que **os 21 roadmaps de galho estão estruturalmente atuais**. O medo anterior ("vários ⬜ já foram enriquecidos por commits posteriores") **não se materializou**: nenhuma nota de galho pendente foi alterada após o diagnóstico de 30/06 — só os 3 galhos já ✅ (Ferramentas 01/07, Evaluation e Structured Outputs 02/07) tiveram commits posteriores. Os estados ⬜/✅ abaixo são fiéis. Banner falso de Anatomia dos LLMs corrigido nesta data. Nenhum galho exige re-diagnóstico.

## Como o rastreio funciona

- **Galho-folha** (só notas): `roadmap.md` mapeia suas notas, uma entrada por nota.
- **Galho-pai** (contém sub-galhos): `roadmap.md` mapeia o estado dos sub-galhos + suas notas diretas.
- **Raiz (este arquivo):** mapeia o estado dos galhos + as notas soltas de `IA/`.
- Ao fechar/mexer num galho, atualizam-se os roadmaps do **galho**, dos **filhos** e dos **pais** (sobe e desce a árvore).

**Legenda de estado:** ✅ completo (0 ⬜) · 📋 diagnosticado, enriquecimento pendente · 🔶 parcial · ⬜ não diagnosticado · ⚪ especial/fora do fluxo · `%` = (✅ + ➖) / total.

## Galhos

| # | Galho | Notas | ⬜ | ➖ | ✅ | % | Estado | roadmap |
|---|-------|------:|---:|---:|---:|--:|--------|---------|
| 1 | [[Anatomia dos LLMs]] | 24 | 0 | 1 | 23 | 100% | ✅ completo (2026-07-03) | ✅ |
| 2 | [[Anatomia de Agents]] | 11 | 11 | 0 | 0 | 0% | 📋 diagnosticado | ✅ |
| 3 | [[Spec-Driven Development]] | 12 | 12 | 0 | 0 | 0% | 📋 diagnosticado (galho mais cru) | ✅ |
| 4 | [[Economia de Tokens]] | 22 | 20 | 2 | 0 | 9% | 📋 diagnosticado | ✅ |
| 5 | [[Context Engineering]] | 16 | 0 | 9 | 7 | 100% | ✅ completo (2026-07-03) | ✅ |
| 6 | [[Agentes de Codificação]] | 18 | 15 | 3 | 0 | 17% | 📋 diagnosticado | ✅ |
| 7 | [[AI Engineering Stack]] | 13 | 12 | 1 | 0 | 8% | 📋 diagnosticado | ✅ |
| 8 | [[RAG e Vector Databases]] | 13 | 12 | 1 | 0 | 8% | 📋 diagnosticado | ✅ |
| 9 | [[MCP]] | 10 | 10 | 0 | 0 | 0% | 📋 diagnosticado | ✅ |
| 10 | [[Segurança e Guardrails]] | 12 | 12 | 0 | 0 | 0% | 📋 diagnosticado (⚠️ EU AI Act, prazo 02/08/2026) | ✅ |
| 11 | [[Memória de Agentes]] | 24 | 17 | 7 | 0 | 29% | 📋 diagnosticado | ✅ |
| 12 | [[Prompt Engineering]] | 9 | 0 | 2 | 7 | 100% | ✅ completo (2026-07-03) | ✅ |
| 13 | [[Structured Outputs]] | 8 | 0 | 1 | 7 | 100% | ✅ completo (2026-07-02) | ✅ |
| 14 | [[Evaluation]] | 8 | 0 | 4 | 4 | 100% | ✅ completo (2026-07-01) | ✅ |
| 15 | [[Observability]] | 8 | 0 | 5 | 3 | 100% | ✅ completo (2026-07-03) | ✅ |
| 16 | [[Multimodal Prompting]] | 7 | 0 | 2 | 5 | 100% | ✅ completo (2026-07-03 — notas 04/05 refeitas com pesquisa real após reprovação) | ✅ |
| 17 | [[Image Prompting]] | 7 | 0 | 3 | 4 | 100% | ✅ completo (2026-07-03) | ✅ |
| 18 | [[Improvement Loop]] | 7 | 0 | 4 | 3 | 100% | ✅ completo (2026-07-03) | ✅ |
| 19 | [[Ferramentas de IA]] | 5 | 0 | 0 | 5 | 100% | ✅ completo (2026-07-01) | ✅ |
| 20 | [[Claude Code]] | 55 (6 sub-galhos) | 54 | 1 | 0 | 2% | 📋 diagnosticado (2026-07-02, galho-pai completo) | ✅ (galho-pai) |
| 21 | [[O Lado Sombrio da IA]] | 1 + glosas | 1 | 0 | 0 | 0% | ⚪ especial — cluster crítico; nota Débito cognitivo diagnosticada (2026-07-02) | ✅ |

## Notas soltas (logo abaixo de IA/)

| Nota | Tipo | Estado |
|------|------|--------|
| `Dicionário de IA.md` | glossary | ➖ saudável (diagnóstico 30/06) |
| `Modelo de Maturidade AI - Steve Yegge.md` | nota solta | ⬜ sem TL;DR/fase (diagnóstico 30/06) |
| `Biblioteca de Desenvolvimento com IA.md` | reference | ⬜ stub (diagnóstico 30/06) |
| `index.md` | MOC do domínio | ➖ não precisa |

## Tabela-resumo (agregado dos galhos)

| Métrica | Valor |
|---------|-------|
| Galhos totais | 21 |
| ✅ completos | 9 (Anatomia dos LLMs, Structured Outputs, Evaluation, Ferramentas de IA, Context Engineering, Prompt Engineering, Observability, Image Prompting, Improvement Loop) |
| 📋 diagnosticados, enriquecimento pendente | 11 (inclui Claude Code; Multimodal Prompting parcial 71%, 2 ⬜) |
| ⬜ não diagnosticados | 0 |
| ⚪ especiais | 1 (O Lado Sombrio da IA — agora com roadmap) |
| Notas soltas diretas | 4 |
| Notas totais (galhos-folha diagnosticados) | ~287 (232 + 55 de Claude Code) |

> **IA 100% diagnosticado em 2026-07-02** — todos os 21 galhos têm `roadmap.md`. Último buraco (Claude Code, galho-pai de 6 sub-galhos = 55 notas) fechado via workflow de fan-out (48 notas em ~2,4 min).

---

## Próximos passos

1. ~~**Diagnosticar Claude Code**~~ ✅ **feito (2026-07-02)** — 6 sub-galhos, 55 notas, todos com `roadmap.md`. Ver `Claude Code/roadmap.md`.
2. ~~**Re-diagnosticar Anatomia dos LLMs**~~ ✅ **desnecessário (auditoria 03/07)** — o roadmap já está pós-reformulação e mapeia 1:1 para os arquivos; banner defasado corrigido.
3. ~~**Reconciliar os 📋**~~ ✅ **feito (auditoria 03/07)** — git confirmou que nenhuma nota de galho pendente mudou após o diagnóstico de 30/06; estados ⬜/✅ fiéis. Próximo movimento em cada galho é **enriquecimento** (`/enriquecer-galho`), não re-diagnóstico.
4. ~~**O Lado Sombrio da IA**~~ ✅ nota Débito cognitivo diagnosticada; cluster mantém glosas na raiz (não promover), mas agora tem `roadmap.md`.
