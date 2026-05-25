---
title: "Comparativo crítico (LongMemEval)"
created: 2026-04-26
updated: 2026-04-26
type: concept
status: seedling
publish: true
tags:
  - memoria-agentes
  - comparativo
  - longmemeval
  - benchmark
aliases:
  - Comparativo de implementações
  - LongMemEval scores
  - Benchmark memória de agentes
---

# Comparativo crítico (LongMemEval)

> [!abstract] TL;DR
> **LongMemEval** (ICLR 2025) virou o benchmark padrão de facto para medir memória de longo prazo em chat assistants — multi-session, retrieval consistente, abstention. Em abril de 2026, os números públicos são: **MemPalace 96,6% raw / 98,4% no modo hybrid v4**, **Mem0 ~93,4% (auto-reportado)** e **Zep 63,8% com gpt-4o-mini / 71,2% com gpt-4o** — não 85%, como circula em algumas coberturas. **Letta, Cognee, LangMem e SuperMemory não publicaram score**. **A-MEM usa LoCoMo, não LongMemEval**, então não entra na comparação direta. Esta nota organiza os números corrigidos, expõe trade-offs (acurácia × custo × latência × modelo base × versão) e dá recomendações por caso de uso, lembrando que score alto não implica best fit.

## O que é

[LongMemEval](https://github.com/xiaowu0162/LongMemEval) é um benchmark publicado em ICLR 2025 (Wu et al.) projetado para avaliar memória de longo prazo em **chat assistants** ao longo de múltiplas sessões. Cobre cinco-plus categorias: *single-hop reasoning*, *multi-hop reasoning*, *temporal reasoning*, *abstention* (saber quando dizer "não sei") e *knowledge-intensive QA*. As métricas mais reportadas são *Recall@5* (R@5) — proporção em que o trecho relevante aparece nos top-5 retrieved — e acurácia de resposta condicionada à recuperação.

A relevância do benchmark é dupla. Primeiro, ele captura o cenário real em que sistemas de memória são usados: conversas longas, com referências cruzadas a sessões anteriores, e a necessidade de não alucinar quando a informação não está disponível. Segundo, por ter sido aceito em ICLR 2025 e adotado por papers subsequentes (Mem0, Zep) como referência, tornou-se o **padrão de facto da indústria** — quem publica score em LongMemEval está participando de uma conversa pública mensurável; quem não publica obriga o leitor a tomar decisões com menos evidência.

## Por que importa

Sem um benchmark padrão, comparações entre sistemas de memória viram anedota: cada framework reporta sua própria métrica, em seu próprio cenário, com seu próprio modelo base — e nada é comparável. LongMemEval resolve parte desse problema, mas adiciona um problema novo: **agora todo mundo cita LongMemEval, e os números viram bullet point de marketing**, frequentemente sem o contexto necessário (qual modelo, qual versão, raw ou hybrid).

A consequência prática é que o **score sozinho não basta**. Precisa vir acompanhado de:

- **Modelo base usado** (gpt-4o-mini, gpt-4o, Claude Sonnet, etc.)
- **Modo de avaliação** (raw retrieval × hybrid com [[Dicionário de IA#reranking|reranking]])
- **Versão do benchmark** (v3, v4, etc.)
- **Quem reportou** (autoria do paper × terceiro independente)
- **Reprodutibilidade** (existe scaffolding público para reexecutar?)

Mais: a **ausência de score também é informação**. Letta, Cognee, LangMem e SuperMemory não publicaram resultado em LongMemEval em abril de 2026. Isso não é condenação automática — pode significar foco em outro tipo de workload, prioridade comercial sobre publicação, ou simplesmente que o benchmark não captura o que o sistema otimiza. Mas é um ponto a registrar quando a decisão é "qual ferramenta adotar".

## Como funciona — tabela rigorosa

A tabela abaixo consolida os números públicos em abril de 2026, com os ajustes feitos a partir da leitura direta dos READMEs oficiais e papers (em vez dos números marketing-flavored que circulam em coberturas secundárias).

| Sistema | LongMemEval (raw) | LongMemEval (hybrid) | Latência | Custo | Substrate | Open source? |
| --- | --- | --- | --- | --- | --- | --- |
| **MemPalace** | 96,6% R@5 | **98,4% v4** ¹ | low (≈170-token startup) | grátis local | spatial palace + SQLite + ChromaDB | sim (MIT) |
| **Mem0** | 93,4% (auto-reportado) | — | 91% lower vs full-context | $-$$ | vetor + grafo (Mem0g) | sim (Apache 2.0, lib) |
| **Zep** | 63,8% (gpt-4o-mini) / **71,2% (gpt-4o)** | — | tokens 115k→1,6k; latência 30s→3s | $$ | KG temporal (Neo4j) | engine sim (Graphiti, Apache 2.0); cloud não |
| **Letta** | **NÃO publicado** | — | — | $20-$200/mês ou self-host | hierarchical (RAM/disk) | sim (Apache 2.0) |
| **Cognee** | NÃO publicado | — | — | varia | KG + vetor | sim |
| **LangMem** | NÃO publicado | — | — | varia | namespaces sobre LangGraph | sim |
| **SuperMemory** | NÃO publicado | — | — | varia | proprietário | parcialmente |
| **A-MEM** | **Usa LoCoMo (não LongMemEval)** | — | — | research | Zettelkasten links | sim (research) |
| **basic-memory** | NÃO publicado (foco MCP/Obsidian) | — | low (markdown local) | grátis | markdown + SQLite FTS | sim (Apache 2.0) |
| **graphify** | NÃO publicado | — | — | grátis | KG sobre raw markdown | sim |
| **LLM-knowledge-base (Wendel)** | NÃO publicado (gist-grade) | — | low | grátis | markdown + SQLite | sim (gist) |

¹ MemPalace 98,4% é o número auditado a partir do README oficial (`github.com/milla-jovovich/mempalace`); coberturas externas reportam até ≈99-100%, e o **paper crítico arxiv 2604.21284** argumenta que o ganho real do modo hybrid vem de armazenamento verbatim + ChromaDB, não da hierarquia espacial. Auditoria externa em `lhl/agentic-memory/blob/main/ANALYSIS-mempalace.md` encontrou **20 MCP tools efetivamente implementadas** (não 29 como circulou em material de marketing) e um drop de 12,4 pontos percentuais (AAAK) em workloads adversariais. Análise completa em [[22 - Críticas, limitações e armadilhas]].

## Detalhes contextuais sobre LongMemEval

Quatro detalhes operacionais explicam a maior parte das discrepâncias quando se compara scores entre sistemas.

**Score depende fortemente do modelo base.** O caso Zep é o exemplo canônico: o paper `arxiv:2501.13956` §4.3.2 Tabela 2 reporta **63,8% com gpt-4o-mini** e **71,2% com gpt-4o** — quase oito pontos absolutos só pela troca de modelo, sem mudança no sistema de memória. Comparar Zep-com-gpt-4o-mini contra Mem0-com-gpt-4o (ou contra MemPalace, que reporta com modelos mais capazes) é, literalmente, *apples to oranges*. O ganho relativo do Zep sobre o baseline gpt-4o sem memória é de **+18,5% relativo (≈11 pontos absolutos)** — número que vale a pena memorizar para evitar a confusão com a métrica absoluta.

**Score depende do modo: raw vs hybrid.** "Raw" refere-se a retrieval direto do store. "Hybrid" envolve uma camada extra ([[Dicionário de IA#LLM (Large Language Model)|LLM]] reranking, expansão de query, fusão com keyword search). O salto MemPalace 96,6% → 98,4% é precisamente esse: ativando o pipeline hybrid v4. Não é necessariamente trapaça — é uma escolha arquitetural válida — mas comparar 98,4% hybrid de um sistema com 93,4% raw de outro embute uma comparação injusta.

**Score depende da versão do benchmark.** "v4" do MemPalace difere do conjunto de queries usado em reports anteriores. LongMemEval, como qualquer benchmark vivo, recebe atualizações; ler o número sem o sufixo de versão é arriscado.

**Quem não publicou também diz algo.** Letta (ex-MemGPT), Cognee, LangMem e SuperMemory não publicaram score em LongMemEval em abril de 2026. Para cada um há uma leitura plausível: Letta otimiza para *agentic loop* mais que para QA multi-session; Cognee aposta em pipelines de KG configuráveis e foca em casos enterprise específicos; LangMem é uma camada sobre LangGraph e o score ficaria condicionado ao agent que usa; SuperMemory tem componente proprietário. Nenhuma dessas leituras é desabono — mas o ponto de transparência fica.

**A-MEM usa LoCoMo, não LongMemEval.** A-MEM (NeurIPS 2025) reporta scores em [LoCoMo](https://github.com/snap-stanford/locomo), benchmark com cobertura sobreposta mas não idêntica. LoCoMo enfatiza *long conversation memory* com narrativas mais longas; LongMemEval cobre mais casos de abstention e temporal. Comparar A-MEM diretamente com MemPalace pelo número agregado é leitura preguiçosa.

> [!note] Sobre o número "85% do Zep" que circula
> Algumas coberturas secundárias atribuem ~85% ao Zep, frequentemente confundindo o score absoluto com o ganho relativo (+18,5%) ou misturando resultados de outro benchmark (DMR — Deep Memory Retrieval). **O paper original reporta 63,8% / 71,2% em LongMemEval. 85% não é o número.** Sempre que aparecer, vale rastrear até a fonte primária.

## Recomendações por caso de uso

Recomendar pelo score puro é o erro mais comum. As recomendações abaixo são por **caso de uso real**.

**Consultor solo / freelancer / knowledge worker que já vive no Obsidian.**
[[13 - basic-memory — MCP nativo Obsidian|basic-memory]] (vault Obsidian, MCP nativo) ou [[17 - MemPalace (Milla Jovovich)|MemPalace]] (local-first, ChromaDB embarcado). Score alto onde foi medido, custo zero, dados na própria máquina. Para fluxo Obsidian puro, basic-memory é menos invasivo; para fluxo Claude Code com workload de retrieval mais agressivo, MemPalace.

**Startup early-stage que precisa de memória "que funciona" ontem.**
[[15 - Mem0 — vetorial + grafo|Mem0]]. Lib open source (Apache 2.0), integrações com cerca de 24 frameworks, score auto-reportado de 93,4% em LongMemEval, latência reduzida em ≈91% vs full-context. Trade-off: o número é auto-reportado; reprodutibilidade externa é aceitável mas não comparável a um peer-reviewed completo.

**Enterprise regulado (banking, healthcare, gov).**
[[16 - Zep e Graphiti — knowledge graph temporal|Zep/Graphiti]] pelo *audit trail temporal* embutido no KG (Neo4j) — caso clássico de *temporal reasoning* (saber não só o fato, mas quando ele passou a valer e quando deixou de valer). Score absoluto mais baixo (71,2% com gpt-4o), mas o ganho de governança compensa em domínio regulado. Alternativa: [[14 - Letta (ex-MemGPT)|Letta]] (Apache 2.0, self-host on-prem fácil, sem score público mas com hierarquia clara RAM/disk e *core memory blocks*).

**Pesquisador acadêmico.**
[[19 - A-MEM — Zettelkasten dinâmico|A-MEM]] (paper NeurIPS 2025 + repo) como base experimental, **rodando LongMemEval e LoCoMo em paralelo** para benchmark próprio. A vantagem é que A-MEM expõe os hooks de Zettelkasten dinâmico, ideais para experimentar variações de write-path e linking automático.

**Quem quer dominar o pattern antes de adotar framework.**
[[10 - LLM-knowledge-base (Wendel) — direto do gist|LLM-knowledge-base (Wendel)]] + [[06 - O LLM Wiki Pattern (gist do Karpathy)|gist do Karpathy]]. Score nenhum publicado (não é o foco), mas a clareza didática é máxima — entende-se o esqueleto do pattern, e depois qualquer framework "sofisticado" vira uma variação compreensível.

**Quem precisa de KG com pipeline customizável.**
[[12 - graphify — knowledge graph de raw|graphify]] ou Cognee. Sem score público em LongMemEval, mas KG é forte em multi-hop e integridade referencial, áreas onde benchmarks de QA puro nem sempre brilham.

## Quando NÃO confiar em LongMemEval

LongMemEval é melhor que nada — mas é benchmark, não oráculo. Há cenários em que o score não deve dirigir a decisão.

- **Workload muito específico** (financeiro real-time, código, multimodal): rodar **benchmark próprio** com queries do domínio é mais informativo que qualquer score genérico.
- **Casos multimodal**. LongMemEval é text-only. Se o sistema vai indexar imagens, áudio ou vídeo, o score não captura o caso.
- **Casos que exigem temporal reasoning específico**. Zep "perde" no número agregado mas brilha em temporal — workloads com bitemporalidade pesada (when-was-true × when-was-known) escolhem Zep apesar do score.
- **Q&A sobre docs estáveis**. Se o caso é literalmente "responder perguntas sobre uma base de documentação que não muda", **[[Dicionário de IA#RAG (Retrieval-Augmented Generation)|RAG]] bem feito basta** (ver [[04 - RAG vs memória de longo prazo|04]]) — não há razão para adicionar memória de agente.
- **Conversas curtas**. LongMemEval mede *long-term*. Em chat de janela única, o benchmark não diferencia bem os sistemas.

## Armadilhas comuns

- **Score alto ≠ best fit.** Workload, modelo base, custo operacional e tolerância a infra pesam mais que o número absoluto.
- **Hybrid scores podem esconder overfitting.** O salto raw→hybrid de MemPalace levantou suspeita o suficiente para gerar paper crítico (arxiv 2604.21284). Não significa que hybrid é "trapaça" — significa que merece leitura cuidadosa. Detalhe em [[22 - Críticas, limitações e armadilhas]].
- **Self-reported scores sem reprodutibilidade independente.** Mem0 e MemPalace reportam os próprios números; reprodutibilidade externa existe mas é parcial. Tratar com hedge.
- **Modelo base pesa muito.** Zep com gpt-4o-mini (63,8%) versus Mem0 com gpt-4o (93,4%) **não é comparação válida** — modelos diferentes, mesmo benchmark, resultados não comensuráveis sem normalização.
- **Confundir LoCoMo (A-MEM) com LongMemEval.** Benchmarks relacionados, mas distintos. Cobertura, tipos de pergunta e protocolo de avaliação diferem.
- **"+18,5% sempre".** O ganho relativo do Zep foi medido **com gpt-4o**. Outros modelos podem variar — o número não é universal.
- **Marketing vs README.** Sempre cruzar o número com o que está no README oficial e no paper, não apenas em blog post de divulgação.

## Veja também

- [[09 - Panorama de implementações (abril 2026)|09 - Panorama]] — overview do mercado e contextualização
- [[10 - LLM-knowledge-base (Wendel) — direto do gist]] até [[17 - MemPalace (Milla Jovovich)|17 - MemPalace]] — implementações detalhadas, uma a uma
- [[18 - Generative Agents (Park, Stanford 2023)|18 - Generative Agents]] — fundação histórica do reflection loop
- [[19 - A-MEM — Zettelkasten dinâmico]] — usa LoCoMo, não LongMemEval
- [[20 - Surveys e estado da arte 2026|20 - Surveys]] — fundamentação acadêmica e cinco mecanismos arquiteturais
- [[22 - Críticas, limitações e armadilhas]] — auditoria do campo, paper crítico de MemPalace, leitura crítica do hybrid score
- [[23 - Guia de implementação do zero]] — escolha aplicada, com checklist de decisão

## Referências

1. **LongMemEval — repo oficial e paper ICLR 2025**: `https://github.com/xiaowu0162/LongMemEval`. Wu et al., *LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory*, ICLR 2025.
2. **Zep paper**: `https://arxiv.org/abs/2501.13956`. Rasmussen et al., *Zep: A Temporal Knowledge Graph Architecture for Agent Memory*, 2025. §4.3.2 Tabela 2 traz os números 63,8% / 71,2%.
3. **Mem0 paper**: `https://arxiv.org/abs/2504.19413`. Mem0 team, *Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory*, 2025. Score auto-reportado 93,4%; também `mem0.ai/research` e blog *State of AI Agent Memory 2026*.
4. **Paper crítico MemPalace**: `https://arxiv.org/abs/2604.21284`. Questiona origem do ganho hybrid; propõe que o ganho real vem de armazenamento verbatim + ChromaDB, não da hierarquia espacial.
5. **Análise externa MemPalace** (auditoria de MCP tools e robustez): `https://github.com/lhl/agentic-memory/blob/main/ANALYSIS-mempalace.md`. Encontrou 20 tools efetivamente implementadas e drop de 12,4pp em workload adversarial (AAAK).
6. **READMEs oficiais** das implementações: `github.com/milla-jovovich/mempalace`, `github.com/mem0ai/mem0`, `github.com/getzep/zep` e `github.com/getzep/graphiti`, `github.com/letta-ai/letta`, `github.com/basicmachines-co/basic-memory`.
7. **A-MEM (LoCoMo, não LongMemEval)**: NeurIPS 2025; ver [[19 - A-MEM — Zettelkasten dinâmico|18]] para detalhes de benchmark.
