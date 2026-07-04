---
title: "Roadmap — Agentes de Codificação"
created: 2026-07-02
type: meta
publish: false
tags:
  - meta
  - roadmap
---

# Roadmap — Agentes de Codificação

Diagnóstico migrado de guia/roadmap - ia.md (30/06). Cada entrada tem estado de enriquecimento, score, classificação de custo e plano de execução acionável.

**Galho:** `03-Dominios/Tecnologia/IA/Agentes de Codificação`

> [!warning] Diagnóstico de 30/06 — pode estar defasado. Vários itens marcados ⬜ podem já ter sido enriquecidos depois; reconciliar com o estado real ao tratar o galho.

## Régua de análise

Checklist `verificar-nota` — 12 itens (isenções por fase/tipo/broto aplicadas por nota):

| Grupo | Itens |
|-------|-------|
| ESTRUTURA | E1 TL;DR · E2 Abertura-problema · E3 Mermaid · E4 Casos práticos · E5 O que vem a seguir · E6 Inglês · E7 Tabela PT↔EN · E8 Armadilhas [!warning] |
| PROFUNDIDADE | P1 Código-com-falha · P2 Mecanismo explicado |
| LINKS | L1 Wikilink cross-galho · L2 Referência externa (URL) |
| MÍDIA | M1 Vídeo/podcast embutido |

**Esquema de `fase:` detectado:** COM fase (Adepto); nota 01 é gap — SEM fase, deveria ser Iniciado
**Piso de linhas:** aplicável — Adepto ≥400 (nota 01, se corrigida para Iniciado, cai sob piso Iniciado ≥300)

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 18 |
| ⬜ pendente | 9 |
| ➖ não precisa | 3 |
| ✅ feita | 6 |
| 🔄 em andamento | 0 |
| % concluído | 40% |

> [!note] Sessão 2026-07-04. +6 notas (01·03·05·06·07·08) em 2 ondas de ≤3 + verify inline (usuário sobrepôs a parada das 15 — tokens com folga total, bloco resetado). Restam ⬜: 09·10·11·12·13·14·15·17·18 (9). Padrão do galho confirmado: quase toda nota = reescrita da ponte E5 nomeando a próxima nota + `[!info]` de caducidade nos dados voláteis. Verify: todos os wikilinks (irmãos + cross-galho `[[Dicionário de IA#tool use]]`, âncora conferida) apontam para alvos existentes. Nenhum preço/modelo inventado ou alterado.

---

## Notas

#### 01 - De autocomplete a agentes autônomos   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-04)
- **Estado:** 405 linhas · fase: AUSENTE (gap — galho usa `fase:`, nota 01 deveria ser Iniciado) · status: growing
- **Núcleo/gaps:** P1
- **Score:** 11/12
- **Plano de execução:**
  - Adicionar `fase: Iniciado` ao frontmatter — único gap; conteúdo já sólido, sem mudança estrutural necessária
- **Resultado:** `fase: Iniciado` adicionada ao frontmatter (405 linhas, acima do piso Iniciado ≥300). Único gap fechado, sem mudança de conteúdo.

#### 02 - Vibe coding vs engenharia disciplinada   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 409 linhas · fase: Adepto · status: growing
- **Núcleo/gaps:** P1
- **Score:** 11/12
- **Plano de execução:**
  - — nenhuma
- **Resultado:** —

#### 03 - O comprehension gate   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-04)
- **Estado:** 409 linhas · fase: Adepto · status: growing / progress: done
- **Núcleo/gaps:** E5, P1
- **Score:** 10/12
- **Plano de execução:**
  - Reescrever a abertura de "## O que vem a seguir" para nomear explicitamente [[04 - Cursor — AI-native IDE]] como próxima nota, com motivação narrativa; manter as pontes atuais para 14/16/18 como contexto adicional
- **Resultado:** 409→410 linhas. Abertura de "O que vem a seguir" reescrita nomeando `[[04 - Cursor — AI-native IDE]]` (irmão confirmado existir) com motivação narrativa (o gate opera dentro da ferramenta, Cursor é onde isso aparece na prática); pontes 14/16/18 mantidas como contexto. E5 quitado. Sem alteração factual do corpo.

#### 04 - Cursor — AI-native IDE   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 410 linhas · fase: Adepto · status: growing
- **Núcleo/gaps:** P1
- **Score:** 11/12
- **Plano de execução:**
  - — nenhuma
  - ⚠️ Aviso data de validade: alta densidade de fatos caducáveis (ARR, preços de planos, nomes de modelos, timeline Series B) — monitorar ao enriquecer
- **Resultado:** —

#### 05 - Claude Code — terminal-first agent   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-04)
- **Estado:** 408 linhas · fase: Adepto · status: growing
- **Núcleo/gaps:** E5, P1
- **Score:** 10/12
- **Plano de execução:**
  - Adicionar parágrafo narrativo de abertura em "O que vem a seguir" apontando para [[06 - GitHub Copilot e Copilot Agents]] como próximo passo — do agente terminal da Anthropic para o maior ecossistema de codificação IA do mercado
  - ⚠️ Data de validade: tabela de custo/modelos, seção "Por que importa" e histórico (opusplan) têm dados caducáveis — adicionar `[!info]` de caducidade
- **Resultado:** 409→417 linhas. Abertura de "O que vem a seguir" contrastando Claude Code (terminal-first) com `[[06 - GitHub Copilot e Copilot Agents]]` (maior ecossistema, embutido no editor) — irmão confirmado. 3 `[!info]` de caducidade (seção "Por que importa", histórico opusplan, tabela custo/modelos) envolvendo dados já existentes — nenhum preço/modelo/data inventado ou alterado. E5 + caducidade quitados.

#### 06 - GitHub Copilot e Copilot Agents   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-04)
- **Estado:** 409 linhas · fase: Adepto · status: growing
- **Núcleo/gaps:** E5, P1
- **Score:** 10/12
- **Plano de execução:**
  - Adicionar ponte narrativa em "O que vem a seguir" para [[07 - Windsurf e Cascade]] — a seção hoje avança o leitor fora de sequência (04/05/12/14/15); inserir parágrafo motivando a transição para um IDE AI-native com agentes de longa duração via Cascade
  - ⚠️ Data de validade: tabela de tiers/preços, "30 milhões de devs em 2026" e histórico de modelos (Claude 3.5 Sonnet, Gemini 1.5 Pro) — sinalizar caducidade
- **Resultado:** 408→419 linhas. Ponte em "O que vem a seguir" para `[[07 - Windsurf e Cascade]]` (irmão confirmado) — contraste extensão-em-editor vs IDE AI-native com Cascade. 3 `[!info]` de caducidade (30M devs 2026, histórico de modelos, tiers/preços) envolvendo dados existentes — nada alterado. E5 quitado.

#### 07 - Windsurf e Cascade   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-04)
- **Estado:** 403 linhas · fase: Adepto · status: growing
- **Núcleo/gaps:** E5, L1, P1
- **Score:** 9/12
- **Plano de execução:**
  - E5 — substituir/complementar "O que vem a seguir" (hoje discute futuro sob a OpenAI) por parágrafo de ponte para [[08 - Gemini CLI — o player Google]]: do IDE-first com agentes integrados para o CLI Google, terminal-first
  - L1 — adicionar ao menos 1 wikilink cross-galho (Dicionário de IA ou galho Economia de Tokens)
  - ⚠️ Data de validade: tabela "Modelo de preços" sem aviso explícito pós-aquisição — adicionar `[!info]` recomendando verificar em windsurf.com
- **Resultado:** 396→407 linhas. E5: ponte final em "O que vem a seguir" para `[[08 - Gemini CLI — o player Google]]` (irmão confirmado) — IDE-first vs terminal-first Google. L1: wikilink cross-galho `[[Dicionário de IA#tool use|tool calls]]` em "Por que importa" (heading `### tool use` confirmado na linha 73 do Dicionário — âncora resolve). `[!info]` de caducidade após tabela "Modelo de preços" (verificar em windsurf.com). E5+L1+caducidade quitados. Nenhum preço alterado.

#### 08 - Gemini CLI — o player Google   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-04)
- **Estado:** 409 linhas · fase: Adepto · status: growing
- **Núcleo/gaps:** E5, P1
- **Score:** 10/12
- **Plano de execução:**
  - E5 — converter o final de "O que vem a seguir" (hoje focado em evolução de produto) para bridge narrativa a [[09 - Aider — o pair programmer de terminal]]: da aposta Google (GCP, contexto gigante, multimodal) ao caminho open-source, agnóstico de modelo
  - ⚠️ Data de validade: tabela "Modelo de preços" (Gemini 2.5 Pro/Flash, 2.0 Flash) sem aviso — adicionar `[!info]` recomendando ai.google.dev/pricing
- **Resultado:** 409→413 linhas. E5: final de "O que vem a seguir" convertido em bridge para `[[09 - Aider — o pair programmer de terminal]]` (irmão confirmado) — da aposta Google (contexto 1M, multimodal, GCP) ao polo open-source agnóstico de modelo. `[!info]` de caducidade antes da tabela "Modelo de preços" (ai.google.dev/pricing citado em texto, não link clicável). E5+caducidade quitados. Nenhum modelo/preço alterado.

#### 09 - Aider — o pair programmer de terminal   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 409 linhas · fase: Adepto · status: growing
- **Núcleo/gaps:** E5, P1
- **Score:** 10/12
- **Plano de execução:**
  - E5 (núcleo) — "O que vem a seguir" cobre tendências do produto Aider mas não bridgeia; adicionar parágrafo final para [[10 - OpenCode — o harness open source]]: do polo "controle total" (um dev, um terminal, diffs aprovados) a um CLI open-source que empurra mais longe a autonomia
  - ⚠️ Data de validade: armadilha "sem MCP nativo (ainda)" datada em 2026 — verificar a cada revisão se mudou
- **Resultado:** —

#### 10 - OpenCode — o harness open source   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 409 linhas · fase: Adepto · status: growing
- **Núcleo/gaps:** E5, P1
- **Score:** 10/12
- **Plano de execução:**
  - E5 (núcleo) — "O que vem a seguir" cobre tendências gerais (MCP, orchestration, memória persistente) mas encerra sem bridge; adicionar parágrafo de fechamento para [[11 - Comparativo — qual ferramenta para qual tarefa]]: do mapa de harnesses open-source ao guia de decisão
  - ⚠️ Data de validade: stars do Cline, versões no histórico (OpenCode/Roo Code) mudam mensalmente — adicionar `[!info]` na seção "## Histórico"
- **Resultado:** —

#### 11 - Comparativo — qual ferramenta para qual tarefa   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 408 linhas · fase: Adepto · status: growing
- **Núcleo/gaps:** E5, L1, P1
- **Score:** 9/12
- **Plano de execução:**
  - E5 (núcleo) — "## O que vem a seguir" cobre tendências futuras mas bridgeia para nota 18, não para a 12; adicionar fechamento explícito para [[12 - Multi-agent — workflows com múltiplos agentes]]
  - L1 (opcional) — adicionar wikilink cross-galho (custo de tokens → Economia de Tokens; codebases longas → RAG e Vector Databases)
  - ⚠️ Data de validade: altíssima densidade de dados perecíveis (preços, mega-comparativo, projeções "em 2027/2028") — considerar `[!info]` antes das tabelas de custo e do mega-comparativo
- **Resultado:** —

#### 12 - Multi-agent — workflows com múltiplos agentes   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 408 linhas · fase: Adepto · status: growing
- **Núcleo/gaps:** E5, P1
- **Score:** 10/12
- **Plano de execução:**
  - E5 (núcleo) — "O que vem a seguir" bridgeia para 16/17 mas não para a nota seguinte; adicionar parágrafo de fechamento para [[13 - Devin e agentes autônomos cloud]]: de entender um agente individual a agentes que operam em cloud sem supervisão contínua
- **Resultado:** —

#### 13 - Devin e agentes autônomos cloud   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 405 linhas · fase: Adepto · status: growing
- **Núcleo/gaps:** E5, P1
- **Score:** 10/12
- **Plano de execução:**
  - E5 (núcleo) — "## O que vem a seguir" cobre roadmap 2026-2028 mas não bridgeia; adicionar parágrafo de fechamento para [[14 - agents.md e configuração de projeto]]: de delegar a task ao agente cloud a configurar o ambiente em que ele opera
  - ⚠️ Data de validade: taxa SWE-bench e scores por player "em 2026" — adicionar `[!info]` de caducidade no início de "## O ecossistema em 2026"
- **Resultado:** —

#### 14 - agents.md e configuração de projeto   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 401 linhas · fase: Adepto · status: growing
- **Núcleo/gaps:** E5, P1
- **Score:** 10/12
- **Plano de execução:**
  - E5 (núcleo) — "## O que vem a seguir" cobre evolução futura dos arquivos de config sem bridgeia; adicionar parágrafo de fechamento para [[15 - MCP — o protocolo universal]]: do CLAUDE.md estático ao acesso dinâmico a ferramentas e contexto sob demanda via MCP
- **Resultado:** —

#### 15 - MCP — o protocolo universal   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 401 linhas · fase: Adepto · status: growing
- **Núcleo/gaps:** E5, L1
- **Score:** 10/12
- **Plano de execução:**
  - Adicionar parágrafo de bridge em "O que vem a seguir" apontando para [[16 - O loop agentic — plan, act, observe]]: como o agente decide quando e como usar as ferramentas conectadas via MCP
  - Adicionar wikilink cross-galho para o galho MCP dedicado (galho 9) em "## Veja também"
- **Resultado:** —

#### 16 - O loop agentic — plan, act, observe   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 401 linhas · fase: Adepto · status: growing
- **Núcleo/gaps:** P1
- **Score:** 11/12
- **Plano de execução:**
  - — nenhuma
- **Resultado:** —

#### 17 - Human-in-the-loop — quando (não) confiar   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 401 linhas · fase: Adepto · status: growing
- **Núcleo/gaps:** E5, P1
- **Score:** 10/12
- **Plano de execução:**
  - Reescrever/complementar o final de "## O que vem a seguir" para conectar narrativamente com a nota 18 (Benchmarks e avaliação — SWE-bench): de decidir quanta autonomia dar ao agente à necessidade de medir capacidade real
  - Opcional: adicionar código-com-falha (P1) — ex: hook com regex incorreto que deveria bloquear `rm -rf` mas não bloqueia
- **Resultado:** —

#### 18 - Benchmarks e avaliação — SWE-bench e além   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 402 linhas · fase: Adepto · status: growing
- **Núcleo/gaps:** P1
- **Score:** 11/12
- **Plano de execução:**
  - Adicionar `[!warning]` de caducidade no início de "## Leaderboard atual (maio 2026)" — modelos e scores mudam mensalmente; conferir em swebench.com ou Artificial Analysis
  - Opcional: ampliar o fechamento de "## O que vem a seguir" com gancho cross-galho (ex: Evaluation ou Observability), já que é a última nota do galho
- **Resultado:** —
