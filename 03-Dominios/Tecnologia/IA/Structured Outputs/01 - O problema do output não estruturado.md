---
title: "01 - O problema do output não estruturado"
created: 2026-05-28
updated: 2026-06-28
type: concept
status: seedling
progress: in_progress
fase: iniciado
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
> LLMs são funções estocásticas com saída não tipada. Você pede JSON, vem markdown com ```` ```json ```` em volta, campo faltando, vírgula sobrando, chave alucinada que nunca foi pedida. Pedir JSON via prompt funciona em 95% dos casos. O sistema quebra nos outros 5%. Estruturar output não é detalhe de UX, é a forma de recriar contrato de tipo na borda entre LLM e código. Esta nota explica por que o problema existe, por que ele é mais grave do que parece, e quando é OK conviver com texto livre.

> [!question]- O que eu preciso saber antes de ler isso?
> Você já entende o básico de como prompts funcionam — que o modelo gera texto token por token, e que instruções no prompt aumentam a probabilidade de determinados outputs mas não garantem nada. Essa nota parte daí: quando o output do LLM vai ser consumido por código (um parser, uma pipeline, um agente), "maior probabilidade" não basta. Você precisa de garantias. Se você já tentou extrair JSON de um LLM e teve que escrever código de limpeza, você já encontrou o problema desta nota.

## O problema em uma linha

Você pede JSON. O modelo gera texto que *parece* JSON. O parser discorda — às vezes, nos inputs mais complexos, nos momentos mais inconvenientes.

A distinção que importa: "parece JSON" é probabilidade. "É JSON válido dentro do schema esperado" é garantia. Sistemas de produção precisam de garantias.

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

1. **Wrapper de markdown**: o JSON vem cercado de ```` ```json ```` apesar do prompt pedir "apenas". Seu parser quebra na primeira linha.
2. **Texto em volta**: saudação antes, despedida depois. Você pode aparar, mas precisa de regex robusto.
3. **Vírgula sobrando**: JSON estrito não aceita trailing comma. Python aceita; JS não. Seu serviço falha em ambiente diferente do dev.
4. **Tipos errados**: `valor` veio como string formatada (`"R$ 1.234,56"`), não número. Você esperava `1234.56`. Operações aritméticas explodem.
5. **Data ambígua**: `15/03/2026` é 15 de março (PT-BR) ou 3 de maio (EN-US)? Sem schema, qualquer um.

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

Resultado: dá pra subir a taxa de sucesso de 95% pra 99% afiando o prompt. Mas pra chegar nos 99.99% que pipeline de produção exige, você precisa de um mecanismo que **force** o modelo a aderir ao schema, não convença ele educadamente. Isso é structured outputs (notas 04-06).

> [!note] A diferença entre teste e produção
> Esse problema é quase invisível em testes manuais porque o desenvolvedor escolhe os casos de teste e, inconscientemente, testa os inputs que o modelo gerencia bem. A taxa de falha real aparece em produção, com inputs de usuários reais — mais ambíguos, mais longos, mais inesperados. Por isso o problema frequentemente é "descoberto" quando o sistema já está em produção e alguém reclama de um erro estranho.

## Taxonomia de falhas de output

Os cinco problemas do exemplo de fatura não são aleatórios — eles pertencem a categorias estáveis de falha. Conhecer a taxonomia ajuda a escolher a solução certa:

| Categoria | Exemplo | Solução |
|---|---|---|
| **Envelope indesejado** | ```` ```json ```` em volta do JSON | Enforcement de output format |
| **Texto decorativo** | Saudação antes e depois do JSON | Output format + constraint declarativa |
| **JSON malformado** | Trailing comma, aspas quebradas | Schema enforcement com retry |
| **Tipo errado** | Número como string formatatada | JSON Schema com `type: number` |
| **Campo alucinado** | Campo extra não pedido | Schema com `additionalProperties: false` |
| **Campo faltando** | Campo obrigatório ausente | Schema com `required: [...]` |
| **Semântica incorreta** | Valor valid dentro do shape mas errado | Validação pós-schema (nota 07) |

As categorias 1-6 são problemas de *forma* — o schema resolve. A categoria 7 é problema de *conteúdo* — precisa de lógica de validação semântica. As notas seguintes cobrem o schema (02) e depois o mecanismo por provider (03-06) e depois a validação semântica (07).

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

## Por que o problema piora com temperatura e volume

Dois multiplicadores do problema que engenheiros descobrem na prática:

**Temperatura:** com `temperature=0`, os modelos seguem as instruções de formato com mais consistência. Mas `temperature=0` não é 100% determinístico em todos os provedores, e não é adequado para todas as tarefas (geração criativa, diversidade, etc.). Em sistemas que precisam de temperatura alta, a taxa de falha de formato sobe.

**Volume:** uma taxa de 2% de falha parece aceitável. Em 100 chamadas, são 2 erros — fácil de tratar com retry manual. Em 100.000 chamadas/dia, são 2.000 erros/dia. Cada erro que não é capturado é dado corrompido ou request que falhou silenciosamente. A matemática de falha em escala muda o que "aceitável" significa.

O enforcement via API resolve os dois: o modelo não tem liberdade de emitir tokens fora do schema, independente de temperatura. E o enforcement acontece antes da resposta chegar ao código chamador, então o volume não afeta a taxa de erro visível ao sistema.

## Quando o problema é crítico vs quando é OK

Nem todo uso de LLM precisa de structured output. Heurística:

| Cenário | Output não estruturado é OK? |
|---|---|
| Resposta de chatbot mostrada ao humano | Sim, texto é o produto |
| Brainstorming, drafts, exploração | Sim, estrutura atrapalha |
| Sumarização que vai pra pessoa | Sim, markdown serve |
| Fatura extraída pra ir pro banco | **Não**: precisa de schema |
| Classificação que vira label em ML pipeline | **Não**: precisa de enum validado |
| Decisão de roteamento de agente | **Não**: precisa de tipo confiável |
| Resposta de função de tool (agente) | **Não**: precisa de schema |
| Input pra outro LLM downstream | **Talvez**, depende se downstream parsea ou consome texto |

A regra: **se o output vai ser consumido por código, structured. Se vai ser consumido por humano, livre.** Cinza só na fronteira (output que humano lê **e** sistema parsea — relatórios, dashboards). Nesses casos, normalmente vale gerar duas versões — uma livre pro humano, uma estruturada pro sistema — ou um structured com um campo `markdown_summary` dentro.

## Armadilhas comuns

> [!warning] Parser defensivo cresce sem parar e esconde drift
> A reação natural quando o modelo não respeita "retorne apenas JSON" é escrever um parser defensivo que conserta a saída. O parser começa com 10 linhas e em seis meses tem 200, com heurísticas empilhadas para cada bug de produção. O problema mais sério: quando o parser conserta sozinho, você nunca vê que o modelo está se desviando. Drift silencioso de qualidade vira regressão que você descobre tarde. Parser defensivo é gambiarra; structured output enforcement é a solução.

> [!warning] "Apenas JSON" no prompt não é garantia em produção
> "Retorne apenas JSON, sem explicações" funciona em 95-98% dos casos com modelos bons. O sistema quebra nos outros 2-5% — que em produção com 10.000 chamadas/dia é 200-500 falhas. E as falhas acontecem nos casos mais complexos de input, exatamente onde você mais precisa de confiabilidade. Pedir "apenas JSON" melhora a taxa; enforcement via API (strict mode, tool use, response schema) é o que faz a taxa chegar perto de 100%.

> [!warning] Campo alucinado é mais grave do que campo faltando
> Quando um campo obrigatório está faltando, o erro é visível — o parser quebra com KeyError. Quando o modelo adiciona um campo que não foi pedido (um `observacao` que você não esperava), o objeto parsea com sucesso mas carrega dado não solicitado. Dependendo do consumidor downstream, isso quebra silenciosamente (campo ignorado) ou contamina (campo injetado em local errado). Validação de schema que apenas verifica a presença de campos obrigatórios não captura essa categoria de erro; você precisa de validação que rejeita campos extras também.

## A reframing certa

A pergunta não é *"como eu faço o LLM retornar JSON?"*. É:

> *"Como eu transformo a saída textual e probabilística do LLM num objeto tipado e validado antes do próximo passo?"*

A resposta tem três partes:

1. **Schema** como contrato declarativo (nota 02).
2. **Mecanismo de enforcement** que o provider oferece — strict mode, tool use, response schema (notas 03-06).
3. **Validação semântica** em cima do shape garantido, com retry quando algo está fora (nota 07).

O resto da trilha é isso, ramificado.

Uma forma alternativa de enquadrar: a borda entre LLM e código é sempre uma borda de desconfiança. Do lado do LLM, tudo é texto probabilístico. Do lado do código, tudo precisa ser tipado e previsível. O mecanismo de structured output é a alfândega nessa fronteira — o que passa precisa satisfazer o schema, ou é retido.

> [!tip] Por que isso importa mais do que parece
> Sistemas LLM que "funcionam bem em teste mas quebram em produção" quase sempre têm um parser defensivo insuficiente ou ausência de enforcement de schema. A diferença entre 98% de sucesso e 99.9% de sucesso não é uma melhora incremental — é a diferença entre "tolerável com monitoramento" e "pode rodar sem supervisão constante".

## Detectar o problema em produção

Diagnóstico antes de refatorar: se você já tem um sistema com LLM e quer saber se o problema de output não estruturado está presente, os sinais estão no código e nos logs.

**Sinais no código:**
- Presença de funções como `clean_json()`, `extract_json()`, `parse_llm_response()` — parser defensivo em ação
- Blocos `try/except json.JSONDecodeError` com múltiplas tentativas aninhadas
- Regex para extrair texto entre ```` ``` ```` e ```` ``` ````
- Código que acessa campos com `.get("campo", valor_default)` em vez de acesso direto
- Validação manual de tipo: `if isinstance(result["valor"], str): result["valor"] = float(result["valor"].replace(",", ".")`

**Sinais em logs:**
- Erros de JSON parsing que somem após retry automático — sinal de falha intermitente mascarada
- Logs de "campo ausente, usando default" — dado estrutural sendo ignorado silenciosamente
- Aumento de erros associado a inputs mais longos ou complexos — correlação típica do problema de geração

**Métricas de baseline:**
Antes de migrar para enforcement de schema, meça: taxa de falha de parse, distribuição de falhas por tipo (envelope, malformed, campo faltando), e tempo gasto em retry. Essas métricas são o argumento para a mudança e o baseline para confirmar melhora depois.

## Por que o problema piora com agentes

Em pipelines LLM simples (usuário → LLM → usuário), output não estruturado é inconveniente. Em sistemas agênticos, é falha em cascata.

Quando um agente chama uma ferramenta, o output da chamada (o resultado do LLM) vira o input da ferramenta. Se esse output não tem o formato certo, a ferramenta falha. Em loops agênticos, o agente pode tentar de novo, mas sem enforcement, tentativas repetidas produzem a mesma distribuição de outputs — incluindo os malformados. O loop entra em ciclo de falha.

As notas 03-06 cobrem como os provedores resolvem isso no nível de API: a resposta do LLM é validada contra um schema antes de ser devolvida ao chamador. Se não validar, o modelo tenta de novo internamente — sem que o código de chamada precise saber. Esse é o mecanismo que torna structured outputs uma solução real, não uma melhora marginal.

O contraste com o pipeline simples fica claro na matemática de propagação de erro. Se cada etapa de uma pipeline de 3 LLMs tem 98% de sucesso de formato, a pipeline completa tem `0.98 × 0.98 × 0.98 ≈ 94.1%` de sucesso. Com enforcement, cada etapa fica próxima de 100%, e a pipeline composta mantém essa confiabilidade. Agentes complexos com 5-10 steps de LLM precisam de enforcement em cada ponto, não só na entrada ou na saída final.

**Sinal de alerta em design agêntico:** se você está planejando escrever código de retry em cima do output do agente porque "às vezes não vem no formato certo", o problema está no nível errado. O retry deveria acontecer dentro do modelo via enforcement, não em lógica de aplicação.

## Quando structured outputs não resolvem tudo

Enforcement de schema resolve o problema de *forma*, não o problema de *conteúdo*. O campo `vencimento` vai existir e vai ser uma string no formato ISO 8601 — mas se o modelo extraiu a data errada, o schema não captura isso. Você vai receber `{"vencimento": "2026-04-15"}` quando a data correta é `2026-03-15`, e o schema vai considerar válido.

Isso não é uma limitação a esconder — é onde entra a validação semântica (nota 07). O pipeline completo é:

```
texto livre → [schema enforcement] → output tipado → [validação semântica] → output confiável
```

Saltar a segunda etapa porque a primeira dá conforto é um equívoco comum. Schema enforcement é necessário mas não suficiente. A nota 07 cobre o que fazer com output que passou no schema mas suspeito de erro semântico: validação com regras de negócio, cross-check com dados externos, e retry com feedback direcionado ao modelo.

## Como explicar em inglês

Em entrevistas sobre sistemas de IA, a questão de structured outputs aparece tanto em design de sistemas quanto em debugging de produção:

> "The fundamental problem is that LLMs are probabilistic text generators, not typed functions. When you need the output to be consumed by code — a parser, an agent, a downstream pipeline — you can't rely on 'please return only JSON' in the prompt. That gets you 95-98% compliance, and 2-5% failures that happen precisely when inputs are complex. Structured output enforcement via provider APIs — strict mode, tool use, response schemas — is what closes that gap to near-100%, without brittle regex parsers."

| Português | Inglês |
|-----------|--------|
| output não estruturado | unstructured output / free-text output |
| saída tipada | typed output |
| schema de output | output schema |
| campo alucinado | hallucinated field / extra field |
| parser defensivo | defensive parser / error-handling parser |
| enforcement de schema | schema enforcement |
| validação de output | output validation |
| trailing comma | trailing comma |
| tipo errado | wrong type / type mismatch |
| consumidor downstream | downstream consumer |

## O que vem a seguir

Você já sabe por que pedir JSON no prompt não basta. A próxima nota resolve a linguagem: como escrever o contrato que o modelo vai respeitar — JSON Schema, a forma padrão de descrever shape, tipos, restrições e defaults.

Ver [[02 - JSON Schema como contrato]].

## Checklist antes de seguir

Antes de continuar para JSON Schema (nota 02), certifique-se de que você:

- [ ] Consegue nomear pelo menos 3 categorias de falha de output (taxonomia da nota)
- [ ] Entende por que `temperature=0` não elimina o problema
- [ ] Sabe identificar parser defensivo no código (os sinais de diagnóstico)
- [ ] Conhece a distinção entre falha de forma (schema resolve) e falha de conteúdo (validação semântica)
- [ ] Sabe em quais cenários output não estruturado é OK

Se algum item ficou obscuro, releia a seção correspondente antes de avançar.

## Fontes

- **@hooeem** — *Become an AI Engineer*, cap #6. Posição "structured outputs is the boundary that turns text into types".
- **Eugene Yan** — *Patterns for Building LLM-based Systems & Products* ([eugeneyan.com](https://eugeneyan.com/writing/llm-patterns/)). Seção sobre "Guardrails" cobre validação de output.
- **Anthropic** — *Tool use overview* ([docs.anthropic.com](https://docs.anthropic.com/en/docs/build-with-claude/tool-use/overview)). Posicionamento de tool use como mecanismo de structured output.

## Veja também

- [[02 - JSON Schema como contrato]] — a linguagem padrão pra escrever o schema
- [[03 - Function calling como mecanismo de output]] — o mecanismo principal de enforcement
- [[07 - Validação e retry — Pydantic, Zod]] — o que fazer quando shape está OK mas semântica não
- [[03-Dominios/Tecnologia/IA/AI Engineering Stack/05 - Output Layer|AI Engineering Stack — Output Layer]] — a camada arquitetural correspondente
- [[Dicionário de IA#structured output|Dicionário: structured output]]
