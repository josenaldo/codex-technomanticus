---
title: "Prompt Layer"
created: 2026-05-28
updated: 2026-05-28
type: concept
status: seedling
progress: in_progress
tags:
  - ai-engineering-stack
  - ia
  - prompt
publish: true
aliases:
  - Prompt Layer
  - Camada de prompt
---

# Prompt Layer

> [!abstract] TL;DR
> A Prompt Layer define **como o modelo deve se comportar** — não o que ele sabe (isso é Context Layer), nem o que ele entrega (isso é Output Layer). Aqui ficam role, primary job, padrões obrigatórios, ações permitidas, ações proibidas, comportamento sob incerteza, estilo de raciocínio. É o [[Dicionário de IA#system prompt|system prompt]] tratado como artefato versionado, não como bloco de texto improvisado. Quando bem feita, a Prompt Layer transforma o modelo num executor com persona estável; quando mal feita, o sistema é instável a cada mudança de input.

## O que é esta camada

A Prompt Layer materializa **comportamento desejado** em texto. É o lugar onde você converte "queremos um assistente cuidadoso e direto" em instruções que o modelo segue de forma reprodutível.

O template mínimo (adaptado do thread @hooeem):

```yaml
role: <quem o modelo é nesta interação>
primary_job: <herda do Purpose Layer>
primary_standard: <o critério principal pelo qual o modelo se autoavalia>
allowed_actions:
  - <ação 1>
  - <ação 2>
forbidden_actions:
  - <proibição 1>
  - <proibição 2>
uncertainty_behavior: <o que fazer quando não sabe>
reasoning_style: <conciso, exploratório, step-by-step, ...>
```

Note que **forbidden_actions na Prompt Layer não substitui Guardrail Layer**. Prompt Layer pede comportamento; Guardrail Layer **impõe** comportamento por código fora do modelo. As duas trabalham juntas — ver [[10 - Guardrail Layer]].

## Decisões-chave

1. **Role específico vs genérico.** "Você é um assistente útil" é zero informação. "Você é editor sênior de uma revista de tecnologia que prioriza clareza e ceticismo" molda decisões reais.

2. **Tom do `uncertainty_behavior`.** Três comportamentos comuns: (a) *ask back* — pede esclarecimento; (b) *flag and proceed* — segue com aviso de baixa confiança; (c) *stop and escalate* — recusa e pede humano. A escolha define UX inteira.

3. **Tamanho do system prompt.** Prompt longo gasta tokens em **todo** request ([[03-Dominios/Tecnologia/IA/Anatomia dos LLMs/06 - A janela de contexto|janela de contexto]] mais cheia, custo a cada chamada). Use [[Dicionário de IA#Prompt caching|prompt caching]] quando disponível; ainda assim, prune o que não muda comportamento.

4. **Few-shot vs zero-shot.** Adicionar 2-3 exemplos no system prompt geralmente sobe qualidade mais do que reescrever instruções. Custa tokens, mas é a alavanca de melhor ROI quando o modelo "quase acerta".

5. **Versionamento.** Trate o system prompt como código: arquivo separado, diff no PR, número de versão. A nota [[11 - Logging Layer]] precisa registrar qual versão rodou em cada chamada.

## Onde aprofundar no Codex

- **[[Prompt Engineering]]** — trilha-irmã dedicada a técnicas (CoT, few-shot, ToT, role prompting). Em construção.
- **[[03-Dominios/Tecnologia/IA/Context Engineering/01 - De prompt engineering a context engineering|De prompt engineering a context engineering]]** — onde a Prompt Layer se posiciona no panorama maior.
- **[[Dicionário de IA#prompt engineering|Dicionário: prompt engineering]]**.

## Veja também

- [[02 - Purpose Layer — o que o sistema é]] — `primary_job` desta camada vem de lá
- [[04 - Context Layer]] — separa conhecimento do sistema (lá) de comportamento (aqui)
- [[10 - Guardrail Layer]] — `forbidden_actions` aqui é aspiracional; lá é imposto

## Fontes

- **@hooeem** — *Become an AI Engineer*, chapter #18, Step 2 (Prompt layer template).
- **Anthropic** — [*Prompt engineering overview*](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview). Estrutura recomendada de system prompt.
- **OpenAI** — [*Prompt engineering guide*](https://platform.openai.com/docs/guides/prompt-engineering).
