---
title: "05 - Anthropic tool use para forçar formato"
created: 2026-05-28
updated: 2026-05-28
type: concept
status: seedling
progress: in_progress
tags:
  - structured-outputs
  - ia
  - anthropic
publish: true
aliases:
  - Anthropic tool use forçado
  - Claude structured output
---

# 05 - Anthropic tool use para forçar formato

> [!abstract] TL;DR
> Anthropic não tem API dedicada de structured output equivalente ao `response_format` da OpenAI ou ao `response_schema` do Gemini. O mecanismo canônico é **tool use forçado**: defina uma tool cujo `input_schema` é seu output, force a chamada via `tool_choice: { type: "tool", name: "..." }`, extraia o `input` do bloco `tool_use`. Funciona em Claude 3.5+, Claude 4.x. Aderência altíssima — Anthropic treina pesadamente em tool use desde Claude 3, e tool_choice forçado tira a possibilidade de "responder em texto livre". Custo: poucos tokens de overhead, pequena latência. Trade-off principal: schema é JSON Schema, mas Anthropic não usa constrained decoding como OpenAI strict — confiabilidade é alta mas não 100% garantida arquiteturalmente.

## A diferença de filosofia

OpenAI e Google escolheram criar APIs dedicadas pra structured output. Anthropic escolheu unificar tool use e structured output sob a mesma primitiva:

> *"A tool é o mecanismo. Se você quer só output estruturado, defina uma tool que não executa nada — só recebe os campos. Force a chamada."*

Vantagens dessa abordagem:

- **Uma única API pra aprender** — quem sabe tool use sabe structured output.
- **Compõe naturalmente com agentes** — pipeline com tools reais + tool de finalização é trivial.
- **Schema é JSON Schema completo** — sem subset arbitrário como strict mode.

Desvantagem: aderência depende do treino do modelo, não de constrained decoding. Em Claude 4.x isso é muito alto em benchmarks comunitários e observação prática, mas não é 100% garantido por arquitetura. Sua aplicação ainda deve validar (ver [nota 07](07%20-%20Validação%20e%20retry%20—%20Pydantic,%20Zod.md)) e fazer retry quando algo escapar.

## O padrão — Python SDK

```python
from anthropic import Anthropic

client = Anthropic()

analysis_tool = {
    "name": "record_analysis",
    "description": (
        "Registra a análise estruturada da pergunta do usuário. "
        "Esta é a única forma válida de responder."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "answer": {
                "type": "string",
                "description": "Resposta direta à pergunta."
            },
            "confidence": {
                "type": "string",
                "enum": ["low", "medium", "high"],
                "description": "Confiança do modelo na resposta."
            },
            "assumptions": {
                "type": "array",
                "items": { "type": "string" },
                "description": "Premissas assumidas."
            },
            "risks": {
                "type": "array",
                "items": { "type": "string" },
                "description": "Riscos ou caveats."
            },
            "next_steps": {
                "type": "array",
                "items": { "type": "string" },
                "description": "Próximos passos sugeridos."
            }
        },
        "required": ["answer", "confidence", "assumptions", "risks", "next_steps"]
    }
}

response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    tools=[analysis_tool],
    tool_choice={"type": "tool", "name": "record_analysis"},
    messages=[
        {"role": "user", "content": "Devo migrar de Postgres pra Mongo?"}
    ]
)

# Extrai o output estruturado
structured_output = None
for block in response.content:
    if block.type == "tool_use" and block.name == "record_analysis":
        structured_output = block.input
        break

if structured_output is None:
    raise RuntimeError("Modelo não chamou a tool — investigar")

# structured_output é dict: {"answer": "...", "confidence": "high", ...}
```

`tool_choice: { type: "tool", name: "..." }` é o que força. Sem isso, o modelo pode decidir responder em texto. Com isso, o `stop_reason` será `tool_use` e o `content` terá pelo menos um bloco `tool_use` com a tool nomeada.

## O padrão — TypeScript SDK

```typescript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const analysisTool = {
  name: "record_analysis",
  description:
    "Registra a análise estruturada da pergunta do usuário. " +
    "Esta é a única forma válida de responder.",
  input_schema: {
    type: "object" as const,
    properties: {
      answer: { type: "string" },
      confidence: {
        type: "string",
        enum: ["low", "medium", "high"],
      },
      assumptions: { type: "array", items: { type: "string" } },
      risks: { type: "array", items: { type: "string" } },
      next_steps: { type: "array", items: { type: "string" } },
    },
    required: ["answer", "confidence", "assumptions", "risks", "next_steps"],
  },
};

const response = await client.messages.create({
  model: "claude-sonnet-4-5",
  max_tokens: 1024,
  tools: [analysisTool],
  tool_choice: { type: "tool", name: "record_analysis" },
  messages: [
    { role: "user", content: "Devo migrar de Postgres pra Mongo?" },
  ],
});

const toolUse = response.content.find(
  (block) => block.type === "tool_use" && block.name === "record_analysis"
);

if (!toolUse || toolUse.type !== "tool_use") {
  throw new Error("Modelo não chamou a tool");
}

const structuredOutput = toolUse.input as {
  answer: string;
  confidence: "low" | "medium" | "high";
  assumptions: string[];
  risks: string[];
  next_steps: string[];
};
```

## Aderência e confiabilidade

Sem constrained decoding, a aderência depende do modelo. Observações empíricas (2026):

- **Claude 4.x (Sonnet, Opus, Haiku)** — aderência muito alta em schemas razoáveis na prática. Falhas tendem a ser em schemas muito complexos ou descrições conflitantes.
- **Claude 3.5 Sonnet** — bom, mas com mais variação em schemas grandes (>30 campos).
- **Claude 3 Opus / Sonnet (legados)** — funciona, com aderência menor em schemas com muitos enums simultâneos.

Modos de falha típicos quando ocorrem:

- **Stop reason `end_turn` em vez de `tool_use`** — modelo respondeu em texto livre (ignorou `tool_choice`). Raro em Claude 4, mas possível com prompts muito conflitantes.
- **Tool chamada com campo extra** — não suportado em strict OpenAI, mas pode acontecer em Anthropic. Validar.
- **Tipo errado em campo** — string onde devia ser number, principalmente em campos `description` ambíguos. Validador semântico pega.

Heurística: trate tool use como **altamente confiável mas não garantido**. Tenha validação + retry-with-feedback em produção.

## `tool_choice` opções

| Valor | Comportamento |
|---|---|
| `{ "type": "auto" }` | Modelo decide se chama tool ou responde em texto. Default. |
| `{ "type": "any" }` | Modelo **tem** que chamar alguma tool (qualquer uma da lista). Útil quando você tem tools alternativas. |
| `{ "type": "tool", "name": "..." }` | Modelo **tem** que chamar essa tool específica. Único modo certo pra structured output single-purpose. |
| `{ "type": "none" }` | Modelo não pode chamar tools (anula a lista). Pra usar tool_choice condicional. |

Pra structured output, sempre `{ "type": "tool", "name": "..." }`. As outras opções são pra agentes.

## Modelos compatíveis (2026)

Tool use forçado funciona em:

- **Claude 3 família** — Opus, Sonnet, Haiku.
- **Claude 3.5 família** — Sonnet (incluindo `claude-3-5-sonnet-20241022`).
- **Claude 4 família** — Sonnet, Opus, Haiku (todos suportam plenamente).
- **Claude 4.5 família** — Sonnet (`claude-sonnet-4-5`), Haiku, e a linha de Opus 4.x.

Anthropic aceita dois estilos de model ID: o **alias semântico** (`claude-sonnet-4-5`) sempre aponta pra versão atual da família, e o **alias datado/pinado** (`claude-sonnet-4-5-20250929`, `claude-3-5-sonnet-20241022`) fixa um snapshot pra reprodutibilidade em produção. Use o datado quando precisar de comportamento estável e versionado.

Não suportado em modelos descontinuados (Claude 2, Claude Instant).

## Boas práticas Anthropic

### `description` na tool e nos campos

Anthropic enfatiza descrições. O modelo lê a `description` da tool como instrução. Inclua "Esta é a única forma válida de responder" ou similar pra reforçar que outras vias não estão disponíveis.

### Tool name semântico

`record_analysis`, `extract_invoice`, `classify_ticket` — nomes que descrevem ação. `output`, `result`, `response` são mais fracos — o modelo aceita, mas usa mais contexto de chat-style.

### Não dependa de validação intermediária

Anthropic não valida `pattern`, `minLength`, `format: email` etc. Você precisa validar (ver nota 07).

### Combine com prompt curto

Prompt longo + schema grande compete pela atenção do modelo. Mantenha prompt user-facing curto; deixe a tool description carregar o contrato.

### Cache de prompt + tools

Tools entram no input cacheado quando você usa prompt caching ([[03-Dominios/Tecnologia/IA/Anatomia dos LLMs/13 - Prompt caching e otimizações de API|prompt caching]]). Se a tool é estável, marque o bloco como `cache_control` pra economizar.

## Quando Anthropic é a escolha certa pra structured output

- **Schemas com nested complexo** — Anthropic não tem as restrições do strict mode.
- **Pipeline já tem agentes** — tool é a primitiva nativa.
- **Quer rationale + structured** — modelo pode raciocinar em `text` block antes do `tool_use` block (use `stop_reason` correto).
- **Multi-provider abstração** — tool use é o denominador comum.

Quando OpenAI ou Gemini podem ser melhores:

- **Garantia arquitetural** — strict mode da OpenAI é 100% de shape.
- **Schemas simples + custo mínimo** — `response_format` da OpenAI tem overhead menor que tool use.

## Fontes

- **Anthropic** — *Tool use with Claude* ([docs.anthropic.com/en/docs/build-with-claude/tool-use/overview](https://docs.anthropic.com/en/docs/build-with-claude/tool-use/overview)).
- **Anthropic** — *Forcing tool use* ([docs.anthropic.com/en/docs/build-with-claude/tool-use#forcing-tool-use](https://docs.anthropic.com/en/docs/build-with-claude/tool-use)).
- **Anthropic SDK** — Python e TypeScript exemplos no GitHub.
- **Anthropic** — *JSON mode is tool use* (posicionamento oficial em blog posts e cookbook).

## Veja também

- [[03 - Function calling como mecanismo de output]] — o padrão geral
- [[04 - OpenAI Structured Outputs — strict mode]] — abordagem alternativa
- [[06 - Gemini structured output]] — terceira abordagem
- [[07 - Validação e retry — Pydantic, Zod]] — necessária especialmente em Anthropic (sem constrained decoding)
- [[03-Dominios/Tecnologia/IA/Anatomia de Agents/02 - O loop ReAct e native tool use|Loop ReAct e native tool use]] — o caso geral de tool use
