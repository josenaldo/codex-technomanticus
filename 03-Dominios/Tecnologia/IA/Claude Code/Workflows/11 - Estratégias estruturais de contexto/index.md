---
title: "Estratégias estruturais de contexto"
type: moc
publish: true
created: 2026-05-22
updated: 2026-05-22
status: seedling
tags:
  - claude-code
  - workflows
  - contexto
  - tokens
  - economia-de-tokens
  - moc
aliases:
  - Economia estrutural de tokens
  - Estratégias estruturais de tokens
---

# Estratégias estruturais de contexto

> [!abstract] TL;DR
> Sub-galho do galho Workflows. Quatro abordagens estruturais (não-táticas) para reduzir consumo de [[Dicionário de IA#Token|tokens]] em sessões do [[Dicionário de IA#Claude Code|Claude Code]]: lazy-load de `.claude/`, sandboxing de tool output, indexação semântica externa e knowledge graph local com AST. As táticas em [[03-Dominios/Tecnologia/IA/Claude Code/Mental Model/07 - Tokens e custo|07 - Tokens e custo]] (leituras cirúrgicas, `/compact`, filtros de output) cobrem o uso do dia-a-dia; este sub-galho cobre decisões arquiteturais que mudam *como* o codebase é apresentado ao agente.

## Por que um sub-galho separado

Existe uma diferença qualitativa entre **gestão tática** de contexto (que você aplica em toda sessão) e **arquitetura de contexto** (que você decide uma vez e vive com a consequência por meses).

- **Tático** — `Read` com `offset` e `limit`, `Bash` com `| tail`, [[Dicionário de IA#context compaction|`/compact`]] no momento certo, CLAUDE.md enxuto. Cobertura: [[03-Dominios/Tecnologia/IA/Claude Code/Mental Model/07 - Tokens e custo|07 - Tokens e custo]] e [[03-Dominios/Tecnologia/IA/Claude Code/Workflows/10 - Gestão de contexto|10 - Gestão de contexto]].
- **Estrutural** — decisões sobre *como o projeto se apresenta* ao agente: o que carrega por default, o que vira tool externa, o que mora em índice vetorial, o que é mediado por grafo. Cobertura: este sub-galho.

A diferença importa porque os ganhos compõem: bom layout estrutural reduz a base sobre a qual as táticas operam.

## Sobre a relação com proxies (RTK)

Proxies como **RTK** (Rust Token Killer, configurado no global `CLAUDE.md` do autor) atuam na fronteira shell — reescrevem comandos para uma versão token-eficiente *antes* da execução. É uma quinta abordagem, ortogonal às quatro deste galho:

- RTK age no **input do tool** (reescreve o comando).
- Sandboxing age no **output do tool** (intercepta o resultado).
- Lazy-load age no **boot da sessão** (o que carrega por default).
- Indexação semântica/knowledge graph agem no **shape do codebase** (como ele é consultado).

As quatro abordagens deste galho podem coexistir com RTK e entre si.

## Conteúdo

### Iniciado

- [[01 - Estrutura .claude lazy-load]] — separar carga inicial da carga sob demanda via `.claudeignore` + `.claude/` estruturado. Zero infra, aplicável hoje.

### Adepto

- [[02 - Sandboxing de tool output]] — interceptar output verboso de tools (Bash, MCP, Read) antes que polua o contexto. Persistir em SQLite local, retornar resumo + handle de busca.

### Magus

- [[03 - Indexação semântica externa]] — vector DB com embeddings do codebase; MCP expõe semantic search. Para monorepos grandes onde o agente "varre" muito código.
- [[04 - Knowledge graph local com AST]] — Tree-sitter + grafo de chamadas/imports/testes; queries de blast-radius substituem leitura. Para review e refactoring multi-arquivo.

## Quando usar o quê

| Sinal no projeto | Abordagem indicada |
|---|---|
| `.claude/` e docs antigas inflam o startup | [[01 - Estrutura .claude lazy-load|01]] |
| Sessões dominadas por output verboso (Playwright, logs, listas de issues) | [[02 - Sandboxing de tool output|02]] |
| Monorepo >100k LOC; agente sempre "lendo o repo inteiro" | [[03 - Indexação semântica externa|03]] |
| Refactoring/review onde "o que isso impacta?" é a pergunta recorrente | [[04 - Knowledge graph local com AST|04]] |

Não são mutuamente exclusivas — mas comece pelo Iniciado. Indexação e knowledge graph têm custo de infra (API keys, vector DB, manutenção do grafo) que só compensa quando o problema é estrutural.

## Sobre a confiabilidade das fontes

Várias das ferramentas referenciadas neste galho são repositórios jovens com crescimento de stars/forks anormalmente acelerado e claims de adoção corporativa sem prova. As **técnicas** descritas aqui são legítimas e bem fundamentadas; as **implementações específicas** referenciadas exigem due diligence antes de adoção em projeto profissional. Cada nota separa claramente o que é técnica (apropriável) do que é ferramenta (avaliável caso a caso).

## Veja também

- [[03-Dominios/Tecnologia/IA/Claude Code/Mental Model/07 - Tokens e custo|07 - Tokens e custo]] — fundamentos econômicos e táticas básicas
- [[03-Dominios/Tecnologia/IA/Claude Code/Workflows/10 - Gestão de contexto|10 - Gestão de contexto]] — disciplina operacional em sessões longas
- [[03-Dominios/Tecnologia/IA/Claude Code/Mental Model/04 - Context window|04 - Context window]] — limites e mecânica da janela
- [[03-Dominios/Tecnologia/IA/Claude Code/Workflows/index|Workflows]] — galho pai
- [[03-Dominios/Tecnologia/IA/Context Engineering/03 - Context rot e atenção diluída|Context rot e atenção diluída]] — contexto mais amplo
