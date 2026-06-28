---
title: "Plano — Trilha HTML"
type: spec
created: 2026-06-27
updated: 2026-06-27
status: active
tags:
  - spec
  - trilha
  - html
  - frontend
---

# Plano — Trilha HTML (3 fases)

## Visão

`Tecnologia/HTML` deixa de ser a nota-semente `HTML semântico.md` (293 ln de referência rasa) e vira uma **trilha atômica de 12 notas em 3 fases** (Iniciado/Adepto/Magus), padrão capítulo de livro. Alvo: prep entrevistas internacionais, eixo frontend-web, perfil Senior Fullstack.

A tese da trilha: **HTML é um contrato de significado, não de aparência.** Usar o elemento certo não é só "boa prática" — é o que dá a11y, SEO e performance de graça, antes de qualquer CSS ou JS. A trilha vai do modelo mental (por que semântica importa) até as APIs nativas modernas e a perspectiva de entrevista.

## Fonte e método

- **Monólito a minerar:** `HTML semântico.md` (293 ln) cobre superficialmente semântica, forms, ARIA e HTML APIs. Cada nota da trilha aprofunda a seção correspondente ao nível capítulo (exemplos trabalhados, divulgação progressiva, Mermaid, registro Feynman).
- **Decisão: o monólito é APOSENTADO** (deletado) quando todas as 12 notas estiverem prontas — não vira tronco-com-callouts. Redirecionar `[[HTML semântico]]` → `[[03-Dominios/Tecnologia/HTML/index|HTML]]`.
- Notas flat numeradas `01..12` em `Tecnologia/HTML/`, frontmatter `fase: Iniciado|Adepto|Magus`.
- MOC `index.md` atualizado por fase ao fim de cada bloco.

## Fronteiras (anti-duplicação)

| Tema | Dono | Esta trilha faz |
|------|------|-----------------|
| Apresentação visual (cores, layout, tipografia) | `Tecnologia/CSS` | Menciona que CSS é separado; não estiliza nada |
| Manipulação programática do DOM | `Tecnologia/Plataforma Web/DOM e seleção` | Cobre estrutura declarativa; não toca JS DOM API |
| Event listeners, `addEventListener` | `Tecnologia/Plataforma Web/Eventos` | Cobre atributos de evento inline só como anti-padrão |
| JSX e componentes React | `Tecnologia/React` | Menciona que JSX compila p/ HTML; não trata React |
| CSS-in-JS, Tailwind aplicado | `Tecnologia/React` / `Tecnologia/CSS` | Fora de escopo |
| HTTP, DNS, TLS | `Fundamentos/Redes e Protocolos` | Menciona `<link rel=preconnect>` só como dica prática |
| Schema.org profundo, SEO estratégico | Carreira/Entrevistas | Cobre o técnico (JSON-LD, Open Graph); não entra em estratégia de conteúdo |

## Roster por fase (12 notas)

### 🟢 Iniciado (4 notas) — modelo mental e estrutura

**01 — O modelo mental do HTML: semântica, árvore e o browser**
O que é HTML (linguagem de marcação, não programação); como o browser parseia (bytes → tokens → nó → árvore → CSSOM + DOM); *semantic HTML* vs *presentational HTML*; o custo da div-ite (inacessível, SEO fraco, manutenção cara); categorias de conteúdo (flow / phrasing / sectioning / embedded / interactive); o contrato de significado.

**02 — Landmark elements e documento estruturado**
`<!DOCTYPE html>` e o modo padrão; estrutura de `<head>` essencial (charset, viewport); landmark elements com semântica implícita: `<header>`, `<nav>`, `<main>`, `<article>`, `<section>`, `<aside>`, `<footer>`; quando usar cada um (regra do `<article>` auto-contido, regra do `<section>` com heading, etc.); heading outline (`h1`→`h6`): hierarquia como estrutura, não como estilo; exemplo full-page comentado; mapa Mermaid da árvore de landmarks.

**03 — Elementos de conteúdo: texto, listas e inline semântico**
Parágrafos e quebras (`<p>`, `<br>` só quando necessário); listas: `<ul>` / `<ol>` / `<dl>` e quando cada uma; `<blockquote>` + `<cite>`, `<figure>` + `<figcaption>`; elementos inline semânticos: `<strong>` / `<em>` (semântica) vs `<b>` / `<i>` (presentacional); `<mark>`, `<time datetime>`, `<abbr title>`, `<code>`, `<kbd>`, `<samp>`, `<var>`, `<address>`, `<q>`; `<pre>` e blocos de código; tabelas (`<table>`, `<thead>`, `<tbody>`, `<tfoot>`, `<caption>`, `scope`) — quando usar e quando não usar.

**04 — Links, imagens e mídia**
`<a>`: `href` (absoluto/relativo/âncora), `rel="noopener noreferrer"` (segurança), `target="_blank"` (tradeoffs), `download`, `type`; `<img>`: `alt` (vazio para decorativas, descritivo para conteúdo), `srcset` + `sizes` (resolução e largura), `loading="lazy"` + `decoding="async"`, `width` + `height` obrigatórios (evitar CLS), `fetchpriority`; `<picture>`: arte-direção (media) vs troca de formato (type); `<video>` / `<audio>`: `controls`, `preload`, `<track kind="captions">`, `<source>`; `<iframe>`: sandbox, loading, title (a11y).

---

### 🟡 Adepto (4 notas) — formulários e acessibilidade

**05 — Formulários I: estrutura e elementos**
`<form>` (action, method, enctype, novalidate, autocomplete); `<fieldset>` + `<legend>`; `<label>` (for vs wrapping — qual é melhor para a11y); todos os `<input type>` modernos (text, email, tel, url, number, date, time, datetime-local, color, range, search, password, file, hidden, checkbox, radio) com tabela comparativa de uso; `<select>` / `<option>` / `<optgroup>`, `<textarea>`, `<datalist>` (autocompletar com sugestões); tipos de `<button>` (submit/reset/button — por que `type="button"` importa); `<output>`; agrupamentos com `<fieldset>`.

**06 — Formulários II: validação nativa e UX**
Atributos de validação: `required`, `pattern` (regex), `min`/`max`/`step`, `minlength`/`maxlength`; `autocomplete` (valores canônicos: `name`, `email`, `new-password`, `current-password`, `username`, etc.); `inputmode` (numeric, email, tel, url, search — teclado mobile); Constraint Validation API: `validity` (objeto ValidityState), `checkValidity()`, `reportValidity()`, `setCustomValidity(msg)`; hooks CSS `:valid` / `:invalid` / `:user-invalid`; quando usar validação nativa vs JS (tradeoffs); UX de erro: `aria-describedby` + mensagem de erro visível; formulário desativado: `disabled` vs `readonly` vs `aria-disabled`.

**07 — Acessibilidade I: fundamentos WCAG e navegação por teclado**
O modelo de acessibilidade: tecnologias assistivas (leitores de tela, switch access, eye tracking); 4 princípios WCAG (Perceptível, Operável, Compreensível, Robusto); WCAG 2.1 AA como baseline; heading hierarchy como estrutura de navegação; skip links (`<a href="#main">`); ordem de foco (DOM order = tab order); `tabindex` (0, -1 e positivo — quando cada um); navegação por teclado: Tab/Shift-Tab/Enter/Space/Arrow keys; `:focus-visible` vs `:focus` (não esconder outline); contraste de cor: 4.5:1 texto normal, 3:1 large text (WCAG AA), ferramentas de checagem; `alt` text: vazio (`alt=""`) para decorativas, descritivo para conteúdo; imagens complexas (gráfico, diagrama): `aria-describedby` + `longdesc`; checklist rápido de a11y em entrevista.

**08 — ARIA: roles, states, properties e live regions**
O primeiro princípio do ARIA: "No ARIA is better than bad ARIA"; quando ARIA é necessário (widget customizado sem equivalente HTML nativo); landmark roles redundantes vs novos (`role="search"`, `role="banner"`, `role="contentinfo"`); `aria-label` vs `aria-labelledby` vs `aria-describedby` — hierarquia e quando cada um; states: `aria-expanded`, `aria-checked`, `aria-selected`, `aria-pressed`, `aria-disabled`, `aria-invalid`, `aria-hidden`; properties: `aria-haspopup`, `aria-controls`, `aria-owns`, `aria-live`; live regions: `aria-live="polite"` vs `"assertive"`, `role="status"` vs `role="alert"`, `aria-atomic`, `aria-relevant`; padrões de widget ARIA: accordion, tabs, modal (focus trap), combobox; anti-padrões clássicos (div clicável sem role, aria-label em input que já tem label).

---

### 🔴 Magus (4 notas) — SEO, performance e APIs modernas

**09 — SEO técnico e metadados**
`<head>` completo e justificado: `<meta charset>`, `<meta name="viewport">`, `<title>` (regras: 50-60 chars, keyword, brand), `<meta name="description">` (max 160 chars), `<meta name="robots">`, `<link rel="canonical">`, `<link rel="alternate" hreflang>`; Open Graph: `og:title`, `og:description`, `og:image` (1200×630), `og:type`, `og:url`, `og:site_name`; Twitter Cards: `twitter:card`, `twitter:site`, `twitter:creator`; JSON-LD / Schema.org: o que é, por que JSON-LD (em vez de microdata), exemplos (Article, Person, Organization, BreadcrumbList, FAQPage); como o Google consome (Rich Results); `robots.txt` e `sitemap.xml` (menção — não é HTML); Lighthouse SEO score; `<link rel="icon">` e `apple-touch-icon`; `<base>` (e por que raramente usar).

**10 — Performance em HTML: resource hints e critical path**
Critical Rendering Path do ponto de vista do HTML: parse → DOM → CSSOM → Render Tree → Layout → Paint; render-blocking: `<link>` no `<head>` bloqueia render, `<script>` bloqueia parse; estratégias para `<script>`: `defer` (DOM ready, ordem garantida), `async` (sem ordem, download paralelo), `type="module"` (defer por padrão), `nomodule` (fallback); resource hints: `<link rel="preload">` (recurso crítico desta página), `<link rel="prefetch">` (recurso da próxima página), `<link rel="preconnect">` (conexão TCP+TLS antecipada), `<link rel="dns-prefetch">` (DNS only, fallback mais leve); `fetchpriority` em `<img>` e `<link>`; `<link rel="modulepreload">`; `width` + `height` em imagens (previne CLS); Largest Contentful Paint: o que o HTML faz por ele; quando usar `loading="eager"` na imagem hero.

**11 — HTML APIs nativas modernas**
`<dialog>`: `showModal()` vs `show()`, `close(returnValue)`, `::backdrop`, focus management automático, `method="dialog"` em form dentro do dialog; `<details>` + `<summary>`: accordions sem JS, `open` attribute, evento `toggle`; Popover API (2024): `popover="auto"` vs `popover="manual"`, `popovertarget`, `showPopover()`/`hidePopover()`/`togglePopover()`, posicionamento com CSS Anchor Positioning (menção); `<template>` + `<slot>`: stamping de conteúdo, web components intro sem framework; `<progress>` vs `<meter>`: quando cada um, atributos (`value`, `max`, `min`, `low`, `high`, `optimum`); `contenteditable` e `spellcheck`; `<dialog>` vs `popover` vs custom modal JS — mapa de decisão.

**12 — HTML em entrevista**
Capstone: vocabulário PT→EN de HTML; framing da semântica em inglês ("semantic HTML means using elements for their meaning, not their appearance"); perguntas clássicas com resposta direta: "Why `<button>` instead of `<div>`?" / "When to use ARIA vs native elements?" / "What causes CLS and how HTML prevents it?" / "Difference between `alt=""` and no alt?" / "What does `rel='noopener noreferrer'` do?" / "What is the document outline?"; checklist de qualidade de HTML (válido, semântico, acessível, performático, SEO-friendly); mapa de revisão da trilha; links para ferramentas (W3C Validator, axe DevTools, WAVE, Lighthouse).

**Total: 12 notas** (4/4/4).

## Sequência de execução

> **Status atual:** ⬜ não iniciada.

1. **Iniciado (01–04)** — base semântica e estrutural
2. **Adepto (05–08)** — forms e a11y (o coração da prep de entrevista)
3. **Magus (09–12)** — SEO, performance e APIs modernas

Ao fim de cada bloco: atualizar `index.md` com as notas da fase. Ao fim do Magus: aposentar `HTML semântico.md`, verificar wikilinks.

## Decisões fechadas

- **Escopo:** 12 notas (4/4/4) — cobre semântica, forms, a11y/ARIA, SEO, perf e APIs modernas
- **Monólito `HTML semântico.md`:** aposentado (deletado) quando 100% absorvido
- **Localização:** `03-Dominios/Tecnologia/HTML/` (flat, sem sub-pastas)
- **Tabelas:** cobertas na nota 03 (tabelas de dados acessíveis) — não ganham nota própria
- **Web Components:** menção na nota 11 (`<template>`/`<slot>`) — aprofundamento vai em Plataforma Web se necessário

## Âncoras

- [[feedback_padrao_capitulo_livro]] — capítulo que pega o leitor pela mão
- [[feedback_notas_profundas_diagramas]] — ~440-540 ln, diagramas Mermaid
- [[feedback_enriquecimento_feynman]] — analogias, perguntas retóricas, callouts
- [[project_trilhas_fases_aprendizado]] — Iniciado/Adepto/Magus, MOC agrupado
- [[project_artefatos_dominio]] — `Biblioteca de HTML.md` a criar (ou não, se não houver recursos suficientes)
- [[2026-06-27-meta-plano-stack-web-js]] — meta-plano da Onda A
