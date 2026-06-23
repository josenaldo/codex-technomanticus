---
title: "03 - Function calling como mecanismo de output"
created: 2026-05-28
updated: 2026-05-28
type: concept
status: seedling
progress: in_progress
tags:
  - structured-outputs
  - ia
  - function-calling
publish: true
aliases:
  - Function calling como output
  - Tool use como structured output
---

# 03 - Function calling como mecanismo de output

> [!abstract] TL;DR
> Function calling (tool use) não é só pra agentes — é o mecanismo mais confiável de forçar formato em qualquer chamada de LLM. O flip conceitual: você define uma única "função" (`record_analysis`, `extract_invoice`, `classify_ticket`) que **não é uma função de verdade**, é só um schema com nome. Pede ao modelo pra "chamar" essa função, e o que volta nos `tool_use` blocks é seu structured output. Funciona em todos os providers que suportam tool use (todos os relevantes), inclusive os que não têm API dedicada de structured output. Custo: latência um pouco maior, alguns tokens a mais de overhead. Ganho: aderência ao schema próxima de 100%.

## O flip conceitual

Quando você aprende sobre function calling, o framing usual é:

> *"Defina ferramentas que o modelo pode chamar pra interagir com o mundo — buscar na web, ler arquivo, mandar email. O modelo decide quando chamar."*

Esse framing é correto pra agentes ([[Anatomia de Agents]]). Mas ele esconde um uso muito mais comum em pipelines não-agênticos:

> *"Defina uma única ferramenta cujo único propósito é receber o output estruturado que você quer. Force o modelo a chamá-la. O que ela receberia como argumentos é o seu structured output."*

A "função" não executa nada. Você nunca chama ela de verdade. Ela é só um schema com nome que sinaliza pro modelo: *"emita os campos que satisfaçam essa assinatura"*.

Por que funciona tão bem:

1. **Modelos são treinados pesadamente em tool use.** RLHF moderno inclui muitos exemplos de chamadas de tool válidas. Aderência ao schema declarado é parte do que recompensa.
2. **A interface separa output de prosa.** O modelo emite tool_use blocks separados de texto narrativo, e o provider valida o JSON antes de entregar. Você não precisa parsear o response inteiro.
3. **Cobertura universal.** OpenAI, Anthropic e Gemini suportam. Llama família via vLLM/SGLang também. Funciona como denominador comum.

## O padrão na prática

A ideia é desenhar uma tool que descreve seu output, com nome semântico:

```python
tools = [{
    "name": "record_analysis",
    "description": (
        "Registra a análise estruturada da pergunta do usuário. "
        "Use esta ferramenta para retornar a resposta no formato esperado."
    ),
    "input_schema": {
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
}]
```

Você não implementa `record_analysis` em lugar nenhum. Quando o modelo "chama", você simplesmente extrai os argumentos:

```python
response = client.messages.create(
    model="claude-sonnet-4-5",
    tools=tools,
    tool_choice={"type": "tool", "name": "record_analysis"},
    messages=[{"role": "user", "content": pergunta}],
    max_tokens=1024
)

for block in response.content:
    if block.type == "tool_use" and block.name == "record_analysis":
        structured_output = block.input
        # structured_output é o dict validado contra o schema
        break
```

`tool_choice` forçado garante que o modelo emite a tool — não vai escolher responder em texto livre.

## Por que isso bate "pede JSON no prompt"

Comparação direta:

| Aspecto | Prompt "retorne JSON" | Tool use forçado |
|---|---|---|
| Aderência ao schema | ~95% | ~99.9% (com providers maduros) |
| Markdown wrapper | Acontece | Não acontece — output é separado |
| Texto em volta | Acontece | Não — tool_use é bloco isolado |
| Chave alucinada | Acontece se schema não trava | Bloqueada pelo provider |
| Tipo errado (string vs number) | Acontece | Validado pelo provider |
| Latência | Baseline | +50-200ms |
| Tokens output | Baseline | +20-50 (overhead de tool_use) |
| Compatível com providers | Todos | Todos os relevantes |

A penalidade é pequena. O ganho é enorme.

## Quando usar essa técnica vs structured outputs nativos

OpenAI tem API dedicada de structured output (`response_format` com `json_schema`, ver [nota 04](04%20-%20OpenAI%20Structured%20Outputs%20—%20strict%20mode.md)). Gemini também (`response_schema`, ver [nota 06](06%20-%20Gemini%20structured%20output.md)). Anthropic **não** — pra Claude, tool use forçado **é** o mecanismo (ver [nota 05](05%20-%20Anthropic%20tool%20use%20para%20forçar%20formato.md)).

Heurística:

- **Anthropic** — sempre tool use forçado. Não tem alternativa.
- **OpenAI** — prefira `response_format` strict (mais simples, sem overhead de tool). Use tool quando precisa de uniões complexas ou quando o pipeline já usa tools.
- **Gemini** — prefira `response_schema`. Use tool se precisar de validação mais rigorosa que o response schema oferece.
- **Multi-provider** — tool use é o denominador comum. Se você abstrai providers, programe contra tool e ganha portabilidade.

## Pattern: tool single-purpose vs tool real

Em pipelines agênticos, você tem tools reais (`search_web`, `read_file`) e *também* quer output estruturado da resposta final. Dois sub-patterns:

### Pattern A — tool de finalização

Adicione uma tool `respond_to_user` cujo schema é o output final. Instrua o modelo a chamá-la quando estiver pronto:

```
Você tem ferramentas para investigar (search_web, read_file).
Quando tiver a resposta, chame `respond_to_user` com a estrutura final.
Não responda em texto livre — só via tool.
```

Funciona, mas o modelo pode esquecer e responder em texto. Em produção, valide e force retry.

### Pattern B — passo de extração separado

Deixe o agente trabalhar com texto livre, e depois faça uma chamada extra ao LLM passando o resultado final + tool de extração:

```python
# Passo 1: agente investiga, responde em texto livre
agent_response = run_agent(pergunta)

# Passo 2: estrutura
structured = client.messages.create(
    model="claude-haiku-4-5",  # modelo barato
    tools=[record_analysis_tool],
    tool_choice={"type": "tool", "name": "record_analysis"},
    messages=[
        {"role": "user", "content": (
            "Extraia da análise abaixo um output estruturado.\n\n"
            f"{agent_response}"
        )}
    ]
)
```

Pattern B custa uma chamada a mais mas separa responsabilidades. Em produção, frequente: agente potente (Claude Sonnet) raciocina, modelo barato (Haiku) estrutura.

## Trade-offs

### Latência

Tool use adiciona overhead — o provider precisa validar schema, e em strict mode, regenerar se inválido. Tipicamente +50-200ms vs texto livre. Em alta vazão, isso conta.

### Custo

Tokens extras: definição da tool entra como input (cobrado), tool_use block tem overhead estrutural. Pra um schema típico de 5 campos, espere +30-80 tokens input + +10-30 output. Em pipelines de alta frequência, otimize a descrição da tool.

### Debug

Quando algo dá errado, você precisa olhar dois lugares: o `stop_reason` (foi `tool_use` mesmo?) e o `tool_use.input`. Texto livre é mais fácil de debugar.

### Modelos pequenos

Modelos pequenos (Haiku, Flash, Mini) são piores em tool use do que em texto. Pra structured output sem tool, eles podem ir melhor com modo nativo (response_format / response_schema). Teste antes de assumir.

## Conexões

Esse mecanismo é o mesmo que [[MCP]] usa pra expor tools de fora — você só descreve schemas, o cliente decide chamar. E o loop ReAct ([[03-Dominios/Tecnologia/IA/Anatomia de Agents/02 - O loop ReAct e native tool use|loop ReAct e native tool use]]) é o caso geral onde múltiplas chamadas de tool encadeiam; structured output é o caso degenerado de uma única chamada, forçada.

## Fontes

- **@hooeem** — *Become an AI Engineer*, cap #11. Posição "tool use é o mecanismo certo pra structured output".
- **Anthropic** — *Tool use overview* ([docs](https://docs.anthropic.com/en/docs/build-with-claude/tool-use/overview)). Recomendação oficial de single tool + `tool_choice` forçado.
- **OpenAI** — *Function calling guide* ([docs](https://platform.openai.com/docs/guides/function-calling)).
- **Eugene Yan** — *Patterns for LLM Systems* ([eugeneyan.com](https://eugeneyan.com/writing/llm-patterns/)). Seção "Guardrails".

## Veja também

- [[02 - JSON Schema como contrato]] — a linguagem que descreve a "função" fake
- [[04 - OpenAI Structured Outputs — strict mode]] — alternativa nativa da OpenAI
- [[05 - Anthropic tool use para forçar formato]] — como Anthropic implementa o padrão
- [[03-Dominios/Tecnologia/IA/Anatomia de Agents/02 - O loop ReAct e native tool use|Anatomia de Agents — Loop ReAct]] — o caso geral
- [[MCP]] — protocolo que expõe tools externamente
