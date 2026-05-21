---
title: "Tool use — como o agente usa ferramentas"
type: concept
publish: true
created: 2026-05-13
updated: 2026-05-13
status: seedling
tags:
  - claude-code
  - mental-model
  - tool-use
---
# Tool use — como o agente usa ferramentas

> [!abstract] TL;DR
> Tools são a interface entre Claude Code e o mundo: ler arquivos, editá-los, executar comandos, buscar na web. Cada tool call segue o protocolo: parâmetros JSON → execução → output de volta ao modelo. O Bash é o mais poderoso (e perigoso). Read+Edit é mais seguro que Write para modificações. O sistema de permissões controla quais tools o agente pode usar sem confirmação.

## O que é

Claude Code não tem acesso direto ao sistema de arquivos ou ao shell — ele usa tools. Uma tool call é: o modelo decide que precisa de informação ou quer executar uma ação, gera um bloco JSON com o nome da tool e os parâmetros, o runtime executa, e retorna o output para o modelo.

## Tools principais

### Leitura e escrita de arquivos

| Tool | Uso | Quando usar |
|------|-----|-------------|
| `Read` | Lê arquivo ou range de linhas | Sempre preferir a `cat` via Bash |
| `Edit` | Substitui texto em arquivo existente | Modificações cirúrgicas |
| `Write` | Cria ou sobrescreve arquivo inteiro | Arquivos novos |

**Edit vs Write**: `Edit` requer que o arquivo exista e faz uma substituição precisa. É mais seguro porque não apaga o que não foi especificado. `Write` sobrescreve tudo — útil para arquivos novos, perigoso para arquivos existentes.

### Navegação

| Tool | Uso |
|------|-----|
| `LS` | Lista diretório |
| `Glob` | Encontra arquivos por padrão (`src/**/*.ts`) |
| `Grep` | Busca conteúdo em arquivos |

### Execução

| Tool | Uso | Risco |
|------|-----|-------|
| `Bash` | Executa comando shell | Alto — pode fazer qualquer coisa |

O `Bash` é onipotente. Com ele o agente pode rodar testes, instalar pacotes, chamar APIs, deletar arquivos. O sistema de permissões e hooks existe em grande parte para controlar o `Bash`.

### Composição e web

| Tool | Uso |
|------|-----|
| `Agent` | Despacha subagente com tarefa isolada |
| `WebFetch` | Fetch de URL |
| `WebSearch` | Busca na web |
| `TodoWrite` | Cria lista de tarefas para a sessão |

## O protocolo de tool call

Do ponto de vista do modelo, uma tool call é:

```
Modelo → [ToolUse: Read, {file_path: "src/auth.ts"}]
Runtime → [ToolResult: "...conteúdo do arquivo..."]
Modelo → [próxima decisão]
```

O output de cada tool call entra no contexto como um `ToolResult`. Isso significa que:
1. Outputs longos (arquivos grandes, bash verboso) consomem muitos tokens
2. O modelo vê o resultado antes de decidir o próximo passo
3. Erros de tool (arquivo não encontrado, permissão negada) também entram como ToolResult — o agente vê o erro e pode reagir

## Permissões

Algumas tools exigem confirmação antes de executar. O comportamento padrão:

| Tool | Permissão padrão |
|------|-----------------|
| `Read`, `Glob`, `Grep`, `LS` | Automática |
| `Edit`, `Write` | Pede confirmação na primeira vez por arquivo (modo interativo) |
| `Bash` | Pede confirmação para comandos novos |
| `WebFetch` | Automática |

Você pode configurar permissões via `.claude/settings.json`:

```json
{
  "permissions": {
    "allow": ["Bash(npm test)", "Bash(npm run lint)"],
    "deny": ["Bash(rm -rf*)"]
  }
}
```

## Na prática

### Vendo tool calls em tempo real

```bash
claude --verbose "add input validation to createUser"
```

Output mostrará cada tool call e resultado antes da resposta final.

### Preferindo Read a cat

O agente deve usar `Read` em vez de `Bash("cat arquivo")` porque:
- `Read` tem parâmetros `offset` e `limit` — lê apenas o trecho necessário
- `Bash("cat arquivo.ts")` lê o arquivo inteiro e coloca no contexto

Para um arquivo de 3000 linhas onde só as linhas 200-250 importam:

```
Bom:  Read("src/auth.ts", offset=200, limit=50)   → ~50 linhas no contexto
Ruim: Bash("cat src/auth.ts")                      → 3000 linhas no contexto
```

## Armadilhas

**Write em arquivo existente**: se o agente usar `Write` para modificar um arquivo existente, vai sobrescrever o conteúdo completo. Se o conteúdo gerado for incompleto, você perde o resto. Prefira `Edit` para modificações.

**Bash com output verboso**: `npm install` ou `docker build` podem gerar megabytes de output. Isso consome tokens e pode forçar compaction. Redirecione ou filtre quando possível.

**Bash como martelo**: o agente tende a usar `Bash` para coisas que teriam tools melhores (leitura de arquivo, busca). Isso é geralmente ineficiente — `Grep` é mais direcional que `Bash("grep -r pattern .")`.

**Encadeamento não supervisionado**: em modo headless ou com permissões muito permissivas, o agente pode executar sequências destrutivas sem oportunidade de intervenção.

## Veja também

- [[03-Dominios/IA/Claude Code/Mental Model/01 - O loop agentic|01 - O loop agentic]]
- [[03-Dominios/IA/Claude Code/Hooks e Guardrails/index|Hooks e Guardrails]] — controlar tool use via hooks
- [[03-Dominios/IA/Claude Code/Configuração/index|Configuração]] — settings.json e permissões
- [[03-Dominios/IA/Claude Code/Mental Model/index|Mental Model]] — índice do galho

## Referências

- [Claude Code — CLI reference](https://docs.anthropic.com/pt/docs/claude-code/cli-reference)
