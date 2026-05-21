---
title: "Dispatch via `claude -p` — casos de uso e padrões"
type: concept
publish: true
created: 2026-05-13
updated: 2026-05-13
status: seedling
tags:
  - claude-code
  - dispatch
  - headless
  - cli
  - automacao
---

# Dispatch via `claude -p` — casos de uso e padrões

> [!abstract] TL;DR
> `claude -p` (ou `claude --print`) é a interface de dispatch: um processo externo invoca o agente com um prompt, captura o output, e age sobre ele. Além de CI/CD, esse padrão aparece em scripts de manutenção, hooks de git que consultam o modelo, e em orquestradores que coordenam múltiplos agentes. A chave é tratar `claude -p` como qualquer outro processo CLI que lê stdin, escreve stdout, e retorna exit code.

## O padrão básico de dispatch

```bash
# Invocação direta
RESPOSTA=$(claude -p "Prompt aqui")

# Com contexto via pipe
CONTEXTO=$(cat arquivo.ts)
RESPOSTA=$(echo "$CONTEXTO" | claude -p "Analise este código")

# Com arquivo de prompt
RESPOSTA=$(claude -p "$(cat prompts/analise.txt)")

# Combinando contexto e instrução
RESPOSTA=$(claude -p "$(cat prompts/instrucao.txt)

CÓDIGO:
$(cat src/main.ts)")
```

## Casos de uso práticos

### Script de manutenção

```bash
#!/bin/bash
# scripts/cleanup-todos.sh
# Encontra TODOs, pergunta ao agente quais vale a pena criar como issues

TODOS=$(grep -rn "TODO\|FIXME\|HACK" src/ --include="*.ts")

if [[ -z "$TODOS" ]]; then
  echo "Nenhum TODO encontrado"
  exit 0
fi

ANALISE=$(echo "$TODOS" | claude -p \
  "Analise esta lista de TODOs e identifique os 3 mais críticos para o sistema.
  Para cada um, retorne uma linha no formato:
  CRÍTICO: arquivo:linha — descrição")

echo "$ANALISE"
```

### Hook de commit inteligente

```bash
#!/bin/bash
# .git/hooks/commit-msg
# Verifica se a mensagem de commit segue o padrão do projeto

MENSAGEM=$(cat "$1")
RESULTADO=$(claude -p \
  --max-turns 1 \
  --allowedTools "" \
  "A mensagem de commit abaixo segue o padrão Conventional Commits?
  Se sim, responda: OK
  Se não, responda: PROBLEMA: <explicação>

  Mensagem: $MENSAGEM")

if echo "$RESULTADO" | grep -q "^PROBLEMA"; then
  MOTIVO=$(echo "$RESULTADO" | sed 's/^PROBLEMA: //')
  echo "Commit rejeitado: $MOTIVO" >&2
  exit 1
fi
```

### Análise incremental de logs

```bash
#!/bin/bash
# scripts/analyze-errors.sh
# Analisa erros novos desde o último check

TIMESTAMP_ARQUIVO=".last-check-timestamp"
ULTIMA_VERIFICACAO=$(cat "$TIMESTAMP_ARQUIVO" 2>/dev/null || echo "1 hora atrás")

ERROS=$(journalctl -u meu-servico --since "$ULTIMA_VERIFICACAO" -p err)

if [[ -z "$ERROS" ]]; then
  echo "Sem novos erros desde $ULTIMA_VERIFICACAO"
else
  ANALISE=$(echo "$ERROS" | claude -p \
    "Estes são os erros de produção da última hora.
    Identifique: padrões recorrentes, erros novos (que não eram esperados), e urgência.
    Formato: uma linha por achado.")
  echo "$ANALISE"
fi

date > "$TIMESTAMP_ARQUIVO"
```

### Orquestrador simples de subagentes

```bash
#!/bin/bash
# Dispatch paralelo para análise de múltiplos módulos

MODULOS=("src/auth" "src/payments" "src/orders")
RESULTADOS=()

for modulo in "${MODULOS[@]}"; do
  RESULTADO=$(find "$modulo" -name "*.ts" | head -5 | xargs cat | claude -p \
    "Analise este módulo e identifique os maiores riscos de segurança.
    Máximo 3 riscos, formato: [RISCO] descrição" \
    --allowedTools "" \
    --max-turns 3) &
  RESULTADOS+=("$!")  # Guarda PID do subshell
done

wait  # Aguarda todos terminarem

# Coletar resultados (simplificado — em produção, use arquivos temporários)
echo "Análise completa"
```

## Padrões de orquestração

### Sequencial com contexto acumulado

```bash
# Passo 1: identificar problemas
PROBLEMAS=$(cat src/auth.ts | claude -p \
  "Liste os problemas de segurança encontrados. Um por linha.")

# Passo 2: priorizar (usa output do passo 1 como contexto)
PRIORIZADOS=$(echo "$PROBLEMAS" | claude -p \
  "Priorize estes problemas por risco. Formato: [ALTO/MÉDIO/BAIXO] problema")

# Passo 3: gerar tickets (usa output do passo 2)
TICKETS=$(echo "$PRIORIZADOS" | claude -p \
  "Para os problemas ALTO, gere descrições de issue no formato GitHub.
  Inclua: título, descrição, steps to reproduce.")

echo "$TICKETS" > /tmp/security-tickets.md
```

### Fan-out e agregação

```bash
#!/bin/bash
# Analisa cada arquivo alterado no PR, agrega ao final

ARQUIVOS=$(git diff --name-only origin/main...HEAD | grep '\.ts$')
TMPDIR=$(mktemp -d)

# Fan-out: análise paralela
for arquivo in $ARQUIVOS; do
  (
    ANALISE=$(cat "$arquivo" | claude -p \
      "--allowedTools ''" \
      "Identifique problemas neste arquivo. Formato: [ARQUIVO:LINHA] problema")
    echo "=== $arquivo ===" > "$TMPDIR/$arquivo.txt"
    echo "$ANALISE" >> "$TMPDIR/$arquivo.txt"
  ) &
done

wait

# Agregação: consolidar todos os resultados
TODOS=$(cat "$TMPDIR"/*.txt)
RESUMO=$(echo "$TODOS" | claude -p \
  "Estes são os problemas encontrados em cada arquivo de um PR.
  Crie um resumo executivo: qual é o risco total, quais são os 3 problemas mais críticos.")

echo "$RESUMO"
rm -rf "$TMPDIR"
```

## Controle de saída

```bash
# JSON estruturado — mais fácil de processar
RESULTADO=$(claude -p \
  --output-format json \
  "Analise src/auth.ts e retorne JSON:
  {\"has_issues\": boolean, \"issues\": [{\"line\": number, \"severity\": string, \"description\": string}]}")

# Verificar se tem problemas
TEM_PROBLEMAS=$(echo "$RESULTADO" | jq '.has_issues')
if [[ "$TEM_PROBLEMAS" == "true" ]]; then
  echo "$RESULTADO" | jq '.issues[] | "[" + .severity + "] linha " + (.line|tostring) + ": " + .description'
fi
```

## Timeout e retry

```bash
# Timeout explícito
RESULTADO=$(timeout 60 claude -p --max-turns 5 "..." || echo "TIMEOUT")

# Retry simples com backoff
for tentativa in 1 2 3; do
  RESULTADO=$(claude -p "..." 2>/dev/null)
  EXIT_CODE=$?
  if [[ $EXIT_CODE -eq 0 ]]; then
    break
  fi
  echo "Tentativa $tentativa falhou, aguardando..."
  sleep $((tentativa * 5))
done
```

## Armadilhas

**Prompt com newlines quebrando o argumento**: use heredoc ou arquivo de prompt para prompts longos em vez de string com `\n`:

```bash
# Problemático
claude -p "linha 1\nlinha 2"  # \n é interpretado literalmente

# Correto
claude -p "$(printf 'linha 1\nlinha 2')"
# Ou
claude -p << 'EOF'
linha 1
linha 2
EOF
```

**Capturar stderr junto com stdout**: se o script usa `RESULTADO=$(claude -p ...)`, erros internos do agente vão para stderr e não aparecem em `$RESULTADO`. Separe os canais ou redirecione stderr para log separado.

**Contexto grande demais em loop**: se você faz `cat arquivo | claude -p` em loop para dezenas de arquivos grandes, cada chamada pode exceder o limite de contexto. Adicione verificação de tamanho antes de passar para o agente.

## Veja também

- [[03-Dominios/IA/Claude Code/Time e Automação/01 - Headless mode|01 - Headless mode]] — flags e opções de `claude --print`
- [[03-Dominios/IA/Claude Code/Time e Automação/02 - CI-CD com GitHub Actions|02 - CI/CD com GitHub Actions]] — dispatch em pipelines
- [[03-Dominios/IA/Claude Code/Time e Automação/05 - Controle de custo|05 - Controle de custo]] — cada invocação consome tokens
- [[03-Dominios/IA/Claude Code/Time e Automação/index|Time e Automação]] — índice do galho
