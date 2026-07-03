---
title: "Roadmap — Anatomia de Agents"
created: 2026-07-02
type: meta
publish: false
tags:
  - meta
  - roadmap
---

# Roadmap — Anatomia de Agents

Diagnóstico migrado de guia/roadmap - ia.md (30/06). Cada entrada tem estado de enriquecimento, score, classificação de custo e plano de execução acionável.

**Galho:** `03-Dominios/Tecnologia/IA/Anatomia de Agents`

> [!success] Galho COMPLETO (2026-07-03). 11/11 notas enriquecidas via fan-out ≤3 subagentes com estágio verify do coordenador (Opus) em cada onda — toda URL/versão/fato conferido contra fonte real (PyPI/npm/WebSearch/WebFetch). Zero fabricação. Diagnóstico original de 30/06.

## Régua de análise

Checklist `verificar-nota` — 12 itens (isenções por fase/tipo/broto aplicadas por nota):

| Grupo | Itens |
|-------|-------|
| ESTRUTURA | E1 TL;DR · E2 Abertura-problema · E3 Mermaid · E4 Casos práticos · E5 O que vem a seguir · E6 Inglês · E7 Tabela PT↔EN · E8 Armadilhas [!warning] |
| PROFUNDIDADE | P1 Código-com-falha · P2 Mecanismo explicado |
| LINKS | L1 Wikilink cross-galho · L2 Referência externa (URL) |
| MÍDIA | M1 Vídeo/podcast embutido |

**Esquema de `fase:` detectado:** SEM fase (sequência)
**Piso de linhas:** N/A (sem fase)

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 11 |
| ⬜ pendente | 0 |
| ➖ não precisa | 0 |
| ✅ feita | 11 |
| 🔄 em andamento | 0 |
| % concluído | 100% |

---

## Notas

#### 01 - O que é um agent   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 190 linhas · fase: ausente · status: growing
- **Núcleo/gaps:** E5, L2, E8
- **Score:** 8/12
- **Plano de execução:**
  - Adicionar seção narrativa "O que vem a seguir" (antes de "## Ver mais") apontando para [[02 - O loop ReAct e native tool use]] com motivação concreta (o que define um agent → o mecanismo exato do loop, ReAct e tool calls nativas)
  - Adicionar URLs reais às referências em "## Referências" (Anthropic Building Effective Agents, OpenAI Practical Guide, ReAct paper arxiv, Lilian Weng blog)
  - Adicionar ≥2 callouts `[!warning]` adicionais com armadilhas concretas (chamar pipeline de agent não elimina fragilidade; max_steps sem limite como fonte de fatura inesperada)
- **Resultado:** ✅ "O que vem a seguir" → nota 02; 2 callouts [!warning] novos; 4 URLs em Referências. **Verify (coordenador):** as 4 URLs conferidas REAIS — Anthropic Building Effective Agents, OpenAI Practical Guide (WebSearch), ReAct arxiv:2210.03629, Lilian Weng. Zero fabricação.

#### 02 - O loop ReAct e native tool use   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 277 linhas · fase: ausente · status: growing
- **Núcleo/gaps:** E5, E8, P1
- **Score:** 9/12
- **Plano de execução:**
  - Adicionar seção narrativa "O que vem a seguir" apontando para [[03 - Tool design — princípios e categorias]] com motivação concreta (ritmo do loop ReAct vs. qualidade de cada passo dependendo do design das tools)
  - Converter os 4 pitfalls de "## Pitfalls do loop" (atualmente ### com prosa) para callouts `[!warning]` individuais
  - Opcional: extrair o snippet do bug da abertura (handler sem branch para `end_turn`) como bloco de código-com-falha seguido do fix
- **Resultado:** ✅ código-com-falha (BUG/FIX) extraído da abertura; 4 pitfalls → callouts [!warning]; "O que vem a seguir" → nota 03. **Verify (coordenador, git diff):** só mudanças estruturais, nenhuma URL/fato novo. Zero fabricação.

#### 03 - Tool design — princípios e categorias   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 264 linhas · fase: ausente · status: growing
- **Núcleo/gaps:** E5, E8
- **Score:** 10/12
- **Plano de execução:**
  - Adicionar seção narrativa "O que vem a seguir" apontando para `[[04 - Memory em agents]]` com motivação concreta (tool design certo → memória como próxima peça, sem a qual o agent refaz tool calls já executadas)
  - Converter a seção "## Anti-patterns" (5 itens em lista bullet) para callouts `[!warning]` individuais
- **Resultado:** ✅ "O que vem a seguir" → nota 04; 5 anti-patterns → 5 callouts [!warning] (+1 pré-existente = 6). **Verify (coordenador):** estrutural, nenhuma URL nova. Zero fabricação.

#### 04 - Memory em agents   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 219 linhas · fase: ausente · status: growing
- **Núcleo/gaps:** E5, E8, L2
- **Score:** 8/12
- **Plano de execução:**
  - Adicionar seção narrativa "O que vem a seguir" apontando para [[05 - Planning — plan-then-execute, dynamic, hierarchical]] com motivação concreta (memória define o que o agent lembra; planning define o que ele faz com esse conhecimento)
  - Converter a seção "## Anti-patterns" (5 itens em lista bullet) para callouts `[!warning]` individuais
  - Adicionar URLs reais às referências em "## Ver mais" (MemGPT arxiv, Lilian Weng blog)
- **Resultado:** ✅ "O que vem a seguir" → nota 05; 5 anti-patterns → callouts [!warning]; URLs MemGPT (arxiv:2310.08560) + Lilian Weng. **Verify (coordenador):** URLs conferidas REAIS; a 3ª ref (Effective Context Engineering) o subagente marcou honestamente "(URL a confirmar)" em vez de inventar. Zero fabricação.

#### 05 - Planning — plan-then-execute, dynamic, hierarchical   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 249 linhas · fase: ausente · status: growing / progress: done
- **Núcleo/gaps:** E5, E8, P1, L2
- **Score:** 8/12
- **Plano de execução:**
  - Adicionar seção narrativa "O que vem a seguir" apontando para [[06 - Multi-agent — orchestrator e sub-agents]] com motivação concreta (planning ancora um único agent; tarefa grande demais exige orquestração de sub-agents)
  - Converter a seção "## Anti-patterns" (6 itens em lista bullet) para callouts `[!warning]` individuais
  - Adicionar URLs reais às referências em "## Ver mais" e "## Referências" (arxiv:2305.04091, arxiv:2305.10601, Anthropic Building Effective Agents)
- **Resultado:** ✅ "O que vem a seguir" → nota 06; 6 anti-patterns → callouts [!warning]; 3 URLs canônicas (Plan-and-Solve 2305.04091, Tree of Thoughts 2305.10601, Anthropic BEA). **Verify (coordenador):** só as 3 URLs autorizadas, conferidas. Zero fabricação.

#### 06 - Multi-agent — orchestrator e sub-agents   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 267 linhas · fase: ausente · status: growing
- **Núcleo/gaps:** E5, L2
- **Score:** 10/12
- **Plano de execução:**
  - Adicionar seção narrativa "O que vem a seguir" apontando para [[07 - Frameworks 2026]] com motivação concreta (quando/como orquestrar → quais frameworks de 2026 implementam o padrão nativamente e o que cada um sacrifica)
  - Adicionar URLs reais às referências em "## Ver mais" e "## Referências" (Anthropic Building Effective Agents, Claude Agent SDK docs, Augment Code CIV, VeriMAP EACL 2026, OpenAI Swarm)
  - Opcional: converter a seção "## Anti-patterns" (6 itens em lista bullet) para callouts `[!warning]` individuais
- **Resultado:** ✅ "O que vem a seguir" → nota 07; 6 anti-patterns → callouts [!warning]; 5 URLs. **Verify (coordenador — galho de alto risco de fabricação):** TODAS as 5 URLs conferidas via WebFetch/WebSearch: Anthropic BEA ✓, OpenAI Swarm ✓, Claude Agent SDK subagents ✓ (302→platform.claude.com), Augment Code CIV ✓ (Paula Hingel), VeriMAP EACL 2026 ✓ (aclanthology 2026.eacl-long.353 = "Verification-Aware Planning for Multi-Agent Systems", Megagon/Hruschka). Zero fabricação. Nota: subagente ajustou título do doc SDK p/ o real ("Subagents in the SDK").

#### 07 - Frameworks 2026   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 319 linhas · fase: ausente · status: growing
- **Núcleo/gaps:** E5, E8
- **Score:** 9/12
- **Plano de execução:**
  - Adicionar seção narrativa "O que vem a seguir" apontando para [[08 - Patterns comuns de agents]] com motivação concreta (escolher/recusar framework → patterns que qualquer stack precisa implementar, com ou sem framework)
  - Converter a seção "## Anti-patterns" (5 itens em lista bullet) para callouts `[!warning]` individuais
  - Pesquisar e atualizar caducidade em "## O panorama em uma tabela" (rankings de popularidade, versões de Claude Agent SDK/Pydantic AI, estimativas de semanas-até-produção) e adicionar `[!info]`/`[!warning]` de validade dos dados
- **Resultado:** ✅ "O que vem a seguir" → nota 08; 5 anti-patterns → callouts [!warning]; [!info] de validade + [!warning] "estimativas não medição" na tabela. **Verify (coordenador — versões conferidas em PyPI/npm oficiais):** claude-agent-sdk Python 0.2.110 ✓ EXATO; pydantic-ai corrigido v2.3.0→**v2.4.0** e TS SDK 0.3.197→**0.3.200** (números reais, só drift de horas — nota já hedava volatilidade). Zero fabricação; "semanas até produção" honestamente marcado como estimativa qualitativa, não benchmark.

#### 08 - Patterns comuns de agents   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 251 linhas · fase: ausente · status: growing / progress: done
- **Núcleo/gaps:** E5, E8, L2
- **Score:** 8/12
- **Plano de execução:**
  - Adicionar seção narrativa "O que vem a seguir" apontando para a nota 09 do galho (Evaluation de agents)
  - Expandir o único `[!warning]` composto (5 sub-itens agrupados) em ≥3 callouts `[!warning]` individuais com título descritivo
  - Adicionar URLs reais às referências em "## Ver mais" e "## Referências" (Anthropic Building Effective Agents, OpenAI Practical Guide, LangChain blog supervisor patterns)
- **Resultado:** ✅ "O que vem a seguir" → nota 09; [!warning] composto expandido em 4 individuais; URLs Anthropic BEA + OpenAI Practical Guide (canônicas). **Verify (coordenador):** LangChain supervisor patterns o subagente marcou honestamente "(URL a confirmar)" — não achou o post exato. Zero fabricação.

#### 09 - Evaluation de agents   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 278 linhas · fase: ausente · status: growing
- **Núcleo/gaps:** E5, E8
- **Score:** 9/12
- **Plano de execução:**
  - Adicionar seção "O que vem a seguir" com ponte narrativa para a nota 10 (Workflow vs Agent — quando usar cada um)
  - Converter os 6 bullets de "## Anti-patterns" em ≥3 callouts `[!warning]` individuais com título descritivo
- **Resultado:** ✅ "O que vem a seguir" → nota 10; 6 anti-patterns → 6 callouts [!warning]. **Verify (coordenador):** puramente estrutural, nenhuma URL/fato novo. Zero fabricação.

#### 10 - Workflow vs Agent — quando usar cada um   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 190 linhas · fase: ausente · status: growing / progress: done
- **Núcleo/gaps:** E5, E8, P1
- **Score:** 9/12
- **Plano de execução:**
  - Adicionar seção narrativa "O que vem a seguir" com ponte para [[11 - Harness engineering — a terceira camada]] com motivação concreta (workflow-vs-agent escolhido → onde o código vive, o harness que envolve o loop com retry/tracing/cost guard/human-in-the-loop)
  - Converter a seção "## Custos e riscos" (5 bullets) para callouts `[!warning]` individuais com título descritivo
- **Resultado:** ✅ "O que vem a seguir" → nota 11; 5 custos/riscos → callouts [!warning]. **Verify (coordenador):** estrutural, 0 URLs novas. Zero fabricação.

#### 11 - Harness engineering — a terceira camada   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 217 linhas · fase: ausente · status: growing / progress: done
- **Núcleo/gaps:** E5, E8, P1
- **Score:** 9/12
- **Plano de execução:**
  - Adicionar seção narrativa "O que vem a seguir", por ser a última nota do galho: fechar o ciclo de Anatomia de Agents e abrir pontes explícitas para os galhos que aprofundam dimensões do harness (Context Engineering = budget, Memória de Agentes = estado, Evaluation = loop de melhoria)
  - Adicionar ≥2 callouts `[!warning]` adicionais com armadilhas concretas (build to delete — hooks compensatórios podem trabalhar contra o próximo modelo; benchmarks sem HarnessCard medem variável confundida)
- **Resultado:** ✅ "O que vem a seguir" fecha o galho + pontes cross-galho ([[Context Engineering]], [[Memória de Agentes]], [[Evaluation]], [[Observability]], [[Economia de Tokens]], [[Segurança e Guardrails]] — todas com index.md confirmado); 2 callouts [!warning] novos (build-to-delete; benchmark sem HarnessCard). **Verify (coordenador):** 0 URLs novas, wikilinks cross-galho resolvem. Zero fabricação.
