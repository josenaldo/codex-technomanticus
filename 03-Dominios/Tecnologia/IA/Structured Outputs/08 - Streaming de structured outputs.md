---
title: "08 - Streaming de structured outputs"
created: 2026-05-28
updated: 2026-05-28
type: concept
status: seedling
progress: in_progress
tags:
  - structured-outputs
  - ia
  - streaming
publish: true
aliases:
  - Streaming structured
  - Partial JSON parsing
---

# 08 - Streaming de structured outputs

> [!abstract] TL;DR
> Streaming clássico de texto funciona bem porque cada chunk é um pedaço válido por si só. Streaming de JSON estruturado tem o problema: um pedaço de JSON no meio (`{"answer": "Sim, mas`) não é parseável. Três caminhos resolvem: (1) streaming nativo de `tool_use` blocks da Anthropic, com `input_json_delta` parcial; (2) parsers de JSON parcial (`json-repair` em Python, `partial-json` em TS) que aceitam JSON incompleto e fecham o que falta; (3) emitir só campos completos pra UI, mantendo o JSON acumulando em buffer. Útil pra UX em chat e canvas longos; quase sempre dispensável em backend pipelines. Validação semântica acontece só no final.

## Por que streaming de JSON é diferente

Streaming de texto:

```
Olá!
Olá! Vou
Olá! Vou te ajudar com
Olá! Vou te ajudar com essa pergunta.
```

Cada estado intermediário é texto válido. Você renderiza incrementalmente. Sem problema.

Streaming de JSON:

```
{
{"answer":
{"answer": "Sim
{"answer": "Sim, considerando
{"answer": "Sim, considerando o cenário", "confidence":
{"answer": "Sim, considerando o cenário", "confidence": "high", "assumptions":
...
{"answer": "Sim, considerando o cenário", "confidence": "high", "assumptions": ["X"], "risks": [], "next_steps": []}
```

Nenhum estado intermediário é JSON válido. Você não pode fazer `JSON.parse(chunk)` em ponto algum exceto no fim. UI que quer mostrar progresso precisa de outra estratégia.

E mais: providers diferentes streamam de formas diferentes. OpenAI streama tokens; Anthropic streama eventos tipados (`input_json_delta` por bloco).

## Caminho 1 — Anthropic native streaming de tool_use

Anthropic streama tool use em deltas tipados. Você recebe eventos `content_block_delta` com `input_json_delta` por bloco de tool:

```python
from anthropic import Anthropic

client = Anthropic()

with client.messages.stream(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    tools=[analysis_tool],
    tool_choice={"type": "tool", "name": "record_analysis"},
    messages=[{"role": "user", "content": "Devo migrar?"}]
) as stream:
    buffer = ""
    for event in stream:
        if event.type == "content_block_delta":
            if event.delta.type == "input_json_delta":
                # Acumula o JSON parcial
                buffer += event.delta.partial_json
                # Tenta parsear (geralmente falha até o fim)
                # — mas pode usar partial parser aqui

    # No final, parseia o output completo
    final_message = stream.get_final_message()
    for block in final_message.content:
        if block.type == "tool_use":
            structured = block.input
```

O streaming nativo serve principalmente pra latência percebida (UI mostra "pensando..." mais cedo). Pra extrair valor real do streaming, combine com partial parser ou emissão por campo (próximas seções).

## Caminho 2 — Partial JSON parsers

Libs que aceitam JSON incompleto e devolvem o objeto "fechado" no melhor esforço:

### Python — `json-repair`

```python
from json_repair import repair_json
import json

partial = '{"answer": "Sim, considerando o cenário", "confidence": "high'

repaired = repair_json(partial)
# '{"answer": "Sim, considerando o cenário", "confidence": "high"}'

parsed = json.loads(repaired)
# {"answer": "Sim, considerando o cenário", "confidence": "high"}
```

A lib fecha strings, arrays, objetos abertos. Útil pra mostrar estado parcial na UI:

```python
import json
from json_repair import repair_json

buffer = ""
for chunk in stream:
    buffer += chunk
    try:
        partial_obj = json.loads(repair_json(buffer))
        render(partial_obj)  # atualiza UI
    except Exception:
        continue  # ignora estados que ainda não dá
```

### TypeScript — `partial-json`

```typescript
import { parse, Allow } from "partial-json";

let buffer = "";
for await (const chunk of stream) {
  buffer += chunk;
  try {
    const partial = parse(buffer, Allow.ALL);
    render(partial);
  } catch {
    // estado intermediário inválido, espera próximo chunk
  }
}
```

`partial-json` é mais permissiva — aceita strings, arrays, objetos parciais e infere o restante.

### Trade-offs de partial parsers

- **Falsos positivos.** Em certos estados, o parser "completa" errado e a UI mostra valor que depois muda. Pode confundir usuário.
- **Custo CPU.** Tentar parsear a cada chunk em alta vazão custa. Use throttling (parse a cada N chunks ou cada X ms).
- **Não enforça schema.** O resultado parcial não respeita seu Pydantic/Zod. É só "JSON-like".

## Caminho 3 — Emissão por campo

Em vez de parsear JSON parcial, identifique quando um campo termina e emita só aquele campo:

```python
import re

buffer = ""
emitted_fields = set()

for chunk in stream:
    buffer += chunk
    # Detecta campos completos via regex simples (não-robusto pra nested)
    matches = re.finditer(
        r'"(\w+)":\s*("(?:[^"\\]|\\.)*"|[\d.]+|true|false|null|\[.*?\])',
        buffer
    )
    for m in matches:
        field, value = m.group(1), m.group(2)
        if field not in emitted_fields:
            emitted_fields.add(field)
            emit_to_ui(field, json.loads(value))
```

Funciona pra schemas planos. Pra schemas nested (arrays de objetos), precisa de parser mais sofisticado.

Caminho 3 só vale a pena pra schemas planos; pra nested, combine Caminho 1 + Caminho 2.

Pattern visual em UI:

```
[━━━━━━━━━━━━━━━━━━━━] Resposta: "Sim, considerando o cenário..."
[━━━━━━━━━━━━━━━━━━━━] Confiança: high
[████░░░░░░░░░░░░░░░░] Premissas: gerando...
[░░░░░░░░░░░░░░░░░░░░] Riscos: aguardando...
```

Cada campo termina, vira "rendered final". Os que ainda não chegaram ficam em skeleton/loading.

## Quando streaming faz sentido em structured

### Faz sentido

- **Canvas / chat UI longos.** Output de várias seções, usuário fica esperando. Mostrar campos conforme chegam reduz percepção de latência.
- **Reasoning models.** Quando o modelo "pensa" antes (`o`-series, `gpt-5-thinking`, Claude Extended Thinking), streamar mostra que está progredindo — usuário não acha que travou.
- **Outputs grandes pra reportar.** Listas longas de itens, código gerado em blocos, narrativas estruturadas.

### Não faz sentido

- **Backend pipelines.** Você consome o objeto inteiro pra próximo passo. Streaming só adiciona complexidade.
- **Schemas pequenos.** Pra 5 campos curtos, o output inteiro chega em <1s. Streaming não muda percepção.
- **Validação semântica obrigatória.** Você precisa do objeto completo + Pydantic antes de fazer qualquer coisa. Stream-pra-display, parse-pra-processar.
- **Logging / auditoria.** Você quer o output final pra log. Stream parcial não vai pro log.

## Validação em streaming — o que dá e o que não dá

Validação semântica completa (Pydantic/Zod com refinements) só roda no final, com o objeto inteiro. Mas algumas verificações podem rodar no parcial:

| Validação | Funciona em parcial? |
|---|---|
| Tipo do campo (string vs number) | Parcial — mas pode mudar antes do fim |
| Enum value | Sim, se a string do enum já fechou |
| `min_length` | Não, ainda pode crescer |
| `max_length` | Sim — se excedeu, abortar |
| Regex match | Não confiável em parcial |
| Cross-field (model_validator) | Não — precisa de tudo |

Em prática: deixe validação completa pro final. No parcial, faça só sanity checks (ex: confidence emitida cedo? bloqueia se for "low" e a task era de alta confiança).

## Mid-stream falha — o que fazer

Quando algo dá errado no meio do stream:

- **Stream cortou** (rede, rate limit) — buffer parcial. Trate como retry com `messages` que inclui o parcial como contexto pro modelo continuar.
- **JSON ficou irrecuperável** (modelo errou e nem `jsonrepair` salva) — descarta, retry sem feedback parcial.
- **Validação semântica falhou no final** — segue o padrão da nota 07 (retry-with-feedback).
- **Excede `max_tokens` no meio** — pode ser sinal de schema muito grande pro budget. Aumenta `max_tokens` ou simplifica schema.

## Boas práticas

### Stream pra UI, completo pra lógica

UI consome stream. Lógica de negócio consome o objeto final validado. Não misture.

### Throttle a renderização

UI atualizando a cada token custa CPU e ofusca leitura. Atualize a cada 100-200ms.

### Logue o objeto final

Stream é UX. Auditoria precisa do objeto completo + status de validação. Logue só no fim.

### Modelo de fallback sem streaming

Se streaming complica demais, considere chamar sem stream e mostrar loading bonito. Em pipelines onde streaming não traz UX clara, simplifica.

### Considere `useObject` / Vercel AI SDK

Em React/Next.js, Vercel AI SDK tem `useObject` que abstrai streaming structured. Vale conhecer se está nessa stack.

## Fontes

- **Anthropic** — *Streaming with tool use* ([docs](https://docs.anthropic.com/en/docs/build-with-claude/tool-use)). Eventos `input_json_delta` e padrão de acumulação.
- **OpenAI** — *Streaming responses* ([platform.openai.com/docs/api-reference/streaming](https://platform.openai.com/docs/api-reference/streaming)).
- **mangiucugna/json_repair** — [GitHub](https://github.com/mangiucugna/json_repair) (lib Python).
- **josdejong/jsonrepair** — [GitHub](https://github.com/josdejong/jsonrepair) (equivalente JS/TS, não confundir com o pacote Python).
- **promplate/partial-json-parser** — [GitHub](https://github.com/promplate/partial-json-parser).
- **Vercel AI SDK** — *useObject docs* ([sdk.vercel.ai](https://sdk.vercel.ai/docs/ai-sdk-ui/object-generation)).

## Veja também

- [[07 - Validação e retry — Pydantic, Zod]] — validação completa só após objeto final
- [[04 - OpenAI Structured Outputs — strict mode]] — streaming com response_format
- [[05 - Anthropic tool use para forçar formato]] — streaming nativo de tool_use
- [[Anatomia dos LLMs/12 - Streaming, batching e latência|Anatomia dos LLMs — Streaming, batching e latência]] — fundamentos de streaming em LLMs
- [[AI Engineering Stack/05 - Output Layer|AI Engineering Stack — Output Layer]] — onde decisão de streaming entra na arquitetura
