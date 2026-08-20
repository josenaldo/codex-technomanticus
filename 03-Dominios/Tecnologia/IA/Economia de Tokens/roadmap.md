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

**Esquema de `fase:` detectado:** MISTO (01-04 sem `fase:`, 05-22 = Adepto) **Piso de linhas:** aplicável às notas com `fase:` (Adepto ≥400). Notas 01-04 sem `fase:` = gap de núcleo a fechar.

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 22 |
| ⬜ pendente | 0 |
| ➖ não precisa | 2 |
| ✅ feita | 20 |
| 🔄 em andamento | 0 |
| % concluído | 100% |

> [!note] Sessão 2026-07-03. Enriquecidas 9 notas (01·02·03·04·06·07·08·10·11) em 3 ondas de ≤3 subagentes + verify inline do coordenador. Pausa por governança de tokens (projeção do bloco >95%). Fonte primária usada: posts de blog do dono (dieta de tokens no Claude Code). Verify pegou: ccusage 18.0.11→20.0.14, Helicone→Mintlify, LangMem ref sem URL, redirect blog.langchain.dev→langchain.com; confirmou arxiv 2308.08155 (AutoGen).
> [!success] Sessão 2026-07-04 (retomada pós-/clear, override consciente do usuário com uso real 28%). **GALHO FECHADO: 20/20 notas acionáveis ✅ (05·09 dispensadas).** +11 notas (12·13·14·15·16·17·18·19·20·21·22) em 4 ondas de ≤3 + verify inline do coordenador. Governança verde o tempo todo (projeção caiu 109%→78% após a carga leve substituir a extrapolação da sessão pesada). **Verify pegou/corrigiu:** fonte fabricada `hamel.ai` (domínio inexistente) removida (nota 12); URL youtube fake → vídeo real (13) e doc oficial (14); URL malformada `/docs/en/docs/` → canônica (14); **nota 17 — corpo cita METR como ganho 13–55% mas o estudo real achou 19% de LENTIDÃO (débito factual anotado, corrigir em passada futura)**; 2 fontes sem link por não-confirmação honesta (Simon Willison + Leanpub, nota 18); openai.com/pricing 403 por bot-block (mantida); nota 20 ficou 302 linhas (abaixo do piso, sem padding). **27 URLs conferidas 200 no total.** Zero fabricação.

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
- **Estado:** 420 linhas · fase: Adepto · status: growing
- **Núcleo/gaps:** P1
- **Score:** 11/12
- **Plano de execução:**
  - — nenhuma
- **Resultado:** —
- **Passe 2026-08-20 — material externo:** Seção **Como escolher: o menor que passa no seu teste** — a pirâmide dizia onde cada tier serve, mas faltava o método de decisão. Processo de 4 passos (20 casos reais com gabarito → rodar nos 3 candidatos → comparar acerto/custo/p95 na mesma tabela → ficar com o menor que passa), callout com as 4 armadilhas (leaderboard como veredito, nome do modelo no código, testar 3 exemplos no chat, trocar sem eval) e o fecho aterrissando a decisão no produto: 96% vs 94% não vale nada em triagem com revisão humana e vale muito em laudo que vai ao cliente. Fonte da lacuna: [[2026-ia-do-zero-ao-senior-trilha-visual]].

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
- **Enriquecimento:** ✅ feita (2026-07-04)
- **Estado:** 467 linhas · fase: Adepto · status: growing
- **Núcleo/gaps:** P1, L2
- **Score:** 10/12
- **Plano de execução:**
  - Adicionar URLs clicáveis às fontes (ex: `[Message Batches API](https://docs.anthropic.com/en/api/creating-message-batches)`)
  - Adicionar exemplo de código-com-falha (ex: `custom_id` duplicado causando colisão de resultados, ou `max_tokens` omitido gerando erro 400)
- **Resultado:** URLs clicáveis em 4/5 fontes (Anthropic Batches, OpenAI Batch, Google Vertex batch-prediction, LangChain Runnable.batch). Código-com-falha (P1): `custom_id = f.name` colidindo silenciosamente com dois `utils.js` em pastas distintas + corretivo `f.relative_to(source_dir)`. **Verify:** 4 URLs 200 (docs.anthropic.com→platform.claude.com e platform.openai.com→developers.openai.com por redirect estável; Google e LangChain diretas). **Fonte fabricada removida:** subagente ia linkar "Hamel Husain — hamel.ai", mas o domínio não existe (real é hamel.dev) e nenhum artigo correspondente foi achado — cortada em vez de inventar URL (guarda anti-fabricação).

#### 13 - Respostas concisas — controlar output tokens   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-04)
- **Estado:** 376 linhas · fase: Adepto · status: growing
- **Núcleo/gaps:** P1, L2
- **Score:** 11/12
- **Plano de execução:**
  - Expandir para ≥400 linhas (piso Adepto): aprofundar "Estado da arte" (structured outputs forçados, instruction following em 2026) ou ampliar Casos práticos
  - Adicionar código-com-falha explícito (ex: `max_tokens=300` truncando resposta sem monitorar `stop_reason`)
  - Substituir URL genérica `https://youtube.com/anthropic` no `[!tip]` por fonte real
- **Resultado:** 376→427 linhas (cruzou piso Adepto). Estado da arte aprofundado (structured outputs/`output_format`: reduzem erros de parsing, NÃO tokens de output; sobem input levemente; invalidam prompt cache). Código-com-falha (P1): `summarize_ticket()` com `max_tokens=300` truncando silenciosamente + versão corrigida que checa `stop_reason == "max_tokens"` e reprocessa. **Verify:** youtube.com/anthropic (fake) → vídeo real "AI prompt engineering: A deep dive" (`youtube.com/watch?v=T9aRN5JkmL8`, equipe Anthropic — Askell/Albert/Hershey/Witten), 200; ref nova Structured Outputs (platform.claude.com/docs/en/build-with-claude/structured-outputs), 200. Score ~11/12 (L1 pendente — 3 wikilinks intra-galho; fora do plano desta passada).

#### 14 - Thinking budget — controlar reasoning tokens   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-04)
- **Estado:** 427 linhas · fase: Adepto · status: growing
- **Núcleo/gaps:** P1, L1
- **Score:** 10/12
- **Plano de execução:**
  - Adicionar ≥1 wikilink cross-galho (ex: `[[15 - Reasoning models e chain-of-thought]]` do galho Anatomia dos LLMs, ou `[[Dicionário de IA]]`)
  - Substituir URL genérica `https://youtube.com/anthropic` no `[!tip]` por fonte verificável (ex: Simon Willison, Anthropic docs)
  - Opcional: adicionar código-com-falha (thinking ativado para task trivial, custo $1.50/chamada sem ganho)
- **Resultado:** Wikilink cross-galho `[[15 - Reasoning models e chain-of-thought]]` (Anatomia dos LLMs — alvo confirmado existir) em "Veja também", quita L1. **Verify:** youtube.com/anthropic (fake) → doc oficial Extended Thinking; coordenador corrigiu a URL de `/docs/en/docs/build-with-claude/...` (docs duplicado, só sobrevivia por redirect) p/ forma canônica `platform.claude.com/docs/en/build-with-claude/extended-thinking`, 200. Código-com-falha OPCIONAL não duplicado — já existia (thinking p/ "capital da França", $1.50/chamada sem ganho). Score ~11/12 (M1 marginal: [!tip] virou doc, não vídeo).

#### 15 - Orçamento e hard limits   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-04)
- **Estado:** 399 linhas · fase: Adepto · status: growing
- **Núcleo/gaps:** L1
- **Score:** 11/12
- **Plano de execução:**
  - Adicionar 1 wikilink cross-galho (ex: `[[Anatomia de Agents]]` ao mencionar agentes em loop nos Kill switches, ou `[[Dicionário de IA]]` no "Veja também") — também empurra a nota acima de 400 linhas
- **Resultado:** Wikilink cross-galho `[[Anatomia de Agents]]` (folder-link, `index.md` do alvo confirmado existir — regra Quartz OK) na seção "Kill switches em agentes". Quita L1. 398 linhas (o "≥400" do plano era meta implícita; só o wikilink estava no escopo, sem expansão de corpo).

#### 16 - Auditoria de consumo   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-04)
- **Estado:** 398 linhas · fase: Adepto · status: growing
- **Núcleo/gaps:** P1, L1
- **Score:** 10/12
- **Plano de execução:**
  - Adicionar 1 wikilink cross-galho (ex: `[[Anatomia de Agents]]` na seção de retries, ou `[[Dicionário de IA]]` no "Veja também") — provavelmente cruza o piso de 400 linhas
- **Resultado:** Wikilink cross-galho `[[Anatomia de Agents]]` (folder-link, `index.md` do alvo confirmado) na seção "Retries invisíveis", ancorado na frase sobre por que o agente insiste na mesma tool call. Quita L1. 397 linhas (adição inline, sem nova quebra; "≥400" era especulativo no plano).

#### 17 - ROI de IA — quando o agente vale o custo   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-04)
- **Estado:** 397 linhas · fase: Adepto · status: growing
- **Núcleo/gaps:** P1, L2
- **Score:** 10/12
- **Plano de execução:**
  - Adicionar URLs diretas às 4 referências da seção "## Fontes" (GitHub Research Copilot study, METR 2025, Stack Overflow Survey 2026, MIT Sloan Kalliamvakou 2025) — supre também as linhas que faltam para o piso de 400
- **Resultado:** 4 URLs diretas na seção Fontes, **todas verificadas 200** (github.blog Copilot study, metr.org/blog/2025-07-10, survey.stackoverflow.co/2025/ai, arxiv.org/abs/2302.06590). 396 linhas. **Verify pegou divergências (anotadas inline nas Fontes, sem apagar):** GitHub study é 2022 (não 2024); Stack Overflow é oficialmente "2025 Survey" (não 2026); paper Kalliamvakou é arXiv preprint 2023 (Peng/Kalliamvakou/Cihon/Demirer), não MIT Sloan. **⚠️ DÉBITO FACTUAL (fora do escopo do plano — decisão editorial do usuário):** o corpo (linha ~292) cita METR como evidência de "ganho de 13–55%", mas o estudo METR real achou o **oposto** — 19% de *lentidão* (RCT, 16 devs experientes, 246 tasks). Corpo e Fontes agora se contradizem de propósito (transparência); corrigir a asserção da linha 292 numa passada futura.

#### 18 - Playbook de economia — checklist completo   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-04)
- **Estado:** 353 linhas · fase: Adepto · status: growing
- **Núcleo/gaps:** P1, L1, L2
- **Score:** 9/12
- **Plano de execução:**
  - Adicionar URLs clicáveis às 4 referências (docs.anthropic.com, helicone.ai/docs, simonwillison.net, leanpub.com)
  - Adicionar ≥1 wikilink cross-galho (ex: `[[Dicionário de IA]]`, `[[Anatomia de Agents]]`)
  - Nota está 47 linhas abaixo do piso Adepto de 400 — se as mudanças acima não cruzarem, expandir "Estado da arte" ou aprofundar um caso prático
- **Resultado:** 353→401 linhas (cruzou piso). 2 seções novas ("Por que a ordem das fases não é arbitrária" + "Adaptando o playbook por perfil de time") + Caso 3 aprofundado. Wikilink `[[Anatomia de Agents]]` (folder-link, alvo confirmado) em "Veja também" — quita L1. **Verify:** docs.anthropic.com/.../prompt-caching 200, docs.helicone.ai/.../cost-tracking 200. **2 fontes NÃO confirmadas, deixadas sem link com anotação honesta (anti-fabricação):** artigo Simon Willison de título exato não achado (só a tag /tags/tokenization/), e "The LLM Cost Optimization Handbook (Leanpub)" ausente do catálogo — subagente não inventou URL.

#### 19 - Planos e tiers — Max, Pro, API, Enterprise   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-04)
- **Estado:** 372 linhas · fase: Adepto · status: growing
- **Núcleo/gaps:** P1, L2
- **Score:** 10/12
- **Plano de execução:**
  - Adicionar hiperlinks clicáveis às 4 referências (anthropic.com/pricing, openai.com/pricing, ai.google.dev/pricing, docs.litellm.ai)
  - Expandir "Estado da arte — junho 2026" (deflação de planos, multi-modal, Enterprise para times menores) ou aprofundar um caso prático com cálculo numérico — nota está 28 linhas abaixo do piso de 400
  - Adicionar `[!warning]`/`[!info]` de caducidade antes das tabelas de preços por provider (validade junho 2026)
- **Resultado:** 372→410 linhas (cruzou piso). Caso 5 (8 devs: 8 planos Max vs API centralizada, cálculo numérico **reusando as taxas já presentes na nota** — nenhum preço novo inventado) + `[!info]` da lição. 3 `[!warning]` de caducidade (validade junho 2026) antes das tabelas Claude/OpenAI/Google. **Verify:** anthropic.com/pricing 200, ai.google.dev/pricing 200, docs.litellm.ai/docs 200. **openai.com/pricing → 403 no curl (bloqueio de bot Cloudflare, não link morto; página real)** — mantida com a incerteza sinalizada. Nenhum preço existente alterado.

#### 20 - O futuro — tokens cada vez mais baratos   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-04)
- **Estado:** 288 linhas · fase: Adepto · status: growing
- **Núcleo/gaps:** E2, P1
- **Score:** 10/12
- **Plano de execução:**
  - Adicionar parágrafo de abertura com cenário concreto antes de "## A queda de preço mais rápida na história da tecnologia" (ex: orçamento de IA com projeções que parecem impossíveis)
  - Nota está 112 linhas abaixo do piso de 400 — abertura + caducidade + aprofundar "Estado da arte" ou um caso prático devem aproximar/cruzar o piso
  - Adicionar `[!warning]`/`[!info]` de caducidade antes da tabela de preços e de "Estado da arte — junho 2026" (projeções 2027-2028, GPT-5/Claude 5)
  - Adicionar URLs clicáveis às 4 referências (artificialanalysis.ai, ben-evans.com, github.com/vipulnaik, semianalysis.com)
- **Resultado:** 288→302 linhas (**gap residual: ainda ~98 abaixo do piso 400** — subagente priorizou substância sobre padding, correto pelo padrão capítulo-de-livro; expandir num ciclo futuro se quiser fechar o piso). Abertura-cenário (orçamento 2024 vs realidade 2028) + `[!warning]` (2027/2028 = projeção) + `[!info]` de caducidade antes de "Estado da arte jun/2026" + Caso 5 (consultoria de legado — **hipotético ilustrativo em 3ª pessoa "um consultor", NÃO caso real do usuário**; coordenador verificou = sem fabricação). **Verify:** 4 URLs 200 (artificialanalysis.ai/models, ben-evans.com, github.com/vipulnaik [perfil, não repo específico — anotado], semianalysis.com).

#### 21 - Hacks de trincheira — Claude, Gemini e Copilot em 2026   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-04)
- **Estado:** 409 linhas · fase: Adepto · status: growing
- **Núcleo/gaps:** L1, L2
- **Score:** 9/12
- **Plano de execução:**
  - Adicionar ≥1 wikilink cross-galho (ex: `[[Anatomia de Agents]]` ou `[[Agentes de Codificação]]`) — os 4 wikilinks atuais em "Veja também" são intra-galho
  - Substituir domínio+path em prosa por URLs Markdown clicáveis reais nas 4 fontes
  - Adicionar `[!warning]`/`[!info]` de caducidade na tabela de decisão e em "Estado da arte — junho 2026" (modelos, preços, AI Credits Copilot)
- **Resultado:** 409→415 linhas. Wikilink cross-galho `[[Agentes de Codificação]]` (folder-link, alvo confirmado) em "Veja também" — quita L1. `[!warning]` antes da "Tabela de decisão — motor por tipo de task" + `[!info]` em "Estado da arte — junho 2026". **Verify:** 5 URLs 200 (code.claude.com/docs/en/best-practices, ai.google.dev/gemini-api/docs/caching, 2× docs.github.com [billing + content-exclusion], github.com/oraios/serena). Nenhuma URL inventada.

#### 22 - Caso real — Auditoria de 47M tokens em maio 2026   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-04)
- **Estado:** 401 linhas · fase: Adepto · status: growing
- **Núcleo/gaps:** L1, P1
- **Score:** 10/12
- **Plano de execução:**
  - Adicionar ≥1 wikilink cross-galho em "O que vem a seguir" ou "Veja também" (ex: `[[Anatomia de Agents]]`, `[[Context Engineering]]`, `[[Agentes de Codificação]]`)
- **Resultado:** 401→402 linhas. Wikilink cross-galho `[[Anatomia de Agents]]` (folder-link, alvo confirmado) em "Veja também", ancorado no Vetor 3 (uso indevido de subagentes `general-purpose`) — quita L1. Escopo restrito: só o wikilink, nada mais alterado.
