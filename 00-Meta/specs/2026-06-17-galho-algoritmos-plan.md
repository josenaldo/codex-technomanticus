---
title: "Galho Algoritmos — design e plano (Fundamentos, Camada A)"
created: 2026-06-17
type: plan
status: draft
publish: false
tags:
  - meta
  - plan
  - fundamentos
  - algoritmos
---

# Galho Algoritmos — design e plano

## Contexto
Segundo galho da **Camada A** do meta-plano de Fundamentos
(`00-Meta/specs/2026-06-15-fundamentos-meta-planejamento-design.md`): refatorar o monólito
`03-Dominios/Fundamentos/Algoritmos.md` (601 linhas) numa sub-trilha de notas atômicas em 3 fases.
Interview-critical (★, Fase 1 da Senda Entrevistas). Mesmo padrão tronco/galhos dos galhos
Complexidade de Software e Estruturas de Dados (ED).

**Fronteira-chave (dono da teoria de complexidade):** ED *delegou* a teoria de complexidade a
este galho. Logo Algoritmos é o dono canônico de: análise de complexidade (Big-O, Θ/Ω,
best/average/worst, amortizado), recorrências e Teorema Mestre, e os algoritmos clássicos
(sorting, searching, two pointers, sliding window, recursão, divide & conquer, DP, greedy,
backtracking). A nota Big-O (02) é o destino dos links de complexidade vindos de ED.

## Decisões herdadas de ED (resolvidas neste galho, 2026-06-17)

1. **Seção "4 linguagens" — targeted, NÃO blanket.** Diferente de ED (onde toda estrutura tem
   divergência de runtime), em Algoritmos a maioria são *técnicas que você implementa* — sem
   história cross-linguagem. Tratamento 4-linguagens COMPLETO só onde a stdlib faz o trabalho e
   cai em entrevista:
   - **Ordenação (07):** TimSort (Java objetos / Python), dual-pivot quicksort (Java primitivos),
     pdqsort (Go), V8 TimSort (JS). "Que sort sua linguagem usa?"
   - **Busca (08):** `Arrays.binarySearch`/`Collections.binarySearch` (Java), `bisect` (Python),
     `sort.Search`/`slices.BinarySearch` (Go), ausência built-in em JS.
   - **Demais notas:** código idiomático em 1–2 linguagens + **callout "particularidades por
     linguagem"** quando houver divergência real (limite de recursão Python ~1000 vs Java ~10⁴
     frames; ausência de TCO no Java; `BigInteger`/overflow; gerador vs lista materializada em DP).
     Sem forçar colunas de 4 linguagens onde não há divergência.
2. **Teto de prosa = 2400 linhas SÓ NESTE GALHO** (permissão, não alvo; código NÃO conta) — igual
   ED, por consistência e porque Big-O / Teorema Mestre / DP rendem fundo. Sem o blanket
   4-linguagens, a maioria das notas aterrissa naturalmente ~500–900 linhas; o teto é liberdade
   pra ir fundo onde o tema pede, nunca licença pra padding.
3. **P/NP — teoria formal vai pro galho 10 (Teoria da Computação); Algoritmos fica com a face
   prática.** O meta-plano já atribui "complexidade P/NP" ao galho 10. Algoritmos NÃO duplica a
   teoria formal (redução, NP-completude, Cook-Levin). Em vez disso ganha a nota 13
   (**Intratabilidade prática**), que linka pra frente ao galho 10 quando nascer. Aplicação de
   [[feedback-redundancia-entre-notas]] (linka, não duplica).

## Fronteira com grafos (rígido)
A seção inteira "Algoritmos em Grafos" do monólito (BFS, DFS, Dijkstra, Bellman-Ford,
topological sort, A*, Floyd-Warshall) **NÃO entra neste galho** — esses algoritmos moram em
`Estruturas de Dados/11 - Grafos - travessia e algoritmos.md`. As notas 11 (greedy) e 14
(capstone) apenas **linkam** pra lá (`[[11 - Grafos - travessia e algoritmos]]`). Redundância via
link, não duplicação de conteúdo.

## Preservação (rígido)
A seção **"Na prática (da minha experiência)"** do monólito tem experiências REAIS do usuário.
**Relocar, NUNCA refazer/fabricar** ([[feedback-no-fabrication]]):
- MedEspecialista — endpoint de busca O(n×m) → coluna desnormalizada + índice composto → O(log n) → **nota 02 (Big-O)**.
- Digidados — `list.contains()` em loop O(n²) → `HashSet.contains()` O(n) → **nota 02 (Big-O)**.
- Prática de patterns (NeetCode 150; "reconhecer padrões, não decorar soluções") → **nota 14 (capstone)**.

Recursos (cursos/livros/prática), vocabulário bilíngue e patterns de entrevista do monólito →
migrar (capstone 14 + por nota onde couber).

## Roster de notas (14 base; pode crescer por split)

### Iniciado — análise e fundamentos
1. **O que é um algoritmo** — correção, terminação, generalidade; algoritmo vs implementação;
   as 4 dimensões avaliadas em entrevista *(intro mais leve)*
2. **Análise de complexidade: Big-O** — comportamento assintótico, hierarquia O(1)→O(n!), regras
   práticas, notação O/Θ/Ω, best/average/worst case. **Nota-âncora** (destino dos links de
   complexidade de ED). Recebe as 2 experiências reais de produção.
3. **Análise amortizada** — custo amortizado; métodos agregado / contábil (banker's) / potencial
   (physicist's); dynamic array doubling como caso canônico *(flag: fundir na 02 se ficar fina)*
4. **Recursão** — base/recursive case, garantia de progresso, call stack, recursão vs iteração,
   tail recursion (e ausência de TCO no Java), stack overflow e limites de profundidade por linguagem

### Adepto — algoritmos clássicos
5. **Recorrências e o Teorema Mestre** — T(n)=a·T(n/b)+f(n), os 3 casos, recursion-tree, método da
   substituição, menção a Akra-Bazzi *(flag: fundir na 06 se ficar fina)*
6. **Divisão e conquista** — estratégia dividir/resolver/combinar; merge sort, quicksort (partição,
   escolha de pivô), closest pair of points, Karatsuba; liga ao Teorema Mestre (05)
7. **Ordenação** — comparativo (bubble/insertion/selection/merge/quick/heap/Tim/counting/radix),
   estabilidade, in-place, comparison vs non-comparison, limite inferior Ω(n log n).
   **Tratamento 4-linguagens completo dos stdlib.**
8. **Busca** — linear, binary search (template confiável, off-by-one, overflow), variações
   (lower/upper bound, busca no espaço de respostas / monotonicidade), quickselect.
   stdlib das 4 linguagens.
9. **Two pointers e sliding window** — ponteiros convergentes/paralelos; janela fixa vs variável;
   fast/slow (Floyd cycle detection); combinação com hash
10. **Programação dinâmica** — subestrutura ótima, subproblemas sobrepostos, memoização (top-down)
    vs tabulação (bottom-up), otimização de espaço, design de estado, problemas clássicos
    (coin change, knapsack 0/1, LCS, LIS, edit distance) *(flag: forte candidata a split em
    "10 Fundamentos de DP" + "11 Padrões clássicos de DP" — renumerar o resto se ocorrer)*
11. **Greedy** — escolha localmente ótima, propriedade da escolha gulosa, exchange argument,
    quando funciona vs falha (coin change canônico vs arbitrário), Huffman/interval scheduling;
    Dijkstra/Kruskal/Prim como exemplos gulosos → linka `[[11 - Grafos - travessia e algoritmos]]`
12. **Backtracking** — explorar + desfazer, poda, estrutura geral; N-queens, sudoku, permutações,
    combinações, subset sum, generate parentheses; complexidade exponencial com poda

### Magus — síntese e limites
13. **Intratabilidade: quando não há algoritmo eficiente** — tratável vs intratável, explosão
    combinatória (2ⁿ, n!), NP-difícil como SINAL PRÁTICO ("pare de procurar polinomial"),
    estratégias (aproximação, heurística, DP-exponencial, poda, parametrização). Linka P/NP
    formal → galho 10 (Teoria da Computação)
14. **Reconhecendo o algoritmo certo (capstone)** — tabela "sinal no enunciado → abordagem",
    framework dos 6 passos em entrevista (clarify→explore→brute force→optimize→code→test), edge
    cases esquecidos, armadilhas comuns, "How to explain in English" + vocabulário bilíngue,
    cheat-sheet. Recebe a prática de patterns (NeetCode) do monólito; recursos (cursos/livros)

## Padrão por nota (herdado de Complexidade + ED)
- Profunda, à profundidade que o assunto exigir; registro **Feynman** didático (analogias,
  perguntas retóricas, resumo em 1 linha). Teto 2400 (permissão), código não conta.
- **Diagramas Mermaid** (3–5 por nota) onde ajudam (árvore de recursão, partição do quicksort,
  tabela DP preenchendo, recursion tree do Teorema Mestre, fluxo do backtracking). Cada diagrama
  com lead-in + "leitura do diagrama".
- **Seção "Em entrevista"** (galho interview-critical) — frases prontas em inglês + vocabulário.
- Fontes verificadas na web para afirmações factuais; callout "lastro" de honestidade.
- **Atomicidade:** cada nota linka as vizinhas em vez de duplicar. Notas `NN - Título.md` flat.
- `publish: false` nas notas; `publish: true` só no `index.md` (convenção de Fundamentos).
- Frontmatter com `fase: iniciado|adepto|magus`, tags.

## Tronco e MOC
- Criar pasta `03-Dominios/Fundamentos/Algoritmos/` com `index.md` (MOC, `type: moc`,
  `publish: true`, agrupado por fase, rotas alternativas, dataview, "Veja também").
- O `index.md` recebe **alias "Algoritmos"** (+ "algoritmos") para que os 10 links de entrada
  existentes (`[[Algoritmos]]` em README, Senda Entrevistas, Coding Challenges Strategy, Helsinki
  MOOC, ED/01, ED/13, ED/index, Fundamentos/index, Fundamentos.md, index raiz) resolvam.
- Migrar o conteúdo do monólito para as notas atômicas; depois **remover** `Algoritmos.md`
  (`git rm`, conteúdo migrado).
- Atualizar o MOC do domínio (`Fundamentos/index.md` e `Fundamentos.md`): a entrada de Algoritmos
  passa a apontar para o `index` do galho.
- Verbetes no Dicionário de Fundamentos conforme termos surgem (opcional, como em ED).

## Convenções de execução
- Feynman didático; fontes/honestidade onde houver afirmação factual.
- **Subagent-driven:** um subagente por nota, sequencial (profundo, Feynman, diagramas).
- Commits **direto na main**, **SEM push**, **SEM Co-Authored-By** ([[feedback-commits]]).

## Sequência de construção
1. Scaffold `index.md` (MOC, esqueleto das 14 entradas) + alias.
2. Atualizar MOC do domínio para apontar ao galho.
3. Escrever as notas Iniciado (1–4), Adepto (5–12), Magus (13–14), uma por subagente.
4. Relocar as experiências reais ("Na prática") nas notas certas (2 prod → 02, NeetCode → 14).
5. Remover o monólito antigo após migração; verbetes (opcional); `verificar-wikilinks`;
   fechar MOC em `growing`.
