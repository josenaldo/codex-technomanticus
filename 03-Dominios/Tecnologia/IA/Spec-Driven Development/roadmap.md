---
title: "Roadmap — Spec-Driven Development"
created: 2026-07-02
type: meta
publish: false
tags:
  - meta
  - roadmap
---

# Roadmap — Spec-Driven Development

Diagnóstico migrado de guia/roadmap - ia.md (30/06). Cada entrada tem estado de enriquecimento, score, classificação de custo e plano de execução acionável.

**Galho:** `03-Dominios/Tecnologia/IA/Spec-Driven Development`

> [!warning] Diagnóstico de 30/06 — pode estar defasado. Vários itens marcados ⬜ podem já ter sido enriquecidos depois; reconciliar com o estado real ao tratar o galho.

## Régua de análise

Checklist `verificar-nota` — 12 itens (isenções por fase/tipo/broto aplicadas por nota):

| Grupo | Itens |
|-------|-------|
| ESTRUTURA | E1 TL;DR · E2 Abertura-problema · E3 Mermaid · E4 Casos práticos · E5 O que vem a seguir · E6 Inglês · E7 Tabela PT↔EN · E8 Armadilhas [!warning] |
| PROFUNDIDADE | P1 Código-com-falha · P2 Mecanismo explicado |
| LINKS | L1 Wikilink cross-galho · L2 Referência externa (URL) |
| MÍDIA | M1 Vídeo/podcast embutido |

**Esquema de fase detectado:** SEM fase (sequência)
**Piso de linhas:** N/A

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 12 |
| ⬜ pendente | 0 |
| ➖ não precisa | 0 |
| ✅ feita | 12 |
| 🔄 em andamento | 0 |
| % concluído | 100% (2026-07-03, fan-out ≤3 verificado) |

---

## Notas

#### 01 - O problema do vibe coding em produção   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 401 linhas · fase: ausente · status: evergreen
- **Núcleo/gaps:** E5, E6, E7, P1, L2
- **Score:** 7/12
- **Plano de execução:**
  - Adicionar seção "O que vem a seguir" apontando para [[02 - O que é Spec-Driven Development]] com motivação concreta
  - Adicionar seção "Como explicar em inglês" com tabela PT↔EN dos termos centrais (vibe coding, tech debt, spec, context drift, acceptance criteria, regression, blast radius, velocity mismatch, code review, hallucination)
  - Adicionar URLs reais às referências (arxiv:2512.11922, Veracode, GitClear, Augment Code)
- **Resultado:** +23 linhas (424 total). Seções "O que vem a seguir"→nota 02 e "Como explicar em inglês" (tabela PT↔EN 10 termos) adicionadas. URLs VERIFICADAS pelo coordenador: arxiv:2512.11922 (Waseem et al., "Vibe Coding in Practice: Flow, Technical Debt...") real e exato; Veracode 2025 GenAI Code Security Report real; GitClear real (subagente corrigiu título p/ "AI Copilot Code Quality: 2025... 4x Growth in Code Clones"). Augment Code deixado "(a confirmar)" — citação literal não localizada (sem fabricação).

#### 02 - O que é Spec-Driven Development   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 401 linhas · fase: ausente · status: evergreen
- **Núcleo/gaps:** E5, L2, E8, E6, E7
- **Score:** 6/12
- **Plano de execução:**
  - Adicionar seção "O que vem a seguir" apontando para [[03 - Níveis de rigor — spec-first, spec-anchored, spec-as-source]]
  - Adicionar URLs reais às referências (GitHub Blog Spec Kit, Augment Code, Microsoft for Developers, Martin Fowler, Amazon Kiro, OpenSpec, DeepLearning.AI)
  - Adicionar ≥3 callouts `[!warning]` individuais com armadilhas concretas (spec sem acceptance criteria mensuráveis, spec fora do repositório, outcomes misturados com decisões técnicas)
  - Adicionar seção "Como explicar em inglês" com tabela PT↔EN (especificação, contrato, critério de aceitação, source of truth, fora do escopo, versionamento, artefato, validação, entregável, rastreabilidade)
- **Resultado:** Seção "O que vem a seguir"→nota 03; 3 callouts [!warning] (spec sem acceptance criteria mensuráveis / fora do repositório / outcomes misturados com decisões técnicas); seção "Como explicar em inglês" (tabela 10 termos). URLs VERIFICADAS: github.blog Spec Kit, Augment Code guide, Microsoft for Devs (spec-driven-development-spec-kit), Martin Fowler sdd-3-tools, kiro.dev, OpenSpec Fission-AI, DeepLearning.AI course — todas reais. Subagente renomeou "Amazon"→"Kiro (AWS)" (domínio kiro.dev) e marcou OpenSpec "v0.3" como "(a confirmar)".

#### 03 - Níveis de rigor — spec-first, spec-anchored, spec-as-source   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 399 linhas · fase: ausente · status: evergreen
- **Núcleo/gaps:** E5, E6, E7, E8, P1, L2
- **Score:** 6/12
- **Plano de execução:**
  - Adicionar seção "O que vem a seguir" apontando para [[04 - Fase Specify — definindo outcomes e constraints]]
  - Adicionar URLs reais às 20+ referências sem hiperlinks (GitHub Blog, Kiro, Tessl, Martin Fowler)
  - Adicionar ≥3 callouts `[!warning]` individuais (spec-as-source sem cultura de spec-anchored, spec-first em projetos com mudança frequente, mistura de níveis sem registro arquitetural)
  - Adicionar seção "Como explicar em inglês" com tabela PT↔EN (spec estática, spec viva, spec como fonte, fonte autoritativa, critério de aceitação, drift de spec, rastreabilidade, código derivado, checklist de aceitação, versionamento)
- **Resultado:** 431 linhas. Seção "O que vem a seguir"→nota 04; 22 refs com URL; 3 callouts [!warning] (spec-first em projeto com mudança frequente / spec-as-source sem cultura spec-anchored / mistura de níveis sem registro arquitetural); seção "Como explicar em inglês" (10 termos). URLs canônicas (DDIA, OpenAPI 3.1, NIST, ISO 25010, PCI, HIPAA, Fowler microservices) + SDD (Fowler sdd-3-tools, github.blog, Hashrocket, Augment Code) VERIFICADAS reais. Kiro e Tessl (títulos de artigo exatos) marcados "(referência a confirmar)" — sem fabricação.

#### 04 - Fase Specify — definindo outcomes e constraints   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 407 linhas · fase: ausente · status: evergreen
- **Núcleo/gaps:** E5, L2, E8
- **Score:** 7/12
- **Plano de execução:**
  - Adicionar parágrafo "O que vem a seguir" apontando para [[05 - Fase Design e Plan — arquitetura e decomposição]]
  - Adicionar URLs reais a pelo menos 1 referência (Augment Code, GitHub Spec Kit)
  - Adicionar ≥2 callouts `[!warning]` adicionais (spec sem out-of-scope declarado, open questions não documentadas)
- **Resultado:** Parágrafo "O que vem a seguir"→nota 05; 2 URLs reais VERIFICADAS (github/spec-kit/blob/main/spec-driven.md; augmentcode.com/guides/what-is-spec-driven-development); 2 callouts [!warning] (scope creep silencioso / decisão por default). Nenhum desvio.

#### 05 - Fase Design e Plan — arquitetura e decomposição   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 420 linhas · fase: ausente · status: evergreen
- **Núcleo/gaps:** E5, L2, E8, L1, E6, E7
- **Score:** 5/12
- **Plano de execução:**
  - Adicionar parágrafo "O que vem a seguir" apontando para [[06 - Fase Implement — execução disciplinada]]
  - Adicionar URLs reais a pelo menos 1 referência (Microsoft, Nygard ADR)
  - Converter a seção "Anti-patterns" (tabela com 7 itens) para callouts `[!warning]` individuais
  - Adicionar wikilink cross-galho pertinente ([[Context Engineering]] ou [[Economia de Tokens]])
  - Adicionar seção "Como explicar em inglês" + tabela PT↔EN (spec, plan, ADR, task, acceptance criteria, decomposition, dependency, interface, component, constraint)
- **Resultado:** Parágrafo "O que vem a seguir"→nota 06; tabela Anti-patterns (7) → 7 callouts [!warning] individuais; wikilink cross-galho [[Context Engineering]] (index.md confirmado); seção "Como explicar em inglês" (10 termos). URLs VERIFICADAS: Microsoft for Devs (subagente corrigiu ano 2026→2025); Nygard ADR (cognitect.com/blog/2011/11/15/documenting-architecture-decisions) real.

#### 06 - Fase Implement — execução disciplinada   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 393 linhas · fase: ausente · status: evergreen
- **Núcleo/gaps:** E5, L2, E8, L1, E6, E7
- **Score:** 5/12
- **Plano de execução:**
  - Adicionar seção "O que vem a seguir" apontando para [[07 - Fase Validate — spec como contrato executável]]
  - Adicionar URLs reais a pelo menos 1 referência (Forsgren et al. *Accelerate*, DORA 2025)
  - Converter a tabela "Anti-patterns da fase Implement" (8 itens) para callouts `[!warning]` individuais
  - Adicionar wikilink cross-galho pertinente ([[Context Engineering]] ou [[Economia de Tokens]])
  - Adicionar seção "Como explicar em inglês" + tabela PT↔EN (spec, plan, task, acceptance criteria, test-first, spec drift, atomic task, scope creep, commit traceability, spec-anchored)
- **Resultado:** Seção "O que vem a seguir"→nota 07; tabela Anti-patterns (8) → 8 callouts [!warning]; wikilink cross-galho [[Context Engineering|05 - Camadas de contexto]]; seção "Como explicar em inglês" (10 termos). URLs VERIFICADAS: Accelerate (itrevolution.com/product/accelerate); DORA 2025 — subagente corrigiu título p/ "State of AI-Assisted Software Development" e **coordenador corrigiu URL** p/ canônica dora.dev/dora-report-2025.

#### 07 - Fase Validate — spec como contrato executável   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 395 linhas · fase: ausente · status: evergreen · progress: complete
- **Núcleo/gaps:** E5, E6, E7, E8, P1, L1, L2
- **Score:** 6/12
- **Plano de execução:**
  - Adicionar seção "O que vem a seguir" apontando para [[08 - Ferramentas SDD — Kiro, Spec Kit, OpenSpec, Tessl]]
  - Adicionar URLs reais a ≥1 referência (arxiv:2512.08769, k6, OWASP Zap)
  - Converter a tabela "Anti-patterns na fase Validate" (7 itens) para callouts `[!warning]` individuais
  - Adicionar wikilink cross-galho pertinente ([[Economia de Tokens]] ou [[Context Engineering]])
  - Adicionar seção "Como explicar em inglês" + tabela PT↔EN (validação, contrato executável, critério de aceitação, desvio/drift, cobertura, pipeline de CI, gate de qualidade, NFR, detecção de drift, especificação viva)
- **Resultado:** Seção "O que vem a seguir"→nota 08; tabela Anti-patterns (7)→7 callouts [!warning]; wikilink cross-galho [[Context Engineering/12 - Guardrails determinísticos]] (alvo confirmado); seção "Como explicar em inglês" (10 termos). URLs VERIFICADAS: arxiv:2512.08769 ("A Practical Guide for... Production-Grade Agentic AI Workflows", Bandara et al.) real e exato; k6 (grafana.com/docs/k6); OWASP ZAP (zaproxy.org).

#### 08 - Ferramentas SDD — Kiro, Spec Kit, OpenSpec, Tessl   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 361 linhas · fase: ausente · status: evergreen
- **Núcleo/gaps:** E5, E6, E7, E8, P1, L2
- **Score:** 6/12
- **Plano de execução:**
  - Adicionar parágrafo "O que vem a seguir" apontando para [[09 - SDD com agentes — coordinator, implementor, validator]]
  - Adicionar URLs reais nas referências (github.com/github/spec-kit, kiro.dev, martinfowler.com)
  - Adicionar ≥3 callouts `[!warning]` com armadilhas concretas (Kiro e Spec Kit em paralelo, Tessl exige domínio formalmente modelável, Kiro sem steering files)
  - Adicionar `[!warning]` de caducidade (stars do Spec Kit, end-of-support Q Developer, recomendação datada jun/2026) nas seções "GitHub Spec Kit" e "A recomendação de start"
- **Resultado:** Parágrafo "O que vem a seguir"→nota 09; URLs reais (github/spec-kit, kiro.dev, martinfowler sdd-3-tools); 3 callouts armadilha + 2 caducidade. Números VERIFICADOS pelo coordenador: EOS Q Developer 30/abr/2027 + signups bloqueados 15/mai/2026 (blog AWS, exato); stars 88k datado "abr/2026" com callout de caducidade honesto apontando ~111k em jun/2026 (star-history confirmou). Zero número cravado sem data.

#### 09 - SDD com agentes — coordinator, implementor, validator   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 419 linhas · fase: ausente · status: evergreen
- **Núcleo/gaps:** E5, L2, E8, L1, E6, E7
- **Score:** 5/12
- **Plano de execução:**
  - Adicionar seção "O que vem a seguir" apontando para [[10 - Integração com context engineering — specs como contexto persistente]]
  - Adicionar URLs reais nas referências (arxiv:2512.08769, Anthropic Claude Agent SDK, Kiro custom subagents)
  - Adicionar ≥2 callouts `[!warning]` adicionais (DAG com paralelo_safe em tasks que compartilham arquivo, coordinator que recebe transcrição completa dos implementors)
  - Adicionar wikilink cross-galho pertinente ([[Economia de Tokens]] ou [[Context Engineering]])
  - Adicionar seção "Como explicar em inglês" + tabela PT↔EN (coordenador, implementador, validador, grafo acíclico dirigido, isolamento de contexto, tarefa, critério de aceitação, paralelismo, replanejamento, escalonamento)
- **Resultado:** 446 linhas. Seção "O que vem a seguir"→nota 10; 2 callouts [!warning] (parallel_safe + race em arquivo compartilhado / coordinator não recebe transcrição completa); wikilink cross-galho [[Economia de Tokens/10 - Sub-agentes especializados]] (alvo confirmado); seção "Como explicar em inglês" (10 termos). URLs VERIFICADAS: arxiv:2512.08769 (mesmo paper Bandara et al., exato); Claude Agent SDK (code.claude.com/docs/en/agent-sdk/subagents, subagente seguiu redirects); Kiro custom subagents (kiro.dev/docs/chat/subagents, chutada 404 corrigida p/ real).

#### 10 - Integração com context engineering — specs como contexto persistente   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 401 linhas · fase: ausente · status: evergreen
- **Núcleo/gaps:** E5, E6, E7, E8, P1, L1, L2
- **Score:** 6/12
- **Plano de execução:**
  - Adicionar parágrafo "O que vem a seguir" apontando para [[11 - Guia de implementação SDD — do zero ao projeto]]
  - Adicionar URLs nas referências (Kiro, Anthropic context engineering, Augment Code)
  - Adicionar wikilink cross-galho para [[Context Engineering]]
  - Converter a tabela "Anti-patterns na integração" (8 itens) para ≥3 callouts `[!warning]` individuais (spec gigantesca >3K tokens, compactação que toca spec, spec retroativa falsa)
  - Adicionar seção "Como explicar em inglês" + tabela PT↔EN (especificação, contexto persistente, recuperação cirúrgica, compactação, âncora de contexto, região protegida, drift de especificação, arquivo de agentes, tarefa, memória externa)
- **Resultado:** Parágrafo "O que vem a seguir"→nota 11; wikilink cross-galho [[Context Engineering]]; tabela Anti-patterns (8)→8 callouts [!warning]; seção "Como explicar em inglês" (10 termos). URLs VERIFICADAS: Anthropic effective-context-engineering (anthropic.com/engineering), Kiro steering (kiro.dev/docs/steering), Augment Code guides. Refs sem fonte exata (Atlan, VeriMAP, Karpathy, Willison, case study "64%") marcadas honestamente "(a confirmar)".

#### 11 - Guia de implementação SDD — do zero ao projeto   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 431 linhas · fase: ausente · status: evergreen
- **Núcleo/gaps:** E2, E5, L2, E8, E3, E6, E7
- **Score:** 4/12
- **Plano de execução:**
  - Adicionar parágrafo de abertura com problema/cenário antes de "Pré-requisitos" (você leu sobre SDD, mas como começa na prática?)
  - Adicionar seção "O que vem a seguir" apontando para [[12 - Debates — spec-as-source vs pragmatismo]]
  - Adicionar URLs reais às referências (GitHub Blog, Microsoft for Developers, Augment Code, Zencoder, DeepLearning.AI/JetBrains, BMAD, Hashrocket)
  - Expandir para ≥3 callouts `[!warning]` individuais (adoção parcial contamina o restante, spec retroativa descreve bugs como desejados, task grande demais quebra a regra das 3h)
  - Adicionar ≥1 diagrama Mermaid (flowchart das semanas 0→12 ou sequenceDiagram spec→plan→tasks→implement→gate)
  - Adicionar seção "Como explicar em inglês" + tabela PT↔EN (especificação, critério de aceitação, desvio, âncora, validação, tarefa, granularidade, adoção incremental, retroativa, manutenção de spec)
- **Resultado:** Parágrafo de abertura (problema) + sequenceDiagram Mermaid (spec→plan→tasks→implement→gate, sintaxe VALIDADA); seção "O que vem a seguir"→nota 12; 4 callouts [!warning] (adoção parcial / task grande / spec retroativa + existente); seção "Como explicar em inglês" (10 termos). URLs VERIFICADAS: github.blog, Microsoft, Augment Code, Zencoder (403 bot-block, domínio real), DeepLearning.AI, BMAD (bmad-code-org "Working in the Brownfield" real). Hashrocket "30-day retro" não localizado → "(a confirmar)".

#### 12 - Debates — spec-as-source vs pragmatismo   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 401 linhas · fase: ausente · status: evergreen
- **Núcleo/gaps:** E5, L2, L1, E8
- **Score:** 5/12
- **Plano de execução:**
  - Adicionar seção "O que vem a seguir" com ponte narrativa para outros galhos de IA ([[Agentes de Codificação]], [[Context Engineering]], [[Prompt Engineering]])
  - Adicionar URLs reais às 14 referências (arxiv:2512.11922, arxiv:2506.14981, Andrej Karpathy, Salesforce Ben, Augment Code, Martin Fowler, Simon Willison, ThoughtWorks Radar, Stack Overflow Developer Survey 2026)
  - Adicionar ≥1 wikilink cross-galho na "Posição de fechamento" ou no corpo ([[Agentes de Codificação]] ou [[Context Engineering]])
  - Converter ≥3 limites/armadilhas da seção "Quando o método te trai" para callouts `[!warning]` individuais
- **Resultado:** Seção "O que vem a seguir" + wikilinks cross-galho ([[Agentes de Codificação]], [[Context Engineering]], [[Prompt Engineering]] — todos confirmados); seção "Quando o método te trai" (5)→callouts [!warning]. Verify do coordenador aplicou 3 correções factuais: (a) **ThoughtWorks Radar Adopt→Assess** (vol.34, confirmado); (b) **arxiv:2506.14981 NÃO é SDD** (é Zarr/geoespacial) → substituído por arxiv:2602.00180 "Spec-Driven Development: From Code to Contract" (Piskala, real e exato); (c) **SO survey /2026 era 404** → corrigido p/ edição publicada /2025. Karpathy tweet (fev/2025) e demais URLs (Salesforce Ben, Pixelmojo, Fowler, Augment Code, Kent Beck LinkedIn) verificadas.
