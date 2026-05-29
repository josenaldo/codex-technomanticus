---
title: "08 - Reasoning models — audit trail, não chain-of-thought"
created: 2026-05-28
updated: 2026-05-28
type: concept
status: seedling
progress: in_progress
tags:
  - prompt-engineering
  - ia
  - reasoning-models
publish: true
aliases:
  - Reasoning models prompting
  - Audit trail prompt
  - Como pedir a o3
---

# 08 - Reasoning models — audit trail, não chain-of-thought

> [!abstract] TL;DR
> Em modelos clássicos, *"think step-by-step"* era uma das alavancas mais eficazes — induzia chain-of-thought, que melhorava raciocínio. Em **reasoning models** (o3, R1, Gemini Thinking), esse pedido virou noise: a cadeia interna já acontece. Pedir CoT de novo polui o output sem ganho. O que muda: você deixa de pedir *raciocínio*, e passa a pedir **audit trail** — pontos de checagem do raciocínio interno (assumptions, checkpoints-chave, uncertainties, como verificar). Esta nota separa o que pedir e o que evitar em reasoning models, com tabela modelo × pedido recomendado × pedido a evitar.

## A mudança de regime

Modelos clássicos (GPT-4, Claude 3.5, Llama 3) precisavam ser **induzidos a raciocinar**. Sem CoT explícito, o output era uma conclusão direta — sem cadeia, sem auditoria. Pedir *"think step-by-step"* destravava a cadeia, que destravava qualidade.

Reasoning models — o3, DeepSeek R1, Gemini Thinking, Claude com extended thinking — fazem a cadeia **internamente**, antes de devolver. O usuário recebe o output já calibrado por uma fase de pensamento. A cadeia é parte do modelo, não do prompt.

Consequência: o pedido *"think step-by-step"* num reasoning model:

- **Não destrava nada** — a cadeia já acontece.
- **Polui o output** — o modelo pode duplicar o pensamento interno como prosa externa, inflando tokens sem ganho.
- **Confunde calibração** — em alguns modelos, força um modo "show your work" que não é o nativo, gerando degradação.

## O novo pedido: audit trail

Em vez de pedir a cadeia, peça os **artefatos de auditoria** da cadeia que já aconteceu. O modelo deve devolver:

1. **Resposta final.** A conclusão calibrada.
2. **Assumptions.** Premissas que o modelo adotou pra responder.
3. **Key reasoning checkpoints.** Os 2-4 pontos de inflexão do raciocínio interno (não a cadeia inteira — só os pivôs).
4. **Uncertainties.** Onde o modelo está em terreno frágil.
5. **How to verify.** Como o usuário poderia checar a resposta de fora.

O esqueleto:

```
Responda a pergunta. Para a resposta, devolva:

1. Final answer
2. Assumptions: as premissas que você adotou
3. Key reasoning checkpoints: 2-4 pontos de inflexão (não a cadeia
   inteira — só os pivôs)
4. Uncertainties: onde sua resposta é mais frágil; use confidence
   levels (high/moderate/low/unknown)
5. How to verify: como eu poderia checar essa resposta sem você

Pergunta: <pergunta>
```

A diferença é cirúrgica: você está pedindo **metadata da inferência**, não a inferência em si. O modelo já pensou — você quer o relatório auditável do pensamento.

## Por que isso funciona melhor

- **Não duplica trabalho.** A cadeia interna já roda; o modelo só precisa **resumir e auditar** o que produziu, não re-fazer.
- **Output mais útil.** Você consegue auditar a resposta de fora, em vez de ler trezentas linhas de CoT.
- **Tokens economizados.** O thinking interno é mais barato (geralmente em pricing reduzido); o output curto, mais barato ainda.
- **Calibrável.** Confidence levels explícitos são o que separa resposta confiável de resposta falsamente assertiva.

## Tabela: modelo × pedido recomendado × pedido a evitar

| Modelo | Pedido recomendado | Pedido a evitar |
|---|---|---|
| **GPT-4 / GPT-4 Turbo** (clássico) | *"Think step-by-step"* + CoT; few-shot com exemplos de raciocínio | Pedir só "final answer" sem CoT (deixa qualidade na mesa) |
| **Claude 3.5 / Claude 4** (sem extended thinking) | *"Think through this carefully"* + CoT explícito | Pedido vago ("solve this") |
| **o3 / o4** (reasoning model) | "Final answer + assumptions + checkpoints + uncertainties + how to verify" | *"Think step-by-step"* (redundante, polui output) |
| **DeepSeek R1** (reasoning model) | Mesmo padrão de audit trail; tag `<think>` é interna, não precisa pedir | Forçar CoT externo |
| **Gemini Thinking** (reasoning model) | Audit trail; pode pedir resumo do "thinking" como parte do output | CoT explícito (sobrepõe ao modo de pensamento) |
| **Claude 4 (Opus/Sonnet) com extended thinking** | Definir tempo de thinking; pedir resumo de checkpoints no output final | Pedir *"think step-by-step"* explicitamente — Claude já roda |
| **Modelos locais pequenos (7B-13B)** sem reasoning | CoT explícito + few-shot; modelos pequenos precisam da indução | Esperar audit trail rico — eles não geram |

## Pitfalls específicos de reasoning models

### Pedir CoT por hábito

O hábito de adicionar *"think step-by-step"* no fim de todo prompt é fortemente arraigado. Em reasoning models, vira ritual sem efeito. Pior: alguns reasoning models mudam de modo quando o detectam, regredindo pra um padrão menos otimizado.

Regra: cheque o modelo antes. Se for reasoning, retire o CoT explícito. Se não souber, deixe — em modelos clássicos não atrapalha.

### Esperar a cadeia inteira como output

Reasoning models não devolvem a cadeia interna por default — só a conclusão. Querer a cadeia exige pedido explícito, geralmente um "summarize your reasoning" no final. E mesmo assim você recebe um resumo, não o thinking literal.

### Confundir "thinking time" com "instrução de profundidade"

Em modelos com tempo de thinking configurável (Claude extended, o3 com reasoning effort), o controle é via **parâmetro**, não via prompt. Dizer *"pense mais profundamente"* no prompt não estende o tempo de thinking. Configure no parâmetro.

### Pedir confidence em modelos clássicos esperando o mesmo

Modelos clássicos respondem a "use confidence levels" também, mas a calibração é pior — eles tendem a marcar tudo como "high confidence". Reasoning models calibram melhor porque a fase de thinking produz incerteza real.

## Quando ainda pedir step-by-step

Algumas situações justificam CoT explícito mesmo em modelos clássicos não-reasoning:

- **Aritmética complexa em modelo não-reasoning.** Pedir cadeia ainda ajuda.
- **Raciocínio multi-step com input que exige decomposição visível.** Quando você quer auditar o passo, não só a conclusão.
- **Few-shot com exemplos de CoT.** Demonstrar a cadeia em exemplos ainda ensina o padrão.

Em reasoning models, nenhuma dessas se aplica — o modelo já faz internamente.

## Composição com role e constraints

Audit trail compõe naturalmente com [[03 - Roles e personas — escolhendo o juízo do modelo|roles]] e [[06 - Constraints declarativas — boundaries como engenharia|constraints]]:

```
Act as a senior physicist evaluating a back-of-the-envelope
estimate.

Standard: accuracy first; if the estimate is wrong by more than
2x, the answer is "no, here's why".

Output format:
1. Final answer (yes/no/inconclusive)
2. Assumptions you made
3. Key checkpoints in your reasoning (max 4)
4. Uncertainties with confidence levels
5. How I could verify this independently

Constraints:
- Generate your own estimate before using mine; do not anchor
- If my estimate is wrong, say so before supporting your answer
```

O role estabelece o juízo; o audit trail estrutura o output; as constraints fecham caminhos de fuga.

## Composição com Karpathy

O mega-prompt do Karpathy ([[04 - O mega-prompt do Karpathy — anatomia da anti-sycophancy|nota 04]]) inclui *"Process information and explain your answers step by step"* — essa cláusula é a única que precisa ser **revista** ao usar o prompt em reasoning models. Em o3/R1/Gemini Thinking, ou se ignora (o modelo já faz internamente) ou se substitui pelo audit trail descrito aqui.

A versão "Karpathy para reasoning":

```
[mantém tudo do prompt original, exceto]

Substituir:
"Process information and explain your answers step by step."

Por:
"Devolva: (1) resposta final, (2) checkpoints-chave do seu
raciocínio interno, (3) assumptions adotadas, (4) uncertainties
com confidence levels, (5) como eu poderia verificar."
```

## Fontes

- **@hooeem** — *Become an AI Engineer*, cap #5. Origem do framing "audit trail, não chain-of-thought".
- **OpenAI** — *Reasoning best practices* (docs OpenAI para o-series).
- **DeepSeek** — *R1 technical report* (2025).
- **Anthropic** — *Extended thinking* (docs.anthropic.com/extended-thinking).
- **Wei et al.** — *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models* ([arxiv:2201.11903](https://arxiv.org/abs/2201.11903), 2022). Paper original de CoT em modelos clássicos.

## Veja também

- [[Anatomia dos LLMs/13 - Reasoning models e chain-of-thought|Anatomia — Reasoning models e chain-of-thought]] — o "porquê" por trás desta nota, em profundidade
- [[04 - O mega-prompt do Karpathy — anatomia da anti-sycophancy]] — cláusula step-by-step a revisar em reasoning models
- [[06 - Constraints declarativas — boundaries como engenharia]] — onde audit trail vira constraint de output
- [[Context Engineering/15 - Técnicas de prompting — zero-shot, few-shot, CoT, ToT|Context Engineering — Técnicas de prompting]] — CoT na taxonomia maior
