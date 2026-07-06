---
title: "Roadmap — Performance em Produção"
created: 2026-07-06
type: meta
publish: false
tags:
  - meta
  - roadmap
---

# Roadmap — Performance em Produção

Roadmap do galho `03-Dominios/Tecnologia/Web Performance/Performance em Produção`. Último galho do domínio. Galho **em construção**: eixo primário = **escrita** (8 notas); enriquecimento (M1 mídia) secundário. Roster derivado do [[00-Meta/specs/2026-07-05-dominio-web-performance-design|design 2026-07-05]] (escopo do Galho 4) + `index.md`.

## Régua de análise

- **Escrita:** ⬜ não escrita · 🔄 rascunho · ✅ escrita + verificada + commitada (YYYY-MM-DD).
- **Enriquecimento:** ⬜ pendente · ➖ n/a · ✅ enriquecida (gap esperado = M1 mídia).

**Esquema de `fase:`:** COM fase (Iniciado/Adepto/Magus; piso guiado pelo padrão capítulo).

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 8 |
| ⬜ não escritas | 0 |
| ✅ escritas | 8 |
| % escrito | 100% |

---

## Notas

#### 01 - Do lab ao CI - Lighthouse CI   [substantivo]
- **Fase:** Iniciado · **Escrita:** ✅ (2026-07-06) · **Enriquecimento:** ⬜ (M1)
- **Escopo:** rodar Lighthouse no pipeline (Lighthouse CI), assertions, histórico; do teste manual (G1 nota 04) ao automatizado.

#### 02 - Budgets no pipeline   [substantivo]
- **Fase:** Iniciado · **Escrita:** ✅ (2026-07-06) · **Enriquecimento:** ⬜ (M1)
- **Escopo:** operacionaliza os budgets conceituais de [[03-Dominios/Tecnologia/Web Performance/Medição e Core Web Vitals/08 - Performance budgets e diagnóstico|G1 nota 08]]: bundle size (size-limit/bundlesize), budgets no LHCI, o gate que FALHA o build.

#### 03 - RUM em produção   [substantivo]
- **Fase:** Iniciado · **Escrita:** ✅ (2026-07-06) · **Enriquecimento:** ⬜ (M1)
- **Escopo:** o pipeline de dados de campo — coleta (web-vitals, recap G1 nota 06), transporte, storage, dashboard; provider vs próprio.

#### 04 - Detecção de regressão e alertas   [substantivo]
- **Fase:** Adepto · **Escrita:** ✅ (2026-07-06) · **Enriquecimento:** ⬜ (M1)
- **Escopo:** comparar release a release, alertar quando p75 piora, correlacionar com deploy; ruído vs sinal; orçamento de regressão.

#### 05 - Monitoramento sintético contínuo   [substantivo]
- **Fase:** Adepto · **Escrita:** ✅ (2026-07-06) · **Enriquecimento:** ⬜ (M1)
- **Escopo:** checagens sintéticas agendadas (além do CI), ferramentas (WebPageTest/DebugBear/SpeedCurve), lab contínuo vs RUM; complementaridade.

#### 06 - Diagnóstico avançado no DevTools   [substantivo]
- **Fase:** Adepto · **Escrita:** ✅ (2026-07-06) · **Enriquecimento:** ⬜ (M1)
- **Escopo:** Performance panel a fundo (aprofunda G1 nota 08): gravar, ler flame chart, main thread, achar culprit de LCP/INP/long task/reflow; Performance Insights.

#### 07 - O business case da performance   [substantivo]
- **Fase:** Magus · **Escrita:** ✅ (2026-07-06) · **Enriquecimento:** ⬜ (M1)
- **Escopo:** vender performance com números (recap G1 nota 01 pelo ângulo de priorização/stakeholder), ligar métrica→receita, priorizar por impacto, dashboards executivos.

#### 08 - Cultura de performance   [substantivo]
- **Fase:** Magus · **Escrita:** ✅ (2026-07-06) · **Enriquecimento:** ⬜ (M1)
- **Escopo:** ownership de performance no time, prevenir o apodrecimento, performance como requisito não-funcional; síntese dos 4 galhos. Capstone do DOMÍNIO.

---

## Fronteiras (o que NÃO duplicar)

- **Como medir / o que são as métricas** → Galho 1. Aqui, o que fazer com elas em produção continuamente.
- **Técnicas de otimização** → Galhos 2 e 3. Aqui, como garantir que elas não regridam.
- **CI/CD como disciplina geral** → [[03-Dominios/Engenharia/Operação/index|Engenharia/Operação]]; aqui, o recorte de performance no pipeline.
- Notas do próprio domínio (G1 04/06/08) = **linkadas como base**, aprofundadas pelo ângulo de produção.

## Próximos passos

1. Semear 01→08 via `escrever-nota`, fechando cada uma com `verificar-nota`.
2. Ao completar, marcar o domínio Web Performance como **escrito 32/32** no roadmap do domínio e no [[00-Meta/Roadmap]].
3. Rodada de enriquecimento (M1 mídia) em todo o domínio.
