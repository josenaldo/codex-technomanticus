---
title: "Armadilhas de configuração — o que dá errado e como evitar"
type: concept
publish: true
created: 2026-05-13
updated: 2026-05-13
status: seedling
tags:
  - claude-code
  - configuracao
  - armadilhas
  - troubleshooting
---

# Armadilhas de configuração — o que dá errado e como evitar

> [!abstract] TL;DR
> Os erros de configuração mais comuns do Claude Code se dividem em três categorias: permissões erradas (o agente para a cada passo, ou faz coisas perigosas sem perguntar), CLAUDE.md ineficaz (contexto ausente ou confuso), e problemas de segurança (secrets no git). Este note documenta cada armadilha com diagnóstico e solução.

## Armadilhas de permissão

### 1. Sem `allow` configurado — confirmação em tudo

**Sintoma**: o agente pede confirmação para `git status`, `ls`, leitura de arquivos. Sessão lenta e frustrante.

**Causa**: nenhum `allow` no `settings.json`.

**Fix**:
```json
{
  "permissions": {
    "allow": [
      "Read(*)",
      "Edit(*)",
      "Bash(git status)",
      "Bash(git log)",
      "Bash(git diff)",
      "Bash(ls)",
      "Bash(ls *)"
    ]
  }
}
```

---

### 2. `allow` muito amplo — agente faz coisas perigosas automaticamente

**Sintoma**: o agente faz `git push --force`, deleta arquivos, modifica branches de produção sem pedir confirmação.

**Causa**: `"Bash(git *)"` ou `"Bash(*)"` no allow.

**Fix**: liste comandos específicos; use deny para os perigosos:
```json
{
  "permissions": {
    "allow": [
      "Bash(git status)",
      "Bash(git log)",
      "Bash(git diff)",
      "Bash(git add *)",
      "Bash(git commit *)"
    ],
    "deny": [
      "Bash(git push --force*)",
      "Bash(git reset --hard*)",
      "Bash(git push origin main*)"
    ]
  }
}
```

---

### 3. `deny` bloqueia tudo — agente travado

**Sintoma**: o agente não consegue executar nada, mesmo ações básicas.

**Causa**: `"deny": ["Bash(*)"]` ou deny muito abrangente.

**Fix**: deny deve ser cirúrgico. Bloqueie ações específicas perigosas, não categorias inteiras.

---

### 4. Esquecer variações do comando

**Sintoma**: `npm test` funciona automaticamente, mas `npm test -- --watch` pede confirmação.

**Causa**: `"Bash(npm test)"` cobre apenas o comando exato, não variações com argumentos.

**Fix**:
```json
"Bash(npm test)",
"Bash(npm test *)"
```

---

### 5. Confundir merge de settings entre camadas

**Sintoma**: as permissões do `~/.claude/settings.json` global parecem ignoradas no projeto.

**Causa**: entender que settings.json "concatena" como CLAUDE.md. Na prática, camadas mais específicas sobrescrevem — se o projeto define `allow`, isso pode suprimir o allow global.

**Fix**: declare explicitamente em cada camada o que você precisa, ou inclua tudo no global e só acrescente no projeto:
```json
// .claude/settings.json — inclua os basics do global explicitamente
{
  "permissions": {
    "allow": [
      "Bash(git status)",   // repete do global para garantir
      "Bash(npm test)"      // específico do projeto
    ]
  }
}
```

---

## Armadilhas de CLAUDE.md

### 6. CLAUDE.md vazio ou inexistente

**Sintoma**: o agente usa `console.log` em vez do logger do projeto, instala libs duplicadas, segue convenções genéricas em vez das do projeto.

**Causa**: sem CLAUDE.md, o agente age com suposições genéricas.

**Fix**: crie `.claude/CLAUDE.md` com pelo menos: stack, comandos de teste, e a seção `## Restrições`. Ver [[03-Dominios/IA/Claude Code/Configuração/02 - CLAUDE.md anatomia|02 - CLAUDE.md anatomia]].

---

### 7. CLAUDE.md desatualizado

**Sintoma**: o agente usa Mongoose quando o projeto migrou para Prisma. Referencia arquivos que foram movidos.

**Causa**: o CLAUDE.md não foi atualizado quando a stack mudou.

**Fix**: trate o CLAUDE.md como parte da definição de done ao mudar a stack. Adicione ao checklist de migração/PR.

---

### 8. Placeholders `[...]` não preenchidos

**Sintoma**: o agente se comporta de forma inconsistente ou faz perguntas básicas que deveria saber.

**Causa**: usou template de CLAUDE.md mas não substituiu os campos marcados com `[...]`.

**Fix**: preencha todos os campos ou remova a seção. Um CLAUDE.md incompleto confunde mais do que nenhum.

---

### 9. Regras sem contexto

**Sintoma**: o agente segue a regra literalmente em casos onde não deveria se aplicar.

**Causa**: "não use `any`" sem explicar por quê — o agente não sabe quando o edge case justifica uma exceção.

**Fix**: adicione o motivo:
```markdown
## Restrições

- Não use `any` em TypeScript — use `unknown` com type guard.
  Razão: tivemos bugs de produção por tipagem solta. Exceção permitida
  apenas em testes de integração onde o tipo externo é genuinamente
  desconhecido.
```

---

## Armadilhas de segurança

### 10. Secrets em `settings.json`

**Sintoma**: API keys, passwords de banco de dados no repositório git.

**Causa**: `settings.json` vai pro git — qualquer coisa em `env` fica exposta.

**Fix**: use `settings.local.json` para secrets:
```json
// .claude/settings.local.json (adicionar ao .gitignore)
{
  "env": {
    "DATABASE_URL": "postgresql://user:senha@localhost/dev",
    "JWT_SECRET": "dev-secret"
  }
}
```

---

### 11. `settings.local.json` no git

**Sintoma**: arquivo com secrets aparece no git history.

**Causa**: esqueceu de adicionar ao `.gitignore`.

**Fix**:
```bash
echo ".claude/settings.local.json" >> .gitignore
# Se já foi commitado:
git rm --cached .claude/settings.local.json
```

---

## Diagnóstico rápido

| Problema | Primeira coisa a checar |
|----------|------------------------|
| Agente pede confirmação em tudo | `settings.json` tem `allow`? |
| Agente faz ações perigosas sem perguntar | `allow` tem glob muito amplo? |
| Agente usa convenções erradas | `CLAUDE.md` existe e está atualizado? |
| Permissões globais ignoradas no projeto | Camada do projeto está sobrescrevendo? |
| Secrets no git | `settings.local.json` no `.gitignore`? |

## Veja também

- [[03-Dominios/IA/Claude Code/Configuração/01 - Hierarquia de configuração|01 - Hierarquia de configuração]] — como as camadas interagem
- [[03-Dominios/IA/Claude Code/Configuração/04 - settings.json|04 - settings.json]] — referência de campos
- [[03-Dominios/IA/Claude Code/Configuração/05 - Permissions|05 - Permissions]] — sintaxe detalhada de allow/deny
- [[03-Dominios/IA/Claude Code/Configuração/07 - Pasta .claude|07 - Pasta .claude]] — o que vai no git e o que não vai
- [[03-Dominios/IA/Claude Code/Configuração/index|Configuração]] — índice do galho
