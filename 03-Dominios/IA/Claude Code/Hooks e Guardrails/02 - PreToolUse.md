---
title: "PreToolUse — interceptar e validar antes de executar"
type: concept
publish: true
created: 2026-05-13
updated: 2026-05-13
status: seedling
tags:
  - claude-code
  - hooks
  - pretooluse
  - guardrails
  - validacao
---

# PreToolUse — interceptar e validar antes de executar

> [!abstract] TL;DR
> PreToolUse é o hook que executa antes de qualquer tool call. É o ponto de controle principal do Claude Code: intercepta, valida, e pode bloquear. Exit code 0 = aprovado, exit code não-zero = bloqueado. O agente recebe o resultado do hook e decide como proceder. É onde guardrails, auditoria e aprovação humana são implementados.

## Como funciona

Quando o agente decide executar uma tool call (ex: `Bash("git push --force origin main")`), o runtime:

1. Serializa o input como JSON e passa para o hook via stdin ou variável de ambiente
2. Executa o hook command
3. Se exit code = 0: executa a tool
4. Se exit code ≠ 0: bloqueia a execução e retorna o stderr do hook ao agente como mensagem de erro

O agente recebe o bloqueio como feedback e pode tentar uma abordagem alternativa.

## Estrutura do input

O hook recebe via stdin um JSON com o input da tool call:

```json
{
  "tool_name": "Bash",
  "tool_input": {
    "command": "git push --force origin main"
  }
}
```

Para Edit:
```json
{
  "tool_name": "Edit",
  "tool_input": {
    "file_path": "/projeto/src/config/database.ts",
    "old_string": "password: 'prod_secret'",
    "new_string": "password: process.env.DB_PASSWORD"
  }
}
```

## Bloqueio simples — exit 1

O hook mais simples: bloquear um padrão e retornar mensagem de erro.

```bash
#!/bin/bash
# hooks/block-force-push.sh

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // ""')

if echo "$COMMAND" | grep -q "push --force\|push -f"; then
  echo "BLOQUEADO: force push não permitido. Use --force-with-lease ou abra PR." >&2
  exit 1
fi

exit 0
```

Configuração:
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [{ "type": "command", "command": "~/.claude/hooks/block-force-push.sh" }]
      }
    ]
  }
}
```

## Bloqueio por padrão de arquivo

Proteger arquivos sensíveis de edição:

```bash
#!/bin/bash
# hooks/protect-sensitive-files.sh

INPUT=$(cat)
FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path // ""')

PROTECTED_PATTERNS=(
  ".*\.env$"
  ".*credentials.*"
  ".*\.pem$"
  ".*secrets.*"
)

for pattern in "${PROTECTED_PATTERNS[@]}"; do
  if echo "$FILE" | grep -qE "$pattern"; then
    echo "BLOQUEADO: $FILE é um arquivo protegido. Edite manualmente." >&2
    exit 1
  fi
done

exit 0
```

## Logging de auditoria

Hook que não bloqueia, só registra:

```bash
#!/bin/bash
# hooks/audit-log.sh

INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.tool_name')
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // .tool_input.file_path // ""')
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
SESSION_ID="${CLAUDE_SESSION_ID:-unknown}"

echo "$TIMESTAMP | $SESSION_ID | $TOOL | $COMMAND" >> ~/.claude/audit.log

exit 0
```

O arquivo `~/.claude/audit.log` acumula todas as tool calls da sessão — útil para debugging e compliance.

## Aprovação humana interativa

Para comandos de alto risco, pedir aprovação antes de executar:

```bash
#!/bin/bash
# hooks/require-approval.sh

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // ""')

HIGH_RISK_PATTERNS=(
  "rm -rf"
  "DROP TABLE"
  "DELETE FROM"
  "git push"
  "kubectl delete"
)

for pattern in "${HIGH_RISK_PATTERNS[@]}"; do
  if echo "$COMMAND" | grep -qi "$pattern"; then
    echo "APROVAÇÃO NECESSÁRIA: $COMMAND"
    echo "Confirma? (s/N): " >&2
    read -r response < /dev/tty
    if [[ ! "$response" =~ ^[Ss]$ ]]; then
      echo "Bloqueado pelo usuário." >&2
      exit 1
    fi
    break
  fi
done

exit 0
```

> [!warning] Aprovação interativa só funciona em sessão interativa
> Em modo headless (CI/CD, `--print`), não há terminal para leitura. Para headless, use bloqueio direto em vez de aprovação interativa.

## Delegação a outro LLM

Para validações complexas que precisam de raciocínio:

```bash
#!/bin/bash
# hooks/llm-validator.sh

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // ""')

# Delegar a decisão a outro LLM
DECISION=$(echo "$COMMAND" | claude --print \
  "Este comando bash é seguro para executar num servidor de produção?
   Responda apenas: SAFE ou UNSAFE: MOTIVO" \
  --max-tokens 50)

if echo "$DECISION" | grep -q "^UNSAFE"; then
  MOTIVO=$(echo "$DECISION" | sed 's/^UNSAFE: //')
  echo "LLM bloqueou: $MOTIVO" >&2
  exit 1
fi

exit 0
```

Ver [[03-Dominios/IA/Claude Code/Hooks e Guardrails/06 - Delegar permissão|06 - Delegar permissão]] para o padrão completo.

## Modificação de input

O hook pode modificar o input antes de executar, retornando JSON via stdout:

```bash
#!/bin/bash
# hooks/sanitize-rm.sh

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // ""')

# Adicionar --interactive em todo rm
if echo "$COMMAND" | grep -q "^rm "; then
  SAFE_COMMAND=$(echo "$COMMAND" | sed 's/^rm /rm -i /')
  echo '{"decision": "approve", "modified_input": {"command": "'"$SAFE_COMMAND"'"}}'
  exit 0
fi

exit 0
```

## Múltiplos hooks em sequência

Quando há múltiplos hooks configurados para o mesmo matcher, todos executam em sequência. Se qualquer um retornar exit ≠ 0, a tool call é bloqueada.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": "~/.claude/hooks/audit-log.sh" },
          { "type": "command", "command": "~/.claude/hooks/block-force-push.sh" },
          { "type": "command", "command": "~/.claude/hooks/protect-sensitive-files.sh" }
        ]
      }
    ]
  }
}
```

## Veja também

- [[03-Dominios/IA/Claude Code/Hooks e Guardrails/01 - Sistema de hooks|01 - Sistema de hooks]] — lifecycle e configuração
- [[03-Dominios/IA/Claude Code/Hooks e Guardrails/05 - Guardrails|05 - Guardrails]] — conjunto completo de guardrails recomendados
- [[03-Dominios/IA/Claude Code/Hooks e Guardrails/06 - Delegar permissão|06 - Delegar permissão]] — meta-agente para validação com LLM
- [[03-Dominios/IA/Claude Code/Hooks e Guardrails/08 - Testando hooks|08 - Testando hooks]] — como testar e debugar hooks
- [[03-Dominios/IA/Claude Code/Hooks e Guardrails/index|Hooks e Guardrails]] — índice do galho
