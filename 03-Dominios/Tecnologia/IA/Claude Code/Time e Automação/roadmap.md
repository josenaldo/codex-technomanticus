---
title: "Roadmap — Time e Automação"
created: 2026-07-02
type: meta
publish: false
tags:
  - meta
  - roadmap
---

# Roadmap — Time e Automação

Diagnóstico nota a nota. Cada entrada tem estado de enriquecimento, score, classificação de custo e plano de execução acionável. Gerado por `/diagnosticar-galho`.

**Galho:** `03-Dominios/Tecnologia/IA/Claude Code/Time e Automação` **Nível:** galho-folha **Diagnóstico:** 2026-07-02 **Última execução:** 2026-07-08 (ondas 1-3: notas 01-08 ✅ — galho completo 8/8)

## Régua de análise

Checklist `verificar-nota` — 12 itens (isenções por fase/tipo/broto aplicadas por nota):

| Grupo | Itens |
|-------|-------|
| ESTRUTURA | E1 TL;DR · E2 Abertura-problema · E3 Mermaid · E4 Casos práticos · E5 O que vem a seguir · E6 Inglês · E7 Tabela PT↔EN · E8 Armadilhas [!warning] |
| PROFUNDIDADE | P1 Código-com-falha · P2 Mecanismo explicado |
| LINKS | L1 Wikilink cross-galho · L2 Referência externa (URL) |
| MÍDIA | M1 Vídeo/podcast embutido |

**Esquema de `fase:` detectado:** SEM fase (sequência 01→08) **Piso de linhas:** não aplicável

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 8 |
| ⬜ pendente | 0 |
| ➖ não precisa | 0 |
| ✅ feita | 8 |
| % concluído | 100% |

> Diagnóstico concluído em 2026-07-02. Custo: 8 `[substantivo]` · 0 `[mecânico]`.

---

## Notas

#### 01 - Headless mode   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-08)
- **Estado:** 424 linhas reais · fase: ausente (SEM fase) · status: evergreen
- **Núcleo/gaps:** E1 (TL;DR é 1 parágrafo denso, não ≥3 linhas), E4 (sem `## Casos práticos` dedicada — conteúdo prático existe mas espalhado), E5 (sem `## O que vem a seguir`), E7 (sem tabela PT↔EN — só bullets em inglês), E8 (`## Armadilhas` usa bold, não callouts `[!warning]`), L2 (sem `## Fontes` com URL externa), M1 (sem `[!tip]` de vídeo/podcast)
- **Score:** 6/13 (nenhum item isento — type concept, tem seção de código)
- **Plano de execução:**
  - Quebrar o TL;DR em ≥3 linhas cobrindo o quê/como/quando usar → ativa E1
  - Criar `## Casos práticos` com 2 cenários de produção (reaproveitar pipeline de revisão e monitoramento de custo já presentes) → ativa E4
  - Adicionar `## O que vem a seguir` com ponte narrativa + wikilink pra "02 - CI/CD com GitHub Actions" → ativa E5
  - Extrair tabela PT↔EN dos termos já usados na seção de inglês (headless, stdout, stdin, exit code, tool call) → ativa E7
  - Converter os 5 itens de `## Armadilhas` em callouts `[!warning]` → ativa E8
  - Pesquisar e adicionar `## Fontes` com URL oficial da doc de CLI/headless da Anthropic → ativa L2
  - Pesquisar vídeo/podcast sobre headless mode ou automação com Claude Code e embutir como `[!tip]` → ativa M1
- **Resultado:** E1 (TL;DR 3 linhas), E4 (2 cenários: pipeline-de-revisao + wrapper de custo), E5 (→ [[02]]), E7 (tabela PT↔EN 5 termos), E8 (5 → [!warning]), L2 (## Fontes 2 URLs oficiais Anthropic), M1 (vídeo headless automation, Sid Bidasaria) aplicados. 455 linhas. Sem desvios (título mantido `## Armadilhas`, conforme literal do plano).

#### 02 - CI-CD com GitHub Actions   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-08)
- **Estado:** 415 linhas reais · fase: ausente · status: evergreen
- **Núcleo/gaps:** E4, E5, E7, E8, L2, M1
- **Score:** 6/12
- **Plano de execução:**
  - Renomear "## Casos de uso em CI/CD" p/ "## Casos práticos" (já tem 4 cenários de produção) → ativa E4
  - Adicionar "## O que vem a seguir" com ponte narrativa + wikilink pra próxima nota do galho → ativa E5
  - Adicionar tabela PT↔EN de termos-chave (headless, workflow, runner, secret, etc.) → ativa E7
  - Renomear "## Armadilhas" p/ "## Armadilhas comuns" e converter os 5 itens em callouts `[!warning]` → ativa E8
  - Criar "## Fontes" com URL externa verificável (docs oficiais GitHub Actions + repo anthropics/claude-code-action) → ativa L2
  - Adicionar `[!tip]` com vídeo/podcast sobre CI/CD com Claude Code ou GitHub Actions com IA → ativa M1
- **Resultado:** E4 (renomeada ## Casos práticos, 4 cenários), E5 (→ [[03]]), E7 (tabela PT↔EN 8 termos), E8 (## Armadilhas comuns, 5 → [!warning]), L2 (## Fontes docs GitHub Actions + anthropics/claude-code-action; ## Referências internas preservadas), M1 (vídeo GitHub+Claude Code) aplicados. 416 → 440 linhas. Sem desvios.

#### 03 - Dispatch via claude -p   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-08)
- **Estado:** 464 linhas reais · fase: ausente · status: evergreen
- **Núcleo/gaps:** E5, E7, E8, L2, M1
- **Score:** 7/12
- **Plano de execução:**
  - Adicionar `## O que vem a seguir` com ponte narrativa + wikilink para a próxima nota do galho → ativa E5
  - Converter a seção de inglês numa tabela PT↔EN dos termos-chave (dispatch, fan-out, headless, exit code) → ativa E7
  - Transformar os 4 blocos de `## Armadilhas` em callouts `[!warning]` (hoje só 1 existe, dentro do caso de uso do commit hook) → ativa E8
  - Criar `## Fontes` com URL externa verificável (docs oficiais de `claude -p`/CLI reference da Anthropic) → ativa L2
  - Pesquisar e embutir `[!tip]` com vídeo/podcast sobre dispatch/automação com Claude Code → ativa M1
- **Resultado:** E5 (→ [[04]]), E7 (tabela PT↔EN 4 termos), E8 (4 → [!warning]), L2 (## Fontes 2 URLs oficiais Anthropic), M1 (vídeo headless automation) aplicados. 485 linhas; score 11/12 (T3 tamanho <500 Magus, fora do plano). Sem desvios.

#### 04 - CLAUDE.md compartilhado   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-08)
- **Estado:** 400 linhas reais · fase: ausente · status: evergreen
- **Núcleo/gaps:** E4, E5, E7, E8, L2, M1
- **Score:** 6/11 (P1 N/A — nota conceitual sobre formato de arquivo, sem código com caso-problema)
- **Plano de execução:**
  - Adicionar `## Casos práticos` com ≥2 cenários de produção (ex: onboarding de dev novo num monorepo real, CLAUDE.md que causou incidente por estar desatualizado) → ativa E4
  - Adicionar `## O que vem a seguir` com ponte narrativa para [[03-Dominios/Tecnologia/IA/Claude Code/Time e Automação/05 - Controle de custo|05 - Controle de custo]] → ativa E5
  - Adicionar tabela PT↔EN de termos-chave (shared CLAUDE.md, ownership, staleness, contract, guardrail) na seção de inglês → ativa E7
  - Converter os 8 blocos de "## Armadilhas" (negrito) em callouts `> [!warning]` (mínimo 3) → ativa E8
  - Criar `## Fontes` com ≥1 URL externa verificável (ex: docs oficiais da Anthropic sobre CLAUDE.md/memory) → ativa L2
  - Adicionar `[!tip]` com link de vídeo/podcast sobre CLAUDE.md compartilhado em times → ativa M1
- **Resultado:** E4 (2 cenários: onboarding monorepo + incidente por CLAUDE.md desatualizado), E5 (→ [[05]]), E7 (tabela PT↔EN 5 termos), E8 (8 → [!warning]), L2 (## Fontes doc oficial memory), M1 (podcast Team OS / DoorDash) aplicados. 439 linhas. Sem desvios.

#### 05 - Controle de custo   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-08)
- **Estado:** 395 linhas reais · fase: ausente · status: evergreen
- **Núcleo/gaps:** E4, E5, E7, E8, L2, M1
- **Score:** 6/12
- **Plano de execução:**
  - Adicionar `## Casos práticos` com ≥2 cenários de produção (ex: time real estourando budget, CI descontrolado) → ativa E4
  - Adicionar `## O que vem a seguir` com ponte narrativa + wikilink pra próxima nota do galho → ativa E5
  - Adicionar tabela PT↔EN dos termos-chave (token, cache hit, max-turns, gate, hard cap) → ativa E7
  - Converter os itens de `## Armadilhas` em callouts `[!warning]` (já há ≥6 candidatos) → ativa E8
  - Criar `## Fontes` com URL externa verificável (ex: docs oficiais de pricing/ccusage) → ativa L2
  - Pesquisar e embutir `[!tip]` com vídeo/podcast sobre otimização de custo de LLM/agentes → ativa M1
- **Resultado:** E4 (2 cenários: budget estourado + CI descontrolado), E5 (→ [[06]]), E7 (tabela PT↔EN 5 termos), E8 (7 → [!warning]), L2 (## Fontes 4 URLs: pricing/prompt-caching + ccusage), M1 (vídeo uso eficiente do Claude Code) aplicados. 431 linhas; 11/11 aplicáveis. Sem desvios.

#### 06 - Segurança organizacional   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-08)
- **Estado:** 391 linhas reais · fase: ausente · status: evergreen
- **Núcleo/gaps:** E4, E5, E7, E8, L2, M1
- **Score:** 6/12
- **Plano de execução:**
  - Adicionar `## Casos práticos` com ≥2 cenários de produção (ex: incidente de MCP prod exposto, prompt injection real em CI) → ativa E4
  - Adicionar `## O que vem a seguir` com ponte narrativa e wikilink pra `07 - Onboarding de time` → ativa E5
  - Adicionar tabela PT↔EN dos termos-chave (guardrail, prompt injection, least privilege, hook, allowedTools) → ativa E7
  - Converter parágrafos de `## Armadilhas` em ≥3 callouts `[!warning]` → ativa E8
  - Criar `## Fontes` com ≥1 URL externa verificável (docs oficiais de segurança/hooks do Claude Code ou OWASP para LLM/agent security) → ativa L2
  - Trocar o `[!tip]` genérico por um com link de vídeo/podcast real sobre segurança de agentes de IA → ativa M1
- **Resultado:** E4 (2 cenários: MCP staging→prod exposto + prompt injection via issue de CI), E5 (→ [[07]]), E7 (tabela PT↔EN 5 termos), E8 (6 → [!warning]), L2 (## Fontes: Hooks reference + OWASP LLM Top 10), M1 (talk Simon Willison, Lethal Trifecta) aplicados. 438 linhas; T3 <500 Magus fora do plano. Sem desvios.

#### 07 - Onboarding de time   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-08)
- **Estado:** 407 linhas reais · fase: ausente · status: evergreen
- **Núcleo/gaps:** E4, E5, E7, E8, P1, L2, M1
- **Score:** 6/13 (E1,E2,E3,E6,P2,L1 presentes)
- **Plano de execução:**
  - Adicionar `## Casos práticos` com ≥2 cenários de produção reaproveitando/expandindo os workflows já descritos → ativa E4
  - Adicionar `## O que vem a seguir` com ponte narrativa e wikilink pra próxima nota do galho → ativa E5
  - Adicionar tabela PT↔EN a partir do "Key vocabulary" já existente → ativa E7
  - Converter itens de "Anti-padrões"/"Armadilhas" em ≥3 callouts `[!warning]` → ativa E8
  - Adicionar `## Fontes` com ≥1 URL externa verificável sobre adoção de IA em times → ativa L2
  - Adicionar `[!tip]` com link de vídeo/podcast real sobre onboarding de times em ferramentas de IA → ativa M1
  - Adicionar bloco de código com caso-problema concreto (ex: falha de onboarding sem pré-requisito) → ativa P1
- **Resultado:** E4 (2 cenários: onboarding no meio da sprint + skill divergindo do CLAUDE.md), E5 (→ [[08]]), E7 (tabela PT↔EN 7 termos), E8 (11 → [!warning]), L2 (## Fontes Faros AI adoção IA), M1 (podcast AI & I / Claude Code), P1 (bloco falha /convencoes sem CLAUDE.md) aplicados. 457 linhas. Sem desvios.

#### 08 - Avaliando qualidade   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-08)
- **Estado:** 403 linhas reais · fase: ausente · status: evergreen
- **Núcleo/gaps:** E4, E5, E7, E8, L2, M1
- **Score:** 6/12
- **Plano de execução:**
  - Adicionar `## Casos práticos` com ≥2 cenários de produção reais (ex: refactor com testes vs. lógica financeira) → ativa E4
  - Adicionar `## O que vem a seguir` como ponte narrativa (não só link) apontando pra próxima nota do galho → ativa E5
  - Adicionar tabela PT↔EN dos termos-chave (trust calibration, verification, blind spots etc.) → ativa E7
  - Renomear `## Armadilhas` para `## Armadilhas comuns` e converter os 6 itens em callouts `[!warning]` (mínimo 3) → ativa E8
  - Adicionar `## Fontes` com ≥1 URL externa verificável sobre avaliação de qualidade de output de IA/code review → ativa L2
  - Pesquisar e embutir `[!tip]` com vídeo/podcast sobre confiar em código gerado por IA → ativa M1
- **Resultado:** E4 (2 cenários: refactor com testes vs. lógica financeira), E5 (→ [[Workflows/index]], último do galho), E7 (tabela PT↔EN), E8 (## Armadilhas comuns, 6 → [!warning]), L2 (## Fontes Addy Osmani + The New Stack), M1 (vídeo review de código de IA) aplicados. 456 linhas; score 12/12. Sem desvios.
