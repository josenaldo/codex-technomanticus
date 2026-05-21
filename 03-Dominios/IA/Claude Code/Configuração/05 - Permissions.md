---
title: "Permissions — allow/deny, glob patterns, tool rules"
type: concept
publish: true
created: 2026-05-13
updated: 2026-05-13
status: seedling
tags:
  - claude-code
  - configuracao
  - permissions
  - settings
---

# Permissions — allow/deny, glob patterns, tool rules

> [!abstract] TL;DR
> Permissions controlam quais tool calls o Claude Code executa automaticamente vs. quais precisam de confirmação. A sintaxe é `"NomeTool(argumento)"` no array `allow` ou `deny` de `settings.json`. Glob patterns com `*` funcionam para caminhos e argumentos de Bash. Deny sempre prevalece sobre allow.

## O que é

Sem permissão configurada, cada tool call que o agente tenta fazer exige confirmação manual. Com permissões, você define quais ações são seguras o suficiente para rodar automaticamente — e quais jamais devem rodar sem revisão humana.

```json
{
  "permissions": {
    "allow": ["Bash(npm test)", "Edit(*)"],
    "deny": ["Bash(rm -rf *)"]
  }
}
```

## Sintaxe geral

```
"NomeTool(padrão)"
```

- **NomeTool**: nome exato da tool (`Bash`, `Edit`, `Read`, `Write`, `WebFetch`, `WebSearch`, etc.)
- **padrão**: string que é comparada com o argumento da tool call

Para permitir uma tool sem restrição de argumento:

```json
"Read(*)"   // Qualquer leitura de arquivo
"Edit(*)"   // Qualquer edição de arquivo
```

## Bash — padrões de comando

Bash é a tool mais crítica de configurar, porque engloba todos os comandos shell.

### Comandos exatos

```json
"Bash(npm test)"           // Apenas 'npm test' — não permite variações
"Bash(git status)"
"Bash(ls -la)"
```

### Glob com `*`

```json
"Bash(npm test *)"         // npm test e qualquer argumento depois
"Bash(npm run *)"          // qualquer npm run <script>
"Bash(git *)"              // qualquer subcomando git
"Bash(docker * ps)"        // docker <algo> ps
```

> [!warning] Cuidado com globs amplos
> `"Bash(git *)"` permite `git push --force`. Prefira listar os subcomandos específicos que você realmente usa.

### Prefixo de comando

O padrão é verificado como **prefixo** da string do comando. `"Bash(npm run)"` permite `npm run lint`, `npm run build`, `npm run test:watch`.

## Read/Edit/Write — padrões de caminho

Para tools de arquivo, o padrão é comparado com o caminho do arquivo.

```json
"Read(*)"                  // Qualquer arquivo
"Edit(*)"                  // Qualquer arquivo
"Edit(src/*)"              // Apenas arquivos em src/
"Edit(src/**/*.ts)"        // TypeScript em qualquer subpasta de src/
"Write(tests/*)"           // Escrever apenas em tests/
```

## WebFetch e WebSearch

```json
"WebFetch(*)"              // Qualquer URL
"WebFetch(https://docs.anthropic.com/*)"  // Apenas domínio específico
"WebSearch(*)"             // Qualquer pesquisa
```

## Deny sempre prevalece

Se um padrão está em `deny`, ele bloqueia mesmo que esteja em `allow`:

```json
{
  "permissions": {
    "allow": ["Bash(git *)"],        // permite qualquer git
    "deny": ["Bash(git push *)"]     // mas bloqueia push — PREVALECE
  }
}
```

Resultado: todos os git commands são permitidos, exceto push (qualquer variação).

## Permissões por camada

As permissões do `settings.json` se combinam entre camadas (global + projeto + local) por **união**:

```
~/.claude/settings.json:    allow: ["Bash(git status)", "Bash(git log)"]
.claude/settings.json:      allow: ["Bash(npm test)"], deny: ["Bash(rm -rf *)"]

Resultado:
  allow: ["Bash(git status)", "Bash(git log)", "Bash(npm test)"]
  deny: ["Bash(rm -rf *)"]
```

> [!info] Nota sobre merge de camadas
> A documentação oficial indica que as camadas mais específicas sobrescrevem as mais gerais para `settings.json`. Na prática, para `permissions.allow`, o comportamento observado é de acumulação. Para evitar surpresas, liste explicitamente em cada camada o que você precisa.

## Configuração recomendada por tipo de projeto

### Qualquer projeto (global)

```json
// ~/.claude/settings.json
{
  "permissions": {
    "allow": [
      "Bash(git status)",
      "Bash(git log)",
      "Bash(git log *)",
      "Bash(git diff)",
      "Bash(git diff *)",
      "Bash(git add *)",
      "Bash(git commit *)",
      "Bash(ls)",
      "Bash(ls *)",
      "Bash(cat *)",
      "Bash(find *)",
      "Read(*)",
      "Edit(*)"
    ],
    "deny": [
      "Bash(git push --force*)",
      "Bash(git reset --hard*)",
      "Bash(rm -rf *)",
      "Bash(sudo *)"
    ]
  }
}
```

### Projeto Node.js (projeto)

```json
// .claude/settings.json
{
  "permissions": {
    "allow": [
      "Bash(npm test)",
      "Bash(npm test *)",
      "Bash(npm run *)",
      "Bash(npm install *)",
      "Bash(npx *)"
    ],
    "deny": [
      "Bash(npm publish*)"
    ]
  }
}
```

### Projeto Python (projeto)

```json
// .claude/settings.json
{
  "permissions": {
    "allow": [
      "Bash(pytest)",
      "Bash(pytest *)",
      "Bash(ruff check *)",
      "Bash(ruff format *)",
      "Bash(python *)",
      "Bash(pip install *)"
    ]
  }
}
```

## Armadilhas

**Sem nenhum allow configurado**: cada tool call pede confirmação. Inclua pelo menos `Read(*)`, `Edit(*)`, `Bash(git status)` para sessões produtivas.

**Deny em `Bash(*)` bloqueia tudo**: `"deny": ["Bash(*)"]` — o agente não consegue rodar absolutamente nada. Deny deve ser cirúrgico.

**Glob muito amplo no allow**: `"Bash(*)"` permite que o agente rode qualquer comando, incluindo destrutivos. Prefira listas explícitas de prefixos seguros.

**Esquecer variações**: `"Bash(npm test)"` não cobre `npm test -- --watch`. Adicione `"Bash(npm test *)"` para cobrir argumentos extras.

## Veja também

- [[03-Dominios/IA/Claude Code/Configuração/04 - settings.json|04 - settings.json]] — contexto de onde permissions se encaixam
- [[03-Dominios/IA/Claude Code/Configuração/01 - Hierarquia de configuração|01 - Hierarquia de configuração]] — como permissões se combinam entre camadas
- [[03-Dominios/IA/Claude Code/Configuração/08 - Armadilhas de configuração|08 - Armadilhas de configuração]] — erros comuns de configuração
- [[03-Dominios/IA/Claude Code/Configuração/index|Configuração]] — índice do galho

## Referências

- [Claude Code — Settings](https://docs.anthropic.com/pt/docs/claude-code/settings)
