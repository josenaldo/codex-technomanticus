---
title: "Criar sua primeira skill — walkthrough prático"
type: concept
publish: true
created: 2026-05-13
updated: 2026-05-13
status: seedling
tags:
  - claude-code
  - skills
  - walkthrough
  - criacao
  - pratico
---

# Criar sua primeira skill — walkthrough prático

> [!abstract] TL;DR
> O walkthrough mais útil é criar uma skill para um processo que você já executa manualmente. Escolha algo repetitivo: code review, deploy checklist, ou como você quer que o agente aborde testes no projeto. Este guia cria uma skill de code review do zero, passo a passo, e explica cada decisão.

## Escolha o processo certo para começar

A melhor primeira skill é aquela que você já sabe de cor. Se você precisa inventar o processo enquanto cria a skill, o resultado vai ser genérico demais.

Bons candidatos para primeira skill:
- Code review que você já faz mentalmente antes de mergear
- Checklist de deploy que você consulta num Notion ou README
- Processo de debugging que você aprendeu com incidentes passados
- Convenções do projeto que você sempre explica para novos devs

Para este walkthrough: skill de code review para TypeScript com foco em segurança.

## Passo 1: Escrever o processo em linguagem natural

Antes de criar o arquivo, escreva o que você faria manualmente:

> Quando reviso código TypeScript, eu verifico: tipos explícitos em funções públicas, ausência de `any`, ausência de console.log no código de produção, tratamento de erros em chamadas assíncronas, testes para o caminho feliz e para erros. Se encontro algum problema, anoto com o nível de severidade (bloqueador, importante, sugestão).

Esse texto já é quase a skill. Você só precisa estruturá-lo.

## Passo 2: Criar o arquivo

```bash
mkdir -p .claude/skills
```

```bash
# .claude/skills/code-review-ts.md
```

## Passo 3: Escrever o frontmatter

```markdown
---
name: code-review-ts
description: Revisa código TypeScript — tipos, segurança, tratamento de erros, testes
metadata:
  type: process
  tags: [code-review, typescript, seguranca]
---
```

O `description` é o campo mais importante para o agente encontrar a skill quando ela é relevante. Seja específico.

## Passo 4: Escrever o corpo

```markdown
# Code Review — TypeScript

## O que verificar (em ordem)

### 1. Tipos e TypeScript

- [ ] Funções públicas têm tipos explícitos de retorno?
- [ ] Parâmetros de função têm tipos declarados?
- [ ] Ausência de `any` (exceto em testes e stubs documentados)?
- [ ] Tipos utilitários usados corretamente (Partial, Required, Pick, Omit)?

### 2. Tratamento de erros

- [ ] Chamadas async/await têm try/catch ou `.catch()`?
- [ ] Erros são tratados ou propagados explicitamente — nunca silenciados?
- [ ] HTTP requests verificam status code antes de usar o body?

### 3. Segurança básica

- [ ] Input de usuário é validado antes de usar?
- [ ] Nenhum `console.log` em código de produção?
- [ ] Sem segredos hardcoded (senhas, API keys, tokens)?

### 4. Testes

- [ ] Há testes para o caminho feliz?
- [ ] Há testes para pelo menos um caso de erro?
- [ ] Testes são independentes entre si (sem estado compartilhado)?

## Como reportar

Use estes níveis:

**Bloqueador**: impede o merge. Ex: segredo hardcoded, acesso sem autenticação.

**Importante**: deve ser corrigido antes do merge, mas pode ser corrigido no PR. Ex: falta de tratamento de erro em path crítico.

**Sugestão**: melhoria não-bloqueadora. Ex: nome de variável mais descritivo.

## Formato de saída

Para cada problema encontrado:
```
[BLOQUEADOR] src/auth/login.ts:47 — senha hardcoded "admin123"
[IMPORTANTE] src/api/orders.ts:23 — chamada async sem try/catch
[SUGESTÃO] src/utils/format.ts:8 — considerar renomear `d` para `date`
```

Ao final, um sumário:
```
Resultado: 1 bloqueador, 1 importante, 1 sugestão. Não pronto para merge.
```
```

## Passo 5: Testar a skill

Abra o Claude Code no projeto e invoque:
```
/code-review-ts
Revise o arquivo src/auth/login.ts
```

Observe se o agente:
- Segue as categorias na ordem definida
- Reporta no formato especificado
- Usa os níveis de severidade corretamente

## Passo 6: Iterar

Após o primeiro uso real, você vai perceber gaps. Coisas comuns a ajustar:

- "O agente não verificou X" → adicione X ao checklist
- "O agente demorou muito em Y" → Y provavelmente não precisa estar na skill
- "O formato de saída ficou diferente" → adicione um exemplo mais explícito no body
- "O agente ignorou a regra Z" → coloque Z em negrito ou num callout `> [!warning]`

## O arquivo final

```markdown
---
name: code-review-ts
description: Revisa código TypeScript — tipos, segurança, tratamento de erros, testes
metadata:
  type: process
  tags: [code-review, typescript, seguranca]
---

# Code Review — TypeScript

## O que verificar (em ordem)

### 1. Tipos e TypeScript
- [ ] Funções públicas têm tipos explícitos de retorno?
- [ ] Parâmetros de função têm tipos declarados?
- [ ] Ausência de `any` (exceto em testes e stubs documentados)?

### 2. Tratamento de erros
- [ ] Chamadas async/await têm try/catch ou `.catch()`?
- [ ] Erros não são silenciados?
- [ ] HTTP requests verificam status code antes de usar o body?

### 3. Segurança
- [ ] Input de usuário é validado?
- [ ] Sem `console.log` em produção?
- [ ] Sem segredos hardcoded?

### 4. Testes
- [ ] Há testes para o caminho feliz?
- [ ] Há testes para pelo menos um caso de erro?

## Como reportar

**Bloqueador**: impede o merge.
**Importante**: deve ser corrigido no PR.
**Sugestão**: melhoria não-bloqueadora.

Formato: `[NÍVEL] arquivo:linha — descrição`
```

## Armadilhas

**Skill com tudo que você sabe sobre code review**: resulta em um documento enorme que o agente lê mas não consegue seguir completamente. Priorize os 20% que cobrem 80% dos problemas reais que você encontra.

**Instruções sem exemplos de output**: o agente interpreta o formato de saída de forma criativa. Sempre inclua um exemplo do output esperado.

**Não testar antes de commitar**: a skill pode estar sintaticamente correta mas instruir o agente de forma ambígua. Teste com um arquivo real antes de versionar.

## Veja também

- [[03-Dominios/IA/Claude Code/Skills e MCP/01 - Anatomia de uma skill|01 - Anatomia de uma skill]] — referência de estrutura
- [[03-Dominios/IA/Claude Code/Skills e MCP/02 - Skills de processo vs domínio|02 - Skills de processo vs domínio]] — qual tipo usar
- [[03-Dominios/IA/Claude Code/Skills e MCP/08 - Skills em time|08 - Skills em time]] — após criar, como versionar e compartilhar
- [[03-Dominios/IA/Claude Code/Skills e MCP/index|Skills e MCP]] — índice do galho
