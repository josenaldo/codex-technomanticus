---
title: "Roadmap — AI Engineering Stack"
created: 2026-07-02
type: meta
publish: false
tags:
  - meta
  - roadmap
---

# Roadmap — AI Engineering Stack

Diagnóstico migrado de guia/roadmap - ia.md (30/06). Cada entrada tem estado de enriquecimento, score, classificação de custo e plano de execução acionável.

**Galho:** `03-Dominios/Tecnologia/IA/AI Engineering Stack`

> [!warning] Diagnóstico de 30/06 — pode estar defasado. Vários itens marcados ⬜ podem já ter sido enriquecidos depois; reconciliar com o estado real ao tratar o galho.

## Régua de análise

Checklist `verificar-nota` — 12 itens (isenções por fase/tipo/broto aplicadas por nota):

| Grupo | Itens |
|-------|-------|
| ESTRUTURA | E1 TL;DR · E2 Abertura-problema · E3 Mermaid · E4 Casos práticos · E5 O que vem a seguir · E6 Inglês · E7 Tabela PT↔EN · E8 Armadilhas [!warning] |
| PROFUNDIDADE | P1 Código-com-falha · P2 Mecanismo explicado |
| LINKS | L1 Wikilink cross-galho · L2 Referência externa (URL) |
| MÍDIA | M1 Vídeo/podcast embutido |

**Esquema de `fase:` detectado:** COM fase (Iniciado 01–12, Adepto 13) **Piso de linhas:** aplicável — Iniciado ≥300; Adepto ≥400

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 13 |
| ⬜ pendente | 0 |
| ➖ não precisa | 1 |
| ✅ feita | 12 |
| 🔄 em andamento | 0 |
| % concluído | 100% |

---

## Notas

#### 01 - As 11 camadas — visão geral   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 308 linhas · fase: Iniciado · status: seedling
- **Núcleo/gaps:** P1
- **Score:** 11/12
- **Plano de execução:**
  - — nenhuma
- **Resultado:** —

#### 02 - Purpose Layer — o que o sistema é   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-05)
- **Estado:** 305 linhas · fase: Iniciado · status: seedling
- **Núcleo/gaps:** P1
- **Score:** 11/12
- **Plano de execução:**
  - Remover a seção "Como explicar em inglês" duplicada (aparece duas vezes: linhas ~138 e ~159); manter a segunda versão (mais completa, com tabela PT↔EN) e excluir a primeira
- **Resultado:** Removida a seção "Como explicar em inglês" duplicada (a primeira, mais curta); mantida a versão completa com tabela PT↔EN. Verificação confirma ocorrência única do cabeçalho. Corte cirúrgico determinístico.

#### 03 - Prompt Layer   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-05)
- **Estado:** 305 linhas totais (~204 de conteúdo efetivo; linhas 205-305 são em branco) · fase: Iniciado · status: seedling
- **Núcleo/gaps:** P1
- **Score:** 11/12
- **Plano de execução:**
  - Purgar as ~100 linhas em branco no fim do arquivo (linhas 205-305)
  - Adicionar exemplo de código-com-falha: system prompt minimalista causando comportamento inesperado em produção (ex: prompt sem `uncertainty_behavior` → modelo inventa resposta em vez de escalar) — ativa P1
  - Expandir "Decisões-chave"/"Anatomia" com exemplo trabalhado adicional para aproximar o conteúdo efetivo do piso de 300 linhas
- **Resultado:** Purgadas ~100 linhas em branco. Adicionado "Cenário 3 — prompt minimalista que inventa resposta em vez de escalar" (YAML sem `uncertainty_behavior` + callout [!danger]) ativando P1, e "Exemplo trabalhado — do template vazio ao system prompt completo". Arquivo 204→261 linhas. ⚠️ Desvio: não atingiu o piso de 300 (T1 reprova); os outros 10/11 itens passam.

#### 04 - Context Layer   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-05)
- **Estado:** 190 linhas (linhas 191–305 são branco) · fase: Iniciado · status: seedling
- **Núcleo/gaps:** P1
- **Score:** 11/12
- **Plano de execução:**
  - Expandir o conteúdo efetivo de ~190 para ≥300 linhas — candidatos: aprofundar "Decisões-chave" com exemplos trabalhados (ex: pull vs push com comparativo de custo por chamada), subseção "Context pipelines na prática" (compressão periódica, expiração por horizonte, reset por unidade de trabalho), ou terceiro cenário prático
  - Purgar as ~115 linhas em branco no fim do arquivo
- **Resultado:** Aprofundado "Decisões-chave" com 3 exemplos trabalhados (custo pull vs push com tabela 8×, compressão vs fidelidade, teste de persistência); nova subseção "Context pipelines na prática" (Mermaid + 3 mecanismos); Cenário 3 (agent de triagem amarrando os mecanismos) + novo [!warning] sobre reset agressivo. Purgadas ~115 linhas em branco. 190→300 linhas efetivas — bate o piso T1.

#### 05 - Output Layer   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-05)
- **Estado:** 201 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** P1
- **Score:** 11/12
- **Plano de execução:**
  - Expandir de 201 para ≥300 linhas — candidatos: subseção "Validação pós-output", exemplos trabalhados de schema rígido vs leve, ou terceiro cenário prático (ex: sistema de geração de código com output como ação direta)
  - Adicionar bloco de código-com-falha (ex: parser Python quebrando com prosa antes do `{`; ou Pydantic rejeitando campo extra inesperado) — ativa P1
  - Purgar as ~105 linhas em branco no fim do arquivo
- **Resultado:** 201→300 linhas. Nova subseção "Validação pós-output" (json.loads quebrando por prosa antes do `{` + Pydantic `extra="forbid"`) ativando P1; "Cenário 3 — Output como ação direta: geração de código"; worked example "Schema rígido vs leve" lado a lado. Purgadas ~105 linhas em branco. Sem desvio.

#### 06 - Retrieval Layer   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-05)
- **Estado:** 241 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** P1
- **Score:** 11/12
- **Plano de execução:**
  - Expandir de 241 para ≥300 linhas — candidatos: aprofundar "Métricas de qualidade do retrieval" com exemplos numéricos concretos, Cenário 3 (conflito entre fontes desatualizadas em sistema jurídico), ou expandir "Implementações comuns" com snippet de hybrid search + reranker (BM25 → embedding → cross-encoder)
  - Purgar as ~62 linhas em branco no fim do arquivo
- **Resultado:** 241→300 linhas. "Métricas de qualidade" com exemplo numérico (recall@10=0,6, precision@10=0,3, MRR=0,25) + benchmarks; Cenário 3 (conflito lei revogada×vigente×blog em sistema jurídico) com `conflict_rule`; "Implementações comuns" com pipeline hybrid search (BM25→RRF→cross-encoder) + orçamento de latência. Purgadas ~62 linhas. Sem desvio.

#### 07 - Tool Layer   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-05)
- **Estado:** 219 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** P1
- **Score:** 11/12
- **Plano de execução:**
  - Expandir de 219 para ≥300 linhas — candidatos: (a) Cenário 3 mostrando tool failure handling na prática (retry+fallback evitando duplicação); (b) aprofundar "Tool design é trabalho de engenharia" com schema bem vs mal descrito lado a lado (ativa também P1); (c) expandir "Categorias de tools" com exemplos concretos em código
- **Resultado:** 219→363 linhas (11/12). Cenário 3 "Failure handling" (diagrama de sequência: timeout ambíguo→ticket duplicado→idempotency key); item 5 de "Decisões-chave" com schema mal×bem descrito lado a lado (ativa P1); 5 "Categorias de tools" com snippets Python (read-only, write idempotente, destructive c/ aprovação, compute puro, integration). status→growing. Sem desvio.

#### 08 - Workflow vs Agent Layer   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-06)
- **Estado:** 201 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** P1
- **Score:** 11/12
- **Plano de execução:**
  - Expandir de 201 para ≥300 linhas — candidatos: (a) Cenário 3 cobrindo caso limítrofe que migrou de workflow para agent; (b) seção de frameworks que implementam a distinção (LangGraph vs Prefect/Temporal); (c) snippet código-com-falha (loop agentic sem kill switch esgotando contexto) — ativa P1
- **Resultado:** 202→300 linhas (11/12). Cenário 3 (suporte que migrou de routing→agent aos 40+ tipos de ticket); seção "Frameworks" (LangGraph vs Temporal/Prefect, tabela + Mermaid do padrão híbrido); snippet com falha (loop sem kill switch estourando contexto) + versão com `max_iterations`/`max_cost_usd` ativando P1. status→growing. Sem desvio.

#### 09 - Evaluation Layer   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-06)
- **Estado:** 199 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** P1
- **Score:** 11/12
- **Plano de execução:**
  - Expandir de 199 para ≥300 linhas — candidatos: (a) seção "Ferramentas de eval" (Braintrust, PromptFoo, LangSmith, Ragas); (b) expandir "Tipos de eval" com exemplos YAML/JSON para reference-based e reference-free; (c) Cenário 3 cobrindo eval de sistema RAG (recall@k, faithfulness, answer relevance)
- **Resultado:** 199→301 linhas. Seção "Ferramentas de eval" (Braintrust/PromptFoo/LangSmith/Ragas + tabela); "Tipos de eval" com exemplo JSON reference-based e YAML reference-free; Cenário 3 (eval de RAG: recall@k/faithfulness/answer relevance + rubrica YAML). Purgadas ~100 linhas. Sem desvio.

#### 10 - Guardrail Layer   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-06)
- **Estado:** 199 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** P1
- **Score:** 11/12
- **Plano de execução:**
  - Expandir de 199 para ≥300 linhas — candidatos: (a) seção "Ferramentas de guardrail" (NeMo Guardrails, Guardrails AI, LangChain moderation); (b) expandir "Calibrando thresholds" com exemplo de log de disparo e ajuste; (c) Cenário 3 cobrindo guardrail de PII em sistema de saúde
- **Resultado:** 199→305 linhas. Seção "Ferramentas de guardrail" (NeMo/Guardrails AI/LangChain moderation + tabela, 3 fontes); "Calibrando thresholds" com log JSON de disparo + ajuste de regex (FP 30%→2%); Cenário 3 (PII em saúde, LGPD/HIPAA, pre/post-LLM/tool-call). status→growing, 3 fontes. Purgadas ~100 linhas.

#### 11 - Logging Layer   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-06)
- **Estado:** 211 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** P1
- **Score:** 11/12
- **Plano de execução:**
  - Expandir de 211 para ≥300 linhas — candidatos: (a) seção "Ferramentas de logging" (OpenTelemetry GenAI, Langfuse, Phoenix, Datadog); (b) expandir cada um dos 3 `[!warning]` com resolução concreta; (c) Cenário 3 cobrindo estratégia de sampling em sistema de alto volume
- **Resultado:** 211→300 linhas. Seção "Ferramentas de logging" (OTel GenAI/Langfuse/Phoenix/Datadog + tabela self-host×gerenciado); 3 [!warning] com resolução (checklist dia-1, teste de queryabilidade, redação de PII default-on); Cenário 3 (sampling em 500k execuções/dia, YAML). status→growing. Sem desvio.

#### 12 - Improvement Layer   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-06)
- **Estado:** 203 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** P1
- **Score:** 11/12
- **Plano de execução:**
  - Expandir de 203 para ≥300 linhas — candidatos: (a) expandir cada um dos 3 `[!warning]` com resolução concreta; (b) Cenário 3 cobrindo drift detection automático (alertas de score + threshold); (c) subseção "Ferramentas" comparando Langfuse, Phoenix e Datadog GenAI
- **Resultado:** 203→300 linhas. 3 [!warning] com resolução (Logging mínima, ata com dono/prazo, versionamento de prompt); Cenário 3 (drift detection automático, YAML de alerta + calibração anti-fadiga); seção "Ferramentas" (Langfuse/Phoenix/Datadog LLM Obs + tabela, 3 fontes). status→growing. Sem desvio.

#### 13 - Setup completo — do zero ao sistema de produção   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-06)
- **Estado:** ~390 linhas reais · fase: Adepto · status: seedling
- **Núcleo/gaps:** P1
- **Score:** 11/12
- **Plano de execução:**
  - Expandir ~10 linhas para atingir o piso de 400 — candidatos: (a) 4º `[!warning]` cobrindo "começar a construir todas as camadas ao mesmo tempo antes de validar a Purpose Layer"; (b) expandir o checklist final com sub-itens de rollback — OU aplicar isenção de capstone (última nota do galho, funciona como recipe de fechamento do ciclo)
  - Corrigir `status: seedling` → `growing` no frontmatter — a nota está substancialmente completa (11/12, núcleo integral, seção de ponte para outros galhos)
- **Resultado:** 405→411 linhas (piso Adepto ≥400 atingido). 4º [!warning] (construir todas as camadas antes de validar a Purpose Layer); checklist de rollback expandido (4 sub-itens: git, critério de disparo, feature flag, notificação do owner). status→growing. 11/12. Sem desvio.
