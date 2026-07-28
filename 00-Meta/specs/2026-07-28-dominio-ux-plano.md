---
title: "Domínio UX — plano de implementação"
created: 2026-07-28
type: plan
status: draft
publish: false
tags:
  - meta
  - plan
  - ux
  - usabilidade
  - design-system
  - ux-writing
---

# Domínio UX — plano de implementação

> **Base:** [[2026-07-28-dominio-ux-design|design do domínio]].
> **Ritmo:** galho a galho, ponta a ponta. Fecha um sub-galho (semear + verificar +
> diagnosticar + enriquecer) antes de abrir o próximo.

**Goal:** construir o domínio `Engenharia/UX` (48 notas + capstone, 8 sub-galhos por
disciplina) e o galho `Tecnologia/Ferramentas de Design` (9 notas), dando ao engenheiro
full-cycle profundidade real de UX sem formação de designer.

**Arquitetura:** split estável/volátil. O ofício neutro de stack mora em `Engenharia/UX/`;
as ferramentas perecíveis moram em `Tecnologia/Ferramentas de Design/`. Decomposição por
disciplina, com a lente full-cycle aplicada dentro de cada nota.

**Workflow do vault (substitui o ciclo TDD):**
- **Semear nota** → skill `/escrever-nota` (padrão capítulo, núcleo mínimo + opcionais por tema).
- **Gate de qualidade** → skill `/verificar-nota` (ESTRUTURA/PROFUNDIDADE/TAMANHO/LINKS/MÍDIA). É o "teste" de cada nota.
- **Roadmap do galho** → skill `/diagnosticar-galho` (gera `roadmap.md`, pré-condição do enriquecimento).
- **Enriquecer** → skill `/enriquecer-galho` (nota a nota, governança de tokens, roda em Opus/opusplan).

## Global Constraints

- Pastas raiz: `03-Dominios/Engenharia/UX/` e `03-Dominios/Tecnologia/Ferramentas de Design/`
  (sem acento no path "Dominios").
- Notas atômicas em 3 fases; `fase:` no frontmatter conforme o roster do design.
- Padrão capítulo de livro + registro Feynman no enriquecimento; Mermaid onde ajudar.
- Núcleo mínimo obrigatório: TL;DR · abertura-problema · corpo-mecanismo · "O que vem a
  seguir" · Fontes · frontmatter.
- **Toda nota separa o praticável sozinho do que exige time/orçamento.** É a promessa do
  domínio ao seu público, não seção opcional.
- **Toda nota responde "o que eu, sozinho, faço com isso na segunda-feira".** É a mitigação
  contra o eixo por disciplina virar enciclopédia.
- **M1 (mídia verificada) é obrigatório em TODA nota** — decisão do usuário em 2026-07-28,
  alinhando UX ao padrão do domínio Acessibilidade (21 vídeos verificados em 21 notas).
  Sobrepõe-se à isenção parcial de M1 que a skill `verificar-nota` concede à fase Iniciado e
  à regra de estado do `diagnosticar-galho` que fecharia a nota em `➖` por score. Uma nota
  sem mídia verificada não fecha. Vale para as notas novas e, retroativamente, para as 14 já
  escritas (ver Task 11).
- **Não recopiar fronteira** — linkar. Ver a tabela de fronteiras da spec (9 entradas).
- **Não inventar dados do usuário** (projetos/clientes/casos). Exemplos genéricos ou marcados.
- **Não afirmar o não-verificado.** A spec lista 9 itens (seção "Rigor de fontes"); cada um
  entra como ressalva explícita na nota que o cita, nunca como fato.
- Commits: paths explícitos, `git diff --cached` antes; **sem trailer `Co-Authored-By`**.
- O repo tem modificações pendentes não relacionadas — **sempre `git add` por path
  explícito**, nunca `git add -A` ou `git add .`.

---

## Task 0: Scaffold dos dois galhos

**Files:**
- Create: `03-Dominios/Engenharia/UX/index.md` (`type: moc`)
- Create: `03-Dominios/Engenharia/UX/roadmap.md` (galho-pai, `Template - Roadmap`)
- Create: as 8 sub-pastas de `UX/` com `index.md` cada (SG1–SG8)
- Create: `03-Dominios/Tecnologia/Ferramentas de Design/index.md` + `roadmap.md`
- Modify: `03-Dominios/Engenharia/index.md` (entrar na lista de domínios da camada)
- Modify: `03-Dominios/Tecnologia/index.md` (entrar na lista de domínios da camada)
- Modify: `00-Meta/Roadmap.md` (registrar UX como construção nova em andamento)

**Produces:** estrutura navegável dos dois galhos + MOC agrupado por fase + entradas nos
índices de camada.

- [ ] **Passo 1:** criar `UX/index.md` — TL;DR + tabela dos 8 sub-galhos + roster agrupado
  por fase + seção Fronteiras (a tabela de 9 entradas da spec, em forma de callout).
- [ ] **Passo 2:** criar `UX/roadmap.md` do galho-pai (mapa de estado dos 8 sub-galhos,
  recursivo raiz → sub-galho → nota).
- [ ] **Passo 3:** criar as 8 sub-pastas + `index.md` stub de cada uma.
- [ ] **Passo 4:** criar `Ferramentas de Design/index.md` + `roadmap.md`, com callout de
  caducidade (`[!warning]`: galho perecível, revalidar ferramentas a cada ciclo).
- [ ] **Passo 5:** adicionar UX na lista de domínios de `Engenharia/index.md` e Ferramentas
  de Design na de `Tecnologia/index.md`.
- [ ] **Passo 6:** registrar no `00-Meta/Roadmap.md` (construção nova em andamento, com
  contagem-alvo 48+1 e 9).
- [ ] **Passo 7:** `git diff --cached` + commit
  (`docs(ux): scaffold do dominio UX — index, roadmap, 8 sub-galhos + Ferramentas de Design`).

---

## Task 1: SG1 — Fundamentos e modelo mental (Iniciado, 5 notas)

**Files (Create):** `03-Dominios/Engenharia/UX/Fundamentos e Modelo Mental/`
- `01 - UX não é tela - o ofício e seus limites.md`
- `02 - Affordances e signifiers.md`
- `03 - As 10 heurísticas de Nielsen.md`
- `04 - Leis de UX - Fitts, Hick, Jakob, Miller, Peak-End.md`
- `05 - Gestalt aplicada a UI.md`

**Fronteiras a linkar:** `Tecnologia/Acessibilidade/index` na nota 01 (o vizinho já
coberto); nada mais — este sub-galho é fundação.

**Atenção:** a nota 01 é onde o domínio declara seu recorte — o que o engenheiro faz
sozinho e o sinal de que é hora de chamar um especialista. É a nota que define o tom de
todas as outras; escrever com cuidado extra.

Para **cada** nota (01→05):
- [ ] **Passo A:** semear com `/escrever-nota` (`fase: Iniciado`).
- [ ] **Passo B:** gate com `/verificar-nota`; corrigir o que reprovar.
- [ ] **Passo C:** commit com path explícito.

Ao fechar as 5:
- [ ] **Passo D:** `/diagnosticar-galho "Fundamentos e Modelo Mental"` → `roadmap.md`.
- [ ] **Passo E:** `/enriquecer-galho "Fundamentos e Modelo Mental"` até ✅.
- [ ] **Passo F:** atualizar `UX/roadmap.md` (SG1 → ✅) + commit.

---

## Task 2: SG2 — Descoberta e pesquisa (Iniciado/Adepto, 9 notas)

**Files (Create):** `03-Dominios/Engenharia/UX/Descoberta e Pesquisa/06..14 - <título>.md`

06 Generativa vs avaliativa · 07 Entrevista de descoberta - as regras do Mom Test ·
08 Cliente não é usuário - a armadilha do B2B/consultoria · 09 Jobs To Be Done - as duas
escolas · 10 Opportunity Solution Tree de bolso · 11 Assumption mapping · 12 Proto-persona
vs persona de verdade · 13 Teste de usabilidade guerrilha com 5 usuários · 14 Personas
sintéticas e síntese por IA.

**Fases:** 06-08 `Iniciado`; 09-14 `Adepto`.

**Fronteiras:** `Tecnologia/IA/index` na nota 14.

**Notas críticas deste sub-galho:**
- **08** é uma das duas notas-espinha do domínio para este público. Precisa ser concreta
  sobre o conflito: quem paga aprova, quem usa sofre.
- **13** deve trazer o caveat honesto — Nielsen recomenda 3 rodadas de 5, não uma.
- **14** carrega três não-verificados da spec: os percentuais de adoção (69%, 88%) vêm de
  blogs de fornecedores; marcar como sinal de mercado, não estudo. A crítica acadêmica às
  personas sintéticas é o ponto da nota, não o hype.

- [ ] Para cada nota 06→14: `/escrever-nota` → `/verificar-nota` → commit.
- [ ] `/diagnosticar-galho "Descoberta e Pesquisa"` → `roadmap.md`.
- [ ] `/enriquecer-galho "Descoberta e Pesquisa"` até ✅ (9 notas — respeitar governança de
  tokens, parada para checagem no meio).
- [ ] Atualizar `UX/roadmap.md` (SG2 → ✅) + commit.

---

## Task 3: SG4 — Design de interação (Adepto, 7 notas)

> Executado antes de SG3 e SG5 por decisão de ordem da spec: é o que se usa no próximo
> projeto.

**Files (Create):** `03-Dominios/Engenharia/UX/Design de Interação/19..25 - <título>.md`

19 Do fluxo antes da tela - user flow como máquina de estados · 20 Os 5 estados de tela ·
21 Progressive disclosure · 22 Modal vs página vs drawer · 23 Undo vs confirmação ·
24 Design de formulários - defaults · 25 Latência percebida e feedback.

**Fases:** todas `Adepto`.

**Fronteiras:** `Tecnologia/HTML/06 - Formulários II` e `Tecnologia/Acessibilidade/Construir
Acessível/07 - Formulários acessíveis de verdade` na nota 24; `Tecnologia/Web Performance`
na nota 25; `Tecnologia/Acessibilidade/Construir Acessível/06 - Gestão de foco em SPAs` na
nota 22 (foco em modal).

**Atenção:** a nota 25 deve marcar como **não consenso** a superioridade de skeleton
screens sobre spinners — há contestação na literatura.

- [ ] Para cada nota 19→25: `/escrever-nota` (`fase: Adepto`) → `/verificar-nota` → commit.
- [ ] `/diagnosticar-galho "Design de Interação"` → `roadmap.md`.
- [ ] `/enriquecer-galho "Design de Interação"` até ✅.
- [ ] Atualizar `UX/roadmap.md` (SG4 → ✅) + commit.

---

## Task 4: SG6 — UX writing e content design (Adepto, 5 notas)

> Território 100% novo no vault — maior ganho marginal do domínio.

**Files (Create):** `03-Dominios/Engenharia/UX/UX Writing e Content Design/33..37 - <título>.md`

33 Voz e tom · 34 Microcopy, labels de ação e jargão interno · 35 Erros - fluxo de
recuperação e mensagem que não culpa · 36 Estados vazios como conteúdo · 37 i18n quebra
layout.

**Fases:** todas `Adepto`.

**Fronteiras:** nota 36 linka a nota 20 (Os 5 estados de tela) — mesma superfície, ângulos
diferentes: 20 é o espaço de estados, 36 é o conteúdo dentro do estado. Deixar a divisão
explícita nas duas notas para não virar duplicação.

**Atenção:** não afirmar o ano da 2ª edição de *Strategic Writing for UX* (Podmajersky) —
não confirmado.

- [ ] Para cada nota 33→37: `/escrever-nota` (`fase: Adepto`) → `/verificar-nota` → commit.
- [ ] `/diagnosticar-galho "UX Writing e Content Design"` → `roadmap.md`.
- [ ] `/enriquecer-galho "UX Writing e Content Design"` até ✅.
- [ ] Atualizar `UX/roadmap.md` (SG6 → ✅) + commit.

---

## Task 5: SG5 — Linguagem visual e design system (Adepto/Magus, 7 notas)

**Files (Create):** `03-Dominios/Engenharia/UX/Linguagem Visual e Design System/26..32 - <título>.md`

26 Hierarquia visual · 27 Escalas de tipografia, espaçamento e densidade · 28 Cor de
produto - OKLCH e paleta semântica · 29 Design tokens como sistema · 30 Atomic Design - o
que ainda vale · 31 Component API design · 32 Adotar vs construir, e governança mínima.

**Fases:** 26-28 `Adepto`; 29-32 `Magus`.

**Fronteiras — o sub-galho de maior risco de duplicação. Linkar, não reescrever:**
- nota 28 → `Tecnologia/Acessibilidade/Construir Acessível/11 - Cor, contraste e visual
  acessível` (contraste) e skill `dataviz` (paleta de dados ≠ paleta de produto).
- nota 29 → `Tecnologia/CSS/07 - Custom properties e design tokens` (a mecânica CSS já
  está lá; aqui é o **sistema**: hierarquia primitivo→semântico→componente e o padrão DTCG).
- nota 32 → `Tecnologia/React/Ecossistema/03` (a comparação técnica MUI/Radix/shadcn já
  está lá; aqui é o **quando adotar** como decisão de produto).
- Style Dictionary como ferramenta de build é candidato a nota em `Tooling e Build`, não
  aqui — apenas mencionar e apontar.

**Atenção a não-verificados:** o padrão W3C DTCG atingiu primeira versão estável em
out/2025 mas segue **Community Group Report, não padrão W3C**. APCA **não** é padrão de
conformidade — foi retirado do working draft de WCAG 3 em 2023; **WCAG 2.2 é o vigente**.

- [ ] Para cada nota 26→32: `/escrever-nota` → `/verificar-nota` → commit.
- [ ] `/diagnosticar-galho "Linguagem Visual e Design System"` → `roadmap.md`.
- [ ] `/enriquecer-galho "Linguagem Visual e Design System"` até ✅.
- [ ] Atualizar `UX/roadmap.md` (SG5 → ✅) + commit.

---

## Task 6: SG3 — Arquitetura de informação (Adepto, 4 notas)

**Files (Create):** `03-Dominios/Engenharia/UX/Arquitetura de Informação/15..18 - <título>.md`

15 Os 4 sistemas da AI · 16 Schema de banco não é estrutura de navegação · 17 Card sorting
e tree testing de guerrilha · 18 Navegação e wayfinding.

**Fases:** todas `Adepto`.

**Fronteiras:** nota 16 linka `Engenharia/Dados` (modelagem) e `Engenharia/Arquitetura` —
o ponto é o contraste, não a modelagem em si. Nota 17 linka a nota 13 (teste guerrilha),
mesmo espírito de método leve.

- [ ] Para cada nota 15→18: `/escrever-nota` (`fase: Adepto`) → `/verificar-nota` → commit.
- [ ] `/diagnosticar-galho "Arquitetura de Informação"` → `roadmap.md`.
- [ ] `/enriquecer-galho "Arquitetura de Informação"` até ✅.
- [ ] Atualizar `UX/roadmap.md` (SG3 → ✅) + commit.

---

## Task 7: SG7 — Medir, validar e sustentar (Magus, 8 notas)

**Files (Create):** `03-Dominios/Engenharia/UX/Medir, Validar e Sustentar/38..45 - <título>.md`

38 HEART + Goals-Signals-Metrics · 39 SUS, UMUX-Lite, SUPR-Q, SEQ · 40 NPS e North Star -
promessa, crítica e Goodhart · 41 Instrumentação - event taxonomy e tracking plan ·
42 Quando A/B não se aplica · 43 Session replay e heatmap · 44 UX debt e matriz severidade
× esforço · 45 Defender decisão de UX com número.

**Fases:** todas `Magus`.

**Fronteiras:** nota 38 precisa de **nota-ponte curta** com `Tecnologia/Web Performance`
(INP/LCP/CLS já estão lá) — a formulação: *performance é insumo de UX, não a mesma coisa;
mau INP pode explicar task success ruim, mas a métrica em si pertence ao outro domínio*.
Nota 41 linka `Engenharia/Operação` (feature flags, progressive delivery).

**Notas críticas deste sub-galho:**
- **42** é a segunda nota-espinha do domínio: cliente único e B2B não são "azar", são a
  condição normal deste público. Alternativas legítimas (feature flag como desenho
  experimental mínimo, micro-conversões, qualitativo como método de primeira classe)
  precisam aparecer como método, não como consolo.
- **45** deve tratar o ROI de UX como estimativa com atribuição causal frágil. A citação
  Forrester ("$1 → $100") é **não-verificada** — se citada, marcar como tal.

- [ ] Para cada nota 38→45: `/escrever-nota` (`fase: Magus`) → `/verificar-nota` → commit.
- [ ] `/diagnosticar-galho "Medir, Validar e Sustentar"` → `roadmap.md`.
- [ ] `/enriquecer-galho "Medir, Validar e Sustentar"` até ✅ (8 notas Magus — o bloco mais
  caro; respeitar governança de tokens).
- [ ] Atualizar `UX/roadmap.md` (SG7 → ✅) + commit.

---

## Task 8: SG8 — Ética e ofício (Magus, 3 notas)

**Files (Create):** `03-Dominios/Engenharia/UX/Ética e Ofício/46..48 - <título>.md`

46 Dark patterns e regulação · 47 UX no ciclo de dev · 48 UX em entrevista sênior/staff.

**Fases:** todas `Magus`.

**Fronteiras:** nota 47 linka `Engenharia/Testes`, `Engenharia/Operação` e
`Tecnologia/Acessibilidade/Sustentar e Conformidade/17 - A11y no ciclo de desenvolvimento`
(mesmo padrão de gate, disciplina diferente). Nota 48 linka
`Carreira/Entrevistas` e `Tecnologia/Acessibilidade/Sustentar e Conformidade/20 - A11y em
entrevista`.

**Atenção à caducidade:** a nota 46 cita cenário regulatório — EU DMA em vigor, **EU
Digital Fairness Act ainda em tramitação** (proposta esperada para o fim de 2026), ações
da FTC. Marcar `[!info]` de data e **verificar vigência na data da escrita**, no mesmo
padrão da nota 18 do domínio de Acessibilidade.

- [ ] Para cada nota 46→48: `/escrever-nota` (`fase: Magus`) → `/verificar-nota` → commit.
- [ ] `/diagnosticar-galho "Ética e Ofício"` → `roadmap.md`.
- [ ] `/enriquecer-galho "Ética e Ofício"` até ✅.
- [ ] Atualizar `UX/roadmap.md` (SG8 → ✅) + commit.

---

## Task 9: Galho Ferramentas de Design (Tecnologia, 9 notas)

> Deixado por último de propósito: é a parte mais perecível do domínio, então quanto mais
> tarde for escrita, mais tempo de validade terá.

**Files (Create):** `03-Dominios/Tecnologia/Ferramentas de Design/01..09 - <título>.md`

01 Figma para o engenheiro · 02 Figma MCP Server + Code Connect · 03 Claude Design e o
handoff bundle · 04 Geradores de UI por IA · 05 Estética genérica de IA e como escapar ·
06 Protótipo em código · 07 Excalidraw e tldraw · 08 Pipeline de tokens · 09 Loop visual
com Playwright MCP e visual regression.

**Fases:** 01, 06, 07 `Iniciado`; 02-05, 08 `Adepto`; 09 `Magus`.

**Fronteiras:** nota 03 linka a skill `handoff-design` já existente (não duplicar o
"como fazer") e `Tecnologia/IA/Claude Code`. Nota 05 linka `Tecnologia/IA/Image Prompting`
(mesma raiz: convergência do modelo para o estatisticamente seguro). Nota 08 linka
`Tecnologia/CSS/07` e a nota 29 (design tokens como sistema). Nota 09 linka
`Tecnologia/Testes JS/14 - Playwright além do básico`.

**Atenção a não-verificados — este é o galho de maior risco factual:**
- O comando `/design-sync` do Claude Design **não foi confirmado** na doc oficial da
  Anthropic (só em blog de terceiros). Não afirmar que existe.
- A data da integração bidirecional Figma ↔ Claude Code (fev/2026) vem de **fonte
  secundária**. Verificar na doc antes de afirmar.
- Claude Design é **research preview** (17/abr/2026, sobre Opus 4.7); a doc oficial não
  detalha limites técnicos. Tratar como ferramenta de visual/protótipo, não de app
  funcional completo, até prova em contrário.
- Não citar preço de ferramenta nenhuma — nenhum foi verificado.
- Todo o galho leva callout `[!warning]` de caducidade com data de escrita.

- [ ] Para cada nota 01→09: `/escrever-nota` → `/verificar-nota` → commit.
- [ ] `/diagnosticar-galho "Ferramentas de Design"` → `roadmap.md`.
- [ ] `/enriquecer-galho "Ferramentas de Design"` até ✅.
- [ ] Atualizar `roadmap.md` do galho + commit.

---

## Task 10: Capstone + fechamento do domínio

**Files:**
- Create: `03-Dominios/Engenharia/UX/49 - Capstone - do requisito ao produto validado.md`
  (`fase: Magus`)
- Modify: `00-Meta/Roadmap.md` (UX → ✅, contagem final e data)
- Modify: `UX/index.md` e `UX/roadmap.md` (estado final)
- Modify: `Tecnologia/Ferramentas de Design/index.md` e `roadmap.md` (estado final)

- [ ] **Passo 1:** semear o capstone — um ciclo completo costurando os 8 sub-galhos:
  descobrir com o cliente (SG2) → definir e estruturar (SG3) → desenhar fluxo e telas
  (SG4) → materializar com sistema e texto (SG5, SG6) → instrumentar e medir (SG7) →
  priorizar a dívida e sustentar (SG7, SG8). `/escrever-nota` → `/verificar-nota` → commit.
- [ ] **Passo 2:** enriquecer o capstone se o gate pedir.
- [ ] **Passo 3:** rodar `/verificar-wikilinks` no domínio inteiro — com 58 notas novas e
  ~15 fronteiras cruzadas, link quebrado é o modo de falha mais provável.
- [ ] **Passo 4:** atualizar `00-Meta/Roadmap.md` — UX ✅, contagem final (49 + 9 = 58) e data.
- [ ] **Passo 5:** atualizar memória (`project_*` de UX + linha no `MEMORY.md`).
- [ ] **Passo 6:** commit de fechamento
  (`docs(ux): dominio UX COMPLETO — 49 notas + Ferramentas de Design 9/9`).

---

## Task 11: Retrofit de mídia (M1) nas 14 notas já escritas

> Inserida em 2026-07-28, depois da decisão de tornar M1 obrigatório. Executa fora da ordem
> numérica: roda logo após a Task 2, antes da Task 3, para que o padrão fique uniforme desde
> cedo e não gere uma dívida crescente.

**Files (Modify):**
- `03-Dominios/Engenharia/UX/Fundamentos e Modelo Mental/01..05` (5 notas, SG1)
- `03-Dominios/Engenharia/UX/Descoberta e Pesquisa/06..14` (9 notas, SG2)
- os dois `roadmap.md` de sub-galho + `UX/roadmap.md` (reclassificar estados)

**Estado atual:** 0 das 14 notas tem vídeo. O enriquecimento até aqui fechou 4 notas com
podcast/URL de referência (08, 09 e duas do SG1); as outras 10 fecharam `➖` por score.

**Critério de aceitação:** cada uma das 14 notas tem pelo menos uma mídia **verificada**
(vídeo preferencialmente; podcast ou talk quando não houver vídeo bom). Verificada significa
que a URL foi conferida e o conteúdo corresponde ao que a nota afirma — não basta plausível.
Vale a constraint do domínio: não afirmar o não-verificado.

- [ ] Para cada nota 01→14: buscar mídia pertinente, **verificar** a URL e o conteúdo,
  inserir no padrão do vault (mesmo formato usado no domínio Acessibilidade), commitar.
- [ ] Reclassificar os estados nos `roadmap.md` dos dois sub-galhos (`➖` por isenção de M1
  deixa de ser válido).
- [ ] Atualizar `UX/roadmap.md` e registrar a política de M1 obrigatório no `UX/index.md`,
  para que quem retomar o domínio depois saiba a regra.

---

## Self-review (cobertura da spec)

- Os 8 sub-galhos + capstone da spec têm task (Task 1–8, 10). ✓
- Galho `Tecnologia/Ferramentas de Design` (9 notas) tem task própria (Task 9). ✓
- Scaffold dos dois galhos + entradas nos índices de camada + Roadmap central: Task 0. ✓
- Ordem de execução da spec (SG1→SG2→SG4→SG6→SG5→SG3→SG7→SG8→Ferramentas→capstone)
  respeitada na numeração das tasks. ✓
- As 9 entradas da tabela de fronteiras da spec estão distribuídas nas tasks certas:
  Acessibilidade (T1, T3, T5, T8) · CSS/07 (T5, T9) · React/Ecossistema/03 (T5) ·
  Web Performance (T3, T7) · Testes JS/14 (T9) · dataviz (T5) · IA/Claude Code +
  handoff-design (T9) · Tooling e Build/Style Dictionary (T5, apontado não escrito) ·
  React/Ecossistema 10-11 (sem task — só link, correto). ✓
- Os 9 não-verificados da spec estão alocados: personas sintéticas/percentuais (T2) ·
  skeleton vs spinner (T3) · Podmajersky 2ª ed (T4) · DTCG e APCA (T5) · Forrester ROI (T7) ·
  EU Digital Fairness Act (T8) · `/design-sync` e Figma↔Claude Code (T9) · citação Ford
  (não alocada — cortar de qualquer nota, é apócrifa e dispensável). ✓
- Constraint "praticável sozinho vs exige time" e "o que faço na segunda-feira" estão em
  Global Constraints, valendo para toda task. ✓
- Fora de escopo da spec (a11y técnica, branding, mobile nativo, formação de designer,
  design de software) — nenhuma task o viola. ✓
- Risco de duplicação SG6/36 ↔ SG4/20 (estados vazios) tratado explicitamente na Task 4. ✓
- Caducidade sinalizada onde importa: T8 (regulação) e T9 (galho inteiro). ✓
