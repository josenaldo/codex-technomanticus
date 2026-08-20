---
title: "Roadmap — UX"
created: 2026-07-28
updated: 2026-07-29
type: meta
publish: false
tags:
  - meta
  - roadmap
  - ux
---

# Roadmap — UX

Roadmap do domínio `03-Dominios/Engenharia/UX` (raiz de domínio / galho-pai). Rastreia o **estado dos 8 sub-galhos + capstone**. Domínio recém-estruturado (scaffold) em 2026-07-28. Fonte do roster: `index.md` + [[00-Meta/specs/2026-07-28-dominio-ux-design|design 2026-07-28]] + plano em `.superpowers/sdd/2026-07-28-dominio-ux-plano/`. SG1 fechado (5/5 escritas + enriquecidas) em 2026-07-28. SG2 fechado (9/9 escritas + diagnosticadas + enriquecidas) em 2026-07-28. SG4 fechado (7/7 escritas + diagnosticadas, 0 gaps de núcleo) em 2026-07-28. SG6 fechado (5/5 escritas + diagnosticadas, 0 gaps de núcleo) em 2026-07-28. SG5 fechado (7/7 escritas + diagnosticadas, 0 gaps de núcleo, 1 buraco honesto de M1 na nota 31) em 2026-07-28. SG3 fechado (4/4 escritas + diagnosticadas, 0 gaps de núcleo, 1 buraco honesto de M1 na nota 16) em 2026-07-29. SG7 fechado (8/8 escritas + diagnosticadas, 0 gaps de núcleo, 1 buraco honesto de M1 na nota 43) em 2026-07-29. SG8 fechado (3/3 escritas + diagnosticadas, 0 gaps de núcleo, 0 buracos de M1 — primeiro sub-galho Magus sem exceção) em 2026-07-29, fechando o domínio principal (48/48 notas dos 8 sub-galhos). Capstone escrito em 2026-07-29, **fechando o domínio inteiro (49/49 notas)**; galho-irmão Ferramentas de Design fechado no mesmo dia (9/9) — par completo em **58 notas**.

**Nível:** raiz de domínio (contém sub-galhos).

> [!info] Política de M1 obrigatório (2026-07-28, Task 11)
> A partir de 2026-07-28, **M1 (mídia verificada — vídeo ou podcast) é obrigatória em toda nota deste domínio**, alinhando ao padrão de `Tecnologia/Acessibilidade` (21/21 notas com vídeo). Isso sobrepõe qualquer isenção de M1 por `fase:` usada em diagnósticos anteriores (`/diagnosticar-galho`, `/verificar-nota`) — **uma nota sem mídia verificada não fecha**. Retrofit aplicado às 14 notas de SG1 e SG2 já escritas: 13/14 receberam mídia; a nota 06 (Descoberta e Pesquisa) ficou sem mídia por buraco honesto — nenhum vídeo/podcast verificável e pertinente foi encontrado. Ver os roadmaps de SG1 e SG2 e `03-Dominios/Engenharia/UX/index.md` para o texto da regra.

**Legenda de estado:** ✅ completo (escrito + enriquecido) · 🔶 em construção · 📋 desenhado, não iniciado · ⬜ só esboçado no design · `%` = notas escritas / total.

## Notas diretas (logo abaixo desta pasta)

| Nota | Tipo | Estado |
|------|------|--------|
| `index.md` | MOC | ➖ não precisa |
| `roadmap.md` | Roadmap | ➖ não precisa |
| [[03-Dominios/Engenharia/UX/49 - Capstone - do requisito ao produto validado\|Capstone — Do requisito ao produto validado]] | Capstone | ✅ escrito (2026-07-29) — sem M1, pendência reabrível (cota de busca esgotada; ver callout na nota) |

## Sub-galhos — ordem canônica (SG1..SG8)

| # | Sub-galho | Notas | Escritas | % | Fase | Estado |
|---|-----------|------:|---------:|--:|------|--------|
| 1 | Fundamentos e Modelo Mental | 5 | 5 | 100% | Iniciado | ✅ completo |
| 2 | Descoberta e Pesquisa | 9 | 9 | 100% | Iniciado/Adepto | ✅ completo |
| 3 | Arquitetura de Informação | 4 | 4 | 100% | Adepto | ✅ completo |
| 4 | Design de Interação | 7 | 7 | 100% | Adepto | ✅ completo |
| 5 | Linguagem Visual e Design System | 7 | 7 | 100% | Adepto/Magus | ✅ completo |
| 6 | UX Writing e Content Design | 5 | 5 | 100% | Adepto | ✅ completo |
| 7 | Medir, Validar e Sustentar | 8 | 8 | 100% | Magus | ✅ completo |
| 8 | Ética e Ofício | 3 | 3 | 100% | Magus | ✅ completo |

## Ordem de execução planejada

A ordem de execução **não é** a ordem de numeração acima. Sequência escolhida no design (2026-07-28):

**SG1 → SG2 → SG4 → SG6 → SG5 → SG3 → SG7 → SG8 → Ferramentas de Design → capstone.**

Justificativa: SG2, SG4 e SG6 vêm cedo porque são o que se usa no próximo projeto; SG7 vem depois porque é o que sustenta entrevista; `Tecnologia/Ferramentas de Design` vem por último porque é a parte mais perecível do par de galhos — quanto mais tarde for escrita, mais tempo de validade terá; o capstone fecha o domínio.

| Ordem de execução | Sub-galho | Ordem canônica |
|---|---|---|
| 1 | Fundamentos e Modelo Mental | SG1 |
| 2 | Descoberta e Pesquisa | SG2 |
| 3 | Design de Interação | SG4 |
| 4 | UX Writing e Content Design | SG6 |
| 5 | Linguagem Visual e Design System | SG5 |
| 6 | Arquitetura de Informação | SG3 |
| 7 | Medir, Validar e Sustentar | SG7 |
| 8 | Ética e Ofício | SG8 |
| 9 | *(galho irmão)* [[03-Dominios/Tecnologia/Ferramentas de Design/roadmap\|Ferramentas de Design]] | — |
| 10 | Capstone — Do requisito ao produto validado | — |

Ao fechar um sub-galho (semear + enriquecer até ✅), abrir o próximo nesta ordem — não na ordem canônica da tabela acima. Ritmo: galho a galho, ponta a ponta, para manter o contexto leve por sessão.

## Tabela-resumo (agregado)

| Métrica | Valor |
|---------|-------|
| Sub-galhos | 8 |
| ✅ completos | 8 |
| 🔶 em construção | 0 |
| 📋 desenhados, não iniciados | 0 |
| Notas totais (8 sub-galhos + capstone) | 48 + 1 = **49** |
| Notas escritas | 49 (100%) |

---

## Próximos passos

1. ✅ Scaffold do domínio (este roadmap + `index.md` + 8 `index.md` de sub-galho + galho `Ferramentas de Design`) — Task 0, 2026-07-28.
2. ✅ **SG1 — Fundamentos e Modelo Mental:** 5/5 notas escritas + enriquecidas (2 substantivo, 3 sem gap de núcleo). Ver [[03-Dominios/Engenharia/UX/Fundamentos e Modelo Mental/roadmap|roadmap do sub-galho]] — Task 1, 2026-07-28.
3. ✅ **SG2 — Descoberta e Pesquisa:** 9/9 notas escritas + diagnosticadas + enriquecidas (2 substantivo — notas 08 e 09 —, 7 sem gap de núcleo). Ver [[03-Dominios/Engenharia/UX/Descoberta e Pesquisa/roadmap|roadmap do sub-galho]] — Task 2, 2026-07-28.
4. ✅ **SG4 — Design de Interação:** 7/7 notas escritas + diagnosticadas (0 gaps de núcleo, 7 `➖ não precisa`, scores 11-12/12). Ver [[03-Dominios/Engenharia/UX/Design de Interação/roadmap|roadmap do sub-galho]] — Task 3, 2026-07-28.
5. ✅ **SG6 — UX Writing e Content Design:** 5/5 notas escritas + diagnosticadas (0 gaps de núcleo, 5 `➖ não precisa`, score 12/12 em todas). Ver [[03-Dominios/Engenharia/UX/UX Writing e Content Design/roadmap|roadmap do sub-galho]] — Task 4, 2026-07-28.
6. ✅ **SG5 — Linguagem Visual e Design System:** 7/7 notas escritas + diagnosticadas (0 gaps de núcleo, 7 `➖ não precisa`, score 11-12/12 — nota 31 fica em 11/12 por buraco honesto de M1, documentado e aceito). Ver [[03-Dominios/Engenharia/UX/Linguagem Visual e Design System/roadmap|roadmap do sub-galho]] — Task 5, 2026-07-28.
7. ✅ **SG3 — Arquitetura de Informação:** 4/4 notas escritas + diagnosticadas (0 gaps de núcleo, 4 `➖ não precisa`, score 11-12/12 — nota 16 fica em 11/12 por buraco honesto de M1, documentado e aceito; interseção de nicho UX/dados sem material dedicado verificável). Duração de vídeo da nota 17 corrigida (era "~4min", real 2:31, conferida via `yt-dlp`). Ver [[03-Dominios/Engenharia/UX/Arquitetura de Informação/roadmap|roadmap do sub-galho]] — Task 6, 2026-07-29.
8. ✅ **SG7 — Medir, Validar e Sustentar:** 8/8 notas escritas + diagnosticadas (0 gaps de núcleo, 8 `➖ não precisa`, score 11-12/12 — nota 43 fica em 11/12 por buraco honesto de M1, documentado e aceito; busca extensiva não encontrou vídeo verificável sobre os limites de session replay/heatmap além de conteúdo promocional de ferramenta comercial). Segunda nota-espinha do domínio (nota 42, tráfego baixo/B2B como condição estrutural) tratada com tom de método, não consolo. Ver [[03-Dominios/Engenharia/UX/Medir, Validar e Sustentar/roadmap|roadmap do sub-galho]] — Task 7, 2026-07-29.
9. ✅ **SG8 — Ética e Ofício:** 3/3 notas escritas + diagnosticadas (0 gaps de núcleo, 3 `➖ não precisa`, score 12/12 em todas — 0 buracos de M1, primeiro sub-galho Magus do domínio sem exceção documentada). Duas correções pontuais aplicadas na nota 46 (contagem de executivos nomeados pela FTC no caso Amazon, de três para dois — Neil Lindsay/SVP e Jamil Ghani/VP, verificado contra o acordo final da FTC; e um "already" residual em português). Ver [[03-Dominios/Engenharia/UX/Ética e Ofício/roadmap|roadmap do sub-galho]] — Task 8, 2026-07-29. **Fecha os 8 sub-galhos do domínio principal (48/48).** Próximo da ordem de execução → galho irmão **Ferramentas de Design**.
10. ✅ [[03-Dominios/Tecnologia/Ferramentas de Design/roadmap|Ferramentas de Design]] (9/9 notas, galho fechado) — por último entre os galhos, por ser o mais perecível.
11. ✅ Capstone — **[[03-Dominios/Engenharia/UX/49 - Capstone - do requisito ao produto validado|Do requisito ao produto validado]]** (2026-07-29) — fecha o domínio. **Domínio UX COMPLETO: 49/49 notas (8 sub-galhos + capstone) + Ferramentas de Design 9/9 = 58 notas no par de galhos.** Único ponto em aberto: M1 do capstone é uma pendência reabrível (busca de mídia não realizada por cota de `WebSearch` esgotada), distinta dos 4 buracos honestos de busca real concluída (notas 06, 16, 31, 43).
