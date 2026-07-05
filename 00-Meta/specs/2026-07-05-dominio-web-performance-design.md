---
title: "Domínio Web Performance & Core Web Vitals — design"
created: 2026-07-05
type: design
status: draft
publish: false
tags:
  - meta
  - design
  - web-performance
  - core-web-vitals
---

# Domínio Web Performance & Core Web Vitals — design

## Contexto

Web Performance & Core Web Vitals é uma das **coberturas ausentes (🚫)** do
[[00-Meta/Roadmap|Roadmap de Trilhas]] — tema que um perfil Senior Fullstack precisa e
que hoje o vault não cobre como trilha própria. O Roadmap registra que o tema é
"tangenciado em Tooling nota 17; falta a ótica de produto".

O domínio é intrinsecamente **transversal**: já existem notas de performance espalhadas
por outras trilhas —

- `Tecnologia/CSS/12 - Performance CSS`
- `Tecnologia/HTML/10 - Performance em HTML - resource hints e critical path`
- `Tecnologia/React/React core/17 - Performance no React`
- `Tecnologia/Plataforma Web/Rendering Pipeline/` (pipeline de renderização do browser)
- `Tecnologia/Plataforma Web/Networking/` (rede, HTTP)
- `Tecnologia/Tooling e Build/17` (tangencia Core Web Vitals)

**Princípio-guia:** este domínio **não reescreve** essas notas. Ele fornece a **lente de
medição e produto** que hoje falta — como medir, o que as métricas significam para
usuário/negócio/SEO, e como diagnosticar — e **linka** as notas existentes como reforço
(redundância entre notas = reforço, nunca deduplicar; ver [[feedback_redundancia_entre_notas]]).

## Decisões de design

Tomadas no brainstorming de 2026-07-05:

1. **Forma:** domínio próprio multi-galho (`Tecnologia/Web Performance/`), no molde de
   Plataforma Web — não um galho único nem um galho dentro de Plataforma Web. Justificativa:
   o tema é grande, cai em entrevista senior por si só, e o Roadmap já o trata como
   cobertura autônoma.
2. **Decomposição:** 4 galhos organizados pela **linha do tempo da experiência do usuário**
   — *medir → carregar → responder → sustentar* — que também mapeia limpo nos três Core
   Web Vitals e minimiza sobreposição entre galhos.
3. **Ritmo:** **galho a galho, ponta a ponta**. Fecha-se o Galho 1 (semear + enriquecer até
   ✅) antes de começar o Galho 2. Mantém o contexto leve por sessão e entrega valor
   utilizável mais rápido. (Alternativa rejeitada: semear a espinha inteira primeiro.)
4. **Convenções do vault aplicadas:** notas atômicas em 3 fases (Iniciado/Adepto/Magus) com
   `fase:` no frontmatter; padrão capítulo de livro; Mermaid; piso de linhas por fase;
   `roadmap.md` do domínio (galho-pai) + `roadmap.md` por galho; MOC agrupado por fase.

## Arquitetura do domínio

**Pasta:** `03-Dominios/Tecnologia/Web Performance/`

**`index.md`** (`type: moc`): TL;DR do domínio + tabela dos 4 galhos com a metáfora
*medir → carregar → responder → sustentar* + bloco **Fronteiras** apontando pras notas de
perf que já existem em CSS/HTML/React/Plataforma Web, deixando explícito o papel de
lente-de-medição deste domínio.

**Os 4 galhos:**

| # | Galho | Escopo | CWV âncora | Fronteira / linka |
|---|-------|--------|-----------|-------------------|
| 1 | **Medição & Core Web Vitals** | LCP/INP/CLS, thresholds, lab vs field (RUM), Lighthouse, PageSpeed, CrUX, lib `web-vitals`, performance budgets como conceito | os 3 | Tooling 17 |
| 2 | **Performance de Carregamento** | critical rendering path, resource hints, lazy loading, imagens (AVIF/WebP/responsive), fontes, compressão (Brotli), cache/CDN, HTTP/2-3, priority hints | LCP | HTML 10, CSS 12, Plataforma Web/Networking |
| 3 | **Performance de Runtime & Rendering** | main thread, long tasks, INP a fundo, reflow/repaint, layout thrashing, compositing/GPU, offload p/ Workers, custo de JS/hidratação | INP, CLS | Plataforma Web/Rendering Pipeline, React core 17 |
| 4 | **Performance em Produção** | budgets no CI (Lighthouse CI), RUM/monitoramento, detecção de regressão, DevTools Performance panel, impacto no negócio, cultura de perf | — | Engenharia/Operação, IA/Improvement Loop |

**Lógica:** medir (você não otimiza o que não mede) → carregar rápido (LCP) → manter
responsivo (INP/CLS) → sustentar em produção. Cada galho tem foco isolado e testável.

## Galho 1 — Medição & Core Web Vitals (detalhado)

Primeiro galho a ser construído (ritmo B). Vertical de 8 notas em 3 fases.

**Iniciado — *por que e o quê***

1. `01 - Por que performance importa` — impacto no usuário, no negócio (bounce/conversão)
   e no SEO. Abre com o problema; fixa a aposta do domínio inteiro.
2. `02 - Os três Core Web Vitals` — LCP, INP (substituiu FID em mar/2024), CLS: o que cada
   um mede + thresholds good / needs-improvement / poor. **Nota-âncora do galho.**
3. `03 - Lab vs Field` — medição sintética (lab) vs dados de usuários reais (RUM/field);
   por que divergem e quando usar cada uma.

**Adepto — *ferramentas e prática***

4. `04 - Lighthouse & PageSpeed Insights` — auditoria lab, como ler o relatório e o
   performance score.
5. `05 - CrUX e dados de campo` — Chrome UX Report, field data, o que o Google usa como
   sinal de ranking.
6. `06 - Instrumentando RUM` — a biblioteca `web-vitals`, coletar métricas de usuários
   reais e enviar pra analytics.
7. `07 - Métricas de apoio` — TTFB, FCP, TBT, Speed Index e como se ligam aos CWV.

**Magus — *síntese e estratégia***

8. `08 - Performance budgets e diagnóstico` — definir orçamentos de performance, priorizar,
   e usar o DevTools Performance panel pra achar a causa de um CWV ruim. **Ponte narrativa**
   pros Galhos 2 (carregamento) e 3 (runtime).

## Fronteiras (o que NÃO duplicar)

- **INP a fundo** (main thread, long tasks) mora no Galho 3; no Galho 1, só "o que o INP mede".
- **Resource hints / critical path** moram no Galho 2 (base em HTML 10); no Galho 1, só
  aparecem como "o que o diagnóstico revela".
- **CI / Lighthouse CI, RUM em produção** moram no Galho 4; no Galho 1, a lib `web-vitals`
  entra só como instrumentação básica.
- Notas existentes (CSS 12, HTML 10, React 17, Rendering Pipeline, Networking) são
  **linkadas como reforço**, nunca reescritas.

## Caducidade a vigiar

Tema envelhece rápido — cravar datas e versões nas notas:

- **INP** substituiu FID como Core Web Vital em **mar/2024**; FID foi descontinuado.
- Thresholds dos CWV (LCP ≤2,5s / INP ≤200ms / CLS ≤0,1) podem ser revisados pelo Google.
- Formatos de imagem (AVIF/WebP) e suporte de browser evoluem.
- Ferramentas (Lighthouse, PageSpeed, CrUX) mudam de versão/UI.

## Escopo desta entrega

Este design cobre **a casca do domínio + o Galho 1**. Os Galhos 2–4 têm o escopo esboçado
na tabela acima, mas seu roster de notas detalhado será desenhado quando chegar a vez de
cada um (ritmo B). O plano de implementação a seguir cobre: criar a pasta + `index.md` +
`roadmap.md` do domínio, e semear + enriquecer as 8 notas do Galho 1.

## Veja também

- [[00-Meta/Roadmap|Roadmap de Trilhas]] — Web Performance sai de 🚫 sem cobertura
- Skills: `escrever-nota`, `verificar-nota`, `diagnosticar-galho`, `enriquecer-galho`
