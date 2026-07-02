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

> [!warning] Estados derivados do diagnóstico mestre de 30/06 (`00-Meta/guia/roadmap - ia.md`), possivelmente DEFASADOS. Vários galhos marcados com ⬜ pendentes já foram enriquecidos por commits posteriores — o diagnóstico apenas encontrou gaps residuais (E2/E1/E3/piso). Reconciliar o estado real **ao tratar cada galho**, atualizando o roadmap do galho e este rollup.

## Como o rastreio funciona

- **Galho-folha** (só notas): `roadmap.md` mapeia suas notas, uma entrada por nota.
- **Galho-pai** (contém sub-galhos): `roadmap.md` mapeia o estado dos sub-galhos + suas notas diretas.
- **Raiz (este arquivo):** mapeia o estado dos galhos + as notas soltas de `IA/`.
- Ao fechar/mexer num galho, atualizam-se os roadmaps do **galho**, dos **filhos** e dos **pais** (sobe e desce a árvore).

**Legenda de estado:** ✅ completo (0 ⬜) · 📋 diagnosticado, enriquecimento pendente · 🔶 parcial · ⬜ não diagnosticado · ⚪ especial/fora do fluxo · `%` = (✅ + ➖) / total.

## Galhos

| # | Galho | Notas | ⬜ | ➖ | ✅ | % | Estado | roadmap |
|---|-------|------:|---:|---:|---:|--:|--------|---------|
| 1 | [[Anatomia dos LLMs]] | 24 | 23 | 1 | 0 | 4% | 📋 ⚠️ diagnóstico PRÉ-reformulação — re-diagnosticar | ✅ |
| 2 | [[Anatomia de Agents]] | 11 | 11 | 0 | 0 | 0% | 📋 diagnosticado | ✅ |
| 3 | [[Spec-Driven Development]] | 12 | 12 | 0 | 0 | 0% | 📋 diagnosticado (galho mais cru) | ✅ |
| 4 | [[Economia de Tokens]] | 22 | 20 | 2 | 0 | 9% | 📋 diagnosticado | ✅ |
| 5 | [[Context Engineering]] | 16 | 7 | 9 | 0 | 56% | 📋 diagnosticado | ✅ |
| 6 | [[Agentes de Codificação]] | 18 | 15 | 3 | 0 | 17% | 📋 diagnosticado | ✅ |
| 7 | [[AI Engineering Stack]] | 13 | 12 | 1 | 0 | 8% | 📋 diagnosticado | ✅ |
| 8 | [[RAG e Vector Databases]] | 13 | 12 | 1 | 0 | 8% | 📋 diagnosticado | ✅ |
| 9 | [[MCP]] | 10 | 10 | 0 | 0 | 0% | 📋 diagnosticado | ✅ |
| 10 | [[Segurança e Guardrails]] | 12 | 12 | 0 | 0 | 0% | 📋 diagnosticado (⚠️ EU AI Act, prazo 02/08/2026) | ✅ |
| 11 | [[Memória de Agentes]] | 24 | 17 | 7 | 0 | 29% | 📋 diagnosticado | ✅ |
| 12 | [[Prompt Engineering]] | 9 | 7 | 2 | 0 | 22% | 📋 diagnosticado | ✅ |
| 13 | [[Structured Outputs]] | 8 | 0 | 1 | 7 | 100% | ✅ completo (2026-07-02) | ✅ |
| 14 | [[Evaluation]] | 8 | 0 | 4 | 4 | 100% | ✅ completo (2026-07-01) | ✅ |
| 15 | [[Observability]] | 8 | 3 | 5 | 0 | 63% | 📋 diagnosticado | ✅ |
| 16 | [[Multimodal Prompting]] | 7 | 5 | 2 | 0 | 29% | 📋 diagnosticado | ✅ |
| 17 | [[Image Prompting]] | 7 | 4 | 3 | 0 | 43% | 📋 diagnosticado | ✅ |
| 18 | [[Improvement Loop]] | 7 | 3 | 4 | 0 | 57% | 📋 diagnosticado | ✅ |
| 19 | [[Ferramentas de IA]] | 5 | 0 | 0 | 5 | 100% | ✅ completo (2026-07-01) | ✅ |
| 20 | [[Claude Code]] | ~51 (6 sub-galhos) | — | — | — | — | ⬜ não diagnosticado (só Workflows/11 ✅) | ✅ (galho-pai) |
| 21 | [[O Lado Sombrio da IA]] | 1 + glosas | — | — | — | — | ⚪ especial — cluster crítico, fora das trilhas | a criar |

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
| ✅ completos | 3 (Structured Outputs, Evaluation, Ferramentas de IA) |
| 📋 diagnosticados, enriquecimento pendente | 16 |
| ⬜ não diagnosticados | 1 (Claude Code — galho-pai, 6 sub-galhos) |
| ⚪ especiais | 1 (O Lado Sombrio da IA) |
| Notas soltas diretas | 4 |
| Notas totais (galhos-folha diagnosticados) | ~232 |

---

## Próximos passos

1. **Diagnosticar Claude Code** — rodar `/diagnosticar-galho` nos 6 sub-galhos (Configuração, Hooks e Guardrails, Mental Model, Skills e MCP, Time e Automação, Workflows). Ver `Claude Code/roadmap.md`.
2. **Re-diagnosticar Anatomia dos LLMs** — o roadmap atual é pré-reformulação; renumeração invalidou o mapeamento nota-a-nota.
3. **Reconciliar os 16 📋** — ao tratar cada galho via `/enriquecer-galho`, conferir quais ⬜ já foram de fato enriquecidos por commits posteriores ao diagnóstico de 30/06 e atualizar o roadmap do galho + este rollup.
4. **O Lado Sombrio da IA** — decidir se ganha roadmap próprio ou permanece fora do fluxo (cluster crítico, glosas na raiz).
