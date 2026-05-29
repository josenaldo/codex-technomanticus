---
title: "DESIGN.md — A format specification for describing a visual identity to coding agents"
aliases: ["DESIGN.md — A format specification for describing a visual identity to coding agents"]
source: https://github.com/google-labs-code/design.md?ref=dailydev
author: google-labs-code
site: GitHub
published:
read: 2026-04-27
created: 2026-04-27
updated: 2026-05-04
type: glosa
status: lido
progress: in_progress
promovida_em: []
tags: [design-systems, design-tokens, coding-agents, specification]
lang: en
publish: false
---

# DESIGN.md — A format specification for describing a visual identity to coding agents — google-labs-code

## TL;DR

DESIGN.md é uma especificação que descreve a identidade visual de um produto em formato consumível por agentes de código. Combina tokens legíveis por máquina (YAML front matter) com racional de design em prosa markdown, dando aos agentes uma compreensão persistente e estruturada de um design system.

## Pontos-chave

- O arquivo tem duas camadas: YAML front matter (tokens normativos) e corpo markdown (racional de design); tokens são os valores autoritativos, a prosa explica por que existem e como aplicá-los.
- Os tokens cobrem `colors`, `typography`, `rounded`, `spacing` e `components`, com referências cruzadas via sintaxe `{path.to.token}` (ex: `{colors.primary}`).
- Há uma ordem canônica de seções `##`: Overview → Colors → Typography → Layout → Elevation & Depth → Shapes → Components → Do's and Don'ts.
- O CLI `@google/design.md` oferece `lint`, `diff`, `export` (Tailwind/DTCG) e `spec`, todos com saída em JSON consumível por agentes — o último útil para injetar contexto da especificação em prompts.
- Sete regras de lint com severidade fixa: `broken-ref` (erro), `contrast-ratio` (warning, exige WCAG AA 4.5:1), `orphaned-tokens`, `missing-primary`, `missing-typography`, `section-order`, `token-summary`.
- Tokens são inspirados no W3C Design Token Format e exportáveis para Tailwind theme config e DTCG `tokens.json`, garantindo interoperabilidade com o ecossistema existente.
- O formato está em versão `alpha` sob desenvolvimento ativo — schema, spec e CLI podem mudar.

## Citações

> "DESIGN.md gives agents a persistent, structured understanding of a design system."

> "A DESIGN.md file combines machine-readable design tokens (YAML front matter) with human-readable design rationale (markdown prose). Tokens give agents exact values. Prose tells them *why* those values exist and how to apply them."

> "The tokens are the normative values. The prose provides context for how to apply them."

> "Validate a DESIGN.md against the spec, catch broken token references, check WCAG contrast ratios, and surface structural findings — all as structured JSON that agents can act on."

## Meu comentário

Parece um padrão interessante de se observar. Preciso testar se o agente melhora a aderência ao Design System usando esse formato. O fato de ter uma camada de tokens estruturados junto com a prosa explicativa é uma que pode me permitir transmitir, ao agente, não só os valores exatos a usar, mas também o racional por trás deles, o que pode ajudar na tomada de decisão em casos de ambiguidade.

## Ver também

- <https://stitch.withgoogle.com/docs/design-md/specification>
