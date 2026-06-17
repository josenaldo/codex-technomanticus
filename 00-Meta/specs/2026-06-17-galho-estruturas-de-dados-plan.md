---
title: "Galho Estruturas de Dados — design e plano (Fundamentos, Camada A)"
created: 2026-06-17
type: plan
status: draft
publish: false
tags:
  - meta
  - plan
  - fundamentos
  - estruturas-de-dados
---

# Galho Estruturas de Dados — design e plano

## Contexto
Primeiro galho da **Camada A** do meta-plano de Fundamentos
(`00-Meta/specs/2026-06-15-fundamentos-meta-planejamento-design.md`): refatorar o monólito
`03-Dominios/Fundamentos/Estruturas de Dados.md` (620 linhas) numa sub-trilha de notas atômicas
em 3 fases. Interview-critical (★, Fase 1 da Senda Entrevistas).

## Padrão por nota (herdado do galho Complexidade + acréscimos do usuário)
- **Profunda, à profundidade que o assunto exigir.** TETO DE PROSA = **2400 linhas SÓ NESTE GALHO**
  (decisão do usuário em 2026-06-17): não é alvo, é permissão — notas vão tão fundo quanto o tema
  honestamente render, sem padding. **Linhas de código NÃO contam** para o limite. Notas-intro mais
  leves (ex.: 01) ficam menores; estruturas ricas em divergência de runtime (arrays, hash, árvores,
  grafos) podem passar de 1000 linhas de prosa com o tratamento 4-linguagens exaustivo.
- **Diagramas Mermaid** (3–5 por nota) onde ajudam (estrutura de memória, operações, árvores, grafos).
- **Seção "Implementações comparadas: Java · TypeScript · Python · Go"** em cada estrutura — PROFUNDA:
  como cada stack trata o assunto e como as particularidades da linguagem moldam a implementação.
  Código idiomático de cada uma (não conta no limite). Particularidades a cobrir, ex.:
  - **Java:** Collections Framework, generics + boxing/autoboxing, `hashCode`/`equals`, treeify de HashMap.
  - **TS/JS:** array como objeto indexado + otimização V8 (densos/homogêneos), `Map` vs `Object`, hidden classes.
  - **Python:** built-ins (`list` com over-allocation, `dict` compacto + ordem de inserção desde 3.6/3.7,
    `set`), tipagem dinâmica, internals do CPython, `collections`/`heapq`/`bisect`.
  - **Go:** `array` vs `slice` `(ptr,len,cap)` + semântica de `append`/aliasing, `map` (iteração
    randomizada, sem ordem), semântica de valor vs ponteiro, generics desde 1.18, `container/heap`/`list`.
- **Seção "Em entrevista"** (galho interview-critical) — frases prontas em inglês + vocabulário.
- **Análise de complexidade** pontual (Big-O da estrutura); teoria de Big-O fica no galho Algoritmos.
- **Atomicidade:** quando a prosa da comparação 4-linguagens estourar, QUEBRAR em "NN Conceito" +
  "NN Implementações nas 4 linguagens" (flagar o split). Estruturas candidatas a split: arrays, hash tables.

## Preservação (rígido)
- A seção **"Na prática (da minha experiência)"** do monólito contém experiências REAIS do usuário
  (MedEspecialista: HashMap cache + PriorityQueue top-10; Digidados: TreeMap range query; fila de replay).
  **Relocar para as notas certas, NUNCA fabricar novas** ([[feedback-no-fabrication]]).
- Recursos, vocabulário bilíngue e patterns de entrevista do monólito → migrar (capstone + por nota).

## Roster de notas (13 base; pode crescer por split)

### Iniciado — estruturas fundamentais
1. O que é uma estrutura de dados — contrato de operações, dimensões (tempo/espaço/ordem), framework de decisão
2. Arrays e listas dinâmicas — array, dynamic array, localidade de cache, custo amortizado *(candidata a split)*
3. Listas encadeadas — singly/doubly, trade-off vs. array
4. Pilhas, filas e deques — LIFO/FIFO, ArrayDeque/Deque
5. Tabelas hash — hashing, colisões, load factor, contrato hashCode/equals *(candidata a split)*

### Adepto — hierárquicas e relacionais
6. Árvores e árvores de busca — BST, balanceadas (AVL/Red-Black), TreeMap
7. Heaps e filas de prioridade — top-K
8. Tries — busca por prefixo, autocomplete
9. Árvores B e índices — B-Tree/B+Tree → índices de banco (link Banco de dados)
10. Grafos: representação e tipos — adjacência (lista/matriz), direcionado/ponderado/DAG
11. Grafos: travessia e algoritmos — BFS, DFS, Dijkstra, Bellman-Ford, topological sort, Union-Find

### Magus — especializadas e aplicação
12. Estruturas especializadas — LRU, Bloom filter, Skip list, Disjoint set (Union-Find)
13. Escolhendo a estrutura certa (capstone) — tabela comparativa, patterns de entrevista, armadilhas, prep bilíngue

## Tronco e MOC
- Criar pasta `03-Dominios/Fundamentos/Estruturas de Dados/` com `index.md` (MOC, `type: moc`,
  `publish: true`, agrupado por fase, rotas alternativas, dataview, "Veja também").
- O `index.md` recebe **alias "Estruturas de Dados"** (+ "Estruturas de dados") para que os links de
  entrada existentes (`[[Estruturas de Dados]]` em Algoritmos, Senda Entrevistas, etc.) resolvam.
- Migrar o conteúdo do monólito para as notas atômicas; depois **remover** `Estruturas de Dados.md`
  da raiz (conteúdo migrado).
- Atualizar o MOC do domínio (`Fundamentos/index.md` e `Fundamentos.md`): a entrada de Estruturas de
  Dados passa a apontar para o `index` do galho.
- Verbetes no Dicionário de Fundamentos conforme termos surgem.

## Convenções
- `publish: false` nas notas; `publish: true` no `index.md` (convenção de Fundamentos).
- Frontmatter com `fase: iniciado|adepto|magus`, tags. Notas `NN - Título.md` flat.
- Feynman didático; fontes/honestidade onde houver afirmação factual; sem assinatura nos commits.
- Direto na main, push manual.

## Sequência de construção
1. Scaffold `index.md` (MOC, esqueleto das 13 entradas) + alias.
2. Atualizar MOC do domínio para apontar ao galho.
3. Escrever as notas Iniciado (1–5), Adepto (6–11), Magus (12–13), uma por subagente (profunda, 4-lang).
4. Relocar as experiências reais ("Na prática") nas notas certas.
5. Remover o monólito antigo após migração; verbetes; `verificar-wikilinks`; fechar MOC em `growing`.
