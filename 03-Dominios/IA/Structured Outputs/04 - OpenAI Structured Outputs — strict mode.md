---
title: "04 - OpenAI Structured Outputs — strict mode"
created: 2026-05-28
updated: 2026-05-28
type: concept
status: seedling
progress: in_progress
tags:
  - structured-outputs
  - ia
  - openai
publish: true
aliases:
  - OpenAI strict mode
  - response_format json_schema
---

# 04 - OpenAI Structured Outputs — strict mode

> [!abstract] TL;DR
> OpenAI oferece duas formas de structured output: via `response_format: { type: "json_schema", strict: true }` (mais simples, recomendada pra output único) e via `tools` + `tool_choice` forçado (necessária quando você já tem pipeline de tools). Em strict mode, a aderência ao schema é **garantida pelo provider** — o decoder é restringido pra só emitir tokens válidos. Custo: subset de JSON Schema (sem `additionalProperties: true`, todos campos `required`), pequena latência adicional. Compatível com gpt-4o-2024-08-06+, gpt-4.1 e família gpt-5. SDK Python tem helper `parse()` que integra direto com Pydantic.

## O mecanismo — strict mode

Strict mode da OpenAI usa **constrained decoding**: o provider monta uma grammar a partir do JSON Schema e força o decoder a emitir só tokens que mantenham o output válido. Resultado: 100% de aderência ao shape (não a semântica), garantido por arquitetura, não por probabilidade.

A penalidade é pequena (~50-150ms na primeira chamada com schema novo, cacheado depois) e a categoria de erro "JSON inválido" desaparece.

### Forma 1 — `response_format` direto

A forma mais simples, recomendada quando você só quer output estruturado:

```python
from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o-2024-08-06",
    messages=[
        {"role": "system", "content": "Você é um analista. Responda em estrutura."},
        {"role": "user", "content": "Devo migrar de Postgres pra Mongo no projeto X?"}
    ],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "analysis",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "answer": { "type": "string" },
                    "confidence": {
                        "type": "string",
                        "enum": ["low", "medium", "high"]
                    },
                    "assumptions": {
                        "type": "array",
                        "items": { "type": "string" }
                    },
                    "risks": {
                        "type": "array",
                        "items": { "type": "string" }
                    },
                    "next_steps": {
                        "type": "array",
                        "items": { "type": "string" }
                    }
                },
                "required": ["answer", "confidence", "assumptions", "risks", "next_steps"],
                "additionalProperties": False
            }
        }
    }
)

import json
output = json.loads(response.choices[0].message.content)
```

O `content` já é JSON válido. Ainda precisa parsear com `json.loads`, mas sem try/except defensivo — strict mode garante.

### Forma 2 — helper `parse()` com Pydantic

Mais ergonômico — define o schema como Pydantic model e o SDK cuida do resto:

```python
from openai import OpenAI
from pydantic import BaseModel
from typing import Literal

class Analysis(BaseModel):
    answer: str
    confidence: Literal["low", "medium", "high"]
    assumptions: list[str]
    risks: list[str]
    next_steps: list[str]

client = OpenAI()

completion = client.chat.completions.parse(
    model="gpt-4o-2024-08-06",
    messages=[
        {"role": "system", "content": "Você é um analista. Responda em estrutura."},
        {"role": "user", "content": "Devo migrar de Postgres pra Mongo?"}
    ],
    response_format=Analysis,
)

analysis: Analysis = completion.choices[0].message.parsed
# analysis.answer, analysis.confidence, etc — tipado
```

`parse()` converte o Pydantic model em JSON Schema, manda com strict, parsea de volta pra Pydantic. Erros de schema (Pydantic não consegue converter) viram exception. É o caminho recomendado pra novos projetos Python.

### Forma 3 — `tools` + `tool_choice`

Quando o pipeline já usa tools, ou quando você quer schema na "função" mas raciocínio em texto:

```python
response = client.chat.completions.create(
    model="gpt-4o-2024-08-06",
    messages=[{"role": "user", "content": pergunta}],
    tools=[{
        "type": "function",
        "function": {
            "name": "record_analysis",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": { ... },
                "required": [...],
                "additionalProperties": False
            }
        }
    }],
    tool_choice={"type": "function", "function": {"name": "record_analysis"}}
)

import json
args = json.loads(response.choices[0].message.tool_calls[0].function.arguments)
```

O `strict: true` no schema da função garante a mesma garantia do `response_format`.

## Restrições do strict mode

Strict mode não suporta JSON Schema inteiro. Os limites importantes:

### Todos os campos em `required`

Não tem opcional. Pra simular:

```json
{
  "type": "object",
  "properties": {
    "nome": { "type": "string" },
    "apelido": { "type": ["string", "null"] }
  },
  "required": ["nome", "apelido"]
}
```

O modelo retorna `null` quando não tem valor. Sua aplicação interpreta `null` como ausente.

### `additionalProperties: false` obrigatório em todo objeto

Não dá pra deixar default. Tem que declarar explícito em cada `object` (incluindo aninhados).

### Subset de tipos suportados

`string`, `number`, `integer`, `boolean`, `array`, `object`, `null`, e união simples (`["string", "null"]`). Sem:

- `pattern` em strings (regex)
- `format` strings exóticos (`date`, `email`, `uri` — alguns suportados, verifique doc)
- `minLength`/`maxLength`/`minimum`/`maximum` — não enforced no decoder (ignorados)
- `minItems`/`maxItems` em arrays — idem
- `oneOf`/`anyOf` com restrições complexas

Pra essas validações, valide você mesmo depois (ver [nota 07](07%20-%20Validação%20e%20retry%20—%20Pydantic,%20Zod.md)).

### Limites de tamanho

- Max 100 propriedades totais no schema (somando objetos aninhados).
- Max 5 níveis de aninhamento.
- Max 500 enum values (somando todos os enums).
- Max 15000 caracteres em string descritivas totais.

Schemas grandes precisam ser simplificados — ou divididos em chamadas separadas.

### `$ref` interno suportado, externo não

```json
{
  "$defs": { "Address": { "type": "object", ... } },
  "type": "object",
  "properties": { "billing": { "$ref": "#/$defs/Address" } }
}
```

Funciona. `$ref` apontando pra URL externa não.

## Modelos compatíveis (2026)

Strict mode da OpenAI funciona em:

- `gpt-4o-2024-08-06` e posteriores (incluindo `gpt-4o-mini`)
- Família `gpt-4.1` (todos)
- Família `gpt-5` (todos, incluindo `gpt-5-mini` e reasoning models como `gpt-5-thinking`)
- `o1`, `o3`, `o4` (reasoning models — strict funciona após `o1-2024-12-17`)

Não funciona em modelos legados (gpt-4-turbo, gpt-3.5-turbo) — usar `response_format: { type: "json_object" }` (JSON mode antigo, sem schema). Em produção em 2026, nenhum motivo pra ficar nesses.

Reasoning models (`o`-series, `gpt-5-thinking`) suportam strict mode plenamente desde 2025, mas custam mais tokens — strict não reduz tokens de reasoning, só formata o output final.

## Quando usar `response_format` vs `tools`

| Caso | Preferência |
|---|---|
| Único output estruturado, sem tools no pipeline | `response_format` |
| Pipeline com tools reais + output estruturado final | `tools` (pattern A da nota 03) |
| Quer raciocínio em texto + structured separado | Duas chamadas, ou `tools` com prompt explícito |
| Schema com uniões complexas | `tools` (mais flexível) |
| Multi-provider abstration | `tools` (denominador comum) |

## Boas práticas

### Inclua `description` nos campos

Strict não enforça descrições, mas o modelo usa pra preenchimento. Tudo o que você quer que ele "considere" coloque em `description`.

### Schema versionado

Trate `schema` como contrato versionado. Mude com cuidado, teste com golden set ([[Anatomia dos LLMs/17 - Evaluation de LLMs em produção|nota de evaluation]]) antes de promover.

### Cache de schema

Schemas grandes têm overhead na primeira chamada (gramática é montada). OpenAI cacheia automaticamente por algumas horas; aproveite mantendo schema estável.

### Use `parse()` no Python

A ergonomia compensa. Em produção Python, Pydantic + `parse()` é o caminho default.

### Não confunda strict com semantic

Strict garante shape. Semântica (valores fazem sentido?) é outra camada. Ver [nota 07](07%20-%20Validação%20e%20retry%20—%20Pydantic,%20Zod.md).

## Fontes

- **OpenAI** — *Structured Outputs guide* ([platform.openai.com/docs/guides/structured-outputs](https://platform.openai.com/docs/guides/structured-outputs)). Documentação oficial completa, com limites e exemplos atualizados.
- **OpenAI** — *Introducing Structured Outputs in the API* ([blog, ago 2024](https://openai.com/index/introducing-structured-outputs-in-the-api/)). Anúncio original com mecanismo de constrained decoding.
- **Pydantic + OpenAI integration** — [Pydantic AI docs](https://ai.pydantic.dev/).

## Veja também

- [[02 - JSON Schema como contrato]] — a linguagem usada no `schema` do strict
- [[03 - Function calling como mecanismo de output]] — quando `tools` é a forma certa
- [[05 - Anthropic tool use para forçar formato]] — como Anthropic resolve (sem API equivalente)
- [[06 - Gemini structured output]] — alternativa do Google
- [[07 - Validação e retry — Pydantic, Zod]] — semântica em cima do shape garantido
