---
title: "Ferramentas de Design"
type: moc
publish: true
created: 2026-07-28
updated: 2026-07-29
status: seedling
tags:
  - moc
  - ux
  - design
  - ferramentas
aliases:
  - Ferramentas de Design
  - Design Tooling
---

# Ferramentas de Design

> [!abstract] TL;DR
> A metade **volátil e concreta** do domínio de UX: as ferramentas que um engenheiro full-cycle usa de fato — Figma no que toca o código, geradores de UI por IA, protótipo em código, e o pipeline de tokens até o CSS. O ofício durável fica em [[03-Dominios/Engenharia/UX/index|Engenharia/UX]]; aqui é a implementação que envelhece.

Galho único, sem sub-pastas — 9 notas em sequência, sem fases (o eixo aqui não é "iniciado → magus", é "o que existe hoje e para que serve").

> [!warning] Galho perecível — revalidar a cada ciclo
> Este é o galho **mais perecível** de todo o domínio de UX: nomes de produto, features e posicionamento de ferramentas de IA generativa mudam em meses, não anos. Por isso ele é escrito **por último** na ordem de execução — quanto mais tarde, mais tempo de validade tem. Ao revisitar o domínio, **revalidar cada nota desta pasta antes de confiar nela** (produto ainda existe? preço/plano mudou? feature foi descontinuada?).

---

## Notas planejadas (9)

1. Figma para o engenheiro — Dev Mode, variables/modes, auto layout; o que é território de designer profissional e dá para ignorar
2. Figma MCP Server + Code Connect — contexto de design estruturado para o agente, em vez de screenshot
3. Claude Design e o handoff bundle — research preview da Anthropic Labs; linka a skill `handoff-design` em vez de duplicá-la
4. Geradores de UI por IA — v0, Lovable, Bolt, Subframe: onde ajudam, onde produzem lixo, como avaliar a saída
5. Estética genérica de IA e como escapar — o fingerprint reconhecível e a causa raiz
6. Protótipo em código — quando o componente real é o protótipo mais barato
7. Excalidraw e tldraw — baixa fidelidade, e tldraw como SDK embutível
8. Pipeline de tokens — Figma Variables → Style Dictionary → CSS custom properties, com Git como fonte de verdade
9. Loop visual com Playwright MCP e visual regression — accessibility tree como feedback estruturado

> **Estado (2026-07-29):** galho fechado. 9/9 escritas, mídia verificada em todas (0
> buracos de M1), diagnosticado e sem gaps de núcleo. Ver [[00-Meta/specs/2026-07-28-dominio-ux-design|design do domínio]] e o [[03-Dominios/Tecnologia/Ferramentas de Design/roadmap|roadmap]] (inclui callout de caducidade com o que já mudou desde a pesquisa).

---

## Fronteiras (linkar, nunca reescrever)

- [[03-Dominios/Tecnologia/IA/Claude Code/index|Tecnologia/IA/Claude Code]] + skill `handoff-design` — Claude Design é produto; a nota 3 linka a skill em vez de duplicá-la.
- [[03-Dominios/Tecnologia/Tooling e Build/index|Tecnologia/Tooling e Build]] — pipeline de build; Style Dictionary é candidato natural a nota **lá**, não aqui.
- [[03-Dominios/Tecnologia/Testes JS/14 - Playwright além do básico|Tecnologia/Testes JS/14]] — Playwright além do básico; a nota 9 usa Playwright como loop de feedback visual/de design, não reexplica a ferramenta.
- [[03-Dominios/Engenharia/UX/index|Engenharia/UX]] — o ofício durável que estas ferramentas servem.

## Veja também

- [[00-Meta/Roadmap|Roadmap de Trilhas]] — Ferramentas de Design entra junto com UX como construção nova em andamento.
- [[03-Dominios/Engenharia/UX/index|Engenharia/UX]] — o domínio-irmão estável.
