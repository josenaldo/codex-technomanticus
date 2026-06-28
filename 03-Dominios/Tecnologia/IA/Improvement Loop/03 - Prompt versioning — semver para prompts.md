---
title: "03 - Prompt versioning — semver para prompts"
created: 2026-05-28
updated: 2026-06-28
type: concept
status: seedling
fase: Iniciado
progress: in_progress
tags:
  - improvement-loop
  - ia
  - versionamento
  - semver
publish: true
aliases:
  - Semver para prompts
  - Prompt semver
  - Quando bumpar prompt
---

# 03 - Prompt versioning — semver para prompts

> [!abstract] TL;DR
> [[03-Dominios/Tecnologia/IA/Observability/05 - Versionamento de prompts|Observability/05]] cobre **como** versionar (registry, label, semver, tying ao trace). Esta nota cobre **quando bumpar e o que cada bump dispara no Improvement Loop**: patch passa sem A/B (deploy direto); minor passa por A/B offline + canary curto; major dispara golden set novo + champion-challenger formal + plano de migração de consumer. Versão do prompt vira **gatilho** no pipeline — bumpou minor, automação roda A/B; bumpou major, automação cria branch de migração. Mapeamento versão → ação é a parte que torna semver útil pro loop em vez de só ser etiqueta bonita.

> [!question]- Como decidir entre major e minor quando a mudança está no limite? E quem decide?
> A heurística definidora: **se o golden set antigo ainda mede a versão nova de forma justa, é minor; se precisa de golden set novo, é major**. Casos limítrofes comuns: (a) adicionou instrução nova que muda como o modelo estrutura a resposta mas sem alterar o schema de saída — provavelmente minor (comportamento mudou, schema não); (b) renomeou campo de `answer` pra `response` — major (quebra consumer); (c) adicionou few-shot com exemplo num novo idioma — minor (só melhora cobertura). Quando ainda estiver em dúvida, bumpa como major: é mais conservador e evita que consumer quebre silenciosamente. Quem decide: no time pequeno é o dev que escreve o prompt; no time médio é convenção documentada na wiki ou `PROMPTS.md` do repositório.

## Ponte com Observability/05

[[03-Dominios/Tecnologia/IA/Observability/05 - Versionamento de prompts]] cobre:

- A regra de semver pra prompt (major/minor/patch e a heurística "se eval antigo ainda vale como baseline, é minor")
- Labels `dev` / `staging` / `production` no registry
- Tying versão ao span do trace
- Tools (Langfuse Prompts, PromptLayer, Braintrust)
- Rollback strategy
- Anti-padrões de versionamento

**Esta nota não duplica isso.** Aqui o foco é o que cada bump **dispara** no loop: o gatilho que conecta versionamento e os outros artefatos da melhoria (A/B, eval, champion-challenger, CI).

## Recap rápido — o mapa semver pra prompt

| Bump | Mudança | Eval antigo ainda vale? |
|---|---|---|
| **Patch** (v1.2.4 → v1.2.5) | Typo, wording sem comportamento | Sim, integralmente |
| **Minor** (v1.2 → v1.3) | Qualidade, few-shot, reordenação | Sim, como baseline |
| **Major** (v1 → v2) | Schema de output, contrato, tool removida | Não — precisa novo dataset |

Detalhes completos em [[03-Dominios/Tecnologia/IA/Observability/05 - Versionamento de prompts]].

## O que cada bump dispara

O ponto desta nota: o bump não é só metadata. Ele é **gatilho** que define o pipeline de promoção.

### Patch — fast-track

| Etapa | O que acontece |
|---|---|
| Eval offline | Smoke test (5-10 itens críticos), confirma que não quebrou |
| A/B | **Não roda** — mudança não comportamental |
| Canary | **Não roda** — risco residual baixo |
| Promoção | Direto pra `production` após smoke OK |
| Rollback plan | Label de volta pra versão anterior |

Patch existe pra **não atrapalhar** o time. Erro de wording corrigido às 23h não pode esperar 7 dias de canary. Trade-off aceitável: risco pequeno por velocidade.

### Minor — A/B obrigatório

| Etapa | O que acontece |
|---|---|
| Eval offline | Full golden set, comparado contra champion atual |
| Gate offline | Métrica primária ≥ champion (com significância); secundárias dentro da tolerância |
| A/B online | Canary 5-10% por período suficiente pro sample size declarado |
| Gate online | Bayesian P(B > A) > 0.95 OR frequentista p < 0.05 na métrica primária; guardrails verdes |
| Promoção | Label `production` move pro novo minor |
| Rollback plan | Label de volta pro minor anterior; cache 60s |

Minor é o **caso médio** do loop: bumpou prompt pra melhorar uma categoria, automação roda eval offline → se passa, dispara canary → se passa, promove.

### Major — champion-challenger formal

| Etapa | O que acontece |
|---|---|
| Eval offline | **Golden set novo** (esquema antigo não vale como baseline pra schema novo); rubrica revisitada |
| Consumer migration | Schema mudou — consumers precisam atualizar; coordena release com downstream |
| Shadow run | Treatment roda em paralelo sem servir ao usuário, pra coletar amostras com o schema novo |
| A/B online | Canary com **traffic split menor** (1-5%) e período maior |
| Gate online | Métricas primárias + guardrails secundários + zero regressão de consumer downstream |
| Promoção | Coordenada com release notes pro consumer; possivelmente feature flag por cliente |
| Rollback plan | Mais complexo — consumer pode já ter migrado pro schema novo; rollback precisa cobrir esse cenário |

Major é caro. Por isso bumpa pouco: se uma mudança pode ser feita preservando schema, prefere-se minor.

## Tabela de gatilhos — versão → automação

```
Push de prompt change → registry detecta bump
                                ↓
                         qual tipo de bump?
                ┌───────────────┼────────────────┐
                ▼               ▼                ▼
              PATCH           MINOR            MAJOR
                │              │                │
        smoke test          full eval       new dataset
        (5-10 itens)        (200+ itens)    + dataset versionado
                │              │                │
        passou? promove     passou?         shadow run
        direto                ↓             (sem servir user)
                              canary 5-10%      ↓
                              ↓                 canary 1-5%
                              passou?           ↓
                              promove           gate (incl. consumer)
                                                ↓
                                                promoção coordenada
                                                + release notes
```

Esta automação é o que diferencia "prompt versionado" de "prompt versionado **e usado pelo loop**". Registry só, sem gatilho, vira só changelog.

## Registry patterns — onde mora cada versão

| Pattern | Onde mora | Quando faz sentido |
|---|---|---|
| **Prompt em Git, tag = versão** | Source code repo, tag `prompt/research-system@v3.1.0` | Time pequeno, prompt poucos, review nativo via PR |
| **Prompt em registry SaaS (Langfuse, Braintrust, PromptLayer)** | Banco do vendor, labels gerenciados via UI/API | Time médio, prompts editados por produto/PM |
| **Prompt em arquivo YAML/JSON versionado** | Repo dedicado de prompts (separado do source), CI publica no registry | Time com muitos prompts, governança forte |
| **Híbrido** | Source canônico em Git, mas registry SaaS é cache pra runtime | Quer best of both — review em Git, hot-reload em runtime |

Não há vencedor universal. A escolha depende de:

- **Quem edita prompt?** Só dev → Git basta. Produto/PM também → registry com UI.
- **Frequência de mudança?** Baixa → Git. Alta → registry.
- **Volume de prompts?** Poucos → Git. Muitos → registry com tagging.
- **Governança?** Compliance pesado → registry com audit log nativo.

## Tying versão a git tag — fazer ou não fazer

Opção A: prompt versionado **só** no registry, sem espelhar em Git tag.

- Pro: edição rápida (não precisa abrir PR pra typo)
- Pro: produto/PM edita sem aprovação de dev
- Contra: source of truth bifurca (Git vs registry)
- Contra: rollback exige acesso ao registry

Opção B: prompt versionado em Git, registry é **mirror** publicado por CI.

- Pro: source of truth único (Git)
- Pro: review padrão (PR + diff)
- Contra: edição requer fluxo de dev
- Contra: cache do registry pode ficar atrás se CI falhar

Opção C: prompt em Git **e** versão do prompt nasce de tag Git semver (`prompt/research-system@v3.1.0`).

- Pro: rastreio integrado com release do produto
- Contra: cada mudança de wording é tag nova — pode poluir histórico do repo

Pattern recomendado em 2026 pra time típico: **B com cache curto** — Git canônico, CI publica no registry SaaS, registry tem cache de 60s no client. Best of both: review forte, runtime ágil.

## Quando bumpar — heurísticas práticas

### Patch — bumpa quando

- Corrigiu typo ou ortografia
- Removeu espaço duplicado, formatação cosmética
- Reformulou em paralelo sem mudar sentido ("favor" → "por favor")
- Atualizou referência externa que não muda comportamento ("ver docs em URL1" → "URL2")

### Minor — bumpa quando

- Adicionou few-shot
- Reordenou seções do system prompt
- Ajustou tom (mais formal, mais conciso)
- Adicionou guardrail soft (request adicional no system, sem mudar schema de output)
- Trocou exemplo few-shot
- Ajustou instrução pra reduzir uma classe específica de erro

### Major — bumpa quando

- Mudou schema do output (adicionou ou removeu campo)
- Mudou formato (markdown → JSON; texto → estruturado)
- Removeu uma tool do `tools` array
- Adicionou tool nova obrigatória
- Mudou contrato com consumer (e.g., consumer agora precisa parsear novo campo)

A regra heurística do [[03-Dominios/Tecnologia/IA/Observability/05 - Versionamento de prompts]] vale: **se o golden set antigo ainda mede a versão nova de forma justa, é minor; se precisa de golden set novo, é major**.

## Automação do gatilho — CI snippet

Exemplo em GitHub Actions: detecta o tipo de bump no PR e dispara o pipeline correspondente.

```yaml
# .github/workflows/prompt-ci.yml
name: Prompt CI

on:
  pull_request:
    paths:
      - "prompts/**"

jobs:
  detect-bump:
    runs-on: ubuntu-latest
    outputs:
      bump_type: ${{ steps.detect.outputs.bump_type }}
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 2
      - name: Detect bump type
        id: detect
        run: |
          python scripts/detect_prompt_bump.py \
            --base ${{ github.base_ref }} \
            --head HEAD \
            >> $GITHUB_OUTPUT

  smoke-test:
    needs: detect-bump
    if: needs.detect-bump.outputs.bump_type == 'patch'
    uses: ./.github/workflows/smoke-test.yml

  full-eval:
    needs: detect-bump
    if: needs.detect-bump.outputs.bump_type == 'minor'
    uses: ./.github/workflows/full-eval.yml

  major-pipeline:
    needs: detect-bump
    if: needs.detect-bump.outputs.bump_type == 'major'
    uses: ./.github/workflows/major-migration.yml
```

O script `detect_prompt_bump.py` compara o `MAJOR.MINOR.PATCH` do frontmatter do arquivo de prompt entre `base_ref` e `HEAD` e emite `patch`, `minor` ou `major`. A pipeline certa roda automaticamente — o autor do PR não decide, o bump decide.

## Anti-padrões específicos do gatilho

- **Patch que muda comportamento** — bumpou como patch, pulou A/B; regressão silenciosa
- **Minor sem A/B** — "vai dar certo, eu testei manualmente"; perde o ciclo de validação
- **Major sem novo golden set** — testou contra dataset antigo que não cobre o schema novo; baseline inválido
- **Bump sem changelog** — versionou, mas ninguém sabe **por que** mudou
- **Sem versionamento de dataset** — prompt em v3.1, eval ainda contra dataset de quando prompt era v2.x; comparação ruim
- **Skipping de promoção (`dev` → `production`)** — pulou `staging` porque "apertou prazo"; sem rede

## Armadilhas comuns

> [!warning] Bumpar como patch quando o comportamento mudou — e pular o A/B que deveria ter rodado
> O instinto é: "é só um ajuste de wording, não muda nada". Mas "adicionei 'seja conciso' no system prompt" pode reduzir respostas em 40% e quebrar consumers que esperam formato longo. A heurística correta: se você não tem certeza que o eval antigo ainda captura o comportamento da versão nova — é minor, não patch. Patch deve ser indiferente ao eval: se a pergunta "isso vai alterar algum score no golden set?" não tem resposta óbvia de "não", não é patch. O custo de rodar o eval uma vez é pequeno; o custo de uma regressão silenciosa em prod pode ser enorme.

> [!warning] Bumpou major sem coordenar a migração do consumer — e quebrou downstream silenciosamente
> Major de prompt que muda schema de saída é o equivalente de uma breaking change em API pública. Consumer que lê `response.answer` quebra quando o campo muda pra `response.output`. Diferente de código, a quebra pode ser silenciosa: o consumer pode receber um campo `None`, parsear errado, e retornar dado ruim sem exception. O padrão correto: (a) deprecation period com os dois formatos suportados simultaneamente (se possível); (b) notificação explícita aos consumers antes de promover o major pra `production`; (c) shadow run com o schema novo antes de qualquer usuário ver. Major sem plano de migração de consumer é um incident esperando acontecer.

> [!warning] Versionamento sem changelog — ninguém sabe por que o prompt mudou
> Bumpar versão sem registrar hipótese, contexto e resultado esperado transforma o histórico em sequência de números sem significado. "v1.3.0 → v1.4.0" não diz nada. "v1.3.0 → v1.4.0: adicionou few-shot pra casos em PT-EU onde summarization estava errando tema; esperado +8% em eval PT-EU" é o registro que o próximo dev vai usar quando a regressão aparecer. O lugar certo pra esse contexto é o commit message do PR de bump OU um `CHANGELOG.md` por prompt. Sem isso, o loop não acumula conhecimento — cada ciclo começa do zero.

## Como explicar em inglês

**Interview quote:** *"We treat prompts as versioned artifacts with semantic versioning adapted for LLM behavior. Patch is a non-behavioral change that goes straight to production after a smoke test. Minor is a behavioral improvement — adding few-shots, reordering instructions — that triggers an offline eval against the golden set and then a canary in production. Major is a schema-breaking change that requires a new golden set, a consumer migration plan, a shadow run, and a formal champion-challenger gate. The bump type becomes an automation trigger — the CI pipeline branches based on what kind of change it detects."*

| Português | Inglês |
|---|---|
| Versionamento semântico de prompt | Prompt semantic versioning |
| Bump de versão | Version bump |
| Mudança sem comportamento (patch) | Non-behavioral change (patch) |
| Mudança comportamental (minor) | Behavioral change (minor) |
| Mudança de schema (major) | Schema-breaking change (major) |
| Migração de consumer | Consumer migration |
| Gatilho de automação | Automation trigger |
| Changelog de prompt | Prompt changelog |
| Registry de prompts | Prompt registry |
| Golden set novo por major | New golden set for major bump |

## O que vem a seguir

Com o versioning e seus gatilhos claros, a nota 04 entra no mecanismo que executa o gate final após A/B: **champion-challenger em produção** — como promover o challener automaticamente quando os critérios passam, como configurar o rollback automático nas primeiras horas após ship, e como decidir entre rollback completo e hotfix quando os sinais são mistos.

## Fontes

- **Langfuse** — [*Prompt Management*](https://langfuse.com/docs/prompts/get-started). Labels e versionamento.
- **PromptLayer** — [*Prompt versioning docs*](https://docs.promptlayer.com/features/prompt-registry).
- **Braintrust** — [*Prompt management*](https://www.braintrust.dev/docs/guides/prompts).
- **Mitchell Hashimoto** — *Prompts are code* (2025). Argumento de prompt-como-artefato.
- **Semver.org** — [*Semantic Versioning 2.0.0*](https://semver.org/). Spec original que serve de base pra adaptação.
- **Hamel Husain** — [*Prompts should be versioned like code*](https://hamel.dev). Argumento de prompt-como-artefato.
- **GitHub Actions** — [*Workflow syntax*](https://docs.github.com/en/actions/writing-workflows). Referência de CI pra automação dos gatilhos.

## Veja também

- [[03-Dominios/Tecnologia/IA/Observability/05 - Versionamento de prompts]] — o **como** completo (registry, labels, tracing); esta nota cobre o **quando** e o **que dispara**
- [[02 - A-B testing de prompts]] — o que minor e major bumps disparam
- [[04 - Champion-challenger em produção]] — o gate que minor e major bumps atravessam
- [[07 - Eval gates em CI — quando bloquear merge]] — onde o bump vira parte do pipeline
- [[01 - O ciclo eval → diff → ship]] — onde o bump entra como passo 3 (diff)
- [[06 - Capturando feedback do usuário como sinal]] — sinal que determina quando bumpar e em qual categoria
- [[05 - Auto-prompt optimization — DSPy e além]] — quando o bump é gerado automaticamente pelo otimizador
- [[Dicionário de IA#Semver|Dicionário: Semver]]
- [[Dicionário de IA#Prompt registry|Dicionário: Prompt registry]]
- [[Dicionário de IA#Golden set|Dicionário: Golden set]]
- [[Dicionário de IA#Schema drift|Dicionário: Schema drift]]
- [[Dicionário de IA#Consumer (de prompt)|Dicionário: Consumer]]
