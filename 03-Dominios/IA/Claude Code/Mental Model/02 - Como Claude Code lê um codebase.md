---
title: "Como Claude Code lê um codebase"
type: concept
publish: true
created: 2026-05-13
updated: 2026-05-13
status: seedling
tags:
  - claude-code
  - mental-model
  - codebase
  - context
---
# Como Claude Code lê um codebase

> [!abstract] TL;DR
> Claude Code não indexa o projeto como uma IDE. Ele navega sob demanda: usa Glob para encontrar arquivos, Grep para buscar símbolos, e Read para ler o que é relevante. O CLAUDE.md funciona como o "onboarding doc" que o agente lê primeiro. Sem CLAUDE.md, o agente descobre o projeto do zero a cada sessão — mais caro e mais lento.

## O que é

IDEs como VS Code ou IntelliJ mantêm um índice persistente do projeto: árvore de arquivos, referências de símbolos, call graph. Esse índice é construído uma vez e mantido atualizado em background.

Claude Code **não tem esse índice**. Cada sessão começa do zero. O agente constrói seu entendimento do projeto **incrementalmente**, usando tools para explorar o que é relevante para a tarefa atual.

Isso é uma escolha de design: o agente pode trabalhar em qualquer projeto sem configuração prévia, e o "índice" é sempre preciso (ele leu o arquivo agora, não há defasagem).

## Como funciona

### 1. Leitura do CLAUDE.md

O primeiro passo de cada sessão é ler os arquivos CLAUDE.md:
- `~/.claude/CLAUDE.md` — configuração global do usuário
- `CLAUDE.md` na raiz do projeto — contexto do projeto
- `CLAUDE.md` em subpastas — contexto específico de área

O CLAUDE.md é o "onboarding doc" que o agente lê antes de fazer qualquer outra coisa. É aqui que você documenta convenções, estrutura, comandos importantes e o que o agente deve ou não deve fazer.

### 2. Exploração sob demanda

Para a tarefa "adicione validação ao endpoint /users", o agente tipicamente:

```
LS("src/")                                       → encontra routes/, controllers/, middleware/
Glob("src/**/*.ts")                              → lista todos os arquivos TypeScript
Grep("router.get.*users", "src/routes/")         → encontra users.router.ts
Read("src/routes/users.router.ts")               → lê o arquivo relevante
```

### 3. Construção incremental do mapa

O agente não lê tudo — lê o mínimo necessário para a tarefa. Isso mantém o contexto enxuto e o custo baixo. À medida que descobre dependências (imports, referências), expande a leitura.

### Comparação: com vs sem CLAUDE.md

| Aspecto | Sem CLAUDE.md | Com CLAUDE.md |
|---------|--------------|---------------|
| Primeiros turnos | Explorando estrutura | Já sabe onde está o quê |
| Convenções | Infere pelo código | Documentado explicitamente |
| Comandos (lint, test, build) | Procura no package.json, Makefile | Listados no CLAUDE.md |
| Custo por sessão | Maior (mais exploração) | Menor |
| Consistência entre sessões | Menor | Maior |

## Por que isso importa

**CLAUDE.md é o maior multiplicador de produtividade.** Um CLAUDE.md bem escrito reduz a exploração inicial, previne erros de convenção, e faz cada sessão começar no nível certo de contexto.

**Pedidos vagos + sem CLAUDE.md = sessões longas.** O agente precisa descobrir tudo sozinho. Com projetos grandes isso significa muitos Greps e Reads antes de chegar ao trabalho real.

**O agente lê seletivamente.** Não assuma que ele "leu tudo". Se há uma convenção importante que o agente não deveria inferir, documente no CLAUDE.md.

## Armadilhas

**Repo muito grande sem CLAUDE.md**: o agente gasta os primeiros 10+ tool calls só entendendo a estrutura. Adicione um CLAUDE.md com a arquitetura em alto nível.

**Estrutura não convencional**: frameworks caseiros, monorepos atípicos, nomes de pastas não padrão confundem a exploração inicial. Documente no CLAUDE.md.

**CLAUDE.md desatualizado**: pior que não ter. Um CLAUDE.md que descreve estrutura antiga induz o agente a tomar decisões erradas. Trate como código — atualize quando a estrutura muda.

**Assumir que o agente "sabe" o projeto**: ele só sabe o que leu na sessão atual. Referências a arquivos não lidos precisam ser explícitas: "o arquivo de autenticação é src/auth/index.ts".

## Veja também

- [[03-Dominios/IA/Claude Code/Mental Model/01 - O loop agentic|01 - O loop agentic]]
- [[03-Dominios/IA/Claude Code/Mental Model/03 - Tool use|03 - Tool use]]
- [[03-Dominios/IA/Claude Code/Configuração/index|Configuração]] — CLAUDE.md em detalhes
- [[03-Dominios/IA/Claude Code/Mental Model/index|Mental Model]] — índice do galho

## Referências

- [Claude Code — CLAUDE.md](https://docs.anthropic.com/pt/docs/claude-code/memory)
