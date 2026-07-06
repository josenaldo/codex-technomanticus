---
title: "Roadmap — Performance de Carregamento"
created: 2026-07-06
type: meta
publish: false
tags:
  - meta
  - roadmap
---

# Roadmap — Performance de Carregamento

Roadmap do galho `03-Dominios/Tecnologia/Web Performance/Performance de Carregamento`. Galho **em construção**: eixo primário = **escrita** (8 notas); enriquecimento (mídia M1) secundário. Roster derivado do [[00-Meta/specs/2026-07-05-dominio-web-performance-design|design 2026-07-05]] (escopo do Galho 2) + `index.md`.

## Régua de análise

- **Escrita:** ⬜ não escrita · 🔄 rascunho · ✅ escrita + verificada + commitada (YYYY-MM-DD).
- **Enriquecimento:** ⬜ pendente · ➖ n/a · ✅ enriquecida (gap esperado = M1 mídia).

**Esquema de `fase:`:** COM fase (Iniciado ≥300 / Adepto ≥400 / Magus ≥500 linhas — piso guiado pelo padrão capítulo, não literal).

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 8 |
| ⬜ não escritas | 0 |
| ✅ escritas | 8 |
| % escrito | 100% |

---

## Notas

#### 01 - O Critical Rendering Path   [substantivo]
- **Fase:** Iniciado · **Escrita:** ✅ (2026-07-06) · **Enriquecimento:** ⬜ (M1)
- **Escopo:** HTML→DOM, CSS→CSSOM, render tree, layout, paint; onde o tempo é gasto; ligação com [[03-Dominios/Tecnologia/Plataforma Web/Rendering Pipeline/index|Rendering Pipeline]].

#### 02 - Recursos que bloqueiam a renderização   [substantivo]
- **Fase:** Iniciado · **Escrita:** ✅ (2026-07-06) · **Enriquecimento:** ⬜ (M1)
- **Escopo:** CSS render-blocking, JS parser-blocking, `async` vs `defer`, critical CSS, adiar o não-crítico. Base em [[03-Dominios/Tecnologia/HTML/10 - Performance em HTML - resource hints e critical path|HTML 10]].

#### 03 - Resource hints e prioridade   [substantivo]
- **Fase:** Iniciado · **Escrita:** ✅ (2026-07-06) · **Enriquecimento:** ⬜ (M1)
- **Escopo:** `preconnect`, `dns-prefetch`, `preload`, `prefetch`, `fetchpriority`, priority hints; quando cada um. Aprofunda HTML 10 pela ótica de LCP.

#### 04 - Otimização de imagens   [substantivo]
- **Fase:** Adepto · **Escrita:** ✅ (2026-07-06) · **Enriquecimento:** ⬜ (M1)
- **Escopo:** AVIF/WebP, `srcset`/`sizes`, `<picture>`, lazy loading nativo, `width`/`height` (anti-CLS), a imagem-LCP e por que quase nunca deve ser lazy.

#### 05 - Fontes web   [substantivo]
- **Fase:** Adepto · **Escrita:** ✅ (2026-07-06) · **Enriquecimento:** ⬜ (M1)
- **Escopo:** FOIT/FOUT, `font-display`, `preload` de fonte, subsetting, self-host vs Google Fonts, variable fonts, `size-adjust` anti-CLS.

#### 06 - Compressão e minificação   [substantivo]
- **Fase:** Adepto · **Escrita:** ✅ (2026-07-06) · **Enriquecimento:** ⬜ (M1)
- **Escopo:** gzip vs Brotli, compressão de texto, minificação; fronteira com [[03-Dominios/Tecnologia/Tooling e Build/17 - Otimização de bundle|Tooling 17]] (bundle) — aqui a ótica é bytes-na-rede.

#### 07 - Cache e CDN   [substantivo]
- **Fase:** Adepto · **Escrita:** ✅ (2026-07-06) · **Enriquecimento:** ⬜ (M1)
- **Escopo:** `Cache-Control`, ETag, immutable, hashing de assets, CDN, edge; fronteira com [[03-Dominios/Ciência/Redes e Protocolos/index|Redes]] e [[03-Dominios/Tecnologia/Plataforma Web/Storage/index|Storage]].

#### 08 - HTTP moderno e estratégia de carregamento   [substantivo]
- **Fase:** Magus · **Escrita:** ✅ (2026-07-06) · **Enriquecimento:** ⬜ (M1)
- **Escopo:** HTTP/2 multiplexing, HTTP/3/QUIC, 103 Early Hints, priorização; síntese de como orquestrar o carregamento pra um LCP bom. Capstone; ponte pro Galho 3.

---

## Fronteiras (o que NÃO duplicar)

- **Runtime/INP/reflow** → Galho 3. Aqui, só o que afeta o *carregamento* (LCP).
- **Bundle/tree-shaking/code-splitting** → [[03-Dominios/Tecnologia/Tooling e Build/17 - Otimização de bundle|Tooling 17]]; aqui a ótica é bytes entregues na rede e seu efeito no LCP.
- **Fundamentos de HTTP/TCP/CORS** → [[03-Dominios/Ciência/Redes e Protocolos/index|Redes e Protocolos]]; aqui, o uso do protocolo para performance.
- Notas existentes (HTML 10, CSS 12, Rendering Pipeline, Networking, Storage, Tooling 17) = **linkadas como reforço**.

## Próximos passos

1. Semear 01→08 via `escrever-nota`, fechando cada uma com `verificar-nota`.
2. Ao completar, subir o estado no roadmap do domínio e no [[00-Meta/Roadmap]].
3. Rodada de enriquecimento (mídia M1).
