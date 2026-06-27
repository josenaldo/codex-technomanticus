---
title: "Roadmap de Trilhas"
type: moc
publish: true
created: 2026-06-25
updated: 2026-06-25
status: growing
tags:
  - moc
  - meta
  - roadmap
  - planejamento
aliases:
  - Roadmap
  - Roadmap de Trilhas
  - Plano de Trilhas
---

# Roadmap de Trilhas

> [!abstract] TL;DR
> Esta é a **fonte única de verdade da ordem de construção** do grimório — o que já existe como trilha atômica, o que ainda é monólito/stub, e o que falta por completo para o perfil-alvo: **Senior Fullstack Developer** (backend Java/Spring + frontend TS/React), prep para entrevistas internacionais remotas.
>
> **Não confundir com as [[04-Sendas/Sendas|Sendas]]**: Senda = *ordem de leitura* curatorial de um tema; Roadmap = *ordem de construção* do vault. As Sendas consomem o que este Roadmap produz.

> [!info] Como manter este arquivo
> Ao concluir/criar uma trilha, mova-a de seção e atualize o `updated:`. Cada item linka o índice do domínio. Estado é avaliado por: existem notas atômicas numeradas em 3 fases (Iniciado/Adepto/Magus)? Ou é só um monólito `.md`?

## Legenda de estado

| Ícone | Estado | Significado |
| ----- | ------ | ----------- |
| ✅ | **Construída** | Trilha atômica em 3 fases, padrão capítulo, enriquecida |
| 🟡 | **Parcial** | Existe estrutura/galhos, mas incompleta ou precisa de reforma |
| 🧱 | **Monólito** | Conteúdo existe como 1 nota gigante; falta atomizar em trilha |
| ⬜ | **Stub/vazio** | Quase nada; precisa ser escrita do zero |
| 🚫 | **Sem cobertura** | Tema que um fullstack precisa e o vault não tem |

---

## 1. Tecnologia — o stack do dia a dia

### Frontend (o maior buraco para o perfil fullstack)

| Trilha | Estado | Nota |
| ------ | ------ | ---- |
| [[03-Dominios/Tecnologia/TypeScript/index\|TypeScript]] | ✅ | 27 notas, 3 fases |
| [[03-Dominios/Tecnologia/Tooling e Build/index\|Tooling e Build]] | ✅ | 26 notas, concluída 2026-06-25 |
| [[03-Dominios/Tecnologia/JavaScript/index\|JavaScript (core)]] | ✅ | 26 notas, 3 fases, concluída 2026-06-25 (monólito aposentado em stub) |
| [[03-Dominios/Tecnologia/React/index\|React]] | 🟡 | domínio multi-galho; **React core ✅** (26) + **Design Patterns ✅** (12, 2026-06-26) + **Next.js ✅** (16, 2026-06-27, baseline Next 15) + TypeScript com React (15); falta Ecossistema |
| [[03-Dominios/Tecnologia/HTML/index\|HTML]] | 🧱 | só `HTML semântico.md`; falta forms, a11y, ARIA, SEO, metadados |
| [[03-Dominios/Tecnologia/CSS/index\|CSS]] | 🧱 | só `CSS.md` + Bootstrap; falta layout (flex/grid), cascade, responsivo, design system |
| [[03-Dominios/Tecnologia/Plataforma Web/index\|Plataforma Web]] | 🟡 | só galho Networking; falta DOM, eventos, rendering, Web APIs, storage, Workers |

### Backend / Runtime

| Trilha | Estado | Nota |
| ------ | ------ | ---- |
| [[03-Dominios/Tecnologia/Java/index\|Java (Senior)]] | ✅ | 18 galhos incl. Certificação OCP |
| [[03-Dominios/Tecnologia/Node/index\|Node]] | 🟡 | 8 galhos construídos — **alvo de "Reforma do Node"**: reordenar/renumerar/atomizar no padrão da reformulação do Anatomia dos LLMs |
| [[03-Dominios/Tecnologia/Go/index\|Go]] | ⬜ | stub (3 notas) |
| [[03-Dominios/Tecnologia/Python/index\|Python]] | ⬜ | stub (4 notas) |

### IA, Terminal, Infra, RPA

| Trilha | Estado | Nota |
| ------ | ------ | ---- |
| [[03-Dominios/Tecnologia/IA/index\|IA]] | 🟡 | 21 galhos, 322 notas; em enriquecimento (Anatomia dos LLMs reformulação, Agents) |
| [[03-Dominios/Tecnologia/Terminal/index\|Terminal]] | ✅ | 7 galhos, 78 notas |
| [[03-Dominios/Tecnologia/Infraestrutura/index\|Infraestrutura]] | 🟡 | só galho Linux; falta Docker, Kubernetes, Nginx, Cloud |
| [[03-Dominios/Tecnologia/RPA/index\|RPA]] | ⬜ | stub (6 notas) |

---

## 2. Engenharia — o diferencial de Senior

| Trilha | Estado | Nota |
| ------ | ------ | ---- |
| [[03-Dominios/Engenharia/Design de Software/index\|Design de Software]] | 🟡 | 25 notas, 2 galhos (SOLID, OO, Patterns) |
| [[03-Dominios/Engenharia/Segurança/index\|Segurança]] | 🟡 | 23 notas; consolidar |
| [[03-Dominios/Engenharia/Testes/index\|Testes]] | 🟡 | 17 notas (geral/conceitual) — **falta a vertente "Testes no ecossistema JS"** (Vitest, Jest, Testing Library, Playwright, MSW) |
| [[03-Dominios/Engenharia/Complexidade de Software/index\|Complexidade de Software]] | 🟡 | 17 notas |
| [[03-Dominios/Engenharia/Arquitetura/index\|Arquitetura / System Design]] | 🟡 | 7 notas — **crítico para entrevista senior; aprofundar** |
| [[03-Dominios/Engenharia/Comunicação entre Sistemas/index\|Comunicação entre Sistemas]] | 🟡 | 8 notas (API design, REST/GraphQL/gRPC, mensageria) |
| [[03-Dominios/Engenharia/Operação/index\|Operação (DevOps/SRE)]] | ⬜ | 1 nota — **CI/CD, deploy, observabilidade, on-call: buraco grande para fullstack** |
| [[03-Dominios/Engenharia/Dados/index\|Dados (Data Engineering)]] | ⬜ | 1 nota — modelagem, pipelines, analytics |

---

## 3. Ciência — fundamentos (camada madura)

> Domínio **Fundamentos** essencialmente completo: 11 trilhas atômicas (Algoritmos, Estruturas de Dados, Banco de Dados, Redes e Protocolos, Sistemas Operacionais, Concorrência, Paradigmas, Teoria da Computação, Complexidade, Organização de Computadores, Compiladores, Matemática). Manutenção/enriquecimento conforme necessário, não construção nova.

---

## 4. Carreira — o que fecha a candidatura

| Trilha | Estado | Nota |
| ------ | ------ | ---- |
| [[03-Dominios/Carreira/Entrevistas/index\|Entrevistas]] | 🟡 | 6 notas — falta behavioral (STAR), system design practice, negociação |
| [[03-Dominios/Carreira/Inglês/index\|Inglês]] | 🟡 | 4 notas + mentoria GCA; articulação técnica em inglês |
| [[03-Dominios/Carreira/Empreendedorismo/index\|Empreendedorismo]] | 🟡 | 23 notas, 1 galho |

---

## 5. O que falta para um Fullstack completo — backlog priorizado

> [!todo] Ordem de construção sugerida
> A lógica: fechar primeiro o **tripé frontend** (a maior lacuna do perfil, já que backend Java está maduro), depois subir para **system design / operação** (profundidade de senior), e em paralelo as **reformas** de consolidação.

### Onda A — Tripé Frontend (prioridade máxima)
1. ✅ **JavaScript (core)** — **CONCLUÍDA 2026-06-25** (26 notas, 3 fases): closures, protótipos & `this`, coerção, async no nível da linguagem, iterators/generators, módulos, metaprogramação, ES2026. Base que o índice do TypeScript referencia.
2. 🟡 **React** — domínio multi-galho. **Galho React core CONCLUÍDO 2026-06-25** (26 notas, TS-first): render model, hooks a fundo, reconciliation, estado, Suspense/concurrent/RSC, Actions, performance, testing. Galhos restantes do domínio: **React Design Patterns**, **Next.js** (App Router + Pages Router), **Ecossistema** (MUI, Mantine, TanStack Query) — specs próprios.
3. 🧱→✅ **HTML** — semântica, forms, acessibilidade (ARIA/a11y), SEO, metadados.
4. 🧱→✅ **CSS** — box model, flex/grid, cascade & specificity, responsivo, design tokens.
5. 🟡→✅ **Plataforma Web** — DOM, event loop no browser, rendering pipeline, Web APIs, storage, Service Workers.

### Onda B — Reformas e consolidações
6. 🟡 **Reforma do Node** — atomizar/reordenar os 8 galhos no padrão capítulo.
7. 🟡 **Testes no ecossistema JS** — galho/trilha específica (Vitest, Jest, Testing Library, Playwright, MSW), ligando a `Engenharia/Testes` (conceitual) e à nota 19 de Tooling (`node:test`).

### Onda C — Profundidade de Senior (system design & operação)
8. 🟡 **Arquitetura / System Design** — escalar de 7 notas para trilha de entrevista (CAP, sharding, caching, filas, consistência, design exercises).
9. ⬜ **Operação (DevOps/SRE)** — CI/CD, containers em produção, observabilidade, deploy strategies, incident response.
10. 🟡 **Comunicação entre Sistemas** — API design (REST/GraphQL/gRPC), versionamento, mensageria, idempotência.

### Onda D — Carreira (em paralelo, contínuo)
11. 🟡 **Entrevistas** — behavioral/STAR, system design practice, coding strategy.
12. 🟡 **Inglês** — articulação técnica (alimentado pela mentoria GCA).

### Coberturas ausentes a considerar (🚫 hoje sem trilha)
- **Cloud** (AWS/GCP) — há `Senda Cloud`, mas sem domínio próprio construído.
- **Auth & Identidade** (OAuth2/OIDC/JWT/sessões) — espalhado em Segurança; merece foco.
- **Web Performance & Core Web Vitals** — tangenciado em Tooling nota 17; falta a ótica de produto.
- **Acessibilidade (a11y)** — entra como fase do HTML, mas é tema de entrevista por si só.

---

## Veja também

- [[04-Sendas/Sendas|Sendas]] — ordens de leitura que consomem estas trilhas
- [[04-Sendas/Senda Frontend|Senda Frontend]] · [[04-Sendas/Senda Entrevistas|Senda Entrevistas]]
- Planos detalhados por trilha/galho: pasta `00-Meta/specs/`
- [[00-Meta/guia/pipeline/Domínios|Pipeline: Domínios]]
