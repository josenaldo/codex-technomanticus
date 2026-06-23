---
title: "Galho Teoria da Computação — design e plano (Fundamentos, Camada B)"
created: 2026-06-19
type: plan
status: draft
publish: false
tags:
  - meta
  - plan
  - fundamentos
  - teoria-da-computacao
---

# Galho Teoria da Computação — design e plano

## Contexto
QUARTO galho da Camada B (depois de Paradigmas, Concorrência e Sistemas Operacionais, COMPLETOS).
Galho 10 do roster: "Teoria da Computação — autômatos, linguagens formais, computabilidade, complexidade
P/NP. (raro em entrevista, fundamento real)". Conteúdo NOVO (sem monólito). Roster de **17 notas (5/5/7)**
aprovado pelo usuário em 2026-06-19 na opção **EXPANDIR**, com house style nível ED (teto de prosa generoso,
muitos diagramas). Depois deste, só falta Matemática para Computação (11) pra fechar a Camada B.

## Decisão de fronteira (rígido — linka, não duplica)
- **Algoritmos/13 (Intratabilidade)** = FACE PRÁTICA de P/NP (NP-difícil como sinal, aproximação/heurística;
  defere o formal "pro galho Teoria da Computação"). ESTE galho é DONO do tratamento FORMAL. Notas 14/15
  **linkam** `[[03-Dominios/Ciência/Algoritmos/13 - Intratabilidade]]` e NÃO repetem a face prática.
- **Matemática para Computação** (galho 11, NÃO existe ainda) = lógica/provas/conjuntos/combinatória. Teoria
  USA prova/diagonalização mas não as ENSINA. Mencionar em PROSA, SEM wikilink quebrado.
- **Compiladores e Linguagens** (Camada D, futuro) = parsing/lexing na PRÁTICA. Teoria é dona das LINGUAGENS
  FORMAIS (regular/livre-de-contexto) e dos autômatos. Mencionar compiladores em PROSA, SEM wikilink.
- **Complexidade de Software** (galho 12, existe) = complexidade cognitiva/de manutenção — COISA OUTRA.
  NÃO confundir com complexidade computacional. NÃO linkar por engano.
- **Paradigmas de Programação** (galho 7, existe) = funcional/λ-cálculo pelo ângulo de estilo. Nota 9
  (Church-Turing) menciona λ-cálculo; pode linkar `[[Paradigmas de Programação]]` em prosa onde ilumina.

## Assinatura ED deste galho
Cada limite teórico fecha com um **resgate prático** (o equivalente ao showcase de SOs reais do galho
anterior): regex tem teto → não parseie HTML com regex; problema da parada → linter nenhum pega todo loop
infinito; Rice → análise estática perfeita não existe; NP-completo → pare de caçar o ótimo, aproxime.

## Roster de notas (17)

### Iniciado — o mundo regular (máquinas sem memória de verdade)
1. **O que é computação (e por que estudar seus limites)** *(âncora)* — o que é um modelo de computação e por
   que formalizar; decidir × reconhecer × computar função; problema = linguagem; a "torre de poder" (AF < AP <
   MT) como mapa do galho; as duas grandes perguntas (o que pode ser computado / a que custo); quem é dono de
   quê. **Linka [[03-Dominios/Ciência/Algoritmos/13 - Intratabilidade]]** (a face prática mora lá).
2. **Linguagens formais e a hierarquia de Chomsky** — alfabeto, palavra, linguagem (conjunto de palavras),
   operações (concatenação, Kleene star); gramática formal (produções); a hierarquia de Chomsky (tipo 3
   regular / 2 livre-de-contexto / 1 sensível-ao-contexto / 0 irrestrita) como mapa-mestre que organiza o
   galho inteiro, casando cada classe com sua máquina.
3. **Autômatos finitos: DFA e NFA** — estados, transições, estado inicial/aceitação; DFA × NFA; ε-transições;
   equivalência NFA↔DFA (construção de subconjuntos / subset construction); minimização (em prosa); a máquina
   sem memória. stateDiagram-v2.
4. **Linguagens regulares e expressões regulares** — teorema de Kleene (regex ↔ AF ↔ gramática regular tipo 3);
   propriedades de fechamento (união/concatenação/estrela/complemento/interseção); **por que a regex "teórica"
   não casa parênteses balanceados / HTML** (a face prática célebre — e por que as regex de PCRE com
   backreferences fogem do modelo). Compiladores/lexer em prosa.
5. **O pumping lemma para linguagens regulares** — a ferramenta de PROVAR que algo NÃO é regular; intuição do
   ciclo (memória finita → repetição forçada); o "jogo adversarial" do bombeamento; aⁿbⁿ como exemplo
   canônico; armadilhas (é condição necessária, não suficiente).

### Adepto — máquinas mais fortes e a máquina universal
6. **Autômatos de pilha e gramáticas livres de contexto** — a memória de PILHA (LIFO); GLC, derivações, árvores
   de parse, ambiguidade; aⁿbⁿ agora dá; por que linguagens de programação são (quase) livres de contexto;
   determinístico × não-determinístico (DPDA). Parsing/compiladores em PROSA.
7. **O pumping lemma para livres de contexto (e os limites das GLC)** — o pumping lemma de Bar-Hillel;
   aⁿbⁿcⁿ NÃO é livre de contexto; fechamento das LC (e o que NÃO fecha — interseção/complemento); por que
   linguagens reais precisam de checagem fora da gramática (tipos, escopo).
8. **A máquina de Turing** — fita infinita, cabeça, estados, função de transição; por que é o modelo "máximo";
   robustez (multifita, não-determinística, fita dupla — todas equivalentes); aceitar × decidir × computar
   função; configurações. stateDiagram / diagrama da fita.
9. **A tese de Church-Turing** — a convergência de modelos independentes (λ-cálculo de Church, funções
   recursivas de Gödel/Kleene, MT de Turing) no MESMO poder; a tese (afirmação sobre o mundo, NÃO um teorema);
   Turing-completude; o que torna uma linguagem Turing-completa (e curiosidades: Regra 110, Game of Life em
   prosa). **Linka [[Paradigmas de Programação]]** (funcional/λ) em prosa.
10. **Decidível, reconhecível e a máquina universal** — linguagem recursiva (decidível) × Turing-reconhecível
    (recursivamente enumerável / r.e.) × co-r.e.; a máquina universal (UTM) — a ideia que funda o computador de
    programa armazenado; **diagonalização de Cantor**: há mais linguagens que máquinas, logo EXISTEM problemas
    sem máquina (a contagem que garante o incomputável antes de exibir um).

### Magus — os muros: o incomputável e o caro
11. **O problema da parada** — o enunciado (dado P e w, P para com w?); a prova por auto-referência/diagonalização
    (a máquina que faz o oposto do que se prevê); por que é o resultado mais famoso; **resgate prático: nenhum
    linter/IDE detecta TODO loop infinito estaticamente — é matematicamente impossível, não preguiça de quem
    escreveu a ferramenta.**
12. **Reduções e indecidibilidade em cascata** — redução de mapeamento (many-one); a lógica "se eu resolvesse B
    eu resolveria a parada, logo B é indecidível"; exemplos clássicos (linguagem vazia? duas MTs equivalentes?
    aceita-w?); como a indecidibilidade se ESPALHA a partir da parada. flowchart de reduções.
13. **O teorema de Rice** — TODA propriedade não-trivial do COMPORTAMENTO (da linguagem reconhecida) é
    indecidível; a generalização do halting; **resgate prático: por que análise estática perfeita é impossível**
    — "esse código sempre termina?", "esses dois programas são equivalentes?", "esse método tem efeito
    colateral?" são todos indecidíveis no caso geral; todo verificador é incompleto OU pode não terminar.
    Análise estática/testes em prosa (linka `[[Testes]]` em prosa onde couber).
14. **Complexidade computacional formal: classes de tempo, P e NP** — MT com relógio (tempo como função do
    tamanho da entrada); a classe **P** (decidível em tempo polinomial = "tratável"); a classe **NP** (duas
    definições equivalentes: verificável em tempo polinomial / MT não-determinística); por que P ⊆ NP; o
    certificado/testemunha. ESTE é o formalismo que `[[03-Dominios/Ciência/Algoritmos/13 - Intratabilidade]]`
    deferiu — linka de volta.
15. **NP-completude: Cook-Levin e a cadeia de Karp** — redução polinomial (≤ₚ); NP-difícil × NP-completo;
    **teorema de Cook-Levin** (SAT é NP-completo — o primeiro, do qual todos descendem); a cascata de 21
    problemas de Karp; como se PROVA NP-completude (reduzir um NP-completo conhecido ao seu problema);
    **resgate prático: reconhecer NP-completo em entrevista** (cheira a empacotar/agendar/rotear → provavelmente
    NP-difícil → pare de caçar o ótimo).
16. **P vs NP e o mapa das classes** — a pergunta do milênio (vale US$ 1mi); por que (quase) todos apostam
    P ≠ NP; PSPACE, EXPTIME; os teoremas de hierarquia (tempo/espaço — mais tempo/espaço resolve estritamente
    mais, em prosa); o mapa P ⊆ NP ⊆ PSPACE ⊆ EXPTIME e onde mora o NP-completo; co-NP em prosa. flowchart do mapa.
17. **Capstone: a teoria da computação na vida do dev / em entrevista** — o panorama: cada limite → o que te diz
    na prática (regex tem teto → não parseie HTML; Rice → análise estática é heurística; halting → linters são
    incompletos; NP-completo → aproxime); reconhecer a classe de um problema no trabalho; "How to explain in
    English"; vocabulário PT→EN; armadilhas comuns; recursos. Recapitula a torre inteira.

## Padrão por nota (house style ED)
- PT-BR, registro Feynman (analogias, perguntas retóricas, callouts, frases curtas, resumo em 1 linha — TL;DR).
- **Teto de prosa generoso (2400); alvo substancial ~360–500 ln.** Subagentes fazem UNDERSHOOT sistemático —
  front-load MUITO conteúdo senior no prompt e PREVER 2ª passada de enriquecimento nos floors por fase.
- **3–5 diagramas Mermaid/nota** (4–6 onde rende), cada um com lead-in + "leitura do diagrama". Excelentes:
  `stateDiagram-v2` (DFA/NFA/MT), `flowchart` (Chomsky, reduções, mapa P/NP/PSPACE), tabelas (classes,
  fechamento, comparativos). **NUNCA `xychart-beta`** (não renderiza no Obsidian). Entidades HTML SÓ em rótulos
  Mermaid e entre aspas; símbolos LITERAIS na prosa (×, →, ∈, ∅, ⊆, ε, Σ, etc.).
- **Seção final "Em entrevista"** — frases EN + vocabulário PT→EN. (Tema é "raro" em entrevista, mas mantém.)
- Fontes VERIFICADAS via WebSearch; callout `> [!info] Lastro`. Canônicos: **Sipser** *Introduction to the
  Theory of Computation*; **Hopcroft, Motwani & Ullman** *Introduction to Automata Theory*; **Arora & Barak**
  *Computational Complexity* (pra P/NP); Cook (1971) e Karp (1972) pros artigos fundacionais. NÃO inventar.
- Atomicidade: linka vizinhas. `NN - Título.md` flat (sem `/` no nome). `publish: false` nas notas;
  `publish: true` só no index. Frontmatter `fase:`, `type: concept`, `status: evergreen`, tags.
- **NUNCA fabricar** experiências/dados do usuário — galho teórico; cenários genéricos e exemplos canônicos
  (a*b*, aⁿbⁿ, o problema da parada, SAT, caixeiro-viajante).

## Tronco e MOC
- Pasta `03-Dominios/Ciência/Teoria da Computação/` com `index.md` (`type: moc`, `status: growing`,
  `publish: true`, fases, rotas, dataview, "Veja também").
- Aliases do index: **"Teoria da Computação"** + **"Teoria da Computação"** + **"Computability"** +
  **"Theory of Computation"** + **"Galho - Teoria da Computação"**.
- Entra no MOC do domínio em `Fundamentos/index.md` e `Fundamentos.md`.

## Convenções de execução
- Subagent-driven, um por nota, UMA chamada Write, house-style completo no prompt (depth front-loaded).
- Disparar por fase (Iniciado 1–5, Adepto 6–10, Magus 11–17). Conferir `wc -l` real; enriquecer floors.
- Commits direto na main, SEM push, SEM Co-Authored-By.
- Ao final: armadilhas (grep wikilink partido, entidades HTML na prosa, NN-links inexistentes); MOCs do domínio;
  atualizar memória `project_fundamentos_meta_plan.md` (Teoria da Computação COMPLETO; Camada B 4 de 5).

## Sequência de construção
1. Scaffold `Teoria da Computação/index.md` + aliases. Commit.
2. Notas por fase, uma por subagente; enriquecer floors. Commit por fase.
3. MOCs do domínio. Checar armadilhas + NN-links + alvos externos. Atualizar memória.
   Próximo na Camada B: Matemática para Computação (11) — fecha a Camada B.
