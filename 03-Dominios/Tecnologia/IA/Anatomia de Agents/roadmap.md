---
title: "Roadmap — Anatomia de Agents"
created: 2026-07-02
type: meta
publish: false
tags:
  - meta
  - roadmap
---

# Roadmap — Anatomia de Agents

Diagnóstico migrado de guia/roadmap - ia.md (30/06). Cada entrada tem estado de enriquecimento, score, classificação de custo e plano de execução acionável.

**Galho:** `03-Dominios/Tecnologia/IA/Anatomia de Agents`

> [!warning] Diagnóstico de 30/06 — pode estar defasado. Vários itens marcados ⬜ podem já ter sido enriquecidos depois; reconciliar com o estado real ao tratar o galho.

## Régua de análise

Checklist `verificar-nota` — 12 itens (isenções por fase/tipo/broto aplicadas por nota):

| Grupo | Itens |
|-------|-------|
| ESTRUTURA | E1 TL;DR · E2 Abertura-problema · E3 Mermaid · E4 Casos práticos · E5 O que vem a seguir · E6 Inglês · E7 Tabela PT↔EN · E8 Armadilhas [!warning] |
| PROFUNDIDADE | P1 Código-com-falha · P2 Mecanismo explicado |
| LINKS | L1 Wikilink cross-galho · L2 Referência externa (URL) |
| MÍDIA | M1 Vídeo/podcast embutido |

**Esquema de `fase:` detectado:** SEM fase (sequência)
**Piso de linhas:** N/A (sem fase)

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 11 |
| ⬜ pendente | 11 |
| ➖ não precisa | 0 |
| ✅ feita | 0 |
| 🔄 em andamento | 0 |
| % concluído | 0% |

---

## Notas

#### 01 - O que é um agent   [mecânico]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 190 linhas · fase: ausente · status: growing
- **Núcleo/gaps:** E5, L2, E8
- **Score:** 8/12
- **Plano de execução:**
  - Adicionar seção narrativa "O que vem a seguir" (antes de "## Ver mais") apontando para [[02 - O loop ReAct e native tool use]] com motivação concreta (o que define um agent → o mecanismo exato do loop, ReAct e tool calls nativas)
  - Adicionar URLs reais às referências em "## Referências" (Anthropic Building Effective Agents, OpenAI Practical Guide, ReAct paper arxiv, Lilian Weng blog)
  - Adicionar ≥2 callouts `[!warning]` adicionais com armadilhas concretas (chamar pipeline de agent não elimina fragilidade; max_steps sem limite como fonte de fatura inesperada)
- **Resultado:** —

#### 02 - O loop ReAct e native tool use   [mecânico]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 277 linhas · fase: ausente · status: growing
- **Núcleo/gaps:** E5, E8, P1
- **Score:** 9/12
- **Plano de execução:**
  - Adicionar seção narrativa "O que vem a seguir" apontando para [[03 - Tool design — princípios e categorias]] com motivação concreta (ritmo do loop ReAct vs. qualidade de cada passo dependendo do design das tools)
  - Converter os 4 pitfalls de "## Pitfalls do loop" (atualmente ### com prosa) para callouts `[!warning]` individuais
  - Opcional: extrair o snippet do bug da abertura (handler sem branch para `end_turn`) como bloco de código-com-falha seguido do fix
- **Resultado:** —

#### 03 - Tool design — princípios e categorias   [mecânico]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 264 linhas · fase: ausente · status: growing
- **Núcleo/gaps:** E5, E8
- **Score:** 10/12
- **Plano de execução:**
  - Adicionar seção narrativa "O que vem a seguir" apontando para `[[04 - Memory em agents]]` com motivação concreta (tool design certo → memória como próxima peça, sem a qual o agent refaz tool calls já executadas)
  - Converter a seção "## Anti-patterns" (5 itens em lista bullet) para callouts `[!warning]` individuais
- **Resultado:** —

#### 04 - Memory em agents   [mecânico]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 219 linhas · fase: ausente · status: growing
- **Núcleo/gaps:** E5, E8, L2
- **Score:** 8/12
- **Plano de execução:**
  - Adicionar seção narrativa "O que vem a seguir" apontando para [[05 - Planning — plan-then-execute, dynamic, hierarchical]] com motivação concreta (memória define o que o agent lembra; planning define o que ele faz com esse conhecimento)
  - Converter a seção "## Anti-patterns" (5 itens em lista bullet) para callouts `[!warning]` individuais
  - Adicionar URLs reais às referências em "## Ver mais" (MemGPT arxiv, Lilian Weng blog)
- **Resultado:** —

#### 05 - Planning — plan-then-execute, dynamic, hierarchical   [mecânico]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 249 linhas · fase: ausente · status: growing / progress: done
- **Núcleo/gaps:** E5, E8, P1, L2
- **Score:** 8/12
- **Plano de execução:**
  - Adicionar seção narrativa "O que vem a seguir" apontando para [[06 - Multi-agent — orchestrator e sub-agents]] com motivação concreta (planning ancora um único agent; tarefa grande demais exige orquestração de sub-agents)
  - Converter a seção "## Anti-patterns" (6 itens em lista bullet) para callouts `[!warning]` individuais
  - Adicionar URLs reais às referências em "## Ver mais" e "## Referências" (arxiv:2305.04091, arxiv:2305.10601, Anthropic Building Effective Agents)
- **Resultado:** —

#### 06 - Multi-agent — orchestrator e sub-agents   [mecânico]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 267 linhas · fase: ausente · status: growing
- **Núcleo/gaps:** E5, L2
- **Score:** 10/12
- **Plano de execução:**
  - Adicionar seção narrativa "O que vem a seguir" apontando para [[07 - Frameworks 2026]] com motivação concreta (quando/como orquestrar → quais frameworks de 2026 implementam o padrão nativamente e o que cada um sacrifica)
  - Adicionar URLs reais às referências em "## Ver mais" e "## Referências" (Anthropic Building Effective Agents, Claude Agent SDK docs, Augment Code CIV, VeriMAP EACL 2026, OpenAI Swarm)
  - Opcional: converter a seção "## Anti-patterns" (6 itens em lista bullet) para callouts `[!warning]` individuais
- **Resultado:** —

#### 07 - Frameworks 2026   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 319 linhas · fase: ausente · status: growing
- **Núcleo/gaps:** E5, E8
- **Score:** 9/12
- **Plano de execução:**
  - Adicionar seção narrativa "O que vem a seguir" apontando para [[08 - Patterns comuns de agents]] com motivação concreta (escolher/recusar framework → patterns que qualquer stack precisa implementar, com ou sem framework)
  - Converter a seção "## Anti-patterns" (5 itens em lista bullet) para callouts `[!warning]` individuais
  - Pesquisar e atualizar caducidade em "## O panorama em uma tabela" (rankings de popularidade, versões de Claude Agent SDK/Pydantic AI, estimativas de semanas-até-produção) e adicionar `[!info]`/`[!warning]` de validade dos dados
- **Resultado:** —

#### 08 - Patterns comuns de agents   [mecânico]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 251 linhas · fase: ausente · status: growing / progress: done
- **Núcleo/gaps:** E5, E8, L2
- **Score:** 8/12
- **Plano de execução:**
  - Adicionar seção narrativa "O que vem a seguir" apontando para a nota 09 do galho (Evaluation de agents)
  - Expandir o único `[!warning]` composto (5 sub-itens agrupados) em ≥3 callouts `[!warning]` individuais com título descritivo
  - Adicionar URLs reais às referências em "## Ver mais" e "## Referências" (Anthropic Building Effective Agents, OpenAI Practical Guide, LangChain blog supervisor patterns)
- **Resultado:** —

#### 09 - Evaluation de agents   [mecânico]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 278 linhas · fase: ausente · status: growing
- **Núcleo/gaps:** E5, E8
- **Score:** 9/12
- **Plano de execução:**
  - Adicionar seção "O que vem a seguir" com ponte narrativa para a nota 10 (Workflow vs Agent — quando usar cada um)
  - Converter os 6 bullets de "## Anti-patterns" em ≥3 callouts `[!warning]` individuais com título descritivo
- **Resultado:** —

#### 10 - Workflow vs Agent — quando usar cada um   [mecânico]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 190 linhas · fase: ausente · status: growing / progress: done
- **Núcleo/gaps:** E5, E8, P1
- **Score:** 9/12
- **Plano de execução:**
  - Adicionar seção narrativa "O que vem a seguir" com ponte para [[11 - Harness engineering — a terceira camada]] com motivação concreta (workflow-vs-agent escolhido → onde o código vive, o harness que envolve o loop com retry/tracing/cost guard/human-in-the-loop)
  - Converter a seção "## Custos e riscos" (5 bullets) para callouts `[!warning]` individuais com título descritivo
- **Resultado:** —

#### 11 - Harness engineering — a terceira camada   [mecânico]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 217 linhas · fase: ausente · status: growing / progress: done
- **Núcleo/gaps:** E5, E8, P1
- **Score:** 9/12
- **Plano de execução:**
  - Adicionar seção narrativa "O que vem a seguir", por ser a última nota do galho: fechar o ciclo de Anatomia de Agents e abrir pontes explícitas para os galhos que aprofundam dimensões do harness (Context Engineering = budget, Memória de Agentes = estado, Evaluation = loop de melhoria)
  - Adicionar ≥2 callouts `[!warning]` adicionais com armadilhas concretas (build to delete — hooks compensatórios podem trabalhar contra o próximo modelo; benchmarks sem HarnessCard medem variável confundida)
- **Resultado:** —
