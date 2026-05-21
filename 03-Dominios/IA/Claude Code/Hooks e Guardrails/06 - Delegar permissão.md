---
title: "Delegar permissão a outro LLM — pattern meta-agente"
type: concept
publish: true
created: 2026-05-13
updated: 2026-05-13
status: seedling
tags:
  - claude-code
  - hooks
  - meta-agente
  - llm-delegation
  - pretooluse
---

# Delegar permissão a outro LLM — pattern meta-agente

> [!abstract] TL;DR
> Em vez de regras fixas de allow/block, você pode delegar a decisão de permissão a outro LLM. O hook chama um segundo Claude via `claude --print`, passa o comando como contexto, e usa a resposta para bloquear ou aprovar. É o pattern meta-agente: um agente supervisiona o outro. Útil quando a lógica de segurança é contextual demais para ser reduzida a regex.

## Por que delegar a um LLM

Guardrails baseados em padrões têm um limite: o que é perigoso depende do contexto. `rm -rf dist/` é rotina. `rm -rf src/` é catastrófico. Um regex que bloqueia um bloqueia o outro.

Um LLM supervisor pode raciocinar sobre o contexto:
- O comando está removendo um diretório de build ou código fonte?
- Essa query SQL está lendo ou deletando dados?
- Esse deploy é para staging ou produção?

A delegação traz raciocínio contextual para o ponto de controle.

## Pattern básico

```bash
#!/bin/bash
# hooks/llm-guard.sh

INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.tool_name')
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // ""')

# Só processa comandos Bash
if [[ "$TOOL" != "Bash" ]]; then exit 0; fi

# Delegar avaliação ao LLM
PROMPT="Você é um guardrail de segurança. Avalie se este comando bash é seguro para executar em um ambiente de desenvolvimento.

Comando: $COMMAND

Responda APENAS com uma dessas opções:
- SAFE: se o comando é rotineiro e não representa risco
- UNSAFE: <motivo curto> se o comando pode causar perda de dados ou acesso não autorizado

Seja conservador: em caso de dúvida, responda UNSAFE."

DECISION=$(echo "$PROMPT" | claude --print --max-tokens 100 2>/dev/null)

if echo "$DECISION" | grep -q "^UNSAFE"; then
  MOTIVO=$(echo "$DECISION" | sed 's/^UNSAFE: //' | sed 's/^UNSAFE/comando potencialmente destrutivo/')
  echo "META-AGENTE: $MOTIVO" >&2
  exit 1
fi

exit 0
```

## Passando contexto adicional ao meta-agente

O LLM supervisor toma decisões melhores com mais contexto:

```bash
#!/bin/bash
# hooks/llm-guard-with-context.sh

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // ""')
BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
PWD_DIR=$(pwd)

PROMPT="Você é um guardrail de segurança avaliando uma ação do Claude Code.

Contexto do projeto:
- Diretório: $PWD_DIR
- Branch atual: $BRANCH

Comando a executar: $COMMAND

Este comando é seguro? Responda SAFE ou UNSAFE: <motivo>."

DECISION=$(echo "$PROMPT" | claude --print --max-tokens 150 2>/dev/null)

if echo "$DECISION" | grep -qi "^UNSAFE"; then
  echo "BLOQUEADO pelo meta-agente: $DECISION" >&2
  exit 1
fi

exit 0
```

## Meta-agente para edições de arquivo

Delegar avaliação de edições de arquivo — útil quando o conteúdo importa, não só o caminho:

```bash
#!/bin/bash
# hooks/llm-file-guard.sh

INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.tool_name')
FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path // ""')
NEW_CONTENT=$(echo "$INPUT" | jq -r '.tool_input.new_string // ""')

if [[ "$TOOL" != "Edit" && "$TOOL" != "Write" ]]; then exit 0; fi

# Verificar apenas arquivos de configuração
if [[ ! "$FILE" =~ \.(json|yaml|yml|env|toml)$ ]]; then exit 0; fi

PROMPT="Avalie se esta edição de arquivo de configuração é segura.

Arquivo: $FILE
Conteúdo novo: $NEW_CONTENT

A edição expõe credenciais, remove configurações críticas, ou introduz valores inválidos?
Responda SAFE ou UNSAFE: <motivo>."

DECISION=$(echo "$PROMPT" | claude --print --max-tokens 100 2>/dev/null)

if echo "$DECISION" | grep -qi "^UNSAFE"; then
  echo "META-AGENTE bloqueou edição: $DECISION" >&2
  exit 1
fi

exit 0
```

## Custo e latência

> [!warning] Cada chamada ao meta-agente custa tokens e tempo
> Uma chamada `claude --print` adiciona latência de 2-5 segundos por tool call avaliada. Para sessões intensas, isso acumula. Use seletivamente:
> - Só em tool calls de alto risco (não em todas as Reads)
> - Com `--max-tokens` baixo (a resposta deve ser curta)
> - Considere fazer pré-filtragem com regex antes de invocar o LLM

```bash
# Pré-filtro: só delega ao LLM se o comando tem potencial de risco
RISK_PATTERNS=("rm " "DROP" "DELETE" "git push" "kubectl" "terraform")

NEEDS_REVIEW=false
for pattern in "${RISK_PATTERNS[@]}"; do
  if echo "$COMMAND" | grep -qi "$pattern"; then
    NEEDS_REVIEW=true
    break
  fi
done

if [[ "$NEEDS_REVIEW" == "false" ]]; then exit 0; fi

# Só aqui invoca o LLM
DECISION=$(echo "$PROMPT" | claude --print --max-tokens 100 2>/dev/null)
```

## Fallback em caso de falha

Se o meta-agente falhar (API offline, timeout), defina comportamento explícito:

```bash
# Invocar meta-agente com timeout
DECISION=$(timeout 10 bash -c "echo '$PROMPT' | claude --print --max-tokens 100" 2>/dev/null)

# Fallback em caso de timeout ou erro
if [[ -z "$DECISION" || $? -ne 0 ]]; then
  # Fail-open: permitir e logar
  echo "$(date -u) | META-AGENTE FALHOU | $COMMAND" >> ~/.claude/meta-agent-failures.log
  exit 0
  
  # OU fail-closed: bloquear (mais seguro para produção)
  # echo "Meta-agente indisponível. Ação bloqueada por precaução." >&2
  # exit 1
fi
```

Escolha fail-open (mais produtivo) ou fail-closed (mais seguro) baseado no ambiente.

## Armadilhas

**Confiar cegamente na resposta do meta-agente**: LLMs podem cometer erros de avaliação. Use o meta-agente como camada adicional, não como substituto completo dos guardrails baseados em padrões.

**Prompt injection via comando**: um atacante que controla o conteúdo do comando pode tentar manipular o meta-agente. Escape o conteúdo do comando antes de incluir no prompt, ou trate o output do meta-agente como dado não confiável.

**Recursão**: se o meta-agente chama `claude --print`, que dispara hooks, que chamam o meta-agente — você tem recursão infinita. Certifique-se de que o subagente não herda os hooks que o dispararam (use `--no-hooks` se disponível, ou desabilite via variável de ambiente).

**Custo invisível**: o meta-agente corre na conta da API do projeto. Em equipes, isso pode escalar rapidamente se cada dev tiver o hook habilitado globalmente.

## Veja também

- [[03-Dominios/IA/Claude Code/Hooks e Guardrails/02 - PreToolUse|02 - PreToolUse]] — onde o meta-agente é integrado
- [[03-Dominios/IA/Claude Code/Hooks e Guardrails/05 - Guardrails|05 - Guardrails]] — guardrails baseados em padrões como alternativa
- [[03-Dominios/IA/Claude Code/Workflows/07 - Sub-agents e dispatch|07 - Sub-agents e dispatch]] — como agentes chamam outros agentes
- [[03-Dominios/IA/Claude Code/Hooks e Guardrails/08 - Testando hooks|08 - Testando hooks]] — como testar o meta-agente
- [[03-Dominios/IA/Claude Code/Hooks e Guardrails/index|Hooks e Guardrails]] — índice do galho
