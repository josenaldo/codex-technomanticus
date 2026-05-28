---
title: "Setup completo — do zero ao sistema de produção"
created: 2026-05-28
updated: 2026-05-28
type: concept
status: seedling
progress: in_progress
tags:
  - ai-engineering-stack
  - ia
  - recipe
  - setup
publish: true
aliases:
  - Setup completo do AI Engineering Stack
  - Recipe end-to-end
---

# Setup completo — do zero ao sistema de produção

> [!abstract] TL;DR
> Esta nota atravessa as 11 camadas com um exemplo concreto: um **gerador de newsletter semanal de IA**. Para cada camada, preenchemos o template e mostramos a decisão. No fim, você tem o blueprint completo de um sistema — não apenas o que cada camada faz, mas como elas conversam entre si. Use esta recipe como ponto de partida pra adaptar a sistemas seus, trocando o exemplo pelos seus inputs.

## O sistema de exemplo

**AI Weekly Newsletter Generator** — um sistema que, toda sexta-feira, monta uma newsletter sobre o que aconteceu em IA na semana, com 5-7 itens curados, cada um com link, resumo e takeaway de uma frase.

Por que esse exemplo:
- É comum o bastante pra todo mundo entender o problema.
- Toca **todas** as 11 camadas (não é trivial demais).
- Tem riscos reais (citação errada, viés de fonte, alucinação de link).
- É o exemplo usado pelo @hooeem no thread original — facilita comparação.

> [!info] Este é um exemplo didático
> Os valores abaixo são razoáveis pro exemplo, não prescrição universal. Adapte a defaults sensatos pro seu domínio.

## Camada 1 — Purpose

```yaml
system_name: ai_weekly
primary_job: gerar newsletter semanal sobre o que aconteceu em IA na semana
user: profissional de tech que quer ficar a par sem ler 200 tweets/dia
main_output: 1 newsletter em markdown com 5-7 itens (título, link, resumo de ~80 palavras, takeaway de 1 frase)
success_criteria:
  - 100% dos links abrem e apontam pra fonte primária
  - cada resumo passa em 30 segundos de leitura
  - takeaway revela a relevância sem clickbait
  - newsletter é entregue toda sexta às 9h
not_in_scope:
  - opinião editorial extensa
  - cobertura de tópicos fora de IA
  - notícias com >7 dias
  - threads inteiras de X reproduzidas
```

O `not_in_scope` é o que evita escopo elástico: o sistema vai **rejeitar** assuntos fora dessa caixa.

## Camada 2 — Workflow vs Agent

**Decisão: workflow**, não agent.

Justificativa: o caminho é predizível — (1) coletar candidatos da semana, (2) filtrar relevância, (3) escrever resumos, (4) montar newsletter. Nenhum passo precisa de "descoberta dinâmica do próximo passo". Agent aqui seria over-engineering — mais erro, mais custo, debug pior.

Forma concreta: **prompt chaining** (4 chamadas de LLM em sequência, cada uma com input estruturado da anterior). Padrão da Anthropic: "the path is fixed; chain LLM calls."

## Camada 3 — Prompt Layer

System prompt (versão 1.0):

```yaml
role: editor sênior especializado em IA, com tom direto e cético
primary_job: curar, resumir e organizar avanços relevantes em IA da semana
primary_standard: relevância > volume — nunca preencha pra atingir N itens
allowed_actions:
  - resumir artigo/release/paper
  - destacar trade-offs e limitações
  - apontar discordâncias entre fontes
forbidden_actions:
  - especulação sobre roadmap não anunciado
  - linguagem promocional ("revolucionário", "game-changer")
  - extrapolação sem citar a fonte
uncertainty_behavior: marcar com [confiança: baixa] e citar limitação da fonte
reasoning_style: conciso; evidência antes de afirmação
```

Note: `forbidden_actions` aqui é **aspiracional** — esperamos que o modelo siga. A imposição real fica na Guardrail Layer.

## Camada 4 — Context Layer

Context montado a cada execução semanal:

```yaml
goal: gerar newsletter da semana de YYYY-MM-DD a YYYY-MM-DD
audience: profissional de tech sênior, segue IA mas não passa o dia no X
project_context: newsletter no ar há N semanas; tom estabelecido na edição #1
source_material:
  - feeds RSS de blogs oficiais (Anthropic, OpenAI, Google, Meta)
  - papers do arXiv (cs.CL, cs.AI, novos da semana)
  - 5 newsletters de referência (cita só, não copia)
preferences:
  - exemplos práticos preferidos a benchmarks abstratos
  - 1 item de paper, 1 item de produto, 1 item de "lado sombrio", o resto livre
constraints:
  - máximo 1200 palavras na newsletter inteira
  - orçamento: $5 por edição em chamadas de modelo
decision_history:
  - edição #12 cortou "tweet of the week" — engagement subiu
  - edição #18 testou tom mais opinativo — feedback negativo, revertido
known_failure_modes:
  - inflar releases de produto com hype
  - confundir paper preprint com peer-reviewed
  - perder release importante por falha de feed RSS
```

`known_failure_modes` no contexto força o modelo a se vigiar sobre esses pontos.

## Camada 5 — Output Layer

```yaml
primary_format: markdown
required_sections:
  - "## Esta semana em IA — [date]"
  - "### Em destaque" (1 item)
  - "### Releases" (1-2 itens)
  - "### Pesquisa" (1-2 itens)
  - "### Para refletir" (1 item — lado sombrio/crítico)
  - "### Curtas" (opcional, 0-2 itens)
confidence_level: opcional — emitir só quando <medium
uncertainty_flags:
  - "[confiança: baixa]" antes do resumo quando aplicável
  - "[fonte: preprint]" quando paper não é peer-reviewed
actionability: sugestão — newsletter é leitura, não ação automática
```

Cada item da newsletter segue schema interno:

```json
{
  "title": "string, ≤80 chars",
  "url": "string, validado por requisição HEAD",
  "summary": "string, 60-100 palavras",
  "takeaway": "string, 1 frase ≤25 palavras",
  "confidence": "high|medium|low",
  "source_type": "official_blog|paper|news|preprint"
}
```

## Camada 6 — Retrieval Layer

```yaml
use_retrieval_when:
  - sempre — newsletter inteira depende de fontes da semana
source_hierarchy:
  - 1. blogs oficiais (Anthropic, OpenAI, Google, Meta, Mistral)
  - 2. arXiv (cs.CL, cs.AI, cs.LG)
  - 3. publicações estabelecidas (The Information, IEEE Spectrum)
  - 4. blogs/newsletters de referência (citar, não reproduzir)
citation_rule: toda claim factual no resumo cita link da fonte primária
conflict_rule: blog oficial > arXiv > terceiros; mais recente em caso de empate
missing_source_rule: se não há fonte primária verificável, item é descartado (não inventado)
```

Implementação: RSS readers + arXiv API + web search via tool. Indexação simples por data (não precisa vector DB — janela é só 7 dias).

## Camada 7 — Tool Layer

```yaml
available_tools:
  - name: fetch_rss
    when_to_use: coletar itens da semana de feeds conhecidos
    when_not_to_use: feeds não estão na allowlist
  - name: fetch_arxiv
    when_to_use: buscar papers novos da semana em categorias-alvo
    when_not_to_use: paper >7 dias
  - name: web_get
    when_to_use: ler conteúdo completo de URL específica
    when_not_to_use: URL fora dos domínios permitidos
  - name: validate_url
    when_to_use: confirmar que URL responde 200 antes de incluir
    when_not_to_use: nunca; sempre validar
allowed_without_approval:
  - fetch_rss, fetch_arxiv, web_get, validate_url
requires_approval:
  - send_newsletter (envio real pros assinantes)
forbidden:
  - tools de escrita em sistemas externos exceto envio aprovado
tool_failure_behavior: retry 2x com backoff exponencial; em falha definitiva, log e continua (newsletter pode sair com -1 item)
```

## Camada 8 — Evaluation Layer

```yaml
success_criteria: herda do Purpose Layer
scoring_rubric:
  accuracy: 1-5 (claims do resumo batem com a fonte?)
  completeness: 1-5 (cobre o que a newsletter prometeu?)
  usefulness: 1-5 (o leitor tira valor?)
  format_adherence: 1-5 (markdown válido, seções na ordem, schema dos itens?)
  source_quality: 1-5 (fonte primária ou terciária?)
  specificity: 1-5 (resumos concretos ou genéricos?)
  risk_control: 1-5 (sem hype, sem clickbait, sem PII?)
pass_threshold: média ≥4 e nenhuma dimensão <3
automatic_failure_conditions:
  - link quebrado em qualquer item
  - palavras-clichê de hype detectadas ("revolucionário", "muda tudo")
  - preprint marcado como peer-reviewed
```

Aplicação: LLM-as-judge roda em todos os candidatos antes da newsletter sair. Itens com nota <3 em qualquer dimensão são reescritos ou descartados. Newsletter inteira só sai se passar o threshold.

Dataset de regression: 20 edições anteriores anotadas, comparadas a cada mudança de prompt.

## Camada 9 — Guardrail Layer

```yaml
allowed_without_approval:
  - gerar drafts internos
  - chamar tools de leitura
requires_approval:
  - publicar newsletter (humano clica "enviar")
forbidden:
  - inclusão de URL não-validada
  - inclusão de claim sem fonte
  - reprodução >50 palavras de fonte de terceiros
must_flag:
  - confidence:low em qualquer item
  - item de fonte tier 4 (newsletter de terceiros)
  - dimensão da rubrica <3
must_stop_when:
  - custo da execução >$5
  - 3 chamadas de modelo falham em sequência
  - guardrail de hype dispara 3x no mesmo item
escalation_rule: pausa, registra trace, notifica owner via Slack
```

Implementação: middleware antes e depois da chamada do modelo, mais filtros no schema validator.

## Camada 10 — Logging Layer

Por execução semanal, registra um trace com:

```json
{
  "run_id": "uuid",
  "week_of": "2026-05-25",
  "prompt_version": "1.0",
  "models": ["claude-opus-4.7", "gpt-5"],
  "sources_consulted": [{ "url": "...", "fetched_at": "...", "status": 200 }],
  "candidates_collected": 47,
  "candidates_after_filter": 6,
  "tool_calls": [{ "name": "fetch_rss", "latency_ms": 230, "success": true }],
  "eval_scores": { "accuracy": 4.6, "format_adherence": 5, "...": "..." },
  "guardrails_triggered": [{ "name": "hype_detector", "item": 3, "action": "rewrite" }],
  "cost_usd": 3.47,
  "final_output_hash": "sha256:...",
  "human_approval": { "approved_by": "...", "approved_at": "..." }
}
```

Implementação: OpenTelemetry GenAI semantic conventions + Langfuse.

## Camada 11 — Improvement Layer

```yaml
review_cadence: após cada edição (curto) + revisão mensal (longo)
questions_per_review:
  - quais itens performaram melhor (open rate, cliques)?
  - quais resumos exigiram edição humana antes do envio?
  - quais guardrails dispararam — padrão?
  - mudou alguma fonte (atualizar source_hierarchy)?
artifacts:
  - changelog do system prompt (versionado em git)
  - dataset de regression atualizado com casos novos
  - novas regras de hype-detector quando palavra clichê passa
ownership: editor humano da newsletter; revisão mensal com time
```

Saída esperada: prompt_version sobe a cada 4-6 semanas; dataset de eval cresce; guardrails ficam mais finos.

## Checklist final antes de produção

Antes de publicar pra primeiro grupo de assinantes:

- [ ] Purpose Layer revisada com um stakeholder
- [ ] Prompt Layer testada em 5 semanas históricas (replay)
- [ ] Schema do Output Layer valida com jsonschema sem erros
- [ ] Retrieval Layer tem allowlist de domínios fechada
- [ ] Tool Layer com `requires_approval` cobrindo o envio
- [ ] Evaluation Layer com dataset de regression e threshold
- [ ] Guardrail Layer com kill switch de custo configurado
- [ ] Logging Layer escrevendo em backend persistente
- [ ] Improvement Layer com cadência agendada no calendário
- [ ] Plano de rollback (versionado) caso a edição 1 falhe feio

## O que esta recipe demonstra

Três coisas que não aparecem olhando camada por camada:

1. **As camadas se referenciam.** `success_criteria` do Purpose vira rubrica da Eval. `forbidden_actions` do Prompt vira regra real na Guardrail. `known_failure_modes` do Context vira guardrail novo após cada incidente.

2. **A ordem natural não é numérica.** Construímos Purpose → Workflow → Output → Prompt+Context → Retrieval → Tool → Eval → Guardrail → Logging → Improvement. Pular pra Prompt Layer antes de fechar Purpose e Output é receita de retrabalho.

3. **Cada camada produz artefato versionado.** Nada disso é "documento de design que ninguém vê". É arquivo de configuração, schema, rubrica, prompt versionado — todos em git, todos com diff revisável.

## Veja também

- [[01 - As 11 camadas — visão geral]]
- [[02 - Purpose Layer — o que o sistema é]] até [[12 - Improvement Layer]] — uma por camada
- [[Spec-Driven Development]] — formaliza a primeira metade do recipe
- [[Context Engineering]] — aprofunda Camada 4
- [[RAG e Vector Databases]] — aprofunda Camada 6
- [[Anatomia de Agents]] — quando seu sistema for agent em vez de workflow

## Fontes

- **@hooeem** — *Become an AI Engineer*, chapter #18, "Building your AI engineering stack" (exemplo do gerador de newsletter).
- **Anthropic** — [*Building effective agents*](https://www.anthropic.com/engineering/building-effective-agents). Padrão prompt chaining como workflow.
- **OpenAI** — [*Structured Outputs guide*](https://platform.openai.com/docs/guides/structured-outputs). Schema enforcement.
- **OpenTelemetry** — [*Semantic Conventions for Generative AI*](https://opentelemetry.io/docs/specs/semconv/gen-ai/). Padrão de logging adotado.
