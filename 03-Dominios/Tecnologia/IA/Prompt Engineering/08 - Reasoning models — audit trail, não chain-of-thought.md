---
title: "08 - Reasoning models — audit trail, não chain-of-thought"
created: 2026-05-28
updated: 2026-07-03
type: concept
status: growing
progress: in_progress
fase: Iniciado
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
> Em modelos clássicos, *"think step-by-step"* era uma das alavancas mais eficazes — induzia chain-of-thought, que melhorava raciocínio.
> Em **reasoning models** (o3, R1, Gemini Thinking), esse pedido virou noise: a cadeia interna já acontece. Pedir CoT de novo polui o output sem ganho.
> O que muda: você deixa de pedir *raciocínio*, e passa a pedir **audit trail** — pontos de checagem do raciocínio interno (assumptions, checkpoints-chave, uncertainties, como verificar).
> Esta nota separa o que pedir e o que evitar em reasoning models, com tabela modelo × pedido recomendado × pedido a evitar.

> [!question]- O que eu preciso saber antes de ler isso?
> Esta nota pressupõe que você sabe o que é chain-of-thought (CoT) e por que ele melhora qualidade em modelos clássicos. Se não sabe, leia [[03-Dominios/Tecnologia/IA/Context Engineering/15 - Técnicas de prompting — zero-shot, few-shot, CoT, ToT|Técnicas de prompting]] antes. O ponto aqui é que reasoning models (o3, R1, Gemini Thinking, Claude com extended thinking) mudaram o jogo: o CoT acontece internamente, antes do output, e o prompt ideal para eles é diferente. Se você usa modelos clássicos, a nota anterior (few-shot, constraints) já é o suficiente; se usa reasoning models em produção, esta nota é leitura obrigatória.

## A mudança de regime

Modelos clássicos (GPT-4, Claude 3.5, Llama 3) precisavam ser **induzidos a raciocinar**. Sem CoT explícito, o output era uma conclusão direta — sem cadeia, sem auditoria. Pedir *"think step-by-step"* destravava a cadeia, que destravava qualidade.

Reasoning models — o3, DeepSeek R1, Gemini Thinking, Claude com extended thinking — fazem a cadeia **internamente**, antes de devolver. O usuário recebe o output já calibrado por uma fase de pensamento. A cadeia é parte do modelo, não do prompt.

Analogia: modelos clássicos são como um especialista que pensa em voz alta quando pedido; reasoning models são como um especialista que já chegou na sala com a análise pronta — você não precisa pedir pra ele pensar, mas pode pedir um resumo das premissas e pontos-chave em que se baseou.

Consequência: o pedido *"think step-by-step"* num reasoning model:

- **Não destrava nada** — a cadeia já acontece.
- **Polui o output** — o modelo pode duplicar o pensamento interno como prosa externa, inflando tokens sem ganho.
- **Confunde calibração** — em alguns modelos, força um modo "show your work" que não é o nativo, gerando degradação.

Em termos de custo: o thinking interno de reasoning models costuma ter pricing de 1-4x o output normal, e acontece independente do prompt. Pedir CoT externo por cima do thinking interno multiplica o custo sem multiplcar a qualidade.

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
- **Detectável quando o raciocínio falha.** Checkpoints e assumptions expostos tornam erros de raciocínio diagnosticáveis — você sabe onde a inferência divergiu, não apenas que o output está errado.
- **Compõe com outros elementos.** Audit trail funciona dentro de role prompts e com constraints declarativas sem atrito — você estrutura o output que quer ver sem interferir no thinking interno.

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

## Caso prático: prompt incorreto vs. correto

Para tornar a diferença concreta, veja o mesmo problema resolvido com os dois estilos de prompt — o hábito herdado de modelos clássicos e o audit trail recomendado para reasoning models.

**Cenário:** você quer saber se, ao implementar busca numa lista ordenada com até 10 milhões de elementos, vale mais usar busca binária recursiva ou a versão iterativa.

**Prompt incorreto** (CoT por hábito, aplicado a um reasoning model):

```
Think step-by-step. Devo usar busca binária recursiva ou iterativa
para buscar em uma lista ordenada de até 10 milhões de elementos?
Explique seu raciocínio detalhadamente, passo a passo, antes de
responder.

Pergunta: qual abordagem escolher e por quê?
```

Por que isso é um erro: em um reasoning model, "think step-by-step" não destrava nada que já não estivesse acontecendo — a cadeia interna já roda antes de qualquer token do output. O modelo reage de uma de duas formas, e as duas são ruins: ou repete o próprio pensamento interno como prosa longa (tokens gastos sem ganho de qualidade), ou trata o pedido como instrução de formatação e produz uma lista de "passos" artificiais — uma cadeia decorativa, escrita depois, que não é a auditoria do raciocínio real.

**Prompt correto** (audit trail):

```
Devo usar busca binária recursiva ou iterativa para buscar em uma
lista ordenada de até 10 milhões de elementos?

Devolva:
1. Final answer
2. Assumptions: as premissas que você adotou
3. Key reasoning checkpoints: 2-4 pontos de inflexão (não a cadeia
   inteira — só os pivôs)
4. Uncertainties: onde sua resposta é mais frágil; use confidence
   levels (high/moderate/low/unknown)
5. How to verify: como eu poderia checar essa resposta sem você
```

O formato de resposta esperado (a estrutura é estável; o conteúdo exato varia por modelo):

1. **Final answer:** iterativa — evita risco de estourar a pilha de chamadas em profundidades de recursão que, embora logarítmicas, ainda somam overhead de função por chamada em linguagens sem otimização de tail-call.
2. **Assumptions:** a linguagem-alvo não faz tail-call optimization (verdade para a maioria: Python, Java, JavaScript); a lista já está ordenada; não há limite de stack customizado no ambiente.
3. **Key checkpoints:** (i) a profundidade de recursão é logarítmica — log₂(10 milhões) ≈ 24 chamadas, o que normalmente não estouraria uma pilha padrão sozinho; (ii) mas o overhead por chamada de função pesa mais que o de uma iteração de loop, e isso importa quando a busca roda em um hot path chamado repetidamente.
4. **Uncertainties (moderate):** se a linguagem-alvo faz TCO (alguns compiladores Scheme, Erlang), a diferença de performance entre as duas versões desaparece — a resposta assume que não faz.
5. **How to verify:** rode um benchmark comparando as duas versões na linguagem real de destino, com profiling de tempo de CPU.

A diferença entre os dois prompts não está em quanto o modelo "sabe" — a cadeia interna é a mesma nos dois casos. A diferença está no que sobra para você auditar depois: o prompt incorreto devolve uma narrativa de raciocínio que pode ou não refletir o pensamento real; o prompt correto devolve pontos específicos e contestáveis — a assumption sobre TCO, o checkpoint sobre profundidade logarítmica — que você pode confirmar ou refutar um a um, em vez de aceitar ou rejeitar a resposta inteira em bloco.

## Armadilhas comuns

> [!warning] CoT por hábito vira ruído em reasoning models
> O hábito de adicionar "think step-by-step" no fim de todo prompt é fortemente arraigado — e em reasoning models, vira ruído. A cadeia interna já acontece; pedir explicitamente pode fazer o modelo duplicar o pensamento interno como prosa no output, inflando tokens sem ganho. Pior: alguns modelos mudam de modo ao detectar o pedido de CoT, regredindo pra um padrão menos otimizado. Antes de usar qualquer prompt com um modelo novo, verifique se ele é reasoning ou clássico — o prompt ideal é radicalmente diferente.

> [!warning] Thinking time é parâmetro, não instrução de prompt
> Em modelos com tempo de thinking configurável (o3 com reasoning effort, Claude com extended thinking, Gemini Thinking), a profundidade de raciocínio é controlada via **parâmetro da API**, não via texto no prompt. Dizer "pense mais profundamente" ou "use mais tempo" no prompt não estende o thinking — essa instrução só chega ao output, não ao orçamento de tokens de thinking. Configure no parâmetro; use o prompt para estruturar o que você quer ver no output final.

> [!warning] Confidence levels em modelos clássicos são mal-calibrados
> Pedir "use confidence levels (high/medium/low)" funciona em qualquer modelo — mas em modelos clássicos sem reasoning interno, a calibração é pobre: eles tendem a marcar quase tudo como "high confidence" independente da real incerteza. Reasoning models calibram melhor porque a fase de thinking produz incerteza real — o modelo "sabe o que não sabe" de forma mais confiável depois de raciocinar. Se você depende de confidence levels para decisões, use reasoning models.

## Quando ainda pedir step-by-step

Algumas situações justificam CoT explícito mesmo em modelos clássicos não-reasoning:

- **Aritmética complexa em modelo não-reasoning.** Pedir cadeia ainda ajuda.
- **Raciocínio multi-step com input que exige decomposição visível.** Quando você quer auditar o passo, não só a conclusão.
- **Few-shot com exemplos de CoT.** Demonstrar a cadeia em exemplos ainda ensina o padrão.

Em reasoning models, nenhuma dessas se aplica — o modelo já faz internamente.

## Quando usar reasoning models vs clássicos

Reasoning models são mais caros — thinking tokens custam 1-4x mais que output tokens em alguns provedores. A questão é quando o custo se justifica:

**Usar reasoning models quando:**
- A tarefa exige múltiplos passos de dedução ou verificação.
- Erros são caros: análise jurídica, debugging de código crítico, raciocínio médico.
- Calibração de incerteza importa: você precisa saber o que o modelo não sabe.
- Problemas de matemática, lógica, planejamento ou código complexo.

**Não usar reasoning models quando:**
- A tarefa é geração de texto simples: sumário, tradução, formatação.
- Você precisa de latência baixa: thinking adiciona latência.
- Volume alto com custo sensível: 10.000 chamadas/dia com thinking caro.
- A resposta é factual e o modelo clássico já acerta.

A heurística: se um humano especialista resolveria o problema em 2 minutos de reflexão intensa, reasoning model provavelmente vale. Se é execução direta de uma tarefa bem-definida, clássico basta.

## O budget de tokens de thinking

Em reasoning models com thinking configurável, o orçamento de tokens de thinking é um parâmetro de qualidade:

```
# Claude extended thinking
client.messages.create(
  model="claude-opus-4-5",
  thinking={
    "type": "enabled",
    "budget_tokens": 10000  # mais tokens = mais profundidade
  },
  ...
)

# o3 (via API OpenAI)
client.chat.completions.create(
  model="o3",
  reasoning_effort="high",  # low / medium / high
  ...
)
```

Mais tokens de thinking = melhor qualidade em problemas difíceis, mas mais latência e custo. A calibração empírica:

| Complexidade do problema | reasoning_effort recomendado | thinking budget indicativo |
|---|---|---|
| Simples (formatação, resumo) | low / não usar | não usar |
| Médio (análise, debugging básico) | medium | 4k-8k tokens |
| Complexo (prova, arquitetura) | high | 16k-32k tokens |
| Expert (ciência, lógica formal) | max | 32k+ tokens |

## Como ler e usar o audit trail

O audit trail não é só output cosmético — é uma ferramenta de verificação. Como usá-lo:

**Assumptions:** leia antes de aceitar a resposta. Se o modelo assumiu algo errado sobre o contexto (interpretou um termo de forma diferente, assumiu um constraint que não existe), a resposta pode ser tecnicamente correta mas errada para o seu caso. Assumptions incorretos são o sinal mais fácil de detectar.

**Key checkpoints:** úteis para debugging de resposta incorreta. Se a resposta final está errada, trace de volta pelo checkpoint onde o raciocínio divergiu. Isso transforma "a resposta está errada" em "o raciocínio errou neste ponto específico" — muito mais acionável para a iteração.

**Uncertainties com confidence levels:** filtre ação pelo nível de confiança. Resposta com "low confidence" na afirmação central precisa de verificação externa antes de virar decisão. Resposta com "high confidence" pode ser aceita com menos scrutiny.

**How to verify:** use antes de aceitar afirmações numéricas ou empíricas. Se o modelo diz "verifique na RFC 7231", faça isso. Audit trail sem verificação é melhor que nada mas é ainda um input, não uma conclusão.

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

## Evolução e futuro

O campo de reasoning models evolui rápido. Alguns padrões que estavam estabilizando em 2025-2026:

- **Thinking interleaved:** modelos que alternam output e thinking em tempo real (Claude streaming thinking). O usuário vê o pensamento acontecer. O prompt ainda segue os princípios de audit trail — você pede estrutura no output final, não no stream de thinking.
- **Agentic reasoning:** em loops agênticos, reasoning models são usados para planejamento (qué fazer) e modelos clássicos para execução (fazer). A divisão reduz custo sem sacrificar qualidade de plano.
- **Thinking budget adaptativo:** modelos que alocam mais tokens de thinking automaticamente para perguntas mais difíceis, sem configuração manual. A tendência é de menos controle via parâmetro e mais controle via prompt de meta-instrução.
- **Hybrid prompting:** alguns provedores permitem o modelo escolher entre modo thinking e modo rápido por turno, baseado na dificuldade percebida. Você instrui o comportamento de seleção, não o comportamento de cada turno.

O princípio estável: **não peça ao modelo pra raciocinar — peça o audit do raciocínio**. Esse princípio sobrevive a qualquer mudança de arquitetura interna.

## Checklist: prompting de reasoning model

Antes de usar um reasoning model em produção, passe por esse checklist:

- [ ] Identifiquei se o modelo é reasoning ou clássico?
- [ ] Removi pedidos de CoT explícito ("think step-by-step") do prompt?
- [ ] Adicionei estrutura de audit trail no output format (assumptions, checkpoints, uncertainties, how to verify)?
- [ ] Configurei o thinking budget pelo parâmetro da API, não pelo prompt?
- [ ] Avaliei se o custo de thinking é justificado pela complexidade da tarefa?
- [ ] Planejei como usar os confidence levels para filtrar ação vs verificação extra?

## Como explicar em inglês

Em entrevistas de engenharia de IA em 2025-2026, "Como você prompta reasoning models diferente de modelos clássicos?" é uma das perguntas que distingue quem trabalha com IA em produção de quem só consumiu tutoriais. Essa pergunta aparece tanto em entrevistas de engenharia de prompt quanto em design reviews de sistemas de IA. Uma resposta sólida:

> "The fundamental shift is that reasoning models run their chain-of-thought internally before producing output. So instead of prompting for the reasoning process — 'think step-by-step' — you prompt for the audit trail: assumptions the model made, key inflection points in its reasoning, uncertainties with confidence levels, and how to independently verify the answer. You're asking for metadata about the inference, not the inference itself. And thinking depth is a parameter — budget_tokens or reasoning_effort — not a prompt instruction."

| Português | Inglês |
|-----------|--------|
| modelo de raciocínio | reasoning model |
| cadeia de pensamento | chain-of-thought (CoT) |
| pensamento interno | internal thinking / scratchpad |
| trilha de auditoria | audit trail |
| ponto de inflexão | reasoning checkpoint / inflection point |
| premissa adotada | assumption |
| nível de confiança | confidence level |
| incerteza calibrada | calibrated uncertainty |
| esforço de raciocínio | reasoning effort (parâmetro da API) |
| modelo clássico vs. reasoning | classic model vs. reasoning model |

## O que vem a seguir

Com o toolkit de prompting coberto — especificidade, role, constraints, few-shot, iteração, e reasoning models — a última nota fecha o galho com o negativo: os anti-patterns e tells que deixam claro que um output saiu de um modelo sem supervisão adequada.

Ver [[09 - Anti-patterns e tells de IA — o que evitar]].

## Fontes

- **@hooeem** — *Become an AI Engineer*, cap #5. Origem do framing "audit trail, não chain-of-thought".
- **OpenAI** — *Reasoning best practices* (docs OpenAI para o-series).
- **DeepSeek** — *R1 technical report* (2025).
- **Anthropic** — *Extended thinking* (docs.anthropic.com/extended-thinking).
- **Wei et al.** — *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models* ([arxiv:2201.11903](https://arxiv.org/abs/2201.11903), 2022). Paper original de CoT em modelos clássicos.

## Veja também

- [[03-Dominios/Tecnologia/IA/Anatomia dos LLMs/15 - Reasoning models e chain-of-thought|Anatomia — Reasoning models e chain-of-thought]] — o "porquê" por trás desta nota, em profundidade
- [[04 - O mega-prompt do Karpathy — anatomia da anti-sycophancy]] — cláusula step-by-step a revisar em reasoning models
- [[06 - Constraints declarativas — boundaries como engenharia]] — onde audit trail vira constraint de output
- [[03-Dominios/Tecnologia/IA/Context Engineering/15 - Técnicas de prompting — zero-shot, few-shot, CoT, ToT|Context Engineering — Técnicas de prompting]] — CoT na taxonomia maior
