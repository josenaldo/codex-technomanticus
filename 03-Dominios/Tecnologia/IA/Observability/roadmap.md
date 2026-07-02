---
title: "Roadmap — Observability"
created: 2026-07-02
type: meta
publish: false
tags:
  - meta
  - roadmap
---

# Roadmap — Observability

Diagnóstico migrado de guia/roadmap - ia.md (02/07). Cada entrada tem estado de enriquecimento, score, classificação de custo e plano de execução acionável.

**Galho:** `03-Dominios/Tecnologia/IA/Observability`

> [!warning] Diagnóstico de 02/07 — pode estar defasado. Vários itens marcados ⬜ podem já ter sido enriquecidos depois; reconciliar com o estado real ao tratar o galho.

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
| Total de notas | 8 |
| ⬜ pendente | 3 |
| ➖ não precisa | 5 |
| ✅ feita | 0 |
| 🔄 em andamento | 0 |
| % concluído | 0% |

---

## Notas

#### 01 - Por que LLMs precisam de observabilidade   [mecânico]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 302 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E3, P1
- **Score:** 10/12
- **Plano de execução:**
  - Remover a segunda seção `## Veja também` duplicada (a primeira já é mais completa e inclui todos os links; manter apenas ela)
- **Resultado:** —

#### 02 - Anatomia de um trace LLM   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 242 linhas reais ⚠️ (piso Iniciado ≥300: não passa) · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E2, E3, P1
- **Score:** 9/12
- **Plano de execução:**
  - Adicionar parágrafo de abertura-problema logo após o TL;DR: cenário concreto (ex: "um agent respondeu errado; como investigar sem hierarquia de spans?") — cobre E2 e soma ~15 linhas
  - Adicionar diagrama Mermaid da árvore sessão→trace→spans, substituindo o bloco ASCII — cobre E3 e soma ~10 linhas
  - Completar com bloco P1 "código-com-falha" mostrando o anti-padrão de criar `trace_id` novo a cada LLM call (já descrito em [!warning] mas sem código) — fecha o piso e marca P1
- **Resultado:** —

#### 03 - Langfuse — open-source standard   [substantivo]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 302 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E3, P1
- **Score:** 10/12
- **Plano de execução:**
  - Substituir diagrama ASCII da arquitetura por Mermaid `graph LR` — fecha E3 sem conteúdo novo
  - Adicionar bloco P1 "código-com-falha" com anti-padrão de criar `trace_id` novo a cada LLM call (já descrito no [!warning] de flush, mas sem código) — fecha P1
  - Caducidade (nota de ferramenta): Langfuse faz releases mensais; revisar free-tier (50k obs/mês), preços e versões do SDK a cada ~3 meses
- **Resultado:** —

#### 04 - Helicone, Phoenix, OpenLLMetry — alternativas   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 204 linhas reais ⚠️ (piso Iniciado ≥300: não passa) · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E3, P1
- **Score:** 10/12
- **Plano de execução:**
  - Adicionar ~100 linhas de conteúdo real: diagrama Mermaid de decisão "qual ferramenta escolher" (fecha E3), bloco P1 "código-com-falha" (ex: instrumentação sem reusar tracer_provider, ou mistura de schemas OpenInference+OTel GenAI), e expandir "Combinações comuns" com exemplo de stack completa
  - Caducidade (catálogo de ferramentas): pricing (Helicone 10k/mês, Langfuse 50k obs/mês, Arize Phoenix Cloud) e trajetória dos projetos podem caducar em 3-6 meses — revisar antes de enriquecer
- **Resultado:** —

#### 05 - Versionamento de prompts   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 301 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E3
- **Score:** 11/12
- **Plano de execução:**
  - — nenhuma
- **Resultado:** —

#### 06 - Session replay e debugging   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 301 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E3, P1
- **Score:** 10/12
- **Plano de execução:**
  - — nenhuma
- **Resultado:** —

#### 07 - Métricas que importam — latência, custo, qualidade   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 301 linhas · fase: Iniciado · status: seedling
- **Núcleo/gaps:** não especificados na fonte
- **Score:** 10/12
- **Plano de execução:**
  - — nenhuma
- **Resultado:** —

#### 08 - Privacy e PII em logs   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 301 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E3, P1
- **Score:** 10/12
- **Plano de execução:**
  - — nenhuma
- **Resultado:** —
