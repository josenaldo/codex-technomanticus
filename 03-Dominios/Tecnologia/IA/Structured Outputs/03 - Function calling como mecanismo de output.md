---
title: "03 - Function calling como mecanismo de output"
created: 2026-05-28
updated: 2026-05-28
type: concept
status: seedling
progress: in_progress
fase: Iniciado
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

> [!question]- O que eu preciso saber antes de ler isso?
> Você sabe o que é JSON Schema (nota 02) — tipos, `properties`, `required`, `enum`, `additionalProperties`. E você entende por que "pedir JSON no prompt" não é enforcement de verdade (nota 01). Esta nota apresenta o mecanismo mais confiável de fazer o provider garantir o schema: transformar seu output desejado em "uma ferramenta que o modelo vai chamar". Se você já usou function calling / tool use no contexto de agentes, o que muda aqui é só o enquadramento: a ferramenta não executa nada, ela é só o schema do output. Se você nunca viu function calling, a nota introduz o conceito do zero.

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

## Por que o nome e a descrição da tool importam

Ao contrário do que parece, a tool não é só um schema — o modelo lê o `name` e `description` como parte do contexto semântico. Isso tem efeitos práticos:

- **Nome influencia o que o modelo coloca nos campos.** Uma tool chamada `extract_invoice` faz o modelo pensar em dados de fatura. A mesma com campos idênticos chamada `get_info` tem desempenho ligeiramente pior porque o frame contextual é genérico.
- **Descrição orienta o preenchimento.** Escreva `description` como instrução, não como documentação: `"Chame esta ferramenta para retornar sua análise estruturada. Nunca responda em texto livre."` Em vez de: `"Ferramenta que retorna análise estruturada."`.
- **Descrições de campo complementam o schema.** Adicione `description` em cada propriedade para guiar o preenchimento. `"confidence": { "type": "string", "enum": ["low", "medium", "high"], "description": "Confiança na resposta: low se dados insuficientes, high se bem estabelecido." }` produz resultados mais consistentes.

O modelo não é um parser de JSON Schema — ele é um gerador de texto que lê o schema como contexto natural. Trate a tool como você trataria um prompt: escolha palavras com cuidado.

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

## A anatomia de uma chamada tool use bem sucedida

Entender o que acontece internamente ajuda a debugar e a escolher parâmetros certos:

1. **Definição de tool no request:** O provider recebe `tools: [...]` junto com o `messages`. A lista é tokenizada e vai para o contexto do modelo — você paga por isso como input tokens. Para um schema típico de 5 campos, adicione ~100-200 tokens de input.

2. **Raciocínio do modelo (interno):** O modelo processa o prompt, entende o que precisa retornar, e "decide" (deterministicamente, dada a configuração) chamar a tool. Com `tool_choice` forçado, essa decisão é compulsória.

3. **Emissão do tool_use block:** O modelo emite um bloco estruturado com `name` e `input` (o JSON com os campos). O provider intercepta antes de entregar ao chamador.

4. **Validação no provider:** O provider valida `input` contra o schema da tool. Em strict mode, valida rigorosamente e regenera se inválido. Em modos padrão, pode entregar mesmo com pequenas inconsistências.

5. **Entrega ao chamador:** Você recebe `response.content` com um ou mais blocks, incluindo o `tool_use` block. Você extrai `block.input` — é o seu structured output, um dict Python (ou objeto JS) pronto pra usar.

O ponto crítico: a validação acontece no provider, não no seu código. Você não precisa escrever o parser. Esse é o ganho.

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

## Diagnóstico quando tool use falha

Mesmo com `tool_choice` forçado, há cenários de falha. Saber diagnosticar rapidamente é parte da habilidade:

**`stop_reason != "tool_use"`:** O modelo encerrou sem chamar a tool. Causas: input muito longo que cortou a definição da tool, modelo que não suporta tool use no modo usado, conflito entre system prompt e tool choice. Verifique se a definição da tool chegou no contexto e se o modelo suporta tools na configuração usada.

**`tool_use.input` fora do schema:** O provider não validou (modo não-strict) ou validou mas o modelo regenerou algo diferente do esperado. Em modo strict isso não deveria acontecer. Em modo não-strict, adicione validação com Pydantic ou Zod antes de usar o output.

**Tool chamada com argumentos vazios:** O modelo chamou a tool mas preencheu os campos com strings vazias ou arrays vazios que não deveriam estar vazios. Isso é semanticamente errado mas sintaticamente válido — schema enforcement não captura. Adicione `minLength` em strings críticas ou validação de negócio pós-schema.

**Modelo chama a tool mas também responde em texto:** Em alguns providers e modos, o modelo pode emitir um bloco de texto antes do tool_use block. Isso é normal em modos não-strict — apenas ignore o texto e processe o tool_use. Se você não quer texto algum, instrua no system prompt: `"Responda exclusivamente via tool. Não emita texto livre."`.

## Trade-offs

### Latência

Tool use adiciona overhead — o provider precisa validar schema, e em strict mode, regenerar se inválido. Tipicamente +50-200ms vs texto livre. Em alta vazão, isso conta.

### Custo

Tokens extras: definição da tool entra como input (cobrado), tool_use block tem overhead estrutural. Pra um schema típico de 5 campos, espere +30-80 tokens input + +10-30 output. Em pipelines de alta frequência, otimize a descrição da tool.

### Debug

Quando algo dá errado, você precisa olhar dois lugares: o `stop_reason` (foi `tool_use` mesmo?) e o `tool_use.input`. Texto livre é mais fácil de debugar.

### Modelos pequenos

Modelos pequenos (Haiku, Flash, Mini) são piores em tool use do que em texto. Pra structured output sem tool, eles podem ir melhor com modo nativo (response_format / response_schema). Teste antes de assumir.

## Armadilhas comuns

> [!warning] Não forçar `tool_choice` — o modelo escolhe quando chamar
> O erro mais comum ao usar tool use pra structured output é esquecer de forçar `tool_choice`. Sem ele, o modelo decide por conta própria se chama a tool ou responde em texto livre. Em prompts ambíguos ou inputs que "não parecem precisar de tool", o modelo vai direto pro texto — e você volta ao problema original. Sempre use `tool_choice: {"type": "tool", "name": "nome_da_tool"}` em chamadas de structured output.

> [!warning] Usar modelo pequeno sem testar aderência a tool use
> Modelos menores (Haiku, Flash, Mini) têm aderência a tool use mais fraca do que modelos maiores. Em testes com prompts simples, funcionam bem; com inputs complexos ou schemas grandes, a taxa de falha sobe. Se você usar Pattern B (modelo barato estrutura o output do modelo caro), teste a aderência do modelo barato especificamente com o schema mais complexo que vai aparecer em produção — não com o caso feliz.

> [!warning] Nomear a ferramenta de forma genérica (`get_output`, `response`, `result`)
> O nome e a descrição da tool influenciam o comportamento do modelo — ele infere do nome o que a tool faz. Nomes genéricos como `get_output` ou `return_json` não ajudam o modelo a entender o contexto. Use nomes semânticos que descrevem o que o output *é*: `record_invoice_data`, `classify_support_ticket`, `extract_medical_entities`. A descrição também importa: explique que o modelo deve chamar a tool pra retornar a resposta no formato esperado, não só liste os campos.

## Como explicar em inglês

Em design reviews e entrevistas, a pergunta sobre como garantir output estruturado de LLM é comum — e saber que tool use é um mecanismo (não só uma feature de agentes) diferencia respostas sênior:

> "Function calling is the most reliable mechanism for structured output across all major providers. The flip: instead of defining tools the model can call to interact with the world, you define a single dummy tool whose schema is exactly the output you want. Force the model to call it via `tool_choice`, and the provider validates the output against the schema before returning it to you. The 'function' never executes — it's just a contract with a name."

| Português | Inglês |
|-----------|--------|
| chamada de função | function call / function calling |
| uso de ferramenta | tool use |
| schema de input da tool | tool input schema |
| forçar tool_choice | force tool_choice |
| ferramenta de finalização | finalization tool |
| bloco de tool_use | tool_use block |
| argumento da ferramenta | tool argument / tool input |
| overhead de latência | latency overhead |
| denominador comum entre providers | cross-provider denominator |
| modelo barato estrutura | cheaper model structures |

## O que vem a seguir

Você entende o mecanismo de base — transformar output em tool fake. Agora vem a implementação por provider: a OpenAI tem uma API dedicada de structured output (strict mode) que simplifica o padrão em alguns casos. A nota 04 cobre as especificidades do strict mode, o que o subset de JSON Schema suportado inclui e exclui, e quando preferir strict mode vs tool use na OpenAI.

Ver [[04 - OpenAI Structured Outputs — strict mode]].

## Conexões

> [!tip] Onde esse padrão aparece em outras notas
> O padrão tool-como-structured-output aparece em vários galhos do domínio IA com nomes diferentes: em Memória de Agentes, o extraction step que estrutura memórias usa tool forçada; em RAG, o query refinement às vezes usa tool pra forçar estrutura de query; em MCP, o protocolo inteiro é baseado em tools com schemas. Quando você vê "JSON Schema" + "tool" em contextos distintos, é o mesmo mecanismo com nome diferente.

Esse mecanismo é o mesmo que [[MCP]] usa pra expor tools de fora — você só descreve schemas, o cliente decide chamar. E o loop ReAct ([[03-Dominios/Tecnologia/IA/Anatomia de Agents/02 - O loop ReAct e native tool use|loop ReAct e native tool use]]) é o caso geral onde múltiplas chamadas de tool encadeiam; structured output é o caso degenerado de uma única chamada, forçada.

## Checklist de implementação

Antes de ir pra produção com tool use como structured output:

- [ ] Tool tem nome semântico (não `get_output` ou `response`)
- [ ] Tool tem `description` que instrui o modelo a chamar ela pra retornar
- [ ] Cada campo tem `description` que orienta o preenchimento
- [ ] `additionalProperties: false` está no schema
- [ ] Todos os campos críticos estão em `required`
- [ ] `tool_choice` está forçado pro nome da tool
- [ ] Código extrai de `tool_use` blocks, não do texto livre
- [ ] Validação semântica existe pós-extração (Pydantic/Zod ou regras manuais)
- [ ] Caso de `stop_reason != "tool_use"` é tratado (log + fallback)
- [ ] Schema testado com inputs de produção, não só casos felizes

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
- [[07 - Validação e retry — Pydantic, Zod]] — o que validar depois que o schema garantiu a forma
