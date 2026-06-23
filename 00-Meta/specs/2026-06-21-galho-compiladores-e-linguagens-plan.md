---
title: "Galho Compiladores e Linguagens — design e plano (Fundamentos, Camada D)"
created: 2026-06-21
type: plan
status: draft
publish: false
tags:
  - meta
  - plan
  - fundamentos
  - compiladores
---

# Galho Compiladores e Linguagens — design e plano

## Contexto
TERCEIRO e ÚLTIMO galho da Camada D — e a **última peça do domínio Fundamentos inteiro** (15 galhos).
Depois de Camada A (7), C (Complexidade), **Camada B FECHADA (5/5)** e da Camada D 2/3 (13 Organização
de Computadores ✓ · 14 Segurança Conceitual ✓), este galho fecha tudo. Galho 15 do roster: "Compiladores
e Linguagens — análise léxica, parsing, AST, interpretação vs. compilação." Conteúdo NOVO (sem
monólito-semente). Roster de **20 notas (6/6/8)** aprovado pelo usuário em 2026-06-21 na opção
**base 18 + expandir 19/20** (recomendada): a base de 18 notas (6/6/6) foi expandida com 2 notas Magus —
**Linking e loading** (fronteira com SO) e **Bootstrapping, self-hosting e o ataque de Thompson** (callback
elegante ao galho 14, Segurança, recém-fechado).

Tese do galho: **um compilador é uma série de traduções que tornam o código humano executável pela máquina —
e cada estágio é uma estrutura de dados, não mágica.** Onde Teoria da Computação pergunta "que linguagens são
reconhecíveis e por qual máquina abstrata", Compiladores pergunta "como eu *construo*, na prática, a máquina
que lê uma linguagem real e a traduz". É a **engenharia** do pipeline: do texto a tokens, de tokens a árvore,
de árvore a significado, de significado a uma representação intermediária, e dela a código que roda. O fio: a
teoria (autômatos, gramáticas) é a *ferramenta*; o assunto é a *construção* do tradutor e o que acontece em
tempo de execução.

## Decisão de fronteira (rígido — linka, não duplica)
- **Teoria da Computação** (galho 10, existe) — dona da TEORIA: autômatos finitos (DFA/NFA), linguagens
  regulares e expressões regulares como objeto formal, hierarquia de Chomsky, gramáticas livres de contexto e
  autômatos de pilha, o pumping lemma. As notas 03 (léxica) e 04 (gramáticas) deste galho **LINKAM**
  `[[03-Dominios/Ciência/Teoria da Computação/03 - Autômatos finitos - DFA e NFA]]`,
  `[[03-Dominios/Ciência/Teoria da Computação/04 - Linguagens regulares e expressões regulares]]` e
  `[[03-Dominios/Ciência/Teoria da Computação/06 - Autômatos de pilha e gramáticas livres de contexto]]`
  e usam o *aplicado* (construir um scanner a partir de regex; construir um parser a partir de uma CFG) —
  NUNCA reescrevem a teoria de autômatos nem o pumping lemma. A regra de ouro: Teoria prova *que* uma
  linguagem é reconhecível; Compiladores *constrói* o reconhecedor.
- **Organização de Computadores** (galho 13, existe) — dona da ISA e do assembly como objeto
  (von Neumann, registradores, modos de execução). As notas 13 (geração de código) e 15 (runtime) deste galho
  **LINKAM** `[[03-Dominios/Ciência/Organização de Computadores/08 - ISA - a interface hardware-software]]`
  e `[[03-Dominios/Ciência/Organização de Computadores/09 - Assembly e o modelo de execução]]` e tratam o
  assembly como *alvo* (o que o back-end emite), sem reensinar a ISA.
- **Paradigmas de Programação** (galho 7, existe) — dono dos SISTEMAS DE TIPOS como ideia de design
  (estático × dinâmico, nominal × estrutural, o que um tipo significa). A nota 10 deste galho (análise
  semântica) **LINKA** `[[03-Dominios/Ciência/Paradigmas/13 - Sistemas de tipos]]` e é dona do
  *algoritmo* de checagem/inferência (como o compilador *verifica* tipos), não da taxonomia de sistemas.
- **Sistemas Operacionais** (galho 9, existe) — dono de processo, memória virtual e do carregamento de
  programas como MECANISMO DO SO. As notas 15 (runtime/stack frames) e 19 (linking e loading) deste galho
  **LINKAM** `[[03-Dominios/Ciência/Sistemas Operacionais/index]]` e são donas do ângulo do *compilador/
  toolchain* (o que o linker resolve, o layout que o compilador assume); a execução do processo é do SO.
- **Segurança Conceitual** (galho 14, existe) — dona de "Trusting Trust" pelo ângulo de confiança sob
  adversário. A nota 20 deste galho (bootstrapping/self-hosting) **LINKA**
  `[[03-Dominios/Engenharia/Segurança/17 - Confiança transitiva e Trusting Trust]]` e é dona do
  ângulo do *compilador* (o mecanismo técnico do compilador que se auto-infecta, bootstrapping, self-hosting);
  Segurança é dona do ângulo de supply-chain/confiança.
- **Estruturas de Dados** (galho 1, existe) — dona de árvores e do percurso. A nota 06 (AST/visitor) menciona
  a árvore como estrutura e pode linkar, mas é dona do *uso compilador* (a AST como espinha do front-end).
- **Compiladores na prática / build de uma linguagem real / LLVM tutorial** — *usar* uma toolchain específica
  (escrever um plugin de Babel, configurar o LLVM, mexer no GCC) é prática, não fundamento. Fica de fora;
  este galho é a TEORIA da construção. Conceitos canônicos (LLVM IR, V8, HotSpot, yacc) entram como
  *ilustração nomeada*, não como tutorial.

## Assinatura ED deste galho (capricho)
Cada estágio do pipeline fecha com **o artefato concreto** que entra e sai (o "antes e depois" da tradução):
o que é um token vs. um lexema, como uma `2 + 3 * 4` vira uma árvore que respeita precedência, por que a AST
descarta parênteses que a parse tree guarda, como `x + 1` vira three-address code, por que SSA facilita
otimização, como um `if` vira saltos condicionais. O **cluster front-end (03–06)** recebe tratamento ED: um
*worked example* contínuo (uma mini-linguagem de expressões aritméticas) atravessa léxica → parsing →
AST, mostrando o mesmo input em cada representação. A **nota 02** (compilação × interpretação × JIT) traz a
tabela comparativa canônica + o espectro AOT↔JIT↔interpretador puro. A **nota 17** (JIT) recria o ciclo
warmup → profiling → otimização → deoptimização do HotSpot/V8. O **capstone (18)** traz um pipeline
end-to-end de uma expressão da fonte ao assembly e o cheat-sheet "estágio → entrada → saída → estrutura".

## Roster de notas (20)

### Iniciado — o panorama e o front-end (6)
1. **O que é um compilador e o pipeline de tradução** *(âncora)* — o compilador como tradutor; front-end ×
   middle-end × back-end; as fases (léxica → sintática → semântica → IR → otimização → geração); fonte →
   objeto → executável; o "ne plus ultra" do livro do dragão como mapa; por que separar em fases (modularidade,
   reuso, portabilidade — N linguagens × M alvos vira N+M com um IR comum).
2. **Compilação × interpretação × JIT** — o espectro de execução; AOT (compila tudo antes) × interpretação
   (executa a AST/bytecode direto) × JIT (compila em runtime o que é quente); bytecode e VMs (JVM, CPython,
   V8); transpilação (fonte → fonte); a tabela de trade-offs (velocidade de execução × velocidade de
   inicialização × portabilidade); por que "linguagem compilada vs. interpretada" é uma falsa dicotomia
   (é o *implementador* que escolhe, não a linguagem).
3. **Análise léxica — do texto a tokens** — o scanner/lexer; lexema × token × padrão; do regex ao autômato na
   *prática* (a teoria é de Teoria da Computação — linka); maximal munch (longest match); tokens com atributos
   (lexema, posição); whitespace/comentários e o que o lexer descarta; lexer generators (lex/flex) como ideia;
   erros léxicos. *(fronteira c/ Teoria — linka DFA/NFA e regex)*.
4. **Gramáticas e a árvore sintática** — a gramática livre de contexto na prática (BNF/EBNF); terminais ×
   não-terminais, produções, derivação; parse tree × AST (o que cada uma guarda); ambiguidade (o
   dangling-else, a associatividade/precedência) e como resolvê-la; o que o parser faz com a stream de tokens.
   *(fronteira c/ Teoria — linka CFG e autômatos de pilha)*.
5. **Recursive descent e Pratt parsing** — escrevendo um parser à mão; top-down preditivo; uma função por
   não-terminal; como codar precedência e associatividade (precedence climbing / Pratt parsing); por que
   recursão à esquerda quebra recursive descent e como eliminá-la; por que parsers escritos à mão dominam
   compiladores de produção (mensagens de erro, recuperação).
6. **A AST e o padrão visitor** — a árvore sintática abstrata como espinha do compilador; nós tipados
   (expressões, statements, declarações); por que a AST é a estrutura que todos os estágios seguintes
   atravessam; o **padrão visitor** (separar operação da estrutura — type-check, otimização, geração são
   visitas); travessia e múltiplas passadas. *(linka Estruturas de Dados — árvore)*.

### Adepto — o miolo de engenharia (6)
7. **Parsing top-down formal** — a teoria por trás do recursive descent; gramáticas LL(k); conjuntos FIRST e
   FOLLOW; a tabela de parsing preditivo (LL(1)); parsing dirigido por tabela × dirigido por código; o que
   torna uma gramática LL(1) e por que algumas linguagens não são.
8. **Parsing bottom-up** — shift-reduce; LR(0), SLR, LR(1), LALR; o autômato de itens (a "pilha de estados");
   por que LR reconhece mais gramáticas que LL; conflitos shift-reduce e reduce-reduce; geradores
   (yacc/bison/ANTLR) e por que a academia ama LR mas a indústria escreve recursive descent à mão.
9. **Tabela de símbolos, escopo e resolução de nomes** — name resolution; a tabela de símbolos como estrutura;
   escopo léxico × dinâmico; aninhamento de escopos (pilha de tabelas / scoping chains); shadowing; binding
   (ligar um uso à sua declaração); forward references; namespaces. *(o coração da análise semântica)*.
10. **Análise semântica e checagem de tipos** — o que a sintaxe não captura (um programa sintaticamente
    válido pode ser semanticamente errado); type checking estático; a **inferência de tipos** (Hindley-Milner
    em alto nível — unificação como ideia); checagem de tipos × coerção; o que o compilador verifica antes de
    deixar o código rodar. *(fronteira c/ Paradigmas — linka Sistemas de tipos como design)*.
11. **Representação intermediária (IR) e SSA** — por que um meio-termo entre AST e assembly; IR de alto ×
    baixo nível; three-address code; o grafo de fluxo de controle (CFG — control-flow graph); **SSA**
    (Static Single Assignment) e por que assignar cada variável uma vez facilita otimização; LLVM IR como
    exemplo canônico; o IR como ponto de desacoplamento N+M.
12. **Otimização** — o que é uma otimização correta (preserva semântica); local × global × interprocedural;
    **dataflow analysis** (liveness, reaching definitions) como o motor; otimizações clássicas (constant
    folding, dead code elimination, common subexpression elimination, inlining, loop-invariant code motion);
    por que "otimização prematura" e por que -O0/-O2/-O3 existem; o limite (problema da parada → otimização
    perfeita é indecidível, linka Teoria).

### Magus — back-end, runtime e fronteiras (8)
13. **Geração de código e seleção de instruções** — da IR ao assembly; instruction selection (casar padrões
    da IR a instruções da ISA); ordenação de instruções (scheduling) em alto nível; ABI e calling conventions
    como contrato; macro × micro (tree pattern matching, BURS como ideia). *(fronteira c/ Org — linka ISA e
    assembly como alvo)*.
14. **Alocação de registradores** — o problema: infinitos temporários da IR × poucos registradores físicos;
    **graph coloring** (o grafo de interferência, coloração); spilling (quando derramar para a memória);
    liveness como insumo; linear scan (o algoritmo dos JITs) × graph coloring; por que é NP-completo (linka
    Teoria) e por que heurísticas ganham.
15. **Runtime, stack frames e gestão de memória** — o que o compilador assume sobre a execução; o stack frame
    (activation record): parâmetros, locais, return address, saved registers; a pilha de chamadas; stack ×
    heap; calling conventions (quem salva o quê); o runtime mínimo de uma linguagem. *(fronteira c/ Org e SO —
    linka modelo de execução e processo)*.
16. **Garbage collection** — gestão automática de memória; reference counting (e o problema dos ciclos);
    tracing GC (mark-and-sweep); copying / semi-space; **generational** (a hipótese geracional — a maioria dos
    objetos morre jovem); stop-the-world × concurrent × incremental; o trade-off throughput × latência (pausas);
    GC × gestão manual × ownership (Rust).
17. **JIT a fundo** — compilação em tempo de execução; interpretador → baseline JIT → optimizing JIT (tiered
    compilation); **profile-guided optimization** (otimizar com dados reais de execução); inline caches;
    speculation e **deoptimização** (assumir e desfazer quando a aposta falha); warmup; V8 (TurboFan) e HotSpot
    (C1/C2) como exemplos canônicos; por que JIT pode bater AOT.
18. **Capstone — compiladores na vida do dev** — o pipeline end-to-end de uma expressão (fonte → tokens → AST
    → IR → assembly); por que entender o compilador melhora você (ler mensagens de erro, entender por que o
    build é lento, transpilers/Babel/TypeScript, source maps, linters e LSP como mini-front-ends, WASM como
    alvo universal); cheat-sheet "estágio → entrada → saída → estrutura"; recap + inglês de entrevista.
19. **Linking e loading** — depois que o compilador emite código objeto, falta juntar tudo; o **linker**
    (resolução de símbolos, relocação); static × dynamic linking; bibliotecas estáticas (.a) × dinâmicas
    (.so/.dll); o **loader** (carregar o executável na memória, resolver símbolos dinâmicos em runtime);
    formatos (ELF como exemplo); por que erros de link são diferentes de erros de compilação. *(fronteira c/
    SO — linka carregamento de processo)*.
20. **Bootstrapping, self-hosting e o ataque de Thompson** — o problema do ovo e da galinha (com o que se
    compila o primeiro compilador?); bootstrapping (escrever o compilador na própria linguagem); self-hosting;
    cross-compilation; o **ataque de Ken Thompson** (*Reflections on Trusting Trust*): um compilador que se
    auto-infecta e some do código-fonte; a defesa (diverse double-compiling de David A. Wheeler).
    *(fronteira c/ Segurança — linka Trusting Trust pelo ângulo de confiança)*.

## House style (espelhar galhos 13/14 — Organização de Computadores e Segurança Conceitual)
- PT-BR, registro Feynman (analogias, perguntas retóricas, callouts). Banda **~450–540 ln/nota** (âncora e
  capstone podem ir a ~570). **Piso explícito por nota no prompt** do subagente.
- **4–6 diagramas Mermaid** por nota (NUNCA `xychart-beta`). `flowchart` pro pipeline de fases, fluxo de
  tradução, CFG, grafo de interferência; `graph` pra taxonomias (tipos de IR, espectro de execução,
  classes de otimização); `sequenceDiagram` pro ciclo JIT (warmup/deopt), resolução de símbolos no link;
  `stateDiagram-v2` pro autômato de scanner, máquina de estados do parser, ciclo de vida de objeto no GC.
  Todo diagrama seguido de callout `> [!info] Leitura do diagrama`.
- Símbolos Unicode **LITERAIS** na prosa (≠, ≥, →, ×, ⊕); entidades HTML (`&rarr;`, `&times;`, `&ne;`) só
  dentro de rótulos Mermaid entre aspas. Cerca de diagrama SEMPRE ` ```mermaid ` (2ª linha = tipo, ex.
  `flowchart LR`); NUNCA abrir a cerca com o tipo.
- Frontmatter idêntico ao template: `type: concept`, `fase: iniciado|adepto|magus`, `status: evergreen`,
  **`publish: false`** nas notas (só o index é `true`), tags `[fundamentos, compiladores, <fase>, entrevista]`.
- Seções canônicas: `> [!abstract] TL;DR` no topo; corpo com `---` entre seções; `## Conexões` (anterior/
  próxima + cross-links); `> [!summary] Resumo em uma linha`; `## Em entrevista` (frases em inglês em itálico +
  tabela Vocabulário PT→EN); `> [!info] Lastro` ao final com fontes verificadas via WebSearch.
- Callouts variados: `tip`, `warning`, `success`, `example`, `danger` pras armadilhas (ex.: recursão à
  esquerda, nonce... não — aqui: maximal munch, conflitos shift-reduce, deoptimização, ciclos no refcount).

## Plano de execução (subagent-driven, 1 subagente por nota)
1. **Scaffold** (este plano + index.md) → commit com paths explícitos.
2. **Fase Iniciado (01–06)** → 6 subagentes, 1 por nota, UMA Write cada, house style completo no prompt →
   conferir `wc -l` REAL → 2ª passada de enriquecimento nos floors → commit.
3. **Fase Adepto (07–12)** → idem, 6 notas → commit.
4. **Fase Magus (13–20)** → idem, 8 notas → commit.
5. **MOCs do domínio** (`03-Dominios/Ciência/index.md` + `Fundamentos.md`) apontam ao galho → commit.
6. Checks finais: NN-links resolvem, cross-galho verificados, zero link quebrado/relativo, zero xychart, zero
   entidade HTML na prosa, `[[...]]` literal só dentro de code fence, todas as cercas = `mermaid`. Atualizar
   memória (Camada D 3/3 → domínio Fundamentos COMPLETO).

## Lições dos galhos 13/14 (aplicar)
- Subagentes fazem UNDERSHOOT sistemático no 1º passe. **Front-load conteúdo senior no prompt + piso de linhas
  explícito por nota** quase eliminou o undershoot no galho 14 — manter. Conferir `wc -l` REAL (auto-relato
  infla); prever 2ª passada de enriquecimento só se ficar abaixo do piso.
- **Git hygiene (crítico):** NUNCA `git add <pasta>`; sempre paths EXPLÍCITOS + conferir
  `git diff --cached --name-only` antes de commitar — o working tree tem trabalho paralelo do usuário
  (renumeração da Anatomia dos LLMs). Commits direto na `main`, SEM push, SEM Co-Authored-By.
- NUNCA fabricar experiências/dados do usuário (galho teórico → exemplos canônicos: o livro do dragão,
  yacc/bison/ANTLR, LLVM IR, V8/TurboFan, HotSpot C1/C2, CPython, Thompson 1984, Wheeler DDC — todos
  verificáveis e citados no Lastro).
- EVITAR `[[...]]` literal fora de code fence. Corrigir cerca de diagrama que abra com o tipo (lição do
  galho 14, nota 02, que abriu com ` ```flowchart `).
