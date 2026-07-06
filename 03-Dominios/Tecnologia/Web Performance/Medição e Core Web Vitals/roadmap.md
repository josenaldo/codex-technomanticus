---
title: "Roadmap — Medição & Core Web Vitals"
created: 2026-07-05
type: meta
publish: false
tags:
  - meta
  - roadmap
---

# Roadmap — Medição & Core Web Vitals

Roadmap do galho `03-Dominios/Tecnologia/Web Performance/Medição e Core Web Vitals`. Galho **em construção**: o eixo primário é **escrita** (quantas das 8 notas do roster já existem); o enriquecimento (sobretudo mídia M1) é secundário, aplicado nota a nota depois. Fonte do roster: `index.md` + [[00-Meta/specs/2026-07-05-dominio-web-performance-design|design 2026-07-05]].

## Régua de análise

Dois eixos de rastreio:

- **Escrita:** ⬜ não escrita · 🔄 rascunho · ✅ escrita + verificada (`verificar-nota`) + commitada (YYYY-MM-DD).
- **Enriquecimento:** ⬜ pendente · ➖ n/a (nota ainda não escrita) · ✅ enriquecida. Gap recorrente esperado = **M1 (vídeo/mídia)**, na rodada futura.

**Esquema de `fase:`:** COM fase (Iniciado ≥300 / Adepto ≥400 / Magus ≥500 linhas).

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 8 |
| ⬜ não escritas | 0 |
| 🔄 rascunho | 0 |
| ✅ escritas | 8 |
| % escrito | 100% |

---

## Notas

#### 01 - Por que performance importa   [substantivo]
- **Fase:** Iniciado
- **Escrita:** ✅ escrita (2026-07-05)
- **Enriquecimento:** ⬜ pendente (M1 mídia)
- **Escopo:** impacto no usuário, no negócio (bounce/conversão) e no SEO. Abre com o problema; fixa a aposta do domínio inteiro. Dados de estudos (Google/Deloitte/Amazon) com fontes.

#### 02 - Os três Core Web Vitals   [substantivo]
- **Fase:** Iniciado
- **Escrita:** ✅ escrita (2026-07-05)
- **Enriquecimento:** ⬜ pendente (M1 mídia)
- **Escopo:** LCP, INP (substituiu FID em mar/2024), CLS — o que cada um mede + thresholds good/needs-improvement/poor. **Nota-âncora do galho.** Cravar datas/valores (caducidade).

#### 03 - Lab vs Field   [substantivo]
- **Fase:** Iniciado
- **Escrita:** ✅ escrita (2026-07-05)
- **Enriquecimento:** ⬜ pendente (M1 mídia)
- **Escopo:** medição sintética (lab) vs dados de usuários reais (RUM/field); por que divergem e quando usar cada uma.

#### 04 - Lighthouse e PageSpeed Insights   [substantivo]
- **Fase:** Adepto
- **Escrita:** ✅ escrita (2026-07-05)
- **Enriquecimento:** ⬜ pendente (M1 mídia)
- **Escopo:** auditoria lab, como ler o relatório e o performance score. Cravar versão/UI (caducidade).

#### 05 - CrUX e dados de campo   [substantivo]
- **Fase:** Adepto
- **Escrita:** ✅ escrita (2026-07-05)
- **Enriquecimento:** ⬜ pendente (M1 mídia)
- **Escopo:** Chrome UX Report, field data, o que o Google usa como sinal de ranking.

#### 06 - Instrumentando RUM   [substantivo]
- **Fase:** Adepto
- **Escrita:** ✅ escrita (2026-07-05)
- **Enriquecimento:** ⬜ pendente (M1 mídia)
- **Escopo:** a biblioteca `web-vitals`, coletar métricas de usuários reais e enviar pra analytics. Código funcional.

#### 07 - Métricas de apoio   [substantivo]
- **Fase:** Adepto
- **Escrita:** ✅ escrita (2026-07-05)
- **Enriquecimento:** ⬜ pendente (M1 mídia)
- **Escopo:** TTFB, FCP, TBT, Speed Index e como se ligam aos CWV.

#### 08 - Performance budgets e diagnóstico   [substantivo]
- **Fase:** Magus
- **Escrita:** ✅ escrita (2026-07-05)
- **Enriquecimento:** ⬜ pendente (M1 mídia)
- **Escopo:** definir orçamentos de performance, priorizar, e usar o DevTools Performance panel pra achar a causa de um CWV ruim. **Ponte narrativa** pros Galhos 2 (carregamento) e 3 (runtime). Capstone.

---

## Fronteiras (o que NÃO duplicar)

- **INP a fundo** (main thread, long tasks) → Galho 3. Aqui, só "o que o INP mede".
- **Resource hints / critical path** → Galho 2 (base em HTML 10). Aqui, só "o que o diagnóstico revela".
- **CI / Lighthouse CI, RUM em produção** → Galho 4. Aqui, `web-vitals` só como instrumentação básica.
- Notas existentes (CSS 12, HTML 10, React core 17, Rendering Pipeline, Networking, Tooling 17) = **linkadas como reforço**, nunca reescritas.

## Próximos passos

1. Semear as 8 notas na ordem (01→08), via `escrever-nota`, fechando cada uma com `verificar-nota`.
2. Ao completar a escrita, subir o estado no `roadmap.md` do domínio (Galho 1: 0% → 100%) e no [[00-Meta/Roadmap]].
3. Rodada de enriquecimento (mídia M1) nota a nota.
