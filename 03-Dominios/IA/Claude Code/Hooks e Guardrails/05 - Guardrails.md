---
title: "Guardrails — bloquear comandos destrutivos"
type: concept
publish: true
created: 2026-05-13
updated: 2026-05-13
status: seedling
tags:
  - claude-code
  - hooks
  - guardrails
  - seguranca
  - producao
---

# Guardrails — bloquear comandos destrutivos

> [!abstract] TL;DR
> Guardrails são PreToolUse hooks que bloqueiam ações destrutivas ou de alto risco antes de executar. São a diferença entre usar Claude Code com auto mode de forma segura ou com risco real de perda de dados. A configuração global (~/.claude/settings.json) garante que os guardrails se aplicam em todos os projetos.

## Por que guardrails são necessários

Em modo automático, o Claude Code executa tool calls sem pedir confirmação. Isso é produtivo — mas significa que um mal-entendimento pode resultar em:

- `rm -rf` em diretório errado
- `git push --force` que sobrescreve o trabalho de outros
- `DROP TABLE` em banco de produção
- Deploy acidental em ambiente errado

Guardrails são a rede de segurança que transforma "confia no agente" em "confia no agente dentro de limites definidos".

## Guardrail básico — script unificado

Em vez de múltiplos hooks, um script centralizado é mais fácil de manter:

```bash
#!/bin/bash
# ~/.claude/hooks/guardrails.sh

INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.tool_name')
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // ""')
FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path // ""')

block() {
  echo "GUARDRAIL: $1" >&2
  exit 1
}

# --- Bash guardrails ---
if [[ "$TOOL" == "Bash" ]]; then
  
  # Force push
  echo "$COMMAND" | grep -qE "push\s+(--force|-f)" \
    && block "force push bloqueado. Use --force-with-lease se necessário."
  
  # rm -rf em caminhos não-temporários
  if echo "$COMMAND" | grep -qE "rm\s+-rf?\s+[^/]*(src|app|lib|config|data)"; then
    block "rm -rf em diretório crítico bloqueado."
  fi
  
  # Comandos de banco em produção
  echo "$COMMAND" | grep -qiE "(DROP\s+TABLE|TRUNCATE|DELETE\s+FROM)" \
    && block "operação destrutiva de banco bloqueada. Execute manualmente."
  
  # Deploy em produção sem confirmação
  echo "$COMMAND" | grep -qE "(deploy|kubectl)\s.*prod" \
    && block "deploy em produção bloqueado. Execute manualmente."
fi

# --- Edit guardrails ---
if [[ "$TOOL" == "Edit" || "$TOOL" == "Write" ]]; then
  
  # Arquivos de credenciais
  echo "$FILE" | grep -qE "\.(env|pem|key|pfx)$" \
    && block "edição de arquivo de credenciais bloqueada."
  
  # Config de produção
  echo "$FILE" | grep -qE "(prod|production)\.(json|yaml|yml|env)" \
    && block "edição de config de produção bloqueada."
fi

exit 0
```

Configuração em `~/.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "",
        "hooks": [
          { "type": "command", "command": "~/.claude/hooks/guardrails.sh" }
        ]
      }
    ]
  }
}
```

O matcher vazio `""` faz o hook executar para todas as tool calls.

## Guardrails por ambiente

Para projetos com ambiente de produção, guardrail baseado em variável de ambiente ou branch:

```bash
#!/bin/bash
# hooks/production-guard.sh

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // ""')
BRANCH=$(git branch --show-current 2>/dev/null)

# Em branch main/master, bloquear deploys diretos
if [[ "$BRANCH" =~ ^(main|master)$ ]]; then
  echo "$COMMAND" | grep -qE "^(npm run deploy|kubectl apply|terraform apply)" \
    && { echo "GUARDRAIL: deploy direto de $BRANCH bloqueado." >&2; exit 1; }
fi

# Se variável de ambiente indica produção
if [[ "$NODE_ENV" == "production" || "$ENVIRONMENT" == "prod" ]]; then
  echo "$COMMAND" | grep -qE "^(rm|mv|cp)\s+-r" \
    && { echo "GUARDRAIL: operação recursiva em produção bloqueada." >&2; exit 1; }
fi

exit 0
```

## Guardrails para git

Proteções específicas para operações git:

```bash
#!/bin/bash
# hooks/git-guard.sh

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // ""')

# Só processa comandos git
echo "$COMMAND" | grep -q "^git " || exit 0

# force push
echo "$COMMAND" | grep -qE "push.*(--force|-f)" \
  && { echo "GUARDRAIL: force push bloqueado. Use --force-with-lease." >&2; exit 1; }

# reset --hard (descarta trabalho não commitado)
echo "$COMMAND" | grep -qE "reset\s+--hard" \
  && { echo "GUARDRAIL: git reset --hard bloqueado. Use git stash primeiro." >&2; exit 1; }

# clean -f (deleta arquivos não rastreados)
echo "$COMMAND" | grep -qE "clean\s+(-f|--force)" \
  && { echo "GUARDRAIL: git clean -f bloqueado." >&2; exit 1; }

# branch -D (força deletar branch, ignora merge check)
echo "$COMMAND" | grep -qE "branch\s+-D" \
  && { echo "GUARDRAIL: git branch -D bloqueado. Use -d (seguro)." >&2; exit 1; }

exit 0
```

## Configuração recomendada por camada

**Global** (`~/.claude/settings.json`) — proteções universais:
- Force push, rm -rf, DROP TABLE, credenciais
- Aplica em todos os projetos automaticamente

**Projeto** (`.claude/settings.json`) — proteções específicas do projeto:
- Arquivos de config do projeto específico
- Ambientes específicos (prod, staging)
- Comandos específicos do stack

**Local** (`.claude/settings.local.json`) — exceções pessoais:
- Se você precisa de uma ação que o guardrail global bloqueia, crie uma exceção local
- Nunca commitado — só afeta você

## Quando o guardrail bloqueia o agente legítimo

Se um guardrail bloqueia uma ação que o agente deveria fazer, o agente recebe o erro e geralmente:
1. Tenta uma abordagem alternativa
2. Reporta o bloqueio para você

Você pode então:
- Executar o comando manualmente (melhor opção)
- Desabilitar temporariamente o guardrail e re-executar
- Ajustar o guardrail para ser mais granular

## Armadilhas

**Guardrails muito restritivos**: bloquear todos os `rm` impede que o agente faça limpeza legítima de arquivos temporários. Seja específico nos padrões.

**Guardrails em settings.json do projeto commitado**: se você commitar guardrails que bloqueiam ações do agente para todo o time, pode atrapalhar os colegas. Guardrails do projeto devem ser discutidos com o time.

**Confiar só nos guardrails**: guardrails cobrem padrões conhecidos. Para projetos críticos, revise o que o agente faz antes de executar com `/plan`.

## Veja também

- [[03-Dominios/IA/Claude Code/Hooks e Guardrails/02 - PreToolUse|02 - PreToolUse]] — como PreToolUse funciona
- [[03-Dominios/IA/Claude Code/Hooks e Guardrails/07 - Segurança com hooks|07 - Segurança com hooks]] — segurança além de guardrails
- [[03-Dominios/IA/Claude Code/Hooks e Guardrails/08 - Testando hooks|08 - Testando hooks]] — testar que guardrails funcionam
- [[03-Dominios/IA/Claude Code/Configuração/05 - Permissions|05 - Permissions]] — controle de permissões como alternativa a hooks
- [[03-Dominios/IA/Claude Code/Hooks e Guardrails/index|Hooks e Guardrails]] — índice do galho
