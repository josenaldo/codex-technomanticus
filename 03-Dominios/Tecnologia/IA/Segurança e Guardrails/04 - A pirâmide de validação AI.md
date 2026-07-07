---
title: "A pirâmide de validação AI"
created: 2026-05-02
updated: 2026-07-06
type: concept
fase: Iniciado
progress: backlog
status: seedling
publish: true
tags:
  - seguranca-ia
  - ia
  - guardrails
  - validation
aliases:
  - Validation pyramid
  - Pirâmide de validação
  - Defense in depth AI
---

# A pirâmide de validação AI

> [!abstract] TL;DR
> Nenhuma camada sozinha protege contra os 45% de [[01 - Código gerado por IA é untrusted|código inseguro]] e [[02 - Slopsquatting — o ataque via alucinação|supply chain attacks]]. A solução é **defesa em profundidade** estruturada como pirâmide: na base, **automação massiva** (linters, type checkers, SAST escalando para milhares de PRs); no meio, **[[Dicionário de IA#Guardrail|guardrails]] determinísticos** ([[Context Engineering|12 - Guardrails determinísticos]]) que param classes de ataque conhecidas; no topo, **human oversight** focado nos poucos casos que merecem revisão humana profunda. Triângulo invertido onde tem o problema.

> [!question]- Por que pirâmide e não checklist plano de validação?
> Um checklist plano trata todos os itens como equivalentes e atribui o trabalho de revisão ao humano. Com o volume de código gerado por IA, um checklist de 20 itens por PR significa que um time que revisa 100 PRs/semana faz 2.000 revisões manuais — impraticável. A pirâmide resolve isso pela especialização: automação faz o que é codificável (90%+ dos casos), guardrails determinísticos fazem o que tem regra clara, e o humano faz apenas o que exige julgamento real. Cada camada filtra o que não devia chegar à camada seguinte, reduzindo o volume e aumentando a qualidade da revisão humana.

## A pirâmide

```mermaid
graph TD
    A["🔴 Human oversight<br/>(1-5% dos casos)"] --> B["🟡 Deterministic guardrails<br/>(blocking checks)"]
    B --> C["🟢 Automation<br/>(linters, SAST, tests)"]
    C --> D["⚪ Generation<br/>(LLM gerando código)"]
```

**Fluxo:** geração → automação → guardrails → humano. Cada camada filtra. Humano só vê o que precisa de julgamento real.

## Por que pirâmide e não checklist

A tentação é "escrever uma lista grande de coisas pra revisar". Falha porque:

- Volume gerado por IA esmaga revisão linear
- Humano fadiga em casos rotineiros, deixa passar casos sérios
- Custo escala linearmente com volume → caro
- Cada camada está fazendo o trabalho errado

Pirâmide é **especialização por camada**: máquina faz o que máquina faz bem; humano faz o que humano faz bem.

## Camada 1 — Automação (90-95% do trabalho)

A base larga. Roda em **todo PR**, em **todo commit**, sem exceção.

| Ferramenta | Pega |
|---|---|
| **Type checker** (mypy, tsc) | Métodos/tipos inexistentes ([[03 - Alucinações em código — APIs fantasma e parâmetros inexistentes]]) |
| **Linter** (ruff, eslint) | Padrões de código, dead code, antipatterns |
| **SAST** (Snyk, Semgrep, CodeQL) | OWASP-grade vulns ([[05 - SAST e SCA para código AI]]) |
| **SCA** (Snyk, Socket.dev) | Slopsquat, dep vulneráveis ([[02 - Slopsquatting — o ataque via alucinação]]) |
| **Test suite** | Comportamento ([[09 - Testes imutáveis — a barreira que o agente não pode reescrever]]) |
| **Format check** | Estilo |

**Critério de qualidade:** todas estas DEVEM **bloquear PR** se falharem. Não devem ser warnings ignorados.

## Camada 2 — Guardrails determinísticos (4-9%)

Quando automação genérica não basta — regras **específicas do projeto**:

| Guardrail | Exemplo |
|---|---|
| **Schema validation** | Output do LLM tem `extra="forbid"` em Pydantic |
| **Permission boundaries** | Agente não pode chamar tools fora do allowlist ([[06 - Permissões e sandboxing]]) |
| **Rate limits** | LLM não faz >N tool calls por turno |
| **Sensitive operation gating** | Mudanças em DB de prod requerem human approval |
| **Output format enforcement** | JSON mode, structured outputs |
| **Domain-specific rules** | "Nenhuma string SQL concatenada com user input" |
| **Hallucination check** | Pacotes verificados em registry oficial antes de install |

Ver [[Context Engineering|12 - Guardrails determinísticos]] para fundamento.

**Critério:** regras **codificáveis**. Se você consegue escrever a regra, escreva a regra. Não delegue julgamento determinístico para [[Dicionário de IA#LLM (Large Language Model)|LLM]].

## Camada 3 — Human oversight (1-5%)

Para o que sobrou: julgamento real.

**O que humano faz bem:**
- Revisão de **arquitetura** (decisões com trade-offs ambíguos)
- Avaliação de **mudanças cross-cutting** (security policy, auth)
- Verificação de **intent** (o código atende ao "porquê" da feature?)
- Aprovação de **operações destrutivas** (drop table, force push)
- Escalação de **incidentes** detectados pelas camadas inferiores

**O que humano NÃO faz bem (deixe para máquina):**
- Detectar XSS em template
- Achar SQL injection escondido
- Verificar 50 linhas de imports
- Confirmar que typescript types batem
- Checar que pacote npm existe

> [!warning] Review fatigue mata
> Time que aprova 100 PRs/semana **não revisa** o de número 47. Camadas 1 e 2 existem para que a camada 3 só receba **5 PRs/semana** que **realmente precisam** de olhar humano.

## Anatomia do pipeline ideal

```yaml
# .github/workflows/ai-code-validation.yml
on: [pull_request]

jobs:
  layer1-automation:
    steps:
      - name: Type check (BLOCK)
        run: mypy src/
      - name: Lint (BLOCK)
        run: ruff check src/
      - name: SAST (BLOCK)
        run: semgrep --config=auto --error
      - name: SCA (BLOCK)
        run: snyk test --severity-threshold=high
      - name: Test suite (BLOCK)
        run: pytest
      - name: Coverage (BLOCK if < 80%)
        run: pytest-cov --fail-under=80

  layer2-guardrails:
    needs: layer1-automation
    steps:
      - name: Schema validation
        run: ./scripts/check-schemas.sh
      - name: Permission boundary check
        run: ./scripts/check-tool-allowlist.sh
      - name: Sensitive ops gate
        if: contains(github.event.pull_request.changed_files, 'migrations/')
        run: echo "::warning::DB migration detected - human approval required"

  layer3-routing:
    needs: layer2-guardrails
    steps:
      - name: Auto-route review
        run: ./scripts/route-review.sh
        # Sensitive PR → senior + security-reviewer
        # Routine PR → any reviewer
```

## Implementação progressiva

Não tente tudo de uma vez. Roadmap típico (ver também [[12 - O roadmap de segurança para times]]):

| Semana | Adiciona |
|---|---|
| 1 | Type check + linter (bloqueando) |
| 2 | Test suite obrigatório + coverage threshold |
| 3 | SAST básico (Semgrep config=auto) |
| 4 | SCA (Snyk ou Socket.dev) |
| 5-6 | Schema validation em boundaries |
| 7-8 | Permission boundaries para agentes |
| 9-10 | Routing inteligente de review humano |
| 11-12 | Métricas e ajuste fino |

## Quando uma camada falha

| Falha | Sintoma | Fix |
|---|---|---|
| **Camada 1 lenta** | CI demora >15 min, time pula validação | Otimize, paralelize, incremental |
| **Camada 1 com falsos positivos** | Time desativa rule | Calibre rules, suppress com comentário |
| **Camada 2 muito rígida** | Bloqueio em casos legítimos | Refine regras com base em casos reais |
| **Camada 2 muito frouxa** | Issues passam | Adicione regra específica para o pattern |
| **Camada 3 fadigada** | Reviews superficiais | Aumente camadas 1 e 2 para reduzir volume |

## Métricas da pirâmide

| Métrica | Alvo | Significado |
|---|---|---|
| **% PRs bloqueados em camada 1** | 30-50% | Sinal saudável — automação funciona |
| **% PRs bloqueados em camada 2** | 5-15% | Guardrails calibrados |
| **% PRs revisados manualmente** | <10% | Humano focado |
| **Tempo médio CI total** | <15 min | Não sufoca produtividade |
| **Defect escape rate** | <5% | Issues que chegam em prod |
| **% issues detectados em prod (não em CI)** | <10% | Pirâmide está pegando |

## Anti-patterns

- **"Vamos só fazer review humano com mais cuidado"** — não escala com volume IA
- **SAST como warning, não erro** — vira ruído
- **Camada 2 por LLM ("AI critic")** — contraditório; quem valida o validador?
- **Pular camada 1 "para mover rápido"** — produção paga depois
- **Métricas só em camada 3** — perde sinal das anteriores
- **Single-vendor SAST** — Veracode mostra: 78% dos issues só pegos por uma das ferramentas; **rode 2+**
- **Coverage % como proxy de qualidade** — teste que roda sem `assert` de verdade infla o número sem pegar regressão nenhuma; a métrica vira meta, não sinal (efeito Goodhart clássico)
- **Guardrails da camada 2 vivendo soltos em scripts sem review** — regra de negócio codificada num shell script isolado, sem changelog nem dono, sofre drift silencioso: ninguém percebe quando ela para de cobrir o caso que deveria bloquear

## Armadilhas comuns

> [!warning] Camada 1 lenta vira camada ignorada
> CI que demora 20 minutos leva desenvolvedores a abrir PRs sem esperar o resultado, ou a pular validações locais "para ganhar tempo". O sinal de alerta é quando o time começa a fazer merge antes do CI terminar. Se a camada 1 fica lenta, paralelize as etapas, use cache agressivo de dependências, e separe checks rápidos (linter, type check) dos lentos (testes de integração) em jobs distintos.

> [!warning] Usar LLM como validador da camada 2 é circular
> Alguns times tentam usar um "AI critic" para revisar o output de outro LLM como guardrail da camada 2. O problema: o validador tem os mesmos pontos cegos que o gerador, pode ser iludido pelas mesmas construções plausíveis, e não tem garantia determinística. Guardrails da camada 2 precisam ser regras codificáveis com resultado binário — não "o outro LLM achou OK".

> [!warning] SAST único vendor garante cobertura falsa
> O relatório Veracode mostra que 78% das vulnerabilidades são detectadas por apenas uma das ferramentas SAST testadas. Rodar só Semgrep ou só CodeQL deixa classes inteiras de problema sem cobertura. A pirâmide precisa de pelo menos dois scanners na camada 1, complementares em cobertura.

## Como explicar em inglês

The validation pyramid for AI-generated code solves a fundamental throughput problem: a human reviewer cannot keep pace with the volume that an LLM-assisted team produces. The pyramid structures validation so that the high-volume, codifiable checks happen automatically — type checking, linting, SAST, SCA — and only the edge cases that genuinely require judgment reach a human reviewer.

The key insight is specialization by layer. Machines are better than humans at consistently catching XSS patterns, missing type declarations, and vulnerable dependency versions — tasks that are repetitive, well-defined, and don't benefit from context. Humans are better at evaluating architectural trade-offs, security implications of cross-cutting changes, and intent alignment. Mixing those responsibilities in a single flat checklist wastes human capacity on mechanical tasks and exhausts reviewers before they reach the decisions that matter.

A well-implemented pyramid means that 90-95% of issues are caught before a human sees the PR, and the human reviewer spends their time on the 5-10% where their judgment creates real value.

**In a technical interview**, you might say:

> "We structure AI code validation as a three-layer pyramid. The base is full automation — type checker, linter, SAST with two complementary scanners, SCA for dependency safety, and a test suite — all as hard blocks in CI. The middle layer is deterministic guardrails specific to our domain: schema validation with `extra=forbid`, tool allowlists for agents, and human approval gates for destructive operations. The top is human review, but only for the PRs that actually need judgment — architecture decisions, cross-cutting security changes, intent verification. This way our reviewers see maybe 5-10% of PRs, but those are the ones where human judgment matters."

| PT | EN |
|----|-----|
| defesa em profundidade | defense in depth |
| pirâmide de validação | validation pyramid |
| automação de base | base automation layer |
| guardrail determinístico | deterministic guardrail |
| revisão humana | human oversight |
| taxa de escape de defeitos | defect escape rate |
| fadiga de revisão | review fatigue |
| roteamento de revisão | review routing |
| validação em camadas | layered validation |
| pipeline de CI | CI pipeline |

## O que vem a seguir

A pirâmide define a estrutura. A camada 1 — automação — é a mais larga e a mais crítica para escalar. Mas ferramentas SAST e SCA genéricas não foram projetadas para código gerado por IA: elas não sabem distinguir padrões que humanos evitariam mas que LLMs reproduzem sistematicamente, e precisam de ajuste para lidar com o volume e os padrões específicos desse fluxo.

A próxima nota detalha como calibrar SAST e SCA especificamente para código AI, incluindo quais regras ativar, quais ferramentas combinar, e como evitar que falsos positivos tornem a camada ineficaz.

- [[05 - SAST e SCA para código AI]] — calibrando as ferramentas de análise estática para o contexto de geração por LLM

## Veja também

- [[05 - SAST e SCA para código AI]]
- [[06 - Permissões e sandboxing]]
- [[07 - Security-focused prompting]]
- [[08 - Code review de código AI — o que muda]]
- [[Context Engineering|12 - Guardrails determinísticos]]

## Referências

- **Veracode** — [*2025 GenAI Code Security Report*](https://www.veracode.com/resources/analyst-reports/2025-genai-code-security-report/) (2025).
- **DryRun Security** — [*Top 10 AI SAST Tools for 2026*](https://www.dryrun.security/blog/top-ai-sast-tools-2026) (2026).
- **NVIDIA** — [*Practical Security Guidance for Sandboxing Agentic Workflows and Managing Execution Risk*](https://developer.nvidia.com/blog/practical-security-guidance-for-sandboxing-agentic-workflows-and-managing-execution-risk/) (2026).
- **Anthropic** — [*Making Claude Code more secure and autonomous with sandboxing*](https://www.anthropic.com/engineering/claude-code-sandboxing) (2025).
- **OWASP** — [*Top 10 for LLM Applications 2025*](https://genai.owasp.org/llm-top-10/) (2025).























































