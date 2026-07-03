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

**Esquema de fase detectado:** SEM fase (sequência) — galho organizado por Blocos, decisão do spec `00-Meta/specs/2026-06-20-galho-anatomia-llms-reformulacao-plan.md`. Ausência de `fase:` NÃO é gap aqui.
**Piso de linhas:** N/A

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 24 |
| ⬜ pendente | 23 |
| ➖ não precisa | 1 |
| ✅ feita | 0 |
| 🔄 em andamento | 0 |
| % concluído | 0% |

---

## Notas

#### 01 - O que é um LLM   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 217 linhas · fase: ausente (Blocos) · status: evergreen
- **Núcleo/gaps:** E2, E8
- **Score:** 9/12
- **Plano de execução:**
  - Converter a seção "Armadilhas" (4 itens em lista simples) para callouts `[!warning]` individuais
  - Adicionar parágrafo de abertura com cenário/problema concreto antes de "## O que é" (ex: engenheiro recebendo API key sem saber o que há por baixo)
- **Resultado:** —

#### 02 - Tokens e tokenização   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 254 linhas · fase: ausente (Blocos) · status: evergreen
- **Núcleo/gaps:** E2, E8, P1
- **Score:** 9/12
- **Plano de execução:**
  - Converter a seção "Armadilhas" (5 itens em lista bullet) para callouts `[!warning]` individuais
  - Adicionar parágrafo de abertura com cenário/problema concreto antes de "## O que é" (ex: "500 palavras enviadas, resposta veio com 600 tokens")
- **Resultado:** —

#### 03 - Embeddings — do token ao vetor   [mecânico]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 197 linhas · fase: ausente (Blocos) · status: growing / progress: done
- **Núcleo/gaps:** E8, P1
- **Score:** 10/12
- **Plano de execução:**
  - Converter os 4 itens da seção "Armadilhas" (lista bullet) para callouts `[!warning]` individuais
- **Resultado:** —

#### 04a - KV cache, prefill e decode — a física da inferência (broto)   [mecânico]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 197 linhas · fase: Magus · status: growing
- **Núcleo/gaps:** E5, E8
- **Score:** 9/12
- **Plano de execução:**
  - Adicionar parágrafo "O que vem a seguir" apontando para o próximo broto (04b — MHA/MQA/GQA/MLA)
  - Opcional: expandir o único [!warning] existente para ≥3 callouts individuais (ex: "dobrar contexto ≠ dobrar custo de compute", "TTFT e throughput não são correlacionados")
- **Resultado:** —

#### 04 - Atenção e o mecanismo transformer   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 442 linhas · fase: Adepto (presente — spec previa ausência) · status: evergreen
- **Núcleo/gaps:** —
- **Score:** 11/12
- **Plano de execução:**
  - — nenhuma
- **Resultado:** —

#### 04b - Encolhendo o KV cache — MHA, MQA, GQA, MLA (broto)   [mecânico]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 209 linhas · fase: Magus · status: growing
- **Núcleo/gaps:** E5, E8, P1
- **Score:** 9/12
- **Plano de execução:**
  - Adicionar parágrafo "O que vem a seguir" apontando para 04c
  - Adicionar ≥3 callouts `[!warning]` com armadilhas concretas (GQA exige uptraining, MLA adiciona custo de up-projection no decode, MQA degrada em raciocínio multi-ângulo em modelos grandes)
- **Resultado:** —

#### 04c - Atenção eficiente — FlashAttention, sparse e híbrida (broto)   [mecânico]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 221 linhas · fase: Magus · status: growing / progress: done
- **Núcleo/gaps:** E5, E8, P1
- **Score:** 9/12
- **Plano de execução:**
  - Adicionar parágrafo "O que vem a seguir" apontando para [[05 - Completação — o loop autoregressivo]]
  - Adicionar ≥2 callouts `[!warning]` adicionais (FlashAttention não muda latência de decode token-a-token; NSA/DSA exigem retreino completo)
- **Resultado:** —

#### 05 - Completação — o loop autoregressivo   [mecânico]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 231 linhas · fase: ausente (Blocos) · status: growing / progress: done
- **Núcleo/gaps:** E8
- **Score:** 10/12
- **Plano de execução:**
  - Converter a seção "Armadilhas" (5 itens em lista bullet) para callouts `[!warning]` individuais (já há 2 [!warning] inline; a seção dedicada ficou como lista)
- **Resultado:** —

#### 06 - A janela de contexto   [mecânico]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 428 linhas · fase: ausente (Blocos) · status: evergreen
- **Núcleo/gaps:** E5, E8, P1
- **Score:** 9/12
- **Plano de execução:**
  - Adicionar parágrafo "O que vem a seguir" apontando para [[07 - Panorama de modelos 2026]]
  - Converter a seção "Armadilhas" (5 itens em lista bullet) para callouts `[!warning]` individuais
- **Resultado:** —

#### 07 - Panorama de modelos 2026   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 242 linhas · fase: ausente (Blocos) · status: growing
- **Núcleo/gaps:** E5, E8, P1
- **Score:** 9/12
- **Plano de execução:**
  - Adicionar parágrafo "O que vem a seguir" apontando para [[08 - Modelos chineses — DeepSeek, Qwen, Kimi, GLM]] com motivação narrativa
  - Converter "Armadilhas comuns" (5 itens bullet) para callouts `[!warning]` individuais
  - Adicionar `[!warning]`/`[!info]` de caducidade no topo de "Os grandes players" (preços e benchmarks mudam mensalmente)
- **Resultado:** —

#### 08 - Modelos chineses — DeepSeek, Qwen, Kimi, GLM   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 233 linhas · fase: ausente (Blocos) · status: growing
- **Núcleo/gaps:** E5, E8, P1
- **Score:** 9/12
- **Plano de execução:**
  - Adicionar parágrafo "O que vem a seguir" apontando para [[09 - Dense vs Mixture-of-Experts]] (MoE = espinha da eficiência chinesa)
  - Converter a seção "Armadilhas" (5 itens bullet) para callouts `[!warning]` individuais
  - Considerar `[!info]` de caducidade em "Comparativo" (versões DeepSeek V4/Qwen 3.6/Kimi K2.6/GLM-5.1, preços)
- **Resultado:** —

#### 09 - Dense vs Mixture-of-Experts   [mecânico]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 292 linhas · fase: ausente (Blocos) · status: growing / progress: done
- **Núcleo/gaps:** E5, L1
- **Score:** 9/12
- **Plano de execução:**
  - Adicionar parágrafo "O que vem a seguir" apontando para [[10 - Modelos locais e self-hosting]] (VRAM necessária, e como MoE muda a conta)
  - Adicionar ≥1 wikilink cross-galho (ex: [[Economia de Tokens]] ou [[RAG e Vector Databases]])
- **Resultado:** —

#### 10 - Modelos locais e self-hosting   [mecânico]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 222 linhas · fase: ausente (Blocos) · status: growing
- **Núcleo/gaps:** E5, E8, P1
- **Score:** 9/12
- **Plano de execução:**
  - Adicionar parágrafo "O que vem a seguir" apontando para `[[11 - APIs de LLM — anatomia de uma chamada]]`
  - Converter a seção "Armadilhas" (5 itens bullet) para callouts `[!warning]` individuais
- **Resultado:** —

#### 11 - APIs de LLM — anatomia de uma chamada   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 259 linhas · fase: ausente (Blocos) · status: growing
- **Núcleo/gaps:** E5, E8, P1
- **Score:** 9/12
- **Plano de execução:**
  - Adicionar parágrafo "O que vem a seguir" apontando para [[12 - Pricing de APIs — como calcular custos]]
  - Converter a seção "Armadilhas" (5 itens bullet) para callouts `[!warning]` individuais
  - Adicionar exemplo de código-com-falha (ex: request Anthropic sem `max_tokens` → erro 400; ou roles fora de ordem)
- **Resultado:** —

#### 12 - Pricing de APIs — como calcular custos   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 220 linhas · fase: ausente (Blocos) · status: growing / progress: done
- **Núcleo/gaps:** E5, L2
- **Score:** 10/12
- **Plano de execução:**
  - Adicionar parágrafo "O que vem a seguir" apontando para [[13 - Prompt caching e otimizações de API]]
  - Adicionar URLs reais às referências (Anthropic pricing, OpenAI pricing, artificialanalysis.ai, costgoat.com)
  - Adicionar `[!warning]` de caducidade no topo de "Tabela de preços (maio 2026)"
- **Resultado:** —

#### 13 - Prompt caching e otimizações de API   [mecânico]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 273 linhas · fase: ausente (Blocos) · status: growing
- **Núcleo/gaps:** E5, E8, P1
- **Score:** 9/12
- **Plano de execução:**
  - Adicionar parágrafo "O que vem a seguir" apontando para [[14 - Streaming, batching e latência]]
  - Converter a seção "Armadilhas" (5 itens bullet) para callouts `[!warning]` individuais
- **Resultado:** —

#### 14 - Streaming, batching e latência   [mecânico]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 247 linhas · fase: ausente (Blocos) · status: growing / progress: done
- **Núcleo/gaps:** E5, E8, P1
- **Score:** 9/12
- **Plano de execução:**
  - Adicionar parágrafo "O que vem a seguir" apontando para [[15 - Reasoning models e chain-of-thought]]
  - Converter a seção "Armadilhas" (5 itens bullet) para callouts `[!warning]` individuais
- **Resultado:** —

#### 15 - Reasoning models e chain-of-thought   [mecânico]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 225 linhas · fase: ausente (Blocos) · status: growing / progress: done
- **Núcleo/gaps:** E5, E8
- **Score:** 9/12
- **Plano de execução:**
  - Adicionar parágrafo "O que vem a seguir" apontando para [[16 - Fine-tuning vs prompting vs RAG]]
  - Converter a seção "Armadilhas" (5 itens bullet) para callouts `[!warning]` individuais
- **Resultado:** —

#### 16 - Fine-tuning vs prompting vs RAG   [mecânico]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 245 linhas · fase: ausente (Blocos) · status: growing
- **Núcleo/gaps:** E5, E8, P1
- **Score:** 9/12
- **Plano de execução:**
  - Adicionar parágrafo "O que vem a seguir" apontando para [[17 - O futuro dos LLMs — tendências 2026-2027]]
  - Converter a seção "Armadilhas" (5 itens bullet) para callouts `[!warning]` individuais
- **Resultado:** —

#### 17 - O futuro dos LLMs — tendências 2026-2027   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 224 linhas · fase: ausente (Blocos) · status: growing / progress: done
- **Núcleo/gaps:** E5, E8, P1
- **Score:** 9/12
- **Plano de execução:**
  - Adicionar parágrafo "O que vem a seguir" apontando para [[18 - Como LLMs são treinados — pretraining, SFT, RLHF]]
  - Converter a seção "Armadilhas" (4 itens bullet) para callouts `[!warning]` individuais
  - Adicionar `[!warning]`/`[!info]` de caducidade nas tabelas de tendência (projeções 2027, preços/ano, versões DeepSeek V4/Qwen 3.6)
- **Resultado:** —

#### 18 - Como LLMs são treinados — pretraining, SFT, RLHF   [mecânico]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 256 linhas · fase: ausente (Blocos) · status: growing
- **Núcleo/gaps:** E5, E8, P1
- **Score:** 9/12
- **Plano de execução:**
  - Adicionar parágrafo "O que vem a seguir" apontando para [[19 - Evaluation de LLMs em produção]]
  - Adicionar ≥2 callouts `[!warning]` adicionais (fine-tuning não adiciona conhecimento, só ajusta comportamento; DPO é sensível à qualidade do dataset de preferências)
- **Resultado:** —

#### 19 - Evaluation de LLMs em produção   [mecânico]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 325 linhas · fase: ausente (Blocos) · status: growing
- **Núcleo/gaps:** E5, E8
- **Score:** 9/12
- **Plano de execução:**
  - Adicionar parágrafo "O que vem a seguir" apontando para [[20 - Compressão de modelos — quantização e destilação]]
  - Converter a seção "Anti-patterns" (6 itens bullet) para callouts `[!warning]` individuais
- **Resultado:** —

#### 20 - Compressão de modelos — quantização e destilação   [mecânico]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 227 linhas · fase: ausente (Blocos) · status: growing / progress: done
- **Núcleo/gaps:** E5, P1
- **Score:** 10/12
- **Plano de execução:**
  - Adicionar parágrafo "O que vem a seguir" apontando para [[21 - Fine-tuning na prática — LoRA, QLoRA, DPO]] (QLoRA fine-tuna sobre base já quantizado em INT4)
- **Resultado:** —

#### 21 - Fine-tuning na prática — LoRA, QLoRA, DPO   [mecânico]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 243 linhas · fase: ausente (Blocos) · status: growing / progress: done
- **Núcleo/gaps:** E5, E8, P1
- **Score:** 9/12
- **Plano de execução:**
  - Adicionar seção "O que vem a seguir" de fechamento do galho (última nota), com ponte para [[Anatomia de Agents]], [[RAG e Vector Databases]] ou [[Context Engineering]]
  - Converter a seção "Armadilhas" (7 itens bullet) para callouts `[!warning]` individuais
- **Resultado:** —
