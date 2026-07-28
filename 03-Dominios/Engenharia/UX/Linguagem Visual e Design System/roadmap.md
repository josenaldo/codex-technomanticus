---
title: "Roadmap — Linguagem Visual e Design System"
created: 2026-07-28
type: meta
publish: false
tags:
  - meta
  - roadmap
---

# Roadmap — Linguagem Visual e Design System

Diagnóstico nota a nota. Cada entrada tem estado de enriquecimento, score, classificação
de custo e plano de execução acionável. Gerado por `/diagnosticar-galho`, a partir da
auditoria já registrada em `.superpowers/sdd/2026-07-28-dominio-ux-plano/task-5-report.md`
(gate `/verificar-nota` rodado manualmente nota a nota na Task 5, rodada de escrita) —
confirmada por amostragem nesta rodada (Task 5, Passos D–F): estrutura de seções, wikilinks,
callouts de precisão e fronteiras conferidos linha a linha nas 7 notas.

**Galho:** `03-Dominios/Engenharia/UX/Linguagem Visual e Design System`
**Diagnóstico:** 2026-07-28
**Última execução:** 2026-07-28 — **diagnóstico COMPLETO, enriquecimento não necessário (7/7 ➖)**

> [!info] Política de M1 obrigatório (herdada do domínio, 2026-07-28, Task 11) — com uma exceção documentada
> M1 (mídia verificada — vídeo ou podcast) é **obrigatória em toda nota** deste domínio, sem
> isenção por `fase:`. **6 das 7 notas** deste sub-galho (26–30, 32) têm mídia verificada por
> transcrição completa (não só título). **A nota 31 (Component API design) é exceção
> documentada e aceita**: pesquisa real (~6 queries — talks de API design de componente
> framework-neutras, boolean trap, compound components) não encontrou candidato que
> passasse no critério de verificação sem violar a restrição desta nota de não ser "nota de
> React". O buraco é reportado na própria nota (callout `[!info]` dedicado), não escondido.
> Um link fraco (tutorial React-específico) seria pior que o buraco — decisão preservada
> nesta rodada, sem forçar mídia. Se aparecer candidato verificável e framework-neutro no
> futuro, reabrir com `/adicionar-midia`.

> [!info] Âncora de profundidade é o SG1 (não o bloco anterior)
> Por decisão do plano (2026-07-28), o piso qualitativo de comparação é sempre o SG1
> (Fundamentos e Modelo Mental), nunca o bloco imediatamente anterior — evita erosão gradual.
> Piso qualitativo: ≥3 casos práticos por nota + recorte em prosa ("praticável sozinho vs.
> exige time"). As 7 notas do SG5 atendem a isso desde a primeira rodada (Task 5), sem
> correção adicional necessária. Duas notas (26, 28) linkam explicitamente de volta à nota
> 05 do SG1 ("Gestalt aplicada a UI") como a base perceptiva que este sub-galho aplica, sem
> reexplicar.

> [!info] Piso de linhas — desvio documentado
> `verificar-nota` cobra T2 (Adepto ≥400 linhas) / T3 (Magus ≥500) como item de score. Este
> domínio segue `00-Meta/guia/Convenções de escrita.md`: "Comprimento não é meta — é
> consequência. Não existe piso de linhas". As 7 notas ficam em **115–162 linhas** (29%–41%
> do piso T2 nominal para as três primeiras, ainda menor fração do T3 nominal para as
> quatro `Magus`) — abaixo do piso nominal, na mesma faixa do SG1 aprovado (138–187), SG4
> (115–137) e SG6 (125–147), mesmo desvio já registrado nesses sub-galhos. T2/T3 são
> tratados como não-bloqueantes neste diagnóstico; densidade (contagem de palavras, casos
> práticos concretos, mecanismo explicado, armadilhas com causa e correção), não contagem de
> linhas, é o critério real. Ver `task-5-report.md` para a comparação de densidade
> palavra-a-palavra contra a nota-âncora do SG1.

## Régua de análise

Checklist `verificar-nota` — 12 itens (isenções por fase/tipo/broto aplicadas por nota):

| Grupo | Itens |
|-------|-------|
| ESTRUTURA | E1 TL;DR · E2 Abertura-problema · E3 Mermaid · E4 Casos práticos · E5 O que vem a seguir · E6 Inglês · E7 Tabela PT↔EN · E8 Armadilhas [!warning] |
| PROFUNDIDADE | P1 Código-com-falha · P2 Mecanismo explicado |
| LINKS | L1 Wikilink cross-galho · L2 Referência externa (URL) |
| MÍDIA | M1 Vídeo/podcast embutido |

**Esquema de `fase:` detectado:** COM fase (Adepto 26–28 / Magus 29–32)
**Piso de linhas:** T2/T3 nominal tratado como não-bloqueante — ver desvio documentado acima.

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 7 |
| ⬜ pendente | 0 |
| ➖ não precisa | 7 |
| ✅ feita | 0 |
| % concluído | 100% |

> Diagnóstico concluído em 2026-07-28: as 7 notas já atendem ao núcleo completo (E1-E8, P2,
> L1, L2; M1 em 6/7, buraco honesto na nota 31; P3 em 29-32 por serem `fase: Magus`) —
> nenhuma entra no loop de execução do `enriquecer-galho`. `% concluído` conta `➖ não
> precisa` como concluído (nada a fazer), não `✅ feita` (nenhuma execução foi disparada,
> pois não havia gap de núcleo).

---

## Notas

#### 26 - Hierarquia visual   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 115 linhas · fase: Adepto · status: seedling
- **Núcleo/gaps:** — (T2 nominal não atingido — 115 vs. 400 — desvio aceito, ver callout acima). Linka explicitamente `Fundamentos e Modelo Mental/05 - Gestalt aplicada a UI` (SG1) como base perceptiva.
- **Score:** 12/12 (P1 N/A — nota conceitual, sem seção de código; P3 isento — fase Adepto). M1: [Visual Hierarchy (NN/g)](https://www.youtube.com/watch?v=8OTbyWndY9M), transcrição lida integralmente.
- **Plano de execução:**
  - nenhuma
- **Resultado:** —
#### 27 - Escalas de tipografia, espaçamento e densidade   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 150 linhas · fase: Adepto · status: seedling
- **Núcleo/gaps:** — (T2 nominal não atingido — 150 vs. 400 — desvio aceito, ver callout acima)
- **Score:** 12/12 (P1 N/A — nota conceitual; P3 isento — fase Adepto). M1: [Creating Type Scales for a Design System](https://www.youtube.com/watch?v=nGv9iDuV09c), com callout honesto de cobertura parcial (só metade tipográfica do tema, não espaçamento/densidade).
- **Plano de execução:**
  - nenhuma
- **Resultado:** —
#### 28 - Cor de produto: OKLCH e paleta semântica   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 137 linhas · fase: Adepto · status: seedling
- **Núcleo/gaps:** — (T2 nominal não atingido — 137 vs. 400 — desvio aceito, ver callout acima). Fronteira respeitada: contraste apontado para `Acessibilidade/Construir Acessível/11` (WCAG 4.5:1/3:1, sem recalcular), paleta de dados apontada para a skill `dataviz` — sem duplicar.
- **Score:** 12/12 (P1 presente — trecho com código OKLCH; P3 isento — fase Adepto). M1: [Why everyone is talking about OKLCH](https://www.youtube.com/watch?v=kVi9Augt7HY), transcrição lida, trecho âncora [0:21] conferido.
- **Plano de execução:**
  - nenhuma
- **Resultado:** —
#### 29 - Design tokens como sistema   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 146 linhas · fase: Magus · status: seedling
- **Núcleo/gaps:** — (T3 nominal não atingido — 146 vs. 500 — desvio aceito, ver callout acima). Fronteira respeitada: mecânica de custom properties apontada para `CSS/07`, aqui só a arquitetura de camadas (primitivo→semântico→componente). Style Dictionary citado e apontado para `Tooling e Build`, não desenvolvido. **Callout `[!warning]` dedicado preserva a precisão factual: DTCG é Community Group Report, não padrão W3C Standards Track** — confirmado nesta rodada por leitura direta do texto da nota.
- **Score:** 12/12 (P1 presente — JSON de token; P3 presente — conecta indireção de tokens a arquitetura de software, exigido por fase Magus). M1: [DTCG W3C release... (Schema by Figma 2025)](https://www.youtube.com/watch?v=XI8cjfw8rt8), transcrição lida; vídeo usado para reforçar, não contradizer, a ressalva.
- **Plano de execução:**
  - nenhuma
- **Resultado:** —
#### 30 - Atomic Design: o que ainda vale   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 119 linhas · fase: Magus · status: seedling
- **Núcleo/gaps:** — (T3 nominal não atingido — 119 vs. 500 — desvio aceito, ver callout acima)
- **Score:** 12/12 (P1 N/A — nota conceitual; P3 presente — conecta à origem da metáfora química e à autocrítica do próprio Brad Frost, exigido por fase Magus). M1: [Is Atomic Design Dead? — SmashingConf NY 2024 (Brad Frost)](https://www.youtube.com/watch?v=-3Pji_frbII), transcrição lida (trecho âncora [11:59]).
- **Plano de execução:**
  - nenhuma
- **Resultado:** —
#### 31 - Component API design   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 162 linhas · fase: Magus · status: seedling
- **Núcleo/gaps:** **M1 ausente — buraco honesto, ver política acima.** Isento de bloqueio: pesquisa real documentada (~6 queries) em callout `[!info]` na própria nota; nenhum link fraco forçado. L1 corrigido antes do commit original (adicionado `[[03-Dominios/Tecnologia/React/Design Patterns/07 - Compound components]]`) — confirmado presente nesta rodada (linha 97 da nota, mais link para a nota 32 na linha 157). Evita ser "nota de React": compound components apresentado como princípio (mesma lógica de `<select>`/`<option>` em HTML), implementação React só linkada, não desenvolvida.
- **Score:** 11/12 (M1 ausente, documentado; P1 presente — snippet de boolean explosion; P3 presente — conecta a "easy to use, hard to misuse", Scott Meyers, exigido por fase Magus)
- **Plano de execução:**
  - nenhuma — buraco de M1 é aceito como exceção documentada, não como gap a fechar por força
- **Resultado:** —
#### 32 - Adotar vs construir, e governança mínima   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 141 linhas · fase: Magus · status: seedling
- **Núcleo/gaps:** — (T3 nominal não atingido — 141 vs. 500 — desvio aceito, ver callout acima). Fronteira respeitada: comparação técnica de bibliotecas (MUI/Radix/shadcn) apontada para `React/Ecossistema/03`, aqui só a decisão de produto (quando adotar). **Callout `[!info]` dedicado rotula o panorama de mercado como "sinal direcional... não fonte de autoridade"** — confirmado nesta rodada por leitura direta; nenhum preço de ferramenta citado em nenhuma das 7 notas do sub-galho (confirmado por grep). "O que vem a seguir" corrigido antes do commit original para apontar também a SG3 (próximo sub-galho real da ordem de execução), não só SG6 (já fechado).
- **Score:** 12/12 (P1 N/A — nota conceitual, sem seção de código; P3 presente — conecta à talk de Dan Abramov sobre abstração prematura, exigido por fase Magus). M1: [Dan Abramov — The WET Codebase (Deconstruct 2019)](https://www.youtube.com/watch?v=17KCHwOwgms), transcrição lida; candidato mais óbvio (zeroheight "Design System Discussions: Adoption") rejeitado antes por tratar de adoção interna de DS já existente, não da decisão adotar-vs-construir.
- **Plano de execução:**
  - nenhuma
- **Resultado:** —
