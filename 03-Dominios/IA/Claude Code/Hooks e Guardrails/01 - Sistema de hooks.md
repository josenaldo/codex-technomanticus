---
title: "Sistema de hooks — visão geral do lifecycle"
type: concept
publish: true
created: 2026-05-13
updated: 2026-05-13
status: seedling
tags:
  - claude-code
  - hooks
  - lifecycle
  - guardrails
---

# Sistema de hooks — visão geral do lifecycle

> [!abstract] TL;DR
> Hooks são shell scripts que o Claude Code executa em pontos determinísticos do seu ciclo de operação. Existem 4 tipos: PreToolUse (antes de uma tool call), PostToolUse (depois), Notification (quando o agente precisa de atenção), e Stop (quando a sessão termina). Hooks transformam Claude Code de "agente que pede permissão" em "agente com políticas programáticas".

## O que são hooks

Um hook é um shell command configurado em `settings.json` que o Claude Code executa automaticamente em resposta a eventos do seu lifecycle. O agente não decide se executa o hook — o runtime executa sempre que o evento ocorre.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "echo '{\"input\": $INPUT}' | meu-validador.sh"
          }
        ]
      }
    ]
  }
}
```

## Os 4 tipos de hook

### PreToolUse

Executa **antes** de uma tool call. Pode:
- Bloquear a execução (exit code não-zero)
- Modificar o input (via stdout JSON)
- Logar a intenção
- Solicitar aprovação humana

Caso de uso principal: guardrails, validação de comandos perigosos, auditoria.

### PostToolUse

Executa **depois** de uma tool call, independente de sucesso ou falha. Pode:
- Reagir ao resultado (auto-lint, auto-format, notificações)
- Logar o resultado
- Disparar ações secundárias

Caso de uso principal: automação de qualidade (rodar linter depois de Edit), notificações de ação.

### Notification

Executa quando o Claude Code quer chamar atenção do usuário (tipicamente quando está esperando input em modo longo, ou concluiu uma tarefa). Útil para notificações de desktop ou push notifications.

### Stop

Executa quando a sessão termina. Útil para: limpar temporários, logar a sessão completa, criar um resumo do que foi feito.

## Fluxo do lifecycle com hooks

```
Usuário dá instrução
        ↓
Agente decide tool call (ex: Bash("rm -rf dist/"))
        ↓
[PreToolUse hook executa]
    ↓ exit 0: continua
    ↓ exit 1: bloqueia, agente recebe erro
        ↓
Tool executa
        ↓
[PostToolUse hook executa]
        ↓
Agente processa resultado
        ↓ (quando sessão encerra)
[Stop hook executa]
```

## Configuração em settings.json

Hooks ficam na chave `"hooks"` do settings.json, com a chave sendo o tipo de hook e o valor sendo um array de matchers:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [{ "type": "command", "command": "/caminho/para/validador.sh" }]
      },
      {
        "matcher": "Edit",
        "hooks": [{ "type": "command", "command": "/caminho/para/log-edits.sh" }]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit",
        "hooks": [{ "type": "command", "command": "npm run lint --quiet" }]
      }
    ],
    "Stop": [
      {
        "hooks": [{ "type": "command", "command": "/caminho/para/session-summary.sh" }]
      }
    ]
  }
}
```

## Matchers

O campo `"matcher"` filtra quais tool calls ativam o hook:

| Matcher | Ativa para |
|---------|-----------|
| `"Bash"` | Qualquer chamada ao Bash tool |
| `"Edit"` | Qualquer chamada ao Edit tool |
| `"Write"` | Qualquer chamada ao Write tool |
| `""` (vazio) | Todas as tool calls |
| `"Bash(rm*)"` | Bash calls cujo comando começa com `rm` |

## Comunicação hook → agente

O hook pode retornar informações ao agente via stdout em formato JSON:

```json
{
  "decision": "block",
  "reason": "Comando rm -rf em diretório protegido"
}
```

Ou para continuar com modificação:

```json
{
  "decision": "approve",
  "modified_input": "rm -rf dist/ --preserve=important.txt"
}
```

## Onde configurar hooks

Hooks podem ser configurados em:

- **Global** (`~/.claude/settings.json`): aplicam em todos os projetos
- **Projeto** (`.claude/settings.json`): aplicam neste projeto para todos
- **Local** (`.claude/settings.local.json`): aplicam só para você neste projeto (não commitado)

Guardrails de segurança → global. Automações de qualidade específicas do projeto → projeto.

## Veja também

- [[03-Dominios/IA/Claude Code/Hooks e Guardrails/02 - PreToolUse|02 - PreToolUse]] — interceptar antes de executar
- [[03-Dominios/IA/Claude Code/Hooks e Guardrails/03 - PostToolUse|03 - PostToolUse]] — automação pós-ação
- [[03-Dominios/IA/Claude Code/Hooks e Guardrails/05 - Guardrails|05 - Guardrails]] — bloquear comandos destrutivos
- [[03-Dominios/IA/Claude Code/Configuração/04 - settings.json|04 - settings.json]] — estrutura completa do settings.json
- [[03-Dominios/IA/Claude Code/Hooks e Guardrails/index|Hooks e Guardrails]] — índice do galho
