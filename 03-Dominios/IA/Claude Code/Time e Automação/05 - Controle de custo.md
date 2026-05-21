---
title: "Controle de custo — monitoramento, limites, ccusage"
type: concept
publish: true
created: 2026-05-13
updated: 2026-05-13
status: seedling
tags:
  - claude-code
  - custo
  - tokens
  - monitoramento
  - ccusage
---

# Controle de custo — monitoramento, limites, ccusage

> [!abstract] TL;DR
> Cada invocação de Claude Code consome tokens — e tokens custam dinheiro. Sem visibilidade, o custo cresce silenciosamente até surpreender no final do mês. A ferramenta `ccusage` agrega o uso por projeto e sessão. Para automações em CI/CD, `--max-turns` e `timeout` são os controles primários. Para o time, o custo por PR pode ser previsto e gerenciado com prompts e contexto bem dimensionados.

## Como o custo se acumula

Cada chamada ao modelo cobra tokens de input (prompt + histórico + contexto de ferramentas) e output (resposta gerada). Em Claude Code:

- **Sessão interativa**: cada mensagem acrescenta ao histórico — conversas longas ficam caras exponencialmente
- **Headless**: custo por invocação é mais previsível, mas invocações em loop somam rápido
- **Tool calls**: cada tool call que retorna resultado grande (ex.: `cat` de arquivo longo) infla o input da próxima mensagem
- **Cache**: o modelo mantém cache de contexto — re-invocar dentro de 5 minutos reusa partes do contexto e reduz custo

## ccusage — visualizando o consumo

`ccusage` é uma CLI que lê os logs locais do Claude Code e agrega o uso:

```bash
# Instalar
npm install -g ccusage

# Uso por sessão
ccusage

# Uso por projeto (últimos 7 dias)
ccusage --days 7

# Breakdown por data
ccusage --daily

# Custo total do mês
ccusage --month
```

Exemplo de saída:

```
Project: /home/user/repos/meu-projeto
Sessions: 23
Total tokens: 1,234,567 (input: 987,654, output: 246,913)
Estimated cost: $4.23

Top sessions by cost:
  2026-05-12 15:32 — $1.12 (auth refactor)
  2026-05-11 09:15 — $0.87 (test coverage)
  2026-05-10 14:45 — $0.65 (debug payment flow)
```

## Fatores de custo e como controlar

### Contexto grande

Passar arquivos inteiros quando só um trecho é necessário:

```bash
# Caro: passa o arquivo inteiro
cat src/auth/session.ts | claude -p "Qual função valida o token?"

# Barato: passa só o que é relevante
grep -n "validate\|token" src/auth/session.ts | claude -p "Qual função valida o token?"
```

### Histórico acumulado em sessões longas

Em sessões interativas, o histórico cresce a cada mensagem. Estratégias:

- Abrir nova sessão para tarefas sem relação com a anterior
- Usar `/clear` para limpar o histórico quando mudar de contexto
- Para automações, prefira `claude -p` (sem histórico) a sessões longas

### Tool calls desnecessárias

O agente pode chamar várias tools antes de responder. `--max-turns` limita isso:

```bash
# Sem limite — pode fazer 20 tool calls para uma tarefa simples
claude -p "Revise o arquivo auth.ts"

# Com limite — 3 tool calls máximo
claude -p --max-turns 3 "Revise o arquivo auth.ts"
```

### CI/CD sem controle

Em GitHub Actions, cada PR pode disparar análise. Com 50 PRs por dia, o custo pode escalar rapidamente. Controles:

```yaml
# Só roda em PRs com mais de 5 arquivos alterados
- name: Check PR size
  id: pr-size
  run: |
    SIZE=$(git diff --name-only origin/main...HEAD | wc -l)
    echo "size=$SIZE" >> $GITHUB_OUTPUT

- name: Claude analysis
  if: steps.pr-size.outputs.size > 5
  run: |
    claude --print --max-turns 5 "..."
```

## Estimativas de custo

Valores aproximados baseados nos preços atuais de Claude Sonnet (podem variar):

| Tarefa | Tokens típicos | Custo aproximado |
|--------|----------------|-----------------|
| Review de função (50 linhas) | 5k tokens | ~$0.02 |
| Review de PR (200 linhas de diff) | 20k tokens | ~$0.08 |
| Análise de arquivo grande (500 linhas) | 50k tokens | ~$0.20 |
| Sessão de refatoração (30 min) | 200k tokens | ~$0.80 |
| Pipeline CI completo | 100k tokens | ~$0.40 |

> [!warning]
> Estes valores mudam conforme preços da Anthropic e o modelo usado. Verifique sempre a [página de preços](https://anthropic.com/pricing) e meça com `ccusage` no seu projeto real.

## Configurar limite de gasto

A Anthropic permite configurar limites de gasto na conta ou por chave de API no console:

1. **Limite mensal**: alerta por email quando aproximar do limite
2. **Hard cap**: bloqueia chamadas acima do limite — útil para evitar surpresas em CI/CD

Para times, criar API keys separadas por projeto ou equipe permite monitorar custo por unidade.

## Otimizações de prompt

Prompts bem calibrados reduzem tokens sem perder qualidade:

```bash
# Verboso — o agente vai produzir output longo
claude -p "Analise este código, identifique todos os problemas, explique cada um em detalhe, e sugira como corrigi-los com exemplos"

# Calibrado — mesmo resultado, menos tokens
claude -p "Liste problemas neste código. Formato: [TIPO] linha N: descrição. Máximo 5 itens."
```

Instruções de formato reduzem output desnecessário. `--max-turns` reduz tool calls. Contexto filtrado reduz input.

## Dashboard de custo por time

Para visibilidade organizacional, o custo pode ser centralizado:

```bash
# Script para agregar ccusage de múltiplos devs
# (requer acesso aos logs de cada máquina ou uso de API key compartilhada)

for dev in alice bob carol; do
  ssh "$dev" "ccusage --month --json" >> /tmp/usage.json
done

cat /tmp/usage.json | jq '.[] | [.project, .cost] | @tsv' | sort -k2 -rn
```

Se o time usa API keys individuais, a Anthropic Console mostra uso agregado por organização.

## Armadilhas

**Ignorar o custo até o bill chegar**: o custo de tokens é invisível durante o trabalho. `ccusage --daily` no início do dia por uma semana calibra a intuição sobre o que custa o quê.

**Automações sem `--max-turns`**: um agente sem limite pode fazer 30 tool calls numa análise que precisava de 3. Em pipelines que rodam dezenas de vezes por dia, esse multiplicador importa.

**Sessão interativa para tarefas repetitivas**: se você repete a mesma análise toda manhã, escreva um script com `claude -p` ao invés de fazer a mesma sessão interativa — o resultado é mais previsível e o custo é mensurável.

**Cache frio em CI**: se o job de CI roda o agente esporadicamente, cada chamada começa sem cache. Agrupar análises em uma só invocação (em vez de múltiplas invocações por arquivo) pode ser mais eficiente.

## Veja também

- [[03-Dominios/IA/Claude Code/Time e Automação/01 - Headless mode|01 - Headless mode]] — `--max-turns` e controles de execução
- [[03-Dominios/IA/Claude Code/Time e Automação/02 - CI-CD com GitHub Actions|02 - CI/CD com GitHub Actions]] — limitação de custo em pipelines
- [[03-Dominios/IA/Claude Code/Time e Automação/03 - Dispatch via claude -p|03 - Dispatch via `claude -p`]] — timeout e retry
- [[03-Dominios/IA/Claude Code/Time e Automação/index|Time e Automação]] — índice do galho
