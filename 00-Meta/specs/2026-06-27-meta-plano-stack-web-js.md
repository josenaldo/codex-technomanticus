---
title: "Meta-plano — Stack Web/JS (Onda A + B)"
type: spec
created: 2026-06-27
updated: 2026-06-27
status: active
tags:
  - spec
  - meta-plano
  - frontend
  - javascript
  - web
---

# Meta-plano — Stack Web/JS

> **Fonte única de verdade** para o trabalho restante no eixo frontend/web/JS.
> Atualizar este arquivo a cada galho concluído — não o Roadmap (ele é derivado).

---

## Trilhas já concluídas (referência)

| Trilha | Notas | Concluída |
|--------|-------|-----------|
| TypeScript | 27 (10/10/7) | 2026-06-24 |
| Tooling e Build | 26 | 2026-06-25 |
| JavaScript (core) | 26 | 2026-06-25 |
| React core | 26 | 2026-06-25~26 |
| React — Design Patterns | 12 | 2026-06-26 |
| React — Next.js (App Router) | 16 | 2026-06-27 |
| React — Ecossistema | 13 | 2026-06-27 |
| HTML | 12 (4/4/4) | 2026-06-27 |
| CSS | 13 (4/5/4) | 2026-06-27 |

---

## Onda A — Tripé Frontend (prioridade máxima)

### A3 — HTML ✅ CONCLUÍDO 2026-06-27

- **12 notas** (4 Iniciado / 4 Adepto / 4 Magus)
- Plano: `2026-06-27-trilha-html-plan.md`
- Monólito `HTML semântico.md` aposentado (redirector para index)
- Roadmap atualizado
- **Status:**
  - [x] Plano detalhado escrito e aprovado
  - [x] Fase Iniciado executada e commitada
  - [x] Fase Adepto executada e commitada
  - [x] Fase Magus executada e commitada
  - [x] Teardown: monólito aposentado, index.md MOC, Roadmap atualizado

---

### A4 — CSS ✅ CONCLUÍDO 2026-06-27

- **Estado:** 13 notas (4 Iniciado / 5 Adepto / 4 Magus), monólitos removidos
- **Plano detalhado:** `2026-06-27-trilha-css-plan.md`
- **Status:**
  - [x] Plano detalhado escrito e aprovado
  - [x] Fase Iniciado executada e commitada (01–04: cascade/box model, unidades/cores, Flexbox, Grid)
  - [x] Fase Adepto executada e commitada (05–09: especificidade/@layer, responsivo, custom props, seletores modernos, animações)
  - [x] Fase Magus executada e commitada (10–13: Tailwind v4, arquitetura de estilos, performance, entrevista)
  - [x] Teardown: `CSS.md` e `Bootstrap.md` removidos, index.md MOC, Roadmap atualizado

---

### A5 — Plataforma Web

- **Estado:** 1 galho `Networking/` (3 stubs: Axios.md, Fetch.md, index.md) + `Debugging.md` solto + `index.md`
- **Plano detalhado:** a criar (`2026-XX-XX-trilha-plataforma-web-plan.md`)
- **Escopo (galhos a construir):**
  1. **DOM e seleção** — árvore DOM, seleção, traversal, manipulação, fragmentos
  2. **Eventos** — event model (bubbling/capturing), delegation, custom events, pointer/keyboard/touch
  3. **Rendering pipeline** — parse HTML→CSSOM→layout→paint→composite; reflow vs repaint; CRP otimizado
  4. **Web APIs** — Intersection Observer, MutationObserver, ResizeObserver, History API, Clipboard, Geolocation, Notifications
  5. **Storage** — cookies, localStorage, sessionStorage, IndexedDB, Cache API
  6. **Workers e concorrência** — Web Workers, Service Workers (ciclo de vida, cache strategies), Worklets
  7. **Networking** — reformar o galho existente: Fetch, Streams, SSE, WebSockets, HTTP/2 push (Axios → stub/ponteiro)
- **Estimativa:** ~7 galhos × ~8–12 notas = ~56–84 notas totais (domínio maior)
- **Dependências:** HTML + CSS como base conceitual
- **Anti-duplicação:** Fundamentos/Redes trata TCP/HTTP em baixo nível; JavaScript trata event loop no Node; Tooling trata bundling/SW via build
- **Status:**
  - [ ] Plano detalhado escrito e aprovado
  - [ ] Galho DOM e seleção executado
  - [ ] Galho Eventos executado
  - [ ] Galho Rendering pipeline executado
  - [ ] Galho Web APIs executado
  - [ ] Galho Storage executado
  - [ ] Galho Workers e concorrência executado
  - [ ] Galho Networking reformado
  - [ ] Teardown: `Debugging.md` relocado ou expandido, index.md MOC, Roadmap atualizado

---

## Onda B — Reformas e consolidações

### B6 — Testes no ecossistema JS

- **Estado:** `JavaScript/Testes em JavaScript.md` (1365 ln, monólito) — candidato a trilha própria em `Engenharia/Testes/` ou `Tecnologia/JavaScript/Testes/`
- **Plano detalhado:** a criar (`2026-XX-XX-trilha-testes-js-plan.md`)
- **Escopo:** fundamentos de teste no ecossistema JS, Vitest, Jest, Testing Library (React), Playwright (E2E), MSW (mocking de rede), estratégias de teste (unitário/integração/E2E), CI de testes
- **Estimativa:** ~14–18 notas (3 fases)
- **Decisão pendente:** local da trilha — `Tecnologia/JavaScript/Testes/` (colado no ecossistema) vs galho em `Engenharia/Testes/` (conceitual já existe lá com 17 notas)
- **Anti-duplicação:** `Engenharia/Testes` trata teoria/conceitos universais; esta trilha trata ferramentas e padrões JS concretos
- **Status:**
  - [ ] Decidir localização da trilha
  - [ ] Plano detalhado escrito e aprovado
  - [ ] Fase Iniciado executada e commitada
  - [ ] Fase Adepto executada e commitada
  - [ ] Fase Magus executada e commitada
  - [ ] Teardown: `Testes em JavaScript.md` aposentado, index.md MOC, links com Engenharia/Testes verificados

---

### B7 — Reforma do Node

- **Estado:** 8 galhos construídos no padrão antigo + monólito `Node.js.md` (16KB) ainda vivo
- **Plano detalhado:** a criar (`2026-XX-XX-reforma-node-plan.md`)
- **Galhos existentes (a reformar):**
  | # atual | Galho | Notas |
  |---------|-------|-------|
  | — | Runtime e Event Loop | 13 |
  | — | Streams | 12 |
  | — | ORMs e banco de dados | 10 |
  | — | Observability e produção | 12 |
  | — | Paralelismo | 12 |
  | — | Segurança | 10 |
  | — | Integrações | 10 |
  | — | Frameworks e arquitetura | 12 |
- **Escopo da reforma:** renumerar galhos em ordem lógica de aprendizado (Runtime→Frameworks→Integrações→ORMs→Streams→Paralelismo→Segurança→Observability), auditar fronteiras entre galhos, aposentar `Node.js.md`, atualizar `index.md` MOC
- **Nota:** as notas *dentro* de cada galho já seguem o padrão capítulo (foram escritas recentemente); a reforma é de estrutura/ordem, não de conteúdo
- **Status:**
  - [ ] Decidir ordem canônica dos galhos
  - [ ] Plano detalhado escrito e aprovado
  - [ ] Renumeração e reorganização executada
  - [ ] `Node.js.md` aposentado
  - [ ] index.md MOC atualizado, Roadmap atualizado

---

## Sequência de execução

```
A3 (HTML) → A4 (CSS) → A5 (Plataforma Web)
                ↓
         B6 (Testes JS)   ← pode iniciar após A3
         B7 (Node)        ← independente, pode ser intercalado
```

HTML primeiro porque:
1. CSS pressupõe elementos semânticos
2. Plataforma Web (DOM/eventos) pressupõe estrutura HTML
3. É o escopo menor → vitória rápida

---

## Convenções aplicadas (todas as trilhas deste meta-plano)

- Notas flat numeradas `01..NN` dentro de cada galho/domínio
- Frontmatter: `fase: Iniciado|Adepto|Magus`, tags pertinentes, `publish: true`
- Padrão capítulo de livro: divulgação progressiva, analogias, Mermaid, registro Feynman
- Callout `[!duvida]` para perguntas de leitura; `[!question]` após resolução
- Commits direto na `main` com paths explícitos (sem `git add .`)
- Sem Co-Authored-By Claude nos commits
- Push manual após cada galho completo
- Monólito aposentado (deletado) só quando 100% absorvido
- `Biblioteca de X.md` e `Dicionário de X.md` = artefatos de domínio, nunca absorvidos na trilha

---

## Como usar este arquivo

1. **Antes de iniciar um galho:** leia a seção correspondente + crie o plano detalhado
2. **Ao concluir cada etapa:** marque o checkbox correspondente
3. **Ao concluir um galho inteiro:** mova-o para a seção "Trilhas já concluídas" com data
4. **Ao concluir toda a Onda A:** atualizar `00-Meta/Roadmap.md` em bloco
