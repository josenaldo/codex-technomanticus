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
| ⬜ pendente | 0 |
| ➖ não precisa | 7 |
| ✅ feita | 17 |
| 🔄 em andamento | 0 |
| % concluído | 100% |

> [!success] Galho COMPLETO em 2026-07-07 — 0 ⬜, 17 ✅, 7 ➖. Sessão de 07/07 fechou 14 notas (06·07·09·10·11·12·13·14·15·17·20·21·22·24) via fan-out ≤3 verificado; notas 01·02·03 feitas em 06/07. Várias notas de implementação (10·11·12·13·14·15·17·20) tiveram caducidade verificada via web (versões/estrelas/pricing atualizados).

---

## Notas

#### 01 - O que é memória em IA   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-06)
- **Estado:** 301 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E1, P1
- **Score:** 10/12
- **Plano de execução:**
  - Expandir o TL;DR de 1 linha compacta para ≥3 linhas distintas (problema da amnésia nativa do LLM · o que é memória persistente · o loop write-manage-read) — ativa E1, eleva para 11/12
  - P1 (código-com-falha) inaplicável para nota puramente conceitual — não forçar
- **Resultado:** TL;DR expandido para 3 linhas (amnésia nativa · memória persistente · loop write-manage-read) ativa E1. P1 corretamente inaplicável. status→growing. Plano integral.

#### 02 - O problema das janelas de contexto   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-06)
- **Estado:** 301 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E2, P1
- **Score:** 10/12
- **Plano de execução:**
  - Converter a abertura de "## O que é" (atualmente "X é...") para começar com cenário/problema (ex: sessão de 20 turnos que esquece tudo na próxima chamada) — ativa E2, eleva para 11/12
  - P1 inaplicável para nota conceitual — não forçar
- **Resultado:** Abertura de "## O que é" reescrita com cenário concreto (sessão de 20 turnos, decisão de JWT no turno 5 revisitada no 18, evapora na próxima chamada) ativa E2. P1 inaplicável. Plano integral.

#### 03 - Taxonomia da memória (episódica, semântica, procedural)   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-06)
- **Estado:** 301 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E2, P1
- **Score:** 10/12
- **Plano de execução:**
  - Adicionar parágrafo de abertura com cenário concreto antes de "## O que é" (atualmente abre com "A taxonomia clássica vem do psicólogo Tulving...") — ativa E2, eleva para 11/12
  - P1 inaplicável para nota conceitual — não forçar
- **Resultado:** Parágrafo de abertura com cenário concreto (agente de coding cometendo 3 falhas de memória distintas — episódica/semântica/procedural) antes de "## O que é" ativa E2. P1 inaplicável. Plano integral.

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
- **Enriquecimento:** ✅ feita (2026-07-07)
- **Estado:** 300 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E2, P1
- **Score:** 10/12
- **Plano de execução:**
  - Trazer a dor já existente na nota ("pesquisadores gastavam 20–30% de cada sessão re-explicando contexto") da seção "## O contexto histórico" para o início como cenário-gancho — ativa E2, eleva para 11/12
- **Resultado:** Dor trazida para parágrafo-gancho após o TL;DR (pesquisador reabrindo chat, re-explicando contexto), abrindo com cenário antes da definição. Seção "## O contexto histórico" ajustada para callback (sem duplicar verbatim). E2 ativado.

#### 07 - Por que Obsidian e markdown como substrato   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-07)
- **Estado:** 302 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E2, P1
- **Score:** 10/12
- **Plano de execução:**
  - Adicionar parágrafo de abertura com cenário/problema antes de "## O que é" (ex: engenheiro que conectou LLM a vector DB e não conseguia abrir/revisar/versionar o que o agente escreveu) — ativa E2, eleva para 11/12
- **Resultado:** Parágrafo de abertura adicionado antes de "## O que é" (engenheiro conecta LLM a vector DB, alucinação vira dogma irrecuperável por falta de diff/histórico/revisão). E2 ativado. Item único aplicado integralmente.

#### 08 - Arquitetura de um sistema de memória   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 301 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** P1
- **Score:** 11/12
- **Plano de execução:**
  - — nenhuma
- **Resultado:** —

#### 09 - Panorama de implementações (abril 2026)   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-07)
- **Estado:** 301 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E2, P1
- **Score:** 10/12
- **Plano de execução:**
  - Adicionar `[!warning]` de caducidade visível logo antes de "## O que é" sinalizando que a tabela é instantâneo de abril/2026 (armadilha 4 já cobre isso, mas só ao final)
  - Reescrever abertura de "## O que é" (atualmente descritiva: "Esta nota é um mapa de mercado...") com cenário concreto — ativa E2, eleva para 11/12
- **Resultado:** (1) Callout [!warning] de caducidade inserido antes de "## O que é" com link para a seção de manutenção. (2) Abertura de "## O que é" reescrita com cenário concreto (time escolhendo framework sob pressão de prazo), preservando o parágrafo original. E2 ativado.

#### 10 - LLM-knowledge-base (Wendel) — direto do gist   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-07)
- **Estado:** 301 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E1, E2, P1
- **Score:** 9/12
- **Plano de execução:**
  - Expandir TL;DR para ≥3 linhas (conceito, mecanismo 4-stage, posicionamento como referência-não-SaaS) — eleva para 10/12
  - Reescrever abertura de "## O que é" (hoje "LLM-knowledge-base é...") com cenário concreto — ativa E2, eleva para 11/12
  - Promover o aviso de caducidade inline (seção "Anatomia técnica", abril/2026) para callout `[!warning]`/`[!info]` visível no topo da seção
- **Resultado:** TL;DR expandido para 3 linhas (conceito/mecanismo 4-stage/referência-não-SaaS). Abertura de "## O que é" reescrita com cenário concreto (PDF em raw/ → kb import-book/compile/qa) ativa E2. Aviso de caducidade promovido a callout [!warning] no topo de "## Anatomia técnica". Plano integral.

#### 11 - OpenKB — wiki compilada com PageIndex   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-07)
- **Estado:** 301 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E2, P1
- **Score:** 10/12
- **Plano de execução:**
  - Reescrever abertura de "## O que é" (hoje "OpenKB se apresenta como...") com problema/cenário concreto — ativa E2, eleva para 11/12
  - ⚠ Caducidade: verificar se o pacote avançou além de `openkb 0.1.3` (alpha, criado 2026-05-06) e atualizar versões/roadmap em "## Anatomia técnica" se necessário
- **Resultado:** Abertura de "## O que é" reescrita com cenário (40 PDFs, RAG sob demanda vs compilação única) ativa E2. Caducidade: PyPI mostra openkb 0.4.3 (02/07, 11 releases) mas classifier segue "3-Alpha" — atualizados frontmatter, Anatomia técnica, warnings, tabela comparativa e fonte PyPI nas Referências. PageIndex (dependência) não reconfirmado — marcado no texto.

#### 12 - graphify — knowledge graph de raw   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-07)
- **Estado:** 308 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E1, E2, P1
- **Score:** 9/12
- **Plano de execução:**
  - Expandir o `[!abstract]` TL;DR para ≥3 linhas físicas (o que é / diferencial do substrato gráfico / saídas + cuidados)
  - Reescrever abertura de "## O que é" (hoje "graphify é uma versão...") com cenário concreto (ex: pasta `/raw` misturada e como o assistente encontra o que importa)
  - ⚠ Caducidade: verificar se versão, ~25 linguagens suportadas e integração de IDEs em "## Anatomia técnica" ainda batem com o README atual (repo `v5`, atualizado 2026-04-26)
- **Resultado:** TL;DR expandido para 3 parágrafos (o que é/diferencial gráfico com multi-hop/saídas+ressalvas). Abertura de "## O que é" reescrita com cenário de pasta /raw (shortest_path vs dezenas de leituras) ativa E2. Caducidade via gh api+README: repo transferido safishamsi→Graphify-Labs, default branch v5→v8, ~25→36 gramáticas tree-sitter, IDEs +CodeBuddy/Factory Droid/Trae — tudo atualizado com ⚠. Plano integral.

#### 13 - basic-memory — MCP nativo Obsidian   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-07)
- **Estado:** 301 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E2, P1
- **Score:** 10/12
- **Plano de execução:**
  - Reescrever o primeiro parágrafo de "## O que é" (hoje "`basic-memory` é um servidor MCP que...") com cenário/problema (memória entre sessões, legível, portátil, sem lock-in)
  - ⚠ Caducidade: verificar contagem de estrelas (2.929 em abril/2026), versão atual (última mencionada v0.19.x), novas tools MCP ou mudanças na Cloud antes de citar em decisão técnica
- **Resultado:** Primeiro parágrafo de "## O que é" reescrito com cenário (esquecer entre sessões, custo de colar histórico) ativa E2. Caducidade via gh api+README: estrelas 2.929→3.385, versão v0.19→v0.22.1, novas tools MCP (schema_*, cloud_info, release_notes), produto Basic Memory Teams — tudo atualizado. Plano integral.

#### 14 - Letta (ex-MemGPT)   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-07)
- **Estado:** 228 linhas reais ⚠ abaixo do piso · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E2, P1
- **Score:** 10/12
- **Plano de execução:**
  - Piso: faltam ~72 linhas para atingir 300 — expandir seções existentes ou adicionar seção nova (ex: "Letta vs self-host tradicional" ou aprofundar sleep-time agents com código)
  - Reescrever abertura de "## O que é" (hoje "Letta é um framework...") com o problema (agent que precisa lembrar decisões sem heurísticas manuais de retenção)
  - ⚠ Caducidade: nota cita `Opus 4.5`/`GPT-5.2`, pricing e "mais de 22 mil estrelas" de abril/2026 apesar de `updated: 2026-06-28` — verificar leaderboard, pricing e estrelas atuais antes de citar
- **Resultado:** Piso já em 300 linhas na execução (roadmap citava 228 defasado) — sem expansão extra. Abertura de "## O que é" reescrita com problema (heurística de retenção manual) ativa E2. Caducidade via docs/github/leaderboard: estrelas ~23,7k, release v0.16.8, recomendação Opus 4.5/GPT-5.2 removida (docs apontam pro leaderboard), pricing atualizado (Free/Pro $20/API/Enterprise). Gaps E4·P1 fora do plano.

#### 15 - Mem0 — vetorial + grafo   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-07)
- **Estado:** 301 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E2, P1
- **Score:** 10/12
- **Plano de execução:**
  - Reescrever abertura de "## O que é" (hoje "`mem0` é um framework para...") com o problema (agent que acumula sessões e esquece instrução na 11ª por estouro de janela)
  - Adicionar exemplo de uso incorreto com consequência (ex: `memory.add` sem tratar custo de extração em alto volume, ou `memory.search` sem verificar `user_id`)
  - ⚠ Caducidade: dados de abril/2026 (54k stars, pricing, ~24 integrações, LongMemEval 93,4% auto-reportado, remoção do graph store externo) apesar de `updated: 2026-06-28` — verificar changelog e estado atual antes de citar
- **Resultado:** Abertura de "## O que é" reescrita com cenário (agent de suporte na 11ª sessão truncando janela) ativa E2. Adicionada subseção "uso incorreto: memory.search sem user_id" (código errado/certo + vazamento entre usuários). Caducidade via github/docs/pricing: estrelas 54k→60,3k, LongMemEval 93,4%→94,8% (single-pass ADD-only), novo tier Growth $79, integrações ~24 e remoção do graph store confirmadas. Score 10/12.

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
- **Enriquecimento:** ✅ feita (2026-07-07)
- **Estado:** 301 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E2, P1
- **Score:** 10/12
- **Plano de execução:**
  - ⚠ Caducidade: projeto lançado abril/2026 com "breaking changes esperáveis" e discrepância 29 vs 20 MCP tools — verificar changelog oficial e auditoria `lhl/agentic-memory` antes de citar estado técnico
  - Opcional: converter abertura de "MemPalace é um sistema..." para cenário-problema; opcional: exemplo de falha concreta (habilitar AAAK sem ler o 12,4pp drop) — nenhum bloqueia aprovação
- **Resultado:** Caducidade via web: arquitetura evoluiu (v3.3.0 + closets/halls/tunnels), contagem de MCP tools não convergiu (19/20/24 reportados; docs oficiais listam 34) — callout [!warning] de atualização + 2 fontes novas. Abertura de "## O que é" convertida em cenário (memória local-first por compliance) ativa E2. Exemplo [!example] de falha AAAK adicionado.

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
- **Enriquecimento:** ✅ feita (2026-07-07)
- **Estado:** 301 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E1, P1
- **Score:** 10/12
- **Plano de execução:**
  - Expandir o `[!abstract]` TL;DR de 1 para ≥3 linhas (maturidade institucional com MemAgents; cinco mecanismos como consenso; distinção agent memory × LLM memorization)
  - Caducidade: seção "ICLR 2026 Workshop MemAgents" usa futuro ("acontece em 27 de abril") mas o evento já ocorreu — reescrever no passado e, se disponíveis, referenciar papers/talks publicados pós-evento
- **Resultado:** TL;DR expandido para 4 linhas (maturidade institucional/cinco mecanismos como consenso/agent memory × LLM memorization). Seção Workshop MemAgents corrigida para passado + bloco "O que aconteceu no evento" (110+ submissões, keynotes, 2 papers com arXiv/OpenReview nas Referências). Score ~10-11/12.

#### 21 - Comparativo crítico (LongMemEval)   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-07)
- **Estado:** 301 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E2, P1
- **Score:** 10/12
- **Plano de execução:**
  - Reformular abertura de "O que é o LongMemEval" (hoje "[LongMemEval] é um benchmark...") para cenário-problema (comparar sistemas de memória sem saber se os números de marketing são comparáveis) antes da definição formal
- **Resultado:** Abertura reformulada com cenário-problema (três sistemas com scores 96,6%/93,4%/71,2% sem contexto de comparabilidade, analogia 100m vs maratona) antes da definição formal, que foi preservada. E2 ativado. Item único integral.

#### 22 - Críticas, limitações e armadilhas   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-07)
- **Estado:** 300 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E2, E3, P1
- **Score:** 9/12
- **Plano de execução:**
  - Reformular abertura de "## O que é" (hoje meta-descrição "Esta nota é uma análise crítica...") para cenário-problema — ex: score de 96,6% num benchmark prestes a ser citado em entrevista, quando o paper crítico aponta que vem de armazenamento verbatim + ChromaDB default, não da inovação anunciada
- **Resultado:** Abertura reformulada de meta-descrição para cenário-problema (entrevista citando 96,6% do MemPalace, confrontado pelo paper arXiv 2604.21284: ganho vem de verbatim + ChromaDB default, não da hierarquia espacial). E2 ativado. Item único integral.

#### 23 - Guia de implementação do zero   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 301 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E3, P1
- **Score:** 10/12
- **Plano de execução:**
  - — nenhuma
- **Resultado:** —

#### 24 - Aplicações comerciais e modelo de negócio   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-07)
- **Estado:** 300 linhas reais ⚠ no limite do piso · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E2, E3, P1, L2
- **Score:** 8/12
- **Plano de execução:**
  - Adicionar ≥1 URL externa real nas Referências (L2 falha) — ex: produto digital comparável (Nick Milo LYT Kit em Gumroad, página pública do livro de Forte) — move para 9/12
  - Refatorar abertura de "## O que é": mover a dor central ("conhecimento técnico sem caminho de monetização vira hobby") para o primeiro parágrafo, antes da descrição dos três modelos
  - Caducidade: preços e análise de amadurecimento de mercado são de 2026 — inserir nota de revisão periódica (a cada 12 meses ou em mudança relevante no ecossistema PKM + IA)
- **Resultado:** 2 URLs externas reais verificadas nas Referências (buildingasecondbrain.com/book · linkingyourthinking.com) resolvem L2. Abertura de "## O que é" refatorada com a dor central (conhecimento sem monetização vira hobby) antes dos três modelos ativa E2. Callout [!warning] de revisão periódica (12 meses) inserido. Move 8/12→~10/12.
