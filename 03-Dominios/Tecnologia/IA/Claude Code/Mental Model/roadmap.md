---
title: "Roadmap — Mental Model"
created: 2026-07-02
type: meta
publish: false
tags:
  - meta
  - roadmap
---

# Roadmap — Mental Model

Diagnóstico nota a nota. Cada entrada tem estado de enriquecimento, score, classificação
de custo e plano de execução acionável. Gerado por `/diagnosticar-galho`.

**Galho:** `03-Dominios/Tecnologia/IA/Claude Code/Mental Model`
**Nível:** galho-folha
**Diagnóstico:** 2026-07-02
**Última execução:** —

## Régua de análise

Checklist `verificar-nota` — 12 itens (isenções por fase/tipo/broto aplicadas por nota):

| Grupo | Itens |
|-------|-------|
| ESTRUTURA | E1 TL;DR · E2 Abertura-problema · E3 Mermaid · E4 Casos práticos · E5 O que vem a seguir · E6 Inglês · E7 Tabela PT↔EN · E8 Armadilhas [!warning] |
| PROFUNDIDADE | P1 Código-com-falha · P2 Mecanismo explicado |
| LINKS | L1 Wikilink cross-galho · L2 Referência externa (URL) |
| MÍDIA | M1 Vídeo/podcast embutido |

**Esquema de `fase:` detectado:** SEM fase (sequência 01→09)
**Piso de linhas:** não aplicável

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 9 |
| ⬜ pendente | 9 |
| ➖ não precisa | 0 |
| ✅ feita | 0 |
| % concluído | 0% |

> Diagnóstico concluído em 2026-07-02. Custo: 9 `[substantivo]` · 0 `[mecânico]`.

---

## Notas

#### 01 - O loop agentic   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 401 linhas reais · fase: ausente · status: growing
- **Núcleo/gaps:** E4, E5, E8, M1
- **Score:** 8/12
- **Plano de execução:**
  - Adicionar `## Casos práticos` com ≥2 cenários de produção reais (ex: debugging de CI headless, refactor multi-agent em paralelo) — ativa E4
  - Substituir `## Veja também` (ou adicionar antes dela) uma `## O que vem a seguir` com ponte narrativa pro próximo tema, citando `[[02 - Como Claude Code lê um codebase]]` — ativa E5
  - Converter os 4 itens de `## Armadilhas comuns` em callouts `[!warning]` (hoje são apenas negrito) — ativa E8
  - Pesquisar e embutir vídeo/podcast relevante sobre agentic loop/ReAct como `[!tip]` — ativa M1
- **Resultado:** —

#### 02 - Como Claude Code lê um codebase   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 399 linhas reais · fase: ausente · status: growing
- **Núcleo/gaps:** E3, E4, E5, E8, L2, M1
- **Score:** 7/13 (rubrica lista 13 itens, não 12; P1 não é N/A — há código)
- **Plano de execução:**
  - Converter um dos diagramas ASCII (ex: hierarquia de CLAUDE.md ou passos de exploração) em bloco ```mermaid``` → ativa E3
  - Adicionar `## Casos práticos` com 2 cenários de produção reais (ex: monorepo grande, projeto legado sem CLAUDE.md) → ativa E4
  - Adicionar `## O que vem a seguir` com ponte narrativa + wikilink pra próxima nota (03 - Tool use), substituindo/complementando "Veja também" → ativa E5
  - Reformular `## Armadilhas comuns` como ≥3 callouts `[!warning]` (hoje são blocos em negrito sem callout) → ativa E8
  - Renomear/restruturar `## Referências` para `## Fontes` (URLs já existem, só formalizar seção) → ativa L2
  - Pesquisar e embutir `[!tip]` com vídeo/podcast sobre navegação de codebase por agente/Claude Code → ativa M1
- **Resultado:** —

#### 03 - Tool use   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 402 linhas reais · fase: ausente · status: growing
- **Núcleo/gaps:** E4, E5, E8, L2, M1
- **Score:** 7/12
- **Plano de execução:**
  - Adicionar seção `## Casos práticos` com ≥2 cenários de produção (ex: agente lendo `.env` por acidente, `Bash` verboso estourando contexto num CI) → ativa E4
  - Substituir `## Veja também` por `## O que vem a seguir` com ponte narrativa e wikilink pra próxima nota do galho → ativa E5
  - Converter os itens de `## Armadilhas comuns` em ≥3 callouts `[!warning]` (hoje são blocos em negrito sem callout) → ativa E8
  - Renomear `## Referências` para `## Fontes` (conteúdo de URLs já existe, só falta o cabeçalho canônico) → ativa L2
  - Pesquisar e embutir um `[!tip]` com vídeo/podcast real sobre tool use / function calling em agentes → ativa M1
- **Resultado:** —

#### 04 - Context window   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 398 linhas reais · fase: ausente · status: growing
- **Núcleo/gaps:** E4, E5, E8, M1
- **Score:** 8/12
- **Plano de execução:**
  - Adicionar `## Casos práticos` com ≥2 cenários de produção (debugging longo, pipeline CI/CD) — ativa E4
  - Adicionar `## O que vem a seguir` com ponte narrativa e wikilink pra próxima nota (06 - Compaction) — ativa E5
  - Converter os 4 itens de "Armadilhas comuns" em callouts `[!warning]` — ativa E8
  - Pesquisar e embutir vídeo/podcast sobre gestão de context window em callout `[!tip]` — ativa M1
- **Resultado:** —

#### 05 - Modos de operação   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 400 linhas reais · fase: ausente · status: growing
- **Núcleo/gaps:** E4 (sem `## Casos práticos`), E5 (sem `## O que vem a seguir`, só `## Veja também`), E8 (seção "Armadilhas por modo" não usa callouts `[!warning]`), L2 (seção é `## Referências`, não `## Fontes`), M1 (nenhum `[!tip]` com vídeo/podcast)
- **Score:** 7/12
- **Plano de execução:**
  - Renomear "Composição de modos em workflows reais" (ou extrair 2 cenários dela) para `## Casos práticos` com 2 cenários de produção explícitos → ativa E4
  - Adicionar seção `## O que vem a seguir` com ponte narrativa + wikilink pra próxima nota do galho (ex.: índice Mental Model ou Workflows/01) → ativa E5
  - Converter os 5 blocos de "Armadilhas por modo" em callouts `> [!warning]` (renomear título para "Armadilhas comuns") → ativa E8
  - Renomear `## Referências` para `## Fontes` (conteúdo de URLs já está pronto) → ativa L2
  - Pesquisar e embutir vídeo/podcast real sobre plan mode/headless/auto mode do Claude Code como `[!tip]` → ativa M1
- **Resultado:** —

#### 06 - Compaction   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 400 linhas reais · fase: ausente · status: growing
- **Núcleo/gaps:** E4, E5, E8, M1
- **Score:** 8/12
- **Plano de execução:**
  - Adicionar `## Casos práticos` com ≥2 cenários de produção (ex: migração multi-dia com compaction repetida, debugging longo perdendo contexto de erro) → ativa E4
  - Adicionar `## O que vem a seguir` com ponte narrativa + wikilink pra próxima nota (ex: "05 - Modos de operação" ou índice do galho) → ativa E5
  - Criar `## Armadilhas comuns` convertendo o checklist/gotchas existentes em ≥3 callouts `[!warning]` → ativa E8
  - Pesquisar e embutir `[!tip]` com vídeo/podcast sobre compaction ou gerenciamento de contexto longo em agentes → ativa M1
- **Resultado:** —

#### 07 - Tokens e custo   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 397 linhas reais · fase: ausente · status: growing
- **Núcleo/gaps:** E4, E5, E8, L2, M1
- **Score:** 7/12
- **Plano de execução:**
  - Adicionar `## Casos práticos` com ≥2 cenários de produção nomeados → ativa E4
  - Adicionar `## O que vem a seguir` com ponte narrativa (não só links) apontando pra próxima nota → ativa E5
  - Converter parágrafos de "## Armadilhas" em ≥3 callouts `[!warning]` → ativa E8
  - Renomear/fundir `## Referências` em `## Fontes` (ou adicionar `## Fontes` com as URLs) → ativa L2
  - Pesquisar e embutir `[!tip]` com vídeo/podcast real sobre custo/tokens do Claude Code → ativa M1
- **Resultado:** —

#### 08 - Como o agente decide   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 371 linhas reais · fase: ausente · status: growing
- **Núcleo/gaps:** E4, E5, E8, L2, M1
- **Score:** 6/11 (P1 N/A — nota conceitual pura)
- **Plano de execução:**
  - Adicionar `## Casos práticos` com ≥2 cenários de produção (agente decidindo em situações reais) → ativa E4
  - Adicionar `## O que vem a seguir` com ponte narrativa + wikilink pra próxima nota → ativa E5
  - Converter `## Armadilhas` em ≥3 callouts `[!warning]` → ativa E8
  - Renomear/reestruturar `## Referências` para `## Fontes` (URLs já existem e são clicáveis) → ativa L2
  - Adicionar `[!tip]` com vídeo/podcast relevante sobre raciocínio do agente/prompting → ativa M1
- **Resultado:** —

#### 09 - O harness como terceira camada   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 377 linhas reais · fase: ausente · status: growing
- **Núcleo/gaps:** E4, E5, E8, M1
- **Score:** 8/12
- **Plano de execução:**
  - Adicionar `## Casos práticos` com ≥2 cenários de produção reais (harness em codebase grande, harness em time distribuído) → ativa E4
  - Adicionar `## O que vem a seguir` com ponte narrativa (não só lista de links) apontando pro próximo galho/nota da trilha → ativa E5
  - Converter `## Armadilhas` de bullets em bold para `## Armadilhas comuns` com ≥3 callouts `[!warning]` → ativa E8
  - Pesquisar e embutir ≥1 `[!tip]` com vídeo/podcast sobre harness engineering / Claude Code em escala → ativa M1
- **Resultado:** —
