---
title: "07 - Iteration patterns — keep, change, do-not"
created: 2026-05-28
updated: 2026-05-28
type: concept
status: seedling
progress: in_progress
tags:
  - prompt-engineering
  - ia
  - iteration
publish: true
aliases:
  - Iteration prompt
  - Keep change do-not
  - Refining prompts
---

# 07 - Iteration patterns — keep, change, do-not

> [!abstract] TL;DR
> O modo errado de iterar um output é dizer *"try again, make it better"* — o modelo regenera às cegas, frequentemente piorando o que estava bom. O modo certo é nomear três conjuntos: **Keep** (o que estava certo e não pode mudar), **Change** (o que precisa virar X), **Do not** (o que apareceu no output anterior e não pode reaparecer). Esta nota cobre o template, quando iterar vs quando recomeçar do zero, e o sinal mais importante de que sua iteração está doente: loop infinito porque o primeiro prompt não era específico.

## O anti-pattern: "try again, make it better"

```
RUIM:
[output 1]
> "Try again, make it better."
[output 2 — pior em algum lugar, melhor em outro]
> "No, like the first but better."
[output 3 — agora misturando os dois e perdendo coisas]
```

O modelo não tem como saber o que estava bom no output anterior. Sem ancoragem, ele regenera **tudo** — incluindo o que estava certo. Resultado: melhora local em uma dimensão, regressão em outra. A entropia do output sobe a cada rodada.

A causa: o modelo trata cada turno como uma nova geração, não como um diff sobre a anterior. Você precisa explicitar o diff.

## O template Keep / Change / Do not

```
[output anterior está acima]

Keep:
- <coisa específica do output anterior que está certa>
- <coisa específica do output anterior que está certa>

Change:
- <dimensão A: de X para Y>
- <dimensão B: de X para Y>

Do not:
- <padrão que apareceu e não deve reaparecer>
- <padrão que apareceu e não deve reaparecer>
```

Três regras:

1. **Keep deve ser concreto.** Não "o tom geral" — sim "o segundo parágrafo, com a estatística sobre X". Quanto mais ancorado em trecho específico, melhor.
2. **Change deve ter direção.** Não "menos formal" — sim "menos formal, no mesmo registro do exemplo do mestre [[Andrej Karpathy]]" ou "menos formal: cortar 'Caro leitor' e abrir com afirmação". A mudança precisa apontar pra onde vai.
3. **Do not deve nomear o sintoma.** O ponto de "Do not" é bloquear especificamente o que apareceu e atrapalhou: "Não usar 'em conclusão'", "Não retomar a frase 'fast-paced world'".

### Exemplo

```
[output 1: artigo de 600 palavras]

Keep:
- A abertura com a estatística sobre custo (primeiro parágrafo)
- A tabela de comparação (terceira seção)
- O fechamento citando o paper de 2024

Change:
- Tom: de "consultoria" para "engenheiro com 15 anos de campo".
  Modelo: prosa do Karpathy nos posts dele.
- Tamanho: de 600 para 350 palavras

Do not:
- Não usar "in today's fast-paced world"
- Não fechar com call to action genérico
- Não reintroduzir disclaimers sobre limitações
```

A iteração 2 entrega algo utilizável. Sem o template, a iteração 2 frequentemente piora a tabela (que estava certa) e mantém o tom de consultoria (que era o problema).

## Quando iterar vs quando recomeçar

Iteração não é sempre a resposta. Quatro sinais de que recomeçar do zero é mais barato:

1. **Você está na terceira iteração e ainda não está perto.** Cada iteração adiciona ruído acumulado da história de conversa. Reset com prompt melhor.
2. **O Keep está vazio.** Se nada do output anterior vale a pena preservar, não está iterando — está produzindo do zero com prompt poluído pelo contexto anterior.
3. **As mudanças são estruturais, não locais.** "Quero outro gênero" não é iteração; é nova tarefa.
4. **O modelo perdeu o fio.** Se a iteração introduziu contradições com instruções anteriores, frequentemente é mais limpo recomeçar do que tentar des-instruir.

A regra prática: **se a segunda iteração ainda não chegou, a terceira raramente chega.** Volte ao prompt original, aplique o aprendizado de "o que estava faltando", e dispare de novo.

## O sinal mais importante: por que você está iterando?

A pergunta de calibração mais útil é: *"Por que precisei iterar?"*

| Por que iterou | Diagnóstico |
|---|---|
| Output ficou no formato errado | Constraint de output ausente no prompt original. Adicione ao próximo. |
| Tom não bateu | Role e style constraints fracas. Reforce no próximo. |
| Resposta foi superficial | Tarefa pediu mas não especificou profundidade ou audiência. Adicione. |
| Modelo inventou fatos | Sem evidence constraint. Adicione "se não sabe, diga". |
| Output veio com clichês | Sem Do-not list pra anti-patterns. Adicione (ver [[09 - Anti-patterns e tells de IA — o que evitar\|nota 09]]). |

Iterar é normal. Iterar repetidamente pela mesma razão é sinal de prompt sub-especificado. Use cada iteração pra alimentar o prompt seguinte.

## Pitfall: iteração infinita por baixa especificidade

O loop tóxico mais comum:

```
Iteração 1: prompt vago → output médio
Iteração 2: "make it more X" → output deslizado em direção X, perdendo Y
Iteração 3: "now bring Y back" → output ping-pong
Iteração 4: "balance both" → output médio (de novo)
```

O modelo está obedecendo. O prompt é que não tem alvo. Sintoma: depois de 3 iterações, você não está mais perto do que queria do que estava na iteração 1.

A saída: pare. Reescreva o prompt original com todas as constraints que você descobriu nas iterações. Dispare uma única vez. Você não está iterando — está descobrindo o prompt que deveria ter escrito de início.

## Pitfall: Keep como confirmação de tom

```
RUIM:
Keep: o tom geral.

(o modelo não sabe que tom, e vai regenerar achando que sabe)
```

"Tom geral" é abstração que o modelo preencher do prior. Em vez disso, cite o trecho concreto onde o tom apareceu certo, ou descreva o tom por adjetivos verificáveis. Keep abstrato é Keep vazio.

## Pitfall: Change sem direção

```
RUIM:
Change: melhor.

(o modelo regenera de novo, do zero — sem saber o que "melhor" quer dizer)
```

Change precisa de **vetor**: de onde, para onde. Sem vetor, vira "try again, make it better" reformulado.

## Quando iteração é a alavanca certa

Iteração funciona melhor quando:

- **A maior parte do output está certa**, e você quer ajustar 1-2 dimensões específicas.
- **As dimensões a mudar são locais** (um parágrafo, o título, a tabela).
- **Você consegue nomear o sintoma** que apareceu e quer bloquear.
- **O custo de regenerar tudo é alto** (output longo, computação cara).

Se nenhuma dessas vale, recomeçar do zero com prompt melhor é provavelmente mais rápido.

## Fontes

- **@hooeem** — *Become an AI Engineer*, cap #7. Origem do template Keep/Change/Do-not.
- **Anthropic** — *Iterating on prompts* (docs.anthropic.com).
- **OpenAI** — *Prompt engineering guide*, seção sobre iteration.

## Veja também

- [[02 - Especificidade — a primeira disciplina]] — iteração compulsiva geralmente é sintoma de prompt vago de partida
- [[06 - Constraints declarativas — boundaries como engenharia]] — Do-not é uma constraint declarativa em escala micro
- [[09 - Anti-patterns e tells de IA — o que evitar]] — o catálogo do que costuma ir no Do-not
