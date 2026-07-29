---
title: "Roadmap — Ética e Ofício"
created: 2026-07-29
type: meta
publish: false
tags:
  - meta
  - roadmap
---

# Roadmap — Ética e Ofício

Diagnóstico nota a nota. Cada entrada tem estado de enriquecimento, score, classificação
de custo e plano de execução acionável. Gerado por `/diagnosticar-galho`, a partir da
auditoria já registrada em `.superpowers/sdd/2026-07-28-dominio-ux-plano/task-8-report.md`
(3 notas semeadas + mídia verificada + gate Mermaid rodado na rodada de escrita) —
confirmada por amostragem nesta rodada (Task 8, Passos D–F): contagem de linhas real
(`wc -l`, 3/3 conferidas, todas batem com o report — 138/141/159), validador
`validar-mermaid.mjs` (3/3 notas, 3 blocos no total, 0 quebrados), resolução em disco
(`test -f`) dos 25 wikilinks cross-galho citados nas 3 notas (Carreira/Entrevistas,
Engenharia/Operação, Engenharia/Testes ×2, Acessibilidade/Sustentar e Conformidade ×3,
mais 15 links internos ao domínio UX), e conferência de estrutura por nota (TL;DR, mermaid,
exatamente 3 casos práticos, exatamente 3 armadilhas `[!warning]`, seção "Como explicar em
inglês", "O que vem a seguir", "Fontes") por `grep` direto nesta rodada. As duas correções
pontuais da nota 46 (contagem de executivos da FTC, de três para dois — verificado nesta
rodada contra o acordo final publicado pela FTC em set/2025, que nomeia **Neil Lindsay**,
SVP, e **Jamil Ghani**, VP; e um "already" residual em português) foram aplicadas e
commitadas antes deste diagnóstico.

**Galho:** `03-Dominios/Engenharia/UX/Ética e Ofício`
**Diagnóstico:** 2026-07-29
**Última execução:** 2026-07-29 — **diagnóstico COMPLETO, enriquecimento não necessário (3/3 ➖)**

**Skills:** o Skill tool não estava disponível para os arquivos deste repositório nesta
sessão (as skills vivem em `.agents/skills/`, não escopadas para este agente) — as
instruções de `diagnosticar-galho`, `enriquecer-galho` e `verificar-nota` foram lidas
diretamente de `.agents/skills/<nome>/SKILL.md` e seguidas manualmente, mesmo padrão já
registrado nas dispatches anteriores (SG6/Task 7 e a rodada de escrita desta própria Task 8).

> [!info] Política de M1 obrigatório (herdada do domínio, 2026-07-28, Task 11)
> M1 (mídia verificada — vídeo ou podcast) é **obrigatória em toda nota** deste domínio, sem
> isenção por `fase:`. **3 das 3 notas** deste sub-galho têm mídia verificada por
> transcrição completa via `yt-dlp` (legenda baixada e lida por inteiro, não só título), com
> durações conferidas via `yt-dlp --print duration_string` antes de citadas no texto: nota
> 46 — The Hidden Engine, *"Amazon's $2.5 Billion Subscription Trick"* (7:33); nota 47 —
> Qase, *"How Can QA Shape UX?"* (27:14); nota 48 — UX Brighton, *"Trade offs, Lucy Spence"*
> (26:05). **Nenhum buraco de M1 neste sub-galho** — é o **primeiro sub-galho Magus do
> domínio sem exceção documentada** (após SG3/nota 16, SG5/nota 31, SG7/nota 43, todos com
> um buraco cada). Cobertura parcial de escopo é registrada nos próprios callouts de mídia
> das notas 46 (vídeo não cobre DSA/DFA nem caso Epic — fontes textuais cobrem essa parte) e
> 47 (vídeo é de perspectiva de QA, não de engenharia de código pura) — isso é nuance de
> escopo, não ausência de mídia, e não rebaixa score.

> [!info] Âncora de profundidade é o SG1 (não o bloco anterior)
> Por decisão do plano (2026-07-28), o piso qualitativo de comparação é sempre o SG1
> (Fundamentos e Modelo Mental), nunca o bloco imediatamente anterior — evita erosão
> gradual. Piso qualitativo: ≥3 casos práticos por nota + recorte em prosa ("praticável
> sozinho vs. exige time/apoio externo", mesma variação usada desde o SG4). As 3 notas do
> SG8 atendem a isso: exatamente 3 casos práticos em prosa cada, confirmado por `grep`
> direto (`^### Cenário`) nesta rodada. Fronteiras preservadas, todas resolvidas em disco
> nesta rodada: nota 46 → [[03-Dominios/Engenharia/UX/Design de Interação/23 - Undo vs confirmação|nota 23]]
> (fricção legítima vs. manipuladora, contraste explícito, não reexplicação); nota 47 →
> [[03-Dominios/Tecnologia/Acessibilidade/Sustentar e Conformidade/17 - A11y no ciclo de desenvolvimento|A11y nota 17]]
> (mesmo mecanismo de gate, disciplina diferente, linkado não reexplicado),
> `Engenharia/Testes` (notas 13 e 15), `Engenharia/Operação` (Anatomia de um incidente de
> produção); nota 48 → `Carreira/Entrevistas` (index + STAR Method) e
> [[03-Dominios/Tecnologia/Acessibilidade/Sustentar e Conformidade/20 - A11y em entrevista|A11y nota 20]].

> [!info] Piso de linhas — desvio documentado
> `verificar-nota` cobra T3 (Magus ≥500 linhas) como item de score. Este domínio segue
> `00-Meta/guia/Convenções de escrita.md`: "Comprimento não é meta — é consequência. Não
> existe piso de linhas". As 3 notas ficam em **138–159 linhas** (28%–32% do piso T3
> nominal) — abaixo do piso nominal, na mesma faixa de desvio já registrada e aceita em
> todos os sub-galhos anteriores (SG1 138–187, SG3 121–130, SG4 115–137, SG5 115–162, SG6
> 125–147, SG7 132–167). T3 é tratado como não-bloqueante neste diagnóstico; densidade (3
> casos práticos por nota, mecanismo explicado, teoria/fundamento subjacente com atribuição
> nomeada — texto legal do DSA Art. 25 na nota 46, literatura de DoD/Scrum na nota 47,
> Cagan/NN/g na nota 48 —, armadilhas com causa e correção) é o critério real, não contagem
> de linhas. Ver `task-8-report.md` para a tabela nota → mídia → verificação → casos
> práticos → desvios da rodada de escrita.

## Régua de análise

Checklist `verificar-nota` — 12 itens (isenções por fase/tipo/broto aplicadas por nota):

| Grupo | Itens |
|-------|-------|
| ESTRUTURA | E1 TL;DR · E2 Abertura-problema · E3 Mermaid · E4 Casos práticos · E5 O que vem a seguir · E6 Inglês · E7 Tabela PT↔EN · E8 Armadilhas [!warning] |
| PROFUNDIDADE | P1 Código-com-falha · P2 Mecanismo explicado |
| LINKS | L1 Wikilink cross-galho · L2 Referência externa (URL) |
| MÍDIA | M1 Vídeo/podcast embutido |

**Esquema de `fase:` detectado:** COM fase (Magus 46–48)
**Piso de linhas:** T3 nominal tratado como não-bloqueante — ver desvio documentado acima.

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 3 |
| ⬜ pendente | 0 |
| ➖ não precisa | 3 |
| ✅ feita | 0 |
| % concluído | 100% |

> Diagnóstico concluído em 2026-07-29: as 3 notas já atendem ao núcleo completo (E1-E8, P2,
> P3, L1, L2, M1 3/3) — nenhuma entra no loop de execução do `enriquecer-galho`. `%
> concluído` conta `➖ não precisa` como concluído (nada a fazer), não `✅ feita` (nenhuma
> execução foi disparada, pois não havia gap de núcleo).

---

## Notas

#### 46 - Dark patterns e regulação   [risco legal]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 138 linhas · fase: Magus · status: seedling
- **Núcleo/gaps:** — (T3 nominal não atingido — 138 vs. 500 — desvio aceito, ver callout
  acima). Cenário regulatório verificado nesta e na rodada anterior: DSA Art. 25 em vigor
  desde 17/02/2024 (multa até 6% do faturamento global), DMA como lei separada sobre
  gatekeepers (teto 10%), DFA não vigente (consulta encerrada out/2025, proposta prevista
  Q4 2026), FTC vs. Amazon US$ 2,5 bi (set/2025, "Project Iliad") e FTC vs. Epic US$ 245 mi
  (2023) — todos confirmados em fonte primária. **Correção aplicada nesta rodada:** a nota
  afirmava três executivos nomeados pessoalmente pela FTC no caso Amazon; verificação
  independente no acordo final publicado pela FTC (set/2025) confirma **dois** — Neil
  Lindsay (SVP) e Jamil Ghani (VP) — corrigido nas 3 ocorrências (linhas ~56, 61, 63).
  **Correção adicional:** "already" residual em português (linha 82) trocado por "já".
  Fronteira com [[03-Dominios/Engenharia/UX/Design de Interação/23 - Undo vs confirmação|nota 23]]
  presente e correta (fricção legítima vs. manipuladora), confirmada por leitura direta.
- **Score:** 12/12 (P1 N/A — nota conceitual, sem seção de código; P3 presente — texto legal
  do DSA Art. 25 citado e traduzido, exigido por fase Magus). M1:
  [The Hidden Engine — *"Amazon's $2.5 Billion Subscription Trick"*](https://www.youtube.com/watch?v=19ZYeOgKvnM),
  legenda automática EN baixada via `yt-dlp` e lida por completo; duração conferida (7:33),
  confirma Project Iliad, quedas de 14% em cancelamento e citações internas.
- **Plano de execução:**
  - nenhuma
- **Resultado:** —
#### 47 - UX no ciclo de dev   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 141 linhas · fase: Magus · status: seedling
- **Núcleo/gaps:** — (T3 nominal não atingido — 141 vs. 500 — desvio aceito, ver callout
  acima). Fronteiras obrigatórias presentes e corretas, confirmadas por `test -f`:
  [[03-Dominios/Tecnologia/Acessibilidade/Sustentar e Conformidade/17 - A11y no ciclo de desenvolvimento|A11y nota 17]]
  (mesmo mecanismo de gate, disciplina diferente — linkado, não reexplicado),
  `Engenharia/Testes` (notas 13 e 15), `Engenharia/Operação` (Anatomia de um incidente de
  produção). Linka também notas 20/29/35/36/37 do próprio domínio UX. Ocorrência de
  "already" nesta nota fica dentro da seção "Como explicar em inglês" (citação em inglês
  legítima) — não confundir com o deslize corrigido na nota 46.
- **Score:** 12/12 (P1 N/A — nota conceitual, sem seção de código; P3 presente — DoD/Scrum e
  prática de shift-left citadas, exigido por fase Magus). M1:
  [Qase — *"How Can QA Shape UX? Early Involvement, Design Reviews & Visual Regression Testing"*](https://www.youtube.com/watch?v=J9dztDkluow),
  legenda automática EN baixada e lida; duração conferida (27:14), confirma checklist de
  design, design review pós-implementação e regressão visual. Cobertura parcial registrada
  no callout de mídia da própria nota (perspectiva de QA, não de engenharia de código pura)
  — nuance de escopo, não ausência.
- **Plano de execução:**
  - nenhuma
- **Resultado:** —
#### 48 - UX em entrevista sênior e staff   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 159 linhas · fase: Magus · status: seedling
- **Núcleo/gaps:** — (T3 nominal não atingido — 159 vs. 500 — desvio aceito, ver callout
  acima). Fronteiras obrigatórias presentes e corretas: `Carreira/Entrevistas` (index e STAR
  Method) e [[03-Dominios/Tecnologia/Acessibilidade/Sustentar e Conformidade/20 - A11y em entrevista|A11y nota 20]],
  confirmadas por `test -f`. Linka também as notas-espinha 08 e 42, mais 03/04/22/23/29/32/40/45/47
  do próprio domínio UX. Um wikilink foi corrigido durante a checagem da rodada de escrita
  (nota 32: "Adotar vs construir, e governança mínima para um time de um" → nome real do
  arquivo, "Adotar vs construir, e governança mínima") — confirmado resolvido nesta rodada.
- **Score:** 12/12 (P1 N/A — nota conceitual, sem seção de código; P3 presente — literatura
  de Cagan/NN/g citada, exigido por fase Magus). M1:
  [UX Brighton — *"Trade offs, Lucy Spence, UX Brighton 2022"*](https://www.youtube.com/watch?v=zNfoSKIobK8),
  legenda automática EN baixada e lida; duração conferida (26:05), confirma trade-off
  explícito entre UX e produto (velocidade vs. qualidade, aquisição vs. retenção). Aplicação
  ao vocabulário de entrevista de engenharia é elaboração própria, nomeada como tal no
  callout da nota — nuance de escopo, não ausência de mídia.
- **Plano de execução:**
  - nenhuma
- **Resultado:** —
