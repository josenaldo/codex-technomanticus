---
title: "PostToolUse — automação pós-ação"
type: concept
publish: true
created: 2026-05-13
updated: 2026-05-13
status: seedling
tags:
  - claude-code
  - hooks
  - posttooluse
  - automacao
  - qualidade
---

# PostToolUse — automação pós-ação

> [!abstract] TL;DR
> PostToolUse executa depois de qualquer tool call completar. Diferente do PreToolUse (que decide se executa), o PostToolUse reage ao resultado. Usos principais: auto-lint depois de edições de arquivo, notificações de ações, logging de resultados, e disparar ações secundárias dependentes. O hook não pode desfazer a tool call — só reagir a ela.

## Como funciona

Após cada tool call completar (com sucesso ou falha), o runtime:

1. Serializa o input e output da tool como JSON
2. Executa o hook command com esse JSON via stdin
3. O output do hook é logado (não volta para o agente por padrão)
4. A sessão continua independente do exit code do hook

> [!info] PostToolUse não bloqueia
> Diferente do PreToolUse, um exit code não-zero no PostToolUse não bloqueia a continuação da sessão. É um hook de reação, não de controle.

## Estrutura do input

O hook recebe via stdin o JSON da tool call completa:

```json
{
  "tool_name": "Edit",
  "tool_input": {
    "file_path": "/projeto/src/services/orders.ts",
    "old_string": "...",
    "new_string": "..."
  },
  "tool_output": {
    "success": true,
    "message": "File edited successfully"
  }
}
```

## Auto-lint depois de edições

O caso de uso mais comum: rodar o linter automaticamente depois que o agente edita um arquivo TypeScript/JavaScript.

```bash
#!/bin/bash
# hooks/auto-lint.sh

INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.tool_name')
FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path // ""')
SUCCESS=$(echo "$INPUT" | jq -r '.tool_output.success // false')

# Só para edições bem-sucedidas de arquivos TS/JS
if [[ "$TOOL" != "Edit" && "$TOOL" != "Write" ]]; then exit 0; fi
if [[ "$SUCCESS" != "true" ]]; then exit 0; fi
if [[ ! "$FILE" =~ \.(ts|tsx|js|jsx)$ ]]; then exit 0; fi

# Rodar linter no arquivo modificado
npx eslint "$FILE" --fix --quiet 2>/dev/null

exit 0
```

Configuração:
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit",
        "hooks": [{ "type": "command", "command": "~/.claude/hooks/auto-lint.sh" }]
      },
      {
        "matcher": "Write",
        "hooks": [{ "type": "command", "command": "~/.claude/hooks/auto-lint.sh" }]
      }
    ]
  }
}
```

## Auto-format depois de edições

Similar ao lint, rodar Prettier automaticamente:

```bash
#!/bin/bash
# hooks/auto-format.sh

INPUT=$(cat)
FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path // ""')

FORMATTABLE_EXTENSIONS=("ts" "tsx" "js" "jsx" "json" "css" "md")
EXTENSION="${FILE##*.}"

for ext in "${FORMATTABLE_EXTENSIONS[@]}"; do
  if [[ "$EXTENSION" == "$ext" ]]; then
    npx prettier --write "$FILE" --log-level silent 2>/dev/null
    break
  fi
done

exit 0
```

## Logging de ações do agente

Registrar todas as edições de arquivo para auditoria:

```bash
#!/bin/bash
# hooks/log-file-changes.sh

INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.tool_name')
FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path // ""')
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
SESSION="${CLAUDE_SESSION_ID:-unknown}"

if [[ "$TOOL" =~ ^(Edit|Write|Read)$ && -n "$FILE" ]]; then
  echo "$TIMESTAMP | $SESSION | $TOOL | $FILE" >> ~/.claude/file-changes.log
fi

exit 0
```

## Notificação de conclusão de tarefa longa

Para tarefas longas (como npm test ou build), notificar quando concluírem:

```bash
#!/bin/bash
# hooks/notify-on-bash-complete.sh

INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.tool_name')
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // ""')
SUCCESS=$(echo "$INPUT" | jq -r '.tool_output.success // false')

if [[ "$TOOL" != "Bash" ]]; then exit 0; fi

# Notificar para comandos longos
LONG_COMMANDS=("npm test" "npm run build" "npm run lint" "pytest" "cargo build")

for cmd in "${LONG_COMMANDS[@]}"; do
  if echo "$COMMAND" | grep -q "^$cmd"; then
    STATUS="✅"
    [[ "$SUCCESS" != "true" ]] && STATUS="❌"
    
    # notify-send no Linux / osascript no Mac
    notify-send "Claude Code" "$STATUS $COMMAND concluído" 2>/dev/null \
      || osascript -e "display notification \"$STATUS $COMMAND concluído\" with title \"Claude Code\"" 2>/dev/null
    break
  fi
done

exit 0
```

## Disparar testes automaticamente

Após editar um arquivo de implementação, rodar os testes relacionados:

```bash
#!/bin/bash
# hooks/auto-run-tests.sh

INPUT=$(cat)
FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path // ""')

if [[ ! "$FILE" =~ src/.+\.(ts|js)$ ]]; then exit 0; fi

# Derivar o arquivo de teste do arquivo de implementação
TEST_FILE=$(echo "$FILE" | sed 's|src/|tests/|' | sed 's|\.\(ts\|js\)$|.test.\1|')

if [[ -f "$TEST_FILE" ]]; then
  npx jest "$TEST_FILE" --no-coverage --silent 2>&1 | tail -5
fi

exit 0
```

## PostToolUse para Bash — reagir a saída de comandos

```bash
#!/bin/bash
# hooks/log-failing-commands.sh

INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.tool_name')
SUCCESS=$(echo "$INPUT" | jq -r '.tool_output.success // true')
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // ""')
OUTPUT=$(echo "$INPUT" | jq -r '.tool_output.output // ""')

if [[ "$TOOL" != "Bash" || "$SUCCESS" == "true" ]]; then exit 0; fi

# Logar comandos que falharam com seu output
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
echo "=== $TIMESTAMP ===" >> ~/.claude/failures.log
echo "COMMAND: $COMMAND" >> ~/.claude/failures.log
echo "OUTPUT: $OUTPUT" >> ~/.claude/failures.log
echo "" >> ~/.claude/failures.log

exit 0
```

## Armadilhas

**Hook pesado em PostToolUse**: o hook executa a cada tool call. Um hook que demora 2 segundos em cada Edit vai tornar a sessão muito mais lenta. Mantenha PostToolUse leve.

**Tentar desfazer a ação**: PostToolUse não pode desfazer — se o agente editou um arquivo, o arquivo já foi editado. Use PreToolUse para prevenir, PostToolUse para reagir.

**Depender do exit code para controle**: PostToolUse não bloqueia baseado em exit code. Se você precisa de controle, use PreToolUse.

## Veja também

- [[03-Dominios/IA/Claude Code/Hooks e Guardrails/01 - Sistema de hooks|01 - Sistema de hooks]] — lifecycle completo
- [[03-Dominios/IA/Claude Code/Hooks e Guardrails/02 - PreToolUse|02 - PreToolUse]] — controle antes de executar
- [[03-Dominios/IA/Claude Code/Hooks e Guardrails/04 - Stop hook|04 - Stop hook]] — ações no encerramento da sessão
- [[03-Dominios/IA/Claude Code/Hooks e Guardrails/08 - Testando hooks|08 - Testando hooks]] — debugging de hooks
- [[03-Dominios/IA/Claude Code/Hooks e Guardrails/index|Hooks e Guardrails]] — índice do galho
