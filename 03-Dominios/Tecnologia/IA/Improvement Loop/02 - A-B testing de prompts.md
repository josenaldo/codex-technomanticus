---
title: "02 - A-B testing de prompts"
created: 2026-05-28
updated: 2026-05-28
type: concept
status: seedling
progress: in_progress
tags:
  - improvement-loop
  - ia
  - ab-testing
  - experimentation
publish: true
aliases:
  - A/B test de prompt
  - Experimentação de prompt
  - Prompt experimentation
---

# 02 - A-B testing de prompts

> [!abstract] TL;DR
> A/B testing de prompt é o experimento que valida o diff: mesmo input, dois prompts (control = champion, treatment = challenger), métrica primária pré-declarada, sample size suficiente, gate de decisão objetivo. Especificidade do contexto LLM: **variância é alta** (mesmo `temperature=0` varia entre snapshots do modelo), **N pequeno mente** (200 por arm é piso razoável pra eval score; mais pra feedback do usuário), e **bayesiano costuma ser mais adequado** que frequentista (small N, prior de eval offline, decisão sequencial). Anti-padrão central: **peeking** — parar o experimento cedo porque o resultado "tá bom". Tools 2026: Statsig, GrowthBook, Eppo pra A/B com estatística pronta; muitas equipes rodam custom em cima do registry de prompt (Langfuse Prompts, Braintrust) com cálculo bayesiano caseiro.

## A unidade de teste — o que é "control" e "treatment"

A/B de prompt mantém **tudo igual menos o prompt**:

| Variável | Control | Treatment |
|---|---|---|
| Prompt | v3.0 (champion) | v3.1 (challenger) |
| Modelo | `claude-sonnet-4-6` | `claude-sonnet-4-6` |
| Parâmetros de inferência | `temperature=0.2, top_p=0.9` | `temperature=0.2, top_p=0.9` |
| Input | mesmos casos do golden set OR mesma amostra de tráfego | (idem) |
| Métrica primária | (escolhida antes) | (idem) |

Se mudar mais de uma coisa por experimento (prompt + modelo, ou prompt + temperatura), você não consegue atribuir o ganho a uma causa específica. **Uma variável por experimento** é a regra que vale aqui.

## Onde rodar — offline vs online

| Modo | O que mede | Quando |
|---|---|---|
| **Offline (eval set)** | Performance no golden set | Antes do canary; gate de "vale ir pra prod?" |
| **Online (canary em prod)** | Performance em tráfego real | Após offline; valida em distribuição real |
| **Shadow** | Roda treatment em paralelo sem servir ao usuário | Quando treatment é arriscado (ex: modelo novo) e quer comparar sem expor |

Fluxo canônico:

```
offline (golden set, 100% treatment)
    ↓ passou no gate
canary online (5-10% tráfego treatment)
    ↓ N suficiente, métricas no verde
ramp up (50% treatment)
    ↓ confirma em volume
promoção (100% treatment vira novo champion)
```

Offline-only é tentador (rápido, barato) mas tem dois problemas: distribuição de input em prod difere do golden set (especialmente cauda longa), e métricas de negócio (conversão, retenção, NPS) só medem em prod.

## Métrica primária — escolher antes de rodar

A regra de ouro: **declarar a métrica antes do experimento**. Sem isso, você (involuntariamente) escolhe a métrica que ganha — viés de seleção.

Opções comuns por tipo de produto:

| Tipo de produto | Métrica primária candidata |
|---|---|
| Resposta a perguntas | Eval score (golden set + judge) |
| Sumário/extração | Eval score por dim (faithfulness, completeness) |
| Geração estruturada | % de output válido no schema |
| Agente com tools | Task completion rate |
| Chatbot com humano | Re-prompt rate, abandonment, thumbs feedback |
| Recomendação | Click-through, conversion downstream |

Métricas **secundárias** (guardrails que não podem regredir) também declaradas antes:

- Custo médio por request (não pode subir > X%)
- Latência p95 (não pode subir > Y%)
- Refusal rate (não pode mudar > Z pontos)
- Safety violations (zero tolerância)

Decisão final precisa olhar a primária **e** as secundárias. Treatment ganhar 5% no primary mas duplicar custo = não vale.

## Sample size — variância manda

LLM é estocástico mesmo com `temperature=0` (snapshot do modelo varia, infra cache varia). Variância nas métricas é maior que em A/B clássico de produto. Regras de bolso:

| Métrica | N mínimo por arm | Por quê |
|---|---|---|
| Eval score (golden set, judge automático) | ~200 | Variância de judge + amostragem |
| User feedback (thumbs up/down) | ~1.000 | Sinal binário esparso |
| Conversão downstream | ~10.000 | Efeito de tamanho pequeno + ruído |
| Métrica contínua (NPS, satisfação) | ~500 | Variância média |

**Estes números são piso de bolso, não derivação estatística**. Cálculo formal de power depende do baseline da métrica, do efeito mínimo detectável (MDE), e da variância observada. Ferramentas como Statsig e GrowthBook fazem o cálculo automático; cálculo manual usa fórmulas clássicas (e.g., `n ≈ 16σ²/Δ²` pra MDE Δ em métrica contínua).

Se o experimento precisa de 10k por arm e produto só faz 100 requests/dia por arm = 200 dias. Trade-off real: ou aumenta tráfego do canary (mais risco) ou aceita decisão com confiança menor.

## Frequentista vs bayesiano — por que bayesiano costuma encaixar melhor

Frequentista clássico (t-test, chi-squared):

- Decisão binária no fim: rejeita H0 ou não
- Precisa de N pré-declarado (ou correção forte pra peeking)
- p-value não responde "qual a probabilidade de B ser melhor"

Bayesiano (cálculo de posterior, e.g., beta-binomial pra conversão):

- Decisão pode ser sequencial sem inflar erro tipo I
- Dá probabilidade direta: "P(B > A) = 0.87"
- Acomoda prior — eval offline vira informação genuína no posterior
- Funciona melhor com N pequeno

**Por que prompt A/B encaixa melhor com bayesiano:**

1. N é tipicamente pequeno (centenas a milhares, não milhões)
2. Você tem prior forte do offline (vai entrar no experimento já com a hipótese de que treatment ≥ control)
3. Decisão é sequencial — você quer parar cedo se o sinal é claro, sem pagar correção forte de peeking
4. Decisão tem múltiplas dimensões (primary + guardrails) — Bayesiano lida melhor com múltiplas posteriors

**Quando frequentista ainda faz sentido:**

- Time já tem A/B framework frequentista maduro
- Métrica é conversão simples com volume alto
- Auditoria/regulação exige p-value clássico

Tools como Statsig, GrowthBook, Eppo oferecem ambos os modos; a escolha é mais de cultura do time que de teoria.

## Peeking — o anti-padrão central

**Peeking** é parar o experimento cedo porque "parece bom" — sem ajustar pra múltiplas comparações ou paradas sequenciais. Resultado: você infla a taxa de falso positivo. Experimento que parece significativo a 50% do N não é o mesmo experimento que seria significativo no N completo.

Como mitigar:

- **Pré-declarar N e duração** (frequentista) — só olha no fim
- **Always-valid p-values** (mSPRT, e-values) — permitem olhar quando quiser, mas com correção
- **Bayesian decision threshold** (e.g., parar se P(B > A) > 0.95 e expected loss < ε) — natural pra sequential

Sinal de que o time peeking-a: "olha, B já tá 8% acima depois de 3 dias, vamos promover". Resposta correta: o N declarado era 14 dias por uma razão.

## Tools 2026

| Tool | Tipo | Forte em | Tradeoff |
|---|---|---|---|
| **Statsig** | SaaS | A/B com estatística bayesiana built-in, free tier generoso | Mais um vendor; integração com prompt registry é custom |
| **GrowthBook** | OSS + Cloud | OSS forte, frequentista + bayesiano, SDK em várias linguagens | Setup precisa mais cuidado que SaaS puro |
| **Eppo** | SaaS | Métricas com warehouse direto, governança forte | Mais caro; alvo enterprise |
| **Langfuse + custom** | OSS | Prompt versionado já no Langfuse; A/B via label `canary`/`production` + cálculo de posterior caseiro | Você implementa a estatística |
| **Braintrust** | SaaS | Eval offline + comparison view nativa; A/B online via integração com feature flag | Combina bem com Braintrust como eval framework |

Padrão pragmático: time pequeno usa Langfuse + cálculo bayesiano caseiro (beta-binomial de 30 linhas Python); time médio/grande adota GrowthBook ou Statsig pra ter estatística e UI prontas; enterprise vai Eppo ou Statsig enterprise.

## Esqueleto de A/B em Langfuse — exemplo prático

```python
import random
import langfuse

# 1. Routing — define qual arm cada request recebe
def select_prompt_arm(request_id: str, treatment_pct: float = 0.10) -> str:
    # hashing determinístico pra mesmo usuário ver mesma arm
    bucket = hash(request_id) % 100
    return "canary" if bucket < treatment_pct * 100 else "production"

# 2. Execução — pega prompt da label e registra arm no trace
arm_label = select_prompt_arm(request.id, treatment_pct=0.10)
prompt = langfuse.get_prompt("research-system", label=arm_label)

with langfuse.start_as_current_span(name="llm-call") as span:
    span.update(metadata={
        "experiment_id": "exp-2026-05-rephrase-pt",
        "arm": arm_label,
        "prompt_version": prompt.version,
    })
    response = client.messages.create(
        model="claude-sonnet-4-6",
        system=prompt.compile(),
        messages=[...],
    )
    span.update(output=response, metadata={"cost_usd": cost})

# 3. Análise — query por arm, calcula posterior
# (pseudo-código; rode em job offline ou notebook)
def analyze(experiment_id: str):
    traces = langfuse.fetch_traces(metadata={"experiment_id": experiment_id})
    df = build_df(traces)  # arm, eval_score, cost, latency
    posterior = beta_binomial_posterior(
        successes_a=df[df.arm == "production"].pass_count,
        n_a=df[df.arm == "production"].total,
        successes_b=df[df.arm == "canary"].pass_count,
        n_b=df[df.arm == "canary"].total,
    )
    return {
        "p_b_better_than_a": posterior.p_b_better,
        "expected_lift": posterior.expected_lift,
        "decision": "promote" if posterior.p_b_better > 0.95 else "continue",
    }
```

O fluxo: routing determinístico no entrypoint, atributo `arm` no span (chave de análise), cálculo offline em job/notebook. Sem precisar de SDK de A/B externo pra começar.

## Anti-padrões

- **Peeking** — discutido acima; o mais comum e mais danoso
- **Múltiplas variáveis por experimento** — mudou prompt + modelo + temperatura; impossível atribuir
- **Métrica escolhida depois** — viés de seleção; sempre declare antes
- **Sem guardrails secundários** — ganha em quality, regride em custo, ninguém viu
- **Sample size insuficiente** — declara vitória com 50 amostras e variância alta
- **Routing não-determinístico** — mesmo usuário vê arms diferentes em sessões diferentes; ruído enorme
- **Esquecer offline antes do canary** — exposição de usuário a treatment pior por economia de tempo
- **Promover sem postmortem do experimento** — perde aprendizado pro próximo ciclo

## Fontes

- **Statsig** — [*Bayesian A/B testing*](https://docs.statsig.com/stats-engine/methodologies/bayesian-testing). Material acessível sobre bayesiano em produto.
- **GrowthBook** — [*Statistics behind A/B testing*](https://docs.growthbook.io/statistics/details). Cobertura frequentista + bayesiano.
- **Eppo** — [*Sample size and statistical power*](https://www.geteppo.com/docs/statistics/sample-size). Cálculo de power.
- **Kohavi, Tang, Xu** — *Trustworthy Online Controlled Experiments* (2020). Livro canônico sobre A/B; tudo que não é específico de LLM se aplica.
- **Howard, Ramdas et al.** — *Time-uniform, nonparametric, nonasymptotic confidence sequences* ([arxiv:1810.08240](https://arxiv.org/abs/1810.08240)). Base teórica de always-valid inference.
- **OpenAI** — [*Evals cookbook — comparison patterns*](https://github.com/openai/openai-cookbook/tree/main/examples/evaluation). Padrões de comparação offline.

## Veja também

- [[01 - O ciclo eval → diff → ship]] — A/B é o passo 4 do ciclo
- [[03 - Prompt versioning — semver para prompts]] — A/B compara versões; versão precisa ser identificável
- [[04 - Champion-challenger em produção]] — o que acontece **depois** que o A/B decide
- [[03-Dominios/Tecnologia/IA/Evaluation/02 - Golden datasets — como construir]] — o dataset onde o A/B offline roda
- [[03-Dominios/Tecnologia/IA/Observability/05 - Versionamento de prompts]] — o registry que viabiliza o routing
- [[03-Dominios/Tecnologia/IA/Anatomia dos LLMs/19 - Evaluation de LLMs em produção]] — A/B em prod como pilar de eval contextual
