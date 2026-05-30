---
title: "02 - JSON Schema como contrato"
created: 2026-05-28
updated: 2026-05-28
type: concept
status: seedling
progress: in_progress
tags:
  - structured-outputs
  - ia
  - json-schema
publish: true
aliases:
  - JSON Schema
  - Schema como contrato
---

# 02 - JSON Schema como contrato

> [!abstract] TL;DR
> JSON Schema é a linguagem padrão pra declarar a forma do output esperado: `type`, `properties`, `required`, `enum`, `additionalProperties`. Todos os providers (OpenAI, Anthropic, Gemini) aceitam JSON Schema (ou um subset dele) como entrada do mecanismo de enforcement. Escrever o schema bem — `enum` pra dimensões fechadas, `required` pra campos críticos, `additionalProperties: false` pra travar alucinação de chaves — é metade do trabalho. Esta nota cobre o subset que importa na prática, traz o schema canônico do @hooeem como exemplo completo, e identifica quando schema é exagero.

## JSON Schema 101

JSON Schema é uma especificação ([json-schema.org](https://json-schema.org/)) pra descrever a estrutura de dados JSON. Você escreve um JSON que descreve outro JSON. Os campos que importam no contexto de LLM:

### `type`

Tipo primitivo do valor. Os úteis:

- `"string"` — texto.
- `"number"` — número (decimal ou inteiro).
- `"integer"` — só inteiro.
- `"boolean"` — `true`/`false`.
- `"array"` — lista.
- `"object"` — objeto.
- `"null"` — null literal (usado em uniões: `["string", "null"]`).

### `properties`

Pra `object`, mapeia nome de campo → schema do campo:

```json
{
  "type": "object",
  "properties": {
    "nome": { "type": "string" },
    "idade": { "type": "integer" }
  }
}
```

### `required`

Lista os campos que **devem** existir. Sem `required`, todo campo é opcional, e o modelo pode legitimamente omitir:

```json
{
  "type": "object",
  "properties": {
    "nome": { "type": "string" },
    "idade": { "type": "integer" }
  },
  "required": ["nome"]
}
```

> [!warning] OpenAI strict mode
> Em strict mode da OpenAI ([nota 04](04%20-%20OpenAI%20Structured%20Outputs%20—%20strict%20mode.md)), **todos** os campos em `properties` precisam estar em `required`. Pra simular opcional, use `["string", "null"]` no `type`.

### `enum`

Restringe o valor a uma lista fechada. Indispensável pra dimensões categóricas:

```json
{
  "type": "string",
  "enum": ["low", "medium", "high"]
}
```

Sem `enum`, o modelo é livre pra inventar valores adjacentes (`"medium-low"`, `"med"`, `"meio"`). Com `enum`, o provider rejeita ou regenera.

### `additionalProperties`

Define se chaves não declaradas são permitidas. Default é `true` (permite). Pra travar alucinação de campos:

```json
{
  "type": "object",
  "properties": { ... },
  "additionalProperties": false
}
```

Esse é provavelmente o campo mais subestimado. Sem ele, o modelo pode adicionar `observacao`, `notas`, `extra_info` à vontade. Com ele, qualquer chave fora do declarado é erro.

### Arrays

```json
{
  "type": "array",
  "items": { "type": "string" },
  "minItems": 1,
  "maxItems": 5
}
```

`items` declara o schema dos elementos. `minItems`/`maxItems` impõem limites (útil pra forçar pelo menos um item, ou no máximo cinco sugestões).

### Aninhamento

Objetos e arrays compõem sem limite:

```json
{
  "type": "object",
  "properties": {
    "endereco": {
      "type": "object",
      "properties": {
        "rua": { "type": "string" },
        "numero": { "type": "integer" }
      },
      "required": ["rua", "numero"]
    },
    "tags": {
      "type": "array",
      "items": { "type": "string" }
    }
  }
}
```

Strict mode da OpenAI suporta até 5 níveis de aninhamento e 100 propriedades totais — confira limites atuais na doc do provider.

## O schema canônico — @hooeem

O exemplo de referência usado ao longo desta trilha vem do @hooeem (cap #6): um schema pra capturar resposta de LLM **com sua incerteza estruturada**. Em vez de pedir "responda a pergunta", você pede um objeto que inclui resposta + confiança + premissas + riscos + próximos passos.

```json
{
  "type": "object",
  "properties": {
    "answer": {
      "type": "string",
      "description": "Resposta direta à pergunta do usuário."
    },
    "confidence": {
      "type": "string",
      "enum": ["low", "medium", "high"],
      "description": "Confiança do modelo na resposta."
    },
    "assumptions": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Premissas que a resposta assume como verdadeiras."
    },
    "risks": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Riscos ou caveats se a resposta for seguida."
    },
    "next_steps": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Próximos passos sugeridos pro usuário."
    }
  },
  "required": ["answer", "confidence", "assumptions", "risks", "next_steps"],
  "additionalProperties": false
}
```

Por que esse schema é instrutivo:

1. **`confidence` como enum.** Força o modelo a escolher entre três níveis discretos. Sem enum, viria *"fairly confident"*, *"about 70%"*, *"unsure"* — tudo difícil de rotear downstream.
2. **`assumptions` e `risks` como arrays obrigatórios.** Mesmo quando vazios, o modelo precisa retornar `[]`. Isso obriga o modelo a *considerar* premissas — efeito comportamental similar a chain-of-thought, mas estruturado.
3. **`next_steps` deslocando o modelo pra ação.** Output puramente declarativo (a resposta) vira um output acionável (o que fazer com ela).
4. **`additionalProperties: false`.** Sem isso, o modelo gostaria de adicionar `confidence_reasoning`, `caveats`, `meta`. Trava.
5. **Tudo `required`.** Strict mode compatível, e força o modelo a preencher cada campo — não pode omitir `risks` porque "não tem".

O schema é genérico o suficiente pra reusar em pipelines diversos — QA, classificação com explicação, recomendação. É um bom default antes de especializar.

## Patterns úteis na prática

### `description` em todo campo

LLMs leem o schema. Descrições orientam o preenchimento:

```json
{
  "type": "string",
  "description": "Sigla do estado em UF (ex: SP, RJ, MG)."
}
```

Em strict mode da OpenAI, descrições contam como parte do contrato — o modelo é mais aderente quando elas existem.

### `enum` pra qualquer dimensão fechada

Categorias, status, prioridades, sentimentos. Não deixe texto livre quando a lista é conhecida.

### Required pra campos críticos, opcional pra extras

Em modos não-strict (Anthropic, Gemini), separar `required` (essencial) de opcional (extras úteis) deixa o modelo decidir se preenche. Bom pra campos como `confidence_reasoning` que só fazem sentido se o modelo tem o que dizer.

### `additionalProperties: false` por padrão

Default é o oposto, mas pra LLM você quase sempre quer `false`. Adicione explicitamente.

### Schema reutilizado via `$ref`

Pra schemas grandes, defina sub-schemas em `$defs` e referencie:

```json
{
  "$defs": {
    "Endereco": {
      "type": "object",
      "properties": { "rua": { "type": "string" }, "cep": { "type": "string" } },
      "required": ["rua", "cep"]
    }
  },
  "type": "object",
  "properties": {
    "cobranca": { "$ref": "#/$defs/Endereco" },
    "entrega": { "$ref": "#/$defs/Endereco" }
  }
}
```

OpenAI e Gemini suportam `$ref` interno. Anthropic aceita JSON Schema completo via tool, então também suporta.

## Quando schema é overkill

Schema vem com custo cognitivo e operacional:

- **Você precisa manter ele em sincronia** com o consumidor downstream.
- **Modelo gasta tokens** pra preencher campos (e você paga por eles).
- **Schema muito rígido frustra exploração** — o modelo não pode dizer "não sei" ou levantar caso não previsto.

Casos onde schema atrapalha:

- **Drafts e brainstorming.** Você quer o modelo divagando, não constrangido por shape.
- **Chat conversacional puro.** O usuário escreve, o modelo responde em texto. Schema aqui é cerimônia.
- **Sumarização pra leitura humana.** Markdown serve.
- **Output com forma muito variável.** Se o que sai depende de qual ramo da lógica o modelo seguir, schema fica cheio de optional/null e perde valor.

Heurística: se downstream é **código**, schema. Se downstream é **humano**, livre. Se cinza, vale gerar duas saídas — uma livre, uma estruturada — em chamadas separadas ou via campo composto.

## Limites práticos por provider

| Provider | Schema language | Limites principais |
|---|---|---|
| **OpenAI** (strict) | JSON Schema subset | Sem `additionalProperties: true`, todos required, max 5 níveis aninhamento, max 100 props totais |
| **OpenAI** (non-strict) | JSON Schema | Mais permissivo, sem garantia 100% |
| **Anthropic** | JSON Schema (via tools) | Sem `pattern`, `oneOf`, `allOf` complexos confiáveis; resto OK |
| **Gemini** | OpenAPI 3.0 subset | Subset menor — sem `$ref` cross-schema, sem `enum` em arrays aninhados em certos modos |

Detalhes específicos nas notas 04, 05, 06.

## Fontes

- **@hooeem** — *Become an AI Engineer*, cap #6. Schema canônico answer/confidence/assumptions/risks/next_steps.
- **JSON Schema spec** ([json-schema.org/specification.html](https://json-schema.org/specification.html)).
- **OpenAI** — *Structured Outputs guide — Supported schemas* ([docs](https://platform.openai.com/docs/guides/structured-outputs#supported-schemas)).
- **Anthropic** — *Tool use — JSON Schema in tool definitions* ([docs](https://docs.anthropic.com/en/docs/build-with-claude/tool-use)).

## Veja também

- [[01 - O problema do output não estruturado]] — o problema que o schema resolve
- [[03 - Function calling como mecanismo de output]] — como o schema é passado pro modelo
- [[04 - OpenAI Structured Outputs — strict mode]] — as restrições específicas do strict
- [[07 - Validação e retry — Pydantic, Zod]] — schema garante shape, validador garante semântica
- [[Dicionário de IA#JSON Schema|Dicionário: JSON Schema]]
