---
title: "Debates — spec-as-source vs pragmatismo"
created: 2026-05-02
updated: 2026-05-02
type: concept
status: seedling
publish: true
tags:
  - sdd
  - ia
  - metodologia
  - debate
aliases:
  - Críticas SDD
  - SDD limitations
  - Quando não usar SDD
  - SDD vs waterfall
---

# Debates — spec-as-source vs pragmatismo

> [!abstract] TL;DR
> SDD não é unanimidade. Em 2026, três críticas legítimas circulam: **(1) é waterfall reciclado**, **(2) custo upfront mata velocidade**, **(3) spec-as-source é over-engineering para a maioria**. Entender as críticas separa quem aplica SDD com discernimento de quem aplica como dogma. Esta nota fecha a trilha com posições contrárias, limites concretos do método, e quando explicitamente **não** usar SDD.

## As três críticas mais fortes

### Crítica 1 — "É waterfall reciclado"

> *"Vocês definem tudo antes de codar. Se isso não é waterfall, o que é?"*

**Onde a crítica acerta:**
- A fase Specify lembra waterfall em nome
- O hábito de "spec antes de código" é genuinamente uma volta a princípios pré-agile
- Times que aplicam mal SDD viram waterfall com markdown

**Onde a crítica erra:**
- Specs em SDD são **incrementais por feature**, não documentos gigantes
- Iteração rápida (mudança de spec = PR atomizado, não projeto refeito)
- Spec é executável (validação contínua), não papel assinado
- Validate retroalimenta Specify — ciclos curtos, não fase única longa

**Posição honesta:** SDD **resgata partes boas** do rigor pré-ágil sem reviver as partes ruins. Mas time descuidado pode regredir.

### Crítica 2 — "Custo upfront mata velocidade"

> *"Antes eu fazia em 2 dias. Agora gasto 1 dia em spec + 1 em plan + 1 em review = 3 dias para a mesma feature."*

**Onde a crítica acerta:**
- Adoção tem curva de 2-4 semanas; primeiras features são mesmo mais lentas
- Para protótipos, é overkill garantido (ver "Quando não usar")
- Time que **só faz features pequenas isoladas** não se beneficia tanto

**Onde a crítica erra:**
- Compara dia 1 vs dia 1, não trimestre vs trimestre
- Ignora retrabalho evitado, bugs evitados, drift evitado
- Em 6 meses, dados consistentes mostram **velocidade líquida maior** com SDD
- "Velocidade" sem qualidade é dívida que cobra com juros

**Posição honesta:** SDD é investimento. ROI real aparece após sprint 3. Times com horizonte curto (<2 sprints) não recuperam.

### Crítica 3 — "Spec-as-source é over-engineering para a maioria"

> *"Lean 4 verification, OpenAPI generators, Tessl... isso é fantasy land para 99% dos projetos."*

**Onde a crítica acerta** — completamente:
- [[03 - Níveis de rigor — spec-first, spec-anchored, spec-as-source|Spec-as-source]] (nível 3) é caro de adotar
- Domínios criativos e exploratórios não modelam bem
- Maior parte dos projetos não precisa
- Hype confunde — "todo mundo deveria fazer spec-as-source" é falso

**Resposta honesta:** Concordo. O nível certo é **spec-anchored** (nível 2) para a maioria. Spec-as-source é nicho. Defender SDD não é defender spec-as-source — é defender que **alguma forma de contrato explícito beat vibe coding**.

## Quando explicitamente NÃO usar SDD

| Cenário | Por que não |
|---|---|
| **Hackathon de fim de semana** | Vida útil do código <72h; overhead não amortiza |
| **Throwaway prototype** | Spec é desperdício se código será descartado |
| **Exploração inicial / "spike"** | Você ainda não sabe o que está construindo |
| **Bug fix isolado de 1 linha** | Spec para isso é teatro |
| **Aprendizado pessoal / tutorial** | Foco é entender, não governar |
| **Time avesso a estrutura** | SDD parcial = pior dos dois mundos |
| **Domínio totalmente novo sem precedentes** | Não há base para spec — explore primeiro, formalize depois |

## Limites genuínos do método

### Domínios criativos

ML research, data science exploratório, design generativo. O caminho do problema é fluido — formalizar adiantado mata a exploração.

**Solução:** SDD na borda (interfaces estáveis), vibe coding no núcleo experimental. Híbrido por área.

### Brownfield com tech debt extremo

Codebase com 0 testes, sem doc, com 5 anos de mudanças sem rastro. Tentar fazer SDD greenfield-style nele é desastre.

**Solução:** BMAD ou abordagens incrementais — spec retroativa por módulo, não tudo de uma vez.

### Times sem disciplina mínima

Se code review é simbólico, se ninguém roda lint, se PRs são "approve" no automático — SDD não vai magicamente trazer disciplina. Vai virar mais um ritual ignorado.

**Solução:** investir em **fundamentos** (CI, code review real, AGENTS.md básico) **antes** de tentar SDD.

### Specs que não conseguem ser machine-readable

Algumas tarefas têm critérios genuinamente subjetivos ("a UI deve ficar bonita"). Spec pode declarar, mas validação automática é limitada.

**Solução:** SDD parcial — spec descreve, validação semi-manual. Aceitar que nem tudo automatiza.

## A controvérsia "specs por LLM"

Posições no debate:

> "Se a spec é gerada por LLM, ela carrega o mesmo viés que o código gerado teria. Não resolve o problema, só transfere."

**Resposta:** verdade, mas:
- Humano revisa spec **antes** de virar contrato
- Spec é pequena (1-3 páginas), revisão é minutos
- Erros em spec são detectáveis por humano (semântica)
- Erros em código são mais sutis (lógica)

Revisar spec gerada > revisar código gerado.

## A controvérsia "drift gates como religião"

> "Vocês falham PR porque uma vírgula da spec não bate com o código. Isso é caroço."

**Resposta:** drift gate **calibrado** falha em casos relevantes (endpoint missing, AC sem teste). Drift gate **mal calibrado** falha em coisas irrelevantes.

Sintoma: time desativa o gate. Solução: ajusta o gate, não desativa o método.

## Quando o método "te trai"

Casos reais onde SDD piorou:

| Caso | Causa | Lição |
|---|---|---|
| Specs gigantescas que ninguém lê | Falta de granularidade | Quebrar features menores |
| Specs sempre stale | Nível spec-first onde precisava anchored | Subir o nível |
| PRs bloqueados eternamente em validation | Gates muito rígidos | Calibrar gates |
| Time produzia menos | Ferramentas pesadas em projeto pequeno | Voltar para Spec Kit simples |
| Devs frustrados | Adoção forçada | Adoção precisa de buy-in |

## Quando reverter

> [!tip] Sinais de que SDD está machucando, não ajudando
> - PRs sentindo-se "engessados" por mais de 4 semanas
> - Time produz menos vs trimestre anterior (líquido, não bruto)
> - Specs viram cópias de templates sem revisão
> - Drift gate falha em 30%+ dos PRs sem motivo real
> - Burnout do time
>
> Se 3+: pause, simplifique, possivelmente reverta para nível mais leve.

## Posição honesta de fechamento

SDD não é "a metodologia certa para todos". É **uma resposta calibrada** ao tech debt do vibe coding em **contextos específicos**:
- Time pequeno-médio
- Código com vida útil >meses
- Disposição a 2-4 semanas de adoção
- Domínio modelável

Em outros contextos (protótipos, exploração, hackathons), use o que funciona. [[Andrej Karpathy|Karpathy]] chamou vibe coding de "libertador" para um público específico — ele estava certo. **A virtude está na escolha, não no dogma.**

## A contribuição duradoura do SDD

Mesmo que daqui a 5 anos a metodologia mude de nome, **três princípios** sobrevivem:

1. **Tornar intent explícito é melhor que deixar agente inferir**
2. **Validação mecânica é melhor que olhômetro**
3. **Contexto persistente versionado é melhor que contexto efêmero**

Quem internaliza esses princípios — com SDD ou outro nome — vai estar bem em qualquer ferramenta futura.

## Veja também

- [[01 - O problema do vibe coding em produção]] — o problema que SDD endereça
- [[03 - Níveis de rigor — spec-first, spec-anchored, spec-as-source]] — escolha do nível certo
- [[11 - Guia de implementação SDD — do zero ao projeto]] — como adotar com cuidado
- [[Agentes de Codificação|02 - Vibe coding vs engenharia disciplinada]]

## Referências

- **Andrej Karpathy** — *Vibe coding* (2025, posição original).
- **Salesforce Ben** — *2026 Predictions: It's the Year of Technical Debt* (2026, posição "vibe coding gerou crise").
- **Augment Code** — *Cursor 3 vs Intent: Prompt-Driven vs Spec-Driven Agents* (2026, debate de posições).
- **Techzine Global** — *Vibe coding vs Spec-Driven Development* (2026).
- **Pixelmojo** — *The AI Coding Technical Debt Crisis: 2026-2027* (2026).
- **arxiv:2512.11922** — *Vibe Coding in Practice: Flow, Technical Debt, and Workarounds* (2025).
