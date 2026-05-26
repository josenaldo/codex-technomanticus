---
title: "Guia de implementação SDD — do zero ao projeto"
created: 2026-05-02
updated: 2026-05-02
type: concept
status: seedling
publish: true
tags:
  - sdd
  - ia
  - metodologia
  - guia
  - pratica
aliases:
  - SDD adoption
  - Guia SDD
  - Implementação SDD
---

# Guia de implementação SDD — do zero ao projeto

> [!abstract] TL;DR
> Esta nota é o roteiro prático para adotar SDD num projeto real, do zero. Não é teoria — é checklist semana-a-semana. Stack assumida: Spec Kit + Claude Code (mais documentado), mas o roteiro funciona com Kiro/Cursor/qualquer agente. Padrão recomendado: começar em **spec-first**, evoluir para **spec-anchored** após 2-4 semanas, considerar **spec-as-source** só se compliance ou domínio justificarem. Roadmap de 12 semanas para chegar em maturidade.

## Pré-requisitos

> [!info] O que precisa estar no lugar
> 1. **AGENTS.md** existente ou disposto a criar (ver [[Context Engineering|11 - Skills e instructions como contexto]])
> 2. **Repositório git** ativo (specs vão versionadas)
> 3. **Pipeline CI mínimo** (vai precisar de gates)
> 4. **Pelo menos um agente configurado** ([[Dicionário de IA#Claude Code|Claude Code]], [[Dicionário de IA#Cursor|Cursor]], Kiro)
> 5. **Time de acordo** — SDD não funciona com adoção parcial, todo mundo segue
> 6. **[[Dicionário de IA#Prompt caching|Prompt caching]] ativo** ([[Economia de Tokens|05 - Prompt caching na prática]]) — specs são prefix cacheável ideal

## Semana 0 — Decisão de adoção

### Avaliar fit

> [!question] SDD faz sentido pro seu projeto?
> - [ ] Time >1 pessoa OU vai escalar
> - [ ] Código vai viver >3 meses
> - [ ] Compliance/auditoria importa OU vai importar
> - [ ] Dor real com tech debt de IA
> - [ ] Disposição a 2-4 semanas de adoção
>
> 4+ marcadas → vale.

### Escolher ferramenta

Ver [[08 - Ferramentas SDD — Kiro, Spec Kit, OpenSpec, Tessl]]. Default recomendado: **GitHub Spec Kit** + agente já em uso.

### Definir nível inicial

[[03 - Níveis de rigor — spec-first, spec-anchored, spec-as-source]]. Default: **spec-first** (subir depois).

## Semana 1 — Setup e primeira spec

### Setup técnico

```bash
# Instalar Spec Kit
pip install specify-cli

# Inicializar no projeto
cd meu-projeto
specify init

# Estrutura criada:
# specs/
# .specify/config.yml
```

### Configurar AGENTS.md (se não existir)

```markdown
# Projeto X

## Build & Test
- ...

## Conventions
- ...

## Spec-Driven Development
- Specs vivem em `specs/<feature>/spec.md`
- Plans vivem em `specs/<feature>/plan.md`
- Antes de implementar uma feature, leia spec + plan
- Mudança comportamental → atualizar spec primeiro
```

### Primeira spec — escolha algo pequeno

Pegue uma feature **pequena** mas real. Não comece pelo módulo mais complexo. Algo como "endpoint de health check" ou "validação de email".

```bash
specify add "Health check endpoint"
# Gera prompt; agente produz primeira draft de spec
```

Edite manualmente — primeira spec **deve ser revisada com cuidado**, ela vira template mental para o time.

## Semana 2 — Plan + tasks + primeira implementação

### Plan

```bash
specify plan health-check
# Gera plan a partir da spec
```

Revise. Tipicamente plan auto-gerado tem:
- ✅ Decisões básicas razoáveis
- ⚠️ Stack pode estar over-engineered
- ⚠️ Tasks podem estar com granularidade errada

Ajuste antes de seguir.

### Tasks

```bash
specify tasks health-check
# Decompõe plan em tasks numeradas
```

Cada task deve passar a "regra das 3h". Quebre tasks gigantes.

### Implement

Use o agente normal (Claude Code, Cursor) com instrução clara:

> *"Trabalhar em `specs/health-check/tasks.md`. Pegue a próxima task `[ ]`. Spec e plan estão em `specs/health-check/`. Use-os como referência. Marque `[x]` quando teste do AC passar."*

Execute task por task. Não pule. Não junte.

### Primeira lição

Provavelmente vai descobrir:
- Spec ainda tem ambiguidades → corrige spec
- Plan tem decisão que não funciona → corrige plan
- Task estava grande demais → quebra

**É esperado.** SDD se aprende fazendo. Documente o que aprendeu.

## Semanas 3-4 — Adoção pelo time

### Documentar o workflow

Criar `docs/SDD-WORKFLOW.md` no projeto:

```markdown
# Como fazer feature com SDD

1. Pegue ticket → cria branch
2. Escreve `specs/<feature>/spec.md` (use template)
3. PR da spec **isolado** (review do PM + tech lead)
4. Após spec aprovada: `specify plan <feature>`, revisa plan
5. PR do plan (review do tech lead)
6. Após plan aprovado: `specify tasks <feature>`, gera lista
7. Trabalha task-a-task usando agente
8. PR final com todas as tasks done + tests + drift gate verde
```

### Treinar o time

Sessão prática: pegar uma feature real, fazer junto, mostrar o ganho. Resistências comuns:

| Reclamação | Resposta |
|---|---|
| "Demora mais" | Curto prazo sim. Em 2 sprints, mais rápido (menos rework) |
| "Burocracia" | Agente faz draft de spec; revisão é minutos |
| "Perdemos flexibilidade" | Mudança de spec é PR — flexível, mas registrado |
| "Não preciso disso" | Mostre os números do tech debt acumulado |

## Semanas 5-8 — Subir para spec-anchored

### Adicionar drift gate

Ver [[07 - Fase Validate — spec como contrato executável]]. Adicionar ao CI:

```yaml
- name: Spec-code drift check
  run: specify verify --drift
```

Falha o PR se spec menciona endpoint que código não tem (ou vice-versa).

### Adicionar coverage gate

```yaml
- name: AC coverage
  run: specify verify --coverage --min=100
```

Cada AC precisa ter teste vinculado.

### PR template

```markdown
## Feature
Link para spec: `specs/X/spec.md`

## Mudanças
- [ ] Spec atualizada (se mudança comportamental)
- [ ] Plan atualizado (se mudança arquitetural)
- [ ] Todas tasks marcadas [x]
- [ ] AC test coverage 100%
- [ ] Drift gate verde
```

## Semanas 9-12 — Maturidade

### Métricas em dashboard

| Métrica | Onde medir |
|---|---|
| % features com spec antes de código | Custom — count de PRs que tem spec/ no diff |
| Drift detectado (ratio) | CI logs |
| Tempo médio specify→merge | Issue/PR analytics |
| AC coverage | spec-kit relatório |
| Tech debt issues criados | GitHub issues label |

### Revisar e ajustar

A cada 3 sprints:
- Specs muito vagas? → reforçar [[04 - Fase Specify — definindo outcomes e constraints|specify]]
- Drift frequente? → suba para [[03 - Níveis de rigor — spec-first, spec-anchored, spec-as-source|nível anchored mais rígido]]
- Validation lenta? → otimize CI, parallelize gates
- Time achou burocrático? → simplifique template

## Considerar spec-as-source (mês 4+)

> [!warning] Não pule semanas para chegar aqui
> Spec-as-source só faz sentido se time **já domina** spec-anchored. Pular etapas = adoção fracassada.

Sinais de que vale subir:
- Compliance regulado (financeiro, médico)
- Múltiplas implementações (web + mobile + API)
- Time grande com necessidade de governance forte

Sinais de que **não** vale:
- Domínio criativo / exploratório
- Time não modela formalmente
- Stack heterogênea sem geradores compatíveis

## Multi-agent SDD (opcional, mês 5+)

Quando spec-anchored está sólido, considere [[09 - SDD com agentes — coordinator, implementor, validator|CIV]] para features grandes. Stack típica:
- Claude Code para implementor (uma sessão por task)
- Custom validator script ou outro agente
- Coordinator manual (humano + agente)

Em Kiro: subagents nativos resolvem.

## Sinais de adoção bem-sucedida

| Sintoma | Significado |
|---|---|
| PRs ficaram menores | Tasks pequenas, foco mantido |
| Reuniões "alinhamento" diminuíram | Specs comunicam |
| Onboarding de novo dev mais rápido | Specs são doc viva |
| Bugs em prod diminuíram | Validation pega |
| Time entende mais o que está sendo construído | Specs forçam clareza |

## Sinais de adoção falhando

| Sintoma | Provável causa |
|---|---|
| Specs viram template padrão sem substância | Falta revisão; fix: tech lead bloqueia PR de spec ruim |
| Drift gate sempre amarelo, ninguém olha | Soft warning vira ruído; faça hard fail |
| Time pula spec "para feature urgente" | Falta cultural; reforce no PR review |
| Specs ficam stale | Não está em anchored; suba o nível |
| Volume de specs explode | Tasks grandes demais; refine granularidade |

## Veja também

- [[02 - O que é Spec-Driven Development]]
- [[03 - Níveis de rigor — spec-first, spec-anchored, spec-as-source]]
- [[08 - Ferramentas SDD — Kiro, Spec Kit, OpenSpec, Tessl]]
- [[Context Engineering|14 - Context engineering na prática — setup completo]]
- [[12 - Debates — spec-as-source vs pragmatismo]]

## Referências

- **GitHub Blog** — *Spec-driven development with AI: Get started* (2025).
- **Microsoft for Developers** — *Diving Into Spec-Driven Development With GitHub Spec Kit* (2026).
- **Augment Code** — *What Is Spec-Driven Development? A Complete Guide* (2026).
- **Zencoder Docs** — *A Practical Guide to Spec-Driven Development* (2026).
- **DeepLearning.AI / JetBrains** — *Spec-Driven Development with Coding Agents* course (2026).
