---
title: "Roadmap — <% tp.file.folder(false) %>"
created: <% tp.date.now("YYYY-MM-DD") %>
type: meta
publish: false
tags:
  - meta
  - roadmap
---

<%* /* ───────────────────────────────────────────────────────────────────────── TEMPLATE DE ROADMAP DE GALHO — rastreio multi-nível do vault.

   Todo galho (pasta de trilha) deve ter um `roadmap.md`. O rastreio é recursivo: raiz-do-domínio → galho → sub-galho → nota. Cada nível mapeia SÓ o nível imediatamente abaixo — sem sobreposição: • galho-FOLHA (só notas)      → mapeia suas NOTAS (uma entrada por nota). • galho-PAI  (tem sub-galhos) → mapeia o ESTADO dos SUB-GALHOS + suas notas diretas. • RAIZ de domínio             → mapeia o ESTADO dos GALHOS + notas soltas do domínio.

   COMO USAR:
   1. Escolha o MODO abaixo (A = folha, B = pai/raiz) e APAGUE o bloco do outro modo.
   2. Preencha os <placeholders>.
   3. Geração automática: a skill /diagnosticar-galho produz o MODO A já preenchido, lendo cada nota e auditando contra /verificar-nota. Prefira a skill para galhos-folha; use este template à mão para galhos-pai/raiz ou quando quiser o esqueleto. ───────────────────────────────────────────────────────────────────────── */ -%>
# Roadmap — <% tp.file.folder(false) %>

<!-- Uma linha dizendo o que este roadmap cobre e de onde veio o diagnóstico. --> Roadmap do galho `<caminho/relativo/ao/vault>`. <!-- ex: 03-Dominios/Tecnologia/IA/MCP -->

> [!warning] <!-- Ressalva de frescor: cite a data do diagnóstico e o risco de defasagem. Remova se o diagnóstico é fresco. -->
> Diagnóstico de <data> — pode estar defasado. Itens ⬜ podem já ter sido resolvidos; reconciliar ao tratar o galho.

<%* /* ══════════════════════════════════════════════════════════════════════════ MODO A — GALHO-FOLHA (só notas). Mantenha este bloco; apague o MODO B. ══════════════════════════════════════════════════════════════════════════ */ -%>
## Régua de análise

Checklist `verificar-nota` — 12 itens (isenções por fase/tipo/broto aplicadas por nota):

| Grupo | Itens |
|-------|-------|
| ESTRUTURA | E1 TL;DR · E2 Abertura-problema · E3 Mermaid · E4 Casos práticos · E5 O que vem a seguir · E6 Inglês · E7 Tabela PT↔EN · E8 Armadilhas [!warning] |
| PROFUNDIDADE | P1 Código-com-falha · P2 Mecanismo explicado |
| LINKS | L1 Wikilink cross-galho · L2 Referência externa (URL) |
| MÍDIA | M1 Vídeo/podcast embutido |

**Esquema de `fase:` detectado:** <COM fase (Iniciado ≥300 / Adepto ≥400) | SEM fase (sequência) | MISTO> **Piso de linhas:** <aplicável — ... | N/A (sem fase)>

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | <N> |
| ⬜ pendente | <N> |
| ➖ não precisa | <N> |
| ✅ feita | <N> |
| 🔄 em andamento | <N> |
| % concluído | <N>% |

---

## Notas

<!-- Uma entrada por nota. Estados: ⬜ pendente · 🔄 em andamento · ✅ feita (YYYY-MM-DD) · ➖ não precisa. Classificação de custo no cabeçalho: [mecânico] (correção barata, sem pesquisa) · [substantivo] (expansão/pesquisa). -->

#### NN - Título da nota   [mecânico|substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** <N> linhas · fase: <X|—> · status: <y>
- **Núcleo/gaps:** <códigos dos itens faltantes, ex: E2, E3, P1>
- **Score:** <N>/12
- **Plano de execução:**
  - <ação concreta ou "— nenhuma">
- **Resultado:** —

<%* /* ══════════════════════════════════════════════════════════════════════════ MODO B — GALHO-PAI ou RAIZ (mapeia sub-galhos/galhos por estado). Apague o MODO A acima e mantenha este. Para a RAIZ de um domínio, troque "Sub-galho"→"Galho" e ajuste os títulos. ══════════════════════════════════════════════════════════════════════════ */ -%> **Nível:** <galho-pai (contém sub-galhos) | raiz de domínio>

**Legenda de estado:** ✅ completo (0 ⬜) · 📋 diagnosticado, enriquecimento pendente · 🔶 parcial · ⬜ não diagnosticado · ⚪ especial/fora do fluxo · `%` = (✅ + ➖) / total.

## Notas diretas (logo abaixo desta pasta)

<!-- Notas .md diretas neste nível (não as dos filhos). MOCs/index geralmente são ➖. -->

| Nota | Tipo | Estado |
|------|------|--------|
| `index.md` | MOC | ➖ não precisa |

## Sub-galhos

<!-- Um por sub-galho. Contagens (⬜/➖/✅) só existem depois que o sub-galho tem roadmap. -->

| Sub-galho | Notas | ⬜ | ➖ | ✅ | % | Estado | roadmap |
|-----------|------:|---:|---:|---:|--:|--------|---------|
| <nome> | <N> | — | — | — | — | ⬜ não diagnosticado | a criar |

## Tabela-resumo (agregado)

| Métrica | Valor |
|---------|-------|
| Sub-galhos | <N> |
| ✅ completos | <N> |
| 🔶 parciais | <N> |
| ⬜ não diagnosticados | <N> |
| Notas diretas | <N> |

---

## Próximos passos

<!-- Ações concretas. Ao mexer num galho, atualizar os roadmaps do galho, dos filhos e dos pais (sobe e desce a árvore). -->
1. <ação>
