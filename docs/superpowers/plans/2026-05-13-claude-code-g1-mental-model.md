# Claude Code — Galho 1: Mental Model

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Criar as 8 notas atômicas do Galho 1 (Mental Model) da trilha Claude Code no vault Obsidian codex-technomanticus.

**Architecture:** Cada nota é um arquivo Markdown independente em `03-Dominios/IA/Claude Code/Mental Model/`. Segue o padrão de notas atômicas da trilha: frontmatter YAML, callout TL;DR, seções de conteúdo, "Veja também" com wikilinks, "Referências". Sem testes — verificação é checar que o arquivo existe e tem a estrutura esperada.

**Tech Stack:** Obsidian Flavored Markdown, frontmatter YAML, wikilinks `[[path|alias]]`, callouts `> [!type]`

---

## File Map

**Criar:**
- `03-Dominios/IA/Claude Code/Mental Model/01 - O loop agentic.md`
- `03-Dominios/IA/Claude Code/Mental Model/02 - Como Claude Code lê um codebase.md`
- `03-Dominios/IA/Claude Code/Mental Model/03 - Tool use.md`
- `03-Dominios/IA/Claude Code/Mental Model/04 - Context window.md`
- `03-Dominios/IA/Claude Code/Mental Model/05 - Modos de operação.md`
- `03-Dominios/IA/Claude Code/Mental Model/06 - Compaction.md`
- `03-Dominios/IA/Claude Code/Mental Model/07 - Tokens e custo.md`
- `03-Dominios/IA/Claude Code/Mental Model/08 - Como o agente decide.md`

---

## Task 1: Criar `01 - O loop agentic.md`

**Files:**
- Create: `03-Dominios/IA/Claude Code/Mental Model/01 - O loop agentic.md`

- [ ] **Step 1: Criar o arquivo**

```markdown
---
title: "O loop agentic — plan, act, observe, iterate"
type: concept
publish: true
created: 2026-05-13
updated: 2026-05-13
status: seedling
tags:
  - claude-code
  - mental-model
  - agentic-loop
---

# O loop agentic — plan, act, observe, iterate

> [!abstract] TL;DR
> Claude Code não é um chatbot que gera texto — é um agente que executa um loop: recebe uma tarefa, planeja o que fazer, executa uma ação (tool call), observa o resultado, e itera. O loop continua até a tarefa estar completa ou o agente pedir ajuda. Entender esse loop muda como você formula pedidos e diagnostica problemas.

## O que é

Um chatbot responde e para. Um agente responde e age — e continua agindo até concluir.

O loop agentic do Claude Code tem quatro fases:

| Fase | O que acontece |
|------|----------------|
| **Plan** | O agente lê a tarefa, o contexto (CLAUDE.md, histórico), e decide qual tool usar |
| **Act** | Executa uma tool call: Read, Edit, Bash, Grep, etc. |
| **Observe** | Lê o output da tool. O output entra no contexto. |
| **Iterate** | Com base no que observou, decide a próxima ação — ou conclui |

A cada iteração, o agente tem mais informação. É por isso que o Claude Code funciona bem em tarefas abertas: ele descobre o que precisa à medida que navega.

## Como funciona na prática

### Exemplo: "fix the failing test"

Tarefa: `fix the failing test in auth.test.ts`

Loop que acontece:
1. **Plan**: preciso ver o arquivo de teste e o código que ele testa
2. **Act**: `Read("src/auth.test.ts")`
3. **Observe**: vê o teste falhar em `validateToken` — expectativa errada no mock
4. **Plan**: preciso ver a implementação de `validateToken`
5. **Act**: `Grep("validateToken", "src/")`
6. **Observe**: encontra `src/auth.ts:47`
7. **Act**: `Read("src/auth.ts", offset=40, limit=30)`
8. **Observe**: vê que o retorno mudou de `{valid: true}` para `{isValid: true}`
9. **Plan**: o teste usa `valid`, precisa usar `isValid`
10. **Act**: `Edit("src/auth.test.ts", old="result.valid", new="result.isValid")`
11. **Observe**: edição aplicada
12. **Act**: `Bash("npm test src/auth.test.ts")`
13. **Observe**: teste passando ✓
14. **Conclude**: tarefa concluída

### Visualizando o loop

Use o flag `--verbose` para ver cada tool call:

```bash
claude --verbose "fix the failing test in auth.test.ts"
```

Você verá cada Read, Grep, Edit e Bash antes do output final.

### `--max-turns`

Por padrão, o agente pode fazer quantas iterações precisar. Para limitar (útil em CI/CD ou para prevenir loops):

```bash
claude -p "task" --max-turns 20
```

## Por que isso importa

**Formule tarefas, não instruções passo a passo.** O loop agentic significa que você pode dizer "adicione autenticação JWT ao endpoint /api/users" em vez de especificar cada arquivo. O agente descobre o que ler.

**O loop é determinístico dentro do contexto.** Se o agente travou ou tomou uma decisão errada, muitas vezes é porque faltou contexto — CLAUDE.md não menciona um padrão, ou a estrutura do projeto é incomum. Adicione contexto, não instruções.

**Iterações custam tokens.** Cada tool call e seu output entram no contexto. Uma sessão com 50 tool calls é muito mais cara que uma com 10. Pedidos mais focados = menos iterações = menor custo.

## Armadilhas

**Loop infinito aparente**: o agente parece não terminar. Causa: tarefa ambígua ou bloqueio não reportado. Diagnóstico: `--verbose`. Solução: reformule a tarefa ou pressione `Esc` para interromper.

**Suposições silenciosas**: o agente assumiu algo errado no passo 1 e nunca corrigiu. Causa: contexto insuficiente. Solução: CLAUDE.md com convenções do projeto.

**Corrida de edições**: o agente edita um arquivo baseado no que leu em loop anterior, mas o arquivo mudou no meio. Pouco comum em uso interativo, mas pode acontecer com subagents paralelos.

## Veja também

- [[03-Dominios/IA/Claude Code/Mental Model/02 - Como Claude Code lê um codebase|02 - Como Claude Code lê um codebase]]
- [[03-Dominios/IA/Claude Code/Mental Model/03 - Tool use|03 - Tool use]]
- [[03-Dominios/IA/Claude Code/Mental Model/04 - Context window|04 - Context window]]
- [[03-Dominios/IA/Claude Code/Mental Model/index|Mental Model]] — índice do galho

## Referências

- [Anthropic — Claude Code overview](https://docs.anthropic.com/pt/docs/claude-code/overview)
- [Anthropic — Agentic patterns](https://docs.anthropic.com/pt/docs/build-with-claude/agents)
```

- [ ] **Step 2: Verificar**

```bash
ls "03-Dominios/IA/Claude Code/Mental Model/"
```

Esperado: `01 - O loop agentic.md` na listagem.

- [ ] **Step 3: Commit**

```bash
git add "03-Dominios/IA/Claude Code/Mental Model/01 - O loop agentic.md"
git commit -m "feat(claude-code/g1): add 01 - O loop agentic"
```

---

## Task 2: Criar `02 - Como Claude Code lê um codebase.md`

**Files:**
- Create: `03-Dominios/IA/Claude Code/Mental Model/02 - Como Claude Code lê um codebase.md`

- [ ] **Step 1: Criar o arquivo**

```markdown
---
title: "Como Claude Code lê um codebase"
type: concept
publish: true
created: 2026-05-13
updated: 2026-05-13
status: seedling
tags:
  - claude-code
  - mental-model
  - codebase
  - context
---

# Como Claude Code lê um codebase

> [!abstract] TL;DR
> Claude Code não indexa o projeto como uma IDE. Ele navega sob demanda: usa Glob para encontrar arquivos, Grep para buscar símbolos, e Read para ler o que é relevante. O CLAUDE.md funciona como o "onboarding doc" que o agente lê primeiro. Sem CLAUDE.md, o agente descobre o projeto do zero a cada sessão — mais caro e mais lento.

## O que é

IDEs como VS Code ou IntelliJ mantêm um índice persistente do projeto: árvore de arquivos, referências de símbolos, call graph. Esse índice é construído uma vez e mantido atualizado em background.

Claude Code **não tem esse índice**. Cada sessão começa do zero. O agente constrói seu entendimento do projeto **incrementalmente**, usando tools para explorar o que é relevante para a tarefa atual.

Isso é uma escolha de design: o agente pode trabalhar em qualquer projeto sem configuração prévia, e o "índice" é sempre preciso (ele leu o arquivo agora, não há defasagem).

## Como funciona

### 1. Leitura do CLAUDE.md

O primeiro passo de cada sessão é ler os arquivos CLAUDE.md:
- `~/.claude/CLAUDE.md` — configuração global do usuário
- `CLAUDE.md` na raiz do projeto — contexto do projeto
- `CLAUDE.md` em subpastas — contexto específico de área

O CLAUDE.md é o "onboarding doc" que o agente lê antes de fazer qualquer outra coisa. É aqui que você documenta convenções, estrutura, comandos importantes e o que o agente deve ou não deve fazer.

### 2. Exploração sob demanda

Para a tarefa "adicione validação ao endpoint /users", o agente tipicamente:

```
LS("src/")                                       → encontra routes/, controllers/, middleware/
Glob("src/**/*.ts")                              → lista todos os arquivos TypeScript
Grep("router.get.*users", "src/routes/")         → encontra users.router.ts
Read("src/routes/users.router.ts")               → lê o arquivo relevante
```

### 3. Construção incremental do mapa

O agente não lê tudo — lê o mínimo necessário para a tarefa. Isso mantém o contexto enxuto e o custo baixo. À medida que descobre dependências (imports, referências), expande a leitura.

### Comparação: com vs sem CLAUDE.md

| Aspecto | Sem CLAUDE.md | Com CLAUDE.md |
|---------|--------------|---------------|
| Primeiros turnos | Explorando estrutura | Já sabe onde está o quê |
| Convenções | Infere pelo código | Documentado explicitamente |
| Comandos (lint, test, build) | Procura no package.json, Makefile | Listados no CLAUDE.md |
| Custo por sessão | Maior (mais exploração) | Menor |
| Consistência entre sessões | Menor | Maior |

## Por que isso importa

**CLAUDE.md é o maior multiplicador de produtividade.** Um CLAUDE.md bem escrito reduz a exploração inicial, previne erros de convenção, e faz cada sessão começar no nível certo de contexto.

**Pedidos vagos + sem CLAUDE.md = sessões longas.** O agente precisa descobrir tudo sozinho. Com projetos grandes isso significa muitos Greps e Reads antes de chegar ao trabalho real.

**O agente lê seletivamente.** Não assuma que ele "leu tudo". Se há uma convenção importante que o agente não deveria inferir, documente no CLAUDE.md.

## Armadilhas

**Repo muito grande sem CLAUDE.md**: o agente gasta os primeiros 10+ tool calls só entendendo a estrutura. Adicione um CLAUDE.md com a arquitetura em alto nível.

**Estrutura não convencional**: frameworks caseiros, monorepos atípicos, nomes de pastas não padrão confundem a exploração inicial. Documente no CLAUDE.md.

**CLAUDE.md desatualizado**: pior que não ter. Um CLAUDE.md que descreve estrutura antiga induz o agente a tomar decisões erradas. Trate como código — atualize quando a estrutura muda.

**Assumir que o agente "sabe" o projeto**: ele só sabe o que leu na sessão atual. Referências a arquivos não lidos precisam ser explícitas: "o arquivo de autenticação é src/auth/index.ts".

## Veja também

- [[03-Dominios/IA/Claude Code/Mental Model/01 - O loop agentic|01 - O loop agentic]]
- [[03-Dominios/IA/Claude Code/Mental Model/03 - Tool use|03 - Tool use]]
- [[03-Dominios/IA/Claude Code/Configuração/index|Configuração]] — CLAUDE.md em detalhes
- [[03-Dominios/IA/Claude Code/Mental Model/index|Mental Model]] — índice do galho

## Referências

- [Claude Code — CLAUDE.md](https://docs.anthropic.com/pt/docs/claude-code/memory)
```

- [ ] **Step 2: Verificar**

```bash
ls "03-Dominios/IA/Claude Code/Mental Model/"
```

Esperado: `02 - Como Claude Code lê um codebase.md` na listagem.

- [ ] **Step 3: Commit**

```bash
git add "03-Dominios/IA/Claude Code/Mental Model/02 - Como Claude Code lê um codebase.md"
git commit -m "feat(claude-code/g1): add 02 - Como Claude Code lê um codebase"
```

---

## Task 3: Criar `03 - Tool use.md`

**Files:**
- Create: `03-Dominios/IA/Claude Code/Mental Model/03 - Tool use.md`

- [ ] **Step 1: Criar o arquivo**

```markdown
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
```

- [ ] **Step 2: Verificar**

```bash
ls "03-Dominios/IA/Claude Code/Mental Model/"
```

Esperado: `03 - Tool use.md` na listagem.

- [ ] **Step 3: Commit**

```bash
git add "03-Dominios/IA/Claude Code/Mental Model/03 - Tool use.md"
git commit -m "feat(claude-code/g1): add 03 - Tool use"
```

---

## Task 4: Criar `04 - Context window.md`

**Files:**
- Create: `03-Dominios/IA/Claude Code/Mental Model/04 - Context window.md`

- [ ] **Step 1: Criar o arquivo**

```markdown
---
title: "Context window — o que entra, o que sai, por que isso importa"
type: concept
publish: true
created: 2026-05-13
updated: 2026-05-13
status: seedling
tags:
  - claude-code
  - mental-model
  - context-window
  - tokens
---

# Context window — o que entra, o que sai, por que isso importa

> [!abstract] TL;DR
> A context window é a memória de trabalho do Claude Code: tudo que o agente "sabe" em uma sessão está nela. Sistema prompt, CLAUDE.md, histórico de conversa, e todos os outputs de tool calls consomem tokens. Quando enche, o agente esquece ou o custo dispara. Gerenciar contexto é gerenciar a qualidade e custo das sessões.

## O que é

A context window é o espaço de tokens que o modelo processa em cada chamada à API. É finita (~200k tokens nos modelos Claude mais recentes). Tudo que está dentro dela é "visível" para o agente. O que está fora não existe para ele.

Em Claude Code, a context window acumula ao longo da sessão:

```
Chamada 1: [system prompt] + [CLAUDE.md] + [turn 1]
Chamada 2: [system prompt] + [CLAUDE.md] + [turn 1] + [tool result 1] + [turn 2]
Chamada 3: [system prompt] + [CLAUDE.md] + [turn 1] + [tool result 1] + [turn 2] + [tool result 2] + [turn 3]
```

Cada iteração do loop agentic adiciona mais tokens.

## O que entra no contexto

| Componente | Tokens típicos | Notas |
|------------|---------------|-------|
| System prompt (Claude Code) | ~2.000–5.000 | Fixo por sessão |
| CLAUDE.md global | Variável | Lido no início |
| CLAUDE.md do projeto | Variável | Lido no início |
| Mensagens do usuário | Variável | Cada turn |
| Respostas do modelo | Variável | Cada turn |
| Tool call outputs | **Maior variável** | Cresce com cada Read, Bash, Grep |

### O que mais consome contexto

**Leituras de arquivo grandes**: `Read("src/huge-service.ts")` num arquivo de 2000 linhas pode adicionar 40k+ tokens de uma vez.

**Bash com output verboso**: `npm ci`, `docker build`, compiladores — o stdout completo vai para o contexto.

**Grep com muitos resultados**: `Grep("import", "src/")` num projeto grande retorna centenas de linhas.

**Múltiplas iterações**: uma sessão de debugging com 30 tool calls pode facilmente passar de 100k tokens de contexto.

## Por que isso importa

### Custo

Input tokens = dinheiro. Em uma sessão que acumula 150k tokens de contexto e tem 20 turnos, você está pagando por ~150k tokens de input por chamada, em média. Gerenciar contexto reduz custo diretamente.

### Qualidade

Com contexto saturado (próximo do limite), o modelo começa a "perder" detalhes do início da sessão. Uma instrução dada no turn 1 pode ser esquecida no turn 40. Isso é [[03-Dominios/IA/Claude Code/Mental Model/06 - Compaction|compaction]] em ação — mas compaction tem custo de fidelidade.

### Velocidade

Janelas de contexto maiores = inferência mais lenta. Uma sessão de 180k tokens responde mais devagar que uma de 10k.

## Estratégias de gerenciamento

**Leituras cirúrgicas**: use `offset` e `limit` no Read para ler apenas o trecho necessário.

```
Ruim: Read("src/big-service.ts")                        → arquivo inteiro
Bom:  Read("src/big-service.ts", offset=150, limit=40)  → só o método relevante
```

**Redirecionamento de output**: para comandos verbosos, filtre antes que entrem no contexto.

```bash
npm ci 2>&1 | tail -5
```

**Compactação manual preventiva**: use `/compact` quando você nota que a sessão cresceu, antes de atingir o limite auto.

**Sessões focadas**: cada sessão = uma tarefa. Não use a mesma sessão para refactoring do módulo A e debugging do módulo B.

**`/resume` com consciência**: retomar uma sessão compactada significa começar com um resumo — pode ter perdido detalhes.

## Armadilhas

**Ler o arquivo inteiro "só para ter"**: um CLAUDE.md que aponta para os arquivos-chave reduz exploração desnecessária.

**Confundir sessão com persistência**: o agente não "lembra" de sessões anteriores. Cada `claude` novo começa do zero (exceto com `--resume`).

**Output de CI sem filtro**: integrar Claude Code em pipelines sem filtrar output de ferramentas pode explodir o contexto em segundos.

## Veja também

- [[03-Dominios/IA/Claude Code/Mental Model/06 - Compaction|06 - Compaction]]
- [[03-Dominios/IA/Claude Code/Mental Model/07 - Tokens e custo|07 - Tokens e custo]]
- [[03-Dominios/IA/Claude Code/Mental Model/03 - Tool use|03 - Tool use]]
- [[03-Dominios/IA/Claude Code/Mental Model/index|Mental Model]] — índice do galho

## Referências

- [Anthropic — Context windows](https://docs.anthropic.com/pt/docs/about-claude/models)
```

- [ ] **Step 2: Verificar**

```bash
ls "03-Dominios/IA/Claude Code/Mental Model/"
```

Esperado: `04 - Context window.md` na listagem.

- [ ] **Step 3: Commit**

```bash
git add "03-Dominios/IA/Claude Code/Mental Model/04 - Context window.md"
git commit -m "feat(claude-code/g1): add 04 - Context window"
```

---

## Task 5: Criar `05 - Modos de operação.md`

**Files:**
- Create: `03-Dominios/IA/Claude Code/Mental Model/05 - Modos de operação.md`

- [ ] **Step 1: Criar o arquivo**

```markdown
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
```

- [ ] **Step 2: Verificar**

```bash
ls "03-Dominios/IA/Claude Code/Mental Model/"
```

Esperado: `05 - Modos de operação.md` na listagem.

- [ ] **Step 3: Commit**

```bash
git add "03-Dominios/IA/Claude Code/Mental Model/05 - Modos de operação.md"
git commit -m "feat(claude-code/g1): add 05 - Modos de operação"
```

---

## Task 6: Criar `06 - Compaction.md`

**Files:**
- Create: `03-Dominios/IA/Claude Code/Mental Model/06 - Compaction.md`

- [ ] **Step 1: Criar o arquivo**

```markdown
---
title: "Compaction — como o Claude Code gerencia contextos longos"
type: concept
publish: true
created: 2026-05-13
updated: 2026-05-13
status: seedling
tags:
  - claude-code
  - mental-model
  - compaction
  - context
---

# Compaction — como o Claude Code gerencia contextos longos

> [!abstract] TL;DR
> Compaction é o mecanismo que permite continuar sessões quando a context window está quase cheia. O Claude Code resume o histórico de conversa em um snapshot denso, preservando informação essencial e descartando detalhes. Auto compaction acontece automaticamente; `/compact` permite triggerar manualmente com foco explícito. O custo: alguns detalhes são perdidos. A prática saudável é compactar cedo e reiniciar para tarefas não relacionadas.

## O que é

Quando a context window se aproxima do limite, o Claude Code pode compactar a sessão: em vez de ter o histórico completo de tool calls, mensagens e outputs, o contexto passa a ter um **summary** desse histórico seguido pelas mensagens mais recentes em forma completa.

```
Antes da compaction:
[system prompt] [CLAUDE.md] [turn1][tool1][turn2][tool2]...[turn25][tool25]

Depois da compaction:
[system prompt] [CLAUDE.md] [SUMMARY: resumo dos turns 1-20] [turn21][tool21]...[turn25][tool25]
```

## Auto compaction vs manual

### Auto compaction

Acontece automaticamente quando o contexto atinge ~80% da janela disponível. Você verá uma notificação:

```
[Conversation compacted to preserve context]
```

O Claude Code chama a API uma vez para gerar o summary, então continua a sessão com o contexto compactado.

### Manual: `/compact`

```
/compact
```

Trigga compaction quando você decide, independente do tamanho do contexto. Útil antes de entrar em uma fase nova da sessão.

Você pode passar um foco para o summary:

```
/compact Focus on the authentication changes made so far
```

Com foco, o summary prioriza o que você especificou ao resumir — muito mais útil que um summary genérico.

## O que é preservado vs descartado

**Preservado com fidelidade:**
- Decisões de design explícitas ("decidimos usar JWT em vez de sessions")
- Arquivos editados e suas mudanças
- Erros encontrados e como foram resolvidos
- Instruções explícitas do usuário
- Estado final dos trabalhos em andamento

**Comprimido ou descartado:**
- Tool outputs detalhados de chamadas antigas
- Explorações que não levaram a nada
- Conteúdo de arquivos lidos (o arquivo em si não muda — pode ser relido)
- Raciocínio intermediário de turns anteriores

## Por que isso importa

### Continuidade de sessão

Sem compaction, sessões longas travavam ou exigiam reinício. Com compaction, você pode trabalhar em uma feature por horas em uma única sessão.

### Custo

Após compaction, cada novo turn processa menos tokens (o summary é mais denso que o histórico completo). Custo por turn cai.

### Risco de perda de informação

O summary é uma aproximação. Detalhes específicos de turns antigos podem ser perdidos. Se você disse "não use lodash" no turn 3 e a sessão foi compactada duas vezes desde então, o agente pode não lembrar dessa restrição.

**Mitigação:** coloque restrições importantes no CLAUDE.md, não confie só no histórico da sessão.

## Estratégias práticas

### Compactar antes, não depois

```
/compact Focus on the API design decisions made so far
```

Compacte quando a sessão está ~50% do limite, não quando já está 90%. Você tem mais controle sobre o que é preservado.

### CLAUDE.md como âncora

Qualquer coisa que precisa sobreviver entre compactions e entre sessões deve estar no CLAUDE.md. O summary pode perder detalhes; o CLAUDE.md é lido no início de cada sessão.

### Reiniciar para tarefas não relacionadas

Se acabou uma feature e vai começar outra não relacionada, inicie uma nova sessão. Uma sessão compactada com histórico de outra feature é ruído.

### `--resume` com consciência

```bash
claude --resume SESSION_ID
```

Retoma uma sessão (incluindo compacted). Útil para continuar trabalho; mas o contexto é o compacted, não o original completo.

## Armadilhas

**Confiar no histórico para restrições críticas**: "não faça X" dito há 30 turns pode não sobreviver à compaction. Repita restrições importantes ou coloque no CLAUDE.md.

**Compaction automática em momento ruim**: se você está no meio de um refactoring complexo quando a compaction auto dispara, pode perder contexto crítico. Compacte manualmente antes de atingir o limite.

**`/compact` sem foco**: sem um foco explícito, o summary é genérico. Para sessões de debugging, `/compact Focus on the root cause investigation and findings` é muito melhor que `/compact` sozinho.

## Veja também

- [[03-Dominios/IA/Claude Code/Mental Model/04 - Context window|04 - Context window]]
- [[03-Dominios/IA/Claude Code/Mental Model/07 - Tokens e custo|07 - Tokens e custo]]
- [[03-Dominios/IA/Claude Code/Configuração/index|Configuração]] — CLAUDE.md como âncora entre sessões
- [[03-Dominios/IA/Claude Code/Mental Model/index|Mental Model]] — índice do galho

## Referências

- [Claude Code — Managing context](https://docs.anthropic.com/pt/docs/claude-code/memory)
```

- [ ] **Step 2: Verificar**

```bash
ls "03-Dominios/IA/Claude Code/Mental Model/"
```

Esperado: `06 - Compaction.md` na listagem.

- [ ] **Step 3: Commit**

```bash
git add "03-Dominios/IA/Claude Code/Mental Model/06 - Compaction.md"
git commit -m "feat(claude-code/g1): add 06 - Compaction"
```

---

## Task 7: Criar `07 - Tokens e custo.md`

**Files:**
- Create: `03-Dominios/IA/Claude Code/Mental Model/07 - Tokens e custo.md`

- [ ] **Step 1: Criar o arquivo**

```markdown
---
title: "Tokens e custo — como sessões consomem tokens na prática"
type: concept
publish: true
created: 2026-05-13
updated: 2026-05-13
status: seedling
tags:
  - claude-code
  - mental-model
  - tokens
  - custo
  - ccusage
---

# Tokens e custo — como sessões consomem tokens na prática

> [!abstract] TL;DR
> Todo token processado pelo Claude Code tem custo. Input tokens (o que entra no contexto) são a maior variável — crescem a cada turno porque o histórico completo vai no input. Uma sessão de refactoring pode acumular centenas de milhares de tokens. `ccusage` mostra o breakdown real. As maiores alavancas de redução: leituras cirúrgicas, compaction preventiva e sessões focadas.

## O que é

Claude Code usa a API da Anthropic para processar cada turno da sessão. Cada chamada à API tem um custo baseado em:

- **Input tokens**: tudo no contexto quando o modelo é chamado
- **Output tokens**: o que o modelo gera (resposta + parâmetros de tool calls)
- **Cache read tokens**: tokens que bateram no prompt cache (muito mais baratos)

Preços de referência (Claude Sonnet 4.x, ordem de grandeza):
- Input: ~$3/MTok
- Output: ~$15/MTok
- Cache read: ~$0.30/MTok

Os valores exatos mudam — consulte [anthropic.com/pricing](https://www.anthropic.com/pricing) para valores atuais.

## Como o contexto acumula tokens

O aspecto menos intuitivo: **input tokens crescem a cada turno**, porque o histórico completo da sessão vai no input de cada chamada.

```
Turno 1:  5k tokens de input
Turno 2:  5k + output1 + toolresult1  = ~12k tokens de input
Turno 3:  12k + output2 + toolresult2 = ~20k tokens de input
...
Turno 20: pode estar em 150k+ tokens de input
```

Cada Read de arquivo grande, cada Bash com output verboso, multiplica esse crescimento.

## O que mais consome tokens

| Operação | Impacto | Mitigação |
|----------|---------|-----------|
| `Read` de arquivo grande (1000+ linhas) | Alto | Use `offset` + `limit` |
| `Bash` com output longo (`npm install`, `docker build`) | Alto | `\| tail -20` para filtrar |
| `Grep` com muitos resultados | Médio | Padrões mais específicos |
| Múltiplas iterações (loop de debugging) | Acumulativo | Sessões focadas |
| `Agent` subagent calls | Médio | Isolado — não polui sessão pai diretamente |

## ccusage — rastreando o custo real

`ccusage` é uma ferramenta CLI que lê os logs do Claude Code e mostra o custo por sessão:

```bash
# Instalar
npm install -g ccusage

# Ver uso hoje
ccusage

# Ver histórico dos últimos 7 dias
ccusage --days 7
```

Output típico:

```
Session 2026-05-13 14:23 — codex-technomanticus
  Input:  145,230 tokens  ($0.44)
  Output:  12,450 tokens  ($0.19)
  Cache:   89,100 tokens  ($0.03)
  Total: $0.66
```

## Estratégias de redução de custo

### 1. Leituras cirúrgicas

```
Caro:   Read("src/big-service.ts")                       → arquivo inteiro (~60k tokens)
Barato: Read("src/big-service.ts", offset=200, limit=30) → só o método (~600 tokens)
```

Use `Grep` primeiro para localizar, `Read` com range depois.

### 2. Filtrar output de comandos

```bash
# Caro: output completo do npm ci (~500 linhas)
Bash("npm ci")

# Barato: só o que importa
Bash("npm ci 2>&1 | tail -5")
```

### 3. Compaction preventiva

`/compact` quando a sessão ainda está pequena é mais barato que deixar auto compaction rodar numa sessão grande.

### 4. Sessões focadas

Uma sessão = uma tarefa. Não acumule contexto de trabalho não relacionado.

### 5. Modelo adequado à tarefa

Para tarefas mecânicas (criar arquivo simples, renomear variável), use um modelo menor:

```bash
claude --model claude-haiku-4-5-20251001 "rename variable x to connectionTimeout in auth.ts"
```

Haiku é ~10x mais barato que Sonnet e suficiente para tarefas simples.

## Custo em perspectiva

Para uma equipe de 5 devs usando Claude Code ~2h/dia cada (estimativas amplas):

| Perfil de uso | Custo estimado/mês |
|---------------|--------------------|
| Conversacional leve (poucos reads) | ~$50–100 |
| Desenvolvimento ativo (reads frequentes) | ~$200–500 |
| Refactoring pesado / sessões longas | ~$500–1500 |

O ccusage é a fonte de verdade para o seu uso real.

## Armadilhas

**Ignorar o custo até a fatura chegar**: configure alertas de uso na Anthropic Console.

**Subagents multiplicam custo**: cada subagent (`Agent` tool) é uma sessão separada com seu próprio contexto. O custo é multiplicado pelo número de subagents.

**Cache hit rate baixo**: o prompt cache é ativado quando o início do contexto (system prompt + CLAUDE.md) é idêntico entre chamadas. Mudar o CLAUDE.md frequentemente anula o benefício de cache.

## Veja também

- [[03-Dominios/IA/Claude Code/Mental Model/04 - Context window|04 - Context window]]
- [[03-Dominios/IA/Claude Code/Mental Model/06 - Compaction|06 - Compaction]]
- [[03-Dominios/IA/Claude Code/Time e Automação/05 - Controle de custo|05 - Controle de custo]] — monitoramento em nível de time
- [[03-Dominios/IA/Claude Code/Mental Model/index|Mental Model]] — índice do galho

## Referências

- [Anthropic — Pricing](https://www.anthropic.com/pricing)
- [ccusage — npm](https://www.npmjs.com/package/ccusage)
```

- [ ] **Step 2: Verificar**

```bash
ls "03-Dominios/IA/Claude Code/Mental Model/"
```

Esperado: `07 - Tokens e custo.md` na listagem.

- [ ] **Step 3: Commit**

```bash
git add "03-Dominios/IA/Claude Code/Mental Model/07 - Tokens e custo.md"
git commit -m "feat(claude-code/g1): add 07 - Tokens e custo"
```

---

## Task 8: Criar `08 - Como o agente decide.md`

**Files:**
- Create: `03-Dominios/IA/Claude Code/Mental Model/08 - Como o agente decide.md`

- [ ] **Step 1: Criar o arquivo**

```markdown
---
title: "Como o agente decide — confiança, raciocínio, iteração"
type: concept
publish: true
created: 2026-05-13
updated: 2026-05-13
status: seedling
tags:
  - claude-code
  - mental-model
  - raciocinio
  - decisao
  - prompting
---

# Como o agente decide — confiança, raciocínio, iteração

> [!abstract] TL;DR
> Claude Code usa raciocínio antes de agir — mesmo quando você não vê. O system prompt, CLAUDE.md e o histórico da sessão moldam cada decisão. A qualidade do prompt afeta diretamente a qualidade das decisões: "adicione auth" gera uma decisão muito mais incerta que "adicione JWT auth ao middleware Express em src/middleware/auth.ts, seguindo o padrão de src/middleware/logger.ts". Explicar o *porquê* frequentemente produz resultados melhores que especificar o *como*.

## O que é

Cada tool call que Claude Code executa é precedida por raciocínio: o agente decide *o que fazer* antes de *fazer*. Esse processo usa:

1. **Contexto de sistema**: instruções built-in do Claude Code (como se comportar, quais tools usar, como pedir confirmação)
2. **CLAUDE.md**: suas instruções de projeto (convenções, restrições, preferências)
3. **Histórico da sessão**: o que foi dito e feito até agora
4. **A tarefa atual**: o que você pediu

O raciocínio não é sempre visível — em modo normal, você vê só a ação. Com Plan Mode ou `--verbose`, parte do raciocínio fica exposta.

## Decisão: clarificar vs proceder

O agente toma decisões sobre quando perguntar e quando agir:

| Situação | Comportamento típico |
|----------|---------------------|
| Tarefa clara com contexto suficiente | Age sem perguntar |
| Tarefa ambígua com múltiplas interpretações | Pergunta ou escolhe a mais conservadora |
| Ação irreversível (delete, push, drop table) | Pede confirmação explícita |
| CLAUDE.md proíbe explicitamente | Recusa e explica |

Em modo interativo, o agente pergunta. Em headless, tende a escolher a interpretação mais conservadora.

## O papel do CLAUDE.md nas decisões

O CLAUDE.md funciona como "instruções do tech lead" — moldando o comportamento do agente mais do que qualquer prompt individual.

**Exemplo: sem CLAUDE.md**

```
você: adicione tratamento de erro ao fetchUser

agente: [adiciona try/catch genérico com console.error]
```

**Com CLAUDE.md que diz "use o logger customizado em src/utils/logger.ts"**

```
você: adicione tratamento de erro ao fetchUser

agente: [adiciona try/catch usando logger.error com o formato padrão do projeto]
```

A mesma tarefa, resultado diferente porque o CLAUDE.md informou a decisão.

## Como melhorar a qualidade das decisões

### Especificidade > Generalidade

| Prompt vago | Prompt específico |
|-------------|-------------------|
| "adicione auth" | "adicione autenticação JWT ao middleware em src/middleware/auth.ts" |
| "melhore os testes" | "aumente cobertura de src/services/payment.ts para >80%, focando nos casos de erro" |
| "refatore isso" | "extraia a lógica de validação de src/controllers/users.ts para src/validators/users.ts" |

### Por que > Como

Explicar o objetivo produz decisões melhores que especificar cada passo:

```
Ruim (como): "edite src/cache.ts linha 47 para adicionar um timeout de 5000ms"

Melhor (por quê): "o Redis está causando timeouts em produção quando fica indisponível.
Adicione timeout de 5 segundos às conexões em src/cache.ts para que o serviço
degrade graciosamente em vez de travar."
```

Com o "por quê", o agente pode verificar se há outros pontos que precisam do mesmo fix, escolher a implementação certa, e adicionar um comentário explicativo.

### Plan Mode para verificar o raciocínio

```
Shift+Tab  → ativa plan mode
```

O plano gerado revela o raciocínio do agente: quais arquivos vai ler, que mudanças planeja. É um checkpoint para verificar se o agente entendeu o que você quer antes de executar.

## Incerteza e erros de decisão

O agente não é infalível. Decisões erradas comuns:

**Assumir convenções**: se o projeto não tem CLAUDE.md, o agente assume convenções genéricas que podem não se aplicar.

**Solução local**: corrige o sintoma imediato em vez do problema raiz. Causa: tarefa descreveu sintoma, não causa.

**Over-engineering**: adiciona mais do que pedido. Causa: instruções vagas permitem interpretação ampla.

**Under-engineering**: faz menos do que o esperado. Causa: tarefa ambígua, agente escolheu interpretação conservadora.

## Sinais de incerteza

O agente expressa incerteza de formas diferentes:
- Pergunta antes de agir (modo interativo)
- Adiciona comentários no código (`// Note: this assumes X`)
- Propõe alternativas ("Fiz X, mas Y poderia ser mais adequado se...")
- Status `DONE_WITH_CONCERNS` em workflows agenticos

Esses sinais são informação valiosa — não os ignore.

## Armadilhas

**Prompt de telefone quebrado**: "melhore o código" → agente faz mudanças de estilo → você diz "não era isso" → agente faz outra coisa. Cada iteração vaga desperdiça tokens e frustração. Invista 2 minutos num prompt preciso.

**Confiança implícita**: o agente não perguntará sobre tudo que não sabe. Se você não especificou o logger, ele escolheu um. Revise outputs, especialmente em sessões longas.

**Correções sem contexto**: "não era isso, tenta de novo" sem explicar o que estava errado é feedback ineficiente. Explique o que estava incorreto e por quê.

## Veja também

- [[03-Dominios/IA/Claude Code/Workflows/09 - Prompting para Claude Code|09 - Prompting para Claude Code]]
- [[03-Dominios/IA/Claude Code/Configuração/index|Configuração]] — CLAUDE.md e como moldar decisões
- [[03-Dominios/IA/Claude Code/Mental Model/01 - O loop agentic|01 - O loop agentic]]
- [[03-Dominios/IA/Claude Code/Mental Model/index|Mental Model]] — índice do galho

## Referências

- [Anthropic — Be clear and direct](https://docs.anthropic.com/pt/docs/build-with-claude/prompt-engineering/be-clear-and-direct)
```

- [ ] **Step 2: Verificar**

```bash
ls "03-Dominios/IA/Claude Code/Mental Model/"
```

Esperado: todos os 8 arquivos listados.

- [ ] **Step 3: Commit**

```bash
git add "03-Dominios/IA/Claude Code/Mental Model/08 - Como o agente decide.md"
git commit -m "feat(claude-code/g1): add 08 - Como o agente decide"
```
