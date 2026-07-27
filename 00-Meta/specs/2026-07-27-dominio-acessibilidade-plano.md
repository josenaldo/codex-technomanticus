---
title: "Domínio Acessibilidade (a11y) — plano de implementação"
created: 2026-07-27
type: plan
status: draft
publish: false
tags:
  - meta
  - plan
  - acessibilidade
  - a11y
---

# Domínio Acessibilidade (a11y) — plano de implementação

> **Base:** [[2026-07-27-dominio-acessibilidade-design|design do domínio]].
> **Ritmo:** galho a galho, ponta a ponta. Fecha SG1 (semear + verificar + enriquecer)
> antes de abrir SG2.

**Goal:** construir o domínio `Tecnologia/Acessibilidade` (~20 notas + capstone, 4
sub-galhos, 3 fases), fechando o último buraco de construção nova do Tier 1 do Roadmap.

**Arquitetura:** domínio multi-galho no molde de Web Performance. Progressão *entender →
construir → auditar → sustentar*. HTML/07 e HTML/08 são porta de entrada linkada, não
recopiada.

**Workflow do vault (substitui o ciclo TDD):**
- **Semear nota** → skill `/escrever-nota` (padrão capítulo, núcleo mínimo + opcionais por tema).
- **Gate de qualidade** → skill `/verificar-nota` (checklist ESTRUTURA/PROFUNDIDADE/TAMANHO/LINKS/MÍDIA). É o "teste" de cada nota.
- **Roadmap do galho** → skill `/diagnosticar-galho` (gera `roadmap.md`, pré-condição do enriquecimento).
- **Enriquecer** → skill `/enriquecer-galho` (nota a nota, governança de tokens, roda em Opus/opusplan).

## Global Constraints

- Pasta raiz: `03-Dominios/Tecnologia/Acessibilidade/` (sem acento no path "Dominios").
- Notas atômicas em 3 fases; `fase:` no frontmatter (Iniciado/Adepto/Magus por sub-galho conforme roster).
- Padrão capítulo de livro + registro Feynman no enriquecimento; Mermaid onde ajudar.
- Núcleo mínimo obrigatório: TL;DR · abertura-problema · corpo-mecanismo · "O que vem a seguir" · Fontes · frontmatter.
- **Não recopiar** WCAG/ARIA-base do HTML/07-08 — linkar como fronteira.
- **Não inventar dados do usuário** (projetos/clientes/casos). Exemplos genéricos ou marcados.
- Commits: paths explícitos, `git diff --cached` antes; sem Co-Authored-By Claude.
- Cada nota nova referencia a fronteira em vez de reexplicá-la.

---

## Task 0: Scaffold do domínio

**Files:**
- Create: `03-Dominios/Tecnologia/Acessibilidade/index.md` (`type: moc`)
- Create: `03-Dominios/Tecnologia/Acessibilidade/roadmap.md` (galho-pai, `Template - Roadmap`)
- Create: as 4 sub-pastas com `index.md` cada (SG1–SG4)
- Modify: `03-Dominios/Tecnologia/HTML/index.md` (callout apontando pro novo domínio)

**Produces:** estrutura navegável do domínio + MOC agrupado por fase + entrada no Roadmap.

- [ ] **Passo 1:** criar `index.md` do domínio (TL;DR + tabela dos 4 sub-galhos com a
  progressão *entender→construir→auditar→sustentar* + roster por fase + seção Fronteiras).
- [ ] **Passo 2:** criar `roadmap.md` do galho-pai (mapa de estado dos 4 sub-galhos, recursivo).
- [ ] **Passo 3:** criar as 4 sub-pastas + `index.md` de cada uma (stub MOC do sub-galho).
- [ ] **Passo 4:** adicionar callout `[!info]` no `HTML/index.md` apontando pra
  `Acessibilidade` como aprofundamento de HTML/07-08.
- [ ] **Passo 5:** `git add` dos paths explícitos + commit
  (`docs(a11y): scaffold do domínio Acessibilidade — index, roadmap, 4 sub-galhos`).

---

## Task 1: SG1 — Fundamentos e modelo mental (Iniciado, 5 notas)

**Files (Create):**
- `.../Acessibilidade/Fundamentos/01 - A11y é ofício, não checklist.md`
- `.../Fundamentos/02 - O accessibility tree.md`
- `.../Fundamentos/03 - Leitores de tela e tecnologias assistivas na prática.md`
- `.../Fundamentos/04 - WCAG 2.2 pelo ofício.md`
- `.../Fundamentos/05 - Semântica primeiro, ARIA por último.md`

**Fronteiras a linkar:** HTML/07 (POUR/teclado) na nota 04; HTML/08 (ARIA) na nota 05.

Para **cada** nota (01→05):
- [ ] **Passo A:** semear com `/escrever-nota` (`fase: Iniciado`, tema da nota, linkar fronteira).
- [ ] **Passo B:** gate com `/verificar-nota`; corrigir o que reprovar.
- [ ] **Passo C:** commit com path explícito.

Ao fechar as 5:
- [ ] **Passo D:** `/diagnosticar-galho Fundamentos` → gera `roadmap.md` do sub-galho.
- [ ] **Passo E:** `/enriquecer-galho Fundamentos` até ✅ (parada a cada 15 notas / governança ccusage).
- [ ] **Passo F:** atualizar `roadmap.md` do galho-pai (SG1 → ✅) + commit.

---

## Task 2: SG2 — Construir acessível (Adepto, 7 notas)

**Files (Create):** `.../Acessibilidade/Construir/06..12 - <título>.md`
06 Gestão de foco em SPAs · 07 Formulários acessíveis · 08 WAI-ARIA APG I ·
09 WAI-ARIA APG II · 10 A11y em React e component libraries · 11 Cor e contraste ·
12 Mídia e movimento.

**Fronteiras:** `React/Ecossistema` (UI libs) na nota 10; HTML/08 (widgets) nas 08-09.

- [ ] Para cada nota 06→12: `/escrever-nota` (`fase: Adepto`) → `/verificar-nota` → commit.
- [ ] `/diagnosticar-galho Construir` → `roadmap.md`.
- [ ] `/enriquecer-galho Construir` até ✅.
- [ ] Atualizar roadmap do galho-pai (SG2 → ✅) + commit.

---

## Task 3: SG3 — Auditar e testar (Adepto/Magus, 4 notas)

**Files (Create):** `.../Acessibilidade/Auditar/13..16 - <título>.md`
13 Auditoria automatizada · 14 Testes de a11y no código · 15 Auditoria manual ·
16 Conduzir uma auditoria completa.

**Fronteiras:** `Testes JS/14` (Playwright) na nota 14.

- [ ] Para cada nota 13→16: `/escrever-nota` (13-14 `Adepto`, 15-16 `Magus`) → `/verificar-nota` → commit.
- [ ] `/diagnosticar-galho Auditar` → `roadmap.md`.
- [ ] `/enriquecer-galho Auditar` até ✅.
- [ ] Atualizar roadmap do galho-pai (SG3 → ✅) + commit.

---

## Task 4: SG4 — Sustentar e o lado humano/legal (Magus, 4 notas)

**Files (Create):** `.../Acessibilidade/Sustentar/17..20 - <título>.md`
17 A11y no ciclo de dev · 18 Cenário legal e normativo · 19 VPAT/ACR e conformidade ·
20 A11y em entrevista.

**Atenção à caducidade:** nota 18 cita EAA (jun/2025), EN 301 549, ADA — marcar `[!info]` de
data e verificar vigência na escrita.

- [ ] Para cada nota 17→20: `/escrever-nota` (`fase: Magus`) → `/verificar-nota` → commit.
- [ ] `/diagnosticar-galho Sustentar` → `roadmap.md`.
- [ ] `/enriquecer-galho Sustentar` até ✅.
- [ ] Atualizar roadmap do galho-pai (SG4 → ✅) + commit.

---

## Task 5: Capstone + fechamento do domínio

**Files:**
- Create: `.../Acessibilidade/21 - Capstone - auditar e remediar um produto do zero.md` (`fase: Magus`)
- Modify: `00-Meta/Roadmap.md` (Tier 1: a11y → ✅; "Coberturas ausentes" → fechada)
- Modify: `.../Acessibilidade/index.md` e `roadmap.md` (estado final do domínio)

- [ ] **Passo 1:** semear o capstone (audita → prioriza severidade/esforço → remedia →
  documenta; costura os 4 sub-galhos). `/escrever-nota` → `/verificar-nota` → commit.
- [ ] **Passo 2:** enriquecer o capstone se o gate pedir.
- [ ] **Passo 3:** atualizar `00-Meta/Roadmap.md` — marcar a11y ✅, remover do Tier 1 de
  construção nova, registrar contagem final de notas e data.
- [ ] **Passo 4:** atualizar memória (`project_*` de Acessibilidade + linha no `MEMORY.md`).
- [ ] **Passo 5:** commit de fechamento (`docs(a11y): domínio Acessibilidade COMPLETO — Tier 1 fechado`).

---

## Self-review (cobertura da spec)

- Todos os 4 sub-galhos + capstone da spec têm task (Task 1–5). ✓
- Scaffold (index/roadmap/sub-pastas/callout HTML) coberto em Task 0. ✓
- Fronteiras (HTML/07-08, Testes JS/14, React/Ecossistema) linkadas nas notas certas. ✓
- Fora de escopo (mobile nativo, UI genérica, reescrever WCAG-base) respeitado — nenhuma task o viola. ✓
- Caducidade legal (SG4/18) sinalizada. ✓
