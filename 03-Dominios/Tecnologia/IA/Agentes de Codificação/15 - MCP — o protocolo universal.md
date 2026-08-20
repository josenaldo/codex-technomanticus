---
title: "MCP — o protocolo universal"
created: 2026-05-02
updated: 2026-07-05
type: concept
progress: done
status: growing
fase: adepto
publish: true
tags:
  - agentes-codificacao
  - ia
  - ferramentas
aliases:
  - MCP
  - Model Context Protocol
  - Protocolo de contexto
---

# MCP — o protocolo universal

> [!abstract] TL;DR
> O [[Dicionário de IA#MCP (Model Context Protocol)|Model Context Protocol (MCP)]] é um padrão aberto criado pela Anthropic que define como agentes AI se conectam com ferramentas externas (bancos de dados, APIs, file systems, browsers). É o "USB da IA" — uma interface universal que elimina o problema de N×M integrações custom: cada ferramenta implementa o protocolo uma vez e funciona com qualquer agente compatível. Em 2026, Claude Code, Cursor, Gemini CLI e dezenas de harnesses open source suportam MCP. Saber configurar MCP servers é a skill que transforma um agente genérico em um agente específico para o seu domínio.

## O problema: N×M integrações

Antes do MCP, o cenário era o seguinte: você tem N agentes (Claude Code, Cursor, Copilot, seu harness interno) e M ferramentas (PostgreSQL, GitHub, Jira, Confluence, browser, sistema de arquivos, API interna). Para cada combinação, alguém precisava escrever uma integração custom.

Resultado: N×M integrações. Para N=5 agentes e M=8 ferramentas, isso é 40 integrações — cada uma com seu próprio formato, autenticação, tratamento de erros e manutenção. Times de infraestrutura de IA grande o suficiente para fazer isso existem; todos os outros vivem sem as integrações.

A analogia histórica é o mercado de cabos de carregadores antes do USB: toda fabricante tinha o próprio conector. Quando o padrão chegou, o ecossistema explodiu. MCP faz o mesmo para a IA — qualquer ferramenta que implementa o protocolo funciona com qualquer agente compatível.

**Com MCP:** N+M integrações. Cada ferramenta implementa o protocolo uma vez. Cada agente implementa o cliente uma vez. O ecossistema cresce em duas direções independentes.

## Como funciona internamente

### Os três participantes

Antes de entrar na arquitetura, a pergunta que vale responder: *por que um protocolo separado?* O agente não poderia simplesmente chamar APIs REST diretamente? Tecnicamente poderia — mas sem padronização, cada ferramenta exige que o modelo aprenda seu formato específico (autenticação, estrutura de request, tratamento de erro). Com MCP, o modelo aprende o protocolo uma vez e qualquer ferramenta que o implementa funciona de forma previsível.

O protocolo define três papéis:

| Papel | O que é | Exemplo |
|-------|---------|---------|
| **Host** | O agente AI que inicia sessões | Claude Code, Cursor, harness custom |
| **Client** | Módulo dentro do host que gerencia conexões MCP | Embutido no agente |
| **Server** | O processo externo que expõe ferramentas | `server-postgres`, seu server custom |

O host pode conectar a vários servers simultaneamente. Cada server roda como processo separado, se comunica com o client via transporte (stdio ou HTTP/SSE), e expõe suas capacidades via três primitivas.

### As três primitivas

```mermaid
graph TB
    subgraph "MCP Server"
        T[Tools — ações que o modelo invoca]
        R[Resources — dados que o modelo lê]
        P[Prompts — templates pré-definidos]
    end
    subgraph "Agent Host"
        M[Modelo LLM]
        C[MCP Client]
    end
    M -->|"decide usar tool"| C
    C -->|"invoca"| T
    C -->|"carrega"| R
    C -->|"usa"| P
    T -->|"retorna resultado"| C
    R -->|"retorna conteúdo"| C
    C -->|"injeta no contexto"| M
```

**Tools:** ações que o modelo pode invocar diretamente — análogas a function calls. São a primitiva mais usada. Exemplos: `execute_query`, `create_issue`, `read_file`, `send_email`.

**Resources:** fontes de dados que o modelo pode ler passivamente — documentação, schemas de BD, configs. São como documentos que o agente pode consultar, não ações que ele toma.

**Prompts:** templates de instrução pré-definidos que o usuário ou o modelo podem instanciar. Menos comuns, mas úteis para padronizar interações repetitivas — `analyze-pr`, `explain-error`, `write-migration`.

### Transporte: como client e server se comunicam

MCP suporta dois transportes:

| Transporte | Quando usar | Exemplo |
|-----------|------------|---------|
| **stdio** | Server local, mesmo processo ou máquina | Server PostgreSQL rodando localmente |
| **HTTP/SSE** | Server remoto, multi-cliente, serviço gerenciado | MCP server na cloud para dados corporativos |

Stdio é mais simples: o client inicia o processo do server e se comunica via stdin/stdout. HTTP/SSE permite servers rodando como serviços independentes — útil para times que querem compartilhar um MCP server entre múltiplos desenvolvedores.

### Fluxo de uma tool invocation

```mermaid
sequenceDiagram
    participant M as Modelo
    participant C as MCP Client
    participant S as MCP Server
    participant D as Banco de Dados

    M->>C: "Preciso consultar usuários ativos"
    C->>S: tools/call: execute_query(sql)
    S->>D: SELECT COUNT(*) FROM users WHERE active=true
    D->>S: 1247
    S->>C: {content: [{type: "text", text: "Active users: 1247"}]}
    C->>M: resultado injetado no contexto
    M->>M: usa resultado para continuar a resposta
```

O modelo decide quando usar uma tool com base na descrição que o server registrou. Boas descrições são críticas — um server com `get_user_count: "Returns user count"` vai ser usado de forma diferente de um com `get_user_count: "Returns the current number of active (non-deleted, last_login within 30 days) users from the production database"`.

## Configuração em Claude Code

O arquivo de configuração fica em `.claude/mcp.json` (nível de projeto) ou `~/.claude/mcp.json` (global):

```json
{
  "servers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "DATABASE_URL": "postgresql://user:pass@localhost/mydb"
      }
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/docs"]
    }
  }
}
```

A configuração é declarativa: você diz qual processo iniciar e com quais variáveis de ambiente. Claude Code inicia o processo quando a sessão começa, mantém a conexão aberta durante toda a sessão, e encerra o processo ao final. Você não gerencia o ciclo de vida — o host faz isso.

**Boa prática:** use `${GITHUB_TOKEN}` em vez do token em texto plano — Claude Code interpola variáveis de ambiente. Commitando o `mcp.json` com tokens literais é o tipo de acidente que vai para o `git log` para sempre.

**Um erro comum:** configurar o server com permissões amplas demais. O `server-filesystem` com `/` como path root dá ao agente acesso a todo o sistema de arquivos — algo que pode ser desejável para um agente de automação e desastroso para um agente de code review. Restrinja o path ao diretório que o agente realmente precisa acessar.

## MCP Servers populares em 2026

| Server | O que expõe | Caso de uso principal |
|--------|------------|----------------------|
| `server-postgres` | execute_query, list_tables, describe_table | Debugging de BD, geração de migrações |
| `server-github` | create_issue, list_prs, get_file, search_code | Workflow de desenvolvimento completo |
| `server-filesystem` | read_file, list_directory, search_files | Acesso a documentação e configs |
| `server-brave-search` | web_search | Pesquisa técnica em tempo real |
| `server-puppeteer` | navigate, screenshot, click, fill_form | Testes visuais, automação de browser |
| `server-slack` | post_message, list_channels, get_thread | Notificações e busca de contexto |
| `server-jira` | create_ticket, get_sprint, update_status | Gestão de projeto |
| `server-sqlite` | execute_query, schema inspection | Desenvolvimento local com SQLite |

> [!tip] Assista: MCP Explained — The Full Beginner's Guide
> **Canal:** James Briggs | **Duração:** ~20min | **Idioma:** EN
>
> James Briggs explica o Model Context Protocol do zero — da motivação (o problema N×M) até a configuração de servers reais com PostgreSQL e GitHub. O vídeo é útil porque mostra o protocolo funcionando ao vivo: você vê o agente consultando o banco de dados, navegando issues do GitHub e lendo arquivos do sistema de arquivos em uma única sessão, sem integração custom entre os tools. O ponto mais revelador vem em [14:32], quando ele mostra que a mesma configuração funciona tanto em Claude Code quanto em Cursor sem modificação — exatamente a promessa do protocolo. Trecho de destaque [14:32]: *"The same MCP server works across different AI clients — that's the whole point. You write the server once, and it just works everywhere."*
>
> 🎬 https://www.youtube.com/watch?v=dK1OoUWiJbQ

## Criando um MCP Server custom

Quando os servers disponíveis não cobrem sua necessidade, criar um server custom é surpreendentemente simples. O SDK oficial está disponível para TypeScript e Python.

```typescript
// server.ts — server mínimo com tool e resource
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const server = new McpServer({
  name: "my-project-tools",
  version: "1.0.0"
});

// Tool: ação que o modelo pode invocar
server.tool(
  "get_active_user_count",
  "Returns the number of active users (last_login within 30 days, non-deleted)",
  {},
  async () => {
    const count = await db.query(
      "SELECT COUNT(*) FROM users WHERE active = true AND deleted_at IS NULL"
    );
    return { content: [{ type: "text", text: `Active users: ${count.rows[0].count}` }] };
  }
);

// Resource: dado que o modelo pode consultar passivamente
server.resource(
  "api-schema",
  "openapi://schema",
  async () => ({
    contents: [{
      uri: "openapi://schema",
      mimeType: "application/json",
      text: JSON.stringify(openApiSpec)
    }]
  })
);

// Exemplo de como um erro seria tratado (o modelo vê a mensagem e decide)
server.tool(
  "deploy_to_staging",
  "Triggers a staging deployment. Returns deployment ID or error message.",
  { branch: { type: "string", description: "branch name to deploy" } },
  async ({ branch }) => {
    try {
      const deployId = await cicd.triggerDeploy(branch, "staging");
      return { content: [{ type: "text", text: `Deploy started: ${deployId}` }] };
    } catch (err) {
      // Não lançar exceção — retornar o erro como conteúdo legível
      return {
        content: [{ type: "text", text: `Deploy failed: ${err.message}` }],
        isError: true
      };
    }
  }
);

const transport = new StdioServerTransport();
server.connect(transport);
```

**Lição da implementação:** tools que lançam exceção interrompem o loop agentic de forma abrupta — o agente recebe um erro que pode não conseguir interpretar. A boa prática é retornar o erro como conteúdo legível com `isError: true`. Assim o modelo lê a mensagem de erro e pode tomar uma decisão (tentar novamente, pedir ajuda, ajustar a abordagem).

## Quando usar (e quando não usar)

A pergunta certa não é "o que posso fazer com MCP?" — é "quando MCP justifica o overhead de configuração e manutenção?"

| Cenário | MCP vale? | Razão |
|---------|-----------|-------|
| Consultar BD regularmente na sessão | ✅ Sim | Elimina copy-paste, mantém contexto |
| Criar issues/PRs como parte do workflow | ✅ Sim | O agente fecha o loop sem sair do terminal |
| Acessar documentação interna constantemente | ✅ Sim | Resource MCP injeta docs no contexto sob demanda |
| Rodar um script bash uma única vez | ❌ Não | Overkill — o agente pode chamar `bash` diretamente |
| Integração que muda toda semana | ⚠️ Cuidado | Overhead de manutenção pode superar o benefício |
| Time com um único desenvolvedor usando IA | ⚠️ Opcional | Vale se o setup for reutilizável; senão, convença o próximo desenvolvedor |

> [!question] Mas e se eu já tenho um script que faz isso?
> Scripts são complementares ao MCP, não concorrentes. Um padrão comum é o MCP server ser uma casca fina que chama scripts existentes — você não reescreve a lógica, só expõe via protocolo. A vantagem é que o agente ganha contexto estruturado (erros legíveis, parâmetros tipados) em vez de parsear saída de terminal bruta.

## Casos práticos

### Caso 1 — Debugando uma query lenta com MCP Postgres

**Cenário:** bug em produção. Usuários reportam que a página de relatórios demora 30 segundos para carregar. Sem MCP, o fluxo é: conectar ao BD, copiar a query suspeita, rodar o EXPLAIN manualmente, voltar para o agente, colar o resultado, pedir análise.

**Com MCP Postgres:** o agente tem acesso direto ao banco. A conversa é:

> *"Está lento? Deixa eu rodar `EXPLAIN ANALYZE` nas queries que mais aparecem no log."*

O agente identifica que há um `WHERE user_id = $1` sem índice em uma tabela de 2 milhões de linhas. Ele escreve a migration para criar o índice, aplica no staging, roda EXPLAIN novamente para confirmar a melhoria, e só então propõe o PR. Tudo em uma sessão.

**O que MCP elimina:** 12 ciclos de copy-paste entre o terminal do BD e o chat. Mas mais importante: elimina o contexto perdido entre esses ciclos — o agente mantém em mente que está investigando o relatório, não começa cada query do zero.

### Caso 2 — Triagem automática de issues com MCP GitHub

**Cenário:** repositório open source com 50+ issues abertas. Toda semana é preciso triá-las: priorizar, classificar por componente, fechar duplicatas, pedir mais informações nas que estão incompletas.

**Com MCP GitHub configurado:**

```
"Você pode me ajudar a triar as issues abertas? Filtre só as abertas na última semana,
classifique por componente (auth/payments/api), marque as que são claramente duplicatas,
e gere um relatório de quais precisam de mais informações."
```

O agente lista as issues via `list_issues`, lê o conteúdo de cada uma, compara com issues mais antigas via `search_issues`, cria labels via `add_label`, e gera um relatório estruturado. Ele também pode rascunhar respostas para issues incompletas que precisam de mais detalhes — você revisa e aprova antes de postar.

**O que diferencia de um script:** o agente entende linguagem natural nas issues, consegue detectar que "app crashes on login" e "authentication fails with 500" são provavelmente o mesmo problema, e justifica as classificações. Um script precisaria de regras explícitas para cada caso.

### Caso 2b — Quando MCP GitHub causa problema

Para completar o panorama: imagine que o server-github tem acesso a criar PRs e fazer merge. Durante uma sessão de refactoring, você pede ao agente para "reorganizar os arquivos de config". Ele reorganiza — e por inferência decide que deve "fechar" a issue relacionada que havia no contexto. Com permissões amplas, `close_issue` está disponível. O agente fecha a issue sem você ter pedido explicitamente.

O problema não é o agente ser malicioso — é que tool selection em modelos de linguagem não é determinística. Com muitas tools disponíveis, o modelo às vezes as usa por proximidade semântica, não por necessidade real. A defesa: configure o server com only as tools que você realmente quer que o agente use. O SDK permite registrar um subconjunto das tools disponíveis.

### Caso 3 — MCP server custom para sistema legado

**Cenário:** API interna legada sem documentação. O time usa o agente para escrever código de integração, mas toda sessão começa com "qual é o endpoint para X? E os parâmetros?" — contexto que se perde entre sessões.

**Solução:** criar um MCP server custom com:
- **Resource:** o schema da API em formato legível (gerado uma vez via engenharia reversa)
- **Tool:** `call_legacy_api(endpoint, params)` — encapsula autenticação interna e tratamento de erros específicos do sistema
- **Tool:** `list_available_endpoints()` — o agente pode perguntar o que está disponível antes de chamar

O server fica em um repositório interno, commitado, com versão. Quando a API muda, alguém atualiza o resource. Todos os desenvolvedores do time têm o contexto automaticamente.

### Caso 4 — MCP como ponte entre agente e CI/CD

**Cenário:** time que usa IA para gerar código também quer usar IA para validar o código gerado — um loop de feedback curto onde o agente implementa, dispara o CI, lê os resultados e corrige sem intervenção humana para erros simples (falhas de lint, testes unitários, type errors).

**Configuração:**

```json
{
  "servers": {
    "cicd": {
      "command": "node",
      "args": ["./tools/mcp-cicd-server.js"],
      "env": {
        "CI_API_TOKEN": "${CI_API_TOKEN}",
        "PROJECT_ID": "my-project-123"
      }
    }
  }
}
```

O server customizado expõe:
- `trigger_pipeline(branch)` → retorna pipeline ID
- `get_pipeline_status(id)` → retorna status + logs resumidos
- `get_failed_jobs(id)` → retorna detalhes dos jobs que falharam
- `get_test_results(id)` → retorna lista de testes que falharam com mensagens de erro

**O loop resultante:** o agente implementa a feature, chama `trigger_pipeline`, aguarda, chama `get_failed_jobs`, lê os erros específicos, corrige o código, aciona novamente. Para erros determinísticos (lint, type check, testes unitários quebrando por assinatura errada), o agente resolve sem intervenção humana. Para erros semânticos (lógica errada, flaky tests), ele reporta com contexto específico em vez de "o CI falhou".

**O que isso elimina:** o desenvolvedor não precisa mais copiar mensagens de erro do CI para o chat. O contexto viaja direto — e o agente tem a exata linha de teste que falhou, não um log de 200 linhas para parsear mentalmente.

## Armadilhas comuns

O fio que une a maioria das armadilhas a seguir é o mesmo: MCP abstrai a complexidade de integração, mas não abstrai as consequências das decisões de segurança e design que você faz ao configurar os servers. A abstração é uma ilusão de simplicidade — por baixo, as implicações de segurança e custo são tão reais quanto em qualquer integração manual.

> [!warning] Muitos servers = muitos tokens de contexto
> Cada MCP server registra suas tool definitions no contexto do modelo — nome, descrição, parâmetros. 10 servers com 5 tools cada = 50 definições de tool = centenas de tokens de contexto em cada request. Isso tem dois custos: (1) custo financeiro literal, pois tokens de contexto são cobrados em toda requisição; (2) degradação de qualidade, pois o modelo pode ter dificuldade em selecionar a tool certa entre muitas opções. Regra prática: configure só os servers que você vai realmente usar na sessão. Claude Code permite ativar/desativar servers por sessão.

> [!warning] Credenciais no mcp.json commitado é um vazamento esperando acontecer
> O `.claude/mcp.json` muitas vezes fica no repositório para que o time compartilhe a configuração. Se você incluir tokens, senhas ou connection strings diretamente no arquivo, eles vão para o `git history` — e de lá não saem facilmente. Use sempre variáveis de ambiente (`"${GITHUB_TOKEN}"`) e documente quais variáveis precisam ser configuradas localmente. Uma alternativa: mantenha um `mcp.json.example` no repositório e o `mcp.json` real no `.gitignore`.

> [!warning] Permissões amplas demais criam superfície de ataque
> Um MCP server de filesystem com acesso ao `/` ou um server de BD com credenciais de `superuser` transformam o agente em um vetor de ataque potencial. Se o agente for comprometido (prompt injection via conteúdo malicioso no contexto), ele pode usar as tools para ações destrutivas. Princípio do menor privilégio: filesystem server com acesso só ao diretório de docs, BD server com user read-only para operações de análise, read-write só quando necessário e restrito às tabelas relevantes.

> [!warning] Tratamento de erro no server determina a qualidade do loop agentic
> Se o seu MCP server lança exceções sem capturar, o agente vê um erro opaco e geralmente desiste ou tenta uma abordagem completamente diferente. Se o server retorna erros legíveis com `isError: true`, o agente consegue diagnosticar, ajustar e tentar novamente. A diferença entre `TypeError: Cannot read property 'count' of undefined` e `"Query failed: table 'users' does not exist in schema 'analytics'"` é a diferença entre um agente que para e um que continua.

> [!warning] "MCP para tudo" é over-engineering
> MCP tem overhead: inicializar o processo do server, manter a conexão, serializar/deserializar o protocolo. Para uma operação que você vai fazer uma vez, um script bash direto é mais eficiente. MCP vale quando: a integração é usada frequentemente, por múltiplos desenvolvedores, e o custo de manter o contexto manualmente é alto. Para automações one-shot, é over-engineering.

## Como explicar em inglês

| Português | Inglês técnico | Contexto de uso |
|-----------|---------------|----------------|
| Protocolo de contexto de modelo | Model Context Protocol | "MCP is the Model Context Protocol — an open standard for AI tool integration" |
| Servidor MCP | MCP server | "We built a custom MCP server for our legacy API" |
| Integração custom | Custom integration | "MCP eliminates the need for custom integrations between every agent and tool" |
| Primitivas do protocolo | Protocol primitives | "MCP has three primitives: tools, resources, and prompts" |
| Ferramenta (MCP) | Tool | "The agent invoked the execute_query tool from the Postgres MCP server" |
| Recurso (MCP) | Resource | "The API schema is exposed as an MCP resource so the agent can consult it" |
| Template de prompt | Prompt template | "We have a prompt template for PR analysis" |
| Transporte | Transport | "We use stdio transport for local servers and HTTP/SSE for shared cloud servers" |
| Menor privilégio | Least privilege | "Configure MCP servers with least privilege — read-only unless write is needed" |
| Prompt injection | Prompt injection | "Broad MCP permissions create a prompt injection attack surface" |
| Definição de tool | Tool definition | "Too many tool definitions dilute the context and reduce tool selection quality" |
| Ecossistema de servidores | Server ecosystem | "The MCP server ecosystem grew to 500+ servers by 2026" |

> [!tip] Frase de impacto para entrevistas
> *"MCP solved the N×M integration problem for AI agents. Before it, connecting an AI to your database meant writing a custom integration for every agent-tool pair. With MCP, you write the server once and it works with any compatible agent. Think of it as USB for AI tooling — a universal connector that lets the ecosystem grow in two directions independently."*

## O que vem a seguir

Em 2026, MCP ainda é relativamente jovem — lançado em novembro de 2024, com adoção acelerada em 2025-2026. A direção que o ecossistema está tomando:

**Servidores gerenciados na cloud:** em vez de cada desenvolvedor rodar o `server-postgres` localmente, o time mantém uma instância centralizada com autenticação e auditoria. O `mcp.json` aponta para o servidor remoto via HTTP/SSE. Isso resolve o problema de credenciais de produção no laptop de cada desenvolvedor.

**Composição de servers:** toolkits que permitem montar um "super-server" que agrega múltiplos sources — o agente vê uma lista de tools unificada sem precisar entender quantos servers estão por trás. Reduz o overhead de configuração para o usuário final.

**Autenticação federada:** integração com OAuth e sistemas de identidade corporativos — o `mcp.json` especifica o método de autenticação, o server obtém as permissões do usuário corrente automaticamente. Elimina o problema de tokens hardcoded nos arquivos de configuração.

**Descoberta de servers:** catálogos públicos e privados de MCP servers que o agente pode consultar dinamicamente — em vez de configurar manualmente, você diz "preciso acessar o Jira" e o agente encontra e configura o server apropriado. Análogo ao `npm install` mas para ferramentas de agentes.

A evolução que vale acompanhar é o movimento de MCP de "protocolo para desenvolvedores" para "infraestrutura invisível" — onde a maioria dos usuários não sabe que MCP existe, mas todos os agentes que usam se beneficiam da padronização.

**Sampling reverso:** uma das funcionalidades menos conhecidas do protocolo é a capacidade do server de fazer sampling requests de volta para o host — o server pode pedir ao modelo que processe algo e use o resultado. Isso abre a porta para servers que são eles mesmos "inteligentes": em vez de retornar dados brutos, o server pode pedir ao LLM que sumarize, classifique ou interprete os dados antes de devolvê-los. A arquitetura se torna bidirecional — não só o modelo chama ferramentas, mas as ferramentas podem "pedir ajuda" ao modelo.

**MCP em ambientes multi-agent:** quando múltiplos agentes trabalham em paralelo (padrão hierárquico ou em paralelo), a questão de compartilhamento de estado via MCP server torna-se relevante. Um MCP server com estado compartilhado (como um server que mantém um "todo list" da tarefa) permite que agentes coordenem sem precisar se comunicar diretamente. É a versão AI do "blackboard pattern" em sistemas multi-agente clássicos.

**Como decidir se vale criar um server custom vs usar um existente:** a heurística é simples. Primeiro verifique o catálogo (MCP Hub, Glama) — se existe um server mantido pela comunidade para a sua ferramenta, use-o. Criar um server custom tem custo de manutenção: você precisa atualizá-lo quando a API da ferramenta muda, gerenciar versões, garantir compatibilidade com novas versões do SDK. O server custom só vale quando a integração é tão específica ao seu sistema (API interna, sistema legado, lógica de negócio proprietária) que nenhum server genérico serve.

**Testando um MCP server antes de colocar em produção:** o cliente oficial de linha de comando `@modelcontextprotocol/inspector` permite testar um server interativamente sem precisar de um agente. Você chama tools, lista resources e verifica a saída — essencial para validar que o server se comporta como esperado antes de depender dele em sessões de desenvolvimento.

Falta ainda responder uma pergunta que este capítulo deixou em aberto: MCP dá ao agente um menu de ferramentas — mas quem decide, dentro de uma tarefa real, quando puxar qual ferramenta desse menu, e o que fazer com o resultado depois? Essa decisão não acontece no protocolo; acontece no loop que envolve o modelo. [[16 - O loop agentic — plan, act, observe]] é onde essa costura fica explícita: o agente planeja um passo, age (e "agir" muitas vezes significa invocar uma tool MCP), observa o resultado que voltou pelo client, e decide se já tem o suficiente ou se precisa de outra rodada. MCP resolve o "como conectar"; o loop agentic resolve o "quando e por quê".

## Veja também

- [[05 - Claude Code — terminal-first agent]] — como configurar MCP especificamente no Claude Code, incluindo permissões granulares por server
- [[16 - O loop agentic — plan, act, observe]] — como tool invocations via MCP se encaixam no loop agentic completo
- [[11 - Comparativo — qual ferramenta para qual tarefa]] — quais ferramentas suportam MCP em 2026
- [[14 - agents.md e configuração de projeto]] — configuração de projeto (CLAUDE.md) trabalha junto com a configuração de MCP servers
- [[12 - Multi-agent — workflows com múltiplos agentes]] — em multi-agent, diferentes agentes podem compartilhar acesso a MCP servers
- [[MCP]] — galho dedicado com os detalhes internos do protocolo: primitivas, arquitetura cliente-servidor, segurança e setup completo

## Referências

- **Anthropic** — *Model Context Protocol Specification* (2026). Spec oficial e documentação do protocolo, com referência de todas as primitivas. https://spec.modelcontextprotocol.io
- **ModelContextProtocol** — *GitHub Organization: SDK e servers oficiais* (2026). Repositório com SDK TypeScript/Python e servers oficiais (postgres, github, filesystem, etc.). https://github.com/modelcontextprotocol
- **MCP Hub** — *Server Directory* (2026). Catálogo comunitário de MCP servers disponíveis, com categorias e ratings. https://mcphub.io
- **Anthropic** — *Claude Code MCP Guide* (2026). Documentação específica de como configurar MCP no Claude Code, incluindo `mcp.json` e permissões. https://docs.anthropic.com/claude-code/mcp
- **Glama** — *MCP Server Registry* (2026). Registro alternativo com mais de 500 MCP servers categorizados por domínio. https://glama.ai/mcp/servers
- **ModelContextProtocol** — *MCP Inspector* (2026). Ferramenta de linha de comando para testar MCP servers interativamente antes de integrá-los ao agente. https://github.com/modelcontextprotocol/inspector
