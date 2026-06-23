---
title: "Memória de Agentes"
type: moc
publish: true
tags: [memoria-agentes, ia, moc]
created: 2026-04-25
updated: 2026-05-06
---

# Memória de Agentes

Memória de agentes é o campo que estuda como sistemas baseados em [[Dicionário de IA#LLM (Large Language Model)|LLMs]] podem reter, recuperar e evoluir conhecimento ao longo do tempo, indo além da [[Dicionário de IA#Context window|janela de contexto]] efêmera de uma única conversa. O tema ganhou tração consolidada em 2026 com surveys de referência, o workshop "MemAgents" no ICLR e uma proliferação de frameworks concorrentes — MemGPT/Letta, Mem0, Zep, MemPalace, A-MEM, basic-memory, OpenKB, entre outros — cada um com sua aposta arquitetural. O gancho de relevância contemporânea veio do gist publicado por [[Andrej Karpathy]] em 3 de abril de 2026, descrevendo o "LLM Wiki Pattern": uma arquitetura de três camadas que reposicionou a discussão sobre substratos de memória (markdown, grafos, vetores) na comunidade. Esta trilha percorre o campo do conceito básico ao guia de implementação, passando pela taxonomia clássica, pelo panorama de implementações disponíveis e pela leitura crítica do estado da arte.

> [!warning] Avisos importantes
> - O domínio `mempalace.tech` é impostor com malware. Apenas `github.com/milla-jovovich/mempalace` e `github.com/MemPalace/mempalace` são oficiais.
> - Dois links que apareceram nas pesquisas iniciais NÃO são sobre memória de agentes apesar do nome: `Mattbusel/srfm-lab` (lab de trading quantitativo) e `forrestchang/andrej-karpathy-skills` (princípios de coding do Karpathy). Ficam fora desta trilha.

> [!info] Pré-leitura sugerida
> Esta trilha menciona "RAG" como termo de referência. Se você nunca leu sobre RAG, dê uma passada nos níveis 1-2 de [[RAG e Vector Databases]] antes de começar — ou siga direto, porque a nota 04 traz um primer rápido com o necessário.

## Comece por aqui

Trilha sequencial recomendada — leia na ordem para construir o terreno do conceito até a implementação.

- [[01 - O que é memória em IA]] — distinção entre memória in-context, persistente e parametrizada
- [[02 - O problema das janelas de contexto]] — por que contexto longo não substitui memória persistente
- [[03 - Taxonomia da memória (episódica, semântica, procedural)|03 - Taxonomia da memória]] — categorias clássicas da ciência cognitiva aplicadas a agentes
- [[04 - RAG vs memória de longo prazo]] — primer de RAG e onde ele acaba
- [[05 - Beyond RAG - quando RAG não basta|05 - Beyond RAG]] — limites do retrieval puro e o que aparece depois
- [[06 - O LLM Wiki Pattern (gist do Karpathy)|06 - O LLM Wiki Pattern]] — o gist do Karpathy de abril/2026 e arquitetura de 3 camadas
- [[07 - Por que Obsidian e markdown como substrato]] — markdown como camada humana legível em sistemas de memória
- [[08 - Arquitetura de um sistema de memória]] — componentes, fluxos de escrita/leitura e decisões de design
- [[09 - Panorama de implementações (abril 2026)|09 - Panorama de implementações]] — mapa dos frameworks e bibliotecas em circulação
- [[10 - LLM-knowledge-base (Wendel) — direto do gist|10 - LLM-knowledge-base (Wendel)]] — implementação de referência derivada do gist
- [[11 - OpenKB — wiki compilada com PageIndex|11 - OpenKB]] — wiki compilada com PageIndex para documentos longos
- [[12 - graphify — knowledge graph de raw|12 - graphify]] — construção de grafo de conhecimento sobre dados brutos
- [[13 - basic-memory — MCP nativo Obsidian|13 - basic-memory]] — servidor MCP que trata o vault como memória
- [[14 - Letta (ex-MemGPT)|14 - Letta]] — herdeiro do MemGPT, com memória hierárquica e gerenciada pelo agente
- [[15 - Mem0 — vetorial + grafo|15 - Mem0]] — abordagem híbrida de embeddings e grafo
- [[16 - Zep e Graphiti — knowledge graph temporal|16 - Zep e Graphiti]] — grafo de conhecimento com dimensão temporal
- [[17 - MemPalace (Milla Jovovich)|17 - MemPalace]] — projeto de memória inspirado em palácio mental
- [[18 - Generative Agents (Park, Stanford 2023)|18 - Generative Agents]] — paper seminal de Stanford com reflexão e recuperação por relevância
- [[19 - A-MEM — Zettelkasten dinâmico|19 - A-MEM]] — memória inspirada em Zettelkasten com links emergentes
- [[20 - Surveys e estado da arte 2026|20 - Surveys e estado da arte]] — leituras de consolidação do campo
- [[21 - Comparativo crítico (LongMemEval)|21 - Comparativo crítico]] — benchmarks e comparações entre frameworks
- [[22 - Críticas, limitações e armadilhas]] — pontos cegos, custos e falhas comuns
- [[23 - Guia de implementação do zero]] — passo a passo para montar um sistema próprio
- [[24 - Aplicações comerciais e modelo de negócio|24 - Aplicações comerciais]] — onde memória de agentes vira produto

## Rotas alternativas

### Rota gerencial (entender e vender)
[[01 - O que é memória em IA]] → [[02 - O problema das janelas de contexto]] → [[06 - O LLM Wiki Pattern (gist do Karpathy)|06 - O LLM Wiki Pattern]] → [[09 - Panorama de implementações (abril 2026)|09 - Panorama]] → [[24 - Aplicações comerciais e modelo de negócio|24 - Aplicações comerciais]]

### Rota técnica (implementar)
[[04 - RAG vs memória de longo prazo]] → [[06 - O LLM Wiki Pattern (gist do Karpathy)|06 - O LLM Wiki Pattern]] → [[08 - Arquitetura de um sistema de memória]] → [[09 - Panorama de implementações (abril 2026)|09 - Panorama]] → [[23 - Guia de implementação do zero]]

### Rota acadêmica (fundamentar discurso)
[[03 - Taxonomia da memória (episódica, semântica, procedural)|03 - Taxonomia]] → [[18 - Generative Agents (Park, Stanford 2023)|18 - Generative Agents]] → [[19 - A-MEM — Zettelkasten dinâmico|19 - A-MEM]] → [[20 - Surveys e estado da arte 2026|20 - Surveys]] → [[22 - Críticas, limitações e armadilhas]]

### Rota implementador (mão na massa rápida)
[[06 - O LLM Wiki Pattern (gist do Karpathy)|06 - O LLM Wiki Pattern]] → [[13 - basic-memory — MCP nativo Obsidian|13 - basic-memory]] → [[23 - Guia de implementação do zero]]

## Todas as notas

```dataview
LIST file.frontmatter.title
FROM "IA/Memória de Agentes"
WHERE type != "moc"
SORT file.name ASC
```
