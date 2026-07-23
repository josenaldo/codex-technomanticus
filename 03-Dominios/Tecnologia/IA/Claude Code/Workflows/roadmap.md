---
title: "Roadmap — Workflows"
created: 2026-07-02
type: meta
publish: false
tags:
  - meta
  - roadmap
---

# Roadmap — Workflows

Roadmap **de galho-pai**: mapeia as **notas diretas** (agora 11: sequência 01→10 + 12) e o
**sub-galho** `11 - Estratégias estruturais de contexto`. Gerado por `/diagnosticar-galho`.

**Galho:** `03-Dominios/Tecnologia/IA/Claude Code/Workflows`
**Nível:** galho-pai (contém sub-galho)
**Diagnóstico:** 2026-07-02
**Última execução:** 2026-07-08 (COMPLETO: 9/9 notas diretas acionáveis ✅ + sub-galho 11 4/4 ✅; 07 dispensada)
**Nota 12 adicionada:** 2026-07-21 (fora do ciclo de `/enriquecer-galho`; ainda não passou por diagnóstico/auditoria)

**Esquema de `fase:` detectado:** COM fase (Adepto nas 10 diretas originais; nota 12 é Magus; sub-galho 11 misto)
**Piso de linhas:** Iniciado ≥300 · Adepto ≥400 · Magus ≥500

## Tabela-resumo (notas diretas)

| Métrica | Valor |
|---------|-------|
| Notas diretas | 11 |
| ⬜ pendente (não auditada) | 1 (nota 12) |
| ➖ não precisa | 1 |
| ✅ feita | 9 |
| Custo | 9 `[substantivo]` · 1 `[mecânico]` · 1 `[não avaliado]` |

## Sub-galhos

| Sub-galho | Notas | Estado | roadmap |
|-----------|-------|--------|---------|
| 11 - Estratégias estruturais de contexto | 4 | ✅ completo (4 ✅ · 100%, 2026-07-08) | ✓ [[11 - Estratégias estruturais de contexto/roadmap\|roadmap]] |

---

## Notas diretas

#### 01 - Plan Mode   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-08)
- **Estado:** 400 linhas reais · fase: Adepto · status: growing
- **Núcleo/gaps:** L2 (seção chama-se "Referências", não "## Fontes"), M1 (nenhum [!tip] com link de vídeo/podcast)
- **Score:** 10/12
- **Plano de execução:**
  - Renomear/ajustar `## Referências` para `## Fontes` (ou adicionar seção `## Fontes` equivalente) → ativa L2
  - Pesquisar e embutir vídeo/podcast relevante sobre Plan Mode em callout `[!tip]` → ativa M1
- **Resultado:** L2 (Referências→Fontes), M1 (vídeo Plan Mode / Senior Engineer's Workflow) aplicados. 403 linhas. Sem desvios (updated não bumpado — omissão menor).

#### 02 - TDD com Claude Code   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-08)
- **Estado:** 398 linhas reais · fase: Adepto · status: growing
- **Núcleo/gaps:** L2 (seção chama-se "Referências", não "Fontes"), M1 (sem [!tip] com vídeo/podcast), piso Adepto (398 < 400)
- **Score:** 10/12
- **Plano de execução:**
  - Renomear "## Referências" para "## Fontes" (mantendo as URLs já clicáveis) → ativa L2
  - Pesquisar e embutir um [!tip] com vídeo/podcast sobre TDD com agentes de IA → ativa M1
  - Expandir levemente (ex: 1 parágrafo em "Cobertura guiada" ou nos casos práticos) para superar o piso de 400 linhas do Adepto
- **Resultado:** L2 (Referências→Fontes), M1 (vídeo Matt Pocock, skill TDD), expansão (400→405 linhas, piso Adepto) aplicados. 11/11 aplicáveis. Sem desvios.

#### 03 - Refactoring pesado   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-08)
- **Estado:** 391 linhas reais · fase: Adepto · status: growing
- **Núcleo/gaps:** L2 (seção chama-se "## Referências", não "## Fontes"), M1 (nenhum [!tip] com vídeo/podcast)
- **Score:** 11/13
- **Plano de execução:**
  - Renomear "## Referências" para "## Fontes" (conteúdo de URLs já qualifica) → ativa L2
  - Pesquisar e embutir vídeo/podcast relevante sobre refactoring pesado com agentes de IA como `[!tip]` → ativa M1
- **Resultado:** L2 (Referências→Fontes), M1 (talk Robert Brennan / OpenHands, refactors paralelos) aplicados. 408 linhas; ~12/12. Sem desvios.

#### 04 - Debugging complexo   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-08)
- **Estado:** 363 linhas reais · fase: Adepto · status: growing
- **Núcleo/gaps:** M1 (sem `[!tip]` com vídeo/podcast) · piso Adepto: 363<400 linhas
- **Score:** 11/12
- **Plano de execução:**
  - Buscar e embutir vídeo/podcast real sobre debugging complexo com agentes de IA como `[!tip]` → ativa M1
  - Expandir levemente uma seção existente (ex: aprofundar "Debugging em produção" ou casos práticos) para superar o piso de 400 linhas Adepto
- **Resultado:** M1 (podcast How I AI / harness Sentry), expansão "Debugging em produção" (amostragem + feature flag). DESVIO registrado: nota tem ~38 linhas em branco de padding no final; conteúdo real 363→389 (ainda <400 se medido por conteúdo), total wc-l 401→427. Piso a revisitar numa próxima rodada (podar padding + expandir ~11 linhas de conteúdo).

#### 05 - Code review   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-08)
- **Estado:** 367 linhas reais · fase: Adepto · status: growing
- **Núcleo/gaps:** M1 (sem [!tip] com vídeo/podcast) · piso de linhas Adepto não atingido (367 < 400)
- **Score:** 11/12 (M1 ausente)
- **Plano de execução:**
  - Buscar e embutir 1 vídeo/podcast relevante sobre code review com Claude Code (`/adicionar-midia`) — ativa M1
  - Expandir levemente uma seção existente (ex: "Review como hábito de equipe" ou "Review vs. linting") para cruzar o piso de 400 linhas de Adepto
- **Resultado:** M1 (vídeo Claude Code Review Agent open-source), expansão "Review como hábito de equipe" (2 parágrafos) aplicados. 409 linhas (piso Adepto ✓). Sem desvios.

#### 06 - Sessões paralelas   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-08)
- **Estado:** 333 linhas reais · fase: Adepto · status: growing
- **Núcleo/gaps:** piso de linhas (333 < 400 Adepto), L2 (seção chama-se "## Referências", não "## Fontes"), M1 (sem [!tip] de vídeo/podcast)
- **Score:** 10/12
- **Plano de execução:**
  - Renomear "## Referências" para "## Fontes" — ativa L2
  - Pesquisar e embutir um `[!tip]` com vídeo/podcast sobre worktrees + Claude Code/tmux — ativa M1
  - Expandir conteúdo (ex.: aprofundar "Setup com tmux" ou "Limpeza de worktrees") até atingir o piso de 400 linhas da fase Adepto
- **Resultado:** L2 (Referências→Fontes), M1 (vídeo "Git Worktrees Explained — Run Multiple AI Agents in Parallel" + ferramenta workmux), expansão "Setup com tmux" (tmux-resurrect) e "Limpeza de worktrees" (ciclo de vida + script) aplicados. 333→414 linhas reais (piso Adepto ✓). 11/11 aplicáveis. Sem desvios.

#### 07 - Sub-agents e dispatch   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 314 linhas reais · fase: Adepto · status: growing
- **Núcleo/gaps:** L2 (heading é "## Referências", não "## Fontes"), M1 (sem [!tip] de vídeo/podcast)
- **Score:** 10/12
- **Plano de execução:**
  - — nenhuma
- **Resultado:** —

#### 08 - Multi-agent   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-08)
- **Estado:** 365 linhas reais · fase: Adepto · status: growing
- **Núcleo/gaps:** M1 (sem [!tip] de vídeo/podcast) · piso de linhas (365 < 400 Adepto)
- **Score:** 11/12
- **Plano de execução:**
  - Pesquisar e embutir ≥1 [!tip] com vídeo/podcast sobre multi-agent/orchestrator-worker no Claude Code → ativa M1
  - Expandir caso prático ou seção "Por que funciona" com mais detalhe/exemplo pra fechar o piso de 400 linhas → resolve gap de piso
- **Resultado:** M1 (vídeo "How to Build Multi-Agent Teams in Claude Code"), expansão "Por que funciona" com exemplo trabalhado (sessão longa vs multi-agent, Registro Feynman); podadas ~37 linhas de padding. 366→422 linhas reais (piso Adepto ✓). Sem desvios. /verificar-nota não rodado no modo --auto.

#### 09 - Prompting para Claude Code   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-08)
- **Estado:** 352 linhas reais · fase: Adepto · status: growing
- **Núcleo/gaps:** L2 (seção chama-se "## Referências", não "## Fontes"), M1 (nenhum `[!tip]` com vídeo/podcast), piso Adepto ≥400 não atingido (352 linhas)
- **Score:** 10/12
- **Plano de execução:**
  - Renomear `## Referências` para `## Fontes` → ativa L2
  - Pesquisar e embutir vídeo/podcast relevante sobre prompting para agentes de código em `[!tip]` → ativa M1
  - Expandir conteúdo (mais um caso prático ou aprofundar mecanismo) para atingir piso de 400 linhas → fecha gap de piso
- **Resultado:** L2 (Referências→Fontes), M1 (vídeo Anthropic "Prompting 101 | Code w/ Claude"), "Caso 4: decompor tarefa grande em etapas verificáveis" (~55 linhas, Registro Feynman); podadas ~50 linhas de padding. 353→412 linhas reais (piso Adepto ✓). Sem desvios.

#### 10 - Gestão de contexto   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-08)
- **Estado:** 316 linhas reais · fase: Adepto · status: growing
- **Núcleo/gaps:** piso de linhas (316 < 400 para Adepto), M1
- **Score:** 11/12
- **Plano de execução:**
  - Expandir com ângulo adicional (ex: gestão de contexto multi-agent, ou métricas de quando o contexto está "cheio") para atingir o piso Adepto ≥400 linhas — cita piso de linhas
  - Adicionar callout `[!tip]` com vídeo/podcast sobre context management em agentes de IA — ativa M1
- **Resultado:** Ângulo métricas (seção "quando o contexto está objetivamente cheio" — `/context`, limiares ~50%/~80%) + ângulo multi-agent (isolamento via sub-agents, dado 90,2% Anthropic, Mermaid, cross-links notas 07/08). M1 (vídeo Matt Pocock "Most devs don't understand how context windows work"). 316→401 linhas reais (piso Adepto ✓); podadas ~85 linhas de padding. Sem desvios.

#### 12 - Orquestração em grafo — fan-out, arestas e verificadores   [não avaliado]
- **Enriquecimento:** ⬜ pendente — nota escrita do zero em 2026-07-21, fora do ciclo de `/enriquecer-galho`; ainda não passou por `/diagnosticar-galho` nem por `/verificar-nota`
- **Estado:** ~445 linhas reais · fase: Magus · status: seedling
- **Núcleo/gaps:** cobre o que 07/08/10 não cobrem — topologia de grafo com dezenas/centenas de sub-agents (fan-out, diamante split→work→merge, roteamento em runtime, loop-until-dry, verificador na aresta, tiering de modelo por nó, barreira vs. fluxo sem barreira). Fonte primária é marketing técnico do X (não documentação); APIs concretas (`agent()`, `pipeline()`, `isolation:"worktree"`, `.claude/workflows/`, `/deep-research`, `ultracode`) verificadas contra `code.claude.com/docs/en/workflows` em 21/07/2026 — `parallel()` citado pela fonte primária NÃO foi localizado literalmente na doc oficial recuperada, marcado como não verificado na própria nota
- **Plano de execução:** rodar `/verificar-nota` numa próxima passada; considerar M1 (vídeo/podcast sobre dynamic workflows) se aplicável
- **Resultado:** —
