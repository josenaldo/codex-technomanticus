---
title: "Testando e debugando hooks"
type: concept
publish: true
created: 2026-05-13
updated: 2026-05-13
status: seedling
tags:
  - claude-code
  - hooks
  - testing
  - debugging
  - desenvolvimento
---

# Testando e debugando hooks

> [!abstract] TL;DR
> Hooks que não são testados não são confiáveis. Um guardrail que você acha que bloqueia `rm -rf` mas na prática não bloqueia é pior que não ter guardrail — dá falsa confiança. Esta nota cobre como testar hooks manualmente, como escrever testes automatizados para hooks, como debugar hooks que não disparam, e armadilhas comuns de hooks que parecem funcionar mas falham em casos reais.

## Teste manual — simular input de hook

A forma mais rápida: passar o JSON que o Claude Code passaria para o hook diretamente.

```bash
# Teste básico: verificar se o hook bloqueia force push
echo '{"tool_name": "Bash", "tool_input": {"command": "git push --force origin main"}}' \
  | ~/.claude/hooks/guardrails.sh

echo "Exit code: $?"  # Deve ser 1 (bloqueado)
```

```bash
# Verificar que o hook NÃO bloqueia comandos normais
echo '{"tool_name": "Bash", "tool_input": {"command": "git status"}}' \
  | ~/.claude/hooks/guardrails.sh

echo "Exit code: $?"  # Deve ser 0 (aprovado)
```

```bash
# Testar hook de arquivo sensível
echo '{"tool_name": "Edit", "tool_input": {"file_path": "/home/user/.env", "old_string": "x", "new_string": "y"}}' \
  | ~/.claude/hooks/guardrails.sh

echo "Exit code: $?"  # Deve ser 1 (bloqueado)
```

## Script de testes automatizados

Para guardrails críticos, um script que documenta e verifica o comportamento esperado:

```bash
#!/bin/bash
# tests/test-guardrails.sh

HOOK=~/.claude/hooks/guardrails.sh
PASS=0
FAIL=0

assert_blocked() {
  local description="$1"
  local input="$2"
  
  echo "$input" | "$HOOK" > /dev/null 2>&1
  if [[ $? -ne 0 ]]; then
    echo "✓ BLOQUEADO: $description"
    ((PASS++))
  else
    echo "✗ PASSOU (deveria bloquear): $description"
    ((FAIL++))
  fi
}

assert_allowed() {
  local description="$1"
  local input="$2"
  
  echo "$input" | "$HOOK" > /dev/null 2>&1
  if [[ $? -eq 0 ]]; then
    echo "✓ PERMITIDO: $description"
    ((PASS++))
  else
    echo "✗ BLOQUEADO (deveria permitir): $description"
    ((FAIL++))
  fi
}

# --- Testes de Bash ---
assert_blocked "force push --force" \
  '{"tool_name":"Bash","tool_input":{"command":"git push --force origin main"}}'

assert_blocked "force push -f" \
  '{"tool_name":"Bash","tool_input":{"command":"git push -f origin main"}}'

assert_blocked "DROP TABLE" \
  '{"tool_name":"Bash","tool_input":{"command":"psql -c \"DROP TABLE users\""}}'

assert_blocked "deploy em producao" \
  '{"tool_name":"Bash","tool_input":{"command":"npm run deploy prod"}}'

assert_allowed "git status" \
  '{"tool_name":"Bash","tool_input":{"command":"git status"}}'

assert_allowed "npm install" \
  '{"tool_name":"Bash","tool_input":{"command":"npm install lodash"}}'

assert_allowed "rm de arquivo temporario" \
  '{"tool_name":"Bash","tool_input":{"command":"rm /tmp/debug.log"}}'

# --- Testes de Edit ---
assert_blocked "editar .env" \
  '{"tool_name":"Edit","tool_input":{"file_path":"/projeto/.env","old_string":"x","new_string":"y"}}'

assert_blocked "editar producao.json" \
  '{"tool_name":"Edit","tool_input":{"file_path":"/config/producao.json","old_string":"x","new_string":"y"}}'

assert_allowed "editar arquivo ts" \
  '{"tool_name":"Edit","tool_input":{"file_path":"/src/services/orders.ts","old_string":"x","new_string":"y"}}'

# --- Resultado ---
echo ""
echo "Resultado: $PASS passou, $FAIL falhou"
[[ $FAIL -eq 0 ]]
```

Tornar executável e rodar:
```bash
chmod +x tests/test-guardrails.sh
./tests/test-guardrails.sh
```

## Debugar hook que não dispara

Se um hook está configurado mas não parece executar, verifique em sequência:

**1. O settings.json está sintaticamente correto?**
```bash
cat ~/.claude/settings.json | jq '.' > /dev/null && echo "JSON válido" || echo "JSON inválido"
```

**2. O path do hook está correto?**
```bash
# O hook precisa existir e ser executável
ls -la ~/.claude/hooks/guardrails.sh
```

**3. O hook tem permissão de execução?**
```bash
chmod +x ~/.claude/hooks/guardrails.sh
```

**4. O matcher está correto?**

`"Bash"` corresponde à tool Bash, não a comandos bash. Um matcher `"bash"` (minúsculo) não vai corresponder.

**5. Adicionar logging temporário para confirmar que o hook executa:**
```bash
#!/bin/bash
echo "$(date) HOOK EXECUTOU: $(cat)" >> /tmp/hook-debug.log
# ... resto do hook
```

Depois observe `/tmp/hook-debug.log` durante uma sessão.

## Debugar saída do hook

Para ver o que o hook está retornando ao Claude:

```bash
# Verificar saída stderr (mensagem de erro que o agente vê)
echo '{"tool_name":"Bash","tool_input":{"command":"git push --force origin main"}}' \
  | ~/.claude/hooks/guardrails.sh 2>&1

# Verificar saída stdout (JSON de decisão, se houver)
echo '{"tool_name":"Bash","tool_input":{"command":"git push --force origin main"}}' \
  | ~/.claude/hooks/guardrails.sh 2>/dev/null
```

## Testar hook de Stop

Stop hook não recebe input de tool call. Simule passando o JSON de sessão:

```bash
echo '{"session_id":"test-123","stop_reason":"end_turn","total_turns":10,"total_tokens":5000}' \
  | ~/.claude/hooks/notify-stop.sh
```

Para verificar o hook de cleanup:
```bash
# Criar arquivo temporário
touch /tmp/debug-test.log

# Rodar hook
echo '{"stop_reason":"end_turn"}' | ~/.claude/hooks/cleanup-temp.sh

# Verificar se removeu
ls /tmp/debug-test.log 2>/dev/null && echo "Arquivo ainda existe" || echo "Removido com sucesso"
```

## Armadilhas de hooks que falham silenciosamente

**jq não instalado**: se `jq` não está disponível, `$(echo "$INPUT" | jq -r '...')` retorna uma string vazia e todos os checks falham silenciosamente. Adicione no início:
```bash
command -v jq > /dev/null || { echo "ERRO: jq não encontrado. Hook inativo." >&2; exit 0; }
```

**Regex muito específico**:
```bash
# Este regex NÃO pega "push  --force" (dois espaços)
echo "$COMMAND" | grep -q "push --force"

# Este pega variações de espaço
echo "$COMMAND" | grep -qE "push\s+--force"
```

**Aspas no JSON quebrando o parse**:
```bash
# Problemático se o comando tiver aspas
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command')

# Mais seguro — jq lida com escaping corretamente
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')
```

**Exit code do último comando**:
```bash
# Este hook parece bloquear mas não bloqueia
if echo "$COMMAND" | grep -q "DROP TABLE"; then
  echo "Bloqueado" >&2
  # esqueceu o exit 1!
fi
exit 0  # sempre sai com 0
```

**Hook não-executável com shebang errado**:
```bash
# Garanta que o shebang aponta para o bash correto
which bash  # /bin/bash ou /usr/bin/bash ou /usr/local/bin/bash
```

## Validação de hook em CI

Para garantir que hooks continuam funcionando após mudanças:

```yaml
# .github/workflows/test-hooks.yml
name: Test Claude Code Hooks

on: [push, pull_request]

jobs:
  test-hooks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Install dependencies
        run: sudo apt-get install -y jq
      
      - name: Make hooks executable
        run: chmod +x .claude/hooks/*.sh
      
      - name: Run hook tests
        run: ./tests/test-hooks.sh
```

## Veja também

- [[03-Dominios/IA/Claude Code/Hooks e Guardrails/01 - Sistema de hooks|01 - Sistema de hooks]] — lifecycle e configuração
- [[03-Dominios/IA/Claude Code/Hooks e Guardrails/02 - PreToolUse|02 - PreToolUse]] — o hook mais testado
- [[03-Dominios/IA/Claude Code/Hooks e Guardrails/05 - Guardrails|05 - Guardrails]] — o que testar
- [[03-Dominios/IA/Claude Code/Hooks e Guardrails/06 - Delegar permissão|06 - Delegar permissão]] — testar o meta-agente
- [[03-Dominios/IA/Claude Code/Hooks e Guardrails/index|Hooks e Guardrails]] — índice do galho
