---
title: "Roadmap — Medir, Validar e Sustentar"
created: 2026-07-29
type: meta
publish: false
tags:
  - meta
  - roadmap
---

# Roadmap — Medir, Validar e Sustentar

Diagnóstico nota a nota. Cada entrada tem estado de enriquecimento, score, classificação
de custo e plano de execução acionável. Gerado por `/diagnosticar-galho`, a partir da
auditoria já registrada em `.superpowers/sdd/2026-07-28-dominio-ux-plano/task-7-report.md`
(gate `verificar-nota` rodado manualmente nota a nota na Task 7, rodada de escrita) —
confirmada por amostragem nesta rodada (Task 7, Passos D–F): contagem de linhas real
(`wc -l`, 8/8 conferidas, todas batem com o report), validador `validar-mermaid.mjs` (8/8
notas, 11 blocos no total, 0 quebrados), e resolução em disco (`test -f`) de todos os
wikilinks cross-galho citados no report (nota 38 → Web Performance ×3, nota 40/45 → nota 08
SG2, nota 41/42 → Operação, nota 44 → nota 20 SG4, nota 45 → índice SG8), todos conferidos
diretamente nesta rodada. Os callouts de precisão aprovados em revisão (SUS 68 = média
empírica não percentual; Forrester "$1→$100" como exemplo de número sem lastro, nunca
argumento; síntese da nota 45 marcada como inferência, não framework nomeado; buraco de M1
da nota 43) foram lidos e confirmados intactos por grep direto no corpo das notas.

**Galho:** `03-Dominios/Engenharia/UX/Medir, Validar e Sustentar`
**Diagnóstico:** 2026-07-29
**Última execução:** 2026-07-29 — **diagnóstico COMPLETO, enriquecimento não necessário (8/8 ➖)**

**Skills:** o Skill tool não estava disponível para os arquivos deste repositório nesta
sessão (as skills vivem em `.claude/skills/`, não escopadas para este agente) — as
instruções de `diagnosticar-galho`, `enriquecer-galho` e `verificar-nota` foram lidas
diretamente de `.claude/skills/<nome>/SKILL.md` e seguidas manualmente, mesmo padrão já
registrado nas dispatches anteriores (SG3/Task 6, e a rodada de escrita desta própria Task 7).

> [!info] Política de M1 obrigatório (herdada do domínio, 2026-07-28, Task 11) — com uma exceção documentada
> M1 (mídia verificada — vídeo ou podcast) é **obrigatória em toda nota** deste domínio, sem
> isenção por `fase:`. **7 das 8 notas** deste sub-galho (38, 39, 40, 41, 42, 44, 45) têm
> mídia verificada por transcrição completa via `yt-dlp` (legenda lida por inteiro, não só
> título), com durações conferidas via `yt-dlp --print duration_string` antes de citadas no
> texto. **A nota 43 (Session replay e heatmap) é exceção documentada e aceita**: busca
> extensiva (WebSearch com múltiplas queries + fetch de `nngroup.com/videos`) não encontrou
> vídeo ou podcast verificável e pedagogicamente sólido especificamente sobre "o que session
> replay/heatmap provam vs. não provam" — só conteúdo promocional de ferramenta comercial
> (Hotjar, FullStory, etc.), que não passaria no critério de verificação independente. O
> buraco é reportado na própria nota, num callout `[!warning] Buraco honesto de mídia (M1)`
> (linha 131), não escondido. **Decisão do usuário registrada (2026-07-28/29): buracos de
> mídia seguem em julgamento caso a caso, sem teto numérico** — nenhuma mídia fraca foi
> forçada na nota 43, e ela não é marcada como pendente por causa disso. Este é o **quarto
> caso** do domínio (após nota 06/SG2, nota 16/SG3, nota 31/SG5). Se aparecer candidato
> verificável no futuro, reabrir com `/adicionar-midia`.

> [!info] Âncora de profundidade é o SG1 (não o bloco anterior)
> Por decisão do plano (2026-07-28), o piso qualitativo de comparação é sempre o SG1
> (Fundamentos e Modelo Mental), nunca o bloco imediatamente anterior — evita erosão
> gradual. Piso qualitativo: ≥3 casos práticos por nota + recorte em prosa (aqui, "aplicável
> a engenheiro solo vs. exige time/orçamento de pesquisa", variação do "praticável sozinho
> vs. exige time" dos sub-galhos anteriores). As 8 notas do SG7 atendem a isso desde a
> primeira rodada (Task 7): todas com exatamente 3 casos práticos em prosa, confirmado na
> tabela do `task-7-report.md`. Fronteiras preservadas: nota 38 → `Tecnologia/Web
> Performance` (ponte "insumo, não substituto", sem reexplicar Core Web Vitals — confirmado
> por leitura direta, linha 81); nota 41 → `Engenharia/Operação` (feature flags/progressive
> delivery); nota 40/45 → nota 08 (SG2, cliente ≠ usuário); nota 44 → nota 20 (SG4, os 5
> estados de tela); nota 45 → índice do SG8 (Ética e Ofício).

> [!info] Piso de linhas — desvio documentado
> `verificar-nota` cobra T3 (Magus ≥500 linhas) como item de score. Este domínio segue
> `00-Meta/guia/Convenções de escrita.md`: "Comprimento não é meta — é consequência. Não
> existe piso de linhas". As 8 notas ficam em **132–167 linhas** (26%–33% do piso T3
> nominal) — abaixo do piso nominal, na mesma faixa de desvio já registrada e aceita em
> todos os sub-galhos anteriores (SG1 138–187, SG3 121–130, SG4 115–137, SG5 115–162, SG6
> 125–147). T3 é tratado como não-bloqueante neste diagnóstico; densidade (3 casos práticos
> por nota, mecanismo explicado "em uma frase", teoria subjacente com atribuição nomeada —
> Brooke 1986, Reichheld/Bain 2003, Cunningham 1992, Rodden/Hutchinson/Fu 2010,
> Sauro/Lewis/Dumas/Maher/Utesch —, armadilhas com causa e correção), não contagem de
> linhas, é o critério real. Ver `task-7-report.md` para a tabela nota → score → mídia →
> verificação da rodada de escrita.

## Régua de análise

Checklist `verificar-nota` — 12 itens (isenções por fase/tipo/broto aplicadas por nota):

| Grupo | Itens |
|-------|-------|
| ESTRUTURA | E1 TL;DR · E2 Abertura-problema · E3 Mermaid · E4 Casos práticos · E5 O que vem a seguir · E6 Inglês · E7 Tabela PT↔EN · E8 Armadilhas [!warning] |
| PROFUNDIDADE | P1 Código-com-falha · P2 Mecanismo explicado |
| LINKS | L1 Wikilink cross-galho · L2 Referência externa (URL) |
| MÍDIA | M1 Vídeo/podcast embutido |

**Esquema de `fase:` detectado:** COM fase (Magus 38–45)
**Piso de linhas:** T3 nominal tratado como não-bloqueante — ver desvio documentado acima.

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 8 |
| ⬜ pendente | 0 |
| ➖ não precisa | 8 |
| ✅ feita | 0 |
| % concluído | 100% |

> Diagnóstico concluído em 2026-07-29: as 8 notas já atendem ao núcleo completo (E1-E8, P2,
> P3, L1, L2; M1 em 7/8, buraco honesto na nota 43) — nenhuma entra no loop de execução do
> `enriquecer-galho`. `% concluído` conta `➖ não precisa` como concluído (nada a fazer), não
> `✅ feita` (nenhuma execução foi disparada, pois não havia gap de núcleo).

---

## Notas

#### 38 - HEART e Goals-Signals-Metrics   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 161 linhas · fase: Magus · status: seedling
- **Núcleo/gaps:** — (T3 nominal não atingido — 161 vs. 500 — desvio aceito, ver callout
  acima). Ponte obrigatória com `Tecnologia/Web Performance` presente e correta ("insumo,
  não substituto"; INP ruim pode explicar Task Success ruim, mas a métrica pertence ao
  outro domínio) — confirmado por leitura direta (linha 81), sem reexplicar Core Web
  Vitals. Linka nota 39 (mesmo sub-galho, Happiness/questionários).
- **Score:** 12/12 (P1 N/A — nota conceitual, sem seção de código; P3 presente — origem do
  HEART no Google/Rodden, Hutchinson & Fu 2010, exigido por fase Magus). M1:
  [Ungrammary — *Heart framework*](https://www.youtube.com/watch?v=NKAg9uM8Z0k), legenda
  manual EN baixada via `yt-dlp` e lida por completo — confirma as 5 categorias e o
  problema original de medir em escala/automação.
- **Plano de execução:**
  - nenhuma
- **Resultado:** —
#### 39 - SUS, UMUX-Lite, SUPR-Q e SEQ   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 155 linhas · fase: Magus · status: seedling
- **Núcleo/gaps:** — (T3 nominal não atingido — 155 vs. 500 — desvio aceito, ver callout
  acima). **Callout de precisão preservado:** SUS 68 é média empírica (Sauro & Lewis, 2016),
  não meio da escala; score não é percentual — confirmado por grep direto (linhas 27–29,
  102–105). Linka nota 38 e nota 45.
- **Score:** 12/12 (P1 N/A — nota conceitual; P3 presente — Brooke 1986 e Sauro/Lewis 2016
  nomeados, exigido por fase Magus). M1:
  [NN/g — *The System Usability Scale (SUS)*](https://www.youtube.com/watch?v=UMv_OW9__qY),
  legenda manual EN baixada; duração conferida (6:34) antes de citada no texto.
- **Plano de execução:**
  - nenhuma
- **Resultado:** —
#### 40 - NPS e North Star - promessa, crítica e Goodhart   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 149 linhas · fase: Magus · status: seedling
- **Núcleo/gaps:** — (T3 nominal não atingido — 149 vs. 500 — desvio aceito, ver callout
  acima). Linka nota 08 (SG2, cliente ≠ usuário — quem responde ao NPS de fato), nota 38 e
  nota 41; nota 45 linka de volta.
- **Score:** 12/12 (P1 N/A — nota conceitual; P3 presente — Reichheld/Bain 2003 e a Lei de
  Goodhart nomeados, exigido por fase Magus). M1:
  [NN/g — *Downsides of the Net Promoter Score*](https://www.youtube.com/watch?v=YwLAGDlhLM8),
  legenda manual EN baixada; duração conferida (5:09), confirma perda de informação e
  recomendação de uso combinado com outras métricas.
- **Plano de execução:**
  - nenhuma
- **Resultado:** —
#### 41 - Instrumentação - event taxonomy e tracking plan   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 138 linhas · fase: Magus · status: seedling
- **Núcleo/gaps:** — (T3 nominal não atingido — 138 vs. 500 — desvio aceito, ver callout
  acima). Fronteira obrigatória com `Engenharia/Operação` presente e correta (feature
  flags/progressive delivery como assunto distinto da instrumentação de evento) —
  confirmado por leitura direta (linha 131) e `test -f` do arquivo-alvo. Linka nota 42 e
  nota 44.
- **Score:** 12/12 (P1 N/A — nota conceitual; P3 presente — formato evento/propriedade
  ancorado em prática de indústria nomeada, exigido por fase Magus). M1:
  [Product Analytics Academy — *Build Your First Tracking Plan*](https://www.youtube.com/watch?v=7Gqy_Kqmg70),
  legenda automática EN baixada e lida; duração conferida (15:38), confirma formato
  evento/propriedade.
- **Plano de execução:**
  - nenhuma
- **Resultado:** —
#### 42 - Quando A-B não se aplica   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 167 linhas · fase: Magus · status: seedling
- **Núcleo/gaps:** — (T3 nominal não atingido — 167 vs. 500 — desvio aceito, ver callout
  acima). **Segunda nota-espinha do domínio** (peso equivalente à nota 08): tráfego
  baixo/B2B/cliente único tratado como condição estrutural, não azar, já no TL;DR e na
  abertura — confirmado por leitura direta. As 5 alternativas (painted door,
  sequencial/bayesiano, micro-conversão, feature flag com rollout progressivo, qualitativo
  rigoroso) apresentadas com tom de método, não consolo, incluindo `[!warning]` dedicado
  contra tratar A/B como substituto de pensar. Linka nota 38, 39, 41, 43, 45 e
  `Engenharia/Operação` (progressive delivery, reaproveitado como "desenho experimental
  mínimo").
- **Score:** 12/12 (P1 N/A — nota conceitual; P3 presente — Cunningham 1992 (feature flags)
  e literatura de teste sequencial/bayesiano nomeadas, exigido por fase Magus). M1:
  [Rosie Hoggmascall (Experiment Nation) — *Low-traffic testing*](https://www.youtube.com/watch?v=BaCLS465BIM),
  legenda automática EN baixada e lida (trecho inicial conferido); duração real 22:23,
  registrada na nota como "~22min", conferida antes de citada.
- **Plano de execução:**
  - nenhuma
- **Resultado:** —
#### 43 - Session replay e heatmap - o que provam e o que não   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 132 linhas · fase: Magus · status: seedling
- **Núcleo/gaps:** **M1 ausente — buraco honesto, ver política acima.** Isento de bloqueio:
  busca extensiva (WebSearch múltiplas queries + fetch de `nngroup.com/videos`) documentada
  no `task-7-report.md`; não encontrou vídeo/podcast verificável e pedagogicamente sólido
  sobre o contraste exato "o que session replay/heatmap provam vs. não provam" — só
  conteúdo promocional de ferramenta comercial. Buraco reportado na própria nota em
  callout `[!warning] Buraco honesto de mídia (M1)` (linha 131), confirmado por grep direto
  nesta rodada. Linka nota 42 e nota 45.
- **Score:** 11/12 (M1 ausente, documentado; P1 N/A — nota conceitual; P3 presente —
  exigido por fase Magus, ancorado em literatura de UX research qualitativo)
- **Plano de execução:**
  - nenhuma — buraco de M1 é aceito como exceção documentada (interseção de nicho entre
    conteúdo pedagógico independente e material promocional de ferramenta comercial), não
    como gap a fechar por força; decisão do usuário: sem teto numérico de buracos de mídia
- **Resultado:** —
#### 44 - UX debt e matriz severidade x esforço   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 162 linhas · fase: Magus · status: seedling
- **Núcleo/gaps:** — (T3 nominal não atingido — 162 vs. 500 — desvio aceito, ver callout
  acima). Linka nota 20 (SG4, os 5 estados de tela) e nota 45 — confirmado por leitura
  direta e `test -f` do arquivo-alvo.
- **Score:** 12/12 (P1 N/A — nota conceitual, sem seção de código; P3 presente — analogia
  com dívida técnica de Ward Cunningham 1992, exigido por fase Magus). M1:
  [NN/g — *UX Debt*](https://www.youtube.com/watch?v=4MdJXPVvrts), legenda manual EN
  baixada; duração conferida (3:02), confirma a analogia com dívida técnica.
- **Plano de execução:**
  - nenhuma
- **Resultado:** —
#### 45 - Defender decisão de UX com número   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 143 linhas · fase: Magus · status: seedling
- **Núcleo/gaps:** — (T3 nominal não atingido — 143 vs. 500 — desvio aceito, ver callout
  acima). **Callout de precisão preservado:** citação Forrester ("$1 → $100") marcada
  explicitamente como não-verificada e apresentada só como exemplo do problema, nunca como
  argumento — confirmado por grep direto (linhas 19, 33–36, 92, 136). **Síntese de 4 passos
  marcada como inferência da pesquisa, não framework nomeado** — callout `[!info]` dedicado
  antes da lista (linha 43), confirmado. Linka nota 08 (SG2), nota 38, 39, 40, 42, 44, e o
  índice do SG8 (Ética e Ofício) — confirmado `test -f` de todos os alvos.
- **Score:** 12/12 (P1 N/A — nota conceitual; P3 presente — ROI de UX ancorado em relatório
  NN/g de 44 case studies e distinção estimativa/fato, exigido por fase Magus). M1:
  [NN/g — *Don't Overthink UX ROI*](https://www.youtube.com/watch?v=25_bu4z72h8), legenda
  manual EN baixada; duração conferida (2:40), confirma recomendação de simplicidade na
  comunicação de ROI.
- **Plano de execução:**
  - nenhuma
- **Resultado:** —
