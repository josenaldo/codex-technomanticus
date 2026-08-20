---
title: "05 - Versionamento de prompts"
created: 2026-05-28
updated: 2026-06-28
type: concept
status: seedling
fase: iniciado
progress: in_progress
tags:
  - observability
  - ia
  - prompt-management
  - versionamento
publish: true
aliases:
  - Prompt versioning
  - Prompt registry
  - Semver pra prompt
---

# 05 - Versionamento de prompts

> [!abstract] TL;DR
> Prompt é **artefato versionado**, não config string em código. Tratá-lo como string hardcoded mata três coisas: rollback (não dá pra voltar pra v anterior sem redeploy), atribuição (não sabe qual versão gerou qual trace), e A/B (não tem como rodar v3.1 contra v3.2 em paralelo). A convenção que funciona é semver adaptado: **major** = mudança de formato de output (breaking pra quem consome), **minor** = melhoria de qualidade preservando schema, **patch** = correção de typo/wording sem mudar comportamento. Ambientes `dev` / `staging` / `production` viram labels no registry. Tools maduras em 2026: Langfuse Prompts, PromptLayer, Braintrust prompts, ou registry caseiro versionado em Git. Anti-padrão: prompt embutido no source-code sem versão — mata observabilidade no nascedouro.

> [!question]- O que acontece em produção quando um novo prompt piora qualidade — e como rollback sem redeploy?
> O sinal chega via dashboard: score de LLM-as-judge cai, refusal rate sobe, ou custo por token explode sem explicação. A resposta é mover o label `production` de volta pra versão anterior no registry — operação de segundos via UI ou API. O cache do SDK expira (default 60s em Langfuse) e todas as instâncias automaticamente voltam a servir o prompt antigo. Não há redeploy, não há push Git. O trace de cada chamada continua registrando `prompt_version` — o que permite confirmar exatamente quando o rollback chegou em produção e quantas chamadas usaram o prompt problemático.

## Por que prompt-como-string não escala

Imagine um bug de produção no sábado à noite: "as respostas do assistente pararam de retornar JSON válido". Você abre o trace, vê o span, e... o campo `prompt_version` não existe. Não sabe se foi o prompt que mudou, o código, ou o modelo. Investigação de horas vira dias. Esse é o custo real de prompt-como-string.

Prompt no source:

```python
# anti-pattern
SYSTEM = """Você é um assistente de pesquisa..."""

response = client.messages.create(system=SYSTEM, ...)
```

O que esse padrão impede:

- **Rollback rápido** — pra voltar à versão anterior precisa reverter código + redeploy
- **A/B test** — não tem mecanismo limpo pra rotear 10% pra v1 e 90% pra v2
- **Atribuição em trace** — span não sabe qual versão do prompt rodou (a string vai inteira, mas comparar entre traces é manual)
- **Iteração não-engenheiro** — produto/PM/pesquisador precisa abrir PR pra mudar wording
- **Audit trail** — quem mudou esse prompt, quando, por quê?

Prompt como artefato versionado resolve os 5.

## Semver-pra-prompt — a regra

Adaptação do semver clássico (`MAJOR.MINOR.PATCH`) pro contexto de prompt:

| Bump | Quando | Exemplo |
|---|---|---|
| **Major** (v1 → v2) | Mudança de **formato de output** que quebra quem consome | Output era markdown livre, virou JSON; output ganhou novo campo obrigatório; ferramenta removida do schema |
| **Minor** (v1.2 → v1.3) | Melhoria de **qualidade** preservando schema/contrato | Adicionou few-shot pra reduzir alucinação; reordenou seções; ajustou tom |
| **Patch** (v1.2.4 → v1.2.5) | Correção de typo, wording sem mudar comportamento | Erro de grafia; substituiu "favor" por "por favor"; corrigiu exemplo errado |

Regra simples pra decidir: **se um eval rodado contra dataset antigo ainda vale como baseline, é minor ou patch; se precisa de novo dataset porque o output mudou de forma, é major**.

Exemplo prático:

```
research-system v3.0.0  → output em JSON {answer, sources, confidence}
research-system v3.1.0  → adicionou few-shot pra confidence calibrada
                          (schema igual, qualidade melhor)
research-system v3.1.1  → typo: "Confiar" → "Confiança"
research-system v4.0.0  → output agora inclui {reasoning_trace}
                          consumers precisam atualizar
```

## Ambientes — labels no registry

Em vez de "produção sempre roda a última versão", o registry expõe labels:

| Label | Aponta pra | Quem promove |
|---|---|---|
| `dev` / `latest` | Última versão criada | Qualquer dev |
| `staging` | Versão em validação | Após eval automatizada passar |
| `production` | Versão servindo tráfego | Manual, após review + aprovação |

```python
# código de produção pega sempre a label, nunca a versão:
prompt = langfuse.get_prompt("research-system", label="production")
```

Promover uma versão = mover o label, não redeployar. Rollback = mover o label de volta. Operação de segundos, sem pipeline de CI envolvido.

A/B test entre duas versões:

```python
# rota 10% do tráfego pra candidato:
if random.random() < 0.10:
    prompt = langfuse.get_prompt("research-system", label="canary")
else:
    prompt = langfuse.get_prompt("research-system", label="production")
```

## Tying versão ao trace — o detalhe crítico

Toda chamada precisa registrar **qual versão exata do prompt foi usada** como atributo do span. Sem isso, comparar traces de antes/depois do deploy fica adivinhação.

Em Langfuse, isso vem de graça quando passa o objeto `prompt`:

```python
prompt = langfuse.get_prompt("research-system", label="production")
# prompt.version = 7 (auto-incrementado pelo registry)

response = client.messages.create(
    model="claude-sonnet-4-6",
    system=prompt.compile(topic=topic),
    messages=[...],
    extra_body={"langfuse_prompt": prompt},  # vincula no trace
)
# Span agora tem prompt_id="research-system", prompt_version=7
```

Em qualquer outro stack (OpenLLMetry, instrumentação manual), faz na mão:

```python
span.set_attribute("prompt.id", "research-system")
span.set_attribute("prompt.version", "3.1.0")
span.set_attribute("prompt.label", "production")
```

A partir desse atributo, dashboards passam a permitir queries como:

- "score médio de v3.1.0 vs v3.0.0 nos últimos 7 dias"
- "taxa de refusal aumentou depois do deploy de v3.1.0?"
- "qual versão estava em produção quando esse incidente aconteceu?"

## Tools de prompt management em 2026

| Tool | Tipo | Forte em | Tradeoff |
|---|---|---|---|
| **Langfuse Prompts** | OSS + Cloud | Integração nativa com tracing/eval; labels; cache server+client | Acoplado ao Langfuse |
| **PromptLayer** | SaaS | UI focada em prompt management; histórico rico | Outro produto pra operar |
| **Braintrust Prompts** | SaaS | Forte integração com evals/CI gates | Pago; melhor em time com Braintrust já adotado |
| **Registry caseiro em Git** | DIY | Source of truth no Git; review nativo; semver via tags | Falta UI, cache, A/B routing — você implementa |
| **Helicone Prompts** | Cloud | Setup leve via proxy | Sem registry/eval no mesmo plano que Langfuse; depende do produto Helicone |

Decisão pragmática: se já está em Langfuse, use Langfuse Prompts. Se já tem Git workflow forte e time pequeno, registry caseiro com tags semver + arquivo YAML/JSON resolve. Tools dedicadas (PromptLayer, Braintrust) brilham quando produto/PM-não-dev edita prompt sem PR.

**Registry caseiro mínimo em Git:**

```
prompts/
  research-system/
    v3.0.0.yaml       # arquivo de cada versão
    v3.1.0.yaml
    CHANGELOG.md      # por que cada bump
    current.txt       # aponta pra versão em staging/prod
```

Pra CI: lê `current.txt`, carrega o YAML correspondente, injeta cache com TTL. Simple, auditable, sem dependência de produto externo. A desvantagem é não ter UI — iteração de PM/pesquisador exige PR.

## Integração com CI/CD — o gate de promoção

O gate que separa `staging` de `production` deve ser explícito, não implícito:

```yaml
# .github/workflows/prompt-staging.yml (simplificado)
on:
  push:
    paths:
      - 'prompts/**'

jobs:
  eval-gate:
    steps:
      - name: Run eval against staging prompt
        run: python scripts/eval_prompt.py --label staging --threshold 0.82
      
      - name: Promote to production if pass
        if: success()
        run: python scripts/promote_prompt.py --from staging --to production
```

Se o eval falha, o label `staging` não avança. Se avança, a promoção é auditável via git history do `current.txt` + trace do span com `prompt_version`. Sem esse gate, promoção vira decisão humana inconsistente.

## Rollback strategy

Plano de rollback prompt-em-produção deve ser **mais rápido que rollback de código**:

1. Detecção: dashboard alertou (score caiu, refusal rate subiu, custo explodiu) ou usuário reportou
2. Mover label `production` de v3.1.0 → v3.0.0 (operação de UI ou API; segundos)
3. Cache client-side (default 60s em Langfuse) expira — todas as instâncias pegam a nova label
4. Trace passa a registrar `prompt_version=3.0.0` — viabiliza confirmar que rollback chegou em produção
5. Postmortem com traces de v3.1.0 já capturados — vira dataset de eval pra próxima tentativa

Não há redeploy. Não há push pra Git. Cache curto + label móvel = rollback de minutos.

## Anti-padrões comuns

- **Prompt hardcoded sem version** — discutido acima; mata as 5 capacidades
- **Mudança de prompt em hotfix sem semver bump** — quem consome não sabe que mudou; bug silencioso
- **Bump errado (minor pra mudança breaking)** — quebra consumer downstream; sempre que mudar schema, é major
- **Prompt em config sem audit log** — quem mudou? Quando? Registry com histórico resolve
- **Sem fallback** — `get_prompt` falha (rede, auth), código quebra; sempre passar `fallback="..."`
- **Versão diferente entre traces e código** — se cache não invalidou direito, código velho rodando prompt novo; observability detecta se atributo `prompt_version` está no span
- **Edição direto em produção sem staging** — promova `dev → staging → production`; staging deve rodar eval automatizada antes de virar produção

## Workflow completo de iteração de prompt

O loop que times maduros usam ao iterar sobre um prompt em produção:

```
1. Escreve nova versão (v3.2.0) no registry, label = dev/latest
2. Roda eval offline: dataset existente + rubrica + LLM-as-judge
   → score ≥ threshold? Segue. Regrediu? Volta ao passo 1.
3. Promove para label "staging"
4. CI/CD roda eval automatizada (subconjunto rápido, ~50 examples)
   → gate pass? Segue. Fail? Notifica e não promove.
5. Code review do diff de prompt (em alguns times, opcional)
6. Promove para label "production" (manual ou CI gate)
7. Monitora dashboard por 24h: score, latência, custo
8. Incidente? Rollback = mover label "production" de volta pra v3.1.0
9. Postmortem: traces de v3.2.0 viram novos itens de dataset
```

Esse loop pode completar em horas quando o eval é automatizado — bem diferente do ciclo de code review + build + deploy que leva dias.

## Prompt template — estrutura interna versionável

Um prompt que vai pra registry não é só texto — é um template com variáveis e metadata:

```yaml
# Exemplo de schema de prompt no registry
id: research-system
version: 3.1.0
label: production
variables:
  - topic
  - output_format   # json ou markdown
  - language        # pt-BR, en-US
template: |
  Você é um assistente de pesquisa especializado em {{topic}}.
  Responda em {{language}}.
  Formato de output: {{output_format}}.
  
  Diretrizes:
  - Seja direto e cite fontes quando possível
  - Se não souber, diga que não sabe
  - Calibre confidence nos valores 0.0–1.0
notes: "v3.1: adicionado few-shot pra confidence; v3.0 era markdown-only"
author: "@user@exemplo.com"
created_at: 2026-05-15
```

Mesmo que o registry não suporte YAML explicitamente, manter esses campos como metadata torna postmortem muito mais rápido: você sabe quem tocou o prompt, quando, e por quê.

## Armadilhas comuns

> [!warning] Prompt em Git sem mecanismo de cache server-side gera latência por chamada
> Registry caseiro em Git parece simples: lê o arquivo, usa o texto. Mas sem cache, cada chamada lê do Git (ou S3, ou onde guardar) antes de chamar o LLM — o que adiciona decenas a centenas de ms de latência em hot paths. Langfuse e PromptLayer fazem cache server-side transparente (TTL configurável). Registry DIY precisa de cache explícito na aplicação. Se isso não for implementado, o time começa a copiar o prompt pra variável de ambiente — e o versionamento perde o ponto.

> [!warning] Mover label `production` sem rodar eval antes — o "rollback rápido" vira "bug diferente"
> Label é fácil de mover. Mas mover `production` de volta pra v3.0.0 sem verificar que v3.0.0 ainda é válida pra os dados atuais é temerário — o dataset de produção pode ter mudado desde então. Rollback de prompt deve ser tratado como qualquer outro rollback de sistema crítico: rápido, mas consciente de que você está voltando pra um estado potencialmente defasado. Tenha evals com dataset vivo pra validar o candidato de rollback também.

> [!warning] Semver de prompt sem disciplina vira número decorativo
> Times adotam semver de prompt com intenção, mas depois de 3 meses todo bump é minor — porque "não chegou a mudar o schema". Se o rubric de avaliação mudou, se o modelo que o prompt foi calibrado mudou (Sonnet 3.7 → 4.6), ou se o contexto do sistema ao redor mudou significativamente, isso pode ser um major mesmo sem tocar o JSON schema. Documente a regra de bump e revise periodicamente.

## Como explicar em inglês

**Interview quote:** *"We treat prompts as versioned artifacts — not config strings. Every production call records the exact prompt version in the trace. When quality drops, we roll back the label in the registry in seconds, without a redeploy. Promotion from staging to production goes through an automated eval gate."*

| Português | Inglês |
|---|---|
| Prompt versionado | Versioned prompt |
| Registry de prompts | Prompt registry |
| Label de ambiente (dev/staging/production) | Environment label |
| Promoção de label | Label promotion |
| Rollback de prompt (sem redeploy) | Prompt rollback (without redeployment) |
| Cache client-side com TTL | Client-side cache with TTL |
| Template com variáveis | Parameterized prompt template |
| Atributo `prompt_version` no span | `prompt_version` span attribute |
| Audit log de quem editou o prompt | Prompt change audit log |

## O que vem a seguir

Com prompt versionado e vinculado ao trace, você pode reproduzir qualquer interação do passado. A nota 06 explora como isso se traduz em **session replay** — a capacidade de remontar uma conversa inteira, span a span, com prompts exatos e contextos completos, pra debugar comportamentos inesperados em produção.

## Fontes

- **Langfuse** — [Prompt Management Docs](https://langfuse.com/docs/prompts/get-started) · [Prompt Versioning](https://langfuse.com/docs/prompts/get-started#prompt-versioning).
- **PromptLayer** — [Documentação](https://docs.promptlayer.com/).
- **Braintrust** — [Prompt management](https://www.braintrust.dev/docs/guides/prompts).
- **Mitchell Hashimoto** — *Prompts are code* (post em hashimoto.dev, 2025). Argumento de prompt-como-artefato versionado.
- **Anthropic** — [*Prompt engineering best practices*](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview). Seção sobre tracking de versão.

## Veja também

- [[03 - Langfuse — open-source standard]] — Langfuse Prompts é a referência operacional
- [[06 - Session replay e debugging]] — versão de prompt é peça obrigatória do replay
- [[02 - Anatomia de um trace LLM]] — `prompt_version` é atributo de span
- [[03-Dominios/Tecnologia/IA/Evaluation/07 - Eval em CI-CD]] — promoção `staging → production` passa pela eval automatizada
- [[Prompt Engineering]] — onde os prompts são desenhados antes de virarem versão
