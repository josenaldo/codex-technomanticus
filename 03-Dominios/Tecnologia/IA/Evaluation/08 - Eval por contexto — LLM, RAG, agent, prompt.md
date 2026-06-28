---
title: "08 - Eval por contexto — LLM, RAG, agent, prompt"
created: 2026-05-28
updated: 2026-06-19
type: concept
status: growing
progress: in_progress
fase: Iniciado
tags:
  - evaluation
  - ia
  - rag
  - agents
  - prompt
publish: true
aliases:
  - Eval por contexto
  - Eval de RAG
  - Eval de agents
  - Eval de prompt
  - Eval de LLM base
---

# 08 - Eval por contexto — LLM, RAG, agent, prompt

> [!abstract] TL;DR
> Eval **não é uma coisa só**. O que você mede muda dramaticamente com o que está avaliando. **Prompt isolado**: golden set + rubrica simples. **RAG pipeline**: retrieval (precision@k, MRR, context recall) **separado** de generation (faithfulness, answer relevance). **Agent**: trajectory eval, tool call success, multi-step reasoning, task completion rate. **LLM base** (provider, modelo): benchmarks padronizados (MMLU, HumanEval, GSM8K, ARC). Cada contexto tem métrica-chave e frameworks indicados diferentes. Esta nota é o **mapa** que liga essa trilha às três notas contextuais existentes: [[03-Dominios/Tecnologia/IA/Anatomia de Agents/09 - Evaluation de agents]], [[03-Dominios/Tecnologia/IA/Anatomia dos LLMs/19 - Evaluation de LLMs em produção]], [[03-Dominios/Tecnologia/IA/RAG e Vector Databases/09 - Evaluation de RAG]].

> [!question]- O que eu preciso saber antes de ler isso?
> Você passou pelas notas 01-07 da trilha Evaluation: EDD, golden sets, rubrics, LLM-as-judge, regression testing, frameworks, CI/CD. Esta nota é a síntese — como esses conceitos se adaptam quando você não está avaliando um prompt isolado, mas um sistema RAG, um agent multi-step, ou um modelo base. Se você só vai usar eval pra prompt isolado, as notas anteriores já cobrem tudo. Esta nota importa quando você precisa entender por que as mesmas métricas não funcionam em sistemas mais complexos.

## Por que eval muda com contexto

A intuição básica: você não avalia um martelo do mesmo jeito que um helicóptero.

```
Prompt isolado: 1 chamada, 1 output
   → eval = output bom?

RAG pipeline: retrieval → rerank → generation
   → 3 estágios podem falhar
   → eval precisa isolar cada um

Agent: planning → tool calls → recovery → loop
   → trajetória importa, não só output final
   → eval precisa medir processo

LLM base (modelo do provider): genérico
   → eval em distribuição ampla de tarefas
   → benchmarks padronizados
```

Cada tipo de sistema falha de jeitos diferentes. Métrica boa pra um pode ser cega pro outro.

## Tabela canônica

| Tipo | Pergunta principal | Métricas-chave | Frameworks indicados | Nota Codex |
|---|---|---|---|---|
| **Prompt isolado** | Output atende à rubrica? | Accuracy, completeness, format, tone | Promptfoo, Braintrust, OpenAI Evals | (esta trilha, notas 02-04) |
| **RAG pipeline** | Retrieval trouxe info certa? Geração fiel? | Context precision/recall, faithfulness, answer relevance, citation accuracy | Ragas, TruLens, DeepEval, Phoenix | [[03-Dominios/Tecnologia/IA/RAG e Vector Databases/09 - Evaluation de RAG]] |
| **Agent** | Tarefa completou? Trajetória eficiente? | Task completion rate, steps per task, tool call success, human intervention rate | Langfuse, LangSmith, Braintrust | [[03-Dominios/Tecnologia/IA/Anatomia de Agents/09 - Evaluation de agents]] |
| **LLM base** | Modelo é capaz na distribuição? | Benchmarks (MMLU, HumanEval, GSM8K, ARC, HellaSwag) | lm-evaluation-harness, BIG-bench | [[03-Dominios/Tecnologia/IA/Anatomia dos LLMs/19 - Evaluation de LLMs em produção]] (parcial) |
| **Multimodal** | Output coerente cross-modal? | CLIP-score, multi-modal faithfulness | Phoenix, custom | (futuro) |

## 1. Eval de prompt isolado

Cenário: um prompt único transforma input em output. Sem retrieval, sem tools, sem multi-step.

**Tipos de tarefa típicos**:
- Classificação (categorize ticket)
- Extração estruturada (extrai dados de email)
- Resumo (summarize artigo)
- Tradução (PT-EN)
- Reescrita (formaliza tom)

**Eval pipeline**:

```python
for item in golden_set:
    output = llm(prompt.format(input=item.input))
    score = rubric.apply(output, expected=item.expected)
    record(item.id, score)

aggregate = mean(scores), per_dimension(scores)
```

**Métricas**:
- Accuracy (classificação): % correto
- Schema validity (extração): % parseável + completo
- Embedding similarity (resumo): cosine > threshold
- LLM-as-judge (subjetivo)

**Frameworks**: Promptfoo brilha aqui — YAML declarativo, comparação cross-provider, eval-as-code.

Para o aprofundamento, esta trilha inteira (notas 01-07) cobre prompt isolado como caso base.

## 2. Eval de RAG pipeline

Cenário: pergunta → retrieve chunks → rerank → generate com chunks no contexto.

**A regra fundamental** (vinda de [[03-Dominios/Tecnologia/IA/RAG e Vector Databases/09 - Evaluation de RAG]]): **medir retrieval separado de generation**.

Por quê: resposta ruim em RAG tem 5 causas possíveis:

1. Chunk relevante não existe no corpus (parse/chunk ruim)
2. Chunk existe mas retrieval não pegou
3. Rerank baixou o chunk certo
4. Chunks corretos mas prompt não usou
5. Modelo complementou com conhecimento próprio (faithfulness ruim)

Métricas agregadas escondem qual delas é o gargalo.

**Métricas canônicas (Ragas)**:

| Métrica | Mede | Estágio |
|---|---|---|
| **Context precision** | Chunks recuperados são relevantes? | Retrieval |
| **Context recall** | Chunks relevantes foram recuperados? | Retrieval |
| **Faithfulness** | Resposta usou só os chunks? | Generation |
| **Answer relevance** | Resposta atende à pergunta? | Generation |
| **Citation accuracy** | Citações [N] apontam pro chunk real? | Generation |

**Frameworks**:
- **Ragas** — mais popular, métricas canônicas, LLM-as-judge interno
- **TruLens** — tracing + eval integrados
- **DeepEval** — pytest-style, fácil em CI
- **Phoenix** — visual debugging
- **Langfuse** — observability em prod

**Aprofundamento**: [[03-Dominios/Tecnologia/IA/RAG e Vector Databases/09 - Evaluation de RAG]] tem o tratamento completo — métricas, Ragas code, golden set com `expected_chunks`, anti-patterns, pipeline CI.

## 3. Eval de agent

Cenário: input → o agent planeja → faz tool calls → recupera de falhas → produz output final em N steps.

**Por que agent é diferente**:

```
LLM puro:  Input → output → match com expected

Agent:     Input → 12 steps com decisões → output
           → mesmo input pode levar a 2 outputs igualmente válidos
           → caminho importa, não só destino
```

**Métricas-chave** (vindas de [[03-Dominios/Tecnologia/IA/Anatomia de Agents/09 - Evaluation de agents]]):

| Métrica | Mede | Alvo |
|---|---|---|
| **Task completion rate** | % tarefas terminadas corretamente | >75% prod, >90% tasks bem-definidas |
| **Steps per task** | Eficiência da trajetória | Decrescente ao longo do tempo |
| **Tool call success rate** | % chamadas de tool corretas | >85% |
| **Cost per task** | $ por tarefa | <budget definido |
| **Human intervention rate** | % vezes humano precisou intervir | <20%, decrescente |
| **Error type catalog** | Distribuição de falhas | Stable ou shrinking |

**Métodos específicos pra agent**:
- **Trajectory eval** — não só o output, mas a sequência de tool calls + reasoning
- **Trace review humana** — 1-2h/semana lendo traces reais ([[03-Dominios/Tecnologia/IA/Anatomia de Agents/09 - Evaluation de agents]] enfatiza isso como "eval mais valioso")
- **Regression em error types** — bug novo vira teste permanente

**Frameworks**:
- **Langfuse** — traces de agent em prod
- **LangSmith** — integração nativa LangChain, eval de chain
- **Braintrust** — eval com versioning, comparação visual de trajetórias

**Aprofundamento**: [[03-Dominios/Tecnologia/IA/Anatomia de Agents/09 - Evaluation de agents]] cobre completion rate, error type catalog, trace review, regression patterns específicos pra agentic systems.

### 3.1 Fixe o harness, não só o modelo

Aqui mora uma armadilha de eval de agent que a tabela acima não captura. Quando você roda um agente, o número que sai não vem só do modelo — vem do modelo **mais** o [[03-Dominios/Tecnologia/IA/Anatomia de Agents/11 - Harness engineering — a terceira camada|harness engineering]] que o envolve: o loop de controle, o scaffolding de tools, o retry, o orquestrador. Troque o harness e o mesmo modelo entrega um número diferente.

Pergunta natural do leitor: então quando um leaderboard diz "modelo X subiu 8 pontos em SWE-bench", quanto disso é o modelo? A resposta honesta é: pode ser que parte considerável seja do harness. Um preprint de 2026, *Harness Engineering for Language Agents*, decompõe a camada em CAR (Control / Agency / Runtime) e argumenta que *"many reported agent gains may be partly harness-sensitive rather than purely model-driven"* — muito do ganho reportado pode ser efeito do harness, não do modelo.

A consequência pra eval é direta. Um leaderboard que troca modelo **e** harness ao mesmo tempo está medindo uma variável confundida — você não sabe a qual das duas mudanças atribuir a diferença. A regra prática é a mesma de qualquer experimento controlado: **fixe o harness antes de atribuir uma diferença ao modelo**. Compare modelos sob o mesmo scaffolding, ou compare scaffoldings sob o mesmo modelo, nunca os dois de uma vez.

> [!example] O confounding na prática
> Setup A: modelo M1 + harness com retry agressivo e 12 tools → 82% completion.
> Setup B: modelo M2 + harness enxuto, 4 tools, sem retry → 74% completion.
> Conclusão ingênua: "M1 > M2". Conclusão correta: **você não sabe** — pode ser que M2 com o harness do A vencesse. Duas variáveis mudaram; o resultado é ilegível.

Os autores propõem o **HarnessCard**: um artefato leve de reporte, análogo aos *model cards* e *datasheets*, descrevendo a camada de harness usada. A posição deles: *"progress in language agents should report not only the model, but also the harness layer that turns capability into governed action"* — reportar não só o modelo, mas a camada que transforma capacidade em ação governada. Pra quem faz eval, isso vira um item de checklist: ao publicar (ou ler) um resultado de agente, exija a descrição do harness junto.

> [!caution] Preprint, não consenso
> *Harness Engineering for Language Agents* é um **preprint não revisado por pares** (preprints.org, abr/2026). Trate CAR e o HarnessCard como **proposta argumentada / tomada de posição**, não como prática consolidada da comunidade. A intuição de "harness confunde a medição" é sólida e útil hoje; a nomenclatura específica e o formato do card ainda não passaram por revisão.

**Resumo em uma linha**: número de agente é modelo × harness — para que a comparação signifique algo, prenda uma das duas variáveis.

## 4. Eval de LLM base

Cenário: você está avaliando o **modelo em si**, não um produto sobre ele. Provider novo, fine-tuned model, comparação cross-modelo.

**Benchmarks padronizados (2026)**:

| Benchmark | Mede | Domínio |
|---|---|---|
| **MMLU** | Conhecimento multi-domínio (57 tópicos) | Genérico |
| **MMLU-Pro** | MMLU expandido, mais difícil | Genérico |
| **HumanEval** | Geração de código Python | Coding |
| **HumanEval+** | HumanEval com testes adicionais | Coding |
| **GSM8K** | Math grade school | Matemática |
| **MATH** | Math olimpíada | Matemática avançada |
| **ARC** (AI2 Reasoning Challenge) | Raciocínio científico | Ciência |
| **HellaSwag** | Senso comum / completion | Genérico |
| **TruthfulQA** | Veracidade vs hallucination | Robustez |
| **BIG-bench** | 200+ tarefas diversas | Genérico amplo |
| **SWE-bench** | Resolução de issues reais em repos open source | Coding agentic |

**Frameworks**:
- **lm-evaluation-harness** (EleutherAI) — padrão de fato pra benchmarks padronizados
- **BIG-bench** — coleção da Google
- **Helm** (Stanford) — Holistic Evaluation of Language Models

**Cuidado**: benchmarks medem **capabilities** do modelo, não **performance na sua tarefa específica**. Modelo que vence MMLU pode ser pior pra classificação de ticket que um modelo menor com prompt bem feito.

**Aprofundamento**: [[03-Dominios/Tecnologia/IA/Anatomia dos LLMs/19 - Evaluation de LLMs em produção]] cobre eval **em produção** (golden set + judge + traces + A/B), que é o mais relevante na maioria dos casos. Benchmarks acadêmicos são úteis quando o trabalho é **escolher** entre modelos base.

## 5. Multimodal e casos especiais (mencionado)

Eval de output multimodal (imagem, áudio, vídeo) é uma fronteira em 2026:

- **CLIP-score** — similaridade texto-imagem
- **Multi-modal faithfulness** — texto descreve a imagem corretamente?
- **Speech eval** — WER (Word Error Rate), MOS (Mean Opinion Score)

Frameworks como Phoenix têm suporte mais maduro pra multi-modal. Ragas adicionou eval multimodal em 2026. É domínio em rápida evolução.

## Decision tree resumido

```
O que você está avaliando?

├── Um prompt isolado (chamada única)?
│   → Notas 02-04 desta trilha + Promptfoo
│
├── Pipeline RAG (retrieval + generation)?
│   → [[RAG e Vector Databases/09 - Evaluation de RAG]] + Ragas
│
├── Agent (multi-step + tools)?
│   → [[Anatomia de Agents/09 - Evaluation de agents]] + Langfuse/Braintrust
│
├── Modelo base novo (escolha de provider)?
│   → lm-evaluation-harness + benchmarks padronizados
│
└── Sistema em produção, geral?
    → [[Anatomia dos LLMs/17 - Evaluation de LLMs em produção]] (4 pilares)
```

## Combinando contextos — o caso real

Produto real raramente é só um desses. Exemplo: assistente de suporte com:

- **RAG** sobre base de conhecimento
- **Tools** pra criar ticket, consultar status
- **Multi-step** quando precisa de info adicional do usuário

Eval combinado:

```yaml
eval_pipeline:
  retrieval:
    metrics: [context_precision, context_recall]
    framework: ragas
    threshold: { precision: 0.7, recall: 0.8 }

  generation:
    metrics: [faithfulness, answer_relevance]
    framework: ragas
    threshold: { faithfulness: 0.9 }

  agent_trajectory:
    metrics: [tool_call_success, steps_per_task, completion_rate]
    framework: langfuse
    threshold: { completion: 0.85, steps: max=8 }

  end_to_end:
    metrics: [user_satisfaction_judge, format_validity]
    framework: braintrust
    threshold: { satisfaction: 4.0 }
```

Cada estágio com seu eval. Failure em qualquer um sinaliza onde está o problema. Eval só end-to-end esconde diagnosis.

## Anti-patterns

- **Métrica única pra sistema multi-componente** — RAG com só "answer relevance" esconde retrieval ruim
- **Benchmark acadêmico como eval de produto** — MMLU não mede sua tarefa
- **Eval de agent sem trace review** — métrica agregada perde bugs sutis em trajetória
- **Mesmo dataset pra tudo** — eval de prompt, RAG e agent precisam datasets diferentes
- **Sem isolar componentes** — performance ruim na ponta sem saber qual estágio falhou

## Armadilhas comuns

> [!warning] Usar métrica de prompt isolado em sistema multi-componente
> A armadilha mais frequente ao expandir de prompt isolado para RAG ou agent é tentar aplicar as mesmas métricas end-to-end. "Answer relevance" num sistema RAG pode estar alta mesmo quando o retrieval está trazendo chunks errados — se o modelo é bom o suficiente, ele responde razoavelmente mesmo com contexto ruim. Você vai otimizar o prompt de generation enquanto o verdadeiro problema está no embedding model ou no reranker. Para cada estágio que pode falhar independentemente, você precisa de métrica isolada daquele estágio. Métricas end-to-end são indicadores de saúde geral, não de diagnóstico.

> [!warning] Benchmark acadêmico como substituto para eval de produto
> MMLU, HumanEval e GSM8K medem capacidade geral do modelo base — não medem se o modelo vai ser bom na sua tarefa específica. Um modelo que domina MMLU (conhecimento multidisciplinar) pode ser pior em classificação de tickets técnicos do que um modelo menor com prompt bem calibrado. Times que usam benchmarks para escolher modelos de produção sem testar no próprio domínio frequentemente descobrem que o "modelo mais capaz" não entrega o melhor resultado no produto. Benchmarks são úteis para triagem inicial; a decisão final exige golden set + rubrica do seu domínio específico.

> [!warning] Eval de agent sem revisar traces manualmente
> Métricas de agent (task completion rate, steps per task, tool call success) são números agregados que escondem padrões de falha sutis. Um agent com 80% de completion rate pode estar falhando sempre nos mesmos tipos de input, ou fazendo o caminho certo pelos motivos errados, ou usando tools em ordem desnecessariamente longa. Nenhuma métrica automática captura esses padrões melhor do que um humano lendo 20-30 traces por semana. A trace review manual é trabalhosa mas é o eval mais valioso em sistemas agentic — ela produz os casos de teste de regression mais úteis e a intuição necessária para melhorar o harness.

## Como explicar em inglês

Em entrevistas sobre avaliação de sistemas LLM, a capacidade de adaptar o framework de eval ao tipo de sistema demonstra maturidade de engenharia:

> "Eval isn't one-size-fits-all. For a standalone prompt, a golden set with a rubric is enough. For a RAG pipeline, you need to measure retrieval separately from generation — context precision and recall at the retrieval stage, faithfulness and answer relevance at the generation stage. For agents, output alone isn't enough; you need trajectory eval — tool call success rate, steps per task, human intervention rate. For choosing between model providers, academic benchmarks like MMLU and HumanEval are useful for capability triaging, but the final decision always needs your own domain-specific golden set."

| Português | Inglês |
|-----------|--------|
| eval por contexto | context-specific evaluation |
| prompt isolado | standalone prompt / single-turn prompt |
| pipeline RAG | RAG pipeline |
| precisão de contexto | context precision |
| revocação de contexto | context recall |
| fidelidade da resposta | answer faithfulness |
| eval de trajetória | trajectory eval |
| benchmark acadêmico | academic benchmark |
| análise de trace | trace review |
| taxa de completude de tarefa | task completion rate |

## O que vem a seguir

Esta nota fecha o galho de Evaluation. O próximo domínio no caminho de AI Engineering é Observability — como monitorar em produção o que os evals mediram em pré-deploy: traces, métricas de uso, drift de output, e debugging de falhas que só aparecem com tráfego real.

Ver galho Observability em [[03-Dominios/Tecnologia/IA/Observability/]].

## Veja também

- [[03-Dominios/Tecnologia/IA/Anatomia dos LLMs/19 - Evaluation de LLMs em produção]] — o tratamento aprofundado de eval em prod (os 4 pilares)
- [[03-Dominios/Tecnologia/IA/Anatomia de Agents/09 - Evaluation de agents]] — eval específico pra agents
- [[03-Dominios/Tecnologia/IA/RAG e Vector Databases/09 - Evaluation de RAG]] — métricas canônicas Ragas
- [[02 - Golden datasets — como construir]] — golden set por tipo
- [[06 - Frameworks 2026 — Promptfoo, Braintrust, Langfuse, Patronus, Phoenix]] — qual framework por contexto
- [[03-Dominios/Tecnologia/IA/AI Engineering Stack/09 - Evaluation Layer]] — a camada onde tudo isso acontece

## Fontes

- **Es et al.** — *RAGAS: Automated Evaluation of Retrieval Augmented Generation* ([arxiv:2309.15217](https://arxiv.org/abs/2309.15217), 2023)
- **EleutherAI** — [*lm-evaluation-harness* (github)](https://github.com/EleutherAI/lm-evaluation-harness)
- **OpenAI** — *HumanEval* paper + dataset (2021)
- **Hendrycks et al.** — *MMLU* ([arxiv:2009.03300](https://arxiv.org/abs/2009.03300), 2020)
- **Cobbe et al.** — *GSM8K* ([arxiv:2110.14168](https://arxiv.org/abs/2110.14168), 2021)
- **Princeton + Stanford** — *SWE-bench* ([arxiv:2310.06770](https://arxiv.org/abs/2310.06770), 2023)
- **Chip Huyen** — *AI Engineering* (2025), cap. eval por contexto
- **Anthropic** — *Eval cookbook — agent and RAG patterns* (2026)
- **Harness Engineering for Language Agents** — [preprints.org 10.20944/preprints202603.1756](https://doi.org/10.20944/preprints202603.1756) (2026). Decompõe a camada de harness em CAR (Control/Agency/Runtime), argumenta que ganhos de agente são "harness-sensitive" e propõe o HarnessCard como artefato de reporte. *Preprint, não peer-reviewed.*
