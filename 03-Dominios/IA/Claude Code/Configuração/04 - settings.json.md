---
title: "settings.json — permissões, comportamentos, env vars"
type: concept
publish: true
created: 2026-05-13
updated: 2026-05-13
status: seedling
tags:
  - claude-code
  - configuracao
  - settings
  - permissions
---

# settings.json — permissões, comportamentos, env vars

> [!abstract] TL;DR
> `settings.json` é o arquivo de configuração estruturada do Claude Code — controla permissões (allow/deny de tools e comandos), comportamentos globais, variáveis de ambiente e hooks. Existe em três locais: global (`~/.claude/`), projeto (`.claude/`) e local (`.claude/settings.local.json`). A maioria dos projetos precisa no mínimo configurar permissões de Bash.

## O que é

Enquanto CLAUDE.md é texto livre (instrução em linguagem natural), `settings.json` é configuração estruturada em JSON. O que você define aqui é interpretado pelo Claude Code diretamente — não pelo modelo.

```json
// .claude/settings.json
{
  "permissions": {
    "allow": ["Bash(npm test)", "Bash(npm run lint)", "Edit(*)"],
    "deny": ["Bash(rm -rf *)"]
  }
}
```

## Campos principais

### `permissions`

Controla quais tools e comandos o agente pode executar sem pedir confirmação.

```json
{
  "permissions": {
    "allow": [
      "Bash(npm test)",
      "Bash(npm run *)",
      "Bash(git status)",
      "Bash(git log)",
      "Bash(git diff)",
      "Edit(*)",
      "Read(*)"
    ],
    "deny": [
      "Bash(rm -rf *)",
      "Bash(git push --force)",
      "Bash(DROP TABLE *)"
    ]
  }
}
```

Ver [[03-Dominios/IA/Claude Code/Configuração/05 - Permissions|05 - Permissions]] para sintaxe completa de allow/deny.

### `env`

Variáveis de ambiente disponíveis para o agente durante a sessão. Útil para apontar para ambientes de desenvolvimento.

```json
{
  "env": {
    "DATABASE_URL": "postgresql://localhost:5432/myapp_dev",
    "NODE_ENV": "development",
    "LOG_LEVEL": "debug"
  }
}
```

> [!warning] Segurança
> Nunca coloque secrets (API keys, passwords de produção) em `settings.json`. Esse arquivo vai para o git. Use `.claude/settings.local.json` (no .gitignore) para variáveis sensíveis locais.

### `hooks`

Configura scripts que rodam antes/depois de tool calls. Alternativa ao CLAUDE.md para hooks que precisam de execução (não só instrução textual).

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "scripts/validate-bash.sh"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "npm run lint -- --fix $FILE"
          }
        ]
      }
    ]
  }
}
```

Ver [[03-Dominios/IA/Claude Code/Hooks e Guardrails/index|Hooks e Guardrails]] para o sistema completo de hooks.

### `model`

Seleciona o modelo padrão para o projeto. Útil para forçar um modelo específico independente do default do usuário.

```json
{
  "model": "claude-sonnet-4-6"
}
```

### `includeCoAuthoredBy`

Controla se Claude adiciona Co-Authored-By em commits. Default: `true`.

```json
{
  "includeCoAuthoredBy": false
}
```

## Configuração mínima recomendada

Para a maioria dos projetos Node/TypeScript, um `settings.json` mínimo útil:

```json
{
  "permissions": {
    "allow": [
      "Bash(npm test)",
      "Bash(npm test -- *)",
      "Bash(npm run lint)",
      "Bash(npm run build)",
      "Bash(npm run dev)",
      "Bash(git status)",
      "Bash(git log)",
      "Bash(git diff)",
      "Bash(git add *)",
      "Bash(git commit *)"
    ],
    "deny": [
      "Bash(git push --force)",
      "Bash(rm -rf *)",
      "Bash(git reset --hard)"
    ]
  },
  "includeCoAuthoredBy": false
}
```

## Global vs projeto vs local

```
~/.claude/settings.json        → preferências pessoais (todos os projetos)
.claude/settings.json          → configurações do projeto (vai pro git, time inteiro)
.claude/settings.local.json    → sobrescritas pessoais (não vai pro git)
```

**Quando usar cada um:**

| Configuração | Onde |
|-------------|------|
| Ferramentas comuns a todos os projetos (`git status`, `ls`) | `~/.claude/settings.json` |
| Scripts específicos do projeto (`npm test`, `cargo build`) | `.claude/settings.json` |
| Variáveis de ambiente locais, paths pessoais | `.claude/settings.local.json` |
| Secrets para desenvolvimento local | `.claude/settings.local.json` |

## Armadilhas

**Nenhum allow configurado**: sem `allow`, cada Bash que o agente tenta rodar pede confirmação — include `git status`, `ls`, tudo. Lento e frustrante. Configure pelo menos os comandos básicos.

**Deny muito amplo**: `"deny": ["Bash(*)"]` bloqueia tudo. O agente fica preso. Deny deve ser cirúrgico — bloqueie o que é perigoso, não tudo.

**Secrets no settings.json**: o arquivo vai para o git. Use `settings.local.json` para qualquer coisa sensível.

**Esquecer o .gitignore**: se criar `settings.local.json`, adicione ao `.gitignore`. Do contrário o arquivo sensível entra no repositório.

## Veja também

- [[03-Dominios/IA/Claude Code/Configuração/05 - Permissions|05 - Permissions]] — sintaxe detalhada de allow/deny
- [[03-Dominios/IA/Claude Code/Configuração/01 - Hierarquia de configuração|01 - Hierarquia de configuração]] — como settings.json se combina entre camadas
- [[03-Dominios/IA/Claude Code/Hooks e Guardrails/index|Hooks e Guardrails]] — configuração de hooks em profundidade
- [[03-Dominios/IA/Claude Code/Configuração/index|Configuração]] — índice do galho

## Referências

- [Claude Code — Settings](https://docs.anthropic.com/pt/docs/claude-code/settings)
