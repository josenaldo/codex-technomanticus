---
title: "Galho Sistemas Operacionais (conceitual) — design e plano (Fundamentos, Camada B)"
created: 2026-06-18
type: plan
status: draft
publish: false
tags:
  - meta
  - plan
  - fundamentos
  - sistemas-operacionais
---

# Galho Sistemas Operacionais (conceitual) — design e plano

## Contexto
TERCEIRO galho da Camada B (depois de Paradigmas e Concorrência, COMPLETOS 2026-06-18). Galho 9 do roster:
"Sistemas Operacionais — processos, threads, scheduling, memória virtual, I/O, filesystems. (não colide com
Infraestrutura, que é *usar* o SO, não a teoria) (parcial)". Conteúdo NOVO (sem monólito). Roster de 14 notas
aprovado pelo usuário em 2026-06-18, **com CAPRICHO NÍVEL ED** (teto de prosa generoso, muitos diagramas, e
showcase comparativo de SOs reais — Linux/Windows/macOS — onde ilumina).

## Decisão de fronteira (rígido)
- **Infraestrutura** (`03-Dominios/Tecnologia/Infraestrutura/`: Linux, Docker, K8s, WSL) = USAR o SO. ESTE galho é a
  TEORIA. Linka `[[03-Dominios/Tecnologia/Infraestrutura/Linux|Linux]]` / `[[Infraestrutura]]` pro concreto.
- **Concorrência e Paralelismo** (galho recém-feito) = threads/scheduling pelo ângulo de SINCRONIZAÇÃO e
  modelos. ESTE galho faz o ângulo de MECANISMO DO KERNEL (PCB/TCB, troca de contexto por dentro, algoritmos
  de scheduler). As notas 04 (threads) e 09 (IPC) **linkam** `[[Concorrência e Paralelismo]]`, não duplicam.
- **JVM** (`03-Dominios/Tecnologia/Java/JVM/index`) = memória/GC do runtime gerenciado. A nota de memória virtual linka
  pro paralelo (o GC vê memória virtual; o managed heap).
- **Banco de Dados** — buffer pool, WAL, fsync têm paralelo FORTE com page cache / journaling / durabilidade
  do SO. A nota 08 e a 12 **linkam** `[[Banco de Dados]]` (o paralelo é didático, não duplicação).
- **Redes** — sockets e I/O não-bloqueante. Notas 09/10 **linkam** `[[Redes e Protocolos]]`.
- **Segurança Conceitual** (futuro galho, Camada D) — anéis de proteção, modo privilegiado a fundo, cripto.
  Mencionar proteção/modo-kernel em PROSA; primitivas de segurança ficam pro futuro galho, SEM wikilink.

## Roster de notas (14)

### Iniciado — o que o SO é e suas abstrações
1. **O que é um sistema operacional** *(âncora)* — as duas visões (gerenciador de recursos × máquina
   estendida/abstração de Tanenbaum); kernel × user space; modo kernel × modo usuário (anéis de proteção em
   prosa); por que existe (multiplexar hardware, proteger, abstrair); monolítico × microkernel × híbrido.
2. **System calls e a fronteira kernel/usuário** — a interface (a "API do SO"); trap/interrupção/exceção; a
   transição user→kernel e seu custo; exemplos (`read`/`write`/`fork`/`mmap`); libc como wrapper; strace.
3. **Processos** — o que é (PCB, espaço de endereço: text/data/heap/stack), criação (`fork`/`exec`, copy-on-write),
   estados (new/ready/running/blocked/terminated), hierarquia, zumbis/órfãos, sinais (intro). Showcase fork×CreateProcess.
4. **Threads na ótica do SO** — kernel threads × user threads, modelo 1:1 / M:N, TCB, compartilham espaço de
   endereço; por que threads são "leves". **Linka [[Concorrência e Paralelismo]]** (sincronização/modelos).

### Adepto — escalonamento e memória
5. **Escalonamento de CPU** — preemptivo × cooperativo; algoritmos (FCFS, SJF/SRTF, round-robin, prioridade,
   MLFQ); métricas (turnaround, waiting, response, throughput); o dilema fairness×latência×throughput; o CFS
   do Linux (e EEVDF moderno). Showcase Linux CFS × Windows priority.
6. **Memória: do endereço lógico ao físico** — abstração de memória, relocação, espaço de endereço, proteção;
   alocação contígua, fragmentação (interna/externa); segmentação; a ponte pra paginação.
7. **Memória virtual e paginação** — páginas/frames, page table (multinível), MMU, TLB, page fault, demand
   paging; por que VM existe (isolamento + ilusão de memória grande + overcommit); mmap/memória compartilhada.
8. **Substituição de páginas e thrashing** — FIFO, LRU, clock/second-chance, optimal/Belady (e a anomalia de
   Belady); working set, thrashing, swap; o **page cache**. **Linka [[Estruturas de Dados]]** (LRU) e
   **[[Banco de Dados]]** (buffer pool — o mesmo problema).
9. **Comunicação entre processos (IPC)** — pipes, named pipes, sockets (Unix domain), shared memory, message
   queues, sinais; síncrono × assíncrono. **Linka [[Concorrência e Paralelismo]]** (troca de mensagens) e
   **[[Redes e Protocolos]]** (sockets).

### Magus — I/O, arquivos e o resto
10. **I/O e o subsistema de entrada/saída** — device drivers, interrupção × polling, DMA; blocking ×
    non-blocking × async I/O (select/poll/epoll/io_uring); buffering; por que I/O domina latência. **Linka** o
    event loop de `[[Concorrência e Paralelismo]]` e `[[Redes e Protocolos]]`.
11. **Sistemas de arquivos** — arquivos/diretórios/inodes, alocação (contígua/encadeada/indexada), metadados,
    hard × soft links, montagem, VFS; o caminho de um `open`/`read`. Showcase ext4 × NTFS × APFS.
12. **Journaling, consistência e durabilidade** — o problema da escrita interrompida; journaling (ext4),
    copy-on-write FS (ZFS/Btrfs/APFS), `fsync`/write-back, o page cache e a durabilidade. **Linka
    [[Banco de Dados]]** (WAL — paralelo direto). Mostra que SGBD e FS resolvem o MESMO problema.
13. **Virtualização e containers** *(conceitual)* — VM (hypervisor tipo 1 × 2, paravirtualização) × containers
    (namespaces + cgroups + chroot/pivot_root); o que o KERNEL fornece pro Docker; isolamento × overhead.
    **Linka [[Infraestrutura]]** (Docker/K8s) — a fronteira teoria×uso.
14. **Capstone: SO em entrevista** — o SO em system design e debugging (o método de rastrear "por que está
    lento?": CPU? page fault/swap? context switch? I/O wait? lock?); ferramentas (top/vmstat/strace/perf em
    prosa); "How to explain in English"; vocabulário PT→EN; armadilhas; recursos.

## Padrão por nota (CAPRICHO NÍVEL ED)
- PT-BR, registro Feynman (analogias, perguntas retóricas, callouts, frases curtas, resumo em 1 linha).
- **Teto de prosa generoso (2400); alvo substancial ~360–500 ln**. Código/exemplos não contam.
- **4–6 diagramas Mermaid** por nota onde ajudam, cada um com lead-in + "leitura do diagrama". Excelentes:
  `flowchart` (camadas do SO, transição syscall, page table/MMU, VFS, hypervisor×container), `stateDiagram-v2`
  (estados do processo), `sequenceDiagram` (syscall trap, page fault handling, DMA, fork/exec), tabelas
  (algoritmos de scheduling, FS comparados). **Sem `xychart-beta`**. Símbolos LITERAIS na prosa; entidades
  HTML SÓ em rótulos Mermaid entre aspas.
- **Showcase comparativo de SOs reais** (a assinatura ED deste galho): onde ilumina, comparar Linux × Windows
  × macOS (ex.: fork×CreateProcess, CFS×priority scheduler, ext4×NTFS×APFS, epoll×IOCP×kqueue). Não em toda
  nota — só onde a divergência ensina.
- **Seção final "Em entrevista"** — frases EN + vocabulário PT→EN. (Tema é "parcial" em entrevista, mas mantém.)
- Fontes verificadas na web (WebSearch); callout `> [!info] Lastro`. Canônico: Tanenbaum *Modern Operating
  Systems*, Silberschatz *Operating System Concepts*, *OSTEP* (Arpaci-Dusseau, gratuito).
- Atomicidade: linka vizinhas. `NN - Título.md` flat. `publish: false` nas notas; `publish: true` só no index.
- **NUNCA fabricar** experiências/dados do usuário — galho teórico, sem monólito; cenários genéricos e
  exemplos canônicos (jantar dos filósofos NÃO — isso é Concorrência; aqui: o shell, o `ls`, o page fault).

## Tronco e MOC
- Pasta `03-Dominios/Ciência/Sistemas Operacionais/` com `index.md` (MOC, `type: moc`, `status: growing`,
  `publish: true`, fases, rotas, dataview, "Veja também").
- Alias do index: **"Sistemas Operacionais"** + **"Sistema Operacional"** + **"SO"** + **"Operating Systems"**.
- Entra no MOC do domínio em `Fundamentos/index.md` e `Fundamentos.md` (seção nova ou junto de Concorrência).

## Convenções de execução
- Subagent-driven, um por nota, UMA chamada Write, house-style completo no prompt (depth front-loaded — os
  subagentes fazem undershoot sistemático; prever 2ª passada de enriquecimento nos floors por fase).
- Disparar por fase (Iniciado 1–4, Adepto 5–9, Magus 10–14). Commits direto na main, SEM push, SEM Co-Authored-By.

## Sequência de construção
1. Scaffold `Sistemas Operacionais/index.md` + aliases. Commit.
2. Notas por fase, uma por subagente; enriquecer floors. Commit por fase.
3. MOCs do domínio. Checar armadilhas + NN-links + alvos externos. Atualizar memória (SO COMPLETO).
   Próximo na Camada B: Teoria da Computação (10) + Matemática para Computação (11).
