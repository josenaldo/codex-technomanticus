---
title: "Roadmap — Memória de Agentes"
created: 2026-07-02
type: meta
publish: false
tags:
  - meta
  - roadmap
---

# Roadmap — Memória de Agentes

Diagnóstico migrado de guia/roadmap - ia.md (30/06). Cada entrada tem estado de enriquecimento, score, classificação de custo e plano de execução acionável.

**Galho:** `03-Dominios/Tecnologia/IA/Memória de Agentes`

> [!warning] Diagnóstico de 30/06 — pode estar defasado. Vários itens marcados ⬜ podem já ter sido enriquecidos depois; reconciliar com o estado real ao tratar o galho.

## Régua de análise

Checklist `verificar-nota` — 12 itens (isenções por fase/tipo/broto aplicadas por nota):

| Grupo | Itens |
|-------|-------|
| ESTRUTURA | E1 TL;DR · E2 Abertura-problema · E3 Mermaid · E4 Casos práticos · E5 O que vem a seguir · E6 Inglês · E7 Tabela PT↔EN · E8 Armadilhas [!warning] |
| PROFUNDIDADE | P1 Código-com-falha · P2 Mecanismo explicado |
| LINKS | L1 Wikilink cross-galho · L2 Referência externa (URL) |
| MÍDIA | M1 Vídeo/podcast embutido |

**Esquema de `fase:` detectado:** COM fase (Iniciado) — galho usa `fase: Iniciado` em todas as notas
**Piso de linhas:** aplicável — Iniciado ≥300

> [!note] Notas 10–19 são de implementações específicas (frameworks/produtos) — sujeitas a caducidade de versão/pricing/estrelas GitHub. Checar conteúdo real antes de citar em decisão técnica.

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 24 |
| ⬜ pendente | 17 |
| ➖ não precisa | 7 |
| ✅ feita | 0 |
| 🔄 em andamento | 0 |
| % concluído | 0% |

---

## Notas

#### 01 - O que é memória em IA   [mecânico]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 301 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E1, P1
- **Score:** 10/12
- **Plano de execução:**
  - Expandir o TL;DR de 1 linha compacta para ≥3 linhas distintas (problema da amnésia nativa do LLM · o que é memória persistente · o loop write-manage-read) — ativa E1, eleva para 11/12
  - P1 (código-com-falha) inaplicável para nota puramente conceitual — não forçar
- **Resultado:** —

#### 02 - O problema das janelas de contexto   [mecânico]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 301 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E2, P1
- **Score:** 10/12
- **Plano de execução:**
  - Converter a abertura de "## O que é" (atualmente "X é...") para começar com cenário/problema (ex: sessão de 20 turnos que esquece tudo na próxima chamada) — ativa E2, eleva para 11/12
  - P1 inaplicável para nota conceitual — não forçar
- **Resultado:** —

#### 03 - Taxonomia da memória (episódica, semântica, procedural)   [mecânico]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 301 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E2, P1
- **Score:** 10/12
- **Plano de execução:**
  - Adicionar parágrafo de abertura com cenário concreto antes de "## O que é" (atualmente abre com "A taxonomia clássica vem do psicólogo Tulving...") — ativa E2, eleva para 11/12
  - P1 inaplicável para nota conceitual — não forçar
- **Resultado:** —

#### 04 - RAG vs memória de longo prazo   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 301 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** P1
- **Score:** 11/12
- **Plano de execução:**
  - — nenhuma
- **Resultado:** —

#### 05 - Beyond RAG - quando RAG não basta   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 301 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** P1
- **Score:** 11/12
- **Plano de execução:**
  - — nenhuma
- **Resultado:** —

#### 06 - O LLM Wiki Pattern (gist do Karpathy)   [mecânico]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 300 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E2, P1
- **Score:** 10/12
- **Plano de execução:**
  - Trazer a dor já existente na nota ("pesquisadores gastavam 20–30% de cada sessão re-explicando contexto") da seção "## O contexto histórico" para o início como cenário-gancho — ativa E2, eleva para 11/12
- **Resultado:** —

#### 07 - Por que Obsidian e markdown como substrato   [mecânico]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 302 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E2, P1
- **Score:** 10/12
- **Plano de execução:**
  - Adicionar parágrafo de abertura com cenário/problema antes de "## O que é" (ex: engenheiro que conectou LLM a vector DB e não conseguia abrir/revisar/versionar o que o agente escreveu) — ativa E2, eleva para 11/12
- **Resultado:** —

#### 08 - Arquitetura de um sistema de memória   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 301 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** P1
- **Score:** 11/12
- **Plano de execução:**
  - — nenhuma
- **Resultado:** —

#### 09 - Panorama de implementações (abril 2026)   [mecânico]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 301 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E2, P1
- **Score:** 10/12
- **Plano de execução:**
  - Adicionar `[!warning]` de caducidade visível logo antes de "## O que é" sinalizando que a tabela é instantâneo de abril/2026 (armadilha 4 já cobre isso, mas só ao final)
  - Reescrever abertura de "## O que é" (atualmente descritiva: "Esta nota é um mapa de mercado...") com cenário concreto — ativa E2, eleva para 11/12
- **Resultado:** —

#### 10 - LLM-knowledge-base (Wendel) — direto do gist   [mecânico]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 301 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E1, E2, P1
- **Score:** 9/12
- **Plano de execução:**
  - Expandir TL;DR para ≥3 linhas (conceito, mecanismo 4-stage, posicionamento como referência-não-SaaS) — eleva para 10/12
  - Reescrever abertura de "## O que é" (hoje "LLM-knowledge-base é...") com cenário concreto — ativa E2, eleva para 11/12
  - Promover o aviso de caducidade inline (seção "Anatomia técnica", abril/2026) para callout `[!warning]`/`[!info]` visível no topo da seção
- **Resultado:** —

#### 11 - OpenKB — wiki compilada com PageIndex   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 301 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E2, P1
- **Score:** 10/12
- **Plano de execução:**
  - Reescrever abertura de "## O que é" (hoje "OpenKB se apresenta como...") com problema/cenário concreto — ativa E2, eleva para 11/12
  - ⚠ Caducidade: verificar se o pacote avançou além de `openkb 0.1.3` (alpha, criado 2026-05-06) e atualizar versões/roadmap em "## Anatomia técnica" se necessário
- **Resultado:** —

#### 12 - graphify — knowledge graph de raw   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 308 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E1, E2, P1
- **Score:** 9/12
- **Plano de execução:**
  - Expandir o `[!abstract]` TL;DR para ≥3 linhas físicas (o que é / diferencial do substrato gráfico / saídas + cuidados)
  - Reescrever abertura de "## O que é" (hoje "graphify é uma versão...") com cenário concreto (ex: pasta `/raw` misturada e como o assistente encontra o que importa)
  - ⚠ Caducidade: verificar se versão, ~25 linguagens suportadas e integração de IDEs em "## Anatomia técnica" ainda batem com o README atual (repo `v5`, atualizado 2026-04-26)
- **Resultado:** —

#### 13 - basic-memory — MCP nativo Obsidian   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 301 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E2, P1
- **Score:** 10/12
- **Plano de execução:**
  - Reescrever o primeiro parágrafo de "## O que é" (hoje "`basic-memory` é um servidor MCP que...") com cenário/problema (memória entre sessões, legível, portátil, sem lock-in)
  - ⚠ Caducidade: verificar contagem de estrelas (2.929 em abril/2026), versão atual (última mencionada v0.19.x), novas tools MCP ou mudanças na Cloud antes de citar em decisão técnica
- **Resultado:** —

#### 14 - Letta (ex-MemGPT)   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 228 linhas reais ⚠ abaixo do piso · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E2, P1
- **Score:** 10/12
- **Plano de execução:**
  - Piso: faltam ~72 linhas para atingir 300 — expandir seções existentes ou adicionar seção nova (ex: "Letta vs self-host tradicional" ou aprofundar sleep-time agents com código)
  - Reescrever abertura de "## O que é" (hoje "Letta é um framework...") com o problema (agent que precisa lembrar decisões sem heurísticas manuais de retenção)
  - ⚠ Caducidade: nota cita `Opus 4.5`/`GPT-5.2`, pricing e "mais de 22 mil estrelas" de abril/2026 apesar de `updated: 2026-06-28` — verificar leaderboard, pricing e estrelas atuais antes de citar
- **Resultado:** —

#### 15 - Mem0 — vetorial + grafo   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 301 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E2, P1
- **Score:** 10/12
- **Plano de execução:**
  - Reescrever abertura de "## O que é" (hoje "`mem0` é um framework para...") com o problema (agent que acumula sessões e esquece instrução na 11ª por estouro de janela)
  - Adicionar exemplo de uso incorreto com consequência (ex: `memory.add` sem tratar custo de extração em alto volume, ou `memory.search` sem verificar `user_id`)
  - ⚠ Caducidade: dados de abril/2026 (54k stars, pricing, ~24 integrações, LongMemEval 93,4% auto-reportado, remoção do graph store externo) apesar de `updated: 2026-06-28` — verificar changelog e estado atual antes de citar
- **Resultado:** —

#### 16 - Zep e Graphiti — knowledge graph temporal   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 317 linhas totais (sem blanks no fim) · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E2, P1
- **Score:** 10/12
- **Plano de execução:**
  - ⚠ Caducidade: seção "Anatomia técnica" diz "verificado em abril de 2026" — checar versões dos backends (Neo4j 5.26+, FalkorDB 1.1.2, Kuzu 0.11.2), pricing Zep Cloud e estado do MCP server
  - Opcional: converter abertura de "Graphiti é um framework..." para cenário-problema; opcional: exemplo de uso incorreto (omitir `reference_time`) — nenhum bloqueia aprovação
- **Resultado:** —

#### 17 - MemPalace (Milla Jovovich)   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 301 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E2, P1
- **Score:** 10/12
- **Plano de execução:**
  - ⚠ Caducidade: projeto lançado abril/2026 com "breaking changes esperáveis" e discrepância 29 vs 20 MCP tools — verificar changelog oficial e auditoria `lhl/agentic-memory` antes de citar estado técnico
  - Opcional: converter abertura de "MemPalace é um sistema..." para cenário-problema; opcional: exemplo de falha concreta (habilitar AAAK sem ler o 12,4pp drop) — nenhum bloqueia aprovação
- **Resultado:** —

#### 18 - Generative Agents (Park, Stanford 2023)   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 301 linhas totais (sem vazias no fim) · fase: Iniciado · status: seedling
- **Núcleo/gaps:** P1
- **Score:** 11/12
- **Plano de execução:**
  - — nenhuma
- **Resultado:** —

#### 19 - A-MEM — Zettelkasten dinâmico   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 301 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** P1
- **Score:** 11/12
- **Plano de execução:**
  - — nenhuma
- **Resultado:** —

#### 20 - Surveys e estado da arte 2026   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 301 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E1, P1
- **Score:** 10/12
- **Plano de execução:**
  - Expandir o `[!abstract]` TL;DR de 1 para ≥3 linhas (maturidade institucional com MemAgents; cinco mecanismos como consenso; distinção agent memory × LLM memorization)
  - Caducidade: seção "ICLR 2026 Workshop MemAgents" usa futuro ("acontece em 27 de abril") mas o evento já ocorreu — reescrever no passado e, se disponíveis, referenciar papers/talks publicados pós-evento
- **Resultado:** —

#### 21 - Comparativo crítico (LongMemEval)   [mecânico]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 301 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E2, P1
- **Score:** 10/12
- **Plano de execução:**
  - Reformular abertura de "O que é o LongMemEval" (hoje "[LongMemEval] é um benchmark...") para cenário-problema (comparar sistemas de memória sem saber se os números de marketing são comparáveis) antes da definição formal
- **Resultado:** —

#### 22 - Críticas, limitações e armadilhas   [mecânico]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 300 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E2, E3, P1
- **Score:** 9/12
- **Plano de execução:**
  - Reformular abertura de "## O que é" (hoje meta-descrição "Esta nota é uma análise crítica...") para cenário-problema — ex: score de 96,6% num benchmark prestes a ser citado em entrevista, quando o paper crítico aponta que vem de armazenamento verbatim + ChromaDB default, não da inovação anunciada
- **Resultado:** —

#### 23 - Guia de implementação do zero   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 301 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E3, P1
- **Score:** 10/12
- **Plano de execução:**
  - — nenhuma
- **Resultado:** —

#### 24 - Aplicações comerciais e modelo de negócio   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 300 linhas reais ⚠ no limite do piso · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E2, E3, P1, L2
- **Score:** 8/12
- **Plano de execução:**
  - Adicionar ≥1 URL externa real nas Referências (L2 falha) — ex: produto digital comparável (Nick Milo LYT Kit em Gumroad, página pública do livro de Forte) — move para 9/12
  - Refatorar abertura de "## O que é": mover a dor central ("conhecimento técnico sem caminho de monetização vira hobby") para o primeiro parágrafo, antes da descrição dos três modelos
  - Caducidade: preços e análise de amadurecimento de mercado são de 2026 — inserir nota de revisão periódica (a cada 12 meses ou em mudança relevante no ecossistema PKM + IA)
- **Resultado:** —
