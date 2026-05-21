---
title: "Stop hook — notificação, logging, cleanup"
type: concept
publish: true
created: 2026-05-13
updated: 2026-05-13
status: seedling
tags:
  - claude-code
  - hooks
  - stop-hook
  - notificacao
  - logging
---

# Stop hook — notificação, logging, cleanup

> [!abstract] TL;DR
> O Stop hook executa quando a sessão do Claude Code termina — seja por conclusão natural, por timeout, ou por interrupção do usuário. É o hook de encerramento. Casos de uso: notificar que o trabalho foi concluído, criar um sumário da sessão, fazer cleanup de arquivos temporários, e registrar métricas de uso.

## Quando o Stop hook executa

O Stop hook dispara em 3 situações:

1. **Conclusão natural**: o agente terminou a tarefa e está aguardando o próximo input
2. **Timeout**: a sessão atingiu o limite de tempo configurado
3. **Interrupção**: o usuário pressionou Ctrl+C ou fechou o terminal

## Estrutura do input

O Stop hook não recebe input de tool call (não houve tool call). Recebe um JSON de sessão:

```json
{
  "session_id": "abc123",
  "stop_reason": "end_turn",
  "total_turns": 47,
  "total_tokens": 125000
}
```

`stop_reason` pode ser: `"end_turn"`, `"max_turns"`, `"stop_sequence"`, ou `"interrupt"`.

## Notificação de desktop

O caso de uso mais simples: avisar que o Claude terminou enquanto você estava em outra janela.

```bash
#!/bin/bash
# hooks/notify-stop.sh

INPUT=$(cat)
REASON=$(echo "$INPUT" | jq -r '.stop_reason // "unknown"')
TURNS=$(echo "$INPUT" | jq -r '.total_turns // 0')

MESSAGE="Claude Code encerrou ($TURNS turns, $REASON)"

# Linux (libnotify)
notify-send "Claude Code" "$MESSAGE" --urgency=normal 2>/dev/null

# macOS
osascript -e "display notification \"$MESSAGE\" with title \"Claude Code\"" 2>/dev/null

# Som de alerta (macOS)
afplay /System/Library/Sounds/Glass.aiff 2>/dev/null

exit 0
```

## Sumário de sessão

Criar um arquivo de log com o resumo do que foi feito:

```bash
#!/bin/bash
# hooks/session-summary.sh

INPUT=$(cat)
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // "unknown"')
TURNS=$(echo "$INPUT" | jq -r '.total_turns // 0')
TOKENS=$(echo "$INPUT" | jq -r '.total_tokens // 0')
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Arquivos modificados nesta sessão (via git diff)
MODIFIED_FILES=$(git diff --name-only HEAD 2>/dev/null | head -20)

{
  echo "=== Sessão Claude Code: $TIMESTAMP ==="
  echo "Session ID: $SESSION_ID"
  echo "Turns: $TURNS | Tokens: $TOKENS"
  echo ""
  echo "Arquivos modificados:"
  echo "$MODIFIED_FILES"
  echo ""
} >> ~/.claude/sessions.log

exit 0
```

## Cleanup de arquivos temporários

Se o agente criou arquivos temporários de debugging, limpá-los ao encerrar:

```bash
#!/bin/bash
# hooks/cleanup-temp.sh

# Remover arquivos de debug temporários deixados pelo agente
find . -name "*.debug.log" -newer ~/.claude/session-start 2>/dev/null | xargs rm -f 2>/dev/null
find . -name "debug-*.json" -newer ~/.claude/session-start 2>/dev/null | xargs rm -f 2>/dev/null

exit 0
```

## Métricas de uso

Para times que querem rastrear consumo por projeto/desenvolvedor:

```bash
#!/bin/bash
# hooks/track-usage.sh

INPUT=$(cat)
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id')
TOKENS=$(echo "$INPUT" | jq -r '.total_tokens // 0')
TURNS=$(echo "$INPUT" | jq -r '.total_turns // 0')
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
PROJECT=$(basename "$(pwd)")
USER=$(whoami)

# Append a CSV de métricas
echo "$TIMESTAMP,$USER,$PROJECT,$SESSION_ID,$TOKENS,$TURNS" >> ~/.claude/usage-metrics.csv

exit 0
```

## Git commit automático ao encerrar

Para workflows que querem commitar automaticamente o trabalho feito:

```bash
#!/bin/bash
# hooks/auto-commit-on-stop.sh

INPUT=$(cat)
REASON=$(echo "$INPUT" | jq -r '.stop_reason')

# Só commita em conclusão natural, não em interrupt
if [[ "$REASON" != "end_turn" ]]; then exit 0; fi

# Verifica se há mudanças
if git diff --quiet && git diff --staged --quiet; then
  exit 0
fi

# Commita com mensagem automática
TIMESTAMP=$(date +"%Y-%m-%d %H:%M")
git add -A
git commit -m "chore: auto-commit Claude Code session $TIMESTAMP"

exit 0
```

> [!warning] Auto-commit tem riscos
> Esse hook commita automaticamente qualquer coisa que o agente modificou — incluindo arquivos de debug, alterações incompletas, e código com testes falhando. Use só se tiver certeza de que quer esse comportamento.

## Stop hook em modo headless

Em pipelines CI/CD com `claude --print`, o Stop hook é especialmente útil para:
- Reportar se a tarefa foi concluída com sucesso
- Criar artefatos de saída (JSON de resultados, relatório)
- Notificar sistemas externos (webhook, Slack, email)

```bash
#!/bin/bash
# hooks/ci-report.sh

INPUT=$(cat)
REASON=$(echo "$INPUT" | jq -r '.stop_reason')
TOKENS=$(echo "$INPUT" | jq -r '.total_tokens // 0')

# Criar relatório para CI
cat > /tmp/claude-report.json <<EOF
{
  "completed": $([ "$REASON" = "end_turn" ] && echo "true" || echo "false"),
  "stop_reason": "$REASON",
  "tokens_used": $TOKENS
}
EOF

exit 0
```

## Veja também

- [[03-Dominios/IA/Claude Code/Hooks e Guardrails/01 - Sistema de hooks|01 - Sistema de hooks]] — lifecycle completo e tipos de hook
- [[03-Dominios/IA/Claude Code/Hooks e Guardrails/03 - PostToolUse|03 - PostToolUse]] — logging durante a sessão
- [[03-Dominios/IA/Claude Code/Time e Automação/index|Time e Automação]] — hooks em pipelines de time
- [[03-Dominios/IA/Claude Code/Hooks e Guardrails/08 - Testando hooks|08 - Testando hooks]] — como testar hooks de Stop
- [[03-Dominios/IA/Claude Code/Hooks e Guardrails/index|Hooks e Guardrails]] — índice do galho
