---
title: "Domínio Acessibilidade (a11y) — design"
created: 2026-07-27
type: design
status: draft
publish: false
tags:
  - meta
  - design
  - acessibilidade
  - a11y
  - wcag
  - aria
---

# Domínio Acessibilidade (a11y) — design

## Contexto

Acessibilidade é o **último item de construção nova (🚫 Tier 1)** do
[[00-Meta/Roadmap|Roadmap de Trilhas]]. Os outros dois buracos reais do Tier 1 já
foram fechados (Go ✅ 2026-07-18, Cloud ✅ 2026-07-24). O Roadmap registra o tema em
três lugares como cobertura autônoma pendente: *"entra como fase do HTML, mas é tema
de entrevista por si só e merece foco próprio"*.

Hoje a **base conceitual** de a11y já existe, mas confinada ao domínio HTML:

- `Tecnologia/HTML/07 - Acessibilidade I - fundamentos WCAG e navegação por teclado` (412 l — POUR, teclado, `tabindex`, `:focus-visible`, contraste, alt text)
- `Tecnologia/HTML/08 - ARIA - roles, states, properties e live regions` (564 l — ARIA completo, anti-padrões, dialog/tabs)
- Menções esparsas: `Testes JS/14 - Playwright além do básico`, `React/Ecossistema` (UI libs), `React/Next.js`

**Princípio-guia:** este domínio **não reescreve** HTML/07 e HTML/08. Eles são a
**porta de entrada** (teoria WCAG/ARIA isolada). O novo domínio parte *de onde o HTML
para*: da teoria para o **ofício transversal** de construir, auditar, testar e
sustentar a11y num produto real. Notas existentes são **linkadas como reforço**
(redundância entre notas = reforço, nunca deduplicar; ver
[[feedback_redundancia_entre_notas]]).

## Decisões de design

Tomadas no brainstorming de 2026-07-27:

1. **Forma:** domínio próprio multi-galho (`Tecnologia/Acessibilidade/`), no molde de
   Web Performance — não um galho único nem galho dentro de outro domínio. Justificativa:
   tema grande, cai em entrevista sênior por si só, e o Roadmap o trata como cobertura
   autônoma. Mora em `Tecnologia/` (lado stack), não em `Engenharia/`. (Confirmado com o usuário.)
2. **Decomposição:** 4 sub-galhos pela **progressão do ofício** — *entender → construir →
   auditar → sustentar* — que minimiza sobreposição entre galhos e espelha o modelo de
   Web Performance. (Alternativa rejeitada: organização por princípio POUR — fragmenta o
   ofício, espalha ferramentas/testes e duplica mais o HTML/07.)
3. **Escala:** ~20 notas + 1 capstone (21 total). Enxuta de propósito: WCAG/ARIA-base
   vivem no HTML e são linkados, não recopiados.
4. **Ritmo:** **galho a galho, ponta a ponta.** Fecha-se SG1 (semear + enriquecer até ✅)
   antes de começar SG2. Mantém o contexto leve por sessão.
5. **Convenções do vault aplicadas:** notas atômicas em 3 fases (Iniciado/Adepto/Magus) com
   `fase:` no frontmatter; padrão capítulo de livro; Mermaid; `roadmap.md` do domínio
   (galho-pai) + `roadmap.md` por sub-galho; MOC (`index.md`) agrupado por fase.

## Arquitetura do domínio

**Pasta:** `03-Dominios/Tecnologia/Acessibilidade/`

- **`index.md`** (`type: moc`): TL;DR do domínio + tabela dos 4 sub-galhos (progressão
  *entender → construir → auditar → sustentar*) + roster agrupado por fase + fronteiras.
- **`roadmap.md`** (galho-pai): mapa de estado dos 4 sub-galhos, recursivo (raiz → sub-galho
  → nota), no template `Template - Roadmap`.
- **4 sub-pastas**, cada uma com seu `index` e `roadmap.md`.

## Roster (~20 notas + capstone)

### SG1 — Fundamentos e modelo mental · *Iniciado*
1. **A11y é ofício, não checklist** — custo humano/negócio, espectro de deficiências (permanente/temporária/situacional), o mito do "só usuário cego"
2. **O accessibility tree** — do DOM à árvore, computação de accessible name/role/value, como o browser expõe a UI às ATs
3. **Leitores de tela e tecnologias assistivas na prática** — NVDA/JAWS/VoiceOver/TalkBack, modos de navegação, zoom, switch, voice control
4. **WCAG 2.2 pelo ofício** — POUR revisitado para *priorizar/aplicar* (não recopiar HTML/07), níveis A/AA/AAA, o que a 2.2 mudou, WCAG 3.0 no horizonte
5. **Semântica primeiro, ARIA por último** — "no ARIA is better than bad ARIA", quando NÃO usar ARIA (ponte pro HTML/08)

### SG2 — Construir acessível · *Adepto*
6. **Gestão de foco em SPAs** — foco em navegação client-side, focus trap, restauração de foco, roving tabindex
7. **Formulários acessíveis de verdade** — labels, erros acessíveis, `aria-describedby`, grupos/fieldset, `autocomplete`
8. **Padrões WAI-ARIA APG I** — disclosure, accordion, tabs, modal dialog
9. **Padrões WAI-ARIA APG II** — combobox/autocomplete, menu/menubar, listbox, tree, grid
10. **A11y em React e component libraries** — headless libs (Radix, React Aria), o que o framework (não) resolve, testar componentes
11. **Cor, contraste e visual acessível** — contraste na prática, não depender só de cor, dark mode, foco visível (SC 2.4.11)
12. **Mídia e movimento** — captions/transcrições/audio description, `prefers-reduced-motion`, animações, flashing (SC 2.3.1)

### SG3 — Auditar e testar · *Adepto/Magus*
13. **Auditoria automatizada** — axe, Lighthouse, WAVE; o que cada um pega e o teto de ~30–40% da automação
14. **Testes de a11y no código** — jest/vitest-axe, Testing Library queries por role, Playwright a11y (ponte pra Testes JS/14)
15. **Auditoria manual** — teclado, screen reader walkthrough, zoom 400%, o roteiro do que a automação não pega
16. **Conduzir uma auditoria completa** — do escopo ao relatório priorizado por severidade/esforço

### SG4 — Sustentar e o lado humano/legal · *Magus*
17. **A11y no ciclo de dev** — gates de CI/CD, design system acessível, a11y no Definition of Done
18. **Cenário legal e normativo** — ADA, Section 508, EN 301 549, EAA (jun/2025), WCAG como referência jurídica
19. **VPAT/ACR e comunicar conformidade** — accessibility statement, como ler/produzir o documento
20. **A11y em entrevista** — falar de a11y como sênior, red flags, o que demonstrar

### Capstone
21. **Auditar e remediar um produto do zero** — audita → prioriza por severidade/esforço → remedia → documenta

## Fronteiras (linkadas, não duplicadas)

- **Porta de entrada:** HTML/07 (WCAG/teclado) e HTML/08 (ARIA) — teoria-base. Callout no
  `HTML/index` aponta pra cá.
- **Pontos de contato:** `Testes JS/14` (Playwright a11y), `React/Ecossistema` (UI libs
  headless), `Web Performance` (motion/rendering tangenciam a11y).
- **Regra:** cada nova nota linka a fronteira em vez de reexplicá-la.

## Convenções e qualidade

- Padrão capítulo de livro (pega o leitor pela mão), registro Feynman no enriquecimento.
- Notas substanciais com diagramas Mermaid; piso de linhas por fase onde o galho adota fases.
- Núcleo mínimo obrigatório (TL;DR · abertura-problema · corpo-mecanismo · O que vem a
  seguir · Fontes · frontmatter) + opcionais por gate de score.
- Cada sub-galho recebe `roadmap.md` antes do enriquecimento (pré-condição da
  `enriquecer-galho`).

## Fora de escopo

- Reescrever WCAG/ARIA-base (vive no HTML).
- Design de UI genérico (vive em CSS/React).
- Acessibilidade nativa mobile (iOS/Android) além de menção — foco é web.

## Ordem de execução

Galho a galho, ponta a ponta: **SG1 → SG2 → SG3 → SG4 → capstone**. Ao fechar o domínio,
atualizar o [[00-Meta/Roadmap|Roadmap]] (Tier 1 → ✅, marcando a11y como cobertura fechada).
