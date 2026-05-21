---
title: "A pasta .claude — estrutura e propósito de cada arquivo"
type: concept
publish: true
created: 2026-05-13
updated: 2026-05-13
status: seedling
tags:
  - claude-code
  - configuracao
  - dotclaude
  - estrutura
---

# A pasta .claude — estrutura e propósito de cada arquivo

> [!abstract] TL;DR
> `.claude/` é o diretório de configuração do projeto para o Claude Code. Contém CLAUDE.md (contexto do projeto), settings.json (permissões e comportamentos), settings.local.json (sobrescritas pessoais, nunca vai ao git) e commands/ (slash commands customizados). Entender o papel de cada arquivo evita configuração no lugar errado.

## Estrutura completa

```
.claude/
├── CLAUDE.md              ← contexto do projeto (vai pro git)
├── settings.json          ← permissões e comportamentos (vai pro git)
├── settings.local.json    ← sobrescritas pessoais (NÃO vai pro git)
└── commands/              ← slash commands customizados (vai pro git)
    ├── review.md          → /review
    ├── pr-check.md        → /pr-check
    └── changelog.md       → /changelog
```

## Cada arquivo e seu propósito

### `CLAUDE.md`

**O que é:** Contexto do projeto em linguagem natural. Lido no início de cada sessão do Claude Code. Concatenado com `~/.claude/CLAUDE.md` (global).

**Contém:** Stack, arquitetura, convenções de código, comandos de desenvolvimento, restrições. O "onboarding doc" do agente para o projeto.

**Vai pro git?** Sim — é para o time inteiro. Todo dev que usar Claude Code no projeto recebe o mesmo contexto.

Ver [[03-Dominios/IA/Claude Code/Configuração/02 - CLAUDE.md anatomia|02 - CLAUDE.md anatomia]] para estrutura detalhada.

### `settings.json`

**O que é:** Configuração estruturada JSON. Controla permissões (allow/deny de tools), variáveis de ambiente, hooks, modelo padrão.

**Contém:**
```json
{
  "permissions": {
    "allow": ["Bash(npm test)", "Edit(*)"],
    "deny": ["Bash(git push --force*)"]
  },
  "env": {
    "NODE_ENV": "development"
  }
}
```

**Vai pro git?** Sim — define as regras do projeto que todo o time deve seguir.

Ver [[03-Dominios/IA/Claude Code/Configuração/04 - settings.json|04 - settings.json]] para todos os campos.

### `settings.local.json`

**O que é:** Sobrescritas pessoais do `settings.json` do projeto. Mesma estrutura, mas aplica apenas para você na sua máquina.

**Contém:** Variáveis de ambiente locais, paths pessoais, permissões temporárias para debugging, secrets de desenvolvimento.

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run dev:local)"
    ]
  },
  "env": {
    "DATABASE_URL": "postgresql://localhost:5432/myapp_dev_local",
    "JWT_SECRET": "dev-only-secret-nao-use-em-prod"
  }
}
```

**Vai pro git?** NUNCA. Adicione ao `.gitignore`.

**Por que existe:** separa configuração compartilhável de configuração pessoal/sensível sem precisar de dois arquivos com nomes diferentes.

### `commands/`

**O que é:** Pasta com arquivos Markdown que viram slash commands disponíveis no projeto.

**Contém:** Um arquivo `.md` por comando. O nome do arquivo (sem extensão) vira o `/comando`.

**Vai pro git?** Sim — os commands do projeto ficam disponíveis para todo o time.

Ver [[03-Dominios/IA/Claude Code/Configuração/06 - Slash commands customizados|06 - Slash commands customizados]] para como criar e usar.

## .gitignore recomendado

```gitignore
# Claude Code — sobrescritas pessoais
.claude/settings.local.json
```

Apenas `settings.local.json` fica fora do git. O resto (CLAUDE.md, settings.json, commands/) deve ser versionado.

## Onde mais o Claude Code lê configuração

A pasta `.claude/` do projeto é só uma camada. O Claude Code também lê:

```
~/.claude/
├── CLAUDE.md              ← preferências pessoais globais
├── settings.json          ← permissões globais
└── commands/              ← slash commands globais
```

Ver [[03-Dominios/IA/Claude Code/Configuração/01 - Hierarquia de configuração|01 - Hierarquia de configuração]] para como as camadas interagem.

## Montando do zero

Para um projeto novo, o mínimo útil:

```bash
mkdir -p .claude/commands

# 1. Crie o CLAUDE.md com contexto do projeto
touch .claude/CLAUDE.md

# 2. Crie settings.json com permissões básicas
touch .claude/settings.json

# 3. Adicione settings.local.json ao .gitignore
echo ".claude/settings.local.json" >> .gitignore
```

Conteúdo mínimo do `settings.json`:

```json
{
  "permissions": {
    "allow": [
      "Bash(npm test)",
      "Bash(npm test *)",
      "Bash(npm run *)",
      "Bash(git status)",
      "Bash(git log)",
      "Bash(git diff)",
      "Edit(*)",
      "Read(*)"
    ],
    "deny": [
      "Bash(git push --force*)",
      "Bash(rm -rf *)"
    ]
  }
}
```

## Armadilhas

**Secrets em settings.json**: vai pro git. Use `settings.local.json`.

**Esquecer de criar o .gitignore entry**: `settings.local.json` com credenciais entra no repositório silenciosamente.

**Commands com nomes de arquivos com espaços**: `deploy check.md` não funciona. Use kebab-case: `deploy-check.md`.

**CLAUDE.md na raiz do projeto (não em .claude/)**: também funciona — Claude Code lê tanto `CLAUDE.md` quanto `.claude/CLAUDE.md`. Mas misturar os dois no mesmo projeto cria redundância. Escolha um local e padronize.

## Veja também

- [[03-Dominios/IA/Claude Code/Configuração/01 - Hierarquia de configuração|01 - Hierarquia de configuração]] — contexto das camadas de configuração
- [[03-Dominios/IA/Claude Code/Configuração/02 - CLAUDE.md anatomia|02 - CLAUDE.md anatomia]] — o que colocar no CLAUDE.md
- [[03-Dominios/IA/Claude Code/Configuração/04 - settings.json|04 - settings.json]] — campos do settings.json
- [[03-Dominios/IA/Claude Code/Configuração/06 - Slash commands customizados|06 - Slash commands customizados]] — como criar commands
- [[03-Dominios/IA/Claude Code/Configuração/index|Configuração]] — índice do galho

## Referências

- [Claude Code — Configuration](https://docs.anthropic.com/pt/docs/claude-code/settings)
