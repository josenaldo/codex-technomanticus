---
title: "Compondo skills e MCP — agentes especializados"
type: concept
publish: true
created: 2026-05-13
updated: 2026-05-13
status: seedling
tags:
  - claude-code
  - skills
  - mcp
  - composicao
  - agentes
---

# Compondo skills e MCP — agentes especializados

> [!abstract] TL;DR
> Skills e MCP servers são complementares: skills ensinam o agente *como* trabalhar; MCP servers dão ao agente *acesso* ao que ele precisa para trabalhar. Um agente especializado para um domínio específico combina as duas coisas: uma skill que define o processo e os MCP servers que expõem os sistemas necessários. A composição acontece na sessão, não em código.

## Por que compor em vez de usar separado

Só com skill: o agente sabe o processo mas não consegue acessar os sistemas externos — precisa pedir para você executar comandos.

Só com MCP: o agente tem acesso aos sistemas mas vai tomar decisões genéricas — vai rodar queries que não seguem os padrões do projeto, criar issues no formato errado.

Combinado: o agente tem contexto específico do domínio (skill) e acesso autônomo aos sistemas (MCP) — pode executar workflows completos sem intermediário.

## Padrão de composição

Uma sessão de agente especializado tem três componentes:

```
1. Skill de domínio    → "O que é este projeto, quais são as regras"
2. Skill de processo   → "Como fazer esta tarefa aqui"
3. MCP server(s)       → Acesso aos sistemas externos necessários
```

Exemplo: agente de triagem de bugs

```
/convencoes-projeto      ← skill de domínio: estrutura do projeto, convenções
/bug-triage              ← skill de processo: como investigar e priorizar bugs
                         ← MCP postgres: consultar tabela de logs
                         ← MCP github: criar issues, ler issues abertas
```

## Exemplo completo: agente de deploy

**Configuração MCP** em `settings.json`:

```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": { "DATABASE_URL": "${DATABASE_URL_STAGING}" }
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}" }
    }
  }
}
```

**Skill de processo** em `.claude/skills/deploy-checklist.md`:

```markdown
---
name: deploy-checklist
description: Guia o agente pelo checklist de deploy para staging — verifica PRs, banco, e notifica time
metadata:
  type: process
  tags: [deploy, staging, checklist]
---

# Deploy para Staging — Checklist

## Antes de deployar

1. Verificar se há PRs abertos que precisam estar neste deploy
   - Listar PRs mesclados desde o último deploy
   - Confirmar que todos estão marcados como "ready for staging"

2. Verificar banco de dados
   - Checar se há migrations pendentes (`SELECT * FROM migrations WHERE applied_at IS NULL`)
   - Se houver migration, confirmar que foi testada localmente

3. Executar deploy
   - Rodar `npm run deploy:staging`
   - Aguardar confirmação de sucesso

## Após o deploy

4. Smoke test
   - Verificar endpoints críticos na URL de staging

5. Criar issue de tracking
   - Criar issue no GitHub com: lista de PRs incluídos, migrations aplicadas, resultado dos smoke tests
```

**Invocação na sessão**:

```
/deploy-checklist
Estamos deployando para staging a branch release/2.4.0
```

O agente:
1. Lê a skill e segue o processo
2. Usa `list_pull_requests` (GitHub MCP) para buscar PRs prontos
3. Usa `query` (Postgres MCP) para verificar migrations pendentes
4. Cria issue de tracking no GitHub com `create_issue`

## Exemplo completo: agente de onboarding de feature

**Skills**:
- `/arquitetura-projeto` — skill de domínio com mapa de módulos
- `/tdd` — skill de processo para desenvolvimento orientado a testes

**MCP servers**:
- Postgres — verificar schema enquanto implementa
- GitHub — ler issue com requisitos da feature, criar PR ao final

**Sessão**:

```
/arquitetura-projeto
/tdd
Implementa a feature descrita na issue #247
```

O agente lê a issue (#247 via GitHub MCP), verifica o schema das tabelas envolvidas (Postgres MCP), segue o processo TDD da skill, e ao final cria o PR (GitHub MCP) com referência à issue.

## Skill que instrui uso de MCP

Você pode incluir na skill instrução explícita sobre quais tools MCP usar:

```markdown
---
name: review-migration
description: Revisa uma migration de banco — analisa impacto, testa em staging, documenta
---

# Review de Migration

## Passos

1. Ler a migration em `db/migrations/` mais recente
2. Usar `describe_table` (MCP postgres-staging) para ver estado atual da tabela
3. Rodar a migration em staging: `npm run migrate:staging`
4. Usar `query` (MCP postgres-staging) para verificar que a estrutura ficou correta
5. Documentar no PR: impacto da migration, rollback procedure
```

A referência explícita a "MCP postgres-staging" remove ambiguidade quando há múltiplos servers com tools de mesmo nome.

## Quando a composição não é necessária

Nem toda tarefa precisa de composição completa. Use o mínimo necessário:

| Tarefa | O que é suficiente |
|--------|-------------------|
| Implementar uma função nova | Só o código + tools nativas |
| Refatorar código existente | Skills de processo (TDD, review) |
| Investigar bug em produção | MCP postgres (logs) + skill de debugging |
| Feature com requisito em issue | MCP github + skill de domínio |
| Deploy com checklist | Skill de processo + MCP de monitoramento |

Adicionar MCP servers sem necessidade aumenta a superfície de ataque e o overhead de cada sessão.

## Armadilhas

**Skill que descreve o processo sem instrução sobre os sistemas**: "verifique o banco" sem especificar qual tool MCP usar leva o agente a tentar acesso via Bash — que pode estar bloqueado por guardrails.

**MCP server de produção com skill que permite mutações**: uma skill de "atualizar dados" + MCP de produção é uma combinação perigosa. Garanta que o MCP server aponta para o ambiente certo para o workflow da skill.

**Muitas skills na mesma sessão**: o agente tenta reconciliar todas. Três skills simultâneas com instruções conflitantes criam comportamento imprevisível. Prefira skills focadas e combine no máximo duas por sessão.

**Skill que assume que MCP está disponível**: se a skill instrui o agente a usar uma tool que não está configurada, o agente vai falhar com erro obscuro. Documente na skill quais MCP servers são necessários.

## Documentar a composição

Para workflows que o time vai repetir, documente a composição no `CLAUDE.md` do projeto:

```markdown
## Workflows disponíveis

### Deploy para staging
Requer: MCP `postgres-staging`, MCP `github`
Invoke: `/deploy-checklist`

### Triagem de bugs
Requer: MCP `postgres-prod` (read-only), MCP `github`
Invoke: `/convencoes-projeto` + `/bug-triage`
```

Isso garante que qualquer dev do time sabe o que configurar antes de usar os workflows.

## Veja também

- [[03-Dominios/IA/Claude Code/Skills e MCP/01 - Anatomia de uma skill|01 - Anatomia de uma skill]] — estrutura de skills
- [[03-Dominios/IA/Claude Code/Skills e MCP/04 - MCP overview|04 - MCP overview]] — arquitetura MCP
- [[03-Dominios/IA/Claude Code/Skills e MCP/05 - MCP servers essenciais|05 - MCP servers essenciais]] — servers prontos para usar
- [[03-Dominios/IA/Claude Code/Skills e MCP/06 - Criar MCP server|06 - Criar MCP server]] — criar server para sistemas internos
- [[03-Dominios/IA/Claude Code/Skills e MCP/08 - Skills em time|08 - Skills em time]] — versionar e manter skills em equipe
- [[03-Dominios/IA/Claude Code/Skills e MCP/index|Skills e MCP]] — índice do galho
