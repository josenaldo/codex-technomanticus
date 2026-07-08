---
title: "MCP — Model Context Protocol overview para dev"
type: concept
progress: published
publish: true
created: 2026-05-13
updated: 2026-06-27
status: evergreen
tags:
  - claude-code
  - mcp
  - model-context-protocol
  - overview
  - ferramentas
---

# MCP — Model Context Protocol overview para dev

> [!abstract] TL;DR
> MCP (Model Context Protocol) é o protocolo padrão que conecta o [[Dicionário de IA#Claude Code|Claude Code]] a ferramentas externas: bancos de dados, GitHub, browsers, APIs. Um MCP server expõe capabilities (tools, resources, prompts) que o agente invoca como se fossem tools nativas. Para o dev, MCP é o que faz o agente enxergar o mundo além dos arquivos locais.

## A analogia do estagiário brilhante

Imagine contratar o estagiário mais inteligente que você já viu. Ele aprende rápido, raciocina bem, escreve código limpo. Mas tem uma limitação: ele só consegue trabalhar com papéis que estão na mesa à frente dele. Tudo que está no computador, no banco de dados, no GitHub, na wiki — para ele não existe.

Essa é a situação do Claude Code sem MCP. As tools nativas (`Read`, `Write`, `Bash`) alcançam os arquivos locais. Mas banco de dados, issues do GitHub, tickets do Jira, resultados de testes de browser — o agente só acessa via terminal, com output de texto bruto que ele precisa parsear.

MCP resolve isso. Com um MCP server configurado, você coloca um "telefone" na mesa do estagiário — ele disca para o banco de dados, para o GitHub, para qualquer sistema externo. Os dados chegam estruturados, não como texto bruto.

> [!question] Por que isso importa na prática?
> Sem MCP: "Rode `SELECT * FROM orders WHERE status = 'pending'` e me mostre o output."
> Com MCP: "Quais são os pedidos pendentes mais antigos?" — o agente consulta o banco diretamente e raciocina sobre os dados.

## O problema que o MCP resolve

Claude Code tem tools nativas: `Read`, `Write`, `Edit`, `Bash`, `Grep`. Com elas, o agente acessa arquivos locais e executa comandos. Mas não acessa diretamente:

- Banco de dados (só via SQL pelo terminal, output como texto)
- GitHub Issues, PRs e commits de outros repos
- Jira, Linear, Notion
- Browser para testar UI em tempo real
- APIs externas autenticadas

Antes do MCP, a única opção era invocar esses sistemas via `Bash`, com output de texto bruto que o agente tinha que parsear. O agente entendia o resultado, mas sem estrutura garantida — uma query retornando 500 linhas de texto é muito diferente de receber um array de objetos JSON tipados.

## Como o MCP funciona

MCP é um protocolo cliente-servidor. O Claude Code tem um **MCP client embutido**. Você configura um ou mais **MCP servers** no `settings.json`. Quando Claude Code inicia, o client lança os servers e expõe suas capabilities ao agente.

```mermaid
flowchart LR
    subgraph CC["Claude Code"]
        A["Agente\n(LLM)"]
        MC["MCP Client\n(embutido)"]
        A <--> MC
    end
    subgraph MS["MCP Servers"]
        PG["server-postgres\n(processo local)"]
        GH["server-github\n(processo local)"]
        BR["server-puppeteer\n(processo local)"]
    end
    subgraph EXT["Sistemas externos"]
        DB[("PostgreSQL")]
        API["GitHub API"]
        WEB["Browser"]
    end
    MC <-->|"JSON-RPC\nstdio/HTTP"| PG
    MC <-->|"JSON-RPC\nstdio/HTTP"| GH
    MC <-->|"JSON-RPC\nstdio/HTTP"| BR
    PG <--> DB
    GH <--> API
    BR <--> WEB
```

O protocolo de comunicação entre client e server é **JSON-RPC sobre stdio** (para processos locais) ou **HTTP/SSE** (para servers remotos). O agente não vê esses detalhes — para ele, as tools do MCP server parecem tools nativas.

## Os três tipos de capability MCP

MCP define três tipos de capability que um server pode expor:

### Tools

Funções que o agente pode invocar. Podem ter efeitos colaterais (criar issues, rodar queries, navegar).

```
Exemplos de tools:
query_database(sql: string) → rows[]
create_issue(title: string, body: string, labels: string[]) → issue_id
navigate_to(url: string) → page_content
run_migration(name: string) → result
```

O agente decide quando invocar uma tool com base no contexto. O resultado volta ao agente como dados estruturados — não como texto bruto.

### Resources

Dados que o agente pode ler, como arquivos — mas de sistemas externos. Somente leitura.

```
Exemplos de resources (URIs):
database://myapp/schema        → schema completo do banco
github://myorg/repo/main/src/  → listagem de arquivos
notion://workspace/pages       → lista de páginas
```

Resources são úteis para fornecer contexto grande (o schema do banco inteiro) sem que o agente precise fazer múltiplas queries.

### Prompts

Templates de instrução que o agente pode invocar como se fossem slash commands do MCP server.

```
Exemplos de prompts:
/debug-slow-query   → template para análise de query lenta com EXPLAIN
/review-migration   → template para revisar migration antes de rodar
/check-pr-diff      → template para analisar o diff de um PR específico
```

A diferença entre um prompt MCP e uma skill: o prompt MCP é definido pelo server (focado nas capabilities do sistema externo); a skill é um arquivo Markdown local (focado no processo do time).

## Configuração básica em settings.json

```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "DATABASE_URL": "${DATABASE_URL}"
      }
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

Quando Claude Code inicia, ele lança cada server como um processo filho via `command + args`. As tools do server ficam disponíveis na sessão automaticamente — você não precisa invocar nada para ativá-las.

> [!warning] Nunca commite segredos inline no settings.json
> Use `"${VARIAVEL}"` (interpolação de env) em vez de colocar o valor diretamente. `DATABASE_URL: "postgresql://user:senha@..."` no settings.json é um segredo no git.

## MCP server vs tool nativa

| Dimensão | Tool nativa | MCP tool |
|---|---|---|
| Onde fica | Embutida no Claude Code | Processo externo separado |
| Como acessa | Chamada direta no runtime | Via MCP client → server → sistema |
| Contexto disponível | Arquivos e processos locais | Qualquer sistema que o server acesse |
| Estado | Sem estado persistente | Server pode manter conexões, cache |
| Latência | Mínima | Depende do server e do sistema externo |
| Exemplo | `Bash`, `Read`, `Edit`, `Grep` | `query_db`, `create_pr`, `navigate_to` |
| Quem define | Anthropic | Anthropic, comunidade, você mesmo |

## Ecossistema de MCP servers

Anthropic e a comunidade mantêm servers para os casos de uso mais comuns:

| Server | Instala via | Capabilities principais |
|---|---|---|
| `@modelcontextprotocol/server-postgres` | npx | Queries SQL, schema, explain |
| `@modelcontextprotocol/server-github` | npx | PRs, issues, code, commits |
| `@modelcontextprotocol/server-filesystem` | npx | Acesso mais granular ao filesystem |
| `@modelcontextprotocol/server-brave-search` | npx | Pesquisa web estruturada |
| `@modelcontextprotocol/server-puppeteer` | npx | Browser automation, screenshots |
| `@modelcontextprotocol/server-sqlite` | npx | SQLite local |
| `@modelcontextprotocol/server-slack` | npx | Mensagens, canais, threads |

Ver [[03-Dominios/Tecnologia/IA/Claude Code/Skills e MCP/05 - MCP servers essenciais|05 - MCP servers essenciais]] para configuração e casos de uso de cada um.

## Por que o dev precisa entender MCP

O MCP tem dois níveis de uso:

**Para usar Claude Code produtivamente:**
1. Saber quais MCP servers existem para o seu stack
2. Configurar em `settings.json` com vars de ambiente
3. Saber que as tools do server aparecem naturalmente na sessão — não precisa invocar

**Para personalizar o agente para o projeto:**
1. Criar MCP servers para ferramentas internas da empresa
2. Expor dados do projeto como resources (schema, configurações)
3. Compor skills + MCP para workflows completos de agente especializado

```mermaid
sequenceDiagram
    participant U as Usuário
    participant CC as Claude Code
    participant PG as MCP Postgres server
    participant DB as PostgreSQL

    U->>CC: Quais pedidos estão pendentes há mais de 7 dias?
    CC->>PG: query_database("SELECT id, created_at FROM orders WHERE status='pending' AND created_at < NOW() - INTERVAL '7 days'")
    PG->>DB: SQL query
    DB-->>PG: rows[]
    PG-->>CC: [{id: 123, created_at: "2026-06-10"}, ...]
    CC-->>U: Há 3 pedidos pendentes há mais de 7 dias: #123 (17 dias), #456 (12 dias), #789 (8 dias)
```

Sem o MCP server, o agente pediria ao usuário para rodar a query manualmente e colar o resultado. Com o server, o agente faz a query, interpreta, e responde diretamente.

## Modelo de segurança do MCP

O MCP delega a segurança para dois lugares:

**1. O server controla o acesso**
O server decide quais queries aceita, com quais credenciais se autentica, e quais sistemas acessa. Um server Postgres bem configurado pode limitar as queries a `SELECT` e rejeitar qualquer `DROP`, `DELETE`, ou `UPDATE`.

**2. O Claude Code controla a aprovação**
Certas tools MCP pedem aprovação do usuário antes de executar — especialmente as que têm efeitos colaterais. O agente apresenta o que vai fazer e aguarda confirmação.

```mermaid
sequenceDiagram
    participant A as Agente
    participant CC as Claude Code
    participant U as Usuário
    participant S as MCP Server

    A->>CC: Quero invocar create_issue(title="Bug crítico")
    CC->>U: 🔔 O agente quer criar uma issue no GitHub. Permitir?
    U->>CC: Sim
    CC->>S: create_issue(title="Bug crítico")
    S-->>CC: issue_id: 456
    CC-->>A: Issue #456 criada
    A-->>U: Criei a issue #456 — Bug crítico
```

**Boas práticas de segurança ao configurar MCP:**
- Banco de dados: use um usuário com permissões mínimas (somente `SELECT` se só vai consultar)
- GitHub: use um token com escopos mínimos (`repo:read` em vez de `repo` completo se não vai criar PRs)
- Nunca conecte MCP servers a produção sem guardrails de hook
- Revise regularmente quais servers estão configurados e com quais permissões

## Armadilhas

> [!warning] MCP server conectado a produção sem guardrails
> Um MCP postgres apontando para o banco de produção significa que o agente pode rodar `DROP TABLE` em produção se instruído (ou enganado) a fazer isso. Configure hooks de guardrail antes de conectar MCP servers em ambientes críticos. Ver [[03-Dominios/Tecnologia/IA/Claude Code/Hooks e Guardrails/index|Hooks e Guardrails]].

> [!warning] Latência impacta a sessão
> Cada invocação de tool MCP é uma chamada ao server e ao sistema externo. Um server lento torna a sessão lenta. Para dados que não mudam frequentemente (schema do banco, lista de projetos), considere cachear no server ou usar resources em vez de tools repetidas.

> [!warning] Versionar o settings.json com cuidado
> O `settings.json` com configuração de MCP pode ir no git — mas sem valores de segredos inline. Use interpolação de variáveis de ambiente (`${VAR}`) e documente quais variáveis o projeto precisa no README ou no onboarding.

> [!warning] Confundir MCP server com skill
> Skills são instruções para o agente (como fazer). MCP servers são capabilities do agente (o que ele pode fazer). São complementares, não substitutos. A skill `/deploy` diz o processo; o MCP server `github` dá a capability de criar o PR.

## Tipos de transporte: stdio vs HTTP/SSE

O MCP suporta dois mecanismos de comunicação entre client e server:

### stdio (padrão para servers locais)

O server é iniciado como processo filho do Claude Code. A comunicação acontece via stdin/stdout.

```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": { "DATABASE_URL": "${DATABASE_URL}" }
    }
  }
}
```

**Vantagens:**
- Simples de configurar
- Sem necessidade de porta ou firewall
- O server começa e termina com o Claude Code

**Quando usar:**
- Tools que rodam localmente (banco na máquina, filesystem, processo local)
- Development e testes

### HTTP/SSE (para servers remotos)

O server roda em um endereço HTTP. O client conecta via URL.

```json
{
  "mcpServers": {
    "minha-api-interna": {
      "url": "https://mcp.empresa.internal/server",
      "headers": {
        "Authorization": "Bearer ${MCP_TOKEN}"
      }
    }
  }
}
```

**Vantagens:**
- Server pode rodar em outra máquina ou na nuvem
- Múltiplos clients podem compartilhar o mesmo server
- Server persiste entre sessões do Claude Code

**Quando usar:**
- APIs da empresa que você quer expor como MCP (sem distribuir o código do server)
- Tools que precisam de autenticação centralizada
- Ambientes de CI/CD onde o server roda separado

```mermaid
flowchart TD
    subgraph LOCAL["Uso local (stdio)"]
        CC1["Claude Code"] -->|"stdin/stdout"| S1["server-postgres\n(processo filho)"]
        S1 --> DB[("Postgres local")]
    end
    subgraph REMOTE["Uso remoto (HTTP/SSE)"]
        CC2["Claude Code"] -->|"HTTPS"| S2["MCP server\n(cloud/empresa)"]
        S2 --> API["API interna"]
    end
```

## Casos de uso por tipo de dev

O MCP é mais útil dependendo do contexto. Aqui estão os casos de uso mais comuns por perfil:

### Backend / Fullstack

O MCP server mais valioso é o de banco de dados. Com ele, o agente pode:
- Inspecionar o schema sem precisar abrir o DBeaver
- Escrever e testar queries direto na conversa
- Analisar dados de um bug reportado sem precisar de acesso direto ao terminal

```
/code-review-ts
Verifique se a query em src/orders/repository.ts usa os índices corretamente
```

O agente lê o código, consulta o schema via MCP Postgres, verifica o plano de execução (EXPLAIN) e responde com análise fundamentada.

### Frontend

O MCP de browser (Puppeteer) é o mais útil: o agente consegue abrir o app, interagir com elementos, tirar screenshots, e reportar o que viu — sem você precisar descrever o estado da UI.

```
Abra http://localhost:3000/checkout e verifique se o botão "Finalizar compra" está habilitado quando o carrinho tem itens
```

O agente navega, verifica, tira screenshot, responde com o estado real — não com uma suposição baseada no código.

### Tech Lead / Gerente técnico

O MCP de GitHub é o mais valioso: o agente acessa PRs abertos, issues prioritárias, e pode ajudar a triagem sem você ter que copiar e colar dados da interface.

```
Quais PRs abertos têm conflito com a branch de release desta semana?
```

O agente verifica os PRs via MCP GitHub, identifica conflitos potenciais e organiza por prioridade.

## O MCP na visão do agente

Do ponto de vista do agente, não há diferença visível entre uma tool nativa e uma MCP tool. Quando você tem o server Postgres configurado, o agente simplesmente tem acesso a uma tool chamada `query_database`. Ele decide quando usá-la pelo contexto — assim como decide quando usar `Read` ou `Bash`.

Isso é intencional no design do MCP: o protocolo é invisível para o modelo. O agente pensa em capabilities, não em transporte. Para ele, a pergunta é "tenho acesso ao banco de dados?" — não "qual é o protocolo de comunicação com o server Postgres?".

> [!tip] Implicação prática
> Você não precisa instruir o agente a "usar o MCP". Configure o server, e o agente vai naturalmente usar as tools disponíveis quando o contexto exigir. O MCP se integra ao raciocínio do agente, não ao workflow do usuário.

## Como explicar em inglês

**MCP (Model Context Protocol)** — an open protocol that standardizes how AI agents connect to external tools and data sources. The agent's version of a USB standard: any system that speaks MCP can be plugged into the agent.

**MCP server** — a separate process that exposes tools, resources, and prompts via JSON-RPC. The agent invokes them as if they were native tools.

**Key phrases for interviews:**
- "MCP extends the agent's reach beyond local files. Without MCP, the agent is limited to what it can read from disk or run in a terminal. With MCP, it can query databases, interact with GitHub, control a browser."
- "The protocol separates *what the agent can do* (capabilities, via MCP) from *how it should do it* (process, via skills). That separation keeps each concern focused."
- "Tools have side effects; resources are read-only; prompts are workflow templates. That distinction matters for safety: read-only resources can't drop tables."

**Common follow-up questions:**
- *"Is MCP Anthropic-specific?"* — No. MCP is an open protocol designed for any AI agent. Other providers are adopting it.
- *"How is an MCP tool different from a function call?"* — They're the same concept at the protocol level. MCP tools are function-call schemas exposed by an external server, not hardcoded in the model.
- *"Who should create MCP servers?"* — For standard tools (Postgres, GitHub), use community servers. For internal tools (your company's API, internal database), create a custom server.

**Termos PT ↔ EN**

| Português | English |
|---|---|
| Servidor MCP | MCP server |
| Ferramentas / recursos / prompts | Tools / resources / prompts |
| Transporte | Transport |

> [!tip] Vídeo sobre MCP
> [Building Agents with Model Context Protocol — Full Workshop com Mahesh Murag (Anthropic)](https://www.youtube.com/watch?v=kQmXtrmQ5Zg) explica os três primitivos do protocolo (tools, resources, prompts) e mostra a construção de um agente com MCP do zero — direto de quem projetou o protocolo.

## O que vem a seguir

Este overview cobriu o *o quê* e o *por quê* do MCP: o protocolo, os três tipos de capability, o modelo de segurança, stdio vs HTTP/SSE. Falta o *com quê* — quais servers existem de fato, o que cada um resolve, e como configurá-los sem reinventar a roda. É esse o assunto de [[03-Dominios/Tecnologia/IA/Claude Code/Skills e MCP/05 - MCP servers essenciais|05 - MCP servers essenciais]], que cataloga os servers mais usados (Postgres, GitHub, filesystem, browser) e as decisões práticas de configuração.

## Referências

- [Model Context Protocol — especificação oficial](https://spec.modelcontextprotocol.io) — documentação completa do protocolo
- [MCP servers — repositório oficial Anthropic](https://github.com/modelcontextprotocol/servers) — catálogo de servers prontos
- [[03-Dominios/Tecnologia/IA/Claude Code/Skills e MCP/05 - MCP servers essenciais|05 - MCP servers essenciais]] — configuração e casos de uso dos servers mais comuns
- [[03-Dominios/Tecnologia/IA/Claude Code/Skills e MCP/06 - Criar MCP server|06 - Criar MCP server]] — quando e como criar um server customizado
- [[03-Dominios/Tecnologia/IA/Claude Code/Skills e MCP/07 - Compondo skills e MCP|07 - Compondo skills e MCP]] — combinando skills + MCP para agentes especializados
- [[03-Dominios/Tecnologia/IA/Claude Code/Hooks e Guardrails/index|Hooks e Guardrails]] — como adicionar segurança ao usar MCP servers
- [[03-Dominios/Tecnologia/IA/Agentes de Codificação/15 - MCP — o protocolo universal|MCP — o protocolo universal]] — visão mais ampla do protocolo no ecossistema de IA
- [[03-Dominios/Tecnologia/IA/Claude Code/Skills e MCP/index|Skills e MCP]] — índice do galho
