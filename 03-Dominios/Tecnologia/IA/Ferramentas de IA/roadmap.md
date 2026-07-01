---
title: "Roadmap — Ferramentas de IA"
created: 2026-07-01
type: meta
publish: false
tags:
  - meta
  - roadmap
---

# Roadmap — Ferramentas de IA

Diagnóstico migrado de guia/roadmap - ia.md (30/06). Cada entrada tem estado de enriquecimento, score, classificação de custo e plano de execução acionável.

**Galho:** `03-Dominios/Tecnologia/IA/Ferramentas de IA`
**Diagnóstico:** 2026-06-28 (migrado 2026-07-01)
**Última execução:** —

## Régua de análise

Checklist `verificar-nota` — 12 itens (isenções por fase/tipo/broto aplicadas por nota):

| Grupo | Itens |
|-------|-------|
| ESTRUTURA | E1 TL;DR · E2 Abertura-problema · E3 Mermaid · E4 Casos práticos · E5 O que vem a seguir · E6 Inglês · E7 Tabela PT↔EN · E8 Armadilhas [!warning] |
| PROFUNDIDADE | P1 Código-com-falha · P2 Mecanismo explicado |
| LINKS | L1 Wikilink cross-galho · L2 Referência externa (URL) |
| MÍDIA | M1 Vídeo/podcast embutido |

**Esquema de `fase:` detectado:** COM fase (Iniciado) — notas-referência por ferramenta, não trilha sequencial; piso OK (626–910 linhas)
**Piso de linhas:** aplicável — Iniciado ≥300 (todas as notas excedem largamente)

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 5 |
| ⬜ pendente | 5 |
| ➖ não precisa | 0 |
| ✅ feita | 0 |
| 🔄 em andamento | 0 |
| % concluído | 0% |

---

## Notas

#### Claude (nota-referência)   [mecânico]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 910 linhas · fase: Iniciado · status: evergreen
- **Núcleo/gaps:** E1, E2, E3, P1
- **Score:** 8/12
- **Plano de execução:**
  - Adicionar `> [!abstract]` TL;DR com ≥3 linhas logo após o título → resolve E1
  - Reescrever abertura de "Claude é uma das três famílias…" para partir de problema/cenário ("Quando o time decide adotar um LLM de produção, a decisão de qual usar...") → resolve E2
  - Opcional: adicionar diagrama Mermaid do ecossistema (5 superfícies) ou fluxo de tiering (Haiku→Sonnet→Opus) → resolve E3
  - Unificar seção "Armadilhas comuns": manter callouts `[!warning]`, remover lista numerada que duplica os mesmos pontos
- **Resultado:** —

#### Codex (nota-referência)   [mecânico]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 627 linhas · fase: Iniciado · status: evergreen
- **Núcleo/gaps:** E1, E3, P1
- **Score:** 9/12
- **Plano de execução:**
  - Converter blockquote de abertura (linha 20) em `[!abstract]` com ≥3 linhas → resolve E1
  - Converter diagrama de arquitetura ASCII (linhas 66-93) para Mermaid `flowchart TD` → resolve E3
  - Verificar e corrigir URLs de docs (`developers.openai.com/codex` e `/codex/skills/`) — OpenAI migrou para `platform.openai.com`; links provavelmente mortos
  - Unificar "Armadilhas comuns": manter callouts `[!warning]`, remover lista numerada redundante
- **Resultado:** —

#### Comparativo de LLMs (nota-referência)   [mecânico]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 729 linhas · fase: Iniciado · status: evergreen
- **Núcleo/gaps:** E1, E3, P1
- **Score:** 9/12
- **Plano de execução:**
  - Adicionar TL;DR `> [!abstract]` ≥3 linhas logo após o H1 → resolve E1
  - Converter os 4 fluxogramas em blocos ` ```text ``` ` (Framework de decisão, Padrões 1-4) para Mermaid `flowchart TD` → resolve E3
  - Unificar "Armadilhas comuns": manter callouts `[!warning]`, remover lista numerada redundante
- **Resultado:** —

#### Gemini (nota-referência)   [mecânico]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 636 linhas · fase: Iniciado · status: evergreen
- **Núcleo/gaps:** E1, E3, P1
- **Score:** 9/12
- **Plano de execução:**
  - Converter blockquote inicial em `> [!abstract]` com ≥3 linhas sintetizando para que serve, diferenciais e quando usar → resolve E1
  - Adicionar diagrama Mermaid (ex: `flowchart TD` de decisão "quando usar qual modelo" ou "Gemini CLI vs Vertex AI vs API direta") → resolve E3
  - Remover duplicação entre os 3 callouts `[!warning]` e a lista numerada em "Armadilhas comuns" — manter callouts, remover lista
- **Resultado:** —

#### GitHub Copilot (nota-referência)   [mecânico]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 706 linhas · fase: Iniciado · status: evergreen
- **Núcleo/gaps:** E1, E3, P1
- **Score:** 9/12
- **Plano de execução:**
  - Adicionar `> [!abstract]` TL;DR com ≥3 linhas logo após o título → resolve E1
  - Adicionar diagrama Mermaid (sugestão: fluxo dos modos de operação Completion → Chat → Edit → Agent → Workspace, ou pipeline de contexto do IDE) → resolve E3
  - Remover lista de 10 itens em "Armadilhas comuns" que duplica os 3 callouts `[!warning]` existentes — manter callouts
- **Resultado:** —
