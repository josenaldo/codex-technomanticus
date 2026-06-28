---
title: "06 - Capturando feedback do usuário como sinal"
created: 2026-05-28
updated: 2026-06-28
type: concept
status: seedling
fase: Iniciado
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

> [!question]- Como começar a coletar feedback sem interromper o fluxo do usuário nem adicionar fadiga de feedback?
> A receita minimal: uma única linha de thumbs up/down ao lado de cada resposta, sem modal obrigatório. Se o usuário clica no thumbs down, aparece (opcionalmente) um campo de texto "o que deu errado?". Esse fluxo tem o menor custo cognitivo possível e captura o sinal mais acionável. Não implemente star rating como primeiro passo — escala de 5 pontos não é calibrada entre usuários e gera dados ruidosos que exigem modelagem mais complexa. Não implemente obrigatoriedade — feedback forçado vira viés de aborrecimento. Em relação ao timing: mostrar o botão de feedback 3-5 segundos após a resposta aparecer (não imediatamente) aumenta CTR porque o usuário já leu a resposta. Depois de 30 dias coletando dados, avalie se faz sentido adicionar categorias (free-text ou dropdown) pra casos de thumbs down.

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

Uma variante para times com produto B2B: adicione passo 2.5 entre Agregação e Triagem — **priorização por impacto de cliente**. Se um cliente Enterprise está 80% do thumbs-down volume, isso tem prioridade de investigação diferente de 80 usuários free-tier. Feedback de cliente de contrato pesa mais do que o número bruto sugere — tanto pelo impacto comercial quanto pela qualidade do sinal (usuários Enterprise geralmente articulam melhor o que está errado).

## Armadilhas comuns

> [!warning] Coletar tudo e não analisar nada — feedback morre no banco
> A ilusão do "coletamos feedback" é acumular thumbs em tabela sem processo de triagem regular. Dados crescem, ninguém lê. Meses depois, o time descobre que havia padrão de reclamação sobre o idioma PT-EU que nunca chegou ao backlog. O feedback precisa de **dono** e **cadência**: uma person designada revisa amostra de feedbacks negativos semanalmente, categoriza, e atualiza o backlog. Sem cadência, feedback é métrica de vaidade (taxa de thumbs up no dashboard) que não vira ação. A triagem não precisa ser longa — 30 minutos semanais revisando amostras estratificadas por tipo já é suficiente pra identificar padrões novos.

> [!warning] Treinar judge em feedback de usuário sem filtrar sycophancy — o modelo aprende a bajular
> Feedback explícito de usuário tem confirmation bias estrutural: respostas que concordam com a hipótese do usuário recebem mais thumbs up, independente de correção factual. Se você usa esse feedback pra treinar (ou calibrar) um LLM-as-judge, o judge aprende a dar score alto pra respostas que confirmam, não pra respostas corretas. O sinal de treinamento entra, a sycophancy sai. A correção começa antes da coleta: identifique no seu dataset feedbacks onde o usuário deu thumbs up em resposta que você sabe ser factualmente errada — esses casos mostram a magnitude do bias. Depois, filtre ou pese por tipo de feedback: pese thumbs down mais do que thumbs up; priorize bug reports sobre star ratings; use sinais implícitos (re-prompt rate) como sanity check do explícito.

> [!warning] Feedback sem trace_id — não saber qual versão de prompt gerou aquela resposta
> Thumbs down chegou. Ótimo. Mas: de qual resposta? Com qual versão do prompt? Com qual modelo? Em qual contexto? Sem o `trace_id` vinculado ao feedback, você não consegue responder nenhuma dessas perguntas — o feedback é sinal de que há um problema, mas não onde. O sistema de coleta deve linkar cada feedback ao `trace_id` no momento da coleta, não depois. É responsabilidade do frontend passar o trace_id como parâmetro quando renderiza o botão de feedback. Na dúvida de como estruturar, siga o padrão da Score API do Langfuse: feedback é um score com `trace_id` como FK.

## Como explicar em inglês

**Interview quote:** *"We capture two kinds of user signals: explicit — thumbs up/down and structured complaints — and implicit — re-prompt rate, abandonment, edit-after-paste, copy rate. Each signal has a different noise-to-signal ratio and collection cost, so we weight them differently. Explicit feedback is sparse but high-signal when negative; implicit is high-volume but requires modeling to interpret. The key discipline is linking every feedback to a trace_id so we can always answer: which prompt version, which model, what context produced this?"*

| Português | Inglês |
|---|---|
| Curtida / descurtida (thumbs) | Thumbs up / thumbs down |
| Taxa de re-prompt | Re-prompt rate |
| Abandono da sessão | Session abandonment |
| Editar após colar (implícito) | Edit-after-paste (implicit signal) |
| Viés de confirmação | Confirmation bias |
| Popularidade ≠ qualidade | Popularity ≠ quality |
| Feedback explícito | Explicit feedback |
| Sinal implícito | Implicit signal |
| Relação de ruído por sinal | Noise-to-signal ratio |
| Sycofantia (bajulação) | Sycophancy |

## O que vem a seguir

Com feedback do usuário capturado e integrado ao loop, a nota 07 fecha o galho cobrindo o **portão final**: eval gates em CI — como transformar o golden set em bloqueio automático de PR, impedindo que mudanças de prompt que causem regressão cheguem à produção sem aviso.

## Fontes

- **Langfuse** — [*User feedback (Score API)*](https://langfuse.com/docs/scores/getting-started).
- **Braintrust** — [*Human review and feedback*](https://www.braintrust.dev/docs/guides/human-review).
- **Helicone** — [*User feedback*](https://docs.helicone.ai/features/user-feedback).
- **Arize** — [*Phoenix annotations*](https://docs.arize.com/phoenix). Feedback como annotation.
- **Sharma et al.** — *Towards Understanding Sycophancy in Language Models* ([arxiv:2310.13548](https://arxiv.org/abs/2310.13548)). Risco de treinar em thumbs up bruto.
- **Anthropic** — [*Constitutional AI*](https://www.anthropic.com/research/constitutional-ai). Padrão pra reduzir dependência de feedback humano cru.
- **Eugene Yan** — [*Evals are all you need*](https://eugeneyan.com/writing/evals/). Discute peso relativo de eval vs feedback.
- **Aman Khan** — [*The anatomy of user feedback in LLM apps*](https://aman.ai/primers/ai/llm-feedback/). Taxonomia de sinais.
- **Cohere** — [*Human preference data*](https://cohere.com/blog/preference-data). Como preference data de usuário vira sinal de fine-tuning.
- **OpenAI** — [*Learning to summarize from human feedback*](https://openai.com/research/learning-to-summarize-with-human-feedback). Origem acadêmica do pipeline de feedback humano.
- **Gallot et al.** — *Feedback Collection in the Wild* (2025). Estudo empírico de padrões de feedback em produtos de LLM.

## Veja também

- [[01 - O ciclo eval → diff → ship]] — feedback é uma das fontes do passo 1 (observability)
- [[03-Dominios/Tecnologia/IA/Evaluation/04 - LLM-as-judge — quando e como]] — judge enviesado por feedback vira problema
- [[Observability]] — feedback como sinal no observability stack
- [[03-Dominios/Tecnologia/IA/Anatomia dos LLMs/19 - Evaluation de LLMs em produção]] — A/B em prod cruza com feedback
- [[Segurança e Guardrails]] — sycophancy é falha de guardrail comportamental
- [[02 - A-B testing de prompts]] — sinais de feedback alimentam métricas do A/B
- [[05 - Auto-prompt optimization — DSPy e além]] — feedback curado entra no trainset do compiler
- [[03-Dominios/Tecnologia/IA/Observability/03 - Tracing de LLMs — OpenTelemetry e Langfuse]] — trace_id que linkeia feedback ao log
- [[Dicionário de IA#Thumbs up/down|Dicionário: Thumbs feedback]]
- [[Dicionário de IA#Re-prompt rate|Dicionário: Re-prompt rate]]
- [[Dicionário de IA#Sycophancy|Dicionário: Sycophancy]]
- [[Dicionário de IA#Implicit feedback|Dicionário: Implicit feedback]]
