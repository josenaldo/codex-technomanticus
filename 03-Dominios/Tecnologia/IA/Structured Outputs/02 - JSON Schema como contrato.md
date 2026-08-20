---
title: "02 - JSON Schema como contrato"
created: 2026-05-28
updated: 2026-07-02
type: concept
status: seedling
progress: in_progress
fase: iniciado
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

> [!question]- O que eu preciso saber antes de ler isso?
> Você entende o problema da nota anterior — que "pedir JSON no prompt" não é suficiente em produção. Esta nota resolve a linguagem: como escrever formalmente o que você quer. JSON Schema é uma especificação independente de LLM, usada em APIs REST, validadores de banco, configurações de serviço — você pode já ter encontrado ele no contexto de OpenAPI. Aqui o uso é diferente: o schema não documenta o output, ele *força* o output. Mas a sintaxe é a mesma, então qualquer familiaridade com JSON Schema / OpenAPI acelera a leitura.

## JSON Schema 101

Imagine que você pede pro modelo classificar um bug report e ele devolve `{"severidade": "bastante grave", "prioridade_sugerida": "P1-ish", "comentario_extra": "acho que é urgente"}`. Três problemas de uma vez: um valor que nenhum enum do seu sistema reconhece (`"bastante grave"`), um campo com dado ambíguo (`"P1-ish"` não é `P0`/`P1`/`P2`), e uma chave que você nunca pediu (`comentario_extra`). Nenhum desses três é bug do modelo — é ausência de contrato. O prompt disse "classifique a severidade", mas nunca disse *qual é a forma exata do JSON de saída*. É isso que JSON Schema resolve: uma especificação ([json-schema.org](https://json-schema.org/)) pra descrever a estrutura de dados JSON — você escreve um JSON que descreve outro JSON. Os campos que importam no contexto de LLM:

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

## Caso prático — do schema quebrado ao contrato confiável

Volta ao exemplo da abertura: você está construindo um triador automático de bug reports. O pipeline lê o texto do report e pede ao modelo pra classificar severidade, decidir se precisa de escalonamento e listar componentes afetados. Downstream, um serviço em produção consome esse JSON pra rotear o ticket — se o shape vier errado, o roteamento quebra silenciosamente.

**Tentativa 1 — o schema que parece certo mas falha:**

```json
{
  "type": "object",
  "properties": {
    "severidade": { "type": "string" },
    "precisa_escalonamento": { "type": "boolean" },
    "componentes_afetados": { "type": "array", "items": { "type": "string" } },
    "justificativa": { "type": "string" }
  },
  "required": ["severidade"]
}
```

Rode esse schema contra alguns reports reais e os problemas aparecem:

1. **`severidade` sem `enum`.** O modelo respondeu `"grave"`, `"alta"`, `"P1"`, `"critical"` em execuções diferentes pro mesmo nível de gravidade. O serviço downstream espera exatamente `"low"`, `"medium"`, `"high"`, `"critical"` — nenhuma dessas variantes bate.
2. **Só `severidade` é `required`.** Em ~30% das respostas o modelo omitiu `componentes_afetados` inteiramente, porque nada obrigava o campo a existir. O código que consome o JSON quebrou com `KeyError` porque assumia que o campo sempre vinha.
3. **Sem `additionalProperties: false`.** Uma das respostas trouxe `"componentes_afetados": [...], "componentes_afetados_extra": [...]` — o modelo duplicou o campo com um nome parecido, achando que estava sendo prestativo. Esse campo extra nunca é lido, mas também nunca é *rejeitado* — ele só fica ali, ruído silencioso que ninguém percebe até auditar os logs.
4. **`justificativa` opcional, mas usada como texto livre longo.** Em alguns casos o modelo escreveu um parágrafo inteiro ali, inflando tokens de saída sem que ninguém tivesse pedido verbosidade.

O erro de raiz não é o modelo "alucinando" — é o schema não fechar as três coisas que ele deveria fechar: vocabulário (`enum`), obrigatoriedade (`required` completo) e superfície (`additionalProperties: false`).

**Tentativa 2 — o schema corrigido:**

```json
{
  "type": "object",
  "properties": {
    "severidade": {
      "type": "string",
      "enum": ["low", "medium", "high", "critical"],
      "description": "Nível de gravidade do bug, avaliado pelo impacto em produção."
    },
    "precisa_escalonamento": {
      "type": "boolean",
      "description": "true se o bug afeta usuários em produção agora."
    },
    "componentes_afetados": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Nomes dos componentes/serviços afetados. Array vazio se não identificado."
    },
    "justificativa": {
      "type": "string",
      "description": "Uma frase curta explicando a severidade escolhida."
    }
  },
  "required": ["severidade", "precisa_escalonamento", "componentes_afetados", "justificativa"],
  "additionalProperties": false
}
```

O que mudou, e por quê cada mudança fecha exatamente um dos furos observados:

- `enum` em `severidade` elimina a variação de vocabulário — o provider rejeita ou regenera qualquer valor fora da lista.
- Todos os campos em `required` eliminam a omissão silenciosa — `componentes_afetados` agora sempre existe, mesmo que como `[]`.
- `additionalProperties: false` elimina os campos-fantasma como `componentes_afetados_extra`.
- `description` em `justificativa` ("uma frase curta") não é enforcement técnico, mas orienta o modelo a não inflar o campo — o provider não garante o comprimento, mas descrições reduzem a variância.

Rodando o schema corrigido contra os mesmos reports, as respostas convergem: `severidade` sempre em um dos quatro valores esperados, `componentes_afetados` sempre presente (mesmo vazio), zero campos extras. O código downstream que fazia `if response["severidade"] == "critical"` para de falhar silenciosamente porque agora a string é sempre uma das quatro que o `if` conhece.

A lição generaliza: quando um schema "parece certo" mas o comportamento em produção é inconsistente, o diagnóstico quase sempre está em um destes três furos — falta `enum` numa dimensão fechada, falta algum campo em `required`, ou falta `additionalProperties: false`. Antes de suspeitar do modelo, releia o schema procurando por esses três.

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

## Armadilhas comuns

> [!warning] Esquecer `additionalProperties: false`
> O default de JSON Schema é `additionalProperties: true` — qualquer chave extra é permitida. Na prática isso significa que o modelo pode adicionar campos que achei úteis mas você não pediu: `confidence_reasoning`, `observacao`, `nota_do_analista`. Esses campos chegam ao seu código silenciosamente, ou quebram parsers que validam shape. Coloque `additionalProperties: false` explicitamente em todo schema de LLM — nunca confie no default.

> [!warning] Usar texto livre onde enum resolve
> Quando um campo tem uma lista fechada de valores válidos — status de pedido, categoria de bug, nível de prioridade — é tentador usar `"type": "string"` e confiar que o modelo vai escolher bem. Sem `enum`, o modelo é livre para inventar variantes: `"medium-high"`, `"baixo"`, `"med"`, `"3/5"`. Com `enum`, o provider rejeita ou regenera. A tentação de deixar texto livre costuma vir de preguiça de listar os valores — e cria inconsistências que só aparecem downstream.

> [!warning] Schema inconsistente com o comportamento real esperado
> Schema é uma forma de comunicação com o modelo — e ele o lê. Se você quer que `confidence` seja baixo/médio/alto mas coloca `"enum": ["low", "medium", "high"]` enquanto o restante do prompt está em português, pode haver tensão entre o schema e o contexto. O modelo pode preencher `confidence` literalmente como `"low"` mas tratar isso como EN no raciocínio. Mais importante: se `required` lista campos que às vezes não fazem sentido (ex: `next_steps` em resposta a um erro), o modelo é forçado a inventar algo. Revise se cada campo required realmente se aplica em todos os casos do schema.

## Como explicar em inglês

Em entrevistas sobre design de sistemas de IA, a pergunta sobre structured outputs frequentemente vem junto com a pergunta sobre "how do you handle LLM output reliability":

> "JSON Schema is the standard language for declaring the expected shape of LLM output. All major providers — OpenAI, Anthropic, Gemini — accept it as input to their enforcement mechanism. The key fields in practice are `type`, `properties`, `required` to lock in mandatory fields, `enum` for closed-vocabulary dimensions, and `additionalProperties: false` to prevent hallucinated extra keys. Schema guarantees shape, not semantics — once you have a valid object, you still need validation logic for business rules."

| Português | Inglês |
|-----------|--------|
| schema como contrato | schema as contract |
| campo obrigatório | required field |
| campo adicional proibido | no additional properties |
| dimensão fechada | closed-vocabulary dimension / enum |
| aninhamento | nesting |
| tipo primitivo | primitive type |
| sub-schema | sub-schema / nested schema |
| limites do provider | provider-specific constraints |
| modo strict | strict mode |
| schema muito rígido | overly rigid schema |

## O que vem a seguir

Você sabe escrever o contrato. Agora precisa de um mecanismo que faça o modelo respeitá-lo — não por instrução de prompt, mas por enforcement de API. A nota 03 cobre function calling, o mecanismo original de structured output: como o conceito de "ferramenta com schema" foi repropositado para forçar formato de output.

Ver [[03 - Function calling como mecanismo de output]].

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
