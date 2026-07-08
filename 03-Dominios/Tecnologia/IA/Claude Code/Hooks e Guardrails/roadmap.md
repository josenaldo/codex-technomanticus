---
title: "Roadmap — Hooks e Guardrails"
created: 2026-07-02
type: meta
publish: false
tags:
  - meta
  - roadmap
---

# Roadmap — Hooks e Guardrails

Diagnóstico nota a nota. Cada entrada tem estado de enriquecimento, score, classificação
de custo e plano de execução acionável. Gerado por `/diagnosticar-galho`.

**Galho:** `03-Dominios/Tecnologia/IA/Claude Code/Hooks e Guardrails`
**Nível:** galho-folha
**Diagnóstico:** 2026-07-02
**Última execução:** 2026-07-07 (8/8 enriquecidas via fan-out ≤3)

## Régua de análise

Checklist `verificar-nota` — 12 itens (isenções por fase/tipo/broto aplicadas por nota):

| Grupo | Itens |
|-------|-------|
| ESTRUTURA | E1 TL;DR · E2 Abertura-problema · E3 Mermaid · E4 Casos práticos · E5 O que vem a seguir · E6 Inglês · E7 Tabela PT↔EN · E8 Armadilhas [!warning] |
| PROFUNDIDADE | P1 Código-com-falha · P2 Mecanismo explicado |
| LINKS | L1 Wikilink cross-galho · L2 Referência externa (URL) |
| MÍDIA | M1 Vídeo/podcast embutido |

**Esquema de `fase:` detectado:** SEM fase (sequência 01→08)
**Piso de linhas:** não aplicável

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 8 |
| ⬜ pendente | 0 |
| ➖ não precisa | 0 |
| ✅ feita | 8 |
| % concluído | 100% |

> Enriquecimento concluído em 2026-07-07 — 8/8 notas via fan-out ≤3 verificado. Custo: 8 `[substantivo]` · 0 `[mecânico]`.

---

## Notas

#### 01 - Sistema de hooks   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-07)
- **Estado:** 426 linhas reais · fase: ausente · status: growing
- **Núcleo/gaps:** E4, E5, E8, L2, M1
- **Score:** 7/12
- **Plano de execução:**
  - Renomear "## Exemplo real" para "## Casos práticos" e adicionar um segundo cenário de produção → ativa E4
  - Adicionar "## O que vem a seguir" com ponte narrativa + wikilink pra "02 - PreToolUse" → ativa E5
  - Extrair 3+ armadilhas (ex: hook sem timeout, matcher errado, hook silencioso) em "## Armadilhas comuns" com `[!warning]` → ativa E8
  - Renomear "## Referências" para "## Fontes" (mantendo URLs) → ativa L2
  - Pesquisar e embutir vídeo/podcast sobre Claude Code hooks em `[!tip]` → ativa M1
- **Resultado:** E4 (Casos práticos, cenário 2 observabilidade), E5 (ponte p/ 02), E8 (3 callouts `[!warning]`: sem timeout/matcher errado/silencioso), L2 (Referências→Fontes), M1 (vídeo IndyDevDan) aplicados. Score 12/12. 495 linhas.

#### 02 - PreToolUse   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-07)
- **Estado:** 577 linhas reais · fase: ausente · status: growing
- **Núcleo/gaps:** E4, E5, E8, L1, L2, M1
- **Score:** 6/12
- **Plano de execução:**
  - Criar `## Casos práticos` com ≥2 cenários de produção (reaproveitar "Exemplo real — PCI-DSS" + adicionar um segundo cenário) → ativa E4
  - Criar `## O que vem a seguir` com ponte narrativa e wikilink pra próxima nota (03 - PostToolUse) → ativa E5
  - Criar `## Armadilhas comuns` com ≥3 callouts `[!warning]` (reaproveitar o warning de aprovação interativa headless + extrair 2 novas armadilhas do texto: hooks sem timeout, exit code mal interpretado) → ativa E8
  - Adicionar ≥1 wikilink pra nota fora da pasta "Hooks e Guardrails" (ex: nota de Segurança Conceitual ou Anatomia dos LLMs relacionada) → ativa L1
  - Renomear `## Referências` para `## Fontes` (ou adicionar seção `## Fontes` equivalente) mantendo as URLs existentes → ativa L2
  - Pesquisar e embutir vídeo/podcast relevante sobre PreToolUse/hooks de segurança em agentes como `[!tip]` → ativa M1
- **Resultado:** E4 (PCI-DSS + kubectl delete em prod), E5 (ponte p/ 03), E8 (3 callouts `[!warning]`: headless/sem timeout/exit code), L1 (wikilink p/ Agentes de Codificação/17), L2 (Referências→Fontes), M1 (vídeo Hooks Deep Dive) aplicados. Score 12/12. 673 linhas.

#### 03 - PostToolUse   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-07)
- **Estado:** 506 linhas reais · fase: ausente · status: growing
- **Núcleo/gaps:** E4, E5, E8, L1, L2, M1
- **Score:** 6/12
- **Plano de execução:**
  - Agrupar/renomear os 7 "Caso de uso N" sob heading `## Casos práticos` → ativa E4
  - Adicionar seção `## O que vem a seguir` com ponte narrativa e wikilink pra próxima nota do galho (ex. 04 - Stop hook) → ativa E5
  - Converter os itens em negrito de `## Armadilhas` em ≥3 callouts `[!warning]` → ativa E8
  - Adicionar ≥1 wikilink pra nota fora da pasta "Hooks e Guardrails" (ex. algum conceito geral de Claude Code ou automação) → ativa L1
  - Renomear `## Referências` para `## Fontes` (mantendo as URLs já presentes) → ativa L2
  - Pesquisar e embutir vídeo/podcast relevante sobre PostToolUse hooks em `[!tip]` → ativa M1
- **Resultado:** E4 (7 casos sob Casos práticos), E5 (ponte p/ 04 - Stop hook), E8 (5 callouts `[!warning]`), L1 (wikilink p/ Time e Automação/02 CI-CD), L2 (Referências→Fontes), M1 (vídeo oficial Anthropic "Hooks in Claude Code", âncora [1:24]) aplicados. Desvio menor: vídeo de 3min (fonte oficial, sem alternativa dedicada). 506→~560 linhas.

#### 04 - Stop hook   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-07)
- **Estado:** 416 linhas reais · fase: ausente · status: growing
- **Núcleo/gaps:** E4 (seções "Caso de uso N" em vez de `## Casos práticos`), E5 (falta "O que vem a seguir"; só tem "Veja também"), E8 (checklist em vez de `## Armadilhas comuns` com `[!warning]`), L2 (seção chama-se "Referências", não "## Fontes"), M1 (nenhum `[!tip]` com vídeo/podcast)
- **Score:** 7/12
- **Plano de execução:**
  - Renomear/reagrupar as 6 seções "Caso de uso N" sob `## Casos práticos` (ou criar a seção e linkar as existentes) → ativa E4
  - Adicionar `## O que vem a seguir` com ponte narrativa e wikilink pra próxima nota do galho (ex: 08 - Testando hooks) → ativa E5
  - Converter itens de risco do checklist em `## Armadilhas comuns` com ≥3 callouts `[!warning]` (ex: cleanup destrutivo em interrupt, session log ausente, auto-commit fora de end_turn) → ativa E8
  - Renomear `## Referências` para `## Fontes` (URLs já existem e são clicáveis) → ativa L2
  - Pesquisar e embutir `[!tip]` com vídeo/podcast sobre Stop hook ou observabilidade de sessões Claude Code → ativa M1
- **Resultado:** E4 (6 casos sob Casos práticos), E5 (ponte p/ 08), E8 (3 callouts `[!warning]`: cleanup destrutivo/session log ausente/auto-commit), L2 (Referências→Fontes), M1 (vídeo IndyDevDan observabilidade) aplicados. Score 12/12. 445 linhas.

#### 05 - Guardrails   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-07)
- **Estado:** 396 linhas reais · fase: ausente · status: growing
- **Núcleo/gaps:** E4, E5, E8, L2, M1
- **Score:** 8/13 (rubrica lista 13 itens, não 12; nenhuma isenção aplicável — type concept, sem fase)
- **Plano de execução:**
  - Renomear "## Armadilhas" para "## Armadilhas comuns" e converter os 4 parágrafos em bold em callouts `[!warning]` → ativa E8
  - Adicionar "## O que vem a seguir" com ponte narrativa pro `[[06 - Delegar permissão]]` (hoje só há "Veja também") → ativa E5
  - Criar "## Casos práticos" com ≥2 cenários de produção nomeados (ex: incidente real de force-push, tentativa de DROP TABLE em CI) reaproveitando/expandindo os exemplos já existentes → ativa E4
  - Renomear "## Referências" para "## Fontes" (URLs já existem, só ajustar heading) → ativa L2
  - Pesquisar e embutir vídeo/podcast sobre guardrails/hooks de segurança em agentes de IA como `[!tip]` → ativa M1
- **Resultado:** E8 (4 callouts `[!warning]`), E5 (ponte p/ 06), E4 (force-push; DROP TABLE em CI), L2 (Referências→Fontes), M1 (vídeo NextWork guardrails, âncora [40:40], transcrição verificada) aplicados. Score ~11-12/12. Cenários com [!summary] de fecho.

#### 06 - Delegar permissão   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-07)
- **Estado:** 405 linhas reais · fase: ausente · status: growing
- **Núcleo/gaps:** E4, E5, E8, L1, M1
- **Score:** 7/12
- **Plano de execução:**
  - Adicionar seção `## Casos práticos` com ≥2 cenários de produção (deploy/staging, query SQL prod) → ativa E4
  - Adicionar `## O que vem a seguir` com ponte narrativa + wikilink pra próxima nota (07 - Segurança com hooks) → ativa E5
  - Converter os 4 parágrafos de `## Armadilhas` em callouts `[!warning]` → ativa E8
  - Trocar/adicionar ≥1 wikilink pra nota fora da pasta Hooks e Guardrails (ex: outro galho de Claude Code) → ativa L1
  - Pesquisar e embutir ≥1 `[!tip]` com vídeo/podcast sobre meta-agentes/LLM-as-judge → ativa M1
- **Resultado:** E4 (deploy staging/prod via kubectl; DELETE SQL em prod), E5 (ponte p/ 07), E8 (4 callouts `[!warning]`), L1 (wikilink p/ Mental Model/08), M1 (vídeo LLM-as-judge security) aplicados. Todos os 5 itens do plano.

#### 07 - Segurança com hooks   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-07)
- **Estado:** 409 linhas reais · fase: ausente · status: growing
- **Núcleo/gaps:** E4 (sem `## Casos práticos` dedicada), E5 (sem "O que vem a seguir" — só "Veja também"), E8 (Armadilhas em prosa, não callouts `[!warning]`, título sem "comuns"), L1 (wikilinks só dentro da própria pasta), L2 (seção é `## Referências`, não `## Fontes`), M1 (sem `[!tip]` de vídeo/podcast)
- **Score:** 7/13 (todos os itens aplicáveis; sem isenções)
- **Plano de execução:**
  - Renomear "Armadilhas" → `## Armadilhas comuns` e converter os 4 parágrafos em bold para callouts `[!warning]` → ativa E8
  - Adicionar `## O que vem a seguir` com ponte narrativa pra [[03-Dominios/Tecnologia/IA/Claude Code/Hooks e Guardrails/08 - Testando hooks|08 - Testando hooks]] → ativa E5
  - Adicionar `## Casos práticos` com ≥2 cenários de produção explícitos (ex: incidente de credencial vazada, force-push acidental) reaproveitando o conteúdo das camadas → ativa E4
  - Renomear `## Referências` → `## Fontes` (URLs já presentes) → ativa L2
  - Adicionar ≥1 wikilink pra nota fora da pasta (ex: nota de Git ou de segurança geral em Tecnologia) → ativa L1
  - Pesquisar e embutir `[!tip]` com vídeo/podcast real sobre segurança de agentes de IA/hooks → ativa M1
- **Resultado:** E8 (4 callouts `[!warning]`), E5 (ponte p/ 08), E4 (credencial AWS vazada; force-push acidental), L2 (Referências→Fontes), L1 (wikilink p/ Segurança e Guardrails/12), M1 (vídeo NextWork defesa em camadas) aplicados. 436 linhas. Todos os itens do plano.

#### 08 - Testando hooks   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-07)
- **Estado:** 699 linhas reais · fase: ausente · status: growing
- **Núcleo/gaps:** E4, E5, E8, L1, L2, M1
- **Score:** 6/12
- **Plano de execução:**
  - Adicionar `## Casos práticos` com ≥2 cenários de produção (ex: guardrail que falhou em CI real, hook Stop travando cleanup) → ativa E4
  - Adicionar `## O que vem a seguir` com ponte narrativa (não só lista) apontando para a próxima nota do galho → ativa E5
  - Converter os 7 itens de "Armadilhas comuns" em callouts `> [!warning]` (mínimo 3) → ativa E8
  - Adicionar ≥1 wikilink para nota fora da pasta Hooks e Guardrails (ex: nota de shell scripting ou CI/CD em outro galho) → ativa L1
  - Renomear `## Referências` para `## Fontes` (mantendo as URLs já clicáveis) → ativa L2
  - Pesquisar e embutir `[!tip]` com vídeo/podcast sobre testar hooks/shell scripts ou CI para bash → ativa M1
- **Resultado:** —
