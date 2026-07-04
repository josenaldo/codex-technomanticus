---
title: "Roadmap — Economia de Tokens"
created: 2026-07-02
type: meta
publish: false
tags:
  - meta
  - roadmap
---

# Roadmap — Economia de Tokens

Diagnóstico migrado de guia/roadmap - ia.md (30/06). Cada entrada tem estado de enriquecimento, score, classificação de custo e plano de execução acionável.

**Galho:** `03-Dominios/Tecnologia/IA/Economia de Tokens`

> [!warning] Diagnóstico de 30/06 — pode estar defasado. Vários itens marcados ⬜ podem já ter sido enriquecidos depois; reconciliar com o estado real ao tratar o galho.

## Régua de análise

Checklist `verificar-nota` — 12 itens (isenções por fase/tipo/broto aplicadas por nota):

| Grupo | Itens |
|-------|-------|
| ESTRUTURA | E1 TL;DR · E2 Abertura-problema · E3 Mermaid · E4 Casos práticos · E5 O que vem a seguir · E6 Inglês · E7 Tabela PT↔EN · E8 Armadilhas [!warning] |
| PROFUNDIDADE | P1 Código-com-falha · P2 Mecanismo explicado |
| LINKS | L1 Wikilink cross-galho · L2 Referência externa (URL) |
| MÍDIA | M1 Vídeo/podcast embutido |

**Esquema de `fase:` detectado:** MISTO (01-04 sem `fase:`, 05-22 = Adepto)
**Piso de linhas:** aplicável às notas com `fase:` (Adepto ≥400). Notas 01-04 sem `fase:` = gap de núcleo a fechar.

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 22 |
| ⬜ pendente | 11 |
| ➖ não precisa | 2 |
| ✅ feita | 9 |
| 🔄 em andamento | 0 |
| % concluído | 50% |

> [!note] Sessão 2026-07-03. Enriquecidas 9 notas (01·02·03·04·06·07·08·10·11) em 3 ondas de ≤3 subagentes + verify inline do coordenador. Pausa por governança de tokens (projeção do bloco >95%). Restam ⬜: 12·13·14·15·16·17·18·19·20·21·22. Fonte primária usada: posts de blog do dono (dieta de tokens no Claude Code). Verify pegou: ccusage 18.0.11→20.0.14, Helicone→Mintlify, LangMem ref sem URL, redirect blog.langchain.dev→langchain.com; confirmou arxiv 2308.08155 (AutoGen).

---

## Notas

#### 01 - O problema — por que tokens custam dinheiro   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 122 linhas · fase: AUSENTE (gap) · status: evergreen
- **Núcleo/gaps:** E2, E5, E6, E7, E8, P1, L2
- **Score:** 5/12
- **Plano de execução:**
  - Adicionar `fase: Iniciado` ao frontmatter — fecha o gap de fase das notas 01-04
  - Adicionar abertura com cenário/problema concreto antes de "## O que é" (ex: engenheiro que recebe fatura de $25 sem entender de onde veio)
  - Adicionar "O que vem a seguir" com ponte narrativa para `[[02 - Anatomia do gasto — input, output e reasoning]]`
  - Converter "## Armadilhas" (lista bullet) para callouts `[!warning]` individuais
  - Adicionar URLs reais às referências (anthropic.com/pricing, artificialanalysis.ai)
- **Resultado:** fase:Iniciado + abertura-cenário (fatura $25) + "O que vem a seguir"→02 + 4 callouts [!warning] + URLs verificadas (claude.com/pricing 200, artificialanalysis.ai/providers/anthropic 200). Preços confirmados contra fonte oficial (platform.claude.com/docs pricing) — batem com o post. Score ~8/12 (136 linhas; T1/E4/E6/E7 fora do escopo do plano). **Débito herdado:** tabelas citam Opus/Sonnet "4.6" (ID atual 4.8) — atualizar versões em ciclo futuro.

#### 02 - Anatomia do gasto — input, output e reasoning   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 111 linhas · fase: AUSENTE (gap — provavelmente Iniciado) · status: evergreen
- **Núcleo/gaps:** E1, E5, E6, E7, E8, P1, L2
- **Score:** 5/12
- **Plano de execução:**
  - Adicionar `fase: Iniciado` ao frontmatter
  - Expandir TL;DR para ≥3 linhas densas (as três faturas distintas · preço diferenciado · onde está a maior alavanca)
  - Adicionar "O que vem a seguir" com ponte para `[[03 - Por que agentes gastam tanto]]`
  - Converter "## Armadilhas Técnicas" (lista numerada) para callouts `[!warning]` individuais
  - Adicionar fonte externa com URL (anthropic.com/pricing, artificialanalysis.ai ou openai.com/pricing)
  - Expandir corpo de 111 para ≥300 linhas (piso Iniciado): seção inglês + PT↔EN, mais exemplos numéricos, ≥1 exemplo de código-com-falha (JSON sem `thinking_budget`)
- **Resultado:** 111→300 linhas. fase:Iniciado + TL;DR 3-linhas (três faturas) + 4 callouts [!warning] + "O que vem a seguir"→03 + seção inglês + tabela PT↔EN (13 pares) + código-com-falha (`thinking` sem `budget_tokens`) + breakdown "$245" (fonte primária: post do dono) + correção do mito Opus 1,67×. Preços verificados em platform.claude.com/docs/pricing (Opus 4.8 $5/$25/$0,50 · Sonnet 4.6 $3/$15/$0,30 · Haiku 4.5 $1/$5/$0,10 · cache write 1,25×). URLs 200: platform.claude.com/docs/pricing, developers.openai.com/api/docs/guides/reasoning. Sem fabricação.

#### 03 - Por que agentes gastam tanto   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 120 linhas · fase: AUSENTE (gap — provavelmente Iniciado) · status: evergreen
- **Núcleo/gaps:** E3, E5, E6, E7, E8, P1
- **Score:** 7/12
- **Plano de execução:**
  - Adicionar `fase: Iniciado` ao frontmatter (ativa verificação de piso ≥300)
  - Adicionar "O que vem a seguir" com ponte para a nota 04 (Monitoramento)
  - Converter armadilhas dos 5 vetores (retries silenciosos, rabbit holes, tool verbosity) para ≥3 callouts `[!warning]` individuais
  - Adicionar diagrama Mermaid (xychart ou sequenceDiagram da acumulação turno-a-turno)
  - Expandir para ≥300 linhas: seção "Como explicar em inglês" + tabela PT↔EN (agentic loop, context window, tool definition, rabbit hole, retry)
- **Resultado:** 120→300 linhas. fase:Iniciado + "O que vem a seguir"→04 + 3 callouts [!warning] (tool verboso/retries/rabbit holes) + 2 Mermaid (sequenceDiagram turno-a-turno + xychart curva quadrática) + seção inglês + tabela PT↔EN (7 termos) + tabela antes/depois com números da auditoria real do dono (68→1.900 req/bloco, 124k tok/min). CLAUDE_CODE_SUBAGENT_MODEL confirmado via WebSearch. 3 URLs pré-existentes revalidadas 200 (stanford/github.blog/openreview). Sem URL nova, sem fabricação.

#### 04 - Monitoramento — ccusage, Langfuse, dashboards   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 312 linhas · fase: AUSENTE (gap) · status: growing / progress: in_progress
- **Núcleo/gaps:** E2, E3, E5, E6, E7, E8, P1
- **Score:** 5/12
- **Plano de execução:**
  - Adicionar `fase: Iniciado` ao frontmatter (nota já está acima do piso ≥300)
  - Adicionar "O que vem a seguir" com ponte para `[[05 - Prompt caching na prática]]`
  - Adicionar parágrafo de abertura com cenário real antes de "## O que é"
  - Converter "## Armadilhas" (7 itens em lista) para callouts `[!warning]` individuais, priorizando monitorar só o total, Helicone e PII em spans OTel
  - Adicionar ≥1 diagrama Mermaid (custo por camada ou ciclo ccusage→dashboard→alerta)
  - Adicionar seção "Como explicar em inglês" + tabela PT↔EN (observability, trace, span, generation, cache hit rate, anomaly detection, cost creep, billing window)
  - Adicionar `[!info]` de caducidade nas versões específicas (ccusage 18.0.11, Helicone maintenance mode, convenções OTel GenAI experimental)
- **Resultado:** 377 linhas, score ~10/12. fase:Iniciado + abertura-cenário ($245: cache read 55%/creation 30%/output 15%, fonte primária post do dono) + 7 callouts [!warning] + Mermaid (ciclo ccusage→dashboard→alerta com loop de baseline) + seção inglês + tabela PT↔EN + "O que vem a seguir"→05 + 3 [!info] caducidade. **Atualização de versão pega no verify: ccusage 18.0.11→20.0.14** (confirmado registry.npmjs.org). Helicone maintenance/aquisição Mintlify (3/mar/2026) confirmada; OTel GenAI spans de cliente estáveis / agente em Development — confirmado. URLs 200: registry.npmjs.org/ccusage, helicone.ai/blog/joining-mintlify, mintlify.com/blog, opentelemetry.io/docs/specs/semconv/gen-ai. Sem fabricação.

#### 05 - Prompt caching na prática   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 401 linhas · fase: Adepto · status: growing
- **Núcleo/gaps:** —
- **Score:** 12/12
- **Plano de execução:**
  - — nenhuma
- **Resultado:** —

#### 06 - Context pruning — o que remover do prompt   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 403 linhas · fase: Adepto · status: growing
- **Núcleo/gaps:** L1
- **Score:** 11/12
- **Plano de execução:**
  - Adicionar 1 wikilink cross-galho no corpo (ex: `[[06 - A janela de contexto]]` ao mencionar "lost in the middle", ou galho RAG e Vector Databases ao tratar semantic chunking/retrieval)
- **Resultado:** wikilink cross-galho `[[06 - A janela de contexto]]` (Anatomia dos LLMs) adicionado na seção "lost in the middle" (linha 33); alvo único confirmado. 403 linhas. L1 quitado.

#### 07 - Compressão de tool definitions   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 399 linhas · fase: Adepto · status: growing
- **Núcleo/gaps:** L1
- **Score:** 11/12
- **Plano de execução:**
  - Adicionar ≥1 wikilink cross-galho (ex: galho MCP ao citar "Estado da arte", `[[Anatomia de Agents]]` ao tratar lazy loading, ou `[[Structured Outputs]]` como alternativa a tools) — qualquer adição também cruza o piso de 400 linhas
- **Resultado:** wikilink cross-galho `[[Anatomia de Agents]]` (folder-link) na seção "Lazy loading" (linha 139); regra Quartz OK (index.md existe no alvo). 398→400 linhas (cruzou o piso). L1 quitado.

#### 08 - Compactação de histórico em agentes   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 384 linhas · fase: Adepto · status: growing
- **Núcleo/gaps:** P1
- **Score:** 11/12
- **Plano de execução:**
  - Expandir "## Estado da arte" ou "## Casos práticos" com ~20 linhas substantivas (ex: padrão LangMem, ou métricas do Caso 4) para cruzar o piso Adepto (384 < 400)
- **Resultado:** 384→401 linhas (cruzou piso). Callout [!info] LangMem SDK (memória semântica/episódica/procedural, extração hot-path vs background) em "Estado da arte" + referência. **Verify:** LangMem v0.0.30 confirmado no PyPI; referência corrigida pelo coordenador p/ URLs clicáveis reais (langchain-ai.github.io/langmem 200, pypi.org/project/langmem 200) — subagente havia deixado citação sem URL limpa.

#### 09 - Model routing — modelo certo para a tarefa   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 405 linhas · fase: Adepto · status: growing
- **Núcleo/gaps:** P1
- **Score:** 11/12
- **Plano de execução:**
  - — nenhuma
- **Resultado:** —

#### 10 - Sub-agentes especializados   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 276 linhas · fase: Adepto · status: growing
- **Núcleo/gaps:** E2, L2
- **Score:** 9/12
- **Plano de execução:**
  - Expandir a nota de 276 → ≥400 linhas (piso Adepto): aprofundar "Estado da arte" e enriquecer casos práticos com números concretos
  - Adicionar parágrafo de abertura com cenário concreto antes da tabela "Sub-agente vs model routing" (ex: agente de análise de codebase que explodiu o contexto a $18/run)
  - Adicionar URLs clicáveis nas Fontes (docs.anthropic.com/tool-use, arxiv Wu et al., blog.langchain.dev)
- **Resultado:** 276→400 linhas (cruzou piso). Abertura-cenário (agente codebase ~180k ctx, $15-20/run) + Estado da arte aprofundado (CLAUDE_CODE_SUBAGENT_MODEL confirmado, regra de teto de fan-out, fórmula custo×req×preço) + Caso 5 (68→1900 req/bloco, fonte primária post do dono) + exemplos LangGraph/CrewAI. **Verify:** 4 URLs 200 (code.claude.com/docs/sub-agents, platform.claude.com/docs/tool-use, arxiv 2308.08155, langchain.com/blog/what-is-an-agent — pegou redirect blog.langchain.dev→langchain.com). **arxiv 2308.08155 confirmado = "AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation" (Wu et al.)** — citação real. 3 marcas "(a confirmar)" honestas (CrewAI/LangGraph/Hamel — fora do escopo de verify), sem fabricação.

#### 11 - Semantic caching   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 401 linhas · fase: Adepto · status: growing
- **Núcleo/gaps:** P1
- **Score:** 11/12
- **Plano de execução:**
  - Adicionar exemplo de código-com-falha (ex: lookup Redis com índice não criado, ou threshold 0.85 servindo "cancelar assinatura" como hit para "suspender assinatura")
- **Resultado:** 401→479 linhas. Código-com-falha (P1) adicionado: `SIMILARITY_THRESHOLD=0.85` servindo "cancelar" como hit p/ "suspender" (cosine ~0.87-0.89) + correção (threshold 0.96 + guarda de intent). APIs reais (GPTCache/Qdrant/Redis, sintaxe correta). **Débito herdado:** placeholder `https://youtube.com` num [!tip] pré-existente (fora do escopo) — trocar por fonte real em ciclo futuro.

#### 12 - Batch API — economia em volume   [mecânico]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 467 linhas · fase: Adepto · status: growing
- **Núcleo/gaps:** P1, L2
- **Score:** 10/12
- **Plano de execução:**
  - Adicionar URLs clicáveis às fontes (ex: `[Message Batches API](https://docs.anthropic.com/en/api/creating-message-batches)`)
  - Adicionar exemplo de código-com-falha (ex: `custom_id` duplicado causando colisão de resultados, ou `max_tokens` omitido gerando erro 400)
- **Resultado:** —

#### 13 - Respostas concisas — controlar output tokens   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 376 linhas · fase: Adepto · status: growing
- **Núcleo/gaps:** P1, L2
- **Score:** 11/12
- **Plano de execução:**
  - Expandir para ≥400 linhas (piso Adepto): aprofundar "Estado da arte" (structured outputs forçados, instruction following em 2026) ou ampliar Casos práticos
  - Adicionar código-com-falha explícito (ex: `max_tokens=300` truncando resposta sem monitorar `stop_reason`)
  - Substituir URL genérica `https://youtube.com/anthropic` no `[!tip]` por fonte real
- **Resultado:** —

#### 14 - Thinking budget — controlar reasoning tokens   [mecânico]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 427 linhas · fase: Adepto · status: growing
- **Núcleo/gaps:** P1, L1
- **Score:** 10/12
- **Plano de execução:**
  - Adicionar ≥1 wikilink cross-galho (ex: `[[15 - Reasoning models e chain-of-thought]]` do galho Anatomia dos LLMs, ou `[[Dicionário de IA]]`)
  - Substituir URL genérica `https://youtube.com/anthropic` no `[!tip]` por fonte verificável (ex: Simon Willison, Anthropic docs)
  - Opcional: adicionar código-com-falha (thinking ativado para task trivial, custo $1.50/chamada sem ganho)
- **Resultado:** —

#### 15 - Orçamento e hard limits   [mecânico]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 399 linhas · fase: Adepto · status: growing
- **Núcleo/gaps:** L1
- **Score:** 11/12
- **Plano de execução:**
  - Adicionar 1 wikilink cross-galho (ex: `[[Anatomia de Agents]]` ao mencionar agentes em loop nos Kill switches, ou `[[Dicionário de IA]]` no "Veja também") — também empurra a nota acima de 400 linhas
- **Resultado:** —

#### 16 - Auditoria de consumo   [mecânico]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 398 linhas · fase: Adepto · status: growing
- **Núcleo/gaps:** P1, L1
- **Score:** 10/12
- **Plano de execução:**
  - Adicionar 1 wikilink cross-galho (ex: `[[Anatomia de Agents]]` na seção de retries, ou `[[Dicionário de IA]]` no "Veja também") — provavelmente cruza o piso de 400 linhas
- **Resultado:** —

#### 17 - ROI de IA — quando o agente vale o custo   [mecânico]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 397 linhas · fase: Adepto · status: growing
- **Núcleo/gaps:** P1, L2
- **Score:** 10/12
- **Plano de execução:**
  - Adicionar URLs diretas às 4 referências da seção "## Fontes" (GitHub Research Copilot study, METR 2025, Stack Overflow Survey 2026, MIT Sloan Kalliamvakou 2025) — supre também as linhas que faltam para o piso de 400
- **Resultado:** —

#### 18 - Playbook de economia — checklist completo   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 353 linhas · fase: Adepto · status: growing
- **Núcleo/gaps:** P1, L1, L2
- **Score:** 9/12
- **Plano de execução:**
  - Adicionar URLs clicáveis às 4 referências (docs.anthropic.com, helicone.ai/docs, simonwillison.net, leanpub.com)
  - Adicionar ≥1 wikilink cross-galho (ex: `[[Dicionário de IA]]`, `[[Anatomia de Agents]]`)
  - Nota está 47 linhas abaixo do piso Adepto de 400 — se as mudanças acima não cruzarem, expandir "Estado da arte" ou aprofundar um caso prático
- **Resultado:** —

#### 19 - Planos e tiers — Max, Pro, API, Enterprise   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 372 linhas · fase: Adepto · status: growing
- **Núcleo/gaps:** P1, L2
- **Score:** 10/12
- **Plano de execução:**
  - Adicionar hiperlinks clicáveis às 4 referências (anthropic.com/pricing, openai.com/pricing, ai.google.dev/pricing, docs.litellm.ai)
  - Expandir "Estado da arte — junho 2026" (deflação de planos, multi-modal, Enterprise para times menores) ou aprofundar um caso prático com cálculo numérico — nota está 28 linhas abaixo do piso de 400
  - Adicionar `[!warning]`/`[!info]` de caducidade antes das tabelas de preços por provider (validade junho 2026)
- **Resultado:** —

#### 20 - O futuro — tokens cada vez mais baratos   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 288 linhas · fase: Adepto · status: growing
- **Núcleo/gaps:** E2, P1
- **Score:** 10/12
- **Plano de execução:**
  - Adicionar parágrafo de abertura com cenário concreto antes de "## A queda de preço mais rápida na história da tecnologia" (ex: orçamento de IA com projeções que parecem impossíveis)
  - Nota está 112 linhas abaixo do piso de 400 — abertura + caducidade + aprofundar "Estado da arte" ou um caso prático devem aproximar/cruzar o piso
  - Adicionar `[!warning]`/`[!info]` de caducidade antes da tabela de preços e de "Estado da arte — junho 2026" (projeções 2027-2028, GPT-5/Claude 5)
  - Adicionar URLs clicáveis às 4 referências (artificialanalysis.ai, ben-evans.com, github.com/vipulnaik, semianalysis.com)
- **Resultado:** —

#### 21 - Hacks de trincheira — Claude, Gemini e Copilot em 2026   [mecânico]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 409 linhas · fase: Adepto · status: growing
- **Núcleo/gaps:** L1, L2
- **Score:** 9/12
- **Plano de execução:**
  - Adicionar ≥1 wikilink cross-galho (ex: `[[Anatomia de Agents]]` ou `[[Agentes de Codificação]]`) — os 4 wikilinks atuais em "Veja também" são intra-galho
  - Substituir domínio+path em prosa por URLs Markdown clicáveis reais nas 4 fontes
  - Adicionar `[!warning]`/`[!info]` de caducidade na tabela de decisão e em "Estado da arte — junho 2026" (modelos, preços, AI Credits Copilot)
- **Resultado:** —

#### 22 - Caso real — Auditoria de 47M tokens em maio 2026   [mecânico]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 401 linhas · fase: Adepto · status: growing
- **Núcleo/gaps:** L1, P1
- **Score:** 10/12
- **Plano de execução:**
  - Adicionar ≥1 wikilink cross-galho em "O que vem a seguir" ou "Veja também" (ex: `[[Anatomia de Agents]]`, `[[Context Engineering]]`, `[[Agentes de Codificação]]`)
- **Resultado:** —
