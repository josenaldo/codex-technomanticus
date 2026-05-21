---
title: "Modos de operação — interativo, plan mode, auto mode, headless"
type: concept
publish: true
created: 2026-05-13
updated: 2026-05-13
status: seedling
tags:
  - claude-code
  - mental-model
  - modos
  - plan-mode
  - headless
---
# Modos de operação — interativo, plan mode, auto mode, headless

> [!abstract] TL;DR
> Claude Code tem quatro modos principais: interativo (REPL com confirmações), plan mode (planeja sem executar), auto mode (menos interrupções via configuração de permissões), e headless (não-interativo, ideal para CI/CD). Escolher o modo certo para a tarefa reduz fricção e risco.

## O que é

O modo de operação define como Claude Code equilibra autonomia e controle do usuário. Mais autonomia = menos interrupções mas mais risco. Mais controle = mais segurança mas mais fricção.

## Modo 1: Interativo (padrão)

```bash
claude
```

O modo REPL. Você digita, o agente responde e age. Confirmações aparecem para ações arriscadas (edições de arquivo, comandos Bash novos).

**Quando usar:** trabalho exploratório, tarefas novas, código desconhecido, aprendizado.

**Comportamento:** pede confirmação antes de:
- Editar um arquivo pela primeira vez na sessão
- Rodar comandos Bash não listados como permitidos
- Operações que poderiam ser destrutivas

## Modo 2: Plan Mode

```
# Dentro do REPL:
Shift+Tab    # toggle plan mode on/off
/plan        # ativa plan mode explicitamente
```

O agente **planeja mas não executa**. Mostra o que faria — quais arquivos editaria, quais comandos rodaria — sem tocar em nada. Você revisa e aprova antes de executar.

**Quando usar:** tarefas de refactoring grande, antes de dar autonomia ao agente, quando quer revisar a estratégia antes da implementação.

**Comportamento:**
- Gera um plano detalhado de ações
- Não faz tool calls destrutivas (Edit, Write, Bash)
- Pode fazer reads para informar o plano
- Após aprovação, você sai do plan mode e o agente executa

### Exemplo de uso

```
você: [Shift+Tab] ativar plan mode
você: refatora o módulo de autenticação para usar JWT

agente: [Plano]
1. Ler src/auth/session.ts e src/auth/middleware.ts
2. Instalar jsonwebtoken: npm install jsonwebtoken @types/jsonwebtoken
3. Modificar src/auth/session.ts: trocar cookie-session por jwt.sign/verify
4. Atualizar middleware.ts: verificar token no header Authorization
5. Atualizar testes em tests/auth.test.ts
6. Rodar npm test para validar

Deseja prosseguir? [y/n]
```

## Modo 3: Auto Mode

Reduz confirmações para ações listadas como permitidas no `settings.json`. Não é um modo ativado com um comando — é configuração de permissões.

```json
// .claude/settings.json
{
  "permissions": {
    "allow": [
      "Bash(npm test)",
      "Bash(npm run lint)",
      "Bash(npm run build)",
      "Edit(*)"
    ]
  }
}
```

Com essas permissões, o agente roda testes, lint, e build sem pedir confirmação. Edições de arquivo também são automáticas.

**Quando usar:** tarefas bem definidas em projetos conhecidos, pair programming acelerado, contexto onde você confia no agente.

**Risco:** o agente executa mais sem supervisão. Combine com hooks para guardrails.

## Modo 4: Headless

```bash
claude -p "adicione logs de entrada e saída em todos os endpoints" --output-format json
```

Não-interativo. Recebe a tarefa, executa, retorna o output. Sem prompts de confirmação, sem REPL.

**Quando usar:** scripts, CI/CD, automação, dispatch de subagentes, tasks programadas.

**Flags importantes:**

| Flag | Efeito |
|------|--------|
| `-p "prompt"` | Define a tarefa (headless mode) |
| `--output-format json` | Output estruturado para parsing |
| `--output-format stream-json` | Stream de eventos JSON |
| `--max-turns N` | Limita iterações |
| `--allowedTools "Edit,Bash"` | Restringe tools disponíveis |
| `--continue` | Continua a última sessão |
| `--resume SESSION_ID` | Retoma sessão específica |

### Exemplo em shell script

```bash
#!/bin/bash
RESULT=$(claude -p "run the test suite and report failures" \
  --output-format json \
  --max-turns 10)

echo "$RESULT" | jq '.result'
```

## Comparação rápida

| Modo | Confirmações | Interatividade | Caso de uso |
|------|-------------|----------------|-------------|
| Interativo | Sim, para ações novas | Total | Exploração, pair programming |
| Plan Mode | Aprova o plano inteiro | Revisão antes de executar | Refactoring grande |
| Auto Mode | Não (para permitidas) | Mínima | Tarefas repetitivas conhecidas |
| Headless | Não | Nenhuma | CI/CD, automação |

## Armadilhas

**Headless sem `--max-turns`**: o agente pode iterar indefinidamente em loops. Sempre defina um limite razoável para CI/CD.

**Auto Mode sem hooks**: sem guardrails, o agente pode executar sequências inesperadas. Combine com hooks PreToolUse para validar ações.

**Plan Mode não persiste**: o plano é no contexto da sessão. Se você fechar e reabrir, perde o plano.

**`-p` sem `--output-format json`**: em scripts, o output em texto livre é difícil de parsear. Use `--output-format json` em automação.

## Veja também

- [[03-Dominios/IA/Claude Code/Workflows/01 - Plan Mode|01 - Plan Mode]] — uso detalhado do plan mode
- [[03-Dominios/IA/Claude Code/Time e Automação/01 - Headless mode|01 - Headless mode]] — headless em profundidade
- [[03-Dominios/IA/Claude Code/Hooks e Guardrails/index|Hooks e Guardrails]] — guardrails para auto mode
- [[03-Dominios/IA/Claude Code/Mental Model/index|Mental Model]] — índice do galho

## Referências

- [Claude Code — CLI reference](https://docs.anthropic.com/pt/docs/claude-code/cli-reference)
