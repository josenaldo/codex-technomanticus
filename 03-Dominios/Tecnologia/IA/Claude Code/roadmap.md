---
title: "Roadmap — Claude Code"
created: 2026-07-02
type: meta
publish: false
tags:
  - meta
  - roadmap
---

# Roadmap — Claude Code

Roadmap **de galho-pai**: mapeia o estado dos **sub-galhos** (não as notas dos netos) e as **notas diretas** logo abaixo desta pasta. Cada sub-galho tem (ou terá) o próprio `roadmap.md` mapeando as próprias notas.

**Galho:** `03-Dominios/Tecnologia/IA/Claude Code`
**Nível:** galho-pai (contém sub-galhos)

> [!warning] Galho NÃO diagnosticado no mestre (30/06). O diagnóstico nota-a-nota do domínio IA (`00-Meta/guia/roadmap - ia.md`) marcou Claude Code como "vazio/fora de escopo" — os sub-galhos abaixo **nunca foram auditados**. Cada um precisa de `/diagnosticar-galho` antes de virar alvo de enriquecimento.

## Notas diretas (logo abaixo de Claude Code)

| Nota | Tipo | Estado |
|------|------|--------|
| `index.md` | MOC do galho | ➖ não precisa (MOC, não é nota de trilha) |

## Sub-galhos

Estado agregado de cada sub-galho. `roadmap` = existe roadmap por-pasta? Contagens só existem após `/diagnosticar-galho`.

| Sub-galho | Notas | Estado | roadmap |
|-----------|-------|--------|---------|
| Configuração | 8 | ⬜ não diagnosticado | a criar |
| Hooks e Guardrails | 8 | ⬜ não diagnosticado | a criar |
| Mental Model | 9 | ⬜ não diagnosticado | a criar |
| Skills e MCP | 8 | ⬜ não diagnosticado | a criar |
| Time e Automação | 8 | ⬜ não diagnosticado | a criar |
| Workflows | 10 (+ sub-galho "11 - Estratégias estruturais de contexto", 4 notas ✅) | 🔶 parcial — só o sub-galho "11" foi enriquecido (2026-06-27, Modo B); resto não diagnosticado | a criar |

## Tabela-resumo (agregado dos sub-galhos)

| Métrica | Valor |
|---------|-------|
| Sub-galhos | 6 |
| ✅ completos | 0 |
| 🔶 parciais | 1 (Workflows) |
| ⬜ não diagnosticados | 5 |
| Notas diretas | 1 (index.md, MOC) |
| Notas totais estimadas (netos) | ~51 |

---

## Próximos passos

1. `/diagnosticar-galho` em cada sub-galho (um a um) — gera o `roadmap.md` de cada um mapeando suas notas.
2. Ao fechar cada sub-galho, atualizar a linha dele na tabela **Sub-galhos** acima (estado + link) e o rollup deste galho no `IA/roadmap.md` (pai).
3. Workflows é ele próprio um galho-pai (tem o sub-galho "11") — seu roadmap deve seguir este mesmo formato de galho-pai.
