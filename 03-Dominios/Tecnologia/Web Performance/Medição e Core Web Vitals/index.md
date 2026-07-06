---
title: "Medição & Core Web Vitals — índice"
created: 2026-07-05
updated: 2026-07-05
type: index
tags:
  - web-performance
  - core-web-vitals
  - medição
publish: true
---

# Medição & Core Web Vitals

Galho 1 da trilha Web Performance. A porta de entrada do domínio: **como medir performance web e o que as métricas significam**. Cobre os três Core Web Vitals (LCP, INP, CLS), a diferença entre medição de laboratório e de campo, as ferramentas do Google (Lighthouse, PageSpeed, CrUX), como instrumentar usuários reais (RUM com a lib `web-vitals`), as métricas de apoio, e como transformar tudo isso em orçamento de performance e diagnóstico.

A aposta do galho — e do domínio: *você não otimiza o que não mede*.

---

## Fase Iniciado

- [[03-Dominios/Tecnologia/Web Performance/Medição e Core Web Vitals/01 - Por que performance importa|01 — Por que performance importa]] — impacto no usuário, no negócio (bounce/conversão) e no SEO; a aposta do domínio
- [[03-Dominios/Tecnologia/Web Performance/Medição e Core Web Vitals/02 - Os três Core Web Vitals|02 — Os três Core Web Vitals]] — LCP, INP, CLS: o que cada um mede + thresholds. **Nota-âncora**
- [[03-Dominios/Tecnologia/Web Performance/Medição e Core Web Vitals/03 - Lab vs Field|03 — Lab vs Field]] — medição sintética vs dados de usuários reais (RUM); por que divergem

## Fase Adepto

- [[03-Dominios/Tecnologia/Web Performance/Medição e Core Web Vitals/04 - Lighthouse e PageSpeed Insights|04 — Lighthouse e PageSpeed Insights]] — auditoria lab, ler o relatório e o performance score
- [[03-Dominios/Tecnologia/Web Performance/Medição e Core Web Vitals/05 - CrUX e dados de campo|05 — CrUX e dados de campo]] — Chrome UX Report, field data, o sinal de ranking do Google
- [[03-Dominios/Tecnologia/Web Performance/Medição e Core Web Vitals/06 - Instrumentando RUM|06 — Instrumentando RUM]] — a lib `web-vitals`, coletar métricas de usuários reais
- [[03-Dominios/Tecnologia/Web Performance/Medição e Core Web Vitals/07 - Métricas de apoio|07 — Métricas de apoio]] — TTFB, FCP, TBT, Speed Index e como se ligam aos CWV

## Fase Magus

- [[03-Dominios/Tecnologia/Web Performance/Medição e Core Web Vitals/08 - Performance budgets e diagnóstico|08 — Performance budgets e diagnóstico]] — orçamentos, priorização, DevTools Performance panel; ponte pros Galhos 2 e 3. **Capstone**

---

## Próximo galho

**G2 — Performance de Carregamento** *(a construir)* — critical rendering path, resource hints, imagens, fontes, compressão, cache/CDN. Aprofunda o LCP que este galho ensina a medir.
