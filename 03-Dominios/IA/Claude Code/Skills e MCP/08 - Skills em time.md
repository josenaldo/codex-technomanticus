---
title: "Skills em time — versionar, manter, compartilhar"
type: concept
publish: true
created: 2026-05-13
updated: 2026-05-13
status: seedling
tags:
  - claude-code
  - skills
  - time
  - versionamento
  - manutencao
---

# Skills em time — versionar, manter, compartilhar

> [!abstract] TL;DR
> Skills em `.claude/skills/` são versionadas junto ao código — qualquer dev que clona o repo tem acesso imediato. O desafio não é técnico: é manter as skills atualizadas conforme o projeto evolui e garantir que o time as conhece e as usa. Skills desatualizadas são ativamente prejudiciais: o agente segue um processo que o projeto abandonou.

## Por que versionar no repo

Skills em `.claude/skills/` são commitadas junto ao código. Vantagens:

- Todo dev que clona o repo tem as mesmas skills
- Mudanças nas skills aparecem no histórico git — você sabe quando e por que uma convenção mudou
- Code review de skills funciona igual a code review de código
- CI pode verificar se as skills estão consistentes com o código

Comparando com `~/.claude/skills/` (global, pessoal):

| | `.claude/skills/` (projeto) | `~/.claude/skills/` (global) |
|--|---------------------------|------------------------------|
| Escopo | Este projeto | Todos os projetos |
| Versionamento | git do projeto | Só em você |
| Compartilhamento | Automático via clone | Manual |
| Quando usar | Convenções do projeto | Seus workflows pessoais |

## Estrutura recomendada

```
.claude/
  skills/
    processo/
      tdd.md
      code-review.md
      deploy-checklist.md
    dominio/
      arquitetura.md
      convencoes.md
      regras-negocio.md
  settings.json
```

Subpastas por tipo tornam o catálogo legível. Claude Code encontra skills em qualquer nível dentro de `.claude/skills/`.

## Ciclo de vida de uma skill

```
1. Necessidade identificada
   ↓
2. Skill escrita (rascunho)
   ↓
3. Testada em uso real
   ↓
4. Commitada e documentada no catálogo
   ↓
5. Usada pelo time
   ↓
6. Atualizada quando o processo muda
   ↓
7. Arquivada se o processo é abandonado
```

O passo que mais falha é o 6. Skills são escritas e nunca mais tocadas — mesmo quando o projeto muda completamente.

## Manter skills atualizadas

### Trigger de atualização

Toda vez que o time toma uma decisão que mudaria o comportamento do agente, é um trigger para atualizar a skill:

- Adotou uma nova convenção de nomenclatura → atualizar `convencoes.md`
- Mudou o processo de deploy → atualizar `deploy-checklist.md`
- Adicionou uma regra de negócio crítica → atualizar `regras-negocio.md`
- Abandonou uma prática → remover da skill ou adicionar nota de "não fazer mais"

### Ownership por skill

Defina um owner para cada skill. Sem owner, a skill não será mantida:

```markdown
---
name: deploy-checklist
description: Checklist de deploy para staging
metadata:
  type: process
  owner: @dev-infra-team
  last_reviewed: 2026-03-01
---
```

O `owner` é o responsável por atualizar quando o processo muda.

### Revisão periódica

Inclua skills na revisão de documentação técnica (sprint review, quarterly tech review). Perguntas a fazer:

- Esta skill ainda reflete como o time trabalha?
- Há passos que foram adicionados à prática mas não à skill?
- Há passos na skill que o time parou de fazer?
- A skill tem exemplos que ficaram desatualizados com o código?

## Catálogo de skills

Documente as skills disponíveis no `CLAUDE.md` do projeto:

```markdown
## Skills disponíveis

### Processo
| Skill | Uso |
|-------|-----|
| `/tdd` | Desenvolvimento orientado a testes — red/green/refactor |
| `/code-review` | Checklist de revisão antes de merge |
| `/deploy-checklist` | Verificações antes de deploy para staging |

### Domínio
| Skill | Uso |
|-------|-----|
| `/arquitetura` | Mapa de módulos e responsabilidades |
| `/convencoes` | Nomenclatura, estrutura de arquivos, padrões |
| `/regras-negocio` | Invariantes do domínio que não podem ser violadas |
```

Isso garante que novos devs no time sabem quais skills existem sem precisar explorar `.claude/skills/`.

## Onboarding de novos devs

Inclua as skills no checklist de onboarding:

```markdown
## Setup do Claude Code

1. Clone o repo (as skills em `.claude/skills/` já estão incluídas)
2. Configure `~/.claude/settings.json` com os MCP servers do projeto (ver `docs/setup.md`)
3. Skills disponíveis: `/help` no Claude Code lista todas
4. Para desenvolvimento: sempre invoque `/convencoes` e `/tdd` antes de começar
```

O novo dev não precisa aprender as convenções do zero — o agente as segue automaticamente.

## Code review de skills

Skills passam pelo mesmo processo de review que código:

- PR com mudança na skill → revisão obrigatória
- Checklist de review de skill:
  - O processo descrito ainda está correto?
  - A mudança não contradiz outra skill existente?
  - Há exemplos atualizados?
  - O formato de output está claro?

Uma skill errada é pior que código com bug — porque o bug aparece nos testes, mas a skill errada vai orientar o agente silenciosamente na direção errada.

## Quando aposentar uma skill

Uma skill que descreve um processo abandonado deve ser removida, não apenas marcada como obsoleta. O agente não sabe que algo está "obsoleto" — ele vai seguir a instrução da mesma forma.

Se você quer manter o histórico, use git:

```bash
git rm .claude/skills/deploy-manual.md
git commit -m "chore: remove skill de deploy manual — substituída por CI/CD automático"
```

O histórico fica no git. A skill não fica no repo confundindo o agente.

## Distribuição via plugin

Para skills que você quer compartilhar entre projetos sem copiar arquivos:

```bash
# Criar estrutura de plugin
mkdir -p ~/.claude/plugins/meu-plugin/skills

# Adicionar skills
cp .claude/skills/processo/*.md ~/.claude/plugins/meu-plugin/skills/
```

Plugins são carregados automaticamente em todos os projetos. Útil para skills de processo genéricas (TDD, debugging) que você usa em qualquer projeto.

## Armadilhas

**Skills que nunca são usadas**: se o time não invoca as skills, elas têm valor zero. O problema pode ser descoberta (o catálogo não está visível) ou adoção (o time não desenvolveu o hábito). Inclua no `CLAUDE.md` quando usar cada skill.

**Skills de domínio sem owner**: skills de processo mudam devagar. Skills de domínio mudam com o projeto — sem owner, ficam desatualizadas em semanas.

**Skill conflitante com outra skill**: se `/convencoes.md` diz "use kebab-case para variáveis" e `/arquitetura.md` tem exemplos com camelCase, o agente vai fazer escolhas inconsistentes. Revise conflitos periodicamente.

**Skill que documenta aspiração, não realidade**: "sempre escreva testes para todos os casos de borda" pode ser uma aspiração, não o processo real. Skills que descrevem como o time gostaria de trabalhar criam fricção. Documente como o time realmente trabalha.

## Veja também

- [[03-Dominios/IA/Claude Code/Skills e MCP/01 - Anatomia de uma skill|01 - Anatomia de uma skill]] — estrutura e frontmatter
- [[03-Dominios/IA/Claude Code/Skills e MCP/02 - Skills de processo vs domínio|02 - Skills de processo vs domínio]] — ciclos de vida diferentes
- [[03-Dominios/IA/Claude Code/Skills e MCP/03 - Criar sua primeira skill|03 - Criar sua primeira skill]] — criar antes de distribuir
- [[03-Dominios/IA/Claude Code/Configuração/02 - CLAUDE.md anatomia|02 - CLAUDE.md anatomia]] — onde documentar o catálogo de skills
- [[03-Dominios/IA/Claude Code/Skills e MCP/index|Skills e MCP]] — índice do galho
