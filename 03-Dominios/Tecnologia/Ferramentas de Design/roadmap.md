---
title: "Roadmap — Ferramentas de Design"
created: 2026-07-28
updated: 2026-07-29
type: meta
publish: false
tags:
  - meta
  - roadmap
  - ux
---

# Roadmap — Ferramentas de Design

Diagnóstico nota a nota. Cada entrada tem estado de enriquecimento, score, classificação
de custo e plano de execução acionável. Gerado a partir da auditoria já registrada em
`.superpowers/sdd/2026-07-28-dominio-ux-plano/task-9-report.md` (semeadura + verificação de
mídia + gate de sintaxe Mermaid, rodada de escrita 2026-07-29) — confirmada por amostragem
nesta rodada (Task 9, diagnóstico/fechamento): contagem de linhas real (`wc -l`, 9/9
conferidas), presença de diagrama Mermaid (9/9), 3 casos práticos em `### Cenário` por nota
(9/9), 3 callouts `[!warning]` na seção Armadilhas por nota (9/9), tabela PT↔EN (9/9), e
resolução em disco (`test -f`) de todos os wikilinks cross-galho citados nas fronteiras do
brief (nota 01 → SG5/29, nota 03 → skill `handoff-design` + `Tecnologia/IA/Claude Code`,
nota 05 → `Tecnologia/IA/Image Prompting` + SG5/26, nota 08 → `Tecnologia/CSS/07` + SG5/29,
nota 09 → `Tecnologia/Testes JS/14`), todos conferidos diretamente nesta rodada. Nenhum
preço de ferramenta encontrado em nenhuma das 9 notas (`grep` dedicado, 0 ocorrências).

**Galho:** `03-Dominios/Tecnologia/Ferramentas de Design` (galho-folha, sem sub-pastas)
**Diagnóstico:** 2026-07-29
**Última execução:** 2026-07-29 — **diagnóstico COMPLETO, enriquecimento não necessário
(9/9 ➖)**, salvo o nivelamento cosmético de nomenclatura aplicado nesta mesma rodada
(ver abaixo)

**Skills:** o Skill tool não estava disponível para os arquivos deste repositório nesta
sessão — as instruções de `diagnosticar-galho`, `enriquecer-galho` e `verificar-nota` foram
lidas diretamente de `.agents/skills/<nome>/SKILL.md` e seguidas manualmente, mesmo padrão
já registrado nos sub-galhos anteriores de `Engenharia/UX`.

> [!warning] Galho perecível — quatro fatos mudaram em UM dia entre pesquisa e escrita
> Este é o galho **mais perecível de todo o domínio de UX** — produtos de IA generativa e
> features de plataforma de design mudam em meses, não anos. A verificação ativa da Task 9
> encontrou **quatro divergências reais** entre a pesquisa (2026-07-28) e a escrita
> (2026-07-29), todas já tratadas nas notas correspondentes, mas registradas aqui porque
> quem retomar este galho no futuro precisa ver isso **primeiro**, antes de confiar em
> qualquer detalhe abaixo:
>
> 1. **`/design-sync` do Claude Design existe e está documentado oficialmente** — a pesquisa
>    original supunha que não (só aparecia em blog de terceiro). Confirmado em
>    `claude.com/product/claude-design`. Ver nota 03, seção "O comando `/design-sync`: o
>    não-confirmado que se confirmou".
> 2. **Claude Design passou de "research preview" para "beta"** — e de limites de uso
>    separados para **limites compartilhados com chat/Cowork/Claude Code**. Ver nota 03,
>    TL;DR e callout de caducidade.
> 3. **v0 (Vercel) agora afirma gerar backend**, não só frontend React — a pesquisa original
>    o descrevia como "gera apenas frontend, sem backend"; a página oficial hoje reivindica
>    geração agentic com conexão a banco de dados. Ver nota 04, seção sobre v0.
> 4. **O repositório "Make Real" do tldraw foi arquivado em 20/02/2026** — não estava no
>    radar da pesquisa original. Ver nota 07, callout de caducidade e Cenário 3.
>
> Dois pontos adicionais, já rastreados desde a pesquisa e reconfirmados nesta rodada:
> **Hallmark tem ~19,6 mil estrelas** no GitHub (bem acima da estimativa original de ~1,8
> mil — nota 05, com aviso explícito de que esse número muda rápido e deve ser revalidado);
> e a **integração bidirecional Figma ↔ Claude Code segue sem data confirmada** em fonte
> primária — o *write-to-canvas* em si está confirmado e em **beta** via `help.figma.com`,
> mas nem a data de fev/2026 da pesquisa original nem a de 24/mar/2026 citada por um vídeo
> de terceiro foram verificadas em fonte primária (nota 02, seção dedicada). **Revalidar
> cada um destes seis pontos antes de reutilizar qualquer um deles em contexto novo.**

> [!info] Política de M1 obrigatório — zero buracos neste galho
> M1 (mídia verificada — vídeo ou podcast) é obrigatória em toda nota deste domínio, sem
> isenção por `fase:`. **As 9 notas deste galho têm mídia verificada por transcrição
> completa via `yt-dlp`** (legenda lida por inteiro, não só título), com durações conferidas
> via `yt-dlp --print duration_string` antes de citadas no texto: nota 01 (6:32), nota 02
> (31:26), nota 03 (13:50), nota 04 (28:57), nota 05 (22:01), nota 06 (6:07), nota 07 (2
> mídias: 14:25 + 2:38), nota 08 (2:01), nota 09 (15:36). **Zero buracos honestos de M1
> neste galho** — diferente dos sub-galhos de `Engenharia/UX` (SG2, SG3, SG5, SG7), onde
> buracos documentados foram aceitos caso a caso.

> [!info] Âncora de profundidade é o SG1 (não o bloco anterior)
> Por decisão do plano (2026-07-28), o piso qualitativo de comparação é sempre o SG1
> (`Engenharia/UX/Fundamentos e Modelo Mental`), nunca o bloco imediatamente anterior — evita
> erosão gradual. Piso qualitativo: ≥3 casos práticos por nota + recorte em prosa
> ("praticável sozinho vs. exige mais estrutura", mesma variação usada nos sub-galhos
> anteriores). As 9 notas deste galho atendem a isso desde a rodada de escrita: todas com
> exatamente 3 casos práticos em `### Cenário`, confirmado por amostragem nesta rodada.
> Fronteiras preservadas (confirmadas por `test -f` nesta rodada): nota 01 →
> [[03-Dominios/Engenharia/UX/Linguagem Visual e Design System/29 - Design tokens como sistema|nota 29 do SG5]];
> nota 03 → skill local `handoff-design` (linkada e descrita sem duplicar o "como fazer") e
> `Tecnologia/IA/Claude Code`; nota 05 →
> [[03-Dominios/Tecnologia/IA/Image Prompting/index|Tecnologia/IA/Image Prompting]] (mesma
> raiz de convergência estatística) e
> [[03-Dominios/Engenharia/UX/Linguagem Visual e Design System/26 - Hierarquia visual|nota 26 do SG5]];
> nota 08 → [[03-Dominios/Tecnologia/CSS/07 - Custom properties e design tokens|Tecnologia/CSS/07]]
> e [[03-Dominios/Engenharia/UX/Linguagem Visual e Design System/29 - Design tokens como sistema|nota 29 do SG5]]
> — consistente com ela: DTCG é **Community Group Report, não padrão W3C**, confirmado por
> grep direto nas duas notas; nota 09 →
> [[03-Dominios/Tecnologia/Testes JS/14 - Playwright além do básico|Tecnologia/Testes JS/14]].

> [!info] Piso de linhas — desvio documentado (herdado da convenção do vault)
> `verificar-nota` cobra piso de linhas por fase como item de score (Iniciado ≥300, Adepto
> ≥400, Magus ≥500). Este domínio segue `00-Meta/guia/Convenções de escrita.md`: "Comprimento
> não é meta — é consequência. Não existe piso de linhas". As 9 notas deste galho ficam em
> **120–145 linhas** — bem abaixo do piso nominal de qualquer fase — na mesma faixa de desvio
> já registrada e aceita em todos os sub-galhos de `Engenharia/UX` (SG1 138–187, SG3
> 121–130, SG4 115–137, SG5 115–162, SG6 125–147, SG7 132–167). A própria âncora SG1 (nota
> 01, 190 linhas, fase Iniciado) e a nota 29 do SG5 (146 linhas, fase Magus) já ficam abaixo
> do piso genérico — nenhuma nota deste domínio persegue o piso de linhas do template
> genérico. O piso é tratado como **não-bloqueante** neste diagnóstico; densidade (3 casos
> práticos por nota, mecanismo explicado, armadilhas com causa e correção, mídia verificada
> com duração conferida) é o critério real. Ver `task-9-report.md` para a tabela nota →
> score → mídia → verificação da rodada de escrita.

> [!success] Achado Minor resolvido nesta rodada — nivelamento de nomenclatura
> A revisão anterior identificou um achado **Minor** (cosmético, não bloqueante): as notas
> **01 e 02** cobriam o conteúdo "praticável sozinho vs. exige time/estrutura" em **prosa
> integrada**, sem o heading `##` dedicado que as notas 03–09 usam
> (`## Praticável sozinho vs. exige mais estrutura`). A substância já estava lá (critério de
> corte explícito, subitens justificados) — só a nomenclatura divergia. **Resolvido nesta
> rodada, sem diluir nem reescrever conteúdo aprovado:**
> - Nota 01: inserido o heading padrão como seção-mãe; as duas seções existentes ("O que
>   vale aprender, e por quê" / "O que dá pra ignorar com segurança") foram demovidas para
>   `###` como subseções — nenhuma frase alterada.
> - Nota 02: a seção única existente ("O que isso muda no dia a dia de quem trabalha
>   sozinho") foi renomeada para o heading padrão, preservando a frase original como abertura
>   de parágrafo — nenhum conteúdo removido ou reescrito.
>
> Nota 03 mantém heading próprio (`## Praticável sozinho vs. exige revisão`) — variação já
> existente antes desta rodada, fora do escopo do achado (que citava só 01 e 02); não
> tocada.

**Nível:** galho-folha (só notas, sem sub-pastas).

**Legenda de estado:** ✅ feita · 🔄 em andamento · ⬜ pendente · ➖ não precisa.

## Régua de análise

Checklist `verificar-nota` — 12 itens (isenções por fase/tipo/broto aplicadas por nota):

| Grupo | Itens |
|-------|-------|
| ESTRUTURA | E1 TL;DR · E2 Abertura-problema · E3 Mermaid · E4 Casos práticos · E5 O que vem a seguir · E6 Inglês · E7 Tabela PT↔EN · E8 Armadilhas [!warning] |
| PROFUNDIDADE | P1 Código-com-falha · P2 Mecanismo explicado |
| LINKS | L1 Wikilink cross-galho · L2 Referência externa (URL) |
| MÍDIA | M1 Vídeo/podcast embutido |

**Esquema de `fase:` detectado:** misto — COM fase, mas sem gradiente único: 01, 06, 07
`Iniciado`; 02–05, 08 `Adepto`; 09 `Magus` (o eixo do galho não é "iniciado → magus" por
nota, é "o que existe hoje e para que serve" — sequência editorial, não progressão de
domínio; ver `index.md`).
**Piso de linhas:** nominal por fase tratado como não-bloqueante — ver desvio documentado
acima.
**Isenção adicional deste galho:** P1 (código-com-falha) é **N/A em todas as 9 notas** —
nenhuma tem seção de código; o único bloco fenced de cada nota é o diagrama Mermaid. P3
(teoria subjacente, exigida em fase Magus nos sub-galhos de `Engenharia/UX`) é tratada como
**N/A por natureza de galho** na nota 09 (única Magus daqui): este é um galho de
ferramentas, não de pesquisa acadêmica — o mecanismo é explicado com atribuição à fonte
primária (repositório oficial `microsoft/playwright-mcp`), não a autor/ano de estudo
nomeado, o que cumpre o espírito do item sem forçar uma citação que não existe.

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 9 |
| ⬜ pendente | 0 |
| ➖ não precisa | 9 |
| ✅ feita | 0 |
| % concluído | 100% |

> Diagnóstico concluído em 2026-07-29: as 9 notas já atendem ao núcleo completo (E1, E2, E5,
> L2, P2 presentes em todas) — nenhuma entra no loop de execução do `enriquecer-galho`. `%
> concluído` conta `➖ não precisa` como concluído (nada a fazer), não `✅ feita` (nenhuma
> execução do loop foi disparada, pois não havia gap de núcleo). O único ajuste desta rodada
> foi o nivelamento cosmético de nomenclatura nas notas 01 e 02 (ver callout acima),
> aplicado diretamente, fora do loop `[mecânico]`/`[substantivo]` — não é gap de núcleo.

---

## Notas

#### 01 - Figma para o engenheiro   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 129 linhas · fase: Iniciado · status: seedling
- **Núcleo/gaps:** — (piso de linhas nominal não atingido — 129 vs. 300 — desvio aceito, ver
  callout acima). Heading "Praticável sozinho vs. exige mais estrutura" adicionado nesta
  rodada (nivelamento cosmético, sem alterar prosa). Linka
  [[03-Dominios/Engenharia/UX/Linguagem Visual e Design System/29 - Design tokens como sistema|nota 29 do SG5]]
  (hierarquia primitivo→semântico→componente) e nota 08 deste galho — confirmado `test -f`.
- **Score:** 12/12 (P1 N/A — nota conceitual, sem seção de código; P3 N/A — fase Iniciado).
  M1: [Figma — *Collaboration and handoff in Dev Mode*](https://www.youtube.com/watch?v=xCJsRuH7v9w),
  canal oficial, legenda auto EN baixada e lida por completo; duração conferida (6:32).
- **Plano de execução:**
  - nenhuma
- **Resultado:** —

#### 02 - Figma MCP Server e Code Connect   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 137 linhas · fase: Adepto · status: seedling
- **Núcleo/gaps:** L1 ausente — todos os wikilinks da nota apontam para outras notas do
  mesmo galho (01, 03, 09), nenhum cross-galho. **Não é gap de núcleo** (núcleo = E1, E2, E5,
  L2, P2) e é aceito por design do brief: as fronteiras cross-galho deste galho se
  concentram nas notas-charneira (01, 03, 05, 08, 09), não são exigidas em toda nota. Heading
  "Praticável sozinho vs. exige mais estrutura" aplicado nesta rodada sobre a seção
  existente (nivelamento cosmético, prosa preservada). Trata explicitamente o não-confirmado
  da integração bidirecional Figma ↔ Claude Code (ver callout de caducidade do galho).
- **Score:** 11/12 (P1 N/A — nota conceitual; L1 ausente, ver acima).
  M1: [Rafael Quintanilha (QuantBrasil) — *Claude Code e Codex com Figma MCP*](https://www.youtube.com/watch?v=VHESZ4GsoQk),
  PT-BR, legenda auto baixada e lida por completo; duração conferida (31:26).
- **Plano de execução:**
  - nenhuma
- **Resultado:** —

#### 03 - Claude Design e o handoff bundle   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 135 linhas · fase: Adepto · status: seedling
- **Núcleo/gaps:** — (piso nominal não atingido — 135 vs. 400 — desvio aceito). Linka skill
  local `handoff-design` (fronteira "linka, não duplica o como fazer", confirmada por
  leitura direta) e [[03-Dominios/Tecnologia/IA/Claude Code/index|Tecnologia/IA/Claude Code]]
  — confirmado `test -f`. Registra as duas mudanças de status mais quentes do galho
  (`/design-sync` confirmado; research preview → beta) — ver callout de caducidade acima.
- **Score:** 12/12 (P1 N/A — nota conceitual; P3 N/A — fase Adepto).
  M1: [Matheus Battisti (Hora de Codar) — *Anthropic ACABOU DE LANÇAR o Claude Design*](https://www.youtube.com/watch?v=ZGJ26VZKYBY),
  PT-BR, publicado no dia do lançamento; legenda auto baixada e lida; duração conferida
  (13:50).
- **Plano de execução:**
  - nenhuma
- **Resultado:** —

#### 04 - Geradores de UI por IA   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 145 linhas · fase: Adepto · status: seedling
- **Núcleo/gaps:** — (piso nominal não atingido — 145 vs. 400 — desvio aceito). Cobertura
  parcial reconhecida na própria nota: mídia cobre Lovable e Bolt diretamente, não
  v0/Subframe/Polymet — registrado em callout, não escondido. Linka
  [[03-Dominios/Tecnologia/Acessibilidade/index|Tecnologia/Acessibilidade]] e nota 08
  (pipeline de tokens) e nota 05 — confirmado `test -f`. Registra a mudança de escopo do v0
  (agora reivindica backend) — ver callout de caducidade acima.
- **Score:** 12/12 (P1 N/A — nota conceitual; P3 N/A — fase Adepto).
  M1: [Christian Peverelli (WeAreNoCode) — *I Built the SAME App in Lovable vs Base44 vs Bolt*](https://www.youtube.com/watch?v=GfnkxLb41ZM),
  EN, legenda auto baixada e lida por completo; duração conferida (28:57).
- **Plano de execução:**
  - nenhuma
- **Resultado:** —

#### 05 - Estética genérica de IA e como escapar   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 126 linhas · fase: Adepto · status: seedling
- **Núcleo/gaps:** — (piso nominal não atingido — 126 vs. 400 — desvio aceito). Linka
  [[03-Dominios/Tecnologia/IA/Image Prompting/index|Tecnologia/IA/Image Prompting]] (mesma
  raiz de convergência estatística) e
  [[03-Dominios/Engenharia/UX/Linguagem Visual e Design System/26 - Hierarquia visual|nota 26 do SG5]]
  — confirmado `test -f`. Cita Hallmark com ~19,6 mil estrelas (número atualizado e
  explicitamente marcado como perecível) — ver callout de caducidade acima.
- **Score:** 12/12 (P1 N/A — nota conceitual; P3 N/A — fase Adepto).
  M1: [DesignCode — *How to Avoid AI Slop in Vibe-Coded Landing Pages*](https://www.youtube.com/watch?v=M4DNgmI7MIM),
  EN, legenda auto baixada e lida por completo; duração conferida (22:01), cita literalmente
  o fingerprint "purple gradient... very 2025" que a nota descreve.
- **Plano de execução:**
  - nenhuma
- **Resultado:** —

#### 06 - Protótipo em código   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 120 linhas · fase: Iniciado · status: seedling
- **Núcleo/gaps:** L1 ausente — wikilinks só para notas 01, 07, 09 deste galho, nenhum
  cross-galho. **Não é gap de núcleo** (mesma justificativa da nota 02: fronteiras cross-
  galho concentradas nas notas-charneira, por design do brief).
- **Score:** 11/12 (P1 N/A — nota conceitual; P3 N/A — fase Iniciado; L1 ausente, ver acima).
  M1: [James Stone — *Why I Don't Prototype Interactions in Figma*](https://www.youtube.com/watch?v=eqJNks8ogkQ),
  EN, legenda auto baixada e lida por completo; duração conferida (6:07). Autor é designer,
  não engenheiro fugindo do Figma — ângulo complementar, registrado em callout.
- **Plano de execução:**
  - nenhuma
- **Resultado:** —

#### 07 - Excalidraw e tldraw   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 126 linhas · fase: Iniciado · status: seedling
- **Núcleo/gaps:** L1 ausente — único wikilink é para a nota 08 deste galho. **Não é gap de
  núcleo** (mesma justificativa da nota 02). Registra o arquivamento do repositório "Make
  Real" do tldraw (20/02/2026) como marco histórico, não feature ativa — ver callout de
  caducidade acima.
- **Score:** 11/12 (P1 N/A — nota conceitual; P3 N/A — fase Iniciado; L1 ausente, ver acima).
  M1: 2 mídias — [Christian Lempa — *Excalidraw, my favorite whiteboard / tech diagram app*](https://www.youtube.com/watch?v=Gv9MezPAchI)
  (14:25) e [tldraw (oficial) — *tldraw sync — multiplayer whiteboards in React*](https://www.youtube.com/watch?v=COw7Wm9HS-g)
  (2:38); ambas com legenda auto EN baixada e lida por completo, durações conferidas. Duas
  mídias (uma por ferramenta coberta), dentro do teto da skill.
- **Plano de execução:**
  - nenhuma
- **Resultado:** —

#### 08 - Pipeline de tokens   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 126 linhas · fase: Adepto · status: seedling
- **Núcleo/gaps:** — (piso nominal não atingido — 126 vs. 400 — desvio aceito). Linka
  [[03-Dominios/Tecnologia/CSS/07 - Custom properties e design tokens|Tecnologia/CSS/07]] e
  [[03-Dominios/Engenharia/UX/Linguagem Visual e Design System/29 - Design tokens como sistema|nota 29 do SG5]]
  — confirmado `test -f`. **Consistência de precisão confirmada por grep direto:** DTCG
  tratado como Community Group Report, não padrão W3C, igual à nota 29 do SG5 (linhas 22,
  52–54, 85, 125).
- **Score:** 12/12 (P1 N/A — nota conceitual; P3 N/A — fase Adepto).
  M1: [Figma (oficial) — *Figma Tip: Syncing variables to code*](https://www.youtube.com/watch?v=7gMOTX4f4rc),
  EN, legenda auto baixada e lida por completo; duração conferida (2:01), demonstra ao vivo
  Figma Variables → API → Style Dictionary → CSS/iOS/JS.
- **Plano de execução:**
  - nenhuma
- **Resultado:** —

#### 09 - Loop visual com Playwright MCP e visual regression   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 136 linhas · fase: Magus · status: seedling
- **Núcleo/gaps:** — (piso nominal não atingido — 136 vs. 500 — desvio aceito). Linka
  [[03-Dominios/Tecnologia/Testes JS/14 - Playwright além do básico|Tecnologia/Testes JS/14]]
  (mesmo motor Playwright, papel de teste formal vs. loop de iteração ativa — fronteira
  "insumo, não substituto" confirmada por leitura direta) — confirmado `test -f`. Recusa
  explicitamente citar números de marketing de Percy/Applitools (alegação de fornecedor),
  consistente com a regra do domínio.
- **Score:** 12/12 (P1 N/A — nota conceitual, sem seção de código; P3 N/A por natureza de
  galho — mecanismo explicado com atribuição à fonte primária `microsoft/playwright-mcp`,
  não a autor/ano de estudo nomeado, ver Régua de análise acima).
  M1: [Alex McFarland — *Claude Code Can Now Control Your Browser (Setup Guide)*](https://www.youtube.com/watch?v=ZewsZZ3_iQs),
  EN, legenda auto baixada e lida por completo; duração conferida (15:36).
- **Plano de execução:**
  - nenhuma
- **Resultado:** —

---

## Próximos passos

1. ✅ Scaffold do galho (`index.md` + este roadmap) — Task 0, 2026-07-28.
2. ✅ Escrita das 9 notas, mídia verificada, gate de sintaxe Mermaid — Task 9, rodada de
   escrita, 2026-07-29.
3. ✅ Diagnóstico + nivelamento de nomenclatura (achado Minor 01/02) — Task 9, rodada de
   fechamento, 2026-07-29. Galho considerado **fechado**: 9/9 `➖ não precisa`, zero `⬜`.
4. ⬜ Próxima revisita: recomendada em ~1 ciclo de domínio (não em prazo fixo — este é o
   galho mais perecível, ver callout de caducidade). Ao revisitar, checar primeiro os seis
   pontos do callout de caducidade acima antes de confiar em qualquer outro detalhe.
