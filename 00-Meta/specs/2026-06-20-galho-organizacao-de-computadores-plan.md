---
title: "Galho Organização de Computadores — design e plano (Fundamentos, Camada D)"
created: 2026-06-20
type: plan
status: draft
publish: false
tags:
  - meta
  - plan
  - fundamentos
  - organizacao-de-computadores
---

# Galho Organização de Computadores — design e plano

## Contexto
PRIMEIRO galho da Camada D (a última), depois de Camada A (7), C (Complexidade) e **Camada B FECHADA (5/5)**.
Galho 13 do roster: "Organização de Computadores — representação binária, arquitetura de von Neumann,
hierarquia de memória, cache." Conteúdo NOVO (sem monólito-semente). Roster de **19 notas (5/7/7)** aprovado
pelo usuário em 2026-06-20 na opção **Capricho ED + Expandir** (profundidade máxima nível Estruturas de Dados +
2 splits). Depois deste: galho 14 (Segurança Conceitual) e 15 (Compiladores e Linguagens) fecham a Camada D e o domínio.

Tese do galho: onde **Sistemas Operacionais** é o *software* que gerencia a máquina, Organização de Computadores
é a *máquina* — como bits viram números, como portas viram processador, e por que o hardware tem uma
"personalidade" (cache, pipeline, especulação) que o código precisa respeitar. **Mechanical sympathy** virado fundamento.

## Decisão de fronteira (rígido — linka, não duplica)
- **Sistemas Operacionais** (galho 9, existe) — dono de memória VIRTUAL/paginação/thrashing/escalonamento (o
  SOFTWARE). Org é o HARDWARE: cache como estrutura física, hierarquia física, TLB-hardware, fetch-decode-execute.
  Eviction de página (SO/08) e eviction de linha de cache (Org/12) = MESMA ideia em escalas → linka, não reescreve.
  `[[03-Dominios/Fundamentos/Sistemas Operacionais/07 - Memória virtual e paginação]]` e `08 - Substituição de páginas e thrashing`.
- **Concorrência e Paralelismo** (galho 8, existe) — dono de modelos de memória/consistência pelo ângulo de
  sincronização. Org/15 é dona do HARDWARE: coerência de cache (MESI), barreiras no nível do hardware, false
  sharing. LINKA `[[03-Dominios/Fundamentos/Concorrência e Paralelismo/11 - Modelos de memória e consistência]]`.
- **Matemática para Computação** (galho 11, existe) — dona de bases e aritmética modular pelo ângulo MATEMÁTICO.
  Org é dona da representação de MÁQUINA: complemento de dois, IEEE 754, endianness, overflow-hardware (mod 2ⁿ).
  Nota 03 (float) LINKA `[[03-Dominios/Fundamentos/Matemática para Computação/13 - Cardinalidade - contável e incontável]]`
  (floats ≠ reais); nota 02 menciona `Matemática/15` (modular) em prosa.
- **Teoria da Computação** (galho 10, existe) — von Neumann/programa-armazenado = REALIZAÇÃO FÍSICA da máquina
  universal. Nota 07 LINKA `[[03-Dominios/Fundamentos/Teoria da Computação/10 - Decidível, reconhecível e a máquina universal]]` em prosa.
- **Estruturas de Dados / Algoritmos** — donos das estruturas e da locality como propriedade algorítmica. Org/12
  é dona da MECÂNICA do cache; ED/Algoritmos linkam pra cá ("array > lista encadeada por cache"). Linka.
- **Segurança Conceitual** (galho 14, Camada D, NÃO existe) — dona de Spectre/Meltdown como ATAQUE. Org/14 é dona
  do MECANISMO (especulação/branch prediction); side-channels só em PROSA, sem wikilink quebrado.
- **Compiladores e Linguagens** (galho 15, Camada D, NÃO existe) — dono da tradução pra ISA. Org/08-09 é dona da
  ISA/assembly como ALVO; codegen só em PROSA, sem wikilink.
- **Infraestrutura/Linux** — USAR o hardware; Org é a teoria. Não confundir.

## Assinatura ED deste galho (capricho)
Cada peça de hardware fecha com o **ângulo prático** (por que `int` estoura = overflow mod 2ⁿ; por que `0.1+0.2≠0.3`
= IEEE 754; por que matriz por linha bate por coluna = localidade espacial; por que array bate lista encadeada =
cache; false sharing = coerência; branch misprediction em hot loop). O **cluster de memória/cache (11-12) e MESI (15)**
recebe tratamento ED: matriz linha×coluna com NÚMEROS reais, `stateDiagram-v2` do MESI, tabela de latências (Jeff Dean).
O **capstone (19)** traz cheat-sheet de *mechanical sympathy* (feature de hardware → consequência no código).

## Roster de notas (19)

### Iniciado — representar e construir (os tijolos)
1. **O que é organização de computadores** *(âncora)* — organização × arquitetura; níveis de abstração (transistor →
   porta → circuito → microarquitetura → ISA → linguagem); a fronteira hardware/software; *Org é o hardware, SO é o
   software que o gerencia*; von Neumann como tema-âncora; o mapa do galho.
2. **Representação binária de inteiros** — bin/hex, unsigned × signed, **complemento de dois** (e por que ganhou),
   overflow/wrap-around (mod 2ⁿ), extensão de sinal, shifts/máscaras. Prática: `int` estoura, bit flags. Menciona
   `Matemática/15` (aritmética modular) em prosa.
3. **Ponto flutuante (IEEE 754)** — fixed × floating, sinal/expoente/mantissa, arredondamento, **`0.1+0.2≠0.3`**,
   NaN/Inf/denormais, float × double. Prática: comparar floats (epsilon), dinheiro em inteiros, cancelamento
   catastrófico. LINKA `[[03-Dominios/Fundamentos/Matemática para Computação/13 - Cardinalidade - contável e incontável]]`.
4. **Texto, endianness e alinhamento** — ASCII, Unicode/UTF-8, **big × little endian**, alinhamento e padding de
   struct. Prática: bugs de encoding/mojibake, byte order em rede/arquivos, layout de struct (data-oriented).
5. **Lógica digital: portas e circuitos combinacionais** — álgebra booleana → hardware (ponte com `Matemática/02`);
   portas, somador (half/full adder), MUX/decoder, ULA. *Como o circuito calcula.* (Ângulo lógico-matemático, não EE.)

### Adepto — a máquina que executa
6. **Circuitos sequenciais e memória** — latch, flip-flop, registrador, clock, máquina de estados; como o hardware
   *lembra*; SRAM × DRAM (e por que cada uma onde está).
7. **Arquitetura de von Neumann e o ciclo de instrução** — fetch-decode-execute; datapath (ULA, registradores, PC,
   unidade de controle); von Neumann × Harvard; o **gargalo de von Neumann**. LINKA `[[03-Dominios/Fundamentos/Teoria da Computação/10 - Decidível, reconhecível e a máquina universal]]` (realização física da UTM).
8. **ISA: a interface hardware-software** — RISC × CISC, registradores, addressing modes, tipos de instrução,
   x86/ARM/RISC-V; a ISA como "contrato". Compiladores (codegen) em prosa.
9. **Assembly e o modelo de execução** — instruções na prática, stack e calling convention, como `if`/loop/função
   viram assembly; registradores × memória.
10. **Pipeline e hazards** — pipeline de 5 estágios (MIPS), hazards (data/control/structural), forwarding, stalls,
    CPI; o paralelismo invisível dentro de um core.
11. **Hierarquia de memória e localidade** — registradores → cache → RAM → disco; localidade **temporal × espacial**;
    o **memory wall**; números de latência (a pirâmide de custos — tabela Jeff Dean). Linka SO (hierarquia).
12. **Cache a fundo** *(showcase ED)* — linha de cache, mapeamento (direto/associativo por conjuntos), política de
    escrita (write-back/through), os **3 C's de miss** (compulsory/capacity/conflict), AMAT; **código cache-friendly**
    (matriz por linha × coluna com NÚMEROS). Linka SO/08 (eviction = mesma ideia) e ED (array > lista encadeada).

### Magus — performance e paralelismo no hardware
13. **Execução fora de ordem e superescalar** — ILP, superescalar, out-of-order (Tomasulo em prosa), renomeação de
    registradores, janela de instruções; por que o hardware reordena pra esconder latência.
14. **Branch prediction e execução especulativa** — branch predictor, especulação, rollback; o custo da
    misprediction em hot loops; gancho **Spectre/Meltdown** em PROSA (mecanismo aqui; ataque na futura Segurança
    Conceitual, sem wikilink quebrado). Prática: branchless code, `likely/unlikely`.
15. **Multicore, coerência de cache e consistência** — SMP, **MESI** (`stateDiagram-v2`), *false sharing*, barreiras
    de memória no hardware; consistência sequencial × relaxada. LINKA `[[03-Dominios/Fundamentos/Concorrência e Paralelismo/11 - Modelos de memória e consistência]]`.
16. **Paralelismo de dados: SIMD e GPU** — vetorização, SIMD/AVX, GPU/SIMT, throughput × latência, o modelo de
    execução da GPU; lei de Amdahl linka (nota 18). Prática: libs numéricas, ML.
17. **Entrada e saída, interrupções e DMA** — memory-mapped I/O, polling × interrupção, DMA, o barramento; fronteira
    com SO (que *usa* esses mecanismos via syscalls/drivers). (Nome do arquivo sem barra: "Entrada e saída".)
18. **Performance: CPI, benchmarks e Amdahl** — equação do tempo de CPU (instruções × CPI × ciclo), MIPS/FLOPS,
    benchmarks (e suas armadilhas), **lei de Amdahl** (linka Concorrência/leis de escala em prosa); por que medir.
19. **Capstone: organização de computadores na vida do dev** — *mechanical sympathy*; cheat-sheet hardware →
    consequência no código; o que cai em entrevista (representação/cache/concorrência-de-hardware) × o que é cultura;
    "How to explain in English"; vocabulário PT→EN; armadilhas; recap da pilha de abstração.

## Padrão por nota (house style ED — capricho)
- PT-BR, registro Feynman (analogias, perguntas retóricas, callouts, frases curtas; `> [!abstract] TL;DR` no topo,
  `> [!summary] Resumo em uma linha` no fim).
- **Teto de prosa generoso (2400); alvo substancial ~370–520 ln.** Subagentes fazem UNDERSHOOT sistemático —
  front-load MUITO conteúdo senior; PREVER 2ª passada de enriquecimento nos floors. Conferir `wc -l` REAL.
- **4–6 diagramas Mermaid/nota** (5–6 no cluster de capricho), cada um com lead-in + "leitura do diagrama". Bons:
  `flowchart` (fetch-decode-execute, pipeline, hierarquia), `graph`/`block` (datapath), `stateDiagram-v2` (MESI,
  máquina de estados sequencial), tabelas (tabelas-verdade de portas, RISC×CISC, níveis de cache, bit-layout IEEE 754,
  latências). **NUNCA `xychart-beta`** (não renderiza no Obsidian). Símbolos LITERAIS na prosa; entidades HTML SÓ em
  rótulos Mermaid e sempre entre aspas. CUIDADO com bit-patterns/binário e operadores (`<<`, `&`, `|`) na prosa —
  não deixar virar entidade; em rótulos Mermaid, nada de `( ) { } |` crus.
- Seção final **"## Em entrevista"** (frases EN + Vocabulário PT→EN). Callout `> [!info] Lastro` com fontes
  VERIFICADAS via WebSearch. Canônicos: **Patterson & Hennessy** *Computer Organization and Design*; **Hennessy &
  Patterson** *Computer Architecture: A Quantitative Approach*; **Bryant & O'Hallaron** *Computer Systems: A
  Programmer's Perspective* (CS:APP); **Tanenbaum** *Structured Computer Organization*. NÃO inventar.
- Atomicidade: linka vizinhas. `NN - Título.md` flat (sem `/` no nome — "I/O" → "Entrada e saída"). `publish: false`
  nas notas; `publish: true` só no index. Frontmatter `fase:`, `type: concept`, `status: evergreen`, tags
  (`fundamentos`, `organizacao-de-computadores`, fase, `entrevista`).
- **NUNCA fabricar** experiências/dados do usuário — galho teórico; exemplos canônicos (somador de 1 bit, `0.1+0.2`,
  matriz linha×coluna, MESI, pipeline de 5 estágios MIPS).

## Tronco e MOC
- Pasta `03-Dominios/Fundamentos/Organização de Computadores/` com `index.md` (`type: moc`, `status: growing`,
  `publish: true`, fases, rotas, dataview, "Veja também").
- Aliases do index: **"Organização de Computadores"** + **"Arquitetura de Computadores"** + **"Computer Organization"**
  + **"Computer Architecture"** + **"Galho - Organização de Computadores"**.
- Entra no MOC do domínio em `Fundamentos/index.md` (após Matemática para Computação) e em `Fundamentos.md`
  (seção nova "## Organização de Computadores").

## Convenções de execução
- Subagent-driven, um por nota, UMA chamada Write, house-style completo no prompt (depth front-loaded).
- Disparar por fase (Iniciado 1–5, Adepto 6–12, Magus 13–19). Conferir `wc -l` real; enriquecer floors ANTES de commitar.
- Commits direto na main, SEM push, SEM Co-Authored-By. **Stage paths EXPLÍCITOS e `git diff --cached --name-only`
  antes de cada commit** (ver `feedback_git_commit_hygiene` — NUNCA `git add <pasta>`; o working tree tem trabalho
  paralelo do usuário).
- Ao final de cada fase: armadilhas — `grep -nE '\[\[[^]]*$'` (wikilink partido); entidades HTML na PROSA; wikilink
  RELATIVO (`[[../`); NN-links vs filenames reais; validar alvos cross-galho (SO/07-08, Concorrência/11, Matemática/13,
  Teoria da Computação/10) com `ls`.

## Sequência de construção
1. Scaffold `Organização de Computadores/index.md` + aliases. Commit (paths explícitos).
2. Notas por fase, uma por subagente; enriquecer floors. Commit por fase (paths explícitos).
3. MOCs do domínio (DOIS arquivos). Checar armadilhas + NN-links + alvos externos. Atualizar memória
   `project_fundamentos_meta_plan.md` (Organização de Computadores COMPLETO; Camada D 1 de 3).
   Próximo: galho 14 (Segurança Conceitual).
