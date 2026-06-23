---
title: "Organização de Computadores"
created: 2026-06-20
updated: 2026-06-20
type: moc
status: growing
publish: true
tags:
  - ciencia-da-computacao
  - organizacao-de-computadores
  - entrevista
  - moc
aliases:
  - Organização de Computadores
  - Arquitetura de Computadores
  - Computer Organization
  - Computer Architecture
  - Galho - Organização de Computadores
---

# Organização de Computadores

> [!abstract] TL;DR
> Se [[03-Dominios/Ciência/Sistemas Operacionais/index|Sistemas Operacionais]] é o *software* que gerencia
> a máquina, Organização de Computadores é a **máquina** — como bits viram números (complemento de dois, IEEE 754),
> como portas lógicas viram um processador (von Neumann, fetch-decode-execute, pipeline), e por que o hardware tem
> uma "personalidade" (cache, especulação, coerência) que o seu código precisa respeitar. É **mechanical sympathy**
> virado fundamento: por que `int` estoura, por que `0.1 + 0.2 ≠ 0.3`, por que percorrer matriz por linha bate por
> coluna, por que array bate lista encadeada na vida real.

## Sobre este galho
Este é o **andar de baixo** da Ciência da Computação: o degrau abaixo do Sistema Operacional. Ele explica a máquina física
sobre a qual todo o resto roda — e, principalmente, *por que a abstração vaza*: o desempenho do seu código depende
de detalhes de hardware (cache, pipeline, ramos) que nenhuma linguagem esconde por completo.

**Fronteiras (linka, não duplica):**
- **Memória virtual, paginação e escalonamento** → [[03-Dominios/Ciência/Sistemas Operacionais/index|Sistemas Operacionais]] (o *software* que gerencia o hardware). Aqui é o **hardware**: cache, hierarquia física, fetch-decode-execute.
- **Modelos de memória e sincronização** → [[03-Dominios/Ciência/Concorrência e Paralelismo/11 - Modelos de memória e consistência|Concorrência e Paralelismo]]. Aqui é a **coerência de cache** (MESI) e as barreiras no nível do hardware.
- **Bases numéricas e aritmética modular** → [[03-Dominios/Ciência/Matemática para Computação/index|Matemática para Computação]] (o ângulo matemático). Aqui é a **representação de máquina**: complemento de dois, IEEE 754, endianness, overflow.
- **A máquina universal** → [[03-Dominios/Ciência/Teoria da Computação/10 - Decidível, reconhecível e a máquina universal|Teoria da Computação]]. A arquitetura de von Neumann é a **realização física** dela.
- **Criptografia/side-channels (Spectre como ataque)** → futuro galho de Segurança Conceitual. Aqui é o **mecanismo** (especulação, branch prediction). **Codegen/tradução** → futuro galho de Compiladores. Aqui é a **ISA** como alvo.

**Audiência:** dev senior em preparação para entrevista internacional. Cada nota tem seção "Em entrevista" com
frases prontas em inglês e vocabulário técnico PT→EN. (Representação, cache e concorrência-de-hardware caem com
alguma frequência; o resto é cultura que afia o raciocínio de performance.)

## Iniciado — representar e construir (os tijolos)
1. [[01 - O que é organização de computadores]] — organização × arquitetura; os níveis de abstração; hardware × software; von Neumann como âncora.
2. [[02 - Representação binária de inteiros]] — complemento de dois, overflow (mod 2ⁿ), shifts e máscaras; por que `int` estoura.
3. [[03 - Ponto flutuante - IEEE 754]] — sinal/expoente/mantissa, arredondamento; por que `0.1 + 0.2 ≠ 0.3`, NaN/Inf.
4. [[04 - Texto, endianness e alinhamento]] — ASCII/Unicode/UTF-8, big × little endian, padding de struct.
5. [[05 - Lógica digital - portas e circuitos combinacionais]] — álgebra booleana → hardware; portas, somador, MUX, ULA.

## Adepto — a máquina que executa
6. [[06 - Circuitos sequenciais e memória]] — flip-flop, registrador, clock, máquina de estados; SRAM × DRAM.
7. [[07 - Arquitetura de von Neumann e o ciclo de instrução]] — fetch-decode-execute, datapath, von Neumann × Harvard, o gargalo.
8. [[08 - ISA - a interface hardware-software]] — RISC × CISC, registradores, addressing modes, x86/ARM/RISC-V.
9. [[09 - Assembly e o modelo de execução]] — instruções, stack e calling convention; como `if`/loop/função viram assembly.
10. [[10 - Pipeline e hazards]] — pipeline de 5 estágios, hazards, forwarding, stalls, CPI.
11. [[11 - Hierarquia de memória e localidade]] — registradores → cache → RAM → disco; localidade temporal × espacial; o memory wall.
12. [[12 - Cache a fundo]] — linha, associatividade, write-back/through, os 3 C's de miss; código cache-friendly (matriz linha × coluna).

## Magus — performance e paralelismo no hardware
13. [[13 - Execução fora de ordem e superescalar]] — ILP, superescalar, out-of-order, renomeação de registradores.
14. [[14 - Branch prediction e execução especulativa]] — predição de desvio, especulação, rollback; o custo da misprediction; Spectre em prosa.
15. [[15 - Multicore, coerência de cache e consistência]] — SMP, MESI, false sharing, barreiras de memória; linka Concorrência.
16. [[16 - Paralelismo de dados - SIMD e GPU]] — vetorização, SIMD/AVX, GPU/SIMT, throughput × latência.
17. [[17 - Entrada e saída, interrupções e DMA]] — memory-mapped I/O, polling × interrupção, DMA; fronteira com SO.
18. [[18 - Performance - CPI, benchmarks e Amdahl]] — equação do tempo de CPU, MIPS/FLOPS, benchmarks, lei de Amdahl.
19. [[19 - Capstone - organização de computadores na vida do dev]] — mechanical sympathy; cheat-sheet hardware → código; inglês; recap.

## Rotas alternativas

### O essencial (o que mais afeta o seu código)
02 → 03 → 11 → 12 → 15. Inteiros, floats, hierarquia de memória, cache e coerência — o quarteto da performance.

### Como a máquina executa (do bit ao programa)
05 → 06 → 07 → 08 → 09 → 10. Da porta lógica ao pipeline, passando pela ISA e pelo assembly.

### Performance e paralelismo de hardware (a fundo)
10 → 12 → 13 → 14 → 15 → 16 → 18. Pipeline, cache, OoO, especulação, multicore, SIMD e a equação de performance.

### Representação de dados (a base numérica da máquina)
02 → 03 → 04 + [[03-Dominios/Ciência/Matemática para Computação/13 - Cardinalidade - contável e incontável|por que floats não são os reais]].

## Todas as notas

```dataview
TABLE fase, status, updated
FROM "03-Dominios/Ciência/Organização de Computadores"
WHERE type = "concept"
SORT file.name ASC
```

## Veja também

- [[03-Dominios/Ciência/index|Fundamentos (MOC do domínio)]]
- [[03-Dominios/Ciência/Sistemas Operacionais/index|Sistemas Operacionais]] — o software que gerencia este hardware
- [[03-Dominios/Ciência/Concorrência e Paralelismo/index|Concorrência e Paralelismo]] — a coerência de cache pelo lado da sincronização
- [[03-Dominios/Ciência/Matemática para Computação/index|Matemática para Computação]] — bases numéricas e aritmética modular pelo lado matemático
- [[Dicionário de Ciência da Computação]]
