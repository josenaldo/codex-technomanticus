---
title: "01 - O ciclo eval → diff → ship"
created: 2026-05-28
updated: 2026-06-28
type: concept
status: seedling
fase: iniciado
progress: in_progress
tags:
  - improvement-loop
  - ia
  - ciclo
  - eval-driven
publish: true
aliases:
  - Eval-diff-ship
  - Improvement cycle
---

# 01 - O ciclo eval → diff → ship

> [!abstract] TL;DR
> Sistema de IA em produção não é one-shot: ele degrada (modelo do provider muda, distribuição de input muda, schema de output drifta) e ele evolui (eval expõe lacuna, surge hipótese, mudança precisa ir pra prod). O ciclo canônico é **eval → diff → ship**, expandido em 5 passos: (1) observability surface um problema; (2) eval mede a magnitude com golden set; (3) hipótese de mudança vira diff; (4) A/B test valida; (5) champion-challenger promove ou faz rollback. Maturidade do time se mede pela fração desse ciclo que é **automática** vs **manual**. O *one-shot prompt* — "escrevi, está bom, segue a vida" — é o anti-padrão fundador desta trilha.

> [!question]- Em que nível de maturidade eu deveria estar agora? E por onde começo se nunca tive nenhum loop?
> Para time novo: Nível 1 em 2 semanas. O investimento mínimo é três coisas: (a) criar um golden set de 20-50 exemplos representativos da tarefa principal; (b) versionar prompts em Git com convenção `MAJOR.MINOR.PATCH`; (c) rodar o golden set antes de qualquer mudança de prompt e comparar score. Esse ciclo manual, feito em planilha, já elimina os erros mais custosos (regressão não detectada, perda da versão anterior). Nível 2 (eval em CI) vem só depois que o golden set é estável — colocar CI sem golden set confiável é alarme falso garantido. Nunca pule do Nível 0 direto pro Nível 3 — o ciclo manual ensina o que a automação ainda não consegue capturar.

## Por que sistemas de IA precisam de loop

Três forças degradam ou desafinam sistema de LLM em produção:

1. **Mudança do modelo** — provider atualiza versão (mesmo "GPT-4o" tem snapshots diferentes), behavior shifta sem aviso. Pinned model ID mitiga mas não elimina, e prompt otimizado pra `claude-sonnet-4-5` pode não ser ótimo pra `claude-sonnet-4-6`.
2. **Distribution shift de tráfego** — input em produção muda ao longo do tempo (usuários novos, idiomas novos, casos não cobertos no golden set inicial). Prompt que era bom em janeiro pode falhar em abril com a mesma rubrica.
3. **Schema drift** — output que o consumer espera evolui (novo campo, nova categoria de tool call). Mantém o prompt sem mexer = quebra de consumer ou degradação silenciosa.

E duas forças puxam pra melhorar mesmo sem degradação:

4. **Hipóteses do time** — "se eu adicionar few-shot pra caso edge X, melhora?". Sem ciclo, vira aposta cega.
5. **Feedback do usuário** — sinal explícito (thumbs down) ou implícito (re-prompt rate) aponta categoria de falha. Sem ciclo, feedback morre no dashboard.

O **Improvement Loop** é o mecanismo que transforma essas cinco forças em mudanças versionadas e medidas.

## O ciclo em 5 passos

```
        ┌─────────────────────────────────┐
        │  1. Observability surface       │
        │  (trace, dashboard, alert,      │
        │   feedback do usuário)          │
        └────────────┬────────────────────┘
                     │
                     ▼
        ┌─────────────────────────────────┐
        │  2. Eval mede a magnitude       │
        │  (golden set, judge, métricas   │
        │   por categoria)                │
        └────────────┬────────────────────┘
                     │
                     ▼
        ┌─────────────────────────────────┐
        │  3. Diff — hipótese vira mudança│
        │  (novo prompt, few-shot novo,   │
        │   modelo trocado, tool nova)    │
        └────────────┬────────────────────┘
                     │
                     ▼
        ┌─────────────────────────────────┐
        │  4. A/B test                    │
        │  (offline eval + canary com     │
        │   tráfego pequeno)              │
        └────────────┬────────────────────┘
                     │
                     ▼
        ┌─────────────────────────────────┐
        │  5. Champion-challenger ship    │
        │  (promove com gate ou rollback) │
        └────────────┬────────────────────┘
                     │
                     ▼
              ┌──────────────┐
              │ Volta pra 1  │  ← feedback do que foi promovido
              │ (loop)       │     vira novo sinal de observability
              └──────────────┘
```

Os feedbacks importantes que fecham o loop:

- De 5 → 1: depois de promovido, o **próprio comportamento em prod** entra na observability como input do próximo ciclo.
- De 4 → 2: A/B pode revelar que a métrica escolhida no passo 2 não é boa proxy — força recalibrar eval.
- De 3 → 2: tentar formular o diff expõe lacunas na rubrica — força refinar eval **antes** de tentar a mudança.

## Os 5 passos em detalhe

### 1. Observability surface o problema

Sinal pode vir de quatro lugares ([[Observability]]):

| Origem | Exemplo |
|---|---|
| Dashboard de qualidade | Eval score caiu de 0.85 → 0.78 nos últimos 14 dias |
| Alerta de custo/latência | Token médio dobrou (signal de over-engineered prompt) |
| Feedback explícito | Thumbs down aumentou em 3x na categoria "summarization" |
| Incidente reportado | Cliente XYZ disse "respostas estão erradas pra português europeu" |

Sem observability, o ciclo nem começa — o problema simplesmente não aparece.

### 2. Eval mede a magnitude

Sinal de observability é **qualitativo** ("parece pior"). Eval traduz pra **quantitativo** ("score caiu 8% na categoria summarization em pt-EU"). Sem essa tradução, hipótese vira aposta:

- Golden set rodado contra a versão atual = baseline confirmado
- Golden set filtrado pela categoria suspeita = isola a regressão
- LLM-as-judge ou rubrica humana confirma que a regressão é real (não ruído estatístico)

Saída: relatório com **delta numérico por categoria**, não "está pior".

### 3. Diff — hipótese vira mudança

Hipótese sai do time: "few-shot com 3 exemplos pt-EU resolve" ou "trocar judge de Sonnet pra Opus calibra melhor". Diff é o **mínimo possível** pra testar a hipótese:

- Uma mudança por experimento (se mexer em 4 coisas e melhorar, qual foi?)
- Diff versionado ([[03 - Prompt versioning — semver para prompts]]): minor pra mudança comportamental, major pra mudança de schema
- Diff documenta: hipótese, eval esperado, métrica primária

### 4. A/B test

Mesmo com eval offline mostrando ganho, **produção é diferente** (distribuição real, ruído, latência). A/B com tráfego pequeno (5-10%) por tempo definido valida em dado real ([[02 - A-B testing de prompts]]).

Resultado possível:

- Ganho confirma offline → vai pro passo 5
- Ganho não confirma → ou amostra muito pequena, ou diff não generaliza, ou métrica não é boa proxy → volta pro passo 2 ou 3
- Ganho confirma **mas** outra métrica regride → mais ciclos antes de ship

### 5. Champion-challenger ship

Promoção não é "merge e reza". É operação com gate ([[04 - Champion-challenger em produção]]):

- Critérios objetivos (eval score, golden subset, custo, latência)
- Promoção automática se critérios passarem
- Rollback automático se um alerta dispara nas primeiras horas
- Versão antiga não é deletada — fica disponível pra rollback rápido

## Maturidade do ciclo

```
Nível 0 — Ad-hoc
  "Mudei o prompt porque me pareceu melhor"
  Sem eval. Sem versão. Sem A/B.

Nível 1 — Manual loop
  Eval rodado à mão antes de cada release.
  Prompt versionado em Git.
  A/B é "rollback se reclamarem".

Nível 2 — Semi-automatizado
  Eval em CI bloqueia regressão crítica.
  Prompt registrado com label production/staging.
  A/B em produção via feature flag, com gate manual.

Nível 3 — Automatizado com gates
  Eval gate em PR + full eval em main.
  Champion-challenger com promoção/rollback automático.
  Drift detection via eval contínua.

Nível 4 — Auto-otimizado
  DSPy ou similar compila prompts contra eval function.
  Loop fechado: feedback do usuário → dataset → recompile.
  Humano supervisiona, máquina otimiza.
```

Meta realista pra time típico em 2026: **nível 2 estável, com partes em nível 3**. Nível 4 ainda é fronteira, vale pra pipeline crítico ou time grande.

## Posição no AI Engineering Stack

O ciclo eval → diff → ship é a operação interna da [[03-Dominios/Tecnologia/IA/AI Engineering Stack/12 - Improvement Layer|Improvement Layer]]. A layer define **o que** acontece (loop fechado, ownership, cadência); este ciclo define **como** acontece operacionalmente.

A layer apoia-se em outras duas:

- [[03-Dominios/Tecnologia/IA/AI Engineering Stack/09 - Evaluation Layer|Evaluation Layer]] entrega o passo 2
- [[03-Dominios/Tecnologia/IA/AI Engineering Stack/11 - Logging Layer|Logging Layer]] / observability entrega o passo 1

E retroalimenta:

- [[03-Dominios/Tecnologia/IA/AI Engineering Stack/03 - Prompt Layer|Prompt Layer]] (mudança do prompt)
- [[03-Dominios/Tecnologia/IA/AI Engineering Stack/04 - Context Layer|Context Layer]] (novos casos no contexto)

## Cadência recomendada por tipo de sistema

O ciclo não tem frequência fixa — depende de quanto o sistema muda e o quanto falha custa:

| Tipo de sistema | Cadência de eval | Gatilho de ciclo |
|----------------|-----------------|-----------------|
| Assistente interno (low stakes) | Mensal | Reclamação explícita ou mudança de modelo |
| Produto B2C (médio stakes) | Semanal | Thumbs-down rate > threshold ou alert de custo |
| Pipeline de dados crítico | Por commit | CI gate; qualquer PR com mudança de prompt |
| Real-time (trading, saúde, segurança) | Contínua + gate | Drift detection automático; rollback automático |
| POC / MVP | A cada iteração grande | Qualitativo manual basta no início |

Regra de bolso: **quanto maior o custo de erro em produção, mais frequente e automatizado deve ser o ciclo**. POC que vai virar produto crítico em 3 meses deve implementar o loop antes da virada, não depois.

## Código: loop manual em Python

Um eval loop mínimo — roda o golden set, compara com baseline, imprime delta:

```python
import json
from anthropic import Anthropic

client = Anthropic()
PROMPT_VERSION = "1.2.0"

def run_eval(golden_set: list[dict], system_prompt: str) -> float:
    scores = []
    for example in golden_set:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            system=system_prompt,
            messages=[{"role": "user", "content": example["input"]}],
        )
        output = response.content[0].text
        # Rubrica simples: LLM judge ou heurística
        score = score_output(output, example["expected"])
        scores.append(score)
    return sum(scores) / len(scores)

# Comparação baseline vs candidato
baseline_score = run_eval(golden_set, BASELINE_PROMPT)
candidate_score = run_eval(golden_set, CANDIDATE_PROMPT)
delta = candidate_score - baseline_score
print(f"Baseline: {baseline_score:.3f} | Candidato: {candidate_score:.3f} | Δ={delta:+.3f}")
if delta >= 0.02:
    print(f"→ Candidato v{PROMPT_VERSION} aprovado pra A/B")
else:
    print("→ Candidato não melhora; reveja hipótese")
```

Esse script cabe no passo 2 do ciclo: depois de rodar, o delta numérico substitui "parece melhor" por dado verificável.

## Anti-padrões

- **One-shot prompt** — escreveu, está bom, fim. Sem loop, prompt degrada silenciosamente.
- **Eval só no laboratório** — passa em golden set, vai pra prod, ninguém mais mede em prod. Drift invisível.
- **Mudança grande, eval pequena** — mexeu em 5 coisas, rodou 10 exemplos. Resultado: não dá pra atribuir.
- **Ship sem A/B em produto crítico** — funcionou no offline ≠ funciona em prod. Canary é barato; pular é caro.
- **Rollback sem postmortem** — voltou pra versão anterior, esqueceu por que. Próximo loop comete o mesmo erro.
- **Loop sem owner** — todo mundo é responsável = ninguém é responsável. Sem owner por loop, não fecha.

## Armadilhas comuns

> [!warning] Não ter golden set — e achar que "parece melhor" é suficiente
> Intuição sobre qualidade de LLM falha sistematicamente: o modelo dá resposta mais fluida mas menos precisa e você acha que melhorou. Sem golden set com métricas objetivas, cada ciclo é aposta. O investimento mínimo pra escapar disso é 20-50 exemplos representativos com critério de avaliação claro por categoria. Se não tiver tempo pra montar o golden set agora, não tem ciclo — tem caos versionado. O golden set é o ativo mais valioso do loop; proteja-o como você protege o schema do banco.

> [!warning] Fazer múltiplas mudanças no mesmo diff — e não saber o que causou o resultado
> "Troquei o modelo, adicionei 3 few-shots, mudei a instrução de saída e ajustei a temperatura" num único PR. Eval melhorou 5%. Qual das quatro mudanças foi responsável? Você não sabe. Na próxima regressão, você vai tentar reverter sem saber o que reverter. O princípio é cirúrgico: **uma hipótese por diff**. Se você precisa testar 4 hipóteses, rode 4 experimentos sequenciais ou paralelos com eval isolado. Mais lento por experimento, mas o resultado é interpretável — e o próximo ciclo é mais rápido porque o contexto foi preservado.

> [!warning] Não ter owner para o loop — e o ciclo morrer por inércia organizacional
> Improvement Loop não acontece sozinho: alguém precisa ser responsável por ler o dashboard de qualidade, propor hipóteses, coordenar A/B, e decidir ship ou rollback. "Todo mundo é responsável" na prática significa "ninguém fez". Em times pequenos, 1 pessoa dedica 20% do tempo ao loop; em times médios, 1 eng de plataforma é o *prompt reliability engineer* informal. Sem ownership explícito, o loop fecha quando tem problema urgente e desaparece quando as coisas parecem ok — que é exatamente quando o drift acumula silenciosamente.

## Como explicar em inglês

**Interview quote:** *"LLM systems in production are not set-and-forget — they degrade through model updates, distribution shift, and schema drift, and they evolve through new hypotheses. The canonical improvement cycle is eval → diff → ship: observability surfaces a problem, eval quantifies it against a golden set, a hypothesis becomes a minimal diff, A/B test validates in production, and champion-challenger mechanics promote or rollback. Team maturity is measured by how much of that cycle is automated versus manual."*

| Português | Inglês |
|---|---|
| Ciclo de melhoria contínua | Improvement loop |
| Conjunto dourado de avaliação | Golden set / evaluation dataset |
| Derivação de distribuição | Distribution shift |
| Desvio de schema | Schema drift |
| Hipótese vira diff | Hypothesis becomes a diff |
| Teste A/B em produção | A/B test in production |
| Campeão-desafiante | Champion-challenger |
| Promover ou fazer rollback | Promote or rollback |
| Loop com owner | Owned improvement loop |
| Eval contínua | Continuous evaluation |

## O que vem a seguir

Com o ciclo completo mapeado, a nota 02 desce no passo 4 — o **A/B test de prompts**: como configurar o split, quais métricas primárias e guardrails usar, como decidir quando a amostra é grande o suficiente para concluir, e o que fazer quando os resultados contradizem o eval offline.

## Fontes

- **@hooeem** — *Become an AI Engineer*, thread #18, Step 11 (*Improvement Layer*). Vocabulário e cadência do loop.
- **Hamel Husain** — [*Your AI Product Needs Evals*](https://hamel.dev/blog/posts/evals/). Eval contínua como motor do loop.
- **OpenAI** — [*Evals cookbook*](https://github.com/openai/openai-cookbook/tree/main/examples/evaluation). Padrões operacionais.
- **Chip Huyen** — *AI Engineering* (2025), capítulos de evaluation e iteration. Discussão sistemática de iteration loop.
- **Anthropic** — [*Iterative prompt engineering*](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview). Prática iterativa documentada pelo lab.

## Veja também

- [[02 - A-B testing de prompts]] — o experimento que valida o diff
- [[04 - Champion-challenger em produção]] — o mecanismo de ship com gate
- [[07 - Eval gates em CI — quando bloquear merge]] — como o passo 2 vira parte do pipeline
- [[Evaluation]] — trilha do passo 2
- [[Observability]] — trilha do passo 1
- [[03-Dominios/Tecnologia/IA/AI Engineering Stack/12 - Improvement Layer]] — a camada conceitual onde este ciclo opera
- [[Dicionário de IA#Golden set|Dicionário: Golden set]]
- [[Dicionário de IA#Champion-challenger|Dicionário: Champion-challenger]]
- [[Dicionário de IA#Distribution shift|Dicionário: Distribution shift]]
