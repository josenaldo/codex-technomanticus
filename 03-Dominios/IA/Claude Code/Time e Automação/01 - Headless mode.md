---
title: "Headless mode — Claude Code sem interação humana"
type: concept
publish: true
created: 2026-05-13
updated: 2026-05-13
status: seedling
tags:
  - claude-code
  - headless
  - automacao
  - cli
  - ci-cd
---

# Headless mode — Claude Code sem interação humana

> [!abstract] TL;DR
> Headless mode é o Claude Code rodando sem terminal interativo: recebe um prompt via argumento, executa as ações necessárias, escreve o resultado em stdout, e sai. Usando `claude --print` ou `claude -p`, você pode invocar o agente como qualquer outro processo CLI — em scripts, CI/CD, cron jobs, ou como subprocesso de outra ferramenta.

## O que é headless mode

No modo interativo padrão, Claude Code abre um REPL onde você digita prompts e o agente responde enquanto a sessão persiste. Em headless mode:

- O prompt é passado como argumento ou via stdin
- O agente executa e termina (processo único, sem loop)
- A saída vai para stdout — pode ser capturada por scripts
- Não há TTY necessário — funciona em CI/CD

```bash
# Modo interativo — abre o REPL
claude

# Headless — executa e sai
claude --print "Qual é a função principal em src/main.ts?"
claude -p "Analisa os últimos 10 commits e identifica regressões potenciais"
```

## Flags essenciais para headless

```bash
# --print / -p: não abre REPL, imprime resposta e sai
claude --print "Descreva a arquitetura deste projeto em 3 frases"

# --output-format: controla o formato da resposta
claude --print --output-format text "Listar todas as funções exportadas"
claude --print --output-format json "Listar todas as funções exportadas"

# --max-turns: limita quantas tool calls o agente pode fazer
claude --print --max-turns 5 "Revise o arquivo src/auth.ts"

# --allowedTools: restringe quais tools o agente pode usar
claude --print --allowedTools "Read,Grep" "Encontre todos os usos de console.log"

# --disallowedTools: bloqueia tools específicas
claude --print --disallowedTools "Bash,Write" "Revise este código"

# --no-permission-prompts: não pede confirmação — executa tudo automaticamente
claude --print --no-permission-prompts "Refatora o módulo de autenticação"
```

> [!warning]
> `--no-permission-prompts` faz o agente executar sem nenhuma confirmação humana. Use apenas em ambientes controlados com guardrails configurados via hooks. Sem guardrails, o agente pode modificar qualquer arquivo ou executar qualquer comando.

## Passando contexto via stdin

Para prompts longos ou para passar conteúdo dinâmico:

```bash
# Prompt via stdin com heredoc
claude --print << 'EOF'
Analise o arquivo abaixo e identifique problemas de segurança:

$(cat src/auth/login.ts)
EOF

# Pipe de outro comando
git diff HEAD~1 | claude --print "Revisar este diff e identificar bugs introduzidos"

# Arquivo como contexto
cat docs/requirements.md | claude --print "Listar os requisitos não implementados ainda"
```

## Output em JSON para automação

```bash
# Resposta estruturada
RESULTADO=$(claude --print --output-format json "
Analise src/api/orders.ts e retorne JSON com:
- has_error_handling: boolean
- missing_validations: string[]
- security_issues: string[]
")

# Processar com jq
echo "$RESULTADO" | jq '.missing_validations[]'
```

## Códigos de saída

```
0  — agente completou sem erro
1  — erro de execução (tool falhou, permissão negada, etc.)
2  — erro de configuração (API key inválida, etc.)
```

Scripts podem verificar o código de saída para reagir a falhas:

```bash
if ! claude --print "Verifica se os testes passam" --allowedTools "Bash"; then
  echo "O agente reportou um problema"
  exit 1
fi
```

## Diferença entre headless e subagente

**Headless**: você invoca `claude --print` de um script externo. O agente tem suas próprias tools nativas. Sem REPL.

**Subagente** (via API ou Agent SDK): outro processo invoca o modelo com contexto específico. Mais controle sobre ferramentas e contexto, mas requer código Python/TypeScript para orquestrar.

Para automação simples (CI/CD, scripts), headless é suficiente. Para orquestração complexa (múltiplos agentes em paralelo, handoffs), use o Agent SDK.

## Armadilhas

**Sem --no-permission-prompts em CI**: o agente vai pausar pedindo confirmação e o job vai travar até o timeout. Sempre use `--no-permission-prompts` em ambientes não-interativos.

**Output misturado com logs internos**: por padrão, mensagens de status do agente vão para stderr e a resposta vai para stdout. Separe corretamente em scripts:

```bash
RESPOSTA=$(claude --print "..." 2>/dev/null)  # Só a resposta
claude --print "..." > resposta.txt 2> logs.txt  # Separados
```

**Max-turns sem limite em tarefa longa**: uma tarefa aberta sem `--max-turns` pode rodar indefinidamente, consumindo tokens e dinheiro. Defina um limite conservador para automações.

**API key não disponível no ambiente CI**: a key precisa estar em `ANTHROPIC_API_KEY` no ambiente. Configure como secret no sistema de CI.

## Veja também

- [[03-Dominios/IA/Claude Code/Time e Automação/02 - CI-CD com GitHub Actions|02 - CI/CD com GitHub Actions]] — headless em pipelines
- [[03-Dominios/IA/Claude Code/Time e Automação/03 - Dispatch via claude -p|03 - Dispatch via `claude -p`]] — padrões de invocação
- [[03-Dominios/IA/Claude Code/Hooks e Guardrails/01 - Sistema de hooks|01 - Sistema de hooks]] — guardrails para headless seguro
- [[03-Dominios/IA/Claude Code/Time e Automação/index|Time e Automação]] — índice do galho
