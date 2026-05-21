---
title: "Hierarquia de configuração — global, projeto, user"
type: concept
publish: true
created: 2026-05-13
updated: 2026-05-13
status: seedling
tags:
  - claude-code
  - configuracao
  - claude-md
  - settings
---

# Hierarquia de configuração — global, projeto, user

> [!abstract] TL;DR
> Claude Code lê configuração em camadas: global (`~/.claude/`) → projeto (`.claude/`) → local (`.claude/settings.local.json`). Camadas mais específicas sobrescrevem as mais gerais. CLAUDE.md é lido em todas as camadas que existirem — o conteúdo é concatenado. Entender a hierarquia é pré-requisito para configurar intencionalmente.

## O que é

Claude Code agrega configuração de múltiplos locais para construir o contexto de cada sessão. A ordem de precedência é:

```
[sistema] → [global] → [projeto] → [local]
          ↑ menor                  ↑ maior
       prioridade               prioridade
```

Configurações mais específicas sobrescrevem as genéricas. O que está no `.claude/` do projeto sobrescreve o que está em `~/.claude/`.

## As camadas

### Camada 1: Sistema (built-in)

O system prompt padrão do Claude Code — comportamento base, quais tools usar, como pedir confirmação, como estruturar respostas. Você não edita isso diretamente.

### Camada 2: Global (`~/.claude/`)

Configuração que aplica a **todos os projetos** do usuário.

| Arquivo | Propósito |
|---------|-----------|
| `~/.claude/CLAUDE.md` | Preferências pessoais: estilo de resposta, idioma, convenções de código pessoais |
| `~/.claude/settings.json` | Permissões e comportamentos padrão para todas as sessões |

**Quando usar:** preferências que você quer em todos os projetos. Exemplo: "responda em português", "nunca adicione Co-Authored-By em commits".

### Camada 3: Projeto (`.claude/`)

Configuração específica do projeto — fica no repositório, é compartilhada com o time.

| Arquivo | Propósito |
|---------|-----------|
| `.claude/CLAUDE.md` | Contexto do projeto: stack, convenções, comandos, o que evitar |
| `.claude/settings.json` | Permissões do projeto: quais Bash commands são permitidos sem confirmação |
| `.claude/commands/` | Slash commands customizados do projeto |

**Quando usar:** tudo que o agente precisa saber sobre o projeto específico e que todo o time deve seguir.

### Camada 4: Local (`.claude/settings.local.json`)

Sobrescritas pessoais que **não vão para o git**. Ideal para sobrescrever temporariamente permissões do projeto sem afetar o time.

```json
// .claude/settings.local.json (adicione ao .gitignore)
{
  "permissions": {
    "allow": [
      "Bash(npm run dev)"
    ]
  }
}
```

## Como CLAUDE.md é lido

A diferença crucial: **settings.json** usa sobrescrita (camada mais específica vence). **CLAUDE.md** usa concatenação — todos os CLAUDE.md encontrados são lidos e combinados no início de cada sessão.

```
Sessão em ~/repos/meu-projeto:

1. Lê ~/.claude/CLAUDE.md   → "Responda em português. Nunca adicione Co-Authored-By."
2. Lê .claude/CLAUDE.md     → "Stack: Node 20 + TypeScript. Use logger em src/utils/logger.ts."

Contexto inicial do agente = ambos, concatenados.
```

Isso significa que suas preferências pessoais (global) se combinam com o contexto do projeto — sem conflito, sem sobrescrita.

## Precedência em settings.json

Para `settings.json`, a camada mais específica sobrescreve:

```json
// ~/.claude/settings.json
{
  "permissions": {
    "allow": ["Bash(git status)", "Bash(git log)"]
  }
}

// .claude/settings.json
{
  "permissions": {
    "allow": ["Bash(npm test)", "Bash(npm run lint)"],
    "deny": ["Bash(rm -rf *)"]
  }
}
```

O agente terá: `git status`, `git log`, `npm test`, `npm run lint` permitidos, e `rm -rf *` bloqueado.

## Diagrama de resolução

```
Sessão inicia
     ↓
Lê ~/.claude/CLAUDE.md       (se existir)
     ↓
Lê .claude/CLAUDE.md         (se existir)
     ↓
Combina settings:
  ~/.claude/settings.json    (base)
  .claude/settings.json      (sobrescreve)
  .claude/settings.local.json (sobrescreve)
     ↓
System prompt + CLAUDE.mds combinados + settings resolvidos
= contexto inicial da sessão
```

## O que vai em cada camada

| O que | Onde colocar |
|-------|-------------|
| Idioma de resposta, estilo pessoal | `~/.claude/CLAUDE.md` |
| Regras de commit pessoais | `~/.claude/CLAUDE.md` |
| Stack e convenções do projeto | `.claude/CLAUDE.md` |
| Arquivos-chave do projeto | `.claude/CLAUDE.md` |
| Comandos de desenvolvimento do projeto | `.claude/settings.json` |
| Guardrails do projeto | `.claude/settings.json` |
| Sobrescrita temporária pessoal | `.claude/settings.local.json` |
| Slash commands do projeto | `.claude/commands/` |

## Armadilhas

**Confundir onde colocar o CLAUDE.md**: `~/.claude/CLAUDE.md` é para você. `.claude/CLAUDE.md` é para o projeto. Se colocar convenções do projeto no global, elas se aplicam a todos os seus outros projetos também.

**settings.local.json no git**: adicione `.claude/settings.local.json` ao `.gitignore`. É sobrescrita pessoal — não deve ser compartilhada.

**Esperar que settings.json concatene como CLAUDE.md**: não concatena. A camada mais específica sobrescreve. Se o projeto define `allow: ["npm test"]` e o global define `allow: ["git status"]`, o resultado é `allow: ["npm test"]` — git status não está mais na lista.

## Veja também

- [[03-Dominios/IA/Claude Code/Configuração/02 - CLAUDE.md anatomia|02 - CLAUDE.md anatomia]]
- [[03-Dominios/IA/Claude Code/Configuração/04 - settings.json|04 - settings.json]]
- [[03-Dominios/IA/Claude Code/Configuração/07 - Pasta .claude|07 - A pasta .claude]]
- [[03-Dominios/IA/Claude Code/Configuração/index|Configuração]] — índice do galho

## Referências

- [Claude Code — Configuration](https://docs.anthropic.com/pt/docs/claude-code/settings)
