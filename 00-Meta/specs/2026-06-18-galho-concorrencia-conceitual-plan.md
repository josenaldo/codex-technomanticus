---
title: "Galho Concorrência e Paralelismo (conceitual) — design e plano (Fundamentos, Camada B)"
created: 2026-06-18
type: plan
status: draft
publish: false
tags:
  - meta
  - plan
  - fundamentos
  - concorrencia
---

# Galho Concorrência e Paralelismo (conceitual) — design e plano

## Contexto
SEGUNDO galho da Camada B do meta-plano de Fundamentos (depois de Paradigmas, COMPLETO 2026-06-18).
Galho 8 do roster (`2026-06-15-fundamentos-meta-planejamento-design.md`): "Concorrência e Paralelismo
(conceitual) — race conditions, deadlock, mutex/semáforo, modelos (atores / CSP / memória compartilhada).
Distinto do galho Java-específico de concorrência. ★ (interview-critical)". Conteúdo NOVO (sem monólito).
Roster aprovado pelo usuário em 2026-06-18 (expandido p/ 18). **Diretriz do usuário: "caprichar que nem o
galho de Estruturas de Dados"** — ou seja: cluster comparativo de MODELOS (cada modelo com showcase profundo
da linguagem canônica, como ED comparava Java·TS·Python·Go por estrutura) + capstone comparativo (análogo a
"Escolhendo a estrutura certa"), teto de prosa generoso, muitos diagramas.

## Decisão de fronteira (a chave — rígido)
Existe um galho Java DEDICADO e completo: `03-Dominios/Java/Concorrência e paralelismo/index` (16 notas:
threads, `synchronized`, JMM, locks, atomics, executors, `CompletableFuture`, virtual threads/Loom,
structured concurrency, scoped values, fork-join) + `[[Java Concurrency]]` (Core). ESTE galho é o andar
**CONCEITUAL e STACK-AGNÓSTICO**: os problemas universais e os MODELOS de concorrência. Sempre que for pra
mecânica Java específica, LINKA o galho Java — não duplica.
- **Java específico** (java.util.concurrent, JMM happens-before na API, Loom) → `[[03-Dominios/Java/Concorrência e paralelismo/index|Concorrência (Java)]]` / `[[Java Concurrency]]`. A nota 10 (memória compartilhada) usa Java como showcase e linka pesado.
- **Imutabilidade como arma contra concorrência** → `[[08 - Imutabilidade e estado]]` (galho Paradigmas) forward-linka pra cá; aqui aprofunda o lado concorrência.
- **Isolamento/MVCC/locking de BANCO** → `[[Banco de Dados]]` (e sua nota 11 Concorrência e locking). A nota 09 (STM) cruza, sem duplicar.
- **Assincronia/reativo** → `[[12 - Programação reativa e dataflow]]` (Paradigmas) e `[[Programação Reativa]]` (Java). A nota 14 (event loop) linka.
- **Processos/threads/scheduling do SO** → futuro galho Sistemas Operacionais (Camada B, ainda não existe) — mencionar em PROSA, sem wikilink quebrado.

## Roster de notas (18; expandido de 16 a pedido do usuário)

### Iniciado — o terreno e os perigos universais
1. **Concorrência e paralelismo: o que é e por que é difícil** *(âncora)* — concorrência (lidar com muitas coisas, estrutura) × paralelismo (fazer muitas ao mesmo tempo, execução; Rob Pike); por que existe (multicore, I/O, responsividade); por que DÓI (não-determinismo, intercalação, Heisenbugs); as duas faces em entrevista.
2. **Processos e threads** *(conceitual)* — unidade de execução; processo (isolamento, memória própria) × thread (compartilha memória, leve); context switch e seu custo; kernel × green/user threads; modelo M:N; fibers/virtual threads conceitualmente. SO em prosa.
3. **A raiz do mal: estado compartilhado e race conditions** — estado mutável compartilhado + intercalação = bug; read-modify-write não-atômico; o contador clássico; data race × race condition. Cruza `[[08 - Imutabilidade e estado]]`.
4. **Os três problemas: atomicidade, visibilidade e ordenação** — atomicidade (indivisível), visibilidade (cache/registrador — uma thread vê a escrita da outra?), ordenação (reordenamento de compilador/CPU); o que TODO modelo de memória precisa resolver. Gancho `[[11 - Modelos de memória e consistência]]`.

### Adepto — primitivas de coordenação (conceituais)
5. **Exclusão mútua: locks, mutexes e monitores** — seção crítica, mutex, lock, monitor (Hoare/Brinch Hansen), reentrância; o custo (contention, serialização, granularidade fina × grossa).
6. **Semáforos e coordenação** — semáforo (Dijkstra, P/V), binário × contador; barreiras, latches, condition variables; o produtor-consumidor clássico.
7. **Deadlock, livelock e starvation** — as 4 condições de Coffman (exclusão mútua, hold-and-wait, no preemption, circular wait); prevenir/evitar (ordem de lock, timeout)/detectar; livelock, starvation, fairness, inversão de prioridade (Mars Pathfinder).
8. **Operações atômicas e lock-free** — CAS (compare-and-swap), o problema ABA, lock-free × wait-free × obstruction-free; por que escala e por que é difícil. Linka atomics do galho Java.
9. **Memória transacional (STM) e abordagens otimistas** — transações em memória (commit/rollback como banco — cruza `[[Banco de Dados]]` isolamento/MVCC); otimista × pessimista; STM em Clojure/Haskell; quando vale (nicho que ilumina).

### Magus — os MODELOS de concorrência (cluster comparativo estilo ED) + leis + padrões + síntese
10. **Modelo 1 — memória compartilhada com threads e locks** — o dominante; poder e perigo; *showcase* **Java** (linka o galho Java a fundo). Por que é o mais difícil de acertar.
11. **Modelos de memória e consistência** — por que cada plataforma define um memory model; happens-before, sequential consistency × consistência relaxada (acquire/release); barreiras de memória; o JMM e o C++ memory model como exemplos. (a nota densa; cruza nota 4)
12. **Modelo 2 — troca de mensagens e CSP** — "Don't communicate by sharing memory; share memory by communicating" (Hoare CSP); canais, `select`; *showcase* **Go** (goroutines + channels) a fundo.
13. **Modelo 3 — o modelo de atores** — ator = estado privado + mailbox + mensagens assíncronas; sem estado compartilhado; supervisão e "let it crash"; *showcase* **Erlang/Elixir/BEAM** (e Akka). 
14. **Modelo 4 — loop de eventos e assincronia** — single-thread + event loop + callbacks/promises/async-await; concorrência sem paralelismo; *showcase* **JavaScript** (event loop, micro/macrotasks) + o **GIL do Python**/asyncio. Cruza `[[12 - Programação reativa e dataflow]]`.
15. **Modelo 5 — paralelismo de dados** — mesma operação sobre muitos dados; SIMD, GPU/CUDA, MapReduce, fork-join/work-stealing, parallel streams; *showcase* fork-join + GPU. Quando paralelizar de verdade.
16. **As leis da escala: Amdahl, Gustafson e os limites do paralelismo** — speedup teórico, a fração serial que limita (Amdahl), o contraponto de carga crescente (Gustafson), overhead de coordenação, lei de Little/contenção; por que "mais núcleos" nem sempre ajuda. (split do "expandir")
17. **Padrões de concorrência** — thread pool, produtor-consumidor/blocking queue, fan-out/fan-in (scatter-gather), pipeline, futures/promises, work-stealing, bulkhead; o vocabulário de design concorrente. Linka resiliência de `[[03-Dominios/Fundamentos/Redes e Protocolos/14 - Resiliência de rede|Resiliência de rede]]`. (split do "expandir")
18. **Capstone: escolher o modelo e concorrência em entrevista** — **tabela comparativa dos 5 modelos** (o análogo de "Escolhendo a estrutura certa" de ED): modelo × como coordena × estado × erro × brilha em × linguagem canônica; como Java/Go/Erlang/JS/Python/Rust escolheram; escolher por problema; "How to explain in English"; vocabulário PT→EN; armadilhas consolidadas; recursos.

## Padrão por nota ("caprichar nível ED")
- PT-BR, registro Feynman (analogias, perguntas retóricas, callouts, frases curtas, resumo em 1 linha).
- **Teto de prosa generoso (2400, permissão); alvo substancial ~360–520 ln** (mais que Paradigmas — o usuário pediu capricho). Código/exemplos multi-linguagem NÃO contam.
- **4–6 diagramas Mermaid** por nota onde ajudam, cada um com lead-in + "leitura do diagrama". Excelentes aqui:
  `sequenceDiagram` (race condition intercalada, deadlock/abraço mortal, handshake de canais CSP, mailbox de
  atores, event loop processando a fila), `flowchart` (modelo de memória, decisão de modelo, padrões),
  `stateDiagram-v2` (ciclo de vida de thread, estados de lock). **Sem `xychart-beta`** (Amdahl/Gustafson via
  TABELA + flowchart, não gráfico). Símbolos LITERAIS na prosa; entidades HTML SÓ em rótulos Mermaid entre aspas.
- **A assinatura ED**: o cluster de modelos (10–15) traz, cada um, um *showcase* PROFUNDO da linguagem canônica
  (como ED comparava implementações por runtime); o capstone (18) consolida na tabela comparativa.
- **Seção final "Em entrevista"** (★ tema interview-critical) — frases EN + vocabulário PT→EN.
- Fontes verificadas na web (WebSearch); callout `> [!info] Lastro`. Atomicidade: linka vizinhas.
- `NN - Título.md` flat. `publish: false` nas notas; `publish: true` só no `index.md`. Frontmatter `fase:`,
  `type: concept`, `status: evergreen`, tags.
- **NUNCA fabricar** experiências/dados do usuário — galho teórico, sem monólito; usar cenários genéricos e
  exemplos canônicos (contador, jantar dos filósofos, produtor-consumidor), nunca projeto/cliente inventado
  ([[feedback-no-fabrication]]).

## Tronco e MOC
- Pasta `03-Dominios/Fundamentos/Concorrência e Paralelismo/` com `index.md` (MOC, `type: moc`,
  `status: growing`, `publish: true`, agrupado por fase, rotas alternativas, dataview, "Veja também").
- Alias do `index.md`: **"Concorrência e Paralelismo"** + **"Concorrência"** + **"Concorrência conceitual"** +
  **"Concurrency"** + **"Paralelismo"**. (Galho novo; alias prepara o terreno e evita colidir com o alias
  "Concorrência Java" do galho Java.)
- Entra no MOC do domínio em DOIS arquivos: `Fundamentos/index.md` e `Fundamentos.md` (adicionar a linha).

## Convenções de execução
- Subagent-driven, um subagente por nota, escrita em UMA chamada Write, house-style completo no prompt.
- Disparar por fase (Iniciado 1–4, Adepto 5–9, Magus 10–18), revisando armadilhas e commitando entre fases.
- Como Magus é grande (9 notas), pode disparar em dois lotes (10–14 modelos+memória; 15–18 dados+leis+padrões+capstone).
- Commits direto na main, SEM push, SEM Co-Authored-By ([[feedback-commits]]).

## Sequência de construção
1. Scaffold `Concorrência e Paralelismo/index.md` + aliases. Commit.
2. Notas Iniciado (01–04), Adepto (05–09), Magus (10–18), uma por subagente. Commit por fase.
3. Adicionar a entrada no MOC do domínio (`Fundamentos/index.md` + `Fundamentos.md`).
4. Checar armadilhas; verificar alvos externos + NN-links internos; atualizar memória
   `project-fundamentos-meta-plan` (Concorrência COMPLETO). Próximo na Camada B: Sistemas Operacionais (9).
