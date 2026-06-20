---
title: "Galho Matemática para Computação — design e plano (Fundamentos, Camada B)"
created: 2026-06-20
type: plan
status: draft
publish: false
tags:
  - meta
  - plan
  - fundamentos
  - matematica-para-computacao
---

# Galho Matemática para Computação — design e plano

## Contexto
QUINTO e ÚLTIMO galho da Camada B (depois de Paradigmas, Concorrência, Sistemas Operacionais e
Teoria da Computação, COMPLETOS). Galho 11 do roster: "Matemática para Computação — matemática discreta:
lógica, conjuntos, combinatória, grafos, probabilidade. (raro)". Conteúdo NOVO (sem monólito-semente).
Roster de **22 notas (4/9/9)** aprovado pelo usuário em 2026-06-20 na opção **Capricho ED + Expandir**
(profundidade máxima nível Estruturas de Dados + splits de combinatória e grafos). Concluí-lo **FECHA a
Camada B (5 de 5)**. Depois só restam os galhos da Camada D (13 Organização de Computadores, 14 Segurança
Conceitual, 15 Compiladores e Linguagens).

Decisão herdada do meta-plano: **10 e 11 são DOIS galhos distintos.** Matemática é a *ferramenta*;
Teoria da Computação é a *teoria sobre os limites do computável*. Este galho é a DONA de lógica, técnicas
de prova, conjuntos, cardinalidade, combinatória, teoria dos números, grafos (lado matemático) e
probabilidade — ferramentas que outros galhos já usam sem ensinar.

## Decisão de fronteira (rígido — linka, não duplica)
- **Teoria da Computação** (galho 10, existe) — USA lógica/provas/diagonalização mas não as ensina.
  Matemática é a DONA. A nota 13 (Cardinalidade) é dona de contável×incontável e da **diagonalização de
  Cantor**, e LINKA `[[03-Dominios/Fundamentos/Teoria da Computação/10 - Decidível, reconhecível e a máquina universal]]`
  (o uso em computabilidade), sem repetir.
- **Algoritmos** (galho 2, existe) — dono de análise assintótica/Big-O (nota 02), recorrências e Teorema
  Mestre (nota 05). A nota 08 (Somatórios, logaritmos e crescimento) dá a BASE matemática (logaritmos,
  somatórios, crescimento, resolução geral de recorrências) e LINKA
  `[[03-Dominios/Fundamentos/Algoritmos/02 - Análise de complexidade - Big-O]]` e
  `[[03-Dominios/Fundamentos/Algoritmos/05 - Recorrências e o Teorema Mestre]]`; **NÃO reescreve o Teorema Mestre.**
- **Estruturas de Dados** (galho 1, existe) — dona de grafos como ESTRUTURA e dos ALGORITMOS de grafo
  (BFS/DFS/Dijkstra em ED/11). As notas 16/17 (grafos) e 18 (árvores) fazem o lado MATEMÁTICO (definições,
  Euler/Hamilton, planaridade, coloração, matching, árvore como objeto) e LINKAM
  `[[03-Dominios/Fundamentos/Estruturas de Dados/11 - Grafos - travessia e algoritmos]]` pro lado algorítmico.
  A nota 21 (aleatorizadas) linka ED/12 (Bloom/skip list). Fronteira delicada — explicitar em prosa.
- **Segurança Conceitual** (galho 14, Camada D, **NÃO existe**) — dona de criptografia/hashing aplicados.
  As notas 14/15 (teoria dos números) são donas da TEORIA (divisibilidade, primos, Euclides, modular,
  Fermat/Euler) como ferramenta; mencionam **RSA/cripto em PROSA, sem wikilink quebrado**.
- **Organização de Computadores** (galho 13, Camada D, **NÃO existe**) — dona de representação binária e
  circuitos/álgebra booleana de hardware. Se a lógica tocar álgebra booleana, fazê-lo pelo ângulo
  LÓGICO-matemático e mencionar lógica digital em PROSA, sem wikilink.
- **Paradigmas de Programação** (galho 7, existe) — recursão/indução pelo ângulo de estilo. A nota 07
  (Indução estrutural) pode LINKAR `[[Paradigmas de Programação]]` em prosa onde ilumina.
- **Concorrência / Complexidade de Software / SO** — NÃO confundir; não linkar por engano.

## Assinatura ED deste galho (capricho)
Cada peça abstrata fecha com o **ângulo prático** (o equivalente ao "comparado por runtime" de ED, ou ao
"resgate prático" da Teoria da Computação): indução = corretude de recursão e loop invariants; lógica =
invariantes/asserções/WHERE do SQL; conjuntos = tipos/set ops; combinatória = tamanho do espaço de estados
e casos de teste; teoria dos números = RSA/hashing/checksums; probabilidade = estruturas aleatorizadas
(Bloom/skip list/hashing). O **cluster de probabilidade (19-21)** recebe tratamento nível ED: cada peça com
worked example profundo, culminando na nota 21 (showcase aplicado de estruturas/algoritmos aleatorizados,
análogo ao cluster-de-modelos da Concorrência). O **capstone (22)** traz um cheat-sheet mestre (técnica de
prova → quando usar; ramo da matemática → aplicação em CS).

## Roster de notas (22)

### Iniciado — a linguagem da prova (lógica e conjuntos)
1. **O que é matemática para computação** *(âncora)* — discreto × contínuo; por que a CS é matemática
   discreta (estados, passos, estruturas finitas/enumeráveis); o mapa do galho (lógica → prova → estruturas
   → contagem → números → grafos → acaso); a fronteira cravada: *matemática é a ferramenta; Teoria da
   Computação é a teoria dos limites*. Menciona em prosa que outros galhos (Algoritmos, ED, Teoria da
   Computação) já usam essas ferramentas. **Linka [[03-Dominios/Fundamentos/Teoria da Computação/index]]** em prosa.
2. **Lógica proposicional** — proposições, conectivos (¬ ∧ ∨ → ↔), tabelas-verdade, tautologia/contradição/
   contingência, equivalências lógicas (De Morgan, distributiva, contrapositiva), implicação × recíproca ×
   contrapositiva × inversa, formas normais (DNF/CNF em prosa), satisfatibilidade (gancho leve pra SAT).
   Prática: condições booleanas, short-circuit, De Morgan ao negar um `if`, `WHERE`/`AND`/`OR`/`NOT` do SQL,
   guard clauses. Tabela-verdade como diagrama; flowchart de equivalência.
3. **Lógica de predicados e quantificadores** — predicados, domínio de discurso, ∀ (universal) e ∃
   (existencial), negação de quantificadores (¬∀ = ∃¬), quantificadores aninhados e a ordem que importa
   (∀∃ ≠ ∃∀), vacuamente verdadeiro. Prática: invariantes de laço, asserções, pré/pós-condições,
   especificação formal, "for all / there exists" em validação e em queries. Linka a nota 02.
4. **Teoria dos conjuntos** — definição, pertinência (∈), ⊆ × ⊂, conjunto vazio, operações (∪ ∩ \ complemento),
   conjunto potência (2ⁿ), produto cartesiano, diagramas de Venn, leis (De Morgan de conjuntos, distributiva),
   cardinalidade finita |A|. Prática: tipos como conjuntos (union/intersection types), operações de conjunto
   em SQL (UNION/INTERSECT/EXCEPT), deduplicação, modelagem de domínios. Aponta pra nota 13 (cardinalidade infinita).

### Adepto — provar, quantificar, contar
5. **Técnicas de prova** — o que é uma prova (cadeia de implicações a partir de axiomas/definições); prova
   direta; por contraposição; por contradição/absurdo; por casos/exaustão; contraexemplo (pra refutar);
   "se e somente se" (ida e volta); erros comuns (afirmar o consequente, circularidade). Prática: raciocinar
   sobre corretude de código; o adversarial "prove que não funciona". Linka 02/03 (a lógica por trás).
6. **Indução matemática (e forte)** — princípio da boa ordenação; indução fraca (base + passo P(n)→P(n+1));
   indução forte (assume P(1..n)); por que funciona (efeito dominó / descida infinita); exemplos canônicos
   (∑i = n(n+1)/2, ∑2ⁱ, 2ⁿ > n). **Prática: corretude de algoritmos recursivos e loop invariants** (a mesma
   estrutura: inicialização = base, manutenção = passo, término). **Linka [[03-Dominios/Fundamentos/Algoritmos/05 - Recorrências e o Teorema Mestre]]**.
7. **Indução estrutural e definições recursivas** — definição recursiva (caso base + regra); estruturas
   indutivamente definidas (naturais, listas, árvores, expressões/ASTs, palavras); indução estrutural como a
   generalização da matemática pra dados recursivos; por que é A técnica de prova da CS. **Prática: provar
   propriedades de ADTs e funções recursivas** (ex.: tamanho da árvore, reverse∘reverse = id). **Linka
   [[Paradigmas de Programação]]** (recursão/ADTs) em prosa.
8. **Somatórios, logaritmos e crescimento** — manipulação de somatórios (Σ): linearidade, telescópico,
   séries (aritmética, geométrica, harmônica ~ ln n), fórmulas fechadas; logaritmos: identidades, mudança de
   base, por que log aparece (dividir pela metade); crescimento de funções e a hierarquia (log < poli < exp);
   resolução *geral* de recorrências (substituição, árvore de recursão, expansão) **sem reescrever o Teorema
   Mestre**. **Dona da base matemática que Algoritmos usa — linka
   [[03-Dominios/Fundamentos/Algoritmos/02 - Análise de complexidade - Big-O]]** e
   **[[03-Dominios/Fundamentos/Algoritmos/05 - Recorrências e o Teorema Mestre]]**.
9. **Funções** — função como mapeamento; domínio, contradomínio, imagem; injetora (1-1), sobrejetora,
   bijetora; composição (∘); função inversa; funções parciais × totais; piso/teto (⌊⌋ ⌈⌉). Prática: funções
   de hash (e por que colisão = não-injetividade), mapeamentos chave→valor, idempotência (f∘f = f), funções
   puras (linka Paradigmas em prosa). Prepara o terreno de bijeção pra nota 13 (cardinalidade).
10. **Relações** — relação binária (subconjunto de A×B); propriedades (reflexiva, simétrica, antissimétrica,
    transitiva); relação de equivalência → classes e partição; ordem parcial × total (diagrama de Hasse);
    fechos (reflexivo, transitivo — fecho transitivo = alcançabilidade). Prática: ordenação topológica (DAG),
    particionamento/union-find conceitual, grafos de dependência (build, módulos), `equals` consistente.
    Linka 09 (funções são relações especiais) e ED em prosa.
11. **Combinatória: a arte de contar** — regra da soma (ou) e do produto (e); arranjos/permutações (com e
    sem repetição); combinações (n escolhe k); binômio de Newton e triângulo de Pascal; permutações
    circulares; multiconjuntos (stars and bars, leve). Prática: contar o tamanho do espaço de estados, o
    número de casos de teste, combinações de flags/configurações, número de subconjuntos (2ⁿ). Tabela de
    "com/sem ordem × com/sem repetição".
12. **Princípios combinatórios: casa dos pombos e inclusão-exclusão** — princípio da casa dos pombos
    (pigeonhole) simples e generalizado; aplicações surpreendentes (dois com mesma hash, colisão garantida,
    aniversários); princípio da inclusão-exclusão (|A∪B| = |A|+|B|−|A∩B| e a generalização); identidades de
    Pascal/Vandermonde em prosa. Prática: garantia de colisão de hash (gancho pra nota 14/19), contagem com
    sobreposição (queries com OR), contar derangements/coprimos. **A casa dos pombos é a MESMA ferramenta que
    o pumping lemma usa** — linka Teoria da Computação em prosa.
13. **Cardinalidade: contável × incontável** — bijeção como "mesmo tamanho"; conjuntos finitos × infinitos;
    ℕ, ℤ, ℚ são **contáveis** (enumeráveis) × ℝ é **incontável**; **diagonalização de Cantor** (a DONA da
    técnica); o argumento de contagem que garante o incomputável (há mais funções/linguagens que programas).
    **Linka [[03-Dominios/Fundamentos/Teoria da Computação/10 - Decidível, reconhecível e a máquina universal]]**
    (o uso: existem problemas sem máquina). Prática: por que "quase todo número real é incomputável", por que
    não há bijeção tipos↔programas.

### Magus — números, grafos e o acaso
14. **Teoria dos números: divisibilidade e primos** — divisibilidade (a | b), algoritmo da divisão (quociente
    e resto), primos, teorema fundamental da aritmética (fatoração única), MDC/MMC, **algoritmo de Euclides**
    (e por que é rápido — gancho pra Algoritmos), infinitude dos primos (prova de Euclides), crivo de
    Eratóstenes. Prática: hashing (por que módulos primos), checksums, redução de frações, gancho pra cripto.
15. **Aritmética modular (e Fermat/Euler)** — congruência (a ≡ b mod m), aritmética modular (soma/produto/
    potência), classes de resíduo, exponenciação modular rápida (square-and-multiply), inverso modular
    (quando existe — gcd=1), **Pequeno Teorema de Fermat** e generalização de **Euler** (φ), Teorema Chinês
    do Resto (leve). Prática: **RSA explicado em prosa** (sem wikilink — fronteira Segurança Conceitual),
    hashing/funções hash, CRC, dígitos verificadores (ISBN/Luhn genérico), relógio/wrap-around, overflow.
16. **Teoria dos grafos: o lado matemático** — grafo como (V, E); dirigido × não-dirigido; grau e **handshaking
    lemma** (∑grau = 2|E|); caminho, ciclo, conexidade, componentes; grafos especiais (completo Kₙ, bipartido,
    regular, ciclo, roda); **caminho/ciclo de Euler** (pontes de Königsberg — todos os graus pares) ×
    **Hamilton** (NP-difícil — gancho leve); representação (matriz × lista — linka ED). **Linka
    [[03-Dominios/Fundamentos/Estruturas de Dados/11 - Grafos - travessia e algoritmos]]** pro lado algorítmico.
17. **Grafos avançados: planaridade, coloração e matching** — planaridade (desenhar sem cruzar), **fórmula de
    Euler** (V − E + F = 2), K₅ e K₃,₃ (Kuratowski em prosa); coloração de vértices, número cromático, o
    **teorema das 4 cores**; coloração de arestas; **matching** (emparelhamento), teorema de Hall (casamento),
    bipartido. Prática: alocação de registradores (coloração), escalonamento/sudoku (coloração), atribuição
    de tarefas/pareamento (matching), detecção de conflitos. Linka 16.
18. **Árvores como objeto matemático** — definição (grafo conexo acíclico) e caracterizações equivalentes
    (n−1 arestas, caminho único entre vértices); árvore enraizada × livre; folhas, altura, profundidade;
    **contagem: fórmula de Cayley** (nⁿ⁻² árvores rotuladas), número de Catalan (árvores binárias — leve);
    **spanning trees** (árvore geradora). Fronteira com ED explícita (ED é dona da árvore como *estrutura de
    dados*; aqui é o *objeto matemático*). Linka ED em prosa.
19. **Probabilidade discreta** — espaço amostral, eventos, axiomas de Kolmogorov; probabilidade uniforme =
    contagem (liga à combinatória); probabilidade condicional, regra do produto, independência; **teorema de
    Bayes** (e a intuição de falso-positivo médico); união e complemento. Prática: **paradoxo do aniversário**
    (e a ligação com colisão de hash), análise de cache hit, testes A/B conceitual, falso-positivo de Bloom
    filter (gancho pra 21).
20. **Variáveis aleatórias e esperança** — variável aleatória; distribuição de probabilidade; **esperança**
    (valor médio) e **linearidade da esperança** (a ferramenta mais poderosa — vale mesmo com dependência);
    variância e desvio; distribuições discretas (Bernoulli, binomial, geométrica, Poisson em prosa); caudas/
    concentração (Markov/Chebyshev leve). Prática: **análise do quicksort randomizado** (comparações esperadas
    = O(n log n)), custo esperado de inserção em hash, número esperado de colisões, tempo esperado de retry.
21. **O acaso na computação: estruturas e algoritmos aleatorizados** *(showcase ED)* — por que randomizar
    (quebrar o pior caso do adversário); **Monte Carlo × Las Vegas**; **Bloom filter** (falso-positivo via
    probabilidade — fechando 19/20); **hashing universal** e por que random hash evita o pior caso;
    **skip list** (balanceamento por moeda); **power-of-two-choices** / load balancing; reservoir sampling;
    Miller-Rabin (primalidade probabilística — fecha 14/15); base probabilística de ML em prosa. **Linka
    [[03-Dominios/Fundamentos/Estruturas de Dados/12 - Estruturas especializadas - LRU, Bloom, skip list, union-find]]**.
    (Confirmar nome exato do arquivo ED/12 no scaffold.)
22. **Capstone: a matemática na vida do dev / em entrevista** — recapitula cada ramo → seu uso prático;
    **cheat-sheet mestre** (técnica de prova → quando usar; ramo da matemática → onde aparece em CS); o que
    realmente cai em entrevista (raro, mas: indução/loop invariant, Big-O/logs, probabilidade de hashing,
    grafos); "How to explain in English"; vocabulário PT→EN; armadilhas; recursos. Recapitula a torre inteira.

## Padrão por nota (house style ED — capricho)
- PT-BR, registro Feynman (analogias, perguntas retóricas, callouts, frases curtas, resumo em 1 linha —
  `> [!abstract] TL;DR` no topo e/ou `> [!summary] Resumo em uma linha` no fim).
- **Teto de prosa generoso (2400); alvo substancial ~360–520 ln.** Subagentes fazem UNDERSHOOT sistemático
  (~210–300 ln no 1º passe) e justificam com "prosa densa" — REJEITAR: o vault usa parágrafos curtos e a
  banda é real. Front-load MUITO conteúdo senior no prompt; PREVER 2ª passada de enriquecimento nos floors.
  Conferir `wc -l` REAL (auto-relato dos agentes infla).
- **4–6 diagramas Mermaid/nota** (capricho), cada um com lead-in + "leitura do diagrama". Bons pra matemática:
  `flowchart` (árvores de prova, Venn como flowchart, relações, reduções), `graph`/grafos, `stateDiagram`
  onde couber, tabelas (tabelas-verdade, regras de inferência, identidades, distribuições, comparativos).
  **NUNCA `xychart-beta`** (não renderiza no Obsidian). Símbolos LITERAIS na prosa (∀, ∃, ∈, ⊆, ⊂, ∪, ∩, ≡,
  →, ↔, ¬, ∧, ∨, ≤, ≥, Σ, ∅, φ, ℕ, ℤ, ℚ, ℝ, ⌊⌋, ⌈⌉, ∘, ≢, ≅); entidades HTML SÓ dentro de rótulos Mermaid
  e sempre entre aspas. CUIDADO: notação pesada — conferir que nenhum símbolo virou entidade HTML na prosa.
- Seção final **"## Em entrevista"** (frases EN + Vocabulário PT→EN). Callout final `> [!info] Lastro` com
  fontes VERIFICADAS via WebSearch. Canônicos: **Rosen** *Discrete Mathematics and Its Applications*;
  **Grimaldi** *Discrete and Combinatorial Mathematics*; **Graham, Knuth & Patashnik** *Concrete Mathematics*;
  **Lehman, Leighton & Meyer** *Mathematics for Computer Science* (MIT 6.042, gratuito). NÃO inventar.
- Atomicidade: linka vizinhas. `NN - Título.md` flat (sem `/` no nome — títulos com barra viram `-`).
  `publish: false` nas notas; `publish: true` só no index. Frontmatter `fase: iniciado|adepto|magus`,
  `type: concept`, `status: evergreen`, tags (`fundamentos`, `matematica-para-computacao`, fase, `entrevista`).
- **NUNCA fabricar** experiências/dados do usuário — galho teórico; cenários genéricos e exemplos canônicos
  (tabelas-verdade, indução em ∑i, RSA com números pequenos, pontes de Königsberg, paradoxo do aniversário,
  diagonalização de Cantor). [[feedback-no-fabrication]].

## Tronco e MOC
- Pasta `03-Dominios/Fundamentos/Matemática para Computação/` com `index.md` (`type: moc`, `status: growing`,
  `publish: true`, fases, rotas alternativas, dataview, "Veja também").
- Aliases do index: **"Matemática para Computação"** + **"Matemática Discreta"** + **"Discrete Mathematics"**
  + **"Math for CS"** + **"Galho - Matemática para Computação"**.
- Entra no MOC do domínio em `Fundamentos/index.md` (após Teoria da Computação) e em
  `Fundamentos/Fundamentos.md` (seção nova "## Matemática para Computação", junto/após Teoria da Computação).

## Convenções de execução
- Subagent-driven, um por nota, UMA chamada Write, house-style completo no prompt (depth front-loaded).
- Disparar por fase (Iniciado 1–4, Adepto 5–13, Magus 14–22). Conferir `wc -l` real; enriquecer floors
  ANTES de commitar a fase.
- Commits direto na main, SEM push, SEM Co-Authored-By ([[feedback-commits]]).
- Ao final de cada fase: armadilhas — `grep -nE '\[\[[^]]*$'` (wikilink partido por quebra de linha);
  entidades HTML (`&forall;` `&isin;` `&#8704;` etc.) na PROSA; NN-links vs filenames reais; validar alvos
  cross-galho (Algoritmos/02, Algoritmos/05, ED/11, ED/12, Teoria da Computação/10) com `ls`.

## Sequência de construção
1. Scaffold `Matemática para Computação/index.md` + aliases. Commit.
2. Notas por fase, uma por subagente; enriquecer floors. Commit por fase.
3. MOCs do domínio (DOIS arquivos). Checar armadilhas + NN-links + alvos externos. Atualizar memória
   `project_fundamentos_meta_plan.md` (Matemática para Computação COMPLETO; **Camada B FECHADA, 5 de 5**).
   Próximo movimento do domínio: Camada D (galhos 13–15).
