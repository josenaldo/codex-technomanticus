---
title: "Roadmap — Image Prompting"
created: 2026-07-02
type: meta
publish: false
tags:
  - meta
  - roadmap
---

# Roadmap — Image Prompting

Diagnóstico migrado de guia/roadmap - ia.md (30/06). Cada entrada tem estado de enriquecimento, score, classificação de custo e plano de execução acionável.

**Galho:** `03-Dominios/Tecnologia/IA/Image Prompting`

> [!warning] Diagnóstico de 30/06 — pode estar defasado. Vários itens marcados ⬜ podem já ter sido enriquecidos depois; reconciliar com o estado real ao tratar o galho.

## Régua de análise

Checklist `verificar-nota` — 12 itens (isenções por fase/tipo/broto aplicadas por nota):

| Grupo | Itens |
|-------|-------|
| ESTRUTURA | E1 TL;DR · E2 Abertura-problema · E3 Mermaid · E4 Casos práticos · E5 O que vem a seguir · E6 Inglês · E7 Tabela PT↔EN · E8 Armadilhas [!warning] |
| PROFUNDIDADE | P1 Código-com-falha · P2 Mecanismo explicado |
| LINKS | L1 Wikilink cross-galho · L2 Referência externa (URL) |
| MÍDIA | M1 Vídeo/podcast embutido |

**Esquema de `fase:` detectado:** COM fase (Iniciado)
**Piso de linhas:** aplicável — Iniciado ≥300

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 7 |
| ⬜ pendente | 4 |
| ➖ não precisa | 3 |
| ✅ feita | 0 |
| 🔄 em andamento | 0 |
| % concluído | 0% |

---

## Notas

#### 01 - Image prompting como engenharia   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 301 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E3, P1
- **Score:** 10/12
- **Plano de execução:**
  - — nenhuma
- **Resultado:** —

#### 02 - Deliverable-first, não scene-first   [mecânico]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 301 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E1
- **Score:** 9/12
- **Plano de execução:**
  - Expandir o `[!abstract]` TL;DR de 2 linhas markdown para ≥3 (quebrar o parágrafo único em pelo menos 3 linhas de citação `> `); como está, o callout tem só header + 1 linha de texto, abaixo do mínimo formal
- **Resultado:** —

#### 03 - Modelos de imagem 2026 — DALL-E, Imagen, Midjourney, FLUX, SD   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 236 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E2, E3, P1
- **Score:** 9/12
- **Plano de execução:**
  - Adicionar abertura com problema/cenário (~10-15 linhas) antes da tabela comparativa: contextualizar "por que tantos modelos existem" e "o custo real de escolher errado" — cobre E2 e contribui para o piso
  - Converter o decision tree ASCII (linhas 76-98) para um diagrama Mermaid `flowchart TD` equivalente — cobre E3 e adiciona ~20 linhas de estrutura
  - Completar com ~1 caso prático trabalhado (entregável real → modelo escolhido → prompt enviado → resultado) para atingir o piso — cobre P1
  - Atualizar `[!warning]` de caducidade: Imagen 4 (já lançado em 2026, hoje referenciado como "quando disponível"), FLUX.1.1 Pro Ultra, e web API oficial do Midjourney (2025), que altera a armadilha "pipeline via Discord bot"
- **Resultado:** —

#### 04 - Anatomia de um prompt visual — canvas, composição, estilo   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 282 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E2, E3, P1
- **Score:** 9/12
- **Plano de execução:**
  - Expandir TL;DR para ≥3 linhas de corpo (atualmente 1 linha densa; quebrar em 3 linhas curtas com as 4 camadas + a regra do default)
  - Substituir abertura de tabela por parágrafo-problema de 3-4 linhas (ex: cenário de abrir o Midjourney sem saber o que digitar além do tema) antes da tabela "As quatro camadas"
  - Essas duas mudanças já devem elevar o conteúdo para ≥300 linhas e zerar as lacunas de núcleo
- **Resultado:** —

#### 05 - Templates por entregável — poster, infográfico, mockup, thumbnail   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 216 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E2, E3
- **Score:** 9/12
- **Plano de execução:**
  - Adicionar abertura com problema/cenário antes de "Como usar os templates" (2-3 §§ que enquadrem a dor: sem template você reescreve o mesmo brief do zero para cada entregável, erra o canvas, erra a hierarquia)
  - Expandir via diagrama Mermaid de decisão (qual template escolher por canal/canvas) para +15-20 linhas reais e ganhar E3
  - As duas ações juntas devem levar a nota acima de 300 linhas reais e zerar as lacunas de núcleo
- **Resultado:** —

#### 06 - Iteração visual — controlled changes   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 301 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E3, P1
- **Score:** 10/12
- **Plano de execução:**
  - — nenhuma
- **Resultado:** —

#### 07 - Geração de diagramas e ilustrações técnicas   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 301 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E3, P1
- **Score:** 10/12
- **Plano de execução:**
  - — nenhuma
- **Resultado:** —
