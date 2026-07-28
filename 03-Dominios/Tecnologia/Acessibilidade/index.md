---
title: "Acessibilidade (a11y)"
type: moc
publish: true
created: 2026-07-27
updated: 2026-07-27
status: growing
tags:
  - moc
  - acessibilidade
  - a11y
  - wcag
  - aria
aliases:
  - Acessibilidade
  - a11y
  - Web Accessibility
---

# Acessibilidade (a11y)

> [!abstract] TL;DR
> Acessibilidade não é um checklist que se passa no fim do sprint — é o **ofício** de construir interfaces que **qualquer pessoa consegue usar**, incluindo quem navega por teclado, leitor de tela, zoom, switch ou voz. Este domínio parte de onde o [[03-Dominios/Tecnologia/HTML/07 - Acessibilidade I - fundamentos WCAG e navegação por teclado|HTML/07]] e o [[03-Dominios/Tecnologia/HTML/08 - ARIA - roles, states, properties e live regions|HTML/08]] param — da teoria WCAG/ARIA isolada — para o ofício transversal de **construir, auditar, testar e sustentar** a11y num produto real.

Este domínio existe porque acessibilidade é tema de entrevista sênior por si só, e o vault só a tratava como **fase do HTML**. A aposta central: *semântica primeiro, ARIA por último, teste com gente de verdade sempre*. Antes de decorar atributos, você precisa saber **como um leitor de tela lê a página, o que a automação não pega, e como priorizar remediação** por severidade e esforço.

O domínio segue a **progressão do ofício** — *entender → construir → auditar → sustentar* — que minimiza sobreposição entre sub-galhos e leva do modelo mental à conformidade em produção.

---

## Sub-galhos

| # | Sub-galho | O quê | Fase |
|---|-----------|-------|------|
| 1 | [[03-Dominios/Tecnologia/Acessibilidade/Fundamentos e Modelo Mental/index\|SG1 — Fundamentos e Modelo Mental]] | espectro de deficiências, accessibility tree, leitores de tela, WCAG 2.2 pelo ofício, semântica antes de ARIA | Iniciado |
| 2 | [[03-Dominios/Tecnologia/Acessibilidade/Construir Acessível/index\|SG2 — Construir Acessível]] | gestão de foco em SPAs, formulários, padrões WAI-ARIA APG, a11y em React, cor/contraste, mídia e movimento | Adepto |
| 3 | [[03-Dominios/Tecnologia/Acessibilidade/Auditar e Testar/index\|SG3 — Auditar e Testar]] | axe/Lighthouse/WAVE, testes de a11y no código, auditoria manual com teclado e leitor de tela, conduzir auditoria | Adepto/Magus |
| 4 | [[03-Dominios/Tecnologia/Acessibilidade/Sustentar e Conformidade/index\|SG4 — Sustentar e Conformidade]] | a11y no CI/design system, cenário legal (ADA/EAA/EN 301 549), VPAT/ACR, a11y em entrevista | Magus |
| — | [[03-Dominios/Tecnologia/Acessibilidade/21 - Capstone - auditar e remediar um produto do zero\|Capstone — auditar e remediar um produto do zero]] | audita → prioriza → remedia → documenta; costura os 4 sub-galhos | Magus |

> **Estado (2026-07-28):** **domínio 100% COMPLETO — 21/21 notas escritas + enriquecidas** (4 sub-galhos + capstone, padrão capítulo, 3 fases). Cada nota traz vídeo YouTube verificado (legenda via yt-dlp), seção "Como explicar em inglês" + tabela PT↔EN, armadilhas `[!warning]`, casos práticos e diagramas Mermaid. Ver [[00-Meta/specs/2026-07-27-dominio-acessibilidade-design|design do domínio]], o [[00-Meta/specs/2026-07-27-dominio-acessibilidade-plano|plano]] e o [[03-Dominios/Tecnologia/Acessibilidade/roadmap|roadmap]].

---

## Fronteiras — a11y que já mora em outras trilhas

Este domínio é a **lente do ofício**; ele **linka** as notas abaixo como reforço, **nunca as reescreve** (redundância entre notas = reforço). A teoria-base de WCAG e ARIA vive no HTML; aqui você aprende a *aplicá-la, auditá-la e sustentá-la*.

- [[03-Dominios/Tecnologia/HTML/07 - Acessibilidade I - fundamentos WCAG e navegação por teclado|HTML 07 — Fundamentos WCAG e teclado]] — POUR, `tabindex`, `:focus-visible`, contraste, alt text. **Porta de entrada.**
- [[03-Dominios/Tecnologia/HTML/08 - ARIA - roles, states, properties e live regions|HTML 08 — ARIA]] — roles, states, properties, live regions, anti-padrões. **Porta de entrada.**
- [[03-Dominios/Tecnologia/Testes JS/14 - Playwright além do básico|Testes JS 14 — Playwright]] — testes E2E que tocam a11y.
- [[03-Dominios/Tecnologia/React/index|React — Ecossistema]] — component libraries headless (Radix, React Aria) que resolvem a11y de widgets.
- [[03-Dominios/Tecnologia/Web Performance/index|Web Performance]] — `prefers-reduced-motion` e rendering tangenciam a11y.

---

## Veja também

- [[00-Meta/Roadmap|Roadmap de Trilhas]] — Acessibilidade sai de 🚫 (Tier 1, construção nova) para domínio próprio.
- [[03-Dominios/Tecnologia/HTML/index|HTML]] — onde a a11y começa como fase.
- [[03-Dominios/Carreira/Entrevistas/index|Entrevistas]] — a11y como diferencial em entrevista sênior.
