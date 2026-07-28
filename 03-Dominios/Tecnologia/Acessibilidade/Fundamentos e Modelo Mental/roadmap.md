---
title: "Roadmap — Fundamentos e Modelo Mental"
created: 2026-07-28
type: meta
publish: false
tags:
  - meta
  - roadmap
---

# Roadmap — Fundamentos e Modelo Mental

Diagnóstico nota a nota. Cada entrada tem estado de enriquecimento, score, classificação
de custo e plano de execução acionável. Gerado por `/diagnosticar-galho` (inline — notas
recém-escritas, já em contexto; sem fan-out de subagentes).

**Galho:** `03-Dominios/Tecnologia/Acessibilidade/Fundamentos e Modelo Mental`
**Diagnóstico:** 2026-07-28
**Última execução:** —

## Régua de análise

Checklist `verificar-nota` — 12 itens (isenções por fase/tipo/broto aplicadas por nota):

| Grupo | Itens |
|-------|-------|
| ESTRUTURA | E1 TL;DR · E2 Abertura-problema · E3 Mermaid · E4 Casos práticos · E5 O que vem a seguir · E6 Inglês · E7 Tabela PT↔EN · E8 Armadilhas [!warning] |
| PROFUNDIDADE | P1 Código-com-falha · P2 Mecanismo explicado |
| LINKS | L1 Wikilink cross-galho · L2 Referência externa (URL) |
| MÍDIA | M1 Vídeo/podcast embutido |

**Esquema de `fase:` detectado:** COM fase (Iniciado)
**Piso de linhas:** aplicável — Iniciado ≥300 (todas passam em conteúdo real; ver Estado)

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 5 |
| ⬜ pendente | 5 |
| ➖ não precisa | 0 |
| ✅ feita | 0 |
| % concluído | 0% |

> Núcleo (E1·E2·E5·L2·P2) íntegro nas 5 notas. Gaps concentrados em **M1 (mídia — a 2ª fase), E6/E7 (inglês), E8 (armadilhas), E4 (casos práticos)** e Mermaid onde falta. Nenhuma nota abaixo do piso de conteúdo.

---

## Notas

#### 01 - A11y é ofício, não checklist   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** ~113 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E3, E4, E6, E7, E8, M1
- **Score:** 6/12
- **Plano de execução:**
  - Adicionar `[!tip]` com vídeo introdutório sobre inclusão/curb-cut effect → ativa M1 (pesquisa)
  - Adicionar seção "Como explicar em inglês" + tabela PT↔EN (a11y/deficiência/inclusão) → ativa E6, E7
  - Converter as 3 frentes do "caso de negócio" ou o espectro em `## Casos práticos` (≥2 cenários) → ativa E4
  - Opcional: 1 diagrama Mermaid do espectro permanente/temporário/situacional → ativa E3
- **Resultado:** —

#### 02 - O accessibility tree   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** ~110 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E4, E6, E7, E8, M1
- **Score:** 7/12 (E3 presente)
- **Plano de execução:**
  - Adicionar `[!tip]` com vídeo (ex.: A11ycasts "The Accessibility Tree" / DevTools) → ativa M1 (pesquisa)
  - Adicionar seção de inglês + tabela PT↔EN (accessibility tree/accessible name/role) → ativa E6, E7
  - Converter o exemplo do botão-lixeira num `## Casos práticos` com 2º cenário (ex.: link vs botão) → ativa E4
  - Considerar `[!warning]` para 2–3 armadilhas de name computation → ativa E8
- **Resultado:** —

#### 03 - Leitores de tela e tecnologias assistivas na prática   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** ~86 linhas reais (parágrafos longos, sem hard-wrap; conteúdo denso ~1.660 palavras) · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E3, E4, E6, E7, E8, M1
- **Score:** 6/12
- **Plano de execução:**
  - Adicionar `[!tip]` com vídeo demo de NVDA/VoiceOver navegando uma página → ativa M1 (pesquisa)
  - Adicionar seção de inglês + tabela PT↔EN (screen reader/browse mode/focus mode) → ativa E6, E7
  - Diagrama Mermaid dos dois modos (navegação↔foco) e a transição → ativa E3
  - `## Casos práticos` (ex.: navegar por cabeçalhos vs. por landmarks num portal) → ativa E4
- **Resultado:** —

#### 04 - WCAG 2.2 pelo ofício   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** ~110 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E4, E6, E7, E8, M1
- **Score:** 7/12 (E3 presente)
- **Plano de execução:**
  - Adicionar `[!tip]` com vídeo sobre WCAG/POUR → ativa M1 (pesquisa)
  - Adicionar seção de inglês + tabela PT↔EN (success criterion/conformance level/POUR) → ativa E6, E7
  - `## Casos práticos`: aplicar POUR a 2 componentes reais (ex.: um form, um carrossel) → ativa E4
  - `[!warning]` para armadilhas de leitura de critério (mirar AAA global, confundir nível com prioridade) → ativa E8
- **Resultado:** —

#### 05 - Semântica primeiro, ARIA por último   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** ~102 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E3, E4, E6, E7, M1 (E8 parcial: 1 [!warning], falta ≥3)
- **Score:** 7/12
- **Plano de execução:**
  - Adicionar `[!tip]` com vídeo (ex.: "No ARIA is better than bad ARIA" / MDN ARIA) → ativa M1 (pesquisa)
  - Adicionar seção de inglês + tabela PT↔EN (native semantics/accessible name/ARIA rules) → ativa E6, E7
  - Ampliar armadilhas para ≥3 `[!warning]` (div-como-botão, role sem teclado, aria-hidden em focável) → ativa E8
  - `## Casos práticos`: div-botão vs button, e um widget onde ARIA é legítimo → ativa E4
  - Opcional: Mermaid da árvore de decisão "nativo resolve? → senão ARIA" → ativa E3
- **Resultado:** —
