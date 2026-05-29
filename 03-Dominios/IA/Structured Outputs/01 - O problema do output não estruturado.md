---
title: "01 - O problema do output não estruturado"
created: 2026-05-28
updated: 2026-05-28
type: concept
status: seedling
progress: in_progress
tags:
  - structured-outputs
  - ia
  - problema
publish: true
aliases:
  - Output não estruturado
  - Por que JSON via prompt falha
---

# 01 - O problema do output não estruturado

> [!abstract] TL;DR
> LLMs são funções estocásticas com saída não tipada. Você pede JSON, vem markdown com ```` ```json ```` em volta, campo faltando, vírgula sobrando, chave alucinada que nunca foi pedida. Pedir JSON via prompt funciona em 95% dos casos — e o sistema quebra nos outros 5%. Estruturar output não é detalhe de UX, é a forma de recriar contrato de tipo na borda entre LLM e código. Esta nota explica por que o problema existe, por que ele é mais grave do que parece, e quando é OK conviver com texto livre.

## O cenário real

Você pediu pra extrair uma fatura em JSON. O prompt diz:

> *"Extraia os dados da fatura abaixo e retorne em JSON com os campos `valor`, `vencimento`, `fornecedor`. Retorne **apenas** o JSON, sem explicações."*

E o que vem de volta, ao longo de mil execuções, inclui variações como:

```text
Aqui está o JSON com os dados extraídos:

```json
{
  "valor": "R$ 1.234,56",
  "vencimento": "15/03/2026",
  "fornecedor": "Acme S.A.",
}
```

Espero ter ajudado!
```

Esse exemplo tem cinco problemas técnicos empilhados, e nenhum é raro:

1. **Wrapper de markdown** — o JSON vem cercado de ```` ```json ```` apesar do prompt pedir "apenas". Seu parser quebra na primeira linha.
2. **Texto em volta** — saudação antes, despedida depois. Você pode aparar, mas precisa de regex robusto.
3. **Vírgula sobrando** — JSON estrito não aceita trailing comma. Python aceita; JS não. Seu serviço falha em ambiente diferente do dev.
4. **Tipos errados** — `valor` veio como string formatada (`"R$ 1.234,56"`), não número. Você esperava `1234.56`. Operações aritméticas explodem.
5. **Data ambígua** — `15/03/2026` é 15 de março (PT-BR) ou 3 de maio (EN-US)? Sem schema, qualquer um.

E em 1 em cada 200 execuções, ainda aparece a categoria mais perversa:

```json
{
  "valor": 1234.56,
  "vencimento": "2026-03-15",
  "fornecedor": "Acme S.A.",
  "observacao": "Pagamento via boleto"
}
```

Veio um campo `observacao` que ninguém pediu. O modelo alucinou um campo que ele achou útil. Seu schema downstream não tem esse campo, e dependendo do consumidor, isso quebra silenciosamente — ou pior, é ignorado e dados relevantes somem.

## Por que "pedir JSON no prompt" não basta

A causa raiz é a natureza do próprio LLM:

- **Geração é probabilística.** Mesmo com `temperature=0`, mudanças mínimas no prompt, no modelo, ou no contexto deslocam a distribuição. O modelo *tende* a obedecer "retorne apenas JSON", mas a probabilidade de obedecer não é 1.
- **O modelo foi treinado em texto humano.** Textos humanos quase sempre vêm com introdução, conclusão, hedge. "Apenas JSON" contraria milhões de exemplos do corpus de treino.
- **A instrução compete com outras instruções.** Quanto mais coisas você pede no prompt, menor a probabilidade de cada uma ser respeitada. "Apenas JSON" entra na fila com "campos completos", "datas em ISO", "valores numéricos".
- **Não há mecanismo de validação interna.** O modelo não roda um parser antes de emitir. Ele emite token por token; se na metade ele "lembrou" de explicar, ele explica.

Resultado: dá pra subir a taxa de sucesso de 95% pra 99% afiando o prompt. Mas pra chegar nos 99.99% que pipeline de produção exige, você precisa de um mecanismo que **force** o modelo a aderir ao schema — não convença ele educadamente. Isso é structured outputs (notas 04-06).

## O custo de parsers defensivos

A reação comum é blindar o parser. Algo como:

```python
def parse_llm_json(text: str) -> dict:
    # Tenta direto
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Extrai bloco markdown
    match = re.search(r"```(?:json)?\s*(.*?)```", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass

    # Remove trailing commas
    cleaned = re.sub(r",(\s*[}\]])", r"\1", text)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    # Última tentativa — extrai primeiro `{...}`
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return json.loads(match.group(0))

    raise ValueError(f"Não consegui parsear: {text[:200]}")
```

Esse parser existe em quase todo projeto LLM legado. Os problemas:

- **Cresce sem parar.** Cada bug em produção vira uma nova heurística. Em seis meses tem 200 linhas e ninguém entende.
- **Esconde o sintoma.** Quando o parser conserta sozinho, você nunca vê que o modelo está se desviando. Drift silencioso vira regressão de qualidade.
- **Não resolve o problema de chave alucinada.** Você parsea com sucesso e passa adiante um objeto com campo a mais.
- **Custo computacional.** Em pipelines de alta vazão, regex e múltiplos `json.loads` custam.

Structured outputs eliminam essa categoria de código. Em vez de consertar a saída ruim, força o modelo a emitir saída boa.

## Quando o problema é crítico vs quando é OK

Nem todo uso de LLM precisa de structured output. Heurística:

| Cenário | Output não estruturado é OK? |
|---|---|
| Resposta de chatbot mostrada ao humano | Sim — texto é o produto |
| Brainstorming, drafts, exploração | Sim — estrutura atrapalha |
| Sumarização que vai pra pessoa | Sim — markdown serve |
| Fatura extraída pra ir pro banco | **Não** — precisa de schema |
| Classificação que vira label em ML pipeline | **Não** — precisa de enum validado |
| Decisão de roteamento de agente | **Não** — precisa de tipo confiável |
| Resposta de função de tool (agente) | **Não** — precisa de schema |
| Input pra outro LLM downstream | **Talvez** — depende se downstream parsea ou consome texto |

A regra: **se o output vai ser consumido por código, structured. Se vai ser consumido por humano, livre.** Cinza só na fronteira (output que humano lê **e** sistema parsea — relatórios, dashboards). Nesses casos, normalmente vale gerar duas versões — uma livre pro humano, uma estruturada pro sistema — ou um structured com um campo `markdown_summary` dentro.

## A reframing certa

A pergunta não é *"como eu faço o LLM retornar JSON?"*. É:

> *"Como eu transformo a saída textual e probabilística do LLM num objeto tipado e validado antes do próximo passo?"*

A resposta tem três partes:

1. **Schema** como contrato declarativo (nota 02).
2. **Mecanismo de enforcement** que o provider oferece — strict mode, tool use, response schema (notas 03-06).
3. **Validação semântica** em cima do shape garantido, com retry quando algo está fora (nota 07).

O resto da trilha é isso, ramificado.

## Fontes

- **@hooeem** — *Become an AI Engineer*, cap #6. Posição "structured outputs is the boundary that turns text into types".
- **Eugene Yan** — *Patterns for Building LLM-based Systems & Products* ([eugeneyan.com](https://eugeneyan.com/writing/llm-patterns/)). Seção sobre "Guardrails" cobre validação de output.
- **Anthropic** — *Tool use overview* ([docs.anthropic.com](https://docs.anthropic.com/en/docs/build-with-claude/tool-use/overview)). Posicionamento de tool use como mecanismo de structured output.

## Veja também

- [[02 - JSON Schema como contrato]] — a linguagem padrão pra escrever o schema
- [[03 - Function calling como mecanismo de output]] — o mecanismo principal de enforcement
- [[07 - Validação e retry — Pydantic, Zod]] — o que fazer quando shape está OK mas semântica não
- [[AI Engineering Stack/05 - Output Layer|AI Engineering Stack — Output Layer]] — a camada arquitetural correspondente
- [[Dicionário de IA#structured output|Dicionário: structured output]]
