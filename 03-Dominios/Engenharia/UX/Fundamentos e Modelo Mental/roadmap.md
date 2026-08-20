---
title: "Roadmap — Fundamentos e Modelo Mental"
created: 2026-07-28
type: meta
publish: false
tags:
  - meta
  - roadmap
---

# Roadmap — Fundamentos e Modelo Mental

Diagnóstico nota a nota. Cada entrada tem estado de enriquecimento, score, classificação de custo e plano de execução acionável. Gerado por `/diagnosticar-galho`.

**Galho:** `03-Dominios/Engenharia/UX/Fundamentos e Modelo Mental` **Diagnóstico:** 2026-07-28 **Última execução:** 2026-07-28 — **enriquecimento COMPLETO (5/5 ✅/➖)** **Retrofit M1 (2026-07-28, Task 11):** política do domínio mudou — M1 (mídia verificada) passou a ser **obrigatório em toda nota**, sem isenção por `fase:`. Isso sobrepõe a isenção de fase Iniciado usada no diagnóstico original. Ver `03-Dominios/Engenharia/UX/index.md` para a regra. Notas 02, 04 e 05 — antes `➖` só por causa do gap de M1 — foram reclassificadas para `✅` depois de receber mídia verificada. Ver entradas abaixo.

## Régua de análise

Checklist `verificar-nota` — 12 itens (isenções por fase/tipo/broto aplicadas por nota):

| Grupo | Itens |
|-------|-------|
| ESTRUTURA | E1 TL;DR · E2 Abertura-problema · E3 Mermaid · E4 Casos práticos · E5 O que vem a seguir · E6 Inglês · E7 Tabela PT↔EN · E8 Armadilhas [!warning] |
| PROFUNDIDADE | P1 Código-com-falha · P2 Mecanismo explicado |
| LINKS | L1 Wikilink cross-galho · L2 Referência externa (URL) |
| MÍDIA | M1 Vídeo/podcast embutido |

**Esquema de `fase:` detectado:** COM fase (Iniciado) **Piso de linhas:** aplicável — Iniciado ≥300

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 5 |
| ⬜ pendente | 0 |
| ➖ não precisa | 0 |
| ✅ feita | 5 |
| % concluído | 100% |

> Gaps concentrados em **M1 (mídia)** nas 5 notas. No diagnóstico original, M1 era recomendado-não-obrigatório em fase Iniciado — daí notas 02, 04 e 05 terem ficado `➖` apesar do gap. **Essa isenção foi revogada em 2026-07-28** (Task 11): M1 é agora obrigatório em toda nota do domínio, sem exceção de fase. As 5 notas do sub-galho têm hoje mídia verificada e ficam `✅`.

---

## Notas

#### 01 - UX não é tela - o ofício e seus limites   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-28)
- **Estado:** 187 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** M1 (ausente — sem callout `[!tip]` com vídeo/podcast; recomendado, não obrigatório na fase Iniciado, mas esta é a nota-manifesto do domínio, o que pesa a favor de incluir)
- **Score:** 11/12
- **Plano de execução:**
  - Pesquisar e adicionar 1 callout `[!tip]` com link para vídeo ou podcast sobre "UX é ofício, não tela" / full-cycle engineer fazendo os três papéis do trio de produto sozinho — resolve M1
- **Resultado:** ✅ Callout `[!tip]` adicionado com o vídeo "Product & UX Partnerships" (Anna Kaley, NN/g) — https://www.nngroup.com/videos/product-ux-partnerships/ — logo após a seção do trio de produto. M1 resolvido; nenhuma outra alteração na nota.

#### 02 - Affordances e signifiers   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-28, Task 11 — retrofit M1)
- **Estado:** 146 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** L1 (todos os wikilinks — notas 01, 03, 04 — apontam para dentro da própria pasta "Fundamentos e Modelo Mental"; nenhum link externo à pasta) — mantido, não bloqueia M1; M1 resolvido; P1 N/A (nota conceitual, sem seção de código)
- **Score:** 11/12
- **Plano de execução:**
  - — nenhuma (M1 já resolvido)
- **Resultado:** ✅ Callout `[!tip]` adicionado com o vídeo "Video: The Norman Door, with Vox" (Vox × 99% Invisible, com Don Norman) — https://www.youtube.com/watch?v=ABYSYQmEq1Q — verificado via yt-dlp (transcrição lida). M1 resolvido.

#### 03 - As 10 heurísticas de Nielsen   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-28)
- **Estado:** 156 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** M1 (ausente — sem callout `[!tip]` com vídeo/podcast; recomendado, não obrigatório na fase Iniciado) + atribuição da estatística ~35% (linhas 105 e 119, creditada em Fontes ao artigo NN/g das 10 heurísticas) a verificar/corrigir — provavelmente originária de Nielsen 2000 ("Why You Only Need to Test with 5 Users") ou Nielsen & Landauer 1993, não do artigo das 10 heurísticas
- **Score:** 11/12
- **Plano de execução:**
  - Verificar fonte real do dado ~35% (Nielsen 2000 "Why You Only Need to Test with 5 Users" ou Nielsen & Landauer 1993) e corrigir atribuição em Fontes; remover o número se não confirmável
  - Pesquisar e adicionar 1 callout `[!tip]` com link para vídeo ou podcast sobre avaliação heurística / as 10 heurísticas de Nielsen — resolve M1
- **Resultado:** ✅ Confirmado via WebFetch: o ~35% vem do artigo NN/g "The Theory Behind Heuristic Evaluations" (citando Nielsen & Landauer 1993, INTERCHI'93), não do artigo "10 Usability Heuristics" como estava creditado. Atribuição corrigida em Fontes com URL real; número mantido (confirmado, não removido). Callout `[!tip]` adicionado com vídeo "Heuristic Evaluation of User Interfaces" (Jakob Nielsen, NN/g) — https://www.nngroup.com/videos/heuristic-evaluation/. M1 resolvido.

#### 04 - Leis de UX - Fitts, Hick, Jakob, Miller, Peak-End   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-28, Task 11 — retrofit M1)
- **Estado:** 149 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** M1 resolvido; P1 N/A (nota conceitual, sem seção de código)
- **Score:** 12/12
- **Plano de execução:**
  - — nenhuma (M1 já resolvido)
- **Resultado:** ✅ Callout `[!tip]` adicionado com a talk "Laws of UX: Using Psychology to Design Better Products & Services" (Jon Yablonski, Proximity Lab, 57min) — https://www.youtube.com/watch?v=Qc5F07l1Fjs — verificado via yt-dlp (transcrição confirma cobertura aprofundada de Jakob, Hick e Peak-End; Fitts e Miller não aparecem no mesmo detalhe — registrado no callout). M1 resolvido.

#### 05 - Gestalt aplicada a UI   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-28, Task 11 — retrofit M1)
- **Estado:** 138 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** M1 resolvido; P1 N/A (nota conceitual, sem seção de código)
- **Score:** 12/12
- **Plano de execução:**
  - — nenhuma (M1 já resolvido)
- **Resultado:** ✅ Callout `[!tip]` adicionado com o vídeo "The Gestalt Principles for User Interface Design" (Maria Rosala, NN/g, 3min) — https://www.nngroup.com/videos/the-gestalt-principles-intro/ — verificado via WebFetch. M1 resolvido.
