---
title: "MCP servers essenciais — postgres, github, filesystem, browser"
type: concept
publish: true
created: 2026-05-13
updated: 2026-05-13
status: seedling
tags:
  - claude-code
  - mcp
  - postgres
  - github
  - browser
  - servidores
---

# MCP servers essenciais — postgres, github, filesystem, browser

> [!abstract] TL;DR
> Anthropic e a comunidade mantêm MCP servers prontos para os casos de uso mais comuns. Para o dev típico, quatro servers cobrem quase tudo: postgres para banco de dados, github para repositórios e issues, filesystem para acesso granular a arquivos, e puppeteer/playwright para automação de browser. Esta nota cobre configuração e quando usar cada um.

## @modelcontextprotocol/server-postgres

**Para que serve**: rodar queries SQL diretas no banco a partir do Claude Code, sem precisar de terminal.

**Instalação**: não precisa instalar globalmente — o `npx` busca na primeira invocação.

**Configuração em settings.json**:

```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "DATABASE_URL": "${DATABASE_URL}"
      }
    }
  }
}
```

**Tools expostas**:

- `query(sql)` — executa SELECT, retorna rows
- `execute(sql)` — executa INSERT, UPDATE, DELETE
- `list_tables()` — lista tabelas do schema
- `describe_table(table)` — retorna estrutura da tabela

**Quando usar**:
- Explorar schema enquanto escreve código de acesso a dados
- Verificar dados de teste sem abrir cliente SQL
- Debugar queries que a aplicação está gerando

> [!warning]
> Nunca aponte para banco de produção. O agente pode rodar `DROP TABLE`, `TRUNCATE`, ou `DELETE` sem WHERE sem perceber. Use sempre banco de desenvolvimento local ou staging isolado.

## @modelcontextprotocol/server-github

**Para que serve**: criar issues, ler PRs, buscar código em repositórios do GitHub diretamente do Claude Code.

**Pré-requisito**: um GitHub Personal Access Token com escopos `repo` e `read:org`.

**Configuração**:

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_PERSONAL_ACCESS_TOKEN}"
      }
    }
  }
}
```

**Tools expostas**:

- `create_issue(owner, repo, title, body)` — cria issue
- `get_issue(owner, repo, issue_number)` — lê issue com comentários
- `list_pull_requests(owner, repo)` — lista PRs abertos
- `get_pull_request(owner, repo, pr_number)` — lê PR e diff
- `search_code(query, owner, repo)` — busca código nos repositórios
- `create_pull_request(owner, repo, title, body, head, base)` — cria PR

**Quando usar**:
- Criar issues enquanto identifica bugs no código
- Ler contexto de issues para implementar features
- Buscar como algo é feito em outro repo da organização
- Criar PRs sem sair do Claude Code

## @modelcontextprotocol/server-filesystem

**Para que serve**: acesso mais granular ao filesystem com controle de quais diretórios o agente pode tocar.

**Configuração**:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/home/user/projects/meu-projeto",
        "/tmp/outputs"
      ]
    }
  }
}
```

Os argumentos após o nome do package são os diretórios permitidos. O server recusa acesso a qualquer caminho fora dos listados.

**Tools expostas**:

- `read_file(path)` — lê arquivo
- `write_file(path, content)` — escreve arquivo
- `list_directory(path)` — lista conteúdo
- `create_directory(path)` — cria diretório
- `move_file(source, destination)` — move arquivo
- `search_files(path, pattern)` — busca por padrão

**Quando usar em relação às tools nativas**:

| Cenário | Tool nativa | MCP filesystem |
|---------|-------------|----------------|
| Editar um arquivo | `Edit` | Overhead desnecessário |
| Restringir acesso a subpasta | Não possível | Use filesystem MCP |
| Gerar arquivos em `/tmp` | `Write` | Mesmo |
| Isolar acesso do agente | Não possível | Configure diretórios |

Para projetos normais, as tools nativas (`Read`, `Write`, `Edit`) são suficientes. O MCP filesystem é útil quando você quer restringir o agente a um subconjunto do filesystem por política.

## @modelcontextprotocol/server-puppeteer

**Para que serve**: automação de browser — navegar, clicar, preencher formulários, tirar screenshots, extrair conteúdo.

**Pré-requisito**: Chrome ou Chromium instalado no sistema.

**Configuração**:

```json
{
  "mcpServers": {
    "puppeteer": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-puppeteer"]
    }
  }
}
```

**Tools expostas**:

- `puppeteer_navigate(url)` — navega para URL
- `puppeteer_screenshot(name)` — captura screenshot
- `puppeteer_click(selector)` — clica em elemento
- `puppeteer_fill(selector, value)` — preenche campo
- `puppeteer_evaluate(script)` — executa JavaScript na página
- `puppeteer_select(selector, value)` — seleciona opção em `<select>`
- `puppeteer_hover(selector)` — hover em elemento
- `puppeteer_content()` — retorna HTML da página atual

**Quando usar**:
- Testar fluxos de UI enquanto desenvolve frontend
- Tirar screenshot para verificar se uma mudança de CSS ficou certa
- Scraping de documentação durante desenvolvimento
- Verificar se a aplicação sobe corretamente depois de um build

**Exemplo de uso em sessão**:

```
puppeteer_navigate("http://localhost:3000/login")
puppeteer_fill("#email", "test@example.com")
puppeteer_fill("#password", "senha123")
puppeteer_click("[type='submit']")
puppeteer_screenshot("after-login")
```

O agente vê o screenshot e pode reportar o que encontrou na tela.

## Combinando servers numa sessão

Você pode ter múltiplos servers ativos simultaneamente:

```json
{
  "mcpServers": {
    "postgres": { ... },
    "github": { ... },
    "puppeteer": { ... }
  }
}
```

O agente escolhe qual tool usar dependendo do contexto. Para implementar uma feature:

1. Lê a issue no GitHub (`get_issue`)
2. Verifica o schema do banco (`describe_table`)
3. Implementa o código
4. Testa a UI no browser (`puppeteer_navigate` + `puppeteer_screenshot`)
5. Cria o PR (`create_pull_request`)

Tudo em uma sessão contínua sem sair do Claude Code.

## Verificar servers disponíveis na sessão

```
/mcp
```

Lista os MCP servers configurados e as tools que cada um expõe. Útil para confirmar que o server iniciou corretamente.

## Armadilhas

**Server que não inicia**: verifique se `npx` consegue baixar o package. Em ambientes sem internet, pré-instale os packages com `npm install -g @modelcontextprotocol/server-postgres`.

**Variáveis de ambiente não resolvidas**: `${GITHUB_PERSONAL_ACCESS_TOKEN}` só é resolvido se a variável estiver exportada no shell onde o Claude Code inicia. Adicione ao `.bashrc` ou `.zshrc`, não só ao `.env` do projeto.

**Dois servers com tools de mesmo nome**: se dois MCP servers expõem uma tool chamada `query`, o agente pode chamar a errada. Prefixe os nomes dos servers para facilitar o rastreamento: `postgres-dev`, `postgres-staging`.

## Veja também

- [[03-Dominios/IA/Claude Code/Skills e MCP/04 - MCP overview|04 - MCP overview]] — arquitetura e conceitos do protocolo
- [[03-Dominios/IA/Claude Code/Skills e MCP/06 - Criar MCP server|06 - Criar MCP server]] — quando criar um server customizado
- [[03-Dominios/IA/Claude Code/Configuração/04 - settings.json|04 - settings.json]] — configuração completa de MCP
- [[03-Dominios/IA/Claude Code/Skills e MCP/index|Skills e MCP]] — índice do galho
