---
title: "Plano de Implementação — Galho React Design Patterns"
type: spec
created: 2026-06-26
updated: 2026-06-26
status: done
tags:
  - spec
  - plano
  - react
  - design-patterns
aliases:
  - Implementação React Design Patterns
---

# Plano de Implementação — Galho React Design Patterns

> **Para executores:** implementa o spec [[00-Meta/specs/2026-06-26-galho-react-design-patterns-plan|Plano — Galho React Design Patterns]]. Execução **subagente-por-nota**, em ondas por fase, gate de qualidade entre fases. Passos com checkbox (`- [ ]`).

**Objetivo:** escrever o galho **React Design Patterns** (12 notas, 3 fases, TS-first, catálogo auto-contido) em `03-Dominios/Tecnologia/React/Design Patterns/`.

**Abordagem:** cada nota é escrita por um subagente via `/escrever-nota`, pesquisando as fontes-base do spec + WebSearch (estado 2026). Exemplos `.tsx`. Commit por sub-lote; gate `/verificar-nota` por nota; `/verificar-wikilinks` por fase.

**Stack/convenções:** Obsidian + Quartz; React 19 + TypeScript; padrão capítulo; fases Iniciado/Adepto/Magus; PT-BR + "Como explicar em inglês".

## Global Constraints (valem para TODA nota)

- **Catálogo auto-contido** — cada padrão é entrada COMPLETA (intenção → mecanismo → exemplo `.tsx` cheio com tipagem inline → trade-offs/quando usar → quais libs usam). PODE repetir conteúdo de React core / TS-com-React, mas sob a ótica do padrão; linkar a nota canônica para aprofundamento.
- **Escrita do ZERO com pesquisa** — consultar as fontes-base do spec (patterns.dev, react-in-patterns/Krasimir, GreatFrontend, LogRocket, perssondennis, refine, etc.) + WebSearch 2026. Citar em `## Referências`.
- **TS-first** — exemplos `.tsx` com tipos idiomáticos; tipagem do padrão mostrada aqui; nuances profundas → linkar [[03-Dominios/Tecnologia/React/TypeScript com React/index|TypeScript com React]].
- **Padrão capítulo** — problema-primeiro; registro Feynman; exemplos trabalhados; Mermaid onde agrega; "Como explicar em inglês" + tabela PT↔EN; "Armadilhas comuns" (≥3 `[!warning]`); TL;DR `[!abstract]`; resumo em 1 linha.
- **Fase calibra a régua** — Iniciado: fundamentos de padrões; Adepto: padrões do dia a dia; Magus: avançados/de biblioteca.
- **Frontmatter** — `type: concept`, `fase: <iniciado|adepto|magus>`, `created: 2026-06-26`, `updated: 2026-06-26`, `status: seedling`, `publish: true`, `tags` (incluindo `react`, `design-patterns`, `entrevista`, a fase).
- **Seams (linkar E reforçar):** tipagem profunda → TS-com-React 14/13; composição/arquitetura → React core 08/24; mecânica de hooks → React core 14/09; polymorphic → TS-com-React 13.
- **Wikilinks só para alvos confirmados** (`ls` antes; sem títulos inventados — atenção a caixa). Verbetes no [[03-Dominios/Tecnologia/React/Dicionário de React|Dicionário de React]] (existe) conforme surgirem.
- **Anti-fabricação** ([[feedback_no_fabrication]]).
- **Numeração** conforme roster do spec (`01 - …` a `12 - …`).

## Estrutura de arquivos

Pasta-alvo: `03-Dominios/Tecnologia/React/Design Patterns/`

- **Criar (12):** `01 - Padrões no React e a evolução.md` … `12 - Capstone ...md` (títulos do roster do spec)
- **Criar (1):** `index.md` do galho (MOC das 3 fases) — Wave 4
- **Modificar (teardown):** `03-Dominios/Tecnologia/React/index.md` (marcar galho Design Patterns)
- **Manter:** `Dicionário de React.md` (enriquecer com verbetes), demais galhos

---

## Procedimento por nota (template — cada uma das 12)

Um subagente por nota:

- [ ] **1. Pesquisar** o padrão (fontes-base do spec + WebSearch 2026): intenção, mecanismo, quando usar/evitar, quais libs usam, estado em 2026.
- [ ] **2. Escrever** via `/escrever-nota` no path exato, fase indicada, exemplos `.tsx`, entrada COMPLETA de catálogo (não só "veja a outra nota").
- [ ] **3. Auto-gate** `/verificar-nota`; corrigir o que reprovar.
- [ ] **4. Reportar** ao orquestrador: padrão coberto, fontes, wikilinks, linhas, score.

Orquestrador **commita por sub-lote** (paths explícitos) e roda `/verificar-wikilinks` ao fim de cada fase.

---

## Wave 1 — Iniciado (notas 01–03)

- [ ] **01 - Padrões no React e a evolução** — o que é um pattern no React; história HOC → render props → custom hooks (por que hooks venceram); como ler uma entrada do catálogo
- [ ] **02 - Container vs Presentational** — smart/dumb; o clássico e por que hooks reescreveram a conversa
- [ ] **03 - Controlled vs Uncontrolled** — fonte da verdade; `value`+`onChange` vs `defaultValue`+ref; suportar ambos
- [ ] **Gate Iniciado:** commit por sub-lote; `/verificar-wikilinks 03-Dominios/Tecnologia/React/Design Patterns`; corrigir quebras reais.

## Wave 2 — Adepto (notas 04–09)

- [ ] **04 - Custom hooks como padrão de reuso de lógica** — substitui HOC/render props; composição de hooks
- [ ] **05 - Provider pattern** — context + provider; provider + reducer (mini-Redux); context module functions; custom hook com guard
- [ ] **06 - Composição: slots, layout e children-as-API** — children como slot; múltiplos slots; layout components; composição sobre configuração
- [ ] **07 - Compound components** — `<Select><Select.Option/></Select>`; context interno; flexibilidade vs acoplamento
- [ ] **08 - Render props e function-as-child** — função que renderiza; quando ainda vale em 2026
- [ ] **09 - Higher-Order Components (HOC)** — legado; `withX`; composição de HOCs; wrapper hell; onde ainda aparece
- [ ] **Gate Adepto:** commit por sub-lote; `/verificar-wikilinks`; corrigir quebras reais.

## Wave 3 — Magus (notas 10–12)

- [ ] **10 - State reducer e prop getters** — inversão de controle; usuário customiza comportamento interno; padrão downshift/Kent C. Dodds
- [ ] **11 - Headless components e headless hooks** — lógica sem apresentação; Radix, TanStack, Headless UI; comportamento vs estilo
- [ ] **12 - Capstone — escolher o padrão certo e em entrevista** — decision tree, anti-patterns, mapa de revisão, "como explicar em inglês" (costurar wikilinks pras 11 irmãs — confirmar via `ls`)
- [ ] **Gate Magus:** commit por sub-lote; `/verificar-wikilinks`; corrigir quebras reais.

## Wave 4 — Teardown e integração

- [ ] **4.1 Criar `index.md`** do galho `Design Patterns/` — MOC das 3 fases (links pras 12), com seam pros galhos vizinhos (React core, TS-com-React).
- [ ] **4.2 Atualizar `React/index.md`** — galho React Design Patterns de ⬜ planejado → 🟩 (linkar o índice).
- [ ] **4.3 `/verificar-wikilinks 03-Dominios/Tecnologia/React/Design Patterns`** — 0 quebras reais.
- [ ] **4.4 Atualizar [[00-Meta/Roadmap|Roadmap]]:** domínio React — galho Design Patterns ✅ (2/6).
- [ ] **4.5 (Opcional) Ciclo de qualidade:** `/plantar-duvidas` → `/colher-duvidas`; `/enriquecer-nota`.
- [ ] **4.6 Commit final** + `status: done` neste plano.

---

## Self-review (cobertura do spec)

- Roster 12/12 → Waves 1–3 item a item ✓
- Catálogo auto-contido + TS-first + fontes-base → Global Constraints + procedimento por nota ✓
- Seams (linkar E reforçar) → Global Constraints ✓
- Dicionário de React (existe) → verbetes no procedimento ✓
- Índice do galho + atualizar React/index + Roadmap → Wave 4 ✓
- Fora de escopo (Next/Ecossistema/tipagem profunda) → respeitado pelos seams ✓
