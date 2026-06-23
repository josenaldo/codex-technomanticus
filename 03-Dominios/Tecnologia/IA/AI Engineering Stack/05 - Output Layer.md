---
title: "Output Layer"
created: 2026-05-28
updated: 2026-05-28
type: concept
status: seedling
progress: in_progress
tags:
  - ai-engineering-stack
  - ia
  - output
publish: true
aliases:
  - Output Layer
  - Camada de saída
---

# Output Layer

> [!abstract] TL;DR
> A Output Layer define **em que formato o modelo entrega**. Não é detalhe de UI — é decisão arquitetural. Markdown? Tabela? Checklist? JSON validado por schema? Quais seções são obrigatórias, qual o nível de confiança esperado, quando o modelo sinaliza incerteza, como o output já vira ação. Sistemas que pulam essa camada produzem texto bonito mas inintegrável. Sistemas que tratam Output Layer como contrato conseguem encadear pipelines determinísticos.

## O que é esta camada

A Output Layer é o **contrato de saída** do sistema. Define o que sai, em qual estrutura, com quais campos obrigatórios. Quando o output é consumido por outro sistema (próximo passo do pipeline, dashboard, API), Output Layer vira [[Dicionário de IA#structured output|structured output]] tipado.

Template mínimo (adaptado do thread @hooeem):

```yaml
primary_format: <markdown | tabela | checklist | JSON | XML>
required_sections:
  - <seção 1>
  - <seção 2>
confidence_level: <obrigatório? escala? livre?>
uncertainty_flags: <como o modelo sinaliza incerteza>
actionability: <output como ação direta vs sugestão vs análise>
```

Para output não-trivial consumido por código, vale formalizar via JSON Schema, Pydantic ou TypeScript types. Modelos de fronteira (GPT-4o, Claude, Gemini) suportam **structured outputs** que **garantem** aderência ao schema.

## Decisões-chave

1. **Markdown vs JSON.** Markdown pra leitura humana; JSON pra consumo por código. Misturar (JSON dentro de markdown em ```json) é tentador mas frágil — parser pode quebrar e o modelo pode escapar mal. Quando o output vai pra pipeline, vá direto pra JSON estrito.

2. **Schema rígido vs leve.** Schema rígido (campos obrigatórios, tipos validados) reduz alucinação de campos mas penaliza quando o modelo quer flagar caso fora do esperado. Leve (alguns required, muitos optional) dá flexibilidade mas exige validação pós-hoc.

3. **Confidence como campo obrigatório.** Forçar o modelo a emitir confidence (`high|medium|low` ou 0-1) muda comportamento — ele se calibra. Útil pra Guardrail Layer rotear pra revisão humana abaixo de threshold.

4. **Uncertainty flags explícitos.** Campos como `assumptions`, `missing_data`, `caveats` deixam o modelo "guardar incerteza num lugar nomeado". Sem eles, incerteza vira hedge prosaico ("pode ser que...").

5. **Actionability.** Output que **é** ação (uma chamada de função) tem latência mais baixa e menos risco de interpretação. Output que **sugere** ação preserva humano-no-loop. Escolher um lado por tarefa.

## Onde aprofundar no Codex

- **[[Structured Outputs]]** — trilha-irmã sobre schemas, Pydantic, structured outputs nas APIs (em construção).
- **[[Dicionário de IA#structured output|Dicionário: structured output]]**.
- **[[Dicionário de IA#function calling|Dicionário: function calling]]** — relação entre tool call e structured output.

## Veja também

- [[03 - Prompt Layer]] — comportamento que produz o output
- [[04 - Context Layer]] — conhecimento que alimenta o output
- [[09 - Evaluation Layer]] — rubrica aplica em cima do que sai aqui

## Fontes

- **@hooeem** — *Become an AI Engineer*, chapter #18, Step 4 (Output layer template).
- **OpenAI** — [*Structured Outputs guide*](https://platform.openai.com/docs/guides/structured-outputs). Schema enforcement na API.
- **Anthropic** — [*Tool use with Claude*](https://docs.anthropic.com/en/docs/build-with-claude/tool-use/overview). JSON schema em tool calls.
