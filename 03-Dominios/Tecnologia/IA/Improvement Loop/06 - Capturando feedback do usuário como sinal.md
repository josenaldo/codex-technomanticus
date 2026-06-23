---
title: "06 - Capturando feedback do usuário como sinal"
created: 2026-05-28
updated: 2026-05-28
type: concept
status: seedling
progress: in_progress
tags:
  - improvement-loop
  - ia
  - feedback
  - sinal-humano
publish: true
aliases:
  - User feedback
  - Sinal humano
  - Thumbs up down
---

# 06 - Capturando feedback do usuário como sinal

> [!abstract] TL;DR
> Feedback do usuário é o sinal **mais rico e mais ruidoso** que entra no Improvement Loop. Dividir em **explícito** (thumbs up/down, star rating, free-text complaint) e **implícito** (re-prompt rate, abandonment, edit-after-paste, copy/share, time-to-action). Cada sinal tem **custo de coleta** diferente e **noise-to-signal** diferente; tratá-los uniformemente é erro comum. Pegadinhas: confirmation bias (usuário fica feliz com resposta confirmadora mas errada), popularity ≠ qualidade (resposta mais reaproveitada pode ser a mais genérica). Quando feedback contradiz eval automatizado: depende do que cada um mede. Eval mede **alinhamento com rubrica**; feedback mede **utilidade percebida**. Os dois importam, mas servem decisões diferentes. Tools 2026: Langfuse, Braintrust, Helicone têm feedback API nativa; rolar próprio é tabela `feedbacks` com FK no trace + endpoint.

## Por que feedback do usuário entra no loop

Eval offline mede **alinhamento com rubrica**: rubrica diz que resposta boa tem 3 bullets factuais, dataset tem ground truth, judge confirma. Eval responde "isso é correto?".

Feedback do usuário mede **utilidade percebida**: a resposta tecnicamente correta foi útil? Resolveu o problema? Conectou com o contexto do usuário? Feedback responde "isso ajudou?".

Sistema de IA em produção precisa dos dois. Sistema sem feedback otimiza pra benchmark e degrada UX; sistema sem eval otimiza pra "sensação boa" e vira chatbot bajulador (o sycophancy problem).

## Explícito vs implícito

### Sinal explícito

Usuário **declara** o feedback. Custo de coleta: alto pra usuário (precisa parar e clicar). Sinal: forte mas esparso (90%+ dos usuários ignoram).

| Sinal | Como coleta | Custo cognitivo | Noise |
|---|---|---|---|
| **Thumbs up/down** | Botão ao lado da resposta | Baixo (1 clique) | Médio (clica sem ler com cuidado) |
| **Star rating (1-5)** | Modal ou inline | Médio | Alto (escala não calibrada entre usuários) |
| **Free-text complaint** | Modal "o que deu errado?" | Alto | Baixo no conteúdo, mas baixo volume |
| **Bug report estruturado** | Form com categoria | Muito alto | Muito baixo (quem responde, sabe o que tá fazendo) |

Padrão pragmático: thumbs simples como **default**, free-text **opcional** depois de thumbs down ("conta mais?"). Thumbs binário evita debate de escala; free-text captura categoria de falha.

### Sinal implícito

Comportamento do usuário **revela** o feedback sem precisar declarar. Custo de coleta: zero pra usuário. Sinal: rico mas exige interpretação.

| Sinal | O que sugere | Confounders |
|---|---|---|
| **Re-prompt rate** | Usuário não ficou satisfeito; tentou de novo | Pode estar refinando, não reclamando |
| **Abandonment** | Usuário fechou sem agir | Pode ter conseguido o que queria e saiu |
| **Edit-after-paste** | Output foi usado mas precisou conserto | Pode ser edição estilística natural |
| **Copy/share** | Output foi útil o suficiente pra mover adiante | Pode ser arquivar pra revisar depois |
| **Time-to-action** | Demora pra agir = usuário processando ou desistindo | Sinal ambíguo sem contexto |
| **Continuação da sessão** | Mais turns = engajamento | Mais turns = também pode ser "ainda procurando" |
| **Retorno após N dias** | Sistema gerou valor o suficiente pra voltar | Sinal lento, alta latência |

Implícito é **mais volume, mais ruído**. Precisa de modelagem (taxa por cohort, comparação com baseline) pra virar sinal acionável.

## Weighting — cada sinal vale o quê

Erro comum: tratar todos os feedbacks como iguais. Realidade: cada sinal tem **custo-pra-coletar diferente** e **noise-pra-signal diferente**.

Heurísticas de weighting:

| Tipo de sinal | Peso típico | Por quê |
|---|---|---|
| Bug report estruturado | **Alto** | Baixo volume, baixo noise; quem reporta sabe o que viu |
| Free-text complaint | **Alto** | Esforço sinaliza intensidade real |
| Thumbs down | **Médio** | Volume razoável, noise médio |
| Thumbs up | **Baixo** | Confirmation bias forte; usuário clica em qualquer coisa que parece OK |
| Re-prompt | **Médio-alto** | Ação implícita forte; usuário não tá satisfeito |
| Abandonment | **Baixo-médio** | Ambíguo; precisa cruzar com outros sinais |
| Edit-after-paste | **Médio** | Indica refinamento, pode ser estilo |
| Copy/share | **Médio-baixo** | Indica utilidade, mas não confirma qualidade do conteúdo |

Cálculo prático: peso × frequência por categoria = ranking de problemas. Categoria que aparece em 5 bug reports detalhados ≈ categoria que aparece em 500 thumbs down.

## Confounders — onde feedback engana

Sinais humanos têm vieses sistemáticos. Os principais no contexto de IA:

### Confirmation bias

Usuário tende a thumbs up em resposta **que concorda com sua hipótese prévia**, mesmo que esteja errada. Exemplo: "Existe relação entre X e Y?" → resposta confirma, usuário curte; resposta nega, usuário não curte. Sistema treinado em thumbs up vira sycophant — concorda com tudo.

Mitigação: pesar thumbs up menos que thumbs down; combinar com eval factual; treinar judges pra detectar sycophancy.

### Popularity ≠ qualidade

Resposta mais copiada/compartilhada pode ser a mais **genérica** (encaixa em vários contextos) e menos a mais útil pra um caso específico. "Top resposta" pelo signal de copy pode ser exatamente a que o usuário quer com baixo esforço cognitivo, não a melhor.

Mitigação: medir por cohort/contexto, não global; cruzar com métricas de resolução do problema downstream.

### Selection bias na coleta

Quem dá feedback explícito tem perfil diferente do usuário médio. Outliers (super-fãs ou super-decepcionados) sobrerepresentados. Sinal não é amostra aleatória da base.

Mitigação: combinar explícito com implícito (que cobre todo mundo); modelar quem tá dando feedback (cohort analysis).

### Reciprocidade percebida

Usuário pode dar thumbs up por "educação" ou por gostar do produto **em geral**, não daquela resposta específica.

Mitigação: thumbs anônimo, sem identificação social; sinais implícitos como contrapeso.

### Anchoring na resposta anterior

Em sessão multi-turn, usuário avalia resposta N comparando com resposta N-1. Resposta N pode ser absolutamente boa mas parecer ruim porque N-1 foi excepcional.

Mitigação: análise por turn isolado quando possível; modelar contexto de sessão.

## Combinando com eval automatizado — quando cada um vence

Frequentemente os dois sinais concordam. Quando não concordam:

### Eval alta, feedback baixo

- Eval diz "resposta correta segundo rubrica"
- Usuários reclamam consistentemente
- **Provável causa**: rubrica não cobre algo importante (UX, tom, completude pra caso real, formato esperado)
- **Ação**: rubrica precisa ser estendida; feedback é o sinal que vence aqui

### Eval baixa, feedback alto

- Eval diz "resposta tem problemas"
- Usuários curtem
- **Provável causa**: sycophancy, bajulação, resposta verbosa que parece esforçada
- **Ação**: investigar tipo de erro que eval pegou; se for sycophancy, eval vence
- **Atenção**: feedback positivo em resposta tecnicamente errada é o sinal mais perigoso — perpetua erro

### Eval e feedback concordam

- Sinal forte; trate como confirmação
- Use a magnitude pra priorizar

### Discordância por subgrupo

- Eval e feedback médios são parecidos; mas feedback no segmento X é negativo
- **Provável causa**: distribuição não capturada no golden set (idioma, vertical, persona)
- **Ação**: dataset precisa adicionar amostras desse segmento

A regra honesta: **nenhum dos dois vence universalmente**. Eval mede "correto"; feedback mede "útil". Decisão de produto precisa pesar os dois. Decisão técnica (regressão de prompt) costuma pesar eval; decisão de UX (formato, tom) costuma pesar feedback.

## Tools 2026

### Built-in em frameworks de eval/observability

| Tool | Como funciona |
|---|---|
| **Langfuse** | Score API — `langfuse.score(trace_id, name="user_thumbs", value=1)`. Score vincula ao trace, dashboard mostra por prompt_version. |
| **Braintrust** | Feedback API similar; integra com eval comparison view. |
| **Helicone** | Feedback endpoint via proxy; UI mostra correlação com prompt/model. |
| **Arize Phoenix** | Feedback como annotation no span; útil pra training de judge. |

### Rolar próprio

Quando o stack é caseiro ou tem requisitos específicos:

```python
# tabela mínima
CREATE TABLE feedbacks (
    id UUID PRIMARY KEY,
    trace_id TEXT NOT NULL,        -- FK pro trace
    user_id TEXT,                  -- opcional, anonimizado quando preciso
    feedback_type TEXT NOT NULL,   -- "thumb", "star", "free_text", "bug"
    value JSONB NOT NULL,          -- {"thumb": "up"} | {"stars": 4} | {"text": "..."}
    metadata JSONB,                -- contexto adicional (cohort, segment)
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_feedbacks_trace ON feedbacks(trace_id);
CREATE INDEX idx_feedbacks_type_time ON feedbacks(feedback_type, created_at);
```

```python
# endpoint mínimo
@app.post("/feedback")
def submit_feedback(payload: FeedbackPayload):
    db.insert("feedbacks", {
        "trace_id": payload.trace_id,
        "user_id": hash_user(payload.user_id),  # privacy by default
        "feedback_type": payload.type,
        "value": payload.value,
        "metadata": payload.metadata,
    })
    # opcional: webhook pra Slack em casos críticos (e.g., free_text)
    if payload.type == "free_text" and payload.value.get("sentiment") == "negative":
        notify_team(payload)
```

Decisão pragmática: time pequeno usa o que vier com framework já adotado (Langfuse Score API, Braintrust Feedback); time grande com privacidade rígida ou stack misto costuma rolar próprio.

## Anti-padrões

- **Coletar tudo, analisar nada** — feedback acumula em tabela, ninguém olha
- **Tratar todo feedback como igual** — thumbs up de usuário aleatório == bug report detalhado de power user
- **Ignorar implícito** — só thumbs/stars; perde 90% do sinal
- **Treinar judge em feedback bruto** — sycophancy in, sycophancy out
- **Não anonimizar** — privacidade vira problema legal antes do feedback virar valor
- **Feedback sem trace_id** — não dá pra ligar feedback à versão do prompt/modelo que gerou
- **Sem postmortem regular** — feedback fica em dashboard, nunca vira backlog
- **Mostrar agregado sem cohort** — média esconde regressão em segmento específico
- **Reagir a feedback isolado em produção crítica** — UM bug report dispara mudança no prompt sem investigar

## Operacionalizando — do feedback à mudança

O feedback vira parte do loop quando segue um fluxo:

```
1. Coleta: API + framework de tracing vinculam feedback ao trace + prompt_version
2. Agregação: dashboard por categoria, cohort, segmento
3. Triagem: revisar amostras (humano), categorizar tipos de falha
4. Backlog: tipos de falha viram itens com prioridade (volume × peso)
5. Eval gap: tipos que eval não pega vão pra extensão do golden set
6. Hipótese de mudança: diff no prompt, novo few-shot, novo guardrail
7. A/B + canary: valida que a mudança resolve a categoria
8. Métrica de fechamento: feedback negativo daquela categoria cai depois do ship
```

Sem o passo 4 (backlog), feedback nunca vira ação. Sem o passo 8 (métrica de fechamento), o time não sabe se resolveu mesmo.

## Fontes

- **Langfuse** — [*User feedback (Score API)*](https://langfuse.com/docs/scores/getting-started).
- **Braintrust** — [*Human review and feedback*](https://www.braintrust.dev/docs/guides/human-review).
- **Helicone** — [*User feedback*](https://docs.helicone.ai/features/user-feedback).
- **Arize** — [*Phoenix annotations*](https://docs.arize.com/phoenix). Feedback como annotation.
- **Sharma et al.** — *Towards Understanding Sycophancy in Language Models* ([arxiv:2310.13548](https://arxiv.org/abs/2310.13548)). Risco de treinar em thumbs up bruto.
- **Anthropic** — [*Constitutional AI*](https://www.anthropic.com/research/constitutional-ai). Padrão pra reduzir dependência de feedback humano cru.
- **Eugene Yan** — [*Evals are all you need*](https://eugeneyan.com/writing/evals/). Discute peso relativo de eval vs feedback.

## Veja também

- [[01 - O ciclo eval → diff → ship]] — feedback é uma das fontes do passo 1 (observability)
- [[Evaluation/04 - LLM-as-judge — quando e como]] — judge enviesado por feedback vira problema
- [[Observability]] — feedback como sinal no observability stack
- [[Anatomia dos LLMs/17 - Evaluation de LLMs em produção]] — A/B em prod cruza com feedback
- [[Segurança e Guardrails]] — sycophancy é falha de guardrail comportamental
