---
title: "Structured Outputs"
type: moc
publish: true
tags:
  - structured-outputs
  - ia
  - moc
created: 2026-05-28
updated: 2026-05-28
aliases:
  - Saídas Estruturadas
  - JSON mode
---

# Structured Outputs

LLMs são **funções estocásticas com saída não tipada** — structured outputs é como você recria contrato de tipo na borda. A frase é a tese que organiza este vault (ver [[03-Dominios/IA/index|Formação Engenheiro de IA]]): o modelo é uma dependência cujo retorno é texto livre, e qualquer pipeline sério precisa transformar esse texto num objeto validável antes do próximo passo. Esta trilha cobre as três camadas dessa disciplina: o problema (por que "pedir JSON no prompt" não basta), os mecanismos (JSON Schema, function calling, structured outputs por provider), e a robustez (validação semântica, retry, streaming).

> [!info] Pré-requisitos
> [[Anatomia dos LLMs/09 - APIs de LLM — anatomia de uma chamada|09 - APIs de LLM — anatomia de uma chamada]] é suficiente. Familiaridade com [[Prompt Engineering]] ajuda a entender por que prompt sozinho não resolve, mas não é obrigatória.

> [!warning] Provider guarante shape, não semântica
> Mesmo com strict mode da OpenAI, tool use da Anthropic, ou response schema do Gemini, a garantia é que o JSON tem os campos certos com os tipos certos. **O conteúdo dos campos** (um `email` realmente ser um email, um `cnpj` ter dígito verificador válido) segue sendo seu problema. Notas 07-08 tratam disso.

## Comece por aqui

Trilha sequencial recomendada — do problema ao mecanismo, do mecanismo à robustez.

### Bloco 1 — Fundamentos (2 notas)

Por que o output não estruturado é um problema técnico, e qual é a linguagem padrão pra resolver.

- [[01 - O problema do output não estruturado]] — markdown wrapper, campos faltando, chaves alucinadas, e por que pedir JSON via prompt não basta
- [[02 - JSON Schema como contrato]] — JSON Schema 101, o schema canônico do @hooeem (answer/confidence/assumptions/risks/next_steps), patterns e quando schema é overkill

### Bloco 2 — Mecanismos (4 notas)

Como o output estruturado é forçado na prática — o flip conceitual de function calling, e as implementações por provider.

- [[03 - Function calling como mecanismo de output]] — o flip: tool use não é só pra agentes, é o mecanismo mais confiável de forçar formato
- [[04 - OpenAI Structured Outputs — strict mode]] — `response_format`, strict mode, `parse()` com Pydantic, restrições do strict
- [[05 - Anthropic tool use para forçar formato]] — single tool + `tool_choice` forçado, por que Anthropic não tem API dedicada de structured output
- [[06 - Gemini structured output]] — `response_mime_type` + `response_schema`, subset de OpenAPI 3.0, diferenças vs OpenAI

### Bloco 3 — Robustez (2 notas)

O que fazer quando o shape está certo mas o conteúdo não, e como lidar com output parcial.

- [[07 - Validação e retry — Pydantic, Zod]] — shape vs semântica, validadores customizados, retry-with-feedback, backoff, fallback
- [[08 - Streaming de structured outputs]] — partial JSON parsers, streaming nativo de tool use, quando faz sentido streamar structured

## Rotas alternativas

### Rota mínima (preciso resolver hoje)

*"Output do meu LLM não está parseando — me dê o essencial"*

[[01 - O problema do output não estruturado]] → [[02 - JSON Schema como contrato]] → [[04 - OpenAI Structured Outputs — strict mode]] ou [[05 - Anthropic tool use para forçar formato]] → [[07 - Validação e retry — Pydantic, Zod]]

### Rota arquitetura (estou desenhando pipeline)

*"Quero entender os mecanismos antes de escolher provider"*

[[02 - JSON Schema como contrato]] → [[03 - Function calling como mecanismo de output]] → [[04 - OpenAI Structured Outputs — strict mode]] → [[05 - Anthropic tool use para forçar formato]] → [[06 - Gemini structured output]] → [[07 - Validação e retry — Pydantic, Zod]]

### Rota provider único (já escolhi stack)

*"Trabalho só com OpenAI / Anthropic / Gemini"*

[[02 - JSON Schema como contrato]] → nota do provider correspondente (04, 05 ou 06) → [[07 - Validação e retry — Pydantic, Zod]] → [[08 - Streaming de structured outputs]]

### Rota streaming UI (UX em chat / canvas)

*"Quero estruturar output mas mostrar enquanto sai"*

[[02 - JSON Schema como contrato]] → [[05 - Anthropic tool use para forçar formato]] → [[08 - Streaming de structured outputs]] → [[07 - Validação e retry — Pydantic, Zod]]

## Leituras recomendadas

| Fonte | Tipo | Cobertura |
|-------|------|-----------|
| **@hooeem** — *Become an AI Engineer*, caps #6 e #11 | Thread / artigo | Notas 01-03 (espinha dorsal conceitual) |
| **OpenAI** — *Structured Outputs guide* ([docs](https://platform.openai.com/docs/guides/structured-outputs)) | Doc oficial | Nota 04 |
| **Anthropic** — *Tool use overview* ([docs](https://docs.anthropic.com/en/docs/build-with-claude/tool-use/overview)) | Doc oficial | Notas 03 e 05 |
| **Google** — *Gemini API — Structured output* ([docs](https://ai.google.dev/gemini-api/docs/structured-output)) | Doc oficial | Nota 06 |
| **JSON Schema spec** ([json-schema.org](https://json-schema.org/)) | Spec | Nota 02 |
| **Eugene Yan** — *Patterns for LLM Systems* ([eugeneyan.com](https://eugeneyan.com/writing/llm-patterns/)) | Artigo | Notas 01, 07 — guardrails e validação |
| **Pydantic** — *Validators docs* | Doc oficial | Nota 07 |
| **Zod** — *Refinements docs* | Doc oficial | Nota 07 |

## Veja também

- [[AI Engineering Stack]] — onde esta trilha se encaixa (Output Layer é a camada referente)
- [[AI Engineering Stack/05 - Output Layer|AI Engineering Stack — Output Layer]] — a camada que cita esta trilha em "Onde aprofundar"
- [[Prompt Engineering]] — prompt pode sugerir formato; structured output o **enforça**
- [[Anatomia dos LLMs]] — pré-requisito conceitual, especialmente nota 09 sobre APIs
- [[Segurança e Guardrails]] — output validado é a base para validar com cuidado o que o LLM produziu

## Todas as notas

```dataview
LIST
FROM "03-Dominios/IA/Structured Outputs"
WHERE type != "moc"
SORT file.name ASC
```
