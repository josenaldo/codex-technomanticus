---
title: "Compiladores e Linguagens"
created: 2026-06-21
updated: 2026-06-21
type: moc
status: growing
publish: true
tags:
  - fundamentos
  - compiladores
  - entrevista
  - moc
aliases:
  - Compiladores e Linguagens
  - Compiladores
  - Construção de Compiladores
  - Linguagens de Programação (implementação)
  - Galho - Compiladores e Linguagens
---

# Compiladores e Linguagens

> [!abstract] TL;DR
> Um compilador não é mágica — é uma **série de traduções**, e cada uma é uma estrutura de dados que você pode
> desenhar. O texto vira uma stream de **tokens** (análise léxica), os tokens viram uma **árvore** (parsing),
> a árvore ganha **significado** e tipos (análise semântica), o significado vira uma **representação
> intermediária** otimizável, e a IR vira **código de máquina**. Este galho é a *engenharia* desse pipeline:
> como você constrói um scanner a partir de regex, um parser à mão (recursive descent) ou por tabela (LR), um
> type-checker, um otimizador (dataflow + SSA), um gerador de código com alocação de registradores — e o que
> acontece em runtime (stack frames, garbage collection, JIT). O fio: a teoria (autômatos, gramáticas) é a
> *ferramenta*; o assunto é a *construção do tradutor*. Por que recursive descent domina a indústria, por que
> SSA facilita otimização, por que o JIT pode bater o AOT, e por que você não pode confiar nem no compilador
> que compilou seu compilador.

## Sobre este galho
Onde **Teoria da Computação** pergunta *que linguagens são reconhecíveis, e por qual máquina abstrata*,
Compiladores e Linguagens pergunta *como eu construo, na prática, a máquina que lê uma linguagem real e a
traduz em algo que roda*. A teoria prova que uma linguagem é reconhecível; este galho **constrói o
reconhecedor** — e depois o otimizador, o gerador de código e o runtime. É a ponte entre o código que você
escreve e os elétrons que correm no silício: o andar conceitual que torna inteligível por que o build é lento,
por que aquela mensagem de erro apareceu, e o que um transpiler, um linter ou um Language Server realmente
fazem por baixo.

**Fronteiras (linka, não duplica):**
- **A teoria de autômatos e linguagens formais** (DFA/NFA, regex como objeto formal, CFG, pumping lemma) → [[03-Dominios/Ciência/Teoria da Computação/index|Teoria da Computação]]. Aqui é o **aplicado**: construir um scanner a partir de regex, um parser a partir de uma gramática.
- **A ISA e o assembly como objeto** (von Neumann, registradores, modos de execução) → [[03-Dominios/Ciência/Organização de Computadores/index|Organização de Computadores]]. Aqui o assembly é o **alvo** que o back-end emite.
- **Sistemas de tipos como ideia de design** (estático × dinâmico, nominal × estrutural) → [[03-Dominios/Ciência/Paradigmas/13 - Sistemas de tipos|Paradigmas]]. Aqui é o **algoritmo** de checagem e inferência.
- **Processo, memória virtual e carregamento** como mecanismo do SO → [[03-Dominios/Ciência/Sistemas Operacionais/index|Sistemas Operacionais]]. Aqui é o ângulo do **compilador/toolchain** (o que o linker resolve, o layout que o código assume).
- **"Trusting Trust" como confiança sob adversário** → [[03-Dominios/Engenharia/Segurança/17 - Confiança transitiva e Trusting Trust|Segurança Conceitual]]. Aqui é o **mecanismo do compilador** que se auto-infecta.
- **Usar uma toolchain específica** (configurar LLVM, escrever um plugin de Babel) → prática, fora deste galho. Aqui é a **teoria** da construção; LLVM/V8/HotSpot/yacc entram como ilustração nomeada.

**Audiência:** dev senior em preparação para entrevista internacional. Cada nota tem seção "Em entrevista" com
frases prontas em inglês e vocabulário técnico PT→EN. (Compilação × interpretação, o que é uma AST, como um
parser funciona e o que é garbage collection caem com frequência real; o resto é a cultura que separa quem
*usa* uma linguagem de quem *entende* como ela é construída — e que torna você muito melhor a debugar.)

## Iniciado — o panorama e o front-end
1. [[01 - O que é um compilador e o pipeline de tradução]] — front-end × middle × back-end, as fases, fonte → executável, por que separar.
2. [[02 - Compilação, interpretação e JIT]] — o espectro de execução, AOT × interpretação × JIT, bytecode/VMs, a falsa dicotomia.
3. [[03 - Análise léxica - do texto a tokens]] — scanner, lexema × token × padrão, regex na prática, maximal munch, lexer generators.
4. [[04 - Gramáticas e a árvore sintática]] — CFG na prática (BNF/EBNF), parse tree × AST, ambiguidade, precedência e associatividade.
5. [[05 - Recursive descent e Pratt parsing]] — um parser à mão, top-down preditivo, precedence climbing, recursão à esquerda.
6. [[06 - A AST e o padrão visitor]] — a árvore sintática abstrata, nós tipados, o visitor, múltiplas passadas.

## Adepto — o miolo de engenharia
7. [[07 - Parsing top-down formal]] — LL(k), FIRST e FOLLOW, tabela preditiva LL(1), dirigido por tabela × por código.
8. [[08 - Parsing bottom-up]] — shift-reduce, LR/SLR/LALR, o autômato de itens, conflitos, yacc/bison/ANTLR.
9. [[09 - Tabela de símbolos, escopo e resolução de nomes]] — name resolution, escopo léxico × dinâmico, shadowing, binding.
10. [[10 - Análise semântica e checagem de tipos]] — o que a sintaxe não captura, type checking, inferência (Hindley-Milner), unificação.
11. [[11 - Representação intermediária e SSA]] — por que um meio-termo, three-address code, CFG, SSA, LLVM IR, o desacoplamento N+M.
12. [[12 - Otimização]] — dataflow analysis, constant folding/DCE/CSE/inlining, -O0/-O2/-O3, o limite da indecidibilidade.

## Magus — back-end, runtime e fronteiras
13. [[13 - Geração de código e seleção de instruções]] — da IR ao assembly, instruction selection, ABI/calling conventions.
14. [[14 - Alocação de registradores]] — temporários × registradores físicos, graph coloring, spilling, linear scan, NP-completude.
15. [[15 - Runtime, stack frames e gestão de memória]] — activation record, pilha de chamadas, stack × heap, calling conventions.
16. [[16 - Garbage collection]] — reference counting × tracing, mark-and-sweep, copying, generational, throughput × latência.
17. [[17 - JIT a fundo]] — tiered compilation, profile-guided optimization, inline caches, speculation e deoptimização, V8/HotSpot.
18. [[18 - Capstone - compiladores na vida do dev]] — o pipeline end-to-end, transpilers/LSP/WASM, cheat-sheet estágio → estrutura.
19. [[19 - Linking e loading]] — resolução de símbolos, relocação, static × dynamic linking, o loader, ELF.
20. [[20 - Bootstrapping, self-hosting e o ataque de Thompson]] — o ovo e a galinha, self-hosting, cross-compilation, Trusting Trust, DDC.

## Rotas alternativas

### O essencial (o que mais cai em entrevista)
01 → 02 → 06 → 16. O pipeline, compilação × interpretação, o que é uma AST e o que é garbage collection — o quarteto que aparece em entrevista de verdade.

### A trilha do front-end (do texto à árvore)
03 → 04 → 05 → 06 → 07 → 08. Léxica, gramática, parser à mão, AST, e a teoria formal de parsing top-down e bottom-up.

### A trilha do back-end (da árvore ao silício)
06 → 10 → 11 → 12 → 13 → 14. AST, semântica, IR/SSA, otimização, geração de código e alocação de registradores.

### A trilha do runtime (o que acontece quando roda)
02 → 15 → 16 → 17 → 19. Execução, stack frames, garbage collection, JIT e linking/loading.

## Todas as notas

```dataview
TABLE fase, status, updated
FROM "03-Dominios/Ciência/Compiladores e Linguagens"
WHERE type = "concept"
SORT file.name ASC
```

## Veja também

- [[03-Dominios/Ciência/index|Fundamentos (MOC do domínio)]]
- [[03-Dominios/Ciência/Teoria da Computação/index|Teoria da Computação]] — a teoria de autômatos e gramáticas que o front-end aplica
- [[03-Dominios/Ciência/Organização de Computadores/index|Organização de Computadores]] — a ISA e o assembly que o back-end emite
- [[03-Dominios/Ciência/Paradigmas/13 - Sistemas de tipos|Sistemas de tipos]] — os tipos como design; aqui é o algoritmo de checagem
- [[03-Dominios/Engenharia/Segurança/17 - Confiança transitiva e Trusting Trust|Trusting Trust]] — o ataque de Thompson pelo ângulo de confiança
- [[Dicionário de Fundamentos]]
