---
title: "Slash commands customizados — .claude/commands/"
type: concept
publish: true
created: 2026-05-13
updated: 2026-05-13
status: seedling
tags:
  - claude-code
  - configuracao
  - slash-commands
  - commands
---

# Slash commands customizados — .claude/commands/

> [!abstract] TL;DR
> Slash commands customizados são arquivos Markdown em `.claude/commands/` que o Claude Code expõe como `/nome-do-arquivo`. O conteúdo do arquivo vira o prompt executado quando você digita o comando. Útil para encapsular fluxos recorrentes do projeto (code review, deploy check, gerar changelog). O argumento `$ARGUMENTS` captura o que você escreve depois do comando.

## O que é

Slash commands built-in (`/compact`, `/clear`, `/help`) são do Claude Code. Commands customizados são seus — criados na pasta `.claude/commands/` do projeto ou em `~/.claude/commands/` (global).

```
.claude/
  commands/
    review.md          → /review
    deploy-check.md    → /deploy-check
    changelog.md       → /changelog
```

Quando você digita `/review` no chat, Claude Code carrega o conteúdo de `review.md` e o executa como prompt.

## Criando um slash command

1. Crie um arquivo `.md` em `.claude/commands/`
2. O nome do arquivo (sem `.md`) vira o comando
3. Escreva o prompt no corpo do arquivo

```markdown
<!-- .claude/commands/review.md -->
Faça um code review das mudanças em staging (git diff --staged).

Avalie:
- Bugs óbvios e edge cases não tratados
- Violações das convenções do projeto (CLAUDE.md)
- Testes ausentes para o happy path e casos de erro
- Performance: queries N+1, alocações desnecessárias

Formato de saída: lista de issues por arquivo, severidade (critical/warning/suggestion).
```

Depois: `/review` no chat executa exatamente esse prompt.

## Usando `$ARGUMENTS`

Para comandos que recebem entrada do usuário, use `$ARGUMENTS` no corpo do arquivo. Claude Code substitui `$ARGUMENTS` pelo texto digitado após o comando.

```markdown
<!-- .claude/commands/test-module.md -->
Rode os testes do módulo $ARGUMENTS e analise as falhas.

Se houver falhas:
1. Mostre o stack trace completo de cada falha
2. Identifique a causa raiz (não apenas o sintoma)
3. Sugira a correção mínima para fazer o teste passar

Se todos os testes passarem, mostre o relatório de cobertura.
```

Uso:

```
/test-module services/payment
```

Claude Code executa o prompt com `$ARGUMENTS` = `services/payment`.

## Exemplos de commands úteis

### `/pr-check` — checklist antes de abrir PR

```markdown
<!-- .claude/commands/pr-check.md -->
Revise as mudanças atuais (git diff main) como se fosse aprovar ou reprovar um PR.

Verifique:
- [ ] Todos os testes passam (`npm test`)
- [ ] Sem console.log ou código de debug esquecido
- [ ] Sem credenciais ou secrets hardcoded
- [ ] Convenções de código seguidas (ver CLAUDE.md)
- [ ] Cobertura: há testes para o que foi adicionado?
- [ ] Breaking changes documentados?

Dê um veredito: APROVADO / APROVADO COM RESSALVAS / REPROVADO, com justificativa.
```

### `/explain` — explicar código para onboarding

```markdown
<!-- .claude/commands/explain.md -->
Explique o arquivo ou função $ARGUMENTS para um dev que acabou de entrar no projeto.

Inclua:
- O que faz em linguagem de negócio (não só técnica)
- Como se encaixa na arquitetura geral
- Decisões de design não óbvias (por que foi feito assim)
- Armadilhas ou pontos de atenção para quem for modificar

Nível: dev sênior, mas novo no projeto.
```

### `/changelog` — gerar changelog

```markdown
<!-- .claude/commands/changelog.md -->
Gere um changelog para os commits desde a última tag, no formato Keep a Changelog.

1. Execute `git log $(git describe --tags --abbrev=0)..HEAD --oneline`
2. Agrupe por: Added, Changed, Fixed, Removed
3. Use linguagem de produto (benefício para o usuário, não detalhes técnicos)
4. Ignore commits de chore, style, e refactor sem impacto visível

Formato de saída: Markdown pronto para adicionar ao CHANGELOG.md.
```

### `/debug` — sessão de debugging estruturada

```markdown
<!-- .claude/commands/debug.md -->
Inicie uma sessão de debugging estruturada para o problema: $ARGUMENTS

Processo:
1. Reproduza o problema: qual é o comportamento esperado vs. observado?
2. Identifique o ponto de entrada: onde o fluxo começa?
3. Adicione logging/print estratégico para rastrear o estado
4. Forme hipóteses e teste cada uma com evidências
5. Não sugira fix antes de ter certeza da causa raiz

Não modifique código até termos a causa confirmada.
```

## Commands globais vs. de projeto

```
~/.claude/commands/      → disponível em todos os projetos
.claude/commands/        → específico do projeto (vai pro git, time inteiro)
```

Commands de projeto ficam no repositório — todo o time tem acesso aos mesmos `/` commands quando trabalham no projeto com Claude Code.

## Armadilhas

**Nome com espaços**: use kebab-case. `deploy check.md` não funciona — use `deploy-check.md`.

**Prompt vago no command file**: um command com "faça um review do código" sem critérios específicos produz output genérico. Seja preciso como num prompt normal.

**$ARGUMENTS sem fallback**: se o comando fizer sentido com e sem argumento, adicione instrução para o caso em que nenhum argumento é passado.

**Commands desatualizados**: se um command referencia um arquivo (`src/utils/logger.ts`) que foi movido, ele vai confundir o agente. Revise commands quando a estrutura do projeto mudar.

## Veja também

- [[03-Dominios/IA/Claude Code/Configuração/07 - Pasta .claude|07 - Pasta .claude]] — estrutura completa da pasta .claude
- [[03-Dominios/IA/Claude Code/Configuração/01 - Hierarquia de configuração|01 - Hierarquia de configuração]] — commands globais vs. de projeto
- [[03-Dominios/IA/Claude Code/Skills e MCP/index|Skills e MCP]] — skills são commands mais poderosos (plugins externos)
- [[03-Dominios/IA/Claude Code/Configuração/index|Configuração]] — índice do galho

## Referências

- [Claude Code — Slash commands](https://docs.anthropic.com/pt/docs/claude-code/slash-commands)
