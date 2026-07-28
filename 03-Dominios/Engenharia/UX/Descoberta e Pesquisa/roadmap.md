---
title: "Roadmap — Descoberta e Pesquisa"
created: 2026-07-28
type: meta
publish: false
tags:
  - meta
  - roadmap
---

# Roadmap — Descoberta e Pesquisa

Diagnóstico nota a nota. Cada entrada tem estado de enriquecimento, score, classificação
de custo e plano de execução acionável. Gerado por `/diagnosticar-galho`.

**Galho:** `03-Dominios/Engenharia/UX/Descoberta e Pesquisa`
**Diagnóstico:** 2026-07-28
**Última execução:** 2026-07-28 — **enriquecimento COMPLETO (9/9 ✅/➖, 0 ⬜, 0 🔄)**
**Retrofit M1 (2026-07-28, Task 11):** política do domínio mudou — M1 (mídia verificada) passou
a ser **obrigatório em toda nota**, sem isenção por `fase:`. Isso sobrepõe a isenção de fase
Iniciado usada no diagnóstico original para 06-08. Ver `03-Dominios/Engenharia/UX/index.md`
para a regra. Notas 07, 10, 11, 12, 13 e 14 — antes `➖` (07 por isenção de fase; 10-14 porque
M1 nunca foi item de núcleo) — foram reclassificadas para `✅` depois de receber mídia
verificada. **Exceção: nota 06 permanece `➖` mesmo sob a política nova** — busca extensiva
não encontrou vídeo/podcast verificável e pertinente ao tema "generativa vs. avaliativa";
buraco honesto, registrado explicitamente na entrada da nota abaixo e no report da Task 11.

## Régua de análise

Checklist `verificar-nota` — 12 itens (isenções por fase/tipo/broto aplicadas por nota):

| Grupo | Itens |
|-------|-------|
| ESTRUTURA | E1 TL;DR · E2 Abertura-problema · E3 Mermaid · E4 Casos práticos · E5 O que vem a seguir · E6 Inglês · E7 Tabela PT↔EN · E8 Armadilhas [!warning] |
| PROFUNDIDADE | P1 Código-com-falha · P2 Mecanismo explicado |
| LINKS | L1 Wikilink cross-galho · L2 Referência externa (URL) |
| MÍDIA | M1 Vídeo/podcast embutido |

**Esquema de `fase:` detectado:** COM fase (Iniciado 06-08, Adepto 09-14)
**Piso de linhas:** aplicável — Iniciado ≥300, Adepto ≥400 (ver nota de tensão no rodapé)

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 9 |
| ⬜ pendente | 0 |
| ➖ não precisa | 1 |
| ✅ feita | 8 |
| % concluído | 100% (8/9 com M1; ver nota 06) |

> Gaps concentrados em **M1 (mídia)** nas 9 notas. No diagnóstico original, só 06-08
> (Iniciado) tinham isenção de M1 por fase; 09-14 (Adepto) não tinham, mas 10-14 ficaram
> `➖` porque M1 nunca foi item de núcleo do checklist. **A isenção por fase foi revogada
> em 2026-07-28** (Task 11): M1 é agora obrigatório em toda nota, de qualquer fase. Notas
> 07, 10, 11, 12, 13 e 14 receberam mídia verificada e ficam `✅`. **Nota 06 é a única
> exceção**: nenhuma mídia verificável e pertinente foi encontrada após busca extensiva —
> fica `➖` por buraco honesto, não por isenção de política. Nota 09 já era `✅` (L2 e M1
> resolvidos antes desta task). Nota 08 é `✅` por desvio de julgamento documentado
> (nota-espinha do domínio), já resolvido antes desta task.

---

## Notas

#### 06 - Generativa vs avaliativa   [mecânico]
- **Enriquecimento:** ➖ não precisa (buraco honesto — ver abaixo)
- **Estado:** 132 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** M1 (ausente — o `[!tip]` existente na nota cita um livro — Erika Hall, *Just Enough Research* — não vídeo/podcast; M1 agora obrigatório sob a política de 2026-07-28, sem isenção de fase); P1 N/A (nota conceitual, sem seção de código)
- **Score:** 11/12
- **Plano de execução (Task 11, 2026-07-28):**
  - Buscar vídeo/podcast verificável sobre generativa vs. avaliativa — resolveria M1
- **Resultado:** ⚠️ Busca extensiva (WebSearch + yt-dlp em múltiplos candidatos: NN/g "5 Qualitative Research Methods", Erika Hall "Design Research Done Right", "Conducting Generative and Evaluative Research for the Visually Impaired") não encontrou vídeo/podcast verificável e diretamente pertinente ao tema específico desta nota. Nenhum link fraco foi forçado — nota permanece sem mídia. Candidato a revisitar em enriquecimento futuro.
#### 07 - Entrevista de descoberta - as regras do Mom Test   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-28, Task 11 — retrofit M1)
- **Estado:** 127 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** M1 resolvido; P1 N/A (nota conceitual, sem seção de código)
- **Score:** 12/12
- **Plano de execução:**
  - — nenhuma (M1 já resolvido)
- **Resultado:** ✅ Callout `[!tip]` adicionado com o vídeo "The Mom Test with Rob Fitzpatrick" (Brian Rhea, 56min) — https://www.youtube.com/watch?v=Az-KSGBECH8 — verificado via yt-dlp (transcrição confirma discussão da *compliment trap* e do livro). M1 resolvido.
#### 08 - Cliente não é usuário - a armadilha do B2B e consultoria   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-28)
- **Estado:** 124 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** M1 (ausente — sem callout `[!tip]` com vídeo/podcast; recomendado, não obrigatório na fase Iniciado, mas esta é uma das duas notas-espinha do domínio UX sobre o conflito "quem paga aprova, quem usa sofre" — pesa a favor de incluir mesmo assim)
- **Score:** 11/12
- **Plano de execução:**
  - Pesquisar e adicionar 1 callout `[!tip]` com link para vídeo ou podcast sobre pesquisa com stakeholder vs. usuário real em contexto B2B/consultoria (ex.: discovery com cliente pagante vs. operador final) — resolve M1. Desvio: incluído por julgamento — nota-espinha do domínio, mesmo tratamento dado à nota-manifesto 01 do roadmap irmão "Fundamentos e Modelo Mental"
- **Resultado:** ✅ Callout `[!tip]` adicionado citando o episódio "Product Discovery: B2B vs. B2C" (All Things Product Podcast, Teresa Torres e Petra Wille) — https://www.producttalk.org/product-discovery-b2b-vs-b2c-all-things-product-podcast-with-teresa-torres-petra-wille/ — verificado via WebFetch. M1 resolvido; nenhuma outra alteração na nota.
#### 09 - Jobs To Be Done - as duas escolas   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-28)
- **Estado:** 138 linhas reais · fase: Adepto · status: seedling
- **Núcleo/gaps:** L2 (ausente — seção `## Fontes` cita Ulwick/Christensen/Moesta só por nome, sem nenhum link externo verificável/URL); M1 (ausente — sem callout `[!tip]` com vídeo/podcast; M1 sem isenção nesta fase — Adepto)
- **Score:** 10/12
- **Plano de execução:**
  - Adicionar ≥1 link externo verificável (URL) na seção `## Fontes` — ex.: artigo/página oficial sobre Outcome-Driven Innovation de Ulwick, ou referência ao livro *The Innovator's Solution* — resolve L2
  - Pesquisar e adicionar callout `[!tip]` com vídeo/podcast relevante sobre JTBD/switch interview — resolve M1
- **Resultado:** ✅ URLs adicionadas em Fontes (Strategyn — https://strategyn.com/jobs-to-be-done/ — e Google Books/The Innovator's Solution — https://books.google.com/books/about/The_Innovator_s_Solution.html?id=I5nBAgAAQBAJ), resolvendo L2. Callout `[!tip]` adicionado com o podcast "The Jobs-to-be-Done Mattress Interview" (jobstobedone.org, Bob Moesta e Chris Spiek) — https://jobstobedone.org/radio/the-mattress-interview-part-one/ — resolvendo M1. Ambas as fontes verificadas via WebFetch.
#### 10 - Opportunity Solution Tree de bolso   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-28, Task 11 — retrofit M1)
- **Estado:** 127 linhas reais · fase: Adepto · status: seedling
- **Núcleo/gaps:** M1 resolvido; P1 N/A (nota conceitual, sem seção de código)
- **Score:** 12/12
- **Plano de execução:**
  - — nenhuma (M1 já resolvido)
- **Resultado:** ✅ Callout `[!tip]` adicionado com o vídeo "Talking Methods: Driving better outcomes with Teresa Torres' OST" (Mural, 14min52, com a própria Teresa Torres) — https://www.youtube.com/watch?v=hHzsau3t_zY — verificado via yt-dlp. M1 resolvido.
#### 11 - Assumption mapping   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-28, Task 11 — retrofit M1)
- **Estado:** 133 linhas reais · fase: Adepto · status: seedling
- **Núcleo/gaps:** M1 resolvido; P1 N/A (nota conceitual, sem seção de código)
- **Score:** 12/12
- **Plano de execução:**
  - — nenhuma (M1 já resolvido)
- **Resultado:** ✅ Callout `[!tip]` adicionado com o vídeo "Testing Business Ideas: Assumptions Mapping Webinar" (David J Bland, 38min) — https://www.youtube.com/watch?v=Am598Cbq5gU — verificado via yt-dlp. M1 resolvido.
#### 12 - Proto-persona vs persona de verdade   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-28, Task 11 — retrofit M1)
- **Estado:** 121 linhas reais · fase: Adepto · status: seedling
- **Núcleo/gaps:** M1 resolvido
- **Score:** 12/12
- **Plano de execução:**
  - — nenhuma (M1 já resolvido)
- **Resultado:** ✅ Callout `[!tip]` adicionado com o vídeo "Proto Personas" (Samhita Tankala, NN/g, 3min) — https://www.nngroup.com/videos/proto-personas/ — verificado via WebFetch. M1 resolvido.
#### 13 - Teste de usabilidade guerrilha com 5 usuários   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-28, Task 11 — retrofit M1)
- **Estado:** 130 linhas reais · fase: Adepto · status: seedling
- **Núcleo/gaps:** M1 resolvido
- **Score:** 12/12
- **Plano de execução:**
  - — nenhuma (M1 já resolvido)
- **Resultado:** ✅ Callout `[!tip]` adicionado com o vídeo "Usability Testing w. 5 Users: Design Process" (Jakob Nielsen, NN/g, 4min) — https://www.nngroup.com/videos/usability-testing-w-5-users-design-process/ — verificado via WebFetch. M1 resolvido.
#### 14 - Personas sintéticas e síntese por IA   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-28, Task 11 — retrofit M1)
- **Estado:** 130 linhas reais · fase: Adepto · status: seedling
- **Núcleo/gaps:** M1 resolvido. Restrição vinculante da spec do domínio permanece: não reintroduzir os percentuais 69%/88% nem a citação apócrifa de Ford em nenhum enriquecimento futuro.
- **Score:** 12/12
- **Plano de execução:**
  - — nenhuma (M1 já resolvido)
- **Resultado:** ✅ Callout `[!tip]` adicionado com o vídeo "Synthetic User Research Explained | How AI Is Changing UX" (UX India, 22min11, entrevista com Sonal, product designer) — https://www.youtube.com/watch?v=o3Ex5o8ewUM — verificado via yt-dlp. Contraponto prático (não endosso) ao ceticismo central da nota — registrado explicitamente no callout. M1 resolvido.
