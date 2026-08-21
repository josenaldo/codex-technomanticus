---
title: "Sistemas Operacionais"
created: 2026-06-18
updated: 2026-06-18
type: moc
status: growing
publish: true
tags:
  - ciencia-da-computacao
  - sistemas-operacionais
  - entrevista
  - moc
aliases:
  - Sistemas Operacionais
  - Sistema Operacional
  - SO
  - Operating Systems
  - Galho - Sistemas Operacionais
---

# Sistemas Operacionais

> [!abstract] TL;DR
> Galho de Ciência da Computação sobre a **teoria** do software que fica entre seus programas e o hardware — o sistema operacional. Cobre as abstrações que ele inventa (processos, threads, memória virtual, arquivos), os mecanismos com que as sustenta (system calls, escalonamento, paginação, I/O, journaling) e a divergência entre os SOs reais (Linux, Windows, macOS). Não é "como usar o Linux" — é **como o SO funciona por dentro** e por que isso explica metade dos problemas de performance que você vai debugar.

## Sobre este galho

Este é o andar **conceitual**: os mecanismos do kernel que sobrevivem à troca de SO. Quando um endpoint está lento e o EXPLAIN do banco diz 20ms, a resposta costuma estar aqui — page fault, context switch, I/O wait, swap.

**Fronteiras (linka, não duplica):**
- **Usar o SO** (Linux na prática, Docker, K8s, WSL) → [[03-Dominios/Tecnologia/Infraestrutura/Linux|Linux]] / [[Infraestrutura]]. Aqui é a teoria.
- **Concorrência pelo ângulo de sincronização** (locks, modelos, race conditions) → [[Concorrência e Paralelismo]]. Aqui, threads/scheduling pelo ângulo do **mecanismo do kernel**.
- **Memória e GC do runtime gerenciado** → [[03-Dominios/Tecnologia/Java/JVM/index|JVM por dentro]].
- **Buffer pool, WAL e durabilidade do banco** → [[Banco de Dados]] (o page cache e o journaling resolvem o mesmo problema).
- **Sockets e I/O não-bloqueante** → [[Redes e Protocolos]].
- **Anéis de proteção e criptografia a fundo** → futuro galho de Segurança Conceitual (mencionados em prosa).

**Audiência:** dev senior em preparação para entrevista internacional. Cada nota tem seção "Em entrevista" com frases prontas em inglês e vocabulário técnico PT→EN. (O tema cai *parcialmente* em entrevista, mas é fundamento real.)

## Iniciado — o que o SO é e suas abstrações

1. [[01 - O que é um sistema operacional]] — gerenciador de recursos × máquina estendida; kernel × user space; modo kernel × usuário.
2. [[02 - System calls e a fronteira kernel-usuário]] — a interface do SO, trap/interrupção, o custo da transição.
3. [[03 - Processos]] — PCB, espaço de endereço, fork/exec, estados, hierarquia, zumbis.
4. [[04 - Threads na ótica do sistema operacional]] — kernel × user threads, modelo M:N, TCB; linka Concorrência.

## Adepto — escalonamento e memória

5. [[05 - Escalonamento de CPU]] — FCFS/SJF/round-robin/prioridade/MLFQ, métricas, o CFS do Linux.
6. [[06 - Memória - do endereço lógico ao físico]] — relocação, proteção, segmentação, fragmentação.
7. [[07 - Memória virtual e paginação]] — páginas/frames, page table, MMU, TLB, page fault, demand paging.
8. [[08 - Substituição de páginas e thrashing]] — LRU/clock/optimal, working set, thrashing, page cache.
9. [[09 - Comunicação entre processos (IPC)]] — pipes, sockets, shared memory, filas, sinais.

## Magus — I/O, arquivos e o resto

10. [[10 - I-O e o subsistema de entrada e saída]] — drivers, interrupção×polling, DMA, blocking/non-blocking/async.
11. [[11 - Sistemas de arquivos]] — inodes, alocação, metadados, hard×soft links, VFS.
12. [[12 - Journaling, consistência e durabilidade]] — journaling, copy-on-write, fsync, page cache; linka WAL do banco.
13. [[13 - Virtualização e containers]] — VM (hypervisor) × containers (namespaces + cgroups); linka Infraestrutura.
14. [[14 - Sistemas operacionais em entrevista]] — o SO em system design e debugging, inglês, vocabulário, armadilhas.

## Rotas alternativas

### O essencial em entrevista
01 → 03 → 05 → 07 → 08 → 14. Abstração, processos, escalonamento, memória virtual, thrashing e o capstone.

### Memória a fundo
06 → 07 → 08 → 12. Do endereço lógico ao journaling, passando por paginação e page cache.

### Por que está lento? (debugging)
05 → 07 → 08 → 10 → 14. Escalonamento, paginação, thrashing, I/O e o método de diagnóstico.

## Veja também

- [[03-Dominios/Ciência/index|Fundamentos (MOC do domínio)]]
- [[Concorrência e Paralelismo]] — threads, scheduling e sincronização pelo ângulo conceitual
- [[03-Dominios/Tecnologia/Infraestrutura/Linux|Linux]] — usar o SO na prática
- [[Banco de Dados]] — buffer pool, WAL e durabilidade (o mesmo problema do page cache/journaling)
- [[Dicionário de Ciência da Computação]]
