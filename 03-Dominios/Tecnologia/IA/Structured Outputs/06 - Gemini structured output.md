---
title: "06 - Gemini structured output"
created: 2026-05-28
updated: 2026-05-28
type: concept
status: seedling
progress: in_progress
tags:
  - structured-outputs
  - ia
  - gemini
publish: true
aliases:
  - Gemini response_schema
  - Gemini JSON mode
---

# 06 - Gemini structured output

> [!abstract] TL;DR
> Gemini oferece structured output via dois parâmetros: `response_mime_type: "application/json"` + `response_schema`. O schema usa um **subset de OpenAPI 3.0** (não JSON Schema puro como OpenAI e Anthropic) — diferenças importantes em `enum`, `format`, e união de tipos. Compatível com Gemini 1.5+ (Pro e Flash) e Gemini 2.x (todos). Aderência é alta mas o subset é menor que o de OpenAI strict — schemas com nested deep ou union complexa podem falhar silenciosamente. SDK Python (`google-genai`) tem helper que aceita Pydantic model diretamente. Tool use também funciona como mecanismo alternativo (ver [nota 03](03%20-%20Function%20calling%20como%20mecanismo%20de%20output.md)) com mais flexibilidade.

## O mecanismo

Gemini separa dois parâmetros:

1. **`response_mime_type`** — força o tipo de resposta. Pra JSON estruturado, `"application/json"`. (Também aceita `"text/x.enum"` pra responder apenas com um valor de enum, útil em classificação.)
2. **`response_schema`** — o schema OpenAPI que define a forma.

Sem `response_schema`, com só `response_mime_type: "application/json"`, o modelo tenta retornar JSON livre — sem garantia de shape. Sempre combine os dois.

## Exemplo Python — `google-genai` SDK

```python
from google import genai
from google.genai import types

client = genai.Client(api_key="...")

response_schema = {
    "type": "OBJECT",
    "properties": {
        "answer": { "type": "STRING" },
        "confidence": {
            "type": "STRING",
            "enum": ["low", "medium", "high"]
        },
        "assumptions": {
            "type": "ARRAY",
            "items": { "type": "STRING" }
        },
        "risks": {
            "type": "ARRAY",
            "items": { "type": "STRING" }
        },
        "next_steps": {
            "type": "ARRAY",
            "items": { "type": "STRING" }
        }
    },
    "required": ["answer", "confidence", "assumptions", "risks", "next_steps"],
    "propertyOrdering": ["answer", "confidence", "assumptions", "risks", "next_steps"]
}

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Devo migrar de Postgres pra Mongo?",
    config=types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=response_schema,
    )
)

import json
output = json.loads(response.text)
```

Observações:

- Tipos em **CAIXA ALTA** (`"OBJECT"`, `"STRING"`, `"ARRAY"`, `"NUMBER"`, `"INTEGER"`, `"BOOLEAN"`) — diferente de JSON Schema clássico. Isso é OpenAPI style.
- `propertyOrdering` (opcional, mas recomendado) — define a ordem em que o modelo emite os campos. Sem ele, ordem é arbitrária. Importante quando você quer que campos como `confidence` sejam emitidos antes de `answer` pra "ancorar" o raciocínio.

## Exemplo Python com Pydantic

O SDK aceita Pydantic model direto — caminho mais ergonômico:

```python
from google import genai
from google.genai import types
from pydantic import BaseModel
from typing import Literal

class Analysis(BaseModel):
    answer: str
    confidence: Literal["low", "medium", "high"]
    assumptions: list[str]
    risks: list[str]
    next_steps: list[str]

client = genai.Client(api_key="...")

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Devo migrar de Postgres pra Mongo?",
    config=types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=Analysis,
    )
)

# SDK parseia automaticamente
analysis: Analysis = response.parsed
# analysis.answer, analysis.confidence, etc — tipado
```

`response.parsed` retorna instância do Pydantic model já validada. Em caso de schema inválido (raro), `response.parsed` é `None` e `response.text` tem o JSON cru pra debug.

## Exemplo Python — enum mode (classificação)

Pra classificação pura — output é um único valor de enum — Gemini tem `response_mime_type: "text/x.enum"`:

```python
class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Classifique a prioridade desse ticket: 'Servidor caiu, clientes não acessam'",
    config=types.GenerateContentConfig(
        response_mime_type="text/x.enum",
        response_schema=Priority,
    )
)

priority = response.text  # "urgent"
```

Output é a string pura, sem JSON wrapping. Útil pra classificadores de alta vazão.

## O subset OpenAPI — diferenças vs JSON Schema

Gemini não aceita JSON Schema puro. O schema segue OpenAPI 3.0, com diferenças importantes:

### Tipos em caixa alta

`"OBJECT"`, `"STRING"`, `"ARRAY"`, `"NUMBER"`, `"INTEGER"`, `"BOOLEAN"`. Não funciona `"object"` minúsculo (que JSON Schema usa).

### `format` mais limitado

Suporta `"date-time"`, `"date"`, `"enum"`. Não suporta `"email"`, `"uri"`, `"uuid"` como format strings.

### `enum` só em string

`enum` em outros tipos não é confiavelmente enforced. Use `string` + enum.

### Sem `additionalProperties`

Gemini não enforça `additionalProperties: false`. Pra travar alucinação de chaves, você precisa validar depois.

### `$ref` limitado

Suporte parcial — refs internos simples funcionam, refs aninhados em arrays podem falhar. Schemas complexos: melhor inline.

### Sem `oneOf`/`anyOf` complexo

Uniões discriminadas não são bem suportadas. Pra polimorfismo, considere modelar como objeto com campo `type` + campos opcionais.

### `nullable: true`

Pra simular tipo opcional/nullable:

```json
{
  "type": "STRING",
  "nullable": true
}
```

Diferente do JSON Schema (`"type": ["string", "null"]`).

### `propertyOrdering`

Específico do Gemini — não existe em OpenAPI puro. Define a ordem de emissão dos campos. Recomendado em todo schema importante porque modelos LLM se beneficiam de ordem coerente (campo "raciocínio" antes do campo "resposta", por exemplo).

## Modelos compatíveis (2026)

Structured output via `response_schema` funciona em:

- **Gemini 1.5 Pro** e **Gemini 1.5 Flash** — suporte estável.
- **Gemini 2.0 Flash**, **Gemini 2.0 Pro** — suporte completo, melhor aderência.
- **Gemini 2.5** (linha mais recente em 2026) — suporte com features adicionais (incluindo `propertyOrdering` mais robusto).

Não funciona em Gemini 1.0 (legado, descontinuado em produção).

Em modelos Flash (menores), schemas muito grandes degradam aderência mais rápido que em Pro — teste antes de assumir paridade.

## Alternativa: tool use (function calling)

Gemini também suporta function calling. Pra structured output via tool:

```python
analysis_function = types.FunctionDeclaration(
    name="record_analysis",
    description="Registra análise estruturada.",
    parameters=response_schema  # mesmo schema
)

tool = types.Tool(function_declarations=[analysis_function])

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Devo migrar?",
    config=types.GenerateContentConfig(
        tools=[tool],
        tool_config=types.ToolConfig(
            function_calling_config=types.FunctionCallingConfig(
                mode="ANY",
                allowed_function_names=["record_analysis"]
            )
        )
    )
)

# Extrai
fc = response.candidates[0].content.parts[0].function_call
args = dict(fc.args)
```

Quando usar tool em vez de `response_schema`:

- Schema usa features que o subset OpenAPI não suporta (uniões, refs complexos).
- Pipeline já tem outras tools.
- Quer raciocínio em texto + structured separado.

## Limitações conhecidas (2026)

- **Aderência levemente abaixo do strict mode da OpenAI** em schemas grandes. Validar é obrigatório.
- **Subset OpenAPI menor que JSON Schema da Anthropic.** Schemas com union, pattern, format custom: forneça por tool ou simplifique.
- **`propertyOrdering` ainda não suportado uniformemente em todos os modelos.** Confira na doc do modelo específico.
- **Erro de schema vira `None` em `response.parsed`** — silencioso. Cheque `response.text` em caso de None.

## Boas práticas

### `description` em cada campo

Como em outros providers, descrições ajudam o modelo. Coloque sempre.

### `propertyOrdering` explícito

Quando suportado, define ordem do output. Coloca campos de raciocínio/contexto antes do output principal — efeito ancoragem similar a chain-of-thought.

### Use Pydantic via SDK

A integração com `google-genai` + Pydantic é a forma ergonômica. Em produção Python, é o caminho default.

### Teste com modelo target

Aderência varia entre Flash e Pro, e entre versões. Teste sempre no modelo que vai rodar em produção, não no maior disponível.

### Combine com validação semântica

Como em todo provider, shape garantido (com ressalvas) ≠ semântica certa. Pydantic validators capturam isso (ver [nota 07](07%20-%20Validação%20e%20retry%20—%20Pydantic,%20Zod.md)).

## Fontes

- **Google** — *Generate structured output with the Gemini API* ([ai.google.dev/gemini-api/docs/structured-output](https://ai.google.dev/gemini-api/docs/structured-output)).
- **Google** — *Function calling with Gemini* ([ai.google.dev/gemini-api/docs/function-calling](https://ai.google.dev/gemini-api/docs/function-calling)).
- **google-genai SDK** — [GitHub: googleapis/python-genai](https://github.com/googleapis/python-genai).

## Veja também

- [[02 - JSON Schema como contrato]] — diferenças vs OpenAPI 3.0
- [[03 - Function calling como mecanismo de output]] — alternativa via tool em Gemini
- [[04 - OpenAI Structured Outputs — strict mode]] — comparação direta
- [[05 - Anthropic tool use para forçar formato]] — terceira abordagem
- [[07 - Validação e retry — Pydantic, Zod]] — necessária pelo subset limitado de Gemini
