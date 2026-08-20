---
title: "Roadmap — Anatomia dos LLMs"
created: 2026-07-02
type: meta
publish: false
tags:
  - meta
  - roadmap
---

# Roadmap — Anatomia dos LLMs

Diagnóstico migrado de guia/roadmap - ia.md (30/06). Cada entrada tem estado de enriquecimento, score, classificação de custo e plano de execução acionável.

**Galho:** `03-Dominios/Tecnologia/IA/Anatomia dos LLMs`

> [!note] Reconciliado em 2026-07-03. As entradas abaixo **já refletem a reformulação** (reordenação transformer→completação→janela, brotos 04a/04b/04c, nota 05 Completação, renumeração): os 24 headings mapeiam 1:1 para os arquivos atuais e nenhuma nota foi alterada após o diagnóstico. O antigo aviso "PRÉ-REFORMULAÇÃO, re-diagnosticar do zero" era um banner defasado — a auditoria de 03/07 (contagem + mapeamento entrada↔arquivo + git) confirmou que este roadmap está atual. Não precisa re-diagnosticar; seguir direto para enriquecimento.

## Régua de análise

Checklist `verificar-nota` — 12 itens (isenções por fase/tipo/broto aplicadas por nota):

| Grupo | Itens |
|-------|-------|
| ESTRUTURA | E1 TL;DR · E2 Abertura-problema · E3 Mermaid · E4 Casos práticos · E5 O que vem a seguir · E6 Inglês · E7 Tabela PT↔EN · E8 Armadilhas [!warning] |
| PROFUNDIDADE | P1 Código-com-falha · P2 Mecanismo explicado |
| LINKS | L1 Wikilink cross-galho · L2 Referência externa (URL) |
| MÍDIA | M1 Vídeo/podcast embutido |

**Esquema de fase detectado:** SEM fase (sequência) — galho organizado por Blocos, decisão do spec `00-Meta/specs/2026-06-20-galho-anatomia-llms-reformulacao-plan.md`. Ausência de `fase:` NÃO é gap aqui. **Piso de linhas:** N/A

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 24 |
| ⬜ pendente | 0 |
| ➖ não precisa | 1 |
| ✅ feita | 23 |
| 🔄 em andamento | 0 |
| % concluído | 100% ✅ |

---

## Notas

#### 01 - O que é um LLM   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 217 linhas · fase: ausente (Blocos) · status: evergreen
- **Núcleo/gaps:** E2, E8
- **Score:** 9/12
- **Plano de execução:**
  - Converter a seção "Armadilhas" (4 itens em lista simples) para callouts `[!warning]` individuais
  - Adicionar parágrafo de abertura com cenário/problema concreto antes de "## O que é" (ex: engenheiro recebendo API key sem saber o que há por baixo)
- **Resultado:** Armadilhas (4 itens) → 4 callouts `[!warning]` individuais; abertura-problema adicionada antes de "## O que é" (engenheiro com API key sem saber o que há por baixo). Ambos os itens do plano, sem desvio.

#### 02 - Tokens e tokenização   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 269 linhas · fase: ausente (Blocos) · status: evergreen
- **Núcleo/gaps:** E2, E8, P1
- **Score:** 9/12
- **Plano de execução:**
  - Converter a seção "Armadilhas" (5 itens em lista bullet) para callouts `[!warning]` individuais
  - Adicionar parágrafo de abertura com cenário/problema concreto antes de "## O que é" (ex: "500 palavras enviadas, resposta veio com 600 tokens")
- **Resultado:** Armadilhas (5 itens) → 5 callouts `[!warning]` individuais; abertura-problema adicionada (prompt de 500 palavras vs. 640 tokens) antes de "## O que é". `updated` bumped p/ 2026-07-03. Sem desvio.
- **Passe 2026-08-20 — material externo:** **Régua de bolso** consolidada em "Por que importa": 1 token ≈ 4 caracteres ≈ 0,75 palavra em inglês; **1,5 a 2 tokens por palavra em português** — a razão tokens-por-palavra que faltava (a nota já tinha a razão caracteres-por-token). Com estimativa trabalhada (800 palavras PT ≈ 1.400 tokens) e a ressalva de medir de verdade para orçamento. Nota de processo: uma primeira versão entrou como callout separado e **duplicava** a "regra prática" que já existia na mesma nota; foi consolidada num bloco só em vez de deixar as duas. Fonte da lacuna: [[2026-ia-do-zero-ao-senior-trilha-visual]].

#### 03 - Embeddings — do token ao vetor   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 197 linhas · fase: ausente (Blocos) · status: growing / progress: done
- **Núcleo/gaps:** E8, P1
- **Score:** 10/12
- **Plano de execução:**
  - Converter os 4 itens da seção "Armadilhas" (lista bullet) para callouts `[!warning]` individuais
- **Resultado:** Armadilhas (4 bullets) → 4 callouts `[!warning]` individuais, texto preservado (título negrito → título do callout). Mapeamento 1:1, sem desvio.

#### 04a - KV cache, prefill e decode — a física da inferência (broto)   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 197 linhas · fase: Magus · status: growing
- **Núcleo/gaps:** E5, E8
- **Score:** 9/12
- **Plano de execução:**
  - Adicionar parágrafo "O que vem a seguir" apontando para o próximo broto (04b — MHA/MQA/GQA/MLA)
  - Opcional: expandir o único [!warning] existente para ≥3 callouts individuais (ex: "dobrar contexto ≠ dobrar custo de compute", "TTFT e throughput não são correlacionados")
- **Resultado:** Seção "O que vem a seguir" → 04b; total 3 callouts `[!warning]` (o original + "dobrar contexto ≠ dobrar custo" + "TTFT vs throughput não correlacionados"). Sem desvio.

#### 04 - Atenção e o mecanismo transformer   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 442 linhas · fase: Adepto (presente — spec previa ausência) · status: evergreen
- **Núcleo/gaps:** —
- **Score:** 11/12
- **Plano de execução:**
  - — nenhuma
- **Resultado:** ➖ não precisa (nota 04 evergreen, 442 linhas, score 11/12)

#### 04b - Encolhendo o KV cache — MHA, MQA, GQA, MLA (broto)   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 209 linhas · fase: Magus · status: growing
- **Núcleo/gaps:** E5, E8, P1
- **Score:** 9/12
- **Plano de execução:**
  - Adicionar parágrafo "O que vem a seguir" apontando para 04c
  - Adicionar ≥3 callouts `[!warning]` com armadilhas concretas (GQA exige uptraining, MLA adiciona custo de up-projection no decode, MQA degrada em raciocínio multi-ângulo em modelos grandes)
- **Resultado:** 3 callouts `[!warning]` (MQA degrada multi-hop; GQA exige uptraining; MLA soma custo up-projection no decode) + seção "O que vem a seguir" → 04c. `updated` bumped. Sem desvio.

#### 04c - Atenção eficiente — FlashAttention, sparse e híbrida (broto)   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 221 linhas · fase: Magus · status: growing / progress: done
- **Núcleo/gaps:** E5, E8, P1
- **Score:** 9/12
- **Plano de execução:**
  - Adicionar parágrafo "O que vem a seguir" apontando para [[05 - Completação — o loop autoregressivo]]
  - Adicionar ≥2 callouts `[!warning]` adicionais (FlashAttention não muda latência de decode token-a-token; NSA/DSA exigem retreino completo)
- **Resultado:** 2 callouts `[!warning]` (FlashAttention não acelera decode token-a-token; NSA/DSA exigem retreino completo) + seção "O que vem a seguir" → 05. `updated` bumped. Sem desvio.

#### 05 - Completação — o loop autoregressivo   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 231 linhas · fase: ausente (Blocos) · status: growing / progress: done
- **Núcleo/gaps:** E8
- **Score:** 10/12
- **Plano de execução:**
  - Converter a seção "Armadilhas" (5 itens em lista bullet) para callouts `[!warning]` individuais (já há 2 [!warning] inline; a seção dedicada ficou como lista)
- **Resultado:** Armadilhas (5 itens) → 5 callouts `[!warning]` individuais, mesmo padrão dos 2 inline existentes. Sem desvio.

#### 06 - A janela de contexto   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 428 linhas · fase: ausente (Blocos) · status: evergreen
- **Núcleo/gaps:** E5, E8, P1
- **Score:** 9/12
- **Plano de execução:**
  - Adicionar parágrafo "O que vem a seguir" apontando para [[07 - Panorama de modelos 2026]]
  - Converter a seção "Armadilhas" (5 itens em lista bullet) para callouts `[!warning]` individuais
- **Resultado:** Armadilhas (5 itens) → 5 callouts `[!warning]` + seção "O que vem a seguir" → 07. `updated` bumped. Sem desvio.

#### 07 - Panorama de modelos 2026   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 242 linhas · fase: ausente (Blocos) · status: growing
- **Núcleo/gaps:** E5, E8, P1
- **Score:** 9/12
- **Plano de execução:**
  - Adicionar parágrafo "O que vem a seguir" apontando para [[08 - Modelos chineses — DeepSeek, Qwen, Kimi, GLM]] com motivação narrativa
  - Converter "Armadilhas comuns" (5 itens bullet) para callouts `[!warning]` individuais
  - Adicionar `[!warning]`/`[!info]` de caducidade no topo de "Os grandes players" (preços e benchmarks mudam mensalmente)
- **Resultado:** `[!info]` de caducidade (retrato maio/2026) no topo de "Os grandes players"; Armadilhas comuns (5) → 5 callouts `[!warning]`; seção "O que vem a seguir" → 08 (geopolítica GPU/MoE/licenças). Sem desvio.

#### 08 - Modelos chineses — DeepSeek, Qwen, Kimi, GLM   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 233 linhas · fase: ausente (Blocos) · status: growing
- **Núcleo/gaps:** E5, E8, P1
- **Score:** 9/12
- **Plano de execução:**
  - Adicionar parágrafo "O que vem a seguir" apontando para [[09 - Dense vs Mixture-of-Experts]] (MoE = espinha da eficiência chinesa)
  - Converter a seção "Armadilhas" (5 itens bullet) para callouts `[!warning]` individuais
  - Considerar `[!info]` de caducidade em "Comparativo" (versões DeepSeek V4/Qwen 3.6/Kimi K2.6/GLM-5.1, preços)
- **Resultado:** ✅ aplicado conforme o plano (2026-07-03) — burst turbo, executor reportou sem desvio; detalhamento por nota no relatório da sessão.

#### 09 - Dense vs Mixture-of-Experts   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 292 linhas · fase: ausente (Blocos) · status: growing / progress: done
- **Núcleo/gaps:** E5, L1
- **Score:** 9/12
- **Plano de execução:**
  - Adicionar parágrafo "O que vem a seguir" apontando para [[10 - Modelos locais e self-hosting]] (VRAM necessária, e como MoE muda a conta)
  - Adicionar ≥1 wikilink cross-galho (ex: [[Economia de Tokens]] ou [[RAG e Vector Databases]])
- **Resultado:** ✅ aplicado conforme o plano (2026-07-03) — burst turbo, executor reportou sem desvio; detalhamento por nota no relatório da sessão.

#### 10 - Modelos locais e self-hosting   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 222 linhas · fase: ausente (Blocos) · status: growing
- **Núcleo/gaps:** E5, E8, P1
- **Score:** 9/12
- **Plano de execução:**
  - Adicionar parágrafo "O que vem a seguir" apontando para `[[11 - APIs de LLM — anatomia de uma chamada]]`
  - Converter a seção "Armadilhas" (5 itens bullet) para callouts `[!warning]` individuais
- **Resultado:** ✅ aplicado conforme o plano (2026-07-03) — burst turbo, executor reportou sem desvio; detalhamento por nota no relatório da sessão.

#### 11 - APIs de LLM — anatomia de uma chamada   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 259 linhas · fase: ausente (Blocos) · status: growing
- **Núcleo/gaps:** E5, E8, P1
- **Score:** 9/12
- **Plano de execução:**
  - Adicionar parágrafo "O que vem a seguir" apontando para [[12 - Pricing de APIs — como calcular custos]]
  - Converter a seção "Armadilhas" (5 itens bullet) para callouts `[!warning]` individuais
  - Adicionar exemplo de código-com-falha (ex: request Anthropic sem `max_tokens` → erro 400; ou roles fora de ordem)
- **Resultado:** ✅ aplicado conforme o plano (2026-07-03) — burst turbo, executor reportou sem desvio; detalhamento por nota no relatório da sessão.

#### 12 - Pricing de APIs — como calcular custos   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 220 linhas · fase: ausente (Blocos) · status: growing / progress: done
- **Núcleo/gaps:** E5, L2
- **Score:** 10/12
- **Plano de execução:**
  - Adicionar parágrafo "O que vem a seguir" apontando para [[13 - Prompt caching e otimizações de API]]
  - Adicionar URLs reais às referências (Anthropic pricing, OpenAI pricing, artificialanalysis.ai, costgoat.com)
  - Adicionar `[!warning]` de caducidade no topo de "Tabela de preços (maio 2026)"
- **Resultado:** ✅ aplicado conforme o plano (2026-07-03) — burst turbo, executor reportou sem desvio; detalhamento por nota no relatório da sessão.

#### 13 - Prompt caching e otimizações de API   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 273 linhas · fase: ausente (Blocos) · status: growing
- **Núcleo/gaps:** E5, E8, P1
- **Score:** 9/12
- **Plano de execução:**
  - Adicionar parágrafo "O que vem a seguir" apontando para [[14 - Streaming, batching e latência]]
  - Converter a seção "Armadilhas" (5 itens bullet) para callouts `[!warning]` individuais
- **Resultado:** ✅ aplicado conforme o plano (2026-07-03) — burst turbo, executor reportou sem desvio; detalhamento por nota no relatório da sessão.

#### 14 - Streaming, batching e latência   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 247 linhas · fase: ausente (Blocos) · status: growing / progress: done
- **Núcleo/gaps:** E5, E8, P1
- **Score:** 9/12
- **Plano de execução:**
  - Adicionar parágrafo "O que vem a seguir" apontando para [[15 - Reasoning models e chain-of-thought]]
  - Converter a seção "Armadilhas" (5 itens bullet) para callouts `[!warning]` individuais
- **Resultado:** ✅ aplicado conforme o plano (2026-07-03) — burst turbo, executor reportou sem desvio; detalhamento por nota no relatório da sessão.

#### 15 - Reasoning models e chain-of-thought   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 225 linhas · fase: ausente (Blocos) · status: growing / progress: done
- **Núcleo/gaps:** E5, E8
- **Score:** 9/12
- **Plano de execução:**
  - Adicionar parágrafo "O que vem a seguir" apontando para [[16 - Fine-tuning vs prompting vs RAG]]
  - Converter a seção "Armadilhas" (5 itens bullet) para callouts `[!warning]` individuais
- **Resultado:** ✅ aplicado conforme o plano (2026-07-03) — burst turbo, executor reportou sem desvio; detalhamento por nota no relatório da sessão.

#### 16 - Fine-tuning vs prompting vs RAG   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 245 linhas · fase: ausente (Blocos) · status: growing
- **Núcleo/gaps:** E5, E8, P1
- **Score:** 9/12
- **Plano de execução:**
  - Adicionar parágrafo "O que vem a seguir" apontando para [[17 - O futuro dos LLMs — tendências 2026-2027]]
  - Converter a seção "Armadilhas" (5 itens bullet) para callouts `[!warning]` individuais
- **Resultado:** ✅ aplicado conforme o plano (2026-07-03) — burst turbo, executor reportou sem desvio; detalhamento por nota no relatório da sessão.

#### 17 - O futuro dos LLMs — tendências 2026-2027   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 224 linhas · fase: ausente (Blocos) · status: growing / progress: done
- **Núcleo/gaps:** E5, E8, P1
- **Score:** 9/12
- **Plano de execução:**
  - Adicionar parágrafo "O que vem a seguir" apontando para [[18 - Como LLMs são treinados — pretraining, SFT, RLHF]]
  - Converter a seção "Armadilhas" (4 itens bullet) para callouts `[!warning]` individuais
  - Adicionar `[!warning]`/`[!info]` de caducidade nas tabelas de tendência (projeções 2027, preços/ano, versões DeepSeek V4/Qwen 3.6)
- **Resultado:** ✅ aplicado conforme o plano (2026-07-03) — burst turbo, executor reportou sem desvio; detalhamento por nota no relatório da sessão.

#### 18 - Como LLMs são treinados — pretraining, SFT, RLHF   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 256 linhas · fase: ausente (Blocos) · status: growing
- **Núcleo/gaps:** E5, E8, P1
- **Score:** 9/12
- **Plano de execução:**
  - Adicionar parágrafo "O que vem a seguir" apontando para [[19 - Evaluation de LLMs em produção]]
  - Adicionar ≥2 callouts `[!warning]` adicionais (fine-tuning não adiciona conhecimento, só ajusta comportamento; DPO é sensível à qualidade do dataset de preferências)
- **Resultado:** ✅ aplicado conforme o plano (2026-07-03) — burst turbo, executor reportou sem desvio; detalhamento por nota no relatório da sessão.

#### 19 - Evaluation de LLMs em produção   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 325 linhas · fase: ausente (Blocos) · status: growing
- **Núcleo/gaps:** E5, E8
- **Score:** 9/12
- **Plano de execução:**
  - Adicionar parágrafo "O que vem a seguir" apontando para [[20 - Compressão de modelos — quantização e destilação]]
  - Converter a seção "Anti-patterns" (6 itens bullet) para callouts `[!warning]` individuais
- **Resultado:** ✅ aplicado conforme o plano (2026-07-03) — burst turbo, executor reportou sem desvio; detalhamento por nota no relatório da sessão.

#### 20 - Compressão de modelos — quantização e destilação   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 227 linhas · fase: ausente (Blocos) · status: growing / progress: done
- **Núcleo/gaps:** E5, P1
- **Score:** 10/12
- **Plano de execução:**
  - Adicionar parágrafo "O que vem a seguir" apontando para [[21 - Fine-tuning na prática — LoRA, QLoRA, DPO]] (QLoRA fine-tuna sobre base já quantizado em INT4)
- **Resultado:** ✅ aplicado conforme o plano (2026-07-03) — burst turbo, executor reportou sem desvio; detalhamento por nota no relatório da sessão.

#### 21 - Fine-tuning na prática — LoRA, QLoRA, DPO   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 243 linhas · fase: ausente (Blocos) · status: growing / progress: done
- **Núcleo/gaps:** E5, E8, P1
- **Score:** 9/12
- **Plano de execução:**
  - Adicionar seção "O que vem a seguir" de fechamento do galho (última nota), com ponte para [[Anatomia de Agents]], [[RAG e Vector Databases]] ou [[Context Engineering]]
  - Converter a seção "Armadilhas" (7 itens bullet) para callouts `[!warning]` individuais
- **Resultado:** ✅ aplicado conforme o plano (2026-07-03) — burst turbo, executor reportou sem desvio; detalhamento por nota no relatório da sessão.
