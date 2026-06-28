---
title: "RAG vs long context vs fine-tuning"
created: 2026-04-11
updated: 2026-05-02
type: concept
progress: backlog
status: seedling
publish: true
fase: Iniciado
tags:
  - rag
  - ia
  - decision-tree
aliases:
  - RAG vs long context
  - RAG vs fine-tuning
  - Decision tree LLM customization
---

# RAG vs long context vs fine-tuning

> [!abstract] TL;DR
> Três caminhos para fazer [[Dicionário de IA#LLM (Large Language Model)|LLM]] "saber seus dados": **[[Dicionário de IA#RAG (Retrieval-Augmented Generation)|RAG]]** (busca em runtime), **long context** (joga tudo no prompt), **[[Dicionário de IA#fine-tuning|fine-tuning]]** (treina modelo). Não competem — resolvem problemas diferentes. Long context vence em corpus pequeno e estável. RAG vence em corpus grande, dinâmico, com requisito de citação. Fine-tuning vence em mudar **comportamento**, não conhecimento. **Híbridos são comuns:** fine-tuning de tom + RAG de fatos é padrão maduro em 2026.

> [!question]- Quando long context supera RAG?
> Long context vence quando o corpus é pequeno, estável e cabe na janela com custo aceitável — especialmente com prompt caching, que elimina o custo de retransmitir o mesmo contexto a cada query. O ponto de virada acontece quando o corpus cresce além de ~200K tokens úteis (context rot deteriora a atenção do modelo) ou quando atualização frequente invalida o cache e reverte a vantagem de custo. A regra prática: se você consegue cachear o contexto inteiro e o corpus não muda mais que uma vez por semana, long context ganha em simplicidade e latência; caso contrário, RAG escala melhor.

## A confusão comum

> *"Devo usar RAG ou fine-tuning?"*

Pergunta errada. Os dois resolvem problemas diferentes:

- **RAG** adiciona **conhecimento factual** ao LLM
- **Fine-tuning** muda **comportamento** do LLM

Não é "ou", é "qual problema você tem".

## Comparativo

| Aspecto | RAG | Long context | Fine-tuning |
|---|---|---|---|
| **O que muda** | Adiciona conhecimento | Adiciona conhecimento | Muda comportamento + estilo |
| **Custo upfront** | Baixo (indexar) | Zero | Alto (treino) |
| **Custo por query** | Médio ([[Dicionário de IA#retrieval\|retrieval]] + tokens) | Alto (muitos tokens) | Baixo |
| **Frescor** | Atualizar = re-indexar | Mudar prompt | Re-treinar |
| **Citação** | Direta | Frágil | Não suporta |
| **Multi-tenant** | Filtrar por user_id | Difícil | Modelo por tenant é caro |
| **Quando vence** | Corpus grande, dinâmico | Corpus pequeno e estável | Estilo, tom, formato |

## Decision tree

```mermaid
graph TD
    A["Preciso que LLM<br/>'saiba' algo novo"] --> B{"Mudar conhecimento<br/>ou comportamento?"}
    B -->|conhecimento| C{"Corpus<br/>cabe na janela?"}
    B -->|comportamento<br/>(tom, formato, vocabulário)| D["Fine-tuning<br/>(LoRA, DPO)"]
    C -->|"sim, estável"| E["Long context<br/>(joga no prompt)"]
    C -->|"não, ou volátil"| F{"Citação<br/>requerida?"}
    F -->|sim| G["RAG"]
    F -->|não| H{"Latência<br/>crítica?"}
    H -->|sim, <500ms| I["RAG com cache<br/>ou long context cacheado"]
    H -->|não| G
```

## Long context — quando vence

✅ Corpus pequeno e **estável** (manual, FAQ pequeno)
✅ Latência <500ms importa (sem round-trip de retrieval)
✅ Multi-hop reasoning (LLM pode "ver tudo" e juntar)
✅ Modelo top de gama com prompt caching ([[Economia de Tokens|05 - Prompt caching na prática]])

> [!example] Caso real
> SaaS de devops com 50K tokens de docs internas. Joga tudo no prompt + cache. Latência 600ms. Custo $0.03/query (cached). Sem RAG infra para manter.
>
> Conta cresce → muda para RAG.

❌ **Cuidado com context rot:** [[Dicionário de IA#Context window|janela]] de 1M tokens não significa qualidade em 1M tokens (ver [[Context Engineering|03 - Context rot e atenção diluída]]).

## RAG — quando vence

✅ Corpus grande (>200K tokens) ou crescendo
✅ Atualização frequente (docs mudam toda semana)
✅ **Citação obrigatória** (compliance, auditabilidade)
✅ Multi-tenant (cada user tem dados)
✅ Volume alto (RAG é mais barato por query que long context)

> [!example] Caso real
> Suporte interno de empresa com 10K artigos. Indexa em pgvector. 1000 queries/dia. Custo $30/mês. Atualizações = re-indexar artigo modificado.

## Fine-tuning — quando vence

✅ **Tom e estilo** específicos (formal jurídico, conciso técnico, brand voice)
✅ Vocabulário de domínio que LLM base não tem
✅ Formato de output rígido (sempre estrutura X)
✅ Latência crítica + custo (modelo menor + fine-tune > modelo grande + prompt)
✅ Compliance que exige modelo controlado (não cloud)

> [!example] Caso real
> Empresa legal com 100K pareceres formatados de jeito específico. Fine-tune de Llama 70B com LoRA. Modelo gera no estilo certo sem precisar few-shot gigante.

❌ **Não use fine-tuning para "ensinar fatos novos":**

- Custa caro
- Atualização = re-treinar
- Não funciona bem (knowledge fica difuso)
- Use RAG

## Híbridos — o padrão maduro

```
Fine-tune (tom + formato) + RAG (fatos)
```

Exemplo: assistente legal que usa **modelo fine-tuned em estilo formal jurídico** + **RAG sobre jurisprudência atualizada**. Cada componente faz o que faz bem.

```
Long context + Fine-tune
```

Modelo fine-tuned com long context window estendida pré-treinado em domain corpus. Custo: alto. Use case: domínios fechados (medicine, legal).

## Custo comparativo (1000 queries/dia, corpus 50MB)

| Approach | Setup | Custo/mês |
|---|---|---|
| **Long context (com cache)** | $0 | ~$50-200 |
| **RAG (pgvector + Cohere Rerank + Sonnet)** | ~$200 | ~$80-300 |
| **Fine-tune (LoRA Llama-70B + RAG)** | $500-2000 | ~$200-500 |

Long context é **mais barato** em volume baixo. RAG escala melhor. Fine-tune tem ganhos qualitativos não-financeiros.

## Tabela de decisão prática

| Cenário | Recomendado |
|---|---|
| Chatbot de FAQ com 100 perguntas | Long context |
| Suporte com 10K artigos | RAG |
| Assistente médico com guidelines + citações | RAG |
| Bot de marketing com brand voice | Fine-tune |
| Code review em estilo de empresa | Fine-tune + RAG (codebase) |
| Tradutor especializado em jargão técnico | Fine-tune |
| Customer support multilíngue | RAG (multilingual embeddings) |
| Análise de docs financeiros novos | RAG (frescor) |

## Quando NÃO faz fine-tuning

- Tem <1000 exemplos de treino → RAG ou prompt engineering
- Goal é "saber fatos" → RAG
- Modelo base se sai >85% bem em prompts → não vale o custo
- Time não tem expertise em treino → terceiriza ou pula

## Quando NÃO faz RAG

- Pergunta requer info não-textual (visualização, cálculo numérico)
- Corpus tem <50 entradas e cabe no prompt → long context
- Latência crítica e queries são repetitivas → cache + long context

## Quando NÃO faz long context

- Corpus muda mais que 1x/semana (cache invalida)
- >200K tokens (context rot real)
- Citação obrigatória (long context cita pouco bem)

## Métricas para comparar

Compare experimentalmente em **golden set**:

| Métrica | Long context | RAG | Fine-tune |
|---|---|---|---|
| Accuracy (golden Q&A) | medir | medir | medir |
| Latência p95 | medir | medir | medir |
| Cost/query | medir | medir | medir |
| Faithfulness | medir | medir | medir |
| Citation accuracy | n/a | medir | n/a |

## Anti-patterns

- **"Vou fine-tunar pra LLM saber meus dados"** — uso errado
- **"RAG vai dar latência" sem medir** — superstição
- **Long context sem caching** — desperdício
- **Hibrido prematuro** (fine-tune + RAG) sem provar que cada componente vale
- **Comparar approaches sem golden set** — opinião, não dado

## Armadilhas comuns

> [!warning] Fine-tuning para ensinar fatos
> É o erro mais comum: o time quer que o modelo "saiba" os documentos internos e parte direto para fine-tuning porque parece mais definitivo. Na prática, fine-tuning codifica padrões de comportamento, não fatos declarativos. O conhecimento fica difuso nos pesos, não endereçável, e qualquer atualização exige re-treino completo. Use RAG para fatos; use fine-tuning para tom, formato e vocabulário de domínio.

> [!warning] Comparar abordagens sem golden set
> "O long context pareceu melhor" e "RAG deu resposta mais rápida" são observações anedóticas. Sem golden set com perguntas representativas e métricas definidas (accuracy, latência, custo por query), você está otimizando intuição. Qualquer decisão entre RAG, long context e fine-tuning deve ter número por trás — mesmo que um golden set rápido de 20-30 perguntas representativas.

> [!warning] Híbrido prematuro sem provar os componentes
> Fine-tune + RAG é o padrão maduro, mas adotar os dois de início sem evidência de que cada componente vale é engenharia por ansiedade. Comece com long context ou RAG puro; adicione fine-tuning só quando tiver dado concreto de que o comportamento base está prejudicando o output e que prompts sozinhos não resolvem.

## O que vem a seguir

Com o mapa de decisão entre RAG, long context e fine-tuning, você sabe quando RAG é a escolha certa. Mas RAG não é um monolito — quando o pipeline básico não alcança a qualidade necessária, existem padrões avançados que ampliam o que é possível: retrieval multi-hop, Graph RAG para domínios com entidades relacionadas, e Agentic RAG para queries de complexidade variável.

- [[11 - Padrões avançados — Graph RAG, Agentic RAG, multi-hop]] — quando vanilla RAG não resolve e como escalar para os 20% de casos mais difíceis

## Como explicar em inglês

Choosing between RAG, long context, and fine-tuning is a common interview question that trips up candidates who treat them as competing alternatives. The key insight is that they solve fundamentally different problems: RAG and long context both add knowledge at inference time, while fine-tuning modifies the model's behavior and style at training time. The practical consequence is that "should I RAG or fine-tune?" is almost always the wrong question — the right question is "what's missing: knowledge or behavior?"

Long context wins when the corpus is small, stable, and can be loaded into the prompt with caching enabled. RAG wins when the corpus is large, frequently updated, or requires traceable citations. Fine-tuning wins when you need consistent tone, domain-specific vocabulary, or rigid output formats that prompting alone can't produce reliably. The mature pattern in 2026 is the hybrid: a fine-tuned model for behavior, RAG for facts.

**In a technical interview**, you might say:

> "I evaluate all three against a golden set before committing. Long context is my first attempt for small corpora — if I can fit the knowledge with caching, I avoid the infra overhead of RAG. When the corpus exceeds roughly 200K useful tokens or updates frequently, RAG scales better. Fine-tuning is off the table unless I need consistent tone or output format that prompts alone can't reliably produce — it's expensive to update and doesn't handle factual recall as well as retrieval does. The hybrid of fine-tuned style plus RAG facts is the pattern I've seen work best in production for legal and medical domains."

| PT | EN |
|----|-----|
| Contexto longo | Long context |
| Ajuste fino | Fine-tuning |
| Atualização do corpus | Corpus update |
| Cache de prompt | Prompt caching |
| Degradação de atenção | Context rot |
| Tom e estilo | Tone and style |
| Vocabulário de domínio | Domain vocabulary |
| Custo por query | Cost per query |
| Combinação híbrida | Hybrid approach |
| Raciocínio multi-hop | Multi-hop reasoning |

## Veja também

- [[01 - O que é RAG e quando usar]]
- [[09 - Evaluation de RAG]]
- [[Anatomia dos LLMs|14 - Fine-tuning vs prompting vs RAG]]
- [[Anatomia dos LLMs|16 - Como LLMs são treinados — pretraining, SFT, RLHF]]
- [[Economia de Tokens|05 - Prompt caching na prática]]
- [[Context Engineering|03 - Context rot e atenção diluída]]

## Referências

- **OpenAI** — *RAG vs Fine-tuning guide* (2024)
- **Anthropic** — *Long context best practices* (2026)
- **Chip Huyen** — *AI Engineering* (2025), capítulos sobre customization
- **Eugene Yan** — *Patterns for Building LLM-based Systems* (2024)


































































