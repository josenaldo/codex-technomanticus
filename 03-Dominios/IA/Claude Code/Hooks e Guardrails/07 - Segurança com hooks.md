---
title: "Hooks para segurança — commits, push force, rm -rf"
type: concept
publish: true
created: 2026-05-13
updated: 2026-05-13
status: seedling
tags:
  - claude-code
  - hooks
  - seguranca
  - git
  - guardrails
---

# Hooks para segurança — commits, push force, rm -rf

> [!abstract] TL;DR
> Segurança com hooks vai além de guardrails individuais: é uma estratégia em camadas que cobre o fluxo de trabalho inteiro — desde bloquear comandos destrutivos até proteger o histórico git, controlar o que pode ser commitado, e detectar commits com credenciais. A diferença entre guardrails (bloquear ações) e segurança (política sistêmica para o fluxo completo).

## A diferença entre guardrail e segurança

Um guardrail bloqueia um comando. Uma estratégia de segurança com hooks cobre:

1. **O que pode ser executado** (PreToolUse para Bash)
2. **O que pode ser editado** (PreToolUse para Edit/Write)
3. **O que pode ser commitado** (PostToolUse no Bash — interceptar git add/commit)
4. **O que pode ser publicado** (PreToolUse — bloquear git push em condições)
5. **Detecção de vazamentos** (verificar credenciais antes de commit)

## Proteção de arquivos sensíveis

A primeira linha: impedir edição de arquivos que nunca devem ser tocados pelo agente.

```bash
#!/bin/bash
# ~/.claude/hooks/protect-files.sh

INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.tool_name')
FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path // ""')

if [[ "$TOOL" != "Edit" && "$TOOL" != "Write" && "$TOOL" != "Read" ]]; then exit 0; fi

BLOCKED_PATTERNS=(
  ".*\.env$"
  ".*\.env\."
  ".*\.pem$"
  ".*\.key$"
  ".*\.pfx$"
  ".*credentials.*"
  ".*secret.*"
  ".*/\.ssh/.*"
  ".*id_rsa.*"
  ".*id_ed25519.*"
)

for pattern in "${BLOCKED_PATTERNS[@]}"; do
  if echo "$FILE" | grep -qiE "$pattern"; then
    echo "SEGURANÇA: $FILE é um arquivo sensível. Acesso bloqueado." >&2
    exit 1
  fi
done

exit 0
```

> [!info] Bloquear Read também
> Além de Edit/Write, considere bloquear Read em arquivos sensíveis. Um agente que lê suas chaves privadas pode inadvertidamente incluí-las em output, logs, ou contexto de uma chamada API.

## Detecção de credenciais antes de commit

PostToolUse no Bash: interceptar git add/commit e verificar se há credenciais.

```bash
#!/bin/bash
# hooks/detect-credentials-on-commit.sh

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // ""')

# Só age depois de git add ou git commit
if ! echo "$COMMAND" | grep -qE "^git (add|commit)"; then exit 0; fi

# Padrões comuns de credenciais em staged files
STAGED_CONTENT=$(git diff --staged 2>/dev/null)

PATTERNS=(
  "AKIA[0-9A-Z]{16}"          # AWS Access Key ID
  "sk-[a-zA-Z0-9]{48}"        # OpenAI API key
  "ghp_[a-zA-Z0-9]{36}"       # GitHub PAT
  "password\s*=\s*['\"][^'\"]+['\"]"  # password = "valor"
  "secret\s*=\s*['\"][^'\"]+['\"]"    # secret = "valor"
  "api_key\s*=\s*['\"][^'\"]+['\"]"   # api_key = "valor"
)

for pattern in "${PATTERNS[@]}"; do
  if echo "$STAGED_CONTENT" | grep -qE "$pattern"; then
    echo "SEGURANÇA: possível credencial detectada no staged content." >&2
    echo "Pattern: $pattern" >&2
    echo "Revise com: git diff --staged" >&2
    exit 0  # Não bloqueia — avisa. Mude para exit 1 para bloquear.
  fi
done

exit 0
```

> [!warning] PostToolUse detecta, mas não previne
> Como PostToolUse não bloqueia, use esse hook como detector. Para prevenir, use um PreToolUse hook que intercepta `git commit` antes de executar.

## Proteção do histórico git

Bloquear operações que reescrevem histórico e podem causar perda de trabalho:

```bash
#!/bin/bash
# ~/.claude/hooks/protect-git-history.sh

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // ""')

echo "$COMMAND" | grep -q "^git " || exit 0

# force push em qualquer forma
if echo "$COMMAND" | grep -qE "push.*(--force\b|-f\b)"; then
  echo "SEGURANÇA: force push bloqueado. Isso pode apagar commits de outros." >&2
  echo "Use --force-with-lease para verificar que não houve push externo." >&2
  exit 1
fi

# rebase em branches compartilhadas
BRANCH=$(git branch --show-current 2>/dev/null)
if echo "$COMMAND" | grep -qE "^git rebase" && [[ "$BRANCH" =~ ^(main|master|develop)$ ]]; then
  echo "SEGURANÇA: git rebase em $BRANCH bloqueado. Rebase em branches compartilhadas é perigoso." >&2
  exit 1
fi

# reset --hard (descarta trabalho não commitado permanentemente)
if echo "$COMMAND" | grep -qE "reset\s+--hard"; then
  echo "SEGURANÇA: git reset --hard bloqueado. Use git stash para preservar trabalho." >&2
  exit 1
fi

# amend de commits já publicados
if echo "$COMMAND" | grep -qE "commit.*--amend"; then
  REMOTE_TRACKING=$(git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null)
  if [[ -n "$REMOTE_TRACKING" ]]; then
    LOCAL=$(git rev-parse HEAD 2>/dev/null)
    REMOTE=$(git rev-parse "$REMOTE_TRACKING" 2>/dev/null)
    if [[ "$LOCAL" == "$REMOTE" || $(git merge-base HEAD "$REMOTE_TRACKING" 2>/dev/null) == "$LOCAL" ]]; then
      echo "SEGURANÇA: --amend em commit já publicado bloqueado." >&2
      exit 1
    fi
  fi
fi

exit 0
```

## Controle de branches protegidas

Impedir commits diretos em branches protegidas:

```bash
#!/bin/bash
# hooks/protect-branches.sh

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // ""')

# Só age em git commit
echo "$COMMAND" | grep -qE "^git commit" || exit 0

BRANCH=$(git branch --show-current 2>/dev/null)
PROTECTED_BRANCHES=("main" "master" "develop" "release" "production")

for protected in "${PROTECTED_BRANCHES[@]}"; do
  if [[ "$BRANCH" == "$protected" ]]; then
    echo "SEGURANÇA: commit direto em $BRANCH bloqueado." >&2
    echo "Crie uma feature branch: git checkout -b feat/sua-tarefa" >&2
    exit 1
  fi
done

exit 0
```

## Auditoria completa de segurança

Para projetos que precisam de auditoria formal, logar todas as tool calls sensíveis:

```bash
#!/bin/bash
# hooks/security-audit.sh

INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.tool_name')
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // ""')
FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path // ""')
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
USER=$(whoami)
PROJECT=$(basename "$(pwd)")

# Logar apenas ações com potencial de impacto
IS_SENSITIVE=false

case "$TOOL" in
  Bash)
    echo "$COMMAND" | grep -qiE "(git push|git commit|rm |mv |npm publish|deploy|kubectl)" \
      && IS_SENSITIVE=true
    ;;
  Edit|Write)
    echo "$FILE" | grep -qiE "\.(env|json|yaml|yml|toml|sh|config)" \
      && IS_SENSITIVE=true
    ;;
esac

if [[ "$IS_SENSITIVE" == "true" ]]; then
  echo "$TIMESTAMP | $USER | $PROJECT | $TOOL | ${COMMAND:-$FILE}" >> ~/.claude/security-audit.log
fi

exit 0
```

## Estratégia de defesa em profundidade

Não confie em uma única camada. Combine:

| Camada | Hook | O que protege |
|--------|------|---------------|
| Arquivos | PreToolUse Edit/Write | Credenciais, configs prod |
| Comandos | PreToolUse Bash | rm -rf, force push, deploys |
| Commits | PostToolUse Bash | Detecção de credenciais staged |
| Histórico | PreToolUse Bash | Rewrite de histórico público |
| Branches | PreToolUse Bash | Commits diretos em protected |
| Auditoria | PreToolUse `""` | Log de todas as ações sensíveis |

## Armadilhas

**Falsa sensação de segurança**: hooks protegem contra ações do agente. Não protegem contra você mesmo executando comandos no terminal. Os hooks são uma política para o Claude Code, não para o shell.

**Hooks commitados no projeto**: se você commitar um hook que bloqueia `git commit`, pode criar uma situação impossível. Hooks de projeto devem ser revisados pelo time.

**Ausência de logging**: bloquear sem logar significa que você não sabe o que o agente tentou fazer. Sempre inclua logging nas regras de bloqueio.

## Veja também

- [[03-Dominios/IA/Claude Code/Hooks e Guardrails/02 - PreToolUse|02 - PreToolUse]] — controle de execução
- [[03-Dominios/IA/Claude Code/Hooks e Guardrails/05 - Guardrails|05 - Guardrails]] — guardrails gerais
- [[03-Dominios/IA/Claude Code/Hooks e Guardrails/06 - Delegar permissão|06 - Delegar permissão]] — meta-agente para decisões complexas
- [[03-Dominios/IA/Claude Code/Time e Automação/06 - Segurança organizacional|06 - Segurança organizacional]] — segurança em contexto de time
- [[03-Dominios/IA/Claude Code/Hooks e Guardrails/index|Hooks e Guardrails]] — índice do galho
