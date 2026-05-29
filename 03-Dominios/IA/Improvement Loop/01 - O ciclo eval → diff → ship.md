---
title: "01 - O ciclo eval → diff → ship"
created: 2026-05-28
updated: 2026-05-28
type: concept
status: seedling
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

O ciclo eval → diff → ship é a operação interna da [[AI Engineering Stack/12 - Improvement Layer|Improvement Layer]]. A layer define **o que** acontece (loop fechado, ownership, cadência); este ciclo define **como** acontece operacionalmente.

A layer apoia-se em outras duas:

- [[AI Engineering Stack/09 - Evaluation Layer|Evaluation Layer]] entrega o passo 2
- [[AI Engineering Stack/11 - Logging Layer|Logging Layer]] / observability entrega o passo 1

E retroalimenta:

- [[AI Engineering Stack/03 - Prompt Layer|Prompt Layer]] (mudança do prompt)
- [[AI Engineering Stack/04 - Context Layer|Context Layer]] (novos casos no contexto)

## Anti-padrões

- **One-shot prompt** — escreveu, está bom, fim. Sem loop, prompt degrada silenciosamente.
- **Eval só no laboratório** — passa em golden set, vai pra prod, ninguém mais mede em prod. Drift invisível.
- **Mudança grande, eval pequena** — mexeu em 5 coisas, rodou 10 exemplos. Resultado: não dá pra atribuir.
- **Ship sem A/B em produto crítico** — funcionou no offline ≠ funciona em prod. Canary é barato; pular é caro.
- **Rollback sem postmortem** — voltou pra versão anterior, esqueceu por que. Próximo loop comete o mesmo erro.
- **Loop sem owner** — todo mundo é responsável = ninguém é responsável. Sem owner por loop, não fecha.

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
- [[AI Engineering Stack/12 - Improvement Layer]] — a camada conceitual onde este ciclo opera
