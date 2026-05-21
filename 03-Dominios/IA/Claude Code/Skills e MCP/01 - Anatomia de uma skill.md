---
title: "Anatomia de uma skill — estrutura, frontmatter, tipos"
type: concept
publish: true
created: 2026-05-13
updated: 2026-05-13
status: seedling
tags:
  - claude-code
  - skills
  - anatomia
  - estrutura
---

# Anatomia de uma skill — estrutura, frontmatter, tipos

> [!abstract] TL;DR
> Uma skill é um arquivo Markdown com frontmatter YAML que o Claude Code lê antes de executar uma tarefa. Ela ensina o agente a seguir um processo específico: como fazer TDD neste projeto, como revisar código aqui, como debugar este stack. O frontmatter controla quando a skill é carregada; o corpo é a instrução que o agente segue.

## O que é uma skill

Uma skill não é código — é instrução estruturada. Quando você invoca `/minha-skill`, o Claude Code lê o arquivo Markdown da skill e o incorpora no contexto antes de responder. O agente então segue aquelas instruções no restante da sessão.

A diferença para um prompt solto no chat: a skill é versionada, compartilhável, e invocável pelo nome. É um processo documentado como artefato que o time pode evoluir.

## Estrutura de uma skill

```markdown
---
name: meu-processo
description: Descrição curta do que esta skill faz — usada pelo agente para decidir relevância
metadata:
  type: process
  tags: [testing, tdd, typescript]
---

# Meu Processo

## O que fazer primeiro
...

## Regras inegociáveis
...

## Quando terminar
...
```

### Campos do frontmatter

| Campo | Obrigatório | Descrição |
|-------|-------------|-----------|
| `name` | sim | Identificador da skill. Usado para invocar com `/name`. |
| `description` | sim | Texto curto. O agente usa isso para decidir se a skill é relevante. |
| `metadata.type` | recomendado | `process` ou `domain` — ajuda a organizar o catálogo |
| `metadata.tags` | recomendado | Tags para descoberta e filtragem |

### O corpo

O corpo é texto Markdown livre. O agente lê o corpo como instrução.

Boas práticas:
- Organize em seções com `##` (o agente navega pela estrutura)
- Use listas para passos sequenciais — o agente tende a seguir listas em ordem
- Use **negrito** para destaque de regras críticas
- Use `> [!warning]` para alertas que o agente não deve ignorar
- Inclua exemplos de código quando o comportamento esperado for ambíguo

## Tipos de skill

### Process skills (tipo: process)

Ensinam o agente a seguir um workflow específico. O agente usa a skill como um checklist a ser executado.

Exemplos:
- TDD: red → green → refactor
- Code review: checklist de segurança, performance, legibilidade
- Debugging: reproduzir → isolar → corrigir → testar

A skill de processo responde "como fazer X" — o processo é o conteúdo.

### Domain skills (tipo: domain)

Ensinam o agente sobre o projeto, o domínio, ou o stack. O agente usa como referência enquanto trabalha.

Exemplos:
- Convenções de nomenclatura do projeto
- Arquitetura e módulos principais
- Regras de negócio específicas do domínio
- Restrições técnicas conhecidas

A skill de domínio responde "o que é X neste contexto" — o conhecimento é o conteúdo.

## Onde armazenar skills

**Projeto-específico**: `.claude/skills/` — versionado junto ao código, compartilhado com o time.

**Pessoal global**: `~/.claude/skills/` — suas skills pessoais, aplicam em qualquer projeto.

**Plugin**: estrutura de plugin com múltiplas skills num pacote — para distribuição externa.

## Como invocar uma skill

```
/nome-da-skill
```

O prefixo `/` identifica o nome da skill. O Claude Code procura primeiro em `.claude/skills/`, depois em `~/.claude/skills/`, depois em plugins instalados.

Para ver skills disponíveis:
```
/help
```

## Como o agente usa a skill

Ao invocar `/minha-skill`, o Claude Code:

1. Encontra o arquivo da skill pelo `name` do frontmatter
2. Lê o conteúdo completo do arquivo
3. Incorpora o conteúdo no contexto da sessão
4. Passa a seguir as instruções da skill ao responder

O agente não "executa" a skill — ele a lê como instrução e a aplica. Se a skill diz "sempre escreva o teste antes da implementação", o agente vai tentar seguir isso ao longo da sessão.

## Armadilhas

**Skills muito longas**: o agente lê a skill inteira, consumindo tokens de contexto. Skills acima de 500 linhas começam a competir com o contexto do codebase. Prefira skills focadas e pequenas.

**Instruções ambíguas**: "escreva código limpo" não instrui — o agente não sabe o que você considera limpo. "Prefira composição de funções puras a classes com estado" instrui.

**Misturar processo e domínio**: uma skill que ensina TDD e também documenta a arquitetura do projeto é difícil de manter e de invocar. Separe por tipo.

**`name` diferente do nome do arquivo**: convenção é manter `name:` idêntico ao nome do arquivo (sem espaços, kebab-case). Divergência cria confusão.

## Veja também

- [[03-Dominios/IA/Claude Code/Skills e MCP/02 - Skills de processo vs domínio|02 - Skills de processo vs domínio]] — quando usar cada tipo
- [[03-Dominios/IA/Claude Code/Skills e MCP/03 - Criar sua primeira skill|03 - Criar sua primeira skill]] — walkthrough prático
- [[03-Dominios/IA/Claude Code/Skills e MCP/08 - Skills em time|08 - Skills em time]] — versionar e compartilhar skills
- [[03-Dominios/IA/Claude Code/Skills e MCP/index|Skills e MCP]] — índice do galho
