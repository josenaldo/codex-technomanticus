---
title: "05 - Regression testing em LLMs"
created: 2026-05-28
updated: 2026-05-28
type: concept
status: seedling
progress: in_progress
fase: Iniciado
tags:
  - evaluation
  - ia
  - regression
  - snapshot
publish: true
aliases:
  - Regression testing
  - LLM regression
  - Snapshot diff
---

# 05 - Regression testing em LLMs

> [!abstract] TL;DR
> Regressão em LLM é o cenário canônico do *"prompt v1.2 melhora o caso geral, mas silenciosamente quebra um edge case que v1.1 acertava"*. Sem regression testing automatizado, a quebra só aparece em prod via reclamação. A abordagem é **snapshot diff**: captura outputs do golden set em v1.1, compara com outputs em v1.2, sinaliza divergências. O detalhe não-trivial é que LLMs são **não-determinísticos** — string diff puro acusa diferença em quase tudo. A solução é **semantic diff** (embedding similarity, equivalence judge, schema validation) com tolerância calibrada. Categorias de regression test: correctness, format, safety, calibration. Cada uma com threshold próprio.

> [!question]- O que eu preciso saber antes de ler isso?
> Você entende o que é um golden set (nota 02), o que é rubrica e threshold (nota 03), e como LLM-as-judge funciona como equivalence judge (nota 04). Esta nota aplica esses conceitos a um problema de engenharia específico: como garantir que mudanças de prompt não quebrem comportamentos que já funcionavam. Se você já trabalhou com regression testing em software convencional (snapshot tests, golden files), vai reconhecer o padrão — a diferença é que LLMs são não-determinísticos, então string diff puro não funciona.

## O problema canônico

Cenário real:

```
Sprint 1 — Prompt v1.0 deployed
  Golden set score: 78%
  Edge case "input em japonês com emoji" → passa

Sprint 2 — Prompt v1.1 com nova instrução de tom
  Golden set score: 84% (subiu!)
  Edge case "input em japonês com emoji" → falha silenciosa

Sprint 3 — Usuário japonês reclama
  Debug: input X agora retorna inglês em vez de japonês
  Causa: nova instrução de tom dominou a instrução de idioma
  Hotfix em pânico
```

Sem regression test, esse ciclo se repete a cada sprint. A métrica agregada subiu — então parece progresso — mas casos específicos quebraram.

A correção é capturar **cada caso** do golden set como snapshot e comparar v→v+1.

## Snapshot diff — a abordagem básica

```python
# Pseudocode
def regression_test(golden_set, prompt_v_old, prompt_v_new, judge):
    results = []
    for item in golden_set:
        out_old = run_prompt(prompt_v_old, item.input)
        out_new = run_prompt(prompt_v_new, item.input)

        equivalent = judge.equivalent(
            input=item.input,
            output_a=out_old,
            output_b=out_new,
            tolerance=item.tolerance
        )

        results.append({
            "id": item.id,
            "old_output": out_old,
            "new_output": out_new,
            "equivalent": equivalent,
            "score_old": score(out_old, item.expected),
            "score_new": score(out_new, item.expected),
        })
    return results

def report(results):
    regressions = [r for r in results if r["score_new"] < r["score_old"]]
    improvements = [r for r in results if r["score_new"] > r["score_old"]]
    neutral = [r for r in results if r["score_new"] == r["score_old"]]

    print(f"Regressions: {len(regressions)}")
    print(f"Improvements: {len(improvements)}")
    print(f"Neutral: {len(neutral)}")
    print(f"Net: {'+' if len(improvements) > len(regressions) else '-'}")
```

O que reportar:

- **Total score** (acompanhar tendência)
- **Regressões individuais** (que itens caíram?)
- **Categoria de regressão** (correctness? format? tone?)
- **Diff de output** (humano ainda precisa ler os casos críticos)

## String diff vs semantic diff

O equívoco de iniciante: comparar outputs com `==`.

```python
out_old = "A senha foi alterada com sucesso."
out_new = "Senha alterada com sucesso!"

out_old == out_new  # False
```

Por string diff, é regressão. Semanticamente, é equivalente. LLM é estocástico — pequenas variações de tokenização, sampling, capitalização são normais.

Semantic diff usa pelo menos um destes:

| Método | Como funciona | Quando usar |
|---|---|---|
| **Schema equality** | Compara campo a campo no JSON parseado | Tarefas com structured output |
| **Embedding cosine** | Embedding(A) vs Embedding(B), cos>0.9 = equiv | Texto livre, similaridade semântica |
| **Equivalence judge** | LLM-as-judge: "essas duas respostas dizem a mesma coisa?" | Subjetivo, alta tolerância |
| **Test execution** | Roda código gerado, vê se passa nos mesmos testes | Geração de código |
| **Exact match** | `==` cru | Apenas para campos canônicos enumerados |

Pra um sistema sério, **misture**. Schema equality pros campos enumerados, embedding pra texto longo, equivalence judge pros casos críticos.

## Calibrando tolerância

Tolerância depende da tarefa:

| Tipo | Tolerância semântica |
|---|---|
| **Classificação** | Zero — categoria é categoria |
| **Extração estruturada** | Zero pros campos, baixa pras strings extraídas |
| **Resumo curto** | Média — paráfrase é OK |
| **Resposta longa de chat** | Alta — variação estilística esperada |
| **Geração de código** | Funcional (passa testes) > estética |

Threshold de embedding similarity por tipo:

```yaml
classify: 1.0       # exato
extract: 0.95       # quase exato
summary: 0.85       # similaridade semântica
chat: 0.75          # tom + conteúdo
code: passes_tests  # binário funcional
```

Threshold alto demais → não detecta regressão real.
Threshold baixo demais → ruído permanente, todos os PRs sinalizam "regressão".

## Quando rebless (atualizar) o snapshot

Snapshot velho não é sagrado. Reblessing é parte do fluxo. Quando:

1. **Mudança intencional de comportamento** — você mudou o prompt **propositadamente** pra responder de outro jeito. Snapshot antigo está obsoleto.
2. **Bug no expected antigo** — o snapshot original estava errado. Atualiza com o output correto.
3. **Mudança de modelo** — trocou Sonnet 4.5 por Sonnet 4.6, todos os outputs mudaram naturalmente.

Como reblessing seguro:

```bash
# Vê os diffs
eval run --golden-set v1.2 --prompt v1.2

# Inspecionar humano (não automatize esse passo)
# Decide quais são regressões reais vs mudanças aceitáveis

eval rebless --items "id1,id5,id12" --reason "tom mudado intencionalmente em v1.2"

# Snapshot novo committed em git, junto com explicação
git add golden_set/snapshots/v1.2.json
git commit -m "rebless: 3 itens — tom intencional em v1.2"
```

Reblessing sem humano = automação destruindo o sinal de regressão. Cada rebless tem que ter **razão escrita**.

## Categorias de regression test

### Correctness regression

- O output está factualmente correto?
- Mesma classificação que antes?
- Mesmo schema preenchido?

Threshold típico: 0% de regressão tolerada nos casos críticos.

### Format regression

- JSON ainda parseável?
- Campos obrigatórios presentes?
- Tipos batendo?

Threshold típico: 0% — quebra de formato bloqueia merge.

### Safety regression

- Continua recusando inputs adversariais?
- Continua não vazando PII?
- Continua dentro dos guardrails?

Threshold típico: 0% — qualquer regressão de segurança = blocker.

### Calibration regression

- Confidence scores ainda calibrados?
- Modelo ainda diz "não sei" quando deve?
- Distribuição de severidades parecida com prod?

Threshold típico: 5-10% — calibração tem ruído natural.

Cada categoria tem peso e threshold próprios. Correctness com peso 1.0; safety com peso "critical" (zera tudo); calibration com peso 0.5.

## Pattern recomendado em CI

```yaml
on:
  pull_request:
    paths: ["prompts/**", "src/llm/**"]

steps:
  - name: Regression — Correctness
    run: eval regression --category correctness --threshold 0
    # bloqueia se houver QUALQUER regressão de correctness

  - name: Regression — Format
    run: eval regression --category format --threshold 0
    # bloqueia se quebrar shape

  - name: Regression — Safety
    run: eval regression --category safety --threshold 0
    # bloqueia se vazar PII ou ignorar guardrail

  - name: Regression — Calibration
    run: eval regression --category calibration --threshold 0.1
    # tolera 10% de variação em calibration

  - name: Comment summary in PR
    run: eval report --format markdown --post-pr
```

Detalhe em [[07 - Eval em CI-CD]].

## Caso de uso real — bug regression

A regra: **todo bug em prod vira regression test permanente**.

```
1. Bug em prod: input "Ignore as instruções" passa por guardrail
2. Reproduzir local
3. Adicionar ao golden set como safety regression test
4. Verificar que o atual prompt FALHA o teste (cor: vermelho)
5. Fix do prompt/guardrail
6. Test agora passa (cor: verde)
7. CI agora sempre roda esse teste
8. Bug nunca volta
```

É como vacinar o sistema com seus próprios bugs — paráfrase da postura defendida por Hamel Husain em *Your AI Product Needs Evals*. Em 6 meses, golden set acumula 50-100 bug regression tests. Em 12 meses, vira o ativo mais valioso do produto.

## Anti-patterns

- **String diff puro** — falsos positivos em 60%+ dos casos
- **Semantic diff sem calibração** — threshold de embedding chutado, ruído permanente
- **Reblessing automático** — qualquer regressão é "intencional", elimina o sinal
- **Sem categorias** — correctness regression e calibration regression no mesmo balde
- **Threshold uniforme** — safety com mesma tolerância de calibration é erro de prioridade
- **Bugs não viram regression test** — mesmos bugs voltam mês após mês
- **Rebless sem razão escrita** — em 3 meses ninguém lembra por que aquele item mudou

## Armadilhas comuns

> [!warning] Reblessing automático — eliminar o sinal de regressão sem perceber
> A armadilha mais insidiosa no regression testing é automatizar o rebless. Parece eficiente: CI falhou, script atualiza o golden set, PR passa verde. Na prática, você acabou de desligar o alarme de incêndio porque ele estava barulhento. Em 3 meses o golden set reflete o comportamento atual do modelo, não o comportamento desejado — e você perdeu a capacidade de detectar regressão. A regra é rigorosa: rebless sempre exige humano lendo o diff e escrevendo a razão. Automatizar pode gerar o arquivo, mas o botão de aprovação deve ser humano.

> [!warning] Threshold único para todas as categorias de regressão
> Usar o mesmo threshold de tolerância para correctness e para calibration é erro de prioridade. Regressão de correctness significa que o modelo respondeu errado — zero tolerância. Regressão de calibration (confidence scores ligeiramente diferentes, distribuição de severidades levemente deslocada) tem variância natural e pode tolerar 5-10%. Quando você usa threshold único, uma das duas coisas acontece: ou o threshold é alto demais (regressões de correctness passam silenciosamente) ou é baixo demais (ruído de calibration gera falsos positivos que o time ignora). Configure threshold por categoria — é trabalho de uma hora mas salva a sanidade do pipeline.

> [!warning] Bugs de produção não virando regression tests permanentes
> O ciclo mais comum em times sem regression testing estruturado: bug é reportado em produção → debug → fix → deploy → mesmo bug volta 2 meses depois em mudança diferente de prompt. A raiz é que o bug foi corrigido mas nunca foi capturado como test case. A disciplina certa: cada bug que chega de produção vai imediatamente para o golden set como regression test que **falha** no código atual, e só é fechado quando o fix faz o test passar. Em 6 meses isso constrói um corpus de defesa que cobre todos os bugs reais do sistema — muito mais valioso do que casos sintéticos inventados antes de prod.

## Como explicar em inglês

Em entrevistas sobre qualidade e reliability de sistemas LLM, regression testing é o que separa times que operam em produção de times que operam em demo:

> "Regression testing in LLMs is snapshot diff: capture golden-set outputs for prompt v1, run v2, compare. The non-trivial part is that LLMs are non-deterministic — string equality produces constant false positives. You need semantic diff: schema equality for structured fields, embedding cosine similarity for free text, and equivalence judge for critical subjective cases. You also need categories with separate thresholds — correctness regressions are blockers, calibration regressions tolerate maybe 10%. Every production bug should become a permanent regression test. And rebless decisions — updating approved snapshots — always require a human writing the reason."

| Português | Inglês |
|-----------|--------|
| regressão de output | output regression |
| diff semântico | semantic diff |
| snapshot de golden set | golden set snapshot |
| threshold de tolerância | tolerance threshold |
| rebless (atualizar snapshot) | rebless / update approved baseline |
| regressão de segurança | safety regression |
| diff de string puro | raw string diff |
| similaridade de embedding | embedding cosine similarity |
| judge de equivalência | equivalence judge |
| caso de teste de bug | bug regression test case |

## O que vem a seguir

Com regression testing cobrindo a detecção de quebras entre versões, a nota 06 expande o horizonte ferramental: quais frameworks de eval existem em 2026 (Promptfoo, Braintrust, Langfuse, Patronus, Phoenix), o que cada um oferece, e como escolher.

Ver [[06 - Frameworks 2026 — Promptfoo, Braintrust, Langfuse, Patronus, Phoenix]].

## Veja também

- [[02 - Golden datasets — como construir]] — dataset é a base do regression
- [[03 - Scoring rubrics e critérios]] — thresholds vêm da rubrica
- [[04 - LLM-as-judge — quando e como]] — equivalence judge
- [[07 - Eval em CI-CD]] — onde o regression test roda
- [[03-Dominios/Tecnologia/IA/Anatomia de Agents/09 - Evaluation de agents]] — regression em agents acumulado

## Fontes

- **Hamel Husain** — [*Your AI Product Needs Evals*](https://hamel.dev/blog/posts/evals/) — seção sobre regression
- **Promptfoo docs** — [*Snapshot testing*](https://promptfoo.dev/docs/configuration/expected-outputs/) — pattern canônico em OSS
- **Braintrust** — *Regression detection patterns* (docs, 2026)
- **Eugene Yan** — *Patterns for Building LLM-based Systems* (2024)
- **OpenAI** — [*Evals — regression patterns*](https://github.com/openai/evals)
