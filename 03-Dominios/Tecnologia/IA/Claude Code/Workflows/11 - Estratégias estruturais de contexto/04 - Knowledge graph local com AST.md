---
title: "Knowledge graph local com AST — blast-radius em vez de re-leitura"
type: concept
progress: backlog
publish: true
created: 2026-05-22
updated: 2026-05-22
status: seedling
fase: magus
tags:
  - claude-code
  - workflows
  - contexto
  - tokens
  - ast
  - tree-sitter
  - knowledge-graph
  - blast-radius
  - mcp
aliases:
  - Code knowledge graph
  - AST graph MCP
  - Blast-radius analysis
---

# Knowledge graph local com AST — blast-radius em vez de re-leitura

> [!abstract] TL;DR
> Em review e refactoring multi-arquivo, a pergunta dominante é "o que essa mudança impacta?". A resposta exige percorrer chamadas, herança, imports e testes — leitura caríssima em [[Dicionário de IA#Token|tokens]]. Knowledge graph local resolve isso parsing o codebase com Tree-sitter, armazenando funções/classes/imports como **nós** e chamadas/herança/cobertura como **arestas** em SQLite, e expondo via [[Dicionário de IA#MCP (Model Context Protocol)|MCP]] queries de blast-radius. O agente lê o **grafo da mudança**, não o **código completo**. Reduções relatadas de 5×–50× em tarefas de review, dependendo do tamanho do monorepo.

## O que é

Uma camada de análise estática que constrói um grafo de relações do código, persiste localmente, e responde queries estruturais em vez de obrigar o agente a re-ler arquivos.

```
Nós:                          Arestas:
  - Function                    - calls          (f1 chama f2)
  - Class                       - extends        (Class A herda B)
  - Module                      - imports        (file imports X)
  - Test                        - tests          (test cobre função)
  - File                        - defines        (file define símbolo)
```

Query típica em review:

```
detect_changes(commit=abc123)
  → arquivos modificados: 3
  → funções afetadas: 7
  → blast-radius (callers transitivos): 23 funções em 11 arquivos
  → testes que cobrem: 4 (faltam: 3 funções sem cobertura)
```

O agente recebe esse resumo (~2 KB) em vez de ler os 11 arquivos completos (~120 KB).

## Como funciona

### Parsing com Tree-sitter

Tree-sitter é o parser incremental usado pelo GitHub, Atom, Neovim e a maioria das implementações de knowledge graph. Roda em ~100ms por arquivo, suporta 20+ linguagens com grammars maduras (Python, TypeScript, Go, Rust, Java, etc).

Para cada arquivo, o parser extrai:

- Definições de função/classe/método.
- Call sites (quem chama quem).
- Imports e referências entre módulos.
- Cadeias de herança.
- Decoradores e atributos relevantes (`@pytest.fixture`, `@Test`, etc).

### Persistência local

O grafo geralmente vive em SQLite no projeto, em algo como `.code-graph/graph.db`. Tabelas básicas:

```sql
CREATE TABLE nodes (
  id INTEGER PRIMARY KEY,
  type TEXT,           -- function, class, module, test
  name TEXT,
  file TEXT,
  line_start INTEGER,
  line_end INTEGER,
  hash TEXT            -- SHA-256 do conteúdo para detecção de mudança
);

CREATE TABLE edges (
  source_id INTEGER,
  target_id INTEGER,
  type TEXT,           -- calls, extends, imports, tests
  confidence REAL      -- 0.0–1.0, extracted vs inferred
);
```

### Atualização incremental

A cada save (ou commit), um hook diffa os hashes dos nós, identifica arquivos modificados, e re-parseia só esses. Em monorepo de 2900 arquivos, atualização típica fica em <2s.

Sem incremental, o grafo vira inútil — ninguém aguenta rebuild de minutos a cada save.

### MCP como interface

O grafo é exposto via MCP server com tools como:

- `find_callers(symbol)` — quem chama esta função.
- `find_dependents(file)` — o que depende deste módulo.
- `blast_radius(commit_or_diff)` — todos os impactos transitivos.
- `find_untested(file)` — funções sem cobertura.
- `find_hubs()` — nós mais conectados (chokepoints arquiteturais).
- `find_bridges()` — nós que conectam comunidades distintas.

Configurado uma vez, vira ferramenta padrão em sessões de review e refactor.

### Análises secundárias úteis

Grafos sérios não param em blast-radius. Métricas baratas a partir do grafo:

- **Comunidades** (Leiden/Louvain) — agrupa código relacionado, identifica módulos coesos vs acoplamento espúrio.
- **Betweenness centrality** — nós-ponte que se conectam comunidades; mudanças neles têm impacto desproporcional.
- **Surprise scoring** — arestas anômalas (cross-language, periphery-to-hub).
- **Dead code detection** — nós sem callers reachable a partir de entry points.
- **Auto-arquitetura** — diagrama do projeto gerado do grafo, útil pra onboarding e PR review.

## Quando usar

A abordagem se justifica em workflows específicos:

| Workflow | Knowledge graph compensa? |
|---|---|
| Code review de PR em monorepo | Sim |
| Refactoring que toca código compartilhado | Sim |
| "Posso remover esta função?" / dead code | Sim |
| Análise de impacto antes de mudar uma API | Sim |
| Coding "verde" em projeto pequeno | Não |
| Geração de código novo | Marginal |

Pareia bem com [[03 - Indexação semântica externa|03 - Indexação semântica]]: semantic search acha "onde fala de X"; knowledge graph acha "o que X afeta".

## Custo da abordagem

- **Build inicial**: ~10s para projeto de 500 arquivos; minutos para monorepo grande.
- **Atualização incremental**: <2s típico, via hooks.
- **Espaço em disco**: SQLite de poucos MB para projetos médios; algumas centenas de MB em monorepos com 10k+ arquivos.
- **Manutenção**: Tree-sitter grammars precisam estar atualizadas pra linguagens menos populares; edges inferidos (não-extraídos diretamente do AST) têm precisão variável.

Custo de infra é menor que indexação semântica (sem API key, sem vector DB cloud), mas requer setup correto de hooks e disciplina de re-build em mudanças de configuração.

## Armadilhas

**Confundir recall com precisão**. Blast-radius bem desenhado prioriza **recall** (não perder impacto real) sobre precisão (over-predict é aceitável). Mas se a precisão fica em 0.2, o agente é inundado de falsos positivos e perde o sinal. Implementações bem calibradas ficam em F1 ~0.5 com recall 1.0 — isso é "conservador funcional", não "ruído".

**Edges inferidos vendidos como extraídos**. Tree-sitter extrai call sites com alta confiança quando a chamada é direta (`foo()`). Em chamadas dinâmicas (`obj[method]()`, callbacks, decorators meta), a aresta é **inferida** com confidence <1.0. Implementações maduras anotam essa confiança; as ruins tratam tudo como extraído e o grafo vira ficção.

**Grafo desatualizado**. Sem hooks de save/commit, o grafo defasa em horas; em uma semana, o agente trabalha com mapa de ontem. Sempre verifique: o hook está configurado? O daemon roda? `find_callers` retorna resultado coerente com `grep`?

**Languages sem grammar maduro**. Tree-sitter cobre bem Python/TS/Go/Rust/Java/Ruby; menos bem Solidity, Zig, Julia, R; mal Bash, COBOL, código legado. Em projeto poliglota exótico, o grafo fica com buracos.

**Dependência de ferramenta unitária**. Se você ata o workflow a um MCP que some (mantenedor abandonou, repo é tomado), você perde o investimento. Vale optar por implementações com formato exportável (GraphML, Neo4j Cypher) que permitem migrar.

**Tomar stars como prova de qualidade**. O espaço de MCPs de knowledge graph tem repos com crescimento de stars/forks anormal (>15k em <3 meses, fork-to-star ratio ~10%) — sinais de star inflation, não de adoção real. Avalie o código, os benchmarks reproduzíveis, e idealmente teste num repo seu antes de incorporar no workflow.

## Relação com outras abordagens deste galho

Knowledge graph age no eixo **estrutural** (calls, imports, herança); [[03 - Indexação semântica externa|indexação semântica]] age no eixo **conceitual** (similaridade de significado). Combinadas, cobrem as duas perguntas dominantes em codebase grande:

- "Onde fala disso?" → semantic search
- "O que isso afeta?" → knowledge graph

Lazy-load ([[01 - Estrutura .claude lazy-load|01]]) e sandboxing ([[02 - Sandboxing de tool output|02]]) atuam em camadas anteriores (boot da sessão, output de tools). As quatro compõem sem conflito.

## Veja também

- [[03-Dominios/Tecnologia/IA/Claude Code/Workflows/05 - Code review|Code review]] — workflow primário onde knowledge graph brilha
- [[03-Dominios/Tecnologia/IA/Claude Code/Workflows/03 - Refactoring pesado|Refactoring pesado]] — blast-radius é central aqui
- [[03-Dominios/Tecnologia/IA/Claude Code/Skills e MCP/04 - MCP overview|MCP overview]] — como o grafo é exposto ao agente
- [[03 - Indexação semântica externa]] — abordagem complementar (eixo conceitual)
- [[03-Dominios/Tecnologia/IA/Claude Code/Workflows/11 - Estratégias estruturais de contexto/index|Tronco do sub-galho]]

## Aprofundamento

> [!convite] Referências externas
> - [tirth8205/code-review-graph](https://github.com/tirth8205/code-review-graph) — implementação Python/MCP com Tree-sitter, SQLite, blast-radius, comunidades via Leiden, hubs/bridges, export GraphML/Neo4j/Obsidian. MIT, 24 linguagens, benchmarks reproduzíveis. **Cuidado:** repo de ~3 meses com ~17k stars e 1846 forks — métricas suspeitas de star inflation (fork ratio anormal). A técnica é legítima; o repo específico merece due diligence antes de adotar em projeto profissional. Leia o código, reproduza os benchmarks num repo seu, decida.
> - Conceitos relacionados: [Tree-sitter](https://tree-sitter.github.io/tree-sitter/) (parser incremental), [Leiden community detection](https://www.nature.com/articles/s41598-019-41695-z) (algoritmo padrão pra clustering de grafos), GraphML / Cypher (formatos portáveis pra grafos).
>
> Consumiu? Faça uma glosa em `02-Glosas/` se quiser destilar mais.
