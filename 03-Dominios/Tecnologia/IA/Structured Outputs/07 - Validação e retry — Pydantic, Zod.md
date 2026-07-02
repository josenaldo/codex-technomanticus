---
title: "07 - Validação e retry — Pydantic, Zod"
created: 2026-05-28
updated: 2026-07-02
type: concept
status: seedling
progress: in_progress
fase: Iniciado
tags:
  - structured-outputs
  - ia
  - validacao
publish: true
aliases:
  - Pydantic validators
  - Zod refinements
  - Retry with feedback
---

# 07 - Validação e retry — Pydantic, Zod

> [!abstract] TL;DR
> Provider garante **shape** (campos certos, tipos certos). Não garante **semântica** — um campo `email` pode vir com texto que não é email, um `cnpj` pode vir com 14 caracteres mas dígitos verificadores errados. Pydantic (Python) e Zod (TypeScript) cobrem essa camada com validators/refinements customizados. Quando algo escapa, o padrão é **retry-with-feedback**: passa o erro de validação de volta pro modelo na próxima iteração, com backoff exponencial e teto de retries. Depois disso, fallback (modelo maior, regra de negócio, intervenção humana). Esta é a parte que separa pipeline robusto de POC.

> [!question]- O que eu preciso saber antes de ler isso?
> Você passou pelas notas de enforcement de schema (03-06) e entende que providers como OpenAI, Anthropic e Gemini garantem que o output tem a forma certa — campos presentes, tipos corretos, enum respeitado. Esta nota trata da camada seguinte: quando o shape está correto mas o conteúdo pode estar errado. Se você usa Pydantic ou Zod no seu código Python/TypeScript atual, você já tem as ferramentas — o que muda é aplicar validators pra saída de LLM especificamente, e conectar isso com um loop de retry.

## Shape vs semântica — a distinção crítica

Strict mode da OpenAI, tool use forçado da Anthropic, response_schema do Gemini — todos garantem shape:

| Garantido (shape) | Não garantido (semântica) |
|---|---|
| Campo `email` existe | Conteúdo de `email` é um email |
| Tipo é `string` | String tem formato válido de email |
| Enum é um dos valores permitidos | Valor do enum é o certo pro contexto |
| Array tem itens do tipo certo | Array não está vazio quando deveria ter algo |
| `confidence` é "low"/"medium"/"high" | "high" é a confiança real (vs alucinação de "high") |

Toda lógica de negócio depende da segunda coluna. E o LLM, mesmo aderente ao shape, pode preencher mal.

Exemplos reais que aparecem em produção:

- `email` = `"contato@empresa"` (sem TLD)
- `cnpj` = `"00.000.000/0000-00"` (formato OK, dígitos verificadores 0)
- `data_nascimento` = `"2050-03-15"` (futuro)
- `valor` = `-1500.00` (negativo onde devia ser positivo)
- `prioridade` = `"high"` (mas o ticket pede info trivial)
- `tags` = `["urgente", "URGENTE", "Urgent"]` (duplicatas com case diferente)

Schema sozinho não pega nada disso. Você precisa de uma camada de validação semântica.

## Pydantic — Python

Pydantic é o padrão em Python. Validators ficam na classe, executam após o parsing inicial:

```python
from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Literal
from datetime import date
import re

class TicketAnalysis(BaseModel):
    priority: Literal["low", "medium", "high", "urgent"]
    summary: str = Field(min_length=10, max_length=500)
    estimated_hours: float = Field(gt=0, le=160)
    assignee_email: str
    tags: list[str] = Field(min_length=1, max_length=5)
    due_date: date | None = None

    @field_validator("assignee_email")
    @classmethod
    def email_must_have_domain(cls, v: str) -> str:
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(pattern, v):
            raise ValueError(f"Email inválido: {v}")
        return v.lower()

    @field_validator("tags")
    @classmethod
    def tags_unique_case_insensitive(cls, v: list[str]) -> list[str]:
        normalized = [t.lower().strip() for t in v]
        if len(set(normalized)) != len(normalized):
            raise ValueError("Tags com duplicatas (case-insensitive)")
        return normalized

    @field_validator("due_date")
    @classmethod
    def due_date_not_past(cls, v: date | None) -> date | None:
        if v is not None and v < date.today():
            raise ValueError(f"Due date no passado: {v}")
        return v

    @model_validator(mode="after")
    def urgent_requires_due_date(self) -> "TicketAnalysis":
        if self.priority == "urgent" and self.due_date is None:
            raise ValueError("Prioridade 'urgent' exige due_date")
        return self
```

Três níveis aqui:

1. **Field constraints embutidos** (`min_length`, `gt`, `le`) — declarativos, lidos como contrato.
2. **`field_validator`** — lógica custom por campo (formato de email, normalização de case).
3. **`model_validator`** — regras entre campos (urgente exige due_date).

Quando o LLM retorna algo que falha, Pydantic levanta `ValidationError` com mensagem detalhada. Essa mensagem é o que vai pro retry.

## Zod — TypeScript

Zod é o equivalente em TS. Refinements jogam o mesmo papel:

```typescript
import { z } from "zod";

const TicketAnalysis = z
  .object({
    priority: z.enum(["low", "medium", "high", "urgent"]),
    summary: z.string().min(10).max(500),
    estimated_hours: z.number().positive().max(160),
    assignee_email: z
      .string()
      .email("Email inválido")
      .transform((v) => v.toLowerCase()),
    tags: z
      .array(z.string())
      .min(1)
      .max(5)
      .refine(
        (tags) => {
          const normalized = tags.map((t) => t.toLowerCase().trim());
          return new Set(normalized).size === normalized.length;
        },
        { message: "Tags com duplicatas (case-insensitive)" }
      ),
    due_date: z
      .string()
      .date()
      .nullable()
      .refine(
        (d) => d === null || new Date(d) >= new Date(),
        { message: "Due date no passado" }
      ),
  })
  .refine(
    (data) => !(data.priority === "urgent" && data.due_date === null),
    { message: "Prioridade 'urgent' exige due_date" }
  );

type TicketAnalysis = z.infer<typeof TicketAnalysis>;

// Uso
const result = TicketAnalysis.safeParse(llmOutput);
if (!result.success) {
  const errorMessage = result.error.format();
  // passa pra retry
}
```

Padrão equivalente: declarativo no topo, refinements no fundo, model-level refinement no `.refine()` final.

## O pattern retry-with-feedback

A sacada operacional: quando validação falha, **passe a mensagem de erro de volta pro modelo** como parte do prompt da próxima chamada. O modelo é muito bom em corrigir quando recebe feedback específico.

```python
from pydantic import ValidationError
import time
import logging

def call_llm_structured(
    messages: list[dict],
    schema: type[BaseModel],
    max_retries: int = 3,
) -> BaseModel:
    last_error: Exception | None = None

    for attempt in range(max_retries):
        # Chama o LLM (assume helper que retorna dict do tool_use ou response_format)
        raw_output = call_llm_raw(messages, schema)

        try:
            return schema.model_validate(raw_output)
        except ValidationError as e:
            last_error = e
            logging.warning(
                f"Validação falhou (tentativa {attempt + 1}/{max_retries}): {e}"
            )

            # Backoff exponencial: 1s, 2s, 4s
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)

            # Adiciona feedback pro modelo
            messages = messages + [
                {"role": "assistant", "content": str(raw_output)},
                {"role": "user", "content": (
                    f"O output anterior falhou na validação:\n\n"
                    f"{e}\n\n"
                    f"Corrija e retorne o output válido."
                )}
            ]

    raise RuntimeError(
        f"Validação falhou após {max_retries} tentativas. "
        f"Último erro: {last_error}"
    )
```

Pontos importantes:

- **Mensagem de erro vai literal pro modelo.** Pydantic ValidationError é detalhada (qual campo, qual regra, qual valor). Vale passar inteira.
- **Mantém o output anterior na conversation.** O modelo precisa ver o que ele emitiu pra saber o que mudar.
- **Backoff exponencial.** Não martele o provider. Custos sobem rápido.
- **Teto de retries.** 3-5 tentativas. Mais que isso, o problema é estrutural — fallback.

## Backoff e rate limit

Além de backoff por validação, considere backoff por rate limit do provider:

```python
import time
from openai import RateLimitError, APIError

def with_retry(fn, max_retries: int = 5):
    for attempt in range(max_retries):
        try:
            return fn()
        except RateLimitError as e:
            wait = min(2 ** attempt, 60)  # cap em 60s
            time.sleep(wait)
        except APIError as e:
            if e.status_code >= 500:
                wait = min(2 ** attempt, 30)
                time.sleep(wait)
            else:
                raise
    raise RuntimeError("Excedeu retries")
```

Combine retry-de-validação com retry-de-rate-limit. Em produção, use libs maduras: `tenacity` (Python), `p-retry` (TS).

## Fallback — quando desistir

Depois do teto de retries, três opções típicas:

### 1. Escalar pra modelo maior

Se você estava em Haiku/Flash/Mini, retente em Sonnet/Pro/GPT-5:

```python
try:
    return call_llm_structured(messages, schema, model="claude-haiku-4-5")
except RuntimeError:
    return call_llm_structured(messages, schema, model="claude-sonnet-4-5")
```

Modelos maiores acertam mais o schema em casos complexos. Custo sobe, mas só pro caso difícil.

### 2. Cair em regra de negócio

Se a tarefa é classificação simples, regex/keywords podem cobrir o resto:

```python
def classify_priority_fallback(text: str) -> str:
    if re.search(r"urgent|down|broken|crítico", text, re.I):
        return "high"
    if re.search(r"asap|hoje|urgente", text, re.I):
        return "medium"
    return "low"
```

Não é elegante. Em produção, é frequente.

### 3. Mandar pra humano

Pipeline que vale a pena ter humano-no-loop quando IA falha:

```python
queue.send({
    "task": "structured_output_failed",
    "input": original_input,
    "last_error": str(last_error),
    "needs_review": True,
})
```

Decisões de alto risco (financeiro, jurídico, saúde) frequentemente preferem isso à automação completa.

## Boas práticas

### Loga tudo

Cada validação falha que vira retry é um sinal de drift ou prompt ruim. Acumule métricas: taxa de retry, qual schema falha mais, qual campo falha mais.

### Schema versionado

Quando você muda o schema, métricas históricas viram inválidas. Trate como contrato versionado.

### Não use validação como "fix"

Tentadora: usar `field_validator` pra "consertar" um output ruim (string com prefixo virar limpa). Faça isso só pra normalização (lowercase, trim). Pra correção de conteúdo, retry é melhor — você vê o problema.

### Rejeite campos extras — `extra="forbid"`

Por padrão, Pydantic ignora chaves que não estão no schema. Isso parece inofensivo até o LLM começar a "inventar" campos: um `internal_notes` que vazou de um exemplo do prompt, um `confidence_score` que o modelo achou que devia existir, um `debug` que sobrou de uma versão anterior do schema. Se o parser ignora silenciosamente, esses campos somem sem ninguém perceber — e você perde o sinal de que o modelo está desviando do contrato.

A correção é declarativa: trave o schema pra rejeitar qualquer campo fora da lista.

```python
from pydantic import BaseModel, ConfigDict

class TicketAnalysis(BaseModel):
    model_config = ConfigDict(extra="forbid")

    priority: Literal["low", "medium", "high", "urgent"]
    summary: str = Field(min_length=10, max_length=500)
    # ...demais campos
```

Com `extra="forbid"`, um campo extra vira `ValidationError` — e cai direto no loop de retry-with-feedback já descrito, com a mensagem indicando exatamente qual chave sobrou. Em Zod, o equivalente é `.strict()` no objeto (por padrão o Zod também descarta chaves desconhecidas, como o Pydantic). O ganho é o mesmo em ambos: campo extra deixa de ser ruído silencioso e vira erro visível, que você pode logar e investigar — muitas vezes é o primeiro sintoma de que o prompt ficou ambíguo ou o few-shot exemplifica um formato antigo.

### Valide o schema em ambiente de desenvolvimento

Um erro comum é só descobrir problema de schema em produção, quando o LLM já está gerando tráfego real. Vale rodar o schema contra um conjunto de exemplos conhecidos — inputs de teste com output esperado — antes de subir qualquer mudança de prompt ou de schema. Isso pega dois tipos de regressão: mudanças no schema que quebram parsing de outputs antigos (campo renomeado, tipo trocado), e mudanças no prompt que fazem o modelo desviar do formato esperado (um exemplo novo no prompt que "ensina" o modelo a incluir um campo que não devia existir). Trate o par prompt+schema como uma unidade testável: toda alteração em um dos dois roda a suíte de exemplos antes do deploy, do mesmo jeito que você rodaria testes unitários antes de mergear código.

## Armadilhas comuns

> [!warning] Passar o output com erro direto pra retry sem incluir o contexto original
> O retry-with-feedback funciona quando o modelo vê dois coisas: o que ele emitiu e o erro específico que gerou. Sem incluir o output anterior na conversa, o modelo não tem como saber o que precisa corrigir — vai gerar algo novo, não necessariamente melhor. A mensagem de retry deve sempre incluir o output anterior como turno de `assistant` e o erro de validação como novo `user` message. Omitir o output anterior torna o retry aleatório em vez de direcionado.

> [!warning] Usar validator para "silently fix" em vez de rejeitar
> É tentador usar `field_validator` para "consertar" outputs inválidos: remover o prefixo `"R$"` de um valor numérico, converter `"Sim"` para `True`, normalizar formato de data. Para normalização simples (lowercase, trim, format canônico), isso é OK. Para correção de conteúdo errado (email sem domínio, CNPJ inválido), fazer a correção no validator esconde o problema — o modelo nunca aprende o que errou, e você nunca vê o drift. Nesses casos, rejeite e faça retry.

> [!warning] Não ter teto de retries nem fallback
> Retry-with-feedback funciona bem para 2-3 tentativas. Depois disso, se o modelo continua falhando, o problema é estrutural: prompt ambíguo, schema que o modelo não consegue satisfazer, input impossível. Retry infinito fica circulando, consome tokens e latência sem convergir. Todo loop de retry precisa de: teto explícito, backoff exponencial, e um caminho claro de saída (escalar modelo, regra de negócio, fila humana). Sem isso, failure loops viram incidentes de custo.

## Como explicar em inglês

Em design reviews de sistemas LLM, a pergunta sobre validação semântica e retry é onde se separa "POC que funciona em teste" de "sistema que roda em produção":

> "Schema enforcement — strict mode, forced tool use — guarantees shape. It doesn't guarantee semantics. A Pydantic or Zod validator is the layer that checks business rules: email format, numeric ranges, cross-field constraints. When validation fails, the pattern is retry-with-feedback: pass the failed output and the error message back to the model in the next call. Models are very good at self-correction when they have specific feedback. After 3-5 retries with exponential backoff, you fall back — scale to a larger model, apply a business rule, or route to a human queue."

| Português | Inglês |
|-----------|--------|
| validação semântica | semantic validation |
| validator de campo | field validator |
| restrição entre campos | cross-field constraint |
| retry com feedback | retry with feedback |
| backoff exponencial | exponential backoff |
| teto de retries | retry cap |
| fallback | fallback |
| humano no loop | human in the loop |
| erro de validação | validation error |
| drift silencioso | silent drift |

## O que vem a seguir

Com validação e retry cobertos, a nota 08 fecha a trilha de Structured Outputs: como lidar com streaming. Quando o output é gerado token por token, você não pode esperar o documento completo para validar — precisa de estratégias de validação parcial e de como apresentar ao usuário output que ainda está sendo gerado.

Ver [[08 - Streaming de structured outputs]].

### Combine validação semântica com guardrails de sistema

Validação semântica pega muito. Mas pra coisas de segurança (PII, prompt injection refletida no output), você precisa de guardrails dedicados ([[03-Dominios/Tecnologia/IA/Segurança e Guardrails/01 - Código gerado por IA é untrusted|01 - Código gerado por IA é untrusted]]).

### Em alta vazão, considere modelos especializados

Pra extração estruturada em grande escala (milhões/dia), modelos como GPT-4o-mini ou Claude Haiku são suficientes 95% das vezes — escalar só os 5% que falham na validação. Custo cai drasticamente.

## Fontes

- **Pydantic** — *Validators docs* ([docs.pydantic.dev](https://docs.pydantic.dev/latest/concepts/validators/)).
- **Zod** — *Refinements* ([zod.dev/?id=refine](https://zod.dev/?id=refine)).
- **Eugene Yan** — *Patterns for LLM Systems* ([eugeneyan.com](https://eugeneyan.com/writing/llm-patterns/)). Seção "Guardrails" cobre retry-with-feedback.
- **Anthropic** — *Tool use error handling* ([docs](https://docs.anthropic.com/en/docs/build-with-claude/tool-use)). Padrão de passar erro de volta pro modelo.

## Veja também

- [[01 - O problema do output não estruturado]] — o problema que essa camada cobre
- [[02 - JSON Schema como contrato]] — schema é shape; validator é semântica
- [[04 - OpenAI Structured Outputs — strict mode]] — strict garante shape mas não semântica
- [[08 - Streaming de structured outputs]] — validação parcial em streaming
- [[03-Dominios/Tecnologia/IA/Segurança e Guardrails/01 - Código gerado por IA é untrusted|Código gerado por IA é untrusted]] — output validado é base pra qualquer execução segura
