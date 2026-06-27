---
title: "React Design Patterns"
type: moc
publish: true
created: 2026-06-26
updated: 2026-06-26
status: evergreen
tags:
  - react
  - design-patterns
  - moc
aliases:
  - React Design Patterns
  - Design Patterns
---

# React Design Patterns

> [!abstract] TL;DR
> **Catálogo de referência** dos padrões consolidados da indústria React, em 3 fases (Iniciado/Adepto/Magus), **TS-first**. O eixo de todos eles é **reuso de lógica** e **inversão de controle**; a evolução foi HOC → render props → **custom hooks**, e os padrões modernos (compound, provider, headless, state reducer/prop getters) compõem essas ideias. Cada entrada é auto-contida (intenção → mecanismo → exemplo `.tsx` → trade-offs → libs que usam); a tipagem difícil vive no galho [[03-Dominios/Tecnologia/React/TypeScript com React/index|TypeScript com React]].

## 🟢 Iniciado — fundamentos de padrões

- [[01 - Padrões no React e a evolução]] — o que é um pattern; HOC → render props → hooks; como ler o catálogo
- [[02 - Container vs Presentational]] — smart/dumb; por que os hooks reescreveram a conversa
- [[03 - Controlled vs Uncontrolled]] — quem é a fonte da verdade; suportar ambos os modos

## 🟡 Adepto — os padrões do dia a dia

- [[04 - Custom hooks como padrão de reuso de lógica]] — o vencedor moderno; substitui HOC/render props
- [[05 - Provider pattern]] — context + provider; provider + reducer; context module functions
- [[06 - Composição - slots, layout e children-as-API]] — children como slot; layout; composição sobre configuração
- [[07 - Compound components]] — `<Select><Select.Option/></Select>`; context interno compartilhado
- [[08 - Render props e function-as-child]] — função que renderiza; quando ainda vale em 2026
- [[09 - Higher-Order Components (HOC)]] — o legado; `withX`; wrapper hell; onde ainda aparece

## 🔴 Magus — padrões avançados e de biblioteca

- [[10 - State reducer e prop getters]] — inversão de controle; o usuário customiza o estado interno (downshift)
- [[11 - Headless components e headless hooks]] — lógica/a11y sem apresentação (Radix, TanStack, Headless UI)
- [[12 - Capstone - escolher o padrão certo e em entrevista]] — decision tree, anti-patterns, mapa de revisão, entrevista

## Veja também

- [[03-Dominios/Tecnologia/React/React core/index|React core]] — a biblioteca (mecânica de hooks, composição, context)
- [[03-Dominios/Tecnologia/React/TypeScript com React/index|TypeScript com React]] — tipagem dos padrões
- [[03-Dominios/Tecnologia/React/Dicionário de React|Dicionário de React]] — glossário
- [[03-Dominios/Tecnologia/React/React Red Flag Manual|React Red Flag Manual]] — antipatterns
- [[03-Dominios/Tecnologia/React/index|React (domínio)]]
