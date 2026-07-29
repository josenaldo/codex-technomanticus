---
title: "Roadmap — Arquitetura de Informação"
created: 2026-07-29
type: meta
publish: false
tags:
  - meta
  - roadmap
---

# Roadmap — Arquitetura de Informação

Diagnóstico nota a nota. Cada entrada tem estado de enriquecimento, score, classificação
de custo e plano de execução acionável. Gerado por `/diagnosticar-galho`, a partir da
auditoria já registrada em `.superpowers/sdd/2026-07-28-dominio-ux-plano/task-6-report.md`
(gate `/verificar-nota` rodado manualmente nota a nota na Task 6, rodada de escrita) —
confirmada por amostragem nesta rodada (Task 6, Passos D–F): contagem de linhas real
(`wc -l`), validador `validar-mermaid.mjs` (4/4 blocos ok) e resolução em disco (`test -f`)
dos 7 wikilinks cross-galho, todos conferidos diretamente nesta rodada.

**Galho:** `03-Dominios/Engenharia/UX/Arquitetura de Informação`
**Diagnóstico:** 2026-07-29
**Última execução:** 2026-07-29 — **diagnóstico COMPLETO, enriquecimento não necessário (4/4 ➖)**

> [!info] Política de M1 obrigatório (herdada do domínio, 2026-07-28, Task 11) — com uma exceção documentada
> M1 (mídia verificada — vídeo ou podcast) é **obrigatória em toda nota** deste domínio, sem
> isenção por `fase:`. **3 das 4 notas** deste sub-galho (15, 17, 18) têm mídia verificada por
> transcrição completa (`yt-dlp`, legenda lida por inteiro, não só título). **A nota 16
> (Schema de banco não é estrutura de navegação) é exceção documentada e aceita**: buscas
> dirigidas por talk/vídeo sobre o contraste exato "schema de banco relacional vs. estrutura
> de navegação" não retornaram candidato verificável — o tema é interseção de nicho entre UX
> e engenharia de dados, sem material dedicado no YouTube. O buraco é reportado na própria
> nota (não escondido). **Decisão do usuário registrada (2026-07-28/29): buracos de mídia
> seguem em julgamento caso a caso, sem teto numérico** — nenhuma mídia fraca foi forçada na
> nota 16, e ela não é marcada como pendente por causa disso. Se aparecer candidato
> verificável no futuro, reabrir com `/adicionar-midia`.

> [!info] Âncora de profundidade é o SG1 (não o bloco anterior)
> Por decisão do plano (2026-07-28), o piso qualitativo de comparação é sempre o SG1
> (Fundamentos e Modelo Mental), nunca o bloco imediatamente anterior — evita erosão gradual.
> Piso qualitativo: ≥3 casos práticos por nota + recorte em prosa ("praticável sozinho vs.
> exige time"). As 4 notas do SG3 atendem a isso desde a primeira rodada (Task 6), sem
> correção adicional necessária. Fronteiras preservadas: nota 15 → nota 34 (SG6, glossário/
> rotulação); nota 16 → `Ciência/Banco de Dados` (modelagem) e `Engenharia/Dados` — como
> **contraste**, sem reexplicar modelagem; nota 17 → nota 13 (SG2, teste de guerrilha), mesmo
> espírito de método leve; nota 18 → nota 04 (SG1, Jakob's Law) e notas 19/22 (SG4, user flow
> e modal empilhado).

> [!info] Piso de linhas — desvio documentado
> `verificar-nota` cobra T2 (Adepto ≥400 linhas) como item de score. Este domínio segue
> `00-Meta/guia/Convenções de escrita.md`: "Comprimento não é meta — é consequência. Não
> existe piso de linhas". As 4 notas ficam em **121–130 linhas** (30%–33% do piso nominal
> T2) — abaixo do piso nominal, na mesma faixa do SG1 aprovado (138–187), SG4 (115–137), SG5
> (115–162) e SG6 (125–147), mesmo desvio já registrado nesses sub-galhos. T2 é tratado como
> não-bloqueante neste diagnóstico; densidade (casos práticos concretos, mecanismo explicado
> "em uma frase", armadilhas com causa e correção), não contagem de linhas, é o critério real.
> Ver `task-6-report.md` para a tabela nota → score → mídia → verificação desta rodada.

> [!info] Correção pontual — duração de vídeo (nota 17)
> Revisão anterior (achado da rodada de review do SG6) apontou que uma duração de vídeo
> citada de forma imprecisa num callout é o tipo de erro que este domínio não tolera ("não
> afirmar o não-verificado"). Na nota 17, o vídeo da Optimal Workshop estava citado como
> "~4min"; conferido nesta rodada via `yt-dlp --print duration_string` → **2:31**. Corrigido
> na nota antes deste diagnóstico.

## Régua de análise

Checklist `verificar-nota` — 12 itens (isenções por fase/tipo/broto aplicadas por nota):

| Grupo | Itens |
|-------|-------|
| ESTRUTURA | E1 TL;DR · E2 Abertura-problema · E3 Mermaid · E4 Casos práticos · E5 O que vem a seguir · E6 Inglês · E7 Tabela PT↔EN · E8 Armadilhas [!warning] |
| PROFUNDIDADE | P1 Código-com-falha · P2 Mecanismo explicado |
| LINKS | L1 Wikilink cross-galho · L2 Referência externa (URL) |
| MÍDIA | M1 Vídeo/podcast embutido |

**Esquema de `fase:` detectado:** COM fase (Adepto 15–18)
**Piso de linhas:** T2 nominal tratado como não-bloqueante — ver desvio documentado acima.

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 4 |
| ⬜ pendente | 0 |
| ➖ não precisa | 4 |
| ✅ feita | 0 |
| % concluído | 100% |

> Diagnóstico concluído em 2026-07-29: as 4 notas já atendem ao núcleo completo (E1-E8, P2,
> L1, L2; M1 em 3/4, buraco honesto na nota 16; P3 N/A por serem `fase: Adepto`) — nenhuma
> entra no loop de execução do `enriquecer-galho`. `% concluído` conta `➖ não precisa` como
> concluído (nada a fazer), não `✅ feita` (nenhuma execução foi disparada, pois não havia
> gap de núcleo).

---

## Notas

#### 15 - Os 4 sistemas da AI   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 121 linhas · fase: Adepto · status: seedling
- **Núcleo/gaps:** — (T2 nominal não atingido — 121 vs. 400 — desvio aceito, ver callout acima). Linka nota 34 (SG6, rotulação/glossário) e nota 17 (mesmo sub-galho, reestruturação em produção).
- **Score:** 12/12 (P1 N/A — nota conceitual, sem seção de código; P3 N/A — fase Adepto). M1: [Donna Spencer — *IA and sitemaps*](https://www.youtube.com/watch?v=SjbQ21klQP8), legenda manual EN baixada via `yt-dlp` e lida por completo (224 linhas) — cobre esquemas de organização, hierarquia rasa/profunda, "desenhe o sitemap antes da navegação".
- **Plano de execução:**
  - nenhuma
- **Resultado:** —
#### 16 - Schema de banco não é estrutura de navegação   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 124 linhas · fase: Adepto · status: seedling
- **Núcleo/gaps:** **M1 ausente — buraco honesto, ver política acima.** Isento de bloqueio: buscas dirigidas (`site:youtube.com`, talks sobre "database schema vs navigation") não retornaram vídeo/palestra específico e verificável sobre o contraste exato; documentado na própria nota, nenhum link fraco forçado. Fronteira respeitada: linka `[[03-Dominios/Ciência/Banco de Dados/04 - Modelagem e normalização]]` e `[[03-Dominios/Engenharia/Dados/index]]` como contraste, sem reexplicar modelagem — confirmado por leitura direta (linhas 120-121).
- **Score:** 11/12 (M1 ausente, documentado; P1 N/A — nota conceitual; P3 N/A — fase Adepto)
- **Plano de execução:**
  - nenhuma — buraco de M1 é aceito como exceção documentada (interseção de nicho UX/dados, sem material dedicado verificável), não como gap a fechar por força; decisão do usuário: sem teto numérico de buracos de mídia
- **Resultado:** —
#### 17 - Card sorting e tree testing de guerrilha   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 124 linhas · fase: Adepto · status: seedling
- **Núcleo/gaps:** — (T2 nominal não atingido — 124 vs. 400 — desvio aceito, ver callout acima). Linka nota 13 (SG2, teste de usabilidade guerrilha), mesmo espírito de método leve. **Duração de vídeo corrigida nesta rodada** (era "~4min", real 2:31 — ver callout de correção pontual acima).
- **Score:** 12/12 (P1 N/A — nota conceitual; P3 N/A — fase Adepto). M1: [Optimal Workshop — *Card sorting and tree testing: how do they work together?*](https://www.youtube.com/watch?v=cSHiu_m6vCs), legenda automática EN baixada via `yt-dlp` e lida por completo (65 linhas) — confirma open/closed card sort, tree test como "reverse card sorting", ordem card-sort-primeiro/tree-test-depois. Duração real 2:31 (`yt-dlp --print duration_string`), conferida e corrigida nesta rodada.
- **Plano de execução:**
  - nenhuma
- **Resultado:** —
#### 18 - Navegação e wayfinding   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 130 linhas · fase: Adepto · status: seedling
- **Núcleo/gaps:** — (T2 nominal não atingido — 130 vs. 400 — desvio aceito, ver callout acima). Linka nota 04 (SG1, Jakob's Law) e notas 19/22 (SG4, user flow e modal empilhado) — confirmado por leitura direta.
- **Score:** 12/12 (P1 N/A — nota conceitual; P3 N/A — fase Adepto). M1: [Kathryn Whitenton (NN/g) — *Digital Wayfinding*](https://www.youtube.com/watch?v=pXaPeJTit7o), legenda manual EN baixada via `yt-dlp` e lida por completo — cita Kevin Lynch/*Image of the City* (1960) nominalmente, traduz distritos/marcos/nós para header, logo/home link, menus.
- **Plano de execução:**
  - nenhuma
- **Resultado:** —
