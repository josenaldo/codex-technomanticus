---
title: "Roadmap — Spec-Driven Development"
created: 2026-07-02
type: meta
publish: false
tags:
  - meta
  - roadmap
---

# Roadmap — Spec-Driven Development

Diagnóstico migrado de guia/roadmap - ia.md (30/06). Cada entrada tem estado de enriquecimento, score, classificação de custo e plano de execução acionável.

**Galho:** `03-Dominios/Tecnologia/IA/Spec-Driven Development`

> [!warning] Diagnóstico de 30/06 — pode estar defasado. Vários itens marcados ⬜ podem já ter sido enriquecidos depois; reconciliar com o estado real ao tratar o galho.

## Régua de análise

Checklist `verificar-nota` — 12 itens (isenções por fase/tipo/broto aplicadas por nota):

| Grupo | Itens |
|-------|-------|
| ESTRUTURA | E1 TL;DR · E2 Abertura-problema · E3 Mermaid · E4 Casos práticos · E5 O que vem a seguir · E6 Inglês · E7 Tabela PT↔EN · E8 Armadilhas [!warning] |
| PROFUNDIDADE | P1 Código-com-falha · P2 Mecanismo explicado |
| LINKS | L1 Wikilink cross-galho · L2 Referência externa (URL) |
| MÍDIA | M1 Vídeo/podcast embutido |

**Esquema de fase detectado:** SEM fase (sequência)
**Piso de linhas:** N/A

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 12 |
| ⬜ pendente | 12 |
| ➖ não precisa | 0 |
| ✅ feita | 0 |
| 🔄 em andamento | 0 |
| % concluído | 0% |

---

## Notas

#### 01 - O problema do vibe coding em produção   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 401 linhas · fase: ausente · status: evergreen
- **Núcleo/gaps:** E5, E6, E7, P1, L2
- **Score:** 7/12
- **Plano de execução:**
  - Adicionar seção "O que vem a seguir" apontando para [[02 - O que é Spec-Driven Development]] com motivação concreta
  - Adicionar seção "Como explicar em inglês" com tabela PT↔EN dos termos centrais (vibe coding, tech debt, spec, context drift, acceptance criteria, regression, blast radius, velocity mismatch, code review, hallucination)
  - Adicionar URLs reais às referências (arxiv:2512.11922, Veracode, GitClear, Augment Code)
- **Resultado:** —

#### 02 - O que é Spec-Driven Development   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 401 linhas · fase: ausente · status: evergreen
- **Núcleo/gaps:** E5, L2, E8, E6, E7
- **Score:** 6/12
- **Plano de execução:**
  - Adicionar seção "O que vem a seguir" apontando para [[03 - Níveis de rigor — spec-first, spec-anchored, spec-as-source]]
  - Adicionar URLs reais às referências (GitHub Blog Spec Kit, Augment Code, Microsoft for Developers, Martin Fowler, Amazon Kiro, OpenSpec, DeepLearning.AI)
  - Adicionar ≥3 callouts `[!warning]` individuais com armadilhas concretas (spec sem acceptance criteria mensuráveis, spec fora do repositório, outcomes misturados com decisões técnicas)
  - Adicionar seção "Como explicar em inglês" com tabela PT↔EN (especificação, contrato, critério de aceitação, source of truth, fora do escopo, versionamento, artefato, validação, entregável, rastreabilidade)
- **Resultado:** —

#### 03 - Níveis de rigor — spec-first, spec-anchored, spec-as-source   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 399 linhas · fase: ausente · status: evergreen
- **Núcleo/gaps:** E5, E6, E7, E8, P1, L2
- **Score:** 6/12
- **Plano de execução:**
  - Adicionar seção "O que vem a seguir" apontando para [[04 - Fase Specify — definindo outcomes e constraints]]
  - Adicionar URLs reais às 20+ referências sem hiperlinks (GitHub Blog, Kiro, Tessl, Martin Fowler)
  - Adicionar ≥3 callouts `[!warning]` individuais (spec-as-source sem cultura de spec-anchored, spec-first em projetos com mudança frequente, mistura de níveis sem registro arquitetural)
  - Adicionar seção "Como explicar em inglês" com tabela PT↔EN (spec estática, spec viva, spec como fonte, fonte autoritativa, critério de aceitação, drift de spec, rastreabilidade, código derivado, checklist de aceitação, versionamento)
- **Resultado:** —

#### 04 - Fase Specify — definindo outcomes e constraints   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 407 linhas · fase: ausente · status: evergreen
- **Núcleo/gaps:** E5, L2, E8
- **Score:** 7/12
- **Plano de execução:**
  - Adicionar parágrafo "O que vem a seguir" apontando para [[05 - Fase Design e Plan — arquitetura e decomposição]]
  - Adicionar URLs reais a pelo menos 1 referência (Augment Code, GitHub Spec Kit)
  - Adicionar ≥2 callouts `[!warning]` adicionais (spec sem out-of-scope declarado, open questions não documentadas)
- **Resultado:** —

#### 05 - Fase Design e Plan — arquitetura e decomposição   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 420 linhas · fase: ausente · status: evergreen
- **Núcleo/gaps:** E5, L2, E8, L1, E6, E7
- **Score:** 5/12
- **Plano de execução:**
  - Adicionar parágrafo "O que vem a seguir" apontando para [[06 - Fase Implement — execução disciplinada]]
  - Adicionar URLs reais a pelo menos 1 referência (Microsoft, Nygard ADR)
  - Converter a seção "Anti-patterns" (tabela com 7 itens) para callouts `[!warning]` individuais
  - Adicionar wikilink cross-galho pertinente ([[Context Engineering]] ou [[Economia de Tokens]])
  - Adicionar seção "Como explicar em inglês" + tabela PT↔EN (spec, plan, ADR, task, acceptance criteria, decomposition, dependency, interface, component, constraint)
- **Resultado:** —

#### 06 - Fase Implement — execução disciplinada   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 393 linhas · fase: ausente · status: evergreen
- **Núcleo/gaps:** E5, L2, E8, L1, E6, E7
- **Score:** 5/12
- **Plano de execução:**
  - Adicionar seção "O que vem a seguir" apontando para [[07 - Fase Validate — spec como contrato executável]]
  - Adicionar URLs reais a pelo menos 1 referência (Forsgren et al. *Accelerate*, DORA 2025)
  - Converter a tabela "Anti-patterns da fase Implement" (8 itens) para callouts `[!warning]` individuais
  - Adicionar wikilink cross-galho pertinente ([[Context Engineering]] ou [[Economia de Tokens]])
  - Adicionar seção "Como explicar em inglês" + tabela PT↔EN (spec, plan, task, acceptance criteria, test-first, spec drift, atomic task, scope creep, commit traceability, spec-anchored)
- **Resultado:** —

#### 07 - Fase Validate — spec como contrato executável   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 395 linhas · fase: ausente · status: evergreen · progress: complete
- **Núcleo/gaps:** E5, E6, E7, E8, P1, L1, L2
- **Score:** 6/12
- **Plano de execução:**
  - Adicionar seção "O que vem a seguir" apontando para [[08 - Ferramentas SDD — Kiro, Spec Kit, OpenSpec, Tessl]]
  - Adicionar URLs reais a ≥1 referência (arxiv:2512.08769, k6, OWASP Zap)
  - Converter a tabela "Anti-patterns na fase Validate" (7 itens) para callouts `[!warning]` individuais
  - Adicionar wikilink cross-galho pertinente ([[Economia de Tokens]] ou [[Context Engineering]])
  - Adicionar seção "Como explicar em inglês" + tabela PT↔EN (validação, contrato executável, critério de aceitação, desvio/drift, cobertura, pipeline de CI, gate de qualidade, NFR, detecção de drift, especificação viva)
- **Resultado:** —

#### 08 - Ferramentas SDD — Kiro, Spec Kit, OpenSpec, Tessl   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 361 linhas · fase: ausente · status: evergreen
- **Núcleo/gaps:** E5, E6, E7, E8, P1, L2
- **Score:** 6/12
- **Plano de execução:**
  - Adicionar parágrafo "O que vem a seguir" apontando para [[09 - SDD com agentes — coordinator, implementor, validator]]
  - Adicionar URLs reais nas referências (github.com/github/spec-kit, kiro.dev, martinfowler.com)
  - Adicionar ≥3 callouts `[!warning]` com armadilhas concretas (Kiro e Spec Kit em paralelo, Tessl exige domínio formalmente modelável, Kiro sem steering files)
  - Adicionar `[!warning]` de caducidade (stars do Spec Kit, end-of-support Q Developer, recomendação datada jun/2026) nas seções "GitHub Spec Kit" e "A recomendação de start"
- **Resultado:** —

#### 09 - SDD com agentes — coordinator, implementor, validator   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 419 linhas · fase: ausente · status: evergreen
- **Núcleo/gaps:** E5, L2, E8, L1, E6, E7
- **Score:** 5/12
- **Plano de execução:**
  - Adicionar seção "O que vem a seguir" apontando para [[10 - Integração com context engineering — specs como contexto persistente]]
  - Adicionar URLs reais nas referências (arxiv:2512.08769, Anthropic Claude Agent SDK, Kiro custom subagents)
  - Adicionar ≥2 callouts `[!warning]` adicionais (DAG com paralelo_safe em tasks que compartilham arquivo, coordinator que recebe transcrição completa dos implementors)
  - Adicionar wikilink cross-galho pertinente ([[Economia de Tokens]] ou [[Context Engineering]])
  - Adicionar seção "Como explicar em inglês" + tabela PT↔EN (coordenador, implementador, validador, grafo acíclico dirigido, isolamento de contexto, tarefa, critério de aceitação, paralelismo, replanejamento, escalonamento)
- **Resultado:** —

#### 10 - Integração com context engineering — specs como contexto persistente   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 401 linhas · fase: ausente · status: evergreen
- **Núcleo/gaps:** E5, E6, E7, E8, P1, L1, L2
- **Score:** 6/12
- **Plano de execução:**
  - Adicionar parágrafo "O que vem a seguir" apontando para [[11 - Guia de implementação SDD — do zero ao projeto]]
  - Adicionar URLs nas referências (Kiro, Anthropic context engineering, Augment Code)
  - Adicionar wikilink cross-galho para [[Context Engineering]]
  - Converter a tabela "Anti-patterns na integração" (8 itens) para ≥3 callouts `[!warning]` individuais (spec gigantesca >3K tokens, compactação que toca spec, spec retroativa falsa)
  - Adicionar seção "Como explicar em inglês" + tabela PT↔EN (especificação, contexto persistente, recuperação cirúrgica, compactação, âncora de contexto, região protegida, drift de especificação, arquivo de agentes, tarefa, memória externa)
- **Resultado:** —

#### 11 - Guia de implementação SDD — do zero ao projeto   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 431 linhas · fase: ausente · status: evergreen
- **Núcleo/gaps:** E2, E5, L2, E8, E3, E6, E7
- **Score:** 4/12
- **Plano de execução:**
  - Adicionar parágrafo de abertura com problema/cenário antes de "Pré-requisitos" (você leu sobre SDD, mas como começa na prática?)
  - Adicionar seção "O que vem a seguir" apontando para [[12 - Debates — spec-as-source vs pragmatismo]]
  - Adicionar URLs reais às referências (GitHub Blog, Microsoft for Developers, Augment Code, Zencoder, DeepLearning.AI/JetBrains, BMAD, Hashrocket)
  - Expandir para ≥3 callouts `[!warning]` individuais (adoção parcial contamina o restante, spec retroativa descreve bugs como desejados, task grande demais quebra a regra das 3h)
  - Adicionar ≥1 diagrama Mermaid (flowchart das semanas 0→12 ou sequenceDiagram spec→plan→tasks→implement→gate)
  - Adicionar seção "Como explicar em inglês" + tabela PT↔EN (especificação, critério de aceitação, desvio, âncora, validação, tarefa, granularidade, adoção incremental, retroativa, manutenção de spec)
- **Resultado:** —

#### 12 - Debates — spec-as-source vs pragmatismo   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 401 linhas · fase: ausente · status: evergreen
- **Núcleo/gaps:** E5, L2, L1, E8
- **Score:** 5/12
- **Plano de execução:**
  - Adicionar seção "O que vem a seguir" com ponte narrativa para outros galhos de IA ([[Agentes de Codificação]], [[Context Engineering]], [[Prompt Engineering]])
  - Adicionar URLs reais às 14 referências (arxiv:2512.11922, arxiv:2506.14981, Andrej Karpathy, Salesforce Ben, Augment Code, Martin Fowler, Simon Willison, ThoughtWorks Radar, Stack Overflow Developer Survey 2026)
  - Adicionar ≥1 wikilink cross-galho na "Posição de fechamento" ou no corpo ([[Agentes de Codificação]] ou [[Context Engineering]])
  - Converter ≥3 limites/armadilhas da seção "Quando o método te trai" para callouts `[!warning]` individuais
- **Resultado:** —
