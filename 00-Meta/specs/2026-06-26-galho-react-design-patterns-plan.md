---
title: "Plano — Galho React Design Patterns"
type: spec
created: 2026-06-26
updated: 2026-06-26
status: draft
tags:
  - spec
  - galho
  - react
  - design-patterns
  - frontend
aliases:
  - Plano React Design Patterns
---

# Plano — Galho React Design Patterns (galho 2 do domínio React)

## Objetivo

Criar o galho **React Design Patterns** no domínio multi-galho `Tecnologia/React` — um **catálogo de referência** dos padrões consolidados da indústria React, em 3 fases (Iniciado/Adepto/Magus), padrão capítulo, **TS-first**. Alvo: prep entrevistas internacionais, perfil Senior Fullstack. É o **galho 2** da sequência do domínio React (após React core), parte da Onda A do [[00-Meta/Roadmap|Roadmap]].

**Tese:** padrões em React são soluções reutilizáveis para problemas recorrentes de composição, reuso de lógica e inversão de controle. Em 2026, **a maioria dos padrões clássicos (HOC, render props) foi absorvida por custom hooks** — então o galho ensina os padrões vivos a fundo e os legados pelo que ainda aparecem (libs antigas, entrevista, casos específicos).

## Princípio: catálogo auto-contido (redundância é reforço)

Diferente das outras trilhas, este galho é um **catálogo de referência auto-contido** ([[feedback_redundancia_entre_notas]]). Cada padrão é uma entrada **completa**: intenção (que problema resolve) → mecanismo → exemplo `.tsx` cheio (com **tipagem mostrada inline**, TS-first) → trade-offs e quando usar/evitar → quais bibliotecas o usam. **Pode repetir** conteúdo que vive em React core / TypeScript com React, mas sempre **sob a ótica do padrão**. Os links pras notas canônicas continuam (para o aprofundamento daquele tema), mas o leitor não precisa sair do catálogo para entender o padrão.

## Domínio multi-galho — posição

Galho 2 de: 1. React core ✅ · **2. React Design Patterns (este)** · 3. Next.js · 4. Ecossistema · 5. TypeScript com React (existe) · 6. Charts (existe).

## Princípios

- **Escrita do ZERO com pesquisa** (estado 2026), usando as fontes-base abaixo + WebSearch dirigido.
- **TS-first**: exemplos em `.tsx` com tipos idiomáticos; a tipagem do padrão é mostrada aqui, linkando [[03-Dominios/Tecnologia/React/TypeScript com React/index|TypeScript com React]] só para nuances profundas.
- **Padrão capítulo** ([[feedback_padrao_capitulo_livro]]): problema-primeiro, registro Feynman ([[feedback_enriquecimento_feynman]]), exemplos trabalhados, Mermaid onde agrega, "Como explicar em inglês" + PT↔EN, "Armadilhas comuns". Notas profundas com diagramas ([[feedback_notas_profundas_diagramas]]).
- **Calibração por fase** ([[project_trilhas_fases_aprendizado]]) — a maioria dos padrões é Adepto/Magus.

## Fontes-base de pesquisa (consultar ao escrever cada padrão)

- [patterns.dev — React](https://www.patterns.dev/react/)
- [react-in-patterns (Krasimir Tsonev)](https://github.com/krasimir/react-in-patterns)
- [refine.dev — React design patterns](https://refine.dev/blog/react-design-patterns/)
- [dev.to (WoMakersCode) — Design Patterns no React](https://dev.to/womakerscode/design-patterns-como-eles-se-aplicam-no-react-1118)
- [Medium (Ignatovich) — A Dive into React Design Patterns](https://medium.com/@ignatovich.dm/a-dive-into-react-design-patterns-76dcd62ccd19)
- [perssondennis — 21 Fantastic React Design Patterns](https://www.perssondennis.com/articles/21-fantastic-react-design-patterns-and-when-to-use-them)
- [GreatFrontend — React Design Patterns](https://www.greatfrontend.com/react-interview-playbook/react-design-patterns)
- [LogRocket — React design patterns](https://blog.logrocket.com/react-design-patterns/)
- [TurboDocx — React Design Patterns](https://www.turbodocx.com/blog/react-design-patterns)
- [UXPin — React Design Patterns](https://www.uxpin.com/studio/blog/react-design-patterns/)

Cada nota cita as fontes que usou em `## Referências` (proveniência), além das oficiais (react.dev) quando aplicável.

## Fronteiras (seams — linkar E reforçar, não apenas adiar)

| Tema | Tratamento aqui | Linka |
| ---- | --------------- | ----- |
| Tipagem profunda dos padrões (generics, satisfies) | tipagem básica mostrada inline | [[03-Dominios/Tecnologia/React/TypeScript com React/14 - Compound components, slots, render props\|TS-com-React 14]], 13 |
| Composição básica / arquitetura de app | recap sob ótica de padrão | React core 08 e 24 |
| Mecânica de hooks (regras, useState/useEffect) | usada, não reensinada do zero | React core 14, 09 |
| Polymorphic (`as` prop) | menção | TS-com-React 13 |

## Roster (12 notas — 3 / 6 / 3)

### 🟢 Iniciado — fundamentos de padrões (3)
1. **Padrões no React e a evolução** — o que é um design pattern no contexto React; a história HOC → render props → **custom hooks** (por que os hooks venceram); como ler uma entrada deste catálogo (intenção/mecanismo/trade-off)
2. **Container vs Presentational** — smart/dumb components; o padrão clássico e por que os hooks reescreveram a conversa
3. **Controlled vs Uncontrolled** — quem é a fonte da verdade; `value`+`onChange` vs `defaultValue`+ref; quando cada um; componentes que suportam ambos

### 🟡 Adepto — os padrões do dia a dia (6)
4. **Custom hooks como padrão de reuso de lógica** — o "vencedor" moderno; como substitui HOC e render props; composição de hooks; exemplos (useToggle, useFetch)
5. **Provider pattern** — context + provider; provider + reducer (o "mini-Redux"); **context module functions** (Kent C. Dodds); custom hook que encapsula o context com guard
6. **Composição: slots, layout e children-as-API** — children como slot; múltiplos slots via props de JSX; layout components; children-as-API; composição sobre configuração
7. **Compound components** — `<Select><Select.Option/></Select>`; context interno compartilhado; flexibilidade vs acoplamento; como as libs de UI usam
8. **Render props e function-as-child** — passar uma função que renderiza; quando ainda vale em 2026 vs custom hook
9. **Higher-Order Components (HOC)** — o legado; `withX`; composição de HOCs; problemas (wrapper hell, props colisão); onde ainda aparece

### 🔴 Magus — padrões avançados e de biblioteca (3)
10. **State reducer + prop getters** — inversão de controle; o usuário customiza o comportamento interno; o padrão do `downshift`/Kent C. Dodds
11. **Headless components e headless hooks** — lógica sem apresentação; Radix, TanStack (Table/Query), Headless UI; separar comportamento de estilo; por que é o padrão dominante de libs em 2026
12. **Capstone — escolher o padrão certo e em entrevista** — decision tree (qual padrão para qual problema), anti-patterns, mapa de revisão do galho, "como explicar em inglês"

## Artefatos do domínio

- **`Dicionário de React`** — já existe; enriquecer com verbetes dos padrões (HOC, render prop, compound component, prop getter, headless, etc.).
- **Índice do galho** — `index.md` da subpasta `Design Patterns/`, MOC das 3 fases.
- **`React/index.md`** — atualizar: galho React Design Patterns de ⬜ planejado → 🟩 (linkar o índice).

## Execução

Pasta-alvo: `03-Dominios/Tecnologia/React/Design Patterns/` (notas `01 - …` a `12 - …` + `index.md`).

1. **Escrever o galho fresco** (com pesquisa nas fontes-base), em ondas por fase, gate `/verificar-nota` por nota e `/verificar-wikilinks` por fase. Padrão subagente-por-nota.
2. **Teardown:** criar índice do galho; atualizar `React/index.md` (marcar galho); verificar 0 quebras; atualizar [[00-Meta/Roadmap|Roadmap]].
3. **(Opcional) Ciclo de qualidade:** `/plantar-duvidas` → `/colher-duvidas`; `/enriquecer-nota`.

## Fora de escopo (deste galho)

- **Next.js**, **Ecossistema (MUI/Mantine/TanStack Query)** → galhos próprios.
- Mecânica de hooks e fundamentos de React → galho React core (pronto).
- Tipagem profunda dos padrões → galho TypeScript com React (existe).

## Padrões e referências

- [[00-Meta/Roadmap|Roadmap de Trilhas]] (Onda A — domínio React)
- [[project_trilhas_fases_aprendizado]], [[feedback_padrao_capitulo_livro]], [[feedback_notas_profundas_diagramas]], [[feedback_redundancia_entre_notas]], [[project_tronco_galhos_pattern]], [[project_artefatos_dominio]]
- Galho-modelo: [[03-Dominios/Tecnologia/React/React core/index|React core]] (26 notas)
