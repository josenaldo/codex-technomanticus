---
title: "PreToolUse — interceptar e validar antes de executar"
type: concept
progress: done
publish: true
created: 2026-05-13
updated: 2026-07-07
status: growing
tags:
  - claude-code
  - hooks
  - pretooluse
  - guardrails
  - validacao
---

# PreToolUse — interceptar e validar antes de executar

> [!abstract] TL;DR
> PreToolUse é o hook que executa **antes** de qualquer tool call. É o ponto de controle principal do Claude Code: recebe o input que o agente quer usar, pode inspecionar, pode bloquear (exit ≠ 0), pode modificar (JSON no stdout). O agente recebe o resultado do hook e decide como proceder. É onde guardrails, auditoria e aprovação humana são implementados — com semântica determinística, não com instruções em linguagem natural.

---

## A analogia: a portaria de segurança antes do datacenter

Imagine um datacenter com portaria de segurança. Cada engenheiro que tenta entrar — mesmo um sênior confiável — para na portaria: apresenta crachá, o sistema valida, e só então a catraca abre. A portaria não convence ninguém, não negocia, não aceita "mas é urgente" — é um processo mecânico. O engenheiro sabe disso, planeja considerando isso, e quando é bloqueado, busca outra rota.

O PreToolUse é essa portaria. Toda vez que o agente decide executar uma ação — rodar um comando Bash, editar um arquivo, buscar na web — o runtime para e executa o hook antes de liberar. O hook recebe o que o agente quer fazer, tem um segundo para inspecionar, e responde com: passa (exit 0) ou bloqueia (exit ≠ 0).

O que torna isso poderoso: o agente sabe que foi bloqueado. Recebe o stderr do hook como feedback e pode recalcular. Um hook bem escrito não é um muro cego — é um sinal que redireciona o agente.

---

## O mecanismo exato

Quando o agente decide executar uma tool call, o runtime:

```mermaid
sequenceDiagram
    participant Agent as Agente (modelo)
    participant Runtime as Runtime CC
    participant Hook as PreToolUse script
    participant Tool as Tool (Bash, Edit...)

    Agent->>Runtime: Tool call com input JSON
    Runtime->>Hook: stdin = JSON do input
    Note over Hook: Script inspeciona,<br>decide, responde

    alt exit 0
        Hook-->>Runtime: Aprovado (stdout opcional = input modificado)
        Runtime->>Tool: Executa com input (original ou modificado)
        Tool-->>Runtime: Output
        Runtime-->>Agent: Resultado da tool
    else exit ≠ 0
        Hook-->>Runtime: Bloqueado (stderr = motivo)
        Runtime-->>Agent: Erro: "hook bloqueou — [stderr]"
        Note over Agent: Recalcula e tenta<br>abordagem alternativa
    end
```

1. O runtime serializa o input como JSON e passa via **stdin** ao script
2. O script executa (lê stdin, inspeciona, decide)
3. **Exit 0:** tool executa (com input original ou modificado via stdout)
4. **Exit ≠ 0:** tool não executa; stderr é injetado no contexto do agente

O agente vê o stderr como mensagem de erro da tool call. Se o script escreve uma mensagem clara — "BLOQUEADO: force push não permitido neste projeto. Use --force-with-lease ou abra um PR" — o agente usa isso para escolher uma abordagem alternativa.

---

## Estrutura do input recebido pelo hook

O hook recebe via stdin um JSON com o nome da tool e todos os parâmetros que o agente quer usar:

### Bash

```json
{
  "tool_name": "Bash",
  "tool_input": {
    "command": "git push --force origin main",
    "description": "Push forçado para publicar refactor"
  }
}
```

### Edit

```json
{
  "tool_name": "Edit",
  "tool_input": {
    "file_path": "/projeto/src/config/database.ts",
    "old_string": "password: 'prod_secret_hardcoded'",
    "new_string": "password: process.env.DB_PASSWORD"
  }
}
```

### Write

```json
{
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/projeto/.env",
    "content": "DATABASE_URL=postgresql://user:senha@localhost/db"
  }
}
```

O hook tem acesso total ao que o agente quer fazer — caminho, conteúdo, argumentos. Essa é a base para todos os padrões: inspecionar o input e decidir com base nele.

---

## Variáveis de ambiente disponíveis

Além do stdin, o runtime injeta variáveis de ambiente úteis:

```bash
$CLAUDE_TOOL_NAME      # Nome da tool: "Bash", "Edit", "Write", etc.
$CLAUDE_TOOL_INPUT     # Input completo serializado como JSON string
$CLAUDE_SESSION_ID     # ID único da sessão atual
```

Você pode usar stdin (mais preciso, via `jq`) ou `$CLAUDE_TOOL_INPUT` (mais conveniente para scripts simples):

```bash
#!/bin/bash
# Via stdin (recomendado para parsing preciso)
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // ""')

# Via variável de ambiente (útil para verificações rápidas)
if echo "$CLAUDE_TOOL_INPUT" | grep -q "push --force"; then
  echo "BLOQUEADO." >&2
  exit 1
fi
```

---

## Semântica dos exit codes

| Exit code | Significado | Resultado |
|-----------|-------------|-----------|
| `0` | Aprovado | Tool executa normalmente |
| `1` | Bloqueado | Tool não executa; stderr vai ao agente |
| `2+` | Bloqueado | Mesmo comportamento que exit 1 |
| Script falha a executar | Erro de hook | Tool pode executar dependendo da config |

O padrão mais simples e robusto: `exit 0` para aprovação, `exit 1` para bloqueio. Qualquer exit code diferente de zero bloqueia. A mensagem no stderr é o canal de feedback ao agente.

---

## Padrão 1 — Bloqueio simples (exit 1)

O hook mais direto: verifica padrão, bloqueia com mensagem clara.

```bash
#!/bin/bash
# hooks/block-force-push.sh

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // ""')

if echo "$COMMAND" | grep -qE "push --force|push -f"; then
  echo "BLOQUEADO: force push não permitido neste projeto." >&2
  echo "Alternativa: use --force-with-lease para push seguro, ou abra um PR." >&2
  exit 1
fi

exit 0
```

Configuração em `settings.json`:
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

A mensagem no `>&2` vai para o stderr — esse texto aparece no contexto do agente como feedback do bloqueio. Escreva mensagens que expliquem o porquê e sugiram a alternativa correta.

---

## Padrão 2 — Proteção de arquivos sensíveis

Impedir edição de arquivos que jamais devem ser modificados pelo agente:

```bash
#!/bin/bash
# hooks/protect-sensitive-files.sh

INPUT=$(cat)
FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path // ""')

PROTECTED_PATTERNS=(
  ".*\.env$"
  ".*\.env\..*"
  ".*credentials.*"
  ".*\.pem$"
  ".*\.key$"
  ".*secrets\.(json|yaml|yml)$"
  ".*/\.ssh/.*"
)

for pattern in "${PROTECTED_PATTERNS[@]}"; do
  if echo "$FILE" | grep -qE "$pattern"; then
    echo "BLOQUEADO: '$FILE' é um arquivo protegido." >&2
    echo "Edite manualmente — o agente não tem permissão para modificar arquivos de credencial." >&2
    exit 1
  fi
done

exit 0
```

Esse hook deve ser configurado para tanto `Edit` quanto `Write`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit",
        "hooks": [{ "type": "command", "command": "~/.claude/hooks/protect-sensitive-files.sh" }]
      },
      {
        "matcher": "Write",
        "hooks": [{ "type": "command", "command": "~/.claude/hooks/protect-sensitive-files.sh" }]
      }
    ]
  }
}
```

---

## Padrão 3 — Auditoria sem bloqueio

Hook que apenas registra — não bloqueia, só cria trilha de auditoria:

```bash
#!/bin/bash
# hooks/audit-log.sh

INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.tool_name')
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // .tool_input.file_path // "(sem argumento principal)"')
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
SESSION_ID="${CLAUDE_SESSION_ID:-unknown}"

# Registra no log de auditoria
echo "$TIMESTAMP | $SESSION_ID | $TOOL | $COMMAND" >> ~/.claude/audit.log

# Sempre exit 0 — não bloqueia, só registra
exit 0
```

O arquivo `~/.claude/audit.log` acumula todas as tool calls de todas as sessões. Útil para:
- Debugging de sessões longas ("o que o agente fez afinal?")
- Compliance ("liste todas as ações do agente neste sprint")
- Diagnóstico de comportamento inesperado

> [!tip] Combinar auditoria com bloqueio
> Configure múltiplos hooks — o de auditoria roda primeiro (exit 0, só loga), depois o de bloqueio roda em seguida. Assim todas as tentativas são registradas, incluindo as bloqueadas.

---

## Padrão 4 — Aprovação humana interativa

Para comandos de alto risco, exigir aprovação explícita antes de executar — a decisão de *quando*
vale a pena pagar esse custo de fricção é a mesma discutida em
[[03-Dominios/Tecnologia/IA/Agentes de Codificação/17 - Human-in-the-loop — quando (não) confiar|Human-in-the-loop — quando (não) confiar]]:
nem toda ação merece parar o agente e esperar um humano, mas as de alto risco (deleção, push,
infraestrutura) geralmente merecem.

```bash
#!/bin/bash
# hooks/require-approval.sh

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // ""')

HIGH_RISK_PATTERNS=(
  "rm -rf"
  "DROP TABLE"
  "DELETE FROM"
  "TRUNCATE"
  "git push"
  "kubectl delete"
  "terraform destroy"
)

for pattern in "${HIGH_RISK_PATTERNS[@]}"; do
  if echo "$COMMAND" | grep -qi "$pattern"; then
    echo "" >&2
    echo "APROVAÇÃO NECESSÁRIA" >&2
    echo "Comando: $COMMAND" >&2
    echo "Confirma? (s/N): " >&2
    read -r response < /dev/tty
    if [[ ! "$response" =~ ^[Ss]$ ]]; then
      echo "Cancelado pelo usuário." >&2
      exit 1
    fi
    echo "Aprovado pelo usuário." >&2
    break
  fi
done

exit 0
```

> [!warning] Aprovação interativa só funciona em sessão interativa
> Em modo headless (`--print`, CI/CD, MCP server), não há terminal para leitura. O `read < /dev/tty` vai falhar silenciosamente ou bloquear para sempre. Para headless: use bloqueio direto (`exit 1`) em vez de aprovação interativa. Ou detecte o modo e adapte:
> ```bash
> if [ -t 0 ]; then
>   read -r response < /dev/tty
> else
>   echo "Modo headless: bloqueando por segurança." >&2
>   exit 1
> fi
> ```

---

## Padrão 5 — Modificação de input

O hook pode modificar o input antes de executar, retornando JSON estruturado via stdout:

```bash
#!/bin/bash
# hooks/force-interactive-rm.sh

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // ""')

# Adiciona -i (interactive) em todo rm que não tem -i nem -rf
if echo "$COMMAND" | grep -qE "^rm " && ! echo "$COMMAND" | grep -q " -[ri]"; then
  SAFE_COMMAND=$(echo "$COMMAND" | sed 's/^rm /rm -i /')
  # Retorna JSON estruturado para modificar o input
  echo "{\"decision\": \"approve\", \"modified_input\": {\"command\": \"$SAFE_COMMAND\"}}"
  exit 0
fi

exit 0
```

Quando o stdout contém JSON estruturado com `"decision": "approve"` e `"modified_input"`, o runtime usa o input modificado ao chamar a tool. O agente não sabe que o input foi alterado — executa com o comando já sanitizado.

Estrutura do JSON de resposta:

```json
{
  "decision": "approve",
  "modified_input": {
    "command": "rm -i arquivo.txt"
  }
}
```

Ou para bloquear com JSON:

```json
{
  "decision": "block",
  "reason": "Comando rm -rf em diretório protegido /var/www"
}
```

---

## Padrão 6 — Delegação a outro LLM

Para validações que requerem raciocínio contextual — quando a decisão não é um pattern simples, mas uma questão de "esse comando faz sentido dado o projeto?":

```bash
#!/bin/bash
# hooks/llm-security-review.sh

INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.tool_name')
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // ""')

# Só delega se for Bash e o comando for não trivial
if [ "$TOOL" != "Bash" ] || [ -z "$COMMAND" ]; then
  exit 0
fi

# Delegar a decisão a outro Claude
DECISION=$(echo "$COMMAND" | claude --print \
  "Você é um revisor de segurança para um servidor de produção Linux.
   Este comando bash é seguro para executar?
   Responda apenas: SAFE ou UNSAFE: <motivo em uma linha>" \
  --max-tokens 60 2>/dev/null)

if echo "$DECISION" | grep -q "^UNSAFE"; then
  MOTIVO=$(echo "$DECISION" | sed 's/^UNSAFE: //')
  echo "Revisão de segurança (LLM): $MOTIVO" >&2
  exit 1
fi

exit 0
```

Ver [[03-Dominios/Tecnologia/IA/Claude Code/Hooks e Guardrails/06 - Delegar permissão|06 - Delegar permissão]] para o padrão completo com meta-agente e controle de timeout.

---

## Múltiplos hooks em sequência

Quando há múltiplos hooks configurados para o mesmo matcher, todos executam em sequência. O primeiro a retornar exit ≠ 0 interrompe a cadeia — a tool não executa.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": "~/.claude/hooks/audit-log.sh" },
          { "type": "command", "command": "~/.claude/hooks/block-force-push.sh" },
          { "type": "command", "command": "~/.claude/hooks/block-sudo.sh" }
        ]
      },
      {
        "matcher": "Edit",
        "hooks": [
          { "type": "command", "command": "~/.claude/hooks/audit-log.sh" },
          { "type": "command", "command": "~/.claude/hooks/protect-sensitive-files.sh" }
        ]
      }
    ]
  }
}
```

Ordem de execução: `audit-log.sh` → `block-force-push.sh` → `block-sudo.sh`. Se o primeiro bloqueia, os demais não rodam. Coloque auditoria primeiro (sempre exit 0) para garantir que todas as tentativas sejam registradas.

---

## Casos práticos

Regra e código isolado convencem em teoria. Na prática, o que separa um hook de brinquedo de um
hook de produção é ver como ele se comporta dentro do fluxo real de um time — com pressão de prazo,
pipeline de CI e gente tentando contornar a portaria.

### Cenário 1 — guardrails PCI-DSS (bloqueio de dados de cartão)

Um time com processamento de pagamentos configurou:

```bash
#!/bin/bash
# hooks/check-pci-patterns.sh
# Bloqueia edições que introduzem padrões de PAN ou CVV em código

INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.tool_name')
NEW_CONTENT=""

case "$TOOL" in
  "Edit")
    NEW_CONTENT=$(echo "$INPUT" | jq -r '.tool_input.new_string // ""')
    ;;
  "Write")
    NEW_CONTENT=$(echo "$INPUT" | jq -r '.tool_input.content // ""')
    ;;
  *)
    exit 0
    ;;
esac

# Padrão de PAN: 13-19 dígitos em formato de cartão
if echo "$NEW_CONTENT" | grep -qE '[0-9]{4}[- ]?[0-9]{4}[- ]?[0-9]{4}[- ]?[0-9]{4}'; then
  echo "BLOQUEADO: possível número de cartão (PAN) detectado no código." >&2
  echo "Dados de cartão nunca devem aparecer em código-fonte. Use tokenização." >&2
  exit 1
fi

# CVV: 3-4 dígitos após padrão "cvv", "cvc", "security_code"
if echo "$NEW_CONTENT" | grep -qiE '(cvv|cvc|security.?code)["\s:=]+[0-9]{3,4}'; then
  echo "BLOQUEADO: possível CVV detectado no código." >&2
  exit 1
fi

exit 0
```

Configurado para `Edit` e `Write`. O agente jamais consegue persistir dados de cartão em código —
mesmo que tente, o hook bloqueia antes.

### Cenário 2 — bloqueio condicional de `kubectl delete` em cluster de produção

Por que não bastava um `deny` fixo pra `kubectl delete`? Porque o time precisava deletar pods em
staging o dia inteiro — só o cluster de produção era intocável. Um `deny` categórico teria travado
o próprio trabalho legítimo; a regra precisava enxergar *qual* cluster estava no contexto atual.

```bash
#!/bin/bash
# hooks/protect-prod-cluster.sh
# Bloqueia comandos destrutivos do kubectl quando o contexto atual aponta pra produção

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // ""')

CURRENT_CONTEXT=$(kubectl config current-context 2>/dev/null)

if echo "$COMMAND" | grep -qE '^kubectl (delete|drain|cordon)'; then
  if echo "$CURRENT_CONTEXT" | grep -q "prod"; then
    echo "BLOQUEADO: comando destrutivo do kubectl em contexto de PRODUÇÃO ($CURRENT_CONTEXT)." >&2
    echo "Troque para o contexto de staging, ou peça aprovação humana explícita." >&2
    exit 1
  fi
fi

exit 0
```

O detalhe que separa esse hook de um bloqueio ingênuo: ele não olha só o *comando*, olha o
*contexto de execução* (`kubectl config current-context`) — a mesma linha de comando é segura em
staging e perigosa em produção. Isso é o que a lente de "condição verificada" do diagrama de fluxo
(mais abaixo) realmente significa na prática: a decisão depende do estado do mundo, não só do texto
do comando.

> [!summary] Os dois cenários mostram os dois modos do PreToolUse
> PCI-DSS bloqueia por **conteúdo** (o que está sendo escrito). O cluster de produção bloqueia por
> **contexto** (onde/quando o comando roda). A maioria dos hooks de produção combina os dois.

---

## Armadilhas comuns

Três formas de escrever um hook que *parece* correto no teste manual e falha justamente quando
mais importa — em produção, sob carga, ou meses depois de quem o escreveu ter saído do time.

> [!warning] Aprovação interativa só funciona em sessão interativa
> Como visto no Padrão 4: em modo headless (`--print`, CI/CD, MCP server) não há terminal para
> leitura. O `read < /dev/tty` falha silenciosamente ou bloqueia para sempre — e "bloquear para
> sempre" aqui não é metáfora, é o hook (e o agente) travados esperando um humano que nunca vai
> digitar nada naquele pipeline. Detecte o modo (`if [ -t 0 ]`) e caia para bloqueio direto quando
> não houver TTY.

> [!warning] Hook sem timeout trava o agente indefinidamente
> O runtime espera o hook terminar antes de liberar (ou não) a tool call. Se o script faz uma
> chamada de rede que nunca retorna — uma API de terceiros fora do ar, um `curl` sem `--max-time`,
> um `read` esquecido — o agente fica pendurado esperando um veredito que nunca chega. A pergunta
> que separa o hook amador do de produção: "o que acontece se a chamada externa deste hook nunca
> responder?" Sempre defina timeout explícito (`curl --max-time 5`, `timeout 10s ./script.sh`) e
> decida o *fail mode*: falhar aberto (deixa passar) ou fechado (bloqueia) quando o timeout estoura.

> [!warning] Exit code mal interpretado
> A tabela de exit codes parece trivial até o script ter um bug silencioso: um `grep` que não
> encontra padrão retorna exit 1 *mesmo dentro de um script que pretendia dizer "aprovado"* — se
> esse `grep` for a última linha do arquivo, o exit code dele vaza como o exit code do hook inteiro,
> e o comando é bloqueado por acidente. Ou o inverso: uma exceção não tratada em Python que retorna
> exit 0 por padrão do interpretador, aprovando silenciosamente um comando que deveria ter sido
> barrado. Termine hooks sempre com um `exit 0`/`exit 1` explícito na última linha — nunca deixe o
> exit code "vazar" do último comando executado dentro do script.

---

## Fluxo de decisão do hook PreToolUse

```mermaid
flowchart TD
    Receive["Hook recebe JSON via stdin"]
    Parse["Parse: tool_name + tool_input"]
    Check{"Condição verificada\n(padrão, arquivo, conteúdo)"}
    Block["exit 1\nstderr = motivo"]
    Modify{"Precisa modificar\no input?"}
    ReturnJSON["stdout = JSON com modified_input\nexit 0"]
    Approve["exit 0\n(sem stdout)"]

    Receive --> Parse --> Check
    Check -- "condição perigosa" --> Block
    Check -- "ok" --> Modify
    Modify -- "sim" --> ReturnJSON
    Modify -- "não" --> Approve

    style Block fill:#c0392b,color:#fff
    style Approve fill:#27ae60,color:#fff
    style ReturnJSON fill:#2980b9,color:#fff
```

---

## Quando usar PreToolUse vs. allow/deny

| Cenário | Use |
|---------|-----|
| Bloquear categoricamente (ex: nunca `git push --force`) | `deny` em settings.json |
| Bloquear condicionalmente (ex: `rm -rf` apenas fora de `/tmp`) | Hook PreToolUse |
| Pedir aprovação humana antes de ação crítica | Hook PreToolUse |
| Logar todas as ações para auditoria | Hook PreToolUse |
| Modificar input antes de executar | Hook PreToolUse |
| Validar conteúdo que o agente vai escrever | Hook PreToolUse |
| Delegar decisão a outro modelo | Hook PreToolUse |

`deny` é mais simples e mais rápido para bloqueios incondicionais. Hooks são necessários quando a lógica é condicional, quando você precisa de feedback rico ao agente, ou quando quer fazer mais do que apenas bloquear.

---

## Checklist — PreToolUse

- [ ] Scripts são executáveis: `chmod +x hooks/*.sh`
- [ ] Testados isoladamente: `echo '{"tool_name":"Bash","tool_input":{"command":"git push --force"}}' | ./hooks/block-force-push.sh`
- [ ] Mensagens no `>&2` são claras e sugerem alternativas
- [ ] Exit 0 em todos os caminhos de aprovação
- [ ] Scripts têm timeout implícito (hooks que travam bloqueiam o agente)
- [ ] Auditoria configurada como primeiro hook na cadeia
- [ ] Aprovação interativa tem fallback para modo headless

---

## Como explicar em inglês

| Português | Inglês |
|-----------|--------|
| Hook de pré-execução | PreToolUse hook |
| Interceptar | Intercept |
| Bloquear a tool call | Block the tool call / veto the action |
| Modificar o input | Modify the input / rewrite the input |
| Feedback ao agente | Feedback to the agent |
| Modo headless | Headless mode / non-interactive mode |

**Frases úteis:**
- "PreToolUse hooks intercept every tool call before it runs — you inspect the input, and either approve (exit 0), block (exit 1 with a reason in stderr), or modify the input before execution."
- "The stderr from a blocking hook is injected into the agent's context as an error message — a good hook gives the agent enough information to try a different approach."
- "Unlike CLAUDE.md instructions, which the model may interpret flexibly, PreToolUse hooks are deterministic: a matching exit code blocks unconditionally, no matter how much the model 'wants' to proceed."

> [!tip] Pra ver os 9 eventos de hook em ação, lado a lado
> [Claude Code — Hooks Deep Dive: All 9 Events & Practical Examples](https://www.youtube.com/watch?v=UcBCLFsPXBk) percorre todo o ciclo de vida de hooks do Claude Code — não só PreToolUse — com exemplos práticos de cada evento configurado e rodando. Bom complemento visual pra fixar onde PreToolUse se encaixa entre os outros 8 eventos do lifecycle.

---

## O que vem a seguir

PreToolUse resolve a pergunta "devo deixar isso acontecer?" — mas responde ela só **antes** da tool
rodar. Depois que o comando executa, que o arquivo é escrito, que o commit é feito, surge uma
pergunta diferente: "o que eu faço agora que já aconteceu?" Rodar o linter automaticamente depois de
um `Edit`, disparar uma notificação depois de um comando demorado, registrar o resultado real (não
só a intenção) de uma tool call — isso é território do hook seguinte no lifecycle.

Veja [[03-Dominios/Tecnologia/IA/Claude Code/Hooks e Guardrails/03 - PostToolUse|03 - PostToolUse]]
para a contraparte reativa do PreToolUse: o hook que roda depois da execução, com acesso ao
resultado real da tool, não apenas à intenção do agente.

---

## Veja também

- [[03-Dominios/Tecnologia/IA/Claude Code/Hooks e Guardrails/01 - Sistema de hooks|01 - Sistema de hooks]] — lifecycle e configuração geral
- [[03-Dominios/Tecnologia/IA/Claude Code/Hooks e Guardrails/03 - PostToolUse|03 - PostToolUse]] — reações pós-execução
- [[03-Dominios/Tecnologia/IA/Claude Code/Hooks e Guardrails/05 - Guardrails|05 - Guardrails]] — conjunto completo de guardrails recomendados
- [[03-Dominios/Tecnologia/IA/Claude Code/Hooks e Guardrails/06 - Delegar permissão|06 - Delegar permissão]] — meta-agente para validação com LLM
- [[03-Dominios/Tecnologia/IA/Claude Code/Hooks e Guardrails/07 - Segurança com hooks|07 - Segurança com hooks]] — hardening do próprio hook
- [[03-Dominios/Tecnologia/IA/Claude Code/Hooks e Guardrails/08 - Testando hooks|08 - Testando hooks]] — como testar e debugar hooks
- [[03-Dominios/Tecnologia/IA/Claude Code/Hooks e Guardrails/index|Hooks e Guardrails]] — índice do galho

---

## Fontes

- **Anthropic** — *Claude Code hooks* (2026). Documentação oficial do PreToolUse e semântica de exit codes — https://docs.anthropic.com/pt/docs/claude-code/hooks
- **Anthropic** — *Claude Code security* (2026). Uso de hooks para guardrails e auditoria de segurança — https://docs.anthropic.com/pt/docs/claude-code/security
- **Anthropic** — *Claude Code best practices* (2026). Padrões de hooks recomendados para projetos de produção — https://www.anthropic.com/engineering/claude-code-best-practices
