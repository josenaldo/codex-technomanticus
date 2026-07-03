---
title: "Roadmap — Skills e MCP"
created: 2026-07-02
type: meta
publish: false
tags:
  - meta
  - roadmap
---

# Roadmap — Skills e MCP

Diagnóstico nota a nota. Cada entrada tem estado de enriquecimento, score, classificação
de custo e plano de execução acionável. Gerado por `/diagnosticar-galho`.

**Galho:** `03-Dominios/Tecnologia/IA/Claude Code/Skills e MCP`
**Nível:** galho-folha
**Diagnóstico:** 2026-07-02
**Última execução:** —

## Régua de análise

Checklist `verificar-nota` — 12 itens (isenções por fase/tipo/broto aplicadas por nota):

| Grupo | Itens |
|-------|-------|
| ESTRUTURA | E1 TL;DR · E2 Abertura-problema · E3 Mermaid · E4 Casos práticos · E5 O que vem a seguir · E6 Inglês · E7 Tabela PT↔EN · E8 Armadilhas [!warning] |
| PROFUNDIDADE | P1 Código-com-falha · P2 Mecanismo explicado |
| LINKS | L1 Wikilink cross-galho · L2 Referência externa (URL) |
| MÍDIA | M1 Vídeo/podcast embutido |

**Esquema de `fase:` detectado:** SEM fase (sequência 01→08)
**Piso de linhas:** não aplicável

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 8 |
| ⬜ pendente | 8 |
| ➖ não precisa | 0 |
| ✅ feita | 0 |
| % concluído | 0% |

> Diagnóstico concluído em 2026-07-02. Custo: 8 `[substantivo]` · 0 `[mecânico]`.

---

## Notas

#### 01 - Anatomia de uma skill   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 400 linhas reais · fase: ausente · status: evergreen
- **Núcleo/gaps:** E4, E5, E7, E8, L2, M1
- **Score:** 6/12
- **Plano de execução:**
  - Adicionar `## Casos práticos` com ≥2 cenários reais de produção (skill quebrando em time real, skill salvando incidente) → ativa E4
  - Adicionar `## O que vem a seguir` com ponte narrativa pra nota 02 (não só lista de links) → ativa E5
  - Adicionar tabela PT↔EN de termos-chave (skill, process skill, domain skill, frontmatter) → ativa E7
  - Converter os 5 itens de `## Armadilhas comuns` em callouts `[!warning]` → ativa E8
  - Renomear `## Referências` para `## Fontes` (ou adicionar `## Fontes` equivalente) mantendo as URLs já clicáveis → ativa L2
  - Pesquisar e embutir ≥1 `[!tip]` com vídeo/podcast sobre skills/Claude Code → ativa M1
- **Resultado:** —

#### 02 - Skills de processo vs domínio   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 397 linhas reais · fase: ausente · status: evergreen
- **Núcleo/gaps:** E4, E5, E7, E8, L2, M1
- **Score:** 6/11 (P1 N/A — sem código com caso-problema real)
- **Plano de execução:**
  - Criar `## Casos práticos` com ≥2 cenários de produção reais (skill de domínio ficando obsoleta, skill de processo rígida travando o agente) → ativa E4
  - Adicionar `## O que vem a seguir` com ponte narrativa + wikilink para "03 - Criar sua primeira skill" → ativa E5
  - Construir tabela PT↔EN de termos-chave (process skill, domain skill, hybrid skill, stale skill, skill owner) → ativa E7
  - Renomear/reformular `## Armadilhas` para `## Armadilhas comuns` convertendo os 4 itens em callouts `[!warning]` (mínimo 3) → ativa E8
  - Adicionar `## Fontes` com ≥1 URL externa verificável (ex. doc oficial de Agent Skills da Anthropic) → ativa L2
  - Pesquisar e embutir vídeo/podcast relevante sobre skills de agente como `[!tip]` → ativa M1
- **Resultado:** —

#### 03 - Criar sua primeira skill   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 404 linhas reais · fase: ausente · status: evergreen
- **Núcleo/gaps:** E4, E5, E7, E8, L2, M1
- **Score:** 6/12
- **Plano de execução:**
  - Adicionar `## Casos práticos` com ≥2 cenários de produção (pode reaproveitar/expandir "Variações") → ativa E4
  - Adicionar `## O que vem a seguir` com ponte narrativa + wikilink pra próxima nota do galho → ativa E5
  - Adicionar tabela PT↔EN de termos-chave da skill (name, description, frontmatter, etc.) → ativa E7
  - Renomear/reforçar `## Armadilhas` para `## Armadilhas comuns` e converter os 4 itens em ≥3 callouts `[!warning]` → ativa E8
  - Adicionar `## Fontes` com ≥1 URL externa verificável (docs oficiais de Claude Code Skills) → ativa L2
  - Adicionar `[!tip]` com link de vídeo/podcast sobre criação de skills → ativa M1
- **Resultado:** —

#### 04 - MCP overview   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 394 linhas reais · fase: ausente · status: evergreen
- **Núcleo/gaps:** E5, E7, E8, M1
- **Score:** 7/11 (P1 N/A — nota conceitual, exemplos são config/JSON, não caso-problema)
- **Plano de execução:**
  - Adicionar seção `## O que vem a seguir` com ponte narrativa até a nota 05 — → ativa E5
  - Converter os 4 itens de `## Armadilhas` em callouts `[!warning]` (já há ≥3 conteúdos prontos, só falta o formato) — → ativa E8
  - Adicionar tabela PT↔EN com os termos já usados na seção "Como explicar em inglês" (MCP server, tools/resources/prompts, transport) — → ativa E7
  - Pesquisar e embutir um `[!tip]` com vídeo/podcast real sobre MCP — → ativa M1
- **Resultado:** —

#### 05 - MCP servers essenciais   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 401 linhas reais · fase: ausente · status: evergreen
- **Núcleo/gaps:** E4, E5, E7, E8, M1
- **Score:** 7/12
- **Plano de execução:**
  - Adicionar `## Casos práticos` com ≥2 cenários de produção detalhados, reaproveitando/expandindo os "Exemplo de workflow" já existentes → ativa E4
  - Adicionar `## O que vem a seguir` com ponte narrativa e wikilink para `[[06 - Criar MCP server]]` → ativa E5
  - Converter a seção de inglês numa tabela PT↔EN de termos-chave → ativa E7
  - Reescrever `## Armadilhas` como `## Armadilhas comuns` com ≥3 callouts `[!warning]` (hoje é prosa em bold) → ativa E8
  - Pesquisar e embutir vídeo/podcast real sobre MCP servers (ex. demo de postgres/github/puppeteer MCP) como `[!tip]` → ativa M1
- **Resultado:** —

#### 06 - Criar MCP server   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 396 linhas reais · fase: ausente · status: evergreen
- **Núcleo/gaps:** E4, E5, E7, E8, L2, M1
- **Score:** 7/12
- **Plano de execução:**
  - Adicionar `## Casos práticos` com ≥2 cenários de produção (pode reaproveitar "Server com estado" e "Expondo resources" reestruturados) → ativa E4
  - Adicionar `## O que vem a seguir` com ponte narrativa (não só links) apontando para 07 - Compondo skills e MCP → ativa E5
  - Adicionar tabela PT↔EN com os termos já usados na seção de inglês (tool, resource, handler, transport, etc.) → ativa E7
  - Renomear `## Armadilhas` para `## Armadilhas comuns` e converter os 4 blocos em callouts `[!warning]` → ativa E8
  - Renomear `## Referências` para `## Fontes` (mantendo as URLs já existentes) → ativa L2
  - Pesquisar e embutir vídeo/podcast real sobre criar MCP server via `[!tip]` → ativa M1
- **Resultado:** —

#### 07 - Compondo skills e MCP   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 386 linhas reais · fase: ausente · status: evergreen
- **Núcleo/gaps:** E4, E5, E7, E8, L2, M1
- **Score:** 6/12
- **Plano de execução:**
  - Renomear/adicionar `## Casos práticos` cobrindo os 2+ cenários já existentes (Exemplo 1/2/3) → ativa E4
  - Adicionar `## O que vem a seguir` com ponte narrativa e wikilink pra "08 - Skills em time" → ativa E5
  - Adicionar tabela PT↔EN dos termos-chave (composição, orquestrador, skill de domínio/processo) → ativa E7
  - Converter os itens de "## Armadilhas" em ≥3 callouts `[!warning]` → ativa E8
  - Criar `## Fontes` com ≥1 URL externa verificável (ex.: docs oficiais Anthropic sobre skills/MCP) → ativa L2
  - Pesquisar e embutir `[!tip]` com vídeo/podcast sobre composição de agentes (skills+MCP) → ativa M1
- **Resultado:** —

#### 08 - Skills em time   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 394 linhas reais · fase: ausente · status: evergreen
- **Núcleo/gaps:** E4, E5, E7, E8, L2, M1
- **Score:** 6/12
- **Plano de execução:**
  - Adicionar `## Casos práticos` com ≥2 cenários de produção (equipe adotando/abandonando skill) → ativa E4
  - Adicionar `## O que vem a seguir` com ponte narrativa + wikilink pra próxima nota do galho → ativa E5
  - Adicionar tabela PT↔EN de termos-chave (skill, owner, stale, versioning) na seção de inglês → ativa E7
  - Renomear/reestruturar "Anti-padrões comuns em times" como `## Armadilhas comuns` com ≥3 callouts `[!warning]` → ativa E8
  - Criar `## Fontes` com ≥1 URL externa verificável (docs oficiais de skills/Claude Code ou artigo sobre manutenção de documentação viva) → ativa L2
  - Buscar e embutir vídeo/podcast relevante sobre manter skills/documentação de agentes atualizada via /adicionar-midia → ativa M1
- **Resultado:** —
